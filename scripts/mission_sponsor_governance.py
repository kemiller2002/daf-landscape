#!/usr/bin/env python3
"""Financial-reporting and governance answers of DAF sponsors on Form 990, TY2022-2024 (task b49-05).

Stdlib only; functional style (pure transforms, I/O at the edges).

Population
  * top50   the 50 largest sponsors by FY2024 end-of-year DAF assets in the DAFRC panel after applied corrections
            (same universe and code as mission_sponsor_compensation.top_sponsors).
  * sample  a seeded simple random sample (random.Random(SEED).sample, SEED = 4905) of 100 sponsors drawn from the
            FY2024 DAFRC rows ranked 51+ with corrected DAF assets > 0, EINs sorted before sampling.

Returns: every RETURN_TYPE = 990 row in IRS index_2023..index_2026 for those EINs whose tax year (year in which the
period begins) is 2022-2024; one return per EIN x tax period (highest OBJECT_ID, which picks up amendments).
Sampled sponsors that file only 990-EZ / 990-PF in those years are kept as `no_full_990` rows (990-EZ has no Part VI
or Part XII).

What it reads per return (e-file XML; local caches first, then the GivingTuesday S3 mirror, then the IRS TEOS zip
by HTTP range request):
  Part XII   accounting method (2023+ schema: cash / accrual / other X boxes); lines 2a compiled-or-reviewed,
             2b audited, 2c audit committee; 3a/3b Single Audit
  Part VI    1a/1b voting and independent members; 2-10 structure items; 11a 990 provided to the board;
             12a-c conflict-of-interest policy; 13 whistleblower; 14 document retention; 15a/15b compensation process;
             16a joint ventures
  Part I     line 5 employees, line 6 volunteers;  Part V line 2a W-2 employees
  Part IV    25a/25b excess-benefit transaction; 26 loans; 27 grants; 28a-c business transactions
  Sched L    every Part I-IV row (individuals' names are masked as "[individual]"; businesses kept as filed)
  Sched O    entries referencing Part VI or Part XII lines (verbatim, truncated)

Inputs (read only): data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv, dafrc-corrections-itemized.csv,
  sponsor-executive-compensation-2021-2025.csv, sponsor-financial-resilience-2021-2024.csv; IRS index_YYYY.csv files.
Output: data/mission-2026-11-14/sponsor-governance-quality-2026-11-20.csv
  record_type = sponsor_year | no_full_990 | schedule_l | band_item | comparison

Usage:
  python3 scripts/mission_sponsor_governance.py . --irs-dir IRS --work-dir WORK [--xml-cache DIR ...] [--fetch]
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import NS, XML_URL, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_sponsor_compensation import panel, segment_of, tax_year, teos_bytes, top_sponsors  # noqa: E402

EXTRACT_VERSION = 6
SEED = 4905
SAMPLE_N = 100
TAX_YEARS = (2022, 2023, 2024)
INDEX_YEARS = (2023, 2024, 2025, 2026)
UA = {"User-Agent": "research-script/1.0 (stdlib urllib)"}
OUT_NAME = "sponsor-governance-quality-2026-11-20.csv"
OID_FILE = re.compile(r"^(\d{18})(?:_public)?\.xml$")

# size bands on FY2024 corrected DAF assets (fixed before looking at answers)
BANDS = ((1e9, "A_ge_1bn"), (1e8, "B_100m_1bn"), (1e7, "C_10m_100m"), (0, "D_lt_10m"))

# (column, XML tag, form reference) for yes/no items
YN_ITEMS = (
    ("xii_2a_compiled_reviewed", "AccountantCompileOrReviewInd", "Part XII 2a"),
    ("xii_2b_audited", "FSAuditedInd", "Part XII 2b"),
    ("xii_2c_audit_committee", "AuditCommitteeInd", "Part XII 2c"),
    ("xii_3a_single_audit_required", "FederalGrantAuditRequiredInd", "Part XII 3a"),
    ("xii_3b_single_audit_done", "FederalGrantAuditPerformedInd", "Part XII 3b"),
    ("vi_2_family_business_rel", "FamilyOrBusinessRlnInd", "Part VI 2"),
    ("vi_3_delegated_mgmt", "DelegationOfMgmtDutiesInd", "Part VI 3"),
    ("vi_4_doc_changes", "ChangeToOrgDocumentsInd", "Part VI 4"),
    ("vi_5_diversion", "MaterialDiversionOrMisuseInd", "Part VI 5"),
    ("vi_6_members_stockholders", "MembersOrStockholdersInd", "Part VI 6"),
    ("vi_7a_members_elect_board", "ElectionOfBoardMembersInd", "Part VI 7a"),
    ("vi_7b_members_approve", "DecisionsSubjectToApprovaInd", "Part VI 7b"),
    ("vi_8a_minutes_board", "MinutesOfGoverningBodyInd", "Part VI 8a"),
    ("vi_8b_minutes_committees", "MinutesOfCommitteesInd", "Part VI 8b"),
    ("vi_11a_990_to_board", "Form990ProvidedToGvrnBodyInd", "Part VI 11a"),
    ("vi_12a_coi_policy", "ConflictOfInterestPolicyInd", "Part VI 12a"),
    ("vi_12b_coi_annual_disclosure", "AnnualDisclosureCoveredPrsnInd", "Part VI 12b"),
    ("vi_12c_coi_monitoring", "RegularMonitoringEnfrcInd", "Part VI 12c"),
    ("vi_13_whistleblower", "WhistleblowerPolicyInd", "Part VI 13"),
    ("vi_14_doc_retention", "DocumentRetentionPolicyInd", "Part VI 14"),
    ("vi_15a_comp_process_ceo", "CompensationProcessCEOInd", "Part VI 15a"),
    ("vi_15b_comp_process_officers", "CompensationProcessOtherInd", "Part VI 15b"),
    ("vi_16a_joint_venture", "InvestmentInJointVentureInd", "Part VI 16a"),
    ("iv_25a_excess_benefit_cy", "EngagedInExcessBenefitTransInd", "Part IV 25a"),
    ("iv_25b_excess_benefit_py", "PYExcessBenefitTransInd", "Part IV 25b"),
    ("iv_26_loans_interested", "LoanOutstandingInd", "Part IV 26"),
    ("iv_27_grants_interested", "GrantToRelatedPersonInd", "Part IV 27"),
    ("iv_28a_bus_tr_officer", "BusinessRlnWithOrgMemInd", "Part IV 28a"),
    ("iv_28b_bus_tr_family", "BusinessRlnWithFamMemInd", "Part IV 28b"),
    ("iv_28c_bus_tr_35pct_entity", "BusinessRlnWith35CtrlEntInd", "Part IV 28c"),
)
COUNT_ITEMS = (
    ("vi_1a_voting_members", "GoverningBodyVotingMembersCnt"),
    ("vi_1b_independent_members", "IndependentVotingMemberCnt"),
    ("i_5_employees", "TotalEmployeeCnt"),
    ("i_6_volunteers", "TotalVolunteersCnt"),
    ("v_2a_w2_employees", "EmployeeCnt"),
)
# key policies whose "No" answers are listed by name; Part VI line keys used to match Schedule O references
KEY_POLICIES = (("vi_12a_coi_policy", "12A"), ("vi_13_whistleblower", "13"), ("vi_14_doc_retention", "14"),
                ("vi_11a_990_to_board", "11A"), ("vi_15a_comp_process_ceo", "15A"), ("vi_15b_comp_process_officers", "15B"))
SCHED_L = (("I_excess_benefit", "DisqualifiedPersonExBnftTrGrp"), ("II_loans", "LoansBtwnOrgInterestedPrsnGrp"),
           ("III_grants_assistance", "GrntAsstBnftInterestedPrsnGrp"), ("IV_business_tr", "BusTrInvolveInterestedPrsnGrp"))
PART_LINE = re.compile(r"PART\s*(XII|VI)\b(?:[^L]|L(?!INE))*?LINES?\s*(\d{1,2}\s*[A-C]?)", re.I)


# ----------------------------------------------------------------------------- pure helpers
def yn(v: str | None) -> str:
    s = (v or "").strip().lower()
    return "Y" if s in ("true", "1", "x") else "N" if s in ("false", "0") else ""


def band(assets: float | None) -> str:
    return next((lab for lo, lab in BANDS if (assets or 0) >= lo), BANDS[-1][1])


def clip(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def line_refs(ref: str) -> tuple[str, ...]:
    return tuple(f"{p.upper()}:{re.sub(r'\s', '', ln).upper()}" for p, ln in PART_LINE.findall(ref or ""))


def pct(k: int, n: int) -> float | None:
    return round(100.0 * k / n, 1) if n else None


# ----------------------------------------------------------------------------- XML extract (streamed)
ORG_MARK = re.compile(r"\b(INC|LLC|L\.L\.C|LLP|LP|PC|P\.C|CO|CORP|CORPORATION|COMPANY|GROUP|FOUNDATION|TRUST|FUND|BANK|"
                      r"MANAGEMENT|SERVICES?|INSURANCE|DISTRIBUTORS|ADVISORY|ADVISORS|PARTNERS|ASSOCIATES|CENTER|CENTRE|"
                      r"UNIVERSITY|SCHOOL|CHURCH|SOCIETY|FIRM|HOLDINGS|CAPITAL|INVESTMENTS?|SCHOLARSHIP|ORGANIZATION)\b", re.I)
PERSON_HINT = re.compile(r"FORMER|\bCEO\b|EXEC(?:UTIVE)? DIR|\bMRS?\b|\bDR\b|BOARD MEMBER|TRUSTEE", re.I)
ROLE_CATS = (("family_member", r"SPOUSE|SON\b|DAUGHTER|GRANDSON|GRANDDAUGHTER|FAMILY|BROTHER|SISTER|FATHER|MOTHER|IN-LAW"),
             ("donor_or_donor_advisor", r"DONOR"),
             ("substantial_contributor", r"SUBSTANTIAL CONTRIBUTOR"),
             ("founder_or_creator", r"FOUNDER|CREATOR"),
             ("controlled_or_affiliated_entity", r"CONTROLLED|35%|OWNED|SUB\.|SUBSIDIARY|SUPPORTING|AFFILIAT"),
             ("board_member_trustee_director", r"BOARD|TRUSTEE|DIRECTOR|COMMITTEE|CHAIR"),
             ("officer_or_key_employee", r"OFFICER|PRESIDENT|TREASURER|SECRETARY|KEY EMPLOYEE|CEO|EXECUTIVE"),
             ("employee", r"EMPLOYEE"))
TX_CATS = (("compensation", r"COMPENSATION|SALARY|WAGES"),
           ("admin_or_management_services", r"ADMIN|MANAGEMENT CONTRACT|OCCUPANCY|TURN-KEY|SERVICES AGREEMENT"),
           ("investment_brokerage_custody", r"INVEST|BROKER|CUSTOD|BANKING|ADVISORY FEE"),
           ("professional_services", r"LEGAL|LAW FIRM|ACCOUNTING|CONSULT|MARKETING|PROFESSIONAL|LEGISLATIVE|INSURANCE"),
           ("sale_or_donation_of_assets", r"SALE OF|DONATED|LAND|BUILDING|SHARES"),
           ("grant_or_fiscal_sponsorship", r"GRANT|FISCAL SPONSOR"),
           ("sponsorship_or_event", r"SPONSORSHIP|ENDORSEMENT|VIDEOGRAPH|TRAVEL"),
           ("interest_or_loan", r"INTEREST|LOAN"))
PART_TX = {"I_excess_benefit": "excess_benefit_4958", "II_loans": "loan", "III_grants_assistance": "grant_or_assistance"}


def categorise(text: str, cats) -> str:
    return next((c for c, rx in cats if re.search(rx, text or "", re.I)), "other_or_unstated")


def sched_l_rows(el) -> list:
    """Schedule L Parts I-IV rows. Names are kept only when the filer entered an organisation name (org marker in
    the name); otherwise '[individual]'. Relationship and description are emitted as categories, not free text,
    because the free text often names individuals."""
    def leaves(g):
        return [(local(c.tag), (c.text or "").strip()) for c in g.iter() if len(c) == 0]
    def one(part, g):
        lv = leaves(g)
        person = g.findtext(f".//{NS}PersonNm")
        biz = g.findtext(f".//{NS}BusinessNameLine1Txt")
        rel = next((v for k, v in lv if k.startswith(("Rln", "Relationship"))), "")
        desc = " ".join(v for k, v in lv if k.endswith(("Desc", "Txt")) and not k.startswith(("Rln", "Relationship",
                                                                                                "BusinessName", "PersonNm")))
        amts = [(k, num(v)) for k, v in lv if k.endswith("Amt") and num(v) is not None]
        is_org = bool(biz and ORG_MARK.search(biz) and not PERSON_HINT.search(biz))
        return {"sl_part": part, "sl_name": clip(biz, 80) if is_org else ("[individual]" if (person or biz) else ""),
                "sl_name_type": "organisation" if is_org else ("individual" if person else
                                                               "individual_name_in_business_field" if biz else ""),
                "sl_relationship": categorise(rel, ROLE_CATS), "sl_amount": amts[0][1] if amts else None,
                "sl_amount_field": amts[0][0] if amts else "",
                "sl_description": PART_TX.get(part) or next((c for c in (categorise(desc, TX_CATS), categorise(rel, TX_CATS))
                                                             if c != "other_or_unstated"), "other_or_unstated"),
                "sl_corrected_ind": yn(g.findtext(f"{NS}TransactionCorrectedInd"))}
    return [one(part, g) for part, tag in SCHED_L for g in el.iter(NS + tag)]


POLICY_WORDS = {"12A": r"CONFLICTS? OF INTEREST", "13": r"WHISTLE ?BLOWER", "14": r"(?:DOCUMENT|RECORDS?) (?:RETENTION|DESTRUCTION)",
                "11A": r"(?:COPY|DRAFT) OF (?:THE )?(?:FORM )?990|990 (?:WAS|IS) (?:PROVIDED|DISTRIBUTED|REVIEWED)",
                "15A": r"COMPENSATION", "15B": r"COMPENSATION"}


def sched_o_rows(el) -> list:
    """Schedule O entries that cite a Part VI / Part XII line, or whose text names one of the key policies."""
    rows = ((g.findtext(NS + "FormAndLineReferenceDesc") or "", g.findtext(NS + "ExplanationTxt") or "")
            for g in el.iter(NS + "SupplementalInformationDetail"))
    keep = lambda r, t: line_refs(r) or any(re.search(w, t, re.I) for w in POLICY_WORDS.values())  # noqa: E731
    return [{"ref": clip(r, 120), "lines": line_refs(r), "text": clip(t, 700),
             "policies": [k for k, w in POLICY_WORDS.items() if re.search(w, r + " " + t, re.I)]}
            for r, t in rows if keep(r, t)]


def irs990_fields(el) -> dict:
    other = el.find(NS + "MethodOfAccountingOtherInd")
    other_desc = (other.get("methodOfAccountingOtherDesc") if other is not None else "") or \
        el.findtext(NS + "MethodOfAccountingOtherDesc") or ""
    method = "|".join(m for m, t in (("cash", "MethodOfAccountingCashInd"), ("accrual", "MethodOfAccountingAccrualInd"),
                                      ("other", "MethodOfAccountingOtherInd")) if el.find(NS + t) is not None)
    basis = lambda g: "|".join(b for b, t in (("separate", "SeparateBasisFinclStmtInd"),  # noqa: E731
                                              ("consolidated", "ConsolidatedBasisFinclStmtInd"),
                                              ("both", "ConsolAndSepBasisFinclStmtInd"))
                               if el.find(f"{NS}{g}/{NS}{t}") is not None)
    return {"xii_1_method": method, "xii_1_other_desc": clip(other_desc, 80),
            "xii_2a_basis": basis("AcctCompileOrReviewBasisGrp"), "xii_2b_basis": basis("FSAuditedBasisGrp"),
            **{c: yn(el.findtext(NS + t)) for c, t, _ in YN_ITEMS},
            **{c: num(el.findtext(NS + t)) for c, t in COUNT_ITEMS},
            "total_assets_eoy": num(el.findtext(f"{NS}TotalAssetsGrp/{NS}EOYAmt")),
            "total_expenses": num(el.findtext(NS + "CYTotalExpensesAmt"))}


def extract_stream(stream) -> dict:
    def step(acc, ev):
        _, e = ev
        tag = local(e.tag)
        if tag == "ReturnHeader":
            acc = {**acc, "tax_period_begin": e.findtext(f".//{NS}TaxPeriodBeginDt") or "",
                   "tax_period_end": e.findtext(f".//{NS}TaxPeriodEndDt") or "",
                   "return_type_hdr": e.findtext(f".//{NS}ReturnTypeCd") or "",
                   "amended": yn(e.findtext(f".//{NS}AmendedReturnInd"))}
        elif tag == "IRS990":
            acc = {**acc, **irs990_fields(e)}
        elif tag == "IRS990ScheduleL":
            acc = {**acc, "sched_l_present": "Y", "sched_l": sched_l_rows(e),
                   "sl_i_tax_imposed": num(e.findtext(NS + "TaxImposedAmt"))}
        elif tag == "IRS990ScheduleO":
            acc = {**acc, "sched_o": sched_o_rows(e)}
        else:
            return acc
        e.clear()
        return acc
    return reduce(step, ET.iterparse(stream, events=("end",)), {"sched_l": [], "sched_o": [], "sched_l_present": "N"})


# ----------------------------------------------------------------------------- I/O edge: caches and fetch
def scan_xml_cache(dirs: Sequence[str]) -> dict:
    found = ((m.group(1), os.path.join(d, f)) for top in dirs for d, _, fs in os.walk(top) for f in fs
             for m in [OID_FILE.match(f)] if m)
    return dict(sorted(found, key=lambda kv: os.path.getsize(kv[1])))   # larger file wins (truncated copies lose)


def from_bytes(data: bytes, src: str) -> dict:
    return {**extract_stream(io.BytesIO(data)), "xml_status": "ok", "xml_source": src}


def fetch_extract(f: Mapping, cache: Mapping, work_dir: str, fetch: bool) -> dict:
    path = os.path.join(work_dir, "extract", f"{f['object_id']}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == EXTRACT_VERSION:
            return c
    res = local_extract(f, cache) or (remote_extract(f, work_dir) if fetch else {"xml_status": "not_fetched"})
    out = {**res, "_v": EXTRACT_VERSION}
    if out["xml_status"] == "ok" or out["xml_status"].startswith("http_"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(out, fh)
    return out


def local_extract(f: Mapping, cache: Mapping) -> dict | None:
    p = cache.get(f["object_id"])
    if not p:
        return None
    try:
        with open(p, "rb") as fh:
            r = from_bytes(fh.read(), "local_cache:" + XML_URL.format(oid=f["object_id"]))
        return r if "tax_period_end" in r else None
    except ET.ParseError:
        return None


def remote_extract(f: Mapping, work_dir: str, retries: int = 2) -> dict:
    url = XML_URL.format(oid=f["object_id"])
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                return from_bytes(r.read(), url)
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                try:
                    data, src = teos_bytes(f, work_dir)
                except (urllib.error.URLError, OSError, ValueError) as e2:
                    data, src = None, f"teos_error:{type(e2).__name__}"
                return from_bytes(data, src) if data else {"xml_status": f"http_{e.code}_{src}"}
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
            last = f"error:{type(e).__name__}"
            time.sleep(2 * (attempt + 1))
    return {"xml_status": locals().get("last", "error:retries")}


def load_index(irs_dir: str, eins: frozenset) -> tuple[dict, ...]:
    def rows(y):
        with open(os.path.join(irs_dir, f"index_{y}.csv"), newline="", encoding="latin-1") as fh:
            yield from ({"ein": ein9(r["EIN"]), "tax_period": r["TAX_PERIOD"], "object_id": r["OBJECT_ID"],
                         "return_type": r["RETURN_TYPE"], "index_year": y, "batch": r.get("XML_BATCH_ID") or ""}
                        for r in csv.DictReader(fh) if ein9(r["EIN"]) in eins)
    return tuple(r for y in INDEX_YEARS for r in rows(y)
                 if r["tax_period"].isdigit() and tax_year(r["tax_period"]) in TAX_YEARS)


def pick_returns(idx: Sequence[Mapping]) -> tuple[dict, ...]:
    full = [r for r in idx if r["return_type"] == "990"]
    best = reduce(lambda acc, r: {**acc, (r["ein"], r["tax_period"]): r}
                  if (r["ein"], r["tax_period"]) not in acc or r["object_id"] > acc[(r["ein"], r["tax_period"])]["object_id"]
                  else acc, full, {})
    return tuple(sorted(best.values(), key=lambda r: (r["ein"], r["tax_period"])))


# ----------------------------------------------------------------------------- population
def population(pn: Mapping) -> tuple[dict, ...]:
    top = top_sponsors(pn)
    top_eins = frozenset(t["ein"] for t in top)
    frame = sorted(e for (e, fy), v in pn.items() if fy == 2024 and e not in top_eins and (v.get("assets") or 0) > 0)
    sample = random.Random(SEED).sample(frame, SAMPLE_N)
    fy24 = sorted(((v.get("assets") or 0, e) for (e, fy), v in pn.items() if fy == 2024), reverse=True)
    rank = {e: i for i, (_, e) in enumerate(fy24, 1)}
    meta = lambda e, grp: {"ein": e, "group": grp, "rank_fy2024": rank.get(e),  # noqa: E731
                           "sponsor_name": pn[(e, 2024)]["name"], "dafrc_type": pn[(e, 2024)]["type"],
                           "dafrc_subtype": pn[(e, 2024)]["subtype"], "fy2024_daf_assets": pn[(e, 2024)].get("assets"),
                           "size_band": band(pn[(e, 2024)].get("assets")), "segment": segment_of(e, pn)[0],
                           "frame_size": len(frame) if grp == "sample" else None}
    return tuple([meta(t["ein"], "top50") for t in top] + [meta(e, "sample") for e in sample])


# ----------------------------------------------------------------------------- row builders (pure)
def cites(o: Mapping, line: str) -> bool:
    """Schedule O entry cites Part VI <line> (a bare 'line 15' covers 15a and 15b) or names the policy in its text."""
    return f"VI:{line}" in o["lines"] or (line[-1].isalpha() and f"VI:{line[:-1]}" in o["lines"]) or \
        (line in ("12A", "13", "14") and line in o.get("policies", []))


def sched_o_for_no(x: Mapping) -> dict:
    so = x.get("sched_o") or []
    def text_for(col, line):
        if x.get(col) != "N":
            return ""
        return " || ".join(f"[{o['ref']}] {o['text']}" for o in so if cites(o, line))[:900]
    l11b = next((o for o in so if "VI:11B" in o["lines"]), None)
    return {**{f"so_no_{c}": text_for(c, ln) for c, ln in KEY_POLICIES},
            "so_vi_11b_review_process": clip(l11b["text"], 400) if l11b else "",
            "so_vi_refs": " ".join(sorted({ln for o in so for ln in o["lines"]})),
            "n_key_policy_no": sum(1 for c, _ in KEY_POLICIES if x.get(c) == "N"),
            "n_key_policy_no_explained": sum(1 for c, ln in KEY_POLICIES if x.get(c) == "N" and any(cites(o, ln) for o in so))}


def sponsor_year(f: Mapping, x: Mapping, m: Mapping, comp: Mapping, res: Mapping) -> dict:
    ty = tax_year(f["tax_period"])
    c = comp.get((f["ein"], str(ty)), {})
    r = res.get((f["ein"], str(ty)), {})
    vm, ind = x.get("vi_1a_voting_members"), x.get("vi_1b_independent_members")
    return {"record_type": "sponsor_year", **m, "tax_year": ty, "tax_period": f["tax_period"],
            "object_id": f["object_id"], "index_year": f["index_year"], "xml_status": x.get("xml_status", ""),
            "xml_source": x.get("xml_source", ""), "amended": x.get("amended", ""),
            **{k: x.get(k) for k in ("xii_1_method", "xii_1_other_desc", "xii_2a_basis", "xii_2b_basis",
                                     "total_assets_eoy", "total_expenses", "sched_l_present", "sl_i_tax_imposed")},
            **{col: x.get(col) for col, _, _ in YN_ITEMS}, **{col: x.get(col) for col, _ in COUNT_ITEMS},
            "independent_share": round(ind / vm, 3) if vm and ind is not None else None,
            "assurance_level": ("audited" if x.get("xii_2b_audited") == "Y" else
                                "compiled_or_reviewed" if x.get("xii_2a_compiled_reviewed") == "Y" else
                                "none_reported" if x.get("xii_2b_audited") == "N" else ""),
            "n_sched_l_rows": len(x.get("sched_l") or []),
            **sched_o_for_no(x),
            "ctx_comp_top_officer_comp_total": c.get("top_officer_comp_total_def"),
            "ctx_comp_flag_affiliate_pay": c.get("flag_affiliate_pay"),
            "ctx_comp_staff_cost_l5_10": c.get("staff_cost_l5_10"),
            "ctx_res_sponsor_group": r.get("sponsor_group"),
            "ctx_res_months_opcost_r1": r.get("months_opcost_r1"),
            "ctx_res_quality_flags": r.get("quality_flags")}


def sched_l_records(f: Mapping, x: Mapping, m: Mapping) -> list:
    return [{"record_type": "schedule_l", **{k: m[k] for k in ("ein", "group", "sponsor_name", "size_band", "rank_fy2024")},
             "tax_year": tax_year(f["tax_period"]), "tax_period": f["tax_period"], "object_id": f["object_id"], **s}
            for s in x.get("sched_l") or []]


def latest_per_sponsor(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    ok = [r for r in rows if r["xml_status"] == "ok"]
    best = reduce(lambda a, r: {**a, r["ein"]: r} if r["ein"] not in a or r["tax_period"] > a[r["ein"]]["tax_period"]
                  else a, ok, {})
    return tuple(best.values())


def band_items(latest: Sequence[Mapping]) -> list:
    groups = (("all", lambda r: True), ("top50", lambda r: r["group"] == "top50"),
              ("sample", lambda r: r["group"] == "sample"),
              *((b, (lambda b: lambda r: r["size_band"] == b)(b)) for _, b in BANDS))
    def yn_row(gname, sel, col, ref):
        rs = [r for r in latest if sel(r)]
        y, n = sum(1 for r in rs if r[col] == "Y"), sum(1 for r in rs if r[col] == "N")
        return {"record_type": "band_item", "band": gname, "item": col, "form_ref": ref, "n_sponsors": len(rs),
                "n_yes": y, "n_no": n, "n_blank": len(rs) - y - n, "pct_yes_of_answered": pct(y, y + n)}
    def cat_row(gname, sel, col, val):
        rs = [r for r in latest if sel(r)]
        k = sum(1 for r in rs if (r.get(col) or "") == val)
        return {"record_type": "band_item", "band": gname, "item": f"{col}={val or 'blank'}", "n_sponsors": len(rs),
                "n_yes": k, "pct_yes_of_answered": pct(k, len(rs))}
    def med_row(gname, sel, col):
        v = sorted(r[col] for r in latest if sel(r) and r.get(col) is not None)
        med = (v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2) if v else None
        return {"record_type": "band_item", "band": gname, "item": f"median_{col}", "n_sponsors": len(v),
                "median": med, "n_zero": sum(1 for x in v if x == 0)}
    cats = (("xii_1_method", ("accrual", "cash", "other", "")),
            ("assurance_level", ("audited", "compiled_or_reviewed", "none_reported", "")))
    return ([yn_row(g, s, c, ref) for g, s in groups for c, _, ref in YN_ITEMS] +
            [cat_row(g, s, c, v) for g, s in groups for c, vals in cats for v in vals] +
            [med_row(g, s, c) for g, s in groups for c in ("vi_1a_voting_members", "vi_1b_independent_members",
                                                          "independent_share", "i_5_employees", "i_6_volunteers")])


def comparison_rows(latest: Sequence[Mapping]) -> list:
    """Cross-tabs of governance answers against the compensation and resilience context columns (TY latest)."""
    top = [r for r in latest if r["group"] == "top50"]
    def row(name, sel, col):
        rs = [r for r in top if sel(r)]
        y, n = sum(1 for r in rs if r[col] == "Y"), sum(1 for r in rs if r[col] == "N")
        return {"record_type": "comparison", "band": name, "item": col, "n_sponsors": len(rs), "n_yes": y, "n_no": n,
                "pct_yes_of_answered": pct(y, y + n)}
    paid = lambda r: num(r.get("ctx_comp_top_officer_comp_total")) not in (None, 0)  # noqa: E731
    unpaid = lambda r: num(r.get("ctx_comp_top_officer_comp_total")) == 0  # noqa: E731
    noemp = lambda r: (r.get("i_5_employees") or 0) == 0  # noqa: E731
    r1neg = lambda r: num(r.get("ctx_res_months_opcost_r1")) is not None and num(r["ctx_res_months_opcost_r1"]) <= 0  # noqa: E731
    r1pos = lambda r: num(r.get("ctx_res_months_opcost_r1")) is not None and num(r["ctx_res_months_opcost_r1"]) > 0  # noqa: E731
    sels = (("top50_top_officer_paid_by_sponsor", paid), ("top50_top_officer_zero_on_990", unpaid),
            ("top50_zero_employees_part_i_5", noemp), ("top50_res_r1_le_0", r1neg), ("top50_res_r1_gt_0", r1pos))
    cols = ("vi_15a_comp_process_ceo", "vi_15b_comp_process_officers", "vi_12a_coi_policy", "vi_13_whistleblower",
            "vi_14_doc_retention", "xii_2b_audited", "xii_2c_audit_committee", "vi_3_delegated_mgmt")
    return [row(n, s, c) for n, s in sels for c in cols]


def no_full_990_rows(pop: Sequence[Mapping], idx: Sequence[Mapping], have: frozenset) -> list:
    def kinds(e):
        return "|".join(sorted({f"{r['return_type']}:TY{tax_year(r['tax_period'])}" for r in idx if r["ein"] == e}))
    return [{"record_type": "no_full_990", **m, "other_returns_indexed": kinds(m["ein"])}
            for m in pop if m["ein"] not in have]


# ----------------------------------------------------------------------------- main (I/O edge)
FIELDS = ("record_type", "ein", "group", "rank_fy2024", "sponsor_name", "dafrc_type", "dafrc_subtype", "segment",
          "fy2024_daf_assets", "size_band", "frame_size", "tax_year", "tax_period", "object_id", "index_year",
          "xml_status", "xml_source", "amended", "total_assets_eoy", "total_expenses",
          "xii_1_method", "xii_1_other_desc", "assurance_level", "xii_2a_basis", "xii_2b_basis",
          *(c for c, _, _ in YN_ITEMS), *(c for c, _ in COUNT_ITEMS), "independent_share",
          "sched_l_present", "sl_i_tax_imposed", "n_sched_l_rows", "n_key_policy_no", "n_key_policy_no_explained",
          *(f"so_no_{c}" for c, _ in KEY_POLICIES), "so_vi_11b_review_process", "so_vi_refs",
          "ctx_comp_top_officer_comp_total", "ctx_comp_flag_affiliate_pay", "ctx_comp_staff_cost_l5_10",
          "ctx_res_sponsor_group", "ctx_res_months_opcost_r1", "ctx_res_quality_flags",
          "sl_part", "sl_name", "sl_name_type", "sl_relationship", "sl_amount", "sl_amount_field", "sl_description",
          "sl_corrected_ind", "other_returns_indexed",
          "band", "item", "form_ref", "n_sponsors", "n_yes", "n_no", "n_blank", "pct_yes_of_answered", "median", "n_zero")


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--xml-cache", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    data = os.path.join(os.path.abspath(a.root), "data", "mission-2026-11-14")
    pn = panel(read_csv(os.path.join(data, "dafrc-sponsor-schedule-d-fy2019-2024.csv")),
               read_csv(os.path.join(data, "dafrc-corrections-itemized.csv")))
    pop = population(pn)
    meta = {m["ein"]: m for m in pop}
    idx = load_index(a.irs_dir, frozenset(meta))
    picks = pick_returns(idx)
    cache = scan_xml_cache(a.xml_cache)
    with ThreadPoolExecutor(8) as ex:
        exts = dict(zip((p["object_id"] for p in picks),
                        ex.map(lambda p: fetch_extract(p, cache, a.work_dir, a.fetch), picks)))
    comp = {(r["ein"], r["tax_year"]): r for r in read_csv(os.path.join(data, "sponsor-executive-compensation-2021-2025.csv"))
            if r["record_type"] == "sponsor_year"}
    res = {(r["ein"], r["tax_year"]): r for r in read_csv(os.path.join(data, "sponsor-financial-resilience-2021-2024.csv"))
           if r["row_type"] == "sponsor_year"}
    sy = [sponsor_year(p, exts[p["object_id"]], meta[p["ein"]], comp, res) for p in picks]
    sl = [r for p in picks for r in sched_l_records(p, exts[p["object_id"]], meta[p["ein"]])]
    latest = latest_per_sponsor(sy)
    nf = no_full_990_rows(pop, idx, frozenset(p["ein"] for p in picks))
    rows = sy + nf + sl + band_items(latest) + comparison_rows(latest)
    write_csv(os.path.join(data, OUT_NAME), rows, FIELDS)
    status = dict(Counter(r["xml_status"] for r in sy))
    summary = {"population": len(pop), "frame_size": next(m["frame_size"] for m in pop if m["group"] == "sample"),
               "returns_picked": len(picks), "xml_status": status, "sponsors_with_990": len({p["ein"] for p in picks}),
               "no_full_990": len(nf), "schedule_l_rows": len(sl), "latest_sponsors": len(latest),
               "local_cache_hits": sum(1 for r in sy if r["xml_source"].startswith("local_cache")),
               "by_tax_year": {ty: sum(1 for r in sy if r["tax_year"] == ty and r["xml_status"] == "ok") for ty in TAX_YEARS}}
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
