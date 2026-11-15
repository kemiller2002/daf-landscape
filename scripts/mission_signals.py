#!/usr/bin/env python3
"""P-NEW-SIG-01: news-coverage and hiring signals for the DAF market (stdlib only, functional style).

Tasks
  discover  For each sponsor / vendor careers page in CAREERS_PAGES: read robots.txt, fetch the page only if allowed,
            and list the applicant-tracking-system (ATS) hosts it links to. Output: JSON in --work-dir (used to fill
            HIRING_SOURCES by hand; nothing is guessed).
  news      GDELT DOC 2.0 API (http://api.gdeltproject.org/api/v2/doc/doc), 2021-01-01 .. 2026-11-14:
            daily raw article counts (mode=timelinevolraw) for the base DAF phrase query and for the base query AND
            each theme keyword group, summed to calendar months; plus up to 250 article titles per year
            (mode=artlist, sort=hybridrel) for a headline sample. One request every >= 10 s (GDELT asks for <= 1 per 5 s).
            Output: data/mission-2026-11-14/daf-news-volume-2021-2026.csv and --work-dir/news-headlines.json
  hiring    Public ATS JSON endpoints (Greenhouse boards-api, Lever postings API, Ashby posting API) and
            robots-permitted career pages listed in HIRING_SOURCES. One row per open posting with keyword flags.
            Output: data/mission-2026-11-14/daf-hiring-signals-2026.csv and --work-dir/hiring-summary.json

Robots policy: robots.txt is read on every host before any other request to it (RFC 9309 semantics: 2xx parsed;
4xx except 429 = no rules; 429 / 5xx / unreachable = disallow everything). The decision log is written to --work-dir/robots-log.json.

Usage
  python3 scripts/mission_signals.py discover --work-dir WORK
  python3 scripts/mission_signals.py news     --work-dir WORK
  python3 scripts/mission_signals.py hiring   --work-dir WORK
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
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
from collections import Counter, defaultdict
from functools import lru_cache
from typing import Iterable, Mapping, Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "mission-2026-11-14")
UA = "Mozilla/5.0 (compatible; research-script/1.0; python-urllib)"
TODAY = "2026-11-15"
ROBOTS_LOG: list[dict] = []

# ----------------------------------------------------------------------------------------------- HTTP + robots


def http_get(url: str, timeout: int = 60, accept: str = "*/*") -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read() if e.fp else b""
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        return 0, str(e).encode()


@lru_cache(maxsize=None)
def robots_for(scheme_host: str) -> urllib.robotparser.RobotFileParser | str:
    """Return a parser, or 'allow_all' / 'disallow_all' per RFC 9309 status handling."""
    status, body = http_get(scheme_host + "/robots.txt", timeout=30)
    if 200 <= status < 300:
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(body.decode("utf-8", "replace").splitlines())
        verdict: urllib.robotparser.RobotFileParser | str = rp
    elif 400 <= status < 500 and status != 429:
        verdict = "allow_all"
    else:
        verdict = "disallow_all"
    ROBOTS_LOG.append({"host": scheme_host, "robots_status": status,
                       "policy": verdict if isinstance(verdict, str) else "parsed"})
    return verdict


def allowed(url: str) -> bool:
    p = urllib.parse.urlsplit(url)
    rp = robots_for(f"{p.scheme}://{p.netloc}")
    if rp == "allow_all":
        return True
    if rp == "disallow_all":
        return False
    return rp.can_fetch(UA, url)  # type: ignore[union-attr]


def polite_get(url: str, timeout: int = 60, accept: str = "*/*") -> tuple[int, bytes]:
    if not allowed(url):
        return -1, b"robots.txt disallows"
    return http_get(url, timeout=timeout, accept=accept)


def get_json(url: str) -> object | None:
    status, body = polite_get(url, accept="application/json")
    if status != 200:
        return None
    try:
        return json.loads(body.decode("utf-8", "replace"))
    except json.JSONDecodeError:
        return None


def write_csv(path: str, rows: Sequence[Mapping], cols: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cols), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def dump(path: str, obj: object) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


# ----------------------------------------------------------------------------------------------- discover

CAREERS_PAGES = [
    ("Fidelity Charitable", "sponsor", "https://www.fidelitycharitable.org/about-us/careers.html"),
    ("Schwab / DAFgiving360", "sponsor", "https://www.schwabjobs.com/"),
    ("Vanguard Charitable", "sponsor", "https://www.vanguardcharitable.org/careers"),
    ("National Philanthropic Trust", "sponsor", "https://www.nptrust.org/careers/"),
    ("Silicon Valley Community Foundation", "sponsor_cf", "https://www.siliconvalleycf.org/careers"),
    ("Chicago Community Trust", "sponsor_cf", "https://www.cct.org/about/careers/"),
    ("New York Community Trust", "sponsor_cf", "https://www.nycommunitytrust.org/about/careers/"),
    ("Greater Kansas City Community Foundation", "sponsor_cf", "https://www.growyourgiving.org/careers"),
    ("Tulsa Community Foundation", "sponsor_cf", "https://tulsacf.org/careers/"),
    ("Ren", "vendor", "https://www.reninc.com/careers"),
    ("Chariot", "vendor", "https://www.givechariot.com/careers"),
    ("Daffy", "vendor", "https://www.daffy.org/careers"),
    ("Endaoment", "vendor", "https://endaoment.org/careers"),
    ("Givinga", "vendor", "https://www.givinga.com/careers"),
    ("Benevity", "vendor", "https://benevity.com/careers"),
    ("Blackbaud", "vendor", "https://careers.blackbaud.com/"),
    ("Bonterra", "vendor", "https://www.bonterratech.com/careers"),
    ("Foundant", "vendor", "https://www.foundant.com/careers/"),
    ("TIFIN", "vendor", "https://tifin.com/careers/"),
    ("Every.org", "vendor", "https://www.every.org/careers"),
]

ATS_RE = re.compile(
    r"https?://[^\"'\s<>]*(?:greenhouse\.io|lever\.co|ashbyhq\.com|myworkdayjobs\.com|paylocity\.com|bamboohr\.com|"
    r"workable\.com|smartrecruiters\.com|applytojob\.com|adp\.com|paycomonline\.net|icims\.com|ultipro\.com|"
    r"recruitee\.com|rippling\.com|dayforcehcm\.com|breezy\.hr|notion\.site|jobvite\.com|phenompeople\.com|"
    r"teamtailor\.com|pinpointhq\.com|gusto\.com|eightfold\.ai|successfactors|oraclecloud\.com)[^\"'\s<>]*", re.I)


def discover_one(org: str, seg: str, url: str) -> dict:
    status, body = polite_get(url, timeout=40, accept="text/html")
    text = body.decode("utf-8", "replace") if status == 200 else ""
    links = sorted({html.unescape(m) for m in ATS_RE.findall(text)})[:25]
    return {"org": org, "segment": seg, "url": url, "status": status, "ats_links": links, "bytes": len(body)}


def task_discover(work: str) -> None:
    out = [discover_one(*row) for row in CAREERS_PAGES]
    dump(os.path.join(work, "careers-discovery.json"), out)
    dump(os.path.join(work, "robots-log.json"), ROBOTS_LOG)
    for r in out:
        print(r["org"], r["status"], r["ats_links"][:4])




# ----------------------------------------------------------------------------------------------- news (GDELT)

GDELT = "http://api.gdeltproject.org/api/v2/doc/doc"  # https endpoint reset connections from this session
GDELT_GAP_S = 12.0
BASE_Q = '("donor-advised fund" OR "donor-advised funds" OR "donor advised fund" OR "donor advised funds")'
THEMES = {
    "payout_reform": '(payout OR "payout rate" OR reform OR "ACE Act" OR "Accelerating Charitable Efforts" OR warehousing)',
    "controversial_grantees": '(SPLC OR "Southern Poverty" OR "hate group" OR "hate groups" OR extremist OR extremists OR "dark money")',
    "crypto": '(crypto OR cryptocurrency OR bitcoin OR ethereum OR NFT)',
    "ai": '("artificial intelligence" OR "generative AI" OR ChatGPT OR chatbot OR "machine learning" OR "AI agent")',
    "giving_records": '(record OR "record-breaking" OR "giving report" OR "all-time high")',
    "legislation": '(Congress OR Senate OR IRS OR Treasury OR legislation OR "proposed regulations" OR "tax bill" OR "One Big Beautiful Bill")',
}
# Title-level classifiers for the headline sample (case-insensitive regex mirrors of THEMES).
TITLE_THEMES = {
    "payout_reform": r"payout|reform|ace act|accelerating charitable|warehous",
    "controversial_grantees": r"splc|southern poverty|hate group|extremis|dark money",
    "crypto": r"crypto|bitcoin|ethereum|\bnft",
    "ai": r"artificial intelligence|generative ai|chatgpt|chatbot|machine learning|\bai\b",
    "giving_records": r"record|giving report|all-time high",
    "legislation": r"congress|senate|\birs\b|treasury|legislat|regulation|tax bill|big beautiful bill",
}
YEARS = [(y, f"{y}0101000000", f"{y}1231235959" if y < 2026 else "20261114235959") for y in range(2021, 2027)]
_last_call = [0.0]


def gdelt(params: Mapping[str, str]) -> dict | None:
    url = GDELT + "?" + urllib.parse.urlencode({**params, "format": "json"})
    for attempt in range(8):
        wait = GDELT_GAP_S - (time.time() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.time()
        status, body = polite_get(url, timeout=90)
        text = body.decode("utf-8", "replace")
        if status == 200 and text.lstrip().startswith("{"):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
        print(f"  gdelt retry {attempt + 1} status={status} {text[:120]!r}", file=sys.stderr)
        time.sleep(60 * (attempt + 1))
    raise RuntimeError(f"GDELT request failed after retries: {url}")  # never write silent zeros


RESOLUTIONS: dict[str, str] = {}


def timeline(query: str, start: str, end: str) -> list[dict]:
    d = gdelt({"query": query + " sourcelang:english", "mode": "timelinevolraw", "startdatetime": start,
               "enddatetime": end, "timelinesmooth": "0"})
    RESOLUTIONS[f"{query[:40]}|{start}"] = (d or {}).get("query_details", {}).get("date_resolution", "")
    if not d or not d.get("timeline"):
        return []
    return d["timeline"][0]["data"]


def monthly(points: Iterable[dict]) -> dict[str, tuple[int, int]]:
    acc: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for p in points:
        k = p["date"][:4] + "-" + p["date"][4:6]
        acc[k][0] += int(p["value"])
        acc[k][1] += int(p.get("norm", 0))
    return {k: (v[0], v[1]) for k, v in acc.items()}


def artlist(query: str, start: str, end: str, n: int) -> list[dict]:
    d = gdelt({"query": query + " sourcelang:english", "mode": "artlist", "maxrecords": str(n),
               "startdatetime": start, "enddatetime": end, "sort": "hybridrel"})
    return (d or {}).get("articles", []) or []


def title_themes(title: str) -> list[str]:
    t = title.lower()
    return [k for k, rx in TITLE_THEMES.items() if re.search(rx, t)]


def task_news(work: str) -> None:
    # One full-window call per series keeps the request count low (GDELT rate-limits this shared egress hard);
    # the API chooses the bucket size for the window, recorded in RESOLUTIONS and summed to calendar months.
    start, end = YEARS[0][1], YEARS[-1][2]
    series: dict[str, dict[str, tuple[int, int]]] = {}
    for name, q in [("base", BASE_Q), *[(t, f"{BASE_Q} {q}") for t, q in THEMES.items()]]:
        print("timeline", name)
        series[name] = monthly(timeline(q, start, end))
    months = sorted(series["base"])
    rows = [{
        "month": mth,
        "articles_daf": series["base"][mth][0],
        "articles_monitored_total": series["base"][mth][1],
        "daf_per_million_monitored": round(series["base"][mth][0] / series["base"][mth][1] * 1e6, 3)
        if series["base"][mth][1] else "",
        **{f"articles_{t}": series[t].get(mth, (0, 0))[0] for t in THEMES},
        "partial_month": "yes" if mth == "2026-11" else "no",
    } for mth in months]
    cols = ["month", "articles_daf", "articles_monitored_total", "daf_per_million_monitored",
            *[f"articles_{t}" for t in THEMES], "partial_month"]
    write_csv(os.path.join(DATA, "daf-news-volume-2021-2026.csv"), rows, cols)

    sample = {}
    for y, a, b in YEARS:
        print("artlist base", y)
        arts = artlist(BASE_Q, a, b, 250)
        sample[str(y)] = [{"date": x.get("seendate", "")[:8], "domain": x.get("domain"), "title": x.get("title"),
                           "url": x.get("url"), "themes": title_themes(x.get("title") or "")} for x in arts]
    theme_samples = {}
    for theme, q in THEMES.items():
        print("artlist", theme)
        arts = artlist(f"{BASE_Q} {q}", YEARS[0][1], YEARS[-1][2], 15)
        theme_samples[theme] = [{"date": x.get("seendate", "")[:8], "domain": x.get("domain"),
                                 "title": x.get("title"), "url": x.get("url")} for x in arts]
    dump(os.path.join(work, "news-headlines.json"), {"by_year": sample, "by_theme": theme_samples,
                                                      "queries": {"base": BASE_Q, **THEMES},
                                                      "resolutions": RESOLUTIONS})
    dump(os.path.join(work, "robots-log-news.json"), ROBOTS_LOG)
    print(summarize_news(rows, sample))


def summarize_news(rows: Sequence[Mapping], sample: Mapping[str, list]) -> str:
    by_year: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        y = r["month"][:4]
        by_year[y]["daf"] += int(r["articles_daf"])
        by_year[y]["norm"] += int(r["articles_monitored_total"])
        for t in THEMES:
            by_year[y][t] += int(r[f"articles_{t}"])
    out = []
    for y in sorted(by_year):
        c = by_year[y]
        sh = {t: round(100 * c[t] / c["daf"], 1) if c["daf"] else 0 for t in THEMES}
        ts = Counter(t for a in sample.get(y, []) for t in a["themes"])
        out.append(f"{y}: daf={c['daf']} per_m={c['daf'] / c['norm'] * 1e6 if c['norm'] else 0:.2f} "
                   f"theme%={sh} title_sample_n={len(sample.get(y, []))} title_themes={dict(ts)}")
    top = sorted(rows, key=lambda r: -int(r["articles_daf"]))[:8]
    out.append("top months: " + ", ".join(f"{r['month']}={r['articles_daf']}" for r in top))
    return "\n".join(out)


# ----------------------------------------------------------------------------------------------- hiring

KW = {
    "ai": re.compile(r"\bAI\b|\bA\.I\.|[Aa]rtificial [Ii]ntelligence|\bGenAI\b|[Gg]enerative|[Aa]gentic"),
    "ml": re.compile(r"[Mm]achine [Ll]earning|\bML\b|\bMLOps\b"),
    "llm": re.compile(r"\bLLMs?\b|[Ll]arge [Ll]anguage [Mm]odel|\bGPT|ChatGPT|[Pp]rompt [Ee]ngineering|\bRAG\b|OpenAI|Anthropic"),
    "automation": re.compile(r"[Aa]utomat"),
    "data": re.compile(r"\b[Dd]ata\b"),
}
FUNCS = [
    ("data", r"\bdata\b|analytic|scientist|\bbi\b|insight"),
    ("engineering", r"engineer|developer|architect|devops|\bsre\b|\bqa\b|software|platform|security|infrastructure|technical|it "),
    ("product_design", r"product|design|\bux\b|research"),
    ("sales_gtm", r"sales|account|partnership|business development|marketing|customer success|gtm|growth|implementation|solutions|relationship"),
]


def func_of(title: str, team: str) -> str:
    t = f" {title} {team} ".lower()
    return next((name for name, rx in FUNCS if re.search(rx, t)), "operations_other")


def strip_html(s: str) -> str:
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s or "", flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def snippet(text: str, rx: re.Pattern) -> str:
    m = rx.search(text)
    return "" if not m else text[max(0, m.start() - 70): m.end() + 70].replace("\n", " ")


def sentences(text: str) -> list[str]:
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+|\s+-\s+|\s{2,}", text) if len(x.strip()) > 25]


def boilerplate_of(rows: Sequence[Mapping], min_share: float = 0.4) -> dict[str, set[str]]:
    """Sentences repeated in >= min_share of an org's postings (org with >= 4 postings) = employer boilerplate."""
    by_org: dict[str, list[set[str]]] = defaultdict(list)
    for r in rows:
        by_org[r["org"]].append(set(sentences(r["_desc"])))
    out = {}
    for org, sets in by_org.items():
        c = Counter(x for st in sets for x in st)
        out[org] = {x for x, n in c.items() if len(sets) >= 4 and n / len(sets) >= min_share}
    return out


