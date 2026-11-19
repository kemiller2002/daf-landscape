#!/usr/bin/env python3
"""P-GAP19-06: consolidate and red-team the relationship graph (stdlib only, functional style).

Steps
1. Read relationship-graph-edges.csv plus every relationship-graph-edges-additions*.csv.
2. Normalise entity names (EIN extraction, alias table, light string normalisation) and
   relationship types (synonyms; passive forms are reversed to the active direction).
3. Apply governing corrections: (a) edge-ID corrections named in validation reports
   (VALIDATION_CORRECTIONS below, each with its report reference) and (b) explicit
   supersession notes inside the edge files ("Supersedes E...", "Upgrades E...",
   "Downgrades E...", "Correction to E...").
4. Deduplicate on (canonical source, canonical target, normalised type), treating a
   reversed duplicate as the same edge. The strongest live (non-superseded) evidence is
   kept; every merged edge ID is listed.
5. Red team: every edge whose evidence class is inferred / unknown / probable / reported /
   pending, rests on crt.sh, or is flagged as a vendor claim gets one independent public
   check (CHECKS below). Each check reads robots.txt first for every host it touches
   (including redirect hops); if robots.txt cannot be read or disallows the path, the page
   is not fetched and the edge stays an unverified lead. crt.sh is never contacted.
   Public DNS resolution (system resolver) is used where the check is a hostname check.
6. Graph statistics and dependency figures (hub degrees, Ren-linked share of DAFRC FY2024
   sponsor assets, sponsor-asset CR3/CR5/HHI recomputed from the DAFRC file, vendor
   client concentration).

Usage
  python3 scripts/mission_graph_consolidate.py probe URL [REGEX]   # one robots-gated fetch
  python3 scripts/mission_graph_consolidate.py run [--offline]      # full pipeline
--offline re-uses the response cache only (no network).
"""
from __future__ import annotations

import csv
import glob
import hashlib
import json
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from functools import reduce
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "mission-2026-11-14"
CACHE = Path("/tmp/claude-0/-home-user/ed3d1503-0f0d-5a0d-a5e2-85e6e3196309/scratchpad/graph-cache")
TODAY = "2026-11-19"
UA = "Mozilla/5.0 (compatible; research-link-check/1.0)"
UA_TOKEN = "research-link-check"
TIMEOUT = 25
MIN_DELAY = 1.0
MAX_BODY = 1_500_000
BANNED_HOSTS = ("crt.sh",)

# ============================================================== network (robots-gated)


def parse_robots(text: str) -> dict:
    groups, agents, rules, last_agent = [], [], [], False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        field, value = (s.strip() for s in line.split(":", 1))
        field = field.lower()
        if field == "user-agent":
            if not last_agent and agents:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value.lower())
            last_agent = True
        elif field in ("allow", "disallow"):
            if agents:
                rules.append((field, value))
            last_agent = False
        else:
            last_agent = False
    if agents:
        groups.append((agents, rules))
    mine = [r for a, r in groups if any(x != "*" and x in UA_TOKEN for x in a)]
    star = [r for a, r in groups if "*" in a]
    return {"rules": tuple(x for g in (mine or star) for x in g)}


def _rx(pattern: str):
    anchored = pattern.endswith("$")
    body = re.escape(pattern[:-1] if anchored else pattern).replace(r"\*", ".*")
    return re.compile(body + ("$" if anchored else ""))


def robots_allows(robots: dict, url: str) -> bool:
    p = urllib.parse.urlsplit(url)
    path = (p.path or "/") + (("?" + p.query) if p.query else "")
    best = (-1, True)
    for field, pat in robots["rules"]:
        if pat and _rx(pat).match(path):
            if len(pat) > best[0] or (len(pat) == best[0] and field == "allow"):
                best = (len(pat), field == "allow")
    return best[1]


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def _opener():
    ca = Path("/root/.ccr/ca-bundle.crt")
    ctx = ssl.create_default_context(cafile=str(ca)) if ca.exists() else ssl.create_default_context()
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), _NoRedirect())


_STATE = {"opener": None, "last": {}, "robots": {}, "offline": False, "requests": 0}


def _cache_path(url: str) -> Path:
    return CACHE / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".json")


def raw_get(url: str) -> dict:
    """One GET without redirect following. Cached on disk (scratchpad)."""
    cp = _cache_path(url)
    if cp.exists():
        return json.loads(cp.read_text())
    if _STATE["offline"]:
        return {"status": None, "error": "offline (not cached)", "location": "", "body": "", "headers": {}}
    host = urllib.parse.urlsplit(url).hostname or ""
    if any(host == b or host.endswith("." + b) for b in BANNED_HOSTS):
        return {"status": None, "error": "banned host", "location": "", "body": "", "headers": {}}
    if _STATE["opener"] is None:
        _STATE["opener"] = _opener()
    wait = _STATE["last"].get(host, 0) + MIN_DELAY - time.monotonic()
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    _STATE["requests"] += 1
    try:
        with _STATE["opener"].open(req, timeout=TIMEOUT) as r:
            body = r.read(MAX_BODY)
            is_pdf = body[:5] == b"%PDF-"
            out = {"status": r.status, "location": r.headers.get("Location", ""),
                   "body": body.decode("latin-1") if is_pdf else body.decode("utf-8", "replace"),
                   "pdf": is_pdf, "error": "",
                   "headers": {k.lower(): v for k, v in r.headers.items()}}
    except urllib.error.HTTPError as e:
        hdrs = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
        try:
            body = e.read(200_000).decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            body = ""
        out = {"status": e.code, "location": hdrs.get("location", ""), "body": body, "error": "", "headers": hdrs}
    except Exception as e:  # noqa: BLE001 - record, never crash
        out = {"status": None, "location": "", "body": "", "error": f"{type(e).__name__}: {str(e)[:90]}",
               "headers": {}}
    finally:
        _STATE["last"][host] = time.monotonic()
    CACHE.mkdir(parents=True, exist_ok=True)
    cp.write_text(json.dumps({**out, "url": url, "fetched": TODAY}))
    return out


def robots_for(url: str) -> dict:
    p = urllib.parse.urlsplit(url)
    key = f"{p.scheme}://{p.netloc}"
    if key in _STATE["robots"]:
        return _STATE["robots"][key]
    r, cur = None, key + "/robots.txt"
    for _ in range(4):  # robots.txt redirects are followed (RFC 9309 2.3.1.2)
        r = raw_get(cur)
        if r.get("status") in (301, 302, 303, 307, 308) and r.get("location"):
            cur = urllib.parse.urljoin(cur, r["location"])
            continue
        break
    st = r.get("status")
    if st and 200 <= st < 300:
        rob = {"ok": True, "note": "robots 200", **parse_robots(r["body"])}
    elif st in (404, 410):
        rob = {"ok": True, "note": f"robots {st} (no rules)", "rules": ()}
    else:
        rob = {"ok": False, "note": f"robots unreadable ({st or r.get('error')})", "rules": ()}
    _STATE["robots"][key] = rob
    return rob


