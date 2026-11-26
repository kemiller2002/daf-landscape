#!/usr/bin/env python3
"""Queue batch 35 A panel screens (stdlib only, functional style: pure transforms, I/O at the edges).

Queue items (data/mission-2026-11-14/research-priority-queue.csv):
  P-B34A-01  fill the 144 xml_status=http_404 rows of form990-returns-schedule-d-harvest-full.csv from the
             IRS 2026 TEOS zips (HTTP range reads of single members; the index label '05A' also covers 05B)
             -> data/mission-2026-11-14/form990-harvest-2026-fill.csv (new file; the harvest is not overwritten)
  P-B34B-01  workplace pass-through DAF reclassification screen: sharp drops in Schedule D Part I DAF account
             counts with stable grants, or account shifts into the 'funds and other accounts' column
             -> data/mission-2026-11-14/daf-reclassification-screen.csv
  P-B34B-02  public-support cliff screen: Schedule A Part II (or III) public-support % for DAF sponsors with few
             accounts and large balances -> data/mission-2026-11-14/public-support-cliff-screen.csv
  P-STF-02   Fidelity Charitable FY2025 and Vanguard Charitable FY2025 Schedule I lines to DAF sponsors, with the
             counterpart sponsor's own filed figures -> data/mission-2026-11-14/daf-to-daf-fy2025-counterparts.csv

Sources
  * IRS TEOS index https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv (2021-2026)
  * IRS e-file XML, GivingTuesday mirror https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OID}_public.xml
  * IRS 2026 TEOS zips https://apps.irs.gov/pub/epostcard/990/xml/2026/{BATCH}.zip (range reads; members are Deflate64,
    inflated with `unzip -p`)
  * Repo inputs: dafrc-sponsor-schedule-d-fy2019-2024.csv, form990-returns-schedule-d-harvest-full.csv,
    dafrc-corrected-market-totals.csv, daf-to-daf-flows-990.csv; caches of mission_990_contractors.py
    (extract990/) and mission_net_payout.py (netpayout990/).

Usage
  python3 scripts/mission_batch35_screens.py --irs-dir IRS --work-dir WORK --np-cache NP1 [--np-cache NP2] [--fetch]
  IRS holds index_2021.csv .. index_2026.csv. WORK receives the XML-extract cache (ext/), TEOS members (teos/) and
  zip central directories (zipcd/). Without --fetch only cached extracts are used.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import (  # noqa: E402  (reuse, no duplication)
    DAFRC_CSV, DATA, NS, XML_URL, _group_by_fast, ein9, load_index, local, num, read_csv,
    return_row, text_of, write_csv)
from mission_990_contractors import extract_stream as harvest_extract  # noqa: E402

HARVEST_FULL = os.path.join(DATA, "form990-returns-schedule-d-harvest-full.csv")
CORRECTED = os.path.join(DATA, "dafrc-corrected-market-totals.csv")
D2D_FLOWS = os.path.join(DATA, "daf-to-daf-flows-990.csv")
WHITELIST = os.path.join(DATA, "daf-to-daf-recipient-whitelist.csv")
OUT = {"fill": "form990-harvest-2026-fill.csv", "reclass": "daf-reclassification-screen.csv",
       "support": "public-support-cliff-screen.csv", "d2d": "daf-to-daf-fy2025-counterparts.csv"}
TEOS_ZIP = "https://apps.irs.gov/pub/epostcard/990/xml/2026/{batch}.zip"
INDEX_YEARS = tuple(range(2021, 2027))
SCREEN_FYS = tuple(range(2021, 2027))           # FY = calendar year in which the tax period ends (DAFRC convention)
UA = {"User-Agent": "research-script/1.0 (stdlib urllib)"}
EXT_VERSION = 1
WORKERS = int(os.environ.get("MISSION990_WORKERS", "12"))

# Workplace / checkout intermediaries named in P-B34B-01 (EINs from pass-through-sponsors-2026.csv and batch 34 B)
NAMED_PASS_THROUGH = {"810739440": "AOGF (Benevity)", "431634280": "CAF America", "450931286": "PayPal Giving Fund",
                      "460942102": "Blackbaud Giving Fund", "680480736": "Network for Good",
                      "462109112": "Bright Funds Foundation", "474172718": "Givinga Foundation",
                      "873165286": "Percent Impact Foundation (Goodstack US)"}
FIDELITY, VANGUARD, AYCO, GS_DAPF = "110303001", "232888152", "141782466", "311774905"
JASPER_RIDGE = "472088631"

# Screen thresholds (judgement; documented in the report)
RECLASS_MIN_PREV_COUNT = 100        # prior-year DAF accounts
RECLASS_MAX_COUNT_RATIO = 0.5       # current / prior DAF accounts
RECLASS_GRANT_BAND = (0.5, 2.0)     # current / prior DAF grants = "stable"
RECLASS_SHIFT_SHARE = 0.5           # other-funds account increase / DAF account drop
RECLASS_SHIFT_MAX_RATIO = 0.75      # a column shift counts only if DAF accounts fell by at least a quarter
U1_MIN_COUNT = 500                  # sponsors whose full FY2021-26 filed series is parsed for the reclass screen
CLIFF_MAX_COUNT, CLIFF_MIN_EOY, CLIFF_AVG = 50, 10_000_000, 10_000_000
THIRD = 1 / 3
NEAR_BAND = 0.40
DROP_PTS = 0.10

SCHED_D = {"DonorAdvisedFundsHeldCnt": "daf_count", "FundsAndOtherAccountsHeldCnt": "other_count",
           "DonorAdvisedFundsContriAmt": "daf_contributions", "FundsAndOtherAccountsContriAmt": "other_contributions",
           "DonorAdvisedFundsGrantsAmt": "daf_grants", "FundsAndOtherAccountsGrantsAmt": "other_grants",
           "DonorAdvisedFundsVlEOYAmt": "daf_eoy", "FundsAndOtherAccountsVlEOYAmt": "other_eoy"}
SCHED_A_NUM = ("PublicSupportCY170Pct", "PublicSupportPY170Pct", "PublicSupportCY509Pct", "PublicSupportPY509Pct",
               "InvestmentIncomeCYPct", "InvestmentIncomePYPct", "PublicSupportTotal170Amt", "TotalSupportAmt",
               "SubstantialContributorsTotAmt")
DAF_TEXT = re.compile(r"donor[- ]advised|\bDAFs?\b|micro-?donation|workplace|employee (?:giving|donation)|"
                      r"pass[- ]through|giving account|charitable account", re.I)
LATE_SCHEDULE = re.compile(r"IRS990Schedule([E-Z])$")


# ----------------------------------------------------------------------------- small pure helpers
def f(x) -> float | None:
    return num(x) if x not in (None, "") else None


def ratio(a, b) -> float | None:
    return a / b if a is not None and b not in (None, 0) else None


def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else f"{v:.6g}"
    return str(v)


def rows_fmt(rows: Iterable[Mapping]) -> tuple[dict, ...]:
    return tuple({k: fmt(v) for k, v in r.items()} for r in rows)


# ----------------------------------------------------------------------------- TEOS zip range reader (from batch 34)
def http_range(url: str, a: int, b: int, retries: int = 3) -> bytes:
    req = urllib.request.Request(url, headers={**UA, "Range": f"bytes={a}-{b}"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            if attempt == retries:
                raise
            time.sleep(3 * (attempt + 1))
    return b""


def http_size(url: str) -> int:
    req = urllib.request.Request(url, method="HEAD", headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers["Content-Length"])


def parse_central_dir(cd: bytes) -> dict:
    def entries(p: int):
        while p < len(cd) and cd[p:p + 4] == b"PK\x01\x02":
            meth, = struct.unpack("<H", cd[p + 10:p + 12])
            crc, csz, usz = struct.unpack("<III", cd[p + 16:p + 28])
            fl, el, cl = struct.unpack("<HHH", cd[p + 28:p + 34])
            lho, = struct.unpack("<I", cd[p + 42:p + 46])
            name = cd[p + 46:p + 46 + fl].decode("utf-8", "replace")
            extra = cd[p + 46 + fl:p + 46 + fl + el]
            usz, csz, lho = zip64(extra, usz, csz, lho)
            yield name, {"method": meth, "crc": crc, "csize": csz, "usize": usz, "offset": lho}
            p += 46 + fl + el + cl
    return dict(entries(0))


def zip64(extra: bytes, usz: int, csz: int, lho: int) -> tuple[int, int, int]:
    q = 0
    while q + 4 <= len(extra):
        hid, hl = struct.unpack("<HH", extra[q:q + 4])
        if hid == 1:
            vals, k = extra[q + 4:q + 4 + hl], 0
            if usz == 0xFFFFFFFF:
                usz, = struct.unpack("<Q", vals[k:k + 8]); k += 8
            if csz == 0xFFFFFFFF:
                csz, = struct.unpack("<Q", vals[k:k + 8]); k += 8
            if lho == 0xFFFFFFFF:
                lho, = struct.unpack("<Q", vals[k:k + 8]); k += 8
        q += 4 + hl
    return usz, csz, lho


def central_directory(url: str, cache_dir: str) -> dict:
    path = os.path.join(cache_dir, re.sub(r"\W", "_", url.rsplit("/", 1)[-1]) + ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    n = http_size(url)
    tail = http_range(url, n - 65536 - 22, n - 1)
    i = tail.rfind(b"PK\x05\x06")
    cd_size, cd_off = struct.unpack("<II", tail[i + 12:i + 20])
    j = tail.rfind(b"PK\x06\x06")
    if j >= 0:
        _, cd_size, cd_off = struct.unpack("<QQQ", tail[j + 32:j + 56])
    members = parse_central_dir(http_range(url, cd_off, cd_off + cd_size - 1))
    out = {"url": url, "size": n, "members": members}
    os.makedirs(cache_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh)
    return out


def member_xml(url: str, name: str, m: Mapping, tmp_dir: str) -> bytes:
    """Fetch one member's compressed bytes and inflate it via a one-member zip (unzip handles Deflate64)."""
    lh = http_range(url, m["offset"], m["offset"] + 30 + 1024)
    fl, el = struct.unpack("<HH", lh[26:30])
    start = m["offset"] + 30 + fl + el
    data = http_range(url, start, start + m["csize"] - 1)
    nb = name.encode()
    local_h = struct.pack("<4sHHHHHIIIHH", b"PK\x03\x04", 45, 0, m["method"], 0, 0, m["crc"], m["csize"], m["usize"],
                          len(nb), 0) + nb
    cen = struct.pack("<4sHHHHHHIIIHHHHHII", b"PK\x01\x02", 45, 45, 0, m["method"], 0, 0, m["crc"], m["csize"],
                      m["usize"], len(nb), 0, 0, 0, 0, 0, 0) + nb
    eocd = struct.pack("<4sHHHHIIH", b"PK\x05\x06", 0, 0, 1, 1, len(cen), len(local_h) + len(data), 0)
    tmp = os.path.join(tmp_dir, f"one_{os.getpid()}_{abs(hash(name))}.zip")
    with open(tmp, "wb") as fh:
        fh.write(local_h + data + cen + eocd)
    try:
        return subprocess.run(["unzip", "-p", tmp], capture_output=True, check=True).stdout
    finally:
        os.remove(tmp)


