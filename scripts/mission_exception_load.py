#!/usr/bin/env python3
"""Public exception-load proxy for the top-50 DAF sponsors, FY2023-FY2024 (queue item P-GAP19-05).

For each sponsor-year, the share of grant dollars and of recipient lines that would plausibly need non-routine
review, from public filings only:

  foreign              Schedule I line with a foreign address or a non-US Pub 78 country, plus every Schedule F
                       foreign grant (Form 990 Part IX line 3 dollars; Schedule F Part II line 2 recipient counts,
                       or Part II rows when line 2 is blank, plus Part III recipients).
  not_c3_or_not_pub78  blank/placeholder EIN, EIN absent from Pub 78, or EO BMF subsection other than 03 /
                       deductibility code 2. `..._unexplained` drops lines that carry a label that legitimately
                       explains absence (government, church/religious, group subordinate, possible public university,
                       LLC / possible disregarded entity, foreign) as defined in mission_recipient_compliance.py.
  recent_ruling_24m    EO BMF RULING month on or after (grant-year start - 24 months). Includes rulings dated after
                       the grant year (re-recognitions or late determinations), reported separately.
  fiscal_sponsor_name  recipient name matches a fixed list of large fiscal sponsors (the list used for Q-B15 in
                       breadth-community-faith-infrastructure-emerging.md section 6.1) or a generic marker
                       ("fiscal sponsor/agent", "project of", "sponsored project").
  pf_or_er             private foundations and expenditure-responsibility (ER) cases. `er_required`: Pub 78 code PF
                       or SONFI, or BMF FOUNDATION 04 (non-operating private foundation) or 24 (Type III
                       non-functionally-integrated supporting organisation): section 4966(c)(2) does not exempt these,
                       so ER under 4945(h) applies. `pof_only`: Pub 78 POF or BMF FOUNDATION 02/03 (private operating
                       foundation; a 170(b)(1)(A)(vii) organisation, so no ER, but status needs checking).
  any                  union of the five categories (raw not_c3_or_not_pub78; every recent ruling).
  any_core             union using not_c3_or_not_pub78_unexplained and only rulings dated inside
                       [grant-year start - 24 months, grant-year end].

Universe, return choice and Schedule I lines are exactly those of mission_recipient_sectors.py /
mission_recipient_compliance.py (top-50 DAFRC sponsors by FY2024 DAF assets; 94 itemising sponsor-years); the
line screen (`screen`, labels) is imported from mission_recipient_compliance.py unchanged. Schedule F figures are
read from data/mission-2026-11-14/daf-foreign-grants-schedule-f-2023-2024.csv (sponsor_year rows,
mission_foreign_grants.py), matched on sponsor EIN, fiscal year and object id.

Pure functions over immutable inputs; I/O only in `main`. Stdlib only.

Usage:
  python3 scripts/mission_exception_load.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --pub78 data-download-pub78.txt [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
from functools import reduce
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_compliance import (EXPLAINING, load_bmf_ext, load_pub78, period_of,  # noqa: E402
                                          screen)
from mission_recipient_sectors import WHITELIST, annotate, load_lines  # noqa: E402

OUT = os.path.join(DATA, "exception-load-proxy-2026-11-19.csv")
SCHED_F_CSV = os.path.join(DATA, "daf-foreign-grants-schedule-f-2023-2024.csv")
SOURCE = ("IRS Form 990 Schedule I Part II lines (e-file XML via GivingTuesday mirror of IRS TEOS; line cache of "
          "mission_recipient_sectors.py) screened against IRS Pub 78 data (apps.irs.gov/pub/epostcard/, Last-Modified "
          "2026-11-11) and EO BMF (www.irs.gov/pub/irs-soi/eo*.csv, Last-Modified 2026-11-09); Form 990 Part IX "
          "line 3 and Schedule F line 2 counts from daf-foreign-grants-schedule-f-2023-2024.csv")

SVCF = "205205488"  # Silicon Valley CF: its FY2023 Schedule I holds a single $1.309bn line (Further Future Foundation)
BIG4 = frozenset({"110303001", "311640316", "232888152", "237825575"})  # Fidelity, DAFgiving360, Vanguard, NPT
# Faith-affiliated sponsors among the top 50 [I: by name/charter]; Servant Foundation (The Signatry) is a DAFRC
# "national" but Christian-affiliated, so sponsor_type moves it to faith while dafrc_segment keeps "national".
FAITH = frozenset({"581493949", "237174183", "042103559", "941156533", "956111928", "411802412", "431890105"})

FISCAL_SPONSORS = re.compile(
    r"^(THE )?TIDES (FOUNDATION|CENTER)\b|^PUBLIC HEALTH INSTITUTE( INC)?$|"
    r"\b(NEW VENTURE FUND|HOPEWELL FUND|WINDWARD FUND|"
    r"ROCKEFELLER PHILANTHROPY ADVISORS|FRACTURED ATLAS|SOCIAL GOOD FUND|PLAYERS PHILANTHROPY FUND|"
    r"TRUST FOR CONSERVATION INNOVATION|EARTH ISLAND INSTITUTE|THIRD SECTOR NEW ENGLAND|TSNE MISSIONWORKS|"
    r"SOCIAL AND ENVIRONMENTAL ENTREPRENEURS|NORTH STAR FUND|MULTIPLYING GOOD|"
    r"OPEN COLLECTIVE FOUNDATION|PROPEL NONPROFITS)\b|^(THE )?TIDES( INC)?$|^COMMUNITY PARTNERS( INC)?$|"
    r"^FJC( A FOUNDATION OF PHILANTHROPIC FUNDS)?( INC)?$")
FISCAL_MARKER = re.compile(r"\bFISCAL(LY)? (SPONSOR|SPONSORED|AGENT)\b|\bA PROJECT OF\b|\bSPONSORED PROJECT\b")
C3_TEXT = re.compile(r"501\s*\(?\s*C\s*\)?\s*\(?\s*3\s*\)?")
ER_CODES = frozenset({"PF", "SONFI"})   # non-operating private foundation; Type III non-functionally-integrated SO
POF_CODES = frozenset({"POF"})          # private operating foundation (170(b)(1)(A)(vii) via (F)(i): no ER needed)
ER_BMF = frozenset({"04", "24"})
POF_BMF = frozenset({"02", "03"})

SI_CATS = ("foreign_si", "not_c3_or_not_pub78", "not_c3_or_not_pub78_unexplained", "recent_ruling_24m",
           "recent_ruling_after_period_end", "fiscal_sponsor_name", "fiscal_sponsor_listed", "pf_or_er",
           "er_required", "pof_only",
           "any_si", "any_core_si", "irc_text_not_c3", "d2d")
TOTAL_CATS = ("foreign", "not_c3_or_not_pub78", "not_c3_or_not_pub78_unexplained", "recent_ruling_24m",
              "fiscal_sponsor_name", "pf_or_er", "any", "any_core")


# ----------------------------------------------------------------------------- line flags (pure)
def upname(s: str) -> str:
    return " ".join(re.sub(r"[^A-Z0-9 ]", " ", (s or "").upper().replace("&", " AND ")).split())


def ruling_cutoff(start) -> str:
    m = start.year * 12 + start.month - 1 - 24
    return f"{m // 12:04d}{m % 12 + 1:02d}"


def line_flags(r: Mapping, start, end) -> frozenset:
    """Category set for one screened Schedule I line (r = mission_recipient_compliance.screen output)."""
    nm = upname(r["name"])
    labels = frozenset(r["labels"])
    ruling = (r["bmf_ruling"] or "")[:6]
    has_ruling = r["in_bmf"] and ruling.isdigit() and ruling > "000000"
    foreign = "foreign" in labels
    not_c3 = (not r["ein"]) or (not r["in_pub78"]) or \
        (r["in_bmf"] and (r["bmf_subsection"] not in ("03", "") or r["bmf_deductibility"] == "2"))
    not_c3_unexpl = not_c3 and not (labels & EXPLAINING)
    recent = bool(has_ruling and ruling >= ruling_cutoff(start))
    recent_after = bool(has_ruling and ruling > end.strftime("%Y%m"))
    listed = bool(FISCAL_SPONSORS.search(nm))
    fiscal = listed or bool(FISCAL_MARKER.search(nm))
    codes = frozenset(c.strip() for c in (r["pub78_codes"] or "").split(","))
    er = bool(ER_CODES & codes) or bool(r["in_bmf"] and r["bmf_foundation"] in ER_BMF)
    pof = bool(POF_CODES & codes) or bool(r["in_bmf"] and r["bmf_foundation"] in POF_BMF)
    pf = er or pof
    irc_not_c3 = bool((r["irc"] or "").strip()) and not C3_TEXT.search((r["irc"] or "").upper())
    base = {"foreign_si": foreign, "not_c3_or_not_pub78": not_c3, "not_c3_or_not_pub78_unexplained": not_c3_unexpl,
            "recent_ruling_24m": recent, "recent_ruling_after_period_end": recent_after,
            "fiscal_sponsor_name": fiscal, "fiscal_sponsor_listed": listed, "pf_or_er": pf,
            "er_required": er, "pof_only": pof and not er,
            "irc_text_not_c3": irc_not_c3, "d2d": bool(r["d2d"])}
    union = foreign or not_c3 or recent or fiscal or pf
    core = foreign or not_c3_unexpl or (recent and not recent_after) or fiscal or pf
    return frozenset(k for k, v in {**base, "any_si": union, "any_core_si": core}.items() if v)


def tally(lines: Iterable[tuple]) -> dict:
    """lines: (amount, flags, d2d) -> counts and dollars per category, plus totals and ex-DAF-to-DAF totals."""
    ls = tuple(lines)
    by = {c: tuple(a for a, f, _ in ls if c in f) for c in SI_CATS}
    nd = tuple((a, f) for a, f, d in ls if not d)
    return {"si_lines": len(ls), "si_usd": sum(a for a, _, _ in ls),
            "si_lines_ex_d2d": len(nd), "si_usd_ex_d2d": sum(a for a, _ in nd),
            "any_si_lines_ex_d2d": sum(1 for _, f in nd if "any_si" in f),
            "any_si_usd_ex_d2d": sum(a for a, f in nd if "any_si" in f),
            **{f"{c}_lines": len(v) for c, v in by.items()}, **{f"{c}_usd": sum(v) for c, v in by.items()}}


# ----------------------------------------------------------------------------- Schedule F (pure)
def to_f(x: str) -> float:
    try:
        return float(x) if x not in (None, "") else 0.0
    except ValueError:
        return 0.0


def sched_f_of(row: Mapping | None) -> dict:
    if not row:
        return {"f_usd": 0.0, "f_recipients": 0, "f_count_basis": "no_row", "f_other_org_cnt": 0, "f_oid": ""}
    c3, oth = row.get("sched_f_part2_501c3_cnt", ""), row.get("sched_f_part2_other_org_cnt", "")
    line2 = c3 != "" or oth != ""
    p2 = int(to_f(c3) + to_f(oth)) if line2 else int(to_f(row.get("sched_f_part2_lines")))
    p3 = int(to_f(row.get("sched_f_part3_recipients")))
    l3 = to_f(row.get("part_ix_l3_foreign_usd"))
    basis = ("line2_counts" if line2 else "part2_rows_fallback") if p2 else ("none" if not l3 else "no_count")
    return {"f_usd": l3, "f_recipients": p2 + p3, "f_count_basis": basis + ("+part3" if p3 else ""),
            "f_other_org_cnt": int(to_f(oth)), "f_oid": row.get("object_id", ""),
            "f_l1": to_f(row.get("part_ix_l1_domestic_orgs_usd")), "f_total_grants": to_f(row.get("total_grants_usd"))}


# ----------------------------------------------------------------------------- shares (pure)
SUM_KEYS = (("si_lines", "si_usd", "si_lines_ex_d2d", "si_usd_ex_d2d", "any_si_lines_ex_d2d", "any_si_usd_ex_d2d",
             "f_usd", "f_recipients", "f_other_org_cnt", "f_total_grants")
            + tuple(f"{c}_{m}" for c in SI_CATS for m in ("lines", "usd")))


def add(a: Mapping, b: Mapping) -> dict:
    return {k: (a.get(k) or 0) + (b.get(k) or 0) for k in SUM_KEYS}


def ratio(n: float, d: float):
    return round(n / d, 6) if d else None


def shares(t: Mapping) -> dict:
    den_n, den_usd = t["si_lines"] + t["f_recipients"], t["si_usd"] + t["f_usd"]
    tot = {"foreign": ("foreign_si", True), "not_c3_or_not_pub78": ("not_c3_or_not_pub78", False),
           "not_c3_or_not_pub78_unexplained": ("not_c3_or_not_pub78_unexplained", False),
           "recent_ruling_24m": ("recent_ruling_24m", False), "fiscal_sponsor_name": ("fiscal_sponsor_name", False),
           "pf_or_er": ("pf_or_er", False), "any": ("any_si", True), "any_core": ("any_core_si", True)}
    out = {"denom_lines": den_n, "denom_usd": round(den_usd)}
    for c, (si, plus_f) in tot.items():
        n = t[f"{si}_lines"] + (t["f_recipients"] if plus_f else 0)
        u = t[f"{si}_usd"] + (t["f_usd"] if plus_f else 0)
        out = {**out, f"{c}_lines": n, f"{c}_usd": round(u), f"{c}_count_share": ratio(n, den_n),
               f"{c}_usd_share": ratio(u, den_usd)}
    cs, us = out["any_count_share"], out["any_usd_share"]
    ex_n = t["si_lines_ex_d2d"] + t["f_recipients"]
    ex_u = t["si_usd_ex_d2d"] + t["f_usd"]
    flag_n, flag_u = out["any_lines"], out["any_usd"]
    rest_n, rest_u = den_n - flag_n, den_usd - flag_u
    return {**out,
            "any_gap_pp": round((us - cs) * 100, 3) if us is not None and cs is not None else None,
            "any_usd_to_count_ratio": round(us / cs, 3) if cs else None,
            "any_core_gap_pp": round((out["any_core_usd_share"] - out["any_core_count_share"]) * 100, 3)
            if out["any_core_usd_share"] is not None else None,
            "avg_usd_flagged_line": round(flag_u / flag_n) if flag_n else None,
            "avg_usd_other_line": round(rest_u / rest_n) if rest_n else None,
            "any_count_share_ex_d2d": ratio(t["any_si_lines_ex_d2d"] + t["f_recipients"], ex_n),
            "any_usd_share_ex_d2d": ratio(t["any_si_usd_ex_d2d"] + t["f_usd"], ex_u),
            "sched_i_foreign_address_usd": round(t["foreign_si_usd"]),
            "l3_foreign_share_of_total_grants": ratio(t["f_usd"], t["f_total_grants"]),
            "fiscal_sponsor_listed_share_of_sched_i_usd": ratio(t["fiscal_sponsor_listed_usd"], t["si_usd"]),
            "fiscal_sponsor_any_share_of_sched_i_usd": ratio(t["fiscal_sponsor_name_usd"], t["si_usd"]),
            "irc_text_not_c3_share_of_sched_i_usd": ratio(t["irc_text_not_c3_usd"], t["si_usd"]),
            "recent_ruling_after_period_end_lines": t["recent_ruling_after_period_end_lines"],
            "recent_ruling_after_period_end_usd": round(t["recent_ruling_after_period_end_usd"]),
            "d2d_usd": round(t["d2d_usd"]), "sched_f_other_org_cnt": t["f_other_org_cnt"],
            "er_required_lines": t["er_required_lines"], "er_required_usd": round(t["er_required_usd"]),
            "pof_only_lines": t["pof_only_lines"], "pof_only_usd": round(t["pof_only_usd"])}


def label_mix(screened: Mapping, flags: Mapping, cat: str) -> dict:
    """Dollars and lines in category `cat` by the explaining labels they carry ('none' when unlabelled)."""
    hits = tuple(("+".join(sorted(frozenset(r["labels"]) & EXPLAINING)) or ("blank_ein" if not r["ein"] else "none"),
                  r["amount"]) for k, rs in screened.items() for r, f in zip(rs, flags[k]) if cat in f)
    by = _group_by_fast(hits, lambda h: h[0])
    return {k: {"lines": len(v), "usd": round(sum(a for _, a in v))}
            for k, v in sorted(by.items(), key=lambda kv: -sum(a for _, a in kv[1]))[:12]}


def dist(vals: Sequence[float]) -> dict:
    v = sorted(x for x in vals if x is not None)
    if not v:
        return {}
    q = statistics.quantiles(v, n=4, method="inclusive") if len(v) > 1 else [v[0]] * 3
    return {"min": round(v[0], 6), "p25": round(q[0], 6), "median": round(q[1], 6), "p75": round(q[2], 6),
            "max": round(v[-1], 6)}


# ----------------------------------------------------------------------------- rows (pure)
def sponsor_type(ein: str, segment: str) -> str:
    return "faith" if ein in FAITH else ("single_issue_other" if segment == "single_issue" else segment)


def base_row(row_type: str, scope: str, **kw) -> dict:
    return {"row_type": row_type, "scope": scope, **kw, "source": SOURCE}


def sy_row(k, t: Mapping, meta: Mapping) -> dict:
    return base_row("sponsor_year", meta["name"], ein=k[0], dafrc_segment=meta["segment"],
                    sponsor_type=sponsor_type(k[0], meta["segment"]), rank_fy2024=meta["rank"], fiscal_year=str(k[1]),
                    sponsor_years=1, object_id=meta["oid"], tax_period_end=meta["tpe"],
                    sched_i_status=meta["status"], sched_f_count_basis=meta["f_count_basis"],
                    sched_i_lines=t["si_lines"], sched_i_usd=round(t["si_usd"]), sched_f_foreign_recipients=t["f_recipients"],
                    sched_f_foreign_usd=round(t["f_usd"]), part_ix_total_grants_usd=round(t["f_total_grants"]),
                    **(shares(t) if meta["status"] == "itemised" else {}))


def scope_row(row_type: str, scope: str, keys: Sequence, tallies: Mapping, meta: Mapping, sponsor_vals=None) -> dict:
    t = reduce(add, (tallies[k] for k in keys), {})
    sp = sorted({k[0] for k in keys})
    segs = sorted({meta[k]["segment"] for k in keys})
    extra = {}
    if sponsor_vals is not None:
        du, dc = dist([v["any_usd_share"] for v in sponsor_vals]), dist([v["any_count_share"] for v in sponsor_vals])
        dg = dist([v["any_gap_pp"] for v in sponsor_vals])
        extra = {**{f"sponsor_any_usd_share_{q}": x for q, x in du.items()},
                 **{f"sponsor_any_count_share_{q}": x for q, x in dc.items()},
                 **{f"sponsor_any_gap_pp_{q}": x for q, x in dg.items()}}
    one = meta[keys[0]]
    return base_row(row_type, scope, ein=sp[0] if len(sp) == 1 else "",
                    dafrc_segment=segs[0] if len(segs) == 1 else "",
                    sponsor_type=sponsor_type(sp[0], one["segment"]) if len(sp) == 1 else
                    (scope if row_type == "sponsor_type" else ""),
                    rank_fy2024=one["rank"] if len(sp) == 1 else "", fiscal_year="-".join(sorted({str(k[1]) for k in keys})),
                    sponsor_years=len(keys), n_sponsors=len(sp), sched_i_status="itemised",
                    sched_i_lines=t["si_lines"], sched_i_usd=round(t["si_usd"]), sched_f_foreign_recipients=t["f_recipients"],
                    sched_f_foreign_usd=round(t["f_usd"]), part_ix_total_grants_usd=round(t["f_total_grants"]),
                    **shares(t), **extra)


def build_rows(tallies: Mapping, meta: Mapping) -> list:
    item = tuple(k for k in sorted(tallies, key=lambda k: (meta[k]["rank"], k[1])) if meta[k]["status"] == "itemised")
    sy = [sy_row(k, tallies[k], meta[k]) for k in sorted(tallies, key=lambda k: (meta[k]["rank"], k[1]))]
    sponsors = sorted({k[0] for k in item}, key=lambda e: next(meta[k]["rank"] for k in item if k[0] == e))
    sp_rows = [scope_row("sponsor", meta[next(k for k in item if k[0] == e)]["name"],
                         [k for k in item if k[0] == e], tallies, meta) for e in sponsors]
    by_sp = {r["ein"]: r for r in sp_rows}
    group = lambda rt, label, pred: scope_row(  # noqa: E731
        rt, label, [k for k in item if pred(k)], tallies, meta,
        [by_sp[e] for e in sponsors if any(pred(k) for k in item if k[0] == e)])
    types = ("national", "community_foundation", "faith", "single_issue_other", "processor", "university_hospital")
    segs = ("national", "community_foundation", "single_issue", "processor", "university_hospital")
    agg = ([group("all", "all_top50_itemising", lambda k: True),
            group("all", "all_ex_university_hospital", lambda k: meta[k]["segment"] != "university_hospital"),
            group("all", "all_ex_university_hospital_ex_svcf",
                  lambda k: meta[k]["segment"] != "university_hospital" and k[0] != SVCF),
            group("big4_nationals", "fidelity_dafgiving360_vanguard_npt", lambda k: k[0] in BIG4)]
           + [group("sponsor_type", t, (lambda k, t=t: sponsor_type(k[0], meta[k]["segment"]) == t)) for t in types]
           + [group("dafrc_segment", s, (lambda k, s=s: meta[k]["segment"] == s)) for s in segs]
           + [scope_row("all_fy", f"all_top50_itemising_fy{fy}", [k for k in item if k[1] == fy], tallies, meta)
              for fy in FYS]
           + [scope_row("big4_fy", f"big4_nationals_fy{fy}", [k for k in item if k[1] == fy and k[0] in BIG4],
                        tallies, meta) for fy in FYS])
    return agg + sp_rows + sy


FIELDS = ("row_type", "scope", "ein", "dafrc_segment", "sponsor_type", "rank_fy2024", "fiscal_year", "sponsor_years",
          "n_sponsors", "object_id", "tax_period_end", "sched_i_status", "sched_f_count_basis", "sched_i_lines",
          "sched_i_usd", "sched_f_foreign_recipients", "sched_f_foreign_usd", "part_ix_total_grants_usd",
          "denom_lines", "denom_usd") + tuple(f"{c}_{m}" for c in TOTAL_CATS
                                               for m in ("lines", "usd", "count_share", "usd_share")) + (
          "any_gap_pp", "any_usd_to_count_ratio", "any_core_gap_pp", "avg_usd_flagged_line", "avg_usd_other_line",
          "any_count_share_ex_d2d", "any_usd_share_ex_d2d", "sched_i_foreign_address_usd",
          "l3_foreign_share_of_total_grants", "fiscal_sponsor_listed_share_of_sched_i_usd",
          "fiscal_sponsor_any_share_of_sched_i_usd", "irc_text_not_c3_share_of_sched_i_usd",
          "recent_ruling_after_period_end_lines", "recent_ruling_after_period_end_usd", "d2d_usd",
          "sched_f_other_org_cnt", "er_required_lines", "er_required_usd", "pof_only_lines", "pof_only_usd") + tuple(f"sponsor_any_{m}_{q}" for m in ("usd_share", "count_share", "gap_pp")
                                           for q in ("min", "p25", "median", "p75", "max")) + ("source",)


def top_by(screened: Mapping, flags: Mapping, cat: str, n: int) -> list:
    """Largest recipients (by EIN, else normalised name) among lines carrying category `cat`."""
    hits = tuple((r["ein"] or "N:" + upname(r["name"]), upname(r["name"]), r["amount"], r["pub78_codes"],
                  r["bmf_foundation"], r["bmf_ruling"], ";".join(r["labels"]))
                 for k, rs in screened.items() for r, f in zip(rs, flags[k]) if cat in f)
    by = _group_by_fast(hits, lambda h: h[0])
    tot = sorted(((e, sum(h[2] for h in v), v) for e, v in by.items()), key=lambda t: -t[1])[:n]
    return [{"key": e, "name": v[0][1], "usd": round(u), "lines": len(v), "pub78": v[0][3], "bmf_found": v[0][4],
             "ruling": v[0][5], "labels": v[0][6]} for e, u, v in tot]


# ----------------------------------------------------------------------------- main (I/O edge)
def _amt(l: Sequence) -> float:
    return float(l[4] or 0.0) + float(l[5] or 0.0)


def is_totals_row(l: Sequence, named_sum: float, named_n: int) -> bool:
    """A Schedule I line with no name and no EIN whose amount equals the sum of the named
    lines, or the number of named lines, is a filer's totals row, not a grant [V wave 32A]."""
    return (not l[0] and not l[1].strip()
            and (abs(_amt(l) - named_sum) < 1.0 or abs(_amt(l) - named_n) < 0.5))


