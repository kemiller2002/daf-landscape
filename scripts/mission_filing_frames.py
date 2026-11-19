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
    return save(p, {"_v": EXTRACT_V, **out}) if out.get("status") == "http_404" else out


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


def boy_of(oid: str, cache: str, fetch: bool) -> dict:
    """Beginning-of-year total assets of a flagged return (size before the exit year; the head pass kept only EOY)."""
    p = os.path.join(cache, "boy", f"{oid}.json")
    c = cached(p)
    if c is not None or not fetch:
        return c or {"status": "not_fetched", "oid": oid}

    def go():
        t, _, _ = stream_until(XML_URL.format(oid=oid), ("</IRS990>", "</IRS990EZ>"))
        boy = num(first_tag(t, "TotalAssetsBOYAmt") or tag(block(t, "Form990TotalAssetsGrp"), "BOYAmt"))
        ts = tag(block(t, "ReturnHeader"), "ReturnTs")
        return save(p, {"_v": EXTRACT_V, "status": "ok", "oid": oid, "total_assets_boy": boy, "return_ts": ts})
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


def read_ok(h: Mapping) -> bool:
    return h.get("status") == "ok"


def scan(rets: Mapping, cache: str, fetch: bool, workers: int, needs, label: str) -> dict:
    """Head pass (to the end of Part IV) on every return, then a full read of every return `needs` selects.
    The run reported here reads every mirrored return in full (needs=read_ok): the Part IV pre-filters
    (line 6 for frame A; Part I line 2 / final-return box for frame B) are kept as columns and their recall is
    measured against the full read instead of being relied on (Groundswell's amended TY2024 return reports
    12,808 DAF accounts in Schedule D Part I while answering 'No' on Part IV line 6)."""
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
                "returns_daf_count_gt0": len(pos),
                "returns_daf_count_gt0_line6_no": sum(not yes(f.get("daf_ind", "")) for f in pos), "max_daf_count": int(best.get("daf_count", 0)),
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


def cf_exit_rows(u: Mapping, bmf: Mapping, sb: Mapping, panel: frozenset, boy: Mapping) -> list:
    heads = sb["heads"]
    sizes = [(u["b"][o]["EIN"], h["total_assets_eoy"]) for o, h in heads.items() if h.get("status") == "ok"] + \
            [(u["b"][o]["EIN"], b.get("total_assets_boy", 0.0)) for o, b in boy.items()]
    max_assets = reduce(lambda acc, kv: {**acc, kv[0]: max(acc.get(kv[0], 0.0), kv[1])}, sizes, {})
    flagged = sorted((o for o, f in sb["fulls"].items() if needs_full_b(heads.get(o, {})) or f.get("has_sched_n")
                      or f.get("status") != "ok"), key=lambda o: (u["b"][o]["EIN"], o))

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
        lines = [{**x, "recipient": x["recipient"] or bmf.get(x["recipient_ein"], {}).get("NAME", "")} for x in f["schedn_lines"]]
        groups = reduce(lambda acc, x: {**acc, (x["part"], x["recipient"].upper(), x["recipient_ein"]): acc.get((x["part"], x["recipient"].upper(), x["recipient_ein"]), ()) + (x,)},
                        lines, {})
        sn_daf = DAF_WORDS.search(" ".join(x["desc"] for x in lines) + " " + f["schedn_text"])
        so_daf = f["schedo_daf_text"]
        has_i = any(x["part"] == "I_liquidation" for x in lines)
        final = yes(flags["final_return_ind"])
        cls = ("exit_liquidation_schedule_n" if has_i else
               "exit_final_return_no_schedule_n_part_i" if final else
               "disposition_over_25pct" if lines else
               "schedule_n_without_detail_lines" if f.get("has_sched_n") else "flag_only_no_schedule_n")
        base = {"object_id": oid, "filer_ein": ein, "filer_name": f.get("filer_name") or r["TAXPAYER_NAME"], "state": f.get("state") or b.get("STATE", ""),
                "cf_basis": basis, "entity_class": EXIT_CLASS.get(ein, "unclassified"), "ntee": b.get("NTEE_CD", ""),
                "index_name": r["TAXPAYER_NAME"], "return_ts": boy.get(oid, {}).get("return_ts", ""), "in_bmf_2026_11": "yes" if b else "no",
                "in_dafrc_panel": "yes" if ein in panel else "no", "form": r["RETURN_TYPE"], "tax_period_end": f.get("tax_period_end", ""),
                **flags, "event_class": cls, "has_schedule_n": "yes" if f.get("has_sched_n") else "no",
                "sched_d_daf_count": int(f.get("daf_count", 0)), "sched_d_daf_value_eoy": int(f.get("daf_value_eoy", 0)),
                "max_total_assets_scanned": int(max_assets.get(ein, 0)),
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
                     "transferee_name_overlap": "", "event_year": (f.get("tax_period_end") or "")[:4]}]
        return [{**base, "schedn_part": part, "transferee_name": xs[0]["recipient"], "transferee_ein": rein,
                 "transferee_is_cf": "yes" if is_cf(xs[0]["recipient"], rein) else "no",
                 "transfer_date": min((x["date"] for x in xs if x["date"]), default=""),
                 "fmv_usd": int(sum(x["fmv"] for x in xs)), "n_lines": len(xs),
                 "asset_desc": " ; ".join(sorted({x["desc"] for x in xs if x["desc"]}))[:300],
                 "daf_named": daf_named(xs)[0], "daf_named_evidence": daf_named(xs)[1],
                 "transferee_name_overlap": "yes" if (rein and rein == ein) or same_entity(base["filer_name"], xs[0]["recipient"]) else "no",
                 "event_year": (min((x["date"] for x in xs if x["date"]), default="") or f.get("tax_period_end", ""))[:4]}
                for (part, _, rein), xs in sorted(groups.items())]
    rows = [x for o in flagged for x in rows_for(o)]
    return [{"row_id": f"CFX{i + 1:04d}", **x} for i, x in enumerate(rows)]