def batch_zips(label: str) -> tuple[str, ...]:
    """The index label 'YYYY_TEOS_XML_05A' can point to the 05A or the 05B zip (batch 31/34 finding)."""
    return tuple(TEOS_ZIP.format(batch=b) for b in (label, label[:-1] + "B")) if label.endswith("A") else (TEOS_ZIP.format(batch=label),)


def teos_fetch(oid: str, label: str, work_dir: str) -> dict:
    """Locate and save {oid}_public.xml from the TEOS zip(s) for its index label. Returns provenance."""
    out_path = os.path.join(work_dir, "teos", f"{oid}_public.xml")
    meta_path = out_path + ".meta.json"
    if os.path.exists(out_path) and os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as fh:
            return json.load(fh)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    for url in batch_zips(label):
        try:
            cd = central_directory(url, os.path.join(work_dir, "zipcd"))
        except urllib.error.HTTPError as e:
            if e.code in (302, 403, 404):
                continue
            raise
        name = next((k for k in cd["members"] if k.endswith(f"{oid}_public.xml")), None)
        if name:
            m = cd["members"][name]
            xml = member_xml(url, name, m, os.path.dirname(out_path))
            with open(out_path, "wb") as fh:
                fh.write(xml)
            meta = {"status": "ok", "zip": url, "member": name, "compressed_bytes": m["csize"], "xml_bytes": len(xml)}
            with open(meta_path, "w", encoding="utf-8") as fh:
                json.dump(meta, fh)
            return meta
    return {"status": "not_in_zips", "zip": " | ".join(batch_zips(label)), "member": "", "compressed_bytes": None,
            "xml_bytes": None}


