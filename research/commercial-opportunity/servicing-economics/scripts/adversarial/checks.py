"""ADV reproducibility checks. Run: python3 -I -B checks.py <daf-landscape root>
Pure functions; prints a JSON dict of every derived number quoted in the ADV report (EV-ADV-*)."""
import csv
import json
import statistics
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from port import MODEL_B, equal, evaluate  # noqa: E402

GRID = tuple(i * 1e7 for i in range(1, 2001))


def sustained_breakeven(org, n=5, b=150000.0, ap="nat", bps=20.0, target=0.0):
    flags = tuple(evaluate(org, ap, bps, equal(n, a, b))["margin"] >= target for a in GRID)
    if not flags[-1]:
        return None
    i = len(flags) - 1
    while i > 0 and flags[i - 1]:
        i -= 1
    return GRID[i]


def latest_cost_rows(path):
    rows = {}
    for r in csv.DictReader(open(path)):
        if r["ein"] not in rows or r["fiscal_year"] > rows[r["ein"]]["fiscal_year"]:
            rows[r["ein"]] = r
    return rows


def fee_vs_sponsor(rows, model, cost):
    out = []
    for t in rows:
        m = model.get(t["ein"].zfill(9))
        c = cost.get(t["ein"].zfill(9))
        if not m or not c or not c["operating_cost_ex_invest_mgmt"]:
            continue
        fee = float(m["fee_20bps"])
        out.append({"name": m["name"], "usd_per_account": fee / float(m["accounts_for_cost"]),
                    "fee_pct_opex": 100 * fee / float(c["operating_cost_ex_invest_mgmt"])})
    return out


def main(root):
    root = Path(root)
    se = root / "data/commercial-opportunity/servicing-economics"
    model = {r["ein"]: r for r in csv.DictReader(open(se / "sponsor-model-economics.csv"))}
    cost = latest_cost_rows(root / "data/mission-2026-11-14/sponsor-cost-structure.csv")
    top = fee_vs_sponsor(list(csv.DictReader(open(se / "top25-hypotheses.csv"))), model, cost)
    ss = fee_vs_sponsor(list(csv.DictReader(open(se / "self-sustaining-candidates.csv"))), model, cost)
    fixed = 1.64e6 + 99478.0
    active = [r for r in model.values() if r["status"] == "active" and r["captive_status"] == "none_found"]

    def covers(price_per_acct):
        return sorted(r["name"] for r in active
                      if min(float(r["accounts_for_cost"]) * price_per_acct, float(r["fee_20bps"]))
                      - float(r["annual_cost_ai_native_base"]) >= fixed)

    base = evaluate(MODEL_B, "nat", 20, equal(5, 1.5e9, 150000))
    out = {
        "port_base_profit_5x1.5B_150k": base["profit"],
        "port_base_peak_cost": base["peak"],
        "profit_ph1360": evaluate(replace(MODEL_B, ph=1360.0, hourly=99478.0 / 1360), "nat", 20, equal(5, 1.5e9, 150000))["profit"],
        "total_cost_af1.0": base["total"],
        "total_cost_af0.6": evaluate(MODEL_B, "nat", 20, equal(5, 1.5e9, 150000), asset_factor=0.6)["total"],
        "effective_bps_floor250": {b: evaluate(MODEL_B, "nat", 20, equal(5, 1.5e9, b), per_acct_floor=250)["rev"] / 1.5e9 * 1e4
                                   for b in (75000, 150000, 300000)},
        "breakeven_150k": {label: sustained_breakeven(replace(MODEL_B, nonpersonnel=MODEL_B.nonpersonnel + x))
                           for label, x in (("as_modelled", 0), ("build_0.72M_5y", 144000), ("unbound_build_5M_5y", 1e6),
                                            ("sales_250k", 250000), ("build_1M_plus_sales_0.25M", 1.25e6))},
        "breakeven_150k_ai_enhanced": sustained_breakeven(MODEL_B, ap="enh"),
        "breakeven_150k_ph1360": sustained_breakeven(replace(MODEL_B, ph=1360.0, hourly=99478.0 / 1360)),
        "strategy_runrate_profit": {
            "C_as_modelled": evaluate(MODEL_B, "nat", 20, ((5000, 300000), (2500, 200000), (2500, 200000)))["profit"],
            "C_anchor_at_200k": evaluate(MODEL_B, "nat", 20, ((7500, 200000), (2500, 200000), (2500, 200000)))["profit"],
            "D_as_modelled": evaluate(MODEL_B, "nat", 20, tuple((1500, 200000) for _ in range(6)))["profit"],
            "D_at_300k": evaluate(MODEL_B, "nat", 20, tuple((1000, 300000) for _ in range(6)))["profit"],
            "C_without_anchor": evaluate(MODEL_B, "nat", 20, ((2500, 200000), (2500, 200000)))["profit"],
            "anchor_alone": evaluate(MODEL_B, "nat", 20, ((5000, 300000),))["profit"],
            "anchor_alone_ai_enhanced": evaluate(MODEL_B, "enh", 20, ((5000, 300000),))["profit"],
            "anchor_alone_minus30pct": evaluate(MODEL_B, "nat", 20, ((5000, 210000),))["profit"],
        },
        "top25_median_usd_per_account_20bps": statistics.median(x["usd_per_account"] for x in top),
        "top25_median_fee_pct_sponsor_opex_ex_invest": statistics.median(x["fee_pct_opex"] for x in top),
        "selfsustain_median_fee_pct_sponsor_opex_ex_invest": statistics.median(x["fee_pct_opex"] for x in ss),
        "selfsustain_rows_over_50pct": sorted((x["name"], round(x["fee_pct_opex"])) for x in ss if x["fee_pct_opex"] > 50),
        "covers_fixed_at_20bps": len([r for r in active if float(r["contribution_20bps_base"]) >= fixed]),
        "covers_fixed_lesser_20bps_or_737": covers(737.0),
        "covers_fixed_lesser_20bps_or_400": covers(400.0),
    }
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/home/user/daf-landscape")
