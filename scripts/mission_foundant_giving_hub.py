"""P-B4222-02-01: Foundant CommunitySuite public Giving Hub tenancy.

Usage:
  python3 -I scripts/mission_foundant_giving_hub.py . [--cache DIR] [--offline] [--core-only]
                                                      [--workers N] [--out CSV]
  root        repo root ('.')
  --cache     directory for fetched pages and robots files (default: $TMPDIR/foundant-hub-cache).
              Kept outside the repo so no stray directories are created.
  --offline   parse only what is in the cache; make no network requests
  --core-only only the Foundant CommunitySuite rows of community-foundation-rails-portals-2026-v2.csv
  --workers   parallel foundations (default 4); requests inside one foundation are sequential
  --out       output CSV (default <root>/data/mission-2026-11-14/foundant-giving-hub-2026-11-20.csv)

Population
  core      every row of community-foundation-rails-portals-2026-v2.csv whose portal_vendor is
            'Foundant CommunitySuite' (counted here, not typed).
  extended  every row of cf-vendor-map-by-ein-v2.csv whose portal_vendor is 'Foundant CommunitySuite'
            and that is not already in core (joined on EIN). Its homepage URL is the start page.

Method (per foundation; no logins, no form submissions, no host enumeration)
  1. robots.txt of the CF host is fetched and parsed first. A path is fetched only if it is allowed
     for BOTH the generic script agent ('research-script/1.0', which falls in the '*' group) and the
     'Claude-User' token (user-directed fetches). Blocks aimed only at training crawlers (ClaudeBot,
     anthropic-ai, GPTBot, CCBot, ...) are logged but are not the agent of this run. Per RFC 9309 a
     4xx robots response means 'allow all' and a 5xx/transport failure means 'disallow all'.
  2. The CF start pages (homepage, plus the repo's own source URLs on the same host for core rows)
     are read and every link whose path contains '/erp/donate' is a Giving Hub link. If none is
     found, at most three same-site links whose href or anchor text says give/donate are followed
     once and searched the same way. The hub host is the host most often linked. No hub URL is ever
     guessed: a foundation with no linked hub is recorded as 'no hub link found'.
  3. robots.txt of the hub host is fetched and parsed (same rule).
  4. The hub's featured page (/erp/donate/list) is read. The hub sets its session cookie from a
     hidden field in that page (this is how a browser with cookies enabled gets it); the cookie is
     sent on the next GETs. The complete list (/erp/donate/list?showlist=1, plus each sorg_id
     affiliate variant linked from the CF site or the hub) is then read and fund cards are unioned
     on funit_id.
  5. Each fund card (title, description, Donate link) is classified by pure functions below.
     None of the hubs read shows a fund-type field on the card (the template has an empty slot), so
     fund type is derived from the fund's own name and description and labelled as such.

DAF classes (per fund)
  daf_explicit      name or description says 'donor advised' / 'donor-advised' / 'DAF', or the
                    description says grants are made as recommended by the (grant/fund) advisor or donor
  advised_agency    name contains 'advised' and 'agency' (a nonprofit's agency-advised fund)
  advised_other     name contains 'advised' but neither of the above (may be a DAF or a nonprofit-
                    advised fund; reported separately, not counted as DAF)
Hub-level 'lists_daf_public' = Y if >=1 daf_explicit fund, P if none but >=1 advised_other, else N.

Stdlib only; functional style (pure functions, map/filter/reduce); no mutable global state.
Prints the summary tables used in the research note.
"""
import csv
import hashlib
import html
import json
import os
import re
import ssl
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import reduce

UA = "research-script/1.0"
AGENTS = (UA, "Claude-User")
LOGGED_AI_TOKENS = ("claudebot", "anthropic-ai", "claude-user", "claude-searchbot", "gptbot", "ccbot")
RETRIEVED = "2026-11-20"
RAILS = "data/mission-2026-11-14/community-foundation-rails-portals-2026-v2.csv"
VMAP = "data/mission-2026-11-14/cf-vendor-map-by-ein-v2.csv"
OUT = "data/mission-2026-11-14/foundant-giving-hub-2026-11-20.csv"
VENDOR = "Foundant CommunitySuite"
DELAY_S = 0.6
MAX_FOLLOW = 3