# ----------------------------------------------------------------------------- extended XML extract
def direct_leaves(el) -> dict:
    return {local(c.tag): (c.text or "").strip() for c in el if len(c) == 0}


def sched_a(el) -> dict:
    leaves = direct_leaves(el)
    inds = sorted(k for k, v in leaves.items() if k.endswith("Ind") and v.upper() in ("X", "1", "TRUE"))
    return {"sched_a_present": 1, "sched_a_inds": ";".join(inds),
            **{k: num(leaves.get(k, "")) for k in SCHED_A_NUM}}


def sched_d(el) -> dict:
    leaves = direct_leaves(el)
    return {"sched_d_present": 1, **{v: num(leaves.get(k, "")) for k, v in SCHED_D.items()}}


def sched_o(el) -> dict:
    hits = tuple(f"[{text_of(g, ('FormAndLineReferenceDesc',))}] {re.sub(chr(10), ' ', text_of(g, ('ExplanationTxt',)))[:900]}"
                 for g in el.iter(NS + "SupplementalInformationDetail")
                 if DAF_TEXT.search(text_of(g, ("ExplanationTxt",))))
    return {"sched_o_daf_text": " || ".join(hits)[:4000]}


def extract_ext(stream, full: bool) -> dict:
    """Header, Part I/X basics, Schedule A (support test), Schedule D Part I both columns; with full=True also
    Schedule O passages that mention DAFs / micro-donations / workplace giving."""
    out: dict = {"sched_a_present": 0, "sched_d_present": 0}
    for event, el in ET.iterparse(stream, events=("start", "end")):
        tag = local(el.tag)
        if event == "start":
            if not full and LATE_SCHEDULE.match(tag) and "return_ts" in out:
                break
            continue
        if tag == "ReturnHeader":
            out.update({"tax_period_end": text_of(el, ("TaxPeriodEndDt",)), "return_ts": text_of(el, ("ReturnTs",)),
                        "return_type": text_of(el, ("ReturnTypeCd",)), "filer_ein": text_of(el, ("Filer", "EIN")),
                        "filer_name": text_of(el, ("Filer", "BusinessName", "BusinessNameLine1Txt"))})
            el.clear()
        elif tag == "IRS990":
            out.update({"amended_ind": text_of(el, ("AmendedReturnInd",)),
                        "total_assets_eoy": num(text_of(el, ("TotalAssetsGrp", "EOYAmt"))),
                        "cy_grants_paid": num(text_of(el, ("CYGrantsAndSimilarPaidAmt",))),
                        "cy_total_revenue": num(text_of(el, ("CYTotalRevenueAmt",))),
                        "cy_contributions": num(text_of(el, ("CYContributionsGrantsAmt",)))})
            el.clear()
        elif tag == "IRS990ScheduleA":
            out.update(sched_a(el)); el.clear()
        elif tag == "IRS990ScheduleD":
            out.update(sched_d(el)); el.clear()
        elif tag == "IRS990ScheduleO":
            out.update(sched_o(el)); el.clear()
        elif tag.startswith("IRS990Schedule") or tag in ("RecipientTable", "GrantsOtherAsstToIndivInUSGrp"):
            el.clear()
    return out


def ext_cache_path(work_dir: str, oid: str, full: bool) -> str:
    return os.path.join(work_dir, "ext", f"{oid}{'_full' if full else ''}.json")


