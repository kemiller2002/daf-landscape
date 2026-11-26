#!/usr/bin/env python3
"""Size-match Chariot's DAF Fundraising Report participants on contributions, not on BMF revenue (P-B40N1202-B43N26-02).

Chariot/K2D 2026: "$26.1 billion in total giving across 54 participating nonprofits", growth measured "from 2021 to
2025" ("across all five years in this study"). $26.1bn / 54 / 5 = $96.7m of giving per participant-year if the panel
is balanced. The committed comparisons (b40n12, b40n1202-b43n26 s2.2/s3) matched that figure against BMF REVENUE_AMT
bands ($25-100m, >=$100m). Here the match is on each sampled recipient's OWN FY2023-24 Form 990 Part VIII
contributions: a recipient is in the Chariot-like domain when its 1h - 1d - 1e (= 1a + 1b + 1c + 1f; 990-EZ line 1)
averaged over its matched FY2023/2024 returns is in [$50m, $200m) a year.

Everything upstream is reused, read from caches only, by importing scripts/mission_coverage_gap.py (which imports
mission_non_top50_numerator.py and the committed recipient-share modules); nothing is modified:
  - committed frame, stratified sample (seed 20261119), return choice and Part VIII caches;
  - numerators:
      top50_unscaled    top-50 DAFRC sponsors' Schedule I, net of DAF-to-DAF, DAF-weighted (committed study basis)
      all_panel_floor   every itemising DAFRC panel sponsor (b40n1202-01 'measured floor')
      central           b40n120201-01 central bounded allocation rw_capall_s10_ni50 (repo central 9.2% / 13.7%)
      env_low           only_non_itemising_top50 (sub-$5,000 component dropped; envelope low, about 8.8% / 13.2%)
      env_high          sens_plus_d2d_residual_all (DAF-to-DAF residual also allocated; envelope high)
  - stratum weights N_h / (n_h - unread), the weighted median and the pooled ratio as in rbe.summary_a.

Bootstrap: within each stratum the full sampled set (all frame parts) is resampled with replacement, THEN the
size domain is applied, so the domain's respondent count varies across replicates (a domain estimator, unlike
rbe.boot, which resamples inside a fixed subset). Weights are held fixed, as in the repo.

Pure functions; I/O only in load_state (caches) and main. Stdlib only.

Usage:
  S=<scratchpad>
  python3 scripts/mission_chariot_size_match.py . --np-cache $S/npcache --lines-cache-top50 $S/rcp/lines \
      --lines-cache $S/q120201/lines --bmf-dir $S/rcp/bmf --index-dir $S/irs --p8-cache $S/q1226/f990p8 \
      --p8-cache-new $S/q120201/f990p8 --p9-cache $S/q12011/p9 [--boot 1000]
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_coverage_gap as cg  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_net_payout import norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import COST, WHITELIST, annotate, load_lines  # noqa: E402

n50, base, rbe = cg.n50, cg.base, cg.rbe
OUT = os.path.join(DATA, "chariot-size-match-2026-11-20.csv")
BASES = ("b1_1h", "b3_1abcf")

# ---- Chariot arithmetic (quoted inputs; see research doc source register)
CHARIOT_TOTAL_GIVING = 26.1e9
CHARIOT_DAF_REVENUE = 3.3e9
CHARIOT_PARTICIPANTS = 54
CHARIOT_YEARS = 5  # 2021-2025 inclusive
CHARIOT_URL = "https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release"

NUMERATORS = ("top50_unscaled", "all_panel_floor", "central", "env_low", "env_high")
SCEN_OF = {"all_panel_floor": "measured_floor", "central": cg.CENTRAL, "env_low": "only_non_itemising_top50",
           "env_high": "sens_plus_d2d_residual_all"}
TOP50_COVERAGE = 0.6727  # committed 1/0.6727 scaling, reported only as the legacy [I] comparison

M = 1e6
# domain name -> (size variable, lo, hi[, extra filter]). size variables: avg_b3 = own (1h-1d-1e)/yr; avg_b1 = own 1h/yr;
# bmf_rev = BMF REVENUE_AMT (the committed matching variable, for contrast)
DOMAINS = {
    "all_recipients": ("avg_b3", float("-inf"), float("inf")),
    "chariot_b3avg_50m_200m": ("avg_b3", 50 * M, 200 * M),
    "chariot_b3avg_50m_200m_ex_intermediaries": ("avg_b3", 50 * M, 200 * M, "not_intermediary"),
    "chariot_b3avg_50m_200m_ex_leaked_daf_sponsors": ("avg_b3", 50 * M, 200 * M, "not_leaked"),
    "chariot_b3avg_50m_200m_form990_only": ("avg_b3", 50 * M, 200 * M, "form990_only"),
    "b3avg_75m_125m": ("avg_b3", 75 * M, 125 * M),
    "b3avg_48m_193m_half_to_double": ("avg_b3", 0.5 * 96.67 * M, 2 * 96.67 * M),
    "b3avg_ge_50m": ("avg_b3", 50 * M, float("inf")),
    "b3avg_25m_100m": ("avg_b3", 25 * M, 100 * M),
    "b3avg_ge_100m": ("avg_b3", 100 * M, float("inf")),
    "b3avg_ge_200m": ("avg_b3", 200 * M, float("inf")),
    "b1avg_50m_200m": ("avg_b1", 50 * M, 200 * M),
    "bmf_rev_50m_200m": ("bmf_rev", 50 * M, 200 * M),
    "bmf_rev_25m_100m": ("bmf_rev", 25 * M, 100 * M),
    "bmf_rev_ge_100m": ("bmf_rev", 100 * M, float("inf")),
}
HEADLINE = "chariot_b3avg_50m_200m"
FILTERS = {"not_intermediary": lambda u: not u["intermediary"], "not_leaked": lambda u: not u["leaked"],
           "form990_only": lambda u: bool(u["forms"]) and "IRS990EZ" not in u["forms"]}
SRC = ("Recipients: b40n1202-01 committed-frame sample, Form 990 Part VIII 1a-1h / 990-EZ line 1 FY2023-24 "
       "(GivingTuesday mirror of IRS TEOS XML, gt990datalake-rawdata.s3.amazonaws.com; located via "
       "apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv). Numerators: mission_coverage_gap.py scenarios. "
       "Chariot inputs: " + CHARIOT_URL)


# ----------------------------------------------------------------------------- pure helpers
def chariot_band() -> dict:
    per_py = CHARIOT_TOTAL_GIVING / CHARIOT_PARTICIPANTS / CHARIOT_YEARS
    return {"giving_per_participant_year": per_py, "pooled_daf_share": CHARIOT_DAF_REVENUE / CHARIOT_TOTAL_GIVING,
            "band_lo_ratio": 50 * M / per_py, "band_hi_ratio": 200 * M / per_py,
            "band_geometric_centre": (50 * M * 200 * M) ** 0.5,
            "per_py_if_4_years_avg": CHARIOT_TOTAL_GIVING / CHARIOT_PARTICIPANTS / 4,
            "per_py_if_3_years_avg": CHARIOT_TOTAL_GIVING / CHARIOT_PARTICIPANTS / 3}


def unit_record(rows_by_num: Mapping[str, Mapping], bmf_rev) -> dict:
    """Merge one recipient's per-numerator rbe rows (same matched years, same denominators)."""
    r0 = rows_by_num["top50_unscaled"]
    n_years = len([y for y in r0["years_matched"].split(";") if y])
    return {"ein": r0["ein"], "name": r0["name"], "stratum": r0["stratum"], "status": r0["status"],
            "sample_part": r0["sample_part"], "revenue_band": r0["revenue_band"], "ntee_major_group": r0["ntee_major_group"],
            "leaked": bool(r0["leaked_sponsor_name"]),
            "intermediary": r0["ntee_cd"].startswith("T") or bool(base.INTERMEDIARY_NAME.search(r0["name"].upper())),
            "forms": r0["forms"], "years_matched": r0["years_matched"], "n_years": n_years,
            "den_b1_1h": r0["den_b1_1h"], "den_b3_1abcf": r0["den_b3_1abcf"],
            "avg_b1": r0["den_b1_1h"] / n_years if n_years else None,
            "avg_b3": r0["den_b3_1abcf"] / n_years if n_years else None,
            "bmf_rev": bmf_rev,
            **{f"num_{k}": rows_by_num[k]["num_daf_weighted_matched"] for k in NUMERATORS}}


