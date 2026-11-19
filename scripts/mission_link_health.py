#!/usr/bin/env python3
"""Citation link-health audit for research/**/*.md (functional style, stdlib only).

Steps
1. Extract every http(s) URL cited in research/**/*.md, with the file, line and the
   sentence (or table cell) it supports.
2. Prioritise: P1 = cited in the industry report, the strategic synthesis or FINAL-STATUS;
   P2 = cited in a direction-*.md file; P3 = the rest, sampled at random (fixed seed)
   to fill the remaining request budget.
3. For every host, read robots.txt before any other request and respect it
   (RFC 9309 longest-match rules; Crawl-delay honoured when larger than 1 s).
   If robots.txt cannot be read (401/403/429/5xx, timeout, connection or proxy error)
   or it disallows the path, the URL is recorded as 'not checked (robots)' and no
   request is sent. A robots.txt that returns 404/410 means "no rules" (RFC 9309 2.3.1.3).
4. Check each URL with HEAD; GET (Range: bytes=0-0, body not read) only if HEAD is
   refused (400/403/405/406/501). Redirects are followed by hand, up to 5 hops,
   and only after robots.txt of each new host allows the target.
5. For 404/410 results, ask the archive.org availability API (only if archive.org's
   robots.txt allows /wayback/available) whether a capture exists.
6. Write the CSV of per-URL results, the markdown report and queue proposals.

Rules: >= 1 s between requests to the same host; generic User-Agent; hard cap on the
total number of HTTP requests (robots.txt and archive.org calls included); crt.sh is
never requested (repository compliance note of 2026-11-15).

Usage:
  python3 scripts/mission_link_health.py            # extract, check, write outputs
  python3 scripts/mission_link_health.py --report-only   # rebuild report from the CSV
"""
import csv
import hashlib
import json
import random
import re
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = "2026-11-19"
OUT_MD = ROOT / f"research/mission-2026-11-14/citation-link-health-{DATE}.md"
OUT_CSV = ROOT / f"data/mission-2026-11-14/citation-link-health-{DATE}.csv"
OUT_OCC = ROOT / f"data/mission-2026-11-14/citation-link-health-{DATE}-headline-occurrences.csv"
META = Path("/tmp/claude-0/-home-user/ed3d1503-0f0d-5a0d-a5e2-85e6e3196309/scratchpad/link-health-meta.json")
OUT_Q = ROOT / "data/mission-2026-11-14/queue-proposals-links19.csv"

HEADLINE_DOCS = (
    "research/DAF-INDUSTRY-REPORT-2026-11.md",
    "research/mission-2026-11-14/strategic-synthesis.md",
    "research/mission-2026-11-14/FINAL-STATUS.md",
)
UA = "Mozilla/5.0 (compatible; link-health-check/1.0)"
UA_TOKEN = "link-health-check"
MAX_REQUESTS = 2495  # 5 requests were spent on a pre-run smoke test
PLAN_BUDGET = 2150          # planned at selection time; the rest absorbs fallbacks/redirects/archive
ARCHIVE_RESERVE = 150
TIMEOUT = 20
MIN_DELAY = 1.0
MAX_CRAWL_DELAY = 10.0      # hosts asking for more are checked at that delay but capped in count
WORKERS = 12
SEED = 20261119
NEVER_REQUEST = ("crt.sh",)
PLACEHOLDER_HOSTS = ("example.com", "example.org", "localhost", "127.0.0.1", "0.0.0.0")
HEAD_REFUSED = {400, 403, 405, 406, 501}

URL_RE = re.compile(r"https?://[^\s<>\"'`|\[\]]+")
TRAIL = ".,;:*_!?'\""


# ---------------------------------------------------------------- extraction (pure)

def cut_unbalanced(u: str) -> str:
    depth = 0
    for i, ch in enumerate(u):
        depth += (ch == "(") - (ch == ")")
        if depth < 0:
            return u[:i]
    return u


def clean_url(raw: str) -> str:
    u = cut_unbalanced(raw)
    while True:
        prev = u
        u = u.rstrip(TRAIL)
        if u.endswith(")") and u.count("(") < u.count(")"):
            u = u[:-1]
        if u.endswith("}") and u.count("{") < u.count("}"):
            u = u[:-1]
        if u == prev:
            return u


def check_key(url: str) -> str:
    return urllib.parse.urldefrag(url)[0]


def split_units(masked: str) -> tuple:
    """Split a masked line into sentence-like units (table cells or sentences)."""
    if masked.lstrip().startswith("|"):
        cells = [c.strip() for c in masked.strip().strip("|").split("|")]
        label = cells[0] if cells else ""
        return tuple((f"{label} | {c}" if i and label else c) for i, c in enumerate(cells))
    return tuple(re.split(r"(?<=[.!?])\s+(?=[A-Z(\[*\"“])", masked.strip()))


