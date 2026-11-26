#!/usr/bin/env python3
"""Financial resilience of the top-100 DAF sponsors, TY2021-2024 (queue item P-NEW-RES-01).

Stdlib only; functional style (pure transforms, I/O at the edges).

Question: how much of a sponsor's balance sheet is NOT donor-advised money, how many months of operating cost
that non-DAF / unrestricted cushion covers, what the operating revenue mix is (contributions, program-service
revenue / fees, investment income) and whether the sponsor runs an operating surplus once DAF flows are stripped.

Per return (Form 990 e-file XML; parsing stops before Schedule E, so Schedule I tables are never read):
  Part I     total revenue, total expenses, revenue less expenses (line 19)
  Part VIII  lines 1h, 2a-f rows (description) and 2g, 3, 4, 5, 6d, 7d, 8c, 9c, 10c, 11 rows (description), 12
  Part IX    every line by column (mission_sponsor_cost_structure.part_ix_from); line 25 total and the
             management & general column
  Part X     lines 1-2 cash, 10c PP&E, 16 total assets, 21 escrow / agency liability, 26 total liabilities,
             27 net assets without donor restrictions, 28 with donor restrictions, 29-31 (non-ASC 958 filers),
             32 total net assets (BOY and EOY)
  Part XI    line 5 net unrealised gains, line 9 other changes
  Sched D    Part I DAF (a) and other funds (b): count, contributions, grants, EOY value; Part V current-year
             endowment balance, administrative expenses charged, board-designated / permanent / term %

Universe: the 100 sponsors ranked 1-100 by FY2024 DAF assets in form990-returns-schedule-d-harvest-full.csv
(`fy2024_asset_rank`; same universe as mission_sponsor_marketing.py). Returns: every Form 990 for those EINs in
IRS index_2021-2026; one per sponsor x tax year (TY = year in which the period begins), longest period then latest
ReturnTs; TY2021-2024.

Sources, in order: the GivingTuesday mirror of IRS e-file XML (robots.txt 404 = no restriction); then TEOS zip
members already range-read by earlier batches (--teos-dir, local files only; no apps.irs.gov requests here).

Reused: mission_990_contractors (num/CSV/XML helpers), mission_sponsor_cost_structure (Part IX map),
mission_sponsor_marketing (universe, groups, IRS index, return picking, period months),
mission_sponsor_compensation (DAFRC panel with applied corrections; segment table for two affiliated nationals).

Usage:
  python3 scripts/mission_sponsor_resilience.py --irs-dir IRS --cache-dir CACHE --teos-dir DIR [...] [--fetch]
Outputs:
  data/mission-2026-11-14/sponsor-financial-resilience-2021-2024.csv  (row_type = sponsor_year | group_year |
                                                                       group_trend)
  prints a JSON summary used by research/mission-2026-11-14/direction-sponsor-financial-resilience.md
"""
from __future__ import annotations

import argparse
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
import mission_sponsor_marketing as mkt  # noqa: E402
import mission_sponsor_compensation as msc  # noqa: E402

DATA = m990.DATA
OUT = os.path.join(DATA, "sponsor-financial-resilience-2021-2024.csv")
HARVEST_CSV = mkt.HARVEST_CSV
EXTRACT_VERSION = 1
TY_RANGE = (2021, 2024)
num, ein9, read_csv, write_csv, local, text_of = m990.num, m990.ein9, m990.read_csv, m990.write_csv, m990.local, m990.text_of
NS = m990.NS
UA = {"User-Agent": "research-script/1.0 (stdlib urllib)"}

# Group overrides [I]: the executive-compensation direction (batch 43 N24, SEGMENT table) classified these two as
# affiliated-commercial after checking Schedule O; the marketing script had left them "affiliation not checked".
AFFILIATED_EXTRA = {"311663020": "Eaton Vance / Morgan Stanley (US Charitable Gift Trust) [I, comp. direction]",
                    "352129262": "Renaissance (for-profit administrator) [I, comp. direction]"}
CAMPAIGN_ADVERTISING = mkt.CAMPAIGN_ADVERTISING
NATIONAL_GROUPS = frozenset({"affiliated_commercial_national", "independent_national", "processor", "digital_first"})
GROUP_ORDER = ("affiliated_commercial_national", "independent_national", "community_foundation", "single_issue",
               "processor", "digital_first", "university_health")
FEE_RX = re.compile(r"\bfees?\b|administrat|\badmin\b|service charge|management fee|mgmt fee", re.I)

PART_X = {  # tag -> column stem (BOY/EOY kept)
    "CashNonInterestBearingGrp": "x01_cash", "SavingsAndTempCashInvstGrp": "x02_savings",
    "LandBldgEquipBasisNetGrp": "x10c_ppe_net", "TotalAssetsGrp": "x16_total_assets",
    "EscrowAccountLiabilityGrp": "x21_escrow_liab", "TotalLiabilitiesGrp": "x26_total_liab",
    "NoDonorRestrictionNetAssetsGrp": "x27_na_without_restr", "DonorRestrictionNetAssetsGrp": "x28_na_with_restr",
    "CapStkTrPrinCurrentFundsGrp": "x29_capital_stock", "PdInCapSrplsLandBldgEqpFundGrp": "x30_paid_in",
    "RtnEarnEndowmentIncmOthFndsGrp": "x31_retained", "TotalNetAssetsFundBalanceGrp": "x32_total_na"}
