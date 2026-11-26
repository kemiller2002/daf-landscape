#!/usr/bin/env python3
"""Institutional (single-issue charity) DAF programmes: size, trend, host-retention and published host rules
(queue item b50-03).

Stdlib only; functional style (pure transforms, I/O at the edges). pdftotext (poppler) is used, if present, to read
PDF policy pages; without it PDF pages are logged as unparsed.

Segments
  * Tier labels are those of scripts/mission_pf_to_daf_flows.py (tier_of, with segment_of from mission_net_payout.py):
    T1 core (FY2024 top-50 national/processor + 4 core single-issue DAF sponsors: NCF, JCF, DonorsTrust, Thrivent),
    T2 other national/processor, T3 community foundations, T4 all other DAFRC "Single Issue Charity" sponsors.
  * T4 is split here (t4_class):
      institution_edu_health  DAFRC subtype "Universities and Healthcare", or subtype "Other" with IRS EO BMF NTEE
                              major B (education), E, F, G or H (health) -- universities, schools, their foundations,
                              hospitals and health systems
      religious               DAFRC subtype "Religiously-Affiliated" (outside the four T1 core sponsors)
      intermediary_t          subtype "Other" with NTEE major T (philanthropy/grantmaking: Tides, United Way, Pew...)
      mission_other           subtype "Other" with any other NTEE major (national/issue charities: Rotary, NIF...)
      unclassified            subtype "Other" with no NTEE in the BMF extract
    NTEE comes from data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv (bmf_ntee / ntee_major).

Values
  * FY2021-24 sponsor-year values are the corrected DAFRC values (DAFRC 2025 panel overridden by applied R1-R4 rows),
    rebuilt with scripts/mission_league_table.py corrected(); market totals = dafrc-corrected-market-totals.csv. The
    rebuilt per-tier sums are checked against the corrected totals.
  * FY = calendar year in which the tax period ends (DAFRC convention).

Schedule I sample (host retention)
  * Sample = top 20 institution_edu_health + top 8 mission_other T4 sponsors by FY2024 corrected DAF assets; their
    FY2023 and FY2024 Form 990 (object ids from form990-returns-schedule-d-harvest-full.csv), read from the
    GivingTuesday mirror of IRS TEOS e-file XML (robots.txt 404 on 2026-11-20).
  * Per return: D = Schedule D Part I DAF grants; Schedule I Part II lines split into host (recipient EIN = filer, a
    Schedule R related organisation, or a listed HOST_EXTRA EIN), research (purpose says research/sub-award/
    subcontract), DAF-labelled (purpose says DAF / donor advised) and other; unitemised = Part IX line 1 - Schedule I
    total; foreign = Part IX line 3.
  * Host-share bounds (share of D that stayed with the host):
      ext_min = min(D, DAF-labelled non-host lines)
      ext_max = min(D, DAF-labelled + other non-host lines + unitemised + foreign)   [research lines excluded]
      host_min = 1 - ext_max/D;  host_max = 1 - ext_min/D, and for a separate foundation also <= host lines / D
      point estimate only where the filer's grants are essentially all DAF grants (D >= 90% of Part IX lines 1+3):
      then every non-host grant is taken to be a DAF grant and the estimate equals host_min (an assumption).
  * A sponsor that IS the institution pays its DAF grants to itself internally; those never appear on Schedule I.

Policy pages
  * POLICY_PAGES: about 20 public programme pages. robots.txt is read per host and checked for ClaudeBot,
    anthropic-ai, Claude-User, Claude-Web, Claude-SearchBot, research-script/1.0 and *; any disallow, or an
    unreadable (non-200/404) robots.txt, means the page is not fetched. Sentences mentioning a share/minimum are
    extracted verbatim; READINGS records the host rule read from them.

Usage
  python3 scripts/mission_institutional_dafs.py . --cache DIR [--fetch]
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from functools import reduce
from statistics import median
from typing import Iterable, Mapping, Sequence
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, ein9, num, read_csv, write_csv  # noqa: E402
from mission_league_table import METRICS, corrected, identity  # noqa: E402
from mission_net_payout import segment_of  # noqa: E402
from mission_pf_to_daf_flows import tier_of  # noqa: E402

UA = "research-script/1.0"
AI_AGENTS = ("ClaudeBot", "anthropic-ai", "Claude-User", "Claude-Web", "Claude-SearchBot")
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
FYS = (2021, 2022, 2023, 2024)
SAMPLE_FYS = (2023, 2024)
N_INST, N_MISSION = 20, 8
OUT_CSV = "institutional-daf-programs-2026-11-20.csv"
SRC_PANEL = ("DAFRC 2025 panel + R1-R4 corrections (dafrc-sponsor-schedule-d-fy2019-2024.csv, "
             "dafrc-corrections-itemized.csv); totals dafrc-corrected-market-totals.csv; NTEE daf-long-tail-sponsors-fy2021-2024.csv")
SRC_XML = "IRS Form 990 e-file XML (Schedule D Part I, Schedule I Part II, Schedule R, Part IX lines 1 and 3), GivingTuesday mirror"

# Host institutions that are separate entities and not listed on the sponsor's Schedule R (judgment, listed here).
HOST_EXTRA = {"866050388": frozenset({"742652689"}),   # University of Arizona Foundation -> University of Arizona
              "952250801": frozenset({"956006143", "943067788"}),  # UCLA Foundation -> UCLA / UC Regents
              "222848738": frozenset({"150532082"}),   # Cornell University Foundation -> Cornell University
              "166053710": frozenset({"146013200", "510244064"})}  # SUNY Binghamton Foundation -> SUNY Binghamton
SEPARATE_FOUNDATION = frozenset(HOST_EXTRA)            # sponsor is a foundation for a separate host institution

RX_RESEARCH = re.compile(r"RESEARCH|SUB-?AWARD|SUBCONTRACT|SUB-?RECIPIENT|SPONSORED|\bRES\.", re.I)
RX_DAF = re.compile(r"\bDAFS?\b|DONOR[- ]?ADVISED|-DAF\b", re.I)

POLICY_PAGES = (
    ("941156365", "Stanford University", "https://assets.stanford.edu/a/f/78141/x/889a0f5be4/wp_daf_02252025.pdf"),
    ("135598093", "Columbia University", "https://giftplanning.columbia.edu/what-you-can-give/donor-advised-fund"),
    ("060646973", "Yale University", "https://plannedgiving.yale.edu/what-you-can-give/donor-advised-fund"),
    ("060646973", "Yale University", "https://plannedgiving.yale.edu/sites/yale/files/2025-09/Donor%20Advised%20Fund_2pager_2025_FIN.pdf"),
    ("350868188", "University of Notre Dame", "https://plannedgiving.nd.edu/gift-options/how-to-give/donor-advised-fund/"),
    ("020222111", "Dartmouth College", "https://giftplanning.dartmouth.edu/node/14"),
    ("952250801", "UCLA Foundation", "https://legacy.ucla.edu/org_files/776/pdf/gift_pdf/Donor%20Advised%20Fund.pdf"),
    ("160743209", "University of Rochester", "https://rochester.giftplans.org/what-to-give/donor-advised-fund"),
    ("160743209", "University of Rochester", "https://rochester.edu/giving/wilson-society/wp-content/uploads/2024/01/GP-2073_DAF_SlipSheet_R2-2.pdf"),
    ("222848738", "Cornell University Foundation", "https://giving.cornell.edu/make-a-grant/"),
    ("222848738", "Cornell University Foundation", "https://giving.cornell.edu/download/2558/"),
    ("", "University of Minnesota Foundation", "https://give.umn.edu/giving/donor-advised-funds"),
    ("", "Michigan State University", "https://spartan.msu.edu/spartan-story-hub/news/2022/11/donor-advised-fund-offers-new-options-for-giving"),
    ("", "University of North Dakota Alumni Association and Foundation", "https://alumni.und.edu/gift-planning/donor-advised-funds.html"),
    ("050258809", "Brown University", "https://policy.brown.edu/policy/donor-advised-funds"),
    ("231352685", "University of Pennsylvania (Penn Medicine)", "https://www.med.upenn.edu/pennmedplannedgiving/penn-donor-advised-fund.html"),
    ("042103580", "Harvard University", "https://alumni.harvard.edu/giving/gift-planning/DAF"),
    ("042103594", "Massachusetts Institute of Technology", "https://giving.mit.edu/donor-advised-funds"),
    ("386006309", "University of Michigan", "https://giving.umich.edu/um/donor-advised-fund"),
    ("416011702", "Mayo Clinic", "https://plannedgiving.mayoclinic.org/donor-advised-funds"),
    ("363245072", "The Rotary Foundation", "https://www.rotary.org/en/donate/donor-advised-fund"),
    ("", "Indiana University Foundation", "https://iufoundation.iu.edu/ways-give/planned-giving/plan-a-future-gift/donor-advised-funds.html"),
)
RX_RULE = re.compile(r"\b\d{1,3}\s?(%|percent)|\bhalf\b|one-quarter|one quarter|\bquarter\b|\bminimum\b|at least|"
                     r"must be (?:designated|directed|distributed|granted)|retained fund|outside charit|other charit", re.I)

# Host rule read from each page's extracted sentences (filled after reading; quoted verbatim in the research note).
READINGS: dict = {
    "https://assets.stanford.edu/a/f/78141/x/889a0f5be4/wp_daf_02252025.pdf": {
        "rule": "contribution share reserved for host, falling with gift size", "min_share": "50% (<$10m); 40% ($10m+); 30% ($20m+)",
        "quote": "Half of the gift amount must be designated to Stanford. The other half may be used to support other approved charities. "
                 "(Note that for gifts of $10 million or more, Stanford requires that only 40 percent come to the university; for a gift of "
                 "$20 million or more, only 30 percent must be reserved for Stanford.)",
        "date": "2025-02-25 (file name wp_daf_02252025)", "note": "minimum gift $1 million"},
    "https://giftplanning.columbia.edu/what-you-can-give/donor-advised-fund": {
        "rule": "share of distributions to host", "min_share": "50%",
        "quote": "Flexible: at least 50% goes to Columbia, and the rest may be distributed to other eligible nonprofit organizations.",
        "date": "page (c) 2026", "note": "Minimum gift level: $1 million; also 'Generally, half of these distributions must remain at Columbia'"},
    "https://plannedgiving.yale.edu/what-you-can-give/donor-advised-fund": {
        "rule": "share of fund to host", "min_share": "50%",
        "quote": "At least 50% of your fund may be designated for Yale use, and the rest may be made to qualified public charities that you recommend.",
        "date": "page (c) 2026", "note": "wording 'may be designated'; the 2025 two-pager says 'must'"},
    "https://plannedgiving.yale.edu/sites/yale/files/2025-09/Donor%20Advised%20Fund_2pager_2025_FIN.pdf": {
        "rule": "share of gifts and growth to host", "min_share": "50%",
        "quote": "At least 50 percent of the gifts donated to the fund and any appreciation or income attributed to those amounts must be "
                 "designated for purposes at Yale.",
        "date": "2025-09 (upload path)", "note": "two-column PDF; sentence reassembled from columns; minimum initial gift $5 million"},
    "https://legacy.ucla.edu/org_files/776/pdf/gift_pdf/Donor%20Advised%20Fund.pdf": {
        "rule": "share of distributions to host + 5% annual payout", "min_share": "50%",
        "quote": "At least 50% of the distributions should be directed to any area of UCLA.",
        "date": "undated PDF, live 2026-11-20", "note": "minimum to create $250,000; 'The total annual distribution amount should be at least 5% of the fund's market value.'; two-column PDF, sentence reassembled"},
    "https://rochester.giftplans.org/what-to-give/donor-advised-fund": {
        "rule": "vested share for host, tiered by starting gift", "min_share": "100% ($100k-$199,999); 50% ($200k-$499,999); 25% ($500k-$999,999); 0% ($1m+)",
        "quote": "$100,000 - $199,999 100% Must be vested . $200,000 - $499,999 50% Must be vested . $500,000 - $999,999 25% Must be vested . "
                 "$1,000,000 + 0% No vesting requirement",
        "date": "undated page, live 2026-11-20", "note": "table text as extracted"},
    "https://rochester.edu/giving/wilson-society/wp-content/uploads/2024/01/GP-2073_DAF_SlipSheet_R2-2.pdf": {
        "rule": "vested share for host, tiered by starting gift", "min_share": "100%/50%/25%/0% by starting gift",
        "quote": "The University manages its DAFs and in exchange, a certain percentage of a DAF must be vested, (allocated or reserved) for "
                 "charitable purposes within the University of Rochester.",
        "date": "2024-01 (upload path)", "note": "same tiers as the giftplans page"},
    "https://giving.cornell.edu/make-a-grant/": {
        "rule": "none stated on grant form", "min_share": None,
        "quote": "Grants must be made to organizations that are tax-exempt under both I.R.C. Section 501 (c)(3) and public charities under Code Section 509 (a).",
        "date": "undated form, live 2026-11-20", "note": "account-holder grant form"},
    "https://giving.cornell.edu/download/2558/": {
        "rule": "share of contributions to host, tiered by account size", "min_share": "50% (<$500k); 25% (>$500k); none (>$1m)",
        "quote": "For accounts under $500,000, 50% or more of the funds contributed must eventually be allocated to Cornell. For accounts greater "
                 "than $500,000, 25% must be allocated to Cornell. ... For accounts greater than $1,000,000, there is no minimum Cornell allocation.",
        "date": "undated PDF, live 2026-11-20", "note": "two-column PDF; sentences reassembled from columns; minimum initial gift $100,000"},
    "https://give.umn.edu/giving/donor-advised-funds": {
        "rule": "none (general DAF explainer, no in-house programme terms on page)", "min_share": None, "quote": "",
        "date": "", "note": ""},
    "https://spartan.msu.edu/spartan-story-hub/news/2022/11/donor-advised-fund-offers-new-options-for-giving": {
        "rule": "split account: half restricted to host", "min_share": "50%",
        "quote": "Fifty percent is allocated into the MSU Only account, and 50 percent is allocated into the Discretionary account.",
        "date": "2022-11 (article path)", "note": "programme run with BNY Mellon; BNY Mellon CGF terminated Dec 2024 (repo league-table note), current status not checked"},
    "https://alumni.und.edu/gift-planning/donor-advised-funds.html": {
        "rule": "share of annual distributions to host", "min_share": "51%",
        "quote": "51 % . minimum of total annual grant distributions to UND", "date": "page (c) 2026",
        "note": "infographic text as extracted; $100k minimum to establish"},
    "https://policy.brown.edu/policy/donor-advised-funds": {
        "rule": "irrevocable host portion of every contribution", "min_share": "25%",
        "quote": "Allocation Requirement: One-quarter of the initial contribution and one-quarter of each addition made to the Fund and of any "
                 "income and appreciation thereon, will be irrevocably donated and allocated to the Brown Portion.",
        "date": "Effective Date: September 7, 2023 (earlier version December 15, 2021)", "note": "minimum initial contribution $100,000"},
    "https://www.med.upenn.edu/pennmedplannedgiving/penn-donor-advised-fund.html": {
        "rule": "share of gift to host over time + 5% annual payout", "min_share": "50%",
        "quote": "At least 50% of the gift must be designated over time to University programs, with the remaining balance available to other charitable organizations.",
        "date": "undated page, live 2026-11-20", "note": "'At least 5% of the DAF must be distributed annually.'"},
    "https://alumni.harvard.edu/giving/gift-planning/DAF": {
        "rule": "share of distributions to host", "min_share": "50%",
        "quote": "(at least half of your distributions must be designated for Harvard)", "date": "page (c) 2026", "note": ""},
    "https://plannedgiving.mayoclinic.org/donor-advised-funds": {
        "rule": "fixed split host / other", "min_share": "60%",
        "quote": "Advisory privileges Yes: Mayo Clinic receives 60% and other charities receive up to 40%",
        "date": "page (c) 2026", "note": "comparison-table cell; initial gift at least $100,000"},
    "https://iufoundation.iu.edu/ways-give/planned-giving/plan-a-future-gift/donor-advised-funds.html": {
        "rule": "none (page about giving from external DAFs)", "min_share": None, "quote": "", "date": "", "note": ""},
    "https://giftplanning.dartmouth.edu/node/14": {
        "rule": "not found: URL now serves the general planned-giving page", "min_share": None, "quote": "", "date": "page (c) 2026",
        "note": "search snippet for this URL named a Dartmouth DAF; the live page carries no DAF terms"},
}


# ----------------------------------------------------------------------------- panel (pure)
def t4_class(ident: Mapping, ntee_major: str) -> str:
    st, m = ident.get("subtype", ""), (ntee_major or "")[:1]
    if st == "Universities and Healthcare" or (st == "Other" and m in ("B", "E", "F", "G", "H")):
        return "institution_edu_health"
    if st == "Religiously-Affiliated":
        return "religious"
    if st == "Other":
        return {"T": "intermediary_t", "": "unclassified"}.get(m, "mission_other")
    return "t4_other_subtype"


def label(e: str, ids: Mapping, rank: Mapping, ntee: Mapping) -> dict:
    i = ids.get(e, {"name": "", "type": "", "subtype": ""})
    tier = tier_of(e, segment_of(i["type"], i["subtype"]), rank)
    return {"tier": tier, "t4_class": t4_class(i, ntee.get(e, "")) if tier == "T4_single_issue" else ""}


def seg_keys(lab: Mapping) -> tuple[str, ...]:
    return (lab["tier"], "ALL") + ((f"T4:{lab['t4_class']}",) if lab["t4_class"] else ())


def segment_rows(corr: Mapping, labels: Mapping, totals: Mapping) -> tuple[dict, ...]:
    def agg(fy, seg):
        ks = tuple(k for k in corr if k[1] == fy and seg in seg_keys(labels[k[0]]))
        prev = tuple(k for k in corr if k[1] == fy - 1 and seg in seg_keys(labels[k[0]]))
        s = {m: sum(corr[k][m] for k in ks) for m in METRICS}
        pos = tuple(corr[k]["daf_assets_eoy"] for k in ks if corr[k]["daf_assets_eoy"] > 0)
        prev_assets = sum(corr[k]["daf_assets_eoy"] for k in prev)
        return {"row_type": "segment_year", "fiscal_year": fy, "segment": seg, "n_sponsor_rows": len(ks),
                "n_positive_assets": len(pos), **{m: round(s[m]) for m in METRICS},
                **{f"share_{m}": (s[m] / totals[(fy, m)]) if totals.get((fy, m)) else None for m in METRICS},
                "median_sponsor_assets": round(median(pos)) if pos else None,
                "grants_over_prior_year_assets": (s["daf_grants"] / prev_assets) if prev_assets else None,
                "source": SRC_PANEL}
    segs = sorted({s for lab in labels.values() for s in seg_keys(lab)})
    return tuple(agg(fy, seg) for fy in FYS for seg in segs)


def check_totals(rows: Sequence[Mapping], totals: Mapping) -> dict:
    alls = {(r["fiscal_year"], m): r[m] for r in rows if r["segment"] == "ALL" for m in METRICS}
    tiers = {(fy, m): sum(r[m] for r in rows if r["fiscal_year"] == fy and r["segment"].startswith("T") and ":" not in r["segment"])
             for fy in FYS for m in METRICS}
    return {f"{fy}:{m}": {"all": alls[(fy, m)], "tiers": tiers[(fy, m)], "corrected_total": round(totals[(fy, m)]),
                          "diff": round(alls[(fy, m)] - totals[(fy, m)])} for fy in FYS for m in METRICS}


def sponsor_rows(corr: Mapping, labels: Mapping, ids: Mapping, ntee_code: Mapping) -> tuple[dict, ...]:
    eins = sorted({e for e, fy in corr if labels[e]["t4_class"] in ("institution_edu_health", "mission_other") and fy in FYS})
    def one(e):
        v = {fy: corr.get((e, fy)) for fy in FYS}
        return {"row_type": "sponsor", "ein": e, "name": ids[e]["name"], "segment": f"T4:{labels[e]['t4_class']}",
                "dafrc_subtype": ids[e]["subtype"], "bmf_ntee": ntee_code.get(e, ""),
                **{f"{m}_fy{fy}": (round(v[fy][m]) if v[fy] else None) for fy in FYS for m in METRICS},
                "corrections_fy2021_24": ";".join(sorted({v[fy]["rules"] for fy in FYS if v[fy] and v[fy]["rules"]})),
                "source": SRC_PANEL}
    rows = tuple(one(e) for e in eins)
    return tuple(r for r in rows if any((r[f"daf_assets_eoy_fy{fy}"] or 0) != 0 or (r[f"daf_grants_fy{fy}"] or 0) != 0 for fy in FYS))


def sample_eins(corr: Mapping, labels: Mapping) -> tuple[str, ...]:
    def top(cls, n):
        xs = sorted(((corr[(e, 2024)]["daf_assets_eoy"], e) for e, fy in corr if fy == 2024 and labels[e]["t4_class"] == cls),
                    reverse=True)
        return tuple(e for _, e in xs[:n])
    return top("institution_edu_health", N_INST) + top("mission_other", N_MISSION)


# ----------------------------------------------------------------------------- XML (pure parse of a tree)
def _loc(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _first(el, name: str):
    return next((c for c in el.iter() if _loc(c.tag) == name), None) if el is not None else None


def _txt(el, name: str) -> str:
    c = _first(el, name)
    return (c.text or "").strip() if c is not None else ""


def parse_return(root) -> dict:
    filer = _first(root, "Filer")
    sr = _first(root, "IRS990ScheduleR")
    related = frozenset(e for e in (_txt(g, "EIN") for g in (sr if sr is not None else ())) if e)
    lines = tuple({"ein": _txt(r, "RecipientEIN"), "name": " ".join(filter(None, (_txt(r, "BusinessNameLine1Txt"), _txt(r, "BusinessNameLine2Txt")))),
                   "purpose": _txt(r, "PurposeOfGrantTxt"),
                   "amt": (num(_txt(r, "CashGrantAmt")) or 0.0) + (num(_txt(r, "NonCashAssistanceAmt")) or 0.0)}
                  for r in root.iter() if _loc(r.tag) == "RecipientTable")
    return {"filer_ein": _txt(filer, "EIN"), "filer_name": " ".join(filter(None, (_txt(filer, "BusinessNameLine1Txt"), _txt(filer, "BusinessNameLine2Txt")))),
            "tax_period_end": _txt(root, "TaxPeriodEndDt"),
            "daf_count": num(_txt(root, "DonorAdvisedFundsHeldCnt")), "daf_contrib": num(_txt(root, "DonorAdvisedFundsContriAmt")),
            "daf_grants": num(_txt(root, "DonorAdvisedFundsGrantsAmt")), "daf_eoy": num(_txt(root, "DonorAdvisedFundsVlEOYAmt")),
            "ix_l1": num(_txt(_first(root, "GrantsToDomesticOrgsGrp"), "TotalAmt")),
            "ix_l3": num(_txt(_first(root, "ForeignGrantsGrp"), "TotalAmt")),
            "related_eins": sorted(related), "lines": lines}


def classify_line(g: Mapping, filer: str, host_eins: frozenset) -> str:
    if g["ein"] and (g["ein"] == filer or g["ein"] in host_eins):
        return "host"
    if RX_DAF.search(g["purpose"]):
        return "daf_labelled"
    if RX_RESEARCH.search(g["purpose"]):
        return "research"
    return "other"


def host_metrics(p: Mapping, sponsor_ein: str) -> dict:
    host_eins = frozenset(p["related_eins"]) | HOST_EXTRA.get(sponsor_ein, frozenset())
    cls = tuple((classify_line(g, p["filer_ein"], host_eins), g["amt"]) for g in p["lines"])
    s = reduce(lambda a, x: {**a, x[0]: a.get(x[0], 0.0) + x[1]}, cls, {})
    n = reduce(lambda a, x: {**a, x[0]: a.get(x[0], 0) + 1}, cls, {})
    itot = sum(a for _, a in cls)
    l1 = p["ix_l1"] if p["ix_l1"] is not None else itot
    l3 = p["ix_l3"] or 0.0
    small = max(0.0, l1 - itot)
    d = p["daf_grants"]
    sep = sponsor_ein in SEPARATE_FOUNDATION
    base = {"structure": "separate_foundation" if sep else "sponsor_is_host", "sched_i_lines": len(cls),
            "sched_i_total": round(itot), **{f"i_{k}": round(s.get(k, 0.0)) for k in ("host", "daf_labelled", "research", "other")},
            **{f"n_{k}": n.get(k, 0) for k in ("host", "daf_labelled", "research", "other")},
            "unitemised_domestic": round(small), "foreign_grants_ix_l3": round(l3), "ix_l1": round(l1),
            "n_related_orgs": len(p["related_eins"])}
    if not d or d <= 0:
        return {**base, "host_share_min": None, "host_share_max": None, "host_share_point": None,
                "daf_dominant": None, "note": "Schedule D DAF grants zero, blank or negative: no host share"}
    ext_min = min(d, s.get("daf_labelled", 0.0))
    ext_max = min(d, s.get("daf_labelled", 0.0) + s.get("other", 0.0) + small + l3)
    hmax = 1 - ext_min / d
    hmax = min(hmax, s.get("host", 0.0) / d) if sep else hmax
    hmin = min(max(0.0, 1 - ext_max / d), hmax)
    dom = d >= 0.9 * (l1 + l3) if (l1 + l3) > 0 else False
    point = hmin if dom else None   # if (nearly) all grants are DAF grants, the lower bound is the estimate
    return {**base, "host_share_min": round(hmin, 4), "host_share_max": round(hmax, 4),
            "host_share_point": round(point, 4) if point is not None else None, "daf_dominant": int(dom), "note": ""}


def sample_rows(targets: Sequence[Mapping], parsed: Mapping, labels: Mapping, ids: Mapping) -> tuple[dict, ...]:
    def one(t):
        p = parsed.get(t["oid"])
        if not p:
            return {"row_type": "schedule_i_sample", "ein": t["ein"], "name": ids[t["ein"]]["name"], "fiscal_year": t["fy"],
                    "return_object_id": t["oid"], "note": "XML not available", "source": SRC_XML}
        hm = host_metrics(p, t["ein"])
        return {"row_type": "schedule_i_sample", "ein": t["ein"], "name": p["filer_name"] or ids[t["ein"]]["name"],
                "segment": f"T4:{labels[t['ein']]['t4_class']}", "fiscal_year": t["fy"], "tax_period_end": p["tax_period_end"],
                "return_object_id": t["oid"], "sched_d_daf_grants": p["daf_grants"], "sched_d_daf_eoy": p["daf_eoy"],
                "sched_d_daf_contributions": p["daf_contrib"], "sched_d_daf_count": p["daf_count"], **hm,
                "url": XML_URL.format(oid=t["oid"]), "source": SRC_XML}
    return tuple(one(t) for t in targets)


def sample_summary(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    def agg(fy, seg):
        rs = tuple(r for r in rows if r.get("fiscal_year") == fy and (seg == "ALL" or r.get("segment") == seg)
                   and r.get("host_share_min") is not None)
        d = sum(r["sched_d_daf_grants"] for r in rs)
        return {"row_type": "schedule_i_summary", "fiscal_year": fy, "segment": seg, "n_returns": len(rs),
                "sched_d_daf_grants": round(d),
                "host_share_min": (sum(r["host_share_min"] * r["sched_d_daf_grants"] for r in rs) / d) if d else None,
                "host_share_max": (sum(r["host_share_max"] * r["sched_d_daf_grants"] for r in rs) / d) if d else None,
                "i_daf_labelled": sum(r["i_daf_labelled"] for r in rs), "source": SRC_XML}
    return tuple(agg(fy, seg) for fy in SAMPLE_FYS for seg in ("ALL", "T4:institution_edu_health", "T4:mission_other"))


# ----------------------------------------------------------------------------- off-panel filers (pure)
RX_INST_NAME = re.compile(r"UNIV|COLLEGE|HOSPITAL|HEALTH|MEDICAL|CLINIC|SCHOOL|ACADEMY", re.I)


def off_panel_rows(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    def one(fy):
        rs = tuple(r for r in rows if r["fiscal_year"] == str(fy) and r["status"] == "reports_daf_value" and RX_INST_NAME.search(r["name"]))
        return {"row_type": "off_panel_inst_filers", "fiscal_year": fy, "segment": "non-DAFRC filers, education/health name",
                "n_sponsor_rows": len(rs), "daf_assets_eoy": round(sum(num(r["sched_d_daf_eoy_value"]) or 0 for r in rs)),
                "daf_contributions": round(sum(num(r["sched_d_daf_contributions"]) or 0 for r in rs)),
                "daf_grants": round(sum(num(r["sched_d_daf_grants"]) or 0 for r in rs)),
                "source": "data/mission-2026-11-14/non-dafrc-daf-filers-990.csv (status reports_daf_value; name regex)"}
    return tuple(one(fy) for fy in FYS)


# ----------------------------------------------------------------------------- policy pages
def robots_verdict(text: str | None, status: int, url: str) -> tuple[bool, str]:
    if status == 404:
        return True, "robots.txt 404: no rules"
    if status != 200 or text is None:
        return False, f"robots.txt {status}: treated as disallowed"
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(text.splitlines())
    bad = tuple(a for a in AI_AGENTS + (UA, "*") if not rp.can_fetch(a, url))
    return (not bad, "robots.txt 200: allowed for " + ", ".join(AI_AGENTS + (UA, "*")) if not bad
            else "robots.txt 200: disallowed for " + ", ".join(bad))


def html_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|li|h\d|div|tr)>", ". ", raw)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).strip()


def rule_sentences(text: str, cap: int = 8) -> tuple[str, ...]:
    sents = re.split(r"(?<=[.;!?])\s+|\s•\s|\s•\s", text)
    hits = tuple(dict.fromkeys(s.strip() for s in sents if RX_RULE.search(s) and 25 <= len(s.strip()) <= 600))
    return hits[:cap]


def http_get(url: str, timeout: int = 40) -> tuple[int, bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, b"", ""
    except Exception as e:  # noqa: BLE001 - network edge: record and move on
        return -1, str(e).encode(), ""


def pdf_text(data: bytes, tmp: str) -> str | None:
    if not shutil.which("pdftotext"):
        return None
    with open(tmp, "wb") as fh:
        fh.write(data)
    out = subprocess.run(["pdftotext", "-layout", tmp, "-"], capture_output=True, timeout=60)
    return re.sub(r"\s+", " ", out.stdout.decode("utf-8", "replace")).strip()


def fetch_pages(pages: Sequence[tuple], cache: str, fetch: bool) -> dict:
    path = os.path.join(cache, "policy_pages.json")
    old = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    if not fetch:
        return old
    raw = {h: (lambda st, b, _: (st, b.decode("utf-8", "replace") if st == 200 else None))(*http_get(f"https://{h}/robots.txt"))
           for h in sorted({urlparse(u).netloc for _, _, u in pages})}

    def one(u):
        st, txt = raw[urlparse(u).netloc]
        ok, why = robots_verdict(txt, st, u)
        if not ok:
            return {"robots": why, "http_status": None, "text_chars": 0, "sentences": []}
        s, data, ctype = http_get(u)
        is_pdf = data[:4] == b"%PDF" or "pdf" in ctype
        text = (pdf_text(data, os.path.join(cache, "tmp.pdf")) if is_pdf else html_text(data.decode("utf-8", "replace"))) if s == 200 else ""
        return {"robots": why, "http_status": s, "content_type": ctype, "pdf": is_pdf, "text_chars": len(text or ""),
                "text": (text or "")[:60000], "sentences": list(rule_sentences(text or ""))}
    new = {u: one(u) for _, _, u in pages}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(new, fh, indent=1)
    return new


def policy_rows(pages: Sequence[tuple], fetched: Mapping) -> tuple[dict, ...]:
    def one(p):
        ein, name, u = p
        f = fetched.get(u, {})
        r = READINGS.get(u, {})
        return {"row_type": "policy_page", "ein": ein, "name": name, "url": u, "robots_status": f.get("robots", "not checked"),
                "http_status": f.get("http_status"), "text_chars": f.get("text_chars"),
                "extracted_sentences": " || ".join(f.get("sentences", [])[:6]),
                "host_rule": r.get("rule", ""), "min_share_to_host": r.get("min_share"), "quote": r.get("quote", ""),
                "page_date": r.get("date", ""), "note": r.get("note", ""), "source": u}
    return tuple(one(p) for p in pages)


# ----------------------------------------------------------------------------- edges
def load_xml(oids: Iterable[str], cache: str, fetch: bool) -> dict:
    d = os.path.join(cache, "xml")
    os.makedirs(d, exist_ok=True)
    def one(o):
        p = os.path.join(d, f"{o}.xml")
        if not os.path.exists(p) and fetch:
            s, data, _ = http_get(XML_URL.format(oid=o), timeout=120)
            if s == 200:
                with open(p, "wb") as fh:
                    fh.write(data)
        return (o, parse_return(ET.parse(p).getroot())) if os.path.exists(p) else (o, None)
    return {o: p for o, p in map(one, oids) if p}


FIELDS = ("row_type", "fiscal_year", "segment", "ein", "name", "dafrc_subtype", "bmf_ntee", "n_sponsor_rows",
          "n_positive_assets", *METRICS, *(f"share_{m}" for m in METRICS), "median_sponsor_assets",
          "grants_over_prior_year_assets",
          *(f"{m}_fy{fy}" for fy in FYS for m in METRICS), "corrections_fy2021_24",
          "tax_period_end", "return_object_id", "sched_d_daf_grants", "sched_d_daf_eoy", "sched_d_daf_contributions",
          "sched_d_daf_count", "structure", "sched_i_lines", "sched_i_total", "i_host", "i_daf_labelled", "i_research",
          "i_other", "n_host", "n_daf_labelled", "n_research", "n_other", "unitemised_domestic", "foreign_grants_ix_l3",
          "ix_l1", "n_related_orgs", "daf_dominant", "host_share_min", "host_share_max", "host_share_point", "n_returns",
          "url", "robots_status", "http_status", "text_chars", "extracted_sentences", "host_rule", "min_share_to_host",
          "quote", "page_date", "note", "source")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    data = os.path.join(a.root, "data", "mission-2026-11-14")
    os.makedirs(a.cache, exist_ok=True)
    dafrc = read_csv(DAFRC_CSV)
    items = read_csv(os.path.join(data, "dafrc-corrections-itemized.csv"))
    corr = {k: v for k, v in corrected(dafrc, items).items() if k[1] in (2020,) + FYS}
    ids = identity(dafrc, items)
    lt = read_csv(os.path.join(data, "daf-long-tail-sponsors-fy2021-2024.csv"))
    ntee = {ein9(r["ein"]): r["ntee_major"] for r in lt}
    ntee_code = {ein9(r["ein"]): r["bmf_ntee"] for r in lt}
    league = read_csv(os.path.join(data, "daf-sponsor-league-table-fy2021-2025.csv"))
    rank = {r["ein"]: int(r["rank_assets"]) for r in league if r["fiscal_year"] == "2024" and r["row_type"] == "top50"}
    totals = {(int(r["fiscal_year"]), r["metric"]): float(r["corrected_value"])
              for r in read_csv(os.path.join(data, "dafrc-corrected-market-totals.csv"))}
    labels = {e: label(e, ids, rank, ntee) for e, _ in corr}

    seg = segment_rows(corr, labels, totals)
    chk = check_totals(seg, totals)
    spon = sponsor_rows(corr, labels, ids, ntee_code)
    eins = sample_eins(corr, labels)
    harvest = read_csv(os.path.join(data, "form990-returns-schedule-d-harvest-full.csv"))
    hk = {(r["ein"], int(r["fiscal_year"])): r["return_object_id"] for r in harvest if r["xml_status"] == "ok"}
    targets = tuple({"ein": e, "fy": fy, "oid": hk[(e, fy)]} for e in eins for fy in SAMPLE_FYS if (e, fy) in hk)
    parsed = load_xml((t["oid"] for t in targets), a.cache, a.fetch)
    samp = sample_rows(targets, parsed, labels, ids)
    summ = sample_summary(samp)
    off = off_panel_rows(read_csv(os.path.join(data, "non-dafrc-daf-filers-990.csv")))
    pages = fetch_pages(POLICY_PAGES, a.cache, a.fetch)
    pol = policy_rows(POLICY_PAGES, pages)

    write_csv(os.path.join(data, OUT_CSV), seg + off + spon + samp + summ + pol, FIELDS)
    with open(os.path.join(a.cache, "check_totals.json"), "w", encoding="utf-8") as fh:
        json.dump(chk, fh, indent=1)
    bad = {k: v for k, v in chk.items() if abs(v["diff"]) > 1 or abs(v["tiers"] - v["corrected_total"]) > 1}
    print(json.dumps({"rows": {"segment_year": len(seg), "off_panel": len(off), "sponsor": len(spon), "sample": len(samp),
                               "summary": len(summ), "policy": len(pol)},
                      "sample_eins": list(eins), "totals_check_failures": bad}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