REPO_PTR = re.compile(r"\]\((?!⟦)[^)]*\)|\brepo\b|(?<![\w/])(data|research|scripts)/[\w\-./]+|\b[\w\-]+\.(csv|md|py|json)\b")


def line_occurrences(rel: str, n: int, line: str) -> tuple:
    found = [(m.start(), clean_url(m.group(0))) for m in URL_RE.finditer(line)]
    if not found:
        return ()
    urls = [u for _, u in found]
    masked, pos = [], 0
    for i, (start, u) in enumerate(found):
        masked.append(line[pos:start])
        masked.append(f"⟦{i}⟧")
        pos = start + len(u)
    masked.append(line[pos:])
    masked = "".join(masked)
    out = []
    for unit in split_units(masked):
        idx = [int(k) for k in re.findall(r"⟦(\d+)⟧", unit)]
        if not idx:
            continue
        text = re.sub(r"\[([^\]]*)\]\(⟦\d+⟧\)", r"[\1]", unit)
        text = re.sub(r"⟦\d+⟧", "<url>", text)
        text = re.sub(r"<!--.*?-->", "", text).strip()
        co = tuple(check_key(urls[k]) for k in idx)
        has_repo = bool(REPO_PTR.search(re.sub(r"⟦\d+⟧", "", unit)))
        out.extend(
            {"url": urls[k], "key": check_key(urls[k]), "file": rel, "line": n,
             "sentence": text, "co_urls": co, "repo_pointer": has_repo}
            for k in idx
        )
    return tuple(out)


def file_occurrences(path: Path) -> tuple:
    rel = path.relative_to(ROOT).as_posix()
    return tuple(o for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1)
                 for o in line_occurrences(rel, n, line))


def priority_of(files) -> int:
    if any(f in HEADLINE_DOCS for f in files):
        return 1
    if any(Path(f).name.startswith("direction-") for f in files):
        return 2
    return 3


def host_of(url: str) -> str:
    return (urllib.parse.urlsplit(url).hostname or "").lower()


def skip_reason(url: str) -> str:
    h = host_of(url)
    if not h:
        return "not checked (unparseable)"
    if any(h == b or h.endswith("." + b) for b in NEVER_REQUEST):
        return "not checked (crt.sh policy)"
    if any(h == b or h.endswith("." + b) for b in PLACEHOLDER_HOSTS) or re.search(r"[{}<>]|\.\.\.|…", url):
        return "not checked (placeholder)"
    return ""


def select(keys_by_pri: dict, hosts_of: dict) -> tuple:
    """Plan which URLs to check: all P1, all P2, random sample of P3, within PLAN_BUDGET."""
    seen_hosts, chosen, cost = set(), [], 0.0
    rng = random.Random(SEED)
    for pri in (1, 2, 3):
        keys = sorted(keys_by_pri.get(pri, ()))
        if pri == 3:
            rng.shuffle(keys)
        for k in keys:
            c = 1.25 + (0 if hosts_of[k] in seen_hosts else 1)
            if cost + c > PLAN_BUDGET and pri == 3:
                continue
            chosen.append(k)
            seen_hosts.add(hosts_of[k])
            cost += c
    return tuple(chosen)


# ---------------------------------------------------------------- robots (pure)

def parse_robots(text: str) -> dict:
    groups, cur_agents, cur_rules, last_was_agent = [], [], [], False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        field, value = (s.strip() for s in line.split(":", 1))
        field = field.lower()
        if field == "user-agent":
            if not last_was_agent and cur_agents:
                groups.append((cur_agents, cur_rules))
                cur_agents, cur_rules = [], []
            cur_agents.append(value.lower())
            last_was_agent = True
        elif field in ("allow", "disallow", "crawl-delay"):
            if cur_agents:
                cur_rules.append((field, value))
            last_was_agent = False
    if cur_agents:
        groups.append((cur_agents, cur_rules))
    mine = [r for a, r in groups if any(x != "*" and x in UA_TOKEN for x in a)]
    star = [r for a, r in groups if "*" in a]
    rules = [x for g in (mine or star) for x in g]
    delays = [float(v) for f, v in rules if f == "crawl-delay" and re.fullmatch(r"\d+(\.\d+)?", v)]
    return {"rules": tuple((f, v) for f, v in rules if f != "crawl-delay"),
            "delay": max(delays) if delays else 0.0}


def rule_regex(pattern: str):
    anchored = pattern.endswith("$")
    body = re.escape(pattern[:-1] if anchored else pattern).replace(r"\*", ".*")
    return re.compile(body + ("$" if anchored else ""))


