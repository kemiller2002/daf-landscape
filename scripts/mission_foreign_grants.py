#!/usr/bin/env python3
"""Foreign grants of the top-50 DAF sponsors from Form 990 Schedule F, FY2023-FY2024 (queue item P-NEW-FGN-01).

Universe and return choice are those of scripts/mission_recipient_sectors.py: top-50 DAFRC sponsors by FY2024 DAF
assets; one return per sponsor x fiscal year via mission_daf_to_daf.pick_returns over the netpayout990/ cache
(fiscal year = calendar year in which the tax period ends; 100 sponsor-years, incl. the six attachment-only
Schedule I sponsor-years, because Schedule F is filed separately from Schedule I).

Steps (pure transforms; I/O at the edges)
  1. Extract   per return, streamed: ReturnHeader; Form 990 Part IX lines 1-3 (grants to domestic orgs, domestic
               individuals, foreign orgs/governments/individuals) and Part IV lines 14a/14b/15/16; Schedule F
               Part I (activities by region; line 1 grant-records indicator), Part II (grants to foreign orgs:
               region, purpose, cash, manner of disbursement, non-cash; line 2 counts of 501(c)(3)-equivalent and
               other recipients), Part III (grants to foreign individuals), Part IV (foreign-entity questions) and
               Part V text. Parsing stops at the first schedule after F, so Schedule I is not downloaded again.
               Local XML copies are used when present; otherwise the GivingTuesday mirror of IRS TEOS is streamed.
  2. Normalise region (the 10 Schedule F regions; country names mapped by a fixed table), manner of disbursement,
               and purpose (keyword buckets, first match wins; raw text kept for a top-purposes table).
  3. Part V    keyword flags: equivalency determination, expenditure responsibility, NGOsource, intermediary.
  4. Route     Schedule I Part II lines (line cache of mission_recipient_sectors.py) to (a) named US cross-border
               intermediaries (fixed EIN list, from the IRS EO BMF), (b) "American/US friends of" names, (c) any
               recipient with NTEE major group Q (international). Each named intermediary's own FY2023-24 returns
               give its foreign-grant share (Part IX line 3 / lines 1-3); inbound x share = estimated pass-through.
  5. Aggregate by scope (all, ex university/hospital, segment, sponsor) x FY (2023, 2024, pooled).

Stdlib only; functional style.

Usage:
  python3 scripts/mission_foreign_grants.py --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF --irs-dir IRS \
      --extract-cache EC [--xml-list FILE] [--fetch] [--workers 6]
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import SVCF, WHITELIST, annotate, load_bmf  # noqa: E402

OUT = os.path.join(DATA, "daf-foreign-grants-schedule-f-2023-2024.csv")
COST = os.path.join(DATA, "sponsor-cost-structure.csv")
EXTRACT_V = 2
SOURCE = ("IRS Form 990 Part IX lines 1-3, Part IV lines 14-16 and Schedule F Parts I-V (e-file XML, GivingTuesday "
          "mirror of IRS TEOS); Schedule I Part II lines from mission_recipient_sectors.py line cache; recipients joined "
          "to IRS EO BMF NTEE_CD; universe per mission_daf_to_daf.py")

# US-registered cross-border re-granting intermediaries (EIN and name as in the IRS EO BMF, 2026-11 snapshot).
INTERMEDIARIES = {
    "431634280": "Charities Aid Foundation America (CAF America)",
    "300108263": "GlobalGiving Foundation",
    "943373670": "Give2Asia",
    "582277856": "Myriad USA (formerly King Baudouin Foundation US)",
    "561834887": "Global Fund for Children",
    "133966503": "Friends of Fondation de France",
    "136161189": "British Schools and Universities Foundation",
    "770155782": "Global Fund for Women",
    "841612422": "Global Greengrants Fund",
}
FRIENDS = re.compile(r"\b(AMERICAN|AMERICANS|US|U S|USA|UNITED STATES|CANADIAN AMERICAN) FRIENDS OF\b|"
                     r"\bAMERICAN (COMMITTEE|ASSOCIATES) (FOR|OF) THE\b|\bFRIENDS OF .*\b(ISRAEL|"
                     r"JERUSALEM|YESHIVA|UNIVERSITY OF OXFORD|CAMBRIDGE|INDIA|AFRICA|HAITI|UKRAINE|IRELAND|MEXICO)\b")

REGIONS = ("Antarctica", "Central America and the Caribbean", "East Asia and the Pacific",
           "Europe (Including Iceland and Greenland)", "Middle East and North Africa", "North America",
           "Russia and the Newly Independent States", "South America", "South Asia", "Sub-Saharan Africa")
# Stage 1: region names (variants seen in filings), applied to the text before any " - " country list.
REGION_NAME_RULES = (
    ("South Asia", r"SOUTH ASIA"),
    ("East Asia and the Pacific", r"EAST ASIA|PACIFIC|OCEANIA"),
    ("Middle East and North Africa", r"MIDDLE[- ]?EAST|NORTH AFRICA"),
    ("Sub-Saharan Africa", r"SUB-?\s?SAHARAN"),
    ("Russia and the Newly Independent States", r"RUSSIA|NEWLY INDEPENDENT|NEIGHBORING STATES"),
    ("North America", r"NORTH AMERICA|CANADA AND MEXICO|CANADA & MEXICO"),
    ("Latin America (unspecified)", r"LATIN AMERICA"),
    ("Central America and the Caribbean", r"CENTRAL AMERICA|CARIBBEAN"),
    ("South America", r"SOUTH AMERICA"),
    ("Europe (Including Iceland and Greenland)", r"EUROPE"),
    ("Antarctica", r"ANTARCTICA"),
    ("Africa (unspecified)", r"^AFRICA$"),
    ("Asia (unspecified)", r"^ASIA$"),
)
# Stage 2: single-country texts.
REGION_RULES = (
    ("Central America and the Caribbean", r"MEXICO|GUATEMALA|HONDURAS|HAITI|DOMINICAN|NICARAGUA|COSTA RICA|PANAMA|"
                                          r"EL SALVADOR|JAMAICA|BELIZE|BAHAMAS|CUBA"),
    ("East Asia and the Pacific", r"CHINA|JAPAN|KOREA|AUSTRALIA|NEW ZEALAND|PHILIPPINES|VIETNAM|INDONESIA|THAILAND|"
                                  r"TAIWAN|HONG KONG|SINGAPORE|CAMBODIA|MALAYSIA|MYANMAR"),
    ("Europe (Including Iceland and Greenland)", r"UNITED KINGDOM|ENGLAND|SCOTLAND|IRELAND|FRANCE|GERMANY|ITALY|SPAIN|"
                                                 r"SWITZERLAND|NETHERLANDS|BELGIUM|POLAND|SWEDEN|NORWAY|DENMARK|"
                                                 r"AUSTRIA|GREECE|PORTUGAL|CZECH|HUNGARY"),
    ("Middle East and North Africa", r"ISRAEL|JORDAN|LEBANON|EGYPT|MOROCCO|TURKEY|PALESTIN|GAZA|WEST BANK|SYRIA|IRAQ|"
                                     r"IRAN|YEMEN|TUNISIA|SAUDI|EMIRATES"),
    ("Russia and the Newly Independent States", r"UKRAINE|GEORGIA|ARMENIA|MOLDOVA|BELARUS|KAZAKH|UZBEK|KYRGYZ|"
                                                r"AZERBAIJAN|TAJIK"),
    ("Sub-Saharan Africa", r"KENYA|UGANDA|NIGERIA|GHANA|ETHIOPIA|TANZANIA|RWANDA|MALAWI|ZAMBIA|ZIMBABWE|SOUTH AFRICA|"
                           r"SENEGAL|LIBERIA|SIERRA LEONE|CONGO|MOZAMBIQUE|BURUNDI"),
    ("South America", r"BRAZIL|ARGENTINA|CHILE|PERU|COLOMBIA|ECUADOR|BOLIVIA|VENEZUELA|URUGUAY|PARAGUAY"),
    ("South Asia", r"INDIA|PAKISTAN|BANGLADESH|NEPAL|SRI LANKA|AFGHANISTAN|BHUTAN"),
    ("North America", r"CANADA|BERMUDA"),
)
COMPILED_NAMES = tuple((g, re.compile(p)) for g, p in REGION_NAME_RULES)
COMPILED_REGIONS = tuple((g, re.compile(p)) for g, p in REGION_RULES)

PURPOSE_RULES = (
    ("relief_humanitarian", r"RELIEF|HUMANITARIAN|DISASTER|EMERGENC|REFUGEE|EARTHQUAKE|FLOOD|HURRICANE|WAR\b|CRISIS"),
    ("religion", r"RELIGIO|CHURCH|MINIST|MISSION|TORAH|YESHIV|SYNAGOGUE|JEWISH|CHRISTIAN|ISLAM|GOSPEL|PARISH|BIBLE"),
    ("education", r"EDUCAT|SCHOOL|SCHOLAR|UNIVERSIT|COLLEGE|STUDENT|ACADEM|LITERACY|TEACH"),
    ("health_medical", r"HEALTH|MEDIC|HOSPITAL|DISEASE|CANCER|CLINIC|MALARIA|NUTRITION|SURG"),
    ("environment_animals", r"ENVIRON|CLIMATE|CONSERV|WILDLIFE|ANIMAL|NATURE|FOREST|OCEAN|BIODIVERS|INDIGENOUS"),
    ("arts_culture", r"\bARTS?\b|CULTUR|MUSEUM|MUSIC|HERITAGE|THEAT"),
    ("development_poverty", r"POVERTY|DEVELOPMENT|LIVELIHOOD|WATER|HOUSING|FOOD|HUNGER|ECONOMIC|MICRO|ORPHAN|CHILD|"
                            r"WOMEN|GIRLS"),
    ("human_services_civic", r"HUMAN SERVICE|COMMUNITY|YOUTH|CIVIC|PUBLIC SAFETY|PUBLIC, SOCIETAL|PUBLIC SOCIETAL|SOCIETAL"),
    ("research_science", r"RESEARCH|SCIENC"),
    ("international_unspecified", r"^INTERNATIONAL"),
    ("general_support", r"GENERAL|UNRESTRICTED|OPERATING|CHARITABLE|EXEMPT PURPOSE|PROGRAM|SUPPORT|MISSION|ORGANIZATIONAL"),
)
COMPILED_PURPOSE = tuple((g, re.compile(p)) for g, p in PURPOSE_RULES)
ER_RX = re.compile(r"EXPENDITURE\s+RESPONSIBILITY|4945\s*\(\s*H\s*\)", re.I)
ED_RX = re.compile(r"EQUIVALEN(CY|T)\s+(DETERMINATION|OF\s+A\s+PUBLIC)|EQUIVALENCY|53\.4945-5\s*\(\s*A\s*\)\s*\(\s*5", re.I)
NGO_RX = re.compile(r"NGO\s?SOURCE", re.I)
INTERMED_RX = re.compile(r"INTERMEDIAR|CAF AMERICA|CHARITIES AID FOUNDATION|GLOBALGIVING|GIVE2ASIA|KING BAUDOUIN|"
                         r"MYRIAD", re.I)
SEGMENTS = ("national", "processor", "community_foundation", "single_issue", "university_hospital")
PART4_IND = ("ForeignOfficeInd", "ForeignActivitiesInd", "MoreThan5000KToOrgInd", "MoreThan5000KToIndividualsInd")
SCHEDF_IND = ("GrantRecordsMaintainedInd", "TransferToForeignCorpInd", "InterestInForeignTrustInd",
              "ForeignCorpOwnershipInd", "PassiveForeignInvestmestCoInd", "ForeignPartnershipInd", "BoycottCountriesInd")
LATER = re.compile(r"IRS990Schedule[G-Z]$")


# ----------------------------------------------------------------------------- extract (streamed)
def kids(el) -> dict:
    out = {}
    for c in el.iter():
        if c is el or c.text is None or not c.text.strip():
            continue
        k = local(c.tag)
        out[k] = (out[k] + " " + c.text.strip()) if k in out else c.text.strip()
    return out


def total_of(el, grp: str) -> float | None:
    g = next((c for c in el.iter() if local(c.tag) == grp), None)
    t = next((c for c in g if local(c.tag) == "TotalAmt"), None) if g is not None else None
    return num(t.text) if t is not None else None


def parse_return(stream) -> dict:
    head, ix, sf = {}, {}, {"present": False}
    groups = {"part1": [], "part2": [], "part3": [], "part5": []}
    gmap = {"AccountActivitiesOutsideUSGrp": "part1", "GrantsToOrgOutsideUSGrp": "part2",
            "ForeignIndividualsGrantsGrp": "part3", "SupplementalInformationDetail": "part5"}
    seen, in_f = set(), False
    for ev, el in ET.iterparse(stream, events=("start", "end")):
        tag = local(el.tag)
        if ev == "start":
            if LATER.match(tag):
                break
            if tag == "IRS990ScheduleF":
                in_f = True
            continue
        if tag == "ReturnHeader":
            k = kids(el)
            head = {"tax_period_end": k.get("TaxPeriodEndDt", ""), "filer_ein": ein9((k.get("EIN", "") or "").split(" ")[0]),
                    "return_type": k.get("ReturnTypeCd", "")}
            el.clear()
        elif tag == "IRS990":
            ix = {"l1": total_of(el, "GrantsToDomesticOrgsGrp"), "l2": total_of(el, "GrantsToDomesticIndividualsGrp"),
                  "l3": total_of(el, "ForeignGrantsGrp"), "l25": total_of(el, "TotalFunctionalExpensesGrp"),
                  **{t: next((c.text for c in el if local(c.tag) == t), "") for t in PART4_IND}}
            el.clear()
        elif in_f and tag in gmap:
            seen.add(tag)
            groups[gmap[tag]].append(kids(el))
            el.clear()
        elif tag == "IRS990ScheduleF":
            sf = {"present": True, **{local(c.tag): c.text.strip() for c in el if c.text and c.text.strip()}}
            in_f = False
            el.clear()
            break
        elif tag.startswith("IRS990Schedule"):
            el.clear()
        elif in_f:
            seen.add(tag)
    return {**head, "ix": ix, "sf": sf, **groups, "schedf_tags": sorted(seen), "_v": EXTRACT_V}


def save(path: str, obj: dict) -> dict:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh)
    return obj


def load_extract(oid: str, cache: str, local_paths: Mapping, fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == EXTRACT_V:
            return c
    lp = local_paths.get(oid)
    if lp:
        try:
            with open(lp, "rb") as fh:
                return save(path, {**parse_return(fh), "status": "ok", "via": "local"})
        except ET.ParseError:
            pass
    if not fetch:
        return {"status": "not_fetched"}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                return save(path, {**parse_return(resp), "status": "ok", "via": "mirror"})
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"status": f"http_{e.code}"}
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError):
            time.sleep(3 * (attempt + 1))
    return {"status": "error"}


def load_all(oids: Sequence[str], cache: str, local_paths: Mapping, fetch: bool, workers: int) -> dict:
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        return dict(zip(oids, ex.map(lambda o: load_extract(o, cache, local_paths, fetch), oids)))


def read_paths(list_files: Sequence[str]) -> dict:
    out = {}
    for f in list_files:
        with open(f, encoding="utf-8") as fh:
            for p in (l.strip() for l in fh if l.strip()):
                b = os.path.basename(p).replace("_public", "").replace(".xml", "")
                if os.path.exists(p):
                    out.setdefault(b, p)
    return out


def intermediary_returns(irs_dir: str) -> dict:
    """(ein, fy) -> oid: latest Form 990 e-file per tax period, tax periods ending in FY2023/FY2024."""
    hits = []
    for y in range(2023, 2027):
        p = os.path.join(irs_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8", errors="replace", newline="") as fh:
            for r in csv.reader(fh):
                if len(r) > 8 and ein9(r[2]) in INTERMEDIARIES and r[6] == "990" and r[3][:4].isdigit() \
                        and int(r[3][:4]) in FYS:
                    hits.append((ein9(r[2]), int(r[3][:4]), r[3], r[8]))
    per_period = {(e, per): max(o for e2, _, p2, o in hits if (e2, p2) == (e, per)) for e, _, per, _ in hits}
    return {(e, int(per[:4])): o for (e, per), o in per_period.items()}


# ----------------------------------------------------------------------------- normalise
def region_of(txt: str) -> str:
    t = (txt or "").strip()
    if t in REGIONS:
        return t
    up = t.upper()
    head = up.split(" - ")[0].strip()
    hit = next((g for g, rx in COMPILED_NAMES if rx.search(head)), "") or \
        next((g for g, rx in COMPILED_REGIONS if rx.search(up)), "")
    return hit or ("unspecified" if not up else "unmapped")


def manner_of(txt: str) -> str:
    up = (txt or "").upper()
    if not up or up in ("N/A", "NA", "NONE", "0"):
        return "not_stated"
    if "WIRE" in up:
        return "wire"
    if re.search(r"ACH|EFT|ELECTRONIC|TRANSFER|BANK", up):
        return "ach_eft_transfer"
    if re.search(r"CHECK|CHEQUE|CHK", up):
        return "check"
    return "other"


def purpose_of(txt: str) -> str:
    up = (txt or "").upper()
    return next((g for g, rx in COMPILED_PURPOSE if rx.search(up)), "not_stated" if not up.strip() else "other")


def flags_of(part5: Sequence[Mapping]) -> dict:
    txt = " ".join(p.get("ExplanationTxt", "") for p in part5)
    return {"ed_text": int(bool(ED_RX.search(txt))), "er_text": int(bool(ER_RX.search(txt))),
            "ngosource_text": int(bool(NGO_RX.search(txt))), "intermediary_text": int(bool(INTERMED_RX.search(txt))),
            "part5_chars": len(txt)}


METHOD_RX = re.compile(r"WIRE|ACH|EFT|ELECTRONIC|CHECK|CHEQUE|TRANSFER|BANK|PAYPAL|N/A")


def repair(g: Mapping) -> dict:
    """Undo a one-column shift seen in some filings (purpose in the manner field, manner in the valuation field)."""
    m, v = (g.get("MannerOfCashDisbursementTxt") or "").upper(), (g.get("ValuationMethodUsedDesc") or "").upper()
    if not g.get("PurposeOfGrantTxt") and m and not METHOD_RX.search(m) and METHOD_RX.search(v):
        return {**g, "PurposeOfGrantTxt": g["MannerOfCashDisbursementTxt"], "MannerOfCashDisbursementTxt": g["ValuationMethodUsedDesc"],
                "_repaired": True}
    return dict(g)


def activity_of(txt: str) -> str:
    up = (txt or "").upper()
    return "grantmaking" if "GRANT" in up else "investments" if "INVEST" in up else "program_or_other" if up else "not_stated"


def bool01(v) -> int | str:
    """e-file booleans come as true/false or 1/0; blank when the item is absent."""
    t = (v or "").strip().lower()
    return 1 if t in ("1", "true", "x") else 0 if t in ("0", "false") else ""


def amt(d: Mapping) -> float:
    return (num(d.get("CashGrantAmt")) or 0.0) + (num(d.get("NonCashAssistanceAmt")) or 0.0)


def sponsor_year(key: tuple, x: Mapping, ex: Mapping, panel: Mapping, rank: Mapping, sched_i: Mapping, weight) -> dict:
    e, fy = key
    ix, sf = ex.get("ix", {}), ex.get("sf", {})
    l1, l2, l3 = (ix.get(k) or 0.0 for k in ("l1", "l2", "l3"))
    p2 = sum(amt(g) for g in ex.get("part2", ()))
    p3 = sum(amt(g) for g in ex.get("part3", ()))
    p1 = sum(num(g.get("RegionTotalExpendituresAmt")) or 0.0 for g in ex.get("part1", ()))
    p1g = sum(num(g.get("RegionTotalExpendituresAmt")) or 0.0 for g in ex.get("part1", ())
              if activity_of(g.get("TypeOfActivitiesConductedTxt")) == "grantmaking")
    si = sched_i.get(key, {})
    return {"row_type": "sponsor_year", "scope": panel[e]["name"], "scope_type": "sponsor", "ein": e,
            "segment": panel[e]["segment"], "sponsor_rank_fy2024": rank[e], "fiscal_year": str(fy), "object_id": x["oid"],
            "tax_period_end": ex.get("tax_period_end", ""), "sched_i_itemised": int(itemized(x)),
            "part_ix_l1_domestic_orgs_usd": round(l1), "part_ix_l2_domestic_indiv_usd": round(l2),
            "part_ix_l3_foreign_usd": round(l3), "total_grants_usd": round(l1 + l2 + l3),
            "foreign_share_of_grants": l3 / (l1 + l2 + l3) if (l1 + l2 + l3) else None,
            "sched_f_present": int(bool(sf.get("present"))), "sched_f_part1_regions": len(ex.get("part1", ())),
            "sched_f_part1_total_usd": round(p1), "sched_f_part1_grantmaking_usd": round(p1g), "sched_f_part1_total_spent_reported_usd": round(num(sf.get("TotalSpentAmt")) or 0),
            "sched_f_part2_lines": len(ex.get("part2", ())), "sched_f_part2_usd": round(p2),
            "sched_f_part2_501c3_cnt": num(sf.get("Total501c3OrgCnt")), "sched_f_part2_other_org_cnt": num(sf.get("TotalOtherOrgCnt")),
            "sched_f_part3_lines": len(ex.get("part3", ())), "sched_f_part3_usd": round(p3),
            "sched_f_part3_recipients": sum(num(g.get("RecipientCnt")) or 0 for g in ex.get("part3", ())),
            **{f"p4_{k}": bool01(ix.get(k)) for k in PART4_IND}, **{f"sf_{k}": bool01(sf.get(k)) for k in SCHEDF_IND},
            **flags_of(ex.get("part5", ())),
            "sched_i_gross_usd": round(si.get("gross", 0)), "sched_i_named_intermediary_usd": round(si.get("named", 0)),
            "sched_i_friends_of_usd": round(si.get("friends", 0)), "sched_i_ntee_q_usd": round(si.get("q", 0)),
            "sched_i_ntee_q_net_usd": round(si.get("q_net", 0)), "sched_i_net_usd": round(si.get("net", 0)),
            "sched_i_intl_union_net_usd": round(si.get("union_net", 0)),
            "daf_weight": weight, "status": ex.get("status", ""), "via": ex.get("via", "")}


# ----------------------------------------------------------------------------- Schedule I routes
def route_lines(key: tuple, lines: Sequence[Sequence], bmf: Mapping, wl_eins: frozenset, wl_names: Mapping) -> dict:
    """Schedule I lines -> gross/net totals and the three alternative routes. DAF-to-DAF flags and NTEE groups come
    from mission_recipient_sectors.annotate, so net totals equal P-NEW-RCP-01's."""
    ann = annotate(key[0], lines, bmf, wl_eins, wl_names)
    s = lambda pred: sum(r["amount"] for r in ann if pred(r))  # noqa: E731
    by_named, friends_top = {}, {}
    for r in ann:
        if r["ein"] in INTERMEDIARIES:
            by_named[r["ein"]] = by_named.get(r["ein"], 0.0) + r["amount"]
        elif FRIENDS.search((r["name"] or "").upper()):
            friends_top[r["key"]] = (r["name"], friends_top.get(r["key"], ("", 0.0))[1] + r["amount"])
    return {"gross": s(lambda r: True), "net": s(lambda r: not r["d2d"]),
            "named": s(lambda r: r["ein"] in INTERMEDIARIES),
            "friends": s(lambda r: r["ein"] not in INTERMEDIARIES and FRIENDS.search((r["name"] or "").upper())),
            "q": s(lambda r: r["ntee"][:1] == "Q"), "q_net": s(lambda r: r["ntee"][:1] == "Q" and not r["d2d"]),
            "union_net": s(lambda r: not r["d2d"] and (r["ein"] in INTERMEDIARIES or r["ntee"][:1] == "Q"
                                                        or FRIENDS.search((r["name"] or "").upper()))),
            "by_named": by_named, "friends_top": friends_top}


