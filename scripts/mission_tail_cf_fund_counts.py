#!/usr/bin/env python3
"""P-B45N33-02-01: fund-count denominators for tail community foundations, and allocation rule F. Task id b45n33-02-01.

Stdlib only; functional style (pure transforms; I/O only at the edges: CSV read/write and the network tasks, which
need --fetch). Imports scripts/mission_long_tail_fee_census.py (b45n33-01) for helpers (read_csv, write_csv, num,
quantiles, http_get, to_text, cache_key, anchors, same_site) and does NOT modify it. The robots check is stricter than
the base one (see robots_verdict below).

Sampling
  Frame: the 641 tail CFs of long-tail-operating-cost-2026-11-19.csv (group == tail_cf; = sponsor_category
  community_foundation with size_band_fy2024 in t10_50, t1_10, t0_1, zero of daf-long-tail-sponsors-fy2021-2024.csv).
  Strata (assets band of corrected FY2024 DAF assets): s0 = t10_50 ($10-50m, N 207), s1 = t1_10 ($1-10m, N 272),
  s2 = t0_1 + zero (<$1m, N 162, as in the cost note's 'under $1m' band). n = 20 per stratum.
  Within stratum i: random.Random(SEED + i).sample(stratum rows sorted by EIN, 20), SEED = 20261120201 (task 02-01).
  Homepages: cf-vendor-map-by-ein-v2.csv `homepage` (990 WebsiteAddressTxt), as in the earlier tail samples.

Robots (hard rule) and terms
  For every host, robots.txt is read once and parsed for EACH of: research-script/1.0, ClaudeBot, anthropic-ai,
  Claude-User, Claude-Web, Claude-SearchBot. A URL is fetched only if ALL of them may fetch it (so a ClaudeBot or
  anthropic-ai disallow binds even where '*' allows). robots.txt 401/403 = disallowed; other non-200 = no rules.
  Hosts listed in OFF_LIMITS are never touched. Every verdict is logged to <cache>/robots_log.tsv.
  Terms: if the homepage links a terms-of-use page, it is read (robots permitting) before any other page; if it
  forbids automated extraction (TERMS_RX), crawling of that site stops and the site is logged as terms_blocked.
  User agent "research-script/1.0". No logins, no forms (GET only, no query strings built).

Counts are recorded only as numbers; no donor or fund names are written anywhere (the CSV holds counts, URLs and
short quotes that contain no names; directory pages are counted, not transcribed).

Tasks
  sample   print the draw.
  schedd   fetch the FY2024 990 XML (return_object_id from the cost file) from the GivingTuesday mirror and extract
           Schedule D Part I line 1 counts: DonorAdvisedFundsHeldCnt (col a) and FundsAndOtherAccountsHeldCnt (col b).
  crawl    robots-checked crawl of each homepage for annual reports, fund directories, audits and fund-type pages.
  fetch    fetch extra URLs (--url, robots-checked) into the cache.
  hits     print every sentence with a number next to 'fund(s)' found in the cache, per sponsor (for transcription).
  robots   print the robots log.
  build    verify transcribed quotes against the cache, compute rule F, write
           data/mission-2026-11-14/tail-cf-fund-counts-2026-11-20.csv and print every table in
           research/mission-2026-11-14/b45n33-02-01-tail-cf-fund-counts.md.

Rule F (allocation by fund count) [inference]
  share_F = min(1, DAF funds / all component funds); DAF cost F = opex_ex_11f x share_F;
  per account = cost F / screened DAF accounts; bps = cost F / corrected DAF assets x 1e4.
  DAF funds: from the same source as the total where it gives a DAF count; else Schedule D col (a) of the return whose
  year is closest to the source (flagged daf_from_sched_d). All funds: the source's stated total, else the sum of the
  type counts it gives (flagged), and only where the source covers all fund types (count_scope == all_funds).

Usage (cache outside the repo):
  python3 -I scripts/mission_tail_cf_fund_counts.py . --task sample
  python3 -I scripts/mission_tail_cf_fund_counts.py . --task schedd --cache-dir CACHE --fetch
  python3 -I scripts/mission_tail_cf_fund_counts.py . --task crawl --cache-dir CACHE --fetch
  python3 -I scripts/mission_tail_cf_fund_counts.py . --task build --cache-dir CACHE
"""
from __future__ import annotations

import argparse
import concurrent.futures
import functools
import importlib.util
import json
import os
import random
import re
import statistics
import sys
import time
import urllib.parse
import urllib.robotparser
import xml.etree.ElementTree as ET
from typing import Mapping, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_base():
    spec = importlib.util.spec_from_file_location("lt_fee_census", os.path.join(HERE, "mission_long_tail_fee_census.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = _load_base()
DATA = "data/mission-2026-11-14"
COST_CSV = f"{DATA}/long-tail-operating-cost-2026-11-19.csv"
VMAP_CSV = f"{DATA}/cf-vendor-map-by-ein-v2.csv"
OUT_CSV = f"{DATA}/tail-cf-fund-counts-2026-11-20.csv"
SEED = 20261120201
N_PER = 20
STRATA = (("s0_10_50m", ("t10_50",)), ("s1_1_10m", ("t1_10",)), ("s2_lt1m", ("t0_1", "zero")))
UA = "research-script/1.0"
ROBOT_AGENTS = (UA, "ClaudeBot", "anthropic-ai", "Claude-User", "Claude-Web", "Claude-SearchBot")
OFF_LIMITS = re.compile(r"(?i)(^|\.)fcsuite\.com$|^www\.foundant\.com$|^dev\.foundant\.com$|^help\.foundant\.com$|"
                        r"^secure\.ncfgiving\.com$|^crt\.sh$|certspotter|(^|\.)sec\.gov$")
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
RETRIEVED = "2026-11-20"
N_BOOT = 10_000
BOOT_SEED = 20201
TERMS_RX = re.compile(r"(?i)(scrap(e|ing)|data mining|automated (means|tools|systems|extraction|access|collection)|"
                      r"\brobots?\b|spiders?|crawl(er|ing)|harvest(ing)?)")
TERMS_LINK = re.compile(r"(?i)terms|conditions|legal|disclaimer")
COUNT_LINK = re.compile(r"(?i)annual.?report|impact.?report|report.?to.?the.?community|year.?in.?review|our.?funds|"
                        r"fund.?(directory|list|search|finder|s/?$)|funds?-?(we-?hold|at-|of-)|find.?a.?fund|component|"
                        r"audit|financial|990|scholarship|types.?of.?funds|fund.?types|endowment|annual|report|\.pdf$")
COUNT_SENT = re.compile(r"(?i)\b\d[\d,]*\+?\s+(?:(?:new|active|permanent|endowed|named|charitable|component|individual|"
                        r"different|separate|total|unique|current|non-endowed|other)\s+)*(?:(?:donor[- ]advised|designated|"
                        r"field[- ]of[- ]interest|scholarship|agency|unrestricted|nonprofit|organizational|endowment|"
                        r"memorial|community|charitable)\s+)?funds\b|\b(?:number of|total) (?:[a-z-]+ ){0,3}funds\b[^.]{0,40}\d"
                        r"|\bfunds?\s*(?:held|total|:)\s*\d")


# ----------------------------------------------------------------------------- pure helpers
num = B.num
read_csv = B.read_csv
write_csv = B.write_csv
quantiles = B.quantiles


def frame(cost_rows: Sequence[Mapping]) -> tuple[dict, ...]:
    return tuple(r for r in cost_rows if r["group"] == "tail_cf")


def strata(fr: Sequence[Mapping]) -> tuple[tuple[str, tuple[dict, ...]], ...]:
    return tuple((name, tuple(sorted((r for r in fr if r["size_band_fy2024"] in bands), key=lambda r: r["ein"])))
                 for name, bands in STRATA)


def draw(fr: Sequence[Mapping]) -> tuple[dict, ...]:
    return tuple({**r, "stratum": name, "stratum_N": len(rows), "stratum_n": N_PER, "weight": len(rows) / N_PER}
                 for i, (name, rows) in enumerate(strata(fr))
                 for r in random.Random(SEED + i).sample(rows, N_PER))


def ratio(a, b):
    return None if a is None or b in (None, 0) else a / b


def fmt(v, nd: int = 1) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def qfmt(xs: Sequence, nd: int = 0, pre: str = "") -> str:
    xs = [x for x in xs if x is not None]
    q = quantiles(xs)
    return "–" if q is None else f"{pre}{q[1]:,.{nd}f} ({pre}{q[0]:,.{nd}f}–{pre}{q[2]:,.{nd}f}; n={len(xs)})"


def wmedian(pairs: Sequence[tuple[float, float]]) -> float | None:
    """Weighted median (lower weighted median) of (value, weight) pairs."""
    ps = sorted((v, w) for v, w in pairs if v is not None)
    if not ps:
        return None
    half = sum(w for _, w in ps) / 2
    cum = tuple(sum(w for _, w in ps[:i + 1]) for i in range(len(ps)))
    return next(v for (v, _), c in zip(ps, cum) if c >= half)


def boot_ci(xs: Sequence[float], stat=statistics.median, n: int = N_BOOT, seed: int = BOOT_SEED) -> tuple[float, float] | None:
    xs = [x for x in xs if x is not None]
    if len(xs) < 3:
        return None
    rng = random.Random(seed)
    sims = sorted(stat([xs[rng.randrange(len(xs))] for _ in xs]) for _ in range(n))
    return sims[int(0.025 * n)], sims[int(0.975 * n) - 1]


def table(head: Sequence[str], body) -> str:
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] +
                     ["| " + " | ".join(str(c) for c in row) + " |" for row in body])