def build(u: Mapping, bmf: Mapping, sa: Mapping, sb: Mapping, irs_dir: str, cache: str, fetch: bool) -> dict:
    panel = frozenset(r["ein"].zfill(9) for r in read_csv(PANEL))
    cohort = {e.replace("-", "").strip(): r["cohort_id"] for r in read_csv(COHORT) for e in r["ein"].split(";") if e.strip()}
    idx26 = frozenset(r["EIN"] for r in index_rows(irs_dir, (2026,)))
    fa = frame_a(u, bmf, sa, panel, cohort, idx26)
    holders = [r for r in fa if r["returns_daf_count_gt0"] > 0]
    write_csv(OUT_FRAME, holders, FRAME_FIELDS)
    add, add_check = additions(holders)
    write_csv(OUT_ADD, add, read_csv_header(COHORT))
    flagged = sorted(o for o, f in sb["fulls"].items() if needs_full_b(sb["heads"].get(o, {})) or f.get("has_sched_n"))
    boy = dict(zip(flagged, pmap(lambda o: boy_of(o, cache, fetch), flagged, 16, "B boy")))
    rows = cf_exit_rows(u, bmf, sb, panel, boy)
    write_csv(OUT_CFX, rows, CFX_FIELDS)
    exits = exits_by_filer(rows)
    in_win = [e for e in exits if "2021" <= e["event_year"] <= "2026"]
    yrs = lambda xs: dict(sorted(Counter(x["event_year"] for x in xs).items()))
    geo = [e for e in in_win if e["entity_class"] == "geographic_cf"]
    hb = sb["heads"].values()
    win = [r for r in holders if r["in_window"] == "yes"]
    return {
        "A": {"universe_returns": len(u["a"]), "universe_eins": len(fa),
              "eins_with_no_mirrored_return": sum(r["returns_ok"] == 0 for r in fa),
              "heads": dict(Counter(h.get("status") for h in sa["heads"].values())),
              "fulls": dict(Counter(h.get("status") for h in sa["fulls"].values())),
              "not_mirrored_by_index_year": dict(sorted(Counter(u["a"][o]["INDEX_YEAR"] for o, h in sa["heads"].items()
                                                                if h.get("status") != "ok").items())),
              "eins_daf_ind_yes": sum(r["returns_daf_ind_yes"] > 0 for r in fa), "eins_daf_count_gt0": len(holders),
              "returns_daf_count_gt0": sum(r["returns_daf_count_gt0"] for r in holders),
              "returns_daf_count_gt0_line6_no": sum(r["returns_daf_count_gt0_line6_no"] for r in holders),
              "holders_missed_by_line6_filter": sum(r["returns_daf_ind_yes"] == 0 for r in holders),
              "returns_line6_yes_but_count_0": sum(yes(h.get("daf_ind", "")) and sa["fulls"].get(o, {}).get("daf_count", 0) == 0
                                                   for o, h in sa["heads"].items()),
              "holders_in_panel": sum(r["in_dafrc_panel"] == "yes" for r in holders),
              "holders_not_in_panel": sum(r["in_dafrc_panel"] == "no" for r in holders),
              "holders_in_window": len(win),
              "holders_in_window_in_panel": sum(r["in_dafrc_panel"] == "yes" for r in win),
              "holders_in_window_not_panel": sum(r["in_dafrc_panel"] == "no" for r in win),
              "holders_in_window_not_panel_value_gt0": sum(r["in_dafrc_panel"] == "no" and r["latest_daf_value_eoy"] > 0 for r in win),
              "holders_in_window_not_panel_ge50": sum(r["in_dafrc_panel"] == "no" and r["max_daf_count"] >= 50 for r in win),
              "holders_in_window_not_panel_ge50_value_0": sum(r["in_dafrc_panel"] == "no" and r["max_daf_count"] >= 50
                                                              and r["latest_daf_value_eoy"] == 0 for r in win),
              "holders_in_window_ntee_T": dict(Counter(r["ntee"][:1] or "-" for r in win)),
              "cohort_rows_found": sorted(r["in_cohort_file"] for r in holders if r["in_cohort_file"]),
              "cohort_rows_in_window_found": sorted(r["in_cohort_file"] for r in win if r["in_cohort_file"]),
              "additions": add_check},
        "B": {"universe_returns": len(u["b"]), "universe_eins": len({r["EIN"] for r in u["b"].values()}),
              "universe_by_form": dict(Counter(r["RETURN_TYPE"] for r in u["b"].values())),
              "universe_basis": dict(Counter("+".join(k for k, hit in (("name", bool(CF_NAME.search(r["TAXPAYER_NAME"]))),
                                                                   ("ntee", bmf.get(r["EIN"], {}).get("NTEE_CD", "").startswith("T31"))) if hit)
                                             for r in u["b"].values())),
              "heads": dict(Counter(h.get("status") for h in hb)),
              "flag_counts": {k: sum(yes(h.get(k, "")) for h in hb) for k in
                              ("part1_line2_ind", "final_return_ind", "terminate_ops_ind", "partial_liq_ind", "ez_dissolved_ind")},
              "flagged_returns": sum(needs_full_b(h) for h in hb),
              "returns_with_schedule_n": sum(bool(f.get("has_sched_n")) for f in sb["fulls"].values()),
              "schedule_n_without_flag": sum(bool(f.get("has_sched_n")) and not needs_full_b(sb["heads"].get(o, {}))
                                             for o, f in sb["fulls"].items()),
              "rows": len(rows), "event_class_rows": dict(Counter(r.get("event_class") for r in rows)),
              "exit_filers_all_years": len(exits), "exit_filers_by_year_all": yrs(exits),
              "exit_filers_2021_2026": len(in_win),
              "exit_filers_2021_2026_by_class": dict(Counter(e["entity_class"] for e in in_win)),
              "geo_cf_exits_by_year": yrs(geo),
              "geo_cf_small_exits_by_year": yrs([e for e in geo if e["small_cf_lt_10m"] == "yes"]),
              "geo_cf_exits_to_cf": sum(e["_to_cf"] for e in geo), "geo_cf_exits_daf_named": sum(e["_daf"] for e in geo),
              "geo_cf_exits_daf_on_final_sched_d": sum(e["_daf_final"] for e in geo),
              "geo_cf_exits_in_panel": sum(e["in_dafrc_panel"] == "yes" for e in geo),
              "geo_cf_exits_fmv_total": int(sum(e["_fmv"] for e in geo)),
              "all_exits_daf_named": sum(e["_daf"] for e in in_win),
              "cf_supporting_org_exits_by_year": yrs([e for e in in_win if e["entity_class"] == "cf_supporting_org"]),
              "geo_exit_list": [(e["filer_ein"], e["filer_name"], e["state"], e["event_year"], e["event_class"],
                                 e["small_cf_lt_10m"], e["in_dafrc_panel"], e["_to_cf"], e["_daf"], e["_daf_final"],
                                 int(e["_fmv"]), e["_recips"]) for e in geo]},
    }