# ----------------------------------------------------------------------------- aggregate
def scopes(panel: Mapping, rank: Mapping) -> list:
    seg = lambda e: panel[e]["segment"]  # noqa: E731
    return ([("all_top50", "all", lambda e: True, "")]
            + [("all_ex_university_hospital", "all", lambda e: seg(e) != "university_hospital", "")]
            + [("all_ex_university_hospital_ex_svcf", "all", lambda e: seg(e) != "university_hospital" and e != SVCF, "")]
            + [(s, "segment", (lambda e, s=s: seg(e) == s), s) for s in SEGMENTS])


FYK = [(str(fy), (fy,)) for fy in FYS] + [("2023-2024", FYS)]


def totals_rows(sy_rows: Sequence[Mapping], panel: Mapping, rank: Mapping) -> list:
    out = []
    for name, stype, pred, segname in scopes(panel, rank):
        for fyl, fys in FYK:
            rs = [r for r in sy_rows if pred(r["ein"]) and int(r["fiscal_year"]) in fys]
            if not rs:
                continue
            s = lambda k: sum(r[k] or 0 for r in rs)  # noqa: E731
            w = lambda k: sum((r[k] or 0) * (r["daf_weight"] if r["daf_weight"] is not None else 1.0) for r in rs)  # noqa: E731
            item = [r for r in rs if r["sched_i_itemised"]]
            si = lambda k: sum(r[k] or 0 for r in item)  # noqa: E731
            l3_item = si("part_ix_l3_foreign_usd")
            net_plus = si("sched_i_net_usd") + l3_item
            out.append({"row_type": "scope_total", "scope": name, "scope_type": stype, "segment": segname,
                        "fiscal_year": fyl, "sponsor_years": len(rs),
                        "sponsor_years_with_foreign_grants": sum(1 for r in rs if (r["part_ix_l3_foreign_usd"] or 0) > 0),
                        "sponsor_years_sched_f": sum(r["sched_f_present"] for r in rs),
                        "part_ix_l3_foreign_usd": s("part_ix_l3_foreign_usd"), "total_grants_usd": s("total_grants_usd"),
                        "foreign_share_of_grants": s("part_ix_l3_foreign_usd") / s("total_grants_usd") if s("total_grants_usd") else None,
                        "foreign_daf_weighted_usd": round(w("part_ix_l3_foreign_usd")),
                        "total_grants_daf_weighted_usd": round(w("total_grants_usd")),
                        "sched_f_part2_usd": s("sched_f_part2_usd"), "sched_f_part3_usd": s("sched_f_part3_usd"),
                        "sched_f_part1_total_usd": s("sched_f_part1_total_usd"),
                        "sched_f_part2_lines": s("sched_f_part2_lines"),
                        "sched_f_part2_501c3_cnt": s("sched_f_part2_501c3_cnt"),
                        "sched_f_part2_other_org_cnt": s("sched_f_part2_other_org_cnt"),
                        "sched_i_gross_usd": si("sched_i_gross_usd"), "sched_i_net_usd": si("sched_i_net_usd"),
                        "sched_i_named_intermediary_usd": si("sched_i_named_intermediary_usd"),
                        "sched_i_friends_of_usd": si("sched_i_friends_of_usd"), "sched_i_ntee_q_usd": si("sched_i_ntee_q_usd"),
                        "sched_i_ntee_q_net_usd": si("sched_i_ntee_q_net_usd"),
                        "sched_i_intl_union_net_usd": si("sched_i_intl_union_net_usd"),
                        "broad_intl_share_of_net_sched_i_plus_l3": (l3_item + si("sched_i_intl_union_net_usd")) / net_plus if net_plus else None,
                        "sched_f_part1_grantmaking_usd": s("sched_f_part1_grantmaking_usd"),
                        "itemising_part_ix_l3_foreign_usd": l3_item,
                        "foreign_share_of_net_sched_i_plus_l3": l3_item / net_plus if net_plus else None,
                        "ntee_q_share_of_net_sched_i_plus_l3": si("sched_i_ntee_q_net_usd") / net_plus if net_plus else None,
                        "ed_text_sponsor_years": sum(1 for r in rs if r["ed_text"]),
                        "er_text_sponsor_years": sum(1 for r in rs if r["er_text"]),
                        "source": SOURCE})
    return out


