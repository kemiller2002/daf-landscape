#!/usr/bin/env python3
"""Do the charities that receive the most DAF grant dollars show DAF giving options on their donate pages?
(queue item P-NEW-NPA-01).

Sample
  The ~300 recipient EINs with the most Schedule I dollars from the top-50 DAF sponsors' FY2023-FY2024 returns,
  exactly the lines behind data/mission-2026-11-14/daf-grant-recipient-sectors-top50.csv
  (scripts/mission_recipient_sectors.py; scope all_ex_university_hospital = non-university grantors).
  Excluded as "DAF sponsors themselves": DAF-to-DAF lines (whitelist decision `include`, self-lines) and every
  recipient EIN that is a DAFRC panel member in the national, community-foundation, single-issue or processor
  segment, plus BMF NTEE T31 (community foundations) outside the panel. University/hospital panel EINs (which also hold DAFs) are kept as charities and flagged.
  Recipients without an EIN or not in the IRS EO BMF (e.g. LLCs) are excluded and counted.

Website
  The recipient's own latest e-filed 990/990-EZ (IRS TEOS index_2023..2026 -> OBJECT_ID), field WebsiteAddressTxt,
  read from the GivingTuesday mirror of IRS TEOS (first 256 KB by HTTP Range). Where the 990 gives no usable URL,
  a manually searched official site is used (MANUAL_SITES, each with its search note).

Scan (stage `scan`; polite)
  For each site: robots.txt is fetched first (urllib, generic UA). 200 -> parsed with urllib.robotparser for
  user-agent `*`; 404/410 -> no rules; anything else (401/403/5xx/timeout) -> robots unreadable, NOT fetched.
  At most two pages per charity are loaded: the homepage, then one donate/give page found from the homepage's
  links. Pages are rendered with headless Chrome via Playwright (node helper embedded below) so that JS-injected
  widgets are seen; images/media/fonts are not loaded; nothing is clicked or submitted. >= 1.1 s between page
  navigations to the same host. If a page redirects to another host, that host's robots.txt is checked and the
  content discarded if disallowed.

Detect (stage `report`; pure)
  DAFpay/Chariot, DAF Direct, sponsor links (Fidelity Charitable, DAFgiving360/Schwab Charitable, Vanguard
  Charitable, NPT), "donor-advised"/"DAF" text, the charity's own EIN shown, DAF-adjacent processors (Every.org,
  PayPal Giving Fund, Daffy, Endaoment, Benevity) and the donation platform, in the raw HTML, rendered DOM,
  child frames and request URLs.

Stdlib only (plus node + Playwright for rendering); functional style.

Usage
  python3 scripts/mission_donate_page_scan.py rank     --np-cache NP --bmf-dir BMF --lines-cache LC --work W [--n 300]
  python3 scripts/mission_donate_page_scan.py websites --index-dir IDX --work W
  python3 scripts/mission_donate_page_scan.py scan     --work W
  python3 scripts/mission_donate_page_scan.py report   --work W
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import (BMF_FILES, LINES_V, WHITELIST, annotate, classify,  # noqa: E402
                                       load_lines)

OUT_CSV = os.path.join(DATA, "nonprofit-donate-page-daf-scan-2026.csv")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
SPONSOR_SEGMENTS = frozenset({"national", "community_foundation", "single_issue", "processor"})
HOST_GAP = 1.1
ACCESSED = "2026-11-15"

# Official sites found by manual public web search where the 990 gave no usable WebsiteAddressTxt.
# ein -> (url, note). Filled only from search results naming the organisation's own domain.
# Searched with no official site found: 85 Fund, Follow Your Dream Fdn, Grantham Env. Trust (granthamtrust.org unconfirmed),
# California Academy of Studio Arts, Mission Mutual, Voter Registration Project, Huntington Fdn, Permanent Archive Fund,
# Archive Sustaining Fdn, Open Library of Richmond, Kollel International, MY Keren Hashluchim, Amidei Zion of Bobov,
# Congregation Ohr Torah; not searched (private family vehicles): James Family Charitable Trust, Deitch Family Charitable
# Support Trust, Sandberg Goldberg Bernthal Family Foundation.
MANUAL_SITES: dict[str, tuple[str, str]] = {
    "870234341": ("https://www.churchofjesuschrist.org/", "search results on newsroom.churchofjesuschrist.org (own domain)"),
    "455600818": ("https://www.lucasmuseum.org/", "search: lucasmuseum.org pages"),
    "883013171": ("https://www.comeandseefoundation.org/", "search: comeandseefoundation.org/donate, /about"),
    "474422640": ("https://xqsuperschool.org/", "search: xqsuperschool.org (Wikipedia infobox, own pages)"),
    "041564655": ("https://www.massgeneralbrigham.org/", "search: massgeneralbrigham.org/giving"),
    "042312909": ("https://www.massgeneralbrigham.org/", "search: massgeneralbrigham.org/giving (second MGB EIN)"),
    "264562328": ("https://schmidtocean.org/", "search: schmidtocean.org home page"),
    "956006173": ("https://www.cru.org/", "search: cru.org fact sheet; giving at give.ccci.org"),
    "386006309": ("https://umich.edu/", "search: giving.umich.edu (umich.edu domain)"),
    "237093281": ("https://everyhome.org/", "search: everyhome.org (Every Home for Christ, formerly World Literature Crusade)"),
    "832504447": ("https://gsd.ngo/", "search summary names gsd.ngo as official site (aggregator-derived)"),
    "813130448": ("https://www.chicagocred.org/", "search: chicagocred.org own pages"),
    "650246247": ("https://onehope.net/", "search: onehope.net annual report 2025"),
    "411917516": ("https://www.mayoclinic.org/", "search: mayoclinic.org/giving-to-mayo-clinic"),
    "951831097": ("https://www.wycliffe.org/", "search: wycliffe.org/give"),
    "580660607": ("https://www.salvationarmyusa.org/", "search: salvationarmyusa.org contact page; give.salvationarmyusa.org"),
    "135562351": ("https://www.salvationarmyusa.org/", "search: salvationarmyusa.org contact page; give.salvationarmyusa.org"),
    "861626267": ("https://murmuration.org/", "search: civictech directory listing murmuration.org (not confirmed on own page)"),
    "821934592": ("https://www.ted.com/", "search: ted.com/support names TED Foundation Inc EIN 82-1934592"),
    "135563422": ("https://www.crs.org/", "search: crs.org own pages"),
    "953188150": ("https://www.focusonthefamily.com/", "search: focusonthefamily.com contact/CFC pages"),
    "530196617": ("https://www.usccb.org/", "search: usccb.org own pages"),
    "956006144": ("https://ucsd.edu/", "search: ucsd.edu/about; giving.ucsd.edu"),
    "731486708": ("https://www.life.church/", "search: life.church (formerly Life Covenant Church)"),
    "946002123": ("https://www.berkeley.edu/", "search: give.berkeley.edu (berkeley.edu domain)"),
    "876000525": ("https://www.utah.edu/", "search: giving.utah.edu (utah.edu domain)"),
    "463508366": ("https://standtogethertrust.org/", "search: standtogethertrust.org home page"),
    "060923895": ("https://legionariesofchrist.org/", "search: legionariesofchrist.org (US territory site)"),
    "873467861": ("https://www.yadeliezer.org/", "search: yadeliezer.org; link of this US EIN to the domain not confirmed"),
    "271401401": ("https://gracefarms.org/", "search: gracefarms.org/about; CauseIQ lists gracefarms.org"),
    "330838929": ("https://seedcompany.com/", "search: seedcompany.com (cited by Wikipedia)"),
    "363155315": ("https://www.nm.org/", "search: nm.org/about-us/foundation/donations"),
    "821503998": ("https://worthingtonscholars.org/", "search: worthingtonscholars.org (college listings, Submittable)"),
}


# ============================================================================ stage: rank
def load_bmf_full(bmf_dir: str, eins: frozenset) -> dict:
    out = {}
    for f in BMF_FILES:
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="latin-1", newline="") as fh:
            for r in csv.DictReader(fh):
                e = ein9(r["EIN"])
                if e in eins:
                    out[e] = {"ntee": (r.get("NTEE_CD") or "").strip().upper(),
                              "foundation": (r.get("FOUNDATION") or "").strip(),
                              "subsection": (r.get("SUBSECTION") or "").strip(),
                              "bmf_name": (r.get("NAME") or "").strip(), "bmf_state": (r.get("STATE") or "").strip(),
                              "revenue": num(r.get("REVENUE_AMT") or "") or 0.0,
                              "assets": num(r.get("ASSET_AMT") or "") or 0.0,
                              "bmf_tax_period": (r.get("TAX_PERIOD") or "").strip()}
    return out


def size_band(revenue: float, in_bmf: bool) -> str:
    if not in_bmf or not revenue:
        return "unknown"
    return ("a_lt_10m" if revenue < 1e7 else "b_10m_100m" if revenue < 1e8 else
            "c_100m_1bn" if revenue < 1e9 else "d_ge_1bn")


def aggregate_recipients(ann: Mapping, panel: Mapping) -> dict:
    """recipient EIN -> {amount, grantors, names}; non-D2D lines from non-university grantors with an EIN."""
    acc: dict = defaultdict(lambda: {"amount": 0.0, "grantors": set(), "names": Counter(), "lines": 0})
    for (g, _fy), rows in ann.items():
        if panel[g]["segment"] == "university_hospital":
            continue
        for r in rows:
            if r["d2d"] or not r["ein"]:
                continue
            a = acc[r["ein"]]
            a["amount"] += r["amount"]
            a["grantors"].add(g)
            a["names"][r["name"]] += 1
            a["lines"] += 1
    return acc


def stage_rank(a) -> int:
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
    eins = frozenset(l[0] for v in good.values() for l in v["lines"] if l[0])
    bmf = load_bmf_full(a.bmf_dir, eins)
    ann = {k: annotate(k[0], v["lines"], bmf, wl_eins, wl_names) for k, v in good.items()}
    acc = aggregate_recipients(ann, panel)

    def excl_reason(e):
        if e in panel and panel[e]["segment"] in SPONSOR_SEGMENTS:
            return "dafrc_sponsor_" + panel[e]["segment"]
        if e not in bmf:
            return "not_in_bmf"
        if bmf[e]["ntee"].startswith("T31"):
            return "ntee_t31_community_foundation"  # DAF sponsors outside the DAFRC panel (e.g. NCF affiliate)
        return ""
    ordered = sorted(acc.items(), key=lambda kv: -kv[1]["amount"])
    excluded, kept = [], []
    for e, v in ordered:
        if len(kept) >= a.n:
            break
        (excluded if excl_reason(e) else kept).append((e, v))
    net_total = sum(v["amount"] for v in acc.values())

    def target(i, e, v):
        b = bmf[e]
        g, ntee, method = classify(e, v["names"].most_common(1)[0][0], "", bmf)
        return {"daf_rank": i, "ein": e, "name": b["bmf_name"] or v["names"].most_common(1)[0][0],
                "schedule_i_name": v["names"].most_common(1)[0][0], "state": b["bmf_state"],
                "daf_grant_usd_fy2023_2024": round(v["amount"]), "grantor_sponsors": len(v["grantors"]),
                "schedule_i_lines": v["lines"], "ntee_cd": b["ntee"], "ntee_major_group": g,
                "sector_method": method, "revenue_usd_bmf": round(b["revenue"]), "assets_usd_bmf": round(b["assets"]),
                "bmf_tax_period": b["bmf_tax_period"], "size_band": size_band(b["revenue"], True),
                "dafrc_university_hospital": int(e in panel and panel[e]["segment"] == "university_hospital")}
    targets = [target(i + 1, e, v) for i, (e, v) in enumerate(kept)]
    summ = {"sponsor_years_itemising": len(item), "lines_loaded_ok": len(good),
            "grantor_sponsor_years_non_university": sum(1 for k in good if panel[k[0]]["segment"] != "university_hospital"),
            "recipients_with_ein_non_d2d": len(acc), "net_usd_with_ein": round(net_total),
            "sample_n": len(targets), "sample_usd": sum(t["daf_grant_usd_fy2023_2024"] for t in targets),
            "sample_share_of_net_usd_with_ein": round(sum(t["daf_grant_usd_fy2023_2024"] for t in targets) / net_total, 4),
            "cutoff_usd": targets[-1]["daf_grant_usd_fy2023_2024"] if targets else None,
            "excluded_above_cutoff": [{"ein": e, "name": v["names"].most_common(1)[0][0], "usd": round(v["amount"]),
                                       "reason": excl_reason(e)} for e, v in excluded],
            "excluded_counts": dict(Counter(excl_reason(e) for e, _ in excluded))}
    save_json(os.path.join(a.work, "targets.json"), {"summary": summ, "targets": targets})
    print(json.dumps({k: v for k, v in summ.items() if k != "excluded_above_cutoff"}, indent=1))
    return 0


# ============================================================================ stage: websites
def latest_filings(index_dir: str, eins: frozenset, keep: int = 4) -> dict:
    """EIN -> up to `keep` e-filed 990/990EZ index rows, newest first (TAX_PERIOD, SUB_DATE); index years 2019-2026."""
    acc: dict = defaultdict(list)
    for y in range(2019, 2027):
        p = os.path.join(index_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            continue
        with open(p, encoding="latin-1", newline="") as fh:
            for r in csv.DictReader(fh):
                e = ein9(r.get("EIN") or "")
                if e not in eins or (r.get("RETURN_TYPE") or "").strip() not in ("990", "990EZ"):
                    continue
                acc[e].append(((r.get("TAX_PERIOD") or ""), (r.get("SUB_DATE") or ""), r.get("OBJECT_ID") or "",
                               {"oid": r["OBJECT_ID"].strip(), "tax_period": r["TAX_PERIOD"].strip(),
                                "return_type": r["RETURN_TYPE"].strip()}))
    return {e: [v[3] for v in sorted(vs, key=lambda v: v[:3], reverse=True)][:keep] for e, vs in acc.items()}


REV_RX = re.compile(r"<(?:\w+:)?(?:CYTotalRevenueAmt|TotalRevenueAmt)>\s*(-?\d+)\s*<")
WEB_RX = re.compile(r"<(?:\w+:)?WebsiteAddressTxt>\s*([^<]*?)\s*</(?:\w+:)?WebsiteAddressTxt>", re.I)


def fetch_website_field(oid: str) -> dict:
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA, "Range": "bytes=0-262143"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read().decode("utf-8", "replace")
            m, rv = WEB_RX.search(body), REV_RX.search(body)
            return {"status": "ok", "website_raw": html.unescape(m.group(1)) if m else "",
                    "revenue_990": num(rv.group(1)) if rv else None}
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"status": f"http_{e.code}", "website_raw": ""}
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            time.sleep(2 * (attempt + 1))
    return {"status": "error", "website_raw": ""}


BAD_SITE = re.compile(r"^(n/?a|none|no|na|nil|null|-+|0|not applicable|no website|www)$", re.I)


def clean_url(raw: str) -> str:
    s = (raw or "").strip().strip(".,;").replace("\\", "/")
    if not s or BAD_SITE.match(s) or " " in s.strip() or "@" in s:
        return ""
    s = re.sub(r"^(https?:?/*)", "", s, flags=re.I)
    host = s.split("/")[0].lower().strip(".")
    if "." not in host or not re.fullmatch(r"[a-z0-9.\-]+", host):
        return ""
    return "https://" + host + "/"


def stage_websites(a) -> int:
    t = load_json(os.path.join(a.work, "targets.json"))["targets"]
    eins = frozenset(x["ein"] for x in t)
    cache_p = os.path.join(a.work, "websites.json")
    cache = load_json(cache_p) if os.path.exists(cache_p) else {}
    fil = latest_filings(a.index_dir, eins)
    todo = [e for e in eins if e in fil and (e not in cache or not clean_url(cache[e].get("website_raw", "")))]

    def one(e):
        """Newest filing first; fall back to older filings when the mirror lacks the object or the field is empty."""
        tried, best = [], None
        for f in fil[e]:
            time.sleep(0.2)
            r = {**f, **fetch_website_field(f["oid"])}
            tried.append(f"{f['oid']}:{r['status']}")
            best = best if (best and best["status"] == "ok" and not r["status"] == "ok") else (best if best and best.get("revenue_990") and not clean_url(r.get("website_raw", "")) else r)
            if clean_url(r.get("website_raw", "")):
                best = r
                break
        return e, {**best, "tried": tried, "filings_newer_than_used": tried.index(f"{best['oid']}:{best['status']}")}
    with ThreadPoolExecutor(max_workers=4) as ex:
        got = dict(ex.map(one, todo))
    cache = {**cache, **got, **{e: {"status": "no_efiled_990_in_index_2019_2026", "website_raw": ""}
                                for e in eins if e not in fil}}
    save_json(cache_p, cache)
    c = Counter(v["status"] for v in cache.values())
    usable = sum(1 for e in eins if clean_url(cache[e].get("website_raw", "")))
    missing = [(x["daf_rank"], x["ein"], x["name"], cache[x["ein"]].get("website_raw", ""), cache[x["ein"]]["status"])
               for x in t if not clean_url(cache[x["ein"]].get("website_raw", "")) and x["ein"] not in MANUAL_SITES]
    print(json.dumps({"status": c, "usable_990_url": usable, "manual": len(MANUAL_SITES), "missing": missing}, indent=1))
    return 0


def site_of(t: Mapping, web: Mapping) -> tuple[str, str]:
    w = web.get(t["ein"], {})
    u = clean_url(w.get("website_raw", ""))
    if u:
        return u, f"990 WebsiteAddressTxt ({w.get('return_type')} TP {w.get('tax_period')}, object {w.get('oid')})"
    if t["ein"] in MANUAL_SITES:
        return MANUAL_SITES[t["ein"]][0], "manual web search: " + MANUAL_SITES[t["ein"]][1]
    return "", "none"


# ============================================================================ robots (I/O)
_robots: dict = {}
_robots_lock = threading.Lock()
_host_last: dict = defaultdict(float)
_host_lock = threading.Lock()


def host_wait(host: str) -> None:
    with _host_lock:
        now = time.time()
        slot = max(now, _host_last[host] + HOST_GAP)
        _host_last[host] = slot
    time.sleep(max(0.0, slot - time.time()))


def robots_for(scheme_host: str) -> dict:
    """-> {'state': ok|none|unreadable, 'code', 'parser'|None}. Cached per scheme://host."""
    with _robots_lock:
        if scheme_host in _robots:
            return _robots[scheme_host]
    host = urllib.parse.urlsplit(scheme_host).hostname or ""
    host_wait(host)
    url = scheme_host.rstrip("/") + "/robots.txt"
    res: dict
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read(500_000).decode("utf-8", "replace")
            final = resp.geturl()
        if "<html" in body[:500].lower() and "user-agent" not in body.lower():
            res = {"state": "none", "code": "200_html_no_rules", "parser": None}  # soft-404 page served as robots
        else:
            rp = urllib.robotparser.RobotFileParser()
            rp.parse(body.splitlines())
            res = {"state": "ok", "code": "200" + ("" if final == url else " via " + final), "parser": rp}
    except urllib.error.HTTPError as e:
        res = ({"state": "none", "code": str(e.code), "parser": None} if e.code in (404, 410)
               else {"state": "unreadable", "code": str(e.code), "parser": None})
    except Exception as e:  # noqa: BLE001 - network edge
        res = {"state": "unreadable", "code": type(e).__name__, "parser": None}
    with _robots_lock:
        _robots[scheme_host] = res
    return res


