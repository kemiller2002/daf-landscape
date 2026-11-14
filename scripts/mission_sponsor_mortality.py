#!/usr/bin/env python3
"""DAF sponsor entry/exit ("mortality") panel for mission 2026-11-14 (P-FAIL-01).

Stdlib only, functional style: every transformation is a pure function over
immutable rows; I/O sits at the edges (load_*, fetch_*, write_csv, main).

Inputs
  data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv  (DAFRC panel)
  Optional verification evidence (``--irs-dir``), all public IRS files:
    eo1.csv..eo4.csv                 IRS EO Business Master File extract
                                     https://www.irs.gov/pub/irs-soi/eo{1-4}.csv
    data-download-revocation.txt     IRS auto-revocation list
                                     https://apps.irs.gov/pub/epostcard/data-download-revocation.zip
    index_YYYY.csv                   IRS e-file (TEOS) index, 2019-2026
                                     https://apps.irs.gov/pub/epostcard/990/xml/YYYY/index_YYYY.csv
  Optional network evidence (``--fetch``, cached in ``--cache-dir``):
    ProPublica Nonprofit Explorer API  https://projects.propublica.org/nonprofits/api/v2/organizations/{EIN}.json
    e-filed 990 XML (GivingTuesday 990 data lake mirror of IRS TEOS XML)
      https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml

Outputs (data/mission-2026-11-14/)
  sponsor-entry-exit-panel.csv     one row per EIN x FY with entry/exit/gap/artifact flags
  sponsor-mortality-summary.csv    long-format counts, rates and assets by year, type,
                                   subtype and asset band (+ verified bounds if verification ran)
  sponsor-exit-verification.csv    (with --irs-dir) every exit candidate with IRS/ProPublica/XML
                                   evidence, rule-based outcome and sample stratum

Usage
  python3 scripts/mission_sponsor_mortality.py                       # panel + summary only
  python3 scripts/mission_sponsor_mortality.py --irs-dir DIR --fetch --cache-dir DIR
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from itertools import groupby
from typing import Callable, Iterable, Mapping, NamedTuple, Sequence

DATA_DIR_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "data", "mission-2026-11-14")
PANEL_IN = "dafrc-sponsor-schedule-d-fy2019-2024.csv"
PANEL_OUT = "sponsor-entry-exit-panel.csv"
SUMMARY_OUT = "sponsor-mortality-summary.csv"
VERIFY_OUT = "sponsor-exit-verification.csv"
DAFRC_URL = "https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx"
PP_API = "https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"
PP_ORG = "https://projects.propublica.org/nonprofits/organizations/{ein}"
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
BMF_URL = "https://www.irs.gov/pub/irs-soi/eo{n}.csv"
REVOC_URL = "https://apps.irs.gov/pub/epostcard/data-download-revocation.zip"
INDEX_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
FIRST_FY, LAST_FY = 2019, 2024
FILED_SOURCES = frozenset({"IRS 990", "NPT historical data", "paper submission"})
SIZE_BANDS = ((1e9, "e_1bn_plus"), (1e8, "d_100m_1bn"), (1e7, "c_10m_100m"),
              (1e6, "b_1m_10m"), (1, "a_under_1m"), (float("-inf"), "z_zero_or_missing"))
SAMPLE_SEED = 20261114
SAMPLE_TOP, SAMPLE_RANDOM = 25, 25

# Manually researched evidence for sampled exits (merger/transfer facts that
# IRS files cannot show). Keyed by EIN; every entry carries its source URL.
# Only facts read on the cited page are recorded here.
MANUAL_EVIDENCE: Mapping[str, Mapping[str, str]] = {}


class Row(NamedTuple):
    ein: str
    fy: int
    period_end: str
    name: str
    accounts: float | None
    contributions: float | None
    grants: float | None
    assets: float | None
    assets_src: str
    accounts_src: str
    operating_status: str
    vetted_status: str
    type: str
    subtype: str


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------
def num(x: str | None) -> float | None:
    try:
        return float(x) if x not in (None, "") else None
    except ValueError:
        return None


def fmt(x) -> str:
    if x is None:
        return ""
    if isinstance(x, bool):
        return "1" if x else "0"
    if isinstance(x, float):
        return str(int(x)) if x.is_integer() else f"{x:.6f}"
    return str(x)


def size_band(assets: float | None) -> str:
    if assets is None or assets <= 0:
        return "z_zero_or_missing"
    return next(label for floor, label in SIZE_BANDS if assets >= floor)


def is_filed(src: str) -> bool:
    return src in FILED_SOURCES


def safe_div(a: float, b: float) -> float | None:
    return a / b if b else None


def to_row(d: Mapping[str, str]) -> Row:
    return Row(
        ein=d["ein"].zfill(9), fy=int(d["fiscal_year_end"]), period_end=d["end_of_tax_period"],
        name=d["name"], accounts=num(d["number_of_daf_accounts"]),
        contributions=num(d["total_daf_contributions"]), grants=num(d["total_daf_grants"]),
        assets=num(d["eoy_daf_assets"]), assets_src=d["source_eoy_daf_assets"],
        accounts_src=d["source_number_of_accounts"], operating_status=d["operating_status"],
        vetted_status=d["vetted_status"], type=d["type"], subtype=d["subtype"],
    )


def group_by_ein(rows: Iterable[Row]) -> dict[str, tuple[Row, ...]]:
    ordered = sorted(rows, key=lambda r: (r.ein, r.fy))
    return {ein: tuple(rs) for ein, rs in groupby(ordered, key=lambda r: r.ein)}


# ---------------------------------------------------------------------------
# Sponsor-level history: entries, exits, gaps, artifacts
# ---------------------------------------------------------------------------
def sponsor_history(rows: Sequence[Row]) -> dict:
    """Classify one EIN's FY2019-FY2024 history. Pure."""
    years = tuple(r.fy for r in rows)
    filed = tuple(r for r in rows if is_filed(r.assets_src) and r.assets is not None)
    filed_pos = tuple(r for r in filed if r.assets > 0)
    first, last = years[0], years[-1]
    last_filed = filed[-1].fy if filed else None
    last_pos = filed_pos[-1] if filed_pos else None
    # terminal zero run: filed zero DAF assets from some year through the end, after a positive year
    trailing_zero = tuple(
        r.fy for r in rows
        if is_filed(r.assets_src) and r.assets == 0 and last_pos is not None and r.fy > last_pos.fy
    )
    zero_exit = bool(
        last_pos is not None and trailing_zero and last == LAST_FY
        and all(not is_filed(r.assets_src) or r.assets == 0 for r in rows if r.fy > last_pos.fy)
    )
    internal_imputed = tuple(
        r.fy for r in rows
        if not is_filed(r.assets_src) and filed and r.fy < last_filed and r.fy > filed[0].fy
    )
    trailing_imputed = tuple(r.fy for r in rows if last_filed is not None and r.fy > last_filed
                             and not is_filed(r.assets_src))
    panel_exit = last < LAST_FY
    masked = (not panel_exit) and last_filed is not None and last_filed <= LAST_FY - 2
    never_filed = last_filed is None
    if panel_exit:
        exit_kind, exit_year = "panel_exit", last + 1
    elif masked:
        exit_kind, exit_year = "imputation_masked_candidate", last_filed + 1
    elif never_filed:
        exit_kind, exit_year = "never_filed_all_imputed", None
    elif zero_exit:
        exit_kind, exit_year = "zero_daf_assets_terminal", trailing_zero[0]
    else:
        exit_kind, exit_year = "", None
    period_months = tuple(r.period_end[5:7] for r in filed if r.period_end)
    exit_ref = last_pos or (filed[-1] if filed else rows[-1])
    return {
        "ein": rows[0].ein, "name": rows[-1].name, "type": rows[-1].type, "subtype": rows[-1].subtype,
        "operating_status": rows[-1].operating_status, "vetted_status": rows[-1].vetted_status,
        "first_fy": first, "last_fy": last, "n_years": len(years),
        "last_filed_fy": last_filed, "last_filed_period_end": filed[-1].period_end if filed else "",
        "entry_fy": first if first > FIRST_FY else None,
        "left_censored": first == FIRST_FY,
        "entry_first_row_imputed": first > FIRST_FY and not is_filed(rows[0].assets_src),
        "exit_kind": exit_kind, "exit_fy": exit_year,
        "imputed_gap_years": internal_imputed, "trailing_imputed_years": trailing_imputed,
        "fiscal_month_changed": len(set(period_months)) > 1,
        "exit_ref_fy": exit_ref.fy, "exit_ref_assets": exit_ref.assets, "exit_ref_accounts": exit_ref.accounts,
        "max_filed_assets": max((r.assets for r in filed), default=None),
        "exit_size_band": size_band(exit_ref.assets),
    }


