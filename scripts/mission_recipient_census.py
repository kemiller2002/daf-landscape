#!/usr/bin/env python3
"""Enlarge the recipient DAF-share sample where it is thin and recompute the headline shares (P-B40N1202-04).

The committed headline (b40n120201-01, mission_coverage_gap.py) is the pooled DAF share of recipient contributions on
the committed frame under the central bounded allocation (scenario rw_capall_s10_ni50): 9.2% on Form 990 Part VIII
line 1h and 13.7% on 1h - 1d - 1e (basis b3_1abcf = 1a + 1b + 1c + 1f). It rests on a certainty stratum of 400 plus a
simple random sample of up to 40 EINs per NTEE major group x BMF revenue band (seed 20261119).

This script keeps that design and adds two things:
  (a) a supplementary simple random sample of --supp-n (150) EINs from each of two thin strata, drawn from the stratum
      members not already sampled, with random.Random(--supp-seed):
          no_ntee|a_lt_1m      (4 in-scope respondents of 40 in the committed sample)
          religion|a_lt_1m     (15 of 40)
      The union of an SRS and an SRS of the remainder is an SRS of the combined size, so the stratum keeps its key and
      N_h, and its weight becomes N_h / (n_old + n_supp - unreadable).
  (b) a census of every committed-frame recipient with BMF REVENUE_AMT >= $25m (revenue bands d_25m_100m and
      e_ge_100m). Certainty-stratum members keep their certainty place; every other member of a d/e stratum is added,
      so those strata are complete (weight N_h / (N_h - unreadable)).
Everything else (frames, numerators, DAF weights, gap decomposition, central allocation, recipient-return choice,
Part VIII reader, weights N_h / (n_h - xml_not_read), pooled estimator, stratified bootstrap) is imported unchanged
from mission_coverage_gap.py, mission_non_top50_numerator.py, mission_recipient_basis_eligibility.py and
mission_daf_share_recipient_revenue.py. The old estimate is reproduced with the exact seed the committed run used.

Standard errors: the SD of B stratified bootstrap replicates of the pooled share (with-replacement within stratum,
as in rbe.boot), reported two ways: `repo` (every stratum resampled, the committed method) and `fpc0` (strata whose
whole membership was sampled are held fixed: a census has no sampling variance; with-replacement resampling of
other strata is kept).

Part VIII extracts: caches q1226/f990p8 and q120201/f990p8 are read first; missing returns are fetched into
--p8-cache-new from the GivingTuesday mirror of IRS TEOS XML (rbe.fetch_part8: streamed, stops after the main form).

Pure functions; I/O only in load/fetch helpers and `main`. Stdlib only. Modifies no existing script.

Usage:
  S=<scratchpad>
  python3 scripts/mission_recipient_census.py . --np-cache $S/npcache --lines-cache-top50 $S/rcp/lines \
      --lines-cache $S/q120201/lines --bmf-dir $S/rcp/bmf --index-dir $S/irs --p8-cache $S/q1226/f990p8 \
      --p8-cache-mid $S/q120201/f990p8 --p8-cache-new $S/b40n120204/f990p8 --p9-cache $S/q12011/p9 [--fetch] [--boot 500]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
import urllib.error
import urllib.request
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
OUT = os.path.join(DATA, "recipient-census-2026-11-20.csv")
UA = "research-script/1.0"
MIRROR = "gt990datalake-rawdata.s3.amazonaws.com"
THIN = ("no_ntee|a_lt_1m", "religion|a_lt_1m")
CENSUS_BANDS = frozenset({"d_25m_100m", "e_ge_100m"})
CENTRAL = cg.CENTRAL
BASES = n50.BASES
SOURCE = ("Numerator: IRS Form 990 Schedule I Part II lines FY2023-24 of every itemising DAFRC 2025 panel sponsor, DAF-weighted, "
          "net of DAF-to-DAF, plus the b40n120201-01 central gap allocation (rw_capall_s10_ni50). Denominator: recipient Form 990 "
          "Part VIII 1a-1h / 990-EZ line 1 (GivingTuesday mirror of IRS TEOS XML, gt990datalake-rawdata.s3.amazonaws.com; "
          "located via apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv). Strata: IRS EO BMF (www.irs.gov/pub/irs-soi/eo*.csv).")


# ----------------------------------------------------------------------------- design
def supplement(frame: Sequence[Mapping], sample: Sequence[Mapping], strata: Sequence[str], n: int, seed: int) -> tuple:
    """SRS of n from each thin stratum's unsampled members (all of them if fewer). Deterministic given seed."""
    taken = frozenset(s["ein"] for s in sample)
    rest = _group_by_fast((u for u in frame if u["ein"] not in taken), lambda u: f"{u['group']}|{u['band']}")
    full = _group_by_fast((u for u in frame if u["ein"] not in frozenset(s["ein"] for s in sample if s["stratum"] == "certainty")),
                          lambda u: f"{u['group']}|{u['band']}")

    def one(i, key):
        members = sorted(rest.get(key, ()), key=lambda r: r["ein"])
        rng = random.Random(seed + i)
        chosen = members if len(members) <= n else rng.sample(members, n)
        return tuple({**r, "stratum": key, "N_h": len(full[key]), "added": "supp_a"} for r in sorted(chosen, key=lambda r: r["ein"]))
    return tuple(x for i, k in enumerate(strata) for x in one(i, k))


