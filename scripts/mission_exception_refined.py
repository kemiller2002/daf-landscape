#!/usr/bin/env python3
"""Exception-load proxy refinements P-G05-03 (fiscal sponsors) and P-G05-01 (time-correct recent rulings).

Imports scripts/mission_exception_load.py unchanged (line screen, flags, tallies, shares, scope rows) and replaces two
of its five categories:

  fiscal_sponsor_name  (P-G05-03) was a 19-name regex (the Q-B15 host list). Now an EIN-keyed host list:
                       - the 19 Q-B15 hosts, keyed by the EINs whose current EO BMF name matches the old regex, plus,
                         for hosts not in the BMF, the modal EIN sponsors reported for that name on Schedule I;
                       - every host on the Fiscal Sponsor Directory "All Fiscal Sponsors (alpha ordered)" page
                         (fiscalsponsordirectory.org), keyed to an EIN through the 2026-11 EO BMF by name + state
                         (exact, then a same-city near match), else to the single EIN sponsors reported on
                         Schedule I lines under the same name (same state).
                       A Schedule I line is flagged when its EIN is on the list; lines with a blank EIN fall back to
                       the old name regex or an exact directory-name match; the generic markers ("fiscal sponsor",
                       "a project of", "sponsored project") are kept. Directory hosts that are community foundations or
                       United Ways (BMF NTEE T31/T70, or the name says so) are listed but not counted in the headline
                       flag (`fs_grantmaker_host_*` reports them); the 19 Q-B15 hosts are always counted.
  recent_ruling_24m    (P-G05-01) was the 2026-11 BMF RULING month >= grant-year start - 24 months. For the lines that
                       flag selected, the ruling month is now read from the archived monthly IRS EO BMF (NCCS mirror
                       of the unmodified IRS file, raw/bmf/YYYY-MM-BMF.csv, 2023-06 to 2026-07; NCCS legacy 2022-01
                       and 2022-08 for prior existence) as of the first snapshot after the grant-year end, and each
                       line is classed:
                         dropped_reset_after_grant  ruling at grant time was older than the cutoff; a later
                                                    reinstatement / re-determination moved it;
                         after_period_new_org       not recognised by grant-year end, no sign of earlier existence;
                         after_period_church        the same for a line labelled church/religious;
                         after_period_other         ruling after grant-year end, with earlier existence;
                         tc_new_org / tc_new_subordinate / tc_newly_listed_church / tc_reinstatement /
                         tc_redetermination
                                                    ruling inside [start - 24 months, end] at grant time, split by
                                                    the evidence of earlier existence: an auto-revocation dated
                                                    before the ruling (reinstatement), an older ruling month in an
                                                    earlier BMF snapshot, or an e-filed return (IRS e-file index,
                                                    2021+) for a tax period >= 36 months before the ruling
                                                    (re-determination); otherwise a church newly listed (line
                                                    labelled church/religious: churches need no application, so a
                                                    first ruling month does not date them), else new (group
                                                    subordinate when the BMF GROUP code is non-zero).
                       The refined `recent_ruling_24m` = tc_* plus after_period_new_org (broad union); the refined
                       core union uses tc_* only (as the original core used in-window rulings only). `any_core_new_only`
                       uses tc_new_org + tc_new_subordinate only.

Rows and columns are those of exception-load-proxy-2026-11-19.csv with the refined definitions, plus `base_*`
columns from the unchanged script and the extra sub-category columns listed in EXTRA_FIELDS.

Pure functions over immutable inputs; I/O only in the `load_*` functions and `main`. Stdlib only.

Usage:
  # 1. recipient EIN list (for filtering the archives)
  python3 scripts/mission_exception_refined.py . --np-cache NP --lines-cache LINES --bmf-dir BMF --pub78 P78 \
      --write-eins EINS.txt
  # 2. filter each archived BMF month while streaming (monthly raw files; add --legacy for the 2022 NCCS files)
  curl -sS https://nccsdata.s3.us-east-1.amazonaws.com/raw/bmf/2024-06-BMF.csv | \
      python3 scripts/mission_exception_refined.py . --filter-archive EINS.txt > ARCH/2024-06.csv
  # 3. run
  python3 scripts/mission_exception_refined.py . --np-cache NP --lines-cache LINES --bmf-dir BMF --pub78 P78 \
      --revocation data-download-revocation.txt --efile-index-dir IRS --bmf-archive-dir ARCH \
      --fsd-html all-fiscal-sponsors-alpha-ordered.html [--out PATH] [--fs-list-out PATH]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import glob
import html
import json
import os
import re
import statistics
import sys
from functools import reduce
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_exception_load as mel  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_compliance import (BMF_FILES, load_bmf_ext, load_pub78, load_revocations,  # noqa: E402
                                          period_of, screen)
from mission_recipient_sectors import WHITELIST, annotate, load_lines  # noqa: E402

OUT = os.path.join(DATA, "exception-proxy-refined-2026-11-19.csv")
FS_LIST_OUT = os.path.join(DATA, "fiscal-sponsor-ein-list-2026-11-19.csv")
SOURCE = (mel.SOURCE + "; fiscal-sponsor hosts from fiscalsponsordirectory.org (all-fiscal-sponsors-alpha-ordered, "
          "fetched 2026-11-19) keyed to EINs via the EO BMF; ruling months as of grant time from archived monthly IRS "
          "EO BMF files (NCCS mirror nccsdata.s3.us-east-1.amazonaws.com/raw/bmf/, 2023-06..2026-07; legacy/bmf 2022-01, "
          "2022-08); IRS auto-revocation list; IRS e-file index 2021-2026")

# Community foundations (NTEE T31) and federated funds / United Ways (T70) also hold DAFs and pooled funds, so a grant
# to one is not plausibly a fiscal-sponsor case; never applied to the 19 Q-B15 hosts.
COMMUNITY_FUND_NTEE = re.compile(r"^T(31|70)")
COMMUNITY_FUND_NAME = re.compile(r"\bCOMMUNITY FOUNDATION\b|\bUNITED WAY\b")
GENERIC = frozenset({"FOUNDATION", "FUND", "CENTER", "CENTRE", "INSTITUTE", "ASSOCIATION", "SOCIETY", "COMMUNITY",
                     "COUNCIL", "ALLIANCE", "TRUST", "NETWORK", "PROJECT", "ORGANIZATION", "INTERNATIONAL", "GLOBAL"})
PRIOR_EFILE_MONTHS = 36                              # e-filed tax period this far before the ruling = pre-existing
ARCHIVE_KEEP = ("EIN", "NAME", "CITY", "STATE", "GROUP", "SUBSECTION", "AFFILIATION", "RULING", "DEDUCTIBILITY",
                "FOUNDATION", "STATUS", "NTEE_CD")
STOP = frozenset({"INC", "INCORPORATED", "THE", "CORP", "CORPORATION", "CO", "LTD", "NFP", "N", "F", "P", "LLC", "A",
                  "OF", "AND", "FOR", "S"})
STATES = {"OHIO": "OH", "CALIFORNIA": "CA", "NEW YORK": "NY", "PUERTO RICO": "PR"}

RR_CLASSES = ("tc_new_org", "tc_new_subordinate", "tc_newly_listed_church", "tc_reinstatement", "tc_redetermination",
              "dropped_reset_after_grant", "after_period_new_org", "after_period_church", "after_period_other")
EXTRA_SI = (("fs_q19_ein", "fs_fsd_ein", "fs_fsd_only_ein", "fs_name_fallback", "fs_marker", "fs_grantmaker_host",
             "fs_all_incl_grantmakers", "fs_d2d", "rr_base", "rr_tc", "rr_asof_lag_ge3m", "rr_efile_proxy_new",
             "rr_efile_proxy_new_and_tc", "any_core_new_only", "any_core_fs_all", "any_core_base_recent")
            + tuple(f"rr_{c}" for c in RR_CLASSES))


# ----------------------------------------------------------------------------- names (pure)
def name_key(s: str) -> str:
    s = re.sub(r"\([^)]*\)", " ", (s or "").replace("’", "").replace("'", ""))
    return " ".join(w for w in mel.upname(s).split() if w not in STOP)


def state_of(loc: str) -> str:
    u = re.sub(r"\b([A-Z]) ([A-Z])$", r"\1\2", mel.upname(loc.split("–")[-1]))
    if re.search(r"(^|\b)D C$|\bDC$", u):
        return "DC"
    m = re.search(r"\b([A-Z]{2})( \d{5})?$", u)
    return m.group(1) if m else next((v for k, v in STATES.items() if u.endswith(k)), "")


def city_of(loc: str) -> str:
    loc = loc.split("–")[-1]
    return mel.upname(loc.split(",")[0]) if "," in loc else mel.upname(re.sub(r"\s+\S+$", "", loc))


# ----------------------------------------------------------------------------- fiscal-sponsor directory (pure)
def fsd_entries(page: str) -> tuple:
    """(url, name, location) per host on the Fiscal Sponsor Directory alpha-ordered page."""
    body = re.search(r"<article.*?</article>", page, re.S)
    segs = re.split(r"<br\s*/?>|</p>|<p>|<h3>", body.group(0) if body else "")
    hits = (re.search(r'<a href="(https://fiscalsponsordirectory\.org/[^"]+)"[^>]*>(.*?)</a>(.*)', s, re.S) for s in segs)
    clean = lambda x: html.unescape(re.sub(r"<[^>]+>", "", x)).strip()  # noqa: E731
    rows = ((m.group(1), clean(m.group(2)), re.sub(r"^[.\s]*[–-]\s*", "", clean(m.group(3))).strip()) for m in hits if m)
    return tuple(r for r in rows if r[1])


def similar(a: str, b: str) -> bool:
    """Near match for directory vs BMF names in the same city: same token set, one token set contains the other
    (>= 2 non-generic tokens in the smaller set; plural 'S' ignored), or the BMF name is a 40-character-truncated
    prefix of the directory name (spaces ignored)."""
    x, y = {w.rstrip("S") for w in a.split()}, {w.rstrip("S") for w in b.split()}
    ca, cb = a.replace(" ", ""), b.replace(" ", "")
    small = min((x, y), key=len) - GENERIC
    return bool(x and y) and (x == y or ca == cb
                              or (len(small) >= 2 and (x <= y or y <= x))
                              or (len(cb) >= 25 and ca.startswith(cb)))


def match_entry(entry: Sequence, exact: Mapping, by_city: Mapping) -> dict:
    url, name, loc = entry
    k, st, city = name_key(re.split(r"\bdba\b", name, flags=re.I)[0]), state_of(loc), city_of(loc)
    cands = exact.get(k, ())
    s1 = tuple(c for c in cands if c["STATE"] == st)
    s2 = tuple(c for c in s1 if mel.upname(c["CITY"]) == city)
    near = tuple(c for c in by_city.get((st, city), ()) if similar(k, name_key(c["NAME"])))
    how, hit = (("name_state", s1[0]) if len(s1) == 1 else
                ("name_state_city", s2[0]) if len(s2) == 1 else
                ("near_name_same_city", near[0]) if len({c["EIN"] for c in near}) == 1 else
                ("ambiguous", None) if s1 or len(near) > 1 else
                ("unmatched", None))
    h = hit or {}
    return {"source": "fiscalsponsordirectory", "host_name": name, "host_location": loc, "host_url": url,
            "host_state": st, "match_method": how, "ein": h.get("EIN", ""), "bmf_name": h.get("NAME", ""),
            "bmf_city": h.get("CITY", ""), "bmf_state": h.get("STATE", ""), "bmf_subsection": h.get("SUBSECTION", ""),
            "bmf_ntee": h.get("NTEE_CD", ""), "bmf_ruling": h.get("RULING", "")}


def key_from_lines(row: Mapping, line_eins: Mapping, bmf: Mapping) -> dict:
    """Second pass for a directory host left unmatched or ambiguous in the BMF: take the EIN that sponsors themselves
    reported on Schedule I lines whose recipient name has the same key, if exactly one EIN is reported and (when that
    EIN is in the BMF) its BMF state is the host's state."""
    if row["ein"]:
        return row
    eins = line_eins.get(name_key(re.split(r"\bdba\b", row["host_name"], flags=re.I)[0]), frozenset())
    e = next(iter(eins)) if len(eins) == 1 else ""
    b = bmf.get(e, {})
    ok = bool(e) and (not b or b.get("state", "") == row["host_state"])
    return {**row, "match_method": "sched_i_reported_ein", "ein": e, "bmf_name": b.get("name", ""),
            "bmf_state": b.get("state", ""), "bmf_subsection": b.get("subsection", ""), "bmf_ruling": b.get("ruling", "")} if ok else row


