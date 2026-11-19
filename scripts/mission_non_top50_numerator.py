#!/usr/bin/env python3
"""Non-top-50 DAF sponsors' grants to recipients, measured from Schedule I instead of inferred (P-B40N1202-01).

The committed study (mission_daf_share_recipient_revenue.py, P-B40N12-02) measured the DAF share of recipient
contributions with a top-50-sponsor numerator and then scaled pooled shares by 1 / 0.673 (top-50 coverage of netted
FY2024 DAF grants). This script measures the other sponsors' part of the numerator directly.

Numerator   Every DAFRC 2025 panel sponsor whose FY2023 or FY2024 return (netpayout990 cache; return choice
            mission_daf_to_daf.pick_returns) itemises Schedule I Part II (mission_net_payout.itemized and >0 lines).
            Full panel, no sponsor sampling. Lines are read with mission_recipient_sectors.load_lines (the top-50
            parser): the 94 top-50 sponsor-years from the committed cache, every other sponsor-year re-read from the
            GivingTuesday mirror of IRS TEOS into a new cache. Filer totals rows dropped
            (mission_exception_load.drop_totals_rows); DAF-to-DAF lines dropped (mission_recipient_sectors.annotate:
            whitelist `include` EINs, self-lines, unique whitelisted-name matches). DAF weight per sponsor-year: its
            daf_share_of_grants from sponsor-cost-structure.csv (capped to [0, 1]); where absent, Schedule D DAF grants /
            Part IX line 1 from the same cached return (capped); where that is absent too, 1
            (--default-weight; 0 gives the lower-bound sensitivity).
Recipients  (i)  the committed sample (2,352 EINs; frame = BMF-listed, non-excluded recipients of top-50 grants;
                 seed 20261119) with Part VIII lines from the committed q1226 cache (cross-checked against q1202);
            (ii) a supplementary stratified sample of `new-only` recipients: BMF-listed, non-excluded EINs that get
                 non-top-50 grants but no top-50 grant, so are outside the committed frame. Certainty stratum
                 (--supp-certainty largest by non-top-50 numerator) plus up to --supp-per-stratum per NTEE major
                 group x BMF revenue band, random.Random(seed + 1). Their returns are read with the q1226 parser
                 (mission_recipient_basis_eligibility.fetch_part8) into a new cache.
Variants    top50_old_frame     committed numerator on the committed frame (reproduces 6.9% / 10.3%)
            all_old_frame       all itemising panel sponsors on the committed frame
            all_expanded_frame  all itemising panel sponsors on committed frame + new-only recipients
            other_expanded      non-top-50 sponsors only, expanded frame
Bases       b1_1h (Part VIII 1h) and b3_1abcf (1h - 1d - 1e, the b40n1202-b43n26 headline). Wave 33A corrections are
            those of mission_recipient_basis_eligibility (no-1h returns out of scope; medians never scaled).
Scaling     c50 = top-50 FY2024 DAF-weighted non-D2D Schedule I / netted DAFRC FY2024 DAF grants (central);
            c_all = the same for all itemising panel sponsors. `scaled_inference` = pooled / coverage of the variant.

Pure functions; I/O only in the load/fetch helpers and `main`. Stdlib only.

Usage:
  python3 scripts/mission_non_top50_numerator.py . --np-cache NPCACHE --lines-cache-top50 RCP_LINES \
      --lines-cache NEW_LINES --bmf-dir BMF --index-dir IRSDIR --p8-cache Q1226_F990P8 --p8-cache-new NEW_P8 \
      --f990-check Q1202_F990 [--fetch] [--boot 500]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_daf_share_recipient_revenue as base  # noqa: E402
import mission_recipient_basis_eligibility as rbe  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, market, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import COST, WHITELIST, annotate, load_lines  # noqa: E402

OUT = os.path.join(DATA, "non-top50-numerator-2026-11-19.csv")
BASES = ("b1_1h", "b3_1abcf")
SOURCE = ("Numerator: IRS Form 990 Schedule I Part II lines FY2023-24 of every itemising DAFRC 2025 panel sponsor "
          "(GivingTuesday mirror of IRS TEOS XML, gt990datalake-rawdata.s3.amazonaws.com), net of DAF-to-DAF, "
          "DAF-weighted (sponsor-cost-structure.csv). Denominator: recipient Form 990 Part VIII 1a-1h / 990-EZ line 1 "
          "(same mirror; located via apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv). BMF: www.irs.gov/pub/irs-soi/eo*.csv.")


# ----------------------------------------------------------------------------- sponsor side
def sponsor_years(chosen: Mapping, panel: Mapping, rank: Mapping) -> dict:
    """(ein, fy) -> {x, tier, status_pre}: every panel sponsor-year FY2023-24 present in the cache."""
    def pre(x):
        return "not_itemised" if not itemized(x) else "no_sched_i_lines" if not (x.get("sched_i_lines") or 0) else "itemised"
    return {k: {"x": x, "tier": "top50" if k[0] in rank else "other", "pre": pre(x)}
            for k, x in chosen.items() if k[0] in panel and k[1] in FYS}


def weight_fallback(cost_w: Mapping, sy: Mapping, default: float = 1.0) -> tuple[dict, dict]:
    """-> (weights, source per key). cost-structure share; else Sched D DAF grants / Part IX line 1; else `default`."""
    def one(k, x):
        if k in cost_w:
            return cost_w[k], "cost_structure"
        g, p = x.get("sched_d_daf_grants"), x.get("part_ix_line1_grants_domestic_orgs")
        if g is not None and p:
            return min(1.0, max(0.0, g / p)), "sched_d_over_part_ix_l1"
        return default, "default_1"
    pairs = {k: one(k, v["x"]) for k, v in sy.items()}
    return {k: v[0] for k, v in pairs.items()}, {k: v[1] for k, v in pairs.items()}


def combine(n50: Mapping, noth: Mapping) -> dict:
    """recipient -> {top50: {fy: {si, dw}}, other: {...}, all: {...}, g50, goth}."""
    def add(a, b):
        return {fy: {"si": a.get(fy, {}).get("si", 0.0) + b.get(fy, {}).get("si", 0.0),
                     "dw": a.get(fy, {}).get("dw", 0.0) + b.get(fy, {}).get("dw", 0.0)} for fy in set(a) | set(b)}
    empty = {"fy": {}, "grantors": set()}
    return {e: {"top50": n50.get(e, empty)["fy"], "other": noth.get(e, empty)["fy"],
                "all": add(n50.get(e, empty)["fy"], noth.get(e, empty)["fy"]),
                "g50": len(n50.get(e, empty)["grantors"]), "goth": len(noth.get(e, empty)["grantors"])}
            for e in set(n50) | set(noth)}


def tot(fy_map: Mapping, k: str = "dw") -> float:
    return sum(v[k] for v in fy_map.values())


# ----------------------------------------------------------------------------- disposition of numerator dollars
def disposition(comb: Mapping, bmf: Mapping, panel_eins: frozenset, blank: Mapping) -> list:
    """Where top-50 and non-top-50 DAF-weighted FY2023-24 dollars land (full universe, no sampling)."""
    def cat(e, c):
        if e not in bmf:
            return "not_in_bmf"
        ex = base.exclusion(bmf[e], panel_eins)
        if ex:
            return f"excluded_{ex}"
        return "frame_committed" if tot(c["top50"], "si") > 0 else "frame_new_only"
    rows = tuple((cat(e, c), tot(c["top50"]), tot(c["other"]), e) for e, c in comb.items())
    rows = rows + tuple(("blank_ein", v["top50"], v["other"], k) for k, v in blank.items())
    t50, toth = sum(r[1] for r in rows), sum(r[2] for r in rows)
    by = _group_by_fast(rows, lambda r: r[0])
    order = ("frame_committed", "frame_new_only", "excluded_university", "excluded_hospital", "excluded_foundation",
             "excluded_daf_sponsor", "excluded_not_501c3", "not_in_bmf", "blank_ein")
    return [{"row_type": "disposition", "category": c,
             "recipients_top50": sum(1 for r in by.get(c, ()) if r[1] > 0),
             "recipients_other": sum(1 for r in by.get(c, ()) if r[2] > 0),
             "usd_top50_daf_weighted": round(sum(r[1] for r in by.get(c, ()))),
             "usd_other_daf_weighted": round(sum(r[2] for r in by.get(c, ()))),
             "share_of_top50_usd": sum(r[1] for r in by.get(c, ())) / t50 if t50 else None,
             "share_of_other_usd": sum(r[2] for r in by.get(c, ())) / toth if toth else None,
             "source": SOURCE} for c in order]


def blank_ein_lines(ann: Mapping, weights: Mapping, tiers: Mapping) -> dict:
    """normalised name -> {top50, other} DAF-weighted $, blank-EIN non-D2D positive lines."""
    flat = tuple(("N:" + norm_name(r["name"]), tiers[k], r["amount"] * weights.get(k, 1.0))
                 for k, rs in ann.items() for r in rs if not r["ein"] and not r["d2d"] and r["amount"] > 0)
    by = _group_by_fast(flat, lambda t: t[0])
    return {k: {"top50": sum(t[2] for t in v if t[1] == "top50"), "other": sum(t[2] for t in v if t[1] == "other")}
            for k, v in by.items()}


# ----------------------------------------------------------------------------- recipients
def sample_row(s: Mapping, filings: Mapping, f990: Mapping, c: Mapping, part: str) -> dict:
    """One recipient with three numerators on the same matched years (rbe.recipient_a does the year matching)."""
    r = {v: rbe.recipient_a({**s, "num": c[v]}, filings, f990) for v in ("top50", "other", "all")}
    a = r["all"]
    return {"row_type": "recipient", "sample_part": part, "ein": s["ein"], "name": s["name"], "ntee_cd": s["ntee"],
            "ntee_major_group": s["group"], "revenue_band": s["band"], "stratum": s["stratum"], "stratum_N": s["N_h"],
            "top50_grantors": c["g50"], "other_grantors": c["goth"],
            "num_top50_dw_fy2023_2024_all": round(tot(c["top50"])), "num_other_dw_fy2023_2024_all": round(tot(c["other"])),
            "years_matched": a["years_matched"], "forms": a["forms"], "object_ids": a["object_ids"],
            "num_top50_dw_matched": r["top50"]["num_daf_weighted_matched"],
            "num_other_dw_matched": r["other"]["num_daf_weighted_matched"],
            "num_all_dw_matched": a["num_daf_weighted_matched"],
            "den_b1_1h": a["den_b1_1h"], "den_b3_1abcf": a["den_b3_1abcf"],
            **{f"share_{v}_{b}": r[v][f"share_{b}"] for v in ("top50", "other", "all") for b in BASES},
            "leaked_sponsor_name": a["leaked_sponsor_name"], "status": a["status"], "source": SOURCE}


def as_variant(rows: Sequence[Mapping], v: str) -> tuple[dict, ...]:
    """Rows shaped for rbe statistics: num_daf_weighted_matched / den_* / share_* of numerator v."""
    return tuple({**r, "num_daf_weighted_matched": r[f"num_{v}_dw_matched"],
                  **{f"share_{b}": r[f"share_{v}_{b}"] for b in BASES}} for r in rows)


VARIANTS = (("top50_old_frame", "top50", "committed"), ("all_old_frame", "all", "committed"),
            ("all_expanded_frame", "all", "expanded"), ("other_expanded_frame", "other", "expanded"),
            ("all_new_only", "all", "new_only"))


def summaries(rows: Sequence[Mapping], scales: Mapping, reps: int, seed: int) -> list:
    w = rbe.weights_a(rows)
    scopes = ([("all", "all_ex_excluded", lambda r: True, reps),
               ("sensitivity", "ex_leaked_daf_sponsors", lambda r: not r["leaked_sponsor_name"], reps),
               ("sensitivity", "non_certainty_only", lambda r: not r["stratum"].endswith("certainty"), reps)]
              + [("revenue_band", b, (lambda r, b=b: r["revenue_band"] == b), reps) for _, _, b in base.BANDS]
              + [("ntee_major_group", g, (lambda r, g=g: r["ntee_major_group"] == g), 0) for g in base.GROUPS])
    frames = {"committed": lambda r: r["sample_part"] == "committed", "new_only": lambda r: r["sample_part"] == "new_only",
              "expanded": lambda r: True}

    def one(i, j, k, vname, v, fr, st, sc, pred, n):
        sub = as_variant([r for r in rows if frames[fr](r) and pred(r)], v)
        b = BASES[j]
        s = rbe.summary_a(st, sc, b, sub, w, scales[v], n, seed + 97 * i + 31 * k + j)
        return {**{x: y for x, y in s.items() if x != "source"}, "variant": vname, "numerator": v, "frame": fr,
                "basis": b, "coverage_used": scales[v], "source": SOURCE}
    return [one(i, j, k, vn, v, fr, *sc)
            for k, (vn, v, fr) in enumerate(VARIANTS) for i, sc in enumerate(scopes) for j in range(len(BASES))]


# ----------------------------------------------------------------------------- I/O helpers
def p8_lookup(oid: str, old_cache: str, new_cache: str, fetch: bool) -> dict:
    hit = rbe.fetch_part8(oid, old_cache, False)
    return hit if hit.get("status") != "not_fetched" else rbe.fetch_part8(oid, new_cache, fetch)


def check_q1202(oids: Sequence[str], f990: Mapping, cache: str) -> dict:
    old = {o: base.fetch_main(o, cache, False) for o in oids}
    both = tuple(o for o in oids if old[o].get("status") == "ok" and f990.get(o, {}).get("status") == "ok"
                 and old[o].get("form") == "IRS990")
    diff = tuple(o for o in both if abs((old[o].get("contrib_1h") or 0) - (f990[o].get("l1h") or 0)) > 1)
    return {"oids_compared_990": len(both), "l1h_mismatch": len(diff), "not_in_q1202": sum(1 for o in oids if old[o]["status"] == "not_fetched")}


FIELDS = ("row_type", "variant", "numerator", "frame", "basis", "scope_type", "scope", "sampled", "respondents",
          "weighted_recipients", "p25_share", "median_share", "median_ci95_lo", "median_ci95_hi", "p75_share",
          "pooled_share", "pooled_ci95_lo", "pooled_ci95_hi", "share_ge_20pct", "share_gt_100pct", "coverage_used",
          "scaled_pooled_inference", "den_nonpos_respondents", "den_nonpos_num_share",
          "category", "recipients_top50", "recipients_other", "usd_top50_daf_weighted", "usd_other_daf_weighted",
          "share_of_top50_usd", "share_of_other_usd",
          "item", "fiscal_year", "value",
          "sample_part", "ein", "name", "ntee_cd", "ntee_major_group", "revenue_band", "stratum", "stratum_N",
          "top50_grantors", "other_grantors", "num_top50_dw_fy2023_2024_all", "num_other_dw_fy2023_2024_all",
          "years_matched", "forms", "object_ids", "num_top50_dw_matched", "num_other_dw_matched", "num_all_dw_matched",
          "den_b1_1h", "den_b3_1abcf", *(f"share_{v}_{b}" for v in ("top50", "other", "all") for b in BASES),
          "leaked_sponsor_name", "status", "source")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; repo CLI convention)")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache-top50", required=True, help="committed top-50 line cache (read only)")
    ap.add_argument("--lines-cache", required=True, help="line cache for non-top-50 sponsor-years")
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True)
    ap.add_argument("--p8-cache", required=True, help="committed q1226 Part VIII cache (read only)")
    ap.add_argument("--p8-cache-new", required=True, help="Part VIII cache for supplementary-sample returns")
    ap.add_argument("--f990-check", default="", help="committed q1202 f990 cache, for a 1h cross-check")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--seed", type=int, default=20261119)
    ap.add_argument("--per-stratum", type=int, default=40)
    ap.add_argument("--certainty", type=int, default=400)
    ap.add_argument("--supp-per-stratum", type=int, default=30)
    ap.add_argument("--supp-certainty", type=int, default=100)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--default-weight", type=float, default=1.0,
                    help="DAF weight for sponsor-years with no DAF share anywhere (sensitivity: 0)")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    sy = sponsor_years(pick_returns(load_np(a.np_cache)), panel, rank)
    item = {k: v for k, v in sy.items() if v["pre"] == "itemised"}

    def lines(k):
        v = item[k]
        cache, fetch = (a.lines_cache_top50, False) if v["tier"] == "top50" else (a.lines_cache, a.fetch)
        return load_lines(v["x"]["oid"], v["x"]["sched_i_lines"], cache, [], fetch)
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
    weights, wsrc = weight_fallback(base.sponsor_weights(read_csv(COST), good), {k: item[k] for k in good}, a.default_weight)
    ann50 = {k: v for k, v in ann.items() if tiers[k] == "top50"}
    annoth = {k: v for k, v in ann.items() if tiers[k] == "other"}
    comb = combine(base.numerators(ann50, weights), base.numerators(annoth, weights))

    # coverage
    net = {int(r["fiscal_year"]): num(r["netted_value"]) for r in read_csv(base.NETTED_CSV)
           if r["metric"] == "daf_grants" and r["tier"] == "central"}
    mk = market(dafrc)
    cov = {(t, fy): base.coverage_fy(an, weights, fy) for t, an in (("top50", ann50), ("other", annoth), ("all", ann))
           for fy in FYS}
    c50 = cov[("top50", 2024)]["daf_weighted_non_d2d"] / net[2024]
    call = cov[("all", 2024)]["daf_weighted_non_d2d"] / net[2024]
    scales = {"top50": c50, "all": call, "other": cov[("other", 2024)]["daf_weighted_non_d2d"] / net[2024]}

    # frames and samples
    panel_eins = frozenset(panel)
    bmf = base.load_bmf(a.bmf_dir, frozenset(comb))

    def unit(e, c):
        b = bmf[e]
        return {**b, "group": base.group_of(b["ntee"]), "band": base.band_of(b["revenue"]), "num": c["top50"],
                "num_si_total": tot(c["top50"], "si"), "num_oth_si": tot(c["other"], "si"), "excl": base.exclusion(b, panel_eins)}
    universe = tuple(unit(e, c) for e, c in comb.items() if e in bmf)
    frame = tuple(u for u in universe if not u["excl"] and u["num_si_total"] > 0)
    new_only = tuple({**u, "num_si_total": u["num_oth_si"]} for u in universe if not u["excl"] and u["num_si_total"] <= 0
                     and u["num_oth_si"] > 0)
    sample = base.draw_sample(frame, a.certainty, a.per_stratum, a.seed)
    supp = tuple({**s, "stratum": "new|" + s["stratum"]}
                 for s in base.draw_sample(new_only, a.supp_certainty, a.supp_per_stratum, a.seed + 1))

    every = sample + supp
    idx = base.load_index(a.index_dir, frozenset(s["ein"] for s in every))
    filings = {s["ein"]: base.choose_filings(idx.get(s["ein"], ())) for s in every}
    oids = sorted({f["oid"] for fs in filings.values() for f in fs.values()})
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        f990 = dict(zip(oids, ex.map(lambda o: p8_lookup(o, a.p8_cache, a.p8_cache_new, a.fetch), oids)))
    rec = ([sample_row(s, filings[s["ein"]], f990, comb[s["ein"]], "committed") for s in sample]
           + [sample_row(s, filings[s["ein"]], f990, comb[s["ein"]], "new_only") for s in supp])

    blank = blank_ein_lines(ann, weights, tiers)
    disp = disposition(comb, bmf, panel_eins, blank)
    summ = summaries(rec, scales, a.boot, a.seed)

    item_rows = (
        [{"row_type": "coverage", "item": f"{t}_{m}", "fiscal_year": fy, "value": round(cov[(t, fy)][m])}
         for t in ("top50", "other", "all") for fy in FYS for m in ("sched_i_non_d2d", "daf_weighted_non_d2d", "d2d_dropped")]
        + [{"row_type": "coverage", "item": f"{t}_share_of_netted_daf_weighted", "fiscal_year": fy,
            "value": cov[(t, fy)]["daf_weighted_non_d2d"] / net[fy]} for t in ("top50", "other", "all") for fy in FYS]
        + [{"row_type": "coverage", "item": "netted_dafrc_daf_grants_central", "fiscal_year": fy, "value": round(net[fy])} for fy in FYS]
        + [{"row_type": "coverage", "item": "dafrc_raw_daf_grants", "fiscal_year": fy, "value": round(mk[fy]["grants"])} for fy in FYS])
    item_rows = [{**r, "source": SOURCE} for r in item_rows]
    write_csv(a.out, summ + disp + item_rows
              + sorted(rec, key=lambda r: (r["sample_part"], not r["stratum"].endswith("certainty"), r["stratum"], r["ein"])),
              FIELDS)

    # diagnostics
    sy_status = {f"{t}:{k}": len(v) for (t, k), v in sorted(_group_by_fast(
        sy.items(), lambda kv: (kv[1]["tier"], kv[1]["pre"] if kv[1]["pre"] != "itemised"
                                else "lines_" + loaded[kv[0]]["status"].split(":")[0])).items())}
    dafrc24 = {ein9(r["ein"]): num(r.get("total_daf_grants")) or 0.0 for r in dafrc if r["fiscal_year_end"] == "2024"}
    with_lines24 = frozenset(k[0] for k in good if k[1] == 2024)
    pick = lambda vn, b, sc="all_ex_excluded": next(s for s in summ if s["variant"] == vn and s["basis"] == b and s["scope"] == sc)  # noqa: E731
    rnd = lambda d: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items() if k not in ("source",)}  # noqa: E731
    w = rbe.weights_a(rec)
    ok_c = tuple(r for r in rec if r["status"] == "ok" and r["sample_part"] == "committed")
    uplift = (sum(w[r["stratum"]] * r["num_other_dw_matched"] for r in ok_c)
              / sum(w[r["stratum"]] * r["num_top50_dw_matched"] for r in ok_c))
    out = {
        "panel_eins": len(panel), "panel_sponsor_years_fy2023_2024_in_cache": len(sy), "sponsor_year_status": sy_status,
        "sponsors_with_lines": {"top50": len({k[0] for k in good if tiers[k] == "top50"}),
                                "other": len({k[0] for k in good if tiers[k] == "other"})},
        "lines_loaded": {t: sum(len(good[k]["lines"]) for k in good if tiers[k] == t) for t in ("top50", "other")},
        "weight_source": {s: {"sponsor_years": len(v), "usd_sched_i_non_d2d": round(sum(
            r["amount"] for k in v for r in ann[k] if not r["d2d"]))} for s, v in _group_by_fast(wsrc, lambda k: wsrc[k]).items()},
        "dafrc_fy2024_grants_by_line_status": {
            "with_itemised_lines": round(sum(v for e, v in dafrc24.items() if e in with_lines24)),
            "without": round(sum(v for e, v in dafrc24.items() if e not in with_lines24)),
            "largest_without": sorted(((panel[e]["name"][:40], round(v)) for e, v in dafrc24.items()
                                       if e not in with_lines24 and e in panel), key=lambda t: -t[1])[:12]},
        "coverage": {f"{t}_{fy}": cov[(t, fy)]["daf_weighted_non_d2d"] / net[fy] for t in ("top50", "other", "all") for fy in FYS},
        "recipient_eins": {"all": len(comb), "top50": sum(1 for c in comb.values() if c["top50"]),
                           "other": sum(1 for c in comb.values() if c["other"])},
        "frame_committed": len(frame), "frame_new_only": len(new_only),
        "frame_new_only_num_other_si": round(sum(u["num_si_total"] for u in new_only)),
        "sample": len(sample), "supp": len(supp), "supp_strata": len({s["stratum"] for s in supp}), "oids": len(oids),
        "f990_status": {k: len(v) for k, v in _group_by_fast(f990.values(), lambda x: x["status"]).items()},
        "recipient_status": {f"{p}:{k}": len(v) for (p, k), v in _group_by_fast(rec, lambda r: (r["sample_part"], r["status"])).items()},
        "q1202_check": check_q1202([o for s in sample for o in (f["oid"] for f in filings[s["ein"]].values())], f990, a.f990_check)
        if a.f990_check else None,
        "uplift_other_over_top50_committed_frame_weighted": uplift,
        "implied_uplift_from_scaling": 1 / c50 - 1,
        "disposition": [rnd(d) for d in disp],
        "headline": {f"{vn}|{b}": rnd({k: pick(vn, b).get(k) for k in ("respondents", "weighted_recipients", "median_share",
                     "median_ci95_lo", "median_ci95_hi", "pooled_share", "pooled_ci95_lo", "pooled_ci95_hi",
                     "scaled_pooled_inference", "coverage_used")}) for vn, _, _ in VARIANTS for b in BASES},
        "bands": {f"{vn}|{b}|{sc}": round(pick(vn, b, sc)["pooled_share"] or 0, 4) for vn in ("top50_old_frame", "all_old_frame", "all_expanded_frame", "all_new_only")
                  for b in BASES for _, _, sc in base.BANDS},
        "band_medians": {f"{vn}|{b}|{sc}": round(pick(vn, b, sc)["median_share"] or 0, 4) for vn in ("top50_old_frame", "all_expanded_frame")
                         for b in BASES for _, _, sc in base.BANDS},
        "sensitivities": {f"{vn}|{b}|{sc}": round(pick(vn, b, sc)["pooled_share"] or 0, 4) for vn in ("top50_old_frame", "all_expanded_frame")
                          for b in BASES for sc in ("ex_leaked_daf_sponsors", "non_certainty_only")},
        "largest_other_recipients_in_sample": sorted(({"name": r["name"][:40], "part": r["sample_part"], "other": r["num_other_dw_matched"],
                                                        "top50": r["num_top50_dw_matched"], "den": r["den_b1_1h"]}
                                                       for r in rec if r["status"] == "ok"), key=lambda d: -d["other"])[:12],
    }
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
