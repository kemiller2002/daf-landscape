#!/usr/bin/env python3
"""Automated accessibility (axe-core) and published service levels, top-20 DAF sponsors (queue item P-NEW-UXS-01).

Universe: the 20 largest DAFRC FY2024 sponsors by end-of-year DAF assets, with the R1 "filed replaces imputed"
corrections applied (same universe function as scripts/mission_void_scan.py).

Per sponsor, at most 5 public pages are loaded in headless Chromium (Playwright):
  1. homepage (seed URL below)
  2. an "open an account / get started" page   - chosen from homepage links by fixed regex priority
  3. a help / FAQ page                           - chosen from homepage links (fallback: contact page)
  4. a contact page (only if distinct from 3)    - service-level text only, no axe
  5. an accessibility statement (if linked)      - service-level text only, no axe
axe-core runs on pages 1-3 with WCAG 2.0/2.1/2.2 A+AA rule tags. No clicks, no form input, no logins,
no cookie-banner dismissal. robots.txt is read (urllib.robotparser) for every host before any page on it is
loaded; status 200 is parsed for '*', 404/410 means no rules, anything else (401/403/429/5xx, network error)
means "robots unreadable, host not fetched" (the rule used in earlier batches). Navigations are paced
>= 2.5 s apart (all work is sequential, so per-host spacing is at least that).

Usage:
  python3 scripts/mission_sponsor_a11y_service.py --cache-dir <scratch> --fetch     # load pages, cache raw JSON
  python3 scripts/mission_sponsor_a11y_service.py --cache-dir <scratch>             # rebuild CSVs from cache
  python3 scripts/mission_sponsor_a11y_service.py --cache-dir <scratch> --rescan-home 232888152   # reload one homepage
Screenshots (homepage only) are written to <cache-dir>/screens/, never into the repo.

Outputs:
  data/mission-2026-11-14/sponsor-a11y-axe-2026.csv          one row per sponsor x page role (home/open_account/help)
  data/mission-2026-11-14/sponsor-service-levels-2026.csv    one row per sponsor
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import urllib.robotparser
from collections import Counter
from typing import Callable, Mapping, Sequence
from urllib.parse import urljoin, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DATA, fmt, read_csv, write_csv  # noqa: E402
from mission_void_scan import CORR_CSV, DAFRC_CSV, corrected_fy2024, top_n  # noqa: E402

RETRIEVED = "2026-11-15"
AXE_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"
AXE_TAGS = ("wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa")
PACE_S = 2.5
UA_TOKEN = "*"   # robots group checked: the generic group (the browser sends its normal headless Chrome UA)
OUT_AXE = os.path.join(DATA, "sponsor-a11y-axe-2026.csv")
OUT_SVC = os.path.join(DATA, "sponsor-service-levels-2026.csv")

# Seed homepage per EIN, and the registrable domain whose subdomains count as "the sponsor's site".
# Corporate-hosted programmes (GS, MS, BofA) have no stand-alone DAF site; the seed is the programme page.
SEEDS: dict[str, tuple[str, str]] = {
    "110303001": ("https://www.fidelitycharitable.org/", "fidelitycharitable.org"),
    "237825575": ("https://www.nptrust.org/", "nptrust.org"),
    "311640316": ("https://www.dafgiving360.org/", "dafgiving360.org"),
    "232888152": ("https://www.vanguardcharitable.org/", "vanguardcharitable.org"),
    "311774905": ("https://pwm.gs.com/nam/en-us/what-we-do/philanthropic-strategy", "gs.com"),
    "205205488": ("https://www.svcf.org/", "svcf.org"),
    "341747398": ("https://www.aefonline.org/", "aefonline.org"),
    "527082731": ("https://www.morganstanley.com/what-we-do/wealth-management/gift", "morganstanley.com"),
    "352129262": ("https://renaissancecharitable.org/", "renaissancecharitable.org"),
    "581493949": ("https://www.ncfgiving.com/", "ncfgiving.com"),
    "046010342": ("https://www.bankofamerica.com/philanthropic/donoradvised.go", "bankofamerica.com"),
    "362167000": ("https://www.cct.org/", "cct.org"),
    "262048480": ("https://impactassets.org/", "impactassets.org"),
    "566047886": ("https://www.fftc.org/", "fftc.org"),
    "237174183": ("https://jcfny.org/", "jcfny.org"),
    "431152398": ("https://www.growyourgiving.org/", "growyourgiving.org"),
    "200849590": ("https://www.greaterhorizons.org/", "greaterhorizons.org"),
    "260724604": ("https://dechomai.org/", "dechomai.org"),
    "042103559": ("https://www.cjp.org/", "cjp.org"),
    "593652538": ("https://www.raymondjamescharitable.org/", "raymondjamescharitable.org"),
}

# Link-selection rules: ordered (label, regex on link text/aria-label, regex on href). First rule with a hit wins.
OPEN_RULES = (
    ("open account/fund (text)", r"\bopen\s+(an?\s+|your\s+)?(\w+\s+)?(new\s+)?(donor[- ]advised\s+fund|daf|account|fund|giving\s+account|charitable\s+account)", None),
    ("start/establish fund (text)", r"\b(start|establish|create)\s+(an?\s+|your\s+|the\s+)?(donor[- ]advised\s+fund|daf|fund|account|giving\s+account)", None),
    ("get started (text)", r"\bget\s+started\b", None),
    ("open/start (href)", None, r"(open|start|establish)[-_]?(an?[-_])?(account|fund|daf)|get[-_]?started"),
)
HELP_RULES = (
    ("faq (text)", r"\bfaqs?\b|frequently\s+asked", None),
    ("help centre (text)", r"\bhelp\s*cent(er|re)\b|\bsupport\s+cent(er|re)\b|knowledge\s+base|^\s*(help|support|donor\s+support|customer\s+(service|support))\s*$", None),
    ("faq/help (href)", None, r"/(faqs?|help|support|knowledge)(/|\.|-|$|\?)"),
)
CONTACT_RULES = (
    ("contact (text)", r"\bcontact(\s+us)?\b", None),
    ("contact (href)", None, r"/contact"),
)
A11Y_RULES = (
    ("accessibility (text)", r"\baccessib", None),
    ("accessibility (href)", None, r"accessib"),
)
LOGIN_HREF = re.compile(r"log[-_]?in|sign[-_]?in|logon|/auth|/sso|oauth|password", re.I)
SKIP_HREF = re.compile(r"^(mailto|tel|javascript):|\.(pdf|docx?|xlsx?|zip|jpe?g|png)(\?|$)", re.I)


# ----------------------------------------------------------------------------- pure helpers
def host_of(url: str) -> str:
    return urlparse(url).netloc.lower()


HELP_PLATFORMS = ("freshdesk.com", "zendesk.com", "helpscoutdocs.com", "intercom.help", "helpdocs.io")


def on_site(url: str, base: str) -> bool:
    """Sponsor's own domain, or a hosted help-centre tenant named after it (e.g. impactassets.freshdesk.com). Pure."""
    h = host_of(url)
    tenant = base.split(".")[0]
    return h == base or h.endswith("." + base) or (h.split(".")[0] == tenant and h.endswith(HELP_PLATFORMS))


