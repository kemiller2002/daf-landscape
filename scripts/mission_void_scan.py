#!/usr/bin/env python3
"""Voided / refunded / rescinded DAF-grant disclosure scan, top-200 DAF sponsors, TY2021-2024 (queue item P-B28-02).

Extends batch 28's top-30 scan (research/mission-2026-11-14/queue-batch28-ledgers-voids-cf-apps.md §3) to the
200 largest DAFRC sponsors by FY2024 DAF assets (DAFRC as published, with the R1 'filed replaces imputed'
corrections in dafrc-corrections-itemized.csv applied). Stdlib only, functional style (pure transforms; I/O at
the edges). Reuses the IRS index loader and XML helpers from scripts/mission_990_contractors.py.

Sources
  * Sponsor universe: data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv (+ dafrc-corrections-itemized.csv)
  * Return locator:   IRS TEOS e-file index index_2021..2026.csv (https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv)
  * Return content:   https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml

What is scanned in each Form 990 (whole document, streamed; Schedule I recipient tables are discarded as parsed)
  * every SupplementalInformationDetail (FormAndLineReferenceDesc + ExplanationTxt) in any schedule
    (Schedule O carries the Part XI line 9 and Part XII explanations; Schedule D Part XIII carries Part XI-XII
    reconciliation explanations);
  * Form 990 Part I line 13 CYGrantsAndSimilarPaidAmt (denominator), Part XI line 9 OtherChangesInNetAssetsAmt,
    Schedule D Part I DonorAdvisedFundsGrantsAmt (context).
A hit is a match of VOID_RX in an explanation. The item amount is read from the same line item, using the two
filed layouts '$ AMOUNT - LABEL' and 'LABEL [-] AMOUNT'; IRS redaction 'XXX-XX-XXXX' is reported as REDACTED.
Hits are then classed as grant-related (label mentions a grant/scholarship/award, or is a voided/uncashed-check
item) or not (e.g. 'excise tax refund'); MANUAL_REVIEW below records the reviewer's decision for every
grant-related hit whose automatic class or amount needs overriding (empty in the 2026-11-15 run: all 128 hits
were reviewed against the filed text and none needed an override; 19 policy/descriptive hits with no figure are
classed automatically).

Usage
  python3 scripts/mission_void_scan.py --irs-dir DIR --cache-dir CACHE [--fetch] [--n 200] [--workers 4]
Outputs
  data/mission-2026-11-14/daf-grant-voids-top200.csv          one row per hit, plus one 'none found' row per return
  data/mission-2026-11-14/daf-grant-voids-top200-summary.csv  disclosure rate and void-share distribution by type
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import (DATA, XML_URL, ein9, ensure_indexes, fmt, latest_per_period,  # noqa: E402
                                     load_index, local, num, read_csv, write_csv)

DAFRC_CSV = os.path.join(DATA, "dafrc-sponsor-schedule-d-fy2019-2024.csv")
CORR_CSV = os.path.join(DATA, "dafrc-corrections-itemized.csv")
OUT_CSV = os.path.join(DATA, "daf-grant-voids-top200.csv")
SUMMARY_CSV = os.path.join(DATA, "daf-grant-voids-top200-summary.csv")
TOP30_CSV = os.path.join(DATA, "daf-grant-voids-disclosures.csv")
TAX_YEARS = (2021, 2022, 2023, 2024)
EXTRACT_VERSION = "voids-1"
RETRIEVED = "2026-11-15"

VOID_RX = re.compile(
    r"(\bvoid(ed|s)?\b|refund(ed|s)?\b[^.;]{0,40}\b(grant|scholarship|award)|\b(grant|scholarship|award)s?\b[^.;]{0,30}\brefund"
    r"|returned\s+(grant|scholarship|award)|grants?\s+returned|return(ed|s)?\s+of\s+(prior[\s-]+years?'?\s+)?grant|\bgrants?\b[^.;]{0,20}\bcancel"
    r"|cancel+(ed|ation)s?\s+(of\s+)?(prior[\s-]+years?'?\s+)?grant|uncashed|rescind|rescission|escheat|unclaimed\s+(grant|check)"
    r"|outstanding\s+checks?|stale[\s-]?dated|grants?\s+(written\s+off|reversed)|revers(al|ed)\s+of\s+(prior[\s-]+years?'?\s+)?grant)",
    re.I)
GRANT_WORD = re.compile(r"grant|scholarship|award|distribut|\bvoid|uncashed|stale|outstanding\s+check|escheat", re.I)
NOT_GRANT = re.compile(r"excise\s+tax|tax\s+refund|refund\s+of\s+(federal|excise|tax)|insurance|lease|rent\b|tuition|event|ticket", re.I)
YEAR_RX = re.compile(r"^(19|20)\d\d$")

# Reviewer decisions for hits whose automatic class or amount was checked against the filed text.
# key: (object_id, matched label fragment, lower-case) -> {"grant_related": yes/no, "amount": str|None, "note": str}
MANUAL_REVIEW: dict[tuple[str, str], dict] = {}


# ----------------------------------------------------------------------------- universe
def corrected_fy2024(dafrc: Sequence[Mapping], corr: Sequence[Mapping]) -> tuple[dict, ...]:
    """FY2024 DAFRC rows with R1 corrections (filed replaces imputed) applied to assets and accounts. Pure."""
    fix = {(c["ein"].zfill(9), c["metric"]): c["corrected_value"] for c in corr
           if c["fiscal_year"] == "2024" and c.get("applied") == "1"}
    return tuple({**r, "ein": ein9(r["ein"]),
                  "assets_corr": num(fix.get((ein9(r["ein"]), "daf_assets_eoy"), r["eoy_daf_assets"])) or 0.0,
                  "accounts_corr": num(fix.get((ein9(r["ein"]), "daf_accounts_eoy"), r["number_of_daf_accounts"]))}
                 for r in dafrc if r["fiscal_year_end"] == "2024")


def top_n(rows: Sequence[Mapping], n: int) -> tuple[dict, ...]:
    ranked = sorted(rows, key=lambda r: -r["assets_corr"])[:n]
    return tuple({**r, "rank": i + 1} for i, r in enumerate(ranked))


def tax_year_of(tax_period: str) -> int:
    """IRS tax year = calendar year in which a 12-month period begins (period ending Dec -> same year)."""
    y, m = int(tax_period[:4]), int(tax_period[4:6])
    return y if m == 12 else y - 1


def returns_for(filings: Sequence[Mapping]) -> tuple[dict, ...]:
    latest = latest_per_period(filings, tuple(range(2021, 2027)), ("990",))
    return tuple({**f, "tax_year": tax_year_of(f["tax_period"])} for f in latest
                 if tax_year_of(f["tax_period"]) in TAX_YEARS)


# ----------------------------------------------------------------------------- XML extract
def extract_stream(stream) -> dict:
    """Whole-document stream parse keeping header, three amounts and every supplemental explanation."""
    out = {"supp": [], "tax_year": "", "tax_period_end": "", "filer_name": "", "amended": "",
           "grants_part_i": None, "part_xi_l9": None, "sched_d_daf_grants": None}
    sched = "IRS990"
    for event, el in ET.iterparse(stream, events=("start", "end")):
        tag = local(el.tag)
        if event == "start":
            if tag.startswith("IRS990"):
                sched = tag
            continue
        if tag == "TaxYr":
            out["tax_year"] = (el.text or "").strip()
        elif tag == "TaxPeriodEndDt":
            out["tax_period_end"] = (el.text or "").strip()
        elif tag == "BusinessNameLine1Txt" and not out["filer_name"]:
            out["filer_name"] = (el.text or "").strip()
        elif tag == "AmendedReturnInd":
            out["amended"] = (el.text or "").strip()
        elif tag == "CYGrantsAndSimilarPaidAmt" and sched == "IRS990":
            out["grants_part_i"] = num(el.text)
        elif tag == "OtherChangesInNetAssetsAmt" and sched == "IRS990":
            out["part_xi_l9"] = num(el.text)
        elif tag == "DonorAdvisedFundsGrantsAmt":
            out["sched_d_daf_grants"] = num(el.text)
        elif tag == "SupplementalInformationDetail":
            ref = next(((c.text or "").strip() for c in el if local(c.tag) == "FormAndLineReferenceDesc"), "")
            txt = next(((c.text or "").strip() for c in el if local(c.tag) == "ExplanationTxt"), "")
            if VOID_RX.search(txt) or VOID_RX.search(ref):
                out["supp"].append({"schedule": sched, "ref": ref, "text": txt})
            el.clear()
        elif tag in ("RecipientTable", "GrantsOtherAsstToIndivInUSGrp", "ForeignGrantsGrp", "SupplementalInformationDetail"):
            el.clear()
        elif tag.startswith("IRS990Schedule"):
            el.clear()
            sched = "IRS990"
    return out


def fetch_extract(oid: str, cache_dir: str, xml_dir: str | None, fetch: bool, retries: int = 3) -> dict:
    path = os.path.join(cache_dir, "voidscan", f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            cached = json.load(fh)
        if cached.get("_v") == EXTRACT_VERSION:
            return cached
    local_xml = os.path.join(xml_dir, f"{oid}.xml") if xml_dir else ""
    out = {"xml_status": "not_fetched"}
    if local_xml and os.path.exists(local_xml):
        with open(local_xml, "rb") as fh:
            out = {**extract_stream(fh), "xml_status": "ok (local copy)"}
    elif fetch:
        req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    out = {**extract_stream(resp), "xml_status": "ok"}
                break
            except urllib.error.HTTPError as e:
                out = {"xml_status": f"http_{e.code}"}
                if e.code in (403, 404):
                    break
            except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
                out = {"xml_status": f"error:{type(e).__name__}"}
                time.sleep(3 * (attempt + 1))
        time.sleep(0.25)
    result = {**out, "_v": EXTRACT_VERSION}
    if not result["xml_status"].startswith(("error", "not_fetched")):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(result, fh)
    return result


# ----------------------------------------------------------------------------- hit parsing (pure)
def money_value(tok: str) -> float | None:
    if tok.startswith("XXX"):
        return None
    neg = tok.strip().startswith(("(", "-"))
    digits = re.sub(r"[^\d.]", "", tok)
    if not digits or YEAR_RX.match(digits):
        return None
    v = float(digits)
    return -v if neg else v


AMT = r"(X{3}-X{2}-X{4}|\(?\$?\s?\(?-?\d{1,3}(?:,\d{3})+(?:\.\d+)?\)?|\(?\$?\s?\(?-?\d{4,}(?:\.\d+)?\)?)"
BEFORE_RX = re.compile(r"\$\s?" + AMT + r"\s+-\s+[A-Za-z ,'/&-]{0,60}$")   # '$ 16,130,006 - ADJUSTMENT FOR ...'
AFTER_RX = re.compile(r"[^\d;.]{0,70}?" + AMT)                                  # 'GRANT REFUNDS 521,014.'


def token_amount(tok: str) -> tuple[str, str]:
    if tok.startswith("XXX"):
        return "REDACTED", "redacted"
    v = money_value(tok.replace("$", "").replace(" ", ""))
    return (fmt(v), "parsed") if v is not None and abs(v) >= 1000 else ("", "no amount in item")


def nearest_amount(text: str, start: int, end: int) -> tuple[str, str]:
    """Amount of the line item containing [start, end). Two filed layouts are recognised: '$ AMOUNT - LABEL'
    (amount before the label) and 'LABEL [-] AMOUNT' (amount after the label, before the next '.' or ';'). Pure."""
    lab_start = max(text.rfind(";", 0, start), text.rfind(". ", 0, start), text.rfind("_", 0, start), -1) + 1
    mb = BEFORE_RX.search(text[max(0, lab_start - 40):start])
    if mb:
        return token_amount(mb.group(1))
    ma = AFTER_RX.match(text, end)
    if ma:
        return token_amount(ma.group(1))
    return "", "no amount in item"


def label_of(text: str, start: int, end: int) -> str:
    lo = max(0, text.rfind("\n", 0, start) + 1, start - 90)
    hi = min(len(text), end + 90)
    return " ".join(text[lo:hi].split())


def item_class(term: str) -> str:
    """Coarse class of the filed label: what kind of event the reconciling item records. Pure."""
    t = term.lower()
    if re.search(r"void|uncashed|stale|outstanding|escheat|unclaimed", t):
        return "voided grant or uncashed check"
    if re.search(r"revers", t):
        return "reversal of grant expense (accrual)"
    if re.search(r"rescind|rescission|cancel", t):
        return "rescinded/cancelled grant"
    return "refunded/returned grant"


def hits_from(supp: Sequence[Mapping]) -> tuple[dict, ...]:
    def one(item):
        txt = item["text"]
        for m in VOID_RX.finditer(txt):
            amt, status = nearest_amount(txt, m.start(), m.end())
            lab = label_of(txt, m.start(), m.end())
            related = "yes" if GRANT_WORD.search(lab) and not NOT_GRANT.search(lab) else "no"
            if status == "no amount in item":
                related = "no (descriptive or policy text; no figure)"
            yield {"item_class": item_class(m.group(0)),"schedule": item["schedule"], "line_reference": item["ref"], "matched_term": m.group(0),
                   "label_snippet": lab, "amount_usd_auto": amt, "amount_status": status, "grant_related": related}
    seen, out = set(), []
    for h in (h for it in supp for h in one(it)):
        key = (h["line_reference"], h["matched_term"].lower(), h["amount_usd_auto"])
        if key not in seen:
            seen.add(key)
            out.append(h)
    return tuple(out)


def apply_review(oid: str, h: Mapping) -> dict:
    rv = next((v for (o, frag), v in MANUAL_REVIEW.items() if o == oid and frag in h["label_snippet"].lower()), None)
    if not rv:
        return {**h, "amount_usd": h["amount_usd_auto"], "review": "automatic"}
    return {**h, "grant_related": rv.get("grant_related", h["grant_related"]),
            "amount_usd": rv.get("amount", h["amount_usd_auto"]) or "", "review": "manual: " + rv.get("note", "")}


def sponsor_type(r: Mapping) -> str:
    return {"National": "national", "Community Foundation": "community foundation",
            "Single Issue Charity": "single-issue charity"}.get(r["type"], r["type"].lower())


def rows_for(sponsor: Mapping, ret: Mapping, ex: Mapping, top30: frozenset) -> tuple[dict, ...]:
    oid = ret["object_id"]
    base = {"sponsor": sponsor["name"], "ein": sponsor["ein"], "sponsor_type": sponsor_type(sponsor),
            "dafrc_subtype": sponsor["subtype"], "fy2024_rank": sponsor["rank"],
            "fy2024_daf_assets_corrected": fmt(sponsor["assets_corr"]), "tax_year": ex.get("tax_year") or ret["tax_year"],
            "tax_period_end": ex.get("tax_period_end", ""), "object_id": oid, "xml_status": ex.get("xml_status", ""),
            "grants_paid_part_i_line13_usd": fmt(ex.get("grants_part_i")),
            "part_xi_line9_other_changes_usd": fmt(ex.get("part_xi_l9")),
            "sched_d_daf_grants_usd": fmt(ex.get("sched_d_daf_grants")),
            "in_batch28_top30_scan": "yes" if sponsor["ein"] in top30 else "no",
            "source_url": XML_URL.format(oid=oid), "retrieved": RETRIEVED}
    hits = tuple(apply_review(oid, h) for h in hits_from(ex.get("supp", ())))
    if not hits:
        return ({**base, "hit_id": "", "schedule": "", "line_reference": "", "matched_term": "", "item_class": "",
                 "label_snippet": "none found" if ex.get("xml_status", "").startswith("ok") else "not scanned",
                 "amount_usd_auto": "", "amount_status": "", "amount_usd": "", "grant_related": "",
                 "pct_of_part_i_grants": "", "review": ""},)
    g = ex.get("grants_part_i") or 0

    def pct(a):
        v = num(a)
        return f"{abs(v) / g * 100:.3f}" if v is not None and g else ""
    return tuple({**base, **h, "hit_id": f"{oid}-{i + 1}", "pct_of_part_i_grants": pct(h["amount_usd"])}
                 for i, h in enumerate(hits))


# ----------------------------------------------------------------------------- summary (pure)
def return_void_share(rows: Sequence[Mapping]) -> float | None:
    """Void share of one return (%): distinct |amount| of grant-related parsed items / Part I line 13 grants.
    Items are taken from Schedule O (the Part XI line 9 explanation) where it has any; otherwise from Schedule D,
    so the same item reported in both places is counted once."""
    ok = [r for r in rows if r["grant_related"] == "yes" and num(r["amount_usd"]) is not None]
    sched_o = [r for r in ok if r["schedule"] == "IRS990ScheduleO"]
    vals = {abs(num(r["amount_usd"])) for r in (sched_o or ok)}
    g = num(rows[0]["grants_paid_part_i_line13_usd"])
    return sum(vals) / g * 100 if vals and g else None


def dist(xs: Sequence[float]) -> dict:
    xs = sorted(xs)
    if not xs:
        return {"n": 0, "min": "", "p25": "", "median": "", "p75": "", "max": ""}
    q = statistics.quantiles(xs, n=4, method="inclusive") if len(xs) > 1 else [xs[0]] * 3
    return {"n": len(xs), "min": f"{xs[0]:.3f}", "p25": f"{q[0]:.3f}", "median": f"{q[1]:.3f}",
            "p75": f"{q[2]:.3f}", "max": f"{xs[-1]:.3f}"}


def summarise(rows: Sequence[Mapping], sponsors: Sequence[Mapping]) -> tuple[dict, ...]:
    """Both item scopes: every grant-related item, and the same excluding accrual reversals of grant expense
    (which record cancelled commitments, not money returned or checks voided)."""
    excl = tuple({**r, "grant_related": "no (accrual reversal excluded)"}
                 if r.get("item_class") == "reversal of grant expense (accrual)" else r for r in rows)
    return tuple({"item_scope": scope, **g} for scope, rs in (("all grant-related items", rows),
                                                             ("excluding accrual reversals", excl))
                 for g in summarise_scope(rs, sponsors))


def summarise_scope(rows: Sequence[Mapping], sponsors: Sequence[Mapping]) -> tuple[dict, ...]:
    by_ret: dict[str, list] = {}
    for r in rows:
        by_ret.setdefault(r["object_id"], []).append(r)
    scanned = {o: v for o, v in by_ret.items() if v[0]["xml_status"].startswith("ok")}
    disc_ret = {o for o, v in scanned.items()
                if any(r["grant_related"] == "yes" and r["amount_status"] in ("parsed", "redacted") for r in v)}
    out = []
    for label, pred in (("all", lambda t: True), ("national", lambda t: t == "national"),
                        ("community foundation", lambda t: t == "community foundation"),
                        ("single-issue charity", lambda t: t == "single-issue charity")):
        sp = [s for s in sponsors if pred(sponsor_type(s))]
        eins = {s["ein"] for s in sp}
        rets = {o: v for o, v in scanned.items() if v[0]["ein"] in eins}
        sp_scanned = {v[0]["ein"] for v in rets.values()}
        sp_disc = {v[0]["ein"] for o, v in rets.items() if o in disc_ret}
        shares = [s for o, v in rets.items() if o in disc_ret for s in (return_void_share(v),) if s is not None]
        assets_disc = sum(s["assets_corr"] for s in sp if s["ein"] in sp_disc)
        assets_all = sum(s["assets_corr"] for s in sp if s["ein"] in sp_scanned)
        d = dist(shares)
        out.append({"group": label, "sponsors_in_top_n": len(sp), "sponsors_with_scanned_return": len(sp_scanned),
                    "returns_scanned": len(rets), "sponsors_disclosing": len(sp_disc),
                    "sponsor_disclosure_rate_pct": f"{len(sp_disc) / len(sp_scanned) * 100:.1f}" if sp_scanned else "",
                    "returns_disclosing": sum(1 for o in rets if o in disc_ret),
                    "return_disclosure_rate_pct": f"{sum(1 for o in rets if o in disc_ret) / len(rets) * 100:.1f}" if rets else "",
                    "daf_assets_share_disclosing_pct": f"{assets_disc / assets_all * 100:.1f}" if assets_all else "",
                    **{f"void_share_{k}": v for k, v in d.items()}})
    return tuple(out)


FIELDS = ("hit_id", "sponsor", "ein", "sponsor_type", "dafrc_subtype", "fy2024_rank", "fy2024_daf_assets_corrected",
          "tax_year", "tax_period_end", "object_id", "xml_status", "schedule", "line_reference", "matched_term", "item_class",
          "label_snippet", "amount_usd_auto", "amount_status", "amount_usd", "grant_related", "review",
          "grants_paid_part_i_line13_usd", "pct_of_part_i_grants", "part_xi_line9_other_changes_usd",
          "sched_d_daf_grants_usd", "in_batch28_top30_scan", "source_url", "retrieved")
SUMMARY_FIELDS = ("item_scope", "group", "sponsors_in_top_n", "sponsors_with_scanned_return", "returns_scanned", "sponsors_disclosing",
                  "sponsor_disclosure_rate_pct", "returns_disclosing", "return_disclosure_rate_pct",
                  "daf_assets_share_disclosing_pct", "void_share_n", "void_share_min", "void_share_p25",
                  "void_share_median", "void_share_p75", "void_share_max")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--xml-dir", default=None, help="optional dir of raw XML named {OBJECT_ID}.xml, used before fetching")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--review-json", default=None, help="optional JSON list of reviewer decisions (see MANUAL_REVIEW)")
    a = ap.parse_args(argv)
    if a.review_json:
        MANUAL_REVIEW.update({(d["object_id"], d["fragment"].lower()): d for d in json.load(open(a.review_json))})
    sponsors = top_n(corrected_fy2024(read_csv(DAFRC_CSV), read_csv(CORR_CSV)), a.n)
    index = load_index(ensure_indexes(a.irs_dir, a.fetch), frozenset(s["ein"] for s in sponsors))
    plan = tuple((s, r) for s in sponsors for r in returns_for(index.get(s["ein"], ())))
    print(f"{len(sponsors)} sponsors, {len(plan)} returns", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        extracts = tuple(ex.map(lambda p: fetch_extract(p[1]["object_id"], a.cache_dir, a.xml_dir, a.fetch), plan))
    top30 = frozenset(ein9(r["ein"]) for r in read_csv(TOP30_CSV))
    rows = tuple(row for (s, r), e in zip(plan, extracts) for row in rows_for(s, r, e, top30))
    no_return = tuple({"sponsor": s["name"], "ein": s["ein"], "sponsor_type": sponsor_type(s), "dafrc_subtype": s["subtype"],
                       "fy2024_rank": s["rank"], "fy2024_daf_assets_corrected": fmt(s["assets_corr"]),
                       "label_snippet": "no TY2021-24 Form 990 e-file in IRS index 2021-2026", "retrieved": RETRIEVED}
                      for s in sponsors if not returns_for(index.get(s["ein"], ())))
    write_csv(OUT_CSV, rows + no_return, FIELDS)
    write_csv(SUMMARY_CSV, summarise(rows, sponsors), SUMMARY_FIELDS)
    print(f"wrote {OUT_CSV} ({len(rows) + len(no_return)} rows) and {SUMMARY_CSV}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