def q19_rows(bmf: Mapping) -> tuple:
    """The 19 Q-B15 hosts keyed by EIN: recipient EINs whose current BMF name matches the original regex."""
    return tuple({"source": "q_b15_19_list", "host_name": b["name"], "host_location": "", "host_url": "",
                  "host_state": b.get("state", ""), "match_method": "bmf_name_matches_q_b15_regex", "ein": e,
                  "bmf_name": b["name"], "bmf_city": "", "bmf_state": b.get("state", ""),
                  "bmf_subsection": b.get("subsection", ""), "bmf_ntee": b.get("ntee", ""), "bmf_ruling": b.get("ruling", "")}
                 for e, b in sorted(bmf.items()) if mel.FISCAL_SPONSORS.search(mel.upname(b["name"])))


def q19_reported(lines: Iterable[tuple], known: frozenset) -> tuple:
    """Q-B15 hosts absent from the current BMF (e.g. dissolved): the modal EIN sponsors reported on Schedule I lines
    whose recipient name matches the Q-B15 regex, per matched host string, when it covers >= half of those lines."""
    hits = _group_by_fast(((m.group(0).strip(), e) for e, nm in lines if e and (m := mel.FISCAL_SPONSORS.search(nm))),
                          lambda t: re.sub(r"^THE |\b(INC|CENTER|FOUNDATION)$", "", t[0]).strip())
    modal = {h: max(((e, sum(1 for _, x in v if x == e)) for e in {x for _, x in v}), key=lambda z: z[1]) + (len(v),)
             for h, v in hits.items()}
    return tuple({"source": "q_b15_19_list", "host_name": h, "host_location": "", "host_url": "", "host_state": "",
                  "match_method": "sched_i_reported_modal_ein", "ein": e, "bmf_name": "", "bmf_city": "", "bmf_state": "",
                  "bmf_subsection": "", "bmf_ntee": "", "bmf_ruling": ""}
                 for h, (e, n, tot) in sorted(modal.items()) if e not in known and 2 * n >= tot)