# ----------------------------------------------------------------------------- network edge
def log_line(cache: str, line: str) -> None:
    with open(os.path.join(cache, "robots_log.tsv"), "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


@functools.lru_cache(maxsize=None)
def robots_file(origin: str) -> tuple[int, bytes]:
    code, _, body = B.http_get(f"{origin}/robots.txt", timeout=20)
    return code, body


def robots_verdict(url: str) -> tuple[str, bool]:
    p = urllib.parse.urlsplit(url)
    if OFF_LIMITS.search(p.netloc.split(":")[0]):
        return "off-limits host (shared rules): not fetched", False
    code, body = robots_file(f"{p.scheme}://{p.netloc}")
    if code in (401, 403):
        return f"robots.txt {code}: treated as disallowed", False
    if code != 200:
        return f"robots.txt {code}: none published, no rules", True
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(body.decode("utf-8", "ignore").splitlines())
    denied = tuple(a for a in ROBOT_AGENTS if not rp.can_fetch(a, url))
    return (f"robots.txt 200: disallowed for {','.join(denied)}" if denied
            else f"robots.txt 200: allowed for {UA} and all Claude/anthropic agents"), not denied


def get(cache: str, url: str) -> dict:
    path = os.path.join(cache, "p_" + B.cache_key(url) + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    verdict, ok = robots_verdict(url)
    log_line(cache, f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{urllib.parse.urlsplit(url).netloc}\t{verdict}\t{url}")
    time.sleep(1)
    code, ctype, body = B.http_get(url) if ok else (None, "", b"")
    is_pdf = body[:4] == b"%PDF" or "pdf" in ctype
    rec = {"url": url, "robots": verdict, "allowed": ok, "status": code, "ctype": ctype,
           "html": "" if is_pdf else body.decode("utf-8", "ignore"), "text": B.to_text(ctype, body) if body else "",
           "retrieved": RETRIEVED}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rec, fh)
    return rec


def cached(cache: str, url: str) -> dict | None:
    path = os.path.join(cache, "p_" + B.cache_key(url) + ".json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def score(url: str, text: str) -> int:
    u, t = urllib.parse.unquote(url).lower(), text.lower()
    return (6 * bool(re.search(r"annual report|impact report|report to the community|year in review", t))
            + 5 * bool(re.search(r"annual.?report|impact.?report|year.?in.?review", u))
            + 4 * bool(re.search(r"our funds|fund (directory|list)|funds we|find a fund|component funds|all funds", t))
            + 3 * bool(re.search(r"fund.?(directory|list)|our.?funds|/funds/?$|find.?a.?fund", u))
            + 3 * bool(re.search(r"audit|financial statement|financials|990", t + " " + u))
            + 1 * bool(re.search(r"scholarship|types of funds|fund types|agency|designated|field of interest", t))
            + u.endswith(".pdf")
            - 9 * bool(re.search(r"feed|privacy|cookie|event|news/|post/|blog|story|stories|career|employment|login|"
                                 r"donate|give-now|cart|checkout|\?", u)))


def candidates(page: Mapping, home: str) -> tuple[tuple[int, str], ...]:
    return tuple((score(u, t), u) for u, t in B.anchors(page.get("html", ""), page["url"])
                 if u.startswith("http") and (B.same_site(u, home) or re.search(r"(?i)\.pdf|uploads|/files?/", u))
                 and (COUNT_LINK.search(urllib.parse.unquote(u)) or COUNT_LINK.search(t)))


def terms_check(cache: str, home_page: Mapping, home: str) -> tuple[str, bool]:
    links = tuple(u for u, t in B.anchors(home_page.get("html", ""), home_page["url"])
                  if B.same_site(u, home) and TERMS_LINK.search(t + " " + urllib.parse.unquote(u).rsplit("/", 2)[-2:][0] +
                                                                  urllib.parse.unquote(u).rsplit("/", 1)[-1]))
    if not links:
        return "no terms page linked from homepage", True
    pg = get(cache, links[0])
    hits = tuple(sorted({m.group(0).lower() for m in TERMS_RX.finditer(pg.get("text", ""))}))
    return (f"terms {links[0]}: mentions {', '.join(hits)} -> stopped" if hits else f"terms {links[0]}: no automated-access clause"), not hits


def crawl_site(cache: str, ein: str, home: str, max_pages: int = 18) -> dict:
    first = get(cache, home)
    if not first["allowed"] or not first.get("html"):
        return {"ein": ein, "home": home, "robots": first["robots"], "home_status": first["status"], "terms": "", "fetched": []}
    tverdict, tok = terms_check(cache, first, home)
    if not tok:
        return {"ein": ein, "home": home, "robots": first["robots"], "home_status": first["status"], "terms": tverdict,
                "fetched": []}
    sm = get(cache, urllib.parse.urljoin(home, "/sitemap.xml"))
    loc_re = r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\s\]]+)"
    sm_all = tuple(re.findall(loc_re, sm.get("html") or ""))
    subs = tuple(u for u in sm_all if u.endswith(".xml") and re.search(r"(?i)page|post-sitemap|sitemap-?\d|pages|fund", u))[:4]
    sm_locs = tuple(u for u in sm_all + tuple(x for s in subs for x in re.findall(loc_re, get(cache, s).get("html") or ""))
                    if not u.endswith(".xml"))
    lvl1 = candidates(first, home) + tuple((score(u, ""), u) for u in sm_locs if COUNT_LINK.search(urllib.parse.unquote(u)))
    top1 = tuple(dict.fromkeys(u for sc, u in sorted(lvl1, key=lambda x: (-x[0], x[1])) if sc > 0))[:10]
    pages1 = tuple(get(cache, u) for u in top1)
    lvl2 = tuple(c for p in pages1 for c in candidates(p, home) if c[1] not in top1 and c[1] != home)
    top2 = tuple(dict.fromkeys(u for sc, u in sorted(lvl2, key=lambda x: (-x[0], x[1])) if sc > 0))[:max_pages - len(top1)]
    pages = pages1 + tuple(get(cache, u) for u in top2)
    return {"ein": ein, "home": home, "robots": first["robots"], "home_status": first["status"], "terms": tverdict,
            "fetched": [p["url"] for p in pages]}