def norm_url(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc.lower()}{p.path.rstrip('/') or '/'}"


NOT_DONOR_HELP = re.compile(r"how\s+(we|you\s+can)\s+help|get\s+help|for\s+nonprofits|mental\s+health|support\s+us|ways\s+to", re.I)


def pick_link(links: Sequence[Mapping], rules: Sequence[tuple], base: str, exclude: frozenset = frozenset()) -> dict:
    """Return the first link matching the highest-priority rule (document order within a rule). Pure.
    Links whose text reads as community-services or fundraising help ("get help", "how we help") are never picked."""
    usable = tuple(l for l in links if l.get("href", "").startswith("http") and not SKIP_HREF.search(l["href"])
                   and not NOT_DONOR_HELP.search(f"{l.get('text', '')} {l.get('aria', '')}")
                   and on_site(l["href"], base) and not LOGIN_HREF.search(l["href"])
                   and norm_url(l["href"]) not in exclude)
    for label, text_rx, href_rx in rules:
        hits = tuple(l for l in usable
                     if (text_rx and re.search(text_rx, f"{l.get('text', '')} {l.get('aria', '')}", re.I))
                     or (href_rx and re.search(href_rx, urlparse(l["href"]).path + "?" + urlparse(l["href"]).query, re.I)))
        if hits:
            return {**hits[0], "rule": label}
    return {}