def allowed(url: str) -> tuple[str, str]:
    """-> (verdict allowed|disallowed|unreadable, robots code)."""
    p = urllib.parse.urlsplit(url)
    r = robots_for(f"{p.scheme}://{p.netloc}")
    if r["state"] == "unreadable":
        return "unreadable", r["code"]
    if r["state"] == "none":
        return "allowed", r["code"]
    return ("allowed" if r["parser"].can_fetch("*", url) else "disallowed"), r["code"]


# ============================================================================ render (node + Playwright)
NODE_HELPER = r"""
const fs = require('fs');
const { chromium } = require(process.env.PW_MODULE || 'playwright');
const [jobsPath, outDir, conc] = process.argv.slice(2);
const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));
const GAP = 1100, last = {};
const cap = (s, n) => (s && s.length > n ? s.slice(0, n) : s || '');
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function hostWait(h) { const now = Date.now(); const slot = Math.max(now, (last[h] || 0) + GAP); last[h] = slot; await sleep(slot - now); }
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome',
    proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
  let i = 0;
  async function worker() {
    while (i < jobs.length) {
      const j = jobs[i++];
      const out = { id: j.id, url: j.url, requests: [], frames: [] };
      const ctx = await browser.newContext({ userAgent: process.env.UA, javaScriptEnabled: true });
      const page = await ctx.newPage();
      await page.route('**/*', r => ['image', 'media', 'font'].includes(r.request().resourceType()) ? r.abort() : r.continue());
      page.on('request', r => { if (out.requests.length < 3000) out.requests.push(r.url()); });
      page.on('dialog', d => d.dismiss().catch(() => {}));
      try {
        await hostWait(new URL(j.url).hostname);
        const resp = await page.goto(j.url, { waitUntil: 'domcontentloaded', timeout: 35000 });
        out.status = resp ? resp.status() : null;
        try { out.raw = cap(await resp.text(), 3000000); } catch (e) { out.raw = ''; }
        try { await page.waitForLoadState('networkidle', { timeout: 10000 }); } catch (e) {}
        await sleep(2500);
        out.final_url = page.url();
        out.html = cap(await page.content(), 4000000);
        out.title = await page.title().catch(() => '');
        for (const f of page.frames()) {
          if (f === page.mainFrame()) continue;
          let c = ''; try { c = await f.content(); } catch (e) {}
          out.frames.push({ url: f.url(), html: cap(c, 600000) });
          if (out.frames.length >= 25) break;
        }
      } catch (e) { out.error = String(e).slice(0, 300); out.final_url = page.url(); }
      fs.writeFileSync(`${outDir}/${j.id}.json`, JSON.stringify(out));
      await ctx.close();
    }
  }
  await Promise.all(Array.from({ length: Number(conc) || 4 }, worker));
  await browser.close();
})();
"""


