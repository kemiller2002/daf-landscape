#!/usr/bin/env python3
"""Recipient-sector join for every itemising DAFRC panel sponsor, FY2023-FY2024, with Schedule F foreign grants as a
sector bucket, sub-$5,000 grants allocated, and a reconciliation against sponsors' own sector splits (P-B39N4-01).

Builds on scripts/mission_recipient_sectors.py (top-50 join, P-NEW-RCP-01) and imports it; modifies nothing.

Universe   Every DAFRC 2025 panel sponsor-year FY2023-24 whose chosen return (mission_daf_to_daf.pick_returns on the
           netpayout990 cache) itemises Schedule I Part II, exactly as mission_non_top50_numerator.sponsor_years /
           mission_coverage_gap: top-50 lines from the committed rcp/lines cache, all other lines from q120201/lines
           (caches only; nothing is fetched). Filer totals rows dropped (mission_exception_load.drop_totals_rows).
Join       mission_recipient_sectors.load_bmf + annotate: DAF-to-DAF flag (whitelist `include`, self-lines, unique
           whitelisted-name matches) and NTEE major group with the BMF FOUNDATION-code and name-rule fallbacks.
           Public-society benefit is split internally into NTEE T (philanthropy, federated giving, grantmakers) and
           the rest, so the treatments below can move T.
Foreign    Form 990 Part IX line 3 (grants to foreign organisations, governments and individuals; itemised on
           Schedule F) per sponsor-year from coverage-gap-decomposition-2026-11-20.csv (row_type sponsor_itemised,
           column l3), added as sector `foreign_schedule_f`. Top-50 values are cross-checked against
           daf-foreign-grants-schedule-f-2023-2024.csv (row_type sponsor_year, part_ix_l3_foreign_usd).
Sub-$5k    As in b40n120201-01 and its wave-41B corrections: per sponsor-year, L1 - Schedule I total (all lines, incl.
           DAF-to-DAF) is non-itemised domestic grants. Sponsor-years itemising >= 50% of L1 ("full itemisers") are
           allocated across sectors by the sector mix of their scope's positive non-DAF-to-DAF lines under $10,000
           (`small10` key); sponsor-years itemising < 50% ("partial itemisers") by the mix of all positive
           non-DAF-to-DAF lines (`all` key). Negative differences are kept in the net. Allocation is per FY.
           Layer `sched_i` leaves the component out (the low end of the wave-41B assumption envelope).
Weights    basis `schedule_i` (filed dollars) and `daf_weighted` (each sponsor-year x w2 = min(1, corrected DAFRC
           DAF grants / (L1 + L3)), the decomposition-B weight in the coverage-gap CSV).
Treatments t_a_base           DAF-to-DAF excluded; NTEE T inside public-society benefit (P-NEW-RCP-01 convention)
           t_b_d2d_included   DAF-to-DAF lines kept, classified by the receiving sponsor's own NTEE code
           t_c_t_separate     DAF-to-DAF excluded; NTEE T reported as its own bucket `philanthropy_t`
           t_d_t_excluded     DAF-to-DAF and NTEE T both excluded (both treated as pass-through)
Layers     sched_i | plus_foreign | plus_foreign_sub5k
Reconcile  Published sector splits (Fidelity Charitable 2025 and 2026 Giving Reports: grant dollars and volumes;
           Vanguard Charitable 2024/2025 annual reports: grant counts by cause) are compared with the sponsor's own
           FY2024 lines under each treatment and layer (the constants below are quoted from those sources).

Stdlib only; pure functions, I/O in the load helpers and main.

Usage:
  python3 scripts/mission_sector_join_all.py . --np-cache NPCACHE --lines-cache-top50 RCP_LINES \
      --lines-cache Q120201_LINES --bmf-dir BMF [--out CSV]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_recipient_sectors as rs  # noqa: E402
import mission_non_top50_numerator as n50  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_net_payout import norm_name, panel_from  # noqa: E402

OUT = os.path.join(DATA, "sector-join-all-sponsors-2026-11-20.csv")
GAP_CSV = os.path.join(DATA, "coverage-gap-decomposition-2026-11-20.csv")
FGN_CSV = os.path.join(DATA, "daf-foreign-grants-schedule-f-2023-2024.csv")
PARTIAL = 0.5
SMALL = 10000.0
FIDELITY, VANGUARD, SCHWAB, NPT = "110303001", "232888152", "311640316", "237825575"
SOURCE = ("IRS Form 990 Schedule I Part II lines (GivingTuesday mirror of IRS TEOS e-file XML; caches rcp/lines and "
          "q120201/lines) of every itemising DAFRC 2025 panel sponsor-year FY2023-24, joined to IRS EO BMF NTEE_CD via "
          "mission_recipient_sectors.py; Part IX lines 1 and 3 and w2 from coverage-gap-decomposition-2026-11-20.csv")

# extended group space: public_societal_benefit is split into NTEE T and the rest
EXT = ("education", "religion", "human_services", "health", "arts_culture", "international", "environment_animals",
       "psb_other", "psb_t", "mutual_membership", "unknown_z", "unclassified")
TREATMENTS = ("t_a_base", "t_b_d2d_included", "t_c_t_separate", "t_d_t_excluded")
LAYERS = ("sched_i", "plus_foreign", "plus_foreign_sub5k")
OUT_GROUPS = ("education", "religion", "human_services", "health", "arts_culture", "international",
              "environment_animals", "public_societal_benefit", "philanthropy_t", "mutual_membership", "unknown_z",
              "unclassified", "foreign_schedule_f")

# Published splits, quoted (shares of grant dollars / volumes). Fidelity labels -> output groups.
FID_MAP = {"Religion": ("religion",), "Human services": ("human_services",), "Education": ("education",),
           "Health": ("health",), "International affairs": ("international", "foreign_schedule_f"),
           "Society benefit": ("public_societal_benefit", "philanthropy_t"),
           "Environment and animals": ("environment_animals",), "Arts and culture": ("arts_culture",),
           "Other": ("mutual_membership", "unknown_z", "unclassified")}
PUBLISHED = (
    # sponsor, source id, period, metric, {label: share}
    (FIDELITY, "fidelity_2025_giving_report_p20_appendix", "CY2024", "dollars",
     {"Religion": .13, "Human services": .13, "Education": .23, "Health": .08, "International affairs": .05,
      "Society benefit": .25, "Environment and animals": .05, "Arts and culture": .06, "Other": .02}),
    (FIDELITY, "fidelity_2025_giving_report_p20_appendix", "CY2024", "volume",
     {"Religion": .27, "Human services": .20, "Education": .12, "Health": .09, "International affairs": .08,
      "Society benefit": .08, "Environment and animals": .08, "Arts and culture": .06, "Other": .02}),
    (FIDELITY, "fidelity_2026_giving_report_p9", "CY2025 (outliers $727m removed)", "dollars",
     {"Religion": .131, "Human services": .122, "Education": .248, "Health": .075, "International affairs": .055,
      "Society benefit": .234, "Environment and animals": .052, "Arts and culture": .059, "Other": .025}),
    (FIDELITY, "fidelity_2026_giving_report_p9", "CY2025", "volume",
     {"Religion": .27, "Human services": .202, "Education": .111, "Health": .086, "International affairs": .082,
      "Society benefit": .084, "Environment and animals": .073, "Arts and culture": .068, "Other": .024}),
    (VANGUARD, "vanguard_charitable_2024_annual_report", "CY2024", "volume",
     {"Human services": 68000 / 240064, "Religion": 52000 / 240064, "Education": 36000 / 240064,
      "Health": 30000 / 240064, "Environment and animals": 19000 / 240064}),
    (VANGUARD, "vanguard_charitable_2025_annual_report", "CY2025", "volume",
     {"Human services": 72000 / 267838, "Religion": 54000 / 267838, "Education": 38000 / 267838,
      "Health": 33000 / 267838, "Environment and animals": 20000 / 267838}),
)


# ----------------------------------------------------------------------------- per sponsor-year aggregates
def ext_group(r: Mapping) -> str:
    if r["group"] == "public_societal_benefit":
        return "psb_t" if r["ntee"][:1] == "T" else "psb_other"
    return r["group"]


def zero() -> dict:
    return {g: 0.0 for g in EXT}


def vadd(a: Mapping, b: Mapping, k: float = 1.0) -> dict:
    return {g: a.get(g, 0.0) + k * b.get(g, 0.0) for g in set(a) | set(b)}


def sy_aggregate(lines: Sequence[Mapping], gap: Mapping) -> dict:
    """One sponsor-year -> vectors over EXT plus Part IX figures (unweighted)."""
    def acc(pred, val=lambda r: r["amount"]):
        return reduce(lambda a, r: _acc(a, ext_group(r), val(r)), (r for r in lines if pred(r)), zero())
    net = acc(lambda r: not r["d2d"])
    d2d = acc(lambda r: r["d2d"])
    si_total = sum(net.values()) + sum(d2d.values())
    l1, l3 = gap.get("l1", 0.0), gap.get("l3", 0.0)
    return {"net": net, "d2d": d2d, "pos": acc(lambda r: not r["d2d"] and r["amount"] > 0),
            "small": acc(lambda r: not r["d2d"] and 0 < r["amount"] < SMALL),
            "n_net": acc(lambda r: not r["d2d"], lambda r: 1.0), "n_d2d": acc(lambda r: r["d2d"], lambda r: 1.0),
            "l1": l1, "l3": l3, "w2": gap.get("w2", 1.0), "si_total": si_total, "nonitem": l1 - si_total,
            "partial": l1 > 0 and si_total < PARTIAL * l1, "gap_found": bool(gap)}


def scaled(a: Mapping, w: float) -> dict:
    vec = ("net", "d2d", "pos", "small", "n_net", "n_d2d")
    return {**a, **{k: {g: v * (w if not k.startswith("n_") else 1.0) for g, v in a[k].items()} for k in vec},
            "l1": a["l1"] * w, "l3": a["l3"] * w, "si_total": a["si_total"] * w, "nonitem": a["nonitem"] * w}


def norm(v: Mapping) -> dict:
    s = sum(v.values())
    return {g: x / s for g, x in v.items()} if s else {g: 0.0 for g in v}


def scope_fy(aggs: Sequence[Mapping]) -> dict:
    """Pool sponsor-year aggregates of one FY; allocate the sub-$5k component within the pool."""
    pool = lambda k: reduce(vadd, (a[k] for a in aggs), zero())  # noqa: E731
    full = sum(a["nonitem"] for a in aggs if not a["partial"])
    part = sum(a["nonitem"] for a in aggs if a["partial"])
    small, pos = pool("small"), pool("pos")
    sub5k = vadd({g: full * x for g, x in norm(small if sum(small.values()) else pos).items()},
                 {g: part * x for g, x in norm(pos).items()})
    return {"net": pool("net"), "d2d": pool("d2d"), "n_net": pool("n_net"), "n_d2d": pool("n_d2d"), "sub5k": sub5k,
            "l3": sum(a["l3"] for a in aggs), "l1": sum(a["l1"] for a in aggs),
            "si_total": sum(a["si_total"] for a in aggs), "sub5k_full": full, "sub5k_partial": part,
            "sponsor_years": len(aggs), "eins": frozenset(a["ein"] for a in aggs), "sponsors": len({a["ein"] for a in aggs})}


def combine_fy(parts: Sequence[Mapping]) -> dict:
    vec = ("net", "d2d", "n_net", "n_d2d", "sub5k")
    sca = ("l3", "l1", "si_total", "sub5k_full", "sub5k_partial", "sponsor_years")
    return {**{k: reduce(vadd, (p[k] for p in parts), zero()) for k in vec},
            **{k: sum(p[k] for p in parts) for k in sca}, "eins": frozenset().union(*(p["eins"] for p in parts)),
            "sponsors": len(frozenset().union(*(p["eins"] for p in parts)))}


# ----------------------------------------------------------------------------- treatments and layers
def collapse(v: Mapping, treatment: str) -> dict:
    """EXT vector -> OUT_GROUPS vector under a T treatment (DAF-to-DAF handled by the caller)."""
    base = {g: v.get(g, 0.0) for g in EXT if g not in ("psb_other", "psb_t")}
    if treatment == "t_c_t_separate":
        return {**base, "public_societal_benefit": v.get("psb_other", 0.0), "philanthropy_t": v.get("psb_t", 0.0)}
    if treatment == "t_d_t_excluded":
        return {**base, "public_societal_benefit": v.get("psb_other", 0.0)}
    return {**base, "public_societal_benefit": v.get("psb_other", 0.0) + v.get("psb_t", 0.0)}


def vector(p: Mapping, treatment: str, layer: str) -> dict:
    sched = vadd(p["net"], p["d2d"]) if treatment == "t_b_d2d_included" else p["net"]
    v = sched if layer != "plus_foreign_sub5k" else vadd(sched, p["sub5k"])
    out = collapse(v, treatment)
    return {**out, "foreign_schedule_f": p["l3"]} if layer != "sched_i" else out


def counts(p: Mapping, treatment: str) -> dict:
    return collapse(vadd(p["n_net"], p["n_d2d"]) if treatment == "t_b_d2d_included" else p["n_net"], treatment)


def share_rows(meta: Mapping, p: Mapping, basis: str, treatments: Sequence[str], conc: Mapping | None) -> list:
    out = []
    for t in treatments:
        cnt = counts(p, t)
        for layer in LAYERS:
            v = vector(p, t, layer)
            tot = sum(v.values())
            head = {**meta, "row_type": "share", "basis": basis, "treatment": t, "layer": layer}
            all_row = {**head, "sector": "ALL", "amount_usd": round(tot), "share": 1.0 if tot else None,
                       "lines": int(sum(cnt.values())), "sponsor_years": p["sponsor_years"], "sponsors": p["sponsors"],
                       "sched_i_total_usd": round(p["si_total"]), "d2d_usd": round(sum(p["d2d"].values())),
                       "ntee_t_non_d2d_usd": round(p["net"]["psb_t"]), "part_ix_l1_usd": round(p["l1"]),
                       "foreign_l3_usd": round(p["l3"]), "sub5k_full_usd": round(p["sub5k_full"]),
                       "sub5k_partial_usd": round(p["sub5k_partial"]),
                       **({k: conc[k] for k in ("recipients", "top10_share", "top100_share", "hhi")}
                          if conc and t == "t_a_base" and layer == "sched_i" else {})}
            out.append(all_row)
            out.extend({**{k: x for k, x in head.items() if k != "source"}, "sector": g, "amount_usd": round(v[g]),
                        "share": v[g] / tot if tot else None,
                        "lines": int(cnt.get(g, 0)) if g != "foreign_schedule_f" else ""}
                       for g in OUT_GROUPS if g in v)
    return out


def concentration(lines_by_sy: Mapping, keys: Sequence) -> dict:
    by = reduce(lambda a, r: _acc(a, r["key"], r["amount"]),
                (r for k in keys for r in lines_by_sy[k] if not r["d2d"]), {})
    vals = sorted((v for v in by.values() if v > 0), reverse=True)
    tot = sum(vals)
    return {"recipients": len(vals), "top10_share": sum(vals[:10]) / tot if tot else None,
            "top100_share": sum(vals[:100]) / tot if tot else None,
            "hhi": round(sum((v / tot * 100) ** 2 for v in vals), 1) if tot else None}


def _acc(a: dict, key: str, v: float) -> dict:
    # accumulator-local mutation inside a reduce step (O(n)); callers only see the finished mapping
    a[key] = a.get(key, 0.0) + v
    return a


# ----------------------------------------------------------------------------- reconciliation
def published_vec(v: Mapping) -> dict:
    """OUT_GROUPS vector -> Fidelity labels."""
    return {lab: sum(v.get(g, 0.0) for g in gs) for lab, gs in FID_MAP.items()}


def recon_rows(sy_parts: Mapping) -> list:
    """Compare each published split with the sponsor's FY2024 (and FY2023-24) lines, all treatments and layers."""
    out = []
    for sp, src, period, metric, pub in PUBLISHED:
        for fy_label, p in sy_parts.get(sp, {}).items():
            for t in TREATMENTS:
                if t == "t_c_t_separate":
                    continue  # no published bucket for T on its own; identical to t_a once mapped
                for layer in (LAYERS if metric == "dollars" else ("sched_i",)):
                    v = published_vec(vector(p, t, layer) if metric == "dollars" else counts(p, t))
                    tot = sum(v.values())  # Vanguard's five counts are over all grants issued, so shares share a base
                    comp = {lab: (v[lab] / tot if tot else None) for lab in v}
                    diffs = {lab: comp[lab] - pub[lab] for lab in pub if comp.get(lab) is not None}
                    l1 = sum(abs(d) for d in diffs.values())
                    head = {"row_type": "reconciliation", "scope": sp, "scope_type": "sponsor", "fiscal_year": fy_label,
                            "basis": "schedule_i", "treatment": t, "layer": layer, "published_source": src,
                            "published_period": period, "metric": metric}
                    out.append({**head, "sector": "SUM_ABS_DIFF", "share": round(l1, 4),
                                "max_abs_diff": round(max(abs(d) for d in diffs.values()), 4)})
                    out.extend({**head, "sector": lab, "published_share": round(pub[lab], 4),
                                "share": round(comp[lab], 4), "diff": round(diffs[lab], 4)} for lab in pub)
    return out