def fetch_ext(oid: str, work_dir: str, fetch: bool, full: bool = False) -> dict:
    path = ext_cache_path(work_dir, oid, full)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == EXT_VERSION:
            return c
    teos = os.path.join(work_dir, "teos", f"{oid}_public.xml")
    if os.path.exists(teos):
        with open(teos, "rb") as fh:
            res = {**extract_ext(fh, full), "xml_status": "ok", "xml_source": "teos_zip"}
    elif not fetch:
        return {"xml_status": "not_fetched"}
    else:
        res = mirror_ext(oid, full)
    res = {**res, "_v": EXT_VERSION, "object_id": oid}
    if not res["xml_status"].startswith("error"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(res, fh)
    return res


def mirror_ext(oid: str, full: bool, retries: int = 2) -> dict:
    req = urllib.request.Request(XML_URL.format(oid=oid), headers=UA)
    out = {"xml_status": "error:none"}
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return {**extract_ext(resp, full), "xml_status": "ok", "xml_source": "gt_mirror"}
        except urllib.error.HTTPError as e:
            out = {"xml_status": f"http_{e.code}"}
            if e.code in (403, 404):
                return out
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
            out = {"xml_status": f"error:{type(e).__name__}"}
            time.sleep(2 * (attempt + 1))
    return out


def fetch_many(oids: Sequence[str], work_dir: str, fetch: bool, full: bool = False) -> dict[str, dict]:
    uniq = tuple(dict.fromkeys(oids))
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        res = tuple(ex.map(lambda o: fetch_ext(o, work_dir, fetch, full), uniq))
    return dict(zip(uniq, res))


def batch_labels(index_2026: str, oids: frozenset) -> dict[str, str]:
    with open(index_2026, newline="", encoding="latin-1") as fh:
        return {d["OBJECT_ID"]: d.get("XML_BATCH_ID", "") for d in csv.DictReader(fh) if d["OBJECT_ID"] in oids}


def resolve_404s(exts: Mapping[str, dict], labels: Mapping[str, str], work_dir: str, fetch: bool) -> dict[str, dict]:
    """Returns not on the mirror but indexed in 2026: range-read from TEOS zips, then re-extract."""
    missing = tuple(o for o, e in exts.items() if e.get("xml_status") == "http_404" and o in labels)
    if not fetch or not missing:
        return dict(exts)
    for o in missing:
        os.remove(ext_cache_path(work_dir, o, False)) if os.path.exists(ext_cache_path(work_dir, o, False)) else None
        teos_fetch(o, labels[o], work_dir)
    return {**exts, **{o: fetch_ext(o, work_dir, fetch) for o in missing}}


# ----------------------------------------------------------------------------- panel inputs
def panel_meta(dafrc: Sequence[Mapping]) -> dict[str, dict]:
    by = _group_by_fast(dafrc, lambda r: ein9(r["ein"]))
    return {e: {"name": max(v, key=lambda r: r["fiscal_year_end"])["name"], "type": v[0]["type"], "subtype": v[0]["subtype"],
                "operating_status": max(v, key=lambda r: r["fiscal_year_end"])["operating_status"]} for e, v in by.items()}


def dafrc_points(dafrc: Sequence[Mapping]) -> dict[tuple, dict]:
    return {(ein9(r["ein"]), int(r["fiscal_year_end"])):
            {"daf_count": f(r["number_of_daf_accounts"]), "daf_contributions": f(r["total_daf_contributions"]),
             "daf_grants": f(r["total_daf_grants"]), "daf_eoy": f(r["eoy_daf_assets"]),
             "source": "dafrc:" + (r["source_number_of_accounts"] or "blank"),
             "imputed": "Imputed" in (r["source_number_of_accounts"], r["source_total_daf_grants"]), "object_id": ""}
            for r in dafrc if int(r["fiscal_year_end"]) >= min(SCREEN_FYS)}


def harvest_points(rows: Sequence[Mapping]) -> dict[tuple, dict]:
    return {(ein9(r["ein"]), int(r["fiscal_year"])):
            {"daf_count": f(r["sched_d_daf_count"]), "daf_contributions": f(r["sched_d_daf_contributions"]),
             "daf_grants": f(r["sched_d_daf_grants"]), "daf_eoy": f(r["sched_d_daf_eoy_value"]),
             "source": "harvest_filed", "imputed": False, "object_id": r["return_object_id"]}
            for r in rows if r.get("xml_status", "").startswith("ok") and r.get("sched_d_present") in ("1", 1)}


def ext_points(chosen: Mapping[tuple, dict], exts: Mapping[str, dict]) -> dict[tuple, dict]:
    def pt(k, filing):
        e = exts.get(filing["object_id"], {})
        if e.get("xml_status") != "ok" or not e.get("sched_d_present"):
            return None
        return {**{v: e.get(v) for v in SCHED_D.values()}, "source": "filed_xml", "imputed": False,
                "object_id": filing["object_id"], "total_assets_eoy": e.get("total_assets_eoy")}
    pts = {k: pt(k, v) for k, v in chosen.items()}
    return {k: v for k, v in pts.items() if v}


def candidate_filings(index: Mapping[str, Sequence[dict]], eins: Iterable[str]) -> tuple[dict, ...]:
    """Every 990 submission for a tax period ending in SCREEN_FYS (originals and amendments)."""
    return tuple(fl for e in eins for fl in index.get(e, ())
                 if fl["return_type"] == "990" and int(fl["tax_period"][:4]) in SCREEN_FYS)


def chosen_filings(cands: Sequence[dict], exts: Mapping[str, dict]) -> dict[tuple, dict]:
    """Latest submission per (ein, FY) by the return's own ReturnTs (object ids are not chronological across
    batches: Givinga's CY2024 amendment 202503179349301975 sorts below its original 202522379349301497)."""
    def key(fl):
        e = exts.get(fl["object_id"], {})
        return (e.get("xml_status") == "ok", e.get("return_ts", ""), fl["object_id"])
    by = _group_by_fast(cands, lambda fl: (fl["ein"], int(fl["tax_period"][:4])))
    return {k: max(v, key=key) for k, v in by.items()}


def best_series(*layers: Mapping[tuple, dict]) -> dict[tuple, dict]:
    """Later layers win where they carry a DAF count or grants."""
    out: dict = {}
    for layer in layers:
        out.update({k: v for k, v in layer.items() if v.get("daf_count") is not None or v.get("daf_grants") is not None})
    return out


# ----------------------------------------------------------------------------- P-B34B-01 reclassification screen
def reclass_pairs(series: Mapping[tuple, dict], meta: Mapping[str, dict]) -> tuple[dict, ...]:
    def row(e, fy, p, c):
        pc, cc = p.get("daf_count"), c.get("daf_count")
        drop = (pc or 0) - (cc or 0)
        shift = ((c.get("other_count") or 0) - (p.get("other_count") or 0)) if c.get("other_count") is not None else None
        gr = ratio(c.get("daf_grants"), p.get("daf_grants"))
        comb = ratio((c.get("daf_grants") or 0) + (c.get("other_grants") or 0),
                     (p.get("daf_grants") or 0) + (p.get("other_grants") or 0))
        sharp = pc is not None and pc >= RECLASS_MIN_PREV_COUNT and cc is not None and cc <= RECLASS_MAX_COUNT_RATIO * pc
        stable = gr is not None and RECLASS_GRANT_BAND[0] <= gr <= RECLASS_GRANT_BAND[1]
        shifted = (shift is not None and drop > 0 and pc is not None and pc >= RECLASS_MIN_PREV_COUNT
                   and cc is not None and cc <= RECLASS_SHIFT_MAX_RATIO * pc and shift >= RECLASS_SHIFT_SHARE * drop)
        if not ((sharp and stable) or shifted):
            return None
        m = meta.get(e, {})
        return {"ein": e, "sponsor_name": m.get("name") or NAMED_PASS_THROUGH.get(e, ""), "dafrc_type": m.get("type", ""),
                "dafrc_subtype": m.get("subtype", ""), "named_pass_through": NAMED_PASS_THROUGH.get(e, ""),
                "fy_prev": fy - 1, "fy_cur": fy, "source_prev": p["source"], "source_cur": c["source"],
                "object_id_prev": p.get("object_id", ""), "object_id_cur": c.get("object_id", ""),
                "daf_count_prev": pc, "daf_count_cur": cc, "daf_count_drop": drop, "daf_count_ratio": ratio(cc, pc),
                "daf_grants_prev": p.get("daf_grants"), "daf_grants_cur": c.get("daf_grants"), "daf_grants_ratio": gr,
                "daf_contributions_prev": p.get("daf_contributions"), "daf_contributions_cur": c.get("daf_contributions"),
                "daf_eoy_prev": p.get("daf_eoy"), "daf_eoy_cur": c.get("daf_eoy"),
                "other_count_prev": p.get("other_count"), "other_count_cur": c.get("other_count"),
                "other_grants_prev": p.get("other_grants"), "other_grants_cur": c.get("other_grants"),
                "other_count_shift": shift, "combined_grants_ratio": comb if c.get("other_count") is not None else None,
                "flag_sharp_drop_stable_grants": int(sharp and stable), "flag_column_shift": int(bool(shifted)),
                "imputed_value_involved": int(bool(p.get("imputed") or c.get("imputed"))),
                "mixed_sources": int(p["source"].split(":")[0] != c["source"].split(":")[0])}
    keys = sorted(series)
    rows = (row(e, fy, series[(e, fy - 1)], series[(e, fy)]) for e, fy in keys if (e, fy - 1) in series)
    return tuple(r for r in rows if r)


def classify_reclass(r: Mapping) -> str:
    if r["daf_count_cur"] == 0 and not r["daf_eoy_cur"]:
        return "terminated_or_merged"
    if r["flag_column_shift"]:
        return "reclassified_to_other_funds_column"
    if r["imputed_value_involved"]:
        return "artifact_imputed_value"
    if r["mixed_sources"]:
        return "artifact_check_mixed_sources"
    return "count_basis_change_no_column_shift"


def market_effect(rows: Sequence[Mapping], corrected: Sequence[Mapping], dafrc: Sequence[Mapping],
                  series: Mapping[tuple, dict], meta: Mapping[str, dict]) -> dict:
    acc = {int(r["fiscal_year"]): f(r["corrected_value"]) for r in corrected if r["metric"] == "daf_accounts_eoy"}
    grants = {int(r["fiscal_year"]): f(r["corrected_value"]) for r in corrected if r["metric"] == "daf_grants"}
    real = tuple(r for r in rows if r["classification"] == "reclassified_to_other_funds_column")
    proc24 = tuple(r for r in dafrc if r["fiscal_year_end"] == "2024" and r["subtype"] == "Donation Processor")
    named_latest = {e: max(((fy, v) for (x, fy), v in series.items() if x == e), default=(None, {}))
                    for e in NAMED_PASS_THROUGH}
    aogf24, aogf26 = series.get(("810739440", 2024), {}), series.get(("810739440", 2026), {})
    oshare = ratio(aogf26.get("other_grants"), (aogf26.get("daf_grants") or 0) + (aogf26.get("other_grants") or 0))
    acc_rm = (aogf24.get("daf_count") or 0) - (aogf26.get("daf_count") or 0)
    gr_rm = (aogf24.get("daf_grants") or 0) * (oshare or 0)
    micro = tuple(e for e in ("474172718", "810739440", "450931286"))
    micro_acc = sum(series.get((e, 2024), {}).get("daf_count") or 0 for e in micro)
    scenarios = {
        "aogf_fy2026_basis_applied_to_fy2024": {
            "aogf_fy2024_accounts": aogf24.get("daf_count"), "aogf_fy2026_daf_accounts": aogf26.get("daf_count"),
            "accounts_removed": acc_rm, "restated_fy2024_accounts": (acc.get(2024) or 0) - acc_rm,
            "accounts_change_pct": ratio(-acc_rm, acc.get(2024)), "aogf_fy2026_other_share_of_grants": oshare,
            "grants_removed": gr_rm, "restated_fy2024_grants": (grants.get(2024) or 0) - gr_rm,
            "grants_change_pct": ratio(-gr_rm, grants.get(2024))},
        "micro_account_processors_fy2024": {
            "eins": micro, "accounts": micro_acc, "share_of_corrected_accounts": ratio(micro_acc, acc.get(2024)),
            "accounts_excluding_them": (acc.get(2024) or 0) - micro_acc}}
    return {"corrected_accounts": acc, "corrected_grants": grants, "scenarios": scenarios,
            "reclassified_rows": [{"ein": r["ein"], "name": r["sponsor_name"], "fy": r["fy_cur"],
                                   "accounts_moved": r["other_count_shift"], "daf_count_drop": r["daf_count_drop"],
                                   "grants_in_other_column_cur": r["other_grants_cur"],
                                   "share_of_fy2024_corrected_accounts": ratio(r["daf_count_drop"], acc.get(2024)),
                                   "other_grants_share_of_fy2024_corrected_grants": ratio(r["other_grants_cur"], grants.get(2024))}
                                  for r in real],
            "dafrc_fy2024_donation_processor": {"sponsors": len(proc24),
                                                "accounts": sum(f(r["number_of_daf_accounts"]) or 0 for r in proc24),
                                                "grants": sum(f(r["total_daf_grants"]) or 0 for r in proc24),
                                                "accounts_share": ratio(sum(f(r["number_of_daf_accounts"]) or 0 for r in proc24), acc.get(2024)),
                                                "grants_share": ratio(sum(f(r["total_daf_grants"]) or 0 for r in proc24), grants.get(2024))},
            "processor_accounts_fy2024_best_series": sorted(
                ({"ein": e, "name": meta.get(e, {}).get("name", ""), "daf_count": v.get("daf_count"), "daf_grants": v.get("daf_grants"),
                  "other_count": v.get("other_count"), "source": v.get("source")}
                 for (e, fy), v in series.items() if fy == 2024 and meta.get(e, {}).get("subtype") == "Donation Processor"
                 and (v.get("daf_count") or 0) >= 1000), key=lambda d: -(d["daf_count"] or 0)),
            "named_latest": {NAMED_PASS_THROUGH[e]: {"fy": fy, **{k: v.get(k) for k in ("daf_count", "daf_grants", "other_count",
                                                                                          "other_grants", "source", "object_id")}}
                             for e, (fy, v) in named_latest.items()}}


# ----------------------------------------------------------------------------- P-B34B-02 public-support cliff screen
def cliff_universe(series: Mapping[tuple, dict]) -> frozenset[str]:
    def hit(v):
        n, eoy = v.get("daf_count"), v.get("daf_eoy")
        return bool(n and n > 0 and eoy and eoy > 0 and ((n < CLIFF_MAX_COUNT and eoy >= CLIFF_MIN_EOY) or eoy / n > CLIFF_AVG))
    return frozenset(e for (e, fy), v in series.items() if fy >= 2021 and hit(v)) | {JASPER_RIDGE}


def support_basis(inds: str) -> str:
    s = set(inds.split(";"))
    for tag, label in (("PublicOrganization170Ind", "170(b)(1)(A)(vi)"), ("CommunityTrustInd", "community trust (vi)"),
                       ("PublicOrganization509a2Ind", "509(a)(2)"), ("PubliclySupportedOrg509a2Ind", "509(a)(2)"), ("CollegeOrganizationInd", "170(b)(1)(A)(iv)"),
                       ("HospitalInd", "hospital (iii)"), ("SchoolInd", "school (ii)"), ("ChurchInd", "church (i)"),
                       ("GovernmentalUnitInd", "government (v)")):
        if tag in s:
            return label
    return "509(a)(3)" if any("509a3" in x or "SupportingOrg" in x for x in s) else ("unknown" if inds else "")


def support_rows(chosen: Mapping[tuple, dict], exts: Mapping[str, dict], universe: frozenset, meta: Mapping,
                 index: Mapping[str, Sequence[dict]], series: Mapping[tuple, dict]) -> tuple[dict, ...]:
    def later_pf(e, tp):
        return ";".join(sorted({fl["tax_period"] for fl in index.get(e, ()) if fl["return_type"] == "990PF" and fl["tax_period"] > tp}))

    def row(e, fy, fl):
        x = exts.get(fl["object_id"], {})
        inds = x.get("sched_a_inds", "") or ""
        cy = x.get("PublicSupportCY170Pct") if x.get("PublicSupportCY170Pct") is not None else x.get("PublicSupportCY509Pct")
        py = x.get("PublicSupportPY170Pct") if x.get("PublicSupportPY170Pct") is not None else x.get("PublicSupportPY509Pct")
        n, eoy = x.get("daf_count"), x.get("daf_eoy")
        s = series.get((e, fy), {})
        first5 = "First5Years" in inds
        flags = tuple(k for k, c in (("first_5_years", first5), ("below_33_cy", cy is not None and cy < THIRD and not first5), ("near_33_cy", cy is not None and THIRD <= cy < NEAR_BAND),
                                     ("drop_10pts", cy is not None and py is not None and py - cy >= DROP_PTS),
                                     ("pf_status_ind", "PrivateFoundation170Ind" in inds or "PrivateFoundation509Ind" in inds),
                                     ("passed_on_prior_year_only", cy is not None and cy < THIRD and "ThirtyThrPctSuprtTestsPY170Ind" in inds),
                                     ("facts_circumstances", "TenPct" in inds)) if c)
        m = meta.get(e, {})
        return {"ein": e, "sponsor_name": m.get("name") or x.get("filer_name", ""), "dafrc_type": m.get("type", ""),
                "dafrc_subtype": m.get("subtype", ""), "dafrc_operating_status_latest": m.get("operating_status", ""),
                "fiscal_year": fy, "tax_period_end": x.get("tax_period_end", ""), "object_id": fl["object_id"],
                "xml_status": x.get("xml_status", ""), "amended_ind": x.get("amended_ind", ""),
                "daf_count": n if n is not None else s.get("daf_count"), "daf_eoy": eoy if eoy is not None else s.get("daf_eoy"),
                "daf_grants": x.get("daf_grants"), "daf_contributions": x.get("daf_contributions"),
                "avg_eoy_per_daf": ratio(eoy, n) if n else None, "total_assets_eoy": x.get("total_assets_eoy"),
                "daf_share_of_total_assets": ratio(eoy, x.get("total_assets_eoy")),
                "sched_a_present": x.get("sched_a_present", ""), "support_basis": support_basis(inds),
                "public_support_cy_pct": cy, "public_support_py_pct": py,
                "public_support_total_170": x.get("PublicSupportTotal170Amt"), "total_support_170": x.get("TotalSupportAmt"),
                "substantial_contributors_excess": x.get("SubstantialContributorsTotAmt"),
                "investment_income_cy_pct_509": x.get("InvestmentIncomeCYPct"), "sched_a_indicators": inds,
                "flags": ";".join(flags), "later_990pf_tax_periods": later_pf(e, fl["tax_period"]),
                "xml_url": XML_URL.format(oid=fl["object_id"])}
    return tuple(row(e, fy, fl) for (e, fy), fl in sorted(chosen.items()) if e in universe)


# ----------------------------------------------------------------------------- P-B34A-01 fill
FILL_EXTRA = ("harvest_xml_status_before", "teos_zip_url", "teos_member", "teos_compressed_bytes", "xml_bytes",
              "sched_d_other_funds_count", "sched_d_other_funds_contributions", "sched_d_other_funds_grants",
              "sched_d_other_funds_eoy_value", "public_support_cy_pct", "fill_note")


def fill_rows(harvest: Sequence[Mapping], labels: Mapping[str, str], work_dir: str, dafrc: Sequence[Mapping]) -> tuple[dict, ...]:
    dafrc_by_key = {(ein9(r["ein"]), int(r["fiscal_year_end"])): r for r in dafrc}

    def row(h):
        oid = h["return_object_id"]
        meta = teos_fetch(oid, labels.get(oid, "2026_TEOS_XML_05A"), work_dir)
        if meta["status"] != "ok":
            return {**h, **{k: "" for k in FILL_EXTRA}, "harvest_xml_status_before": h["xml_status"],
                    "xml_status": meta["status"], "teos_zip_url": meta["zip"], "fill_note": "member not found in TEOS zips"}
        with open(os.path.join(work_dir, "teos", f"{oid}_public.xml"), "rb") as fh:
            raw = fh.read()
        ex = {**harvest_extract(io.BytesIO(raw)), "xml_status": "ok_teos_zip"}
        xe = extract_ext(io.BytesIO(raw), False)
        filing = {"ein": h["ein"], "tax_period": h["tax_period"], "object_id": oid, "return_type": h["return_type"],
                  "taxpayer_name": h["filer_name_990"], "index_url": h["index_url"]}
        base = return_row(h, filing, ex, dafrc_by_key)
        cy = xe.get("PublicSupportCY170Pct") if xe.get("PublicSupportCY170Pct") is not None else xe.get("PublicSupportCY509Pct")
        notes = "; ".join(filter(None, (
            "negative DAF grants (suspect Part I)" if (ex.get("sched_d_daf_grants") or 0) < 0 else "",
            "zero DAFs at year end" if ex.get("sched_d_daf_count") == 0 else "",
            "no Schedule D" if not ex.get("sched_d_present") else "",
            "amended return" if ex.get("amended_ind") else "")))
        return {**base, "xml_url": f"{meta['zip']}#{meta['member']}", "harvest_xml_status_before": h["xml_status"],
                "teos_zip_url": meta["zip"], "teos_member": meta["member"], "teos_compressed_bytes": meta["compressed_bytes"],
                "xml_bytes": meta["xml_bytes"], "sched_d_other_funds_count": xe.get("other_count"),
                "sched_d_other_funds_contributions": xe.get("other_contributions"),
                "sched_d_other_funds_grants": xe.get("other_grants"), "sched_d_other_funds_eoy_value": xe.get("other_eoy"),
                "public_support_cy_pct": cy, "fill_note": notes}
    return tuple(row(h) for h in harvest if h["xml_status"] == "http_404")


def fill_summary(rows: Sequence[Mapping], harvest: Sequence[Mapping]) -> dict:
    ok = tuple(r for r in rows if r["xml_status"] == "ok_teos_zip")
    fy25_before = {r["ein"] for r in harvest if r["fiscal_year"] == "2025" and r["xml_status"] == "ok"}
    fy25_after = fy25_before | {r["ein"] for r in ok}
    sumv = lambda k: sum(f(r.get(k)) or 0 for r in ok if r.get("sched_d_present") in (1, "1"))
    return {"rows": len(rows), "filled": len(ok), "zips": dict(_count(r["teos_zip_url"] for r in rows)),
            "fy2025_sponsors_parsed_before": len(fy25_before), "fy2025_sponsors_parsed_after": len(fy25_after),
            "sched_d_present": sum(1 for r in ok if r.get("sched_d_present") in (1, "1")),
            "daf_eoy_sum": sumv("sched_d_daf_eoy_value"), "daf_grants_sum": sumv("sched_d_daf_grants"),
            "daf_contrib_sum": sumv("sched_d_daf_contributions"),
            "notes": dict(_count(n for r in ok for n in str(r["fill_note"]).split("; ") if n)),
            "largest": sorted(({"name": r["sponsor_name"], "eoy": f(r.get("sched_d_daf_eoy_value")), "count": f(r.get("sched_d_daf_count"))}
                               for r in ok), key=lambda d: -(d["eoy"] or 0))[:12]}


def _count(xs: Iterable) -> dict:
    out: dict = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


# ----------------------------------------------------------------------------- P-STF-02 Fidelity / Vanguard FY2025 lines
def np_extract(np_dirs: Sequence[str], oid: str) -> dict:
    for d in np_dirs:
        p = os.path.join(d, f"{oid}.json")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
    return {}


def d2d_rows(grantors: Sequence[tuple[str, str, str]], np_dirs: Sequence[str], meta: Mapping, series: Mapping[tuple, dict],
             flows: Sequence[Mapping], whitelist: Mapping[str, Mapping] | None = None) -> tuple[dict, ...]:
    wl = whitelist or {}
    reverse = _group_by_fast((r for r in flows if r["fiscal_year"] in ("2025", "2026")), lambda r: (r["grantor_ein"], r["recipient_ein"]))

    def for_grantor(gname, gein, oid):
        ex = np_extract(np_dirs, oid)
        lines = tuple(l for l in ex.get("sched_i_panel_lines", ()) if (l.get("matched_ein") or "") != gein)
        by = _group_by_fast(lines, lambda l: l["matched_ein"])
        return tuple(row(gein, gname, oid, ex, r, v) for r, v in by.items())

    def row(gein, gname, oid, ex, rein, ls):
        amt = sum((l.get("cash") or 0) + (l.get("noncash") or 0) for l in ls)
        rec = {fy: series.get((rein, fy), {}) for fy in (2025, 2026)}
        rfy = 2025 if rec[2025] else (2026 if rec[2026] else None)
        rc = (rec.get(rfy) or {}).get("daf_contributions") if rfy else None
        back = sum(f(r["amount_usd"]) or 0 for r in reverse.get((rein, gein), ()))
        m = meta.get(rein, {})
        return {"grantor": gname, "grantor_ein": gein, "grantor_object_id": oid, "grantor_tax_period_end": ex.get("tax_period_end", ""),
                "recipient_ein": rein, "recipient_name": m.get("name") or ls[0].get("recipient_name", ""),
                "recipient_dafrc_type": m.get("type", ""), "recipient_dafrc_subtype": m.get("subtype", ""),
                "whitelist_decision": (wl.get(rein) or {}).get("decision", "not_in_whitelist"),
                "whitelist_rule": (wl.get(rein) or {}).get("rule", ""),
                "lines": len(ls), "amount_usd": amt, "cash_usd": sum(l.get("cash") or 0 for l in ls),
                "noncash_usd": sum(l.get("noncash") or 0 for l in ls), "largest_line_usd": max((l.get("cash") or 0) + (l.get("noncash") or 0) for l in ls),
                "match_methods": ";".join(sorted({l.get("match_method", "") for l in ls})),
                "recipient_filed_fy": rfy, "recipient_daf_contributions_filed_fy": rc,
                "line_share_of_recipient_daf_contributions": ratio(amt, rc),
                "recipient_source": (rec.get(rfy) or {}).get("source", "") if rfy else "",
                "reverse_lines_fy2025_usd": back if back else None,
                "purpose_sample": (ls[0].get("purpose") or "")[:120]}
    rows = tuple(r for g in grantors for r in for_grantor(*g))
    within = {(r["grantor_ein"], r["recipient_ein"]): r["amount_usd"] for r in rows}
    rows = tuple({**r, "reverse_lines_fy2025_usd": r["reverse_lines_fy2025_usd"] or within.get((r["recipient_ein"], r["grantor_ein"]))}
                 for r in rows)
    return tuple(sorted(rows, key=lambda r: (r["grantor"], -r["amount_usd"])))


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--np-cache", action="append", default=[], help="netpayout990/ directories (mission_net_payout.py)")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--out-dir", default=DATA)
    a = ap.parse_args(argv)
    t0 = time.time()

    dafrc, harvest, corrected, flows = read_csv(DAFRC_CSV), read_csv(HARVEST_FULL), read_csv(CORRECTED), read_csv(D2D_FLOWS)
    meta = panel_meta(dafrc)
    idx_paths = tuple(os.path.join(a.irs_dir, f"index_{y}.csv") for y in INDEX_YEARS if os.path.exists(os.path.join(a.irs_dir, f"index_{y}.csv")))
    index_2026 = os.path.join(a.irs_dir, "index_2026.csv")

    # P-B34A-01: fill
    oids404 = frozenset(h["return_object_id"] for h in harvest if h["xml_status"] == "http_404")
    labels404 = batch_labels(index_2026, oids404)
    fills = fill_rows(harvest, labels404, a.work_dir, dafrc) if a.fetch or all(
        os.path.exists(os.path.join(a.work_dir, "teos", f"{o}_public.xml")) for o in oids404) else ()
    harvest_fields = tuple(harvest[0].keys())
    write_csv(os.path.join(a.out_dir, OUT["fill"]), rows_fmt(fills), harvest_fields + FILL_EXTRA)
    fill_layer = harvest_points(tuple({**r, "xml_status": "ok", "sched_d_present": fmt(r.get("sched_d_present"))} for r in fills))
    print(f"[fill] {len(fills)} rows, {time.time() - t0:.0f}s", file=sys.stderr)

    # base series (no fetch): DAFRC, then harvest, then fill
    base = best_series(dafrc_points(dafrc), harvest_points(harvest), fill_layer)

    # universes
    big = frozenset(e for (e, fy), v in base.items() if (v.get("daf_count") or 0) >= U1_MIN_COUNT)
    u1 = big | frozenset(NAMED_PASS_THROUGH) | {GS_DAPF, AYCO}
    u2 = cliff_universe(base)
    index = load_index(idx_paths, frozenset(u1 | u2))
    cands = candidate_filings(index, u1 | u2)
    exts = fetch_many(tuple(fl["object_id"] for fl in cands), a.work_dir, a.fetch)
    labels = batch_labels(index_2026, frozenset(o for o, e in exts.items() if e.get("xml_status") == "http_404"))
    exts = resolve_404s(exts, labels, a.work_dir, a.fetch)
    chosen = chosen_filings(cands, exts)
    print(f"[universe] U1 {len(u1)} sponsors, U2 {len(u2)} sponsors, {len(cands)} submissions, {len(chosen)} sponsor-years",
          file=sys.stderr)
    print(f"[ext] {len(exts)} extracts, status {_count(e.get('xml_status') for e in exts.values())}, {time.time() - t0:.0f}s", file=sys.stderr)

    series = best_series(base, ext_points({k: v for k, v in chosen.items() if k[0] in u1}, exts))

    # P-B34B-01
    pairs = tuple({**r, "classification": classify_reclass(r)} for r in reclass_pairs(series, meta))
    full = fetch_many(tuple(o for r in pairs for o in (r["object_id_prev"], r["object_id_cur"]) if o), a.work_dir, a.fetch, full=True)
    pairs = tuple({**r, "sched_o_daf_text_cur": full.get(r["object_id_cur"], {}).get("sched_o_daf_text", ""),
                   "sched_o_daf_text_prev": full.get(r["object_id_prev"], {}).get("sched_o_daf_text", ""),
                   "source_url_cur": XML_URL.format(oid=r["object_id_cur"]) if r["object_id_cur"] else ""} for r in pairs)
    pairs = tuple(sorted(pairs, key=lambda r: (r["classification"] != "reclassified_to_other_funds_column", -(r["daf_count_drop"] or 0))))
    write_csv(os.path.join(a.out_dir, OUT["reclass"]), rows_fmt(pairs), tuple(pairs[0].keys()) if pairs else ("ein",))
    effect = market_effect(pairs, corrected, dafrc, series, meta)

    # P-B34B-02
    sup = support_rows(chosen, exts, u2, meta, index, series)
    write_csv(os.path.join(a.out_dir, OUT["support"]), rows_fmt(sup), tuple(sup[0].keys()) if sup else ("ein",))

    # P-STF-02
    van_oid = next((fl["object_id"] for (e, fy), fl in chosen.items() if e == VANGUARD and fy == 2025), "202621329349306657")
    d2d = d2d_rows((("Fidelity Charitable", FIDELITY, "202601389349301700"), ("Vanguard Charitable", VANGUARD, van_oid)),
                   a.np_cache, meta, series, flows, {ein9(r["recipient_ein"]): r for r in read_csv(WHITELIST)})
    write_csv(os.path.join(a.out_dir, OUT["d2d"]), rows_fmt(d2d), tuple(d2d[0].keys()) if d2d else ("grantor",))

    # summary
    flagged_sup = tuple(r for r in sup if r["flags"])
    summary = {
        "fill": fill_summary(fills, harvest) if fills else {},
        "universe": {"u1": len(u1), "u2": len(u2), "returns": len(chosen),
                     "ext_status": _count(e.get("xml_status") for e in exts.values()),
                     "ext_source": _count(e.get("xml_source") for e in exts.values())},
        "reclass": {"pairs": len(pairs), "by_class": _count(r["classification"] for r in pairs),
                    "rows": [{k: r[k] for k in ("ein", "sponsor_name", "fy_prev", "fy_cur", "daf_count_prev", "daf_count_cur",
                                                "daf_grants_prev", "daf_grants_cur", "other_count_prev", "other_count_cur",
                                                "other_grants_cur", "classification", "source_prev", "source_cur")} for r in pairs],
                    "market_effect": effect},
        "support": {"rows": len(sup), "sponsors": len({r["ein"] for r in sup}),
                    "with_pct": sum(1 for r in sup if r["public_support_cy_pct"] is not None),
                    "basis": _count(r["support_basis"] for r in sup),
                    "flag_counts": _count(x for r in sup for x in r["flags"].split(";") if x),
                    "below_33_sponsors": sorted({r["sponsor_name"] for r in sup if "below_33_cy" in r["flags"]}),
                    "flagged": [{k: r[k] for k in ("ein", "sponsor_name", "dafrc_subtype", "fiscal_year", "daf_count", "daf_eoy",
                                                   "daf_share_of_total_assets", "support_basis", "public_support_cy_pct",
                                                   "public_support_py_pct", "flags", "later_990pf_tax_periods",
                                                   "dafrc_operating_status_latest", "object_id")}
                                for r in flagged_sup if {"below_33_cy", "near_33_cy", "drop_10pts", "pf_status_ind"} & set(r["flags"].split(";"))]},
        "d2d": {"rows": len(d2d), "by_grantor": {g: {"recipients": sum(1 for r in d2d if r["grantor"] == g),
                                                     "amount": sum(r["amount_usd"] for r in d2d if r["grantor"] == g)}
                                                 for g in ("Fidelity Charitable", "Vanguard Charitable")},
                "by_grantor_decision": {f"{g}|{dec}": sum(r["amount_usd"] for r in d2d if r["grantor"] == g and r["whitelist_decision"] == dec)
                                        for g in ("Fidelity Charitable", "Vanguard Charitable")
                                        for dec in ("include", "exclude", "not_in_whitelist")},
                "top": [{k: r[k] for k in ("grantor", "recipient_name", "whitelist_decision", "amount_usd", "lines", "recipient_daf_contributions_filed_fy",
                                           "recipient_filed_fy", "line_share_of_recipient_daf_contributions", "reverse_lines_fy2025_usd")}
                        for g in ("Fidelity Charitable", "Vanguard Charitable") for r in [x for x in d2d if x["grantor"] == g][:15]]},
        "ayco_gs": {k: {fy: {kk: series.get((e, fy), {}).get(kk) for kk in ("daf_count", "daf_contributions", "daf_grants", "daf_eoy", "source", "object_id")}
                        for fy in SCREEN_FYS if (e, fy) in series} for k, e in (("ayco", AYCO), ("gs_dapf", GS_DAPF))},
        "vanguard_series": {fy: {kk: series.get((VANGUARD, fy), {}).get(kk) for kk in ("daf_count", "daf_contributions", "daf_grants", "daf_eoy", "source")}
                            for fy in SCREEN_FYS if (VANGUARD, fy) in series},
        "elapsed_s": round(time.time() - t0)}
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
