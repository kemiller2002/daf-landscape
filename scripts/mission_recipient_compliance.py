#!/usr/bin/env python3
"""Recipient compliance screen: Schedule I grant recipients of the top-50 DAF sponsors, FY2023-FY2024, against
IRS public bulk data (queue item P-NEW-REC-01).

Universe, return choice and the full Schedule I Part II lines are exactly those of
scripts/mission_recipient_sectors.py (top-50 DAFRC sponsors by FY2024 DAF assets; one return per sponsor x DAFRC
fiscal year via mission_daf_to_daf.pick_returns; every RecipientTable line, cached one JSON per object id). The
DAF-to-DAF flag is that script's (`annotate`).

Each line (recipient EIN, name, amount, the sponsor's tax period) is checked against:
  (a) IRS Automatic Revocation of Exemption List (data-download-revocation.txt; pipe-delimited:
      EIN|name|dba|street|city|state|zip|country|subsection|revocation date|posting date|reinstatement date).
      For each line the latest revocation record with revocation date <= the sponsor's tax-period end is taken and
      compared with the tax period [start = end - 1 year + 1 day]:
        rev_before_not_reinstated   revoked before the period start, no reinstatement on or before period end
        rev_before_reinstated_in    revoked before the period start, reinstated during the period
        rev_during                  revoked during the period, not retroactively reinstated (reinst > rev date)
        rev_reinstated_before       context only: reinstated on or before the period start, or retroactively
        rev_after                   context only: first revocation after the period end
      The first three are "revoked before or during the grant year" screening hits. The posting date shows
      whether the revocation had been published by the end of the period (Rev. Proc. 2018-32 reliance turns on
      what the IRS had published).
  (b) Publication 78 data (data-download-pub78.txt: EIN|name|city|state|country|deductibility codes).
  (c) EO Business Master File extract (eo1-eo4, eo_pr, eo_xx): SUBSECTION, DEDUCTIBILITY, FOUNDATION, STATUS,
      AFFILIATION, GROUP, RULING.
Pub 78 and BMF are November 2026 snapshots, not as-of the grant year.

Labels that can legitimately explain an absence (never conclusions): government (sponsor's IRC text or name),
church_or_religious (BMF FOUNDATION 10, sponsor's IRC text "religious"/170(b)(1)(A)(i), or a congregation /
religious-order / yeshiva name rule), foreign address, possible_public_university and llc_possible_disregarded_entity
(only for EINs in neither Pub 78 nor the BMF; name rules), group_subordinate (BMF AFFILIATION 9 / GROUP code; covered by a central organisation's group ruling),
possible_ein_misreport (the Schedule I name matches exactly one Pub 78 name under another EIN), name_differs
(Schedule I name and BMF/Pub 78 name share under a third of their tokens: possible name change or wrong EIN).

Nothing here says a grant was improper. Every flag is a screening hit needing review.

Stdlib only; functional style.

Usage:
  python3 scripts/mission_recipient_compliance.py --np-cache NPCACHE --bmf-dir BMF --lines-cache LC \
      --pub78 data-download-pub78.txt --revocation data-download-revocation.txt [--hit-min 100000]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import BMF_FILES, WHITELIST, annotate, load_lines  # noqa: E402

OUT = os.path.join(DATA, "recipient-compliance-screen-top50.csv")
SOURCE = ("IRS Form 990 Schedule I Part II lines (universe/lines per mission_recipient_sectors.py) vs IRS Auto-"
          "Revocation List and Pub 78 data (apps.irs.gov/pub/epostcard/, Last-Modified 2026-11-11) and EO BMF "
          "(www.irs.gov/pub/irs-soi/eo*.csv, Last-Modified 2026-11-09)")
SEGMENTS = ("national", "community_foundation", "single_issue", "processor", "university_hospital")
REV_HITS = ("rev_before_not_reinstated", "rev_before_reinstated_in", "rev_during")
GOV_IRC = re.compile(r"GOV|170\s*\(?C\)?\s*\(?1\)?|PUBLIC SCHOOL|MUNICIPAL|STATE AGENCY|115")
GOV_NAME = re.compile(r"\b(CITY OF|COUNTY OF|STATE OF|TOWN OF|VILLAGE OF|TOWNSHIP|BOROUGH OF|COMMONWEALTH OF|"
                      r"SCHOOL DISTRICT|PUBLIC SCHOOLS|UNIFIED SCHOOL|INDEPENDENT SCHOOL DIST|BOARD OF EDUCATION|"
                      r"DEPARTMENT OF|BOARD OF REGENTS|REGENTS OF THE UNIVERSITY|UNITED STATES|NATIONAL PARK SERVICE|"
                      r"PUBLIC LIBRARY|FIRE DEPARTMENT|FIRE DISTRICT|POLICE DEPARTMENT|SHERIFF|PARKS AND RECREATION|"
                      r"STATE UNIVERSITY|CITY COLLEGE|COUNTY LIBRARY|LIBRARY DISTRICT|PARK DISTRICT|COUNTY SCHOOLS|"
                      r"CITY SCHOOLS|SCHOOL BOARD|HEALTH BOARD|INDIAN NATION|TRIBE|TRIBAL|PUEBLO OF|BAND OF)\b")
PLACEHOLDER = frozenset({"999999999", "123456789", "111111111", "000000001", "987654321"})
CHURCH_IRC = re.compile(r"RELIGIOUS|CHURCH|170\s*\(?B\)?\s*\(?1\)?\s*\(?A\)?\s*\(?I\)")
CHURCH_NAME = re.compile(r"\b(CHURCH|PARISH|DIOCESE|ARCHDIOCESE|SYNAGOGUE|CONGREGATION|CHABAD|MOSQUE|MASJID|"
                         r"ISLAMIC CENTER|CATHEDRAL|CHAPEL|SHUL|KEHILLA|TABERNACLE|ASSEMBLY OF GOD|SOCIETY OF JESUS|"
                         r"JESUITS?|SISTERS OF|ABBEY|MONASTERY|CONVENT|FRANCISCAN|DOMINICAN|YESHIVA|TORAH|KOLLEL|"
                         r"TALMUD)\b|\bTEMPLE\b(?!.*UNIVERSITY)")
PUBLIC_UNIV = re.compile(r"\b(UNIVERSITY|COLLEGE|CURATORS|REGENTS)\b")  # only used when absent from BMF and Pub 78
LLC = re.compile(r"\bL\.?\s?L\.?\s?C\b")
ER_CODES = ("PF", "SONFI")  # non-operating private foundation; non-functionally-integrated Type III SO


# ----------------------------------------------------------------------------- loaders (I/O edge)
def date_of(s: str):
    s = (s or "").strip()
    try:
        return dt.datetime.strptime(s, "%d-%b-%Y").date() if s else None
    except ValueError:
        return None


def load_revocations(path: str, eins: frozenset) -> dict:
    out = {}
    with open(path, encoding="latin-1", newline="") as fh:
        for raw in fh:
            p = raw.rstrip("\r\n").split("|")
            if len(p) < 12:
                continue
            e = ein9(p[0])
            if e in eins:
                out.setdefault(e, []).append({"name": (p[1] + " " + p[2]).strip(), "subsection": p[8].strip(),
                                              "rev": date_of(p[9]), "posted": date_of(p[10]), "reinst": date_of(p[11])})
    return {e: tuple(sorted(v, key=lambda r: r["rev"] or dt.date.min)) for e, v in out.items()}


def load_pub78(path: str, eins: frozenset, names: frozenset) -> tuple[dict, dict]:
    by_ein, by_name = {}, {}
    with open(path, encoding="latin-1", newline="") as fh:
        for raw in fh:
            p = raw.rstrip("\r\n").split("|")
            if len(p) < 6:
                continue
            e = ein9(p[0])
            if e in eins:
                by_ein[e] = {"name": p[1].strip(), "country": p[4].strip(), "codes": p[5].strip()}
            n = norm_name(p[1])
            if n in names:
                by_name.setdefault(n, set()).add(e)
    return by_ein, {k: frozenset(v) for k, v in by_name.items()}


def load_bmf_ext(bmf_dir: str, eins: frozenset) -> dict:
    keep = ("NAME", "SUBSECTION", "DEDUCTIBILITY", "FOUNDATION", "STATUS", "AFFILIATION", "GROUP", "RULING",
            "CLASSIFICATION", "STATE")
    out = {}
    for f in BMF_FILES:
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="latin-1", newline="") as fh:
            for r in csv.DictReader(fh):
                e = ein9(r["EIN"])
                if e in eins:
                    out[e] = {k.lower(): (r.get(k) or "").strip() for k in keep}
    return out


# ----------------------------------------------------------------------------- screen (pure)
def period_of(tax_period_end: str) -> tuple:
    end = dt.date.fromisoformat(tax_period_end)
    try:
        start = end.replace(year=end.year - 1) + dt.timedelta(days=1)
    except ValueError:  # 29 Feb
        start = end.replace(year=end.year - 1, day=28) + dt.timedelta(days=1)
    return start, end


def rev_status(recs: Sequence[Mapping], start, end) -> tuple[str, Mapping | None]:
    if not recs:
        return "never_revoked", None
    prior = [r for r in recs if r["rev"] and r["rev"] <= end]
    if not prior:
        return "rev_after", recs[0]
    r = prior[-1]
    rv, ri = r["rev"], r["reinst"]
    if ri and (ri <= rv or ri <= start):
        return "rev_reinstated_before", r
    if rv < start:
        return ("rev_before_reinstated_in", r) if ri and ri <= end else ("rev_before_not_reinstated", r)
    return "rev_during", r


def token_overlap(a: str, b: str) -> float:
    x, y = set(norm_name(a).split()), set(norm_name(b).split())
    return len(x & y) / min(len(x), len(y)) if x and y else 0.0


def labels_of(line: Mapping, irc: str, bmf: Mapping | None, p78: Mapping | None, alt_eins: frozenset) -> tuple:
    up, ircu = line["name"].upper(), (irc or "").upper()
    lab = []
    if GOV_IRC.search(ircu) or GOV_NAME.search(up):
        lab.append("government")
    if (bmf and bmf["foundation"] == "10") or CHURCH_IRC.search(ircu) or CHURCH_NAME.search(up):
        lab.append("church_or_religious")
    if line["where"].startswith("F:") or (p78 and p78["country"] not in ("", "United States")):
        lab.append("foreign")
    if bmf and (bmf["affiliation"] == "9" or (bmf["group"] not in ("", "0000") and bmf["affiliation"] != "6"
                                              and bmf["affiliation"] != "8")):
        lab.append("group_subordinate")
    if not bmf and not p78 and "government" not in lab and PUBLIC_UNIV.search(up):
        lab.append("possible_public_university")
    if not bmf and not p78 and LLC.search(up):
        lab.append("llc_possible_disregarded_entity")
    if line["ein"] and alt_eins and line["ein"] not in alt_eins and len(alt_eins) == 1:
        lab.append("possible_ein_misreport")
    ref = (p78 or {}).get("name") or (bmf or {}).get("name") or ""
    if ref and token_overlap(line["name"], ref) < 0.34:
        lab.append("name_differs")
    return tuple(lab)


def screen(line: Mapping, irc: str, sy: Mapping, bmf: Mapping, p78: Mapping, p78_names: Mapping, revs: Mapping) -> dict:
    e = "" if line["ein"] in PLACEHOLDER else line["ein"]
    start, end = sy["start"], sy["end"]
    b, p = bmf.get(e) if e else None, p78.get(e) if e else None
    rs, rr = rev_status(revs.get(e, ()), start, end) if e else ("blank_or_placeholder_ein", None)
    alt = p78_names.get(norm_name(line["name"]), frozenset()) if (e and not p) else frozenset()
    codes = (p or {}).get("codes", "")
    flags = []
    if rs in REV_HITS:
        flags.append("revoked_in_or_before_grant_year")
    if not e:
        flags.append("blank_ein")
    elif not p and not b:
        flags.append("absent_pub78_and_bmf")
    elif not p:
        flags.append("absent_pub78_in_bmf")
    elif not b:
        flags.append("in_pub78_absent_bmf")
    if b and (b["subsection"] not in ("03", "") or b["deductibility"] == "2"):
        flags.append("bmf_not_501c3_or_not_deductible")
    if any(c in codes.split(",") for c in ER_CODES):
        flags.append("pf_or_sonfi_recipient")
    line = {**line, "ein": e}
    return {"ein": e, "name": line["name"], "where": line["where"], "irc": irc, "amount": line["amount"],
            "d2d": line["d2d"], "rev_status": rs, "rev_date": rr["rev"].isoformat() if rr and rr["rev"] else "",
            "rev_posted": rr["posted"].isoformat() if rr and rr["posted"] else "",
            "reinstated": rr["reinst"].isoformat() if rr and rr["reinst"] else "",
            "rev_posted_by_period_end": (rr["posted"] <= end) if rr and rr["posted"] and rs in REV_HITS else "",
            "rerecognized_now": bool(p or b) if rs in REV_HITS else "",
            "ruling_after_period_end": (b["ruling"][:6] > end.strftime("%Y%m")) if rs in REV_HITS and b and b["ruling"][:6].isdigit() else "",
            "in_pub78": bool(p), "pub78_codes": codes, "in_bmf": bool(b),
            "bmf_subsection": (b or {}).get("subsection", ""), "bmf_deductibility": (b or {}).get("deductibility", ""),
            "bmf_foundation": (b or {}).get("foundation", ""), "bmf_status": (b or {}).get("status", ""),
            "bmf_ruling": (b or {}).get("ruling", ""),
            "ref_name": (p or {}).get("name") or (b or {}).get("name") or (rr or {}).get("name", ""),
            "alt_ein": next(iter(alt)) if len(alt) == 1 and e not in alt else "",
            "flags": tuple(flags), "labels": labels_of(line, irc, b, p, alt)}


# ----------------------------------------------------------------------------- aggregate (pure)
def agg(rows: Sequence[Mapping], pred) -> dict:
    hit = [r for r in rows if pred(r)]
    return {"lines": len(hit), "usd": round(sum(r["amount"] for r in hit)), "eins": len({r["ein"] for r in hit if r["ein"]})}


def label_mix(rows: Sequence[Mapping], pred) -> dict:
    out = {}
    for r in rows:
        if pred(r):
            k = "+".join(r["labels"]) or "none"
            d = out.setdefault(k, [0, 0.0])
            d[0] += 1
            d[1] += r["amount"]
    return {k: {"lines": v[0], "usd": round(v[1])} for k, v in sorted(out.items(), key=lambda kv: -kv[1][1])}


def sum_by(rows, key, n: int) -> dict:
    acc = {}
    for r in rows:
        acc[key(r)] = acc.get(key(r), 0.0) + r["amount"]
    return {k: round(v) for k, v in sorted(acc.items(), key=lambda kv: -kv[1])[:n]}


def unexplained(r: Mapping) -> bool:
    return not set(r["labels"]) & EXPLAINING


EXPLAINING = frozenset({"government", "church_or_religious", "foreign", "group_subordinate", "possible_public_university",
                        "llc_possible_disregarded_entity"})


FLAG_DEFS = (
    ("all_lines", lambda r: True),
    ("revoked_in_or_before_grant_year", lambda r: "revoked_in_or_before_grant_year" in r["flags"]),
    ("rev_before_not_reinstated", lambda r: r["rev_status"] == "rev_before_not_reinstated"),
    ("rev_before_reinstated_in", lambda r: r["rev_status"] == "rev_before_reinstated_in"),
    ("rev_during", lambda r: r["rev_status"] == "rev_during"),
    ("rev_hit_posted_by_period_end", lambda r: r["rev_posted_by_period_end"] is True),
    ("rev_hit_not_in_pub78_or_bmf_now", lambda r: r["rerecognized_now"] is False),
    ("rev_hit_in_pub78_or_bmf_now", lambda r: r["rerecognized_now"] is True),
    ("rev_hit_bmf_ruling_after_period_end", lambda r: r["ruling_after_period_end"] is True),
    ("rev_hit_not_in_lists_now_posted_unexplained",
     lambda r: r["rerecognized_now"] is False and r["rev_posted_by_period_end"] is True and unexplained(r)),
    ("rev_reinstated_before_context", lambda r: r["rev_status"] == "rev_reinstated_before"),
    ("rev_after_context", lambda r: r["rev_status"] == "rev_after"),
    ("absent_pub78_and_bmf", lambda r: "absent_pub78_and_bmf" in r["flags"]),
    ("absent_pub78_and_bmf_unexplained", lambda r: "absent_pub78_and_bmf" in r["flags"] and unexplained(r)),
    ("absent_pub78_and_bmf_unexplained_not_revoked",
     lambda r: "absent_pub78_and_bmf" in r["flags"] and unexplained(r) and r["rev_status"] == "never_revoked"),
    ("absent_pub78_in_bmf", lambda r: "absent_pub78_in_bmf" in r["flags"]),
    ("absent_pub78_in_bmf_unexplained", lambda r: "absent_pub78_in_bmf" in r["flags"] and unexplained(r)),
    ("in_pub78_absent_bmf", lambda r: "in_pub78_absent_bmf" in r["flags"]),
    ("absent_pub78_any", lambda r: r["ein"] and not r["in_pub78"]),
    ("blank_ein", lambda r: "blank_ein" in r["flags"]),
    ("bmf_not_501c3_or_not_deductible", lambda r: "bmf_not_501c3_or_not_deductible" in r["flags"]),
    ("pf_or_sonfi_recipient", lambda r: "pf_or_sonfi_recipient" in r["flags"]),
    ("possible_ein_misreport", lambda r: "possible_ein_misreport" in r["labels"]),
    ("any_screen_hit_unexplained", lambda r: bool(set(r["flags"]) - {"in_pub78_absent_bmf"}) and unexplained(r)),
)


def aggregate_rows(scr: Mapping, panel: Mapping) -> list:
    scopes = [("all_top50_itemising", "all", lambda k: True)] + \
             [(s, "segment", (lambda k, s=s: panel[k[0]]["segment"] == s)) for s in SEGMENTS] + \
             [(panel[e]["name"], "sponsor", (lambda k, e=e: k[0] == e)) for e in sorted({k[0] for k in scr})]
    out = []
    for name, stype, pred in scopes:
        for fy_label, fys in [(str(f), (f,)) for f in FYS] + [("2023-2024", FYS)]:
            keys = [k for k in scr if pred(k) and k[1] in fys]
            if not keys:
                continue
            rows = [r for k in keys for r in scr[k]]
            net = [r for r in rows if not r["d2d"]]
            tot = agg(rows, lambda r: True)
            for flag, fp in FLAG_DEFS:
                if stype == "sponsor" and fy_label != "2023-2024":
                    continue
                a, an = agg(rows, fp), agg(net, fp)
                out.append({"record_type": "aggregate", "scope": name, "scope_type": stype,
                            "segment": panel[keys[0][0]]["segment"] if stype != "all" else "",
                            "fiscal_year": fy_label, "flag": flag, "lines": a["lines"], "amount_usd": a["usd"],
                            "distinct_eins": a["eins"], "share_of_scope_usd": round(a["usd"] / tot["usd"], 8) if tot["usd"] else None,
                            "amount_usd_ex_d2d": an["usd"], "sponsor_years": len(keys), "source": SOURCE})
    return out


ALWAYS = frozenset({"revoked_in_or_before_grant_year", "pf_or_sonfi_recipient", "bmf_not_501c3_or_not_deductible"})


def keep_hit(r: Mapping, hit_min: float) -> bool:
    """Revocation, PF/SONFI and non-501(c)(3) hits are always listed; absence hits only when no exception label
    explains them and the line is at least hit_min dollars (all absence lines are in the aggregates)."""
    fl = set(r["flags"]) - {"in_pub78_absent_bmf", "blank_ein"}
    return bool(r["ein"]) and (bool(fl & ALWAYS) or (bool(fl) and unexplained(r) and r["amount"] >= hit_min))


def hit_rows(scr: Mapping, panel: Mapping, sy: Mapping, hit_min: float) -> list:
    out = []
    for k, rows in scr.items():
        for r in rows:
            fl = [f for f in r["flags"] if f != "in_pub78_absent_bmf"]
            if not keep_hit(r, hit_min):
                continue
            out.append({"record_type": "hit", "scope": panel[k[0]]["name"], "scope_type": "sponsor",
                        "segment": panel[k[0]]["segment"], "fiscal_year": str(k[1]), "flag": ";".join(fl),
                        "sponsor_ein": k[0], "tax_period_end": sy[k]["end"].isoformat(),
                        "recipient_ein": r["ein"], "recipient_name": r["name"], "recipient_state": r["where"],
                        "sched_i_irc_section": r["irc"], "amount_usd": round(r["amount"]),
                        "exception_labels": ";".join(r["labels"]), "rev_status": r["rev_status"],
                        "revocation_date": r["rev_date"], "revocation_posted": r["rev_posted"],
                        "reinstatement_date": r["reinstated"], "rev_posted_by_period_end": r["rev_posted_by_period_end"],
                        "rev_hit_in_pub78_or_bmf_now": r["rerecognized_now"], "bmf_ruling": r["bmf_ruling"],
                        "bmf_ruling_after_period_end": r["ruling_after_period_end"],
                        "in_pub78": int(r["in_pub78"]), "pub78_codes": r["pub78_codes"], "in_bmf": int(r["in_bmf"]),
                        "bmf_subsection": r["bmf_subsection"], "bmf_deductibility": r["bmf_deductibility"],
                        "bmf_foundation": r["bmf_foundation"], "bmf_status": r["bmf_status"],
                        "irs_ref_name": r["ref_name"], "pub78_alt_ein_same_name": r["alt_ein"],
                        "d2d_line": int(r["d2d"]), "source": SOURCE})
    return sorted(out, key=lambda r: (r["flag"].split(";")[0] != "revoked_in_or_before_grant_year", -r["amount_usd"]))


FIELDS = ("record_type", "scope", "scope_type", "segment", "fiscal_year", "flag", "lines", "amount_usd",
          "distinct_eins", "share_of_scope_usd", "amount_usd_ex_d2d", "sponsor_years", "sponsor_ein", "tax_period_end",
          "recipient_ein", "recipient_name", "recipient_state", "sched_i_irc_section", "exception_labels", "rev_status",
          "revocation_date", "revocation_posted", "reinstatement_date", "rev_posted_by_period_end",
          "rev_hit_in_pub78_or_bmf_now", "bmf_ruling", "bmf_ruling_after_period_end", "in_pub78",
          "pub78_codes", "in_bmf", "bmf_subsection", "bmf_deductibility", "bmf_foundation", "bmf_status",
          "irs_ref_name", "pub78_alt_ein_same_name", "d2d_line", "source")


def top_by_recipient(scr: Mapping, panel: Mapping, pred, n: int) -> list:
    by = {}
    for k, rows in scr.items():
        for r in rows:
            if r["ein"] and pred(r):
                d = by.setdefault(r["ein"], {"ein": r["ein"], "name": r["name"], "usd": 0.0, "lines": 0, "sponsors": set(),
                                             "segments": set(), "rev_status": set(), "labels": set(),
                                             "ref_name": r["ref_name"], "rev": r["rev_date"], "reinst": r["reinstated"],
                                             "posted": r["rev_posted"], "codes": r["pub78_codes"],
                                             "bmf": f"{r['bmf_subsection']}/{r['bmf_deductibility']}/{r['bmf_status']}",
                                             "alt_ein": r["alt_ein"], "irc": r["irc"],
                                             "now": r["rerecognized_now"], "ruling": r["bmf_ruling"]})
                d["usd"] += r["amount"]
                d["lines"] += 1
                d["sponsors"].add(panel[k[0]]["name"][:28])
                d["segments"].add(panel[k[0]]["segment"])
                d["rev_status"].add(r["rev_status"])
                d["labels"].update(r["labels"])
    top = sorted(by.values(), key=lambda d: -d["usd"])[:n]
    return [{**d, "usd": round(d["usd"]), **{s: sorted(d[s]) for s in ("sponsors", "segments", "rev_status", "labels")}}
            for d in top]


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--pub78", required=True)
    ap.add_argument("--revocation", required=True)
    ap.add_argument("--hit-min", type=float, default=100000.0, help="min line $ for listing unexplained absence hits")
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    item = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen and itemized(chosen[(e, fy)])}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: v for k, v in loaded.items() if v["status"] == "ok"}
    sy = {k: dict(zip(("start", "end"), period_of(item[k]["tax_period_end"]))) for k in good}

    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    names = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in names.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    irc = {k: tuple(l[3] for l in v["lines"]) for k, v in good.items()}
    eins = frozenset(r["ein"] for rs in ann.values() for r in rs if r["ein"])

    bmf = load_bmf_ext(a.bmf_dir, eins)
    revs = load_revocations(a.revocation, eins)
    p78_e, _ = load_pub78(a.pub78, eins, frozenset())
    absent_names = frozenset(norm_name(r["name"]) for rs in ann.values() for r in rs
                             if r["ein"] and r["ein"] not in p78_e and r["name"])
    _, p78_n = load_pub78(a.pub78, frozenset(), absent_names)

    scr = {k: tuple(screen(r, irc[k][i], sy[k], bmf, p78_e, p78_n, revs) for i, r in enumerate(ann[k])) for k in ann}
    rows = aggregate_rows(scr, panel) + hit_rows(scr, panel, sy, a.hit_min)
    write_csv(OUT, rows, FIELDS)

    pick = lambda scope, flag, fy="2023-2024": next(  # noqa: E731
        ({x: r[x] for x in ("lines", "amount_usd", "distinct_eins", "share_of_scope_usd", "amount_usd_ex_d2d")}
         for r in rows if r["record_type"] == "aggregate" and r["scope"] == scope and r["flag"] == flag
         and r["fiscal_year"] == fy), None)
    allrows = [r for rs in scr.values() for r in rs]
    hits = [r for r in rows if r["record_type"] == "hit"]
    summary = {
        "sponsor_years_itemising": len(item), "sponsor_years_loaded": len(good),
        "tax_period_ends": sorted({v["end"].isoformat() for v in sy.values()})[:1] + sorted({v["end"].isoformat() for v in sy.values()})[-1:],
        "lines": len(allrows), "distinct_eins": len(eins), "eins_in_bmf": len(bmf), "eins_in_pub78": len(p78_e),
        "eins_with_any_revocation_record": len(revs),
        "pooled": {f: pick("all_top50_itemising", f) for f, _ in FLAG_DEFS},
        "by_fy": {fy: {f: pick("all_top50_itemising", f, fy) for f in ("all_lines", "revoked_in_or_before_grant_year",
                                                                       "absent_pub78_and_bmf", "absent_pub78_any")}
                  for fy in ("2023", "2024")},
        "by_segment": {s: {f: pick(s, f) for f in ("all_lines", "revoked_in_or_before_grant_year",
                                                   "rev_hit_not_in_pub78_or_bmf_now", "rev_hit_not_in_lists_now_posted_unexplained",
                                                   "rev_before_not_reinstated", "rev_during", "absent_pub78_and_bmf",
                                                   "absent_pub78_and_bmf_unexplained", "absent_pub78_in_bmf",
                                                   "absent_pub78_in_bmf_unexplained", "blank_ein",
                                                   "pf_or_sonfi_recipient", "any_screen_hit_unexplained")}
                       for s in SEGMENTS},
        "labels_rev_hits": label_mix(allrows, lambda r: r["rev_status"] in REV_HITS),
        "labels_absent_both": label_mix(allrows, lambda r: "absent_pub78_and_bmf" in r["flags"]),
        "labels_absent_pub78_in_bmf": label_mix(allrows, lambda r: "absent_pub78_in_bmf" in r["flags"]),
        "absent_pub78_in_bmf_by_bmf_sub_ded_found": sum_by(
            (r for r in allrows if "absent_pub78_in_bmf" in r["flags"]),
            lambda r: f"{r['bmf_subsection']}/{r['bmf_deductibility']}/{r['bmf_foundation']}", 15),
        "pf_sonfi_codes": label_mix(allrows, lambda r: "pf_or_sonfi_recipient" in r["flags"]),
        "top_rev_hits": top_by_recipient(scr, panel, lambda r: r["rev_status"] in REV_HITS, 25),
        "top_rev_not_in_lists_now": top_by_recipient(scr, panel, lambda r: r["rerecognized_now"] is False, 20),
        "top_rev_ruling_after": top_by_recipient(scr, panel, lambda r: r["ruling_after_period_end"] is True, 10),
        "top_absent_both": top_by_recipient(scr, panel, lambda r: "absent_pub78_and_bmf" in r["flags"], 25),
        "top_absent_both_unexplained": top_by_recipient(
            scr, panel, lambda r: "absent_pub78_and_bmf" in r["flags"] and unexplained(r) and not r["d2d"], 20),
        "top_absent_pub78_in_bmf_unexplained": top_by_recipient(
            scr, panel, lambda r: "absent_pub78_in_bmf" in r["flags"] and unexplained(r), 12),
        "top_pf_sonfi": top_by_recipient(scr, panel, lambda r: "pf_or_sonfi_recipient" in r["flags"], 10),
        "top_not_c3": top_by_recipient(scr, panel, lambda r: "bmf_not_501c3_or_not_deductible" in r["flags"], 10),
        "hit_rows_written": len(hits),
        "sponsor_rev_hits": sorted(({"sponsor": r["scope"][:40], "segment": r["segment"], "lines": r["lines"],
                                     "usd": r["amount_usd"], "share": r["share_of_scope_usd"]}
                                    for r in rows if r["record_type"] == "aggregate" and r["scope_type"] == "sponsor"
                                    and r["flag"] == "revoked_in_or_before_grant_year"), key=lambda d: -d["usd"])[:12],
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
