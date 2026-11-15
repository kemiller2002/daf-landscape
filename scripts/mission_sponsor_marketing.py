#!/usr/bin/env python3
"""Sponsor marketing spend from Form 990 Part IX line 12, related lines, and Schedule D growth (TY2021-2025).

Queue item P-NEW-MKT-01. Stdlib only; functional style (pure transforms, I/O at the edges).

Universe: the top 100 DAF sponsors by FY2024 DAF assets (`fy2024_asset_rank` in the full harvest, DAFRC FY2024
values) plus the repo's digital-first sponsors (Daffy, Charityvest, Endaoment, Givinga, GiveClear/TIFIN Give,
GoFundMe.org, Percent Impact Foundation/Goodstack; Every.org files 990-PF and has no line 12) and PayPal Giving Fund
as a processor comparator.

Returns: every Form 990 (not 990-PF/990-EZ) in IRS TEOS indexes 2021-2026 for those EINs whose tax period ends
2021-12 or later; latest object id per (EIN, tax period). Tax year (TY) = year in which the period begins (IRS
convention), read from the return header; kept when TY is 2021-2025.

Sources, in order:
  1. GivingTuesday mirror of IRS e-file XML (https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/
     {OID}_public.xml; robots.txt returns 404, i.e. no restrictions). Streamed; parsing stops after Schedule D, so
     large Schedule I tables are never downloaded in full.
  2. TEOS zip members already range-read by earlier batches (local `*/work/teos/{OID}_public.xml`, --teos-dir).
  3. Cross-check: the JSON cache of scripts/mission_sponsor_cost_structure.py (`extract990cost/{OID}.json`,
     --cost-cache) must give the same line-12 total where it exists.

Reused: number parsing, CSV I/O and XML helpers from mission_990_contractors.py; the Part IX group map, column map
and `part_ix_from` from mission_sponsor_cost_structure.py.

Usage:
  python3 scripts/mission_sponsor_marketing.py --irs-dir IRS --cache-dir CACHE --cost-cache COSTCACHE \
      --teos-dir DIR [--teos-dir DIR2 ...] [--fetch] [--workers 12]
Outputs:
  data/mission-2026-11-14/sponsor-marketing-spend-2021-2025.csv  (row_type = return | group_year | group_pooled)
  prints a JSON summary used by research/mission-2026-11-14/direction-sponsor-marketing-spend.md
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as m990  # noqa: E402
import mission_sponsor_cost_structure as mcs  # noqa: E402

DATA = m990.DATA
HARVEST_CSV = os.path.join(DATA, "form990-returns-schedule-d-harvest-full.csv")
DAFRC_CSV = m990.DAFRC_CSV
OUT = os.path.join(DATA, "sponsor-marketing-spend-2021-2025.csv")
XML_URL = m990.XML_URL
EXTRACT_VERSION = 1
TY_RANGE = (2021, 2025)
num, fmt, ein9, read_csv, write_csv, local = m990.num, m990.fmt, m990.ein9, m990.read_csv, m990.write_csv, m990.local
NS = m990.NS

# ----------------------------------------------------------------------------- universe and sponsor groups
# Digital-first list as used in queue-batch35-agents-analysts-rails.md / digital-sponsor-entities-2026.csv.
DIGITAL_FIRST = {
    "863177440": "Daffy", "812771871": "Charityvest", "844661797": "Endaoment", "474172718": "Givinga",
    "813222963": "GiveClear (TIFIN Give)", "812279757": "GoFundMe.org (GoFundMe Giving Funds)",
    "873165286": "Percent Impact Foundation (Goodstack)", "611913297": "Every.org (990-PF filer)",
}
COMPARATORS = {"450931286": "PayPal Giving Fund (processor comparator)"}
# Affiliated-commercial nationals: sponsor named for, and run with, a for-profit financial firm [I: classification
# by name and public program branding; parent named for the limitation note].
AFFILIATED = {
    "110303001": "Fidelity (FMR)", "311640316": "Charles Schwab", "232888152": "Vanguard",
    "311774905": "Goldman Sachs", "527082731": "Morgan Stanley", "046010342": "Bank of America",
    "593652538": "Raymond James", "141782466": "Ayco (Goldman Sachs)", "137111099": "Bessemer Trust",
    "311709466": "T. Rowe Price", "113813663": "Goldman Sachs", "842049692": "Stifel",
    "300233491": "Johnson Financial Group",
}
# Digital-first sponsors and processors whose platform or operating company sits outside the charity, so donor
# acquisition can be paid off the 990. Basis per sponsor; [F] from repo files, [I] inference.
PLATFORM_PAID = {
    "863177440": "Daffy: donors pay membership fees to the Daffy platform (repo source C21); the charity's 990 shows "
                 "no management fee or named platform payee [I]",
    "812771871": "Charityvest: 990 line 24 'platform fee' ($507k TY2023, $653k TY2024), payee not named [F]; platform "
                 "marketing not visible [I]",
    "474172718": "Givinga: affiliated taxable vendor Givinga, Inc. (digital-sponsor-entities-2026.csv) [F]",
    "813222963": "GiveClear: operates as TIFIN Give; platform company outside the 990 [I]",
    "812279757": "GoFundMe.org: consumer platform operated by GoFundMe's for-profit company [I]",
    "873165286": "Percent Impact Foundation: service provider We Are Percent Ltd t/a Goodstack (repo) [F]",
    "450931286": "PayPal Giving Fund: donations collected through PayPal's products [I]",
    "810739440": "AOGF: workplace programs run on Benevity; line 11a management fees $32-58m a year [F]",
}
# Nationals whose commercial affiliation was not checked here: kept as independent, flagged.
AFFILIATION_UNCHECKED = frozenset({"311663020", "812576201", "812375745"})
PROCESSOR_EINS = frozenset({"260724604", "810739440", "450931286"})  # Dechomai, AOGF, PPGF (not digital-first list)
ACCOUNT_UNIT_UNDEFINED = frozenset({"474172718", "450931286", "810739440"})  # batch 36 §1: Givinga, PPGF, AOGF
CAMPAIGN_ADVERTISING = frozenset({"431890105"})  # Servant Foundation: line 12 is campaign spending (cost-structure §8)
GROUPS = ("affiliated_commercial_national", "independent_national", "digital_first", "community_foundation",
          "processor", "single_issue")


def sponsor_group(ein: str, dafrc_type: str) -> tuple[str, str]:
    if ein in DIGITAL_FIRST:
        return "digital_first", "repo digital-first list"
    if ein in AFFILIATED:
        return "affiliated_commercial_national", f"parent: {AFFILIATED[ein]} [I]"
    if ein in PROCESSOR_EINS:
        return "processor", "DAFRC subtype Donation Processor"
    if dafrc_type == "Community Foundation":
        return "community_foundation", "DAFRC type"
    if dafrc_type == "National":
        return "independent_national", ("affiliation not checked [I]" if ein in AFFILIATION_UNCHECKED
                                         else "no commercial parent in name or branding [I]")
    return "single_issue", f"DAFRC type {dafrc_type}"


def universe(harvest: Sequence[Mapping]) -> dict[str, dict]:
    top = {h["ein"]: h for h in harvest if h["fy2024_asset_rank"] and int(h["fy2024_asset_rank"]) <= 100}
    named = {e: next((h for h in harvest if h["ein"] == e), {"ein": e, "sponsor_name": n, "type": "", "subtype": "",
                                                             "fy2024_asset_rank": ""})
             for e, n in {**DIGITAL_FIRST, **COMPARATORS}.items()}
    pick = {**top, **named}
    return {e: {"ein": e, "sponsor_name": h["sponsor_name"], "dafrc_type": h["type"], "dafrc_subtype": h["subtype"],
                "fy2024_asset_rank": h["fy2024_asset_rank"],
                "selection": "top100_fy2024_daf_assets" if e in top else (
                    "digital_first" if e in DIGITAL_FIRST else "comparator"),
                **dict(zip(("sponsor_group", "group_basis"), sponsor_group(e, h["type"])))}
            for e, h in pick.items()}


# ----------------------------------------------------------------------------- IRS index -> return list
def index_rows(irs_dir: str, eins: frozenset) -> tuple[dict, ...]:
    def one(y):
        with open(os.path.join(irs_dir, f"index_{y}.csv"), newline="", encoding="utf-8-sig", errors="replace") as fh:
            return tuple({**r, "EIN": ein9(r["EIN"]), "index_year": y} for r in csv.DictReader(fh)
                         if ein9(r.get("EIN", "")) in eins)
    return tuple(r for y in range(2021, 2027) for r in one(y))


def pick_returns(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    """Form 990 only; period ending 2021-12 or later. All filings per period are kept (original and amended);
    the one with the latest ReturnTs is chosen after parsing, because an amendment can carry a lower object id
    (Givinga CY2024, cost-structure §8)."""
    ok = tuple(r for r in rows if r["RETURN_TYPE"].strip() == "990" and r["TAX_PERIOD"].strip() >= "202112")
    uniq = {r["OBJECT_ID"]: r for r in ok}
    return tuple(sorted(uniq.values(), key=lambda r: (r["EIN"], r["TAX_PERIOD"], r["OBJECT_ID"])))


# ----------------------------------------------------------------------------- XML extract (streamed, early stop)
MKT_STRICT = re.compile(r"market|advertis|promot|brand|sponsorship|public relation|(?:/|&\s?)PR\b", re.I)
MKT_BROAD = re.compile(r"communicat|outreach|media|donor (?:engagement|acquisition|development|education)|event", re.I)
MKT_EXCLUDE = re.compile(r"fiscal sponsor|grant|telephone|board communicat", re.I)  # false positives seen in run 1


def mkt_kind(desc: str) -> str:
    d = desc or ""
    return ("" if MKT_EXCLUDE.search(d) else "strict" if MKT_STRICT.search(d) else
            "broad" if MKT_BROAD.search(d) else "")


def other_expense_rows(el) -> tuple[dict, ...]:
    return tuple({"desc": m990.text_of(g, ("Desc",)),
                  **{c: num(m990.text_of(g, (t,))) for c, t in mcs.COLS}}
                 for g in el if local(g.tag) == "OtherExpensesGrp")


def extract_stream(stream) -> dict:
    out: dict = {"sched_d_present": 0}
    for event, el in ET.iterparse(stream, events=("start", "end")):
        tag = local(el.tag)
        if event == "start":
            if tag.startswith("IRS990Schedule") and tag[len("IRS990Schedule"):][:1] > "D":
                break
            continue
        if tag == "ReturnHeader":
            out.update({"tax_period_end": m990.text_of(el, ("TaxPeriodEndDt",)),
                        "tax_period_begin": m990.text_of(el, ("TaxPeriodBeginDt",)),
                        "return_ts": m990.text_of(el, ("ReturnTs",)),
                        "return_type": m990.text_of(el, ("ReturnTypeCd",)),
                        "filer_name": " ".join(x.text.strip() for x in el.iter()
                                               if local(x.tag) == "BusinessNameLine1Txt" and x.text)[:120]})
            el.clear()
        elif tag == "IRS990":
            out.update({"part_i": {t: num(m990.text_of(el, (t,))) for t in mcs.PART_I},
                        "part_ix": mcs.part_ix_from(el),
                        "other_expenses": list(other_expense_rows(el)),
                        "amended_ind": m990.text_of(el, ("AmendedReturnInd",))})
            el.clear()
        elif tag == "IRS990ScheduleD":
            out.update({"sched_d_present": 1,
                        "sched_d_daf_count": num(m990.text_of(el, ("DonorAdvisedFundsHeldCnt",))),
                        "sched_d_daf_contributions": num(m990.text_of(el, ("DonorAdvisedFundsContriAmt",))),
                        "sched_d_daf_grants": num(m990.text_of(el, ("DonorAdvisedFundsGrantsAmt",))),
                        "sched_d_daf_eoy_value": num(m990.text_of(el, ("DonorAdvisedFundsVlEOYAmt",)))})
            break
        elif tag.startswith("IRS990Schedule"):
            el.clear()
    return out


def teos_path(oid: str, teos_dirs: Sequence[str]) -> str | None:
    return next((p for p in (os.path.join(d, f"{oid}_public.xml") for d in teos_dirs) if os.path.exists(p)), None)


def fetch_extract(oid: str, cache_dir: str, teos_dirs: Sequence[str], fetch: bool, retries: int = 2) -> dict:
    path = os.path.join(cache_dir, "extract990mkt", f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            cached = json.load(fh)
        if cached.get("_v") == EXTRACT_VERSION:
            return cached
    url = XML_URL.format(oid=oid)
    out = {"xml_status": "not_fetched"}
    if fetch:
        req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    out = {**extract_stream(resp), "xml_status": "ok", "xml_source": "gt_mirror", "xml_url": url}
                break
            except urllib.error.HTTPError as e:
                out = {"xml_status": f"http_{e.code}"}
                if e.code in (403, 404):
                    break
            except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
                out = {"xml_status": f"error:{type(e).__name__}"}
                time.sleep(2 * (attempt + 1))
    local_xml = teos_path(oid, teos_dirs)
    if out["xml_status"] != "ok" and local_xml:
        with open(local_xml, "rb") as fh:
            out = {**extract_stream(fh), "xml_status": "ok", "xml_source": "teos_zip_member_cached",
                   "xml_url": local_xml.rsplit("/", 1)[-1], "mirror_status": out["xml_status"]}
    result = {**out, "_v": EXTRACT_VERSION}
    if result["xml_status"] == "ok" or result["xml_status"].startswith("http_404"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(result, fh)
    return result


def cost_cache_l12(oid: str, cost_cache: str) -> float | None:
    p = os.path.join(cost_cache, "extract990cost", f"{oid}.json")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        x = json.load(fh)
    return ((x.get("part_ix") or {}).get("l12_advertising") or {}).get("total")


# ----------------------------------------------------------------------------- per-return row
def ssum(*xs):
    v = tuple(x for x in xs if x is not None)
    return sum(v) if v else None


def div(a, b):
    return None if a is None or b in (None, 0) else a / b


def clip01(x):
    return None if x is None else max(0.0, min(1.0, x))


def months(begin: str, end: str) -> int | None:
    try:
        b, e = (tuple(int(p) for p in s[:7].split("-")) for s in (begin, end))
        return (e[0] - b[0]) * 12 + e[1] - b[1] + 1
    except (ValueError, IndexError):
        return None


def return_row(meta: Mapping, idx: Mapping, x: Mapping, cost_l12) -> dict:
    ix = x.get("part_ix") or {}
    p1 = x.get("part_i") or {}
    L = lambda k, c="total": (ix.get(k) or {}).get(c)  # noqa: E731
    oth = x.get("other_expenses") or []
    strict = tuple(o for o in oth if mkt_kind(o["desc"]) == "strict")
    broad = tuple(o for o in oth if mkt_kind(o["desc"]) == "broad")
    tfe = L("l25_total") if L("l25_total") is not None else p1.get("CYTotalExpensesAmt")
    grants = ssum(L("l01_grants_domestic_orgs"), L("l02_grants_domestic_individuals"), L("l03_grants_foreign"))
    opex_ex_inv = None if tfe is None else tfe - (grants or 0) - (L("l04_benefits_to_members") or 0) - (
        L("l11f_fees_investment_mgmt") or 0)
    adv = L("l12_advertising")
    fee_keys = ("l11a_fees_management", "l11b_fees_legal", "l11c_fees_accounting", "l11d_fees_lobbying",
                "l11e_fees_prof_fundraising", "l11f_fees_investment_mgmt", "l11g_fees_other")
    ty = int(x["tax_period_begin"][:4]) if x.get("tax_period_begin") else None
    contrib_total = p1.get("CYContributionsGrantsAmt")
    sd_contrib = x.get("sched_d_daf_contributions")
    return {
        **meta, "row_type": "return", "tax_year": ty, "tax_period_begin": x.get("tax_period_begin"),
        "tax_period_end": x.get("tax_period_end"), "period_months": months(x.get("tax_period_begin", ""),
                                                                           x.get("tax_period_end", "")),
        "return_object_id": idx["OBJECT_ID"], "return_ts": x.get("return_ts"), "amended_ind": x.get("amended_ind"),
        "xml_source": x.get("xml_source"), "xml_url": x.get("xml_url"),
        "adv_l12_total": adv, "adv_l12_program": L("l12_advertising", "program"),
        "adv_l12_mgmt": L("l12_advertising", "mgmt"), "adv_l12_fundraising": L("l12_advertising", "fundraising"),
        "adv_l12_cost_cache_check": ("match" if cost_l12 is not None and (cost_l12 or 0) == (adv or 0) else
                                     "mismatch" if cost_l12 is not None else "not_in_cost_cache"),
        "fees_mgmt_l11a": L(fee_keys[0]), "fees_legal_l11b": L(fee_keys[1]), "fees_accounting_l11c": L(fee_keys[2]),
        "fees_lobbying_l11d": L(fee_keys[3]), "fees_prof_fundraising_l11e": L(fee_keys[4]),
        "fees_invest_mgmt_l11f": L(fee_keys[5]), "fees_other_l11g": L(fee_keys[6]),
        "fees_l11_total": ssum(*(L(k) for k in fee_keys)),
        "it_l14_total": L("l14_information_technology"), "it_l14_program": L("l14_information_technology", "program"),
        "it_l14_mgmt": L("l14_information_technology", "mgmt"),
        "it_l14_fundraising": L("l14_information_technology", "fundraising"),
        "l24_marketing_strict_amt": ssum(*(o["total"] for o in strict)),
        "l24_marketing_strict_desc": " | ".join(f"{o['desc']}={fmt(o['total'])}" for o in strict)[:300],
        "l24_marketing_broad_amt": ssum(*(o["total"] for o in broad)),
        "l24_marketing_broad_desc": " | ".join(f"{o['desc']}={fmt(o['total'])}" for o in broad)[:300],
        "adv_plus_l24_strict": ssum(adv, ssum(*(o["total"] for o in strict))),
        "total_functional_expenses_l25": tfe, "fundraising_col_l25": L("l25_total", "fundraising"),
        "operating_cost_ex_invest": opex_ex_inv, "adv_share_of_opex": div(adv, opex_ex_inv),
        "total_contributions_part_i": contrib_total, "total_assets_eoy": p1.get("TotalAssetsEOYAmt"),
        "employees": p1.get("TotalEmployeeCnt"),
        "sd_present": x.get("sched_d_present"), "sd_daf_count": x.get("sched_d_daf_count"),
        "sd_daf_contributions": sd_contrib, "sd_daf_grants": x.get("sched_d_daf_grants"),
        "sd_daf_eoy_value": x.get("sched_d_daf_eoy_value"),
        "daf_share_of_contributions": clip01(div(sd_contrib, contrib_total)),
    }


# ----------------------------------------------------------------------------- growth and cost ratios
def dafrc_lookup(dafrc: Sequence[Mapping]) -> dict:
    return {(r["ein"], r["fy"]): r for r in dafrc}


def with_growth(rows: Sequence[Mapping], dafrc: Mapping) -> tuple[dict, ...]:
    """Net new accounts = count_t - count_(t-1). Prior from the sponsor's previous return in this set (TY-1, a
    12-month period), else the DAFRC row for the fiscal year before this period's end (flagged)."""
    by = {(r["ein"], r["tax_year"]): r for r in rows}

    def one(r):
        prev = by.get((r["ein"], r["tax_year"] - 1)) if r["tax_year"] else None
        fy = int(r["tax_period_end"][:4]) if r.get("tax_period_end") else None
        d = dafrc.get((r["ein"], fy - 1)) if fy else None
        prior, src = ((prev["sd_daf_count"], "prior_return") if prev and prev.get("sd_daf_count") is not None else
                      (num(d["number_of_daf_accounts"]), f"dafrc_fy{fy - 1}:{d['source_number_of_accounts']}")
                      if d and num(d["number_of_daf_accounts"]) is not None else (None, ""))
        cur = r.get("sd_daf_count")
        nna = None if cur is None or prior is None else cur - prior
        adv = r.get("adv_l12_total")
        share = r.get("daf_share_of_contributions")
        adv_alloc = None if adv is None or share is None else adv * share
        flags = tuple(f for f, c in (
            ("affiliate_paid_marketing_possible", r["sponsor_group"] == "affiliated_commercial_national"),
            ("platform_paid_marketing_possible", r["ein"] in PLATFORM_PAID),
            ("account_unit_undefined", r["ein"] in ACCOUNT_UNIT_UNDEFINED),
            ("campaign_advertising_not_overhead", r["ein"] in CAMPAIGN_ADVERTISING),
            ("university_health_whole_org", r["dafrc_subtype"] == "Universities and Healthcare"),
            ("pooled_single_fund", cur is not None and cur <= 1),
            ("short_or_long_period", r.get("period_months") not in (None, 12)),
            ("amended_return", bool(r.get("amended_ind"))),
            ("sched_d_blank", cur is None and r.get("sd_daf_contributions") is None),
            ("prior_count_from_dafrc", src.startswith("dafrc")),
            ("net_new_accounts_le_0", nna is not None and nna <= 0),
            ("l12_blank", adv is None),
            ("l24_marketing_lines", r.get("l24_marketing_strict_amt") is not None),
            ("daf_contrib_gt_total_contrib", (div(r.get("sd_daf_contributions"), r.get("total_contributions_part_i"))
                                              or 0) > 1),
        ) if c)
        return {**r, "prior_daf_count": prior, "prior_count_source": src, "net_new_accounts": nna,
                "account_growth_pct": div(nna, prior),
                "adv_per_dollar_daf_contrib": div(adv or 0, r.get("sd_daf_contributions")) if adv is not None else None,
                "adv_bps_of_daf_contrib": (lambda v: None if v is None else v * 1e4)(
                    div(adv, r.get("sd_daf_contributions"))),
                "adv_bps_of_total_contrib": (lambda v: None if v is None else v * 1e4)(
                    div(adv, r.get("total_contributions_part_i"))),
                "adv_alloc_daf": adv_alloc,
                "adv_per_net_new_account": div(adv, nna) if nna and nna > 0 else None,
                "adv_alloc_per_net_new_account": div(adv_alloc, nna) if nna and nna > 0 else None,
                "adv_alloc_per_new_dollar_bps": (lambda v: None if v is None else v * 1e4)(
                    div(adv_alloc, r.get("sd_daf_contributions"))),
                "outside_990_marketing_basis": (f"commercial parent {AFFILIATED[r['ein']]} may pay marketing [I]"
                                                if r["ein"] in AFFILIATED else PLATFORM_PAID.get(r["ein"], "")),
                "quality_flags": ";".join(flags)}
    return tuple(one(r) for r in rows)


