#!/usr/bin/env python3
"""Executive compensation and staffing at the 50 largest DAF sponsors, TY2021-2025 (queue item P-NEW-EXC-01).

Stdlib only; functional style (pure transforms, I/O at the edges).

What it reads per return (Form 990 e-file XML; the GivingTuesday S3 mirror, or the IRS TEOS zip by range request
when the mirror lacks a 2025/2026-indexed return):
  Part VII Section A   every listed person: title, hours, role boxes, reportable comp from the organisation (D),
                       from related organisations (E), other comp (F); section totals; line 2 (> $100k count)
  Schedule J Part II   every row (base, bonus, other, deferred, non-taxable, totals; filing org and related orgs)
  Part V line 2a       W-2 employee count;  Part I line 5 total employees
  Part IX lines 5-10   compensation lines (total column) and line 25;  Part X total assets
  Schedule D Part I    DAF count and end-of-year value;  Schedule R related-organisation names;
  Schedule O           sentences about who employs or pays staff (regex screen, quoted verbatim)

Universe: the 50 largest sponsors by FY2024 end-of-year DAF assets in the DAFRC panel after applied corrections
(dafrc-corrections-itemized.csv, applied = 1), plus a labelled supplement of five digital-first sponsors that are
not in the top 50. Returns: every Form 990 for those EINs in IRS index_2021-2026 whose tax year (year in which the
period begins) is 2021-2025; one return per EIN x tax period (the latest submission, which picks up amendments).

Inputs (read only):
  data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv, dafrc-corrections-itemized.csv
  IRS index_YYYY.csv files (--irs-dir)
Outputs:
  data/mission-2026-11-14/sponsor-executive-compensation-2021-2025.csv  (record_type = sponsor_year | person |
                                                                         segment_year | segment_trend)
Usage:
  python3 scripts/mission_sponsor_compensation.py --irs-dir IRS --work-dir WORK [--fetch]
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
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
from mission_batch35_screens import central_directory, member_xml  # noqa: E402

EXTRACT_VERSION = 1
UA = {"User-Agent": "research-script/1.0 (stdlib urllib)"}
TEOS_ZIP = "https://apps.irs.gov/pub/epostcard/990/xml/{year}/{batch}.zip"
INDEX_YEARS = tuple(range(2021, 2027))
TAX_YEARS = tuple(range(2021, 2026))
TOP_N = 50
OUT_CSV = os.path.join(DATA, "sponsor-executive-compensation-2021-2025.csv")
DAFRC_CSV = os.path.join(DATA, "dafrc-sponsor-schedule-d-fy2019-2024.csv")
ITEMIZED_CSV = os.path.join(DATA, "dafrc-corrections-itemized.csv")
COST_CSV = os.path.join(DATA, "sponsor-cost-structure.csv")     # context join by object id (FY2022+ harvest returns)
COST_COLS = ("operating_cost_ex_invest_mgmt", "outside_services_l11", "fees_mgmt_l11a", "fees_other_l11g")

# ----------------------------------------------------------------------------- segment table (manual, [I])
# ein -> (segment, commercial_affiliate_or_note). Segments:
#   affiliated_commercial  national sponsor founded by / branded with / administered by a for-profit financial firm
#   independent_national   national sponsor with no for-profit financial parent
#   community_foundation   DAFRC "Community Foundation" type
#   faith_single_issue     DAFRC single-issue religious / other (incl. faith nationals and Jewish federations)
#   university_health      DAFRC single-issue universities and healthcare
#   digital_first          supplement outside the top 50 (app-first sponsors named in direction-donor-feature-census.md)
SEGMENT = {
    "110303001": ("affiliated_commercial", "Fidelity Investments"),
    "311640316": ("affiliated_commercial", "Charles Schwab (DAFgiving360)"),
    "232888152": ("affiliated_commercial", "Vanguard"),
    "311774905": ("affiliated_commercial", "Goldman Sachs"),
    "527082731": ("affiliated_commercial", "Morgan Stanley"),
    "046010342": ("affiliated_commercial", "Bank of America / Merrill"),
    "593652538": ("affiliated_commercial", "Raymond James"),
    "311663020": ("affiliated_commercial", "Eaton Vance / Morgan Stanley (US Charitable Gift Trust)"),
    "141782466": ("affiliated_commercial", "Ayco (Goldman Sachs)"),
    "137111099": ("affiliated_commercial", "Bessemer Trust"),
    "311709466": ("affiliated_commercial", "T. Rowe Price"),
    "352129262": ("affiliated_commercial", "Renaissance (for-profit administrator of white-label programmes)"),
    "237825575": ("independent_national", ""),
    "341747398": ("independent_national", ""),
    "262048480": ("independent_national", ""),
    "200849590": ("independent_national", "affiliate of Greater Kansas City Community Foundation"),
    "260724604": ("independent_national", "DAFRC subtype Donation Processor"),
    "516506426": ("independent_national", ""),
    "581493949": ("faith_single_issue", "national Christian sponsor"),
    "431890105": ("faith_single_issue", "national Christian sponsor (The Signatry family)"),
    "825070897": ("faith_single_issue", "national Christian sponsor (The Signatry family)"),
    "411802412": ("faith_single_issue", "Thrivent (fraternal financial-services organisation) affiliate"),
    "237174183": ("faith_single_issue", ""),
    "042103559": ("faith_single_issue", ""),
    "941156533": ("faith_single_issue", ""),
    "956111928": ("faith_single_issue", ""),
    "522166327": ("faith_single_issue", "DAFRC single-issue other"),
    "941156365": ("university_health", ""),
    "952250801": ("university_health", ""),
    "863177440": ("digital_first", "Daffy"),
    "812771871": ("digital_first", "Charityvest"),
    "844661797": ("digital_first", "Endaoment"),
    "474172718": ("digital_first", "Givinga (account unit undefined; see wave-5 corrections)"),
    "813222963": ("digital_first", "GiveClear / TIFIN Give"),
}
DIGITAL = tuple(e for e, (s, _) in SEGMENT.items() if s == "digital_first")

TOP_TITLE = ((re.compile(r"\bC\.?E\.?O\b|CHIEF EXECUTIVE", re.I), 1),
             (re.compile(r"(?<!VICE )(?<!VICE-)(?<!VP )\bPRES(?:IDENT\b|\.|\b)", re.I), 2),
             (re.compile(r"EXECUTIVE DIRECTOR", re.I), 3))
NOT_TOP = re.compile(r"\bVICE\b|\bVP\b|\bSVP\b|\bEVP\b|ASSISTANT|ASST|ASSOCIATE|DEPUTY", re.I)
PAST_TITLE = re.compile(r"FORMER|PREVIOUS|\bPAST\b|RETIRED|EMERIT|\bTHRU\b|THROUGH|UNTIL|\bTO \d|\bLEFT\b|RESIGN|ENDING|SENIOR ADVISOR", re.I)
SUB_UNIT = re.compile(r"REGION|\bUK\b|TRANSATLANTIC|,\s*SMC\b", re.I)   # subsidiary / regional heads are not the top officer
# Manual top-officer overrides [I]: Stanford's return lists the CEO of Stanford Management Company first; the
# university president is the organisation's top officer.
TOP_OVERRIDE = {"941156365": re.compile(r"^PRESIDENT", re.I)}
COMP_TXT = re.compile(r"employ(?:ed|ees)\s+(?:of|by)\b|paid\s+by\b|compensat\w*\s+(?:by|from)\b|administrative services agreement"
                      r"|has no employees|does not have (?:any )?(?:paid )?employees|receives? no compensation|not compensated"
                      r"|leased employees|shared (?:services|staff|employees)|services agreement|payroll", re.I)


# ----------------------------------------------------------------------------- small pure helpers
def median(xs: Iterable) -> float | None:
    v = [x for x in xs if x is not None]
    return statistics.median(v) if v else None


def ratio(a, b) -> float | None:
    return a / b if a is not None and b not in (None, 0) else None


def ssum(*xs) -> float | None:
    v = [x for x in xs if x is not None]
    return sum(v) if v else None


def tax_year(tax_period: str) -> int:
    y, m = int(tax_period[:4]), int(tax_period[4:6])
    return y if m == 12 else y - 1


def norm_name(s: str) -> str:
    return re.sub(r"[^A-Z]", "", (s or "").upper())


def leaf_dict(g) -> dict:
    return {local(c.tag): (c.text or "").strip() for c in g.iter() if len(c) == 0 and c is not g}


# ----------------------------------------------------------------------------- universe
def panel(dafrc: Sequence[Mapping], items: Sequence[Mapping]) -> dict:
    """{(ein, fy): {name, type, subtype, assets, accounts}} with applied corrections."""
    base = {(ein9(r["ein"]), int(r["fiscal_year_end"])): {
        "name": r["name"], "type": r["type"], "subtype": r["subtype"],
        "assets": num(r["eoy_daf_assets"]), "accounts": num(r["number_of_daf_accounts"])} for r in dafrc}
    fix = {(ein9(c["ein"]), int(c["fiscal_year"]), c["metric"]): num(c["corrected_value"])
           for c in items if c["applied"] == "1" and c["metric"] in ("daf_assets_eoy", "daf_accounts_eoy")}
    keys = set(base) | {(e, fy) for e, fy, _ in fix}
    return {k: {**base.get(k, {"name": "", "type": "", "subtype": ""}),
                **({"assets": fix[(*k, "daf_assets_eoy")]} if (*k, "daf_assets_eoy") in fix else {}),
                **({"accounts": fix[(*k, "daf_accounts_eoy")]} if (*k, "daf_accounts_eoy") in fix else {})} for k in keys}


def top_sponsors(pn: Mapping, n: int = TOP_N) -> tuple[dict, ...]:
    fy24 = sorted(((v.get("assets") or 0, e) for (e, fy), v in pn.items() if fy == 2024), reverse=True)[:n]
    return tuple({"ein": e, "rank": i, "fy2024_daf_assets_corrected": a} for i, (a, e) in enumerate(fy24, 1))


def segment_of(ein: str, pn: Mapping) -> tuple[str, str]:
    if ein in SEGMENT:
        return SEGMENT[ein]
    t = (pn.get((ein, 2024)) or {}).get("type", "")
    return ("community_foundation", "") if t == "Community Foundation" else ("unclassified", t)


def load_index(irs_dir: str, eins: frozenset) -> tuple[dict, ...]:
    def rows(y):
        with open(os.path.join(irs_dir, f"index_{y}.csv"), newline="", encoding="latin-1") as fh:
            for r in csv.DictReader(fh):
                if r["RETURN_TYPE"] == "990" and ein9(r["EIN"]) in eins:
                    yield {"ein": ein9(r["EIN"]), "tax_period": r["TAX_PERIOD"], "object_id": r["OBJECT_ID"],
                           "index_year": y, "batch": r.get("XML_BATCH_ID") or "", "sub_date": r["SUB_DATE"]}
    allr = [r for y in INDEX_YEARS for r in rows(y) if r["tax_period"].isdigit() and tax_year(r["tax_period"]) in TAX_YEARS]
    best: dict = {}
    for r in allr:
        k = (r["ein"], r["tax_period"])
        if k not in best or r["object_id"] > best[k]["object_id"]:
            best[k] = r
    count = {k: sum(1 for r in allr if (r["ein"], r["tax_period"]) == k) for k in best}
    return tuple({**r, "returns_for_period": count[(r["ein"], r["tax_period"])]} for r in best.values())


# ----------------------------------------------------------------------------- XML extract (streamed)
def part_vii_rows(irs990) -> list:
    return [leaf_dict(g) for g in irs990.iter(NS + "Form990PartVIISectionAGrp")]


def schedule_o_comp(el) -> list:
    out = []
    for g in el.iter(NS + "SupplementalInformationDetail"):
        ref = (g.findtext(NS + "FormAndLineReferenceDesc") or "").strip()
        txt = re.sub(r"\s+", " ", g.findtext(NS + "ExplanationTxt") or "")
        for m in COMP_TXT.finditer(txt):
            out.append(f"[{ref[:60]}] …{txt[max(0, m.start() - 220):m.end() + 220]}…")
            break
    return out[:6]


def extract_stream(stream) -> dict:
    out: dict = {"sched_j_rows": [], "sched_o_comp": [], "sched_r_names": [], "sched_j_present": 0}
    for _, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        if tag == "ReturnHeader":
            out.update({"tax_period_end": el.findtext(f".//{NS}TaxPeriodEndDt") or "",
                        "tax_period_begin": el.findtext(f".//{NS}TaxPeriodBeginDt") or "",
                        "return_ts": el.findtext(f".//{NS}ReturnTs") or "",
                        "filer_name": el.findtext(f".//{NS}Filer/{NS}BusinessName/{NS}BusinessNameLine1Txt") or ""})
            el.clear()
        elif tag == "IRS990":
            f = lambda t: num(el.findtext(NS + t))  # noqa: E731
            ix = lambda t: num(el.findtext(f"{NS}{t}/{NS}TotalAmt"))  # noqa: E731
            out.update({"part_vii": part_vii_rows(el),
                        "employees_part_v_2a": f("EmployeeCnt"), "employees_part_i_5": f("TotalEmployeeCnt"),
                        "part_vii_tot_org": f("TotalReportableCompFromOrgAmt"),
                        "part_vii_tot_related": f("TotReportableCompRltdOrgAmt"),
                        "part_vii_tot_other": f("TotalOtherCompensationAmt"),
                        "part_vii_n_over_100k": f("IndivRcvdGreaterThan100KCnt"),
                        "part_vii_former_listed_ind": el.findtext(NS + "FormerOfcrEmployeesListedInd") or "",
                        "part_vii_comp_other_srcs_ind": el.findtext(NS + "CompensationFromOtherSrcsInd") or "",
                        "l05": ix("CompCurrentOfcrDirectorsGrp"), "l06": ix("CompDisqualPersonsGrp"),
                        "l07": ix("OtherSalariesAndWagesGrp"), "l08": ix("PensionPlanContributionsGrp"),
                        "l09": ix("OtherEmployeeBenefitsGrp"), "l10": ix("PayrollTaxesGrp"),
                        "l25": ix("TotalFunctionalExpensesGrp"),
                        "total_assets_eoy": num(el.findtext(f"{NS}TotalAssetsGrp/{NS}EOYAmt")) or f("TotalAssetsEOYAmt"),
                        "amended_ind": el.findtext(NS + "AmendedReturnInd") or ""})
            el.clear()
        elif tag == "IRS990ScheduleJ":
            out["sched_j_present"] = 1
            out["sched_j_rows"] = [leaf_dict(g) for g in el.iter(NS + "RltdOrgOfficerTrstKeyEmplGrp")]
            el.clear()
        elif tag == "IRS990ScheduleD":
            out.update({"sched_d_daf_count": num(el.findtext(NS + "DonorAdvisedFundsHeldCnt")),
                        "sched_d_daf_eoy_value": num(el.findtext(NS + "DonorAdvisedFundsVlEOYAmt"))})
            el.clear()
        elif tag == "IRS990ScheduleO":
            out["sched_o_comp"] = schedule_o_comp(el)
            el.clear()
        elif tag == "IRS990ScheduleR":
            names = [(x.text or "").strip() for x in el.iter(NS + "BusinessNameLine1Txt") if x.text]
            out["sched_r_names"] = list(dict.fromkeys(names))[:12]
            el.clear()
        elif tag.startswith("IRS990Schedule") or tag in ("RecipientTable", "GrantsOtherAsstToIndivInUSGrp"):
            el.clear()
    return out


def teos_bytes(f: Mapping, work_dir: str) -> tuple[bytes | None, str]:
    if not f.get("batch"):
        return None, "no_batch"
    labels = (f["batch"], f["batch"][:-1] + "B") if f["batch"].endswith("A") else (f["batch"],)
    for lb in labels:
        url = TEOS_ZIP.format(year=f["index_year"], batch=lb)
        try:
            cd = central_directory(url, os.path.join(work_dir, "zipcd"))
        except urllib.error.HTTPError:
            continue
        name = next((k for k in cd["members"] if k.endswith(f"{f['object_id']}_public.xml")), None)
        if name:
            return member_xml(url, name, cd["members"][name], work_dir), url
    return None, "not_in_zip"


def fetch_extract(f: Mapping, work_dir: str, fetch: bool, retries: int = 2) -> dict:
    path = os.path.join(work_dir, "extract", f"{f['object_id']}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == EXTRACT_VERSION:
            return c
    if not fetch:
        return {"xml_status": "not_fetched"}
    url = XML_URL.format(oid=f["object_id"])
    out: dict = {"xml_status": "error:none"}
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                out = {**extract_stream(r), "xml_status": "ok", "xml_source": url}
            break
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                try:
                    data, src = teos_bytes(f, work_dir)
                except (urllib.error.URLError, OSError, ValueError) as e2:
                    data, src = None, f"teos_error:{type(e2).__name__}"
                if data:
                    out = {**extract_stream(io.BytesIO(data)), "xml_status": "ok", "xml_source": src}
                else:
                    out = {"xml_status": f"http_{e.code}_{src}"}
                break
            out = {"xml_status": f"http_{e.code}"}
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
            out = {"xml_status": f"error:{type(e).__name__}"}
            time.sleep(2 * (attempt + 1))
    res = {**out, "_v": EXTRACT_VERSION}
    if not res["xml_status"].startswith("error"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(res, fh)
    return res


# ----------------------------------------------------------------------------- person-level transforms (pure)
def is_x(v: str) -> bool:
    return (v or "").strip().upper() in ("X", "TRUE", "1")


def person(p: Mapping) -> dict:
    name = p.get("PersonNm") or p.get("BusinessNameLine1Txt") or ""
    org, rel, oth = (num(p.get(k)) or 0.0 for k in ("ReportableCompFromOrgAmt", "ReportableCompFromRltdOrgAmt", "OtherCompensationAmt"))
    roles = "|".join(r for r, k in (("trustee", "IndividualTrusteeOrDirectorInd"), ("institutional_trustee", "InstitutionalTrusteeInd"),
                                    ("officer", "OfficerInd"), ("key_employee", "KeyEmployeeInd"),
                                    ("highest_compensated", "HighestCompensatedEmployeeInd"), ("former", "FormerOfcrDirectorTrusteeInd"))
                     if is_x(p.get(k)))
    return {"person_name": name, "title": p.get("TitleTxt", ""), "roles": roles,
            "institutional": int(is_x(p.get("InstitutionalTrusteeInd"))),
            "hours_org": num(p.get("AverageHoursPerWeekRt")), "hours_related": num(p.get("AverageHoursPerWeekRltdOrgRt")),
            "comp_org_d": org, "comp_related_e": rel, "comp_other_f": oth, "comp_total_def": org + rel + oth}


def top_officer(people: Sequence[Mapping], override=None) -> tuple[dict | None, str]:
    cands = [p for p in people if ("officer" in p["roles"] or "key_employee" in p["roles"]) and "former" not in p["roles"]
             and not p["institutional"]]
    if override is not None:
        hit = [p for p in cands if override.search(p["title"])]
        if hit:
            return max(hit, key=lambda p: p["comp_total_def"]), "manual_override"
    def rank(p):
        t = p["title"]
        if SUB_UNIT.search(t) or (NOT_TOP.search(t) and not re.search(r"\bC\.?E\.?O\b|CHIEF EXECUTIVE", t, re.I)):
            return 9
        r = next((r for rx, r in TOP_TITLE if rx.search(t)), 9)
        return r + 3 if r < 9 and PAST_TITLE.search(t) else r
    ranked = sorted(cands, key=lambda p: (rank(p), -p["comp_total_def"]))
    if ranked and rank(ranked[0]) < 9:
        n_ceo = sum(1 for p in ranked if rank(p) == rank(ranked[0]))
        return ranked[0], f"title_rank{rank(ranked[0])}" + ("_multiple" if n_ceo > 1 else "")
    paid = sorted((p for p in cands if p["comp_total_def"] > 0 and (p["hours_org"] or 0) >= 20), key=lambda p: -p["comp_total_def"])
    return (paid[0], "highest_paid_officer") if paid else (None, "none")


def schedule_j_map(rows: Sequence[Mapping]) -> dict:
    def g(r, k):
        return num(r.get(k))
    return {norm_name(r.get("PersonNm") or r.get("BusinessNameLine1Txt") or ""): {
        "schj_base_org": g(r, "BaseCompensationFilingOrgAmt"), "schj_base_related": g(r, "CompensationBasedOnRltdOrgsAmt"),
        "schj_bonus_org": g(r, "BonusFilingOrganizationAmount"), "schj_bonus_related": g(r, "BonusRelatedOrganizationsAmt"),
        "schj_other_org": g(r, "OtherCompensationFilingOrgAmt"), "schj_other_related": g(r, "OtherCompensationRltdOrgsAmt"),
        "schj_deferred_org": g(r, "DeferredCompensationFlngOrgAmt"), "schj_deferred_related": g(r, "DeferredCompRltdOrgsAmt"),
        "schj_nontaxable_org": g(r, "NontaxableBenefitsFilingOrgAmt"), "schj_nontaxable_related": g(r, "NontaxableBenefitsRltdOrgsAmt"),
        "schj_total_org": g(r, "TotalCompensationFilingOrgAmt"), "schj_total_related": g(r, "TotalCompensationRltdOrgsAmt"),
        "schj_prior_990_org": g(r, "CompReportPrior990FilingOrgAmt"), "schj_prior_990_related": g(r, "CompReportPrior990RltdOrgsAmt")}
        for r in rows}


# ----------------------------------------------------------------------------- sponsor-year row (pure)
def affiliate_flag(top: Mapping | None, x: Mapping, seg: str, staff: float | None) -> str:
    if top is None:
        return "no_officer_listed_institutional_trustee" if x.get("_inst") else "no_officer_identified"
    if top["comp_org_d"] == 0 and top["comp_related_e"] > 0:
        return "top_officer_paid_by_related_org"
    if top["comp_total_def"] == 0 and (staff or 0) == 0:
        return "no_staff_cost_on_990" + ("_affiliate_staffed" if seg == "affiliated_commercial" else "")
    if top["comp_total_def"] == 0:
        return "top_officer_0_on_990" + ("_affiliate_staffed" if seg == "affiliated_commercial" else "")
    if top["comp_org_d"] > 0 and top["comp_related_e"] > 0:
        return "top_officer_split_org_and_related"
    return ""


def sponsor_year(f: Mapping, x: Mapping, meta: Mapping, pn: Mapping, cost: Mapping) -> tuple[dict, tuple[dict, ...]]:
    allp = tuple(person(p) for p in x.get("part_vii", []))
    inst = tuple(p for p in allp if p["institutional"])
    people = tuple(p for p in allp if not p["institutional"])
    sj = schedule_j_map(x.get("sched_j_rows", []))
    top, basis = top_officer(people, TOP_OVERRIDE.get(f["ein"]))
    others = sorted((p for p in people if p is not top), key=lambda p: -p["comp_total_def"])[:5]
    others = tuple(p for p in others if p["comp_total_def"] > 0)
    fy = int(f["tax_period"][:4])
    dafrc = pn.get((f["ein"], fy)) or {}
    daf_assets = x.get("sched_d_daf_eoy_value") or dafrc.get("assets")
    accounts = x.get("sched_d_daf_count") or dafrc.get("accounts")
    staff = ssum(*(x.get(k) for k in ("l05", "l06", "l07", "l08", "l09", "l10")))
    seg, note = meta["segment"], meta["segment_note"]
    t = top or {}
    tj = sj.get(norm_name(t.get("person_name", ""))) if top else None
    rel_all = sum(p["comp_related_e"] for p in people)
    vii_all = sum(p["comp_total_def"] for p in people)
    top6 = tuple(p for p in (top, *others) if p)
    row = {"record_type": "sponsor_year", "ein": f["ein"], "sponsor_name": meta["name"], "rank_fy2024": meta["rank"],
           "segment": seg, "segment_note": note, "fy": fy, "tax_year": tax_year(f["tax_period"]), "tax_period": f["tax_period"],
           "object_id": f["object_id"], "returns_for_period": f["returns_for_period"], "return_ts": x.get("return_ts"),
           "amended_ind": x.get("amended_ind"), "xml_source": x.get("xml_source"),
           "employees_part_v_2a": x.get("employees_part_v_2a"), "employees_part_i_5": x.get("employees_part_i_5"),
           "part_vii_listed": len(allp), "part_vii_paid": sum(1 for p in people if p["comp_total_def"] > 0),
           "institutional_trustee_names": " | ".join(p["person_name"] for p in inst),
           "institutional_trustee_comp_def": sum(p["comp_total_def"] for p in inst) if inst else None,
           "part_vii_n_over_100k": x.get("part_vii_n_over_100k"),
           "part_vii_sum_org_d": sum(p["comp_org_d"] for p in people), "part_vii_sum_related_e": rel_all,
           "part_vii_sum_other_f": sum(p["comp_other_f"] for p in people),
           "part_vii_tot_org": x.get("part_vii_tot_org"), "part_vii_tot_related": x.get("part_vii_tot_related"),
           "part_vii_tot_other": x.get("part_vii_tot_other"),
           "related_share_of_part_vii": ratio(rel_all, vii_all),
           "top6_comp_total": sum(p["comp_total_def"] for p in top6), "top6_comp_related": sum(p["comp_related_e"] for p in top6),
           "l05": x.get("l05"), "l06": x.get("l06"), "l07": x.get("l07"), "l08": x.get("l08"), "l09": x.get("l09"), "l10": x.get("l10"),
           "staff_cost_l5_10": staff, "l25_total_expenses": x.get("l25"), "total_assets_eoy": x.get("total_assets_eoy"),
           "daf_assets_eoy": daf_assets, "daf_assets_source": "990_sched_d" if x.get("sched_d_daf_eoy_value") else ("dafrc_corrected" if daf_assets else ""),
           "daf_accounts": accounts, "daf_accounts_source": "990_sched_d" if x.get("sched_d_daf_count") else ("dafrc_corrected" if accounts else ""),
           "top_officer_title": t.get("title", ""), "top_officer_name": t.get("person_name", ""), "top_officer_basis": basis,
           "top_officer_hours_org": t.get("hours_org"), "top_officer_hours_related": t.get("hours_related"),
           "top_officer_comp_org_d": t.get("comp_org_d"), "top_officer_comp_related_e": t.get("comp_related_e"),
           "top_officer_comp_other_f": t.get("comp_other_f"), "top_officer_comp_total_def": t.get("comp_total_def"),
           "top_officer_schj_total": ssum((tj or {}).get("schj_total_org"), (tj or {}).get("schj_total_related")) if tj else None,
           "top_officer_schj_matched": int(bool(tj)), "sched_j_present": x.get("sched_j_present"),
           "top_pay_per_bn_daf": ratio(t.get("comp_total_def"), (daf_assets or 0) / 1e9),
           "top_pay_per_1000_accounts": ratio(t.get("comp_total_def"), (accounts or 0) / 1000),
           "top_pay_per_bn_total_assets": ratio(t.get("comp_total_def"), (x.get("total_assets_eoy") or 0) / 1e9),
           **{f"ctx_{k}": num((cost.get(f["object_id"]) or {}).get(k)) for k in COST_COLS},
           "ctx_staff_share_of_opex_ex_l11f": ratio(staff, num((cost.get(f["object_id"]) or {}).get("operating_cost_ex_invest_mgmt"))),
           "ctx_fee_and_trustee_bps_daf_assets": ratio(((num((cost.get(f["object_id"]) or {}).get("fees_mgmt_l11a")) or 0)
                                                        + (num((cost.get(f["object_id"]) or {}).get("fees_other_l11g")) or 0)
                                                        + sum(p["comp_total_def"] for p in inst)) * 1e4, daf_assets)
           if f["object_id"] in cost else None,
           "staff_cost_bps_daf_assets": ratio((staff or 0) * 1e4, daf_assets) if staff is not None else None,
           "staff_cost_bps_total_assets": ratio((staff or 0) * 1e4, x.get("total_assets_eoy")) if staff is not None else None,
           "staff_cost_per_account": ratio(staff, accounts),
           "staff_cost_per_employee": ratio(staff, x.get("employees_part_v_2a")),
           "flag_affiliate_pay": affiliate_flag(top, {**x, "_inst": bool(inst)}, seg, staff),
           "sched_r_related_names": " | ".join(x.get("sched_r_names", [])[:8]),
           "sched_o_comp_text": " || ".join(x.get("sched_o_comp", [])[:3])[:1800],
           "xml_url": XML_URL.format(oid=f["object_id"])}
    labelled = ((("top_officer", top),) if top else ()) + tuple((f"highest_paid_{i}", p) for i, p in enumerate(others, 1))
    prow = tuple({"record_type": "person", "ein": f["ein"], "sponsor_name": meta["name"], "rank_fy2024": meta["rank"], "segment": seg,
                  "fy": fy, "tax_year": row["tax_year"], "tax_period": f["tax_period"], "object_id": f["object_id"],
                  "person_role": lab, **p, **(sj.get(norm_name(p["person_name"])) or {}),
                  "schj_matched": int(norm_name(p["person_name"]) in sj), "xml_url": row["xml_url"]}
                 for lab, p in labelled)
    return row, prow


# ----------------------------------------------------------------------------- aggregates (pure)
def mark_shared_officers(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    """Same top officer (normalised name) at two universe sponsors in one tax year: the pay is one person's, filed twice."""
    key = lambda r: (r["tax_year"], norm_name(r["top_officer_name"]))  # noqa: E731
    seen: dict = {}
    for r in rows:
        if r["top_officer_name"] and (r["top_officer_comp_total_def"] or 0) > 0:
            seen.setdefault(key(r), set()).add(r["ein"])
    return tuple({**r, "top_officer_shared_with": "|".join(sorted(seen.get(key(r), set()) - {r["ein"]}))} for r in rows)



