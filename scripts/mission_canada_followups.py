#!/usr/bin/env python3
"""Canada follow-ups P-B3946-01, -03 and -04 to b39n3-0406 (netting and disbursement quota).

Imports scripts/mission_canada_daf_panel.py and scripts/mission_canada_netting_dq.py unchanged and rebuilds their
sponsor rows and transfer edges in memory (it never calls their main(), so their CSVs are not rewritten).
Stdlib only; functional style (pure transforms, I/O at the edges, no mutable global state).

(01) Public-foundation donees of DAF sponsors (tier C, class 'public_foundation' in mission_canada_netting_dq)
     are typed from the donee's CRA category / sub-category code (Identification file; codes_en.pdf) and its
     legal name, plus the donee's own return (line 4700 revenue, 5050 gifts to qualified donees, T1236 rows):
       giving_platform       CanadaHelps (BN 896568417), or any donee with >= 1,000 T1236 rows and line 5050 >= 80%
                             of line 4700 (a pass-through rule; it also catches PayPal Giving Fund Canada)
       federation_united_way United Way / Centraide / Jewish federations (Federation CJA, UJA) / ShareLife (name)
       hospital_health       hospital / health / cancer / hospice names, or category 0100-0140 (health)
       university_college    university / college / cegep / polytechnic / institute-of-technology names
       other_education       other donees in categories 0010-0015 (education)
       community_foundation  'community foundation' / 'fondation communautaire' names (none answered 5860 = Y)
       religious             categories 0030-0090
       other                 the rest
     Nested middle tiers between tier B (any 5860 = Y donee) and tier C (+ all private and public foundations):
       tier_b_ch    = B + CanadaHelps only
       tier_bp      = B + giving_platform                       (the rebuilt middle tier)
       tier_bp_cf   = tier_bp + community_foundation
       tier_bp_cf_f = tier_bp_cf + federation_united_way
       tier_b_pub   = B + all public foundations (C without private foundations)
     Transfers are capped at line 5864 and payout is on prior-release line 5862, as in the parent script.

(03) Schedule 8 coverage: every v27 return (Section D / Schedule 6 file, one row per BN x FPE) with line 5900 above
     C$1m is checked for a Schedule 8 row (same BN and FPE; also any FPE of the BN). Counts by release, FPE
     month/quarter (the published Schedule 8 file has no Filing Date column although the dictionary lists one),
     form ID, line 5850 answer, designation, T1236 presence. For panel sponsors without Schedule 8 the DQ is
     imputed from line 5900 with the Schedule 8 formula and compared with 5864 and Schedule 6 spending.

(04) CanadaHelps CanaDon (BN 896568417RR0001): its own T3010 lines in each release, the sponsor gifts it receives,
     and the panel with CanadaHelps added as a sponsor under two proxies for line 5862: designated cash per its
     audited statements (quoted constants below) or line 4200; line 5864 proxy = its line 5050.

Usage:
  python3 scripts/mission_canada_followups.py . --data-dir DIR --extra-dir DIR2
      [--out data/mission-2026-11-14/canada-followups-2026-11-19.csv] [--summary FILE.json] [--check-parent CSV]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import statistics
import sys
import unicodedata
from functools import reduce

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_canada_daf_panel as panel  # noqa: E402  (imported, not modified)
import mission_canada_netting_dq as ndq  # noqa: E402  (imported, not modified)

YEARS = ndq.NET_YEARS
CANADAHELPS = "896568417RR0001"
# CanadaHelps CanaDon audited statements, "Designated cash" = "Contributions due to designated charities"
# (Statement of Financial Position): 2025-06-30 $11,019,785 and 2024-06-30 $10,028,476 (FY2025 statements, notes 7
# and 10); 2023-06-30 $8,874,105 (FY2024 statements, notes 6 and 9).
# https://www.canadahelps.org/media/2024-2025_CanadaHelps_CanaDon_FinancialStatement.pdf
# https://www.canadahelps.org/media/2023-2024_CanadaHelps_CanaDon_FinancialStatement.pdf
CH_DESIGNATED_CASH = {"2025-06-30": 11_019_785.0, "2024-06-30": 10_028_476.0, "2023-06-30": 8_874_105.0}
PLATFORM_MIN_ROWS = 1000
PLATFORM_MIN_PASS = 0.80

TYPES = ("giving_platform", "federation_united_way", "hospital_health", "university_college", "other_education",
         "community_foundation", "religious", "other")
VARIANTS = {
    "tier_b": (),
    "tier_b_ch": ("canadahelps",),
    "tier_bp": ("giving_platform",),
    "tier_bp_cf": ("giving_platform", "community_foundation"),
    "tier_bp_cf_f": ("giving_platform", "community_foundation", "federation_united_way"),
    "tier_b_pub": TYPES,
    "tier_c": TYPES + ("private_foundation",),
}

FED_RE = re.compile(r"UNITED WAY|CENTRAIDE|FEDERATION CJA|UNITED JEWISH APPEAL|JEWISH FEDERATION|"
                    r"COMBINED JEWISH APPEAL|\bUJA\b|SHARELIFE")
HOSP_RE = re.compile(r"HOSPITAL|HOPITAL|HEALTH|SANTE|\bCHU\b|CANCER|HOSPICE|MEDICAL|HEART INSTITUTE|"
                     r"MENTAL|REHABILITATION|SICKKIDS|BAYCREST")
UNIV_RE = re.compile(r"UNIVERSIT|COLLEGE|CEGEP|POLYTECHNI|INSTITUTE OF TECHNOLOGY|TECHNION|WEIZMANN|\bHEC\b")
CF_RE = re.compile(r"COMMUNITY FOUNDATION|FONDATION COMMUNAUTAIRE|COMMUNITY TRUST")
HEALTH_CATS = {"0100", "0110", "0120", "0130", "0140"}
EDU_CATS = {"0010", "0011", "0012", "0013", "0014", "0015"}
REL_CATS = {"0030", "0040", "0050", "0060", "0070", "0080", "0090"}

FIELDS = [
    "section", "dataset_year", "bn", "legal_name", "designation", "category_code", "sub_category_code",
    "donee_type", "type_rule", "received_from_sponsors", "n_sponsor_donors", "share_of_public_fdn_gifts",
    "own_revenue_4700", "own_gifts_5050", "own_total_assets_4200", "own_t1236_rows", "own_pass_through",
    "own_5860", "fpe", "form_id", "fpe_quarter", "line_5850", "line_5900", "has_t1236", "panel_sponsor",
    "daf_assets_5862", "daf_disbursements_5864", "imputed_dq_from_5900", "sched6_spending", "imputed_route",
    "variant", "population", "n_sponsors", "prior_daf_assets", "gross_5864", "transfers_capped", "payout_gross",
    "payout_net", "median_net", "share_lt_5pct", "scenario", "value", "note",
]


# ---------- pure helpers ----------
def z(v) -> float:
    return v or 0.0


def upper_ascii(s: str) -> str:
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper()


def fsum(pairs) -> dict:
    """[(key, amount)] -> {key: sum} (sort + groupby; no mutation)."""
    return ndq.fold_sum(pairs)


def latest(rs: list[dict]) -> dict:
    """BN -> row with the latest FPE."""
    return {r["BN"]: r for r in sorted(rs, key=lambda r: r["FPE"])}


def median(xs: list) -> float | None:
    return statistics.median(xs) if xs else None


def fpe_quarter(fpe: str) -> str:
    return f"{fpe[:4]}-Q{(int(fpe[5:7]) - 1) // 3 + 1}" if len(fpe) >= 7 else ""


def donee_type(bn: str, name: str, cat: str, prof: dict) -> tuple[str, str]:
    """(type, rule) for a public-foundation donee; first matching rule wins."""
    n = upper_ascii(name)
    if bn[:9] == CANADAHELPS[:9]:
        return "giving_platform", "named:CanadaHelps"
    if prof.get("t1236_rows", 0) >= PLATFORM_MIN_ROWS and z(prof.get("pass_through")) >= PLATFORM_MIN_PASS \
            and not FED_RE.search(n):
        return "giving_platform", f"data:t1236_rows>={PLATFORM_MIN_ROWS}&5050/4700>={PLATFORM_MIN_PASS}"
    if FED_RE.search(n):
        return "federation_united_way", "name"
    if HOSP_RE.search(n):
        return "hospital_health", "name"
    if cat in HEALTH_CATS:
        return "hospital_health", "category"
    if UNIV_RE.search(n):
        return "university_college", "name"
    if z(prof.get("share_gifts_to_health")) >= 0.5:
        return "hospital_health", "data:>=50% of own T1236 gifts to health donees"
    if z(prof.get("share_gifts_to_univ")) >= 0.5:
        return "university_college", "data:>=50% of own T1236 gifts to university/college donees"
    if cat in EDU_CATS:
        return "other_education", "category"
    if CF_RE.search(n):
        return "community_foundation", "name"
    if cat in REL_CATS:
        return "religious", "category"
    return "other", "residual"


def dq_route(dq: float | None, dis: float, net_b: float, spend: float | None) -> str:
    """Parent route codes (mission_canada_netting_dq.route_for) applied to an imputed DQ."""
    if not dq:
        return "NO_DQ"
    if spend is None:
        return "INCOMPLETE"
    if spend < dq:
        return "SHORTFALL"
    if dis < dq:
        return "NEEDS_NON_DAF"
    return "DAF_NET_COVERS" if net_b >= dq else "DAF_GROSS_ONLY"


# ---------- (01) public-foundation typing and middle tiers ----------
def donee_profiles(fin_by_year: dict, abc_by_year: dict, qd_rows_by_year: dict) -> dict:
    """(year, BN) -> own return profile (latest FPE of the BN in that release)."""
    def one(y, bn, f):
        rev, g = panel.num(f.get("4700")), panel.num(f.get("5050"))
        return (y, bn), {"revenue_4700": rev, "gifts_5050": g, "assets_4200": panel.num(f.get("4200")),
                         "t1236_rows": qd_rows_by_year[y].get(bn, 0),
                         "pass_through": panel.ratio(g, rev) if g is not None else None,
                         "own_5860": abc_by_year[y].get(bn, {}).get("5860", "")}
    return dict(one(y, bn, f) for y, rows in fin_by_year.items() for bn, f in rows.items())


def recipient_shares(qd_raw: dict, wanted: set, cats: dict) -> dict:
    """(year, BN) -> share of the BN's own T1236 gifts going to health-named/-coded and university-named donees."""
    def kind(r):
        bn = (r.get("Donee BN", "") or "").strip().upper().replace(" ", "")
        c = cats.get(bn, ("", "", "", ""))
        nm = upper_ascii(c[2] or r.get("Donee Name", ""))
        return ("health" if HOSP_RE.search(nm) or c[0] in HEALTH_CATS else
                "univ" if UNIV_RE.search(nm) else "other")
    rows = [(y, r["BN"], kind(r), z(panel.num(r.get("Total Gifts")))) for y in qd_raw for r in qd_raw[y]
            if (y, r["BN"]) in wanted]
    tot = fsum(((y, b), a) for y, b, _, a in rows)
    part = fsum(((y, b, k), a) for y, b, k, a in rows)
    return {key: {"share_gifts_to_health": panel.ratio(part.get(key + ("health",), 0.0), t),
                  "share_gifts_to_univ": panel.ratio(part.get(key + ("univ",), 0.0), t)} for key, t in tot.items()}


