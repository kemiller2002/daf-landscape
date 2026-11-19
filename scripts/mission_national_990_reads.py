#!/usr/bin/env python3
"""National-sponsor Form 990 reads (task g0702-b4531): queue items P-G07-02 and P-B45N31-02.

P-G07-02  Wirehouse / adviser-managed DAF assets at Fidelity Charitable, DAFgiving360 (Schwab Charitable),
          Vanguard Charitable and National Philanthropic Trust (NPT), FY2021-FY2025 Form 990s.
          Per return: Part VII Section B (five highest-paid independent contractors and the >$100k count),
          Part IX line 11a-g (fees for services) and line 24 rows naming investment/adviser costs, Part X
          investments (lines 11-13), Schedule D Part I (DAF count and value), Schedule J (top compensation),
          Schedule L Part V and Schedule O narratives that mention advisers, brokers or investment managers.
          Contractors are bucketed by name/service text (affiliated administrator, investment manager / adviser,
          wirehouse or broker-dealer brand, other). The rows are joined with a fixed table of the sponsors'
          own published adviser-programme statements (each with its URL and retrieval date) and an
          adviser-managed share is estimated only where a published figure or a filed number supports it.

P-B45N31-02 NPT's foreign grants, FY2021-FY2025 (focus FY2023-FY2024, the $742.8m in
          direction-foreign-grants-schedule-f.md). Schedule F Part I (activities by region), Part II (grants to
          foreign organisations: region, purpose, cash; recipient lines; line 2 counts of 501(c)(3)-equivalent
          and other recipients), Part III, Part V. Schedule R: related organisations (Parts I-IV), Part V line 1
          indicators (1b = gift/grant/capital contribution TO a related organisation) and line 2 transactions.
          The affiliate split uses Schedule R plus the affiliates' own published UK accounts (fixed table, URLs).
          NPT's FY2024 Part II columns are shifted (purpose in the manner field); this is repaired as in
          scripts/mission_foreign_grants.py.

Return choice: IRS TEOS e-file index (index_2021..index_2026.csv), RETURN_TYPE 990, the four EINs, tax periods
ending 2021-01..2025-12; the newest OBJECT_ID per (EIN, tax period). FY = calendar year in which the tax period
ends (repo convention). XML: a local copy when one is found under --local-dir (searched recursively for
{OBJECT_ID}.xml or {OBJECT_ID}_public.xml), otherwise the GivingTuesday mirror of IRS TEOS
(https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml; robots.txt 404 = no
rules). Extracts are cached as JSON in --cache.

Stdlib only; functional style (pure transforms, I/O at the edges).

Usage:
  python3 scripts/mission_national_990_reads.py . --irs-dir IRS --cache DIR [--local-dir D ...] [--fetch]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Iterable, Mapping, Sequence

XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
UA = {"User-Agent": "research-script/1.0 (stdlib urllib)"}
EXTRACT_V = 3
OUT_A = "data/mission-2026-11-14/adviser-managed-daf-assets-2026-11-19.csv"
OUT_B = "data/mission-2026-11-14/npt-foreign-grants-breakdown-2026-11-19.csv"

SPONSORS = {
    "110303001": "Fidelity Charitable",
    "311640316": "DAFgiving360 (Schwab Charitable)",
    "232888152": "Vanguard Charitable",
    "237825575": "National Philanthropic Trust",
}
NPT = "237825575"
KEEP = {"ReturnHeader", "IRS990", "IRS990ScheduleD", "IRS990ScheduleF", "IRS990ScheduleJ", "IRS990ScheduleL",
        "IRS990ScheduleO", "IRS990ScheduleR"}

# ----------------------------------------------------------------------------- published statements (P-G07-02)
# Each figure is quoted from the sponsor's own document, fetched 2026-11-19 with a generic user agent after a
# robots.txt check (see the research doc's robots log). DAFgiving360's host returned 403 to robots.txt itself,
# so nothing was fetched there; its rows cite pages already quoted in the repo and are marked accordingly.
FC_AUD25 = "https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf"
FC_AUD24 = "https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf"
FC_AUD23 = "https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2023-2022.pdf"
FC_CIAP = "https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf"
FC_IPG = "https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf"
VC_POL = "https://www.vanguardcharitable.org/company-policies/policies-and-guidelines"
NPT_GUIDE = "https://www.nptrust.org/a-guide-to-your-donor-advised-fund-npt/"
NPT_FIN25 = "https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf"
NPT_AR25 = "https://www.nptrust.org/annual-reports/npt-annual-report/"
D360_FEES = "https://www.dafgiving360.org/features/fees-and-minimums"
D360_POL = "https://www.dafgiving360.org/content/dam/dafgiving360/pdf/DAFgiving360-2024-Program-Policies.pdf"
IN_2026 = ("https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/"
           "264994")

PUBLIC = (
    # sponsor, fy, item, value, unit, quote, url, status
    ("110303001", 2022, "ciap_assets", 18112561857, "usd", "Total Advisor-managed Investments at Fair Value (2022)", FC_AUD23, "fetched"),
    ("110303001", 2022, "total_investments", 44823238524, "usd", "Total Investments at Fair Value (2022)", FC_AUD23, "fetched"),
    ("110303001", 2023, "ciap_assets", 22433249315, "usd", "Total Advisor-managed Investments at Fair Value (2023)", FC_AUD24, "fetched"),
    ("110303001", 2023, "total_investments", 52650176429, "usd", "Total Investments at Fair Value (2023)", FC_AUD24, "fetched"),
    ("110303001", 2024, "ciap_assets", 27546211645, "usd", "Total Advisor-managed Investments at Fair Value (2024)", FC_AUD25, "fetched"),
    ("110303001", 2024, "total_investments", 61514405850, "usd", "Total Investments at Fair Value (2024)", FC_AUD25, "fetched"),
    ("110303001", 2025, "ciap_assets", 37139208368, "usd", "Total Advisor-managed Investments at Fair Value (2025)", FC_AUD25, "fetched"),
    ("110303001", 2025, "total_investments", 79232938398, "usd", "Total Investments at Fair Value (2025)", FC_AUD25, "fetched"),
    ("110303001", 2022, "audit_investment_management_fees", 56692887, "usd", "Investment management fees (2022)", FC_AUD23, "fetched"),
    ("110303001", 2023, "audit_investment_management_fees", 53687639, "usd", "Investment management fees (2023)", FC_AUD24, "fetched"),
    ("110303001", 2024, "audit_investment_management_fees", 67308635, "usd", "Investment management fees (2024)", FC_AUD25, "fetched"),
    ("110303001", 2025, "audit_investment_management_fees", 84317489, "usd", "Investment management fees (2025)", FC_AUD25, "fetched"),
    ("110303001", None, "program_name", "Charitable Investment Advisor Program (CIAP)", "text",
     "Our Charitable Investment Advisor Program allows independent investment advisors to serve their clients beyond our investment pools by actively managing the contributions made to their clients' Fidelity Charitable Giving Account", FC_CIAP, "fetched"),
    ("110303001", None, "minimum_balance", 100000, "usd", "a Giving Account that meets the program's $100,000 minimum balance requirement", FC_CIAP, "fetched"),
    ("110303001", None, "adviser_fee_basis", "mutually agreeable and reasonable annual Investment Advisory Fee; no numeric cap", "text",
     "in return for a mutually agreeable and reasonable annual Investment Advisory Fee ... Agreed-upon Investment Advisory Fees cannot be assessed on Giving Account assets in the Fidelity Charitable investment pools", FC_IPG, "fetched"),
    ("110303001", None, "sponsor_admin_fee_on_ciap", "60/30/20/15 bps tiers below $5m (70/30/20/15 bps at other custodians); flat 19-11.5 bps from $5m", "text",
     "First $500K 60 basis points (bps) Next $500K 30 bps Next $1.5M 20 bps Next $2.5M 15 bps", FC_CIAP, "fetched"),
    ("232888152", None, "program_name", "none (no adviser-managed programme)", "text",
     "Vanguard Charitable trustees have sole responsibility and authority to invest Vanguard Charitable's assets; they select, approve, and periodically review all investment options", VC_POL, "fetched"),
    ("232888152", None, "adviser_fee_basis", "none charged by the sponsor; fund expense ratios only", "text",
     "Vanguard Charitable does not itself charge investment fees; expense ratios are assessed by the underlying funds", VC_POL, "fetched"),
    ("232888152", None, "adviser_role", "financial advisor may be an 'interested party' with some account access", "text",
     "This role is ideal for a financial advisor, accountant, or family member to whom the account advisors wish to provide some account access", VC_POL, "fetched"),
    ("237825575", None, "program_name", "Segregated Account - Financial Advisor Managed", "text",
     "DAF accounts over $500,000 may recommend a financial advisor to propose a custom investment portfolio. A different fee schedule may apply.", NPT_GUIDE, "fetched"),
    ("237825575", None, "minimum_balance", 500000, "usd",
     "The account minimum for segregated accounts is $500,000 for discretionary account types ... For non-discretionary accounts ... the minimum is $2 million.", NPT_GUIDE, "fetched"),
    ("237825575", None, "adviser_fee_basis", "not published ('A different fee schedule may apply')", "text",
     "Segregated Account Fees A different fee schedule may apply to segregated accounts.", NPT_GUIDE, "fetched"),
    ("237825575", 2025, "asset_management_fees_usd_thousands", 116260, "usd_thousands", "Asset management fees 116,260 (FY2024 94,289), in thousands", NPT_FIN25, "fetched"),
    ("237825575", 2025, "investments_fair_value_usd_thousands", 47837978, "usd_thousands", "Investments, fair value 47,837,978 (FY2024 36,915,275), in thousands", NPT_FIN25, "fetched"),
    ("237825575", 2025, "assets_under_management", 56400000000, "usd", "NPT held $56.4 billion in assets under management", NPT_AR25, "fetched"),
    ("311640316", None, "program_name", "Professionally managed / investment advisor option", "text",
     "repo quote (batch 32 / Pave doc): advisor must be approved and work with Schwab Advisor Services; $100k minimum; 1% max adviser fee", D360_FEES, "not_fetched_robots_403"),
    ("311640316", None, "adviser_fee_basis", "advisory fee capped at 1.00% (repo quote)", "text",
     "repo quote: 1% max adviser fee (DAFgiving360 Program Policies, Dec 2024)", D360_POL, "not_fetched_robots_403"),
    ("311640316", 2025, "assets_associated_with_advisor_share", 0.77, "share",
     "77% of DAF assets were associated with an advisor relationship (CY2025; secondary, quoting DAFgiving360)", IN_2026, "repo_secondary"),
)

# ----------------------------------------------------------------------------- NPT affiliates' own accounts (P-B45N31-02)
UK_TA25 = "https://www.nptuk.org/transatlantic-annual-report-and-accounts-2025/"
UK_UK25 = "https://www.nptuk.org/npt-uk-annual-report-and-accounts-2025/"
UK_GR23 = "https://www.nptuk.org/annual-reports/2023-grantmaking-report/"
UK_TA_PAGE = "https://www.nptuk.org/what-is-npt-transatlantic/"
AFFILIATE_FACTS = (
    # entity, npt_fy, item, value, unit, quote, url
    ("NPT Transatlantic", None, "status", "disregarded entity of NPT (US); English charity 1153376", "text",
     "recognised by the Internal Revenue Service (IRS) as US public charity because it is considered a disregarded entity of National Philanthropic Trust (EIN 23-7825575)", UK_TA_PAGE),
    ("NPT Transatlantic", 2023, "grants_total_gbp", 68000000, "gbp", "NPT Transatlantic distributed a further £68 million in grants in FY23", UK_GR23),
    ("NPT UK", 2023, "grants_total_gbp", 16000000, "gbp", "Grantmaking from NPT UK surpassed £16 million in value during FY23", UK_GR23),
    ("NPT Transatlantic", 2024, "grants_total_gbp", 47490000, "gbp", "795 grants to 561 unique charities, totalling £47.5M (2023/24); table total 47,490 £'000", UK_TA25),
    ("NPT Transatlantic", 2025, "grants_total_gbp", 84264000, "gbp", "846 grants to 616 unique charities, totalling £84.3M; table total 84,264 £'000", UK_TA25),
    ("NPT Transatlantic", 2025, "grant_to_npt_uk_gbp", 30939000, "gbp", "National Philanthropic Trust UK Limited 30,939 (£'000), year ended 30 June 2025", UK_TA25),
    ("NPT Transatlantic", 2025, "grant_to_npt_us_gbp", 30000, "gbp", "NPT Transatlantic granted £30,000 (2023/24 - £30,000) to National Philanthropic Trust", UK_TA25),
    ("NPT Transatlantic", 2024, "grant_to_npt_us_gbp", 30000, "gbp", "NPT Transatlantic granted £30,000 (2023/24 - £30,000) to National Philanthropic Trust", UK_TA25),
    ("NPT Transatlantic", 2024, "grant_to_npt_uk_gbp_listed", 0, "gbp",
     "NPT UK is not among the FY2023/24 grantees listed as material (smallest listed £1,257k; 'Other grants less than £1M' £27,149k)", UK_TA25),
    ("NPT UK", 2025, "grants_total_gbp", 43000000, "gbp", "Donor-recommended grants totalled £43.0M this financial year", UK_UK25),
    ("NPT UK", 2025, "contributions_from_affiliates_gbp", 30900000, "gbp",
     "Contributions of £30.9M were received from NPT Transatlantic and £30.9M from National Philanthropic Trust", UK_UK25),
)


# ----------------------------------------------------------------------------- small pure helpers
def num(x) -> float:
    try:
        return float(str(x).replace(",", "")) if x not in (None, "") else 0.0
    except ValueError:
        return 0.0


def local(tag: str) -> str:
    return tag.split("}")[-1]


def kids(el, name: str) -> list:
    return [c for c in el if local(c.tag) == name]


def first(el, *path: str):
    return reduce(lambda n, t: None if n is None else next(iter(kids(n, t)), None), path, el)


def txt(el, *path: str) -> str:
    n = first(el, *path) if path else el
    return " ".join("".join(n.itertext()).split()) if n is not None else ""


def descend(el, name: str) -> list:
    return [n for n in el.iter() if local(n.tag) == name]


def name_of(el) -> str:
    """Business or person name inside a group, whatever wrapper the schema version uses."""
    hits = [txt(n) for n in el.iter() if local(n.tag) in ("BusinessNameLine1Txt", "BusinessNameLine1", "PersonNm")]
    return hits[0] if hits else ""


# ----------------------------------------------------------------------------- return location
def locate_returns(irs_dir: str) -> tuple[dict, ...]:
    def rows(y: int) -> Iterable[dict]:
        p = os.path.join(irs_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple(r for r in csv.DictReader(fh)
                         if r.get("EIN") in SPONSORS and r.get("RETURN_TYPE") == "990"
                         and "202101" <= (r.get("TAX_PERIOD") or "") <= "202512")
    hits = tuple(r for y in range(2021, 2027) for r in rows(y))
    best = reduce(lambda acc, r: {**acc, (r["EIN"], r["TAX_PERIOD"]): r}
                  if (r["EIN"], r["TAX_PERIOD"]) not in acc or r["OBJECT_ID"] > acc[(r["EIN"], r["TAX_PERIOD"])]["OBJECT_ID"]
                  else acc, hits, {})
    superseded = {k: tuple(sorted(x["OBJECT_ID"] for x in hits if (x["EIN"], x["TAX_PERIOD"]) == k and x["OBJECT_ID"] != v["OBJECT_ID"]))
                  for k, v in best.items()}
    return tuple(sorted(({"ein": k[0], "sponsor": SPONSORS[k[0]], "tax_period": k[1], "fy": int(k[1][:4]),
                          "object_id": v["OBJECT_ID"], "sub_date": v.get("SUB_DATE", ""),
                          "superseded": ";".join(superseded[k])} for k, v in best.items()),
                        key=lambda r: (r["ein"], r["tax_period"])))


def find_local(dirs: Sequence[str]) -> dict:
    names = re.compile(r"^(\d{18})(?:_public)?\.xml$")
    return reduce(lambda acc, p: acc if names.match(os.path.basename(p)).group(1) in acc
                  else {**acc, names.match(os.path.basename(p)).group(1): p},
                  (os.path.join(r, f) for d in dirs for r, _, fs in os.walk(d) for f in fs
                   if names.match(f) and os.path.getsize(os.path.join(r, f)) > 50000), {})


# ----------------------------------------------------------------------------- extraction (one pass per return)
def ex_header(el) -> dict:
    return {"filer_ein": txt(el, "Filer", "EIN"), "tax_period_begin": txt(el, "TaxPeriodBeginDt"),
            "tax_period_end": txt(el, "TaxPeriodEndDt"), "tax_year": txt(el, "TaxYr"),
            "filer_name": txt(el, "Filer", "BusinessName", "BusinessNameLine1Txt")}


LINE11 = (("11a_management", "FeesForServicesManagementGrp"), ("11b_legal", "FeesForServicesLegalGrp"),
          ("11c_accounting", "FeesForServicesAccountingGrp"), ("11d_lobbying", "FeesForServicesLobbyingGrp"),
          ("11e_prof_fundraising", "FeesForServicesProfFundraising"),
          ("11f_investment_management", "FeesForSrvcInvstMgmntFeesGrp"), ("11g_other", "FeesForServicesOtherGrp"))


def ex_990(el) -> dict:
    return {
        "line11": {k: num(txt(el, t, "TotalAmt")) for k, t in LINE11},
        "line24": [{"desc": txt(g, "Desc"), "amount": num(txt(g, "TotalAmt"))} for g in kids(el, "OtherExpensesGrp")],
        "contractors": [{"name": name_of(first(g, "ContractorName") or g), "services": txt(g, "ServicesDesc"),
                         "amount": num(txt(g, "CompensationAmt"))} for g in kids(el, "ContractorCompensationGrp")],
        "contractors_over_100k": num(txt(el, "CntrctRcvdGreaterThan100KCnt")),
        "total_assets_eoy": num(txt(el, "TotalAssetsEOYAmt")),
        "investments_eoy": sum(num(txt(el, t, "EOYAmt")) for t in
                               ("InvestmentsPubTradedSecGrp", "InvestmentsOtherSecuritiesGrp", "InvestmentsProgramRelatedGrp")),
        "grants_domestic_orgs": num(txt(el, "GrantsToDomesticOrgsGrp", "TotalAmt")),
        "grants_domestic_ind": num(txt(el, "GrantsToDomesticIndividualsGrp", "TotalAmt")),
        "grants_foreign": num(txt(el, "ForeignGrantsGrp", "TotalAmt")),
        "total_functional_expenses": num(txt(el, "TotalFunctionalExpensesGrp", "TotalAmt")),
        "sched_j_required": txt(el, "ScheduleJRequiredInd"),
    }


def ex_d(el) -> dict:
    return {k: num(txt(el, t)) for k, t in (("daf_count", "DonorAdvisedFundsHeldCnt"),
                                            ("daf_value_eoy", "DonorAdvisedFundsVlEOYAmt"),
                                            ("daf_contributions", "DonorAdvisedFundsContriAmt"),
                                            ("daf_grants", "DonorAdvisedFundsGrantsAmt"))}


def ex_j(el) -> dict:
    people = [{"name": name_of(g), "title": txt(g, "TitleTxt"),
               "total_filing_org": num(txt(g, "TotalCompensationFilingOrgAmt")),
               "total_related_orgs": num(txt(g, "TotalCompensationRltdOrgsAmt"))}
              for g in kids(el, "RltdOrgOfficerTrstKeyEmplGrp")]
    return {"sched_j": sorted(people, key=lambda p: -(p["total_filing_org"] + p["total_related_orgs"]))}


ADV_RX = re.compile(r"ADVIS|INVESTMENT MANAG|BROKER|WEALTH|CIAP|SEGREGATED|ADVISOR PROGRAM|MANAGED ACCOUNT", re.I)
# Row-stage filter: drops 'donor advised' / 'donor advisor' hits that the broad extract-stage filter keeps.
ADV_STRICT = re.compile(r"(?<!DONOR )(?<!DONOR-)ADVIS(?:OR|ER|ORY)|INVESTMENT MANAG|BROKER|WEALTH MANAG|CIAP|"
                        r"SEGREGATED|MANAGED ACCOUNT", re.I)


def ex_text(el, sched: str) -> dict:
    entries = [{"ref": txt(g, "FormAndLineReferenceDesc") or txt(g, "FormAndLineReferenceDesc"),
                "text": txt(g, "ExplanationTxt")} for g in descend(el, "SupplementalInformationDetail")]
    extra = [{"ref": local(n.tag), "text": txt(n)} for n in el.iter()
             if local(n.tag) in ("ExcessBenefitTransactionGrp", "BusTrInvolveInterestedPrsnGrp")]
    return {f"text_{sched}": [e for e in entries + extra if ADV_RX.search(e["text"] or "")]}


def ex_f(el) -> dict:
    p1 = [{"region": txt(g, "RegionTxt"), "offices": num(txt(g, "OfficesCnt")), "employees": num(txt(g, "EmployeeCnt")),
           "activity": txt(g, "TypeOfActivitiesConductedTxt"), "amount": num(txt(g, "RegionTotalExpendituresAmt"))}
          for g in kids(el, "AccountActivitiesOutsideUSGrp")]
    p2 = [{"region": txt(g, "RegionTxt"), "purpose": txt(g, "PurposeOfGrantTxt"), "cash": num(txt(g, "CashGrantAmt")),
           "manner": txt(g, "MannerOfCashDisbursementTxt"), "noncash": num(txt(g, "NonCashAssistanceAmt")),
           "valuation": txt(g, "ValuationMethodUsedDesc"), "ein": txt(g, "EIN"), "irc": txt(g, "IRCSectionDesc")}
          for g in kids(el, "GrantsToOrgOutsideUSGrp")]
    p3 = [{"region": txt(g, "RegionTxt"), "cash": num(txt(g, "CashGrantAmt")), "recipients": num(txt(g, "RecipientCnt"))}
          for g in kids(el, "ForeignIndividualsGrantsGrp")]
    return {"f_part1": p1, "f_part2": p2, "f_part3": p3,
            "f_cnt_501c3": num(txt(el, "Total501c3OrgCnt")), "f_cnt_other": num(txt(el, "TotalOtherOrgCnt")),
            "f_part5": [txt(g, "ExplanationTxt") for g in descend(el, "SupplementalInformationDetail")]}


def ex_r(el) -> dict:
    orgs = [{"group": local(g.tag), "name": name_of(g),
             "country": next((txt(n) for n in g.iter() if local(n.tag) in ("CountryCd", "LegalDomicileForeignCountryCd")), ""),
             "ein": txt(g, "EIN"), "income": num(txt(g, "TotalIncomeAmt")), "assets_eoy": num(txt(g, "EndOfYearAssetsAmt")),
             "activity": txt(g, "PrimaryActivitiesTxt")}
            for g in el if local(g.tag).startswith("Id")]
    inds = {local(n.tag): txt(n) for n in el if local(n.tag).endswith("Ind")}
    trans = [{"name": name_of(g), "type": txt(g, "TransactionTypeTxt"), "amount": num(txt(g, "InvolvedAmt"))}
             for g in kids(el, "TransactionsRelatedOrgGrp")]
    return {"r_orgs": orgs, "r_indicators": inds, "r_transactions": trans}


HANDLERS = {"ReturnHeader": ex_header, "IRS990": ex_990, "IRS990ScheduleD": ex_d, "IRS990ScheduleF": ex_f,
            "IRS990ScheduleJ": ex_j, "IRS990ScheduleL": lambda e: ex_text(e, "L"),
            "IRS990ScheduleO": lambda e: ex_text(e, "O"), "IRS990ScheduleR": ex_r}


def parse_stream(fh) -> dict:
    """Stream the XML; keep only the needed top-level documents, clear everything else as it closes."""
    def step(state, ev):
        event, el = ev
        depth, keep_at, parts = state
        tag = local(el.tag)
        if event == "start":
            d = depth + 1
            return d, (d if keep_at is None and tag in KEEP and d in (2, 3) else keep_at), parts
        if keep_at == depth:
            out = HANDLERS[tag](el)
            el.clear()
            return depth - 1, None, parts + (out,)
        if keep_at is None and depth >= 3:
            el.clear()
        return depth - 1, keep_at, parts
    _, _, parts = reduce(step, ET.iterparse(fh, events=("start", "end")), (0, None, ()))
    return reduce(lambda a, b: {**a, **b}, parts, {"_v": EXTRACT_V})


def load_extract(oid: str, cache: str, local_paths: Mapping, fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == EXTRACT_V:
            return c

    def save(obj: dict) -> dict:
        os.makedirs(cache, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh)
        return obj

    lp = local_paths.get(oid)
    if lp:
        with open(lp, "rb") as fh:
            return save({**parse_stream(fh), "via": "local", "xml_url": XML_URL.format(oid=oid)})
    if not fetch:
        return {"status": "not_fetched"}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers=UA)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=900) as resp:
                return save({**parse_stream(resp), "via": "mirror", "xml_url": XML_URL.format(oid=oid)})
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"status": f"http_{e.code}"}
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError):
            time.sleep(5 * (attempt + 1))
    return {"status": "error"}


# ----------------------------------------------------------------------------- classification (P-G07-02)
AFFILIATE = re.compile(r"\bFMR\b|FIDELITY|SCHWAB|VANGUARD|NATIONAL PHILANTHROPIC|STRATEGIC ADVISERS", re.I)
WIREHOUSE = re.compile(r"MORGAN STANLEY|MORGAN STA\b|GRAYSTONE|MERRILL|BANK OF AMERICA|\bUBS\b|WELLS FARGO", re.I)
BROKER = re.compile(r"EDWARD JONES|EDWARD D\.? JONES|RAYMOND JAMES|\bLPL\b|AMERIPRISE|J\.?P\.? ?MORGAN|GOLDMAN|"
                    r"\bRBC\b|STIFEL|BAIRD|JANNEY|OPPENHEIMER|NORTHERN TRUST|\bBNY\b|CITI|ROCKEFELLER|BERNSTEIN|"
                    r"BESSEMER|PERSHING|INTERACTIVE BROKERS", re.I)
INVEST = re.compile(r"INVEST|ADVIS|ASSET MAN|WEALTH|PORTFOLIO|CAPITAL MAN|FUND MAN|CUSTOD", re.I)


def classify(c: Mapping) -> str:
    s = f"{c['name']} {c['services']}"
    if AFFILIATE.search(c["name"]):
        return "affiliated_administrator"
    if WIREHOUSE.search(c["name"]):
        return "wirehouse_brand"
    if BROKER.search(c["name"]):
        return "other_broker_dealer_or_bank_brand"
    if INVEST.search(s):
        return "investment_manager_or_adviser"
    return "other"


# ----------------------------------------------------------------------------- P-G07-02 rows
def rows_a(ret: Mapping, ex: Mapping) -> list:
    base = {"sponsor": ret["sponsor"], "ein": ret["ein"], "fy": ret["fy"], "tax_period": ret["tax_period"],
            "object_id": ret["object_id"], "source_url": ex.get("xml_url", ""), "evidence": "F"}
    l11 = ex.get("line11", {})
    contr = [{**c, "class": classify(c)} for c in ex.get("contractors", [])]
    adv_contr = [c for c in contr if c["class"] in ("investment_manager_or_adviser", "wirehouse_brand",
                                                    "other_broker_dealer_or_bank_brand")]
    out = (
        [{**base, "row_type": "part9_line11", "item": k, "value": v, "unit": "usd", "form_ref": "990 Part IX line " + k[:3]}
         for k, v in l11.items()]
        + [{**base, "row_type": "part9_line24", "item": r["desc"], "value": r["amount"], "unit": "usd", "form_ref": "990 Part IX line 24"}
           for r in ex.get("line24", []) if ADV_RX.search(r["desc"] or "") or re.search(r"INV|ADV", r["desc"] or "", re.I)]
        + [{**base, "row_type": "part7b_contractor", "item": c["name"], "detail": c["services"], "class": c["class"],
            "value": c["amount"], "unit": "usd", "form_ref": "990 Part VII Section B line 1"} for c in contr]
        + [{**base, "row_type": "part7b_count_over_100k", "item": "contractors receiving > $100,000",
            "value": ex.get("contractors_over_100k", 0), "unit": "count", "form_ref": "990 Part VII Section B line 2"},
           {**base, "row_type": "part7b_adviser_subtotal", "item": "top-5 contractors classed as adviser / BD / wirehouse",
            "value": sum(c["amount"] for c in adv_contr), "unit": "usd", "evidence": "C",
            "detail": "; ".join(f"{c['name']} ({c['class']})" for c in adv_contr), "form_ref": "990 Part VII-B (classified here)"},
           {**base, "row_type": "part10_investments", "item": "investments lines 11-13 EOY", "value": ex.get("investments_eoy", 0),
            "unit": "usd", "form_ref": "990 Part X lines 11-13"},
           {**base, "row_type": "total_assets", "item": "total assets EOY", "value": ex.get("total_assets_eoy", 0),
            "unit": "usd", "form_ref": "990 Part X line 16"},
           {**base, "row_type": "sched_d_daf", "item": "DAF value EOY", "value": ex.get("daf_value_eoy", 0), "unit": "usd",
            "form_ref": "Schedule D Part I line 4"},
           {**base, "row_type": "sched_d_daf", "item": "DAF count", "value": ex.get("daf_count", 0), "unit": "count",
            "form_ref": "Schedule D Part I line 1"},
           {**base, "row_type": "sched_j_summary", "item": "Schedule J persons",
            "value": len(ex.get("sched_j", [])), "unit": "count", "form_ref": "Schedule J Part II",
            "detail": "; ".join(f"{p['name']} ({p['title']}) {int(p['total_filing_org'] + p['total_related_orgs'])}"
                                for p in ex.get("sched_j", [])[:3]) or "no Schedule J filed"}]
        + [{**base, "row_type": f"sched_{s.lower()}_text", "item": e["ref"][:120], "detail": e["text"][:900],
            "value": "", "unit": "text", "form_ref": f"Schedule {s}"}
           for s in ("O", "L") for e in ex.get(f"text_{s}", []) if ADV_STRICT.search(e["text"] or "")]
    )
    return out


def pub_rows() -> list:
    return [{"sponsor": SPONSORS[e], "ein": e, "fy": fy or "", "row_type": "public_statement", "item": item,
             "value": v, "unit": unit, "detail": q, "source_url": url, "evidence": "P" if st == "fetched" else "S",
             "form_ref": st} for e, fy, item, v, unit, q, url, st in PUBLIC]


def pub(ein: str, fy, item: str):
    return next((v for e, f, i, v, *_ in PUBLIC if e == ein and f == fy and i == item), None)


def estimates(exts: Mapping) -> list:
    """Adviser-managed share per sponsor-year, only where a published or filed number supports it."""
    def fid(fy: int) -> list:
        a, t = pub("110303001", fy, "ciap_assets"), pub("110303001", fy, "total_investments")
        prev = pub("110303001", fy - 1, "ciap_assets")
        fee = pub("110303001", fy, "audit_investment_management_fees")
        daf = exts.get(("110303001", fy), {}).get("daf_value_eoy", 0)
        rows = [{"item": "adviser_managed_share_of_investments", "value": round(a / t, 4), "unit": "share",
                 "detail": f"CIAP {a:.0f} / total investments {t:.0f} (audit Note 3)", "evidence": "P/C"}] if a and t else []
        rows += [{"item": "adviser_managed_share_of_daf_value", "value": round(a / daf, 4), "unit": "share",
                  "detail": f"CIAP {a:.0f} / Schedule D DAF value {daf:.0f}", "evidence": "P/F/C"}] if a and daf else []
        rows += [{"item": "investment_mgmt_fee_bps_of_avg_ciap", "value": round(fee / ((a + prev) / 2) * 1e4, 2), "unit": "bps",
                  "detail": f"audit investment management fees {fee:.0f} / mean CIAP {(a + prev) / 2:.0f}; reads as the "
                            "asset-weighted adviser fee if the line is CIAP adviser fees only [I]", "evidence": "C/I"}] if a and prev and fee else []
        return [{**r, "sponsor": SPONSORS["110303001"], "ein": "110303001", "fy": fy, "row_type": "estimate"} for r in rows]

    def fee_bounds(ein: str, fy: int, cap, scen_bps: float) -> list:
        """Bounds on adviser-managed assets from filed fee lines. With an adviser-fee cap c, assets >= fees / c.
        Hard floor: identified adviser / BD contractor payments (Part VII-B top five) / c. Conditional floor:
        all of line 11f / c (holds only if 11f is adviser fees). Scenario: 11f at Fidelity's audit-implied
        CIAP fee rate (scen_bps) [I]."""
        ex, prev = exts.get((ein, fy), {}), exts.get((ein, fy - 1), {})
        f = ex.get("line11", {}).get("11f_investment_management", 0)
        daf = ex.get("daf_value_eoy", 0)
        inv = (ex.get("investments_eoy", 0) + prev.get("investments_eoy", 0)) / 2 if prev.get("investments_eoy") else 0
        adv = sum(c["amount"] for c in ex.get("contractors", []) if classify(c) in
                  ("investment_manager_or_adviser", "wirehouse_brand", "other_broker_dealer_or_bank_brand"))
        b = {"sponsor": SPONSORS[ein], "ein": ein, "fy": fy, "row_type": "estimate"}
        rows = [{**b, "item": "line11f_bps_of_mean_investments", "value": round(f / inv * 1e4, 2), "unit": "bps",
                 "detail": f"line 11f {f:.0f} / mean Part X investments {inv:.0f}", "evidence": "F/C"}] if f and inv else []
        if cap and daf:
            rows += [{**b, "item": "adviser_managed_floor_identified_contractors", "value": round(adv / cap), "unit": "usd",
                      "detail": f"Part VII-B adviser/BD contractors {adv:.0f} / {cap:.2%} cap = {adv / cap / daf:.4f} of DAF value",
                      "evidence": "F/C"},
                     {**b, "item": "adviser_managed_floor_if_11f_all_adviser_fees", "value": round(f / cap), "unit": "usd",
                      "detail": f"line 11f {f:.0f} / {cap:.2%} cap = {f / cap / daf:.4f} of DAF value; holds only if 11f is "
                                "adviser fees [I]", "evidence": "F/C/I"},
                     {**b, "item": "adviser_managed_scenario_11f_at_fidelity_rate", "value": round(f / (scen_bps / 1e4)), "unit": "usd",
                      "detail": f"line 11f / {scen_bps:.2f} bps (Fidelity FY2023-25 mean audit-implied CIAP fee) = "
                                f"{f / (scen_bps / 1e4) / daf:.4f} of DAF value; scenario, not a measurement [I]", "evidence": "C/I"}]
        return rows

    fids = [r for fy in (2022, 2023, 2024, 2025) for r in fid(fy)]
    rates = [r["value"] for r in fids if r["item"] == "investment_mgmt_fee_bps_of_avg_ciap"]
    scen = sum(rates) / len(rates) if rates else 26.5
    d360 = [r for fy in range(2021, 2026) for r in fee_bounds("311640316", fy, 0.01, scen)]
    npt = [r for fy in range(2021, 2026) for r in fee_bounds(NPT, fy, None, scen)] + [
        {"sponsor": SPONSORS[NPT], "ein": NPT, "fy": 2025, "row_type": "estimate", "item": "adviser_managed_share_of_investments",
         "value": "", "unit": "share", "evidence": "I",
         "detail": "not estimable: line 11f mixes model-portfolio advisory fees ('each model portfolio charges an investment "
                   "advisory fee') with segregated-account adviser fees; no segregated-account total or adviser cap is published"}]
    fidr = [r for fy in range(2021, 2026) for r in fee_bounds("110303001", fy, None, scen)]
    van = [{"sponsor": SPONSORS["232888152"], "ein": "232888152", "fy": 2025, "row_type": "estimate",
            "item": "adviser_managed_share_of_investments", "value": 0, "unit": "share",
            "detail": "no adviser-managed option in the Policies & Guidelines (updated 2026-01-09); trustees invest; "
                      "line 11f is 0 in FY2021-25 and no adviser/BD contractor appears in Part VII-B", "evidence": "P/F"}]
    return fids + fidr + d360 + npt + van


# ----------------------------------------------------------------------------- P-B45N31-02 rows
REGION_RULES = ((r"EUROPE", "Europe"), (r"MIDDLE.?EAST|NORTH AFRICA", "Middle East and North Africa"),
                (r"SUB.?SAHARAN", "Sub-Saharan Africa"), (r"SOUTH ASIA", "South Asia"),
                (r"EAST ASIA|PACIFIC|OCEANIA", "East Asia and the Pacific"), (r"SOUTH AMERICA", "South America"),
                (r"CENTRAL AMERICA|CARIBBEAN", "Central America and the Caribbean"),
                (r"RUSSIA|NEWLY INDEPENDENT", "Russia and the Newly Independent States"),
                (r"NORTH AMERICA|CANADA|MEXICO", "North America (Canada, Mexico)"), (r"LATIN AMERICA", "Latin America (unspecified)"),
                (r"ANTARCTICA", "Antarctica"))
METHOD = re.compile(r"WIRE|CHECK|CHEQUE|ACH|EFT|ELECTRONIC|TRANSFER", re.I)


def region(t: str) -> str:
    return next((lab for rx, lab in REGION_RULES if re.search(rx, t or "", re.I)), "Other / unmapped: " + (t or ""))


def repair(line: Mapping) -> dict:
    """NPT FY2024: purpose in the manner field, manner in the valuation field (as in mission_foreign_grants.py)."""
    shifted = not line["purpose"] and line["manner"] and not METHOD.search(line["manner"]) and METHOD.search(line["valuation"] or "")
    return {**line, "purpose": line["manner"], "manner": line["valuation"], "repaired": True} if shifted else {**line, "repaired": False}


BANDS = ((0, 100000, "<$100k"), (100000, 1000000, "$100k-<$1m"), (1000000, 10000000, "$1m-<$10m"),
         (10000000, 30000000, "$10m-<$30m"), (30000000, float("inf"), ">=$30m"))


def band(x: float) -> str:
    return next(lab for lo, hi, lab in BANDS if lo <= x < hi)


def agg(lines: Sequence[Mapping], key) -> dict:
    return reduce(lambda acc, l: {**acc, key(l): (acc.get(key(l), (0, 0.0))[0] + 1, acc.get(key(l), (0, 0.0))[1] + l["cash"] + l["noncash"])},
                  lines, {})


def rows_b(ret: Mapping, ex: Mapping) -> list:
    base = {"fy": ret["fy"], "tax_period": ret["tax_period"], "object_id": ret["object_id"], "source_url": ex.get("xml_url", "")}
    lines = [repair(l) for l in ex.get("f_part2", [])]
    p2 = sum(l["cash"] + l["noncash"] for l in lines)
    l3 = ex.get("grants_foreign", 0)
    tot = [{"row_type": "total", "dimension": "form990_part9_line3_foreign_grants", "category": "all", "lines": "", "usd": l3, "evidence": "F"},
           {"row_type": "total", "dimension": "schedF_part2_total", "category": "all", "lines": len(lines), "usd": p2, "evidence": "F/C"},
           {"row_type": "total", "dimension": "schedF_part3_individuals", "category": "all",
            "lines": len(ex.get("f_part3", [])), "usd": sum(x["cash"] for x in ex.get("f_part3", [])), "evidence": "F"},
           {"row_type": "total", "dimension": "all_grants_lines1_3", "category": "all", "lines": "",
            "usd": ex.get("grants_domestic_orgs", 0) + ex.get("grants_domestic_ind", 0) + l3, "evidence": "F/C"},
           {"row_type": "total", "dimension": "columns_repaired_usd", "category": "Part II lines with shifted columns", "lines": sum(1 for l in lines if l["repaired"]),
            "usd": sum(l["cash"] for l in lines if l["repaired"]), "evidence": "C"}]
    rtype = [{"row_type": "recipient_type", "dimension": "schedF_part2_line2", "category": "501(c)(3) or equivalency-determined",
              "lines": ex.get("f_cnt_501c3", 0), "usd": "", "evidence": "F"},
             {"row_type": "recipient_type", "dimension": "schedF_part2_line3", "category": "other organisations (typically expenditure responsibility)",
              "lines": ex.get("f_cnt_other", 0), "usd": "", "evidence": "F"},
             {"row_type": "recipient_type", "dimension": "schedF_part2_recipient_ids", "category": "lines with an EIN or IRC section shown",
              "lines": sum(1 for l in lines if l["ein"] or l["irc"]), "usd": sum(l["cash"] for l in lines if l["ein"] or l["irc"]), "evidence": "F"}]
    by_reg = [{"row_type": "region", "dimension": "schedF_part2", "category": k, "lines": n, "usd": v, "share": v / p2 if p2 else "", "evidence": "F/C"}
              for k, (n, v) in sorted(agg(lines, lambda l: region(l["region"])).items(), key=lambda kv: -kv[1][1])]
    by_band = [{"row_type": "size_band", "dimension": "schedF_part2_line_size", "category": k, "lines": n, "usd": v, "share": v / p2 if p2 else "", "evidence": "C"}
               for k, (n, v) in agg(lines, lambda l: band(l["cash"] + l["noncash"])).items()]
    by_reg_band = [{"row_type": "region_x_size_band", "dimension": "schedF_part2", "category": f"{k[0]} | {k[1]}", "lines": n, "usd": v, "evidence": "C"}
                   for k, (n, v) in sorted(agg(lines, lambda l: (region(l["region"]), band(l["cash"] + l["noncash"]))).items())]
    by_purpose = [{"row_type": "purpose", "dimension": "schedF_part2_purpose_text", "category": k or "(blank)", "lines": n, "usd": v,
                   "share": v / p2 if p2 else "", "evidence": "F/C"}
                  for k, (n, v) in sorted(agg(lines, lambda l: (l["purpose"] or "").upper()).items(), key=lambda kv: -kv[1][1])[:12]]
    top = sorted(lines, key=lambda l: -(l["cash"] + l["noncash"]))[:10]
    top_rows = [{"row_type": "largest_line", "dimension": f"rank {i + 1}", "category": f"{region(l['region'])} | {l['purpose']}",
                 "lines": 1, "usd": l["cash"] + l["noncash"], "evidence": "F"} for i, l in enumerate(top)]
    part1 = [{"row_type": "part1_activity", "dimension": p["activity"][:60], "category": region(p["region"]),
              "lines": f"offices {int(p['offices'])}; employees {int(p['employees'])}", "usd": p["amount"], "evidence": "F"}
             for p in ex.get("f_part1", [])]
    inds = ex.get("r_indicators", {})
    rel = [{"row_type": "schedR_related_org", "dimension": o["group"], "category": o["name"],
            "lines": f"country {o['country'] or 'US'}; income {int(o['income'])}; assets {int(o['assets_eoy'])}",
            "usd": "", "evidence": "F"} for o in ex.get("r_orgs", [])
           if o["country"] or re.search(r"NPT|PHILANTHROPIC TRUST", o["name"], re.I)]
    rel += [{"row_type": "schedR_part5_line1", "dimension": k, "category": "Yes" if inds[k] in ("1", "true") else "No",
             "lines": "", "usd": "", "evidence": "F"} for k in ("GiftGrntOrCapContriToOthOrgInd", "GiftGrntCapContriFromOthOrgInd",
                                                                 "TransferToOtherOrgInd", "TransferFromOtherOrgInd") if k in inds]
    rel += [{"row_type": "schedR_part5_line2", "dimension": f"type {t['type']}", "category": t["name"], "lines": "", "usd": t["amount"], "evidence": "F"}
            for t in ex.get("r_transactions", []) if re.search(r"UK|TRANSATLANTIC", t["name"], re.I)]
    return [{**base, **r} for r in tot + rtype + by_reg + by_band + by_reg_band + by_purpose + top_rows + part1 + rel]


H10_URL = "https://www.federalreserve.gov/releases/h10/hist/dat00_uk.htm"
MONTHS = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}


def read_h10(path: str) -> tuple:
    """(yyyymmdd, usd_per_gbp) from the Fed H.10 historical page; ND rows dropped."""
    if not path or not os.path.exists(path):
        return ()
    with open(path, encoding="utf-8", errors="replace") as fh:
        t = fh.read()
    pairs = re.findall(r"<th[^>]*>\s*(\d{1,2})-([A-Z]{3})-(\d{2})\s*</th>\s*<td[^>]*>\s*([\d.]+)", t)
    return tuple((f"20{y}{MONTHS[m]:02d}{int(d):02d}", float(v)) for d, m, y, v in pairs)


def fy_rate(h10: Sequence, fy: int):
    """Mean noon buying rate (USD per GBP) over 1 July (fy-1) to 30 June fy, NPT's fiscal year."""
    xs = [v for d, v in h10 if f"{fy - 1}0701" <= d <= f"{fy}0630"]
    return sum(xs) / len(xs) if xs else None