PART_VIII_COL = {  # group tag -> key (TotalRevenueColumnAmt)
    "InvestmentIncomeGrp": "v03_investment_income", "IncmFromInvestBondProceedsGrp": "v04_bond_proceeds",
    "RoyaltiesRevenueGrp": "v05_royalties", "NetRentalIncomeOrLossGrp": "v06d_net_rent",
    "NetGainOrLossInvestmentsGrp": "v07d_net_gain", "NetIncmFromFundraisingEvtGrp": "v08c_fundraising_events",
    "NetIncomeFromGamingGrp": "v09c_gaming", "NetIncomeOrLossGrp": "v10c_sales", "TotalRevenueGrp": "v12_total_revenue"}
PART_I = ("CYContributionsGrantsAmt", "CYProgramServiceRevenueAmt", "CYInvestmentIncomeAmt", "CYOtherRevenueAmt",
          "CYTotalRevenueAmt", "CYTotalExpensesAmt", "CYRevenuesLessExpensesAmt", "NetAssetsOrFundBalancesBOYAmt",
          "NetAssetsOrFundBalancesEOYAmt", "TotalAssetsEOYAmt")


# ----------------------------------------------------------------------------- small pure helpers
def ssum(*xs):
    v = tuple(x for x in xs if x is not None)
    return sum(v) if v else None


def sub(a, *bs):
    return None if a is None else a - sum(b or 0 for b in bs)


def div(a, b):
    return None if a is None or b is None or b == 0 else a / b


def pos_div(a, b):
    """a / b only when the denominator is positive (months of cover, margins)."""
    return None if a is None or b is None or b <= 0 else a / b


def median(xs: Iterable):
    v = [x for x in xs if x is not None]
    return statistics.median(v) if v else None