def drop_totals_rows(v: Mapping) -> dict:
    named = tuple(x for x in v["lines"] if x[1].strip())
    s, n = sum(map(_amt, named)), len(named)
    return {**v, "lines": [l for l in v["lines"] if not is_totals_row(l, s, n)]}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; accepted for the repo's CLI convention)")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--pub78", required=True)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

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
    irc = {k: tuple(l[3] for l in v["lines"]) for k, v in good.items()}
    eins = frozenset(r["ein"] for rs in ann.values() for r in rs if r["ein"])
    bmf = load_bmf_ext(a.bmf_dir, eins)
    p78, _ = load_pub78(a.pub78, eins, frozenset())
    period = {k: dict(zip(("start", "end"), period_of(item[k]["tax_period_end"]))) for k in good}
    screened = {k: tuple(screen(r, irc[k][i], period[k], bmf, p78, {}, {}) for i, r in enumerate(ann[k])) for k in ann}
    flags = {k: tuple(line_flags(r, period[k]["start"], period[k]["end"]) for r in rs) for k, rs in screened.items()}

    sf_rows = {(ein9(r["ein"]), int(r["fiscal_year"])): r for r in read_csv(SCHED_F_CSV) if r["row_type"] == "sponsor_year"}
    keys = tuple(present)
    sf = {k: sched_f_of(sf_rows.get(k)) for k in keys}
    meta = {k: {"name": panel[k[0]]["name"], "segment": panel[k[0]]["segment"], "rank": rank[k[0]],
                "oid": present[k]["oid"], "tpe": present[k]["tax_period_end"],
                "status": "itemised" if k in good else ("attachment_only" if k not in item else "lines_not_loaded"),
                "f_count_basis": sf[k]["f_count_basis"]} for k in keys}
    empty = tally(())
    tallies = {k: {**(tally((r["amount"], f, r["d2d"]) for r, f in zip(screened[k], flags[k])) if k in good else empty),
                   **{x: sf[k][x] for x in ("f_usd", "f_recipients", "f_other_org_cnt")},
                   "f_total_grants": sf[k].get("f_total_grants", 0.0)} for k in keys}
    rows = build_rows(tallies, meta)
    write_csv(a.out, rows, FIELDS)

    pick = lambda scope: next(r for r in rows if r["scope"] == scope)  # noqa: E731
    keep = ("sponsor_years", "n_sponsors", "denom_lines", "denom_usd") + tuple(
        f"{c}_{m}" for c in TOTAL_CATS for m in ("lines", "usd", "count_share", "usd_share")) + (
        "any_gap_pp", "any_usd_to_count_ratio", "any_core_gap_pp", "avg_usd_flagged_line", "avg_usd_other_line",
        "any_count_share_ex_d2d", "any_usd_share_ex_d2d", "l3_foreign_share_of_total_grants",
        "fiscal_sponsor_listed_share_of_sched_i_usd", "fiscal_sponsor_any_share_of_sched_i_usd",
        "irc_text_not_c3_share_of_sched_i_usd", "sched_i_foreign_address_usd", "recent_ruling_after_period_end_usd",
        "er_required_lines", "er_required_usd", "pof_only_lines", "pof_only_usd", "sched_f_other_org_cnt", "d2d_usd",
        "sponsor_any_usd_share_median", "sponsor_any_count_share_median", "sponsor_any_gap_pp_median",
        "sponsor_any_usd_share_min", "sponsor_any_usd_share_max", "sponsor_any_count_share_min",
        "sponsor_any_count_share_max")
    slim = lambda r: {k: r.get(k) for k in keep if r.get(k) not in (None, "")}  # noqa: E731
    summary = {
        "sponsor_years_present": len(present), "sponsor_years_itemised_loaded": len(good),
        "not_itemised": sorted(f"{meta[k]['name']} FY{k[1]}" for k in keys if meta[k]["status"] != "itemised"),
        "sched_f_oid_mismatch": sorted(f"{meta[k]['name']} FY{k[1]}" for k in keys
                                       if sf[k]["f_oid"] and sf[k]["f_oid"] != meta[k]["oid"]),
        "sched_f_missing": sorted(f"{meta[k]['name']} FY{k[1]}" for k in keys if sf[k]["f_count_basis"] == "no_row"),
        "count_basis_mix": {b: sum(1 for k in good if meta[k]["f_count_basis"] == b)
                            for b in sorted({meta[k]["f_count_basis"] for k in good})},
        "lines": sum(len(v) for v in screened.values()), "eins": len(eins), "in_bmf": len(bmf), "in_pub78": len(p78),
        "scopes": {r["scope"]: slim(r) for r in rows if r["row_type"] not in ("sponsor", "sponsor_year")},
        "sponsors_by_any_usd_share": sorted(({"sponsor": r["scope"][:40], "type": r["sponsor_type"],
                                              "usd_share": r["any_usd_share"], "count_share": r["any_count_share"],
                                              "gap_pp": r["any_gap_pp"]} for r in rows if r["row_type"] == "sponsor"),
                                            key=lambda d: -(d["usd_share"] or 0)),
        "not_c3_or_not_pub78_label_mix": label_mix(screened, flags, "not_c3_or_not_pub78"),
        "top_recipients": {c: top_by(screened, flags, c, 30 if c.startswith("fiscal") else 15) for c in
                           ("fiscal_sponsor_name", "fiscal_sponsor_listed", "pf_or_er", "recent_ruling_24m", "recent_ruling_after_period_end",
                            "not_c3_or_not_pub78_unexplained", "foreign_si", "er_required")},
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