# NPT Transatlantic material grants (accounts note, £'000). us_name = the grantee's name or a well-known
# identity marks it as a US-registered body (Inc., USA, a US university or a US 'friends' charity) [I];
# such grants would sit in NPT's Schedule I, not Schedule F.
TA_MATERIAL = (
    (2025, "National Philanthropic Trust UK Limited", 30939, False), (2025, "Economics Education and Research Consortium, Inc.", 6000, True),
    (2025, "Longview Philanthropy USA Inc", 3048, True), (2025, "British Schools and Universities Foundation", 3000, True),
    (2025, "Imperial College London", 2548, False), (2025, "World Economic Forum", 2424, False),
    (2025, "Impetus - The Private Equity Foundation", 2245, False), (2025, "Data for Society e.V.", 1158, False),
    (2025, "The Board of Trustees of the Leland Stanford Junior University", 1055, True),
    (2025, "Other grants less than £1M", 31847, False),
    (2024, "Arc Research Institute", 5543, False), (2024, "Economics Education and Research Consortium, Inc.", 3339, True),
    (2024, "World Economic Forum", 2755, False), (2024, "Impetus - The Private Equity Foundation", 2187, False),
    (2024, "Brown University", 2102, True), (2024, "London School of Economics and Political Science", 1722, False),
    (2024, "Institut Europeen de Cooperation et de Developpement", 1436, False), (2024, "Simon Fraser University", 1257, False),
    (2024, "Other grants less than £1M", 27149, False),
)