def exits_by_filer(rows: Sequence[Mapping]) -> list:
    """One exit per filer EIN: the earliest return whose class is an exit class, with all its transfer rows summarised."""
    ex = [r for r in rows if r.get("event_class", "").startswith("exit_")]
    first = reduce(lambda acc, r: acc if r["filer_ein"] in acc and acc[r["filer_ein"]]["event_year"] <= r["event_year"]
                   else {**acc, r["filer_ein"]: r}, ex, {})

    def summary(e: str, r: Mapping) -> dict:
        mine = [x for x in ex if x["filer_ein"] == e and x["object_id"] == r["object_id"]]
        return {**r, "_daf": any(x["daf_named"] == "yes" for x in mine),
                "_daf_final": any(int(x["sched_d_daf_count"] or 0) > 0 for x in mine),
                "_reorg": any(x.get("transferee_name_overlap") == "yes" for x in mine),
                "_to_cf": any(x.get("transferee_is_cf") == "yes" for x in mine),
                "_fmv": sum(float(x["fmv_usd"] or 0) for x in mine),
                "_recips": "; ".join(sorted({x["transferee_name"] for x in mine if x["transferee_name"]}))[:120]}
    return [summary(e, r) for e, r in sorted(first.items())]


FRAME_FIELDS = ("ein", "name", "state", "bmf_ruling", "bmf_foundation", "ntee", "returns_scanned", "returns_ok",
                "returns_daf_ind_yes", "returns_daf_count_gt0", "returns_daf_count_gt0_line6_no", "max_daf_count", "max_daf_count_tax_period",
                "latest_daf_value_eoy", "latest_daf_tax_period", "first_index_tax_period", "formation_yr",
                "pre_window_evidence", "in_window", "in_dafrc_panel", "in_cohort_file", "listed_in_index_2026",
                "latest_tax_period", "website", "mission", "evidence_url")
