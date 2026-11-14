#!/usr/bin/env python3
"""Sponsor operating-cost structure from Form 990 Part IX, plus Givinga and SDG Impact Fund sensitivities.

Queue items P-99F-04 (cost structure), P-ASR-03 (Givinga sensitivity), P-99F-02 (SDG Impact Fund treatment).
Stdlib only; functional style (pure transforms, I/O at the edges). Reuses helpers from
scripts/mission_990_contractors.py (number parsing, CSV I/O, XML tag helpers). That script's own extractor stops
after Schedule D and keeps only four Part IX totals; this script adds an *extended* extractor (full Part IX by
column, Part I summary lines, Part III narrative grant mentions, Schedule I recipient counts) with its own cache,
so the earlier harvest outputs are untouched.

Inputs (read only):
  data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv  5,416 returns located / 5,272 parsed (object ids)
  data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv     DAFRC sponsor panel (type, subtype, values)
  data/mission-2026-11-14/dafrc-corrections-itemized.csv              corrected values (applied = 1)
  data/mission-2026-11-14/dafrc-corrected-market-totals.csv           corrected totals (validation of the rebuild)
  data/mission-2026-11-14/non-dafrc-daf-filers-990.csv                SDG Impact Fund rows (EIN 462368538)
  data/mission-2026-11-14/sponsor-level-metrics.csv                   self-reported grant counts (grant_count rows)
  Form 990 XML  https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml
Outputs:
  data/mission-2026-11-14/sponsor-cost-structure.csv           one row per parsed sponsor return (sponsor-year)
  data/mission-2026-11-14/sponsor-cost-structure-summary.csv   group statistics, scale elasticities, grant-count anchors
  data/mission-2026-11-14/market-sensitivity-givinga-sdg.csv   P-ASR-03 and P-99F-02 sensitivity tables

Usage:
  python3 scripts/mission_sponsor_cost_structure.py --cache-dir CACHE [--fetch] [--task all|extract|cost|givinga|sdg]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as m990  # noqa: E402

DATA = m990.DATA
HARVEST_CSV = os.path.join(DATA, "form990-returns-schedule-d-harvest-full.csv")
ITEMIZED_CSV = os.path.join(DATA, "dafrc-corrections-itemized.csv")
CORRECTED_TOTALS_CSV = os.path.join(DATA, "dafrc-corrected-market-totals.csv")
NON_DAFRC_CSV = os.path.join(DATA, "non-dafrc-daf-filers-990.csv")
METRICS_CSV = os.path.join(DATA, "sponsor-level-metrics.csv")
OUT_ROWS = os.path.join(DATA, "sponsor-cost-structure.csv")
OUT_SUMMARY = os.path.join(DATA, "sponsor-cost-structure-summary.csv")
OUT_SENS = os.path.join(DATA, "market-sensitivity-givinga-sdg.csv")
NS = m990.NS
XML_URL = m990.XML_URL
DAFRC_URL = m990.DAFRC_URL
EXTRACT_VERSION = 1
GIVINGA_EIN = "474172718"
PAYPAL_EIN = "450931286"
SDG_EIN = "462368538"

# Part IX line -> e-file group tag (IRS 990 schema 2020+). 11e has no "Grp" suffix in the schema.
PART_IX = (
    ("l01_grants_domestic_orgs", "GrantsToDomesticOrgsGrp"),
    ("l02_grants_domestic_individuals", "GrantsToDomesticIndividualsGrp"),
    ("l03_grants_foreign", "ForeignGrantsGrp"),
    ("l04_benefits_to_members", "BenefitsToMembersGrp"),
    ("l05_comp_officers_directors", "CompCurrentOfcrDirectorsGrp"),
    ("l06_comp_disqualified", "CompDisqualPersonsGrp"),
    ("l07_other_salaries_wages", "OtherSalariesAndWagesGrp"),
    ("l08_pension", "PensionPlanContributionsGrp"),
    ("l09_other_benefits", "OtherEmployeeBenefitsGrp"),
    ("l10_payroll_taxes", "PayrollTaxesGrp"),
    ("l11a_fees_management", "FeesForServicesManagementGrp"),
    ("l11b_fees_legal", "FeesForServicesLegalGrp"),
    ("l11c_fees_accounting", "FeesForServicesAccountingGrp"),
    ("l11d_fees_lobbying", "FeesForServicesLobbyingGrp"),
    ("l11e_fees_prof_fundraising", "FeesForServicesProfFundraising"),
    ("l11f_fees_investment_mgmt", "FeesForSrvcInvstMgmntFeesGrp"),
    ("l11g_fees_other", "FeesForServicesOtherGrp"),
    ("l12_advertising", "AdvertisingGrp"),
    ("l13_office", "OfficeExpensesGrp"),
    ("l14_information_technology", "InformationTechnologyGrp"),
    ("l15_royalties", "RoyaltiesGrp"),
    ("l16_occupancy", "OccupancyGrp"),
    ("l17_travel", "TravelGrp"),
    ("l18_travel_officials", "PymtTravelEntrtnmntPubOfclGrp"),
    ("l19_conferences", "ConferencesMeetingsGrp"),
    ("l20_interest", "InterestGrp"),
    ("l21_payments_affiliates", "PaymentsToAffiliatesGrp"),
    ("l22_depreciation", "DepreciationDepletionGrp"),
    ("l23_insurance", "InsuranceGrp"),
    ("l24_other_expenses", "OtherExpensesGrp"),          # repeating (24a-d) -> summed
    ("l24e_all_other", "AllOtherExpensesGrp"),
    ("l25_total", "TotalFunctionalExpensesGrp"),
)
TAG_TO_LINE = {t: k for k, t in PART_IX}
COLS = (("total", "TotalAmt"), ("program", "ProgramServicesAmt"),
        ("mgmt", "ManagementAndGeneralAmt"), ("fundraising", "FundraisingAmt"))
PART_I = ("TotalEmployeeCnt", "TotalVolunteersCnt", "CYContributionsGrantsAmt", "CYInvestmentIncomeAmt",
          "CYTotalRevenueAmt", "CYGrantsAndSimilarPaidAmt", "CYSalariesCompEmpBnftPaidAmt",
          "CYTotalProfFndrsngExpnsAmt", "CYTotalFundraisingExpenseAmt", "CYOtherExpensesAmt", "CYTotalExpensesAmt",
          "TotalAssetsBOYAmt", "TotalAssetsEOYAmt", "NetAssetsOrFundBalancesEOYAmt")
NARRATIVE_TAGS = frozenset({"DescriptionProgramSrvcAccomTxt", "Desc"})
GRANT_MENTION = re.compile(r"(\d{1,3}(?:,\d{3})+|\d{3,})\s+(?:individual\s+|separate\s+|charitable\s+|total\s+)?grants\b", re.I)


# ----------------------------------------------------------------------------- small pure helpers
num, fmt, ein9, read_csv, write_csv = m990.num, m990.fmt, m990.ein9, m990.read_csv, m990.write_csv
local = m990.local


def group_by(items: Iterable, key: Callable) -> dict:
    return m990._group_by_fast(items, key)


def ssum(*xs) -> float | None:
    vals = tuple(x for x in xs if x is not None)
    return sum(vals) if vals else None


def div(a, b) -> float | None:
    return a / b if a is not None and b not in (None, 0) else None


def clip01(x) -> float | None:
    return None if x is None else max(0.0, min(1.0, x))


def quantile(xs: Sequence[float], q: float) -> float | None:
    s = sorted(xs)
    if not s:
        return None
    pos = (len(s) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def ols(xs: Sequence[float], ys: Sequence[float]) -> tuple[float, float, float] | None:
    """Slope, intercept, r2 of y on x. Pure."""
    n = len(xs)
    if n < 5:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    icpt = my - slope * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - icpt - slope * x) ** 2 for x, y in zip(xs, ys))
    return slope, icpt, (1 - ss_res / ss_tot) if ss_tot else 0.0


# ----------------------------------------------------------------------------- extended XML extract (streamed)
def part_ix_from(el) -> dict:
    """{line_key: {col: amount}} for every Part IX group that is a direct child of IRS990. Repeating groups summed."""
    def cols(g) -> dict:
        return {c: num(m990.text_of(g, (t,))) for c, t in COLS}
    groups = tuple((TAG_TO_LINE[local(c.tag)], cols(c)) for c in el if local(c.tag) in TAG_TO_LINE)
    by = group_by(groups, lambda kv: kv[0])
    return {k: {c: ssum(*(v[1][c] for v in vs)) for c, _ in COLS} for k, vs in by.items()}


def narrative_from(el) -> tuple[str, ...]:
    return tuple((x.text or "").strip() for x in el.iter()
                 if local(x.tag) in NARRATIVE_TAGS and x.text and "grant" in x.text.lower())


def extract_cost_stream(stream) -> dict:
    """Stream-parse a whole return: header, IRS990 (Part I, Part III text, Part IX), Schedule D Part I, Schedule I
    counts. RecipientTable rows are counted and cleared as they close, so memory stays flat."""
    out: dict = {"sched_i_present": 0, "sched_i_recipient_rows": 0, "sched_d_present": 0}
    in_sched_i = False
    for event, el in ET.iterparse(stream, events=("start", "end")):
        tag = local(el.tag)
        if event == "start":
            in_sched_i = in_sched_i or tag == "IRS990ScheduleI"
            continue
        if tag == "ReturnHeader":
            out.update({"tax_period_end": m990.text_of(el, ("TaxPeriodEndDt",)),
                        "tax_period_begin": m990.text_of(el, ("TaxPeriodBeginDt",)),
                        "return_ts": m990.text_of(el, ("ReturnTs",)),
                        "return_type": m990.text_of(el, ("ReturnTypeCd",))})
            el.clear()
        elif tag == "IRS990":
            out.update({"part_i": {t: num(m990.text_of(el, (t,))) for t in PART_I},
                        "part_ix": part_ix_from(el),
                        "narrative": list(narrative_from(el))[:12],
                        "amended_ind": m990.text_of(el, ("AmendedReturnInd",)),
                        "audited_fs_ind": m990.text_of(el, ("FSAuditedInd",)) or m990.text_of(el, ("IndependentAuditFinclStmtInd",))})
            el.clear()
        elif tag == "IRS990ScheduleD":
            out.update({"sched_d_present": 1,
                        "sched_d_daf_count": num(m990.text_of(el, ("DonorAdvisedFundsHeldCnt",))),
                        "sched_d_daf_contributions": num(m990.text_of(el, ("DonorAdvisedFundsContriAmt",))),
                        "sched_d_daf_grants": num(m990.text_of(el, ("DonorAdvisedFundsGrantsAmt",))),
                        "sched_d_daf_eoy_value": num(m990.text_of(el, ("DonorAdvisedFundsVlEOYAmt",)))})
            el.clear()
        elif in_sched_i and tag == "RecipientTable":
            out["sched_i_recipient_rows"] += 1
            el.clear()
        elif tag == "IRS990ScheduleI":
            indiv = tuple(num(m990.text_of(g, ("RecipientCnt",))) for g in el.iter(NS + "GrantsOtherAsstToIndivInUSGrp"))
            out.update({"sched_i_present": 1,
                        "sched_i_501c3_org_cnt": num(m990.text_of(el, ("Total501c3OrgCnt",))),
                        "sched_i_other_org_cnt": num(m990.text_of(el, ("TotalOtherOrgCnt",))),
                        "sched_i_individual_recipient_cnt": ssum(*indiv)})
            in_sched_i = False
            el.clear()
        elif tag.startswith("IRS990Schedule"):
            el.clear()
    return out


def fetch_cost_extract(oid: str, cache_dir: str, fetch: bool, retries: int = 2) -> dict:
    path = os.path.join(cache_dir, "extract990cost", f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            cached = json.load(fh)
        if cached.get("_v") == EXTRACT_VERSION:
            return cached
    if not fetch:
        return {"xml_status": "not_fetched"}
    url = XML_URL.format(oid=oid)
    req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    out = {"xml_status": "error:none"}
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                out = {**extract_cost_stream(resp), "xml_status": "ok"}
            break
        except urllib.error.HTTPError as e:
            out = {"xml_status": f"http_{e.code}"}
            if e.code in (403, 404):
                break
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
            out = {"xml_status": f"error:{type(e).__name__}"}
            time.sleep(2 * (attempt + 1))
    result = {**out, "_v": EXTRACT_VERSION, "xml_url": url}
    if not result["xml_status"].startswith("error"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(result, fh)
    return result


def fetch_all(oids: Sequence[str], cache_dir: str, fetch: bool, workers: int) -> dict[str, dict]:
    uniq = tuple(dict.fromkeys(oids))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return dict(zip(uniq, ex.map(lambda o: fetch_cost_extract(o, cache_dir, fetch), uniq)))


# ----------------------------------------------------------------------------- classification
def category(type_: str, subtype: str) -> str:
    return {("National", "Standard"): "National-Standard", ("National", "Donation Processor"): "National-Processor",
            ("Community Foundation", "Community"): "Community",
            ("Single Issue Charity", "Religiously-Affiliated"): "SingleIssue-Religious",
            ("Single Issue Charity", "Universities and Healthcare"): "SingleIssue-UnivHealth",
            ("Single Issue Charity", "Other"): "SingleIssue-Other"}.get((type_, subtype), f"{type_}/{subtype}")


SIZE_BANDS = ((10e6, "a <$10m"), (50e6, "b $10-50m"), (250e6, "c $50-250m"), (1e9, "d $250m-1bn"),
              (10e9, "e $1-10bn"), (float("inf"), "f >$10bn"))


def size_band(daf_assets) -> str:
    if daf_assets is None or daf_assets <= 0:
        return "z no DAF value"
    return next(lbl for ub, lbl in SIZE_BANDS if daf_assets < ub)


def grant_mention(texts: Sequence[str]) -> tuple[float | None, str]:
    hits = tuple((m, t) for t in texts for m in GRANT_MENTION.finditer(t))
    if not hits:
        return None, ""
    m, t = max(hits, key=lambda h: num(h[0].group(1)) or 0)
    lo = max(0, m.start() - 90)
    return num(m.group(1)), re.sub(r"\s+", " ", t[lo:m.end() + 40])


# ----------------------------------------------------------------------------- per sponsor-year cost row (pure)
def cost_row(h: Mapping, x: Mapping, dafrc: Mapping) -> dict:
    ix = x.get("part_ix", {}) or {}
    p1 = x.get("part_i", {}) or {}
    L = lambda k, c="total": (ix.get(k) or {}).get(c)  # noqa: E731
    tfe = L("l25_total") if L("l25_total") is not None else p1.get("CYTotalExpensesAmt")
    grants = ssum(L("l01_grants_domestic_orgs"), L("l02_grants_domestic_individuals"), L("l03_grants_foreign"))
    benefits = L("l04_benefits_to_members")
    opex = None if tfe is None else tfe - (grants or 0) - (benefits or 0)
    staff = ssum(*(L(k) for k in ("l05_comp_officers_directors", "l06_comp_disqualified", "l07_other_salaries_wages",
                                    "l08_pension", "l09_other_benefits", "l10_payroll_taxes")))
    fee_keys = ("l11a_fees_management", "l11b_fees_legal", "l11c_fees_accounting", "l11d_fees_lobbying",
                "l11e_fees_prof_fundraising", "l11f_fees_investment_mgmt", "l11g_fees_other")
    outside = ssum(*(L(k) for k in fee_keys))
    inv = L("l11f_fees_investment_mgmt")
    it = L("l14_information_technology")
    opex_ex_inv = None if opex is None else opex - (inv or 0)
    occupancy_office = ssum(L("l13_office"), L("l16_occupancy"), L("l22_depreciation"), L("l23_insurance"))
    other_lines = None if opex is None else opex - sum(v or 0 for v in (staff, outside, it, occupancy_office))
    ta_eoy = p1.get("TotalAssetsEOYAmt") if p1.get("TotalAssetsEOYAmt") is not None else num(h.get("total_assets_eoy"))
    ta_boy = p1.get("TotalAssetsBOYAmt")
    ta_avg = (ta_eoy + ta_boy) / 2 if ta_eoy is not None and ta_boy is not None else ta_eoy
    daf_v = x.get("sched_d_daf_eoy_value", num(h.get("sched_d_daf_eoy_value")))
    daf_n = x.get("sched_d_daf_count", num(h.get("sched_d_daf_count")))
    daf_g = x.get("sched_d_daf_grants", num(h.get("sched_d_daf_grants")))
    dafrc_v = num(dafrc.get("eoy_daf_assets")) if dafrc else None
    dafrc_n = num(dafrc.get("number_of_daf_accounts")) if dafrc else None
    daf_v_used = daf_v if daf_v not in (None, 0) else dafrc_v
    daf_n_used = daf_n if daf_n not in (None, 0) else dafrc_n
    share_a_raw = div(daf_v_used, ta_eoy)
    share_g_raw = div(daf_g, grants)
    share_a, share_g = clip01(share_a_raw), clip01(share_g_raw)
    alloc_a = None if opex_ex_inv is None or share_a is None else opex_ex_inv * share_a
    alloc_g = None if opex_ex_inv is None or share_g is None else opex_ex_inv * share_g
    mention, snippet = grant_mention(x.get("narrative", ()))
    sched_i_recips = ssum(x.get("sched_i_501c3_org_cnt"), x.get("sched_i_other_org_cnt"), x.get("sched_i_individual_recipient_cnt"))
    flags = tuple(f for f, cond in (
        ("givinga_undefined_account_unit", h["ein"] == GIVINGA_EIN),
        ("tfe_missing", tfe is None),
        ("opex_nonpositive", opex is not None and opex <= 0),
        ("no_daf_value", daf_v_used in (None, 0)),
        ("daf_value_gt_total_assets", share_a_raw is not None and share_a_raw > 1.0001),
        ("daf_grants_gt_part_ix_grants", share_g_raw is not None and share_g_raw > 1.0001),
        ("daf_share_assets_lt_5pct", share_a is not None and share_a < 0.05),
        ("daf_value_from_dafrc", daf_v in (None, 0) and dafrc_v not in (None, 0)),
        ("accounts_from_dafrc", daf_n in (None, 0) and dafrc_n not in (None, 0)),
        ("amended_return", bool(x.get("amended_ind"))),
    ) if cond)
    return {
        "ein": h["ein"], "sponsor_name": h["sponsor_name"], "category": category(h["type"], h["subtype"]),
        "type": h["type"], "subtype": h["subtype"], "fiscal_year": int(h["fiscal_year"]), "tax_period": h["tax_period"],
        "size_band_daf_assets": size_band(daf_v_used),
        "return_object_id": h["return_object_id"], "return_ts": x.get("return_ts") or h.get("return_ts"),
        "total_functional_expenses": tfe, "grants_part_ix_l1_3": grants, "benefits_l4": benefits,
        "operating_cost": opex, "operating_cost_ex_invest_mgmt": opex_ex_inv,
        "staff_cost_l5_10": staff, "salaries_l7": L("l07_other_salaries_wages"),
        "comp_officers_l5": L("l05_comp_officers_directors"),
        "outside_services_l11": outside, "fees_mgmt_l11a": L("l11a_fees_management"), "fees_legal_l11b": L("l11b_fees_legal"),
        "fees_accounting_l11c": L("l11c_fees_accounting"), "fees_prof_fundraising_l11e": L("l11e_fees_prof_fundraising"),
        "fees_invest_mgmt_l11f": inv, "fees_other_l11g": L("l11g_fees_other"),
        "it_l14": it, "advertising_l12": L("l12_advertising"), "occupancy_office_ins_depr": occupancy_office,
        "other_expense_lines": other_lines,
        "program_col_total": L("l25_total", "program"), "mgmt_col_total": L("l25_total", "mgmt"),
        "fundraising_col_total": L("l25_total", "fundraising"),
        "program_col_ex_grants": None if L("l25_total", "program") is None else L("l25_total", "program") - (grants or 0) - (benefits or 0),
        "it_mgmt_col": L("l14_information_technology", "mgmt"), "it_program_col": L("l14_information_technology", "program"),
        "employees": p1.get("TotalEmployeeCnt"), "total_revenue": p1.get("CYTotalRevenueAmt"),
        "total_assets_eoy": ta_eoy, "total_assets_avg": ta_avg,
        "daf_assets_eoy": daf_v_used, "daf_accounts": daf_n_used, "daf_grants": daf_g,
        "daf_contributions": x.get("sched_d_daf_contributions", num(h.get("sched_d_daf_contributions"))),
        "dafrc_daf_assets_same_fy": dafrc_v, "dafrc_accounts_same_fy": dafrc_n,
        "daf_share_of_total_assets": share_a, "daf_share_of_grants": share_g,
        "opex_bps_of_total_assets": div(opex_ex_inv, ta_avg) and div(opex_ex_inv, ta_avg) * 1e4,
        "opex_incl_invest_bps_of_total_assets": div(opex, ta_avg) and div(opex, ta_avg) * 1e4,
        "opex_share_of_tfe": div(opex, tfe),
        "it_share_of_opex": div(it, opex_ex_inv), "outside_ex_invest_share_of_opex": div(None if outside is None else outside - (inv or 0), opex_ex_inv),
        "staff_share_of_opex": div(staff, opex_ex_inv),
        "it_bps_of_total_assets": div(it, ta_avg) and div(it, ta_avg) * 1e4,
        "daf_alloc_opex_by_assets": alloc_a, "daf_alloc_opex_by_grants": alloc_g,
        "opex_per_account_unallocated": div(opex_ex_inv, daf_n_used),
        "daf_opex_per_account_assets_alloc": div(alloc_a, daf_n_used),
        "daf_opex_per_account_grants_alloc": div(alloc_g, daf_n_used),
        "daf_it_per_account_assets_alloc": div(None if it is None or share_a is None else it * share_a, daf_n_used),
        "daf_opex_bps_of_daf_assets_grants_alloc": div(alloc_g, daf_v_used) and div(alloc_g, daf_v_used) * 1e4,
        "opex_per_employee": div(opex_ex_inv, p1.get("TotalEmployeeCnt")),
        "daf_assets_per_employee": div(daf_v_used, p1.get("TotalEmployeeCnt")),
        "sched_i_recipients": sched_i_recips, "sched_i_recipient_rows": x.get("sched_i_recipient_rows"),
        "opex_per_sched_i_recipient": div(opex_ex_inv, sched_i_recips),
        "narrative_grant_mention": mention, "narrative_grant_snippet": snippet,
        "audited_fs_ind": x.get("audited_fs_ind"),
        "quality_flags": ";".join(flags), "xml_url": x.get("xml_url"),
        "source_url": h.get("source_url"),
    }


COST_FIELDS = ("ein", "sponsor_name", "category", "type", "subtype", "fiscal_year", "tax_period", "size_band_daf_assets",
               "total_functional_expenses", "grants_part_ix_l1_3", "benefits_l4", "operating_cost",
               "operating_cost_ex_invest_mgmt", "staff_cost_l5_10", "comp_officers_l5", "salaries_l7",
               "outside_services_l11", "fees_mgmt_l11a", "fees_legal_l11b", "fees_accounting_l11c",
               "fees_prof_fundraising_l11e", "fees_invest_mgmt_l11f", "fees_other_l11g", "it_l14", "advertising_l12",
               "occupancy_office_ins_depr", "other_expense_lines", "program_col_total", "program_col_ex_grants",
               "mgmt_col_total", "fundraising_col_total", "it_program_col", "it_mgmt_col", "employees", "total_revenue",
               "total_assets_eoy", "total_assets_avg", "daf_assets_eoy", "daf_accounts", "daf_contributions", "daf_grants",
               "dafrc_daf_assets_same_fy", "dafrc_accounts_same_fy", "daf_share_of_total_assets", "daf_share_of_grants",
               "opex_share_of_tfe", "opex_bps_of_total_assets", "opex_incl_invest_bps_of_total_assets",
               "it_share_of_opex", "outside_ex_invest_share_of_opex", "staff_share_of_opex", "it_bps_of_total_assets",
               "daf_alloc_opex_by_assets", "daf_alloc_opex_by_grants", "opex_per_account_unallocated",
               "daf_opex_per_account_assets_alloc", "daf_opex_per_account_grants_alloc", "daf_it_per_account_assets_alloc",
               "daf_opex_bps_of_daf_assets_grants_alloc", "opex_per_employee", "daf_assets_per_employee",
               "sched_i_recipients", "sched_i_recipient_rows", "opex_per_sched_i_recipient", "narrative_grant_mention",
               "narrative_grant_snippet", "audited_fs_ind", "quality_flags", "return_object_id", "return_ts", "xml_url",
               "source_url")


# ----------------------------------------------------------------------------- summary statistics (pure)
# metric -> (numerator field, denominator field, scale, row filter description)
RATIO_METRICS = (
    ("opex_bps_of_total_assets", "operating_cost_ex_invest_mgmt", "total_assets_avg", 1e4),
    ("opex_incl_invest_bps_of_total_assets", "operating_cost", "total_assets_avg", 1e4),
    ("opex_share_of_tfe", "operating_cost", "total_functional_expenses", 1),
    ("it_share_of_opex", "it_l14", "operating_cost_ex_invest_mgmt", 1),
    ("outside_ex_invest_share_of_opex", None, None, 1),
    ("staff_share_of_opex", "staff_cost_l5_10", "operating_cost_ex_invest_mgmt", 1),
    ("it_bps_of_total_assets", "it_l14", "total_assets_avg", 1e4),
    ("daf_share_of_total_assets", "daf_assets_eoy", "total_assets_eoy", 1),
    ("daf_share_of_grants", "daf_grants", "grants_part_ix_l1_3", 1),
    ("opex_per_account_unallocated", "operating_cost_ex_invest_mgmt", "daf_accounts", 1),
    ("daf_opex_per_account_assets_alloc", "daf_alloc_opex_by_assets", "daf_accounts", 1),
    ("daf_opex_per_account_grants_alloc", "daf_alloc_opex_by_grants", "daf_accounts", 1),
    ("daf_it_per_account_assets_alloc", None, None, 1),
    ("daf_opex_bps_of_daf_assets_grants_alloc", "daf_alloc_opex_by_grants", "daf_assets_eoy", 1e4),
    ("opex_per_employee", "operating_cost_ex_invest_mgmt", "employees", 1),
    ("daf_assets_per_employee", "daf_assets_eoy", "employees", 1),
    ("opex_per_sched_i_recipient", "operating_cost_ex_invest_mgmt", "sched_i_recipients", 1),
)
LEVEL_METRICS = ("operating_cost_ex_invest_mgmt", "it_l14", "outside_services_l11", "fees_accounting_l11c",
                 "fees_invest_mgmt_l11f", "fees_other_l11g", "staff_cost_l5_10", "employees")


def analysable(r: Mapping) -> bool:
    flags = r["quality_flags"].split(";")
    return not any(f in flags for f in ("tfe_missing", "opex_nonpositive", "givinga_undefined_account_unit"))


def per_account_ok(r: Mapping, metric: str) -> bool:
    if "account" not in metric:
        return True
    return (r.get("daf_accounts") or 0) >= 1


def stats_rows(rows: Sequence[Mapping], fy: int, dim: str, cat: str, band: str) -> tuple[dict, ...]:
    base = tuple(r for r in rows if analysable(r))

    def ratio_row(metric, nf, df, scale):
        sub = tuple(r for r in base if r.get(metric) is not None and per_account_ok(r, metric))
        vals = tuple(r[metric] for r in sub)
        agg = None
        nsum = dsum = None
        if nf and df:
            pairs = tuple((r[nf], r[df]) for r in sub if r.get(nf) is not None and r.get(df) not in (None, 0))
            nsum, dsum = sum(p[0] for p in pairs), sum(p[1] for p in pairs)
            agg = div(nsum, dsum) and div(nsum, dsum) * scale
        return {"fiscal_year": fy, "dimension": dim, "category": cat, "size_band": band, "metric": metric,
                "n": len(vals), "p25": quantile(vals, .25), "median": quantile(vals, .5), "p75": quantile(vals, .75),
                "aggregate_ratio": agg, "numerator_sum": nsum, "denominator_sum": dsum}

    def level_row(metric):
        vals = tuple(r[metric] for r in base if r.get(metric) is not None)
        return {"fiscal_year": fy, "dimension": dim, "category": cat, "size_band": band, "metric": metric + "_level",
                "n": len(vals), "p25": quantile(vals, .25), "median": quantile(vals, .5), "p75": quantile(vals, .75),
                "numerator_sum": sum(vals) if vals else None}
    return tuple(ratio_row(*m) for m in RATIO_METRICS) + tuple(level_row(m) for m in LEVEL_METRICS)


def elasticity_rows(rows: Sequence[Mapping], fy: int) -> tuple[dict, ...]:
    """log-log OLS of cost on scale. Slope < 1 means cost rises less than proportionally (scale economies)."""
    specs = (
        ("National-Standard", "operating_cost_ex_invest_mgmt", "daf_assets_eoy", "opex vs DAF assets"),
        ("National-Standard", "operating_cost_ex_invest_mgmt", "daf_accounts", "opex vs DAF accounts"),
        ("National-Standard", "it_l14", "daf_assets_eoy", "IT vs DAF assets (IT>0)"),
        ("Community", "operating_cost_ex_invest_mgmt", "total_assets_avg", "whole-org opex vs total assets"),
        ("Community", "daf_alloc_opex_by_assets", "daf_accounts", "asset-allocated DAF opex vs DAF accounts"),
        ("Community", "it_l14", "total_assets_avg", "IT vs total assets (IT>0)"),
        ("Community", "operating_cost_ex_invest_mgmt", "employees", "opex vs employees"),
        ("SingleIssue-Religious", "operating_cost_ex_invest_mgmt", "total_assets_avg", "whole-org opex vs total assets"),
        ("SingleIssue-Other", "operating_cost_ex_invest_mgmt", "total_assets_avg", "whole-org opex vs total assets"),
        ("ALL_EX_PROCESSOR", "operating_cost_ex_invest_mgmt", "total_assets_avg", "whole-org opex vs total assets"),
    )

    def one(cat, yf, xf, label):
        sub = tuple(r for r in rows if analysable(r) and (cat == "ALL_EX_PROCESSOR" and r["category"] != "National-Processor"
                                                          or r["category"] == cat)
                    and (r.get(yf) or 0) > 0 and (r.get(xf) or 0) > 0)
        fit = ols(tuple(math.log(r[xf]) for r in sub), tuple(math.log(r[yf]) for r in sub))
        return {"fiscal_year": fy, "dimension": "elasticity", "category": cat, "size_band": "all",
                "metric": f"elasticity:{yf}~{xf}", "n": len(sub),
                "elasticity": fit[0] if fit else None, "r2": fit[2] if fit else None, "note": label}
    return tuple(one(*s) for s in specs)


def grant_anchor_rows(cost: Sequence[Mapping], metrics: Sequence[Mapping]) -> tuple[dict, ...]:
    """Self-reported (or 990-narrative) grant counts matched to the sponsor's 990 with the nearest period end."""
    gc = tuple(m for m in metrics if m["metric"] == "grant_count")
    by_ein = group_by(cost, lambda r: r["ein"])

    def months(a: str, b: str) -> int:
        return (int(a[:4]) * 12 + int(a[5:7])) - (int(b[:4]) * 12 + int(b[4:6]))

    def one(m):
        cands = tuple(r for r in by_ein.get(ein9(m["ein"]), ()) if r.get("operating_cost_ex_invest_mgmt"))
        if not cands:
            return None
        r = min(cands, key=lambda r: abs(months(m["period_end"], r["tax_period"])))
        g = num(m["value"])
        return {"fiscal_year": r["fiscal_year"], "dimension": "grant_count_anchor", "category": r["category"],
                "size_band": r["size_band_daf_assets"], "metric": "opex_per_grant_selfreported_count",
                "n": 1, "median": div(r["operating_cost_ex_invest_mgmt"], g),
                "numerator_sum": r["operating_cost_ex_invest_mgmt"], "denominator_sum": g,
                "staff_cost_per_grant": div(r["staff_cost_l5_10"], g), "it_per_grant": div(r["it_l14"], g),
                "outside_services_ex_invest_per_grant": div(None if r["outside_services_l11"] is None else
                                                            r["outside_services_l11"] - (r["fees_invest_mgmt_l11f"] or 0), g),
                "note": (f"{m['sponsor']} ({r['ein']}): {m['value_qualifier']} grant count {m['value']} for period ending "
                         f"{m['period_end']} ({m['period_basis']}); 990 period {r['tax_period']} "
                         f"(gap {months(m['period_end'], r['tax_period'])} months); count source {m['source_url']}; 990 {r['xml_url']}")}
    return tuple(x for x in map(one, gc) if x)