def render(jobs: Sequence[Mapping], out_dir: str, work: str, conc: int = 5) -> None:
    todo = [j for j in jobs if not os.path.exists(os.path.join(out_dir, f"{j['id']}.json"))]
    if not todo:
        return
    os.makedirs(out_dir, exist_ok=True)
    hp, jp = os.path.join(work, "render_helper.js"), os.path.join(work, f"jobs_{os.path.basename(out_dir)}.json")
    with open(hp, "w") as fh:
        fh.write(NODE_HELPER)
    save_json(jp, list(todo))
    env = {**os.environ, "UA": UA, "PW_MODULE": os.environ.get("PW_MODULE", "/opt/node-tools/node_modules/playwright")}
    subprocess.run(["node", hp, jp, out_dir, str(conc)], env=env, check=False, timeout=7200)


# ============================================================================ link discovery (pure)
class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self._cur = [], None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self._cur = {"href": d["href"], "text": " ".join(filter(None, (d.get("aria-label"), d.get("title")))), "parts": []}
        elif tag in ("img",) and self._cur is not None and d.get("alt"):
            self._cur["parts"].append(d["alt"])

    def handle_data(self, data):
        if self._cur is not None:
            self._cur["parts"].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._cur is not None:
            c = self._cur
            self.links.append((c["href"].strip(), re.sub(r"\s+", " ", (" ".join(c["parts"]) + " " + c["text"])).strip()))
            self._cur = None