def dim_rows(sy: Mapping, ex: Mapping, panel: Mapping, rank: Mapping) -> list:
    """Region (Parts I-III), purpose bucket, purpose text (Part II), manner (Parts II-III) by scope x FY."""
    def items(k):
        e, fy = k
        x = {**ex[k], "part2": [repair(g) for g in ex[k].get("part2", ())]}
        p1g = [g for g in x.get("part1", ()) if activity_of(g.get("TypeOfActivitiesConductedTxt")) == "grantmaking"]
        return ([("region_part2", region_of(g.get("RegionTxt")), amt(g)) for g in x.get("part2", ())]
                + [("activity_part1", activity_of(g.get("TypeOfActivitiesConductedTxt")),
                    num(g.get("RegionTotalExpendituresAmt")) or 0.0) for g in x.get("part1", ())]
                + [("region_part1_grantmaking", region_of(g.get("RegionTxt")), num(g.get("RegionTotalExpendituresAmt")) or 0.0)
                   for g in p1g]
                + [("region_part3", region_of(g.get("RegionTxt")), amt(g)) for g in x.get("part3", ())]
                + [("purpose_bucket_part2", purpose_of(g.get("PurposeOfGrantTxt")), amt(g)) for g in x.get("part2", ())]
                + [("purpose_text_part2", re.sub(r"\s+", " ", (g.get("PurposeOfGrantTxt") or "").upper().strip())[:80]
                    or "(blank)", amt(g)) for g in x.get("part2", ())]
                + [("manner_part2", manner_of(g.get("MannerOfCashDisbursementTxt")), amt(g)) for g in x.get("part2", ())]
                + [("manner_part3", manner_of(g.get("MannerOfCashDisbursementTxt")), amt(g)) for g in x.get("part3", ())]
                + [("assistance_type_part3", (g.get("TypeOfAssistanceTxt") or "(blank)").upper()[:60], amt(g))
                   for g in x.get("part3", ())])
    per = {k: items(k) for k in sy if k in ex}
    out = []
    sponsor_scopes = [(panel[e]["name"], "sponsor", (lambda x, e=e: x == e), panel[e]["segment"], rank[e])
                      for e in sorted(rank, key=rank.get)]
    for name, stype, pred, segname, *rk in [s + () for s in scopes(panel, rank)] + sponsor_scopes:
        for fyl, fys in FYK:
            keys = [k for k in per if pred(k[0]) and k[1] in fys]
            if not keys:
                continue
            its = [i for k in keys for i in per[k]]
            for dim, rows in _group_by_fast(its, lambda i: i[0]).items():
                if stype == "sponsor" and dim == "purpose_text_part2":
                    continue
                tot = sum(r[2] for r in rows)
                by = _group_by_fast(rows, lambda i: i[1])
                cats = sorted(by.items(), key=lambda kv: -sum(r[2] for r in kv[1]))
                if dim == "purpose_text_part2":
                    cats = cats[:25]
                for c, rs in cats:
                    a = sum(r[2] for r in rs)
                    out.append({"row_type": dim, "scope": name, "scope_type": stype, "segment": segname,
                                "sponsor_rank_fy2024": rk[0] if rk else "", "fiscal_year": fyl, "category": c,
                                "amount_usd": round(a), "share": a / tot if tot else None, "denominator_usd": round(tot),
                                "lines": len(rs), "sponsor_years": len(keys), "source": SOURCE})
    return out


