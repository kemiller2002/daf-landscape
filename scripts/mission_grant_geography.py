#!/usr/bin/env python3
"""Where DAF grant dollars land: state and metro geography of top-50 sponsors' Schedule I grants, FY2023-FY2024
(queue item P-NEW-GEO-01).

Universe, return choice, full Schedule I line cache and DAF-to-DAF exclusion are those of
scripts/mission_recipient_sectors.py (top-50 DAFRC sponsors by FY2024 DAF assets; one return per sponsor x FY;
94 itemising sponsor-years; lines to `include` EINs in daf-to-daf-recipient-whitelist.csv and self-lines removed).

Steps (pure transforms; I/O at the edges)
  1. Address   The line cache keeps state only, so each return's Schedule I Part II RecipientTable is re-read for
               ZIPCd/CityNm (local XML copy, else the GivingTuesday mirror of IRS TEOS, streamed). A return's ZIPs
               are accepted only when the re-read gives the same line count and the same EIN/amount sequence as
               the cache.
  2. State     Schedule I recipient state (USAddress StateAbbreviationCd). Lines with a foreign address are
               set aside (`foreign_part_ii`); lines with no address fall back to the recipient's EO BMF STATE.
  3. Metro     ZIP5 (Schedule I, or BMF ZIP when the state came from the BMF) -> 2020 ZCTA -> county with the
               largest land-area overlap (Census rel2020 ZCTA520-county file) -> CBSA (county rows of Census
               cbsa-est2024-alldata.csv, July 2023 delineations). Connecticut's 2020 counties are mapped to the
               2023 planning-region CBSAs by a fixed approximate table (CT_OLD_COUNTY_CBSA). A ZIP that is not a
               ZCTA (PO box, lockbox, unique ZIP) takes the CBSA holding at least half of its ZIP3's ZCTAs.
               Sensitivity: state shares re-keyed on the recipient's BMF state (`amount_bmf_state_basis_usd`),
               since Schedule I often carries a remittance/lockbox address rather than the charity's office.
  4. Denominators  Census Vintage 2024 resident population (July 2023 and July 2024) for states and CBSAs;
               EO BMF count of SUBSECTION 03 organisations by STATE and by ZIP5 -> CBSA (2026-11 snapshot).
  5. Outputs   state (and CBSA) dollar shares, per-capita and per-501(c)(3) dollars, concentration, and each
               sponsor's own-state / own-metro share (community foundations vs national sponsors).

Stdlib only; functional style.

Usage:
  python3 scripts/mission_grant_geography.py --np-cache NPCACHE --bmf-dir BMF --lines-cache LC \
      --census-dir CENSUS --zip-cache ZC [--xml-list FILE] [--fetch]
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
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import BMF_FILES, COST, SVCF, WHITELIST, annotate, load_lines  # noqa: E402

OUT_STATE = os.path.join(DATA, "daf-grant-geography-state-2023-2024.csv")
OUT_LOCAL = os.path.join(DATA, "daf-grant-geography-cf-local-share.csv")
ZIP_V = 2
SOURCE = ("IRS Form 990 Schedule I Part II (e-file XML; GivingTuesday mirror of IRS TEOS), all lines, top-50 DAFRC "
          "sponsors FY2023-2024, DAF-to-DAF lines excluded (daf-to-daf-recipient-whitelist.csv); state from Schedule I "
          "recipient address, else IRS EO BMF STATE (2026-11-09); Census Vintage 2024 population (NST-EST2024-ALLDATA, "
          "cbsa-est2024-alldata); Census rel2020 ZCTA520-county; 501(c)(3) counts from EO BMF SUBSECTION 03")

STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
    "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky",
    "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
    "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota",
    "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
    "PR": "Puerto Rico"}
OTHER_US = {"GU", "VI", "AS", "MP", "FM", "MH", "PW", "AA", "AE", "AP"}  # territories and military post codes
US_CODES = frozenset(STATE_NAMES) | OTHER_US
STATE_FIPS = {"01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA", "08": "CO", "09": "CT", "10": "DE",
              "11": "DC", "12": "FL", "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN", "19": "IA",
              "20": "KS", "21": "KY", "22": "LA", "23": "ME", "24": "MD", "25": "MA", "26": "MI", "27": "MN",
              "28": "MS", "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH", "34": "NJ", "35": "NM",
              "36": "NY", "37": "NC", "38": "ND", "39": "OH", "40": "OK", "41": "OR", "42": "PA", "44": "RI",
              "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT", "50": "VT", "51": "VA", "53": "WA",
              "54": "WV", "55": "WI", "56": "WY", "72": "PR"}
# 2020 Connecticut counties -> 2023-delineation CBSA (planning regions). Approximate: New Haven County is split
# between New Haven (35300) and Waterbury (47930); Middlesex and Tolland partly fall in other regions.
CT_OLD_COUNTY_CBSA = {"09001": "14860", "09003": "25540", "09005": "45860", "09007": "25540", "09009": "35300",
                      "09011": "35980", "09013": "25540", "09015": "39480"}
SCOPES = ("all_top50_itemising", "all_ex_university_hospital", "all_ex_uh_ex_svcf", "national", "processor",
          "community_foundation", "community_foundation_ex_svcf", "single_issue", "university_hospital")


# ----------------------------------------------------------------------------- 1. Schedule I addresses
def addr_of(el) -> list:
    g = {local(c.tag): c for c in el.iter()}
    t = lambda k: (g[k].text or "").strip() if k in g and g[k].text else ""  # noqa: E731
    e = ein9(t("RecipientEIN")) if t("RecipientEIN") else ""
    zp = t("ZIPCd")[:5] if "USAddress" in g or "ZIPCd" in g else ""
    return [e if e.strip("0") else "", (num(t("CashGrantAmt")) or 0.0) + (num(t("NonCashAssistanceAmt")) or 0.0),
            zp, t("CityNm")[:40]]


def parse_addr(stream) -> tuple[list, dict]:
    """-> (RecipientTable [ein, amount, zip5, city] in order, filer header {state, zip5})."""
    out, filer = [], {}
    for _, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        if tag == "RecipientTable":
            out.append(addr_of(el))
            el.clear()
        elif tag == "Filer" and not filer:
            g = {local(c.tag): (c.text or "").strip() for c in el.iter() if c.text}
            filer = {"state": g.get("StateAbbreviationCd", ""), "zip5": g.get("ZIPCd", "")[:5]}
        elif tag.startswith("IRS990") and tag != "IRS990ScheduleI":
            el.clear()
    return out, filer


def same_lines(addr: Sequence, lines: Sequence) -> bool:
    return len(addr) == len(lines) and all(a[0] == (l[0] if l[0].strip("0") else "") and abs(a[1] - l[4] - l[5]) < 0.5
                                           for a, l in zip(addr, lines))


def load_addr(oid: str, lines: Sequence, cache: str, xml_paths: Mapping, fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == ZIP_V:
            return c
    tried = []
    for p in xml_paths.get(oid, ()):
        try:
            with open(p, "rb") as fh:
                a, filer = parse_addr(fh)
        except (ET.ParseError, OSError):
            tried.append(f"{p}:parse_error")
            continue
        if same_lines(a, lines):
            return save(path, {"zip_city": [x[2:] for x in a], "filer": filer, "status": "ok", "via": "local", "_v": ZIP_V})
        tried.append(f"{p}:mismatch")
    if not fetch:
        return {"status": "not_fetched", "zip_city": [], "tried": tried}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                a, filer = parse_addr(resp)
            if same_lines(a, lines):
                return save(path, {"zip_city": [x[2:] for x in a], "filer": filer, "status": "ok", "via": "mirror", "_v": ZIP_V})
            return {"status": "mismatch_mirror", "zip_city": []}
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"status": f"http_{e.code}", "zip_city": []}
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError):
            time.sleep(3 * (attempt + 1))
    return {"status": "error", "zip_city": []}


def save(path: str, obj: dict) -> dict:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh)
    return obj


# ----------------------------------------------------------------------------- 2. reference data
def scan_bmf(bmf_dir: str, eins: frozenset) -> tuple[dict, dict, dict]:
    """-> (ein -> fields for eins of interest, 501(c)(3) count by STATE, 501(c)(3) count by ZIP5)."""
    rec, by_state, by_zip = {}, {}, {}
    for f in BMF_FILES:
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="latin-1", newline="") as fh:
            for r in csv.DictReader(fh):
                st, zp, sub = (r.get("STATE") or "").strip(), (r.get("ZIP") or "").strip()[:5], (r.get("SUBSECTION") or "").strip()
                if sub == "03":
                    by_state[st] = by_state.get(st, 0) + 1
                    by_zip[zp] = by_zip.get(zp, 0) + 1
                e = ein9(r["EIN"])
                if e in eins:
                    rec[e] = {"ntee": (r.get("NTEE_CD") or "").strip().upper(), "foundation": (r.get("FOUNDATION") or "").strip(),
                              "subsection": sub, "bmf_name": (r.get("NAME") or "").strip(), "bmf_state": st, "bmf_zip": zp,
                              "bmf_city": (r.get("CITY") or "").strip()}
    return rec, by_state, by_zip


def state_pop(path: str) -> dict:
    rows = read_csv(path)
    return {STATE_FIPS[r["STATE"]]: {"pop_2023": int(r["POPESTIMATE2023"]), "pop_2024": int(r["POPESTIMATE2024"])}
            for r in rows if r["SUMLEV"] == "040" and r["STATE"] in STATE_FIPS}


def cbsa_tables(path: str) -> tuple[dict, dict]:
    """-> (cbsa -> {name, lsad, pop_2023, pop_2024}, county FIPS -> cbsa)."""
    with open(path, encoding="latin-1", newline="") as fh:
        rows = tuple(csv.DictReader(fh))
    cb = {r["CBSA"]: {"name": r["NAME"], "lsad": r["LSAD"], "pop_2023": int(r["POPESTIMATE2023"]),
                      "pop_2024": int(r["POPESTIMATE2024"])}
          for r in rows if not r["MDIV"] and not r["STCOU"]}
    county = {r["STCOU"]: r["CBSA"] for r in rows if r["STCOU"]}
    return cb, {**county, **CT_OLD_COUNTY_CBSA}


def zip3_fallback(zip_cbsa: Mapping, zctas: frozenset) -> dict:
    """ZIP3 -> CBSA held by the most 2020 ZCTAs in that ZIP3 (CBSA-assigned or not), when that CBSA holds at least
    half of them. Used only for ZIPs that are not ZCTAs (PO boxes, lockboxes, unique-organisation ZIPs)."""
    cnt = {}
    for z in zctas:
        d = cnt.setdefault(z[:3], {})
        c = zip_cbsa.get(z, "")
        d[c] = d.get(c, 0) + 1
    out = {}
    for z3, d in cnt.items():
        c, n = max(d.items(), key=lambda kv: kv[1])
        if c and n * 2 >= sum(d.values()):
            out[z3] = c
    return out


def zcta_county(path: str) -> dict:
    """ZCTA5 -> county FIPS with the largest land-area overlap (2020 relationship file)."""
    best = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="|"):
            z, c = r["GEOID_ZCTA5_20"], r["GEOID_COUNTY_20"]
            if not z:
                continue
            a = int(r["AREALAND_PART"] or 0)
            if z not in best or a > best[z][1]:
                best[z] = (c, a)
    return {z: c for z, (c, _) in best.items()}


# ----------------------------------------------------------------------------- 3. geocode lines
def cbsa_of(z: str, zip_cbsa: Mapping, zctas: frozenset, z3: Mapping) -> tuple[str, str]:
    if not z:
        return "", ""
    if z in zctas:
        return zip_cbsa.get(z, ""), "zcta" if zip_cbsa.get(z) else "zcta_non_cbsa"
    return (z3[z[:3]], "zip3_fallback") if z[:3] in z3 else ("", "zip_unresolved")


def geo_line(r: Mapping, zc: Sequence, bmf: Mapping, zip_cbsa: Mapping, zctas: frozenset, z3: Mapping) -> dict:
    b = bmf.get(r["ein"], {}) if r["ein"] else {}
    w = r["where"]
    if w.startswith("F:"):
        st, src = "FOREIGN_PART_II", "sched_i_foreign"
    elif w in US_CODES:
        st, src = w, "sched_i"
    elif b.get("bmf_state") in US_CODES:
        st, src = b["bmf_state"], "bmf_fallback"
    else:
        st, src = "UNKNOWN", "none"
    z = (zc[0] if zc else "") if src == "sched_i" else (b.get("bmf_zip", "") if src == "bmf_fallback" else "")
    zsrc = "sched_i" if src == "sched_i" and z else ("bmf" if z else "")
    if src == "sched_i" and not z and b.get("bmf_state") == st and b.get("bmf_zip"):
        z, zsrc = b["bmf_zip"], "bmf_same_state"
    c, cm = cbsa_of(z, zip_cbsa, zctas, z3)
    alt = b["bmf_state"] if b.get("bmf_state") in US_CODES and st in US_CODES else st
    return {**r, "state": st, "state_src": src, "zip5": z, "zip_src": zsrc, "cbsa": c, "cbsa_method": cm,
            "bmf_state": b.get("bmf_state", ""), "alt_state": alt}


# ----------------------------------------------------------------------------- 4. aggregate
def scope_preds(panel: Mapping) -> dict:
    seg = lambda e: panel[e]["segment"]  # noqa: E731
    return {"all_top50_itemising": lambda e: True,
            "all_ex_university_hospital": lambda e: seg(e) != "university_hospital",
            "all_ex_uh_ex_svcf": lambda e: seg(e) != "university_hospital" and e != SVCF,
            "community_foundation_ex_svcf": lambda e: seg(e) == "community_foundation" and e != SVCF,
            **{s: (lambda e, s=s: seg(e) == s) for s in ("national", "processor", "community_foundation",
                                                           "single_issue", "university_hospital")}}


def sums(rows: Sequence[Mapping], key, weight: Mapping) -> dict:
    out = {}
    for r in rows:
        k = key(r)
        d = out.setdefault(k, {"usd": 0.0, "usd_w": 0.0, "fy2023": 0.0, "fy2024": 0.0, "lines": 0, "rec": set(),
                               "src_sched_i": 0.0, "src_bmf": 0.0, "by_rec": {}, "sponsors": set(), "zip3": 0.0})
        a = r["amount"]
        d["usd"] += a
        d["usd_w"] += a * weight.get(r["_sy"], 1.0)
        d[f"fy{r['_sy'][1]}"] += a
        d["lines"] += 1
        d["rec"].add(r["key"])
        d["sponsors"].add(r["_sy"][0])
        d["src_sched_i"] += a if r["state_src"] == "sched_i" else 0.0
        d["src_bmf"] += a if r["state_src"] == "bmf_fallback" else 0.0
        d["by_rec"][r["key"]] = d["by_rec"].get(r["key"], 0.0) + a
        d["zip3"] += a if r["cbsa_method"] == "zip3_fallback" else 0.0
    return out


def hhi(vals: Sequence[float]) -> float | None:
    t = sum(vals)
    return sum((v / t * 100) ** 2 for v in vals) if t else None


def top_share(vals: Sequence[float], n: int) -> float | None:
    t = sum(vals)
    return sum(sorted(vals, reverse=True)[:n]) / t if t else None


def geo_rows(scope: str, geo_type: str, agg: Mapping, denom: Mapping, names: Mapping, c3: Mapping,
             rec_name: Mapping, weight_on: bool, alt: Mapping) -> list:
    tot = sum(d["usd"] for d in agg.values())
    tot_w = sum(d["usd_w"] for d in agg.values())
    dom = {k: d for k, d in agg.items() if k in denom}
    tot_dom = sum(d["usd"] for d in dom.values())
    ranked = sorted(agg.items(), key=lambda kv: -kv[1]["usd"])
    rank_dom = {k: i + 1 for i, (k, _) in enumerate((kv for kv in ranked if kv[0] in denom))}
    pc = {k: (d["usd"] / 2) / ((denom[k]["pop_2023"] + denom[k]["pop_2024"]) / 2) for k, d in dom.items()}
    pc_rank = {k: i + 1 for i, (k, _) in enumerate(sorted(pc.items(), key=lambda kv: -kv[1]))}

    def one(k, d):
        p = denom.get(k)
        top = sorted(d["by_rec"].items(), key=lambda kv: -kv[1])
        n3 = c3.get(k)
        return {"scope": scope, "geo_type": geo_type, "geo_code": k, "geo_name": names.get(k, k),
                "fiscal_years": "2023-2024", "amount_usd": round(d["usd"]), "share_of_net": d["usd"] / tot if tot else None,
                "share_of_us_located": d["usd"] / tot_dom if p and tot_dom else None,
                "amount_fy2023_usd": round(d["fy2023"]), "amount_fy2024_usd": round(d["fy2024"]),
                "amount_daf_weighted_usd": round(d["usd_w"]) if weight_on else "",
                "share_daf_weighted": (d["usd_w"] / tot_w if tot_w else None) if weight_on else "",
                "rank_by_amount": rank_dom.get(k, ""), "lines": d["lines"], "recipients": len(d["rec"]),
                "sponsors": len(d["sponsors"]),
                "pop_2023": p["pop_2023"] if p else "", "pop_2024": p["pop_2024"] if p else "",
                "usd_per_capita_per_year": pc.get(k) if p else "", "rank_per_capita": pc_rank.get(k, ""),
                "c3_orgs_bmf": n3 if n3 is not None else "",
                "usd_per_c3_per_year": (d["usd"] / 2 / n3) if n3 else "",
                "c3_per_10k_pop": (n3 / p["pop_2024"] * 1e4) if (n3 and p) else "",
                "state_from_sched_i_usd": round(d["src_sched_i"]), "state_from_bmf_usd": round(d["src_bmf"]),
                "amount_bmf_state_basis_usd": round(alt[k]) if k in alt else "",
                "cbsa_via_zip3_fallback_usd": round(d["zip3"]) if geo_type == "cbsa" else "",
                "top_recipient": rec_name.get(top[0][0], top[0][0])[:80] if top else "",
                "top_recipient_usd": round(top[0][1]) if top else "",
                "top5_recipient_share": top_share([v for _, v in top], 5), "source": SOURCE}
    return [one(k, d) for k, d in ranked]


def state_names_cbsa(cb: Mapping) -> dict:
    return {k: v["name"] for k, v in cb.items()}


def own_share_rows(ann: Mapping, panel: Mapping, rank: Mapping, bmf: Mapping, zc_of, cb: Mapping,
                   d2d_tot: Mapping, filer_addr: Mapping) -> list:
    """Sponsor home = EO BMF STATE/ZIP; when the sponsor is not in the BMF, the latest return's Filer address."""
    by_sp = _group_by_fast(((k[0], r) for k, rs in ann.items() for r in rs), lambda t: t[0])
    out = []
    for e, pairs in by_sp.items():
        rs = [r for _, r in pairs]
        b = bmf.get(e) or {"bmf_state": filer_addr.get(e, {}).get("state", ""), "bmf_zip": filer_addr.get(e, {}).get("zip5", ""),
                           "_src": "filer_header"}
        st, home_cbsa = b.get("bmf_state", ""), zc_of(b.get("bmf_zip", ""))
        tot = sum(r["amount"] for r in rs)
        dom = [r for r in rs if r["state"] in US_CODES]
        tot_dom = sum(r["amount"] for r in dom)
        own = sum(r["amount"] for r in dom if r["state"] == st)
        cbsa_known = [r for r in dom if r["cbsa"]]
        tot_cb = sum(r["amount"] for r in cbsa_known)
        own_cb = sum(r["amount"] for r in cbsa_known if r["cbsa"] == home_cbsa) if home_cbsa else 0.0
        by_st = {}
        for r in dom:
            by_st[r["state"]] = by_st.get(r["state"], 0.0) + r["amount"]
        out_st = sorted(((k, v) for k, v in by_st.items() if k != st), key=lambda kv: -kv[1])
        nat_pull = sum(by_st.get(s, 0.0) for s in ("DC", "NY", "MA", "CA") if s != st)
        out.append({
            "sponsor_ein": e, "sponsor_name": panel[e]["name"], "segment": panel[e]["segment"],
            "sponsor_rank_fy2024": rank.get(e, ""), "sponsor_state": st, "sponsor_home_source": b.get("_src", "bmf"),
            "sponsor_cbsa": home_cbsa,
            "sponsor_cbsa_name": cb.get(home_cbsa, {}).get("name", ""),
            "fiscal_years": ";".join(sorted({str(k[1]) for k in ann if k[0] == e})),
            "net_usd": round(tot), "d2d_excluded_usd": round(d2d_tot.get(e, 0.0)), "us_located_usd": round(tot_dom),
            "foreign_part_ii_usd": round(sum(r["amount"] for r in rs if r["state"] == "FOREIGN_PART_II")),
            "unknown_state_usd": round(sum(r["amount"] for r in rs if r["state"] == "UNKNOWN")),
            "own_state_usd": round(own), "own_state_share": own / tot_dom if tot_dom else None,
            "cbsa_resolved_usd": round(tot_cb), "own_cbsa_usd": round(own_cb),
            "own_cbsa_share_of_resolved": own_cb / tot_cb if tot_cb and home_cbsa else None,
            "states_reached": len(by_st),
            "top_other_state": out_st[0][0] if out_st else "", "top_other_state_usd": round(out_st[0][1]) if out_st else "",
            "dc_ny_ma_ca_out_of_state_share": nat_pull / tot_dom if tot_dom else None,
            "recipients": len({r["key"] for r in rs}), "source": SOURCE})
    return sorted(out, key=lambda r: (r["segment"], r["sponsor_rank_fy2024"] or 999))


