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
  build    -> data/mission-2026-11-14/state-daf-law-50-state-check-2026-11-19.csv

Usage: python3 -I scripts/mission_gap19_state_daf_check.py <scratch_dir> search|unfiltered|control|florida|build  (build runs from the repo root)
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://open.pluralpolicy.com"
UA = "Mozilla/5.0 (compatible; research-script/1.0)"
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


# --- Build stage: merge sweep results with the hand-verified classification ------
# Every classification below was set by reading the text named in `verification`.
# Nothing is inferred from a title alone unless `verification` says "title only".
OUT_CSV = "data/mission-2026-11-14/state-daf-law-50-state-check-2026-11-19.csv"
CHECK_DATE = "2026-11-19"

STATE_NAMES = dict(zip(STATES, (
    "Alabama,Alaska,Arizona,Arkansas,California,Colorado,Connecticut,Delaware,"
    "District of Columbia,Florida,Georgia,Hawaii,Idaho,Illinois,Indiana,Iowa,Kansas,"
    "Kentucky,Louisiana,Maine,Maryland,Massachusetts,Michigan,Minnesota,Mississippi,"
    "Missouri,Montana,Nebraska,Nevada,New Hampshire,New Jersey,New Mexico,New York,"
    "North Carolina,North Dakota,Ohio,Oklahoma,Oregon,Pennsylvania,Rhode Island,"
    "South Carolina,South Dakota,Tennessee,Texas,Utah,Vermont,Virginia,Washington,"
    "West Virginia,Wisconsin,Wyoming").split(",")))

# Official legislature host and what its robots.txt said on 2026-11-19 (curl, generic UA).
ROBOTS = {
    "al": "alison.legislature.state.al.us: 200, no Disallow",
    "ak": "www.akleg.gov: 200; Disallow / for ClaudeBot, anthropic-ai, Claude-Web (not fetched)",
    "az": "www.azleg.gov: 200; /search/ disallowed; crawl-delay 120 (not fetched)",
    "ar": "arkleg.state.ar.us: 200; Disallow only for ChatGPT agents (not fetched)",
    "ca": "leginfo.legislature.ca.gov: 403 Cloudflare challenge, robots unreadable (not fetched)",
    "co": "leg.colorado.gov: 200; file downloads disallowed (not fetched)",
    "ct": "www.cga.ct.gov: TLS failure through proxy, robots unreadable (not fetched)",
    "de": "legis.delaware.gov: 302 (not fetched)",
    "dc": "lims.dccouncil.gov: 200; Disallow / for all agents (not fetched)",
    "fl": "www.flsenate.gov: 200; /Session/Bills allowed; crawl-delay 10 (bill-text search run)",
    "ga": "www.legis.ga.gov: 200, no Disallow (not fetched; search is a JS app)",
    "hi": "www.capitol.hawaii.gov: 403; data.capitol.hawaii.gov: PDFs allowed, *.htm disallowed (PDFs fetched)",
    "id": "legislature.idaho.gov: 200; calendar paths disallowed (not fetched)",
    "il": "www.ilga.gov / lig.ilga.gov / witnessslips.ilga.gov: TLS failure; WebFetch 503 (not fetched)",
    "in": "iga.in.gov: 200, no Disallow (not fetched)",
    "ia": "www.legis.iowa.gov: 200; /chambers/ disallowed (Code sections 15E.303, 15E.305 fetched)",
    "ks": "www.kslegislature.gov: 404 (nothing disallowed; not fetched)",
    "ky": "apps.legislature.ky.gov: 404 (nothing disallowed; not fetched this pass)",
    "la": "legis.la.gov: 404 (nothing disallowed; not fetched)",
    "me": "legislature.maine.gov: 200; search_ps.asp disallowed (not fetched)",
    "md": "mgaleg.maryland.gov: 404 (not fetched)",
    "ma": "malegislature.gov: 200, empty Disallow (bill search run, 194th Court)",
    "mi": "www.legislature.mi.gov: 404 (not fetched)",
    "mn": "www.revisor.mn.gov: 200; /search/doc_result.php disallowed (search is now a JS app; not run)",
    "ms": "billstatus.ls.state.ms.us: 404 (nothing disallowed; bill documents fetched)",
    "mo": "house.mo.gov: /bill.aspx and /*? disallowed, crawl-delay 120 (one bill page fetched before the full file was read; not used); documents.house.mo.gov: crawl-delay 20 (two bill PDFs fetched)",
    "mt": "bills.legmt.gov: 200, empty Disallow; archive.legmt.gov MCA paths 404 (not fetched)",
    "ne": "nebraskalegislature.gov: 200; some search pages disallowed (not fetched)",
    "nv": "www.leg.state.nv.us: 200; reports and exhibits disallowed (not fetched)",
    "nh": "gc.nh.gov: empty reply (robots unreadable; not fetched)",
    "nj": "www.njleg.state.nj.us: 200, no Disallow; pub.njleg.gov redirects to it (P.L.2018 c.29 PDF fetched)",
    "nm": "www.nmlegis.gov: 200; *.axd disallowed (not fetched)",
    "ny": "www.nysenate.gov: 403 Cloudflare challenge on 2026-11-19 (earlier pass read it; not fetched)",
    "nc": "www.ncleg.gov: 200; crawl-delay 2 (bill PDF fetched)",
    "nd": "ndlegis.gov: 200; /search/ disallowed (cencode t57c38.pdf fetched)",
    "oh": "www.legislature.ohio.gov: TLS failure; search-prod.lis.state.oh.us: 404 (bill PDFs fetched)",
    "ok": "www.oklegislature.gov: 200; Disallow / (incl. ClaudeBot) (not fetched)",
    "or": "olis.oregonlegislature.gov: 404 (not fetched)",
    "pa": "www.palegis.us: 200; /legislation/bills/* disallowed for one UA (not fetched)",
    "ri": "status.rilegislature.gov: 200; Disallow / for all agents (not fetched)",
    "sc": "www.scstatehouse.gov: 200; image and dashboard paths disallowed (not fetched)",
    "sd": "sdlegislature.gov: 200; PDF viewer disallowed (not fetched)",
    "tn": "wapp.capitol.tn.gov: 200; Disallow / for all agents (not fetched)",
    "tx": "capitol.texas.gov: 200; /Search/ disallowed (not fetched)",
    "ut": "le.utah.gov: 200; crawl-delay 10 (not fetched)",
    "vt": "legislature.vermont.gov: 200; crawl-delay 30 (not fetched)",
    "va": "lis.virginia.gov: 200, no Disallow (not fetched; JS app)",
    "wa": "app.leg.wa.gov: 200; Disallow / for all agents (not fetched)",
    "wv": "www.wvlegislature.gov: 200; /WVCODE/ disallowed (not fetched)",
    "wi": "docs.legis.wisconsin.gov: connection reset, robots unreadable (not fetched)",
    "wy": "wyoleg.gov: 404 (not fetched)",
}