def intermediary_rows(sched_i: Mapping, inter_ex: Mapping, inter_oids: Mapping, sy_keys) -> tuple[list, dict]:
    out, summ = [], {}
    for e, nm in INTERMEDIARIES.items():
        for fyl, fys in FYK:
            inbound = sum(sched_i.get(k, {}).get("by_named", {}).get(e, 0.0) for k in sy_keys if k[1] in fys)
            exs = [inter_ex.get(inter_oids.get((e, fy))) for fy in fys]
            exs = [x for x in exs if x and x.get("status") == "ok"]
            l = lambda k: sum(x["ix"].get(k) or 0.0 for x in exs)  # noqa: E731
            tot = l("l1") + l("l2") + l("l3")
            share = l("l3") / tot if tot else None
            grantors = len({k[0] for k in sy_keys if k[1] in fys and sched_i.get(k, {}).get("by_named", {}).get(e)})
            r = {"row_type": "intermediary", "scope": nm, "scope_type": "intermediary", "ein": e, "fiscal_year": fyl,
                 "object_id": ";".join(sorted(inter_oids[(e, fy)] for fy in fys if (e, fy) in inter_oids)),
                 "amount_usd": round(inbound), "grantors": grantors,
                 "intermediary_total_grants_usd": round(tot), "intermediary_part_ix_l3_foreign_usd": round(l("l3")),
                 "intermediary_foreign_share": share,
                 "est_foreign_pass_through_usd": round(inbound * share) if share is not None else None,
                 "source": SOURCE}
            out.append(r)
            summ.setdefault(fyl, []).append(r)
    return out, summ


