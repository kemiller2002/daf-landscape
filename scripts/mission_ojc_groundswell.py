#!/usr/bin/env python3
"""Audit of the OJC Fund's FY2023-24 Schedule I in the church block (P-B4026-06-01-01) and of Groundswell Charitable
Foundation's TY2024 Schedule D Part I accounts (P-P0503-1915-02). Task b4026-0601-01-p0503.

Part A (OJC Fund, EIN 113618879)
  Rebuilds the b4026-06-01 frame exactly as scripts/mission_faith_sponsors_outside.py does (same caches, same imported
  functions; S0-S3 reproduce its CSV), then:
  * classifies every OJC Schedule I line (FY2023 oid 202411369349313111, FY2024 oid 202521359349314057) by BMF
    SUBSECTION / FOUNDATION and name: netted DAF sponsor, other DAF sponsor, federation, church block, other
    church-coded, other public charity, no BMF match;
  * sub-types church-block recipients with an Orthodox-aware name rule (FINE_RX: school/yeshiva, chesed or relief
    fund, communal umbrella, congregation, unclassified), first match wins, and also reports the base rtype;
  * measures money flowing INTO the OJC Fund from other DAFRC panel sponsors' Schedule I (lines netted as
    DAF-to-DAF in the frame) and the overlap of OJC block recipients with other sponsors;
  * recomputes the block faith share (S2, S3) with flagged lines excluded: OJC-only exclusions and symmetric
    exclusions applied to every sponsor's block lines.
Part B (Groundswell Charitable Foundation, EIN 871530516)
  Reads the amended TY2024 Form 990 (oid 202640289349301029) from the GivingTuesday mirror and pages of
  www.groundswell.io after a robots.txt check, and records the tags and verbatim snippets that bear on whether its
  12,808 Schedule D Part I accounts are donor-advised funds in the DAFRC sense.

Pure functions; I/O only in fetch/load helpers and `main`. Stdlib only. The base scripts are imported, not modified.

Usage:
  python3 scripts/mission_ojc_groundswell.py . --np-cache NPCACHE --lines-cache-top50 RCP_LINES \
      --lines-cache Q120201_LINES --bmf-dir BMF --index-dir IRSDIR --outreach-dir OUTREACH --np-work Q2661 \
      --work QOJC [--fetch]
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import urllib.robotparser
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_faith_sponsors_outside as fso  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, read_csv, write_csv  # noqa: E402

OUT = os.path.join(DATA, "ojc-groundswell-audit-2026-11-20.csv")
UA = "research-script/1.0"
OJC = "113618879"
OJC_OIDS = {"202411369349313111": 2023, "202521359349314057": 2024}
GS = "871530516"
GS_OID = "202640289349301029"
GS_PAGES = ("faq", "legal/terms", "products/giving", "pricing", "employee-assistance", "daf", "phaas")
GS_BASE = "https://www.groundswell.io/"

FINE = (
    ("school_yeshiva", r"SCHOOL|ACADEMY|YESHIV|SEMINARY|KOLLEL|KOLEL|MESIVTA|MESIFTA|TALMUD|BAIS YAAKOV|BETH JACOB|"
                       r"BNOS|CHEDER|CHEIDER|MOSDOT|MOSDOS|\bUTA\b|TORAH V ?YIRAH|TORAH VEYIRAH|CHINUCH|"
                       r"BAIS MEDRASH|BETH MEDRASH|BEIS MEDRASH|PRESCHOOL|DAY CARE|INSTITUTIONS"),
    ("chesed_or_relief_fund", r"KEREN|CHESED|CHASDEI|CHASDE\b|CHASODIM|GEMACH|GEMILUS|GEMILUT|TZEDAK|TZDOK|ZTADUK|"
                              r"TZDAK|TZEDOK|EZRA\b|EZRAS|EZRAH|REFUAH|RFUAH|BIKUR|HATZOL|HATZAL|HELPLINE|\bFUND\b|"
                              r"RELIEF|HACHNOSAS|KALLAH|YESOMIM|ALMANOS|MAOS|PIDYON|TOMCHE|ACHIEZER|ACHIAZER|\bYAD |"
                              r"LENITZRUCHIM|MIFAL|LEPLEITOS|SHEMESH|VCHESED|CHAYIM|ROFEH|CHOLIM|AID\b|CHARIT"),
    ("communal_umbrella", r"CENTRAL CONGREGATIONS|CENTRAL UTA|\bVAAD\b|AGUDA|COUNCIL|KAHAL ADAS|ASSOCIATION|UNION OF"),
    ("congregation", r"CHURCH|PARISH|CONGREGATION|SYNAGOGUE|\bTEMPLE|MASJID|MOSQUE|CHAPEL|TABERNACLE|\bSHUL\b|"
                     r"CATHEDRAL|BASILICA|\bCONG\b|ANSHE|\bBETH\b|\bBAIS\b|\bBEIS\b|\bBNAI|AHAVAS|AHAVATH|\bKHAL\b|"
                     r"\bKEHAL|\bKEHIL|\bOHEL\b|\bADAS\b|MINYAN|NUSACH|KLOIZ|SHTIEBEL|FELLOWSHIP\b|ASSEMBLY\b|"
                     r"IGLESIA|MINISTR|WORSHIP|HOUSE OF PRAYER"),
)
FINE_RX = tuple((t, re.compile(p)) for t, p in FINE)
FED_RX = re.compile(r"FEDERATION|\bUJA\b|UNITED JEWISH (APPEAL|FEDERATION|COMMUNIT|ASSOCIATION)|JEWISH UNITED FUND|"
                    r"ASSOCIATED JEWISH|JEWISH COMMUNAL FUND|JEWISH COMMUNITY FOUNDATION")
DAF_RX = re.compile(r"DONORS FUND|DONORS' FUND|MATBIA|GIFT FUND|GIFT FND|DONOR ADVISED|ACHISOMOCH|NATIONAL CHRISTIAN|"
                    r"SCHWAB CHARITABLE|VANGUARD CHARITABLE|AMERICA GIVES|PAYPAL CHARITABLE|BENEVITY|NETWORK FOR GOOD|"
                    r"CHARITABLE GIVING FUND|ENDOWMENT FUNDS|\bOJC\b")
NON_CONG = ("school_yeshiva", "chesed_or_relief_fund", "communal_umbrella", "unclassified")
SRC_A = ("IRS Form 990 Schedule I Part II FY2023-24 (GivingTuesday mirror of IRS TEOS e-file XML, oids 202411369349313111 "
         "and 202521359349314057 for the OJC Fund; panel caches of b40n1202-01); IRS EO BMF (www.irs.gov/charities-non-"
         "profits/exempt-organizations-business-master-file-extract-eo-bmf); DAFRC 2025 dataset")
SRC_B = ("Groundswell Charitable Foundation amended TY2024 Form 990, https://gt990datalake-rawdata.s3.amazonaws.com/"
         "EfileData/XmlFiles/202640289349301029_public.xml; www.groundswell.io pages as named")
FIELDS = ("section", "scenario", "key", "label", "detail", "category", "recipients", "lines", "usd_schedule_i",
          "usd_daf_weighted", "share", "value", "note", "source")


# ----------------------------------------------------------------------------- pure: classification
def fine_type(name: str) -> str:
    u = re.sub(r"[^A-Z0-9' ]", " ", name.upper())
    return next((t for t, rx in FINE_RX if rx.search(u)), "unclassified")


def ojc_bucket(r: Mapping, bmf: Mapping, block: frozenset, church: frozenset, panel: Mapping) -> str:
    e, u = r["ein"], r["name"].upper()
    if r["d2d"]:
        return "daf_sponsor_netted"
    if e in panel or DAF_RX.search(u):
        return "daf_sponsor_not_netted"
    if FED_RX.search(u):
        return "federation"
    if e in block:
        return "church_block"
    if e in church:
        return "church_coded_not_block"
    if e in bmf:
        return f"bmf_{bmf[e]['subsection']}_{bmf[e]['foundation']}"
    return "no_bmf_match" if e else "blank_ein"


def mk(section, scenario="", key="", label="", detail="", category="", recipients="", lines="", si="", dw="", share="",
       value="", note="", source=SRC_A):
    r = lambda x, n=0: round(x, n) if isinstance(x, float) else x  # noqa: E731
    return {"section": section, "scenario": scenario, "key": key, "label": label, "detail": detail, "category": category,
            "recipients": recipients, "lines": lines, "usd_schedule_i": r(si), "usd_daf_weighted": r(dw),
            "share": r(share, 5), "value": r(value, 5) if isinstance(value, float) else value, "note": note,
            "source": source}


def faith_share(ls: Sequence[Mapping]) -> tuple:
    tot = sum(l["dw"] for l in ls)
    f = sum(l["dw"] for l in ls if l["group"] in fso.FAITH_GROUPS)
    n = sum(l["dw"] for l in ls if l["group"] == "national")
    return tot, (f / tot if tot else None), (n / tot if tot else None)


def variants(bl: Sequence[Mapping], ftype: Mapping) -> tuple:
    """(name, predicate-to-keep, description). Predicates drop lines from numerator and denominator alike."""
    is_ojc = lambda l: l["sponsor"] == OJC  # noqa: E731
    t = lambda l: ftype.get(l["rec"], "unclassified")  # noqa: E731
    return (("central", lambda l: True, "b4026-06-01 as published"),
            ("excl_ojc_all", lambda l: not is_ojc(l), "drop every OJC line"),
            ("excl_ojc_school", lambda l: not (is_ojc(l) and t(l) == "school_yeshiva"), "drop OJC lines to school/yeshiva names"),
            ("excl_ojc_school_chesed", lambda l: not (is_ojc(l) and t(l) in ("school_yeshiva", "chesed_or_relief_fund")),
             "drop OJC lines to school/yeshiva and chesed/relief-fund names"),
            ("ojc_congregations_only", lambda l: not (is_ojc(l) and t(l) in NON_CONG),
             "keep only OJC lines to congregation names (drop school, fund, umbrella, unclassified)"),
            ("sym_excl_school_chesed", lambda l: t(l) not in ("school_yeshiva", "chesed_or_relief_fund"),
             "drop every sponsor's block lines to school/yeshiva and chesed/relief-fund names"),
            ("sym_congregations_only", lambda l: t(l) == "congregation",
             "every sponsor: only block recipients with congregation names (fine rule)"))


def ojc_rows(frame: Mapping, bmfx: Mapping) -> list:
    ann, block, church, panel, flat = frame["ann"], frame["block"], frame["church"], frame["panel"], frame["flat"]
    bmf = frame["bmf"]
    o_lines = tuple({**r, "fy": k[1], "oid": frame["oid"][k]} for k, rs in ann.items() if k[0] == OJC for r in rs)
    w = {k[1]: frame["weights"][k] for k in ann if k[0] == OJC}
    o_lines = tuple({**r, "w": w[r["fy"]], "bucket": ojc_bucket(r, bmf, block, church, panel),
                     "ftype": fine_type(r["name"]) if r["ein"] in block else ""} for r in o_lines)
    pos = tuple(r for r in o_lines if r["amount"] > 0)
    tot_si = sum(r["amount"] for r in pos)
    out = [mk("ojc:return", "", f"FY{fy}", "THE OJC FUND", f"oid {oid}", "", "", sum(1 for r in o_lines if r["fy"] == fy),
              sum(r["amount"] for r in pos if r["fy"] == fy), sum(r["amount"] * r["w"] for r in pos if r["fy"] == fy),
              "", w[fy], "value = DAF weight used in the frame (sponsor-cost-structure DAF share of grants)")
           for oid, fy in sorted(OJC_OIDS.items(), key=lambda kv: kv[1])]
    by_b = _group_by_fast(pos, lambda r: r["bucket"])
    out += [mk("ojc:bucket", "FY2023-24", b, category=b, recipients=len({r['key'] for r in v}), lines=len(v),
               si=sum(r["amount"] for r in v), dw=sum(r["amount"] * r["w"] for r in v),
               share=sum(r["amount"] for r in v) / tot_si,
               note="share = share of OJC's positive Schedule I $ (unweighted); bmf_SS_FF = BMF SUBSECTION_FOUNDATION")
            for b, v in sorted(by_b.items(), key=lambda kv: -sum(r["amount"] for r in kv[1]))]
    bl = tuple(r for r in pos if r["bucket"] == "church_block")
    bl_dw = sum(r["amount"] * r["w"] for r in bl)
    by_t = _group_by_fast(bl, lambda r: r["ftype"])
    out += [mk("ojc:block_fine_type", "FY2023-24", t, category=t, recipients=len({r['ein'] for r in v}), lines=len(v),
               si=sum(r["amount"] for r in v), dw=sum(r["amount"] * r["w"] for r in v),
               share=sum(r["amount"] * r["w"] for r in v) / bl_dw,
               note="church-block recipients of OJC by Orthodox-aware name rule (FINE_RX, first match wins); share of OJC block dw")
            for t, v in sorted(by_t.items(), key=lambda kv: -sum(r["amount"] for r in kv[1]))]
    by_bt = _group_by_fast(bl, lambda r: fso.mcr.rtype_of(r["name"], False))
    out += [mk("ojc:block_base_rtype", "FY2023-24", t, category=t, recipients=len({r['ein'] for r in v}), lines=len(v),
               si=sum(r["amount"] for r in v), dw=sum(r["amount"] * r["w"] for r in v),
               share=sum(r["amount"] * r["w"] for r in v) / bl_dw, note="base study name rules (no Outreach override)")
            for t, v in sorted(by_bt.items(), key=lambda kv: -sum(r["amount"] for r in kv[1]))]
    # BMF attributes of block recipients ($-weighted)
    recs = _group_by_fast(bl, lambda r: r["ein"])
    rec_dw = {e: sum(r["amount"] * r["w"] for r in v) for e, v in recs.items()}
    attr = lambda f: _group_by_fast(rec_dw.items(), lambda kv: f(bmfx.get(kv[0], {})))  # noqa: E731
    ruling_band = lambda b: ("missing" if not (b.get("ruling") or "").strip("0") else  # noqa: E731
                             "<2000" if b["ruling"][:4] < "2000" else "2000-2009" if b["ruling"][:4] < "2010" else
                             "2010-2017" if b["ruling"][:4] < "2018" else "2018+")
    for nm, f in (("ruling_year", ruling_band), ("ntee", lambda b: b.get("ntee") or "blank"),
                  ("state", lambda b: b.get("state") or "?"), ("deductibility", lambda b: b.get("deductibility") or "?"),
                  ("filing_req", lambda b: b.get("filing_req") or "?")):
        g = attr(f)
        out += [mk("ojc:block_bmf_attr", "FY2023-24", f"{nm}={k}", category=nm, recipients=len(v),
                   dw=sum(x for _, x in v), share=sum(x for _, x in v) / bl_dw,
                   note="BMF attribute of OJC church-block recipients, share of OJC block dw")
                for k, v in sorted(g.items(), key=lambda kv: -sum(x for _, x in kv[1]))[:12]]
    # overlap with other sponsors in S3 (all panel + non-panel faith)
    s3 = tuple(l for l in flat if fso.in_scenario(l, frozenset({"top50", "panel_other", "nonpanel_faith"}), "all", frame["faith"]))
    other = _group_by_fast((l for l in s3 if l["rec"] in rec_dw and l["sponsor"] != OJC), lambda l: l["rec"])
    shared = {e for e in rec_dw if e in other}
    out += [mk("ojc:block_overlap", "S3", "recipients_also_paid_by_other_sponsors", recipients=len(shared),
               dw=sum(rec_dw[e] for e in shared), share=sum(rec_dw[e] for e in shared) / bl_dw,
               value=sum(l["dw"] for e in shared for l in other[e]),
               note="OJC block recipients that also get S3 lines from any other sponsor; dw = OJC $ to them; value = other sponsors' dw to them"),
            mk("ojc:block_overlap", "S3", "recipients_ojc_only", recipients=len(rec_dw) - len(shared),
               dw=bl_dw - sum(rec_dw[e] for e in shared), share=1 - sum(rec_dw[e] for e in shared) / bl_dw)]
    by_os = _group_by_fast((l for e in shared for l in other[e]), lambda l: l["sponsor"])
    out += [mk("ojc:block_overlap_sponsor", "S3", s, frame["names"].get(s, ""), l0[0]["group"], recipients=len({l["rec"] for l in l0}),
               lines=len(l0), dw=sum(l["dw"] for l in l0), note="other sponsors paying OJC block recipients (S3)")
            for s, l0 in sorted(by_os.items(), key=lambda kv: -sum(l["dw"] for l in kv[1]))[:15]]
    # top recipients
    top = sorted(recs.items(), key=lambda kv: -rec_dw[kv[0]])[:100]
    out += [mk("ojc:block_top_recipient", "FY2023-24", e, v[0]["name"],
               f"{bmfx.get(e, {}).get('city', '')}, {bmfx.get(e, {}).get('state', '')}; SUBSECTION {bmfx.get(e, {}).get('subsection', '')} "
               f"FOUNDATION {bmfx.get(e, {}).get('foundation', '')}; NTEE {bmfx.get(e, {}).get('ntee', '') or '-'}; ruling "
               f"{bmfx.get(e, {}).get('ruling', '') or '-'}; base rtype {fso.mcr.rtype_of(v[0]['name'], False)}",
               v[0]["ftype"], 1, len(v), sum(r["amount"] for r in v), rec_dw[e], rec_dw[e] / bl_dw,
               sum(l["dw"] for l in other.get(e, ())), "value = other sponsors' S3 dw to this recipient")
            for e, v in top]
    # non-block lines: DAF sponsors and federations itemised
    out += [mk("ojc:passthrough_line", f"FY{r['fy']}", r["ein"], r["name"], f"{bmfx.get(r['ein'], {}).get('city', '')}, "
               f"{bmfx.get(r['ein'], {}).get('state', '')}; in DAFRC panel: {'yes' if r['ein'] in panel else 'no'}",
               r["bucket"], 1, 1, r["amount"], r["amount"] * r["w"], r["amount"] / tot_si, "",
               "OJC line to a DAF sponsor or federation (netted lines never reach the church block)")
            for r in sorted(pos, key=lambda r: -r["amount"]) if r["bucket"] in ("daf_sponsor_netted", "daf_sponsor_not_netted", "federation")]
    # inflows to OJC from other sponsors' Schedule I
    inflow = tuple({**r, "sponsor": k[0], "fy": k[1]} for k, rs in ann.items() if k[0] != OJC for r in rs
                   if r["ein"] == OJC and r["amount"] > 0)
    out += [mk("ojc:inflow_from_panel_sponsor", f"FY{fy}", s, frame["names"].get(s, ""), frame["tier"].get((s, fy), ""),
               lines=len(v), si=sum(r["amount"] for r in v),
               note="Schedule I lines from other DAFRC panel sponsors to the OJC Fund (netted as DAF-to-DAF in the frame)")
            for (s, fy), v in sorted(_group_by_fast(inflow, lambda r: (r["sponsor"], r["fy"])).items(),
                                     key=lambda kv: -sum(r["amount"] for r in kv[1]))]
    out += [mk("ojc:inflow_total", "FY2023-24", "all_panel_sponsors", recipients=len({r['sponsor'] for r in inflow}),
               lines=len(inflow), si=sum(r["amount"] for r in inflow),
               value=sum(r["amount"] for r in inflow) / frame["ojc_contrib"] if frame["ojc_contrib"] else "",
               note=f"value = inflow / OJC Schedule D DAF contributions FY2023+FY2024 (${frame['ojc_contrib']:,.0f}); sponsor FYs differ")]
    return out


def inflow_ratio(frame: Mapping) -> float:
    """Schedule I $ paid INTO the OJC Fund by other panel sponsors / OJC's Schedule D DAF contributions (FY2023+24)."""
    inflow = sum(r["amount"] for k, rs in frame["ann"].items() if k[0] != OJC for r in rs if r["ein"] == OJC and r["amount"] > 0)
    return inflow / frame["ojc_contrib"] if frame["ojc_contrib"] else 0.0