def in_domain(u: Mapping, dom: str) -> bool:
    var, lo, hi, *extra = DOMAINS[dom]
    v = u.get(var)
    return v is not None and lo <= v < hi and all(FILTERS[f](u) for f in extra)


def usable(u: Mapping, basis: str) -> bool:
    return u["status"] == "ok" and u[f"den_{basis}"] > 0


def stats(units: Sequence[Mapping], w: Mapping, dom: str, numer: str, basis: str) -> dict:
    use = tuple(u for u in units if usable(u, basis) and in_domain(u, dom))
    if not use:
        return {"respondents": 0}
    wt = lambda u: w[u["stratum"]]  # noqa: E731
    den = sum(wt(u) * u[f"den_{basis}"] for u in use)
    nm = sum(wt(u) * u[f"num_{numer}"] for u in use)
    shares = [(u[f"num_{numer}"] / u[f"den_{basis}"], wt(u)) for u in use]
    return {"respondents": len(use), "weighted_recipients": sum(wt(u) for u in use),
            "certainty_respondents": sum(u["stratum"].endswith("certainty") for u in use),
            "pooled_share": nm / den, "median_share": base.wquantile(shares, 0.5),
            "p25_share": base.wquantile(shares, 0.25), "p75_share": base.wquantile(shares, 0.75),
            "weighted_den_usd": den, "weighted_num_usd": nm}