def links_of(doc: str) -> list:
    p = Links()
    try:
        p.feed(doc or "")
    except Exception:  # noqa: BLE001 - malformed HTML
        pass
    return p.links


SKIP_HOST = re.compile(r"(facebook|twitter|x\.com|instagram|linkedin|youtube|tiktok|pinterest|flickr|vimeo)\.", re.I)
SPONSOR_HOST = re.compile(r"(fidelitycharitable|dafgiving360|schwabcharitable|vanguardcharitable|nptrust|dafdirect)\.", re.I)


def link_score(href: str, text: str) -> int:
    t, h = text.lower(), urllib.parse.urlsplit(href).path.lower() + "?" + urllib.parse.urlsplit(href).query.lower()
    host = (urllib.parse.urlsplit(href).hostname or "").lower()
    if re.search(r"\bdonat", t) or re.search(r"donat", h) or host.startswith("donate."):
        return 4
    if re.search(r"\b(give now|give today|give online|make a gift|make a donation|ways to give|give)\b", t):
        return 3
    if re.search(r"(^|/)(give|giving|make-a-gift|makeagift|support-us|ways-to-give)(/|$|\?|-)", h) or host.startswith(("give.", "giving.")):
        return 2
    if re.search(r"\b(support us|support|giving)\b", t):
        return 1
    return 0