def quant(xs: Iterable, q: float):
    v = sorted(x for x in xs if x is not None)
    if not v:
        return None
    k = (len(v) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


# ----------------------------------------------------------------------------- universe
def group_of(u: Mapping) -> tuple[str, str]:
    if u["ein"] in AFFILIATED_EXTRA:
        return "affiliated_commercial_national", AFFILIATED_EXTRA[u["ein"]]
    if u["dafrc_subtype"] == "Universities and Healthcare":
        return "university_health", "DAFRC subtype Universities and Healthcare (whole-institution 990)"
    return u["sponsor_group"], u["group_basis"]


def universe(harvest: Sequence[Mapping]) -> dict:
    uni = {e: u for e, u in mkt.universe(harvest).items() if u["selection"] == "top100_fy2024_daf_assets"}
    return {e: {**u, **dict(zip(("sponsor_group", "group_basis"), group_of(u)))} for e, u in uni.items()}


# ----------------------------------------------------------------------------- XML extract (streamed, early stop)
def amt(el, tag: str, col: str):
    return num(text_of(el, (tag, col)))


def part_viii_rows(el, tag: str) -> list:
    return [{"desc": text_of(g, ("Desc",)), "code": text_of(g, ("BusinessCd",)),
             "amt": num(text_of(g, ("TotalRevenueColumnAmt",)))} for g in el if local(g.tag) == tag]


def irs990_fields(el) -> dict:
    px = {f"{stem}_{c.lower()}": amt(el, tag, f"{c}Amt") for tag, stem in PART_X.items() for c in ("BOY", "EOY")}
    pviii = {k: amt(el, t, "TotalRevenueColumnAmt") for t, k in PART_VIII_COL.items()}
    return {"part_i": {t: num(text_of(el, (t,))) for t in PART_I},
            "part_ix": mcs.part_ix_from(el),
            "part_x": px,
            "part_viii": {**pviii, "v01h_contributions": num(text_of(el, ("TotalContributionsAmt",))),
                          "v02g_program_service": num(text_of(el, ("TotalProgramServiceRevenueAmt",)))},
            "psr_rows": part_viii_rows(el, "ProgramServiceRevenueGrp"),
            "misc_rows": part_viii_rows(el, "OtherRevenueMiscGrp"),
            "part_xi": {"xi05_unrealized": num(text_of(el, ("NetUnrlzdGainsLossesInvstAmt",))),
                        "xi09_other_changes": num(text_of(el, ("OtherChangesInNetAssetsAmt",)))},
            "fasb_ind": text_of(el, ("OrganizationFollowsFASB117Ind",)) or text_of(el, ("OrgDoesNotFollowFASB117Ind",)),
            "amended_ind": text_of(el, ("AmendedReturnInd",))}


def sched_d_fields(el) -> dict:
    g = lambda t: num(text_of(el, (t,)))  # noqa: E731
    return {"sched_d_present": 1,
            "daf_count": g("DonorAdvisedFundsHeldCnt"), "daf_contrib": g("DonorAdvisedFundsContriAmt"),
            "daf_grants": g("DonorAdvisedFundsGrantsAmt"), "daf_eoy": g("DonorAdvisedFundsVlEOYAmt"),
            "oth_count": g("FundsAndOtherAccountsHeldCnt"), "oth_contrib": g("FundsAndOtherAccountsContriAmt"),
            "oth_grants": g("FundsAndOtherAccountsGrantsAmt"), "oth_eoy": g("FundsAndOtherAccountsVlEOYAmt"),
            "endow_eoy": num(text_of(el, ("CYEndwmtFundGrp", "EndYearBalanceAmt"))),
            "endow_admin_exp": num(text_of(el, ("CYEndwmtFundGrp", "AdministrativeExpensesAmt"))),
            "endow_board_pct": g("BoardDesignatedBalanceEOYPct"), "endow_perm_pct": g("PrmnntEndowmentBalanceEOYPct"),
            "endow_term_pct": g("TermEndowmentBalanceEOYPct")}


def extract_stream(stream) -> dict:
    out: dict = {"sched_d_present": 0}
    for event, el in ET.iterparse(stream, events=("start", "end")):
        tag = local(el.tag)
        if event == "start":
            if tag.startswith("IRS990Schedule") and tag[len("IRS990Schedule"):][:1] > "D":
                break
            continue
        if tag == "ReturnHeader":
            out.update({"tax_period_end": text_of(el, ("TaxPeriodEndDt",)),
                        "tax_period_begin": text_of(el, ("TaxPeriodBeginDt",)),
                        "return_ts": text_of(el, ("ReturnTs",)), "return_type": text_of(el, ("ReturnTypeCd",))})
            el.clear()
        elif tag == "IRS990":
            out.update(irs990_fields(el))
            el.clear()
        elif tag == "IRS990ScheduleD":
            out.update(sched_d_fields(el))
            break
        elif tag.startswith("IRS990Schedule"):
            el.clear()
    return out


def fetch_extract(oid: str, cache_dir: str, teos_dirs: Sequence[str], fetch: bool, retries: int = 2) -> dict:
    path = os.path.join(cache_dir, "extract990res", f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            cached = json.load(fh)
        if cached.get("_v") == EXTRACT_VERSION:
            return cached
    url = m990.XML_URL.format(oid=oid)
    out = {"xml_status": "not_fetched"}
    if fetch:
        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as resp:
                    out = {**extract_stream(resp), "xml_status": "ok", "xml_source": "gt_mirror"}
                break
            except urllib.error.HTTPError as e:
                out = {"xml_status": f"http_{e.code}"}
                if e.code in (403, 404):
                    break
            except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
                out = {"xml_status": f"error:{type(e).__name__}"}
                time.sleep(2 * (attempt + 1))
    local_xml = mkt.teos_path(oid, teos_dirs)
    if out["xml_status"] != "ok" and local_xml:
        with open(local_xml, "rb") as fh:
            out = {**extract_stream(fh), "xml_status": "ok", "xml_source": "teos_zip_member_cached",
                   "mirror_status": out["xml_status"]}
    result = {**out, "_v": EXTRACT_VERSION}
    if result["xml_status"] == "ok" or result["xml_status"].startswith("http_404"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(result, fh)
    return result


# ----------------------------------------------------------------------------- sponsor-year row (pure)
def ix(x: Mapping, line: str, col: str = "total"):
    return ((x.get("part_ix") or {}).get(line) or {}).get(col)


def ix_lines(x: Mapping, prefixes: Sequence[str], col: str = "total"):
    return ssum(*(v.get(col) for k, v in (x.get("part_ix") or {}).items() if k.startswith(tuple(prefixes))))


def return_row(u: Mapping, idx: Mapping, x: Mapping, pn: Mapping) -> dict:
    pi, px, pv, pxi = (x.get(k) or {} for k in ("part_i", "part_x", "part_viii", "part_xi"))
    begin, end = x.get("tax_period_begin", ""), x.get("tax_period_end", "")
    ty = int(begin[:4]) if begin[:4].isdigit() else None
    fy = int(end[:4]) if end[:4].isdigit() else None
    pm = mkt.months(begin, end)
    ann = 12 / pm if pm else None
    # Schedule D DAF value; fall back to the corrected DAFRC panel for the same FY (flagged)
    dafrc = pn.get((u["ein"], fy)) or {}
    daf = x.get("daf_eoy") if x.get("daf_eoy") is not None else dafrc.get("assets")
    daf_src = "990_sched_d" if x.get("daf_eoy") is not None else ("dafrc_corrected" if daf is not None else "")
    oth = x.get("oth_eoy")
    na_total = px.get("x32_total_na_eoy") if px.get("x32_total_na_eoy") is not None else pi.get("NetAssetsOrFundBalancesEOYAmt")
    na_wo = px.get("x27_na_without_restr_eoy")
    na_w = px.get("x28_na_with_restr_eoy")
    ppe = px.get("x10c_ppe_net_eoy") or 0.0
    board = (x.get("endow_eoy") or 0) * (x.get("endow_board_pct") or 0) if x.get("endow_eoy") else 0.0
    l25 = ix(x, "l25_total")
    l25_mgmt = ix(x, "l25_total", "mgmt")
    l25_fr = ix(x, "l25_total", "fundraising")
    grants = ix_lines(x, ("l01", "l02", "l03"))
    l04 = ix_lines(x, ("l04",))
    l11f = ix(x, "l11f_fees_investment_mgmt")
    l11f_mgmt = ix(x, "l11f_fees_investment_mgmt", "mgmt")
    admin = sub(l25_mgmt, l11f_mgmt) if l25_mgmt is not None else None   # M&G column less its line-11f cell
    opcost = sub(l25, grants, l04, l11f)                      # governing definition (cost-structure wave 5)
    opcost_ann = opcost * ann if opcost is not None and ann else opcost
    l25_ann = l25 * ann if l25 is not None and ann else l25
    mgmt_ann = admin * ann if admin is not None and ann else admin
    # reserves (EOY)
    r1 = sub(na_total, daf) if daf is not None else None                      # non-DAF net assets
    r2 = sub(na_wo, daf) if (na_wo is not None and daf is not None) else None  # unrestricted net of DAFs
    r3 = na_wo                                                                # literal Part X line 27
    r4 = sub(r2, ppe) if r2 is not None else None                             # r2 less net PP&E
    r5 = sub(r4, board) if r4 is not None else None                           # r4 less board-designated endowment
    r6 = sub(r1, oth) if r1 is not None else None                             # non-DAF net assets less Sched D (b) funds
    rev = pv.get("v12_total_revenue") if pv.get("v12_total_revenue") is not None else pi.get("CYTotalRevenueAmt")
    contrib = pv.get("v01h_contributions") if pv.get("v01h_contributions") is not None else pi.get("CYContributionsGrantsAmt")
    psr = pv.get("v02g_program_service") if pv.get("v02g_program_service") is not None else pi.get("CYProgramServiceRevenueAmt")
    inv_core = ssum(pv.get("v03_investment_income"), pv.get("v04_bond_proceeds"), pv.get("v05_royalties"))
    gains = pv.get("v07d_net_gain")
    other = sub(rev, contrib, psr, inv_core, gains) if rev is not None else None
    fee_misc = ssum(*(r["amt"] for r in x.get("misc_rows", []) if FEE_RX.search(r["desc"] or "")))
    fee_psr = ssum(*(r["amt"] for r in x.get("psr_rows", []) if FEE_RX.search(r["desc"] or "")))
    fee_on_990 = ssum(fee_psr, fee_misc) or 0.0             # description-matched fee lines only (Part VIII 2 and 11)
    s1 = pi.get("CYRevenuesLessExpensesAmt") if pi.get("CYRevenuesLessExpensesAmt") is not None else sub(rev, l25)
    daf_net_flow = sub(x.get("daf_contrib"), x.get("daf_grants")) if x.get("daf_contrib") is not None else None
    s2 = sub(s1, daf_net_flow) if s1 is not None and daf_net_flow is not None else None
    s3 = sub(s2, gains) if s2 is not None else None
    s4 = sub(s3, inv_core) if s3 is not None else None
    per = lambda r, d: pos_div(r, d / 12) if d is not None else None  # noqa: E731
    flags = tuple(f for f, c in (
        ("short_or_long_period", pm not in (None, 12)),
        ("amended_return", x.get("amended_ind") in ("X", "true", "1")),
        ("sched_d_daf_blank", x.get("daf_eoy") is None),
        ("daf_value_from_dafrc", daf_src == "dafrc_corrected"),
        ("no_asc958_split", na_wo is None),
        ("daf_gt_na_without_restr", na_wo is not None and daf is not None and daf > na_wo),
        ("daf_gt_total_na", na_total is not None and daf is not None and daf > na_total),
        ("mgmt_column_zero", (l25 or 0) > 0 and (l25_mgmt or 0) == 0),
        ("opcost_le_0", opcost is not None and opcost <= 0),
        ("opcost_lt_1bp_daf", opcost is not None and daf and opcost_ann is not None and 0 < opcost_ann < daf * 1e-4),
        ("board_endowment_gt_unrestricted_less_daf", r4 is not None and r5 is not None and r4 > 0 > r5),
        ("total_revenue_le_0", rev is not None and rev <= 0),
        ("affiliate_costs_off_990", u["sponsor_group"] == "affiliated_commercial_national"),
        ("campaign_advertising_in_opcost", u["ein"] in CAMPAIGN_ADVERTISING),
        ("university_health_whole_org", u["sponsor_group"] == "university_health"),
        ("escrow_agency_liability", (px.get("x21_escrow_liab_eoy") or 0) > 0)) if c)
    return {
        "row_type": "sponsor_year", "ein": u["ein"], "sponsor_name": u["sponsor_name"],
        "fy2024_asset_rank": u["fy2024_asset_rank"], "sponsor_group": u["sponsor_group"], "group_basis": u["group_basis"],
        "dafrc_type": u["dafrc_type"], "dafrc_subtype": u["dafrc_subtype"], "tax_year": ty, "fiscal_year": fy,
        "tax_period_begin": begin, "tax_period_end": end, "period_months": pm, "object_id": idx["OBJECT_ID"],
        "return_ts": x.get("return_ts"), "xml_source": x.get("xml_source"),
        "total_assets_eoy": px.get("x16_total_assets_eoy") if px.get("x16_total_assets_eoy") is not None else pi.get("TotalAssetsEOYAmt"),
        "total_liabilities_eoy": px.get("x26_total_liab_eoy"), "escrow_agency_liab_eoy": px.get("x21_escrow_liab_eoy"),
        "cash_and_savings_eoy": ssum(px.get("x01_cash_eoy"), px.get("x02_savings_eoy")), "ppe_net_eoy": px.get("x10c_ppe_net_eoy"),
        "na_total_boy": px.get("x32_total_na_boy") if px.get("x32_total_na_boy") is not None else pi.get("NetAssetsOrFundBalancesBOYAmt"),
        "na_total_eoy": na_total, "na_without_restr_eoy": na_wo, "na_with_restr_eoy": na_w,
        "na_without_restr_boy": px.get("x27_na_without_restr_boy"),
        "na_lines_29_31_eoy": ssum(px.get("x29_capital_stock_eoy"), px.get("x30_paid_in_eoy"), px.get("x31_retained_eoy")),
        "fasb_ind": x.get("fasb_ind"),
        "daf_value_eoy": daf, "daf_value_source": daf_src, "daf_count": x.get("daf_count"),
        "daf_contributions": x.get("daf_contrib"), "daf_grants": x.get("daf_grants"),
        "other_funds_value_eoy": oth, "other_funds_count": x.get("oth_count"),
        "endowment_eoy": x.get("endow_eoy"), "endowment_board_designated_pct": x.get("endow_board_pct"),
        "endowment_permanent_pct": x.get("endow_perm_pct"), "endowment_term_pct": x.get("endow_term_pct"),
        "endowment_admin_expenses_cy": x.get("endow_admin_exp"),
        "daf_share_of_total_na": div(daf, na_total),
        "r1_nondaf_na": r1, "r2_unrestricted_less_daf": r2, "r3_unrestricted_literal": r3,
        "r4_unrestricted_less_daf_ppe": r4, "r5_unrestricted_less_daf_ppe_board_endow": r5,
        "r6_nondaf_na_less_other_funds": r6,
        "l25_total_expenses": l25, "l25_program": ix(x, "l25_total", "program"), "l25_mgmt_general": l25_mgmt,
        "l25_fundraising": l25_fr, "l11f_mgmt_column": l11f_mgmt, "admin_mgmt_ex_11f": admin, "grants_l1_3": grants, "l04_member_benefits": l04, "l11f_invest_mgmt_fees": l11f,
        "operating_cost": opcost, "operating_cost_annualised": opcost_ann,
        "mgmt_share_of_l25": div(l25_mgmt, l25), "mgmt_share_of_opcost": pos_div(admin, opcost),
        "opcost_bps_daf": pos_div(opcost_ann, daf) and pos_div(opcost_ann, daf) * 1e4,
        "mgmt_bps_daf": pos_div(mgmt_ann, daf) and pos_div(mgmt_ann, daf) * 1e4,
        "months_opcost_r1": per(r1, opcost_ann), "months_opcost_r2": per(r2, opcost_ann),
        "months_opcost_r3": per(r3, opcost_ann), "months_opcost_r4": per(r4, opcost_ann),
        "months_opcost_r5": per(r5, opcost_ann), "months_opcost_r6": per(r6, opcost_ann),
        "months_mgmt_r1": per(r1, mgmt_ann), "months_l25_r1": per(r1, l25_ann),
        "rev_total": rev, "rev_contributions_1h": contrib, "rev_program_service_2g": psr,
        "rev_investment_income_3_4_5": inv_core, "rev_net_gains_7d": gains, "rev_other_residual": other,
        "rev_net_rent_6d": pv.get("v06d_net_rent"), "rev_fundraising_events_8c": pv.get("v08c_fundraising_events"),
        "psr_rows": " | ".join(f"{r['desc']}: {r['amt']:.0f}" for r in x.get("psr_rows", []) if r["amt"] is not None)[:400],
        "misc_revenue_rows": " | ".join(f"{r['desc']}: {r['amt']:.0f}" for r in x.get("misc_rows", []) if r["amt"] is not None)[:400],
        "fee_like_misc_revenue": fee_misc, "fee_like_psr_rows": fee_psr, "fee_income_on_990": fee_on_990,
        "share_contributions": pos_div(contrib, rev), "share_program_service": pos_div(psr, rev),
        "share_investment_income": pos_div(inv_core, rev), "share_net_gains": pos_div(gains, rev),
        "fee_income_cover_opcost": pos_div(fee_on_990, opcost), "inv_income_cover_opcost": pos_div(inv_core, opcost),
        "endowment_admin_cover_opcost": pos_div(x.get("endow_admin_exp"), opcost),
        "s1_rev_less_exp_line19": s1, "daf_net_inflow": daf_net_flow, "s2_ex_daf_flows": s2,
        "s3_ex_daf_flows_ex_gains": s3, "s4_ex_daf_flows_ex_all_investment": s4,
        "s2_per_opcost": pos_div(s2, opcost), "s3_per_opcost": pos_div(s3, opcost), "s4_per_opcost": pos_div(s4, opcost),
        "xi05_unrealized_gains": pxi.get("xi05_unrealized"), "xi09_other_changes": pxi.get("xi09_other_changes"),
        "quality_flags": "|".join(flags)}


def with_changes(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    """Year-on-year change in non-DAF net assets (R1) against the sponsor's previous TY row; DAF roll-forward
    residual; and `daf_share_break`: a national / processor row whose Sched D DAF value is < 85% of Part X net
    assets while every neighbouring TY row of the same sponsor is > 95% (an isolated break, read as a Schedule D
    value that does not match the balance sheet; excluded from group statistics)."""
    by = {(r["ein"], r["tax_year"]): r for r in rows}
    def brk(r):
        nb = tuple(by[(r["ein"], r["tax_year"] + d)]["daf_share_of_total_na"] for d in (-1, 1) if (r["ein"], r["tax_year"] + d) in by)
        nb = tuple(v for v in nb if v is not None)
        return (r["sponsor_group"] in NATIONAL_GROUPS and r["daf_share_of_total_na"] is not None
                and r["daf_share_of_total_na"] < 0.85 and bool(nb) and all(v > 0.95 for v in nb))
    broken = frozenset((r["ein"], r["tax_year"]) for r in rows if brk(r))
    def one(r):
        r = {**r, "quality_flags": "|".join(f for f in (r["quality_flags"], "daf_share_break" if (r["ein"], r["tax_year"]) in broken else "") if f)}
        p = by.get((r["ein"], r["tax_year"] - 1))
        p = None if p is None or (r["ein"], r["tax_year"] - 1) in broken or (r["ein"], r["tax_year"]) in broken else p
        d = sub(r["r1_nondaf_na"], p["r1_nondaf_na"]) if p and r["r1_nondaf_na"] is not None and p["r1_nondaf_na"] is not None else None
        implied = ssum(p["daf_value_eoy"], r["daf_contributions"], -(r["daf_grants"] or 0)) if p and p["daf_value_eoy"] else None
        resid = div(sub(r["daf_value_eoy"], implied), p["daf_value_eoy"]) if implied is not None and r["daf_value_eoy"] is not None else None
        return {**r, "r1_change_yoy": d, "r1_change_per_opcost": pos_div(d, r["operating_cost_annualised"]),
                "daf_rollforward_residual_pct": resid}
    return tuple(one(r) for r in rows)


# ----------------------------------------------------------------------------- aggregates (pure)
def analysable(r: Mapping) -> bool:
    return (r["sponsor_group"] != "university_health" and r["operating_cost"] is not None and r["operating_cost"] > 0
            and r["daf_value_eoy"] is not None and "daf_share_break" not in r["quality_flags"])


MED_KEYS = ("months_opcost_r1", "months_opcost_r2", "months_opcost_r3", "months_opcost_r4", "months_opcost_r5",
            "months_opcost_r6", "months_l25_r1", "daf_share_of_total_na", "mgmt_share_of_opcost", "mgmt_share_of_l25",
            "opcost_bps_daf", "mgmt_bps_daf", "share_contributions", "share_program_service", "share_investment_income",
            "fee_income_cover_opcost", "inv_income_cover_opcost", "endowment_admin_cover_opcost", "s2_per_opcost", "s3_per_opcost", "s4_per_opcost",
            "r1_change_per_opcost")
SUM_KEYS = ("na_total_eoy", "na_without_restr_eoy", "daf_value_eoy", "r1_nondaf_na", "r2_unrestricted_less_daf",
            "r4_unrestricted_less_daf_ppe", "r5_unrestricted_less_daf_ppe_board_endow", "r6_nondaf_na_less_other_funds",
            "operating_cost_annualised", "l25_total_expenses", "l25_mgmt_general", "admin_mgmt_ex_11f", "r1_change_yoy", "rev_total", "rev_contributions_1h",
            "rev_program_service_2g", "rev_investment_income_3_4_5", "rev_net_gains_7d", "rev_other_residual",
            "fee_income_on_990", "endowment_admin_expenses_cy", "s1_rev_less_exp_line19", "s2_ex_daf_flows", "s3_ex_daf_flows_ex_gains",
            "s4_ex_daf_flows_ex_all_investment")


def group_stats(rows: Sequence[Mapping], group: str, ty) -> dict:
    rs = tuple(r for r in rows if analysable(r))
    sums = {f"sum_{k}": ssum(*(r[k] for r in rs)) for k in SUM_KEYS}
    meds = {f"med_{k}": median(r[k] for r in rs) for k in MED_KEYS}
    p25 = {f"p25_{k}": quant((r[k] for r in rs), .25) for k in ("months_opcost_r1", "months_opcost_r2", "months_opcost_r5")}
    p75 = {f"p75_{k}": quant((r[k] for r in rs), .75) for k in ("months_opcost_r1", "months_opcost_r2", "months_opcost_r5")}
    oc = sums["sum_operating_cost_annualised"]
    pooled = {"pooled_months_opcost_r1": pos_div(sums["sum_r1_nondaf_na"], oc / 12 if oc else None),
              "pooled_months_opcost_r2": pos_div(sums["sum_r2_unrestricted_less_daf"], oc / 12 if oc else None),
              "pooled_months_opcost_r5": pos_div(sums["sum_r5_unrestricted_less_daf_ppe_board_endow"], oc / 12 if oc else None),
              "pooled_mgmt_share_of_opcost": pos_div(sums["sum_admin_mgmt_ex_11f"], oc),
              "pooled_r1_change_per_opcost": pos_div(sums["sum_r1_change_yoy"], ssum(*(r["operating_cost_annualised"] for r in rs if r["r1_change_yoy"] is not None))),
              "pooled_share_contributions": pos_div(sums["sum_rev_contributions_1h"], sums["sum_rev_total"]),
              "pooled_share_program_service": pos_div(sums["sum_rev_program_service_2g"], sums["sum_rev_total"]),
              "pooled_share_investment_income": pos_div(sums["sum_rev_investment_income_3_4_5"], sums["sum_rev_total"]),
              "pooled_share_net_gains": pos_div(sums["sum_rev_net_gains_7d"], sums["sum_rev_total"]),
              "pooled_fee_income_cover_opcost": pos_div(sums["sum_fee_income_on_990"], oc),
              "pooled_endowment_admin_cover_opcost": pos_div(sums["sum_endowment_admin_expenses_cy"], oc),
              "pooled_daf_share_of_total_na": pos_div(sums["sum_daf_value_eoy"], sums["sum_na_total_eoy"])}
    counts = {"n_returns": len(rs), "n_sponsors": len({r["ein"] for r in rs}),
              "n_r1_le_0": sum(1 for r in rs if r["r1_nondaf_na"] is not None and r["r1_nondaf_na"] <= 0),
              "n_r2_le_0": sum(1 for r in rs if r["r2_unrestricted_less_daf"] is not None and r["r2_unrestricted_less_daf"] <= 0),
              "n_months_r2_lt_3": sum(1 for r in rs if r["r2_unrestricted_less_daf"] is not None and (r["months_opcost_r2"] or 0) < 3),
              "n_r1_change_negative": sum(1 for r in rs if r["r1_change_yoy"] is not None and r["r1_change_yoy"] < 0),
              "n_r1_change_known": sum(1 for r in rs if r["r1_change_yoy"] is not None),
              "n_opcost_lt_1bp_daf": sum(1 for r in rs if "opcost_lt_1bp_daf" in r["quality_flags"]),
              "n_s2_deficit": sum(1 for r in rs if r["s2_ex_daf_flows"] is not None and r["s2_ex_daf_flows"] < 0),
              "n_s4_deficit": sum(1 for r in rs if r["s4_ex_daf_flows_ex_all_investment"] is not None and r["s4_ex_daf_flows_ex_all_investment"] < 0),
              "n_s4_known": sum(1 for r in rs if r["s4_ex_daf_flows_ex_all_investment"] is not None),
              "n_psr_positive": sum(1 for r in rs if (r["rev_program_service_2g"] or 0) > 0),
              "n_fee_lines_positive": sum(1 for r in rs if (r["fee_income_on_990"] or 0) > 0),
              "n_mgmt_column_zero": sum(1 for r in rs if "mgmt_column_zero" in r["quality_flags"]),
              "n_daf_gt_na_without_restr": sum(1 for r in rs if "daf_gt_na_without_restr" in r["quality_flags"])}
    return {"row_type": "group_year", "sponsor_group": group, "tax_year": ty, **counts, **sums, **meds, **p25, **p75, **pooled}


def summaries(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    groups = tuple(g for g in GROUP_ORDER if g != "university_health" and any(r["sponsor_group"] == g for r in rows)) + ("all_ex_university_health",)
    def pick(g, ty):
        return tuple(r for r in rows if (g == "all_ex_university_health" or r["sponsor_group"] == g) and r["tax_year"] == ty)
    return tuple(group_stats(pick(g, ty), g, ty) for g in groups for ty in range(TY_RANGE[0], TY_RANGE[1] + 1))


def trends(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    """Matched sponsors analysable in both TY2021 and TY2024: medians of each metric in both years."""
    by = {(r["ein"], r["tax_year"]): r for r in rows if analysable(r)}
    keys = ("months_opcost_r1", "months_opcost_r2", "months_opcost_r5", "mgmt_share_of_opcost", "opcost_bps_daf",
            "share_program_service", "fee_income_cover_opcost", "s2_per_opcost", "s4_per_opcost")
    def one(g):
        eins = sorted({e for (e, ty) in by if ty == 2021 and (e, 2024) in by
                       and (g == "all_ex_university_health" or by[(e, ty)]["sponsor_group"] == g)})
        out = {"row_type": "group_trend", "sponsor_group": g, "tax_year": "2021->2024", "n_sponsors": len(eins)}
        for k in keys:
            a, b = median(by[(e, 2021)][k] for e in eins), median(by[(e, 2024)][k] for e in eins)
            out.update({f"med_{k}_2021": a, f"med_{k}_2024": b})
        oc = lambda ty: ssum(*(by[(e, ty)]["operating_cost_annualised"] for e in eins))  # noqa: E731
        r1 = lambda ty: ssum(*(by[(e, ty)]["r1_nondaf_na"] for e in eins))  # noqa: E731
        out.update({"pooled_opcost_growth_pa": ((oc(2024) / oc(2021)) ** (1 / 3) - 1) if oc(2021) and oc(2024) and oc(2021) > 0 else None,
                    "pooled_r1_growth_pa": ((r1(2024) / r1(2021)) ** (1 / 3) - 1) if r1(2021) and r1(2024) and r1(2021) > 0 and r1(2024) > 0 else None,
                    "n_s2_deficit_2021": sum(1 for e in eins if (by[(e, 2021)]["s2_ex_daf_flows"] or 0) < 0),
                    "n_s2_deficit_2024": sum(1 for e in eins if (by[(e, 2024)]["s2_ex_daf_flows"] or 0) < 0)})
        return out
    groups = tuple(g for g in GROUP_ORDER if g != "university_health" and any(r["sponsor_group"] == g for r in rows)) + ("all_ex_university_health",)
    return tuple(one(g) for g in groups)


def round_row(r: Mapping) -> dict:
    def rd(k, v):
        if not isinstance(v, float):
            return v
        if any(t in k for t in ("share", "cover", "per_opcost", "_pct", "growth", "rollforward")):
            return round(v, 4)
        if "months" in k or "bps" in k:
            return round(v, 2)
        return round(v)
    return {k: rd(k, v) for k, v in r.items()}


def fields(rows: Sequence[Mapping]) -> tuple[str, ...]:
    seen: dict = {}
    for r in rows:
        for k in r:
            seen.setdefault(k, None)
    return tuple(seen)


# ----------------------------------------------------------------------------- main (I/O)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--teos-dir", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args(argv)
    harvest = tuple({**h, "ein": ein9(h["ein"])} for h in read_csv(HARVEST_CSV))
    uni = universe(harvest)
    pn = msc.panel(read_csv(msc.DAFRC_CSV), read_csv(msc.ITEMIZED_CSV))
    idx = mkt.pick_returns(mkt.index_rows(a.irs_dir, frozenset(uni)))
    idx = tuple(i for i in idx if i["TAX_PERIOD"] <= "202511")   # TY2024 periods end by 2025-11
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        exts = dict(zip((i["OBJECT_ID"] for i in idx),
                        ex.map(lambda i: fetch_extract(i["OBJECT_ID"], a.cache_dir, a.teos_dir, a.fetch), idx)))
    status: dict = {}
    for i in idx:
        s = exts[i["OBJECT_ID"]]["xml_status"]
        status[s] = status.get(s, 0) + 1
    ok = tuple(i for i in idx if exts[i["OBJECT_ID"]]["xml_status"] == "ok")
    base = tuple(return_row(uni[i["EIN"]], i, exts[i["OBJECT_ID"]], pn) for i in ok)
    base = tuple(r for r in base if r["tax_year"] and TY_RANGE[0] <= r["tax_year"] <= TY_RANGE[1])
    keep: dict = {}
    for r in sorted(base, key=lambda r: ((r["period_months"] or 0), r["return_ts"] or "", r["object_id"])):
        keep[(r["ein"], r["tax_year"])] = r
    rows = with_changes(tuple(sorted(keep.values(), key=lambda r: (GROUP_ORDER.index(r["sponsor_group"]),
                                                                   int(r["fy2024_asset_rank"]), r["tax_year"]))))
    summ, tr = summaries(rows), trends(rows)
    allrows = tuple(round_row(r) for r in rows + summ + tr)
    write_csv(OUT, allrows, fields(allrows))
    cov: dict = {}
    for r in rows:
        cov.setdefault(r["sponsor_group"], {}).setdefault(r["tax_year"], 0)
        cov[r["sponsor_group"]][r["tax_year"]] += 1
    missing = tuple({"ein": i["EIN"], "period": i["TAX_PERIOD"], "oid": i["OBJECT_ID"], "status": exts[i["OBJECT_ID"]]["xml_status"]}
                    for i in idx if exts[i["OBJECT_ID"]]["xml_status"] != "ok")
    no_rows = sorted(e for e in uni if e not in {r["ein"] for r in rows})
    gaps = sorted((uni[e]["sponsor_name"], ty) for e in uni for ty in range(2021, 2025) if (e, ty) not in keep)
    print(json.dumps({"universe": len(uni), "index_returns": len(idx), "xml_status": status, "missing": missing,
                      "rows": len(rows), "dup_period_dropped": len(base) - len(keep), "coverage": cov,
                      "sponsors_without_rows": [(e, uni[e]["sponsor_name"]) for e in no_rows], "sponsor_year_gaps": gaps,
                      "n_analysable": sum(1 for r in rows if analysable(r)),
                      "flags": {f: sum(1 for r in rows if f in r["quality_flags"].split("|"))
                                for f in sorted({f for r in rows for f in r["quality_flags"].split("|") if f})}},
                     indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
