#!/usr/bin/env python3
"""Merge the per-agent source fragments (data/sources-*.csv) into data/source-register.csv
and validate citations in the package markdown.

Pure functions over immutable tuples; file I/O only in main().

Checks (exit 1 on any error):
  S1  every fragment has the canonical header
  S2  source IDs are unique across fragments and match <CODE>-NNN
  S3  every [CODE-NNN] citation in a package .md file resolves to a registered source
  S4  every source has a URL, evidence class and access date
Warnings (reported, not failing): sources never cited in any markdown file.

Usage:
  python3 -I scripts/merge_source_register.py            write data/source-register.csv and data/source-register-stats.json
  python3 -I scripts/merge_source_register.py --check    fail if the written files are stale
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence, Tuple

HEADER = ("source_id", "title", "publisher", "url", "publication_date", "access_date", "source_type",
          "evidence_class", "excerpt", "used_in", "confidence", "limitations")
ID = re.compile(r"^[A-Z]{3,4}-\d{3}$")
CITE = re.compile(r"\[((?:[A-Z]{3,4}-\d{3})(?:\s*[,;]\s*[A-Z]{3,4}-\d{3})*)\]")
Row = Mapping[str, str]


def parse_fragment(name: str, text: str) -> Tuple[Tuple[str, ...], Tuple[Row, ...]]:
    rows = tuple(csv.reader(io.StringIO(text)))
    header = tuple(rows[0]) if rows else ()
    body = tuple({**dict(zip(HEADER, r)), "fragment": name} for r in rows[1:] if any(c.strip() for c in r))
    return header, body


def citations(text: str) -> Tuple[str, ...]:
    return tuple(i.strip() for group in CITE.findall(text) for i in re.split(r"[,;]", group))


def check_headers(fragments: Sequence[Tuple[str, Tuple[str, ...]]]) -> Tuple[str, ...]:
    return tuple(f"S1 {name} header differs" for name, header in fragments if header != HEADER)


def check_ids(rows: Sequence[Row]) -> Tuple[str, ...]:
    counts = Counter(r["source_id"] for r in rows)
    return tuple(f"S2 malformed id {r['source_id']} in {r['fragment']}" for r in rows if not ID.match(r["source_id"])) + \
        tuple(f"S2 duplicate id {i}" for i, n in sorted(counts.items()) if n > 1)


def check_citations(cited: Mapping[str, Tuple[str, ...]], known: frozenset) -> Tuple[str, ...]:
    return tuple(f"S3 {doc} cites unknown source {c}" for doc, cs in sorted(cited.items()) for c in sorted(set(cs))
                 if c not in known)


def check_fields(rows: Sequence[Row]) -> Tuple[str, ...]:
    return tuple(f"S4 {r['source_id']} missing {f}" for r in rows for f in ("url", "evidence_class", "access_date")
                 if not (r.get(f) or "").strip())


def render_csv(rows: Sequence[Row]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(HEADER + ("fragment",))
    tuple(writer.writerow(tuple(r.get(k, "") for k in HEADER + ("fragment",))) for r in rows)
    return buf.getvalue()


def stats(rows: Sequence[Row], cited: Mapping[str, Tuple[str, ...]]) -> dict:
    all_cited = frozenset(c for cs in cited.values() for c in cs)
    count = lambda key: dict(sorted(Counter((r.get(key) or "").strip() or "(blank)" for r in rows).items()))
    return {
        "sources": len(rows),
        "by_fragment": count("fragment"),
        "by_source_type": count("source_type"),
        "by_evidence_class": count("evidence_class"),
        "by_confidence": count("confidence"),
        "cited_in_markdown": len([r for r in rows if r["source_id"] in all_cited]),
        "uncited": sorted(r["source_id"] for r in rows if r["source_id"] not in all_cited),
    }


def main(argv: Sequence[str]) -> int:
    pkg = Path(__file__).resolve().parent.parent
    check = "--check" in argv
    fragment_paths = sorted((pkg / "data").glob("sources-*.csv"))
    parsed = tuple((p.stem.replace("sources-", ""), *parse_fragment(p.stem, p.read_text(encoding="utf-8")))
                   for p in fragment_paths)
    rows = tuple(sorted((r for _, _, body in parsed for r in body), key=lambda r: r["source_id"]))
    cited = {p.name: citations(p.read_text(encoding="utf-8")) for p in sorted(pkg.glob("*.md"))}
    known = frozenset(r["source_id"] for r in rows)
    errors = (check_headers(tuple((n, h) for n, h, _ in parsed)) + check_ids(rows)
              + check_citations(cited, known) + check_fields(rows))
    outputs = ((pkg / "data/source-register.csv", render_csv(rows)),
               (pkg / "data/source-register-stats.json", json.dumps(stats(rows, cited), indent=2) + "\n"))
    stale = tuple(f"stale {p.name}" for p, text in outputs
                  if not p.exists() or p.read_text(encoding="utf-8") != text)
    if not check:
        tuple(p.write_text(text, encoding="utf-8") for p, text in outputs)
    report = {"sources": len(rows), "errors": list(errors + (stale if check else ())),
              "uncited": len(stats(rows, cited)["uncited"])}
    print(json.dumps(report, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