def pick_donate(base: str, doc: str) -> tuple[str, str, int]:
    """-> (absolute url, anchor text, score) of the best donate/give link, or ('', '', 0)."""
    cands = []
    for i, (href, text) in enumerate(links_of(doc)):
        if re.match(r"^(mailto|tel|javascript|sms):", href, re.I):
            continue
        u = urllib.parse.urljoin(base, href)
        sp = urllib.parse.urlsplit(u)
        if sp.scheme not in ("http", "https") or SKIP_HOST.search(sp.hostname or "") or SPONSOR_HOST.search(sp.hostname or ""):
            continue
        if re.search(r"\.(pdf|docx?|jpe?g|png)$", sp.path, re.I):
            continue
        s = link_score(u, text)
        if s:
            cands.append((s, -i, u, text[:80]))
    if not cands:
        return "", "", 0
    s, _, u, text = max(cands)
    return u, text, s


def same_page(a: str, b: str) -> bool:
    n = lambda u: urllib.parse.urlsplit(u)._replace(fragment="").geturl().rstrip("/").lower()  # noqa: E731
    return n(a) == n(b)


# ============================================================================ detection (pure)
SIG = {
    # widget/script, a DAFpay link, or an active DAFpay payment method in the page's config. Platform-generic strings
    # (Classy "paymentMethods.dafpay.label", Fundraise Up ".ui-payment-button-dafpay" CSS) do NOT count: see DAFPAY_GENERIC.
    "dafpay_chariot": re.compile(r"givechariot\.com|chariot-connect|<chariot-|dafpay\.com|\"DAFPay\"\}|\"status\":\"ACTIVE\",\"type\":\"DAFPay\"", re.I),
    "daf_direct": re.compile(r"dafdirect\.org|\bdaf ?direct\b", re.I),
    "fidelity_charitable": re.compile(r"fidelitycharitable\.org|fidelity charitable", re.I),
    "dafgiving360_schwab": re.compile(r"dafgiving360|schwabcharitable\.org|schwab charitable", re.I),
    "vanguard_charitable": re.compile(r"vanguardcharitable\.org|vanguard charitable", re.I),
    "npt": re.compile(r"nptrust\.org|national philanthropic trust", re.I),
    "every_org": re.compile(r"every\.org", re.I),
    "paypal_giving_fund": re.compile(r"paypal giving fund|paypal\.com/(?:[a-z]{2}/)?fundraiser/charity|paypalgivingfund", re.I),
    "daffy": re.compile(r"daffy\.org", re.I),
    "endaoment": re.compile(r"endaoment\.org", re.I),
    "benevity": re.compile(r"benevity\.(?:org|com)|causes\.benevity", re.I),
}
LINK_SIG = {k: re.compile(p, re.I) for k, p in {
    "fidelity_charitable": r"fidelitycharitable\.org", "dafgiving360_schwab": r"dafgiving360\.org|schwabcharitable\.org",
    "vanguard_charitable": r"vanguardcharitable\.org", "npt": r"nptrust\.org"}.items()}
DAFPAY_GENERIC = re.compile(r"paymentMethods\.dafpay|ui-payment-button-dafpay|#dafpay-button|\bdafpay\b", re.I)
DAFPAY_TEXT = re.compile(r"\bDAF ?pay\b", re.I)
DAFPAY_WIDGET = re.compile(r"givechariot\.com|chariot-connect|<chariot-", re.I)
DAFDIRECT_WIDGET = re.compile(r"dafdirect\.org/\S*(?:widget|ddirect)|dafwidget", re.I)
PLATFORMS = {
    "fundraise_up": r"fundraiseup\.com", "classy_gofundme_pro": r"classy\.org|classy-cdn|gofundme\.com/pro|givecloud",
    "blackbaud": r"blackbaud|bbcdn\.|luminatecdn|convio|donorperfect\.blackbaud|bbis|sky\.blackbaudcdn",
    "givebutter": r"givebutter\.com", "donorbox": r"donorbox\.org", "give_lively": r"givelively\.org",
    "qgiv": r"qgiv\.com", "bloomerang_kindful": r"bloomerang|kindful\.com", "engaging_networks": r"engagingnetworks|e-activist\.com",
    "everyaction_ngpvan": r"everyaction|ngpvan\.com|secure\.ngpvan|act\.myngp", "idonate": r"idonate\.com",
    "donorperfect": r"donorperfect\.net|donorperfect\.com", "neon": r"neoncrm|neonone", "funraise": r"funraise\.(?:io|org)",
    "network_for_good_bonterra": r"networkforgood|bonterratech|mobilecause", "raisely": r"raisely\.com",
    "springly_onecause": r"onecause\.com", "salesforce_nonprofit": r"force\.com/(?:donate|s/)|salesforce-sites",
    "stripe_checkout": r"js\.stripe\.com|checkout\.stripe\.com", "virtuous": r"virtuoussoftware|virtuous\.org/give",
    "givesmart_dojiggy": r"givesmart\.com", "tithely_pushpay": r"tithe\.ly|pushpay\.com",
}
PLATFORM_RX = {k: re.compile(v, re.I) for k, v in PLATFORMS.items()}
DAF_TEXT = re.compile(r"donor[\s\-‐-—]*advised", re.I)
DAF_ACRONYM = re.compile(r"\bDAFs?\b")
EIN_LABEL = re.compile(r"\b(EIN|Tax[\s\-]?ID|Federal (?:Tax )?ID|Tax Identification Number|Employer Identification)\b", re.I)
CHALLENGE = re.compile(r"cf-chl|challenge-platform|Just a moment\.\.\.|Attention Required!|px-captcha|"
                       r"Access Denied</title>|Request unsuccessful\. Incapsula|_Incapsula_Resource|captcha-delivery", re.I)


def visible_text(doc: str) -> str:
    s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", doc or "")
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s))