def typed_edges(edges: list[tuple], cats: dict, profiles: dict) -> list[dict]:
    """Tier-C edges (year, donor, donee, class, amount) with a donee type for public foundations."""
    def one(e):
        y, donor, donee, cls, amt = e
        if cls != "public_foundation":
            return {"year": y, "donor": donor, "donee": donee, "cls": cls, "amount": amt, "type": None, "rule": None}
        name, cat = cats.get(donee, ("", "", ""))[2], cats.get(donee, ("", "", ""))[0]
        t, rule = donee_type(donee, name, cat, profiles.get((y, donee), {}))
        return {"year": y, "donor": donor, "donee": donee, "cls": cls, "amount": amt, "type": t, "rule": rule}
    return [one(e) for e in edges]


def variant_transfers(row: dict, by_donor: dict) -> dict:
    """Raw transfers per variant for one sponsor row (tier B from the parent row plus typed edges)."""
    te = by_donor.get((row["dataset_year"], row["bn"]), [])
    pub = fsum((e["type"], e["amount"]) for e in te if e["cls"] == "public_foundation")
    ch = sum(e["amount"] for e in te if e["donee"] == CANADAHELPS)
    priv = sum(e["amount"] for e in te if e["cls"] == "private_foundation")
    extra = lambda types: sum(pub.get(t, 0.0) for t in types if t in TYPES) + (
        ch if "canadahelps" in types else 0.0) + (priv if "private_foundation" in types else 0.0)
    return {v: row["transfers_tier_b"] + extra(types) for v, types in VARIANTS.items()}