def robots_allows(robots: dict, url: str) -> bool:
    parts = urllib.parse.urlsplit(url)
    path = (parts.path or "/") + (("?" + parts.query) if parts.query else "")
    best = (-1, True)
    for field, pat in robots["rules"]:
        if not pat:
            continue
        if rule_regex(pat).match(path) or rule_regex(urllib.parse.unquote(pat)).match(urllib.parse.unquote(path)):
            length = len(pat)
            allow = field == "allow"
            if length > best[0] or (length == best[0] and allow):
                best = (length, allow)
    return best[1]


# ---------------------------------------------------------------- network layer

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def make_net():
    ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt") if Path("/root/.ccr/ca-bundle.crt").exists() \
        else ssl.create_default_context()
    plain = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), NoRedirect())
    follow = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
    state = {"count": 0, "last": {}, "delay": {}}
    glock = threading.Lock()
    hlocks = defaultdict(threading.Lock)
    rlocks = defaultdict(threading.Lock)
    robots_cache = {}

    def take_budget(reserve=0) -> bool:
        with glock:
            if state["count"] >= MAX_REQUESTS - reserve:
                return False
            state["count"] += 1
            return True

    def raw(url, method, follow_redirects=False, headers=None, reserve=0):
        host = host_of(url)
        with glock:
            lock = hlocks[host]
        with lock:
            if not take_budget(reserve):
                return {"status": None, "error": "budget"}
            delay = max(MIN_DELAY, min(state["delay"].get(host, 0.0), MAX_CRAWL_DELAY))
            wait = state["last"].get(host, 0) + delay - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "*/*", **(headers or {})})
            try:
                with (follow if follow_redirects else plain).open(req, timeout=TIMEOUT) as r:
                    body = r.read(200_000) if follow_redirects else b""
                    return {"status": r.status, "location": r.headers.get("Location", ""), "body": body,
                            "final": r.geturl(), "error": ""}
            except urllib.error.HTTPError as e:
                return {"status": e.code, "location": e.headers.get("Location", "") if e.headers else "", "body": b"",
                        "final": url, "error": ""}
            except (socket.timeout, TimeoutError):
                return {"status": None, "error": "timeout"}
            except urllib.error.URLError as e:
                reason = str(e.reason)
                if "timed out" in reason:
                    return {"status": None, "error": "timeout"}
                if "Tunnel connection failed" in reason:
                    return {"status": None, "error": "proxy/connect error: " + reason[:80]}
                return {"status": None, "error": "connection error: " + reason[:80]}
            except Exception as e:  # noqa: BLE001  (record, never crash the audit)
                return {"status": None, "error": f"error: {type(e).__name__}: {str(e)[:60]}"}
            finally:
                state["last"][host] = time.monotonic()

    def robots_for(scheme, host):
        key = f"{scheme}://{host}"
        with glock:
            lock = rlocks[key]
        with lock:
            if key in robots_cache:
                return robots_cache[key]
            r = raw(f"{key}/robots.txt", "GET", follow_redirects=True)
            st = r.get("status")
            if st and 200 <= st < 300:
                rob = {"ok": True, "note": "robots 200", **parse_robots(r["body"].decode("utf-8", "replace"))}
            elif st in (404, 410):
                rob = {"ok": True, "note": f"robots {st} (no rules)", "rules": (), "delay": 0.0}
            elif r.get("error") == "budget":
                rob = {"ok": False, "note": "budget", "rules": (), "delay": 0.0}
            else:
                rob = {"ok": False, "note": f"robots unreadable ({st or r.get('error')})", "rules": (), "delay": 0.0}
            state["delay"][host] = rob["delay"]
            robots_cache[key] = rob
            return rob

    def gate(url):
        p = urllib.parse.urlsplit(url)
        rob = robots_for(p.scheme, host_of(url))
        if rob["note"] == "budget":
            return False, "not checked (budget)"
        if not rob["ok"]:
            return False, "not checked (robots: " + rob["note"] + ")"
        if not robots_allows(rob, url):
            return False, "not checked (robots: disallowed)"
        return True, rob["note"]

    def check(url, get_only=False):
        hops, cur, method_used = [], url, ""
        for _ in range(6):
            if skip_reason(cur):
                return {"outcome": skip_reason(cur), "http_status": "", "final_url": cur, "hops": hops, "method": method_used}
            ok, note = gate(cur)
            if not ok:
                return {"outcome": note if not hops else note.replace("not checked", "redirect target not checked"),
                        "http_status": "", "final_url": cur, "hops": hops, "method": method_used}
            r = raw(cur, "GET", headers={"Range": "bytes=0-0"}) if get_only else raw(cur, "HEAD")
            method_used = "GET (confirm)" if get_only else "HEAD"
            if not get_only and r.get("status") in HEAD_REFUSED:
                r = raw(cur, "GET", headers={"Range": "bytes=0-0"})
                method_used = "HEAD->GET"
            st = r.get("status")
            if st is None:
                out = "not checked (budget)" if r["error"] == "budget" else r["error"]
                return {"outcome": out, "http_status": "", "final_url": cur, "hops": hops, "method": method_used}
            if 300 <= st < 400 and r.get("location"):
                hops.append(st)
                cur = urllib.parse.urljoin(cur, r["location"])
                continue
            return {"outcome": "http", "http_status": st, "final_url": cur, "hops": hops, "method": method_used}
        return {"outcome": "redirect loop (>5 hops)", "http_status": "", "final_url": cur, "hops": hops, "method": method_used}

    def archive(url):
        ok, note = gate("https://archive.org/wayback/available")
        if not ok:
            return "archive not checked (" + note + ")"
        r = raw("https://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe=""), "GET",
                follow_redirects=True)
        if r.get("status") != 200:
            return f"archive unreachable ({r.get('status') or r.get('error')})"
        try:
            snap = json.loads(r["body"].decode("utf-8", "replace")).get("archived_snapshots", {}).get("closest")
        except ValueError:
            return "archive unreachable (bad JSON)"
        if snap and snap.get("available"):
            return f"capture {snap.get('timestamp', '')} {snap.get('url', '')}"
        return "no capture"

    return {"check": check, "archive": archive, "count": lambda: state["count"], "robots": robots_cache}