PHONE_RX = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?([2-9]\d\d)\)?[\s.-]?(\d{3})[\s.-]?(\d{4})(?!\d)")
DAY = r"(?:mon(?:day)?|tue(?:s(?:day)?)?|wed(?:nesday)?|thu(?:rs(?:day)?)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?|weekdays?)\.?"
TIME = r"\d{1,2}(?::\d\d)?\s*(?:a\.?m\.?|p\.?m\.?|am|pm)"
TZ = r"(?:\s*\(?\s*(?:ET|EST|EDT|Eastern(?:\s+Time)?|CT|CST|CDT|Central(?:\s+Time)?|MT|Mountain(?:\s+Time)?|PT|PST|PDT|Pacific(?:\s+Time)?)\b\.?\)?)?"
HOURS_RX = (
    re.compile(rf"{DAY}(?:\s*(?:-|–|—|to|through|thru)\s*{DAY})?\s*[,:|]?\s*(?:from\s+)?{TIME}\s*(?:-|–|—|to|until)\s*{TIME}{TZ}", re.I),
    re.compile(rf"{TIME}\s*(?:-|–|—|to|until)\s*{TIME}{TZ}[,]?\s*(?:on\s+)?{DAY}(?:\s*(?:-|–|—|to|through|thru)\s*{DAY})?", re.I),
    re.compile(r"(?:phone|call|support|service|representative|agent)[^.]{0,60}(?:\b24\s*/\s*7\b|\b24\s+hours\s+a\s+day\b)"
               r"|(?:\b24\s*/\s*7\b|\b24\s+hours\s+a\s+day\b)[^.]{0,40}(?:phone|call|support|service)", re.I),
)
WITHIN_RX = re.compile(r"within\s+(?:\d+|one|two|three|four|five|a\s+few|24|48|72)(?:\s*(?:-|–|to)\s*\d+)?\s+(?:business\s+|working\s+)?(?:minutes?|hours?|days?|weeks?)", re.I)
SUPPORT_CTX = re.compile(r"respon|reply|repl(y|ies)|get\s+back|return\s+(your\s+)?(call|email)|inquir|enquir|question|contact|message|reach", re.I)
SOFT_RX = re.compile(r"\b(?:we'?ll|we\s+will|will|someone\s+will)\s+(?:be\s+in\s+touch|respond|reply|get\s+back\s+to\s+you|contact\s+you|reach\s+out)[^.\n]{0,40}", re.I)
CHAT_TEXT_RX = re.compile(r"\blive\s+chat\b|\bchat\s+(with|now|online|is\s+available)\b|\bstart\s+(a\s+)?chat\b|\bvirtual\s+assistant\b|\bchat\s+bot\b|\bchatbot\b", re.I)
WCAG_RX = re.compile(r"(?:WCAG|Web\s+Content\s+Accessibility\s+Guidelines)\s*\)?\s*(?:\(WCAG\)\s*)?(?:version\s*)?(2\.[0-2]|2\b)?\s*,?\s*(?:Level\s*|conformance\s+level\s*)?\(?\b(AAA|AA|A)\b", re.I)
WCAG_VER_RX = re.compile(r"(?:WCAG|Web\s+Content\s+Accessibility\s+Guidelines)[^.]{0,40}?(2\.[0-2])", re.I)
WCAG_LVL_RX = re.compile(r"(?:WCAG|Web\s+Content\s+Accessibility\s+Guidelines)[^.]{0,80}?\b(?:Level\s+)?(AAA|AA|A)\b(?![a-z])", re.I)


def snippets(text: str, rx: re.Pattern, width: int = 0, limit: int = 3) -> tuple[str, ...]:
    out = []
    for m in rx.finditer(text or ""):
        s = text[max(0, m.start() - width): m.end() + width]
        s = re.sub(r"\s+", " ", s).strip()
        if s not in out:
            out.append(s)
        if len(out) >= limit:
            break
    return tuple(out)


def phones(text: str) -> tuple[str, ...]:
    seen = []
    for m in PHONE_RX.finditer(text or ""):
        p = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        if p not in seen:
            seen.append(p)
    return tuple(seen)