# Hand-verified classification of every Open States hit (keyed by Open States path).
# subject: payout | reporting | donor intent | tax credit or deduction | other
# daf_role: what the DAF wording does in the text.
HITS = {
 "/ak/bills/33/HB110/": dict(status="died in committee (last action 2024-03-28, referred to Finance)", subject="other", daf_role="DAF wording not read; bill re-enacts PFD contribution law, which bars community foundations from putting PFD gifts in a DAF (AS 43.23.130(k)) [I]", mandate="N", label="S/I", verification="aggregator hit; text not read (akleg.gov robots bars Anthropic agents); AS 43.23.130(k) wording from search snippet"),
 "/ca/bills/20192020/AB1712/": dict(status="failed 2020-02-03 (Joint Rule 56)", subject="reporting", daf_role="would have required AG rules for DAF sponsor reporting (tracker T08)", mandate="proposed (failed)", label="S", verification="aggregator hit; tracker T08"),
 "/ca/bills/20192020/AB2936/": dict(status="died (held in Senate Judiciary, 2020)", subject="reporting", daf_role="separate AG registration class for DAF sponsors (tracker T07)", mandate="proposed (failed)", label="S", verification="aggregator hit; tracker T07"),
 "/ca/bills/20212022/AB1353/": dict(status="died at desk 2022-02-01", subject="other", daf_role="intent-only bill titled 'Donor-advised funds'; no operative text (tracker T06)", mandate="N (intent only)", label="S", verification="aggregator hit; tracker T06"),
 "/ca/bills/20212022/AB488/": dict(status="enacted (Ch. 616, Stats. 2021)", subject="other", daf_role="platform law; DAF sponsor excluded unless it names charities to non-account holders (tracker T01)", mandate="N", label="F", verification="aggregator hit; tracker T01 (official AG pages)"),
 "/ca/bills/20252026/AB576/": dict(status="failed (Joint Rule 56, 2026-02-02)", subject="other", daf_role="platform-law amendment; keeps DAF-sponsor exclusion", mandate="N", label="S", verification="aggregator hit; content from search snippets (leginfo robots unreadable)"),
 "/co/bills/2017A/SB17-287/": dict(status="failed 2017", subject="tax credit or deduction", daf_role="endowment credit bill; DAF wording not read", mandate="N", label="S", verification="aggregator hit; title only"),
 "/co/bills/2018A/HB18-1013/": dict(status="postponed indefinitely 2018-05-10", subject="tax credit or deduction", daf_role="endowment credit bill; DAF wording not read", mandate="N", label="S", verification="aggregator hit; title only"),
 "/dc/bills/22/PR22-0890/": dict(status="withdrawn 2018-10-22", subject="other", daf_role="board confirmation resolution (DAF in nominee biography) [I]", mandate="N", label="S/I", verification="aggregator hit; title only"),
 "/dc/bills/22/PR22-1100/": dict(status="final reading 2018-11-13", subject="other", daf_role="board confirmation resolution (DAF in nominee biography) [I]", mandate="N", label="S/I", verification="aggregator hit; title only"),
 "/hi/bills/2025/HB992/": dict(status="HD1 reported 2025-02-14; carried over to 2026 (last action shown 2025-12-08)", subject="other", daf_role="platform-law amendment; DAF sponsor excluded from 'platform charity' unless it names charities to non-advisors", mandate="N", label="F", verification="official text fetched (HB992_.PDF, HB992_HD1_.PDF)"),
 "/hi/bills/2026/HB992/": dict(status="carried over to 2026 session (same bill as 2025 HB992)", subject="other", daf_role="as 2025 HB992", mandate="N", label="F", verification="same document as 2025 row"),
 "/hi/bills/2025/SB1311/": dict(status="referred 2025-01-27; carried over to 2026 (last action shown 2025-12-08)", subject="other", daf_role="platform-law amendment; same DAF-sponsor exclusion", mandate="N", label="F", verification="official text fetched (SB1311_.PDF)"),
 "/hi/bills/2026/SB1311/": dict(status="carried over to 2026 session (same bill as 2025 SB1311)", subject="other", daf_role="as 2025 SB1311", mandate="N", label="F", verification="same document as 2025 row"),
 "/il/bills/102nd/HB3475/": dict(status="died (sine die 2023-01-10)", subject="other", daf_role="wealth (mark-to-market) tax; counts gifts to a DAF in the base (tax treatment, not a DAF mandate)", mandate="N", label="S", verification="aggregator hit; wording from search snippet (ilga.gov unreachable)"),
 "/il/bills/102nd/SB2121/": dict(status="died (sine die 2023-01-10)", subject="other", daf_role="Senate companion of HB3475; same wealth-tax base wording [S]", mandate="N", label="S", verification="aggregator hit; wording from search snippet"),
 "/il/bills/102nd/HB4462/": dict(status="enacted (P.A. 102-0774, 2022-05-13)", subject="other", daf_role="lets credit unions make charitable gifts through DAF accounts (205 ILCS 305/39); limits transfers to 501(c)(3) foundations and grants to public charities", mandate="N (permission with conditions on credit unions)", label="S", verification="aggregator hit; wording from search snippet of the ILCS page"),
 "/il/bills/102nd/HB5817/": dict(status="died (sine die 2023-01-10)", subject="tax credit or deduction", daf_role="Endow Illinois credit bill; DAF wording not read", mandate="N", label="S", verification="aggregator hit; title only"),
 "/il/bills/103rd/HB5372/": dict(status="failed (floor amendment re-referred to Rules 2024-04-19; sine die)", subject="other", daf_role="credit-union bill; DAF wording not read, probably the reprinted 205 ILCS 305 text [I]", mandate="N", label="S/I", verification="aggregator hit; snippet found no DAF context"),
 "/il/bills/104th/SB3778/": dict(status="pending (referred to Assignments 2026-02-05)", subject="other", daf_role="wealth (mark-to-market) tax part counts gifts to a DAF in the base", mandate="N", label="S", verification="aggregator hit; wording from search snippet"),
 "/la/bills/2019/SR178/": dict(status="enrolled 2019-05-31", subject="other", daf_role="commendation resolution [I]", mandate="N", label="S/I", verification="aggregator hit; title only"),
 "/mn/bills/2017-2018/HF2339/": dict(status="not enacted (last action 2018-03-28)", subject="tax credit or deduction", daf_role="Endow Minnesota credit bill; DAF wording not read", mandate="N", label="S", verification="aggregator hit; title only"),
 "/mn/bills/2017-2018/SF2186/": dict(status="not enacted (last action 2018-03-19)", subject="tax credit or deduction", daf_role="Endow Minnesota credit bill; DAF wording not read", mandate="N", label="S", verification="aggregator hit; title only"),
 "/mo/bills/2025/HB1181/": dict(status="referred to Emerging Issues 2025-05-15; not passed", subject="tax credit or deduction", daf_role="Missouri Gives credit; a credit-eligible permanent endowment fund 'Is not a donor advised fund' (DAF excluded)", mandate="N", label="F", verification="official text fetched (documents.house.mo.gov 2257H.01I)"),
 "/mo/bills/2026/HB2216/": dict(status="referred to Emerging Issues 2026-05-15; not passed", subject="tax credit or deduction", daf_role="same DAF exclusion as HB1181", mandate="N", label="F", verification="official text fetched (documents.house.mo.gov 4074H.01I)"),
 "/ms/bills/2018/HB1485/": dict(status="died in committee 2018-02-21", subject="tax credit or deduction", daf_role="endowment credit bill (precursor of SB2210)", mandate="N", label="S", verification="aggregator hit; title only"),
 "/ms/bills/2018/SB2611/": dict(status="died in committee 2018-02-21", subject="tax credit or deduction", daf_role="endowment credit bill (precursor of SB2210)", mandate="N", label="S", verification="aggregator hit; title only"),
 "/ms/bills/2019/HB1430/": dict(status="died in committee 2019-03-19", subject="tax credit or deduction", daf_role="endowment credit bill", mandate="N", label="S", verification="aggregator hit; title only"),
 "/ms/bills/2019/SB2077/": dict(status="died in committee 2019-02-27", subject="tax credit or deduction", daf_role="endowment credit bill", mandate="N", label="S", verification="aggregator hit; title only"),
 "/ms/bills/2019/SB2210/": dict(status="enacted (approved 2019-03-29); credit allowed through calendar year 2023", subject="tax credit or deduction", daf_role="Endow Mississippi credit; an 'endowed fund' may include donor-advised funds (DAF included)", mandate="N", label="F", verification="official text fetched (SB2210SG, as sent to Governor)"),
 "/ms/bills/2023/SC555/": dict(status="enrolled 2023-03-03", subject="other", daf_role="memorial resolution: honoree established 'one of their first donor advised funds'", mandate="N", label="F", verification="official text fetched (SC0555SG.pdf)"),
 "/ms/bills/2025/SR17/": dict(status="adopted 2025-01-30", subject="other", daf_role="arts-award resolution: honoree established 'one of the first donor-advised funds'", mandate="N", label="F", verification="official text fetched (SR0017IN.pdf)"),
 "/nc/bills/2025/SB684/": dict(status="passed 1st reading 2025-03-26 (no later action shown)", subject="tax credit or deduction", daf_role="credit to endow community foundations; 'endowed fund' includes donor-advised funds (DAF included)", mandate="N", label="F", verification="official text fetched (S684v1.pdf)"),
 "/nj/bills/218/A3615/": dict(status="substituted by S2247 2018-04-12", subject="donor intent", daf_role="Assembly companion of S2247; text not read [I: same wording]", mandate="N", label="S/I", verification="aggregator hit; companion of S2247"),
 "/nj/bills/218/S2247/": dict(status="enacted (P.L.2018, c.29, 2018-05-30); in force", subject="donor intent", daf_role="hospital-conversion assets placed with a charity and moved to a donor-advised fund, if undisbursed, are 'remaining charitable assets' that a court may reallocate to a successor nonprofit hospital (purpose-protection rule for one asset class)", mandate="narrow (court reallocation of conversion assets; not a general DAF rule)", label="F", verification="official text fetched (pub.njleg.gov PL18/29_.PDF)"),
 "/ny/bills/2019-2020/A10414/": dict(status="not enacted (2019-20 session)", subject="other", daf_role="mark-to-market tax; DAF gifts in tax base (pre-window)", mandate="N", label="S", verification="aggregator hit; title only"),
 "/ny/bills/2019-2020/S8277/": dict(status="not enacted (2019-20 session)", subject="other", daf_role="mark-to-market tax; DAF gifts in tax base (pre-window)", mandate="N", label="S", verification="aggregator hit; title only"),
 "/ny/bills/2021-2022/A5092/": dict(status="died in committee", subject="other", daf_role="billionaire mark-to-market tax counts DAF gifts in tax base (tracker T14)", mandate="N", label="F", verification="aggregator hit; tracker T14 (nysenate.gov)"),
 "/ny/bills/2021-2022/S4482/": dict(status="died in committee (referred 2022-01-05)", subject="other", daf_role="Senate companion of A5092; wealth tax base [I]", mandate="N", label="S/I", verification="aggregator hit; text not read (nysenate.gov 403 this pass)"),
 "/ny/bills/2023-2024/A3252/": dict(status="died in committee", subject="other", daf_role="wealth tax counts DAF gifts in tax base (tracker T13)", mandate="N", label="F", verification="aggregator hit; tracker T13"),
 "/ny/bills/2023-2024/S1570/": dict(status="died in committee", subject="other", daf_role="wealth tax counts DAF gifts in tax base (tracker T13)", mandate="N", label="F", verification="aggregator hit; tracker T13"),
 "/ny/bills/2025-2026/A3632/": dict(status="pending (referred to Ways and Means 2026-01-07)", subject="other", daf_role="wealth tax counts DAF gifts in tax base (tracker T12)", mandate="N", label="F", verification="aggregator hit; tracker T12"),
 "/ny/bills/2025-2026/S165/": dict(status="pending (referred to Budget and Revenue 2026-01-07)", subject="other", daf_role="Senate billionaire mark-to-market bill; wealth tax base [I: same DAF clause as A3632]", mandate="N", label="S/I", verification="aggregator hit; text not read"),
 "/oh/bills/135/SB309/": dict(status="referred to committee 2024-11-12; died at end of 135th GA", subject="other", daf_role="definition of 'community foundation' lists 'Providing grants, including donor-advised funds'", mandate="N", label="F", verification="official text fetched (search-prod.lis.state.oh.us SB309 As Introduced)"),
 "/oh/bills/136/SB12/": dict(status="referred to committee 2025-01-29 (no later action shown)", subject="other", daf_role="same community-foundation definition as SB309", mandate="N", label="F", verification="official text fetched (SB12 As Introduced)"),
 "/va/bills/2018/HJ150/": dict(status="agreed 2018-02-08", subject="other", daf_role="commending resolution [I]", mandate="N", label="S/I", verification="aggregator hit; title only"),
 "/wi/bills/2025/AB665/": dict(status="failed to pass (SJR 1, 2026-03-23)", subject="tax credit or deduction", daf_role="non-itemizer charitable subtraction; gifts to DAFs not eligible (DAF excluded)", mandate="N", label="S", verification="aggregator hit; wording from search snippet (docs.legis.wisconsin.gov unreachable)"),
}