def pool_rows(rows: Sequence[Mapping], fy: int) -> tuple[dict, ...]:
    """Market-level DAF operating-cost pool: whole-organisation cost lines allocated to DAFs by the sponsor's DAF share
    of total assets (A) or of Part IX grants (G). Sums over analysable rows; ratio = bps of the rows' DAF assets."""
    def sh(r, basis):
        return r.get("daf_share_of_total_assets") if basis == "A" else r.get("daf_share_of_grants")

    def pool(sub, line, basis):
        if line == "outside_ex_invest":
            val = lambda r: None if r.get("outside_services_l11") is None else r["outside_services_l11"] - (r.get("fees_invest_mgmt_l11f") or 0)  # noqa: E731
        else:
            val = lambda r: r.get(line)  # noqa: E731
        pairs = tuple((val(r) * sh(r, basis), r.get("daf_assets_eoy") or 0, r.get("daf_accounts") or 0)
                      for r in sub if val(r) is not None and sh(r, basis) is not None)
        return pairs

    groups = (("ALL_EX_UNIVHEALTH", lambda r: r["category"] != "SingleIssue-UnivHealth"),) + tuple(
        (c, (lambda c: lambda r: r["category"] == c)(c)) for c in sorted({r["category"] for r in rows}))
    out = []
    for gname, gf in groups:
        sub = tuple(r for r in rows if analysable(r) and gf(r))
        for line in ("operating_cost_ex_invest_mgmt", "staff_cost_l5_10", "outside_ex_invest", "it_l14", "fees_invest_mgmt_l11f"):
            for basis in ("A", "G"):
                pairs = pool(sub, line, basis)
                if not pairs:
                    continue
                num_, assets, accts = sum(p[0] for p in pairs), sum(p[1] for p in pairs), sum(p[2] for p in pairs)
                out.append({"fiscal_year": fy, "dimension": "daf_cost_pool", "category": gname, "size_band": "all",
                            "metric": f"pool:{line}:alloc_{'assets' if basis == 'A' else 'grants'}", "n": len(pairs),
                            "numerator_sum": num_, "denominator_sum": assets,
                            "aggregate_ratio": div(num_, assets) and div(num_, assets) * 1e4,
                            "median": div(num_, accts),
                            "note": "aggregate_ratio = allocated cost in bps of DAF assets; median field = allocated cost per DAF account (sum/sum)"})
    return tuple(out)