def response_promises(text: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Split 'within N units' statements into support-response promises vs other (e.g. grant processing). Pure."""
    sup, other = [], []
    for m in WITHIN_RX.finditer(text or ""):
        ctx = re.sub(r"\s+", " ", text[max(0, m.start() - 120): m.end() + 40]).strip()
        (sup if SUPPORT_CTX.search(text[max(0, m.start() - 120): m.start()]) else other).append(ctx)
    dedup = lambda xs: tuple(dict.fromkeys(xs))[:3]
    return dedup(sup), dedup(other)


def question_lines(text: str) -> int:
    """Distinct lines of visible text that read as questions (8-250 chars, ending '?'). Pure."""
    return len({l.strip() for l in (text or "").splitlines() if 8 < len(l.strip()) < 250 and l.strip().endswith("?")})


def axe_summary(axe: Mapping | None) -> dict:
    if not axe:
        return {}
    viol = axe.get("violations", [])
    by_rules = Counter(v.get("impact") or "unknown" for v in viol)
    by_nodes = Counter()
    for v in viol:
        by_nodes[v.get("impact") or "unknown"] += len(v.get("nodes", []))
    top = sorted(viol, key=lambda v: (-len(v.get("nodes", [])), v["id"]))[:5]
    out = {"rules_violated": len(viol), "nodes_total": sum(by_nodes.values()),
           "top_rule_ids": "; ".join(f"{v['id']}({v.get('impact')}):{len(v.get('nodes', []))}" for v in top),
           "incomplete_rules": axe.get("incomplete_n", ""), "passes_rules": axe.get("passes_n", ""),
           "axe_version": axe.get("testEngine", {}).get("version", "")}
    for imp in ("critical", "serious", "moderate", "minor"):
        out[f"{imp}_rules"] = by_rules.get(imp, 0)
        out[f"{imp}_nodes"] = by_nodes.get(imp, 0)
    return out


# ----------------------------------------------------------------------------- IO: robots + browser
def fetch_text(url: str, timeout: int = 30) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research; robots-respecting)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return -1, f"{type(e).__name__}: {e}"


def robots_checker(cache: dict) -> Callable[[str], tuple[bool, str]]:
    """Return can_fetch(url) -> (allowed, note). Reads each host's robots.txt once (memoised in `cache`)."""
    def load(host: str) -> dict:
        if host not in cache:
            status, body = fetch_text(f"https://{host}/robots.txt")
            time.sleep(PACE_S)
            cache[host] = {"status": status, "body": body if status == 200 else "", "error": body if status == -1 else ""}
        return cache[host]

    def can(url: str) -> tuple[bool, str]:
        host = host_of(url)
        r = load(host)
        st = r["status"]
        if st in (404, 410):
            return True, f"robots.txt {st}: no rules (allow)"
        if st != 200:
            return False, f"robots.txt unreadable ({st}): host not fetched"
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(r["body"].splitlines())
        ok = rp.can_fetch(UA_TOKEN, url)
        return ok, f"robots.txt 200: {'allowed' if ok else 'disallowed'} for '*'"
    return can


PAGE_JS = r"""() => {
  const links = [...document.querySelectorAll('a[href]')].map(a => ({
      href: a.href, text: (a.innerText || a.textContent || '').trim().replace(/\s+/g,' ').slice(0,120),
      aria: (a.getAttribute('aria-label') || a.getAttribute('title') || '').slice(0,120)}));
  const srcs = [...document.querySelectorAll('script[src],iframe[src]')].map(e => e.src);
  const ids = [...document.querySelectorAll('[id],[class]')].slice(0,6000)
      .map(e => (e.id || '') + ' ' + (typeof e.className === 'string' ? e.className : '')).join(' ');
  const g = ['Intercom','zE','zEACLoaded','drift','LiveChatWidget','LC_API','lpTag','embedded_svc','HubSpotConversations',
             'Genesys','_genesys','adaEmbed','Five9SocialWidget','olark','$crisp','fcWidget','Tawk_API','tidioChatApi',
             'Kustomer','gladly','Gladly','SprChat','qualified','Glia','sn_csm_ec','inqSiteID','Inq','salesforceChat']
      .filter(k => { try { return typeof window[k] !== 'undefined'; } catch(e) { return false; } });
  const qs = [...document.querySelectorAll('h2,h3,h4,h5,h6,summary,dt,button,[role=button],[aria-expanded]')]
      .map(e => (e.innerText || '').trim().replace(/\s+/g,' ')).filter(t => t.length > 8 && t.length < 250 && t.endsWith('?'));
  return {links, srcs, ids: ids.slice(0, 200000), globals: g, title: document.title,
          text: (document.body ? document.body.innerText : '').slice(0, 400000),
          has_password: !!document.querySelector('input[type=password]'),
          details_n: document.querySelectorAll('details > summary').length,
          question_items: [...new Set(qs)].length,
          article_links: [...new Set([...document.querySelectorAll('a[href*="/articles/"],a[href*="/article/"],a[href*="/kb/"]')].map(a => a.href))].length};
}"""

AXE_JS = """async (tags) => {
  const r = await axe.run(document, {runOnly: {type: 'tag', values: tags}, resultTypes: ['violations']});
  return {testEngine: r.testEngine, url: r.url,
          violations: r.violations.map(v => ({id: v.id, impact: v.impact, tags: v.tags, help: v.help,
                                              nodes: v.nodes.map(n => ({target: n.target}))})),
          incomplete_n: r.incomplete.length, passes_n: r.passes.length};
}"""


def _load_page(ctx, url: str, axe_src: str | None, can_fetch, shot: str | None = None) -> dict:
    allowed, rnote = can_fetch(url)
    rec = {"url_requested": url, "robots": rnote, "robots_allowed": allowed}
    if not allowed:
        return {**rec, "status": "skipped: robots"}
    page = ctx.new_page()
    try:
        resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
        try:
            page.wait_for_load_state("networkidle", timeout=12000)
        except Exception:  # noqa: BLE001
            pass
        page.wait_for_timeout(2500)
        info = page.evaluate(PAGE_JS)
        rec = {**rec, "http_status": resp.status if resp else "", "url_final": page.url, **info}
        if resp and resp.status >= 400:
            return {**rec, "status": f"http {resp.status}"}
        if shot:
            page.screenshot(path=shot, full_page=False)
        if axe_src is not None:
            if info["has_password"] and (LOGIN_HREF.search(page.url) or re.search(r"log\s*in|sign\s*in|log\s*on", info["title"] or "", re.I)):
                return {**rec, "status": "login/credential page: axe not run"}
            page.evaluate(axe_src)
            rec = {**rec, "axe": page.evaluate(AXE_JS, list(AXE_TAGS))}
        return {**rec, "status": "ok"}
    except Exception as e:  # noqa: BLE001
        return {**rec, "status": f"error: {type(e).__name__}: {str(e)[:200]}"}
    finally:
        page.close()
        time.sleep(PACE_S)


def scan_sponsor(ctx, sponsor: Mapping, axe_src: str, can_fetch, screens: str, prior: Mapping | None = None) -> dict:
    """Select and load pages. `prior` (an earlier raw record) lets pages already loaded be reused instead of
    re-fetched, as long as the reuse does not need an axe result the earlier load lacks."""
    seed, base = SEEDS[sponsor["ein"]]
    cached = {norm_url(p["url_requested"]): p for p in (prior or {}).get("pages", {}).values()}
    navs = [0]

    def load_page(ctx_, url, axe, can, shot=None):  # noqa: ANN001 - shadows the IO loader with a cache in front
        old = cached.get(norm_url(url))
        if old and (axe is None or old.get("axe") or old.get("status") != "ok"):
            return {k: v for k, v in old.items() if k not in ("selection", "link_text")} | {"reused_from_earlier_load": True}
        navs[0] += 1 if can(url)[0] else 0
        return _load_page(ctx_, url, axe, can, shot)

    home = load_page(ctx, seed, axe_src, can_fetch, os.path.join(screens, f"{sponsor['ein']}-home.png"))
    links = home.get("links", [])
    seen = frozenset({norm_url(seed), norm_url(home.get("url_final", seed))})
    open_l = pick_link(links, OPEN_RULES, base, seen)
    help_l = pick_link(links, HELP_RULES, base, seen | ({norm_url(open_l["href"])} if open_l else set()))
    contact_l = pick_link(links, CONTACT_RULES, base, seen)
    help_sel = help_l or ({**contact_l, "rule": "fallback: " + contact_l["rule"]} if contact_l else {})
    pages = {"home": {**home, "selection": "seed homepage"}}
    if open_l:
        pages["open_account"] = {**load_page(ctx, open_l["href"], axe_src, can_fetch), "selection": open_l["rule"], "link_text": open_l.get("text") or open_l.get("aria")}
    if help_sel:
        pages["help"] = {**load_page(ctx, help_sel["href"], axe_src, can_fetch), "selection": help_sel["rule"], "link_text": help_sel.get("text") or help_sel.get("aria")}
    if contact_l and help_l and norm_url(contact_l["href"]) != norm_url(help_l["href"]):
        pages["contact"] = {**load_page(ctx, contact_l["href"], None, can_fetch), "selection": contact_l["rule"], "link_text": contact_l.get("text")}
    all_links = tuple(l for p in pages.values() for l in p.get("links", []))
    a11y_l = pick_link(all_links, A11Y_RULES, base, frozenset(norm_url(p.get("url_final") or p["url_requested"]) for p in pages.values()))
    if a11y_l:
        pages["a11y_statement"] = {**load_page(ctx, a11y_l["href"], None, can_fetch), "selection": a11y_l["rule"], "link_text": a11y_l.get("text") or a11y_l.get("aria")}
    trimmed = pages
    return {"ein": sponsor["ein"], "seed": seed, "base": base,
            "navigations": (prior or {}).get("navigations", 0) + navs[0],
            "candidates": {"open": open_l, "help": help_l, "contact": contact_l, "a11y": a11y_l},
            "a11y_link_on_scanned_pages": bool(a11y_l), "pages": trimmed}


def rescan_home(sponsors: Sequence[Mapping], cache_dir: str, eins: Sequence[str]) -> None:
    """Reload only the homepage of the given sponsors (e.g. after a scan-rule fix) and merge it into the raw cache."""
    from playwright.sync_api import sync_playwright
    robots_cache_path = os.path.join(cache_dir, "robots.json")
    robots_cache = json.load(open(robots_cache_path)) if os.path.exists(robots_cache_path) else {}
    can_fetch = robots_checker(robots_cache)
    st, axe_src = fetch_text(AXE_URL)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for s in (x for x in sponsors if x["ein"] in eins):
            path = os.path.join(cache_dir, "raw", f"{s['ein']}.json")
            raw = json.load(open(path))
            ctx = browser.new_context(viewport={"width": 1366, "height": 900}, bypass_csp=True, locale="en-US")
            home = _load_page(ctx, raw["seed"], axe_src, can_fetch)
            ctx.close()
            raw["pages"]["home"] = {**home, "selection": "seed homepage", "rescanned": True}
            raw["navigations"] = raw.get("navigations", 0) + 1
            json.dump(raw, open(path, "w"))
            print(s["rank"], s["name"], "home rescanned:", home.get("status"), flush=True)
        browser.close()
    json.dump(robots_cache, open(robots_cache_path, "w"))


def run_fetch(sponsors: Sequence[Mapping], cache_dir: str, reselect: bool = False) -> None:
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(cache_dir, "raw"), exist_ok=True)
    screens = os.path.join(cache_dir, "screens")
    os.makedirs(screens, exist_ok=True)
    robots_cache_path = os.path.join(cache_dir, "robots.json")
    robots_cache = json.load(open(robots_cache_path)) if os.path.exists(robots_cache_path) else {}
    can_fetch = robots_checker(robots_cache)
    ok, note = can_fetch(AXE_URL)
    st, axe_src = fetch_text(AXE_URL)
    if not ok or st != 200:
        raise SystemExit(f"axe-core not loadable: {note} / {st}")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for s in sponsors:
            out = os.path.join(cache_dir, "raw", f"{s['ein']}.json")
            prior = json.load(open(out)) if os.path.exists(out) else None
            if prior and not (reselect and prior["pages"]["home"].get("status") == "ok"):
                continue
            ctx = browser.new_context(viewport={"width": 1366, "height": 900}, bypass_csp=True, locale="en-US")
            res = scan_sponsor(ctx, s, axe_src, can_fetch, screens, prior)
            ctx.close()
            json.dump(res, open(out, "w"))
            json.dump(robots_cache, open(robots_cache_path, "w"))
            print(s["rank"], s["name"], {k: v.get("status") for k, v in res["pages"].items()}, flush=True)
        browser.close()


