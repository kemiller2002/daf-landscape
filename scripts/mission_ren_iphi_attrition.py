#!/usr/bin/env python3
"""P-BMG-03 (Ren/Stellar iPhi client attrition 2023-2026), with P-VEN-05 (PNC / Truist / UBS iPhi hosts),
P-BMG-02 (spectrumportal.net / Foundation Cloud tenants) and P-QA2-03 (Ren for Charities / RDE program coverage).

Task `census` (P-BMG-03 + P-VEN-05)
  1. Seed iPhi tenant labels from (a) every `*.iphiview.com` host or path already cited in the repo (research/ and
     data/ text files), (b) certificate transparency (crt.sh bare-domain queries for iphiview.com,
     stellartechsol.com, donorfirstx.com, reninc.com), (c) a guess list: the homepage domain stem and two
     initial-letter acronyms of every sponsor in the CF vendor map and the 990 sponsor universe, plus a fixed list
     of bank / broker / Ren-program labels.
  2. DNS: resolve <label>.iphiview.com for every seed through DNS-over-HTTPS (dns.google and cloudflare-dns.com,
     alternating; at most 1 request/s per resolver). iphiview.com has no wildcard record (a random label returns
     NXDOMAIN, checked in the run), so NOERROR + A record = the host exists. The CNAME target classifies hosting
     (AWS Global Accelerator anycast pair vs the `ren-workload-02` ELB).
  3. HTTP (public login pages only; no login, no form): GET https://<host>/ (no redirect following) and
     https://<host>/<label>/ (and each path tenant cited in the repo); extract the DotNetNuke `MetaAuthor`,
     `MetaCopyright`, `MetaDescription`, footer (c) year, portal title text and transition banners.
  4. Cross-reference: CF vendor map (current fund-login vendor per EIN, homepage links to the tenant), the
     990 Part VII-B harvest (Stellar / Ren payee lines by tax year), the dated migration file, and a short manual
     table of first-party evidence already in the repo for non-CF sponsors (each row carries its URL).
  5. Classify each tenant: active / migrated (destination vendor where evidenced) / lapsed / unknown /
     out_of_scope (not a DAF/CF fund portal), and compute the 2023-2026 attrition rate with bounds.
Task `spectrum` (P-BMG-02): fetch every spectrumportal.net tenant in the CF map, record status and title, and join
  990 Blackbaud / NPact (Fusion) / Foundant lines and the ledger file; re-set ledger_implied.
Task `rde` (P-QA2-03): fetch the public Ren for Charities help-centre articles and sponsor charity-facing pages and
  record which named programs are tied to Ren ACH / the charity portal, with the quoted text.

No outreach, no logins, no forms, no auth attempts. All responses are cached under --cache-dir; reruns without
--fetch are offline and reproducible. Stdlib only, functional style (pure transforms; I/O at the edges).

Usage: python3 scripts/mission_ren_iphi_attrition.py --cache-dir DIR [--fetch] [--task census|spectrum|rde|all]
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import html
import json
import math
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Mapping, Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "mission-2026-11-14")
CFMAP = os.path.join(DATA, "cf-vendor-map-by-ein.csv")
SIGNALS = os.path.join(DATA, "cf-vendor-map-signals.csv")
HARVEST = os.path.join(DATA, "form990-contractors-harvest-full.csv")
UNIVERSE = os.path.join(DATA, "form990-harvest-sponsor-universe-full.csv")
MIGR = os.path.join(DATA, "cf-vendor-migrations-2022-2026.csv")
LEDGER = os.path.join(DATA, "cf-ledger-vendors-2026.csv")
OUT_CENSUS = os.path.join(DATA, "ren-iphi-tenant-census.csv")
OUT_SPECTRUM = os.path.join(DATA, "spectrumportal-tenant-audit.csv")
OUT_RDE = os.path.join(DATA, "ren-charity-ach-program-evidence.csv")
OUT_SUMMARY = os.path.join(DATA, "ren-iphi-attrition-summary.json")
RETRIEVED = "2026-11-15"
UA = {"User-Agent": "Mozilla/5.0 (compatible; research-client)"}
NOW_YEARS = 2026 + 10.5 / 12 - 2023  # 2023-01-01 .. 2026-11-15 in years

# ----------------------------------------------------------------------------- fetch layer (I/O edge)
_LOCK = threading.Lock()
_LAST: dict[str, float] = {}


def throttle(key: str, gap: float = 1.05) -> None:
    """Block until at least `gap` seconds since the last request with this key (per host / registrable domain)."""
    while True:
        with _LOCK:
            wait = _LAST.get(key, 0) + gap - time.time()
            if wait <= 0:
                _LAST[key] = time.time()
                return
        time.sleep(wait)


def rate_key(url: str) -> str:
    host = urllib.parse.urlsplit(url).hostname or ""
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def cache_path(cache_dir: str, url: str) -> str:
    return os.path.join(cache_dir, hashlib.sha1(url.encode()).hexdigest()[:24])


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # noqa: D401 - return None => do not follow
        return None


_OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url: str, cache_dir: str, do_fetch: bool, timeout: int = 60, headers: Mapping | None = None) -> dict:
    """{'status','location','body','set_cookie'}; status 0 = transport failure, -1 = not cached and not fetching.
    Redirects are NOT followed (the Location header is recorded)."""
    p = cache_path(cache_dir, url)
    if os.path.exists(p + ".json"):
        with open(p + ".json") as fh, open(p + ".bin", "rb") as fb:
            meta = json.load(fh)
            return {**meta, "body": fb.read()}
    if not do_fetch:
        return {"url": url, "status": -1, "location": "", "set_cookie": "", "body": b""}
    throttle(rate_key(url))
    try:
        with _OPENER.open(urllib.request.Request(url, headers={**UA, **(headers or {})}), timeout=timeout) as r:
            meta = {"status": r.status, "location": r.headers.get("Location", "") or "",
                    "set_cookie": "; ".join(r.headers.get_all("Set-Cookie") or [])}
            body = r.read()
    except urllib.error.HTTPError as e:
        meta = {"status": e.code, "location": e.headers.get("Location", "") or "",
                "set_cookie": "; ".join(e.headers.get_all("Set-Cookie") or [])}
        try:
            body = e.read() or b""
        except Exception:  # noqa: BLE001
            body = b""
    except Exception as e:  # noqa: BLE001 - transport failures are data
        meta, body = {"status": 0, "location": "", "set_cookie": "", "error": type(e).__name__}, b""
    meta = {"url": url, "retrieved": RETRIEVED, **meta}
    os.makedirs(cache_dir, exist_ok=True)
    with open(p + ".json", "w") as fh, open(p + ".bin", "wb") as fb:
        json.dump(meta, fh)
        fb.write(body)
    return {**meta, "body": body}


def fetch_follow(url: str, cache_dir: str, do_fetch: bool, hops: int = 4) -> dict:
    r = fetch(url, cache_dir, do_fetch)
    while hops and r.get("status") in (301, 302, 303, 307, 308) and r.get("location"):
        url, hops = urllib.parse.urljoin(url, r["location"]), hops - 1
        r = fetch(url, cache_dir, do_fetch)
    return r


def fetch_json(url: str, cache_dir: str, do_fetch: bool, timeout: int = 120, headers: Mapping | None = None):
    r = fetch(url, cache_dir, do_fetch, timeout, headers)
    try:
        return json.loads(r["body"].decode("utf-8", "replace")) if r["status"] == 200 else None
    except ValueError:
        return None


def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return tuple(csv.DictReader(fh))


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows({k: ("" if r.get(k) is None else r.get(k)) for k in fields} for r in rows)


def group_by(items: Iterable, key) -> dict:
    acc = defaultdict(list)
    for it in items:
        acc[key(it)].append(it)
    return {k: tuple(v) for k, v in acc.items()}


# ----------------------------------------------------------------------------- seeds
IPHI_RE = re.compile(r"(?:https?://)?((?:[a-z0-9-]+\.)?iphiview\.com)(/[a-z0-9_-]+)?", re.I)
STOP = frozenset("OF THE AND INC FOR A AN AT IN ON TO CO CORP CORPORATION LLC LTD TR TRUST'S &".split())
FIXED_LABELS = (
    # banks, brokers, trust companies and wealth firms
    "pnc", "truist", "ubs", "suntrust", "bbt", "bbandt", "jpm", "jpmorgan", "jpmc", "chase", "wellsfargo", "wf",
    "wfa", "citi", "citigroup", "citibank", "schwab", "fidelity", "vanguard", "merrill", "ml", "bofa", "boa",
    "bankofamerica", "usbank", "usb", "bny", "bnym", "bnymellon", "mellon", "northerntrust", "ntrs", "nt",
    "keybank", "key", "fifththird", "53", "regions", "huntington", "bmo", "citizens", "td", "hsbc", "rbc",
    "edwardjones", "ej", "ameriprise", "ampf", "lpl", "stifel", "raymondjames", "rj", "rjf", "baird", "janney",
    "morganstanley", "ms", "msgift", "gs", "goldman", "gspf", "gsgives", "wilmington", "wilmingtontrust", "mtb",
    "comerica", "frost", "glenmede", "bessemer", "fiduciary", "tiaa", "nuveen", "thrivent", "infaith", "pershing",
    "fisher", "nwm", "northwestern", "principal", "lincoln", "nationwide", "prudential", "voya", "massmutual",
    "ayco", "eqt", "equitable", "cafa", "cfa", "caf", "ccfnj", "ocf", "sci", "azzad", "rcf", "aef", "npt",
    "impactassets", "assetmark", "ncf", "waterstone", "ccf", "signatry", "servant", "rsf", "jcf", "jfn",
    "trowe", "troweprice", "stifelcharitable", "agf", "acf", "ncfgiving", "givingpoint", "dafgiving360",
    "maintenance", "www", "demo", "test", "staging", "stg", "dev", "uat", "sandbox", "training", "admin",
    "api", "auth", "sso", "help", "support", "status", "secure", "portal", "donor", "donorview", "granteeview",
    "iphi", "stellar", "ren", "renaissance", "cfgm", "cfcf", "gccf", "truistfe", "fe", "f-e", "scbf",
    "bremer", "associated", "oldnational", "firsthorizon", "synovus", "umb", "commerce", "zions", "pinnacle",
    "atlantic", "cadence", "hancock", "trustmark", "bok", "bokf", "arvest", "simmons", "firstcitizens", "fnb",
    "wintrust", "webster", "valley", "fulton", "mtbank", "peoples", "unitedbank", "first", "heartland",
)


def repo_iphi_mentions(root: str) -> tuple[tuple[str, str, str], ...]:
    """(host, path, file) for every iphiview.com host/path cited in research/ and data/ text files."""
    pats = ("research/**/*.md", "data/**/*.csv", "data/**/*.json")
    files = sorted({f for p in pats for f in glob.glob(os.path.join(root, p), recursive=True)})
    files = [f for f in files if os.path.basename(f) not in {os.path.basename(OUT_CENSUS), os.path.basename(OUT_SUMMARY)}]

    def scan(f: str):
        try:
            txt = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            return ()
        return tuple((m.group(1).lower(), (m.group(2) or "").lower(), os.path.relpath(f, root)) for m in IPHI_RE.finditer(txt))
    return tuple(x for f in files for x in scan(f))


def label_of(host: str) -> str:
    h = host.lower()
    return "" if h == "iphiview.com" else h[: -len(".iphiview.com")]


def acronyms(name: str) -> tuple[str, ...]:
    words = re.findall(r"[A-Za-z0-9]+", name.upper().replace("&", " "))
    keep_the = [w for w in words if w not in STOP or w == "THE"]
    no_the = [w for w in words if w not in STOP]
    return tuple({"".join(w[0] for w in ws).lower() for ws in (keep_the, no_the) if len(ws) >= 2})


def domain_stem(url: str) -> str:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    host = re.sub(r"^(www\d?|m)\.", "", host)
    return host.split(".")[0] if host else ""


def valid_label(s: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]([a-z0-9-]{0,40}[a-z0-9])?", s or ""))


def guess_labels(cfmap: Sequence[Mapping], universe: Sequence[Mapping]) -> tuple[str, ...]:
    from_map = [x for r in cfmap for x in (domain_stem(r.get("homepage", "")),) + acronyms(r.get("name", ""))]
    from_uni = [x for r in universe for x in acronyms(r.get("sponsor_name", ""))]
    return tuple(sorted({x for x in from_map + from_uni + list(FIXED_LABELS) if valid_label(x)}))


# ----------------------------------------------------------------------------- certificate transparency
CT_DOMAINS = ("iphiview.com", "stellartechsol.com", "donorfirstx.com", "reninc.com", "spectrumportal.net")


def ct_rows(domain: str, cache_dir: str, do_fetch: bool) -> tuple[dict, ...]:
    """Named-host certificate ranges from crt.sh (bare-domain identity query); falls back to certspotter."""
    data = fetch_json(f"https://crt.sh/?q={domain}&output=json", cache_dir, do_fetch, timeout=180)
    src = "crt.sh"
    if data is None:
        data = fetch_json(f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names",
                          cache_dir, do_fetch)
        src = "certspotter"
        data = tuple({"name_value": "\n".join(d.get("dns_names", [])), "not_before": d.get("not_before", "")} for d in (data or ()))
    return tuple({"domain": domain, "name": n.strip().lower(), "not_before": (d.get("not_before") or "")[:10], "source": src}
                 for d in (data or ()) for n in (d.get("name_value") or "").split("\n") if n.strip())


def ct_ranges(rows: Sequence[Mapping]) -> dict[str, tuple[str, str, int, str]]:
    g = group_by(rows, lambda r: r["name"])
    return {n: (min(x["not_before"] for x in v), max(x["not_before"] for x in v), len(v), v[0]["source"]) for n, v in g.items()}


# ----------------------------------------------------------------------------- DNS
DOH = ("https://dns.google/resolve?name={}&type=A", "https://cloudflare-dns.com/dns-query?name={}&type=A")


def doh(name: str, i: int, cache_dir: str, do_fetch: bool) -> dict:
    url = DOH[i % 2].format(name)
    d = fetch_json(url, cache_dir, do_fetch, timeout=30, headers={"accept": "application/dns-json"})
    if d is None:  # try the other resolver once
        url = DOH[(i + 1) % 2].format(name)
        d = fetch_json(url, cache_dir, do_fetch, timeout=30, headers={"accept": "application/dns-json"})
    if d is None:
        return {"name": name, "dns_status": "ERROR", "cname": "", "a": "", "dns_url": url}
    ans = d.get("Answer") or []
    return {"name": name, "dns_status": {0: "NOERROR", 3: "NXDOMAIN", 2: "SERVFAIL"}.get(d.get("Status"), str(d.get("Status"))),
            "cname": " ".join(a["data"].rstrip(".") for a in ans if a.get("type") == 5),
            "a": " ".join(a["data"] for a in ans if a.get("type") == 1),
            "dns_url": DOH[0].format(name)}


def sock_dns(name: str) -> dict:
    """System-resolver lookup (used for the small spectrumportal set; not cached, so recorded as of the run)."""
    import socket
    try:
        cn, _, ips = socket.gethostbyname_ex(name)
        return {"name": name, "dns_status": "NOERROR", "cname": cn if cn != name else "", "a": " ".join(ips), "dns_url": ""}
    except socket.gaierror as e:
        return {"name": name, "dns_status": "NXDOMAIN" if e.errno in (-2, -5) else f"ERR{e.errno}", "cname": "", "a": "", "dns_url": ""}


def dns_sweep(names: Sequence[str], cache_dir: str, do_fetch: bool) -> dict[str, dict]:
    with ThreadPoolExecutor(max_workers=2) as ex:
        res = list(ex.map(lambda t: doh(t[1], t[0], cache_dir, do_fetch), enumerate(names)))
    return {r["name"]: r for r in res}


def hosting(dns: Mapping) -> str:
    if "ren-workload" in dns.get("cname", ""):
        return "ren-workload-02 ELB (AWS)"
    if set(dns.get("a", "").split()) & {"35.71.183.32", "13.248.164.2"}:
        return "AWS Global Accelerator pair (35.71.183.32 / 13.248.164.2)"
    return ("other: " + (dns.get("cname") or dns.get("a", ""))[:60]) if dns.get("dns_status") == "NOERROR" else ""


# ----------------------------------------------------------------------------- page parsing (pure)
def meta(body: str, mid: str) -> str:
    m = re.search(r'<meta[^>]+id="Meta%s"[^>]*content="([^"]*)"' % mid, body, re.I) or \
        re.search(r'<meta[^>]+name="%s"[^>]*content="([^"]*)"' % mid, body, re.I)
    return html.unescape(m.group(1)).strip() if m else ""


def plain(body: str) -> str:
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip()


BANNER = re.compile(r"(moving to a new (?:system|platform|portal)[^.]{0,160}\.|new (?:donor|fund|fundholder) portal[^.]{0,160}\.|"
                    r"no longer (?:available|in use|be used)[^.]{0,120}\.|transition(?:ed|ing)? to [^.]{0,140}\.|"
                    r"has been retired[^.]{0,120}\.|please (?:visit|use) our new [^.]{0,120}\.)", re.I)


def page_facts(r: Mapping) -> dict:
    body = r.get("body", b"").decode("utf-8", "replace")
    txt = plain(body)
    years = re.findall(r"(?:©|&copy;|\(c\)|copyright)\s*(?:20\d\d\s*[-–]\s*)?(20\d\d)", body, re.I)
    title = re.search(r"(?is)<title[^>]*>(.*?)</title>", body)
    welcome = re.search(r"(Welcome to [^.|]{3,60}?)(?: Sign in| Log ?in| User| Username|$)", txt)
    return {"status": r.get("status"), "location": r.get("location", ""),
            "author": meta(body, "Author"), "copyright_meta": meta(body, "Copyright"), "description": meta(body, "Description"),
            "title": re.sub(r"\s+", " ", html.unescape(title.group(1))).strip()[:120] if title else "",
            "footer_year": max(years) if years else "", "banner": "; ".join(sorted({m.group(1)[:200] for m in BANNER.finditer(txt)}))[:400],
            "welcome": welcome.group(1).strip() if welcome else "",
            "iphi_markers": ";".join(k for k, pat in (("iPhiSession_cookie", r"iPhiSession"), ("DNN_LogIn_tabid", r"LogIn/tabid"),
                                                       ("Stellar_text", r"Stellar Technology"), ("DotNetNuke", r"DotNetNuke|dnn_"))
                                      if re.search(pat, body + r.get("set_cookie", ""), re.I))}


# ----------------------------------------------------------------------------- manual first-party evidence
# Organisation mapping and status evidence for tenants the CF map does not cover. Each row cites a source URL
# (all already in the repo or fetched by this script). ein '' = no EIN established.
MANUAL = {
    "npt.iphiview.com/npt": {"ein": "232617233", "org": "National Philanthropic Trust", "org_type": "national_sponsor",
        "note": "npt.iphiview.com 301 -> nptgivingpoint.org (Ren-hosted, ren-workload-02); iPhi lineage behind NPT GivingPoint (queue-vendor-scope-ren-denominator.md)",
        "src": "https://npt.iphiview.com/npt/LogIn/tabid/444/Default.aspx?returnurl=%2fnpt%2f"},
    "impactassets.iphiview.com/impactassets": {"ein": "262048480", "org": "ImpactAssets", "org_type": "national_sponsor",
        "note": "Stellar 'technology services' $232,315 TY2024; Give Interactive staging/production certificates (queue-vendor-scope)",
        "src": "https://projects.propublica.org/nonprofits/organizations/262048480/202543169349307999/full"},
    "impactassets.iphiview.com/assetmark": {"ein": "262048480", "org": "ImpactAssets (AssetMark program)", "org_type": "national_sponsor",
        "note": "AssetMark white-label path on the ImpactAssets tenant", "src": "https://impactassets.iphiview.com/assetmark/"},
    "infaith.iphiview.com/infaith": {"ein": "411802412", "org": "Thrivent Charitable Impact & Investing", "org_type": "faith_affinity_sponsor",
        "note": "Stellar $270,307 TY2024; Renaissance Acquisition Co 'technology services' $479,172 TY2025; Give Interactive staging tenant",
        "src": "https://www.thriventcharitable.com/"},
    "gccf.iphiview.com/gccf": {"ein": "", "org": "Gulf Coast Community Foundation (which one unverified)", "org_type": "community_foundation",
        "note": "EIN not established (queue-vendor-scope: 'which Gulf Coast is unverified')", "src": "https://gccf.iphiview.com/gccf/"},
    "cfcf.iphiview.com/cfcf": {"ein": "", "org": "Catholic Foundation of Central Florida", "org_type": "faith_affinity_sponsor",
        "note": "no DAFRC match in repo", "src": "https://cfcf.iphiview.com/cfcf/"},
    "rcf.iphiview.com/azzad": {"ein": "352049116", "org": "Renaissance Charitable Foundation (Azzad program)", "org_type": "national_sponsor",
        "note": "RCF white-label program on iPhi host", "src": "https://rcf.iphiview.com/azzad/"},
    "truist.iphiview.com/truist": {"ein": "", "org": "Truist Financial Corporation (F&E ClientView)", "org_type": "bank_trust_reporting",
        "note": "Login page reads 'Welcome to F&E ClientView' (Foundations & Endowments client reporting); no DAF or sponsor named",
        "src": "https://truist.iphiview.com/truist/"},
    "pnc.iphiview.com/scbf": {"ein": "", "org": "PNC (path /scbf; program unnamed)", "org_type": "bank_platform",
        "note": "root 301 -> /scbf which returns IIS 404; host still on ren-workload-02 ELB. PNC Institutional Asset Management launched the white-label 'PNC Gifting Portal' DAF platform for nonprofit sponsors on 2021-03-08 [candidate, not proven]",
        "src": "https://pnc.iphiview.com/"},
    "ubs.iphiview.com/": {"ein": "232617233", "org": "UBS Donor Advised Fund (NPT-sponsored) [I]", "org_type": "bank_program",
        "note": "root 301 -> https://donoradvisedfund.ubs.com/ (UBS-owned host); UBS DAF launched 2008 with NPT as sponsor [R press]; counted inside NPT",
        "src": "https://ubs.iphiview.com/"},
}
# Sponsor-level status evidence for non-CF sponsors (990-only or tenant-less). Each: status, destination, date, basis, url.
MANUAL_STATUS = {
    "751750059": ("migrated", "Give Interactive", "2025 [I]", "WaterStone (Christian Community Foundation Inc): Stellar paid through FYE 3/2025 ($366,469); queue-vendor-scope tier C lists it as 'now on Give' (historical / moved)",
                  "https://projects.propublica.org/nonprofits/organizations/751750059/202610409349301411/full"),
    "237174183": ("migrated", "Give Interactive", "by FYE 6/2023", "JCF 990 TY2022 pays Renaissance Acquisition Co for 'PREVIOUS DONOR PORTAL SUPPORT' $417,742, i.e. the Ren/iPhi portal was already the previous system; JCF is a Give Interactive client (queue-vendor-scope)",
                  "https://projects.propublica.org/nonprofits/organizations/237174183"),
}

# Map-family strings that mean "the sponsor's current fund login is not iPhi"
NON_IPHI = re.compile(r"foundant|akoya|salesforce|foundation cloud|blackbaud|donorsphere|giftingnetwork|give interactive|fund-miner|power pages|smartsimple", re.I)


# ----------------------------------------------------------------------------- joins (pure)
REN_990 = re.compile(r"stellar|\bren\b|renpsg|ren psg|renaissance (acquisition|philanthropic)|^renaissance$|ren technology", re.I)


def ren_lines(harvest: Sequence[Mapping]) -> dict[str, tuple[dict, ...]]:
    rows = [r for r in harvest if REN_990.search(r.get("contractor_name", "")) or "Ren" in r.get("vendor_entity", "") or "Stellar" in r.get("vendor_entity", "")]
    return group_by(rows, lambda r: r["ein"])


def tenant_hosts_from_signals(signals: Sequence[Mapping]) -> dict[str, set]:
    """tenant key 'host/path' -> {ein} for CF-map signals that link to an iPhi tenant; plus login_context flags."""
    acc = defaultdict(set)
    for s in signals:
        for m in IPHI_RE.finditer(s.get("detail", "") + " " + s.get("evidence_url", "")):
            acc[(m.group(1).lower() + (m.group(2) or "").lower())].add(s["ein"])
    return acc


def tenant_key(host: str, path: str) -> str:
    return host + (path if path else "/")


def classify(t: Mapping) -> tuple[str, str, str, str]:
    """(status, destination_vendor, exit_date, basis). Pure function of the joined row."""
    mv = t.get("migration_event")
    if t.get("org_type") in ("bank_trust_reporting",):
        return "out_of_scope", "", "", "Not a DAF/CF donor portal (trust/foundation client reporting)"
    if mv:
        return "migrated", mv["to_system"], mv["event_date"] or "undated", f"cf-vendor-migrations-2022-2026.csv: {mv['direction'][:140]}"
    if t.get("manual_status"):
        s = t["manual_status"]
        return s[0], s[1], s[2], s[3]
    cur = t.get("map_portal_vendor", "")
    if cur and NON_IPHI.search(cur) and "iPhi" not in cur:
        return "migrated", cur, "undated", f"CF map 2026-11-14: current fund login is {cur} ({t.get('map_portal_url','')[:80]})"
    if t["dns_status"] == "NXDOMAIN":
        return "lapsed", "", "undated", "iPhi host NXDOMAIN 2026-11-15 and no destination evidenced"
    if t.get("tenant_status") in (404, 410) and not t.get("root_location_external"):
        return "lapsed", "", "undated", f"iPhi tenant path returns HTTP {t.get('tenant_status')} on 2026-11-15"
    if t.get("root_location_external"):
        return "active", "", "", f"host redirects to sponsor-owned/branded host {t['root_location_external']} (Ren-hosted front end) [I]"
    if t.get("tenant_status") == 200 and t.get("author"):
        if t.get("banner"):
            return "migrating", "", "", f"live iPhi login with transition banner: {t['banner'][:120]}"
        return "active", "", "", "live iPhi login page with sponsor identity; " + ("sponsor homepage links it (CF map)" if t.get("map_links_tenant") else "no current homepage link in CF map")
    return "unknown", "", "", f"dns={t['dns_status']} root={t.get('root_status')} tenant={t.get('tenant_status')}"


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


# ----------------------------------------------------------------------------- task: census
def census(cache_dir: str, do_fetch: bool) -> dict:
    cfmap, signals, harvest = read_csv(CFMAP), read_csv(SIGNALS), read_csv(HARVEST)
    universe, migr = read_csv(UNIVERSE), read_csv(MIGR)
    by_ein = {r["ein"]: r for r in cfmap}
    uni_by_ein = {r["ein"]: r for r in universe}
    ren990 = ren_lines(harvest)
    events = {r["ein"]: r for r in migr if r["record_type"] == "event" and "iPhi" in r.get("from_system", "")}

    mentions = repo_iphi_mentions(ROOT)
    junk = lambda h: bool(re.fullmatch(r"\d+", label_of(h)))  # e.g. '%25.iphiview.com' URL-encoding residue
    repo_hosts = sorted({h for h, _, _ in mentions if not junk(h)})
    repo_paths = sorted({(h, p) for h, p, _ in mentions if p and not junk(h)})
    ct = tuple(x for d in CT_DOMAINS for x in ct_rows(d, cache_dir, do_fetch))
    ctr = ct_ranges(ct)
    ct_iphi_hosts = sorted({n for n in ctr if n.endswith(".iphiview.com") and not n.startswith("*")})
    guesses = guess_labels(cfmap, universe)
    labels = sorted({label_of(h) for h in repo_hosts + ct_iphi_hosts if label_of(h)} | set(guesses))
    wildcard_probe = doh("zz-nonexistent-probe-7q.iphiview.com", 0, cache_dir, do_fetch)
    dns = dns_sweep([f"{l}.iphiview.com" for l in labels], cache_dir, do_fetch)
    live_hosts = sorted(h for h, d in dns.items() if d["dns_status"] == "NOERROR" and d["a"])
    src_of = lambda h: ";".join(s for s, ok in (("repo", h in repo_hosts), ("ct", h in ct_iphi_hosts),
                                                ("dns_guess", label_of(h) in guesses)) if ok)

    # tenant instances: (host, path). Live hosts get /<label>/; repo-cited paths are added; cited-but-dead hosts too.
    inst = sorted({(h, "/" + label_of(h)) for h in live_hosts if label_of(h) not in ("www", "maintenance")} |
                  {(h, p) for h, p in repo_paths} |
                  {(h, "/" + label_of(h)) for h in repo_hosts + ct_iphi_hosts if label_of(h) and label_of(h) not in ("www", "maintenance")})
    roots = {h: page_facts(fetch(f"https://{h}/", cache_dir, do_fetch)) for h in sorted({h for h, _ in inst} | set(live_hosts))
             if dns.get(h, {}).get("dns_status") == "NOERROR" or h == "www.iphiview.com"}
    pages = {(h, p): page_facts(fetch(f"https://{h}{p}/", cache_dir, do_fetch)) for h, p in inst
             if h in roots}
    # drop path instances that are pure 404 on a host whose root redirects elsewhere (keep one row per host)
    sig_tenants = tenant_hosts_from_signals(signals)

    def map_eins(h: str, p: str) -> set:
        key = h + p
        return set().union(*(v for k, v in sig_tenants.items() if k == key or (not p and k.startswith(h)))) if sig_tenants else set()

    def row(h: str, p: str) -> dict:
        d = dns.get(h, {"dns_status": "not_queried", "cname": "", "a": "", "dns_url": ""})
        rt, pg = roots.get(h, {}), pages.get((h, p), {})
        key = tenant_key(h, p)
        man = MANUAL.get(key) or MANUAL.get(h + "/")
        eins = sorted(map_eins(h, p)) or ([man["ein"]] if man and man.get("ein") else [])
        ein = eins[0] if eins else ""
        m = by_ein.get(ein, {})
        lines = ren990.get(ein, ())
        loc = rt.get("location", "")
        ext = loc if loc and "iphiview.com" not in loc and loc.startswith("http") else ""
        ctn = ctr.get(h)
        out = {
            "tenant_key": key, "host": h, "path": p, "label": label_of(h),
            "product": ("iPhi F&E ClientView (trust reporting)" if man and man.get("org_type") == "bank_trust_reporting" else "Ren (Stellar) iPhi"),
            "org_identity_meta_author": pg.get("author") or rt.get("author") or "",
            "org": (man or {}).get("org") or m.get("name") or uni_by_ein.get(ein, {}).get("sponsor_name", ""),
            "org_type": (man or {}).get("org_type") or ("community_foundation" if ein in by_ein else (uni_by_ein.get(ein, {}).get("type", "").lower() or "")),
            "ein": ein, "eins_all": " ".join(eins),
            "fy2024_daf_assets_usd": m.get("fy2024_daf_assets_usd") or uni_by_ein.get(ein, {}).get("fy2024_daf_assets", ""),
            "discovery": src_of(h) + (";cf_map_link" if map_eins(h, p) else ""),
            "dns_status": d["dns_status"], "dns_cname": d["cname"], "dns_a": d["a"], "hosting": hosting(d), "dns_evidence_url": d["dns_url"],
            "root_status": rt.get("status", ""), "root_location": loc, "root_location_external": ext,
            "tenant_url": f"https://{h}{p}/", "tenant_status": pg.get("status", ""), "tenant_location": pg.get("location", ""),
            "author": pg.get("author", ""), "copyright_meta": pg.get("copyright_meta", ""), "footer_year": pg.get("footer_year", ""),
            "welcome_text": pg.get("welcome", ""), "banner": pg.get("banner", ""), "iphi_markers": pg.get("iphi_markers", ""),
            "ct_named_first": ctn[0] if ctn else "", "ct_named_last": ctn[1] if ctn else "", "ct_named_count": ctn[2] if ctn else 0,
            "map_portal_vendor": m.get("portal_vendor", ""), "map_portal_url": m.get("portal_url", ""),
            "map_links_tenant": "yes" if map_eins(h, p) else "no",
            "map_conflicting_signals": m.get("conflicting_signals", "")[:200],
            "ren_990_lines": " | ".join(f"TY{x['tax_year']} {x['contractor_name'][:28]} '{x['services'][:28]}' ${int(float(x['compensation'])):,}" for x in sorted(lines, key=lambda x: x["tax_year"])),
            "ren_990_last_ty": max((x["tax_year"] for x in lines), default=""),
            "migration_event": events.get(ein), "manual_status": MANUAL_STATUS.get(ein),
            "manual_note": (man or {}).get("note", ""), "manual_src": (man or {}).get("src", ""),
        }
        st, dest, date, basis = classify(out)
        return {**out, "status": st, "destination_vendor": dest, "exit_date": date, "status_basis": basis}

    rows = collapse([row(h, p) for h, p in inst], {h + p for h, p in repo_paths})
    # 990-only Stellar/Ren payees with no tenant row (scope: Stellar-named payee = iPhi product lineage)
    have = {r["ein"] for r in rows if r["ein"]}
    extra = []
    for ein, lines in sorted(ren990.items()):
        if ein in have:
            continue
        stellar = any("stellar" in x["contractor_name"].lower() for x in lines)
        tech = any(re.search(r"tech|software|portal|platform|system|it serv|computer|web", x["services"], re.I) for x in lines)
        m, u = by_ein.get(ein, {}), uni_by_ein.get(ein, {})
        base = {"tenant_key": f"990-only:{ein}", "host": "", "path": "", "label": "", "product": "Ren (Stellar) iPhi [990 payee]" if stellar else "Ren platform (product not identified) [990 payee]",
                "org": m.get("name") or u.get("sponsor_name") or lines[0]["sponsor_name"], "org_type": "community_foundation" if ein in by_ein else (u.get("type", "") or lines[0].get("sponsor_type", "")).lower(),
                "ein": ein, "eins_all": ein, "fy2024_daf_assets_usd": m.get("fy2024_daf_assets_usd") or u.get("fy2024_daf_assets", ""),
                "discovery": "990_harvest", "dns_status": "", "map_portal_vendor": m.get("portal_vendor", ""), "map_portal_url": m.get("portal_url", ""),
                "map_links_tenant": "no", "ren_990_lines": " | ".join(f"TY{x['tax_year']} {x['contractor_name'][:28]} '{x['services'][:28]}' ${int(float(x['compensation'])):,}" for x in sorted(lines, key=lambda x: x["tax_year"])),
                "ren_990_last_ty": max(x["tax_year"] for x in lines), "migration_event": events.get(ein), "manual_status": MANUAL_STATUS.get(ein),
                "in_scope_hint": stellar or tech}
        if not (stellar or tech):
            continue
        mv, ms = base["migration_event"], base["manual_status"]
        cur = base["map_portal_vendor"]
        if mv:
            st = ("migrated", mv["to_system"], mv["event_date"] or "undated", "cf-vendor-migrations-2022-2026.csv")
        elif ms:
            st = ms[:4]
        elif cur and NON_IPHI.search(cur) and "iPhi" not in cur:
            st = ("migrated", cur, "undated", f"Stellar/Ren 990 payee but CF map 2026-11-14 current fund login is {cur}")
        elif int(base["ren_990_last_ty"]) >= 2024:
            st = ("active", "", "", f"990 payee in TY{base['ren_990_last_ty']} (latest harvested year); no iPhi host found by DNS guess")
        else:
            st = ("unknown", "", "", f"last Ren/Stellar 990 line TY{base['ren_990_last_ty']}; absence later is weak (> $100k top-5 listing threshold)")
        extra.append({**base, "status": st[0], "destination_vendor": st[1], "exit_date": st[2], "status_basis": st[3]})
    allrows = rows + extra

    for r in allrows:
        r["retrieved"] = RETRIEVED
        r["in_attrition_scope"] = in_scope(r)
        r["migration_event"] = (r["migration_event"] or {}).get("event_date", "") if isinstance(r.get("migration_event"), dict) else ""
        r["manual_status"] = "yes" if r.get("manual_status") else ""
    allrows.sort(key=lambda r: (r["in_attrition_scope"] != "yes", r["status"], -(float(r.get("fy2024_daf_assets_usd") or 0)), r["tenant_key"]))
    write_csv(OUT_CENSUS, allrows, CENSUS_FIELDS)
    summary = attrition_summary(allrows)
    summary.update({"labels_queried": len(labels), "guess_labels": len(guesses), "repo_hosts": len(repo_hosts),
                    "ct_named_iphiview_hosts": ct_iphi_hosts, "live_iphiview_hosts": live_hosts,
                    "wildcard_probe": wildcard_probe["dns_status"],
                    "nxdomain_repo_or_ct_hosts": sorted(h for h in repo_hosts + ct_iphi_hosts if dns.get(h, {}).get("dns_status") == "NXDOMAIN"),
                    "ct_ranges": {k: v for k, v in ctr.items() if not k.startswith("*") and any(k.endswith(d) for d in CT_DOMAINS)},
                    "hosting_counts": dict(sorted({hk: sum(1 for r in rows if r.get("hosting") == hk) for hk in {r.get("hosting") for r in rows}}.items(), key=lambda x: str(x[0])))})
    with open(OUT_SUMMARY, "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True, default=str)
    return summary


def collapse(rows: Sequence[Mapping], cited: set) -> list:
    """One or more rows per host: every path answering 200 (plus MANUAL keys); for hosts with no 200 path, a single
    row, preferring a MANUAL key, then a repo-cited path, then the /<label> path."""
    out = []
    for h, rs in group_by(rows, lambda r: r["host"]).items():
        ok = [r for r in rs if r["tenant_status"] == 200 or r["tenant_key"] in MANUAL]
        if ok:
            out += ok
            continue
        pref = sorted(rs, key=lambda r: (r["tenant_key"] not in MANUAL, r["tenant_key"] not in cited, r["path"] != "/" + r["label"]))
        out.append(pref[0])
    return out


def in_scope(r: Mapping) -> str:
    """Attrition population: a DAF/CF sponsor evidenced as an iPhi client at some point since 2023-01-01."""
    if r["status"] == "out_of_scope" or r.get("org_type") in ("bank_platform",):
        return "no"
    if "Ren platform (product not identified)" in r.get("product", ""):
        return "no"
    if r["tenant_key"].startswith("990-only:"):
        return "yes" if (r.get("ren_990_last_ty") and int(r["ren_990_last_ty"]) >= 2022) else "no"
    if r.get("tenant_key", "").endswith("/assetmark") or r.get("tenant_key") == "ubs.iphiview.com/":
        return "no"  # sub-program of a sponsor already counted
    evid_2023 = (r["status"] in ("active", "migrating")) or (r.get("ren_990_last_ty") and int(r["ren_990_last_ty"]) >= 2023) or \
        (r["status"] == "migrated" and (r.get("exit_date", "")[:4] >= "2023" or r.get("exit_date") == "undated")) or \
        r.get("ct_named_last", "") >= "2023" or r.get("map_links_tenant") == "yes"
    return "yes" if evid_2023 else "no"


def attrition_summary(rows: Sequence[Mapping]) -> dict:
    pop = [r for r in rows if r["in_attrition_scope"] == "yes"]
    n = len(pop)
    exits = [r for r in pop if r["status"] in ("migrated", "lapsed")]
    dated = [r for r in exits if re.match(r"20(2[3-6])", r.get("exit_date", ""))]
    unk = [r for r in pop if r["status"] in ("unknown",)]
    migrating = [r for r in pop if r["status"] == "migrating"]
    assets = lambda rs: sum(float(r.get("fy2024_daf_assets_usd") or 0) for r in rs)
    k = len(exits)
    lo, hi = wilson(k, n)
    return {
        "population_n": n, "population_daf_assets_usd": assets(pop),
        "status_counts": {s: sum(1 for r in pop if r["status"] == s) for s in sorted({r["status"] for r in pop})},
        "exits_n": k, "exits_dated_2023_2026_n": len(dated), "unknown_n": len(unk), "migrating_n": len(migrating),
        "attrition_point": k / n if n else 0, "attrition_wilson95": [lo, hi],
        "attrition_lower_dated_only": len(dated) / n if n else 0,
        "attrition_upper_incl_unknown_and_migrating": (k + len(unk) + len(migrating)) / n if n else 0,
        "annualised_point": 1 - (1 - k / n) ** (1 / NOW_YEARS) if n and k < n else None,
        "exit_daf_assets_usd": assets(exits), "exit_asset_share": assets(exits) / assets(pop) if assets(pop) else 0,
        "destinations": {d: sum(1 for r in exits if (r["destination_vendor"] or "none evidenced") == d) for d in sorted({r["destination_vendor"] or "none evidenced" for r in exits})},
        "years_window": NOW_YEARS,
    }


CENSUS_FIELDS = (
    "tenant_key", "host", "path", "label", "product", "org", "org_identity_meta_author", "org_type", "ein", "eins_all",
    "fy2024_daf_assets_usd", "discovery", "dns_status", "dns_cname", "dns_a", "hosting", "dns_evidence_url",
    "root_status", "root_location", "tenant_url", "tenant_status", "tenant_location", "copyright_meta", "footer_year",
    "welcome_text", "banner", "iphi_markers", "ct_named_first", "ct_named_last", "ct_named_count",
    "map_portal_vendor", "map_portal_url", "map_links_tenant", "map_conflicting_signals", "ren_990_lines", "ren_990_last_ty",
    "migration_event", "status", "destination_vendor", "exit_date", "status_basis", "in_attrition_scope",
    "manual_note", "manual_src", "retrieved",
)


# ----------------------------------------------------------------------------- task: spectrum (P-BMG-02)
V990 = re.compile(r"blackbaud|npact|fusion lab|foundant|stellar|akoya|microedge|sage|armanino|redpath|clark nuber", re.I)
SITE_KW = re.compile(r"raiser'?s edge|financial edge|host\.nxt\.blackbaud\.com|bbox\.blackbaudhosting\.com|blackbaud|npact|foundation cloud|fims|communitysuite|fcsuite|foundant|iphiview|akoyago", re.I)


def spectrum(cache_dir: str, do_fetch: bool) -> tuple[dict, ...]:
    cfmap, harvest, signals, migr = read_csv(CFMAP), read_csv(HARVEST), read_csv(SIGNALS), read_csv(MIGR)
    ledg = {r["ein"]: r for r in read_csv(LEDGER)}
    h990 = group_by([r for r in harvest if V990.search(r["contractor_name"])], lambda r: r["ein"])
    mig = {r["ein"]: r for r in migr if r["record_type"] == "event"}
    sp = defaultdict(set)
    for s in signals:
        for m in re.finditer(r"https?://([a-z0-9-]+\.spectrumportal\.net)", s.get("detail", "") + " " + s.get("evidence_url", ""), re.I):
            sp[s["ein"]].add(m.group(1).lower())
    for r in cfmap:
        for m in re.finditer(r"https?://([a-z0-9-]+\.spectrumportal\.net)", r["portal_url"] + " " + r["evidence_detail"] + " " + r["conflicting_signals"], re.I):
            sp[r["ein"]].add(m.group(1).lower())
    byein = {r["ein"]: r for r in cfmap}
    out = []
    for ein in sorted(sp, key=lambda e: -float(byein.get(e, {}).get("fy2024_daf_assets_usd") or 0)):
        m = byein.get(ein, {})
        for host in sorted(sp[ein]):
            d = sock_dns(host)
            pg = page_facts(fetch(f"https://{host}/", cache_dir, do_fetch))
            si = page_facts(fetch(f"https://{host}/accounts/signin", cache_dir, do_fetch))
            home = fetch_follow(m.get("homepage", ""), cache_dir, do_fetch) if m.get("homepage") else {"body": b"", "status": ""}
            hometxt = home["body"].decode("utf-8", "replace")
            kws = sorted({k.group(0).lower() for k in SITE_KW.finditer(hometxt)})
            lines = h990.get(ein, ())
            fam = lambda pat: [x for x in lines if re.search(pat, x["contractor_name"], re.I)]
            bb, np_, fd = fam("blackbaud|microedge"), fam("npact|fusion lab"), fam("foundant")
            mv = mig.get(ein)
            sign_live = si["status"] == 200 and "Not Found" not in (si.get("title") or "")
            if mv and "Foundation Cloud" in (mv.get("from_system") or ""):
                role, ledger = "outgoing portal (migrated)", "Blackbaud (before migration) -> Foundant"
            elif mv and mv.get("to_system") == "n/a":
                role, ledger = "partner/grantee portal", "not a fund ledger front end"
            elif any(k in kws for k in ("host.nxt.blackbaud.com", "bbox.blackbaudhosting.com")):
                role, ledger = "fund portal (sign-in SPA served)" if sign_live else "portal (signin not live)", "Blackbaud RE NXT (homepage uses Blackbaud NXT/BBOX donation forms) [I]"
            elif np_:
                role, ledger = "fund portal (sign-in SPA served)" if sign_live else "portal (signin not live)", "NPact (Fusion Labs payee) [I]"
            elif bb:
                role, ledger = "fund portal (sign-in SPA served)" if sign_live else "portal (signin not live)", "Blackbaud (payee) [I]"
            else:
                role, ledger = "fund portal (sign-in SPA served)" if sign_live else "portal (signin not live)", "unknown (no 990 ledger payee > $100k)"
            out.append({"ein": ein, "name": m.get("name", ""), "fy2024_daf_assets_usd": m.get("fy2024_daf_assets_usd", ""), "host": host,
                        "dns_status": d["dns_status"], "dns_cname": d["cname"], "root_status": pg["status"], "root_title": pg["title"],
                        "signin_status": si["status"], "signin_title": si["title"], "map_portal_vendor": m.get("portal_vendor", ""),
                        "map_ledger_implied": m.get("ledger_implied", ""), "ledger_file_vendor": ledg.get(ein, {}).get("ledger_vendor", ""),
                        "homepage_keywords": ";".join(kws), "homepage_status": home.get("status", ""),
                        "signin_loads_bbcheckout": "yes" if "bbCheckout" in fetch(f"https://{host}/accounts/signin", cache_dir, do_fetch)["body"].decode("utf-8", "replace") else "no",
                        "blackbaud_990": " | ".join(f"TY{x['tax_year']} {x['contractor_name'][:24]} ${int(float(x['compensation'])):,}" for x in bb),
                        "npact_990": " | ".join(f"TY{x['tax_year']} {x['contractor_name'][:24]} '{x['services'][:24]}' ${int(float(x['compensation'])):,}" for x in np_),
                        "foundant_990": " | ".join(f"TY{x['tax_year']} ${int(float(x['compensation'])):,}" for x in fd),
                        "migration_event": (mv or {}).get("direction", "")[:160], "portal_role": role, "ledger_reading": ledger,
                        "ledger_implied_revised": "no (portal over Blackbaud)" if "Blackbaud" in ledger else ("yes [I]" if "NPact" in ledger else ("no" if "not a fund" in ledger else "unknown")),
                        "evidence_url": f"https://{host}/accounts/signin", "retrieved": RETRIEVED})
    write_csv(OUT_SPECTRUM, out, list(out[0].keys()) if out else ["ein"])
    return tuple(out)


# ----------------------------------------------------------------------------- task: rde (P-QA2-03)
PROGRAMS = (
    ("Renaissance Charitable Foundation", r"Renaissance Charitable|\bRCF\b"), ("American Endowment Foundation", r"American Endowment|\bAEF\b"),
    ("Morgan Stanley GIFT", r"Morgan Stanley|\bGIFT\b"), ("BofA Charitable Gift Fund", r"Bank of America|BofA"),
    ("Edward Jones Charitable Gift Fund", r"Edward Jones"), ("LPL", r"\bLPL\b"), ("Fisher Investments", r"Fisher Investments"), ("Pershing", r"Pershing"),
    ("Ameriprise", r"Ameriprise"), ("Stifel Charitable", r"Stifel"), ("T. Rowe Price", r"T\.? ?Rowe"), ("Thrivent", r"Thrivent"),
    ("NPT", r"National Philanthropic|\bNPT\b"), ("Goldman Sachs", r"Goldman"), ("UBS", r"\bUBS\b"), ("Northwestern Mutual", r"Northwestern Mutual|\bNWM\b"),
    ("Flex Giving Fund", r"Flex Giving"),
)
RDE_KW = re.compile(r"\bACH\b|electronic(?:ally)? (?:grant|payment|deliver|transfer|funds)|direct deposit|Rapid Disbursement|Ren for Charities|"
                    r"Powered by Ren|Charity Portal|25\+ donor-advised fund programs|every DAF program we support|called .Legacy", re.I)
RDE_PAGES = (
    ("Ren", "vendor", "https://www.reninc.com/payments/"),
    ("Ren", "vendor", "https://www.reninc.com/charities/"),
    ("Ren", "vendor", "https://intercom.help/rengiving/en/collections/11021724-charities"),
    ("Ren", "vendor", "https://intercom.help/rengiving/en/collections/11016041-general-daf"),
    ("American Endowment Foundation", "sponsor", "https://www.aefonline.org/charities/"),
    ("Renaissance Charitable Foundation", "sponsor", "https://renaissancecharitable.org/faqs/"),
    ("Renaissance Charitable Foundation", "sponsor", "https://renaissancecharitable.org/"),
    ("Edward Jones Charitable Gift Fund", "sponsor", "https://www.edwardjones.com/us-en/investment-services/charitable-giving"),
    ("Morgan Stanley GIFT", "sponsor", "https://msgift.donorfirstx.com/"),
    ("Morgan Stanley GIFT", "sponsor", "https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf"),
    ("BofA Charitable Gift Fund", "sponsor", "https://bofa.donorfirst.org/"),
    ("Ren", "vendor", "https://www.prnewswire.com/news-releases/ren-debuts-rapid-disbursement-engine-expanding-philanthropic-services-to-meet-rapid-daf-growth-301999647.html"),
)


def pdf_plain(body: bytes) -> str:
    """Best-effort text from an uncompressed or Flate PDF stream set (stdlib zlib); used for keyword search only."""
    import zlib
    chunks = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", body, re.S):
        try:
            chunks.append(zlib.decompress(m.group(1)))
        except zlib.error:
            chunks.append(m.group(1))
    raw = b" ".join(chunks).decode("latin-1", "replace")
    return re.sub(r"\s+", " ", " ".join(re.findall(r"\(([^)]{1,200})\)", raw)))


def rde_rows(owner: str, kind: str, url: str, r: Mapping) -> list:
    body = r["body"]
    txt = pdf_plain(body) if url.endswith(".pdf") else plain(body.decode("utf-8", "replace"))
    upd = re.search(r'"(?:updated_at|lastUpdated|dateModified|updatedAt|modified)"\s*:\s*"([0-9T:\-]{10})', body.decode("utf-8", "replace"))
    base = {"page_owner": owner, "page_kind": kind, "url": url, "http_status": r["status"], "page_updated": upd.group(1) if upd else "", "retrieved": RETRIEVED}
    if r["status"] != 200:
        return [{**base, "program": "(fetch failed)", "rde_keywords": "", "snippet": r.get("location", "") or r.get("error", "")}]
    out, seen = [], set()
    for k in RDE_KW.finditer(txt):
        ctx = txt[max(0, k.start() - 260): k.end() + 260]
        progs = [p for p, pat in PROGRAMS if re.search(pat, ctx)] or ["(no program named)"]
        for p in progs:
            key = (p, k.group(0).lower())
            if key in seen:
                continue
            seen.add(key)
            out.append({**base, "program": p, "rde_keywords": k.group(0), "snippet": re.sub(r"\s+", " ", ctx)[:520]})
    return out


def rde(cache_dir: str, do_fetch: bool) -> tuple[dict, ...]:
    pages = list(RDE_PAGES)
    for _, _, u in RDE_PAGES:  # expand help-centre collections into their article links
        if "intercom.help" in u and "/collections/" in u:
            body = fetch(u, cache_dir, do_fetch)["body"].decode("utf-8", "replace")
            pages += [("Ren", "vendor_help", a) for a in sorted(set(re.findall(r'href="(https://intercom\.help/rengiving/en/articles/[^"]+)"', body)))]
    out = [x for o, k, u in pages for x in rde_rows(o, k, u, fetch(u, cache_dir, do_fetch))]
    write_csv(OUT_RDE, out, ("page_owner", "page_kind", "url", "http_status", "page_updated", "program", "rde_keywords", "snippet", "retrieved"))
    return tuple(out)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--task", default="all", choices=("census", "spectrum", "rde", "all"))
    a = ap.parse_args(argv)
    if a.task in ("census", "all"):
        s = census(a.cache_dir, a.fetch)
        print(json.dumps({k: s[k] for k in ("population_n", "status_counts", "exits_n", "exits_dated_2023_2026_n", "attrition_point",
                                             "attrition_wilson95", "attrition_lower_dated_only", "attrition_upper_incl_unknown_and_migrating",
                                             "annualised_point", "exit_asset_share", "destinations", "labels_queried", "live_iphiview_hosts")}, indent=1, default=str))
    if a.task in ("spectrum", "all"):
        for r in spectrum(a.cache_dir, a.fetch):
            print("SPECTRUM", r["name"][:34], r["host"], r["signin_status"], r["signin_title"][:40], r["portal_role"], "|", r["ledger_reading"])
    if a.task in ("rde", "all"):
        rr = rde(a.cache_dir, a.fetch)
        print("RDE rows", len(rr), sorted({r["program"] for r in rr}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