def payout_block(rows: list[dict], tr: dict) -> dict:
    """Aggregate / median / share < 5% on prior-year DAF assets for each variant (matched sponsors)."""
    m = [r for r in rows if r["prior_daf_assets_5862"]]
    pos = [r for r in m if r["prior_daf_assets_5862"] > 0]
    base = sum(r["prior_daf_assets_5862"] for r in m)
    gross = sum(z(r["daf_disbursements_5864"]) for r in m)
    net = lambda r, v: z(r["daf_disbursements_5864"]) - min(max(tr[(r["dataset_year"], r["bn"])][v], 0.0),
                                                            z(r["daf_disbursements_5864"]))

    def per(v):
        nets = [net(r, v) / r["prior_daf_assets_5862"] for r in pos]
        return {"payout_net": panel.ratio(sum(net(r, v) for r in m), base),
                "transfers_capped": gross - sum(net(r, v) for r in m),
                "median_net": median(nets),
                "share_lt_5pct": (sum(1 for x in nets if x < 0.05) / len(nets)) if nets else None}
    return {"n": len(m), "prior_assets": base, "gross_5864": gross, "payout_gross": panel.ratio(gross, base),
            **{v: per(v) for v in VARIANTS}}


# ---------- (03) Schedule 8 coverage ----------
def sched8_gap(y: int, fin: list[dict], abc: dict, ident: dict, dq_keys: set, qd_keys: set,
               panel_y: dict, net_b: dict) -> tuple[dict, list[dict]]:
    dq_bns = {k[0] for k in dq_keys}
    big = [r for r in fin if z(panel.num(r.get("5900"))) > 1_000_000]
    has8 = lambda r: (r["BN"], r["FPE"]) in dq_keys
    miss = [r for r in big if not has8(r)]
    a = lambda r: abc.get((r["BN"], r["FPE"]), {})
    count = lambda rs, key: fsum((key(r), 1) for r in rs)
    rate_by = lambda key: {k: {"returns": v, "no_sched8": count(miss, key).get(k, 0),
                               "share_missing": count(miss, key).get(k, 0) / v}
                           for k, v in sorted(count(big, key).items())}
    all_x = [(a(r).get("5850", "") or "blank", has8(r)) for r in fin]
    s = {
        "year": y, "v27_returns": sum(1 for r in fin if r.get("Form ID", "").strip() == "27"),
        "returns_all_form_ids": count(fin, lambda r: r.get("Form ID", "").strip()),
        "returns_5900_gt_1m": len(big), "no_sched8": len(miss),
        "no_sched8_any_fpe_of_bn": sum(1 for r in miss if r["BN"] not in dq_bns),
        "share_missing": len(miss) / len(big) if big else None,
        "by_form_id": rate_by(lambda r: r.get("Form ID", "").strip()),
        "by_fpe_month": rate_by(lambda r: r["FPE"][:7]),
        "by_fpe_quarter": rate_by(lambda r: fpe_quarter(r["FPE"])),
        "by_line_5850": rate_by(lambda r: a(r).get("5850", "") or "blank"),
        "by_designation": rate_by(lambda r: ident.get(r["BN"], {}).get("Designation", "") or "?"),
        "by_section_used": rate_by(lambda r: r.get("Section Used", "")),
        "by_5860": rate_by(lambda r: a(r).get("5860", "") or "blank"),
        "no_sched8_with_t1236_rows": sum(1 for r in miss if (r["BN"], r["FPE"]) in qd_keys),
        "all_returns_5850_x_sched8": {f"{k}|{'s8' if h else 'no_s8'}": v for (k, h), v in
                                      sorted(fsum(((k, h), 1) for k, h in all_x).items())},
        "sched8_rows": len(dq_keys),
        "no_sched8_5900_total": sum(z(panel.num(r.get("5900"))) for r in miss),
    }

    def detail(r):
        p = panel_y.get(r["BN"])
        f = lambda k: panel.num(r.get(k))
        base = f("5900")
        dqv = ndq.dq_formula(base)
        spend = ndq.sum_present([f("5000"), f("5045"), f("5050")])
        dis = z(p["daf_disbursements_5864"]) if p else 0.0
        i = ident.get(r["BN"], {})
        return {"section": "no_sched8_return", "dataset_year": y, "bn": r["BN"], "legal_name": i.get("Legal Name", ""),
                "designation": i.get("Designation", ""), "category_code": i.get("Category", ""),
                "sub_category_code": i.get("Sub Category", ""), "fpe": r["FPE"], "form_id": r.get("Form ID", ""),
                "fpe_quarter": fpe_quarter(r["FPE"]), "line_5850": a(r).get("5850", ""), "line_5900": base,
                "own_5860": a(r).get("5860", ""), "has_t1236": (r["BN"], r["FPE"]) in qd_keys,
                "panel_sponsor": p is not None,
                "daf_assets_5862": p["daf_assets_5862"] if p else None,
                "daf_disbursements_5864": p["daf_disbursements_5864"] if p else None,
                "imputed_dq_from_5900": dqv, "sched6_spending": spend,
                "imputed_route": dq_route(dqv, dis, net_b.get(r["BN"], dis), spend) if p else ""}
    return s, [detail(r) for r in sorted(miss, key=lambda r: -z(panel.num(r.get("5900"))))]


