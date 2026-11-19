#!/usr/bin/env python3
"""P-B45N33-01: published DAF fee census of a stratified random sample of the long tail (sponsors under $50m).

Stdlib only; functional style (pure transforms; I/O only at the edges: CSV read/write, the optional fetch task).

Tasks
  sample   Draw the stratified random sample (fixed seed) from the 1,240 FY2024 tail sponsors and print it.
  fetch    For every source URL in FEES (below): read robots.txt on the host first (generic user agent
           "research-script/1.0"), log the verdict, and fetch the page only if allowed; PDFs are converted with
           pdftotext. Results are cached in --cache-dir (outside the repository). Needs --fetch to touch the network.
  census   Verify each transcribed quote against the cached text of its source (whitespace-normalised, case-
           insensitive), compute the effective annual admin fee at $25k / $100k / $500k, join the allocated operating
           cost (rules A, G, AM) from long-tail-operating-cost-2026-11-19.csv, write the census CSV and print every
           summary table used in research/mission-2026-11-14/b45n33-01-long-tail-fee-census.md.

Sampling
  Frame: daf-long-tail-sponsors-fy2021-2024.csv rows with size_band_fy2024 in t10_50, t1_10, t0_1, zero (1,240).
  Type (4): community_foundation -> cf; single_issue_other -> single_issue; religious -> faith;
            university_or_hospital, national_standard, donation_processor -> other.
  Strata: type x size band (16 cells, all non-empty). Allocation of n = 60: proportional to stratum size, largest-
  remainder rounding, floor of 1 per stratum. Within a stratum: random.Random(SEED + stratum index).sample() over the
  stratum's rows sorted by EIN, so the draw is reproducible and independent of file order.

Fee computation
  Effective annual admin fee at a constant balance B: tiers ((lower, upper|None, rate_pct), ...) applied 'marginal'
  (each rate on its slice) or 'flat_on_total' (the rate of B's tier on all of B); then max(fee, minimum annual fee)
  plus any flat annual fee. Gift and grant fees are recorded but are not in the effective annual fee (they depend on
  activity); a separate column adds a stated grant/gift percentage at an assumed 10% annual turnover only where the
  schedule has no balance-based fee. bps = fee / B x 1e4.

Usage
  python3 scripts/mission_long_tail_fee_census.py . --task sample
  python3 scripts/mission_long_tail_fee_census.py . --task fetch --cache-dir CACHE --fetch
  python3 scripts/mission_long_tail_fee_census.py . --task census --cache-dir CACHE
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import functools
import html
import json
import math
import os
import random
import re
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from functools import reduce
from typing import Iterable, Mapping, Sequence

DATA = "data/mission-2026-11-14"
LT_CSV = f"{DATA}/daf-long-tail-sponsors-fy2021-2024.csv"
COST_CSV = f"{DATA}/long-tail-operating-cost-2026-11-19.csv"
TOP100_CSV = f"{DATA}/cf-daf-fee-census-2026.csv"
REFRESH_CSV = f"{DATA}/cf-daf-fee-census-refresh-2026-11-19.csv"
OUT_CSV = f"{DATA}/long-tail-fee-census-2026-11-19.csv"
TAIL_BANDS = ("t10_50", "t1_10", "t0_1", "zero")
TYPE_OF = {
    "community_foundation": "cf",
    "single_issue_other": "single_issue",
    "religious": "faith",
    "university_or_hospital": "other",
    "national_standard": "other",
    "donation_processor": "other",
}
TYPES = ("cf", "single_issue", "faith", "other")
SEED = 20261119
N_SAMPLE = 60
BALANCES = (25_000, 100_000, 500_000)
UA = "research-script/1.0"
RETRIEVED = "2026-11-19"
TURNOVER = 0.10  # assumed share of balance granted out a year, used only for grant-fee-only schedules

# ----------------------------------------------------------------------------- transcription (filled after research)
# Keyed by EIN. status: published_schedule | partial | no_published_fee | no_website_found
# For published/partial: tiers, basis, min_fee, flat_fee, opening_min, gift_fee, grant_fee, grant_fee_pct,
# investment, source_url, source_date, quotes (verbatim strings that must occur in the cached source text).
FEES: dict[str, dict] = {}

# Official homepages: CFs from cf-vendor-map-by-ein-v2.csv (990 WebsiteAddressTxt); others from the FY2024 990
# WebsiteAddressTxt in the GivingTuesday mirror, or from a web search where the 990 gives none (noted in FEES).
SITES: dict[str, str] = {
    "911726410": "https://www.whatcomcf.org/",
    "481076910": "https://www.hutchcf.org/",
    "751709180": "https://www.cfwtx.org/",
    "521326014": "https://www.cfes.org/",
    "752817894": "https://www.wfacf.org/",
    "841339670": "https://www.ppcf.org/",
    "593182886": "https://www.cffound.org/",
    "311760702": "https://www.thelcfoundation.org/",
    "043401997": "https://www.glcfoundation.org/",
    "341713261": "https://www.community-foundation.com/",
    "680330462": "https://www.communityfound.org/",
    "920139183": "https://www.homerfoundation.org/",
    "510173092": "https://fourwaycommunityfoundation.org/",
    "383179612": "https://www.micf.org/",
    "351859959": "https://www.madisonccf.org/",
    "311140087": "https://clintoncountyohiofoundation.org/",
    "593343026": "https://www.cfslc.org/",
    "266394395": "https://atccf.org/",
    "611304905": "https://www.cfwestky.org/",
    "311040215": "https://www.athensfoundation.org/",
    "300752563": "https://spccf.org/",
    "390827885": "https://www.cfcwi.org/",
    "351870979": "https://dccfound.org/",
    "841374928": "https://www.grandfoundation.com/",
    "351842404": "https://www.jaspernewtonfoundation.org/",
    "382236628": "https://cfmonroe.org/",
    "421495980": "https://givinggreater.org/",
    "251881899": "https://www.cfgcpa.org/",
    "421285187": "https://clarindafoundation.com/",
    "237410312": "https://www.capecoralcf.org/",
    "951644609": "https://www.eifoundation.org/",
    "911325007": "https://pridefoundation.org/",
    "270388708": "https://www.greenwoodcf.org/",
    "752675978": "https://www.bsafoundation.org/",
    "042104847": "https://www.williams.edu/",
    "131624046": "https://www.iie.org/",
    "020459470": "https://www.manchesterpal.org/",
    "472525808": "https://www.globaltrustfunds.org/",
    "381359193": "https://www.unitedforscmi.org/",
    "132992977": "https://www.astraeafoundation.org/",
    "920146538": "https://www.bcsfoundation.org/",
    "930395586": "https://www.unitedwaymwv.org/",
    "050259003": "https://www.jewishallianceri.org/",
    "822189237": "https://www.jewishyoungstown.org/",
    "453969752": "https://christianaidministries.org/biblical-stewardship-services/",  # web search; 990 lists none
    "204595721": "https://www.ccfmm.org/",
    "720779104": "https://umf.org/",
    "042104351": "https://www.jccns.org/",
    "510159835": "https://www.jewishdesmoines.org/",
    "486088461": "https://www.emporia.edu/foundation-giving/",
    "133219917": "https://www.sunyorangefoundation.org/",
    "362182171": "https://www.wheaton.edu/",
    "351635296": "https://johnsonmemorialfoundation.org/",
    "832300241": "https://www.cpp.edu/philanthropy/",
    "200385860": "https://www.cmafohio.org/",
    "590974739": "https://www.uff.ufl.edu/",
}

FEE_LINK = re.compile(r"(?i)fee|donor.?advised|\bdaf\b|fund.?(type|option|polic|agreement|guideline)|polic|"
                      r"open.?a.?fund|start.?a.?fund|create.?a.?fund|ways.?to.?give|giving.?option|types.?of.?funds|"
                      r"advisor|professional|\.pdf$")
FEE_SENT = re.compile(r"(?i)(administrative|admin|management|service|annual)\s+fee|\bfees?\b.{0,60}(%|percent|basis points)|"
                      r"minimum.{0,40}\$\s?[\d,]+|\$\s?[\d,]+.{0,40}(to open|to establish|minimum)|"
                      r"(%|percent).{0,60}(of the fund|balance|market value|assets|per year|annually|of grants|of gifts)")


# ----------------------------------------------------------------------------- pure helpers
def num(x) -> float | None:
    try:
        v = float(str(x).replace(",", "").replace("$", "").strip())
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def fmt(v, nd: int = 1) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


# ----------------------------------------------------------------------------- sampling
def tail_frame(lt_rows: Iterable[Mapping]) -> tuple[dict, ...]:
    return tuple(
        {**r, "type4": TYPE_OF[r["sponsor_category"]]}
        for r in lt_rows
        if r["size_band_fy2024"] in TAIL_BANDS
    )


def strata(frame: Sequence[Mapping]) -> tuple[tuple[tuple[str, str], tuple[dict, ...]], ...]:
    keys = tuple((t, b) for t in TYPES for b in TAIL_BANDS)
    return tuple(
        (k, tuple(sorted((r for r in frame if (r["type4"], r["size_band_fy2024"]) == k), key=lambda r: r["ein"])))
        for k in keys
    )


def allocate(sizes: Sequence[int], n: int) -> tuple[int, ...]:
    """Proportional allocation, floor 1 per non-empty stratum, largest remainder for the rest."""
    total = sum(sizes)
    base = tuple(max(1, math.floor(n * s / total)) if s else 0 for s in sizes)
    rem = n - sum(base)
    order = sorted(range(len(sizes)), key=lambda i: (-(n * sizes[i] / total - math.floor(n * sizes[i] / total)), i))
    bump = frozenset(order[:max(0, rem)])
    return tuple(min(sizes[i], base[i] + (1 if i in bump else 0)) for i in range(len(sizes)))


def draw(frame: Sequence[Mapping], n: int = N_SAMPLE, seed: int = SEED) -> tuple[dict, ...]:
    st = strata(frame)
    alloc = allocate(tuple(len(rows) for _, rows in st), n)
    return tuple(
        {**r, "stratum": f"{k[0]}|{k[1]}", "stratum_N": len(rows), "stratum_n": a, "weight": len(rows) / a}
        for i, ((k, rows), a) in enumerate(zip(st, alloc))
        for r in random.Random(seed + i).sample(rows, a)
    )


# ----------------------------------------------------------------------------- fee engine
def effective_admin_fee(s: Mapping, balance: float) -> float | None:
    tiers = s.get("tiers") or ()
    if not tiers and not s.get("flat_fee") and not s.get("min_fee"):
        return None
    if s.get("basis", "marginal") == "marginal":
        fee = sum(max(0.0, min(balance, up if up is not None else balance) - lo) * r / 100 for lo, up, r in tiers)
    else:
        fee = balance * next((r for lo, up, r in tiers if balance >= lo and (up is None or balance < up)),
                             tiers[-1][2] if tiers else 0) / 100
    return round(max(fee, s.get("min_fee") or 0) + (s.get("flat_fee") or 0), 2)


def bps(fee: float | None, balance: float) -> float | None:
    return None if fee is None else round(fee / balance * 1e4, 1)


def activity_fee_bps(s: Mapping) -> float | None:
    """Grant-fee-only schedules: stated % of grants x assumed turnover, in bps of balance."""
    p = s.get("grant_fee_pct")
    return None if p is None or s.get("tiers") else round(p / 100 * TURNOVER * 1e4, 1)


# ----------------------------------------------------------------------------- statistics
def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float, float] | None:
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def quantiles(xs: Sequence[float]) -> tuple[float, float, float] | None:
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    if len(xs) == 1:
        return xs[0], xs[0], xs[0]
    q = statistics.quantiles(xs, n=4, method="inclusive")
    return q[0], statistics.median(xs), q[2]


def qfmt(xs: Sequence[float], nd: int = 0) -> str:
    q = quantiles(xs)
    n = len([x for x in xs if x is not None])
    return "–" if q is None else f"{q[1]:,.{nd}f} ({q[0]:,.{nd}f}–{q[2]:,.{nd}f}; n={n})"


# ----------------------------------------------------------------------------- network edge (fetch task only)
def cache_key(url: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", url)[:180]


def http_get(url: str, timeout: int = 30) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read(10_000_000)
    except urllib.error.HTTPError as e:
        return e.code, "", b""
    except Exception as e:  # noqa: BLE001 - network edge
        return -1, type(e).__name__, b""


@functools.lru_cache(maxsize=None)
def robots_file(origin: str) -> tuple[int, bytes]:
    code, _, body = http_get(f"{origin}/robots.txt", timeout=20)
    return code, body


def robots_verdict(url: str) -> tuple[str, bool]:
    p = urllib.parse.urlsplit(url)
    code, body = robots_file(f"{p.scheme}://{p.netloc}")
    if code in (401, 403):
        return f"robots.txt {code}: treated as disallowed", False
    if code != 200:
        return f"robots.txt {code}: none published, fetch allowed", True
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(body.decode("utf-8", "ignore").splitlines())
    ok = rp.can_fetch(UA, url)
    return f"robots.txt 200: {'allowed' if ok else 'disallowed'} for {UA}", ok


def to_text(ctype: str, body: bytes) -> str:
    if body[:4] == b"%PDF" or "pdf" in ctype:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(body)
            f.flush()
            r = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, text=True)
            return r.stdout
    t = body.decode("utf-8", "ignore")
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
    return html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))


def fetch_one(cache: str, url: str) -> dict:
    path = os.path.join(cache, cache_key(url) + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    verdict, ok = robots_verdict(url)
    time.sleep(1)
    code, ctype, body = http_get(url) if ok else (None, "", b"")
    rec = {"url": url, "robots": verdict, "allowed": ok, "status": code, "ctype": ctype,
           "text": to_text(ctype, body) if body else "", "retrieved": RETRIEVED}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh)
    return rec


def cached(cache: str, url: str) -> dict | None:
    path = os.path.join(cache, cache_key(url) + ".json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'").replace(" ", " ")).strip().lower()


def verify(cache: str, s: Mapping) -> str:
    quotes = s.get("quotes") or ()
    if not quotes:
        return "no quotes"
    recs = [cached(cache, u) for u in s.get("verify_urls") or (s.get("source_url"),)]
    text = norm(" ".join(r["text"] for r in recs if r))
    if not text:
        return "source not cached (robots or fetch failure)"
    hits = sum(1 for q in quotes if norm(q) in text)
    return f"verified {hits}/{len(quotes)}"


def links(page_html: str, base: str) -> tuple[str, ...]:
    hrefs = re.findall(r"""(?i)href\s*=\s*["']([^"'#]+)""", page_html or "")
    return tuple(dict.fromkeys(urllib.parse.urljoin(base, html.unescape(h)) for h in hrefs))


def same_site(url: str, home: str) -> bool:
    strip = lambda h: re.sub(r"^www\.", "", h.lower())  # noqa: E731
    return strip(urllib.parse.urlsplit(url).netloc) == strip(urllib.parse.urlsplit(home).netloc)


def raw_get(cache: str, url: str) -> dict:
    """Like fetch_one, but keeps the raw HTML too (for link discovery)."""
    path = os.path.join(cache, "raw_" + cache_key(url) + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    verdict, ok = robots_verdict(url)
    time.sleep(1)
    code, ctype, body = http_get(url) if ok else (None, "", b"")
    is_pdf = body[:4] == b"%PDF" or "pdf" in ctype
    rec = {"url": url, "robots": verdict, "allowed": ok, "status": code, "ctype": ctype,
           "html": "" if is_pdf else body.decode("utf-8", "ignore"), "text": to_text(ctype, body) if body else ""}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh)
    return rec


def fee_sentences(text: str) -> tuple[str, ...]:
    parts = re.split(r"(?<=[.;:!?])\s+|\n{2,}", re.sub(r"[ \t]+", " ", text))
    return tuple(dict.fromkeys(p.strip()[:400] for p in parts if FEE_SENT.search(p)))


FEE_TEXT = re.compile(r"(?i)\bfees?\b|minimum|schedule|donor.?advised|\bdaf\b|fund (types|options|agreement)|"
                      r"types of funds|policies|guidelines|open a fund|start a fund|create a fund|establish")


def anchors(page_html: str, base: str) -> tuple[tuple[str, str], ...]:
    found = re.findall(r"""(?is)<a\b[^>]*href\s*=\s*["']([^"'#]+)["'][^>]*>(.*?)</a>""", page_html or "")
    return tuple((urllib.parse.urljoin(base, html.unescape(h)), re.sub(r"<[^>]+>|\s+", " ", t).strip()) for h, t in found)


def score(url: str, text: str) -> int:
    u, t = urllib.parse.unquote(url).lower(), text.lower()
    return (6 * bool(re.search(r"\bfees?\b", t)) + 4 * ("fee" in u and "feed" not in u) + 3 * ("donor" in u or "daf" in u)
            + 2 * bool(re.search(r"donor.?advised|minimum|schedule", t)) + u.endswith(".pdf")
            - 8 * bool(re.search(r"feed|privacy|cookie|event|news|post/|blog|story|stories|career|employment", u)))


def candidates(page: Mapping, home: str) -> tuple[tuple[int, str], ...]:
    an = anchors(page.get("html", ""), page["url"])
    return tuple((score(u, t), u) for u, t in an
                 if u.startswith("http") and (same_site(u, home) and (FEE_LINK.search(urllib.parse.unquote(u)) or FEE_TEXT.search(t))
                                              or (FEE_TEXT.search(t) and re.search(r"(?i)\.pdf|drive\.google|/files?/|uploads|ugd", u))))


def crawl_site(cache: str, ein: str, home: str, max_pages: int = 16) -> dict:
    first = raw_get(cache, home)
    sm = raw_get(cache, urllib.parse.urljoin(home, "/sitemap.xml")) if first["allowed"] else {"html": ""}
    sm_locs = tuple(u for u in re.findall(r"<loc>\s*([^<\s]+)", sm.get("html") or "") if not u.endswith(".xml"))
    lvl1 = candidates(first, home) + tuple((score(u, ""), u) for u in sm_locs if FEE_LINK.search(urllib.parse.unquote(u)))
    top1 = tuple(dict.fromkeys(u for sc, u in sorted(lvl1, key=lambda x: (-x[0], x[1])) if sc >= 0))[:10]
    pages1 = tuple(raw_get(cache, u) for u in top1)
    lvl2 = tuple(c for p in pages1 for c in candidates(p, home) if c[1] not in top1 and c[1] != home)
    top2 = tuple(dict.fromkeys(u for sc, u in sorted(lvl2, key=lambda x: (-x[0], x[1])) if sc >= 0))[:max_pages - len(top1)]
    pages = pages1 + tuple(raw_get(cache, u) for u in top2)
    hits = tuple((p["url"], sn) for p in (first,) + pages for sn in fee_sentences(p.get("text", "")))
    return {"ein": ein, "home": home, "robots": first["robots"], "home_status": first["status"],
            "n_candidates": len(lvl1) + len(lvl2), "fetched": [p["url"] for p in pages], "hits": hits}


# ----------------------------------------------------------------------------- census rows
def census_row(r: Mapping, cost: Mapping, cache: str | None) -> dict:
    s = FEES.get(r["ein"], {"status": "not_researched"})
    fees = {b: effective_admin_fee(s, b) for b in BALANCES} if s["status"] in ("published_schedule", "partial") else {}
    rec = cached(cache, s["source_url"]) if cache and s.get("source_url") else None
    out = {
        "ein": r["ein"], "name": r["name"], "type4": r["type4"], "sponsor_category": r["sponsor_category"],
        "size_band_fy2024": r["size_band_fy2024"], "stratum": r["stratum"], "stratum_N": r["stratum_N"],
        "stratum_n": r["stratum_n"], "weight": fmt(r["weight"], 3),
        "daf_assets_fy2024": r["daf_assets_fy2024"], "accounts_fy2024_screened": r["accounts_fy2024_screened"],
        "avg_account_fy2024": r["avg_account_fy2024"],
        "website": s.get("website", ""), "fee_status": s["status"],
        "fee_basis": s.get("basis", "") if s.get("tiers") else "",
        "admin_tiers": "; ".join(f"{lo:,.0f}-{'' if up is None else f'{up:,.0f}'}: {rt}%" for lo, up, rt in s.get("tiers") or ()),
        "min_annual_fee_usd": fmt(s.get("min_fee")), "flat_annual_fee_usd": fmt(s.get("flat_fee")),
        "opening_min_usd": fmt(s.get("opening_min")), "gift_fee": s.get("gift_fee", ""),
        "grant_fee": s.get("grant_fee", ""), "investment": s.get("investment", ""),
        "source_url": s.get("source_url", ""), "source_date": s.get("source_date", ""),
        "robots": (rec or {}).get("robots", s.get("robots", "")), "quote_check": verify(cache, s) if cache and s.get("quotes") else "",
        "notes": s.get("notes", ""),
    }
    fee_cols = {f"admin_fee_usd_{b // 1000}k": fmt(fees.get(b), 0) for b in BALANCES}
    bps_cols = {f"admin_bps_{b // 1000}k": fmt(bps(fees.get(b), b)) for b in BALANCES}
    act = activity_fee_bps(s) if s["status"] in ("published_schedule", "partial") else None
    cost_cols = {
        "usable_cost": cost.get("usable", ""),
        "cost_bps_alloc_A": cost.get("daf_cost_bps_daf_assets_alloc_A", ""),
        "cost_bps_alloc_G": cost.get("daf_cost_bps_daf_assets_alloc_G", ""),
        "cost_bps_alloc_AM": cost.get("daf_cost_bps_daf_assets_alloc_AM", ""),
        "cost_per_account_alloc_A": cost.get("daf_cost_per_account_alloc_A", ""),
        "cost_per_account_alloc_G": cost.get("daf_cost_per_account_alloc_G", ""),
        "cost_per_account_alloc_AM": cost.get("daf_cost_per_account_alloc_AM", ""),
    }
    fee_at_avg = fee_at_balance(s, num(r["avg_account_fy2024"])) if fees else None
    cover = {
        "fee_usd_at_avg_account": fmt(fee_at_avg, 0),
        "fee_bps_at_avg_account": fmt(bps(fee_at_avg, num(r["avg_account_fy2024"])) if fee_at_avg is not None else None),
        **{f"covers_alloc_{k}": coverage(fee_at_avg, num(cost_cols[f"cost_per_account_alloc_{k}"])) for k in ("A", "G", "AM")},
        **{f"coverage_ratio_alloc_{k}": fmt(ratio(fee_at_avg, num(cost_cols[f"cost_per_account_alloc_{k}"])), 2)
           for k in ("A", "G", "AM")},
    }
    return {**out, **fee_cols, **bps_cols, "activity_fee_bps_at_10pct_turnover": fmt(act), **cost_cols, **cover}


def fee_at_balance(s: Mapping, bal: float | None) -> float | None:
    return None if not bal else effective_admin_fee(s, bal)


def ratio(a, b) -> float | None:
    return a / b if a is not None and b else None


def coverage(fee: float | None, cost: float | None) -> str:
    return "" if fee is None or not cost else ("yes" if fee >= cost else "no")


FIELDS = (
    "ein", "name", "type4", "sponsor_category", "size_band_fy2024", "stratum", "stratum_N", "stratum_n", "weight",
    "daf_assets_fy2024", "accounts_fy2024_screened", "avg_account_fy2024", "website", "fee_status", "fee_basis",
    "admin_tiers", "min_annual_fee_usd", "flat_annual_fee_usd", "opening_min_usd", "gift_fee", "grant_fee",
    "investment", "admin_fee_usd_25k", "admin_fee_usd_100k", "admin_fee_usd_500k", "admin_bps_25k",
    "admin_bps_100k", "admin_bps_500k", "activity_fee_bps_at_10pct_turnover", "usable_cost", "cost_bps_alloc_A",
    "cost_bps_alloc_G", "cost_bps_alloc_AM", "cost_per_account_alloc_A", "cost_per_account_alloc_G",
    "cost_per_account_alloc_AM", "fee_usd_at_avg_account", "fee_bps_at_avg_account", "covers_alloc_A",
    "covers_alloc_G", "covers_alloc_AM", "coverage_ratio_alloc_A", "coverage_ratio_alloc_G",
    "coverage_ratio_alloc_AM", "source_url", "source_date", "robots", "quote_check", "notes",
)


# ----------------------------------------------------------------------------- report (pure: rows -> markdown)
PUBLISHED = ("published_schedule", "partial")


def is_pub(r: Mapping) -> bool:
    return r["fee_status"] in PUBLISHED


def has_rate(r: Mapping) -> bool:
    return is_pub(r) and r["admin_bps_100k"] != ""


def pct(t) -> str:
    return "–" if t is None else f"{t[0]*100:.1f}% (95% Wilson {t[1]*100:.1f}–{t[2]*100:.1f}%)"


def weighted_share(rows: Sequence[Mapping], pred) -> float | None:
    w = sum(num(r["weight"]) for r in rows)
    return None if not w else sum(num(r["weight"]) for r in rows if pred(r)) / w


def table(head: Sequence[str], body: Iterable[Sequence]) -> str:
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] +
                      ["| " + " | ".join(str(c) for c in b) + " |" for b in body])


