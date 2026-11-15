#!/usr/bin/env python3
"""Queue batch 36 A: DAF account metric on an 'ongoing advisory privilege' basis (P-B35A-01), carry-forward
replacement of DAFRC 'closed' flags and imputations for line-6-Yes / Part I blank returns (P-B33A-02), and two
dated panels of published grant-rail statements (P-B35C-03 electronic-vs-check shares; P-PAY-05 latency).

Stdlib only; functional style (pure transforms, I/O at the edges).

Task `accounts` (P-B35A-01 + P-B33A-02) -> data/mission-2026-11-14/dafrc-market-accounts-restated.csv
  Inputs: DAFRC 2025 panel (dafrc-sponsor-schedule-d-fy2019-2024.csv) + applied rules R1-R4
  (dafrc-corrections-itemized.csv) -> corrected sponsor-year values; the sums are checked against
  dafrc-corrected-market-totals.csv. blank-schedule-d-panel.csv (batch 33) for P-B33A-02. Filed XML (GivingTuesday
  mirror of IRS TEOS) for the processors' Schedule D columns and narrative; IRS index_2026.csv for the TY2025 check.

  Account rules (an account counts when its donor/adviser holds ongoing advisory privileges, IRC 4966(d)(2)(A)(iii)):
    A1 (central; filed reclassification) a sponsor whose own filing moves accounts out of the Schedule D DAF column
       because donors recommend "at or near the time of donation, without ongoing advisory privileges" is restated
       to its post-reclassification basis in every FY. Only AOGF qualifies (FYE 2026-03 return). Accounts -> its
       FYE 2026 DAF-column count (695, constant proxy); grants and EOY value scaled by the FYE 2026 DAF-column share
       of (DAF + other-funds) grants and EOY value. Scenario, not filed values for FY2021-24.
    A2 (upper; named micro-account processors) A1, plus Givinga and PPGF accounts set to 0. Accounts only:
       their grants and balances are real DAF-column money under their own filings and stay in.
    A3 (sensitivity; size screen) A1, plus accounts set to 0 for every sponsor-year with >= SCREEN_MIN_ACCTS
       accounts and average EOY DAF value per account < SCREEN_MAX_AVG. Accounts only.
  Blank-return rules (P-B33A-02), FY2021-24 rows of blank-schedule-d-panel.csv:
    B1 (carry-forward) 'dafrc_no_row_sponsor_closed' / 'dafrc_row_value_blank' -> add the sponsor's last filed DAF
       count and EOY value; 'dafrc_row_imputed' -> replace DAFRC's imputed count/value with the last filed ones.
       A sponsor-year whose corrected value already comes from an applied R1-R4 row is left alone.
    B2 (interpolated) as B1, but linear interpolation by fiscal year between the last and next filed values when
       both exist (carry-forward otherwise).
    C1 = A1 + B1.

Task `rails` -> grant-rail-shares-panel-2026.csv and grant-latency-statements-2026.csv
  Observations are transcribed from public pages fetched 2026-11-15 (robots.txt read first; URL and verbatim quote
  in each row). The script derives check shares, implied counts and day ranges; it adds no figures of its own.

Usage:
  python3 scripts/mission_account_metric.py accounts --work-dir WORK --index IRS/index_2026.csv [--fetch]
  python3 scripts/mission_account_metric.py rails
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402

FYS = (2021, 2022, 2023, 2024)
CORR_ITEMS = os.path.join(DATA, "dafrc-corrections-itemized.csv")
CORR_TOTALS = os.path.join(DATA, "dafrc-corrected-market-totals.csv")
BLANK = os.path.join(DATA, "blank-schedule-d-panel.csv")
OUT_ACCTS = os.path.join(DATA, "dafrc-market-accounts-restated.csv")
OUT_SHARES = os.path.join(DATA, "grant-rail-shares-panel-2026.csv")
OUT_LAT = os.path.join(DATA, "grant-latency-statements-2026.csv")
MIRROR = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
DAFRC_URL = "https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx"

METRIC_COL = {"daf_accounts_eoy": "number_of_daf_accounts", "daf_assets_eoy": "eoy_daf_assets",
              "daf_grants": "total_daf_grants"}
AOGF, GIVINGA, PPGF = "810739440", "474172718", "450931286"
SCREEN_MIN_ACCTS, SCREEN_MAX_AVG = 5000, 500.0
FILED = frozenset({"IRS 990", "NPT historical data", "paper submission"})

# Returns read for the processor evidence (latest submission per period, per batch 35 / harvest).
PROCESSOR_RETURNS = (
    (AOGF, "AOGF FYE 2026-03", "202642259349301349"),
    (AOGF, "AOGF FYE 2025-03 (amended)", "202641969349302754"),
    (PPGF, "PPGF CY2024", "202533079349301308"),
    (GIVINGA, "Givinga CY2024 (amended)", "202503179349301975"),
    ("262449481", "Give Back Foundation CY2025", "202631669349300818"),
    ("460942102", "Blackbaud Giving Fund CY2025", "202622529349301602"),
    ("680480736", "Network for Good CY2024", "202513039349301631"),
    ("455634144", "Philanthropi CY2024", "202523219349326042"),
)
# Sponsors whose TY2025 return the queue asks to re-read (EIN or name pattern for the index check).
TY2025_TARGETS = (("PPGF", PPGF), ("Givinga", GIVINGA), ("Network for Good", "680480736"),
                  ("Blackbaud Giving Fund", "460942102"), ("Bright Funds", "BRIGHT FUNDS"))
SCHED_D_TAGS = ("DonorAdvisedFundsHeldCnt", "FundsAndOtherAccountsHeldCnt", "DonorAdvisedFundsGrantsAmt",
                "FundsAndOtherAccountsGrantsAmt", "DonorAdvisedFundsVlEOYAmt", "FundsAndOtherAccountsVlEOYAmt",
                "TaxPeriodEndDt")
TEXT_RX = re.compile(r"ADVISORY PRIVILEGE|MICRO-DONATION|AT OR NEAR THE TIME OF DONATION|SHOULD NOT BE TREATED"
                     r"|DONOR ADVISED FUNDS? SHOULD|ACCOUNT HOLDERS|DIRECT THE FUNDS FROM THEIR ACCOUNT", re.I)


# ----------------------------------------------------------------------------- I/O edges
def fetch_xml(oid: str, work: str, fetch: bool) -> str:
    path = os.path.join(work, "xml", f"{oid}.xml")
    if not os.path.exists(path):
        if not fetch:
            raise SystemExit(f"missing {path}; rerun with --fetch")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with urllib.request.urlopen(MIRROR.format(oid=oid), timeout=180) as r, open(path, "wb") as fh:
            fh.write(r.read())
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def index_hits(path: str, targets: Sequence[tuple[str, str]]) -> dict:
    """label -> tuple of index rows (EIN match, or taxpayer-name substring when the key is not numeric)."""
    rows = read_csv(path)
    def hit(key: str, r: Mapping) -> bool:
        return r["EIN"].zfill(9) == key if key.isdigit() else key in (r["TAXPAYER_NAME"] or "").upper()
    return {lab: tuple(r for r in rows if hit(key, r)) for lab, key in targets}


# ----------------------------------------------------------------------------- pure transforms
def sched_d(xml: str) -> dict:
    def tag(t: str):
        m = re.search(rf"<{t}>([^<]*)<", xml)
        return (m.group(1) if t.endswith("Dt") else num(m.group(1))) if m else None
    return {t: tag(t) for t in SCHED_D_TAGS}


def daf_text(xml: str) -> tuple[str, ...]:
    """Distinct narrative passages (Part III / VI / Schedule O) with account-basis wording, truncated."""
    seen, out = set(), []
    for m in re.finditer(r"<(\w*(?:Txt|Desc))>([^<]{40,8000})<", xml):
        s = m.group(2)
        if TEXT_RX.search(s) and s[:80] not in seen:
            seen.add(s[:80])
            out.append(s[:700])
    return tuple(out)


def corrected(dafrc: Sequence[Mapping], items: Sequence[Mapping]) -> tuple[dict, dict, dict]:
    """(values, names, overridden): (ein, fy, metric) -> corrected value; ein -> name; keys overridden by R1-R4."""
    base = {(ein9(r["ein"]), int(r["fiscal_year_end"]), m): num(r[c]) or 0.0
            for r in dafrc if int(r["fiscal_year_end"]) in FYS for m, c in METRIC_COL.items()}
    over = {(ein9(r["ein"]), int(r["fiscal_year"]), r["metric"]): num(r["corrected_value"]) or 0.0
            for r in items if r["applied"] == "1" and r["metric"] in METRIC_COL and int(r["fiscal_year"]) in FYS}
    names = {ein9(r["ein"]): r["name"] for r in dafrc}
    return {**base, **over}, names, frozenset(over)


def totals(vals: Mapping) -> dict:
    acc: dict = {}
    for (e, fy, m), v in vals.items():
        acc[(fy, m)] = acc.get((fy, m), 0.0) + v
    return acc


def check_totals(t: Mapping, published: Sequence[Mapping]) -> tuple[dict, ...]:
    ref = {(int(r["fiscal_year"]), r["metric"]): num(r["corrected_value"]) for r in published}
    return tuple({"fy": fy, "metric": m, "rebuilt": t.get((fy, m)), "published": ref.get((fy, m)),
                  "diff": (t.get((fy, m)) or 0) - (ref.get((fy, m)) or 0)} for fy in FYS for m in METRIC_COL)


def adj(e: str, fy: int, m: str, new: float, vals: Mapping, rule: str, note: str) -> dict:
    old = vals.get((e, fy, m), 0.0)
    return {"ein": e, "fy": fy, "metric": m, "old": old, "new": new, "delta": new - old, "rule": rule, "note": note}


def rule_a1(vals: Mapping, aogf26: Mapping) -> tuple[dict, ...]:
    d = aogf26
    g_share = d["DonorAdvisedFundsGrantsAmt"] / (d["DonorAdvisedFundsGrantsAmt"] + d["FundsAndOtherAccountsGrantsAmt"])
    v_share = d["DonorAdvisedFundsVlEOYAmt"] / (d["DonorAdvisedFundsVlEOYAmt"] + d["FundsAndOtherAccountsVlEOYAmt"])
    note = (f"AOGF FYE 2026-03 basis: DAF-column accounts {int(d['DonorAdvisedFundsHeldCnt'])}; DAF share of grants "
            f"{g_share:.4f}, of EOY value {v_share:.4f}")
    return tuple(a for fy in FYS if (AOGF, fy, "daf_accounts_eoy") in vals for a in (
        adj(AOGF, fy, "daf_accounts_eoy", d["DonorAdvisedFundsHeldCnt"], vals, "A1", note),
        adj(AOGF, fy, "daf_grants", vals[(AOGF, fy, "daf_grants")] * g_share, vals, "A1", note),
        adj(AOGF, fy, "daf_assets_eoy", vals[(AOGF, fy, "daf_assets_eoy")] * v_share, vals, "A1", note)))


def rule_a2(vals: Mapping) -> tuple[dict, ...]:
    return tuple(adj(e, fy, "daf_accounts_eoy", 0.0, vals, "A2", "named micro-account processor: accounts excluded")
                 for e in (GIVINGA, PPGF) for fy in FYS if (e, fy, "daf_accounts_eoy") in vals)


def rule_a3(vals: Mapping) -> tuple[dict, ...]:
    keys = sorted({(e, fy) for (e, fy, m) in vals if e != AOGF})
    def flagged(e, fy):
        n, a = vals.get((e, fy, "daf_accounts_eoy"), 0.0), vals.get((e, fy, "daf_assets_eoy"), 0.0)
        return n >= SCREEN_MIN_ACCTS and a / n < SCREEN_MAX_AVG
    return tuple(adj(e, fy, "daf_accounts_eoy", 0.0, vals, "A3",
                     f"screen: {int(vals[(e, fy, 'daf_accounts_eoy')])} accounts, avg EOY "
                     f"${vals[(e, fy, 'daf_assets_eoy')] / vals[(e, fy, 'daf_accounts_eoy')]:.0f}")
                 for e, fy in keys if flagged(e, fy))


def interp(fy: int, p_fy: int | None, p_v: float | None, n_fy: int | None, n_v: float | None) -> float | None:
    if p_v is None:
        return None
    if n_v is None or n_fy is None or p_fy is None or n_fy <= p_fy:
        return p_v
    return p_v + (n_v - p_v) * (fy - p_fy) / (n_fy - p_fy)


def fy_of(period: str) -> int | None:
    return int(period[:4]) if period else None


def last_filed_counts(dafrc: Sequence[Mapping]) -> dict:
    """ein -> tuple of (fy, accounts) from DAFRC rows whose account count is filed (not imputed), any FY."""
    rows = [(ein9(r["ein"]), int(r["fiscal_year_end"]), num(r["number_of_daf_accounts"])) for r in dafrc
            if r["source_number_of_accounts"] in FILED and num(r["number_of_daf_accounts"]) is not None]
    return {e: tuple(sorted((fy, n) for _, fy, n in rs)) for e, rs in _group_by_fast(rows, lambda t: t[0]).items()}


def count_before(lfc: Mapping, e: str, fy: int) -> tuple[int | None, float | None]:
    prior = [(f, n) for f, n in lfc.get(e, ()) if f < fy]
    return prior[-1] if prior else (None, None)


def rule_b(vals: Mapping, overridden: frozenset, blank: Sequence[Mapping], mode: str,
           lfc: Mapping | None = None) -> tuple[dict, ...]:
    """B1 (carry) / B2 (interp). One adjustment per (sponsor-year, metric) in accounts and assets.
    The prior count falls back to DAFRC's last filed (non-imputed) count when the 990 extract has none."""
    out = []
    for r in blank:
        fy, e, treat = int(r["fiscal_year"]), ein9(r["ein"]), r["dafrc_treatment"]
        if fy not in FYS or treat not in ("dafrc_no_row_sponsor_closed", "dafrc_row_imputed", "dafrc_row_value_blank"):
            continue
        p_fy, n_fy = fy_of(r["prior_reported_period"]), fy_of(r["next_reported_period"])
        p_val = num(r["prior_reported_daf_eoy"])
        p_val = p_val if p_val is not None else num(r["dafrc_last_filed_daf_assets_before"])
        p_cnt, c_fy = num(r["prior_reported_daf_count"]), p_fy
        if p_cnt is None:
            c_fy, p_cnt = count_before(lfc or {}, e, fy)
        v_fy = p_fy if num(r["prior_reported_daf_eoy"]) is not None else fy_of(r["dafrc_last_filed_fy_before"])
        for m, p, n, pf in (("daf_accounts_eoy", p_cnt, num(r["next_reported_daf_count"]), c_fy),
                            ("daf_assets_eoy", p_val, num(r["next_reported_daf_eoy"]), v_fy)):
            if (e, fy, m) in overridden:
                continue
            new = p if mode == "carry" else interp(fy, pf, p, n_fy, n)
            if new is None:
                continue
            new = float(round(new)) if m == "daf_accounts_eoy" else new
            note = (f"{treat}; blank_kind={r['blank_kind']}; last filed "
                    f"{r['prior_reported_period'] or (f'FY{pf} (DAFRC filed row)' if pf else 'n/a')}"
                    + (f"; next filed {r['next_reported_period']}" if r["next_reported_period"] else ""))
            out.append(adj(e, fy, m, new, vals, "B1" if mode == "carry" else "B2", note))
    return tuple(out)