# ---------- (04) CanadaHelps ----------
def ch_scenarios(y: int, rows: list[dict], fin_y: dict, fin_prev: dict, abc_y: dict, ch_tb: float) -> dict:
    """Panel aggregates with and without CanadaHelps as a sponsor (5862 proxies: designated cash; line 4200)."""
    yr = [r for r in rows if r["dataset_year"] == y]
    ch = fin_y.get(CANADAHELPS, {})
    chp = fin_prev.get(CANADAHELPS, {})
    gifts = panel.num(ch.get("5050"))
    fpe, fpe_p = ch.get("FPE", ""), chp.get("FPE", "")
    proxies = {"designated_cash": (CH_DESIGNATED_CASH.get(fpe), CH_DESIGNATED_CASH.get(fpe_p)),
               "total_assets_4200": (panel.num(ch.get("4200")), panel.num(chp.get("4200")))}
    same = lambda a, d: panel.ratio(d, a)
    tot_a = sum(z(r["daf_assets_5862"]) for r in yr)
    tot_d = sum(z(r["daf_disbursements_5864"]) for r in yr)
    m = [r for r in yr if r["prior_daf_assets_5862"]]
    base = sum(r["prior_daf_assets_5862"] for r in m)
    gross = sum(z(r["daf_disbursements_5864"]) for r in m)
    net_b = sum(r["net_5864_tier_b"] for r in m)
    ch_net_b = z(gifts) - min(ch_tb, z(gifts))
    rank_by = lambda vals, v: 1 + sum(1 for x in vals if x > v)

    def scen(cur, prev):
        return {"ch_5862_proxy": cur, "ch_prior_5862_proxy": prev, "ch_5864_proxy": gifts,
                "ch_payout_same_year": same(cur, gifts), "ch_payout_prior": same(prev, gifts),
                "panel_assets": tot_a + z(cur), "panel_5864": tot_d + z(gifts),
                "aggregate_same_year": same(tot_a + z(cur), tot_d + z(gifts)),
                "aggregate_prior_matched": same(base + z(prev), gross + z(gifts)) if prev else None,
                "ch_tier_b_transfers": ch_tb, "ch_net_5864_tier_b": ch_net_b,
                "aggregate_prior_matched_net_tier_b": same(base + z(prev), net_b + ch_net_b) if prev else None,
                "ch_rank_by_5862": rank_by([z(r["daf_assets_5862"]) for r in yr], z(cur)),
                "ch_rank_by_5864": rank_by([z(r["daf_disbursements_5864"]) for r in yr], z(gifts)),
                "ch_share_of_panel_5864": panel.ratio(z(gifts), tot_d + z(gifts))}
    return {"year": y, "ch_fpe": fpe, "ch_form_id": ch.get("Form ID", ""),
            "ch_5860": abc_y.get(CANADAHELPS, {}).get("5860", ""), "ch_5850": abc_y.get(CANADAHELPS, {}).get("5850", ""),
            "ch_4700": panel.num(ch.get("4700")), "ch_5050": gifts, "ch_4200": panel.num(ch.get("4200")),
            "ch_5900": panel.num(ch.get("5900")),
            "baseline": {"n": len(yr), "assets": tot_a, "disb_5864": tot_d, "aggregate_same_year": same(tot_a, tot_d),
                         "n_matched": len(m), "aggregate_prior_matched": same(base, gross),
                         "aggregate_prior_matched_net_tier_b": same(base, net_b)},
            **{k: scen(*v) for k, v in proxies.items()}}


