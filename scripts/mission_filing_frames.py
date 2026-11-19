#!/usr/bin/env python3
"""Two IRS e-file filing frames (task gap1915-b4011): queue items P-GAP19-15-01 and P-B40N11-02.

P-GAP19-15-01  New DAF sponsors beyond DAFRC. Universe: every Form 990 (RETURN_TYPE 990) listed in the IRS TEOS
               e-file index 2022-2026 whose filer is a 501(c)(3) (BMF SUBSECTION 03) with BMF RULING >= 202101.
               Pre-filter (documented): BMF FOUNDATION code in {15,16,17,21,22,23,24} (public charities under
               170(b)(1)(A)(vi), 509(a)(2) and 509(a)(3)); private foundations (02-04, which cannot sponsor DAFs under
               IRC 4966(d)(1)) and churches, schools, hospitals and medical-research orgs (10-13) are dropped, and
               990-EZ/990-PF are dropped because Schedule D Part I is filed only with Form 990.
               Each return is streamed only as far as Form 990 Part IV (line 6, DonorAdvisedFundInd). When line 6 is
               'yes' the full XML is read and Schedule D Part I (DonorAdvisedFundsHeldCnt, ...VlEOYAmt, ...ContriAmt,
               ...GrantsAmt) is extracted. An EIN is a 'new DAF holder' if any scanned return reports DAF accounts > 0.
               The holders are compared with the DAFRC panel (sponsor-entry-exit-panel.csv) and screened with the
               cohort's pre-registered rule (gap19-startup-cohort.md §2.1) to give the additions CSV.

P-B40N11-02    Schedule N screen of community foundations. Universe: every Form 990 or 990-EZ in the e-file index
               2021-2026 whose filer name matches a community-foundation pattern (CF_NAME) or whose BMF NTEE code is
               T31. Each return is streamed to the end of Part IV (990) or of the form (990-EZ); Part I line 2
               (ContractTerminationInd), the final-return box (FinalReturnInd), Part IV lines 31/32
               (TerminateOperationsInd, PartialLiquidationInd) and 990-EZ line 36 (OrganizationDissolvedEtcInd) are
               read. When any is set, the full return is read and Schedule N (Part I liquidation, Part II disposition
               >25%), Schedule D Part I and DAF wording in Schedules N and O are recorded.

XML: GivingTuesday mirror of IRS TEOS XML, https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/
{OBJECT_ID}_public.xml (robots.txt on that host returns 404 = no rules; checked 2026-11-19). Extracts are cached as
JSON (one file per OBJECT_ID) under --cache. Generic user agent. Stdlib only; functional style (pure transforms,
I/O at the edges).

Usage:
  python3 scripts/mission_filing_frames.py . --irs-dir IRS --bmf-dir BMF --cache DIR [--fetch] [--workers 24]
         [--task scan-a|scan-b|build|all]
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from functools import reduce
from typing import Iterable, Mapping, Sequence

XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
INDEX_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
UA = {"User-Agent": "research-script/1.0"}
EXTRACT_V = 1
DATA = "data/mission-2026-11-14"
PANEL = f"{DATA}/sponsor-entry-exit-panel.csv"
COHORT = f"{DATA}/daf-startup-cohort-2021-2026.csv"
CONSOL = f"{DATA}/cf-consolidation-2021-2026.csv"
OUT_ADD = f"{DATA}/daf-startup-cohort-additions-2026-11-19.csv"
OUT_CFX = f"{DATA}/cf-exits-schedule-n-2021-2026.csv"
OUT_FRAME = f"{DATA}/new-daf-holders-frame-2022-2026.csv"

KEEP_FDN = frozenset({"15", "16", "17", "21", "22", "23", "24"})
CF_NAME = re.compile(r"COMMUNITY\s+(FOUNDATION|FDN|FND|TRUST|FUND\b|ENDOWMENT)|AREA\s+FOUNDATION|"
                     r"FOUNDATION\s+FOR\s+(THE\s+)?GREATER|REGIONAL\s+FOUNDATION", re.I)
DAF_WORDS = re.compile(r"DONOR[\s-]*ADVISED|\bDAFS?\b|ADVISED\s+FUNDS?", re.I)
YES = frozenset({"1", "true", "X", "x", "TRUE", "True"})
STOP_990 = ("<DisregardedEntityInd", "<RelatedEntityInd", "<RelatedOrganizationCtrlEntInd",
            "<ActivitiesConductedPrtshpInd", "<ScheduleORequiredInd", "</IRS990>", "</IRS990EZ>")
SMALL_CF_USD = 10_000_000


# ----------------------------------------------------------------------------- pure helpers
def num(x) -> float:
    try:
        return float(str(x).replace(",", "")) if x not in (None, "") else 0.0
    except ValueError:
        return 0.0


def tag(t: str, name: str) -> str:
    m = re.search(rf"<{name}(?:\s[^>]*)?>(.*?)</{name}>", t, re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split()) if m else ""


def tags(t: str, name: str) -> list:
    return [b for b in re.findall(rf"<{name}(?:\s[^>]*)?>(.*?)</{name}>", t, re.S)]


def block(t: str, name: str) -> str:
    i = t.find(f"<{name}")
    return t[i:t.find(f"</{name}>", i) + len(name) + 3] if i >= 0 else ""


def first_tag(t: str, *names: str) -> str:
    return next((v for v in (tag(t, n) for n in names) if v), "")


def yes(v: str) -> bool:
    return v in YES


def fmt_ein(e: str) -> str:
    return f"{e[:2]}-{e[2:]}" if len(e) == 9 else e


# ----------------------------------------------------------------------------- inputs
def read_csv(path: str) -> tuple:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return tuple(csv.DictReader(fh))


def read_bmf(bmf_dir: str) -> dict:
    files = sorted(f for f in os.listdir(bmf_dir) if f.endswith(".csv"))

    def rows(f):
        with open(os.path.join(bmf_dir, f), encoding="latin-1", newline="") as fh:
            return tuple((r["EIN"], {k: r[k] for k in ("NAME", "STATE", "SUBSECTION", "RULING", "FOUNDATION",
                                                       "NTEE_CD", "ASSET_AMT", "TAX_PERIOD")})
                         for r in csv.DictReader(fh))
    return dict(p for f in files for p in rows(f))


def index_rows(irs_dir: str, years: Iterable[int]) -> Iterable[dict]:
    for y in years:
        p = os.path.join(irs_dir, f"index_{y}.csv")
        if os.path.exists(p):
            with open(p, encoding="latin-1", newline="") as fh:
                yield from ({**r, "INDEX_YEAR": y} for r in csv.DictReader(fh))


def universes(irs_dir: str, bmf: Mapping) -> dict:
    """One pass over index 2019-2026: A returns, B returns, first listed tax period per A-eligible EIN, funnel."""
    new_c3 = frozenset(e for e, b in bmf.items() if b["SUBSECTION"] == "03" and b["RULING"] >= "202101")

    def is_b(r):
        b = bmf.get(r["EIN"])
        return r["RETURN_TYPE"] in ("990", "990EZ") and r["INDEX_YEAR"] >= 2021 and (
            bool(CF_NAME.search(r["TAXPAYER_NAME"])) or bool(b and b["NTEE_CD"].startswith("T31")))

    def step(acc, r):
        e, rt, y = r["EIN"], r["RETURN_TYPE"], r["INDEX_YEAR"]
        if e in new_c3:
            tp = r["TAX_PERIOD"]
            acc["first_tp"][e] = min(acc["first_tp"].get(e, tp), tp)
            acc["types"].setdefault(e, set()).add(rt)
            if y >= 2022 and rt == "990":
                fdn = bmf[e]["FOUNDATION"]
                acc["funnel"][fdn] += 1
                if fdn in KEEP_FDN:
                    acc["a"][r["OBJECT_ID"]] = r
        if is_b(r):
            acc["b"][r["OBJECT_ID"]] = r
        return acc
    return reduce(step, index_rows(irs_dir, range(2019, 2027)),
                  {"a": {}, "b": {}, "first_tp": {}, "types": {}, "funnel": Counter(), "new_c3": len(new_c3)})


# ----------------------------------------------------------------------------- extraction
def ex_head(t: str) -> dict:
    hdr = block(t, "ReturnHeader")
    form = "990EZ" if "<IRS990EZ" in t else ("990" if "<IRS990" in t else "")
    return {
        "form": form, "filer_ein": tag(block(hdr, "Filer"), "EIN"),
        "filer_name": first_tag(block(hdr, "Filer"), "BusinessNameLine1Txt", "BusinessNameLine1"),
        "state": tag(block(hdr, "Filer"), "StateAbbreviationCd"),
        "tax_period_end": tag(hdr, "TaxPeriodEndDt"), "tax_year": tag(hdr, "TaxYr"),
        "final_return_ind": tag(t, "FinalReturnInd"), "amended_ind": tag(t, "AmendedReturnInd"),
        "part1_line2_ind": tag(t, "ContractTerminationInd"),
        "terminate_ops_ind": tag(t, "TerminateOperationsInd"), "partial_liq_ind": tag(t, "PartialLiquidationInd"),
        "ez_dissolved_ind": tag(t, "OrganizationDissolvedEtcInd"),
        "daf_ind": first_tag(t, "DonorAdvisedFundInd", "DonorAdvisedFndsInd"),
        "total_assets_eoy": num(first_tag(t, "TotalAssetsEOYAmt") or tag(block(t, "Form990TotalAssetsGrp"), "EOYAmt")),
        "formation_yr": tag(t, "FormationYr"), "website": tag(t, "WebsiteAddressTxt"),
        "mission": (first_tag(t, "ActivityOrMissionDesc", "MissionDesc", "PrimaryExemptPurposeTxt"))[:240],
    }


def ex_full(t: str) -> dict:
    sd, sn, so = block(t, "IRS990ScheduleD"), block(t, "IRS990ScheduleN"), block(t, "IRS990ScheduleO")
    lines = [{"part": "I_liquidation" if g == "LiquidationOfAssetsDetail" else "II_disposition",
              "desc": first_tag(b, "AssetsDistriOrExpnssPaidDesc", "AssetsDistributedOrExpensesPaidDesc")[:200],
              "date": first_tag(b, "DistributionDt", "DispositionDt"), "fmv": num(first_tag(b, "FairMarketValueOfAssetAmt",
                                                                                         "FMVOfAssetAmt")),
              "method": tag(b, "MethodOfFMVDeterminationTxt")[:80],
              "recipient": first_tag(b, "BusinessNameLine1Txt", "BusinessNameLine1", "PersonNm"),
              "recipient_ein": tag(b, "EIN"), "recipient_irc": first_tag(b, "IRCSectionTxt", "IRCSection")}
             for g, b in re.findall(r"<(LiquidationOfAssetsDetail|DispositionOfAssetsDetail)(?:\s[^>]*)?>(.*?)</\1>", sn, re.S)]
    sn_text = " | ".join(tag(b, "ExplanationTxt") for b in tags(sn, "SupplementalInformationDetail"))[:1500]
    so_daf = [x for x in (tag(b, "ExplanationTxt") for b in tags(so, "SupplementalInformationDetail"))
              if DAF_WORDS.search(x) and re.search(r"TERMINAT|DISSOL|LIQUIDAT|MERG|TRANSFER|SUCCESSOR|CEASE", x, re.I)]
    return {**ex_head(t), "has_sched_d": bool(sd), "has_sched_n": bool(sn),
            "daf_count": num(tag(sd, "DonorAdvisedFundsHeldCnt")), "daf_value_eoy": num(tag(sd, "DonorAdvisedFundsVlEOYAmt")),
            "daf_contributions": num(tag(sd, "DonorAdvisedFundsContriAmt")), "daf_grants": num(tag(sd, "DonorAdvisedFundsGrantsAmt")),
            "other_funds_count": num(tag(sd, "FundsAndOtherAccountsHeldCnt")),
            "schedn_lines": lines, "schedn_text": sn_text, "schedo_daf_text": " | ".join(so_daf)[:1500]}


# ----------------------------------------------------------------------------- fetching (I/O edge)
def cached(path: str):
    try:
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        return c if c.get("_v") == EXTRACT_V else None
    except (OSError, ValueError):
        return None


def save(path: str, obj: dict) -> dict:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".tmp", "w", encoding="utf-8") as fh:
        json.dump(obj, fh)
    os.replace(path + ".tmp", path)
    return obj


def stream_until(url: str, stops: Sequence[str], cap: int = 8_000_000) -> tuple:
    """Read the response in 16 KiB chunks until any stop marker appears; returns (text, bytes_read, complete)."""
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        def step(buf):
            chunk = r.read(16_384)
            return buf + chunk, bool(chunk)
        buf, more = b"", True
        while more and len(buf) < cap and not any(s.encode() in buf for s in stops):
            buf, more = step(buf)
        return buf.decode("utf-8", "replace"), len(buf), not more


def with_retry(fn, oid: str) -> dict:
    def attempt(i: int) -> dict:
        try:
            return fn()
        except urllib.error.HTTPError as e:
            return {"status": f"http_{e.code}", "oid": oid} if e.code in (403, 404) or i == 2 else None
        except Exception as e:  # noqa: BLE001  (network errors: retry)
            time.sleep(3 * (i + 1))
            return {"status": f"error:{type(e).__name__}", "oid": oid} if i == 2 else None
    return next((x for x in map(attempt, range(3)) if x is not None), {"status": "error", "oid": oid})


def head_of(oid: str, cache: str, fetch: bool) -> dict:
    p = os.path.join(cache, "head", oid[:4], f"{oid}.json")
    c = cached(p)
    if c is not None or not fetch:
        return c or {"status": "not_fetched", "oid": oid}

    def go():
        t, n, complete = stream_until(XML_URL.format(oid=oid), STOP_990)
        return save(p, {"_v": EXTRACT_V, "status": "ok", "oid": oid, "bytes_read": n, "read_to_eof": complete, **ex_head(t)})
    out = with_retry(go, oid)
    return out


def full_of(oid: str, cache: str, fetch: bool) -> dict:
    p = os.path.join(cache, "full", f"{oid}.json")
    c = cached(p)
    if c is not None or not fetch:
        return c or {"status": "not_fetched", "oid": oid}

    def go():
        with urllib.request.urlopen(urllib.request.Request(XML_URL.format(oid=oid), headers=UA), timeout=300) as r:
            t = r.read().decode("utf-8", "replace")
        return save(p, {"_v": EXTRACT_V, "status": "ok", "oid": oid, **ex_full(t)})
    return with_retry(go, oid)


def pmap(fn, items: Sequence, workers: int, label: str) -> list:
    def logged(i_x):
        i, x = i_x
        out = fn(x)
        if i % 2000 == 0:
            print(f"  {label}: {i}/{len(items)}", file=sys.stderr, flush=True)
        return out
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(logged, enumerate(items)))


# ----------------------------------------------------------------------------- frame A
def needs_full_a(h: Mapping) -> bool:
    return h.get("status") == "ok" and yes(h.get("daf_ind", ""))


def needs_full_b(h: Mapping) -> bool:
    return h.get("status") == "ok" and any(yes(h.get(k, "")) for k in
                                          ("part1_line2_ind", "final_return_ind", "terminate_ops_ind",
                                           "partial_liq_ind", "ez_dissolved_ind"))


def scan(rets: Mapping, cache: str, fetch: bool, workers: int, needs, label: str) -> dict:
    oids = sorted(rets)
    heads = dict(zip(oids, pmap(lambda o: head_of(o, cache, fetch), oids, workers, f"{label} head")))
    want = sorted(o for o, h in heads.items() if needs(h))
    fulls = dict(zip(want, pmap(lambda o: full_of(o, cache, fetch), want, max(4, workers // 2), f"{label} full")))
    return {"heads": heads, "fulls": fulls}


# ----------------------------------------------------------------------------- build (pure over scan results)
def norm_name(s: str) -> frozenset:
    stop = {"THE", "INC", "OF", "AND", "FOUNDATION", "COMMUNITY", "FUND", "TRUST", "CORP", "CORPORATION", "AREA", "FDN", "&"}
    return frozenset(w for w in re.sub(r"[^A-Z0-9& ]", " ", s.upper()).split() if w not in stop)


def same_entity(a: str, b: str) -> bool:
    x, y = norm_name(a), norm_name(b)
    return bool(x and y) and len(x & y) / min(len(x), len(y)) >= 0.6


def frame_a(u: Mapping, bmf: Mapping, sa: Mapping, panel: frozenset, cohort: Mapping, idx26: frozenset) -> list:
    """One row per EIN in universe A with its DAF evidence across scanned returns."""
    by_ein = reduce(lambda acc, kv: {**acc, kv[1]["EIN"]: acc.get(kv[1]["EIN"], ()) + (kv[0],)}, u["a"].items(), {})

    def row(ein: str, oids: tuple) -> dict:
        heads = [sa["heads"].get(o, {}) for o in oids]
        fulls = [sa["fulls"][o] for o in oids if o in sa["fulls"] and sa["fulls"][o].get("status") == "ok"]
        pos = [f for f in fulls if f["daf_count"] > 0]
        latest = max((h for h in heads if h.get("status") == "ok"), key=lambda h: h.get("tax_period_end", ""), default={})
        best = max(pos, key=lambda f: f["daf_count"], default={})
        last_pos = max(pos, key=lambda f: f.get("tax_period_end", ""), default={})
        b = bmf[ein]
        fy = min((h.get("formation_yr") or "9999" for h in heads if h.get("status") == "ok"), default="9999")
        pre = [why for why, hit in (("index lists a return for tax period %s" % u["first_tp"].get(ein, ""), u["first_tp"].get(ein, "999999") < "202101"),
                                    ("Form 990 formation year %s" % fy, fy < "2021")) if hit]
        return {"ein": ein, "name": latest.get("filer_name") or b["NAME"], "state": b["STATE"], "bmf_ruling": b["RULING"],
                "bmf_foundation": b["FOUNDATION"], "ntee": b["NTEE_CD"], "returns_scanned": len(oids),
                "returns_ok": sum(h.get("status") == "ok" for h in heads),
                "returns_daf_ind_yes": sum(yes(h.get("daf_ind", "")) for h in heads),
                "returns_daf_count_gt0": len(pos), "max_daf_count": int(best.get("daf_count", 0)),
                "max_daf_count_tax_period": best.get("tax_period_end", ""),
                "latest_daf_value_eoy": int(last_pos.get("daf_value_eoy", 0)), "latest_daf_tax_period": last_pos.get("tax_period_end", ""),
                "first_index_tax_period": u["first_tp"].get(ein, ""), "formation_yr": "" if fy == "9999" else fy,
                "pre_window_evidence": "; ".join(pre), "in_window": "no" if pre else "yes",
                "in_dafrc_panel": "yes" if ein in panel else "no", "in_cohort_file": cohort.get(ein, ""),
                "listed_in_index_2026": "yes" if ein in idx26 else "no",
                "latest_tax_period": latest.get("tax_period_end", ""), "website": latest.get("website", ""),
                "mission": latest.get("mission", ""),
                "evidence_url": XML_URL.format(oid=best["oid"]) if best else ""}
    return sorted((row(e, o) for e, o in by_ein.items()), key=lambda r: (-r["max_daf_count"], r["ein"]))


def cf_exit_rows(u: Mapping, bmf: Mapping, sb: Mapping, panel: frozenset) -> list:
    heads = sb["heads"]
    max_assets = reduce(lambda acc, h: {**acc, h["filer_ein"]: max(acc.get(h["filer_ein"], 0.0), h["total_assets_eoy"])},
                        (h for h in heads.values() if h.get("status") == "ok" and h.get("filer_ein")), {})
    flagged = sorted((o for o in sb["fulls"]), key=lambda o: (u["b"][o]["EIN"], o))

    def is_cf(name: str, ein: str) -> bool:
        return bool(CF_NAME.search(name or "")) or bool(ein and bmf.get(ein, {}).get("NTEE_CD", "").startswith("T31"))

    def rows_for(oid: str) -> list:
        r, f = u["b"][oid], sb["fulls"][oid]
        if f.get("status") != "ok":
            return [{"object_id": oid, "filer_ein": r["EIN"], "filer_name": r["TAXPAYER_NAME"], "event_class": "xml_unavailable:" + f.get("status", "")}]
        ein = r["EIN"]
        b = bmf.get(ein, {})
        basis = "+".join(k for k, hit in (("name", bool(CF_NAME.search(r["TAXPAYER_NAME"]))),
                                           ("ntee_T31", b.get("NTEE_CD", "").startswith("T31"))) if hit)
        flags = {k: f.get(k, "") for k in ("final_return_ind", "part1_line2_ind", "terminate_ops_ind", "partial_liq_ind", "ez_dissolved_ind")}
        lines = f["schedn_lines"]
        groups = reduce(lambda acc, x: {**acc, (x["part"], x["recipient"].upper(), x["recipient_ein"]): acc.get((x["part"], x["recipient"].upper(), x["recipient_ein"]), ()) + (x,)},
                        lines, {})
        sn_daf = DAF_WORDS.search(" ".join(x["desc"] for x in lines) + " " + f["schedn_text"])
        so_daf = f["schedo_daf_text"]
        has_i = any(x["part"] == "I_liquidation" for x in lines)
        final = yes(flags["final_return_ind"])
        cls = ("exit_liquidation_schedule_n" if has_i else
               "exit_final_return_no_schedule_n_part_i" if final else
               "disposition_over_25pct" if lines else "flag_only_no_schedule_n")
        base = {"object_id": oid, "filer_ein": ein, "filer_name": f.get("filer_name") or r["TAXPAYER_NAME"], "state": f.get("state") or b.get("STATE", ""),
                "cf_basis": basis, "ntee": b.get("NTEE_CD", ""), "in_bmf_2026_11": "yes" if b else "no",
                "in_dafrc_panel": "yes" if ein in panel else "no", "form": r["RETURN_TYPE"], "tax_period_end": f.get("tax_period_end", ""),
                **flags, "event_class": cls, "has_schedule_n": "yes" if f.get("has_sched_n") else "no",
                "sched_d_daf_count": int(f.get("daf_count", 0)), "sched_d_daf_value_eoy": int(f.get("daf_value_eoy", 0)),
                "max_total_assets_eoy_scanned": int(max_assets.get(ein, 0)),
                "small_cf_lt_10m": "yes" if max_assets.get(ein, 0) < SMALL_CF_USD else "no",
                "xml_url": XML_URL.format(oid=oid)}
        def daf_named(xs) -> tuple:
            hit = next((x["desc"] for x in xs if DAF_WORDS.search(x["desc"])), "")
            ev = hit or (sn_daf.group(0) + " (Schedule N text)" if sn_daf else "") or (so_daf[:200] + " (Schedule O)" if so_daf else "")
            return ("yes" if ev else "no"), ev[:300]
        if not groups:
            return [{**base, "schedn_part": "", "transferee_name": "", "transferee_ein": "", "transferee_is_cf": "",
                     "transfer_date": "", "fmv_usd": "", "n_lines": 0, "asset_desc": "",
                     "daf_named": daf_named([])[0], "daf_named_evidence": daf_named([])[1],
                     "successor_same_name": "", "event_year": (f.get("tax_period_end") or "")[:4]}]
        return [{**base, "schedn_part": part, "transferee_name": xs[0]["recipient"], "transferee_ein": rein,
                 "transferee_is_cf": "yes" if is_cf(xs[0]["recipient"], rein) else "no",
                 "transfer_date": min((x["date"] for x in xs if x["date"]), default=""),
                 "fmv_usd": int(sum(x["fmv"] for x in xs)), "n_lines": len(xs),
                 "asset_desc": " ; ".join(sorted({x["desc"] for x in xs if x["desc"]}))[:300],
                 "daf_named": daf_named(xs)[0], "daf_named_evidence": daf_named(xs)[1],
                 "successor_same_name": "yes" if (rein and rein == ein) or same_entity(base["filer_name"], xs[0]["recipient"]) else "no",
                 "event_year": (min((x["date"] for x in xs if x["date"]), default="") or f.get("tax_period_end", ""))[:4]}
                for (part, _, rein), xs in sorted(groups.items())]
    rows = [x for o in flagged for x in rows_for(o)]
    return [{"row_id": f"CFX{i + 1:04d}", **x} for i, x in enumerate(rows)]


def exits_by_filer(rows: Sequence[Mapping]) -> list:
    """One exit per filer EIN: the earliest return whose class is an exit class."""
    ex = [r for r in rows if r.get("event_class", "").startswith("exit_")]
    first = reduce(lambda acc, r: acc if r["filer_ein"] in acc and acc[r["filer_ein"]]["event_year"] <= r["event_year"]
                   else {**acc, r["filer_ein"]: r}, ex, {})
    daf = {e for e in first if any(r["filer_ein"] == e and r["daf_named"] == "yes" for r in ex)}
    reorg = {e for e in first if any(r["filer_ein"] == e and r.get("successor_same_name") == "yes" for r in ex)}
    return [{**r, "_daf": e in daf, "_reorg": e in reorg} for e, r in sorted(first.items())]


def build(u: Mapping, bmf: Mapping, sa: Mapping, sb: Mapping, irs_dir: str) -> dict:
    panel = frozenset(r["ein"].zfill(9) for r in read_csv(PANEL))
    cohort = {e.replace("-", "").strip(): r["cohort_id"] for r in read_csv(COHORT) for e in r["ein"].split(";") if e.strip()}
    idx26 = frozenset(r["EIN"] for r in index_rows(irs_dir, (2026,)))
    fa = frame_a(u, bmf, sa, panel, cohort, idx26)
    write_csv(OUT_FRAME, [r for r in fa if r["returns_daf_count_gt0"] > 0], FRAME_FIELDS)
    holders = [r for r in fa if r["returns_daf_count_gt0"] > 0]
    add = additions(holders)
    write_csv(OUT_ADD, add, read_csv_header(COHORT))
    rows = cf_exit_rows(u, bmf, sb, panel)
    write_csv(OUT_CFX, rows, CFX_FIELDS)
    exits = exits_by_filer(rows)
    yrs = lambda xs: dict(sorted(Counter(x["event_year"] for x in xs).items()))
    hb = sb["heads"].values()
    return {
        "A": {"universe_returns": len(u["a"]), "universe_eins": len(fa),
              "heads": dict(Counter(h.get("status") for h in sa["heads"].values())),
              "fulls": dict(Counter(h.get("status") for h in sa["fulls"].values())),
              "eins_daf_ind_yes": sum(r["returns_daf_ind_yes"] > 0 for r in fa), "eins_daf_count_gt0": len(holders),
              "holders_in_panel": sum(r["in_dafrc_panel"] == "yes" for r in holders),
              "holders_not_in_panel": sum(r["in_dafrc_panel"] == "no" for r in holders),
              "holders_in_window": sum(r["in_window"] == "yes" for r in holders),
              "holders_in_window_not_panel": sum(r["in_window"] == "yes" and r["in_dafrc_panel"] == "no" for r in holders),
              "holders_in_window_not_panel_ge50": sum(r["in_window"] == "yes" and r["in_dafrc_panel"] == "no" and r["max_daf_count"] >= 50 for r in holders),
              "holders_in_window_in_panel_ge50": sum(r["in_window"] == "yes" and r["in_dafrc_panel"] == "yes" and r["max_daf_count"] >= 50 for r in holders),
              "cohort_eins_found": sorted(r["in_cohort_file"] for r in holders if r["in_cohort_file"]),
              "additions_rows": len(add), "additions_in_cohort": sum(r["in_cohort"] == "yes" for r in add)},
        "B": {"universe_returns": len(u["b"]), "universe_eins": len({r["EIN"] for r in u["b"].values()}),
              "heads": dict(Counter(h.get("status") for h in hb)),
              "flag_counts": {k: sum(yes(h.get(k, "")) for h in hb) for k in
                              ("part1_line2_ind", "final_return_ind", "terminate_ops_ind", "partial_liq_ind", "ez_dissolved_ind")},
              "flagged_returns": len(sb["fulls"]), "rows": len(rows),
              "event_class_rows": dict(Counter(r.get("event_class") for r in rows)),
              "exit_filers": len(exits), "exit_filers_small": sum(e["small_cf_lt_10m"] == "yes" for e in exits),
              "exits_by_year": yrs(exits), "small_exits_by_year": yrs([e for e in exits if e["small_cf_lt_10m"] == "yes"]),
              "small_exits_by_year_excl_reorg": yrs([e for e in exits if e["small_cf_lt_10m"] == "yes" and not e["_reorg"]]),
              "exits_daf_named": sum(e["_daf"] for e in exits), "exits_reorg_same_name": sum(e["_reorg"] for e in exits),
              "exits_in_panel": sum(e["in_dafrc_panel"] == "yes" for e in exits),
              "exits_ntee_t31": sum("ntee_T31" in e["cf_basis"] for e in exits),
              "exit_list": [(e["filer_ein"], e["filer_name"], e["event_year"], e["event_class"], e["small_cf_lt_10m"],
                             e["in_dafrc_panel"], e["_daf"], e["_reorg"], e["cf_basis"]) for e in exits]},
    }


FRAME_FIELDS = ("ein", "name", "state", "bmf_ruling", "bmf_foundation", "ntee", "returns_scanned", "returns_ok",
                "returns_daf_ind_yes", "returns_daf_count_gt0", "max_daf_count", "max_daf_count_tax_period",
                "latest_daf_value_eoy", "latest_daf_tax_period", "first_index_tax_period", "formation_yr",
                "pre_window_evidence", "in_window", "in_dafrc_panel", "in_cohort_file", "listed_in_index_2026",
                "latest_tax_period", "website", "mission", "evidence_url")
CFX_FIELDS = ("row_id", "filer_ein", "filer_name", "state", "cf_basis", "ntee", "in_bmf_2026_11", "in_dafrc_panel", "form",
              "object_id", "tax_period_end", "final_return_ind", "part1_line2_ind", "terminate_ops_ind", "partial_liq_ind",
              "ez_dissolved_ind", "event_class", "event_year", "has_schedule_n", "schedn_part", "transferee_name",
              "transferee_ein", "transferee_is_cf", "successor_same_name", "transfer_date", "fmv_usd", "n_lines", "asset_desc",
              "daf_named", "daf_named_evidence", "sched_d_daf_count", "sched_d_daf_value_eoy",
              "max_total_assets_eoy_scanned", "small_cf_lt_10m", "xml_url")


def read_csv_header(path: str) -> tuple:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return tuple(next(csv.reader(fh)))


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def additions(holders: Sequence[Mapping]) -> list:
    """Placeholder until the manual screen table is filled (see SCREEN)."""
    return []


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root")
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--limit", type=int, default=0, help="test: scan only the first N returns of each universe")
    ap.add_argument("--task", default="all", choices=("scan-a", "scan-b", "build", "all"))
    a = ap.parse_args(argv)
    os.chdir(a.root)
    bmf = read_bmf(a.bmf_dir)
    u = universes(a.irs_dir, bmf)
    cut = (lambda d: dict(sorted(d.items())[:a.limit])) if a.limit else (lambda d: d)
    print(json.dumps({"bmf_rows": len(bmf), "new_c3_eins": u["new_c3"], "a_returns": len(u["a"]),
                      "a_eins": len({r["EIN"] for r in u["a"].values()}), "b_returns": len(u["b"]),
                      "b_eins": len({r["EIN"] for r in u["b"].values()}),
                      "funnel_990_returns_by_fdn": dict(sorted(u["funnel"].items()))}), flush=True)
    sa = scan(cut(u["a"]), a.cache, a.fetch, a.workers, needs_full_a, "A") if a.task in ("scan-a", "all", "build") else None
    sb = scan(cut(u["b"]), a.cache, a.fetch, a.workers, needs_full_b, "B") if a.task in ("scan-b", "all", "build") else None
    if a.task in ("build", "all"):
        print(json.dumps(build(u, bmf, sa, sb, a.irs_dir), indent=1, default=str))
    else:
        s = sa or sb
        print(json.dumps({"heads": Counter(h.get("status") for h in s["heads"].values()),
                          "fulls": Counter(h.get("status") for h in s["fulls"].values())}, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
