#!/usr/bin/env python3
"""Recipient-side follow-ups to P-B40N12-02: (A) DAF share on an individual-giving-like denominator (P-B40N1202-03)
and (B) the share of top-50 DAF grant dollars reaching recipients eligible for a Charity Navigator star rating under
its 2026 published rules (P-B43N26-02).

Shared numerator  Exactly as scripts/mission_daf_share_recipient_revenue.py (imported, not modified): top-50 DAFRC
                  sponsors by FY2024 DAF assets, FY2023-2024 Schedule I Part II lines (94 itemising sponsor-years),
                  totals rows dropped, DAF-to-DAF lines dropped, `daf_weighted` = each sponsor-year's lines x its DAF
                  share of grants (sponsor-cost-structure.csv, capped at 1).

(A) Same frame, same stratified sample (seed 20261119, 400 certainty + up to 40 per NTEE group x BMF band), same
    return choice (latest object id per tax period, latest period per FY 2023/2024). Each chosen return is re-read in
    full from the GivingTuesday mirror of IRS TEOS XML and Form 990 Part VIII lines 1a-1h are taken from the direct
    children of the IRS990 element:
        1a FederatedCampaignsAmt  1b MembershipDuesAmt  1c FundraisingAmt  1d RelatedOrganizationsAmt
        1e GovernmentGrantsAmt    1f AllOtherContributionsAmt  1g NoncashContributionsAmt  1h TotalContributionsAmt
    (direct children only: FundraisingAmt also occurs inside the Part IX expense groups). 990-EZ line 1
    (ContributionsGiftsGrantsEtcAmt) cannot be split and is used unchanged on every basis; a 990-only scope is
    reported. Bases (denominator over matched FYs):
        b1_1h            1h (reproduces the committed study)
        b2_1h_less_1e    1h - 1e (private contributions; committed sensitivity)
        b3_1abcf         1a + 1b + 1c + 1f = 1h - 1d - 1e (all non-government, non-related-organisation gifts)
        b4_1bcf          1b + 1c + 1f = 1h - 1a - 1d - 1e (queue-item definition)
        b5_1af           1a + 1f
        b6_1f            1f only (the line the IRS instructions assign DAF grants to)
    Recipients with a non-positive basis denominator are left out of that basis (counted in `den_nonpos_*`).
    Wave 33A corrections applied: EINs whose returns parse but carry no line 1h / EZ line 1 are out of scope (not
    missing); a sensitivity scope drops DAF sponsors outside the DAFRC panel that leak into the frame (Jewish
    federations, National Christian Foundation affiliates, Navigation Charitable Fund); medians are not scaled.

(B) Universe: every top-50 FY2023-2024 non-DAF-to-DAF Schedule I line with a positive amount (blank-EIN lines kept,
    split foreign / domestic by the line's address). Charity Navigator 2026 rules applied from filing data:
        - U.S. 501(c)(3) public charity: in the IRS EO BMF, SUBSECTION 03, FOUNDATION not 02/03/04;
        - DAF sponsors: CN's 2024-04-08 release note says "DAFs were determined to be ineligible". Central reading:
          DAFRC 2025 panel EINs in the national and donation-processor segments are ineligible; `strict` also
          excludes community foundations; `lenient` applies the filing rules to every panel EIN (universities,
          hospitals and single-issue charities that sponsor DAFs are never excluded on this ground in the central
          reading);
        - >= 3 e-filed Form 990-series returns (990, 990-EZ, 990-PF; distinct tax periods, amendments collapsed) with
          a tax period ending 2020-2025 ("within the past six years"); sensitivity: IRS index (processing) year
          2021-2026;
        - >= 2 of the 4 most recent returns are the full Form 990; the most recent is not a 990-PF.
    Form type comes from the DLN prefix (93493 = 990, 93492 = 990-EZ, 93491 = 990-PF), which also resolves the
    2019-2020 index labels 990O / 990EO / 990PR. The expense rule (functional expenses > 0, program <= total) is
    tested on the (A) sample's returns only. "Giving Not Recommended" alerts and CN's own receipt of filings are
    not observable. No ratings are read.

Pure functions; I/O only in fetch/load helpers and `main`. Stdlib only.

Usage:
  python3 scripts/mission_recipient_basis_eligibility.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --index-dir IRSDIR --f990-cache DIR [--fetch] [--boot 500]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_share_recipient_revenue import (BANDS, GROUPS, INTERMEDIARY_NAME, NETTED_CSV, band_of,  # noqa: E402
                                                  choose_filings, coverage_fy, draw_sample, exclusion, group_of,
                                                  load_bmf, numerators, sponsor_weights, wquantile)
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import COST, WHITELIST, annotate, load_lines  # noqa: E402

OUT_A = os.path.join(DATA, "daf-share-individual-basis-2026-11-19.csv")
OUT_B = os.path.join(DATA, "charity-rating-eligibility-share-2026-11-19.csv")
HIST_YEARS = tuple(range(2019, 2027))
P8_V = 1
UA = "research-script/1.0"
DLN_FORM = {"93493": "990", "93492": "990EZ", "93491": "990PF"}
WINDOW_TY = (2020, 2025)
WINDOW_IDX = (2021, 2026)
PF_CODES = frozenset({"02", "03", "04"})
LEAKED_SPONSOR = re.compile(r"\b(JEWISH FEDERATIONS?|UJA|JEWISH UNITED FUND|COMBINED JEWISH PHILANTHROPIES|"
                            r"NATIONAL CHRISTIAN|NAVIGATION CHARITABLE)\b")
P8_FIELDS = {"FederatedCampaignsAmt": "l1a", "MembershipDuesAmt": "l1b", "FundraisingAmt": "l1c",
             "RelatedOrganizationsAmt": "l1d", "GovernmentGrantsAmt": "l1e", "AllOtherContributionsAmt": "l1f",
             "NoncashContributionsAmt": "l1g", "TotalContributionsAmt": "l1h", "CYTotalRevenueAmt": "total_revenue",
             "CYTotalExpensesAmt": "total_expenses"}
EZ_FIELDS = {"ContributionsGiftsGrantsEtcAmt": "ez_l1", "TotalRevenueAmt": "total_revenue",
             "TotalExpensesAmt": "total_expenses", "TotalProgramServiceExpensesAmt": "program_expenses"}
LINES = ("l1a", "l1b", "l1c", "l1d", "l1e", "l1f", "l1g", "l1h")
BASES = (("b1_1h", lambda d: d["l1h"]),
         ("b2_1h_less_1e", lambda d: d["l1h"] - d["l1e"]),
         ("b3_1abcf", lambda d: d["l1a"] + d["l1b"] + d["l1c"] + d["l1f"]),
         ("b4_1bcf", lambda d: d["l1b"] + d["l1c"] + d["l1f"]),
         ("b5_1af", lambda d: d["l1a"] + d["l1f"]),
         ("b6_1f", lambda d: d["l1f"]))
SRC_A = ("Numerator: top-50 DAFRC sponsors' IRS Form 990 Schedule I Part II lines FY2023-24, net of DAF-to-DAF, "
         "DAF-weighted (as mission_daf_share_recipient_revenue.py). Denominator: recipient Form 990 Part VIII lines "
         "1a-1h / 990-EZ line 1 (GivingTuesday mirror of IRS TEOS XML; returns located via "
         "apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv). Line definitions: www.irs.gov/instructions/i990.")
SRC_B = ("Dollars: top-50 DAFRC sponsors' Schedule I Part II lines FY2023-24, net of DAF-to-DAF. Eligibility: Charity "
         "Navigator rules (intercom.help/charity-navigator/en/articles/8557824, 2026-04-09) applied to the IRS TEOS "
         "e-file index 2019-2026 (form type by DLN prefix) and the IRS EO BMF (SUBSECTION, FOUNDATION, NTEE_CD, "
         "REVENUE_AMT).")


# ----------------------------------------------------------------------------- numerator (as the committed study)
def build_numerator(a) -> dict:
    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    present = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen}
    item = {k: x for k, x in present.items() if itemized(x)}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    groups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in groups.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    weights = sponsor_weights(read_csv(COST), good)
    return {"dafrc": dafrc, "panel": panel, "ann": ann, "weights": weights, "nums": numerators(ann, weights),
            "sponsor_years": len(good)}


def no_ein_lines(ann: Mapping, weights: Mapping) -> dict:
    """Blank-EIN, non-DAF-to-DAF, positive lines -> key -> {si, dw, foreign}."""
    flat = tuple((r["key"], r["where"].startswith("F:"), r["amount"], r["amount"] * weights.get(k, 1.0))
                 for k, rs in ann.items() for r in rs if not r["ein"] and not r["d2d"] and r["amount"] > 0)
    by = _group_by_fast(flat, lambda t: t[0])
    return {key: {"si": sum(t[2] for t in v), "dw": sum(t[3] for t in v), "foreign": any(t[1] for t in v)}
            for key, v in by.items()}


# ----------------------------------------------------------------------------- filing history (IRS TEOS index)
def load_history(index_dir: str, eins: frozenset) -> dict:
    def rows(y):
        p = os.path.join(index_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            return ()
        with open(p, encoding="utf-8", errors="replace", newline="") as fh:
            return tuple({"ein": ein9(d["EIN"]), "tax_period": d["TAX_PERIOD"], "form": DLN_FORM[d["DLN"][:5]],
                          "return_type": d["RETURN_TYPE"], "oid": d["OBJECT_ID"], "index_year": y}
                         for d in csv.DictReader(fh)
                         if (d.get("DLN") or "")[:5] in DLN_FORM and ein9(d.get("EIN", "")) in eins)
    return _group_by_fast((r for y in HIST_YEARS for r in rows(y)), lambda r: r["ein"])


def per_period(filings: Sequence[Mapping]) -> tuple[dict, ...]:
    """Latest object id per tax period (amendments supersede), newest period first."""
    per = {tp: max(v, key=lambda r: r["oid"]) for tp, v in _group_by_fast(filings, lambda r: r["tax_period"]).items()}
    return tuple(sorted(per.values(), key=lambda r: r["tax_period"], reverse=True))


def cn_filing_test(filings: Sequence[Mapping], window: str = "tax_year") -> dict:
    periods = per_period(filings)
    lo, hi = WINDOW_TY if window == "tax_year" else WINDOW_IDX
    in_win = tuple(p for p in periods if lo <= (int(p["tax_period"][:4]) if window == "tax_year" else p["index_year"]) <= hi)
    last4 = periods[:4]
    return {"n_periods": len(periods), "n_in_window": len(in_win), "n_full_990_last4": sum(p["form"] == "990" for p in last4),
            "latest_form": periods[0]["form"] if periods else "", "latest_tp": periods[0]["tax_period"] if periods else "",
            "forms_last4": ";".join(p["form"] for p in last4)}


DAF_RULES = {"lenient": frozenset(),
             "national": frozenset({"national", "processor"}),
             "national_cf": frozenset({"national", "processor", "community_foundation"})}


def cn_reason(b: Mapping | None, daf_segment: str, t: Mapping, rule: str) -> str:
    """First failing Charity Navigator rule, or 'eligible'. Order: identity, status, DAF sponsor, filings.
    daf_segment: the recipient's DAFRC panel segment ('' when not a panel EIN); `rule` names which panel segments are
    read as the "DAFs" CN calls ineligible (DAF_RULES)."""
    if b is None:
        return "not_in_bmf"
    if b["subsection"] != "03":
        return "not_501c3"
    if b["foundation"] in PF_CODES:
        return "private_foundation"
    if daf_segment in DAF_RULES[rule]:
        return "daf_sponsor_" + ("community_foundation" if daf_segment == "community_foundation" else "national_or_processor")
    if t["n_periods"] == 0:
        return ("no_efiled_990_church" if b["foundation"] == "10"
                else "no_efiled_990_group_subordinate" if b.get("affiliation") in ("6", "9") or b.get("group", "0000") not in ("", "0000")
                else "no_efiled_990_other")
    if t["n_in_window"] < 3:
        return "fewer_than_3_efiled_in_6y"
    if t["latest_form"] == "990PF":
        return "latest_is_990pf"
    if t["n_full_990_last4"] < 2:
        return "fewer_than_2_full_990_in_latest_4" + ("_ez_filer" if "990EZ" in t["forms_last4"] else "")
    return "eligible"


def load_bmf_extra(bmf_dir: str, eins: frozenset) -> dict:
    """GROUP and AFFILIATION, which the committed load_bmf does not keep."""
    from mission_recipient_sectors import BMF_FILES

    def rows(f):
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple((ein9(r["EIN"]), {"group": (r.get("GROUP") or "").strip(), "affiliation": (r.get("AFFILIATION") or "").strip()})
                         for r in csv.DictReader(fh) if ein9(r["EIN"]) in eins)
    return dict(x for f in BMF_FILES for x in rows(f))


def load_revoked(index_dir: str, eins: frozenset) -> frozenset:
    """EINs on the IRS automatic-revocation list with no reinstatement date."""
    p = os.path.join(index_dir, "data-download-revocation.txt")
    if not os.path.exists(p):
        return frozenset()
    with open(p, encoding="latin-1") as fh:
        parts = (ln.rstrip("\r\n").split("|") for ln in fh)
        return frozenset(ein9(x[0]) for x in parts if len(x) >= 12 and ein9(x[0]) in eins and not x[11].strip())


# ----------------------------------------------------------------------------- (A) Part VIII reader
def parse_part8(stream) -> dict:
    """Stream the return; at the end of IRS990 / IRS990EZ read its direct children and stop."""
    try:
        for _, el in ET.iterparse(stream, events=("end",)):
            tag = local(el.tag)
            if tag in ("IRS990", "IRS990EZ"):
                fields = P8_FIELDS if tag == "IRS990" else EZ_FIELDS
                kids = {local(c.tag): c for c in el}
                vals = {v: num(kids[k].text) for k, v in fields.items() if k in kids and kids[k].text}
                tfe = kids.get("TotalFunctionalExpensesGrp")
                sub = {local(c.tag): num(c.text) for c in tfe} if tfe is not None else {}
                extra = ({"functional_expenses": sub.get("TotalAmt"), "program_expenses": sub.get("ProgramServicesAmt")}
                         if tag == "IRS990" else {})
                return {**vals, **extra, "form": tag, "status": "ok"}
    except ET.ParseError:
        return {"status": "parse_error"}
    return {"status": "no_main_form"}


def fetch_part8(oid: str, cache: str, fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == P8_V:
            return c
    if not fetch:
        return {"status": "not_fetched"}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    r = {"status": "error"}
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                r = parse_part8(resp)
            break
        except urllib.error.HTTPError as e:
            r = {"status": f"http_{e.code}"}
            if e.code in (403, 404):
                break
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            r = {"status": "error"}
            time.sleep(2 * (attempt + 1))
    obj = {**r, "oid": oid, "_v": P8_V}
    if r["status"] in ("ok", "http_404", "no_main_form", "parse_error"):
        os.makedirs(cache, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh)
    return obj


def lines_of(x: Mapping) -> dict | None:
    """-> 1a..1h for a parsed return (EZ: line 1 on every line slot that matters), or None without a contributions total."""
    if x.get("status") != "ok":
        return None
    if x["form"] == "IRS990EZ":
        v = x.get("ez_l1")
        return None if v is None else {**{k: 0.0 for k in LINES}, "l1f": v, "l1h": v, "ez": True}
    if x.get("l1h") is None:
        return None
    return {**{k: (x.get(k) or 0.0) for k in LINES}, "ez": False}


def recipient_a(s: Mapping, filings: Mapping, f990: Mapping) -> dict:
    parsed = {fy: f990.get(filings[fy]["oid"], {}) for fy in FYS if fy in filings}
    yrs = tuple(fy for fy, x in parsed.items() if lines_of(x) is not None)
    ln = {fy: lines_of(parsed[fy]) for fy in yrs}
    tot = {k: sum(ln[fy][k] for fy in yrs) for k in LINES}
    n_dw = sum(s["num"].get(fy, {}).get("dw", 0.0) for fy in yrs)
    any_fail = any(x.get("status") not in ("ok",) for x in parsed.values())
    status = ("no_fy2023_2024_990_or_ez_in_index" if not filings
              else "xml_not_read" if not yrs and any_fail and not any(x.get("status") == "ok" for x in parsed.values())
              else "no_contributions_line" if not yrs
              else "zero_or_negative_contributions" if tot["l1h"] <= 0 else "ok")
    dens = {b: fn(tot) for b, fn in BASES}
    forms = ";".join("IRS990EZ" if ln[fy]["ez"] else "IRS990" for fy in yrs)
    sum_ok = all(abs(sum(ln[fy][k] for k in LINES[:6]) - ln[fy]["l1h"]) <= 1 for fy in yrs if not ln[fy]["ez"])
    ratio = lambda a_, b_: (a_ / b_) if b_ and b_ > 0 else None  # noqa: E731
    return {"row_type": "recipient", "ein": s["ein"], "name": s["name"], "ntee_cd": s["ntee"], "ntee_major_group": s["group"],
            "revenue_band": s["band"], "stratum": s["stratum"], "stratum_N": s["N_h"], "years_matched": ";".join(map(str, yrs)),
            "forms": forms, "object_ids": ";".join(filings[fy]["oid"] for fy in yrs),
            "num_daf_weighted_matched": round(n_dw), **{f"{k}_matched": round(tot[k]) for k in LINES},
            "lines_sum_to_1h": sum_ok, "leaked_sponsor_name": bool(LEAKED_SPONSOR.search(s["name"].upper())),
            **{f"share_{b}": (ratio(n_dw, dens[b]) if status == "ok" else None) for b, _ in BASES},
            **{f"den_{b}": round(dens[b]) for b, _ in BASES}, "status": status, "source": SRC_A}


# ----------------------------------------------------------------------------- (A) statistics
def weights_a(rows: Sequence[Mapping]) -> dict:
    by = _group_by_fast(rows, lambda r: r["stratum"])
    return {k: v[0]["stratum_N"] / (len(v) - sum(r["status"] == "xml_not_read" for r in v))
            for k, v in by.items() if any(r["status"] == "ok" for r in v)}


def pooled(ok: Sequence[Mapping], w: Mapping, basis: str):
    use = tuple(r for r in ok if r[f"den_{basis}"] > 0)
    d = sum(w[r["stratum"]] * r[f"den_{basis}"] for r in use)
    return sum(w[r["stratum"]] * r["num_daf_weighted_matched"] for r in use) / d if d > 0 else None


def boot(ok: Sequence[Mapping], w: Mapping, basis: str, reps: int, seed: int) -> dict:
    if len(ok) < 10 or reps <= 0:
        return {}
    by = _group_by_fast(ok, lambda r: r["stratum"])
    rng = random.Random(seed)
    draws = tuple(tuple(x for k in sorted(by) for x in rng.choices(by[k], k=len(by[k]))) for _ in range(reps))
    key = f"share_{basis}"
    p = sorted(x for x in (pooled(d, w, basis) for d in draws) if x is not None)
    m = sorted(x for x in (wquantile([(r[key], w[r["stratum"]]) for r in d], 0.5) for d in draws) if x is not None)
    pct = lambda xs, q: xs[min(len(xs) - 1, int(q * len(xs)))] if xs else None  # noqa: E731
    return {"median_ci95_lo": pct(m, 0.025), "median_ci95_hi": pct(m, 0.975),
            "pooled_ci95_lo": pct(p, 0.025), "pooled_ci95_hi": pct(p, 0.975)}


def summary_a(scope_type: str, scope: str, basis: str, rows: Sequence[Mapping], w: Mapping, scale: float,
              reps: int, seed: int) -> dict:
    ok = tuple(r for r in rows if r["status"] == "ok")
    use = tuple(r for r in ok if r[f"den_{basis}"] > 0)
    wt = lambda r: w[r["stratum"]]  # noqa: E731
    key = f"share_{basis}"
    q = lambda p: wquantile([(r[key], wt(r)) for r in use], p)  # noqa: E731
    tw = sum(wt(r) for r in use)
    nonpos = tuple(r for r in ok if r[f"den_{basis}"] <= 0)
    pl = pooled(ok, w, basis)
    return {"row_type": "summary", "scope_type": scope_type, "scope": scope, "basis": basis, "sampled": len(rows),
            "respondents": len(use), "weighted_recipients": round(tw),
            "den_nonpos_respondents": len(nonpos), "den_nonpos_num_share": (
                sum(wt(r) * r["num_daf_weighted_matched"] for r in nonpos) / sum(wt(r) * r["num_daf_weighted_matched"] for r in ok)
                if ok and sum(r["num_daf_weighted_matched"] for r in ok) > 0 else None),
            "p25_share": q(0.25), "median_share": q(0.5), "p75_share": q(0.75), "pooled_share": pl,
            "share_ge_20pct": (sum(wt(r) for r in use if r[key] >= 0.2) / tw) if tw else None,
            "share_gt_100pct": (sum(wt(r) for r in use if r[key] > 1) / tw) if tw else None,
            **boot(use, w, basis, reps, seed), "scaled_pooled_inference": (pl / scale) if pl is not None else None,
            "source": SRC_A}


def build_a(rows: Sequence[Mapping], scale: float, reps: int, seed: int) -> list:
    w = weights_a(rows)
    not_interm = lambda r: not (r["ntee_cd"].startswith("T") or INTERMEDIARY_NAME.search(r["name"].upper()))  # noqa: E731
    scopes = ([("all", "all_ex_excluded", lambda r: True),
               ("sensitivity", "form_990_only", lambda r: r["forms"] and "IRS990EZ" not in r["forms"]),
               ("sensitivity", "ex_leaked_daf_sponsors", lambda r: not r["leaked_sponsor_name"]),
               ("sensitivity", "non_certainty_only", lambda r: r["stratum"] != "certainty"),
               ("sensitivity", "ex_ntee_T_and_fund_foundation_trust_names", not_interm)]
              + [("ntee_major_group", g, (lambda r, g=g: r["ntee_major_group"] == g)) for g in GROUPS]
              + [("revenue_band", b, (lambda r, b=b: r["revenue_band"] == b)) for _, _, b in BANDS])
    return [summary_a(st, sc, b, [r for r in rows if pred(r)], w, scale, reps, seed + 31 * i + j)
            for i, (st, sc, pred) in enumerate(scopes) for j, (b, _) in enumerate(BASES)]


# ----------------------------------------------------------------------------- (B) eligibility table
def units_b(nums: Mapping, blank: Mapping, bmf: Mapping, extra: Mapping, hist: Mapping, panel: Mapping) -> tuple[dict, ...]:
    panel_eins = frozenset(panel)

    def one(e, n):
        b = {**bmf[e], **extra.get(e, {})} if e in bmf else None
        fl = hist.get(e, ())
        t = cn_filing_test(fl, "tax_year")
        ti = cn_filing_test(fl, "index_year")
        return {"key": e, "si": sum(v["si"] for v in n["fy"].values()), "dw": sum(v["dw"] for v in n["fy"].values()),
                "group": group_of(b["ntee"]) if b else "not_in_bmf", "band": band_of(b["revenue"]) if b else "not_in_bmf",
                "type": (("daf_panel_" + panel[e]["segment"]) if e in panel else (exclusion(b, panel_eins) or "other_charity"))
                        if b else "not_in_bmf",
                "daf_segment": panel[e]["segment"] if e in panel else "",
                "reason": cn_reason(b, panel[e]["segment"] if e in panel else "", t, "national"),
                "reason_lenient": cn_reason(b, panel[e]["segment"] if e in panel else "", t, "lenient"),
                "reason_national_cf": cn_reason(b, panel[e]["segment"] if e in panel else "", t, "national_cf"),
                "reason_index_window": cn_reason(b, panel[e]["segment"] if e in panel else "", ti, "national"), **t}
    named = tuple(one(e, n) for e, n in nums.items())
    nob = tuple({"key": k, "si": v["si"], "dw": v["dw"], "group": "no_ein", "band": "no_ein", "type": "no_ein",
                 "reason": "no_ein_foreign" if v["foreign"] else "no_ein_domestic",
                 "reason_lenient": "no_ein_foreign" if v["foreign"] else "no_ein_domestic",
                 "reason_national_cf": "no_ein_foreign" if v["foreign"] else "no_ein_domestic", "daf_segment": "",
                 "reason_index_window": "no_ein_foreign" if v["foreign"] else "no_ein_domestic",
                 "n_periods": 0, "n_in_window": 0, "n_full_990_last4": 0, "latest_form": "", "latest_tp": "",
                 "forms_last4": ""} for k, v in blank.items())
    return named + nob


def share_rows(units: Sequence[Mapping], scope_type: str, scope: str, pred) -> list:
    sub = tuple(u for u in units if pred(u))
    tot_dw, tot_si, n = sum(u["dw"] for u in sub), sum(u["si"] for u in sub), len(sub)
    def row(metric, rk, val):
        hit = tuple(u for u in sub if u[rk] == val) if val != "*" else sub
        dw, si = sum(u["dw"] for u in hit), sum(u["si"] for u in hit)
        return {"row_type": "share", "scope_type": scope_type, "scope": scope, "rule_variant": metric, "category": val if val != "*" else "all",
                "recipients": len(hit), "recipient_share": len(hit) / n if n else None,
                "usd_daf_weighted_fy2023_2024": round(dw), "dollar_share_daf_weighted": dw / tot_dw if tot_dw else None,
                "usd_sched_i_fy2023_2024": round(si), "dollar_share_sched_i": si / tot_si if tot_si else None, "source": SRC_B}
    cats = sorted({u["reason"] for u in sub})
    return ([row("central_tax_year_window", "reason", "*")]
            + [row("central_tax_year_window", "reason", c) for c in cats]
            + [row("lenient_all_daf_sponsors_by_filings", "reason_lenient", "eligible"),
               row("strict_cfs_also_ineligible", "reason_national_cf", "eligible"),
               row("central_index_year_window", "reason_index_window", "eligible")])


def build_b(units: Sequence[Mapping]) -> list:
    types = sorted({u["type"] for u in units})
    groups = list(GROUPS) + ["not_in_bmf", "no_ein"]
    bands = [b for _, _, b in BANDS] + ["not_in_bmf", "no_ein"]
    return (share_rows(units, "all", "all_recipients", lambda u: True)
            + [r for t in types for r in share_rows(units, "recipient_type", t, lambda u, t=t: u["type"] == t)]
            + [r for g in groups for r in share_rows(units, "ntee_major_group", g, lambda u, g=g: u["group"] == g)]
            + [r for b in bands for r in share_rows(units, "revenue_band", b, lambda u, b=b: u["band"] == b)])


def expense_check(sample_rows: Sequence[Mapping], units_by: Mapping, hist: Mapping, f990: Mapping) -> dict:
    """Expense rule on the latest FY2023/24 full 990 read for sampled recipients that pass the filing rules."""
    def latest(e):
        xs = sorted((x for x in (f990.get(o) for o in (r["oid"] for r in per_period(hist.get(e, ())))) if x and x.get("form") == "IRS990"),
                    key=lambda x: x["oid"], reverse=True)
        return xs[0] if xs else None
    elig = tuple(s for s in sample_rows if units_by.get(s["ein"], {}).get("reason") == "eligible")
    lat = tuple((s, latest(s["ein"])) for s in elig)
    seen = tuple((s, x) for s, x in lat if x is not None)
    fail = tuple((s, x) for s, x in seen if not ((x.get("functional_expenses") or 0) > 0
                                                and (x.get("program_expenses") or 0) <= (x.get("functional_expenses") or 0)))
    return {"sampled_eligible": len(elig), "with_cached_full_990": len(seen), "fail_expense_rule": len(fail),
            "fail_examples": [{"ein": s["ein"], "name": s["name"][:40], "tfe": x.get("functional_expenses"),
                               "prog": x.get("program_expenses")} for s, x in fail[:10]]}


FIELDS_A = ("row_type", "scope_type", "scope", "basis", "sampled", "respondents", "weighted_recipients",
            "den_nonpos_respondents", "den_nonpos_num_share", "p25_share", "median_share", "median_ci95_lo",
            "median_ci95_hi", "p75_share", "pooled_share", "pooled_ci95_lo", "pooled_ci95_hi", "share_ge_20pct",
            "share_gt_100pct", "scaled_pooled_inference",
            "ein", "name", "ntee_cd", "ntee_major_group", "revenue_band", "stratum", "stratum_N", "years_matched", "forms",
            "object_ids", "num_daf_weighted_matched", *(f"{k}_matched" for k in LINES), "lines_sum_to_1h",
            "leaked_sponsor_name", *(f"den_{b}" for b, _ in BASES), *(f"share_{b}" for b, _ in BASES), "status", "source")
FIELDS_B = ("row_type", "scope_type", "scope", "rule_variant", "category", "recipients", "recipient_share",
            "usd_daf_weighted_fy2023_2024", "dollar_share_daf_weighted", "usd_sched_i_fy2023_2024", "dollar_share_sched_i",
            "source")


# ----------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; repo CLI convention)")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True)
    ap.add_argument("--f990-cache", required=True, help="cache of parsed Part VIII JSON (new; not the committed f990 cache)")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--seed", type=int, default=20261119)
    ap.add_argument("--per-stratum", type=int, default=40)
    ap.add_argument("--certainty", type=int, default=400)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--out-a", default=OUT_A)
    ap.add_argument("--out-b", default=OUT_B)
    a = ap.parse_args(argv)

    N = build_numerator(a)
    nums, panel_eins = N["nums"], frozenset(N["panel"])
    bmf = load_bmf(a.bmf_dir, frozenset(nums))
    universe = tuple({**bmf[e], "group": group_of(bmf[e]["ntee"]), "band": band_of(bmf[e]["revenue"]),
                      "num": dict(n["fy"]), "grantors": len(n["grantors"]),
                      "num_si_total": sum(v["si"] for v in n["fy"].values()),
                      "excl": exclusion(bmf[e], panel_eins)} for e, n in nums.items() if e in bmf)
    frame = tuple(u for u in universe if not u["excl"])
    sample = draw_sample(frame, a.certainty, a.per_stratum, a.seed)

    hist = load_history(a.index_dir, frozenset(nums))
    filings = {s["ein"]: choose_filings(tuple(r for r in hist.get(s["ein"], ()) if r["form"] in ("990", "990EZ")
                                              and r["index_year"] >= 2023 and r["return_type"] in ("990", "990EZ")))
               for s in sample}
    oids = sorted({f["oid"] for fs in filings.values() for f in fs.values()})
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        f990 = dict(zip(oids, ex.map(lambda o: fetch_part8(o, a.f990_cache, a.fetch), oids)))
    rec = [recipient_a(s, filings[s["ein"]], f990) for s in sample]

    cov24 = coverage_fy(N["ann"], N["weights"], 2024)
    net = {int(r["fiscal_year"]): num(r["netted_value"]) for r in read_csv(NETTED_CSV)
           if r["metric"] == "daf_grants" and r["tier"] == "central"}
    scale = cov24["daf_weighted_non_d2d"] / net[2024]
    summ_a = build_a(rec, scale, a.boot, a.seed)
    write_csv(a.out_a, summ_a + sorted(rec, key=lambda r: (r["stratum"] != "certainty", r["stratum"], r["ein"])), FIELDS_A)

    # (B)
    extra = load_bmf_extra(a.bmf_dir, frozenset(bmf))
    revoked = load_revoked(a.index_dir, frozenset(bmf))
    blank = no_ein_lines(N["ann"], N["weights"])
    # BMF rows are the IRS's current exempt list; the revocation list is a diagnostic only (an org revoked and later
    # re-recognised keeps its old revocation row without a reinstatement date), so it is not applied as a rule.
    units = units_b(nums, blank, bmf, extra, hist, N["panel"])
    summ_b = build_b(units)
    write_csv(a.out_b, summ_b, FIELDS_B)

    ub = {u["key"]: u for u in units}
    pick = lambda st, sc, b: next(s for s in summ_a if s["scope_type"] == st and s["scope"] == sc and s["basis"] == b)  # noqa: E731
    rnd = lambda d: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items() if k != "source"}  # noqa: E731
    out = {
        "sponsor_years": N["sponsor_years"], "recipient_eins": len(nums), "frame": len(frame), "sample": len(sample),
        "scale_top50_share_of_netted_fy2024": scale, "oids": len(oids),
        "f990_status": {k: len(v) for k, v in _group_by_fast(f990.values(), lambda x: x["status"]).items()},
        "recipient_status": {k: len(v) for k, v in _group_by_fast(rec, lambda r: r["status"]).items()},
        "form_mix_ok": {k: len(v) for k, v in _group_by_fast((r for r in rec if r["status"] == "ok"), lambda r: r["forms"]).items()},
        "lines_sum_to_1h_false": sum(1 for r in rec if r["status"] == "ok" and not r["lines_sum_to_1h"]),
        "leaked_sponsor_names": sorted(r["name"] for r in rec if r["leaked_sponsor_name"]),
        "a_all": {b: rnd(pick("all", "all_ex_excluded", b)) for b, _ in BASES},
        "a_line_mix_weighted": (lambda ok, w: {k: sum(w[r["stratum"]] * r[f"{k}_matched"] for r in ok) /
                                               sum(w[r["stratum"]] * r["l1h_matched"] for r in ok) for k in LINES})(
            [r for r in rec if r["status"] == "ok" and "IRS990EZ" not in r["forms"]], weights_a(rec)),
        "a_line_mix_weighted_median_1f_over_1h": wquantile(
            [(r["l1f_matched"] / r["l1h_matched"], weights_a(rec)[r["stratum"]]) for r in rec
             if r["status"] == "ok" and "IRS990EZ" not in r["forms"]], 0.5),
        "b_all": [rnd(r) for r in summ_b if r["scope_type"] == "all"],
        "b_not_in_bmf_passing_filing_rules": (lambda xs: {"recipients": len(xs), "usd_daf_weighted": round(sum(u["dw"] for u in xs)),
                                                           "dollar_share": sum(u["dw"] for u in xs) / sum(u["dw"] for u in units)})(
            tuple(u for u in units if u["reason"] == "not_in_bmf" and u["n_in_window"] >= 3 and u["latest_form"] != "990PF"
                  and u["n_full_990_last4"] >= 2)),
        "b_not_in_bmf_with_any_efiled_return": sum(1 for u in units if u["reason"] == "not_in_bmf" and u["n_periods"] > 0),
        "b_unit_count": len(units), "b_total_dw": round(sum(u["dw"] for u in units)), "b_total_si": round(sum(u["si"] for u in units)),
        "b_bmf_eins_also_on_revocation_list_no_reinstatement": len(revoked),
        "b_expense_rule_sample_check": expense_check(sample, ub, {s["ein"]: tuple(r for r in hist.get(s["ein"], ())
                                                                                   if r["oid"] in f990) for s in sample}, f990),
        "b_sample_overlap": {k: len(v) for k, v in _group_by_fast((ub[s["ein"]] for s in sample), lambda u: u["reason"]).items()},
        "b_largest_ineligible": sorted(({"key": u["key"], "reason": u["reason"], "dw": round(u["dw"]), "type": u["type"],
                                         "name": (bmf.get(u["key"], {}).get("name") or "")[:40]}
                                        for u in units if u["reason"] != "eligible"), key=lambda d: -d["dw"])[:25],
    }
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