SUMMARY_FIELDS = ("fiscal_year", "dimension", "category", "size_band", "metric", "n", "p25", "median", "p75",
                  "aggregate_ratio", "numerator_sum", "denominator_sum", "elasticity", "r2", "staff_cost_per_grant",
                  "it_per_grant", "outside_services_ex_invest_per_grant", "note")


def summarise(cost: Sequence[Mapping], metrics: Sequence[Mapping]) -> tuple[dict, ...]:
    fys = (2022, 2023, 2024)
    cats = sorted({r["category"] for r in cost})
    bands = sorted({r["size_band_daf_assets"] for r in cost})
    out = []
    for fy in fys:
        rf = tuple(r for r in cost if r["fiscal_year"] == fy)
        out += stats_rows(rf, fy, "all", "ALL", "all")
        out += stats_rows(tuple(r for r in rf if r["category"] != "National-Processor"), fy, "all", "ALL_EX_PROCESSOR", "all")
        for c in cats:
            out += stats_rows(tuple(r for r in rf if r["category"] == c), fy, "category", c, "all")
        for b in bands:
            out += stats_rows(tuple(r for r in rf if r["size_band_daf_assets"] == b), fy, "size_band", "ALL", b)
        for c in ("National-Standard", "Community", "SingleIssue-Religious", "SingleIssue-Other", "SingleIssue-UnivHealth"):
            for b in bands:
                sub = tuple(r for r in rf if r["category"] == c and r["size_band_daf_assets"] == b)
                if sub:
                    out += stats_rows(sub, fy, "category_x_size_band", c, b)
        out += elasticity_rows(rf, fy)
        out += pool_rows(rf, fy)
    out += grant_anchor_rows(cost, metrics)
    return tuple(r for r in out if r.get("n"))


