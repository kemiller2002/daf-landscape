#!/usr/bin/env python3
"""Owner-directed re-fetch of previously blocked sources (functional style, stdlib only).

Context: owner decision of 2026-11-20 (research/education/owner-decision-robots-2026-11-20.md):
robots.txt no longer limits owner-directed research. This script still never bypasses access
controls: pages that answer with a login wall, CAPTCHA or bot challenge are recorded as
'challenge' and left alone. 'lookup' rows (form-driven registry searches) are skipped.

Input : data/mission-2026-11-14/owner-fetch-targets-2026-11-20.csv
Output: <out>/files/<target_id>.<ext>   fetched bodies (kept outside the repository)
        data/mission-2026-11-14/owner-refetch-results-2026-11-20.csv   one row per target
Usage : python3 -I scripts/owner_refetch.py <out_dir> [--priority high,medium,low]
Requests: browser-like User-Agent, at most one in flight per host, >= 2 s apart per host.
"""
import csv
import hashlib
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from itertools import groupby
from pathlib import Path

TARGETS = Path("data/mission-2026-11-14/owner-fetch-targets-2026-11-20.csv")
RESULTS = Path("data/mission-2026-11-14/owner-refetch-results-2026-11-20.csv")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
CHALLENGE = ("just a moment", "cf-chl", "challenge-platform", "vercel security checkpoint",
             "captcha", "are you a robot", "access denied", "please enable javascript and cookies",
             "attention required! | cloudflare", "perimeterx", "px-captcha", "datadome")
EXT = {"application/pdf": "pdf", "text/html": "html", "application/json": "json", "text/csv": "csv",
       "application/xml": "xml", "text/xml": "xml", "text/plain": "txt", "application/zip": "zip"}


def fetch(url: str) -> tuple:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.headers.get_content_type(), r.geturl(), r.read(30_000_000)
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get_content_type() if e.headers else "", url, e.read(200_000) if e.fp else b""
    except Exception as e:  # network errors
        return 0, type(e).__name__, url, b""


def classify(status: int, ctype: str, body: bytes) -> str:
    head = body[:60_000].decode("utf-8", "ignore").lower()
    if status == 0:
        return "network_error"
    if any(m in head for m in CHALLENGE) and (status in (401, 403, 429, 503) or len(body) < 40_000):
        return "challenge"
    if status in (401, 407):
        return "login"
    if 200 <= status < 300 and len(body) > 200:
        return "fetched"
    return f"http_{status}"


def run_host(rows: list, out: Path) -> list:
    def one(row):
        status, ctype, final, body = fetch(row["url"])
        state = classify(status, ctype, body)
        path = ""
        if state == "fetched":
            path = str(out / "files" / f"{row['target_id']}.{EXT.get(ctype, 'bin')}")
            Path(path).write_bytes(body)
        time.sleep(2)
        return {"target_id": row["target_id"], "url": row["url"], "host": row["host"],
                "prior_block": row["block_reason"], "priority": row["priority"], "result": state,
                "http_status": status, "content_type": ctype, "final_url": final, "bytes": len(body),
                "sha1": hashlib.sha1(body).hexdigest() if body else "", "local_file": path,
                "fetched_on": time.strftime("%Y-%m-%d")}
    return [one(r) for r in rows]


def main(out: Path, priorities: tuple) -> int:
    (out / "files").mkdir(parents=True, exist_ok=True)
    rows = [r for r in csv.DictReader(TARGETS.open(newline="", encoding="utf-8"))
            if r["mode"] != "lookup" and r["priority"] in priorities and not r["already_in_owner_fetch"].startswith("fetched")]
    by_host = [list(g) for _, g in groupby(sorted(rows, key=lambda r: r["host"]), key=lambda r: r["host"])]
    with ThreadPoolExecutor(max_workers=12) as pool:
        results = [x for chunk in pool.map(lambda g: run_host(g, out), by_host) for x in chunk]
    with RESULTS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(sorted(results, key=lambda r: r["target_id"]))
    counts = {}
    for r in results:
        counts[r["result"]] = counts.get(r["result"], 0) + 1
    print(len(results), "targets:", counts)
    return 0


if __name__ == "__main__":
    pr = next((a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--priority")), "high,medium,low")
    sys.exit(main(Path(sys.argv[1]), tuple(pr.split(","))))
