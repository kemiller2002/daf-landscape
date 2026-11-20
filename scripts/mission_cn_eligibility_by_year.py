#!/usr/bin/env python3
"""P-B40N1202-B43N26-04: Charity Navigator rating eligibility of top-50 DAF dollars as of each grant year.

The parent study (scripts/mission_recipient_basis_eligibility.py, imported, not modified) tested CN's 2026 published
eligibility rules against filings available in November 2026: 76.85% of top-50 FY2023-24 DAF-weighted Schedule I
dollars went to rating-eligible recipients. This script re-tests every grant against the filings that were available
when its sponsor-year ended.

Grant unit   One recipient EIN x one sponsor-year (sponsor EIN, FY), from the same annotated Schedule I lines, DAF
             weights and DAF-to-DAF filter as the parent (`build_numerator`). Blank-EIN lines stay ineligible, as in
             the parent. Each sponsor-year's fiscal year is the 12 months ending on its chosen return's
             tax_period_end (`pick_returns`, as mission_non_bmf_recipients.py). Grant dates inside the year are not
             public.

Cut-off      Central: the end of the sponsor's fiscal year (the task's "filings available at the end of FY2023 and
             FY2024"). Sensitivity: the first day of that fiscal year (a grant made on day one; this also stands in
             for a twelve-month lag between IRS processing and CN receiving the return).

"Available"  A return counts if its IRS processing date is on or before the cut-off. The processing date is the
             Julian date in the e-file DLN, which the TEOS OBJECT_ID repeats: OBJECT_ID[:4] = processing year,
             OBJECT_ID[5:8] = Julian day (checked: equal to DLN[5:8] on every 990/990-EZ/990-PF row of the 2019-2026
             index files). When CN actually received each return is not public.

Filing rules (as the parent's cn_filing_test, re-dated)
             >= 3 distinct e-filed 990-series tax periods with a tax period ending in years Y-6..Y-1, where Y is the
             cut-off year (the parent's Nov 2026 window is 2020-2025, i.e. Y-6..Y-1 for Y = 2026); amendments
             collapsed to the latest object id per tax period among returns processed by the cut-off; >= 2 of the
             4 most recent periods are full 990s; the latest is not a 990-PF. Sensitivity: processing year
             Y-5..Y (the parent's index-year window, re-dated). The order of tests and the reason labels are the
             parent's `cn_reason` (central DAF-sponsor reading: national and processor panel segments).

IRS status as of the cut-off
             No dated EO BMF or Pub 78 extract is published for 2023-24 (see b40n1202-b43n26-03 §1.3), so:
             - current_bmf variants use the November 2026 BMF row as the status at grant time (as the parent);
             - reconstructed variants (headline) adjust it with dated IRS evidence:
               * an EIN in the current BMF with an automatic revocation effective on or before the cut-off and a
                 reinstatement date after it was listed as revoked -> `revoked_at_cutoff_later_reinstated`;
               * an EIN absent from the current BMF is presumed listed at the cut-off as a 501(c)(3) when there is
                 501(c)(3) evidence (exemption type 03 on the revocation list, or Organization501c3Ind on a cached
                 return header from the b40n1202-b43n26-03 run) AND evidence that it left the BMF after the cut-off
                 (an automatic revocation effective after the cut-off, or a 990-series return processed after it).
                 Its foundation code is unknown; a 990-PF latest return still fails `latest_is_990pf`.
             Sensitivity only (`plus_ruling_date_rule`): an EIN in the current BMF whose RULING (YYYYMM) is after
             the cut-off month is treated as not yet recognised (`not_yet_recognised_at_cutoff`). It is not in the
             headline because RULING is reset by later determinations: KIPP New York (ruling 202512) and Christian
             Union (202505) filed full 990s for years before those dates.
             Pub 78 presence is reported as a diagnostic only (current file; no dated version).

Index coverage  The parent's cached TEOS index starts with the 2019 file, which holds only part of processing year
             2018 and none before it. As-of windows reach back to tax year 2017 (cut-offs in 2023), so the as-of
             variants also read the 2017 and 2018 index files (--early-index-dir; same row shape and DLN form rule).
             The current-status reproduction uses the parent's 2019-2026 files only.

Other variants
             - index_2019_on_only: the headline with the parent's 2019-2026 index only (shows what the early files
               change); `_plus_gap_bound` passes any unit that fails only on the three-return rule and would reach
               three if every window tax year <= 2018 it lacks had been filed (the bound that the early files
               replace).
             - asof_fy_end_current_bmf: filings re-dated, IRS status as in November 2026 (no reconstruction).
             - asof_fy_end_reconstructed_index_year_window: processing-year window Y-5..Y.
             - cz_lookthrough: the four Chan Zuckerberg LLC EINs (disregarded entities of Chan Zuckerberg Biohub
               Inc, EIN 81-1669175, per its FY2023-24 Schedule R; validation wave 46A) are tested as that parent.

Pure functions; I/O only in the load helpers and `main`. Stdlib only. No network access (cached files only).

Usage:
  python3 scripts/mission_cn_eligibility_by_year.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --index-dir IRSDIR --early-index-dir IRS_2017_2018 --xml-cache NB03_XMLHDR [--out CSV]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DATA, _group_by_fast, ein9, write_csv  # noqa: E402
from mission_daf_share_recipient_revenue import load_bmf  # noqa: E402
from mission_daf_to_daf import load_np, pick_returns  # noqa: E402
from mission_recipient_basis_eligibility import (DLN_FORM, build_numerator, cn_filing_test, cn_reason, load_bmf_extra,  # noqa: E402
                                                 load_history, no_ein_lines, per_period)
from mission_non_bmf_recipients import fetch_header, fy_bounds, load_pub78, load_revocation, parse_date  # noqa: E402
from mission_recipient_sectors import BMF_FILES  # noqa: E402

OUT = os.path.join(DATA, "cn-eligibility-by-year-2026-11-20.csv")
INDEX_DOWNLOAD = dt.date(2026, 11, 15)          # index_2026.csv cache date (parent note §5 item 7)
CZ_PARENT = "811669175"                          # Chan Zuckerberg Biohub Inc (validation wave 46A)
CZ_LLCS = ("882242512", "882010111", "931478843", "922259616")
FIRST_FULL_INDEX_TY = 2019                        # parent's index (2019-2026): tax years <= 2018 may be missing
EARLY_YEARS = (2017, 2018)                        # extra TEOS index files read for the as-of windows
EARLY_FIRST_TY = 2017                             # with them, every as-of window year (>= 2017) is covered
SRC = ("Dollars: top-50 DAFRC sponsors' Schedule I Part II lines FY2023-24, net of DAF-to-DAF, DAF-weighted "
       "(mission_recipient_basis_eligibility.py). Eligibility: Charity Navigator rules "
       "(intercom.help/charity-navigator/en/articles/8557824, 2026-04-09) re-dated to each sponsor-year's cut-off "
       "using IRS TEOS e-file index 2019-2026 processing dates (apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv), "
       "IRS EO BMF (www.irs.gov/pub/irs-soi/eo*.csv), revocation list and Pub 78 "
       "(apps.irs.gov/pub/epostcard/data-download-*.zip).")


# ----------------------------------------------------------------------------- pure helpers
def proc_date(oid: str) -> dt.date:
    """IRS processing date from the TEOS object id (year + Julian day, as in the DLN)."""
    return dt.date(int(oid[:4]), 1, 1) + dt.timedelta(days=int(oid[5:8]) - 1)


def asof_test(filings: Sequence[Mapping], cutoff: dt.date, window: str = "tax_year",
              first_full_ty: int = FIRST_FULL_INDEX_TY) -> dict:
    """The parent's cn_filing_test, restricted to returns processed by `cutoff` and with the window re-dated."""
    avail = tuple(r for r in filings if proc_date(r["oid"]) <= cutoff)
    periods = per_period(avail)
    y = cutoff.year
    lo, hi = (y - 6, y - 1) if window == "tax_year" else (y - 5, y)
    key = (lambda p: int(p["tax_period"][:4])) if window == "tax_year" else (lambda p: int(p["oid"][:4]))
    in_win = tuple(p for p in periods if lo <= key(p) <= hi)
    last4 = periods[:4]
    gap = sum(1 for ty in range(lo, min(hi, first_full_ty - 1) + 1)
              if ty not in {int(p["tax_period"][:4]) for p in periods}) if window == "tax_year" else 0
    return {"n_periods": len(periods), "n_in_window": len(in_win), "n_full_990_last4": sum(p["form"] == "990" for p in last4),
            "latest_form": periods[0]["form"] if periods else "", "latest_tp": periods[0]["tax_period"] if periods else "",
            "forms_last4": ";".join(p["form"] for p in last4), "pre2019_gap_years": gap,
            "processed_after_cutoff": any(proc_date(r["oid"]) > cutoff for r in filings)}


