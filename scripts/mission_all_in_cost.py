#!/usr/bin/env python3
"""All-in annual donor cost of a DAF across sponsors at three balances (queue item P-ANL-05).

Stdlib only; functional style (inputs are immutable records, every cost is a pure function of
balance, I/O only in main()).

What "all-in" means here (see research/mission-2026-11-14/queue-all-in-cost-dafpay-access.md):
  admin            sponsor administrative / program fee from the published schedule, including any
                   minimum annual fee, other mandatory platform/admin layers (e.g. MS GIFT's MSSB fee),
                   and, for transaction-priced sponsors (Daffy, Endaoment), fees implied by the FLOW
                   ASSUMPTION below.
  investment       expense ratio of (a) the cheapest published pool or portfolio ("low") and (b) the
                   sponsor's default, most popular or typical balanced pool ("typical"). Blank where the
                   sponsor publishes no pool expense (adviser-managed-only programs).
  adviser          the permitted adviser / sub-advisory fee. Uses the sponsor's PUBLISHED CAP where one
                   exists; a mandatory program fee where documented (Edward Jones); otherwise, where an
                   adviser-managed option exists but no cap is published, an ILLUSTRATIVE 1.00%
                   (equal to the three published caps found) clearly flagged as an assumption.
  min-fee effects  whether a minimum annual fee binds at the balance, and the balance below which it binds.

Outputs: data/mission-2026-11-14/all-in-cost-comparison-2026.csv (one row per sponsor x balance).

Usage: python3 scripts/mission_all_in_cost.py [--out PATH]
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Callable, NamedTuple, Optional

ROOT = Path(__file__).resolve().parent.parent
OUT_DEFAULT = ROOT / "data" / "mission-2026-11-14" / "all-in-cost-comparison-2026.csv"
RETRIEVED = "2026-11-14"

BALANCES = (25_000, 250_000, 2_500_000)

# FLOW ASSUMPTION (only affects Daffy's subscription tier and Endaoment's per-transaction fees):
# steady state with annual contributions and annual grants each equal to 20% of the balance.
CONTRIB_SHARE = 0.20
GRANT_SHARE = 0.20

# Illustrative adviser fee where an adviser-managed option exists but no cap is published.
ILLUSTRATIVE_ADVISER_BPS = 100.0

INF = float("inf")


class Src(NamedTuple):
    url: str
    date: str          # date stated on/inside the source, or "undated (live 2026-11-14)"
    status: str        # primary | primary_pdf_ocr | search_index_capture | third_party | repo_prior


class Sponsor(NamedTuple):
    key: str
    sponsor: str
    program: str
    admin_fn: Callable[[float], float]          # annual admin USD as function of balance
    min_fee_usd: Optional[float]                # published minimum annual fee (None = none published)
    first_tier_bps: Optional[float]             # used for min-fee breakeven
    admin_src: Src
    inv_low_bps: Optional[float]
    inv_low_label: str
    inv_typical_bps: Optional[float]
    inv_typical_label: str
    inv_src: Optional[Src]
    adviser_bps: Optional[float]
    adviser_basis: str                          # published_cap | program_fee | illustrative_assumption | not_offered_or_not_found | not_published
    adviser_min_balance: Optional[float]        # balance needed for adviser-managed option (None = n/a / unknown)
    adviser_required: bool                      # adviser layer is part of the standard program
    adviser_src: Optional[Src]
    confidence: str                             # high | medium | low
    assumptions: str
    notes: str


# ---------------------------------------------------------------- fee primitives (pure)

def marginal(tiers: tuple[tuple[float, float, float], ...]) -> Callable[[float], float]:
    """tiers = ((lower, upper, rate_pct), ...) applied marginally."""
    def fee(b: float) -> float:
        return sum(max(0.0, min(b, hi) - lo) * rate / 100.0 for lo, hi, rate in tiers)
    return fee


def first_dollar_band(bands: tuple[tuple[float, float, float], ...]) -> Callable[[float], float]:
    """Flat rate of the band containing the balance, applied to the whole balance (BofA CGF)."""
    def fee(b: float) -> float:
        rate = next(r for lo, hi, r in bands if lo <= b <= hi)
        return b * rate / 100.0
    return fee


def with_minimum(fn: Callable[[float], float], minimum: float) -> Callable[[float], float]:
    return lambda b: max(fn(b), minimum)


def plus(*fns: Callable[[float], float]) -> Callable[[float], float]:
    return lambda b: sum(f(b) for f in fns)


def flat_pct(rate_pct: float) -> Callable[[float], float]:
    return lambda b: b * rate_pct / 100.0


def npt_fee(b: float) -> float:
    """NPT: 0.85% first $250k 'or the minimum monthly fee [$17], whichever is greater', then marginal."""
    first = max(min(b, 250_000) * 0.0085, 17 * 12)
    rest = marginal(((250_000, 500_000, 0.70), (500_000, 1_000_000, 0.60), (1_000_000, 2_500_000, 0.45),
                     (2_500_000, 5_000_000, 0.25), (5_000_000, 10_000_000, 0.15), (10_000_000, INF, 0.10)))(b)
    return first + rest


def daffy_fee(b: float) -> float:
    """Daffy flat monthly membership chosen by average annualized contributions (individual fund)."""
    c = b * CONTRIB_SHARE
    monthly = 3 if c <= 25_000 else 20 if c <= 100_000 else 40
    return monthly * 12.0


def endaoment_fee(b: float) -> float:
    """Endaoment: one-time tiered inbound fee (fill-the-bucket by donation size) + 1.0% grant fee."""
    inbound = marginal(((0, 250_000, 0.50), (250_000, 500_000, 0.40), (500_000, 1_000_000, 0.30),
                        (1_000_000, 10_000_000, 0.20), (10_000_000, 100_000_000, 0.10),
                        (100_000_000, INF, 0.05)))
    return inbound(b * CONTRIB_SHARE) + b * GRANT_SHARE * 0.01


def unknown(_b: float) -> float:
    return float("nan")


# ---------------------------------------------------------------- sources

S = {
    "fid": Src("https://www.fidelitycharitable.org/giving-account/what-it-costs.html", "undated (live 2026-11-14; ©1998-2026; pool data refers to 2026-09-30)", "primary"),
    "fid_ciap": Src("https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/giving-account-guide-financial-advisors.pdf", "undated advisor guide (embedded metadata to 2021; references 2026 tax year)", "primary"),
    "vg_fee": Src("https://www.vanguardcharitable.org/fees-and-expenses", "undated (live 2026-11-14; schedule reviewed annually)", "primary"),
    "vg_inv": Src("https://www.vanguardcharitable.org/investments", "expense ratios last updated 2026-09-30", "primary"),
    "d360_deck": Src("https://www.financialplanningassociation.org/sites/default/files/2024-09/FPA%20of%20MI_DAFGiving360_deck_092724_ver3.pdf", "2024-09 (DAFgiving360 deck, ©2024)", "primary"),
    "d360_fee": Src("https://www.dafgiving360.org/features/fees-and-minimums", "page 403 to automated fetch; search-index capture 2026-11-14", "search_index_capture"),
    "d360_adv": Src("https://www.dafgiving360.org/investment-options-advisor", "page 403; search-index capture 2026-11-14 ('not to exceed 1%')", "search_index_capture"),
    "swtsx": Src("https://www.schwabassetmanagement.com/products/swtsx", "fund page (0.03% total expense ratio; search-index capture)", "search_index_capture"),
    "d360_bal": Src("https://www.dafgiving360.org/public/file/p-9677269", "undated DAFgiving360 PDF (returns to 2020; 403) - search-index capture", "search_index_capture"),
    "npt_guide": Src("https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf", "PDF created 2026-10-15", "primary"),
    "npt_inv": Src("https://www.nptrust.org/investment-descriptions-and-performance-npt/", "NPT FOR IDAP 0926; performance as of 2026-06-30", "primary"),
    "npt_faq": Src("https://www.nptrust.org/?p=206", "undated (live 2026-11-14; ©2026)", "primary"),
    "rcf_am": Src("https://renaissancecharitable.org/advisor-managed-dafs/", "undated (live 2026-11-14)", "primary"),
    "rcf_dd": Src("https://renaissancecharitable.org/donor-directed-dafs/", "undated (live 2026-11-14)", "primary"),
    "ej": Src("https://intercom.help/rengiving/en/articles/11004460-ej-daf-opening-instructions", "undated; page now 404; search-index capture 2026-11-14", "search_index_capture"),
    "aef_3p": Src("https://donoradvisedfunds.com/dafs/american-endowment-foundation-aef/", "third-party listing (©2024); AEF publishes no schedule", "third_party"),
    "aef_mtf": Src("https://advisorwelcome.aefonline.org/maintain-the-fund", "undated (live 2026-11-14)", "primary"),
    "bofa": Src("https://www.bankofamerica.com/content/documents/philanthropic/cgf_fee_schedule.pdf", "fee estimates as of 2024-02-16", "repo_prior"),
    "msgift": Src("https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf", "Donor Circular August 2024 (Schedule C; OCR of image-font PDF)", "primary_pdf_ocr"),
    "gs": Src("https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111", "Program Circular last revised 2008-08 (pre-2021; not used)", "primary"),
    "ncf_fee": Src("https://www.ncfgiving.com/givingfund", "undated (live 2026-11-14; ©2026)", "primary"),
    "ncf_inv": Src("https://site.ncfgiving.com//wp-content/uploads/2026/08/Grow-your-giving-for-greater-impact.pdf", "expense ratios 'Estimate as of July 31, 2026'", "primary"),
    "daffy_fee": Src("https://help.daffy.org/en/articles/6323771-what-are-daffy-s-membership-fees", "updated 2026-08-06", "primary"),
    "daffy_inv": Src("https://www.daffy.org/answers/what-is-the-range-of-the-expense-ratio-for-the-etfs-in-these-portfolios", "JS-rendered; search-index capture (fund data as of 2025-06-13 per related page)", "search_index_capture"),
    "cv": Src("https://pcadafguide.foundationsource.com/how-client-fees-work", "undated (live 2026-11-14)", "primary"),
    "endo_fee": Src("https://docs.endaoment.org/donors/resources/fee-schedule.md", "undated (live 2026-11-14)", "primary"),
    "endo_inv": Src("https://app.shadow.endaoment.org/portfolios/7b59269e-05d0-4a74-837c-44f1249da4da", "search-index capture of portfolio page (0.530% VOO; 0.600% another portfolio)", "search_index_capture"),
    "endo_adv": Src("https://docs.endaoment.org/advisors/resources/fee-schedule.md", "undated (live 2026-11-14)", "primary"),
    "tifin": Src("https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines", "updated 2025-08-12", "primary"),
    "giveclear_cust": Src("https://irp.cdn-website.com/5c4108df/files/uploaded/DAF+Program+Guidelines-d1858d87.pdf", "V08.25.2025", "primary"),
    "sff": Src("https://sff.org/wp-content/uploads/2026/05/2026-Advisor-Guide-1.pdf", "2026 Advisor Guide (uploaded 2026-05)", "primary"),
}


# ---------------------------------------------------------------- sponsor inputs

FC_TIERS = ((0, 500_000, 0.60), (500_000, 1_000_000, 0.30), (1_000_000, 2_500_000, 0.20), (2_500_000, 5_000_000, 0.15))

SPONSORS: tuple[Sponsor, ...] = (
    Sponsor("fidelity", "Fidelity Charitable", "Giving Account (pools; CIAP adviser option)",
            with_minimum(marginal(FC_TIERS), 100), 100, 60, S["fid"],
            1.5, "Total Market Index Pool 0.015%", 55.0, "Asset Allocation 60% Equity Pool 0.55%", S["fid"],
            ILLUSTRATIVE_ADVISER_BPS, "illustrative_assumption", None, False, S["fid_ciap"],
            "high",
            "Adviser fee: CIAP lets advisers 'charge your customary advisor fee'; no cap published, so 1.00% is illustrative. CIAP minimum 'varies by firm'.",
            "Tier 4 is 'Next $2,499,999' to $5m; balances >= $5m priced by phone. Asset-allocation pools 0.45-0.56%; index pools 0.015-0.035%."),
    Sponsor("vanguard", "Vanguard Charitable", "Premier pricing (most > $1m accounts after 3 months)",
            marginal(((0, 500_000, 0.60), (500_000, 1_000_000, 0.30), (1_000_000, 5_000_000, 0.12),
                      (5_000_000, 15_000_000, 0.10), (15_000_000, 30_000_000, 0.08), (30_000_000, 100_000_000, 0.05))),
            None, 60, S["vg_fee"],
            1.0, "Income / Conservative Growth / Balanced Index 0.01%", 2.0, "Moderate Growth (Portfolio Solutions) 0.02%", S["vg_inv"],
            None, "not_offered_or_not_found", None, False, None,
            "high",
            "Premier schedule assumed at $2.5m; a Standard account over $1m pays 0.30% (page footnote), which would raise the $2.5m admin fee.",
            "No minimum annual admin fee, but 'Accounts having a balance below $25,000 may be subject to an annual maintenance fee of $250' (investments page). Vanguard Charitable 'does not itself charge investment fees'. No adviser-fee program found on public pages."),
    Sponsor("dafgiving360", "DAFgiving360 (formerly Schwab Charitable)", "Core account (pools); professionally managed option",
            marginal(FC_TIERS + ((5_000_000, 10_000_000, 0.13), (10_000_000, 15_000_000, 0.12), (15_000_000, INF, 0.10))),
            None, 60, S["d360_deck"],
            3.0, "Total Market Equity Index Pool (SWTSX 0.03%)", 65.0, "Balanced Pool (JBALX ~0.65%, search-index capture)", S["swtsx"],
            100.0, "published_cap", 100_000, False, S["d360_adv"],
            "medium",
            "Underlying funds changed September 2026 (per DAFgiving360 advisor page snippet); pool->fund mapping is from the 2024 deck. JBALX 0.65% is from an undated DAFgiving360 PDF seen only in search-index.",
            "Core admin 0.60% is 'collected as part of the operating expenses of the investment pools' with a quarterly rebate above $500k, so it is modelled separately from underlying fund expense (no double count). 2024 deck: '$0+ - no annual fee or minimum'; professionally managed $100k+; adviser fee 'not to exceed 1%'. Live dafgiving360.org pages return HTTP 403."),
    Sponsor("npt", "National Philanthropic Trust", "Pooled DAF (index or active model portfolios)",
            npt_fee, 204, 85, S["npt_guide"],
            17.0, "Index Fund Moderate Portfolio 0.07% + 0.10% NPT advisory fee", 61.0, "Actively Managed Moderate Portfolio 0.51% + 0.10% advisory fee", S["npt_inv"],
            ILLUSTRATIVE_ADVISER_BPS, "illustrative_assumption", None, False, S["npt_faq"],
            "high",
            "Adviser fee: FAQ lists 'a fee to financial advisors' for some accounts; no rate published, so 1.00% is illustrative. Segregated-account minimum not stated.",
            "Minimum monthly CAF $17 ($204/yr). Index portfolios also bear trading costs up to 4 cents/share. Guide rate examples: $750k 0.72%, $1.5m 0.61%."),
    Sponsor("rcf_advisor", "Renaissance Charitable Foundation (Ren)", "Advisor-managed DAF",
            with_minimum(marginal(((0, 500_000, 0.65), (500_000, 1_000_000, 0.35), (1_000_000, 2_500_000, 0.25), (2_500_000, 5_000_000, 0.20))), 250),
            250, 65, S["rcf_am"],
            None, "not published (custody-neutral SMAs)", None, "not published", None,
            ILLUSTRATIVE_ADVISER_BPS, "illustrative_assumption", 0, True, S["rcf_am"],
            "high",
            "Adviser fee not published on the RCF page; 1.00% illustrative. Fund expenses depend on the adviser's portfolio.",
            "Same schedule on Ren Direct (repo E03). > $5m: 'Contact us'."),
    Sponsor("rcf_donor", "Renaissance Charitable Foundation (Ren)", "Donor-directed DAF",
            with_minimum(marginal(((0, 500_000, 0.60), (500_000, 1_000_000, 0.30), (1_000_000, 2_500_000, 0.20), (2_500_000, INF, 0.15))), 250),
            250, 60, S["rcf_dd"],
            None, "not published", None, "not published", None,
            None, "not_offered_or_not_found", None, False, None,
            "high", "", "Labelled 'Total Program Bps'; > $5m quote on request."),
    Sponsor("edward_jones", "Edward Jones Charitable Gift Fund (Ren / RCF program)", "Advisor-serviced DAF",
            with_minimum(marginal(((0, 500_000, 0.60), (500_000, 1_000_000, 0.30), (1_000_000, 2_500_000, 0.20), (2_500_000, INF, 0.15))), 200),
            200, 60, S["ej"],
            None, "not published", None, "not published", None,
            70.0, "program_fee", 10_000, True, S["ej"],
            "low",
            "Only the starting rate (60 bps, 'tiers down') and $200 minimum are documented; breakpoints ASSUMED equal to RCF donor-directed (60/30/20/15). Source page now 404 (search-index capture).",
            "Separate 0.70% Program Fee that 'goes to the advisor's standard payout'. Opening minimum $10,000 (Edward Jones DAF brochure also says $10,000)."),
    Sponsor("aef", "American Endowment Foundation", "Adviser-managed DAF (AEF administers; adviser invests)",
            marginal(((0, 500_000, 0.70), (500_000, 1_000_000, 0.35), (1_000_000, 2_500_000, 0.25),
                      (2_500_000, 15_000_000, 0.15), (15_000_000, 30_000_000, 0.10))),
            None, 70, S["aef_3p"],
            None, "not published (adviser portfolio)", None, "not published", None,
            ILLUSTRATIVE_ADVISER_BPS, "illustrative_assumption", 0, True, S["aef_mtf"],
            "low",
            "AEF publishes no schedule; tiers are a third-party listing (©2024). Adviser fee not published; 1.00% illustrative.",
            "Fees assessed quarterly from a ~1% liquidity account (AEF Maintain the Fund page). Third-party listing: $25,000 initial, $10,000 minimum balance."),
    Sponsor("bofa", "Bank of America Charitable Gift Fund", "Donor-advised account",
            first_dollar_band(((0, 100_000, 0.90), (100_000.01, 500_000, 0.75), (500_000.01, 1_000_000, 0.50),
                               (1_000_000.01, 2_500_000, 0.35), (2_500_000.01, 5_000_000, 0.25), (5_000_000.01, 10_000_000, 0.15),
                               (10_000_000.01, 20_000_000, 0.12), (20_000_000.01, 50_000_000, 0.10))),
            None, 90, S["bofa"],
            17.0, "Passive objective, low end (fund 0.05% + 0.12% BofA investment management)", 21.0, "Passive objective, high end", S["bofa"],
            None, "not_offered_or_not_found", None, False, None,
            "medium",
            "Uses the repo's reading of the CGF fee PDF (estimates as of 2024-02-16; not re-read 2026-11-14). The 0.12% Private Bank management fee is inside the investment estimate.",
            "NOT marginal: 'flat rate applied back to the first dollar'. Sustainable objectives 0.20-0.29%."),
    Sponsor("msgift", "Morgan Stanley GIFT", "Select UMA / Portfolio Management program accounts",
            plus(with_minimum(marginal(((0, 2_000_000, 0.27), (2_000_000, 5_000_000, 0.20), (5_000_000, 10_000_000, 0.15),
                                        (10_000_000, 25_000_000, 0.13), (25_000_000, 50_000_000, 0.11))), 100),
                 flat_pct(0.07), flat_pct(0.03)),
            100, 27, S["msgift"],
            None, "not published (mutual fund/ETF expenses 'vary')", None, "not published", None,
            100.0, "published_cap", 25_000, True, S["msgift"],
            "medium",
            "Charitable Administrative Fee taken at its stated MAXIMUM 0.03%. Fund/SMA expenses excluded (not published). Third-party administrator (Ren) minimum $100 applies to the 0.27% tier only.",
            "Three admin layers: third-party administrator 0.27% (min $100), MSSB administrative fee 0.07%, charitable admin fee max 0.03%. Max Morgan Stanley Advisory fee 1.00% (shared with the Financial Advisor). $25,000 minimum for Select UMA / PM accounts."),
    Sponsor("gs", "Goldman Sachs Philanthropy Fund (GS DAF for Wealth Management)", "Donor-advised account",
            unknown, None, None, S["gs"],
            None, "not published", None, "not published", None,
            None, "not_published", None, True, None,
            "low", "No 2021+ fee schedule public; the only circular is dated 2008 and is not used (recency rule).",
            "CY2024 990 shows GS Trust Co $14.6m and GS & Co $8.1m paid for investment/advisory and technology (repo bank-program-terms-2026.csv)."),
    Sponsor("ncf", "National Christian Foundation", "Giving Fund (core pools; SMA option)",
            with_minimum(marginal(((0, 500_000, 0.90), (500_000, 1_000_000, 0.70), (1_000_000, 2_500_000, 0.50), (2_500_000, 5_000_000, 0.35),
                                   (5_000_000, 10_000_000, 0.30), (10_000_000, 20_000_000, 0.25), (20_000_000, 35_000_000, 0.20),
                                   (35_000_000, 50_000_000, 0.15), (50_000_000, 75_000_000, 0.10), (75_000_000, 100_000_000, 0.05))), 360),
            360, 90, S["ncf_fee"],
            50.0, "Stable Capital Pool 0.50% (cheapest core pool)", 55.0, "Balanced Growth Pool 0.55%", S["ncf_inv"],
            ILLUSTRATIVE_ADVISER_BPS, "illustrative_assumption", 300_000, False, S["ncf_inv"],
            "high",
            "SMA adviser fee not published; 1.00% illustrative (SMA minimum $300k; 5% must stay in cash).",
            "Ministry support fee min $30/month ($360/yr). Pool expense ratios are 'net of NCF investment oversight fee'; NCF says no separate investment management fee."),
    Sponsor("daffy", "Daffy Charitable Fund", "Individual fund (membership pricing)",
            daffy_fee, 36, None, S["daffy_fee"],
            13.0, "ETF portfolios 0.13% (low end of stated range)", 16.0, "ETF portfolios 0.16% (high end)", S["daffy_inv"],
            None, "not_offered_or_not_found", None, False, None,
            "medium",
            "FLOW ASSUMPTION: annual contributions = 20% of balance pick the tier (Contributor $3/mo, Benefactor $20/mo, Philanthropist $40/mo).",
            "Daffy charges no investment management fee; bond portfolios 0.04-0.05%, cash 0.00%."),
    Sponsor("charityvest", "Charityvest (Foundation Source DAF technology)", "Invested account",
            with_minimum(marginal(((0, 500_000, 0.60), (500_000, 1_000_000, 0.30), (1_000_000, 2_500_000, 0.20),
                                   (2_500_000, 5_000_000, 0.15), (5_000_000, 10_000_000, 0.10))), 100),
            100, 60, S["cv"],
            5.0, "Built-in fund fees, low end 0.05%", 11.0, "Built-in fund fees, high end 0.11%", S["cv"],
            None, "not_offered_or_not_found", None, False, None,
            "medium",
            "Guide is the Foundation Source PCA program guide naming Charityvest as sponsor; assumed to match the retail Charityvest invested account.",
            "Same page also says admin fee 'starting at 45bps' / 'up to 45bps' (unreconciled); the 60 bps tier table is used. Cash accounts: no admin fee."),
    Sponsor("endaoment", "Endaoment", "Endaoment App fund (transaction pricing)",
            endaoment_fee, None, None, S["endo_fee"],
            53.0, "VOO portfolio all-in 0.530% (search-index capture)", 60.0, "another traditional portfolio 0.600% (search-index capture)", S["endo_inv"],
            ILLUSTRATIVE_ADVISER_BPS, "illustrative_assumption", 0, False, S["endo_adv"],
            "medium",
            "FLOW ASSUMPTION: one contribution per year = 20% of balance (tiered inbound fee) and grants = 20% of balance (1.0% fee). Advisor-managed portfolio fee 'separately disclosed'; 1.00% illustrative.",
            "No annual or recurring Endaoment fee; impact/crypto portfolios $0 Endaoment fee; traditional portfolios carry the custodian/brokerage expense ratio shown in-app."),
    Sponsor("tifin_giveclear", "TIFIN Give (GiveClear Foundation sponsor)", "TIFIN Give DAF program",
            marginal(((0, 1_000_000, 0.60), (1_000_000, INF, 0.20))), None, 60, S["tifin"],
            None, "not published (investment-related expenses assessed from account)", None, "not published", None,
            100.0, "published_cap", 0, True, S["tifin"],
            "high",
            "Sub-advisory fee 'set by the Advisor ... may not exceed 1%'. Pool/fund expenses not published.",
            "GiveClear 'Customer DAF' white-label guidelines (V08.25.2025) use 0.60% first $1m / 0.20% next $1.5m / 0.10% above $2.5m with the same 1.0% cap; TIFIN's 2025 ADV lists entity-level 30+10 bps service/management fees that are NOT added here (repo warning)."),
    Sponsor("sff", "San Francisco Foundation (large community foundation)", "Standard DAF (pooled)",
            marginal(((0, 3_000_000, 1.00), (3_000_000, 10_000_000, 0.75), (10_000_000, 25_000_000, 0.50), (25_000_000, 50_000_000, 0.25))),
            None, 100, S["sff"],
            24.0, "Short-Term Pool 0.13% + 0.11% foundation investment admin", 113.0, "Long-Term Pool 1.02% (low end of 1.02-1.10%) + 0.11%", S["sff"],
            ILLUSTRATIVE_ADVISER_BPS, "illustrative_assumption", 1_000_000, False, S["sff"],
            "high",
            "Separately managed funds from $1m with an outside adviser; adviser fee not published, 1.00% illustrative. Pool fees exclude incentive fees.",
            "Minimum to start $10,000. Long-Term Pool holds private equity, venture capital and hedge funds."),
)


# ---------------------------------------------------------------- row computation (pure)

def r2(x: Optional[float]) -> str:
    return "" if x is None or x != x else f"{x:.2f}"


def bps(usd: Optional[float], b: float) -> str:
    return "" if usd is None or usd != usd else f"{usd / b * 10_000:.1f}"


def usd_of(bp: Optional[float], b: float) -> Optional[float]:
    return None if bp is None else b * bp / 10_000.0


def add(*xs: Optional[float]) -> Optional[float]:
    return None if any(x is None or x != x for x in xs) else sum(xs)  # type: ignore[arg-type]


def breakeven(s: Sponsor) -> Optional[float]:
    return None if s.min_fee_usd is None or not s.first_tier_bps else s.min_fee_usd / (s.first_tier_bps / 10_000.0)


def min_binding(s: Sponsor, b: float) -> str:
    be = breakeven(s)
    if s.key == "vanguard":
        return "no (a $250 maintenance fee may apply below $25,000)"
    if s.key == "daffy":
        return "n/a (flat membership)"
    return "" if be is None else ("yes" if b < be else "no")


def adviser_eligible(s: Sponsor, b: float) -> str:
    if s.adviser_bps is None:
        return "n/a"
    if s.adviser_min_balance is None:
        return "unknown (minimum not published)"
    return "yes" if b >= s.adviser_min_balance else "no"


def row(s: Sponsor, b: float) -> dict[str, str]:
    admin = s.admin_fn(b)
    admin = None if admin != admin else admin
    inv_lo, inv_ty = usd_of(s.inv_low_bps, b), usd_of(s.inv_typical_bps, b)
    adv = usd_of(s.adviser_bps, b)
    flow = "yes" if s.key in ("daffy", "endaoment") else "no"
    return {
        "sponsor": s.sponsor,
        "program": s.program,
        "balance_usd": f"{b:.0f}",
        "admin_fee_usd": r2(admin),
        "admin_fee_bps": bps(admin, b),
        "min_annual_fee_usd": r2(s.min_fee_usd),
        "min_fee_binding_at_balance": min_binding(s, b),
        "min_fee_breakeven_balance_usd": r2(breakeven(s)),
        "inv_low_bps": r2(s.inv_low_bps),
        "inv_low_option": s.inv_low_label,
        "inv_low_usd": r2(inv_lo),
        "inv_typical_bps": r2(s.inv_typical_bps),
        "inv_typical_option": s.inv_typical_label,
        "inv_typical_usd": r2(inv_ty),
        "all_in_low_usd": r2(add(admin, inv_lo)),
        "all_in_low_bps": bps(add(admin, inv_lo), b),
        "all_in_typical_usd": r2(add(admin, inv_ty)),
        "all_in_typical_bps": bps(add(admin, inv_ty), b),
        "adviser_fee_bps": r2(s.adviser_bps),
        "adviser_fee_basis": s.adviser_basis,
        "adviser_layer_standard": "yes" if s.adviser_required else "no",
        "adviser_option_eligible_at_balance": adviser_eligible(s, b),
        "adviser_fee_usd": r2(adv),
        "all_in_with_adviser_excl_fund_exp_usd": r2(add(admin, adv)),
        "all_in_with_adviser_excl_fund_exp_bps": bps(add(admin, adv), b),
        "all_in_with_adviser_typical_usd": r2(add(admin, adv, inv_ty)),
        "all_in_with_adviser_typical_bps": bps(add(admin, adv, inv_ty), b),
        "flow_assumption_used": f"contributions {CONTRIB_SHARE:.0%} and grants {GRANT_SHARE:.0%} of balance" if flow == "yes" else "no",
        "admin_source_url": s.admin_src.url,
        "admin_source_date": s.admin_src.date,
        "admin_source_status": s.admin_src.status,
        "inv_source_url": s.inv_src.url if s.inv_src else "",
        "inv_source_date": s.inv_src.date if s.inv_src else "",
        "inv_source_status": s.inv_src.status if s.inv_src else "",
        "adviser_source_url": s.adviser_src.url if s.adviser_src else "",
        "adviser_source_date": s.adviser_src.date if s.adviser_src else "",
        "adviser_source_status": s.adviser_src.status if s.adviser_src else "",
        "retrieved": RETRIEVED,
        "confidence": s.confidence,
        "assumptions": s.assumptions,
        "notes": s.notes,
    }


def build_rows(sponsors: tuple[Sponsor, ...], balances: tuple[int, ...]) -> list[dict[str, str]]:
    return [row(s, float(b)) for s in sponsors for b in balances]


def summary(rows: list[dict[str, str]]) -> str:
    def line(r: dict[str, str]) -> str:
        return (f"{r['sponsor'][:38]:38} {r['program'][:22]:22} {int(r['balance_usd']):>9,} "
                f"admin {r['admin_fee_bps'] or '-':>6} low {r['all_in_low_bps'] or '-':>6} typ {r['all_in_typical_bps'] or '-':>6} "
                f"adv {r['all_in_with_adviser_excl_fund_exp_bps'] or '-':>6} min {r['min_fee_binding_at_balance'][:3]}")
    return "\n".join(map(line, rows))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = ap.parse_args()
    rows = build_rows(SPONSORS, BALANCES)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)
    print(summary(rows))
    print(f"\nwrote {len(rows)} rows ({len(SPONSORS)} sponsor programs x {len(BALANCES)} balances) -> {args.out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