USE_RX = re.compile(r"AI[- ](?:powered |assisted |enabled )?tools?|(?:use|using|leverag\w*|comfort\w*|fluen\w*|curio\w*)"
                    r"[^.]{0,40}\bAI\b|AI-(?:assisted|forward|enabled content)|ChatGPT|Claude", re.I)
BUILD_RX = re.compile(r"build\w*[^.]{0,60}(?:AI|LLM|agent|model)|(?:AI|LLM|ML)[-/ ](?:powered |driven )?"
                      r"(?:product|feature|application|system|agent|pipeline|engineer)|agentic|\bRAG\b|model serving|"
                      r"machine learning|LLM judges", re.I)


def role_level(rows: list[dict]) -> list[dict]:
    """Add flags computed on the description minus employer boilerplate, and a heuristic AI-mention type."""
    bp = boilerplate_of(rows)

    def one(r: dict) -> dict:
        if r["description_available"] != "yes":
            extra = {f"role_{k}": "" for k in KW} | {"role_any_ai_ml_llm": "", "ai_mention_type": ""}
        else:
            kept = " ".join(x for x in sentences(r["_desc"]) if x not in bp[r["org"]])
            txt = f"{r['title']} {r['team']} {kept}"
            extra = {f"role_{k}": int(bool(rx.search(txt))) for k, rx in KW.items()}
            extra["role_any_ai_ml_llm"] = max(extra["role_ai"], extra["role_ml"], extra["role_llm"])
            build = bool(BUILD_RX.search(txt)) and r["function"] in ("engineering", "data", "product_design")
            extra["ai_mention_type"] = ("" if not extra["role_any_ai_ml_llm"] else "build_ai" if build
                                        else "use_ai_tools" if USE_RX.search(txt) else "other_mention")
        return {**{k: v for k, v in r.items() if k != "_desc"}, **extra}

    return [one(r) for r in rows]