def fetch(url: str, max_hops: int = 5) -> dict:
    """Robots-gated GET following redirects; robots.txt checked for each hop's host first."""
    hops, cur = [], url
    for _ in range(max_hops + 1):
        rob = robots_for(cur)
        if not rob["ok"]:
            return {"outcome": "not fetched: " + rob["note"], "url": url, "final": cur, "hops": hops,
                    "status": None, "body": "", "headers": {}}
        if not robots_allows(rob, cur):
            return {"outcome": "not fetched: robots disallow", "url": url, "final": cur, "hops": hops,
                    "status": None, "body": "", "headers": {}}
        r = raw_get(cur)
        if r.get("status") in (301, 302, 303, 307, 308) and r.get("location"):
            hops.append(f"{r['status']}->{r['location'][:120]}")
            cur = urllib.parse.urljoin(cur, r["location"])
            continue
        oc = "fetched" if r.get("status") else ("error: " + r.get("error", ""))
        body = r.get("body", "")
        if r.get("pdf"):
            body = pdf_text(body)
        return {"outcome": oc, "url": url, "final": cur, "hops": hops, "status": r.get("status"),
                "body": body, "headers": r.get("headers", {}), "pdf": bool(r.get("pdf"))}
    return {"outcome": "redirect loop", "url": url, "final": cur, "hops": hops, "status": None, "body": "",
            "headers": {}}


def dns(host: str) -> dict:
    cp = _cache_path("dns:" + host)
    if cp.exists():
        return json.loads(cp.read_text())
    if _STATE["offline"]:
        return {"host": host, "ok": False, "error": "offline (not cached)", "cname": "", "ips": []}
    try:
        name, aliases, ips = socket.gethostbyname_ex(host)
        out = {"host": host, "ok": True, "error": "", "cname": name if name != host else "", "ips": sorted(ips)}
    except Exception as e:  # noqa: BLE001
        out = {"host": host, "ok": False, "error": f"{type(e).__name__}: {str(e)[:60]}", "cname": "", "ips": []}
    CACHE.mkdir(parents=True, exist_ok=True)
    cp.write_text(json.dumps(out))
    return out


def text_of(html: str) -> str:
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def _pdf_strings(chunk: bytes) -> str:
    out = []
    for m in re.finditer(rb"\[(.*?)\]\s*TJ|\((.*?)(?<!\\)\)\s*Tj", chunk, re.S):
        seg = m.group(1) if m.group(1) is not None else b"(" + m.group(2) + b")"
        parts = re.findall(rb"\(((?:\\.|[^\\)])*)\)", seg)
        out.append(b"".join(parts).decode("latin-1", "replace"))
    return " ".join(out)


def pdf_text(body_latin1: str) -> str:
    """Best-effort text from a PDF (FlateDecode streams, Tj/TJ literal strings). Stdlib zlib."""
    import zlib
    raw = body_latin1.encode("latin-1", "replace")
    texts = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", raw, re.S):
        data = m.group(1)
        try:
            data = zlib.decompress(data)
        except Exception:  # noqa: BLE001
            pass
        texts.append(_pdf_strings(data))
    return re.sub(r"\s+", " ", " ".join(texts))


def snippet(body: str, rx: str, width: int = 90) -> str:
    m = re.search(rx, body, re.I | re.S)
    if not m:
        return ""
    s, e = max(0, m.start() - width), min(len(body), m.end() + width)
    return re.sub(r"\s+", " ", body[s:e]).strip()


# ============================================================== load


def edge_files() -> tuple:
    adds = sorted(glob.glob(str(DATA / "relationship-graph-edges-additions*.csv")),
                  key=lambda p: (0, 0) if p.endswith("additions.csv") else
                  (1, int(re.search(r"additions-(\d+)\.csv$", p).group(1))))
    return (str(DATA / "relationship-graph-edges.csv"),) + tuple(adds)


def read_csv(path: str) -> list:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_edges() -> tuple:
    return tuple({**row, "file": Path(f).name} for f in edge_files() for row in read_csv(f))


# ============================================================== entity normalisation

# (regex on the raw name, canonical label). First match wins. Product or legal-entity
# variants collapse to the corporate/sponsor node; the raw name is kept on every edge.
ALIASES = (
    (r"^(ren\b|ren \(|renpsg|stellar technology solutions|ren for charities)", "Ren (incl. Stellar/iPhi)"),
    (r"^foundant technologies", "Foundant Technologies"),
    (r"^chariot\b", "Chariot"),
    (r"^fidelity charitable|ein 11-0303001", "Fidelity Charitable"),
    (r"^(fmr llc|fidelity brokerage services|fidelity investments)", "Fidelity Investments (FMR)"),
    (r"^edward jones (private daf|generations)", "Edward Jones private DAF (Generations)"),
    (r"^edward jones charitable gift fund", "Edward Jones Charitable Gift Fund"),
    (r"^edward jones$", "Edward Jones"),
    (r"^blackbaud\b(?! giving fund)(?!.*yourcause)", "Blackbaud"),
    (r"^(npact\b(?! payments)|fusion laboratories|foundation cloud community portal)", "NPact (Fusion Laboratories LLC)"),
    (r"^salesforce", "Salesforce"),
    (r"^tifin give|^tifin wealthtech", "TIFIN Give"),
    (r"^(tifin$|tifin group|tifin\.ai)", "TIFIN (group)"),
    (r"^giveclear foundation", "GiveClear Foundation"),
    (r"^renaissance charitable foundation", "Renaissance Charitable Foundation (RCF)"),
    (r"^(natl christian charitable fdn|national christian foundation)", "National Christian Foundation (NCF)"),
    (r"^national philanthropic trust$|ein 23-7825575", "National Philanthropic Trust (NPT)"),
    (r"^(dafgiving360|schwab charitable fund)", "DAFgiving360 (Schwab Charitable)"),
    (r"^(charles schwab)", "Charles Schwab (firm)"),
    (r"^vanguard charitable", "Vanguard Charitable"),
    (r"^american endowment foundation", "American Endowment Foundation (AEF)"),
    (r"^morgan stanley (global impact funding trust|gift)", "Morgan Stanley GIFT"),
    (r"^morgan stanley( smith barney llc)?$", "Morgan Stanley (firm)"),
    (r"^bank of america charitable gift fund", "Bank of America Charitable Gift Fund"),
    (r"^bank of america\b", "Bank of America (firm)"),
    (r"^the goldman sachs charitable gift fund", "Goldman Sachs Charitable Gift Fund (GS Gives)"),
    (r"^(gs donor advised philanthropy fund|goldman sachs pwm daf)", "GS Donor Advised Philanthropy Fund (GS PWM DAF)"),
    (r"^(akoya|akoyago)", "Akoya"),
    (r"^benevity", "Benevity"),
    (r"^paypal( inc)?$", "PayPal"),
    (r"^(foundation source)", "Foundation Source"),
    (r"^vennfi", "Vennfi"),
    (r"^charityvest", "Charityvest"),
    (r"^bonterra", "Bonterra"),
    (r"^(repay)\b", "REPAY"),
    (r"^broadwest partners", "BroadWest Partners"),
    (r"^microsoft", "Microsoft"),
    (r"^foundation partners llc", "Foundation Partners LLC (Fund 360)"),
    (r"^(donor-portal\.org)", "donor-portal.org"),
    (r"^truist financial corporation", "Truist Financial Corporation"),
    (r"^(icgf donor-advised fund)", "ICGF Donor-Advised Fund (NPT program)"),
    (r"^j\.p\. morgan charitable gift fund", "J.P. Morgan Charitable Gift Fund (NPT program)"),
    (r"^j\.p\. morgan charitable giving fund", "J.P. Morgan Charitable Giving Fund (NPT program)"),
    (r"^assetmark charitable program", "AssetMark Charitable Program"),
    (r"^(network for good)", "Network for Good (For Good)"),
    (r"^(goodstack impact foundation us|percent impact foundation)", "Goodstack Impact Foundation US"),
    (r"^(durable capital for sustainable outcomes)", "Durable Capital for Sustainable Outcomes (The Resiliency Company)"),
)

