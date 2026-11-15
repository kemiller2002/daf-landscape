#!/usr/bin/env python3
"""P-CFV-03 (community-foundation ledger/portal switches, 2022-2026) and P-FCG-02 (Goodstack's US DAF sponsor 990s).

Task `migrations` (P-CFV-03). For the eight CFs that the CF vendor map flagged (three Stellar 990 payees with a
Foundant portal today; five with two fund-login vendors), fetch the dated public evidence and write one CSV with
two record types:
  * record_type=evidence: one row per fetched source, with the value extracted by a stated rule (WordPress REST
    `date`/`modified`, JSON-LD datePublished, Webflow "Last Published" comment, PDF CreationDate, crt.sh
    certificate not_before range, dns.google status, HTTP status, or a regex snippet of the page text), plus the
    990 Part VII-B vendor lines for the CF from form990-contractors-harvest-full.csv (TY2021+).
  * record_type=event: one row per CF: from-system, to-system, direction, event date and its basis, confidence.
    The event date is copied from a named evidence row (EVENTS[...]["date_from"]) or, where no source states a
    year, from a stated inference rule (weekday check, 990 payee year). Direction text is the analyst's reading,
    tagged [I] where it is inference.
Task `goodstack` (P-FCG-02). Parse the FY2023-FY2025 Form 990 XML of Percent Impact Foundation (EIN 87-3165286,
Goodstack's US partner foundation) and print a year-by-year table: revenue, grants, Part IX lines, Schedule D
Part I, Schedule A public-support test, Schedule I and F grants, officers, contractors, Schedule O text.

No outreach, no logins, no forms. Reads public pages only; every response is cached (--cache-dir) so reruns are
offline without --fetch. Stdlib only, functional style (pure transforms, I/O at the edges). `pdftotext` is used
if present (only to test whether a user guide names the vendor's mail sender); everything else is stdlib.

Usage: python3 scripts/mission_cf_migrations_goodstack.py --cache-dir DIR [--fetch] [--task migrations|goodstack|all]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as m990  # noqa: E402

DATA = m990.DATA
OUT = os.path.join(DATA, "cf-vendor-migrations-2022-2026.csv")
HARVEST = os.path.join(DATA, "form990-contractors-harvest-full.csv")
CFMAP = os.path.join(DATA, "cf-vendor-map-by-ein.csv")
UA = {"User-Agent": "Mozilla/5.0 (compatible; research-client)"}
RETRIEVED = "2026-11-14"
VENDOR_990 = re.compile(r"stellar|foundant|akoya|blackbaud|npact|spectrum|fidtech|microedge|ren\b|renaissance", re.I)

CF = {  # ein -> short name used in this file
    "521055743": "Arkansas Community Foundation",
    "721493023": "Community Foundation of Acadiana",
    "382190667": "Community Foundation of Greater Flint",
    "593001853": "Community Foundation Tampa Bay",
    "566037615": "The Winston-Salem Foundation",
    "850311210": "New Mexico Community Foundation",
    "201729243": "Indian River Community Foundation",
    "200697012": "Yakima Valley Community Foundation",
}

# (evidence_id, ein, kind, url, rule, rule argument). Rules are implemented in `extract`.
EVIDENCE = (
    ("AR-POST", "521055743", "announcement", "https://www.arcf.org/wp-json/wp/v2/posts?slug=arkansas-community-foundation-announces-database-transition", "wp_json", ""),
    ("AR-POST-TEXT", "521055743", "announcement", "https://www.arcf.org/blog/arkansas-community-foundation-announces-database-transition/", "regex", r"Arkansas Community Foundation has transitioned to a new database.{0,200}?emailed on June 1\."),
    ("AR-GUIDE", "521055743", "donor_notice_pdf", "https://www.arcf.org/app/uploads/2026/06/Fundholder-Portal-How-to-Guide3.pdf", "pdf", r"no-reply@fcsuite\.com"),
    ("AR-LEGACY-IPHI", "521055743", "legacy_portal_live", "https://arcf.iphiview.com/arcf/", "regex", r"©\s*20\d\d Arkansas Community Foundation"),
    ("AC-HOME", "721493023", "portal_page", "https://www.cfacadiana.org/wp-json/wp/v2/pages/2?_fields=date,modified,link,content", "wp_json", r"Our new fund portal features enhanced visuals"),
    ("AC-DONORS", "721493023", "portal_page", "https://www.cfacadiana.org/wp-json/wp/v2/pages/429?_fields=date,modified,link,content", "wp_json", r"Donor Portal"),
    ("AC-UPGRADE", "721493023", "announcement_removed", "https://www.cfacadiana.org/upgrade", "http_status", ""),
    ("AC-IPHI-DNS", "721493023", "legacy_portal_dns", "https://dns.google/resolve?name=cfacadiana.iphiview.com&type=A", "dns", ""),
    ("FL-LOGIN", "382190667", "portal_page", "https://www.cfgf.org/who-we-are/login", "jsonld", r"Donor Portal"),
    ("FL-LEGACY-IPHI", "382190667", "legacy_portal_live", "https://cfgf.iphiview.com/cfgf/", "regex", r"we are moving to a new system\..{0,120}"),
    ("FL-GRANT-FAQ", "382190667", "donor_notice_pdf", "https://stdidcfgfprod.blob.core.windows.net/cfgf/documents/CFGF_FAQ_2026.pdf", "pdf", r"transitioned to a new grant application portal"),
    ("TB-GUIDE", "593001853", "announcement", "https://www.cftampabay.org/portal-guide", "regex", r"(transition from our current system, Raiser's Edge, to a new platform powered by Foundant|we have transitioned from our previous system, Raiser's Edge, to a new platform powered by Foundant|access the current portal through June 15|expected to launch in late July)"),
    ("TB-GUIDE-PUB", "593001853", "announcement", "https://www.cftampabay.org/portal-guide", "webflow", ""),
    ("TB-FUNDS", "593001853", "donor_notice", "https://www.cftampabay.org/give-now/cftb-funds", "regex", r"temporarily unavailable during our transition to a new giving portal"),
    ("TB-OLD-PORTAL", "593001853", "legacy_portal_live", "https://cftampabay.spectrumportal.net/", "regex", r"<TITLE>[^<]*</TITLE>|<title[^>]*>[^<]*</title>"),
    ("TB-HOME", "593001853", "portal_page", "https://www.cftampabay.org/", "regex", r"href=\"https://cftampabay\.(spectrumportal\.net|fcsuite\.com)[^\"]*\"[^>]*>[^<]*Fundholder Login"),
    ("WS-PORTAL", "566037615", "announcement", "https://www.wsfoundation.org/portal", "regex", r"(This summer we migrated from Blackbaud to Foundant|August 21\s*:\s*last day to access the current Fund Portal|September 30\s*:\s*New Fund Portal launched)"),
    ("WS-PORTAL-PUB", "566037615", "announcement", "https://www.wsfoundation.org/portal", "webflow", ""),
    ("WS-HOME", "566037615", "portal_page", "https://www.wsfoundation.org/", "regex", r"href=\"https://wsfoundation\.spectrumportal\.net/\"[^>]*>[^<]*"),
    ("WS-OLD-PORTAL", "566037615", "legacy_portal_live", "https://wsfoundation.spectrumportal.net/", "regex", r"<title[^>]*>[^<]*</title>|bbCheckout"),
    ("NM-NMRRF", "850311210", "portal_page", "https://nmcf.org/wp-json/wp/v2/pages?slug=nmrrf", "wp_json", r"pre-approved agency partners to apply for New Mexico Rapid Response Funding"),
    ("NM-LOGIN", "850311210", "portal_page", "https://nmcf.org/wp-json/wp/v2/pages?slug=login", "wp_json", r"pre-approved agency partners to submit applications and reports"),
    ("NM-HOME", "850311210", "portal_page", "https://nmcf.org/", "regex", r"href=\"https://[a-z]+\.(fcsuite\.com|spectrumportal\.net)[^\"]*\""),
    ("IR-UPGRADE", "201729243", "donor_notice", "https://ircommunityfoundation.org/wp-json/wp/v2/pages?slug=my-fund-has-been-upgraded", "wp_json", r"new and improved My Fund"),
    ("IR-UPGRADE-LINK", "201729243", "donor_notice", "https://ircommunityfoundation.org/my-fund-has-been-upgraded/", "regex", r"href=\"https://indianriver\.fcsuite\.com/erp/portal\"[^>]*>Go to My Fund|href=\"https://ircf\.donor-portal\.org/login\">My Fund: Login"),
    ("IR-GUIDE", "201729243", "donor_notice_pdf", "https://ircommunityfoundation.org/wp-content/uploads/2025/03/RESOURCE-My-Fund-User-Guide-1.pdf", "pdf", r"access monthly statements"),
    ("IR-DONORPORTAL-CT", "201729243", "crt_sh", "https://crt.sh/?q=ircf.donor-portal.org&output=json", "crt", ""),
    ("YV-HOME", "200697012", "portal_page", "https://www.yakimavalleycf.org/", "regex", r"href=\"https://(gofund\.akoyago\.com/yakimavalleycf[^\"]*|yvcf\.iphiview\.com[^\"]*)\""),
    ("YV-IPHI-DNS", "200697012", "legacy_portal_dns", "https://dns.google/resolve?name=yvcf.iphiview.com&type=A", "dns", ""),
)

# Event readings. date_from names the evidence row (and field) that carries the date; `rule` is used when no
# source states a year and the date is inferred.
EVENTS = {
    "521055743": {"from": "Ren (Stellar) iPhi", "to": "Foundant CommunitySuite", "direction": "iPhi -> Foundant (complete; legacy arcf.iphiview.com login page still answers)",
                  "date_from": ("AR-GUIDE", "pdf_created"), "date_basis": "Fundholder Portal user guide PDF created 2026-06-01 and names no-reply@fcsuite.com; post (WP date 2026-04-20, modified 2026-08-13) says instructions were 'emailed on June 1'",
                  "confidence": "high", "ren_implication": "Ren iPhi loses a $100m+ statewide CF; last Stellar 990 line TY2022 ($100,555)"},
    "721493023": {"from": "Ren (Stellar) iPhi", "to": "Foundant CommunitySuite (CSuite)", "direction": "iPhi -> Foundant (complete; cfacadiana.iphiview.com no longer resolves)",
                  "date_from": None, "rule": "weekday",
                  "date_basis": "[I] Removed /upgrade page (now HTTP 404), as indexed by a search engine: blackout March 19-April 6, login e-mails 'May 5 - May 9', portal live 'May 14', year not stated. May 5-9 is Monday-Friday only in 2025 among 2024-2026 (computed). The donors page with 'Donor Portal' was created 2025-04-09 (WP API). Stellar was still paid $118,458 in TY2024",
                  "confidence": "medium", "ren_implication": "Ren iPhi loses a CF that paid Stellar $118-124k a year (TY2022-TY2024)"},
    "382190667": {"from": "Ren (Stellar) iPhi", "to": "Foundant CommunitySuite", "direction": "iPhi -> Foundant (in progress or just finished; cfgf.iphiview.com still live with a 'moving to a new system' banner)",
                  "date_from": ("FL-LOGIN", "date_published"), "date_basis": "[I] Earliest dated page linking the fcsuite Donor Portal: cfgf.org login page JSON-LD datePublished 2026-01-20; the 2026 grant FAQ (PDF created 2026-02-25) says CFGF 'has transitioned to a new grant application portal'. Stellar TY2022 $114,605; absent from the TY2023-TY2024 top-contractor lists. Read as: switch around year-end 2025/January 2026",
                  "confidence": "low-medium", "ren_implication": "Ren iPhi loses a $29m-DAF CF; the iPhi tenant still serves a transition banner"},
    "593001853": {"from": "Blackbaud Raiser's Edge ledger + Foundation Cloud portal (spectrumportal.net)", "to": "Foundant CommunitySuite", "direction": "Foundation Cloud portal / Raiser's Edge -> Foundant. Not a Foundation Cloud win: spectrumportal was the outgoing portal",
                  "date_from": None, "rule": "tampa",
                  "date_basis": "[I] portal-guide: old portal 'through June 15', new Fund Advisor Portal 'late July', later text 'This summer, we have transitioned'; year not stated. Read as summer 2026: on 2026-11-14 online gifts to CFTB funds are still 'temporarily unavailable during our transition', cftampabay.spectrumportal.net now returns 'Not Found', and no Foundant payee appears in the FYE-June-2025 990",
                  "confidence": "medium-low", "ren_implication": "No Ren involvement; one Foundation Cloud portal tenant lost to Foundant"},
    "566037615": {"from": "Blackbaud (ledger) + Foundation Cloud portal (spectrumportal.net)", "to": "Foundant CommunitySuite", "direction": "Blackbaud / Foundation Cloud portal -> Foundant. Not a Foundation Cloud win: the homepage 'Fundholders Login' to spectrumportal is a stale link",
                  "date_from": None, "rule": "wsf",
                  "date_basis": "[I] /portal: 'This summer we migrated from Blackbaud to Foundant'; old Fund Portal closed 'August 21'; 'September 30: New Fund Portal launched'; year not stated. TY2024 (calendar 2024) 990 lists Foundant Technologies at $187,344, the first Foundant line, so 2024 is read as the migration year",
                  "confidence": "medium", "ren_implication": "No Ren involvement; one Foundation Cloud portal tenant lost to Foundant"},
    "850311210": {"from": "n/a", "to": "n/a", "direction": "No fund-login migration: spectrumportal.net (Foundation Cloud) is a partner/grantee portal (NMRRF applications, grant reports); fcsuite is used only for online donations. The map's 'dual fund login' flag is a misclassification",
                  "date_from": ("NM-NMRRF", "wp_date"), "date_basis": "NMRRF Login page created 2026-06-05; Login page (partner login) created 2026-05-14 (WP API). No fundholder login found on nmcf.org",
                  "confidence": "high (for the reclassification)", "ren_implication": "None; Foundation Cloud use here is grants-side"},
    "201729243": {"from": "donor-portal.org white-label portal", "to": "Foundant CommunitySuite ('My Fund')", "direction": "donor-portal.org -> Foundant; the header 'My Fund: Login' to ircf.donor-portal.org is a leftover link",
                  "date_from": ("IR-UPGRADE", "wp_date"), "date_basis": "'My Fund has been Upgraded!' page created 2023-07-31 (WP API), linking indianriver.fcsuite.com/erp/portal; user guide re-issued March 2025 (PDF created 2025-03-18, adds monthly statements). ircf.donor-portal.org had named certificates 2021-02-08 to 2022-01-04 (crt.sh)",
                  "confidence": "high", "ren_implication": "None; a donor-portal.org tenant lost to Foundant"},
    "200697012": {"from": "Ren (Stellar) iPhi", "to": "akoyaGO (GOfund / GOdonate)", "direction": "iPhi -> akoyaGO (complete; the homepage still links a yvcf.iphiview.com give page, which no longer resolves)",
                  "date_from": None, "rule": "undated",
                  "date_basis": "No dated announcement found; no vendor appears in the TY2022-TY2024 990 top-contractor lists; certificate logs carry no named yvcf host. Date not established",
                  "confidence": "none (date)", "ren_implication": "Ren iPhi loses an $18m-DAF CF to akoyaGO"},
}


# ----------------------------------------------------------------------------- I/O edges
def cache_path(cache_dir: str, url: str) -> str:
    return os.path.join(cache_dir, hashlib.sha1(url.encode()).hexdigest()[:20])


def fetch(url: str, cache_dir: str, do_fetch: bool) -> tuple[int, bytes]:
    if "crt.sh" in url:
        return (0, b"")  # disabled 2026-11-15: crt.sh robots.txt disallows all crawlers (see research/mission-2026-11-14/compliance-note-crtsh-robots.md)
    """(HTTP status, body); cached as <hash>.json (status) + <hash>.bin (body). Status 0 = transport failure."""
    p = cache_path(cache_dir, url)
    if os.path.exists(p + ".json"):
        with open(p + ".json") as fh, open(p + ".bin", "rb") as fb:
            return json.load(fh)["status"], fb.read()
    if not do_fetch:
        return -1, b""
    time.sleep(1.0)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
            status, body = r.status, r.read()
    except urllib.error.HTTPError as e:
        status, body = e.code, e.read() or b""
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
        status, body = 0, b""
    os.makedirs(cache_dir, exist_ok=True)
    with open(p + ".json", "w") as fh, open(p + ".bin", "wb") as fb:
        json.dump({"url": url, "status": status, "retrieved": RETRIEVED}, fh)
        fb.write(body)
    return status, body


def pdf_text(body: bytes, cache_dir: str, url: str) -> str:
    exe = shutil.which("pdftotext")
    if not exe or not body.startswith(b"%PDF"):
        return ""
    p = cache_path(cache_dir, url) + ".pdf"
    with open(p, "wb") as fh:
        fh.write(body)
    return subprocess.run([exe, p, "-"], capture_output=True, text=True, check=False).stdout


# ----------------------------------------------------------------------------- pure transforms
def plain(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).replace("\xa0", " ").strip()


def snippet(text: str, pat: str) -> str:
    hits = tuple(dict.fromkeys(m.group(0)[:240] for m in re.finditer(pat, text, re.I | re.S)))
    return " || ".join(hits[:4])


def pdf_created(body: bytes) -> str:
    m = re.search(rb"/CreationDate\s*\(D:(\d{4})(\d{2})(\d{2})", body) or re.search(rb"<xmp:CreateDate>(\d{4})-(\d{2})-(\d{2})", body)
    return "-".join(x.decode() for x in m.groups()) if m else ""


def extract(ev: Sequence, status: int, body: bytes, text_pdf: str = "") -> dict:
    """Apply the evidence rule to a fetched body -> {field: value}. Pure."""
    _, _, _, url, rule, arg = ev
    raw = body.decode("utf-8", "ignore")
    out = {"http_status": status}
    if rule == "wp_json":
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            return {**out, "note": "not JSON"}
        d = d[0] if isinstance(d, list) and d else d
        if not isinstance(d, dict):
            return {**out, "note": "no WP object"}
        content = plain((d.get("content") or {}).get("rendered", "")) if isinstance(d.get("content"), dict) else ""
        return {**out, "wp_date": (d.get("date") or "")[:10], "wp_modified": (d.get("modified") or "")[:10],
                "page": d.get("link", ""), "snippet": snippet(content, arg) if arg and content else ""}
    if rule == "regex":
        return {**out, "snippet": snippet(raw if arg.startswith(("href", "<")) else plain(raw), arg)}
    if rule == "jsonld":
        pub = re.search(r'"datePublished":"([0-9-]{10})', raw)
        mod = re.search(r'"dateModified":"([0-9-]{10})', raw)
        return {**out, "date_published": pub.group(1) if pub else "", "wp_modified": mod.group(1) if mod else "",
                "snippet": snippet(plain(raw), r".{0,80}" + arg + r".{0,80}")}
    if rule == "webflow":
        m = re.search(r"Last Published:\s*\w{3} (\w{3}) (\d{1,2}) (\d{4})", raw)
        return {**out, "webflow_last_published": dt.datetime.strptime(" ".join(m.groups()), "%b %d %Y").date().isoformat() if m else ""}
    if rule == "pdf":
        return {**out, "pdf_created": pdf_created(body), "snippet": snippet(text_pdf, r".{0,80}" + arg + r".{0,40}") if text_pdf else "(pdftotext unavailable)"}
    if rule == "crt":
        try:
            d = json.loads(raw or "[]")
        except json.JSONDecodeError:
            return {**out, "note": "crt.sh returned non-JSON"}
        nb = sorted(x["not_before"][:10] for x in d)
        na = sorted(x["not_after"][:10] for x in d)
        return {**out, "ct_cert_count": len(d), "ct_first_not_before": nb[0] if nb else "", "ct_last_not_before": nb[-1] if nb else "",
                "ct_last_not_after": na[-1] if na else ""}
    if rule == "dns":
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            return {**out, "note": "dns.google non-JSON"}
        return {**out, "dns_status": {0: "NOERROR", 3: "NXDOMAIN"}.get(d.get("Status"), str(d.get("Status"))),
                "dns_answers": ";".join(a.get("data", "") for a in d.get("Answer", []))}
    if rule == "http_status":
        return out
    return {**out, "note": "unknown rule"}


def evidence_value(x: Mapping) -> str:
    keys = ("wp_date", "wp_modified", "date_published", "webflow_last_published", "pdf_created", "ct_first_not_before",
            "ct_last_not_before", "ct_last_not_after", "ct_cert_count", "dns_status", "dns_answers")
    return "; ".join(f"{k}={x[k]}" for k in keys if x.get(k) not in (None, ""))


def harvest_lines(rows: Sequence[Mapping], ein: str) -> tuple[dict, ...]:
    """990 Part VII-B vendor lines (TY2021+) for one EIN, plus a row per harvested return without one."""
    mine = tuple(r for r in rows if r["ein"] == ein and int(r["tax_year"] or 0) >= 2021)
    vend = tuple(r for r in mine if VENDOR_990.search(r["contractor_name"]))
    tys = sorted({r["tax_year"] for r in mine})
    return tuple({"evidence_id": f"990-{ein}-TY{r['tax_year']}", "kind": "990_part_vii_b", "url": r["filing_page_url"] or r["source_url"],
                  "value": f"TY{r['tax_year']} (period end {r['tax_period_end']})", "snippet": f"{r['contractor_name']} '{r['services']}' ${r['compensation']}"}
                 for r in vend) + tuple({"evidence_id": f"990-{ein}-TY{ty}-none", "kind": "990_part_vii_b", "url": next(r["filing_page_url"] or r["source_url"] for r in mine if r["tax_year"] == ty),
                                         "value": f"TY{ty}", "snippet": "no Stellar/Foundant/akoya/Blackbaud/NPact payee among the listed (> $100k, top-5) contractors"}
                                        for ty in tys if not any(r["tax_year"] == ty for r in vend))


def weekday_years(month: int, d0: int, d1: int, years: Sequence[int]) -> tuple[int, ...]:
    """Years in which month/d0..d1 runs Monday..Friday."""
    return tuple(y for y in years if dt.date(y, month, d0).weekday() == 0 and dt.date(y, month, d1).weekday() == 4)


def event_date(ein: str, spec: Mapping, ev: Mapping) -> str:
    if spec.get("date_from"):
        eid, field = spec["date_from"]
        return (ev.get(eid) or {}).get(field, "")
    rule = spec.get("rule")
    if rule == "weekday":
        ys = weekday_years(5, 5, 9, (2024, 2025, 2026))
        return f"{ys[0]}-05-14" if len(ys) == 1 else ""
    if rule == "wsf":
        return "2024-09-30"  # launch day stated on /portal; year from the TY2024 Foundant 990 line (date_basis)
    if rule == "tampa":
        return "2026-07 (late July, year inferred)"
    return ""


MIG_FIELDS = ("record_type", "ein", "cf_name", "fy2024_daf_assets_usd", "map_signal", "evidence_id", "evidence_kind", "url",
              "http_status", "value", "snippet", "from_system", "to_system", "direction", "event_date", "date_basis",
              "date_confidence", "implication", "evidence_ids", "retrieved")


def migrations(cache_dir: str, do_fetch: bool) -> tuple[dict, ...]:
    cfmap = {r["ein"]: r for r in m990.read_csv(CFMAP)}
    harvest = m990.read_csv(HARVEST)
    fetched = {e[0]: (e, *fetch(e[3], cache_dir, do_fetch)) for e in EVIDENCE}
    ev = {k: extract(e, s, b, pdf_text(b, cache_dir, e[3]) if e[4] == "pdf" else "") for k, (e, s, b) in fetched.items()}
    signal = {"521055743": "stellar_990_payee_foundant_portal", "721493023": "stellar_990_payee_foundant_portal",
              "382190667": "stellar_990_payee_foundant_portal"}
    def base(ein):
        return {"ein": ein, "cf_name": CF[ein], "fy2024_daf_assets_usd": cfmap.get(ein, {}).get("fy2024_daf_assets_usd", ""),
                "map_signal": signal.get(ein, "dual_live_fund_login"), "retrieved": RETRIEVED}
    ev_rows = tuple({**base(e[1]), "record_type": "evidence", "evidence_id": e[0], "evidence_kind": e[2], "url": e[3],
                     "http_status": ev[e[0]].get("http_status"), "value": evidence_value(ev[e[0]]) or ev[e[0]].get("note", ""),
                     "snippet": ev[e[0]].get("snippet", "")} for e in EVIDENCE)
    h_rows = tuple({**base(ein), "record_type": "evidence", "evidence_kind": h["kind"], **{k: h[k] for k in ("evidence_id", "url", "value", "snippet")}}
                   for ein in CF for h in harvest_lines(harvest, ein))
    events = tuple({**base(ein), "record_type": "event", "from_system": s["from"], "to_system": s["to"], "direction": s["direction"],
                    "event_date": event_date(ein, s, ev), "date_basis": s["date_basis"], "date_confidence": s["confidence"],
                    "implication": s["ren_implication"],
                    "evidence_ids": ";".join(r["evidence_id"] for r in ev_rows + h_rows if r["ein"] == ein)} for ein, s in EVENTS.items())
    return events + ev_rows + h_rows


# ----------------------------------------------------------------------------- Goodstack (P-FCG-02)
GOODSTACK = (("FY2023", "202411459349301006"), ("FY2024", "202522489349301512"), ("FY2025", "202602459349300235"))


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def first(root, name: str) -> str:
    el = next((e for e in root.iter() if local(e.tag) == name), None)
    return (el.text or "").strip() if el is not None else ""


def child_text(el, name: str) -> str:
    return first(el, name)


def sched(root, name: str):
    return next((e for e in root.iter() if local(e.tag) == name), None)


def goodstack_return(xml_bytes: bytes) -> dict:
    root = ET.fromstring(xml_bytes)
    f990 = sched(root, "IRS990")
    part9 = {local(e.tag): child_text(e, "TotalAmt") for e in (f990 if f990 is not None else ()) if local(e.tag).endswith("Grp") and first(e, "TotalAmt")}
    si = sched(root, "IRS990ScheduleI")
    recips = tuple((child_text(g, "BusinessNameLine1Txt"), int(child_text(g, "CashGrantAmt") or 0))
                   for g in (si.iter() if si is not None else ()) if local(g.tag) == "RecipientTable")
    sf = sched(root, "IRS990ScheduleF")
    regions = tuple((child_text(g, "RegionTxt"), child_text(g, "RegionTotalExpendituresAmt"))
                    for g in (sf.iter() if sf is not None else ()) if local(g.tag) == "AccountActivitiesOutsideUSGrp")
    so = sched(root, "IRS990ScheduleO")
    so_txt = tuple((child_text(g, "FormAndLineReferenceDesc"), child_text(g, "ExplanationTxt"))
                   for g in (so.iter() if so is not None else ()) if local(g.tag) == "SupplementalInformationDetail")
    officers = tuple(f"{child_text(g, 'PersonNm')} ({child_text(g, 'TitleTxt')}, {child_text(g, 'AverageHoursPerWeekRt')} h/wk)"
                     for g in root.iter() if local(g.tag) == "Form990PartVIISectionAGrp")
    contractors = tuple(f"{first(g, 'BusinessNameLine1Txt')} '{child_text(g, 'ServicesDesc')}' ${child_text(g, 'CompensationAmt')}"
                        for g in root.iter() if local(g.tag) == "ContractorCompensationGrp")
    sd = sched(root, "IRS990ScheduleD")
    schedules = tuple(local(e.tag) for e in root.iter() if local(e.tag).startswith("IRS990"))
    return {"return_ts": first(root, "ReturnTs")[:10], "tax_period_end": first(root, "TaxPeriodEndDt"), "name": first(sched(root, "Filer"), "BusinessNameLine1Txt"),
            "website": first(root, "WebsiteAddressTxt"), "schedules": ",".join(dict.fromkeys(schedules)),
            "contributions": first(root, "CYContributionsGrantsAmt"), "total_revenue": first(root, "CYTotalRevenueAmt"),
            "grants_paid": first(root, "CYGrantsAndSimilarPaidAmt"), "total_expenses": first(root, "CYTotalExpensesAmt"),
            "total_assets_eoy": first(root, "TotalAssetsEOYAmt"), "total_liabilities_eoy": first(root, "TotalLiabilitiesEOYAmt"),
            "net_assets_eoy": first(root, "NetAssetsOrFundBalancesEOYAmt"), "employees": first(root, "TotalEmployeeCnt"),
            "part_ix_lines": part9,
            "sched_d_daf_count": child_text(sd, "DonorAdvisedFundsHeldCnt") if sd is not None else "",
            "sched_d_daf_contributions": child_text(sd, "DonorAdvisedFundsContriAmt") if sd is not None else "",
            "sched_d_daf_grants": child_text(sd, "DonorAdvisedFundsGrantsAmt") if sd is not None else "",
            "sched_d_daf_eoy": child_text(sd, "DonorAdvisedFundsVlEOYAmt") if sd is not None else "",
            "substantial_contributors_total": first(root, "SubstantialContributorsTotAmt"), "public_support_total": first(root, "PublicSupportTotal170Amt"),
            "total_support": first(root, "TotalSupportAmt"),
            "sched_i_recipients": len(recips), "sched_i_total": sum(a for _, a in recips),
            "sched_i_top": sorted(recips, key=lambda x: -x[1])[:8], "sched_f_regions": regions,
            "officers": officers, "contractors": contractors,
            "sched_o": so_txt}


def goodstack(cache_dir: str, do_fetch: bool) -> tuple[tuple[str, str, dict], ...]:
    def get(oid):
        s, b = fetch(m990.XML_URL.format(oid=oid), cache_dir, do_fetch)
        return goodstack_return(b) if s == 200 and b else {"error": f"http {s}"}
    return tuple((fy, oid, get(oid)) for fy, oid in GOODSTACK)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--task", default="all", choices=("migrations", "goodstack", "all"))
    a = ap.parse_args(argv)
    if a.task in ("migrations", "all"):
        rows = migrations(a.cache_dir, a.fetch)
        m990.write_csv(OUT, rows, MIG_FIELDS)
        print(f"wrote {OUT}: {sum(r['record_type'] == 'event' for r in rows)} events, {sum(r['record_type'] == 'evidence' for r in rows)} evidence rows")
        for r in rows:
            if r["record_type"] == "event":
                print(f"  {r['cf_name'][:38]:38} | {r['from_system'][:30]:30} -> {r['to_system'][:28]:28} | {r['event_date']} ({r['date_confidence']})")
        print("  weekday check: May 5 (Mon) - May 9 (Fri) falls in", weekday_years(5, 5, 9, range(2022, 2028)))
    if a.task in ("goodstack", "all"):
        for fy, oid, d in goodstack(a.cache_dir, a.fetch):
            print(f"\n== Percent Impact Foundation {fy} (object {oid}; {m990.XML_URL.format(oid=oid)})")
            print(json.dumps(d, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