def apply(vals: Mapping, adjs: Sequence[Mapping]) -> dict:
    return {**vals, **{(a["ein"], a["fy"], a["metric"]): a["new"] for a in adjs}}


VARIANTS = {
    "V0_corrected": ("", "corrected DAFRC totals (rules R1-R4), as in dafrc-corrected-market-totals.csv"),
    "A1_advisory_filed_basis": ("A1", "central P-B35A-01: AOGF restated to its FYE 2026 filed DAF-column basis"),
    "A2_named_processors_excluded": ("A1+A2", "upper: A1 plus Givinga and PPGF accounts excluded (accounts only)"),
    "A3_small_balance_screen": ("A1+A3", f"sensitivity: A1 plus sponsor-years with >= {SCREEN_MIN_ACCTS} accounts and "
                                f"avg EOY < ${SCREEN_MAX_AVG:.0f} excluded (accounts only)"),
    "B1_blank_carry_forward": ("B1", "P-B33A-02: closed flags and imputations replaced by last filed values"),
    "B2_blank_interpolated": ("B2", "P-B33A-02 alternative: interpolation where a later filed value exists"),
    "C1_advisory_plus_blank_cf": ("A1+B1", "A1 and B1 combined"),
}


def variant_adjs(vals, overridden, blank, aogf26, lfc) -> dict:
    a1, a2, a3 = rule_a1(vals, aogf26), rule_a2(vals), rule_a3(vals)
    b1, b2 = rule_b(vals, overridden, blank, "carry", lfc), rule_b(vals, overridden, blank, "interp", lfc)
    return {"V0_corrected": (), "A1_advisory_filed_basis": a1, "A2_named_processors_excluded": a1 + a2,
            "A3_small_balance_screen": a1 + a3, "B1_blank_carry_forward": b1, "B2_blank_interpolated": b2,
            "C1_advisory_plus_blank_cf": a1 + b1}