# EINs for sponsor names that carry none in the edge files (DAFRC FY2024 rows, same EIN).
MANUAL_EIN = {
    "Fidelity Charitable": "110303001", "National Philanthropic Trust (NPT)": "237825575",
    "DAFgiving360 (Schwab Charitable)": "311640316", "Vanguard Charitable": "232888152",
    "GS Donor Advised Philanthropy Fund (GS PWM DAF)": "311774905",
    "American Endowment Foundation (AEF)": "341747398", "Morgan Stanley GIFT": "527082731",
    "Renaissance Charitable Foundation (RCF)": "352129262", "National Christian Foundation (NCF)": "581493949",
    "Bank of America Charitable Gift Fund": "046010342", "Goldman Sachs Charitable Gift Fund (GS Gives)": "113813663",
    "GiveClear Foundation": "813222963", "Charityvest": "812771871",
}


def ein_of(name: str) -> str:
    m = re.search(r"EIN[ :]*(\d{2})-?(\d{7})", name)
    return (m.group(1) + m.group(2)) if m else ""


def name_key(name: str) -> str:
    s = re.sub(r"\([^)]*\)", " ", name).lower()
    s = s.replace("&", " and ")
    s = re.sub(r"\b(inc|llc|l\.?p|corp|corporation|co|the)\b\.?", " ", s)
    s = re.sub(r"\bfdn\b", "foundation", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def alias_of(name: str) -> str:
    low = name.strip().lower()
    return next((label for rx, label in ALIASES if re.search(rx, low)), "")


def build_resolver(edges: tuple, dafrc_names: dict) -> dict:
    """raw name -> {'id','label','ein'}; EIN > alias > name key; keys inherit EINs seen elsewhere."""
    raws = sorted({e[k] for e in edges for k in ("source_entity", "target_entity")})
    key_ein = {}
    for r in raws:
        if ein_of(r) and not alias_of(r):
            key_ein.setdefault(name_key(r), ein_of(r))
    for ein, nm in dafrc_names.items():
        key_ein.setdefault(name_key(nm), ein)

    def resolve(r: str) -> dict:
        label = alias_of(r)
        if label:
            ein = MANUAL_EIN.get(label, "") or ein_of(r)
            return {"id": "A:" + label, "label": label, "ein": ein}
        ein = ein_of(r) or key_ein.get(name_key(r), "")
        return {"id": ("EIN:" + ein) if ein else ("K:" + name_key(r)), "label": "", "ein": ein}

    first = {r: resolve(r) for r in raws}
    # display label = most frequent raw spelling in the cluster (alias label if any)
    counts = Counter(e[k] for e in edges for k in ("source_entity", "target_entity"))
    by_id = defaultdict(list)
    for r, v in first.items():
        by_id[v["id"]].append(r)
    label_of = {i: (first[rs[0]]["label"] or
                    re.sub(r"\s*\((EIN[^)]*)\)\s*$", "", max(rs, key=lambda x: (counts[x], -len(x)))))
                for i, rs in by_id.items()}
    return {r: {**v, "label": label_of[v["id"]], "variants": len(by_id[v["id"]])} for r, v in first.items()}


# ============================================================== relationship types

TYPE_MAP = {"general_ledger": "ledger_provider", "portal_provider": "technology_provider",
            "lead_investor": "investor", "shareholder": "investor", "acquired": "acquirer",
            "owns": "controls"}
REVERSE_TYPES = {"acquired_by": "acquirer"}

STATUS_RANK = {"confirmed": 6, "historically_confirmed": 5, "reported": 4, "probable": 3, "pending": 3,
               "inferred": 2, "unknown": 1, "rejected": 0}
PRIMARY_HOSTS = ("sec.gov", "irs.gov", "gt990datalake", "propublica.org", "efts.sec.gov")

# ============================================================== governing corrections

# Edge-ID corrections stated in validation / red-team reports. op: set_type, set_status,
# add_note, replace_note (old, new). 'check' = text whose presence means already applied.
VALIDATION_CORRECTIONS = (
    ("EN001", "set_type", "technology_provider", "validation-wave14-report.md l.138 (V14-01)"),
    ("EN001", "add_note", "fund-accounting overlay on the NetSuite GL", "validation-wave14-report.md l.138 (V14-01)"),
    ("EN011", "set_status", "reported", "validation-wave14-report.md l.139"),
    ("EN011", "add_note", "donor-portal.org portal tenant (first-party link); back-office service not shown",
     "validation-wave14-report.md l.139"),
    ("ER017", "add_note", "superseded by the FireAid App. B circular (ratios as of 2024-09-30), which names Goldman "
     "Sachs Wealth Services, L.P. as ETF selector (up to 50 bps) and payment by check or wire; V18-01",
     "validation-wave18-report.md l.185"),
    ("ER015", "add_note", "report wording varies: '$535 million ... since inception' vs 'In 2023: ... assets under "
     "care'; V18-27", "validation-wave18-report.md l.186"),
    ("ES016", "add_note", "the source text is in Schedule N Part II as well as Schedule O (V19)",
     "validation-wave19-report.md l.132"),
    ("ES006", "add_note", "Sch R also lists codes C $2,209,075, L $1,742,154, O $689,031, P $307,024 (V19)",
     "validation-wave19-report.md l.133"),
    ("EU013", "add_note", "GS & Co's payee label is 'TECH & INV ADV FEES', so technology_provider is a partial "
     "reading; investment advisory also (V22)", "validation-wave22-report.md l.177"),
    ("EV002", "add_note", "posting not re-observable (wave 23)", "validation-wave23-report.md l.243"),
    ("EV003", "add_note", "terms not re-read in wave 23 (npact.com unreachable)", "validation-wave23-report.md l.244"),
    ("EV006", "add_note", "the five CT-discovered clients ($9.81bn) are DNS-confirmed implementation hosts, not live "
     "portals (V23)", "validation-wave23-report.md l.245"),
    ("EV001", "add_note", "cite the fcjc.fftc.org page and the fftc.org link rather than daf.fftc.org/m/login "
     "(robots intent; V23)", "validation-wave23-report.md l.246"),
    ("EW020", "replace_note", ("file built 2014", "created 2014-11-18, modified 2023-01-02"),
     "validation-wave25b-report.md l.169-170"),
    ("EW020", "replace_note", ("file metadata 2014", "created 2014-11-18, modified 2023-01-02"),
     "validation-wave25b-report.md l.169-170"),
    ("EW019", "add_note", "amended FY6/22 return (filed 2024); also $197,000 cash to Dechomai Foundation (V25B)",
     "validation-wave25b-report.md l.171-172"),
    ("EX001", "add_note", "Fidelity named in the 2026 proxy only; not in the 2025 10-K (V26)",
     "validation-wave26-report.md l.171"),
    ("E086", "set_status", "confirmed", "red-team-wave2b-graph-data-incentives.md l.204"),
    ("E151", "add_note", "scope=donor_checkout", "red-team-wave2b-graph-data-incentives.md l.205"),
    ("E093", "set_status", "reported", "gap19-edward-jones-wealth-channels.md l.34, l.209-210 (EZ012)"),
    ("E093", "add_note", "not re-confirmed 2026-11-19: source URL redirects to the Private Wealth hub; live Wells "
     "Fargo DAF pages name no sponsor (EZ012); search-excerpt evidence only",
     "gap19-edward-jones-wealth-channels.md l.34, l.209-210 (EZ012)"),
    ("E094", "set_status", "reported", "gap19-edward-jones-wealth-channels.md l.209-210"),
    ("E094", "add_note", "not re-confirmed 2026-11-19 (same redirected source as E093); search-excerpt evidence only",
     "gap19-edward-jones-wealth-channels.md l.209-210"),
    ("E018", "add_note", "explicit negatives EZ001-EZ003 (10-Ks, ADV 2A, RCF audits): do not assume RCF or Ren",
     "gap19-edward-jones-wealth-channels.md l.23"),
)

# Explicit supersession notes inside the edge files (superseded edge, superseding edges).
# Only cases where the later edge restates the same relationship; note-level references
# (EJ005<-EP001, EA002<-EB001, EN004<-EV001, EJ007<-EM001, E045<-EZ008, EA016<-EE001) are
# annotated, not superseded.
SUPERSESSIONS = (
    ("EA027", ("EK021",)), ("EA032", ("EK030", "ED002")), ("EJ032", ("EM033",)), ("EH013", ("ER005",)),
    ("E034", ("EF001",)), ("EG008", ("EH004", "EH005")), ("E161", ("EA010",)), ("E092", ("EA016",)),
    ("E120", ("EA017",)), ("E162", ("EA025",)), ("E077", ("EA022",)),
)
ANNOTATE_ONLY = (("EJ005", "EP001"), ("EA002", "EB001"), ("EN004", "EV001"), ("EJ007", "EM001"),
                 ("E045", "EZ008"), ("EA016", "EE001"))


def apply_correction(edge: dict, op: str, val, ref: str) -> tuple:
    """Return (new_edge, log_row). Pure."""
    before = {"relationship_type": edge["relationship_type"], "status": edge["status"]}
    if op == "set_type":
        done = edge["relationship_type"] == val
        new = edge if done else {**edge, "relationship_type": val}
    elif op == "set_status":
        done = edge["status"] == val
        new = edge if done else {**edge, "status": val}
    elif op == "add_note":
        done = val.lower()[:40] in edge["notes"].lower()
        new = edge if done else {**edge, "notes": (edge["notes"] + " | " if edge["notes"] else "") + val}
    else:  # replace_note
        old, rep = val
        done = old not in edge["notes"] and old not in edge["evidence_summary"]
        new = edge if done else {**edge, "notes": edge["notes"].replace(old, rep),
                                 "evidence_summary": edge["evidence_summary"].replace(old, rep)}
    log = {"edge_id": edge["edge_id"], "op": op, "value": val if isinstance(val, str) else " -> ".join(val),
           "source": ref, "result": "already applied in source file" if done else "applied in consolidated file",
           "before_type": before["relationship_type"], "before_status": before["status"]}
    return new, log


def apply_corrections(edges: tuple) -> tuple:
    by_id = {e["edge_id"]: e for e in edges}

    def step(acc, c):
        eid, op, val, ref = c
        if eid not in acc[0]:
            return acc[0], acc[1] + ({"edge_id": eid, "op": op, "value": str(val), "source": ref,
                                      "result": "edge not found"},)
        new, log = apply_correction(acc[0][eid], op, val, ref)
        return {**acc[0], eid: new}, acc[1] + (log,)

    final, logs = reduce(step, VALIDATION_CORRECTIONS, (by_id, ()))
    return tuple(final[e["edge_id"]] for e in edges), logs


# ============================================================== normalise + dedup


def normalise(edge: dict, res: dict) -> dict:
    s, t, typ = edge["source_entity"], edge["target_entity"], edge["relationship_type"].strip()
    if typ in REVERSE_TYPES:
        s, t, typ = t, s, REVERSE_TYPES[typ]
    typ = TYPE_MAP.get(typ, typ)
    rs, rt = res[s], res[t]
    return {**edge, "src_id": rs["id"], "tgt_id": rt["id"], "src": rs["label"], "tgt": rt["label"],
            "src_ein": rs["ein"], "tgt_ein": rt["ein"], "type_norm": typ,
            "src_type": edge["source_type"] if s == edge["source_entity"] else edge["target_type"],
            "tgt_type": edge["target_type"] if t == edge["target_entity"] else edge["source_type"],
            "self_loop": rs["id"] == rt["id"]}


def strength(e: dict) -> tuple:
    url = e["source_url"].lower()
    primary = int(any(h in url for h in PRIMARY_HOSTS))
    acc = re.search(r"\d{4}-\d{2}-\d{2}", e["accessed_date"] or "")
    return (STATUS_RANK.get(e["status"], 0), primary, acc.group(0) if acc else "", e["edge_id"])


def dedup(edges: tuple, superseded: dict) -> tuple:
    """Group on unordered endpoints + type; the head is the strongest non-superseded edge."""
    groups = defaultdict(list)
    for e in edges:
        key = (tuple(sorted((e["src_id"], e["tgt_id"]))), e["type_norm"])
        groups[key].append(e)

    def head(members):
        live = [m for m in members if m["edge_id"] not in superseded] or members
        # a downgrade/correction edge governs the edge it corrects even if weaker
        return max(live, key=strength)

    out = []
    for key, members in groups.items():
        h = head(members)
        ids = [m["edge_id"] for m in sorted(members, key=lambda m: m["edge_id"] != h["edge_id"])]
        statuses = sorted({m["status"] for m in members})
        reversed_dup = any((m["src_id"], m["tgt_id"]) != (h["src_id"], h["tgt_id"]) for m in members)
        out.append({**h, "merged_edge_ids": ";".join(ids), "n_merged": len(members),
                    "merged_statuses": ";".join(statuses), "reversed_duplicate": reversed_dup,
                    "superseded_ids": ";".join(i for i in ids if i in superseded),
                    "member_files": ";".join(sorted({m["file"] for m in members}))})
    return tuple(sorted(out, key=lambda e: e["edge_id"]))


PLACEHOLDER_RX = r"^(unknown|unidentified|any daf|daf providers on dafpay)"
REDTEAM_STATUSES = ("inferred", "unknown", "probable", "reported", "pending")
VENDOR_CLAIM_RX = r"vendor[- ]claim|vendor[- ]stated|\[V\] vendor|vendor wording"


def evidence_class(e: dict) -> str:
    blob = " ".join((e["evidence_summary"], e["notes"], e["source_url"]))
    if e["status"] in REDTEAM_STATUSES:
        return e["status"]
    if "crt.sh" in e["source_url"].lower():
        return "crt.sh-sourced"
    if e["relationship_type"] == "vendor_claim" or re.search(VENDOR_CLAIM_RX, blob, re.I):
        return "vendor_claim"
    return ""


def redteam_set(edges: tuple, superseded: dict) -> tuple:
    return tuple(e for e in edges if evidence_class(e) and e["edge_id"] not in superseded)


# ============================================================== red-team checks
# One independent public check per edge. Fields: url ('dns:<host>' for a resolver check),
# find (regex on page text + raw HTML), on_find / on_absent outcomes, and what the check is.
# A page that is not fetched (robots unreadable/disallow, network error), or a 4xx/5xx on a
# URL chosen for this pass, gives 'unverified-lead' unless 'on_dead' is set (liveness checks).
# Outcomes: confirmed / weakened / unverified-lead / contradicted. For 'unknown' edges
# (explicit negatives / open slots) 'confirmed' means the slot is still unfilled on the
# independent source; 'contradicted' would mean a party is now named.

DC_NOTE = ("tenant live on donorcentral.com, but NPact acquired DonorCentral NXT and FIMS from Blackbaud "
           "(PR Newswire 2022-09-12, read in check of E087): vendor of record is NPact, not Blackbaud")
FC_NOTE = ("tenant serves 'Foundation Cloud Community Portal'; Foundation Cloud is NPact's per NPact's own "
           "customer stories (EN004 FFTC, EN005 Catholic Foundation), so the [R] owner caveat is lifted")
AK_NOTE = "tenant serves an akoyaGO module (GOfund/GOapply/GOdonate); scope may be grants or donations, not DAF"

CHECKS = {
    "E014": dict(url="https://edwardjones.donorfirstx.com/Terms%20of%20Service.pdf",
                 find=r"administ\w* (the |your )?(edward jones|fund|program)|Ren[^.]{0,80}administ",
                 on_find="confirmed", on_absent="unverified-lead",
                 what="EJ portal Terms of Service (a Renaissance Acquisition Company LLC agreement): does it give Ren an administration role?"),
    "E016": dict(url="https://edwardjones.donorfirstx.com/", find=r"portfolio[^.]{0,120}(managed|manager)[^.]{0,80}Edward Jones",
                 on_find="confirmed", on_absent="unverified-lead",
                 what="EJ CGF portal: who manages the portfolios?"),
    "E018": dict(url="https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds",
                 find=r"private (donor[- ]advised fund|DAF)[^.]{0,200}(sponsor|Renaissance|National Philanthropic|Fidelity Charitable)",
                 on_find="contradicted", on_absent="confirmed",
                 what="EJ DAF product page: is a sponsor named for the private DAF?"),
    "E058": dict(url="https://ft.donorfirstx.com/", find=r"sponsor\w*[^.]{0,80}Renaissance Charitable|Renaissance Charitable Foundation[^.]{0,60}sponsor",
                 on_find="confirmed", on_absent="unverified-lead",
                 what="Franklin portal re-read (no other public program document found): RCF named as sponsor?"),
    "E069": dict(url="https://tda.donorfirstx.com/", find=r"TD Ameritrade|Ameritrade", on_find="confirmed",
                 on_absent="unverified-lead", what="TDA-coded portal: does the page itself name TD Ameritrade?"),
    "E083": dict(url="https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf",
                 find=r"\bRen\b|reninc|RenPSG|Renaissance", on_find="confirmed", on_absent="weakened",
                 what="BofA CGF Program Guidelines v3.2024: is Ren named? (Guidelines say the fund 'is currently administered by Bank of America Private Bank')"),
    "E087": dict(url="https://prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html",
                 find=r"NPact Acquires FIMS and DonorCentral", on_find="weakened", on_absent="unverified-lead",
                 what="PR Newswire 2022-09-12: NPact acquired DonorCentral from Blackbaud, so AEF's DonorCentral vendor after 2022-09 was NPact (cf. EA024 NPact payee)"),
    "E088": dict(url="https://gccf.donorfirstx.com/", find=r"service: 'dfx'|DFX powered by Ren|Powered_by_REN",
                 on_find="confirmed", on_absent="unverified-lead", what="Direct fetch of the DFX tenant (edge rested on search index only)"),
    "E089": dict(url="https://semo.donorfirstx.com/", find=r"service: 'dfx'|DFX powered by Ren|Powered_by_REN",
                 on_find="confirmed", on_absent="unverified-lead", what="Direct fetch of the DFX tenant"),
    "E090": dict(url="https://jewishfed.donorfirst.org/", find=r"service: 'dfx'|DFX powered by Ren|Powered_by_REN",
                 on_find="confirmed", on_absent="unverified-lead", what="Direct fetch of the DonorFirst tenant"),
    "E093": dict(url="https://www.nptrust.org/", find=r"Wells Fargo", on_find="confirmed", on_absent="unverified-lead",
                 what="NPT home page: does NPT name a Wells Fargo program?"),
    "E094": dict(url="https://www.wellsfargoadvisors.com/private-wealth/conversations/philanthropy/donor-advised-funds.htm",
                 find=r"Wells Fargo[^.]{0,60}manages[^.]{0,40}investments", on_find="confirmed", on_absent="unverified-lead",
                 what="Live WF Advisors DAF page: does WF say it manages the DAF investments?"),
    "E113": dict(url="https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541919349300514_public.xml",
                 find=r"BNY MELLON,? N\.?A\.?|THE BANK OF NEW YORK MELLON", on_find="confirmed", on_absent="unverified-lead",
                 what="BNY CGF CY2024 Form 990 (e-file XML) instead of the CauseIQ aggregator: BNY Mellon N.A. named?"),
    "E155": dict(url="https://www.candid.org/", find=r"Groundswell", on_find="confirmed", on_absent="unverified-lead",
                 what="Candid side of the claimed integration"),
    "E157": dict(url="https://tifin.com/news/tifin-give-launches-louise-the-ai-platform-for-philanthropy/19124/",
                 find=r"OpenAI|GPT-?\d|Anthropic|\bClaude\b|Gemini|Llama|Mistral|Azure OpenAI|Bedrock",
                 on_find="contradicted", on_absent="confirmed",
                 what="Louise launch page re-read (tifingive.com unreachable): model vendor named?"),
    "EA001": dict(url="https://www.vanguardcharitable.org/", find=r"Give Interactive|giveinteractive",
                  on_find="confirmed", on_absent="unverified-lead",
                  what="Vanguard Charitable home page / login links: any Give Interactive reference?"),
    "EA005": dict(url="https://www.cct.org/", find=r"giveinteractive", on_find="confirmed", on_absent="unverified-lead",
                  what="Chicago Community Trust home page: login link to a Give Interactive tenant?"),
    "EA006": dict(url="https://jcfny.org/", find=r"giveinteractive", on_find="confirmed", on_absent="weakened",
                  what="JCF home page: client login link (login.jcfny.org) - Give Interactive?"),
    "EA007": dict(url="https://impactassets.org/", find=r"giveinteractive", on_find="confirmed", on_absent="weakened",
                  what="ImpactAssets home page: client login still on Ren iPhi (iphi.stellartechsol.com/calvert)?"),
    "EA009": dict(url="https://www.minneapolisfoundation.org/", find=r"giveinteractive", on_find="confirmed",
                  on_absent="weakened", what="Minneapolis Foundation home page: donor login still tmf.iphiview.com?"),
    "EA011": dict(url="https://www.thriventcharitable.com/", find=r"giveinteractive", on_find="confirmed",
                  on_absent="weakened", what="Thrivent Charitable home page: log-in still infaith.iphiview.com?"),
    "EA013": dict(url="https://www.stifelcharitable.org/", find=r"giveinteractive", on_find="confirmed",
                  on_absent="unverified-lead", what="Stifel Charitable home page: login link"),
    "EA015": dict(url="https://www.nhf.org/", find=r"giveinteractive", on_find="confirmed", on_absent="unverified-lead",
                  what="National Heritage Foundation home page: login link"),
    "EB009": dict(url="dns:jmacarthurtrust.giveinteractive.com", find=r".", on_find="unverified-lead",
                  on_dead="weakened", what="Public DNS (admissible re-source of a crt.sh-only lead): host resolves; identity still a slug match"),
    "ED007": dict(url="https://altruist.com/", find=r"(now|officially) part of Vanguard|Vanguard (has )?completed|acquisition[^.]{0,40}(closed|completed)",
                  on_find="contradicted", on_absent="confirmed",
                  what="Altruist home page: closing announced? (absent = still pending)"),
    "ED008": dict(url="dns:api-give.vanguardcharitable.org", find=r"execute-api|amazonaws", on_find="unverified-lead",
                  on_dead="weakened", what="Public DNS: host resolves (to an AWS API Gateway); name says nothing about the vendor"),
    "EE001": dict(url="https://www.nptgivingpoint.org/", find=r"DonorView|iPhi|Stellar|reninc", on_find="confirmed",
                  on_absent="unverified-lead", what="NPT GivingPoint front page: iPhi/DonorView/Ren markers?"),
    "EE007": dict(url="https://www.nptrust.org/annual-reports/npt-annual-report/", find=r"RSM US|RSM LLP|independent auditor",
                  on_find="confirmed", on_absent="unverified-lead", what="NPT 2025 annual report page: auditor named?"),
    "EE009": dict(url="https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf",
                  find=r"Ernst|independent auditor|audited", on_find="confirmed", on_absent="unverified-lead",
                  what="MS GIFT 'How it works' PDF: auditor named?"),
    "EG003": dict(url="https://thecommunityfoundation.spectrumportal.net/", find=r"Foundation Cloud Community Portal",
                  on_find="confirmed", on_absent="unverified-lead", what="GWCF tenant page; " + FC_NOTE),
    "EH003": dict(url="https://delcf.org/", find=r"delcf\.donorsphere\.org", on_find="confirmed", on_absent="unverified-lead",
                  what="DCF home page (first-party) links its Login Portal to delcf.donorsphere.org?"),
    "EH005": dict(url="https://pittsburghfoundation.org/", find=r"donorsphere", on_find="contradicted",
                  on_absent="confirmed", what="Pittsburgh Foundation home page: any DonorSphere link?"),
    "EH014": dict(url="https://www.jfnnj.org/", find=r"donorsphere", on_find="confirmed", on_absent="unverified-lead",
                  what="JFNNJ home page: DonorSphere login link?"),
    "EH015": dict(url="https://www.ncfgiving.com/", find=r"donorsphere", on_find="contradicted", on_absent="confirmed",
                  what="NCF home page: any DonorSphere link (absent = no current use shown)?"),
    "EJ005": dict(url="https://sbfoundation.org/", find=r"spectrumportal\.net", on_find="confirmed", on_absent="unverified-lead",
                  what="SBF home page links its Donor Portal to an NPact Foundation Cloud tenant (consistent with 'hosted infrastructure')"),
    "EJ020": dict(url="https://ircommunityfoundation.org/my-fund-has-been-upgraded/", find=r"fcsuite\.com|CommunitySuite|Foundant",
                  on_find="weakened", on_absent="unverified-lead",
                  what="IRCF 'My Fund has been Upgraded!' page: fund access moved to Foundant?"),
    "EJ025": dict(url="https://www.armanino.com/case-studies/transforming-nonprofit-technology-for-greater-impact/",
                  find=r"Vermont Community Foundation", on_find="confirmed", on_absent="unverified-lead",
                  what="Direct read of the Armanino case study (edge used search capture)"),
    "EJ026": dict(url="https://www.slalom.com/us/en/customer-stories", find=r"Silicon Valley Community Foundation|SVCF",
                  on_find="confirmed", on_absent="unverified-lead", what="Slalom customer stories: SVCF named?"),
    "EJ028": dict(url="https://www.fundminer.com/community", find=r"Warren County", on_find="confirmed",
                  on_absent="weakened", what="FundMiner community page re-read: Warren County still listed? (no CF page identified)"),
    "EK018": dict(url="https://keybank.iphiview.com/keybank/", find=r"KeyBank|KeyCorp", on_find="confirmed",
                  on_absent="weakened", on_dead="weakened", what="Live re-observation of the iPhi tenant (no KeyBank page links it)"),
    "EK022": dict(url="https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541919349300514_public.xml",
                  find=r"NO LONGER OPERATE THE DONOR ADVISED FUND", on_find="weakened", on_absent="unverified-lead",
                  what="BNY CGF CY2024 990: DAF program wound down (2024-12-24), so the iPhi tenant is historical at most"),
    "EK032": dict(url="https://kzcf.org/", find=r"blackbaud\.com", on_find="confirmed", on_absent="weakened",
                  what="Live re-observation of kzcf.org Blackbaud NXT donation form (CRM/ledger still only implied)"),
    "EK033": dict(url="https://intercom.help/rengiving/en/articles/6232119-charity-ach-setup-step-by-step",
                  find=r"ACH grant payments from our DAF programs|grant payments from our DAF programs",
                  on_find="confirmed", on_absent="unverified-lead", what="Ren help centre: Ren sends ACH grant payments for its DAF programs"),
    "EL027": dict(url="dns:nuance.fidelitycharitable.org", find=r"nuance", on_find="confirmed", on_absent="unverified-lead",
                  on_dead="weakened", what="Public DNS: does the host CNAME to a Nuance domain? (Akamai CNAME says nothing about the vendor)"),
    "EL028": dict(url="https://www.fidelitycharitable.org/nonprofits/faqs.html", find=r"reninc|Stellar|iPhi|donorfirst",
                  on_find="contradicted", on_absent="confirmed", what="Fidelity Charitable nonprofit FAQ: any Ren marker?"),
    "EM001": dict(url="https://www.daytonfoundation.org/", find=r"Fund ?360|fdnpartners|Foundation Partners", on_find="confirmed",
                  on_absent="unverified-lead", what="Dayton Foundation home page: Fund 360 / Foundation Partners named?"),
    "EM013": dict(url="https://vermontcf.org/donor-portal/", find=r"Sage Intacct|Salesforce|Experience Cloud|force\.com",
                  on_find="confirmed", on_absent="unverified-lead", what="VCF donor-portal page: Sage/Salesforce markers?"),
    "EM014": dict(url="https://thenytrust.org/", find=r"Sage Intacct|Intacct", on_find="confirmed", on_absent="unverified-lead",
                  what="NYCT home page: Sage Intacct named?"),
    "EM015": dict(url="https://thenytrust.org/", find=r"force\.com|salesforce", on_find="confirmed", on_absent="unverified-lead",
                  what="NYCT home page: Salesforce-hosted portal link?"),
    "EM016": dict(url="https://www.calfund.org/", find=r"Financial Edge", on_find="confirmed", on_absent="unverified-lead",
                  what="CCF home page: Financial Edge named?"),
    "EM017": dict(url="https://pittsburghfoundation.org/systems-solutions-architect", find=r"NetSuite", on_find="confirmed",
                  on_absent="unverified-lead", what="Direct read of the first-party posting (edge used search capture)"),
    "EM018": dict(url="https://pittsburghfoundation.org/systems-solutions-architect", find=r"Salesforce", on_find="confirmed",
                  on_absent="unverified-lead", what="Direct read of the first-party posting"),
    "EM019": dict(url="https://www.svcf.org/about/join-our-team", find=r"NetSuite", on_find="confirmed", on_absent="unverified-lead",
                  what="SVCF careers page (first-party): NetSuite named?"),
    "EM021": dict(url="https://www.ncfgiving.com/about/careers/", find=r"NetSuite", on_find="confirmed", on_absent="unverified-lead",
                  what="NCF careers page: NetSuite named?"),
    "EM034": dict(url="https://www.broadwestpartners.com/", find=r"Cambria", on_find="confirmed", on_absent="unverified-lead",
                  what="BroadWest site: Cambria named as investor?"),
    "EN001": dict(url="https://www.svcf.org/", find=r"NPact|Fund Investment Tool", on_find="confirmed", on_absent="unverified-lead",
                  what="SVCF site: NPact/FIT named (sponsor-side confirmation of the vendor case study)?"),
    "EN008": dict(url="https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived", find=r"Financial Edge",
                  on_find="confirmed", on_absent="unverified-lead", what="GWCF portal announcement (first-party): Financial Edge NXT named as ledger?"),
    "EN011": dict(url="https://ircf.donor-portal.org/login", find=r"Indian River|IRCF", on_find="unverified-lead",
                  on_absent="weakened", on_dead="weakened",
                  what="donor-portal.org tenant still live? (tenant use does not show back-office service; IRCF also sends fund access to Foundant)"),
    "EP003": dict(url="https://www.sdfoundation.org/", find=r"Financial Edge|blackbaud", on_find="confirmed", on_absent="unverified-lead",
                  what="SDF home page: Blackbaud markers?"),
    "EP004": dict(url="https://www.nevadacf.org/", find=r"blackbaud", on_find="confirmed", on_absent="unverified-lead",
                  what="NCF (Nevada) home page: Blackbaud markers?"),
    "EP007": dict(url="https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf",
                  find=r"\bRen\b|reninc|Ren for Charities", on_find="confirmed", on_absent="unverified-lead",
                  what="MS GIFT 'How it works' PDF (MS side): Ren named for disbursement?"),
    "EP008": dict(url="https://www.prnewswire.com/news-releases/ren-debuts-rapid-disbursement-engine-expanding-philanthropic-services-to-meet-rapid-daf-growth-301999647.html",
                  find=r"Renaissance Charitable", on_find="confirmed", on_absent="unverified-lead",
                  what="Ren Rapid Disbursement Engine release: RCF named as a user?"),
    "EQ008": dict(url="https://guide.charityvest.org/about-our-venture/charityvest-%2B-vennfi", find=r"Foundation Source",
                  on_find="confirmed", on_absent="unverified-lead", what="Charityvest's own guide (sponsor side, no crt.sh): Foundation Source named?"),
    "EQ015": dict(url="https://www.giftingnetwork.com/", find=r"Orion", on_find="confirmed", on_absent="unverified-lead",
                  what="GiftingNetwork site: Orion partnership named?"),
    "ER016": dict(url="https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds",
                  find=r"private (donor[- ]advised fund|DAF)[^.]{0,200}(sponsor|Renaissance|National Philanthropic|Fidelity Charitable)",
                  on_find="contradicted", on_absent="confirmed", what="EJ DAF product page (independent of the release): sponsor named for the private DAF?"),
    "ER018": dict(url="https://www.cafamerica.org/", find=r"Bonterra|CyberGrants", on_find="unverified-lead", on_absent="unverified-lead",
                  what="CAF America site: Bonterra named? (even if so, the GS Gives hop is unstated)"),
    "ES016": dict(url="https://www.dafdirect.org/", find=r"BNY", on_find="weakened", on_absent="confirmed",
                  what="dafdirect.org: BNY still listed although the 990 records the DAF program's wind-down?"),
    "ES022": dict(url="https://www.aleragroup.com/", find=r"GiveClear", on_find="confirmed", on_absent="unverified-lead",
                  what="Alera Group site: GiveClear named as Alera Charitable's sponsor?"),
    "EV005": dict(url="https://jpmgiving.org/", find=r"export", on_find="confirmed", on_absent="unverified-lead",
                  what="jpmgiving.org front page: export feature described?"),
    "EV006": dict(url="https://www.giveinteractive.com/", find=r"\$40\s?B", on_find="unverified-lead", on_absent="unverified-lead",
                  what="No independent source can test a vendor's own volume claim; vendor home page re-read"),
    "EV007": dict(url="https://pnc.iphiview.com/scbf/", find=r"PNC", on_find="confirmed", on_absent="weakened", on_dead="weakened",
                  what="Live tenant path (host resolves to a Ren load balancer)"),
    "EV008": dict(url="dns:ocf.iphiview.com", find=r".", on_find="unverified-lead", on_dead="weakened",
                  what="Public DNS: does the tenant host still exist?"),
    "EX004": dict(url="https://www.pledge1percent.org/pledging-1-percent-to-charity-made-easy-for-companies/", find=r"Tides",
                  on_find="unverified-lead", on_absent="unverified-lead",
                  what="Pledge 1% page (sponsor source for Twilio.org): only a Tides referral, not Twilio-specific"),
    "EX017": dict(url="https://www.crowdstrike.com/en-us/about-us/crowdstrike-foundation/", find=r"CAF America|Charities Aid Foundation",
                  on_find="confirmed", on_absent="unverified-lead", what="CrowdStrike Foundation page: CAF America named?"),
    "EX025": dict(url="https://www.pledge1percent.org/pledging-1-percent-to-charity-made-easy-for-companies/", find=r"Tides",
                  on_find="confirmed", on_absent="unverified-lead", what="Pledge 1% public page (edge used a 403 community guide)"),
    "EY006": dict(url="https://dafgiving360.org/explore-charities", find=r"Candid|GuideStar", on_find="confirmed",
                  on_absent="unverified-lead", what="Direct read (edge used a search snippet)"),
    "EY007": dict(url="https://dafgiving360.org/explore-charities", find=r"Charity Navigator", on_find="confirmed",
                  on_absent="unverified-lead", what="Direct read (edge used a search snippet)"),
    "EY008": dict(url="https://www.vanguardcharitable.org/nonprofit-organizations", find=r"Candid|GuideStar",
                  on_find="confirmed", on_absent="unverified-lead", what="Vanguard Charitable nonprofit page (sponsor side): Candid named?"),
    "EY015": dict(url="https://benevity.com/solutions/nonprofit-due-diligence", find=r"Charity ?Navigator", on_find="confirmed",
                  on_absent="weakened", what="Direct re-read of the Benevity page (the snippet text was not on the 2026-11-15 fetch)"),
    "EY018": dict(url="https://help.daffy.org/en/", find=r"IRS", on_find="confirmed", on_absent="unverified-lead",
                  what="Daffy help centre front page: IRS status check described?"),
    "EZ001": dict(url="https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds",
                  find=r"private (donor[- ]advised fund|DAF)[^.]{0,200}(sponsor|Renaissance|National Philanthropic|Fidelity Charitable)",
                  on_find="contradicted", on_absent="confirmed", what="EJ DAF product page: sponsor named for the private DAF?"),
    "EZ002": dict(url="https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds",
                  find=r"private (donor[- ]advised fund|DAF)[^.]{0,200}(sponsor|Renaissance|National Philanthropic|Fidelity Charitable)",
                  on_find="contradicted", on_absent="confirmed", what="EJ DAF product page: sponsor named for the private DAF?"),
    "EZ003": dict(url="https://renaissancecharitable.org/", find=r"Edward Jones", on_find="unverified-lead", on_absent="confirmed",
                  what="RCF home page: Edward Jones named? (the standard EJ CGF is RCF's; only a private-DAF reference would contradict)"),
    "EZ010": dict(url="https://www.pavefinance.com/", find=r"charit|donor[- ]advised|philanthrop", on_find="contradicted",
                  on_absent="confirmed", what="Pave home page: any DAF/charitable offering?"),
    "EZ012": dict(url="https://www.nptrust.org/", find=r"Wells Fargo", on_find="contradicted", on_absent="confirmed",
                  what="NPT home page: Wells Fargo program named? (absent = slot stays unconfirmed)"),
    "EZ022": dict(url="https://www.usbank.com/wealth-management/charitable-giving-strategies.html",
                  find=r"sponsor(ing)? organization[^.]{0,80}(is|:)\s+[A-Z]|National Philanthropic|Fidelity Charitable|Renaissance Charitable|Schwab Charitable|American Endowment",
                  on_find="contradicted", on_absent="confirmed", what="U.S. Bank charitable-giving page re-read: sponsor named?"),
}


def tenant_url(evidence: str) -> str:
    m = re.search(r"->\s*(https?://\S+)", evidence)
    return m.group(1).rstrip(".,;") if m else ""


def auto_check(e: dict) -> dict:
    """Checks for the automated CF vendor-map edges (EI*): fetch the vendor tenant itself."""
    url = tenant_url(e["evidence_summary"])
    ev = e["evidence_summary"]
    if "spectrumportal" in url:
        return dict(url=url, find=r"Foundation Cloud Community Portal", on_find="confirmed", on_absent="unverified-lead",
                    what="Direct fetch of the vendor tenant; " + FC_NOTE)
    if "donorcentral" in url:
        return dict(url=url, find=r"<title>\s*Donorcentral", on_find="weakened", on_absent="unverified-lead",
                    on_dead="weakened", what="Direct fetch of the vendor tenant; " + DC_NOTE)
    if "akoyago" in url:
        return dict(url=url, find=r"GOfund|GOapply|GOdonate|akoya", on_find="confirmed", on_absent="unverified-lead",
                    what="Direct fetch of the vendor tenant; " + AK_NOTE)
    return dict(url=url or e["source_url"], find=re.escape(e["source_entity"][:12]), on_find="confirmed",
                on_absent="unverified-lead", what="Direct fetch of the linked host: " + ev[:80])


def check_for(e: dict) -> dict:
    return CHECKS.get(e["edge_id"]) or auto_check(e)


def run_check(e: dict) -> dict:
    c = check_for(e)
    base = {"edge_id": e["edge_id"], "evidence_class": evidence_class(e), "check_url": c["url"],
            "check_description": c["what"], "check_regex": c["find"]}
    if c["url"].startswith("dns:"):
        d = dns(c["url"][4:])
        if not d["ok"]:
            oc = c.get("on_dead", "unverified-lead")
            return {**base, "fetch_result": "DNS: " + d["error"], "http_status": "", "matched": "", "outcome": oc}
        hay = d["cname"] + " " + " ".join(d["ips"])
        hit = re.search(c["find"], hay, re.I)
        return {**base, "fetch_result": f"DNS ok cname={d['cname'] or '-'} ips={','.join(d['ips'])}", "http_status": "",
                "matched": hay[:120] if hit else "", "outcome": c["on_find"] if hit else c["on_absent"]}
    r = fetch(c["url"])
    st = r["status"]
    fr = r["outcome"] + (f" -> {r['final']}" if r["final"] != c["url"] else "")
    if r["outcome"] != "fetched":
        oc = c.get("on_dead", "unverified-lead") if r["outcome"].startswith("error") and "Name or service" in r["outcome"] \
            else "unverified-lead"
        return {**base, "fetch_result": fr[:200], "http_status": "", "matched": "", "outcome": oc}
    if st >= 400:
        oc = c.get("on_dead", "unverified-lead") if st in (404, 410) else "unverified-lead"
        return {**base, "fetch_result": fr[:200], "http_status": st, "matched": "", "outcome": oc}
    hay = r["body"] if r.get("pdf") else text_of(r["body"]) + " " + r["body"]
    m = snippet(hay, c["find"], 70)
    return {**base, "fetch_result": fr[:200], "http_status": st, "matched": m[:240],
            "outcome": c["on_find"] if m else c["on_absent"]}