STATE_FIELDS = ("scope", "geo_type", "geo_code", "geo_name", "fiscal_years", "amount_usd", "share_of_net",
                "share_of_us_located", "amount_fy2023_usd", "amount_fy2024_usd", "amount_daf_weighted_usd",
                "share_daf_weighted", "rank_by_amount", "lines", "recipients", "sponsors", "pop_2023", "pop_2024",
                "usd_per_capita_per_year", "rank_per_capita", "c3_orgs_bmf", "usd_per_c3_per_year", "c3_per_10k_pop",
                "state_from_sched_i_usd", "state_from_bmf_usd", "amount_bmf_state_basis_usd",
                "cbsa_via_zip3_fallback_usd", "top_recipient", "top_recipient_usd",
                "top5_recipient_share", "source")
LOCAL_FIELDS = ("sponsor_ein", "sponsor_name", "segment", "sponsor_rank_fy2024", "sponsor_state", "sponsor_home_source",
                "sponsor_cbsa",
                "sponsor_cbsa_name", "fiscal_years", "net_usd", "d2d_excluded_usd", "us_located_usd",
                "foreign_part_ii_usd", "unknown_state_usd", "own_state_usd", "own_state_share", "cbsa_resolved_usd",
                "own_cbsa_usd", "own_cbsa_share_of_resolved", "states_reached", "top_other_state",
                "top_other_state_usd", "dc_ny_ma_ca_out_of_state_share", "recipients", "source")