def share_rows(frame: Mapping) -> list:
    flat, block, faith = frame["flat"], frame["block"], frame["faith"]
    ratio = inflow_ratio(frame)
    ftype = {e: fine_type(frame["bmf"][e]["name"]) for e in block if e in frame["bmf"]}
    out = []
    for scn, tset, mode in fso.SCENARIOS:
        if scn not in ("S2_top50_plus_all_faith", "S3_all_panel_plus_nonpanel_faith"):
            continue
        bl = tuple(l for l in flat if fso.in_scenario(l, tset, mode, faith) and l["rec"] in block)
        tot0, fs0, _ = faith_share(bl)
        for name, keep, desc in variants(bl, ftype):
            kept = tuple(l for l in bl if keep(l))
            tot, fs, ns = faith_share(kept)
            out.append(mk("faith_share:block", scn, name, desc, f"national share {ns:.5f}" if ns is not None else "",
                          recipients=len({l["rec"] for l in kept}), lines=len(kept), si=sum(l["si"] for l in kept),
                          dw=tot, share=tot / tot0, value=fs,
                          note=f"value = faith share of block dw; share = block dw kept / central block dw; central faith share {fs0:.5f}"))
        ojc_bl = sum(l["dw"] for l in bl if l["sponsor"] == OJC)
        out.append(mk("faith_share:block", scn, "ojc_inflow_reattributed", "move the share of OJC block dw funded by other "
                      "panel sponsors' grants into OJC (inflow ratio) from faith to non-faith; denominator unchanged",
                      f"inflow ratio {ratio:.5f}; shifted dw {ojc_bl * ratio:.0f}", lines=len(bl), dw=tot0, share=1.0,
                      value=(fs0 * tot0 - ojc_bl * ratio) / tot0, note="value = faith share of block dw after reattribution"))
        by_t = _group_by_fast(bl, lambda l: (ftype.get(l["rec"], "unclassified"), l["group"] in fso.FAITH_GROUPS))
        out += [mk("faith_share:block_fine_type", scn, f"{t}|{'faith' if f else 'non_faith'}", category=t,
                   recipients=len({l["rec"] for l in v}), lines=len(v), dw=sum(l["dw"] for l in v),
                   share=sum(l["dw"] for l in v) / tot0, note="every sponsor's block dw by fine name type and faith flag")
                for (t, f), v in sorted(by_t.items())]
    return out