# Instruments found outside the Open States sweep (tracker rows, recall misses, statutes).
EXTRA = [
 dict(state="hi", instrument_id="SB 2983 (2024) = Act 205, SLH 2024", session="2024", year="2024", title="Solicitation of funds from the public (platform law)", status="enacted; effective 2026-07-01 (per Act 108)", subject="other", daf_role="DAF sponsor excluded from 'charitable fundraising platform' and 'platform charity' unless it names charities to non-advisors", mandate="N", label="F", verification="official Act PDF fetched (9 DAF mentions); MISSED by Open States phrase search", url="https://data.capitol.hawaii.gov/sessions/sessionlaws/Years/SLH2024/SLH2024_Act205.pdf", record_type="bill"),
 dict(state="hi", instrument_id="SB 1048 (2025) = Act 108, SLH 2025", session="2025", year="2025", title="Amends Act 205 platform law", status="enacted 2025-05-29", subject="other", daf_role="keeps DAF-sponsor exclusion (4 DAF mentions in Act); introduced and SD1 texts have none, so the wording entered later", mandate="N", label="F", verification="official Act and SB1048_/SB1048_SD1_ PDFs fetched; MISSED by Open States phrase search", url="https://data.capitol.hawaii.gov/sessions/sessionlaws/Years/SLH2025/SLH2025_Act108.pdf", record_type="bill"),
 dict(state="il", instrument_id="35 ILCS 60 (Illinois Gives Tax Credit Act, P.A. 103-592) and 86 Ill. Adm. Code 1050", session="103rd GA", year="2024", title="Illinois Gives tax credit", status="enacted; rule effective 2025-05-23", subject="tax credit or deduction", daf_role="credit-eligible permanent endowment fund must not be a DAF (DAF excluded)", mandate="N", label="F/S", verification="tracker T20 (LII mirror of rule); enacting bill not surfaced by the Open States phrase search", url="https://www.law.cornell.edu/regulations/illinois/Ill-Admin-Code-tit-86-SS-1050.100", record_type="statute+regulation"),
 dict(state="il", instrument_id="205 ILCS 305/39 (Illinois Credit Union Act)", session="in force", year="2022", title="Credit union charitable contributions via DAF accounts", status="in force (P.A. 102-774; amended P.A. 103-1034)", subject="other", daf_role="conditions on credit unions' own DAF accounts", mandate="N", label="S", verification="search snippet of ilga.gov ILCS page (not fetched: TLS)", url="https://ilga.gov/legislation/ilcs/documents/020503050K39.htm", record_type="statute"),
 dict(state="ak", instrument_id="AS 43.23.130(k)", session="in force", year="n/a", title="PFD charitable contributions program", status="in force (enacting year not verified)", subject="other", daf_role="community foundation may not deposit PFD-program contributions into a DAF", mandate="N (condition on a state giving program)", label="S", verification="search snippet of FindLaw mirror; akleg.gov robots bars Anthropic agents", url="https://codes.findlaw.com/ak/title-43-revenue-and-taxation/ak-st-sect-43-23-130/", record_type="statute"),
 dict(state="ks", instrument_id="K.A.R. 92-12-152", session="2026", year="2026", title="Pregnancy Resource Act tax credit: contributions", status="in force 2026-04-17", subject="tax credit or deduction", daf_role="no credit for a contribution to a DAF (DAF excluded)", mandate="N", label="F", verification="tracker T21 (Kansas Register); a regulation, so not in a bill search", url="https://www.sos.ks.gov/publications/Register/Volume-45/Issues/Issue-14/04-02-26-54020.html", record_type="regulation"),
 dict(state="ca", instrument_id="FPPC Reg. 18424.3", session="2021", year="2021", title="Behested payment reporting: payments from DAFs", status="in force 2021-12-22", subject="reporting", daf_role="officials (not sponsors) must name sponsor, fund and donor of DAF-sourced behested payments", mandate="N (binds officials, not sponsors)", label="F", verification="tracker T03; a regulation, so not in a bill search", url="https://www.fppc.ca.gov/siteassets/documents/legal_div/regulations/01_index/chapter_04/18424.3._Behested_Payment_Reporting_Payments_from_Donor_Advised_Funds.pdf", record_type="regulation"),
 dict(state="nj", instrument_id="P.L.2000, c.143 (C.26:2H-7.10 et seq.) as amended by P.L.2018, c.29", session="in force", year="2018", title="Community Health Care Assets Protection Act: remaining charitable assets", status="in force", subject="donor intent", daf_role="undisbursed hospital-conversion assets moved to a donor-advised fund remain subject to Superior Court reallocation to a successor nonprofit hospital", mandate="narrow (court reallocation of conversion assets; not a general DAF rule)", label="F", verification="official text fetched (pub.njleg.gov PL18/29_.PDF); same text as bill row S2247; DAF clause first enacted by P.L.2014 c.82 approved 2014-12-26 (pub.njleg.gov PL14/82_.PDF) [V wave 32B]", url="https://pub.njleg.gov/Bills/2018/PL18/29_.PDF", record_type="statute"),
 dict(state="ms", instrument_id="Endow Mississippi credit (2019 SB 2210)", session="in force", year="2019", title="Endow Mississippi Program tax credit", status="enacted 2019; credit allowed through calendar year 2023 (later status not checked)", subject="tax credit or deduction", daf_role="'endowed fund' may include donor-advised funds (DAF included)", mandate="N", label="F", verification="official text fetched (SB2210SG)", url="https://billstatus.ls.state.ms.us/documents/2019/html/SB/2200-2299/SB2210SG.htm", record_type="statute"),
 dict(state="ia", instrument_id="Iowa Code 15E.303, 15E.305 (Endow Iowa)", session="in force", year="n/a", title="Endow Iowa tax credit", status="in force", subject="tax credit or deduction", daf_role="no 'donor' wording at all (negative statute check)", mandate="N", label="F", verification="official Code section PDFs fetched; 0 hits", url="https://www.legis.iowa.gov/docs/code/15E.305.pdf", record_type="statute (negative)"),
 dict(state="nd", instrument_id="N.D.C.C. ch. 57-38 (incl. endowment credit)", session="in force", year="n/a", title="Income tax chapter", status="in force", subject="tax credit or deduction", daf_role="no 'donor' wording in the chapter (negative statute check)", mandate="N", label="F", verification="official chapter PDF fetched; 0 hits", url="https://ndlegis.gov/cencode/t57c38.pdf", record_type="statute (negative)"),
 dict(state="wa", instrument_id="RCW 82.87.080", session="in force", year="2021", title="Capital gains tax charitable deduction", status="in force", subject="tax credit or deduction", daf_role="no DAF wording; sponsor-location test applies by commentary (tracker T22)", mandate="N", label="F/S", verification="tracker T22", url="https://lawfilesext.leg.wa.gov/Law/RCW/RCW%20%2082%20%20TITLE/RCW%20%2082%20.%2087%20%20CHAPTER/RCW%20%2082%20.%2087%20.080.htm", record_type="statute (negative)"),
]

