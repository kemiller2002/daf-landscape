#!/usr/bin/env python3
"""Build the mission's combined evidence and assumptions registers from the research passes.

Inputs: data/commercial-opportunity/ai-native-capital-minimization/pass-evidence/<group>-{evidence,assumptions}.jsonl.
Outputs: evidence-register.csv and assumptions-register.csv in the same data directory. Local checkout paths are
rewritten to repository-qualified paths (e.g. `unbound:requirements/...`, `praxis:src/...`). Deterministic; pure
functions except main().

    python3 -I -B research/commercial-opportunity/ai-native-capital-minimization/scripts/build_registers.py .
"""
import csv
import io
import json
import re
import sys
from pathlib import Path

DATA = Path("data/commercial-opportunity/ai-native-capital-minimization")
GROUPS = ("dev", "ops", "com", "lyr", "adv")

EVIDENCE_FIELDS = ("evidence_id", "pass", "claim", "value", "unit", "source_url_or_path", "source_type",
                   "filing_period", "accessed", "quality", "notes")
ASSUMPTION_FIELDS = ("assumption_id", "pass", "statement", "value", "unit", "low", "high", "basis", "evidence_ids",
                     "sensitivity")

REWRITES = (
    (re.compile(r"/home/user/daf-landscape/"), ""),
    (re.compile(r"/home/user/unbound/"), "unbound:"),
    (re.compile(r"/home/user/echelon-components/([A-Za-z0-9_.-]+)/?"), r"\1:"),
    (re.compile(r"/home/user/Echelon-AI-Native-Enterprise-Design-Framework/?"), "Echelon-AI-Native-Enterprise-Design-Framework:"),
    (re.compile(r"/home/user/AI-Engineering/?"), "AI-Engineering:"),
    (re.compile(r"/home/user/clarity-framework/?"), "clarity-framework:"),
    (re.compile(r"/home/user/kemiller2002/echelon-diagnostic-framework/?"), "echelon-diagnostic-framework:"),
    (re.compile(r"/tmp/claude-0/[^ ;,\"]*/scratchpad/aincm/"), "scratch:aincm/"),
    (re.compile(r"/home/user/echelon-components/"), "echelon-components/"),
    (re.compile(r"/home/user/"), ""),
)


def rewrite(text):
    out = str(text)
    for pattern, replacement in REWRITES:
        out = pattern.sub(replacement, out)
    return out


def read_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def flatten(value):
    return "; ".join(map(str, value)) if isinstance(value, list) else ("" if value is None else str(value))


def to_row(record, group, fields):
    return {f: rewrite(flatten(group.upper() if f == "pass" else record.get(f, ""))) for f in fields}


def register(root, kind, fields):
    rows = [to_row(r, g, fields) for g in GROUPS for r in read_jsonl(root / DATA / "pass-evidence" / f"{g}-{kind}.jsonl")]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue(), len(rows)


def normalise_files(root):
    """Rewrite local checkout paths in the copied pass datasets (text otherwise unchanged)."""
    paths = [p for pattern in ("*.csv", "*.json", "pass-reports/*.jsonl", "pass-evidence/*.jsonl", "build-logs/*")
             for p in sorted((root / DATA).glob(pattern))]
    changed = [p for p in paths if rewrite(p.read_text(encoding="utf-8")) != p.read_text(encoding="utf-8")]
    for p in changed:
        p.write_text(rewrite(p.read_text(encoding="utf-8")), encoding="utf-8")
    return len(changed)


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else ".")
    print(f"normalised {normalise_files(root)} files")
    for name, kind, fields in (("evidence-register.csv", "evidence", EVIDENCE_FIELDS),
                               ("assumptions-register.csv", "assumptions", ASSUMPTION_FIELDS)):
        text, count = register(root, kind, fields)
        (root / DATA / name).write_text(text, encoding="utf-8")
        print(f"{name}: {count} rows")


if __name__ == "__main__":
    main(sys.argv)