# ---------------------------------------------------------------- classification (pure)

def trivial_move(a: str, b: str) -> bool:
    pa, pb = urllib.parse.urlsplit(a), urllib.parse.urlsplit(b)
    norm = lambda p: (re.sub(r"^www\.", "", (p.hostname or "").lower()), p.path.rstrip("/") or "/", p.query)  # noqa: E731
    return norm(pa) == norm(pb)


def classify(url: str, res: dict) -> dict:
    out, st, final = res["outcome"], res["http_status"], res["final_url"]
    if out != "http":
        if out.startswith("not checked (robots") or out.startswith("redirect target not checked (robots"):
            cat = "robots-blocked"
        elif out.startswith("not checked") or out.startswith("redirect target not checked"):
            cat = "not checked"
        elif out == "timeout":
            cat = "timeout"
        else:
            cat = "connection error"
        return {"category": cat, "detail": out}
    if 200 <= st < 300:
        if not res["hops"]:
            return {"category": "alive", "detail": f"{st}"}
        moved = not trivial_move(url, final)
        homepage = moved and (urllib.parse.urlsplit(final).path in ("", "/")) and urllib.parse.urlsplit(url).path not in ("", "/")
        return {"category": "moved" if moved else "alive",
                "detail": f"{'/'.join(map(str, res['hops']))} -> {st}" + (" (redirect to homepage: possible soft 404)" if homepage else "")}
    if st in (404, 410):
        return {"category": "dead", "detail": f"{st}" + (f" after {'/'.join(map(str, res['hops']))}" if res["hops"] else "")}
    if st in (401, 403, 429, 451) or 400 <= st < 500:
        return {"category": "4xx other", "detail": f"{st}"}
    return {"category": "5xx", "detail": f"{st}"}


# ---------------------------------------------------------------- outputs

CSV_FIELDS = ("url", "priority", "checked", "category", "http_status", "detail", "method", "final_url",
              "archive", "n_citations", "n_files", "headline_docs", "first_cited_at")


def build_rows(keys, occ_by_key, results, archives, chosen):
    rows = []
    for k in keys:
        occ = occ_by_key[k]
        files = sorted({o["file"] for o in occ})
        res = results.get(k)
        if res is None:
            reason = skip_reason(k) or "not checked (not sampled)"
            res = {"outcome": reason, "http_status": "", "final_url": k, "hops": [], "method": ""}
        c = classify(k, res)
        rows.append({
            "url": k, "priority": priority_of(files), "checked": "yes" if k in results and res["outcome"] == "http" else "no",
            "category": c["category"], "http_status": res["http_status"], "detail": c["detail"],
            "method": res.get("method", ""), "final_url": res["final_url"] if res["final_url"] != k else "",
            "archive": archives.get(k, ""), "n_citations": len(occ), "n_files": len(files),
            "headline_docs": ";".join(f for f in files if f in HEADLINE_DOCS),
            "first_cited_at": f"{occ[0]['file']}:{occ[0]['line']}",
        })
    return rows


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


CATS = ("alive", "moved", "dead", "4xx other", "5xx", "timeout", "connection error", "robots-blocked", "not checked")


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "n/a"


