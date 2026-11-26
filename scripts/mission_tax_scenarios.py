#!/usr/bin/env python3
"""Worked 2026 federal tax scenarios: direct gift vs DAF vs private non-operating foundation (P-NEW-TAX-01).

ILLUSTRATIVE MODELLING FOR RESEARCH. NOT TAX ADVICE. Stylised households, federal income tax only.
State and local income tax effects are EXCLUDED. AMT, credits, QBI (199A), tips/overtime/senior
deductions, phase-outs and the SALT-cap mechanics are NOT modelled (other itemized deductions are a
stylised input per profile).

Stdlib only; functional style: parameters are immutable records, every tax quantity is a pure function
of its inputs, and file I/O happens only in main().

Every rule parameter below carries a source id (see SOURCES); each was read in the primary text on
2026-11-15 (statute on govinfo.gov / law.cornell.edu, IRS Rev. Proc. 2025-32, IRS IR-2026-135,
IRS Pub. 6196, eCFR 26 CFR 53.4940-1). Household profiles, gift sizes, basis fractions and the
illustrative PF investment return are STYLISED INPUTS, not sourced facts, and are labelled as such.

Outputs (default paths):
  data/mission-2026-11-14/donor-tax-scenarios-2026.csv              one row per scenario-year + a total row
  data/mission-2026-11-14/donor-tax-scenarios-2026-sensitivity.csv  sensitivity table
  data/mission-2026-11-14/donor-tax-parameters-2026.csv             parameter table with citations

Usage: python3 scripts/mission_tax_scenarios.py [--outdir DIR]
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List, NamedTuple, Tuple

ROOT = Path(__file__).resolve().parent.parent
OUTDIR_DEFAULT = ROOT / "data" / "mission-2026-11-14"
RETRIEVED = "2026-11-15"

# ---------------------------------------------------------------------------------------------
# Sources (all read 2026-11-15; robots.txt checked on each host before fetching)
# ---------------------------------------------------------------------------------------------
SOURCES: Dict[str, Tuple[str, str]] = {
    "PL119-21": ("Public Law 119-21 (OBBBA), Statutes at Large text, secs. 70111, 70424, 70425",
                 "https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm"),
    "IRC170": ("26 U.S.C. 170 as amended through P.L. 119-21 (LII)", "https://www.law.cornell.edu/uscode/text/26/170"),
    "IRC63": ("26 U.S.C. 63(b) (LII)", "https://www.law.cornell.edu/uscode/text/26/63"),
    "IRC1": ("26 U.S.C. 1(h)(1) and 1(j)(5) (LII)", "https://www.law.cornell.edu/uscode/text/26/1"),
    "IRC1411": ("26 U.S.C. 1411 (LII)", "https://www.law.cornell.edu/uscode/text/26/1411"),
    "IRC4940": ("26 U.S.C. 4940 (LII)", "https://www.law.cornell.edu/uscode/text/26/4940"),
    "IRC4942": ("26 U.S.C. 4942 (LII)", "https://www.law.cornell.edu/uscode/text/26/4942"),
    "REG53.4940-1": ("26 CFR 53.4940-1(f)(2) (eCFR, 2026-11-01 point in time)",
                     "https://www.ecfr.gov/current/title-26/chapter-I/subchapter-D/part-53/subpart-B/section-53.4940-1"),
    "RP2025-32": ("IRS Rev. Proc. 2025-32, sec. 4.01, 4.03, 4.14 (2026 inflation adjustments)",
                  "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf"),
    "IR-2026-135": ("IRS IR-2026-135 (Nov 10, 2026), non-itemizer deduction; DAF gifts do not qualify",
                    "https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize"),
    "P6196": ("IRS Publication 6196 (10-2026), Charitable Contribution Deduction Tips for Non-Itemizers",
              "https://www.irs.gov/pub/irs-pdf/p6196.pdf"),
}


class Param(NamedTuple):
    key: str
    value: object
    rule: str
    source: str        # key into SOURCES
    note: str


# ---------------------------------------------------------------------------------------------
# 2026 rule parameters (married filing jointly only). Values copied from the cited primary text.
# ---------------------------------------------------------------------------------------------
MFJ_BRACKETS = ((24_800, 0.10), (100_800, 0.12), (211_400, 0.22), (403_550, 0.24),
                (512_450, 0.32), (768_700, 0.35), (float("inf"), 0.37))
PARAMS: Tuple[Param, ...] = (
    Param("mfj_brackets", MFJ_BRACKETS, "2026 MFJ ordinary rate schedule", "RP2025-32",
          "Table 1, sec. 4.01; upper bound of each band and its rate"),
    Param("top_bracket_start_mfj", 768_700, "Start of 37% bracket (used by new sec. 68)", "RP2025-32",
          "Table 1; sec. 68(a)(2) as enacted by P.L. 119-21 sec. 70111"),
    Param("std_deduction_mfj", 32_200, "2026 standard deduction, MFJ", "RP2025-32", "sec. 4.14(1)"),
    Param("cg_zero_max_mfj", 98_900, "Maximum zero-rate amount (taxable income), MFJ", "RP2025-32",
          "sec. 4.03; applied via sec. 1(h)(1) as modified by sec. 1(j)(5)(A) [IRC1]"),
    Param("cg_15_max_mfj", 613_700, "Maximum 15%-rate amount (taxable income), MFJ", "RP2025-32", "sec. 4.03"),
    Param("cg_rates", (0.0, 0.15, 0.20), "LTCG rates 0/15/20%", "IRC1", "sec. 1(h)(1)(B)-(D)"),
    Param("niit_rate", 0.038, "Net investment income tax rate", "IRC1411", "sec. 1411(a)(1)"),
    Param("niit_threshold_mfj", 250_000, "NIIT threshold, joint return (not indexed)", "IRC1411", "sec. 1411(b)(1)"),
    Param("sec68_fraction", 2 / 37, "Itemized deductions reduced by 2/37 of lesser of (1) itemized deductions or "
          "(2) taxable income + itemized deductions above the 37% bracket start", "PL119-21",
          "sec. 70111 (new sec. 68(a)); applied after all other limitations (sec. 68(b)); tax years after 2025"),
    Param("floor_pct_contribution_base", 0.005, "0.5% of contribution base floor on itemized charitable deduction",
          "PL119-21", "sec. 70425(a) (new sec. 170(b)(1)(I)); applied first to (D), then (C), (B), (E), (A), (G) gifts"),
    Param("floor_carryforward_rule", "only from years in which a percentage limit is exceeded", "Floor-disallowed "
          "amounts carried forward only with a percentage-limit excess", "PL119-21", "sec. 70425(a)(2) (new sec. 170(d)(1)(C))"),
    Param("contribution_base", "AGI (without NOL carryback)", "Contribution base definition", "IRC170", "sec. 170(b)(1)(H)"),
    Param("limit_cash_public_G", 0.60, "Cash to public charity (incl. DAF sponsor): 60% of contribution base",
          "PL119-21", "sec. 70425(b)(1) makes sec. 170(b)(1)(G)(i) permanent"),
    Param("limit_capgain_public_C", 0.30, "Capital gain property to public charity (incl. DAF sponsor): 30%",
          "IRC170", "sec. 170(b)(1)(C)(i)"),
    Param("limit_other_B", 0.30, "Cash to private non-operating foundation: 30% (lesser of 30% or 50% less A/G gifts)",
          "IRC170", "sec. 170(b)(1)(B)"),
    Param("limit_capgain_pf_D", 0.20, "Capital gain property to private non-operating foundation: 20% "
          "(lesser of 20% or 30% less C gifts)", "IRC170", "sec. 170(b)(1)(D)(i)"),
    Param("carryforward_years", 5, "Percentage-limit excess carried forward 5 years", "IRC170",
          "secs. 170(b)(1)(B), (C)(ii), (D)(ii), (G)(ii), 170(d)(1)(A)"),
    Param("pf_stock_fmv_rule", "FMV for qualified appreciated stock", "Gift of listed long-held stock to a "
          "non-operating PF is not reduced to basis", "IRC170",
          "sec. 170(e)(1)(B)(ii) reduction disapplied by sec. 170(e)(5) (listed stock; donor+family <=10% of the company)"),
    Param("nonitemizer_cap_mfj", 2_000, "Non-itemizer deduction cap ($1,000 single / $2,000 joint), permanent",
          "PL119-21", "sec. 70424 amends sec. 170(p); deductible in addition to standard deduction per sec. 63(b)(4) [IRC63]"),
    Param("nonitemizer_scope", "cash to sec. 170(b)(1)(A) org; not 509(a)(3); not to establish/maintain a DAF",
          "Non-itemizer deduction excludes DAF gifts; non-operating PFs are not 170(b)(1)(A) orgs (unless sec. "
          "170(b)(1)(F) conduit/pooled)", "IRC170", "sec. 170(p) text; IR-2026-135 and P6196 confirm DAF exclusion"),
    Param("nonitemizer_floor", "not applied", "0.5% floor does not apply to the non-itemizer deduction",
          "PL119-21", "sec. 70425(a)(3) adds (b)(1)(I) to the 'determined without regard to' list in sec. 170(p)"),
    Param("pf_excise_rate", 0.0139, "Excise tax on PF net investment income (incl. capital gains)", "IRC4940",
          "sec. 4940(a); not amended by P.L. 119-21 (text search of the Act: sec. 4940 referenced only in new "
          "sec. 4968(f))"),
    Param("pf_gain_basis", "donor's carryover basis", "PF gain on sale of donated property uses basis under "
          "Part II of Subchapter O (gift basis)", "REG53.4940-1", "26 CFR 53.4940-1(f)(2)(i)(B)"),
    Param("pf_min_payout", 0.05, "Distributable amount = 5% of non-charitable-use assets less sec. 4940 and income "
          "taxes; due by end of following year", "IRC4942", "sec. 4942(d), (e)(1)"),
)
P = {p.key: p.value for p in PARAMS}

# Parameters requested but deliberately excluded (could not verify or out of scope); reported in the note.
EXCLUDED = (
    "State and local income tax (excluded by design).",
    "Sponsor/foundation fees, legal and setup costs for a PF (not tax parameters; not modelled).",
    "Inflation adjustment of 2027+ brackets and standard deduction (2026 values held flat across the horizon).",
    "Cash held for charitable activities (1.5% set-aside in regs) and other 4942 adjustments: not modelled.",
    "AMT, credits, sec. 199A, sec. 224/225 deductions, senior deduction, SALT-cap phase-down mechanics.",
)

# ---------------------------------------------------------------------------------------------
# Stylised inputs (NOT sourced facts). Married filing jointly throughout.
# ---------------------------------------------------------------------------------------------


class Profile(NamedTuple):
    pid: str
    label: str
    wages: float                 # ordinary income per year (stylised)
    other_itemized: float        # non-charitable itemized deductions per year (stylised; SALT etc. already capped)
    gift_per_year: float         # intended annual giving (stylised)
    horizon: int                 # years modelled
    event_ltcg_y1: float         # one-off long-term gain from an unrelated sale in year 1 (stylised)
    oneoff: bool                 # True: single gift in year 1 rather than annual giving
    basis_fraction: float        # basis / FMV of donated stock (stylised)


PROFILES: Tuple[Profile, ...] = (
    Profile("H1", "Non-itemizer, moderate income", 90_000, 12_000, 2_000, 3, 0, False, 0.20),
    Profile("H2", "Itemizer near the standard deduction, 24% bracket", 300_000, 25_000, 10_000, 3, 0, False, 0.20),
    Profile("H3", "Itemizer, 37% bracket", 1_000_000, 40_000, 50_000, 3, 0, False, 0.20),
    Profile("H4", "High income with one-off liquidity event (investment sale) in year 1", 400_000, 40_000,
            1_000_000, 6, 3_000_000, True, 0.20),
)

ASSETS = ("cash", "stock_in_kind", "stock_sold_then_cash")
VEHICLES = ("direct", "daf", "pf")
ILLUSTRATIVE_PF_RETURNS = (0.0, 0.04, 0.08)   # sensitivity only; not sourced


# ---------------------------------------------------------------------------------------------
# Tax engine (pure functions)
# ---------------------------------------------------------------------------------------------

def ordinary_tax(ti: float) -> float:
    """Tax on ordinary taxable income using the 2026 MFJ schedule."""
    tax, lower = 0.0, 0.0
    for upper, rate in P["mfj_brackets"]:
        if ti <= lower:
            break
        tax += (min(ti, upper) - lower) * rate
        lower = upper
    return tax


def regular_tax(ti: float, ltcg: float) -> float:
    """Sec. 1(h)(1) with sec. 1(j)(5): gains stacked on top of ordinary income; thresholds on taxable income."""
    ti = max(0.0, ti)
    cg = min(max(0.0, ltcg), ti)
    ord_ti = ti - cg
    zero_band = max(0.0, min(cg, P["cg_zero_max_mfj"] - ord_ti))
    fifteen_band = max(0.0, min(cg - zero_band, P["cg_15_max_mfj"] - ord_ti - zero_band))
    twenty_band = cg - zero_band - fifteen_band
    return ordinary_tax(ord_ti) + 0.15 * fifteen_band + 0.20 * twenty_band


def niit(agi: float, nii: float) -> float:
    return P["niit_rate"] * max(0.0, min(nii, agi - P["niit_threshold_mfj"]))


LIMITS = {"G": "limit_cash_public_G", "C": "limit_capgain_public_C", "B": "limit_other_B", "D": "limit_capgain_pf_D"}
FLOOR_ORDER = ("D", "C", "B", "E", "A", "G")


def category(vehicle: str, asset: str) -> str:
    """Sec. 170(b)(1) category. DAF sponsors are public charities (A orgs); the stylised PF is non-operating."""
    is_cash = asset in ("cash", "stock_sold_then_cash")
    if vehicle in ("direct", "daf"):
        return "G" if is_cash else "C"
    return "B" if is_cash else "D"


class CharResult(NamedTuple):
    allowed: float
    floor_applied: float
    pct_limit_excess: float
    carry_out: Tuple[Tuple[int, float], ...]   # (vintage year, amount)
    expired: float


def charitable_itemized(year: int, cat: str, current: float, carry_in: Tuple[Tuple[int, float], ...],
                        cb: float) -> CharResult:
    """One category per scenario (assertion in run_scenario). Current-year gifts are absorbed before carryovers
    (sec. 170(d)(1)(A)); carryovers oldest first; vintages older than 5 years expire.
    The 0.5% floor is applied to the aggregate otherwise allowable amount, including carryovers absorbed this
    year [interpretation: statute applies the floor to 'any charitable contribution otherwise allowable'].
    Floor-disallowed amounts are added to the carryforward only in a year with a percentage-limit excess
    (sec. 170(d)(1)(C)); we date them to the current year [interpretation]."""
    live = tuple((v, a) for v, a in carry_in if year - v <= P["carryforward_years"] and a > 0)
    expired = sum(a for v, a in carry_in if year - v > P["carryforward_years"])
    limit = P[LIMITS[cat]] * cb
    take_current = min(current, limit)
    room = limit - take_current
    remaining: List[Tuple[int, float]] = []
    taken_carry = 0.0
    for v, a in sorted(live):
        t = min(a, room)
        room -= t
        taken_carry += t
        if a - t > 1e-9:
            remaining.append((v, a - t))
    excess_current = current - take_current
    if excess_current > 1e-9:
        remaining.append((year, excess_current))
    pre_floor = take_current + taken_carry
    floor = min(pre_floor, P["floor_pct_contribution_base"] * cb)
    excess_total = excess_current + sum(a for _, a in remaining if _ != year)
    if floor > 0 and remaining:  # a percentage-limit excess exists this year -> floor amount carried forward
        remaining.append((year, floor))
    merged: Dict[int, float] = {}
    for v, a in remaining:
        merged[v] = merged.get(v, 0.0) + a
    return CharResult(pre_floor - floor, floor, excess_total, tuple(sorted(merged.items())), expired)


class YearIn(NamedTuple):
    year: int
    wages: float
    ltcg: float
    other_itemized: float
    gift_fmv: float
    cat: str            # sec. 170(b)(1) category of the gift ("" if none)
    nonitemizer_cash: float   # cash qualifying for sec. 170(p)
    carry_in: Tuple[Tuple[int, float], ...]


class YearOut(NamedTuple):
    agi: float
    method: str
    char_allowed: float
    floor_applied: float
    sec68_reduction: float
    deduction: float
    taxable_income: float
    regular_tax: float
    niit: float
    total_tax: float
    carry_out: Tuple[Tuple[int, float], ...]
    expired: float
    pct_limit_excess: float


def year_tax(y: YearIn) -> YearOut:
    agi = y.wages + y.ltcg
    cb = agi
    if y.cat:
        ch = charitable_itemized(y.year, y.cat, y.gift_fmv, y.carry_in, cb)
    else:
        ch = CharResult(0.0, 0.0, 0.0, y.carry_in, 0.0)
    itemized_pre68 = y.other_itemized + ch.allowed
    red68 = P["sec68_fraction"] * min(itemized_pre68, max(0.0, agi - P["top_bracket_start_mfj"]))
    itemized = itemized_pre68 - red68
    std = P["std_deduction_mfj"] + min(P["nonitemizer_cap_mfj"], y.nonitemizer_cash)
    def tax_for(ded: float) -> Tuple[float, float, float, float]:
        ti = max(0.0, agi - ded)
        rt = regular_tax(ti, y.ltcg)
        nt = niit(agi, y.ltcg)
        return ti, rt, nt, rt + nt
    ti_i, rt_i, nt_i, tot_i = tax_for(itemized)
    ti_s, rt_s, nt_s, tot_s = tax_for(std)
    if tot_i < tot_s:
        return YearOut(agi, "itemize", ch.allowed, ch.floor_applied, red68, itemized, ti_i, rt_i, nt_i, tot_i,
                       ch.carry_out, ch.expired, ch.pct_limit_excess)
    # Standard deduction year. Carryovers: treatment when not itemizing is NOT modelled (kept, flagged).
    return YearOut(agi, "standard", 0.0, 0.0, 0.0, std, ti_s, rt_s, nt_s, tot_s,
                   y.carry_in if not y.cat else ch.carry_out, ch.expired, ch.pct_limit_excess)


# ---------------------------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------------------------

def schedules(pr: Profile) -> Dict[str, Tuple[float, ...]]:
    """Gift FMV by year for each timing strategy."""
    n, g = pr.horizon, pr.gift_per_year
    if pr.oneoff:
        return {"oneoff_y1": (g,) + (0.0,) * (n - 1)}
    return {"annual": (g,) * n, "bunched_y1": (g * n,) + (0.0,) * (n - 1)}


def run_years(pr: Profile, vehicle: str, asset: str, gifts: Tuple[float, ...], basis_fraction: float,
              other_itemized: float) -> List[Tuple[YearIn, YearOut]]:
    rows: List[Tuple[YearIn, YearOut]] = []
    carry: Tuple[Tuple[int, float], ...] = ()
    cat = category(vehicle, asset) if any(gifts) else ""
    for i in range(pr.horizon):
        year = 2026 + i
        g = gifts[i]
        sale_gain = g * (1 - basis_fraction) if asset == "stock_sold_then_cash" else 0.0
        ltcg = (pr.event_ltcg_y1 if i == 0 else 0.0) + sale_gain
        nonitem = g if (vehicle == "direct" and asset in ("cash", "stock_sold_then_cash")) else 0.0
        yi = YearIn(year, pr.wages, ltcg, other_itemized, g, cat if (g > 0 or carry) else "", nonitem, carry)
        yo = year_tax(yi)
        rows.append((yi, yo))
        carry = yo.carry_out
    return rows


def baseline(pr: Profile, other_itemized: float) -> List[YearOut]:
    return [yo for _, yo in run_years(pr, "direct", "cash", (0.0,) * pr.horizon, pr.basis_fraction, other_itemized)]


def pf_vehicle_metrics(vehicle: str, asset: str, gifts: Tuple[float, ...], basis_fraction: float,
                       pf_return: float) -> Dict[str, float]:
    """Vehicle-level PF quantities (not donor tax). Stylised: PF receives the gift at FMV, zero growth unless
    pf_return given, no grants in the year of receipt."""
    if vehicle != "pf":
        return {"pf_excise_if_donated_stock_sold": 0.0, "pf_y1_annual_excise_on_return": 0.0,
                "pf_min_distribution_from_y1_assets": 0.0}
    g1 = gifts[0]
    builtin = g1 * (1 - basis_fraction) if asset == "stock_in_kind" else 0.0
    excise_sale = P["pf_excise_rate"] * builtin
    excise_ret = P["pf_excise_rate"] * pf_return * g1
    return {"pf_excise_if_donated_stock_sold": excise_sale,
            "pf_y1_annual_excise_on_return": excise_ret,
            # 4942(d)/(e): 5% of non-charitable-use assets less sec. 4940 tax (year-end FMV used as the average)
            "pf_min_distribution_from_y1_assets": max(0.0, P["pf_min_payout"] * g1 - excise_sale - excise_ret)}


def scenario_rows(pr: Profile, basis_fraction: float = None, other_itemized: float = None,
                  gift_scale: float = 1.0, pf_return: float = 0.0) -> List[Dict[str, object]]:
    bf = pr.basis_fraction if basis_fraction is None else basis_fraction
    oi = pr.other_itemized if other_itemized is None else other_itemized
    base = baseline(pr, oi)
    base_tax = sum(b.total_tax for b in base)
    out: List[Dict[str, object]] = []
    for timing, sched in schedules(pr).items():
        gifts = tuple(x * gift_scale for x in sched)
        for asset in ASSETS:
            for vehicle in VEHICLES:
                yrs = run_years(pr, vehicle, asset, gifts, bf, oi)
                total_tax = sum(yo.total_tax for _, yo in yrs)
                gift_total = sum(gifts)
                saving = base_tax - total_tax
                sid = f"{pr.pid}|{asset}|{vehicle}|{timing}"
                common = {"scenario_id": sid, "profile": pr.pid, "profile_label": pr.label, "asset": asset,
                          "vehicle": vehicle, "timing": timing, "basis_fraction": bf, "other_itemized": oi,
                          "pf_return_illustrative": pf_return}
                for (yi, yo), b in zip(yrs, base):
                    out.append({**common, "row": "year", "year": yi.year, "wages": yi.wages, "ltcg": yi.ltcg,
                                "agi": round(yo.agi, 2), "gift_fmv": yi.gift_fmv, "sec170_category": yi.cat,
                                "method": yo.method, "char_deduction_allowed": round(yo.char_allowed, 2),
                                "floor_disallowed": round(yo.floor_applied, 2),
                                "sec68_reduction": round(yo.sec68_reduction, 2),
                                "total_deduction": round(yo.deduction, 2),
                                "taxable_income": round(yo.taxable_income, 2),
                                "regular_tax": round(yo.regular_tax, 2), "niit": round(yo.niit, 2),
                                "federal_tax": round(yo.total_tax, 2), "baseline_tax": round(b.total_tax, 2),
                                "tax_saving_vs_no_gift": round(b.total_tax - yo.total_tax, 2),
                                "carryforward_end": round(sum(a for _, a in yo.carry_out), 2),
                                "carry_expired": round(yo.expired, 2),
                                "flag": ("carryover_in_standard_deduction_year" if yo.method == "standard"
                                         and yo.carry_out else "")})
                last = yrs[-1][1]
                pfm = pf_vehicle_metrics(vehicle, asset, gifts, bf, pf_return)
                out.append({**common, "row": "total", "year": f"2026-{2025 + pr.horizon}",
                            "wages": pr.wages * pr.horizon, "ltcg": sum(yi.ltcg for yi, _ in yrs),
                            "gift_fmv": gift_total, "federal_tax": round(total_tax, 2),
                            "baseline_tax": round(base_tax, 2), "tax_saving_vs_no_gift": round(saving, 2),
                            "saving_per_gift_dollar": round(saving / gift_total, 4) if gift_total else "",
                            "net_cost_to_donor": round(gift_total - saving, 2),
                            "char_deduction_allowed": round(sum(yo.char_allowed for _, yo in yrs), 2),
                            "floor_disallowed": round(sum(yo.floor_applied for _, yo in yrs), 2),
                            "sec68_reduction": round(sum(yo.sec68_reduction for _, yo in yrs), 2),
                            "carryforward_end": round(sum(a for _, a in last.carry_out), 2),
                            "years_itemized": sum(1 for _, yo in yrs if yo.method == "itemize"),
                            **{k: round(v, 2) for k, v in pfm.items()}})
    return out


def add_deltas(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Compare each total row with the direct/cash/same-timing row and the direct/annual row of the same asset."""
    totals = {r["scenario_id"]: r for r in rows if r["row"] == "total"}
    def ref(r, asset, vehicle, timing):
        return totals.get(f"{r['profile']}|{asset}|{vehicle}|{timing}")
    def enrich(r):
        if r["row"] != "total":
            return r
        first_timing = "oneoff_y1" if r["timing"] == "oneoff_y1" else "annual"
        d1 = ref(r, r["asset"], "direct", first_timing)
        d2 = ref(r, "stock_sold_then_cash", r["vehicle"], r["timing"])
        return {**r,
                "saving_minus_direct_annual_same_asset": round(r["tax_saving_vs_no_gift"] - d1["tax_saving_vs_no_gift"], 2),
                "stock_in_kind_saving_minus_sell_then_give": (
                    round(r["tax_saving_vs_no_gift"] - d2["tax_saving_vs_no_gift"], 2)
                    if r["asset"] == "stock_in_kind" else "")}
    return [enrich(r) for r in rows]