# ----------------------------------------------------------------------------- group statistics
def quant(xs: Sequence[float], q: float):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def analysable(r: Mapping) -> bool:
    """Has Part IX data and line 12 is overhead: Servant Foundation's campaign line and university/hospital
    foundations (whole-institution advertising) are excluded from group statistics, as in the cost-structure work."""
    return (r["adv_l12_total"] is not None or r["total_functional_expenses_l25"] is not None) and \
        "campaign_advertising_not_overhead" not in r["quality_flags"] and \
        "university_health_whole_org" not in r["quality_flags"]


def group_stats(rows: Sequence[Mapping], group: str, label: str, row_type: str) -> dict:
    rs = tuple(r for r in rows if analysable(r))
    adv = lambda r: r["adv_l12_total"] or 0  # noqa: E731  blank line 12 = nothing reported
    contrib_rows = tuple(r for r in rs if (r["sd_daf_contributions"] or 0) > 0)
    acct_rows = tuple(r for r in rs if (r["net_new_accounts"] or 0) > 0 and "account_unit_undefined" not in r["quality_flags"])
    alloc_rows = tuple(r for r in contrib_rows if r["adv_alloc_daf"] is not None)
    s_adv_c = sum(adv(r) for r in contrib_rows)
    s_c = sum(r["sd_daf_contributions"] for r in contrib_rows)
    return {
        "row_type": row_type, "sponsor_group": group, "tax_year": label,
        "n_returns": len(rs), "n_sponsors": len({r["ein"] for r in rs}),
        "n_l12_positive": sum(1 for r in rs if adv(r) > 0),
        "share_l12_positive": div(sum(1 for r in rs if adv(r) > 0), len(rs)),
        "adv_l12_total": sum(adv(r) for r in rs),
        "adv_l12_program": sum(r["adv_l12_program"] or 0 for r in rs),
        "adv_l12_mgmt": sum(r["adv_l12_mgmt"] or 0 for r in rs),
        "adv_l12_fundraising": sum(r["adv_l12_fundraising"] or 0 for r in rs),
        "adv_plus_l24_strict": sum(r["adv_plus_l24_strict"] or 0 for r in rs),
        "fees_mgmt_l11a": sum(r["fees_mgmt_l11a"] or 0 for r in rs),
        "fees_legal_l11b": sum(r["fees_legal_l11b"] or 0 for r in rs),
        "fees_accounting_l11c": sum(r["fees_accounting_l11c"] or 0 for r in rs),
        "fees_invest_mgmt_l11f": sum(r["fees_invest_mgmt_l11f"] or 0 for r in rs),
        "fees_other_l11g": sum(r["fees_other_l11g"] or 0 for r in rs),
        "it_l14_total": sum(r["it_l14_total"] or 0 for r in rs),
        "operating_cost_ex_invest": sum(r["operating_cost_ex_invest"] or 0 for r in rs),
        "adv_share_of_opex": div(sum(adv(r) for r in rs), sum(r["operating_cost_ex_invest"] or 0 for r in rs)),
        "sd_daf_contributions": s_c,
        "adv_bps_of_daf_contrib": None if not s_c else s_adv_c / s_c * 1e4,
        "adv_bps_of_daf_contrib_median": quant(tuple(adv(r) / r["sd_daf_contributions"] * 1e4 for r in contrib_rows), .5),
        "adv_bps_of_daf_contrib_p25": quant(tuple(adv(r) / r["sd_daf_contributions"] * 1e4 for r in contrib_rows), .25),
        "adv_bps_of_daf_contrib_p75": quant(tuple(adv(r) / r["sd_daf_contributions"] * 1e4 for r in contrib_rows), .75),
        "adv_alloc_daf": sum(r["adv_alloc_daf"] for r in alloc_rows),
        "adv_alloc_per_new_dollar_bps": div(sum(r["adv_alloc_daf"] for r in alloc_rows) * 1e4,
                                            sum(r["sd_daf_contributions"] for r in alloc_rows)),
        "net_new_accounts": sum(r["net_new_accounts"] for r in acct_rows),
        "n_returns_net_new_positive": len(acct_rows),
        "adv_per_net_new_account": div(sum(adv(r) for r in acct_rows), sum(r["net_new_accounts"] for r in acct_rows)),
        "adv_per_net_new_account_median": quant(tuple(adv(r) / r["net_new_accounts"] for r in acct_rows), .5),
        "adv_alloc_per_net_new_account": div(sum(r["adv_alloc_daf"] or 0 for r in acct_rows),
                                             sum(r["net_new_accounts"] for r in acct_rows)),
    }