# ----------------------------------------------------------------------------- CSV builders (pure)
AXE_FIELDS = ("fy2024_rank", "sponsor", "ein", "fy2024_daf_assets_corrected", "page_role", "selection_rule", "link_text",
              "url_requested", "url_final", "http_status", "robots", "scan_status", "page_title", "axe_version",
              "axe_rule_tags", "rules_violated", "critical_rules", "serious_rules", "moderate_rules", "minor_rules",
              "nodes_total", "critical_nodes", "serious_nodes", "moderate_nodes", "minor_nodes", "top_rule_ids",
              "incomplete_rules", "retrieved")


def axe_rows(s: Mapping, raw: Mapping) -> tuple[dict, ...]:
    base = {"fy2024_rank": s["rank"], "sponsor": s["name"], "ein": s["ein"],
            "fy2024_daf_assets_corrected": fmt(s["assets_corr"]), "retrieved": RETRIEVED,
            "axe_rule_tags": " ".join(AXE_TAGS)}
    def row(role: str) -> dict:
        p = raw["pages"].get(role)
        if not p:
            return {**base, "page_role": role, "scan_status": "no matching public link found on homepage"}
        return {**base, "page_role": role, "selection_rule": p.get("selection", ""), "link_text": p.get("link_text", ""),
                "url_requested": p["url_requested"], "url_final": p.get("url_final", ""), "http_status": p.get("http_status", ""),
                "robots": p.get("robots", ""), "scan_status": p.get("status", ""), "page_title": (p.get("title") or "")[:120],
                **axe_summary(p.get("axe"))}
    return tuple(row(r) for r in ("home", "open_account", "help"))