def report(rows: Sequence[Mapping], top100: Sequence[Mapping], frame: Sequence[Mapping]) -> str:
    groups = (("All sampled", rows),) + tuple((t, tuple(r for r in rows if r["type4"] == t)) for t in TYPES) + \
             tuple((f"band {b}", tuple(r for r in rows if r["size_band_fy2024"] == b)) for b in TAIL_BANDS)
    design = table(("Stratum", "Frame N", "Sample n", "Weight"),
                   ((k, sum(1 for f in frame if f"{f['type4']}|{f['size_band_fy2024']}" == k),
                     sum(1 for r in rows if r["stratum"] == k),
                     next((r["weight"] for r in rows if r["stratum"] == k), "")) for k in dict.fromkeys(r["stratum"] for r in rows)))
    status = table(("Group", "n", "published or partial", "with a balance-based rate", "no published fee",
                    "no website found"),
                   ((g, len(rs), sum(map(is_pub, rs)), sum(map(has_rate, rs)),
                     sum(r["fee_status"] == "no_published_fee" for r in rs),
                     sum(r["fee_status"] == "no_website_found" for r in rs)) for g, rs in groups))
    rate = table(("Group", "Published (any fee term)", "Published balance-based admin rate", "Design-weighted, any term"),
                 ((g, pct(wilson(sum(map(is_pub, rs)), len(rs))), pct(wilson(sum(map(has_rate, rs)), len(rs))),
                   fmt((weighted_share(rs, is_pub) or 0) * 100) + "%") for g, rs in groups))
    pub = tuple(r for r in rows if has_rate(r))
    fee_groups = (("All with a rate", pub), ("CFs", tuple(r for r in pub if r["type4"] == "cf")),
                  ("Non-CF", tuple(r for r in pub if r["type4"] != "cf")))
    fees = table(("Group", "$25k bps", "$100k bps", "$500k bps", "Min annual fee $", "Opening minimum $"),
                 ((g, qfmt([num(r["admin_bps_25k"]) for r in rs]), qfmt([num(r["admin_bps_100k"]) for r in rs]),
                   qfmt([num(r["admin_bps_500k"]) for r in rs]), qfmt([num(r["min_annual_fee_usd"]) for r in rs]),
                   qfmt([num(r["opening_min_usd"]) for r in rs])) for g, rs in fee_groups))
    t100 = tuple(r for r in top100 if r["status"] == "published_schedule")
    t100_any = tuple(r for r in top100 if r["status"] not in ("national_comparator",))
    t100_pub = sum(r["status"] in ("published_schedule", "published_schedule_pre2021", "partial", "noninvested_flat",
                                   "grant_or_gift_based") for r in t100_any)
    tail_cf = tuple(r for r in rows if r["type4"] == "cf")
    comp = table(("Measure", "Tail sample, CFs", "Top-100 CF census (cf-daf-fee-census-2026.csv)"),
                 (("Any fee term published", pct(wilson(sum(map(is_pub, tail_cf)), len(tail_cf))),
                   pct(wilson(t100_pub, len(t100_any))) + " incl. pre-2021 and partial"),
                  ("2021+ balance-based schedule", pct(wilson(sum(map(has_rate, tail_cf)), len(tail_cf))),
                   pct(wilson(len(t100), len(t100_any))) + " (`published_schedule`)"),
                  ("Admin bps at $100k", qfmt([num(r["admin_bps_100k"]) for r in tail_cf if has_rate(r)]),
                   qfmt([num(r["admin_bps_100k"]) for r in t100]) + " (as filed; refreshed doc median 100, n=37)"),
                  ("Min annual fee $", qfmt([num(r["min_annual_fee_usd"]) for r in tail_cf if has_rate(r)]),
                   qfmt([num(r["min_annual_fee_usd"]) for r in t100])),
                  ("Opening minimum $", qfmt([num(r["opening_min_usd"]) for r in tail_cf if is_pub(r)]),
                   qfmt([num(r["min_opening_usd"]) for r in t100]))))
    perr = table(("EIN", "Sponsor", "Type", "Status", "$25k", "$100k", "$500k", "Min fee", "Opening min", "Source date"),
                 ((r["ein"], r["name"], r["type4"], r["fee_status"], r["admin_bps_25k"] or "–", r["admin_bps_100k"] or "–",
                   r["admin_bps_500k"] or "–", r["min_annual_fee_usd"] or "–", r["opening_min_usd"] or "–",
                   r["source_date"] or "–") for r in rows if is_pub(r)))
    cov_rows = tuple(r for r in rows if r["fee_usd_at_avg_account"] != "")
    cov = table(("Rule", "n with fee and cost", "Fee >= allocated cost", "Median fee / cost", "IQR"),
                tuple((k, len(rs), f"{sum(r[f'covers_alloc_{k}'] == 'yes' for r in rs)} of {len(rs)}",
                       fmt((quantiles([num(r[f'coverage_ratio_alloc_{k}']) for r in rs]) or (None, None, None))[1], 2),
                       "–" if not rs else "{:.2f}–{:.2f}".format(*(quantiles([num(r[f'coverage_ratio_alloc_{k}']) for r in rs])[0::2])))
                      for k in ("A", "G", "AM")
                      for rs in (tuple(r for r in cov_rows if r[f"covers_alloc_{k}"] != ""),)))
    cov_detail = table(("EIN", "Sponsor", "Avg account $", "Fee at avg $", "Fee bps", "Cost bps A", "Cost bps G",
                        "Cost bps AM", "Cost/acct A $", "Cost/acct G $", "Cost/acct AM $", "Covers A/G/AM"),
                       ((r["ein"], r["name"], fmt(num(r["avg_account_fy2024"]), 0), r["fee_usd_at_avg_account"],
                         r["fee_bps_at_avg_account"], fmt(num(r["cost_bps_alloc_A"])), fmt(num(r["cost_bps_alloc_G"])),
                         fmt(num(r["cost_bps_alloc_AM"])), fmt(num(r["cost_per_account_alloc_A"]), 0),
                         fmt(num(r["cost_per_account_alloc_G"]), 0), fmt(num(r["cost_per_account_alloc_AM"]), 0),
                         "/".join(r[f"covers_alloc_{k}"] or "–" for k in ("A", "G", "AM"))) for r in cov_rows))
    unpub_cost = table(("Group", "Rule A bps", "Rule G bps", "AM bps"),
                       ((g, qfmt([num(r["cost_bps_alloc_A"]) for r in rs]), qfmt([num(r["cost_bps_alloc_G"]) for r in rs]),
                         qfmt([num(r["cost_bps_alloc_AM"]) for r in rs]))
                        for g, rs in (("Publishers (rate)", pub), ("Non-publishers", tuple(r for r in rows if not is_pub(r))))))
    return "\n\n".join((
        "## T1 Sample design", design, "## T2 Fee status by group", status,
        "## T3 Publication rate (Wilson 95%)", rate, "## T4 Effective annual admin fee, bps (median (p25-p75; n))", fees,
        "## T5 Tail CFs vs top-100 CF census", comp, "## T6 Per-sponsor published fees", perr,
        "## T7 Fee at the sponsor's own average account vs allocated cost per account", cov, cov_detail,
        "## T8 Allocated cost, publishers vs non-publishers", unpub_cost))


