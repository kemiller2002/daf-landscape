#!/usr/bin/env python3
"""Expected-information-value ranking of outstanding research questions (functional, stdlib only).

Input : data/mission-2026-11-14/research-priority-inputs.csv
Output: data/mission-2026-11-14/research-priority-queue.csv (ranked)

Score (documented, deliberately simple and auditable):
    eiv = importance * p_change * gap * commercial * availability / effort
    breadth_bonus: x1.25 when the question covers an entity/segment whose coverage
                   matrix cells are majority "Not investigated" (to keep breadth).
    dependency penalty: x0.6 when a listed dependency is still open (not 'done').
Scales: importance, gap, commercial, availability, effort are 1-5; p_change is 0-1.
The inputs are judgements, recorded so that a reviewer can dispute them line by line.
"""
import csv
import sys
from pathlib import Path

NUMERIC = ("importance", "p_change", "gap", "commercial", "availability", "effort")


def parse(row: dict) -> dict:
    return {**row, **{k: float(row[k]) for k in NUMERIC}}


def open_ids(rows) -> frozenset:
    return frozenset(r["question_id"] for r in rows if r.get("state", "open") != "done")


def score(row: dict, still_open: frozenset) -> dict:
    base = (row["importance"] * row["p_change"] * row["gap"] * row["commercial"] * row["availability"]
            / row["effort"])
    deps = tuple(d for d in row.get("depends_on", "").split(";") if d)
    dep_factor = 0.6 if any(d in still_open for d in deps) else 1.0
    breadth = 1.25 if row.get("breadth_gap", "").lower() == "yes" else 1.0
    return {**row, "eiv_score": round(base * dep_factor * breadth, 2),
            "dependency_factor": dep_factor, "breadth_factor": breadth}


def rank(rows) -> tuple:
    still_open = open_ids(rows)
    scored = sorted((score(r, still_open) for r in rows), key=lambda r: (r.get("state") == "done", -r["eiv_score"]))
    return tuple({**r, "rank": i + 1} for i, r in enumerate(scored))


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    d = root / "data" / "mission-2026-11-14"
    with (d / "research-priority-inputs.csv").open(newline="", encoding="utf-8") as fh:
        rows = tuple(parse(r) for r in csv.DictReader(fh))
    ranked = rank(rows)
    with (d / "research-priority-queue.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["rank", "eiv_score", *[k for k in ranked[0] if k not in ("rank", "eiv_score")]])
        w.writeheader()
        w.writerows(ranked)
    for r in ranked[:15]:
        print(f'{r["rank"]:>2} {r["eiv_score"]:>7} {r["question_id"]} [{r.get("state")}] {r["question"][:90]}')
