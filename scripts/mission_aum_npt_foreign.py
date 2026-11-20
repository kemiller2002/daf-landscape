#!/usr/bin/env python3
"""Assets Under Movement / Amalgamated Charitable Foundation and NPT's $39.1m Europe line (P-G050303-02, P-NPTREN-05).

Part A (P-G050303-02). EIN 82-1517696 (IRS EO BMF 2026-11: ASSETS UNDER MOVEMENT; filed name Amalgamated Charitable
Foundation Inc) is the largest of the five "added" de facto fiscal-sponsor hosts in mission_de_facto_fiscal_sponsors.py
($58.0m of the $114.6m addition). This script
  A1 reads its own FY2023 and FY2024 Form 990s (IRS TEOS e-file XML, cached copies or the GivingTuesday mirror):
     Part I, Part III (mission and program-service text), Part IV line 6 (DonorAdvisedFundInd), Part VII-B contractors,
     Part IX lines 1/3/7/11g/25, Part X line 16, Schedule D Part I (DAF counts and amounts), Schedule I (counts, $ and
     outbound lines to DAF-to-DAF whitelist sponsors), Schedule F, Schedule R, and every text field that says
     "fiscal" (fiscal-sponsorship language);
  A2 lists every top-50 FY2023-24 Schedule I line to the EIN (the unchanged mission_exception_refined.load_screened
     pipeline) with the filer's own PurposeOfGrantTxt (read from the filer's Schedule I XML) and classifies the line's
     evidence: project-style name (FBO), purpose naming a fiscal sponsorship, purpose naming a pooled fund or
     collaborative, purpose naming a DAF, or generic;
  A3 apportions the $58.0m between DAF pass-through and non-DAF (fiscally sponsored projects, pooled funds,
     unrestricted) on three bases taken from the recipient's own returns: DAF share of total assets (the
     whitelist rule W2 basis), DAF share of contributions (Schedule D line 2 / Part VIII line 1h) and DAF share of
     grants (Schedule D line 3 / Part IX lines 1-3), each per fiscal year;
  A4 re-cuts the fiscal-sponsor share, the core and broad unions, DAF-to-DAF dollars and the broad shares ex
     DAF-to-DAF under four scenarios: S0 as published (AUM added as a fiscal-sponsor host, not DAF-to-DAF); S1 AUM
     dropped from the addition; S2 AUM whitelisted as DAF-to-DAF and dropped from the addition; S3 AUM whitelisted
     and kept as a fiscal-sponsor host (the Tides Foundation precedent). Flags are rebuilt exactly as
     mission_de_facto_fiscal_sponsors.main does, with the imported functions of that script and of
     mission_exception_refined.py (neither is modified).

Part B (P-NPTREN-05). NPT's FY2025 (tax period ending 2025-06) Schedule F Part II line of $39,100,000 (Europe,
"ENVIRONMENT, ANIMALS", wire) is carried as a flagged candidate affiliate transfer (npt-ren-followups-2026-11-19.md
section 3.3). Top-50 foreign-grant totals (Form 990 Part IX line 3; Schedule F Part II cash) are reported with and
without it for: FY2024, the latest complete year (daf-foreign-grants-schedule-f-2023-2024.csv, unchanged); FY2025,
the top-50 sponsors whose FY2025 Form 990 is in the IRS TEOS index (parsed with mission_foreign_grants.parse_return /
load_extract); and a "latest available" splice (FY2025 where filed, else FY2024).

Pure functions; I/O only in `main` and the two loaders. Stdlib only.

Usage:
  python3 scripts/mission_aum_npt_foreign.py . --np-cache NP --lines-cache LINES --bmf-dir BMF --pub78 P78 \
      --revocation REV --efile-index-dir IRS --bmf-archive-dir ARCH --fsd-html FSD.html --extract-cache EC \
      --xml-dir DIR [--xml-dir DIR ...] [--fetch] [--out CSV]
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_de_facto_fiscal_sponsors as dff  # noqa: E402
import mission_exception_refined as mer  # noqa: E402
import mission_foreign_grants as mfg  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import TOP_N, top_n  # noqa: E402
from mission_recipient_sectors import WHITELIST  # noqa: E402

mel = mer.mel
OUT = os.path.join(DATA, "aum-npt-foreign-2026-11-20.csv")
AUM = "821517696"
AUM_RETURNS = {2023: "202413159349300006", 2024: "202543179349307759"}   # IRS TEOS index 2024 / 2025, 990
AUM_PRIOR = "202302999349302215"                                         # FY2022 990 (Schedule D roll-forward only)
NPT = "237825575"
NPT_FY2025 = "202601289349302480"   # IRS TEOS index 2026, tax period 202506
NPT_FY2024 = "202511339349301311"   # IRS TEOS index 2025, tax period 202406
NPT_LINE_USD = 39_100_000.0
FY_LINES_SOURCE = "daf-foreign-grants-schedule-f-2023-2024.csv"
UA = "research-script/1.0 (stdlib urllib)"
FIELDS = ("row_type", "section", "scope", "fiscal_year", "metric", "value", "unit", "detail", "evidence", "source_url")

FS_TXT = re.compile(r"\bFISCAL(LY)?\b")
DAF_TXT = re.compile(r"\bDONOR[ -]ADVISED\b|\bDAF\b")
FUND_TXT = re.compile(r"\bFUND\b|\bCOLLABORATIVE\b|\bINITIATIVE\b")


# ----------------------------------------------------------------------------- pure helpers
def lname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def row(row_type: str, section: str, scope: str, fy, metric: str, value, unit: str = "usd", detail: str = "",
        evidence: str = "C", url: str = "") -> dict:
    v = round(value, 6) if isinstance(value, float) and abs(value) < 10 else (round(value) if isinstance(value, float) else value)
    return {"row_type": row_type, "section": section, "scope": scope, "fiscal_year": fy, "metric": metric, "value": v,
            "unit": unit, "detail": detail, "evidence": evidence, "source_url": url}


def ratio(n, d):
    return (n / d) if (n is not None and d) else None


def grp_total(root, grp: str) -> float | None:
    g = next((e for e in root.iter() if lname(e.tag) == grp), None)
    t = next((c for c in g if lname(c.tag) == "TotalAmt"), None) if g is not None else None
    return num(t.text) if t is not None else None


def first_text(root, tag: str) -> str:
    e = next((e for e in root.iter() if lname(e.tag) == tag and e.text and e.text.strip()), None)
    return e.text.strip() if e is not None else ""


def all_text(root, tag: str) -> tuple:
    return tuple(e.text.strip() for e in root.iter() if lname(e.tag) == tag and e.text and e.text.strip())


def child(root, tag: str):
    return next((e for e in root.iter() if lname(e.tag) == tag), None)


def kids(el) -> dict:
    return reduce(lambda acc, c: {**acc, lname(c.tag): (acc[lname(c.tag)] + " " + c.text.strip())
                                  if lname(c.tag) in acc else c.text.strip()},
                  (c for c in el.iter() if c is not el and c.text and c.text.strip()), {})


def parse_aum(root, wl_include: frozenset) -> dict:
    """Fields of one AUM Form 990 (whole-document parse; the files are about 1 MB)."""
    f990 = child(root, "IRS990")
    sd, si, sf, sr = (child(root, t) for t in ("IRS990ScheduleD", "IRS990ScheduleI", "IRS990ScheduleF", "IRS990ScheduleR"))
    recips = tuple(kids(e) for e in si.iter() if lname(e.tag) == "RecipientTable") if si is not None else ()
    amt = lambda k: (num(k.get("CashGrantAmt")) or 0.0) + (num(k.get("NonCashAssistanceAmt")) or 0.0)  # noqa: E731
    to_wl = tuple(k for k in recips if ein9(k.get("RecipientEIN", "")) in wl_include)
    purposes = _group_by_fast((k.get("PurposeOfGrantTxt", "").strip().upper() for k in recips), lambda p: p)
    contractors = tuple(kids(e) for e in f990.iter() if lname(e.tag) == "ContractorCompensationGrp")
    fiscal = tuple((lname(e.tag), re.sub(r"\s+", " ", e.text.strip()))
                   for e in root.iter() if e.text and FS_TXT.search(e.text.upper()))
    sf_lines = tuple(kids(e) for e in sf.iter() if lname(e.tag) == "GrantsToOrgOutsideUSGrp") if sf is not None else ()
    related = tuple(kids(e).get("BusinessNameLine1Txt", "") for e in sr.iter()
                    if lname(e.tag).startswith(("IdDisregardedEntitiesGrp", "IdRelatedTaxExemptOrgGrp",
                                                "IdRelatedOrgTxblPartnershipGrp", "IdRelatedOrgTxblCorpTrGrp"))) \
        if sr is not None else ()
    return {
        "tax_period_end": first_text(root, "TaxPeriodEndDt"),
        "filer_name": first_text(child(root, "ReturnHeader"), "BusinessNameLine1Txt"),
        "mission": first_text(f990, "ActivityOrMissionDesc"),
        "mission_part3": first_text(f990, "MissionDesc"),
        "program_desc": " || ".join(all_text(f990, "Desc")),
        "program_expense": num(first_text(f990, "ExpenseAmt")), "program_grants": num(first_text(f990, "GrantAmt")),
        "part4_l6_daf_ind": first_text(f990, "DonorAdvisedFundInd"),
        "employees": num(first_text(f990, "TotalEmployeeCnt")),
        "contributions_l1h": num(first_text(f990, "CYContributionsGrantsAmt")),
        "total_revenue": num(first_text(f990, "CYTotalRevenueAmt")),
        "grants_paid_part1_l13": num(first_text(f990, "CYGrantsAndSimilarPaidAmt")),
        "ix_l1_domestic_orgs": grp_total(f990, "GrantsToDomesticOrgsGrp"),
        "ix_l3_foreign": grp_total(f990, "ForeignGrantsGrp"),
        "ix_l7_other_salaries": grp_total(f990, "OtherSalariesAndWagesGrp"),
        "ix_l11g_fees_other": grp_total(f990, "FeesForServicesOtherGrp"),
        "ix_l25_total_expenses": grp_total(f990, "TotalFunctionalExpensesGrp"),
        "total_assets_eoy": num(first_text(f990, "TotalAssetsEOYAmt")),
        "sd_daf_count": num(first_text(sd, "DonorAdvisedFundsHeldCnt")) if sd is not None else None,
        "sd_daf_contributions": num(first_text(sd, "DonorAdvisedFundsContriAmt")) if sd is not None else None,
        "sd_daf_grants": num(first_text(sd, "DonorAdvisedFundsGrantsAmt")) if sd is not None else None,
        "sd_daf_eoy_value": num(first_text(sd, "DonorAdvisedFundsVlEOYAmt")) if sd is not None else None,
        "sd_other_funds_count": num(first_text(sd, "FundsAndOtherAccountsHeldCnt")) if sd is not None else None,
        "sd_disclosed_legal_control": first_text(sd, "DisclosedOrgLegCtrlInd") if sd is not None else "",
        "sd_disclosed_charitable_only": first_text(sd, "DisclosedForCharitablePrpsInd") if sd is not None else "",
        "si_lines": len(recips), "si_usd": sum(amt(k) for k in recips),
        "si_501c3_cnt": num(first_text(si, "Total501c3OrgCnt")) if si is not None else None,
        "si_other_cnt": num(first_text(si, "TotalOtherOrgCnt")) if si is not None else None,
        "si_to_whitelist_lines": len(to_wl), "si_to_whitelist_usd": sum(amt(k) for k in to_wl),
        "si_to_whitelist_top": "; ".join(f"{k.get('BusinessNameLine1Txt', '')} ${amt(k):,.0f}"
                                         for k in sorted(to_wl, key=lambda k: -amt(k))[:5]),
        "si_top_purposes": "; ".join(f"{p or '(blank)'} ({len(v)})" for p, v in
                                     sorted(purposes.items(), key=lambda kv: -len(kv[1]))[:6]),
        "sf_present": int(sf is not None), "sf_part2_lines": len(sf_lines),
        "sf_part2_usd": sum(num(k.get("CashGrantAmt")) or 0.0 for k in sf_lines),
        "contractors_top": "; ".join(f"{k.get('BusinessNameLine1Txt', '')} [{k.get('ServicesDesc', '')}] "
                                     f"${num(k.get('CompensationAmt')) or 0:,.0f}" for k in contractors),
        "contractors_over_100k": num(first_text(f990, "CntrctRcvdGreaterThan100KCnt")),
        "related_orgs": "; ".join(sorted(set(r for r in related if r))),
        "fiscal_text": fiscal,
    }


def derived(x: Mapping, prior_daf_eoy: float | None) -> dict:
    grants = sum(v or 0.0 for v in (x["ix_l1_domestic_orgs"], x["ix_l3_foreign"]))
    roll = (prior_daf_eoy + x["sd_daf_contributions"] - x["sd_daf_grants"]) if prior_daf_eoy is not None else None
    return {"daf_share_assets": ratio(x["sd_daf_eoy_value"], x["total_assets_eoy"]),
            "daf_share_contributions": ratio(x["sd_daf_contributions"], x["contributions_l1h"]),
            "daf_share_grants": ratio(x["sd_daf_grants"], grants or x["grants_paid_part1_l13"]),
            "daf_rollforward_expected_eoy": roll,
            "daf_rollforward_gap": (x["sd_daf_eoy_value"] - roll) if roll is not None else None,
            "program_expense_ex_grants": (x["program_expense"] or 0) - (x["program_grants"] or 0)}


def evidence_class(name: str, purpose: str, fbo: bool) -> str:
    p = (purpose or "").upper()
    return ("project_style_fbo" if fbo else "purpose_fiscal_sponsorship" if FS_TXT.search(p) else
            "purpose_daf" if DAF_TXT.search(p) else "purpose_named_fund" if FUND_TXT.search(p) else "generic")


def apportion(lines: Sequence[Mapping], shares: Mapping, basis: str) -> float:
    """DAF-attributable $ of AUM's inbound lines: each line x the recipient's DAF share for the filer's fiscal year
    (FY2023 lines use AUM's CY2023 return, FY2024 lines its CY2024 return)."""
    return sum(l["amount"] * (shares[l["fy"]][basis] or 0.0) for l in lines)


def tally_ext(keys: Sequence, screened: Mapping, fl: Mapping, d2d: Mapping, fpart: Mapping) -> dict:
    t = reduce(mel.add, ({**mel.tally((r["amount"], f, dd) for r, f, dd in zip(screened[k], fl[k], d2d[k])), **fpart[k]}
                         for k in keys), {})
    s = mel.shares({**t, "d2d_usd": sum(r["amount"] for k in keys for r, dd in zip(screened[k], d2d[k]) if dd),
                    **{c: t.get(c, 0) for c in ("recent_ruling_after_period_end_lines", "recent_ruling_after_period_end_usd",
                                                "fiscal_sponsor_listed_usd", "irc_text_not_c3_usd", "er_required_lines",
                                                "er_required_usd", "pof_only_lines", "pof_only_usd")}})
    return {k: s[k] for k in ("denom_lines", "denom_usd", "fiscal_sponsor_name_lines", "fiscal_sponsor_name_usd",
                              "fiscal_sponsor_name_count_share", "fiscal_sponsor_name_usd_share", "any_core_lines",
                              "any_core_usd", "any_core_count_share", "any_core_usd_share", "any_lines", "any_usd",
                              "any_count_share", "any_usd_share", "any_count_share_ex_d2d", "any_usd_share_ex_d2d",
                              "d2d_usd")}


def sched_i_hits(stream, ein: str) -> tuple:
    """(name, amount, purpose) of every Schedule I RecipientTable row to `ein`; stops at the end of Schedule I."""
    out = []
    for _, el in ET.iterparse(stream):
        t = lname(el.tag)
        if t == "RecipientTable":
            k = kids(el)
            if ein9(k.get("RecipientEIN", "")) == ein:
                out.append((k.get("BusinessNameLine1Txt", ""), (num(k.get("CashGrantAmt")) or 0.0)
                            + (num(k.get("NonCashAssistanceAmt")) or 0.0), k.get("PurposeOfGrantTxt", "")))
            el.clear()
        elif t == "IRS990ScheduleI":
            break
    return tuple(out)


def match_purposes(lines: Sequence[Mapping], hits: Sequence[tuple]) -> tuple:
    """Attach the filer's purpose text to each cached line by amount (then name), in filing order."""
    def step(acc, l):
        used, out = acc
        i = next((j for j, h in enumerate(hits) if j not in used and abs(h[1] - l["amount"]) < 0.5
                  and mel.upname(h[0]) == mel.upname(l["name"])), None)
        i = i if i is not None else next((j for j, h in enumerate(hits) if j not in used and abs(h[1] - l["amount"]) < 0.5), None)
        return (used | {i} if i is not None else used, out + ({**l, "purpose": hits[i][2] if i is not None else ""},))
    return reduce(step, lines, (frozenset(), ()))[1]


def npt_part2(ex: Mapping) -> dict:
    p2 = tuple(ex.get("part2", ()))
    amt = lambda g: num(g.get("CashGrantAmt")) or 0.0  # noqa: E731
    eu = tuple(g for g in p2 if "EUROPE" in (g.get("RegionTxt", "") or "").upper())
    top = sorted(p2, key=lambda g: -amt(g))[:3]
    hit = tuple(g for g in p2 if abs(amt(g) - NPT_LINE_USD) < 0.5)
    return {"lines": len(p2), "usd": sum(amt(g) for g in p2), "europe_lines": len(eu), "europe_usd": sum(amt(g) for g in eu),
            "largest": "; ".join(f"${amt(g):,.0f} {g.get('RegionTxt', '')} / {g.get('PurposeOfGrantTxt', '')} / "
                                 f"{g.get('MannerOfCashDisbursementTxt', '')}" for g in top),
            "line_found": len(hit),
            "line_detail": "; ".join(f"{g.get('RegionTxt', '')} | {g.get('PurposeOfGrantTxt', '')} | "
                                     f"{g.get('MannerOfCashDisbursementTxt', '')} | {amt(g):,.0f}" for g in hit),
            "l3": (ex.get("ix") or {}).get("l3")}


def fy2025_returns(index_rows: Iterable[Mapping], eins: frozenset) -> dict:
    """{ein: (tax_period, oid)}: latest-filed Form 990 per EIN for tax periods ending in calendar 2025."""
    hits = tuple((ein9(r["EIN"]), r["TAX_PERIOD"], r["OBJECT_ID"]) for r in index_rows
                 if r.get("RETURN_TYPE") == "990" and (r.get("TAX_PERIOD") or "").startswith("2025") and ein9(r["EIN"]) in eins)
    by = _group_by_fast(hits, lambda h: h[0])
    return {e: max(((tp, o) for _, tp, o in v), key=lambda t: (t[0], t[1])) for e, v in by.items()}


# ----------------------------------------------------------------------------- loaders (I/O)
def xml_index(dirs: Sequence[str]) -> dict:
    return reduce(lambda acc, p: {**{os.path.basename(p).replace("_public", "")[:-4]: p}, **acc},
                  (p for d in dirs for p in sorted(glob.glob(os.path.join(d, "*.xml")))), {})


def open_xml(oid: str, paths: Mapping, fetch: bool):
    if oid in paths:
        return open(paths[oid], "rb"), "local"
    if not fetch:
        return None, "not_local"
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=600), "mirror"