NOT_CHECKABLE = {
    "ct": "Open States text index is thin for CT (control phrase hits 16, against 50-3,851 elsewhere) and cga.ct.gov fails TLS through the proxy, so no full-text search could be run",
}

OFFICIAL_CHECKS = {
    "fl": "flsenate.gov bill-text search, all versions and amendments, sessions 2021-2026: 0 hits for both phrasings; control phrase 63-88 bills per session",
    "ma": "malegislature.gov search, 194th Court (2025-26): 0 hits for both phrasings; control phrase 172 results",
    "hi": "data.capitol.hawaii.gov bill and Act PDFs read",
    "mo": "documents.house.mo.gov bill PDFs read",
    "ms": "billstatus.ls.state.ms.us bill documents read",
    "nc": "ncleg.gov bill PDF read",
    "nj": "pub.njleg.gov P.L.2018 c.29 PDF read",
    "oh": "search-prod.lis.state.oh.us bill PDFs read",
    "ia": "Iowa Code 15E.303 and 15E.305 read (no DAF wording)",
    "nd": "N.D.C.C. ch. 57-38 read (no DAF wording)",
}

IN_WINDOW_SESSIONS = re.compile(r"202[1-6]|10[2-4](nd|rd|th)|3[34]rd|13[56]th")

FIELDS = ["record_id", "record_type", "state", "state_name", "state_result", "instrument_id",
          "session", "year", "title", "status", "subject", "mention_type", "daf_role", "is_daf_mandate",
          "in_window_2021_2026", "evidence_label", "verification", "url",
          "os_hits_donor_advised", "os_hits_donor_hyphen_advised", "os_control_hits_irc",
          "official_check", "robots_official_host", "notes", "check_date"]