def carry_forward_period(rows: Sequence[Row]) -> frozenset[int]:
    """FYs whose end_of_tax_period repeats the previous FY's (label lag / carry-forward)."""
    return frozenset(b.fy for a, b in zip(rows, rows[1:]) if b.period_end and b.period_end == a.period_end)


def panel_rows(rows: Sequence[Row], hist: Mapping) -> tuple[dict, ...]:
    cf = carry_forward_period(rows)
    return tuple({
        "ein": r.ein, "fiscal_year": r.fy, "end_of_tax_period": r.period_end, "name": r.name,
        "type": r.type, "subtype": r.subtype, "operating_status": r.operating_status,
        "vetted_status": r.vetted_status, "eoy_daf_assets": r.assets, "number_of_daf_accounts": r.accounts,
        "total_daf_grants": r.grants, "total_daf_contributions": r.contributions,
        "source_eoy_daf_assets": r.assets_src, "assets_filed": is_filed(r.assets_src),
        "size_band": size_band(r.assets),
        "is_entry_year": hist["entry_fy"] == r.fy,
        "is_first_obs_left_censored": hist["left_censored"] and r.fy == FIRST_FY,
        "is_last_panel_year": r.fy == hist["last_fy"],
        "is_last_filed_year": r.fy == hist["last_filed_fy"],
        "is_imputed_gap": r.fy in hist["imputed_gap_years"],
        "is_trailing_imputed": r.fy in hist["trailing_imputed_years"],
        "is_period_carry_forward": r.fy in cf,
        "sponsor_exit_kind": hist["exit_kind"], "sponsor_exit_fy": hist["exit_fy"],
        "sponsor_first_fy": hist["first_fy"], "sponsor_last_fy": hist["last_fy"],
        "sponsor_last_filed_fy": hist["last_filed_fy"],
    } for r in rows)


