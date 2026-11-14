#!/usr/bin/env python3
"""Dated text monitor for DAF / foundation vendor and sponsor terms (queue item P-PAY-07).

Stdlib only; functional style (pure transforms, I/O at the edges).

What it does, per URL in the config CSV (default data/mission-2026-11-14/terms-monitor-urls.csv):
  1. fetch the document (HTML, PDF, DOCX, Markdown or plain text);
  2. extract and normalize text (HTML tags/scripts stripped, whitespace collapsed, volatile
     lines such as "Updated 12 minutes ago" dropped, plus any per-row ignore_regex);
  3. store a dated snapshot  data/terms-snapshots/<slug>/<YYYY-MM-DD>.txt
     and its metadata         data/terms-snapshots/<slug>/<YYYY-MM-DD>.meta.json
     (url, final url, HTTP status, content type, raw and text sha256, sizes, extractor, watch-term counts);
  4. compare with the most recent earlier snapshot of the same slug and write a Markdown diff
     report  data/terms-snapshots/reports/<YYYY-MM-DD>-terms-diff.md ;
  5. append one row per URL to data/terms-snapshots/manifest.csv (status log, including fetch failures).

URLs that block or fail are skipped (no snapshot written) and recorded with their status.
Re-running on the same date overwrites that date's snapshot (idempotent).

Watch terms: counts of clause vocabulary relevant to NPact §2.4-style anti-passthrough and
agent-initiation clauses (third party, automated, agent, AI, bot/scrape, initiate, on behalf of,
pass-through, aggregator, API). A change in counts is flagged in the report even if the diff is long.

PDF text uses the `pdftotext` binary (poppler) when present, else a crude stdlib fallback
(FlateDecode streams, Tj/TJ operators) that is good enough for change detection, not for reading.

Usage:
  python3 scripts/mission_terms_monitor.py                       # fetch all, snapshot, report
  python3 scripts/mission_terms_monitor.py --only daffy-mcp-docs # one slug
  python3 scripts/mission_terms_monitor.py --date 2027-02-14     # override snapshot date
  python3 scripts/mission_terms_monitor.py --report-only         # rebuild report from stored snapshots

Suggested cadence: quarterly (P-PAY-07), e.g. a scheduled run in Feb/May/Aug/Nov.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import hashlib
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
import zlib
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, NamedTuple

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "data/mission-2026-11-14/terms-monitor-urls.csv"
DEFAULT_SNAPDIR = ROOT / "data/terms-snapshots"
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36 terms-monitor/1.0")
MAX_BYTES = 25 * 1024 * 1024
DIFF_LINE_CAP = 120

WATCH_TERMS: dict[str, str] = {
    "third_party": r"third[\s-]+part(?:y|ies)",
    "automated": r"\bautomat(?:ed|ic|ion|ically)\b",
    "agent": r"\bagents?\b|\bagentic\b",
    "artificial_intelligence": r"artificial intelligence|\bA\.?I\.?\b|machine learning|large language model|\bLLM",
    "bot_scrape": r"\bbots?\b|scrap(?:e|ing|er)|crawl(?:er|ing)?|spider",
    "initiate": r"\binitiat(?:e|ed|es|ing|ion)\b",
    "on_behalf_of": r"on behalf of",
    "pass_through": r"pass[\s-]?through",
    "aggregator": r"aggregat(?:or|ors|ion|e)",
    "api": r"\bAPIs?\b|application programming interface",
    "mcp": r"model context protocol|\bMCP\b",
}

VOLATILE_LINE_PATTERNS = [
    r"^updated \d+ (?:second|minute|hour|day)s? ago$",
    r"^last updated:? .{0,40}ago$",
    r"^\W*$",
]


class Target(NamedTuple):
    slug: str
    vendor: str
    document: str
    url: str
    format_hint: str
    ignore_regex: str


class Fetched(NamedTuple):
    ok: bool
    status: str          # HTTP code or error class
    final_url: str
    content_type: str
    body: bytes
    error: str


# ----------------------------------------------------------------------------- config

def read_targets(path: Path) -> list[Target]:
    with path.open(newline="", encoding="utf-8") as fh:
        return [Target(r["slug"].strip(), r["vendor"].strip(), r["document"].strip(), r["url"].strip(),
                       (r.get("format_hint") or "").strip().lower(), (r.get("ignore_regex") or "").strip())
                for r in csv.DictReader(fh) if r.get("slug") and r.get("url")]


# ----------------------------------------------------------------------------- fetch (I/O)

def fetch(url: str, timeout: float) -> Fetched:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "text/html,application/pdf,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                return Fetched(False, "too_large", resp.geturl(), resp.headers.get("Content-Type", ""), b"", "body > 25MB")
            return Fetched(True, str(resp.status), resp.geturl(), resp.headers.get("Content-Type", ""), body, "")
    except urllib.error.HTTPError as e:
        return Fetched(False, str(e.code), url, e.headers.get("Content-Type", "") if e.headers else "", b"", str(e.reason))
    except Exception as e:  # network, TLS, timeout
        return Fetched(False, type(e).__name__, url, "", b"", str(e)[:200])


# ----------------------------------------------------------------------------- extraction (pure)

class _TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "head", "template", "iframe"}
    BLOCK = {"p", "div", "br", "li", "ul", "ol", "tr", "td", "th", "table", "section", "article",
             "h1", "h2", "h3", "h4", "h5", "h6", "header", "footer", "nav", "blockquote", "pre", "dd", "dt"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_startendtag(self, tag, attrs):
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth:
            self.skip_depth -= 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip_depth:
            self.parts.append(data)


def html_to_text(raw: bytes) -> str:
    p = _TextExtractor()
    p.feed(raw.decode("utf-8", errors="replace"))
    p.close()
    return "".join(p.parts)


def docx_to_text(raw: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab/>", "\t", xml)
    return html.unescape(re.sub(r"<[^>]+>", "", xml))


def _pdf_fallback(raw: bytes) -> str:
    out: list[str] = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", raw, re.S):
        data = m.group(1)
        try:
            data = zlib.decompress(data)
        except zlib.error:
            pass
        for t in re.finditer(rb"\((?:\\.|[^\\)])*\)\s*Tj|\[(.*?)\]\s*TJ", data, re.S):
            chunk = t.group(0)
            out.append(" ".join(s.decode("latin-1", errors="replace")
                                for s in re.findall(rb"\(((?:\\.|[^\\)])*)\)", chunk)))
        out.append("\n")
    return "".join(out)


def pdf_to_text(raw: bytes) -> tuple[str, str]:
    exe = shutil.which("pdftotext")
    if exe:
        with tempfile.TemporaryDirectory() as td:
            src = Path(td, "in.pdf")
            src.write_bytes(raw)
            res = subprocess.run([exe, "-layout", "-enc", "UTF-8", str(src), "-"],
                                 capture_output=True, timeout=120)
            if res.returncode == 0:
                return res.stdout.decode("utf-8", errors="replace"), "pdftotext"
    return _pdf_fallback(raw), "pdf-stdlib-fallback"


def sniff_format(hint: str, content_type: str, url: str, raw: bytes) -> str:
    ct = content_type.lower()
    if raw[:5] == b"%PDF-" or "pdf" in ct:
        return "pdf"
    if raw[:2] == b"PK" and ("wordprocessingml" in ct or url.lower().endswith(".docx") or hint == "docx"):
        return "docx"
    if "html" in ct or raw.lstrip()[:15].lower().startswith((b"<!doctype html", b"<html")):
        return "html"
    if hint in {"markdown", "text"} or "markdown" in ct or "text/plain" in ct:
        return "text"
    return hint or "html"


def extract_text(fmt: str, raw: bytes) -> tuple[str, str]:
    if fmt == "pdf":
        return pdf_to_text(raw)
    if fmt == "docx":
        return docx_to_text(raw), "docx-xml"
    if fmt == "html":
        return html_to_text(raw), "html-parser"
    return raw.decode("utf-8", errors="replace"), "plain"


def normalize(text: str, ignore_regex: str = "") -> str:
    text = html.unescape(text).replace(" ", " ").replace("​", "")
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[–—]", "-", text)
    pats = [re.compile(p, re.I) for p in VOLATILE_LINE_PATTERNS + ([ignore_regex] if ignore_regex else [])]
    lines = (re.sub(r"[ \t\f\v]+", " ", ln).strip() for ln in text.splitlines())
    kept = [ln for ln in lines if ln and not any(p.search(ln) for p in pats)]
    return "\n".join(kept) + "\n"


def watch_counts(text: str) -> dict[str, int]:
    return {k: len(re.findall(p, text, re.I)) for k, p in WATCH_TERMS.items()}


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ----------------------------------------------------------------------------- snapshots (I/O)

def snapshot_dates(slug_dir: Path) -> list[str]:
    return sorted(p.stem for p in slug_dir.glob("????-??-??.txt")) if slug_dir.exists() else []


def previous_date(slug_dir: Path, date: str) -> str | None:
    earlier = [d for d in snapshot_dates(slug_dir) if d < date]
    return earlier[-1] if earlier else None


def write_snapshot(slug_dir: Path, date: str, text: str, meta: dict) -> None:
    slug_dir.mkdir(parents=True, exist_ok=True)
    (slug_dir / f"{date}.txt").write_text(text, encoding="utf-8")
    (slug_dir / f"{date}.meta.json").write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")


def read_snapshot(slug_dir: Path, date: str) -> tuple[str, dict]:
    meta_p = slug_dir / f"{date}.meta.json"
    meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.exists() else {}
    return (slug_dir / f"{date}.txt").read_text(encoding="utf-8"), meta


# ----------------------------------------------------------------------------- comparison (pure)

def compare(prev_text: str | None, cur_text: str, prev_counts: dict | None, cur_counts: dict) -> dict:
    if prev_text is None:
        return {"state": "baseline", "added": 0, "removed": 0, "diff": [], "count_changes": {}}
    if prev_text == cur_text:
        return {"state": "unchanged", "added": 0, "removed": 0, "diff": [], "count_changes": {}}
    diff = list(difflib.unified_diff(prev_text.splitlines(), cur_text.splitlines(),
                                     "previous", "current", n=1, lineterm=""))
    added = sum(1 for d in diff if d.startswith("+") and not d.startswith("+++"))
    removed = sum(1 for d in diff if d.startswith("-") and not d.startswith("---"))
    pc = prev_counts or {}
    changes = {k: (pc.get(k, 0), v) for k, v in cur_counts.items() if pc.get(k, 0) != v}
    return {"state": "changed", "added": added, "removed": removed, "diff": diff, "count_changes": changes}


def process(target: Target, fetched: Fetched, date: str, snapdir: Path) -> dict:
    """Pure-ish orchestration for one target given an already-fetched response; returns a result row.
    Side effect: writes the snapshot when the fetch succeeded."""
    slug_dir = snapdir / target.slug
    base = {"date": date, "slug": target.slug, "vendor": target.vendor, "url": target.url,
            "final_url": fetched.final_url, "http_status": fetched.status, "error": fetched.error}
    if not fetched.ok:
        return {**base, "outcome": "fetch_failed", "state": "skipped"}
    fmt = sniff_format(target.format_hint, fetched.content_type, fetched.final_url, fetched.body)
    raw_text, extractor = extract_text(fmt, fetched.body)
    text = normalize(raw_text, target.ignore_regex)
    if len(text.strip()) < 200:
        return {**base, "outcome": "too_little_text", "state": "skipped", "format": fmt,
                "extractor": extractor, "text_chars": len(text),
                "error": (fetched.error + " extracted <200 chars (JS-rendered or blocked page?)").strip()}
    counts = watch_counts(text)
    meta = {"slug": target.slug, "vendor": target.vendor, "document": target.document, "url": target.url,
            "final_url": fetched.final_url, "http_status": fetched.status, "content_type": fetched.content_type,
            "format": fmt, "extractor": extractor, "raw_bytes": len(fetched.body),
            "raw_sha256": sha256(fetched.body), "text_chars": len(text),
            "text_sha256": sha256(text.encode("utf-8")), "watch_counts": counts,
            "fetched_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    prev = previous_date(slug_dir, date)
    prev_text, prev_meta = read_snapshot(slug_dir, prev) if prev else (None, {})
    write_snapshot(slug_dir, date, text, meta)
    cmp = compare(prev_text, text, prev_meta.get("watch_counts"), counts)
    return {**base, "outcome": "snapshot_written", "format": fmt, "extractor": extractor,
            "raw_sha256": meta["raw_sha256"], "text_sha256": meta["text_sha256"], "text_chars": len(text),
            "previous_date": prev or "", "watch_counts": counts, **cmp}


# ----------------------------------------------------------------------------- reporting (pure + I/O)

def render_report(date: str, results: list[dict]) -> str:
    n_ok = sum(r["outcome"] == "snapshot_written" for r in results)
    lines = [f"# Terms monitor diff report: {date}", "",
             f"Generated by `scripts/mission_terms_monitor.py`. {len(results)} URLs; {n_ok} snapshots written; "
             f"{len(results) - n_ok} skipped.", "",
             "| slug | vendor | HTTP | outcome | state vs previous | previous | +lines | -lines | text sha256 (12) | watch-count changes |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        cc = "; ".join(f"{k} {a}->{b}" for k, (a, b) in r.get("count_changes", {}).items())
        lines.append(f"| {r['slug']} | {r['vendor']} | {r['http_status']} | {r['outcome']} | {r.get('state','')} | "
                     f"{r.get('previous_date','')} | {r.get('added','')} | {r.get('removed','')} | "
                     f"{r.get('text_sha256','')[:12]} | {cc} |")
    skipped = [r for r in results if r["outcome"] != "snapshot_written"]
    if skipped:
        lines += ["", "## Skipped URLs", ""]
        lines += [f"- `{r['slug']}` {r['url']} -> status `{r['http_status']}`: {r.get('error','')}" for r in skipped]
    lines += ["", "## Watch-term counts (current snapshot)", "",
              "| slug | " + " | ".join(WATCH_TERMS) + " |", "|---|" + "---|" * len(WATCH_TERMS)]
    for r in results:
        if r.get("watch_counts"):
            lines.append(f"| {r['slug']} | " + " | ".join(str(r['watch_counts'][k]) for k in WATCH_TERMS) + " |")
    changed = [r for r in results if r.get("state") == "changed"]
    lines += ["", "## Diffs", ""]
    if not changed:
        lines.append("No changed documents versus the previous snapshot "
                     "(baseline runs have nothing to compare against).")
    for r in changed:
        d = r["diff"]
        lines += [f"### {r['slug']} ({r['previous_date']} -> {date})", "", "```diff"]
        lines += d[:DIFF_LINE_CAP]
        if len(d) > DIFF_LINE_CAP:
            lines.append(f"... {len(d) - DIFF_LINE_CAP} more diff lines; compare the snapshot files directly")
        lines += ["```", ""]
    return "\n".join(lines) + "\n"


MANIFEST_FIELDS = ["date", "slug", "vendor", "url", "final_url", "http_status", "outcome", "state",
                   "previous_date", "format", "extractor", "text_chars", "raw_sha256", "text_sha256",
                   "added", "removed", "error"]


def append_manifest(path: Path, results: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(results)
    existing = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as fh:
            existing = [r for r in csv.DictReader(fh)]
    dates_slugs = {(r["date"], r["slug"]) for r in rows}
    kept = [r for r in existing if (r.get("date"), r.get("slug")) not in dates_slugs]  # idempotent per date
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(kept + [{k: r.get(k, "") for k in MANIFEST_FIELDS} for r in rows])


def rebuild_from_snapshots(targets: list[Target], date: str, snapdir: Path) -> list[dict]:
    out = []
    for t in targets:
        sd = snapdir / t.slug
        if date not in snapshot_dates(sd):
            out.append({"date": date, "slug": t.slug, "vendor": t.vendor, "url": t.url, "final_url": "",
                        "http_status": "", "outcome": "no_snapshot_for_date", "state": "skipped", "error": ""})
            continue
        text, meta = read_snapshot(sd, date)
        prev = previous_date(sd, date)
        prev_text, prev_meta = read_snapshot(sd, prev) if prev else (None, {})
        counts = meta.get("watch_counts") or watch_counts(text)
        out.append({"date": date, "slug": t.slug, "vendor": t.vendor, "url": t.url,
                    "final_url": meta.get("final_url", ""), "http_status": meta.get("http_status", ""),
                    "outcome": "snapshot_written", "text_sha256": meta.get("text_sha256", ""),
                    "previous_date": prev or "", "watch_counts": counts,
                    **compare(prev_text, text, prev_meta.get("watch_counts"), counts)})
    return out


# ----------------------------------------------------------------------------- main

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--snapshots", type=Path, default=DEFAULT_SNAPDIR)
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--only", action="append", default=[], help="slug(s) to process")
    ap.add_argument("--timeout", type=float, default=45.0)
    ap.add_argument("--report-only", action="store_true", help="rebuild report from stored snapshots, no fetching")
    a = ap.parse_args(argv)

    targets = [t for t in read_targets(a.config) if not a.only or t.slug in a.only]
    if a.report_only:
        results = rebuild_from_snapshots(targets, a.date, a.snapshots)
    else:
        results = []
        for t in targets:
            r = process(t, fetch(t.url, a.timeout), a.date, a.snapshots)
            print(f"{t.slug:38s} {r['http_status']:>6s} {r['outcome']:18s} {r.get('state','')}", file=sys.stderr)
            results.append(r)
        append_manifest(a.snapshots / "manifest.csv", results)
    report = a.snapshots / "reports" / f"{a.date}-terms-diff.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(render_report(a.date, results), encoding="utf-8")
    print(f"report: {report}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
