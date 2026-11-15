#!/usr/bin/env python3
"""P-CFV-02 / P-B29A-02 (batch 30C): close unmapped community foundations in the CF vendor map, and split
the Foundation Cloud (spectrumportal.net) rows into portal-only versus ledger.

Input : data/mission-2026-11-14/cf-vendor-map-by-ein.csv (v1, 803 CFs, 315 'unmapped').
Output: data/mission-2026-11-14/cf-vendor-map-by-ein-v2.csv     (all 803 rows, v1 columns + change_note)
        data/mission-2026-11-14/cf-vendor-close-signals-v2.csv  (every new signal per EIN)
        data/mission-2026-11-14/cf-vendor-map-summary-v2.json   (coverage and shares, v1 vs v2)
        data/mission-2026-11-14/spectrumportal-portal-vs-ledger-v2.csv (P-B29A-02 split, 14 rows)

Passes for each v1-unmapped CF (public, passive; no logins, no forms, no tenant APIs):
  1. Website: v1 homepage, else <WebsiteAddressTxt> from any harvested e-filed 990 (not only the latest).
  2. Fresh homepage crawl with the v1 crawler (robots.txt honoured, <=1 req/s/host, same identifying UA,
     no UA spoofing; blocked sites are not worked around).
  3. Raw-HTML scan of every fetched page (menus rendered in JS/JSON are missed by the anchor parser) for
     DAF-specific vendor hosts only (fcsuite, iphiview, spectrumportal, akoyaGO, donorsphere, giveinteractive,
     donorcentral, fund-miner, donor-portal.org); generic hosts (Salesforce, Blackbaud hosted) are not used.
  4. sitemap.xml login-like URLs, else six common login paths (/login/, /donor-login/, ...), up to 4 pages.
  5. DNS (dns.google): CNAME chain for six own-domain portal labels; A lookup of <domain stem> under the
     vendor zones that have NO wildcard (fcsuite.com, iphiview.com, spectrumportal.net, giveinteractive.com:
     a random label returns NXDOMAIN, checked at run time). A label counts only if it is >=3 chars and is
     the stem of exactly one CF in the 803-CF universe; for fcsuite/iphiview/spectrumportal one GET of the public
     sign-in page checks for a link back to the CF's own domain (vendor_tenant_backlink, medium); a bare DNS hit is low.
  6. Full text of the latest harvested e-filed 990 XML (Schedule O, Part IX other-expense lines, Part VII-B)
     for vendor names.
  7. Repo cross-references: cf-ledger-families-2026(-v2).csv, ren-iphi-tenant-census.csv (live tenants), and
     hand checks in data/mission-2026-11-14/cf-vendor-close-handchecks-batch30.csv (WebFetch/search reads).

Usage:
  python3 scripts/mission_cf_vendor_close.py --fetch --cache-dir <dir>   # network + cache
  python3 scripts/mission_cf_vendor_close.py --cache-dir <dir>           # rebuild from cache only
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import json
import os
import re
import sys
import threading
import time
import urllib.parse
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_cf_vendor_map as m  # noqa: E402  (reuse the v1 crawler, signatures and network layer)

DATA = m.DATA
V1 = f"{DATA}/cf-vendor-map-by-ein.csv"
OUT = f"{DATA}/cf-vendor-map-by-ein-v2.csv"
OUT_SIG = f"{DATA}/cf-vendor-close-signals-v2.csv"
OUT_SUM = f"{DATA}/cf-vendor-map-summary-v2.json"
OUT_SPLIT = f"{DATA}/spectrumportal-portal-vs-ledger-v2.csv"
HAND = f"{DATA}/cf-vendor-close-handchecks-batch30.csv"
LEDGER_V1 = f"{DATA}/cf-ledger-families-2026.csv"
LEDGER_V2 = f"{DATA}/cf-ledger-families-2026-v2.csv"
REN_CENSUS = f"{DATA}/ren-iphi-tenant-census.csv"
SPECTRUM_AUDIT = f"{DATA}/spectrumportal-tenant-audit.csv"
RETRIEVED = "2026-11-15"

DAF_SPECIFIC = tuple(v for v in m.VENDOR_HOST_RE if not v[4] and v[0] not in ("GiftingNetwork",))
URL_RE = re.compile(r"""https?:(?:\\?/){2}([a-z0-9][a-z0-9.-]+\.[a-z]{2,})(/[^\s"'<>\\)]*)?""", re.I)
OWN_LABELS = ("donor", "donors", "portal", "myfund", "fund", "giving", "mycf", "login", "donorportal", "fundportal")
VENDOR_ZONES = (("fcsuite.com", "Foundant", "Foundant CommunitySuite", "yes", "/erp/portal"),
                ("iphiview.com", "Ren / Stellar iPhi", "Ren (Stellar) iPhi DonorView", "yes", "/"),
                ("spectrumportal.net", "Foundation Cloud (spectrumportal.net; NPact [R])", "Foundation Cloud portal (spectrumportal.net)", "yes", "/accounts/signin"),
                ("giveinteractive.com", "Give Interactive", "Give Interactive", "yes", ""))
GUESS_PATHS = ("/login/", "/donor-login/", "/fund-login/", "/fundholder-login/", "/donor-portal/", "/fund-holders/")
SITEMAP_LOGIN = re.compile(r"login|log-in|sign-in|fundholder|fund-holder|donor-portal|donorportal|my-fund|myfund|access-your-fund|fund-access|online-access|donor-access|fund-portal", re.I)
# 990 full-text vendor names (Schedule O, Part IX other expenses, VII-B). Strong = DAF fund-accounting vendors.
TXT990 = (
    ("Foundant", "Foundant (990 text)", r"FOUNDANT|COMMUNITY ?SUITE|FCSUITE", True),
    ("Ren / Stellar iPhi", "Stellar/Ren (990 text)", r"STELLAR TECHNOLOGY|\bIPHI\b|RENAISSANCE PHILANTHROPIC|RENPSG", True),
    ("Foundation Cloud (spectrumportal.net; NPact [R])", "NPact / Fusion Labs (990 text)", r"\bNPACT\b|FUSION LAB", True),
    ("akoyaGO", "Akoya (990 text)", r"\bAKOYA", True),
    ("DonorSphere / FidTech", "FidTech (990 text)", r"FIDTECH|DONORSPHERE", True),
    ("Give Interactive", "Give Interactive (990 text)", r"GIVE INTERACTIVE", True),
    ("GiftingNetwork", "GiftingNetwork (990 text)", r"GIFTING ?NETWORK", True),
    ("Blackbaud", "Blackbaud (990 text; product not stated)", r"BLACKBAUD|MICROEDGE|FINANCIAL EDGE|\bFIMS\b", False),
)
TXT990_RE = tuple((f, p, re.compile(rx, re.I), s) for f, p, rx, s in TXT990)
PRIORITY = {**m.PRIORITY, "hand_check_first_party": 9, "repo_ren_census_live": 8, "raw_html_vendor_host": 6,
            "login_path_vendor_host": 8, "vendor_tenant_backlink": 5, "vendor_zone_dns_label": 3, "990_text_vendor_name": 3,
            "repo_ledger_families": 2, "hand_check_secondary": 2}
FAM_LEDGER = {v[0]: v[2] for v in m.VENDORS}


class Net(m.Net):
    """v1 network layer, with dns.google allowed at 5 req/s (public resolver) and all other hosts at <=1 req/s."""

    def _throttle(self, host: str) -> None:
        with self._meta:
            lock = self._locks[host]
        with lock:
            gap = 0.2 if host == "dns.google" else m.MIN_INTERVAL
            wait = self._last.get(host, 0) + gap - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last[host] = time.monotonic()


def sig(fam, prod, led, etype, url, detail, strength=3, context=True) -> dict:
    return {**m.signal(fam, prod, led, etype, url, detail, strength, context), "detail": detail[:300]}


# ---------------------------------------------------------------- passes
def raw_vendor_hosts(body: str, page: str, etype: str = "raw_html_vendor_host") -> list[dict]:
    seen, out = set(), []
    for mm in URL_RE.finditer(body or ""):
        h = mm.group(1).lower()
        v = next(((f, p, l) for f, p, l, rx, _ in DAF_SPECIFIC if rx.search(h)), None)
        if v and h not in seen and not h.startswith(("www.fcsuite", "www.akoyago", "www.giveinteractive")) and h not in ("fcsuite.com", "akoyago.com"):
            seen.add(h)
            out.append(sig(*v, etype, page, f"page {page[:100]} contains {mm.group(0)[:150]}"))
    return out


def dns_json(net: Net, name: str, rtype: str) -> dict:
    res = net.get("https://dns.google/resolve?" + urllib.parse.urlencode({"name": name, "type": rtype}), {"Accept": "application/dns-json"}, timeout=15)
    try:
        return json.loads(res.get("body") or "{}")
    except ValueError:
        return {}


def resolves(net: Net, name: str) -> bool:
    d = dns_json(net, name, "A")
    return d.get("Status") == 0 and any(a.get("type") in (1, 5) for a in d.get("Answer", []))


def non_wildcard_zones(net: Net) -> tuple:
    return tuple(z for z in VENDOR_ZONES if not resolves(net, f"zq7x0probe1k.{z[0]}"))


def page_pass(net: Net, own: str, home: str, home_body: str) -> tuple[list[dict], list[str]]:
    """Raw scan of homepage + sitemap/guessed login pages."""
    sigs = raw_vendor_hosts(home_body, home)
    origin = "https://" + host_of_safe(home)
    sm = m.polite_get(net, origin + "/sitemap.xml")
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sm.get("body", "") or "")
    subs = [u for u in locs if u.endswith(".xml")][:4]
    for s in subs:
        locs += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", m.polite_get(net, s).get("body", "") or "")
    cands = [u for u in locs if not u.endswith(".xml") and SITEMAP_LOGIN.search(urllib.parse.urlsplit(u).path)][:4]
    tried = []
    for u in (cands or [origin + p for p in GUESS_PATHS]):
        res = m.polite_get(net, u)
        tried.append(f"{u} -> {res.get('status')}")
        fin = res.get("final_url") or ""
        fh = m.host_of(fin)
        if fh and m.reg_domain(fh) != own:
            v = m.vendor_by_host(fh)
            if v:
                sigs.append(sig(v[0], v[1], v[2], "login_path_vendor_host", u, f"{u[:100]} redirects to {fin[:150]}"))
            continue
        if res.get("status") == 200 and res.get("body"):
            s2, _, _ = m.link_signals(m.anchors(res["body"], fin or u), fin or u, own)
            sigs += [{**s, "evidence_type": "login_path_vendor_host" if s["evidence_type"] == "homepage_link_vendor_host" else s["evidence_type"]} for s in s2]
            sigs += raw_vendor_hosts(res["body"], fin or u)
    return sigs, tried


