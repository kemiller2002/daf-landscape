#!/usr/bin/env python3
"""b50-04: giving circles hosted on DAF / fund infrastructure (stdlib, functional).

Usage (run from repo root; pass '.' as ROOT):
  python3 -I scripts/mission_b50_04_giving_circles.py . sample  OUT_DIR
      systematic 1-in-3 sample of the top-100 community foundations (by FY2024 DAF
      assets) from data/mission-2026-11-14/cf-vendor-map-by-ein-v2.csv -> OUT_DIR/sample.csv
  python3 -I scripts/mission_b50_04_giving_circles.py . discover OUT_DIR
      for each sampled CF: robots.txt check (all Claude agents + '*' + our UA, with
      wildcard support), sitemap / homepage link discovery of giving-circle URLs,
      fetch of up to MAX_PAGES candidate pages, keyword-sentence extraction.
      Writes OUT_DIR/robots-log.csv, OUT_DIR/candidates.csv, OUT_DIR/text/*.txt
  python3 -I scripts/mission_b50_04_giving_circles.py . fetch OUT_DIR URL [URL...]
      robots-checked fetch of named URLs (national sponsors, research reports);
      appends to OUT_DIR/robots-log.csv and writes OUT_DIR/text/*.txt

Rules honoured: generic UA 'research-script/1.0'; robots disallow for ClaudeBot,
anthropic-ai, Claude-User, Claude-Web or Claude-SearchBot is treated as binding;
robots unreachable / non-200 / non-404 => blocked; hard off-limits hosts never contacted.
"""
import csv
import datetime
import hashlib
import html
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from functools import lru_cache, reduce
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

UA = "research-script/1.0"
AGENTS = ("*", UA, "ClaudeBot", "anthropic-ai", "Claude-User", "Claude-Web", "Claude-SearchBot")
OFF_LIMITS = ("fcsuite.com", "www.foundant.com", "dev.foundant.com", "help.foundant.com",
              "secure.ncfgiving.com", "www.ncfgiving.com", "ncfgiving.com", "donorportal.cct.org",
              "www.charitynavigator.org", "sec.gov", "crt.sh", "certspotter")
CTX = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt"))
CF_LIST = "data/mission-2026-11-14/cf-vendor-map-by-ein-v2.csv"
URL_PAT = re.compile(r"circle|collective-giving|giving-together|givingtogether|collective_giving", re.I)
KEY_PAT = re.compile(r"circle|minimum|fee|advis|recommend|vote|voting|pool|member|collective|"
                     r"fiscal|sponsor|grant|\$\s?\d", re.I)
MAX_PAGES = 6
MAX_SITEMAPS = 25


def off_limits(host):
    return any(host == h or host.endswith("." + h) or h in host for h in OFF_LIMITS)


def http_get(url, timeout=40):
    if off_limits(urlparse(url).netloc.lower()):
        return 999, b"", ""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.status, r.read(4_000_000), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, b"", ""
    except Exception as e:  # network error => status 0
        return 0, str(e)[:120].encode(), ""


# ---------- robots.txt (RFC 9309 style, wildcard + $ aware, longest match wins) ----------

def parse_groups(text):
    """Return tuple of (agents tuple, rules tuple[(allow:bool, pattern)])."""
    lines = [l.split("#", 1)[0].strip() for l in text.splitlines()]
    kv = [(l.split(":", 1)[0].strip().lower(), l.split(":", 1)[1].strip()) for l in lines if ":" in l]

    def step(acc, item):
        groups, cur_agents, cur_rules, last_was_agent = acc
        k, v = item
        if k == "user-agent":
            if last_was_agent or not cur_agents:
                return groups, cur_agents + (v.lower(),), cur_rules, True
            return groups + ((cur_agents, cur_rules),), (v.lower(),), (), True
        if k in ("allow", "disallow") and cur_agents:
            return groups, cur_agents, cur_rules + ((k == "allow", v),), False
        return groups, cur_agents, cur_rules, last_was_agent if k != "sitemap" else last_was_agent

    groups, agents, rules, _ = reduce(step, kv, ((), (), (), False))
    return groups + (((agents, rules),) if agents else ())


def sitemaps_in(text):
    return tuple(l.split(":", 1)[1].strip() for l in text.splitlines()
                 if l.lower().startswith("sitemap:"))


def pat_regex(p):
    body = "".join(".*" if c == "*" else re.escape(c) for c in p.rstrip("$"))
    return re.compile("^" + body + ("$" if p.endswith("$") else ""))