def census(frame: Sequence[Mapping], sample: Sequence[Mapping]) -> tuple:
    """Every frame recipient in a census band that is not already in the sample (certainty or SRS)."""
    taken = frozenset(s["ein"] for s in sample)
    cert = frozenset(s["ein"] for s in sample if s["stratum"] == "certainty")
    full = _group_by_fast((u for u in frame if u["ein"] not in cert), lambda u: f"{u['group']}|{u['band']}")
    return tuple({**u, "stratum": f"{u['group']}|{u['band']}", "N_h": len(full[f"{u['group']}|{u['band']}"]), "added": "census_b"}
                 for u in sorted(frame, key=lambda r: r["ein"]) if u["band"] in CENSUS_BANDS and u["ein"] not in taken)


# ----------------------------------------------------------------------------- statistics
def complete_strata(rows: Sequence[Mapping]) -> frozenset:
    by = _group_by_fast(rows, lambda r: r["stratum"])
    return frozenset(k for k, v in by.items() if len(v) >= v[0]["stratum_N"])


def boot_reps(rows: Sequence[Mapping], w: Mapping, basis: str, reps: int, seed: int, fixed: frozenset) -> tuple:
    """Pooled-share replicates; strata in `fixed` are not resampled."""
    use = tuple(r for r in rows if r["status"] == "ok" and r[f"den_{basis}"] > 0)
    by = _group_by_fast(use, lambda r: r["stratum"])
    rng = random.Random(seed)
    keep = tuple(x for k in sorted(by) if k in fixed for x in by[k])
    draw = lambda: keep + tuple(x for k in sorted(by) if k not in fixed for x in rng.choices(by[k], k=len(by[k])))  # noqa: E731
    return tuple(p for p in (rbe.pooled(draw(), w, basis) for _ in range(reps)) if p is not None)


def sd(xs: Sequence[float]):
    if len(xs) < 2:
        return None
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def pct(xs: Sequence[float], q: float):
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))] if s else None


def estimate(rows: Sequence[Mapping], w: Mapping, basis: str, reps: int, seed: int) -> dict:
    """Pooled share, percentile CI and bootstrap SE (repo method and census-fixed)."""
    ok = tuple(r for r in rows if r["status"] == "ok")
    fixed = complete_strata(rows)
    r_repo = boot_reps(rows, w, basis, reps, seed, frozenset())
    r_fpc = boot_reps(rows, w, basis, reps, seed, fixed)
    return {"sampled": len(rows), "respondents": sum(1 for r in ok if r[f"den_{basis}"] > 0),
            "pooled_share": rbe.pooled(ok, w, basis),
            "ci95_lo": pct(r_repo, 0.025), "ci95_hi": pct(r_repo, 0.975), "se_boot": sd(r_repo),
            "ci95_lo_fpc0": pct(r_fpc, 0.025), "ci95_hi_fpc0": pct(r_fpc, 0.975), "se_boot_fpc0": sd(r_fpc),
            "complete_strata": len({r["stratum"] for r in rows} & fixed)}