def summaries(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    years = tuple(range(TY_RANGE[0], TY_RANGE[1] + 1))
    by_year = tuple(group_stats(tuple(r for r in rows if r["sponsor_group"] == g and r["tax_year"] == y), g, str(y),
                                "group_year") for g in GROUPS for y in years)
    pooled = tuple(group_stats(tuple(r for r in rows if r["sponsor_group"] == g and 2021 <= r["tax_year"] <= 2024), g,
                               "2021-2024", "group_pooled") for g in GROUPS)
    ex_schwab = (group_stats(tuple(r for r in rows if r["sponsor_group"] == "affiliated_commercial_national"
                                   and r["ein"] != "311640316" and 2021 <= r["tax_year"] <= 2024),
                             "affiliated_commercial_national_ex_schwab", "2021-2024", "group_pooled"),)
    allrow = tuple(group_stats(tuple(r for r in rows if 2021 <= r["tax_year"] <= 2024 and r["ein"] not in COMPARATORS),
                               "all_ex_comparator", "2021-2024", "group_pooled") for _ in (0,))
    return by_year + pooled + ex_schwab + allrow


# ----------------------------------------------------------------------------- per-sponsor pooled view and rank test
def sponsor_pooled(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    """TY2021-2024 per sponsor: sums of line 12, line 12 + line-24 marketing, DAF contributions; account change from
    the prior count of the first year to the TY2024 count."""
    def one(ein, rs):
        rs = tuple(sorted(rs, key=lambda r: r["tax_year"]))
        adv = sum(r["adv_l12_total"] or 0 for r in rs)
        adv24 = sum(r["adv_plus_l24_strict"] or 0 for r in rs)
        c = sum(r["sd_daf_contributions"] or 0 for r in rs)
        first, last = rs[0], rs[-1]
        # start = count before the first year; if none (new sponsor), the first year's EOY count, and that year's
        # spend then drops out of the per-account ratio window
        from_eoy = first["prior_daf_count"] is None and first["sd_daf_count"] is not None and len(rs) > 1
        start = first["sd_daf_count"] if from_eoy else first["prior_daf_count"]
        d = None if last["sd_daf_count"] is None or start is None or last["tax_year"] != 2024 else last["sd_daf_count"] - start
        adv_w = sum(r["adv_l12_total"] or 0 for r in (rs[1:] if from_eoy else rs))
        adv24_w = sum(r["adv_plus_l24_strict"] or 0 for r in (rs[1:] if from_eoy else rs))
        opex = sum(r["operating_cost_ex_invest"] or 0 for r in rs)
        return {"ein": ein, "sponsor_name": first["sponsor_name"], "sponsor_group": first["sponsor_group"],
                "years": len(rs), "adv_l12": adv, "adv_plus_l24_strict": adv24, "daf_contributions": c,
                "adv_bps_of_daf_contrib": None if not c else round(adv / c * 1e4, 3),
                "adv24_bps_of_daf_contrib": None if not c else round(adv24 / c * 1e4, 3),
                "adv_share_of_opex": None if not opex else round(adv / opex, 4),
                "accounts_start": start, "start_basis": f"eoy_ty{first['tax_year']}" if from_eoy else
                f"prior_to_ty{first['tax_year']} ({first['prior_count_source']})", "accounts_ty2024": last["sd_daf_count"],
                "net_new_accounts_2021_2024": d,
                "account_growth_2021_2024": None if d is None or not start else round(d / start, 4),
                "contrib_growth_ty2021_to_ty2024": None if not (rs[0]["sd_daf_contributions"] and last["tax_year"] == 2024
                                                                and rs[0]["tax_year"] == 2021) else
                round(last["sd_daf_contributions"] / rs[0]["sd_daf_contributions"] - 1, 4),
                "adv_per_net_new_account": None if not d or d <= 0 else round(adv_w / d, 1),
                "adv24_per_net_new_account": None if not d or d <= 0 else round(adv24_w / d, 1),
                "functional_split_prog_mgmt_fr": tuple(round(sum(r[k] or 0 for r in rs) / adv, 3) if adv else None
                                                       for k in ("adv_l12_program", "adv_l12_mgmt", "adv_l12_fundraising")),
                "flags": sorted({f for r in rs for f in r["quality_flags"].split(";") if f})}
    sel = tuple(r for r in rows if 2021 <= r["tax_year"] <= 2024)
    by: dict = {}
    for r in sel:
        by.setdefault(r["ein"], []).append(r)
    return tuple(one(e, rs) for e, rs in by.items())


def ranks(xs: Sequence[float]) -> tuple[float, ...]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return tuple(out)


def spearman(pairs: Sequence[tuple[float, float]]) -> dict:
    if len(pairs) < 5:
        return {"n": len(pairs), "rho": None}
    rx, ry = ranks(tuple(p[0] for p in pairs)), ranks(tuple(p[1] for p in pairs))
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num_ = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return {"n": len(pairs), "rho": round(num_ / den, 3) if den else None}


def rank_tests(pooled: Sequence[Mapping]) -> dict:
    """Marketing intensity (line 12 / operating cost) against account growth and contribution growth, by group."""
    def test(group, ykey):
        ps = tuple((p["adv_share_of_opex"], p[ykey]) for p in pooled
                   if (group == "all" or p["sponsor_group"] == group) and p["adv_share_of_opex"] is not None
                   and p[ykey] is not None and "account_unit_undefined" not in p["flags"]
                   and "campaign_advertising_not_overhead" not in p["flags"]
                   and "university_health_whole_org" not in p["flags"])
        return spearman(ps)
    return {f"{g}|{y}": test(g, y) for g in ("community_foundation", "all") for y in
            ("account_growth_2021_2024", "contrib_growth_ty2021_to_ty2024")}


FIELDS = (
    "row_type", "ein", "sponsor_name", "sponsor_group", "group_basis", "selection", "dafrc_type", "dafrc_subtype",
    "fy2024_asset_rank", "tax_year", "tax_period_begin", "tax_period_end", "period_months", "return_object_id",
    "return_ts", "amended_ind", "xml_source", "xml_url",
    "adv_l12_total", "adv_l12_program", "adv_l12_mgmt", "adv_l12_fundraising", "adv_l12_cost_cache_check",
    "l24_marketing_strict_amt", "l24_marketing_strict_desc", "l24_marketing_broad_amt", "l24_marketing_broad_desc",
    "adv_plus_l24_strict",
    "fees_mgmt_l11a", "fees_legal_l11b", "fees_accounting_l11c", "fees_lobbying_l11d", "fees_prof_fundraising_l11e",
    "fees_invest_mgmt_l11f", "fees_other_l11g", "fees_l11_total",
    "it_l14_total", "it_l14_program", "it_l14_mgmt", "it_l14_fundraising",
    "total_functional_expenses_l25", "fundraising_col_l25", "operating_cost_ex_invest", "adv_share_of_opex",
    "total_contributions_part_i", "total_assets_eoy", "employees",
    "sd_present", "sd_daf_count", "sd_daf_contributions", "sd_daf_grants", "sd_daf_eoy_value",
    "daf_share_of_contributions", "prior_daf_count", "prior_count_source", "net_new_accounts", "account_growth_pct",
    "adv_per_dollar_daf_contrib", "adv_bps_of_daf_contrib", "adv_bps_of_total_contrib", "adv_alloc_daf",
    "adv_alloc_per_new_dollar_bps", "adv_per_net_new_account", "adv_alloc_per_net_new_account",
    "outside_990_marketing_basis", "quality_flags",
    # group rows
    "n_returns", "n_sponsors", "n_l12_positive", "share_l12_positive", "operating_cost_ex_invest",
    "adv_bps_of_daf_contrib_median", "adv_bps_of_daf_contrib_p25", "adv_bps_of_daf_contrib_p75",
    "net_new_accounts", "n_returns_net_new_positive", "adv_per_net_new_account_median",
)


def round_row(r: Mapping) -> dict:
    return {k: (round(v, 4) if isinstance(v, float) and abs(v) < 1e4 and not float(v).is_integer() else
                round(v) if isinstance(v, float) else v) for k, v in r.items()}


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--cost-cache", required=True)
    ap.add_argument("--teos-dir", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args(argv)
    harvest = tuple({**h, "ein": ein9(h["ein"])} for h in read_csv(HARVEST_CSV))
    uni = universe(harvest)
    idx = pick_returns(index_rows(a.irs_dir, frozenset(uni)))
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        exts = dict(zip((i["OBJECT_ID"] for i in idx),
                        ex.map(lambda i: fetch_extract(i["OBJECT_ID"], a.cache_dir, a.teos_dir, a.fetch), idx)))
    status = {}
    for i in idx:
        status[exts[i["OBJECT_ID"]]["xml_status"]] = status.get(exts[i["OBJECT_ID"]]["xml_status"], 0) + 1
    ok = tuple(i for i in idx if exts[i["OBJECT_ID"]]["xml_status"] == "ok")
    base = tuple(return_row({k: uni[i["EIN"]][k] for k in ("ein", "sponsor_name", "sponsor_group", "group_basis",
                                                         "selection", "dafrc_type", "dafrc_subtype", "fy2024_asset_rank")},
                            i, exts[i["OBJECT_ID"]], cost_cache_l12(i["OBJECT_ID"], a.cost_cache)) for i in ok)
    base = tuple(r for r in base if r["tax_year"] and TY_RANGE[0] <= r["tax_year"] <= TY_RANGE[1])
    # one row per sponsor and tax year: keep the longest period, then the latest object id
    keep: dict = {}
    for r in sorted(base, key=lambda r: ((r["period_months"] or 0), r["return_ts"] or "", r["return_object_id"])):
        keep[(r["ein"], r["tax_year"])] = r
    dup_dropped = len(base) - len(keep)
    rows = with_growth(tuple(sorted(keep.values(), key=lambda r: (r["sponsor_group"], r["ein"], r["tax_year"]))),
                       dafrc_lookup(m990.load_dafrc()))
    summ = summaries(rows)
    write_csv(OUT, tuple(round_row(r) for r in rows + summ), FIELDS)
    missing = tuple({"ein": i["EIN"], "period": i["TAX_PERIOD"], "oid": i["OBJECT_ID"],
                     "status": exts[i["OBJECT_ID"]]["xml_status"]} for i in idx if exts[i["OBJECT_ID"]]["xml_status"] != "ok")
    cov = {}
    for r in rows:
        cov.setdefault(r["sponsor_group"], {}).setdefault(r["tax_year"], 0)
        cov[r["sponsor_group"]][r["tax_year"]] += 1
    no_rows = sorted(e for e in uni if e not in {r["ein"] for r in rows})
    pooled = sponsor_pooled(rows)
    show = tuple(p for p in pooled if p["sponsor_group"] not in ("community_foundation", "single_issue"))
    top_cf = tuple(sorted((p for p in pooled if p["sponsor_group"] == "community_foundation"),
                          key=lambda p: -p["adv_l12"]))[:12]
    cf_med = {k: quant(tuple(p[k] for p in pooled if p["sponsor_group"] == "community_foundation" and p[k] is not None), .5)
              for k in ("adv_share_of_opex", "adv_bps_of_daf_contrib", "adv_per_net_new_account", "account_growth_2021_2024")}
    fshare = {g["sponsor_group"]: {k: round(g[k] / g["adv_l12_total"], 3) if g["adv_l12_total"] else None
                                   for k in ("adv_l12_program", "adv_l12_mgmt", "adv_l12_fundraising")}
              for g in summ if g["row_type"] == "group_pooled"}
    print(json.dumps({"functional_shares_pooled": fshare, "sponsor_pooled_nationals_digital": show, "top_cf_by_l12": top_cf, "cf_pooled_medians": cf_med,
                      "rank_tests": rank_tests(pooled)}, indent=1, default=str), file=sys.stderr)
    print(json.dumps({"universe": len(uni), "index_returns": len(idx), "xml_status": status, "missing": missing,
                      "rows": len(rows), "dup_period_dropped": dup_dropped, "coverage": cov,
                      "sponsors_without_rows": [(e, uni[e]["sponsor_name"]) for e in no_rows],
                      "cost_cache_check": {k: sum(1 for r in rows if r["adv_l12_cost_cache_check"] == k)
                                           for k in ("match", "mismatch", "not_in_cost_cache")}},
                     indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