# ---------------------------------------------------------------------------
# Summary (count- and asset-weighted)
# ---------------------------------------------------------------------------
EXIT_KINDS = ("panel_exit", "imputation_masked_candidate", "zero_daf_assets_terminal")
DIMENSIONS: Mapping[str, Callable[[Mapping], str]] = {
    "all": lambda h: "all",
    "type": lambda h: h["type"],
    "subtype": lambda h: h["subtype"],
}


def summary_rows(by_ein: Mapping[str, Sequence[Row]], hists: Mapping[str, Mapping]) -> list[dict]:
    """At-risk set for FY t = EINs with a panel row in t-1 whose exit (if any) is >= t.
    Exits are dated to the first FY without filed DAF data (exit_fy)."""
    row_at = {(e, r.fy): r for e, rs in by_ein.items() for r in rs}

    def alive(h, t):  # present in t-1 and not yet exited before t
        return (h["ein"], t - 1) in row_at and (h["exit_fy"] is None or h["exit_fy"] >= t)

    def band_dim(h, t):
        r = row_at.get((h["ein"], t - 1))
        return size_band(r.assets if r else None)

    out: list[dict] = []
    defn = {
        "at_risk_n": "EINs with a DAFRC row in FY t-1 and not exited before t",
        "at_risk_assets": "sum of FY t-1 eoy_daf_assets (filed or imputed) of the at-risk set",
        "entries_n": "EINs whose first DAFRC row is FY t (t>2019); FY2019 is left-censored",
        "entries_first_row_imputed_n": "entries whose first row is imputed (inclusion artefact risk)",
        "entry_assets": "FY t eoy_daf_assets of entrants",
    }
    for t in range(FIRST_FY + 1, LAST_FY + 1):
        for dim, key in {**DIMENSIONS, "size_band_prior_year": None}.items():
            keyf = (lambda h, t=t: band_dim(h, t)) if key is None else key
            risk = [h for h in hists.values() if alive(h, t)]
            groups = sorted({keyf(h) for h in risk} | {keyf(h) for h in hists.values() if h["entry_fy"] == t})
            for g in groups:
                r_g = [h for h in risk if keyf(h) == g]
                at_n = len(r_g)
                at_a = sum((row_at[(h["ein"], t - 1)].assets or 0) for h in r_g)
                ent = [h for h in hists.values() if h["entry_fy"] == t and keyf(h) == g]
                base = {"dimension": dim, "group": g, "fiscal_year": t}
                vals = [
                    ("at_risk_n", at_n, None, None),
                    ("at_risk_assets", at_a, None, None),
                    ("entries_n", len(ent), None, None),
                    ("entries_first_row_imputed_n", sum(h["entry_first_row_imputed"] for h in ent), None, None),
                    ("entry_assets", sum((row_at[(h["ein"], t)].assets or 0) for h in ent), None, None),
                ]
                for k in EXIT_KINDS:
                    ex = [h for h in r_g if h["exit_kind"] == k and h["exit_fy"] == t]
                    ex_a = sum(h["exit_ref_assets"] or 0 for h in ex)
                    vals += [
                        (f"exits_{k}_n", len(ex), None, None),
                        (f"exits_{k}_assets", ex_a, None, None),
                        (f"exit_rate_{k}_count", safe_div(len(ex), at_n), len(ex), at_n),
                        (f"exit_rate_{k}_asset_weighted", safe_div(ex_a, at_a), ex_a, at_a),
                    ]
                out += [{**base, "measure": m, "value": v, "numerator": n, "denominator": d,
                         "definition": defn.get(m, exit_definition(m))} for m, v, n, d in vals]
    return out


