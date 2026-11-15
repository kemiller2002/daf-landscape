#!/usr/bin/env python3
"""Queue batch 38 B: data follow-ups (stdlib only, functional style: pure transforms, I/O at the edges).

Queue items (data/mission-2026-11-14/research-priority-queue.csv):
  P-B37B-01  line-6 false-negative screen beyond NTEE T30/T31/T70 and DAF-like names. Universe: every section 501(c)(3)
             EIN whose newest FY2022+ return in the IRS SOI 990 extracts (22..25eoextract990.csv) answers Part IV line 6
             'N' and reports total assets >= $1m, minus the DAFRC panel and minus the batch-37 universe. The newest
             FY2022+ Form 990 of each EIN in TEOS index_2021..2026 is read in full: Schedule D Part I (both columns) and
             every text leaf that mentions donor-advised / donor-directed funds or 'sponsoring organization'.
             -> data/mission-2026-11-14/line6-fulltext-screen.csv                                    (task fulltext)
  P-ANL-08   practitioner 'payout triad' FY2021-24 from repo data (aggregate, median sponsor, ex-DAF-to-DAF)
             -> data/mission-2026-11-14/payout-triad-2021-2024.csv                                    (task triad)
  P-B34A-03  recipient-side check of R5 central weights for the 10 largest community-foundation and single-issue
             recipients (Schedule D Part I contributions vs inbound sponsor-to-sponsor lines, same and next FY)
             -> JSON summary (figures quoted in the batch-38 note)                                    (task recipients)
  P-B37B-03  MS GIFT line-3 anomaly: Part VIII / IX / XI, Schedule D Parts XI-XIII and Schedule O of every indexed
             FY2022+ return                                                                           (task msgift)
  P-LND-04   per-head vs per-FTE pay for the 20 largest staffed sponsors (FTE from public audits / reports, manual
             table FTE_EVIDENCE below)  -> data/mission-2026-11-14/sponsor-pay-per-fte.csv             (task fte)
  P-B36A-01  TY2025 index check for PPGF, Givinga, NFG, Bright Funds and CAF America                  (task accounts)

Sources
  * IRS SOI annual extracts https://www.irs.gov/pub/irs-soi/{22..25}eoextract990.zip
  * IRS EO BMF eo1..eo4.csv; IRS TEOS index https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv
  * IRS e-file XML, GivingTuesday mirror https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OID}_public.xml
    (2026 TEOS zip fallback via mission_batch35_screens.teos_fetch)
  * Repo CSVs named in each task.

Usage
  python3 scripts/mission_batch38_data.py fulltext   --irs-dir IRS --soi-dir SOI --work-dir WORK [--fetch]
  python3 scripts/mission_batch38_data.py triad
  python3 scripts/mission_batch38_data.py recipients
  python3 scripts/mission_batch38_data.py msgift     --irs-dir IRS --work-dir WORK [--fetch]
  python3 scripts/mission_batch38_data.py fte
  python3 scripts/mission_batch38_data.py accounts   --irs-dir IRS
"""
from __future__ import annotations

import argparse
import csv
import io
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
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DATA, NS, XML_URL, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_batch37_filings import (TEOS_LOCK, UA, classify_snippet, fmt, fy_of, full_xml, load_bmf,  # noqa: E402
                                     read_return, sentence_around, _dedupe_hits)
from mission_batch35_screens import batch_zips, central_directory, member_xml  # noqa: E402

WORKERS = int(os.environ.get("MISSION990_WORKERS", "48"))
FT_VERSION = 1
INDEX_YEARS = tuple(range(2021, 2027))
MIN_TAX_PD = "202201"               # FY2022+ (tax periods ending 2022 or later; TY2021+)
MIN_ASSETS = 1_000_000
SOI_FILES = tuple(f"{y}eoextract990.csv" for y in (22, 23, 24, 25))
OUT = {"fulltext": "line6-fulltext-screen.csv", "triad": "payout-triad-2021-2024.csv", "fte": "sponsor-pay-per-fte.csv"}

# Mention regex is wider than batch 37: adds donor-directed funds and the IRC 4966 term "sponsoring organization".
MENTION = re.compile(r"donor[- ]advised|\bDAFs?\b|donor[- ]directed funds?|sponsoring organi[sz]ation", re.I)
# Strong holding language: the filer itself sponsors / offers / reports a number of DAFs (checked on the window).
STRONG = re.compile(
    r"(serv\w*|act\w*|operat\w*|is|as)\s+(a|the)\s+sponsoring organi[sz]ation"
    r"|sponsoring organi[sz]ation\s+(of|for)\s+(\w+\s+){0,2}donor[- ]advised"
    r"|\b\d[\d,]*\s+donor[- ](advised|directed) (funds|accounts)"
    r"|\b(offer|offers|offering|administer|administers|maintain|maintains|hold|holds|manage|manages|host|hosts|sponsor|sponsors)"
    r"\s+(\w+\s+){0,3}donor[- ](advised|directed) funds?"
    r"|\b(our|its)\s+donor[- ](advised|directed) funds?"
    r"|donor[- ]advised funds? (program|platform|accounts?)\b(?! at)", re.I)
RECEIPT = re.compile(r"\b(from|through|via|by|to|into|at|with)\s+(a|an|the|their|his|her|its|donors'?|various|several)?\s*"
                     r"(donor[- ]advised|DAF)", re.I)


# ----------------------------------------------------------------------------- small helpers (I/O at edges)
def read_rows(path: str, encoding: str = "latin-1") -> Iterable[dict]:
    with open(path, newline="", encoding=encoding) as fh:
        r = csv.reader(fh)
        head = [h.replace("﻿", "").strip().lower() for h in next(r)]
        for row in r:
            yield dict(zip(head, row))


def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh)


def median(xs: Sequence[float]) -> float | None:
    xs = tuple(x for x in xs if x is not None)
    return statistics.median(xs) if xs else None