COLS = ["row_id", "population", "foundation", "ein", "fy2024_daf_assets_usd", "dafrc_rank_fy2024",
        "cf_start_url", "cf_host", "cf_robots_status", "cf_robots_allows_agent", "cf_robots_ai_group",
        "hub_link_found_on", "hub_url", "hub_host", "hub_robots_status", "hub_robots_allows_agent",
        "hub_robots_ai_group", "hub_read_status", "featured_funds", "public_funds_total",
        "affiliate_lists_read", "type_daf_explicit", "type_advised_agency", "type_advised_other",
        "type_scholarship", "type_endowment", "type_memorial", "type_designated", "type_agency",
        "type_field_of_interest_or_general", "type_family_or_named_charitable", "type_other",
        "fund_type_shown_on_hub", "lists_daf_public", "daf_examples", "hub_nav_items",
        "donor_portal_link_on_hub", "grant_catalog_on_hub", "recommend_grant_text_on_hub",
        "daf_mention_in_hub_text", "dafpay_or_dafdirect_on_hub", "dafpay_or_dafdirect_on_cf_pages",
        "notes", "retrieved"]

# ----------------------------------------------------------------------------------------------
# Pure helpers: text, URLs, links
# ----------------------------------------------------------------------------------------------

def strip_tags(fragment):
    no_script = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", no_script))).strip()


def host_of(url):
    return (urllib.parse.urlsplit(url).hostname or "").lower()


def site_key(host):
    return re.sub(r"^www\.", "", host)


def links_in(page, base):
    pairs = re.findall(r"<a\b[^>]*?href\s*=\s*[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", page, flags=re.S | re.I)
    absolute = map(lambda p: (urllib.parse.urljoin(base, html.unescape(p[0]).strip()), strip_tags(p[1])), pairs)
    return tuple(filter(lambda p: p[0].startswith("http"), absolute))


def is_hub_link(url):
    return "/erp/donate" in urllib.parse.urlsplit(url).path.lower()


def is_give_link(pair, cf_site):
    url, text = pair
    parts = urllib.parse.urlsplit(url)
    same_site = site_key((parts.hostname or "").lower()) == cf_site
    looks_give = re.search(r"donat|\bgive\b|give-|/give|gift|ways-to-give", (parts.path + " " + text).lower())
    not_file = not re.search(r"\.(pdf|jpg|png|docx?)$", parts.path.lower())
    return bool(same_site and looks_give and not_file and not is_hub_link(url))


def sorg_ids(urls):
    return tuple(sorted({q for u in urls for q in urllib.parse.parse_qs(urllib.parse.urlsplit(u).query).get("sorg_id", [])}))


def most_common_host(urls):
    counts = Counter(map(host_of, urls))
    return counts.most_common(1)[0][0] if counts else ""


def daf_widget(page):
    found = re.findall(r"dafpay|givechariot|chariot-connect|dafdirect|daf direct|daf-direct", page, flags=re.I)
    return ";".join(sorted({f.lower() for f in found}))

# ----------------------------------------------------------------------------------------------
# Pure helpers: robots
# ----------------------------------------------------------------------------------------------

def robots_parser(text):
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(text.splitlines())
    return parser


def robots_verdict(fetched, url):
    """fetched = (status, text). Returns (status_label, allows_agent bool, ai_group_note)."""
    status, text = fetched
    if status == 200:
        parser = robots_parser(text)
        allows = all(parser.can_fetch(a, url) for a in AGENTS)
        named = sorted({t for t in LOGGED_AI_TOKENS
                        if re.search(r"(?im)^\s*user-agent:\s*" + re.escape(t) + r"\s*$", text)})
        blocked = [t for t in named if not parser.can_fetch(t, url)]
        note = ("named " + ",".join(named) + "; disallowed for this path: " + (",".join(blocked) or "none")) if named else "no AI-specific group"
        return ("200", allows, note)
    if isinstance(status, int) and 400 <= status < 500:
        return (f"{status} (allow all per RFC 9309)", True, "n/a")
    return (f"{status} (disallow all per RFC 9309)", False, "n/a")

# ----------------------------------------------------------------------------------------------
# Pure helpers: hub parsing and classification
# ----------------------------------------------------------------------------------------------

def session_cookie(page):
    m = re.search(r"value=\"SID&#61;([0-9a-f]+)", page)
    return ("SID=" + m.group(1)) if m else ""


def card_chunks(page):
    body = page[page.find('id="ft_content"'):] if 'id="ft_content"' in page else ""
    return tuple(filter(lambda c: 'class="card-title"' in c, re.split(r'<div class="ft_card card', body)[1:]))


