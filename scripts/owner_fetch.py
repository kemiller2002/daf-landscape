#!/usr/bin/env python3
"""Owner-run helper: collect the documents the agents could not fetch.

Run this on YOUR OWN computer, not in the cloud session. Most targets are pages
that block automated agents (robots.txt, CloudFront, site terms) or sit behind
sign-up forms. The script is a download assistant for a person: it opens each
page in a visible browser and records what you save. It does not
  * fill in or submit forms (you type your own details, if you choose to),
  * solve CAPTCHAs or bot checks, or hide that it is automation,
  * crawl: it only visits the named start URLs, one tab at a time.

Modes per task
  api      Regulations.gov official API (needs a free api.data.gov key in
           REGS_API_KEY). Downloads the attachment files for each comment.
  direct   A known file URL (e.g. a Wayback "id_" snapshot). Fetched once
           through the browser context and saved.
  lookup   State charity registries (CA, NY). Writes lookup-template.csv listing the
           top-50 sponsors; you search each one, fill the sheet, and press Enter to
           save each result page. Type "d" when finished.
  guided   Opens the start page. You navigate, fill any form yourself, and
           click the downloads; every download is saved into the task folder.
           Press Enter in the terminal when done and the script also saves an
           .mhtml and .html snapshot of the page you are on (useful for terms
           pages and press releases). Type "s" + Enter to skip a task.

Setup
  python3 -m pip install playwright
  python3 -m playwright install chromium
  export REGS_API_KEY=...            # optional; https://api.data.gov/signup/

Usage
  python3 scripts/owner_fetch.py --list
  python3 scripts/owner_fetch.py --out owner-files               # all tasks
  python3 scripts/owner_fetch.py --out owner-files --only regs-0242 wayback-rcf-1

Output
  owner-files/<task_id>/...         saved files
  owner-files/manifest.csv          task_id, kind, file, url, sha1, bytes, saved_at

Before committing: some reports are copyrighted (Chariot/K2D, M+R, FreeWill).
Commit only what the licence allows (the DAFRC report is CC BY), or keep them
local and paste the needed extracts. Public comments on regulations.gov and
the Wayback snapshots are fine to commit.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, NamedTuple, Optional, Sequence


class Task(NamedTuple):
    task_id: str
    queue_item: str
    mode: str          # "api" | "direct" | "guided" | "lookup"
    url: str
    note: str


DOCKET = "IRS-2023-0053"
WB = "https://web.archive.org/web/{ts}id_/{url}"

REGS_TASKS = tuple(
    Task(f"regs-{n:04d}", "P-B39N101-01", "api", f"{DOCKET}-{n:04d}",
         f"Public comment {DOCKET}-{n:04d} (2026 letter). Click the attachment's download button, then press Enter.")
    for n in range(242, 255)
)

TASKS: tuple[Task, ...] = REGS_TASKS + (
    Task("dafgiving360-financials", "P-G0702-01", "guided", "https://www.dafgiving360.org/",
         "Find the FY2024 and FY2025 audited financial statements (About / Financials) and download both PDFs."),
    Task("dafgiving360-policies", "P-B4428-01", "guided", "https://www.dafgiving360.org/",
         "Download the 2026 Program Policies PDF, then open the 'how to recommend a grant' help page and press Enter to snapshot it."),
    Task("chariot-daf-reports", "P-B40N12-01; P-B40N1202-B43N2602-01", "guided",
         "https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release",
         "Get the DAF Fundraising Report 2026 PDF (form: fill in yourself if you choose), and the 2024 and 2025 editions if offered."),
    Task("mr-benchmarks-2026", "P-B40N12-01", "guided", "https://mrbenchmarks.com/",
         "Download the M+R Benchmarks 2026 PDF."),
    Task("dafrc-reinventing-the-cycle", "P-B44N28-02", "guided",
         "https://scholarworks.iu.edu/dspace/discover?query=%22Reinventing+the+Cycle%22",
         "Open the DAF Research Collaborative report 'Reinventing the Cycle' (2025, CC BY) and download the PDF."),
    Task("freewill-daf-reports", "P-B44N28-02", "guided", "https://www.freewill.com/",
         "Find and download the FreeWill 2025 and 2026 DAF Report PDFs."),
    Task("candid-api-license", "P-B43N26-03-01", "guided",
         "https://candid.org/terms-of-service/api-license-agreement/",
         "Let the page load fully, then press Enter to snapshot it (need s.3.b.xi wording and any caching/retention clause)."),
    Task("ncf-program-agreement", "P-B4222-020101-03", "guided", "https://secure.ncfgiving.com/agreement",
         "Let the agreement load, then press Enter to snapshot it (owner read for the robots-blocked NCF quotes)."),
    Task("cn-press-horizon", "B43N26-03-0304 (CNAI-01/02)", "guided",
         "https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search/",
         "Press Enter to snapshot (owner read replaces the scripted CN fetch)."),
    Task("cn-press-allegory", "B43N26-03-0304 (CNAI-03)", "guided",
         "https://www.charitynavigator.org/about-us/press-release/allegory-integrates-cn-api/",
         "Press Enter to snapshot."),
    Task("cn-press-board", "B43N26-03-0304 (CNAI-05)", "guided",
         "https://www.charitynavigator.org/about-us/press-release/charity-navigator-expands-board/",
         "Press Enter to snapshot."),
    Task("every-org-terms", "P-B43N26-03-02", "guided", "https://www.every.org/terms",
         "Press Enter to snapshot; then the script moves on to /charity-api."),
    Task("every-org-charity-api", "P-B43N26-03-02", "guided", "https://www.every.org/charity-api",
         "Press Enter to snapshot."),
    Task("ca-registry-top50", "P-B5002-01", "lookup", "https://oag.ca.gov/charities",
         "Open the Registry Search from this page. For each sponsor in lookup-template.csv, search by name or "
         "EIN, fill status / latest filing year / notes in the CSV, and press Enter to save that result page."),
    Task("ny-registry-top50", "P-B5002-01", "lookup", "https://charities-search.ag.ny.gov/RegistrySearch",
         "For each sponsor in lookup-template.csv, search by name or EIN (solve any CAPTCHA yourself), fill the "
         "CSV, and press Enter to save that result page."),
    Task("wayback-rcf-1", "P-NPTREN-01", "direct",
         WB.format(ts="20260316031245", url="https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf"),
         "RCF Donor User Guide, capture 2026-03-16."),
    Task("wayback-rcf-2", "P-NPTREN-01", "direct",
         WB.format(ts="20260722200822", url="https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf"),
         "RCF Donor User Guide, capture 2026-07-22."),
    Task("wayback-ubs", "P-NPTREN-01", "direct",
         WB.format(ts="20250421145451", url="https://ubs.donorfirstx.com/pdf/UBS/UBS%20Donor%20User%20Guide.pdf"),
         "UBS Donor User Guide, capture 2025-04-21."),
)


# ---------- pure helpers ----------

def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def safe_name(s: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in s)[:150] or "file"


def select(tasks: Sequence[Task], only: Optional[Sequence[str]]) -> tuple[Task, ...]:
    return tuple(t for t in tasks if not only or t.task_id in only)


def manifest_row(task: Task, kind: str, path: Path, url: str) -> dict:
    data = path.read_bytes()
    return {"task_id": task.task_id, "queue_item": task.queue_item, "kind": kind,
            "file": str(path), "url": url, "sha1": sha1(data), "bytes": len(data), "saved_at": now()}


def regs_attachment_urls(payload: dict) -> tuple[str, ...]:
    """File URLs from a Regulations.gov v4 comment response with include=attachments."""
    included = payload.get("included") or []
    return tuple(f.get("fileUrl") for a in included
                 for f in ((a.get("attributes") or {}).get("fileFormats") or [])
                 if f.get("fileUrl"))


# ---------- side effects ----------

def append_manifest(out: Path, rows: Iterable[dict]) -> None:
    rows = list(rows)
    if not rows:
        return
    path = out / "manifest.csv"
    new = not path.exists()
    with path.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        if new:
            w.writeheader()
        w.writerows(rows)


def http_get(url: str, headers: dict) -> bytes:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def run_api(task: Task, out: Path, key: str) -> list[dict]:
    folder = out / task.task_id
    folder.mkdir(parents=True, exist_ok=True)
    meta = http_get(f"https://api.regulations.gov/v4/comments/{task.url}?include=attachments",
                    {"X-Api-Key": key})
    (folder / "comment.json").write_bytes(meta)
    urls = regs_attachment_urls(json.loads(meta))
    saved = []
    for u in urls:
        time.sleep(1.5)  # stay well inside api.data.gov limits
        p = folder / safe_name(u.rsplit("/", 1)[-1])
        p.write_bytes(http_get(u, {}))
        saved.append(manifest_row(task, "api_attachment", p, u))
    return [manifest_row(task, "api_metadata", folder / "comment.json", task.url)] + saved


def run_direct(task: Task, out: Path, context) -> list[dict]:
    folder = out / task.task_id
    folder.mkdir(parents=True, exist_ok=True)
    resp = context.request.get(task.url, timeout=120_000)
    if not resp.ok:
        print(f"  ! HTTP {resp.status} for {task.url}")
        return []
    p = folder / safe_name(task.url.rsplit("/", 1)[-1])
    p.write_bytes(resp.body())
    return [manifest_row(task, "direct", p, task.url)]


def snapshot(page, folder: Path, task: Task) -> list[dict]:
    html = folder / "page.html"
    html.write_text(page.content(), encoding="utf-8")
    rows = [manifest_row(task, "page_html", html, page.url)]
    try:
        cdp = page.context.new_cdp_session(page)
        mhtml = folder / "page.mhtml"
        mhtml.write_text(cdp.send("Page.captureSnapshot", {"format": "mhtml"})["data"], encoding="utf-8")
        rows.append(manifest_row(task, "page_mhtml", mhtml, page.url))
    except Exception as exc:  # non-Chromium or CDP unavailable
        print(f"  (mhtml snapshot skipped: {exc})")
    return rows


def run_guided(task: Task, out: Path, context) -> list[dict]:
    folder = out / task.task_id
    folder.mkdir(parents=True, exist_ok=True)
    saved: list[dict] = []

    def on_download(dl):
        p = folder / safe_name(dl.suggested_filename)
        dl.save_as(str(p))
        saved.append(manifest_row(task, "download", p, dl.url))
        print(f"  saved {p.name}")

    context.on("download", on_download)
    page = context.new_page()
    page.goto(task.url if task.mode == "guided" else
              f"https://www.regulations.gov/comment/{task.url}", wait_until="domcontentloaded")
    print(f"  {task.note}")
    answer = input("  Enter = done and snapshot page, s = skip: ").strip().lower()
    rows = [] if answer == "s" else snapshot(page, folder, task)
    context.remove_listener("download", on_download)
    page.close()
    return saved + rows


REG_CSV = Path("data/mission-2026-11-14/state-registration-2026-11-20.csv")
LOOKUP_COLS = ("ein", "sponsor_name", "fy2024_rank_assets", "status", "registry_id", "latest_filing_year",
               "enforcement_notice", "notes", "looked_up_on")


def top50_sponsors(rows: Iterable[dict]) -> tuple[dict, ...]:
    """Unique top-50 sponsors (EIN, name, rank) from the state-registration CSV, rank order."""
    seen = {r["ein"]: r for r in rows if r.get("size_band_fy2024") == "top50"}
    key = lambda r: int(float(r.get("fy2024_rank_assets") or 9999))
    return tuple(sorted(seen.values(), key=key))


def template_rows(sponsors: Iterable[dict]) -> tuple[dict, ...]:
    return tuple({**{c: "" for c in LOOKUP_COLS}, "ein": s["ein"], "sponsor_name": s["sponsor_name"],
                  "fy2024_rank_assets": s.get("fy2024_rank_assets", "")} for s in sponsors)


def write_template(folder: Path) -> Path:
    path = folder / "lookup-template.csv"
    if path.exists():  # never overwrite the owner's filled-in sheet
        return path
    src = list(csv.DictReader(REG_CSV.open(newline=""))) if REG_CSV.exists() else []
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(LOOKUP_COLS))
        w.writeheader()
        w.writerows(template_rows(top50_sponsors(src)))
    return path


def run_lookup(task: Task, out: Path, context) -> list[dict]:
    """Manual registry lookups: one template to fill, one saved page per Enter."""
    folder = out / task.task_id
    folder.mkdir(parents=True, exist_ok=True)
    tpl = write_template(folder)
    print(f"  Template: {tpl}  (fill it in as you go)")
    page = context.new_page()
    page.goto(task.url, wait_until="domcontentloaded")
    print(f"  {task.note}")
    rows: list[dict] = []
    n = 0
    while True:
        answer = input("  Enter = save this result page, d = done: ").strip().lower()
        if answer == "d":
            break
        n += 1
        sub = folder / f"result-{n:03d}"
        sub.mkdir(exist_ok=True)
        rows += snapshot(page, sub, task)
    page.close()
    return rows + ([manifest_row(task, "lookup_template", tpl, task.url)] if tpl.exists() else [])


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="owner-files")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--profile", default=str(Path.home() / ".daf-owner-fetch-profile"),
                    help="persistent browser profile, so sign-ins and cookies survive between runs")
    args = ap.parse_args(argv)

    tasks = select(TASKS, args.only)
    if args.list:
        print("\n".join(f"{t.task_id:30} {t.mode:7} {t.queue_item:28} {t.url}" for t in tasks))
        return 0

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    key = os.environ.get("REGS_API_KEY", "")

    api_tasks = tuple(t for t in tasks if t.mode == "api" and key)
    browser_tasks = tuple(t if t.mode != "api" else t._replace(mode="guided_regs")
                          for t in tasks if not (t.mode == "api" and key))

    for t in api_tasks:
        print(f"[api] {t.task_id}")
        try:
            append_manifest(out, run_api(t, out, key))
        except Exception as exc:
            print(f"  ! {exc}; rerun without REGS_API_KEY to use the browser for this one")

    if browser_tasks:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            context = pw.chromium.launch_persistent_context(args.profile, headless=False, accept_downloads=True)
            for t in browser_tasks:
                print(f"[{t.mode}] {t.task_id}  ({t.queue_item})")
                runner = {"direct": run_direct, "lookup": run_lookup}.get(t.mode, run_guided)
                append_manifest(out, runner(t, out, context))
            context.close()
    print(f"Done. Manifest: {out / 'manifest.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