def ratio(a, b) -> float | None:
    return a / b if a is not None and b not in (None, 0) else None


# ----------------------------------------------------------------------------- P-B37B-01 universe
def soi_newest(soi_dir: str) -> dict[str, dict]:
    """Newest FY2022+ SOI 990 row per 501(c)(3) EIN (later file wins on ties)."""
    def rows():
        for f in SOI_FILES:
            for r in read_rows(os.path.join(soi_dir, f)):
                if r.get("subseccd", "").strip().lstrip("0") == "3" and r.get("tax_pd", "").strip() >= MIN_TAX_PD:
                    yield {"ein": ein9(r["ein"]), "tax_pd": r["tax_pd"].strip(), "soi_line6": r["dnradvisedfundscd"].strip(),
                           "soi_total_assets": num(r["totassetsend"].strip()), "soi_file": f,
                           "soi_employees": num(r.get("noemplyeesw3cnt", "").strip())}
    best: dict[str, dict] = {}
    for r in rows():
        if r["ein"] not in best or r["tax_pd"] >= best[r["ein"]]["tax_pd"]:
            best[r["ein"]] = r
    return best


def load_index(irs_dir: str, eins: frozenset, types=("990",)) -> dict[str, tuple[dict, ...]]:
    def rows(y):
        for d in read_rows(os.path.join(irs_dir, f"index_{y}.csv")):
            if d["return_type"] in types and ein9(d["ein"]) in eins:
                yield {"ein": ein9(d["ein"]), "tax_period": d["tax_period"], "return_type": d["return_type"],
                       "object_id": d["object_id"], "taxpayer_name": d["taxpayer_name"], "index_year": y,
                       "batch": d.get("xml_batch_id", "")}
    dedup = {r["object_id"]: r for y in INDEX_YEARS for r in rows(y)}
    out: dict[str, list] = {}
    for r in dedup.values():
        out.setdefault(r["ein"], []).append(r)
    return {e: tuple(sorted(v, key=lambda r: (r["tax_period"], r["object_id"]))) for e, v in out.items()}


def bmf_lookup(irs_dir: str, eins: frozenset) -> dict[str, dict]:
    return {ein9(r["ein"]): {"ntee": r["ntee_cd"], "state": r["state"]}
            for i in range(1, 5) for r in read_rows(os.path.join(irs_dir, f"eo{i}.csv")) if ein9(r["ein"]) in eins}


def newest(filings: Sequence[Mapping]) -> dict | None:
    keep = tuple(f for f in filings if f["tax_period"] >= MIN_TAX_PD)
    return max(keep, key=lambda f: (f["tax_period"], f["object_id"])) if keep else None


# ----------------------------------------------------------------------------- P-B37B-01 extract
SD_FIELDS = {"DonorAdvisedFundsHeldCnt": "sd_daf_count", "DonorAdvisedFundsContriAmt": "sd_daf_contributions",
             "DonorAdvisedFundsGrantsAmt": "sd_daf_grants", "DonorAdvisedFundsVlEOYAmt": "sd_daf_eoy",
             "FundsAndOtherAccountsHeldCnt": "sd_other_count", "FundsAndOtherAccountsVlEOYAmt": "sd_other_eoy",
             "FundsAndOtherAccountsContriAmt": "sd_other_contributions", "FundsAndOtherAccountsGrantsAmt": "sd_other_grants"}
TEXT_SCOPE = re.compile(r"^IRS990(EZ|Schedule[A-Z]+)?$")


def window_kind(s: str) -> str:
    strong = bool(STRONG.search(s))
    rec = bool(RECEIPT.search(s))
    base = classify_snippet(s)                   # batch-37 hold / hold_and_receipt / receipt / mention
    return ("strong" if strong and not rec else "strong_and_receipt" if strong else
            base if base != "mention" else "mention")


def extract_ft(stream) -> dict:
    out: dict = {"sched_d_present": 0, "hits": []}
    stack: list[str] = []
    for event, el in ET.iterparse(stream, events=("start", "end")):
        tag = local(el.tag)
        if event == "start":
            stack.append(tag)
            continue
        stack.pop()
        if tag == "ReturnHeader":
            g = lambda p: next(((c.text or "").strip() for c in el.iter() if local(c.tag) == p), "")
            out.update({"tax_period_end": g("TaxPeriodEndDt"), "return_ts": g("ReturnTs"), "return_type": g("ReturnTypeCd"),
                        "filer_name": g("BusinessNameLine1Txt"), "filer_state": g("StateAbbreviationCd")})
            el.clear()
            continue
        if tag == "DonorAdvisedFundInd" and "IRS990" in stack:
            out["daf_ind_part_iv"] = (el.text or "").strip()
        elif tag == "AmendedReturnInd":
            out["amended"] = (el.text or "").strip()
        elif tag == "EOYAmt" and stack and stack[-1] == "TotalAssetsGrp":
            out["total_assets_eoy"] = num(el.text or "")
        elif tag in SD_FIELDS and "IRS990ScheduleD" in stack:
            out[SD_FIELDS[tag]] = num(el.text or "")
        elif tag == "IRS990ScheduleD":
            out["sched_d_present"] = 1
        elif len(el) == 0 and el.text and len(el.text) > 20 and MENTION.search(el.text):
            sched = next((s for s in reversed(stack) if TEXT_SCOPE.match(s)), "")
            for m in list(MENTION.finditer(el.text))[:3]:
                snip = sentence_around(el.text, m)
                out["hits"].append({"where": f"{sched}/{tag}", "kind": window_kind(snip), "text": snip[:600]})
        if TEXT_SCOPE.match(tag):
            el.clear()
    out["hits"] = _dedupe_hits(out["hits"])[:25]
    return out


