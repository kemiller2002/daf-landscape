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
            out = {"status": r.status, "location": r.headers.get("Location", ""),
                   "body": body.decode("utf-8", "replace"), "error": "",
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
        return {"outcome": oc, "url": url, "final": cur, "hops": hops, "status": r.get("status"),
                "body": r.get("body", ""), "headers": r.get("headers", {})}
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