def whole(x, m: str = ""):
    """Integers for money and counts (write_csv's %.6g would truncate them); averages in whole dollars."""
    return None if x is None else int(round(x))


def total_rows(vals: Mapping, by_variant: Mapping) -> list[dict]:
    base = totals(vals)
    rows = []
    for v, adjs in by_variant.items():
        t = totals(apply(vals, adjs))
        for fy in FYS:
            for m in (*METRIC_COL, "avg_assets_per_account"):
                val = (t[(fy, "daf_assets_eoy")] / t[(fy, "daf_accounts_eoy")] if m == "avg_assets_per_account"
                       else t[(fy, m)])
                ref = (base[(fy, "daf_assets_eoy")] / base[(fy, "daf_accounts_eoy")] if m == "avg_assets_per_account"
                       else base[(fy, m)])
                hit = [a for a in adjs if a["fy"] == fy and (a["metric"] == m or m == "avg_assets_per_account")]
                rows.append({"row_type": "total", "fiscal_year": fy, "variant": v, "rules": VARIANTS[v][0],
                             "metric": m, "value": whole(val, m), "corrected_value": whole(ref, m),
                             "delta": whole(val - ref, m),
                             "delta_pct": (val - ref) / ref if ref else None,
                             "sponsors_adjusted": len({a["ein"] for a in hit}), "variant_description": VARIANTS[v][1]})
    return rows