def fetch_ft(f: Mapping, work_dir: str, fetch: bool, retries: int = 2) -> dict:
    oid = f["object_id"]
    path = os.path.join(work_dir, "ft", oid[:4], f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == FT_VERSION:
            return c
    if not fetch:
        return {"xml_status": "not_fetched", "object_id": oid}
    res = {"xml_status": "error:none"}
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(XML_URL.format(oid=oid), headers=UA), timeout=120) as r:
                res = {**extract_ft(r), "xml_status": "ok", "xml_source": "gt_mirror"}
            break
        except urllib.error.HTTPError as e:
            res = {"xml_status": f"http_{e.code}"}
            if e.code in (403, 404):
                break
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
            res = {"xml_status": f"error:{type(e).__name__}"}
            time.sleep(2 * (attempt + 1))
    if res["xml_status"] == "http_404" and f.get("index_year") == 2026 and f.get("batch"):
        try:
            xml = teos_member(oid, f["batch"], work_dir)
            res = ({**extract_ft(io.BytesIO(xml)), "xml_status": "ok", "xml_source": "teos_zip"} if xml
                   else {"xml_status": "teos_not_in_zips"})
        except (urllib.error.URLError, OSError, ValueError, ET.ParseError) as e:
            res = {"xml_status": f"error:teos_{type(e).__name__}"}
    res = {**res, "_v": FT_VERSION, "object_id": oid}
    if not res["xml_status"].startswith("error"):
        write_json(path, res)
    return res


_CD: dict[str, dict] = {}


def zip_members(url: str, work_dir: str) -> dict:
    """Central directory of a TEOS zip, read once per process (the cached JSON is large) and shared by threads."""
    with TEOS_LOCK:
        if url not in _CD:
            try:
                _CD[url] = central_directory(url, os.path.join(work_dir, "zipcd"))["members"]
            except urllib.error.HTTPError as e:
                if e.code not in (302, 403, 404):
                    raise
                _CD[url] = {}
            _CD[url] = {k.rsplit("/", 1)[-1]: (k, v) for k, v in _CD[url].items()}
        return _CD[url]


def teos_member(oid: str, label: str, work_dir: str) -> bytes | None:
    """Inflate {oid}_public.xml from the TEOS zip(s) for its index label (member reads run in parallel)."""
    os.makedirs(os.path.join(work_dir, "teos"), exist_ok=True)
    for url in batch_zips(label):
        hit = zip_members(url, work_dir).get(f"{oid}_public.xml")
        if hit:
            return member_xml(url, hit[0], hit[1], os.path.join(work_dir, "teos"))
    return None


def evidence_class(ex: Mapping) -> str:
    sd = any((ex.get(k) or 0) > 0 for k in ("sd_daf_count", "sd_daf_eoy", "sd_daf_contributions", "sd_daf_grants"))
    kinds = {h["kind"] for h in ex.get("hits", ())}
    return ("A_schedule_d_part_i_daf_values" if sd else
            "B1_strong_holding_language" if "strong" in kinds else
            "B2_holding_language" if kinds & {"hold", "strong_and_receipt"} else
            "B3_hold_and_receipt_language" if "hold_and_receipt" in kinds else
            "C_receipt_or_mention_only" if kinds else "D_none")


def line6_status(ex: Mapping) -> str:
    v = (ex.get("daf_ind_part_iv") or "").lower()
    return "line6_yes" if v in ("true", "1") else "line6_no" if v in ("false", "0") else "line6_blank"


# Manual reading [I] of every A and B1 row and of B2 rows with assets >= $25m (2026-11-15); see review_note.
REVIEW: dict[str, tuple[str, str]] = {}


def ft_row(ein: str, f: Mapping, ex: Mapping, soi: Mapping, bmf: Mapping) -> dict:
    hits = tuple(ex.get("hits", ()))
    order = {"strong": 0, "strong_and_receipt": 1, "hold": 2, "hold_and_receipt": 3, "receipt": 4, "mention": 5}
    show = tuple(sorted(hits, key=lambda h: order.get(h["kind"], 9)))
    b = bmf.get(ein, {})
    v = REVIEW.get(ein, ("unreviewed", ""))
    return {"ein": ein, "name": ex.get("filer_name") or f["taxpayer_name"], "bmf_ntee": b.get("ntee", ""),
            "state": ex.get("filer_state") or b.get("state", ""),
            "fiscal_year": fy_of(f["tax_period"]), "tax_period": f["tax_period"], "amended": ex.get("amended", ""),
            "line6_status": line6_status(ex), "soi_line6": soi["soi_line6"], "soi_tax_pd": soi["tax_pd"],
            "evidence_class": evidence_class(ex), "review_verdict": v[0], "review_note": v[1],
            "sd_daf_count": ex.get("sd_daf_count"), "sd_daf_eoy": ex.get("sd_daf_eoy"),
            "sd_daf_contributions": ex.get("sd_daf_contributions"), "sd_daf_grants": ex.get("sd_daf_grants"),
            "sd_other_count": ex.get("sd_other_count"), "sd_other_eoy": ex.get("sd_other_eoy"),
            "total_assets_eoy": ex.get("total_assets_eoy"),
            "n_text_hits": len(hits), "n_strong_hits": sum(h["kind"] == "strong" for h in hits),
            "hit_locations": ";".join(sorted({h["where"] for h in show[:4]})),
            "evidence_text": " || ".join(h["text"] for h in show[:2])[:1200],
            "return_object_id": f["object_id"], "xml_source": ex.get("xml_source", ""),
            "xml_url": XML_URL.format(oid=f["object_id"])}