def fs_index(rows: Sequence[Mapping]) -> dict:
    """EIN -> {q19, fsd, grantmaker} for every keyed host (`grantmaker` = community foundation / United Way host
    not on the Q-B15 list)."""
    keyed = _group_by_fast((r for r in rows if r["ein"]), lambda r: r["ein"])
    q19 = lambda v: any(r["source"] == "q_b15_19_list" for r in v)  # noqa: E731
    return {e: {"q19": q19(v), "fsd": any(r["source"] == "fiscalsponsordirectory" for r in v),
                "grantmaker": (not q19(v)) and any(community_fund(r) for r in v)}
            for e, v in keyed.items()}


def community_fund(r: Mapping) -> bool:
    return bool(COMMUNITY_FUND_NTEE.match(r["bmf_ntee"] or "") or COMMUNITY_FUND_NAME.search(mel.upname(r["bmf_name"])))


# ----------------------------------------------------------------------------- BMF archives (pure)
def ym(s: str) -> str:
    d = re.sub(r"\D", "", s or "")[:6]
    return d if len(d) == 6 and d > "000000" else ""


def months_back(yyyymm: str, n: int) -> str:
    m = int(yyyymm[:4]) * 12 + int(yyyymm[4:6]) - 1 - n
    return f"{m // 12:04d}{m % 12 + 1:02d}"


