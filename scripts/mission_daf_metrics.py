#!/usr/bin/env python3
"""Derived DAF market metrics for mission 2026-11-14 (stdlib only, functional style).

Inputs  (data/mission-2026-11-14/):
  daf-market-annual-series.csv, dafrc-sponsor-schedule-d-fy2019-2024.csv,
  sponsor-level-metrics.csv
Output:
  derived-metrics.csv

Computations (each output row carries its definition):
  A. YoY growth and CAGR per published series (never across publishers / vintages).
  B. Recomputation of DAFRC published totals from the sponsor-level dataset (check).
  C. Market payout: grants_t / assets_{t-1} (DAFRC & NPT convention) and
     grants_t / mean(assets_{t-1}, assets_t).
  D. Sponsor-level payout for named sponsors + cross-sponsor payout distribution.
  E. Named-sponsor share of DAFRC totals, with fiscal-year matching checks.
  F. CR1/CR3/CR5/CR10 and HHI of sponsor DAF assets (and grants, contributions,
     accounts) with coverage shares (all rows vs filed-only rows).
  G. Cross-source checks: DAFRC vs NPT for overlapping FYs; Schedule D vs
     ProPublica Form 990 totals.

Usage: python3 scripts/mission_daf_metrics.py [--data-dir DIR]
"""
from __future__ import annotations

import argparse
import csv
import io
import os
from collections import defaultdict
from functools import reduce
from statistics import median, quantiles
from typing import Callable, Iterable, Mapping, Sequence

OUT_FIELDS = (
    "metric_id", "computation", "entity", "ein", "fiscal_year", "value", "unit",
    "numerator", "denominator", "coverage_share", "check_status", "definition", "inputs",
)
DAFRC_FILE = "dafrc-sponsor-schedule-d-fy2019-2024.csv"
MARKET_FILE = "daf-market-annual-series.csv"
SPONSOR_FILE = "sponsor-level-metrics.csv"
DAFRC_FIELDS = {
    "daf_assets_eoy": "eoy_daf_assets",
    "daf_grants": "total_daf_grants",
    "daf_contributions": "total_daf_contributions",
    "daf_accounts_eoy": "number_of_daf_accounts",
}
PROVENANCE_FIELD = {
    "eoy_daf_assets": "source_eoy_daf_assets",
    "total_daf_grants": "source_total_daf_grants",
    "total_daf_contributions": "source_total_daf_contributions",
    "number_of_daf_accounts": "source_number_of_accounts",
}


# ---------------------------------------------------------------------------
# Generic pure helpers
# ---------------------------------------------------------------------------
def to_float(x) -> float | None:
    try:
        return float(x) if x not in (None, "") else None
    except ValueError:
        return None


def safe_div(n: float | None, d: float | None) -> float | None:
    return n / d if n is not None and d not in (None, 0) else None


def rnd(x: float | None, nd: int = 6):
    return "" if x is None else round(x, nd)


def group_by(items: Iterable, key: Callable) -> dict:
    """Pure from the caller's view; local accumulation keeps it O(n)."""
    acc: dict = defaultdict(list)
    for it in items:
        acc[key(it)].append(it)
    return {k: tuple(v) for k, v in acc.items()}


def row(**kw) -> dict:
    return {f: kw.get(f, "") for f in OUT_FIELDS}


def read_csv(path: str) -> tuple:
    with open(path, encoding="utf-8", newline="") as fh:
        return tuple(csv.DictReader(fh))