def task_fulltext(a) -> dict:
    panel = frozenset(ein9(r["ein"]) for r in read_csv(os.path.join(DATA, "dafrc-sponsor-schedule-d-fy2019-2024.csv")))
    b37 = frozenset(load_bmf(a.irs_dir, frozenset()))          # batch-37 universe (NTEE T30/T31/T70 or DAF-like name)
    soi = soi_newest(a.soi_dir)
    universe = {e: r for e, r in soi.items() if r["soi_line6"] == "N" and (r["soi_total_assets"] or 0) >= MIN_ASSETS
                and e not in panel and e not in b37}
    idx = load_index(a.irs_dir, frozenset(universe))
    chosen = {e: f for e, f in ((e, newest(v)) for e, v in idx.items()) if f}
    todo = tuple(chosen.values())
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        res = tuple(ex.map(lambda f: fetch_ft(f, a.work_dir, a.fetch), todo))
    exts = {f["object_id"]: r for f, r in zip(todo, res)}
    bmf = bmf_lookup(a.irs_dir, frozenset(chosen))
    rows = tuple(ft_row(e, f, exts[f["object_id"]], universe[e], bmf) for e, f in sorted(chosen.items())
                 if exts[f["object_id"]].get("xml_status") == "ok")
    count = lambda xs: dict(sorted(_count(xs).items()))
    in_scope = tuple(r for r in rows if r["line6_status"] != "line6_yes")
    keep = tuple(r for r in in_scope if r["evidence_class"][0] in "AB")
    keep = tuple(sorted(keep, key=lambda r: (r["evidence_class"], -(r["sd_daf_eoy"] or 0), -(r["total_assets_eoy"] or 0))))
    write_csv(os.path.join(DATA, OUT["fulltext"]), [{k: fmt(v) for k, v in r.items()} for r in keep],
              tuple(rows[0]) if rows else ())
    a_rows = tuple(r for r in keep if r["evidence_class"].startswith("A"))
    return {"soi_501c3_eins_fy2022plus": len(soi),
            "soi_line6_N_assets_ge_1m": sum(1 for r in soi.values() if r["soi_line6"] == "N" and (r["soi_total_assets"] or 0) >= MIN_ASSETS),
            "excluded_dafrc_panel": sum(1 for e, r in soi.items() if r["soi_line6"] == "N" and (r["soi_total_assets"] or 0) >= MIN_ASSETS and e in panel),
            "excluded_batch37_universe": sum(1 for e, r in soi.items() if r["soi_line6"] == "N" and (r["soi_total_assets"] or 0) >= MIN_ASSETS and e in b37 and e not in panel),
            "universe_eins": len(universe), "eins_with_990_fy2022plus_in_index": len(chosen),
            "xml_status": count(exts[f["object_id"]].get("xml_status") for f in todo),
            "newest_fy": count(fy_of(f["tax_period"]) for f in todo),
            "line6_status_read": count(r["line6_status"] for r in rows),
            "evidence_in_scope": count(r["evidence_class"] for r in in_scope),
            "verdicts": count(r["review_verdict"] for r in keep),
            "a_rows": [{k: r[k] for k in ("ein", "name", "fiscal_year", "line6_status", "sd_daf_count", "sd_daf_eoy",
                                           "sd_daf_contributions", "total_assets_eoy", "review_verdict")}
                       for r in sorted(a_rows, key=lambda r: -(r["sd_daf_eoy"] or 0))],
            "a_daf_eoy_sum": sum(r["sd_daf_eoy"] or 0 for r in a_rows),
            "a_daf_count_sum": sum(r["sd_daf_count"] or 0 for r in a_rows),
            "rows_written": len(keep)}


def _count(xs: Iterable) -> dict:
    out: dict = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


# ----------------------------------------------------------------------------- R5 replication (shared by triad, recipients)
def r5_state(np_cache: str) -> dict:
    """Re-run the batch-34 R5 pipeline in memory (mission_market_netting functions, unchanged) and return the netted
    lines per tier plus corrected sponsor-year values (grants, contributions, EOY assets)."""
    import mission_market_netting as mn
    from mission_net_payout import panel_from
    dafrc = read_csv(mn.DAFRC_CSV)
    items = read_csv(mn.CORR_ITEMS)
    panel = panel_from(dafrc)
    corr = mn.corrected_values(dafrc, items)
    assets = {**{(ein9(r["ein"]), int(r["fiscal_year_end"]), "daf_assets_eoy"): num(r["eoy_daf_assets"]) or 0.0 for r in dafrc},
              **{(ein9(r["ein"]), int(r["fiscal_year"]), "daf_assets_eoy"): num(r["corrected_value"]) or 0.0
                 for r in items if r["applied"] == "1" and r["metric"] == "daf_assets_eoy"}}
    shares = mn.cost_shares(read_csv(mn.COST))
    seg_med = lambda seg, k: mn.med([mn.clip01(shares[e][k]) for e in panel if panel[e]["segment"] == seg  # noqa: E731
                                     and e in shares and shares[e][k] is not None]) or 1.0
    defaults = {k: {sg: seg_med(sg, k) for sg in {p["segment"] for p in panel.values()}} for k in ("assets", "grants")}
    chosen = mn.pick_returns(mn.load_np(np_cache))
    lines = mn.panel_lines(chosen, panel)
    decision = {r: mn.recipient_decision(panel[r], shares.get(r)) for r in {l["recipient"] for l in lines}}
    wl = tuple({**l, "w": mn.weights(l, panel, decision, shares, defaults)} for l in lines)
    netted = {t: mn.capped(wl, t, corr) for t in mn.TIERS}
    return {"panel": panel, "corr": {**corr, **assets}, "netted": netted, "lines": lines, "decision": decision,
            "shares": shares, "defaults": defaults, "dafrc": dafrc}


def sum_by(xs: Iterable[Mapping], key, val) -> dict:
    out: dict = {}
    for x in xs:
        k = key(x)
        out[k] = out.get(k, 0.0) + val(x)
    return out


# ----------------------------------------------------------------------------- P-ANL-08 payout triad
TRIAD_FYS = (2021, 2022, 2023, 2024)
MIN_BOY = 1_000_000          # sponsor-level medians use sponsors with >= $1m of BOY DAF assets (small-base ratios are noise)


