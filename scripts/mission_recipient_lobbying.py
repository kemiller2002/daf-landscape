#!/usr/bin/env python3
"""Lobbying and political-campaign reporting by DAF grant recipients: top-50 DAF sponsors, FY2023-FY2024
(queue item P-NEW-ADV-01).

Universe, Schedule I lines and the DAF-to-DAF flag are exactly those of scripts/mission_recipient_sectors.py
(top-50 DAFRC sponsors by FY2024 DAF assets; 94 itemising sponsor-years; every Schedule I Part II line from the
cached line JSON; DAF-to-DAF lines flagged via daf-to-daf-recipient-whitelist.csv and excluded here).

Steps (pure transforms; I/O at the edges)
  1. Recipients  net (non-DAF-to-DAF) Schedule I dollars per recipient EIN, pooled FY2023-2024.
  2. Targets     recipient EINs covering the top --share-all of net dollars across all sponsors, plus the top
                 --share-seg of each sponsor segment's net dollars (so community-foundation recipients are
                 not under-sampled). Lines below the cut stay in the denominators as "not selected".
  3. Return      IRS TEOS e-file index (apps.irs.gov/pub/epostcard/990/xml/{Y}/index_{Y}.csv, 2021-2026):
                 one Form 990 or 990-EZ per target EIN, preferring tax-period ends 2023-01..2024-12 (latest),
                 then 2025, then 2022, then 2021-12; latest object id within a period (990 before 990-EZ).
                 990-PF filers and EINs with no TY2021+ e-filed return are classified from the EO BMF
                 (church / 990-N / group-return subordinate / government / private foundation / other).
  4. Parse       the chosen XML (GivingTuesday mirror of IRS TEOS, or a local copy) is streamed; the main form's
                 Part IV lines 3-4 (PoliticalCampaignActyInd, LobbyingActivitiesInd), total expenses, and
                 every Schedule C leaf value are kept. Reading stops after Schedule C ends (or when a later
                 schedule starts and Part IV lines 3-4 are both No).
  5. Classify    Part II-A (501(h) elector): TotalLobbyingExpendGrp/FilingOrganizationsTotalAmt (or direct +
                 grassroots) > 0 -> reports lobbying. Part II-B (non-electing): any of lines 1a-1i 'Yes' or line
                 1j total > 0 -> reports lobbying. No Part II and Part IV line 4 = No -> reports none.
                 Part IV line 4 = Yes but no Schedule C Part II parsed -> reports lobbying, amount unknown.
                 Intensity = lobbying expenditures / total expenses (Part I line 18; 990-EZ line 17).
                 Political: Part IV line 3 = Yes, or any positive Schedule C Part I-A/I-B/I-C amount.
  6. Aggregate   shares of net DAF grant dollars to recipients reporting any lobbying, by scope (all, segment)
                 x NTEE major group x FY; intensity distribution; coverage.

Stdlib only; functional style.

Usage:
  python3 scripts/mission_recipient_lobbying.py --np-cache NPCACHE --bmf-dir BMF --lines-cache LC \
      --irs-dir IRS --ret-cache RC [--xml-dir D ...] [--fetch] [--workers 16]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
import mission_recipient_sectors as RS  # noqa: E402

OUT = os.path.join(DATA, "daf-recipient-lobbying-2023-2024.csv")
INDEX_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
INDEX_YEARS = (2021, 2022, 2023, 2024, 2025, 2026)
RET_V = 1
SOURCE = ("Recipient Form 990/990-EZ Part IV and Schedule C (IRS e-file XML via GivingTuesday mirror of IRS TEOS; "
          "return located with IRS TEOS index 2021-2026); grant dollars = top-50 sponsors' Schedule I Part II, "
          "FY2023-2024, net of DAF-to-DAF (mission_recipient_sectors.py); sectors = IRS EO BMF NTEE")

II_B_IND = ("VolunteersInd", "PaidStaffOrManagementInd", "MediaAdvertisementsInd", "MailingsMembersInd",
            "PublicationsOrBroadcastInd", "GrantsOtherOrganizationsInd", "DirectContactLegislatorsInd",
            "RalliesDemonstrationsInd", "OtherActivitiesInd")
II_A_TOTAL = "TotalLobbyingExpendGrp/FilingOrganizationsTotalAmt"
II_A_DIRECT = "TotalDirectLobbyingGrp/FilingOrganizationsTotalAmt"
II_A_GRASS = "TotalGrassrootsLobbyingGrp/FilingOrganizationsTotalAmt"
II_A_EXEMPT = "TotalExemptPurposeExpendGrp/FilingOrganizationsTotalAmt"
II_A_NONTAX = "LobbyingNontaxableAmountGrp/FilingOrganizationsTotalAmt"
MAIN_KEEP = ("CYTotalExpensesAmt", "TotalExpensesAmt", "PoliticalCampaignActyInd", "LobbyingActivitiesInd",
             "GroupReturnForAffiliatesInd", "Organization501c3Ind", "DescribedInSection501c3Ind",
             "Organization501cInd", "TotalFunctionalExpensesGrp/TotalAmt")
HDR_KEEP = ("ReturnTypeCd", "TaxPeriodEndDt", "TaxPeriodBeginDt", "AmendedReturnInd", "TaxYr")
SKIP_TEXT = ("ExplanationTxt", "FormAndLineReferenceDesc", "Desc", "Txt")
BINS = ((0.0, 0.0, "0 (none reported)"), (0.0, 0.001, ">0-0.1%"), (0.001, 0.01, "0.1-1%"), (0.01, 0.05, "1-5%"),
        (0.05, 0.20, "5-20%"), (0.20, 1e9, ">20%"))
STATUS_CODE = {"lobby_501h": 1, "lobby_ii_b": 2, "lobby_part_iv_only": 3, "none_501h_zero": 4, "none_ii_b_all_no": 5,
               "none_part_iv_no": 6, "parsed_no_lobby_data": 7, "no_sched_c_990pf": 8, "no_return_church": 9,
               "no_return_990n": 10, "no_return_group_subordinate": 11, "no_return_government": 12,
               "no_return_other_in_bmf": 13, "no_return_not_in_bmf": 14, "fetch_or_parse_failed": 15,
               "not_selected": 16, "blank_ein": 17, "parsed_non_501c3": 18}
FORM_CODE = {"990": 1, "990EZ": 2, "990PF": 3, "": 0}
SECTOR_CODE = {g: i + 1 for i, g in enumerate(RS.GROUPS)}


# ----------------------------------------------------------------------------- small pure helpers
def ind(v: str | None) -> int | None:
    if v is None or v == "":
        return None
    return 1 if v.strip().lower() in ("1", "true", "x", "yes") else 0


def amount(d: Mapping, k: str) -> float | None:
    return num(d.get(k)) if d.get(k) not in (None, "") else None


def bin_of(r: float | None) -> str:
    if r is None:
        return "unknown_amount"
    if r <= 0:
        return BINS[0][2]
    return next(lbl for lo, hi, lbl in BINS[1:] if lo < r <= hi or (hi > 1 and r > lo))


# ----------------------------------------------------------------------------- recipients and targets
def recipient_totals(ann: Mapping, panel: Mapping) -> dict:
    """-> ein -> {"total", "by_seg": {seg: $}, "by_fy": {fy: $}, "group", "ntee"} over non-DAF-to-DAF lines."""
    out = {}
    for (spon, fy), rs in ann.items():
        seg = panel[spon]["segment"]
        for r in rs:
            if r["d2d"] or not r["ein"]:
                continue
            d = out.setdefault(r["ein"], {"total": 0.0, "by_seg": {}, "by_fy": {}, "group": r["group"], "ntee": r["ntee"]})
            d["total"] += r["amount"]
            d["by_seg"][seg] = d["by_seg"].get(seg, 0.0) + r["amount"]
            d["by_fy"][fy] = d["by_fy"].get(fy, 0.0) + r["amount"]
    return out


def top_share(vals: Mapping, share: float) -> frozenset:
    tot = sum(v for v in vals.values() if v > 0)
    acc, keep = 0.0, []
    for e, v in sorted(vals.items(), key=lambda kv: -kv[1]):
        if v <= 0 or acc >= share * tot:
            break
        keep.append(e)
        acc += v
    return frozenset(keep)


def select_targets(rec: Mapping, share_all: float, share_seg: float) -> frozenset:
    segs = {s for d in rec.values() for s in d["by_seg"]}
    per_seg = (top_share({e: d["by_seg"].get(s, 0.0) for e, d in rec.items()}, share_seg) for s in segs)
    return top_share({e: d["total"] for e, d in rec.items()}, share_all).union(*per_seg)


# ----------------------------------------------------------------------------- index and BMF
def load_index(irs_dir: str, eins: frozenset) -> dict:
    out = {}
    for y in INDEX_YEARS:
        p = os.path.join(irs_dir, f"index_{y}.csv")
        with open(p, encoding="utf-8", errors="replace", newline="") as fh:
            for r in csv.DictReader(fh):
                e = ein9(r["EIN"])
                if e in eins and r["RETURN_TYPE"] in ("990", "990EZ", "990PF") and r["TAX_PERIOD"][:6].isdigit():
                    out.setdefault(e, []).append({"form": r["RETURN_TYPE"], "period": int(r["TAX_PERIOD"][:6]),
                                                  "oid": r["OBJECT_ID"], "index_year": y})
    return out


def period_rank(p: int) -> tuple:
    if 202301 <= p <= 202412:
        return (0, -p)
    if 202501 <= p <= 202612:
        return (1, p)
    if 202201 <= p <= 202212:
        return (2, -p)
    if 202112 <= p <= 202112:
        return (3, -p)
    return (9, 0)


def choose_return(rows: Sequence[Mapping]) -> Mapping | None:
    ok = [r for r in rows if period_rank(r["period"])[0] < 9]
    full = [r for r in ok if r["form"] in ("990", "990EZ")]
    pool = full or [r for r in ok if r["form"] == "990PF"]
    if not pool:
        return None
    return min(pool, key=lambda r: (period_rank(r["period"]), 0 if r["form"] == "990" else 1, -int(r["oid"] or 0)))


def load_bmf_filing(bmf_dir: str, eins: frozenset) -> dict:
    keep = ("SUBSECTION", "FOUNDATION", "AFFILIATION", "GROUP", "FILING_REQ_CD", "PF_FILING_REQ_CD", "NAME")
    out = {}
    for f in RS.BMF_FILES:
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="latin-1", newline="") as fh:
            for r in csv.DictReader(fh):
                e = ein9(r["EIN"])
                if e in eins:
                    out[e] = {k.lower(): (r.get(k) or "").strip() for k in keep}
    return out


def no_return_status(ein: str, bmf: Mapping, name: str) -> str:
    b = bmf.get(ein)
    if not b:
        return "no_return_not_in_bmf"
    fr = b["filing_req_cd"]
    if b["foundation"] == "10" or fr in ("06", "13"):
        return "no_return_church"
    if b["subsection"] == "01" or fr == "14" or "GOV" in name.upper().split():
        return "no_return_government"
    if fr == "02":
        return "no_return_990n"
    if b["affiliation"] == "9" or fr == "03" or (b["group"] not in ("", "0000") and b["affiliation"] != "6"):
        return "no_return_group_subordinate"
    return "no_return_other_in_bmf"


# ----------------------------------------------------------------------------- parse one return (streamed)
def parse_return(stream) -> dict:
    hdr, main, sc, stack = {}, {}, {}, []
    seen_c = in_c = main_done = False
    part_iv_no = lambda: ind(main.get("PoliticalCampaignActyInd")) == 0 and ind(main.get("LobbyingActivitiesInd")) == 0  # noqa: E731
    sec = "hdr"
    for ev, el in ET.iterparse(stream, events=("start", "end")):
        tag = local(el.tag)
        if ev == "start":
            if tag == "IRS990ScheduleC":
                in_c, seen_c, sec = True, True, "C"
            elif tag in ("IRS990", "IRS990EZ", "IRS990PF"):
                sec = "main"
            elif tag.startswith("IRS990Schedule") and tag > "IRS990ScheduleC" and main_done and not seen_c and part_iv_no():
                break
            stack.append(tag)
            continue
        stack.pop()
        txt = (el.text or "").strip()
        parent = stack[-1] if stack else ""
        if tag == "IRS990ScheduleC":
            in_c = False
            el.clear()
            break
        if tag in ("IRS990", "IRS990EZ", "IRS990PF"):
            main_done, sec = True, "post"
            el.clear()
            continue
        if in_c and txt and not tag.endswith(SKIP_TEXT):
            key = f"{parent}/{tag}" if parent.endswith("Grp") else tag
            sc[key] = txt[:40]
        elif sec == "main":
            key = f"{parent}/{tag}" if parent.endswith("Grp") else tag
            if key in MAIN_KEEP or ("Lobby" in tag or "Politic" in tag) and tag.endswith(("Ind", "Amt")):
                main[key] = txt[:40] if txt else ("X" if tag == "Organization501cInd" else "")
        elif sec == "hdr" and tag in HDR_KEEP:
            hdr[tag] = txt
        elif sec == "hdr" and tag == "EIN" and parent == "Filer":
            hdr["FilerEIN"] = txt
        if not stack or len(stack) <= 2:
            el.clear()
    return {"hdr": hdr, "main": main, "sched_c": sc, "sched_c_present": seen_c}


def cache_path(cache: str, oid: str) -> str:
    return os.path.join(cache, oid[:6], f"{oid}.json")


def load_return(oid: str, cache: str, xml_dirs: Sequence[str], fetch: bool) -> dict:
    path = cache_path(cache, oid)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == RET_V:
            return c
    for p in (os.path.join(d, f"{oid}{s}") for d in xml_dirs for s in (".xml", "_public.xml")):
        if os.path.exists(p):
            try:
                with open(p, "rb") as fh:
                    return RS.save(path, {**parse_return(fh), "status": "ok", "via": "local", "_v": RET_V})
            except ET.ParseError:
                pass
    if not fetch:
        return {"status": "not_fetched"}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    last = "error"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                r = parse_return(resp)
            return RS.save(path, {**r, "status": "ok", "via": "mirror", "_v": RET_V})
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return RS.save(path, {"status": f"http_{e.code}", "via": "mirror", "_v": RET_V})
            last = f"http_{e.code}"
        except ET.ParseError:
            last = "parse_error"
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last = f"net:{type(e).__name__}"
        time.sleep(2 * (attempt + 1))
    return {"status": last}


# ----------------------------------------------------------------------------- classify one recipient (pure)
II_A_PREFIXES = ("TotalGrassrootsLobbyingGrp", "TotalDirectLobbyingGrp", "TotalLobbyingExpendGrp",
                 "OtherExemptPurposeExpendGrp", "TotalExemptPurposeExpendGrp", "LobbyingNontaxableAmountGrp",
                 "GrassrootsNontaxableGrp", "TotLbbyngGrassrootMnsNonTxGrp", "TotLbbyExpendMnsLbbyngNonTxGrp",
                 "AvgLobbyingNontaxableAmountGrp", "AvgTotalLobbyingExpendGrp", "AvgGrassrootsNontaxableGrp",
                 "AvgGrassrootsLobbyingExpendGrp", "LobbyingCeilingAmt", "GrassrootsCeilingAmt")
II_B_AMTS = frozenset(f"{x[:-3]}Amt" for x in II_B_IND) | {"TotalLobbyingExpendituresAmt"}


def is_part_ii(k: str) -> bool:
    return k.split("/")[0] in II_A_PREFIXES or k in II_B_AMTS


def classify_return(ret: Mapping, form: str) -> dict:
    m, sc = ret.get("main", {}), ret.get("sched_c", {})
    exp = (amount(m, "CYTotalExpensesAmt") if form == "990" else amount(m, "TotalExpensesAmt"))
    exp = exp if exp is not None else amount(m, "TotalFunctionalExpensesGrp/TotalAmt")
    iv3, iv4 = ind(m.get("PoliticalCampaignActyInd")), ind(m.get("LobbyingActivitiesInd"))
    h_total, h_direct, h_grass = amount(sc, II_A_TOTAL), amount(sc, II_A_DIRECT), amount(sc, II_A_GRASS)
    h_exempt, h_nontax = amount(sc, II_A_EXEMPT), amount(sc, II_A_NONTAX)
    elector = any(x is not None for x in (h_total, h_direct, h_grass, h_exempt, h_nontax))
    h_lobby = h_total if h_total is not None else (h_direct or 0.0) + (h_grass or 0.0) if elector else None
    b_inds = {k: ind(sc.get(k)) for k in II_B_IND}
    b_any = any(v == 1 for v in b_inds.values())
    b_total = amount(sc, "TotalLobbyingExpendituresAmt")
    ii_b = any(v is not None for v in b_inds.values()) or b_total is not None
    part1 = {k: v for k, v in sc.items() if k.split("/")[-1].endswith(("Amt", "Cnt")) and not is_part_ii(k)}
    pol_amt = sum(num(v) or 0.0 for k, v in part1.items() if k.endswith("Amt"))
    not_c3 = ind(m.get("Organization501c3Ind")) != 1 and "Organization501cInd" in m
    if not_c3:
        status, lobby = "parsed_non_501c3", None
    elif elector and (h_lobby or 0) > 0:
        status, lobby = "lobby_501h", h_lobby
    elif ii_b and (b_any or (b_total or 0) > 0):
        status, lobby = "lobby_ii_b", b_total if b_total is not None else None
    elif elector:
        status, lobby = "none_501h_zero", 0.0
    elif ii_b:
        status, lobby = "none_ii_b_all_no", 0.0
    elif iv4 == 1:
        status, lobby = "lobby_part_iv_only", None
    elif iv4 == 0 or (form == "990EZ" and not ret.get("sched_c_present")):
        status, lobby = "none_part_iv_no", 0.0
    else:
        status, lobby = "parsed_no_lobby_data", None
    ratio = (lobby / exp) if (lobby is not None and exp and exp > 0) else (0.0 if lobby == 0 else None)
    return {"status": status, "reports_lobbying": int(status.startswith("lobby_")), "elector_501h": int(elector),
            "lobbying_usd": lobby, "total_expenses_usd": exp, "lobby_to_expenses": ratio,
            "lobby_to_nontaxable_501h": (h_lobby / h_nontax) if elector and h_nontax and h_lobby is not None else None,
            "ii_b_yes_count": sum(1 for v in b_inds.values() if v == 1),
            "ii_b_grants_other_orgs": int(b_inds.get("GrantsOtherOrganizationsInd") == 1),
            "ii_b_direct_contact": int(b_inds.get("DirectContactLegislatorsInd") == 1),
            "part_iv_line3_political": iv3, "part_iv_line4_lobbying": iv4,
            "sched_c_part_i_amount_usd": pol_amt, "sched_c_part_i_keys": sorted(part1),
            "political_reported": int(iv3 == 1 or pol_amt > 0),
            "not_c3": int(not_c3)}


def recipient_record(ein: str, chosen: Mapping | None, ret: Mapping | None, bmf: Mapping) -> dict:
    if chosen is None:
        return {"status": no_return_status(ein, bmf, bmf.get(ein, {}).get("name", "")), "form": "", "period": None, "oid": ""}
    base = {"form": chosen["form"], "period": chosen["period"], "oid": chosen["oid"]}
    if chosen["form"] == "990PF":
        return {**base, "status": "no_sched_c_990pf"}
    if not ret or ret.get("status") != "ok":
        return {**base, "status": "fetch_or_parse_failed", "fetch_status": (ret or {}).get("status", "")}
    return {**base, **classify_return(ret, chosen["form"]), "sched_c_present": int(bool(ret.get("sched_c_present"))),
            "tax_period_end": ret.get("hdr", {}).get("TaxPeriodEndDt", "")}


# ----------------------------------------------------------------------------- aggregate (pure)
COVERED = ("lobby_501h", "lobby_ii_b", "lobby_part_iv_only", "none_501h_zero", "none_ii_b_all_no", "none_part_iv_no")


def agg_cell(lines: Sequence[Mapping], rec: Mapping) -> dict:
    tot = sum(l["amount"] for l in lines)
    by_status = {}
    for l in lines:
        s = rec.get(l["ein"], {}).get("status", "blank_ein" if not l["ein"] else "not_selected")
        by_status[s] = by_status.get(s, 0.0) + l["amount"]
    cov = sum(by_status.get(s, 0.0) for s in COVERED)
    lob = sum(by_status.get(s, 0.0) for s in COVERED if s.startswith("lobby_"))
    eins = {l["ein"] for l in lines if l["ein"]}
    cov_eins = {e for e in eins if rec.get(e, {}).get("status") in COVERED}
    lob_eins = {e for e in cov_eins if rec[e]["status"].startswith("lobby_")}
    bins = {}
    for l in lines:
        r = rec.get(l["ein"], {})
        if r.get("status") in COVERED:
            b = bin_of(r.get("lobby_to_expenses"))
            bins[b] = bins.get(b, 0.0) + l["amount"]
    c3 = lambda l: rec.get(l["ein"], {}).get("status") in COVERED  # noqa: E731
    pol = sum(l["amount"] for l in lines if c3(l) and rec[l["ein"]].get("political_reported") == 1)
    pol_iv3 = sum(l["amount"] for l in lines if c3(l) and rec[l["ein"]].get("part_iv_line3_political") == 1)
    nonc3 = [l for l in lines if rec.get(l["ein"], {}).get("status") == "parsed_non_501c3"]
    elect = sum(l["amount"] for l in lines if rec.get(l["ein"], {}).get("status") in COVERED and rec[l["ein"]].get("elector_501h") == 1)
    lob_usd_known = [(l["amount"], rec[l["ein"]]["lobby_to_expenses"]) for l in lines
                     if rec.get(l["ein"], {}).get("status") in COVERED and rec[l["ein"]].get("lobby_to_expenses") is not None]
    wavg = (sum(a * r for a, r in lob_usd_known) / sum(a for a, _ in lob_usd_known)) if lob_usd_known else None
    lk = [(a, r) for a, r in lob_usd_known if r > 0]
    wavg_lob = (sum(a * r for a, r in lk) / sum(a for a, _ in lk)) if lk else None
    return {"net_usd": tot, "covered_usd": cov, "coverage_share": cov / tot if tot else None,
            "lobbying_usd_to": lob, "lobbying_share_of_covered": lob / cov if cov else None,
            "lobbying_share_of_net_lower_bound": lob / tot if tot else None,
            "elector_501h_share_of_covered": elect / cov if cov else None,
            "political_reported_usd": pol, "part_iv_line3_yes_usd": pol_iv3,
            "non_501c3_parsed_usd": sum(l["amount"] for l in nonc3),
            "non_501c3_political_usd": sum(l["amount"] for l in nonc3 if rec[l["ein"]].get("political_reported") == 1),
            "dollar_weighted_mean_intensity": wavg, "dollar_weighted_mean_intensity_lobbying_only": wavg_lob,
            "recipients": len(eins), "recipients_covered": len(cov_eins), "recipients_lobbying": len(lob_eins),
            "recipient_count_share_lobbying": len(lob_eins) / len(cov_eins) if cov_eins else None,
            "by_status": {k: round(v) for k, v in sorted(by_status.items(), key=lambda kv: -kv[1])},
            "intensity_bins_usd": {lbl: round(bins.get(lbl, 0.0)) for _, _, lbl in BINS} | {"unknown_amount": round(bins.get("unknown_amount", 0.0))}}


AGG_FIELDS = ("record_type", "scope", "scope_type", "fiscal_year", "ntee_major_group", "metric", "net_usd", "covered_usd",
              "coverage_share", "lobbying_usd_to", "lobbying_share_of_covered", "lobbying_share_of_net_lower_bound",
              "elector_501h_share_of_covered", "political_reported_usd", "part_iv_line3_yes_usd", "non_501c3_parsed_usd",
              "non_501c3_political_usd",
              "dollar_weighted_mean_intensity", "dollar_weighted_mean_intensity_lobbying_only", "recipients", "recipients_covered", "recipients_lobbying",
              "recipient_count_share_lobbying", "bin_or_status", "bin_usd", "bin_share_of_covered")
REC_FIELDS = ("ein", "object_id", "return_form_code", "tax_period_yyyymm", "status_code", "sector_code", "net_daf_grant_usd",
              "net_usd_fy2023", "net_usd_fy2024", "net_usd_national", "net_usd_community_foundation",
              "net_usd_single_issue", "net_usd_other_segments", "reports_lobbying", "elector_501h", "lobbying_usd",
              "total_expenses_usd", "lobby_to_expenses", "lobby_to_nontaxable_501h", "ii_b_yes_count",
              "ii_b_grants_other_orgs", "ii_b_direct_contact", "part_iv_line3_political", "part_iv_line4_lobbying",
              "sched_c_part_i_amount_usd", "political_reported")
FIELDS = AGG_FIELDS + tuple(f for f in REC_FIELDS if f not in AGG_FIELDS)


def scopes(panel: Mapping, top10: frozenset) -> list:
    seg = lambda s: (lambda e: panel[e]["segment"] == s)  # noqa: E731
    not_uh = lambda e: panel[e]["segment"] != "university_hospital"  # noqa: E731
    every = lambda r: True  # noqa: E731
    return ([("all_top50_itemising", "all", lambda e: True, every),
             ("all_ex_university_hospital", "all", not_uh, every),
             ("all_ex_uh_ex_top10_recipients", "sensitivity", not_uh, lambda r: r["ein"] not in top10)]
            + [(s, "segment", seg(s), every) for s in ("national", "community_foundation", "single_issue", "processor",
                                                        "university_hospital")]
            + [("community_foundation_ex_svcf", "segment",
                lambda e: panel[e]["segment"] == "community_foundation" and e != RS.SVCF, every)])


def aggregate_rows(ann: Mapping, panel: Mapping, rec: Mapping, top10: frozenset) -> tuple[list, dict]:
    rows, summ = [], {}
    fyk = [(str(fy), (fy,)) for fy in FYS] + [("2023-2024", FYS)]
    for name, stype, pred, lpred in scopes(panel, top10):
        for fy_label, fys in fyk:
            lines = [r for k, rs in ann.items() if pred(k[0]) and k[1] in fys for r in rs if not r["d2d"] and lpred(r)]
            if not lines:
                continue
            groups = [("ALL", lines)] + sorted(_group_by_fast(lines, lambda r: r["group"]).items())
            for g, ls in groups:
                c = agg_cell(ls, rec)
                base = {"record_type": "aggregate", "scope": name, "scope_type": stype, "fiscal_year": fy_label,
                        "ntee_major_group": g}
                rows.append({**base, "metric": "summary", **{k: v for k, v in c.items() if k in AGG_FIELDS}})
                if g == "ALL" or fy_label == "2023-2024":
                    cov = c["covered_usd"]
                    rows.extend({**base, "metric": "intensity_bin", "bin_or_status": lbl, "bin_usd": v,
                                 "bin_share_of_covered": v / cov if cov else None}
                                for lbl, v in c["intensity_bins_usd"].items())
                    rows.extend({**base, "metric": "status", "bin_or_status": s, "bin_usd": v,
                                 "bin_share_of_covered": v / c["net_usd"] if c["net_usd"] else None}
                                for s, v in c["by_status"].items())
                if fy_label == "2023-2024" and (g == "ALL" or name in ("all_ex_university_hospital", "national",
                                                                       "community_foundation", "single_issue")):
                    summ.setdefault(name, {})[g] = {k: (round(v, 4) if isinstance(v, float) and abs(v) < 10 else
                                                        round(v) if isinstance(v, float) else v) for k, v in c.items()}
    return rows, summ


def recipient_rows(rtot: Mapping, rec: Mapping, sel: frozenset) -> list:
    def r(e):
        d, x = rtot[e], rec[e]
        fy = d["by_fy"]
        seg = d["by_seg"]
        other = sum(v for s, v in seg.items() if s not in ("national", "community_foundation", "single_issue"))
        return {"record_type": "recipient", "ein": e, "object_id": x.get("oid", ""),
                "return_form_code": FORM_CODE.get(x.get("form", ""), 0), "tax_period_yyyymm": x.get("period") or "",
                "status_code": STATUS_CODE[x["status"]], "sector_code": SECTOR_CODE.get(d["group"], ""),
                "net_daf_grant_usd": round(d["total"]), "net_usd_fy2023": round(fy.get(2023, 0.0)),
                "net_usd_fy2024": round(fy.get(2024, 0.0)), "net_usd_national": round(seg.get("national", 0.0)),
                "net_usd_community_foundation": round(seg.get("community_foundation", 0.0)),
                "net_usd_single_issue": round(seg.get("single_issue", 0.0)), "net_usd_other_segments": round(other),
                **{k: (round(x[k]) if isinstance(x.get(k), float) and k.endswith("usd") else x.get(k, ""))
                   for k in ("reports_lobbying", "elector_501h", "lobbying_usd", "total_expenses_usd", "lobby_to_expenses",
                             "lobby_to_nontaxable_501h", "ii_b_yes_count", "ii_b_grants_other_orgs", "ii_b_direct_contact",
                             "part_iv_line3_political", "part_iv_line4_lobbying", "sched_c_part_i_amount_usd",
                             "political_reported")}}
    return [r(e) for e in sorted(sel, key=lambda e: -rtot[e]["total"])]


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--irs-dir", required=True, help="dir with index_2021.csv .. index_2026.csv")
    ap.add_argument("--ret-cache", required=True, help="parsed recipient-return JSON cache")
    ap.add_argument("--xml-dir", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--share-all", type=float, default=0.85)
    ap.add_argument("--share-seg", type=float, default=0.80)
    ap.add_argument("--select-only", action="store_true")
    ap.add_argument("--sens-n", type=int, default=1500, help="top-N recipients for the return-year sensitivity")
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen_sy = pick_returns(load_np(a.np_cache))
    sy = {(e, fy): chosen_sy[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen_sy}
    item = {k: x for k, x in sy.items() if itemized(x)}
    loaded = {k: RS.load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: v for k, v in loaded.items() if v["status"] == "ok"}
    wl = read_csv(RS.WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    names = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in names.items() if k and len(v) == 1}
    eins_all = frozenset(l[0] for v in good.values() for l in v["lines"] if l[0])
    bmf_s = RS.load_bmf(a.bmf_dir, eins_all)
    ann = {k: RS.annotate(k[0], v["lines"], bmf_s, wl_eins, wl_names) for k, v in good.items()}

    rtot = recipient_totals(ann, panel)
    net_total = sum(r["amount"] for rs in ann.values() for r in rs if not r["d2d"])
    sel = select_targets(rtot, a.share_all, a.share_seg)
    sel_usd = sum(rtot[e]["total"] for e in sel)
    print(f"sponsor-years {len(good)}; net ${net_total/1e9:.2f}bn; recipients {len(rtot)}; selected {len(sel)} "
          f"(${sel_usd/1e9:.2f}bn, {sel_usd/net_total:.3f})", file=sys.stderr)

    idx = load_index(a.irs_dir, sel)
    choice = {e: choose_return(idx.get(e, ())) for e in sel}
    bmf_f = load_bmf_filing(a.bmf_dir, sel)
    todo = sorted({c["oid"] for c in choice.values() if c and c["form"] in ("990", "990EZ")})
    print(f"in index (TY2021+): {sum(1 for c in choice.values() if c)}; returns to parse {len(todo)}", file=sys.stderr)
    if a.select_only:
        return 0

    def one(oid):
        return oid, load_return(oid, a.ret_cache, a.xml_dir, a.fetch)
    rets, t0 = {}, time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for i, (oid, r) in enumerate(ex.map(one, todo)):
            rets[oid] = r
            if i % 1000 == 999:
                print(f"  {i+1}/{len(todo)} {time.time()-t0:.0f}s", file=sys.stderr)

    rec = {e: recipient_record(e, choice[e], rets.get(choice[e]["oid"]) if choice[e] else None, bmf_f) for e in sel}
    top10 = frozenset(sorted(rtot, key=lambda e: -sum(v for s_, v in rtot[e]["by_seg"].items()
                                                         if s_ != "university_hospital"))[:10])
    rows, summ = aggregate_rows(ann, panel, rec, top10)
    write_csv(OUT, rows + recipient_rows(rtot, rec, sel), FIELDS)

    covered = [e for e in sel if rec[e]["status"] in COVERED]
    # return-year sensitivity: the latest 2023-period return (period end 2023-01..2023-12) of the top-N covered recipients
    alt = {}
    for e in sorted(covered, key=lambda e: -rtot[e]["total"])[:a.sens_n]:
        c = [r for r in idx.get(e, ()) if 202301 <= r["period"] <= 202312 and r["form"] in ("990", "990EZ")]
        if c and rec[e]["period"] // 100 != 2023:
            alt[e] = max(c, key=lambda r: (0 if r["form"] == "990EZ" else 1, int(r["oid"])))
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        alt_ret = dict(ex.map(one, sorted({c["oid"] for c in alt.values()})))
    alt_rec = {e: recipient_record(e, c, alt_ret.get(c["oid"]), bmf_f) for e, c in alt.items()}
    pair = [e for e in alt if alt_rec[e]["status"] in COVERED]
    agree = [e for e in pair if alt_rec[e]["reports_lobbying"] == rec[e]["reports_lobbying"]]
    sens = {"compared": len(pair), "compared_usd": round(sum(rtot[e]["total"] for e in pair)),
            "agree": len(agree), "agree_usd_share": round(sum(rtot[e]["total"] for e in agree) / max(1.0, sum(rtot[e]["total"] for e in pair)), 4),
            "lobby_2024_not_2023": sum(1 for e in pair if rec[e]["reports_lobbying"] == 1 and alt_rec[e]["reports_lobbying"] == 0),
            "lobby_2023_not_2024": sum(1 for e in pair if rec[e]["reports_lobbying"] == 0 and alt_rec[e]["reports_lobbying"] == 1),
            "lobby_share_usd_chosen": round(sum(rtot[e]["total"] for e in pair if rec[e]["reports_lobbying"] == 1) / max(1.0, sum(rtot[e]["total"] for e in pair)), 4),
            "lobby_share_usd_2023_returns": round(sum(rtot[e]["total"] for e in pair if alt_rec[e]["reports_lobbying"] == 1) / max(1.0, sum(rtot[e]["total"] for e in pair)), 4),
            "median_abs_intensity_diff_both_lobby": (lambda xs: xs[len(xs) // 2] if xs else None)(sorted(
                abs(rec[e]["lobby_to_expenses"] - alt_rec[e]["lobby_to_expenses"]) for e in pair
                if rec[e]["reports_lobbying"] == 1 and alt_rec[e]["reports_lobbying"] == 1
                and rec[e].get("lobby_to_expenses") is not None and alt_rec[e].get("lobby_to_expenses") is not None))}
    el = [e for e in covered if rec[e].get("elector_501h") == 1]
    over = [e for e in el if (rec[e].get("lobby_to_nontaxable_501h") or 0) > 1]
    over_entry = [e for e in over if (lambda sc: (amount(sc, II_A_EXEMPT) or 0) <= (amount(sc, II_A_TOTAL) or 0) * 1.0001)(rets[rec[e]["oid"]].get("sched_c", {}))]
    lob_r = [rec[e]["lobby_to_expenses"] for e in covered if rec[e]["status"].startswith("lobby_") and rec[e].get("lobby_to_expenses") is not None]
    count_bins = {lbl: sum(1 for x in lob_r if bin_of(x) == lbl) for _, _, lbl in BINS[1:]}
    pol_all = [e for e in covered if rec[e].get("political_reported") == 1]
    pol_detail = {"recipients": len(pol_all), "usd": round(sum(rtot[e]["total"] for e in pol_all)),
                  "part_iv_line3_yes": sum(1 for e in pol_all if rec[e].get("part_iv_line3_political") == 1),
                  "part_iv_line3_yes_usd": round(sum(rtot[e]["total"] for e in pol_all if rec[e].get("part_iv_line3_political") == 1)),
                  "part_i_amount_positive": sum(1 for e in pol_all if (rec[e].get("sched_c_part_i_amount_usd") or 0) > 0),
                  "both": sum(1 for e in pol_all if rec[e].get("part_iv_line3_political") == 1 and (rec[e].get("sched_c_part_i_amount_usd") or 0) > 0),
                  "part_i_amount_sum": round(sum(rec[e].get("sched_c_part_i_amount_usd") or 0 for e in pol_all)),
                  "part_i_amount_median": (lambda xs: xs[len(xs) // 2] if xs else None)(sorted(rec[e]["sched_c_part_i_amount_usd"] for e in pol_all if (rec[e].get("sched_c_part_i_amount_usd") or 0) > 0)),
                  "section4955_tax_positive": sum(1 for e in pol_all if any(k.startswith("Section4955") and (num(rets[rec[e]["oid"]]["sched_c"].get(k)) or 0) > 0 for k in rets[rec[e]["oid"]]["sched_c"])),
                  "also_reports_lobbying": sum(1 for e in pol_all if rec[e]["reports_lobbying"] == 1),
                  "covered_recipients": len(covered), "covered_usd": round(sum(rtot[e]["total"] for e in covered))}
    p1_keys = {}
    for e in covered:
        for k in rec[e].get("sched_c_part_i_keys", ()):
            p1_keys[k] = p1_keys.get(k, 0) + 1
    lob = [e for e in covered if rec[e]["status"].startswith("lobby_")]
    top_int = sorted((e for e in lob if rec[e].get("lobby_to_expenses") is not None), key=lambda e: -rtot[e]["total"])
    ratios = sorted(rec[e]["lobby_to_expenses"] for e in lob if rec[e].get("lobby_to_expenses") is not None)
    q = lambda p: ratios[min(len(ratios) - 1, int(p * len(ratios)))] if ratios else None  # noqa: E731
    pol = sorted((e for e in covered if rec[e].get("political_reported") == 1), key=lambda e: -rtot[e]["total"])
    summary = {
        "sponsor_years": len(good), "net_usd_all": round(net_total), "recipients_with_ein": len(rtot),
        "blank_ein_net_usd": round(sum(r["amount"] for rs in ann.values() for r in rs if not r["d2d"] and not r["ein"])),
        "selected": len(sel), "selected_usd": round(sel_usd), "selected_share": round(sel_usd / net_total, 4),
        "returns_parsed": sum(1 for r in rets.values() if r.get("status") == "ok"),
        "via": {s: sum(1 for r in rets.values() if r.get("via") == s) for s in ("local", "mirror")},
        "fetch_failures": {s: sum(1 for r in rets.values() if r.get("status") == s) for s in {r.get("status") for r in rets.values()} if s != "ok"},
        "status_counts_selected": {s: sum(1 for e in sel if rec[e]["status"] == s) for s in STATUS_CODE},
        "status_usd_selected": {s: round(sum(rtot[e]["total"] for e in sel if rec[e]["status"] == s)) for s in STATUS_CODE},
        "period_mix_parsed": {str(p): n for p, n in sorted(((p, sum(1 for e in covered if rec[e]["period"] // 100 == p)) for p in range(2021, 2027)))},
        "form_mix_covered": {f: sum(1 for e in covered if rec[e]["form"] == f) for f in ("990", "990EZ")},
        "lobbying_recipients": len(lob), "electors_501h_covered": sum(1 for e in covered if rec[e].get("elector_501h") == 1),
        "electors_501h_lobbying": sum(1 for e in lob if rec[e].get("elector_501h") == 1),
        "intensity_quantiles_lobbying_recipients": {p: q(p) for p in (0.1, 0.25, 0.5, 0.75, 0.9, 0.99)},
        "elector_ratio_to_nontaxable_quantiles": (lambda xs: {p: xs[min(len(xs) - 1, int(p * len(xs)))] for p in (0.5, 0.9, 0.99)} if xs else {})(
            sorted(rec[e]["lobby_to_nontaxable_501h"] for e in lob if rec[e].get("lobby_to_nontaxable_501h") is not None)),
        "elector_over_nontaxable": len(over), "elector_over_nontaxable_exempt_le_lobbying_entry": len(over_entry),
        "electors_covered": len(el), "lobbying_recipient_count_bins": count_bins, "political_detail": pol_detail,
        "return_year_sensitivity": sens, "top10_excluded_usd": round(sum(rtot[e]["total"] for e in top10)),
        "part_i_keys_seen": p1_keys,
        "main_keys_seen_by_form": {f: (lambda ks: {k: ks.count(k) for k in sorted(set(ks))})(
            [k for e in covered if rec[e]["form"] == f for k in rets[rec[e]["oid"]].get("main", {})]) for f in ("990", "990EZ")},
        "sched_c_keys_seen_990ez": (lambda ks: {k: ks.count(k) for k in sorted(set(ks))})(
            [k for e in covered if rec[e]["form"] == "990EZ" for k in rets[rec[e]["oid"]].get("sched_c", {})]),
        "political_reported": [{"ein": e, "net_usd": round(rtot[e]["total"]), "iv3": rec[e].get("part_iv_line3_political"),
                                "part_i_usd": rec[e].get("sched_c_part_i_amount_usd"), "keys": rec[e].get("sched_c_part_i_keys"),
                                "not_c3": rec[e].get("not_c3"), "name": bmf_f.get(e, {}).get("name", "")} for e in pol[:40]],
        "political_reported_count": len(pol),
        "not_c3_covered": sum(1 for e in covered if rec[e].get("not_c3") == 1),
        "non_c3_parsed": (lambda xs: {"recipients": len(xs), "usd": round(sum(rtot[e]["total"] for e in xs)),
                                      "political_reported": sum(1 for e in xs if rec[e].get("political_reported") == 1),
                                      "political_reported_usd": round(sum(rtot[e]["total"] for e in xs if rec[e].get("political_reported") == 1)),
                                      "bmf_subsections": {s_: sum(1 for e in xs if bmf_f.get(e, {}).get("subsection") == s_)
                                                          for s_ in sorted({bmf_f.get(e, {}).get("subsection", "") for e in xs})}})(
            [e for e in sel if rec[e]["status"] == "parsed_non_501c3"]),
        "top20_lobbying_by_daf_usd": [{"ein": e, "name": bmf_f.get(e, {}).get("name", ""), "net_usd": round(rtot[e]["total"]),
                                       "lobby_usd": rec[e]["lobbying_usd"], "ratio": round(rec[e]["lobby_to_expenses"], 5),
                                       "h": rec[e]["elector_501h"], "group": rtot[e]["group"]} for e in top_int[:20]],
        "top20_by_intensity_min_1m": [{"ein": e, "name": bmf_f.get(e, {}).get("name", ""), "net_usd": round(rtot[e]["total"]),
                                       "ratio": round(rec[e]["lobby_to_expenses"], 4), "h": rec[e]["elector_501h"], "group": rtot[e]["group"]}
                                      for e in sorted((e for e in top_int if rtot[e]["total"] >= 1e6), key=lambda e: -rec[e]["lobby_to_expenses"])[:20]],
        "agg": summ,
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
