#!/usr/bin/env python3
"""Pass-through recipients: large top-50 DAF grantees with no public donate link (queue item P-B39N6-03).

Population
  Rows of data/mission-2026-11-14/nonprofit-donate-page-daf-scan-2026.csv with scan_status = home_only_no_donate_link
  (the homepage was read and robots-allowed, but no donate/give link was found). 28 EINs.

Dollars (stage `report`, pure)
  The same top-50 Schedule I Part II lines as scripts/mission_recipient_sectors.py (94 itemising sponsor-years,
  FY2023-FY2024, lines cache of that script), DAF-to-DAF lines removed with the same rule (whitelist decision
  `include`, self-lines, blank-EIN lines matching one whitelisted name: mission_recipient_sectors.annotate).
  Two scopes: `all` (all 94 sponsor-years) and `ex_uh` (grantors that are not DAFRC university/hospital panel
  members, the frame of mission_donate_page_scan.py; reproduces its daf_grant_usd_fy2023_2024 exactly).
  Two bases: `filed` (Schedule I dollars) and `daf_weighted` (each sponsor-year's lines x its daf_share_of_grants
  from sponsor-cost-structure.csv, capped at 1; the repo's weighting in mission_recipient_sectors.py).

Recipient filings (stage `fetch`, I/O)
  Each EIN's own e-filed Form 990 for tax years 2023 and 2024 (IRS TEOS index_2024..2026; latest submission per
  TAX_PERIOD), read from the GivingTuesday mirror of IRS TEOS (cached under --work/xml). Fields: Part VIII 1h
  contributions (1a federated, 1e government grants), total revenue, total functional expenses, Part IX lines 1-3
  (grants to domestic organisations, to individuals, foreign), Schedule I Part II lines (count, $, recipients),
  net assets BOY/EOY, Part IV line 6 (DAF indicator), and every text node mentioning fiscal sponsorship.

Receiving channel (stage `fetch`, I/O; polite, public pages only)
  For each website in the scan: robots.txt first (200 -> parsed for `*`; 404/410 -> no rules; else unreadable and
  nothing fetched). Then, only where allowed: the homepage, up to 8 same-site pages whose link URL or anchor text
  suggests giving or partnering, up to 6 sitemap URLs with such words, and 6 fixed paths (/donate, /give,
  /support, /ways-to-give, /faq, /contact). Raw HTML only (no JS rendering); nothing is clicked or submitted.
  >= 1.5 s between requests to a host. UA "research-script/1.0".
  Detectors: donor-advised / DAF text; DAFpay/Chariot or DAF Direct widget; sponsor links; wire/ACH; check by
  mail; stock/securities transfer; own EIN shown; grant agreement; fiscal-sponsorship language; giving contact
  e-mail. Channel class (first match): daf_instructions, giving_page_no_daf, giving_contact_only,
  no_giving_info_found (or robots_* / unreachable).

Pass-through class (pure; computed from the recipient's own 990s, 2023+2024 pooled)
  fiscal_sponsor        990 text mentions fiscal sponsorship (FISCAL(LY) SPONSOR) at least once
  regranting_intermediary  otherwise, Part IX lines 1-3 >= 50% of total functional expenses
  operating             otherwise
  no_990                no e-filed 990 for 2023/2024 (e.g. churches)
  Within-year onward flow = Part IX lines 1-3 / Part VIII 1h (grants out per $ contributed in), pooled over the
  two tax years; also Schedule I $ to other population EINs (chains inside the set).

Stdlib only; functional style (pure transforms; I/O at the edges).

Usage
  python3 scripts/mission_pass_through_recipients.py fetch  . --index-dir IRS --work W
  python3 scripts/mission_pass_through_recipients.py report . --np-cache NPCACHE --lines-cache LC --work W [--out CSV]
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from html.parser import HTMLParser
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import COST, WHITELIST, annotate, load_lines  # noqa: E402

SCAN_CSV = os.path.join(DATA, "nonprofit-donate-page-daf-scan-2026.csv")
OUT_CSV = os.path.join(DATA, "pass-through-recipients-2026-11-20.csv")
UA = "research-script/1.0"
HOST_GAP = 1.5
TAX_YEARS = (2023, 2024)
POP_STATUS = "home_only_no_donate_link"
# The organisations the queue item names (P-B39N6-03); both Energy Foundation EINs are kept.
NAMED = frozenset({"205806345", "473681860", "473522162", "815086187", "262303250", "831740146", "943126848"})

# ============================================================================ population
def population(scan_rows: Sequence[Mapping]) -> tuple[dict, ...]:
    return tuple(r for r in scan_rows if r["scan_status"] == POP_STATUS)


# ============================================================================ dollars (pure)
def recipient_dollars(ann: Mapping, panel: Mapping, weights: Mapping, eins: frozenset) -> dict:
    """-> {"totals": {scope: {basis: $}}, "by_ein": {ein: {...}}} for non-D2D lines."""
    def scope_ok(scope, g):
        return scope == "all" or panel[g]["segment"] != "university_hospital"

    rows = tuple((k, r) for k, rs in ann.items() for r in rs if not r["d2d"])

    def tot(scope, basis, pred=lambda r: True):
        return sum(r["amount"] * (weights.get(k, 1.0) if basis == "daf_weighted" else 1.0)
                   for k, r in rows if scope_ok(scope, k[0]) and pred(r))
    totals = {s: {b: tot(s, b) for b in ("filed", "daf_weighted")} for s in ("all", "ex_uh")}
    totals_with_ein = {s: {b: tot(s, b, lambda r: bool(r["ein"])) for b in ("filed", "daf_weighted")} for s in ("all", "ex_uh")}
    mine = _group_by_fast((kr for kr in rows if kr[1]["ein"] in eins), lambda kr: kr[1]["ein"])

    def per(e, krs):
        def s(scope, basis, fy=None):
            return sum(r["amount"] * (weights.get(k, 1.0) if basis == "daf_weighted" else 1.0)
                       for k, r in krs if scope_ok(scope, k[0]) and (fy is None or k[1] == fy))
        by_g = reduce(lambda acc, kr: {**acc, kr[0][0]: acc.get(kr[0][0], 0.0) + kr[1]["amount"]}, krs, {})
        top = sorted(by_g.items(), key=lambda kv: -kv[1])
        return {"all_filed": s("all", "filed"), "all_daf_weighted": s("all", "daf_weighted"),
                "ex_uh_filed": s("ex_uh", "filed"), "ex_uh_daf_weighted": s("ex_uh", "daf_weighted"),
                "fy2023_filed": s("all", "filed", 2023), "fy2024_filed": s("all", "filed", 2024),
                "lines": len(krs), "grantors": len(by_g),
                "top_grantors": "; ".join(f"{panel[g]['name']} ${v / 1e6:.1f}m" for g, v in top[:3]),
                "top_grantor_share": (top[0][1] / sum(by_g.values())) if by_g and sum(by_g.values()) else None}
    return {"totals": totals, "totals_with_ein": totals_with_ein, "by_ein": {e: per(e, v) for e, v in mine.items()}}


# ============================================================================ 990 extraction (pure on bytes)
FS_RX = re.compile(r"FISCAL(LY)?[\s-]+SPONSOR", re.I)
F990PF = {"contrib_1h": "ContriRcvdRevAndExpnssAmt", "total_revenue": "TotalRevAndExpnssAmt",
          "total_expenses": "TotalExpensesRevAndExpnssAmt", "grants_part_i_13": "ContriPaidRevAndExpnssAmt",
          "net_assets_boy": "TotNetAstOrFundBalancesBOYAmt", "net_assets_eoy": "TotNetAstOrFundBalancesEOYAmt",
          "website": "WebsiteAddressTxt"}
F990EZ = {"contrib_1h": "ContributionsGiftsGrantsEtcAmt", "total_revenue": "TotalRevenueAmt", "total_expenses": "TotalExpensesAmt",
          "grants_part_i_13": "GrantsAndSimilarAmountsPaidAmt", "net_assets_boy": "NetAssetsOrFundBalancesBOYAmt",
          "net_assets_eoy": "NetAssetsOrFundBalancesEOYAmt", "website": "WebsiteAddressTxt"}
F990 = {"contrib_1h": "TotalContributionsAmt", "federated_1a": "FederatedCampaignsAmt", "gov_grants_1e": "GovernmentGrantsAmt",
        "total_revenue": "CYTotalRevenueAmt", "total_expenses": "CYTotalExpensesAmt", "grants_part_i_13": "CYGrantsAndSimilarPaidAmt",
        "net_assets_boy": "NetAssetsOrFundBalancesBOYAmt", "net_assets_eoy": "NetAssetsOrFundBalancesEOYAmt",
        "daf_ind": "DonorAdvisedFundInd", "website": "WebsiteAddressTxt", "fiscal_sponsor_ind_none": "__none__"}
IX_GROUPS = {"grants_ix1": "GrantsToDomesticOrgsGrp", "grants_ix2": "GrantsToDomesticIndividualsGrp", "grants_ix3": "ForeignGrantsGrp"}


def extract_990(data: bytes) -> dict:
    root = ET.fromstring(data)
    first = {}
    for el in root.iter():
        t = local(el.tag)
        if t not in first and el.text and el.text.strip():
            first[t] = el.text.strip()
    rtype = next((local(el.tag) for el in root.iter() if local(el.tag) in ("IRS990", "IRS990EZ", "IRS990PF")), "")
    fmap = {"IRS990PF": F990PF, "IRS990EZ": F990EZ}.get(rtype, F990)
    out = {k: first.get(v, "") for k, v in fmap.items() if not k.endswith("_none")}

    def group_total(name):
        g = next((el for el in root.iter() if local(el.tag) == name), None)
        if g is None:
            return 0.0
        return num(next((c.text for c in g.iter() if local(c.tag) == "TotalAmt" and c.text), "0")) or 0.0
    # 990-PF / 990-EZ have no Part IX lines 1-3: all grants paid go to grants_ix1 (Part I line 25 / EZ line 10).
    ix = ({k: group_total(v) for k, v in IX_GROUPS.items()} if rtype == "IRS990" else
          {"grants_ix1": num(out.get("grants_part_i_13") or "0") or 0.0, "grants_ix2": 0.0, "grants_ix3": 0.0})

    def rec(el):
        g = {local(c.tag): (c.text or "").strip() for c in el.iter()}
        name = " ".join((c.text or "").strip() for c in el.iter()
                        if local(c.tag) in ("BusinessNameLine1Txt", "BusinessNameLine2Txt") and c.text)
        amt = ((num(g.get("CashGrantAmt", "")) or 0.0) + (num(g.get("NonCashAssistanceAmt", "")) or 0.0)
               if local(el.tag) == "RecipientTable" else (num(g.get("Amt", "")) or 0.0))
        return {"ein": ein9(g["RecipientEIN"]) if g.get("RecipientEIN") else "", "name": name[:90], "amount": amt}
    recs = tuple(rec(el) for el in root.iter() if local(el.tag) in ("RecipientTable", "GrantOrContributionPdDurYrGrp"))
    fs_texts = tuple(sorted({re.sub(r"\s+", " ", el.text.strip())[:240] for el in root.iter()
                             if el.text and FS_RX.search(el.text)}))
    return {**{k: (num(v) if k not in ("daf_ind", "website") else v) for k, v in out.items()}, **ix,
            "return_type": rtype, "sched_i_lines": len(recs), "sched_i_usd": sum(r["amount"] for r in recs),
            "sched_i_recipients": recs, "fiscal_sponsor_texts": fs_texts}


# ============================================================================ index (I/O light)
def filings_for(index_dir: str, eins: frozenset) -> dict:
    """EIN -> {tax_year: index row} for RETURN_TYPE 990 / 990EZ / 990PF, latest submission (OBJECT_ID) per TAX_PERIOD."""
    def rows():
        for y in range(2023, 2027):
            p = os.path.join(index_dir, f"index_{y}.csv")
            if not os.path.exists(p):
                continue
            with open(p, encoding="latin-1", newline="") as fh:
                for r in csv.DictReader(fh):
                    if ein9(r.get("EIN") or "") in eins and (r.get("RETURN_TYPE") or "").strip() in ("990", "990EZ", "990PF"):
                        yield {"ein": ein9(r["EIN"]), "tax_period": r["TAX_PERIOD"].strip(), "return_type": r["RETURN_TYPE"].strip(),
                               "oid": r["OBJECT_ID"].strip(), "index_year": y}
    g = _group_by_fast(tuple(rows()), lambda r: (r["ein"], int(r["tax_period"][:4])))
    best = {k: max(v, key=lambda r: r["oid"]) for k, v in g.items() if k[1] in TAX_YEARS}
    return reduce(lambda acc, kv: {**acc, kv[0][0]: {**acc.get(kv[0][0], {}), kv[0][1]: kv[1]}}, best.items(), {})


def get_xml(oid: str, cache_dir: str) -> bytes | None:
    p = os.path.join(cache_dir, f"{oid}_public.xml")
    if os.path.exists(p) and os.path.getsize(p) > 5000:
        with open(p, "rb") as fh:
            return fh.read()
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()
            os.makedirs(cache_dir, exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)
            return data
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return None
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            time.sleep(3 * (attempt + 1))
    return None


# ============================================================================ web (I/O)
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self._a, self._txt = [], None, []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._a, self._txt = dict(attrs).get("href") or "", []

    def handle_data(self, d):
        if self._a is not None:
            self._txt.append(d)

    def handle_endtag(self, tag):
        if tag == "a" and self._a is not None:
            self.links.append((self._a, " ".join("".join(self._txt).split())[:80]))
            self._a = None


def links_of(base: str, body: str) -> tuple[tuple[str, str], ...]:
    p = Links()
    try:
        p.feed(body)
    except Exception:  # noqa: BLE001 - malformed HTML is data, not an error
        pass
    return tuple((urllib.parse.urljoin(base, h).split("#")[0], t) for h, t in p.links if h and not h.startswith(("mailto:", "tel:", "javascript:")))


CHANNEL_WORDS = re.compile(r"donat|\bgive\b|giving|support[-_ ]?us|ways[-_ ]to|donor|\bdaf\b|partner[-_ ]with|work[-_ ]with[-_ ]us|"
                           r"fund[-_ ]?with|contribut|philanthrop|for[-_ ]funders|funders|invest[-_ ]with|faq", re.I)
FIXED_PATHS = ("/donate", "/give", "/support", "/ways-to-give", "/faq", "/contact")


def text_of_html(body: str) -> str:
    b = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", body)
    return " ".join(html.unescape(re.sub(r"(?s)<[^>]+>", " ", b)).split())


DETECT = {
    "daf_text": re.compile(r"donor[- ]advised|\bDAFs?\b", re.I),
    "daf_widget": re.compile(r"dafpay|chariot|dafdirect|daf-direct|daf direct", re.I),
    "sponsor_link": re.compile(r"fidelitycharitable\.org|schwabcharitable\.org|dafgiving360|vanguardcharitable\.org", re.I),
    "wire_ach": re.compile(r"\bwire (transfer|instructions)|\bwiring\b|\bACH\b|bank transfer|routing number", re.I),
    "check_mail": re.compile(r"(mail|send) (a |your )?(check|cheque)|checks? (should be |can be )?(made )?payable", re.I),
    "stock": re.compile(r"(gifts?|transfers?|donations?) of (stock|securities|appreciated)|stock (gift|transfer|donation)", re.I),
    "grant_agreement": re.compile(r"grant agreement", re.I),
    "fiscal_sponsor": re.compile(r"fiscal(ly)?[- ]sponsor", re.I),
    "tax_id_label": re.compile(r"\b(EIN|tax[- ]ID|federal (tax )?identification)\b", re.I),
}
EMAIL_RX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
GIVE_EMAIL_RX = re.compile(r"^(give|giving|donat|development|philanthropy|partner|funders?|advancement|gifts?)", re.I)


def detect(url: str, body: str, ein: str) -> dict:
    txt = text_of_html(body)
    hits = {k: bool(rx.search(body if k in ("daf_widget", "sponsor_link") else txt)) for k, rx in DETECT.items()}
    d = ein
    hits["own_ein_shown"] = bool(re.search(rf"{d[:2]}[- ]?{d[2:]}", txt))
    emails = sorted({m for m in EMAIL_RX.findall(body) if GIVE_EMAIL_RX.match(m)})
    snip = next((txt[max(0, m.start() - 90): m.end() + 110] for m in [DETECT["daf_text"].search(txt)] if m), "")
    return {"url": url, **hits, "giving_emails": emails, "daf_snippet": snip}


def fetch(url: str, timeout: int = 30) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.5"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ct = resp.headers.get("Content-Type", "")
            body = resp.read(3_000_000).decode("utf-8", "replace") if ("html" in ct or "xml" in ct or not ct) else ""
            return resp.status, resp.geturl(), body
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:  # noqa: BLE001
        return -1, url, type(e).__name__


def robots_for(base: str) -> dict:
    u = urllib.parse.urljoin(base, "/robots.txt")
    code, final, body = fetch(u)
    rp = urllib.robotparser.RobotFileParser()
    if code == 200:
        rp.parse(body.splitlines())
        state = "parsed"
    elif code in (404, 410):
        rp.parse([])
        state = "no_rules"
    else:
        state = "unreadable"
    sitemaps = tuple(l.split(":", 1)[1].strip() for l in body.splitlines() if l.lower().startswith("sitemap:")) if code == 200 else ()
    return {"robots_url": u, "robots_code": code, "robots_state": state, "rp": rp, "sitemaps": sitemaps}


def same_site(a: str, b: str) -> bool:
    h = lambda u: urllib.parse.urlparse(u).netloc.lower().removeprefix("www.")  # noqa: E731
    return h(a) == h(b)


def scan_site(row: Mapping) -> dict:
    base, ein = row["website"], row["ein"]
    if not base:
        return {"ein": ein, "robots_state": "no_website", "pages": [], "log": []}
    rb = robots_for(base)
    log = [{"host": urllib.parse.urlparse(base).netloc, "robots_url": rb["robots_url"], "code": rb["robots_code"],
            "state": rb["robots_state"]}]
    if rb["robots_state"] == "unreadable":
        return {"ein": ein, "robots_state": "unreadable", "robots_code": rb["robots_code"], "pages": [], "log": log}
    allowed = lambda u: rb["rp"].can_fetch("*", u)  # noqa: E731
    seen, pages = set(), []

    def get(u):
        if u in seen or not allowed(u):
            return None
        seen.add(u)
        time.sleep(HOST_GAP)
        code, final, body = fetch(u)
        if final != u and not same_site(final, base):
            return {"url": u, "code": code, "final": final, "body": "", "note": "offsite_redirect_discarded"}
        if final != u and not allowed(final):
            return {"url": u, "code": code, "final": final, "body": "", "note": "redirect_robots_disallowed"}
        return {"url": u, "code": code, "final": final, "body": body if code == 200 else ""}
    home = get(base)
    cand = tuple(dict.fromkeys(u for u, t in links_of(home["final"], home["body"])
                               if same_site(u, base) and (CHANNEL_WORDS.search(urllib.parse.urlparse(u).path) or CHANNEL_WORDS.search(t))
                               and not re.search(r"\.(pdf|jpg|png|zip|docx?)$", u, re.I)))[:8] if home else ()
    sm_urls = ()
    for sm in (rb["sitemaps"] or (urllib.parse.urljoin(base, "/sitemap.xml"),))[:2]:
        r = get(sm)
        if r and r["body"]:
            locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r["body"])
            sub = [l for l in locs if l.endswith(".xml")][:3]
            subs = tuple(x for s in sub for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", (get(s) or {}).get("body", "")))
            sm_urls += tuple(l for l in (*locs, *subs) if not l.endswith(".xml") and same_site(l, base)
                             and CHANNEL_WORDS.search(urllib.parse.urlparse(l).path))
    sm_urls = tuple(dict.fromkeys(sm_urls))[:6]
    fixed = tuple(urllib.parse.urljoin(base, p) for p in FIXED_PATHS)
    others = [get(u) for u in dict.fromkeys((*cand, *sm_urls, *fixed))]
    for r in [home, *others]:
        if r is None:
            continue
        pages.append({k: v for k, v in r.items() if k != "body"} | (detect(r["final"], r["body"], ein) if r["body"] else {}))
    disallowed = [u for u in dict.fromkeys((base, *cand, *sm_urls, *fixed)) if not allowed(u)]
    return {"ein": ein, "robots_state": rb["robots_state"], "robots_code": rb["robots_code"], "pages": pages,
            "disallowed": disallowed, "candidates": list(cand), "sitemap_hits": list(sm_urls), "log": log}


def stage_fetch(a) -> int:
    pop = population(read_csv(SCAN_CSV))
    eins = frozenset(r["ein"] for r in pop)
    fil = filings_for(a.index_dir, eins)
    xml_dir = os.path.join(a.work, "xml")
    oids = sorted({f["oid"] for v in fil.values() for f in v.values()})
    with ThreadPoolExecutor(max_workers=4) as ex:
        got = dict(zip(oids, ex.map(lambda o: get_xml(o, xml_dir), oids)))
    ext = {o: (extract_990(b) if b else None) for o, b in got.items()}
    filings = {e: {str(y): {**f, "extract": ext.get(f["oid"])} for y, f in v.items()} for e, v in fil.items()}
    with open(os.path.join(a.work, "filings.json"), "w") as fh:
        json.dump(filings, fh)
    if not a.no_web:
        with ThreadPoolExecutor(max_workers=6) as ex:
            web = list(ex.map(scan_site, pop))
        with open(os.path.join(a.work, "web.json"), "w") as fh:
            json.dump({w["ein"]: w for w in web}, fh, default=str)
    print(json.dumps({"population": len(pop), "eins_with_990": len(fil), "xml": len(oids),
                      "xml_ok": sum(1 for v in ext.values() if v)}, indent=1))
    return 0


# ============================================================================ report (pure + edges)
def channel_class(w: Mapping) -> tuple[str, dict]:
    st = w.get("robots_state")
    if st in ("unreadable", "no_website"):
        return f"robots_{st}" if st == "unreadable" else st, {}
    ok = [p for p in w.get("pages", []) if p.get("code") == 200 and "daf_text" in p]
    if not ok:
        return "unreachable", {}
    agg = {k: any(p.get(k) for p in ok) for k in ("daf_text", "daf_widget", "sponsor_link", "wire_ach", "check_mail",
                                                  "stock", "grant_agreement", "fiscal_sponsor", "own_ein_shown", "tax_id_label")}
    emails = sorted({e for p in ok for e in p.get("giving_emails", [])})
    giving_pages = [p["url"] for p in ok if CHANNEL_WORDS.search(urllib.parse.urlparse(p["url"]).path)
                    and (p.get("daf_text") or p.get("wire_ach") or p.get("check_mail") or p.get("stock") or p.get("own_ein_shown"))]
    daf_pages = [p for p in ok if p.get("daf_widget") or p.get("sponsor_link") or (p.get("daf_text") and (p.get("own_ein_shown") or p.get("wire_ach") or p.get("check_mail") or p.get("stock")))]
    cls = ("daf_instructions" if daf_pages else "giving_page_no_daf" if giving_pages else
           "giving_contact_only" if emails else "no_giving_info_found")
    ev = {**agg, "giving_emails": "; ".join(emails),
          "evidence_url": (daf_pages[0]["url"] if daf_pages else giving_pages[0] if giving_pages else ""),
          "daf_snippet": next((p["daf_snippet"] for p in daf_pages if p.get("daf_snippet")), "")
          or next((p["daf_snippet"] for p in ok if p.get("daf_snippet")), ""),
          "pages_read": len(ok), "pages_robots_disallowed": len(w.get("disallowed", []))}
    return cls, ev


def pooled(filings: Mapping, e: str) -> dict:
    ys = [f["extract"] for f in filings.get(e, {}).values() if f.get("extract")]
    s = lambda k: sum((y.get(k) or 0.0) for y in ys)  # noqa: E731
    fs = tuple(t for y in ys for t in y["fiscal_sponsor_texts"])
    return {"years": len(ys), "contrib_1h": s("contrib_1h"), "gov_grants_1e": s("gov_grants_1e"),
            "total_revenue": s("total_revenue"), "total_expenses": s("total_expenses"),
            "grants_out": s("grants_ix1") + s("grants_ix2") + s("grants_ix3"), "grants_ix1": s("grants_ix1"),
            "grants_ix3": s("grants_ix3"), "sched_i_usd": s("sched_i_usd"), "sched_i_lines": s("sched_i_lines"),
            "na_boy_first": (min(filings[e].items())[1]["extract"] or {}).get("net_assets_boy") if ys else None,
            "na_eoy_last": (max(filings[e].items())[1]["extract"] or {}).get("net_assets_eoy") if ys else None,
            "daf_ind": "|".join(y.get("daf_ind") or "" for y in ys), "fs_hits": len(fs),
            "fs_example": fs[0] if fs else "",
            "tax_periods": ";".join(f["tax_period"] for _, f in sorted(filings.get(e, {}).items())),
            "object_ids": ";".join(f["oid"] for _, f in sorted(filings.get(e, {}).items())),
            "recipients": tuple(r for y in ys for r in y["sched_i_recipients"])}


def pt_class(p: Mapping) -> str:
    if not p["years"]:
        return "no_990"
    if p["fs_hits"]:
        return "fiscal_sponsor"
    if p["total_expenses"] and p["grants_out"] / p["total_expenses"] >= 0.5:
        return "regranting_intermediary"
    return "operating"


def ratio(a, b):
    return (a / b) if (a is not None and b) else None


def r4(x):
    return "" if x is None else round(x, 4)


def stage_report(a) -> int:
    pop = population(read_csv(SCAN_CSV))
    eins = frozenset(r["ein"] for r in pop)
    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    sy = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen}
    item = {k: x for k, x in sy.items() if itemized(x)}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: v for k, v in loaded.items() if v["status"] == "ok"}
    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    names = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in names.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    cost = read_csv(COST)
    share = {(ein9(r["ein"]), int(r["fiscal_year"])): num(r["daf_share_of_grants"]) for r in cost if r["daf_share_of_grants"]}
    weights = {k: min(1.0, max(0.0, share[k])) for k in good if share.get(k) is not None}
    dol = recipient_dollars(ann, panel, weights, eins)
    with open(os.path.join(a.work, "filings.json")) as fh:
        filings = json.load(fh)
    web_p = os.path.join(a.work, "web.json")
    web = json.load(open(web_p)) if os.path.exists(web_p) else {}
    T = dol["totals"]

    def row(s):
        e = s["ein"]
        d = dol["by_ein"].get(e, {})
        p = pooled(filings, e)
        cls, ev = channel_class(web.get(e, {}))
        intra = sum(r["amount"] for r in p["recipients"] if r["ein"] in eins and r["ein"] != e)
        intra_to = Counter()
        for r in p["recipients"]:
            if r["ein"] in eins and r["ein"] != e:
                intra_to[r["ein"]] += r["amount"]
        top_out = sorted(_group_by_fast(p["recipients"], lambda r: r["ein"] or r["name"]).items(),
                         key=lambda kv: -sum(x["amount"] for x in kv[1]))[:3]
        return {"daf_rank": s["daf_rank"], "ein": e, "name": s["name"], "ntee_cd": s["ntee_cd"], "website": s["website"],
                "named_in_queue_item": int(e in NAMED), "pass_through_class": pt_class(p),
                "top50_usd_ex_uh_filed": round(d.get("ex_uh_filed", 0)), "scan_daf_grant_usd": s["daf_grant_usd_fy2023_2024"],
                "top50_usd_all_filed": round(d.get("all_filed", 0)), "top50_usd_all_daf_weighted": round(d.get("all_daf_weighted", 0)),
                "top50_usd_fy2023": round(d.get("fy2023_filed", 0)), "top50_usd_fy2024": round(d.get("fy2024_filed", 0)),
                "share_all_filed": r4(ratio(d.get("all_filed", 0), T["all"]["filed"])),
                "share_all_daf_weighted": r4(ratio(d.get("all_daf_weighted", 0), T["all"]["daf_weighted"])),
                "top50_lines": d.get("lines", 0), "top50_grantors": d.get("grantors", 0), "top_grantors": d.get("top_grantors", ""),
                "top_grantor_share": r4(d.get("top_grantor_share")),
                "f990_tax_periods": p["tax_periods"], "f990_object_ids": p["object_ids"], "f990_years": p["years"],
                "contrib_1h_usd": round(p["contrib_1h"]), "gov_grants_1e_usd": round(p["gov_grants_1e"]),
                "total_revenue_usd": round(p["total_revenue"]), "total_expenses_usd": round(p["total_expenses"]),
                "grants_out_ix1_3_usd": round(p["grants_out"]), "grants_foreign_ix3_usd": round(p["grants_ix3"]),
                "sched_i_lines": int(p["sched_i_lines"]), "sched_i_usd": round(p["sched_i_usd"]),
                "onward_ratio_grants_to_contrib": r4(ratio(p["grants_out"], p["contrib_1h"])),
                "grants_share_of_expenses": r4(ratio(p["grants_out"], p["total_expenses"])),
                "top50_daf_share_of_contrib": r4(ratio(d.get("all_filed", 0), p["contrib_1h"])),
                "net_assets_boy_first": "" if p["na_boy_first"] is None else round(p["na_boy_first"]),
                "net_assets_eoy_last": "" if p["na_eoy_last"] is None else round(p["na_eoy_last"]),
                "net_assets_change": "" if p["na_boy_first"] is None or p["na_eoy_last"] is None else round(p["na_eoy_last"] - p["na_boy_first"]),
                "sched_i_to_population_usd": round(intra),
                "sched_i_to_population_detail": "; ".join(f"{x}:{round(v)}" for x, v in intra_to.most_common()),
                "top_sched_i_recipients": "; ".join(f"{k} ${sum(x['amount'] for x in v) / 1e6:.1f}m" for k, v in top_out),
                "daf_ind_part_iv_6": p["daf_ind"], "fiscal_sponsor_text_hits": p["fs_hits"], "fiscal_sponsor_text_example": p["fs_example"],
                "robots_state": web.get(e, {}).get("robots_state", ""), "robots_code": web.get(e, {}).get("robots_code", ""),
                "channel_class": cls, **{f"web_{k}": (int(v) if isinstance(v, bool) else v) for k, v in ev.items()}}
    rows = tuple(row(s) for s in pop)
    fields = list(dict.fromkeys(k for r in rows for k in r))
    write_csv(a.out, [{f: r.get(f, "") for f in fields} for r in rows], fields)

    def agg(sel):
        rs = [r for r in rows if sel(r)]
        s = lambda k: sum(float(r[k] or 0) for r in rs)  # noqa: E731
        return {"n": len(rs), "top50_all_filed": round(s("top50_usd_all_filed")),
                "share_all_filed": round(s("top50_usd_all_filed") / T["all"]["filed"], 5),
                "top50_all_daf_weighted": round(s("top50_usd_all_daf_weighted")),
                "share_all_daf_weighted": round(s("top50_usd_all_daf_weighted") / T["all"]["daf_weighted"], 5),
                "top50_ex_uh_filed": round(s("top50_usd_ex_uh_filed")),
                "share_ex_uh_filed": round(s("top50_usd_ex_uh_filed") / T["ex_uh"]["filed"], 5),
                "share_ex_uh_filed_with_ein": round(s("top50_usd_ex_uh_filed") / dol["totals_with_ein"]["ex_uh"]["filed"], 5),
                "contrib_1h": round(s("contrib_1h_usd")), "grants_out": round(s("grants_out_ix1_3_usd")),
                "onward_ratio": round(s("grants_out_ix1_3_usd") / s("contrib_1h_usd"), 4) if s("contrib_1h_usd") else None,
                "grants_share_of_expenses": round(s("grants_out_ix1_3_usd") / s("total_expenses_usd"), 4) if s("total_expenses_usd") else None,
                "top50_daf_share_of_contrib": round(s("top50_usd_all_filed") / s("contrib_1h_usd"), 4) if s("contrib_1h_usd") else None,
                "net_assets_change": round(sum(float(r["net_assets_change"] or 0) for r in rs)),
                "intra_population": round(s("sched_i_to_population_usd")),
                "channel": dict(Counter(r["channel_class"] for r in rs))}
    pt = lambda r: r["pass_through_class"] in ("fiscal_sponsor", "regranting_intermediary")  # noqa: E731
    summ = {"totals": {k: {b: round(v) for b, v in x.items()} for k, x in T.items()},
            "totals_with_ein": {k: {b: round(v) for b, v in x.items()} for k, x in dol["totals_with_ein"].items()},
            "sponsor_years": len(good), "daf_weight_coverage": f"{len(weights)}/{len(good)}",
            "scan_reproduced": sum(1 for r in rows if abs(r["top50_usd_ex_uh_filed"] - float(r["scan_daf_grant_usd"])) <= 1),
            "class_counts": dict(Counter(r["pass_through_class"] for r in rows)),
            "population": agg(lambda r: True), "pass_through": agg(pt), "named": agg(lambda r: r["named_in_queue_item"] == 1),
            "fiscal_sponsor": agg(lambda r: r["pass_through_class"] == "fiscal_sponsor"),
            "regranting_intermediary": agg(lambda r: r["pass_through_class"] == "regranting_intermediary"),
            "robots_log": [l for w in web.values() for l in w.get("log", [])]}
    print(json.dumps(summ, indent=1, default=str))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stage", choices=("fetch", "report"))
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--index-dir")
    ap.add_argument("--np-cache")
    ap.add_argument("--lines-cache")
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", default=OUT_CSV)
    ap.add_argument("--no-web", action="store_true")
    a = ap.parse_args(argv)
    return stage_fetch(a) if a.stage == "fetch" else stage_report(a)


if __name__ == "__main__":
    sys.exit(main())