def triad_rows(st: Mapping) -> tuple[dict, ...]:
    corr, panel, netted = st["corr"], st["panel"], st["netted"]
    out_by = {t: sum_by(netted[t], lambda x: (x["grantor"], x["fy"]), lambda x: x["net_amt"]) for t in netted}
    g = lambda e, fy, m: corr.get((e, fy, m))  # noqa: E731
    def sponsor_years(fy: int, min_boy: float) -> tuple[dict, ...]:
        return tuple({"ein": e, "seg": panel[e]["segment"], "boy": g(e, fy - 1, "daf_assets_eoy"),
                      "grants": g(e, fy, "daf_grants"), **{t: out_by[t].get((e, fy), 0.0) for t in netted}}
                     for e in panel if (g(e, fy - 1, "daf_assets_eoy") or 0) >= min_boy and g(e, fy, "daf_grants") is not None)
    def pct(xs, q):
        xs = sorted(xs)
        return xs[min(len(xs) - 1, int(q * (len(xs) - 1) + 0.5))] if xs else None
    rows = []
    for fy in TRIAD_FYS:
        agg_boy = sum(v for (e, y, m), v in corr.items() if y == fy - 1 and m == "daf_assets_eoy")
        agg_gr = sum(v for (e, y, m), v in corr.items() if y == fy and m == "daf_grants")
        n = {t: sum(x["net_amt"] for x in netted[t] if x["fy"] == fy) for t in netted}
        for scope, min_boy in (("all_sponsors_boy_gt_0", 1.0), ("sponsors_boy_ge_1m", MIN_BOY)):
            sy = sponsor_years(fy, min_boy)
            gross = tuple(s["grants"] / s["boy"] for s in sy)
            for seg in ("all", "national", "community_foundation", "single_issue", "university_hospital", "processor"):
                ss = tuple(s for s in sy if seg == "all" or s["seg"] == seg)
                gr = tuple(s["grants"] / s["boy"] for s in ss)
                ex = tuple(max(s["grants"] - s["central"], 0.0) / s["boy"] for s in ss)
                rows.append({"fiscal_year": fy, "scope": scope, "segment": seg, "sponsor_years": len(ss),
                             "aggregate_gross_payout": agg_gr / agg_boy if seg == "all" else
                             ratio(sum(s["grants"] for s in ss), sum(s["boy"] for s in ss)),
                             "aggregate_ex_daf_to_daf_central": (agg_gr - n["central"]) / agg_boy if seg == "all" else
                             ratio(sum(s["grants"] - s["central"] for s in ss), sum(s["boy"] for s in ss)),
                             "aggregate_ex_daf_to_daf_lower": (agg_gr - n["lower"]) / agg_boy if seg == "all" else None,
                             "aggregate_ex_daf_to_daf_upper": (agg_gr - n["upper"]) / agg_boy if seg == "all" else None,
                             "median_sponsor_gross_payout": median(gr), "median_sponsor_ex_daf_to_daf_central": median(ex),
                             "p25_sponsor_gross_payout": pct(gr, 0.25), "p75_sponsor_gross_payout": pct(gr, 0.75),
                             "share_sponsors_gross_below_5pct": ratio(sum(1 for x in gr if x < 0.05), len(gr)),
                             "share_sponsors_ex_d2d_below_5pct": ratio(sum(1 for x in ex if x < 0.05), len(ex)),
                             "boy_daf_assets": sum(s["boy"] for s in ss) if seg != "all" else agg_boy,
                             "daf_grants": sum(s["grants"] for s in ss) if seg != "all" else agg_gr,
                             "r5_central_outbound": sum(s["central"] for s in ss) if seg != "all" else n["central"],
                             "label": "analysis [C]: repo data, not a filed statistic"})
    return tuple(rows)


def task_triad(a) -> dict:
    st = r5_state(a.np_cache)
    rows = triad_rows(st)
    check = {fy: round(sum(x["net_amt"] for x in st["netted"]["central"] if x["fy"] == fy)) for fy in TRIAD_FYS}
    published = {int(r["fiscal_year"]): int(r["r5_netting_amount"]) for r in read_csv(os.path.join(DATA, "dafrc-market-totals-netted.csv"))
                 if r["metric"] == "daf_grants" and r["tier"] == "central"}
    fields = tuple(rows[0]) + ("sources",)
    src = ("dafrc-sponsor-schedule-d-fy2019-2024.csv + dafrc-corrections-itemized.csv (corrected R1-R4); R5 central lines "
           "re-run in memory with scripts/mission_market_netting.py functions; scripts/mission_batch38_data.py triad")
    write_csv(os.path.join(DATA, OUT["triad"]), [{**r, "sources": src} for r in rows], fields)
    keyrows = [{k: (round(v, 4) if isinstance(v, float) and abs(v) < 10 else v) for k, v in r.items() if k != "label"}
               for r in rows if r["segment"] == "all"]
    return {"r5_central_rebuild": check, "r5_central_published": published, "rows": len(rows), "all_segment_rows": keyrows}


# ----------------------------------------------------------------------------- P-B34A-03 recipient-side check
NAMED_RECIPIENTS = ("200849590",)   # Greater Horizons (named in the queue item; DAFRC type National)


def soi_contrib(soi_dir: str, eins: frozenset) -> dict:
    """(ein, FY) -> Part VIII line 1h total contributions and tax period from the SOI extracts (TY2021+)."""
    out = {}
    for f in ("21eoextract990.csv",) + SOI_FILES:
        for r in read_rows(os.path.join(soi_dir, f)):
            e = ein9(r["ein"])
            if e in eins:
                out[(e, int(r["tax_pd"][:4]))] = {"contrib_1h": num(r.get("totcntrbgfts", "")), "tax_pd": r["tax_pd"]}
    return out


