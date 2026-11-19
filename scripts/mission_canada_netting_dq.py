#!/usr/bin/env python3
"""Canadian DAF payout netted of sponsor-to-sponsor / foundation transfers, and DAF payout vs the charity-level
disbursement quota (queue items P-B39N3-04 and P-B39N3-06).

Builds on scripts/mission_canada_daf_panel.py, which it imports unchanged (panel rows, helpers).
Stdlib only; functional style (pure transforms, I/O at the edges, no mutable global state).

Inputs (CRA "List of charities" open data, open.canada.ca; one dataset per FPE year):
  --data-dir   the panel's files: {Y}_abc_*, {Y}_ident_*, {Y}_fin_* for Y = 2023, 2024, 2025
  --extra-dir  {Y}_qd_qualified_donees_{Y}_updated.csv and {Y}_dq_schedule_8_dq_{Y}_updated.csv, Y = 2024, 2025
               (T1236 qualified-donee worksheet: donor BN, FPE, donee BN, donee name, Total Gifts;
                Schedule 8 lines 805-890)

(A) Netting. For each panel sponsor-year (line 5860 = Y) in the 2024 and 2025 releases, the sponsor's T1236 gifts
for the same FPE are classified by donee:
  self                 donee BN (9-digit root) = donor BN (dropped)
  sponsor_daf_primary  donee answered 5860 = Y in a 2023-2025 release and, in its latest such return, DAF assets
                       (5862) are at least half of total assets (4200): a DAF-primary sponsor
  sponsor_other        any other donee that answered 5860 = Y in a 2023-2025 release
  private_foundation   designation B, never a 5860 = Y filer
  public_foundation    designation A, never a 5860 = Y filer
  charitable_org       designation C, never a 5860 = Y filer
  unmatched            donee BN / name not found in the 2023-2025 Identification files (non-charity qualified
                       donees such as municipalities, universities abroad, or malformed BNs)
Donee resolution: exact 15-character BN; else the 9-digit BN root (RR0001 preferred); else an exact match of the
normalised donee name to a single legal name.
Transfer tiers (nested, in the spirit of the US tiers A/B/C in scripts/mission_net_payout.py):
  tier_a = sponsor_daf_primary (narrow DAF-to-DAF); tier_b = tier_a + sponsor_other (any 5860 = Y donee);
  tier_c = tier_b + private and public foundations that never answered 5860 = Y (upper bound).
Gifts are all T1236 gifts of the sponsor (DAF and non-DAF money), so transfers are capped at 5864 as in the US.
netting_coverage: 'itemised' if the sponsor has T1236 rows for the FPE or 5864 is zero, else 'no_t1236' (unknown).
US netted definition: net_t = 5864 - min(transfers_t, 5864); net payout = net_t / prior-release 5862 (matched BNs).
Blank 5864 counts as zero (wave-37B convention).

(B) Disbursement quota. Schedule 8 rows joined on (BN, FPE). Line 840 = DQ requirement; 860 = 845 + 850 + 855
(charitable activities + grants to grantees + gifts to qualified donees); 865 = 860 - 840 (excess / shortfall).
Recomputed DQ from line 815: 3.5% if <= C$1m, else C$35,000 + 5% of the excess over C$1m (CRA dictionary 3.19;
ITA s.149.1(1)). Route codes per sponsor-year are documented in route_for().

Usage:
  python3 scripts/mission_canada_netting_dq.py . --data-dir DIR --extra-dir DIR2
      [--out data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv] [--summary FILE.json]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import statistics
import sys
from functools import reduce
from itertools import groupby
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_canada_daf_panel as panel  # noqa: E402  (imported, not modified)

NET_YEARS = (2024, 2025)
CATEGORIES = ("self", "sponsor_daf_primary", "sponsor_other", "private_foundation", "public_foundation",
              "charitable_org", "unmatched")
TIERS = {
    "tier_a": ("sponsor_daf_primary",),
    "tier_b": ("sponsor_daf_primary", "sponsor_other"),
    "tier_c": ("sponsor_daf_primary", "sponsor_other", "private_foundation", "public_foundation"),
}
DQ_LINES = ("805", "810", "815", "840", "845", "850", "855", "860", "865", "870")
TOP_N = 20

FIELDS = [
    "dataset_year", "bn", "fpe", "legal_name", "designation", "rank_assets_in_year", "top20",
    "daf_assets_5862", "prior_daf_assets_5862", "daf_disbursements_5864", "total_assets_4200",
    "qd_rows", "qd_total_gifts", "line_5050", "netting_coverage",
    *[f"gifts_{c}" for c in CATEGORIES],
    "n_donees_sponsor", "n_donees_foundation",
    *[f"transfers_{t}" for t in TIERS],
    *[f"net_5864_{t}" for t in TIERS],
    "payout_prior_gross", *[f"payout_prior_net_{t}" for t in TIERS],
    "has_schedule8", *[f"dq_{x}" for x in DQ_LINES],
    "dq_recomputed", "dq_check", "dq_requirement_used", "dq_rate_on_base", "dq_over_prior_daf_assets",
    "daf_5864_over_dq", "net_b_over_dq", "dq_on_prior_daf_assets", "daf_meets_own_dq_proxy_gross",
    "daf_meets_own_dq_proxy_net_b", "dq_spending_used", "dq_spending_source", "dq_excess_used",
    "prior_release_dq_865", "shortfall_covered_by_prior_release_excess", "route",
]


# ---------- pure helpers ----------
def z(v: float | None) -> float:
    return v or 0.0


def norm_name(s: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())


def bn_root(s: str) -> str | None:
    m = re.match(r"\s*(\d{9})", s or "")
    return m.group(1) if m else None


def dq_formula(base: float | None) -> float | None:
    """CRA dictionary 3.19 lines 820-835 (ITA s.149.1(1) 'disbursement quota', B(a)/(b)); no day pro-rating and
    no C$25k/C$100k de minimis (the schedule shows 3.5% for any base up to C$1m)."""
    if base is None:
        return None
    b = max(base, 0.0)
    return 0.035 * b if b <= 1_000_000 else 35_000 + 0.05 * (b - 1_000_000)


def group_by(rows: Iterable, key) -> dict:
    """{key: [items]} via sort + groupby (stable, no mutation of inputs)."""
    return {k: list(g) for k, g in groupby(sorted(rows, key=lambda r: str(key(r))), key=key)}


def fold_sum(pairs: Iterable[tuple]) -> dict:
    """[(key, amount)] -> {key: sum}."""
    return {k: sum(v for _, v in g) for k, g in groupby(sorted(pairs, key=lambda kv: str(kv[0])), key=lambda kv: kv[0])}


# ---------- registries ----------
def ident_registry(data_dir: str) -> dict:
    """BN -> (designation, legal name), later releases override earlier ones; plus root and name indexes."""
    rows = [r for y in panel.YEARS for r in panel.read_csv(panel.find(data_dir, y, "ident"))]
    by_bn = {r["BN"]: (r.get("Designation", ""), r.get("Legal Name", "")) for r in rows}
    roots = group_by(sorted(by_bn), lambda bn: bn[:9])
    names = group_by(sorted(by_bn), lambda bn: norm_name(by_bn[bn][1]))
    return {
        "by_bn": by_bn,
        "by_root": {k: v[0] for k, v in roots.items()},  # sorted -> RR0001 first
        "by_name": {k: v[0] for k, v in names.items() if k and len(v) == 1},
    }


def resolve(reg: dict, donee_bn: str, donee_name: str) -> tuple[str | None, str]:
    bn = (donee_bn or "").strip().upper().replace(" ", "")
    if bn in reg["by_bn"]:
        return bn, "bn"
    root = bn_root(bn)
    if root and root in reg["by_root"]:
        return reg["by_root"][root], "root"
    nm = norm_name(donee_name)
    if nm in reg["by_name"]:
        return reg["by_name"][nm], "name"
    return None, "none"


def sponsor_map(panel_rows: list[dict]) -> dict:
    """BN -> True if DAF-primary (5862 >= 50% of 4200 in its latest 5860 = Y return), for every panel BN."""
    latest = {r["bn"]: r for r in sorted(panel_rows, key=lambda r: (r["dataset_year"], r["fpe"]))}
    return {bn: (r["daf_share_of_total_assets"] or 0) >= 0.5 for bn, r in latest.items()}


def classify(reg: dict, sponsors: dict, donor: str, donee: str | None) -> str:
    if donee is None:
        return "unmatched"
    if donee == donor or donee[:9] == donor[:9]:
        return "self"
    des = reg["by_bn"].get(donee, ("", ""))[0]
    if donee in sponsors:
        return "sponsor_daf_primary" if sponsors[donee] else "sponsor_other"
    return {"A": "public_foundation", "B": "private_foundation", "C": "charitable_org"}.get(des, "unmatched")


# ---------- netting ----------
def gifts_for(qd_rows: list[dict], reg: dict, sponsors: dict, donor: str) -> dict:
    resolved = [(resolve(reg, r.get("Donee BN", ""), r.get("Donee Name", ""))[0], z(panel.num(r.get("Total Gifts"))))
                for r in qd_rows]
    tagged = [(classify(reg, sponsors, donor, d), d, amt) for d, amt in resolved]
    sums = fold_sum((c, amt) for c, _, amt in tagged)
    return {
        "qd_rows": len(qd_rows),
        "qd_total_gifts": sum(a for _, _, a in tagged),
        **{f"gifts_{c}": sums.get(c, 0.0) for c in CATEGORIES},
        "n_donees_sponsor": len({d for c, d, _ in tagged if c in TIERS["tier_b"]}),
        "n_donees_foundation": len({d for c, d, _ in tagged if c in ("private_foundation", "public_foundation")}),
        "_edges": [(donor, d, c, a) for c, d, a in tagged if c in TIERS["tier_c"] and a],
    }


def netting(row: dict, g: dict) -> dict:
    dis = z(row["daf_disbursements_5864"])
    prior = row["prior_daf_assets_5862"]
    tr = {t: sum(g[f"gifts_{c}"] for c in cats) for t, cats in TIERS.items()}
    net = {t: dis - min(max(v, 0.0), dis) for t, v in tr.items()}
    return {
        **{f"transfers_{t}": v for t, v in tr.items()},
        **{f"net_5864_{t}": v for t, v in net.items()},
        "payout_prior_gross": panel.ratio(dis, prior),
        **{f"payout_prior_net_{t}": panel.ratio(v, prior) for t, v in net.items()},
    }


# ---------- disbursement quota ----------
def first_present(*vals):
    return next((v for v in vals if v is not None), None)


def sum_present(vals: list) -> float | None:
    present = [v for v in vals if v is not None]
    return sum(present) if present else None


def dq_fields(row: dict, dq: dict | None, prior_dq: dict | None, net_b: float, fin_row: dict) -> dict:
    g = (lambda k: panel.num(dq.get(k))) if dq else (lambda k: None)
    filed_base = g("815")
    base = filed_base if filed_base is not None else (
        max(z(g("805")) - z(g("810")), 0.0) if g("805") is not None else None)
    rec = dq_formula(base)
    filed_req = g("840")
    req = filed_req if filed_req is not None else rec
    prior = row["prior_daf_assets_5862"]
    dis = z(row["daf_disbursements_5864"])
    own = dq_formula(prior) if prior else None
    f = lambda k: panel.num(fin_row.get(k))
    spend = first_present(g("860"), sum_present([g("845"), g("850"), g("855")]),
                          sum_present([f("5000"), f("5045"), f("5050")]) if dq else None)
    spend_src = ("860" if g("860") is not None else "845+850+855" if sum_present([g("845"), g("850"), g("855")]) is not None
                 else "sched6_5000+5045+5050" if spend is not None else None)
    gap = None if req is None or spend is None else spend - req
    pr = panel.num(prior_dq.get("865")) if prior_dq else None
    return {
        "has_schedule8": dq is not None,
        **{f"dq_{x}": g(x) for x in DQ_LINES},
        "dq_recomputed": rec,
        "dq_check": (None if dq is None else "840_blank_recomputed_from_805" if filed_req is None and rec is not None
                     else None if req is None or rec is None
                     else "ok" if abs(req - rec) <= max(2.0, 0.001 * rec) else "differs"),
        "dq_requirement_used": req,
        "dq_rate_on_base": panel.ratio(req, base),
        "dq_over_prior_daf_assets": panel.ratio(req, prior),
        "daf_5864_over_dq": panel.ratio(dis, req),
        "net_b_over_dq": panel.ratio(net_b, req),
        "dq_on_prior_daf_assets": own,
        "daf_meets_own_dq_proxy_gross": None if own is None else dis >= own,
        "daf_meets_own_dq_proxy_net_b": None if own is None else net_b >= own,
        "dq_spending_used": spend, "dq_spending_source": spend_src, "dq_excess_used": gap,
        "prior_release_dq_865": pr,
        "shortfall_covered_by_prior_release_excess": (None if gap is None or gap >= 0 else
                                                      pr is not None and pr >= -gap),
    }


def route_for(r: dict) -> str:
    """Route by which the sponsor meets its charity-level DQ in the year (Schedule 8 as filed):
    NO_SCHEDULE8           no Schedule 8 row for this BN/FPE
    NO_DQ                  requirement zero or not computable (840 blank and 805 blank)
    INCOMPLETE             requirement known but no spending lines (860, 845-855, Schedule 6 5000/5045/5050)
    DAF_NET_COVERS         DAF disbursements net of tier-B sponsor transfers >= 840
    DAF_GROSS_ONLY         5864 >= 840 > 5864 net of tier-B transfers (relies on gifts to other DAF sponsors)
    NEEDS_NON_DAF          5864 < 840 <= 860 (meets only with non-DAF charitable spending / gifts)
    SHORTFALL              spending < requirement (needs a carry-forward of an excess from up to five earlier years
                           or a carry-back from the next year, ITA s.149.1(20)-(21))
    Spending = line 860, else 845+850+855, else Schedule 6 lines 5000+5045+5050 (dq_spending_source)."""
    if not r["has_schedule8"]:
        return "NO_SCHEDULE8"
    req, tot, dis = r["dq_requirement_used"], r["dq_spending_used"], z(r["daf_disbursements_5864"])
    if not req:
        return "NO_DQ"
    if tot is None:
        return "INCOMPLETE"
    if tot < req:
        return "SHORTFALL"
    if dis < req:
        return "NEEDS_NON_DAF"
    return "DAF_NET_COVERS" if r["net_5864_tier_b"] >= req else "DAF_GROSS_ONLY"


# ---------- assembly ----------
def build(panel_rows: list[dict], fin_by_key: dict, qd_by_key: dict, dq_by_key: dict, dq_by_bn_year: dict,
          reg: dict) -> tuple[list[dict], list[tuple]]:
    sponsors = sponsor_map(panel_rows)
    cur = [r for r in panel_rows if r["dataset_year"] in NET_YEARS]
    top = {(r["dataset_year"], r["bn"]) for r in cur if r["rank_assets_in_year"] <= TOP_N}

    def one(r: dict) -> tuple[dict, list]:
        key = (r["bn"], r["fpe"])
        g = gifts_for(qd_by_key.get(key, []), reg, sponsors, r["bn"])
        n = netting(r, g)
        d = dq_fields(r, dq_by_key.get(key), dq_by_bn_year.get((r["bn"], r["dataset_year"] - 1)), n["net_5864_tier_b"],
                      fin_by_key.get(key, {}))
        out = {
            **{k: r[k] for k in ("dataset_year", "bn", "fpe", "legal_name", "designation", "rank_assets_in_year",
                                 "daf_assets_5862", "prior_daf_assets_5862", "daf_disbursements_5864",
                                 "total_assets_4200")},
            "top20": (r["dataset_year"], r["bn"]) in top,
            "line_5050": panel.num(fin_by_key.get(key, {}).get("5050")),
            "netting_coverage": "itemised" if g["qd_rows"] or not z(r["daf_disbursements_5864"]) else "no_t1236",
            **{k: v for k, v in g.items() if not k.startswith("_")}, **n, **d,
        }
        return {**out, "route": route_for(out)}, [(r["dataset_year"],) + e for e in g["_edges"]]

    pairs = [one(r) for r in cur]
    return [p[0] for p in pairs], [e for p in pairs for e in p[1]]


# ---------- summaries ----------
def agg_payout(rows: list[dict]) -> dict:
    m = [r for r in rows if r["prior_daf_assets_5862"]]
    base = sum(r["prior_daf_assets_5862"] for r in m)
    gross = sum(z(r["daf_disbursements_5864"]) for r in m)
    pos = [r for r in m if r["prior_daf_assets_5862"] > 0]
    big = [r for r in pos if r["prior_daf_assets_5862"] >= 10_000_000]
    med = lambda sel, k: statistics.median([z(r[k]) for r in sel]) if sel else None
    return {
        "n_matched": len(m), "prior_assets": base, "gross_5864": gross,
        "payout_gross": panel.ratio(gross, base),
        **{f"transfers_{t}": sum(r[f"transfers_{t}"] for r in m) for t in TIERS},
        **{f"capped_transfers_{t}": sum(z(r["daf_disbursements_5864"]) - r[f"net_5864_{t}"] for r in m) for t in TIERS},
        **{f"payout_net_{t}": panel.ratio(sum(r[f"net_5864_{t}"] for r in m), base) for t in TIERS},
        "median_gross_blank_as_zero": med(pos, "payout_prior_gross"),
        **{f"median_net_{t}": med(pos, f"payout_prior_net_{t}") for t in TIERS},
        "n_ge_10m": len(big),
        "median_gross_ge_10m": med(big, "payout_prior_gross"),
        **{f"median_net_{t}_ge_10m": med(big, f"payout_prior_net_{t}") for t in TIERS},
        "share_lt_5pct_gross": (sum(1 for r in pos if z(r["payout_prior_gross"]) < 0.05) / len(pos)) if pos else None,
        **{f"share_lt_5pct_net_{t}": (sum(1 for r in pos if z(r[f"payout_prior_net_{t}"]) < 0.05) / len(pos))
           if pos else None for t in TIERS},
    }


def year_summary(rows: list[dict], y: int) -> dict:
    yr = [r for r in rows if r["dataset_year"] == y]
    dis_pos = [r for r in yr if z(r["daf_disbursements_5864"]) > 0]
    cats = {c: sum(r[f"gifts_{c}"] for r in yr) for c in CATEGORIES}
    routes = fold_sum((r["route"], 1) for r in yr)
    routes_top = fold_sum((r["route"], 1) for r in yr if r["top20"])
    return {
        "year": y, "sponsors": len(yr),
        "with_qd_rows": sum(1 for r in yr if r["qd_rows"]),
        "share_5864_dollars_with_qd_rows": panel.ratio(sum(z(r["daf_disbursements_5864"]) for r in dis_pos if r["qd_rows"]),
                                                       sum(z(r["daf_disbursements_5864"]) for r in dis_pos)),
        "qd_total_gifts": sum(r["qd_total_gifts"] for r in yr),
        "line_5050_total": sum(z(r["line_5050"]) for r in yr),
        "gross_5864": sum(z(r["daf_disbursements_5864"]) for r in yr),
        "gifts_by_category": cats,
        "transfers_by_tier_all_sponsors": {t: sum(r[f"transfers_{t}"] for r in yr) for t in TIERS},
        "transfers_by_tier_share_of_5864": {t: panel.ratio(sum(z(r["daf_disbursements_5864"]) - r[f"net_5864_{t}"] for r in yr),
                                                          sum(z(r["daf_disbursements_5864"]) for r in yr)) for t in TIERS},
        "payout_matched": agg_payout(yr),
        "payout_matched_itemised_only": agg_payout([r for r in yr if r["netting_coverage"] == "itemised"]),
        "no_t1236_rows": {"n": sum(1 for r in yr if r["netting_coverage"] == "no_t1236"),
                          "gross_5864": sum(z(r["daf_disbursements_5864"]) for r in yr if r["netting_coverage"] == "no_t1236")},
        "payout_matched_top20": agg_payout([r for r in yr if r["top20"]]),
        "schedule8_rows": sum(1 for r in yr if r["has_schedule8"]),
        "dq_check": fold_sum((r["dq_check"] or "na", 1) for r in yr),
        "routes_all": routes, "routes_top20": routes_top,
        "routes_all_daf_assets": fold_sum((r["route"], z(r["daf_assets_5862"])) for r in yr),
        "routes_by_designation": fold_sum((f'{r["designation"]}:{r["route"]}', 1) for r in yr),
        "shortfall_rows": [{k: r[k] for k in ("bn", "legal_name", "designation", "daf_assets_5862",
                                              "daf_disbursements_5864", "dq_requirement_used", "dq_spending_used",
                                              "dq_spending_source", "dq_excess_used", "prior_release_dq_865",
                                              "shortfall_covered_by_prior_release_excess")}
                           for r in sorted(yr, key=lambda r: -z(r["daf_assets_5862"])) if r["route"] == "SHORTFALL"],
        "shortfall_covered_by_prior_release_excess": sum(
            1 for r in yr if r["route"] == "SHORTFALL" and r["shortfall_covered_by_prior_release_excess"]),
        "shortfall_by_designation": fold_sum((r["designation"], 1) for r in yr if r["route"] == "SHORTFALL"),
        "needs_non_daf_by_designation": fold_sum((r["designation"], 1) for r in yr if r["route"] == "NEEDS_NON_DAF"),
        "own_dq_proxy_matched": {
            sel: {"n": len(rs), "meets_gross": sum(1 for r in rs if r["daf_meets_own_dq_proxy_gross"]),
                  "meets_net_tier_b": sum(1 for r in rs if r["daf_meets_own_dq_proxy_net_b"])}
            for sel, rs in (("all", [r for r in yr if r["dq_on_prior_daf_assets"] is not None]),
                            ("top20", [r for r in yr if r["top20"] and r["dq_on_prior_daf_assets"] is not None]))},
        "sponsors_with_tier_b_donees_dq": fold_sum((r["route"], 1) for r in yr if r["transfers_tier_b"] > 0),
    }


def top_edges(edges: list[tuple], reg: dict, y: int, n: int = 15) -> list[dict]:
    yr = [e for e in edges if e[0] == y]
    s = fold_sum(((e[1], e[2], e[3]), e[4]) for e in yr)
    name = lambda bn: reg["by_bn"].get(bn, ("", ""))[1]
    return [{"donor": k[0], "donor_name": name(k[0]), "donee": k[1], "donee_name": name(k[1]), "category": k[2],
             "amount": v} for k, v in sorted(s.items(), key=lambda kv: -kv[1])[:n]]


def top20_table(rows: list[dict]) -> list[dict]:
    keep = ("dataset_year", "rank_assets_in_year", "bn", "legal_name", "daf_assets_5862", "prior_daf_assets_5862",
            "daf_disbursements_5864", "transfers_tier_a", "transfers_tier_b", "transfers_tier_c",
            "netting_coverage", "payout_prior_gross", "payout_prior_net_tier_a", "payout_prior_net_tier_b",
            "payout_prior_net_tier_c", "dq_815", "dq_840", "dq_requirement_used", "dq_860", "dq_spending_used",
            "dq_excess_used", "shortfall_covered_by_prior_release_excess",
            "dq_865", "dq_check", "daf_5864_over_dq", "net_b_over_dq", "dq_on_prior_daf_assets",
            "daf_meets_own_dq_proxy_net_b", "prior_release_dq_865", "route")
    return [{k: r[k] for k in keep} for r in sorted((r for r in rows if r["top20"]),
                                                    key=lambda r: (r["dataset_year"], r["rank_assets_in_year"]))]


def to_csv_rows(rows: list[dict]) -> list[dict]:
    return [{k: panel.fmt(r[k]) for k in FIELDS}
            for r in sorted(rows, key=lambda r: (r["dataset_year"], r["rank_assets_in_year"]))]


# ---------- I/O ----------
def find_extra(extra_dir: str, year: int, kind: str) -> str:
    return panel.find(extra_dir, year, kind)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", help="repo root ('.')")
    ap.add_argument("--data-dir", required=True, help="panel inputs (abc, ident, fin for 2023-2025)")
    ap.add_argument("--extra-dir", required=True, help="qd and dq files for 2024-2025")
    ap.add_argument("--out", default="data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv")
    ap.add_argument("--summary", default=None)
    a = ap.parse_args(argv)

    panel_rows = panel.enrich([r for y in panel.YEARS for r in panel.load_year(a.data_dir, y)])
    keys = {(r["bn"], r["fpe"]) for r in panel_rows if r["dataset_year"] in NET_YEARS}
    bns = {k[0] for k in keys}
    fin = {(r["BN"], r["FPE"]): r for y in NET_YEARS for r in panel.read_csv(panel.find(a.data_dir, y, "fin"))
           if (r["BN"], r["FPE"]) in keys}
    qd = group_by((r for y in NET_YEARS for r in panel.read_csv(find_extra(a.extra_dir, y, "qd"))
                   if (r["BN"], r["FPE"]) in keys), lambda r: (r["BN"], r["FPE"]))
    dq_all = [dict(r, _year=y) for y in NET_YEARS for r in panel.read_csv(find_extra(a.extra_dir, y, "dq"))
              if r["BN"] in bns]
    dq_by_key = {(r["BN"], r["FPE"]): r for r in dq_all}
    dq_by_bn_year = reduce(lambda acc, r: {**acc, (r["BN"], r["_year"]): r}
                           if (r["BN"], r["_year"]) not in acc or r["FPE"] > acc[(r["BN"], r["_year"])]["FPE"] else acc,
                           dq_all, {})
    reg = ident_registry(a.data_dir)

    rows, edges = build(panel_rows, fin, qd, dq_by_key, dq_by_bn_year, reg)
    out = os.path.join(a.root, a.out)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(to_csv_rows(rows))

    resolution = fold_sum((resolve(reg, r.get("Donee BN", ""), r.get("Donee Name", ""))[1], 1)
                          for v in qd.values() for r in v)
    summary = {
        "panel_rows_by_year": fold_sum((r["dataset_year"], 1) for r in panel_rows),
        "donee_resolution_rows": resolution,
        "years": [year_summary(rows, y) for y in NET_YEARS],
        "top_transfer_edges": {y: top_edges(edges, reg, y) for y in NET_YEARS},
        "top20": top20_table(rows),
    }
    text = json.dumps(summary, indent=1, default=str)
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