SVC_FIELDS = ("fy2024_rank", "sponsor", "ein", "fy2024_daf_assets_corrected", "seed_url", "pages_loaded", "page_loads_total", "page_urls",
              "phone_numbers_found", "phone_hours_stated", "phone_hours_text", "phone_hours_source_role",
              "support_response_promise", "support_response_text", "support_response_unquantified", "other_within_statements",
              "live_chat_signal", "live_chat_evidence", "help_page_url", "help_article_links", "help_faq_question_items",
              "help_question_lines", "help_count_method", "a11y_overlay_detected", "a11y_statement_present", "a11y_statement_url", "a11y_statement_status",
              "wcag_version_claimed", "wcag_level_claimed", "a11y_wcag_text", "notes", "retrieved")

CHAT_SRC_RX = re.compile(r"intercom|zdassets|zendesk|zopim|drift\.com|livechatinc|liveperson|lpsnmedia|salesforceliveagent|"
                         r"embeddedservice|my\.salesforce-scrt|messaging\.salesforce|usemessages|hs-scripts|genesys|"
                         r"purecloud|mypurecloud|ada\.support|five9|olark|crisp\.chat|freshchat|tawk\.to|tidio|kustomer|"
                         r"gladly|sprinklr|qualified\.com|glia|nuance|inq\.com|touchcommerce|servicenow", re.I)