def summary_table(rows, label_fn, labels):
    checked = [r for r in rows if r["category"] != "not checked"]
    head = "| Group | Attempted | " + " | ".join(CATS[:-1]) + " | Not attempted |\n|---|" + "---|" * (len(CATS) + 1)
    lines = [head]
    for lab in labels:
        grp = [r for r in rows if label_fn(r) == lab]
        att = [r for r in grp if r["category"] != "not checked"]
        cnt = Counter(r["category"] for r in grp)
        cells = " | ".join(f"{cnt[c]} ({pct(cnt[c], len(att))})" for c in CATS[:-1])
        lines.append(f"| {lab} | {len(att)} of {len(grp)} | {cells} | {cnt['not checked']} |")
    return "\n".join(lines), len(checked)


def md_escape(s):
    return s.replace("|", "\\|").replace("\n", " ")


SOURCE_LIST = re.compile(r"^[-*]\s.{0,240}:\s*<url>\s*$")


def is_source_list(occ) -> bool:
    return bool(SOURCE_LIST.match(occ["sentence"].strip()))


def verdict_for(occ, status_of):
    if is_source_list(occ):
        return "source-list entry (not a claim)"
    others = [u for u in dict.fromkeys(str(occ["co_urls"]).split()) if u != occ["key"]]
    other_cats = [status_of.get(u, "not checked") for u in others]
    dead_like = ("dead",)
    if not others:
        base = "only external source dead"
    elif all(c in dead_like for c in other_cats):
        base = "all external sources dead"
    elif any(c in ("alive", "moved") for c in other_cats):
        base = "another cited source alive"
    else:
        base = "co-sources unverified (" + ", ".join(sorted(set(other_cats))) + ")"
    if base.endswith("dead"):
        base += "; repo pointer present" if str(occ["repo_pointer"]) == "True" else "; NO repo pointer"
    return base


