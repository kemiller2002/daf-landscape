#!/usr/bin/env python3
"""P-B4142-04: OBBBA tax-page audit of sponsors ranked 11-25 (FY2024 DAF assets) and of the
Fidelity Charitable "Tools and calculators" page.

Usage:
  python3 -I scripts/mission_tax_page_audit_11_25.py .            # print JSON report
  python3 -I scripts/mission_tax_page_audit_11_25.py . --write    # also write the audit CSV

Stdlib only; pure functions; file I/O only in main(). NOT TAX ADVICE.

What it does
- Ports the two Fidelity Charitable calculators read on 2026-11-20 from
  www.fidelitycharitable.org/etc.clientlibs/fidelitycharitable/clientlibs/clientlib-site.lc-5e5c8d29c69fa8948eceeecc3a5eb7fc-lc.min.js
  (C(): g/v/b tax-savings formulas and T() result-page routing; the securities calculator's addListener()).
  Constants are from the calculator page's hidden inputs (std-married 32200) and select options.
- Runs the repo's profiles H1-H4 (scripts/mission_tax_scenarios.py PROFILES) through each port and compares
  with the repo's statute results (data/mission-2026-11-14/donor-tax-scenarios-2026.csv).
- Recomputes every worked tax example found on the sponsor pages, using the repo engine
  (mission_tax_scenarios.year_tax / run_years) where the example needs a full computation.
- Builds the audit CSV: one row per calculator x profile, per worked example, per tested statement,
  plus one coverage row per sponsor ranked 11-25.
The 2026 law is taken as the repo describes it (donor-tax-parameters-2026.csv; b41n18-02 for the
corporate floor): 0.5% floor (sec. 170(b)(1)(I)); 2/37 reduction (sec. 68) = 35% value cap for the top
bracket; sec. 170(p) $1,000/$2,000 for non-itemizers, cash only, not DAFs; corporate 1% floor
(sec. 170(b)(2)(A)(i)).
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from functools import reduce
from pathlib import Path
from typing import Dict, List, Tuple

ACCESSED = "2026-11-20"
OUT_CSV = "data/mission-2026-11-14/tax-page-audit-11-25-2026-11-20.csv"
SCEN_CSV = "data/mission-2026-11-14/donor-tax-scenarios-2026.csv"
LEAGUE_CSV = "data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv"

FLOOR = 0.005
SEC68 = 2 / 37
STD_MFJ_FIDELITY = 32200       # calculator hidden input id="std-married"
CORP_FLOOR = 0.01


def load_engine(root: Path):
    """Import the repo tax engine (constants + pure functions only; its main() is not run)."""
    spec = importlib.util.spec_from_file_location("mts", root / "scripts" / "mission_tax_scenarios.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------
# Ports of the Fidelity Charitable calculators (faithful to the JS; JS Math.floor kept)
# ------------------------------------------------------------------------------------------------

def fidelity_tax_savings_calc(rate: float, contribution: float, other_itemized: float,
                              std: float = STD_MFJ_FIDELITY) -> Dict[str, object]:
    """C(): g=floor((e+t-p)*m), v=floor((2e+t-p)*m), b=floor((3e+t-p)*m); T(): page routing."""
    e, t, p, m = contribution, other_itemized, std, rate
    g = math.floor((e + t - p) * m)
    v = math.floor((2 * e + t - p) * m)
    b = math.floor((3 * e + t - p) * m)
    page = ("r1" if (g <= 0 and v <= 0) or b <= 0 else
            "r2" if g <= 0 and v > 0 and b > 0 else
            "r4" if t > p else
            "r3" if g > 0 else "none")
    return {"first_year": g, "second_year": v, "third_year": b, "result_page": page}


def fidelity_securities_calc(fmv: float, basis: float, rate: float, cg_rate: float) -> Dict[str, float]:
    """securities-donation-calculator addListener(): n=FMV*rate; c=gain*cg; u=FMV-c; f=(FMV-c)*rate-c; h=n-f."""
    gain = fmv - basis if fmv - basis > 0 else 0.0
    n = fmv * rate
    c = gain * cg_rate
    u = fmv - c
    f = (fmv - c) * rate - c
    return {"contribute_tax_saving": n, "cg_tax_if_sold": c, "sell_deduction": u,
            "sell_net_tax_saving": f, "extra_tax_saving_contribute": n - f, "charity_extra": fmv - u}


# ------------------------------------------------------------------------------------------------
# Statute helpers (2026 law as the repo states it)
# ------------------------------------------------------------------------------------------------

def floor_amt(contribution_base: float) -> float:
    return FLOOR * contribution_base


def top_bracket_value(gift: float, rate: float = 0.37) -> float:
    """Simple per-dollar value used by sponsor examples: rate x (1 - 2/37) = 35 cents for 37%."""
    return gift * rate * (1 - SEC68)


def corporate_deductible(gifts: float, taxable_income: float) -> float:
    """sec. 170(b)(2)(A): deductible only to the extent above 1% and not above 10% of taxable income."""
    return max(0.0, min(gifts, 0.10 * taxable_income) - CORP_FLOOR * taxable_income)


def corporate_cliff_reading(gifts: float, taxable_income: float) -> float:
    """Reading in which giving 'at least 1%' unlocks a deduction for the whole gift (not the law)."""
    return min(gifts, 0.10 * taxable_income) if gifts >= CORP_FLOOR * taxable_income else 0.0


def repo_rows(root: Path) -> Dict[str, Dict[str, str]]:
    with open(root / SCEN_CSV, newline="") as fh:
        return {r["scenario_id"]: r for r in csv.DictReader(fh) if r["row"] == "total"}


def engine_profile_totals(eng, pid: str, wages: float, other: float, gift: float, horizon: int,
                          vehicle: str = "daf", asset: str = "cash") -> Dict[str, float]:
    """Repo engine: total 3-year tax saving vs no gift for annual and bunched schedules."""
    pr = eng.Profile(pid, pid, wages, other, gift, horizon, 0, False, 0.20)
    base = sum(yo.total_tax for yo in eng.baseline(pr, other))
    def saving(gifts: Tuple[float, ...]) -> float:
        return base - sum(yo.total_tax for _, yo in eng.run_years(pr, vehicle, asset, gifts, 0.20, other))
    sched = eng.schedules(pr)
    return {"annual": saving(sched["annual"]), "bunched": saving(sched["bunched_y1"])}


def bofa_business_sale(eng) -> Dict[str, float]:
    """BofA Private Bank example: $30M zero-basis business, $10M gift; stated assumptions only
    (no other income stated; seller not subject to NIIT -> regular tax only; floor then sec. 68)."""
    def one(ltcg: float, gift: float, cat: str) -> float:
        yo = eng.year_tax(eng.YearIn(2026, 0.0, ltcg, 0.0, gift, cat, 0.0, ()))
        return yo.regular_tax
    post = one(30_000_000, 10_000_000, "G")     # sell, then give $10M cash to a public charity/DAF
    pre = one(20_000_000, 10_000_000, "C")      # give 1/3 of the business (capital gain property) first
    return {"post_sale_tax": post, "pre_sale_tax": pre, "saving": post - pre,
            "gross_cg_tax_post": 0.20 * 30_000_000, "gross_cg_tax_pre": 0.20 * 20_000_000}


def statute_value_itemized_vs_std(eng, wages: float, ltcg: float, other: float, gift: float,
                                  cat: str = "G") -> float:
    """Tax with standard deduction and no gift minus tax itemizing with the gift (one year, repo engine)."""
    agi = wages + ltcg
    std_tax = eng.regular_tax(agi - eng.P["std_deduction_mfj"], ltcg) + eng.niit(agi, ltcg)
    yo = eng.year_tax(eng.YearIn(2026, wages, ltcg, other, gift, cat, 0.0, ()))
    return std_tax - yo.total_tax


# ------------------------------------------------------------------------------------------------
# Calculator x profile rows
# ------------------------------------------------------------------------------------------------

USER_RATE = {"H1": 0.12, "H2": 0.24, "H3": 0.37, "H4": 0.37}   # marginal rate a user would select [I]
USER_CG = {"H1": 0.15, "H2": 0.15, "H3": 0.20, "H4": 0.20}     # calculator offers only 15% and 20%


def calculator_rows(eng, rep: Dict[str, Dict[str, str]]) -> List[Dict[str, object]]:
    url_tax = "https://www.fidelitycharitable.org/tools/charitable-tax-savings-calculator.html"
    url_sec = "https://www.fidelitycharitable.org/tools/securities-donation-calculator.html"
    def tax_row(pr) -> Dict[str, object]:
        pid, r = pr.pid, USER_RATE[pr.pid]
        out = fidelity_tax_savings_calc(r, pr.gift_per_year, pr.other_itemized)
        if pid == "H4":
            repo = float(rep["H4|cash|daf|oneoff_y1"]["tax_saving_vs_no_gift"])
            stmt = statute_value_itemized_vs_std(eng, pr.wages, pr.event_ltcg_y1, pr.other_itemized, pr.gift_per_year)
            return {"pid": pid, "out": out, "stated": out["first_year"],
                    "recomputed": round(stmt, 2),
                    "basis": "calc first-year figure (page " + out["result_page"] + ") vs repo engine one-year value of "
                             "itemizing (gift + other) over the standard deduction; repo gift-only saving over 2026-31 = "
                             f"{repo:,.0f}"}
        ann = float(rep[f"{pid}|cash|daf|annual"]["tax_saving_vs_no_gift"])
        bun = float(rep[f"{pid}|cash|daf|bunched_y1"]["tax_saving_vs_no_gift"])
        direct = float(rep[f"{pid}|cash|direct|annual"]["tax_saving_vs_no_gift"])
        page = out["result_page"]
        shown = {"r1": "no savings figure; text: contributions 'may not significantly reduce your tax liability'",
                 "r2": f"3-yr bunched saving shown {out['third_year']:,}",
                 "r3": f"this-year saving {out['first_year']:,}; 3-yr bunched {out['third_year']:,}",
                 "r4": f"this-year 'itemized deductions' saving {out['first_year']:,}"}[page]
        stated = 0 if page == "r1" else (out["third_year"] if page in ("r2", "r3") else out["first_year"])
        recomputed = (direct if page == "r1" else bun if page in ("r2", "r3")
                      else round(statute_value_itemized_vs_std(eng, pr.wages, 0.0, pr.other_itemized, pr.gift_per_year), 2))
        return {"pid": pid, "out": out, "stated": stated, "recomputed": recomputed,
                "basis": f"page {page}: {shown}; repo 3-yr DAF annual {ann:,.0f}, DAF bunched {bun:,.0f}, "
                         f"direct cash annual (sec. 170(p)) {direct:,.0f}"}
    def sec_row(pr) -> Dict[str, object]:
        pid = pr.pid
        fmv = pr.gift_per_year
        out = fidelity_securities_calc(fmv, fmv * pr.basis_fraction, USER_RATE[pid], USER_CG[pid])
        timing = "oneoff_y1" if pr.oneoff else "annual"
        years = 1 if pr.oneoff else pr.horizon
        repo = float(rep[f"{pid}|stock_in_kind|daf|{timing}"]["stock_in_kind_saving_minus_sell_then_give"])
        return {"pid": pid, "out": out, "stated": round(out["extra_tax_saving_contribute"] * years, 2),
                "recomputed": repo,
                "basis": f"calc 'reduce your taxes by an extra' x {years} yr(s) (FMV {fmv:,.0f}, basis 20%, rate "
                         f"{USER_RATE[pid]:.0%}, CG {USER_CG[pid]:.0%}) vs repo stock-in-kind minus sell-then-give (DAF)"}
    def to_csv(kind: str, url: str, d: Dict[str, object]) -> Dict[str, object]:
        diff = float(d["stated"]) - float(d["recomputed"])
        cls = "outdated (pre-OBBBA)"
        if kind == "sec" and d["pid"] == "H1":
            cls = "ambiguous"
        if kind == "tax" and d["pid"] == "H1":
            cls = "outdated (pre-OBBBA)"
        return {"item_type": "calculator", "page_url": url,
                "item": ("Charitable Giving Tax Savings Calculator" if kind == "tax" else "Appreciated Assets Donation Calculator"),
                "profile_or_inputs": d["pid"], "stated_value": d["stated"], "recomputed_value": d["recomputed"],
                "difference": round(diff, 2), "basis": d["basis"], "classification": cls}
    tax = [to_csv("tax", url_tax, tax_row(p)) for p in eng.PROFILES]
    sec = [to_csv("sec", url_sec, sec_row(p)) for p in eng.PROFILES]
    return tax + sec


# ------------------------------------------------------------------------------------------------
# Worked examples and statements (stated figures as quoted; recomputation under the page's assumptions)
# ------------------------------------------------------------------------------------------------

def worked_examples(eng) -> List[Dict[str, object]]:
    ia = engine_profile_totals(eng, "IA1", 1_000_000, 40_000, 100_000, 3)
    bofa = bofa_business_sale(eng)
    lou_gain = 100_000 - 8_000
    return [
        {"id": "GKCCF-EX1", "stated": 3500, "recomputed": top_bracket_value(10_000), "cls": "correct",
         "inputs": "$10,000 gift, 37% bracket"},
        {"id": "GH-EX1", "stated": 3500, "recomputed": top_bracket_value(10_000), "cls": "correct",
         "inputs": "$10,000 gift, 37% bracket (same article on greaterhorizons.org)"},
        {"id": "GKCCF-EX2", "stated": 2500, "recomputed": floor_amt(500_000), "cls": "correct", "inputs": "AGI $500,000"},
        {"id": "GH-EX2", "stated": 2500, "recomputed": floor_amt(500_000), "cls": "correct", "inputs": "AGI $500,000"},
        {"id": "COL-EX1", "stated": 5000, "recomputed": floor_amt(1_000_000), "cls": "correct", "inputs": "AGI $1,000,000"},
        {"id": "IA-FAQ1", "stated": 5000, "recomputed": floor_amt(1_000_000), "cls": "correct", "inputs": "AGI $1,000,000"},
        {"id": "IA-EX1a", "stated": 10000, "recomputed": 3 * floor_amt(1_000_000) - floor_amt(1_000_000), "cls": "correct",
         "inputs": "AGI $1M/yr; $100k/yr x3 vs $300k once: extra deductible giving"},
        {"id": "IA-EX1b", "stated": 3500, "recomputed": round(ia["bunched"] - ia["annual"], 2), "cls": "ambiguous",
         "inputs": "same; 'worth up to about $3,500'; repo engine with other itemized $40k (repo H3 value; not stated on page)"},
        {"id": "IA-EX2", "stated": 3_100_000, "recomputed": 4_000_000 - (4_000_000 - 200_000) * (0.20 + 0.038), "cls": "correct",
         "inputs": "$4M stock, $200k basis, AGI $15M; sold first at 20% + 3.8% NIIT"},
        {"id": "BOFA-EX1", "stated": 50_000, "recomputed": corporate_deductible(150_000, 10_000_000), "cls": "correct",
         "inputs": "corporation, taxable income $10M, gifts $150k"},
        {"id": "BOFA-EX2", "stated": 30_000, "recomputed": 10_000 + 10_000 + (15_000 - floor_amt(1_000_000)), "cls": "correct",
         "inputs": "$1M income; SALT $10k; mortgage $10k; charity $15k -> itemized total vs std $32,200"},
        {"id": "BOFA-FOOT", "stated": 0.0005 * 30_000_000, "recomputed": floor_amt(30_000_000), "cls": "arithmetic error",
         "inputs": "footnote '0.05% AGI floor' applied to the example's $30M AGI vs the 0.5% statute rate"},
        {"id": "BOFA-EX3", "stated": 2_000_000, "recomputed": round(bofa["saving"], 2), "cls": "ambiguous",
         "inputs": (f"$30M zero-basis sale, $10M gift; stated taxes $6.2M/$4.2M; engine with stated assumptions only: "
                    f"post {bofa['post_sale_tax']:,.0f}, pre {bofa['pre_sale_tax']:,.0f}; gross CG tax "
                    f"{bofa['gross_cg_tax_post']:,.0f}/{bofa['gross_cg_tax_pre']:,.0f}")},
        {"id": "JCF-LOU", "stated": 15_000, "recomputed": lou_gain * 0.15, "cls": "ambiguous",
         "inputs": (f"$100k stock, $8k cost; gain {lou_gain:,}: 15% {lou_gain*0.15:,.0f}; 18.8% {lou_gain*0.188:,.0f}; "
                    f"20% {lou_gain*0.20:,.0f}; 23.8% {lou_gain*0.238:,.0f} (rate and year not stated)")},
        {"id": "JCF-CAP", "stated": 0.35 * 1_000_000, "recomputed": top_bracket_value(50_000), "cls": "ambiguous",
         "inputs": "'value of all deductions is capped at 35% of AGI': read literally at repo H3 AGI $1M = $350k cap; "
                   "statute: per-dollar value 35 cents (H3 $50k gift -> $17,500)"},
        {"id": "COL-CORP", "stated": corporate_cliff_reading(150_000, 10_000_000),
         "recomputed": corporate_deductible(150_000, 10_000_000), "cls": "ambiguous",
         "inputs": "'at least 1 percent ... in order to qualify': TI $10M, gifts $150k; cliff reading vs statute"},
        {"id": "JCF-CORP", "stated": corporate_cliff_reading(150_000, 10_000_000),
         "recomputed": corporate_deductible(150_000, 10_000_000), "cls": "ambiguous",
         "inputs": "'must now give more than 1% of income before deductions apply': same test inputs"},
        {"id": "GKCCF-CORP", "stated": corporate_deductible(150_000, 10_000_000),
         "recomputed": corporate_deductible(150_000, 10_000_000), "cls": "correct",
         "inputs": "'only apply to giving above 1% of taxable income': same test inputs"},
        {"id": "FC-SEC-FN3", "stated": "98,901-613,700", "recomputed":
         f"{eng.P['cg_zero_max_mfj'] + 1:,}-{eng.P['cg_15_max_mfj']:,}", "cls": "correct",
         "inputs": "2026 MFJ 15% capital-gain band on the calculator page vs repo parameters (Rev. Proc. 2025-32)"},
    ]


# ------------------------------------------------------------------------------------------------
# Static page data (quotes as read 2026-11-20; see the research note's source register)
# ------------------------------------------------------------------------------------------------

CSV_COLS = ("finding_id", "rank_fy2024", "sponsor", "ein", "fy2024_daf_assets_usd_bn", "item_type", "item",
            "page_url", "page_date", "accessed", "evidence_label", "rule_tested", "quote_or_output",
            "profile_or_inputs", "stated_value", "recomputed_value", "difference", "classification",
            "error_kind", "note")

FC = ("FIDELITY", "Fidelity Charitable (tools page)", "110303001")
U = {
    "fc_tools": "https://www.fidelitycharitable.org/tools.html",
    "fc_meth": "https://www.fidelitycharitable.org/tools/charitable-tax-savings-calculator/charitable-tax-savings-methodology.html",
    "fc_r4": "https://www.fidelitycharitable.org/tools/charitable-tax-savings-calculator/r4.html",
    "fc_r1": "https://www.fidelitycharitable.org/tools/charitable-tax-savings-calculator/r1.html",
    "fc_sec": "https://www.fidelitycharitable.org/tools/securities-donation-calculator.html",
    "gk": "https://www.growyourgiving.org/news/charitable-giving-under-the-new-tax-law-what-donors-and-their-advisors-should-know/",
    "gh": "https://www.greaterhorizons.org/news/charitable-giving-under-the-new-tax-law-what-donors-and-their-advisors-should-know/",
    "gk_calc": "https://www.growyourgiving.org/resources/gift-calculators/outright-gifts-calculator/",
    "gh_calc": "https://www.greaterhorizons.org/outright-gifts-calculator/",
    "ia": "https://impactassets.org/what-the-one-big-beautiful-bill-act-means-for-2026-charitable-giving/",
    "ia7": "https://impactassets.org/7-tax-benefits-of-the-impactassets-donor-advised-fund/",
    "jcf25": "https://jcfny.org/blog/charitable-giving-in-2025-what-the-new-tax-law-means-for-donors/",
    "jcf_dafx": "https://jcfny.org/donor-advised-funds-tax-deductions/",
    "jcf_tdd": "https://jcfny.org/donor-advised-funds-tax-deductions/tax-deductible-donations/",
    "col": "https://columbusfoundation.org/charitable-insights/important-tax-law-changes",
    "col_b": "https://www.columbusfoundation.org/charitable-insights/bunching-charitable-contributions-is-about-to-become-more-popular-than-ever",
    "bofa_bo": "https://www.privatebank.bankofamerica.com/articles/charitable-giving-unlocked-for-business-owners-under-the-obbba.html",
    "bofa_sum": "https://www.privatebank.bankofamerica.com/articles/one-big-beautiful-bill-act-summary.html",
    "cjp": "https://www.cjp.org/ways-to-give/donor-advised-funds",
    "dt_guide": "https://consider.donorstrust.org/hubfs/DT%20Forms%20and%20Files/Donors%20Guide%20to%20DonorsTrust.pdf",
    "dt_25": "https://www.donorstrust.org/a-smarter-way-to-navigate-2025s-final-giving-stretch/",
    "dech": "https://dechomai.org/a-forensic-deconstructed-post-mortem-2025-noncash-activity-breakdown-with-2026-trends/",
}

# Worked-example metadata: id -> (rank, page key, page_date, rule, quote, error_kind, note)
EX_META = {
    "GKCCF-EX1": (16, "gk", "2025-10-02", "cap_35pct", "a $10,000 donation produces $3,500 of tax savings rather than $3,700", "", ""),
    "GH-EX1": (17, "gh", "2025-10-02", "cap_35pct", "a $10,000 donation produces $3,500 of tax savings rather than $3,700", "", "same article as GKCCF"),
    "GKCCF-EX2": (16, "gk", "2025-10-02", "floor_0_5pct", "with $500,000 of AGI, the first $2,500 of giving won't generate a deduction", "", ""),
    "GH-EX2": (17, "gh", "2025-10-02", "floor_0_5pct", "with $500,000 of AGI, the first $2,500 of giving won't generate a deduction", "", ""),
    "COL-EX1": (22, "col", "undated (2025)", "floor_0_5pct", "someone with $1,000,000 in AGI wouldn't get a tax break on the first $5,000 of donations", "", ""),
    "IA-FAQ1": (13, "ia", "undated (2026 year-end)", "floor_0_5pct", "With $1M of AGI, the first $5,000 you give isn't deductible.", "", ""),
    "IA-EX1a": (13, "ia", "undated (2026 year-end)", "floor_0_5pct", "Contributing three years at once ($300,000) hits the floor only once. That preserves roughly $10,000 more in deductible giving.", "", ""),
    "IA-EX1b": (13, "ia", "undated (2026 year-end)", "cap_35pct", "The extra $10,000 is deductible giving, worth up to about $3,500 in federal tax at 35 cents per dollar.", "unstated_inputs",
                "$3,500 = $10,000 x 35%, correct as a floor-only figure; the repo engine adds about $250 because bunching also shrinks the sec. 68 reduction (depends on other deductions, not stated)"),
    "IA-EX2": (13, "ia", "undated (2026 year-end)", "other", "Had she sold the shares first ... her DAF would have received about $3.1M instead of $4M.", "", "uses 20% + 3.8% NIIT"),
    "BOFA-EX1": (11, "bofa_bo", "2026-07-21", "corporate_1pct_floor", "1% of 10 million is 100,000. If a corporation gave 150,000 ... only the excess, the 50,000", "", "Bank of America Private Bank administers the Charitable Gift Fund"),
    "BOFA-EX2": (11, "bofa_sum", "2025-07 (video, 'next year' = 2026)", "floor_0_5pct", "charitable contributions of 15,000 ... makes $1 million ... floor is 5000 ... only deduct 10,000 ... Collectively that's 30,000. So it doesn't make sense", "", "SALT at $10k matches the phase-down floor at $1M"),
    "BOFA-FOOT": (11, "bofa_bo", "2026-07-21", "floor_0_5pct", "The charitable deduction is first subject to the 0.05% Adjusted Gross Income (AGI) floor", "wrong_parameter",
                  "the same video's narration says 'a half of 1%'; footnote rate is 10x too low"),
    "BOFA-EX3": (11, "bofa_bo", "2026-07-21", "floor_0_5pct", "$30 million sale and a $10 million donation ... ($4.2M vs. $6.2M) and total tax savings of about $2.0M", "not_reproducible",
                 "stated levels equal 20% CG tax on $20M/$30M plus $0.2M; with the slide's own assumptions (floor, 2/37, deduction against gains, 30%/60% limits) the engine gives $2.84M vs $4.09M, saving $1.25M; other income not stated"),
    "JCF-LOU": (14, "jcf_dafx", "undated testimonial (donor since 2006)", "other", "If I had sold the stock, my tax would have been around $15,000 ... fund worth $100,000 with stock that cost me $8,000", "unstated_inputs", "between the 15% and 18.8% results"),
    "JCF-CAP": (14, "jcf25", "2025-10-16", "cap_35pct", "for those in the highest tax bracket the value of all deductions is capped at 35% of AGI", "misstated_mechanism",
                "the statute limits the per-dollar value (2/37 reduction), not deductions as a share of AGI"),
    "COL-CORP": (22, "col", "undated (2025)", "corporate_1pct_floor", "such corporations would have to contribute at least 1 percent of their taxable income in order to qualify for a charitable tax deduction", "threshold_wording",
                 "reads as a cliff; the first 1% is never deductible (same wording on the Columbus bunching article)"),
    "JCF-CORP": (14, "jcf25", "2025-10-16", "corporate_1pct_floor", "C corporations must now give more than 1% of income before deductions apply", "threshold_wording", "base given as 'income', not taxable income"),
    "GKCCF-CORP": (16, "gk", "2025-10-02", "corporate_1pct_floor", "Corporate charitable deductions will only apply to giving above 1% of taxable income.", "", ""),
    "FC-SEC-FN3": ("FIDELITY", "fc_sec", "2026 values on page", "other", "taxable income of $98,901 to $613,700 with a tax filing status of Married Filing Jointly (Note: All values are for tax year 2026.)", "", ""),
}

# Statement rows: (id, rank, page key, page_date, label, rule, quote, classification, error_kind, note)
STATEMENTS = (
    ("FC-METH", "FIDELITY", "fc_meth", "rates as of 2026-01-01", "F", "floor_0_5pct; cap_35pct; nonitemizer_170p",
     "This calculator does not account for ... the 0.5% of AGI charitable deduction floor; the itemized deduction cap that limits the value of deductions against income to 35% ... or the $1,000 cash donation limit for non-itemizers ($2,000 for those married filing jointly).",
     "correct", "", "disclosure is accurate; the formula itself is pre-OBBBA (see calculator rows)"),
    ("FC-R4", "FIDELITY", "fc_r4", "undated", "F", "nonitemizer_170p",
     "Charitable contributions can only reduce your tax bill if you choose to itemize your taxes.",
     "outdated (pre-OBBBA)", "omits_170p", "from 2026 a non-itemizer's direct cash gift is deductible up to $1,000/$2,000 (repo H1: $720 over 3 years); true only for DAF contributions"),
    ("FC-R1", "FIDELITY", "fc_r1", "undated", "F", "nonitemizer_170p",
     "your total itemized tax deductions may not surpass the standard deduction this year, so your charitable contributions may not significantly reduce your tax liability ... Consider the 'bunching' strategy",
     "outdated (pre-OBBBA)", "omits_170p", "repo H1 lands here; page does not mention sec. 170(p) for direct cash gifts"),
    ("FC-SEC-DISC", "FIDELITY", "fc_sec", "2026 values on page", "F", "floor_0_5pct; cap_35pct",
     "This calculator does not consider the new provisions from the One Big Beautiful Bill Act effective in 2026, including the 0.5% floor for charitable deductions or the 35% limit on itemized deductions.",
     "correct", "", "disclosure accurate; CG-rate menu offers only 15% and 20% (no 0% band, no 3.8% NIIT)"),
    ("GKCCF-NI", 16, "gk", "2025-10-02", "F", "nonitemizer_170p",
     "A permanent, above-the-line deduction for non-itemizers giving cash ... up to $1,000 ... or $2,000 ... for cash donations made directly to operating charities. Gifts to donor-advised funds ... don't qualify",
     "ambiguous", "imprecise_term", "amounts and DAF exclusion correct; 'above-the-line' (sec. 63(b)(4) deduction is below AGI) and 'operating charities' (statute: sec. 170(b)(1)(A) organizations) are imprecise; same text on greaterhorizons.org"),
    ("IA-NI", 13, "ia", "undated (2026 year-end)", "F", "nonitemizer_170p; floor_0_5pct",
     "A new deduction for people who don't itemize (up to $1,000, or $2,000 for joint filers) doesn't apply to gifts to a DAF ... Giving below the floor carries forward only in limited cases, generally when your gifts also exceed the annual AGI limits.",
     "correct", "", ""),
    ("JCF-NI", 14, "jcf25", "2025-10-16", "F", "nonitemizer_170p; floor_0_5pct",
     "Beginning in 2026 $1000 for single filers and $2000 for joint. The contribution cannot be made to a DAF ... a floor of 0.5 percent of AGI",
     "correct", "", ""),
    ("JCF-EVERGREEN", 14, "jcf_tdd", "undated (live 2026)", "F", "floor_0_5pct",
     "If you itemize your taxes, you can deduct the amount of money you gave to charity from your taxable income.",
     "outdated (pre-OBBBA)", "omits_floor", "no 2026 floor or cap on JCF's evergreen tax pages"),
    ("COL-NI", 22, "col", "undated (2025)", "F", "nonitemizer_170p; cap_35pct",
     "This deduction is capped at $1,000 for single filers or $2,000 for joint filers ... ineligible ... donations to Donor Advised Funds ... caps the tax benefit at $0.35 for each dollar",
     "correct", "", ""),
    ("BOFA-NI", 11, "bofa_sum", "2025-07 (video)", "F", "nonitemizer_170p",
     "A single taxpayer could deduct up to $1,000 of a cash gift to a public charity. Okay, or $2,000 for a for a couple.",
     "ambiguous", "omits_daf_exclusion", "the DAF exclusion is not stated; DAFs are mentioned only as a bunching vehicle"),
    ("BOFA-FLOORWORD", 11, "bofa_sum", "2025-07 (video)", "F", "floor_0_5pct",
     "the first half of 1% of charitable deductions will no longer be deductible",
     "ambiguous", "wrong_base", "base stated as charitable deductions, not AGI; the worked example later uses AGI correctly"),
    ("CJP-FULL", 18, "cjp", "undated (live 2026)", "F", "floor_0_5pct",
     "You may be eligible for an immediate tax deduction of the full amount you donate!",
     "outdated (pre-OBBBA)", "omits_floor", "from 2026 the first 0.5% of AGI is not deductible for itemizers"),
    ("DT-GUIDE", 23, "dt_guide", "revised June 2025", "F", "floor_0_5pct",
     "Cash: Your deduction is for the amount of your cash contribution, up to 60% of your adjusted gross income",
     "outdated (pre-OBBBA)", "omits_floor", "guide revised before enactment (July 2025)"),
    ("DT-2025", 23, "dt_25", "2025-Q4", "F", "floor_0_5pct; cap_35pct",
     "significant changes to charitable giving tax rules that take effect in 2026. These changes include a new giving floor for itemizers and caps on deductions for high earners.",
     "correct", "", "no figures"),
    ("IA-7BEN", 13, "ia7", "undated", "F", "other",
     "The 2017 Tax Cuts and Jobs Act doubled the standard deduction ... from roughly $12,000 to $24,000 for a married couple ... Excise Tax on Investment Income ... Up to 2%",
     "outdated (pre-OBBBA)", "stale_figures", "2026 MFJ standard deduction is $32,200; PF excise has been a flat 1.39% since 2020; no floor or cap"),
    ("GKCCF-CALC", 16, "gk_calc", "undated", "F", "floor_0_5pct; cap_35pct; nonitemizer_170p",
     "Outright Gifts Calculator (embedded calculator.giftillustrator.com/A0046063/outright-gift)",
     "", "not_ported", "computation is server-side (the page JS posts inputs to a back end); running it is a form submission, so it was not run; same tool on greaterhorizons.org"),
)

COVERAGE = {
    11: ("F (affiliate)", "bofa.donorfirst.org robots 404 (fetched, no tax page); OBBBA pages on privatebank.bankofamerica.com (robots 200)"),
    12: ("R", "www.cct.org robots.txt 403 to curl; 200 to the stdlib client but the page then returned 403; not read"),
    13: ("F", "impactassets.org robots 200; OBBBA article read"),
    14: ("F", "jcfny.org robots 200; 2025 OBBBA article and evergreen tax pages read"),
    15: ("U", "fftc.org not requested: repo records site terms barring robots/scraping"),
    16: ("F", "growyourgiving.org robots 200; OBBBA article read; calculator not ported (server-side)"),
    17: ("F", "greaterhorizons.org robots 200; same article and calculator as GKCCF"),
    18: ("F", "cjp.org robots 200; DAF page read; no OBBBA page found (sitemap and search)"),
    19: ("R", "www.raymondjamescharitable.org robots.txt 403 (timeout on first try); not read"),
    20: ("F", "dechomai.org robots 200; only a 2026-03-01 webinar notice on 2026 trends; no tax figures or calculator"),
    21: ("U", "www.giveny.org unreachable (wrong domain guess); www.nycommunitytrust.org robots 200, guessed URLs 404; no OBBBA page found by search"),
    22: ("F", "columbusfoundation.org robots 404 (no rules); OBBBA article read"),
    23: ("F", "www.donorstrust.org robots 200; one page served a JS verification challenge (not bypassed); 2025 article and June 2025 guide read"),
    24: ("R", "www.uscharitablegifttrust.org robots.txt 403; not read"),
    25: ("U", "no website for the Ayco Charitable Foundation found (search returned only aggregators)"),
}


def build_rows(calc: List[Dict[str, object]], ex: List[Dict[str, object]], league: List[Dict[str, object]],
               accessed: str) -> List[Dict[str, object]]:
    lg = {int(r["rank"]): r for r in league}
    def sponsor(rank) -> Tuple[str, str, str]:
        return (FC[1], FC[2], "") if rank == "FIDELITY" else (lg[rank]["name"], lg[rank]["ein"], lg[rank]["daf_assets_bn"])
    def base(fid, rank, item_type, item, url, date, label, rule) -> Dict[str, object]:
        name, ein, bn = sponsor(rank)
        return {**{c: "" for c in CSV_COLS}, "finding_id": fid, "rank_fy2024": "n/a (tools page)" if rank == "FIDELITY" else rank,
                "sponsor": name, "ein": ein, "fy2024_daf_assets_usd_bn": bn, "item_type": item_type, "item": item,
                "page_url": url, "page_date": date, "accessed": accessed, "evidence_label": label, "rule_tested": rule}
    calc_rows = [{**base(f"FC-CALC-{'TAX' if 'Savings' in c['item'] else 'SEC'}-{c['profile_or_inputs']}", "FIDELITY",
                         "calculator", c["item"], c["page_url"], "2026 values on page", "F+C",
                         "floor_0_5pct; cap_35pct; nonitemizer_170p"),
                  "quote_or_output": c["basis"], "profile_or_inputs": c["profile_or_inputs"],
                  "stated_value": c["stated_value"], "recomputed_value": c["recomputed_value"],
                  "difference": c["difference"], "classification": c["classification"],
                  "error_kind": ("rate_menu_lacks_0pct" if c["classification"] == "ambiguous" else
                                 "omits_170p" if c["profile_or_inputs"] == "H1" else "no_floor_no_cap"),
                  "note": "port of the served JS; recomputed = repo statute engine"} for c in calc]
    ex_rows = [{**base(e["id"], EX_META[e["id"]][0], "worked_example", e["id"], U[EX_META[e["id"]][1]],
                       EX_META[e["id"]][2], "F+C", EX_META[e["id"]][3]),
                "quote_or_output": EX_META[e["id"]][4], "profile_or_inputs": e["inputs"],
                "stated_value": e["stated"], "recomputed_value": e["recomputed"],
                "difference": (round(float(e["stated"]) - float(e["recomputed"]), 2)
                               if not isinstance(e["stated"], str) else ""),
                "classification": e["cls"], "error_kind": EX_META[e["id"]][5], "note": EX_META[e["id"]][6]} for e in ex]
    st_rows = [{**base(s[0], s[1], "statement" if s[7] else "calculator", s[0], U[s[2]], s[3], s[4], s[5]),
                "quote_or_output": s[6], "classification": s[7], "error_kind": s[8], "note": s[9]} for s in STATEMENTS]
    cov_rows = [{**base(f"COV-{k:02d}", k, "coverage", "page coverage", "", "", v[0], ""), "note": v[1]}
                for k, v in sorted(COVERAGE.items())]
    return calc_rows + ex_rows + st_rows + cov_rows


def summarize(rows: List[Dict[str, object]]) -> Dict[str, int]:
    return reduce(lambda acc, r: {**acc, r["classification"]: acc.get(r["classification"], 0) + 1}, rows, {})


def league_11_25(root: Path) -> List[Dict[str, str]]:
    with open(root / LEAGUE_CSV, newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["fiscal_year"] == "2024" and r["row_type"] == "top50"]
    return sorted((r for r in rows if 11 <= int(r["rank_assets"]) <= 25), key=lambda r: int(r["rank_assets"]))


def main(argv: List[str]) -> None:
    root = Path(argv[1] if len(argv) > 1 and not argv[1].startswith("--") else ".").resolve()
    sys.dont_write_bytecode = True   # do not leave a __pycache__ entry for the imported engine
    eng = load_engine(root)
    rep = repo_rows(root)
    calc = calculator_rows(eng, rep)
    ex = worked_examples(eng)
    league = [{"rank": r["rank_assets"], "ein": r["ein"], "name": r["name"],
               "daf_assets_bn": round(float(r["daf_assets_eoy"]) / 1e9, 2)} for r in league_11_25(root)]
    report = {"calculators_vs_repo": calc, "worked_examples": ex, "league_11_25": league,
              "calculator_classes": summarize(calc),
              "fidelity_tax_calc_raw": {p.pid: fidelity_tax_savings_calc(USER_RATE[p.pid], p.gift_per_year, p.other_itemized)
                                        for p in eng.PROFILES}}
    print(json.dumps(report, indent=1, default=str))
    if "--write" in argv:
        rows = build_rows(calc, ex, league, ACCESSED)
        with open(root / OUT_CSV, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(CSV_COLS))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {len(rows)} rows to {OUT_CSV}; classes: {summarize([r for r in rows if r['classification']])}",
              file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv)
