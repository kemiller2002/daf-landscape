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
    "iphi", "stellar", "ren", "renaissance", "cfgm", "cfcf", "gccf", "truistfe", "fe", "f-e", "scbf", "fuller", "kofc", "calvert", "faithwise",
    "bremer", "associated", "oldnational", "firsthorizon", "synovus", "umb", "commerce", "zions", "pinnacle",
    "atlantic", "cadence", "hancock", "trustmark", "bok", "bokf", "arvest", "simmons", "firstcitizens", "fnb",
    "wintrust", "webster", "valley", "fulton", "mtbank", "peoples", "unitedbank", "first", "heartland",
)


# this script's own outputs are excluded from the repo seed scan so reruns do not seed themselves
OWN_OUTPUTS = frozenset({"ren-iphi-tenant-census.csv", "ren-iphi-attrition-summary.json", "spectrumportal-tenant-audit.csv",
                         "ren-charity-ach-program-evidence.csv", "relationship-graph-edges-additions-11.csv",
                         "queue-proposals-ren-attrition.csv", "queue-ren-iphi-attrition.md"})


def repo_iphi_mentions(root: str) -> tuple[tuple[str, str, str], ...]:
    """(host, path, file) for every iphiview.com host/path cited in research/ and data/ text files."""
    pats = ("research/**/*.md", "data/**/*.csv", "data/**/*.json")
    files = sorted({f for p in pats for f in glob.glob(os.path.join(root, p), recursive=True)})
    files = [f for f in files if os.path.basename(f) not in OWN_OUTPUTS]

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
    if dns.get("a", "").startswith(LEGACY_NET):
        return "legacy 67.216.67.0/24 (dbsintl.net)"
    if "ren-workload" in dns.get("cname", "") or set(dns.get("a", "").split()) & {"44.223.132.165", "54.88.200.68"}:
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