def write_report(rows, occ_rows, meta):
    n = len(rows)
    status_of = {r["url"]: r["category"] for r in rows}
    arch_of = {r["url"]: r["archive"] for r in rows}
    http_of = {r["url"]: r["detail"] for r in rows}
    pri_label = {"1": "P1 headline docs", "2": "P2 direction-*.md", "3": "P3 other (sampled)"}
    tbl_pri, n_att = summary_table(rows, lambda r: pri_label[str(r["priority"])], list(pri_label.values()))
    tbl_all, _ = summary_table(rows, lambda r: "All URLs", ["All URLs"])
    att = [r for r in rows if r["category"] != "not checked"]
    cnt = Counter(r["category"] for r in att)
    notc = Counter(r["detail"] for r in rows if r["category"] == "not checked")
    robots_notes = Counter(r["detail"] for r in rows if r["category"] == "robots-blocked")
    four = Counter(r["http_status"] for r in att if r["category"] == "4xx other")
    soft = sum(1 for r in att if "soft 404" in r["detail"])

    dead_occ = [o for o in occ_rows if status_of.get(o["key"]) == "dead"]
    dead_occ.sort(key=lambda o: (o["file"], int(o["line"])))
    dead_lines = []
    flagged = []
    for o in dead_occ:
        v = verdict_for(o, status_of)
        if "NO repo pointer" in v and ("only" in v or "all" in v):
            flagged.append((o, v))
        dead_lines.append(f"| {Path(o['file']).name}:{o['line']} | {md_escape(o['key'])} | {http_of[o['key']]} | "
                          f"{md_escape(o['sentence'][:320])}{'…' if len(o['sentence']) > 320 else ''} | {v} | "
                          f"{md_escape(arch_of.get(o['key'], '') or '—')} |")
    dead_head_urls = sorted({o["key"] for o in dead_occ})

    hl_blocked = sorted({o["key"] for o in occ_rows if status_of.get(o["key"]) in ("robots-blocked", "4xx other", "5xx", "timeout", "connection error")})
    hl_blocked_tbl = "\n".join(
        f"| {md_escape(u)} | {status_of[u]} | {md_escape(http_of[u])} |" for u in hl_blocked)
    moved_hl = sorted({o["key"] for o in occ_rows if status_of.get(o["key"]) == "moved"})
    moved_rows = {r["url"]: r for r in rows}
    moved_tbl = "\n".join(f"| {md_escape(u)} | {md_escape(moved_rows[u]['final_url'])} | {md_escape(moved_rows[u]['detail'])} |" for u in moved_hl)

    dead_all = [r for r in rows if r["category"] == "dead"]
    arch_cnt = Counter(("capture" if r["archive"].startswith("capture") else (r["archive"] or "not looked up").split(" (")[0]) for r in dead_all)
    host_dead = Counter(host_of(r["url"]) for r in dead_all).most_common(10)

    flag_txt = "\n".join(
        f"- **{Path(o['file']).name}:{o['line']}** — {md_escape(o['sentence'][:400])} — dead source: {md_escape(o['key'])} ({v}; "
        f"archive: {md_escape(arch_of.get(o['key'], '') or 'not looked up')})" for o, v in flagged) or "- None found among checked URLs."

    md = f"""# Citation link health, {DATE}

**What this is.** A mechanical check of whether the web pages cited in `research/**/*.md` still respond, run on {DATE} by [`scripts/mission_link_health.py`](../../scripts/mission_link_health.py). Per-URL results: [`citation-link-health-{DATE}.csv`](../../data/mission-2026-11-14/citation-link-health-{DATE}.csv). Headline-document citations with their sentences: [`citation-link-health-{DATE}-headline-occurrences.csv`](../../data/mission-2026-11-14/citation-link-health-{DATE}-headline-occurrences.csv). Queue proposals: [`queue-proposals-links19.csv`](../../data/mission-2026-11-14/queue-proposals-links19.csv).

A live URL does not mean the page still says what the research says it says. This audit tests reachability only, not content.

## Method
- **Extraction.** Every `http(s)://` string in {meta['n_files']} markdown files under `research/` was extracted, cleaned of trailing punctuation and unbalanced brackets, and de-duplicated without the `#fragment`. This gives **{n:,} unique URLs** from {meta['n_occ']:,} citations. (FINAL-STATUS counted 3,424 with a simpler regex.)
- **Priority.** P1: cited in the industry report, the strategic synthesis or FINAL-STATUS ({meta['n_p'][1]} URLs). P2: cited in a `direction-*.md` file and not P1 ({meta['n_p'][2]}). P3: everything else ({meta['n_p'][3]}), randomly sampled with seed {SEED} to fill the request budget.
- **Robots first.** For each host, `robots.txt` was fetched before any other request (one GET per scheme and host). Rules were applied by RFC 9309 longest match for the `*` group (no group names this checker). Crawl-delay was honoured up to {MAX_CRAWL_DELAY:.0f} s. A `robots.txt` returning 404/410 means no rules (RFC 9309 §2.3.1.3). Any other failure (401/403/429/5xx, timeout, proxy or connection error) means **not checked (robots)**: no further request went to that host.
- **Check.** HEAD first. GET with `Range: bytes=0-0` only when HEAD was refused (400/403/405/406/501), and the body was not read. Redirects were followed by hand up to 5 hops, and only after the new host's `robots.txt` allowed the target. A redirect to a different path or host counts as **moved**. A redirect that only changes http→https, `www.` or a trailing slash counts as **alive**.
- **Archive.** For 404/410 results, the archive.org availability API (`/wayback/available`) was queried, after checking archive.org's `robots.txt`.
- **Limits.** At least {MIN_DELAY:.0f} s between requests to one host; generic User-Agent `{UA}`; {TIMEOUT} s timeout; hard cap of {MAX_REQUESTS:,} HTTP requests including robots.txt and archive calls. **{meta['requests']:,} requests were sent.** crt.sh was never requested (compliance note of 2026-11-15). No logins and no forms.

## Summary
Shares below are of URLs **attempted** (robots-blocked counts as attempted: robots.txt was read or failed, and the URL was then withheld). "Not attempted" means not sampled, out of budget, crt.sh, or a placeholder.

{tbl_all}

{tbl_pri}

- **Alive:** {cnt['alive']} of {len(att)} attempted ({pct(cnt['alive'], len(att))}); **moved** (redirected to a new location that answers 2xx): {cnt['moved']} ({pct(cnt['moved'], len(att))}). Of the moved URLs, {soft} redirect a deep link to a site homepage, a likely soft 404.
- **Dead (404/410):** {cnt['dead']} ({pct(cnt['dead'], len(att))}). Archive lookups for dead URLs: {', '.join(f'{k}: {v}' for k, v in arch_cnt.most_common()) or 'none'}.
- **Other 4xx:** {cnt['4xx other']} ({', '.join(f'{k}: {v}' for k, v in sorted(four.items(), key=lambda x: -x[1])) or 'none'}). Hosts: {', '.join(f'{h} ({c})' for h, c in Counter(host_of(r['url']) for r in att if r['category'] == '4xx other').most_common(8))}. A 403 usually means a bot or access wall, not a missing page, so these are not counted as dead.
- **5xx:** {cnt['5xx']}; **timeouts:** {cnt['timeout']}; **connection or proxy errors:** {cnt['connection error']}.
- **Robots-blocked:** {cnt['robots-blocked']} ({pct(cnt['robots-blocked'], len(att))}). By reason: {'; '.join(f'{k}: {v}' for k, v in robots_notes.most_common(8))}.
- **Not attempted:** {sum(notc.values())} ({'; '.join(f'{k}: {v}' for k, v in notc.most_common())}).
- Hosts with the most dead URLs: {', '.join(f'{h} ({c})' for h, c in host_dead) or 'none'}.

## Dead links in the headline documents
{len(dead_head_urls)} unique dead URLs are cited {len(dead_occ)} times in the industry report, the strategic synthesis and FINAL-STATUS. The "Sentence" column is the sentence or table cell that carries the citation (`<url>` marks where the link stood). The "Other sources" column says whether the same sentence also cites a live URL or a repository file.

| Location | Dead URL | Status | Sentence | Other sources | Archive |
|---|---|---|---|---|---|
{chr(10).join(dead_lines) or '| — | none | | | | |'}

### Headline claims whose only external source is now dead and that carry no repository pointer
{flag_txt}

### Headline-document URLs that could not be confirmed (robots, access wall, server error, timeout)
These are not evidence that a link is dead. They are listed so a person can check them in a browser.

| URL | Category | Detail |
|---|---|---|
{hl_blocked_tbl or '| none | | |'}

### Headline-document URLs that redirect to a new location
| Cited URL | Final URL | Hops |
|---|---|---|
{moved_tbl or '| none | | |'}

## Limitations
- **Reachability, not content.** A 2xx response does not confirm that the page still supports the claim. Redirects to homepages and "page not found" pages served with a 200 status (soft 404s) are flagged only when the redirect itself lands on `/`.
- **HEAD-first bias.** Some servers answer HEAD differently from GET. GET was used only when HEAD was refused, to keep within the request cap.
- **Access walls are not dead links.** 401/403/429 responses (EDGAR, ProPublica, Cloudflare and similar) and robots.txt files that could not be read are reported separately. They need a browser check, not a re-source.
- **Sampling.** P3 URLs were sampled at random to fit the {MAX_REQUESTS:,}-request cap. P3 shares are estimates for the unsampled remainder. P1 and P2 were attempted in full, except where the budget ran out (see "Not attempted").
- **Robots strictness.** Hosts whose `robots.txt` could not be read were not checked at all, so results for those hosts are unknown. Robots rules apply to the `*` group, because no group names this checker.
- **Single run.** Transient outages and rate limits on {DATE} may show as timeouts or 5xx. One re-run would separate them from persistent failures.
- **Proxy.** Requests went through the session's egress proxy. A proxy refusal (CONNECT 403/502) is recorded as a connection or proxy error, not as a site response.
- **Sentence attribution.** Sentences are split mechanically on punctuation, or by table cell. A claim may also be supported by text on neighbouring lines that this audit does not see.
"""
    OUT_MD.write_text(md, encoding="utf-8")
    return {"flagged": flagged, "dead_head": dead_head_urls, "hl_blocked": hl_blocked, "cnt": cnt, "att": len(att),
            "notc": notc, "dead_all": dead_all}