def hrefs_and_srcs(doc: str) -> str:
    return " ".join(re.findall(r"""(?:href|src|action|data-src)\s*=\s*["']([^"']+)""", doc or "", re.I))


def page_blob(p: Mapping) -> dict:
    """Combine raw HTML, rendered DOM, child frames and request URLs into searchable parts."""
    frames = p.get("frames") or []
    markup = "\n".join([p.get("raw") or "", p.get("html") or ""] + [f.get("html") or "" for f in frames])
    urls = "\n".join((p.get("requests") or []) + [f.get("url") or "" for f in frames])
    text = visible_text(p.get("html") or p.get("raw") or "") + " " + " ".join(visible_text(f.get("html") or "") for f in frames)
    return {"markup": markup, "urls": urls, "text": text, "links": hrefs_and_srcs(markup)}


def detect(p: Mapping, ein: str) -> dict:
    b = page_blob(p)
    allm = b["markup"] + "\n" + b["urls"]
    ein_fmt = f"{ein[:2]}-{ein[2:]}"
    d = {k: int(bool(rx.search(allm))) for k, rx in SIG.items()}
    d["dafpay_text"] = int(bool(DAFPAY_TEXT.search(b["text"])))
    d["dafpay_chariot"] = int(d["dafpay_chariot"] or d["dafpay_text"])
    d["dafpay_generic_string_only"] = int(not d["dafpay_chariot"] and bool(DAFPAY_GENERIC.search(allm)))
    d["dafpay_widget"] = int(bool(DAFPAY_WIDGET.search(allm)))
    d["daf_direct_widget"] = int(bool(DAFDIRECT_WIDGET.search(allm)))
    for k, rx in LINK_SIG.items():
        d[k + "_link"] = int(bool(rx.search(b["links"] + "\n" + b["urls"])))
    d["sponsor_specific_any"] = int(any(d[k] for k in ("fidelity_charitable", "dafgiving360_schwab", "vanguard_charitable", "npt")))
    d["sponsor_link_any"] = int(any(d[k + "_link"] for k in LINK_SIG))
    d["text_donor_advised"] = int(bool(DAF_TEXT.search(b["text"])))
    d["text_daf_acronym"] = int(bool(DAF_ACRONYM.search(b["text"])))
    d["daf_text_any"] = int(d["text_donor_advised"] or d["text_daf_acronym"])
    d["ein_own_displayed"] = int(ein_fmt in b["text"] or bool(re.search(rf"(?<!\d){ein}(?!\d)", b["text"])))
    d["ein_label_present"] = int(bool(EIN_LABEL.search(b["text"])))
    d["daf_adjacent_processor_any"] = int(any(d[k] for k in ("every_org", "paypal_giving_fund", "daffy", "endaoment", "benevity")))
    d["platforms"] = ";".join(k for k, rx in PLATFORM_RX.items() if rx.search(allm))
    d["any_daf_option"] = int(any(d[k] for k in ("dafpay_chariot", "daf_direct", "sponsor_specific_any", "daf_text_any")))
    return d


def page_state(p: Mapping | None) -> str:
    if p is None:
        return "not_fetched"
    if p.get("error") and not p.get("html"):
        return "error:" + re.sub(r"\s.*", "", (p.get("error") or "").split("\n")[0])[:60]
    st = p.get("status")
    if st and st >= 400:
        return f"http_{st}"
    if CHALLENGE.search((p.get("html") or "")[:200000]) and len(visible_text(p.get("html") or "")) < 3000:
        return "bot_challenge"
    return "ok"


# ============================================================================ stage: scan
def stage_scan(a) -> int:
    t = load_json(os.path.join(a.work, "targets.json"))["targets"]
    web = load_json(os.path.join(a.work, "websites.json"))
    plan_p = os.path.join(a.work, "plan.json")
    plan = load_json(plan_p) if os.path.exists(plan_p) else {}
    home_dir, don_dir = os.path.join(a.work, "home"), os.path.join(a.work, "donate")

    # 1. robots for homepages
    sites = {x["ein"]: site_of(x, web) for x in t}

    def home_check(x):
        url, src = sites[x["ein"]]
        if not url:
            return x["ein"], {"site": "", "site_source": src, "home_robots": "", "home_robots_code": ""}
        v, code = allowed(url)
        return x["ein"], {"site": url, "site_source": src, "home_robots": v, "home_robots_code": code}
    with ThreadPoolExecutor(max_workers=12) as ex:
        hc = dict(ex.map(home_check, t))
    plan = {e: {**plan.get(e, {}), **hc[e]} for e in hc}
    save_json(plan_p, plan)
    render([{"id": e, "url": p["site"]} for e, p in plan.items() if p["home_robots"] == "allowed"], home_dir, a.work)

    # 2. redirect robots check + donate link
    def donate_check(e):
        p = plan[e]
        if p["home_robots"] != "allowed":
            return e, {}
        h = load_json(os.path.join(home_dir, f"{e}.json")) if os.path.exists(os.path.join(home_dir, f"{e}.json")) else None
        st = page_state(h)
        out = {"home_state": st, "home_final_url": (h or {}).get("final_url", "")}
        if h and not same_host(p["site"], h.get("final_url") or p["site"]) and h.get("final_url", "").startswith("http"):
            v, code = allowed(h["final_url"])
            out["home_redirect_robots"] = v
            if v != "allowed":
                out["home_state"] = "robots_" + v + "_after_redirect"
                return e, out
        if out["home_state"] != "ok":
            return e, out
        base = h.get("final_url") or p["site"]
        u, text, score = pick_donate(base, (h.get("html") or "") + (h.get("raw") or ""))
        out.update({"donate_url": u, "donate_anchor": text, "donate_score": score})
        if not u:
            out["donate_state"] = "no_donate_link_found"
        elif same_page(u, base):
            out["donate_state"] = "donate_on_homepage"
        else:
            v, code = allowed(u)
            out["donate_robots"], out["donate_robots_code"] = v, code
            out["donate_state"] = "to_fetch" if v == "allowed" else "robots_" + v
        return e, out
    with ThreadPoolExecutor(max_workers=12) as ex:
        dc = dict(ex.map(donate_check, list(plan)))
    plan = {e: {**plan[e], **dc[e]} for e in plan}
    save_json(plan_p, plan)
    render([{"id": e, "url": p["donate_url"]} for e, p in plan.items() if p.get("donate_state") == "to_fetch"], don_dir, a.work)

    # 3. donate redirect robots
    def donate_after(e):
        p = plan[e]
        if p.get("donate_state") != "to_fetch":
            return e, {}
        d = load_json(os.path.join(don_dir, f"{e}.json")) if os.path.exists(os.path.join(don_dir, f"{e}.json")) else None
        out = {"donate_page_state": page_state(d), "donate_final_url": (d or {}).get("final_url", "")}
        if d and d.get("final_url", "").startswith("http") and not same_host(p["donate_url"], d["final_url"]):
            v, _ = allowed(d["final_url"])
            out["donate_redirect_robots"] = v
            if v != "allowed":
                out["donate_page_state"] = "robots_" + v + "_after_redirect"
        return e, out
    with ThreadPoolExecutor(max_workers=12) as ex:
        da = dict(ex.map(donate_after, list(plan)))
    plan = {e: {**plan[e], **da[e]} for e in plan}
    save_json(plan_p, plan)
    print(json.dumps({"home_robots": Counter(p["home_robots"] or "no_site" for p in plan.values()),
                      "home_state": Counter(p.get("home_state", "-") for p in plan.values()),
                      "donate_state": Counter(p.get("donate_state", "-") for p in plan.values()),
                      "donate_page_state": Counter(p.get("donate_page_state", "-") for p in plan.values())}, indent=1))
    return 0


