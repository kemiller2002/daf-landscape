#!/usr/bin/env python3
"""P-B4501-04 and P-B45N33-02-03: long-tail admin-fee pool range and per-sponsor fee coverage.

Stdlib only; functional style (pure functions over tuples/dicts; I/O only at the edges). No network.

Inputs (repository files)
  data/mission-2026-11-14/long-tail-fee-census-2026-11-19.csv   published schedules (admin_tiers, basis, min fee)
  data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv the 1,240 tail sponsors (FY2024 DAF assets, accounts)
  data/mission-2026-11-14/long-tail-operating-cost-2026-11-19.csv allocated DAF operating cost, rules A / G / AM

What it computes
  1. Fee engine: re-parses each published schedule from the census CSV text and checks the recomputed fee at
     $25k / $100k / $500k against the census columns (must match to 0.1 bps).
  2. Pool, flat-rate view: rate x $9.18bn for reference rates (old 100 bps hypothetical; tail p25/median/p75/max).
  3. Pool, schedule view: each published 2021+ schedule applied to every tail sponsor at its own FY2024 average
     account (fee per account x implied accounts = fee bps at the average account x DAF assets). Sponsors without a
     screened average account get the median average account of their sponsor_category. Two charge sets:
     whole tail (1,240) and CFs only (641; non-CFs at zero). With and without minimum annual fees.
     Central = median of the schedule pools; low/high = lowest non-zero and highest schedule pool. A seeded
     bootstrap of the median over the 6 CF schedules (and the 7 all-type schedules) gives a sampling interval.
  4. Per-sponsor coverage: for each sampled sponsor with a published rate, fee revenue = fee at its own average
     account x screened accounts, against its allocated DAF cost (rules A, G, AM). Alternative readings
     (Whatcom, Athens, Pikes Peak) and the pre-2021 West Texas schedule are shown as sensitivity rows.
  5. Population coverage: for every usable tail CF in the cost study, fee bps at its own average account under each
     CF schedule vs its allocated cost bps; counts of CFs at a loss under each rule; aggregate fee / aggregate cost.
  6. check-corrections: parses the "## Exact corrections" section of the research note and verifies that each Find
     occurs exactly once in its file, that each Replace ends with [b4501-04], and that applying all corrections in
     order (in memory only) succeeds. Files are never written by this task.

Usage
  python3 scripts/mission_tail_fee_pool.py . --task pool          # prints tables, writes the CSV
  python3 scripts/mission_tail_fee_pool.py . --task check-corrections
"""
from __future__ import annotations

import argparse
import csv
import os
import random
import re
import statistics
import sys
from functools import reduce
from typing import Callable, Iterable, Mapping, Sequence

D = "data/mission-2026-11-14"
CENSUS = f"{D}/long-tail-fee-census-2026-11-19.csv"
TAIL = f"{D}/daf-long-tail-sponsors-fy2021-2024.csv"
COST = f"{D}/long-tail-operating-cost-2026-11-19.csv"
OUT = f"{D}/tail-fee-pool-revision-2026-11-19.csv"
NOTE = "research/mission-2026-11-14/b4501-04-tail-fee-pool-revision.md"
TAIL_BANDS = ("t10_50", "t1_10", "t0_1", "zero")
TAG = "[b4501-04]"
SEED = 20261119
BOOT = 20000
OLD_RATE_BPS = 100.0

# Alternative readings documented in b45n33-01 §2.2 (each is the census's own sensitivity, not new data).
# Upper tiers that the census did not transcribe for the alternative column are kept from the standard column;
# they only matter for average accounts above the first tier's ceiling.
ALTERNATIVES = {
    "911726410": ("Whatcom 1.50% (endowed / long-term-pool reading)", "marginal",
                  ((0, 500_000, 1.5), (500_000, 1_000_000, 1.5), (1_000_000, 5_000_000, 1.25), (5_000_000, None, 1.0))),
    "311040215": ("Athens marginal reading", "marginal", ((0, 500_000, 1.5), (500_000, None, 1.0))),
    "841339670": ("Pikes Peak endowed-DAF column (1.00% first $3m)", "marginal",
                  ((0, 3_000_000, 1.0), (3_000_000, 5_000_000, 1.0), (5_000_000, 10_000_000, 0.75), (10_000_000, None, 0.25))),
}


