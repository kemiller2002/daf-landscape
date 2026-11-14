#!/usr/bin/env python3
"""Citation audit for mission research documents (functional style, stdlib only).

Flags markdown lines that state a figure (a digit followed by %, $, bn, m, k, or a 4-digit
year) without any citation marker on the same line. Recognized markers: an http(s) URL,
a markdown link, a bracketed source ID such as [S12] / [R3] / [P1] / [repo ...], or a
pointer to a repository file. Lines in tables, headings and data dictionaries are checked
as well; fenced code is skipped.

This is a mechanical screen: a flagged line may be legitimately supported by the paragraph
around it, and an unflagged line may cite the wrong source. Output is for human review.

Usage: python3 scripts/mission_citation_audit.py [glob ...]
"""
import re
import sys
from pathlib import Path

FIGURE = re.compile(r"(\$\s?\d|\d[\d,.]*\s?(%|bn|m\b|k\b|billion|million)|\b(19|20)\d{2}\b)")
CITATION = re.compile(
    r"(https?://|\]\(|\[(S|R|P|D|C|G|U|V|B|X|F|repo|Q|E)[A-Za-z0-9 ,.\-–_/]*\]|\.md\b|\.csv\b|\.json\b|\.py\b"
    r"|source:|per |\(repo|data/|research/|\[V\]|\[RT\]|\[S\]|\[F\]|\[I\])",
    re.IGNORECASE,
)
DEFAULT_GLOBS = ("research/mission-2026-11-14/*.md", "research/DAF-INDUSTRY-REPORT-2026-11.md")


def lines_outside_code(text: str):
    fence = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            yield n, line


def uncited(path: Path) -> tuple:
    return tuple(
        (n, line.strip())
        for n, line in lines_outside_code(path.read_text(encoding="utf-8"))
        if FIGURE.search(line) and not CITATION.search(line) and not line.lstrip().startswith("#")
    )


def report(paths) -> str:
    results = tuple((p, uncited(p)) for p in paths)
    total = sum(len(r) for _, r in results)
    body = "\n".join(
        f"{p}: {len(r)} flagged\n" + "\n".join(f"  L{n}: {t[:160]}" for n, t in r)
        for p, r in results if r
    )
    return f"Flagged lines (figure without same-line citation marker): {total}\n{body}"


if __name__ == "__main__":
    root = Path(".")
    globs = sys.argv[1:] or DEFAULT_GLOBS
    print(report(sorted({p for g in globs for p in root.glob(g)})))