# ----------------------------------------------------------------------------- pure: Groundswell
TAGS = ("AmendedReturnInd", "ReturnTs", "TaxPeriodEndDt", "FormationYr", "DonorAdvisedFundInd", "DonorAdvisedFundsHeldCnt",
        "FundsAndOtherAccountsHeldCnt", "DonorAdvisedFundsContriAmt", "FundsAndOtherAccountsContriAmt",
        "DonorAdvisedFundsGrantsAmt", "FundsAndOtherAccountsGrantsAmt", "DonorAdvisedFundsVlEOYAmt",
        "FundsAndOtherAccountsVlEOYAmt", "DisclosedOrgLegCtrlInd", "DisclosedForCharitablePrpsInd",
        "CYContributionsGrantsAmt", "CYGrantsAndSimilarPaidAmt", "TotalEmployeeCnt", "TotalVolunteersCnt",
        "TotalAssetsEOYAmt", "ActivityOrMissionDesc", "WebsiteAddressTxt", "GrantsToOrganizationsInd")
GS_SNIPS = (("faq", r"Groundswell accounts are powered by a donor-advised fund[^.]*\."),
            ("faq", r"Employees can contribute funds to their account, companies match those funds[^.]*\."),
            ("faq", r"A Groundswell account is theirs forever[^.]*\."),
            ("faq", r"Employees can fund their Groundswell accounts via[^.]*\."),
            ("faq", r"a minimum amount of \$5 is required for each transaction\."),
            ("legal/terms", r"Last Updated Date: [A-Z]+ \d+, \d{4}"),
            ("legal/terms", r"Your Contributions will be held by the Foundation in a Donor Advised Fund account for you"),
            ("legal/terms", r"The Foundation operates all DAFs in compliance with Internal Revenue Code"),
            ("legal/terms", r"DAFs are component funds of the Foundation; they are not separate legal entities\."),
            ("legal/terms", r"such Authorized Employer may directly contribute funds to your DAF[^.]*\."),
            ("legal/terms", r"all Payroll Contributions that have been deposited to your DAF shall remain in your DAF[^.]*\."),
            ("legal/terms", r"you must annually recommend Distributions in an amount that totals at least five percent[^.]*\."),
            ("legal/terms", r"not including any Employer Contributions or gifts from others[^.]*\."),
            ("products/giving", r"Groundswell offers each employee their own donor-advised fund \(DAF\)[^.]*\."),
            ("products/giving", r"Create and manage multiple corporate Donor-Advised Funds \(DAFs\)[^.]*\."),
            ("employee-assistance", r"employees can support it directly from their Groundswell personal giving accounts\."),
            ("phaas", r"the matching happens preemptively into an employee.s PhaaS-powered donor advised fund\."))