def posting(org: str, seg: str, source: str, title: str, team: str = "", location: str = "", posted: str = "",
            description: str = "", desc_available: bool = True) -> dict:
    title, team, desc = strip_html(title), strip_html(team), strip_html(description)
    full = f"{title} {team} {desc}"
    flags = {f"desc_{k}": int(bool(rx.search(full))) if desc_available else "" for k, rx in KW.items()}
    tflags = {f"title_{k}": int(bool(rx.search(f"{title} {team}"))) for k, rx in KW.items()}
    any_ai_t = max(tflags["title_ai"], tflags["title_ml"], tflags["title_llm"])
    if desc_available:
        any_ai = max(flags["desc_ai"], flags["desc_ml"], flags["desc_llm"])
        any5 = max(any_ai, flags["desc_automation"], flags["desc_data"])
    else:
        any_ai, any5 = "", ""
    ctx = next((snippet(full, KW[k]) for k in ("llm", "ml", "ai") if KW[k].search(full)), "") if desc_available else ""
    return {"org": org, "segment": seg, "source": source, "date_fetched": TODAY, "title": title, "team": team,
            "location": strip_html(location), "posted_or_updated": posted[:10], "function": func_of(title, team),
            "description_available": "yes" if desc_available else "no", "desc_chars": len(desc), **tflags,
            "title_any_ai_ml_llm": any_ai_t, **flags, "desc_any_ai_ml_llm": any_ai, "desc_any_of_five": any5,
            "ai_context": ctx[:200], "_desc": desc}


