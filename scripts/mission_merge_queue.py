#!/usr/bin/env python3
"""Merge agent queue proposals into the research priority inputs (functional, stdlib only).

Reads data/mission-2026-11-14/queue-proposals-*.csv, drops proposals whose question_id
already exists or whose normalized question text duplicates an existing question, appends
the rest to research-priority-inputs.csv, then re-ranks via mission_prioritize.
"""
import csv
import re
import subprocess
import sys
from pathlib import Path

BASE = ("question_id", "question", "area", "importance", "p_change", "gap", "commercial",
        "availability", "effort", "depends_on", "breadth_gap", "state", "assigned_to", "conclusion_affected")
EXTRA = ("proposed_by", "rationale", "evidence_pointer")


def norm(q: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", q.lower()).strip()


def read(path: Path) -> tuple:
    with path.open(newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def valid(row: dict) -> bool:
    try:
        return all(row.get(k) for k in ("question_id", "question")) and \
            all(1 <= float(row[k]) <= 5 for k in ("importance", "gap", "commercial", "availability", "effort")) and \
            0 <= float(row["p_change"]) <= 1
    except (KeyError, ValueError, TypeError):
        return False


def merge(existing: tuple, proposals: tuple) -> tuple:
    ids = {r["question_id"] for r in existing}
    texts = {norm(r["question"]) for r in existing}
    def step(acc, p):
        kept, seen_ids, seen_texts = acc
        if not valid(p) or p["question_id"] in seen_ids or norm(p["question"]) in seen_texts:
            return acc
        row = {k: (p.get(k) or ("open" if k == "state" else "")) for k in BASE + EXTRA}
        return kept + (row,), seen_ids | {p["question_id"]}, seen_texts | {norm(p["question"])}
    from functools import reduce
    return reduce(step, proposals, ((), ids, texts))[0]


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    d = root / "data" / "mission-2026-11-14"
    inputs = d / "research-priority-inputs.csv"
    existing = read(inputs)
    proposals = tuple(r for f in sorted(d.glob("queue-proposals-*.csv")) for r in read(f))
    added = merge(existing, proposals)
    fields = list(dict.fromkeys(list(existing[0].keys()) + list(EXTRA)))
    with inputs.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows({**{k: "" for k in fields}, **r} for r in existing + added)
    print(f"proposals read: {len(proposals)}; added: {len(added)}")
    subprocess.run([sys.executable, str(root / "scripts" / "mission_prioritize.py"), str(root)], check=True)