def parse_card(chunk):
    title = re.search(r'<h2 class="card-title">(.*?)</h2>', chunk, flags=re.S)
    desc = re.search(r'class="(?:card-text )?ft_p_multiline_truncate">(.*?)</(?:p|div)>', chunk, flags=re.S)
    donate = re.findall(r'href="[^"]*funit_id=(\d+)[^"]*"[^>]*class="[^"]*btn-primary[^"]*"[^>]*>\s*Donate', chunk)
    return dict(name=strip_tags(title.group(1)) if title else "",
                desc=strip_tags(desc.group(1)) if desc else "",
                funit_id=donate[-1] if donate else "")


def parse_cards(page):
    return tuple(filter(lambda c: c["funit_id"], map(parse_card, card_chunks(page))))


def nav_items(page):
    items = re.findall(r'<li class="ft_navigation_item nav-item[^"]*">\s*<a href="([^"]+)"[^>]*>(.*?)</a>', page, flags=re.S)
    return tuple(dict.fromkeys((strip_tags(t), h) for h, t in items if strip_tags(t)))


def header_text(page):
    """Hub's own text outside the fund cards: everything before the card area plus the footer."""
    start = page.find('id="ft_content"')
    head = page[:start] if start >= 0 else page
    foot = page[page.find('class="ft_footer"'):] if 'class="ft_footer"' in page else ""
    return strip_tags(re.sub(r"<head\b.*?</head>", " ", head, flags=re.S | re.I)) + " " + strip_tags(foot)


def fund_type_shown(page):
    return "Y" if re.search(r'ft_(?:fund_type|granttype|grant_type)[^"]*">\s*[^<\s]', page) else "N"


DAF_EXPLICIT = re.compile(r"donor[- ]advised|\bDAF\b|recommended by the (?:grant |fund )?(?:advisor|donor)s?", re.I)


GIFT_FROM_DAF = re.compile(r"from\s+(?:your\s+|a\s+|an\s+)?$", re.I)


def says_daf(text):
    """True if text calls the fund a DAF; 'give from your donor-advised fund' (a payment source) does not count."""
    return any(not GIFT_FROM_DAF.search(text[max(0, m.start() - 20):m.start()]) for m in DAF_EXPLICIT.finditer(text))


def daf_class(fund):
    text = fund["name"] + " " + fund["desc"]
    name = fund["name"].lower()
    if says_daf(text):
        return "daf_explicit"
    if "advised" in name and "agency" in name:
        return "advised_agency"
    if "advised" in name:
        return "advised_other"
    return ""


NAME_TYPES = (
    ("scholarship", r"scholarship"),
    ("agency", r"\bagency\b|endowment fund for |organi[sz]ation endowment|nonprofit endowment"),
    ("designated", r"designated"),
    ("endowment", r"endow"),
    ("memorial", r"memorial|in memory|in honor|legacy"),
    ("field_of_interest_or_general", r"general fund|unrestricted|community fund|field of interest|impact fund|"
                                     r"relief|response fund|disaster|community needs|opportunity fund"),
    ("family_or_named_charitable", r"family|charitable fund|philanthropic fund|giving fund"),
)


def name_type(fund):
    dc = daf_class(fund)
    if dc:
        return dc
    text = (fund["name"] + " " + fund["desc"]).lower()
    hit = next((label for label, rx in NAME_TYPES if re.search(rx, text)), None)
    return hit or "other"


def lists_daf(counts):
    return "Y" if counts.get("daf_explicit", 0) else ("P" if counts.get("advised_other", 0) else "N")


def union_funds(card_lists):
    merged = reduce(lambda acc, cards: {**acc, **{c["funit_id"]: c for c in cards if c["funit_id"] not in acc}},
                    card_lists, {})
    return tuple(merged.values())

# ----------------------------------------------------------------------------------------------
# IO: cached HTTP GET (the only impure part)
# ----------------------------------------------------------------------------------------------

def cache_path(cache, url):
    return os.path.join(cache, hashlib.sha1(url.encode()).hexdigest() + ".json")