def task_recipients(a) -> dict:
    st = r5_state(a.np_cache)
    panel, corr, netted, lines = st["panel"], st["corr"], st["netted"], st["lines"]
    cent = sum_by(netted["central"], lambda x: x["recipient"], lambda x: x["net_amt"])
    pool = sorted((e for e in cent if panel[e]["segment"] in ("community_foundation", "single_issue")
                   and st["decision"][e][0] == "include"), key=lambda e: -cent[e])[:10]
    targets = tuple(pool) + tuple(e for e in NAMED_RECIPIENTS if e not in pool)
    soi = soi_contrib(a.soi_dir, frozenset(targets))
    fye = lambda e, fy: (panel[e]["fy"].get(fy) or {}).get("end_of_tax_period", "")[5:7]  # noqa: E731
    gross = sum_by(lines, lambda l: (l["recipient"], l["fy"]), lambda l: l["amount"])
    cen_fy = sum_by(netted["central"], lambda x: (x["recipient"], x["fy"]), lambda x: x["net_amt"])
    up_fy = sum_by(netted["upper"], lambda x: (x["recipient"], x["fy"]), lambda x: x["net_amt"])
    mism = sum_by(lines, lambda l: (l["recipient"], l["fy"], fye(l["grantor"], l["fy"]) != fye(l["recipient"], l["fy"])),
                  lambda l: l["amount"])
    out = []
    for e in targets:
        for fy in TRIAD_FYS:
            dc = corr.get((e, fy, "daf_contributions"))
            dc_next = corr.get((e, fy + 1, "daf_contributions"))
            c1h = (soi.get((e, fy)) or {}).get("contrib_1h")
            g = gross.get((e, fy), 0.0)
            out.append({"ein": e, "name": panel[e]["name"], "segment": panel[e]["segment"], "fy": fy, "fye_month": fye(e, fy),
                        "inbound_gross": round(g), "netted_central": round(cen_fy.get((e, fy), 0.0)),
                        "netted_upper": round(up_fy.get((e, fy), 0.0)),
                        "implied_central_weight": ratio(cen_fy.get((e, fy), 0.0), g),
                        "recipient_daf_contributions": dc, "recipient_total_contributions_1h": c1h,
                        "daf_share_of_contributions": ratio(dc, c1h),
                        "daf_share_of_assets_central_weight": (st["shares"].get(e) or {}).get("assets"),
                        "gross_over_daf_contributions_same_fy": ratio(g, dc),
                        "gross_over_daf_contributions_next_fy": ratio(g, dc_next),
                        "gross_over_total_contributions": ratio(g, c1h),
                        "share_of_inbound_from_grantors_with_other_fye": ratio(mism.get((e, fy, True), 0.0), g)})
    def agg(xs, k):
        return sum(x[k] or 0 for x in xs)
    tot = {"inbound_gross": agg(out, "inbound_gross"), "netted_central": agg(out, "netted_central"),
           "netted_upper": agg(out, "netted_upper")}
    by_e = {e: {"name": panel[e]["name"], "fye": fye(e, 2024),
                "gross_fy2021_24": round(sum(r["inbound_gross"] for r in out if r["ein"] == e)),
                "central_fy2021_24": round(sum(r["netted_central"] for r in out if r["ein"] == e)),
                "daf_contrib_fy2021_24": round(sum(r["recipient_daf_contributions"] or 0 for r in out if r["ein"] == e)),
                "total_contrib_1h_fy2021_24": round(sum(r["recipient_total_contributions_1h"] or 0 for r in out if r["ein"] == e)),
                "daf_share_assets": (st["shares"].get(e) or {}).get("assets"),
                "other_fye_share": ratio(sum((r["share_of_inbound_from_grantors_with_other_fye"] or 0) * r["inbound_gross"]
                                             for r in out if r["ein"] == e),
                                         sum(r["inbound_gross"] for r in out if r["ein"] == e))} for e in targets}
    for v in by_e.values():
        v["central_weight"] = ratio(v["central_fy2021_24"], v["gross_fy2021_24"])
        v["daf_share_of_contrib"] = ratio(v["daf_contrib_fy2021_24"], v["total_contrib_1h_fy2021_24"])
        v["gross_over_daf_contrib"] = ratio(v["gross_fy2021_24"], v["daf_contrib_fy2021_24"])
        v["gross_over_total_contrib"] = ratio(v["gross_fy2021_24"], v["total_contrib_1h_fy2021_24"])
    # Alternative recipient weight: swap the recipient's DAF share of assets for its same-FY DAF share of contributions
    alt = sum(r["netted_central"] * min(1.0, r["daf_share_of_contributions"]) / r["daf_share_of_assets_central_weight"]
              for r in out if r["daf_share_of_contributions"] is not None and r["daf_share_of_assets_central_weight"])
    by_fy = {fy: {"central": round(sum(r["netted_central"] for r in out if r["fy"] == fy)),
                  "alt_contrib_share": round(sum(r["netted_central"] * min(1.0, r["daf_share_of_contributions"]) / r["daf_share_of_assets_central_weight"]
                                                 for r in out if r["fy"] == fy and r["daf_share_of_contributions"] is not None
                                                 and r["daf_share_of_assets_central_weight"]))} for fy in TRIAD_FYS}
    return {"targets": by_e, "totals": tot, "alt_central_with_daf_share_of_contributions": round(alt), "alt_by_fy": by_fy,
            "rows": out}


# ----------------------------------------------------------------------------- P-B36A-01 TY2025 index check
TY2025 = (("PPGF", "450931286", "202512"), ("Givinga", "474172718", "202512"), ("Network for Good", "680480736", "202512"),
          ("CAF America", "431634280", "202604"), ("Bright Funds", "BRIGHT FUNDS", "202512"))