def exit_definition(measure: str) -> str:
    k = next((k for k in EXIT_KINDS if k in measure), "")
    what = {
        "panel_exit": "EIN has no DAFRC row in FY t or later (DAFRC operating_status 'Assume Sponsor Closed t')",
        "imputation_masked_candidate": "EIN stays in panel to FY2024 but its last filed DAF-asset value is FY t-1<=FY2022; later rows imputed",
        "zero_daf_assets_terminal": "EIN files Schedule D with zero DAF assets from FY t to FY2024 after a positive year",
    }.get(k, "")
    if measure.endswith("_count"):
        return f"count-weighted rate = exits/at_risk_n; exit = {what}"
    if measure.endswith("_asset_weighted"):
        return f"asset-weighted rate = exiting sponsors' last positive filed DAF assets / at_risk_assets; exit = {what}"
    if measure.endswith("_assets"):
        return f"sum of last positive filed eoy_daf_assets of exiting sponsors; exit = {what}"
    return f"count; exit = {what}"


# ---------------------------------------------------------------------------
# Verification evidence (IRS files, ProPublica API, e-file XML)
# ---------------------------------------------------------------------------
def load_bmf(irs_dir: str, eins: frozenset[str]) -> dict[str, dict]:
    paths = [os.path.join(irs_dir, f"eo{n}.csv") for n in (1, 2, 3, 4)]
    return {d["EIN"]: {**d, "_file": BMF_URL.format(n=i + 1)}
            for i, p in enumerate(paths) if os.path.exists(p)
            for d in csv.DictReader(open(p, newline="", encoding="latin-1")) if d["EIN"] in eins}


def load_revocations(irs_dir: str, eins: frozenset[str]) -> dict[str, dict]:
    p = os.path.join(irs_dir, "data-download-revocation.txt")
    if not os.path.exists(p):
        return {}
    cols = ("ein", "name", "dba", "street", "city", "state", "zip", "country",
            "exemption_type", "revocation_date", "posting_date", "reinstatement_date")
    with open(p, encoding="latin-1") as fh:
        recs = (dict(zip(cols, line.rstrip("\n").split("|"))) for line in fh if line[:9] in eins)
        return {r["ein"]: r for r in recs if r.get("ein") in eins}


def load_efile_index(irs_dir: str, eins: frozenset[str]) -> dict[str, tuple[dict, ...]]:
    paths = sorted(p for p in os.listdir(irs_dir) if re.fullmatch(r"index_\d{4}\.csv", p))
    recs = [{**d, "_index_url": INDEX_URL.format(y=p[6:10])}
            for p in paths for d in csv.DictReader(open(os.path.join(irs_dir, p), newline="", encoding="latin-1"))
            if d.get("EIN", "").zfill(9) in eins]
    by = defaultdict(list)
    for d in recs:
        by[d["EIN"].zfill(9)].append(d)
    return {e: tuple(sorted(v, key=lambda d: (d["TAX_PERIOD"], d["OBJECT_ID"]))) for e, v in by.items()}


def fetch_cached(url: str, path: str, fetch: bool, pause: float = 0.4) -> str | None:
    if os.path.exists(path):
        txt = open(path, encoding="utf-8-sig", errors="replace").read()
        return None if txt.startswith("__HTTP_") else txt
    if not fetch:
        return None
    req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            txt = resp.read().decode("utf-8-sig", errors="replace")
    except urllib.error.HTTPError as e:
        txt = f"__HTTP_{e.code}__"
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"fetch failed {url}: {e}", file=sys.stderr)
        return None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(txt)
    time.sleep(pause)
    return None if txt.startswith("__HTTP_") else txt


