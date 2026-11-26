#!/usr/bin/env python3
"""In-fund investment cost per DAF dollar at the largest nationals, Fidelity CIAP adviser-fee rate, and where the
Morgan Stanley GIFT wrap fees sit in its Form 990 (queue items P-B31A-02, P-B31A-01, P-B31A-03).

Stdlib only; functional style (pure transforms, I/O at the edges). Reuses helpers from
scripts/mission_990_contractors.py.

Inputs
  * Transcribed published figures (constants below; each row carries its source URL):
      - Fidelity Charitable audited consolidated financial statements FY2025/2024, FY2024/2023, FY2023/2022
        (Note 3 pool balances; CIAP advisor-managed investments; Statement of Activities expense lines).
      - Fidelity Charitable "What it costs" page: gross and net pool expense ratios (pool data as of 2026-09-30).
      - Vanguard Charitable investments page, DAFgiving360 repo rows, NPT investment descriptions PDF: expense-ratio
        ranges only (pool assets are not published by these sponsors).
  * data/mission-2026-11-14/sponsor-cost-structure.csv: Part IX operating cost (incl. and excl. line 11f) per return.
  * Form 990 XML streamed from https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OID}_public.xml
    (Part VIII lines 3 and 7, Part IX 11f and line 24, Part X total assets, Schedule D Part XI/XII), cached as JSON in
    CACHE/extract990inv/{oid}.json.
  * Optional --verify-dir: folder holding pdftotext output of the Fidelity audits; every transcribed pool balance
    and CIAP figure is checked to appear verbatim.

Output
  data/mission-2026-11-14/infund-expense-nationals-2026.csv

Usage
  python3 scripts/mission_infund_costs.py --cache-dir CACHE [--fetch] [--verify-dir DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as m990  # noqa: E402

DATA = m990.DATA
COST_CSV = os.path.join(DATA, "sponsor-cost-structure.csv")
OUT_CSV = os.path.join(DATA, "infund-expense-nationals-2026.csv")
XML_URL = m990.XML_URL
EXTRACT_VERSION = 2
num, fmt, local, text_of = m990.num, m990.fmt, m990.local, m990.text_of

FC_AFS25 = "https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf"
FC_AFS24 = "https://fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf"
FC_AFS23 = "https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2023-2022.pdf"
FC_COST = "https://www.fidelitycharitable.org/giving-account/what-it-costs.html"
FC_CIAP = "https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf"
VC_INV = "https://www.vanguardcharitable.org/investments"
VC_FEES = "https://www.vanguardcharitable.org/fees-and-expenses"
NPT_INV = "https://www.nptrust.org/investment-descriptions-and-performance-npt/"
D360_REPO = "research/mission-2026-11-14/queue-adviser-fees-pools-npact.md (section 2; stockanalysis.com fund pages [3P])"
MS_CIRC = "https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf"
MS_UMA_ADV = "https://www.morganstanley.com/content/dam/msdotcom/en/wealth-investmentsolutions/pdfs/adv/adv_selectuma.pdf"

# Fidelity Note 3 pool balances (USD, 30 June) and the matching net / gross expense ratio (percent) from FC_COST.
# None = pool not listed on the expense-ratio page.
FIDELITY_POOLS = (
    # audit pool name,                                   fy2025,          fy2024,          net,   gross
    ("Asset Allocation 85% Equity",                   1_885_744_998,   1_455_808_750,   0.56,  0.59),
    ("Asset Allocation 70% Equity",                   2_333_352_337,   2_084_133_319,   0.55,  0.59),
    ("Asset Allocation 60% Equity",                   1_777_072_420,   1_556_507_952,   0.55,  0.58),
    ("Asset Allocation 50% Equity",                   2_231_116_559,   2_012_208_623,   0.45,  0.48),
    ("Asset Allocation 40% Equity",                     603_662_866,     582_222_370,   0.47,  0.49),
    ("Asset Allocation 30% Equity",                     572_972_321,     517_297_271,   0.47,  0.50),
    ("Asset Allocation 20% Equity",                   2_384_586_789,   2_001_312_647,   0.45,  0.48),
    ("U.S. Equity Pool",                              4_257_644_982,   3_870_169_768,   0.42,  0.42),
    ("Total Market Index Pool",                       8_439_416_425,   7_022_924_969,   0.015, 0.015),
    ("International Equity Pool",                       460_122_448,     379_577_918,   0.58,  0.58),
    ("International Index Pool",                      1_461_834_901,   1_211_380_163,   0.035, 0.035),
    ("Fixed Income Pool",                               365_390_247,     321_687_520,   0.36,  0.40),
    ("U.S. Bond Index Pool",                          1_342_153_457,   1_096_929_707,   0.025, 0.025),
    ("Money Market Pool",                            10_561_770_494,   6_996_918_373,   0.14,  0.18),
    ("Charitable Legacy Pool",                          594_604_862,     532_481_123,   0.65,  0.67),
    ("Charitable Cash Pool",                              1_056_657,         719_007,   None,  None),
    ("U.S. Equity Access Pool",                         889_046_293,     703_123_833,   0.34,  0.34),
    ("International Equity Access Pool",                 75_738_930,      64_027_816,   0.67,  0.67),
    ("Fixed Income Access Pool",                        106_733_704,      69_932_946,   0.52,  0.52),
    ("Short Term Fixed Income Access Pool",             418_350_415,     324_759_955,   0.33,  0.33),
    ("Impact Investing Pool",                           220_673_575,     234_952_955,   None,  None),
    ("Sustainable U.S. Index",                          625_666_231,     596_040_932,   0.11,  0.11),
    ("Sustainable International Index",                 102_313_822,      75_308_709,   0.20,  0.20),
    ("Sustainable U.S. Bond Index",                      90_130_231,      53_808_051,   0.10,  0.10),
    ("Inflation Protected Bond Index",                  143_999_262,      69_093_585,   0.05,  0.05),
    ("Environmental Impact Access",                     148_574_804,     134_865_943,   0.93,  0.93),
)
FIDELITY_POOL_TOTAL = {2025: 42_093_730_030, 2024: 33_968_194_205}
FIDELITY_TOTAL_INVESTMENTS = {2025: 79_232_938_398, 2024: 61_514_405_850}
# CIAP advisor-managed investments at 30 June (audit Note 3) and Statement of Activities lines (USD, FY ending June).
FIDELITY_CIAP = {2025: 37_139_208_368, 2024: 27_546_211_645, 2023: 22_433_249_315, 2022: 18_112_561_857}
FIDELITY_CIAP_MIX_2025 = {"equity securities": 15_606_579_501, "fixed-income securities": 4_396_175_098,
                          "mutual funds": 10_076_236_725, "alternative investment & private equity funds": 7_060_217_044}
FIDELITY_INV_MGMT_FEES = {2025: 84_317_489, 2024: 67_308_635, 2023: 53_687_639, 2022: 56_692_887}
FIDELITY_OTHER_EXPENSES = {2025: 21_311_634, 2024: 20_670_116, 2023: 9_982_465}
FIDELITY_AFS_URL = {2025: FC_AFS25, 2024: FC_AFS24, 2023: FC_AFS23, 2022: FC_AFS23}
FIDELITY_990 = {2025: "202601389349301700", 2024: "202521349349310887"}

# Sponsors without published pool assets: (sponsor, ein, low %, high %, label, basis, url, date)
RANGE_ONLY = (
    ("Vanguard Charitable", "232888152", 0.01, 0.59, "F",
     "70 'Expense Ratio Last updated 09/30/2026' values on the investments page, 0.01%-0.59%; page states index "
     "building blocks 0.01%-0.11% and values-driven 0.09%-0.59%; fees page example 'Average investment fee' 0.06%",
     VC_INV + " ; " + VC_FEES, "expense ratios as of 2026-09-30"),
    ("DAFgiving360", "311640316", 0.03, 0.669, "R/3P",
     "Pool fund expense ratios in repo: SWTSX 0.03% to PAXIX/JBALX ~0.66-0.67% (pre and post 2026-09-24 fund change)",
     D360_REPO, "2026-11-15 reads"),
    ("National Philanthropic Trust", "237825575", 0.07, 0.61, "F",
     "Weighted average management fee 0.07%-0.61% across 7 portfolios, plus a 0.10% (0.15% impact) investment "
     "advisory fee and trading costs up to 4 cents/share", NPT_INV, "NPT FOR IDAP 0926; fees as of 2026-06-30"),
)
NPT_ADVISORY_PCT = (0.10, 0.15)

# Returns for the investment-income test (P-B31A-03): (label, oid)
INCOME_TEST = (
    ("Morgan Stanley GIFT", "202302999349301010"), ("Morgan Stanley GIFT", "202403209349313980"),
    ("Morgan Stanley GIFT", "202503239349300435"),
    ("Fidelity Charitable", "202601389349301700"), ("Vanguard Charitable", "202511349349313096"),
    ("National Philanthropic Trust", "202601289349302480"), ("DAFgiving360", "202611199349300601"),
    ("GS DAF (GS Donor Advised Philanthropy Fund)", "202503109349303645"),
    ("BofA Charitable Gift Fund", "202503219349318170"), ("American Endowment Foundation", "202513219349310376"),
    ("Renaissance Charitable Foundation", "202543189349301959"), ("U.S. Charitable Gift Trust", "202533189349305673"),
    ("Raymond James CEF", "202630489349300743"),
)


# ----------------------------------------------------------------------------- streamed 990 extract
def amt(el, *path) -> float | None:
    return num(text_of(el, path))


def extract_inv_stream(stream) -> dict:
    out: dict = {}
    for _event, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        if tag == "ReturnHeader":
            out["tax_period_end"] = text_of(el, ("TaxPeriodEndDt",))
            el.clear()
        elif tag == "IRS990":
            out.update({
                "l3_investment_income": amt(el, "InvestmentIncomeGrp", "TotalRevenueColumnAmt"),
                "l7a_gross_sales_securities": amt(el, "GrossAmountSalesAssetsGrp", "SecuritiesAmt"),
                "l7b_cost_and_sales_expenses_securities": amt(el, "LessCostOthBasisSalesExpnssGrp", "SecuritiesAmt"),
                "l7d_net_gain": amt(el, "NetGainOrLossInvestmentsGrp", "TotalRevenueColumnAmt"),
                "l11f": amt(el, "FeesForSrvcInvstMgmntFeesGrp", "TotalAmt"),
                "l11g": amt(el, "FeesForServicesOtherGrp", "TotalAmt"),
                "l25_total": amt(el, "TotalFunctionalExpensesGrp", "TotalAmt"),
                "xi_5_unrealized": amt(el, "NetUnrlzdGainsLossesInvstAmt"),
                "net_assets_boy": amt(el, "NetAssetsOrFundBalancesBOYAmt"),
                "net_assets_eoy": amt(el, "NetAssetsOrFundBalancesEOYAmt"),
                "assets_boy": amt(el, "TotalAssetsGrp", "BOYAmt"), "assets_eoy": amt(el, "TotalAssetsGrp", "EOYAmt"),
                "l24": [(text_of(g, ("Desc",)), num(text_of(g, ("TotalAmt",)))) for g in el.iter(m990.NS + "OtherExpensesGrp")],
            })
            el.clear()
        elif tag == "IRS990ScheduleD":
            out.update({"sd_xi_4a_inv_exp": amt(el, "InvestmentExpensesNotIncldAmt"),
                        "sd_xii_4a_inv_exp": amt(el, "InvestmentExpensesNotIncld2Amt"),
                        "sd_xii_4b_other": amt(el, "OtherExpensesNotIncludedAmt"),
                        "sd_xii_2e_subtotal": amt(el, "ExpensesNotReportedAmt"),
                        "sd_xii_1_audit_expenses": amt(el, "TotalExpensesAndLossesAmt")})
            return out
        elif tag.startswith("IRS990Schedule"):
            el.clear()
    return out


def fetch_inv(oid: str, cache_dir: str, fetch: bool, retries: int = 2) -> dict:
    path = os.path.join(cache_dir, "extract990inv", f"{oid}.json")
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
                out = {**extract_inv_stream(resp), "xml_status": "ok"}
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


# ----------------------------------------------------------------------------- pure computations
def bps(x: float | None) -> str:
    return "" if x is None else f"{x * 1e4:.1f}"


def row(**kw) -> dict:
    return kw


def fidelity_pool_rows(fy: int) -> tuple[dict, ...]:
    idx = 1 if fy == 2025 else 2
    pools = tuple((p[0], p[idx], p[3], p[4]) for p in FIDELITY_POOLS)
    assert sum(p[1] for p in pools) == FIDELITY_POOL_TOTAL[fy], "pool balances do not sum to audit total"
    priced = tuple(p for p in pools if p[2] is not None)
    unpriced = sum(p[1] for p in pools if p[2] is None)
    w_net = sum(a * er / 100 for _, a, er, _ in priced)
    w_gross = sum(a * g / 100 for _, a, _, g in priced)
    priced_assets = sum(a for _, a, _, _ in priced)
    total = FIDELITY_POOL_TOTAL[fy]
    hi_unpriced = unpriced * 0.93 / 100
    url = FIDELITY_AFS_URL[fy] + " ; " + FC_COST
    per_pool = tuple(row(
        sponsor="Fidelity Charitable", ein="110303001", fiscal_year=fy, layer="pool_in_fund", item=name,
        assets_usd=fmt(float(a)), rate_bps=bps(er / 100) if er is not None else "",
        amount_usd=fmt(round(a * er / 100)) if er is not None else "", weighting="pool",
        basis=f"net expense ratio {er}% (gross {g}%)" if er is not None else "pool not listed on expense-ratio page",
        source_url=url, evidence_label="F / C",
        notes="Assets at 30 June; expense ratios as of 2026-09-30 (timing mismatch)") for name, a, er, g in pools)
    summary = (
        row(sponsor="Fidelity Charitable", ein="110303001", fiscal_year=fy, layer="pool_in_fund",
            item="Asset-weighted pool expense ratio (net), priced pools", assets_usd=fmt(float(priced_assets)),
            rate_bps=bps(w_net / priced_assets), amount_usd=fmt(round(w_net)), weighting="asset_weighted",
            basis="sum(pool assets x net ER) / priced pool assets", source_url=url, evidence_label="C",
            notes=f"Gross-ER basis {bps(w_gross / priced_assets)} bps; unpriced pools ${unpriced:,.0f} excluded"),
        row(sponsor="Fidelity Charitable", ein="110303001", fiscal_year=fy, layer="pool_in_fund",
            item="Asset-weighted pool expense ratio (net), all pools, unpriced at 0 / at 0.93%",
            assets_usd=fmt(float(total)), rate_bps=f"{w_net / total * 1e4:.1f}-{(w_net + hi_unpriced) / total * 1e4:.1f}",
            amount_usd=f"{round(w_net)}-{round(w_net + hi_unpriced)}", weighting="asset_weighted_bounds",
            basis="unpriced Impact Investing and Charitable Cash pools at 0% and at the highest listed ER (0.93%)",
            source_url=url, evidence_label="C", notes=""),
        row(sponsor="Fidelity Charitable", ein="110303001", fiscal_year=fy, layer="pool_in_fund_per_investment_dollar",
            item="Pool in-fund cost per dollar of total investments (CIAP in-fund cost set to 0)",
            assets_usd=fmt(float(FIDELITY_TOTAL_INVESTMENTS[fy])),
            rate_bps=bps(w_net / FIDELITY_TOTAL_INVESTMENTS[fy]), amount_usd=fmt(round(w_net)),
            weighting="lower_bound", basis="pool in-fund $ / audit Total Investments at Fair Value",
            source_url=url, evidence_label="C",
            notes="Lower bound: CIAP mutual-fund, ETF and alternative-fund expenses are inside NAV and not published"),
        row(sponsor="Fidelity Charitable", ein="110303001", fiscal_year=fy, layer="pool_in_fund_per_investment_dollar",
            item="Sensitivity: CIAP mutual funds also at the pool-weighted ER",
            assets_usd=fmt(float(FIDELITY_TOTAL_INVESTMENTS[fy])),
            rate_bps=bps((w_net + (FIDELITY_CIAP_MIX_2025["mutual funds"] if fy == 2025 else 8_777_966_812)
                          * w_net / priced_assets) / FIDELITY_TOTAL_INVESTMENTS[fy]),
            amount_usd="", weighting="sensitivity",
            basis="adds CIAP 'Mutual funds' balance x pool-weighted net ER; alternatives still at 0",
            source_url=FIDELITY_AFS_URL[fy], evidence_label="C / I", notes="Illustrative only"),
    )
    return per_pool + summary


def avg(a, b) -> float | None:
    return (a + b) / 2 if a is not None and b is not None else None


def ciap_rows() -> tuple[dict, ...]:
    def one(fy: int) -> tuple[dict, ...]:
        a = avg(FIDELITY_CIAP.get(fy), FIDELITY_CIAP.get(fy - 1))
        fee = FIDELITY_INV_MGMT_FEES[fy]
        other = FIDELITY_OTHER_EXPENSES.get(fy)
        l24 = {2025: 15_615_744, 2024: 20_670_116}.get(fy)
        base = row(sponsor="Fidelity Charitable", ein="110303001", fiscal_year=fy, layer="ciap_adviser_fee",
                   source_url=FIDELITY_AFS_URL[fy] + (f" ; {XML_URL.format(oid=FIDELITY_990[fy])}" if fy in FIDELITY_990 else ""),
                   evidence_label="F / C")
        out = (
            {**base, "item": "Audit 'Investment management fees' / average CIAP advisor-managed investments",
             "assets_usd": fmt(a), "rate_bps": bps(fee / a) if a else "", "amount_usd": fmt(float(fee)),
             "weighting": "observed_ratio",
             "basis": "Statement of Activities line (= Form 990 line 11f) over mean of 30 June CIAP balances",
             "notes": "Upper bound on the CIAP adviser rate if any pool-level manager fees are in the line; lower "
                      "bound on adviser cost per fee-paying account because no-fee CIAP accounts are in the denominator"},)
        if l24 is not None and a:
            out += ({**base, "item": "Incl. Form 990 line 24 'OTH CHARITABL INV ADVISOR PRGM'",
                     "assets_usd": fmt(a), "rate_bps": bps((fee + l24) / a), "amount_usd": fmt(float(fee + l24)),
                     "weighting": "observed_ratio",
                     "basis": f"11f + line 24 CIAP item ${l24:,.0f}; audit 'Other expenses' ${other:,.0f}",
                     "notes": "Line 24 CIAP item = audit 'Other expenses' (FY2024) or 'Other expenses' less "
                              "'Federal & state tax payments' $5,695,890 (FY2025); nature not described in the audit"},)
        return out
    return tuple(r for fy in (2025, 2024, 2023) for r in one(fy))


def cost_rows(cost: Sequence[Mapping]) -> tuple[dict, ...]:
    want = {"110303001": "2025", "232888152": "2024", "311640316": "2025", "237825575": "2025", "527082731": "2024"}
    names = {"110303001": "Fidelity Charitable", "232888152": "Vanguard Charitable", "311640316": "DAFgiving360",
             "237825575": "National Philanthropic Trust", "527082731": "Morgan Stanley GIFT"}
    sel = tuple(r for r in cost if want.get(r["ein"]) == r["fiscal_year"])
    return tuple(row(sponsor=names[r["ein"]], ein=r["ein"], fiscal_year=r["fiscal_year"], layer="part_ix_operating",
                     item="Part IX operating cost incl. 11f, bps of average total assets",
                     assets_usd=r["total_assets_avg"], rate_bps=f"{float(r['opex_incl_invest_bps_of_total_assets']):.1f}",
                     amount_usd=fmt(num(r["operating_cost"])), weighting="observed_ratio",
                     basis=f"ex-11f {float(r['opex_bps_of_total_assets']):.1f} bps; operating cost = Part IX less lines 1-4",
                     source_url=r["xml_url"], evidence_label="F / C",
                     notes="From data/mission-2026-11-14/sponsor-cost-structure.csv") for r in sel)


def range_rows() -> tuple[dict, ...]:
    return tuple(row(sponsor=s, ein=e, fiscal_year="2026 (ER date)", layer="pool_in_fund",
                     item="Pool expense-ratio range (pool assets not published)", assets_usd="",
                     rate_bps=f"{lo * 100:.1f}-{hi * 100:.1f}", amount_usd="", weighting="bounds_unweighted",
                     basis=basis, source_url=url, evidence_label=lab, notes=date) for s, e, lo, hi, lab, basis, url, date in RANGE_ONLY)


def all_in_rows(cost_r: Sequence[Mapping], fid_pool: Mapping[int, float]) -> tuple[dict, ...]:
    op = {r["ein"]: float(r["rate_bps"]) for r in cost_r}
    rng = {e: (lo * 100, hi * 100) for _, e, lo, hi, *_ in RANGE_ONLY}
    names = {"232888152": "Vanguard Charitable", "311640316": "DAFgiving360", "237825575": "National Philanthropic Trust"}
    fid = row(sponsor="Fidelity Charitable", ein="110303001", fiscal_year=2025, layer="all_in_per_dollar",
              item="Part IX operating incl. 11f + pool in-fund per investment dollar (lower bound)", assets_usd="",
              rate_bps=f"{op['110303001'] + fid_pool[2025]:.1f}", amount_usd="", weighting="sum",
              basis=f"{op['110303001']:.1f} + {fid_pool[2025]:.1f}", source_url=FC_AFS25 + " ; " + FC_COST,
              evidence_label="C", notes="Excludes CIAP in-fund cost and donor-paid adviser fees outside the account")
    others = tuple(row(sponsor=names[e], ein=e, fiscal_year="latest", layer="all_in_per_dollar",
                       item="Part IX operating incl. 11f + pool ER range (unweighted bounds)", assets_usd="",
                       rate_bps=f"{op[e] + rng[e][0]:.1f}-{op[e] + rng[e][1]:.1f}", amount_usd="", weighting="bounds",
                       basis=f"{op[e]:.1f} + [{rng[e][0]:.1f}, {rng[e][1]:.1f}]"
                             + (" ; NPT advisory fee assumed inside 11f" if e == "237825575" else ""),
                       source_url="see pool_in_fund row", evidence_label="C",
                       notes="Bounds only: needs pool assets") for e in names if e in op)
    return (fid,) + others


def income_rows(ex: Mapping[str, Mapping]) -> tuple[dict, ...]:
    def one(label: str, oid: str) -> dict:
        g = ex.get(oid, {})
        a = avg(g.get("assets_boy"), g.get("assets_eoy"))
        l3 = g.get("l3_investment_income")
        tr = (sum(x for x in (l3, g.get("l7d_net_gain"), g.get("xi_5_unrealized")) if x is not None) / a
              if a and l3 is not None else None)
        return row(sponsor=label, ein="", fiscal_year=(g.get("tax_period_end") or "")[:7], layer="investment_income_test",
                   item="Part VIII line 3 investment income / average total assets", assets_usd=fmt(a),
                   rate_bps=bps(l3 / a) if l3 is not None and a else "", amount_usd=fmt(l3), weighting="observed_ratio",
                   basis=(f"11f {fmt(g.get('l11f'))}; 11g {fmt(g.get('l11g'))}; 7a sales {fmt(g.get('l7a_gross_sales_securities'))}; "
                          f"7b cost+sales exp {fmt(g.get('l7b_cost_and_sales_expenses_securities'))}; "
                          f"Sch D XII 4a {fmt(g.get('sd_xii_4a_inv_exp'))}; XII 4b {fmt(g.get('sd_xii_4b_other'))}"),
                   source_url=XML_URL.format(oid=oid), evidence_label="F / C",
                   total_return_proxy_bps=bps(tr),
                   notes="A very low line-3 yield is consistent with account-level fees being netted against income; "
                         "it does not prove it (asset mix and cash drag also matter)")
    return tuple(one(l, o) for l, o in INCOME_TEST)


def ms_gift_rows(ex: Mapping[str, Mapping]) -> tuple[dict, ...]:
    g = ex.get("202503239349300435", {})
    a = avg(g.get("assets_boy"), g.get("assets_eoy"))
    base = dict(sponsor="Morgan Stanley GIFT", ein="527082731", fiscal_year=2024, layer="ms_gift_fee_location",
                source_url=XML_URL.format(oid="202503239349300435") + " ; " + MS_CIRC, evidence_label="C / I")
    adv_cap = a * 0.01 if a else None
    mssb = a * 0.0007 if a else None
    visible = sum(x or 0 for x in (g.get("l11f"),) + tuple(v for d, v in g.get("l24", []) if "COMMISSION" in d.upper()))
    return (
        {**base, "item": "Advisory fee at the 1.00% cap on average total assets", "assets_usd": fmt(a),
         "rate_bps": "100.0", "amount_usd": fmt(round(adv_cap)) if adv_cap else "", "weighting": "ceiling",
         "basis": "circular Schedule C max Morgan Stanley Advisory fee 1.00%", "notes": "Ceiling, not an observed fee"},
        {**base, "item": "Visible advisory-type lines (11f 'Morgan Stanley investment advisor' + line 24 FA commissions)",
         "assets_usd": fmt(a), "rate_bps": bps(visible / a) if a else "", "amount_usd": fmt(visible),
         "weighting": "observed_ratio", "basis": "Part IX", "notes": ""},
        {**base, "item": "MSSB administrative fee at 0.07% (upper bound; tiers lower it on large accounts)",
         "assets_usd": fmt(a), "rate_bps": "7.0", "amount_usd": fmt(round(mssb)) if mssb else "",
         "weighting": "ceiling", "basis": "circular Schedule C MSSB Administrative Fee table",
         "notes": "No Part IX line or Schedule O text matches it"},
        {**base, "item": "Schedule D Part XI/XII reconciling items", "assets_usd": "",
         "rate_bps": "", "amount_usd": fmt(g.get("sd_xii_4a_inv_exp")), "weighting": "observed",
         "basis": f"Part XII 4a {fmt(g.get('sd_xii_4a_inv_exp'))}, 4b {fmt(g.get('sd_xii_4b_other'))}, 2e {fmt(g.get('sd_xii_2e_subtotal'))}",
         "notes": "All zero: whatever the audit nets inside investment return, the 990 nets the same way"},
    )


def verify(verify_dir: str) -> dict:
    texts = " ".join(open(os.path.join(verify_dir, f), encoding="utf-8").read()
                     for f in os.listdir(verify_dir) if f.endswith(".txt"))
    def present(n: int) -> bool:
        return f"{n:,}" in texts
    vals = ([p[1] for p in FIDELITY_POOLS] + [p[2] for p in FIDELITY_POOLS] + list(FIDELITY_CIAP.values())
            + list(FIDELITY_INV_MGMT_FEES.values()) + list(FIDELITY_OTHER_EXPENSES.values())
            + list(FIDELITY_POOL_TOTAL.values()) + list(FIDELITY_TOTAL_INVESTMENTS.values())
            + list(FIDELITY_CIAP_MIX_2025.values()))
    missing = [v for v in vals if not present(v)]
    return {"checked": len(vals), "missing": missing}


FIELDS = ("row_id", "sponsor", "ein", "fiscal_year", "layer", "item", "assets_usd", "rate_bps", "amount_usd",
          "total_return_proxy_bps",
          "weighting", "basis", "source_url", "evidence_label", "retrieved", "notes")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--verify-dir")
    ap.add_argument("--out", default=OUT_CSV)
    a = ap.parse_args(argv)
    ver = verify(a.verify_dir) if a.verify_dir else None
    oids = tuple(dict.fromkeys(o for _, o in INCOME_TEST))
    with ThreadPoolExecutor(max_workers=8) as ex:
        extracts = dict(zip(oids, ex.map(lambda o: fetch_inv(o, a.cache_dir, a.fetch), oids)))
    cost = m990.read_csv(COST_CSV)
    pools = {fy: fidelity_pool_rows(fy) for fy in (2025, 2024)}
    fid_lb = {fy: float(next(r for r in rs if r["weighting"] == "lower_bound")["rate_bps"]) for fy, rs in pools.items()}
    c_rows = cost_rows(cost)
    rows = (pools[2025] + pools[2024] + range_rows() + c_rows + all_in_rows(c_rows, fid_lb) + ciap_rows()
            + ms_gift_rows(extracts) + income_rows(extracts))
    out = tuple({**r, "row_id": f"N{i + 1:03d}", "retrieved": "2026-11-15"} for i, r in enumerate(rows))
    m990.write_csv(a.out, out, FIELDS)
    show = tuple(r for r in out if r["weighting"] not in ("pool",))
    print(json.dumps({"rows": len(out), "verify": ver,
                      "xml_status": {o: e.get("xml_status") for o, e in extracts.items()},
                      "summary": [(r["row_id"], r["sponsor"], r["fiscal_year"], r["item"][:70], r["rate_bps"], r["amount_usd"], r.get("total_return_proxy_bps", ""))
                                  for r in show]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