# ----------------------------------------------------------------------------- P-ASR-03 / P-99F-02 sensitivity (pure)
VAL_COLS = {"daf_assets_eoy": "eoy_daf_assets", "daf_contributions": "total_daf_contributions",
            "daf_grants": "total_daf_grants", "daf_accounts_eoy": "number_of_daf_accounts"}
SRC_COLS = {"daf_assets_eoy": "source_eoy_daf_assets", "daf_accounts_eoy": "source_number_of_accounts"}


def panel_published(dafrc: Sequence[Mapping]) -> dict:
    return {(r["fy"], r["ein"]): {"name": r["name"], "type": r["type"], "subtype": r["subtype"],
                                  **{m: num(r[c]) for m, c in VAL_COLS.items()},
                                  **{f"src_{m}": r[c] for m, c in SRC_COLS.items()}} for r in dafrc}


def panel_corrected(pub: Mapping, items: Sequence[Mapping], dafrc: Sequence[Mapping]) -> dict:
    sub_of = {r["ein"]: (r["type"], r["subtype"]) for r in sorted(dafrc, key=lambda r: r["fy"])}
    applied = tuple(i for i in items if i["applied"] == "1")
    new_keys = {(int(i["fiscal_year"]), ein9(i["ein"])): i for i in applied if (int(i["fiscal_year"]), ein9(i["ein"])) not in pub}
    base = {**pub, **{k: {"name": i["name"], "type": sub_of.get(k[1], (i["type"], ""))[0],
                          "subtype": sub_of.get(k[1], (i["type"], ""))[1], **{m: None for m in VAL_COLS}}
                      for k, i in new_keys.items()}}
    patches = group_by(applied, lambda i: (int(i["fiscal_year"]), ein9(i["ein"])))
    return {k: {**v, **{i["metric"]: num(i["corrected_value"]) for i in patches.get(k, ())},
                **({"corrected_src": "R4_added"} if k in new_keys else {})} for k, v in base.items()}