def same_host(a: str, b: str) -> bool:
    h = lambda u: re.sub(r"^www\.", "", (urllib.parse.urlsplit(u).hostname or "").lower())  # noqa: E731
    return h(a) == h(b)


# ============================================================================ stage: report
FLAG_COLS = ("dafpay_chariot", "dafpay_widget", "dafpay_text", "dafpay_generic_string_only", "daf_direct", "daf_direct_widget", "fidelity_charitable",
             "fidelity_charitable_link", "dafgiving360_schwab", "dafgiving360_schwab_link", "vanguard_charitable",
             "vanguard_charitable_link", "npt", "npt_link", "sponsor_specific_any", "sponsor_link_any",
             "text_donor_advised", "text_daf_acronym", "daf_text_any", "ein_own_displayed", "ein_label_present",
             "every_org", "paypal_giving_fund", "daffy", "endaoment", "benevity", "daf_adjacent_processor_any",
             "any_daf_option")
FIELDS = (["daf_rank", "ein", "name", "schedule_i_name", "state", "ntee_cd", "ntee_major_group", "sector_method",
           "size_band", "size_source", "revenue_usd", "dafrc_university_hospital", "daf_grant_usd_fy2023_2024", "grantor_sponsors",
           "website", "website_source", "home_robots", "home_robots_code", "home_state", "donate_url", "donate_anchor",
           "donate_state", "donate_robots", "donate_page_state", "page_scanned", "scan_status"]
          + [f"donate_{c}" for c in FLAG_COLS] + ["donate_platforms"]
          + [f"either_{c}" for c in FLAG_COLS] + ["either_platforms", "accessed", "source"])
SOURCE = ("Recipients: IRS Form 990 Schedule I Part II lines of top-50 DAF sponsors FY2023-24 (mission_recipient_sectors.py "
          "lines cache) ex DAF-to-DAF and ex DAFRC sponsor EINs; BMF eo1-eo4 (NTEE, REVENUE_AMT); website: recipient's "
          "990 WebsiteAddressTxt (GivingTuesday mirror of IRS TEOS) or manual search; pages rendered with headless Chrome, "
          "robots.txt checked first")


def scan_status(p: Mapping) -> str:
    if not p.get("site"):
        return "no_website_found"
    if p["home_robots"] == "unreadable":
        return "robots_unreadable_home"
    if p["home_robots"] == "disallowed":
        return "robots_blocked_home"
    hs = p.get("home_state", "")
    if hs.startswith("robots_"):
        return "robots_blocked_home"
    if hs != "ok":
        return "home_unreachable"
    ds = p.get("donate_state", "")
    if ds == "no_donate_link_found":
        return "home_only_no_donate_link"
    if ds == "donate_on_homepage":
        return "donate_on_homepage"
    if ds == "robots_unreadable":
        return "home_only_donate_robots_unreadable"
    if ds.startswith("robots_"):
        return "home_only_donate_robots_blocked"
    dps = p.get("donate_page_state", "")
    if dps.startswith("robots_"):
        return "home_only_donate_robots_blocked"
    if dps != "ok":
        return "home_only_donate_unreachable"
    return "donate_scanned"


def clean_out_url(u: str) -> str:
    """Drop session and tracking parameters from a URL before it is written out."""
    sp = urllib.parse.urlsplit(u or "")
    q = [(k, v) for k, v in urllib.parse.parse_qsl(sp.query, keep_blank_values=True)
         if not re.match(r"(session_?id|utm_|s_src|s_subsrc|ms$|source$|ea\.tracking|supporter\.appeal|en_og_source|sid$|gclid|fbclid)", k, re.I)]
    return sp._replace(query=urllib.parse.urlencode(q)).geturl() if u else ""


def size_of(x: Mapping, web: Mapping) -> tuple[str, str, object]:
    if x["size_band"] != "unknown":
        return x["size_band"], "bmf_revenue_amt", x["revenue_usd_bmf"]
    rv = (web.get(x["ein"]) or {}).get("revenue_990")
    if rv:
        return size_band(rv, True), "990_total_revenue", round(rv)
    return "unknown", "", ""


