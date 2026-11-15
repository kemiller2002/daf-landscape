#!/usr/bin/env python3
"""DAF-to-DAF netting rule R5 for the corrected DAFRC market totals, FY2021-FY2024 (queue items P-B33A-01, P-NPO-04).

Stdlib only; functional style (pure transforms, I/O at the edges). No new parsing: the script transforms
  * the Schedule I extracts cached by scripts/mission_net_payout.py (CACHE/netpayout990/{oid}.json: every Schedule I
    Part II line whose recipient is a DAFRC panel EIN, with cash, non-cash and purpose text);
  * data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv (DAFRC 2025 panel) and
    data/mission-2026-11-14/dafrc-corrections-itemized.csv (rules R1-R4) -> corrected sponsor-year values, which are
    checked against data/mission-2026-11-14/dafrc-corrected-market-totals.csv;
  * data/mission-2026-11-14/sponsor-cost-structure.csv (filed DAF share of total assets and of grants, FY2022-25).

Why R5. A transfer from sponsor A's DAF to sponsor B's DAF is counted in A's Schedule D Part I grants and in B's
Part I contributions. Summing the panel therefore counts it as market grants and as market contributions although
no money left the DAF system. R5 subtracts the same amount N from both aggregates.

Recipient whitelist (P-NPO-04), one decision per recipient EIN (data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv)
  W1 university/hospital sponsor (DAFRC subtype 'Universities and Healthcare')         -> exclude (programme grants)
  W2 national (Standard) or donation processor, DAF share of total assets >= 0.50 or
     no cost-structure row                                                              -> include
     ... DAF share < 0.50 (fiscal sponsors, crowdfunding, microlending)                 -> exclude
  W3 community foundation                                                               -> include, weighted by its
                                                                                           DAF share of total assets
  W4 single-issue or religious sponsor, DAF share of total assets >= 0.50              -> include
     ... DAF share < 0.50 or no cost-structure row                                      -> exclude
  W5 reviewed affiliate pairs (same sponsor family filing separately)                   -> pair excluded from the
                                                                                           lower and central tiers
  DAF share = median of the recipient's filed Schedule D Part I EOY value / Part X total assets over FY2022-25.

Netting tiers (each line is weighted, then capped)
  lower    lines to W2 recipients only, weight = grantor DAF share of grants (Sched D grants / Part IX grants)
  central  lines to every whitelisted recipient, weight = grantor DAF share of grants x recipient DAF share of assets
  upper    lines to every whitelisted recipient plus W5 affiliate pairs, weight = 1
  Cap: per grantor-year the weighted lines cannot exceed its corrected DAF grants; per recipient-year they cannot
  exceed its corrected DAF contributions (line scale = min(1, grants/sum, contributions/sum)). The same capped
  amount is subtracted from grants and from contributions.
  Only grantor-years and recipient-years present in the corrected market (positive corrected grants / contributions)
  are netted. Fiscal year = calendar year in which the tax period ends (DAFRC convention) on both sides.

Usage:
  python3 scripts/mission_market_netting.py --np-cache NPCACHE   # NPCACHE holds netpayout990/
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
from typing import Callable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import load_np, pick_returns  # noqa: E402
from mission_net_payout import itemized, panel_from  # noqa: E402

FYS = (2021, 2022, 2023, 2024)
CORR_ITEMS = os.path.join(DATA, "dafrc-corrections-itemized.csv")
CORR_TOTALS = os.path.join(DATA, "dafrc-corrected-market-totals.csv")
COST = os.path.join(DATA, "sponsor-cost-structure.csv")
OUT_TOTALS = os.path.join(DATA, "dafrc-market-totals-netted.csv")
OUT_WL = os.path.join(DATA, "daf-to-daf-recipient-whitelist.csv")
SHARE_MIN = 0.5
TIERS = ("lower", "central", "upper")
METRIC_COL = {"daf_grants": "total_daf_grants", "daf_contributions": "total_daf_contributions"}

# W5: reviewed affiliate pairs (unordered). Same family filing separate returns; evidence in the batch-34 report.
AFFILIATES = {
    frozenset({"260724604", "061676688"}): "Dechomai Asset Trust / Dechomai Foundation (asset-conversion trust feeding the foundation)",
    frozenset({"473574130", "812375745"}): "Impact Investing Charitable Foundation / Impact Investing Charitable Trust (same sponsor family)",
    frozenset({"541934032", "522166327"}): "Donors Capital Fund / Donors Trust (sister organisations, shared management)",
    frozenset({"277059768", "237825575"}): "NPT Charitable Asset Trust / National Philanthropic Trust (supporting organisation, Schedule R)",
    frozenset({"311044298", "316027287"}): "Dayton Foundation Depository / The Dayton Foundation (depository affiliate)",
    frozenset({"223106737", "237250641"}): "Rochester Area Community Foundation (two EINs, same name)",
    frozenset({"431758789", "436023126"}): "St Louis Community Foundation (two EINs, same name)",
    frozenset({"352019497", "356028362"}): "The Portland Foundation (two EINs, same name)",
    frozenset({"141782466", "311774905"}): "Ayco Charitable Foundation / GS DAPF (common control; merged 2025-07-01, Ayco FY6/2025 Schedule O)",
}

DAF_TXT = re.compile(r"\bDAFS?\b|DONOR[- ]?ADVISED|ADVISED FUND|ADVISED -|TRANSFER TO (A |THE )?(DONOR|FUND|DAF)|FUND TRANSFER|"
                     r"SUCCESSOR|FUND CLOSE|'S FUND\b|FAMILY FUND|CHARITABLE FUND\b|GIVING FUND\b|FUND FOR\b", re.I)
NONDAF_TXT = re.compile(r"SCHOLARSHIP|DISASTER|RELIEF|RESPONSE|ENDOWMENT|FIELD OF INTEREST|DESIGNATED|AGENCY|PROJECT|"
                        r"PROGRAM|CAPACITY|INITIATIVE|COVID|EMERGENCY|CAMPAIGN|EVENT|SPONSORSHIP|MATCH|OPERATING|"
                        r"RACIAL|EQUITY|HOUSING|HEALTH|ARTS|EDUCATION|YOUTH|CHILDREN", re.I)
SOURCE = ("IRS Form 990 Schedule I Part II lines (e-file XML, GivingTuesday mirror of IRS TEOS) cached by "
          "scripts/mission_net_payout.py; DAFRC 2025 panel + rules R1-R4 (dafrc-corrections-itemized.csv); "
          "sponsor-cost-structure.csv")


# ----------------------------------------------------------------------------- pure helpers
def amt(l: Mapping) -> float:
    return (l.get("cash") or 0.0) + (l.get("noncash") or 0.0)


def clip01(x: float | None) -> float | None:
    return None if x is None else min(max(x, 0.0), 1.0)


def med(xs: Sequence[float]) -> float | None:
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


def corrected_values(dafrc: Sequence[Mapping], items: Sequence[Mapping]) -> dict:
    """(ein, fy, metric) -> corrected value: DAFRC as published, overridden by applied R1-R4 rows."""
    base = {(ein9(r["ein"]), int(r["fiscal_year_end"]), m): num(r[c]) or 0.0
            for r in dafrc for m, c in METRIC_COL.items()}
    over = {(ein9(r["ein"]), int(r["fiscal_year"]), r["metric"]): num(r["corrected_value"]) or 0.0
            for r in items if r["applied"] == "1" and r["metric"] in METRIC_COL}
    return {**base, **over}


def cost_shares(rows: Sequence[Mapping]) -> dict:
    """ein -> {'assets': median DAF share of total assets, 'grants': median DAF share of grants, 'fys': ...}."""
    by = _group_by_fast(rows, lambda r: ein9(r["ein"]))
    return {e: {"assets": med([num(r["daf_share_of_total_assets"]) for r in rs]),
                "grants": med([num(r["daf_share_of_grants"]) for r in rs]),
                "fys": ";".join(sorted({r["fiscal_year"] for r in rs}))} for e, rs in by.items()}


def purpose_class(text: str) -> str:
    t = text or ""
    return "explicit_daf" if DAF_TXT.search(t) else ("explicit_non_daf" if NONDAF_TXT.search(t) else "generic")


def affiliate(a: str, b: str) -> str:
    return AFFILIATES.get(frozenset({a, b}), "")


def recipient_decision(p: Mapping, share: Mapping | None) -> tuple[str, str, str]:
    """(decision, rule, reason) for one recipient EIN."""
    seg, s = p["segment"], (share or {}).get("assets")
    if seg == "university_hospital":
        return "exclude", "W1", "university/hospital sponsor: Schedule I lines are programme grants"
    if seg in ("national", "processor"):
        if s is None:
            return "include", "W2", "national/processor, no cost-structure row (kept by segment)"
        return (("include", "W2", f"national/processor, DAF share of assets {s:.2f} >= {SHARE_MIN}") if s >= SHARE_MIN
                else ("exclude", "W2", f"national/processor but DAF share of assets {s:.2f} < {SHARE_MIN} (fiscal sponsor / processor inflows)"))
    if seg == "community_foundation":
        return "include", "W3", "community foundation: weighted by DAF share of assets in the central tier"
    if s is None:
        return "exclude", "W4", "single-issue/religious, no cost-structure row"
    return (("include", "W4", f"single-issue/religious, DAF share of assets {s:.2f} >= {SHARE_MIN}") if s >= SHARE_MIN
            else ("exclude", "W4", f"single-issue/religious, DAF share of assets {s:.2f} < {SHARE_MIN}: programme grants"))


def panel_lines(chosen: Mapping, panel: Mapping) -> tuple[dict, ...]:
    """Every Schedule I line from a panel grantor-year (FY2021-24) to another panel EIN."""
    return tuple({"grantor": g, "recipient": l["matched_ein"], "fy": fy, "amount": amt(l), "purpose": l.get("purpose") or "",
                  "match_method": l.get("match_method", ""), "oid": ex["oid"]}
                 for (g, fy), ex in chosen.items() if fy in FYS and g in panel
                 for l in ex.get("sched_i_panel_lines", ()) if l["matched_ein"] != g and amt(l) > 0)


def weights(line: Mapping, panel: Mapping, decision: Mapping, shares: Mapping, defaults: Mapping) -> dict:
    g, r = line["grantor"], line["recipient"]
    dec, aff = decision[r][0], affiliate(g, r)
    gs = clip01((shares.get(g) or {}).get("grants"))
    gs = defaults["grants"][panel[g]["segment"]] if gs is None else gs
    rs = clip01((shares.get(r) or {}).get("assets"))
    rs = defaults["assets"][panel[r]["segment"]] if rs is None else rs
    ok = dec == "include"
    return {"lower": gs if ok and not aff and panel[r]["segment"] in ("national", "processor") else 0.0,
            "central": gs * rs if ok and not aff else 0.0,
            "upper": 1.0 if ok or aff else 0.0}


def capped(lines: Sequence[Mapping], tier: str, corr: Mapping) -> tuple[dict, ...]:
    """Apply grantor-year and recipient-year caps to the weighted lines of one tier."""
    w = tuple({**l, "w_amt": l["amount"] * l["w"][tier]} for l in lines
              if l["w"][tier] > 0 and corr.get((l["grantor"], l["fy"], "daf_grants"), 0) > 0
              and corr.get((l["recipient"], l["fy"], "daf_contributions"), 0) > 0)
    gsum = {k: sum(x["w_amt"] for x in v) for k, v in _group_by_fast(w, lambda x: (x["grantor"], x["fy"])).items()}
    rsum = {k: sum(x["w_amt"] for x in v) for k, v in _group_by_fast(w, lambda x: (x["recipient"], x["fy"])).items()}

    def scale(x):
        gk, rk = (x["grantor"], x["fy"]), (x["recipient"], x["fy"])
        return min(1.0, corr[(*gk, "daf_grants")] / gsum[gk] if gsum[gk] else 1.0,
                   corr[(*rk, "daf_contributions")] / rsum[rk] if rsum[rk] else 1.0)
    return tuple({**x, "net_amt": x["w_amt"] * scale(x)} for x in w)


def market_rows(netted: Mapping, corr_tot: Mapping, lines: Sequence[Mapping], chosen: Mapping, panel: Mapping,
                corr: Mapping) -> tuple[dict, ...]:
    def unobserved(fy):  # DAF grants of panel grantor-years whose Schedule I is not itemised or not parsed
        keys = {k for k in corr if k[1] == fy and k[2] == "daf_grants" and corr[k] > 0}
        miss = [corr[k] for k in keys if (k[0], fy) not in chosen]
        attach = [corr[k] for k in keys if (k[0], fy) in chosen and not itemized(chosen[(k[0], fy)])]
        return sum(miss), sum(attach)

    def one(fy, metric, tier):
        xs = [x for x in netted[tier] if x["fy"] == fy]
        n = sum(x["net_amt"] for x in xs)
        cv = corr_tot[(fy, metric)]
        prev = corr_tot.get((fy - 1, metric))
        prev_n = (prev - sum(x["net_amt"] for x in netted[tier] if x["fy"] == fy - 1)) if prev is not None and fy - 1 in FYS else None
        miss, attach = unobserved(fy)
        return {"fiscal_year": fy, "metric": metric, "tier": tier, "corrected_value": round(cv),
                "r5_netting_amount": round(n), "netted_value": round(cv - n), "netting_share_of_corrected": n / cv,
                "weighted_before_caps": round(sum(x["w_amt"] for x in xs)),
                "gross_lines_in_tier": round(sum(x["amount"] for x in xs)), "lines": len(xs),
                "grantors": len({x["grantor"] for x in xs}), "recipients": len({x["recipient"] for x in xs}),
                "yoy_growth_corrected": (cv / prev - 1) if prev else None,
                "yoy_growth_netted": ((cv - n) / prev_n - 1) if prev_n else None,
                "all_panel_lines_gross": round(sum(l["amount"] for l in lines if l["fy"] == fy)),
                "grantor_daf_grants_no_parsed_return": round(miss),
                "grantor_daf_grants_sched_i_not_itemised": round(attach),
                "sources": SOURCE}
    return tuple(one(fy, m, t) for fy in FYS for m in METRIC_COL for t in TIERS)


def whitelist_rows(panel: Mapping, shares: Mapping, decision: Mapping, lines: Sequence[Mapping],
                   netted: Mapping) -> tuple[dict, ...]:
    by_r = _group_by_fast(lines, lambda l: l["recipient"])
    net_r = {t: {k: sum(x["net_amt"] for x in v) for k, v in _group_by_fast(netted[t], lambda x: x["recipient"]).items()}
             for t in TIERS}

    def one(r, ls):
        p, sh = panel[r], shares.get(r) or {}
        dec, rule, why = decision[r]
        affs = sorted({affiliate(l["grantor"], r) for l in ls} - {""})
        pc = _group_by_fast(ls, lambda l: purpose_class(l["purpose"]))
        return {"recipient_ein": r, "recipient_name": p["name"], "dafrc_type": p["type"], "dafrc_subtype": p["subtype"],
                "segment": p["segment"], "daf_share_of_total_assets": sh.get("assets"),
                "daf_share_of_grants": sh.get("grants"), "cost_structure_fys": sh.get("fys", ""),
                "decision": dec, "rule": rule, "reason": why, "affiliate_pairs": " | ".join(affs),
                "inbound_lines_fy2021_2024": len(ls), "inbound_grantors": len({l["grantor"] for l in ls}),
                "inbound_gross_fy2021_2024": round(sum(l["amount"] for l in ls)),
                **{f"inbound_gross_fy{fy}": round(sum(l["amount"] for l in ls if l["fy"] == fy)) for fy in FYS},
                "purpose_explicit_daf_usd": round(sum(l["amount"] for l in pc.get("explicit_daf", ()))),
                "purpose_explicit_non_daf_usd": round(sum(l["amount"] for l in pc.get("explicit_non_daf", ()))),
                **{f"netted_{t}_fy2021_2024": round(net_r[t].get(r, 0.0)) for t in TIERS},
                "source": SOURCE}
    return tuple(sorted((one(r, ls) for r, ls in by_r.items()), key=lambda d: -d["inbound_gross_fy2021_2024"]))


def purpose_audit(lines: Sequence[Mapping], panel: Mapping) -> dict:
    def seg_stats(seg):
        xs = [l for l in lines if panel[l["recipient"]]["segment"] == seg]
        tot = sum(l["amount"] for l in xs)
        by = _group_by_fast(xs, lambda l: purpose_class(l["purpose"]))
        return {"lines": len(xs), "usd": round(tot),
                **{f"share_usd_{k}": (sum(l["amount"] for l in by.get(k, ())) / tot if tot else None)
                   for k in ("explicit_daf", "explicit_non_daf", "generic")},
                **{f"lines_{k}": len(by.get(k, ())) for k in ("explicit_daf", "explicit_non_daf", "generic")}}
    return {s: seg_stats(s) for s in ("national", "processor", "community_foundation", "single_issue", "university_hospital")}


FIELDS_T = ("fiscal_year", "metric", "tier", "corrected_value", "r5_netting_amount", "netted_value",
            "netting_share_of_corrected", "weighted_before_caps", "gross_lines_in_tier", "lines", "grantors", "recipients",
            "yoy_growth_corrected", "yoy_growth_netted", "all_panel_lines_gross", "grantor_daf_grants_no_parsed_return",
            "grantor_daf_grants_sched_i_not_itemised", "sources")
FIELDS_W = ("recipient_ein", "recipient_name", "dafrc_type", "dafrc_subtype", "segment", "daf_share_of_total_assets",
            "daf_share_of_grants", "cost_structure_fys", "decision", "rule", "reason", "affiliate_pairs",
            "inbound_lines_fy2021_2024", "inbound_grantors", "inbound_gross_fy2021_2024",
            *(f"inbound_gross_fy{fy}" for fy in FYS), "purpose_explicit_daf_usd", "purpose_explicit_non_daf_usd",
            *(f"netted_{t}_fy2021_2024" for t in TIERS), "source")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--np-cache", required=True, help="cache dir holding netpayout990/ (mission_net_payout.py)")
    a = ap.parse_args(argv)
    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    corr = corrected_values(dafrc, read_csv(CORR_ITEMS))
    corr_tot = {(int(r["fiscal_year"]), r["metric"]): float(r["corrected_value"]) for r in read_csv(CORR_TOTALS)
                if r["metric"] in METRIC_COL}
    check = {f"{fy}_{m}": {"rebuilt": round(sum(v for k, v in corr.items() if k[1] == fy and k[2] == m)),
                           "published_corrected": round(corr_tot[(fy, m)])} for fy in FYS for m in METRIC_COL}
    shares = cost_shares(read_csv(COST))
    seg_med: Callable[[str, str], float] = lambda seg, k: med(  # noqa: E731
        [clip01(shares[e][k]) for e in panel if panel[e]["segment"] == seg and e in shares and shares[e][k] is not None]) or 1.0
    defaults = {k: {s: seg_med(s, k) for s in {p["segment"] for p in panel.values()}} for k in ("assets", "grants")}
    chosen = pick_returns(load_np(a.np_cache))
    lines = panel_lines(chosen, panel)
    decision = {r: recipient_decision(panel[r], shares.get(r)) for r in {l["recipient"] for l in lines}}
    wl = tuple({**l, "w": weights(l, panel, decision, shares, defaults)} for l in lines)
    netted = {t: capped(wl, t, corr) for t in TIERS}
    write_csv(OUT_TOTALS, market_rows(netted, corr_tot, lines, chosen, panel, corr), FIELDS_T)
    write_csv(OUT_WL, whitelist_rows(panel, shares, decision, lines, netted), FIELDS_W)
    seg_flow = {t: {fy: {s: round(sum(x["net_amt"] for x in netted[t] if x["fy"] == fy and panel[x["recipient"]]["segment"] == s))
                         for s in ("national", "processor", "community_foundation", "single_issue")} for fy in FYS} for t in TIERS}
    pair_top = sorted(({"grantor": panel[k[0]]["name"], "recipient": panel[k[1]]["name"], "net_central": round(sum(x["net_amt"] for x in v))}
                       for k, v in _group_by_fast(netted["central"], lambda x: (x["grantor"], x["recipient"])).items()),
                      key=lambda d: -d["net_central"])[:15]
    aff_upper = {fy: round(sum(x["net_amt"] for x in netted["upper"] if x["fy"] == fy and affiliate(x["grantor"], x["recipient"]))) for fy in FYS}
    print(json.dumps({"corrected_totals_rebuild_check": check, "grantor_returns_by_fy": {fy: sum(1 for k in chosen if k[1] == fy) for fy in FYS},
                      "panel_lines": len(lines), "recipients": len(decision),
                      "decisions": {d: sum(1 for v in decision.values() if v[0] == d) for d in ("include", "exclude")},
                      "decisions_by_rule": {f"{r}_{d}": sum(1 for v in decision.values() if v[1] == r and v[0] == d)
                                            for r in ("W1", "W2", "W3", "W4") for d in ("include", "exclude")},
                      "segment_default_shares": defaults, "purpose_audit_fy2021_2024": purpose_audit(lines, panel),
                      "netted_by_recipient_segment": seg_flow, "affiliate_pairs_in_upper": aff_upper,
                      "top_pairs_central_fy2021_2024": pair_top}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
