#!/usr/bin/env python3
"""P-QA1-05: map DAFRC FY2024 community-foundation sponsors to donor-portal / ledger vendors by EIN.

Public, passive methods only (no logins, no form submissions):
  1. Form 990 Part VII Section B contractor lines already harvested in
     data/mission-2026-11-14/form990-contractors-harvest-full.csv (tax years 2021+).
  2. Homepage per EIN from the latest e-filed Form 990 (<WebsiteAddressTxt>, first 96 KB fetched
     from the IRS e-file mirror with an HTTP Range request).
  3. Homepage crawl: read robots.txt, fetch the homepage, follow up to MAX_INTERNAL donor-login-like
     internal links and up to MAX_PORTAL portal links; record link hostnames, redirect targets,
     response headers and vendor markers in the portal page (e.g. 'Powered by GiftingNetwork').
  4. DNS CNAME lookups (DNS-over-HTTPS, dns.google) for portal hosts on the foundation's own domain.
  5. crt.sh certificate-transparency listings for vendor tenant domains (2021+ certificates), matched
     to foundations only when the tenant label equals the foundation's own website domain stem.
Politeness: <=1 request/second per host (global per-host throttle), robots.txt honoured for crawl
fetches, identifying generic User-Agent, every response cached so reruns hit no network.

Usage:
  python3 scripts/mission_cf_vendor_map.py --fetch            # network + cache
  python3 scripts/mission_cf_vendor_map.py                    # rebuild outputs from cache only
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import csv
import datetime as dt
import functools
import hashlib
import html
import json
import os
import re
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from typing import Iterable, Mapping, Sequence

DATA = "data/mission-2026-11-14"
DAFRC_CSV = f"{DATA}/dafrc-sponsor-schedule-d-fy2019-2024.csv"
RETURNS_CSV = f"{DATA}/form990-returns-schedule-d-harvest-full.csv"
CONTRACTORS_CSV = f"{DATA}/form990-contractors-harvest-full.csv"
V2_CSV = f"{DATA}/community-foundation-rails-portals-2026-v2.csv"
EDGE_GLOB_PREFIX = f"{DATA}/relationship-graph-edges"
OUT_CSV = f"{DATA}/cf-vendor-map-by-ein.csv"
OUT_SIGNALS = f"{DATA}/cf-vendor-map-signals.csv"
OUT_SUMMARY = f"{DATA}/cf-vendor-map-summary.json"
OUT_EDGES = f"{DATA}/relationship-graph-edges-additions-9.csv"
RETRIEVED = "2026-11-14"
UA = "Mozilla/5.0 (compatible; DAF-landscape-public-research/1.0; passive, robots-respecting)"
MAX_INTERNAL, MAX_PORTAL = 3, 3
MIN_INTERVAL = 1.05  # seconds between requests to one host

# ---------------------------------------------------------------- vendor signatures
# (family, product label, ledger_implied, host regex, html-marker regex, generic?)
# generic=True: the host also serves non-donor uses (grant apps, fundraising), so a link counts
# only in a donor-login context.
VENDORS = (
    ("Foundant", "Foundant CommunitySuite", "yes", r"(^|\.)fcsuite\.com$|communitysuite", r"fcsuite\.com|CommunitySuite", False),
    ("Ren / Stellar iPhi", "Ren (Stellar) iPhi DonorView", "yes", r"(^|\.)iphiview\.com$|stellartechsol\.com$|(^|\.)donorfirstx?\.(org|com)$", r"iphiview\.com|stellartechsol|DonorFirst", False),
    ("Foundation Cloud (spectrumportal.net; NPact [R])", "Foundation Cloud portal (spectrumportal.net)", "yes", r"(^|\.)spectrumportal\.net$", r"spectrumportal\.net", False),
    ("akoyaGO", "akoyaGO GOfund", "yes", r"(^|\.)akoyago\.com$", r"akoyago\.com|akoyaGO", False),
    ("DonorSphere / FidTech", "DonorSphere", "yes", r"(^|\.)donorsphere\.(org|com)$|fidtechpartners\.com$", r"Powered by DonorSphere|donorsphere\.org", False),
    ("Give Interactive", "Give Interactive", "yes", r"(^|\.)giveinteractive\.com$", r"giveinteractive\.com", False),
    ("GiftingNetwork", "GiftingNetwork", "unknown", r"giftingnetwork", r"Powered by GiftingNetwork|giftingnetwork\.com", False),
    ("Blackbaud", "Blackbaud DonorCentral", "yes", r"(^|\.)edonorcentral\.com$|donorcentral\.(com|net)$", r"edonorcentral\.com", False),
    ("donor-portal.org (unidentified white-label)", "donor-portal.org white-label", "unknown", r"(^|\.)donor-portal\.org$", r"donor-portal\.org|giving_portal_client", False),
    ("Blackbaud", "Blackbaud hosted (NetCommunity/other)", "unknown", r"blackbaud(hosting)?\.(com|net)$|(^|\.)bbnc\.|netcommunity", r"BLACKBAUD\.netcommunity|blackbaudhosting\.com|netcommunity", True),
    ("Salesforce", "Salesforce Experience Cloud", "unknown", r"(^|\.)my\.site\.com$|(^|\.)force\.com$|salesforce-sites\.com$|siteforce\.com$", r"/s/sfsites/|force\.com|x-sfdc", True),
    ("Microsoft Power Pages", "Microsoft Power Pages", "unknown", r"powerappsportals\.(com|us)$|powerpages\.microsoft\.com$", r"powerappsportals|Microsoft\.Dynamic365\.Portal", True),
    ("SmartSimple", "SmartSimple", "unknown", r"(^|\.)smartsimple\.(com|ca)$", r"smartsimple", True),
    ("Bonterra", "Bonterra CyberGrants", "unknown", r"cybergrants\.com$", r"cybergrants", True),
)
VENDOR_HOST_RE = tuple((v[0], v[1], v[2], re.compile(v[3], re.I), v[5]) for v in VENDORS)
VENDOR_MARK_RE = tuple((v[0], v[1], v[2], re.compile(v[4], re.I)) for v in VENDORS)

# 990 Part VII-B contractor name -> family (only vendors whose business includes CF fund ledgers/portals)
C990 = (
    ("Foundant", "Foundant Technologies (990; product not stated)", re.compile(r"FOUNDANT", re.I)),
    ("Ren / Stellar iPhi", "Stellar/Ren (990)", re.compile(r"STELLAR TECH|\bREN TECHNOLOGY|RENAISSANCE (ACQUISITION|PHILANTHROPIC)", re.I)),
    ("Foundation Cloud (spectrumportal.net; NPact [R])", "NPact (990)", re.compile(r"\bNPACT\b", re.I)),
    ("akoyaGO", "Akoya (990)", re.compile(r"\bAKOYA", re.I)),
    ("DonorSphere / FidTech", "FidTech (990)", re.compile(r"FIDTECH|FIDUCIARY TECHNOLOGY PARTNERS", re.I)),
    ("Give Interactive", "Give Interactive (990)", re.compile(r"GIVE INTERACTIVE", re.I)),
    ("GiftingNetwork", "GiftingNetwork (990)", re.compile(r"GIFTING ?NETWORK", re.I)),
    ("Blackbaud", "Blackbaud (990; product not stated)", re.compile(r"BLACKBAUD|MICROEDGE", re.I)),
)
STRONG_990 = frozenset({"Foundant", "Ren / Stellar iPhi", "Foundation Cloud (spectrumportal.net; NPact [R])", "akoyaGO",
                        "DonorSphere / FidTech", "Give Interactive", "GiftingNetwork"})

CT_DOMAINS = (("fcsuite.com", "Foundant"), ("iphiview.com", "Ren / Stellar iPhi"),
              ("spectrumportal.net", "Foundation Cloud (spectrumportal.net; NPact [R])"),
              ("donorsphere.org", "DonorSphere / FidTech"), ("giveinteractive.com", "Give Interactive"),
              ("donor-portal.org", "donor-portal.org (unidentified white-label)"))
CT_NOISE = re.compile(r"^(www|api|mail|demo|test|sandbox|staging|stage|dev|uat|qa|support|help|docs|status|auth|login|admin|portal|app|cdn|static|sftp|int|ftp|vpn|remote|autodiscover|webmail|beta|preview|training|train|sso|origin)$")
CT_SUFFIX = re.compile(r"-(staging|stage|sandbox|test|uat|dev|qa|demo|sftp|innov|train|training|preview|beta|int)$")

LOGIN_TXT = re.compile(r"log\s*-?\s*in|sign\s*-?\s*in|fund\s*-?\s*holder|donor\s*(portal|login|log|center|centre|central|access|view|sphere|services)|"
                       r"my\s*fund|access\s+(your|my)\s+fund|fund\s+(advisor|adviser|manager|login|portal|access|account)|manage\s+(your|my)\s+fund|"
                       r"online\s+access|\bportal\b|account\s+access|giving\s+(portal|center)|\bmy[a-z]{2,8}\b", re.I)
DONOR_TXT = re.compile(r"donor|fund|advis|holder|giving|\bmy[a-z]{2,8}\b|account", re.I)
EXCLUDE_TXT = re.compile(r"grant\s*(application|portal|seeker|applicant|report|lifecycle)|apply|scholarship|nonprofit|non-profit|grantee|applicant|"
                         r"employment|career|newsletter|subscribe|e-?news|facebook|twitter|linkedin|instagram|youtube|board\s+portal|staff|volunteer|event|ticket", re.I)
EXCLUDE_PATH = re.compile(r"grantee|grant-?app|grantseeker|funding|apply|applica|scholar|nonprofit|/np/|vendor|employ", re.I)
LOGIN_HREF = re.compile(r"login|log-in|signin|sign-in|portal|fundholder|fund-holder|donor-?(login|portal|access|central)|myfund|access-your-fund|fund-access|donorview|/erp/", re.I)

ANCHOR_RE = re.compile(r"<a\b([^>]*)>(.*?)</a\s*>", re.I | re.S)
HREF_RE = re.compile(r"""href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
ATTR_TXT_RE = re.compile(r"""(?:title|aria-label)\s*=\s*["']([^"']+)["']""", re.I)
TAG_RE = re.compile(r"<[^>]+>")
META_REFRESH_RE = re.compile(r"""<meta[^>]+http-equiv\s*=\s*["']?refresh["']?[^>]*content\s*=\s*["'][^"']*url\s*=\s*([^"'>\s]+)""", re.I)
JS_REDIRECT_RE = re.compile(r"""(?:window\.)?location(?:\.href)?\s*=\s*["'](https?://[^"']+)["']""", re.I)