def text_of(root, tag: str) -> str | None:
    el = next((e for e in root.iter() if e.tag.rsplit("}", 1)[-1] == tag), None)
    return None if el is None else (el.text or "").strip()


def sched_d(cache: str, oid: str) -> dict:
    rec = get(cache, XML_URL.format(oid=oid))
    if not rec.get("html"):
        return {"oid": oid, "status": rec["status"], "robots": rec["robots"]}
    root = ET.fromstring(rec["html"].encode("utf-8"))
    return {"oid": oid, "status": rec["status"], "robots": rec["robots"],
            "daf_cnt": text_of(root, "DonorAdvisedFundsHeldCnt"), "other_cnt": text_of(root, "FundsAndOtherAccountsHeldCnt"),
            "daf_eoy": text_of(root, "DonorAdvisedFundsVlEOYAmt"), "other_eoy": text_of(root, "FundsAndOtherAccountsVlEOYAmt"),
            "period_end": text_of(root, "TaxPeriodEndDt"), "website": text_of(root, "WebsiteAddressTxt")}


def site_pages(cache: str, ein: str) -> tuple[dict, ...]:
    path = os.path.join(cache, "crawl_summary.json")
    if not os.path.exists(path):
        return ()
    with open(path, encoding="utf-8") as fh:
        summ = {r["ein"]: r for r in json.load(fh)}
    s = summ.get(ein)
    return () if not s else tuple(p for p in (cached(cache, u) for u in [s["home"]] + s["fetched"]) if p)


def count_sentences(text: str) -> tuple[str, ...]:
    parts = re.split(r"(?<=[.;!?])\s+|\n{2,}", re.sub(r"[ \t]+", " ", text))
    return tuple(dict.fromkeys(p.strip()[:300] for p in parts if COUNT_SENT.search(p)))


