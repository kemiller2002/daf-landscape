"""P-B43N26-03: validate the charity-data terms x AI-use matrix and tally it.

Usage: python3 scripts/mission_b43n26_03_terms_matrix.py .

Reads data/mission-2026-11-14/charity-data-terms-ai-matrix-2026-11-20.csv, checks
the schema and the controlled vocabulary, and prints:
  - the provider x use grid,
  - counts by value (all providers, and commercial providers only),
  - counts of rows with an express clause and with AI/LLM/ML-specific wording.
Pure functions, stdlib only. Exits non-zero if validation fails.
"""
import csv
import os
import sys
from collections import Counter
from functools import reduce

MATRIX = "data/mission-2026-11-14/charity-data-terms-ai-matrix-2026-11-20.csv"
VALUES = ("permitted", "prohibited", "requires-licence", "silent")
USES = ("a", "b", "c", "d")
REQUIRED = ("provider", "use_code", "use", "value", "express_clause", "ai_specific_language",
            "clause_quote", "clause_ref", "document", "url", "effective_date",
            "evidence_label", "evidence_status", "notes")
BASELINE_PREFIX = "IRS"


def load(root):
    with open(os.path.join(root, MATRIX), newline="") as fh:
        return tuple(csv.DictReader(fh))


def row_errors(row):
    checks = (
        (all(k in row for k in REQUIRED), "missing column"),
        (row.get("value") in VALUES, f"bad value {row.get('value')!r}"),
        (row.get("use_code") in USES, f"bad use_code {row.get('use_code')!r}"),
        (row.get("express_clause") in ("yes", "no"), "express_clause not yes/no"),
        (row.get("ai_specific_language") in ("yes", "no"), "ai_specific_language not yes/no"),
        (row.get("evidence_label") in ("F", "C", "I"), "evidence_label not F/C/I"),
        (row.get("evidence_status") in ("read", "partial", "blocked"), "bad evidence_status"),
        (str(row.get("url", "")).startswith("http"), "url missing"),
        (bool(row.get("clause_quote")), "clause_quote empty"),
    )
    return tuple(f"{row.get('provider')}/{row.get('use_code')}: {msg}" for ok, msg in checks if not ok)


def grid_errors(rows):
    keys = tuple((r["provider"], r["use_code"]) for r in rows)
    dupes = tuple(k for k, n in Counter(keys).items() if n > 1)
    providers = tuple(dict.fromkeys(r["provider"] for r in rows))
    missing = tuple((p, u) for p in providers for u in USES if (p, u) not in keys)
    return tuple(f"duplicate {d}" for d in dupes) + tuple(f"missing {m}" for m in missing)


def tally(rows, field):
    return reduce(lambda acc, r: acc + Counter({r[field]: 1}), rows, Counter())


def grid(rows):
    providers = tuple(dict.fromkeys(r["provider"] for r in rows))
    cell = {(r["provider"], r["use_code"]): r["value"] for r in rows}
    head = "provider".ljust(30) + "".join(f"({u})".ljust(18) for u in USES)
    body = tuple(p[:29].ljust(30) + "".join(cell[(p, u)].ljust(18) for u in USES) for p in providers)
    return (head,) + body


def fmt(counter):
    return ", ".join(f"{k}={counter.get(k, 0)}" for k in VALUES)


def main(root):
    rows = load(root)
    errors = tuple(e for r in rows for e in row_errors(r)) + grid_errors(rows)
    commercial = tuple(r for r in rows if not r["provider"].startswith(BASELINE_PREFIX))
    providers = tuple(dict.fromkeys(r["provider"] for r in rows))
    ai_rows = tuple(r for r in rows if r["ai_specific_language"] == "yes")
    lines = (
        f"rows={len(rows)} providers={len(providers)} (commercial={len(providers) - 1})",
        *grid(rows),
        f"all rows: {fmt(tally(rows, 'value'))}",
        f"commercial rows: {fmt(tally(commercial, 'value'))}",
        *(f"commercial use ({u}): {fmt(tally(tuple(r for r in commercial if r['use_code'] == u), 'value'))}" for u in USES),
        f"express_clause=yes (commercial): {sum(r['express_clause'] == 'yes' for r in commercial)}",
        f"ai_specific_language=yes: {len(ai_rows)} -> {[r['provider'] + '/' + r['use_code'] for r in ai_rows]}",
        f"evidence_status (commercial): {dict(tally(commercial, 'evidence_status'))}",
        f"commercial cells where use is permitted without a licence: {sum(r['value'] == 'permitted' for r in commercial)}",
        f"validation errors: {len(errors)}",
        *errors,
    )
    print("\n".join(lines))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
