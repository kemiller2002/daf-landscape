#!/usr/bin/env python3
"""NPT-pattern screen of the DAFRC panel (P-B44N27B39N4-02) and realised admin-fee rates for the long tail
(P-B4501-02 / P-B450104-02). Task id b4427b-b4501.

Stdlib only; functional style: pure transforms, with I/O confined to the small read/fetch/write helpers and main().

Task `fetch`   For every sponsor with a DAFRC row in FY2021-2024, pick the newest Form 990 for each FY2020-2025 from the
               IRS TEOS indexes (fiscal year = calendar year in which the tax period ends; a higher object id supersedes,
               as in mission_dafrc_corrected_totals.py), fetch the XML from the GivingTuesday mirror of IRS TEOS (or reuse a
               cached copy) and append the parsed lines to a JSONL cache (one record per object id). XMLs are not kept.
Task `screen`  The NPT pattern, for each sponsor-year t in FY2021-2024 with filed returns for t-1, t and t+1:
                 r_t = Schedule D Part I line 4 (DAF value EOY) / Part X line 33 net assets EOY
                 break      : |r_t - r_(t-1)| > 10 points AND |r_t - r_(t+1)| > 10 points, same sign (a spike or dip,
                              not a trend)
                 flows      : Sch D line 2 / Part VIII line 1h contributions and Sch D line 3 / Part IX lines 1-3 grants
                              in year t each within [min, max] of the two neighbours' shares +/- 10 points
                 size       : gap_t = line4_t - mean(r_(t-1), r_(t+1)) x net assets_t; breaks with |gap| > $250m listed
               Roll-forward test of each listed break (DAF flows plus the year's net-asset return):
                 rho_t      = (NA_t - NA_(t-1) - (PartVIII contrib_t - PartIX grants_t)) / NA_(t-1)
                 forward    = line4_(t-1) x (1 + rho_t) + line2_t - line3_t
                 backward   = (line4_(t+1) - line2_(t+1) + line3_(t+1)) / (1 + rho_(t+1))
               and, for comparison with b44n27-b39n4 §2.2, the NPT net-asset-change roll: line4_(t-1) + (NA_t - NA_(t-1)).
               Verdict 'filed fails roll-forward' when forward and backward agree within 10% of each other and the filed
               value is more than 10% from both.
Task `fees`    Realised admin-fee rate = fee income transcribed from audited statements or Form 990 (FEE_EVIDENCE below;
               every quote is checked against the cached source text) / average of BOY and EOY balance (DAF balance from
               Schedule D Part I line 4, or the component-fund / net-asset balance named in the source).

Inputs (never modified):
  data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv, dafrc-corrections-itemized.csv,
  long-tail-fee-census-2026-11-19.csv, long-tail-operating-cost-2026-11-19.csv
  IRS TEOS index  https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv (--irs-dir; later dirs win)
  Form 990 XML    https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml
Outputs:
  data/mission-2026-11-14/npt-pattern-screen-2026-11-20.csv
  data/mission-2026-11-14/tail-realised-fee-rates-2026-11-20.csv
  markdown tables on stdout (used by research/mission-2026-11-14/b4427b-b4501-npt-screen-and-realised-fees.md)

Usage:
  python3 -I scripts/mission_npt_screen_fees.py . --task fetch  --irs-dir IRS [--irs-dir NEWER] --cache CACHE.jsonl
          [--xml-dir DIR ...] [--fetch]
  python3 -I scripts/mission_npt_screen_fees.py . --task screen --irs-dir IRS [--irs-dir NEWER] --cache CACHE.jsonl
  python3 -I scripts/mission_npt_screen_fees.py . --task fees   --cache CACHE.jsonl --text-dir TEXTDIR
"""
from __future__ import annotations

import argparse
import csv
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
from functools import reduce
from typing import Iterable, Mapping, Sequence

UA = "research-script/1.0"
NS = "{http://www.irs.gov/efile}"
INDEX_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
PANEL = "data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv"
ITEMS = "data/mission-2026-11-14/dafrc-corrections-itemized.csv"
CENSUS = "data/mission-2026-11-14/long-tail-fee-census-2026-11-19.csv"
COST = "data/mission-2026-11-14/long-tail-operating-cost-2026-11-19.csv"
OUT_SCREEN = "data/mission-2026-11-14/npt-pattern-screen-2026-11-20.csv"
OUT_FEES = "data/mission-2026-11-14/tail-realised-fee-rates-2026-11-20.csv"
SCREEN_FYS = (2021, 2022, 2023, 2024)
FETCH_FYS = tuple(range(2020, 2026))
BREAK_PTS = 0.10
FLOW_PTS = 0.10
MIN_GAP = 250e6
ROLL_TOL = 0.10

