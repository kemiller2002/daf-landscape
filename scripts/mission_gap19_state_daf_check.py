#!/usr/bin/env python3
"""P-GAP19-14: 50-state + DC search for 'donor advised' / 'donor-advised' bills, 2021-2026.

Functional style: pure parsing functions, one small I/O layer.

Source: Open States (open.pluralpolicy.com) public full-text bill search page,
`/search/?query=...&state=xx`. robots.txt for that host (read 2026-11-19)
disallows only /admin/, /api/v1/, /graphql and /get_district/, so the /search/
pages and /<state>/bills/ pages are allowed. A 2-second delay is used between
requests.

Stages (each writes JSON into the scratch directory given as argv[1]):
  search   -> raw_hits.json      (every hit row for both phrasings, per state)
  unfiltered -> unfiltered_hits.json (both phrases, no state filter)
  florida  -> florida_official.json (flsenate.gov bill-text search, 2021-2026)
  control  -> control_counts.json (per-state count for a text-only control
                                   phrase, to show that bill full text is indexed)

Usage: python3 -I scripts/mission_gap19_state_daf_check.py <scratch_dir> search|unfiltered|control|florida
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://open.pluralpolicy.com"
UA = "Mozilla/5.0 (compatible; daf-landscape-research/1.0; desk research)"
DELAY_S = 2.0

STATES = (
    "al ak az ar ca co ct de dc fl ga hi id il in ia ks ky la me md ma mi mn ms "
    "mo mt ne nv nh nj nm ny nc nd oh ok or pa ri sc sd tn tx ut vt va wa wv wi wy"
).split()

PHRASES = ('"donor advised"', '"donor-advised"')
CONTROL_PHRASE = '"internal revenue code"'

ROW_RE = re.compile(
    r'<tr class="row--align-top">\s*<td>\s*<strong><a href="(?P<href>/[a-z]{2}/bills/[^"]+)">'
    r"(?P<bill>[^<]+)</a></strong>\s*<span[^>]*>\(<strong>(?P<state_name>[^<]+)</strong>"
    r"\s*-\s*(?P<session>.*?)\)</span>\s*<br>\s*<span>(?P<title>.*?)</span>\s*</td>\s*"
    r"<td>(?P<introduced>[^<]*)</td>\s*<td>\s*<span>(?P<action>.*?)</span>\s*<br>\s*"
    r'<span class="u-color--gray">(?P<action_date>[^<]*)</span>',
    re.S,
)
FOUND_RE = re.compile(r"Found (\d+) bills?\b")


def search_url(phrase, state, page):
    q = {"query": phrase} | ({"state": state} if state else {})
    if page > 1:
        q["page"] = str(page)
    return f"{BASE}/search/?{urllib.parse.urlencode(q)}"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def parse_found(page_html):
    m = FOUND_RE.search(page_html)
    return int(m.group(1)) if m else None


def parse_rows(page_html):
    clean = lambda s: re.sub(r"\s+", " ", html.unescape(s)).strip()
    return [
        {k: clean(v) for k, v in m.groupdict().items()} | {"url": BASE + m.group("href")}
        for m in ROW_RE.finditer(page_html)
    ]


def pages_needed(found, per_page=20):
    return max(1, -(-(found or 0) // per_page))


def polite_fetch(url):
    time.sleep(DELAY_S)
    return fetch(url)


def search_state_phrase(state, phrase):
    first = polite_fetch(search_url(phrase, state, 1))
    found = parse_found(first)
    rest = [polite_fetch(search_url(phrase, state, p)) for p in range(2, pages_needed(found) + 1)]
    rows = [r | {"query_state": state, "phrase": phrase}
            for page in (first, *rest) for r in parse_rows(page)]
    return {"state": state, "phrase": phrase, "found": found, "rows": rows,
            "url": search_url(phrase, state, 1)}


def run_search(scratch):
    out = [search_state_phrase(s, p) for s in STATES for p in PHRASES]
    json.dump(out, open(f"{scratch}/raw_hits.json", "w"), indent=1)
    print(sum(len(o["rows"]) for o in out), "rows;", sum((o["found"] or 0) for o in out), "found")


def run_unfiltered(scratch):
    """Same phrases with no state filter, to reconcile against the per-state sums."""
    out = [search_state_phrase(None, p) for p in PHRASES]
    json.dump(out, open(f"{scratch}/unfiltered_hits.json", "w"), indent=1)
    print([(o["phrase"], o["found"], len(o["rows"])) for o in out])


def run_control(scratch):
    out = [{"state": s, "phrase": CONTROL_PHRASE,
            "found": parse_found(polite_fetch(search_url(CONTROL_PHRASE, s, 1))),
            "url": search_url(CONTROL_PHRASE, s, 1)} for s in STATES]
    json.dump(out, open(f"{scratch}/control_counts.json", "w"), indent=1)
    print([(o["state"], o["found"]) for o in out])


# --- Official-site cross-check: Florida Senate bill text search -----------------
# www.flsenate.gov robots.txt (read 2026-11-19): /Session/Bills is not disallowed;
# Crawl-delay 10, which is respected here.
FL_BASE = "https://www.flsenate.gov/Session/Bills"
FL_SESSIONS = ("2021", "2022", "2023", "2024", "2025", "2026")
FL_FOUND_RE = re.compile(r"([\d,]+) Bills? Found")


def fl_url(session, phrase):
    q = {"chamber": "both", "searchOnlyCurrentVersion": "False",
         "isIncludeAmendments": "True", "SearchQuery": phrase}
    return f"{FL_BASE}/{session}?{urllib.parse.urlencode(q)}"


def fl_count(page_html):
    m = FL_FOUND_RE.search(page_html)
    return int(m.group(1).replace(",", "")) if m else None


def run_florida(scratch):
    def one(session, phrase):
        time.sleep(10)
        url = fl_url(session, phrase)
        return {"state": "fl", "session": session, "phrase": phrase,
                "found": fl_count(fetch(url)), "url": url}
    out = [one(s, p) for s in FL_SESSIONS for p in (*PHRASES, CONTROL_PHRASE)]
    json.dump(out, open(f"{scratch}/florida_official.json", "w"), indent=1)
    print([(o["session"], o["phrase"], o["found"]) for o in out])


if __name__ == "__main__":
    {"search": run_search, "control": run_control, "unfiltered": run_unfiltered,
     "florida": run_florida}[sys.argv[2]](sys.argv[1])
