#!/usr/bin/env python3
"""Transparent opportunity scoring with sensitivity analysis (functional style, stdlib only).

Inputs (data/commercial-opportunity/):
  opportunity-scores.csv   one row per opportunity; 1-5 judgement per criterion, plus a short
                           evidence pointer per criterion in <criterion>_basis columns.
  scoring-weights.csv      named weight scenarios (scenario, criterion, weight).

Criteria are scored 1-5 where 5 is always *better for Echelon Foundry*. Criteria that are
naturally "bad when high" (competitive intensity, delivery complexity, regulatory/reputational
risk, uncertainty, time to first revenue) are therefore entered already inverted, and the CSV
column names say so (e.g. low_competitive_intensity).

Outputs (printed, and written next to the inputs):
  opportunity-ranking.csv      score and rank under every weight scenario
  opportunity-sensitivity.csv  rank range under (a) every scenario, (b) each criterion weight
                               doubled or zeroed one at a time, (c) every single score moved +/-1.

No probabilities are produced. Scores are judgements recorded so a reviewer can dispute them
line by line; the sensitivity output shows which conclusions depend on which judgements.
Usage: python3 -I scripts/commercial_opportunity_scoring.py [data_dir]
"""
import csv
import sys
from functools import reduce
from pathlib import Path

CRITERIA = (
    "customer_evidence", "economic_value", "budget_accessibility", "buyer_urgency",
    "low_competitive_intensity", "ease_of_reaching_buyers", "capability_fit",
    "fast_time_to_revenue", "low_delivery_complexity", "recurring_revenue",
    "low_regulatory_reputational_risk", "low_uncertainty",
)


def read_csv(path: Path) -> tuple:
    with path.open(newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def scores_of(row: dict) -> dict:
    return {c: float(row[c]) for c in CRITERIA}


def weights_by_scenario(rows) -> dict:
    return reduce(
        lambda acc, r: {**acc, r["scenario"]: {**acc.get(r["scenario"], {}), r["criterion"]: float(r["weight"])}},
        rows, {})


def total(scores: dict, weights: dict) -> float:
    wsum = sum(weights.get(c, 0.0) for c in CRITERIA)
    return round(sum(scores[c] * weights.get(c, 0.0) for c in CRITERIA) / wsum, 3) if wsum else 0.0


def ranks(table: dict, weights: dict) -> dict:
    ordered = sorted(table, key=lambda k: (-total(table[k], weights), k))
    return {k: i + 1 for i, k in enumerate(ordered)}


def weight_variants(base: dict) -> tuple:
    doubled = tuple((f"{c} x2", {**base, c: base.get(c, 0) * 2}) for c in CRITERIA)
    zeroed = tuple((f"{c} x0", {**base, c: 0.0}) for c in CRITERIA)
    return doubled + zeroed


def score_variants(table: dict) -> tuple:
    return tuple(
        (f"{k}.{c} {d:+d}", {**table, k: {**table[k], c: min(5.0, max(1.0, table[k][c] + d))}})
        for k in table for c in CRITERIA for d in (-1, 1)
    )


def write(path: Path, header, rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def main(data_dir: Path) -> int:
    opp = read_csv(data_dir / "opportunity-scores.csv")
    table = {r["opportunity_id"]: scores_of(r) for r in opp}
    names = {r["opportunity_id"]: r["opportunity"] for r in opp}
    scen = weights_by_scenario(read_csv(data_dir / "scoring-weights.csv"))
    base = scen["base"]

    scen_ranks = {s: ranks(table, w) for s, w in scen.items()}
    wvar = tuple(ranks(table, w) for _, w in weight_variants(base))
    svar = tuple(ranks(t, base) for _, t in score_variants(table))

    write(data_dir / "opportunity-ranking.csv",
          ["opportunity_id", "opportunity"] + [f"{s}_score" for s in scen] + [f"{s}_rank" for s in scen],
          [[k, names[k]] + [total(table[k], scen[s]) for s in scen] + [scen_ranks[s][k] for s in scen]
           for k in sorted(table, key=lambda k: scen_ranks["base"][k])])

    def span(rs, k):
        vals = tuple(r[k] for r in rs)
        return min(vals), max(vals)

    sens = [[k, names[k], scen_ranks["base"][k], *span(scen_ranks.values(), k), *span(wvar, k), *span(svar, k),
             sum(1 for r in svar if r[k] <= 3), len(svar)]
            for k in sorted(table, key=lambda k: scen_ranks["base"][k])]
    write(data_dir / "opportunity-sensitivity.csv",
          ["opportunity_id", "opportunity", "base_rank", "scenario_best", "scenario_worst",
           "weight_perturb_best", "weight_perturb_worst", "score_perturb_best", "score_perturb_worst",
           "score_perturbations_in_top3", "score_perturbations_total"], sens)

    print("Base ranking:")
    print("\n".join(f"  {scen_ranks['base'][k]:>2}. {names[k]} ({total(table[k], base)})"
                    for k in sorted(table, key=lambda k: scen_ranks['base'][k])))
    print("Rank ranges (scenarios | weight x2/x0 | score +/-1; top-3 share under score perturbation):")
    print("\n".join(f"  {r[1][:48]:<48} {r[3]}-{r[4]} | {r[5]}-{r[6]} | {r[7]}-{r[8]} | {r[9]}/{r[10]}" for r in sens))
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else "data/commercial-opportunity")))