# name -> tag path under IRS990 (Form) or IRS990ScheduleD
FORM_FIELDS = {
    "net_assets_boy": ("NetAssetsOrFundBalancesBOYAmt",), "net_assets_eoy": ("NetAssetsOrFundBalancesEOYAmt",),
    "total_assets_eoy": ("TotalAssetsGrp", "EOYAmt"),
    "contributions_total": ("TotalContributionsAmt",), "grants_paid": ("CYGrantsAndSimilarPaidAmt",),
    "program_service_revenue": ("TotalProgramServiceRevenueAmt",), "total_revenue": ("CYTotalRevenueAmt",),
    "rev_less_exp": ("ReconcilationRevenueExpnssAmt",), "unrealized_gains": ("NetUnrlzdGainsLossesInvstAmt",),
    "other_changes_net_assets": ("OtherChangesInNetAssetsAmt",), "fees_mgmt_l11a": ("FeesForServicesManagementGrp", "TotalAmt"),
}
SCHED_D_FIELDS = {
    "daf_accounts": ("DonorAdvisedFundsHeldCnt",), "daf_contributions": ("DonorAdvisedFundsContriAmt",),
    "daf_grants": ("DonorAdvisedFundsGrantsAmt",), "daf_value_eoy": ("DonorAdvisedFundsVlEOYAmt",),
    "other_funds_count": ("FundsAndOtherAccountsHeldCnt",), "other_funds_eoy": ("FundsAndOtherAccountsVlEOYAmt",),
    "endow_boy": ("CYEndwmtFundGrp", "BeginningYearBalanceAmt"), "endow_eoy": ("CYEndwmtFundGrp", "EndYearBalanceAmt"),
    "endow_admin_exp": ("CYEndwmtFundGrp", "AdministrativeExpensesAmt"),
}


# ----------------------------------------------------------------------------- small pure helpers
def num(x) -> float | None:
    try:
        return float(str(x).replace(",", "").strip()) if x not in (None, "") else None
    except ValueError:
        return None


def ein9(x: str) -> str:
    return re.sub(r"\D", "", str(x)).zfill(9)


def fy_of(tax_period: str) -> int:
    return int(str(tax_period)[:4])


def fmt(x) -> str:
    if x is None:
        return ""
    if isinstance(x, float):
        return f"{x:.0f}" if abs(x) >= 1000 or x == int(x) else f"{x:.4f}"
    return str(x)


def m(x: float | None) -> str:
    return "–" if x is None else f"{x / 1e6:,.1f}"


def pct(x: float | None, d: int = 1) -> str:
    return "–" if x is None else f"{100 * x:.{d}f}%"


def div(a: float | None, b: float | None) -> float | None:
    return a / b if a is not None and b not in (None, 0) else None


def median(xs: Iterable[float]) -> float | None:
    v = [x for x in xs if x is not None]
    return statistics.median(v) if v else None


def quartiles(xs: Iterable[float]) -> tuple[float | None, float | None]:
    v = sorted(x for x in xs if x is not None)
    if len(v) < 2:
        return (v[0], v[0]) if v else (None, None)
    q = statistics.quantiles(v, n=4, method="inclusive")
    return q[0], q[2]


def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows({k: fmt(r.get(k)) for k in fields} for r in rows)