def se_components(rows: Sequence[Mapping], w: Mapping, basis: str, reps: int, seed: int) -> dict:
    """Bootstrap SE of the pooled share when only one block of strata is resampled (certainty, or the non-certainty
    strata of one revenue band) and every other stratum is held fixed. Shows where the remaining variance sits."""
    strata = frozenset(r["stratum"] for r in rows)
    block = lambda k: "certainty" if k == "certainty" else k.split("|")[-1]  # noqa: E731
    blocks = sorted({block(k) for k in strata})
    return {b: sd(boot_reps(rows, w, basis, reps, seed, frozenset(k for k in strata if block(k) != b))) for b in blocks}


def stratum_rows(rows_old: Sequence[Mapping], rows_new: Sequence[Mapping], w_old: Mapping, w_new: Mapping) -> list:
    bo, bn = _group_by_fast(rows_old, lambda r: r["stratum"]), _group_by_fast(rows_new, lambda r: r["stratum"])

    def one(k):
        o, n = bo.get(k, ()), bn[k]
        cnt = lambda v, st: sum(1 for r in v if r["status"] == st)  # noqa: E731
        return {"row_type": "stratum", "scope": k, "frame": "committed" if not k.startswith("new|") else "new_only",
                "stratum_N": n[0]["stratum_N"], "sampled_old": len(o), "sampled_new": len(n),
                "respondents_old": cnt(o, "ok"), "respondents_new": cnt(n, "ok"),
                "out_of_scope_new": len(n) - cnt(n, "ok") - cnt(n, "xml_not_read"), "xml_not_read_new": cnt(n, "xml_not_read"),
                "weight_old": w_old.get(k), "weight_new": w_new.get(k),
                **{f"pooled_{b}_{t}": rbe.pooled([r for r in v if r["status"] == "ok"], ww, b) if ww.get(k) else None
                   for b in BASES for t, v, ww in (("old", o, w_old), ("new", n, w_new))},
                "source": SOURCE}
    return [one(k) for k in sorted(bn)]


# ----------------------------------------------------------------------------- I/O
def robots_check(log_dir: str) -> str:
    req = urllib.request.Request(f"https://{MIRROR}/robots.txt", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            code, body = r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        code, body = e.code, ""
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "log.tsv"), "a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{MIRROR}\t{code}\t{len(body)}\n")
    groups = body.lower().split("user-agent:")
    ours = ("claudebot", "anthropic-ai", "claude-user", "claude-web", "claude-searchbot", "*")
    hit = any(g.split("\n", 1)[0].strip() in ours and any(l.strip() in ("disallow: /", "disallow: /efiledata")
                                                           for l in g.splitlines()) for g in groups)
    return "blocked" if code == 200 and hit else f"allowed_{code}"


def p8_lookup(oid: str, caches: Sequence[str], new_cache: str, fetch: bool) -> dict:
    hit = next((h for h in (rbe.fetch_part8(oid, c, False) for c in caches) if h.get("status") != "not_fetched"), None)
    return hit if hit is not None else rbe.fetch_part8(oid, new_cache, fetch)