# ---------------------------------------------------------------- small pure helpers
def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def ein9(x: str) -> str:
    d = re.sub(r"\D", "", x or "")
    return d.zfill(9) if d else ""


def num(x) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def host_of(url: str) -> str:
    try:
        return (urllib.parse.urlsplit(url).hostname or "").lower().rstrip(".")
    except ValueError:
        return ""


def reg_domain(host: str) -> str:
    parts = host.split(".")
    two_level = {"co.uk", "org.uk", "com.au", "org.au"}
    return ".".join(parts[-3:]) if ".".join(parts[-2:]) in two_level else ".".join(parts[-2:])


def domain_stem(host: str) -> str:
    return reg_domain(host).split(".")[0]


def clean_website(raw: str) -> str:
    s = (raw or "").strip().strip("/").replace(" ", "")
    if not s or re.fullmatch(r"(?i)n/?a|none|na|-+|0", s) or "." not in s:
        return ""
    s = re.sub(r"(?i)^https?://", "", s)
    s = re.sub(r"(?i)^https?:", "", s)
    host = s.split("/")[0].lower().strip(".")
    return f"https://{host}/" if re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", host) else ""


def vendor_by_host(host: str) -> tuple | None:
    return next(((fam, prod, led, generic) for fam, prod, led, rx, generic in VENDOR_HOST_RE if rx.search(host)), None)