def read_index(irs_dir: str, years: Sequence[int]) -> tuple:
    def one(y):
        p = os.path.join(irs_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple(csv.DictReader(fh))
    return tuple(r for y in years for r in one(y))


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    for f in ("--np-cache", "--lines-cache", "--bmf-dir", "--pub78", "--revocation", "--efile-index-dir",
              "--bmf-archive-dir", "--fsd-html", "--extract-cache"):
        ap.add_argument(f, required=True)
    ap.add_argument("--xml-dir", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)
    paths = xml_index(a.xml_dir)
    wl = read_csv(WHITELIST)
    wl_include = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    wl_aum = next((r for r in wl if ein9(r["recipient_ein"]) == AUM), {})

    # ---------------- A1 AUM's own returns
    def load_aum(oid):
        fh, via = open_xml(oid, paths, a.fetch)
        with fh:
            return {**parse_aum(ET.parse(fh).getroot(), wl_include), "oid": oid, "via": via}
    aum = {fy: load_aum(o) for fy, o in AUM_RETURNS.items()}
    prior = load_aum(AUM_PRIOR)
    der = {2023: derived(aum[2023], prior["sd_daf_eoy_value"]), 2024: derived(aum[2024], aum[2023]["sd_daf_eoy_value"])}

    # ---------------- A2/A4 lines and flags, rebuilt as mission_de_facto_fiscal_sponsors.main does
    d = mer.load_screened(a)
    screened, period, present, panel, good = (d[k] for k in ("screened", "period", "present", "panel", "good"))
    base_flags = {k: tuple(mel.line_flags(r, period[k]["start"], period[k]["end"]) for r in rs) for k, rs in screened.items()}
    with open(a.fsd_html, encoding="utf-8", errors="replace") as fh:
        entries = mer.fsd_entries(fh.read())
    nkeys = frozenset(mer.name_key(re.split(r"\bdba\b", n, flags=re.I)[0]) for _, n, _ in entries)
    cities = frozenset((mer.state_of(l), mer.city_of(l)) for _, _, l in entries)
    q_eins = frozenset(e for e, b in d["bmf"].items() if mel.FISCAL_SPONSORS.search(mel.upname(b["name"])))
    exact, by_city, _ = mer.load_bmf_names(a.bmf_dir, nkeys, cities, q_eins)
    line_eins = {k: frozenset(e for e, _ in v) for k, v in _group_by_fast(
        ((r["ein"], mer.name_key(r["name"])) for rs in screened.values() for r in rs if r["ein"]), lambda t: t[1]).items()}
    fsd_rows = tuple(mer.key_from_lines(mer.match_entry(e, exact, by_city), line_eins, d["bmf"]) for e in entries)
    q19 = mer.q19_rows({e: d["bmf"][e] for e in q_eins})
    q19 = q19 + mer.q19_reported(((r["ein"], mel.upname(r["name"])) for rs in screened.values() for r in rs),
                                 frozenset(r["ein"] for r in q19))
    fsx = mer.fs_index(q19 + fsd_rows)
    fsd_names = frozenset(mer.name_key(n) for _, n, _ in entries)
    rr_eins = frozenset(r["ein"] for k, rs in screened.items() for r, f in zip(rs, base_flags[k]) if "recent_ruling_24m" in f)
    arch, sizes, groups = mer.load_archives(a.bmf_archive_dir, rr_eins)
    months = mer.complete_months({m: n for m, n in sizes.items() if not m.startswith("L")})
    legacy = tuple(sorted(m for m in arch if m.startswith("L")))
    revs = mer.load_revocations(a.revocation, rr_eins)
    efile = mer.load_efile_first(a.efile_index_dir, rr_eins)
    rr = {k: tuple(mer.classify(r["ein"], mer.ym(r["bmf_ruling"]), period[k]["start"], period[k]["end"], arch, months,
                                legacy, revs, efile, groups.get(r["ein"], ""), "church_or_religious" in r["labels"])
                   if "recent_ruling_24m" in f else None for r, f in zip(rs, base_flags[k]))
          for k, rs in screened.items()}
    ref_flags = {k: tuple(mer.refined_flags(r, f, fsx, x, fsd_names)[0] for r, f, x in zip(rs, base_flags[k], rr[k]))
                 for k, rs in screened.items()}
    # the published added set (>= 3 projects, intermediary class, not already counted), recomputed
    bmf = d["bmf"]
    modal = dff.modal_plain((r["ein"], r["name"]) for rs in screened.values() for r in rs)
    dets = tuple({"sponsor_ein": k[0], "fy": k[1], "idx": i, "ein": r["ein"], **x}
                 for k, rs in screened.items() for i, r in enumerate(rs)
                 for x in (dff.detect(r["name"], r["ein"], bmf.get(r["ein"], {}).get("name", ""), modal.get(r["ein"], "")),)
                 if x and x["status"] == "valid")
    canon = {e: dff.merge_projects(x["project_key"] for x in v) for e, v in _group_by_fast(dets, lambda x: x["ein"]).items()}
    nproj = {e: len({canon[e][x["project_key"]] for x in v}) for e, v in _group_by_fast(dets, lambda x: x["ein"]).items()}
    _, _, ext = mer.load_bmf_names(a.bmf_dir, frozenset(), frozenset(), frozenset(nproj))
    cls = {e: dff.host_class(bmf.get(e, {}).get("name", "") or modal.get(e, ""), ext.get(e, {}).get("NTEE_CD", ""),
                             bmf.get(e, {}).get("foundation", ""), bmf.get(e, {}).get("group", "")) for e in nproj}
    counted = frozenset(e for e, v in fsx.items() if not v["grantmaker"])
    added = frozenset(e for e, n in nproj.items() if n >= dff.MIN_PROJECTS and cls[e] == "intermediary_other") - counted
    fbo_idx = frozenset((x["sponsor_ein"], x["fy"], x["idx"]) for x in dets if x["ein"] == AUM)

    sf_rows = {(ein9(r["ein"]), int(r["fiscal_year"])): r for r in read_csv(mel.SCHED_F_CSV) if r["row_type"] == "sponsor_year"}
    keys = tuple(k for k in present if k in good)
    sf = {k: mel.sched_f_of(sf_rows.get(k)) for k in keys}
    fpart = {k: {**{x: sf[k][x] for x in ("f_usd", "f_recipients", "f_other_org_cnt")},
                 "f_total_grants": sf[k].get("f_total_grants", 0.0)} for k in keys}
    st = lambda k: mel.sponsor_type(k[0], panel[k[0]]["segment"])  # noqa: E731
    scopes = {"all_top50_itemising": keys, "big4_nationals": tuple(k for k in keys if k[0] in mel.BIG4),
              "national": tuple(k for k in keys if st(k) == "national"),
              "community_foundation": tuple(k for k in keys if st(k) == "community_foundation"),
              "faith": tuple(k for k in keys if st(k) == "faith")}
    cut = lambda add: {k: tuple(dff.recut(f, r["ein"], add) for r, f in zip(screened[k], ref_flags[k])) for k in keys}  # noqa: E731
    d2d_base = {k: tuple(bool(r["d2d"]) for r in screened[k]) for k in keys}
    d2d_aum = {k: tuple(bool(r["d2d"]) or r["ein"] == AUM for r in screened[k]) for k in keys}
    with_d2d = lambda fl: {k: tuple(f | {"d2d"} if r["ein"] == AUM else f for r, f in zip(screened[k], fl[k])) for k in keys}  # noqa: E731
    others = added - {AUM}
    scen = {"R_refined_as_published": (ref_flags, d2d_base),
            "S0_published_de_facto": (cut(added), d2d_base),
            "S1_aum_dropped": (cut(others), d2d_base),
            "S2_aum_whitelisted_dropped": (with_d2d(cut(others)), d2d_aum),
            "S3_aum_whitelisted_kept": (with_d2d(cut(added)), d2d_aum)}
    res = {s: {sc: tally_ext(ks, screened, fl, dd, fpart) for sc, ks in scopes.items()} for s, (fl, dd) in scen.items()}

    # ---------------- A2 inbound lines with purposes
    inbound = tuple({"sponsor_ein": k[0], "sponsor": panel[k[0]]["name"], "fy": k[1], "oid": d["item"][k]["oid"],
                     "idx": i, "name": r["name"], "amount": r["amount"], "d2d": bool(r["d2d"]),
                     "fbo": (k[0], k[1], i) in fbo_idx,
                     "flags_refined": ";".join(sorted(f for f in ref_flags[k][i] if f in ("foreign_si", "not_c3_or_not_pub78",
                                               "recent_ruling_24m", "pf_or_er", "fiscal_sponsor_name", "any_core_si")))}
                    for k in keys for i, r in enumerate(screened[k]) if r["ein"] == AUM)

    def purposes_for(oid, ls):
        fh, via = open_xml(oid, paths, a.fetch)
        if fh is None:
            return tuple({**l, "purpose": "", "purpose_via": via} for l in ls)
        with fh:
            hits = sched_i_hits(fh, AUM)
        return tuple({**l, "purpose_via": via} for l in match_purposes(ls, hits))
    inbound = tuple(l for oid, ls in _group_by_fast(inbound, lambda l: l["oid"]).items() for l in purposes_for(oid, ls))
    inbound = tuple(sorted(({**l, "evidence_class": evidence_class(l["name"], l["purpose"], l["fbo"])} for l in inbound),
                           key=lambda l: (-l["amount"], l["sponsor_ein"], l["fy"], l["idx"])))
    tot_in = sum(l["amount"] for l in inbound)
    by_cls = {c: (len(v), sum(l["amount"] for l in v)) for c, v in _group_by_fast(inbound, lambda l: l["evidence_class"]).items()}
    by_sp = {s: (len(v), sum(l["amount"] for l in v)) for s, v in _group_by_fast(inbound, lambda l: l["sponsor"]).items()}
    shares_fy = {fy: der[fy] for fy in (2023, 2024)}
    app = {b: apportion(inbound, shares_fy, b) for b in ("daf_share_assets", "daf_share_contributions", "daf_share_grants")}
    explicit_non_daf = sum(l["amount"] for l in inbound if l["evidence_class"] in
                           ("project_style_fbo", "purpose_fiscal_sponsorship", "purpose_named_fund"))
    generic = sum(l["amount"] for l in inbound if l["evidence_class"] == "generic")
    app_generic = {b: apportion(tuple(l for l in inbound if l["evidence_class"] == "generic"), shares_fy, b) for b in app}

    # ---------------- B NPT line and top-50 foreign totals
    fcsv = read_csv(os.path.join(DATA, FY_LINES_SOURCE))
    tot = {int(r["fiscal_year"]): r for r in fcsv if r["row_type"] == "scope_total" and r["scope"] == "all_top50"}
    sy = {(ein9(r["ein"]), int(r["fiscal_year"])): r for r in fcsv if r["row_type"] == "sponsor_year"}
    rank = top_n(read_csv(DAFRC_CSV), TOP_N)
    idx = read_index(a.efile_index_dir, (2025, 2026))
    r25 = fy2025_returns(idx, frozenset(rank))
    local_paths = {o: paths[o] for _, o in r25.values() if o in paths}
    ex25 = {e: mfg.load_extract(o, a.extract_cache, local_paths, a.fetch) for e, (_, o) in r25.items()}
    ex_npt24 = mfg.load_extract(NPT_FY2024, a.extract_cache, {o: p for o, p in paths.items() if o == NPT_FY2024}, a.fetch)
    npt25 = npt_part2(ex25.get(NPT, {}))
    npt24 = npt_part2(ex_npt24)
    ok25 = {e: x for e, x in ex25.items() if x.get("status") == "ok"}
    l3_25 = {e: (x.get("ix") or {}).get("l3") or 0.0 for e, x in ok25.items()}
    p2_25 = {e: sum(num(g.get("CashGrantAmt")) or 0.0 for g in x.get("part2", ())) for e, x in ok25.items()}
    tg_25 = {e: sum((x.get("ix") or {}).get(k) or 0.0 for k in ("l1", "l2", "l3")) for e, x in ok25.items()}
    fy24_l3 = {e: num(sy[(e, 2024)]["part_ix_l3_foreign_usd"]) or 0.0 for e in rank if (e, 2024) in sy}
    fy24_p2 = {e: num(sy[(e, 2024)]["sched_f_part2_usd"]) or 0.0 for e in rank if (e, 2024) in sy}
    fy24_tg = {e: num(sy[(e, 2024)]["total_grants_usd"]) or 0.0 for e in rank if (e, 2024) in sy}
    splice_l3 = sum(l3_25.get(e, fy24_l3.get(e, 0.0)) for e in rank)
    splice_p2 = sum(p2_25.get(e, fy24_p2.get(e, 0.0)) for e in rank)
    splice_tg = sum(tg_25.get(e, fy24_tg.get(e, 0.0)) for e in rank)
    same24_l3 = sum(fy24_l3.get(e, 0.0) for e in ok25)
    npt_in = NPT in ok25 and npt25["line_found"] == 1

    # ---------------- rows
    U = lambda oid: XML_URL.format(oid=oid)  # noqa: E731
    rows = []
    for fy, x in aum.items():
        u = U(x["oid"])
        rows += [row("aum_return", "A1", "aum", fy, k, x[k], unit, "", "F", u) for k, unit in (
            ("tax_period_end", "date"), ("filer_name", "text"), ("part4_l6_daf_ind", "flag"), ("sd_daf_count", "count"),
            ("sd_daf_contributions", "usd"), ("sd_daf_grants", "usd"), ("sd_daf_eoy_value", "usd"),
            ("sd_other_funds_count", "count"), ("sd_disclosed_legal_control", "flag"), ("sd_disclosed_charitable_only", "flag"),
            ("contributions_l1h", "usd"), ("total_revenue", "usd"), ("grants_paid_part1_l13", "usd"),
            ("ix_l1_domestic_orgs", "usd"), ("ix_l3_foreign", "usd"), ("ix_l7_other_salaries", "usd"),
            ("ix_l11g_fees_other", "usd"), ("ix_l25_total_expenses", "usd"), ("total_assets_eoy", "usd"),
            ("employees", "count"), ("program_expense", "usd"), ("program_grants", "usd"), ("si_lines", "count"),
            ("si_usd", "usd"), ("si_501c3_cnt", "count"), ("si_other_cnt", "count"), ("si_to_whitelist_lines", "count"),
            ("si_to_whitelist_usd", "usd"), ("si_to_whitelist_top", "text"), ("si_top_purposes", "text"),
            ("sf_present", "flag"), ("sf_part2_lines", "count"), ("sf_part2_usd", "usd"), ("contractors_top", "text"),
            ("contractors_over_100k", "count"), ("related_orgs", "text"), ("mission", "text"), ("mission_part3", "text"),
            ("program_desc", "text"))]
        rows += [row("aum_fiscal_text", "A1", "aum", fy, f"fiscal_text_{i + 1}", t, "text", tag, "F", u)
                 for i, (tag, t) in enumerate(x["fiscal_text"])]
        rows += [row("aum_derived", "A1", "aum", fy, k, v, "share" if "share" in k else "usd",
                     "Schedule D line 1 / Part X line 16; line 2 / Part VIII 1h; line 3 / Part IX 1-3; roll-forward = prior EOY "
                     "+ contributions - grants (Schedule D lines 2-4)", "C", u) for k, v in der[fy].items()]
    rows += [row("aum_return", "A1", "aum", 2022, "sd_daf_eoy_value", prior["sd_daf_eoy_value"], "usd", "prior-year EOY, for roll-forward",
                 "F", U(AUM_PRIOR))]
    rows += [row("aum_whitelist", "A3", "aum", "2022-2024", k, wl_aum.get(k, ""), "text" if k in ("decision", "rule", "reason") else "share",
                 "daf-to-daf-recipient-whitelist.csv (unchanged)", "F") for k in
             ("decision", "rule", "reason", "daf_share_of_total_assets", "daf_share_of_grants")]
    rows += [row("aum_inbound_line", "A2", l["sponsor"], l["fy"], f"line_{l['sponsor_ein']}_{l['idx']}", l["amount"], "usd",
                 json.dumps({"filed_name": l["name"], "purpose": l["purpose"], "evidence_class": l["evidence_class"],
                             "fbo_detection": l["fbo"], "d2d": l["d2d"], "refined_flags": l["flags_refined"],
                             "purpose_via": l["purpose_via"]}, ensure_ascii=False), "F", U(l["oid"])) for l in inbound]
    rows += [row("aum_inbound_summary", "A2", "aum", "2023-2024", k, v, u) for k, v, u in (
        ("lines", len(inbound), "count"), ("usd", tot_in, "usd"), ("sponsors", len(by_sp), "count"),
        ("explicit_non_daf_usd", explicit_non_daf, "usd"), ("generic_usd", generic, "usd"))]
    rows += [row("aum_inbound_by_class", "A2", c, "2023-2024", "lines|usd", f"{n}|{round(u)}", "count|usd") for c, (n, u) in sorted(by_cls.items())]
    rows += [row("aum_inbound_by_sponsor", "A2", s, "2023-2024", "lines|usd", f"{n}|{round(u)}", "count|usd")
             for s, (n, u) in sorted(by_sp.items(), key=lambda kv: -kv[1][1])]
    rows += [row("aum_apportion", "A3", "aum", "2023-2024", f"daf_attributable_usd__{b}", v, "usd",
                 f"non-DAF remainder {tot_in - v:,.0f}; generic lines only: DAF {app_generic[b]:,.0f}") for b, v in app.items()]
    for s, by in res.items():
        rows += [row("proxy_scenario", "A4", sc, "2023-2024", f"{s}__{m}", v, "share" if "share" in m else
                     ("count" if "lines" in m else "usd")) for sc, t in by.items() for m, v in t.items()]
    rows += [row("de_facto_addition", "A4", "all_top50_itemising", "2023-2024", f"{nm}__{m}", v, u) for nm, es in
             (("published_5_hosts", added), ("ex_aum_4_hosts", others), ("aum_only", frozenset({AUM})))
             for m, v, u in (("eins", len(es), "count"),
                             ("lines", sum(1 for k in keys for r in screened[k] if r["ein"] in es), "count"),
                             ("usd", sum(r["amount"] for k in keys for r in screened[k] if r["ein"] in es), "usd"))]
    # B
    for nm, x, oid, fy in (("npt_fy2025", npt25, NPT_FY2025, 2025), ("npt_fy2024", npt24, NPT_FY2024, 2024)):
        rows += [row("npt_sched_f", "B", "npt", fy, k, v, "count" if k.endswith(("lines", "found")) else
                     ("text" if k in ("largest", "line_detail") else "usd"), "", "F/C", U(oid)) for k, v in x.items()]
    rows += [row("npt_sched_f", "B", "npt", 2025, "candidate_share_of_l3", ratio(NPT_LINE_USD, npt25["l3"]), "share",
                 "$39.1m / FY2025 Part IX line 3", "C", U(NPT_FY2025))]
    r24 = tot[2024]
    rows += [row("foreign_totals", "B", "all_top50", 2024, m, v, u, d_, "F/C", "") for m, v, u, d_ in (
        ("sponsors", 50, "count", "top-50; FY2024 returns as in the 2023-2024 CSV"),
        ("part_ix_l3_foreign_usd", num(r24["part_ix_l3_foreign_usd"]), "usd", "unchanged; the $39.1m line is FY2025, not FY2024"),
        ("part_ix_l3_foreign_usd_ex_candidate", num(r24["part_ix_l3_foreign_usd"]), "usd", "identical: line not in FY2024"),
        ("sched_f_part2_usd", num(r24["sched_f_part2_usd"]), "usd", ""),
        ("total_grants_usd", num(r24["total_grants_usd"]), "usd", ""),
        ("foreign_share_of_grants", ratio(num(r24["part_ix_l3_foreign_usd"]), num(r24["total_grants_usd"])), "share", ""))]
    l3s, p2s, tgs = sum(l3_25.values()), sum(p2_25.values()), sum(tg_25.values())
    sub = NPT_LINE_USD if npt_in else 0.0
    rows += [row("foreign_totals", "B", "top50_with_fy2025_return", 2025, m, v, u, d_, "C", "") for m, v, u, d_ in (
        ("sponsors", len(ok25), "count", f"{len(r25)} of 50 top-50 sponsors have a FY2025 Form 990 in the TEOS index (2025-2026)"),
        ("sponsor_eins", ";".join(sorted(ok25)), "text", ""),
        ("part_ix_l3_foreign_usd", l3s, "usd", "with the $39.1m NPT line"),
        ("part_ix_l3_foreign_usd_ex_candidate", l3s - sub, "usd", "without it"),
        ("candidate_share_of_l3", ratio(sub, l3s), "share", ""),
        ("sched_f_part2_usd", p2s, "usd", "with"), ("sched_f_part2_usd_ex_candidate", p2s - sub, "usd", "without"),
        ("total_grants_usd", tgs, "usd", "Part IX lines 1-3"),
        ("foreign_share_of_grants", ratio(l3s, tgs), "share", "with"),
        ("foreign_share_of_grants_ex_candidate", ratio(l3s - sub, tgs - sub), "share", "without (line removed from numerator and denominator)"),
        ("same_sponsors_fy2024_part_ix_l3_usd", same24_l3, "usd", "the same sponsors' FY2024 line 3, for growth"))]
    rows += [row("foreign_totals", "B", "all_top50_latest_available", "2025|2024", m, v, u, d_, "C", "") for m, v, u, d_ in (
        ("part_ix_l3_foreign_usd", splice_l3, "usd", f"FY2025 for {len(ok25)} sponsors, FY2024 for the rest"),
        ("part_ix_l3_foreign_usd_ex_candidate", splice_l3 - sub, "usd", "without the $39.1m line"),
        ("candidate_share_of_l3", ratio(sub, splice_l3), "share", ""),
        ("sched_f_part2_usd", splice_p2, "usd", "with"), ("sched_f_part2_usd_ex_candidate", splice_p2 - sub, "usd", "without"),
        ("total_grants_usd", splice_tg, "usd", ""),
        ("foreign_share_of_grants", ratio(splice_l3, splice_tg), "share", "with"),
        ("foreign_share_of_grants_ex_candidate", ratio(splice_l3 - sub, splice_tg - sub), "share", "without"))]
    rows += [row("foreign_fy2025_sponsor", "B", e, 2025, "l3|part2|total_grants|fy2024_l3",
                 f"{round(l3_25[e])}|{round(p2_25[e])}|{round(tg_25[e])}|{round(fy24_l3.get(e, 0))}", "usd", f"rank {rank[e]}; tax period {r25[e][0]}; via {ok25[e].get('via', '')}",
                 "F", U(r25[e][1])) for e in sorted(ok25, key=lambda e: rank[e])]
    rows += [row("foreign_fy2025_sponsor", "B", e, 2025, "status", ex25[e].get("status"), "text", "", "C", U(r25[e][1]))
             for e in sorted(set(ex25) - set(ok25))]
    write_csv(a.out, rows, FIELDS)

    summary = {
        "aum": {fy: {k: v for k, v in x.items() if k not in ("fiscal_text",)} for fy, x in aum.items()},
        "aum_fiscal_text": {fy: x["fiscal_text"] for fy, x in aum.items()},
        "aum_derived": der, "aum_prior_daf_eoy": prior["sd_daf_eoy_value"], "whitelist_row": {k: wl_aum.get(k) for k in
                                                                                              ("decision", "rule", "reason", "daf_share_of_total_assets", "daf_share_of_grants")},
        "inbound_lines": len(inbound), "inbound_usd": round(tot_in), "inbound_by_class": by_cls, "inbound_by_sponsor": by_sp,
        "inbound_purposes": [(l["sponsor"][:30], l["fy"], l["name"], l["amount"], l["purpose"], l["evidence_class"], l["flags_refined"])
                             for l in inbound],
        "apportion": app, "apportion_generic": app_generic, "explicit_non_daf_usd": explicit_non_daf, "generic_usd": generic,
        "added": sorted(added), "scenarios": res,
        "npt25": npt25, "npt24": npt24, "fy2025_returns": {e: list(v) for e, v in r25.items()},
        "fy2025_ok": len(ok25), "l3_25": l3s, "p2_25": p2s, "tg_25": tgs, "same24_l3": same24_l3,
        "splice_l3": splice_l3, "splice_p2": splice_p2, "splice_tg": splice_tg, "npt_line_in_fy2025": npt_in,
        "fy2024_total": {k: r24[k] for k in ("part_ix_l3_foreign_usd", "sched_f_part2_usd", "total_grants_usd")},
        "rows": len(rows),
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