def adj_rows(by_variant: Mapping, names: Mapping, blank: Sequence[Mapping]) -> list[dict]:
    bname = {ein9(r["ein"]): r["sponsor_name"] for r in blank}
    seen, rows = set(), []
    for v in ("A1_advisory_filed_basis", "A2_named_processors_excluded", "A3_small_balance_screen",
              "B1_blank_carry_forward", "B2_blank_interpolated"):
        for a in by_variant[v]:
            k = (a["rule"], a["ein"], a["fy"], a["metric"])
            if k in seen:
                continue
            seen.add(k)
            rows.append({"row_type": "adjustment", "fiscal_year": a["fy"], "variant": v, "rules": a["rule"],
                         "metric": a["metric"], "ein": a["ein"], "sponsor_name": names.get(a["ein"]) or bname.get(a["ein"], ""),
                         "value": whole(a["new"]), "corrected_value": whole(a["old"]), "delta": whole(a["delta"]),
                         "delta_pct": a["delta"] / a["old"] if a["old"] else None, "note": a["note"]})
    return rows


ACCT_FIELDS = ("row_type", "fiscal_year", "variant", "rules", "metric", "ein", "sponsor_name", "value",
               "corrected_value", "delta", "delta_pct", "sponsors_adjusted", "variant_description", "note", "sources")
ACCT_SOURCES = (f"{DAFRC_URL} ; data/mission-2026-11-14/dafrc-corrections-itemized.csv ; "
                "data/mission-2026-11-14/blank-schedule-d-panel.csv ; " + MIRROR.format(oid="202642259349301349"))


def run_accounts(args) -> dict:
    dafrc = read_csv(DAFRC_CSV)
    vals, names, overridden = corrected(dafrc, read_csv(CORR_ITEMS))
    check = check_totals(totals(vals), read_csv(CORR_TOTALS))
    evidence = {lab: {"ein": e, "object_id": oid, "url": MIRROR.format(oid=oid), **sched_d(x), "text": daf_text(x)}
                for e, lab, oid in PROCESSOR_RETURNS for x in (fetch_xml(oid, args.work_dir, args.fetch),)}
    aogf26 = evidence["AOGF FYE 2026-03"]
    blank = read_csv(BLANK)
    by_variant = variant_adjs(vals, overridden, blank, aogf26, last_filed_counts(dafrc))
    rows = total_rows(vals, by_variant) + adj_rows(by_variant, names, blank)
    write_csv(OUT_ACCTS, [{**r, "sources": ACCT_SOURCES} for r in rows], ACCT_FIELDS)
    idx = index_hits(args.index, TY2025_TARGETS) if args.index else {}
    tot = {(r["variant"], r["fiscal_year"], r["metric"]): r["value"] for r in rows if r["row_type"] == "total"}
    b1 = by_variant["B1_blank_carry_forward"]
    return {
        "rebuild_check_max_abs_diff": max(abs(c["diff"]) for c in check),
        "totals": {f"{v}|{fy}": {m: round(tot[(v, fy, m)], 2) for m in (*METRIC_COL, "avg_assets_per_account")}
                   for v in VARIANTS for fy in FYS},
        "a3_hits": sorted({(a["ein"], names.get(a["ein"], ""), a["fy"], int(a["old"]))
                           for a in by_variant["A3_small_balance_screen"] if a["rule"] == "A3"}),
        "b1_counts": {fy: {"closed_added": sum(1 for a in b1 if a["fy"] == fy and a["metric"] == "daf_assets_eoy" and a["old"] == 0),
                           "imputed_replaced": sum(1 for a in b1 if a["fy"] == fy and a["metric"] == "daf_assets_eoy" and a["old"] != 0)}
                      for fy in FYS},
        "b1_largest": sorted(({"ein": a["ein"], "fy": a["fy"], "delta": round(a["delta"])} for a in b1
                              if a["metric"] == "daf_assets_eoy"), key=lambda a: -abs(a["delta"]))[:12],
        "evidence": {k: {kk: vv for kk, vv in v.items()} for k, v in evidence.items()},
        "ty2025_index_check": {k: [(r["EIN"], r["TAX_PERIOD"], r["OBJECT_ID"]) for r in v] for k, v in idx.items()},
    }