SEG_ORDER = ("affiliated_commercial", "independent_national", "community_foundation", "faith_single_issue",
             "university_health", "digital_first")


def latest_per_sponsor_ty(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    """One row per sponsor x tax year (a short-period return plus a full one: keep the later period end)."""
    best: dict = {}
    for r in rows:
        k = (r["ein"], r["tax_year"])
        if k not in best or r["tax_period"] > best[k]["tax_period"]:
            best[k] = r
    return tuple(best.values())


def segment_year_rows(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    out = []
    for seg in SEG_ORDER:
        for ty in TAX_YEARS:
            rs = [r for r in rows if r["segment"] == seg and r["tax_year"] == ty]
            if not rs:
                continue
            paid = [r for r in rs if (r["top_officer_comp_total_def"] or 0) > 0]
            out.append({"record_type": "segment_year", "segment": seg, "tax_year": ty, "n_returns": len(rs),
                        "n_top_officer_paid": len(paid),
                        "median_top_officer_comp": median(r["top_officer_comp_total_def"] for r in paid),
                        "median_top_pay_per_bn_daf": median(r["top_pay_per_bn_daf"] for r in paid),
                        "median_top_pay_per_1000_accounts": median(r["top_pay_per_1000_accounts"] for r in paid),
                        "median_top_pay_per_bn_total_assets": median(r["top_pay_per_bn_total_assets"] for r in paid),
                        "median_staff_cost_bps_daf_assets": median(r["staff_cost_bps_daf_assets"] for r in rs),
                        "median_staff_cost_bps_total_assets": median(r["staff_cost_bps_total_assets"] for r in rs),
                        "median_staff_cost_per_account": median(r["staff_cost_per_account"] for r in rs),
                        "median_employees_part_v_2a": median(r["employees_part_v_2a"] for r in rs),
                        "sum_staff_cost_l5_10": sum(r["staff_cost_l5_10"] or 0 for r in rs),
                        "sum_daf_assets": sum(r["daf_assets_eoy"] or 0 for r in rs),
                        "pooled_staff_cost_bps_daf_assets": ratio(sum(r["staff_cost_l5_10"] or 0 for r in rs) * 1e4,
                                                                  sum(r["daf_assets_eoy"] or 0 for r in rs)),
                        "sum_part_vii_related_e": sum(r["part_vii_sum_related_e"] or 0 for r in rs),
                        "sum_part_vii_org_d": sum(r["part_vii_sum_org_d"] or 0 for r in rs),
                        "n_flag_affiliate_pay": sum(1 for r in rs if r["flag_affiliate_pay"]),
                        "n_top_paid_by_org": sum(1 for r in rs if (r["top_officer_comp_org_d"] or 0) > 0),
                        "n_top_paid_related_only": sum(1 for r in rs if (r["top_officer_comp_org_d"] or 0) == 0
                                                       and (r["top_officer_comp_related_e"] or 0) > 0),
                        "n_top_zero_or_none": sum(1 for r in rs if not (r["top_officer_comp_total_def"] or 0)),
                        "median_top6_comp": median(r["top6_comp_total"] for r in rs if r["top6_comp_total"]),
                        "median_top6_share_of_staff_cost": median(ratio(r["top6_comp_total"], r["staff_cost_l5_10"]) for r in rs
                                                                  if r["top6_comp_total"] and r["staff_cost_l5_10"]),
                        "median_n_over_100k": median(r["part_vii_n_over_100k"] for r in rs if r["part_vii_n_over_100k"] is not None),
                        "pooled_staff_plus_l11a_bps_daf_ctx": ratio(sum((r["staff_cost_l5_10"] or 0) + (r["ctx_fees_mgmt_l11a"] or 0) for r in rs
                                                                        if r["ctx_operating_cost_ex_invest_mgmt"] is not None) * 1e4,
                                                                    sum(r["daf_assets_eoy"] or 0 for r in rs if r["ctx_operating_cost_ex_invest_mgmt"] is not None)),
                        "n_ctx": sum(1 for r in rs if r["ctx_operating_cost_ex_invest_mgmt"] is not None)})
    return tuple(out)


def trend_rows(rows: Sequence[Mapping], base: int = 2021, end: int = 2024) -> tuple[dict, ...]:
    """Matched sponsors filed in both tax years with a paid top officer in both (same title basis not required)."""
    by = {(r["ein"], r["tax_year"]): r for r in rows}
    out = []
    for seg in SEG_ORDER:
        eins = sorted({r["ein"] for r in rows if r["segment"] == seg})
        pairs = [(by[(e, base)], by[(e, end)]) for e in eins if (e, base) in by and (e, end) in by]
        pp = [(a, b) for a, b in pairs if (a["top_officer_comp_total_def"] or 0) > 0 and (b["top_officer_comp_total_def"] or 0) > 0]
        sc = [(a, b) for a, b in pairs if (a["staff_cost_l5_10"] or 0) > 0 and (b["staff_cost_l5_10"] or 0) > 0]
        da = [(a, b) for a, b in pairs if (a["daf_assets_eoy"] or 0) > 0 and (b["daf_assets_eoy"] or 0) > 0]
        yrs = end - base
        cagr = lambda a, b: (b / a) ** (1 / yrs) - 1  # noqa: E731
        if not pairs:
            continue
        out.append({"record_type": "segment_trend", "segment": seg, "tax_year": f"{base}-{end}", "n_returns": len(pairs),
                    "n_top_officer_paid": len(pp),
                    "median_top_officer_comp_cagr": median(cagr(a["top_officer_comp_total_def"], b["top_officer_comp_total_def"]) for a, b in pp),
                    "pooled_top_officer_comp_cagr": cagr(sum(a["top_officer_comp_total_def"] for a, _ in pp),
                                                         sum(b["top_officer_comp_total_def"] for _, b in pp)) if pp else None,
                    "median_staff_cost_cagr": median(cagr(a["staff_cost_l5_10"], b["staff_cost_l5_10"]) for a, b in sc),
                    "pooled_staff_cost_cagr": cagr(sum(a["staff_cost_l5_10"] for a, _ in sc), sum(b["staff_cost_l5_10"] for _, b in sc)) if sc else None,
                    "median_daf_assets_cagr": median(cagr(a["daf_assets_eoy"], b["daf_assets_eoy"]) for a, b in da),
                    "pooled_daf_assets_cagr": cagr(sum(a["daf_assets_eoy"] for a, _ in da), sum(b["daf_assets_eoy"] for _, b in da)) if da else None,
                    "top_officer_changed_title_or_person": sum(1 for a, b in pp if norm_name(a["top_officer_name"]) != norm_name(b["top_officer_name"]))})
    return tuple(out)


def ols_loglog(pairs: Sequence[tuple[float, float]]) -> dict:
    pts = [(math.log(x), math.log(y)) for x, y in pairs if x and y and x > 0 and y > 0]
    if len(pts) < 3:
        return {"n": len(pts)}
    mx, my = statistics.fmean(p[0] for p in pts), statistics.fmean(p[1] for p in pts)
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    syy = sum((p[1] - my) ** 2 for p in pts)
    return {"n": len(pts), "slope": round(sxy / sxx, 3), "r2": round(sxy * sxy / (sxx * syy), 3) if syy else None}


def elasticities(rows: Sequence[Mapping], ty: int = 2024) -> dict:
    """Top-officer pay vs scale, sponsors with a paid top officer (org column > 0), one row per sponsor."""
    paid = [r for r in rows if r["tax_year"] == ty and (r["top_officer_comp_org_d"] or 0) > 0]
    grp = {"community_foundation": [r for r in paid if r["segment"] == "community_foundation"],
           "all_ex_university_digital": [r for r in paid if r["segment"] not in ("university_health", "digital_first")]}
    return {g: {"vs_total_assets": ols_loglog([(r["total_assets_eoy"], r["top_officer_comp_total_def"]) for r in rs]),
                "vs_daf_assets": ols_loglog([(r["daf_assets_eoy"], r["top_officer_comp_total_def"]) for r in rs]),
                "vs_employees_v2a": ols_loglog([(r["employees_part_v_2a"], r["top_officer_comp_total_def"]) for r in rs])}
            for g, rs in grp.items()}


# ----------------------------------------------------------------------------- CLI (I/O edge)
FIELDS_SY = ("record_type", "ein", "sponsor_name", "rank_fy2024", "segment", "segment_note", "fy", "tax_year", "tax_period", "object_id",
             "returns_for_period", "return_ts", "amended_ind", "xml_source", "employees_part_v_2a", "employees_part_i_5", "part_vii_listed",
             "part_vii_paid", "institutional_trustee_names", "institutional_trustee_comp_def", "part_vii_n_over_100k", "part_vii_sum_org_d", "part_vii_sum_related_e", "part_vii_sum_other_f",
             "part_vii_tot_org", "part_vii_tot_related", "part_vii_tot_other", "related_share_of_part_vii", "top6_comp_total",
             "top6_comp_related", "l05", "l06", "l07", "l08", "l09", "l10", "staff_cost_l5_10", "l25_total_expenses", "total_assets_eoy",
             "daf_assets_eoy", "daf_assets_source", "daf_accounts", "daf_accounts_source", "top_officer_title", "top_officer_name",
             "top_officer_basis", "top_officer_hours_org", "top_officer_hours_related", "top_officer_comp_org_d",
             "top_officer_comp_related_e", "top_officer_comp_other_f", "top_officer_comp_total_def", "top_officer_schj_total",
             "top_officer_schj_matched", "top_officer_shared_with", "sched_j_present", "top_pay_per_bn_daf", "top_pay_per_1000_accounts",
             "top_pay_per_bn_total_assets", "staff_cost_bps_daf_assets", "staff_cost_bps_total_assets", "staff_cost_per_account",
             "staff_cost_per_employee", "ctx_operating_cost_ex_invest_mgmt", "ctx_outside_services_l11", "ctx_fees_mgmt_l11a",
             "ctx_fees_other_l11g", "ctx_staff_share_of_opex_ex_l11f", "ctx_fee_and_trustee_bps_daf_assets",
             "flag_affiliate_pay", "sched_r_related_names", "sched_o_comp_text", "xml_url")
FIELDS_P = ("person_role", "person_name", "title", "roles", "hours_org", "hours_related", "comp_org_d", "comp_related_e", "comp_other_f",
            "comp_total_def", "schj_matched", "schj_base_org", "schj_base_related", "schj_bonus_org", "schj_bonus_related", "schj_other_org",
            "schj_other_related", "schj_deferred_org", "schj_deferred_related", "schj_nontaxable_org", "schj_nontaxable_related",
            "schj_total_org", "schj_total_related", "schj_prior_990_org", "schj_prior_990_related")
FIELDS_AGG = ("n_returns", "n_top_officer_paid", "median_top_officer_comp", "median_top_pay_per_bn_daf", "median_top_pay_per_1000_accounts",
              "median_top_pay_per_bn_total_assets", "n_top_paid_by_org", "n_top_paid_related_only", "n_top_zero_or_none",
              "median_top6_comp", "median_top6_share_of_staff_cost", "median_n_over_100k", "pooled_staff_plus_l11a_bps_daf_ctx", "n_ctx",
              "median_staff_cost_bps_daf_assets", "median_staff_cost_bps_total_assets", "median_staff_cost_per_account",
              "median_employees_part_v_2a", "sum_staff_cost_l5_10", "sum_daf_assets", "pooled_staff_cost_bps_daf_assets",
              "sum_part_vii_related_e", "sum_part_vii_org_d", "n_flag_affiliate_pay", "median_top_officer_comp_cagr",
              "pooled_top_officer_comp_cagr", "median_staff_cost_cagr", "pooled_staff_cost_cagr", "median_daf_assets_cagr",
              "pooled_daf_assets_cagr", "top_officer_changed_title_or_person")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args(argv)
    pn = panel(read_csv(DAFRC_CSV), read_csv(ITEMIZED_CSV))
    top = top_sponsors(pn)
    uni = {**{t["ein"]: {**t} for t in top}, **{e: {"ein": e, "rank": "", "fy2024_daf_assets_corrected": (pn.get((e, 2024)) or {}).get("assets")}
                                                for e in DIGITAL}}
    meta = {e: {**u, "name": (pn.get((e, 2024)) or {}).get("name", ""), "segment": segment_of(e, pn)[0],
                "segment_note": segment_of(e, pn)[1]} for e, u in uni.items()}
    filings = sorted(load_index(a.irs_dir, frozenset(uni)), key=lambda f: (f["ein"], f["tax_period"]))
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        exs = dict(zip((f["object_id"] for f in filings), ex.map(lambda f: fetch_extract(f, a.work_dir, a.fetch), filings)))
    ok = [f for f in filings if exs[f["object_id"]].get("xml_status") == "ok"]
    cost = {r["return_object_id"]: r for r in read_csv(COST_CSV)}
    built = [sponsor_year(f, exs[f["object_id"]], meta[f["ein"]], pn, cost) for f in ok]
    sy = mark_shared_officers(tuple(r for r, _ in built))
    people = tuple(p for _, ps in built for p in ps)
    sy_one = latest_per_sponsor_ty(sy)
    agg = segment_year_rows(sy_one) + trend_rows(sy_one)
    fields = FIELDS_SY + tuple(k for k in FIELDS_P if k not in FIELDS_SY) + tuple(k for k in FIELDS_AGG if k not in FIELDS_SY)
    write_csv(OUT_CSV, (*sy, *people, *agg), fields)
    missing = [f for f in filings if exs[f["object_id"]].get("xml_status") != "ok"]
    print(json.dumps({"universe": len(uni), "returns_indexed": len(filings), "returns_ok": len(ok),
                      "not_ok": [(f["ein"], f["tax_period"], f["object_id"], exs[f["object_id"]].get("xml_status")) for f in missing],
                      "elasticities_ty2024": elasticities(sy_one),
                      "sponsor_years": len(sy), "sponsor_ty_unique": len(sy_one), "person_rows": len(people),
                      "no_return": sorted(set(uni) - {f["ein"] for f in ok})}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