OVERLAY_RX = re.compile(r"accessibe|acsbapp|userway|audioeye|equalweb|maxaccess|reciteme|accessibilityadvocate|essentialaccessibility|"
                        r"levelaccess|ally\.js|purpose-?built\s*access", re.I)

# Reviewer notes, added after reading the cached page text (not inferred by the regexes).
REVIEW_NOTES: dict[str, str] = {
    "341747398": "accessibility statement page body is placeholder text ('See our Accessibility Tips for what to do for this page on your website.'); no WCAG claim",
    "205205488": "homepage footer 'ACCESSIBILITY' is a javascript: control (widget), not a statement page",
    "566047886": "homepage links to accessiBe's screen-reader guide (overlay widget), no statement page found",
    "232888152": "homepage contains a login form; homepage axe run in a second load after the login-page rule was narrowed",
}


def overlay_signal(pages: Mapping) -> str:
    hits = sorted({host_of(u) for p in pages.values() for u in p.get("srcs", []) if OVERLAY_RX.search(u)}
                  | {host_of(l["href"]) for p in pages.values() for l in p.get("links", []) if OVERLAY_RX.search(l.get("href", ""))})
    return "; ".join(hits)


def chat_signal(pages: Mapping) -> tuple[str, str]:
    ev = []
    for role, p in pages.items():
        ev += [f"{role}:global:{g}" for g in p.get("globals", [])]
        ev += [f"{role}:src:{host_of(u)}" for u in p.get("srcs", []) if CHAT_SRC_RX.search(u)]
        ev += [f"{role}:text:{t}" for t in snippets(p.get("text", ""), CHAT_TEXT_RX, 40, 2)]
    ev = list(dict.fromkeys(ev))
    tech = [e for e in ev if ":global:" in e or ":src:" in e]
    txt = [e for e in ev if ":text:" in e]
    sig = ("chat widget script/global detected" if tech else "") + ("; " if tech and txt else "") + ("chat mentioned in page text" if txt else "")
    return (sig or "none detected on scanned public pages"), " | ".join(ev[:6])