def xml_tag(t: str, k: str) -> str:
    m = re.search(rf"<{k}(?:\s[^>]*)?>(.*?)</{k}>", t, re.S)
    return m.group(1) if m else ""


def xml_tags(t: str) -> dict:
    return {k: xml_tag(t, k) for k in TAGS}


def cash_eoy(t: str) -> str:
    m = re.search(r"<CashNonInterestBearingGrp>.*?<EOYAmt>(\d+)</EOYAmt>", t, re.S)
    return m.group(1) if m else ""


def part_iii_desc(t: str) -> str:
    m = re.search(r"<ProgSrvcAccomActy2Grp>|<ProgSrvcAccomActyOtherGrp>", t)
    d = re.findall(r"<Desc>(.*?)</Desc>", t[:m.start()] if m else t, re.S)
    return next((x for x in d if "GRANTS" in x.upper()), "")


def sched_o_amend(t: str) -> str:
    m = re.search(r"AMENDED RETURN:</FormAndLineReferenceDesc>\s*<ExplanationTxt>(.*?)</ExplanationTxt>", t, re.S)
    return m.group(1) if m else ""


def sched_r(t: str) -> str:
    m = re.search(r"<IRS990ScheduleR.*?</IRS990ScheduleR>", t, re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip() if m else ""


def page_text(raw: str) -> str:
    t = re.sub(r"(?is)<(script|style|svg|noscript)[^>]*>.*?</\1>", " ", raw)
    t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def gs_rows(xml: str, pages: Mapping, robots: Sequence[Mapping]) -> list:
    tg = xml_tags(xml)
    n, v = float(tg["DonorAdvisedFundsHeldCnt"] or 0), float(tg["DonorAdvisedFundsVlEOYAmt"] or 0)
    c, g = float(tg["DonorAdvisedFundsContriAmt"] or 0), float(tg["CYGrantsAndSimilarPaidAmt"] or 0)
    desc = part_iii_desc(xml)
    grants_n = re.search(r"OVER ([\d,]+) INDIVIDUAL GRANTS", desc)
    recips = re.search(r"APPROXIMATELY ([\d,]+) UNIQUE", desc)
    gn = float(grants_n.group(1).replace(",", "")) if grants_n else 0.0
    out = [mk("gs:xml_tag", "TY2024", k, value=val, note=f"oid {GS_OID}", source=SRC_B) for k, val in tg.items()]
    out += [mk("gs:derived", "TY2024", "avg_eoy_value_per_account", value=v / n if n else "", note="DonorAdvisedFundsVlEOYAmt / DonorAdvisedFundsHeldCnt", source=SRC_B),
            mk("gs:derived", "TY2024", "avg_contribution_per_account", value=c / n if n else "", note="DonorAdvisedFundsContriAmt / count (count is year-end)", source=SRC_B),
            mk("gs:derived", "TY2024", "sched_d_col_a_plus_b_eoy_vs_cash_eoy",
               value=f"{v + float(tg['FundsAndOtherAccountsVlEOYAmt'] or 0):.0f} vs {cash_eoy(xml)}",
               note="Schedule D Part I line 4 (a)+(b) against Part X line 1 cash, non-interest-bearing, EOY", source=SRC_B),
            mk("gs:derived", "TY2024", "grants_per_account", value=g / n if n else "", note="Part IX line 1 grants / year-end DAF count", source=SRC_B),
            mk("gs:derived", "TY2024", "avg_grant_size", value=g / gn if gn else "", note="Part IX grants / 'over N individual grants' (Part III); an upper bound", source=SRC_B),
            mk("gs:derived", "TY2024", "grants_count_part_iii", value=gn, note="Part III text: 'OVER N INDIVIDUAL GRANTS'", source=SRC_B),
            mk("gs:derived", "TY2024", "unique_recipients_part_iii", value=float(recips.group(1).replace(",", "")) if recips else "",
               note="Part III text: 'APPROXIMATELY N UNIQUE NONPROFIT RECIPIENTS'", source=SRC_B),
            mk("gs:text", "TY2024", "part_iii_program_desc", value=desc, note="Form 990 Part III line 4a", source=SRC_B),
            mk("gs:text", "TY2024", "schedule_o_amended_return", value=sched_o_amend(xml), note="Schedule O, amended-return explanation", source=SRC_B),
            mk("gs:text", "TY2024", "schedule_r", value=sched_r(xml)[:600], note="Schedule R text (related organisation)", source=SRC_B)]
    out += [mk("gs:robots", "", r["host"], value=r["result"], note=r["why"] + "; " + r["ts"], source=r["url"]) for r in robots]
    txt = {p: page_text(raw) for p, raw in pages.items()}
    out += [mk("gs:web_snippet", "2026-11-20", p, value=(m.group(0) if m else "NOT FOUND"),
               note="verbatim snippet from the live page (retrieved 2026-11-20)", source=GS_BASE + p)
            for p, rx in GS_SNIPS for m in [re.search(rx, txt.get(p, ""))]]
    return out


# ----------------------------------------------------------------------------- I/O
def robots_check(url: str, cache: str, fetch: bool) -> dict:
    host = url.split("/")[2]
    if not fetch:  # cache-only: report the latest logged check for this host
        logp = os.path.join(cache, "robots-log.tsv")
        rows = [l.rstrip("\n").split("\t") for l in open(logp, encoding="utf-8")] if os.path.exists(logp) else []
        last = [r for r in rows if len(r) >= 4 and r[1] == host][-1:]
        return ({"host": host, "url": f"https://{host}/robots.txt", "result": last[0][3], "why": last[0][2], "ts": last[0][0]}
                if last else {"host": host, "url": f"https://{host}/robots.txt", "result": "not_checked", "why": "", "ts": ""})
    rp = urllib.robotparser.RobotFileParser()
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with urllib.request.urlopen(urllib.request.Request(f"https://{host}/robots.txt", headers={"User-Agent": UA}), timeout=30) as r:
            rp.parse(r.read().decode("utf-8", "replace").splitlines())
        res = {"host": host, "url": f"https://{host}/robots.txt", "result": "allowed" if rp.can_fetch(UA, url) else "blocked", "why": "robots 200", "ts": ts}
    except urllib.error.HTTPError as e:
        res = {"host": host, "url": f"https://{host}/robots.txt", "result": "allowed" if e.code in (404, 410) else "blocked", "why": f"robots {e.code}", "ts": ts}
    except Exception as e:  # noqa: BLE001
        res = {"host": host, "url": f"https://{host}/robots.txt", "result": "blocked", "why": f"robots error {type(e).__name__}", "ts": ts}
    os.makedirs(cache, exist_ok=True)
    with open(os.path.join(cache, "robots-log.tsv"), "a", encoding="utf-8") as fh:
        fh.write(f"{ts}\t{host}\t{res['why']}\t{res['result']}\t{url}\n")
    return res


def cached_get(url: str, path: str, fetch: bool, allowed: bool) -> str:
    if os.path.exists(path):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    if not (fetch and allowed):
        return ""
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120) as r:
        body = r.read().decode("utf-8", "replace")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    time.sleep(1)
    return body