def from_greenhouse(org: str, seg: str, slug: str, filt=None) -> list[dict]:
    src = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
    d = get_json(src) or {}
    return [posting(org, seg, src, j["title"], ", ".join(x["name"] for x in j.get("departments", [])),
                    (j.get("location") or {}).get("name", ""), j.get("updated_at", ""), j.get("content", ""))
            for j in d.get("jobs", []) if not filt or filt(j)]


def from_lever(org: str, seg: str, slug: str) -> list[dict]:
    src = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    d = get_json(src) or []
    return [posting(org, seg, src, j["text"], (j.get("categories") or {}).get("team", ""),
                    (j.get("categories") or {}).get("location", ""),
                    dt.datetime.utcfromtimestamp(j.get("createdAt", 0) / 1000).isoformat(),
                    j.get("descriptionPlain", "") + " " + j.get("additionalPlain", "")) for j in d]


def from_ashby(org: str, seg: str, slug: str) -> list[dict]:
    src = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    d = get_json(src) or {}
    return [posting(org, seg, src, j["title"], " / ".join(x for x in (j.get("department"), j.get("team")) if x),
                    j.get("location", ""), j.get("publishedAt", ""), j.get("descriptionPlain") or j.get("descriptionHtml", ""))
            for j in d.get("jobs", []) if j.get("isListed", True)]


