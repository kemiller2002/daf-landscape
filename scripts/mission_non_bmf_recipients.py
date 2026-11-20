#!/usr/bin/env python3
"""P-B40N1202-B43N26-03: resolve the top-50 recipient EINs that are not in the November 2026 IRS EO BMF.

Universe  Exactly the `not_in_bmf` recipients of scripts/mission_recipient_basis_eligibility.py (imported, not
          modified): top-50 DAFRC sponsors, FY2023-24 Schedule I Part II lines, non-DAF-to-DAF, positive amounts,
          EIN present, EIN absent from the IRS EO BMF files (eo1-4, eo_pr, eo_xx). Dollars are `daf_weighted`
          (each sponsor-year's lines x its DAF share of grants) as in that script; Schedule I dollars are kept too.

Evidence joined per EIN (all IRS bulk files, apps.irs.gov/pub/epostcard/ and www.irs.gov/pub/irs-soi/):
    - Pub 78 data (data-download-pub78.txt): EIN|name|city|state|country|deductibility codes;
    - automatic-revocation list (data-download-revocation.txt): EIN|name|dba|street|city|state|zip|country|
      exemption type|revocation date|posting date|reinstatement date (latest row per EIN by posting date);
    - Form 990-N e-Postcard data (data-download-epostcard.txt): only EIN, tax year, organisation name and the
      "organization has terminated" flag are read (officer names and addresses are never read into memory);
    - TEOS e-file index 2019-2026 (all DLN prefixes) for filing history and the filer's name;
    - the header and Part IV/V indicators of the earliest and latest e-filed return per EIN (GivingTuesday mirror
      of IRS TEOS XML): InitialReturnInd, FinalReturnInd, ApplicationPendingInd, NameChangeInd,
      TerminateOperationsInd and any other true/X indicator whose tag names termination or liquidation;
    - the full BMF (all ~1.9m rows) as a name index, for the wrong-EIN / typo test.
    Earlier BMF extracts are not offered by the IRS (www.irs.gov/charities-non-profits/
    exempt-organizations-business-master-file-extract-eo-bmf lists only the current files), so none is used.

Categories (first match wins, in this order):
    revoked                   on the revocation list with no reinstatement date, and the revocation-list name
                              matches the name as filed (name_sim >= NAME_OK). Sub: `name_now_in_bmf_other_ein`
                              when the same normalised name is in the BMF under another EIN (re-recognised or
                              successor), else `no_bmf_successor`.
    foreign_or_government     line address foreign, IRC-section text naming a government / 170(c)(1) / 115, or a
                              government-unit name rule (state, county, city, school district, public university
                              system, ...). Sub says which rule fired.
    subsidiary_or_disregarded LLC / limited-liability names (disregarded single-member LLCs have no BMF row). This
                              category is an addition to the task's list; folding it into `unresolved` gives the
                              task's six-way split (both are reported).
    invalid_or_typo           (a) EIN prefix the IRS does not assign; or (b) the EIN has IRS history under a
                              different name (name_sim < NAME_BAD) while the filed name is in the BMF under another
                              EIN; or (c) no IRS trace at all and the filed name is in the BMF under another EIN
                              (exact normalised name, or a BMF EIN one digit / one adjacent transposition away with
                              name_sim >= NAME_OK).
    merged_or_terminated      a final-return or terminate-operations indicator on the latest e-filed return, an
                              e-Postcard "terminated" flag, or IRS history under the filed name with that name now in
                              the BMF under another EIN (successor / name moved).
    new_ein                   first e-filed or e-Postcard tax period ends 2022 or later, an initial-return indicator
                              on the earliest return, or an application-pending indicator.
    unresolved                everything else; sub says whether the EIN has any IRS trace.

Revoked at grant time  For revoked EINs, each sponsor-year line is dated only to the sponsor's fiscal year (12
    months ending on the return's tax_period_end). `before_fy` = revocation effective date before the fiscal year
    began; `posted_before_fy` = the IRS posting date (when it became public) before the fiscal year began;
    `during_fy`; `after_fy`. Reinstatements can be retroactive and later rows can change this.

Pure functions; I/O only in load/fetch helpers and `main`. Stdlib only.

Usage:
  python3 scripts/mission_non_bmf_recipients.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --index-dir IRSDIR --epostcard FILE --xml-cache DIR [--fetch] [--base-cache FILE]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import json
import os
import pickle
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DATA, XML_URL, _group_by_fast, ein9, local  # noqa: E402
from mission_daf_share_recipient_revenue import load_bmf  # noqa: E402
from mission_daf_to_daf import load_np, pick_returns  # noqa: E402
from mission_recipient_basis_eligibility import (HIST_YEARS, build_numerator, cn_filing_test,  # noqa: E402
                                                 load_history, no_ein_lines)
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_recipient_sectors import BMF_FILES, load_lines  # noqa: E402

OUT = os.path.join(DATA, "non-bmf-recipients-2026-11-20.csv")
UA = "research-script/1.0"
XML_V = 1
NAME_OK = 0.80
NAME_BAD = 0.45
FUZZY_OK = 0.90
NEW_FROM = 2022
# IRS "How EINs are assigned and valid EIN prefixes" (www.irs.gov/businesses/small-businesses-self-employed/
# how-eins-are-assigned-and-valid-ein-prefixes): prefixes not in this set are not assigned.
VALID_PREFIX = frozenset(f"{p:02d}" for p in (*range(1, 7), *range(10, 17), *range(20, 28), *range(30, 49),
                                               *range(50, 69), *range(71, 78), *range(80, 89), *range(90, 96), 98, 99))
STOP = frozenset({"THE", "INC", "INCORPORATED", "CORP", "CORPORATION", "CO", "LTD", "OF", "AND", "A", "AN", "FOR",
                  "NFP", "NONPROFIT", "NON", "PROFIT"})
GOV_IRC = re.compile(r"GOV|170\s*\(?C\)?\s*\(?1\)?|\b115\b|MUNICIPAL|PUBLIC\s+(SCHOOL|ENTITY|AGENCY|INSTITUTION)|STATE\s+(AGENCY|ENTITY|INSTITUTION)")
FOREIGN_IRC = re.compile(r"FOREIGN|NON[- ]?US|NON[- ]?U\.S")
STATES = ("ALABAMA|ALASKA|ARIZONA|ARKANSAS|CALIFORNIA|COLORADO|CONNECTICUT|DELAWARE|FLORIDA|GEORGIA|HAWAII|IDAHO|"
          "ILLINOIS|INDIANA|IOWA|KANSAS|KENTUCKY|LOUISIANA|MAINE|MARYLAND|MASSACHUSETTS|MICHIGAN|MINNESOTA|"
          "MISSISSIPPI|MISSOURI|MONTANA|NEBRASKA|NEVADA|NEW HAMPSHIRE|NEW JERSEY|NEW MEXICO|NEW YORK|NORTH CAROLINA|"
          "NORTH DAKOTA|OHIO|OKLAHOMA|OREGON|PENNSYLVANIA|RHODE ISLAND|SOUTH CAROLINA|SOUTH DAKOTA|TENNESSEE|TEXAS|"
          "UTAH|VERMONT|VIRGINIA|WASHINGTON|WEST VIRGINIA|WISCONSIN|WYOMING")
GOV_NAME = (
    ("school_district", re.compile(r"\b(SCHOOL DISTRICT|SCHOOL DIST|SCH DIST|UNIFIED SCHOOL|INDEPENDENT SCHOOL|ISD|USD|"
                                   r"PUBLIC SCHOOLS?|BOARD OF EDUCATION|BOARD OF ED|COUNTY SCHOOLS|CITY SCHOOLS|"
                                   r"DEPARTMENT OF EDUCATION|SCHOOL BOARD|CSD|UFSD)\b")),
    ("public_school_by_level", re.compile(r"\b(ELEMENTARY|MIDDLE SCHOOL|HIGH SCHOOL|JUNIOR HIGH|INTERMEDIATE SCHOOL|"
                                          r"PRIMARY SCHOOL)\b")),
    ("state_university", re.compile(r"\b(STATE UNIVERSITY|STATE COLLEGE|COMMUNITY COLLEGE|TECHNICAL COLLEGE|"
                                    r"UNIVERSITY OF (" + STATES + r")|(" + STATES + r") UNIVERSITY|REGENTS|"
                                    r"BOARD OF TRUSTEES OF|UNIVERSITY SYSTEM|PENN STATE|PENNSYLVANIA STATE)\b")),
    ("local_government", re.compile(r"\b(CITY OF|TOWN OF|VILLAGE OF|COUNTY OF|TOWNSHIP|BOROUGH OF|PARISH OF|"
                                    r"COUNTY|MUNICIPALITY|CITY COUNCIL|PARKS? (AND|&) REC|RECREATION DEPARTMENT|"
                                    r"PUBLIC LIBRARY|LIBRARY DISTRICT|FIRE DEPARTMENT|FIRE DEPT|FIRE DISTRICT|"
                                    r"POLICE DEPARTMENT|POLICE DEPT|SHERIFF|PARK DISTRICT|HOSPITAL DISTRICT|"
                                    r"HEALTH DISTRICT|WATER DISTRICT|PORT AUTHORITY|HOUSING AUTHORITY)\b")),
    ("state_or_federal", re.compile(r"\b(STATE OF|COMMONWEALTH OF|DEPARTMENT OF|DEPT OF|UNITED STATES|U S |"
                                    r"NATIONAL PARK SERVICE|TREASURER|GOVERNMENT|GOVT|TRIBE|TRIBAL|NATION OF|"
                                    r"VETERANS AFFAIRS|STATE PARKS?)\b")),
)
FOREIGN_NAME = re.compile(r"\b(CANADA|CANADIAN|UK|ENGLAND|LONDON|AUSTRALIA|ISRAEL|STIFTUNG|E\.?\s?V\.?|GMBH|"
                          r"FONDATION|FUNDACION|FONDAZIONE|ASBL|VZW|TRUST UK|LIMITED|LTD|CIC|SOCIETE|ASOCIACION|"
                          r"ASSOCIACAO|AMUTA|MEXICO|INDIA|KENYA|UGANDA|HAITI)\b")
LLC_NAME = re.compile(r"\b(L\s?L\s?C|L\.L\.C\.?|LIMITED LIABILITY|BIOHUB)\b")
TERM_FLAGS = frozenset({"FinalReturnInd", "TerminateOperationsInd", "OrganizationDissolvedEtcInd"})
RELIGIOUS = re.compile(r"\b(CHURCH|CATHOLIC|PARISH|DIOCESE|ARCHDIOCESE|SYNAGOGUE|CONGREGATION|CONG|YESHIVA|TEMPLE|"
                       r"MOSQUE|MASJID|MINISTRY|MINISTRIES|CHAPEL|BAPTIST|METHODIST|PRESBYTERIAN|LUTHERAN|EPISCOPAL|"
                       r"JESUIT|SOCIETY OF JESUS|PROVINCE|SISTERS|FRIARS|ABBEY|MONASTERY|KOLLEL|TORAH|CHABAD|"
                       r"FELLOWSHIP|ASSEMBLY OF GOD|BIBLE|GOSPEL|SAINT|ST)\b")
HDR_TAGS = frozenset({"InitialReturnInd", "FinalReturnInd", "ApplicationPendingInd", "NameChangeInd",
                      "AmendedReturnInd", "TerminateOperationsInd", "GroupReturnForAffiliatesInd",
                      "Organization501c3Ind", "DisregardedEntityInd", "OrganizationDissolvedEtcInd"})
CATS = ("revoked", "foreign_or_government", "subsidiary_or_disregarded", "invalid_or_typo", "merged_or_terminated",
        "new_ein", "unresolved")


# ----------------------------------------------------------------------------- names
def norm(s: str) -> str:
    t = re.sub(r"[^A-Z0-9 ]", " ", (s or "").upper().replace("&", " AND "))
    return " ".join(w for w in t.split() if w not in STOP)


def name_sim(a: str, b: str) -> float:
    """max(SequenceMatcher ratio, token containment of the shorter name) on normalised names; 0 if either empty."""
    x, y = norm(a), norm(b)
    if not x or not y:
        return 0.0
    tx, ty = set(x.split()), set(y.split())
    cont = len(tx & ty) / min(len(tx), len(ty))
    return max(difflib.SequenceMatcher(None, x, y).ratio(), cont if min(len(tx), len(ty)) >= 2 else 0.0)


def ein_neighbours(e: str) -> tuple[str, ...]:
    subs = (e[:i] + d + e[i + 1:] for i in range(9) for d in "0123456789" if d != e[i])
    swaps = (e[:i] + e[i + 1] + e[i] + e[i + 2:] for i in range(8) if e[i] != e[i + 1])
    return tuple(dict.fromkeys((*subs, *swaps)))


def parse_date(s: str) -> dt.date | None:
    s = (s or "").strip()
    for fmt in ("%d-%b-%Y", "%m-%d-%Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


# ----------------------------------------------------------------------------- loaders (I/O)
def read_pipe(path: str, keep, cols: Sequence[int]) -> Iterable[tuple]:
    with open(path, encoding="latin-1") as fh:
        parts = (ln.rstrip("\r\n").split("|") for ln in fh)
        yield from (tuple(p[i] if i < len(p) else "" for i in cols) for p in parts
                    if len(p) > max(cols) // 2 and ein9(p[0]) in keep)


def load_revocation(path: str, keep: frozenset) -> dict:
    rows = tuple({"ein": ein9(r[0]), "name": r[1].strip(), "dba": r[2].strip(), "state": r[5].strip(),
                  "country": r[7].strip(), "exempt_type": r[8].strip(), "rev_date": parse_date(r[9]),
                  "post_date": parse_date(r[10]), "reinst_date": parse_date(r[11])}
                 for r in read_pipe(path, keep, range(12)))
    return {e: tuple(sorted(v, key=lambda r: (r["post_date"] or dt.date.min, r["rev_date"] or dt.date.min)))
            for e, v in _group_by_fast(rows, lambda r: r["ein"]).items()}


def load_pub78(path: str, keep: frozenset) -> dict:
    return {ein9(r[0]): {"name": r[1].strip(), "state": r[3].strip(), "country": r[4].strip(), "codes": r[5].strip()}
            for r in read_pipe(path, keep, range(6))}


def load_epostcard(path: str, keep: frozenset) -> dict:
    rows = tuple((ein9(r[0]), {"tax_year": r[1].strip(), "name": r[2].strip(), "terminated": r[4].strip().upper() == "T"})
                 for r in read_pipe(path, keep, (0, 1, 2, 3, 4)))
    return {e: tuple(x for _, x in v) for e, v in _group_by_fast(rows, lambda t: t[0]).items()}


def load_index_any(index_dir: str, keep: frozenset) -> dict:
    """All TEOS index rows (any DLN prefix) for `keep`: ein -> rows with tax_period, name, return_type, oid."""
    def rows(y):
        p = os.path.join(index_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            return ()
        with open(p, encoding="utf-8", errors="replace", newline="") as fh:
            return tuple({"ein": ein9(d["EIN"]), "tax_period": d["TAX_PERIOD"], "name": (d.get("TAXPAYER_NAME") or "").strip(),
                          "return_type": d["RETURN_TYPE"], "dln": d.get("DLN") or "", "oid": d["OBJECT_ID"], "index_year": y}
                         for d in csv.DictReader(fh) if ein9(d.get("EIN", "")) in keep)
    return _group_by_fast((r for y in HIST_YEARS for r in rows(y)), lambda r: r["ein"])


def load_bmf_names(bmf_dir: str) -> tuple[dict, dict]:
    """(ein -> name, normalised name -> tuple of EINs) over every BMF row."""
    def rows(f):
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple((ein9(r["EIN"]), (r.get("NAME") or "").strip(), (r.get("STATE") or "").strip())
                         for r in csv.DictReader(fh))
    allr = tuple(x for f in BMF_FILES for x in rows(f))
    by_ein = {e: {"name": n, "state": st} for e, n, st in allr}
    by_name = {k: tuple(e for e, _, _ in v) for k, v in _group_by_fast(allr, lambda t: norm(t[1])).items() if k}
    return by_ein, by_name


def token_index(by_ein: Mapping) -> dict:
    """(state, token) -> EINs, over normalised BMF names, for the same-state fuzzy name search."""
    pairs = ((st_tok, e) for e, v in by_ein.items() for st_tok in {(v["state"], t) for t in norm(v["name"]).split()})
    return {k: tuple(e for _, e in v) for k, v in _group_by_fast(pairs, lambda t: t[0]).items()}


def parse_header(stream) -> dict:
    flags, name, form, tpe = set(), "", "", ""
    for _, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        txt = (el.text or "").strip()
        if (tag in HDR_TAGS or tag in TERM_FLAGS) and txt.lower() in ("true", "x", "1"):
            flags.add(tag)
        elif tag == "BusinessNameLine1Txt" and not name:
            name = txt
        elif tag == "ReturnTypeCd" and not form:
            form = txt
        elif tag == "TaxPeriodEndDt" and not tpe:
            tpe = txt
        if tag.startswith("IRS990Schedule") or tag in ("IRS990ScheduleI",):
            el.clear()
    return {"flags": sorted(flags), "filer_name": name, "form": form, "tax_period_end": tpe}


def fetch_header(oid: str, cache: str, fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == XML_V:
            return c
    if not fetch:
        return {"status": "not_fetched", "flags": []}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                r = {**parse_header(resp), "status": "ok", "_v": XML_V}
            break
        except urllib.error.HTTPError as e:
            r = {"status": f"http_{e.code}", "flags": [], "_v": XML_V}
            if e.code in (403, 404):
                break
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError) as e:
            r = {"status": f"error:{type(e).__name__}", "flags": [], "_v": XML_V}
        time.sleep(1 + attempt)
    if r["status"] == "ok" or r["status"].startswith("http_404"):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(r, fh)
    return r


# ----------------------------------------------------------------------------- base (as the eligibility script)
def build_base(a) -> dict:
    N = build_numerator(a)
    nums = N["nums"]
    bmf = load_bmf(a.bmf_dir, frozenset(nums))
    nb = frozenset(e for e in nums if e not in bmf)
    chosen = pick_returns(load_np(a.np_cache))
    tpe = {k: x["tax_period_end"] for k, x in chosen.items()}
    irc = {k: tuple(l[3] for l in drop_totals_rows(load_lines(chosen[k]["oid"], chosen[k].get("sched_i_lines") or 0,
                                                              a.lines_cache, [], False))["lines"]) for k in N["ann"]}
    assert all(len(irc[k]) == len(v) for k, v in N["ann"].items()), "line alignment with the eligibility script failed"
    lines = tuple({"ein": r["ein"], "name": r["name"], "where": r["where"], "irc": irc[k][i],
                   "sponsor": k[0], "fy": k[1], "tpe": tpe.get(k, ""), "si": r["amount"],
                   "dw": r["amount"] * N["weights"].get(k, 1.0)}
                  for k, rs in N["ann"].items() for i, r in enumerate(rs)
                  if r["ein"] in nb and not r["d2d"] and r["amount"] > 0)
    hist = load_history(a.index_dir, nb)
    tests = {e: cn_filing_test(hist.get(e, ()), "tax_year") for e in nb}
    blank = no_ein_lines(N["ann"], N["weights"])
    return {"nb": nb, "lines": lines, "tests": tests, "hist": hist, "total_dw_blank_ein": sum(v["dw"] for v in blank.values()),
            "total_dw_all": sum(sum(v["dw"] for v in n["fy"].values()) for n in nums.values()),
            "n_recipient_eins": len(nums)}


# ----------------------------------------------------------------------------- classification (pure)
def ein_profile(e: str, ls: Sequence[Mapping]) -> dict:
    by_name = _group_by_fast(ls, lambda l: l["name"])
    top = max(by_name.items(), key=lambda kv: sum(l["dw"] for l in kv[1]))[0]
    return {"ein": e, "name_filed": top, "names_filed": sorted(by_name), "dw": sum(l["dw"] for l in ls),
            "si": sum(l["si"] for l in ls),
            "state": max(_group_by_fast(ls, lambda l: l["where"]).items(), key=lambda kv: sum(l["dw"] for l in kv[1]))[0],
            "foreign_addr": any(l["where"].startswith("F:") for l in ls),
            "irc": sorted({l["irc"].upper() for l in ls if l["irc"]}), "sponsors": len({l["sponsor"] for l in ls}),
            "dw_fy": {fy: sum(l["dw"] for l in v) for fy, v in _group_by_fast(ls, lambda l: l["fy"]).items()}}


def gov_rule(p: Mapping) -> str:
    if p["foreign_addr"]:
        return "foreign_address"
    if any(FOREIGN_IRC.search(i) for i in p["irc"]):
        return "foreign_irc_text"
    if any(GOV_IRC.search(i) for i in p["irc"]):
        return "government_irc_text"
    nm = " ".join(norm(n) for n in p["names_filed"]) + " " + " ".join(n.upper() for n in p["names_filed"])
    by_name = next((f"government_name_{k}" for k, rx in GOV_NAME if rx.search(nm)), "")
    return by_name or ("government_ein_600_series_heuristic" if p["ein"][2:5] == "600" else "")


def fuzzy_same_state(name: str, state: str, bmf_ein: Mapping, tok_idx: Mapping, cap: int = 4000) -> tuple:
    """BMF EINs in `state` whose name_sim with `name` >= FUZZY_OK, searched via the rarest name token."""
    toks = sorted({t for t in norm(name).split()}, key=lambda t: len(tok_idx.get((state, t), ())))
    cand = tok_idx.get((state, toks[0]), ()) if toks and state else ()
    if not cand or len(cand) > cap:
        return ()
    return tuple(sorted(((x, s) for x in cand for s in (name_sim(name, bmf_ein[x]["name"]),) if s >= FUZZY_OK),
                        key=lambda t: -t[1]))


def hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def typo_match(e: str, name: str, state: str, bmf_ein: Mapping, bmf_name: Mapping, tok_idx: Mapping) -> dict:
    """Candidate 'intended' BMF EINs for a filed (EIN, name, state). `unique_state` = exactly one BMF EIN in the line's
    state carries the same normalised name, or (failing that) exactly one same-state fuzzy match."""
    exact = tuple(x for x in bmf_name.get(norm(name), ()) if x != e)
    exact_st = tuple(x for x in exact if state and bmf_ein[x]["state"] == state)
    near = tuple(sorted(((x, name_sim(name, bmf_ein[x]["name"])) for x in ein_neighbours(e) if x in bmf_ein),
                        key=lambda t: -t[1]))
    good_near = tuple(t for t in near if t[1] >= NAME_OK)
    fz = () if (good_near or exact_st) else tuple(t for t in fuzzy_same_state(name, state, bmf_ein, tok_idx) if t[0] != e)
    best, how = ((good_near[0][0], "neighbour_ein_name_match") if good_near
                 else (exact_st[0], "exact_name_unique_in_state") if len(exact_st) == 1
                 else ("", "exact_name_ambiguous_in_state") if len(exact_st) > 1
                 else (fz[0][0], "fuzzy_name_unique_in_state") if len(fz) == 1
                 else ("", "fuzzy_name_ambiguous_in_state") if len(fz) > 1
                 else ("", "exact_name_other_state_only") if exact else ("", ""))
    return {"exact_other_eins": exact, "best": best, "how": how,
            "hamming": hamming(e, best) if best else None}


def classify(p: Mapping, ev: Mapping, bmf_ein: Mapping, bmf_name: Mapping, tok_idx: Mapping) -> dict:
    e, nm = p["ein"], p["name_filed"]
    rev = ev["rev"][-1] if ev["rev"] else None
    rev_live = rev is not None and rev["reinst_date"] is None
    trace_names = tuple(x for x in ((rev or {}).get("name"), (ev["pub78"] or {}).get("name"),
                                    *(r["name"] for r in ev["idx"]), *(r["name"] for r in ev["epost"])) if x)
    sim_trace = max((name_sim(nm, t) for t in trace_names), default=None)
    has_trace = bool(trace_names)
    tm = typo_match(e, nm, p["state"], bmf_ein, bmf_name, tok_idx)
    hdr_flags = frozenset(f for h in ev["hdr"] for f in h.get("flags", ()))
    latest_flags = frozenset(ev["hdr"][-1].get("flags", ())) if ev["hdr"] else frozenset()
    periods = sorted({r["tax_period"][:4] for r in ev["idx"] if r["tax_period"][:4].isdigit()} |
                     {r["tax_year"] for r in ev["epost"] if r["tax_year"].isdigit()})
    first_year = int(periods[0]) if periods else None
    gr = gov_rule(p)
    base = {"has_irs_trace": has_trace, "name_sim_irs": None if sim_trace is None else round(sim_trace, 3),
            "first_year": first_year, "last_year": int(periods[-1]) if periods else None,
            "typo_best_ein": tm["best"], "typo_how": tm["how"], "typo_hamming": tm["hamming"], "flags": ";".join(sorted(hdr_flags)),
            "rev_date": rev["rev_date"] if rev else None, "post_date": rev["post_date"] if rev else None,
            "reinst_date": rev["reinst_date"] if rev else None, "rev_name": rev["name"] if rev else "",
            "in_pub78": ev["pub78"] is not None, "valid_prefix": e[:2] in VALID_PREFIX}

    def out(cat, sub):
        return {**base, "category": cat, "sub": sub}

    if rev_live and name_sim(nm, rev["name"]) >= NAME_OK:
        return out("revoked", "name_now_in_bmf_other_ein" if tm["best"] else "no_bmf_successor")
    if gr:
        return out("foreign_or_government", gr)
    if any(LLC_NAME.search(n.upper()) for n in p["names_filed"]):
        return out("subsidiary_or_disregarded", "llc_name")
    if not base["valid_prefix"]:
        return out("invalid_or_typo", "unassigned_ein_prefix")
    if has_trace and sim_trace is not None and sim_trace < NAME_BAD and tm["best"]:
        return out("invalid_or_typo", "ein_belongs_to_other_org_name_in_bmf")
    if not has_trace and tm["best"]:
        return out("invalid_or_typo", ("typo_" if tm["hamming"] is not None and tm["hamming"] <= 2 else "wrong_ein_")
                   + tm["how"])
    if rev_live:
        return out("invalid_or_typo" if tm["best"] else "revoked",
                   "revoked_ein_other_name_name_in_bmf" if tm["best"] else "revoked_name_mismatch")
    if latest_flags & TERM_FLAGS:
        return out("merged_or_terminated", "final_or_terminate_flag_latest_return")
    if any(r["terminated"] for r in ev["epost"]):
        return out("merged_or_terminated", "epostcard_terminated")
    if has_trace and tm["best"] and (sim_trace or 0) >= NAME_OK:
        return out("merged_or_terminated", "name_now_in_bmf_other_ein")
    if (first_year is not None and first_year >= NEW_FROM) or "ApplicationPendingInd" in hdr_flags \
            or (ev["hdr"] and "InitialReturnInd" in ev["hdr"][0].get("flags", ()) and (first_year or 0) >= 2019):
        return out("new_ein", "application_pending" if "ApplicationPendingInd" in hdr_flags
                   else f"first_period_{NEW_FROM}_plus" if first_year and first_year >= NEW_FROM else "initial_return_flag")
    if rev is not None:
        return out("unresolved", "revoked_then_reinstated_not_in_bmf")
    if ev["idx"] or ev["epost"] or ev["pub78"]:
        return out("unresolved", "has_irs_filings" if ev["idx"] else "epostcard_only" if ev["epost"] else "pub78_only")
    if tm["how"] in ("exact_name_ambiguous_in_state", "fuzzy_name_ambiguous_in_state", "exact_name_other_state_only"):
        return out("unresolved", "no_irs_trace_" + tm["how"])
    if any(RELIGIOUS.search(norm(n)) for n in p["names_filed"]):
        return out("unresolved", "no_irs_trace_religious_name")
    return out("unresolved", "no_irs_trace_other")


def fy_bounds(tpe: str) -> tuple[dt.date, dt.date] | None:
    end = parse_date(tpe)
    if end is None:
        return None
    try:
        start = end.replace(year=end.year - 1) + dt.timedelta(days=1)
    except ValueError:
        start = dt.date(end.year - 1, 3, 1)
    return start, end


def timing(line: Mapping, rev_date: dt.date | None, post_date: dt.date | None) -> str:
    b = fy_bounds(line["tpe"])
    if b is None or rev_date is None:
        return "unknown"
    if rev_date < b[0]:
        return "before_fy_posted_before_fy" if post_date and post_date < b[0] else "before_fy_posted_later"
    return "during_fy" if rev_date <= b[1] else "after_fy"


# ----------------------------------------------------------------------------- outputs (pure)
def agg_rows(units: Sequence[Mapping], key, scope: str, total_dw_all: float) -> list:
    tot = sum(u["dw"] for u in units)
    by = _group_by_fast(units, key)
    return [{"row_type": "aggregate", "scope": scope, "category": k, "recipients": len(v),
             "usd_daf_weighted": round(sum(u["dw"] for u in v)), "usd_schedule_i": round(sum(u["si"] for u in v)),
             "usd_daf_weighted_fy2023": round(sum(u["dw_fy"].get(2023, 0.0) for u in v)),
             "usd_daf_weighted_fy2024": round(sum(u["dw_fy"].get(2024, 0.0) for u in v)),
             "share_of_non_bmf_daf_weighted": round(sum(u["dw"] for u in v) / tot, 6) if tot else "",
             "share_of_all_top50_daf_weighted": round(sum(u["dw"] for u in v) / total_dw_all, 6)}
            for k, v in sorted(by.items(), key=lambda kv: -sum(u["dw"] for u in kv[1]))]


FIELDS = ("row_type", "scope", "category", "recipients", "usd_daf_weighted", "usd_schedule_i",
          "usd_daf_weighted_fy2023", "usd_daf_weighted_fy2024", "share_of_non_bmf_daf_weighted",
          "share_of_all_top50_daf_weighted", "ein", "name_as_filed", "sub_category")


def write_out(path: str, rows: Sequence[Mapping]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def six_way(c: str) -> str:
    return "unresolved" if c == "subsidiary_or_disregarded" else c


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True, help="holds index_YYYY.csv, data-download-revocation.txt, data-download-pub78.txt")
    ap.add_argument("--epostcard", required=True, help="data-download-epostcard.txt")
    ap.add_argument("--xml-cache", required=True)
    ap.add_argument("--base-cache", default="", help="optional pickle of the (slow) base extract")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    if a.base_cache and os.path.exists(a.base_cache):
        with open(a.base_cache, "rb") as fh:
            B = pickle.load(fh)
    else:
        B = build_base(a)
        if a.base_cache:
            with open(a.base_cache, "wb") as fh:
                pickle.dump(B, fh)
    nb = B["nb"]
    profiles = {e: ein_profile(e, v) for e, v in _group_by_fast(B["lines"], lambda l: l["ein"]).items()}
    rev = load_revocation(os.path.join(a.index_dir, "data-download-revocation.txt"), nb)
    pub = load_pub78(os.path.join(a.index_dir, "data-download-pub78.txt"), nb)
    epost = load_epostcard(a.epostcard, nb)
    idx = load_index_any(a.index_dir, nb)
    bmf_ein, bmf_name = load_bmf_names(a.bmf_dir)
    tok_idx = token_index(bmf_ein)

    def pick_oids(rs):
        efile = sorted((r for r in rs if r["dln"][:5] in ("93493", "93492", "93491")), key=lambda r: (r["tax_period"], r["oid"]))
        return tuple(dict.fromkeys(x["oid"] for x in (efile[:1] + efile[-1:])))
    want = {e: pick_oids(rs) for e, rs in idx.items()}
    os.makedirs(a.xml_cache, exist_ok=True)
    oids = sorted({o for v in want.values() for o in v})
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        hdr = dict(zip(oids, ex.map(lambda o: fetch_header(o, a.xml_cache, a.fetch), oids)))
    ev = {e: {"rev": rev.get(e, ()), "pub78": pub.get(e), "epost": epost.get(e, ()),
              "idx": tuple(sorted(idx.get(e, ()), key=lambda r: (r["tax_period"], r["oid"]))),
              "hdr": tuple(hdr[o] for o in want.get(e, ()) if hdr[o].get("status") == "ok")} for e in nb}
    units = tuple({**p, **classify(p, ev[e], bmf_ein, bmf_name, tok_idx), **{"cn_" + k: v for k, v in B["tests"][e].items()}}
                  for e, p in profiles.items())
    cn_pass = lambda u: u["cn_n_in_window"] >= 3 and u["cn_latest_form"] != "990PF" and u["cn_n_full_990_last4"] >= 2  # noqa: E731

    # revoked at grant time (lines of EINs in the `revoked` category)
    rv = {u["ein"]: u for u in units if u["category"] == "revoked"}
    tl = tuple({**l, "timing": timing(l, rv[l["ein"]]["rev_date"], rv[l["ein"]]["post_date"]), "sub": rv[l["ein"]]["sub"]}
               for l in B["lines"] if l["ein"] in rv)
    timing_summary = {k: {"lines": len(v), "eins": len({l["ein"] for l in v}), "usd_daf_weighted": round(sum(l["dw"] for l in v)),
                          "usd_schedule_i": round(sum(l["si"] for l in v)),
                          "by_sub": {s: round(sum(l["dw"] for l in w)) for s, w in _group_by_fast(v, lambda l: l["sub"]).items()},
                          "sponsors": len({l["sponsor"] for l in v})}
                      for k, v in _group_by_fast(tl, lambda l: l["timing"]).items()}

    TOT = B["total_dw_all"] + B["total_dw_blank_ein"]
    rows = (agg_rows(units, lambda u: u["category"], "category", TOT)
            + agg_rows(units, lambda u: six_way(u["category"]), "category_six_way", TOT)
            + agg_rows(units, lambda u: u["category"] + "/" + u["sub"], "category_sub", TOT)
            + agg_rows(tuple(u for u in units if cn_pass(u)), lambda u: u["category"], "cn_filing_rule_pass_1213", TOT)
            + agg_rows(units, lambda u: "all", "all", TOT)
            + [{"row_type": "recipient", "ein": u["ein"], "name_as_filed": u["name_filed"], "category": u["category"],
                "sub_category": u["sub"], "usd_daf_weighted": round(u["dw"])}
               for u in sorted(units, key=lambda u: (-u["dw"], u["ein"]))])
    write_out(a.out, rows)

    top = lambda c, n=8: [{"ein": u["ein"], "name": u["name_filed"][:45], "sub": u["sub"], "dw": round(u["dw"]),  # noqa: E731
                           "rev_date": str(u["rev_date"] or ""), "typo_best": u["typo_best_ein"],
                           "typo_best_name": bmf_ein.get(u["typo_best_ein"], {}).get("name", "")[:40]}
                          for u in sorted((u for u in units if u["category"] == c), key=lambda u: -u["dw"])[:n]]
    summary = {
        "non_bmf_eins": len(nb), "non_bmf_with_lines": len(units), "usd_dw": round(sum(u["dw"] for u in units)),
        "recipient_eins_all": B["n_recipient_eins"], "total_dw_all": round(B["total_dw_all"]), "total_dw_incl_blank_ein": round(TOT),
        "evidence_counts": {"revocation_any_row": sum(1 for e in nb if rev.get(e)),
                            "revocation_no_reinstatement": sum(1 for e in nb if rev.get(e) and rev[e][-1]["reinst_date"] is None),
                            "pub78": len(pub), "epostcard": len(epost), "teos_index_any": len(idx),
                            "teos_index_990_series": sum(1 for e in nb if B["hist"].get(e)),
                            "no_irs_trace": sum(1 for u in units if not u["has_irs_trace"]),
                            "invalid_prefix": sum(1 for u in units if not u["valid_prefix"])},
        "xml_headers": {k: len(v) for k, v in _group_by_fast(hdr.values(), lambda h: h.get("status")).items()},
        "pub78_eins": {e: {**v, "category": next(u["category"] for u in units if u["ein"] == e)} for e, v in pub.items()},
        "cn_pass": {"recipients": sum(1 for u in units if cn_pass(u)), "usd_dw": round(sum(u["dw"] for u in units if cn_pass(u)))},
        "revoked_timing": timing_summary,
        "revoked_rev_year": {k: {"eins": len(v), "dw": round(sum(u["dw"] for u in v))}
                             for k, v in sorted(_group_by_fast(rv.values(), lambda u: str(u["rev_date"])[:4]).items())},
        "top": {c: top(c) for c in CATS},
        "top_cn_pass": [{"ein": u["ein"], "name": u["name_filed"][:45], "cat": u["category"], "sub": u["sub"],
                         "dw": round(u["dw"])} for u in sorted((u for u in units if cn_pass(u)), key=lambda u: -u["dw"])[:12]],
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
