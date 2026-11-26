#!/usr/bin/env python3
"""Panel-wide Form 990 scans over the parsed-return caches (queue batch 33 A).

Three tasks, each a pure transform of caches that earlier scripts built (no new parsing logic is invented):

  blank_sd     P-B32B-01. Part IV line 6 = Yes but Schedule D Part I DAF count and end-of-year value both blank,
               for DAFRC panel EINs, tax years 2021+. Source cache: CACHE990/extract990/{oid}.json written by
               scripts/mission_990_contractors.py (12,257 returns, full-universe harvest + outside-DAFRC run).
               Each flagged return is matched to the DAFRC row for the same fiscal year (imputed / filed / no row)
               and bracketed by the sponsor's own last and next reported DAF values. The 100 exit candidates of
               data/mission-2026-11-14/sponsor-exit-verification.csv are then re-tested mechanically and the
               verified exit-rate bounds are recomputed net of reporting gaps.
  sweepstakes  P-B32A-01. Schedule G Part I line 2b gross receipts (sweepstakes, charity auctions) of Givinga,
               Pledgeling, CAF America and Our Change against Schedule D DAF contributions, the DAFRC panel and the
               DAFRC market totals. Inputs: data/mission-2026-11-14/schedule-g-screen.csv (P-COST-05 output),
               dafrc-sponsor-schedule-d-fy2019-2024.csv, dafrc-corrected-market-totals.csv.
  lowinc       P-B32A-03. Part VIII line 3 investment income / average total assets for every return in
               sponsor-cost-structure.csv (5,272 returns, FY2022-2025). Line 3, line 7d, Part XI line 5, 11f and
               Schedule D Part XII 4a come from CACHE/extract990inv/{oid}.json, written by
               scripts/mission_infund_costs.py:fetch_inv (reused here; --fetch fills missing extracts).

Definitions
  fiscal year (FY) = calendar year in which the tax period ends (repo convention); tax year (TY) = filed TaxYr.
  line6_yes        = Part IV line 6 DonorAdvisedFundInd in {true, 1}.
  part_i_blank     = DonorAdvisedFundsHeldCnt and DonorAdvisedFundsVlEOYAmt both absent from the XML.

Stdlib only; functional style (pure transforms, I/O at the edges).

Usage:
  python3 scripts/mission_panel_scans.py --task all --extract990-dir CACHE990/extract990 \
      --inv-cache CACHE [--fetch] [--workers 16]
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DATA, DAFRC_CSV, XML_URL, _group_by_fast, ein9, fmt, num, read_csv, write_csv  # noqa: E402

COST_CSV = os.path.join(DATA, "sponsor-cost-structure.csv")
SCHED_G_CSV = os.path.join(DATA, "schedule-g-screen.csv")
MARKET_CSV = os.path.join(DATA, "dafrc-corrected-market-totals.csv")
VERIFY_CSV = os.path.join(DATA, "sponsor-exit-verification.csv")
TIERB_CSV = os.path.join(DATA, "tier-b-daf-exit-reasons.csv")
OUT_BLANK = os.path.join(DATA, "blank-schedule-d-panel.csv")
OUT_SWEEP = os.path.join(DATA, "sweepstakes-receipts-dafrc-share.csv")
OUT_LOWINC = os.path.join(DATA, "low-investment-income-screen.csv")
DAFRC_URL = "https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx"
MIN_TY = 2021
EXPOSURE_SPONSOR_YEARS = 5746          # sponsor-mortality-summary.csv, verified rows (FY2019-FY2022 at risk)
LOWINC_BPS = 50.0
LOWINC_MIN_AVG_ASSETS = 1_000_000
FOCUS_MIN_DAF_ASSETS = 10_000_000
FOCUS_MIN_DAF_SHARE = 0.5
PLATFORM_EINS = {"474172718": "Givinga Foundation", "462440594": "Pledgeling Foundation",
                 "431634280": "Charities Aid Foundation America", "863353394": "Our Change Foundation"}


def yes(v) -> bool:
    return str(v).strip().lower() in ("true", "1")


def fy_of(period_end: str) -> int | None:
    return int(period_end[:4]) if period_end and period_end[:4].isdigit() else None


def ratio(a, b):
    return a / b if a is not None and b else None


# ----------------------------------------------------------------------------- loaders (I/O)
def load_extract_dir(path: str) -> tuple[dict, ...]:
    def one(f):
        with open(os.path.join(path, f), encoding="utf-8") as fh:
            return {**json.load(fh), "oid": f[:-5]}
    return tuple(one(f) for f in sorted(os.listdir(path)) if f.endswith(".json"))


def dafrc_index(rows: Sequence[Mapping]) -> tuple[dict, dict]:
    by_key = {(ein9(r["ein"]), int(r["fiscal_year_end"])): r for r in rows}
    by_ein = _group_by_fast(rows, lambda r: ein9(r["ein"]))
    return by_key, {e: sorted(v, key=lambda r: int(r["fiscal_year_end"])) for e, v in by_ein.items()}


# ----------------------------------------------------------------------------- task blank_sd (P-B32B-01)
def normalise_return(x: Mapping) -> dict:
    pe = x.get("tax_period_end") or ""
    return {"oid": x["oid"], "ein": ein9(x.get("filer_ein") or ""), "filer_name": x.get("filer_name") or "",
            "tax_year": int(x["tax_year"]) if str(x.get("tax_year") or "").isdigit() else None,
            "tax_period_end": pe, "fy": fy_of(pe), "line6_raw": x.get("daf_ind_part_iv"),
            "line6_yes": yes(x.get("daf_ind_part_iv")), "sched_d_present": x.get("sched_d_present"),
            "daf_count": x.get("sched_d_daf_count"), "daf_eoy": x.get("sched_d_daf_eoy_value"),
            "daf_contrib": x.get("sched_d_daf_contributions"), "daf_grants": x.get("sched_d_daf_grants"),
            "other_count": x.get("sched_d_other_funds_count"), "other_eoy": x.get("sched_d_other_funds_eoy_value"),
            "total_assets_eoy": x.get("total_assets_eoy"), "amended": x.get("amended_ind") or "",
            "return_ts": (x.get("return_ts") or "")[:10], "xml_url": x.get("xml_url") or XML_URL.format(oid=x["oid"])}


def latest_per_period(rets: Sequence[Mapping]) -> tuple[dict, ...]:
    """One return per (EIN, tax period end): the highest object id (amended or later submission supersedes)."""
    by = _group_by_fast(rets, lambda r: (r["ein"], r["tax_period_end"]))
    return tuple(max(v, key=lambda r: r["oid"]) for v in by.values())


def part_i_blank(r: Mapping) -> bool:
    return r["daf_count"] is None and r["daf_eoy"] is None


def blank_kind(r: Mapping) -> str:
    if not r["sched_d_present"]:
        return "no_schedule_d"
    if (r["other_count"] or 0) > 0 or (r["other_eoy"] or 0) > 0:
        return "other_funds_column_only"
    if r["daf_contrib"] is not None or r["daf_grants"] is not None:
        return "count_and_value_blank_flows_reported"
    return "part_i_daf_column_blank"


def reported(r: Mapping) -> bool:
    return r["daf_eoy"] is not None or r["daf_count"] is not None


def dafrc_treatment(fy: int | None, row: Mapping | None, ein_rows: Sequence[Mapping]) -> str:
    if fy is None:
        return "no_fiscal_year"
    if fy > 2024:
        return "outside_dafrc_window_fy2025plus"
    if row is None:
        last = ein_rows[-1] if ein_rows else None
        if last and "Closed" in last["operating_status"]:
            return "dafrc_no_row_sponsor_closed"
        return "dafrc_no_row_other"
    if row["source_eoy_daf_assets"] == "Imputed":
        return "dafrc_row_imputed"
    if row["eoy_daf_assets"] == "":
        return "dafrc_row_value_blank"
    return "dafrc_row_filed_value"


def blank_rows(rets: Sequence[Mapping], dafrc_rows: Sequence[Mapping]) -> tuple[dict, ...]:
    by_key, by_ein = dafrc_index(dafrc_rows)
    panel = frozenset(by_ein)
    by_sponsor = {e: sorted(v, key=lambda r: r["tax_period_end"]) for e, v in _group_by_fast(rets, lambda r: r["ein"]).items()}

    def one(r):
        hist = by_sponsor[r["ein"]]
        prior = [h for h in hist if h["tax_period_end"] < r["tax_period_end"] and reported(h)]
        later = [h for h in hist if h["tax_period_end"] > r["tax_period_end"]]
        nxt = next((h for h in later if reported(h)), None)
        pv = prior[-1] if prior else None
        drow = by_key.get((r["ein"], r["fy"]))
        ein_rows = by_ein.get(r["ein"], [])
        treat = dafrc_treatment(r["fy"], drow, ein_rows)
        lf = [d for d in ein_rows if int(d["fiscal_year_end"]) < (r["fy"] or 0) and d["source_eoy_daf_assets"] != "Imputed"
              and d["eoy_daf_assets"] != ""]
        lfv = num(lf[-1]["eoy_daf_assets"]) if lf else None
        base = pv["daf_eoy"] if pv and pv["daf_eoy"] is not None else lfv
        missing_cf = (base or 0) if treat in ("dafrc_no_row_sponsor_closed", "dafrc_row_value_blank", "dafrc_no_row_other") else 0
        later_line6 = ";".join(f"{h['tax_period_end'][:7]}:{'Y' if h['line6_yes'] else 'N'}{'' if not h['line6_yes'] else ('b' if part_i_blank(h) else 'v')}"
                               for h in later)
        name = (ein_rows[-1]["name"] if ein_rows else r["filer_name"])
        return {"ein": r["ein"], "sponsor_name": name, "dafrc_type": ein_rows[-1]["type"] if ein_rows else "",
                "dafrc_subtype": ein_rows[-1]["subtype"] if ein_rows else "",
                "dafrc_last_operating_status": ein_rows[-1]["operating_status"] if ein_rows else "",
                "tax_year": r["tax_year"], "fiscal_year": r["fy"], "tax_period_end": r["tax_period_end"],
                "line6_raw": r["line6_raw"], "blank_kind": blank_kind(r),
                "daf_contributions_filed": r["daf_contrib"], "daf_grants_filed": r["daf_grants"],
                "other_funds_count": r["other_count"], "other_funds_eoy_value": r["other_eoy"],
                "total_assets_eoy": r["total_assets_eoy"],
                "dafrc_treatment": treat,
                "dafrc_eoy_daf_assets_same_fy": num(drow["eoy_daf_assets"]) if drow else None,
                "dafrc_accounts_same_fy": num(drow["number_of_daf_accounts"]) if drow else None,
                "dafrc_source_same_fy": drow["source_eoy_daf_assets"] if drow else "",
                "prior_reported_period": pv["tax_period_end"] if pv else "",
                "prior_reported_daf_count": pv["daf_count"] if pv else None,
                "prior_reported_daf_eoy": pv["daf_eoy"] if pv else None,
                "dafrc_last_filed_fy_before": int(lf[-1]["fiscal_year_end"]) if lf else None,
                "dafrc_last_filed_daf_assets_before": lfv,
                "next_reported_period": nxt["tax_period_end"] if nxt else "",
                "next_reported_daf_count": nxt["daf_count"] if nxt else None,
                "next_reported_daf_eoy": nxt["daf_eoy"] if nxt else None,
                "later_returns_line6": later_line6,
                "est_missing_assets_carry_forward": missing_cf,
                "amended_ind": r["amended"], "return_ts": r["return_ts"], "return_object_id": r["oid"],
                "xml_url": r["xml_url"], "source_url": DAFRC_URL}

    flagged = tuple(r for r in rets if r["ein"] in panel and (r["tax_year"] or 0) >= MIN_TY and r["line6_yes"] and part_i_blank(r))
    return tuple(sorted((one(r) for r in flagged), key=lambda x: (x["ein"], x["tax_period_end"])))


def blank_summary(rows: Sequence[Mapping], rets: Sequence[Mapping], panel: frozenset) -> dict:
    scope = tuple(r for r in rets if (r["tax_year"] or 0) >= MIN_TY)
    yes_panel = tuple(r for r in scope if r["ein"] in panel and r["line6_yes"])
    yes_non = tuple(r for r in scope if r["ein"] not in panel and r["line6_yes"])

    def agg(rs):
        return {"returns": len(rs), "sponsors": len({r["ein"] for r in rs}),
                "dafrc_value_same_fy": round(sum(r["dafrc_eoy_daf_assets_same_fy"] or 0 for r in rs)),
                "prior_reported_value_sum": round(sum(r["prior_reported_daf_eoy"] or 0 for r in rs)),
                "dafrc_last_filed_value_sum": round(sum(r["dafrc_last_filed_daf_assets_before"] or 0 for r in rs)),
                "est_missing_carry_forward": round(sum(r["est_missing_assets_carry_forward"] for r in rs))}
    by = lambda key: {str(k): agg(v) for k, v in sorted(_group_by_fast(rows, key).items(), key=lambda kv: str(kv[0]))}  # noqa: E731
    reappear = tuple(r for r in rows if r["next_reported_daf_eoy"])
    last_per_sponsor = {e: max(v, key=lambda r: r["tax_period_end"]) for e, v in _group_by_fast(rows, lambda r: r["ein"]).items()}
    return {"scope_returns_ty2021plus": len(scope), "panel_line6_yes_returns": len(yes_panel),
            "panel_line6_yes_sponsors": len({r["ein"] for r in yes_panel}),
            "non_panel_line6_yes_returns": len(yes_non),
            "non_panel_line6_yes_blank_returns": sum(part_i_blank(r) for r in yes_non),
            "non_panel_line6_yes_blank_sponsors": len({r["ein"] for r in yes_non if part_i_blank(r)}),
            "flagged": agg(rows), "by_fy": by(lambda r: r["fiscal_year"]), "by_kind": by(lambda r: r["blank_kind"]),
            "by_treatment": by(lambda r: r["dafrc_treatment"]),
            "by_fy_treatment": by(lambda r: (r["fiscal_year"], r["dafrc_treatment"])),
            "by_type": by(lambda r: r["dafrc_type"]),
            "values_reappear_returns": len(reappear), "values_reappear_sponsors": len({r["ein"] for r in reappear}),
            "values_reappear_next_value_sum_by_sponsor": round(sum(
                (max((x for x in rows if x["ein"] == e and x["next_reported_daf_eoy"]), key=lambda x: x["tax_period_end"],
                     default={}).get("next_reported_daf_eoy") or 0) for e in {r["ein"] for r in reappear})),
            "sponsors_never_any_reported_value": sum(1 for e, r in last_per_sponsor.items()
                                                     if not any(x["prior_reported_daf_eoy"] is not None or x["next_reported_daf_eoy"] is not None
                                                                for x in rows if x["ein"] == e)),
            "top_by_prior_value": sorted(({"ein": r["ein"], "name": r["sponsor_name"], "fy": r["fiscal_year"],
                                           "treatment": r["dafrc_treatment"], "prior": r["prior_reported_daf_eoy"],
                                           "prior_period": r["prior_reported_period"], "dafrc": r["dafrc_eoy_daf_assets_same_fy"],
                                           "next": r["next_reported_daf_eoy"], "kind": r["blank_kind"]}
                                          for r in rows), key=lambda d: -(d["prior"] or 0))[:25]}


def exit_retest(verify: Sequence[Mapping], tierb: Sequence[Mapping], rets: Sequence[Mapping]) -> dict:
    """Mechanical reporting-gap test of the 100 exit candidates, then exit-rate bounds net of gaps."""
    by_sponsor = _group_by_fast(rets, lambda r: r["ein"])
    tb = {ein9(r["ein"]): r["exit_reason"] for r in tierb}

    def status(v):
        last = v["last_filed_period_end"] or ""
        later = sorted((r for r in by_sponsor.get(ein9(v["ein"]), ()) if r["tax_period_end"] > last),
                       key=lambda r: r["tax_period_end"])
        if not later:
            return "no_later_return_in_cache", 0
        if any(r["line6_yes"] and (r["daf_eoy"] or 0) > 0 for r in later):
            return "values_reappear", len(later)
        yb = [r["line6_yes"] and r["daf_eoy"] is None for r in later]   # Yes with the DAF value line blank (count may be filed)
        if all(yb):
            return "line6_yes_value_blank_all_later", len(later)
        if any(yb) and not later[-1]["line6_yes"]:
            return "gap_then_line6_no", len(later)
        if later[-1]["line6_yes"]:
            return "line6_yes_latest_mixed", len(later)
        return "line6_no_no_gap", len(later)

    rows = tuple({"ein": ein9(v["ein"]), "name": v["name"], "tier": v["outcome_tier"][:1], "exit_fy": v["exit_fy"],
                  "exit_ref_daf_assets": num(v["exit_ref_daf_assets"]), "tierb_manual": tb.get(ein9(v["ein"]), ""),
                  **dict(zip(("mech_status", "later_returns"), status(v)))} for v in verify)
    gap = ("values_reappear", "line6_yes_value_blank_all_later")
    n = lambda pred: sum(1 for r in rows if pred(r))  # noqa: E731
    a, b, c = n(lambda r: r["tier"] == "A"), n(lambda r: r["tier"] == "B"), n(lambda r: r["tier"] == "C")
    b_gap, c_gap = n(lambda r: r["tier"] == "B" and r["mech_status"] in gap), n(lambda r: r["tier"] == "C" and r["mech_status"] in gap)
    b_amb, c_amb = (n(lambda r: r["tier"] == t and r["mech_status"] == "gap_then_line6_no") for t in ("B", "C"))
    rate = lambda k: round(k / EXPOSURE_SPONSOR_YEARS, 6)  # noqa: E731
    return {"candidates": len(rows),
            "tier_counts": {"A": a, "B": b, "C": c, "D": n(lambda r: r["tier"] == "D")},
            "status_by_tier": {f"{t}:{s}": len(v) for (t, s), v in sorted(_group_by_fast(rows, lambda r: (r["tier"], r["mech_status"])).items())},
            "tierb_manual_vs_mech": {f"{m}|{s}": len(v) for (m, s), v in sorted(
                _group_by_fast([r for r in rows if r["tier"] == "B"], lambda r: (r["tierb_manual"], r["mech_status"])).items())},
            "bounds": {"central_original": (a + b, rate(a + b)), "central_net_gaps": (a + b - b_gap, rate(a + b - b_gap)),
                       "central_net_gaps_and_ambiguous": (a + b - b_gap - b_amb, rate(a + b - b_gap - b_amb)),
                       "upper_original": (a + b + c, rate(a + b + c)),
                       "upper_net_gaps": (a + b + c - b_gap - c_gap, rate(a + b + c - b_gap - c_gap)),
                       "upper_net_gaps_and_ambiguous": (a + b + c - b_gap - c_gap - b_amb - c_amb,
                                                        rate(a + b + c - b_gap - c_gap - b_amb - c_amb))},
            "gap_exits_assets": round(sum(r["exit_ref_daf_assets"] or 0 for r in rows if r["tier"] in "BC" and r["mech_status"] in gap)),
            "c_tier_rows": [r for r in rows if r["tier"] == "C"],
            "b_gap_rows": [{k: r[k] for k in ("ein", "name", "mech_status", "tierb_manual", "exit_ref_daf_assets")}
                           for r in rows if r["tier"] == "B" and r["mech_status"] in gap]}


BLANK_FIELDS = ("ein", "sponsor_name", "dafrc_type", "dafrc_subtype", "dafrc_last_operating_status", "tax_year", "fiscal_year",
                "tax_period_end", "line6_raw", "blank_kind", "daf_contributions_filed", "daf_grants_filed", "other_funds_count",
                "other_funds_eoy_value", "total_assets_eoy", "dafrc_treatment", "dafrc_eoy_daf_assets_same_fy",
                "dafrc_accounts_same_fy", "dafrc_source_same_fy", "prior_reported_period", "prior_reported_daf_count",
                "prior_reported_daf_eoy", "dafrc_last_filed_fy_before",
                "dafrc_last_filed_daf_assets_before", "next_reported_period", "next_reported_daf_count", "next_reported_daf_eoy",
                "later_returns_line6", "est_missing_assets_carry_forward", "amended_ind", "return_ts", "return_object_id",
                "xml_url", "source_url")


def run_blank(extract_dir: str) -> dict:
    rets = latest_per_period(tuple(normalise_return(x) for x in load_extract_dir(extract_dir) if x.get("xml_status") == "ok"))
    dafrc = read_csv(DAFRC_CSV)
    panel = frozenset(ein9(r["ein"]) for r in dafrc)
    rows = blank_rows(rets, dafrc)
    write_csv(OUT_BLANK, rows, BLANK_FIELDS)
    return {"blank_sd": blank_summary(rows, rets, panel),
            "exit_retest": exit_retest(read_csv(VERIFY_CSV), read_csv(TIERB_CSV), rets),
            "cache_returns_deduped": len(rets), "cache_panel_eins": len({r["ein"] for r in rets} & panel)}


# ----------------------------------------------------------------------------- task sweepstakes (P-B32A-01)
def market_lookup(rows: Sequence[Mapping]) -> dict:
    return {(int(r["fiscal_year"]), r["metric"]): r for r in rows}


def sweep_rows(sg: Sequence[Mapping], dafrc_rows: Sequence[Mapping], market: Mapping) -> tuple[dict, ...]:
    by_key, _ = dafrc_index(dafrc_rows)

    def one(r):
        fy, ein = int(r["fiscal_year"]), r["ein"]
        gross, kept = num(r["sg_fundraiser_gross_total"]) or 0.0, num(r["sg_fundraiser_retained_total"]) or 0.0
        tot, dc = num(r["total_contributions_part_i"]), num(r["daf_contributions"])
        share = min(1.0, dc / tot) if dc is not None and tot else None
        central = gross * share if share is not None else None
        upper = min(gross, dc) if dc is not None else None
        d = by_key.get((ein, fy))
        m_c, m_a = market.get((fy, "daf_contributions")), market.get((fy, "daf_accounts_eoy"))
        mkt_pub = num(m_c["dataset_sum_as_published"]) if m_c else None
        mkt_cor = num(m_c["corrected_value"]) if m_c else None
        acc_mkt = num(m_a["dataset_sum_as_published"]) if m_a else None
        accts, eoy = num(r["daf_accounts"]), num(r["daf_assets_eoy"])
        return {"ein": ein, "sponsor": PLATFORM_EINS[ein], "fiscal_year": fy, "tax_period": r["tax_period"], "screen_tier": r["tier"],
                "sg_fundraisers": r["sg_fundraisers"][:300], "sg_gross_receipts": gross, "sg_retained_by_agent": kept,
                "sg_retained_share": ratio(kept, gross), "total_contributions_part_i": tot, "sched_d_daf_contributions": dc,
                "daf_share_of_contributions": share, "daf_gross_central_prorata": central, "daf_gross_upper": upper,
                "daf_retained_central_prorata": kept * share if share is not None else None,
                "sched_d_daf_accounts": accts, "sched_d_daf_assets_eoy": eoy,
                "assets_per_account": ratio(eoy, accts), "contributions_per_account": ratio(dc, accts),
                "dafrc_contributions_same_fy": num(d["total_daf_contributions"]) if d else None,
                "dafrc_accounts_same_fy": num(d["number_of_daf_accounts"]) if d else None,
                "dafrc_source_same_fy": d["source_total_daf_contributions"] if d else "",
                "in_dafrc_totals": int(d is not None),
                "market_contributions_published_dataset": mkt_pub, "market_contributions_corrected": mkt_cor,
                "share_of_market_central": ratio(central, mkt_pub) if d else None,
                "share_of_market_upper": ratio(upper, mkt_pub) if d else None,
                "market_accounts_published_dataset": acc_mkt,
                "share_of_market_accounts": ratio(num(d["number_of_daf_accounts"]), acc_mkt) if d and acc_mkt else None,
                "return_object_id": r["return_object_id"], "xml_url": r["xml_url"], "source_url": DAFRC_URL}
    keep = tuple(r for r in sg if r["ein"] in PLATFORM_EINS and (num(r["sg_fundraiser_gross_total"]) or 0) > 0)
    return tuple(sorted((one(r) for r in keep), key=lambda x: (x["sponsor"], x["fiscal_year"])))


def sweep_summary(rows: Sequence[Mapping]) -> dict:
    def agg(rs):
        mk = rs[0]["market_contributions_published_dataset"]
        cen = sum(r["daf_gross_central_prorata"] or 0 for r in rs if r["in_dafrc_totals"])
        up = sum(r["daf_gross_upper"] or 0 for r in rs if r["in_dafrc_totals"])
        kept = sum(r["daf_retained_central_prorata"] or 0 for r in rs if r["in_dafrc_totals"])
        return {"sponsors": [r["sponsor"] for r in rs], "central": round(cen), "upper": round(up), "retained_central": round(kept),
                "market": mk, "share_central": ratio(cen, mk), "share_upper": ratio(up, mk), "retained_share": ratio(kept, mk),
                "outside_dafrc_window_gross": round(sum(r["sg_gross_receipts"] for r in rs if not r["in_dafrc_totals"]))}
    by = _group_by_fast(rows, lambda r: r["fiscal_year"])
    return {"by_fy": {fy: agg(v) for fy, v in sorted(by.items())}}


SWEEP_FIELDS = ("ein", "sponsor", "fiscal_year", "tax_period", "screen_tier", "sg_fundraisers", "sg_gross_receipts",
                "sg_retained_by_agent", "sg_retained_share", "total_contributions_part_i", "sched_d_daf_contributions",
                "daf_share_of_contributions", "daf_gross_central_prorata", "daf_gross_upper", "daf_retained_central_prorata",
                "sched_d_daf_accounts", "sched_d_daf_assets_eoy", "assets_per_account", "contributions_per_account",
                "dafrc_contributions_same_fy", "dafrc_accounts_same_fy", "dafrc_source_same_fy", "in_dafrc_totals",
                "market_contributions_published_dataset", "market_contributions_corrected", "share_of_market_central",
                "share_of_market_upper", "market_accounts_published_dataset", "share_of_market_accounts",
                "return_object_id", "xml_url", "source_url")


def run_sweep() -> dict:
    rows = sweep_rows(read_csv(SCHED_G_CSV), read_csv(DAFRC_CSV), market_lookup(read_csv(MARKET_CSV)))
    write_csv(OUT_SWEEP, rows, SWEEP_FIELDS)
    return {"sweepstakes": sweep_summary(rows), "rows": len(rows)}


# ----------------------------------------------------------------------------- task lowinc (P-B32A-03)
def load_inv(oids: Sequence[str], inv_cache: str, fetch: bool, workers: int) -> dict:
    import mission_infund_costs as mi  # reuse the streamed Part VIII / Sch D XII extractor
    with ThreadPoolExecutor(max(1, workers)) as ex:
        return dict(zip(oids, ex.map(lambda o: mi.fetch_inv(o, inv_cache, fetch), oids)))


def bps(x):
    return round(x * 10_000, 1) if x is not None else None


def lowinc_rows(cost: Sequence[Mapping], inv: Mapping) -> tuple[dict, ...]:
    def one(c):
        g = inv.get(c["return_object_id"], {})
        a_boy, a_eoy = g.get("assets_boy"), g.get("assets_eoy")
        avg = statistics.mean([v for v in (a_boy, a_eoy) if v is not None]) if (a_boy is not None or a_eoy is not None) else None
        l3 = g.get("l3_investment_income")
        l3v = l3 if l3 is not None else 0.0
        tr = sum(x for x in (l3v, g.get("l7d_net_gain"), g.get("xi_5_unrealized")) if x is not None)
        daf_eoy, daf_share = num(c["daf_assets_eoy"]), num(c["daf_share_of_total_assets"])
        fee_l24 = "; ".join(f"{d} {fmt(v)}" for d, v in (g.get("l24") or ()) if d and any(
            k in d.upper() for k in ("FEE", "ADVIS", "COMMISS", "INVEST", "WRAP", "MANAG", "PLATFORM")))[:300]
        return {"ein": c["ein"], "sponsor_name": c["sponsor_name"], "category": c["category"], "fiscal_year": int(c["fiscal_year"]),
                "tax_period": c["tax_period"], "xml_status": g.get("xml_status", ""),
                "l3_investment_income": l3, "l3_reported": int(l3 is not None), "avg_total_assets": avg,
                "l3_bps_of_avg_assets": bps(ratio(l3v, avg)), "l7d_net_gain": g.get("l7d_net_gain"),
                "xi5_unrealized": g.get("xi_5_unrealized"), "total_return_proxy_bps": bps(ratio(tr, avg)),
                "l11f_invest_mgmt_fees": g.get("l11f"), "l11f_bps_of_avg_assets": bps(ratio(g.get("l11f"), avg)),
                "l11g_other_fees": g.get("l11g"), "l24_fee_like_items": fee_l24,
                "sd_xii_4a_inv_exp_not_in_990": g.get("sd_xii_4a_inv_exp"), "sd_xi_4a_inv_exp": g.get("sd_xi_4a_inv_exp"),
                "daf_assets_eoy": daf_eoy, "daf_accounts": num(c["daf_accounts"]), "daf_share_of_total_assets": daf_share,
                "return_object_id": c["return_object_id"], "xml_url": c["xml_url"]}
    return tuple(one(c) for c in cost)


def hit_kind(r: Mapping) -> str:
    if r["avg_total_assets"] is None or r["avg_total_assets"] < LOWINC_MIN_AVG_ASSETS or r["xml_status"] != "ok":
        return ""
    if not r["l3_reported"]:
        return "line3_blank"
    if r["l3_bps_of_avg_assets"] < 0:
        return "line3_negative"
    return "line3_under_50bps" if r["l3_bps_of_avg_assets"] < LOWINC_BPS else ""


def context_pattern(r: Mapping) -> str:
    """Coarse reading of a low line-3 hit from the other investment lines (not evidence of fee netting by itself)."""
    if not r["hit_kind"] and not hit_kind(r):
        return ""
    if not r["l7d_net_gain"] and not r["xi5_unrealized"]:
        return "no_gain_lines_cash_or_noninvesting"
    tr = r["total_return_proxy_bps"]
    if tr is not None and tr >= 300:
        return "normal_total_return_income_likely_in_gains_or_pooled_units"
    if tr is not None and tr < 0:
        return "down_year_ambiguous"
    return "low_yield_and_low_total_return"


def annotate_hits(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    by_ein = _group_by_fast(rows, lambda r: r["ein"])
    peer = {fy: statistics.median([r["l3_bps_of_avg_assets"] for r in v if r["l3_reported"] and r["l3_bps_of_avg_assets"] is not None
                                   and (r["avg_total_assets"] or 0) >= LOWINC_MIN_AVG_ASSETS])
            for fy, v in _group_by_fast(rows, lambda r: r["fiscal_year"]).items()}

    def ann(r):
        k = hit_kind(r)
        yrs = by_ein[r["ein"]]
        nh = sum(1 for y in yrs if hit_kind(y))
        focus = int(bool(k) and (r["daf_assets_eoy"] or 0) >= FOCUS_MIN_DAF_ASSETS and (r["daf_share_of_total_assets"] or 0) >= FOCUS_MIN_DAF_SHARE)
        gains_reclass = int(bool(k) and r["total_return_proxy_bps"] is not None and r["total_return_proxy_bps"] >= 300)
        return {**r, "hit_kind": k, "focus_daf_heavy": focus, "sponsor_years_hit": nh, "sponsor_years_screened": len(yrs),
                "panel_median_l3_bps_same_fy": round(peer.get(r["fiscal_year"], 0), 1),
                "total_return_normal_flag": gains_reclass, "context_pattern": context_pattern({**r, "hit_kind": k})}
    return tuple(sorted((ann(r) for r in rows), key=lambda r: (r["hit_kind"] == "", -(r["daf_assets_eoy"] or 0), r["ein"], r["fiscal_year"])))


LOWINC_FIELDS = ("ein", "sponsor_name", "category", "fiscal_year", "tax_period", "hit_kind", "focus_daf_heavy", "sponsor_years_hit",
                 "sponsor_years_screened", "l3_investment_income", "l3_reported", "avg_total_assets", "l3_bps_of_avg_assets",
                 "panel_median_l3_bps_same_fy", "l7d_net_gain", "xi5_unrealized", "total_return_proxy_bps", "total_return_normal_flag", "context_pattern",
                 "l11f_invest_mgmt_fees", "l11f_bps_of_avg_assets", "l11g_other_fees", "l24_fee_like_items",
                 "sd_xii_4a_inv_exp_not_in_990", "sd_xi_4a_inv_exp", "daf_assets_eoy", "daf_accounts", "daf_share_of_total_assets",
                 "xml_status", "return_object_id", "xml_url")


def lowinc_summary(rows: Sequence[Mapping]) -> dict:
    rows = tuple(rows)
    hits = tuple(r for r in rows if r["hit_kind"])
    foc = tuple(r for r in hits if r["focus_daf_heavy"])
    screened = tuple(r for r in rows if r["xml_status"] == "ok" and (r["avg_total_assets"] or 0) >= LOWINC_MIN_AVG_ASSETS)
    return {"returns": len(rows), "screened_ge_1m_assets": len(screened), "hits": len(hits), "hit_sponsors": len({r["ein"] for r in hits}),
            "hits_by_kind": {k: len(v) for k, v in _group_by_fast(hits, lambda r: r["hit_kind"]).items()},
            "hits_by_category": {k: len(v) for k, v in _group_by_fast(hits, lambda r: r["category"]).items()},
            "focus_hits": len(foc), "focus_sponsors": len({r["ein"] for r in foc}),
            "focus_total_return_normal": sum(r["total_return_normal_flag"] for r in foc),
            "focus_patterns": {k: len(v) for k, v in _group_by_fast(foc, lambda r: r["context_pattern"]).items()},
            "focus_pattern_sponsors": {k: sorted({r["sponsor_name"] for r in v}) for k, v in _group_by_fast(foc, lambda r: r["context_pattern"]).items()},
            "all_hit_patterns": {k: len(v) for k, v in _group_by_fast(hits, lambda r: r["context_pattern"]).items()},
            "national_standard_hits": sorted({(r["sponsor_name"], r["fiscal_year"], r["l3_bps_of_avg_assets"]) for r in hits if r["category"] == "National-Standard"}),
            "national_ge_500m_lowest_l3": sorted(([r["sponsor_name"], r["fiscal_year"], r["l3_bps_of_avg_assets"], r["total_return_proxy_bps"]]
                                                  for r in rows if r["category"].startswith("National") and r["l3_reported"]
                                                  and (r["avg_total_assets"] or 0) >= 500_000_000), key=lambda x: x[2])[:12],
            "focus_with_xii_4a": sum(1 for r in foc if r["sd_xii_4a_inv_exp_not_in_990"]),
            "focus_list": [{k: r[k] for k in ("sponsor_name", "category", "fiscal_year", "hit_kind", "l3_bps_of_avg_assets",
                                              "total_return_proxy_bps", "l11f_bps_of_avg_assets", "daf_assets_eoy",
                                              "daf_share_of_total_assets", "sponsor_years_hit", "sd_xii_4a_inv_exp_not_in_990")}
                           for r in foc],
            "median_l3_bps_by_fy": {fy: round(statistics.median([r["l3_bps_of_avg_assets"] for r in v if r["l3_reported"]]), 1)
                                    for fy, v in sorted(_group_by_fast(screened, lambda r: r["fiscal_year"]).items())}}


def run_lowinc(inv_cache: str, fetch: bool, workers: int) -> dict:
    cost = read_csv(COST_CSV)
    inv = load_inv([c["return_object_id"] for c in cost], inv_cache, fetch, workers)
    rows = annotate_hits(lowinc_rows(cost, inv))
    write_csv(OUT_LOWINC, [r for r in rows if r["hit_kind"]], LOWINC_FIELDS)
    return {"lowinc": lowinc_summary(rows), "xml_status": {k: len(v) for k, v in _group_by_fast(rows, lambda r: r["xml_status"]).items()}}


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--task", choices=("blank_sd", "sweepstakes", "lowinc", "all"), default="all")
    ap.add_argument("--extract990-dir", help="dir of extract990/{oid}.json (mission_990_contractors.py cache)")
    ap.add_argument("--inv-cache", help="cache dir holding extract990inv/ (mission_infund_costs.py)")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args(argv)
    out: dict = {}
    if a.task in ("blank_sd", "all"):
        out.update(run_blank(a.extract990_dir))
    if a.task in ("sweepstakes", "all"):
        out.update(run_sweep())
    if a.task in ("lowinc", "all"):
        out.update(run_lowinc(a.inv_cache, a.fetch, a.workers))
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
