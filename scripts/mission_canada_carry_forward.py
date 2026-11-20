#!/usr/bin/env python3
"""Carry-forward pools for Canadian DAF sponsors in disbursement-quota (DQ) shortfall (task P-B3946-02).

Question. The 2025 release of the CRA T3010 open data has 22 DAF sponsors (line 5860 = Y) whose Schedule 8
spending is below their DQ (route SHORTFALL in data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv).
ITA s.149.1(20) lets a charity count a "disbursement excess" of one taxation year towards the DQ of the
immediately preceding year and of up to five immediately subsequent years, for the part not already used.
This script chains each sponsor's yearly excess / shortfall by BN and tests whether excesses from up to five
earlier years cover the 2025 shortfall.

Yearly excess (+) or shortfall (-), by regime:
  * NEW (fiscal periods beginning on or after 2023-01-01; T3010 v27; Schedule 8 published in the 2023, 2024 and
    2025 releases): filed line 865 (= 860 - 840); if 865 is blank, spending (860, else 845+850+855) minus the DQ
    (840, else the formula on 815 or 805 - 810).
  * OLD_PROXY (earlier fiscal periods; no Schedule 8 exists: the 2019-2022 Schedule 8 files are header-only):
    Schedule 6 line 5000 (charitable programs) + line 5050 (gifts to qualified donees) minus the pre-2023 DQ,
    3.5% of line 5900 if line 5900 exceeds C$100k (charitable organization, designation C) or C$25k (foundations,
    A/B), else nil (ITA s.149.1(1) "disbursement quota" as consolidated 2022-11-17). A proxy, not the filed figure.

Coverage tests for the 2025 shortfall S (each a separate column):
  1. prior_release_865   the previous release's latest line 865 >= S (reproduces the 10 of 22 in the parent doc)
  2. filed_gross         sum of positive NEW-regime excesses in the five preceding taxation years >= S
  3. filed_net           FIFO pool over NEW-regime years only: each excess enters the pool and expires after five
                         subsequent years; each intermediate shortfall first takes the next year's excess
                         (carry-back) and then the oldest pool excess; S is covered if the pool left at the 2025
                         year is >= S
  4. proxy_net           as 3, adding OLD_PROXY years (fiscal periods ending 2020-2023 releases)

Usage:
  python3 scripts/mission_canada_carry_forward.py . --dq-dirs DIR_A DIR_B --fin-dirs DIR_C DIR_D
      [--netting data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv]
      [--out data/mission-2026-11-14/canada-carry-forward-2026-11-20.csv] [--summary FILE.json]
  --dq-dirs   holds {Y}_dq_schedule_8_dq_{Y}*.csv for Y = 2023, 2024, 2025 (2019-2022 optional, header-only)
  --fin-dirs  holds {Y}_fin_financial_d_and_schedule_6_{Y}_updated.csv for Y = 2020 ... 2023
Stdlib only; functional (pure functions, no mutable global state). Imports the parent scripts unchanged.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import sys
from datetime import date, timedelta
from functools import reduce

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_canada_daf_panel as panel  # noqa: E402  (imported, not modified)
import mission_canada_netting_dq as ndq  # noqa: E402  (imported, not modified)

DQ_YEARS = (2019, 2020, 2021, 2022, 2023, 2024, 2025)
FIN_YEARS = (2020, 2021, 2022, 2023)
TARGET_YEAR = 2025
LOOKBACK_YEARS = 5
SLACK_DAYS = 31  # tolerance for a changed fiscal year end when counting "five preceding years"
OLD_RATE = 0.035
OLD_THRESHOLD = {"C": 100_000.0, "A": 25_000.0, "B": 25_000.0}

FIELDS = [
    "bn", "legal_name", "designation", "target_fpe", "target_dq", "target_spending", "target_shortfall",
    "fpe", "release", "regime", "form_id", "in_lookback_window", "years_before_target",
    "dq_840_or_proxy", "spending_or_proxy", "line_865_filed", "excess_or_shortfall", "excess_source",
    "pool_after_year_filed_net", "pool_after_year_proxy_net",
    "prior_release_865", "covered_prior_release_865", "lookback_excess_filed_gross", "covered_filed_gross",
    "pool_at_target_filed_net", "covered_filed_net", "pool_at_target_proxy_net", "covered_proxy_net",
    "uncovered_filed_net", "uncovered_proxy_net", "n_new_regime_prior_years", "n_old_proxy_prior_years",
    "verdict",
]


# ---------- pure helpers ----------
def d(s: str) -> date:
    return date.fromisoformat(s[:10])


def years_back(t: date, n: int) -> date:
    """t minus n calendar years (Feb 29 -> Feb 28)."""
    try:
        return t.replace(year=t.year - n)
    except ValueError:
        return t.replace(year=t.year - n, day=28)


def in_window(target_fpe: str, fpe: str) -> bool:
    """fpe ends one of the (up to) five taxation years immediately preceding the target year."""
    t, f = d(target_fpe), d(fpe)
    return years_back(t, LOOKBACK_YEARS) - timedelta(days=SLACK_DAYS) <= f < t


def new_regime_excess(r: dict) -> tuple[float | None, str | None, float | None, float | None]:
    """(excess, source, dq, spending) for a Schedule 8 row."""
    g = lambda k: panel.num(r.get(k))
    base = g("815") if g("815") is not None else (max((g("805") or 0) - (g("810") or 0), 0.0)
                                                  if g("805") is not None else None)
    dq = g("840") if g("840") is not None else ndq.dq_formula(base)
    spend = ndq.first_present(g("860"), ndq.sum_present([g("845"), g("850"), g("855")]))
    if g("865") is not None:
        return g("865"), "865", dq, spend
    if dq is not None and spend is not None:
        return spend - dq, "860-840", dq, spend
    return None, None, dq, spend


def old_regime_excess(r: dict, designation: str) -> tuple[float | None, str | None, float | None, float | None]:
    """Pre-2023 proxy: 5000 + 5050 - 3.5% x 5900 (nil DQ at or below the C$100k / C$25k threshold)."""
    g = lambda k: panel.num(r.get(k))
    base = g("5900")
    spend = ndq.sum_present([g("5000"), g("5050")])
    if base is None or spend is None:
        return None, None, None, spend
    dq = OLD_RATE * base if base > OLD_THRESHOLD.get(designation, 25_000.0) else 0.0
    return spend - dq, "proxy_5000+5050-3.5%x5900", dq, spend


def chain_records(bn: str, designation: str, dq_rows: list[dict], fin_rows: list[dict]) -> list[dict]:
    """One record per FPE: Schedule 8 (NEW) wins; else a pre-v27 Schedule 6 return gives OLD_PROXY.
    Later releases override earlier ones for the same FPE."""
    new = reduce(lambda acc, r: {**acc, r["FPE"]: r}, sorted(dq_rows, key=lambda r: r["_release"]), {})
    old_cands = [r for r in sorted(fin_rows, key=lambda r: r["_release"])
                 if r["FPE"] not in new and (panel.num(r.get("Form ID")) or 0) < 27]
    old = reduce(lambda acc, r: {**acc, r["FPE"]: r}, old_cands, {})

    def rec_new(fpe: str, r: dict) -> dict:
        ex, src, dq, sp = new_regime_excess(r)
        return {"bn": bn, "fpe": fpe, "release": r["_release"], "regime": "NEW", "form_id": r.get("Form ID", ""),
                "dq_840_or_proxy": dq, "spending_or_proxy": sp, "line_865_filed": panel.num(r.get("865")),
                "excess_or_shortfall": ex, "excess_source": src}

    def rec_old(fpe: str, r: dict) -> dict:
        ex, src, dq, sp = old_regime_excess(r, designation)
        return {"bn": bn, "fpe": fpe, "release": r["_release"], "regime": "OLD_PROXY",
                "form_id": r.get("Form ID", ""), "dq_840_or_proxy": dq, "spending_or_proxy": sp,
                "line_865_filed": None, "excess_or_shortfall": ex, "excess_source": src}

    return sorted([rec_new(f, r) for f, r in new.items()] + [rec_old(f, r) for f, r in old.items()],
                  key=lambda x: x["fpe"])


def fifo_pool(records: list[dict]) -> list[tuple[dict, float]]:
    """Chronological s.149.1(20) pool. State = (pool [(expiry_date, amount)], pending shortfall of last year).
    For each year: drop expired excesses; a shortfall takes from the oldest excess first and leaves any rest
    pending for a carry-back from the next year; an excess first covers the previous year's pending shortfall
    (carry-back, immediately preceding year only), then enters the pool, usable for five subsequent years.
    Returns [(record, pool total after the year)]. Unknown years (excess None) break nothing and add nothing."""
    def take(pool: list, need: float) -> tuple[list, float]:
        def step(acc, item):
            kept, rest = acc
            exp, amt = item
            used = min(amt, rest)
            return (kept + ([(exp, amt - used)] if amt - used > 0 else []), rest - used)
        return reduce(step, sorted(pool), ([], need))

    def step(state, rec):
        pool, pending, out = state
        f = d(rec["fpe"])
        live = [(e, a) for e, a in pool if e >= f]
        x = rec["excess_or_shortfall"]
        if x is None:
            return live, 0.0, out + [(rec, sum(a for _, a in live))]
        if x < 0:
            new_pool, rest = take(live, -x)
            return new_pool, rest, out + [(rec, sum(a for _, a in new_pool))]
        left = x - min(x, pending)
        exp = years_back(f, -LOOKBACK_YEARS) + timedelta(days=SLACK_DAYS)
        new_pool = live + ([(exp, left)] if left > 0 else [])
        return new_pool, 0.0, out + [(rec, sum(a for _, a in new_pool))]

    return reduce(step, records, ([], 0.0, []))[2]


def pool_before(records: list[dict], target_fpe: str) -> tuple[list[tuple[dict, float]], float]:
    """Pool states for the prior years and the unexpired pool available at the target year."""
    prior = [r for r in records if r["fpe"] < target_fpe]
    states = fifo_pool(prior)
    t = d(target_fpe)
    # recompute the live pool at the target date (expiry check) by re-running with a zero-excess target
    probe = fifo_pool(prior + [{"fpe": target_fpe, "excess_or_shortfall": 0.0}])
    _ = t
    return states, probe[-1][1] if probe else 0.0


def sponsor_rows(s: dict, records: list[dict]) -> list[dict]:
    t_fpe = s["fpe"]
    shortfall = -(panel.num(s["dq_excess_used"]) or 0.0)
    prior = [r for r in records if r["fpe"] < t_fpe]
    window = [r for r in prior if in_window(t_fpe, r["fpe"])]
    window5 = sorted(window, key=lambda r: r["fpe"])[-LOOKBACK_YEARS:]
    w_fpes = {r["fpe"] for r in window5}
    new_prior = [r for r in prior if r["regime"] == "NEW"]
    states_f, pool_f = pool_before(new_prior, t_fpe)
    states_p, pool_p = pool_before(prior, t_fpe)
    gross = sum(max(r["excess_or_shortfall"] or 0.0, 0.0) for r in window5 if r["regime"] == "NEW")
    pr865 = panel.num(s["prior_release_dq_865"])
    after_f = {r["fpe"]: p for r, p in states_f}
    after_p = {r["fpe"]: p for r, p in states_p}
    cov = {
        "covered_prior_release_865": pr865 is not None and pr865 >= shortfall,
        "covered_filed_gross": gross >= shortfall,
        "covered_filed_net": pool_f >= shortfall,
        "covered_proxy_net": pool_p >= shortfall,
    }
    verdict = ("COVERED_FILED" if cov["covered_filed_net"] else
               "COVERED_ONLY_WITH_PRE2023_PROXY" if cov["covered_proxy_net"] else
               "PARTLY_COVERED" if pool_p > 0 else "UNCOVERED")
    common = {
        "bn": s["bn"], "legal_name": s["legal_name"], "designation": s["designation"], "target_fpe": t_fpe,
        "target_dq": panel.num(s["dq_requirement_used"]), "target_spending": panel.num(s["dq_spending_used"]),
        "target_shortfall": shortfall, "prior_release_865": pr865, "lookback_excess_filed_gross": gross,
        "pool_at_target_filed_net": pool_f, "pool_at_target_proxy_net": pool_p,
        "uncovered_filed_net": max(shortfall - pool_f, 0.0), "uncovered_proxy_net": max(shortfall - pool_p, 0.0),
        "n_new_regime_prior_years": sum(1 for r in window5 if r["regime"] == "NEW"),
        "n_old_proxy_prior_years": sum(1 for r in window5 if r["regime"] == "OLD_PROXY"),
        "verdict": verdict, **cov,
    }
    target = {"fpe": t_fpe, "release": TARGET_YEAR, "regime": "NEW", "form_id": "27",
              "dq_840_or_proxy": common["target_dq"], "spending_or_proxy": common["target_spending"],
              "line_865_filed": panel.num(s["dq_865"]), "excess_or_shortfall": -shortfall,
              "excess_source": "target_year (netting CSV dq_excess_used)"}
    rows = [{**common, **{k: r[k] for k in ("fpe", "release", "regime", "form_id", "dq_840_or_proxy",
                                              "spending_or_proxy", "line_865_filed", "excess_or_shortfall",
                                              "excess_source")},
             "in_lookback_window": r["fpe"] in w_fpes,
             "years_before_target": round((d(t_fpe) - d(r["fpe"])).days / 365.25, 2),
             "pool_after_year_filed_net": after_f.get(r["fpe"]),
             "pool_after_year_proxy_net": after_p.get(r["fpe"])} for r in prior]
    return rows + [{**common, **target, "in_lookback_window": None, "years_before_target": 0.0,
                    "pool_after_year_filed_net": None, "pool_after_year_proxy_net": None}]


# ---------- payout effect ----------
def payout_effect(net_rows: list[dict], sponsors: list[dict]) -> dict:
    """Tier-B netted payout (2025 release) with and without the shortfall sponsors, and with uncovered
    shortfalls hypothetically paid out as extra DAF grants (upper bound on any effect)."""
    yr = [r for r in net_rows if r["dataset_year"] == str(TARGET_YEAR) and panel.num(r["prior_daf_assets_5862"])]
    num_ = lambda r: panel.num(r["net_5864_tier_b"]) or 0.0
    den_ = lambda r: panel.num(r["prior_daf_assets_5862"]) or 0.0
    agg = lambda rs, extra=0.0: panel.ratio(sum(map(num_, rs)) + extra, sum(map(den_, rs)))
    bns = {s["bn"] for s in sponsors}
    unc = {s["bn"] for s in sponsors if s["verdict"] in ("UNCOVERED", "PARTLY_COVERED")}
    shortfall_in_base = [r for r in yr if r["bn"] in bns]
    unc_dollars = sum(s["uncovered_proxy_net"] for s in sponsors if s["bn"] in {r["bn"] for r in shortfall_in_base})
    return {
        "n_matched": len(yr), "base_prior_daf_assets": sum(map(den_, yr)),
        "payout_net_tier_b": agg(yr),
        "shortfall_sponsors_in_matched_base": len(shortfall_in_base),
        "shortfall_sponsors_prior_daf_assets": sum(map(den_, shortfall_in_base)),
        "shortfall_sponsors_net_5864_tier_b": sum(map(num_, shortfall_in_base)),
        "shortfall_sponsors_payout_net_tier_b": agg(shortfall_in_base),
        "payout_net_tier_b_excluding_shortfall_sponsors": agg([r for r in yr if r["bn"] not in bns]),
        "payout_net_tier_b_excluding_uncovered": agg([r for r in yr if r["bn"] not in unc]),
        "uncovered_shortfall_dollars_in_base": unc_dollars,
        "payout_net_tier_b_if_uncovered_paid_as_daf_grants": agg(yr, unc_dollars),
    }


# ---------- I/O ----------
def find_any(dirs: list[str], year: int, kind: str) -> str | None:
    hits = sorted(h for dd in dirs for h in glob.glob(os.path.join(dd, f"{year}_{kind}_*.csv")))
    return hits[0] if hits else None


def load(dirs: list[str], years: tuple, kind: str, bns: set) -> tuple[list[dict], dict]:
    paths = {y: find_any(dirs, y, kind) for y in years}
    rows = [dict(r, _release=y) for y, p in paths.items() if p for r in panel.read_csv(p) if r.get("BN") in bns]
    counts = {y: (sum(1 for _ in panel.read_csv(p)) if p else None) for y, p in paths.items()}
    return rows, counts


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", help="repo root ('.')")
    ap.add_argument("--dq-dirs", nargs="+", required=True)
    ap.add_argument("--fin-dirs", nargs="+", required=True)
    ap.add_argument("--netting", default="data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv")
    ap.add_argument("--out", default="data/mission-2026-11-14/canada-carry-forward-2026-11-20.csv")
    ap.add_argument("--summary", default=None)
    a = ap.parse_args(argv)

    net_rows = panel.read_csv(os.path.join(a.root, a.netting))
    targets = [r for r in net_rows if r["dataset_year"] == str(TARGET_YEAR) and r["route"] == "SHORTFALL"]
    bns = {r["bn"] for r in targets}
    dq_rows, dq_counts = load(a.dq_dirs, DQ_YEARS, "dq", bns)
    fin_rows, fin_counts = load(a.fin_dirs, FIN_YEARS, "fin", bns)

    per = [sponsor_rows(s, chain_records(s["bn"], s["designation"],
                                         [r for r in dq_rows if r["BN"] == s["bn"]],
                                         [r for r in fin_rows if r["BN"] == s["bn"]]))
           for s in sorted(targets, key=lambda r: -(panel.num(r["dq_requirement_used"]) or 0))]
    rows = [r for p in per for r in p]
    sponsors = [p[-1] for p in per]

    out = os.path.join(a.root, a.out)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows({k: panel.fmt(r.get(k)) for k in FIELDS} for r in rows)

    tot = lambda sel, k: sum(s[k] for s in sel)
    by_verdict = ndq.fold_sum((s["verdict"], 1) for s in sponsors)
    summary = {
        "schedule8_rows_by_release": dq_counts, "fin_rows_by_release": fin_counts,
        "n_shortfall_sponsors": len(sponsors),
        "total_shortfall": tot(sponsors, "target_shortfall"),
        "covered": {k: {"n": sum(1 for s in sponsors if s[k]),
                        "shortfall_dollars": sum(s["target_shortfall"] for s in sponsors if s[k])}
                    for k in ("covered_prior_release_865", "covered_filed_gross", "covered_filed_net",
                              "covered_proxy_net")},
        "uncovered_dollars": {"filed_net": tot(sponsors, "uncovered_filed_net"),
                              "proxy_net": tot(sponsors, "uncovered_proxy_net")},
        "verdicts": by_verdict,
        "verdict_dollars": ndq.fold_sum((s["verdict"], s["target_shortfall"]) for s in sponsors),
        "prior_years_available": ndq.fold_sum(((s["n_new_regime_prior_years"], s["n_old_proxy_prior_years"]), 1)
                                              for s in sponsors),
        "sponsors": [{k: s[k] for k in ("bn", "legal_name", "designation", "target_fpe", "target_dq",
                                         "target_spending", "target_shortfall", "prior_release_865",
                                         "lookback_excess_filed_gross", "pool_at_target_filed_net",
                                         "pool_at_target_proxy_net", "uncovered_proxy_net",
                                         "n_new_regime_prior_years", "n_old_proxy_prior_years",
                                         "covered_prior_release_865", "covered_filed_net", "covered_proxy_net",
                                         "verdict")} for s in sponsors],
        "payout_effect": payout_effect(net_rows, sponsors),
    }
    text = json.dumps(summary, indent=1, default=str)
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