def vendor_by_marker(text: str, generic_ok: bool) -> tuple | None:
    hits = ((fam, prod, led, rx.search(text)) for fam, prod, led, rx in VENDOR_MARK_RE)
    return next(((fam, prod, led, m.group(0)) for fam, prod, led, m in hits if m), None)


def anchors(page_html: str, base: str) -> tuple[tuple[str, str], ...]:
    def one(m):
        attrs, inner = m.group(1), m.group(2)
        h = HREF_RE.search(attrs)
        if not h:
            return None
        href = html.unescape(next(g for g in h.groups() if g is not None)).strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            return None
        text = " ".join(filter(None, (html.unescape(TAG_RE.sub(" ", inner)), *ATTR_TXT_RE.findall(attrs))))
        try:
            return urllib.parse.urljoin(base, href), re.sub(r"\s+", " ", text).strip()[:160]
        except ValueError:
            return None
    return tuple(a for a in map(one, ANCHOR_RE.finditer(page_html or "")) if a)


def is_login_context(url: str, text: str) -> bool:
    blob = f"{text} {urllib.parse.urlsplit(url).path}"
    if EXCLUDE_TXT.search(text) or EXCLUDE_TXT.search(urllib.parse.urlsplit(url).path) or EXCLUDE_PATH.search(url):
        return False
    return bool(LOGIN_TXT.search(text) and (DONOR_TXT.search(blob) or re.search(r"log\s*-?\s*in|sign\s*-?\s*in", text, re.I))) or bool(
        LOGIN_HREF.search(url) and DONOR_TXT.search(blob))


def login_score(url: str, text: str) -> int:
    return (3 * bool(re.search(r"donor|fund", text, re.I)) + 2 * bool(re.search(r"log\s*-?\s*in|sign\s*-?\s*in|portal|access", text, re.I))
            + bool(LOGIN_HREF.search(url)))