def from_workday_sitemap(org: str, seg: str, host: str, tenant: str, site: str) -> list[dict]:
    sm = f"https://{host}/{site}/siteMap.xml"
    status, body = polite_get(sm)
    locs = re.findall(r"<loc>(https://[^<]+/job/[^<]+)</loc>", body.decode("utf-8", "replace")) if status == 200 else []
    out = []
    for loc in locs:
        path = loc.split(f"/{site}/", 1)[1]
        d = get_json(f"https://{host}/wday/cxs/{tenant}/{site}/{path}") or {}
        j = d.get("jobPostingInfo") or {}
        if j:
            out.append(posting(org, seg, sm, j.get("title", ""), "", j.get("location", ""), j.get("startDate", ""),
                               j.get("jobDescription", "")))
        time.sleep(0.5)
    return out


def from_phenom(org: str, seg: str, base: str) -> list[dict]:
    out, seen, start, total = [], set(), 0, None
    while total is None or start < total:
        url = f"{base}?from={start}&s=1"
        status, body = polite_get(url)
        t = body.decode("utf-8", "replace")
        m = re.search(r'"eagerLoadRefineSearch":(\{.*?\}),"(?:jobwidgetsettings|siteConfig|pageName)"', t, re.S)
        blob = None
        if m:
            try:
                blob = json.loads(m.group(1))
            except json.JSONDecodeError:
                blob = None
        if blob is None:
            i = t.find('"eagerLoadRefineSearch":')
            if i < 0:
                break
            blob, _ = json.JSONDecoder().raw_decode(t[i + len('"eagerLoadRefineSearch":'):])
        total = int(blob.get("totalHits", 0))
        jobs = (blob.get("data") or {}).get("jobs", [])
        if not jobs:
            break
        for j in jobs:
            key = j.get("jobSeqNo") or j.get("jobId") or j.get("title")
            if key in seen:
                continue
            seen.add(key)
            desc = (j.get("descriptionTeaser") or "") + " " + " ".join(j.get("ml_skills") or [])
            out.append(posting(org, seg, base, j.get("title", ""), j.get("category", ""), j.get("location", ""),
                               j.get("postedDate", ""), desc))
        start += len(jobs)
        time.sleep(1)
    return out