def status_asof(e: str, b: Mapping | None, cutoff: dt.date, rev: Sequence[Mapping], c3_hdr: bool,
                t: Mapping, use_ruling: bool = False) -> tuple[Mapping | None, str]:
    """Reconstructed IRS status at the cut-off -> (bmf-like row or None, pre-empting reason or '')."""
    last = rev[-1] if rev else None
    if b is not None:
        ruling = b.get("ruling", "")
        if use_ruling and len(ruling) == 6 and ruling.isdigit() and ruling > cutoff.strftime("%Y%m"):
            return b, "not_yet_recognised_at_cutoff"
        if any(r["rev_date"] and r["rev_date"] <= cutoff and r["reinst_date"] and r["reinst_date"] > cutoff for r in rev):
            return b, "revoked_at_cutoff_later_reinstated"
        return b, ""
    c3 = c3_hdr or any(r["exempt_type"] == "03" for r in rev)
    left_later = bool(last and last["rev_date"] and last["rev_date"] > cutoff) or t["processed_after_cutoff"]
    revoked_before = bool(last and last["rev_date"] and last["rev_date"] <= cutoff and not last["reinst_date"])
    if c3 and left_later and not revoked_before:
        return {"subsection": "03", "foundation": "", "group": "", "affiliation": "", "reconstructed": True}, ""
    return None, ""