XML_TAGS = ("DonorAdvisedFundInd", "DonorAdvisedFundsHeldCnt", "DonorAdvisedFundsVlEOYAmt",
            "DonorAdvisedFundsGrantsAmt", "TotalAssetsEOYAmt", "TaxPeriodEndDt", "ReturnTypeCd",
            "TerminateOperationsInd", "PartialLiquidationInd", "FinalReturnInd",
            "DisposedOfMoreThan25PctInd", "SignificantDisposalInd", "DissolutionInd")


def parse_return_xml(txt: str | None) -> dict:
    if not txt:
        return {}
    first = {t: (re.search(rf"<{t}>([^<]*)</{t}>", txt) or [None, None])[1] for t in XML_TAGS}
    sched_n = re.findall(r"<IRS990ScheduleN\b.*?</IRS990ScheduleN>", txt, re.S)
    recips = re.findall(r"<BusinessNameLine1Txt>([^<]*)</BusinessNameLine1Txt>", sched_n[0]) if sched_n else []
    return {**first, "has_schedule_n": bool(sched_n), "schedule_n_recipients": "; ".join(dict.fromkeys(recips))}


def evidence_for(h: Mapping, bmf: Mapping, revoc: Mapping, idx: Mapping, pp: Mapping | None,
                 xml_later: Mapping, xml_last: Mapping, successor: str = "") -> dict:
    """Combine evidence and assign a rule-based outcome. Pure."""
    e = h["ein"]
    b, rv, filings = bmf.get(e), revoc.get(e), idx.get(e, ())
    ref_period = (h["last_filed_period_end"] or f"{h['last_filed_fy'] or h['last_fy']}-12-31").replace("-", "")[:6]
    later = tuple(f for f in filings if f["TAX_PERIOD"] > ref_period)
    latest = later[-1] if later else None
    pp_org = (pp or {}).get("organization") or {}
    pp_periods = sorted({str(f.get("tax_prd")) for k in ("filings_with_data", "filings_without_data")
                         for f in (pp or {}).get(k, []) if f.get("tax_prd")})
    pp_later = [p for p in pp_periods if p > ref_period]
    daf_cnt = num(xml_later.get("DonorAdvisedFundsHeldCnt"))
    daf_val = num(xml_later.get("DonorAdvisedFundsVlEOYAmt"))
    daf_later = (daf_cnt or 0) > 0 or (daf_val or 0) > 0
    acct_pd = (b or {}).get("ACCT_PD", "")
    last_month = (h["last_filed_period_end"] or "")[5:7]
    fy_change = bool(b and acct_pd and last_month and acct_pd.zfill(2) != last_month)
    terminated_flag = (xml_last.get("TerminateOperationsInd") in ("1", "true")
                       or xml_later.get("TerminateOperationsInd") in ("1", "true"))
    manual = MANUAL_EVIDENCE.get(e, {})
    if manual.get("outcome"):
        outcome = manual["outcome"]
    elif rv and not rv.get("reinstatement_date", "").strip():
        outcome = "revoked_auto_nonfiling"
    elif terminated_flag:
        outcome = "terminated_final_return"
    elif not b:
        outcome = "removed_from_irs_bmf_terminated_or_merged"
    elif latest and latest["RETURN_TYPE"] in ("990EZ", "990PF", "990N"):
        outcome = f"form_change_to_{latest['RETURN_TYPE']}_no_schedule_d_daf_data"
    elif latest and latest["RETURN_TYPE"] == "990" and xml_later and daf_later:
        outcome = "reporting_artifact_later_990_reports_dafs"
    elif latest and latest["RETURN_TYPE"] == "990" and xml_later:
        outcome = "stopped_reporting_dafs_org_still_files_990"
    elif latest:
        outcome = "later_return_filed_daf_status_unknown"
    elif pp_later:
        outcome = "later_paper_or_unparsed_return_daf_status_unknown"
    else:
        outcome = "unresolved_in_bmf_no_later_return_found"
    true_exit = outcome in ("revoked_auto_nonfiling", "terminated_final_return",
                            "removed_from_irs_bmf_terminated_or_merged",
                            "stopped_reporting_dafs_org_still_files_990", "merged_daf_assets_transferred")
    artifact = outcome.startswith("reporting_artifact")
    src = [PP_API.format(ein=e)] if pp is not None else []
    src += [BMF_URL.format(n="1-4")] + ([REVOC_URL] if rv else [])
    src += [latest["_index_url"]] if latest else []
    src += [XML_URL.format(oid=latest["OBJECT_ID"])] if latest and xml_later else []
    src += [manual["source_url"]] if manual.get("source_url") else []
    return {
        "ein": e, "name": h["name"], "type": h["type"], "subtype": h["subtype"],
        "exit_kind": h["exit_kind"], "exit_fy": h["exit_fy"], "dafrc_operating_status": h["operating_status"],
        "last_filed_fy": h["last_filed_fy"], "last_filed_period_end": h["last_filed_period_end"],
        "exit_ref_fy": h["exit_ref_fy"], "exit_ref_daf_assets": h["exit_ref_assets"],
        "exit_ref_daf_accounts": h["exit_ref_accounts"], "exit_size_band": h["exit_size_band"],
        "in_irs_bmf_2026": bool(b), "bmf_status": (b or {}).get("STATUS", ""),
        "bmf_latest_tax_period": (b or {}).get("TAX_PERIOD", ""), "bmf_filing_req_cd": (b or {}).get("FILING_REQ_CD", ""),
        "bmf_acct_pd": acct_pd, "bmf_foundation_cd": (b or {}).get("FOUNDATION", ""),
        "fiscal_year_change_flag": fy_change or h["fiscal_month_changed"],
        "irs_revocation_date": (rv or {}).get("revocation_date", ""),
        "irs_revocation_posting_date": (rv or {}).get("posting_date", ""),
        "irs_reinstatement_date": (rv or {}).get("reinstatement_date", "").strip(),
        "efile_returns_after_last_filed": len(later),
        "latest_later_efile_period": latest["TAX_PERIOD"] if latest else "",
        "latest_later_efile_type": latest["RETURN_TYPE"] if latest else "",
        "latest_later_efile_object_id": latest["OBJECT_ID"] if latest else "",
        "later_990_daf_accounts": xml_later.get("DonorAdvisedFundsHeldCnt") or "",
        "later_990_daf_assets_eoy": xml_later.get("DonorAdvisedFundsVlEOYAmt") or "",
        "later_990_daf_ind": xml_later.get("DonorAdvisedFundInd") or "",
        "terminate_operations_ind": "1" if terminated_flag else "",
        "schedule_n_recipients": xml_later.get("schedule_n_recipients") or xml_last.get("schedule_n_recipients") or "",
        "propublica_checked": pp is not None, "propublica_found": bool(pp_org),
        "propublica_latest_tax_prd": pp_periods[-1] if pp_periods else "",
        "propublica_periods_after_last_filed": ";".join(pp_later),
        "outcome": outcome, "true_exit": true_exit, "reporting_artifact": artifact,
        "possible_successor_ein": successor,
        "manual_note": manual.get("note", ""),
        "source_urls": " ; ".join(dict.fromkeys(src + [PP_ORG.format(ein=e), DAFRC_URL])),
    }


