#!/usr/bin/env python3
"""Queue batch 37 B: filing questions (stdlib only, functional style: pure transforms, I/O at the edges).

Queue items (data/mission-2026-11-14/research-priority-queue.csv):
  P-99F-03   sponsors that answer Form 990 Part IV line 6 'No' (or file a 990-EZ) yet hold donor-advised funds.
             Universe: EO BMF section 501(c)(3) organisations with NTEE T30/T31/T70, or a DAF-like name, that are NOT in
             the DAFRC panel and filed a 990 or 990-EZ for FY2022+ (TY2021+). The newest return per EIN is read in
             full and screened for (a) Schedule D Part I DAF values, (b) DAF-holding language anywhere in the return.
             -> data/mission-2026-11-14/line6-no-daf-holders.csv                                         (task line6)
  P-99F-01   the FY2024 DAFRC imputed sponsor-years left unresolved by dafrc-corrections-itemized.csv (applied = 0),
             re-tested against the 2026 harvest fill, the full harvest and every FY2024 return in index_2021..2026
             -> data/mission-2026-11-14/dafrc-imputation-resolution-fy2024.csv                           (task dafrc)
  P-STF-03 / P-GPT-03 / P-B33A-03 / P-QA3-06
             full-text reads of named returns (Schedule O, Schedule D Parts XI-XIII, Part VIII lines 3/4/7, Part XI
             line 5) and pattern greps of locally saved audited statements / annual reports (pdftotext output)
             -> JSON summary printed to stdout; figures quoted in the batch-37 note                 (tasks texts, docs)

Sources
  * IRS EO BMF eo1..eo4.csv (https://www.irs.gov/pub/irs-soi/eo{1..4}.csv)
  * IRS TEOS index https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv (2021-2026)
  * IRS e-file XML, GivingTuesday mirror https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OID}_public.xml
    (falls back to the 2026 TEOS zips through mission_batch35_screens.teos_fetch for unmirrored 2026 returns)
  * Repo: dafrc-sponsor-schedule-d-fy2019-2024.csv, dafrc-corrections-itemized.csv, form990-harvest-2026-fill.csv,
    form990-returns-schedule-d-harvest-full.csv, non-dafrc-daf-filers-990.csv

Usage
  python3 scripts/mission_batch37_filings.py line6 --irs-dir IRS --work-dir WORK [--fetch]
  python3 scripts/mission_batch37_filings.py dafrc --irs-dir IRS --work-dir WORK [--fetch]
  python3 scripts/mission_batch37_filings.py texts --irs-dir IRS --work-dir WORK [--fetch]
  python3 scripts/mission_batch37_filings.py docs  --doc-dir DOCS
  IRS holds eo1..eo4.csv and index_2021..2026.csv. WORK receives l6/ (JSON extracts) and teos/ + zipcd/ (zip reads).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DATA, NS, XML_URL, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_batch35_screens import teos_fetch  # noqa: E402

TEOS_LOCK = threading.Lock()
UA = {"User-Agent": "research-script/1.0 (stdlib urllib)"}
WORKERS = int(os.environ.get("MISSION990_WORKERS", "16"))
L6_VERSION = 1
INDEX_YEARS = tuple(range(2021, 2027))
MIN_FY = 2022                       # FY2022+ = tax periods ending 2022 or later (TY2021+)
NTEE_CODES = ("T30", "T31", "T70")  # public foundations, community foundations, federated giving
NAME_SIGNAL = re.compile(r"DONOR[- ]ADVISED|GIFT FUND|GIVING FUND|CHARITABLE FUND|\bDAF\b", re.I)
OUT = {"line6": "line6-no-daf-holders.csv", "dafrc": "dafrc-imputation-resolution-fy2024.csv"}

DAF_MENTION = re.compile(r"donor[- ]advised|\bDAFs?\b", re.I)
# Language that says the filer itself holds / runs DAFs (checked on the sentence around a mention)
HOLD_PATTERNS = tuple(re.compile(p, re.I) for p in (
    r"\b(establish|creat|open|manag|administ|maintain|hold|held|offer|sponsor|host|provid)\w*\b[^.;]{0,80}donor[- ]advised",
    r"donor[- ]advised funds?\b[^.;]{0,60}\b(held|maintained|established|administered|managed|hosted|created|opened)\b",
    r"donor[- ]advised funds?\b[^.;]{0,40}\b(at|of|with|within) (the|our|this) (foundation|organization|fund|corporation|trust)",
    r"\b\d[\d,]*\s+donor[- ]advised funds?\b",
    r"\b(our|its|the foundation'?s?|the organization'?s?)\s+donor[- ]advised",
    r"donor[- ]advised funds?\s*(\(|-)?\s*(program|holders?|account holders?|fund holders?|component)",
    r"(types?|kinds?|categories) of funds?[^.;]{0,120}donor[- ]advised",
    r"donor[- ]advised[^.;]{0,40}(designated|field[- ]of[- ]interest|scholarship|agency|unrestricted) funds?",
    r"(designated|field[- ]of[- ]interest|scholarship|agency|unrestricted)[^.;]{0,40}donor[- ]advised",
))
# Language that only describes money received from, or paid to, someone else's DAF
RECEIPT_PATTERNS = tuple(re.compile(p, re.I) for p in (
    r"\b(from|through|via|by)\s+(a|an|the|their|his|her|donors'?|various)?\s*(donor[- ]advised|DAF)",
    r"(grants?|contributions?|gifts?|donations?|distributions?)\s+(received\s+)?(from|through)\s+[^.;]{0,30}(donor[- ]advised|DAF)",
    r"(to|into)\s+(a|the)?\s*donor[- ]advised funds?\s+(at|with|held by)",
))
ID_TAGS = ("ReturnHeader",)
TEXT_SCOPE = re.compile(r"^IRS990(EZ|Schedule[A-Z]+)?$")


# ----------------------------------------------------------------------------- small pure helpers
def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else f"{v:.6g}"
    return str(v)


def fy_of(tax_period: str) -> int:
    return int(tax_period[:4])


def sentence_around(text: str, m: re.Match, width: int = 260) -> str:
    a, b = max(0, m.start() - width), min(len(text), m.end() + width)
    return re.sub(r"\s+", " ", text[a:b]).strip()


def classify_snippet(s: str) -> str:
    hold = any(p.search(s) for p in HOLD_PATTERNS)
    rec = any(p.search(s) for p in RECEIPT_PATTERNS)
    return "hold" if hold and not rec else "hold_and_receipt" if hold else "receipt" if rec else "mention"


# ----------------------------------------------------------------------------- universe (BMF x index)
def load_bmf(irs_dir: str, exclude: frozenset) -> dict[str, dict]:
    def rows(p):
        with open(p, newline="", encoding="latin-1") as fh:
            yield from csv.DictReader(fh)
    keep = (r for i in range(1, 5) for r in rows(os.path.join(irs_dir, f"eo{i}.csv"))
            if r["SUBSECTION"] == "03" and ein9(r["EIN"]) not in exclude
            and (r["NTEE_CD"][:3] in NTEE_CODES or NAME_SIGNAL.search(r["NAME"])))
    return {ein9(r["EIN"]): {"name": r["NAME"], "ntee": r["NTEE_CD"], "state": r["STATE"], "foundation_code": r["FOUNDATION"],
                             "bmf_asset_amt": r["ASSET_AMT"],
                             "universe_basis": "ntee" if r["NTEE_CD"][:3] in NTEE_CODES else "name"} for r in keep}


def load_index_rows(irs_dir: str, eins: frozenset, types=("990", "990EZ")) -> dict[str, tuple[dict, ...]]:
    def rows(y):
        with open(os.path.join(irs_dir, f"index_{y}.csv"), newline="", encoding="latin-1") as fh:
            for d in csv.DictReader(fh):
                if d["RETURN_TYPE"] in types and ein9(d["EIN"]) in eins:
                    yield {"ein": ein9(d["EIN"]), "tax_period": d["TAX_PERIOD"], "return_type": d["RETURN_TYPE"],
                           "object_id": d["OBJECT_ID"], "taxpayer_name": d["TAXPAYER_NAME"], "index_year": y,
                           "batch": d.get("XML_BATCH_ID", "")}
    dedup = {r["object_id"]: r for y in INDEX_YEARS for r in rows(y)}
    out: dict[str, list] = {}
    for r in dedup.values():
        out.setdefault(r["ein"], []).append(r)
    return {e: tuple(sorted(v, key=lambda r: (r["tax_period"], r["object_id"]))) for e, v in out.items()}


def newest_return(filings: Sequence[Mapping]) -> dict | None:
    keep = tuple(f for f in filings if fy_of(f["tax_period"]) >= MIN_FY)
    return max(keep, key=lambda f: (f["tax_period"], f["object_id"])) if keep else None


# ----------------------------------------------------------------------------- full-return extract
def extract_l6(stream) -> dict:
    """Header, return type, Part IV line 6, total assets, Schedule D Part I (both columns) and every text leaf that
    mentions donor-advised funds (with the schedule it sits in and a classified sentence window)."""
    out: dict = {"sched_d_present": 0, "hits": []}
    stack: list[str] = []
    for event, el in ET.iterparse(stream, events=("start", "end")):
        tag = local(el.tag)
        if event == "start":
            stack.append(tag)
            continue
        stack.pop()
        if tag == "ReturnHeader":
            out.update({"tax_period_end": _t(el, "TaxPeriodEndDt"), "return_ts": _t(el, "ReturnTs"),
                        "return_type": _t(el, "ReturnTypeCd"), "filer_ein": _t(el, "Filer/EIN"),
                        "filer_name": _t(el, "Filer/BusinessName/BusinessNameLine1Txt")})
            el.clear()
            continue
        if tag == "DonorAdvisedFundInd" and "IRS990" in stack:
            out["daf_ind_part_iv"] = (el.text or "").strip()
        elif tag == "EOYAmt" and stack and stack[-1] in ("TotalAssetsGrp", "Form990TotalAssetsGrp"):
            out["total_assets_eoy"] = num(el.text or "")
        elif tag in SCHED_D_FIELDS and "IRS990ScheduleD" in stack:
            out[SCHED_D_FIELDS[tag]] = num(el.text or "")
        elif tag == "IRS990ScheduleD":
            out["sched_d_present"] = 1
        elif len(el) == 0 and el.text and len(el.text) > 20 and DAF_MENTION.search(el.text):
            sched = next((s for s in reversed(stack) if TEXT_SCOPE.match(s)), "")
            for m in list(DAF_MENTION.finditer(el.text))[:3]:
                snip = sentence_around(el.text, m)
                out["hits"].append({"where": f"{sched}/{tag}", "kind": classify_snippet(snip), "text": snip[:600]})
        if TEXT_SCOPE.match(tag):
            el.clear()
    out["hits"] = _dedupe_hits(out["hits"])[:25]
    return out


SCHED_D_FIELDS = {"DonorAdvisedFundsHeldCnt": "sd_daf_count", "DonorAdvisedFundsContriAmt": "sd_daf_contributions",
                  "DonorAdvisedFundsGrantsAmt": "sd_daf_grants", "DonorAdvisedFundsVlEOYAmt": "sd_daf_eoy",
                  "FundsAndOtherAccountsHeldCnt": "sd_other_count", "FundsAndOtherAccountsVlEOYAmt": "sd_other_eoy"}


def _t(el, path: str) -> str:
    cur = el
    for p in path.split("/"):
        cur = next((c for c in cur.iter() if local(c.tag) == p), None)
        if cur is None:
            return ""
    return (cur.text or "").strip()


def _dedupe_hits(hits: Sequence[dict]) -> list[dict]:
    seen: dict[str, dict] = {}
    for h in hits:
        seen.setdefault(h["text"][:200], h)
    return list(seen.values())


def fetch_l6(f: Mapping, work_dir: str, fetch: bool, retries: int = 2) -> dict:
    oid = f["object_id"]
    path = os.path.join(work_dir, "l6", f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == L6_VERSION:
            return c
    if not fetch:
        return {"xml_status": "not_fetched", "object_id": oid}
    res = {"xml_status": "error:none"}
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(XML_URL.format(oid=oid), headers=UA), timeout=180) as r:
                res = {**extract_l6(r), "xml_status": "ok", "xml_source": "gt_mirror"}
            break
        except urllib.error.HTTPError as e:
            res = {"xml_status": f"http_{e.code}"}
            if e.code in (403, 404):
                break
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
            res = {"xml_status": f"error:{type(e).__name__}"}
            time.sleep(2 * (attempt + 1))
    if res["xml_status"] == "http_404" and f.get("index_year") == 2026 and f.get("batch"):
        with TEOS_LOCK:                       # zip central-directory cache is shared; one zip read at a time
            try:
                meta = teos_fetch(oid, f["batch"], work_dir)
            except (urllib.error.URLError, OSError, ValueError) as e:
                meta = {"status": f"error:{type(e).__name__}"}
        if meta.get("status") == "ok":
            with open(os.path.join(work_dir, "teos", f"{oid}_public.xml"), "rb") as fh:
                res = {**extract_l6(fh), "xml_status": "ok", "xml_source": "teos_zip"}
    res = {**res, "_v": L6_VERSION, "object_id": oid}
    if not res["xml_status"].startswith("error"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(res, fh)
    return res


def fetch_all(filings: Sequence[Mapping], work_dir: str, fetch: bool) -> dict[str, dict]:
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        res = tuple(ex.map(lambda f: fetch_l6(f, work_dir, fetch), filings))
    return {f["object_id"]: r for f, r in zip(filings, res)}


# ----------------------------------------------------------------------------- P-99F-03 classification
# Manual reading of every A/B/C row (2026-11-15). Verdicts are [I]: the text is quoted in evidence_text.
#   sponsor_likely      the return says the filer itself holds/offers/operates DAFs, or reports Schedule D DAF values
#   sponsor_possible    wording implies the filer runs DAF-type funds but could describe outside funds
#   data_entry_suspect  a Schedule D value that cannot be a DAF count for this filer
#   affiliate_or_related  DAFs are held by an affiliate or a related organisation (Schedule R) named in the return
#   holder_at_other_sponsor  the filer (or its donors) holds a DAF at another sponsor, or refers donors to one
#   grant_or_receipt    a grant paid into, or received from, someone else's DAF
#   name_or_other       the match is a name or unrelated use of "DAF"
REVIEW = {
    "871530516": ("sponsor_likely", "Amended CY2024 return (filed 2026-01-28) adds Schedule D Part I: 12,808 DAFs, $10.08m EOY, $9.69m contributions; line 6 still 'No'. The original CY2024 return and CY2022-23 returns had Part I blank"),
    "352012880": ("data_entry_suspect", "70,085 DAFs with no value, contributions or grants, on $2.2m of total assets"),
    "883801559": ("sponsor_likely", "Part III: 'will serve as a sponsoring organization of donor advised funds' (corporate and employee giving)"),
    "582348181": ("sponsor_likely", "Offers 'DONOR ADVISED FUNDS, SCHOLARSHIP FUNDS'; answered line 6 Yes in FY2020-24 (non-DAFRC file: $0.38m, 5 DAFs FY2021), No in FY2025"),
    "203098434": ("sponsor_likely", "Mission: 'the ability to open Donor Advised Funds in support of the French Christian community'"),
    "464499862": ("sponsor_possible", "Mission: 'facilitating charitable donations through donor advised funds'; does not say whose"),
    "841516244": ("sponsor_possible", "Community foundation describes a pooled fund as an alternative to 'establishing an individual donor-advised fund' with it"),
    "580623603": ("sponsor_possible", "Schedule D Part XIII reconciliation item 'DONOR ADVISED FUNDS -1,187,656' between audit and 990 revenue"),
    "880889841": ("sponsor_likely", "Part III: grantmaking 'through the operation of a donor advised fund that processes charitable contributions made online'"),
    "823036091": ("sponsor_possible", "Part III: 'through grantmaking, programming and donor advised funds'"),
    "843243945": ("sponsor_possible", "990-EZ: 'a 501c3 donor-advised fund that will collect, authenticate and liquidate your wine collection'; $7k of assets"),
    "841547618": ("sponsor_possible", "Schedule I: 'the CCF board approves the purpose statement of donor advised funds' and reviews recommendations against them"),
    "391815260": ("sponsor_possible", "Schedule I: grantee selection 'determined by the community foundation and/or donor advised fund'"),
    "311607501": ("sponsor_possible", "Same Schedule I wording as Whitewater CF (same administrative trustee)"),
    "203395198": ("affiliate_or_related", "Tides Network describes the Tides entities; DAFs sit at Tides Foundation"),
    "540506322": ("affiliate_or_related", "Schedule R related organisation's primary activity: 'Investing and distributing donor advised funds'"),
    "912008707": ("affiliate_or_related", "Supports Seattle Foundation's donor advised funds"),
    "261917492": ("affiliate_or_related", "NCF affiliate; funds held by National Christian Foundation"),
    "203788055": ("holder_at_other_sponsor", "Contributions 'to donor advised funds held by National Christian Foundation'"),
    "300118912": ("holder_at_other_sponsor", "'maintains a Donor Advised Fund, over which it has full authority to make recommendations' (as advisor)"),
    "593383574": ("holder_at_other_sponsor", "Assets transferred to Pinellas Community Foundation; 'manages donor advised funds with the community foundation'"),
    "020482034": ("holder_at_other_sponsor", "Funds 'held by the New Hampshire Charitable Fund and the Rotary Foundation donor advised fund'"),
    "203651144": ("holder_at_other_sponsor", "Grant to funds 'held and managed by Hampton Roads Community Foundation'"),
    "850535172": ("holder_at_other_sponsor", "DAF established with the Hartford Foundation for Public Giving; board acts as advisory committee"),
    "814324857": ("holder_at_other_sponsor", "Schedule I recipient 'Charles Schwab Donor Advised Fund'"),
    "475370542": ("holder_at_other_sponsor", "'Donation to donor advised fund'; recipient 'Cross Timbers Rotary Club DAF'"),
    "475332690": ("holder_at_other_sponsor", "Recipient: the Ray and Dagmar Dolby Fund of Marin Community Foundation (DAF)"),
    "812367982": ("holder_at_other_sponsor", "Grants made through Charityvest"),
    "921391218": ("holder_at_other_sponsor", "Donation to a Schwab Charitable DAF"),
    "863971267": ("holder_at_other_sponsor", "Greater Washington Community Foundation's Birdseed DAF"),
    "440545992": ("grant_or_receipt", "Recipient name of a Greater Kansas City CF DAF"),
    "474959497": ("grant_or_receipt", "Grant to Santa Barbara Foundation 'to establish a donor advised fund'"),
    "200690144": ("grant_or_receipt", "Grant purpose 'donor advised fund and scholarship fund'"),
    "834222626": ("grant_or_receipt", "Grant purpose 'fund new DAF'"),
    "311583883": ("grant_or_receipt", "Grant purpose 'donor advised fund'"),
    "922857918": ("grant_or_receipt", "'We received a donor advised fund' grant"),
    "473162614": ("grant_or_receipt", "Receives grants from individuals and/or DAFs"),
    "520607957": ("grant_or_receipt", "Campaign receipts, incl. DAF gifts"),
    "231600703": ("grant_or_receipt", "Donors could not recommend grants from their DAFs to it while it was a private foundation"),
    "043547092": ("grant_or_receipt", "Grants made indirectly through community foundations and/or DAFs"),
    "472714377": ("name_or_other", "Schedule O line 'PROJECT PITCH IT (DAF)'"),
    "834023550": ("name_or_other", "Scholarship text"),
    "871305438": ("name_or_other", "Organisation name 'The Quick DAF'"),
    "453962008": ("name_or_other", "Grantor name 'Charitable DAF HoldCo'"),
}
VERDICT_ORDER = {"sponsor_likely": 0, "sponsor_possible": 1, "data_entry_suspect": 2, "affiliate_or_related": 3,
                 "holder_at_other_sponsor": 4, "grant_or_receipt": 5, "name_or_other": 6}


def l6_class(f: Mapping, ex: Mapping) -> str:
    ind = (ex.get("daf_ind_part_iv") or "").lower()
    if f["return_type"] == "990EZ":
        return "990EZ"
    return "line6_yes" if ind in ("true", "1") else "line6_no" if ind in ("false", "0") else "line6_blank"


def evidence(ex: Mapping) -> tuple[str, str]:
    sd = any((ex.get(k) or 0) > 0 for k in ("sd_daf_count", "sd_daf_eoy", "sd_daf_contributions", "sd_daf_grants"))
    kinds = {h["kind"] for h in ex.get("hits", ())}
    if sd:
        return "A_schedule_d_part_i_daf_values", "schedule_d"
    if "hold" in kinds:
        return "B_text_says_holds_dafs", "text"
    if "hold_and_receipt" in kinds:
        return "B2_text_hold_and_receipt_language", "text"
    if kinds & {"receipt"}:
        return "C_receipt_or_payment_mention_only", "text"
    if kinds:
        return "C_mention_only", "text"
    return "D_no_daf_evidence", ""


def l6_rows(universe: Mapping[str, dict], chosen: Mapping[str, dict], exts: Mapping[str, dict]) -> tuple[dict, ...]:
    def row(ein: str) -> dict:
        f, ex = chosen[ein], exts[chosen[ein]["object_id"]]
        cls, src = evidence(ex)
        hold_hits = tuple(h for h in ex.get("hits", ()) if h["kind"] in ("hold", "hold_and_receipt"))
        show = hold_hits or tuple(ex.get("hits", ()))
        return {"ein": ein, "name": ex.get("filer_name") or f["taxpayer_name"], "bmf_name": universe[ein]["name"],
                "ntee": universe[ein]["ntee"], "state": universe[ein]["state"], "universe_basis": universe[ein]["universe_basis"],
                "name_signal": int(bool(NAME_SIGNAL.search(universe[ein]["name"]))),
                "fiscal_year": fy_of(f["tax_period"]), "tax_period": f["tax_period"], "return_type": f["return_type"],
                "line6_status": l6_class(f, ex), "daf_ind_part_iv": ex.get("daf_ind_part_iv", ""),
                "evidence_class": cls, "evidence_source": src,
                "review_verdict": REVIEW.get(ein, ("unreviewed", ""))[0], "review_note": REVIEW.get(ein, ("", ""))[1],
                "sd_daf_count": ex.get("sd_daf_count"), "sd_daf_eoy": ex.get("sd_daf_eoy"),
                "sd_daf_contributions": ex.get("sd_daf_contributions"), "sd_daf_grants": ex.get("sd_daf_grants"),
                "sd_other_count": ex.get("sd_other_count"), "sd_other_eoy": ex.get("sd_other_eoy"),
                "total_assets_eoy": ex.get("total_assets_eoy"),
                "n_daf_text_hits": len(ex.get("hits", ())), "n_hold_hits": len(hold_hits),
                "hit_locations": ";".join(sorted({h["where"] for h in show})),
                "evidence_text": " || ".join(h["text"] for h in show[:2])[:1200],
                "return_object_id": f["object_id"], "xml_status": ex.get("xml_status", ""),
                "xml_url": XML_URL.format(oid=f["object_id"]),
                "index_url": f"https://apps.irs.gov/pub/epostcard/990/xml/{f['index_year']}/index_{f['index_year']}.csv"}
    return tuple(row(e) for e in sorted(chosen))


def l6_summary(rows: Sequence[Mapping], universe_n: int, filers_n: int) -> dict:
    def count(rs, key):
        out: dict = {}
        for r in rs:
            out[r[key]] = out.get(r[key], 0) + 1
        return dict(sorted(out.items()))
    scope = tuple(r for r in rows if r["line6_status"] in ("line6_no", "990EZ", "line6_blank"))
    by_cls = {s: count(tuple(r for r in scope if r["line6_status"] == s), "evidence_class")
              for s in ("line6_no", "990EZ", "line6_blank")}
    a_rows = tuple(r for r in scope if r["evidence_class"].startswith("A_"))
    abc = tuple(r for r in scope if r["evidence_class"][0] in "ABC")
    return {"verdicts": count(abc, "review_verdict"),
            "verdict_by_status": {s: count(tuple(r for r in abc if r["line6_status"] == s), "review_verdict") for s in ("line6_no", "990EZ")},
            "sponsor_rows": [{k: r[k] for k in ("ein", "name", "ntee", "fiscal_year", "return_type", "review_verdict", "total_assets_eoy",
                                                "sd_daf_count", "sd_daf_eoy")} for r in abc if r["review_verdict"].startswith("sponsor")],
            "bmf_universe_eins": universe_n, "eins_with_990_or_ez_fy2022plus": filers_n,
            "returns_read": len(rows), "xml_status": count(rows, "xml_status"),
            "line6_status": count(rows, "line6_status"), "evidence_by_status": by_cls,
            "a_daf_eoy_sum": sum(r["sd_daf_eoy"] or 0 for r in a_rows),
            "a_daf_count_sum": sum(r["sd_daf_count"] or 0 for r in a_rows),
            "a_rows": [{k: r[k] for k in ("ein", "name", "fiscal_year", "return_type", "line6_status", "sd_daf_count",
                                           "sd_daf_eoy", "total_assets_eoy")} for r in sorted(a_rows, key=lambda r: -(r["sd_daf_eoy"] or 0))],
            "b_top": [{k: r[k] for k in ("ein", "name", "fiscal_year", "return_type", "line6_status", "total_assets_eoy",
                                          "evidence_class", "evidence_text")}
                      for r in sorted((r for r in scope if r["evidence_class"].startswith("B")),
                                      key=lambda r: -(r["total_assets_eoy"] or 0))[:60]]}


def task_line6(a) -> dict:
    panel = frozenset(ein9(r["ein"]) for r in read_csv(os.path.join(DATA, "dafrc-sponsor-schedule-d-fy2019-2024.csv")))
    universe = load_bmf(a.irs_dir, panel)
    idx = load_index_rows(a.irs_dir, frozenset(universe))
    chosen = {e: f for e, f in ((e, newest_return(v)) for e, v in idx.items()) if f}
    exts = fetch_all(tuple(chosen.values()), a.work_dir, a.fetch)
    ok = {e: f for e, f in chosen.items() if exts[f["object_id"]].get("xml_status") == "ok"}
    rows = l6_rows(universe, ok, exts)
    keep = tuple(r for r in rows if r["line6_status"] in ("line6_no", "990EZ", "line6_blank")
                 and r["evidence_class"][0] in "ABC")
    keep = tuple(sorted(keep, key=lambda r: (VERDICT_ORDER.get(r["review_verdict"], 9), r["evidence_class"], -(r["sd_daf_eoy"] or 0), -(r["total_assets_eoy"] or 0))))
    write_csv(os.path.join(DATA, OUT["line6"]), [{k: fmt(v) for k, v in r.items()} for r in keep], tuple(rows[0]))
    s = l6_summary(rows, len(universe), len(chosen))
    s["not_ok"] = {k: v for k, v in _count(exts[f["object_id"]].get("xml_status") for f in chosen.values()).items() if k != "ok"}
    s["rows_written"] = len(keep)
    return s


def _count(xs: Iterable) -> dict:
    out: dict = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


# ----------------------------------------------------------------------------- P-99F-01 FY2024 imputation resolution
METRIC_COLS = {"daf_assets_eoy": ("sched_d_daf_eoy_value", "sd_daf_eoy", "eoy_daf_assets", "source_eoy_daf_assets"),
               "daf_accounts_eoy": ("sched_d_daf_count", "sd_daf_count", "number_of_daf_accounts", "source_number_of_accounts")}
FILED_SRC = frozenset({"IRS 990", "NPT historical data", "paper submission"})


def unresolved_fy2024(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    return tuple(r for r in rows if r["fiscal_year"] == "2024" and r["applied"] == "0" and r["metric"] in METRIC_COLS)


def last_filed_before(dafrc: Sequence[Mapping], ein: str, metric: str, fy: int) -> tuple[int | None, float | None]:
    _, _, col, src = METRIC_COLS[metric]
    pts = sorted((int(r["fiscal_year_end"]), num(r[col])) for r in dafrc
                 if ein9(r["ein"]) == ein and int(r["fiscal_year_end"]) < fy and r[src] in FILED_SRC and r[col] not in ("", None))
    return pts[-1] if pts else (None, None)


def harvest_value(rows: Sequence[Mapping], ein: str, fy: int, metric: str) -> tuple[float | None, str, str]:
    col = METRIC_COLS[metric][0]
    hits = tuple(r for r in rows if ein9(r["ein"]) == ein and r["fiscal_year"] == str(fy) and r["xml_status"].startswith("ok"))
    best = max(hits, key=lambda r: r.get("return_ts", "")) if hits else None
    return (num(best[col]) if best and best[col] not in ("", None) else None,
            best["return_object_id"] if best else "", best.get("xml_status", "") if best else "")


def resolve_row(r: Mapping, ctx: Mapping) -> dict:
    ein, metric, fy = ein9(r["ein"]), r["metric"], 2024
    imputed = num(r["dafrc_value"])
    filed = num(r["filed_value"]) if r["filed_value"] not in ("", None) else None
    fill_24 = harvest_value(ctx["fill"], ein, fy, metric)
    fill_25 = harvest_value(ctx["fill"], ein, 2025, metric)
    harv_25 = harvest_value(ctx["harvest"], ein, 2025, metric)
    other = tuple(o for o in ctx["other_returns"].get(ein, ()) if o["object_id"] != r["return_object_id"])
    other_vals = tuple((o, ctx["exts"].get(o["object_id"], {})) for o in other)
    other_hit = next(((o, e) for o, e in other_vals if e.get(METRIC_COLS[metric][1]) is not None), None)
    last_fy, last_v = last_filed_before(ctx["dafrc"], ein, metric, fy)
    idx_25 = next(((o, e) for o, e in ((o, ctx["exts"].get(o["object_id"], {})) for o in ctx["fy2025_returns"].get(ein, ()))
                   if e.get(METRIC_COLS[metric][1]) is not None), None)
    idx_25v = idx_25[1].get(METRIC_COLS[metric][1]) if idx_25 else None
    next_v, next_src = ((fill_25[0], "fill_fy2025") if fill_25[0] is not None else (harv_25[0], "harvest_fy2025")
                        if harv_25[0] is not None else (idx_25v, "index_fy2025_return") if idx_25v is not None else (None, ""))
    zero_next = next_v == 0 and (last_v or 0) > 0     # count-without-value or wind-down: not a usable bracket
    interp = (last_v + (next_v - last_v) * (fy - last_fy) / (2025 - last_fy)) \
        if last_v is not None and next_v is not None and not zero_next else None
    if fill_24[0] is not None:
        res, new, src = "filed_value_from_2026_fill_fy2024", fill_24[0], fill_24[1]
    elif other_hit:
        res, new, src = "filed_value_from_other_fy2024_return", other_hit[1].get(METRIC_COLS[metric][1]), other_hit[0]["object_id"]
    elif filed is not None and imputed is not None and filed == imputed:
        res, new, src = "already_equals_filed_value", filed, r["return_object_id"]
    elif next_v is not None and zero_next:
        res, new, src = f"next_value_zero_{next_src}_not_used", None, ""
    elif next_v is not None and interp is not None:
        res, new, src = f"bracketed_by_{next_src}_proxy_only", interp, "interpolation"
    elif next_v is not None:
        res, new, src = f"next_value_only_{next_src}_no_prior_filed", None, ""
    else:
        res, new, src = "unresolved", None, ""
    return {"fiscal_year": fy, "ein": ein, "name": r["name"], "type": r["type"], "metric": metric,
            "evidence_class_before": r["evidence_class"], "note_before": r["note"][:160],
            "dafrc_imputed_value": imputed, "filed_value_fy2024_return": filed,
            "fy2024_return_object_id": r["return_object_id"],
            "other_fy2024_returns_checked": ";".join(o["object_id"] for o in other),
            "other_fy2024_return_status": ";".join(e.get("xml_status", "") for _, e in other_vals),
            "fill_fy2024_value": fill_24[0], "fill_fy2025_value": fill_25[0], "fill_fy2025_object_id": fill_25[1],
            "harvest_fy2025_value": harv_25[0], "harvest_fy2025_object_id": harv_25[1],
            "index_fy2025_value": idx_25v, "index_fy2025_object_id": idx_25[0]["object_id"] if idx_25 else "",
            "last_filed_fy": last_fy, "last_filed_value": last_v, "interpolated_fy2024_proxy": interp,
            "resolution": res, "resolved_value": new, "resolved_value_source": src,
            "becomes_filed_value": int(res.startswith("filed_value") or res == "already_equals_filed_value"),
            "becomes_new_filed_value": int(res.startswith("filed_value")),
            "delta_vs_imputed": (new - imputed) if new is not None and imputed is not None else None}


def task_dafrc(a) -> dict:
    corr = read_csv(os.path.join(DATA, "dafrc-corrections-itemized.csv"))
    todo = unresolved_fy2024(corr)
    eins = frozenset(ein9(r["ein"]) for r in todo)
    idx = load_index_rows(a.irs_dir, eins, types=("990",))
    fy24 = {e: tuple(f for f in v if fy_of(f["tax_period"]) == 2024) for e, v in idx.items()}
    used = frozenset(r["return_object_id"] for r in todo)
    others = tuple(f for v in fy24.values() for f in v if f["object_id"] not in used)
    fy25 = {e: tuple(sorted((f for f in v if fy_of(f["tax_period"]) == 2025), key=lambda f: f["object_id"], reverse=True))
            for e, v in idx.items()}       # every FY2025 990 in index_2021..2026, used only when fill/harvest give no value
    exts = fetch_all(others + tuple(f for v in fy25.values() for f in v), a.work_dir, a.fetch)
    ctx = {"fill": read_csv(os.path.join(DATA, "form990-harvest-2026-fill.csv")),
           "harvest": read_csv(os.path.join(DATA, "form990-returns-schedule-d-harvest-full.csv")),
           "dafrc": read_csv(os.path.join(DATA, "dafrc-sponsor-schedule-d-fy2019-2024.csv")),
           "other_returns": fy24, "fy2025_returns": fy25, "exts": exts}
    rows = tuple(resolve_row(r, ctx) for r in todo)
    write_csv(os.path.join(DATA, OUT["dafrc"]), [{k: fmt(v) for k, v in r.items()} for r in rows], tuple(rows[0]))
    def agg(metric):
        rs = tuple(r for r in rows if r["metric"] == metric)
        by = _count(r["resolution"] for r in rs)
        imp = {k: sum(r["dafrc_imputed_value"] or 0 for r in rs if r["resolution"] == k) for k in by}
        new = {k: sum(r["resolved_value"] or 0 for r in rs if r["resolution"] == k) for k in by}
        return {"rows": len(rs), "by_resolution": by, "imputed_sum_by_resolution": imp, "resolved_sum_by_resolution": new,
                "becomes_filed": sum(r["becomes_filed_value"] for r in rs),
                "becomes_new_filed": sum(r["becomes_new_filed_value"] for r in rs),
                "fill_eins_matched": len({r["ein"] for r in rs if r["fill_fy2025_value"] is not None or r["fill_fy2024_value"] is not None})}
    return {"unresolved_rows": len(todo), "other_fy2024_returns": len(others),
            "index_fy2025_returns_read": sum(len(v) for v in fy25.values()),
            "other_status": _count(e.get("xml_status") for e in exts.values()),
            **{m: agg(m) for m in METRIC_COLS},
            "new_filed_rows": [{k: r[k] for k in ("ein", "name", "metric", "dafrc_imputed_value", "resolved_value",
                                                  "resolved_value_source", "resolution")}
                               for r in rows if r["becomes_new_filed_value"]],
            "bracket_rows": [{k: r[k] for k in ("ein", "name", "metric", "dafrc_imputed_value", "last_filed_fy",
                                                "last_filed_value", "fill_fy2025_value", "harvest_fy2025_value",
                                                "index_fy2025_value", "interpolated_fy2024_proxy", "resolution")}
                             for r in rows if not r["becomes_filed_value"] and r["resolution"] != "unresolved"]}


# ----------------------------------------------------------------------------- full-text reads (P-STF-03, P-GPT-03, P-B33A-03, P-QA3-06)
TEXT_TOPICS = {
    "daf_to_daf": re.compile(r"(transfer\w*|grant\w*|distribut\w*|mov\w*)[^.;]{0,90}(other|another|third[- ]party|outside)\s+"
                             r"(sponsoring organi[sz]ations?|donor[- ]advised fund|DAF|charitable gift fund|national)"
                             r"|(sponsoring organi[sz]ations?|donor[- ]advised funds?)[^.;]{0,60}(transfer\w*)"
                             r"|DAF[- ]to[- ]DAF|fund[- ]to[- ]fund|succession[^.;]{0,40}another", re.I),
    "institutional_channel": re.compile(r"\b(financial institution|institutional|private[- ]label|white[- ]label|"
                                        r"bank(s|ing)? partner|wealth management (firm|partner)|partner(ed)? (firms?|institutions?)|"
                                        r"GivingPoint|program partners?|affiliated (giving )?programs?)\b", re.I),
    "advisor_managed": re.compile(r"advis[oe]r[- ](managed|directed)|professionally managed|investment advis[oe]r program|"
                                  r"Charitable Investment Advis[oe]r|CIAP|independent (investment )?advis[oe]rs?", re.I),
    "investment_income_booking": re.compile(r"(interest and dividends?|dividends? and interest|investment income|investment return|"
                                            r"unitiz|pooled (investment )?funds?|investment pools?|net asset value|"
                                            r"realized and unrealized|investment (management )?fees?|net of (investment )?(fees|expenses))", re.I),
}
NUM_FIELDS = {  # Part VIII / IX / XI and Schedule D Parts XI-XII (reconciliations)
    "InvestmentIncomeGrp/TotalRevenueColumnAmt": "p8_l3_investment_income",
    "NetGainOrLossInvestmentsGrp/TotalRevenueColumnAmt": "p8_l7d_net_gain_securities_other",
    "GrossAmountSalesAssetsGrp/SecuritiesAmt": "p8_l7a_gross_sales_securities",
    "GrossAmountSalesAssetsGrp/OtherAmt": "p8_l7a_gross_sales_other",
    "NetUnrlzdGainsLossesInvstAmt": "p11_l5_net_unrealized_gains",
    "FeesForServicesInvstMgmntFeesGrp/TotalAmt": "p9_l11f_invest_mgmt_fees",
    "OtherRevenueTotalAmt": "p8_l11e_other_revenue_total",
    "TotalRevenueGrp/TotalRevenueColumnAmt": "p8_l12_total_revenue",
    "DonorAdvisedFundsHeldCnt": "sd_daf_count", "DonorAdvisedFundsContriAmt": "sd_daf_contributions",
    "DonorAdvisedFundsGrantsAmt": "sd_daf_grants", "DonorAdvisedFundsVlEOYAmt": "sd_daf_eoy",
    "FundsAndOtherAccountsHeldCnt": "sd_other_count", "FundsAndOtherAccountsVlEOYAmt": "sd_other_eoy",
    "NetUnrealizedGainsInvstAmt": "sd_xi_2a_net_unrealized_gains", "InvestmentExpensesAmt": "sd_xi_4a_or_xii_4a_investment_expenses",
    "UnrealizedGainsLossesAmt": "sd_unrealized_gains_other", "TotalRevenuePerAuditedFinclAmt": "sd_xi_1_total_revenue_audit",
    "TotalExpensesPerAuditedFinclAmt": "sd_xii_1_total_expenses_audit",
}
TEXT_TARGETS = (  # (label, EIN, topics, fiscal years)
    ("NPT", "237825575", ("institutional_channel", "daf_to_daf", "advisor_managed"), (2023, 2024, 2025)),
    ("Fidelity Charitable", "110303001", ("advisor_managed", "daf_to_daf"), (2024, 2025)),
    ("DAFgiving360", "311640316", ("advisor_managed", "daf_to_daf", "institutional_channel"), (2024, 2025)),
    ("MS GIFT", "527082731", ("investment_income_booking", "advisor_managed"), (2023, 2024, 2025)),
    ("Foundation For The Carolinas", "566047886", ("investment_income_booking",), (2023, 2024, 2025)),
    ("Foundation for the Charlotte Jewish Community", "311501858", ("investment_income_booking",), (2023, 2024, 2025)),
    ("Endaoment", "844661797", ("investment_income_booking",), (2024, 2025)),
)


def full_xml(f: Mapping, work_dir: str, fetch: bool) -> bytes | None:
    path = os.path.join(work_dir, "xmlfull", f"{f['object_id']}_public.xml")
    teos = os.path.join(work_dir, "teos", f"{f['object_id']}_public.xml")
    for p in (path, teos):
        if os.path.exists(p):
            with open(p, "rb") as fh:
                return fh.read()
    if not fetch:
        return None
    try:
        with urllib.request.urlopen(urllib.request.Request(XML_URL.format(oid=f["object_id"]), headers=UA), timeout=300) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if e.code != 404 or not f.get("batch") or f.get("index_year") != 2026:
            return None
        with TEOS_LOCK:
            meta = teos_fetch(f["object_id"], f["batch"], work_dir)
        return full_xml(f, work_dir, False) if meta.get("status") == "ok" else None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    return data


def read_return(xml: bytes, topics: Sequence[str]) -> dict:
    root = ET.fromstring(xml)
    def path_val(path: str):
        parts = path.split("/")
        for el in root.iter(NS + parts[-1]):
            return num(el.text or "") if len(parts) == 1 else None
        return None
    nums: dict = {}
    for path, name in NUM_FIELDS.items():
        parts = path.split("/")
        for grp in (root.iter(NS + parts[0]) if len(parts) > 1 else ()):
            leaf = grp.find(NS + parts[1])
            if leaf is not None:
                nums[name] = num(leaf.text or "")
                break
        else:
            if len(parts) == 1:
                nums[name] = path_val(path)
    texts = tuple((_where(root, el), re.sub(r"\s+", " ", el.text)) for el in root.iter()
                  if len(el) == 0 and el.text and len(el.text) > 40)
    hits = {t: [f"[{w}] {sentence_around(txt, m, 300)}" for w, txt in texts for m in list(TEXT_TOPICS[t].finditer(txt))[:2]]
            for t in topics}
    part_i_notes = tuple(re.sub(r"\s+", " ", f"[{_txt(g, 'FormAndLineReferenceDesc')}] {_txt(g, 'ExplanationTxt')}")[:1500]
                         for g in root.iter(NS + "SupplementalInformationDetail")
                         if re.search(r"PART\s*I\b|PART\s*1\b|DONOR[- ]ADVISED", _txt(g, "FormAndLineReferenceDesc"), re.I))
    hdr = {k: (root.find(f".//{NS}{k}").text if root.find(f".//{NS}{k}") is not None else "")
           for k in ("TaxPeriodEndDt", "ReturnTs", "ReturnTypeCd", "AmendedReturnInd")}
    return {**hdr, **nums, "sched_d_part_i_or_daf_notes": list(part_i_notes)[:10],
            "hits": {t: list(dict.fromkeys(v))[:30] for t, v in hits.items()}}


def _txt(el, tag: str) -> str:
    c = el.find(NS + tag)
    return (c.text or "") if c is not None else ""


def _where(root, el) -> str:
    return local(el.tag)


def top_sponsors(n: int = 50, fy: str = "2024") -> tuple[tuple, ...]:
    d = tuple(r for r in read_csv(os.path.join(DATA, "dafrc-sponsor-schedule-d-fy2019-2024.csv")) if r["fiscal_year_end"] == fy)
    top = sorted(d, key=lambda r: -(num(r["eoy_daf_assets"]) or 0))[:n]
    named = frozenset(t[1] for t in TEXT_TARGETS)
    return tuple((f"top50:{r['name']}", ein9(r["ein"]), ("daf_to_daf",), (2024,)) for r in top if ein9(r["ein"]) not in named)


def task_texts(a) -> dict:
    targets = TEXT_TARGETS + top_sponsors()
    eins = frozenset(t[1] for t in targets)
    idx = load_index_rows(a.irs_dir, eins, types=("990",))
    out = {}
    for label, ein, topics, fys in targets:
        rets = {}
        for fy in fys:
            cand = tuple(f for f in idx.get(ein, ()) if fy_of(f["tax_period"]) == fy)
            f = max(cand, key=lambda f: f["object_id"]) if cand else None
            xml = full_xml(f, a.work_dir, a.fetch) if f else None
            rets[str(fy)] = ({"object_id": f["object_id"], "tax_period": f["tax_period"], "xml_url": XML_URL.format(oid=f["object_id"]),
                              **read_return(xml, topics)} if xml else {"object_id": f["object_id"] if f else "", "status": "not_read"})
        out[label] = {"ein": ein, "returns": rets}
    return out


# ----------------------------------------------------------------------------- local document greps (audits, reports)
DOC_PATTERNS = {
    "advisor_managed": r"advisor[- ]managed|Charitable Investment Advisor Program|Total Advisor-managed|professionally managed",
    "investment_income": r"interest and dividends|net investment income|investment return, net|presented net of|realized and unrealized|"
                         r"investment (management )?fees|unitiz|net asset value",
    "daf_to_daf": r"other sponsoring|another sponsoring|other donor[- ]advised|transfers? (to|from) (other|another)|DAF[- ]to[- ]DAF",
    "institutional": r"financial institution|institutional|private[- ]label|partner(ed)? (firms?|institutions?)|GivingPoint",
    "accounts": r"giving accounts|donor[- ]advised funds in total|number of (accounts|funds|donor)",
}


def task_docs(a) -> dict:
    def grep(path: str) -> dict:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
        return {k: [f"{i + 1}: {re.sub(r'\\s+', ' ', l).strip()}" for i, l in enumerate(lines) if re.search(p, l, re.I)][:40]
                for k, p in DOC_PATTERNS.items()}
    files = sorted(f for f in os.listdir(a.doc_dir) if f.endswith(".txt"))
    return {f: grep(os.path.join(a.doc_dir, f)) for f in files}


# ----------------------------------------------------------------------------- CLI
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", choices=("line6", "dafrc", "texts", "docs"))
    ap.add_argument("--irs-dir", default="IRS")
    ap.add_argument("--work-dir", default="WORK")
    ap.add_argument("--doc-dir", default="DOCS")
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    task = {"line6": task_line6}.get(a.task) or globals()[f"task_{a.task}"]
    print(json.dumps(task(a), indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
