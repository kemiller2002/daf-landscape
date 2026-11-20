#!/usr/bin/env python3
"""P-B39N1-03 + P-B39N2-02: DAF-adjacent federal lobbying (LDA LD-2 / LD-203) and state breach-notice registers
for DAF-sponsor parents and distributors.

(A) LDA (lda.gov REST API v1, anonymous, <= 15 requests/minute per robots.txt and the API terms; lda.senate.gov
    was sunset on 2026-07-31 and lda.gov is its documented successor).
    1. Targets   the 33 client names in data/mission-2026-11-14/daf-lobbying-lda-2021plus.csv, plus seven
                 sponsor parents / distributors (Charles Schwab, FMR/Fidelity Investments, Vanguard Group,
                 Morgan Stanley, Goldman Sachs, BNY/Bank of New York Mellon, TIFIN).
    2. Pull      /filings/?client_name=Q&filing_dt_posted_after=2021-01-01 (all pages). Queries whose hit count
                 exceeds BROAD_LIMIT (the substring "REN") go through /clients/?client_name=Q instead and then
                 /filings/?client_id=ID for each accepted client record.
    3. Accept    client names are accepted per target by exact normalised name (33 clients, with alias groups)
                 or by a pattern (parents). filing_year >= 2021. The latest posted version is kept per
                 (registrant id, client id, filing year, filing period, registration-vs-report).
    4. Tag       every lobbying-activity line: daf_named, charitable_deduction, s4966, obbba (P.L. 119-21),
                 qcd, charity_sector (general context). Regexes are in TAGS below.
    5. LD-203    /contributions/?registrant_id=ID&filing_dt_posted_after=2021-01-01 for registrants that file
                 for themselves (self-filers) among DAF-sponsor and sponsor-parent targets. Organisation-filed
                 items are kept line by line; lobbyist-filed items are only counted and summed (no names).
(B) Breach registers
    Vermont AGO: the current summary table (reports from 2026-04-17) and the archived notice listing
    (50 pages) at ago.vermont.gov/categories/security-breach-notices; matching archived notices are opened and
    their posted PDF read with pdftotext. Maine (www.maine.gov) and Massachusetts (www.mass.gov) are probed once
    and logged; both return HTTP 403 to a generic client, so nothing is taken from them.

Stdlib only (plus the pdftotext binary for PDFs); functional style; all network I/O cached on disk.

Usage:
  python3 scripts/mission_lda_breach.py . --cache DIR [--offline] [--step lda|breach|all]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from functools import reduce
from typing import Callable, Iterable, Mapping, Sequence

UA = "research-script/1.0"
API = "https://lda.gov/api/v1"
POSTED_AFTER = "2021-01-01"
MIN_YEAR = 2021
BROAD_LIMIT = 600
LDA_DELAY = 4.2          # robots.txt Crawl-delay 4; 15/minute anonymous
VT_DELAY = 2.0
STAMP = "2026-11-20"
MISSION = os.path.join("data", "mission-2026-11-14")
IN_CSV = os.path.join(MISSION, "daf-lobbying-lda-2021plus.csv")
OUT_LDA = os.path.join(MISSION, f"lda-daf-adjacent-2021plus-{STAMP}.csv")
OUT_203 = os.path.join(MISSION, f"lda-ld203-daf-sponsor-contributions-2021plus-{STAMP}.csv")
OUT_BREACH = os.path.join(MISSION, f"breach-notices-daf-parents-{STAMP}.csv")

ROBOTS = ("https://lda.gov/robots.txt", "https://lda.senate.gov/robots.txt", "https://ago.vermont.gov/robots.txt",
          "https://www.maine.gov/robots.txt", "https://apps.web.maine.gov/robots.txt",
          "https://www.mass.gov/robots.txt")
PROBES = ("https://www.maine.gov/agviewer/content/ag/985235c7-cb95-4be2-8792-a1252b4f8318/list.html",
          "https://apps.web.maine.gov/online/aeviewer/ME/40/list.shtml",
          "https://www.mass.gov/lists/data-breach-reports")

# --------------------------------------------------------------------------------------------------- targets
SPONSOR_CATS = ("national_daf_sponsor", "single_issue_faith_daf_sponsor", "community_foundation", "giving_platform",
                "daf_platform_vendor")
ALIASES = {  # normalised name -> entity key
    "JEWISH FEDERATIONS OF NORTH AMERICA": "JEWISH FEDERATIONS OF NORTH AMERICA",
    "PHILANTHROPY ROUNDTABLE": "PHILANTHROPY ROUNDTABLE",
    "REN": "REN", "REN ACQUISITION COMPANY": "REN",
}
# parents / distributors: (entity, queries, accept pattern, sponsor link per repo research)
PARENTS = (
    ("CHARLES SCHWAB", ("Charles Schwab",), r"^(THE )?CHARLES SCHWAB\b", "Schwab Charitable (DAFgiving360)"),
    ("FMR / FIDELITY INVESTMENTS", ("FMR", "Fidelity Investments"),
     r"^FMR LLC\b|^FIDELITY INVESTMENTS\b|^FIDELITY MANAGEMENT (&|AND) RESEARCH", "Fidelity Charitable"),
    ("VANGUARD GROUP", ("Vanguard",), r"^(THE )?VANGUARD( GROUP\b.*)?$", "Vanguard Charitable"),
    ("MORGAN STANLEY", ("Morgan Stanley",), r"\bMORGAN STANLEY\b", "Morgan Stanley GIFT"),
    ("GOLDMAN SACHS", ("Goldman Sachs",), r"\bGOLDMAN SACHS\b", "Goldman Sachs Philanthropy Fund"),
    ("BNY", ("BNY", "Bank of New York Mellon", "BNY Mellon"),
     r"^(THE )?BANK OF NEW YORK MELLON\b|^BNY\b|BNY MELLON|FORMERLY BANK OF NEW YORK MELLON", "BNY Mellon Charitable Gift Fund"),
    ("TIFIN", ("TIFIN",), r"\bTIFIN\b", "TIFIN Give (GiveClear)"),
)
EXTRA_QUERIES = {"GO FUND ME": ("GoFundMe",)}


def norm(name: str) -> str:
    s = re.sub(r"[^A-Z0-9& ]", " ", (name or "").upper().replace(",", " "))
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^THE ", "", s)
    return re.sub(r"( (INC|LLC|L L C|CORP|CORPORATION|CO|LTD|LP))+$", "", s).strip()


def entity_of(name: str) -> str:
    n = norm(name)
    return ALIASES.get(n, n)


def read_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: str, rows: Sequence[Mapping], cols: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cols), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def targets_from(prior: Sequence[Mapping]) -> tuple[dict, ...]:
    names = sorted({(r["client"], r["client_category"]) for r in prior})
    base = tuple({"entity": entity_of(n), "query": q, "source": "csv33", "category": c,
                  "accept": ("exact", entity_of(n)), "sponsor_link": ""}
                 for n, c in names for q in (n,) + EXTRA_QUERIES.get(n, ()))
    par = tuple({"entity": e, "query": q, "source": "parent7", "category": "sponsor_parent_or_distributor",
                 "accept": ("regex", pat), "sponsor_link": link}
                for e, qs, pat, link in PARENTS for q in qs)
    return base + par


def accepts(t: Mapping, client_name: str) -> bool:
    kind, val = t["accept"]
    return entity_of(client_name) == val if kind == "exact" else bool(re.search(val, (client_name or "").upper()))


# --------------------------------------------------------------------------------------------------- http
def cache_path(cache: str, url: str, ext: str = "") -> str:
    return os.path.join(cache, hashlib.sha1(url.encode()).hexdigest() + ext)


def http_get(url: str, delay: float, tries: int = 4) -> tuple[int, bytes]:
    time.sleep(delay)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        if e.code in (429, 502, 503, 504) and tries > 1:
            time.sleep(65 if e.code == 429 else 15)
            return http_get(url, delay, tries - 1)
        return e.code, e.read() if hasattr(e, "read") else b""
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        if tries > 1:
            time.sleep(15)
            return http_get(url, delay, tries - 1)
        return 0, str(e).encode()


def fetch(cache: str, offline: bool, delay: float) -> Callable[[str], tuple[int, bytes]]:
    def go(url: str) -> tuple[int, bytes]:
        p = cache_path(cache, url)
        if os.path.exists(p):
            with open(p, "rb") as f:
                meta = json.loads(f.readline())
                return meta["status"], f.read()
        if offline:
            return -1, b""
        status, body = http_get(url, delay)
        if status in (200, 403, 404):
            with open(p, "wb") as f:
                f.write((json.dumps({"url": url, "status": status, "at": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n").encode())
                f.write(body)
        return status, body
    return go


def get_json(get: Callable, url: str) -> dict:
    status, body = get(url)
    if status != 200:
        raise RuntimeError(f"{status} for {url}")
    return json.loads(body)


def paged(get: Callable, url: str) -> tuple[dict, ...]:
    def step(acc: tuple, u: str | None) -> tuple:
        if not u:
            return acc
        d = get_json(get, u)
        return step(acc + tuple(d["results"]), d.get("next"))
    return step((), url)


def api_url(path: str, **params) -> str:
    return f"{API}/{path}/?" + urllib.parse.urlencode({**params, "page_size": 25})


# --------------------------------------------------------------------------------------------------- LDA pull
def pull_target(get: Callable, t: Mapping) -> tuple[dict, ...]:
    first = get_json(get, api_url("filings", client_name=t["query"], filing_dt_posted_after=POSTED_AFTER))
    if first["count"] <= BROAD_LIMIT:
        rows = paged(get, api_url("filings", client_name=t["query"], filing_dt_posted_after=POSTED_AFTER))
    else:
        clients = paged(get, api_url("clients", client_name=t["query"]))
        ids = sorted({c["id"] for c in clients if accepts(t, c["name"])})
        rows = tuple(f for i in ids for f in paged(get, api_url("filings", client_id=i, filing_dt_posted_after=POSTED_AFTER)))
    return tuple({**f, "_target": t} for f in rows if accepts(t, f["client"]["name"]))


def version_key(f: Mapping) -> tuple:
    reg = "REG" if (f.get("filing_type") or "").startswith("R") else "LD2"
    return (f["registrant"]["id"], f["client"]["id"], f["filing_year"], f.get("filing_period") or "", reg)


def latest_versions(filings: Iterable[Mapping]) -> tuple[dict, ...]:
    by_uuid = reduce(lambda acc, f: acc if f["filing_uuid"] in acc else {**acc, f["filing_uuid"]: f}, filings, {})
    in_window = [f for f in by_uuid.values() if int(f["filing_year"]) >= MIN_YEAR]
    best = reduce(lambda acc, f: {**acc, version_key(f): f}
                  if version_key(f) not in acc or (f["dt_posted"] or "") > (acc[version_key(f)]["dt_posted"] or "")
                  else acc, in_window, {})
    return tuple(sorted(best.values(), key=lambda f: (f["_target"]["entity"], f["filing_year"], f["dt_posted"] or "")))


# --------------------------------------------------------------------------------------------------- tags
DAF = r"donor[\s-]*advised|\bDAFs?\b|accelerating charitable efforts|\bACE Act\b"
TAGS: dict[str, tuple[str, int]] = {   # tag -> (regex, minimum filing year for the pattern)
    "charitable_deduction": (r"charitable (?:contribution|deduction|giving|donation|gift)s?\b|non-?itemizer|"
                             r"universal charitable|\bcharitable act\b|deduction for (?:charitable|gifts)|"
                             r"(?:section|sec\.|§|IRC)\s*170\b|charitable tax", MIN_YEAR),
    "s4966": (r"4966|taxable distributions?\b|donor[\s-]*advised funds?\W+(?:\w+\W+){0,4}regulat|"
              r"regulat\w*\W+(?:\w+\W+){0,6}donor[\s-]*advised", MIN_YEAR),
    "obbba": (r"119[\s-]*21\b|one big beautiful|\bOBBBA?\b", MIN_YEAR),
    "obbba_hr1": (r"\bH\.?\s*R\.?\s*1\b(?![\d.,]\d)", 2025),
    "qcd": (r"qualified charitable distributions?|\bQCDs?\b|charitable rollover|\bIRA (?:charitable )?rollover|"
            r"legacy IRA", MIN_YEAR),
    "qcd_bill": (r"\b(?:H\.?\s*R\.?|S\.?)\s*(?:2891|3975)\b", 2025),
    "charity_sector": (r"charit|philanthrop|non-?profit|tax[\s-]*exempt organi|exempt organi|foundations?\b", MIN_YEAR),
}


def daf_named(text: str) -> bool:
    hits = re.findall(DAF, text or "", flags=re.I)
    air_force = re.search(r"air force", text or "", flags=re.I) and not re.search(r"donor", text or "", flags=re.I)
    return bool(hits) and not air_force


def tag_line(text: str, year: int) -> dict:
    raw = {k: bool(re.search(p, text or "", flags=re.I)) and year >= y for k, (p, y) in TAGS.items()}
    return {"tag_daf_named": daf_named(text),
            "tag_charitable_deduction": raw["charitable_deduction"],
            "tag_s4966": raw["s4966"],
            "tag_obbba": raw["obbba"] or raw["obbba_hr1"],
            "tag_qcd": raw["qcd"] or raw["qcd_bill"],
            "tag_charity_sector": raw["charity_sector"]}


POLICY = ("tag_charitable_deduction", "tag_s4966", "tag_obbba", "tag_qcd")
ALLTAGS = ("tag_daf_named",) + POLICY + ("tag_charity_sector",)


def yn(b: bool) -> str:
    return "Y" if b else "N"


def self_filer(f: Mapping) -> bool:
    r, c = norm(f["registrant"]["name"]), norm(f["client"]["name"])
    first2 = lambda s: " ".join(s.split()[:2])
    return r == c or first2(r) == first2(c) or (r.startswith("FMR") and "FIDELITY" in c)


def line_rows(f: Mapping, prior_uuids: frozenset) -> list[dict]:
    year = int(f["filing_year"])
    acts = f.get("lobbying_activities") or []
    tagged = [(i, a, tag_line(a.get("description") or "", year)) for i, a in enumerate(acts, 1)]
    names_daf = any(t["tag_daf_named"] for _, _, t in tagged)
    any_policy = any(t[k] for _, _, t in tagged for k in POLICY)
    t = f["_target"]
    base = {
        "filing_uuid": f["filing_uuid"], "filing_year": year, "filing_period": f.get("filing_period") or "",
        "filing_type": f.get("filing_type") or "", "dt_posted": (f.get("dt_posted") or "")[:10],
        "registrant": f["registrant"]["name"], "registrant_id": f["registrant"]["id"],
        "client": f["client"]["name"], "client_id": f["client"]["id"], "target_entity": t["entity"],
        "target_source": t["source"], "target_category": t["category"], "sponsor_link": t["sponsor_link"],
        "self_filer": yn(self_filer(f)), "income_usd": f.get("income") or "", "expenses_usd": f.get("expenses") or "",
        "filing_names_daf": yn(names_daf), "filing_has_policy_tag": yn(any_policy),
        "daf_adjacent_unnamed": yn(any_policy and not names_daf),
        "in_prior_daf_csv": yn(f["filing_uuid"] in prior_uuids),
        "filing_document_url": f.get("filing_document_url") or "", "api_url": f.get("url") or ""}
    return [{**base, "line_no": i, "issue_code": a.get("general_issue_code") or "",
             **{k: yn(v) for k, v in tg.items()},
             "government_entities": ";".join(sorted({g["name"] for g in a.get("government_entities") or []})),
             "line_text": re.sub(r"\s+", " ", a.get("description") or "").strip()[:1500]}
            for i, a, tg in tagged if any(tg.values())]


LDA_COLS = ("filing_uuid", "filing_year", "filing_period", "filing_type", "dt_posted", "registrant", "registrant_id",
            "client", "client_id", "target_entity", "target_source", "target_category", "sponsor_link", "self_filer",
            "income_usd", "expenses_usd", "line_no", "issue_code") + ALLTAGS + (
            "filing_names_daf", "filing_has_policy_tag", "daf_adjacent_unnamed", "in_prior_daf_csv",
            "government_entities", "line_text", "filing_document_url", "api_url")


def amount(f: Mapping) -> float:
    return float(f.get("income") or 0) + float(f.get("expenses") or 0)


def summarise_lda(filings: Sequence[Mapping], rows: Sequence[Mapping]) -> dict:
    by_f = reduce(lambda acc, r: {**acc, r["filing_uuid"]: r}, rows, {})
    ents = sorted({f["_target"]["entity"] for f in filings})
    def ent(e: str) -> dict:
        fs = [f for f in filings if f["_target"]["entity"] == e]
        flag = lambda f, k: by_f.get(f["filing_uuid"], {}).get(k) == "Y"
        lines = [r for r in rows if r["target_entity"] == e]
        return {"entity": e, "source": fs[0]["_target"]["source"], "category": fs[0]["_target"]["category"],
                "filings": len(fs), "years": f"{min(f['filing_year'] for f in fs)}-{max(f['filing_year'] for f in fs)}",
                "registrants": len({f["registrant"]["id"] for f in fs}),
                "amount_all": sum(map(amount, fs)),
                "names_daf": sum(flag(f, "filing_names_daf") for f in fs),
                "policy_tag": sum(flag(f, "filing_has_policy_tag") for f in fs),
                "adjacent_unnamed": sum(flag(f, "daf_adjacent_unnamed") for f in fs),
                "adjacent_unnamed_amount": sum(amount(f) for f in fs if flag(f, "daf_adjacent_unnamed")),
                **{k: len({r["filing_uuid"] for r in lines if r[k] == "Y"}) for k in ALLTAGS}}
    by_year = {y: {"filings": sum(1 for f in filings if f["filing_year"] == y),
                   "adjacent_unnamed": sum(1 for f in filings if f["filing_year"] == y
                                           and by_f.get(f["filing_uuid"], {}).get("daf_adjacent_unnamed") == "Y"),
                   **{k: len({r["filing_uuid"] for r in rows if r["filing_year"] == y and r[k] == "Y"}) for k in ALLTAGS}}
               for y in sorted({f["filing_year"] for f in filings})}
    uu = lambda pred: len({r["filing_uuid"] for r in rows if pred(r)})
    return {"filings": len(filings), "entities": len(ents), "per_entity": [ent(e) for e in ents], "by_year": by_year,
            "lines_tagged": len(rows),
            "filings_policy_tag": uu(lambda r: r["filing_has_policy_tag"] == "Y"),
            "filings_daf_named": uu(lambda r: r["filing_names_daf"] == "Y"),
            "filings_adjacent_unnamed": uu(lambda r: r["daf_adjacent_unnamed"] == "Y"),
            "filings_daf_named_not_in_prior": uu(lambda r: r["filing_names_daf"] == "Y" and r["in_prior_daf_csv"] == "N"),
            "tag_filings": {k: uu(lambda r, k=k: r[k] == "Y") for k in ALLTAGS},
            "filings_adjacent_unnamed_new": uu(lambda r: r["daf_adjacent_unnamed"] == "Y" and r["in_prior_daf_csv"] == "N"),
            "adjacent_new_by_entity": dict(sorted(reduce(lambda acc, r: {**acc, r["target_entity"]: acc.get(r["target_entity"], set()) | {r["filing_uuid"]}},
                                                         [r for r in rows if r["daf_adjacent_unnamed"] == "Y" and r["in_prior_daf_csv"] == "N"], {}).items())),
            "obbba_and_chardeduct_line_filings": uu(lambda r: r["tag_obbba"] == "Y" and r["tag_charitable_deduction"] == "Y"),
            "obbba_and_chardeduct_by_entity": sorted({r["target_entity"] for r in rows if r["tag_obbba"] == "Y" and r["tag_charitable_deduction"] == "Y"}),
            "policy_tags_parent7": {k: uu(lambda r, k=k: r[k] == "Y" and r["target_source"] == "parent7") for k in ALLTAGS},
            "obbba_by_entity": sorted({(r["target_entity"]) for r in rows if r["tag_obbba"] == "Y"}),
            "s4966_by_entity": sorted({(r["target_entity"]) for r in rows if r["tag_s4966"] == "Y"}),
            "qcd_by_entity": sorted({(r["target_entity"]) for r in rows if r["tag_qcd"] == "Y"})}


# --------------------------------------------------------------------------------------------------- LD-203
def ld203_registrants(filings: Sequence[Mapping]) -> tuple[tuple[int, str, str], ...]:
    keep = [f for f in filings if self_filer(f) and (f["_target"]["category"] in SPONSOR_CATS
            or f["_target"]["source"] == "parent7" or f["_target"]["category"] == "financial_firm")]
    ents = reduce(lambda acc, f: {**acc, (f["registrant"]["id"], f["registrant"]["name"]):
                                  acc.get((f["registrant"]["id"], f["registrant"]["name"]), frozenset()) | {f["_target"]["entity"]}},
                  keep, {})
    return tuple(sorted((i, n, " + ".join(sorted(e))) for (i, n), e in ents.items()))


def latest_reports(reports: Iterable[Mapping]) -> tuple[dict, ...]:
    """One LD-203 per (registrant, filer type, lobbyist, year, half): the latest posted (amendments replace originals)."""
    key = lambda r: (r["registrant"]["id"], r.get("filer_type"), (r.get("lobbyist") or {}).get("id"),
                     r["filing_year"], "mid" if (r.get("filing_type") or "").startswith("M") else "year_end")
    best = reduce(lambda acc, r: {**acc, key(r): r} if key(r) not in acc or (r.get("dt_posted") or "") > (acc[key(r)].get("dt_posted") or "")
                  else acc, reports, {})
    return tuple(best.values())


PERSON_PAYEE = re.compile(r"(?i)\b(director|staff|senator|congressman|congresswoman)\b")


def redact_ld203(row: Mapping) -> dict:
    """Privacy: honorary-expense and similar non-FECA items name board members and staff; keep the
    organisation-level payee and withhold individual names. FECA items name candidate committees and
    officeholders, which stay as filed."""
    return dict(row) if row["contribution_type"] == "feca" else {
        **row,
        "honoree_name": "[individual names withheld]" if row["honoree_name"] else "",
        "payee_name": "[individual payee withheld]" if PERSON_PAYEE.search(row["payee_name"]) else row["payee_name"]}


def ld203_rows(reports: Sequence[Mapping], entity: str) -> list[dict]:
    return [redact_ld203(r_) for r_ in _ld203_rows_raw(reports, entity)]


def _ld203_rows_raw(reports: Sequence[Mapping], entity: str) -> list[dict]:
    return [{"registrant": r["registrant"]["name"], "registrant_id": r["registrant"]["id"], "linked_target": entity,
             "filing_uuid": r["filing_uuid"], "filing_year": r["filing_year"], "filing_period": r["filing_period"],
             "filing_type": r["filing_type"], "contribution_type": i.get("contribution_type") or "",
             "contributor_name": i.get("contributor_name") or "", "payee_name": i.get("payee_name") or "",
             "honoree_name": i.get("honoree_name") or "", "amount_usd": i.get("amount") or "",
             "contribution_date": i.get("date") or "", "pacs": "; ".join(r.get("pacs") or []),
             "filing_document_url": r.get("filing_document_url") or ""}
            for r in reports if r.get("filer_type") == "organization" and int(r["filing_year"]) >= MIN_YEAR
            for i in r.get("contribution_items") or []]


LD203_COLS = ("registrant", "registrant_id", "linked_target", "filing_uuid", "filing_year", "filing_period",
              "filing_type", "contribution_type", "contributor_name", "payee_name", "honoree_name", "amount_usd",
              "contribution_date", "pacs", "filing_document_url")


def ld203_summary(reports_by_reg: Mapping[tuple, Sequence[Mapping]]) -> list[dict]:
    def one(key: tuple, reps: Sequence[Mapping]) -> dict:
        reps = [r for r in reps if int(r["filing_year"]) >= MIN_YEAR]
        org = [r for r in reps if r.get("filer_type") == "organization"]
        lob = [r for r in reps if r.get("filer_type") == "lobbyist"]
        items = lambda rs: [i for r in rs for i in r.get("contribution_items") or []]
        tot = lambda its, t=None: round(sum(float(i.get("amount") or 0) for i in its
                                            if t is None or i.get("contribution_type") == t), 2)
        return {"registrant_id": key[0], "registrant": key[1], "linked_target": key[2],
                "org_reports": len(org), "org_reports_no_contrib": sum(1 for r in org if r.get("no_contributions")),
                "org_items": len(items(org)), "org_total": tot(items(org)),
                **{f"org_{t}": tot(items(org), t) for t in ("feca", "he", "me", "ple", "pic")},
                "pacs": sorted({p for r in org for p in r.get("pacs") or []}),
                "lobbyist_reports": len(lob), "lobbyist_items": len(items(lob)), "lobbyist_total": tot(items(lob)),
                "years": sorted({r["filing_year"] for r in reps})}
    return [one(k, v) for k, v in sorted(reports_by_reg.items())]


def charity_items(rows: Sequence[Mapping]) -> list[dict]:
    pat = r"charit|foundation|donor|philanthrop|gift fund"
    return [r for r in rows if r["contribution_type"] in ("he", "me", "pic", "ple")
            and re.search(pat, r["payee_name"] + " " + r["honoree_name"], flags=re.I)]


# --------------------------------------------------------------------------------------------------- breach
NOTICES = (  # id, label, entity pattern, reporting-date window used to pick the candidate register entry
    ("BN-VAN-2026", "Vanguard, 2026-07", r"vanguard group", ("2026-07-01", "2026-11-20")),
    ("BN-AMP-2026", "Ameriprise, 2026-03", r"ameriprise", ("2026-03-01", "2026-07-31")),
    ("BN-FID-2024", "Fidelity Investments, 2024-08", r"fidelity investments(?! life)|fidelity brokerage|fidelity management|\bfmr\b", ("2024-08-01", "2025-01-31")),
    ("BN-SCH-2023", "Schwab / TD Ameritrade (MOVEit), 2023-05", r"schwab|ameritrade", ("2023-05-15", "2024-03-31")),
    ("BN-FLI-2023", "Fidelity Investments Life Insurance / Empire Fidelity via Infosys McCamish (IMS), 2023-10", r"fidelity investments life|empire fidelity", ("2024-01-01", "2024-12-31")),
    ("BN-IMS-2023", "Infosys McCamish Systems own notice (the IMS vendor incident behind BN-FLI-2023), 2023-10/11", r"mccamish", ("2024-01-01", "2024-12-31")),
    ("BN-MS-2021", "Morgan Stanley, 2021", r"morgan stanley", ("2021-01-01", "2021-12-31")),
)
DAF_ENTITY = r"fidelity charitable|fidelity investments charitable|schwab charitable|vanguard charitable|" \
             r"global impact funding trust|\bGIFT\b(?! card)|renaissance charitable|\bRCF\b|donor ?first|donor[\s-]*advised|" \
             r"charitable gift fund|daf ?giving ?360|charitable endowment program|national philanthropic trust"
BROAD_CHARITY = r"charit|philanthrop|donor|foundation"
DATA_TYPES = (("name", r"\bnames?\b"), ("address", r"\baddress(es)?\b"), ("SSN", r"social security|\bSSNs?\b"),
              ("date of birth", r"date of birth|\bDOB\b|birth ?date"),
              ("account number", r"account (number|information|numbers)|account no"),
              ("tax ID", r"taxpayer identification|\bTIN\b|tax identification"),
              ("driver's licence / government ID", r"driver'?s licen[cs]e|passport|government[- ]issued|state id"),
              ("phone / email", r"telephone|phone number|e-?mail address"),
              ("financial / balance / transaction", r"balance|transaction|holdings|positions"),
              ("health / insurance", r"medical|health|policy number|insurance"),
              ("username / password", r"user ?name|password|login credential"))
VT_LIST = "https://ago.vermont.gov/categories/security-breach-notices"
MA_LIST = "https://www.mass.gov/lists/data-breach-reports"
MA_YEARS = (2021, 2022, 2023, 2024, 2025, 2026)
MA_DOC = "https://www.mass.gov/doc/data-breach-report-{y}/download"
MONTHS = {m: i for i, m in enumerate(("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), 1)}
DATE_RE = re.compile(r"(\d{1,2})-([A-Za-z]{3})-(\d{2})\b|(\d{1,2})/(\d{1,2})/(\d{4})\b|(\d{1,2})-(\d{1,2})-(\d{4})\b")


def iso_date(m: re.Match) -> str:
    g = m.groups()
    if g[0]:
        return f"20{g[2]}-{MONTHS.get(g[1].lower(), 0):02d}-{int(g[0]):02d}"
    if g[3]:
        return f"{g[5]}-{int(g[3]):02d}-{int(g[4]):02d}"
    return f"{g[8]}-{int(g[6]):02d}-{int(g[7]):02d}"


def strip_html(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def vt_table(page: str) -> list[dict]:
    tab = (re.findall(r"<table.*?</table>", page, flags=re.S) or [""])[0]
    rows = [[strip_html(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, flags=re.S)]
            for r in re.findall(r"<tr.*?</tr>", tab, flags=re.S)]
    head = rows[0] if rows else []
    return [dict(zip(head, r)) for r in rows[1:] if len(r) == len(head)]


def vt_archive(page: str) -> list[dict]:
    return [{"href": h, "title": strip_html(t)}
            for h, t in re.findall(r'<h2 class="margin-0">\s*<a href="(/document/[^"]+)"[^>]*>(.*?)</a>', page, flags=re.S)]


def vt_last_page(page: str) -> int:
    return max([int(x) for x in re.findall(r'href="\?page=(\d+)"', page)] or [0])


def pdf_text(path: str) -> str:
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, timeout=120).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def involved_section(text: str) -> str:
    t = re.sub(r"\s+", " ", text or "")
    m = re.search(r"what information was involved\??(.{0,700}?)(?:what we are doing|what you can do|$)", t, flags=re.I)
    return m.group(1).strip() if m else ""


def data_types(text: str) -> list[str]:
    sec = involved_section(text)
    if not sec:
        return ["(no 'What information was involved' section found)"]
    merge = ["(data elements are a mail-merge field in the posted sample: " + "; ".join(re.findall(r"<<[^>]+>>", sec)) + ")"] \
        if "<<" in sec else []
    return [k for k, p in DATA_TYPES if re.search(p, re.sub(r"<<[^>]+>>", " ", sec), flags=re.I)] + merge


def count_snippets(text: str) -> list[str]:
    t = re.sub(r"\s+", " ", text or "")
    pats = r"[^.]{0,120}\baffected \d[\d,]* (?:Vermont|resident|individual|customer|person|people|participant)s?[^.]{0,80}\.|" \
           r"[^.]{0,120}\b\d[\d,]* Vermont residents?[^.]{0,80}\."
    return [m.strip() for m in re.findall(pats, t, flags=re.I)][:6]


def hits(pat: str, text: str) -> list[str]:
    return sorted({m.group(0) for m in re.finditer(pat, text or "", flags=re.I)})


def match_notice(name: str) -> list[str]:
    return [n[0] for n in NOTICES if re.search(n[2], name or "", flags=re.I)]


def in_window(nid: str, iso: str) -> bool:
    lo, hi = next(n[3] for n in NOTICES if n[0] == nid)
    return lo <= (iso or "") <= hi


# Massachusetts OCABR annual PDF (pdftotext -layout) -------------------------------------------------------
MA_HEADER_LABELS = (("SSN", r"SSN"), ("medical records", r"Medical"), ("financial account", r"Financial"),
                    ("account number", r"Account"), ("driver's licence", r"Drivers"), ("credit/debit card", r"Credit"),
                    ("credit monitoring provided", r"Provided"), ("data encrypted", r"Encrypted|Data"),
                    ("mobile device lost/stolen", r"Mobile"))


def ma_header_cols(line: str) -> list[tuple[str, float]]:
    """Column label -> centre position, from the first header line of a page."""
    found = []
    for lab, pat in MA_HEADER_LABELS:
        m = re.search(r"\b" + pat, line[60:])
        if m and not (lab == "account number" and "Financial" in line) and not (lab == "data encrypted" and "Encrypted" not in line and "Provided" not in line):
            found.append((lab, 60 + m.start() + 4))
    return sorted(found, key=lambda x: x[1])


def ma_is_header(line: str) -> bool:
    return bool(re.search(r"Breached|Reported|Organization Name|Residents|COMMONWEALTH|GOVERNOR|Boylston|total number", line))


def ma_records(text: str, year: int, url: str) -> list[dict]:
    lines = text.splitlines()
    mains = [i for i, l in enumerate(lines) if (m := DATE_RE.search(l)) and m.start() < 45 and not ma_is_header(l)]
    heads = [i for i, l in enumerate(lines) if re.search(r"SSN", l) and re.search(r"Credit", l)]
    main_set = frozenset(mains)

    def wraps(i: int) -> list[str]:
        prev_m = max([k for k in mains if k < i], default=-99)
        next_m = min([k for k in mains if k > i], default=10 ** 9)
        lo = i - 1 if i - 1 > prev_m and not ma_is_header(lines[i - 1]) else i
        hi = i + 1 if i + 1 < next_m and i + 1 < len(lines) and not ma_is_header(lines[i + 1]) else i
        return [(j < i, lines[j]) for j in range(lo, hi + 1) if j != i and j not in main_set]

    def one(i: int) -> dict:
        l = lines[i]
        dm = DATE_RE.search(l)
        rest = l[dm.end():]
        toks = list(re.finditer(r"\S+", rest))
        yn_tail = []
        while toks and toks[-1].group(0) in ("Yes", "No"):
            yn_tail.insert(0, toks.pop())
        cnt = toks.pop() if toks and re.fullmatch(r"\d[\d,]*", toks[-1].group(0)) else None
        before = rest[:cnt.start()] if cnt else rest
        segs = [x for x in re.split(r"\s{2,}", before.strip()) if x]
        name = segs[0] if segs else ""
        nstart = dm.end() + (before.find(name) if name else 0)
        nend = nstart + len(name)
        cut = lambda w: w[max(0, nstart - 6):nend + 6].strip()
        above = [cut(w) for up, w in wraps(i) if up and cut(w)]
        below = [cut(w) for up, w in wraps(i) if not up and cut(w)]
        wrap_txt = above + below
        hdr = max([h for h in heads if h < i], default=heads[0] if heads else None)
        cols = ma_header_cols(lines[hdr]) if hdr is not None else []
        fixed = {5: ("SSN", "medical records", "financial account", "driver's licence", "credit/debit card"),
                 4: ("SSN", "account number", "driver's licence", "credit/debit card")}
        if any(t.group(0) == "No" for t in yn_tail) or year >= 2023:
            labels = fixed.get(len(yn_tail), tuple(f"col{k}" for k in range(len(yn_tail))))
            flags = {lab: t.group(0) for lab, t in zip(labels, yn_tail)}
        else:
            centre = lambda t: dm.end() + (t.start() + t.end()) / 2
            near = lambda t: min(cols, key=lambda c: abs(c[1] - centre(t)))[0] if cols else "?"
            flags = {near(t): "Yes" for t in yn_tail}
        nm = re.sub(r"\s+", " ", " ".join(above + [name] + below)).strip()
        centred = year >= 2024 and above and below
        return {"year_file": year, "date": iso_date(dm), "name": nm, "name_main": nm if centred else name,
                "count": int(cnt.group(0).replace(",", "")) if cnt else None, "flags": flags,
                "breach_no": (re.match(r"\s*(\d{4}-\d+|\d{5})", l) or [None, ""])[1], "raw": re.sub(r"\s+", " ", l).strip(),
                "url": url}
    return [one(i) for i in mains]


def ma_types(flags: Mapping) -> str:
    return "; ".join(k for k, v in flags.items() if v == "Yes" and k not in ("credit monitoring provided", "data encrypted"))


BREACH_COLS = ("notice_id", "notice_label", "register", "register_status", "candidate_for_notice", "entity_named",
               "date_reported", "number_affected_state", "number_affected_stated_in_notice",
               "data_types_register", "data_types_in_notice_text", "daf_entity_named", "daf_terms_found",
               "entries_for_entity_in_window", "matched_on", "source_url", "pdf_url", "evidence")


# --------------------------------------------------------------------------------------------------- runners
def run_robots(get: Callable) -> list[dict]:
    def one(u: str) -> dict:
        s, b = get(u)
        txt = b.decode("utf-8", "replace")
        is_robots = s == 200 and "user-agent" in txt.lower()
        return {"url": u, "status": s, "robots_readable": is_robots,
                "excerpt": re.sub(r"\s+", " ", txt[:300]) if is_robots else strip_html(txt)[:160]}
    return [one(u) for u in ROBOTS] + [{**one(u), "probe": True} for u in PROBES]


def run_lda(root: str, get: Callable, outdir: str) -> dict:
    prior = read_csv(os.path.join(root, IN_CSV))
    prior_uuids = frozenset(r["filing_uuid"] for r in prior)
    tgs = targets_from(prior)
    pulled = tuple(f for t in tgs for f in pull_target(get, t))
    filings = latest_versions(pulled)
    rows = [r for f in filings for r in line_rows(f, prior_uuids)]
    write_csv(os.path.join(root, OUT_LDA), rows, LDA_COLS)
    regs = ld203_registrants(filings)
    reps = {(i, n, e): latest_reports(paged(get, api_url("contributions", registrant_id=i, filing_dt_posted_after=POSTED_AFTER)))
            for i, n, e in regs}
    c_rows = [r for (i, n, e), rs in sorted(reps.items()) for r in ld203_rows(rs, e)]
    write_csv(os.path.join(root, OUT_203), c_rows, LD203_COLS)
    summ = {**summarise_lda(filings, rows), "targets": len({t["entity"] for t in tgs}),
            "queries": len(tgs), "raw_rows": len(pulled),
            "prior_uuids_recovered": len(prior_uuids & {f["filing_uuid"] for f in filings}),
            "prior_uuids": len(prior_uuids),
            "entities_with_zero_filings": sorted({t["entity"] for t in tgs} - {f["_target"]["entity"] for f in filings}),
            "ld203": ld203_summary(reps), "ld203_items": len(c_rows), "ld203_charity_items": charity_items(c_rows),
            "client_names_accepted": sorted({(f["_target"]["entity"], f["client"]["name"]) for f in filings})}
    with open(os.path.join(outdir, "lda_summary.json"), "w") as f:
        json.dump(summ, f, indent=1, default=lambda o: sorted(o) if isinstance(o, set) else str(o))
    return summ


def run_breach(root: str, get: Callable, cache: str, outdir: str, robots: Sequence[Mapping]) -> dict:
    page0 = get(VT_LIST)[1].decode("utf-8", "replace")
    table = vt_table(page0)
    last = vt_last_page(page0)
    pages = [page0] + [get(f"{VT_LIST}?page={n}")[1].decode("utf-8", "replace") for n in range(1, last + 1)]
    archive = [a for p in pages for a in vt_archive(p)]
    org_key = next((k for k in (table[0].keys() if table else []) if "Organization Name" in k), "")
    date_key = next((k for k in (table[0].keys() if table else []) if "Date" in k), "")
    vt_iso = lambda s: iso_date(DATE_RE.search(s)) if DATE_RE.search(s or "") else ""

    def save_pdf(url: str) -> str:
        st, pb = get(url)
        p = cache_path(cache, url, ".pdf")
        if st == 200 and pb[:4] == b"%PDF" and not os.path.exists(p):
            with open(p, "wb") as f:
                f.write(pb)
        return pdf_text(p) if os.path.exists(p) else ""

    def open_doc(a: Mapping) -> dict:
        url = "https://ago.vermont.gov" + a["href"]
        pdfs = re.findall(r'href="([^"]+\.pdf)"', get(url)[1].decode("utf-8", "replace"))
        pdf = urllib.parse.urljoin(url, pdfs[0]) if pdfs else ""
        txt = save_pdf(pdf) if pdf else ""
        with open(os.path.join(outdir, "vt_" + os.path.basename(a["href"]) + ".txt"), "w") as f:
            f.write(txt)
        return {"url": url, "pdf": pdf, "text": txt}

    # Vermont
    vt_tab = [(nid, r, vt_iso(r.get(date_key, ""))) for r in table for nid in match_notice(r.get(org_key, ""))]
    arc_hits = [(nid, a) for a in archive for nid in match_notice(a["title"])]
    docs = {a["href"]: open_doc(a) for _, a in arc_hits}
    vt_rows = ([{"notice_id": nid, "register": "Vermont AGO summary table (reports from 2026-04-17)",
                 "register_status": "listed", "entity_named": r.get(org_key, ""), "date_reported": d,
                 "number_affected_state": r.get("Number of VT Residents Affected", ""),
                 "data_types_register": r.get("Categories of Data Breached", ""),
                 "daf_entity_named": yn(bool(hits(DAF_ENTITY, r.get(org_key, "")))),
                 "daf_terms_found": "; ".join(hits(DAF_ENTITY, r.get(org_key, ""))),
                 "_in": in_window(nid, d), "source_url": VT_LIST, "matched_on": "organisation name",
                 "evidence": " | ".join(f"{k}: {v}" for k, v in r.items())} for nid, r, d in vt_tab]
               + [{"notice_id": nid, "register": "Vermont AGO archived notices (PDF posted, to mid-2026)",
                   "register_status": "listed",
                   "entity_named": re.sub(r"^\d{4}-\d{2}-\d{2}\s*|\s*-?\s*(Data|Date|Security) Breach.*$", "", a["title"]),
                   "date_reported": (re.match(r"\d{4}-\d{2}-\d{2}", a["title"]) or [""])[0],
                   "number_affected_stated_in_notice": " || ".join(count_snippets(docs[a["href"]]["text"])),
                   "data_types_in_notice_text": "; ".join(data_types(docs[a["href"]]["text"])),
                   "daf_entity_named": yn(bool(hits(DAF_ENTITY, docs[a["href"]]["text"]))),
                   "daf_terms_found": "; ".join(hits(DAF_ENTITY, docs[a["href"]]["text"])),
                   "_in": in_window(nid, a["title"][:10]), "matched_on": "notice title",
                   "source_url": docs[a["href"]]["url"], "pdf_url": docs[a["href"]]["pdf"],
                   "evidence": f"title: {a['title']}; pdf text chars={len(docs[a['href']]['text'])}"} for nid, a in arc_hits])

    # Massachusetts
    ma_list_ok = get(MA_LIST)[0] == 200
    ma_texts = {y: save_pdf(MA_DOC.format(y=y)) for y in MA_YEARS} if ma_list_ok else {}
    ma_all = [r for y, t in ma_texts.items() for r in ma_records(t, y, MA_DOC.format(y=y))]
    on_main = lambda nid, r: nid in match_notice(r["name_main"])
    ma_hit0 = [(nid, r) for r in ma_all for nid in match_notice(r["name"])]
    main_dates = {(nid, r["date"]) for nid, r in ma_hit0 if on_main(nid, r)}
    ma_hit = [(nid, r) for nid, r in ma_hit0 if on_main(nid, r) or (nid, r["date"]) not in main_dates]
    ma_rows = [{"notice_id": nid, "register": f"Massachusetts OCABR annual report {r['year_file']}",
                "register_status": "listed", "entity_named": r["name_main"] if on_main(nid, r) else r["name"], "date_reported": r["date"],
                "number_affected_state": r["count"] if r["count"] is not None else "",
                "data_types_register": ma_types(r["flags"]),
                "daf_entity_named": yn(bool(hits(DAF_ENTITY, r["name"]))), "daf_terms_found": "; ".join(hits(DAF_ENTITY, r["name"])),
                "_in": in_window(nid, r["date"]), "_main": on_main(nid, r), "source_url": r["url"],
                "matched_on": "main line" if on_main(nid, r) else "wrapped name line (verify)",
                "evidence": f"name incl. wrapped lines: {r['name']}; breach no {r['breach_no'] or '(wrapped)'}; flags {json.dumps(r['flags'])}; line: {r['raw'][:220]}"}
               for nid, r in ma_hit]

    def mark(rows: list[dict]) -> list[dict]:
        def cnt(r: Mapping) -> int:
            v = str(r.get("number_affected_state") or "").replace(",", "")
            return int(v) if v.isdigit() else -1
        groups = {}
        for r in rows:
            groups.setdefault((r["notice_id"], r["register"].split(" annual")[0].split(" summary")[0].split(" archived")[0]), []).append(r)
        pool = lambda g: [r for r in g if r["_in"] and r.get("_main", True)] or [r for r in g if r["_in"]]
        best = {k: max(pool(g), key=cnt, default=None) for k, g in groups.items()}
        n_in = {k: sum(1 for r in g if r["_in"]) for k, g in groups.items()}
        key = lambda r: (r["notice_id"], r["register"].split(" annual")[0].split(" summary")[0].split(" archived")[0])
        return [{**r, "candidate_for_notice": yn(best[key(r)] is r), "entries_for_entity_in_window": n_in[key(r)]} for r in rows]

    listed = mark(vt_rows + ma_rows)
    have = {(r["notice_id"], st) for r in listed if r["candidate_for_notice"] == "Y"
            for st in (("VT" if r["register"].startswith("Vermont") else "MA"),)}
    status_of = {r["url"]: r for r in robots}
    me, mer = status_of.get(PROBES[0], {}).get("status"), status_of.get("https://www.maine.gov/robots.txt", {}).get("status")
    gaps = ([{"notice_id": n[0], "register": "Maine AG",
              "register_status": f"blocked: HTTP {me} to a generic client; robots.txt HTTP {mer} (unreadable)",
              "source_url": PROBES[0], "evidence": "not retrieved; user agent not changed"} for n in NOTICES]
            + [{"notice_id": n[0], "register": "Vermont AGO (table + archive)", "register_status": "no entry in reporting window",
                "source_url": VT_LIST,
                "evidence": f"/{n[2]}/ within {n[3][0]}..{n[3][1]}: none in {len(table)} table rows or {len(archive)} archived notices"}
               for n in NOTICES if (n[0], "VT") not in have]
            + [{"notice_id": n[0], "register": "Massachusetts OCABR annual reports 2021-2026",
                "register_status": "no entry in reporting window",
                "source_url": MA_LIST, "evidence": f"/{n[2]}/ within {n[3][0]}..{n[3][1]}: none in {len(ma_all)} parsed records"}
               for n in NOTICES if (n[0], "MA") not in have and ma_list_ok])
    labels = {n[0]: n[1] for n in NOTICES}
    rows = sorted(listed + gaps, key=lambda r: (r["notice_id"], r["register"], r.get("date_reported", "")))
    rows = [{**{k: v for k, v in r.items() if not k.startswith("_")}, "notice_label": labels[r["notice_id"]]} for r in rows]
    write_csv(os.path.join(root, OUT_BREACH), rows, BREACH_COLS)
    daf_scan = {"vt_table": [r.get(org_key) for r in table if hits(DAF_ENTITY, r.get(org_key, ""))],
                "vt_archive": [a["title"] for a in archive if hits(DAF_ENTITY, a["title"])],
                "ma": [(r["date"], r["name"]) for r in ma_all if hits(DAF_ENTITY, r["name"])]}
    broad_scan = {"vt_table": [r.get(org_key) for r in table if hits(BROAD_CHARITY, r.get(org_key, ""))],
                  "vt_archive_n": sum(1 for a in archive if hits(BROAD_CHARITY, a["title"])),
                  "ma_n": sum(1 for r in ma_all if hits(BROAD_CHARITY, r["name"])),
                  "ma_charit": sorted({r["name"] for r in ma_all if re.search(r"charit", r["name"], re.I)})}
    summ = {"vt_table_rows": len(table), "vt_table_dates": [min(x for x in (vt_iso(r.get(date_key, "")) for r in table) if x), max(vt_iso(r.get(date_key, "")) for r in table)] if table else [],
            "vt_archive_pages": last + 1, "vt_archive_notices": len(archive),
            "vt_archive_dates": [min((a["title"][:10] for a in archive if re.match(r"20\d\d-", a["title"])), default=""),
                                 max((a["title"][:10] for a in archive if re.match(r"20\d\d-", a["title"])), default="")],
            "ma_records_by_year": {y: sum(1 for r in ma_all if r["year_file"] == y) for y in MA_YEARS},
            "ma_records_no_count": sum(1 for r in ma_all if r["count"] is None),
            "ma_total_lines": {y: (re.search(r"total number of breaches affecting residents:\s*([\d,]+)", t) or [None, ""])[1] for y, t in ma_texts.items()},
            "candidates": [{k: r.get(k, "") for k in ("notice_id", "register", "entity_named", "date_reported", "number_affected_state",
                                              "data_types_register", "entries_for_entity_in_window")}
                           for r in rows if r.get("candidate_for_notice") == "Y"],
            "daf_entity_scan": daf_scan, "broad_charity_scan": broad_scan, "rows": len(rows)}
    with open(os.path.join(outdir, "breach_summary.json"), "w") as f:
        json.dump(summ, f, indent=1, default=str)
    return summ


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--cache", required=True)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--step", default="all", choices=("lda", "breach", "all"))
    a = ap.parse_args(argv)
    os.makedirs(a.cache, exist_ok=True)
    outdir = a.cache
    robots = run_robots(fetch(a.cache, a.offline, 3.0))
    with open(os.path.join(outdir, "robots_log.json"), "w") as f:
        json.dump(robots, f, indent=1)
    if a.step in ("lda", "all"):
        s = run_lda(a.root, fetch(a.cache, a.offline, LDA_DELAY), outdir)
        print(json.dumps({k: s[k] for k in ("filings", "entities", "lines_tagged", "filings_policy_tag",
                                             "filings_adjacent_unnamed", "ld203_items")}))
    if a.step in ("breach", "all"):
        s = run_breach(a.root, fetch(a.cache, a.offline, VT_DELAY), a.cache, outdir, robots)
        print(json.dumps({k: s[k] for k in ("vt_table_rows", "vt_archive_notices", "ma_records_by_year", "candidates")}, default=str, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