# ----------------------------------------------------------------------------- tasks
def task_sample(sample: Sequence[Mapping]) -> str:
    lines = ["stratum|stratum_N|stratum_n|ein|name|daf_assets_fy2024"]
    return "\n".join(lines + [f"{r['stratum']}|{r['stratum_N']}|{r['stratum_n']}|{r['ein']}|{r['name']}|{r['daf_assets_fy2024']}"
                              for r in sample])


def all_urls() -> tuple[str, ...]:
    return tuple(dict.fromkeys(u for s in FEES.values() for u in (s.get("verify_urls") or (s.get("source_url"),)) if u))


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--task", choices=("sample", "crawl", "fetch", "census"), required=True)
    ap.add_argument("--cache-dir")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--url", action="append", default=[])
    a = ap.parse_args(argv)
    os.chdir(a.root)
    sample = draw(tail_frame(read_csv(LT_CSV)))
    if a.task == "sample":
        print(task_sample(sample))
        return 0
    if a.task == "crawl":
        os.makedirs(a.cache_dir, exist_ok=True)
        targets = [(e, SITES[e]) for e in (a.url or [r["ein"] for r in sample]) if SITES.get(e)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            res = list(ex.map(lambda t: crawl_site(a.cache_dir, *t), targets))
        with open(os.path.join(a.cache_dir, "crawl_summary.json"), "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("\n".join(f"{r['ein']}\t{r['home_status']}\t{r['robots']}\t{r['n_candidates']}\t{len(r['hits'])}" for r in res))
        return 0
    if a.task == "fetch":
        if not (a.fetch and a.cache_dir):
            print("fetch needs --fetch and --cache-dir", file=sys.stderr)
            return 2
        os.makedirs(a.cache_dir, exist_ok=True)
        recs = [fetch_one(a.cache_dir, u) for u in (a.url or all_urls())]
        print("\n".join(f"{r['status']}\t{r['robots']}\t{len(r['text'])}\t{r['url']}" for r in recs))
        return 0
    cost = {r["ein"]: r for r in read_csv(COST_CSV)}
    rows = tuple(census_row(r, cost.get(r["ein"], {}), a.cache_dir) for r in sample)
    write_csv(OUT_CSV, rows, FIELDS)
    print(report(rows, read_csv(TOP100_CSV), tail_frame(read_csv(LT_CSV))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