def complete_months(sizes: Mapping) -> tuple:
    """Monthly snapshots whose filtered row count is >= 90% of the median (drops truncated captures)."""
    med = statistics.median(sizes.values()) if sizes else 0
    return tuple(sorted(m for m, n in sizes.items() if n >= 0.9 * med))


def asof_month(end: dt.date, months: Sequence[str]) -> str:
    """First monthly snapshot published after the grant-year end month (a file dated the 1st of M reflects M-1)."""
    em = end.strftime("%Y-%m")
    return next((m for m in months if m > em), months[-1])


def classify(ein: str, now_ruling: str, start: dt.date, end: dt.date, arch: Mapping, months: Sequence[str],
             legacy: Sequence[str], revs: Mapping, efile_first: Mapping, group: str, church: bool) -> dict:
    """Time-correct class of one recent-ruling line (see module docstring)."""
    cutoff, endm = mel.ruling_cutoff(start), end.strftime("%Y%m")
    snap = asof_month(end, months)
    at = ym(arch[snap].get(ein, ""))
    seen = tuple(r for r in (ym(arch[m].get(ein, "")) for m in tuple(legacy) + tuple(months)) if r)
    later = tuple(r for r in (ym(arch[m].get(ein, "")) for m in months if m > snap) if r)
    first_seen = next((m for m in months if arch[m].get(ein)), "")
    ref = at or (later[0] if later else now_ruling)
    rev_before = any(r["rev"] and r["rev"].strftime("%Y%m") < ref for r in revs.get(ein, ()))
    older = any(r < ref for r in seen)
    ef = efile_first.get(ein, "")
    old_filer = bool(ef) and ef <= months_back(ref, PRIOR_EFILE_MONTHS)
    kind = ("reinstatement" if rev_before else "redetermination" if older or old_filer else
            "church" if church else "new_subordinate" if group not in ("", "0", "0000") else "new_org")
    in_window = cutoff <= ref <= endm
    cls = ("dropped_reset_after_grant" if ref < cutoff else
           ("tc_newly_listed_church" if kind == "church" else f"tc_{kind}") if in_window else
           ("after_period_new_org" if kind in ("new_org", "new_subordinate") else
            "after_period_church" if kind == "church" else "after_period_other"))
    lag = (int(snap[:4]) * 12 + int(snap[5:7])) - (end.year * 12 + end.month)
    return {"class": cls, "asof_snapshot": snap, "ruling_asof": at, "ruling_ref": ref, "first_seen": first_seen,
            "efile_first": ef, "efile_new": (not ef) or ef >= cutoff, "lag_ge3m": lag >= 3}


# ----------------------------------------------------------------------------- refined flags (pure)
def refined_flags(r: Mapping, base: frozenset, fsx: Mapping, rr: Mapping | None, fsd_names: frozenset) -> tuple:
    """(refined category set for mel.tally, extra sub-category set)."""
    nm = mel.upname(r["name"])
    host = fsx.get(r["ein"]) if r["ein"] else None
    fallback = (not r["ein"]) and bool(mel.FISCAL_SPONSORS.search(nm) or name_key(r["name"]) in fsd_names)
    marker = bool(mel.FISCAL_MARKER.search(nm))
    gm = bool(host and host["grantmaker"])
    fs_all = bool(host) or fallback or marker
    fs = (bool(host) and not gm) or fallback or marker
    cls = rr["class"] if rr else ""
    tc = cls.startswith("tc_")
    new_tc = cls in ("tc_new_org", "tc_new_subordinate")
    recent = tc or cls == "after_period_new_org"
    other = base - {"fiscal_sponsor_name", "fiscal_sponsor_listed", "recent_ruling_24m", "recent_ruling_after_period_end",
                    "any_si", "any_core_si"}
    has = lambda c: c in base  # noqa: E731
    core_rest = has("foreign_si") or has("not_c3_or_not_pub78_unexplained") or has("pf_or_er")
    union = has("foreign_si") or has("not_c3_or_not_pub78") or has("pf_or_er") or recent or fs
    core = core_rest or tc or fs
    ref = frozenset(other | {k for k, v in {"fiscal_sponsor_name": fs, "fiscal_sponsor_listed": bool(host and not gm) or fallback,
                                             "recent_ruling_24m": recent,
                                             "recent_ruling_after_period_end": cls.startswith("after_period"),
                                             "any_si": union, "any_core_si": core}.items() if v})
    extra = {"fs_q19_ein": bool(host and host["q19"]), "fs_fsd_ein": bool(host and host["fsd"]),
             "fs_fsd_only_ein": bool(host and host["fsd"] and not host["q19"]), "fs_name_fallback": fallback,
             "fs_marker": marker, "fs_grantmaker_host": gm, "fs_all_incl_grantmakers": fs_all,
             "fs_d2d": fs and bool(r["d2d"]), "rr_base": has("recent_ruling_24m"), "rr_tc": tc,
             "rr_asof_lag_ge3m": bool(rr and tc and rr["lag_ge3m"]),
             "rr_efile_proxy_new": bool(rr and rr["efile_new"] and has("recent_ruling_24m")
                                        and not has("recent_ruling_after_period_end")),
             "rr_efile_proxy_new_and_tc": bool(rr and rr["efile_new"] and tc),
             "any_core_new_only": core_rest or new_tc or fs,
             "any_core_fs_all": core_rest or tc or fs_all,
             "any_core_base_recent": core_rest or (has("recent_ruling_24m") and not has("recent_ruling_after_period_end")) or fs,
             **{f"rr_{c}": cls == c for c in RR_CLASSES}}
    return ref, frozenset(k for k, v in extra.items() if v)