def from_adp(org: str, seg: str, cid: str) -> list[dict]:
    src = ("https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/job-requisitions"
           f"?cid={cid}&lang=en_US")
    d = get_json(src) or {}
    out = []
    for j in d.get("jobRequisitions", []):
        loc = "; ".join((x.get("address") or {}).get("cityName", "") for x in j.get("requisitionLocations", []))
        title = j.get("requisitionTitle", "")
        desc_url = (f"https://workforcenow.adp.com/mascsr/default/careercenter/public/events/staffing/v1/"
                    f"job-requisitions/{j.get('itemID')}?cid={cid}&lang=en_US")
        dd = get_json(desc_url) or {}
        desc = dd.get("requisitionDescription", "")
        out.append(posting(org, seg, src, title, "", loc, j.get("postDate", ""), desc, desc_available=bool(desc)))
    return out


def from_paylocity(org: str, seg: str, url: str) -> list[dict]:
    status, body = polite_get(url)
    t = body.decode("utf-8", "replace")
    i = t.find("pageData = ")
    if status != 200 or i < 0:
        return []
    d, _ = json.JSONDecoder().raw_decode(t[i + len("pageData = "):])
    return [posting(org, seg, url, j.get("JobTitle", ""), j.get("HiringDepartment") or "", j.get("LocationName", ""),
                    j.get("PublishedDate", ""), j.get("Description", ""), desc_available=False) for j in d.get("Jobs", [])]