# ---------- CSV rows ----------
def donee_rows(tedges: list[dict], cats: dict, profiles: dict) -> list[dict]:
    pub = [e for e in tedges if e["cls"] == "public_foundation"]
    tot = fsum((e["year"], e["amount"]) for e in pub)
    keyed = fsum(((e["year"], e["donee"]), e["amount"]) for e in pub)
    donors = {k: {e["donor"] for e in v} for k, v in ndq.group_by(pub, lambda e: (e["year"], e["donee"])).items()}
    tmap = {(e["year"], e["donee"]): (e["type"], e["rule"]) for e in pub}

    def one(k, amt):
        y, bn = k
        c = cats.get(bn, ("", "", "", ""))
        p = profiles.get(k, {})
        return {"section": "pf_donee", "dataset_year": y, "bn": bn, "legal_name": c[2], "designation": c[3],
                "category_code": c[0], "sub_category_code": c[1], "donee_type": tmap[k][0], "type_rule": tmap[k][1],
                "received_from_sponsors": amt, "n_sponsor_donors": len(donors[k]),
                "share_of_public_fdn_gifts": panel.ratio(amt, tot[y]),
                "own_revenue_4700": p.get("revenue_4700"), "own_gifts_5050": p.get("gifts_5050"),
                "own_total_assets_4200": p.get("assets_4200"), "own_t1236_rows": p.get("t1236_rows"),
                "own_pass_through": p.get("pass_through"), "own_share_to_health": p.get("share_gifts_to_health"),
                "own_share_to_univ": p.get("share_gifts_to_univ"), "own_5860": p.get("own_5860")}
    return [one(k, v) for k, v in sorted(keyed.items(), key=lambda kv: (kv[0][0], -kv[1]))]