# ----------------------------------------------------------------------------- main
FIELDS = ("row_type", "sample", "frame", "basis", "scope", "scenario", "sampled", "respondents", "pooled_share", "ci95_lo",
          "ci95_hi", "se_boot", "ci95_lo_fpc0", "ci95_hi_fpc0", "se_boot_fpc0", "complete_strata", "se_change", "se_ratio",
          "stratum_N", "sampled_old", "sampled_new", "respondents_old", "respondents_new", "out_of_scope_new",
          "xml_not_read_new", "weight_old", "weight_new", *(f"pooled_{b}_{t}" for b in BASES for t in ("old", "new")),
          "ein", "name", "ntee_cd", "ntee_major_group", "revenue_band", "bmf_revenue_amt", "stratum", "added",
          "years_matched", "forms", "object_ids", "num_daf_weighted_central", "num_daf_weighted_floor",
          *(f"den_{b}" for b in BASES), *(f"share_{b}" for b in BASES), "status", "source")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; repo CLI convention)")
    for k in ("np-cache", "lines-cache-top50", "lines-cache", "bmf-dir", "index-dir", "p8-cache", "p8-cache-mid",
              "p8-cache-new", "p9-cache"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--fetch", action="store_true", help="fetch missing recipient Part VIII extracts")
    ap.add_argument("--fetch-only", action="store_true")
    ap.add_argument("--seed", type=int, default=20261119)
    ap.add_argument("--per-stratum", type=int, default=40)
    ap.add_argument("--certainty", type=int, default=400)
    ap.add_argument("--supp-per-stratum", type=int, default=30)
    ap.add_argument("--supp-certainty", type=int, default=100)
    ap.add_argument("--supp-n", type=int, default=150)
    ap.add_argument("--supp-seed", type=int, default=20261120)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    # ---- sponsor side and numerators, exactly as mission_coverage_gap.main (caches only)
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
        return {"ein": k[0], "fiscal_year": k[1], "tier": "top50" if k[0] in rank else "other",
                "status": "not_in_cache" if x is None else ("lines_" + loaded[k]["status"]) if k in loaded else x["pre"],
                "d_raw": d_raw.get(k, 0.0), "d_corr": d_raw.get(k, 0.0) + deltas.get(k, 0.0), "w": w_all.get(k),
                "l1": q.get("l1") if ok else None, "l2": q.get("l2") if ok else None, "l3": q.get("l3") if ok else None,
                "sf_org_usd": q.get("sf_org_usd") if ok else None, "p9_status": q.get("status", ""),
                "dom_share": ((q.get("l1") or 0.0) / l13) if l13 > 0 else None}
    ni_keys = sorted(k for k in set(d_raw) | {k for k in deltas if k[1] in FYS} if k not in good and k[0] in panel)
    non_item = tuple(r for r in map(non_item_row, ni_keys) if r["d_corr"])
    dec_b = {fy: cg.decompose(rows_item, non_item, netted, netting, fy, "B") for fy in FYS}
    split = {fy: cg.domestic_split(rows_item, non_item, fy) for fy in FYS}

    def numer(wts):
        a50 = {k: v for k, v in ann.items() if tiers[k] == "top50"}
        aot = {k: v for k, v in ann.items() if tiers[k] == "other"}
        return n50.combine(base.numerators(a50, wts), base.numerators(aot, wts))
    cw, c2 = numer(weights), numer(w2)
    keys_w2 = cg.line_keys(ann, w2, tiers)
    panel_eins = frozenset(panel)
    bmf = base.load_bmf(a.bmf_dir, frozenset(cw))

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
    supp_new = tuple({**s, "stratum": "new|" + s["stratum"]}
                     for s in base.draw_sample(new_only, a.supp_certainty, a.supp_per_stratum, a.seed + 1))
    old_units = (tuple({**s, "part": "committed", "added": ""} for s in sample)
                 + tuple({**s, "part": "new_only", "added": ""} for s in supp_new))

    # ---- (a) supplement and (b) census
    add_a = supplement(frame, sample, THIN, a.supp_n, a.supp_seed)
    add_b = census(frame, sample)
    added = tuple({**s, "part": "committed"} for s in add_a + add_b)
    new_units = old_units + added
    ge25 = tuple(u for u in frame if u["band"] in CENSUS_BANDS)

    idx = base.load_index(a.index_dir, frozenset(s["ein"] for s in new_units))
    filings = {s["ein"]: base.choose_filings(idx.get(s["ein"], ())) for s in new_units}
    oids_old = sorted({f["oid"] for s in old_units for f in filings[s["ein"]].values()})
    oids = sorted({f["oid"] for fs in filings.values() for f in fs.values()})
    caches = (a.p8_cache, a.p8_cache_mid)
    robots = robots_check(os.path.join(os.path.dirname(os.path.abspath(a.p8_cache_new)), "robots")) if a.fetch else "not_checked_cache_only"
    if robots == "blocked":
        raise SystemExit("robots.txt disallows the mirror")
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        f990 = dict(zip(oids, ex.map(lambda o: p8_lookup(o, caches, a.p8_cache_new, a.fetch), oids)))
    st_all = {s: len(v) for s, v in _group_by_fast(f990.values(), lambda x: x.get("status")).items()}
    if a.fetch_only:
        print(json.dumps({"robots": robots, "oids": len(oids), "oids_old": len(oids_old), "status": st_all}))
        return 0

    # ---- numerators: floor and central allocation
    al = cg.allocations(dec_b, split, cg.SCENARIOS[CENTRAL]["rule"])
    nums_c = {u["ein"]: cg.alloc_num(u["ein"], c2[u["ein"]]["all"], keys_w2, al) for u in new_units}
    nums_f = {u["ein"]: cw[u["ein"]]["all"] for u in new_units}
    rows = {(smp, sc): cg.scenario_rows(us, filings, f990, nn)
            for smp, us in (("old", old_units), ("new", new_units)) for sc, nn in (("floor", nums_f), ("central", nums_c))}
    wts = {smp: rbe.weights_a(rows[(smp, "floor")]) for smp in ("old", "new")}

    # reproduce the committed central row with its own seed (coverage_gap: seed + 1000 * scenario index)
    ci = list(cg.SCENARIOS).index(CENTRAL)
    floor0 = cg.scen_summaries("measured_floor", rows[("old", "floor")], wts["old"], 0, a.seed, {})
    floor_map = {(s["frame"], s["scope"], s["basis"]): s["pooled_share"] for s in floor0}
    repro = cg.scen_summaries(CENTRAL, rows[("old", "central")], wts["old"], a.boot, a.seed + 1000 * ci, floor_map)

    frames = {"committed": lambda r: r["sample_part"] == "committed", "expanded": lambda r: True}
    scopes = ([("all_ex_excluded", lambda r: True)]
              + [(f"revenue_band={b}", (lambda r, b=b: r["revenue_band"] == b)) for _, _, b in base.BANDS]
              + [(f"stratum={k}", (lambda r, k=k: r["stratum"] == k)) for k in THIN])
    jobs = [(smp, sc, fr, b, sn) for sc in ("central", "floor") for fr in frames for j, b in enumerate(BASES)
            for sn, _ in scopes for smp in ("old", "new")]
    pred = dict(scopes)

    def job(t):
        smp, sc, fr, b, sn = t
        rr = [r for r in rows[(smp, sc)] if frames[fr](r) and pred[sn](r)]
        reps = a.boot if (sn == "all_ex_excluded" or sc == "central") else 0
        return {"row_type": "estimate", "sample": smp, "scenario": CENTRAL if sc == "central" else "measured_floor",
                "frame": fr, "basis": b, "scope": sn, **estimate(rr, wts[smp], b, reps, a.seed + 7 * BASES.index(b)),
                "source": SOURCE}
    with ThreadPoolExecutor(max_workers=4) as ex:
        est = list(ex.map(job, jobs))
    key = lambda e: (e["scenario"], e["frame"], e["basis"], e["scope"])  # noqa: E731
    old_by = {key(e): e for e in est if e["sample"] == "old"}
    est = [{**e, **({"se_change": (e["se_boot"] - old_by[key(e)]["se_boot"]) if e["se_boot"] and old_by[key(e)]["se_boot"] else None,
                     "se_ratio": (e["se_boot"] / old_by[key(e)]["se_boot"]) if e["se_boot"] and old_by[key(e)]["se_boot"] else None}
                  if e["sample"] == "new" else {})} for e in est]

    comm = {smp: [r for r in rows[(smp, "central")] if r["sample_part"] == "committed"] for smp in ("old", "new")}
    comp_jobs = [(smp, b) for smp in ("old", "new") for b in BASES]
    with ThreadPoolExecutor(max_workers=4) as ex:
        comps = dict(zip(comp_jobs, ex.map(lambda t: se_components(comm[t[0]], wts[t[0]], t[1], a.boot,
                                                                    a.seed + 7 * BASES.index(t[1])), comp_jobs)))
    comp_rows = [{"row_type": "se_component", "sample": smp, "scenario": CENTRAL, "frame": "committed", "basis": b,
                  "scope": f"resampled_only={blk}", "se_boot": v, "source": SOURCE}
                 for (smp, b), d in comps.items() for blk, v in d.items()]
    strat = stratum_rows(rows[("old", "floor")], rows[("new", "floor")], wts["old"], wts["new"])
    cen_by = {r["ein"]: r for r in rows[("new", "central")]}
    added_e = {u["ein"]: u for u in added}
    rec = [{"row_type": "recipient", "sample": "new", "frame": "committed", "ein": r["ein"], "name": r["name"],
            "ntee_cd": r["ntee_cd"], "ntee_major_group": r["ntee_major_group"], "revenue_band": r["revenue_band"],
            "bmf_revenue_amt": added_e[r["ein"]]["revenue"], "stratum": r["stratum"], "stratum_N": r["stratum_N"],
            "added": added_e[r["ein"]]["added"], "years_matched": r["years_matched"], "forms": r["forms"],
            "object_ids": r["object_ids"], "num_daf_weighted_central": cen_by[r["ein"]]["num_daf_weighted_matched"],
            "num_daf_weighted_floor": r["num_daf_weighted_matched"], **{f"den_{b}": r[f"den_{b}"] for b in BASES},
            **{f"share_{b}": cen_by[r["ein"]][f"share_{b}"] for b in BASES}, "status": r["status"], "source": SOURCE}
           for r in rows[("new", "floor")] if r["ein"] in added_e]
    write_csv(a.out, est + comp_rows + strat + rec, FIELDS)

    r5 = lambda v: round(v, 5) if isinstance(v, float) else v  # noqa: E731
    head = {f"{e['sample']}|{e['scenario']}|{e['frame']}|{e['basis']}": {k: r5(e[k]) for k in (
        "sampled", "respondents", "pooled_share", "ci95_lo", "ci95_hi", "se_boot", "se_boot_fpc0", "ci95_lo_fpc0", "ci95_hi_fpc0",
        "se_change", "se_ratio") if k in e} for e in est if e["scope"] == "all_ex_excluded"}
    out = {"robots": robots,
           "frame_committed": len(frame), "frame_ge_25m": len(ge25),
           "frame_ge_25m_in_certainty": sum(1 for s in sample if s["stratum"] == "certainty" and s["band"] in CENSUS_BANDS),
           "frame_ge_25m_in_old_srs": sum(1 for s in sample if s["stratum"] != "certainty" and s["band"] in CENSUS_BANDS),
           "added_supp_a": {k: len(v) for k, v in _group_by_fast(add_a, lambda u: u["stratum"]).items()},
           "added_census_b": len(add_b), "units_old": len(old_units), "units_new": len(new_units),
           "oids_old": len(oids_old), "oids_new_total": len(oids), "oids_added": len(set(oids) - set(oids_old)),
           "f990_status": st_all,
           "added_status": {s: len(v) for s, v in _group_by_fast(rec, lambda r: f"{r['added']}|{r['status']}").items()},
           "repro_committed_central": {f"{s['frame']}|{s['basis']}": {k: r5(s[k]) for k in ("pooled_share", "pooled_ci95_lo", "pooled_ci95_hi")}
                                       for s in repro if s["scope"] == "all_ex_excluded"},
           "se_components": {f"{smp}|{b}": {k: r5(v) for k, v in d.items()} for (smp, b), d in comps.items()},
           "headline": head}
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