def host_of_safe(url: str) -> str:
    return m.host_of(url) or ""


def dns_pass(net: Net, own: str, stem_ok: bool, zones: Sequence) -> list[dict]:
    out = []
    for lab in OWN_LABELS:
        chain = m.dns_cname_chain(net, f"{lab}.{own}")
        v = next((m.vendor_by_host(c) for c in chain if m.vendor_by_host(c)), None)
        if v:
            out.append(sig(v[0], v[1], v[2], "dns_cname", f"https://dns.google/resolve?name={lab}.{own}&type=CNAME",
                           f"{lab}.{own} CNAME -> {' -> '.join(chain)[:200]}"))
    stem = own.split(".")[0]
    if stem_ok:
        for zone, fam, prod, led, path in zones:
            host = f"{stem}.{zone}"
            if not resolves(net, host):
                continue
            back, note = False, "tenant page not fetched (Give: tenant pages not probed)"
            if path:  # one GET of the public sign-in page; look for a link back to the CF's own domain
                res = m.polite_get(net, f"https://{host}{path}")
                body = res.get("body", "") or ""
                back = bool(re.search(r"https?://(www\.)?" + re.escape(own) + r"\b", body, re.I))
                note = f"GET https://{host}{path} -> {res.get('status')}; " + ("page links back to " + own if back else "no link back to " + own)
            out.append(sig(fam, prod, led, "vendor_tenant_backlink" if back else "vendor_zone_dns_label",
                           f"https://dns.google/resolve?name={host}&type=A",
                           f"{host} resolves; {zone} has no wildcard (random label NXDOMAIN); label = this CF's unique domain stem; {note}", 1))
    return out