def sensitivity(profiles: Iterable[Profile]) -> List[Dict[str, object]]:
    by = {p.pid: p for p in profiles}
    out: List[Dict[str, object]] = []
    def pick(rows, sid):
        return next(r for r in rows if r["row"] == "total" and r["scenario_id"] == sid)
    # S1: basis fraction -> value of giving stock in kind vs selling then giving cash (DAF, annual/oneoff)
    for pid, timing in (("H2", "annual"), ("H3", "annual"), ("H4", "oneoff_y1")):
        for bf in (0.0, 0.2, 0.5, 1.0):
            rows = add_deltas(scenario_rows(by[pid], basis_fraction=bf))
            r = pick(rows, f"{pid}|stock_in_kind|daf|{timing}")
            out.append({"test": "S1 basis fraction", "profile": pid, "scenario_id": r["scenario_id"],
                        "varied_input": "basis_fraction", "value": bf,
                        "tax_saving_vs_no_gift": r["tax_saving_vs_no_gift"],
                        "metric": "stock_in_kind_saving_minus_sell_then_give",
                        "metric_value": r["stock_in_kind_saving_minus_sell_then_give"]})
    # S2: other itemized deductions -> value of DAF bunching vs annual direct (cash), H2
    for oi in (10_000, 20_000, 25_000, 30_000, 40_000):
        rows = add_deltas(scenario_rows(by["H2"], other_itemized=oi))
        r = pick(rows, "H2|cash|daf|bunched_y1")
        out.append({"test": "S2 other itemized deductions", "profile": "H2", "scenario_id": r["scenario_id"],
                    "varied_input": "other_itemized", "value": oi,
                    "tax_saving_vs_no_gift": r["tax_saving_vs_no_gift"],
                    "metric": "saving_minus_direct_annual_same_asset",
                    "metric_value": r["saving_minus_direct_annual_same_asset"]})
    # S3: gift size -> AGI limits and carryforward, H4 one-off stock gift, DAF vs PF
    for scale in (0.5, 1.0, 1.5, 2.0):
        rows = add_deltas(scenario_rows(by["H4"], gift_scale=scale))
        for v in ("daf", "pf"):
            r = pick(rows, f"H4|stock_in_kind|{v}|oneoff_y1")
            out.append({"test": "S3 gift size (AGI limits)", "profile": "H4", "scenario_id": r["scenario_id"],
                        "varied_input": "gift_fmv", "value": r["gift_fmv"],
                        "tax_saving_vs_no_gift": r["tax_saving_vs_no_gift"],
                        "metric": "carryforward_end (unused after horizon)", "metric_value": r["carryforward_end"]})
    # S4: illustrative PF return -> annual 1.39% excise drag on a PF holding the H4 gift
    for ret in ILLUSTRATIVE_PF_RETURNS:
        rows = scenario_rows(by["H4"], pf_return=ret)
        r = pick(rows, "H4|cash|pf|oneoff_y1")
        out.append({"test": "S4 PF investment return (illustrative input)", "profile": "H4",
                    "scenario_id": r["scenario_id"], "varied_input": "pf_return", "value": ret,
                    "tax_saving_vs_no_gift": r["tax_saving_vs_no_gift"],
                    "metric": "pf_y1_annual_excise_on_return", "metric_value": r["pf_y1_annual_excise_on_return"]})
    # S5: H1 gift size -> when does DAF bunching make itemizing worthwhile vs non-itemizer direct cash
    for g in (1_000, 2_000, 5_000, 8_000):
        pr = by["H1"]._replace(gift_per_year=g)
        rows = add_deltas(scenario_rows(pr))
        for sid in (f"H1|cash|direct|annual", f"H1|cash|daf|bunched_y1"):
            r = pick(rows, sid)
            out.append({"test": "S5 non-itemizer gift size", "profile": "H1", "scenario_id": sid,
                        "varied_input": "gift_per_year", "value": g,
                        "tax_saving_vs_no_gift": r["tax_saving_vs_no_gift"],
                        "metric": "years_itemized", "metric_value": r["years_itemized"]})
    return out


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    cols: List[str] = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def self_checks() -> None:
    """Hand-checkable identities from the cited text."""
    assert abs(ordinary_tax(211_400) - 35_932) < 0.01          # Rev. Proc. 2025-32 Table 1
    assert abs(ordinary_tax(768_700) - 206_583.50) < 0.01
    assert abs(regular_tax(98_900, 98_900) - 0.0) < 0.01       # all gain inside the zero-rate amount
    # 35% cap: an extra $1,000 of itemized deductions deep in the 37% band saves 37% * (1 - 2/37) = 35%
    a = year_tax(YearIn(2026, 2_000_000, 0, 50_000, 0, "", 0, ()))
    b = year_tax(YearIn(2026, 2_000_000, 0, 51_000, 0, "", 0, ()))
    assert abs((a.total_tax - b.total_tax) - 350.0) < 0.01


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--outdir", default=str(OUTDIR_DEFAULT))
    outdir = Path(ap.parse_args().outdir)
    self_checks()
    rows = [r for pr in PROFILES for r in add_deltas(scenario_rows(pr))]
    write_csv(outdir / "donor-tax-scenarios-2026.csv", rows)
    write_csv(outdir / "donor-tax-scenarios-2026-sensitivity.csv", sensitivity(PROFILES))
    write_csv(outdir / "donor-tax-parameters-2026.csv",
              [{"key": p.key, "value": p.value, "rule": p.rule, "source_id": p.source,
                "source_title": SOURCES[p.source][0], "url": SOURCES[p.source][1], "pinpoint": p.note,
                "retrieved": RETRIEVED} for p in PARAMS]
              + [{"key": f"excluded_{i + 1}", "value": "EXCLUDED", "rule": e, "source_id": "", "source_title": "",
                  "url": "", "pinpoint": "", "retrieved": RETRIEVED} for i, e in enumerate(EXCLUDED)]
              + [{"key": f"input_{pr.pid}", "value": "STYLISED INPUT (not sourced)",
                  "rule": f"{pr.label}: wages {pr.wages:,.0f}; other itemized {pr.other_itemized:,.0f}; gift "
                          f"{pr.gift_per_year:,.0f}{' one-off' if pr.oneoff else '/yr'}; horizon {pr.horizon}y; "
                          f"year-1 LTCG {pr.event_ltcg_y1:,.0f}; stock basis/FMV {pr.basis_fraction}",
                  "source_id": "", "source_title": "", "url": "", "pinpoint": "MFJ", "retrieved": RETRIEVED}
                 for pr in PROFILES])
    tot = [r for r in rows if r["row"] == "total"]
    print(f"{len(rows)} rows ({len(tot)} scenario totals) -> {outdir}")
    for r in tot:
        print(f"{r['scenario_id']:<40} gift {r['gift_fmv']:>11,.0f}  saving {r['tax_saving_vs_no_gift']:>11,.2f}"
              f"  per$ {r['saving_per_gift_dollar']!s:>7}  vsDirAnn {r['saving_minus_direct_annual_same_asset']:>10,.2f}"
              f"  carry {r['carryforward_end']:>10,.0f}  itemYrs {r['years_itemized']}")


if __name__ == "__main__":
    main()