def http_get(url, cookie, cache, offline):
    """Returns (status, text, final_url). Cached by URL. Sleeps DELAY_S after a live request."""
    path = cache_path(cache, url)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
        return rec["status"], rec["text"], rec["final_url"]
    if offline:
        return "not_cached", "", url
    headers = {"User-Agent": UA, **({"Cookie": cookie} if cookie else {})}
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30, context=ctx) as resp:
            rec = dict(status=resp.status, text=resp.read(8_000_000).decode("utf-8", "replace"), final_url=resp.geturl())
    except urllib.error.HTTPError as err:
        rec = dict(status=err.code, text="", final_url=url)
    except Exception as err:  # transport failure: record, never retry around a block
        rec = dict(status="transport_error:" + type(err).__name__, text="", final_url=url)
    time.sleep(DELAY_S)
    if isinstance(rec["status"], int):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(dict(url=url, **rec), fh)
    return rec["status"], rec["text"], rec["final_url"]


def robots_for(host, cache, offline):
    status, text, _ = http_get(f"https://{host}/robots.txt", "", cache, offline)
    return (status, text)

# ----------------------------------------------------------------------------------------------
# Per-foundation pipeline (composes IO with the pure helpers)
# ----------------------------------------------------------------------------------------------

def read_cf_pages(start_urls, cf_robots, cache, offline):
    allowed = tuple(filter(lambda u: robots_verdict(cf_robots, u)[1], start_urls))
    pages = tuple(map(lambda u: (u,) + http_get(u, "", cache, offline), allowed))
    return tuple(filter(lambda p: p[1] == 200, pages))


def find_hub(start_urls, cf_site, cf_robots, cache, offline):
    first = read_cf_pages(start_urls, cf_robots, cache, offline)
    first_links = tuple(l for (u, _s, text, final) in first for l in links_in(text, final))
    hubs = tuple(filter(lambda l: is_hub_link(l[0]), first_links))
    if hubs:
        return first, hubs, first[0][0] if first else ""
    follow = tuple(dict.fromkeys(l[0].split("#")[0] for l in first_links if is_give_link(l, cf_site)))[:MAX_FOLLOW]
    second = read_cf_pages(follow, cf_robots, cache, offline)
    second_hubs = tuple((l, u) for (u, _s, text, final) in second for l in links_in(text, final) if is_hub_link(l[0]))
    found_on = second_hubs[0][1] if second_hubs else ""
    return first + second, tuple(h for h, _ in second_hubs), found_on


def read_hub(hub_host, affiliate_ids, hub_robots, cache, offline):
    featured_url = f"https://{hub_host}/erp/donate/list"
    if not robots_verdict(hub_robots, featured_url)[1]:
        return dict(status="robots_disallowed")
    f_status, featured, _ = http_get(featured_url, "", cache, offline)
    if f_status != 200:
        return dict(status=f"featured_http_{f_status}")
    cookie = session_cookie(featured)
    first_featured = featured
    # with the cookie the featured page shows its cards; the cookie-less copy shows only a notice
    f2_status, featured2, _ = http_get(featured_url + "?", cookie, cache, offline)
    featured = featured2 if f2_status == 200 and card_chunks(featured2) else first_featured
    hub_ids = sorg_ids(map(lambda l: l[0], links_in(featured, featured_url)))
    variants = ("",) + tuple(sorted(set(affiliate_ids) | set(hub_ids)))
    list_urls = tuple(map(lambda s: f"https://{hub_host}/erp/donate/list?showlist=1" + (f"&sorg_id={s}" if s else ""), variants))
    lists = tuple(map(lambda u: http_get(u, cookie, cache, offline), filter(lambda u: robots_verdict(hub_robots, u)[1], list_urls)))
    ok_lists = tuple(filter(lambda r: r[0] == 200, lists))
    return dict(status="read" if ok_lists else "list_not_read", featured=featured,
                lists=tuple(r[1] for r in ok_lists), n_lists=len(ok_lists))