def load_bmf_x(bmf_dir: str, eins: frozenset) -> dict:
    def rows(f):
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple((ein9(r["EIN"]), {"name": r["NAME"].strip(), "city": r["CITY"].strip(), "state": r["STATE"].strip(),
                                           "subsection": r["SUBSECTION"].strip(), "foundation": r["FOUNDATION"].strip(),
                                           "ruling": r["RULING"].strip(), "ntee": r["NTEE_CD"].strip(),
                                           "deductibility": r["DEDUCTIBILITY"].strip(), "filing_req": r["FILING_REQ_CD"].strip()})
                         for r in csv.DictReader(fh) if ein9(r["EIN"]) in eins)
    return dict(x for f in fso.BMF_FILES for x in rows(f))


def build_frame(a) -> dict:
    """The b4026-06-01 frame, rebuilt with the same functions and caches as mission_faith_sponsors_outside.main."""
    ntn, base = fso.ntn, fso.base
    dafrc = read_csv(DAFRC_CSV)
    dafrc_last = {ein9(r["ein"]): r for r in sorted(dafrc, key=lambda r: r["fiscal_year_end"])}
    panel = fso.panel_from(dafrc)
    rank = fso.top_n(dafrc, fso.TOP_N)
    faith_p = fso.panel_faith(panel, dafrc_last)
    sy = ntn.sponsor_years(fso.pick_returns(fso.load_np(a.np_cache)), panel, rank)
    item = {k: v for k, v in sy.items() if v["pre"] == "itemised"}
    loaded = {k: fso.load_lines(item[k]["x"]["oid"], item[k]["x"]["sched_i_lines"],
                                a.lines_cache_top50 if item[k]["tier"] == "top50" else a.lines_cache, [], False) for k in sorted(item)}
    good_p = {k: fso.drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    tiers_p = {k: ("top50" if item[k]["tier"] == "top50" else "panel_other") for k in good_p}
    cand = fso.nonpanel_candidates(fso.load_bmf_rows(a.bmf_dir, lambda r: (r.get("SUBSECTION") or "").strip() == "03"
                                                     and fso.FAITH_NONPANEL_RX.search((r.get("NAME") or "").upper())), frozenset(panel))
    picks = fso.pick_index_returns(fso.index_990s(a.index_dir, frozenset(cand)))
    pk = sorted(picks)
    sd = {k: fso.fetch_extract(picks[k]["oid"], a.np_work, False, frozenset(), {}, False) for k in pk}
    daf_keys = [k for k in pk if sd[k].get("xml_status") == "ok" and (sd[k].get("sched_d_daf_grants") or 0) > 0]
    full = {k: fso.fetch_extract(picks[k]["oid"], a.np_work, False, frozenset(), {}, True) for k in daf_keys}
    np_item = {k: x for k, x in full.items() if x.get("xml_status") == "ok" and (x.get("sched_i_lines") or 0) > 0 and fso.itemized(x)}
    np_loaded = {k: fso.load_lines(np_item[k]["oid"] if "oid" in np_item[k] else picks[k]["oid"], np_item[k]["sched_i_lines"],
                                   os.path.join(a.np_work, "lines"), [], False) for k in sorted(np_item)}
    good_n = {k: fso.drop_totals_rows(v) for k, v in np_loaded.items() if v["status"] == "ok"}
    np_faith = {e: (fso.faith_kind(cand[e]["name"]), "nonpanel_bmf_name_and_sched_d") for e in {k[0] for k in good_n}}
    faith = {**faith_p, **np_faith}
    names = {**{e: p["name"] for e, p in panel.items()}, **{e: cand[e]["name"] for e in np_faith}}
    good = {**good_p, **good_n}
    tiers = {**tiers_p, **{k: "nonpanel_faith" for k in good_n}}
    wl = read_csv(fso.WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    wgroups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: fso.norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in wgroups.items() if k and len(v) == 1}
    ann = {k: fso.annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    sy_all = {**{k: item[k] for k in good_p}, **{k: {"x": np_item[k]} for k in good_n}}
    weights, _ = ntn.weight_fallback(base.sponsor_weights(read_csv(fso.COST), good), sy_all, 1.0)
    flat = fso.flat_lines(ann, weights, tiers, frozenset(np_faith))
    flat = tuple({**l, "group": fso.sponsor_group(l["sponsor"], panel, faith)} for l in flat)
    rec_eins = frozenset(l["rec"] for l in flat if l["rec"]) | frozenset(r["ein"] for k, rs in ann.items() if k[0] == OJC for r in rs if r["ein"])
    bmf = base.load_bmf(a.bmf_dir, rec_eins)
    extra = fso.load_bmf_extra(a.bmf_dir, frozenset(bmf))
    hist = fso.load_history(a.index_dir, rec_eins)
    church = frozenset(e for e, b in bmf.items() if b["foundation"] == "10")
    reason = {u["key"]: u["reason"] for u in fso.units_b({e: {"fy": {}, "grantors": set()} for e in church}, {}, bmf, extra, hist, panel)}
    block = frozenset(e for e in church if reason.get(e) == fso.BLOCK)
    oid = {k: (item[k]["x"]["oid"] if k in item else np_item[k].get("oid", picks.get(k, {}).get("oid", ""))) for k in good}
    ojc_contrib = sum(float(item[k]["x"].get("sched_d_daf_contributions") or 0) for k in good_p if k[0] == OJC)
    return {"panel": panel, "faith": faith, "names": names, "ann": ann, "weights": weights, "flat": flat, "bmf": bmf,
            "church": church, "block": block, "tier": tiers, "oid": oid, "ojc_contrib": ojc_contrib}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    for f in ("--np-cache", "--lines-cache-top50", "--lines-cache", "--bmf-dir", "--index-dir", "--outreach-dir", "--np-work", "--work"):
        ap.add_argument(f, required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    frame = build_frame(a)
    ojc_recs = frozenset(r["ein"] for k, rs in frame["ann"].items() if k[0] == OJC for r in rs if r["ein"])
    bmfx = load_bmf_x(a.bmf_dir, ojc_recs)
    rows_a = ojc_rows(frame, bmfx) + share_rows(frame)

    xml_url = XML_URL.format(oid=GS_OID)
    rob = [robots_check(xml_url, a.work, a.fetch), robots_check(GS_BASE + "faq", a.work, a.fetch)]
    xml = cached_get(xml_url, os.path.join(a.work, "xml", f"{GS_OID}.xml"), a.fetch, rob[0]["result"] == "allowed")
    pages = {p: cached_get(GS_BASE + p, os.path.join(a.work, "web", p.replace("/", "_") + ".html"), a.fetch,
                           rob[1]["result"] == "allowed") for p in GS_PAGES}
    rows_b = gs_rows(xml, pages, rob)
    write_csv(a.out, rows_a + rows_b, FIELDS)

    summ = {r["key"]: r for r in rows_a if r["section"] in ("ojc:bucket", "ojc:block_fine_type", "ojc:inflow_total")}
    print(json.dumps({
        "faith_share": {f"{r['scenario']}|{r['key']}": [r["value"], r["detail"], r["usd_daf_weighted"]]
                        for r in rows_a if r["section"] == "faith_share:block"},
        "ojc": {k: [v["section"], v["usd_schedule_i"], v["usd_daf_weighted"], v["share"], v["recipients"], v["value"]] for k, v in summ.items()},
        "groundswell": {r["key"]: r["value"] for r in rows_b if r["section"] in ("gs:derived",)},
        "web_found": sum(1 for r in rows_b if r["section"] == "gs:web_snippet" and r["value"] != "NOT FOUND"),
        "web_total": sum(1 for r in rows_b if r["section"] == "gs:web_snippet"), "robots": rob}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