CFX_FIELDS = ("row_id", "filer_ein", "filer_name", "index_name", "state", "cf_basis", "entity_class", "ntee", "in_bmf_2026_11", "in_dafrc_panel", "form",
              "object_id", "tax_period_end", "final_return_ind", "part1_line2_ind", "terminate_ops_ind", "partial_liq_ind",
              "ez_dissolved_ind", "event_class", "event_year", "has_schedule_n", "schedn_part", "transferee_name",
              "transferee_ein", "transferee_is_cf", "transferee_name_overlap", "transfer_date", "fmv_usd", "n_lines", "asset_desc",
              "daf_named", "daf_named_evidence", "sched_d_daf_count", "sched_d_daf_value_eoy",
              "max_total_assets_scanned", "small_cf_lt_10m", "return_ts", "xml_url")


def read_csv_header(path: str) -> tuple:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return tuple(next(csv.reader(fh)))


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# ----------------------------------------------------------------------------- hand-coded screen tables
# Frame B entity classes for every filer with an exit-class return (Schedule N Part I or final-return box).
# 'geographic_cf' = a place-based community foundation or community trust; the other classes are kept in the CSV but
# are not counted as CF exits. Classes marked [I] in the research doc are analyst inference from name and filing.
_GEO = ("383315675 383341102 260394674 330216692 382051672 273581914 850261515 320196064 311625750 460427565 240796877 "
        "203153511 812566406 650056930 391392267 824586796 873485646 812943823 237002871 462161591 853378589 474606495 "
        "341961329 274237687 205440142 275464729 571023842 860767009 460403105 823527581 841709233 "
        "113729710 311739538 821178194 842084322 161539889 200423761 201110274 208578861 208660184 383223079 "
        "421411234 460350319 473487091 582348181 841701434")
_SUPPORT = ("136105057 820915718 860790314 860800012 860846677 860898996 860914248 860941890 860955776 860965287 680544541 "
            "942597088 270697033 421513946")