def from_link_pages(org: str, seg: str, index_url: str, link_rx: str, base: str) -> list[dict]:
    status, body = polite_get(index_url)
    links = sorted(set(re.findall(link_rx, body.decode("utf-8", "replace")))) if status == 200 else []
    out = []
    for path in links:
        url = urllib.parse.urljoin(base, path)
        s, b = polite_get(url)
        if s != 200:
            continue
        t = b.decode("utf-8", "replace")
        m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        title = strip_html(m.group(1)) if m else path.rsplit("/", 1)[-1].replace("-", " ")
        body_from_h1 = t[m.start():] if m else t  # drop site navigation above the role heading
        out.append(posting(org, seg, index_url, title, "", "", "", strip_html(body_from_h1)))
        time.sleep(1)
    return out


def from_fidelity_charitable() -> list[dict]:
    sm = "https://jobs.fidelity.com/sitemap.xml"
    status, body = polite_get(sm)
    locs = sorted(set(re.findall(r"<loc>(https://jobs\.fidelity\.com/en/jobs/\d+/[^<]+)</loc>", body.decode()))) \
        if status == 200 else []

    def one(u: str) -> dict | None:
        time.sleep(0.4)
        s, b = polite_get(u)
        if s != 200:
            return None
        t = b.decode("utf-8", "replace")
        m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        full = strip_html(t)
        a = full.find("Job Description")
        z = min([i for i in (full.find("Certifications:", a), full.find("Category:", a)) if i > a] or [len(full)])
        text = full[a:z] if a >= 0 else ""  # job-description body only; site chrome has an "AI Guidelines" link
        cat = re.search(r"Category:\s*(.*?)\s+Please be advised", full)
        return {"url": u, "title": strip_html(m.group(1)) if m else "", "text": text,
                "category": cat.group(1)[:60] if cat else "", "fc_mentions": text.count("Fidelity Charitable")}

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex:
        pages = [p for p in ex.map(one, locs) if p]
    fc = [p for p in pages if p["fc_mentions"] > 0]
    print(f"  fidelity sitemap jobs={len(locs)} fetched={len(pages)} mentioning Fidelity Charitable={len(fc)}")
    FID_META.update({"sitemap_jobs": len(locs), "fetched": len(pages), "fc": len(fc),
                     "fidelity_all_jobs_desc_ai_ml_llm_share": round(
                         sum(bool(KW["ai"].search(p["text"]) or KW["ml"].search(p["text"]) or KW["llm"].search(p["text"]))
                             for p in pages) / max(1, len(pages)), 3)})
    return [posting("Fidelity Charitable", "sponsor", sm + " (job pages whose description names 'Fidelity Charitable')",
                    p["title"], p["category"], "", "", p["text"]) for p in fc]


FID_META: dict = {}

NOT_COLLECTED = [
    ("Schwab / DAFgiving360", "sponsor", "https://www.schwabjobs.com/search-jobs/", "robots.txt disallows /search-jobs/"),
    ("National Philanthropic Trust", "sponsor", "https://www.nptrust.org/", "no careers page linked from site (404 on /careers/, /about-us/careers/)"),
    ("Chicago Community Trust", "sponsor_cf", "https://www.cct.org/about/careers/", "HTTP 403 to script"),
    ("Silicon Valley Community Foundation", "sponsor_cf", "https://www.svcf.org/about/join-our-team", "page lists no openings in static HTML"),
    ("Tulsa Community Foundation", "sponsor_cf", "https://tulsacf.org/careers/tcf-gkff/", "listing not in static HTML"),
    ("Endaoment", "vendor", "https://endaoment.org/careers", "JS app; no listing in static HTML; no Greenhouse/Lever/Ashby board"),
    ("Foundant", "vendor", "https://www.foundant.com/careers/", "HTTP 403 to script"),
    ("Every.org", "vendor", "https://www.every.org/careers", "robots.txt returned 429; treated as disallow"),
]


def nyct() -> list[dict]:
    url = "https://thenytrust.org/careers-fellowships/"
    status, body = polite_get(url)
    t = strip_html(body.decode("utf-8", "replace")) if status == 200 else ""
    m = re.search(r"Open Positions (.*?) Apply", t)
    return [posting("New York Community Trust", "sponsor_cf", url, x.strip(), "", "New York", "", "",
                    desc_available=False) for x in ([m.group(1)] if m else [])]