BANNER = re.compile(r"(upgraded our (?:donor|fund) portal[^.]{0,160}\.|now lives in our new [^.]{0,200}\.|moving to a new (?:system|platform|portal|donor portal)[^.]{0,160}\.|new (?:donor|fund|fundholder) portal[^.]{0,160}\.|"
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
    "npt.iphiview.com/npt": {"ein": "237825575", "org": "National Philanthropic Trust", "org_type": "national_sponsor",
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
    "gccf.iphiview.com/gccf": {"ein": "591052433", "org": "Gulf Coast Community Foundation (Venice, FL)", "org_type": "community_foundation",
        "note": "Tenant page footer gives 601 Tamiami Trail South, Venice, FL, which identifies EIN 59-1052433 (resolves the 'which Gulf Coast' question)", "src": "https://gccf.iphiview.com/gccf/"},
    "cfcf.iphiview.com/cfcf": {"ein": "260879378", "org": "The Catholic Foundation of Central Florida [EIN by truncated-name match, I]", "org_type": "faith_affinity_sponsor",
        "note": "DAFRC name 'The Catholic Foundation of Central' (truncated); match is inferred", "src": "https://cfcf.iphiview.com/cfcf/"},
    "rcf.iphiview.com/azzad": {"ein": "352129262", "org": "Renaissance Charitable Foundation (Azzad program)", "org_type": "national_sponsor",
        "note": "RCF white-label program on iPhi host", "src": "https://rcf.iphiview.com/azzad/"},
    "truist.iphiview.com/truist": {"ein": "", "org": "Truist Financial Corporation (F&E ClientView)", "org_type": "bank_trust_reporting",
        "note": "Login page reads 'Welcome to F&E ClientView' (Foundations & Endowments client reporting); no DAF or sponsor named",
        "src": "https://truist.iphiview.com/truist/"},
    "bnym.iphiview.com/bnym": {"ein": "300748315", "org": "BNY Mellon Charitable Gift Fund", "org_type": "bank_program",
        "note": "bnym.iphiview.com 301 -> BNYMellonCharitableGiftFund.org, which resolves to the same AWS Global Accelerator pair as iPhi (answered HTTP 502 on 2026-11-15)", "src": "https://bnym.iphiview.com/"},
    "jpmc.iphiview.com/jpmc": {"ein": "237825575", "org": "J.P. Morgan Charitable Giving Fund (NPT program)", "org_type": "bank_program",
        "note": "jpmc.iphiview.com/jpmc 301 -> jpmgiving.org (ren-workload-02 ELB); bundle: 'GivingPoint for J.P. Morgan Private Bank', 'offered in conjunction with National Philanthropic Trust', renpsg.atlassian.net links", "src": "https://jpmgiving.org/"},
    "icgf.iphiview.com/icgf": {"ein": "237825575", "org": "ICGF Donor-Advised Fund (Independent Charitable Gift Fund; NPT program)", "org_type": "bank_program",
        "note": "icgf.iphiview.com/icgf 301 -> icgfdaf.org (iPhi Global Accelerator pair); bundle: 'The ICGF Donor-Advised Fund is a donor-advised fund offered in conjunction with the National Philanthropic Trust', GivingPoint, renpsg links", "src": "https://icgfdaf.org/"},
    "iphi.stellartechsol.com/calvert": {"ein": "262048480", "org": "ImpactAssets", "org_type": "national_sponsor",
        "note": "impactassets.org homepage login links iphi.stellartechsol.com/calvert/LogIn (MetaAuthor 'ImpactAssets')", "src": "https://impactassets.org/"},
    "ccfnj.iphiview.com/kofc": {"ein": "815466677", "org": "Knights of Columbus Charitable Fund Inc", "org_type": "faith_affinity_sponsor",
        "note": "ccfnj.iphiview.com/ccfnj 302 -> /kofc/ (MetaAuthor 'Knights of Columbus'); EIN by name match to DAFRC 'KNIGHTS OF COLUMBUS CHARITABLE FUND INC'", "src": "https://ccfnj.iphiview.com/kofc/"},
    "fuller.iphiview.com/fuller": {"ein": "954124436", "org": "FaithWise Advisors (tff -> fuller tenant) [EIN The Fuller Foundation, I]", "org_type": "faith_affinity_sponsor",
        "note": "tff.iphiview.com 301 -> fuller.iphiview.com/fuller (MetaAuthor 'FaithWise Advisors'); EIN match to 'THE FULLER FOUNDATION' is inferred", "src": "https://fuller.iphiview.com/fuller/"},
    "cfacadiana.iphiview.com/cfacadiana": {"ein": "721493023", "org": "Community Foundation of Acadiana", "org_type": "community_foundation",
        "note": "former iPhi host (NXDOMAIN); see cf-vendor-migrations-2022-2026.csv", "src": "https://dns.google/resolve?name=cfacadiana.iphiview.com&type=A"},
    "iphi.stellartechsol.com/ws": {"ein": "751750059", "org": "WaterStone (Christian Community Foundation Inc)", "org_type": "faith_affinity_sponsor",
        "note": "Legacy iPhi page: 'We've upgraded our Donor Portal. Your Giving Fund now lives in our new WaterStone Donor Portal at waterstone.giveinteractive.com'; waterstone.org links waterstone.giveinteractive.com",
        "src": "https://iphi.stellartechsol.com/ws/"},
    "iphi.stellartechsol.com/ubs": {"ein": "237825575", "org": "UBS Donor Advised Fund (NPT-sponsored) [I]", "org_type": "bank_program",
        "note": "iphi.stellartechsol.com/ubs 301 -> donoradvisedfund.ubs.com/ubs (legacy 67.216.67.0/24 range shared with dead iPhi hosts af/lcf/mccf)", "src": "https://iphi.stellartechsol.com/ubs/"},
    "bbt.iphiview.com/bbt": {"ein": "", "org": "Truist Financial Corporation (BB&T legacy alias; F&E ClientView)", "org_type": "bank_trust_reporting",
        "note": "Same 'Welcome to F&E ClientView' page as truist.iphiview.com", "src": "https://bbt.iphiview.com/bbt/"},
    "keybank.iphiview.com/keybank": {"ein": "", "org": "KeyBank (client log-in; product not stated)", "org_type": "bank_platform",
        "note": "Generic 'Client Log In' page, (c) 2021 KeyCorp; no DAF or sponsor named", "src": "https://keybank.iphiview.com/keybank/"},
    "eqt.iphiview.com/eqt": {"ein": "", "org": "Equity Trustees (Australia)", "org_type": "non_us_trustee",
        "note": "EQT Holdings (ASX: EQT) client portal; not a US DAF sponsor", "src": "https://eqt.iphiview.com/eqt/"},
    "rb.iphiview.com/rb": {"ein": "275098203", "org": "THE COMMUNITY FOUNDATION FOR ... (DAFRC truncated name, EIN 27-5098203) via a Regions Bank iPhi tenant", "org_type": "community_foundation",
        "note": "MetaAuthor 'Regions Bank'; 'Go to my Fund' -> Donor Dashboard; the CF map links it from a small CF's homepage", "src": "https://rb.iphiview.com/rb/"},
    "pnc.iphiview.com/scbf": {"ein": "", "org": "PNC (path /scbf; program unnamed)", "org_type": "bank_platform",
        "note": "root 301 -> /scbf which returns IIS 404; host still on ren-workload-02 ELB. PNC Institutional Asset Management launched the white-label 'PNC Gifting Portal' DAF platform for nonprofit sponsors on 2021-03-08 [candidate, not proven]",
        "src": "https://pnc.iphiview.com/"},
    "ubs.iphiview.com/": {"ein": "237825575", "org": "UBS Donor Advised Fund (NPT-sponsored) [I]", "org_type": "bank_program",
        "note": "root 301 -> https://donoradvisedfund.ubs.com/ (UBS-owned host); UBS DAF launched 2008 with NPT as sponsor [R press]; counted inside NPT",
        "src": "https://ubs.iphiview.com/"},
}
# EINs for tenant identities (MetaAuthor) by exact / truncated-name match to the 990 sponsor universe (DAFRC names).
AUTHOR_EIN = {
    "Arkansas Community Foundation": "521055743", "Baton Rouge Area Foundation": "726030391", "CAFAmerica": "431634280",
    "Dallas Seminary Foundation": "752188543", "Faithful Journey Foundation": "863667928", "Johnson Charitable Gift Fund": "300233491",
    "The Methodist Foundation of Mississippi": "640507167", "Missouri United Methodist Foundation": "430899770",
    "Palm Health Foundation": "592391119", "Raymond James Charitable Endowment Fund": "593652538", "RSF Social Finance": "136082763",
    "Stifel Charitable": "842049692", "Warren County Community Foundation": "251380549",
}
AUTHOR_EIN_NOTE = {"Palm Health Foundation": "DAFRC 'Palm Healthcare Foundation Inc' (former name) [I]",
                   "Warren County Community Foundation": "page address Warren, PA; DAFRC 'Community Foundation of Warren County' (25- prefix) [I]"}
NO_EIN = {"Barnabas Foundation", "Christian Financial Resources", "Georgia Baptist Foundation", "Mennonite Brethren Foundation",
          "Tennessee Baptist Foundation", "Community Foundation of Teton Valley"}  # not in the 1,512-sponsor 990 universe

# Sponsor-level status evidence for non-CF sponsors (990-only or tenant-less). Each: status, destination, date, basis, url.
MANUAL_STATUS = {
    "751750059": ("migrated", "Give Interactive", "2025-2026 [I]", "WaterStone: legacy iPhi page (iphi.stellartechsol.com/ws) says 'Your Giving Fund now lives in our new WaterStone Donor Portal at waterstone.giveinteractive.com'; Stellar still paid $366,469 in FYE 3/2025",
                  "https://iphi.stellartechsol.com/ws/"),
    "591052433": ("migrated", "Foundant CommunitySuite", "2026 [I] (in progress)", "Gulf Coast CF (Venice): CF map 2026-11-14 fund login is gulfcoastcf.fcsuite.com; legacy iPhi page: 'We're moving to a new Donor Portal experience launching soon'",
                  "https://gccf.iphiview.com/gccf/"),
    "311774905": ("active", "", "", "GS PWM DAF log-in gspf.goldman.com is iPhi (Stellar footer, iPhiSession cookie) on the ren-workload-02 ELB (queue-vendor-scope, validation-wave3 V3-01)",
                  "https://gspf.goldman.com/gspf/"),
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


DEST_VENDOR = (("tifingive.com", "TIFIN Give"), ("giveinteractive.com", "Give Interactive"), ("fcsuite.com", "Foundant CommunitySuite"),
               ("akoyago.com", "akoyaGO"), ("spectrumportal.net", "Foundation Cloud"))


def classify(t: Mapping) -> tuple[str, str, str, str]:
    """(status, destination_vendor, exit_date, basis). Pure function of the joined row."""
    mv = t.get("migration_event")
    if "F&E ClientView" in t.get("product", "") or t.get("org_type") in ("bank_trust_reporting", "non_us_trustee"):
        return "out_of_scope", "", "", "Not a US DAF/CF donor portal (trust/foundation client reporting or non-US trustee)"
    if mv:
        return "migrated", mv["to_system"], mv["event_date"] or "undated", f"cf-vendor-migrations-2022-2026.csv: {mv['direction'][:140]}"
    if t.get("manual_status"):
        s = t["manual_status"]
        return s[0], s[1], s[2], s[3]
    cur = t.get("map_portal_vendor", "")
    if cur and NON_IPHI.search(cur) and "iPhi" not in cur:
        return "migrated", cur, "undated", f"CF map 2026-11-14: current fund login is {cur} ({t.get('map_portal_url','')[:80]})"
    bdv = next((v for k, v in DEST_VENDOR if k in t.get("banner", "")), "")
    if bdv:
        return "migrated", bdv, "undated", f"legacy iPhi page names the new portal: {t['banner'][:200]}"
    ext = t.get("external_redirect", "")
    if ext:
        if t.get("redirect_dest_on_ren") and t.get("redirect_dest_status") != 200:
            return "unknown", "", "", f"redirects to {ext}, which resolves to Ren/iPhi hosting ({t.get('redirect_dest_hosting','')}) but answered HTTP {t.get('redirect_dest_status')} on 2026-11-15"
        if t.get("redirect_dest_on_ren"):
            return "active", "", "", f"redirects to Ren-hosted front end {ext} ({t.get('redirect_dest_hosting','')}; {t.get('redirect_dest_markers','') or 'no bundle markers'}; HTTP {t.get('redirect_dest_status')})"
        if "legacy" in t.get("redirect_dest_hosting", ""):
            return "unknown", "", "", f"redirects to {ext} on the legacy 67.216.67.0/24 (dbsintl.net) range; no HTTPS answer on 2026-11-15"
        dv = next((v for k, v in DEST_VENDOR if k in ext), "non-Ren host " + (urllib.parse.urlsplit(ext).hostname or ""))
        return "migrated", dv, "undated", f"iPhi path now 301-redirects to {ext} ({t.get('redirect_dest_hosting','')})"
    if t["dns_status"] == "NXDOMAIN":
        return "lapsed", "", "undated", "iPhi host NXDOMAIN 2026-11-15 and no destination evidenced"
    if "legacy" in t.get("hosting", "") and t.get("tenant_status") in (0, "", None):
        return "unknown", "", "", "host resolves to legacy 67.216.67.0/24 (dbsintl.net) range and gives no HTTPS answer; no identity"
    if t.get("tenant_status") in (404, 410):
        return "lapsed", "", "undated", f"iPhi tenant path returns HTTP {t.get('tenant_status')} on 2026-11-15"
    if t.get("tenant_status") == 200 and t.get("org_identity_meta_author"):
        if t.get("banner"):
            return "migrating", "", "", f"live iPhi login with transition banner: {t['banner'][:160]}"
        return "active", "", "", "live iPhi login page with sponsor identity; " + ("sponsor homepage links it (CF map)" if t.get("map_links_tenant") == "yes" else "no homepage link recorded in CF map")
    return "unknown", "", "", f"dns={t['dns_status']} root={t.get('root_status')} tenant={t.get('tenant_status')}"


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


STELLAR_RE = re.compile(r"(?:https?://)?((?:iphi|www|demo|npt)\.stellartechsol\.com)(/[a-z0-9_-]+)", re.I)
PATH_HOSTS = ("www.iphiview.com", "iphi.stellartechsol.com")  # hosts that serve several tenants as /<path>/
REN_IPS = {"35.71.183.32", "13.248.164.2", "44.223.132.165", "54.88.200.68"}
LEGACY_NET = "67.216.67."  # dbsintl.net range (PTR user-67-216-67-*.dbsintl.net); legacy pre-AWS hosting


def path_labels(universe: Sequence[Mapping]) -> tuple[str, ...]:
    """Labels probed as /<label>/ on the multi-tenant path hosts: acronyms of non-CF sponsors + the fixed list."""
    return tuple(sorted({x for r in universe if r.get("type") != "Community Foundation" for x in acronyms(r["sponsor_name"])
                         if valid_label(x)} | set(FIXED_LABELS)))


def follow_tenant(url: str, cache_dir: str, do_fetch: bool, hops: int = 3) -> tuple[dict, str, str]:
    """Fetch a tenant URL, following redirects that stay on Ren/iPhi hosts. Returns (facts, final_url, external_location)."""
    r = fetch(url, cache_dir, do_fetch)
    while hops and r.get("status") in (301, 302, 303, 307, 308) and r.get("location"):
        nxt = urllib.parse.urljoin(url, r["location"])
        host = urllib.parse.urlsplit(nxt).hostname or ""
        if not (host.endswith("iphiview.com") or host.endswith("stellartechsol.com")):
            return page_facts(r), url, nxt
        url, hops = nxt if nxt.endswith("/") else nxt + "/", hops - 1
        r = fetch(url, cache_dir, do_fetch)
    return page_facts(r), url, ""


def dest_facts(url: str, cache_dir: str, do_fetch: bool) -> dict:
    """Where an external redirect lands: DNS hosting class and, for the Angular 'GivingPoint' front end, bundle text."""
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    d = doh(host, 0, cache_dir, do_fetch)
    r = fetch_follow(url, cache_dir, do_fetch)
    body = r["body"].decode("utf-8", "replace")
    m = re.search(r'src="(main-[A-Z0-9]+\.js)"', body)
    js = fetch(urllib.parse.urljoin(url, m.group(1)), cache_dir, do_fetch)["body"].decode("utf-8", "replace") if m else ""
    prog = re.search(r"The ([^\"<>]{3,80}?) is a donor-advised fund offered in conjunction with (?:the )?National Philanthropic Trust", js)
    ips = set(d["a"].split())
    return {"dest_host": host, "dest_status": r.get("status"), "dest_hosting": hosting(d) or ("legacy 67.216.67.0/24 (dbsintl.net)" if d["a"].startswith(LEGACY_NET) else ""),
            "dest_on_ren": bool(ips & REN_IPS) or "ren-workload" in d["cname"],
            "dest_markers": ";".join(k for k, pat in (("GivingPoint", r"GivingPoint"), ("renpsg_jira", r"renpsg\.atlassian"), ("NPT", r"National Philanthropic Trust"))
                                     if re.search(pat, js)), "dest_program": prog.group(1) if prog else ""}


def org_type_of(in_cfmap: bool, u: Mapping, name: str) -> str:
    if u.get("subtype") == "Religiously-Affiliated":
        return "faith_affinity_sponsor"
    if in_cfmap or u.get("type") == "Community Foundation" or re.search(r"community foundation", name, re.I):
        return "community_foundation"
    if re.search(r"baptist|methodist|mennonite|christian|barnabas|catholic|jewish|seminary", name, re.I):
        return "faith_affinity_sponsor"
    return {"National": "national_sponsor", "Single Issue Charity": "single_issue_charity"}.get(u.get("type", ""), "")


def name_ein(author: str) -> tuple[str, str]:
    if author in AUTHOR_EIN:
        return AUTHOR_EIN[author], AUTHOR_EIN_NOTE.get(author, "exact name match to 990 sponsor universe")
    return "", ("not in the 1,512-sponsor 990 universe" if author in NO_EIN else "")


# ----------------------------------------------------------------------------- task: census
def census(cache_dir: str, do_fetch: bool) -> dict:
    cfmap, signals, harvest = read_csv(CFMAP), read_csv(SIGNALS), read_csv(HARVEST)
    universe, migr = read_csv(UNIVERSE), read_csv(MIGR)
    by_ein = {r["ein"]: r for r in cfmap}
    uni_by_ein = {r["ein"]: r for r in universe}
    ren990 = ren_lines(harvest)
    events = {r["ein"]: r for r in migr if r["record_type"] == "event" and "iPhi" in r.get("from_system", "")}

    mentions = repo_iphi_mentions(ROOT)
    junk = lambda h: bool(re.fullmatch(r"\d+", label_of(h))) or h == "iphiview.com"
    repo_hosts = sorted({h for h, _, _ in mentions if not junk(h)})
    repo_paths = sorted({(h, p) for h, p, _ in mentions if p and not junk(h)} | set(repo_stellar_paths(ROOT)))
    ct = tuple(x for d in CT_DOMAINS for x in ct_rows(d, cache_dir, do_fetch))
    ctr = ct_ranges(ct)
    ct_iphi_hosts = sorted({n for n in ctr if n.endswith(".iphiview.com") and not n.startswith("*")})
    guesses = guess_labels(cfmap, universe)
    labels = sorted({label_of(h) for h in repo_hosts + ct_iphi_hosts if label_of(h)} | set(guesses))
    wildcard_probe = doh("zz-nonexistent-probe-7q.iphiview.com", 0, cache_dir, do_fetch)
    dns = dns_sweep([f"{l}.iphiview.com" for l in labels], cache_dir, do_fetch)
    for h in ("iphi.stellartechsol.com",):
        dns[h] = doh(h, 0, cache_dir, do_fetch)
    live_hosts = sorted(h for h, d in dns.items() if d["dns_status"] == "NOERROR" and d["a"] and h.endswith("iphiview.com"))
    # path probe on the multi-tenant hosts (one worker per host, <= 1 request/s each)
    plabels = path_labels(universe)
    with ThreadPoolExecutor(max_workers=2) as ex:
        probes = list(ex.map(lambda hp: (hp, fetch(f"https://{hp[0]}/{hp[1]}/", cache_dir, do_fetch)),
                             [(h, l) for l in plabels for h in PATH_HOSTS]))
    path_hits = sorted({(h, "/" + l) for (h, l), r in probes if r["status"] == 200 or
                        (r["status"] in (301, 302) and r.get("location"))})
    src_of = lambda h, p: ";".join(s for s, ok in (("repo", h in repo_hosts or (h, p) in repo_paths), ("ct", h in ct_iphi_hosts),
                                                   ("dns_guess", label_of(h) in guesses and h not in PATH_HOSTS),
                                                   ("path_probe", (h, p) in path_hits)) if ok)

    inst = sorted({(h, "/" + label_of(h)) for h in live_hosts if label_of(h) not in ("www", "maintenance")} |
                  set(repo_paths) | set(path_hits) | {(h, p.rstrip("/")) for h, p in ((k.split("/", 1)[0], "/" + k.split("/", 1)[1]) for k in MANUAL) if p.strip("/")} |
                  {(h, "/" + label_of(h)) for h in repo_hosts + ct_iphi_hosts if label_of(h) and label_of(h) not in ("www", "maintenance")})
    roots = {h: fetch(f"https://{h}/", cache_dir, do_fetch) for h in sorted({h for h, _ in inst})
             if dns.get(h, {}).get("dns_status") == "NOERROR" or h in PATH_HOSTS}
    sig_tenants = tenant_hosts_from_signals(signals)
    map_eins = lambda h, p: set().union(set(), *(v for k, v in sig_tenants.items() if k == h + p))

    def row(h: str, p: str) -> dict:
        d = dns.get(h) or {"dns_status": "not_queried", "cname": "", "a": "", "dns_url": ""}
        rt = page_facts(roots[h]) if h in roots else {}
        pg, final, ext = follow_tenant(f"https://{h}{p}/", cache_dir, do_fetch) if h in roots else ({}, "", "")
        ext = ext or (rt.get("location", "") if rt.get("location", "").startswith("http") and "iphiview.com" not in rt.get("location", "") and p == "/" + label_of(h) else "")
        df = dest_facts(ext, cache_dir, do_fetch) if ext else {}
        key = tenant_key(h, p)
        fkey = tenant_key(urllib.parse.urlsplit(final).hostname or h, urllib.parse.urlsplit(final).path.rstrip("/")) if final else key
        man = MANUAL.get(key) or MANUAL.get(fkey) or MANUAL.get(h + "/")
        author = pg.get("author", "")
        eins = sorted(map_eins(h, p))
        ne, ne_note = name_ein(author)
        ein = (man or {}).get("ein") or ne or (eins[0] if eins else "")
        eins_all = sorted(set(eins) | ({ein} if ein else set()))
        m, u = by_ein.get(ein, {}), uni_by_ein.get(ein, {})
        lines = ren990.get(ein, ())
        ctn = ctr.get(h)
        hst = hosting(d) or ("legacy 67.216.67.0/24 (dbsintl.net)" if d.get("a", "").startswith(LEGACY_NET) else "")
        out = {
            "tenant_key": key, "host": h, "path": p, "label": label_of(h) if h.endswith("iphiview.com") else p.strip("/"),
            "product": "iPhi F&E ClientView (trust reporting)" if "F&E ClientView" in pg.get("welcome", "") else
                       ("Ren GivingPoint front end (NPT white label)" if "GivingPoint" in df.get("dest_markers", "") else "Ren (Stellar) iPhi"),
            "org_identity_meta_author": author,
            "org": (man or {}).get("org") or author or m.get("name") or u.get("sponsor_name", ""),
            "org_type": (man or {}).get("org_type") or org_type_of(ein in by_ein, u, author),
            "ein": ein, "eins_all": " ".join(eins_all), "ein_basis": (man or {}).get("note", "")[:0] or ("manual table" if (man or {}).get("ein") else (ne_note or ("CF-map homepage link" if eins else ne_note))),
            "fy2024_daf_assets_usd": m.get("fy2024_daf_assets_usd") or u.get("fy2024_daf_assets", ""),
            "discovery": src_of(h, p) + (";cf_map_link" if eins else ""),
            "dns_status": d["dns_status"], "dns_cname": d["cname"], "dns_a": d["a"], "hosting": hst, "dns_evidence_url": d["dns_url"],
            "root_status": rt.get("status", ""), "root_location": rt.get("location", ""),
            "tenant_url": f"https://{h}{p}/", "tenant_status": pg.get("status", ""), "tenant_final_url": final if final != f"https://{h}{p}/" else "",
            "external_redirect": ext, "redirect_dest_hosting": df.get("dest_hosting", ""), "redirect_dest_status": df.get("dest_status", ""),
            "redirect_dest_markers": df.get("dest_markers", ""), "redirect_dest_program": df.get("dest_program", ""), "redirect_dest_on_ren": df.get("dest_on_ren", ""),
            "copyright_meta": pg.get("copyright_meta", ""), "footer_year": pg.get("footer_year", ""),
            "welcome_text": pg.get("welcome", ""), "banner": pg.get("banner", ""), "iphi_markers": pg.get("iphi_markers", ""),
            "ct_named_first": ctn[0] if ctn else "", "ct_named_last": ctn[1] if ctn else "", "ct_named_count": ctn[2] if ctn else 0,
            "map_portal_vendor": m.get("portal_vendor", ""), "map_portal_url": m.get("portal_url", ""),
            "map_links_tenant": "yes" if eins else "no", "map_conflicting_signals": m.get("conflicting_signals", "")[:200],
            "ren_990_lines": fmt_lines(lines), "ren_990_last_ty": max((x["tax_year"] for x in lines), default=""),
            "migration_event": events.get(ein), "manual_status": MANUAL_STATUS.get(ein),
            "manual_note": (man or {}).get("note", ""), "manual_src": (man or {}).get("src", ""),
        }
        st, dest, date, basis = classify(out)
        return {**out, "status": st, "destination_vendor": dest, "exit_date": date, "status_basis": basis}

    rows = collapse([row(h, p) for h, p in inst], set(repo_paths))
    have = {e for r in rows for e in r["eins_all"].split()}
    extra = [x for x in (row_990_only(ein, lines, by_ein, uni_by_ein, events) for ein, lines in sorted(ren990.items()) if ein not in have) if x]
    allrows = rows + extra
    for r in allrows:
        r["retrieved"] = RETRIEVED
        r["in_attrition_scope"] = in_scope(r)
        r["sponsor_key"] = r["ein"] or ("org:" + (r.get("org_identity_meta_author") or r["tenant_key"]))
        r["migration_event"] = r["migration_event"]["event_date"] if isinstance(r.get("migration_event"), dict) else ""
        r["manual_status"] = "yes" if r.get("manual_status") else ""
    allrows.sort(key=lambda r: (r["in_attrition_scope"] != "yes", r["status"], -(float(r.get("fy2024_daf_assets_usd") or 0)), r["tenant_key"]))
    write_csv(OUT_CENSUS, allrows, CENSUS_FIELDS)
    summary = attrition_summary(allrows)
    summary.update({"labels_queried_dns": len(labels), "guess_labels": len(guesses), "path_labels_probed": len(plabels),
                    "path_probe_hits": [h + p for h, p in path_hits], "repo_hosts": len(repo_hosts),
                    "ct_named_iphiview_hosts": ct_iphi_hosts, "live_iphiview_hosts": live_hosts, "wildcard_probe": wildcard_probe["dns_status"],
                    "nxdomain_repo_or_ct_hosts": sorted(h for h in repo_hosts + ct_iphi_hosts if dns.get(h, {}).get("dns_status") == "NXDOMAIN"),
                    "ct_ranges": {k: v for k, v in ctr.items() if not k.startswith("*") and any(k.endswith(dm) for dm in CT_DOMAINS)},
                    "hosting_counts": {str(k): sum(1 for r in rows if r.get("hosting") == k) for k in sorted({str(r.get("hosting")) for r in rows})}})
    with open(OUT_SUMMARY, "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True, default=str)
    return summary


def repo_stellar_paths(root: str) -> tuple[tuple[str, str], ...]:
    files = sorted({f for p in ("research/**/*.md", "data/**/*.csv") for f in glob.glob(os.path.join(root, p), recursive=True)})
    return tuple(sorted({(m.group(1).lower(), m.group(2).lower()) for f in files if os.path.basename(f) not in OWN_OUTPUTS
                         for m in STELLAR_RE.finditer(open(f, encoding="utf-8", errors="replace").read())
                         if m.group(1).lower() == "iphi.stellartechsol.com"}))


def fmt_lines(lines: Sequence[Mapping]) -> str:
    return " | ".join(f"TY{x['tax_year']} {x['contractor_name'][:28]} '{x['services'][:28]}' ${int(float(x['compensation'])):,}"
                      for x in sorted(lines, key=lambda x: x["tax_year"]))


def row_990_only(ein: str, lines: Sequence[Mapping], by_ein: Mapping, uni_by_ein: Mapping, events: Mapping) -> dict | None:
    """Stellar/Ren 990 payee with no tenant row. Scope hint: a Stellar-named payee = iPhi lineage."""
    stellar = any("stellar" in x["contractor_name"].lower() for x in lines)
    tech = any(re.search(r"tech|software|portal|platform|system|it serv|computer|web", x["services"], re.I) for x in lines)
    if not (stellar or tech):
        return None
    m, u = by_ein.get(ein, {}), uni_by_ein.get(ein, {})
    last = max(x["tax_year"] for x in lines)
    mv, ms, cur = events.get(ein), MANUAL_STATUS.get(ein), m.get("portal_vendor", "")
    if mv:
        st = ("migrated", mv["to_system"], mv["event_date"] or "undated", "cf-vendor-migrations-2022-2026.csv")
    elif ms:
        st = ms[:4]
    elif cur and NON_IPHI.search(cur) and "iPhi" not in cur:
        st = ("migrated", cur, "undated", f"Stellar/Ren 990 payee but CF map 2026-11-14 current fund login is {cur}")
    elif int(last) >= 2024:
        st = ("active", "", "", f"990 payee in TY{last} (latest harvested year); no iPhi host found by DNS guess or path probe")
    else:
        st = ("unknown", "", "", f"last Ren/Stellar 990 line TY{last}; later absence is weak (top-5 > $100k listing rule)")
    return {"tenant_key": f"990-only:{ein}", "host": "", "path": "", "label": "",
            "product": "Ren (Stellar) iPhi [990 payee]" if stellar else "Ren platform (product not identified) [990 payee]",
            "org": m.get("name") or u.get("sponsor_name") or lines[0]["sponsor_name"],
            "org_type": org_type_of(ein in by_ein, u, lines[0]["sponsor_name"]),
            "ein": ein, "eins_all": ein, "ein_basis": "990 harvest", "fy2024_daf_assets_usd": m.get("fy2024_daf_assets_usd") or u.get("fy2024_daf_assets", ""),
            "discovery": "990_harvest", "dns_status": "", "map_portal_vendor": cur, "map_portal_url": m.get("portal_url", ""), "map_links_tenant": "no",
            "ren_990_lines": fmt_lines(lines), "ren_990_last_ty": last, "migration_event": mv, "manual_status": ms,
            "status": st[0], "destination_vendor": st[1], "exit_date": st[2], "status_basis": st[3],
            "manual_src": ms[4] if ms else ""}


def collapse(rows: Sequence[Mapping], cited: set) -> list:
    """Per host: every path that answers 200 (or is a MANUAL key); a host with neither keeps one row (MANUAL key, then
    repo-cited path, then /<label>). Rows whose followed redirect lands on another row's URL are aliases and dropped."""
    out = []
    for h, rs in group_by(rows, lambda r: r["host"]).items():
        ok = [r for r in rs if r["tenant_status"] == 200 or r["tenant_key"] in MANUAL or r.get("external_redirect")]
        if ok:
            out += ok
            continue
        out.append(sorted(rs, key=lambda r: (r["tenant_key"] not in MANUAL, (r["host"], r["path"]) not in cited, r["path"] != "/" + r["label"]))[0])
    urls = {r["tenant_url"] for r in out}
    keep = [r for r in out if not (r.get("tenant_final_url") and r["tenant_final_url"] in urls and r["tenant_key"] not in MANUAL)]
    seen_ext = {}
    return [r for r in keep if not (r.get("external_redirect") and seen_ext.setdefault((r["external_redirect"], r["host"]), r["tenant_key"]) != r["tenant_key"])]


def in_scope(r: Mapping) -> str:
    """Row-level filter for the attrition population: US DAF/CF sponsors with an iPhi tenant or Stellar 990 payee,
    evidenced as an iPhi client at some point since 2023-01-01 (or with no evidence of exit before 2023)."""
    if r["status"] == "out_of_scope" or r.get("org_type") in ("bank_platform", "non_us_trustee", "bank_trust_reporting"):
        return "no"
    if "not identified" in r.get("product", ""):
        return "no"
    if not r.get("org_identity_meta_author") and not r.get("ein"):
        return "no"  # host exists (or existed) but no sponsor identity can be tied to it
    if r["tenant_key"].startswith("990-only:"):
        return "yes" if int(r.get("ren_990_last_ty") or 0) >= 2022 else "no"
    if r["status"] == "migrated" and re.match(r"20(1\d|2[0-2])", r.get("exit_date", "")):
        return "no"
    return "yes"


STATUS_RANK = {"active": 0, "migrating": 1, "unknown": 2, "migrated": 3, "lapsed": 4}


def sponsors(rows: Sequence[Mapping]) -> list[dict]:
    """One record per sponsor (EIN, else tenant identity): the best status over its in-scope tenants."""
    out = []
    for k, rs in group_by([r for r in rows if r["in_attrition_scope"] == "yes"], lambda r: r["sponsor_key"]).items():
        best = sorted(rs, key=lambda r: (STATUS_RANK.get(r["status"], 9), r["tenant_key"].startswith("990-only:")))[0]
        out.append({"sponsor_key": k, "org": best["org"], "status": best["status"], "destination_vendor": best["destination_vendor"],
                    "exit_date": best["exit_date"], "assets": float(best.get("fy2024_daf_assets_usd") or 0), "org_type": best.get("org_type", ""),
                    "tenants": [r["tenant_key"] for r in rs], "manual": best.get("manual_status") == "yes"})
    return out


def attrition_summary(rows: Sequence[Mapping]) -> dict:
    sp = sponsors(rows)
    n = len(sp)
    exits = [r for r in sp if r["status"] in ("migrated", "lapsed")]
    dated = [r for r in exits if re.match(r"20(2[3-6])", r.get("exit_date", ""))]
    unk = [r for r in sp if r["status"] == "unknown"]
    migrating = [r for r in sp if r["status"] == "migrating"]
    assets = lambda rs: sum(r["assets"] for r in rs)
    k = len(exits)
    lo, hi = wilson(k, n)
    active_keys = {r["sponsor_key"] for r in sp if r["status"] in ("active", "migrating")}
    prog_exits = [r["tenant_key"] + " -> " + (r["destination_vendor"] or r["status"]) for r in rows
                  if r["in_attrition_scope"] == "yes" and r["status"] in ("migrated", "lapsed") and r["sponsor_key"] in active_keys]
    by_type = {t: {s: sum(1 for r in sp if r["org_type"] == t and r["status"] == s) for s in STATUS_RANK} for t in sorted({r["org_type"] for r in sp})}
    return {
        "unit": "sponsor (EIN; tenant identity where no EIN)", "population_n": n, "population_daf_assets_usd": assets(sp),
        "status_counts": {s: sum(1 for r in sp if r["status"] == s) for s in STATUS_RANK}, "status_by_org_type": by_type,
        "exits": sorted(f"{r['org']} -> {r['destination_vendor'] or r['status']} ({r['exit_date']})" for r in exits),
        "exits_n": k, "exits_dated_2023_2026_n": len(dated), "unknown_n": len(unk), "migrating_n": len(migrating),
        "unknown": sorted(r["org"] for r in unk), "migrating": sorted(r["org"] for r in migrating),
        "attrition_point": k / n if n else 0, "attrition_wilson95": [lo, hi],
        "attrition_lower_dated_only": len(dated) / n if n else 0,
        "attrition_upper_incl_unknown_and_migrating": (k + len(unk) + len(migrating)) / n if n else 0,
        "active_990_only": sorted(r["org"] for r in sp if r["status"] == "active" and not r["manual"] and all(t.startswith("990-only:") for t in r["tenants"])),
        "attrition_upper_incl_unknown_and_990_only_active": (k + len(unk) + len(migrating) + sum(1 for r in sp if r["status"] == "active" and not r["manual"] and all(t.startswith("990-only:") for t in r["tenants"]))) / n if n else 0,
        "annualised_point": 1 - (1 - k / n) ** (1 / NOW_YEARS) if n and k < n else None,
        "annualised_upper": 1 - (1 - (k + len(unk) + len(migrating)) / n) ** (1 / NOW_YEARS) if n else None,
        "exit_daf_assets_usd": assets(exits), "exit_asset_share": assets(exits) / assets(sp) if assets(sp) else 0,
        "destinations": {d: sum(1 for r in exits if (r["destination_vendor"] or "none evidenced") == d) for d in sorted({r["destination_vendor"] or "none evidenced" for r in exits})},
        "program_level_exits_within_active_sponsors": prog_exits, "years_window": NOW_YEARS,
        "exit_asset_share_ex_npt_gs": (lambda rest: assets([r for r in exits]) / assets(rest) if assets(rest) else 0)(
            [r for r in sp if r["sponsor_key"] not in ("237825575", "311774905", "113813663")]),
        "cf_only": (lambda cf: {"n": len(cf), "exits": sum(1 for r in cf if r["status"] in ("migrated", "lapsed")),
                                "wilson95": wilson(sum(1 for r in cf if r["status"] in ("migrated", "lapsed")), len(cf)),
                                "assets": assets(cf), "exit_assets": assets([r for r in cf if r["status"] in ("migrated", "lapsed")])})(
            [r for r in sp if r["org_type"] == "community_foundation"]),
    }


CENSUS_FIELDS = (
    "tenant_key", "sponsor_key", "host", "path", "label", "product", "org", "org_identity_meta_author", "org_type", "ein", "eins_all", "ein_basis",
    "fy2024_daf_assets_usd", "discovery", "dns_status", "dns_cname", "dns_a", "hosting", "dns_evidence_url",
    "root_status", "root_location", "tenant_url", "tenant_status", "tenant_final_url", "external_redirect", "redirect_dest_hosting",
    "redirect_dest_status", "redirect_dest_markers", "redirect_dest_program", "redirect_dest_on_ren", "copyright_meta", "footer_year",
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
    ("Morgan Stanley GIFT", r"Morgan Stanley|\bGIFT\b"), ("BofA Charitable Gift Fund", r"(?:Bank of America|BofA)(?!'s recent study)"),
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
        print(json.dumps({k: s[k] for k in ("population_n", "status_counts", "exits", "exits_n", "exits_dated_2023_2026_n", "unknown", "migrating",
                                             "attrition_point", "attrition_wilson95", "attrition_lower_dated_only", "attrition_upper_incl_unknown_and_migrating",
                                             "annualised_point", "annualised_upper", "exit_asset_share", "destinations",
                                             "program_level_exits_within_active_sponsors", "path_probe_hits")}, indent=1, default=str))
    if a.task in ("spectrum", "all"):
        for r in spectrum(a.cache_dir, a.fetch):
            print("SPECTRUM", r["name"][:34], r["host"], r["signin_status"], r["signin_title"][:40], r["portal_role"], "|", r["ledger_reading"])
    if a.task in ("rde", "all"):
        rr = rde(a.cache_dir, a.fetch)
        print("RDE rows", len(rr), sorted({r["program"] for r in rr}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