def svc_row(s: Mapping, raw: Mapping) -> dict:
    pages = {k: v for k, v in raw["pages"].items() if v.get("status") == "ok"}
    order = ("contact", "help", "home", "open_account", "a11y_statement")
    found = tuple((r, x) for r in order if r in pages for rx in HOURS_RX for x in snippets(pages[r].get("text", ""), rx, 30, 2))
    hours = found[0] if found else None
    allhours = tuple(dict.fromkeys(x for _, x in found))
    sup = tuple(x for r in order if r in pages for x in response_promises(pages[r].get("text", ""))[0])
    oth = tuple(x for r in order if r in pages for x in response_promises(pages[r].get("text", ""))[1])
    soft = tuple(dict.fromkeys(f"{r}: {x}" for r in order if r in pages for x in snippets(pages[r].get("text", ""), SOFT_RX, 0, 2)))
    ph = tuple(dict.fromkeys(x for r in order if r in pages for x in phones(pages[r].get("text", ""))))
    chat, chat_ev = chat_signal(pages)
    hp = raw["pages"].get("help", {})
    a = raw["pages"].get("a11y_statement")
    a_text = (a or {}).get("text", "")
    wcag_snips = snippets(a_text, WCAG_RX, 60, 2)
    ver = sorted(set(WCAG_VER_RX.findall(a_text)))
    lvl = sorted(set(m.upper() for m in WCAG_LVL_RX.findall(a_text)))
    if not pages:
        na = "not assessed (no page loaded)"
        return {"fy2024_rank": s["rank"], "sponsor": s["name"], "ein": s["ein"], "fy2024_daf_assets_corrected": fmt(s["assets_corr"]),
                "seed_url": raw["seed"], "pages_loaded": 0, "page_loads_total": raw.get("navigations", 0), "page_urls": "",
                **{k: na for k in ("phone_hours_stated", "support_response_promise", "live_chat_signal", "a11y_statement_present")},
                "notes": "; ".join(f"{k}:{v.get('status')} ({v.get('robots')})" for k, v in raw["pages"].items()), "retrieved": RETRIEVED}
    notes = [REVIEW_NOTES[s["ein"]]] if s["ein"] in REVIEW_NOTES else []
    blocked = [f"{k}:{v.get('status')}" for k, v in raw["pages"].items() if v.get("status") != "ok"]
    if blocked:
        notes.append("not ok: " + ", ".join(blocked))
    if hp.get("selection", "").startswith("fallback"):
        notes.append("no FAQ/help link on homepage; contact page used as help page")
    return {"fy2024_rank": s["rank"], "sponsor": s["name"], "ein": s["ein"], "fy2024_daf_assets_corrected": fmt(s["assets_corr"]),
            "seed_url": raw["seed"], "page_loads_total": raw.get("navigations", 0), "pages_loaded": sum(1 for v in raw["pages"].values() if v.get("status") == "ok"),
            "page_urls": " ; ".join(f"{k}={v.get('url_final') or v['url_requested']}" for k, v in raw["pages"].items()),
            "phone_numbers_found": " ; ".join(ph[:4]),
            "phone_hours_stated": "Y" if hours else "N (none found on scanned pages)",
            "phone_hours_text": " | ".join(allhours[:2]), "phone_hours_source_role": hours[0] if hours else "",
            "support_response_promise": "Y (time stated)" if sup else ("unquantified only" if soft else "N (none found on scanned pages)"),
            "support_response_text": " | ".join(sup[:2]), "support_response_unquantified": " | ".join(soft[:3]), "other_within_statements": " | ".join(oth[:2]),
            "live_chat_signal": chat, "live_chat_evidence": chat_ev,
            "help_page_url": hp.get("url_final", ""), "help_article_links": hp.get("article_links", ""),
            "help_faq_question_items": hp.get("question_items", ""),
            "help_question_lines": question_lines(hp.get("text", "")) if hp.get("status") == "ok" else "",
            "help_count_method": "article_links = distinct links to /articles|/article|/kb; faq_question_items = distinct headings/buttons/summary/dt ending '?'; question_lines = distinct visible text lines ending '?' (all on the help page as first rendered, accordions closed)" if hp.get("status") == "ok" else "",
            "a11y_overlay_detected": overlay_signal(pages),
            "a11y_statement_present": ("Y" if a and a.get("status") == "ok" else "linked but not loaded") if a else "N (no accessibility link on scanned pages)",
            "a11y_statement_url": (a or {}).get("url_final") or (a or {}).get("url_requested", ""),
            "a11y_statement_status": (a or {}).get("status", ""),
            "wcag_version_claimed": "/".join(ver), "wcag_level_claimed": "/".join(lvl),
            "a11y_wcag_text": " | ".join(wcag_snips), "notes": "; ".join(notes), "retrieved": RETRIEVED}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--reselect", action="store_true",
                    help="with --fetch: re-run link selection for cached sponsors, reusing pages already loaded")
    ap.add_argument("--rescan-home", default="", help="comma-separated EINs whose homepage only is reloaded")
    a = ap.parse_args()
    sponsors = top_n(corrected_fy2024(read_csv(DAFRC_CSV), read_csv(CORR_CSV)), a.n)
    missing = [s["ein"] for s in sponsors if s["ein"] not in SEEDS]
    if missing:
        raise SystemExit(f"no seed URL for EINs {missing}")
    if a.fetch:
        run_fetch(sponsors, a.cache_dir, a.reselect)
    if a.rescan_home:
        rescan_home(sponsors, a.cache_dir, tuple(a.rescan_home.split(",")))
    raws = {s["ein"]: json.load(open(os.path.join(a.cache_dir, "raw", f"{s['ein']}.json"))) for s in sponsors
            if os.path.exists(os.path.join(a.cache_dir, "raw", f"{s['ein']}.json"))}
    have = tuple(s for s in sponsors if s["ein"] in raws)
    write_csv(OUT_AXE, tuple(r for s in have for r in axe_rows(s, raws[s["ein"]])), AXE_FIELDS)
    write_csv(OUT_SVC, tuple(svc_row(s, raws[s["ein"]]) for s in have), SVC_FIELDS)
    print(f"wrote {OUT_AXE} and {OUT_SVC} for {len(have)} of {len(sponsors)} sponsors")


if __name__ == "__main__":
    main()