def task_accounts(a) -> dict:
    """Newest indexed return per target and whether its TY2025 period (expected period end in col 3) is present."""
    def hit(r, key):
        return ein9(r["ein"]) == key if key.isdigit() else key in (r["taxpayer_name"] or "").upper()
    rows = tuple(r for y in (2024, 2025, 2026) for r in read_rows(os.path.join(a.irs_dir, f"index_{y}.csv"))
                 if any(hit(r, k) for _, k, _ in TY2025))
    req = urllib.request.Request("https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv", method="HEAD", headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            lm = r.headers.get("Last-Modified")
    except (urllib.error.URLError, OSError) as e:
        lm = f"error:{type(e).__name__}"
    out = {}
    for label, key, ty in TY2025:
        mine = sorted((r for r in rows if hit(r, key)), key=lambda r: (r["tax_period"], r["object_id"]))
        out[label] = {"returns": [(r["ein"], r["return_type"], r["tax_period"], r["object_id"]) for r in mine],
                      "ty2025_period": ty, "ty2025_indexed": any(r["tax_period"] >= ty and r["return_type"] == "990" for r in mine)}
    return {"index_2026_last_modified": lm, "targets": out}


# ----------------------------------------------------------------------------- P-B37B-03 MS GIFT
MSGIFT = "527082731"
MS_NUM = {  # extra Part VIII / IX lines beyond batch-37 NUM_FIELDS
    "IncmFromInvestBondProceedsGrp/TotalRevenueColumnAmt": "p8_l4_bond_proceeds_income",
    "RoyaltiesRevenueGrp/TotalRevenueColumnAmt": "p8_l5_royalties",
    "GrossAmountSalesAssetsGrp/SecuritiesAmt": "p8_l7a_sec", "CostOrOtherBasisExpenseSaleGrp/SecuritiesAmt": "p8_l7b_sec",
    "GainOrLossGrp/SecuritiesAmt": "p8_l7c_sec", "InvestmentIncomeGrp/UnrelatedBusinessRevenueAmt": "p8_l3_ubi_col_c",
    "InvestmentIncomeGrp/ExclusionAmt": "p8_l3_excluded_col_d", "InvestmentIncomeGrp/RelatedOrExemptFuncIncomeAmt": "p8_l3_col_b",
    "FeesForServicesOtherGrp/TotalAmt": "p9_l11g_other_fees", "FeesForServicesManagementGrp/TotalAmt": "p9_l11a_mgmt",
    "TotalFunctionalExpensesGrp/TotalAmt": "p9_l25_total", "GrantsToDomesticOrgsGrp/TotalAmt": "p9_l1_grants",
    "InvestmentsPubTradedSecGrp/EOYAmt": "p10_l11_public_securities_eoy", "InvestmentsPubTradedSecGrp/BOYAmt": "p10_l11_public_securities_boy",
    "InvestmentsOtherSecuritiesGrp/EOYAmt": "p10_l12_other_securities_eoy", "CashNonInterestBearingGrp/EOYAmt": "p10_l1_cash_eoy",
    "SavingsAndTempCashInvstGrp/EOYAmt": "p10_l2_savings_eoy", "TotalAssetsGrp/EOYAmt": "p10_l16_total_assets_eoy",
    "TotalAssetsGrp/BOYAmt": "p10_l16_total_assets_boy", "OtherChangesInNetAssetsAmt": "p11_l9_other_changes",
}


def ms_extra(xml: bytes) -> dict:
    root = ET.fromstring(xml)
    def grp(path):
        g, leaf = path.split("/") if "/" in path else (None, path)
        if g is None:
            el = next(root.iter(NS + leaf), None)
            return num(el.text) if el is not None else None
        for e in root.iter(NS + g):
            c = e.find(NS + leaf)
            if c is not None:
                return num(c.text)
        return None
    def items(tag):
        return [{local(c.tag): (c.text or "").strip() for c in g.iter() if len(c) == 0} for g in root.iter(NS + tag)]
    texts = [re.sub(r"\s+", " ", f"[{(g.find(NS + 'FormAndLineReferenceDesc').text if g.find(NS + 'FormAndLineReferenceDesc') is not None else '')}] "
                    f"{(g.find(NS + 'ExplanationTxt').text if g.find(NS + 'ExplanationTxt') is not None else '')}")[:2500]
             for g in root.iter(NS + "SupplementalInformationDetail")]
    return {**{v: grp(k) for k, v in MS_NUM.items()},
            "p8_l11_other_revenue_items": items("OtherRevenueMiscGrp"), "p9_l24_other_expense_items": items("OtherExpensesGrp"),
            "supplemental_texts": texts,
            "accounting_method": {k: grp(k) is not None for k in ("MethodOfAccountingAccrualInd", "MethodOfAccountingCashInd")},
            "fs_audited": {k: (next(root.iter(NS + k)).text if next(root.iter(NS + k), None) is not None else "")
                           for k in ("FSAuditedInd", "FSAuditedBasisGrp", "ConsolidatedAuditFinclStmtInd", "IndependentAccountantFinclStmtInd",
                                     "AccountantCompileOrReviewInd")}}


def task_msgift(a) -> dict:
    idx = load_index(a.irs_dir, frozenset({MSGIFT}), types=("990", "990T"))
    out = {}
    for f in idx.get(MSGIFT, ()):
        if f["tax_period"] < "202112":
            continue
        xml = full_xml(f, a.work_dir, a.fetch)
        key = f"{f['return_type']}_{f['tax_period']}"
        if not xml:
            out[key] = {"object_id": f["object_id"], "status": "not_read"}
            continue
        base = {"object_id": f["object_id"], "xml_url": XML_URL.format(oid=f["object_id"])}
        if f["return_type"] == "990T":
            root = ET.fromstring(xml)
            leaves = [(local(e.tag), re.sub(r"\s+", " ", e.text)[:600]) for e in root.iter() if len(e) == 0 and e.text and e.text.strip()]
            out[key] = {**base, "leaves": leaves[:400]}
        else:
            out[key] = {**base, **read_return(xml, ("investment_income_booking", "advisor_managed")), **ms_extra(xml)}
    return out


# ----------------------------------------------------------------------------- P-LND-04 per-head vs per-FTE pay
# Public FTE evidence found for the 20 sponsors (2026-11-15). Audited statements read (NCF FY2025, Vanguard Charitable
# FY2025-26, FFTC 2025, NPT FY2025 summary, RCF 2024, Fidelity Charitable FY2024-25) state no headcount or FTE.
# Values below are what the cited text says; [S] = search-index / third-party text, not verified on a first-party page.
FTE_EVIDENCE: dict[str, tuple[str, str, str]] = {   # ein -> (fte_value, label, source)
    "237825575": ("235", "S", "job-board copy of NPT recruiting text: 'more than 235 fulltime employees across 18 states in the U.S. and "
                  "more than 10 employees in the United Kingdom' (undated; not on nptrust.org/contact-us/work-at-npt/ as fetched 2026-11-15)"),
    "133615533": ("45", "S", "fiscalsponsordirectory.org listing: '45 full-time staff' (undated, pre-2024; RPA reported staff cuts in Feb 2025)"),
}
PAID_OFFICER = re.compile(r"Officer|KeyEmployee|HighestCompensated|IndividualTrustee", re.I)


def part_vii(xml: bytes) -> dict:
    """Part VII Section A: persons with reportable compensation from the organisation (> 0), split into officers /
    key employees / highest-compensated employees vs trustees only."""
    root = ET.fromstring(xml)
    people = []
    for g in root.iter(NS + "Form990PartVIISectionAGrp"):
        comp = num((g.find(NS + "ReportableCompFromOrgAmt").text if g.find(NS + "ReportableCompFromOrgAmt") is not None else "") or "")
        roles = {local(c.tag) for c in g if local(c.tag).endswith("Ind") and (c.text or "").strip().upper() in ("X", "TRUE", "1")}
        avg_h = num((g.find(NS + "AverageHoursPerWeekRt").text if g.find(NS + "AverageHoursPerWeekRt") is not None else "") or "")
        people.append({"comp": comp or 0.0, "roles": roles, "hours": avg_h})
    paid = tuple(p for p in people if p["comp"] > 0)
    staff_paid = tuple(p for p in paid if p["roles"] & {"OfficerInd", "KeyEmployeeInd", "HighestCompensatedEmployeeInd"})
    return {"part_vii_listed": len(people), "part_vii_paid": len(paid), "part_vii_paid_staff": len(staff_paid),
            "part_vii_paid_staff_comp": sum(p["comp"] for p in staff_paid),
            "part_vii_paid_lt_35h": sum(1 for p in staff_paid if p["hours"] is not None and p["hours"] < 35)}


def task_fte(a) -> dict:
    rows = tuple(r for r in read_csv(os.path.join(DATA, "sponsor-salary-per-employee.csv")) if r["record_type"] == "return")
    best: dict[str, dict] = {}
    for r in rows:
        if r["ein"] not in best or (r["fiscal_year"], r["return_object_id"]) > (best[r["ein"]]["fiscal_year"], best[r["ein"]]["return_object_id"]):
            best[r["ein"]] = r
    pool = sorted((r for r in best.values() if not r["category"].startswith("SingleIssue")), key=lambda r: -(num(r["employees"]) or 0))[:20]
    out = []
    for r in pool:
        f = {"object_id": r["return_object_id"], "index_year": 0, "batch": ""}
        xml = full_xml(f, a.work_dir, a.fetch)
        p7 = part_vii(xml) if xml else {}
        emp = num(r["employees"]) or 0
        l5, l7 = num(r["l05_comp_officers_directors"]) or 0.0, num(r["l07_other_salaries_wages"]) or 0.0
        non_off = emp - p7.get("part_vii_paid_staff", 0) if p7 else None
        fte = FTE_EVIDENCE.get(r["ein"])
        wages = l5 + l7
        out.append({"ein": r["ein"], "sponsor_name": r["sponsor_name"], "category": r["category"], "fiscal_year": r["fiscal_year"],
                    "employees_part_i_l5": emp, "l05_comp_officers_directors": l5, "l07_other_salaries_wages": l7,
                    "loaded_l5_10": num(r["loaded_l5_10"]), "wage_all_per_head": ratio(wages, emp),
                    "loaded_all_per_head": ratio(num(r["loaded_l5_10"]), emp),
                    **p7, "non_officer_heads": non_off,
                    "non_officer_wage_per_head": ratio(l7, non_off) if non_off and non_off > 0 else None,
                    "officer_avg_comp_part_vii": ratio(p7.get("part_vii_paid_staff_comp"), p7.get("part_vii_paid_staff")) if p7 else None,
                    "fte_public": fte[0] if fte else "", "fte_label": fte[1] if fte else "U", "fte_source": fte[2] if fte else
                    "no public FTE figure found (audits read state none; search-index results were third-party estimates only)",
                    "wage_all_per_fte": ratio(wages, num(fte[0])) if fte else None,
                    "loaded_all_per_fte": ratio(num(r["loaded_l5_10"]), num(fte[0])) if fte else None,
                    "fte_to_head_ratio": ratio(num(fte[0]), emp) if fte else None,
                    "flags": r["flags"], "return_object_id": r["return_object_id"],
                    "xml_url": XML_URL.format(oid=r["return_object_id"])})
    fields = tuple(out[0])
    write_csv(os.path.join(DATA, OUT["fte"]), out, fields)
    return {"rows": len(out), "with_public_fte": sum(1 for o in out if o["fte_public"]),
            "summary": [{k: (round(v) if isinstance(v, float) else v) for k, v in o.items()
                         if k in ("sponsor_name", "fiscal_year", "employees_part_i_l5", "part_vii_paid_staff", "wage_all_per_head",
                                  "non_officer_wage_per_head", "officer_avg_comp_part_vii", "fte_public", "wage_all_per_fte", "flags")}
                        for o in out]}


# ----------------------------------------------------------------------------- CLI
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", choices=("fulltext", "triad", "recipients", "msgift", "fte", "accounts"))
    ap.add_argument("--irs-dir", default="IRS")
    ap.add_argument("--soi-dir", default="SOI")
    ap.add_argument("--work-dir", default="WORK")
    ap.add_argument("--np-cache", default="NPCACHE", help="dir holding netpayout990/ (mission_net_payout.py cache)")
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    print(json.dumps(globals()[f"task_{a.task}"](a), indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