def mention_type(row):
    """Tax treatment vs regulation vs mandate vs descriptive wording, from the verified fields."""
    role, subj, mand = row["daf_role"].lower(), row["subject"], row["is_daf_mandate"]
    if "negative" in row["record_type"]:
        return "none (negative check)"
    if mand.startswith("proposed"):
        return "mandate (proposed, failed)"
    if mand.startswith("narrow"):
        return "narrow asset rule"
    if "not read" in role:
        return "unclassified (text not read)"
    if "binds officials" in mand:
        return "disclosure duty on officials (not sponsors)"
    if subj == "tax credit or deduction" or "tax" in role and "base" in role:
        return "tax treatment"
    if "resolution" in role or "biography" in role:
        return "descriptive (resolution)"
    if "definition" in role:
        return "descriptive (definition)"
    if "intent-only" in role:
        return "intent bill (no operative text)"
    return "regulatory exclusion or condition"


def in_window(session, year=""):
    return "Y" if IN_WINDOW_SESSIONS.search(f"{session} {year}") or year == "in force" else "N"


def year_of(r):
    m = re.search(r"(20\d\d)$", r["introduced"])
    return m.group(1) if m else ""


def merge_hits(raw):
    by_href = {}
    for o in raw:
        for r in o["rows"]:
            by_href.setdefault(r["href"], r)
    return by_href