def median(xs: Sequence[float]) -> float | None:
    s = sorted(xs)
    n = len(s)
    return None if not n else (s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2)


def r4(x):
    return round(x, 4) if isinstance(x, float) else x


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--census-dir", required=True)
    ap.add_argument("--zip-cache", required=True)
    ap.add_argument("--xml-list", default="")
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    item = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen and itemized(chosen[(e, fy)])}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: v for k, v in loaded.items() if v["status"] == "ok"}

    xml_paths = {}
    if a.xml_list:
        with open(a.xml_list, encoding="utf-8") as fh:
            for p in (l.strip() for l in fh if l.strip()):
                p = p if os.path.isabs(p) else os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(a.xml_list)), "..", p))
                xml_paths.setdefault(os.path.basename(p).replace("_public.xml", "").replace(".xml", ""), []).append(p)
    addrs = {k: load_addr(item[k]["oid"], v["lines"], a.zip_cache, xml_paths, a.fetch) for k, v in good.items()}
    addr_bad = {f"{panel[k[0]]['name']} FY{k[1]}": v["status"] for k, v in addrs.items() if v["status"] != "ok"}

    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    names = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in names.items() if k and len(v) == 1}
    eins = frozenset(l[0] for v in good.values() for l in v["lines"] if l[0]) | frozenset(rank)
    bmf, c3_state, c3_zip = scan_bmf(a.bmf_dir, eins)

    spop = state_pop(os.path.join(a.census_dir, "NST-EST2024-ALLDATA.csv"))
    cb, county_cbsa = cbsa_tables(os.path.join(a.census_dir, "cbsa-est2024-alldata.csv"))
    z2c = zcta_county(os.path.join(a.census_dir, "tab20_zcta520_county20_natl.txt"))
    zip_cbsa = {z: county_cbsa[c] for z, c in z2c.items() if c in county_cbsa}
    zctas = frozenset(z2c)
    z3 = zip3_fallback(zip_cbsa, zctas)
    zc_of = lambda z: cbsa_of(z, zip_cbsa, zctas, z3)[0]  # noqa: E731
    c3_cbsa = {}
    for z, n in c3_zip.items():
        c = zc_of(z)
        if c:
            c3_cbsa[c] = c3_cbsa.get(c, 0) + n
    c3_zip_resolved = sum(n for z, n in c3_zip.items() if zc_of(z))

    cost = read_csv(COST)
    share = {(ein9(r["ein"]), int(r["fiscal_year"])): num(r["daf_share_of_grants"]) for r in cost if r["daf_share_of_grants"]}
    weights = {k: min(1.0, max(0.0, share[k])) for k in good if share.get(k) is not None}

    ann_all = {}
    for k, v in good.items():
        zc = addrs[k]["zip_city"] if addrs[k]["status"] == "ok" else [[] for _ in v["lines"]]
        rows = annotate(k[0], v["lines"], bmf, wl_eins, wl_names)
        ann_all[k] = tuple({**geo_line(r, z, bmf, zip_cbsa, zctas, z3), "_sy": k} for r, z in zip(rows, zc))
    d2d_tot = {}
    for k, rs in ann_all.items():
        d2d_tot[k[0]] = d2d_tot.get(k[0], 0.0) + sum(r["amount"] for r in rs if r["d2d"])
    ann = {k: tuple(r for r in rs if not r["d2d"]) for k, rs in ann_all.items()}

    rec_name = {}
    for rs in ann.values():
        for r in rs:
            rec_name.setdefault(r["key"], (bmf.get(r["ein"], {}).get("bmf_name") or r["name"]))
    preds = scope_preds(panel)
    st_names = {**STATE_NAMES, "FOREIGN_PART_II": "Foreign address (Schedule I Part II)", "UNKNOWN": "No state"}
    cb_names = state_names_cbsa(cb)
    out_rows, aggs, alts = [], {}, {}
    for s in SCOPES:
        rs = tuple(r for k, x in ann.items() if preds[s](k[0]) for r in x)
        ag = sums(rs, lambda r: r["state"], weights)
        alt = {}
        for r in rs:
            alt[r["alt_state"]] = alt.get(r["alt_state"], 0.0) + r["amount"]
        aggs[s] = (rs, ag)
        alts[s] = alt
        out_rows += geo_rows(s, "state", ag, spop, st_names, c3_state, rec_name, True, alt)
    for s in ("all_ex_university_hospital", "all_ex_uh_ex_svcf", "national", "community_foundation"):
        rs = aggs[s][0]
        ag = sums([r for r in rs if r["cbsa"]], lambda r: r["cbsa"], weights)
        out_rows += geo_rows(s, "cbsa", ag, cb, cb_names, c3_cbsa, rec_name, True, {})
    write_csv(OUT_STATE, out_rows, STATE_FIELDS)

    filer_addr = {k[0]: v.get("filer", {}) for k, v in sorted(addrs.items(), key=lambda kv: kv[0][1])}
    local_rows = own_share_rows(ann, panel, rank, bmf, zc_of, cb, d2d_tot, filer_addr)
    write_csv(OUT_LOCAL, local_rows, LOCAL_FIELDS)

    # ------------------------------------------------------------- summary
    def scope_sum(s):
        rs, ag = aggs[s]
        tot = sum(d["usd"] for d in ag.values())
        dom = {k: d["usd"] for k, d in ag.items() if k in spop}
        cbs = {}
        for r in rs:
            if r["cbsa"]:
                cbs[r["cbsa"]] = cbs.get(r["cbsa"], 0.0) + r["amount"]
        metro = {k: v for k, v in cbs.items() if cb.get(k, {}).get("lsad") == "Metropolitan Statistical Area"}
        top_st = sorted(dom.items(), key=lambda kv: -kv[1])
        top_cb = sorted(cbs.items(), key=lambda kv: -kv[1])
        sd = sum(dom.values())
        return {"net_usd": round(tot), "us_state_usd": round(sd),
                "foreign_part_ii_usd": round(ag.get("FOREIGN_PART_II", {}).get("usd", 0.0)),
                "unknown_usd": round(ag.get("UNKNOWN", {}).get("usd", 0.0)),
                "other_us_codes_usd": round(sum(d["usd"] for k, d in ag.items() if k in OTHER_US)),
                "state_src_sched_i_share": r4(sum(d["src_sched_i"] for d in ag.values()) / tot) if tot else None,
                "state_src_bmf_share": r4(sum(d["src_bmf"] for d in ag.values()) / tot) if tot else None,
                "top_states": [(k, round(v), r4(v / sd)) for k, v in top_st[:10]],
                "top5_state_share": r4(top_share(list(dom.values()), 5)), "top10_state_share": r4(top_share(list(dom.values()), 10)),
                "state_hhi": round(hhi(list(dom.values())), 1) if dom else None,
                "pop_top5_share": r4(sum(spop[k]["pop_2024"] for k, _ in top_st[:5]) / sum(p["pop_2024"] for p in spop.values())),
                "cbsa_resolved_share_of_us": r4(sum(cbs.values()) / sd) if sd else None,
                "cbsa_method_share_of_us": {m: r4(sum(r["amount"] for r in rs if r["state"] in US_CODES and r["cbsa_method"] == m) / sd)
                                            for m in ("zcta", "zip3_fallback", "zcta_non_cbsa", "zip_unresolved", "")} if sd else None,
                "bmf_state_basis_top": [(k, round(v), r4(v / sum(x for kk, x in alts[s].items() if kk in spop)))
                                        for k, v in sorted(((k, v) for k, v in alts[s].items() if k in spop), key=lambda kv: -kv[1])[:10]],
                "top_cbsa": [(cb[k]["name"], round(v), r4(v / sum(cbs.values()))) for k, v in top_cb[:12]],
                "top10_cbsa_share": r4(top_share(list(cbs.values()), 10)),
                "metro_share_of_cbsa_resolved": r4(sum(metro.values()) / sum(cbs.values())) if cbs else None,
                "cbsa_hhi": round(hhi(list(cbs.values())), 1) if cbs else None,
                "pop_top10_cbsa_share": r4(sum(cb[k]["pop_2024"] for k, _ in top_cb[:10]) / sum(spop[s]["pop_2024"] for s in spop))}

    def pc_table(s, keys):
        ag = aggs[s][1]
        return {k: {"usd": round(ag.get(k, {}).get("usd", 0.0)),
                    "per_capita_yr": round(ag.get(k, {}).get("usd", 0.0) / 2 / ((spop[k]["pop_2023"] + spop[k]["pop_2024"]) / 2), 2),
                    "per_c3_yr": round(ag.get(k, {}).get("usd", 0.0) / 2 / c3_state[k]) if c3_state.get(k) else None}
                for k in keys}

    def pc_rank(s, n=10):
        ag = aggs[s][1]
        pc = {k: ag[k]["usd"] / 2 / ((spop[k]["pop_2023"] + spop[k]["pop_2024"]) / 2) for k in ag if k in spop}
        pcc = {k: ag[k]["usd"] / 2 / c3_state[k] for k in ag if k in spop and c3_state.get(k)}
        us = sum(ag[k]["usd"] for k in ag if k in spop) / 2 / sum((spop[k]["pop_2023"] + spop[k]["pop_2024"]) / 2 for k in spop)
        usc = sum(ag[k]["usd"] for k in ag if k in spop) / 2 / sum(c3_state.get(k, 0) for k in spop)
        srt = sorted(pc.items(), key=lambda kv: -kv[1])
        srtc = sorted(pcc.items(), key=lambda kv: -kv[1])
        return {"us_per_capita_yr": round(us, 2), "us_per_c3_yr": round(usc), "median_state_per_capita": round(median(list(pc.values())), 2),
                "top_pc": [(k, round(v, 2)) for k, v in srt[:n]], "bottom_pc": [(k, round(v, 2)) for k, v in srt[-n:]],
                "top_per_c3": [(k, round(v)) for k, v in srtc[:n]], "bottom_per_c3": [(k, round(v)) for k, v in srtc[-5:]],
                "max_min_pc_ratio": round(srt[0][1] / srt[-1][1], 1),
                "max_min_pc_ratio_ex_dc": round(next(v for k, v in srt if k != "DC") / srt[-1][1], 1)}

    home = {r["sponsor_ein"]: r["sponsor_state"] for r in local_rows}

    def outlier(s, st, n=6):
        rs = [r for r in aggs[s][0] if r["state"] == st]
        by = {}
        for r in rs:
            d = by.setdefault(r["key"], {"usd": 0.0, "sponsors": set(), "grp": r["group"]})
            d["usd"] += r["amount"]
            d["sponsors"].add(r["_sy"][0])
        tot = sum(d["usd"] for d in by.values())
        top = sorted(by.items(), key=lambda kv: -kv[1]["usd"])[:n]
        grp = {}
        for r in rs:
            grp[r["group"]] = grp.get(r["group"], 0.0) + r["amount"]
        multi = sum(d["usd"] for d in by.values() if len(d["sponsors"]) >= 10)
        # dollars from sponsors headquartered elsewhere (BMF state of sponsor != recipient state)
        from_out = sum(r["amount"] for r in rs if home.get(r["_sy"][0]) != st)
        cf_from_out = sum(r["amount"] for r in rs if panel[r["_sy"][0]]["segment"] == "community_foundation"
                          and home.get(r["_sy"][0]) != st)
        return {"usd": round(tot), "top": [(rec_name.get(k, k)[:50], round(d["usd"]), len(d["sponsors"]), d["grp"]) for k, d in top],
                "top5_share": r4(top_share([d["usd"] for d in by.values()], 5)),
                "share_to_recipients_with_10plus_sponsors": r4(multi / tot) if tot else None,
                "share_from_sponsors_hq_elsewhere": r4(from_out / tot) if tot else None,
                "cf_dollars_from_out_of_state_cfs": round(cf_from_out),
                "groups": {g: r4(v / tot) for g, v in sorted(grp.items(), key=lambda kv: -kv[1])[:6]}}

    def local_stats(seg, excl=()):
        xs = [r for r in local_rows if r["segment"] == seg and r["sponsor_ein"] not in excl and r["own_state_share"] is not None]
        num_ = sum(r["own_state_usd"] for r in xs)
        den = sum(r["us_located_usd"] for r in xs)
        cbx = [r for r in xs if r["own_cbsa_share_of_resolved"] is not None]
        return {"n": len(xs), "pooled_own_state_share": r4(num_ / den) if den else None,
                "median_own_state_share": r4(median([r["own_state_share"] for r in xs])),
                "min": r4(min((r["own_state_share"] for r in xs), default=None)) if xs else None,
                "max": r4(max((r["own_state_share"] for r in xs), default=None)) if xs else None,
                "pooled_own_cbsa_share": r4(sum(r["own_cbsa_usd"] for r in cbx) / sum(r["cbsa_resolved_usd"] for r in cbx)) if cbx else None,
                "median_own_cbsa_share": r4(median([r["own_cbsa_share_of_resolved"] for r in cbx])) if cbx else None,
                "median_states_reached": median([r["states_reached"] for r in xs]),
                "pooled_dc_ny_ma_ca_out_of_state": r4(sum(r["dc_ny_ma_ca_out_of_state_share"] * r["us_located_usd"] for r in xs) / den) if den else None}

    # Schedule I state vs BMF state agreement (EIN-matched, US lines)
    both = [r for rs in ann.values() for r in rs if r["state_src"] == "sched_i" and r["bmf_state"] in US_CODES]
    agree = sum(r["amount"] for r in both if r["state"] == r["bmf_state"])
    lines_all = [r for rs in ann.values() for r in rs]
    zip_src = {}
    for r in lines_all:
        zip_src[r["zip_src"] or "none"] = zip_src.get(r["zip_src"] or "none", 0.0) + r["amount"]
    tot_all = sum(r["amount"] for r in lines_all)
    # population-weighted expected share vs actual: share of US pop in the states with the top-5 dollar share
    summary = {
        "sponsor_years_itemising": len(item), "lines_loaded_ok": len(good), "addr_ok": sum(1 for v in addrs.values() if v["status"] == "ok"),
        "addr_problems": addr_bad, "addr_via": {s: sum(1 for v in addrs.values() if v.get("via") == s) for s in ("local", "mirror")},
        "net_lines": len(lines_all), "net_usd_all_top50": round(tot_all),
        "d2d_excluded_usd_all": round(sum(d2d_tot.values())),
        "zip_source_share_all": {k: r4(v / tot_all) for k, v in sorted(zip_src.items(), key=lambda kv: -kv[1])},
        "sched_i_vs_bmf_state_agreement_usd_share": r4(agree / sum(r["amount"] for r in both)) if both else None,
        "sched_i_vs_bmf_state_compared_usd": round(sum(r["amount"] for r in both)),
        "zcta_count": len(z2c), "zip_cbsa_count": len(zip_cbsa), "c3_total_bmf_us": sum(c3_state.get(k, 0) for k in spop),
        "c3_in_cbsa_share": r4(sum(c3_cbsa.values()) / sum(c3_zip.values())), "c3_zip_resolved": c3_zip_resolved,
        "scopes": {s: scope_sum(s) for s in ("all_ex_university_hospital", "all_ex_uh_ex_svcf", "national", "processor",
                                             "community_foundation", "community_foundation_ex_svcf", "single_issue")},
        "per_capita": {s: pc_rank(s) for s in ("all_ex_university_hospital", "all_ex_uh_ex_svcf", "national", "community_foundation")},
        "outlier_states": {s: pc_table(s, ("DC", "NY", "CA", "MA", "TX", "FL", "MS", "WV")) for s in ("all_ex_university_hospital", "all_ex_uh_ex_svcf", "national", "community_foundation")},
        "outlier_detail": {st: outlier("all_ex_university_hospital", st) for st in ("DC", "NY", "CA", "MA")},
        "local_share": {"community_foundation": local_stats("community_foundation"),
                        "community_foundation_ex_svcf": local_stats("community_foundation", (SVCF,)),
                        "national": local_stats("national"), "processor": local_stats("processor"),
                        "single_issue": local_stats("single_issue")},
        "local_rows": [(r["sponsor_name"][:34], r["segment"][:8], r["sponsor_state"], r4(r["own_state_share"]),
                        r4(r["own_cbsa_share_of_resolved"]), r["states_reached"], r["top_other_state"], r4(r["dc_ny_ma_ca_out_of_state_share"]))
                       for r in local_rows],
        "by_fy_all_ex_uh": {fy: {k: round(v["fy" + fy]) for k, v in sorted(aggs["all_ex_university_hospital"][1].items(),
                                                                           key=lambda kv: -kv[1]["fy" + fy])[:6]} for fy in ("2023", "2024")},
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
