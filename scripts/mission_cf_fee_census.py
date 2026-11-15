#!/usr/bin/env python3
"""P-NEW-CFC-01: community-foundation consolidation 2021-2026 and CF DAF fee census (top-100 CFs by FY2024 DAF assets).

Public, passive methods only: no logins, no form submissions, no outreach. robots.txt is read before any
fetch on a host and honoured; hosts whose robots.txt cannot be read with a 401/403 are treated as disallowed.

Tasks
  crawl    For each top-100 CF (cf-vendor-map-by-ein-v2.csv, ranked by fy2024_daf_assets_usd): fetch robots.txt,
           the homepage and sitemap(s); pick fee-like pages and PDFs; save text (pdftotext for PDFs) in the cache;
           write candidate fee sentences to <cache>/snippets/<ein>.txt for transcription.  (--fetch for network)
  census   Read the transcribed FEE_SCHEDULES below, verify every quote verbatim (whitespace-normalised) against the
           cached text of its source URL where a cache copy exists, compute the effective annual admin fee at
           $100k, $1m and $10m balances, and write cf-daf-fee-census-2026.csv plus a summary JSON on stdout.
           Compares with national sponsors in sponsor-fee-schedules.csv (computed with the same engine).
  schedn   Scan local IRS e-file XML directories (--xml-dir, repeatable) for Schedule N (Part I liquidation /
           Part II >25% disposition) where filer or transferee is a community foundation, plus fetch (--fetch)
           Part IV lines 31/32 for the top-250 CF filers' 2021+ returns from the GivingTuesday e-file mirror.
  consol   Write cf-consolidation-2021-2026.csv from CONSOLIDATION_EVENTS (transcribed from cited public sources)
           plus Schedule N rows found by `schedn`.

Usage
  python3 scripts/mission_cf_fee_census.py --task crawl --cache-dir CACHE --fetch
  python3 scripts/mission_cf_fee_census.py --task schedn --cache-dir CACHE --xml-dir DIR [--xml-dir DIR2] [--fetch]
  python3 scripts/mission_cf_fee_census.py --task census --cache-dir CACHE
  python3 scripts/mission_cf_fee_census.py --task consol --cache-dir CACHE
Stdlib only, functional style.
"""
from __future__ import annotations

import argparse
import base64
import collections
import concurrent.futures as cf
import csv
import functools
import hashlib
import html
import json
import os
import re
import statistics
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from typing import Iterable, Mapping, Sequence

DATA = "data/mission-2026-11-14"
CF_MAP = f"{DATA}/cf-vendor-map-by-ein-v2.csv"
NATIONAL_FEES = f"{DATA}/sponsor-fee-schedules.csv"
RETURNS_CSV = f"{DATA}/form990-returns-schedule-d-harvest-full.csv"
OUT_FEES = f"{DATA}/cf-daf-fee-census-2026.csv"
OUT_CONSOL = f"{DATA}/cf-consolidation-2021-2026.csv"
RETRIEVED = "2026-11-15"
UA = "Mozilla/5.0 (compatible; DAF-landscape-public-research/1.0; passive, robots-respecting)"
MIN_INTERVAL = 1.05
TOP_N = 100
BALANCES = (100_000, 1_000_000, 10_000_000)