def extra_tally(lines: Iterable[tuple]) -> dict:
    ls = tuple(lines)
    return {**{f"{c}_lines": sum(1 for _, x in ls if c in x) for c in EXTRA_SI},
            **{f"{c}_usd": sum(a for a, x in ls if c in x) for c in EXTRA_SI}}


def add_extra(a: Mapping, b: Mapping) -> dict:
    return {k: (a.get(k) or 0) + (b.get(k) or 0) for k in set(a) | set(b)}


# ----------------------------------------------------------------------------- scope membership (pure)
def scope_keys(row: Mapping, item: Sequence, meta: Mapping) -> tuple:
    rt, sc = row["row_type"], row["scope"]
    st = lambda k: mel.sponsor_type(k[0], meta[k]["segment"])  # noqa: E731
    pred = {"sponsor_year": lambda k: k[0] == row["ein"] and str(k[1]) == str(row["fiscal_year"]),
            "sponsor": lambda k: k[0] == row["ein"],
            "sponsor_type": lambda k: st(k) == sc,
            "dafrc_segment": lambda k: meta[k]["segment"] == sc,
            "big4_nationals": lambda k: k[0] in mel.BIG4,
            "all_fy": lambda k: sc.endswith(f"fy{k[1]}"),
            "big4_fy": lambda k: k[0] in mel.BIG4 and sc.endswith(f"fy{k[1]}"),
            "all": {"all_top50_itemising": lambda k: True,
                    "all_ex_university_hospital": lambda k: meta[k]["segment"] != "university_hospital",
                    "all_ex_university_hospital_ex_svcf":
                        lambda k: meta[k]["segment"] != "university_hospital" and k[0] != mel.SVCF}.get(sc)}[rt]
    return tuple(k for k in item if pred(k))


EXTRA_FIELDS = (tuple(f"{c}_{m}" for c in EXTRA_SI for m in ("lines", "usd", "count_share", "usd_share"))
                + ("any_core_new_only_gap_pp",)
                + tuple(f"base_{c}_{m}" for c in ("fiscal_sponsor_name", "recent_ruling_24m", "any", "any_core")
                        for m in ("lines", "usd", "count_share", "usd_share")) + ("base_any_core_gap_pp",))


def extra_cols(row: Mapping, keys: Sequence, extras: Mapping, base_row: Mapping | None) -> dict:
    if row.get("sched_i_status") != "itemised" or not keys:
        return {}
    t = reduce(add_extra, (extras[k] for k in keys), {})
    dn, du = row["denom_lines"], row["denom_usd"]
    plus_f = frozenset({"any_core_new_only", "any_core_fs_all", "any_core_base_recent"})  # unions include Sched F
    f_n, f_u = int(row.get("sched_f_foreign_recipients") or 0), float(row.get("sched_f_foreign_usd") or 0)
    vals = {c: (t[f"{c}_lines"] + (f_n if c in plus_f else 0), t[f"{c}_usd"] + (f_u if c in plus_f else 0.0))
            for c in EXTRA_SI}
    out = {k: v for c, (n, u) in vals.items() for k, v in
           ((f"{c}_lines", n), (f"{c}_usd", round(u)), (f"{c}_count_share", mel.ratio(n, dn)),
            (f"{c}_usd_share", mel.ratio(u, du)))}
    cs, us = out["any_core_new_only_count_share"], out["any_core_new_only_usd_share"]
    b = base_row or {}
    return {**out, "any_core_new_only_gap_pp": round((us - cs) * 100, 3) if cs is not None and us is not None else None,
            **{f"base_{c}_{m}": b.get(f"{c}_{m}") for c in ("fiscal_sponsor_name", "recent_ruling_24m", "any", "any_core")
               for m in ("lines", "usd", "count_share", "usd_share")},
            "base_any_core_gap_pp": b.get("any_core_gap_pp")}