def xml990_pass(net: Net, url: str) -> list[dict]:
    if not url:
        return []
    res = net.get(url, timeout=60, max_bytes=6_000_000)
    body = res.get("body", "") or ""
    out = []
    for fam, prod, rx, strong in TXT990_RE:
        mm = rx.search(body)
        if mm:
            a, b = max(0, mm.start() - 120), mm.end() + 120
            ctx = re.sub(r"<[^>]+>", " ", body[a:b])
            out.append(sig(fam, prod, FAM_LEDGER.get(fam, "unknown") if strong else "unknown", "990_text_vendor_name", url,
                           f"990 XML text: ...{re.sub(r'\\s+', ' ', ctx).strip()[:220]}...", 1))
    return out


def repo_signals() -> dict[str, list[dict]]:
    out = collections.defaultdict(list)
    for path in (LEDGER_V1, LEDGER_V2):
        for r in m.read_csv(path):
            if r["ledger_family"] not in ("UNRESOLVED", "NPACT") and r["confidence"] in ("high", "medium"):
                out[m.ein9(r["ein"])].append(sig("", "", "", "repo_ledger_families", path, f"{os.path.basename(path)}: {r['ledger_family']} ({r['confidence']}): {r['product'][:150]}", 0))
    for r in m.read_csv(REN_CENSUS):
        e = m.ein9(r.get("ein") or "0")
        if r.get("ein") and r.get("status", "") == "active":
            out[e].append(sig("Ren / Stellar iPhi", "Ren (Stellar) iPhi DonorView", "yes", "repo_ren_census_live", r.get("tenant_url") or r["host"],
                              f"ren-iphi-tenant-census.csv: {r['host']}{r['path']} status={r['status']} ({r.get('status_basis','')[:120]})"))
    if os.path.exists(HAND):
        for r in m.read_csv(HAND):
            out[m.ein9(r["ein"])].append(sig(r["family"], r["product"], r["ledger_implied"], r["evidence_type"], r["source_url"], r["detail"],
                                             3 if r["evidence_type"] == "hand_check_first_party" else 1))
    return dict(out)