def affiliate_rows(exts: Mapping, h10: Sequence = ()) -> list:
    def usd(fy, unit, v):
        r = fy_rate(h10, fy) if fy and unit == "gbp" else None
        return round(v * r) if r else ""
    facts = [{"fy": fy or "", "row_type": "affiliate_account", "dimension": item, "category": ent, "lines": "",
              "usd": usd(fy, unit, v), "gbp": v if unit == "gbp" else "",
              "note": q + (f" [USD at FY mean H.10 rate {fy_rate(h10, fy):.4f}]" if usd(fy, unit, v) != "" else ""),
              "source_url": url, "evidence": "P/C" if usd(fy, unit, v) != "" else "P"}
             for ent, fy, item, v, unit, q, url in AFFILIATE_FACTS]
    mat = [{"fy": fy, "row_type": "affiliate_material_grant", "dimension": "NPT Transatlantic grantee", "category": n,
            "gbp": k * 1000, "usd": usd(fy, "gbp", k * 1000), "lines": "US-registered name [I]" if us else "",
            "note": "accounts note 'material' grants, £'000", "source_url": UK_TA25, "evidence": "P/C"} for fy, n, k, us in TA_MATERIAL]
    fx = [{"fy": fy, "row_type": "fx_rate", "dimension": "usd_per_gbp_fy_mean", "category": "Fed H.10 noon buying rate",
           "usd": round(fy_rate(h10, fy), 4), "source_url": H10_URL, "evidence": "P/C"} for fy in range(2021, 2026) if fy_rate(h10, fy)]

    def split(fy: int) -> list:
        ex = exts.get((NPT, fy), {})
        if not ex:
            return []
        l3 = ex.get("grants_foreign", 0)
        to_rel = "Yes" if ex.get("r_indicators", {}).get("GiftGrntOrCapContriToOthOrgInd") in ("1", "true") else "No"
        uk_in_r = any(re.search(r"PHILANTHROPIC TRUST UK", o["name"], re.I) for o in ex.get("r_orgs", []))
        reported_to_uk = sum(t["amount"] for t in ex.get("r_transactions", []) if re.search(r"UK", t["name"]))
        base = {"fy": fy, "tax_period": ex.get("tax_period_end", ""), "row_type": "affiliate_split", "source_url": ex.get("xml_url", "")}
        return [{**base, "dimension": "to_npt_uk_and_other_related_orgs_as_filed", "category": f"Schedule R Part V line 1b = {to_rel}; NPT UK listed in Part II: {uk_in_r}",
                 "usd": reported_to_uk, "evidence": "F"},
                {**base, "dimension": "to_other_foreign_organisations_as_filed", "category": "line 3 less filed related-org grants",
                 "usd": l3 - reported_to_uk, "share": (l3 - reported_to_uk) / l3 if l3 else "", "evidence": "F/C"}]
    def via_ta(fy: int) -> list:
        tot = next((v for e, f, i, v, *_ in AFFILIATE_FACTS if e == "NPT Transatlantic" and f == fy and i == "grants_total_gbp"), None)
        l3 = exts.get((NPT, fy), {}).get("grants_foreign", 0)
        if not tot or not l3 or not fy_rate(h10, fy):
            return []
        us_named = sum(k * 1000 for f, _, k, us in TA_MATERIAL if f == fy and us)
        ub = (tot - us_named) * fy_rate(h10, fy)
        return [{"fy": fy, "row_type": "affiliate_split", "dimension": "made_via_npt_transatlantic_upper_bound",
                 "category": "Transatlantic grants less US-named material grantees, USD at FY mean rate; inside line 3, not a grant to an affiliate",
                 "gbp": tot - us_named, "usd": round(ub), "share": ub / l3, "source_url": UK_TA25 if fy >= 2024 else UK_GR23, "evidence": "P/C/I"}]
    yearly = [r for fy in range(2021, 2026) for r in split(fy) + via_ta(fy)]
    l3p = sum(exts.get((NPT, fy), {}).get("grants_foreign", 0) for fy in (2023, 2024))
    ta_p = sum(r["usd"] for r in yearly if r["dimension"] == "made_via_npt_transatlantic_upper_bound" and r["fy"] in (2023, 2024))
    l3_25 = exts.get((NPT, 2025), {}).get("grants_foreign", 0)
    uk25 = usd(2025, "gbp", 30939000)
    pooled = [{"fy": "2023-2024", "row_type": "affiliate_split", "dimension": "line3_pooled", "category": "FY2023+FY2024 foreign grants",
               "usd": l3p, "evidence": "F/C"},
              {"fy": "2023-2024", "row_type": "affiliate_split", "dimension": "to_npt_uk_and_other_related_orgs_as_filed",
               "category": "Schedule R line 1b = No both years; NPT UK absent from Transatlantic's FY2024 material grantees", "usd": 0, "share": 0, "evidence": "F/P"},
              {"fy": "2023-2024", "row_type": "affiliate_split", "dimension": "made_via_npt_transatlantic_upper_bound",
               "category": "sum of the FY2023 and FY2024 bounds", "usd": ta_p, "share": ta_p / l3p if l3p else "", "evidence": "P/C/I"},
              {"fy": "2023-2024", "row_type": "affiliate_split", "dimension": "to_other_foreign_organisations",
               "category": "all of line 3 (no related-organisation recipient reported)", "usd": l3p, "share": 1 if l3p else "", "evidence": "F/C"}]
    fy25 = [{"fy": 2025, "row_type": "affiliate_split", "dimension": "to_npt_uk_per_affiliate_accounts",
             "category": "NPT Transatlantic grant to NPT UK £30.939m (accounts note); NPT 990 Schedule R line 1b still = No",
             "gbp": 30939000, "usd": uk25, "share": uk25 / l3_25 if uk25 != "" and l3_25 else "", "source_url": UK_TA25, "evidence": "P/C"}]
    return facts + mat + fx + yearly + pooled + fy25