def is_processor(v: Mapping) -> bool:
    return v.get("subtype") == "Donation Processor"


def market_stats(panel: Mapping, fy: int, exclude: frozenset = frozenset(), add: Sequence[Mapping] = ()) -> dict:
    rows = tuple({**v, "ein": k[1]} for k, v in panel.items() if k[0] == fy and k[1] not in exclude) + tuple(add)
    s = lambda m, f=lambda r: True: sum((r.get(m) or 0) for r in rows if f(r))  # noqa: E731
    acc, assets = s("daf_accounts_eoy"), s("daf_assets_eoy")
    p_acc, p_assets = s("daf_accounts_eoy", is_processor), s("daf_assets_eoy", is_processor)
    shares = sorted(((r.get("daf_assets_eoy") or 0) / assets for r in rows if assets), reverse=True)
    return {"sponsors": sum(1 for r in rows if (r.get("daf_assets_eoy") or 0) > 0 or (r.get("daf_accounts_eoy") or 0) > 0),
            "accounts": acc, "processor_accounts": p_acc, "non_processor_accounts": acc - p_acc,
            "processor_share_accounts": div(p_acc, acc), "assets": assets, "processor_share_assets": div(p_assets, assets),
            "contributions": s("daf_contributions"), "grants": s("daf_grants"),
            "avg_assets_per_account": div(assets, acc), "avg_assets_per_non_processor_account": div(assets - p_assets, acc - p_acc),
            "cr1_assets": sum(shares[:1]), "cr5_assets": sum(shares[:5]), "cr10_assets": sum(shares[:10]),
            "hhi_assets": sum((x * 100) ** 2 for x in shares),
            "sdg_asset_rank": next((i + 1 for i, r in enumerate(sorted(rows, key=lambda r: -(r.get("daf_assets_eoy") or 0)))
                                    if r["ein"] == SDG_EIN), None)}