# ----------------------------------------------------------------------------- task `rails`
# Each observation: published statement as transcribed (verbatim quote), fetched 2026-11-15 unless noted.
# share_basis: count | dollars | unstated. electronic_share as a fraction; None when only volumes are published.
SHARE_OBS = (
    # sponsor, rail, as_of, period_covered, electronic_share, share_qualifier, share_basis, volume_note, quote, source_class, url
    ("Fidelity Charitable", "EFT (ACH + Stripe) vs check", "2023 Giving Report (covers CY2022; PDF metadata 2024-04-15, likely re-saved)", "early 2023 ('now')", 0.50,
     "more than", "count", "2.2 million grants in 2022",
     "More than 50% of our grants are now dispersed via EFT, at no charge to the nonprofit or the donor.",
     "sponsor_report", "https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf"),
    ("Fidelity Charitable", "EFT (ACH + Stripe) vs check", "2024 Giving Report (PDF created 2024-03-06)", "early 2024 ('now'); 2023 grants",
     0.54, "nearly", "count", "2.3 million grants in 2023; report says EFT allowed '950,000 grants' in 2023",
     "Nearly 54% of our grants are now dispersed via EFT, at no charge to the nonprofit or the donor—and, in 2023, "
     "allowing 950,000 grants to get to their nonprofits faster", "sponsor_report",
     "https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf"),
    ("Fidelity Charitable", "EFT (ACH + Stripe) vs check", "2025 Giving Report (PDF created 2025-02-19)", "early 2025 ('today'); 2024 grants",
     0.58, "over", "count", "nearly 2.7 million grants in 2024; report says EFT enabled 'more than 750,000 grants'",
     "Today, over 58% of our grants are now distributed via EFT, enabling more than 750,000 grants to reach nonprofits "
     "faster and more securely than with traditional check processing.", "sponsor_report",
     "https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf"),
    ("Fidelity Charitable", "EFT (ACH + Stripe) vs check", "2026 Giving Report (PDF created 2026-04-21)", "early 2026 ('today'); 2025 grants",
     0.67, "exact", "count", "3 million grants in 2025; 'more than 2 million grants' via EFT",
     "Today, 67% of our grants are distributed via EFT, meaning that more than 2 million grants have reached nonprofits "
     "faster and more securely than with traditional check processing.", "sponsor_report",
     "https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf"),
    ("Fidelity Charitable", "EFT vs check", "2026-03-24 (Chariot post)", "2025", 0.67, "exact", "count",
     "secondary: Chariot states 67% EFT / 33% check in 2025",
     "67% EFT and 33% check in 2025 (as summarised in repo, queue-payment-rails-cluster.md §2)", "vendor_secondary",
     "https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report"),
    ("Vanguard Charitable", "PayPal Grant Payments vs other", "2023-09-20", "2023-08 (three weeks after Maui fires)", 0.57,
     "exact", "dollars", "$3.7m of grants in the three weeks after the fires",
     "Of the $3.7 million that Vanguard Charitable donors issued in grants in the three weeks following the fires ... "
     "57% was sent electronically and arrived within a day of the grant's approval", "sponsor_press_release",
     "https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html"),
    ("Vanguard Charitable", "PayPal Grant Payments", "2023-09-20", "2023-05-03 to 2023-09-15", None, "", "dollars",
     "more than $130m to more than 400 charities electronically; non-check share up 'more than elevenfold' YoY",
     "electronically granted more than $130 million to more than 400 eligible charities", "sponsor_press_release",
     "https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html"),
    ("Vanguard Charitable", "PayPal Grant Payments", "2024-01-30", "launch to 2024-01 (calendar 2023 release)", None, "",
     "dollars", "more than $460m electronically to over 8,000 charities; 209,000 grants in CY2023 (all rails)",
     "Since launching Grant Payments, Vanguard Charitable donors have electronically granted more than $460 million to "
     "over 8,000 eligible charities", "sponsor_press_release",
     "https://prnewswire.com/news-releases/vanguard-charitable-donors-granted-more-than-2-6-billion-to-charity-in-2023--302047196.html"),
    ("Vanguard Charitable", "PayPal Grant Payments", "2024-09-06", "FY2024 (Jul 2023-Jun 2024)", None, "", "dollars",
     "$1bn via Grant Payments ('milestone'); FY2024 grants 'more than $3 billion'",
     "In fiscal year 2024, Vanguard Charitable reached another significant milestone – $1 billion in grants issued via "
     "Grant Payments with PayPal", "trade_press_reprint",
     "https://www.nonprofitpro.com/article/vanguard-charitable-donors-gave-more-than-3b-in-fiscal-year-2024/"),
    ("National Philanthropic Trust", "PayPal Grant Payments vs check", "2022-08-25", "2021 (baseline)", 0.0,
     "approximately", "dollars", "$6.4bn of grants in 2021 'almost entirely by check'",
     "these payments were made almost entirely by check", "vendor_press_release",
     "https://newsroom.paypal-corp.com/2022-08-25-PayPal-Launches-Grant-Payments,-Enabling-Charities-to-Quickly-Receive-Funds-from-Grantmakers"),
    ("National Philanthropic Trust", "PayPal Grant Payments eligibility", "2022-08-25", "2022-08 (launch)", None, "",
     "grantees", "one third of NPT grantees eligible (have PayPal accounts); not a payment share",
     "A full third of NPT's current grantees have accounts with PayPal and are eligible for receiving electronic grant payments.",
     "sponsor_article", "https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/"),
    ("Chariot (all Disbursements partners pooled)", "Chariot Deposit Account vs check", "2026-11-15 (live page)",
     "since launch (2025-04) to page date", 0.9457, "exact", "count", "vendor aggregate, no sponsor split",
     "Since launch, 94.57% of grant payments made through Chariot are sent electronically.", "vendor",
     "https://givechariot.com/disbursements.md"),
    ("Dallas Jewish Community Foundation", "Chariot Disbursements vs check", "2026-03", "as of Mar 2026", 0.92, "exact",
     "unstated", "~5,000 grants and ~$41m a year; 0% electronic in 2022; ~35% under a prior bank vendor",
     "92% ... Of all grantmaking now processed electronically (as of Mar 2026)", "vendor_case_study",
     "https://givechariot.com/resources/customer-stories/how-djcf-modernized-grant-payments--freed-its-team-from-the-back-office"),
    ("Dallas Jewish Community Foundation", "check only", "2022", "2022 (baseline)", 0.0, "exact", "unstated",
     "every grant by check when the CEO joined",
     "0% electronic payments", "vendor_case_study",
     "https://givechariot.com/resources/customer-stories/how-djcf-modernized-grant-payments--freed-its-team-from-the-back-office"),
    ("Dallas Jewish Community Foundation", "bank-sponsored invoice vendor vs check", "undated (2022-2025)", "interim", 0.35,
     "roughly", "unstated", "prior vendor stage", "roughly 35% electronic payments", "vendor_case_study",
     "https://givechariot.com/resources/customer-stories/how-djcf-modernized-grant-payments--freed-its-team-from-the-back-office"),
    ("Founders Pledge", "Chariot Disbursements vs check", "2026-03/04 (case-study images 2026-03-17..04-15)",
     "first 4 months after 2025-11 go-live", 0.97, "exact", "dollars", "$12m disbursed in first 4 months",
     "97% grant volume moving electronically on Chariot", "vendor_case_study",
     "https://givechariot.com/resources/customer-stories/how-founders-pledge-doubled-its-grantmaking-volume--without-doubling-its-operational-risk"),
    ("Founders Pledge", "Chariot Disbursements vs check", "2026-07-15 (webinar recap)", "about a year in", 0.98,
     "roughly", "count", "webinar recap, no volume",
     "roughly 98% of its grants go out electronically", "vendor_webinar_recap",
     "https://givechariot.com/resources/webinars/-powering-modern-daf-grants"),
    ("TIFIN Give (GiveClear Foundation; AssetMark Charitable and others)", "Chariot Disbursements vs check",
     "2026-06 (case-study images 2026-06-12..15)", "first 4 months with Chariot", 0.82, "exact", "dollars",
     "$34.1m granted; 5,175 grants processed",
     "82% Grant volume paid electronically", "vendor_case_study",
     "https://givechariot.com/resources/customer-stories/tifin-give-moves-80-of-grant-volume-electronically-with-chariot-disbursements"),
    ("Daffy", "Chariot Disbursements", "2026-07-21 (Chariot post)", "since Chariot launch", None, "", "dollars",
     "'over a quarter billion dollars electronically'; no share published",
     "over a quarter billion dollars electronically", "vendor_partner_post",
     "https://givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner"),
    ("Large national DAFs (unnamed)", "ACH vs check", "2026-01-20 (Chariot report)", "2025", 0.50, "about (ceiling)",
     "count", "vendor statement, providers unnamed",
     "Even the largest national DAFs have struggled to get their ACH rates much higher than 50% of their payments.",
     "vendor_report", "https://givechariot.com/resources/insights/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits"),
)