def draw_sample(cands: Sequence[Mapping]) -> dict[str, str]:
    """Top-N by exit-reference assets plus a seeded random draw of the rest. Pure."""
    ranked = sorted(cands, key=lambda h: -(h["exit_ref_assets"] or 0))
    top = [h["ein"] for h in ranked[:SAMPLE_TOP]]
    rest = sorted(h["ein"] for h in ranked[SAMPLE_TOP:])
    rnd = random.Random(SAMPLE_SEED).sample(rest, min(SAMPLE_RANDOM, len(rest)))
    return {**{e: "top25_by_assets" for e in top}, **{e: "random25" for e in rnd}}


def verified_bounds(ver: Sequence[Mapping], hists: Mapping[str, Mapping],
                    by_ein: Mapping[str, Sequence[Row]]) -> list[dict]:
    """Annualised exit-rate bounds over FY2020-FY2023 exposure, count- and asset-weighted."""
    years = range(FIRST_FY + 1, LAST_FY)  # exits observable FY2020..FY2023
    row_at = {(e, r.fy): r for e, rs in by_ein.items() for r in rs}
    exposure_n = sum(1 for t in years for e in by_ein if (e, t - 1) in row_at)
    exposure_a = sum((row_at[(e, t - 1)].assets or 0) for t in years for e in by_ein if (e, t - 1) in row_at)
    in_window = [v for v in ver if v["exit_fy"] and FIRST_FY < int(v["exit_fy"]) < LAST_FY]
    sampled = [v for v in in_window if v["sample_stratum"]]
    sets = {
        "lower_verified_true_exits_all_candidates": [v for v in in_window if v["true_exit"]],
        "upper_true_plus_unresolved_plus_form_change": [v for v in in_window if not v["reporting_artifact"]],
        "naive_panel_exits_only": [v for v in in_window if v["exit_kind"] == "panel_exit"],
        "naive_all_candidates": in_window,
    }
    out = []
    for label, s in sets.items():
        n = len(s)
        a = sum(num(fmt(v["exit_ref_daf_assets"])) or 0 for v in s)
        out += [
            {"dimension": "verified", "group": label, "fiscal_year": "2020-2023", "measure": "annual_exit_rate_count",
             "value": safe_div(n, exposure_n), "numerator": n, "denominator": exposure_n,
             "definition": "exits dated FY2020-FY2023 / sponsor-years at risk (rows in FY2019-FY2022)"},
            {"dimension": "verified", "group": label, "fiscal_year": "2020-2023", "measure": "annual_exit_rate_asset_weighted",
             "value": safe_div(a, exposure_a), "numerator": a, "denominator": exposure_a,
             "definition": "last positive filed DAF assets of exits / sum of prior-year DAF assets at risk"},
        ]
    out.append({"dimension": "verified", "group": "sample_outcomes", "fiscal_year": "2020-2024",
                "measure": "sampled_candidates_n", "value": len([v for v in ver if v["sample_stratum"]]),
                "numerator": None, "denominator": None,
                "definition": "exit candidates in the top-25 + random-25 verification sample"})
    out += [{"dimension": "verified_outcome", "group": k, "fiscal_year": "all", "measure": "candidates_n",
             "value": c, "numerator": None, "denominator": len(ver), "definition": "rule-based outcome, all exit candidates"}
            for k, c in sorted(Counter(v["outcome"] for v in ver).items())]
    out += [{"dimension": "verified_outcome_sample", "group": k, "fiscal_year": "all", "measure": "candidates_n",
             "value": c, "numerator": None, "denominator": len(sampled),
             "definition": "rule-based outcome, sampled candidates with exit FY2020-FY2023"}
            for k, c in sorted(Counter(v["outcome"] for v in sampled).items())]
    return out


