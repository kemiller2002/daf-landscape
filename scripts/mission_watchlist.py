#!/usr/bin/env python3
"""Dated watchlist for DAF vendor moves, sponsor portals, IRS filings and deal closings
(queue items P-GIV-01/02, P-BUY-01, P-ASR-01, P-VEN-02/08/10).

Stdlib only; functional style (pure transforms; network and file I/O at the edges).
Patterns reused from scripts/mission_terms_monitor.py (text extraction, normalisation, dated
snapshots, compare-with-previous, Markdown report, idempotent manifest) and
scripts/mission_990_contractors.py (IRS TEOS e-file index access).

Config: data/mission-2026-11-14/watchlist.csv, one row per check:
  check_id, check_type, entity, queue_items, target, link_regex, watch_regex, params, notes
check_type:
  ct_crtsh        target = crt.sh identity query (leading '%' wildcard only), e.g. %.giveinteractive.com;
                  params name_filter=<regex> narrows names (one cached query serves many checks)
  ct_certspotter  target = domain; currently valid issuances incl. subdomains (params: max_pages)
  http            target = URL; manual redirect chain, final host, <title>, links matching
                  link_regex, 'Powered by' / copyright footers, sentences matching watch_regex
  rss             target = RSS URL (e.g. Google News search); items; flagged items match watch_regex
  sec_efts        target = EDGAR full-text query; params startdt=YYYY-MM-DD; forms=A|B
  irs_index       target = EIN; params min_tax_period=YYYYMM; types=990|990PF
watch_regex: what counts as a signal (CT names, URLs/footers/sentences, RSS titles).

Outputs:
  data/watchlist-snapshots/<date>/<check_id>.json   one observation per check (summary + detail)
  data/watchlist-snapshots/reports/<date>.md        diff report vs the latest earlier snapshot
  data/watchlist-snapshots/manifest.csv             one row per check per date (idempotent per date)

IRS index files (~60-100 MB each) are cached outside the repo: --irs-dir (default
$WATCHLIST_IRS_DIR or ~/.cache/daf-landscape/irs-index). They are re-downloaded when the server's
Last-Modified changes.

Usage:
  python3 scripts/mission_watchlist.py                     # run all checks for today
  python3 scripts/mission_watchlist.py --only ct-give-tmf  # one check (repeatable)
  python3 scripts/mission_watchlist.py --type irs_index    # one check type (repeatable)
  python3 scripts/mission_watchlist.py --report-only       # rebuild today's report from snapshots
Suggested cadence: weekly (P-GIV-01 asks for weekly login checks); IRS checks monthly.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import email.utils
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable, Iterable, Mapping, NamedTuple, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mission_terms_monitor import html_to_text, normalize, sha256  # noqa: E402  (reuse)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "data/mission-2026-11-14/watchlist.csv"
DEFAULT_SNAPDIR = ROOT / "data/watchlist-snapshots"
DEFAULT_IRS_DIR = Path(os.environ.get("WATCHLIST_IRS_DIR", Path.home() / ".cache/daf-landscape/irs-index"))
# Honest, generic client name (no personal contact details). Override with WATCHLIST_UA if a
# site (e.g. SEC) asks automated clients to declare a contact.
USER_AGENT = os.environ.get("WATCHLIST_UA", "daf-landscape-watchlist/1.0 (research; public pages)")
INDEX_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
PP_ORG_URL = "https://projects.propublica.org/nonprofits/organizations/{ein}"
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
MAX_BYTES = 30 * 1024 * 1024
MAX_SET_LINES = 40


class Check(NamedTuple):
    check_id: str
    check_type: str
    entity: str
    queue_items: str
    target: str
    link_regex: str
    watch_regex: str
    params: dict
    notes: str


class Resp(NamedTuple):
    ok: bool
    status: str
    url: str
    headers: dict
    body: bytes
    error: str


# ----------------------------------------------------------------------------- config (pure + read)

def parse_params(s: str) -> dict:
    return dict(kv.split("=", 1) for kv in (p.strip() for p in (s or "").split(";")) if "=" in kv)


def read_checks(path: Path) -> list[Check]:
    with path.open(newline="", encoding="utf-8") as fh:
        return [Check(r["check_id"].strip(), r["check_type"].strip(), r["entity"].strip(),
                      r.get("queue_items", "").strip(), r["target"].strip(), (r.get("link_regex") or "").strip(),
                      (r.get("watch_regex") or "").strip(), parse_params(r.get("params", "")),
                      (r.get("notes") or "").strip())
                for r in csv.DictReader(fh) if r.get("check_id") and r.get("target")]


# ----------------------------------------------------------------------------- HTTP (I/O)

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER_NOREDIR = urllib.request.build_opener(_NoRedirect)


def http_get(url: str, timeout: float, follow: bool = True, accept: str = "*/*") -> Resp:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    opener = urllib.request.build_opener() if follow else _OPENER_NOREDIR
    try:
        with opener.open(req, timeout=timeout) as r:
            body = r.read(MAX_BYTES)
            return Resp(True, str(r.status), r.geturl(), dict(r.headers.items()), body, "")
    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read(MAX_BYTES)
        except Exception:
            pass
        return Resp(False, str(e.code), url, dict(e.headers.items()) if e.headers else {}, body, str(e.reason)[:200])
    except Exception as e:  # DNS, TLS, timeout, reset
        return Resp(False, type(e).__name__, url, {}, b"", str(e)[:200])


def http_retry(url: str, timeout: float, tries: int = 3, **kw) -> Resp:
    r = http_get(url, timeout, **kw)
    for i in range(1, tries):
        if r.ok or r.status in {"404", "403", "410"}:
            break
        time.sleep(3 * i)
        r = http_get(url, timeout, **kw)
    return r


def redirect_chain(url: str, timeout: float, max_hops: int = 10) -> tuple[list[dict], Resp]:
    """Follow redirects by hand so every hop (and its host) is recorded."""
    chain, cur = [], url
    for _ in range(max_hops):
        r = http_get(cur, timeout, follow=False, accept="text/html,*/*;q=0.8")
        loc = {k.lower(): v for k, v in r.headers.items()}.get("location", "")
        chain.append({"url": cur, "status": r.status, "location": loc})
        if r.status in {"301", "302", "303", "307", "308"} and loc:
            cur = urllib.parse.urljoin(cur, loc)
            continue
        return chain, r
    return chain, Resp(False, "too_many_redirects", cur, {}, b"", "")


# ----------------------------------------------------------------------------- HTML parsing (pure)

class _LinkTitle(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[list[str]] = []
        self.title, self._in_title, self._a = "", False, None
        self.meta: dict[str, str] = {}
        self.forms: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self._a = [a["href"], ""]
            self.links.append(self._a)
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and (a.get("name") or a.get("property")):
            self.meta[(a.get("name") or a.get("property")).lower()] = (a.get("content") or "")[:300]
        elif tag == "form" and a.get("action"):
            self.forms.append(a["action"])
        elif tag in {"iframe", "script"} and a.get("src"):
            self.links.append([a["src"], f"<{tag}>"])

    def handle_endtag(self, tag):
        if tag == "a":
            self._a = None
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._a is not None:
            self._a[1] += data


def parse_html(raw: bytes) -> _LinkTitle:
    p = _LinkTitle()
    try:
        p.feed(raw.decode("utf-8", errors="replace"))
        p.close()
    except Exception:
        pass
    return p


def host_of(url: str) -> str:
    return (urllib.parse.urlsplit(url).hostname or "").lower()


def sentences_matching(text: str, rx: str, cap: int = 25) -> list[str]:
    if not rx:
        return []
    pat = re.compile(rx)
    sents = re.split(r"(?<=[.!?])\s+|\n", text)
    return sorted({s.strip()[:300] for s in sents if pat.search(s)})[:cap]


def footers(text: str) -> list[str]:
    pats = [r"[Pp]owered by[^\n]{0,80}", r"(?:Copyright|©)\s*[^\n]{0,100}"]
    return sorted({m.group(0).strip() for p in pats for m in re.finditer(p, text)})[:10]


# ----------------------------------------------------------------------------- observers (I/O -> observation)
# Each returns {"ok", "status", "error", "summary": {...stable, diffable...}, "detail": {...}}

def obs_fail(status: str, error: str, extra: dict | None = None) -> dict:
    return {"ok": False, "status": status, "error": error, "summary": {}, "detail": extra or {}}


def crtsh_rows_to_names(rows: Sequence[Mapping]) -> dict[str, dict]:
    acc: dict[str, dict] = {}
    for r in rows:
        for n in str(r.get("name_value", "")).lower().split("\n"):
            n = n.strip()
            if not n:
                continue
            nb = str(r.get("not_before", ""))[:10]
            cur = acc.get(n, {"first_not_before": nb, "last_not_before": nb, "certs": 0})
            acc[n] = {"first_not_before": min(cur["first_not_before"], nb) if nb else cur["first_not_before"],
                      "last_not_before": max(cur["last_not_before"], nb), "certs": cur["certs"] + 1}
    return dict(sorted(acc.items()))


def names_obs(names: dict[str, dict], c: Check, src_url: str, status: str) -> dict:
    pat = re.compile(c.watch_regex, re.I) if c.watch_regex else None
    hits = sorted(n for n in names if pat and pat.search(n))
    return {"ok": True, "status": status, "error": "", "source_url": src_url,
            "summary": {"names": sorted(names), "watch_hits": hits, "name_count": len(names)},
            "detail": {"names": names}}


def filter_names(names: dict[str, dict], rx: str) -> dict[str, dict]:
    pat = re.compile(rx, re.I) if rx else None
    return {n: v for n, v in names.items() if not pat or pat.search(n)}


def observe_crtsh(c: Check, timeout: float, cache: dict) -> dict:
    """crt.sh only accepts a leading '%' wildcard, so per-tenant checks share one domain-wide query
    (cached for the run) and narrow it with params name_filter=<regex>."""
    url = "https://crt.sh/?" + urllib.parse.urlencode({"q": c.target, "output": "json", **{
        k: v for k, v in c.params.items() if k in {"exclude", "match"}}})
    if url not in cache:
        r = http_retry(url, max(timeout, 90), tries=4, accept="application/json")
        try:
            cache[url] = (r, json.loads(r.body.decode("utf-8") or "[]") if r.ok else None, "")
        except json.JSONDecodeError as e:
            cache[url] = (r, None, str(e)[:200])
    r, rows, err = cache[url]
    if not r.ok:
        return obs_fail(r.status, r.error, {"url": url})
    if rows is None:
        return obs_fail("bad_json", err, {"url": url})
    human = "https://crt.sh/?" + urllib.parse.urlencode({"q": c.target})
    return names_obs(filter_names(crtsh_rows_to_names(rows), c.params.get("name_filter", "")), c, human, r.status)


def observe_certspotter(c: Check, timeout: float) -> dict:
    base = ("https://api.certspotter.com/v1/issuances?" +
            urllib.parse.urlencode({"domain": c.target, "include_subdomains": "true", "expand": "dns_names"}))
    rows, after, status = [], "", "200"
    for _ in range(int(c.params.get("max_pages", "10"))):
        r = http_retry(base + (f"&after={after}" if after else ""), timeout, accept="application/json")
        if not r.ok:
            if not rows:
                return obs_fail(r.status, r.error, {"url": base})
            status = f"partial:{r.status}"
            break
        page = json.loads(r.body.decode("utf-8") or "[]")
        if not page:
            break
        rows += [{"name_value": "\n".join(i.get("dns_names", [])), "not_before": i.get("not_before", "")}
                 for i in page]
        after = page[-1].get("id", "")
    return names_obs(crtsh_rows_to_names(rows), c, base, status)


def observe_http(c: Check, timeout: float) -> dict:
    chain, r = redirect_chain(c.target, timeout)
    final = chain[-1]["url"] if chain else c.target
    base = {"chain": chain, "final_url": final}
    if not r.ok:
        return {**obs_fail(r.status, r.error, base),
                "summary": {"final_host": host_of(final), "final_status": r.status,
                            "chain_hosts": [host_of(h["url"]) for h in chain]}}
    p = parse_html(r.body)
    text = normalize(html_to_text(r.body))
    lrx = re.compile(c.link_regex) if c.link_regex else None
    def link_key(h: str, t: str) -> str:
        return urllib.parse.urljoin(final, h.strip()) + " | " + re.sub(r"\s+", " ", t).strip()[:60]
    links = sorted({link_key(h, t) for h, t in p.links if lrx and (lrx.search(h) or lrx.search(t))})[:60]
    wrx = re.compile(c.watch_regex) if c.watch_regex else None
    hay = [h["url"] for h in chain] + [h["location"] for h in chain] + links + footers(text) + p.forms
    hits = sorted({m.group(0) for s in hay for m in (wrx.finditer(s) if wrx else [])})
    return {"ok": True, "status": r.status, "error": "", "source_url": c.target,
            "summary": {"final_host": host_of(final), "final_status": r.status,
                        "chain_hosts": [host_of(h["url"]) for h in chain],
                        "title": re.sub(r"\s+", " ", p.title).strip()[:200],
                        "links": links, "footers": footers(text),
                        "watch_hits_urls": hits,
                        "watch_sentences": sentences_matching(text, c.watch_regex)},
            "detail": {**base, "form_actions": p.forms[:20], "meta": p.meta, "text_chars": len(text),
                       "text_sha256": sha256(text.encode("utf-8")), "raw_sha256": sha256(r.body)}}


def observe_rss(c: Check, timeout: float) -> dict:
    r = http_retry(c.target, timeout, accept="application/rss+xml,application/xml,*/*")
    if not r.ok:
        return obs_fail(r.status, r.error)
    try:
        root = ET.fromstring(r.body)
    except ET.ParseError as e:
        return obs_fail("bad_xml", str(e)[:200])
    items = [{"title": (i.findtext("title") or "").strip(), "link": (i.findtext("link") or "").strip(),
              "pubDate": (i.findtext("pubDate") or "").strip(),
              "source": (i.findtext("source") or "").strip()} for i in root.iter("item")]

    def iso(d: str) -> str:
        try:
            return email.utils.parsedate_to_datetime(d).date().isoformat()
        except Exception:
            return d[:16]
    pat = re.compile(c.watch_regex) if c.watch_regex else None
    keys = sorted(f"{iso(i['pubDate'])} | {i['title'][:160]}" for i in items)
    flagged = sorted(f"{iso(i['pubDate'])} | {i['title'][:160]}" for i in items if pat and pat.search(i["title"]))
    return {"ok": True, "status": r.status, "error": "", "source_url": c.target,
            "summary": {"items": keys, "watch_hits": flagged, "item_count": len(items)},
            "detail": {"items": items}}


def observe_sec(c: Check, timeout: float, run_date: str) -> dict:
    q = {"q": c.target, "dateRange": "custom", "startdt": c.params.get("startdt", "2001-01-01"), "enddt": run_date}
    if c.params.get("forms"):
        q["forms"] = c.params["forms"].replace("|", ",")
    url = "https://efts.sec.gov/LATEST/search-index?" + urllib.parse.urlencode(q)
    r = http_retry(url, timeout, accept="application/json")
    if not r.ok:
        return obs_fail(r.status, r.error, {"url": url})
    try:
        hits = json.loads(r.body.decode("utf-8")).get("hits", {}).get("hits", [])
    except Exception as e:
        return obs_fail("bad_json", str(e)[:200], {"url": url})
    rows = [{"adsh": h.get("_source", {}).get("adsh", ""), "form": h.get("_source", {}).get("form", ""),
             "file_date": h.get("_source", {}).get("file_date", ""),
             "names": h.get("_source", {}).get("display_names", [])} for h in hits]
    keys = sorted({f"{x['file_date']} | {x['form']} | {x['adsh']} | {'; '.join(x['names'])[:120]}" for x in rows})
    human = "https://efts.sec.gov/LATEST/search-index?" + urllib.parse.urlencode(q)
    return {"ok": True, "status": r.status, "error": "", "source_url": human,
            "summary": {"filings": keys, "hit_count": len(keys)}, "detail": {"hits": rows}}


# -- IRS e-file index (pattern from mission_990_contractors.ensure_indexes / load_index)

def ensure_index(irs_dir: Path, year: int, timeout: float) -> tuple[Path | None, str]:
    irs_dir.mkdir(parents=True, exist_ok=True)
    url, path, side = INDEX_URL.format(y=year), irs_dir / f"index_{year}.csv", irs_dir / f"index_{year}.lastmod"
    head = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(head, timeout=timeout) as r:
            lastmod = r.headers.get("Last-Modified", "")
    except urllib.error.HTTPError as e:
        return (path if path.exists() else None), f"http_{e.code}"
    except Exception as e:
        return (path if path.exists() else None), type(e).__name__
    if path.exists() and side.exists() and side.read_text().strip() == lastmod:
        return path, lastmod
    print(f"  downloading {url}", file=sys.stderr)
    tmp = path.with_suffix(".part")
    urllib.request.urlretrieve(url, tmp)  # noqa: S310 (fixed https IRS URL)
    tmp.replace(path)
    side.write_text(lastmod)
    return path, lastmod


def index_rows(path: Path, ein: str) -> list[dict]:
    with path.open(newline="", encoding="latin-1") as fh:
        return [{"tax_period": d.get("TAX_PERIOD", ""), "return_type": d.get("RETURN_TYPE", ""),
                 "object_id": d.get("OBJECT_ID", ""), "taxpayer_name": d.get("TAXPAYER_NAME", ""),
                 "sub_date": d.get("SUB_DATE", ""), "index_file": path.name}
                for d in csv.DictReader(fh) if re.sub(r"\D", "", d.get("EIN", "")).zfill(9) == ein]


def observe_irs(c: Check, timeout: float, irs_dir: Path, run_date: str, cache: dict) -> dict:
    ein = re.sub(r"\D", "", c.target).zfill(9)
    y = int(run_date[:4])
    years = [int(v) for v in c.params.get("years", "").split("|") if v] or [y - 1, y, y + 1]
    types = set(c.params.get("types", "990").split("|"))
    minp = c.params.get("min_tax_period", "000000")
    rows, lastmods = [], {}
    for yr in years:
        idx = cache.setdefault("irs", {})
        if yr not in idx:
            idx[yr] = ensure_index(irs_dir, yr, timeout)
        path, lm = idx[yr]
        lastmods[str(yr)] = lm
        if path:
            rows += index_rows(path, ein)
    rows = sorted({r["object_id"]: r for r in rows if r["return_type"] in types}.values(),
                  key=lambda r: (r["tax_period"], r["object_id"]))
    target = [r for r in rows if r["tax_period"] >= minp]
    return {"ok": True, "status": "ok", "error": "", "source_url": INDEX_URL.format(y=y),
            "summary": {"returns": [f"{r['tax_period']} | {r['return_type']} | {r['object_id']}" for r in rows],
                        "target_return_present": bool(target), "min_tax_period": minp,
                        "target_returns": [f"{r['tax_period']} | {r['return_type']} | {r['object_id']}" for r in target]},
            "detail": {"rows": rows, "index_last_modified": lastmods,
                       "xml_urls": {r["object_id"]: XML_URL.format(oid=r["object_id"]) for r in target},
                       "propublica": PP_ORG_URL.format(ein=ein)}}


def observe(c: Check, timeout: float, run_date: str, irs_dir: Path, cache: dict) -> dict:
    table: dict[str, Callable[[], dict]] = {
        "ct_crtsh": lambda: observe_crtsh(c, timeout, cache.setdefault("crtsh", {})),
        "ct_certspotter": lambda: observe_certspotter(c, timeout),
        "http": lambda: observe_http(c, timeout),
        "rss": lambda: observe_rss(c, timeout),
        "sec_efts": lambda: observe_sec(c, timeout, run_date),
        "irs_index": lambda: observe_irs(c, timeout, irs_dir, run_date, cache),
    }
    fn = table.get(c.check_type)
    if not fn:
        return obs_fail("bad_type", f"unknown check_type {c.check_type}")
    try:
        return fn()
    except Exception as e:  # keep the run going; record the failure
        return obs_fail("exception", f"{type(e).__name__}: {str(e)[:200]}")


# ----------------------------------------------------------------------------- snapshots (I/O)

def snapshot_dates(snapdir: Path) -> list[str]:
    return sorted(p.name for p in snapdir.glob("????-??-??") if p.is_dir())


def load_snapshot(snapdir: Path, date: str, check_id: str) -> dict | None:
    p = snapdir / date / f"{check_id}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def previous_ok(snapdir: Path, date: str, check_id: str) -> tuple[str, dict] | tuple[None, None]:
    for d in reversed([d for d in snapshot_dates(snapdir) if d < date]):
        s = load_snapshot(snapdir, d, check_id)
        if s and s.get("ok"):
            return d, s
    return None, None


def write_snapshot(snapdir: Path, date: str, c: Check, ob: dict) -> dict:
    rec = {"check_id": c.check_id, "check_type": c.check_type, "entity": c.entity, "queue_items": c.queue_items,
           "target": c.target, "watch_regex": c.watch_regex, "date": date,
           "observed_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **ob}
    (snapdir / date).mkdir(parents=True, exist_ok=True)
    (snapdir / date / f"{c.check_id}.json").write_text(json.dumps(rec, indent=2, sort_keys=True), encoding="utf-8")
    return rec


# ----------------------------------------------------------------------------- compare (pure)

def diff_summary(prev: Mapping | None, cur: Mapping) -> dict:
    if not cur.get("ok"):
        return {"state": "failed", "changes": {}}
    if prev is None:
        return {"state": "baseline", "changes": {}}
    ps, cs = prev.get("summary", {}), cur.get("summary", {})
    changes = {}
    for k in sorted(set(ps) | set(cs)):
        a, b = ps.get(k), cs.get(k)
        if a == b:
            continue
        if isinstance(a, list) or isinstance(b, list):
            sa, sb = set(a or []), set(b or [])
            changes[k] = {"added": sorted(sb - sa), "removed": sorted(sa - sb)}
        else:
            changes[k] = {"from": a, "to": b}
    return {"state": "changed" if changes else "unchanged", "changes": changes}


def signals(rec: Mapping, d: Mapping) -> list[str]:
    """Human-readable signals worth a look (pure)."""
    s, out = rec.get("summary", {}), []
    ch = d.get("changes", {})
    t = rec["check_type"]
    if t.startswith("ct_"):
        if ch.get("names", {}).get("added"):
            out.append("new CT names: " + ", ".join(ch["names"]["added"][:15]))
        if ch.get("watch_hits", {}).get("added"):
            out.append("NEW WATCHED NAME: " + ", ".join(ch["watch_hits"]["added"]))
    elif t == "http":
        for k in ("final_host", "final_status"):
            if k in ch:
                out.append(f"{k} {ch[k].get('from')} -> {ch[k].get('to')}")
        for k in ("watch_hits_urls", "links", "footers", "watch_sentences", "chain_hosts"):
            if ch.get(k, {}).get("added") or ch.get(k, {}).get("removed"):
                out.append(f"{k} changed (+{len(ch[k].get('added', []))}/-{len(ch[k].get('removed', []))})")
    elif t == "rss" and ch.get("watch_hits", {}).get("added"):
        out.append("new flagged headlines: " + " || ".join(ch["watch_hits"]["added"][:5]))
    elif t == "sec_efts" and ch.get("filings", {}).get("added"):
        out.append("new EDGAR hits: " + " || ".join(ch["filings"]["added"][:5]))
    elif t == "irs_index":
        if s.get("target_return_present") and (d.get("state") == "baseline" or "target_return_present" in ch):
            out.append("WATCHED RETURN PRESENT: " + "; ".join(s.get("target_returns", [])))
        if ch.get("returns", {}).get("added"):
            out.append("new index rows: " + "; ".join(ch["returns"]["added"]))
    if d.get("state") == "failed":
        out.append(f"fetch failed ({rec.get('status')}: {rec.get('error', '')[:80]})")
    return out


# ----------------------------------------------------------------------------- report (pure)

def _fmt_list(xs: Sequence, cap: int = MAX_SET_LINES) -> list[str]:
    xs = list(xs)
    return [f"  - `{x}`" for x in xs[:cap]] + ([f"  - ... {len(xs) - cap} more"] if len(xs) > cap else [])


def render_report(date: str, rows: Sequence[Mapping]) -> str:
    n_fail = sum(r["diff"]["state"] == "failed" for r in rows)
    L = [f"# Watchlist diff report: {date}", "",
         f"Generated by `scripts/mission_watchlist.py` from `data/mission-2026-11-14/watchlist.csv`. "
         f"{len(rows)} checks; {len(rows) - n_fail} observed; {n_fail} failed. Snapshots: "
         f"`data/watchlist-snapshots/{date}/`.", "",
         "A certificate name is a configured environment, not a go-live; a headline is a lead, not a fact.", "",
         "## Summary", "",
         "| check_id | type | entity | queue | status | state vs previous | previous | signals |",
         "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        sig = "; ".join(r["signals"]).replace("|", "/")[:300]
        L.append(f"| {r['rec']['check_id']} | {r['rec']['check_type']} | {r['rec']['entity']} | "
                 f"{r['rec']['queue_items']} | {r['rec'].get('status', '')} | {r['diff']['state']} | "
                 f"{r['prev_date'] or ''} | {sig} |")
    L += ["", "## Current observations", ""]
    for r in rows:
        rec, s = r["rec"], r["rec"].get("summary", {})
        L += [f"### {rec['check_id']} ({rec['check_type']}): {rec['entity']}", "",
              f"- target: `{rec['target']}`" + (f" ([source]({rec['source_url']}))" if rec.get("source_url") else ""),
              f"- status: {rec.get('status')} {('- ' + rec['error']) if rec.get('error') else ''}"]
        if rec["check_type"].startswith("ct_"):
            names = rec.get("detail", {}).get("names", {})
            L.append(f"- names: {s.get('name_count', 0)}; watch hits: {', '.join(s.get('watch_hits', [])) or 'none'}")
            L += _fmt_list([f"{n} first {v['first_not_before']} last {v['last_not_before']} ({v['certs']} certs)"
                            for n, v in sorted(names.items(), key=lambda kv: kv[1]['first_not_before'], reverse=True)],
                           cap=25 if len(names) > 25 else len(names))
        elif rec["check_type"] == "http":
            L.append("- redirect chain: " + " -> ".join(f"{h['status']} {h['url']}" for h in rec.get("detail", {}).get("chain", [])))
            L.append(f"- final host: `{s.get('final_host', '')}`; title: {s.get('title', '')}")
            if s.get("links"):
                L.append("- matching links:")
                L += _fmt_list(s["links"], 15)
            if s.get("footers"):
                L.append("- footers: " + " / ".join(s["footers"]))
            if s.get("watch_hits_urls"):
                L.append("- watch hits (URLs/footers): " + ", ".join(s["watch_hits_urls"]))
            if s.get("watch_sentences"):
                L.append("- watch sentences:")
                L += _fmt_list(s["watch_sentences"], 12)
        elif rec["check_type"] == "rss":
            L.append(f"- items: {s.get('item_count', 0)}; flagged:")
            L += _fmt_list(s.get("watch_hits", []), 15)
        elif rec["check_type"] == "sec_efts":
            L.append(f"- hits: {s.get('hit_count', 0)}")
            L += _fmt_list(s.get("filings", []), 15)
        elif rec["check_type"] == "irs_index":
            L.append(f"- watched return (tax_period >= {s.get('min_tax_period')}) present: "
                     f"**{s.get('target_return_present')}**; index Last-Modified: "
                     f"{rec.get('detail', {}).get('index_last_modified', {})}")
            L += _fmt_list(s.get("returns", [])[-8:], 8)
        if r["diff"]["changes"]:
            L.append("- changes vs previous:")
            for k, v in r["diff"]["changes"].items():
                if "added" in v:
                    L += [f"  - {k}: +{len(v['added'])} / -{len(v['removed'])}"]
                    L += ["  " + x for x in _fmt_list(["+ " + a for a in v["added"]] + ["- " + b for b in v["removed"]], 20)]
                else:
                    L.append(f"  - {k}: `{v['from']}` -> `{v['to']}`")
        L.append("")
    return "\n".join(L) + "\n"


MANIFEST_FIELDS = ["date", "check_id", "check_type", "entity", "queue_items", "status", "state",
                   "previous_date", "signals", "error"]


def write_manifest(path: Path, date: str, rows: Iterable[Mapping]) -> None:
    new = [{"date": date, "check_id": r["rec"]["check_id"], "check_type": r["rec"]["check_type"],
            "entity": r["rec"]["entity"], "queue_items": r["rec"]["queue_items"], "status": r["rec"].get("status", ""),
            "state": r["diff"]["state"], "previous_date": r["prev_date"] or "", "signals": " ; ".join(r["signals"]),
            "error": r["rec"].get("error", "")} for r in rows]
    old = []
    if path.exists():
        with path.open(newline="", encoding="utf-8") as fh:
            old = list(csv.DictReader(fh))
    keys = {(n["date"], n["check_id"]) for n in new}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows([o for o in old if (o.get("date"), o.get("check_id")) not in keys] + new)


# ----------------------------------------------------------------------------- main

def evaluate(snapdir: Path, date: str, rec: dict) -> dict:
    pdate, prev = previous_ok(snapdir, date, rec["check_id"])
    d = diff_summary(prev, rec)
    return {"rec": rec, "prev_date": pdate, "diff": d, "signals": signals(rec, d)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--snapshots", type=Path, default=DEFAULT_SNAPDIR)
    ap.add_argument("--irs-dir", type=Path, default=DEFAULT_IRS_DIR)
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--only", action="append", default=[])
    ap.add_argument("--type", action="append", default=[])
    ap.add_argument("--timeout", type=float, default=45.0)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args(argv)

    checks = [c for c in read_checks(a.config)
              if (not a.only or c.check_id in a.only) and (not a.type or c.check_type in a.type)]
    cache: dict = {}
    rows = []
    for c in checks:
        if a.report_only:
            rec = load_snapshot(a.snapshots, a.date, c.check_id)
            if rec is None:
                continue
        else:
            rec = write_snapshot(a.snapshots, a.date, c, observe(c, a.timeout, a.date, a.irs_dir, cache))
            time.sleep(1.0 if c.check_type.startswith("ct_") else 0.2)  # be gentle with crt.sh
        r = evaluate(a.snapshots, a.date, rec)
        print(f"{c.check_id:28s} {str(rec.get('status')):>8s} {r['diff']['state']:10s} {'; '.join(r['signals'])[:120]}",
              file=sys.stderr)
        rows.append(r)
    if not a.report_only:
        write_manifest(a.snapshots / "manifest.csv", a.date, rows)
    # A partial run (--only/--type) merges with any other snapshots already stored for the date.
    done = {r["rec"]["check_id"] for r in rows}
    for c in read_checks(a.config):
        if c.check_id not in done and (rec := load_snapshot(a.snapshots, a.date, c.check_id)):
            rows.append(evaluate(a.snapshots, a.date, rec))
    order = {c.check_id: i for i, c in enumerate(read_checks(a.config))}
    rows.sort(key=lambda r: order.get(r["rec"]["check_id"], 999))
    out = a.snapshots / "reports" / f"{a.date}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_report(a.date, rows), encoding="utf-8")
    print(f"report: {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
