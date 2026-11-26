"""P-B42N20-03 numeric checks: sponsor calculators and worked examples vs repo H1-H3.

Usage: python3 scripts/mission_b41n16_b42n20_checks.py .   (root of the repo)

Stdlib only, pure functions. Prints a JSON report to stdout; writes nothing.
- vanguard_calc(): faithful port of the calculateTaxSavings() function served in
  vanguardcharitable.org/charitable-tax-center JS (fetched 2026-11-19).
- schwab_bunching_calc(): faithful port of taxCalculator() in the DAFgiving360
  bunching-calculator component p-577835bb.entry.js (fetched 2026-11-19).
- statute_*: the 2026 rules as read in P.L. 119-21 s.70111/70424/70425 and
  26 USC 170(p) (0.5% floor; 2/37 reduction; $2,000 joint non-itemizer cash).
Not tax advice.
"""
import csv, json, os, sys

STD_MFJ = 32200
FLOOR = 0.005


def floor_amt(agi):
    return FLOOR * agi


def vanguard_calc(agi, rate, contrib, itemized, std=STD_MFJ):
    fl = floor_amt(agi)
    allowed = max(0.0, min(contrib - fl, agi * 0.6 - fl))
    total = allowed + itemized
    eff = 0.35 if rate == 0.37 else rate
    return max(0.0, (total - std) * eff)


def schwab_bunching_calc(rate, itemized, donation, std=STD_MFJ):
    total = itemized + donation
    n = total if total > std else std
    three_without = n * 3
    bunch_y1 = itemized + donation * 3
    later = std if std > itemized else itemized
    three_with = bunch_y1 + 2 * later
    one = donation * rate if itemized > std else (total - std) * rate
    three = donation * 3 * rate if itemized > std else (itemized + donation * 3 - std) * rate
    return {
        "annual_saving_per_year": max(0.0, one),
        "annual_saving_3yr": 3 * max(0.0, one),
        "bunched_3yr_saving": max(0.0, three),
        "bunch_addl_tax_saving": (three_with - three_without) * rate if three_with > three_without else 0.0,
    }


def statute_gift_saving_itemizer(agi, rate, gift, other_itemized, std=STD_MFJ, top_start=768700):
    """Marginal saving of an itemized gift vs no gift, simple single-rate model
    (rate held fixed), floor then s.68 2/37 reduction when AGI is past the 37% start."""
    def taxable_deduction(g):
        allowed = max(0.0, g - floor_amt(agi)) if g > 0 else 0.0
        item = allowed + other_itemized
        red = (2 / 37) * min(item, max(0.0, agi - top_start)) if rate == 0.37 else 0.0
        return max(std, item - red)
    return (taxable_deduction(gift) - taxable_deduction(0.0)) * rate