# ---------------------------------------------------------------------------
# I/O edges
# ---------------------------------------------------------------------------
def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows({k: fmt(r.get(k)) if not isinstance(r.get(k), tuple) else ";".join(map(str, r[k]))
                     for k in fields} for r in rows)


STOPWORDS = frozenset({"INC", "THE", "OF", "FOR", "AND", "CORP", "CORPORATION", "FUND", "FOUNDATION", "TRUST", "CO"})


def norm_name(name: str) -> str:
    toks = re.sub(r"[^A-Z0-9 ]", " ", name.upper()).split()
    return " ".join(t for t in toks if t not in STOPWORDS)


def successor_links(hists: Mapping[str, Mapping], threshold: float = 0.82) -> dict[str, str]:
    """Exit candidate EIN -> 'EIN|name|first_fy' of a *different* EIN with a near-identical
    name that appears in the panel no later than the exit year (possible re-EIN / merger). Pure."""
    exits = [h for h in hists.values() if h["exit_kind"] in EXIT_KINDS]
    others = list(hists.values())

    def match(h):
        n = norm_name(h["name"])
        hits = [o for o in others if o["ein"] != h["ein"] and n and
                SequenceMatcher(None, n, norm_name(o["name"])).ratio() >= threshold and
                o["last_fy"] >= (h["exit_fy"] or LAST_FY)]
        return "; ".join(f"{o['ein']}|{o['name']}|first_fy={o['first_fy']}" for o in hits)

    return {h["ein"]: m for h in exits if (m := match(h))}


def entrant_rows(hists: Mapping[str, Mapping], bmf: Mapping[str, Mapping], links: Mapping[str, str]) -> list[dict]:
    """Classify each entrant (first panel FY > 2019) by IRS ruling year. Pure."""
    succ_targets = {t.split("|")[0]: src for src, v in links.items() for t in v.split("; ")}

    def cls(h):
        b = bmf.get(h["ein"])
        ruling = int(b["RULING"][:4]) if b and b.get("RULING", "")[:4].isdigit() else None
        if h["ein"] in succ_targets:
            c = "possible_successor_ein_of_exiting_sponsor"
        elif ruling is None:
            c = "unknown_not_in_bmf"
        elif ruling >= h["entry_fy"] - 1:
            c = "new_organization_ruling_within_1y"
        else:
            c = "existing_organization_new_to_panel"
        return {"ein": h["ein"], "name": h["name"], "type": h["type"], "subtype": h["subtype"],
                "entry_fy": h["entry_fy"], "irs_ruling": (b or {}).get("RULING", ""), "entry_class": c,
                "predecessor_ein": succ_targets.get(h["ein"], "")}

    return [cls(h) for h in hists.values() if h["entry_fy"]]