# ---------------------------------------------------------------- decision
def decide(sigs: Sequence[Mapping]) -> dict:
    named = [s for s in sigs if s.get("family") and not s["family"].startswith("Foundant GLM")]
    if not named:
        return {}
    fams = collections.Counter(s["family"] for s in named)
    best = max(named, key=lambda s: (PRIORITY.get(s["evidence_type"], 0), fams[s["family"]]))
    same = [s for s in named if s["family"] == best["family"] and s is not best]
    et, p = best["evidence_type"], PRIORITY.get(best["evidence_type"], 0)
    if p >= 6 and et != "raw_html_vendor_host":
        conf = "high"
    elif et == "raw_html_vendor_host":
        conf = "high" if same else "medium"
    elif et == "vendor_tenant_backlink":
        conf = "medium"
    elif et in ("990_part_vii_b_contractor",):
        conf = "medium" if best["family"] in m.STRONG_990 else "low"
    elif et in ("vendor_zone_dns_label", "990_text_vendor_name"):
        conf = "medium" if any(s["evidence_type"] in ("vendor_zone_dns_label", "990_text_vendor_name", "990_part_vii_b_contractor") and s["evidence_type"] != et for s in same) else "low"
        if best["family"] == "Blackbaud":
            conf = "low"
    else:
        conf = "low"
    url = re.search(r"https?://[^\s'\"]+", best["detail"])
    portal = url.group(0) if url and et not in ("990_text_vendor_name",) else ("https://" + best["detail"].split(" ")[0] if et in ("vendor_zone_dns_label", "vendor_tenant_backlink") else "")
    if et == "dns_cname":
        portal = "https://" + best["detail"].split(" ")[0]
    conflicts = sorted({f"{s['family']} ({s['evidence_type']})" for s in named if s["family"] != best["family"]})
    return {"portal_vendor": best["product"] or best["family"], "vendor_family": best["family"], "portal_url": portal,
            "evidence_type": et, "evidence_url": best["evidence_url"], "confidence": conf,
            "ledger_implied": best["ledger_implied"] or FAM_LEDGER.get(best["family"], "unknown"),
            "evidence_detail": best["detail"], "corroborating_evidence": " | ".join(sorted({f"{s['evidence_type']}: {s['detail'][:110]}" for s in same}))[:600],
            "conflicting_signals": "; ".join(conflicts)[:300]}