def counts(raw, state):
    pick = lambda ph: sum(len(o["rows"]) for o in raw if o["state"] == state and o["phrase"] == ph)
    return pick(PHRASES[0]), pick(PHRASES[1])


def bill_row(r):
    c = HITS[r["href"]]
    st = r["query_state"]
    return {"record_type": "bill", "state": st.upper(), "state_name": STATE_NAMES[st],
            "instrument_id": r["bill"], "session": r["session"], "year": year_of(r),
            "title": r["title"], "status": c["status"], "subject": c["subject"],
            "daf_role": c["daf_role"], "is_daf_mandate": c["mandate"],
            "in_window_2021_2026": in_window(r["session"], year_of(r)),
            "evidence_label": c["label"], "verification": c["verification"], "url": r["url"],
            "notes": f"Open States latest action: {r['action']} ({r['action_date']})"}


def extra_row(e):
    return {"record_type": e["record_type"], "state": e["state"].upper(),
            "state_name": STATE_NAMES[e["state"]], "instrument_id": e["instrument_id"],
            "session": e["session"], "year": e["year"], "title": e["title"],
            "status": e["status"], "subject": e["subject"], "daf_role": e["daf_role"],
            "is_daf_mandate": e["mandate"],
            "in_window_2021_2026": "Y" if e["session"] == "in force" else in_window(e["session"], e["year"]),
            "evidence_label": e["label"], "verification": e["verification"], "url": e["url"]}