def task_hiring(work: str) -> None:
    collectors = [
        ("Fidelity Charitable", from_fidelity_charitable),
        ("Vanguard Charitable", lambda: from_adp("Vanguard Charitable", "sponsor", "0c68d588-8c9c-408d-9476-64d2fbc7640d")),
        ("Greater Kansas City CF", lambda: from_paylocity("Greater Kansas City Community Foundation", "sponsor_cf",
            "https://recruiting.paylocity.com/Recruiting/Jobs/All/caf479db-2051-4124-a5db-d0bbf0a5300d/Greater-Kansas-City-Community-Foundation")),
        ("New York Community Trust", nyct),
        ("Ren", lambda: from_greenhouse("Ren", "vendor", "renpsg")),
        ("Chariot", lambda: from_ashby("Chariot", "vendor", "chariot")),
        ("Daffy", lambda: from_link_pages("Daffy", "vendor", "https://www.daffy.org/careers",
                                          r'href="(/careers/[a-z0-9\-]+)"', "https://www.daffy.org")),
        ("Givinga", lambda: from_link_pages("Givinga", "vendor", "https://www.givinga.com/careers",
                                            r'href="\./(careers/[a-z0-9\-]+)"', "https://www.givinga.com/")),
        ("Benevity", lambda: from_ashby("Benevity", "vendor", "benevity")),
        ("Blackbaud", lambda: from_phenom("Blackbaud", "vendor", "https://careers.blackbaud.com/us/en/search-results")),
        ("Bonterra", lambda: from_workday_sitemap("Bonterra", "vendor", "bonterra.wd1.myworkdayjobs.com", "bonterra",
                                                  "bonterratech")),
        ("TIFIN", lambda: from_greenhouse("TIFIN", "vendor", "tifin")),
    ]
    rows: list[dict] = []
    for name, fn in collectors:
        got = fn()
        uniq = {(r["title"].lower(), r["_desc"][:2000]): r for r in got}  # same role multi-posted by location
        print(f"{name}: {len(got)} postings ({len(uniq)} unique title+description)")
        rows.extend(uniq.values())
    rows = role_level(rows)
    cols = list(rows[0].keys()) if rows else []
    write_csv(os.path.join(DATA, "daf-hiring-signals-2026.csv"), rows, cols)
    summary = summarize_hiring(rows)
    summary["fidelity_meta"] = FID_META
    summary["not_collected"] = [dict(zip(("org", "segment", "url", "reason"), x)) for x in NOT_COLLECTED]
    dump(os.path.join(work, "hiring-summary.json"), summary)
    dump(os.path.join(work, "robots-log-hiring.json"), ROBOTS_LOG)
    print(json.dumps({k: v for k, v in summary.items() if k != "not_collected"}, indent=1))


def share(rows: Sequence[Mapping], col: str) -> tuple[int, int, float | str]:
    vals = [int(r[col]) for r in rows if r[col] != ""]
    return sum(vals), len(vals), round(100 * sum(vals) / len(vals), 1) if vals else ""


def summarize_hiring(rows: Sequence[Mapping]) -> dict:
    groups: dict[str, list] = defaultdict(list)
    for r in rows:
        groups[r["org"]].append(r)
        groups["SEGMENT:" + ("sponsor" if r["segment"].startswith("sponsor") else "vendor")].append(r)
        groups["ALL"].append(r)
    cols = ["desc_any_ai_ml_llm", "role_any_ai_ml_llm", "role_ai", "role_ml", "role_llm", "role_automation",
            "role_data", "desc_automation", "desc_data", "desc_any_of_five", "title_any_ai_ml_llm", "title_data"]
    out = {"by_group": {g: {"n": len(rs), **{c: share(rs, c) for c in cols},
                            "functions": dict(Counter(r["function"] for r in rs)),
                            "ai_mention_type": dict(Counter(r["ai_mention_type"] for r in rs if r["ai_mention_type"]))}
                        for g, rs in sorted(groups.items())}}
    eng = [r for r in rows if r["function"] in ("engineering", "data", "product_design")]
    out["tech_roles"] = {"n": len(eng), **{c: share(eng, c) for c in cols}}
    out["non_tech_roles"] = {"n": len(rows) - len(eng),
                             **{c: share([r for r in rows if r not in eng], c) for c in cols}}
    return out


TASKS = {"discover": task_discover, "news": task_news, "hiring": task_hiring}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", choices=sorted(TASKS))
    ap.add_argument("--work-dir", required=True)
    a = ap.parse_args()
    os.makedirs(a.work_dir, exist_ok=True)
    TASKS[a.task](a.work_dir)