# ----------------------------------------------------------------------------- main
FIELDS = ("row_type", "scope", "scope_type", "tier_filter", "segment", "fiscal_year", "basis", "treatment", "layer",
          "sector", "amount_usd", "share", "lines", "sponsor_years", "sponsors", "sched_i_total_usd", "d2d_usd",
          "ntee_t_non_d2d_usd", "part_ix_l1_usd", "foreign_l3_usd", "sub5k_full_usd", "sub5k_partial_usd",
          "recipients", "top10_share", "top100_share", "hhi", "published_source", "published_period", "metric",
          "published_share", "diff", "max_abs_diff", "source")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; repo CLI convention)")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache-top50", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    sy = n50.sponsor_years(pick_returns(load_np(a.np_cache)), panel, rank)
    item = {k: v for k, v in sy.items() if v["pre"] == "itemised"}

    def lines(k):
        v = item[k]
        return rs.load_lines(v["x"]["oid"], v["x"]["sched_i_lines"],
                             a.lines_cache_top50 if v["tier"] == "top50" else a.lines_cache, [], False)
    keys = sorted(item)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        loaded = dict(zip(keys, ex.map(lines, keys)))
    good = {k: drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    tiers = {k: item[k]["tier"] for k in good}

    wl = read_csv(rs.WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    groups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in groups.items() if k and len(v) == 1}
    eins = frozenset(l[0] for v in good.values() for l in v["lines"] if l[0])
    bmf = rs.load_bmf(a.bmf_dir, eins)
    ann = {k: rs.annotate(k[0], v["lines"], bmf, wl_eins, wl_names) for k, v in good.items()}

    gap = {(ein9(r["ein"]), int(r["fiscal_year"])): {"l1": num(r["l1"]) or 0.0, "l3": num(r["l3"]) or 0.0,
                                                     "w2": num(r["w2"]) if r["w2"] not in ("", None) else 1.0,
                                                     "si_non": num(r["si_non_d2d"]) or 0.0, "si_d2d": num(r["si_d2d"]) or 0.0,
                                                     "partial": r["partial"]}
           for r in read_csv(GAP_CSV) if r["row_type"] == "sponsor_itemised"}
    fgn = {(ein9(r["ein"]), int(r["fiscal_year"])): num(r["part_ix_l3_foreign_usd"]) or 0.0
           for r in read_csv(FGN_CSV) if r["row_type"] == "sponsor_year"}

    agg = {k: {**sy_aggregate(ann[k], gap.get(k, {})), "ein": k[0], "fy": k[1], "tier": tiers[k],
               "segment": panel[k[0]]["segment"]} for k in good}

    # checks
    chk_si = max((abs(agg[k]["si_total"] - gap[k]["si_non"] - gap[k]["si_d2d"]) for k in agg if k in gap), default=0.0)
    chk_d2d = max((abs(sum(agg[k]["d2d"].values()) - gap[k]["si_d2d"]) for k in agg if k in gap), default=0.0)
    fgn_diff = {f"{panel[k[0]]['name'][:40]} FY{k[1]}": round(agg[k]["l3"] - fgn[k]) for k in agg
                if k in fgn and abs(agg[k]["l3"] - fgn[k]) > 1}

    uh = lambda k: agg[k]["segment"] == "university_hospital"  # noqa: E731
    seg = lambda s: (lambda k: agg[k]["segment"] == s)  # noqa: E731
    SVCF = rs.SVCF
    scopes = (
        ("all_itemising", "all", "all", "", lambda k: True),
        ("all_ex_university_hospital", "all", "all", "", lambda k: not uh(k)),
        ("top50_ex_university_hospital", "all", "top50", "", lambda k: tiers[k] == "top50" and not uh(k)),
        ("non_top50", "all", "other", "", lambda k: tiers[k] == "other"),
        ("non_top50_ex_university_hospital", "all", "other", "", lambda k: tiers[k] == "other" and not uh(k)),
        *((s, "segment", "all", s, seg(s)) for s in ("national", "processor", "community_foundation", "single_issue",
                                                     "university_hospital")),
        ("community_foundation_ex_svcf", "segment", "all", "community_foundation",
         lambda k: agg[k]["segment"] == "community_foundation" and k[0] != SVCF),
        *((f"non_top50_{s}", "segment", "other", s, (lambda k, s=s: tiers[k] == "other" and agg[k]["segment"] == s))
          for s in ("national", "community_foundation", "single_issue")),
        *((f"top50_{s}", "segment", "top50", s, (lambda k, s=s: tiers[k] == "top50" and agg[k]["segment"] == s))
          for s in ("national", "community_foundation", "single_issue")),
        *((panel[e]["name"], "sponsor", "top50", panel[e]["segment"], (lambda k, e=e: k[0] == e))
          for e in (FIDELITY, SCHWAB, VANGUARD, NPT)),
    )
    conc_scopes = {"all_itemising", "all_ex_university_hospital", "top50_ex_university_hospital", "non_top50",
                   "non_top50_ex_university_hospital", "community_foundation_ex_svcf", "non_top50_community_foundation"}

    def parts_for(pred, basis):
        per = {fy: scope_fy(tuple(scaled(agg[k], agg[k]["w2"]) if basis == "daf_weighted" else agg[k]
                                  for k in agg if k[1] == fy and pred(k))) for fy in FYS}
        return {**{str(fy): p for fy, p in per.items() if p["sponsor_years"]},
                "2023-2024": combine_fy(tuple(p for p in per.values() if p["sponsor_years"]))}

    rows, pooled = [], {}
    for name, stype, tier, segname, pred in scopes:
        for basis in ("schedule_i", "daf_weighted"):
            parts = parts_for(pred, basis)
            if not parts["2023-2024"]["sponsor_years"]:
                continue
            pooled[(name, basis)] = parts
            for fy_label, p in parts.items():
                tr = TREATMENTS if fy_label in ("2024", "2023-2024") else ("t_a_base",)
                conc = (concentration(ann, [k for k in agg if pred(k) and (fy_label == "2023-2024" or str(k[1]) == fy_label)])
                        if basis == "schedule_i" and name in conc_scopes else None)
                meta = {"scope": name, "scope_type": stype, "tier_filter": tier, "segment": segname,
                        "fiscal_year": fy_label, "source": SOURCE}
                rows.extend(share_rows(meta, p, basis, tr, conc))

    sy_parts = {e: {k: v for k, v in pooled[(panel[e]["name"], "schedule_i")].items() if k in ("2024", "2023-2024")}
                for e in (FIDELITY, VANGUARD) if (panel[e]["name"], "schedule_i") in pooled}
    recon = recon_rows(sy_parts)
    rows.extend({**r, "scope": panel[r["scope"]]["name"],
                 **({"source": "published split (doc source register) vs the sponsor's Schedule I lines"}
                    if r["sector"] == "SUM_ABS_DIFF" else {})} for r in recon)
    write_csv(a.out, rows, FIELDS)

    def shares(name, fy="2023-2024", basis="schedule_i", t="t_a_base", layer="sched_i"):
        return {r["sector"]: (round(r["share"], 4) if r["share"] is not None else None, r["amount_usd"])
                for r in rows if r["row_type"] == "share" and r["scope"] == name and r["fiscal_year"] == fy
                and r["basis"] == basis and r["treatment"] == t and r["layer"] == layer}
    all_row = lambda name, **kw: next(r for r in rows if r["row_type"] == "share" and r["scope"] == name and r["sector"] == "ALL"  # noqa: E731
                                      and r["fiscal_year"] == kw.get("fy", "2023-2024") and r["basis"] == kw.get("basis", "schedule_i")
                                      and r["treatment"] == kw.get("t", "t_a_base") and r["layer"] == kw.get("layer", "sched_i"))
    summary = {
        "sponsor_years_panel": len(sy), "itemised": len(item), "lines_ok": len(good),
        "load_problems": {f"{k[0]} FY{k[1]}": v["status"] for k, v in loaded.items() if v["status"] != "ok"},
        "sponsor_years_by_tier": {t: sum(1 for k in good if tiers[k] == t) for t in ("top50", "other")},
        "sponsors": len({k[0] for k in good}), "lines_total": sum(len(v["lines"]) for v in good.values()),
        "distinct_eins": len(eins), "bmf_matched": len(bmf),
        "gap_rows_matched": sum(1 for k in good if k in gap), "check_max_abs_si_total_vs_gap_csv": round(chk_si, 2),
        "check_max_abs_d2d_vs_gap_csv": round(chk_d2d, 2), "foreign_l3_vs_foreign_csv_diffs_top50": fgn_diff,
        "top50_foreign_csv_rows_matched": sum(1 for k in agg if k in fgn),
        "method_mix_non_d2d_all": rs.method_mix(ann),
        "all_rows": {n: {k: all_row(n, **kw)[k] for k in ("amount_usd", "sched_i_total_usd", "d2d_usd", "ntee_t_non_d2d_usd",
                                                           "part_ix_l1_usd", "foreign_l3_usd", "sub5k_full_usd",
                                                           "sub5k_partial_usd", "sponsor_years", "sponsors", "recipients",
                                                           "top10_share", "top100_share", "hhi", "lines") if k in all_row(n, **kw)}
                     for n, kw in (("all_itemising", {}), ("all_ex_university_hospital", {}),
                                   ("top50_ex_university_hospital", {}), ("non_top50", {}),
                                   ("non_top50_ex_university_hospital", {}), ("community_foundation_ex_svcf", {}),
                                   ("non_top50_community_foundation", {}))},
        "shares": {f"{n}|{t}|{l}": shares(n, t=t, layer=l)
                   for n in ("all_ex_university_hospital", "top50_ex_university_hospital", "non_top50_ex_university_hospital")
                   for t in TREATMENTS for l in LAYERS},
        "shares_dw": {f"{n}|{l}": shares(n, basis="daf_weighted", layer=l)
                      for n in ("all_ex_university_hospital", "non_top50_ex_university_hospital") for l in LAYERS},
        "segments": {n: shares(n, layer=l) for n in ("national", "community_foundation", "community_foundation_ex_svcf",
                                                    "single_issue", "non_top50_national", "non_top50_community_foundation",
                                                    "non_top50_single_issue", "top50_community_foundation", "processor")
                     for l in ("plus_foreign_sub5k",)},
        "by_fy_all_ex_uh": {fy: shares("all_ex_university_hospital", fy=fy, layer="plus_foreign_sub5k") for fy in ("2023", "2024")},
        "schwab_fy2024": {t: shares(panel[SCHWAB]["name"], fy="2024", t=t, layer="plus_foreign_sub5k") for t in TREATMENTS},
        "vanguard_fy2024": {t: shares(panel[VANGUARD]["name"], fy="2024", t=t, layer="plus_foreign_sub5k") for t in TREATMENTS},
        "recon_sum_abs": [(r["scope"][:20], r["fiscal_year"], r["published_source"][:30], r["metric"], r["treatment"],
                           r["layer"], r["share"], r["max_abs_diff"]) for r in recon if r["sector"] == "SUM_ABS_DIFF"],
        "recon_fid_fy2024": [(r["published_source"][:22], r["metric"], r["treatment"], r["layer"], r["sector"],
                              r["published_share"], r["share"], r["diff"]) for r in recon
                             if r["sector"] != "SUM_ABS_DIFF" and r["fiscal_year"] == "2024" and r["scope"] == FIDELITY
                             and r["layer"] in ("sched_i", "plus_foreign_sub5k")],
        "recon_vg": [(r["published_source"][-16:], r["treatment"], r["sector"], r["published_share"], r["share"])
                     for r in recon if r["scope"] == VANGUARD and r["fiscal_year"] == "2024" and r["sector"] != "SUM_ABS_DIFF"],
        "rows": len(rows),
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