def tier_rows(blocks: dict) -> list[dict]:
    return [{"section": "tier_payout", "dataset_year": y, "population": pop, "variant": v, "n_sponsors": b["n"],
             "prior_daf_assets": b["prior_assets"], "gross_5864": b["gross_5864"], "payout_gross": b["payout_gross"],
             **b[v]}
            for (y, pop), b in sorted(blocks.items()) for v in VARIANTS]


def ch_rows(sc: list[dict]) -> list[dict]:
    flat = lambda s, p: [{"section": "canadahelps", "dataset_year": s["year"], "bn": CANADAHELPS, "fpe": s["ch_fpe"],
                          "scenario": p, "note": k, "value": v}
                         for k, v in (s[p].items() if p != "baseline" else s["baseline"].items())]
    return [r for s in sc for p in ("baseline", "designated_cash", "total_assets_4200") for r in flat(s, p)]


# ---------- I/O ----------
def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", help="repo root ('.')")
    ap.add_argument("--data-dir", required=True, help="panel inputs (abc, ident, fin for 2023-2025)")
    ap.add_argument("--extra-dir", required=True, help="qd and dq files for 2024-2025")
    ap.add_argument("--out", default="data/mission-2026-11-14/canada-followups-2026-11-19.csv")
    ap.add_argument("--summary", default=None)
    ap.add_argument("--check-parent", default=None, help="parent CSV to compare the rebuilt sponsor rows with")
    a = ap.parse_args(argv)

    # Rebuild the parent's sponsor rows and edges exactly as mission_canada_netting_dq.main() does.
    panel_rows = panel.enrich([r for y in panel.YEARS for r in panel.load_year(a.data_dir, y)])
    keys = {(r["bn"], r["fpe"]) for r in panel_rows if r["dataset_year"] in YEARS}
    bns = {k[0] for k in keys}
    fin_raw = {y: panel.read_csv(panel.find(a.data_dir, y, "fin")) for y in YEARS}
    qd_raw = {y: panel.read_csv(panel.find(a.extra_dir, y, "qd")) for y in YEARS}
    dq_raw = {y: panel.read_csv(panel.find(a.extra_dir, y, "dq")) for y in YEARS}
    abc_raw = {y: panel.read_csv(panel.find(a.data_dir, y, "abc")) for y in YEARS}
    ident_raw = {y: panel.read_csv(panel.find(a.data_dir, y, "ident")) for y in panel.YEARS}

    fin = {(r["BN"], r["FPE"]): r for y in YEARS for r in fin_raw[y] if (r["BN"], r["FPE"]) in keys}
    qd = ndq.group_by((r for y in YEARS for r in qd_raw[y] if (r["BN"], r["FPE"]) in keys),
                      lambda r: (r["BN"], r["FPE"]))
    dq_all = [dict(r, _year=y) for y in YEARS for r in dq_raw[y] if r["BN"] in bns]
    dq_by_key = {(r["BN"], r["FPE"]): r for r in dq_all}
    dq_by_bn_year = reduce(lambda acc, r: {**acc, (r["BN"], r["_year"]): r}
                           if (r["BN"], r["_year"]) not in acc or r["FPE"] > acc[(r["BN"], r["_year"])]["FPE"] else acc,
                           dq_all, {})
    reg = ndq.ident_registry(a.data_dir)
    rows, edges = ndq.build(panel_rows, fin, qd, dq_by_key, dq_by_bn_year, reg)

    parent_check = None
    if a.check_parent:
        with open(a.check_parent, encoding="utf-8", newline="") as fh:
            parent = list(csv.DictReader(fh))
        mine = ndq.to_csv_rows(rows)
        parent_check = {"rows_parent": len(parent), "rows_rebuilt": len(mine),
                        "identical": [dict(r) for r in parent] == mine}

    # registries for donee typing
    cats = {r["BN"]: (r.get("Category", ""), r.get("Sub Category", ""), r.get("Legal Name", ""),
                      r.get("Designation", "")) for y in panel.YEARS for r in ident_raw[y]}
    fin_by_year = {y: latest(fin_raw[y]) for y in YEARS}
    abc_by_year = {y: latest(abc_raw[y]) for y in YEARS}
    qd_rows_by_year = {y: fsum((r["BN"], 1) for r in qd_raw[y]) for y in YEARS}
    base_prof = donee_profiles(fin_by_year, abc_by_year, qd_rows_by_year)
    wanted = {(e[0], e[2]) for e in edges if e[3] == "public_foundation"}
    shares = recipient_shares(qd_raw, wanted, cats)
    profiles = {k: {**v, **shares.get(k, {})} for k, v in base_prof.items()}

    tedges = typed_edges(edges, cats, profiles)
    by_donor = ndq.group_by(tedges, lambda e: (e["year"], e["donor"]))
    tr = {(r["dataset_year"], r["bn"]): variant_transfers(r, by_donor) for r in rows}
    pops = {"all_matched": lambda r: True, "itemised_only": lambda r: r["netting_coverage"] == "itemised",
            "top20": lambda r: r["top20"]}
    blocks = {(y, p): payout_block([r for r in rows if r["dataset_year"] == y and f(r)], tr)
              for y in YEARS for p, f in pops.items()}

    pub = [e for e in tedges if e["cls"] == "public_foundation"]
    type_totals = {y: {t: {"amount": sum(e["amount"] for e in pub if e["year"] == y and e["type"] == t),
                           "donees": len({e["donee"] for e in pub if e["year"] == y and e["type"] == t}),
                           "sponsor_donors": len({e["donor"] for e in pub if e["year"] == y and e["type"] == t})}
                       for t in TYPES} for y in YEARS}
    code_totals = {y: dict(sorted(fsum(("/".join(cats.get(e["donee"], ("?", "?"))[:2]), e["amount"])
                                        for e in pub if e["year"] == y).items(), key=lambda kv: -kv[1])[:12])
                   for y in YEARS}
    type_by_subcode = {y: fsum((f'{e["type"]}|{"/".join(cats.get(e["donee"], ("?", "?"))[:2])}', e["amount"])
                               for e in pub if e["year"] == y) for y in YEARS}
    top_by_type = {y: {t: [{"bn": k, "name": cats.get(k, ("", "", ""))[2], "amount": v}
                           for k, v in sorted(fsum((e["donee"], e["amount"]) for e in pub
                                                   if e["year"] == y and e["type"] == t).items(),
                                              key=lambda kv: -kv[1])[:6]] for t in TYPES} for y in YEARS}

    # (03)
    ident_latest = {y: {r["BN"]: r for r in ident_raw[y]} for y in YEARS}
    gaps = {y: sched8_gap(y, fin_raw[y], {(r["BN"], r["FPE"]): r for r in abc_raw[y]}, ident_latest[y],
                          {(r["BN"], r["FPE"]) for r in dq_raw[y]}, {(r["BN"], r["FPE"]) for r in qd_raw[y]},
                          {r["bn"]: r for r in panel_rows if r["dataset_year"] == y},
                          {r["bn"]: r["net_5864_tier_b"] for r in rows if r["dataset_year"] == y})
            for y in YEARS}
    nos8 = [r for y in YEARS for r in rows if r["dataset_year"] == y and r["route"] == "NO_SCHEDULE8"]
    fin_key = {(r["BN"], r["FPE"]): r for y in YEARS for r in fin_raw[y]}
    abc_key = {(r["BN"], r["FPE"]): r for y in YEARS for r in abc_raw[y]}
    band = lambda v: ("blank" if v is None else "<=25k" if v <= 25_000 else "25k-100k" if v <= 100_000
                      else "100k-1m" if v <= 1_000_000 else ">1m")
    panel_nos8 = {y: {
        "n": sum(1 for r in nos8 if r["dataset_year"] == y),
        "daf_assets": sum(z(r["daf_assets_5862"]) for r in nos8 if r["dataset_year"] == y),
        "by_5850_and_5900_band": fsum((f'{abc_key.get((r["bn"], r["fpe"]), {}).get("5850", "") or "blank"}|'
                                       f'{band(panel.num(fin_key.get((r["bn"], r["fpe"]), {}).get("5900")))}', 1)
                                      for r in nos8 if r["dataset_year"] == y),
        "daf_assets_by_5850": fsum((abc_key.get((r["bn"], r["fpe"]), {}).get("5850", "") or "blank",
                                    z(r["daf_assets_5862"])) for r in nos8 if r["dataset_year"] == y),
        "daf_assets_above_5850_threshold": {
            k: {"n": len(v), "daf_assets": sum(z(r["daf_assets_5862"]) for r in v)} for k, v in ndq.group_by(
                [r for r in nos8 if r["dataset_year"] == y
                 and z(r["daf_assets_5862"]) > (100_000 if r["designation"] == "C" else 25_000)],
                lambda r: abc_key.get((r["bn"], r["fpe"]), {}).get("5850", "") or "blank").items()},
        "imputed_routes_5900_gt_1m": fsum((d["imputed_route"], 1) for d in gaps[y][1] if d["panel_sponsor"]),
        "imputed_routes_daf_assets": fsum((d["imputed_route"], z(d["daf_assets_5862"])) for d in gaps[y][1]
                                          if d["panel_sponsor"]),
        "largest": [{k: d[k] for k in ("bn", "legal_name", "designation", "fpe", "line_5850", "line_5900",
                                       "daf_assets_5862", "daf_disbursements_5864", "imputed_dq_from_5900",
                                       "sched6_spending", "imputed_route")}
                    for d in sorted((d for d in gaps[y][1] if d["panel_sponsor"]),
                                    key=lambda d: -z(d["daf_assets_5862"]))[:12]],
    } for y in YEARS}

    # (04)
    ch_edges = {y: {"from_sponsors": sum(e["amount"] for e in tedges if e["year"] == y and e["donee"] == CANADAHELPS),
                    "n_sponsor_donors": len({e["donor"] for e in tedges if e["year"] == y and e["donee"] == CANADAHELPS}),
                    "top": [{"donor": k, "name": cats.get(k, ("", "", ""))[2], "amount": v}
                            for k, v in sorted(fsum((e["donor"], e["amount"]) for e in tedges
                                                    if e["year"] == y and e["donee"] == CANADAHELPS).items(),
                                               key=lambda kv: -kv[1])[:8]]} for y in YEARS}
    sponsors = ndq.sponsor_map(panel_rows)
    ch_own = {y: {k: v for k, v in ndq.gifts_for([r for r in qd_raw[y] if r["BN"] == CANADAHELPS], reg, sponsors,
                                                 CANADAHELPS).items() if not k.startswith("_")} for y in YEARS}
    ch_sc = [ch_scenarios(y, rows, fin_by_year[y], fin_by_year.get(y - 1) or latest(panel.read_csv(
        panel.find(a.data_dir, y - 1, "fin"))), abc_by_year[y],
                          ch_own[y]["gifts_sponsor_daf_primary"] + ch_own[y]["gifts_sponsor_other"]) for y in YEARS]

    out_rows = (donee_rows(tedges, cats, profiles) + tier_rows(blocks)
                + [d for y in YEARS for d in gaps[y][1]] + ch_rows(ch_sc))
    with open(os.path.join(a.root, a.out), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows({k: panel.fmt(r.get(k)) for k in FIELDS} for r in out_rows)

    summary = {
        "parent_check": parent_check,
        "csv_rows_by_section": fsum((r["section"], 1) for r in out_rows),
        "p01_public_fdn_by_type": type_totals, "p01_public_fdn_by_category_code": code_totals,
        "p01_type_by_subcode": type_by_subcode, "p01_top_by_type": top_by_type,
        "p01_payout_by_variant": {f"{y}|{p}": b for (y, p), b in blocks.items()},
        "p03_sched8_gap": {y: gaps[y][0] for y in YEARS}, "p03_panel_no_sched8": panel_nos8,
        "p04_canadahelps_received": ch_edges, "p04_canadahelps_own_gifts": ch_own, "p04_canadahelps_scenarios": ch_sc,
    }
    text = json.dumps(summary, indent=1, default=str)
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