def state_result(state, rows):
    if state in NOT_CHECKABLE:
        return "not checkable"
    hit = [r for r in rows if r["state"] == state.upper() and r["in_window_2021_2026"] == "Y"
           and "negative" not in r["record_type"]]
    return "found" if hit else "checked-none"


def state_row(state, raw, control, rows):
    a, h = counts(raw, state)
    res = state_result(state, rows)
    mine = [r for r in rows if r["state"] == state.upper()]
    window = [r for r in mine if r["in_window_2021_2026"] == "Y" and "negative" not in r["record_type"]]
    pre = [r for r in mine if r["in_window_2021_2026"] == "N"]
    subjects = sorted({r["subject"] for r in window})
    mandates = [r["instrument_id"] for r in window if r["is_daf_mandate"].startswith(("Y", "narrow", "proposed"))]
    note = "; ".join(filter(None, [
        f"{len(window)} in-window instrument(s): subjects {', '.join(subjects)}" if window else "no in-window instrument with DAF wording",
        f"{len(pre)} pre-2021 hit(s) (context only)" if pre else "",
        f"mandate-type items: {', '.join(mandates)}" if mandates else "no payout, reporting or donor-intent mandate on DAF sponsors",
        NOT_CHECKABLE.get(state, ""),
        "thin Open States text index (control < 100): negative is weaker" if (control.get(state) or 0) < 100 and state not in NOT_CHECKABLE else "",
    ]))
    return {"record_type": "state", "state": state.upper(), "state_name": STATE_NAMES[state],
            "state_result": res, "os_hits_donor_advised": a, "os_hits_donor_hyphen_advised": h,
            "os_control_hits_irc": control.get(state), "official_check": OFFICIAL_CHECKS.get(state, "none run"),
            "robots_official_host": ROBOTS[state],
            "url": search_url(PHRASES[0], state, 1), "notes": note}


def run_build(scratch):
    import csv
    raw = json.load(open(f"{scratch}/raw_hits.json"))
    control = {o["state"]: o["found"] for o in json.load(open(f"{scratch}/control_counts.json"))}
    hits = merge_hits(raw)
    missing = set(hits) - set(HITS)
    assert not missing, f"unclassified hits: {missing}"
    rows = sorted([bill_row(r) for r in hits.values()] + [extra_row(e) for e in EXTRA],
                  key=lambda r: (r["state"], r["in_window_2021_2026"] == "N", r["session"], r["instrument_id"]))
    states = [state_row(s, raw, control, rows) for s in STATES]
    result = {r["state"]: r["state_result"] for r in states}
    rows = [r | {"state_result": result[r["state"]], "mention_type": mention_type(r)} for r in rows]
    allrows = [r | {"record_id": f"G{i:03d}", "check_date": CHECK_DATE}
               for i, r in enumerate(states + rows, 1)]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in FIELDS} for r in allrows)
    from collections import Counter
    print(Counter(result.values()), len(rows), "instrument rows")


if __name__ == "__main__":
    {"search": run_search, "control": run_control, "unfiltered": run_unfiltered,
     "florida": run_florida, "build": run_build}[sys.argv[2]](sys.argv[1])