def reason_for(b, seg: str, t: Mapping, pre: str) -> str:
    return pre or cn_reason(b, seg, t, "national")


def is_ok(r: str) -> bool:
    return r == "eligible"


def bound_pass(r: str, t: Mapping) -> bool:
    return is_ok(r) or (r == "fewer_than_3_efiled_in_6y" and t["n_in_window"] + t["pre2019_gap_years"] >= 3
                        and t["latest_form"] != "990PF" and t["n_full_990_last4"] >= 2)


def share_rows(units: Sequence[Mapping], variant: str, rk: str, scope_type: str, scope: str, pred,
               cats: bool = True) -> list:
    sub = tuple(u for u in units if pred(u))
    tdw, tsi, n = sum(u["dw"] for u in sub), sum(u["si"] for u in sub), len(sub)

    def row(cat):
        hit = sub if cat == "all" else tuple(u for u in sub if u[rk] == cat)
        dw, si = sum(u["dw"] for u in hit), sum(u["si"] for u in hit)
        return {"row_type": "share", "variant": variant, "scope_type": scope_type, "scope": scope, "category": cat,
                "grant_units": len(hit), "recipients": len({u["key"] for u in hit}), "grant_unit_share": len(hit) / n if n else None,
                "usd_daf_weighted": round(dw), "dollar_share_daf_weighted": dw / tdw if tdw else None,
                "usd_sched_i": round(si), "dollar_share_sched_i": si / tsi if tsi else None, "source": SRC}
    names = sorted({u[rk] for u in sub}) if cats else ["eligible"]
    return [row("all")] + [row(c) for c in names]


def transition_rows(units: Sequence[Mapping], a: str, b: str, label: str) -> list:
    tot = sum(u["dw"] for u in units)
    by = _group_by_fast(units, lambda u: (u[a], u[b]))
    return [{"row_type": "transition", "variant": label, "scope_type": "all", "scope": "all_recipients",
             "category": f"{k[0]} -> {k[1]}", "grant_units": len(v), "recipients": len({u["key"] for u in v}),
             "usd_daf_weighted": round(sum(u["dw"] for u in v)), "dollar_share_daf_weighted": sum(u["dw"] for u in v) / tot,
             "usd_sched_i": round(sum(u["si"] for u in v)), "source": SRC}
            for k, v in sorted(by.items(), key=lambda kv: -sum(u["dw"] for u in kv[1])) if k[0] != k[1]]