# ---------------------------------------------------------------- P-B29A-02 split
SPLIT_RULES = {  # ein -> (class, ledger_reading, confidence, basis). Evidence quoted in the batch30 report.
    "566047886": ("portal over Blackbaud FE NXT", "BLACKBAUD_FE", "medium", "NPact story: FE NXT + FCG/FCCP (batch29 v2 row)"),
    "237343119": ("portal over Blackbaud FE NXT", "BLACKBAUD_FE", "medium", "Portal 'replaces Donor Central'; Blackbaud REPAY grant rail; 990 BLACKBAUD 'TECHNOLOGY' (batch29 v2 row)"),
}


def split_rows(v1rows: Sequence[Mapping], hand_split: Mapping[str, Mapping]) -> list[dict]:
    audit = {m.ein9(r["ein"]): r for r in m.read_csv(SPECTRUM_AUDIT)}
    lv2 = {m.ein9(r["ein"]): r for r in m.read_csv(LEDGER_V2)}
    out = []
    for r in v1rows:
        if not r["vendor_family"].startswith("Foundation Cloud"):
            continue
        e, a = r["ein"], audit.get(r["ein"], {})
        h = hand_split.get(e)
        if e in lv2 and lv2[e]["ledger_family"] != "NPACT":
            cls, led, conf, basis = SPLIT_RULES.get(e, ("portal over other GL", lv2[e]["ledger_family"], lv2[e]["confidence"], "cf-ledger-families-2026-v2.csv"))
        elif h:
            cls, led, conf, basis = h["split_class"], h["ledger_reading"], h["confidence"], h["detail"]
        elif a.get("portal_role", "").startswith("partner/grantee"):
            cls, led, conf, basis = "not a fund portal (partner/grantee portal)", "not evidenced", "high", f"spectrumportal-tenant-audit.csv: {a.get('migration_event','')[:160]}"
        elif "Blackbaud" in a.get("ledger_reading", ""):
            cls, led, conf, basis = "portal over Blackbaud (inferred)", "BLACKBAUD (RE/FE NXT inferred)", "low", f"spectrumportal-tenant-audit.csv: {a.get('ledger_reading','')} | {a.get('homepage_keywords','')}"
        elif "NPact" in a.get("ledger_reading", ""):
            cls, led, conf, basis = "NPact-hosted (ledger possible)", "NPACT (Fusion Labs hosting payee) [I]", "low", f"spectrumportal-tenant-audit.csv: {a.get('npact_990','')}"
        else:
            cls, led, conf, basis = "portal; GL not evidenced", "unknown", "none", "no GL evidence in 990 VII-B, homepage keywords or postings found"
        out.append({"ein": e, "name": r["name"], "fy2024_daf_assets_usd": r["fy2024_daf_assets_usd"], "portal_url": r["portal_url"],
                    "split_class": cls, "ledger_reading": led, "confidence": conf, "basis": basis[:400],
                    "ledger_families_v1": "NPACT (portal_suite_implied)", "retrieved": RETRIEVED})
    return out


