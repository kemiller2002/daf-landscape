#!/usr/bin/env python3
"""Operating cost per DAF dollar and per DAF account in the long tail (< $50m), vs the top 50 (queue item P-B45N33-02).

Stdlib only; functional style (pure transforms, I/O at the edges). Nothing is fetched.

Inputs (repository, read only)
  * data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv  universe: 1,240 FY2024 sponsors under $50m of corrected
    DAF assets + the top 50; corrected FY2024 DAF assets, grants, screened accounts, DAFRC type (P-NEW-TAIL-01)
  * data/mission-2026-11-14/sponsor-cost-structure.csv  full Part IX by return, FY2022-25 (P-99F-04). Built by
    scripts/mission_sponsor_cost_structure.py from the GivingTuesday mirror of IRS e-file XML. The Schedule D harvest
    (form990-returns-schedule-d-harvest-full.csv) carries only Part IX lines 11a, 11f, 11g and 14 and no line 25 or
    employee count, so it cannot be used alone.

Definitions
  * opex = Part IX line 25(A) - lines 1-3 (grants) - line 4 - line 11f (investment-management fees)  [F/C]
    (identical to `operating_cost_ex_invest_mgmt` in sponsor-cost-structure.csv)
  * Whole-organisation ratios (no allocation) [C]: opex / DAF accounts, opex / DAF assets. These are upper bounds on what
    DAF administration can cost, because they load every non-DAF activity onto the DAFs.
  * Allocation rules [I] (labelled in every output column name with `_alloc_`):
      A (assets):  DAF cost = opex x min(1, DAF assets EOY / total assets EOY)
      G (grants):  DAF cost = opex x min(1, DAF grants / Part IX grants, lines 1-3)
      AM (admin-only floor): DAF cost = Part IX line 25 column C (management and general) x the rule-A share. It drops
           program-service cost (e.g. running a library or a hospital), which matters for single-issue sponsors; it
           understates CFs, which book grantmaking and donor services in column B. Column C can include part of 11f.
    Per account = allocated cost / screened DAF accounts; per DAF dollar = allocated cost / DAF assets EOY (in bps).
  * Usable: FY2024 return in the cost file, line 25 present, opex > 0, opex >= 1 bp of DAF assets (below that the cost sits
    outside Part IX, e.g. at an affiliated bank), not Givinga / BNY Mellon CGF (structural outliers, P-NEW-TAIL-01).
    DAF assets and grants are used only where not DAFRC-imputed; accounts only where `accounts_fy2024_screened` is set.
  * Duplicate returns for one EIN-FY (15 cases in the cost file): the one with the latest return timestamp is used.

Usage
  python3 scripts/mission_long_tail_cost.py .
Outputs
  data/mission-2026-11-14/long-tail-operating-cost-2026-11-19.csv  one row per sponsor (tail + top 50)
  stdout: markdown summary tables used in research/mission-2026-11-14/b45n33-long-tail-operating-cost.md
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys
from functools import reduce
from typing import Callable, Iterable, Mapping, Sequence

LT_CSV = "data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv"
COST_CSV = "data/mission-2026-11-14/sponsor-cost-structure.csv"
OUT_CSV = "data/mission-2026-11-14/long-tail-operating-cost-2026-11-19.csv"
STRUCTURAL = frozenset({"300748315", "474172718"})  # BNY Mellon CGF (terminated Dec 2024), Givinga (undefined account unit)
TAIL_BANDS = ("t10_50", "t1_10", "t0_1", "zero")
SI_CATS = ("single_issue_other", "religious", "university_or_hospital")
NAT_CATS = ("national_standard", "donation_processor")
YEARS = (2022, 2023, 2024, 2025)


# ----------------------------------------------------------------------------- pure helpers
def num(x) -> float | None:
    try:
        v = float(str(x).replace(",", "").strip())
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def div(a, b) -> float | None:
    return a / b if a is not None and b not in (None, 0) else None


def mul(a, b) -> float | None:
    return a * b if a is not None and b is not None else None


def clip01(x) -> float | None:
    return None if x is None else max(0.0, min(1.0, x))


def bps(a, b) -> float | None:
    v = div(a, b)
    return None if v is None else v * 1e4


def quantile(xs: Sequence[float], q: float) -> float | None:
    s = sorted(xs)
    if not s:
        return None
    pos = (len(s) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def group_by(items: Iterable, key: Callable) -> dict:
    return reduce(lambda acc, it: {**acc, key(it): acc.get(key(it), ()) + (it,)}, items, {})


def latest_return(rows: Sequence[Mapping]) -> Mapping:
    return max(rows, key=lambda r: (r.get("return_ts") or "", r.get("return_object_id") or ""))


def implausible_accounts(n, v) -> bool:
    """League-table screen: > 1,000 accounts averaging < $5 is not a donor-account count."""
    return n is not None and n > 1000 and (v is None or v / n < 5)


# ----------------------------------------------------------------------------- I/O edges
def read_csv(root: str, rel: str) -> list[dict]:
    with open(os.path.join(root, rel), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(root: str, rel: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(os.path.join(root, rel), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows([{k: fmt(r.get(k)) for k in fields} for r in rows])


def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, float):
        return f"{v:.6g}" if abs(v) < 1e6 else f"{v:.0f}"
    return str(v)


# ----------------------------------------------------------------------------- sponsor rows
def group_of(r: Mapping) -> str:
    tail = r["size_band_fy2024"] in TAIL_BANDS
    cat = r["sponsor_category"]
    kind = "cf" if cat == "community_foundation" else "si" if cat in SI_CATS else "national" if cat in NAT_CATS else "other"
    return ("tail_" if tail else "top50_") + kind


def cost_index(cost: Sequence[Mapping]) -> dict:
    by = group_by(cost, lambda r: (r["ein"], int(r["fiscal_year"])))
    return {k: latest_return(v) for k, v in by.items()}


def sponsor_row(s: Mapping, c: Mapping | None) -> dict:
    imputed = set(filter(None, (s.get("imputed_kept_fy2024") or "").split(";")))
    daf_a = num(s["daf_assets_fy2024"]) if "daf_assets_eoy" not in imputed else None
    daf_a = daf_a if daf_a is not None and daf_a > 0 else None
    daf_g = num(s["daf_grants_fy2024"]) if "daf_grants" not in imputed else None
    acc = num(s["accounts_fy2024_screened"])
    acc = acc if acc is not None and acc > 0 else None
    c = c or {}
    tfe = num(c.get("total_functional_expenses"))
    opex = num(c.get("operating_cost_ex_invest_mgmt"))
    ta = num(c.get("total_assets_eoy"))
    p9_grants = num(c.get("grants_part_ix_l1_3"))
    emp = num(c.get("employees"))
    share_a_raw = div(daf_a, ta) if ta and ta > 0 else None
    share_g_raw = div(daf_g, p9_grants) if p9_grants and p9_grants > 0 else None
    share_a, share_g = clip01(share_a_raw), clip01(share_g_raw)
    alloc_a, alloc_g = mul(opex, share_a), mul(opex, share_g)
    mg = num(c.get("mgmt_col_total"))
    alloc_am = mul(mg, share_a)
    reasons = tuple(f for f, cond in (
        ("structural_outlier", s["ein"] in STRUCTURAL),
        ("no_fy2024_return_in_cost_file", not c),
        ("line25_missing", bool(c) and tfe is None),
        ("opex_nonpositive", bool(c) and (opex is None or opex <= 0)),
        ("opex_lt_1bp_daf_assets", opex is not None and opex > 0 and daf_a is not None and opex / daf_a < 1e-4),
    ) if cond)
    ok = not reasons
    flags = tuple(f for f, cond in (
        ("daf_assets_imputed_or_nonpositive", daf_a is None),
        ("daf_grants_imputed", "daf_grants" in imputed),
        ("accounts_unscreened_or_imputed", acc is None),
        ("daf_assets_gt_total_assets_clipped", share_a_raw is not None and share_a_raw > 1.0001),
        ("daf_grants_gt_part_ix_grants_clipped", share_g_raw is not None and share_g_raw > 1.0001),
        ("employees_zero", emp == 0),
    ) if cond)
    g = lambda v: v if ok else None  # noqa: E731  metrics are blanked for unusable sponsors
    return {
        "ein": s["ein"], "name": s["name"], "group": group_of(s), "sponsor_category": s["sponsor_category"],
        "size_band_fy2024": s["size_band_fy2024"], "fy2024_rank_assets": s["fy2024_rank_assets"],
        "daf_assets_fy2024": daf_a, "daf_grants_fy2024": daf_g, "daf_accounts_fy2024_screened": acc,
        "return_object_id": c.get("return_object_id"), "tax_period": c.get("tax_period"),
        "total_functional_expenses": tfe, "part_ix_grants_l1_3": p9_grants,
        "opex_ex_11f": opex, "staff_cost_l5_10": num(c.get("staff_cost_l5_10")),
        "fees_mgmt_l11a": num(c.get("fees_mgmt_l11a")), "fees_other_l11g": num(c.get("fees_other_l11g")),
        "it_l14": num(c.get("it_l14")), "employees": emp, "total_assets_eoy": ta,
        "usable": ok, "exclusion_reason": ";".join(reasons), "data_flags": ";".join(flags),
        "daf_share_assets": g(share_a), "daf_share_grants": g(share_g),
        "opex_bps_total_assets": g(bps(opex, ta)),
        "opex_per_account_whole_org": g(div(opex, acc)),
        "opex_bps_daf_assets_whole_org": g(bps(opex, daf_a)),
        "daf_cost_alloc_A": g(alloc_a), "daf_cost_alloc_G": g(alloc_g), "mgmt_col_l25c": mg,
        "daf_cost_alloc_AM": g(alloc_am), "daf_cost_per_account_alloc_AM": g(div(alloc_am, acc)),
        "daf_cost_bps_daf_assets_alloc_AM": g(bps(alloc_am, daf_a)),
        "daf_cost_per_account_alloc_A": g(div(alloc_a, acc)),
        "daf_cost_per_account_alloc_G": g(div(alloc_g, acc)),
        "daf_cost_bps_daf_assets_alloc_A": g(bps(alloc_a, daf_a)),
        "daf_cost_bps_daf_assets_alloc_G": g(bps(alloc_g, daf_a)),
        "daf_cost_cents_per_grant_dollar_alloc_G": g(None if div(alloc_g, daf_g) is None or not daf_g or daf_g <= 0
                                                     else 100 * alloc_g / daf_g),
        "it_share_opex": g(div(num(c.get("it_l14")), opex)),
        "staff_share_opex": g(div(num(c.get("staff_cost_l5_10")), opex)),
        "fees_11a_11g_share_opex": g(div((num(c.get("fees_mgmt_l11a")) or 0) + (num(c.get("fees_other_l11g")) or 0), opex)),
        "it_per_account_alloc_A": g(div(mul(num(c.get("it_l14")), share_a), acc)),
        "accounts_per_employee": g(div(acc, emp) if emp and emp > 0 else None),
        "daf_fte_alloc_A": g(mul(emp, share_a)),
        "accounts_per_daf_fte_alloc_A": g(div(acc, mul(emp, share_a)) if emp and emp > 0 and share_a else None),
    }


SPONSOR_FIELDS = ("ein", "name", "group", "sponsor_category", "size_band_fy2024", "fy2024_rank_assets",
                  "daf_assets_fy2024", "daf_grants_fy2024", "daf_accounts_fy2024_screened", "return_object_id",
                  "tax_period", "total_functional_expenses", "part_ix_grants_l1_3", "opex_ex_11f", "staff_cost_l5_10",
                  "fees_mgmt_l11a", "fees_other_l11g", "it_l14", "employees", "total_assets_eoy", "mgmt_col_l25c", "usable",
                  "exclusion_reason", "data_flags", "daf_share_assets", "daf_share_grants", "opex_bps_total_assets",
                  "opex_per_account_whole_org", "opex_bps_daf_assets_whole_org", "daf_cost_alloc_A", "daf_cost_alloc_G", "daf_cost_alloc_AM",
                  "daf_cost_per_account_alloc_AM", "daf_cost_bps_daf_assets_alloc_AM",
                  "daf_cost_per_account_alloc_A", "daf_cost_per_account_alloc_G", "daf_cost_bps_daf_assets_alloc_A",
                  "daf_cost_bps_daf_assets_alloc_G", "daf_cost_cents_per_grant_dollar_alloc_G", "it_share_opex",
                  "staff_share_opex", "fees_11a_11g_share_opex", "it_per_account_alloc_A", "accounts_per_employee",
                  "daf_fte_alloc_A", "accounts_per_daf_fte_alloc_A")


# ----------------------------------------------------------------------------- statistics
def describe(rows: Sequence[Mapping], k: str) -> dict:
    xs = tuple(v for v in (r.get(k) for r in rows) if v is not None)
    return {"n": len(xs), "p25": quantile(xs, .25), "median": quantile(xs, .5), "p75": quantile(xs, .75)}


def pooled(rows: Sequence[Mapping], num_k: str, den_k: str, scale: float = 1) -> float | None:
    both = tuple(r for r in rows if r.get(num_k) is not None and r.get(den_k))
    v = div(sum(r[num_k] for r in both), sum(r[den_k] for r in both))
    return None if v is None else v * scale


STAT_KEYS = ("daf_share_assets", "daf_share_grants", "opex_ex_11f", "employees", "opex_bps_total_assets",
             "opex_per_account_whole_org", "opex_bps_daf_assets_whole_org", "daf_cost_per_account_alloc_A",
             "daf_cost_per_account_alloc_G", "daf_cost_bps_daf_assets_alloc_A", "daf_cost_bps_daf_assets_alloc_G",
             "daf_cost_per_account_alloc_AM", "daf_cost_bps_daf_assets_alloc_AM", "daf_cost_cents_per_grant_dollar_alloc_G", "it_l14", "it_share_opex", "staff_share_opex",
             "fees_11a_11g_share_opex", "it_per_account_alloc_A", "accounts_per_employee", "daf_fte_alloc_A",
             "accounts_per_daf_fte_alloc_A", "daf_accounts_fy2024_screened", "daf_assets_fy2024")


def group_stats(rows: Sequence[Mapping]) -> dict:
    use = tuple(r for r in rows if r["usable"])
    acc_rows = tuple({**r, "_acc": r["daf_accounts_fy2024_screened"]} for r in use)
    return {"sponsors": len(rows), "usable": len(use),
            "excluded": {k: len(v) for k, v in group_by(tuple(r for r in rows if not r["usable"]),
                                                     lambda r: r["exclusion_reason"]).items()},
            **{k: describe(use, k) for k in STAT_KEYS},
            "pooled_per_account_A": pooled(acc_rows, "daf_cost_alloc_A", "_acc"),
            "pooled_per_account_G": pooled(acc_rows, "daf_cost_alloc_G", "_acc"),
            "pooled_bps_A": pooled(use, "daf_cost_alloc_A", "daf_assets_fy2024", 1e4),
            "pooled_bps_G": pooled(use, "daf_cost_alloc_G", "daf_assets_fy2024", 1e4),
            "share_le_100bps_A": share_le(use, "daf_cost_bps_daf_assets_alloc_A", 100),
            "share_le_100bps_G": share_le(use, "daf_cost_bps_daf_assets_alloc_G", 100),
            "avg_account": describe(tuple({"v": div(r["daf_assets_fy2024"], r["daf_accounts_fy2024_screened"])} for r in use), "v")}


def share_le(rows: Sequence[Mapping], k: str, cut: float) -> dict:
    """Share of sponsors whose allocated cost is at or below `cut` bps: the 100 bps CF census median fee (hypothetical)."""
    xs = tuple(r[k] for r in rows if r.get(k) is not None)
    return {"n": len(xs), "share": div(sum(x <= cut for x in xs), len(xs))}


def segments(rows: Sequence[Mapping]) -> dict:
    sel = lambda f: tuple(r for r in rows if f(r))  # noqa: E731
    tail = lambda r: r["size_band_fy2024"] in TAIL_BANDS  # noqa: E731
    defs = {
        "tail_all": lambda r: tail(r),
        "tail_cf": lambda r: r["group"] == "tail_cf",
        "tail_cf_10_50m": lambda r: r["group"] == "tail_cf" and r["size_band_fy2024"] == "t10_50",
        "tail_cf_1_10m": lambda r: r["group"] == "tail_cf" and r["size_band_fy2024"] == "t1_10",
        "tail_cf_lt1m": lambda r: r["group"] == "tail_cf" and r["size_band_fy2024"] in ("t0_1", "zero"),
        "tail_si": lambda r: r["group"] == "tail_si",
        "tail_si_ex_univ": lambda r: tail(r) and r["sponsor_category"] in ("single_issue_other", "religious"),
        "tail_si_other": lambda r: tail(r) and r["sponsor_category"] == "single_issue_other",
        "tail_si_religious": lambda r: tail(r) and r["sponsor_category"] == "religious",
        "tail_si_univ_hosp": lambda r: tail(r) and r["sponsor_category"] == "university_or_hospital",
        "tail_si_10_50m": lambda r: r["group"] == "tail_si" and r["size_band_fy2024"] == "t10_50",
        "tail_si_1_10m": lambda r: r["group"] == "tail_si" and r["size_band_fy2024"] == "t1_10",
        "tail_si_lt1m": lambda r: r["group"] == "tail_si" and r["size_band_fy2024"] in ("t0_1", "zero"),
        "tail_national": lambda r: r["group"] == "tail_national",
        "top50_all": lambda r: r["size_band_fy2024"] == "top50",
        "top50_national": lambda r: r["group"] == "top50_national",
        "top50_cf": lambda r: r["group"] == "top50_cf",
        "top50_si": lambda r: r["group"] == "top50_si",
    }
    return {k: group_stats(sel(f)) for k, f in defs.items()}


# ----------------------------------------------------------------------------- FY2022-25 robustness (Schedule D values)
def year_metrics(c: Mapping) -> dict | None:
    opex, ta = num(c.get("operating_cost_ex_invest_mgmt")), num(c.get("total_assets_eoy"))
    v, n = num(c.get("daf_assets_eoy")), num(c.get("daf_accounts"))
    if opex is None or opex <= 0 or not v or v <= 0 or c["ein"] in STRUCTURAL or opex / v < 1e-4:
        return None
    n = None if not n or n <= 0 or implausible_accounts(n, v) else n
    a = clip01(div(v, ta)) if ta and ta > 0 else None
    alloc = mul(opex, a)
    return {"per_account_A": div(alloc, n), "bps_A": bps(alloc, v), "per_account_whole": div(opex, n)}


def by_year(cost_idx: Mapping, rows: Sequence[Mapping]) -> dict:
    groups = ("tail_cf", "tail_si", "top50_cf", "top50_all")
    member = lambda r, g: r["size_band_fy2024"] == "top50" if g == "top50_all" else r["group"] == g  # noqa: E731
    eins = lambda g: tuple(r["ein"] for r in rows if member(r, g))  # noqa: E731
    metrics = lambda g, y: tuple(filter(None, (year_metrics(cost_idx[(e, y)]) for e in eins(g) if (e, y) in cost_idx)))  # noqa: E731
    return {g: {y: {k: describe(metrics(g, y), k) for k in ("per_account_A", "bps_A", "per_account_whole")} for y in YEARS}
            for g in groups}


# ----------------------------------------------------------------------------- markdown rendering
def m(v, kind="n") -> str:
    if v is None:
        return "–"
    return {"usd": f"${v:,.0f}", "bps": f"{v:,.0f}", "pct": f"{100 * v:.1f}%", "n": f"{v:,.1f}" if v < 100 else f"{v:,.0f}",
            "c": f"{v:.1f}"}[kind]


def miq(d: Mapping, kind: str) -> str:
    return f"{m(d['median'], kind)} ({m(d['p25'], kind)}–{m(d['p75'], kind)}; n={d['n']})"


def render(seg: Mapping, yrs: Mapping) -> str:
    order = ("tail_cf", "tail_cf_10_50m", "tail_cf_1_10m", "tail_cf_lt1m", "tail_si", "tail_si_ex_univ", "tail_si_other",
             "tail_si_religious", "tail_si_univ_hosp", "tail_si_10_50m", "tail_si_1_10m", "tail_si_lt1m",
             "tail_national", "tail_all", "top50_all", "top50_national", "top50_cf", "top50_si")
    t1 = ["| Segment | Sponsors | Usable | DAF share of assets | DAF share of grants | Opex (whole org) | Employees | Opex bps of total assets |",
          "|---|---|---|---|---|---|---|---|"] + [
        f"| {k} | {seg[k]['sponsors']} | {seg[k]['usable']} | {miq(seg[k]['daf_share_assets'], 'pct')} | "
        f"{miq(seg[k]['daf_share_grants'], 'pct')} | {miq(seg[k]['opex_ex_11f'], 'usd')} | {miq(seg[k]['employees'], 'n')} | "
        f"{miq(seg[k]['opex_bps_total_assets'], 'bps')} |" for k in order]
    t2 = ["| Segment | Whole-org opex per account [C] | Per account, rule A [I] | Per account, rule G [I] | Per account, rule AM [I] | Pooled per account A / G [I] |",
          "|---|---|---|---|---|---|"] + [
        f"| {k} | {miq(seg[k]['opex_per_account_whole_org'], 'usd')} | {miq(seg[k]['daf_cost_per_account_alloc_A'], 'usd')} | "
        f"{miq(seg[k]['daf_cost_per_account_alloc_G'], 'usd')} | {miq(seg[k]['daf_cost_per_account_alloc_AM'], 'usd')} | "
        f"{m(seg[k]['pooled_per_account_A'], 'usd')} / "
        f"{m(seg[k]['pooled_per_account_G'], 'usd')} |" for k in order]
    t3 = ["| Segment | Whole-org opex, bps of DAF assets [C] | Rule A, bps of DAF assets [I] | Rule G, bps of DAF assets [I] | Rule AM, bps [I] | Pooled bps A / G [I] | Rule G, cents per DAF grant dollar [I] |",
          "|---|---|---|---|---|---|---|"] + [
        f"| {k} | {miq(seg[k]['opex_bps_daf_assets_whole_org'], 'bps')} | {miq(seg[k]['daf_cost_bps_daf_assets_alloc_A'], 'bps')} | "
        f"{miq(seg[k]['daf_cost_bps_daf_assets_alloc_G'], 'bps')} | {miq(seg[k]['daf_cost_bps_daf_assets_alloc_AM'], 'bps')} | {m(seg[k]['pooled_bps_A'], 'bps')} / {m(seg[k]['pooled_bps_G'], 'bps')} | "
        f"{miq(seg[k]['daf_cost_cents_per_grant_dollar_alloc_G'], 'c')} |" for k in order]
    t4 = ["| Segment | IT line 14 ($) | IT share of opex | Staff share of opex | 11a+11g share of opex | IT per account, rule A [I] | Accounts per employee (whole org) | DAF FTE, rule A [I] | Accounts per DAF FTE, rule A [I] |",
          "|---|---|---|---|---|---|---|---|---|"] + [
        f"| {k} | {miq(seg[k]['it_l14'], 'usd')} | {miq(seg[k]['it_share_opex'], 'pct')} | {miq(seg[k]['staff_share_opex'], 'pct')} | "
        f"{miq(seg[k]['fees_11a_11g_share_opex'], 'pct')} | {miq(seg[k]['it_per_account_alloc_A'], 'usd')} | "
        f"{miq(seg[k]['accounts_per_employee'], 'n')} | {miq(seg[k]['daf_fte_alloc_A'], 'n')} | {miq(seg[k]['accounts_per_daf_fte_alloc_A'], 'n')} |"
        for k in order]
    t5 = ["| Group | FY | Whole-org per account [C] | Per account, rule A [I] | bps of DAF assets, rule A [I] |", "|---|---|---|---|---|"] + [
        f"| {g} | {y} | {miq(yrs[g][y]['per_account_whole'], 'usd')} | {miq(yrs[g][y]['per_account_A'], 'usd')} | {miq(yrs[g][y]['bps_A'], 'bps')} |"
        for g in yrs for y in YEARS]
    t6 = ["| Segment | Median average account (IQR; n) | Share with rule-A cost <= 100 bps [I] | Share with rule-G cost <= 100 bps [I] |",
          "|---|---|---|---|"] + [
        f"| {k} | {miq(seg[k]['avg_account'], 'usd')} | {m(seg[k]['share_le_100bps_A']['share'], 'pct')} (n={seg[k]['share_le_100bps_A']['n']}) | "
        f"{m(seg[k]['share_le_100bps_G']['share'], 'pct')} (n={seg[k]['share_le_100bps_G']['n']}) |" for k in order]
    excl = ["| Segment | Exclusions |", "|---|---|"] + [f"| {k} | {json.dumps(seg[k]['excluded'])} |" for k in order]
    return "\n\n".join("\n".join(t) for t in (t1, t2, t3, t4, t5, t6, excl))


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str]) -> int:
    root = argv[0] if argv else "."
    lt = read_csv(root, LT_CSV)
    universe = tuple(r for r in lt if r["size_band_fy2024"] in TAIL_BANDS + ("top50",))
    cidx = cost_index(read_csv(root, COST_CSV))
    rows = tuple(sponsor_row(s, cidx.get((s["ein"], 2024))) for s in universe)
    write_csv(root, OUT_CSV, rows, SPONSOR_FIELDS)
    seg = segments(rows)
    yrs = by_year(cidx, rows)
    print(render(seg, yrs))
    print("\n<!-- counts -->", json.dumps({"universe": len(universe),
                                          "tail": sum(r["size_band_fy2024"] in TAIL_BANDS for r in universe),
                                          "top50": sum(r["size_band_fy2024"] == "top50" for r in universe),
                                          "tail_flags": {k: len(v) for k, v in group_by(
                                              tuple(f for r in rows if r["size_band_fy2024"] in TAIL_BANDS and r["usable"]
                                                    for f in r["data_flags"].split(";") if f), lambda f: f).items()}}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