def pooled(rows: Sequence[Mapping], row_type: str, fys=(2023, 2024)) -> list:
    """FY2023+FY2024 pooled view of per-year region / size-band rows."""
    sel = [r for r in rows if r["row_type"] == row_type and r["fy"] in fys]
    tot = sum(r["usd"] for r in sel)
    acc = reduce(lambda a, r: {**a, r["category"]: (a.get(r["category"], (0, 0))[0] + r["lines"], a.get(r["category"], (0, 0))[1] + r["usd"])}, sel, {})
    return [{"fy": "2023-2024", "row_type": row_type + "_pooled", "dimension": "schedF_part2", "category": k, "lines": n, "usd": v,
             "share": v / tot if tot else "", "evidence": "C"} for k, (n, v) in sorted(acc.items(), key=lambda kv: -kv[1][1])]


# ----------------------------------------------------------------------------- I/O
FIELDS_A = ("sponsor", "ein", "fy", "tax_period", "object_id", "row_type", "item", "class", "value", "unit", "detail",
            "form_ref", "evidence", "source_url")
FIELDS_B = ("fy", "tax_period", "object_id", "row_type", "dimension", "category", "lines", "usd", "gbp", "share", "note",
            "evidence", "source_url")


def fmt(x) -> str:
    if isinstance(x, float):
        return str(int(x)) if x.is_integer() else f"{x:.6g}"
    return "" if x is None else str(x)


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows({k: fmt(r.get(k)) for k in fields} for r in rows)


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", help="repo root ('.')")
    ap.add_argument("--irs-dir", required=True, help="holds index_2021.csv .. index_2026.csv")
    ap.add_argument("--cache", required=True, help="extract cache directory (JSON per return)")
    ap.add_argument("--local-dir", action="append", default=[], help="directories searched for local XML copies")
    ap.add_argument("--fetch", action="store_true", help="stream missing returns from the GivingTuesday mirror")
    ap.add_argument("--fx-h10", default="", help="saved copy of the Fed H.10 USD/GBP history page (optional)")
    a = ap.parse_args(argv)
    rets = locate_returns(a.irs_dir)
    local_paths = find_local(a.local_dir)
    exts_list = [(r, load_extract(r["object_id"], a.cache, local_paths, a.fetch)) for r in rets]
    bad = [(r["object_id"], e.get("status")) for r, e in exts_list if e.get("status")]
    mism = [(r["object_id"], e.get("filer_ein")) for r, e in exts_list if not e.get("status") and e.get("filer_ein") != r["ein"]]
    ok = [(r, e) for r, e in exts_list if not e.get("status")]
    exts = {(r["ein"], r["fy"]): e for r, e in ok if r["tax_period"].endswith("06") or (r["ein"], r["fy"]) not in {(x["ein"], x["fy"]) for x, _ in ok if x["tax_period"].endswith("06")}}
    rows = [x for r, e in ok for x in rows_a(r, e)] + pub_rows() + estimates(exts)
    write_csv(os.path.join(a.root, OUT_A), rows, FIELDS_A)
    npt_years = [x for r, e in ok if r["ein"] == NPT for x in rows_b(r, e)]
    npt = npt_years + pooled(npt_years, "region") + pooled(npt_years, "size_band") + affiliate_rows(exts, read_h10(a.fx_h10))
    write_csv(os.path.join(a.root, OUT_B), npt, FIELDS_B)
    print(json.dumps({"returns": [(r["sponsor"], r["tax_period"], r["object_id"], e.get("via", e.get("status")),
                                   e.get("tax_period_begin"), e.get("tax_period_end")) for r, e in exts_list],
                      "failed": bad, "ein_mismatch": mism, "rows_a": len(rows), "rows_b": len(npt)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