def hub_row(cf, cache, offline):
    start_urls = cf["start_urls"]
    cf_host = host_of(start_urls[0]) if start_urls else ""
    cf_robots = robots_for(cf_host, cache, offline) if cf_host else ("no_host", "")
    cf_rv = robots_verdict(cf_robots, start_urls[0] if start_urls else "")
    base = dict(population=cf["population"], foundation=cf["foundation"], ein=cf["ein"],
                fy2024_daf_assets_usd=cf["assets"], dafrc_rank_fy2024=cf["rank"],
                cf_start_url=start_urls[0] if start_urls else "", cf_host=cf_host,
                cf_robots_status=cf_rv[0], cf_robots_allows_agent="Y" if cf_rv[1] else "N",
                cf_robots_ai_group=cf_rv[2], retrieved=RETRIEVED)
    if not cf_rv[1]:
        return {**base, "hub_read_status": "cf_robots_disallowed"}
    pages, hubs, found_on = find_hub(start_urls, site_key(cf_host), cf_robots, cache, offline)
    cf_widget = ";".join(sorted({w for p in pages for w in daf_widget(p[2]).split(";") if w}))
    base = {**base, "dafpay_or_dafdirect_on_cf_pages": cf_widget or "none seen",
            "notes": "" if pages else "CF start pages not read"}
    if not hubs:
        return {**base, "hub_read_status": "no hub link found", "lists_daf_public": "n/a"}
    hub_urls = tuple(h[0] for h in hubs)
    hub_host = most_common_host(hub_urls)
    hub_robots = robots_for(hub_host, cache, offline)
    hub_rv = robots_verdict(hub_robots, f"https://{hub_host}/erp/donate/list")
    base = {**base, "hub_link_found_on": found_on, "hub_url": f"https://{hub_host}/erp/donate/list",
            "hub_host": hub_host, "hub_robots_status": hub_rv[0],
            "hub_robots_allows_agent": "Y" if hub_rv[1] else "N", "hub_robots_ai_group": hub_rv[2]}
    hub = read_hub(hub_host, sorg_ids(u for u in hub_urls if host_of(u) == hub_host), hub_robots, cache, offline)
    if hub["status"] != "read":
        return {**base, "hub_read_status": hub["status"], "lists_daf_public": "n/a"}
    featured_cards = parse_cards(hub["featured"])
    funds = union_funds(tuple(map(parse_cards, hub["lists"])))
    counts = Counter(map(name_type, funds))
    explicit = [f for f in funds if daf_class(f) == "daf_explicit"]
    nav = nav_items(hub["featured"])
    hub_text = header_text(hub["featured"])
    all_hub_html = hub["featured"] + "".join(hub["lists"])
    return {**base,
            "hub_read_status": "read",
            "featured_funds": len(featured_cards),
            "public_funds_total": len(funds),
            "affiliate_lists_read": hub["n_lists"] - 1,
            **{f"type_{k}": counts.get(k, 0) for k in ("daf_explicit", "advised_agency", "advised_other", "scholarship",
                                                       "endowment", "memorial", "designated", "agency",
                                                       "field_of_interest_or_general", "family_or_named_charitable", "other")},
            "fund_type_shown_on_hub": fund_type_shown(all_hub_html),
            "lists_daf_public": lists_daf(counts),
            "daf_examples": " | ".join(f"{f['name']} (funit_id={f['funit_id']})" for f in explicit[:3]),
            "hub_nav_items": "; ".join(t for t, _ in nav),
            "donor_portal_link_on_hub": "Y" if any(re.search(r"/erp/(portal|fundmanager|login)", h) for _, h in nav) else "N",
            "grant_catalog_on_hub": "Y" if any("/erp/donate/list/grant" in h for _, h in nav) else "N",
            "recommend_grant_text_on_hub": "Y" if re.search(r"recommend(?:ing)? a grant|grant recommendation", strip_tags(hub["featured"]), re.I) else "N",
            "daf_mention_in_hub_text": "Y" if re.search(r"donor[- ]advised|\bDAF\b", hub_text) else "N",
            "dafpay_or_dafdirect_on_hub": daf_widget(all_hub_html) or "none seen"}

# ----------------------------------------------------------------------------------------------
# Population
# ----------------------------------------------------------------------------------------------

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def homepage_of(urls):
    first = urls[0] if urls else ""
    parts = urllib.parse.urlsplit(first)
    return f"{parts.scheme}://{parts.netloc}/" if parts.netloc else ""


def core_population(root):
    rows = tuple(filter(lambda r: r["portal_vendor"] == VENDOR, read_csv(os.path.join(root, RAILS))))

    def to_cf(r):
        urls = tuple(u.strip() for u in r["source_urls"].split(" ; ") if u.strip())
        home = homepage_of(tuple(u for u in urls if "fcsuite" not in u and "gt990" not in u))
        same_host = tuple(u for u in urls if host_of(u) == host_of(home) and u.rstrip("/") != home.rstrip("/"))
        return dict(population="core", foundation=r["foundation"], ein=r["ein"].zfill(9),
                    assets=r["fy2024_daf_assets_usd"], rank=r["dafrc_rank_fy2024"],
                    start_urls=(home,) + same_host)
    return tuple(map(to_cf, rows))