# ---------------------------------------------------------------- network layer (cached, throttled)
class Net:
    def __init__(self, cache_dir: str, fetch: bool):
        self.cache_dir, self.fetch = cache_dir, fetch
        os.makedirs(cache_dir, exist_ok=True)
        self._locks: dict[str, threading.Lock] = collections.defaultdict(threading.Lock)
        self._last: dict[str, float] = {}
        self._meta = threading.Lock()

    def _throttle(self, host: str) -> None:
        with self._meta:
            lock = self._locks[host]
        with lock:
            wait = self._last.get(host, 0) + MIN_INTERVAL - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last[host] = time.monotonic()

    def get(self, url: str, headers: Mapping | None = None, timeout: int = 25, max_bytes: int = 1_500_000, cache_fail: bool = True) -> dict:
        key = hashlib.sha256((url + json.dumps(headers or {}, sort_keys=True)).encode()).hexdigest()
        path = os.path.join(self.cache_dir, key[:2], key + ".json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        if not self.fetch:
            return {"url": url, "status": "not_cached", "final_url": "", "headers": {}, "body": ""}
        self._throttle(host_of(url))
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/json,*/*;q=0.8",
                                                   "Accept-Language": "en-US,en;q=0.8", **(headers or {})})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read(max_bytes)
                out = {"url": url, "status": r.status, "final_url": r.geturl(), "headers": {k.lower(): v for k, v in r.headers.items()},
                       "body": body.decode(r.headers.get_content_charset() or "utf-8", "replace")}
        except urllib.error.HTTPError as e:
            out = {"url": url, "status": e.code, "final_url": e.geturl() if hasattr(e, "geturl") else url,
                   "headers": {k.lower(): v for k, v in (e.headers or {}).items()}, "body": ""}
            try:
                out["body"] = e.read(200_000).decode("utf-8", "replace")
            except Exception:  # noqa: BLE001
                pass
        except Exception as e:  # noqa: BLE001 - network errors are data here
            out = {"url": url, "status": f"error:{type(e).__name__}:{str(e)[:120]}", "final_url": "", "headers": {}, "body": ""}
        if cache_fail or out["status"] == 200:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(out, fh)
        return out


@functools.lru_cache(maxsize=None)
def _robots_for(net_id: int, origin: str) -> urllib.robotparser.RobotFileParser | None:
    net = _NETS[net_id]
    res = net.get(origin + "/robots.txt", timeout=15, max_bytes=300_000)
    rp = urllib.robotparser.RobotFileParser()
    if isinstance(res["status"], int) and res["status"] == 200 and "html" not in res["headers"].get("content-type", "html").lower():
        rp.parse(res["body"].splitlines())
        return rp
    if isinstance(res["status"], int) and res["status"] in (401, 403):
        rp.parse(["User-agent: *", "Disallow: /"])
        return rp
    return None  # 404 / error / HTML: no robots restrictions published


_NETS: dict[int, Net] = {}


def allowed(net: Net, url: str) -> bool:
    sp = urllib.parse.urlsplit(url)
    rp = _robots_for(id(net), f"{sp.scheme}://{sp.netloc}")
    return True if rp is None else rp.can_fetch(UA, url)


def polite_get(net: Net, url: str) -> dict:
    if not allowed(net, url):
        return {"url": url, "status": "robots_disallowed", "final_url": "", "headers": {}, "body": ""}
    return net.get(url)


def dns_cname_chain(net: Net, host: str) -> tuple[str, ...]:
    def step(name, depth):
        if depth > 5:
            return ()
        res = net.get("https://dns.google/resolve?" + urllib.parse.urlencode({"name": name, "type": "CNAME"}), {"Accept": "application/dns-json"}, timeout=15)
        try:
            ans = [a["data"].rstrip(".").lower() for a in json.loads(res["body"] or "{}").get("Answer", []) if a.get("type") == 5]
        except (ValueError, KeyError):
            ans = []
        return tuple(ans[:1]) + (step(ans[0], depth + 1) if ans else ())
    return step(host, 0)


# ---------------------------------------------------------------- inputs
def cf_universe() -> tuple[dict, ...]:
    rows = (r for r in read_csv(DAFRC_CSV) if r["type"] == "Community Foundation" and r["fiscal_year_end"] == "2024")
    return tuple(sorted(({"ein": ein9(r["ein"]), "name": r["name"], "fy2024_daf_assets": num(r["eoy_daf_assets"])} for r in rows),
                        key=lambda r: -r["fy2024_daf_assets"]))


def latest_xml_urls(eins: frozenset[str]) -> dict[str, tuple[str, ...]]:
    rows = sorted((r for r in read_csv(RETURNS_CSV) if ein9(r["ein"]) in eins and r["xml_status"] == "ok"),
                  key=lambda r: (r["tax_period_end"], r["return_ts"]), reverse=True)
    grouped = collections.defaultdict(list)
    for r in rows:
        grouped[ein9(r["ein"])].append(r["xml_url"])
    return {k: tuple(v) for k, v in grouped.items()}


def website_from_990(net: Net, urls: Sequence[str]) -> tuple[str, str]:
    for u in urls[:3]:
        res = net.get(u, {"Range": "bytes=0-98303"}, timeout=40, max_bytes=98304)
        m = re.search(r"<WebsiteAddressTxt>([^<]+)</WebsiteAddressTxt>", res.get("body", ""))
        site = clean_website(html.unescape(m.group(1))) if m else ""
        if site:
            return site, u
    return "", (urls[0] if urls else "")


def contractor_signals(eins: frozenset[str]) -> dict[str, tuple[dict, ...]]:
    out = collections.defaultdict(list)
    for r in read_csv(CONTRACTORS_CSV):
        e = ein9(r["ein"])
        if e not in eins or num(r["tax_year"]) < 2021:
            continue
        hit = next(((fam, prod) for fam, prod, rx in C990 if rx.search(r["contractor_name"])), None)
        if hit:
            out[e].append({"family": hit[0], "product": hit[1], "ledger_implied": "yes" if hit[0] in STRONG_990 else "unknown",
                           "evidence_type": "990_part_vii_b_contractor", "evidence_url": r["filing_page_url"],
                           "detail": f"TY{r['tax_year']} {r['contractor_name']} '{r['services']}' ${int(num(r['compensation'])):,}",
                           "strength": 2 if hit[0] in STRONG_990 else 1, "first_party": True})
    return dict(out)


# ---------------------------------------------------------------- crawl one foundation
def signal(fam, prod, led, etype, url, detail, strength, context=True) -> dict:
    return {"family": fam, "product": prod, "ledger_implied": led, "evidence_type": etype, "evidence_url": url,
            "detail": detail[:300], "strength": strength, "first_party": True, "login_context": context}


def link_signals(links: Iterable[tuple[str, str]], page_url: str, own_domain: str) -> tuple[list, list, list]:
    """Return (vendor signals, internal candidate pages, external/subdomain portal candidates)."""
    sigs, internal, portals = [], [], []
    for url, text in links:
        h = host_of(url)
        if not h:
            continue
        ctx = is_login_context(url, text)
        v = vendor_by_host(h)
        if v and (ctx or not v[3]):
            sigs.append(signal(v[0], v[1], v[2], "homepage_link_vendor_host" if ctx else "site_link_vendor_host", page_url,
                               f"link '{text[:60]}' -> {url[:150]}", 3 if ctx else 2, ctx))
        elif ctx and not v:
            bucket = internal if h in (own_domain, "www." + own_domain) else portals
            bucket.append((login_score(url, text), url, text))
    return sigs, internal, portals


def inspect_portal(net: Net, url: str, text: str, own_domain: str) -> list[dict]:
    h = host_of(url)
    sigs = []
    res = polite_get(net, url)
    final = res.get("final_url") or ""
    fh = host_of(final)
    if fh and fh != h:
        v = vendor_by_host(fh)
        if v:
            sigs.append(signal(v[0], v[1], v[2], "portal_redirect_vendor_host", url, f"'{text[:50]}' {url[:100]} redirects to {final[:150]}", 3))
    hdrs = res.get("headers", {})
    if any(k.startswith("x-sfdc") for k in hdrs) or "salesforce" in hdrs.get("server", "").lower():
        sigs.append(signal("Salesforce", "Salesforce Experience Cloud", "unknown", "portal_response_header", final or url,
                           f"{url[:120]} response header x-sfdc*/server Salesforce", 3))
    body = res.get("body", "")
    if body:
        m = vendor_by_marker(body, True)
        if m:
            sigs.append(signal(m[0], m[1], m[2], "portal_page_marker", final or url, f"'{text[:50]}' page {(final or url)[:120]} contains '{m[3][:60]}'", 3))
        for nxt in filter(None, (*(META_REFRESH_RE.findall(body) or ()), *(JS_REDIRECT_RE.findall(body)[:2]))):
            v = vendor_by_host(host_of(urllib.parse.urljoin(final or url, nxt)))
            if v:
                sigs.append(signal(v[0], v[1], v[2], "portal_page_redirect_vendor_host", final or url, f"{url[:100]} client-side redirect to {nxt[:120]}", 3))
    if reg_domain(h) == own_domain or (fh and reg_domain(fh) == own_domain):
        for target in (h, fh):
            if not target or reg_domain(target) != own_domain:
                continue
            chain = dns_cname_chain(net, target)
            v = next((vendor_by_host(c) for c in chain if vendor_by_host(c)), None)
            if v:
                sigs.append(signal(v[0], v[1], v[2], "dns_cname", f"https://dns.google/resolve?name={target}&type=CNAME",
                                   f"{target} CNAME -> {' -> '.join(chain)[:200]}", 3))
            elif chain:
                sigs.append({"family": "", "product": "", "ledger_implied": "", "evidence_type": "dns_cname_unmatched",
                             "evidence_url": f"https://dns.google/resolve?name={target}&type=CNAME", "detail": f"{target} CNAME -> {' -> '.join(chain)[:200]}",
                             "strength": 0, "first_party": True, "login_context": True})
    status = res.get("status")
    sigs.append({"family": "", "product": "", "ledger_implied": "", "evidence_type": "portal_fetch", "evidence_url": url,
                 "detail": f"status={status} final={final[:150]}", "strength": 0, "first_party": True, "login_context": True})
    return sigs


def crawl(net: Net, cfrow: Mapping) -> dict:
    home = cfrow["homepage"]
    if not home:
        return {"crawl_status": "no_homepage", "signals": [], "portal_candidates": []}
    own = reg_domain(host_of(home))
    res = polite_get(net, home)
    if res["status"] == "robots_disallowed":
        return {"crawl_status": "robots_disallowed", "signals": [], "portal_candidates": []}
    if not res.get("body"):
        hh = host_of(home)
        alt = "https://" + (hh[4:] if hh.startswith("www.") else "www." + hh) + "/"
        res = polite_get(net, alt) if alt else res
    if not res.get("body"):
        return {"crawl_status": f"homepage_{res['status']}", "signals": [], "portal_candidates": []}
    base = res.get("final_url") or home
    own = reg_domain(host_of(base)) or own
    sigs, internal, portals = link_signals(anchors(res["body"], base), base, own)
    seen = {base}
    for _, url, text in sorted(set(internal), key=lambda t: -t[0])[:MAX_INTERNAL]:
        if url.split("#")[0] in seen:
            continue
        seen.add(url.split("#")[0])
        sub = polite_get(net, url)
        fh = host_of(sub.get("final_url") or "")
        if fh and reg_domain(fh) != own:  # internal link redirected off-site: treat as portal
            v = vendor_by_host(fh)
            if v:
                sigs.append(signal(v[0], v[1], v[2], "homepage_link_redirect_vendor_host", url, f"'{text[:50]}' {url[:100]} -> {sub['final_url'][:150]}", 3))
            else:
                portals.append((login_score(url, text), sub["final_url"], text))
            continue
        s2, _, p2 = link_signals(anchors(sub.get("body", ""), sub.get("final_url") or url), sub.get("final_url") or url, own)
        sigs.extend(s2)
        portals.extend(p2)
    if not any(s["strength"] >= 3 for s in sigs):
        uniq = {}
        for sc, url, text in sorted(portals, key=lambda t: -t[0]):
            uniq.setdefault(host_of(url), (sc, url, text))
        for _, url, text in list(uniq.values())[:MAX_PORTAL]:
            sigs.extend(inspect_portal(net, url, text, own))
    return {"crawl_status": f"ok_{res['status']}", "signals": sigs,
            "portal_candidates": [u for _, u, _ in sorted(portals, key=lambda t: -t[0])][:5]}


# ---------------------------------------------------------------- certificate transparency
def ct_tenants(net: Net) -> dict[str, list[dict]]:
    """family -> [{label, host, first, last}] for 2021+ certificates."""
    out = {}
    for dom, fam in CT_DOMAINS:
        def pull(q):
            for attempt in range(4):
                res = net.get("https://crt.sh/?" + urllib.parse.urlencode({"q": q, "output": "json"}), timeout=120, max_bytes=60_000_000, cache_fail=False)
                if res.get("status") == 200 or not net.fetch:
                    return res
                time.sleep(8 * (attempt + 1))
            return res
        pulls = tuple(map(pull, (dom, f"%.{dom}")))
        certs, status = [], "/".join(str(p.get("status")) for p in pulls)
        for res in pulls:
            try:
                certs.extend(json.loads(res.get("body") or "[]") if res.get("status") == 200 else [])
            except ValueError:
                pass
        res = {"status": status}
        hosts = collections.defaultdict(list)
        for c in certs:
            if (c.get("not_before") or "") < "2021-01-01":
                continue
            for n in (c.get("name_value") or "").lower().split("\n"):
                n = n.strip().lstrip("*.")
                if n.endswith("." + dom) and n != dom:
                    hosts[n].append(c["not_before"][:10])
        out[fam] = [{"host": h, "label": h[: -len(dom) - 1].split(".")[-1], "first": min(d), "last": max(d), "domain": dom,
                     "status": res.get("status")} for h, d in sorted(hosts.items())]
    return out


def ct_signals(ct: Mapping[str, list], universe: Sequence[Mapping]) -> dict[str, list[dict]]:
    stems = collections.defaultdict(list)
    for r in universe:
        if r["homepage"]:
            stems[domain_stem(host_of(r["homepage"]))].append(r["ein"])
    out = collections.defaultdict(list)
    for fam, tenants in ct.items():
        for t in tenants:
            raw = t["label"]
            label = CT_SUFFIX.sub("", raw)
            if CT_NOISE.match(label) or len(label) < 3:
                continue
            eins = stems.get(label, [])
            if len(eins) == 1:
                prod = next(v[1] for v in VENDORS if v[0] == fam)
                test_only = raw != label
                out[eins[0]].append({"family": fam, "product": prod, "ledger_implied": "yes" if fam in STRONG_990 else "unknown",
                                     "evidence_type": "ct_tenant_label_matches_domain_stem",
                                     "evidence_url": "https://crt.sh/?q=%25." + t["domain"],
                                     "detail": f"cert host {t['host']} (first {t['first']}, last {t['last']}){' [non-production label]' if test_only else ''}",
                                     "strength": 1, "first_party": False, "login_context": False, "ct_last": t["last"]})
    return dict(out)


# ---------------------------------------------------------------- decision
V2_FAMILY = ((r"Foundant", "Foundant"), (r"iPhi|Stellar", "Ren / Stellar iPhi"), (r"spectrumportal|Foundation Cloud", "Foundation Cloud (spectrumportal.net; NPact [R])"),
             (r"Akoya", "akoyaGO"), (r"DonorSphere", "DonorSphere / FidTech"), (r"GiftingNetwork", "GiftingNetwork"),
             (r"Salesforce", "Salesforce"), (r"SmartSimple", "SmartSimple"), (r"Power Pages", "Microsoft Power Pages"),
             (r"Blackbaud", "Blackbaud"), (r"donor-portal\.org", "donor-portal.org (unidentified white-label)"))


def v2_signals() -> dict[str, list[dict]]:
    out = {}
    for r in read_csv(V2_CSV):
        fam = next((f for rx, f in V2_FAMILY if re.search(rx, r["portal_vendor"], re.I)), "")
        if fam and not re.match(r"(?i)unknown", r["portal_vendor"]):
            out[ein9(r["ein"])] = [{"family": fam, "product": r["portal_vendor"], "ledger_implied": "",
                                    "evidence_type": "repo_v2_manual_check", "evidence_url": r["source_urls"].split(" ; ")[0],
                                    "detail": r["portal_evidence"][:280], "strength": 3, "first_party": True, "login_context": True}]
    return out


PRIORITY = {"homepage_link_vendor_host": 9, "homepage_link_redirect_vendor_host": 9, "portal_redirect_vendor_host": 9,
            "portal_page_redirect_vendor_host": 8, "dns_cname": 8, "portal_page_marker": 7, "portal_response_header": 7,
            "repo_v2_manual_check": 6, "site_link_vendor_host": 5, "990_part_vii_b_contractor": 4, "ct_tenant_label_matches_domain_stem": 1}


def decide(row: Mapping, sigs: Sequence[Mapping]) -> dict:
    named = [s for s in sigs if s.get("family")]
    crawl_named = [s for s in named if s["evidence_type"] not in ("990_part_vii_b_contractor", "ct_tenant_label_matches_domain_stem", "repo_v2_manual_check")]
    fams = collections.Counter(s["family"] for s in named)
    best = max(named, key=lambda s: (PRIORITY.get(s["evidence_type"], 0), fams[s["family"]], s.get("login_context", False)), default=None)
    if not best:
        portal = next((s for s in sigs if s["evidence_type"] == "portal_fetch"), None)
        return {"portal_vendor": "unidentified (portal found, no vendor marker)" if portal else "unmapped", "vendor_family": "Unidentified portal" if portal else "Unmapped",
                "portal_url": portal["evidence_url"] if portal else "", "evidence_type": portal["evidence_type"] if portal else "",
                "evidence_url": portal["evidence_url"] if portal else "", "confidence": "none", "ledger_implied": "unknown",
                "evidence_detail": portal["detail"] if portal else "", "corroborating_evidence": ""}
    corroborate = sorted({f"{s['evidence_type']}: {s['detail'][:110]}" for s in named if s is not best and s["family"] == best["family"]})
    conflicts = sorted({f"{s['family']} ({s['evidence_type']})" for s in named if s["family"] != best["family"]})
    et = best["evidence_type"]
    if PRIORITY.get(et, 0) >= 6:
        conf = "high"
    elif et == "site_link_vendor_host":
        conf = "high" if best["family"] in STRONG_990 or len(corroborate) else "medium"
    elif et == "990_part_vii_b_contractor":
        conf = "medium" if best["family"] in STRONG_990 else "low"
    else:
        conf = "medium" if any(s["evidence_type"] == "990_part_vii_b_contractor" and s["family"] == best["family"] for s in named) else "low"
    portal_url = ""
    m = re.search(r"https?://[^\s'\"]+", best["detail"])
    if et in ("homepage_link_vendor_host", "site_link_vendor_host", "homepage_link_redirect_vendor_host", "portal_redirect_vendor_host", "portal_page_redirect_vendor_host") and m:
        portal_url = m.group(0)
    elif et in ("portal_page_marker", "portal_response_header", "dns_cname"):
        portal_url = best["evidence_url"] if et != "dns_cname" else "https://" + best["detail"].split(" ")[0]
    elif et == "repo_v2_manual_check":
        mm = re.search(r"([a-z0-9-]+(\.[a-z0-9-]+)+\.(com|org|net)(/[^\s;')]*)?)", best["detail"])
        portal_url = ("https://" + mm.group(1)) if mm else ""
    elif et == "ct_tenant_label_matches_domain_stem":
        portal_url = "https://" + best["detail"].split(" ")[2]
    prod = best["product"]
    if best["family"] == "Foundant" and any("fcsuite" in s["detail"] or "CommunitySuite" in s["product"] for s in named if s["family"] == "Foundant"):
        prod = "Foundant CommunitySuite"
    led = best["ledger_implied"] or next((v[2] for v in VENDORS if v[0] == best["family"]), "unknown")
    return {"portal_vendor": prod, "vendor_family": best["family"], "portal_url": portal_url, "evidence_type": et,
            "evidence_url": best["evidence_url"], "confidence": conf, "ledger_implied": led,
            "evidence_detail": best["detail"], "corroborating_evidence": " | ".join(corroborate)[:600],
            "conflicting_signals": "; ".join(conflicts)[:300],
            "crawl_vendor_family": max(crawl_named, key=lambda s: PRIORITY.get(s["evidence_type"], 0))["family"] if crawl_named else ""}


# ---------------------------------------------------------------- outputs
def shares(rows: Sequence[Mapping], key: str = "vendor_family", min_conf: frozenset = frozenset({"high", "medium"})) -> list[dict]:
    tot_n, tot_a = len(rows), sum(r["fy2024_daf_assets"] for r in rows)
    g = collections.defaultdict(lambda: [0, 0.0])
    for r in rows:
        fam = (r[key] if r["confidence"] in min_conf else "Unidentified portal" if r["vendor_family"] == "Unidentified portal"
               else "Unmapped (low-confidence signal only)" if r["confidence"] in ("low", "medium", "high") else "Unmapped")
        g[fam][0] += 1
        g[fam][1] += r["fy2024_daf_assets"]
    return [{"vendor_family": k, "cfs": n, "share_cfs": round(n / tot_n, 4), "daf_assets_usd": round(a), "share_daf_assets": round(a / tot_a, 4)}
            for k, (n, a) in sorted(g.items(), key=lambda kv: -kv[1][1])]


def existing_edges() -> tuple[dict, ...]:
    d = os.path.dirname(EDGE_GLOB_PREFIX)
    files = sorted(f for f in os.listdir(d) if f.startswith("relationship-graph-edges") and f.endswith(".csv") and "additions-9" not in f)
    return tuple(r for f in files for r in read_csv(os.path.join(d, f)))


EDGE_VENDOR = {"Foundant": "Foundant Technologies", "Ren / Stellar iPhi": "Stellar Technology Solutions (iPhi)",
               "Foundation Cloud (spectrumportal.net; NPact [R])": "NPact (Foundation Cloud)", "akoyaGO": "Akoya",
               "DonorSphere / FidTech": "DonorSphere", "Give Interactive": "Give Interactive", "GiftingNetwork": "GiftingNetwork",
               "Blackbaud": "Blackbaud", "Salesforce": "Salesforce", "Microsoft Power Pages": "Microsoft (Power Pages)",
               "SmartSimple": "SmartSimple", "Bonterra": "Bonterra"}


def name_key(s: str) -> frozenset:
    stop = {"the", "inc", "of", "for", "community", "foundation", "fdn", "and", "&", "a", "trust", "area", "greater", "county", "co"}
    return frozenset(t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in stop)


def v2_names() -> dict[str, str]:
    return {ein9(r["ein"]): r["foundation"] for r in read_csv(V2_CSV)}


def edges(rows: Sequence[Mapping]) -> list[dict]:
    have = {(e["source_entity"], name_key(e["target_entity"])) for e in existing_edges()}
    alias = v2_names()

    def known(r):
        keys = {k for k in (name_key(r["name"]), name_key(alias.get(r["ein"], ""))) if len(k) >= 1}
        return any((EDGE_VENDOR[r["vendor_family"]], k) in have for k in keys)
    keep = [r for r in rows if r["vendor_family"] in EDGE_VENDOR and r["confidence"] in ("high", "medium")
            and r["evidence_type"] != "repo_v2_manual_check" and not known(r)]
    out = []
    for i, r in enumerate(keep, 1):
        fp = r["evidence_type"] != "ct_tenant_label_matches_domain_stem" and r["confidence"] == "high"
        status = "confirmed" if fp or (r["evidence_type"] == "990_part_vii_b_contractor" and r["vendor_family"] in STRONG_990) else "inferred"
        display = f"{alias.get(r['ein'], r['name'])} (EIN {r['ein'][:2]}-{r['ein'][2:]}; {reg_domain(host_of(r['homepage'])) or 'no website'})"
        out.append({"edge_id": f"EI{i:03d}", "source_entity": EDGE_VENDOR[r["vendor_family"]], "source_type": "technology_vendor",
                    "target_entity": display, "target_type": "daf_sponsor",
                    "relationship_type": "technology_provider", "status": status,
                    "evidence_summary": f"{r['portal_vendor']}: {r['evidence_type']} - {r['evidence_detail'][:220]}",
                    "source_url": r["evidence_url"], "source_date": "live 2026-11-14" if "990" not in r["evidence_type"] else r["evidence_detail"][:6],
                    "accessed_date": RETRIEVED,
                    "notes": f"P-QA1-05 automated map (scripts/mission_cf_vendor_map.py); confidence {r['confidence']}; portal vendor, ledger_implied={r['ledger_implied']}"})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="allow network fetches (otherwise cache only)")
    ap.add_argument("--cache-dir", default=os.path.join(tempfile.gettempdir(), "cf_vendor_map_cache"))
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    net = Net(a.cache_dir, a.fetch)
    _NETS[id(net)] = net
    uni = cf_universe()[: a.limit or None]
    eins = frozenset(r["ein"] for r in uni)
    xmls = latest_xml_urls(eins)
    with cf.ThreadPoolExecutor(8) as ex:  # one host (S3) -> throttle keeps it at <=1 req/s
        sites = dict(zip((r["ein"] for r in uni), ex.map(lambda r: website_from_990(net, xmls.get(r["ein"], ())), uni)))
    uni = tuple({**r, "homepage": sites[r["ein"]][0], "homepage_source": sites[r["ein"]][1]} for r in uni)
    print(f"universe {len(uni)}; homepages {sum(1 for r in uni if r['homepage'])}", flush=True)
    c990 = contractor_signals(eins)
    ct = ct_tenants(net)
    cts = ct_signals(ct, uni)
    v2 = v2_signals()
    done = collections.Counter()

    def run(r):
        out = crawl(net, r)
        done["n"] += 1
        if done["n"] % 50 == 0:
            print(f"crawled {done['n']}", flush=True)
        return out
    with cf.ThreadPoolExecutor(a.workers) as ex:
        crawls = dict(zip((r["ein"] for r in uni), ex.map(run, uni)))
    rows, sig_rows = [], []
    for r in uni:
        cr = crawls[r["ein"]]
        sigs = [*cr["signals"], *c990.get(r["ein"], ()), *cts.get(r["ein"], ()), *v2.get(r["ein"], ())]
        d = decide(r, sigs)
        rows.append({**r, **d, "fy2024_daf_assets_usd": int(r["fy2024_daf_assets"]), "crawl_status": cr["crawl_status"],
                     "vendor_990_lines": " | ".join(s["detail"] for s in c990.get(r["ein"], ()))[:400], "retrieved": RETRIEVED})
        sig_rows.extend({"ein": r["ein"], "name": r["name"], **s} for s in sigs)
    fields = ("ein", "name", "fy2024_daf_assets_usd", "homepage", "portal_url", "portal_vendor", "evidence_type", "evidence_url", "confidence",
              "retrieved", "vendor_family", "ledger_implied", "evidence_detail", "corroborating_evidence", "conflicting_signals",
              "vendor_990_lines", "crawl_status", "crawl_vendor_family", "homepage_source")
    write_csv(OUT_CSV, rows, fields)
    write_csv(OUT_SIGNALS, sig_rows, ("ein", "name", "family", "product", "ledger_implied", "evidence_type", "evidence_url", "detail", "strength", "first_party", "login_context"))
    e = edges(rows)
    write_csv(OUT_EDGES, e, ("edge_id", "source_entity", "source_type", "target_entity", "target_type", "relationship_type", "status",
                             "evidence_summary", "source_url", "source_date", "accessed_date", "notes"))
    v2_check = [(r["ein"], v2[r["ein"]][0]["family"], r["crawl_vendor_family"]) for r in rows if r["ein"] in v2]
    summary = {
        "universe_cfs": len(rows), "universe_daf_assets_usd": round(sum(r["fy2024_daf_assets"] for r in rows)),
        "homepages_found": sum(1 for r in rows if r["homepage"]),
        "crawl_status": collections.Counter(re.sub(r"_\d+$|:.*", "", r["crawl_status"]) for r in rows).most_common(),
        "confidence": collections.Counter(r["confidence"] for r in rows).most_common(),
        "evidence_type_of_decision": collections.Counter(r["evidence_type"] for r in rows).most_common(),
        "shares_high_medium": shares(rows), "shares_high_only": shares(rows, min_conf=frozenset({"high"})),
        "ct_tenants_2021plus": {f: len(t) for f, t in ct.items()},
        "v2_agreement": {"v2_rows_with_vendor": len(v2_check), "crawl_found": sum(1 for _, _, c in v2_check if c),
                         "crawl_agrees": sum(1 for _, v, c in v2_check if c and c == v),
                         "disagreements": [(e_, v, c) for e_, v, c in v2_check if c and c != v]},
        "edges_written": len(e), "edges_confirmed": sum(1 for x in e if x["status"] == "confirmed"),
    }
    with open(OUT_SUMMARY, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, default=str)
    print(json.dumps({k: summary[k] for k in ("universe_cfs", "homepages_found", "crawl_status", "confidence", "v2_agreement", "edges_written")}, indent=1, default=str))


if __name__ == "__main__":
    main()