# ----------------------------------------------------------------------------- loaders (I/O)
def load_ruling(bmf_dir: str, eins: frozenset) -> dict:
    def rows(f):
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple((ein9(r["EIN"]), (r.get("RULING") or "").strip()) for r in csv.DictReader(fh) if ein9(r["EIN"]) in eins)
    return dict(x for f in BMF_FILES for x in rows(f))


def load_early_history(index_dir: str, eins: frozenset) -> dict:
    """TEOS index 2017-2018 rows in the parent's load_history row shape (form from the DLN prefix)."""
    def rows(y):
        p = os.path.join(index_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            return ()
        with open(p, encoding="utf-8", errors="replace", newline="") as fh:
            return tuple({"ein": ein9(d["EIN"]), "tax_period": d["TAX_PERIOD"], "form": DLN_FORM[d["DLN"][:5]],
                          "return_type": d["RETURN_TYPE"], "oid": d["OBJECT_ID"], "index_year": y}
                         for d in csv.DictReader(fh)
                         if (d.get("DLN") or "")[:5] in DLN_FORM and ein9(d.get("EIN", "")) in eins)
    return _group_by_fast((r for y in EARLY_YEARS for r in rows(y)), lambda r: r["ein"])


def grant_lines(N: Mapping, tpe: Mapping) -> tuple[dict, ...]:
    """(recipient key, sponsor-year) units with Schedule I and DAF-weighted dollars; blank EINs keyed by name key."""
    flat = tuple(((r["ein"] or "NOEIN:" + r["key"]), k, r["amount"], r["amount"] * N["weights"].get(k, 1.0),
                  r["where"].startswith("F:"))
                 for k, rs in N["ann"].items() for r in rs if not r["d2d"] and r["amount"] > 0)
    by = _group_by_fast(flat, lambda t: (t[0], t[1]))
    return tuple({"key": key, "sponsor": k[0], "fy": k[1], "tpe": tpe.get(k, ""), "si": sum(t[2] for t in v),
                  "dw": sum(t[3] for t in v), "foreign": any(t[4] for t in v)} for (key, k), v in by.items())


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True, help="index_YYYY.csv, data-download-revocation.txt, data-download-pub78.txt")
    ap.add_argument("--early-index-dir", required=True, help="index_2017.csv and index_2018.csv")
    ap.add_argument("--xml-cache", required=True, help="return-header cache of mission_non_bmf_recipients.py (read only)")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    N = build_numerator(a)
    nums, panel = N["nums"], N["panel"]
    tpe = {k: x["tax_period_end"] for k, x in pick_returns(load_np(a.np_cache)).items()}
    lines = grant_lines(N, tpe)
    # reconciliation with the parent's universe
    blank = no_ein_lines(N["ann"], N["weights"])
    tot_parent = sum(sum(v["dw"] for v in n["fy"].values()) for n in nums.values()) + sum(v["dw"] for v in blank.values())
    assert abs(sum(u["dw"] for u in lines) - tot_parent) < 1.0, "dollar reconciliation with the parent failed"
    assert all(fy_bounds(u["tpe"]) for u in lines), "missing sponsor fiscal-year end"

    eins = frozenset(nums) | {CZ_PARENT}
    bmf = load_bmf(a.bmf_dir, eins)
    extra = load_bmf_extra(a.bmf_dir, frozenset(bmf))
    ruling = load_ruling(a.bmf_dir, frozenset(bmf))
    B = {e: {**bmf[e], **extra.get(e, {}), "ruling": ruling.get(e, "")} for e in bmf}
    hist = load_history(a.index_dir, eins)
    early = load_early_history(a.early_index_dir, eins)
    hist_x = {e: tuple(hist.get(e, ())) + tuple(early.get(e, ())) for e in frozenset(hist) | frozenset(early)}
    rev = load_revocation(os.path.join(a.index_dir, "data-download-revocation.txt"), eins)
    pub = load_pub78(os.path.join(a.index_dir, "data-download-pub78.txt"), eins)
    nb = frozenset(e for e in nums if e not in bmf)
    c3_hdr = {e: any("Organization501c3Ind" in fetch_header(r["oid"], a.xml_cache, False).get("flags", [])
                     for r in hist.get(e, ())) for e in nb}
    seg = {e: panel[e]["segment"] if e in panel else "" for e in eins}

    def asof_reason(e: str, cutoff: dt.date) -> str:
        t = asof_test(hist_x.get(e, ()), cutoff)
        b, pre = status_asof(e, B.get(e), cutoff, rev.get(e, ()), c3_hdr.get(e, False), t)
        return reason_for(b, seg[e], t, pre)

    def asof(e: str, fl: Sequence[Mapping], cutoff: dt.date, window: str = "tax_year", first_ty: int = EARLY_FIRST_TY,
             current_bmf: bool = False, use_ruling: bool = False) -> tuple[str, dict, bool]:
        t = asof_test(fl, cutoff, window, first_ty)
        if current_bmf:
            return cn_reason(B.get(e), seg[e], t, "national"), t, False
        b, pre = status_asof(e, B.get(e), cutoff, rev.get(e, ()), c3_hdr.get(e, False), t, use_ruling)
        return reason_for(b, seg[e], t, pre), t, bool(b and b.get("reconstructed"))

    R = ("r_now", "r_end_cur", "r_end", "r_end_ruling", "r_start", "r_end_idx", "r_end_2019", "r_end_2019_bound", "r_now_cz", "r_end_cz")

    def evaluate(u: Mapping) -> dict:
        k = u["key"]
        if k.startswith("NOEIN:"):
            r = "no_ein_foreign" if u["foreign"] else "no_ein_domestic"
            return {**u, **{f: r for f in R}, "presumed_listed": False, "pub78_now": False}
        fy_start, fy_end = fy_bounds(u["tpe"])
        day_before = fy_start - dt.timedelta(days=1)
        e, b = k, B.get(k)
        fl, fx = hist.get(e, ()), hist_x.get(e, ())
        r_now = cn_reason(b, seg[e], cn_filing_test(fl, "tax_year"), "national")
        r_end, _, presumed = asof(e, fx, fy_end)
        r_19, t_19, _ = asof(e, fl, fy_end, first_ty=FIRST_FULL_INDEX_TY)
        cz = e in CZ_LLCS
        pfl = hist.get(CZ_PARENT, ())
        return {**u, "r_now": r_now,
                "r_end_cur": asof(e, fx, fy_end, current_bmf=True)[0],
                "r_end": r_end, "r_end_ruling": asof(e, fx, fy_end, use_ruling=True)[0],
                "r_start": asof(e, fx, day_before)[0],
                "r_end_idx": asof(e, fx, fy_end, "index_year")[0],
                "r_end_2019": r_19, "r_end_2019_bound": "eligible" if bound_pass(r_19, t_19) else r_19,
                "r_now_cz": cn_reason(B.get(CZ_PARENT), seg[CZ_PARENT], cn_filing_test(pfl, "tax_year"), "national") if cz else r_now,
                "r_end_cz": asof_reason(CZ_PARENT, fy_end) if cz else r_end,
                "presumed_listed": presumed, "pub78_now": e in pub}

    units = tuple(map(evaluate, lines))

    # self-check: the current-status reading reproduces the parent's central share (0.768507)
    tot = sum(u["dw"] for u in units)
    now_share = sum(u["dw"] for u in units if is_ok(u["r_now"])) / tot

    variants = (("current_status_parent_rules", "r_now", True),
                ("asof_fy_end_current_bmf", "r_end_cur", True),
                ("asof_fy_end_reconstructed", "r_end", True),
                ("asof_fy_start_reconstructed", "r_start", True),
                ("asof_fy_end_reconstructed_plus_ruling_date_rule", "r_end_ruling", False),
                ("asof_fy_end_reconstructed_index_year_window", "r_end_idx", False),
                ("asof_fy_end_reconstructed_index_2019_on_only", "r_end_2019", False),
                ("asof_fy_end_reconstructed_index_2019_on_plus_gap_bound", "r_end_2019_bound", False),
                ("current_status_cz_lookthrough", "r_now_cz", False),
                ("asof_fy_end_reconstructed_cz_lookthrough", "r_end_cz", False))
    scopes = (("all", "all_recipients", lambda u: True),
              ("grant_fy", "fy2023", lambda u: u["fy"] == 2023),
              ("grant_fy", "fy2024", lambda u: u["fy"] == 2024))
    share = [r for v, rk, cats in variants for st, sc, p in scopes for r in share_rows(units, v, rk, st, sc, p, cats)]
    trans = (transition_rows(units, "r_now", "r_end", "current_status -> asof_fy_end_reconstructed")
             + transition_rows(units, "r_now", "r_start", "current_status -> asof_fy_start_reconstructed"))
    by_cut = _group_by_fast(units, lambda u: (u["sponsor"], u["fy"], u["tpe"]))
    cut_rows = [{"row_type": "sponsor_year_cutoff", "variant": "asof_fy_end_reconstructed", "scope_type": "sponsor_year",
                 "scope": f"{k[0]}:FY{k[1]}", "category": f"cutoff={k[2]}", "grant_units": len(v),
                 "recipients": len({u["key"] for u in v}), "usd_daf_weighted": round(sum(u["dw"] for u in v)),
                 "dollar_share_daf_weighted": (sum(u["dw"] for u in v if is_ok(u["r_end"])) / sum(u["dw"] for u in v))
                 if sum(u["dw"] for u in v) else None, "usd_sched_i": round(sum(u["si"] for u in v)), "source": SRC}
                for k, v in sorted(by_cut.items())]
    write_csv(a.out, share + trans + cut_rows,
              ("row_type", "variant", "scope_type", "scope", "category", "grant_units", "recipients", "grant_unit_share",
               "usd_daf_weighted", "dollar_share_daf_weighted", "usd_sched_i", "dollar_share_sched_i", "source"))

    name = lambda e: (bmf.get(e, {}).get("name") or "")[:45]  # noqa: E731
    agg = lambda us: {"dw": round(sum(u["dw"] for u in us)), "units": len(us), "recipients": len({u["key"] for u in us})}  # noqa: E731
    pick = lambda v, sc="all_recipients": next(r for r in share if r["variant"] == v and r["scope"] == sc and r["category"] == "eligible")  # noqa: E731
    lost = tuple(u for u in units if is_ok(u["r_now"]) and not is_ok(u["r_end"]))
    gained = tuple(u for u in units if not is_ok(u["r_now"]) and is_ok(u["r_end"]))
    top = lambda us: [{"ein": k, "name": name(k), "dw": round(sum(u["dw"] for u in v)),  # noqa: E731
                       "now": v[0]["r_now"], "asof": sorted({u["r_end"] for u in v}),
                       "fys": sorted({u["fy"] for u in v}), "tpe": sorted({u["tpe"] for u in v})}
                      for k, v in sorted(_group_by_fast(us, lambda u: u["key"]).items(), key=lambda kv: -sum(u["dw"] for u in kv[1]))[:15]]
    cz_units = tuple(u for u in units if u["key"] in CZ_LLCS)
    pfl = hist_x.get(CZ_PARENT, ())
    out = {
        "units": len(units), "recipients": len({u["key"] for u in units}), "total_dw": round(tot),
        "total_dw_by_fy": {fy: round(sum(u["dw"] for u in v)) for fy, v in _group_by_fast(units, lambda u: u["fy"]).items()},
        "self_check_current_share": now_share,
        "eligible_share": {v: {sc: round(pick(v, sc)["dollar_share_daf_weighted"], 6) for _, sc, _ in scopes} for v, _, _ in variants},
        "eligible_usd": {v: pick(v)["usd_daf_weighted"] for v, _, _ in variants},
        "cutoff_ends": {k: round(sum(u["dw"] for u in v)) for k, v in sorted(_group_by_fast(units, lambda u: u["tpe"]).items())},
        "lost_eligible_now_not_asof_end": agg(lost),
        "lost_by_asof_reason": {k: agg(v) for k, v in _group_by_fast(lost, lambda u: u["r_end"]).items()},
        "gained_asof_not_now": agg(gained),
        "gained_by_now_reason": {k: agg(v) for k, v in _group_by_fast(gained, lambda u: u["r_now"]).items()},
        "gained_presumed_listed": agg(tuple(u for u in gained if u["presumed_listed"])),
        "gained_presumed_listed_in_pub78_now": sum(1 for u in gained if u["presumed_listed"] and u["pub78_now"]),
        "top_lost": top(lost), "top_gained": top(gained),
        "start_minus_end_lost": agg(tuple(u for u in units if is_ok(u["r_end"]) and not is_ok(u["r_start"]))),
        "early_index_added_vs_2019_on": agg(tuple(u for u in units if is_ok(u["r_end"]) and not is_ok(u["r_end_2019"]))),
        "early_index_removed_vs_2019_on": agg(tuple(u for u in units if not is_ok(u["r_end"]) and is_ok(u["r_end_2019"]))),
        "early_rows": sum(len(v) for v in early.values()),
        "ruling_rule_underlying_reason": {k: agg(v) for k, v in _group_by_fast(
            tuple(u for u in units if u["r_end_ruling"] == "not_yet_recognised_at_cutoff"), lambda u: u["r_end"]).items()},
        "ruling_rule_top": [{"ein": k, "name": name(k), "ruling": B[k].get("ruling"), "dw": round(sum(u["dw"] for u in v)),
                             "now": v[0]["r_now"], "underlying": sorted({u["r_end"] for u in v}),
                             "tpe": sorted({u["tpe"] for u in v}),
                             "rev": [(str(r["rev_date"]), str(r["reinst_date"])) for r in rev.get(k, ())]}
                            for k, v in sorted(_group_by_fast(tuple(u for u in units if u["r_end_ruling"] == "not_yet_recognised_at_cutoff"),
                                                              lambda u: u["key"]).items(), key=lambda kv: -sum(u["dw"] for u in kv[1]))[:15]],
        "revoked_rule": agg(tuple(u for u in units if u["r_end"] == "revoked_at_cutoff_later_reinstated")),
        "presumed_listed_all": agg(tuple(u for u in units if u["presumed_listed"])),
        "cz": {"parent_in_bmf": B.get(CZ_PARENT, {}).get("name"), "parent_foundation": B.get(CZ_PARENT, {}).get("foundation"),
               "parent_ruling": B.get(CZ_PARENT, {}).get("ruling"), "parent_in_pub78": CZ_PARENT in pub,
               "parent_filings": [(p["tax_period"], p["form"], str(proc_date(p["oid"]))) for p in sorted(per_period(pfl), key=lambda p: p["tax_period"])],
               "llc_filings": {e: [(r["tax_period"], r["form"], str(proc_date(r["oid"]))) for r in hist_x.get(e, ())] for e in CZ_LLCS},
               "llc_revocation_rows": {e: len(rev.get(e, ())) for e in CZ_LLCS},
               "units": [{"ein": u["key"], "sponsor": u["sponsor"], "fy": u["fy"], "tpe": u["tpe"], "dw": round(u["dw"]),
                          "r_now": u["r_now"], "r_end": u["r_end"], "r_now_cz": u["r_now_cz"], "r_end_cz": u["r_end_cz"]} for u in cz_units],
               "parent_test_at_cutoffs": {u["tpe"]: asof_test(pfl, fy_bounds(u["tpe"])[1]) for u in cz_units}},
        "reasons_asof_end": {k: agg(v) for k, v in sorted(_group_by_fast(units, lambda u: u["r_end"]).items(), key=lambda kv: -sum(u["dw"] for u in kv[1]))},
        "reasons_now": {k: agg(v) for k, v in sorted(_group_by_fast(units, lambda u: u["r_now"]).items(), key=lambda kv: -sum(u["dw"] for u in kv[1]))},
    }
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