FIELDS = ("row_type", "scope", "scope_type", "ein", "segment", "sponsor_rank_fy2024", "fiscal_year", "object_id",
          "tax_period_end", "category", "amount_usd", "share", "denominator_usd", "lines", "sponsor_years", "grantors",
          "sched_i_itemised", "part_ix_l1_domestic_orgs_usd", "part_ix_l2_domestic_indiv_usd", "part_ix_l3_foreign_usd",
          "total_grants_usd", "foreign_share_of_grants", "foreign_daf_weighted_usd", "total_grants_daf_weighted_usd",
          "daf_weight", "sponsor_years_with_foreign_grants", "sponsor_years_sched_f", "sched_f_present",
          "sched_f_part1_regions", "sched_f_part1_total_usd", "sched_f_part1_grantmaking_usd", "sched_f_part1_total_spent_reported_usd",
          "sched_f_part2_lines", "sched_f_part2_usd", "sched_f_part2_501c3_cnt", "sched_f_part2_other_org_cnt",
          "sched_f_part3_lines", "sched_f_part3_usd", "sched_f_part3_recipients",
          *(f"p4_{k}" for k in PART4_IND), *(f"sf_{k}" for k in SCHEDF_IND),
          "ed_text", "er_text", "ngosource_text", "intermediary_text", "part5_chars", "ed_text_sponsor_years",
          "er_text_sponsor_years", "sched_i_gross_usd", "sched_i_net_usd", "sched_i_named_intermediary_usd",
          "sched_i_friends_of_usd", "sched_i_ntee_q_usd", "sched_i_ntee_q_net_usd", "sched_i_intl_union_net_usd",
          "itemising_part_ix_l3_foreign_usd", "foreign_share_of_net_sched_i_plus_l3", "ntee_q_share_of_net_sched_i_plus_l3",
          "broad_intl_share_of_net_sched_i_plus_l3", "intermediary_total_grants_usd",
          "intermediary_part_ix_l3_foreign_usd", "intermediary_foreign_share", "est_foreign_pass_through_usd",
          "status", "via", "source")


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--extract-cache", required=True)
    ap.add_argument("--xml-list", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    sy = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen}
    local_paths = read_paths(a.xml_list)
    inter_oids = intermediary_returns(a.irs_dir)
    oids = sorted({x["oid"] for x in sy.values()} | set(inter_oids.values()))
    loaded = load_all(oids, a.extract_cache, local_paths, a.fetch, a.workers)
    ex = {k: loaded[x["oid"]] for k, x in sy.items() if loaded[x["oid"]].get("status") == "ok"}
    bad = {f"{panel[k[0]]['name']} FY{k[1]}": loaded[x["oid"]].get("status") for k, x in sy.items() if k not in ex}
    filer_mismatch = [k for k, v in ex.items() if v.get("filer_ein") != k[0]]

    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    names = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in names.items() if k and len(v) == 1}
    lines = {}
    for k, x in sy.items():
        p = os.path.join(a.lines_cache, f"{x['oid']}.json")
        if itemized(x) and os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                lines[k] = json.load(fh)["lines"]
    bmf = load_bmf(a.bmf_dir, frozenset(l[0] for ls in lines.values() for l in ls if l[0].strip("0")))
    sched_i = {k: route_lines(k, ls, bmf, wl_eins, wl_names) for k, ls in lines.items()}

    cost = read_csv(COST)
    share = {(ein9(r["ein"]), int(r["fiscal_year"])): num(r["daf_share_of_grants"]) for r in cost if r["daf_share_of_grants"]}
    wt = lambda k: min(1.0, max(0.0, share[k])) if share.get(k) is not None else None  # noqa: E731

    sy_rows = [sponsor_year(k, sy[k], ex[k], panel, rank, sched_i, wt(k)) for k in sorted(ex, key=lambda k: (rank[k[0]], k[1]))]
    tot_rows = totals_rows(sy_rows, panel, rank)
    d_rows = dim_rows(sy, ex, panel, rank)
    inter_ex = {o: loaded[o] for o in inter_oids.values()}
    i_rows, i_summ = intermediary_rows(sched_i, inter_ex, inter_oids, list(sched_i))
    write_csv(OUT, tot_rows + sy_rows + d_rows + i_rows, FIELDS)

    def pick(rt, scope, fy="2023-2024"):
        return [r for r in (tot_rows + d_rows) if r["row_type"] == rt and r["scope"] == scope and r["fiscal_year"] == fy]
    fr = {}
    for k, v in sched_i.items():
        for kk, (nm, a_) in v["friends_top"].items():
            fr[kk] = (nm, fr.get(kk, ("", 0.0))[1] + a_)
    l3_vs_f = [(r["scope"][:30], r["fiscal_year"], r["part_ix_l3_foreign_usd"], r["sched_f_part2_usd"] + r["sched_f_part3_usd"])
               for r in sy_rows if r["part_ix_l3_foreign_usd"] or r["sched_f_part2_usd"]]
    summary = {
        "sponsor_years": len(sy), "extracted_ok": len(ex), "problems": bad, "filer_mismatch": filer_mismatch,
        "via": {s: sum(1 for k in ex if ex[k].get("via") == s) for s in ("local", "mirror")},
        "intermediary_returns": {f"{INTERMEDIARIES[e][:20]} FY{fy}": o for (e, fy), o in sorted(inter_oids.items())},
        "intermediary_status": {o: loaded[o].get("status") for o in inter_oids.values()},
        "schedf_tags": sorted({t for v in ex.values() for t in v.get("schedf_tags", [])}),
        "part2_keys": sorted({kk for v in ex.values() for g in v.get("part2", []) for kk in g}),
        "part3_keys": sorted({kk for v in ex.values() for g in v.get("part3", []) for kk in g}),
        "unmapped_regions": sorted({g.get("RegionTxt", "") for v in ex.values() for p in ("part1", "part2", "part3")
                                    for g in v.get(p, []) if region_of(g.get("RegionTxt")) in ("unmapped",)
                                    or (g.get("RegionTxt") or "") not in REGIONS})[:60],
        "totals": {r["scope"] + " " + r["fiscal_year"]: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()
                                                         if k not in ("source", "row_type", "scope", "scope_type", "segment")}
                   for r in tot_rows},
        "regions_ex_uh": {d: [(r["category"], r["amount_usd"], round(r["share"] or 0, 4)) for r in pick(d, "all_ex_university_hospital")]
                          for d in ("region_part2", "region_part3", "region_part1_grantmaking", "activity_part1")},
        "repaired_part2_usd": round(sum(amt(g) for v in ex.values() for g in map(repair, v.get("part2", [])) if g.get("_repaired"))),
        "purpose_bucket_ex_uh": [(r["category"], r["amount_usd"], round(r["share"] or 0, 4), r["lines"]) for r in pick("purpose_bucket_part2", "all_ex_university_hospital")],
        "purpose_text_ex_uh": [(r["category"], r["amount_usd"], r["lines"]) for r in pick("purpose_text_part2", "all_ex_university_hospital")][:20],
        "manner_ex_uh": [(r["category"], r["amount_usd"], round(r["share"] or 0, 4), r["lines"]) for r in pick("manner_part2", "all_ex_university_hospital")],
        "part3_types_ex_uh": [(r["category"], r["amount_usd"], r["lines"]) for r in pick("assistance_type_part3", "all_ex_university_hospital")][:10],
        "sponsor_years_table": [(r["sponsor_rank_fy2024"], r["scope"][:32], r["segment"][:5], r["fiscal_year"], r["part_ix_l3_foreign_usd"],
                                 round(r["foreign_share_of_grants"] or 0, 4), r["sched_f_part2_usd"], r["sched_f_part3_usd"],
                                 r["sched_f_part2_lines"], r["sched_f_part2_501c3_cnt"], r["sched_f_part2_other_org_cnt"],
                                 int(r["ed_text"]), int(r["er_text"]), int(r["ngosource_text"]), r["sched_i_named_intermediary_usd"],
                                 r["sched_i_friends_of_usd"], r["sched_i_ntee_q_net_usd"]) for r in sy_rows],
        "l3_vs_part2_plus_part3": l3_vs_f,
        "intermediaries": {fy: [(r["scope"][:28], r["amount_usd"], r["grantors"], r["intermediary_total_grants_usd"],
                                 round(r["intermediary_foreign_share"], 4) if r["intermediary_foreign_share"] is not None else None,
                                 r["est_foreign_pass_through_usd"]) for r in rs] for fy, rs in i_summ.items()},
        "top_foreign_sponsors_ex_uh": sorted(((r["sponsor_rank_fy2024"], r["scope"][:32], r["segment"], r["fiscal_year"], r["part_ix_l3_foreign_usd"])
                                              for r in sy_rows if r["segment"] != "university_hospital"), key=lambda t: -t[4])[:14],
        "foreign_by_sponsor_pooled_ex_uh": sorted(((rank[e], panel[e]["name"][:32], panel[e]["segment"],
                                                    sum(r["part_ix_l3_foreign_usd"] for r in sy_rows if r["ein"] == e),
                                                    sum(r["total_grants_usd"] for r in sy_rows if r["ein"] == e))
                                                   for e in rank if panel[e]["segment"] != "university_hospital"), key=lambda t: -t[3])[:15],
        "method_text_among_foreign_granting_sy": {
            "n": sum(1 for r in sy_rows if r["part_ix_l3_foreign_usd"] > 0),
            "ed": sum(1 for r in sy_rows if r["part_ix_l3_foreign_usd"] > 0 and r["ed_text"]),
            "er": sum(1 for r in sy_rows if r["part_ix_l3_foreign_usd"] > 0 and r["er_text"]),
            "either": sum(1 for r in sy_rows if r["part_ix_l3_foreign_usd"] > 0 and (r["ed_text"] or r["er_text"])),
            "usd_with_either": sum(r["part_ix_l3_foreign_usd"] for r in sy_rows if r["ed_text"] or r["er_text"]),
            "ngosource": sum(1 for r in sy_rows if r["ngosource_text"]),
            "intermediary_text": sum(1 for r in sy_rows if r["intermediary_text"]),
            "grant_records_maintained_false": [r["scope"][:30] + " " + r["fiscal_year"] for r in sy_rows
                                               if r["sf_GrantRecordsMaintainedInd"] == 0]},
        "indicator_counts": {k: {"yes": sum(1 for r in sy_rows if r[k] == 1), "no": sum(1 for r in sy_rows if r[k] == 0)}
                             for k in [f"p4_{x}" for x in PART4_IND] + [f"sf_{x}" for x in SCHEDF_IND]},
        "intermediary_totals": {fy: {"inbound": sum(r["amount_usd"] for r in rs),
                                     "est_pass_through": sum(r["est_foreign_pass_through_usd"] or 0 for r in rs)}
                                for fy, rs in i_summ.items()},
        "friends_top": sorted(((v[0], round(v[1])) for v in fr.values()), key=lambda t: -t[1])[:25],
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