# ----------------------------------------------------------------------------- I/O
def load_bmf_names(bmf_dir: str, keys: frozenset, cities: frozenset, eins: frozenset) -> tuple:
    """(exact name-key index, (state, city) index restricted to the given cities, {ein: record} for `eins`) over the
    current EO BMF."""
    exact, by_city, by_ein = {}, {}, {}
    for f in BMF_FILES:
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="latin-1", newline="") as fh:
            for r in csv.DictReader(fh):
                rec = {k: (r.get(k) or "").strip() for k in ("EIN", "NAME", "CITY", "STATE", "SUBSECTION", "NTEE_CD", "RULING")}
                rec = {**rec, "EIN": ein9(rec["EIN"])}
                k = name_key(rec["NAME"])
                if k in keys:
                    exact.setdefault(k, []).append(rec)
                sc = (rec["STATE"], mel.upname(rec["CITY"]))
                if sc in cities:
                    by_city.setdefault(sc, []).append(rec)
                if rec["EIN"] in eins:
                    by_ein[rec["EIN"]] = rec
    return ({k: tuple(v) for k, v in exact.items()}, {k: tuple(v) for k, v in by_city.items()}, by_ein)


def load_archives(arch_dir: str, eins: frozenset) -> tuple:
    """({month: {ein: ruling}}, {month: filtered rows}, {ein: group code from the latest month}) from filtered files
    named YYYY-MM.csv (monthly) and LYYYY-MM.csv (NCCS legacy)."""
    arch, sizes, groups = {}, {}, {}
    for p in sorted(glob.glob(os.path.join(arch_dir, "*.csv"))):
        m = os.path.basename(p)[:-4]
        with open(p, encoding="utf-8", errors="replace", newline="") as fh:
            rows = tuple(csv.DictReader(fh))
        sizes[m] = len(rows)
        arch[m] = {r["EIN"]: r["RULING"] for r in rows if r["EIN"] in eins}
        if not m.startswith("L"):
            groups = {**groups, **{r["EIN"]: r["GROUP"] for r in rows if r["EIN"] in eins}}
    return arch, sizes, groups