LAT_OBS = (
    # sponsor, rail, clock_start, clock_end, stat_type, low_days, high_days, day_unit, quote, measured?, as_of, url
    ("Fidelity Charitable", "any", "recommendation", "processed (approved)", "stated_minimum", 10, None, "business",
     "Grant recommendations may take 10 or more business days to be processed", "policy", "2026-11-15",
     "https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html"),
    ("Fidelity Charitable", "Stripe / ACH", "processed", "funds at nonprofit", "stated_range", 1, 2, "calendar",
     "Stripe and ACH ... '1-2 days' (nonprofit FAQ, repo capture 2026-11-14)", "policy", "2026-11-14",
     "https://www.fidelitycharitable.org/nonprofits/faqs.html"),
    ("Fidelity Charitable", "EFT vs check", "-", "-", "ratio", None, None, "",
     "Electronic funds transfers (EFTs) are nine times faster than traditional channels", "claim_unmeasured",
     "2026-04", "https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf"),
    ("DAFgiving360", "check", "recommendation", "check mailed", "stated_average", 7, 10, "business",
     "on average, checks are generally mailed within seven to 10 business days", "policy", "2024 policies (repo)",
     "https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf"),
    ("DAFgiving360", "check", "check mailed", "check delivered", "stated_typical", 3, 5, "business",
     "USPS delivery typically takes three to five business days", "policy", "2024 policies (repo)",
     "https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf"),
    ("Vanguard Charitable", "PayPal Grant Payments", "charity accepts grant", "funds at nonprofit", "stated_maximum", 0, 1,
     "calendar", "arrive within one day of the receiving charity accepting the grant", "policy", "2023-09-20",
     "https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html"),
    ("Vanguard Charitable", "PayPal Grant Payments", "approval", "funds at nonprofit", "stated_typical", 0, 1, "calendar",
     "Funds are now arriving in charity bank accounts in as quickly as minutes to hours.", "claim_unmeasured",
     "2024-01-30", "https://prnewswire.com/news-releases/vanguard-charitable-donors-granted-more-than-2-6-billion-to-charity-in-2023--302047196.html"),
    ("Vanguard Charitable", "any", "recommendation", "processed", "stated_typical", None, None, "",
     "Grants are generally processed within a few days (repo capture 2026-11-14)", "policy", "2026-11-14",
     "https://www.vanguardcharitable.org/nonprofit-organizations"),
    ("National Philanthropic Trust", "any (domestic)", "recommendation", "due diligence complete", "stated_maximum", 0, 5,
     "business", "Domestic due diligence '5 business days or less' (DAF Guide, PDF dated 2026-10-15; repo capture)",
     "policy", "2026-10-15", "https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf"),
    ("National Philanthropic Trust", "PayPal Grant Payments", "grant sent", "expiry then check reissue", "acceptance_window",
     14, 14, "calendar", "the grantee has 14 days to accept the payment before it expires and is then reissued to the grantee as a check",
     "policy", "2026-10-15", "https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf"),
    ("Charityvest", "check (pre-Chariot guide)", "check sent", "check arrives", "stated_approx", 10, 10, "business",
     "It can take approximately 10 business days for the check to arrive in the mail.", "policy", "2026-11-15",
     "https://guide.charityvest.org/for-donors/getting-started/check-grant-status.md"),
    ("Charityvest", "check (pre-Chariot guide)", "check sent", "check deposited", "P95", None, 35, "calendar",
     "Based on our data, 95% of checks are deposited by recipient charities within 35 days of when they are sent.",
     "measured_vendor_undisclosed_sample", "2026-11-15", "https://guide.charityvest.org/for-donors/getting-started/check-grant-status.md"),
    ("AssetMark Charitable (TIFIN Give)", "all rails (Chariot + check)", "grant submission", "funds received", "median",
     2, 2, "calendar", "Overall: 2 days.", "measured_vendor_undisclosed_sample", "2026-11-15 ('updated this week')",
     "https://intercom.help/assetmark-help-center/en/articles/13931838-how-grant-payments-are-delivered-electronic-check"),
    ("AssetMark Charitable (TIFIN Give)", "Chariot electronic", "grant submission", "funds received", "median", 0, 0,
     "calendar", "Electronic delivery: 0 days.", "measured_vendor_undisclosed_sample", "2026-11-15 ('updated this week')",
     "https://intercom.help/assetmark-help-center/en/articles/13931838-how-grant-payments-are-delivered-electronic-check"),
    ("TIFIN Give", "Chariot Disbursements", "grant recommendation", "funds at nonprofit", "benchmark", 4, 4, "unstated",
     "T+4 from grant recommendation to nonprofit receiving funds", "vendor_case_study", "2026-06",
     "https://givechariot.com/resources/customer-stories/tifin-give-moves-80-of-grant-volume-electronically-with-chariot-disbursements"),
    ("BlueGive", "ACH", "approval", "ACH sent", "stated_maximum", 0, 3, "business",
     "ACH 'within 3 business days' of approval (repo capture 2026-11-14)", "policy", "2026-11-14",
     "https://intercom.help/bluegive-help-center/en/articles/10597826-granting-faqs"),
    ("BlueGive", "check", "approval", "check sent", "stated_range", 7, 14, "calendar",
     "check 'within 1-2 weeks' (repo capture 2026-11-14)", "policy", "2026-11-14",
     "https://intercom.help/bluegive-help-center/en/articles/10597826-granting-faqs"),
    ("Daffy", "any", "recommendation", "reviewed", "stated_maximum", 0, 7, "calendar",
     "Review 'can take up to one week' (repo capture 2026-11-14)", "policy", "2026-11-14",
     "https://help.daffy.org/en/articles/9122843-how-does-daffy-send-donations-to-charity"),
    ("Chariot Disbursements (partners)", "check fallback", "grant issued", "check delivered", "stated_typical", 14, 21,
     "calendar", "checks '~2-3 week delays' (repo capture 2026-11-14)", "policy", "2026-11-14",
     "https://help.givechariot.com/getting-started/disbursements-faqs.md"),
    ("Chariot Disbursements (partners)", "Chariot Deposit Account", "grant issued", "claim deadline then check",
     "claim_window", 5, 5, "business", "Five-business-day claim window with three reminder emails, then mailed check (repo capture)",
     "policy", "2026-11-14", "https://help.givechariot.com/disbursements/for-grantmakers/tracking-and-delivery.md"),
    ("Dallas Jewish Community Foundation", "Chariot Disbursements", "approval", "funds at nonprofit", "stated_typical", 0, 0,
     "calendar", "Once those payments are approved, within an hour the receiving nonprofit has it in their account.",
     "vendor_webinar_recap", "2026-07-15", "https://givechariot.com/resources/webinars/-powering-modern-daf-grants"),
    ("Dallas Jewish Community Foundation", "check (before Chariot)", "weekly grant run", "check reaches nonprofit",
     "stated_range", 10, 15, "calendar", "Checks used to reach nonprofits 10 to 15 days after the weekly grant run.",
     "vendor_webinar_recap", "2026-07-15", "https://givechariot.com/resources/webinars/-powering-modern-daf-grants"),
    ("Dallas Jewish Community Foundation", "check (before Chariot)", "check issued", "check cleared", "stated_range", 60, 90,
     "calendar", "Checks sometimes sat uncleared for 60 to 90 days", "vendor_case_study", "undated (pre-2026)",
     "https://givechariot.com/resources/customer-stories/how-djcf-modernized-grant-payments--freed-its-team-from-the-back-office"),
    ("Greater Houston Community Foundation", "ACH", "payment sent", "deposited", "stated_typical", 1, 2, "business",
     "ACH grant payments are typically deposited within 1–2 business days", "policy", "2026-04-17",
     "https://ghcf.org/articles/why-ach-grant-payments-benefit-nonprofits/"),
    ("Greater Houston Community Foundation", "check", "payment sent", "deposited", "stated_minimum", 7, None, "calendar",
     "checks may take a week or more to arrive, be opened, and deposited", "policy", "2026-04-17",
     "https://ghcf.org/articles/why-ach-grant-payments-benefit-nonprofits/"),
    ("34 DAF providers to one nonprofit (Chariot sample)", "ACH (3 fastest providers)", "grant approval", "payment received",
     "provider_average", 1, 2, "calendar",
     "Pledger Charitable, The Donors Fund, and Fidelity Charitable all delivered payment via ACH within 1-2 days of grant approval, on average",
     "measured_vendor_n1_recipient", "2026-01-20",
     "https://givechariot.com/resources/insights/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits"),
    ("34 DAF providers to one nonprofit (Chariot sample)", "check (18 providers)", "grant approval", "payment received",
     "provider_average_range", 7, 162, "calendar",
     "the 18 providers that sent payment as physical checks had average delivery times of anywhere from 7 to 162 days",
     "measured_vendor_n1_recipient", "2026-01-20",
     "https://givechariot.com/resources/insights/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits"),
    ("PayPal Giving Fund", "PPGF monthly payout (enrolled)", "donation", "grant paid", "stated_range", 15, 45, "calendar",
     "Paid 15-45 days after donation at month end (repo capture of PayPal help969)", "policy", "2026-11-14",
     "https://www.paypal.com/us/cshelp/article/how-does-paypal-giving-fund-grant-donations-to-charities-help969"),
)