def extended_population(root, core_eins):
    rows = filter(lambda r: r["portal_vendor"] == VENDOR and r["homepage"].startswith("http")
                  and r["ein"].zfill(9) not in core_eins, read_csv(os.path.join(root, VMAP)))
    return tuple(map(lambda r: dict(population="extended", foundation=r["name"], ein=r["ein"].zfill(9),
                                    assets=r["fy2024_daf_assets_usd"], rank="", start_urls=(r["homepage"],)),
                     rows))

# ----------------------------------------------------------------------------------------------
# Summaries (pure)
# ----------------------------------------------------------------------------------------------

def share(rows, pred):
    n = len(rows)
    k = sum(1 for r in rows if pred(r))
    return k, n, (round(100.0 * k / n, 1) if n else 0.0)


def summarise(rows):
    def block(label, sub):
        read = tuple(filter(lambda r: r.get("hub_read_status") == "read", sub))
        lines = [f"[{label}] foundations={len(sub)} hub_status={dict(Counter(r.get('hub_read_status') for r in sub))}",
                 "  hubs read: %d; lists DAF (Y) %d/%d = %.1f%%" % ((len(read),) + share(read, lambda r: r["lists_daf_public"] == "Y")),
                 "  Y or P (any 'advised' name): %d/%d = %.1f%%" % share(read, lambda r: r["lists_daf_public"] in ("Y", "P")),
                 "  public funds total: %d; explicit-DAF funds: %d" % (sum(int(r["public_funds_total"]) for r in read),
                                                                       sum(int(r["type_daf_explicit"]) for r in read)),
                 "  fund type field shown on hub: %d/%d" % share(read, lambda r: r["fund_type_shown_on_hub"] == "Y")[:2],
                 "  donor portal link on hub: %d/%d; grant catalog: %d/%d; recommend-grant text: %d/%d; DAF in hub text: %d/%d" % (
                     share(read, lambda r: r["donor_portal_link_on_hub"] == "Y")[:2] + share(read, lambda r: r["grant_catalog_on_hub"] == "Y")[:2]
                     + share(read, lambda r: r["recommend_grant_text_on_hub"] == "Y")[:2] + share(read, lambda r: r["daf_mention_in_hub_text"] == "Y")[:2]),
                 "  DAFpay/DAF Direct on hub: %d/%d; on CF pages read: %d/%d" % (
                     share(read, lambda r: r["dafpay_or_dafdirect_on_hub"] != "none seen")[:2]
                     + share(sub, lambda r: r.get("dafpay_or_dafdirect_on_cf_pages", "none seen") not in ("none seen", ""))[:2])]
        return "\n".join(lines)
    core = tuple(filter(lambda r: r["population"] == "core", rows))
    return "\n".join([block("core", core), block("extended", tuple(filter(lambda r: r["population"] == "extended", rows))),
                      block("all", rows)])

# ----------------------------------------------------------------------------------------------

def parse_args(argv):
    flags = {"--offline", "--core-only"}
    opts = reduce(lambda acc, i: {**acc, argv[i]: True} if argv[i] in flags else
                  ({**acc, argv[i]: argv[i + 1]} if argv[i].startswith("--") and i + 1 < len(argv) else acc),
                  range(len(argv)), {})
    root = argv[0] if argv and not argv[0].startswith("--") else "."
    return dict(root=root, cache=opts.get("--cache", os.path.join(tempfile.gettempdir(), "foundant-hub-cache")),
                offline=bool(opts.get("--offline")), core_only=bool(opts.get("--core-only")),
                workers=int(opts.get("--workers", 4)), out=opts.get("--out", os.path.join(root, OUT)))


def main(argv):
    args = parse_args(argv)
    os.makedirs(args["cache"], exist_ok=True)
    core = core_population(args["root"])
    print(f"core population (portal_vendor == '{VENDOR}' in {RAILS}): {len(core)}")
    ext = () if args["core_only"] else extended_population(args["root"], {c["ein"] for c in core})
    print(f"extended population ({VMAP}, not in core): {len(ext)}")
    cfs = core + ext
    with ThreadPoolExecutor(max_workers=args["workers"]) as pool:
        rows = tuple(pool.map(lambda cf: hub_row(cf, args["cache"], args["offline"]), cfs))
    numbered = tuple({**{c: "" for c in COLS}, **r, "row_id": f"FGH-{i:03d}"} for i, r in enumerate(rows, 1))
    with open(args["out"], "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(numbered)
    print(f"wrote {args['out']} ({len(numbered)} rows)")
    print(summarise(numbered))


if __name__ == "__main__":
    main(sys.argv[1:])