FEE_URL_RE = re.compile(r"fee|cost|pricing|policies|policy|guideline|schedule-of|start-a-fund|open-a-fund|donor-advised|daf|fund-agreement|advisor", re.I)
FEE_STRONG_RE = re.compile(r"fee|cost|pricing", re.I)
PDF_RE = re.compile(r"\.pdf(\?|$)", re.I)
SNIP_RE = re.compile(r"(?i)(admin\w*|fee|minimum|basis points|bps|per year|annual)")
NUM_RE = re.compile(r"\d(\.\d+)?\s?%|\$\s?\d|basis points|\bbps\b")
TAG_RE = re.compile(r"<[^>]+>")
ANCHOR_RE = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.I | re.S)
HREF_RE = re.compile(r"""href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.I)


# ---------------------------------------------------------------- pure helpers
def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def num(x) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def host_of(url: str) -> str:
    try:
        return (urllib.parse.urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def reg_domain(host: str) -> str:
    return ".".join(host.split(".")[-2:])


def norm_ws(s: str) -> str:
    s = html.unescape(s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ").replace("‐", "-").replace("‑", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def html_text(body: str) -> str:
    body = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", body or "")
    body = re.sub(r"(?i)<br\s*/?>|</(p|div|li|tr|h\d|td|th)>", "\n", body)
    return html.unescape(TAG_RE.sub(" ", body))


def anchors(page_html: str, base: str) -> tuple[tuple[str, str], ...]:
    def one(m):
        h = HREF_RE.search(m.group(1))
        if not h:
            return None
        href = html.unescape(next(g for g in h.groups() if g is not None)).strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            return None
        try:
            return urllib.parse.urljoin(base, href).split("#")[0], re.sub(r"\s+", " ", html.unescape(TAG_RE.sub(" ", m.group(2)))).strip()[:160]
        except ValueError:
            return None
    return tuple(a for a in map(one, ANCHOR_RE.finditer(page_html or "")) if a)


def top_cfs(n: int = TOP_N) -> tuple[dict, ...]:
    rows = sorted(read_csv(CF_MAP), key=lambda r: -num(r["fy2024_daf_assets_usd"]))
    return tuple({**r, "rank": i + 1} for i, r in enumerate(rows[:n]))


# ---------------------------------------------------------------- network layer (cached, throttled, binary-safe)
class Net:
    def __init__(self, cache_dir: str, fetch: bool):
        self.dir, self.fetch = os.path.join(cache_dir, "net"), fetch
        os.makedirs(self.dir, exist_ok=True)
        self._locks: dict[str, threading.Lock] = collections.defaultdict(threading.Lock)
        self._last: dict[str, float] = {}
        self._meta = threading.Lock()

    def path(self, url: str) -> str:
        k = hashlib.sha256(url.encode()).hexdigest()
        return os.path.join(self.dir, k[:2], k + ".json")

    def _throttle(self, host: str) -> None:
        with self._meta:
            lock = self._locks[host]
        with lock:
            wait = self._last.get(host, 0) + MIN_INTERVAL - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last[host] = time.monotonic()

    def cached(self, url: str) -> dict | None:
        p = self.path(url)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        return None

    def get(self, url: str, max_bytes: int = 8_000_000, timeout: int = 30) -> dict:
        hit = self.cached(url)
        if hit is not None:
            return hit
        if not self.fetch:
            return {"url": url, "status": "not_cached", "final_url": "", "ctype": "", "b64": ""}
        self._throttle(host_of(url))
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/pdf,application/xml,*/*;q=0.8"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read(max_bytes)
                out = {"url": url, "status": r.status, "final_url": r.geturl(), "ctype": r.headers.get("content-type", ""),
                       "b64": base64.b64encode(body).decode()}
        except urllib.error.HTTPError as e:
            out = {"url": url, "status": e.code, "final_url": url, "ctype": "", "b64": ""}
        except Exception as e:  # noqa: BLE001 - network errors are data
            out = {"url": url, "status": f"error:{type(e).__name__}", "final_url": "", "ctype": "", "b64": ""}
        if isinstance(out["status"], int):
            os.makedirs(os.path.dirname(self.path(url)), exist_ok=True)
            with open(self.path(url), "w", encoding="utf-8") as fh:
                json.dump(out, fh)
        return out


def body_bytes(res: Mapping) -> bytes:
    return base64.b64decode(res.get("b64") or "")


def is_pdf(res: Mapping) -> bool:
    return "pdf" in (res.get("ctype") or "").lower() or body_bytes(res)[:5] == b"%PDF-"


def pdf_to_text(data: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        fh.write(data)
        fh.flush()
        try:
            return subprocess.run(["pdftotext", "-layout", fh.name, "-"], capture_output=True, timeout=60).stdout.decode("utf-8", "replace")
        except (subprocess.SubprocessError, OSError):
            return ""


def res_text(res: Mapping) -> str:
    if res.get("status") != 200:
        return ""
    data = body_bytes(res)
    return pdf_to_text(data) if is_pdf(res) else html_text(data.decode("utf-8", "replace"))


_ROBOTS: dict[str, urllib.robotparser.RobotFileParser | None] = {}
_ROBOTS_LOCK = threading.Lock()


def robots(net: Net, origin: str) -> urllib.robotparser.RobotFileParser | None:
    with _ROBOTS_LOCK:
        if origin in _ROBOTS:
            return _ROBOTS[origin]
    res = net.get(origin + "/robots.txt", max_bytes=300_000, timeout=15)
    rp = urllib.robotparser.RobotFileParser()
    txt = body_bytes(res).decode("utf-8", "replace")
    if res["status"] == 200 and "<html" not in txt[:500].lower():
        rp.parse(txt.splitlines())
    elif res["status"] in (401, 403):
        rp.parse(["User-agent: *", "Disallow: /"])
    else:
        rp = None
    with _ROBOTS_LOCK:
        _ROBOTS[origin] = rp
    return rp


def polite_get(net: Net, url: str) -> dict:
    sp = urllib.parse.urlsplit(url)
    rp = robots(net, f"{sp.scheme}://{sp.netloc}")
    if rp is not None and not rp.can_fetch(UA, url):
        return {"url": url, "status": "robots_disallowed", "final_url": "", "ctype": "", "b64": ""}
    return net.get(url)


# ---------------------------------------------------------------- crawl task
def url_score(url: str, text: str) -> int:
    blob = f"{urllib.parse.urlsplit(url).path} {text}"
    return 4 * bool(FEE_STRONG_RE.search(blob)) + 2 * bool(re.search(r"donor.advised|\bdaf\b|start.a.fund|open.a.fund", blob, re.I)) + bool(FEE_URL_RE.search(blob)) + bool(PDF_RE.search(url))


def sitemap_urls(net: Net, origin: str, depth: int = 0) -> tuple[str, ...]:
    rp = robots(net, origin)
    maps = tuple(getattr(rp, "site_maps", lambda: None)() or ()) if rp else ()
    maps = maps or (origin + "/sitemap.xml", origin + "/sitemap_index.xml")

    def expand(u: str, d: int) -> tuple[str, ...]:
        if d > 1 or host_of(u) and reg_domain(host_of(u)) != reg_domain(host_of(origin)):
            return ()
        res = polite_get(net, u)
        if res["status"] != 200:
            return ()
        locs = tuple(LOC_RE.findall(body_bytes(res).decode("utf-8", "replace")))
        subs = tuple(x for x in locs if re.search(r"sitemap[^/]*\.xml", x, re.I))
        pages = tuple(x for x in locs if x not in subs)
        relevant_subs = tuple(x for x in subs if re.search(r"page|post|resource|document|attachment|media|sitemap\.xml$", x, re.I))[:8]
        return pages + tuple(y for s in relevant_subs for y in expand(s, d + 1))
    return tuple(dict.fromkeys(u for m in maps[:3] for u in expand(m, depth)))


def crawl_one(net: Net, cfrow: Mapping, max_pages: int = 10, max_pdfs: int = 6) -> dict:
    home = cfrow["homepage"]
    origin = f"{urllib.parse.urlsplit(home).scheme}://{urllib.parse.urlsplit(home).netloc}"
    hres = polite_get(net, home)
    links = anchors(body_bytes(hres).decode("utf-8", "replace"), hres.get("final_url") or home) if hres["status"] == 200 else ()
    own = reg_domain(host_of(home))
    smap = sitemap_urls(net, origin)
    cand = {u: url_score(u, t) for u, t in links if reg_domain(host_of(u)) == own and url_score(u, t) >= 4}
    cand.update({u: max(cand.get(u, 0), url_score(u, "")) for u in smap if url_score(u, "") >= 4})
    pages = sorted(cand, key=lambda u: (-cand[u], len(u)))[:max_pages]
    fetched = {u: polite_get(net, u) for u in pages}
    pdfs = {u: url_score(u, t) for p, r in fetched.items() if r["status"] == 200 and not is_pdf(r)
            for u, t in anchors(body_bytes(r).decode("utf-8", "replace"), p) if PDF_RE.search(u) and url_score(u, t) >= 5}
    pdf_list = [u for u in sorted(pdfs, key=lambda u: -pdfs[u]) if u not in fetched][:max_pdfs]
    fetched.update({u: polite_get(net, u) for u in pdf_list})
    texts = {u: res_text(r) for u, r in fetched.items()}
    snips = tuple((u, s) for u, t in texts.items() for s in fee_sentences(t))
    return {"ein": cfrow["ein"], "name": cfrow["name"], "home_status": hres["status"], "n_sitemap": len(smap),
            "fetched": {u: r["status"] for u, r in fetched.items()}, "snippets": snips}


def fee_sentences(text: str) -> tuple[str, ...]:
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in re.split(r"\n|(?<=\.)\s{2,}", text)]
    return tuple(dict.fromkeys(ln[:400] for ln in lines if SNIP_RE.search(ln) and NUM_RE.search(ln) and 10 < len(ln)))


def task_crawl(cache_dir: str, fetch: bool, workers: int, only: frozenset[str]) -> dict:
    net = Net(cache_dir, fetch)
    cfs = tuple(r for r in top_cfs() if not only or r["ein"] in only)
    os.makedirs(os.path.join(cache_dir, "snippets"), exist_ok=True)

    def run(r):
        out = crawl_one(net, r)
        with open(os.path.join(cache_dir, "snippets", f"{r['ein']}.txt"), "w", encoding="utf-8") as fh:
            fh.write(f"# {r['rank']} {r['name']} {r['homepage']} home={out['home_status']} sitemap={out['n_sitemap']}\n")
            fh.writelines(f"# fetched {s} {u}\n" for u, s in out["fetched"].items())
            fh.writelines(f"{u}\t{s}\n" for u, s in out["snippets"])
        return out
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        res = tuple(ex.map(run, cfs))
    return {"cfs": len(res), "home_200": sum(r["home_status"] == 200 for r in res),
            "home_robots_disallowed": sum(r["home_status"] == "robots_disallowed" for r in res),
            "with_snippets": sum(bool(r["snippets"]) for r in res)}


def task_urls(cache_dir: str, fetch: bool, urls: Sequence[str], workers: int) -> dict:
    """Fetch specific fee-page URLs found by search (robots-checked), cache them, write their text to <cache>/texts/."""
    net = Net(cache_dir, fetch)
    os.makedirs(os.path.join(cache_dir, "texts"), exist_ok=True)

    def one(u):
        r = polite_get(net, u)
        t = res_text(r)
        name = hashlib.sha256(u.encode()).hexdigest()[:12]
        with open(os.path.join(cache_dir, "texts", f"{name}.txt"), "w", encoding="utf-8") as fh:
            fh.write(f"# {u} status={r['status']} pdf={is_pdf(r) if r['status'] == 200 else ''}\n{t}")
        return u, r["status"], name, len(t)
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(one, urls))
    return {u: f"{st} {nm} {n}" for u, st, nm, n in res}


# ---------------------------------------------------------------- fee engine
def effective_admin_fee(schedule: Mapping, balance: float, basis: str | None = None) -> float | None:
    """Annual admin fee in USD at a constant balance.
    tiers: ((lower, upper|None, rate_pct), ...). basis 'marginal' (each rate applies to the slice in its tier) or
    'flat_on_total' (the rate of the tier containing the balance applies to the whole balance).
    flat_bands: ((threshold_usd, rate_pct), ...) - if balance > threshold, the highest such band's rate applies to the whole
    balance (hybrid schedules, e.g. 'x% flat on funds over $5M'). cap_usd: balances above it are priced individually -> None.
    Then: minimum annual fee, plus any flat annual fee."""
    tiers = schedule.get("tiers") or ()
    if not tiers and not schedule.get("flat_fee"):
        return None
    if schedule.get("cap_usd") and balance > schedule["cap_usd"]:
        return None
    basis = basis or schedule.get("basis", "marginal")
    bands = [r for t, r in sorted(schedule.get("flat_bands") or ()) if balance > t]
    if bands:
        fee = balance * bands[-1] / 100
    elif basis == "marginal":
        fee = sum(max(0.0, min(balance, up if up is not None else balance) - lo) * rate / 100 for lo, up, rate in tiers)
    else:
        rate = next((r for lo, up, r in tiers if balance >= lo and (up is None or balance < up)), tiers[-1][2] if tiers else 0)
        fee = balance * rate / 100
    fee = max(fee, schedule.get("min_fee") or 0) + (schedule.get("flat_fee") or 0)
    return round(fee, 2)


def bps(fee: float | None, balance: float) -> float | None:
    return None if fee is None else round(fee / balance * 1e4, 1)


def national_schedules() -> dict[str, dict]:
    """National comparators transcribed from sponsor-fee-schedules.csv (see NATIONAL_COMPARATORS in mission_cf_fee_data)."""
    return {n["sponsor"]: {**n, "basis_raw": n.get("note", "")} for n in NATIONAL_COMPARATORS}


def task_census(cache_dir: str) -> dict:
    net = Net(cache_dir, False)
    cfs = top_cfs()
    sched = {s["ein"]: s for s in FEE_DATA}

    def verify(s: Mapping) -> str:
        if not s.get("quotes"):
            return "no_quote"
        texts = [norm_ws(res_text(r)) for u in (s.get("url"), *s.get("alt_urls", ())) if u and (r := net.cached(u)) and r.get("status") == 200]
        if s.get("local"):
            p = os.path.join(cache_dir, s["local"])
            if os.path.exists(p):
                with open(p, "rb") as fh:
                    texts.append(norm_ws(pdf_to_text(fh.read())))
        if not texts:
            return "not_verifiable(webfetch_or_search_capture)"
        hits = [any(norm_ws(q) in t for t in texts) for q in s["quotes"]]
        return f"verified {sum(hits)}/{len(hits)}" if all(hits) else f"MISMATCH {sum(hits)}/{len(hits)}"

    def row(cfr):
        s = sched.get(cfr["ein"], {})
        fees = {b: effective_admin_fee(s, b) if s.get("status") == "published_schedule" else None for b in BALANCES}
        return {"rank": cfr["rank"], "ein": cfr["ein"], "name": cfr["name"], "fy2024_daf_assets_usd": cfr["fy2024_daf_assets_usd"],
                "status": s.get("status", "not_found"), "fund_type": s.get("fund_type", ""),
                "fee_basis": s.get("basis", "") if s.get("tiers") else "",
                "admin_tiers": "; ".join(f"{int(lo):,}-{'' if up is None else f'{int(up):,}'}: {r}%" for lo, up, r in s.get("tiers", ())),
                "min_annual_fee_usd": s.get("min_fee", ""), "flat_annual_fee_usd": s.get("flat_fee", ""),
                "min_opening_usd": s.get("min_open", ""), "min_grant_usd": s.get("min_grant", ""),
                "investment_fee_pass_through": s.get("invest", ""),
                **{f"admin_fee_usd_{b // 1000}k": fees[b] if fees[b] is not None else "" for b in BALANCES},
                **{f"admin_bps_{b // 1000}k": bps(fees[b], b) if fees[b] is not None else "" for b in BALANCES},
                **{f"admin_bps_{b // 1000}k_alt_flat": bps(effective_admin_fee(s, b, "flat_on_total"), b) if s.get("basis_stated") is False and s.get("status") == "published_schedule" else "" for b in BALANCES},
                "basis_stated": {True: "yes", False: "no"}.get(s.get("basis_stated", True) if s.get("tiers") else None, ""),
                "cap_usd": s.get("cap_usd", ""), "contribution_fee_pct": s.get("contrib_fee", ""), "grant_fee_note": s.get("grant_fee", ""),
                "source_url": s.get("url", ""), "source_date": s.get("as_of", ""), "source_method": s.get("method", ""),
                "quote_check": verify(s) if s else "", "notes": s.get("notes", ""), "retrieved": RETRIEVED}
    rows = [row(c) for c in cfs]
    nat = national_schedules()
    nat_rows = [{"rank": "", "ein": "", "name": f"NATIONAL: {n['sponsor']} ({n['program']})", "status": "national_comparator", "fee_basis": n["basis"],
                 "admin_tiers": "; ".join(f"{int(lo):,}-{'' if up is None else f'{int(up):,}'}: {r}%" for lo, up, r in n["tiers"]),
                 "min_annual_fee_usd": n.get("min_fee", ""),
                 **{f"admin_fee_usd_{b // 1000}k": effective_admin_fee(n, b) for b in BALANCES},
                 **{f"admin_bps_{b // 1000}k": bps(effective_admin_fee(n, b), b) for b in BALANCES},
                 "source_url": NATIONAL_FEES, "source_method": "repo", "notes": n["basis_raw"], "retrieved": RETRIEVED} for n in nat.values()]
    fields = list(rows[0].keys())
    write_csv(OUT_FEES, rows + nat_rows, fields)

    pub = [r for r in rows if r["status"] == "published_schedule"]

    def dist(key, rs):
        v = sorted(num(r[key]) for r in rs if r[key] != "")
        if not v:
            return {}
        q = statistics.quantiles(v, n=4) if len(v) >= 4 else [v[0], statistics.median(v), v[-1]]
        return {"n": len(v), "min": v[0], "p25": round(q[0], 1), "median": round(statistics.median(v), 1), "p75": round(q[2], 1), "max": v[-1],
                "mean": round(statistics.mean(v), 1)}
    wts = {r["ein"]: num(r["fy2024_daf_assets_usd"]) for r in pub}

    def wmean(key):
        tot = sum(wts[r["ein"]] for r in pub if r[key] != "")
        return round(sum(num(r[key]) * wts[r["ein"]] for r in pub if r[key] != "") / tot, 1) if tot else None
    status_counts = collections.Counter(r["status"] for r in rows)
    return {"top_n": len(rows), "status_counts": dict(status_counts),
            "coverage_by_daf_assets_pct": round(100 * sum(wts.values()) / sum(num(r["fy2024_daf_assets_usd"]) for r in rows), 1),
            "quote_checks": dict(collections.Counter(r["quote_check"].split(" ")[0] for r in rows if r["quote_check"])),
            "bps": {f"{b // 1000}k": dist(f"admin_bps_{b // 1000}k", pub) for b in BALANCES},
            "bps_daf_asset_weighted_mean": {f"{b // 1000}k": wmean(f"admin_bps_{b // 1000}k") for b in BALANCES},
            "min_fee": dist("min_annual_fee_usd", [r for r in pub if r["min_annual_fee_usd"] not in ("", 0)]),
            "min_open": dist("min_opening_usd", [r for r in rows if r["min_opening_usd"] not in ("",)]),
            "min_grant": dist("min_grant_usd", [r for r in rows if r["min_grant_usd"] not in ("",)]),
            "nationals_bps": {n: {f"{b // 1000}k": bps(effective_admin_fee(s, b), b) for b in BALANCES} for n, s in nat.items()}}


# ---------------------------------------------------------------- Schedule N
def xml_files(dirs: Sequence[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for d in dirs:
        for dp, _, fs in os.walk(d):
            for f in fs:
                if f.endswith(".xml") and re.match(r"\d{18}", f):
                    out.setdefault(f[:18], os.path.join(dp, f))
    return out


def tag(t: str, name: str) -> str:
    m = re.search(rf"<{name}>(.*?)</{name}>", t, re.S)
    return html.unescape(m.group(1)).strip() if m else ""


CF_NAME_RE = re.compile(r"community\s+(foundation|trust|fdn)|foundation for (the )?greater|area foundation|community fund|charitable foundation", re.I)


def parse_schedn(oid: str, t: str) -> dict | None:
    if "IRS990ScheduleN" not in t:
        return None
    filer = t[t.find("<Filer>"):t.find("</Filer>")]
    sn = t[t.find("<IRS990ScheduleN"):t.find("</IRS990ScheduleN>")]
    groups = re.findall(r"<(LiquidationOfAssetsDetail|DispositionOfAssetsDetail)Grp>(.*?)</\1Grp>", sn, re.S)
    det = [{"part": "I_liquidation" if g == "LiquidationOfAssetsDetail" else "II_disposition",
            "desc": tag(b, "AssetsDistriOrExpnssPaidDesc")[:120] or tag(b, "AssetsDistributedOrExpensesPaidDesc")[:120],
            "fmv": tag(b, "FairMarketValueOfAssetAmt"), "date": tag(b, "DistributionDt"),
            "recipient": tag(b, "BusinessNameLine1Txt") or tag(b, "PersonNm"), "recipient_ein": tag(b, "EIN")} for g, b in groups]
    return {"object_id": oid, "filer_ein": tag(filer, "EIN"), "filer_name": tag(filer, "BusinessNameLine1Txt"),
            "tax_year": tag(t, "TaxYr"), "tax_period_end": tag(t, "TaxPeriodEndDt"),
            "terminate_ind": tag(t, "TerminateOperationsInd"), "partial_liq_ind": tag(t, "PartialLiquidationInd"), "details": det}


YES = ("1", "true", "X")


def task_schedn(cache_dir: str, xml_dirs: Sequence[str], fetch: bool, workers: int) -> dict:
    files = xml_files(xml_dirs)
    found = []
    for oid, p in sorted(files.items()):
        with open(p, encoding="utf-8", errors="ignore") as fh:
            t = fh.read()
        r = parse_schedn(oid, t)
        if r:
            found.append({**r, "source": "local_xml"})
    # CF filers' own returns (2021+ tax years) from the e-file mirror (no robots.txt on the S3 host: 404).
    # Stream each return only to </IRS990> to read Part IV lines 31/32; fetch the full XML only when either is yes.
    cf_eins = {r["ein"] for r in read_csv(CF_MAP)}
    rets = [r for r in read_csv(RETURNS_CSV) if r.get("ein", "").zfill(9) in cf_eins and num(r.get("tax_year")) >= 2021 and r.get("xml_url")]
    mdir = os.path.join(cache_dir, "partiv")
    os.makedirs(mdir, exist_ok=True)
    throttle = threading.Semaphore(workers)

    def head_flags(u: str) -> dict:
        oid = re.search(r"(\d{18})_public", u).group(1)
        p = os.path.join(mdir, oid + ".json")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        if not fetch:
            return {"oid": oid, "status": "not_cached"}
        if oid in files:
            with open(files[oid], encoding="utf-8", errors="ignore") as fh:
                t = fh.read()
            out = {"oid": oid, "status": 200, "terminate_ind": tag(t, "TerminateOperationsInd"), "partial_liq_ind": tag(t, "PartialLiquidationInd"),
                   "schedn": parse_schedn(oid, t)}
        else:
            with throttle:
                try:
                    req = urllib.request.Request(u, headers={"User-Agent": UA})
                    buf = b""
                    with urllib.request.urlopen(req, timeout=60) as r:
                        while b"</IRS990>" not in buf and len(buf) < 60_000_000:
                            chunk = r.read(262_144)
                            if not chunk:
                                break
                            buf += chunk
                    t = buf.decode("utf-8", "replace")
                    out = {"oid": oid, "status": 200, "terminate_ind": tag(t, "TerminateOperationsInd"), "partial_liq_ind": tag(t, "PartialLiquidationInd")}
                    if out["terminate_ind"] in YES or out["partial_liq_ind"] in YES:
                        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=120) as r:
                            out["schedn"] = parse_schedn(oid, r.read().decode("utf-8", "replace"))
                except Exception as e:  # noqa: BLE001
                    return {"oid": oid, "status": f"error:{type(e).__name__}"}
        out.update({"ein": next((x["ein"] for x in rets if oid in x["xml_url"]), ""), "url": u})
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(out, fh)
        return out
    urls = sorted({r["xml_url"] for r in rets})
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        mirror = list(ex.map(head_flags, urls))
    found += [{**m["schedn"], "source": "mirror_cf_filer"} for m in mirror if m.get("schedn")]
    flags = [m for m in mirror if m.get("status") == 200 and (m.get("terminate_ind") in YES or m.get("partial_liq_ind") in YES)]
    out = {"local_xml_scanned": len(files), "cf_filer_returns_2021plus": len(rets), "mirror_urls": len(urls),
           "mirror_ok": sum(m.get("status") == 200 for m in mirror), "mirror_errors": [m for m in mirror if m.get("status") != 200],
           "schedn_found": found, "part_iv_31_32_yes": flags}
    with open(os.path.join(cache_dir, "schedn.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    return {k: (len(v) if isinstance(v, list) else v) for k, v in out.items()}


def schedn_cf_rows(cache_dir: str) -> list[dict]:
    p = os.path.join(cache_dir, "schedn.json")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as fh:
        d = json.load(fh)
    cf_eins = {r["ein"]: r["name"] for r in read_csv(CF_MAP)}
    rows, seen = [], set()
    for s in d["schedn_found"]:
        filer_cf = s["filer_ein"] in cf_eins or bool(CF_NAME_RE.search(s["filer_name"]))
        for x in s["details"]:
            rec_cf = x["recipient_ein"] in cf_eins or bool(CF_NAME_RE.search(x["recipient"]))
            if not (filer_cf or rec_cf) or num(s["tax_year"]) < 2021:
                continue
            key = (s["filer_ein"], s["tax_year"], x["recipient"], x["fmv"])
            if key in seen:
                continue
            seen.add(key)
            rows.append({"event_type": f"schedule_n_{x['part']}", "party_a": f"{s['filer_name']} (EIN {s['filer_ein']})",
                         "party_b": f"{x['recipient']}" + (f" (EIN {x['recipient_ein']})" if x["recipient_ein"] else ""),
                         "date": x["date"] or s["tax_period_end"], "year": (x["date"] or s["tax_period_end"])[:4],
                         "daf_or_asset_usd_moved": x["fmv"], "asset_basis": "Schedule N FMV of assets distributed (all assets, not DAF-only)",
                         "description": x["desc"], "geography": "", "cf_role": "filer_is_cf" if filer_cf else "recipient_is_cf",
                         "source_url": f"https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{s['object_id']}_public.xml",
                         "source_type": "irs_990_schedule_n", "confidence": "high_filed", "notes": f"tax year {s['tax_year']}"})
    return rows


# ---------------------------------------------------------------- consolidation events (transcribed)
CONSOL_FIELDS = ("event_id", "event_type", "party_a", "party_b", "date", "year", "daf_or_asset_usd_moved", "asset_basis", "description",
                 "geography", "cf_role", "source_url", "source_type", "confidence", "notes")


def task_consol(cache_dir: str) -> dict:
    ev = [dict(e) for e in CONSOLIDATION_EVENTS]
    sn = schedn_cf_rows(cache_dir)
    rows = [{**r, "event_id": f"C{i + 1:03d}"} for i, r in enumerate(ev + sn)]
    write_csv(OUT_CONSOL, rows, CONSOL_FIELDS)
    return {"events": len(ev), "schedule_n_rows": len(sn), "by_type": dict(collections.Counter(r["event_type"] for r in rows)),
            "by_year": dict(sorted(collections.Counter(r["year"] for r in rows).items()))}


from mission_cf_fee_data import FEE_DATA, CONSOLIDATION_EVENTS, NATIONAL_COMPARATORS  # noqa: E402  (transcribed constants, same directory)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=("crawl", "urls", "census", "schedn", "consol"))
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--xml-dir", action="append", default=[])
    ap.add_argument("--only", default="", help="comma-separated EINs (crawl)")
    ap.add_argument("--url-file", default="", help="file with one URL per line (urls task)")
    a = ap.parse_args()
    out = {"crawl": lambda: task_crawl(a.cache_dir, a.fetch, a.workers, frozenset(filter(None, a.only.split(",")))),
           "urls": lambda: task_urls(a.cache_dir, a.fetch, [ln.strip() for ln in open(a.url_file) if ln.strip() and not ln.startswith("#")], a.workers),
           "census": lambda: task_census(a.cache_dir),
           "schedn": lambda: task_schedn(a.cache_dir, a.xml_dir, a.fetch, a.workers),
           "consol": lambda: task_consol(a.cache_dir)}[a.task]()
    print(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