def sensitivity_rows(pub: Mapping, cor: Mapping, sdg: Sequence[Mapping]) -> tuple[dict, ...]:
    fys = (2019, 2020, 2021, 2022, 2023, 2024)
    paypal_imputed = frozenset(k[0] for k, v in pub.items() if k[1] == PAYPAL_EIN and v.get("src_daf_accounts_eoy") == "Imputed")
    sdg_by_fy = {int(r["fiscal_year"]): {"name": r["name"], "type": "National", "subtype": "Standard (not in DAFRC)",
                                          "ein": SDG_EIN, "daf_assets_eoy": num(r["sched_d_daf_eoy_value"]),
                                          "daf_accounts_eoy": num(r["sched_d_daf_count"]),
                                          "daf_contributions": num(r["sched_d_daf_contributions"]),
                                          "daf_grants": num(r["sched_d_daf_grants"])} for r in sdg}
    variants = (
        ("published", pub, lambda fy: frozenset(), lambda fy: ()),
        ("published_excl_givinga", pub, lambda fy: frozenset({GIVINGA_EIN}), lambda fy: ()),
        ("published_excl_givinga_and_imputed_paypal", pub,
         lambda fy: frozenset({GIVINGA_EIN} | ({PAYPAL_EIN} if fy in paypal_imputed else set())), lambda fy: ()),
        ("corrected", cor, lambda fy: frozenset(), lambda fy: ()),
        ("corrected_excl_givinga", cor, lambda fy: frozenset({GIVINGA_EIN}), lambda fy: ()),
        ("published_plus_sdg", pub, lambda fy: frozenset(), lambda fy: (sdg_by_fy[fy],) if fy in sdg_by_fy else ()),
        ("corrected_plus_sdg", cor, lambda fy: frozenset(), lambda fy: (sdg_by_fy[fy],) if fy in sdg_by_fy else ()),
    )
    stats = {(name, fy): market_stats(p, fy, ex(fy), add(fy)) for name, p, ex, add in variants for fy in fys}

    def growth(name, fy, m):
        prev = stats.get((name, fy - 1))
        return div(stats[(name, fy)][m] - prev[m], prev[m]) if prev and prev[m] else None

    giv = {fy: pub.get((fy, GIVINGA_EIN), {}) for fy in fys}
    rows = tuple({"variant": name, "fiscal_year": fy, **stats[(name, fy)],
                  "assets_growth_yoy": growth(name, fy, "assets"), "accounts_growth_yoy": growth(name, fy, "accounts"),
                  "payout_grants_over_prior_assets": div(stats[(name, fy)]["grants"], stats.get((name, fy - 1), {}).get("assets")),
                  "givinga_accounts_published": giv[fy].get("daf_accounts_eoy"),
                  "givinga_assets_published": giv[fy].get("daf_assets_eoy"),
                  "givinga_accounts_source": giv[fy].get("src_daf_accounts_eoy"),
                  "sdg_assets_added": (sdg_by_fy.get(fy) or {}).get("daf_assets_eoy") if "sdg" in name else None,
                  "paypal_accounts_imputed_this_fy": int(fy in paypal_imputed),
                  "sources": f"{DAFRC_URL}; data/mission-2026-11-14/dafrc-corrections-itemized.csv; "
                             f"data/mission-2026-11-14/non-dafrc-daf-filers-990.csv (SDG {SDG_EIN})"}
                 for name, _, _, _ in variants for fy in fys)
    return rows


