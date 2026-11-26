#!/usr/bin/env python3
"""Validate the DAFCP investigation package (functional style, stdlib only).

Checks
  1. Every CSV in data/dafcp-investigation-2026-11-20/ parses, has a unique id column
     and no empty required fields.
  2. Enumerated columns (tag, epistemic class, confidence, relationship status, coverage
     level, scenario confidence) use only the allowed vocabulary.
  3. Evidence rows tagged [F] or [R] carry an http(s) source URL; excerpts stay short
     (<= 40 words) so no coursework or long copyrighted text is reproduced.
  4. Every evidence_ids reference in the other CSVs resolves to an evidence_register row.
  5. Every relative markdown link in research/dafcp-investigation-2026-11-20/*.md resolves
     to a file in the repository.

Usage: python3 -I scripts/dafcp_validate.py [repo_root]
Exit status 0 only if every check passes. Pure functions; no mutable global state.
"""
import csv
import re
import sys
from functools import reduce
from pathlib import Path

DATA_DIR = "data/dafcp-investigation-2026-11-20"
DOC_DIR = "research/dafcp-investigation-2026-11-20"

CONFIDENCE = frozenset({"Low", "Low-Medium", "Medium", "Medium-High", "High"})
TAGS = frozenset({"F", "R", "I", "X", "S", "U"})
EPISTEMIC = frozenset({
    "verified-fact", "strongly-supported-inference", "working-hypothesis",
    "unsupported-claim", "unknown", "negative-finding",
})
REL_STATUS = frozenset({
    "confirmed-formal", "informal-professional", "unverified-possibility", "searched-none-found",
})
COVERAGE = frozenset({
    "not-mentioned", "mentioned", "tool-demonstrated", "process-redesign-taught", "cannot-determine",
})

# file -> (id column, required columns, {column: allowed values}, evidence-reference column or None)
SPECS = {
    "evidence-register.csv": (
        "evidence_id",
        ("phase", "claim", "evidence_type", "tag", "epistemic_class", "confidence", "observed_on"),
        {"tag": TAGS, "epistemic_class": EPISTEMIC, "confidence": CONFIDENCE},
        None,
    ),
    "relationship-map.csv": (
        "rel_id",
        ("organization", "org_type", "relationship_type", "status", "evidence_ids"),
        {"status": REL_STATUS},
        "evidence_ids",
    ),
    "curriculum-audit.csv": (
        "row_id",
        ("module", "dimension", "finding", "assessability", "evidence_ids"),
        {"assessability": frozenset({"public-text-supports", "inferable", "cannot-assess"})},
        "evidence_ids",
    ),
    "ai-technology-coverage.csv": (
        "row_id",
        ("capability", "coverage_level", "evidence_ids"),
        {"coverage_level": COVERAGE},
        "evidence_ids",
    ),
    "credential-comparison.csv": (
        "row_id",
        ("credential", "issuer", "dimension", "value", "evidence_ids"),
        {},
        "evidence_ids",
    ),
    "adoption-evidence.csv": (
        "row_id",
        ("measure", "finding", "evidence_ids"),
        {},
        "evidence_ids",
    ),
    "scenarios.csv": (
        "scenario_id",
        ("scenario", "leading_indicators", "qualitative_confidence"),
        {"qualitative_confidence": CONFIDENCE},
        "evidence_ids",
    ),
    "faculty-affiliations.csv": (
        "row_id",
        ("name_as_printed", "current_affiliation", "affiliation_class", "sponsor_tie_status", "tag", "confidence", "evidence_ids"),
        {"tag": TAGS, "confidence": CONFIDENCE},
        "evidence_ids",
    ),
    "legal-baseline.csv": (
        "row_id",
        ("topic", "authority", "status_class", "key_point", "tag"),
        {"tag": TAGS},
        None,
    ),
    "open-questions.csv": (
        "question_id",
        ("question", "why_it_matters", "could_change", "priority", "route"),
        {"priority": frozenset({"1", "2", "3"})},
        None,
    ),
}

LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def read_rows(path: Path) -> tuple:
    with path.open(newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def split_ids(cell: str) -> tuple:
    return tuple(x.strip() for x in (cell or "").split(";") if x.strip())


def check_table(name: str, rows: tuple, evidence_ids: frozenset) -> tuple:
    id_col, required, enums, ref_col = SPECS[name]
    ids = tuple(r.get(id_col, "") for r in rows)
    dupes = tuple(sorted({i for i in ids if ids.count(i) > 1}))
    missing = tuple(
        f"{name}:{r.get(id_col)}: empty {c}"
        for r in rows for c in (id_col,) + required if not (r.get(c) or "").strip()
    )
    bad_enum = tuple(
        f"{name}:{r.get(id_col)}: {c}={r.get(c)!r} not in vocabulary"
        for r in rows for c, allowed in enums.items() if (r.get(c) or "").strip() not in allowed
    )
    bad_refs = tuple(
        f"{name}:{r.get(id_col)}: unknown evidence id {e}"
        for r in rows if ref_col for e in split_ids(r.get(ref_col, "")) if e not in evidence_ids
    )
    return tuple(f"{name}: duplicate id {d}" for d in dupes) + missing + bad_enum + bad_refs


def check_evidence_specifics(rows: tuple) -> tuple:
    no_url = tuple(
        f"evidence-register.csv:{r['evidence_id']}: tag {r['tag']} needs an http(s) source_url"
        for r in rows
        if r.get("tag") in {"F", "R"} and not (r.get("source_url") or "").startswith("http")
    )
    long_excerpt = tuple(
        f"evidence-register.csv:{r['evidence_id']}: excerpt over 40 words"
        for r in rows if len((r.get("excerpt") or "").split()) > 40
    )
    return no_url + long_excerpt


def check_links(root: Path) -> tuple:
    docs = tuple(sorted((root / DOC_DIR).glob("*.md")))
    return tuple(
        f"{d.relative_to(root)}: broken link {target}"
        for d in docs
        for target in LINK.findall(d.read_text(encoding="utf-8"))
        if not target.startswith(("http://", "https://", "mailto:"))
        and not (d.parent / target).resolve().exists()
    )


def main(root: Path) -> int:
    data = root / DATA_DIR
    tables = {name: read_rows(data / name) for name in SPECS if (data / name).exists()}
    absent = tuple(f"missing file {DATA_DIR}/{n}" for n in SPECS if n not in tables)
    evidence = tables.get("evidence-register.csv", ())
    evidence_ids = frozenset(r["evidence_id"] for r in evidence)
    errors = reduce(
        lambda acc, item: acc + check_table(item[0], item[1], evidence_ids),
        tables.items(),
        absent,
    ) + check_evidence_specifics(evidence) + check_links(root)
    counts = ", ".join(f"{n}={len(rows)}" for n, rows in sorted(tables.items()))
    print(f"Rows: {counts}")
    print("\n".join(errors) if errors else "All DAFCP package checks passed.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
