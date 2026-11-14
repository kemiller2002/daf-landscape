#!/usr/bin/env python3
"""Repository research inventory (functional style, stdlib only).

Scans research/**/*.md, docs/*.md and data/**/*.csv and reports:
  * document and dataset counts, word counts, row counts
  * unique cited URLs and unique cited domains (a proxy for "sources reviewed";
    a URL cited is not proof the page was read in full)
  * mentions of a fixed organization list (a proxy for "organizations investigated")

Usage: python3 scripts/mission_inventory.py [repo_root] > data/mission-2026-11-14/repo-inventory.json
The counts are mechanical; they do not judge evidence quality.
"""
import csv
import json
import re
import sys
from functools import reduce
from pathlib import Path
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s)\]>\"'`,;|]+")

ORGANIZATIONS = (
    "Ren", "RenPSG", "Renaissance Charitable", "TIFIN", "GiveClear", "Chariot", "Daffy",
    "Charityvest", "Vennfi", "Foundation Source", "Fidelity Charitable", "DAFgiving360",
    "Schwab Charitable", "Vanguard Charitable", "National Philanthropic Trust", "American Endowment Foundation",
    "National Christian Foundation", "Edward Jones", "Morgan Stanley", "Goldman Sachs", "Bank of America",
    "Merrill", "UBS", "Wells Fargo", "Raymond James", "LPL", "Ameriprise", "J.P. Morgan", "TIAA", "SEI",
    "OneAscent", "Pave", "Givinga", "Stellar", "iPhi", "DonorFirstX", "GivingPoint", "DAF Direct", "Candid",
    "GuideStar", "Groundswell", "GivingIQ", "Givefront", "Benevity", "Blackbaud", "YourCause", "Jewish Communal Fund",
    "Silicon Valley Community Foundation", "ImpactAssets", "DonorsTrust", "Signatry", "National Heritage Foundation",
    "Greater Horizons", "Northern Trust", "BNY", "AssetMark", "Zions", "Blue Trust", "Founders Pledge",
    "Every.org", "PayPal Giving Fund", "Network for Good", "Bonterra", "Foundant", "FIMS", "CSuite", "Altruist",
)

TEXT_GLOBS = ("research/**/*.md", "docs/*.md", "README.md")
DATA_GLOBS = ("data/**/*.csv", "data/**/*.json")


def files(root: Path, globs) -> tuple:
    return tuple(sorted({p for g in globs for p in root.glob(g) if p.is_file()}))


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def urls_in(text: str) -> frozenset:
    return frozenset(u.rstrip(".") for u in URL_RE.findall(text))


def domain(u: str) -> str:
    host = urlparse(u).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def org_hits(text: str) -> frozenset:
    return frozenset(o for o in ORGANIZATIONS if re.search(r"\b" + re.escape(o) + r"\b", text))


def csv_rows(p: Path) -> int:
    if p.suffix != ".csv":
        return 0
    with p.open(encoding="utf-8", errors="replace", newline="") as fh:
        return max(sum(1 for _ in csv.reader(fh)) - 1, 0)


def describe(root: Path, p: Path) -> dict:
    text = read(p)
    return {
        "path": str(p.relative_to(root)),
        "words": len(text.split()),
        "rows": csv_rows(p),
        "urls": sorted(urls_in(text)),
        "orgs": sorted(org_hits(text)),
    }


def union(key: str, records) -> frozenset:
    return reduce(lambda acc, r: acc | frozenset(r[key]), records, frozenset())


def summarize(root: Path) -> dict:
    texts = tuple(describe(root, p) for p in files(root, TEXT_GLOBS))
    datas = tuple(describe(root, p) for p in files(root, DATA_GLOBS))
    all_records = texts + datas
    all_urls = union("urls", all_records)
    orgs = union("orgs", all_records)
    org_doc_counts = {o: sum(1 for r in all_records if o in r["orgs"]) for o in sorted(orgs)}
    return {
        "markdown_documents": len(texts),
        "markdown_words": sum(r["words"] for r in texts),
        "datasets": len(datas),
        "dataset_rows": sum(r["rows"] for r in datas),
        "unique_urls_cited": len(all_urls),
        "unique_domains_cited": len({domain(u) for u in all_urls}),
        "organizations_from_fixed_list_mentioned": len(orgs),
        "organization_file_mentions": org_doc_counts,
        "per_file": [{k: v for k, v in r.items() if k != "urls"} | {"url_count": len(r["urls"])} for r in all_records],
    }


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    json.dump(summarize(root), sys.stdout, indent=2)