SENS_FIELDS = ("variant", "fiscal_year", "sponsors", "accounts", "processor_accounts", "non_processor_accounts",
               "processor_share_accounts", "assets", "processor_share_assets", "contributions", "grants",
               "avg_assets_per_account", "avg_assets_per_non_processor_account", "assets_growth_yoy",
               "accounts_growth_yoy", "payout_grants_over_prior_assets", "cr1_assets", "cr5_assets", "cr10_assets",
               "hhi_assets", "givinga_accounts_published", "givinga_assets_published", "givinga_accounts_source",
               "sdg_assets_added", "sdg_asset_rank", "paypal_accounts_imputed_this_fy", "sources")


# ----------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--task", default="all", choices=("all", "extract", "cost", "givinga", "sdg"))
    a = ap.parse_args(argv)

    dafrc = m990.load_dafrc()
    if a.task in ("all", "extract", "cost"):
        harvest = tuple(h for h in read_csv(HARVEST_CSV) if h["xml_status"] == "ok")
        harvest = tuple({**h, "ein": ein9(h["ein"])} for h in harvest)
        ex = fetch_all(tuple(h["return_object_id"] for h in harvest), a.cache_dir, a.fetch, a.workers)
        bad = sum(1 for v in ex.values() if v.get("xml_status") != "ok")
        print(f"extracts: {len(ex)} ({bad} not ok)", file=sys.stderr)
        if a.task != "extract":
            dafrc_by = {(r["fy"], r["ein"]): r for r in dafrc}
            cost = tuple(cost_row(h, ex[h["return_object_id"]], dafrc_by.get((int(h["fiscal_year"]), h["ein"]), {}))
                         for h in harvest if ex[h["return_object_id"]].get("xml_status") == "ok")
            cost = tuple(sorted(cost, key=lambda r: (r["fiscal_year"], r["ein"])))
            write_csv(OUT_ROWS, cost, COST_FIELDS)
            summ = summarise(cost, read_csv(METRICS_CSV))
            write_csv(OUT_SUMMARY, summ, SUMMARY_FIELDS)
            print(f"wrote {OUT_ROWS} ({len(cost)}) and {OUT_SUMMARY} ({len(summ)})", file=sys.stderr)
    if a.task in ("all", "givinga", "sdg"):
        pub = panel_published(dafrc)
        cor = panel_corrected(pub, read_csv(ITEMIZED_CSV), dafrc)
        sdg = tuple(r for r in read_csv(NON_DAFRC_CSV) if ein9(r["ein"]) == SDG_EIN and r["status"] == "reports_daf_value")
        rows = sensitivity_rows(pub, cor, sdg)
        # validation: rebuilt corrected panel must reproduce dafrc-corrected-market-totals.csv
        tot = {(int(t["fiscal_year"]), t["metric"]): num(t["corrected_value"]) for t in read_csv(CORRECTED_TOTALS_CSV)}
        for r in rows:
            if r["variant"] == "corrected" and (r["fiscal_year"], "daf_assets_eoy") in tot:
                for m, col in (("daf_assets_eoy", "assets"), ("daf_accounts_eoy", "accounts")):
                    want = tot[(r["fiscal_year"], m)]
                    if abs(r[col] - want) > max(1, 1e-6 * want):
                        print(f"VALIDATION MISMATCH FY{r['fiscal_year']} {m}: {r[col]} vs {want}", file=sys.stderr)
        write_csv(OUT_SENS, rows, SENS_FIELDS)
        print(f"wrote {OUT_SENS} ({len(rows)})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