_FAITH = "946098382 911307530 383941057 860465177"
_CHEST = "430862058 237187608 463115448 454967529 371913339 611558867"
_CORP = "952311678 916053828 542152547 800728749 451134650 311727591 862945144"
_CLUB = "680069883 680441952 831973017 860814086 270056566"
EXIT_CLASS = {**{e: "other_named_cf_like" for e in (
    "043494861 201038213 201947389 202704690 261595490 300696665 311415073 330804747 333990696 364286309 "
    "364334358 453160329 475516600 581635306 593733183 832495371 833173390 834674817 852671534 862049916 "
    "872958413 882955635 931301816 208559313 131919791 204121892 208514659 274272614 275199748 432099497 "
    "621584777 752857160 823398078 844740090 871682236 876759994 850694623").split()},
               **{e: "geographic_cf" for e in _GEO.split()}, **{e: "cf_supporting_org" for e in _SUPPORT.split()},
               **{e: "faith_based_cf" for e in _FAITH.split()}, **{e: "community_chest_or_fund" for e in _CHEST.split()},
               **{e: "corporate_or_employee_fund" for e in _CORP.split()}, **{e: "service_club_fund" for e in _CLUB.split()}}
# Disposition-only filers above are classed only for completeness; geographic CFs among them (e.g. Keweenaw, Watertown
# Area, Virginia CF, CF of East Alabama) are not exits and are not counted.