def write_queue(rows, rep):
    q = []
    def add(question, area, imp, pc, gap, com, av, eff, concl, rationale, ptr):
        q.append({"question_id": f"P-LNK19-{len(q) + 1:02d}", "question": question, "area": area, "importance": imp,
                  "p_change": pc, "gap": gap, "commercial": com, "availability": av, "effort": eff, "depends_on": "",
                  "breadth_gap": "no", "state": "open", "assigned_to": "", "conclusion_affected": concl,
                  "proposed_by": "citation link-health agent", "rationale": rationale, "evidence_pointer": ptr})
    ptr = f"data/mission-2026-11-14/citation-link-health-{DATE}.csv; research/mission-2026-11-14/citation-link-health-{DATE}.md"
    if rep["flagged"]:
        locs = "; ".join(sorted({f"{Path(o['file']).name}:{o['line']}" for o, _ in rep["flagged"]}))[:600]
        add(f"Re-source the {len(rep['flagged'])} headline-document claims whose only external citation now returns 404/410 and that cite no repository file ({locs}). Use the archive.org capture where one exists, or a live replacement source.",
            "Data quality / citations", 4, 0.3, 4, 2, 4, 2, "Industry report and strategic synthesis sentences listed in the link-health report",
            f"{len(rep['flagged'])} headline citations rest on a single dead URL with no repository pointer", ptr)
    if rep["dead_head"]:
        add(f"Replace or add archive links for all {len(rep['dead_head'])} dead URLs cited in the industry report, strategic synthesis and FINAL-STATUS. Record the archive.org capture timestamp next to each citation.",
            "Data quality / citations", 3, 0.2, 3, 2, 4, 2, "Citation durability of headline documents",
            f"{len(rep['dead_head'])} unique headline URLs returned 404/410 on {DATE}", ptr + " category=dead")
    if rep["hl_blocked"]:
        add(f"Check in a browser the {len(rep['hl_blocked'])} headline-document URLs that this audit could not confirm (robots.txt unreadable or disallowing, 401/403/429, 5xx, timeout). Record whether each still supports its sentence.",
            "Data quality / citations", 3, 0.2, 3, 2, 4, 2, "Headline citations of unknown status",
            "Automated check stopped at robots.txt or an access wall; no claim about these links is possible without a manual check", ptr)
    dead_rest = [r for r in rep["dead_all"] if r["priority"] != "1"]
    if dead_rest:
        add(f"Triage the {len(dead_rest)} dead (404/410) URLs cited in direction-*.md and other research files: add the archive.org capture, or mark the claim unverified where none exists.",
            "Data quality / citations", 2, 0.2, 3, 1, 4, 3, "Supporting research documents",
            f"{len(dead_rest)} dead URLs outside headline docs", ptr + " category=dead priority=2,3")
    if rep["notc"].get("not checked (not sampled)", 0) or rep["notc"].get("not checked (budget)", 0):
        k = rep["notc"].get("not checked (not sampled)", 0) + rep["notc"].get("not checked (budget)", 0)
        add(f"Extend the link-health check to the {k} research URLs that were not sampled or were left out by the request budget, in a later run with a fresh budget.",
            "Data quality / citations", 2, 0.1, 2, 1, 5, 2, "Coverage of citation audit",
            "The 2026-11-19 run checked headline and direction citations in full and sampled the rest", ptr + " category='not checked'")
    fields = ("question_id,question,area,importance,p_change,gap,commercial,availability,effort,depends_on,breadth_gap,"
              "state,assigned_to,conclusion_affected,proposed_by,rationale,evidence_pointer").split(",")
    write_csv(OUT_Q, fields, q)
    return len(q)