def worked_examples():
    """Each sponsor example: stated figures and recomputation under the stated assumptions."""
    vg_annual = (40000 - floor_amt(700000)) * 0.35
    vg_bunch = (120000 - floor_amt(700000)) * 0.35
    aef_item = 36000 - floor_amt(300000) + 18000
    aef_tot_annual = 3 * STD_MFJ
    aef_tot_bunch = aef_item + 2 * STD_MFJ
    aef_tot_annual_direct_170p = 3 * (STD_MFJ + 2000)
    fid_deck_after = (200000 - floor_amt(2_500_000)) * 0.35
    return [
        {"id": "VC-EX1", "sponsor": "Vanguard Charitable", "stated": {"annual_saving_per_year": 9490, "annual_3yr": 28470, "bunched": 29125, "gain": 655},
         "recomputed": {"annual_saving_per_year": vg_annual, "annual_3yr": 3 * vg_annual, "bunched": vg_bunch, "gain": vg_bunch - 3 * vg_annual},
         "implied_rate_annual": 9490 / 36500, "implied_rate_bunched": 29125 / 116500},
        {"id": "VC-EX2", "sponsor": "Vanguard Charitable", "stated": {"floor": 3200, "deductible_bunched": 5800},
         "recomputed": {"floor": floor_amt(640000), "deductible_bunched": 9000 - floor_amt(640000)}},
        {"id": "VC-EX3", "sponsor": "Vanguard Charitable", "stated": {"floor": 10000, "deductible_25k": 15000},
         "recomputed": {"floor": floor_amt(2_000_000), "deductible_25k": 25000 - floor_amt(2_000_000)}},
        {"id": "AEF-EX1", "sponsor": "American Endowment Foundation",
         "stated": {"itemized_y1": 52500, "total_annual": 96600, "total_bunched": 116900, "addl": 20300, "tax_approx": 4900},
         "recomputed": {"itemized_y1": aef_item, "total_annual": aef_tot_annual, "total_bunched": aef_tot_bunch,
                        "addl": aef_tot_bunch - aef_tot_annual, "tax": (aef_tot_bunch - aef_tot_annual) * 0.24,
                        "alt_if_annual_gifts_direct_cash_with_170p": {"total_annual": aef_tot_annual_direct_170p,
                                                                      "addl": aef_tot_bunch - aef_tot_annual_direct_170p,
                                                                      "tax": (aef_tot_bunch - aef_tot_annual_direct_170p) * 0.24}}},
        {"id": "FC-EX1", "sponsor": "Fidelity Charitable", "stated": {"saving_per_1000_37pct": 350, "before": 370},
         "recomputed": {"saving_per_1000_37pct": 1000 * 0.37 * (1 - 2 / 37), "before": 370}},
        {"id": "FC-EX2", "sponsor": "Fidelity Charitable (advisor deck)", "stated": {"deductible": 187500, "saving_before": 74000, "saving_after": 65600},
         "recomputed": {"deductible": 200000 - floor_amt(2_500_000), "saving_before": 200000 * 0.37, "saving_after": fid_deck_after}},
        {"id": "FLOOR-EX", "sponsor": "various", "stated": {"300k": 1500, "200k": 1000, "1m": 5000, "500k[S]": 2500},
         "recomputed": {"300k": floor_amt(300000), "200k": floor_amt(200000), "1m": floor_amt(1_000_000), "500k[S]": floor_amt(500000)}},
        {"id": "SCH-EX1", "sponsor": "DAFgiving360", "stated": {"saving_10k_37pct": 3500, "before": 3700},
         "recomputed": {"saving_10k_37pct": 10000 * 0.35, "before": 3700}},
    ]


PROFILES = {  # repo H1-H3 inputs (direction-donor-tax-scenarios-2026.md s.2.1)
    "H1": {"agi": 90000, "rate": 0.12, "gift": 2000, "other": 12000},
    "H2": {"agi": 300000, "rate": 0.24, "gift": 10000, "other": 25000},
    "H3": {"agi": 1000000, "rate": 0.37, "gift": 50000, "other": 40000},
}


def repo_totals(root):
    path = os.path.join(root, "data/mission-2026-11-14/donor-tax-scenarios-2026.csv")
    rows = [r for r in csv.DictReader(open(path)) if r["row"] == "total" and r["profile"] in PROFILES and r["asset"] == "cash"]
    return {f'{r["profile"]}|{r["vehicle"]}|{r["timing"]}': float(r["tax_saving_vs_no_gift"]) for r in rows}


def calculator_vs_repo(root):
    rep = repo_totals(root)
    def one(pid, p):
        vg_annual = 3 * vanguard_calc(p["agi"], p["rate"], p["gift"], p["other"])
        vg_bunch = vanguard_calc(p["agi"], p["rate"], 3 * p["gift"], p["other"]) + 2 * vanguard_calc(p["agi"], p["rate"], 0, p["other"])
        sc = schwab_bunching_calc(p["rate"], p["other"], p["gift"])
        return {"profile": pid,
                "repo_daf_annual_3yr": rep[f"{pid}|daf|annual"], "repo_daf_bunched_3yr": rep[f"{pid}|daf|bunched_y1"],
                "repo_direct_cash_annual_3yr": rep[f"{pid}|direct|annual"],
                "vanguard_calc_annual_3yr": vg_annual, "vanguard_calc_bunched_3yr": vg_bunch,
                "schwab_calc_annual_3yr": sc["annual_saving_3yr"], "schwab_calc_bunched_3yr": sc["bunched_3yr_saving"],
                "schwab_calc_bunch_addl": sc["bunch_addl_tax_saving"],
                "simple_statute_daf_annual_3yr": 3 * statute_gift_saving_itemizer(p["agi"], p["rate"], p["gift"], p["other"])}
    return [one(k, v) for k, v in PROFILES.items()]


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps({"worked_examples": worked_examples(), "calculators_vs_repo": calculator_vs_repo(root)}, indent=1))