# Frame A additions: each row applies the cohort's pre-registered rule (gap19-startup-cohort.md §2.1) to an in-window,
# non-DAFRC Schedule D Part I DAF holder. Evidence: the filer's own 990 (Part III, Part VI, Schedule O; ReturnTs is
# the e-file timestamp) and, where robots.txt allowed, the homepage fetched 2026-11-19.
X = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml"
SCREEN = (
    {"cohort_id": "SA01", "in_cohort": "yes", "eins": ("992418877",), "entity_name": "Givmo (Givmo Charitable Fund)",
     "daf_entity_legal_name": "Givmo Charitable Fund", "product_category": "core_daf_sponsor (DAF account inside a mobile giving app)",
     "channel": "B2C app (+companies)", "entry_event": "sponsor IRS ruling", "entry_date": "2024-09 (ruling)",
     "parent_founded_pre2021": "unknown (Givmo app company founding date not verified)", "strict_window_subset": "unknown",
     "funding_evidence": "none found (not searched beyond filing and homepage)", "venture_backed": "unknown",
     "status": "active", "status_date": "2026-07-27",
     "status_evidence": "TY2025 Form 990 e-filed 2026-07-27 (ReturnTs): Part III 'operates exclusively as a donor-advised fund (DAF) sponsor ... through the Givmo mobile application'; 31 DAF accounts, $865 EOY; homepage live with (c) 2026",
     "status_evidence_url": X.format("202602089349300530") + " ; https://www.givmocharitable.org/", "evidence_tier": "1;4", "evidence_strength": "moderate"},
    {"cohort_id": "SA02", "in_cohort": "yes", "eins": ("872497866",), "entity_name": "Spiral Giving Network",
     "daf_entity_legal_name": "Spiral Giving Network Inc", "product_category": "daf_like_account (giving embedded in online banking)",
     "channel": "embedded in fintech/banking (Spiral Financial)", "entry_event": "sponsor IRS ruling", "entry_date": "2022-12 (ruling)",
     "parent_founded_pre2021": "unknown (sole member Spiral Financial, Inc.; founding date not verified)", "strict_window_subset": "unknown",
     "funding_evidence": "none found", "venture_backed": "unknown", "status": "active", "status_date": "2026-08-12",
     "status_evidence": "TY2025 Form 990 e-filed 2026-08-12 (ReturnTs); 990 Part III: 'sponsoring organization ... maintains ... classic donor-advised funds' and grants online-platform contributions; Schedule O: Spiral Financial, Inc. is sole member; 1 classic DAF ($449)",
     "status_evidence_url": X.format("202612249349301741") + " ; https://www.spiralgivingnetwork.org/", "evidence_tier": "1;4", "evidence_strength": "moderate"},
    {"cohort_id": "SA03", "in_cohort": "yes", "eins": ("932276661",), "entity_name": "Neta Foundation",
     "daf_entity_legal_name": "Neta Foundation", "product_category": "core_daf_sponsor (venture-philanthropy DAF, 'GrantVestments')",
     "channel": "B2C (donors)", "entry_event": "sponsor IRS ruling", "entry_date": "2023-11 (ruling)",
     "parent_founded_pre2021": "no (formation year 2023 on Form 990)", "strict_window_subset": "yes",
     "funding_evidence": "none found", "venture_backed": "no", "status": "unknown", "status_date": "",
     "status_evidence": "TY2024 990 e-filed 2025-10-12 (before the 12-month cutoff): 19 DAF accounts, $7.59m EOY; homepage live ('charitable asset manager', DAF) but latest copyright 2025; no dated item on or after 2025-11-19 found",
     "status_evidence_url": X.format("202542859349300019") + " ; https://www.netafoundation.org/", "evidence_tier": "1;4", "evidence_strength": "weak"},
    {"cohort_id": "SA04", "in_cohort": "yes", "eins": ("993997336",), "entity_name": "One Big Gift",
     "daf_entity_legal_name": "One Big Gift", "product_category": "core_daf_sponsor (endowment-style DAFs benefiting nonprofits)",
     "channel": "B2B2C (donors via nonprofits)", "entry_event": "sponsor IRS ruling", "entry_date": "2024-12 (ruling)",
     "parent_founded_pre2021": "no (formation year 2024)", "strict_window_subset": "yes", "funding_evidence": "none found",
     "venture_backed": "no", "status": "active", "status_date": "2026-08-18",
     "status_evidence": "TY2025 Form 990 e-filed 2026-08-18 (ReturnTs): 'create a sustainable source of income for nonprofit organizations through Donor Advised Funds'; 6 DAF accounts, $0.93m EOY. Homepage live but carries injected casino links (apparent site compromise, 2026-11-19)",
     "status_evidence_url": X.format("202632309349302723") + " ; https://www.onebiggift.org/", "evidence_tier": "1;4", "evidence_strength": "moderate"},
    {"cohort_id": "SA05", "in_cohort": "yes", "eins": ("934052953",), "entity_name": "DAFshare (DAF Gives Charitable)",
     "daf_entity_legal_name": "DAF Gives Charitable", "product_category": "daf_like_account (group-giving platform on a sponsor)",
     "channel": "B2C collective (online platform)", "entry_event": "sponsor IRS ruling", "entry_date": "2023-12 (ruling)",
     "parent_founded_pre2021": "no (formation year 2023)", "strict_window_subset": "yes", "funding_evidence": "none found",
     "venture_backed": "no", "status": "unknown", "status_date": "",
     "status_evidence": "TY2024 990 e-filed 2025-11-17, two days before the 12-month cutoff: 'we accept donations from the general public and various groups who have organized on our platform'; 740 grants to 169 charities in 2024; 1 DAF, $106k. dafshare.com shows a login page only (undated)",
     "status_evidence_url": X.format("202543219349326029") + " ; https://dafshare.com/", "evidence_tier": "1;4", "evidence_strength": "weak"},
    {"cohort_id": "SA06", "in_cohort": "yes", "eins": ("932565248",), "entity_name": "Monument Charitable",
     "daf_entity_legal_name": "Monument Charitable", "product_category": "core_daf_sponsor (non-cash / 'atypical' assets)",
     "channel": "unknown (no website found)", "entry_event": "sponsor IRS ruling", "entry_date": "2024-06 (ruling)",
     "parent_founded_pre2021": "no (formation year 2023)", "strict_window_subset": "yes", "funding_evidence": "none found",
     "venture_backed": "no", "status": "unknown", "status_date": "",
     "status_evidence": "TY2024 990 e-filed 2025-11-14 (before the cutoff); Schedule O: exists to 'provide donors with a method to support ... charities ... through unique and atypical donations'; 12 DAF accounts, $3.76m EOY; no website on the return",
     "status_evidence_url": X.format("202513189349304316"), "evidence_tier": "1", "evidence_strength": "weak"},
    {"cohort_id": "SA07", "in_cohort": "yes", "eins": ("883232461",), "entity_name": "Overflow Foundation",
     "daf_entity_legal_name": "Overflow Foundation", "product_category": "daf_adjacent (stock/crypto gift processing with DAFs; corporate giving vehicle of Overflow)",
     "channel": "B2B churches and nonprofits", "entry_event": "sponsor IRS ruling", "entry_date": "2023-01 (ruling)",
     "parent_founded_pre2021": "unknown (Overflow company founding date not verified)", "strict_window_subset": "unknown",
     "funding_evidence": "none found", "venture_backed": "unknown", "status": "unknown", "status_date": "",
     "status_evidence": "TY2024 990 e-filed 2025-11-15 (before the cutoff): 'Overflow Foundation maintains donor-advised funds'; 29 DAF accounts (value not reported); homepage: 'the vehicle by which we distribute Overflow's 10% commitment' (undated)",
     "status_evidence_url": X.format("202533199349300323") + " ; https://www.theoverflowfoundation.org/", "evidence_tier": "1;4", "evidence_strength": "weak"},
    {"cohort_id": "SAX01", "in_cohort": "no", "eins": ("991674027",), "entity_name": "Bridges Philanthropic Fund",
     "exclusion_reason": "product of a pre-2021 financial firm (private DAF run by Bridges Investment Management / Bridges Trust Company), treated like bank DAF programs",
     "daf_entity_legal_name": "Bridges Philanthropic Fund", "product_category": "core_daf_sponsor", "channel": "wealth-management clients",
     "entry_event": "sponsor IRS ruling", "entry_date": "2025-01 (ruling)",
     "status_evidence": "TY2025 990 (e-filed 2026-09-11): 42 DAF accounts, $106.98m EOY; Schedule O: operational functions delegated to Bridges Investment Management and Bridges Trust Company; homepage: 'our private donor advised fund'",
     "status_evidence_url": X.format("202612549349300906") + " ; https://bridgesphilanthropicfund.org/"},
    {"cohort_id": "SAX02", "in_cohort": "no", "eins": ("872542019",), "entity_name": "Anderson Donor Advised Charitable Fund",
     "exclusion_reason": "no public-facing DAF product found (31 accounts; return prepared by Anderson Global Business Group LLC; affiliation not established) [I]",
     "daf_entity_legal_name": "Anderson Donor Advised Charitable Fund", "entry_event": "sponsor IRS ruling", "entry_date": "2022-06 (ruling)",
     "status_evidence": "TY2024 990: 31 DAF accounts, $2.36m EOY; no website on the return", "status_evidence_url": X.format("202513219349314606")},
    {"cohort_id": "SAX03", "in_cohort": "no", "eins": ("853759949",), "entity_name": "JustFund",
     "exclusion_reason": "entry before window (index lists a return for tax period 2020-12; Form 990 formation year 2020)",
     "daf_entity_legal_name": "JustFundUs", "product_category": "daf_adjacent (common grant application platform)",
     "status_evidence": "TY2025 990: 8 DAF accounts, $0.72m"},
    {"cohort_id": "SAX04", "in_cohort": "no", "eins": ("873652885",), "entity_name": "The Alternatives Foundation",
     "exclusion_reason": "single-issue charity (supports Texas higher-education institutions); one DAF program started",
     "daf_entity_legal_name": "The Alternatives Foundation", "status_evidence": "TY2024 990: 1 DAF account, $0.11m"},
    {"cohort_id": "SAX05", "in_cohort": "no", "eins": ("886273927", "922859521"),
     "entity_name": "Mortarstone Trust; Kindred One Foundation",
     "exclusion_reason": "single-donor or family vehicles holding one DAF each; no public offering found",
     "daf_entity_legal_name": "The Mortarstone Trust; Kindred One Foundation"},
    {"cohort_id": "SAX06", "in_cohort": "no", "eins": ("872487558",), "entity_name": "Fenwick Community Fund",
     "exclusion_reason": "employer (law-firm) member fund for its own community; not sold to the public",
     "daf_entity_legal_name": "Fenwick Community Fund"},
    {"cohort_id": "SAX07", "in_cohort": "no", "eins": ("862589534",), "entity_name": "Richmond Christian Foundation",
     "exclusion_reason": "local faith-based community foundation (community-foundation exclusion)",
     "daf_entity_legal_name": "Richmond Christian Foundation"},
    {"cohort_id": "SAX08", "in_cohort": "no", "eins": ("372007864", "872158877", "871782380", "872043014", "923847849", "854391782",
                                                     "933345569", "854363773", "931342196", "883613546"),
     "entity_name": "In-window community foundations holding DAFs",
     "exclusion_reason": "community foundations (cohort exclusion)",
     "daf_entity_legal_name": "Jewish Foundation of Greensboro; Tulsa Fiduciary Fund; Three Valleys Community Foundation; Our Community Foundation Inc; Wichita County Community Foundation; Huron County Community Foundation; Greater Cabarrus Foundation; Bird City Century II; Community Foundation of Nevada County; Minnesota Black Collective Foundation"},
    {"cohort_id": "SAX09", "in_cohort": "no", "eins": "RESIDUAL", "entity_name": "Other in-window Schedule D Part I filers",
     "exclusion_reason": "single-issue or operating charities (schools, shelters, ministries, clubs); many Part I entries are implausible (dollar amounts in the account-count field, zero value)",
     "daf_entity_legal_name": "see new-daf-holders-frame-2022-2026.csv (in_window=yes, in_dafrc_panel=no)"},
)