# ---------------------------------------------------------------- main

def extract():
    files = sorted(p for p in (ROOT / "research").rglob("*.md") if not p.name.startswith(f"citation-link-health-{DATE}"))
    occ = tuple(o for p in files for o in file_occurrences(p))
    occ_by_key = defaultdict(list)
    for o in occ:
        occ_by_key[o["key"]].append(o)
    return files, occ, occ_by_key


OCC_FIELDS = ("file", "line", "key", "sentence", "co_urls", "repo_pointer")


def main(argv):
    files, occ, occ_by_key = extract()
    keys = sorted(occ_by_key)
    pri = {k: priority_of({o["file"] for o in occ_by_key[k]}) for k in keys}
    headline_occ = [{"file": o["file"], "line": o["line"], "key": o["key"], "sentence": o["sentence"],
                     "co_urls": " ".join(o["co_urls"]), "repo_pointer": o["repo_pointer"]}
                    for o in occ if o["file"] in HEADLINE_DOCS]
    meta = {"n_files": len(files), "n_occ": len(occ), "n_p": Counter(pri.values())}
    if "--report-only" in argv:
        rows = read_csv(OUT_CSV)
        meta["requests"] = int(json.loads((META).read_text())["requests"])
    else:
        checkable = [k for k in keys if not skip_reason(k)]
        by_pri = defaultdict(list)
        for k in checkable:
            by_pri[pri[k]].append(k)
        chosen = select(by_pri, {k: host_of(k) for k in checkable})
        print(f"{len(keys)} unique URLs; P1={meta['n_p'][1]} P2={meta['n_p'][2]} P3={meta['n_p'][3]}; planned {len(chosen)}", flush=True)
        net = make_net()
        results = {}
        for phase in (1, 2, 3):
            groups = defaultdict(list)
            for k in chosen:
                if pri[k] == phase:
                    groups[host_of(k)].append(k)
            def run_group(urls):
                return [(u, net["check"](u)) for u in urls]
            with ThreadPoolExecutor(WORKERS) as ex:
                for part in ex.map(run_group, sorted(groups.values(), key=len, reverse=True)):
                    results.update(part)
            print(f"phase {phase} done: {len(results)} results, {net['count']()} requests", flush=True)
        dead = [k for k, r in results.items() if r["outcome"] == "http" and r["http_status"] in (404, 410)]
        dead.sort(key=lambda k: pri[k])
        archives = {k: net["archive"](k) for k in dead}
        print(f"archive lookups: {len(archives)}; total requests {net['count']()}", flush=True)
        rows = build_rows(keys, occ_by_key, results, archives, chosen)
        write_csv(OUT_CSV, CSV_FIELDS, rows)
        meta["requests"] = net["count"]()
        META.write_text(json.dumps({"requests": meta["requests"],
                                                                  "robots_hosts": len(net["robots"])}))
    for r in rows:
        r["priority"] = str(r["priority"])
    write_csv(OUT_OCC, OCC_FIELDS, headline_occ)
    rep = write_report(rows, headline_occ, meta)
    nq = write_queue(rows, rep)
    print(f"report: {OUT_MD.relative_to(ROOT)}; dead={rep['cnt']['dead']} of {rep['att']} attempted; "
          f"headline dead URLs={len(rep['dead_head'])}; flagged claims={len(rep['flagged'])}; queue rows={nq}")


if __name__ == "__main__":
    main(sys.argv[1:])