SHARE_FIELDS = ("obs_id", "sponsor", "rail", "as_of", "period_covered", "electronic_share", "share_qualifier",
                "share_basis", "check_or_other_share_implied", "implied_electronic_count", "volume_note", "quote",
                "source_class", "first_party", "url", "retrieved")
LAT_FIELDS = ("obs_id", "sponsor", "rail", "clock_start", "clock_end", "stat_type", "low_days", "high_days", "day_unit",
              "high_days_calendar_approx", "evidence_type", "as_of", "quote", "url", "retrieved")
FIRST_PARTY = ("sponsor_report", "sponsor_press_release", "sponsor_article")
COUNTS = {"2.2 million": 2.2e6, "2.3 million": 2.3e6, "2.7 million": 2.7e6, "3 million": 3.0e6}


def share_row(i: int, o: tuple) -> dict:
    sp, rail, asof, per, sh, q, basis, vol, quote, cls, url = o
    n = next((v for k, v in COUNTS.items() if vol.startswith(("nearly " + k, k))), None)
    return {"obs_id": f"S{i:02d}", "sponsor": sp, "rail": rail, "as_of": asof, "period_covered": per,
            "electronic_share": sh, "share_qualifier": q, "share_basis": basis,
            "check_or_other_share_implied": None if sh is None else round(1 - sh, 4),
            "implied_electronic_count": round(sh * n) if (sh is not None and n and basis == "count") else None,
            "volume_note": vol, "quote": quote, "source_class": cls,
            "first_party": "yes" if cls in FIRST_PARTY else "no", "url": url, "retrieved": "2026-11-15"}