# ---------------------------------------------------------------- shares
def shares(rows: Sequence[Mapping]) -> list[dict]:
    tn, ta = len(rows), sum(m.num(r["fy2024_daf_assets_usd"]) for r in rows)
    g = collections.defaultdict(lambda: [0, 0.0])
    for r in rows:
        k = r["vendor_family"] if r["confidence"] in ("high", "medium") else ("Unmapped (low-confidence signal only)" if r["confidence"] == "low" else
                                                                           "Unidentified portal" if r["vendor_family"] == "Unidentified portal" else "Unmapped")
        g[k][0] += 1
        g[k][1] += m.num(r["fy2024_daf_assets_usd"])
    return [{"vendor_family": k, "cfs": n, "share_cfs": round(n / tn, 4), "daf_assets_usd": round(a), "share_daf_assets": round(a / ta, 4)}
            for k, (n, a) in sorted(g.items(), key=lambda kv: -kv[1][0])]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--workers", type=int, default=24)
    a = ap.parse_args()
    net = Net(a.cache_dir, a.fetch)
    m._NETS[id(net)] = net
    v1 = m.read_csv(V1)
    stems = collections.Counter(m.domain_stem(m.host_of(r["homepage"])) for r in v1 if r["homepage"])
    um = [r for r in v1 if r["vendor_family"] in ("Unmapped",)]
    eins = frozenset(r["ein"] for r in um)
    xmls = m.latest_xml_urls(eins)
    zones = non_wildcard_zones(net)
    print(f"unmapped {len(um)}; non-wildcard zones {[z[0] for z in zones]}", flush=True)
    repo = repo_signals()
    c990 = m.contractor_signals(eins)
    done = collections.Counter()
    lock = threading.Lock()

    def run(r):
        home, hsrc = r["homepage"], ""
        if not home:
            home, hsrc = m.website_from_990(net, xmls.get(r["ein"], ())[:8])
        sigs, notes = [], []
        status = "no_homepage"
        if home:
            own = m.reg_domain(m.host_of(home))
            cr = m.crawl(net, {**r, "homepage": home})
            status = cr["crawl_status"]
            sigs += cr["signals"]
            hres = m.polite_get(net, home)
            if hres.get("body"):
                ps, tried = page_pass(net, own, hres.get("final_url") or home, hres["body"])
                sigs += ps
                notes.append("login pages tried: " + "; ".join(tried)[:300])
            stem = own.split(".")[0]
            sigs += dns_pass(net, own, len(stem) >= 3 and stems.get(stem, 0) <= 1, zones)
        x = xmls.get(r["ein"], ())
        sigs += xml990_pass(net, x[0] if x else "")
        sigs += list(c990.get(r["ein"], ())) + repo.get(r["ein"], [])
        with lock:
            done["n"] += 1
            if done["n"] % 25 == 0:
                print(f"done {done['n']}", flush=True)
        return {"home": home, "home_src": hsrc, "status": status, "sigs": sigs, "notes": notes}

    with cf.ThreadPoolExecutor(a.workers) as ex:
        res = dict(zip((r["ein"] for r in um), ex.map(run, um)))

    hand_split = {m.ein9(r["ein"]): r for r in (m.read_csv(HAND) if os.path.exists(HAND) else ()) if r.get("split_class")}
    split = split_rows(v1, hand_split)
    split_by = {s["ein"]: s for s in split}
    out_rows, sig_rows = [], []
    for r in v1:
        row = {**r, "retrieved": r["retrieved"], "change_note": "unchanged (v1)"}
        if r["ein"] in res:
            rr = res[r["ein"]]
            d = decide(rr["sigs"])
            ledger_notes = [s["detail"] for s in rr["sigs"] if s["evidence_type"] == "repo_ledger_families"]
            base = {"homepage": rr["home"] or r["homepage"], "crawl_status": f"v2:{rr['status']}", "retrieved": RETRIEVED}
            if rr["home_src"]:
                base["homepage_source"] = rr["home_src"]
            if d:
                row.update({**base, **d, "crawl_vendor_family": ""})
                row["change_note"] = f"unmapped -> {d['vendor_family']} ({d['confidence']}) via {d['evidence_type']}" + (f"; ledger file: {ledger_notes[0][:160]}" if ledger_notes else "")
            else:
                row.update(base)
                row["change_note"] = "still unmapped after v2 passes" + (f"; ledger file: {ledger_notes[0][:160]} (GL, not portal)" if ledger_notes else "")
            sig_rows += [{"ein": r["ein"], "name": r["name"], **{k: s.get(k, "") for k in ("family", "product", "ledger_implied", "evidence_type", "evidence_url", "detail", "strength")}}
                         for s in rr["sigs"] if s.get("family") or s["evidence_type"] in ("repo_ledger_families",)]
            sig_rows += [{"ein": r["ein"], "name": r["name"], "family": "", "product": "", "ledger_implied": "", "evidence_type": "note", "evidence_url": "", "detail": n, "strength": 0} for n in rr["notes"]]
        if r["ein"] in split_by:
            s = split_by[r["ein"]]
            new_led = "no" if s["split_class"].startswith(("portal over", "not a fund")) else ("yes" if s["split_class"].startswith("NPact") else "unknown")
            row["ledger_implied"] = new_led
            row["change_note"] = f"P-B29A-02 split: {s['split_class']}; ledger {s['ledger_reading']} ({s['confidence']}); ledger_implied yes -> {new_led}"
        out_rows.append(row)
    fields = tuple(v1[0].keys()) + ("change_note",)
    m.write_csv(OUT, out_rows, fields)
    m.write_csv(OUT_SIG, sig_rows, ("ein", "name", "family", "product", "ledger_implied", "evidence_type", "evidence_url", "detail", "strength"))
    m.write_csv(OUT_SPLIT, split, tuple(split[0].keys()))
    closed = [r for r in out_rows if r["ein"] in res and r["vendor_family"] not in ("Unmapped",)]
    tot = sum(m.num(r["fy2024_daf_assets_usd"]) for r in out_rows)
    summ = {
        "v1_unmapped": len(um), "v1_unmapped_assets_usd": round(sum(m.num(r["fy2024_daf_assets_usd"]) for r in um)),
        "closed_any_confidence": len(closed),
        "closed_by_confidence": collections.Counter(r["confidence"] for r in closed).most_common(),
        "closed_by_family": collections.Counter(f"{r['vendor_family']} [{r['confidence']}]" for r in closed).most_common(),
        "closed_by_evidence": collections.Counter(r["evidence_type"] for r in closed).most_common(),
        "closed_assets_usd": round(sum(m.num(r["fy2024_daf_assets_usd"]) for r in closed)),
        "closed_assets_share_of_cf_total": round(sum(m.num(r["fy2024_daf_assets_usd"]) for r in closed) / tot, 4),
        "still_unmapped": sum(1 for r in out_rows if r["vendor_family"] == "Unmapped"),
        "v2_crawl_status_unmapped_set": collections.Counter(re.sub(r"_\d+$|:.*", "", res[e]["status"]) for e in res).most_common(),
        "non_wildcard_zones": [z[0] for z in zones],
        "shares_v1": shares(v1), "shares_v2": shares(out_rows),
        "split_b29a02": collections.Counter(s["split_class"] for s in split).most_common(),
    }
    with open(OUT_SUM, "w", encoding="utf-8") as fh:
        json.dump(summ, fh, indent=1)
    print(json.dumps({k: v for k, v in summ.items() if not k.startswith("shares")}, indent=1))


if __name__ == "__main__":
    main()
