#!/usr/bin/env python3
"""Long tail of DAF sponsors (< $50m / < $10m / < $1m of FY2024 DAF assets) vs the top 50 (queue item P-NEW-TAIL-01).

Stdlib only; functional style (pure transforms, I/O at the edges). Nothing is fetched: every input is repository data,
plus an optional local copy of the IRS EO Business Master File (eo1-4, eo_pr, eo_xx; https://www.irs.gov/pub/irs-soi/).

Inputs (repository)
  * dafrc-sponsor-schedule-d-fy2019-2024.csv + dafrc-corrections-itemized.csv  corrected sponsor-years (R1-R4), built with
    mission_league_table.corrected(); checked against dafrc-corrected-market-totals.csv (FY2021-24, 4 metrics)
  * sponsor-entry-exit-panel.csv, sponsor-exit-verification.csv, tier-b-daf-exit-reasons.csv  entries, exits, outcomes
  * cf-vendor-map-by-ein-v2.csv (CF platform vendor), form990-contractors-harvest-full.csv (Part VII-B DAF-relevant lines)
  * cf-daf-fee-census-2026.csv (top-100 CF fee census), sponsor-fee-schedules.csv (national schedules)
  * blank-schedule-d-panel.csv (blank Part I returns), public-support-cliff-screen.csv (support-test screen)
  * non-dafrc-daf-filers-990.csv (DAF filers outside DAFRC; context row only)

Conventions
  * FY = calendar year in which the tax period ends (DAFRC). Recency rule: FY2021-FY2024 only.
  * Size bands on FY2024 corrected EOY DAF assets: top50 (rank 1-50), mid (rank > 50 and >= $50m), t10_50 ($10m-<$50m),
    t1_10 ($1m-<$10m), t0_1 (> $0 and < $1m), zero (<= $0). Cumulative tails: lt50m = t10_50+t1_10+t0_1+zero, etc.
  * Payout = corrected grants FY t / corrected EOY assets FY t-1 (the repository's market payout definition), computed only
    where neither value is still DAFRC-imputed and prior assets > 0.
  * Average account = assets / accounts where neither is imputed, accounts > 0 and the count passes the plausibility screen
    (> 1,000 accounts averaging < $5 is blanked, as in mission_league_table).
  * Exits use the mortality study's definitions (panel_exit, imputation_masked_candidate, zero_daf_assets_terminal) dated
    FY2021-2023 (FY2024 exits are right-censored); rates are exits / at-risk sponsor-years, banded on prior-year assets.

Usage
  python3 scripts/mission_long_tail.py [--bmf-dir DIR]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
from typing import Callable, Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_league_table import CORR_ITEMS, CORR_TOTALS, METRICS, corrected, identity  # noqa: E402

OUT_CSV = os.path.join(DATA, "daf-long-tail-sponsors-fy2021-2024.csv")
P = lambda f: os.path.join(DATA, f)  # noqa: E731
FYS = (2021, 2022, 2023, 2024)
BMF_FILES = ("eo1.csv", "eo2.csv", "eo3.csv", "eo4.csv", "eo_pr.csv", "eo_xx.csv")
BMF_URL = "https://www.irs.gov/pub/irs-soi/{f}"
BANDS = ("top50", "mid", "t10_50", "t1_10", "t0_1", "zero")
GROUPS = {"top50": ("top50",), "mid_ge50m": ("mid",), "lt50m": ("t10_50", "t1_10", "t0_1", "zero"),
          "lt10m": ("t1_10", "t0_1", "zero"), "lt1m": ("t0_1", "zero"), "b10_50m": ("t10_50",), "b1_10m": ("t1_10",),
          "all": BANDS}
# Sensitivity: tail without two documented structural outliers. BNY Mellon CGF (300748315) terminated in Dec 2024 and granted
# $619.8m to RCF (mission_league_table.EVENTS); Givinga (474172718) is a micro-account processor whose 1.42m "DAFs" are
# not donor accounts in the usual sense (queue-batch35-panel-screens.md, P-B35A-01).
STRUCTURAL = frozenset({"300748315", "474172718"})
CATEGORY = {("Community Foundation", "Community"): "community_foundation",
            ("Single Issue Charity", "Other"): "single_issue_other",
            ("Single Issue Charity", "Religiously-Affiliated"): "religious",
            ("Single Issue Charity", "Universities and Healthcare"): "university_or_hospital",
            ("National", "Standard"): "national_standard",
            ("National", "Donation Processor"): "donation_processor"}
DAF_VENDOR_CATS = {"daf_tech_admin_vendor", "daf_tech_vendor", "giving_platform_or_outsourced_admin", "payment_processor",
                   "grant_admin_due_diligence", "investment_accounting_software"}
# sponsor-fee-schedules.csv carries names only; map each to a unique DAFRC name fragment (checked unique at run time)
FEE_NAME_KEYS = {"Fidelity Charitable": "FIDELITY INVESTMENTS CHARITABLE", "Vanguard Charitable": "VANGUARD CHARITABLE",
                 "DAFgiving360": "DONOR ADVISED CHARITABLE GIVING", "Charityvest Inc": "CHARITYVEST",
                 "Daffy Charitable Fund": "DAFFY CHARITABLE", "Bank of America Charitable Gift Fund": "BANK OF AMERICA CHARITABLE",
                 "National Philanthropic Trust": "NATIONAL PHILANTHROPIC TRUST",
                 "Renaissance Charitable Foundation": "RENAISSANCE CHARITABLE FOUNDATION",
                 "American Endowment Foundation": "AMERICAN ENDOWMENT FOUNDATION",
                 "Goldman Sachs Philanthropy Fund": "GOLDMAN SACHS PHILANTHROPY FUND",
                 "Morgan Stanley GIFT": "MORGAN STANLEY GLOBAL IMPACT", "National Christian Charitable Foundation": "NATIONAL CHRISTIAN"}
NTEE_MAJOR = {"T": "T_philanthropy", "X": "X_religion", "B": "B_education", "E": "E_health", "S": "S_community_improvement",
              "P": "P_human_services", "A": "A_arts", "Q": "Q_international"}


# ----------------------------------------------------------------------------- small pure helpers
def quant(xs: Sequence[float], q: float) -> float | None:
    s = sorted(xs)
    if not s:
        return None
    k = (len(s) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def counter(xs: Iterable[str]) -> dict:
    out: dict = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))


def band_of(rank: int, a: float) -> str:
    return ("top50" if rank <= 50 else "mid" if a >= 50e6 else "t10_50" if a >= 10e6 else "t1_10" if a >= 1e6
            else "t0_1" if a > 0 else "zero")


def size_band(a: float | None) -> str:
    """Band for entries/exits (no rank available consistently): on assets only."""
    a = a or 0.0
    return "ge50m" if a >= 50e6 else "10_50m" if a >= 10e6 else "1_10m" if a >= 1e6 else "lt1m" if a > 0 else "zero"


def implausible(n: float | None, v: float | None) -> bool:
    return bool(n and n > 1000 and v is not None and v < 5 * n)


# ----------------------------------------------------------------------------- loaders (I/O)
def load_bmf(bmf_dir: str | None, eins: frozenset) -> dict:
    if not bmf_dir:
        return {}
    out = {}
    for f in BMF_FILES:
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, newline="", encoding="latin-1") as fh:
            for r in csv.DictReader(fh):
                e = ein9(r["EIN"])
                if e in eins and e not in out:
                    out[e] = {"ruling": r.get("RULING", "").strip(), "state": r.get("STATE", "").strip(),
                              "ntee": r.get("NTEE_CD", "").strip(), "foundation": r.get("FOUNDATION", "").strip(),
                              "subsection": r.get("SUBSECTION", "").strip(), "file": BMF_URL.format(f=f)}
    return out


def bmf_last_modified(bmf_dir: str | None) -> str:
    """Read the saved HTTP header (eo1.hdr) next to the BMF copy, if present."""
    if not bmf_dir:
        return ""
    p = os.path.join(bmf_dir, "eo1.hdr")
    if not os.path.exists(p):
        return ""
    with open(p, encoding="latin-1") as fh:
        return next((ln.split(":", 1)[1].strip() for ln in fh if ln.lower().startswith("last-modified")), "")


# ----------------------------------------------------------------------------- core transforms
def check_totals(corr: Mapping, totals: Sequence[Mapping]) -> dict:
    """Rebuilt corrected sums vs dafrc-corrected-market-totals.csv, FY2021-24."""
    def s(fy, m):
        return sum(v[m] for (e, f), v in corr.items() if f == fy)
    rows = [(int(t["fiscal_year"]), {"assets": "daf_assets_eoy", "contributions": "daf_contributions", "grants": "daf_grants",
                                     "accounts": "daf_accounts_eoy"}.get(t["metric"], t["metric"]), num(t["corrected_value"]))
            for t in totals if int(t["fiscal_year"]) in FYS]
    diffs = [(fy, m, round(s(fy, m) - (v or 0))) for fy, m, v in rows if m in METRICS]
    return {"cells": len(diffs), "max_abs_diff": max((abs(d) for *_, d in diffs), default=None)}


def market_totals(corr: Mapping) -> dict:
    return {fy: {m: sum(v[m] for (e, f), v in corr.items() if f == fy) for m in METRICS} for fy in FYS}


def ranks_fy(corr: Mapping, fy: int) -> dict:
    vals = sorted(((e, v["daf_assets_eoy"]) for (e, f), v in corr.items() if f == fy), key=lambda t: (-t[1], t[0]))
    return {e: i + 1 for i, (e, _) in enumerate(vals)}


def payout(corr: Mapping, e: str, fy: int) -> float | None:
    cur, prev = corr.get((e, fy)), corr.get((e, fy - 1))
    if not cur or not prev or cur["daf_grants_imputed"] or prev["daf_assets_eoy_imputed"] or prev["daf_assets_eoy"] <= 0:
        return None
    return cur["daf_grants"] / prev["daf_assets_eoy"]


def avg_account(v: Mapping | None) -> tuple[float | None, float | None]:
    """(accounts, avg account) with the imputation and plausibility screens."""
    if not v or v["daf_accounts_eoy_imputed"] or v["daf_assets_eoy_imputed"]:
        return None, None
    n, a = v["daf_accounts_eoy"], v["daf_assets_eoy"]
    if not n or n <= 0 or implausible(n, a):
        return None, None
    return n, a / n


def ruling_year(b: Mapping | None) -> int | None:
    r = (b or {}).get("ruling", "")
    return int(r[:4]) if len(r) >= 4 and r[:4].isdigit() and int(r[:4]) > 1800 else None


def exits(panel: Sequence[Mapping]) -> dict:
    """ein -> (exit_kind, exit_fy) from the mortality panel (EIN-level fields repeat on every row)."""
    return {ein9(r["ein"]): (r["sponsor_exit_kind"], int(r["sponsor_exit_fy"]))
            for r in panel if r["sponsor_exit_kind"] in ("panel_exit", "imputation_masked_candidate", "zero_daf_assets_terminal")
            and r["sponsor_exit_fy"]}


def entries(panel: Sequence[Mapping]) -> dict:
    return {ein9(r["ein"]): {"entry_fy": int(r["fiscal_year"]), "entry_class": r["sponsor_entry_class"],
                             "irs_ruling": r["sponsor_irs_ruling"]} for r in panel if r["is_entry_year"] == "1"}


def exit_rates(corr: Mapping, ex: Mapping) -> dict:
    """At-risk sponsor-years (row in t-1, not yet exited) and exits dated t, banded on prior-year corrected assets, t=2021..23."""
    def at_risk(fy):
        return [e for (e, f) in corr if f == fy - 1 and not (e in ex and ex[e][1] < fy)]
    out: dict = {}
    for fy in (2021, 2022, 2023):
        for e in at_risk(fy):
            b = size_band(corr[(e, fy - 1)]["daf_assets_eoy"])
            d = out.setdefault(b, {"at_risk": 0, "exits": 0, "exit_assets_prior": 0.0, "at_risk_assets": 0.0})
            exited = e in ex and ex[e][1] == fy
            out[b] = {"at_risk": d["at_risk"] + 1, "exits": d["exits"] + exited,
                      "at_risk_assets": d["at_risk_assets"] + corr[(e, fy - 1)]["daf_assets_eoy"],
                      "exit_assets_prior": d["exit_assets_prior"] + (corr[(e, fy - 1)]["daf_assets_eoy"] if exited else 0.0)}
    return {b: {**d, "exit_rate_count_per_yr": d["exits"] / d["at_risk"] if d["at_risk"] else None} for b, d in out.items()}


def vendor_990(contractors: Sequence[Mapping]) -> dict:
    rows = [r for r in contractors if r["vendor_category"] in DAF_VENDOR_CATS and r["fiscal_year"] in ("2022", "2023", "2024", "2025")]
    by = _group_by_fast(rows, lambda r: ein9(r["ein"]))
    return {e: ";".join(sorted({r["vendor_group"] for r in rs})) for e, rs in by.items()}


def fee_lookup(census: Sequence[Mapping], sched: Sequence[Mapping], ids: Mapping) -> dict:
    cf = {ein9(r["ein"]): {"fee_source": "cf-daf-fee-census-2026.csv", "fee_status": r["status"],
                           "fee_bps_100k": r["admin_bps_100k"], "fee_bps_1m": r["admin_bps_1000k"], "fee_url": r["source_url"]}
          for r in census if r["status"] != "national_comparator" and r["ein"]}
    names = {s["sponsor"] for s in sched}
    nat = {}
    for s in sorted(names):
        key = FEE_NAME_KEYS.get(s)
        hits = [e for e, i in ids.items() if key and key in i["name"].upper()]
        if len(hits) == 1:
            urls = sorted({r["source_url"] for r in sched if r["sponsor"] == s})
            nat[hits[0]] = {"fee_source": "sponsor-fee-schedules.csv", "fee_status": "published_schedule_national",
                            "fee_bps_100k": "", "fee_bps_1m": "", "fee_url": urls[0] if urls else ""}
    return {**nat, **cf}


def sponsor_rows(corr, ids, ranks24, bmf, ent, ex, verif, tierb, cfmap, v990, fees, blanks, cliff) -> list[dict]:
    eins = sorted({e for (e, f) in corr if f in (2020,) + FYS})  # FY2020 kept only as the baseline for FY2021 exits
    vby = {ein9(r["ein"]): r for r in verif}
    tby = {ein9(r["ein"]): r for r in tierb}
    cby = {ein9(r["ein"]): r for r in cfmap}

    def row(e):
        i = ids.get(e, {"name": "", "type": "", "subtype": ""})
        v24 = corr.get((e, 2024))
        rank = ranks24.get(e)
        band = band_of(rank, v24["daf_assets_eoy"]) if v24 else "not_in_fy2024"
        n24, avg24 = avg_account(v24)
        b = bmf.get(e)
        ry = ruling_year(b)
        en, x = ent.get(e, {}), ex.get(e)
        vr, tb, cm, fe = vby.get(e, {}), tby.get(e, {}), cby.get(e, {}), fees.get(e, {})
        return {"ein": e, "name": i["name"], "dafrc_type": i["type"], "dafrc_subtype": i["subtype"],
                "sponsor_category": CATEGORY.get((i["type"], i["subtype"]), "unclassified"),
                "fy2024_rank_assets": rank or "", "size_band_fy2024": band,
                "in_lt50m": int(band in GROUPS["lt50m"]), "in_lt10m": int(band in GROUPS["lt10m"]), "in_lt1m": int(band in GROUPS["lt1m"]),
                **{f"daf_assets_fy{fy}": (corr[(e, fy)]["daf_assets_eoy"] if (e, fy) in corr else None) for fy in FYS},
                "daf_contributions_fy2024": v24["daf_contributions"] if v24 else None,
                "daf_grants_fy2024": v24["daf_grants"] if v24 else None,
                "daf_accounts_fy2024": v24["daf_accounts_eoy"] if v24 else None,
                "accounts_fy2024_screened": n24, "avg_account_fy2024": avg24,
                **{f"payout_fy{fy}": payout(corr, e, fy) for fy in (2022, 2023, 2024)},
                "imputed_kept_fy2024": ";".join(m for m in METRICS if v24 and v24[f"{m}_imputed"]),
                "corrections_fy2024": (v24 or {}).get("rules", ""),
                "entry_fy": en.get("entry_fy", ""), "entry_in_fy2021_24": int(bool(en) and 2021 <= en["entry_fy"] <= 2024),
                "entry_class": en.get("entry_class", "") if en and 2021 <= en["entry_fy"] <= 2024 else "",
                "exit_kind": x[0] if x else "", "exit_fy": x[1] if x else "",
                "exit_in_fy2021_23": int(bool(x) and 2021 <= x[1] <= 2023),
                "exit_outcome": vr.get("outcome", ""), "exit_outcome_tier": vr.get("outcome_tier", ""),
                "exit_ref_daf_assets": vr.get("exit_ref_daf_assets", ""), "tierb_exit_reason": tb.get("exit_reason", ""),
                "bmf_ruling": (b or {}).get("ruling", ""), "ruling_year": ry or "", "age_years_at_2024": (2024 - ry) if ry else "",
                "bmf_state": (b or {}).get("state", ""), "bmf_ntee": (b or {}).get("ntee", ""),
                "ntee_major": NTEE_MAJOR.get((b or {}).get("ntee", "")[:1], (b or {}).get("ntee", "")[:1] or ""),
                "bmf_foundation_cd": (b or {}).get("foundation", ""), "in_bmf_2026": int(bool(b)),
                "cf_vendor_family": cm.get("vendor_family", ""), "cf_vendor_confidence": cm.get("confidence", ""),
                "cf_vendor_evidence_type": cm.get("evidence_type", ""),
                "vendors_990_daf_relevant_fy2022_25": v990.get(e, ""),
                "fee_status": fe.get("fee_status", ""), "fee_bps_100k": fe.get("fee_bps_100k", ""),
                "fee_bps_1m": fe.get("fee_bps_1m", ""), "fee_source": fe.get("fee_source", ""), "fee_url": fe.get("fee_url", ""),
                "blank_part_i_returns_fy2021_24": blanks.get(e, 0), "support_cliff_flags_fy2021_24": cliff.get(e, ""),
                "source": "corrected DAFRC panel (R1-R4); IRS EO BMF; repo vendor/fee/exit files (see script docstring)"}
    return [row(e) for e in eins]


def group_stats(rows: Sequence[Mapping], tot24: Mapping) -> dict:
    n24 = sum(r["size_band_fy2024"] in BANDS for r in rows)

    def stats(rs):
        a = [r["daf_assets_fy2024"] for r in rs]
        pay = [r["payout_fy2024"] for r in rs if r["payout_fy2024"] is not None]
        pay_pool = [r[f"payout_fy{fy}"] for r in rs for fy in (2022, 2023, 2024) if r[f"payout_fy{fy}"] is not None]
        acc = [r["accounts_fy2024_screened"] for r in rs if r["accounts_fy2024_screened"]]
        avg = [r["avg_account_fy2024"] for r in rs if r["avg_account_fy2024"] is not None]
        ages = [r["age_years_at_2024"] for r in rs if r["age_years_at_2024"] != ""]
        ryrs = [r["ruling_year"] for r in rs if r["ruling_year"] != ""]
        cfs = [r for r in rs if r["sponsor_category"] == "community_foundation"]
        sumk = lambda k: sum((r[k] or 0) for r in rs)  # noqa: E731
        pv = [r for r in rs if r["payout_fy2024"] is not None]
        return {
            "n": len(rs), "share_n": len(rs) / n24 if n24 else None,
            "assets": sumk("daf_assets_fy2024"), "share_assets": sumk("daf_assets_fy2024") / tot24["daf_assets_eoy"],
            "contributions": sumk("daf_contributions_fy2024"), "share_contributions": sumk("daf_contributions_fy2024") / tot24["daf_contributions"],
            "grants": sumk("daf_grants_fy2024"), "share_grants": sumk("daf_grants_fy2024") / tot24["daf_grants"],
            "accounts": sumk("daf_accounts_fy2024"), "share_accounts": sumk("daf_accounts_fy2024") / tot24["daf_accounts_eoy"],
            "median_assets": quant(a, .5),
            "category_n": counter(r["sponsor_category"] for r in rs),
            "category_assets_share": {c: sum(r["daf_assets_fy2024"] for r in rs if r["sponsor_category"] == c) / (sum(a) or 1)
                                      for c in counter(r["sponsor_category"] for r in rs)},
            "n_imputed_kept_any": sum(bool(r["imputed_kept_fy2024"]) for r in rs),
            "n_with_ruling": len(ryrs), "median_ruling_year": quant(ryrs, .5), "median_age": quant(ages, .5),
            "p25_age": quant(ages, .25), "p75_age": quant(ages, .75),
            "share_ruled_2015_plus": sum(y >= 2015 for y in ryrs) / len(ryrs) if ryrs else None,
            "share_ruled_pre1990": sum(y < 1990 for y in ryrs) / len(ryrs) if ryrs else None,
            "n_states": len({r["bmf_state"] for r in rs if r["bmf_state"]}),
            "top_states": dict(list(counter(r["bmf_state"] for r in rs if r["bmf_state"]).items())[:8]),
            "ntee_major": dict(list(counter(r["ntee_major"] or "none" for r in rs if r["in_bmf_2026"]).items())[:8]),
            "n_accounts_valid": len(acc), "median_accounts": quant(acc, .5), "p25_accounts": quant(acc, .25), "p75_accounts": quant(acc, .75),
            "n_avg_valid": len(avg), "median_avg_account": quant(avg, .5), "p25_avg_account": quant(avg, .25), "p75_avg_account": quant(avg, .75),
            "n_payout_valid": len(pay), "median_payout_fy2024": quant(pay, .5), "p25_payout": quant(pay, .25), "p75_payout": quant(pay, .75),
            "share_payout_lt5pct": sum(p < .05 for p in pay) / len(pay) if pay else None,
            "share_payout_zero_or_less": sum(p <= 0 for p in pay) / len(pay) if pay else None,
            "share_payout_ge20pct": sum(p >= .20 for p in pay) / len(pay) if pay else None,
            "share_payout_gt100pct": sum(p > 1 for p in pay) / len(pay) if pay else None,
            "aggregate_payout_fy2024_valid": (sum(r["daf_grants_fy2024"] for r in pv) / sum(r["daf_assets_fy2023"] for r in pv)) if pv else None,
            "n_payout_pooled_fy2022_24": len(pay_pool), "median_payout_pooled_fy2022_24": quant(pay_pool, .5),
            "share_payout_lt5pct_pooled": sum(p < .05 for p in pay_pool) / len(pay_pool) if pay_pool else None,
            "entered_fy2021_24": sum(r["entry_in_fy2021_24"] for r in rs),
            "n_cf": len(cfs), "cf_vendor_family": counter(r["cf_vendor_family"] or "not_in_map" for r in cfs),
            "cf_mapped_high_or_medium": sum(r["cf_vendor_confidence"] in ("high", "medium") for r in cfs),
            "cf_foundant_high_or_medium": sum(r["cf_vendor_family"] == "Foundant" and r["cf_vendor_confidence"] in ("high", "medium") for r in cfs),
            "n_with_990_daf_vendor_line": sum(bool(r["vendors_990_daf_relevant_fy2022_25"]) for r in rs),
            "vendor_990_groups": counter(v for r in rs for v in r["vendors_990_daf_relevant_fy2022_25"].split(";") if v),
            "n_fee_published": sum(r["fee_status"] in ("published_schedule", "published_schedule_national") for r in rs),
            "n_fee_any_census_row": sum(bool(r["fee_status"]) for r in rs),
            "n_blank_part_i_any": sum(r["blank_part_i_returns_fy2021_24"] > 0 for r in rs),
            "n_cliff_screened_flagged": sum(bool(r["support_cliff_flags_fy2021_24"]) for r in rs),
        }
    cur = [r for r in rows if r["size_band_fy2024"] in BANDS]
    base = {g: stats([r for r in cur if r["size_band_fy2024"] in bs]) for g, bs in GROUPS.items()}
    return {**base, "lt50m_ex_structural": stats([r for r in cur if r["size_band_fy2024"] in GROUPS["lt50m"] and r["ein"] not in STRUCTURAL]),
            "lt10m_ex_structural": stats([r for r in cur if r["size_band_fy2024"] in GROUPS["lt10m"] and r["ein"] not in STRUCTURAL])}


def entry_exit_summary(rows: Sequence[Mapping], corr: Mapping, ex: Mapping) -> dict:
    ent = [r for r in rows if r["entry_in_fy2021_24"]]
    ent_band = counter(size_band(corr[(r["ein"], r["entry_fy"])]["daf_assets_eoy"]) for r in ent if (r["ein"], r["entry_fy"]) in corr)
    exs = [r for r in rows if r["exit_in_fy2021_23"]]
    ex_band = lambda r: size_band(num(r["exit_ref_daf_assets"]))  # noqa: E731
    return {
        "entries_fy2021_24_n": len(ent), "entries_by_entry_year_band": ent_band,
        "entries_by_fy2024_band": counter(r["size_band_fy2024"] for r in ent),
        "entries_by_class": counter(r["entry_class"] or "blank" for r in ent),
        "entries_by_year": counter(str(r["entry_fy"]) for r in ent),
        "entries_lt50m_by_category": counter(r["sponsor_category"] for r in ent if r["size_band_fy2024"] in GROUPS["lt50m"]),
        "exits_fy2021_23_n": len(exs), "exits_by_kind": counter(r["exit_kind"] for r in exs),
        "exits_by_exit_ref_band": counter(ex_band(r) for r in exs),
        "exits_by_band_and_tier": counter(f"{ex_band(r)}|{r['exit_outcome_tier'] or 'none'}" for r in exs),
        "exits_lt50m_by_category": counter(r["sponsor_category"] for r in exs if ex_band(r) != "ge50m"),
        "exits_lt50m_tierb_reasons": counter(r["tierb_exit_reason"] for r in exs if ex_band(r) != "ge50m" and r["tierb_exit_reason"]),
        "exit_rates_by_prior_year_band_fy2021_23": exit_rates(corr, ex),
    }


def outside_context(rows: Sequence[Mapping]) -> dict:
    out = {}
    for fy in ("2023", "2024"):
        v = [num(r["sched_d_daf_eoy_value"]) for r in rows if r["fiscal_year"] == fy and r["status"] == "reports_daf_value"]
        v = [x for x in v if x is not None]
        out[fy] = {"n": len(v), "sum": sum(v), "median": quant(v, .5), "n_lt1m": sum(x < 1e6 for x in v),
                   "n_lt50m": sum(x < 50e6 for x in v)}
    return out


# ----------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--bmf-dir", default=None, help="directory with IRS EO BMF eo1-4.csv, eo_pr.csv, eo_xx.csv")
    a = ap.parse_args(argv)

    dafrc, items = read_csv(DAFRC_CSV), read_csv(CORR_ITEMS)
    corr, ids = corrected(dafrc, items), identity(dafrc, items)
    chk = check_totals(corr, read_csv(CORR_TOTALS))
    tots = market_totals(corr)
    ranks24 = ranks_fy(corr, 2024)
    panel = read_csv(P("sponsor-entry-exit-panel.csv"))
    ent, ex = entries(panel), exits(panel)
    eins = frozenset(e for (e, f) in corr if f in FYS)
    bmf = load_bmf(a.bmf_dir, eins)
    blanks = counter(ein9(r["ein"]) for r in read_csv(P("blank-schedule-d-panel.csv")) if r["fiscal_year"] in {str(f) for f in FYS})
    cliff_rows = [r for r in read_csv(P("public-support-cliff-screen.csv")) if r["fiscal_year"] in {str(f) for f in FYS} and r["flags"]]
    cliff = {e: ";".join(sorted({f for r in rs for f in r["flags"].split(";")})) for e, rs in _group_by_fast(cliff_rows, lambda r: ein9(r["ein"])).items()}
    fees = fee_lookup(read_csv(P("cf-daf-fee-census-2026.csv")), read_csv(P("sponsor-fee-schedules.csv")), ids)
    rows = sponsor_rows(corr, ids, ranks24, bmf, ent, ex, read_csv(P("sponsor-exit-verification.csv")),
                        read_csv(P("tier-b-daf-exit-reasons.csv")), read_csv(P("cf-vendor-map-by-ein-v2.csv")),
                        vendor_990(read_csv(P("form990-contractors-harvest-full.csv"))), fees, blanks, cliff)
    write_csv(OUT_CSV, rows, list(rows[0].keys()))
    summary = {
        "corrected_totals_check_fy2021_24": chk, "market_fy2024": tots[2024],
        "fy2024_sponsors": sum(1 for (e, f) in corr if f == 2024),
        "band_n": counter(r["size_band_fy2024"] for r in rows),
        "rank50_assets": next(r["daf_assets_fy2024"] for r in rows if r["fy2024_rank_assets"] == 50),
        "bmf_matched_fy2024": sum(r["in_bmf_2026"] for r in rows if r["size_band_fy2024"] in BANDS),
        "bmf_last_modified": bmf_last_modified(a.bmf_dir),
        "groups": group_stats(rows, tots[2024]),
        "entry_exit": entry_exit_summary(rows, corr, ex),
        "outside_dafrc_reports_daf_value": outside_context(read_csv(P("non-dafrc-daf-filers-990.csv"))),
        "fee_rows_matched": {e: fees[e]["fee_source"] for e in fees if e in eins and fees[e]["fee_source"] == "sponsor-fee-schedules.csv"},
        "structural_in_tail": {r["ein"]: [r["name"], r["daf_assets_fy2024"], r["daf_grants_fy2024"], r["daf_accounts_fy2024"]]
                               for r in rows if r["ein"] in STRUCTURAL},
        "tail_payout_gt100pct_examples": [[r["name"], r["sponsor_category"], round(r["payout_fy2024"], 2)] for r in sorted(
            (r for r in rows if r["in_lt50m"] and r["payout_fy2024"] is not None and r["payout_fy2024"] > 1),
            key=lambda r: -r["daf_grants_fy2024"])[:10]],
        "tail_top_accounts": [[r["name"], r["sponsor_category"], r["daf_accounts_fy2024"]] for r in sorted(
            (r for r in rows if r["in_lt50m"]), key=lambda r: -(r["daf_accounts_fy2024"] or 0))[:6]],
        "tail_persistent_payout_lt5pct_fy2022_24": (lambda t3: {
            "n_with_three_payouts": len(t3), "n_all_three_lt5pct": sum(all(r[f"payout_fy{y}"] < .05 for y in (2022, 2023, 2024)) for r in t3),
            "assets_fy2024": sum(r["daf_assets_fy2024"] for r in t3 if all(r[f"payout_fy{y}"] < .05 for y in (2022, 2023, 2024))),
            "by_category": counter(r["sponsor_category"] for r in t3 if all(r[f"payout_fy{y}"] < .05 for y in (2022, 2023, 2024)))})(
            [r for r in rows if r["in_lt50m"] and all(r[f"payout_fy{y}"] is not None for y in (2022, 2023, 2024))]),
        "rows_written": len(rows), "out": os.path.relpath(OUT_CSV),
    }
    print(json.dumps(summary, indent=1, default=lambda x: round(x, 6) if isinstance(x, float) else str(x)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
