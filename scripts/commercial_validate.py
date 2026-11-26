#!/usr/bin/env python3
"""Validate the commercial-opportunity package (functional style, stdlib only).

Checks
  1. Prospect CSVs: required columns present and non-empty; unique prospect_id across files;
     confidence uses the EDF labels; every row cites at least one source: a URL or a repository path.
  2. Named-person rule: a named_decision_makers cell either declines to name ("None", "Not
     verified", "Programme director …") or carries an [F …] first-party tag.
  3. opportunity-scores.csv: every criterion in 1..5; every row has a basis.
  4. Markdown under research/commercial-opportunity: relative links resolve; no scratchpad
     or /tmp paths leak into the repository.
Usage: python3 -I scripts/commercial_validate.py [repo_root]
"""
import csv
import re
import sys
from pathlib import Path

DATA = "data/commercial-opportunity"
DOCS = "research/commercial-opportunity"
PROSPECT_FILES = ("prospects-sponsors.csv", "prospects-wealth.csv", "prospects-other.csv")
REQUIRED = ("prospect_id", "organization", "segment", "opportunity_hypothesis", "supporting_evidence",
            "contradictory_evidence", "confidence", "sources", "next_validation_action")
CONF = re.compile(r"^(Low|Low-Medium|Medium|Medium-High|High)\b")
DECLINE = re.compile(r"^(None|Not verified|Programme director|Program director)", re.I)
CRITERIA = ("customer_evidence", "economic_value", "budget_accessibility", "buyer_urgency",
            "low_competitive_intensity", "ease_of_reaching_buyers", "capability_fit",
            "fast_time_to_revenue", "low_delivery_complexity", "recurring_revenue",
            "low_regulatory_reputational_risk", "low_uncertainty")
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def rows(path: Path) -> tuple:
    with path.open(newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def prospect_errors(name: str, rs: tuple) -> tuple:
    missing_cols = tuple(f"{name}: missing column {c}" for c in REQUIRED if rs and c not in rs[0])
    empty = tuple(f"{name}:{r.get('prospect_id')}: empty {c}" for r in rs for c in REQUIRED
                  if c in r and not (r[c] or "").strip())
    conf = tuple(f"{name}:{r['prospect_id']}: confidence {r['confidence']!r}" for r in rs
                 if not CONF.match((r.get("confidence") or "").strip()))
    src = tuple(f"{name}:{r['prospect_id']}: no source (URL or repository path)" for r in rs
                if not re.search(r"https?://|research/|data/", r.get("sources") or ""))
    named = tuple(f"{name}:{r['prospect_id']}: named person without [F] tag" for r in rs
                  if (r.get("named_decision_makers") or "").strip()
                  and not DECLINE.match(r["named_decision_makers"].strip())
                  and "[F" not in r["named_decision_makers"])
    return missing_cols + empty + conf + src + named


def score_errors(rs: tuple) -> tuple:
    bad = tuple(f"opportunity-scores.csv:{r['opportunity_id']}: {c}={r[c]}" for r in rs for c in CRITERIA
                if not r.get(c, "").replace(".", "", 1).isdigit() or not 1 <= float(r[c]) <= 5)
    basis = tuple(f"opportunity-scores.csv:{r['opportunity_id']}: empty basis" for r in rs if not r.get("basis", "").strip())
    return bad + basis


def doc_errors(root: Path) -> tuple:
    docs = tuple(sorted((root / DOCS).rglob("*.md")))
    links = tuple(f"{d.relative_to(root)}: broken link {t}" for d in docs
                  for t in LINK.findall(d.read_text(encoding="utf-8"))
                  if not t.startswith(("http://", "https://", "mailto:")) and not (d.parent / t).resolve().exists())
    leaks = tuple(f"{p.relative_to(root)}: scratchpad path" for p in docs + tuple((root / DATA).glob("*.csv"))
                  if "/tmp/claude" in p.read_text(encoding="utf-8"))
    return links + leaks


def main(root: Path) -> int:
    data = root / DATA
    prospects = {n: rows(data / n) for n in PROSPECT_FILES if (data / n).exists()}
    absent = tuple(f"missing {DATA}/{n}" for n in PROSPECT_FILES if n not in prospects)
    ids = [r["prospect_id"] for rs in prospects.values() for r in rs]
    dupes = tuple(f"duplicate prospect_id {i}" for i in sorted({i for i in ids if ids.count(i) > 1}))
    errs = (absent + dupes
            + tuple(e for n, rs in prospects.items() for e in prospect_errors(n, rs))
            + score_errors(rows(data / "opportunity-scores.csv"))
            + doc_errors(root))
    print(f"Prospects: {len(ids)} rows in {len(prospects)} files")
    print("\n".join(errs) if errs else "All commercial-opportunity package checks passed.")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