def additions(holders: Sequence[Mapping]) -> tuple:
    """Rows for daf-startup-cohort-additions (same columns as the cohort file) plus a consistency report."""
    by = {r["ein"]: r for r in holders}
    named = frozenset(e for s in SCREEN if s["eins"] != "RESIDUAL" for e in s["eins"])
    residual = sorted(r["ein"] for r in holders if r["in_window"] == "yes" and r["in_dafrc_panel"] == "no"
                      and not r["in_cohort_file"] and r["ein"] not in named)

    def row(s: Mapping) -> dict:
        eins = residual if s["eins"] == "RESIDUAL" else list(s["eins"])
        hs = [by[e] for e in eins if e in by]
        facts = "; ".join(f"{fmt_ein(h['ein'])}: max {h['max_daf_count']} DAF accounts ({h['max_daf_count_tax_period']}), "
                          f"latest DAF value ${h['latest_daf_value_eoy']:,} ({h['latest_daf_tax_period']}), BMF ruling {h['bmf_ruling']}"
                          for h in hs) if len(hs) <= 3 else f"{len(hs)} EINs; see frame CSV"
        urls = " ; ".join(h["evidence_url"] for h in hs if h["evidence_url"]) if len(hs) <= 3 else ""
        return {"status_evidence_url": urls, **{k: v for k, v in s.items() if k != "eins"},
                "ein": "; ".join(fmt_ein(e) for e in eins) if len(eins) <= 12 else f"{len(eins)} EINs (frame CSV)",
                "frames": "D", "frame_source": "IRS e-file frame 2022-2026 (this task): Schedule D Part I DAF accounts > 0; BMF ruling >= 2021-01",
                "last_990_period_propublica": "; ".join(sorted({h["latest_tax_period"] for h in hs}))[:60] if len(hs) <= 3 else "",
                "in_dafrc_panel": "; ".join(sorted({h["in_dafrc_panel"] for h in hs})) or "n/a",
                "dafrc_exit_flag": "n/a" if all(h["in_dafrc_panel"] == "no" for h in hs) else "",
                "notes": ("Frame D facts: " + facts + ". last_990_period_propublica holds the latest tax period in the IRS e-file index "
                          "(ProPublica not used)."
                          + (" Account threshold (>=50) not applied: the entity is a dedicated DAF sponsor (DAFRC 'National'-type analogue)."
                             if s["in_cohort"] == "yes" else ""))}
    rows = [row(s) for s in SCREEN]
    check = {"screen_eins_not_in_window_nonpanel_holders": sorted(e for e in named if e not in by or by[e]["in_window"] != "yes"),
             "residual_count": len(residual), "members": sum(s["in_cohort"] == "yes" for s in SCREEN),
             "member_eins_in_panel": sorted(e for s in SCREEN if s["in_cohort"] == "yes" for e in s["eins"]
                                            if by.get(e, {}).get("in_dafrc_panel") == "yes")}
    return rows, check




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
    sa = scan(cut(u["a"]), a.cache, a.fetch, a.workers, read_ok, "A") if a.task in ("scan-a", "all", "build") else None
    sb = scan(cut(u["b"]), a.cache, a.fetch, a.workers, read_ok, "B") if a.task in ("scan-b", "all", "build") else None
    if a.task in ("build", "all"):
        print(json.dumps(build(u, bmf, sa, sb, a.irs_dir, a.cache, a.fetch), indent=1, default=str))
    else:
        s = sa or sb
        print(json.dumps({"heads": Counter(h.get("status") for h in s["heads"].values()),
                          "fulls": Counter(h.get("status") for h in s["fulls"].values())}, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