def md_table(header: Sequence[str], rows: Iterable[Sequence]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return "\n".join(lines + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


# ----------------------------------------------------------------------------- index and XML I/O
def index_paths(dirs: Sequence[str]) -> dict[str, str]:
    """year -> path; later dirs win."""
    found = ((mm.group(1), os.path.join(d, f)) for d in dirs for f in sorted(os.listdir(d))
             for mm in (re.fullmatch(r"index_(\d{4})\.csv", f),) if mm)
    return reduce(lambda acc, kv: {**acc, kv[0]: kv[1]}, found, {})


def load_index(paths: Mapping[str, str], eins: frozenset[str]) -> dict[str, tuple[dict, ...]]:
    def recs(year, p):
        with open(p, newline="", encoding="latin-1") as fh:
            return tuple({"ein": ein9(d["EIN"]), "tax_period": d["TAX_PERIOD"], "return_type": d["RETURN_TYPE"],
                          "object_id": d["OBJECT_ID"], "index_year": year}
                         for d in csv.DictReader(fh) if d.get("RETURN_TYPE") == "990" and ein9(d.get("EIN", "")) in eins)
    allrecs = {r["object_id"]: r for y, p in sorted(paths.items()) for r in recs(y, p)}
    grouped: dict[str, tuple[dict, ...]] = {}
    for r in allrecs.values():  # local accumulation only
        grouped[r["ein"]] = grouped.get(r["ein"], ()) + (r,)
    return grouped


def latest_fy_return(filings: Sequence[Mapping], fy: int) -> dict | None:
    cand = tuple(f for f in filings if fy_of(f["tax_period"]) == fy)
    return max(cand, key=lambda f: (f["tax_period"], f["object_id"])) if cand else None


def fy_candidates(filings: Sequence[Mapping], fy: int) -> tuple[dict, ...]:
    """All Form 990s for fy, newest first (the order latest_fy_return uses)."""
    return tuple(sorted((f for f in filings if fy_of(f["tax_period"]) == fy),
                        key=lambda f: (f["tax_period"], f["object_id"]), reverse=True))


def selected_returns(index: Mapping[str, Sequence[Mapping]], eins: Iterable[str],
                     cache: Mapping[str, Mapping] | None = None) -> dict[tuple[str, int], dict]:
    """Newest return per (EIN, FY). With a parse cache, the newest whose XML parsed (a return missing from the mirror
    falls back to the next-newest for the same fiscal year; the fallback is flagged)."""
    def pick(cands):
        if cache is None:
            return cands[0] if cands else None
        ok = [c for c in cands if cache.get(c["object_id"], {}).get("parse") == "ok"]
        return ({**ok[0], "fallback": int(ok[0]["object_id"] != cands[0]["object_id"])} if ok else
                (cands[0] if cands else None))
    return {(e, fy): r for e in eins for fy in FETCH_FYS for r in (pick(fy_candidates(index.get(e, ()), fy)),) if r}


def first(base, tags) -> str | None:
    node = None if base is None else base.find(".//" + "/".join(NS + t for t in tags))
    return (node.text or "").strip() if node is not None and node.text else None


def parse_xml_bytes(data: bytes) -> dict:
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return {"parse": "error"}
    form, sd = root.find(f".//{NS}IRS990"), root.find(f".//{NS}IRS990ScheduleD")
    hdr = root.find(f"{NS}ReturnHeader")
    psr = tuple({"desc": first(g, ("Desc",)), "amt": num(first(g, ("TotalRevenueColumnAmt",)))}
                for g in (form.findall(f".//{NS}ProgramServiceRevenueGrp") if form is not None else ()))
    sched_o = " ".join(" ".join(t.strip() for t in e.itertext()) for e in root.iter()
                       if e.tag in (f"{NS}IRS990ScheduleO", f"{NS}IRS990ScheduleD") and e is not None)
    fee_snips = tuple(sorted({sched_o[max(0, mm.start() - 160): mm.end() + 220].strip()
                              for mm in re.finditer(r"(?i)(administrative|admin\.?|management|service)\s+fees?", sched_o)}))[:8]
    return {
        "parse": "ok", "tax_period_end": first(hdr, ("TaxPeriodEndDt",)), "return_ts": (first(hdr, ("ReturnTs",)) or "")[:10],
        "sched_d_present": int(sd is not None), "amended": first(form, ("AmendedReturnInd",)),
        **{k: num(first(form, p)) for k, p in FORM_FIELDS.items()},
        **{k: num(first(sd, p)) for k, p in SCHED_D_FIELDS.items()},
        "psr_lines": psr, "fee_snippets": fee_snips,
    }


def cached_xml_paths(dirs: Sequence[str]) -> dict[str, str]:
    """object id -> an existing XML file anywhere under the given dirs (reuse of earlier downloads)."""
    return {mm.group(1): os.path.join(root, f) for d in dirs for root, _, files in os.walk(d) for f in files
            for mm in (re.search(r"(\d{18})(?:_public)?\.xml$", f),) if mm}


def get_xml(oid: str, local: Mapping[str, str], fetch: bool) -> tuple[bytes | None, str]:
    path = local.get(oid)
    if path and os.path.getsize(path) > 0:
        with open(path, "rb") as fh:
            return fh.read(), "cache"
    if not fetch:
        return None, "not_cached"
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read(), "mirror"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, "http_404"
            time.sleep(2 + attempt * 3)
        except Exception:  # noqa: BLE001 - retried, then logged as a failure
            time.sleep(2 + attempt * 3)
    return None, "fetch_failed"


def read_cache(path: str) -> dict[str, dict]:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return {d["object_id"]: d for d in map(json.loads, fh)}


# ----------------------------------------------------------------------------- (A) NPT-pattern screen: pure
def year_record(ret: Mapping | None, parsed: Mapping | None) -> dict | None:
    if not ret or not parsed or parsed.get("parse") != "ok":
        return None
    return {**parsed, "object_id": ret["object_id"], "tax_period": ret["tax_period"]}


def ratio(y: Mapping | None) -> float | None:
    return div(y.get("daf_value_eoy"), y.get("net_assets_eoy")) if y and (y.get("net_assets_eoy") or 0) > 0 else None


def share(a, b) -> float | None:
    return div(a, b) if (b or 0) > 0 and a is not None else None


def within_band(x: float | None, a: float | None, b: float | None, tol: float) -> bool | None:
    if None in (x, a, b):
        return None
    return min(a, b) - tol <= x <= max(a, b) + tol


def rho(y: Mapping, prev: Mapping) -> float | None:
    """Net-asset return in year y other than contributions and grants, as a share of opening net assets."""
    na, na0 = y.get("net_assets_eoy"), prev.get("net_assets_eoy")
    if None in (na, na0) or na0 <= 0:
        return None
    return (na - na0 - ((y.get("contributions_total") or 0) - (y.get("grants_paid") or 0))) / na0


def rollforward(prev: Mapping, cur: Mapping, nxt: Mapping) -> dict:
    r_t, r_n = rho(cur, prev), rho(nxt, cur)
    fwd = (prev["daf_value_eoy"] * (1 + r_t) + (cur.get("daf_contributions") or 0) - (cur.get("daf_grants") or 0)
           if r_t is not None else None)
    bwd = ((nxt["daf_value_eoy"] - (nxt.get("daf_contributions") or 0) + (nxt.get("daf_grants") or 0)) / (1 + r_n)
           if r_n is not None and r_n > -1 else None)
    na_roll_fwd = prev["daf_value_eoy"] + cur["net_assets_eoy"] - prev["net_assets_eoy"]
    na_roll_bwd = nxt["daf_value_eoy"] - (nxt["net_assets_eoy"] - cur["net_assets_eoy"])
    filed = cur["daf_value_eoy"]
    agree = fwd is not None and bwd is not None and abs(fwd - bwd) <= ROLL_TOL * max(abs(fwd), abs(bwd))
    off = lambda v: v is not None and abs(filed - v) > ROLL_TOL * abs(v)  # noqa: E731
    verdict = ("filed fails roll-forward" if off(fwd) and off(bwd) else
               "filed consistent with roll-forward" if (fwd is not None and not off(fwd)) or (bwd is not None and not off(bwd)) else
               "untestable")
    implied = (fwd + bwd) / 2 if fwd is not None and bwd is not None else None
    return {"rho_t": r_t, "rho_next": r_n, "roll_forward": fwd, "roll_backward": bwd, "roll_mid": implied,
            "na_roll_forward": na_roll_fwd, "na_roll_backward": na_roll_bwd, "roll_verdict": verdict, "rolls_agree": int(agree),
            "filed_minus_roll_mid": filed - implied if implied is not None else None}


def screen_year(ein: str, fy: int, yrs: Mapping[int, Mapping | None]) -> dict:
    prev, cur, nxt = yrs.get(fy - 1), yrs.get(fy), yrs.get(fy + 1)
    base = {"ein": ein, "fiscal_year": fy}
    if not cur:
        return {**base, "status": "no_filed_990_year_t"}
    if cur.get("daf_value_eoy") is None:
        return {**base, "status": "no_sched_d_line4_year_t", **ids(prev, cur, nxt)}
    r = (ratio(prev), ratio(cur), ratio(nxt))
    if r[1] is None:
        return {**base, "status": "net_assets_nonpositive_or_missing_t", **ids(prev, cur, nxt)}
    if r[0] is None or r[2] is None or prev.get("daf_value_eoy") is None or nxt.get("daf_value_eoy") is None:
        return {**base, "status": "neighbour_missing", "ratio_t": r[1], **ids(prev, cur, nxt),
                "line4_t": cur["daf_value_eoy"], "net_assets_t": cur["net_assets_eoy"], **one_sided(prev, cur, nxt, r)}
    d_prev, d_next = r[1] - r[0], r[1] - r[2]
    brk = abs(d_prev) > BREAK_PTS and abs(d_next) > BREAK_PTS and (d_prev > 0) == (d_next > 0)
    c = tuple(share(y.get("daf_contributions"), y.get("contributions_total")) for y in (prev, cur, nxt))
    g = tuple(share(y.get("daf_grants"), y.get("grants_paid")) for y in (prev, cur, nxt))
    c_ok, g_ok = within_band(c[1], c[0], c[2], FLOW_PTS), within_band(g[1], g[0], g[2], FLOW_PTS)
    flows_ok = bool(c_ok) and bool(g_ok)
    ref = (r[0] + r[2]) / 2
    gap = cur["daf_value_eoy"] - ref * cur["net_assets_eoy"]
    pattern = brk and flows_ok
    out = {**base, **ids(prev, cur, nxt), "status": "tested",
           "line4_prev": prev["daf_value_eoy"], "line4_t": cur["daf_value_eoy"], "line4_next": nxt["daf_value_eoy"],
           "net_assets_prev": prev["net_assets_eoy"], "net_assets_t": cur["net_assets_eoy"], "net_assets_next": nxt["net_assets_eoy"],
           "ratio_prev": r[0], "ratio_t": r[1], "ratio_next": r[2], "dpts_vs_prev": d_prev, "dpts_vs_next": d_next,
           "ratio_break": int(brk), "contrib_share_prev": c[0], "contrib_share_t": c[1], "contrib_share_next": c[2],
           "grant_share_prev": g[0], "grant_share_t": g[1], "grant_share_next": g[2],
           "contrib_consistent": "" if c_ok is None else int(c_ok), "grants_consistent": "" if g_ok is None else int(g_ok),
           "npt_pattern": int(pattern), "gap_vs_neighbour_ratio": gap, "over_250m": int(pattern and abs(gap) > MIN_GAP),
           "contributions_t": cur.get("daf_contributions"), "grants_t": cur.get("daf_grants"),
           "other_funds_eoy_t": cur.get("other_funds_eoy"), "other_funds_eoy_prev": prev.get("other_funds_eoy"),
           "other_funds_eoy_next": nxt.get("other_funds_eoy")}
    return {**out, **(rollforward(prev, cur, nxt) if brk else {})}


def one_sided(prev, cur, nxt, r) -> dict:
    """Supplement for sponsor-years with only one usable neighbour (mostly FY2024, whose FY2025 return is not yet filed):
    the ratio test against that neighbour alone. Not the NPT pattern as defined; listed separately."""
    side = ((prev, r[0], "prev") if r[0] is not None and prev.get("daf_value_eoy") is not None else
            (nxt, r[2], "next") if r[2] is not None and nxt.get("daf_value_eoy") is not None else None)
    if not side:
        return {}
    y, ry, which = side
    gap = cur["daf_value_eoy"] - ry * cur["net_assets_eoy"]
    c = (share(y.get("daf_contributions"), y.get("contributions_total")), share(cur.get("daf_contributions"), cur.get("contributions_total")))
    g = (share(y.get("daf_grants"), y.get("grants_paid")), share(cur.get("daf_grants"), cur.get("grants_paid")))
    flows = all(a is not None and b is not None and abs(a - b) <= FLOW_PTS for a, b in (c, g))
    return {"one_sided_neighbour": which, "one_sided_ratio_neighbour": ry, "one_sided_dpts": r[1] - ry,
            "one_sided_gap": gap, "one_sided_flows_consistent": int(flows),
            "one_sided_flag": int(abs(r[1] - ry) > BREAK_PTS and abs(gap) > MIN_GAP and flows)}


def ids(prev, cur, nxt) -> dict:
    return {"oid_prev": (prev or {}).get("object_id"), "oid_t": (cur or {}).get("object_id"),
            "oid_next": (nxt or {}).get("object_id"), "tax_period_t": (cur or {}).get("tax_period")}


def panel_lookup(panel: Iterable[Mapping], items: Iterable[Mapping]) -> dict[tuple[str, int], dict]:
    corr = {(ein9(i["ein"]), int(i["fiscal_year"])): i for i in items
            if i["metric"] == "daf_assets_eoy" and i["applied"] == "1"}
    return {(ein9(r["ein"]), int(r["fiscal_year_end"])): {
        "name": r["name"], "type": r["type"], "dafrc_value": num(r["eoy_daf_assets"]), "dafrc_source": r["source_eoy_daf_assets"],
        "repo_value": num(corr[(ein9(r["ein"]), int(r["fiscal_year_end"]))]["corrected_value"])
        if (ein9(r["ein"]), int(r["fiscal_year_end"])) in corr else num(r["eoy_daf_assets"])}
        for r in panel if r["fiscal_year_end"].isdigit()}


SCREEN_FIELDS = ("ein", "name", "type", "fiscal_year", "tax_period_t", "status", "dafrc_source", "dafrc_value", "repo_value",
                 "line4_prev", "line4_t", "line4_next", "net_assets_prev", "net_assets_t", "net_assets_next",
                 "ratio_prev", "ratio_t", "ratio_next", "dpts_vs_prev", "dpts_vs_next", "ratio_break",
                 "contrib_share_prev", "contrib_share_t", "contrib_share_next", "grant_share_prev", "grant_share_t",
                 "grant_share_next", "contrib_consistent", "grants_consistent", "npt_pattern", "gap_vs_neighbour_ratio",
                 "over_250m", "contributions_t", "grants_t", "other_funds_eoy_prev", "other_funds_eoy_t", "other_funds_eoy_next",
                 "rho_t", "rho_next", "roll_forward", "roll_backward", "roll_mid", "na_roll_forward", "na_roll_backward",
                 "roll_verdict", "rolls_agree", "filed_minus_roll_mid", "one_sided_neighbour", "one_sided_ratio_neighbour",
                 "one_sided_dpts", "one_sided_gap", "one_sided_flows_consistent", "one_sided_flag",
                 "oid_prev", "oid_t", "oid_next", "xml_url_t")


def run_screen(panel, items, selected, cache) -> tuple[dict, ...]:
    pl = panel_lookup(panel, items)
    keys = sorted(k for k in pl if k[1] in SCREEN_FYS)
    eins = sorted({k[0] for k in keys})
    years = {e: {fy: year_record(selected.get((e, fy)), cache.get((selected.get((e, fy)) or {}).get("object_id")))
                 for fy in FETCH_FYS} for e in eins}
    rows = (dict(screen_year(e, fy, years[e]), **pl[(e, fy)]) for e, fy in keys)
    return tuple({**r, "xml_url_t": XML_URL.format(oid=r["oid_t"]) if r.get("oid_t") else ""} for r in rows)


def screen_report(rows: Sequence[Mapping]) -> str:
    tested = [r for r in rows if r["status"] == "tested"]
    by_status = {s: sum(1 for r in rows if r["status"] == s) for s in sorted({r["status"] for r in rows})}
    brk = [r for r in tested if r["ratio_break"]]
    pat = [r for r in tested if r["npt_pattern"]]
    big = sorted((r for r in pat if r["over_250m"]), key=lambda r: -abs(r["gap_vs_neighbour_ratio"]))
    big_brk_noflow = sorted((r for r in brk if not r["npt_pattern"] and abs(r["gap_vs_neighbour_ratio"]) > MIN_GAP),
                            key=lambda r: -abs(r["gap_vs_neighbour_ratio"]))
    fy_tab = [(fy, sum(1 for r in rows if r["fiscal_year"] == fy), sum(1 for r in tested if r["fiscal_year"] == fy),
               sum(1 for r in brk if r["fiscal_year"] == fy), sum(1 for r in pat if r["fiscal_year"] == fy),
               sum(1 for r in big if r["fiscal_year"] == fy),
               f"{sum(r['line4_t'] for r in tested if r['fiscal_year'] == fy) / 1e9:,.2f}")
              for fy in SCREEN_FYS]
    out = ["## S1 Coverage and counts by fiscal year",
           md_table(("FY", "DAFRC sponsor-years", "Tested (t-1, t, t+1 filed)", "Ratio break >10 pts both sides",
                     "NPT pattern (break + flows consistent)", "Pattern with |gap| > $250m", "Filed line 4 tested, $bn"), fy_tab),
           "", "Status counts: " + "; ".join(f"{k} {v}" for k, v in by_status.items()),
           f"Tested sponsor-years: {len(tested)}; ratio breaks: {len(brk)}; NPT pattern: {len(pat)}; "
           f"pattern breaks above $250m: {len(big)}; breaks above $250m failing only the flow test: {len(big_brk_noflow)}",
           f"Line 4 tested: ${sum(r['line4_t'] for r in tested) / 1e9:,.1f}bn of "
           f"${sum((r['dafrc_value'] or 0) for r in rows) / 1e9:,.1f}bn DAFRC FY2021-24 value",
           "", "## S2 NPT-pattern breaks above $250m, with roll-forward test ($m)",
           md_table(("Sponsor", "EIN", "FY", "Line 4 filed", "Net assets", "Ratio t-1 / t / t+1", "Gap vs neighbour ratio",
                     "Contrib share t-1/t/t+1", "Grant share t-1/t/t+1", "Roll fwd / bwd", "NA-change roll fwd / bwd", "Verdict",
                     "Rolls agree",
                     "Filed − roll mid"),
                    ((r["name"], r["ein"], r["fiscal_year"], m(r["line4_t"]), m(r["net_assets_t"]),
                      f"{pct(r['ratio_prev'])} / {pct(r['ratio_t'])} / {pct(r['ratio_next'])}", m(r["gap_vs_neighbour_ratio"]),
                      f"{pct(r['contrib_share_prev'], 0)}/{pct(r['contrib_share_t'], 0)}/{pct(r['contrib_share_next'], 0)}",
                      f"{pct(r['grant_share_prev'], 0)}/{pct(r['grant_share_t'], 0)}/{pct(r['grant_share_next'], 0)}",
                      f"{m(r.get('roll_forward'))} / {m(r.get('roll_backward'))}",
                      f"{m(r.get('na_roll_forward'))} / {m(r.get('na_roll_backward'))}", r.get("roll_verdict", ""),
                      "yes" if r.get("rolls_agree") else "no", m(r.get("filed_minus_roll_mid"))) for r in big)),
           "", "## S3 Ratio breaks above $250m that fail the flow-consistency test (not the NPT pattern; shown for completeness)",
           md_table(("Sponsor", "EIN", "FY", "Line 4 filed", "Net assets", "Ratio t-1 / t / t+1", "Gap", "Contrib share t-1/t/t+1",
                     "Grant share t-1/t/t+1", "Roll verdict"),
                    ((r["name"], r["ein"], r["fiscal_year"], m(r["line4_t"]), m(r["net_assets_t"]),
                      f"{pct(r['ratio_prev'])} / {pct(r['ratio_t'])} / {pct(r['ratio_next'])}", m(r["gap_vs_neighbour_ratio"]),
                      f"{pct(r['contrib_share_prev'], 0)}/{pct(r['contrib_share_t'], 0)}/{pct(r['contrib_share_next'], 0)}",
                      f"{pct(r['grant_share_prev'], 0)}/{pct(r['grant_share_t'], 0)}/{pct(r['grant_share_next'], 0)}",
                      r.get("roll_verdict", "")) for r in big_brk_noflow)),
           ]
    near = sorted((r for r in pat if not r["over_250m"] and abs(r["gap_vs_neighbour_ratio"]) > 50e6),
                  key=lambda r: -abs(r["gap_vs_neighbour_ratio"]))
    out += ["", "## S2b NPT-pattern breaks between $50m and $250m (below the listing threshold; context only, $m)",
            md_table(("Sponsor", "EIN", "FY", "Line 4 filed", "Net assets", "Ratio t-1 / t / t+1", "Gap", "Roll fwd / bwd", "Verdict"),
                     ((r["name"], r["ein"], r["fiscal_year"], m(r["line4_t"]), m(r["net_assets_t"]),
                       f"{pct(r['ratio_prev'])} / {pct(r['ratio_t'])} / {pct(r['ratio_next'])}", m(r["gap_vs_neighbour_ratio"]),
                       f"{m(r.get('roll_forward'))} / {m(r.get('roll_backward'))}", r.get("roll_verdict", "")) for r in near))]
    ones = sorted((r for r in rows if r.get("one_sided_flag") == 1), key=lambda r: -abs(r["one_sided_gap"]))
    n_one = sum(1 for r in rows if r.get("one_sided_neighbour"))
    out += ["", f"## S5 One-sided supplement: {n_one} sponsor-years with one usable neighbour; ratio moves >10 pts "
                f"against it with |gap| > $250m and consistent flows ($m)",
            md_table(("Sponsor", "EIN", "FY", "Neighbour", "Line 4 filed", "Net assets", "Ratio neighbour / t", "Gap"),
                     ((r["name"], r["ein"], r["fiscal_year"], r["one_sided_neighbour"], m(r["line4_t"]), m(r["net_assets_t"]),
                       f"{pct(r['one_sided_ratio_neighbour'])} / {pct(r['ratio_t'])}", m(r["one_sided_gap"])) for r in ones))]
    fails = [r for r in big if r.get("roll_verdict") == "filed fails roll-forward"]
    sens = {fy: sum(r["filed_minus_roll_mid"] for r in fails if r["fiscal_year"] == fy) for fy in SCREEN_FYS}
    out += ["", "## S4 Market effect if every break that fails the roll-forward were replaced by the roll-forward midpoint",
            md_table(("FY", "Breaks failing roll-forward", "Filed − roll midpoint, $m (negative = filed understated)"),
                     ((fy, sum(1 for r in fails if r["fiscal_year"] == fy), m(sens[fy])) for fy in SCREEN_FYS))]
    return "\n".join(out)


# ----------------------------------------------------------------------------- (B) realised fee rates: see FEE_EVIDENCE
def task_fees(root: str, args) -> int:
    raise SystemExit('fees: not yet implemented')


# ----------------------------------------------------------------------------- main
def panel_eins(panel: Iterable[Mapping]) -> frozenset[str]:
    return frozenset(ein9(r["ein"]) for r in panel if r["fiscal_year_end"].isdigit() and int(r["fiscal_year_end"]) in SCREEN_FYS)


def fetch_one(oid: str, local: Mapping[str, str], fetch: bool) -> dict:
    data, how = get_xml(oid, local, fetch)
    parsed = parse_xml_bytes(data) if data else {"parse": "none"}
    if how == "cache" and parsed.get("parse") != "ok":  # truncated local copy: fall back to the mirror
        data, how = get_xml(oid, {}, fetch)
        parsed = parse_xml_bytes(data) if data else {"parse": "none"}
    return {"object_id": oid, "xml_status": how, **parsed}


def task_fetch(root: str, args) -> int:
    panel = read_csv(os.path.join(root, PANEL))
    eins = panel_eins(panel) | frozenset(ein9(r["ein"]) for r in read_csv(os.path.join(root, CENSUS)))
    index = load_index(index_paths(args.irs_dir), eins)
    done = read_cache(args.cache)
    sel = selected_returns(index, eins)
    # a newest return missing from the mirror: also fetch the next-newest for that fiscal year
    backups = {c["object_id"] for e in eins for fy in FETCH_FYS for cands in (fy_candidates(index.get(e, ()), fy),)
               if cands and done.get(cands[0]["object_id"], {}).get("parse") not in (None, "ok") for c in cands[1:2]}
    todo = sorted(({r["object_id"] for r in sel.values()} | backups)
                  - {k for k, v in done.items() if v.get("parse") == "ok" or v.get("xml_status") == "http_404"})
    local = cached_xml_paths(args.xml_dir)
    print(f"sponsors {len(eins)}; selected returns {len(sel)}; cached parsed {len(done)}; to fetch {len(todo)}; "
          f"local XML copies {sum(1 for o in todo if o in local)}", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=args.workers) as ex, open(args.cache, "a", encoding="utf-8") as fh:
        for i, rec in enumerate(ex.map(lambda o: fetch_one(o, local, args.fetch), todo), 1):
            fh.write(json.dumps(rec) + "\n")
            if i % 250 == 0:
                fh.flush()
                print(f"  {i}/{len(todo)}", file=sys.stderr)
    return 0


def task_screen(root: str, args) -> int:
    panel = read_csv(os.path.join(root, PANEL))
    items = read_csv(os.path.join(root, ITEMS))
    eins = panel_eins(panel)
    cache = read_cache(args.cache)
    sel = selected_returns(load_index(index_paths(args.irs_dir), eins), eins, cache)
    rows = run_screen(panel, items, sel, cache)
    write_csv(os.path.join(root, args.out_screen), rows, SCREEN_FIELDS)
    xml_status = {}
    for o in {r["object_id"] for r in sel.values()}:  # local tally only
        s = cache.get(o, {}).get("xml_status", "not_fetched")
        xml_status[s] = xml_status.get(s, 0) + 1
    print(f"Selected FY2020-25 returns: {len(sel)}; XML status: {xml_status}; "
          f"fallback to next-newest return (newest not on mirror): {sum(1 for r in sel.values() if r.get('fallback'))}\n")
    print(screen_report(rows))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--task", choices=("fetch", "screen", "fees"), required=True)
    ap.add_argument("--irs-dir", action="append", default=[])
    ap.add_argument("--xml-dir", action="append", default=[])
    ap.add_argument("--cache", required=True, help="JSONL cache of parsed returns (outside the repo)")
    ap.add_argument("--text-dir", default="", help="cached text of fee sources (task fees)")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out-screen", default=OUT_SCREEN)
    ap.add_argument("--out-fees", default=OUT_FEES)
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    return {"fetch": task_fetch, "screen": task_screen, "fees": task_fees}[args.task](root, args)


if __name__ == "__main__":
    sys.exit(main())