# ----------------------------------------------------------------------------- tasks (network ones need --fetch)
def homepages(vmap_rows: Sequence[Mapping]) -> dict:
    return {r["ein"]: r["homepage"] for r in vmap_rows if r.get("homepage", "").startswith("http")}


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--task", choices=("sample", "schedd", "crawl", "fetch", "hits", "robots", "build"), required=True)
    ap.add_argument("--cache-dir")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--ein", action="append", default=[])
    a = ap.parse_args(argv)
    os.chdir(a.root)
    sample = draw(frame(read_csv(COST_CSV)))
    homes = {**homepages(read_csv(VMAP_CSV)), **HOME_OVERRIDE}
    if a.task == "sample":
        print("\n".join(f"{r['stratum']}\t{r['stratum_N']}\t{r['ein']}\t{r['name']}\t{r['usable']}\t{homes.get(r['ein'], '')}"
                        for r in sample))
        return 0
    if a.task in ("schedd", "crawl", "fetch") and not (a.fetch and a.cache_dir):
        print("network tasks need --fetch and --cache-dir", file=sys.stderr)
        return 2
    if a.cache_dir:
        os.makedirs(a.cache_dir, exist_ok=True)
    if a.task == "schedd":
        oids = [r["return_object_id"] for r in sample if r["return_object_id"]] + a.url
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
            res = list(ex.map(lambda o: sched_d(a.cache_dir, o), oids))
        with open(os.path.join(a.cache_dir, "schedd.json"), "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)
        print("\n".join(json.dumps(r) for r in res))
        return 0
    if a.task == "crawl":
        targets = [(e, homes[e]) for e in (a.ein or [r["ein"] for r in sample]) if homes.get(e)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            res = list(ex.map(lambda t: crawl_site(a.cache_dir, *t), targets))
        path = os.path.join(a.cache_dir, "crawl_summary.json")
        old = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else []
        merged = {**{r["ein"]: r for r in old}, **{r["ein"]: r for r in res}}
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(list(merged.values()), fh, indent=1)
        print("\n".join(f"{r['ein']}\t{r['home_status']}\t{r['robots']}\t{r['terms']}\t{len(r['fetched'])}" for r in res))
        return 0
    if a.task == "fetch":
        recs = [get(a.cache_dir, u) for u in a.url]
        print("\n".join(f"{r['status']}\t{r['robots']}\t{len(r['text'])}\t{r['url']}" for r in recs))
        return 0
    if a.task == "hits":
        for r in sample:
            if a.ein and r["ein"] not in a.ein:
                continue
            pages = site_pages(a.cache_dir, r["ein"])
            print(f"\n=== {r['ein']} {r['name']} [{r['stratum']}] pages={len(pages)}")
            for p in pages:
                ss = count_sentences(p.get("text", ""))
                if ss:
                    print(f"  -- {p['url']} ({p['status']}, {len(p.get('text', ''))} chars)")
                    print("\n".join(f"     * {s}" for s in ss[:25]))
        return 0
    if a.task == "robots":
        print(open(os.path.join(a.cache_dir, "robots_log.tsv"), encoding="utf-8").read())
        return 0
    return build(sample, a.cache_dir)


HOME_OVERRIDE: dict[str, str] = {
    "383210718": "https://www.chippewacountycommunityfoundation.org/",  # vendor-map homepage lacks a TLD; 990 WebsiteAddressTxt truncated
}


# ----------------------------------------------------------------------------- transcription (filled after research)
# status: counted (a total of all component funds is published) | endowment_only (count covers endowed funds only) |
#   cumulative (count of funds ever established) | partial (only some fund types counted) | no_count_found (site read,
#   no 2021+ fund count) | robots_blocked | bot_challenge | site_unreachable | no_website
# total_qual: exact | lower_bound ('over', 'more than', '+') ; types: counts by type (same keys as TYPE_KEYS); type
# counts with '_lb' in type_qual are lower bounds. Quotes are verified against the cached source text (or raw HTML).
TYPE_KEYS = ("daf", "designated", "field_of_interest", "scholarship", "agency", "unrestricted", "other")
X990 = XML_URL
FUNDS: dict[str, dict] = {
    # ================= s0 $10-50m
    "461997449": dict(status="partial", source_type="form990_narrative", source_url=X990.format(oid="202523149349306462"),
                      period="FY2024 990", scope="endowment_only", quotes=("ENDOWMENT INCLUDES FOUR INDIVIDUAL FUNDS",),
                      notes="Site annual reports and 990 copies on the site are 2014-2021 and give no total fund count; FY2024 990 "
                            "counts only the endowment's funds (4). Not used for rule F."),
    "330748536": dict(status="bot_challenge", notes="Homepage returned 'Please wait while your request is being verified'."),
    "550748246": dict(status="counted", source_type="annual_report", total=500, total_qual="lower_bound", scope="all_funds",
                      period="2021 annual report",
                      source_url="https://stdidpacfwvprod.blob.core.windows.net/pacfwv/documents/publications/Annual-Reports/PACF_AnnualReport2021.pdf",
                      quotes=("charitable steward of more than 500 different charitable funds",),
                      types=dict(scholarship=200), type_qual="scholarship_lb",
                      type_source="https://pacfwv.com/initiatives/scholarships (live 2026-11-20): 'administers more than 200 scholarship funds'",
                      type_quotes=("administers more than 200 scholarship funds",), type_url="https://pacfwv.com/initiatives/scholarships",
                      notes="Includes the three regional affiliates. 2022-23 and 2023-24 reports are image PDFs (no text). Total is FY2021; "
                            "Schedule D DAF count is FY2024 (June)."),
    "840920862": dict(status="no_count_found", notes="2024 annual report page and report archive read (2002-2010 PDFs pre-2021): no fund count."),
    "741839536": dict(status="counted", source_type="annual_report", total=600, total_qual="lower_bound", scope="all_funds",
                      period="Report to the Community (2023)", source_url="https://www.epcf.org/who-we-are/report-to-the-community",
                      quotes=("The more than 600 funds now established in",),
                      notes="Page text is two interleaved columns; the sentence continues 'the El Paso Community Foundation represent ...'."),
    "581610318": dict(status="no_count_found", notes="2017-2024 annual reports read: new-fund counts only (2018: 47 new funds, pre-2021); no total."),
    "383649922": dict(status="bot_challenge", notes="Homepage returned a bot-verification page."),
    "341935499": dict(status="cumulative", source_type="website_stat", total=250, total_qual="lower_bound", scope="all_funds_cumulative",
                      period="live 2026-11-20", source_url="https://www.myhcf.org/", quotes=("250+ Funds Established",),
                      notes="'Funds Established' may count funds ever opened, not funds held; used only in the sensitivity set. "
                            "Agency and scholarship directories exist but were not counted."),
    "582360356": dict(status="counted", source_type="form990_narrative", total=200, total_qual="lower_bound", scope="all_funds",
                      period="FY2024 990 (same return as Schedule D)", source_url=X990.format(oid="202523019349300037"),
                      quotes=("MANAGES OVER 200 CHARITABLE FUNDS",), notes="Homepage has no counter; 990 Part III narrative."),
    "232765498": dict(status="counted", source_type="form990_narrative", total=400, total_qual="lower_bound", scope="all_funds",
                      period="FY2024 990 (same return as Schedule D)", source_url=X990.format(oid="202512799349300406"),
                      quotes=("THE LUZERNE FOUNDATION MANAGES OVER 400 FUNDS",),
                      notes="Site figures disagree: types-of-funds page 'over 318 funds', 2023 brochure 'more than 400', 2025 annual "
                            "report 'nearly 500 funds', homepage '700+ Charitable Funds'. The FY2024 990 figure is used (same period)."),
    "311044298": dict(status="partial", source_type="form990_narrative", source_url=X990.format(oid="202501349349310815"),
                      period="FY2024 990", scope="grantmaking_funds_only", quotes=("FROM 1,283 FUNDS",),
                      notes="The Depository (a Dayton Foundation affiliate holding donor-advised and designated funds) made grants 'from "
                            "1,283 funds' in FY2024, fewer than its 1,785 Schedule D DAFs, so this is not a fund total. The Dayton "
                            "Foundation's '4400+ Total Funds' (homepage) is the parent group. Not used for rule F."),
    "411429402": dict(status="partial", source_type="form990_narrative", source_url=X990.format(oid="202523079349302892"),
                      period="FY2024 990", scope="some_types", types=dict(), quotes=("FROM 4 TEMPORARY SCHOLARSHIP FUNDS",),
                      notes="Only temporary scholarship funds are counted (4); endowed scholarship funds not counted. The 2022-2025 annual reports sit on cdn.prod.website-files.com, whose robots.txt returns 403 (treated as disallowed): not read."),
    "232773822": dict(status="counted", source_type="website_stat", total=430, total_qual="lower_bound", scope="all_funds",
                      period="live 2026-11-20", source_url="https://www.chescocf.org/",
                      quotes=("We currently manage over 430 different charitable funds",)),
    "386057160": dict(status="no_count_found", notes="'Our Funds' page lists funds in free text; not countable reliably; no stated total."),
    "042572276": dict(status="partial", source_type="website_stat", scope="some_types", period="live 2026-11-20",
                      source_url="https://greaterworcester.org/for-students/scholarships-overview/our-scholarship-funds",
                      types=dict(scholarship=150), type_qual="scholarship_lb", quotes=("While we have over 150 funds",),
                      notes="Scholarship funds only; 2025 annual report page gives no total."),
    "592114988": dict(status="robots_blocked", notes="robots.txt returned 403: treated as disallowed."),
    "426060414": dict(status="counted", source_type="website_stat", total=1000, total_qual="exact", scope="all_funds",
                      period="live 2026-11-20", source_url="https://www.cfneia.org/", quotes=("1000 Funds",),
                      notes="Round homepage figure ('$194 Million In Total Assets 1000 Funds'); impact report gives assets by type in $ only."),
    "264322369": dict(status="no_count_found", notes="Audits (2023-2025) give designated/FOI/scholarship balances in $, not counts; 'Our Funds' page has no total."),
    "262101084": dict(status="site_unreachable", notes="Homepage HTTP 403 to research-script/1.0 (robots.txt 404)."),
    "351830262": dict(status="site_unreachable", notes="Homepage HTTP 404."),
    # ================= s1 $1-10m
    "541963011": dict(status="no_count_found", notes="Our Funds page: 'To see a full list of our funds, view our latest annual report' (not reached by the crawl)."),
    "330216692": dict(status="site_unreachable", notes="Connection error on robots.txt and homepage."),
    "371397503": dict(status="counted", source_type="fund_directory", scope="all_funds", period="live 2026-11-20",
                      source_url="https://www.mortoncommunityfoundation.org/categorized-funds",
                      directory=dict(start="Funds Organized by Type: Structured for Impact", marker="CLICK HERE to learn more",
                                     sections=(("Scholarships You can invest your gifts", "scholarship"),
                                               ("Designated Funds You can direct your gifts", "designated"),
                                               ("Field of Interest Funds You can target your gifts", "field_of_interest"),
                                               ("Agency Funds An Agency Fund is established", "agency"),
                                               ("Unrestricted Funds Your gift can address", "unrestricted"),
                                               ("Donor Advised Funds - Endowed You can have ongoing", None),
                                               ("Donor Choice Funds - Non-Endowed You can establish", None),
                                               ("Pass-Through Funds - Non-Endowed", "other")),
                                     end="Privacy Policy"),
                      quotes=("Funds Organized by Type: Structured for Impact", "more than 150 endowment funds"),
                      verify_urls=("https://www.mortoncommunityfoundation.org/categorized-funds", "https://www.mortoncommunityfoundation.org/"),
                      notes="Non-DAF types counted from the by-type directory (one 'CLICK HERE to learn more' per fund; the separator count "
                            "differs by 1 in 4 sections). DAF sections list holders' names only and are not counted; DAFs = Schedule D "
                            "FY2024 count. Total = directory non-DAF funds + Schedule D DAFs. Homepage: 'more than 150 endowment funds'."),
    "742341399": dict(status="partial", source_type="website_stat", scope="some_types", period="live 2026-11-20",
                      source_url="https://summitfoundation.org/students/apply-for-a-scholarship", types=dict(scholarship=33),
                      quotes=("we manage 33 named scholarship funds",),
                      notes="'Nearly 60 philanthropic funds' (fundholder page) covers donor-advised and similar funds only."),
    "731566026": dict(status="robots_blocked", notes="occf.org (parent OCCF site) robots.txt disallows ClaudeBot, anthropic-ai, Claude-User, "
                                                      "Claude-Web and Claude-SearchBot: not fetched (hard rule)."),
    "731547637": dict(status="counted", source_type="website_stat", total=345, total_qual="exact", scope="all_funds",
                      period="live 2026-11-20", source_url="https://www.cherokeestripcf.com/", quotes=("345 $34 Funds Million in Assets",),
                      types=dict(scholarship=15), type_url=X990.format(oid="202502789349300005"),
                      type_quotes=("administration of 15 different scholarship funds",),
                      notes="Homepage counters ('345 Funds', '$34 Million in Assets') are interleaved in the text. Scholarship count from FY2024 990."),
    "721390352": dict(status="no_count_found", notes="Fund-type page only."),
    "391563654": dict(status="no_count_found", notes="Annual-reports page read; no count."),
    "470786586": dict(status="partial", source_type="website_stat", scope="some_types", period="'Updated January 2026'",
                      source_url="https://www.kearneyfoundation.org/_files/ugd/90548d_aea5b0537831467e85951a6db7f07ac7.pdf",
                      types=dict(scholarship=69), quotes=("manages 69 scholarship funds",),
                      notes="'More than 260 funds' appears only in the 1995-2020 impact report (pre-2021, not used)."),
    "912143250": dict(status="site_unreachable", notes="Connection error."),
    "541950727": dict(status="counted", source_type="annual_report", scope="all_funds", period="2022 Report to the Community",
                      source_url="https://communityfoundationlf.org/wp-content/uploads/2023/09/2022-Report-to-the-Community.pdf",
                      types=dict(daf=33, designated=26, agency=12, field_of_interest=21, scholarship=7, unrestricted=10, other=1),
                      quotes=("Donor Advised Funds (33)", "Designated Funds (26)", "Agency Funds (12)", "Field of Interest Funds (21)",
                              "Scholarship Funds (7)", "Fiscal Sponsorship Funds (1)", "Unrestricted Funds (10)"),
                      notes="'Endowment & Component Funds' by type with counts; other = 1 fiscal sponsorship fund. 2021 report: 29/24/11/20/5/1/10."),
    "760821144": dict(status="counted", source_type="fund_directory", total=68, total_qual="exact", scope="all_funds",
                      period="live 2026-11-20", source_url="https://willcountycf.org/funds/view-all-funds/",
                      quotes=("presently home to sixty-eight funds",)),
    "352036110": dict(status="endowment_only", source_type="annual_report", total=187, total_qual="exact", scope="endowment_only",
                      period="2024 annual report",
                      source_url="https://www.dearborncf.org/wp-content/uploads/2026/02/2024-DCF-Annual-Report-12-2025-1.pdf",
                      quotes=("administers 187 endowment funds",),
                      notes="Endowed funds only; types page: 'a total of more than 160 endowments and non-permanent funds' (older)."),
    "470596705": dict(status="no_count_found", notes="Directory menu lists scholarship and managed funds; no stated total; not counted."),
    "351860518": dict(status="robots_blocked", notes="robots.txt returned 403: treated as disallowed."),
    "831970895": dict(status="counted", source_type="fund_directory", total=200, total_qual="lower_bound", scope="all_funds",
                      period="live 2026-11-20", source_url="https://oceanafoundation.org/give/our-funds/",
                      quotes=("Explore any of our 200+ charitable funds",), types=dict(scholarship=63),
                      type_url="https://oceanafoundation.org/scholarships/",
                      type_quotes=("Across 63 scholarship funds",),
                      notes="Scholarship page also says 'more than 55 scholarship funds' (older paragraph); 63 is the current-year figure."),
    "411761590": dict(status="no_count_found", notes="Scholarship list PDFs only."),
    "042103944": dict(status="robots_blocked", notes="robots.txt disallows ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot."),
    "203579294": dict(status="no_count_found", notes="Fund List page (free text, about 150 entries) has no stated total and no reliable per-fund marker; not counted. Financials PDFs are on a usrfiles.com host whose robots.txt returns 403: not read."),
    "481169158": dict(status="partial", source_type="website_stat", scope="some_types", period="live 2026-11-20",
                      source_url="https://www.emporiacf.org/types-of-funds.cfm", quotes=("we have set up nearly 20 of these accounts",),
                      notes="DAFs set up since 1996 (cumulative), not a current count; no total."),
    # ================= s2 <$1m
    "956068137": dict(status="robots_blocked", notes="robots.txt returned 403: treated as disallowed."),
    "233096312": dict(status="counted", source_type="website_stat", total=178, total_qual="exact", scope="all_funds",
                      period="2025 (homepage counter, live 2026-11-20)", source_url="https://www.twintierscf.org/",
                      quotes=("Total Number of Funds in 2025", 'data-number-value="178"'),
                      notes="Counter value is in the HTML attribute (animated number). Scholarship handbook (revised 2026-04) says "
                            "'160 Individual Funds' and 'over 50 scholarship funds'."),
    "203841038": dict(status="no_count_found", notes="2023-2025 annual reports give balances by fund type in $ only."),
    "760530567": dict(status="no_count_found", notes="Site pages read; no count."),
    "251881899": dict(status="robots_blocked", notes="robots.txt returned 403: treated as disallowed."),
    "341399690": dict(status="no_count_found", notes="Site pages read; no count."),
    "351903148": dict(status="no_count_found", notes="2023 annual report has a 'Funds List' (pp. 17-18) in multi-column layout; not counted reliably."),
    "541239701": dict(status="partial", source_type="website_stat", scope="some_types", period="2026 presentation",
                      source_url="https://www.eastmontcf.com/s/ecf-2026-presentation.pdf", types=dict(scholarship=6),
                      quotes=("has 6 endowed funds from local donors dedicated for annual",), notes="Endowed scholarship funds only."),
    "351934464": dict(status="counted", source_type="website_stat", total=250, total_qual="lower_bound", scope="all_funds",
                      period="live 2026-11-20", source_url="https://www.owencountycf.org/", quotes=("one of our over 250 funds",),
                      types=dict(scholarship=61),
                      type_url="https://www.owencountycf.org/_files/ugd/a8e52d_772d975677cc4b5aa53cdb12d6e8b8a4.pdf",
                      type_quotes=("61 Scholarship Funds",), notes="Scholarship count from the 2022 annual report."),
    "421088936": dict(status="no_count_found", notes="Site pages read; no count. Annual report (2.28.25) and 2025 990 copy are on irp.cdn-website.com, whose robots.txt returns 403 (treated as disallowed): not read."),
    "204265927": dict(status="no_website", notes="No homepage in cf-vendor-map or the FY2024 990."),
    "472581417": dict(status="no_count_found", notes="Site pages read; no count."),
    "351769294": dict(status="no_count_found", notes="Site pages read; no count."),
    "351881810": dict(status="no_count_found", notes="Site pages read; no count."),
    "841528859": dict(status="no_count_found", notes="Menu lists about 20 funds; no stated total; not counted."),
    "931167214": dict(status="counted", source_type="website_stat", total=28, total_qual="exact", scope="all_funds",
                      period="live 2026-11-20", source_url="https://dallascommunityfoundation.com/", quotes=("Charitable Funds 28",),
                      types=dict(scholarship=18), type_url="https://dallascommunityfoundation.com/scholarships/",
                      type_quotes=("administers 18 scholarship funds",), notes="Homepage dashboard square 'Charitable Funds' = 28."),
    "383210718": dict(status="endowment_only", source_type="audit_note", total=75, total_qual="approx", scope="endowment_only",
                      period="FY2025 audit (same wording FY2021-24)",
                      source_url="https://www.chippewacountycommunityfoundation.org/wp-content/uploads/2026/11/CCCF-12.31.25-Audited-Financial-Statements.pdf",
                      quotes=("endowments consist of approximately seventy-five individual funds",), notes="Endowed funds only."),
    "752970373": dict(status="partial", source_type="form990_narrative", scope="some_types", period="FY2024 990",
                      source_url=X990.format(oid="202533249349300648"), types=dict(agency=5),
                      quotes=("THE FOUNDATION WAS THE OWNER OF FIVE AGENCY FUNDS",),
                      notes="Agency funds only. Schedule D DAF count blank in the FY2024 return."),
    "392041822": dict(status="no_website", notes="No homepage in cf-vendor-map or the FY2024 990."),
    "474465692": dict(status="counted", source_type="website_stat", total=40, total_qual="lower_bound", scope="all_funds",
                      period="live 2026-11-20", source_url="https://www.ccfks.org/", quotes=("Through more than 40 charitable funds",),
                      notes="2021 annual report: 'We have 34 funds'."),
}


# ----------------------------------------------------------------------------- build (pure given the cache)
def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("’", "'").replace(" ", " ")).strip().lower()


def source_text(cache: str | None, urls: Sequence[str]) -> str:
    recs = tuple(r for r in (cached(cache, u) for u in urls if u) if r) if cache else ()
    return norm(" ".join((r.get("text") or "") + " " + (r.get("html") or "") for r in recs))


def verify(cache: str | None, urls: Sequence[str], quotes: Sequence[str]) -> str:
    if not quotes:
        return ""
    text = source_text(cache, urls)
    return "source not cached" if not text else f"verified {sum(1 for q in quotes if norm(q) in text)}/{len(quotes)}"


def directory_counts(text: str, spec: Mapping) -> dict:
    """Count spec['marker'] between consecutive section anchors (searched in order after spec['start'])."""
    t = re.sub(r"\s+", " ", text)
    start = t.find(spec["start"])
    if start < 0:
        return {}
    pos = reduce_positions(t, start, tuple(a for a, _ in spec["sections"]) + (spec["end"],))
    if any(p < 0 for p in pos):
        return {}
    segs = tuple((typ, t[a:b].count(spec["marker"])) for (anchor, typ), a, b in zip(spec["sections"], pos, pos[1:]))
    return {typ: sum(n for k, n in segs if k == typ) for typ in {k for k, _ in segs if k}}


def reduce_positions(t: str, start: int, anchors: Sequence[str]) -> tuple[int, ...]:
    def step(acc: tuple[int, ...], a: str) -> tuple[int, ...]:
        last = acc[-1] if acc else start
        return acc + ((t.find(a, last + 1) if last >= 0 else -1),)
    return functools.reduce(step, anchors, ())


def sched_rows(cache: str | None) -> dict:
    path = os.path.join(cache or "", "schedd.json")
    if not cache or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return {d["oid"]: d for d in json.load(fh)}


def homepage_robots(cache: str | None, home: str) -> str:
    rec = cached(cache, home) if cache and home else None
    return "" if not rec else f"{rec['robots']}; HTTP {rec['status']}"


def fund_row(r: Mapping, sd: Mapping, home: str, cache: str | None) -> dict:
    f = FUNDS.get(r["ein"], {"status": "not_researched"})
    d = sd.get(r["return_object_id"], {})
    sched_daf, sched_other = num(d.get("daf_cnt")), num(d.get("other_cnt"))
    dir_types = (directory_counts((cached(cache, f["source_url"]) or {}).get("text", ""), f["directory"])
                 if f.get("directory") and cache else {})
    types = {**(f.get("types") or {}), **dir_types}
    stated_total = f.get("total")
    total, total_basis = ((stated_total, "stated") if stated_total is not None else
                          ((sum(types.get(k, 0) for k in TYPE_KEYS) if "daf" in types else
                            (sum(types.get(k, 0) for k in TYPE_KEYS) + (sched_daf or 0)) if dir_types and sched_daf is not None else None),
                           ("sum_of_types" if "daf" in types else "directory_non_daf_plus_sched_d_daf")) if types and f.get("scope") == "all_funds"
                          else (None, ""))
    daf_n, daf_basis = ((types["daf"], "source") if "daf" in types else (sched_daf, "sched_d_fy2024") if sched_daf is not None else (None, ""))
    opex, accts, dassets = num(r["opex_ex_11f"]), num(r["daf_accounts_fy2024_screened"]), num(r["daf_assets_fy2024"])
    share_f = (None if (daf_n is None or not total or r["usable"] != "1" or f.get("scope") != "all_funds")
               else min(1.0, daf_n / total))
    share_f_sd = None if (sched_daf is None or not total or r["usable"] != "1") else min(1.0, sched_daf / total)
    cost_f = None if share_f is None or opex is None else opex * share_f
    quotes_ok = verify(cache, f.get("verify_urls") or (f.get("source_url"),), f.get("quotes") or ())
    type_ok = verify(cache, (f.get("type_url"),), f.get("type_quotes") or ())
    return {
        "ein": r["ein"], "name": r["name"], "stratum": r["stratum"], "size_band_fy2024": r["size_band_fy2024"],
        "stratum_N": r["stratum_N"], "stratum_n": r["stratum_n"], "weight": fmt(r["weight"], 2), "usable_cost": r["usable"],
        "daf_assets_fy2024": r["daf_assets_fy2024"], "daf_accounts_fy2024_screened": r["daf_accounts_fy2024_screened"],
        "opex_ex_11f": r["opex_ex_11f"], "total_assets_eoy": r["total_assets_eoy"], "return_object_id": r["return_object_id"],
        "sched_d_tax_period_end": d.get("period_end", ""), "sched_d_daf_count": fmt(sched_daf, 0),
        "sched_d_other_funds_count": fmt(sched_other, 0), "website": home, "homepage_robots": homepage_robots(cache, home),
        "count_status": f["status"], "source_type": f.get("source_type", ""), "source_url": f.get("source_url", ""),
        "source_period": f.get("period", ""), "count_scope": f.get("scope", ""),
        **{f"n_{k}": fmt(types.get(k), 0) for k in TYPE_KEYS},
        "type_qual": f.get("type_qual", ""), "n_total_funds": fmt(total, 0), "total_basis": total_basis,
        "total_qual": f.get("total_qual", "computed" if total_basis.startswith(("sum", "directory")) else ""),
        "daf_count_for_F": fmt(daf_n, 0), "daf_count_basis": daf_basis,
        "daf_share_F": fmt(share_f, 4), "daf_share_F_sched_d": fmt(share_f_sd, 4),
        "daf_share_A": r["daf_share_assets"], "daf_share_G": r["daf_share_grants"],
        "daf_cost_alloc_F": fmt(cost_f, 0),
        "daf_cost_per_account_alloc_F": fmt(ratio(cost_f, accts), 0),
        "daf_cost_bps_daf_assets_alloc_F": fmt(None if ratio(cost_f, dassets) is None else ratio(cost_f, dassets) * 1e4, 1),
        "opex_per_fund": fmt(ratio(opex, total) if r["usable"] == "1" else None, 0),
        "daf_cost_per_account_alloc_A": r["daf_cost_per_account_alloc_A"], "daf_cost_per_account_alloc_G": r["daf_cost_per_account_alloc_G"],
        "daf_cost_bps_daf_assets_alloc_A": r["daf_cost_bps_daf_assets_alloc_A"], "daf_cost_bps_daf_assets_alloc_G": r["daf_cost_bps_daf_assets_alloc_G"],
        "quote_check": quotes_ok, "type_quote_check": type_ok, "notes": f.get("notes", ""),
    }


FIELDS = ("ein", "name", "stratum", "size_band_fy2024", "stratum_N", "stratum_n", "weight", "usable_cost", "daf_assets_fy2024",
          "daf_accounts_fy2024_screened", "opex_ex_11f", "total_assets_eoy", "return_object_id", "sched_d_tax_period_end",
          "sched_d_daf_count", "sched_d_other_funds_count", "website", "homepage_robots", "count_status", "source_type",
          "source_url", "source_period", "count_scope") + tuple(f"n_{k}" for k in TYPE_KEYS) + (
          "type_qual", "n_total_funds", "total_basis", "total_qual", "daf_count_for_F", "daf_count_basis", "daf_share_F",
          "daf_share_F_sched_d", "daf_share_A", "daf_share_G", "daf_cost_alloc_F", "daf_cost_per_account_alloc_F",
          "daf_cost_bps_daf_assets_alloc_F", "opex_per_fund", "daf_cost_per_account_alloc_A", "daf_cost_per_account_alloc_G",
          "daf_cost_bps_daf_assets_alloc_A", "daf_cost_bps_daf_assets_alloc_G", "quote_check", "type_quote_check", "notes")

STRATUM_LABEL = {"s0_10_50m": "$10–50m", "s1_1_10m": "$1–10m", "s2_lt1m": "Under $1m"}


def col(rows: Sequence[Mapping], k: str) -> list:
    return [num(r[k]) for r in rows]


def report(rows: Sequence[Mapping], fr: Sequence[Mapping]) -> str:
    strata_names = tuple(n for n, _ in STRATA)
    by = lambda s: tuple(r for r in rows if r["stratum"] == s)  # noqa: E731
    status_order = ("counted", "endowment_only", "cumulative", "partial", "no_count_found", "robots_blocked", "bot_challenge",
                    "site_unreachable", "no_website")
    out = ["## Coverage by status (sampled CFs)",
           table(("Status",) + tuple(STRATUM_LABEL[s] for s in strata_names) + ("All",),
                 [(st,) + tuple(sum(1 for r in by(s) if r["count_status"] == st) for s in strata_names) +
                  (sum(1 for r in rows if r["count_status"] == st),) for st in status_order])]
    fset = tuple(r for r in rows if r["daf_share_F"])
    sens = tuple(r for r in rows if r["n_total_funds"] and r["usable_cost"] == "1" and r["sched_d_daf_count"])
    sens_share = lambda r: min(1.0, num(r["sched_d_daf_count"]) / num(r["n_total_funds"]))  # noqa: E731
    out += ["", "## Schedule D Part I line 1 (FY2024 return), all 60",
            table(("Stratum", "n with DAF count", "DAF count (col a) median (IQR)", "n col (b) filled", "Col (b) 'funds and other accounts' median (IQR)"),
                  [(STRATUM_LABEL[s], sum(1 for r in by(s) if r["sched_d_daf_count"]), qfmt(col(by(s), "sched_d_daf_count")),
                    sum(1 for r in by(s) if r["sched_d_other_funds_count"]), qfmt(col(by(s), "sched_d_other_funds_count")))
                   for s in strata_names] +
                  [("All", sum(1 for r in rows if r["sched_d_daf_count"]), qfmt(col(rows, "sched_d_daf_count")),
                    sum(1 for r in rows if r["sched_d_other_funds_count"]), qfmt(col(rows, "sched_d_other_funds_count")))])]
    out += ["", "## Fund counts and DAF shares, CFs with an all-funds total (rule-F set)",
            table(("EIN", "Stratum", "Total funds", "Qual", "DAF funds (basis)", "Share F", "Share A", "Share G", "Opex per fund"),
                  [(r["ein"], STRATUM_LABEL[r["stratum"]], r["n_total_funds"], r["total_qual"],
                    f"{r['daf_count_for_F']} ({r['daf_count_basis']})", r["daf_share_F"], fmt(num(r["daf_share_A"]), 4),
                    fmt(num(r["daf_share_G"]), 4), f"${num(r['opex_per_fund']):,.0f}") for r in fset])]
    out += ["", "## Rule F vs rules A and G on the same CFs (medians, IQR, n)",
            table(("Stratum", "Share F", "Share A", "Share G", "F per account", "A per account", "G per account", "F bps", "A bps", "G bps"),
                  [(lab, qfmt(col(rs, "daf_share_F"), 3), qfmt(col(rs, "daf_share_A"), 3), qfmt(col(rs, "daf_share_G"), 3),
                    qfmt(col(rs, "daf_cost_per_account_alloc_F"), 0, "$"), qfmt(col(rs, "daf_cost_per_account_alloc_A"), 0, "$"),
                    qfmt(col(rs, "daf_cost_per_account_alloc_G"), 0, "$"), qfmt(col(rs, "daf_cost_bps_daf_assets_alloc_F"), 0),
                    qfmt(col(rs, "daf_cost_bps_daf_assets_alloc_A"), 0), qfmt(col(rs, "daf_cost_bps_daf_assets_alloc_G"), 0))
                   for lab, rs in tuple((STRATUM_LABEL[s], tuple(r for r in fset if r["stratum"] == s)) for s in strata_names) +
                   (("All (unweighted)", fset),)])]
    ratios_a = [ratio(num(r["daf_share_F"]), num(r["daf_share_A"])) for r in fset]
    ratios_g = [ratio(num(r["daf_share_F"]), num(r["daf_share_G"])) for r in fset]
    wpairs = lambda k: [(num(r[k]), num(r["weight"])) for r in fset if num(r[k]) is not None]  # noqa: E731
    ci = lambda k: boot_ci(col(fset, k))  # noqa: E731
    out += ["", "## Ratios and weighted medians (rule-F set)",
            f"- F share ÷ A share: median {qfmt(ratios_a, 2)}; F > A at {sum(1 for x in ratios_a if x and x > 1)} of {len([x for x in ratios_a if x])}",
            f"- F share ÷ G share: median {qfmt(ratios_g, 2)}; F > G at {sum(1 for x in ratios_g if x and x > 1)} of {len([x for x in ratios_g if x])}",
            f"- Stratum-weighted median (weights N/n): F per account ${wmedian(wpairs('daf_cost_per_account_alloc_F')):,.0f}; "
            f"A per account ${wmedian(wpairs('daf_cost_per_account_alloc_A')):,.0f}; F bps {wmedian(wpairs('daf_cost_bps_daf_assets_alloc_F')):,.0f}; "
            f"A bps {wmedian(wpairs('daf_cost_bps_daf_assets_alloc_A')):,.0f}; G bps {wmedian(wpairs('daf_cost_bps_daf_assets_alloc_G')):,.0f}",
            f"- Bootstrap 95% CI of the unweighted median ({N_BOOT:,} resamples, seed {BOOT_SEED}): F per account "
            f"${ci('daf_cost_per_account_alloc_F')[0]:,.0f}–${ci('daf_cost_per_account_alloc_F')[1]:,.0f}; "
            f"F bps {ci('daf_cost_bps_daf_assets_alloc_F')[0]:,.0f}–{ci('daf_cost_bps_daf_assets_alloc_F')[1]:,.0f}; "
            f"share F {ci('daf_share_F')[0]:.3f}–{ci('daf_share_F')[1]:.3f}",
            f"- Opex per fund (whole org ÷ all funds): {qfmt(col(fset, 'opex_per_fund'), 0, '$')}",
            f"- Lower-bound totals ('over', 'more than', '+'): {sum(1 for r in fset if r['total_qual'] == 'lower_bound')} of {len(fset)} "
            "(share F and F cost are upper bounds for these)"]
    out += ["", "## Sensitivity: Schedule D DAF count as numerator everywhere, and endowment-only / cumulative totals included",
            table(("Set", "n", "Share (Sched D DAFs ÷ total)", "Cost per account", "bps"),
                  [(lab, len(rs), qfmt([sens_share(r) for r in rs], 3),
                    qfmt([ratio(num(r["opex_ex_11f"]) * sens_share(r), num(r["daf_accounts_fy2024_screened"])) for r in rs], 0, "$"),
                    qfmt([None if ratio(num(r["opex_ex_11f"]) * sens_share(r), num(r["daf_assets_fy2024"])) is None else
                          ratio(num(r["opex_ex_11f"]) * sens_share(r), num(r["daf_assets_fy2024"])) * 1e4 for r in rs], 0))
                   for lab, rs in (("All-funds totals only", tuple(r for r in sens if r["count_scope"] == "all_funds")),
                                   ("+ cumulative and endowment-only totals", sens))])]
    typed = tuple(r for r in rows if r["count_scope"] == "all_funds" and r["n_total_funds"])
    out += ["", "## Fund-type counts where published (all-funds CFs)",
            table(("EIN", "Total", "DAF", "Designated", "FOI", "Scholarship", "Agency", "Unrestricted", "Other", "Scholarship ÷ total", "DAF (Sched D) ÷ total"),
                  [(r["ein"], r["n_total_funds"], r["n_daf"], r["n_designated"], r["n_field_of_interest"], r["n_scholarship"], r["n_agency"],
                    r["n_unrestricted"], r["n_other"], fmt(ratio(num(r["n_scholarship"]), num(r["n_total_funds"])), 3),
                    fmt(ratio(num(r["sched_d_daf_count"]), num(r["n_total_funds"])), 3))
                   for r in typed if any(r[f"n_{k}"] for k in TYPE_KEYS)])]
    usable = tuple(r for r in fr if r["usable"] == "1")
    out += ["", "## Context: the sample against the frame (rule A, tail CFs, cost-note medians)",
            table(("Set", "n", "A per account", "A bps", "G bps"),
                  [("Frame: all usable tail CFs", len(usable), qfmt(col(usable, "daf_cost_per_account_alloc_A"), 0, "$"),
                    qfmt(col(usable, "daf_cost_bps_daf_assets_alloc_A"), 0), qfmt(col(usable, "daf_cost_bps_daf_assets_alloc_G"), 0)),
                   ("Sample of 60", len(rows), qfmt(col(rows, "daf_cost_per_account_alloc_A"), 0, "$"),
                    qfmt(col(rows, "daf_cost_bps_daf_assets_alloc_A"), 0), qfmt(col(rows, "daf_cost_bps_daf_assets_alloc_G"), 0)),
                   ("Rule-F set", len(fset), qfmt(col(fset, "daf_cost_per_account_alloc_A"), 0, "$"),
                    qfmt(col(fset, "daf_cost_bps_daf_assets_alloc_A"), 0), qfmt(col(fset, "daf_cost_bps_daf_assets_alloc_G"), 0))])]
    out += ["", "## Quote checks", "\n".join(f"- {r['ein']}: {r['quote_check']}{'; types ' + r['type_quote_check'] if r['type_quote_check'] else ''}"
                                             for r in rows if r["quote_check"])]
    return "\n".join(out)


def build(sample: Sequence[Mapping], cache: str | None) -> int:
    homes = {**homepages(read_csv(VMAP_CSV)), **HOME_OVERRIDE}
    sd = sched_rows(cache)
    rows = tuple(fund_row(r, sd, homes.get(r["ein"], ""), cache) for r in sample)
    write_csv(OUT_CSV, rows, FIELDS)
    print(report(rows, frame(read_csv(COST_CSV))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