def run_verification(hists, by_ein, irs_dir, cache_dir, fetch) -> list[dict]:
    cands = [h for h in hists.values() if h["exit_kind"] in EXIT_KINDS]
    eins = frozenset(h["ein"] for h in cands)
    bmf, revoc, idx = load_bmf(irs_dir, eins), load_revocations(irs_dir, eins), load_efile_index(irs_dir, eins)
    sample = draw_sample(cands)
    links = successor_links(hists)

    def ref_period(h):
        return (h["last_filed_period_end"] or f"{h['last_filed_fy'] or h['last_fy']}-12-31").replace("-", "")[:6]

    def xml_for(f):
        return parse_return_xml(fetch_cached(XML_URL.format(oid=f["OBJECT_ID"]),
                                             os.path.join(cache_dir, "xml", f"{f['OBJECT_ID']}.xml"), fetch)) if f else {}

    def one(h):
        e = h["ein"]
        filings = idx.get(e, ())
        later = [f for f in filings if f["TAX_PERIOD"] > ref_period(h) and f["RETURN_TYPE"] == "990"]
        last_any = filings[-1] if filings else None
        pp_txt = fetch_cached(PP_API.format(ein=e), os.path.join(cache_dir, "propublica", f"{e}.json"),
                              fetch) if e in sample else None
        pp = json.loads(pp_txt) if pp_txt else ({} if e in sample and fetch else None)
        ev = evidence_for(h, bmf, revoc, idx, pp, xml_for(later[-1] if later else None), xml_for(last_any),
                         links.get(e, ""))
        return {**ev, "sample_stratum": sample.get(e, "")}

    return sorted((one(h) for h in cands), key=lambda v: (v["sample_stratum"] == "", -(v["exit_ref_daf_assets"] or 0)))


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data-dir", default=DATA_DIR_DEFAULT)
    ap.add_argument("--irs-dir", help="dir with eo1-4.csv, data-download-revocation.txt, index_YYYY.csv")
    ap.add_argument("--cache-dir", default=os.path.expanduser("~/.cache/daf-landscape"))
    ap.add_argument("--fetch", action="store_true", help="download missing ProPublica JSON / 990 XML")
    a = ap.parse_args(argv)
    with open(os.path.join(a.data_dir, PANEL_IN), newline="", encoding="utf-8") as fh:
        rows = tuple(to_row(d) for d in csv.DictReader(fh))
    by_ein = group_by_ein(rows)
    hists = {e: sponsor_history(rs) for e, rs in by_ein.items()}
    panel = [p for e, rs in by_ein.items() for p in panel_rows(rs, hists[e])]
    write_csv(os.path.join(a.data_dir, PANEL_OUT), panel, list(panel[0].keys()))
    summ = summary_rows(by_ein, hists)
    ver: list[dict] = []
    if a.irs_dir:
        ver = run_verification(hists, by_ein, a.irs_dir, a.cache_dir, a.fetch)
        write_csv(os.path.join(a.data_dir, VERIFY_OUT), ver, ["sample_stratum"] + [k for k in ver[0] if k != "sample_stratum"])
        ent = entrant_rows(hists, load_bmf(a.irs_dir, frozenset(h["ein"] for h in hists.values() if h["entry_fy"])),
                           successor_links(hists))
        summ = summ + verified_bounds(ver, hists, by_ein) + [
            {"dimension": "entrant_class", "group": c, "fiscal_year": fy, "measure": "entries_n", "value": n,
             "numerator": None, "denominator": None,
             "definition": "entrants classified by IRS BMF ruling year and name-match to an exiting EIN"}
            for (fy, c), n in sorted(Counter((r["entry_fy"], r["entry_class"]) for r in ent).items())]
        print(f"entrant classes={dict(Counter(r['entry_class'] for r in ent))}")
    write_csv(os.path.join(a.data_dir, SUMMARY_OUT), summ,
              ["dimension", "group", "fiscal_year", "measure", "value", "numerator", "denominator", "definition"])
    kinds = Counter(h["exit_kind"] or "survivor_or_censored" for h in hists.values())
    entries = Counter(h["entry_fy"] for h in hists.values() if h["entry_fy"])
    print(f"EINs={len(hists)} rows={len(rows)} entries_by_fy={dict(sorted(entries.items()))}")
    print(f"exit kinds={dict(kinds)}")
    if ver:
        print(f"verification candidates={len(ver)} sampled={sum(1 for v in ver if v['sample_stratum'])}")
        print(f"outcomes={dict(Counter(v['outcome'] for v in ver))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