def max_influence(units: Sequence[Mapping], w: Mapping, dom: str, numer: str, basis: str) -> dict:
    """Leave-one-out: the recipient whose removal moves the pooled share most."""
    use = tuple(u for u in units if usable(u, basis) and in_domain(u, dom))
    if len(use) < 2:
        return {}
    wt = lambda u: w[u["stratum"]]  # noqa: E731
    N = sum(wt(u) * u[f"num_{numer}"] for u in use)
    D = sum(wt(u) * u[f"den_{basis}"] for u in use)
    full = N / D
    loo = ((u["ein"], u["name"], (N - wt(u) * u[f"num_{numer}"]) / (D - wt(u) * u[f"den_{basis}"])) for u in use)
    e, n, p = max(loo, key=lambda t: abs(t[2] - full))
    return {"loo_max_ein": e, "loo_max_name": n, "loo_max_pooled_share": p}


def bootstrap(units: Sequence[Mapping], w: Mapping, combos: Sequence[tuple], reps: int, seed: int) -> dict:
    """combo -> {pooled_ci95_lo/hi, median_ci95_lo/hi}. Resample every stratum, then apply the domain."""
    by = _group_by_fast((u for u in units if u["stratum"] in w), lambda u: u["stratum"])
    rng = random.Random(seed)
    draws = (tuple(x for k in sorted(by) for x in rng.choices(by[k], k=len(by[k]))) for _ in range(reps))
    doms = sorted({c[0] for c in combos})

    def point(sub, n, b):
        use = tuple(u for u in sub if u[f"den_{b}"] > 0)
        if not use:
            return {}
        den = sum(w[u["stratum"]] * u[f"den_{b}"] for u in use)
        return {"pooled_share": sum(w[u["stratum"]] * u[f"num_{n}"] for u in use) / den,
                "median_share": base.wquantile([(u[f"num_{n}"] / u[f"den_{b}"], w[u["stratum"]]) for u in use], 0.5)}

    def one_rep(d):
        subs = {dm: tuple(u for u in d if u["status"] == "ok" and in_domain(u, dm)) for dm in doms}
        return {c: point(subs[c[0]], c[1], c[2]) for c in combos}
    reps_out = tuple(map(one_rep, draws))
    pct = lambda xs, q: xs[min(len(xs) - 1, int(q * len(xs)))] if xs else None  # noqa: E731

    def ci(c):
        p = sorted(r[c]["pooled_share"] for r in reps_out if r[c].get("pooled_share") is not None)
        m = sorted(r[c]["median_share"] for r in reps_out if r[c].get("median_share") is not None)
        return {"pooled_ci95_lo": pct(p, 0.025), "pooled_ci95_hi": pct(p, 0.975),
                "median_ci95_lo": pct(m, 0.025), "median_ci95_hi": pct(m, 0.975), "boot_reps_used": len(p)}
    return {c: ci(c) for c in combos}