def rules_for(groups, agent):
    a = agent.lower()
    specific = tuple(r for ags, rs in groups for r in rs
                     if any(g != "*" and (g in a or a in g) for g in ags))
    if specific:
        return specific
    return tuple(r for ags, rs in groups for r in rs if "*" in ags)


def allowed(rules, path):
    hits = tuple((len(p), allow) for allow, p in rules if p and pat_regex(p).match(path))
    if not hits:
        return True
    best = max(h[0] for h in hits)
    return any(allow for n, allow in hits if n == best)  # tie => allow


@lru_cache(maxsize=None)
def robots(host):
    if off_limits(host):
        return ("off-limits host (rules)", None, ())
    st, body, _ = http_get(f"https://{host}/robots.txt", timeout=25)
    if st == 404:
        return ("no robots (404)", (), ())
    if st != 200:
        return (f"robots HTTP {st} => treat as disallowed", None, ())
    text = body.decode("utf-8", "replace")
    if "<html" in text[:500].lower():
        return ("robots returned HTML => treat as no rules", (), ())
    return ("robots 200", parse_groups(text), sitemaps_in(text))


def verdict(url):
    u = urlparse(url)
    note, groups, _ = robots(u.netloc.lower())
    if groups is None:
        return False, note
    path = (u.path or "/") + (("?" + u.query) if u.query else "")
    denied = tuple(a for a in AGENTS if not allowed(rules_for(groups, a), path))
    return (not denied), note + ("; disallowed for " + ",".join(denied) if denied else "; allowed all agents")


# ---------- text extraction ----------

class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links, self.skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        if tag == "a":
            self.links.extend(v for k, v in attrs if k == "href" and v)
        if tag in ("p", "li", "br", "h1", "h2", "h3", "h4", "tr", "div", "section"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip:
            self.parts.append(d)


def html_text_links(body):
    p = _Text()
    try:
        p.feed(body.decode("utf-8", "replace"))
    except Exception:
        pass
    text = re.sub(r"[ \t\r\f\v]+", " ", "".join(p.parts))
    text = "\n".join(l.strip() for l in text.splitlines() if l.strip())
    return text, tuple(p.links)


def key_sentences(text):
    sents = re.split(r"(?<=[.!?])\s+|\n", text)
    return tuple(s.strip() for s in sents if 25 < len(s.strip()) < 600 and KEY_PAT.search(s))


def cache_name(url):
    return hashlib.sha1(url.encode()).hexdigest()[:16]


def fetch(out, url):
    ok, note = verdict(url)
    base = dict(url=url, robots=note, fetched=datetime.date.today().isoformat())
    if not ok:
        return {**base, "status": "blocked_robots", "bytes": 0, "text_path": ""}
    st, body, ct = http_get(url)
    if st != 200:
        return {**base, "status": str(st), "bytes": len(body), "text_path": ""}
    is_pdf = body[:4] == b"%PDF"
    raw = os.path.join(out, "raw", cache_name(url) + (".pdf" if is_pdf else ".html"))
    os.makedirs(os.path.dirname(raw), exist_ok=True)
    with open(raw, "wb") as f:
        f.write(body)
    text = "" if is_pdf else html_text_links(body)[0]
    tp = os.path.join(out, "text", cache_name(url) + ".txt")
    os.makedirs(os.path.dirname(tp), exist_ok=True)
    with open(tp, "w") as f:
        f.write(url + "\n\n" + text)
    return {**base, "status": "200" + (" pdf" if is_pdf else ""), "bytes": len(body), "text_path": tp}


# ---------- discovery ----------

def locs(body):
    return tuple(html.unescape(m) for m in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body.decode("utf-8", "replace")))


def crawl_sitemaps(seeds):
    """Breadth-first over sitemap indexes, robots-checked, capped. Returns (page_urls, n_fetched)."""
    def step(acc, _):
        queue, seen, pages = acc
        if not queue or len(seen) >= MAX_SITEMAPS:
            return acc
        sm, rest = queue[0], queue[1:]
        if sm in seen or not verdict(sm)[0]:
            return rest, seen | {sm}, pages
        st, body, _ = http_get(sm, timeout=30)
        found = locs(body) if st == 200 else ()
        subs = tuple(u for u in found if re.search(r"sitemap|\.xml(\.gz)?$", u, re.I) and u not in seen)
        return rest + subs, seen | {sm}, pages + tuple(u for u in found if u not in subs)
    _, seen, pages = reduce(step, range(MAX_SITEMAPS * 3), (tuple(seeds), frozenset(), ()))
    return pages, len(seen)