def to_csv(rows: Sequence[Mapping]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(OUT_FIELDS), quoting=csv.QUOTE_ALL, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def is_filed(provenance: str) -> bool:
    return provenance.strip().lower() in ("irs 990", "paper submission")


# ---------------------------------------------------------------------------
# A. YoY growth per published series
# ---------------------------------------------------------------------------
def yoy_rows(market: Sequence[Mapping]) -> tuple:
    """YoY within a series_id+metric (+edition for NPT revised/current pairs)."""
    def series_key(r):
        # NPT within-edition pairs: compare edition's current year vs its revised prior year.
        return (r["series_id"], r["metric"])

    out = []
    # A1: contiguous-year series (DAFRC_2025_UPDATED, NPT_DAFR_HEADLINE chained across editions)
    for (sid, metric), rs in group_by(
            (r for r in market if r["series_id"] in ("DAFRC_2025_UPDATED", "NPT_DAFR_HEADLINE")),
            series_key).items():
        by_year = {int(r["fiscal_year"]): r for r in rs}
        for y in sorted(by_year):
            prev = by_year.get(y - 1)
            if prev is None or metric.endswith("_pct"):
                continue
            cur_v, prev_v = to_float(by_year[y]["value"]), to_float(prev["value"])
            out.append(row(
                metric_id=f"YOY_{sid}_{metric}", computation="yoy_growth", entity=sid,
                fiscal_year=y, value=rnd(safe_div(cur_v - prev_v, prev_v) if None not in (cur_v, prev_v) else None),
                unit="ratio", numerator=cur_v, denominator=prev_v,
                check_status=("chained_across_editions_unrevised" if sid == "NPT_DAFR_HEADLINE" else "same_vintage"),
                definition="(value_t - value_{t-1}) / value_{t-1} within one series_id; NPT headline chain mixes editions (each year's first estimate) so prefer within-edition YoY",
                inputs=MARKET_FILE))
    # A2: NPT within-edition YoY (current vs revised prior from the same edition)
    npt_pairs = group_by((r for r in market if r["series_id"].startswith("NPT_DAFR_")),
                         lambda r: (r["report_edition"], r["metric"]))
    for (edition, metric), rs in npt_pairs.items():
        cur = next((r for r in rs if r["series_id"] == "NPT_DAFR_HEADLINE"), None)
        prv = next((r for r in rs if r["series_id"] == "NPT_DAFR_REVISED_PRIOR"), None)
        if not cur or not prv or metric.endswith("_pct"):
            continue
        c, p = to_float(cur["value"]), to_float(prv["value"])
        out.append(row(
            metric_id=f"YOY_NPT_WITHIN_EDITION_{metric}", computation="yoy_growth",
            entity=edition, fiscal_year=cur["fiscal_year"], value=rnd(safe_div(c - p, p)),
            unit="ratio", numerator=c, denominator=p, check_status="same_edition",
            definition="NPT edition current-year value vs the same edition's revised prior-year value",
            inputs=MARKET_FILE))
    return tuple(out)


def cagr_rows(market: Sequence[Mapping]) -> tuple:
    """Compound annual growth between first and last FY of a series (same series_id only)."""
    def one(sid, metric, rs):
        by_year = {int(r["fiscal_year"]): to_float(r["value"]) for r in rs}
        y0, y1 = min(by_year), max(by_year)
        v0, v1 = by_year[y0], by_year[y1]
        val = (v1 / v0) ** (1 / (y1 - y0)) - 1 if v0 and v1 and y1 > y0 else None
        return row(metric_id=f"CAGR_{sid}_{metric}", computation="cagr", entity=sid, fiscal_year=f"{y0}-{y1}",
                   value=rnd(val), unit="ratio per year", numerator=v1, denominator=v0,
                   check_status="chained_across_editions_unrevised" if sid == "NPT_DAFR_HEADLINE" else "same_vintage",
                   definition="(value_last / value_first)^(1/years) - 1 within one series_id", inputs=MARKET_FILE)
    groups = group_by((r for r in market if r["series_id"] in ("DAFRC_2025_UPDATED", "NPT_DAFR_HEADLINE")
                       and r["metric"] in ("grants", "contributions", "charitable_assets", "daf_accounts")),
                      lambda r: (r["series_id"], r["metric"]))
    return tuple(one(sid, m, rs) for (sid, m), rs in sorted(groups.items()))


# ---------------------------------------------------------------------------
# B. Recompute DAFRC totals from sponsor dataset
# ---------------------------------------------------------------------------
def dafrc_totals(dafrc: Sequence[Mapping]) -> dict:
    by_fy = group_by(dafrc, lambda r: int(r["fiscal_year_end"]))
    return {fy: {**{m: sum(to_float(r[f]) or 0.0 for r in rs) for m, f in DAFRC_FIELDS.items()},
                 "sponsors": len({r["ein"] for r in rs}),
                 **{f"filed_share_{m}": safe_div(
                     sum(to_float(r[f]) or 0.0 for r in rs if is_filed(r[PROVENANCE_FIELD[f]])),
                     sum(to_float(r[f]) or 0.0 for r in rs)) for m, f in DAFRC_FIELDS.items()}}
            for fy, rs in by_fy.items()}


def published_lookup(market: Sequence[Mapping], series_id: str) -> dict:
    return {(int(r["fiscal_year"]), r["metric"]): to_float(r["value"])
            for r in market if r["series_id"] == series_id}


def recompute_check_rows(totals: Mapping, published: Mapping) -> tuple:
    mapping = {"charitable_assets": "daf_assets_eoy", "grants": "daf_grants",
               "contributions": "daf_contributions", "daf_accounts": "daf_accounts_eoy",
               "sponsors": "sponsors"}

    def check(fy, pub_metric):
        pub = published.get((fy, pub_metric))
        calc = totals.get(fy, {}).get(mapping[pub_metric])
        if pub is None or calc is None:
            return None
        tol = 0.005 * pub if pub_metric not in ("daf_accounts", "sponsors") else 0.5
        return row(metric_id=f"CHECK_DAFRC_RECOMPUTE_{pub_metric}", computation="recompute_total",
                   entity="DAFRC_2025_UPDATED", fiscal_year=fy, value=calc,
                   unit="USD" if pub_metric not in ("daf_accounts", "sponsors") else "count",
                   numerator=calc, denominator=pub,
                   check_status="match" if abs(calc - pub) <= tol else "MISMATCH",
                   definition="Sum of sponsor rows in DAFRC dataset vs published (rounded) total; tolerance 0.5% for $ (rounding to $0.01b), exact for counts",
                   inputs=f"{DAFRC_FILE};{MARKET_FILE}")
    return tuple(r for r in (check(fy, m) for fy in sorted(totals) for m in mapping) if r)


def coverage_rows(totals: Mapping) -> tuple:
    return tuple(row(metric_id=f"DAFRC_FILED_COVERAGE_{m}", computation="coverage_share",
                     entity="DAFRC universe", fiscal_year=fy, value=rnd(t[f"filed_share_{m}"]),
                     unit="ratio", check_status="info",
                     definition="Share of the DAFRC total coming from rows whose provenance is 'IRS 990' or 'paper submission' (i.e. not Imputed / NPT historical)",
                     inputs=DAFRC_FILE)
                 for fy, t in sorted(totals.items()) for m in DAFRC_FIELDS)


# ---------------------------------------------------------------------------
# C. Market payout
# ---------------------------------------------------------------------------
def payout_pair(grants: float | None, prev_assets: float | None, cur_assets: float | None) -> tuple:
    beg = safe_div(grants, prev_assets)
    avg = safe_div(grants, (prev_assets + cur_assets) / 2) if None not in (prev_assets, cur_assets) else None
    return beg, avg


def market_payout_rows(totals: Mapping, npt_published: Mapping) -> tuple:
    dafrc = tuple(
        r for fy in sorted(totals) if fy - 1 in totals
        for beg, avg in [payout_pair(totals[fy]["daf_grants"], totals[fy - 1]["daf_assets_eoy"], totals[fy]["daf_assets_eoy"])]
        for r in (
            row(metric_id="PAYOUT_MARKET_BEGINNING_ASSETS", computation="payout_ratio", entity="DAFRC universe (recomputed)",
                fiscal_year=fy, value=rnd(beg), unit="ratio", numerator=totals[fy]["daf_grants"],
                denominator=totals[fy - 1]["daf_assets_eoy"], check_status="aggregate_not_account_level",
                definition="grants_t / end-of-year assets_{t-1} (DAFRC/NPT/Candid convention)", inputs=DAFRC_FILE),
            row(metric_id="PAYOUT_MARKET_AVERAGE_ASSETS", computation="payout_ratio", entity="DAFRC universe (recomputed)",
                fiscal_year=fy, value=rnd(avg), unit="ratio", numerator=totals[fy]["daf_grants"],
                denominator=(totals[fy - 1]["daf_assets_eoy"] + totals[fy]["daf_assets_eoy"]) / 2,
                check_status="aggregate_not_account_level",
                definition="grants_t / mean(assets_{t-1}, assets_t)", inputs=DAFRC_FILE),
        ))
    # NPT revised-prior assets give a consistent denominator within each edition
    npt = tuple(
        row(metric_id="PAYOUT_NPT_RECOMPUTED_BEGINNING_ASSETS", computation="payout_ratio",
            entity="NPT edition (current grants / same-edition revised prior assets)", fiscal_year=fy,
            value=rnd(safe_div(g, a)), unit="ratio", numerator=g, denominator=a,
            check_status="compare_to_published_payout_rate_pct",
            definition="grants_t / revised assets_{t-1}, both from the same NPT edition", inputs=MARKET_FILE)
        for (fy, g, a) in npt_published)
    return dafrc + npt


def npt_payout_inputs(market: Sequence[Mapping]) -> tuple:
    by_ed = group_by((r for r in market if r["series_id"].startswith("NPT_DAFR_")), lambda r: r["report_edition"])

    def pick(rs, sid, metric):
        return next((r for r in rs if r["series_id"] == sid and r["metric"] == metric), None)
    return tuple((int(g["fiscal_year"]), to_float(g["value"]), to_float(a["value"]))
                 for rs in by_ed.values()
                 for g, a in [(pick(rs, "NPT_DAFR_HEADLINE", "grants"), pick(rs, "NPT_DAFR_REVISED_PRIOR", "charitable_assets"))]
                 if g and a)


# ---------------------------------------------------------------------------
# D. Sponsor payout (named + distribution)
# ---------------------------------------------------------------------------
def sponsor_year_index(dafrc: Sequence[Mapping]) -> dict:
    return {(r["ein"], int(r["fiscal_year_end"])): r for r in dafrc}


def named_eins(sponsor_rows: Sequence[Mapping]) -> dict:
    return {r["ein"]: r["sponsor"] for r in sponsor_rows if r["data_source_type"] == "dafrc_schedule_d_dataset"}


def sponsor_payout_rows(idx: Mapping, names: Mapping) -> tuple:
    def one(ein, fy):
        cur, prev = idx.get((ein, fy)), idx.get((ein, fy - 1))
        if not cur or not prev:
            return None
        g, a0, a1 = (to_float(cur["total_daf_grants"]), to_float(prev["eoy_daf_assets"]), to_float(cur["eoy_daf_assets"]))
        beg, avg = payout_pair(g, a0, a1)
        flags = ";".join(f for f in (
            "imputed_current" if not is_filed(cur["source_total_daf_grants"]) else "",
            "imputed_prior_assets" if not is_filed(prev["source_eoy_daf_assets"]) else "") if f)
        return row(metric_id="PAYOUT_SPONSOR_BEGINNING_ASSETS", computation="payout_ratio", entity=names[ein], ein=ein,
                   fiscal_year=fy, value=rnd(beg), unit="ratio", numerator=g, denominator=a0,
                   coverage_share=rnd(avg), check_status=flags or "filed",
                   definition="Sponsor-level DAF grants_t / DAF assets_{t-1} (Schedule D); coverage_share column holds the average-assets variant grants_t/mean(assets_{t-1},assets_t)",
                   inputs=DAFRC_FILE)
    return tuple(r for r in (one(e, fy) for e in sorted(names) for fy in range(2020, 2025)) if r)


def payout_distribution_rows(dafrc: Sequence[Mapping], idx: Mapping) -> tuple:
    def ratios(fy, min_assets):
        return sorted(
            g / a for r in dafrc if int(r["fiscal_year_end"]) == fy and is_filed(r["source_total_daf_grants"])
            for prev in [idx.get((r["ein"], fy - 1))]
            if prev and is_filed(prev["source_eoy_daf_assets"])
            for g, a in [(to_float(r["total_daf_grants"]), to_float(prev["eoy_daf_assets"]))]
            if g is not None and a is not None and a >= min_assets)

    def stats(fy, min_assets, label):
        xs = ratios(fy, min_assets)
        if len(xs) < 4:
            return ()
        q = quantiles(xs, n=4)
        base = dict(computation="payout_distribution_across_sponsors", entity=label, fiscal_year=fy, unit="ratio",
                    denominator=len(xs), check_status="sponsor_level_not_account_level", inputs=DAFRC_FILE,
                    definition=f"Distribution of sponsor-level grants_t/assets_(t-1) across sponsors with filed (non-imputed) values and prior assets >= ${min_assets:,.0f}; denominator = n sponsors")
        return (row(metric_id="PAYOUT_SPONSOR_P25", value=rnd(q[0]), **base),
                row(metric_id="PAYOUT_SPONSOR_MEDIAN", value=rnd(median(xs)), **base),
                row(metric_id="PAYOUT_SPONSOR_P75", value=rnd(q[2]), **base),
                row(metric_id="PAYOUT_SPONSOR_SHARE_BELOW_5PCT", value=rnd(sum(x < 0.05 for x in xs) / len(xs)), **base))
    return tuple(r for fy in range(2020, 2025) for (m, lab) in ((1e6, "sponsors with prior DAF assets >= $1m"), (1e9, "sponsors with prior DAF assets >= $1bn"))
                 for r in stats(fy, m, lab))


# ---------------------------------------------------------------------------
# E. Sponsor share of DAFRC totals with fiscal-year matching
# ---------------------------------------------------------------------------
def share_rows(sponsor_rows: Sequence[Mapping], totals: Mapping) -> tuple:
    def year_status(r):
        fy = int(r["fiscal_year"])
        if fy not in totals:
            return "year_mismatch_no_DAFRC_total_for_FY"
        pe = r["period_end"][:4]
        if r["data_source_type"] == "dafrc_schedule_d_dataset":
            if r["value_provenance"].lower() == "imputed":
                return "matched_FY_but_value_imputed"
            return "matched" if pe in ("", str(fy)) else "matched_FY_label_period_end_lags"
        if r["period_basis"].startswith("calendar_year") or r["period_basis"].startswith("point_in_time"):
            return "period_definition_mismatch_calendar_vs_990_FY"
        return "matched_FY_label_different_source"

    eligible = tuple(r for r in sponsor_rows if r["metric"] in DAFRC_FIELDS and r["value"] != "")

    def one(r):
        fy, status = int(r["fiscal_year"]), year_status(r)
        total = totals.get(fy, {}).get(r["metric"])
        ok = status.startswith("matched")
        return row(metric_id=f"SHARE_OF_DAFRC_{r['metric']}", computation="sponsor_share_of_market",
                   entity=r["sponsor"], ein=r["ein"], fiscal_year=fy,
                   value=rnd(safe_div(to_float(r["value"]), total)) if ok else "",
                   unit="ratio", numerator=r["value"], denominator=total if total else "",
                   check_status=f"{status};source={r['data_source_type']}",
                   definition="Sponsor value / DAFRC updated total for the same DAFRC FY label; blank when periods do not match (calendar-year or post-FY2024 self-reports)",
                   inputs=f"{SPONSOR_FILE};{DAFRC_FILE}")
    return tuple(map(one, eligible))


# ---------------------------------------------------------------------------
# F. Concentration
# ---------------------------------------------------------------------------
def concentration(values: Sequence[float]) -> dict:
    xs = sorted((v for v in values if v and v > 0), reverse=True)
    tot = sum(xs)
    shares = tuple(v / tot for v in xs) if tot else ()
    return {"total": tot, "n": len(xs), "CR1": sum(shares[:1]), "CR3": sum(shares[:3]),
            "CR5": sum(shares[:5]), "CR10": sum(shares[:10]),
            "HHI": sum((s * 100) ** 2 for s in shares)}


def concentration_rows(dafrc: Sequence[Mapping], totals: Mapping) -> tuple:
    def rows_for(fy, metric, field, universe, pred, label):
        rs = tuple(r for r in dafrc if int(r["fiscal_year_end"]) == fy and pred(r))
        vals = tuple(to_float(r[field]) or 0.0 for r in rs)
        c = concentration(vals)
        cov = safe_div(c["total"], totals[fy][metric])
        top = sorted(rs, key=lambda r: -(to_float(r[field]) or 0.0))[:5]
        top_names = " > ".join(r["name"] for r in top)
        return tuple(row(metric_id=f"CONC_{k}_{metric}", computation="concentration", entity=label,
                         fiscal_year=fy, value=rnd(c[k], 2 if k == "HHI" else 6),
                         unit="HHI points (0-10000)" if k == "HHI" else "ratio",
                         numerator="", denominator=c["n"], coverage_share=rnd(cov),
                         check_status=universe,
                         definition=f"{k} of sponsor {field} computed over {label}; denominator = n sponsors with positive values; coverage_share = covered value / DAFRC total for FY. Top5: {top_names}",
                         inputs=DAFRC_FILE)
                     for k in ("CR1", "CR3", "CR5", "CR10", "HHI"))

    specs = (
        ("all_rows_incl_imputed", lambda f: (lambda r: True), "DAFRC universe, all rows"),
        ("filed_only", lambda f: (lambda r: is_filed(r[PROVENANCE_FIELD[f]])), "DAFRC universe, filed values only (Imputed/NPT-historical excluded)"),
        ("national_sponsors_only", lambda f: (lambda r: r["type"] == "National"), "DAFRC national sponsors (all rows)"),
    )
    return tuple(r for fy in sorted(totals) for metric, field in DAFRC_FIELDS.items()
                 for (universe, pred_f, label) in specs
                 for r in rows_for(fy, metric, field, universe, pred_f(field), label))


def type_share_rows(dafrc: Sequence[Mapping], totals: Mapping) -> tuple:
    keyed = group_by(dafrc, lambda r: (int(r["fiscal_year_end"]), r["type"], r["subtype"] if r["type"] == "National" else ""))
    return tuple(row(metric_id=f"TYPE_SHARE_{metric}", computation="segment_share", entity=f"{t}{'/' + st if st else ''}",
                     fiscal_year=fy, value=rnd(safe_div(sum(to_float(r[field]) or 0 for r in rs), totals[fy][metric])),
                     unit="ratio", numerator=sum(to_float(r[field]) or 0 for r in rs), denominator=totals[fy][metric],
                     check_status="info", definition="Segment (DAFRC type / national subtype) share of DAFRC total",
                     inputs=DAFRC_FILE)
                 for (fy, t, st), rs in sorted(keyed.items()) for metric, field in DAFRC_FIELDS.items())


# ---------------------------------------------------------------------------
# G. Cross-source checks
# ---------------------------------------------------------------------------
def npt_vs_dafrc_rows(market: Sequence[Mapping]) -> tuple:
    dafrc = published_lookup(market, "DAFRC_2025_UPDATED")
    # latest NPT vintage for each FY: prefer revised prior (later edition) over headline
    npt_rev = published_lookup(market, "NPT_DAFR_REVISED_PRIOR")
    npt_head = published_lookup(market, "NPT_DAFR_HEADLINE")
    npt_best = {**npt_head, **npt_rev}
    return tuple(row(metric_id=f"RATIO_DAFRC_TO_NPT_{m}", computation="cross_publisher_ratio", entity="DAFRC updated / NPT latest vintage",
                     fiscal_year=fy, value=rnd(safe_div(dafrc[(fy, m)], npt_best[(fy, m)])), unit="ratio",
                     numerator=dafrc[(fy, m)], denominator=npt_best[(fy, m)],
                     check_status="DIFFERENT_UNIVERSES_do_not_splice",
                     definition="DAFRC value / NPT value for same FY label; NPT latest vintage = revised-prior column of the next edition when available",
                     inputs=MARKET_FILE)
                 for (fy, m) in sorted(dafrc) if (fy, m) in npt_best and not m.endswith("_pct"))


def schedule_d_vs_990_rows(sponsor_rows: Sequence[Mapping]) -> tuple:
    idx = {(r["ein"], r["fiscal_year"], r["metric"]): r for r in sponsor_rows}
    pairs = (("daf_contributions", "form990_total_contributions_gifts_grants"),
             ("daf_assets_eoy", "form990_total_assets_eoy"))
    keys = sorted({(r["ein"], r["fiscal_year"]) for r in sponsor_rows if r["data_source_type"] == "propublica_form990_extract"})
    return tuple(
        row(metric_id=f"RATIO_SCHEDULE_D_TO_990_{a}", computation="cross_source_ratio", entity=d["sponsor"], ein=ein,
            fiscal_year=fy, value=rnd(safe_div(to_float(d["value"]), to_float(p["value"]))), unit="ratio",
            numerator=d["value"], denominator=p["value"],
            check_status=("period_end_mismatch" if d["period_end"][:7] != p["period_end"][:7] else "period_matched")
                         + (";dafrc_imputed" if d["value_provenance"].lower() == "imputed" else ""),
            definition="DAF-only Schedule D value / whole-organisation Form 990 total (ProPublica); <1 indicates non-DAF activity, >1 a definitional or period mismatch",
            inputs=SPONSOR_FILE)
        for (ein, fy) in keys for a, b in pairs
        for d, p in [(idx.get((ein, fy, a)), idx.get((ein, fy, b)))] if d and p and d["value"] and p["value"])


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------
def compute_all(market, dafrc, sponsors) -> tuple:
    totals = dafrc_totals(dafrc)
    idx = sponsor_year_index(dafrc)
    names = named_eins(sponsors)
    steps = (
        lambda: yoy_rows(market),
        lambda: cagr_rows(market),
        lambda: recompute_check_rows(totals, published_lookup(market, "DAFRC_2025_UPDATED")),
        lambda: coverage_rows(totals),
        lambda: market_payout_rows(totals, npt_payout_inputs(market)),
        lambda: sponsor_payout_rows(idx, names),
        lambda: payout_distribution_rows(dafrc, idx),
        lambda: share_rows(sponsors, totals),
        lambda: concentration_rows(dafrc, totals),
        lambda: type_share_rows(dafrc, totals),
        lambda: npt_vs_dafrc_rows(market),
        lambda: schedule_d_vs_990_rows(sponsors),
    )
    return reduce(lambda acc, step: acc + step(), steps, ())


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description="Compute derived DAF metrics")
    ap.add_argument("--data-dir", default=os.path.join(root, "data", "mission-2026-11-14"))
    args = ap.parse_args()
    load = lambda f: read_csv(os.path.join(args.data_dir, f))  # noqa: E731
    rows = compute_all(load(MARKET_FILE), load(DAFRC_FILE), load(SPONSOR_FILE))
    out = os.path.join(args.data_dir, "derived-metrics.csv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write(to_csv(rows))
    mism = sum(1 for r in rows if r["check_status"] == "MISMATCH")
    print(f"wrote {out}: {len(rows)} rows; recompute mismatches: {mism}")


if __name__ == "__main__":
    main()