def size_profile(units: Sequence[Mapping], w: Mapping, dom: str) -> dict:
    """Cross-tab of the domain against BMF revenue bands (weighted recipients), showing what the old match picked."""
    use = tuple(u for u in units if usable(u, "b3_1abcf") and in_domain(u, dom))
    by = _group_by_fast(use, lambda u: u["revenue_band"])
    return {b: {"respondents": len(v), "weighted": round(sum(w[u["stratum"]] for u in v), 1)} for b, v in sorted(by.items())}


# ----------------------------------------------------------------------------- state (caches only)
def load_state(a) -> dict:
    """Rebuild mission_coverage_gap.py's recipient rows for the five numerators, from caches (no network)."""
    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    sy = n50.sponsor_years(pick_returns(load_np(a.np_cache)), panel, rank)
    sy_keys = sorted(sy)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        p9 = dict(zip(sy_keys, ex.map(lambda k: cg.fetch_p9(sy[k]["x"]["oid"], a.p9_cache, False), sy_keys)))
    item = {k: v for k, v in sy.items() if v["pre"] == "itemised"}

    def lines(k):
        v = item[k]
        return load_lines(v["x"]["oid"], v["x"]["sched_i_lines"],
                          a.lines_cache_top50 if v["tier"] == "top50" else a.lines_cache, [], False)
    keys = sorted(item)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        loaded = dict(zip(keys, ex.map(lines, keys)))
    good = {k: drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    tiers = {k: item[k]["tier"] for k in good}
    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    groups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in groups.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    cost = read_csv(COST)
    weights, _ = n50.weight_fallback(base.sponsor_weights(cost, good), {k: item[k] for k in good}, 1.0)

    net_rows = [r for r in read_csv(base.NETTED_CSV) if r["metric"] == "daf_grants" and r["tier"] == "central"]
    netted = {int(r["fiscal_year"]): num(r["netted_value"]) for r in net_rows}
    netting = {int(r["fiscal_year"]): num(r["r5_netting_amount"]) for r in net_rows}
    deltas = cg.corrected_deltas(read_csv(cg.CORR_CSV))
    d_raw = {(ein9(r["ein"]), int(r["fiscal_year_end"])): num(r.get("total_daf_grants")) or 0.0
             for r in dafrc if r["fiscal_year_end"] in tuple(map(str, FYS))}
    rows_item = tuple(cg.sponsor_row(k, p9.get(k, {}), item[k]["x"], weights[k], d_raw.get(k, 0.0),
                                     d_raw.get(k, 0.0) + deltas.get(k, 0.0), ann[k]) for k in sorted(good))
    w2 = {(r["ein"], r["fiscal_year"]): r["w2"] for r in rows_item}
    w_all = base.sponsor_weights(cost, sy)

    def non_item_row(k):
        x = sy.get(k)
        q = p9.get(k, {}) if x else {}
        ok = q.get("status") == "ok"
        l13 = ((q.get("l1") or 0.0) + (q.get("l3") or 0.0)) if ok else 0.0
        return {"ein": k[0], "fiscal_year": k[1], "d_raw": d_raw.get(k, 0.0), "d_corr": d_raw.get(k, 0.0) + deltas.get(k, 0.0),
                "w": w_all.get(k), "dom_share": ((q.get("l1") or 0.0) / l13) if l13 > 0 else None}
    ni_keys = sorted(k for k in set(d_raw) | {k for k in deltas if k[1] in FYS} if k not in good and k[0] in panel)
    non_item = tuple(r for r in map(non_item_row, ni_keys) if r["d_corr"])
    dec = {w_: {fy: cg.decompose(rows_item, non_item, netted, netting, fy, w_) for fy in FYS} for w_ in ("A", "B")}
    split = {fy: cg.domestic_split(rows_item, non_item, fy) for fy in FYS}

    def numer(wts):
        a50 = {k: v for k, v in ann.items() if tiers[k] == "top50"}
        aot = {k: v for k, v in ann.items() if tiers[k] == "other"}
        return n50.combine(base.numerators(a50, wts), base.numerators(aot, wts))
    comb = {"w": numer(weights), "w2": numer(w2)}
    keysets = {"w": cg.line_keys(ann, weights, tiers), "w2": cg.line_keys(ann, w2, tiers)}
    panel_eins = frozenset(panel)
    bmf = base.load_bmf(a.bmf_dir, frozenset(comb["w"]))
    cw = comb["w"]

    def unit(e, c):
        b = bmf[e]
        return {**b, "group": base.group_of(b["ntee"]), "band": base.band_of(b["revenue"]), "num": c["top50"],
                "num_si_total": n50.tot(c["top50"], "si"), "num_oth_si": n50.tot(c["other"], "si"),
                "excl": base.exclusion(b, panel_eins)}
    universe = tuple(unit(e, c) for e, c in cw.items() if e in bmf)
    frame = tuple(u for u in universe if not u["excl"] and u["num_si_total"] > 0)
    new_only = tuple({**u, "num_si_total": u["num_oth_si"]} for u in universe if not u["excl"] and u["num_si_total"] <= 0
                     and u["num_oth_si"] > 0)
    sample = base.draw_sample(frame, a.certainty, a.per_stratum, a.seed)
    supp = tuple({**s, "stratum": "new|" + s["stratum"]}
                 for s in base.draw_sample(new_only, a.supp_certainty, a.supp_per_stratum, a.seed + 1))
    units = tuple({**s, "part": "committed"} for s in sample) + tuple({**s, "part": "new_only"} for s in supp)
    idx = base.load_index(a.index_dir, frozenset(s["ein"] for s in units))
    filings = {s["ein"]: base.choose_filings(idx.get(s["ein"], ())) for s in units}
    oids = sorted({f["oid"] for fs in filings.values() for f in fs.values()})
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        f990 = dict(zip(oids, ex.map(lambda o: n50.p8_lookup(o, a.p8_cache, a.p8_cache_new, False), oids)))

    def nums_for(name):
        if name == "top50_unscaled":
            return {u["ein"]: cw[u["ein"]]["top50"] for u in units}
        spec = cg.SCENARIOS[SCEN_OF[name]]
        if SCEN_OF[name] == "measured_floor":
            return {u["ein"]: cw[u["ein"]]["all"] for u in units}
        al = cg.allocations(dec["A" if spec["weights"] == "w" else "B"], split, spec["rule"])
        c = comb[spec["weights"]]
        return {u["ein"]: cg.alloc_num(u["ein"], c[u["ein"]]["all"], keysets[spec["weights"]], al) for u in units}
    rows = {k: cg.scenario_rows(units, filings, f990, nums_for(k)) for k in NUMERATORS}
    w = rbe.weights_a(rows["all_panel_floor"])
    rev = {u["ein"]: u["revenue"] for u in units}
    recs = tuple(unit_record({k: rows[k][i] for k in NUMERATORS}, rev[rows["top50_unscaled"][i]["ein"]])
                 for i in range(len(units)))
    return {"units": recs, "w": w}


# ----------------------------------------------------------------------------- output rows
FIELDS = ("row_type", "frame", "domain", "size_variable", "size_lo_usd", "size_hi_usd", "domain_filter", "numerator", "basis",
          "respondents", "certainty_respondents", "weighted_recipients", "median_share", "median_ci95_lo",
          "median_ci95_hi", "p25_share", "p75_share", "pooled_share", "pooled_ci95_lo", "pooled_ci95_hi",
          "boot_reps_used", "scaled_pooled_inference", "repo_reference_share", "chariot_pooled_share",
          "chariot_minus_pooled_pts", "loo_max_ein", "loo_max_name", "loo_max_pooled_share",
          "ein", "name", "stratum", "stratum_weight", "revenue_band_bmf", "bmf_revenue_usd", "ntee_major_group",
          "forms", "years_matched", "avg_1h_usd", "avg_1h_less_1d_1e_usd", "num_top50_unscaled", "num_all_panel_floor",
          "num_central", "num_env_low", "num_env_high", "share_central_b1_1h", "share_central_b3_1abcf",
          "share_top50_b3_1abcf", "metric", "value", "source")


def frames_of(units: Sequence[Mapping]) -> dict:
    return {"committed": tuple(u for u in units if u["sample_part"] == "committed"), "expanded": tuple(units)}


def summary_rows(units, w, reps, seed, repo_ref) -> list:
    combos = [(d, n, b) for d in DOMAINS for n in NUMERATORS for b in BASES]
    fr = frames_of(units)
    boots = {f: bootstrap(fr[f], w, combos if f == "committed" else [c for c in combos if c[1] == "central"], reps,
                          seed + (0 if f == "committed" else 7)) for f in fr}
    ch = chariot_band()["pooled_daf_share"]

    def one(f, d, n, b):
        s = stats(fr[f], w, d, n, b)
        var, lo, hi, *extra = DOMAINS[d]
        infl = max_influence(fr[f], w, d, n, b) if d in (HEADLINE, "all_recipients") and f == "committed" else {}
        pl = s.get("pooled_share")
        return {"row_type": "summary", "frame": f, "domain": d, "size_variable": var,
                "size_lo_usd": lo if lo != float("-inf") else "", "size_hi_usd": hi if hi != float("inf") else "", "domain_filter": ";".join(extra),
                "numerator": n, "basis": b, **{k: s.get(k) for k in ("respondents", "certainty_respondents",
                                                                     "weighted_recipients", "median_share", "p25_share",
                                                                     "p75_share", "pooled_share")},
                **boots[f].get((d, n, b), {}),
                "scaled_pooled_inference": (pl / TOP50_COVERAGE) if (pl is not None and n == "top50_unscaled") else None,
                "repo_reference_share": repo_ref.get((n, b)) if d == "all_recipients" else None,
                "chariot_pooled_share": ch if b == "b3_1abcf" else None,
                "chariot_minus_pooled_pts": (100 * (ch - pl)) if (pl is not None and b == "b3_1abcf") else None,
                **infl, "source": SRC}
    return [one(f, d, n, b) for f in fr for d in DOMAINS for n in NUMERATORS for b in BASES
            if f == "committed" or n == "central"]


def recipient_rows(units, w) -> list:
    use = sorted((u for u in frames_of(units)["committed"] if usable(u, "b3_1abcf") and in_domain(u, HEADLINE)),
                 key=lambda u: -u["avg_b3"])
    sh = lambda u, n, b: u[f"num_{n}"] / u[f"den_{b}"] if u[f"den_{b}"] > 0 else None  # noqa: E731
    return [{"row_type": "recipient", "frame": "committed", "domain": HEADLINE, "ein": u["ein"], "name": u["name"],
             "stratum": u["stratum"], "stratum_weight": w[u["stratum"]], "revenue_band_bmf": u["revenue_band"],
             "bmf_revenue_usd": u["bmf_rev"], "ntee_major_group": u["ntee_major_group"], "forms": u["forms"],
             "years_matched": u["years_matched"], "avg_1h_usd": round(u["avg_b1"]),
             "avg_1h_less_1d_1e_usd": round(u["avg_b3"]), **{f"num_{n}": u[f"num_{n}"] for n in NUMERATORS},
             "share_central_b1_1h": sh(u, "central", "b1_1h"), "share_central_b3_1abcf": sh(u, "central", "b3_1abcf"),
             "share_top50_b3_1abcf": sh(u, "top50_unscaled", "b3_1abcf"), "source": SRC} for u in use]


def band_rows() -> list:
    return [{"row_type": "chariot_band", "metric": k, "value": v, "source": CHARIOT_URL} for k, v in chariot_band().items()]


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; repo CLI convention)")
    for k in ("np-cache", "lines-cache-top50", "lines-cache", "bmf-dir", "index-dir", "p8-cache", "p8-cache-new", "p9-cache"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--seed", type=int, default=20261119)
    ap.add_argument("--per-stratum", type=int, default=40)
    ap.add_argument("--certainty", type=int, default=400)
    ap.add_argument("--supp-per-stratum", type=int, default=30)
    ap.add_argument("--supp-certainty", type=int, default=100)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--boot-seed", type=int, default=20261120)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    st = load_state(a)
    units, w = st["units"], st["w"]
    # repo central figures being compared against (b40n120201-01 recommendation; b40n1202-b43n26 s2.1 top-50)
    repo_ref = {("central", "b1_1h"): 0.092, ("central", "b3_1abcf"): 0.137, ("all_panel_floor", "b1_1h"): 0.084,
                ("all_panel_floor", "b3_1abcf"): 0.126, ("top50_unscaled", "b1_1h"): 0.069,
                ("top50_unscaled", "b3_1abcf"): 0.103}
    summ = summary_rows(units, w, a.boot, a.boot_seed, repo_ref)
    rec = recipient_rows(units, w)
    write_csv(a.out, band_rows() + summ + rec, FIELDS)

    r4 = lambda v: round(v, 4) if isinstance(v, float) else v  # noqa: E731
    pick = lambda d, n, b, f="committed": next(s for s in summ if (s["frame"], s["domain"], s["numerator"], s["basis"]) == (f, d, n, b))  # noqa: E731
    out = {"chariot_band": {k: r4(v) for k, v in chariot_band().items()},
           "committed_units": len(frames_of(units)["committed"]),
           "headline": {f"{d}|{n}|{b}": {k: r4(pick(d, n, b)[k]) for k in ("respondents", "weighted_recipients", "pooled_share",
                                                                            "pooled_ci95_lo", "pooled_ci95_hi", "median_share",
                                                                            "median_ci95_lo", "median_ci95_hi", "loo_max_name",
                                                                            "loo_max_pooled_share")}
                        for d in ("all_recipients", HEADLINE) for n in NUMERATORS for b in BASES},
           "domains_central": {f"{d}|{b}": {k: r4(pick(d, "central", b)[k]) for k in ("respondents", "pooled_share",
                                                                                        "pooled_ci95_lo", "pooled_ci95_hi",
                                                                                        "median_share", "median_ci95_lo",
                                                                                        "median_ci95_hi")}
                               for d in DOMAINS for b in BASES},
           "headline_profile_by_bmf_band": size_profile(frames_of(units)["committed"], w, HEADLINE),
           "rows": {"summary": len(summ), "recipient": len(rec), "chariot_band": len(band_rows())}}
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