def candidate_rank(url):
    """Hub / product pages first; stories, blogs, events, news and PDFs last; then shorter paths."""
    path = urlparse(url).path.lower()
    noisy = bool(re.search(r"/(stories|story|blog|news|events?|press|posts?|media|grants?-awarded|\d{4})/", path))
    product = bool(re.search(r"(ways-to-give|types-of-funds|fund-types|open-a-fund|start-a-fund|giving-circle-fund|"
                             r"collective-giving|giving-circles?/?$)", path))
    return (0 if product and not noisy else 1 if not noisy else 2, path.endswith(".pdf"), len(path))


def discover_one(out, row):
    home = row["homepage"]
    host = urlparse(home).netloc.lower()
    note, groups, sms = robots(host)
    if groups is None:
        return dict(row, robots=note, sitemaps_read=0, candidates="", fetched=()), ()
    seeds = sms or (f"https://{host}/sitemap.xml", f"https://{host}/sitemap_index.xml", f"https://{host}/wp-sitemap.xml")
    pages, n = crawl_sitemaps(seeds)
    home_ok = verdict(home)[0]
    st, body, _ = http_get(home) if home_ok else (0, b"", "")
    home_links = tuple(urljoin(home, l) for l in html_text_links(body)[1]) if st == 200 else ()
    same_site = lambda u: urlparse(u).netloc.lower().replace("www.", "") == host.replace("www.", "")
    raw = tuple(dict.fromkeys(u.split("#")[0] for u in pages + home_links if URL_PAT.search(u) and same_site(u)))
    cands = tuple(sorted(raw, key=candidate_rank))
    fetched = tuple(fetch(out, u) for u in cands[:MAX_PAGES])
    return dict(row, robots=note, sitemaps_read=n, candidates=" ; ".join(cands[:40])), fetched


def sample_rows(root):
    rows = list(csv.DictReader(open(os.path.join(root, CF_LIST))))
    top = sorted((r for r in rows if r["homepage"] and r["fy2024_daf_assets_usd"]),
                 key=lambda r: -float(r["fy2024_daf_assets_usd"]))[:100]
    picked = [dict(rank=i + 1, ein=r["ein"], name=r["name"], homepage=r["homepage"],
                   fy2024_daf_assets_usd=r["fy2024_daf_assets_usd"]) for i, r in enumerate(top) if i % 3 == 0]
    return list({r["homepage"]: r for r in reversed(picked)}.values())[::-1]


def write_csv(path, rows, fields, mode="w"):
    new = mode == "w" or not os.path.exists(path)
    with open(path, mode, newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerows(rows)


LOG_FIELDS = ["fetched", "url", "robots", "status", "bytes", "text_path"]


def main(argv):
    root, mode, out = argv[1], argv[2], argv[3]
    os.makedirs(out, exist_ok=True)
    if mode == "sample":
        rows = sample_rows(root)
        write_csv(os.path.join(out, "sample.csv"), rows, list(rows[0].keys()))
        print(f"{len(rows)} CFs sampled")
    elif mode == "discover":
        rows = list(csv.DictReader(open(os.path.join(out, "sample.csv"))))
        only = set(argv[4:])
        rows = [r for r in rows if not only or r["rank"] in only]
        results = [discover_one(out, r) for r in rows]
        summary = [s for s, _ in results]
        logs = [f for _, fs in results for f in fs]
        write_csv(os.path.join(out, "candidates.csv"), summary, list(summary[0].keys()), "a")
        write_csv(os.path.join(out, "robots-log.csv"), logs, LOG_FIELDS, "a")
        print("\n".join(f"{s['rank']}\t{s['name'][:30]}\t{s['robots'][:40]}\tsm={s['sitemaps_read']}\t{s['candidates'][:200]}" for s in summary))
    elif mode == "fetch":
        logs = [fetch(out, u) for u in argv[4:]]
        write_csv(os.path.join(out, "robots-log.csv"), logs, LOG_FIELDS, "a")
        print("\n".join(f"{l['status']}\t{l['bytes']}\t{l['robots'][:80]}\t{l['url']}\t{l['text_path']}" for l in logs))
    elif mode == "sentences":
        for p in argv[4:]:
            print("=== " + p)
            print("\n".join(key_sentences(open(p).read())))


if __name__ == "__main__":
    main(sys.argv)