def load_efile_first(index_dir: str, eins: frozenset) -> dict:
    """Earliest TAX_PERIOD (YYYYMM) per EIN across IRS e-file index files index_2021.csv .. index_2026.csv."""
    first = {}
    for y in range(2021, 2027):
        p = os.path.join(index_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            continue
        with open(p, encoding="latin-1", newline="") as fh:
            for r in csv.DictReader(fh):
                e = ein9(r["EIN"])
                tp = ym(r.get("TAX_PERIOD", ""))
                if e in eins and tp and (e not in first or tp < first[e]):
                    first[e] = tp
    return first


def filter_archive(eins_path: str, legacy: bool) -> int:
    """Stream an archived BMF CSV on stdin; write ARCHIVE_KEEP columns for listed EINs to stdout."""
    with open(eins_path) as fh:
        eins = frozenset(l.strip() for l in fh if l.strip())
    pick = ((lambda r: (r["NAME"], r["CITY"], r["STATE"], "", r["SUBSECCD"], "", r["RULEDATE"], "",
                        (r["FNDNCD"] or "").split(".")[0], "", r["NTEEFINAL"])) if legacy else
            (lambda r: tuple((r.get(k) or "").strip() for k in ARCHIVE_KEEP[1:])))
    ein_of = lambda r: (r.get("EIN") or "").strip().split(".")[0].zfill(9)  # noqa: E731
    w = csv.writer(sys.stdout)
    w.writerow(ARCHIVE_KEEP)
    n = 0
    for r in csv.DictReader(sys.stdin):  # streaming I/O edge
        n += 1
        if ein_of(r) in eins:
            w.writerow((ein_of(r),) + pick(r))
    print(json.dumps({"rows_read": n}), file=sys.stderr)
    return 0


def load_screened(a) -> dict:
    """The unchanged mission_exception_load pipeline up to screened lines (mirrors its `main`)."""
    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    present = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen}
    item = {k: x for k, x in present.items() if itemized(x)}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: mel.drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    groups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in groups.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    irc = {k: tuple(l[3] for l in v["lines"]) for k, v in good.items()}
    eins = frozenset(r["ein"] for rs in ann.values() for r in rs if r["ein"])
    bmf = load_bmf_ext(a.bmf_dir, eins)
    p78, _ = load_pub78(a.pub78, eins, frozenset())
    period = {k: dict(zip(("start", "end"), period_of(item[k]["tax_period_end"]))) for k in good}
    screened = {k: tuple(screen(r, irc[k][i], period[k], bmf, p78, {}, {}) for i, r in enumerate(ann[k])) for k in ann}
    return {"panel": panel, "rank": rank, "present": present, "item": item, "good": good, "eins": eins, "bmf": bmf,
            "period": period, "screened": screened}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; accepted for the repo's CLI convention)")
    ap.add_argument("--np-cache")
    ap.add_argument("--lines-cache")
    ap.add_argument("--bmf-dir")
    ap.add_argument("--pub78")
    ap.add_argument("--revocation")
    ap.add_argument("--efile-index-dir")
    ap.add_argument("--bmf-archive-dir")
    ap.add_argument("--fsd-html")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--fs-list-out", default=FS_LIST_OUT)
    ap.add_argument("--write-eins")
    ap.add_argument("--filter-archive", metavar="EINS")
    ap.add_argument("--legacy", action="store_true")
    a = ap.parse_args(argv)
    if a.filter_archive:
        return filter_archive(a.filter_archive, a.legacy)

    d = load_screened(a)
    if a.write_eins:
        with open(a.write_eins, "w") as fh:
            fh.write("\n".join(sorted(d["eins"])) + "\n")
        return 0
    screened, period, item, present, panel, rank = (d[k] for k in ("screened", "period", "item", "present", "panel", "rank"))
    good = d["good"]
    base_flags = {k: tuple(mel.line_flags(r, period[k]["start"], period[k]["end"]) for r in rs) for k, rs in screened.items()}

    # --- P-G05-03: EIN-keyed fiscal-sponsor list
    with open(a.fsd_html, encoding="utf-8", errors="replace") as fh:
        entries = fsd_entries(fh.read())
    keys = frozenset(name_key(re.split(r"\bdba\b", n, flags=re.I)[0]) for _, n, _ in entries)
    cities = frozenset((state_of(l), city_of(l)) for _, _, l in entries)
    q_eins = frozenset(e for e, b in d["bmf"].items() if mel.FISCAL_SPONSORS.search(mel.upname(b["name"])))
    exact, by_city, by_ein = load_bmf_names(a.bmf_dir, keys, cities, q_eins)
    line_eins = {k: frozenset(e for e, _ in v) for k, v in _group_by_fast(
        ((r["ein"], name_key(r["name"])) for rs in screened.values() for r in rs if r["ein"]), lambda t: t[1]).items()}
    fsd_rows = tuple(key_from_lines(match_entry(e, exact, by_city), line_eins, d["bmf"]) for e in entries)
    q19 = tuple({**r, "bmf_ntee": by_ein.get(r["ein"], {}).get("NTEE_CD", ""), "bmf_city": by_ein.get(r["ein"], {}).get("CITY", "")}
                for r in q19_rows({e: d["bmf"][e] for e in q_eins}))
    q19 = q19 + q19_reported(((r["ein"], mel.upname(r["name"])) for rs in screened.values() for r in rs),
                             frozenset(r["ein"] for r in q19))
    fs_rows = q19 + fsd_rows
    fsx = fs_index(fs_rows)
    fsd_names = frozenset(name_key(n) for _, n, _ in entries)

    # --- P-G05-01: time-correct ruling months for the recent-ruling lines
    rr_eins = frozenset(r["ein"] for k, rs in screened.items() for r, f in zip(rs, base_flags[k])
                        if "recent_ruling_24m" in f)
    arch, sizes, groups = load_archives(a.bmf_archive_dir, rr_eins)
    months = complete_months({m: n for m, n in sizes.items() if not m.startswith("L")})
    legacy = tuple(sorted(m for m in arch if m.startswith("L")))
    revs = load_revocations(a.revocation, rr_eins)
    efile = load_efile_first(a.efile_index_dir, rr_eins)
    rr = {k: tuple(classify(r["ein"], ym(r["bmf_ruling"]), period[k]["start"], period[k]["end"], arch, months, legacy,
                            revs, efile, groups.get(r["ein"], ""), "church_or_religious" in r["labels"])
                   if "recent_ruling_24m" in f else None for r, f in zip(rs, base_flags[k]))
          for k, rs in screened.items()}
    both = {k: tuple(refined_flags(r, f, fsx, x, fsd_names) for r, f, x in zip(rs, base_flags[k], rr[k]))
            for k, rs in screened.items()}

    # --- tallies and rows (mel.build_rows on base and refined flags)
    sf_rows = {(ein9(r["ein"]), int(r["fiscal_year"])): r for r in read_csv(mel.SCHED_F_CSV) if r["row_type"] == "sponsor_year"}
    keys_all = tuple(present)
    sf = {k: mel.sched_f_of(sf_rows.get(k)) for k in keys_all}
    meta = {k: {"name": panel[k[0]]["name"], "segment": panel[k[0]]["segment"], "rank": rank[k[0]],
                "oid": present[k]["oid"], "tpe": present[k]["tax_period_end"],
                "status": "itemised" if k in good else ("attachment_only" if k not in item else "lines_not_loaded"),
                "f_count_basis": sf[k]["f_count_basis"]} for k in keys_all}
    fpart = lambda k: {**{x: sf[k][x] for x in ("f_usd", "f_recipients", "f_other_org_cnt")},  # noqa: E731
                       "f_total_grants": sf[k].get("f_total_grants", 0.0)}
    mk = lambda fl: {k: {**(mel.tally((r["amount"], f, r["d2d"]) for r, f in zip(screened[k], fl(k))) if k in good  # noqa: E731
                            else mel.tally(())), **fpart(k)} for k in keys_all}
    base_t = mk(lambda k: base_flags[k])
    ref_t = mk(lambda k: tuple(x[0] for x in both[k]))
    extras = {k: extra_tally((r["amount"], x[1]) for r, x in zip(screened[k], both[k])) if k in good else extra_tally(())
              for k in keys_all}
    base_rows = {(r["row_type"], r["scope"], r["fiscal_year"]): r for r in mel.build_rows(base_t, meta)}
    item_keys = tuple(k for k in keys_all if meta[k]["status"] == "itemised")
    rows = [{**r, **extra_cols(r, scope_keys(r, item_keys, meta), extras, base_rows.get((r["row_type"], r["scope"], r["fiscal_year"]))),
             "source": SOURCE} for r in mel.build_rows(ref_t, meta)]
    fields = mel.FIELDS[:-1] + EXTRA_FIELDS + ("source",)
    write_csv(a.out, rows, fields)
    fs_fields = ("source", "host_name", "host_location", "host_url", "host_state", "match_method", "ein", "bmf_name",
                 "bmf_city", "bmf_state", "bmf_subsection", "bmf_ntee", "bmf_ruling", "grantmaker_host",
                 "top50_sched_i_lines", "top50_sched_i_usd")
    hits = _group_by_fast(((r["ein"], r["amount"]) for k, rs in screened.items() for r in rs if r["ein"] in fsx),
                          lambda h: h[0])
    write_csv(a.fs_list_out, [{**r, "grantmaker_host": fsx[r["ein"]]["grantmaker"] if r["ein"] else "",
                               "top50_sched_i_lines": len(hits.get(r["ein"], ())) if r["ein"] else "",
                               "top50_sched_i_usd": round(sum(x for _, x in hits.get(r["ein"], ()))) if r["ein"] else ""}
                              for r in fs_rows], fs_fields)

    # --- summary
    flat = tuple((k, r, x, c) for k in screened for r, x, c in zip(screened[k], both[k], rr[k]))
    top = lambda cat, n: sorted(((e, sum(r["amount"] for _, r, _, _ in v), len(v), v[0][1]["name"][:50],  # noqa: E731
                                  (v[0][3] or {}).get("ruling_asof", ""), v[0][1]["bmf_ruling"])
                                 for e, v in _group_by_fast((t for t in flat if cat in t[2][1]),
                                                            lambda t: t[1]["ein"] or "N:" + mel.upname(t[1]["name"])).items()),
                                key=lambda z: -z[1])[:n]
    allrow = next(r for r in rows if r["scope"] == "all_top50_itemising")
    pick = ("denom_lines", "denom_usd") + tuple(f for f in fields if f.endswith(("_count_share", "_usd_share", "_lines", "_usd"))
                                                and (f.startswith(("fiscal", "recent", "any", "base_", "fs_", "rr_"))))
    summary = {
        "fsd_entries": len(entries),
        "fsd_match_methods": {m: sum(1 for r in fsd_rows if r["match_method"] == m) for m in sorted({r["match_method"] for r in fsd_rows})},
        "fsd_keyed_eins": len({r["ein"] for r in fsd_rows if r["ein"]}),
        "q19_eins": [(r["ein"], r["bmf_name"]) for r in q19],
        "fs_list_eins": len(fsx), "fs_grantmaker_eins": sum(1 for v in fsx.values() if v["grantmaker"]),
        "fsd_eins_with_top50_lines": sum(1 for e, v in fsx.items() if v["fsd"] and e in hits),
        "archive_months_used": months, "archive_months_dropped": sorted(set(sizes) - set(months) - set(legacy)),
        "archive_legacy": legacy, "archive_sizes": sizes,
        "recent_eins": len(rr_eins), "recent_eins_with_efile": len(efile), "recent_eins_with_revocation": len(revs),
        "rr_class_by_line": {c: {"lines": sum(1 for t in flat if t[3] and t[3]["class"] == c),
                                 "usd": round(sum(t[1]["amount"] for t in flat if t[3] and t[3]["class"] == c))} for c in RR_CLASSES},
        "base_vs_refined_recent": {f"{b}->{c}": {"lines": len(v), "usd": round(sum(t[1]["amount"] for t in v))}
                                   for (b, c), v in sorted(_group_by_fast(
                                       (t for t in flat if t[3]),
                                       lambda t: ("base_after_end" if ym(t[1]["bmf_ruling"]) > period[t[0]]["end"].strftime("%Y%m")
                                                  else "base_in_window", t[3]["class"])).items())},
        "efile_proxy_vs_archive_class": {f"efile_new={n}->{c}": {"lines": len(v), "usd": round(sum(t[1]["amount"] for t in v))}
                                         for (n, c), v in sorted(_group_by_fast(
                                             (t for t in flat if t[3]), lambda t: (t[3]["efile_new"], t[3]["class"])).items())},
        "all_top50": {f: allrow.get(f) for f in pick},
        "top": {c: top(c, 25) for c in ("fs_fsd_only_ein", "fs_grantmaker_host", "fs_q19_ein", "rr_tc_new_org", "rr_tc_reinstatement",
                                        "rr_tc_redetermination", "rr_dropped_reset_after_grant", "rr_after_period_new_org",
                                        "rr_tc_new_subordinate")},
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