def build_row(x: Mapping, p: Mapping, work: str, web: Mapping) -> dict:
    st = scan_status(p)
    band, band_src, rev = size_of(x, web)
    jl = lambda d, e: load_json(os.path.join(work, d, f"{e}.json")) if os.path.exists(os.path.join(work, d, f"{e}.json")) else None  # noqa: E731
    home = jl("home", x["ein"]) if st != "no_website_found" and not st.startswith(("robots_", "home_unreachable")) else None
    don = jl("donate", x["ein"]) if st == "donate_scanned" else (home if st == "donate_on_homepage" else None)
    dd = detect(don, x["ein"]) if don else {}
    hd = detect(home, x["ein"]) if home else {}
    either = ({c: int(bool(dd.get(c)) or bool(hd.get(c))) for c in FLAG_COLS} if (dd or hd) else {})
    ep = ";".join(sorted(set(filter(None, (dd.get("platforms", "") + ";" + hd.get("platforms", "")).split(";")))))
    return {**{k: x[k] for k in ("daf_rank", "ein", "name", "schedule_i_name", "state", "ntee_cd", "ntee_major_group",
                                 "sector_method", "dafrc_university_hospital", "daf_grant_usd_fy2023_2024", "grantor_sponsors")},
            "size_band": band, "size_source": band_src, "revenue_usd": rev,
            "website": p.get("site", ""), "website_source": p.get("site_source", ""),
            "home_robots": p.get("home_robots", ""), "home_robots_code": p.get("home_robots_code", ""),
            "home_state": p.get("home_state", ""), "donate_url": clean_out_url(p.get("donate_url", "")),
            "donate_anchor": p.get("donate_anchor", ""), "donate_state": p.get("donate_state", ""),
            "donate_robots": p.get("donate_robots", ""), "donate_page_state": p.get("donate_page_state", ""),
            "page_scanned": "donate" if don else ("homepage" if home else "none"), "scan_status": st,
            **{f"donate_{c}": (dd.get(c, "") if dd else "") for c in FLAG_COLS}, "donate_platforms": dd.get("platforms", ""),
            **{f"either_{c}": either.get(c, "") for c in FLAG_COLS}, "either_platforms": ep,
            "accessed": ACCESSED if (dd or hd) else "", "source": SOURCE}


def rates(rows: Sequence[Mapping], prefix: str, cols: Iterable[str]) -> dict:
    base = [r for r in rows if r[f"{prefix}{'any_daf_option'}"] != ""]
    n = len(base)
    return {"n": n, **{c: (round(sum(int(r[f"{prefix}{c}"]) for r in base) / n, 3) if n else None) for c in cols},
            **{c + "_count": sum(int(r[f"{prefix}{c}"]) for r in base) for c in cols}}


KEY = ("dafpay_chariot", "dafpay_widget", "dafpay_generic_string_only", "daf_direct", "sponsor_specific_any", "sponsor_link_any", "fidelity_charitable",
       "dafgiving360_schwab", "vanguard_charitable", "npt", "daf_text_any", "text_donor_advised", "ein_own_displayed",
       "every_org", "paypal_giving_fund", "daf_adjacent_processor_any", "any_daf_option")


def stage_report(a) -> int:
    tj = load_json(os.path.join(a.work, "targets.json"))
    plan = load_json(os.path.join(a.work, "plan.json"))
    web = load_json(os.path.join(a.work, "websites.json"))
    rows = [build_row(x, plan[x["ein"]], a.work, web) for x in tj["targets"]]
    write_csv(OUT_CSV, rows, FIELDS)
    don = [r for r in rows if r["page_scanned"] == "donate"]
    by = lambda key, rs, pre: {k: rates(v, pre, KEY) for k, v in sorted(_group_by_fast(rs, lambda r: r[key]).items())}  # noqa: E731
    plat = Counter(p for r in don for p in r["donate_platforms"].split(";") if p)
    rank_band = lambda r: "001-100" if r["daf_rank"] <= 100 else "101-200" if r["daf_rank"] <= 200 else "201-300"  # noqa: E731
    summ = {
        "rank_summary": tj["summary"] | {"excluded_above_cutoff": len(tj["summary"]["excluded_above_cutoff"])},
        "scan_status": Counter(r["scan_status"] for r in rows),
        "website_source": Counter(r["website_source"].split(":")[0].split(" (")[0] for r in rows),
        "robots_codes_unreadable": Counter(r["home_robots_code"] for r in rows if r["home_robots"] == "unreadable"),
        "home_state": Counter(r["home_state"] for r in rows if r["home_state"]),
        "donate_page_state": Counter(r["donate_page_state"] for r in rows if r["donate_page_state"]),
        "overall_donate_page": rates(don, "donate_", KEY),
        "overall_donate_or_homepage_page": rates([r for r in rows if r["page_scanned"] != "none"], "either_", KEY),
        "overall_either_page_for_donate_scanned": rates(don, "either_", KEY),
        "by_sector_donate": by("ntee_major_group", don, "donate_"),
        "by_size_donate": by("size_band", don, "donate_"),
        "by_rankband_donate": {k: rates(v, "donate_", KEY) for k, v in sorted(_group_by_fast(don, rank_band).items())},
        "by_univ_hosp_flag_donate": by("dafrc_university_hospital", don, "donate_"),
        "platforms_donate": plat.most_common(),
        "dafpay_by_platform": Counter(p for r in don if int(r["donate_dafpay_chariot"] or 0) for p in (r["donate_platforms"] or "none").split(";")),
        "dafpay_rows": [(r["daf_rank"], r["name"], r["donate_url"], r["donate_dafpay_widget"]) for r in don if int(r["donate_dafpay_chariot"] or 0)],
        "dafdirect_rows": [(r["daf_rank"], r["name"], r["donate_url"]) for r in don if int(r["donate_daf_direct"] or 0)],
        "dollar_weighted_donate": {c: round(sum(r["daf_grant_usd_fy2023_2024"] for r in don if int(r[f"donate_{c}"])) /
                                            max(1, sum(r["daf_grant_usd_fy2023_2024"] for r in don)), 3) for c in KEY},
    }
    save_json(os.path.join(a.work, "summary.json"), summ)
    print(json.dumps(summ, indent=1, default=str))
    return 0


# ============================================================================ io helpers
def save_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, default=lambda o: sorted(o) if isinstance(o, set) else str(o))


def load_json(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stage", choices=("rank", "websites", "scan", "report"))
    ap.add_argument("--work", required=True)
    ap.add_argument("--np-cache")
    ap.add_argument("--bmf-dir")
    ap.add_argument("--lines-cache")
    ap.add_argument("--index-dir")
    ap.add_argument("--n", type=int, default=300)
    a = ap.parse_args(argv)
    return {"rank": stage_rank, "websites": stage_websites, "scan": stage_scan, "report": stage_report}[a.stage](a)


if __name__ == "__main__":
    raise SystemExit(main())