# ----------------------------------------------------------------------------- small pure helpers
def num(x) -> float | None:
    try:
        return None if x in (None, "") else float(x)
    except ValueError:
        return None


def median(xs: Sequence[float]) -> float | None:
    return statistics.median(xs) if xs else None


def quantile(xs: Sequence[float], q: float) -> float | None:
    s = sorted(xs)
    if not s:
        return None
    pos = (len(s) - 1) * q
    lo, hi = int(pos), min(int(pos) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def group_by(items: Iterable, key: Callable) -> dict:
    return reduce(lambda acc, x: {**acc, key(x): acc.get(key(x), ()) + (x,)}, items, {})


def read_csv(root: str, rel: str) -> tuple[dict, ...]:
    with open(os.path.join(root, rel), newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def write_csv(root: str, rel: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(os.path.join(root, rel), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.4f}".rstrip("0").rstrip(".") if abs(v) < 100 else f"{v:.1f}".rstrip("0").rstrip(".")
    return str(v)


def usd_m(v: float | None) -> str:
    return "–" if v is None else f"${v / 1e6:,.1f}m"


# ----------------------------------------------------------------------------- fee engine
def parse_tiers(text: str) -> tuple[tuple[float, float | None, float], ...]:
    """'0-500,000: 2.0%; 500,000-: 1.0%' -> ((0, 500000, 2.0), (500000, None, 1.0))."""
    def one(part: str):
        m = re.fullmatch(r"\s*([\d,]+)-([\d,]*):\s*([\d.]+)%\s*", part)
        if not m:
            raise ValueError(f"unparsed tier: {part!r}")
        lo, up, r = m.groups()
        return float(lo.replace(",", "")), (float(up.replace(",", "")) if up else None), float(r)
    return tuple(map(one, filter(None, text.split(";")))) if text else ()


def fee_at(s: Mapping, balance: float, use_min: bool = True) -> float:
    tiers = s["tiers"]
    if s["basis"] == "marginal":
        fee = sum(max(0.0, min(balance, up if up is not None else balance) - lo) * r / 100 for lo, up, r in tiers)
    else:
        fee = balance * next((r for lo, up, r in tiers if balance >= lo and (up is None or balance < up)),
                             tiers[-1][2]) / 100
    floor = (s.get("min_fee") or 0.0) if use_min else 0.0
    return max(fee, floor) + (s.get("flat_fee") or 0.0)


def fee_bps(s: Mapping, balance: float, use_min: bool = True) -> float:
    return fee_at(s, balance, use_min) / balance * 1e4


def schedule_of(r: Mapping, label: str | None = None, basis: str | None = None, tiers=None, kind: str = "published") -> dict:
    return dict(ein=r["ein"], name=r["name"], type4=r["type4"], status=r["fee_status"],
                label=label or r["name"].title(), kind=kind,
                basis=basis or r["fee_basis"], tiers=tiers if tiers is not None else parse_tiers(r["admin_tiers"]),
                min_fee=num(r["min_annual_fee_usd"]), flat_fee=num(r["flat_annual_fee_usd"]),
                census=r)


def schedules(census: Sequence[Mapping]) -> dict:
    with_rate = tuple(r for r in census if r["admin_tiers"])
    main = tuple(schedule_of(r) for r in with_rate if r["in_2021plus_distribution"] == "yes")
    pre = tuple(schedule_of(r, kind="pre2021") for r in with_rate if r["fee_status"] == "published_pre2021")
    alt = tuple(schedule_of(next(r for r in with_rate if r["ein"] == e), label=a[0], basis=a[1], tiers=a[2], kind="alternative")
                for e, a in ALTERNATIVES.items())
    return dict(main=main, cf=tuple(s for s in main if s["type4"] == "cf"), pre=pre, alt=alt)


def engine_check(main: Sequence[Mapping]) -> tuple[str, ...]:
    """Recomputed bps at $25k/$100k/$500k must equal the census columns."""
    def bad(s):
        return tuple(f"{s['name']} at {b}: {fee_bps(s, b):.1f} vs census {s['census'][k]}"
                     for b, k in ((25_000, "admin_bps_25k"), (100_000, "admin_bps_100k"), (500_000, "admin_bps_500k"))
                     if abs(fee_bps(s, b) - float(s["census"][k])) > 0.1)
    return tuple(x for s in main for x in bad(s))


# ----------------------------------------------------------------------------- frame
def tail_frame(tail_rows: Sequence[Mapping]) -> tuple[dict, ...]:
    rows = tuple(r for r in tail_rows if r["size_band_fy2024"] in TAIL_BANDS)
    by_cat = group_by((r for r in rows if num(r["avg_account_fy2024"])), lambda r: r["sponsor_category"])
    cat_med = {k: median([num(r["avg_account_fy2024"]) for r in v]) for k, v in by_cat.items()}
    def one(r):
        own = num(r["avg_account_fy2024"])
        return dict(ein=r["ein"], name=r["name"], cat=r["sponsor_category"], is_cf=r["sponsor_category"] == "community_foundation",
                    assets=num(r["daf_assets_fy2024"]) or 0.0, avg=own or cat_med[r["sponsor_category"]],
                    avg_source="own" if own else "category_median")
    return tuple(map(one, rows))


def pool(frame: Sequence[Mapping], s: Mapping | None, rate_bps: float | None = None, cf_only: bool = False,
         use_min: bool = True) -> float:
    """Annual admin fees if every sponsor in the charge set applied schedule s (or a flat rate) to its DAF assets,
    evaluated at the sponsor's average account (fee bps at the average account x assets)."""
    charged = (f for f in frame if f["assets"] > 0 and (f["is_cf"] or not cf_only))
    rate = (lambda f: rate_bps) if s is None else (lambda f: fee_bps(s, f["avg"], use_min))
    return sum(f["assets"] * rate(f) / 1e4 for f in charged)


def bootstrap_median(values: Sequence[float], seed: int, n: int = BOOT) -> tuple[float, float]:
    rng = random.Random(seed)
    meds = sorted(statistics.median(rng.choices(values, k=len(values))) for _ in range(n))
    return quantile(meds, 0.05), quantile(meds, 0.95)


# ----------------------------------------------------------------------------- coverage
def cost_index(cost_rows: Sequence[Mapping]) -> dict:
    return {r["ein"]: r for r in cost_rows}


def coverage_row(s: Mapping, cost: Mapping | None) -> dict:
    c = s["census"]
    avg, n = num(c["avg_account_fy2024"]), num(c["accounts_fy2024_screened"])
    fee_acct = fee_at(s, avg) if avg else None
    revenue = fee_acct * n if fee_acct is not None and n else None
    def rule(k):
        tot = num(cost.get(f"daf_cost_alloc_{k}")) if cost else None
        per = num(cost.get(f"daf_cost_per_account_alloc_{k}")) if cost else None
        ratio = (fee_acct / per) if fee_acct is not None and per else None
        return {f"cost_alloc_{k}_usd": tot, f"cost_per_account_{k}_usd": per,
                f"coverage_{k}": ratio, f"covers_{k}": None if ratio is None else ("yes" if ratio >= 1 else "no"),
                f"cost_bps_{k}": num(cost.get(f"daf_cost_bps_daf_assets_alloc_{k}")) if cost else None}
    return dict(section="sponsor_coverage", scenario_id=f"cov_{s['kind']}_{s['ein']}", description=s["label"],
                schedule_kind=s["kind"], ein=s["ein"], name=s["name"], type4=s["type4"], fee_status=s["status"],
                avg_account_usd=avg, accounts=n, daf_assets_usd=num(c["daf_assets_fy2024"]),
                fee_per_account_usd=fee_acct, fee_bps_at_avg=(fee_acct / avg * 1e4) if fee_acct is not None else None,
                fee_revenue_usd=revenue, **rule("A"), **rule("G"), **rule("AM"))


def population_rows(cost_rows: Sequence[Mapping], tail_idx: Mapping, cf_sched: Sequence[Mapping]) -> tuple[dict, ...]:
    cfs = tuple(r for r in cost_rows if r["group"] == "tail_cf" and r["usable"] == "1" and num(r["daf_assets_fy2024"]))
    cat_med = median([f["avg"] for f in tail_idx.values() if f["is_cf"] and f["avg_source"] == "own"])
    avg = lambda r: tail_idx[r["ein"]]["avg"] if r["ein"] in tail_idx else cat_med
    def per_rule(s, k):
        have = tuple(r for r in cfs if num(r[f"daf_cost_bps_daf_assets_alloc_{k}"]) is not None)
        fees = tuple(fee_bps(s, avg(r)) for r in have)
        loss = sum(1 for r, f in zip(have, fees) if f < num(r[f"daf_cost_bps_daf_assets_alloc_{k}"]))
        fee_tot = sum(num(r["daf_assets_fy2024"]) * f / 1e4 for r, f in zip(have, fees))
        cost_tot = sum(num(r[f"daf_cost_alloc_{k}"]) or 0.0 for r in have)
        return dict(section="population_coverage", scenario_id=f"pop_{k}_{s['ein']}",
                    description=f"Tail CFs (cost study, usable, DAF assets > 0) at {s['label']}'s schedule, rule {k}",
                    schedule_kind=s["kind"], ein=s["ein"], name=s["name"], rule=k, share_n=len(have),
                    share_k=loss, share_value=loss / len(have), fee_pool_usd=fee_tot, cost_pool_usd=cost_tot,
                    aggregate_coverage=fee_tot / cost_tot if cost_tot else None)
    return tuple(per_rule(s, k) for s in cf_sched for k in ("A", "G", "AM"))


# ----------------------------------------------------------------------------- assembly
def pool_rows(frame: Sequence[Mapping], sch: Mapping) -> tuple[tuple[dict, ...], dict]:
    total = sum(f["assets"] for f in frame)
    cf_assets = sum(f["assets"] for f in frame if f["is_cf"])
    main, cf = sch["main"], sch["cf"]
    main_bps100 = [float(s["census"]["admin_bps_100k"]) for s in main]
    cf_bps100 = [float(s["census"]["admin_bps_100k"]) for s in cf]
    flat_rates = (("flat_old_100", "Old hypothetical: top-100 CF median at $100k", OLD_RATE_BPS),
                  ("flat_cf_p25", "Tail-CF published p25 at $100k (n=6)", quantile(cf_bps100, 0.25)),
                  ("flat_cf_median", "Tail-CF published median at $100k (n=6)", median(cf_bps100)),
                  ("flat_all_median", "All-type published median at $100k (n=7)", median(main_bps100)),
                  ("flat_cf_p75", "Tail-CF published p75 at $100k (n=6)", quantile(cf_bps100, 0.75)),
                  ("flat_max", "Highest published rate (Whatcom, Cal Poly Pomona)", max(main_bps100)))
    flat = tuple(dict(section="pool_flat_rate", scenario_id=i, description=d, rate_bps=r, charge_set=cs,
                      daf_assets_charged_usd=a, fee_pool_usd=a * r / 1e4, implied_bps=r, n_basis=n)
                 for i, d, r in flat_rates
                 for cs, a, n in (("whole_tail", total, 1240), ("cf_only", cf_assets, 641)))
    sched = tuple(dict(section="pool_schedule", scenario_id=f"sched_{s['kind']}_{s['ein']}_{cs}_{'min' if um else 'nomin'}",
                       description=s["label"], schedule_kind=s["kind"], ein=s["ein"], name=s["name"], type4=s["type4"],
                       charge_set=cs, use_min_fee="yes" if um else "no",
                       daf_assets_charged_usd=total if cs == "whole_tail" else cf_assets,
                       fee_pool_usd=p, implied_bps=p / (total if cs == "whole_tail" else cf_assets) * 1e4, n_basis=1240 if cs == "whole_tail" else 641)
                  for s in main + sch["pre"] + sch["alt"]
                  for cs in ("whole_tail", "cf_only") for um in (True, False)
                  for p in (pool(frame, s, cf_only=cs == "cf_only", use_min=um),))
    def summary(set_name, ss, cs, seed):
        pools = [pool(frame, s, cf_only=cs == "cf_only") for s in ss]
        nz = [p for p in pools if p > 0]
        lo_b, hi_b = bootstrap_median(pools, seed)
        return dict(set=set_name, charge_set=cs, n=len(ss), central=median(pools), low_nonzero=min(nz), high=max(pools),
                    zero=min(pools), boot_lo=lo_b, boot_hi=hi_b, pools=pools)
    summ = {(n, cs): summary(n, ss, cs, SEED + i) for i, (n, ss, cs) in enumerate(
        (n, ss, cs) for n, ss in (("cf6", cf), ("all7", main)) for cs in ("whole_tail", "cf_only"))}
    summ_rows = tuple(dict(section="pool_summary", scenario_id=f"summary_{k[0]}_{k[1]}_{stat}",
                           description=f"{stat} of the {v['n']} schedule pools ({k[0]}), charge set {k[1]}",
                           charge_set=k[1], fee_pool_usd=v[stat], n_basis=v["n"],
                           implied_bps=v[stat] / (total if k[1] == "whole_tail" else cf_assets) * 1e4,
                           notes="bootstrap: 5th/95th percentile of the median over 20,000 resamples of the schedules (seeded)" if stat.startswith("boot") else "")
                      for k, v in summ.items() for stat in ("central", "low_nonzero", "high", "zero", "boot_lo", "boot_hi"))
    return flat + sched + summ_rows, dict(total=total, cf_assets=cf_assets, summ=summ, cf_bps100=cf_bps100,
                                          main_bps100=main_bps100)


FIELDS = ("section", "scenario_id", "description", "schedule_kind", "ein", "name", "type4", "fee_status", "charge_set",
          "use_min_fee", "rate_bps", "n_basis", "daf_assets_charged_usd", "fee_pool_usd", "implied_bps",
          "avg_account_usd", "accounts", "daf_assets_usd", "fee_per_account_usd", "fee_bps_at_avg", "fee_revenue_usd",
          "cost_alloc_A_usd", "cost_alloc_G_usd", "cost_alloc_AM_usd", "cost_bps_A", "cost_bps_G", "cost_bps_AM",
          "coverage_A", "coverage_G", "coverage_AM", "covers_A", "covers_G", "covers_AM",
          "rule", "share_k", "share_n", "share_value", "cost_pool_usd", "aggregate_coverage", "notes")


def render(meta: Mapping, flat_sched: Sequence[Mapping], cov: Sequence[Mapping], pop: Sequence[Mapping], frame) -> str:
    L = []
    own = sum(1 for f in frame if f["avg_source"] == "own")
    own_assets = sum(f["assets"] for f in frame if f["avg_source"] == "own")
    L.append(f"Tail frame: {len(frame)} sponsors, DAF assets {usd_m(meta['total'])}; CFs {usd_m(meta['cf_assets'])} "
             f"({meta['cf_assets'] / meta['total']:.1%}). Own average account for {own} sponsors "
             f"({own_assets / meta['total']:.1%} of assets); category median for the rest.")
    L.append(f"Published bps at $100k: CF n=6 {sorted(meta['cf_bps100'])}; all n=7 {sorted(meta['main_bps100'])}")
    L.append("\n## P1 Flat-rate pools")
    L.append("| Scenario | Rate bps | Whole tail | CFs only |\n|---|---|---|---|")
    fr = group_by((r for r in flat_sched if r["section"] == "pool_flat_rate"), lambda r: r["scenario_id"])
    L += [f"| {v[0]['description']} | {v[0]['rate_bps']:.1f} | {usd_m(v[0]['fee_pool_usd'])} | {usd_m(v[1]['fee_pool_usd'])} |" for v in fr.values()]
    L.append("\n## P2 Schedule pools (each schedule applied at every sponsor's own average account)")
    L.append("| Schedule | Kind | Whole tail (min fee) | Whole tail bps | Whole tail (no min) | CFs only (min fee) | CFs only bps |\n|---|---|---|---|---|---|---|")
    sp = group_by((r for r in flat_sched if r["section"] == "pool_schedule"), lambda r: (r["schedule_kind"], r["ein"]))
    def cell(v, cs, um):
        return next(r for r in v if r["charge_set"] == cs and r["use_min_fee"] == um)
    L += [f"| {v[0]['description']} | {k[0]} | {usd_m(cell(v, 'whole_tail', 'yes')['fee_pool_usd'])} | "
          f"{cell(v, 'whole_tail', 'yes')['implied_bps']:.1f} | {usd_m(cell(v, 'whole_tail', 'no')['fee_pool_usd'])} | "
          f"{usd_m(cell(v, 'cf_only', 'yes')['fee_pool_usd'])} | {cell(v, 'cf_only', 'yes')['implied_bps']:.1f} |" for k, v in sp.items()]
    L.append("\n## P3 Pool range (2021+ schedules with minimum fees)")
    L.append("| Schedule set | Charge set | n | Central (median) | Low (lowest non-zero) | High | Bootstrap 90% of median | Zero-fee schedule |\n|---|---|---|---|---|---|---|---|")
    L += [f"| {k[0]} | {k[1]} | {v['n']} | {usd_m(v['central'])} | {usd_m(v['low_nonzero'])} | {usd_m(v['high'])} | "
          f"{usd_m(v['boot_lo'])}–{usd_m(v['boot_hi'])} | {usd_m(v['zero'])} |" for k, v in meta["summ"].items()]
    L.append("\n## C1 Per-sponsor coverage (fee revenue at own schedule and own average account vs allocated DAF cost)")
    L.append("| Sponsor | Kind | Avg account | Accounts | Fee bps | Fee revenue | Cost A / G / AM | Coverage A / G / AM | Covers A/G/AM |\n|---|---|---|---|---|---|---|---|---|")
    f0 = lambda v: "–" if v is None else f"${v:,.0f}"
    f2 = lambda v: "–" if v is None else f"{v:.2f}"
    f1 = lambda v: "–" if v is None else f"{v:.1f}"
    L += [f"| {r['description']} | {r['schedule_kind']} | {f0(r['avg_account_usd'])} | {fmt(r['accounts']) or '–'} | "
          f"{f1(r['fee_bps_at_avg'])} | {f0(r['fee_revenue_usd'])} | "
          f"{f0(r['cost_alloc_A_usd'])} / {f0(r['cost_alloc_G_usd'])} / {f0(r['cost_alloc_AM_usd'])} | "
          f"{f2(r['coverage_A'])} / {f2(r['coverage_G'])} / {f2(r['coverage_AM'])} | "
          f"{r['covers_A'] or '–'}/{r['covers_G'] or '–'}/{r['covers_AM'] or '–'} |" for r in cov]
    main_cov = [r for r in cov if r["schedule_kind"] == "published"]
    for k in ("A", "G", "AM"):
        rs = [r[f"coverage_{k}"] for r in main_cov if r[f"coverage_{k}"] is not None and r[f"cost_alloc_{k}_usd"]]
        L.append(f"- Rule {k}: covers {sum(1 for x in rs if x >= 1)} of {len(rs)}; median ratio {median(rs):.2f}; "
                 f"sum fee revenue / sum cost = {sum(r['fee_revenue_usd'] for r in main_cov if r[f'coverage_{k}'] is not None and r[f'cost_alloc_{k}_usd']) / sum(r[f'cost_alloc_{k}_usd'] for r in main_cov if r[f'coverage_{k}'] is not None and r[f'cost_alloc_{k}_usd']):.2f}")
    L.append("\n## C2 Population: usable tail CFs at a loss (fee at own average account < allocated cost), by CF schedule")
    L.append("| Schedule | Rule | CFs at a loss | Share | Aggregate fee / aggregate cost |\n|---|---|---|---|---|")
    L += [f"| {r['name'].title()} | {r['rule']} | {r['share_k']}/{r['share_n']} | {r['share_value']:.1%} | {r['aggregate_coverage']:.2f} |" for r in pop]
    by_rule = group_by(pop, lambda r: r["rule"])
    L.append("\n| Rule | Share at a loss: median of 6 CF schedules | lowest non-zero-fee schedule | highest | zero-fee schedule | Aggregate coverage, median |\n|---|---|---|---|---|---|")
    for k, v in by_rule.items():
        nz = [r["share_value"] for r in v if r["aggregate_coverage"] > 0]
        L.append(f"| {k} | {median([r['share_value'] for r in v]):.1%} | {min(nz):.1%} | {max(nz):.1%} | "
                 f"{max(r['share_value'] for r in v):.1%} | {median([r['aggregate_coverage'] for r in v]):.2f} |")
    return "\n".join(L)


def run_pool(root: str) -> int:
    census, tail_rows, cost_rows = read_csv(root, CENSUS), read_csv(root, TAIL), read_csv(root, COST)
    sch = schedules(census)
    errs = engine_check(sch["main"] + sch["pre"])
    if errs:
        print("ENGINE MISMATCH:\n" + "\n".join(errs))
        return 1
    print(f"Engine check: {len(sch['main']) + len(sch['pre'])} schedules reproduce the census bps at $25k/$100k/$500k.")
    frame = tail_frame(tail_rows)
    flat_sched, meta = pool_rows(frame, sch)
    cidx = cost_index(cost_rows)
    cov = tuple(coverage_row(s, cidx.get(s["ein"])) for s in sch["main"] + sch["alt"] + sch["pre"])
    pop = population_rows(cost_rows, {f["ein"]: f for f in frame}, sch["cf"])
    rows = tuple({k: fmt(v) for k, v in r.items()} for r in flat_sched + cov + pop)
    write_csv(root, OUT, rows, FIELDS)
    print(render(meta, flat_sched, cov, pop, frame))
    print(f"\nWrote {OUT} ({len(rows)} rows).")
    return 0


# ----------------------------------------------------------------------------- correction check
def parse_corrections(note_text: str) -> tuple[dict, ...]:
    sec = note_text.split("## Exact corrections", 1)[1].split("\n## ", 1)[0]
    blocks = re.split(r"^### `([^`]+)`\s*$", sec, flags=re.M)[1:]
    pairs = tuple(zip(blocks[0::2], blocks[1::2]))
    pat = re.compile(r"\*\*Find:\*\*\s*\n```text\n(.*?)\n```\s*\n\s*-?\s*\*\*Replace with:\*\*\s*\n```text\n(.*?)\n```", re.S)
    return tuple(dict(path=p, find=m.group(1), replace=m.group(2)) for p, body in pairs for m in pat.finditer(body))


def check_corrections(root: str) -> int:
    with open(os.path.join(root, NOTE), encoding="utf-8") as fh:
        corr = parse_corrections(fh.read())
    texts = {p: open(os.path.join(root, p), encoding="utf-8").read() for p in {c["path"] for c in corr}}
    def check(c):
        n = texts[c["path"]].count(c["find"])
        return (f"{'OK ' if n == 1 and c['replace'].endswith(TAG) else 'BAD'} count={n} "
                f"tag={'yes' if c['replace'].endswith(TAG) else 'NO'} {c['path']}: {c['find'][:70]!r}"), n == 1 and c["replace"].endswith(TAG)
    results = tuple(map(check, corr))
    def apply(acc, c):
        t = acc[0].get(c["path"])
        ok = t.count(c["find"]) == 1
        return ({**acc[0], c["path"]: t.replace(c["find"], c["replace"], 1) if ok else t}, acc[1] and ok)
    _, seq_ok = reduce(apply, corr, (texts, True))
    print("\n".join(r[0] for r in results))
    good = all(r[1] for r in results) and seq_ok and bool(corr)
    print(f"\n{sum(r[1] for r in results)}/{len(corr)} corrections pass; sequential in-memory application "
          f"{'succeeds' if seq_ok else 'FAILS'}; {len(texts)} files. No file was written.")
    return 0 if good else 1


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root")
    ap.add_argument("--task", choices=("pool", "check-corrections"), default="pool")
    a = ap.parse_args(argv)
    return run_pool(a.root) if a.task == "pool" else check_corrections(a.root)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