def lat_row(i: int, o: tuple) -> dict:
    sp, rail, c0, c1, st, lo, hi, unit, quote, ev, asof, url = o
    cal = None if hi is None else (round(hi * 7 / 5, 1) if unit == "business" else hi)
    return {"obs_id": f"L{i:02d}", "sponsor": sp, "rail": rail, "clock_start": c0, "clock_end": c1, "stat_type": st,
            "low_days": lo, "high_days": hi, "day_unit": unit, "high_days_calendar_approx": cal, "evidence_type": ev,
            "as_of": asof, "quote": quote, "url": url,
            "retrieved": "2026-11-14 (repo capture)" if "repo capture" in quote else "2026-11-15"}


def run_rails(_args) -> dict:
    shares = [share_row(i, o) for i, o in enumerate(SHARE_OBS, 1)]
    lats = [lat_row(i, o) for i, o in enumerate(LAT_OBS, 1)]
    write_csv(OUT_SHARES, shares, SHARE_FIELDS)
    write_csv(OUT_LAT, lats, LAT_FIELDS)
    fid = [(r["as_of"], r["electronic_share"], r["implied_electronic_count"]) for r in shares
           if r["sponsor"] == "Fidelity Charitable" and r["first_party"] == "yes"]
    return {"share_rows": len(shares), "latency_rows": len(lats), "fidelity_series": fid,
            "first_party_share_rows": sum(r["first_party"] == "yes" for r in shares),
            "measured_latency_rows": sum(r["evidence_type"].startswith("measured") for r in lats)}


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", choices=("accounts", "rails"))
    ap.add_argument("--work-dir", default="WORK")
    ap.add_argument("--index", default="", help="IRS index_2026.csv for the TY2025 filing check")
    ap.add_argument("--fetch", action="store_true")
    args = ap.parse_args(argv)
    out = run_accounts(args) if args.task == "accounts" else run_rails(args)
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
