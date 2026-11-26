#!/usr/bin/env python3
"""Complaint rates per 10,000 grants for the FY2024 top-15 DAF sponsors and top-5 donation processors (P-G1913-02).

Stdlib only, functional style: pure transforms; I/O only in read_csv() and main().

Inputs   data/mission-2026-11-14/complaint-rates-2026-11-19.csv          numerators n by entity and scope (P-GAP19-13,
                                                                          window 2021-01-01..2026-11-19, dup_of removed)
         data/mission-2026-11-14/grant-count-denominators-2026-11-20.csv  grant counts (this task)
Choice   One denominator per entity:
           1. the row with is_primary = 1 (count_status 'stated' or 'derived'), else
           2. the largest lower bound (count_status 'lower_bound_recipients' or 'derived_lower_bound_schedule_i').
         A lower-bound denominator makes the rate an UPPER bound; it is labelled so in `rate_kind`.
Rates    window rate  = n / G x 10,000                    (n over ~5.9 years against a one-year grant count)
         annual rate  = n / window_years / G x 10,000     (the headline; assumes a stable grant base)
Interval exact (Garwood) two-sided 95% Poisson interval on n (poisson_ci from mission_complaint_rates_gap19.py),
         scaled by the same factor. Zero counts: lower bound 0, upper bound only.
Pooled   POOLED top15_sponsor: every top-15 sponsor with a primary count (zero-record sponsors included, because
         every sponsor's venues were checked). POOLED processor: lower-bound denominators, so an upper bound.
         Pooled n counts each record id once (a "big three" record matches three sponsors but is one complaint).
Note     Run with python3 -B so that importing mission_complaint_rates_gap19.py writes no bytecode.

Usage:   python3 scripts/mission_grant_count_rates.py [ROOT] [--force]       (ROOT defaults to the repo root)
Output:  data/mission-2026-11-14/complaint-rates-per-grant-2026-11-20.csv  (refuses to overwrite without --force)
"""
from __future__ import annotations

import csv
import importlib.util
import os
import sys
from typing import Mapping, Sequence

REL_DATA = os.path.join("data", "mission-2026-11-14")
RATES_IN = "complaint-rates-2026-11-19.csv"
DENOM_IN = "grant-count-denominators-2026-11-20.csv"
OUT_NAME = "complaint-rates-per-grant-2026-11-20.csv"
SCOPES = ("all_venues", "review_venues", "strict")
POINT_STATUSES = ("stated", "derived")
LOWER_STATUSES = ("lower_bound_recipients", "derived_lower_bound_schedule_i")
PER = 10_000


# ---------- I/O edge ----------
def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return tuple(csv.DictReader(fh))


def load_poisson_ci(root: str):
    """Reuse the exact Poisson interval already used for the per-account and per-$ rates."""
    path = os.path.join(root, "scripts", "mission_complaint_rates_gap19.py")
    spec = importlib.util.spec_from_file_location("mission_complaint_rates_gap19", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.poisson_ci


# ---------- pure helpers ----------
def fmt(x: float | None, nd: int = 4) -> str:
    return "" if x is None else f"{x:.{nd}f}"


def as_int(s: str) -> int | None:
    return int(s) if s and s.strip().isdigit() else None


def choose_denominator(rows: Sequence[Mapping]) -> Mapping | None:
    """Primary stated/derived row, else the largest lower bound, else None. Pure."""
    primary = tuple(r for r in rows if r["is_primary"] == "1" and r["count_status"] in POINT_STATUSES)
    lowers = sorted((r for r in rows if r["count_status"] in LOWER_STATUSES and as_int(r["grant_count"])),
                    key=lambda r: as_int(r["grant_count"]), reverse=True)
    return primary[0] if primary else (lowers[0] if lowers else None)


def rate_kind(n: int, den: Mapping | None) -> str:
    if den is None:
        return "not computed (no grant count or lower bound)"
    bound = den["count_status"] in LOWER_STATUSES
    if n == 0:
        return "zero records: upper bound only" + ("; denominator is a lower bound, so the bound is loose" if bound else "")
    return "upper bound (denominator is a lower bound on grants)" if bound else "point estimate"


def rate_cols(n: int, g: int | None, years: float, ci) -> dict:
    if not g:
        return {k: "" for k in ("rate_per_10k_grants_window", "window_ci95_low", "window_ci95_high",
                                "annual_rate_per_10k_grants", "annual_ci95_low", "annual_ci95_high")}
    lo, hi = ci(n)
    w = lambda v: v / g * PER
    a = lambda v: v / years / g * PER
    return {"rate_per_10k_grants_window": fmt(w(n)), "window_ci95_low": fmt(w(lo)), "window_ci95_high": fmt(w(hi)),
            "annual_rate_per_10k_grants": fmt(a(n)), "annual_ci95_low": fmt(a(lo)), "annual_ci95_high": fmt(a(hi))}


def entity_row(rate: Mapping, den: Mapping | None, ci) -> dict:
    n = int(rate["n_complaint_mixed"])
    years = float(rate["window_years"])
    g = as_int(den["grant_count"]) if den else None
    dollars = float(rate["fy2024_daf_grants_usd"]) if rate["fy2024_daf_grants_usd"] else None
    point = den is not None and den["count_status"] in POINT_STATUSES
    return {"entity": rate["entity"], "entity_group": rate["entity_group"], "ein": rate["ein"],
            "scope": rate["scope"], "window_years": years, "n_complaint_mixed": n,
            "grant_count": g or "", "denominator_status": den["count_status"] if den else "not_found",
            "denominator_period": den["period_label"] if den else "", "denominator_row_id": den["row_id"] if den else "",
            **rate_cols(n, g, years, ci), "rate_kind": rate_kind(n, den),
            "fy2024_daf_grants_usd": rate["fy2024_daf_grants_usd"],
            "implied_avg_grant_usd": fmt(dollars / g, 0) if (point and dollars and g) else "",
            "rate_per_1bn_grants_p_gap19_13": rate["rate_per_1bn_grants"],
            "rate_per_10k_accounts_p_gap19_13": rate["rate_per_10k_accounts"],
            "record_ids": rate["record_ids"]}


def pooled_row(label: str, group: str, scope: str, rows: Sequence[Mapping], ci, kind: str) -> dict:
    sel = tuple(r for r in rows if r["entity_group"] == group and r["scope"] == scope and r["grant_count"] != ""
                and (r["denominator_status"] in POINT_STATUSES) == (kind == "point"))
    # each record counted once even when it matches several entities ("big three" records)
    n = len({i for r in sel for i in r["record_ids"].split(";") if i})
    g = sum(int(r["grant_count"]) for r in sel)
    years = sel[0]["window_years"] if sel else 1.0
    return {"entity": f"POOLED {group} ({label}; {len(sel)} entities)", "entity_group": group, "ein": "",
            "scope": scope, "window_years": years, "n_complaint_mixed": n, "grant_count": g or "",
            "denominator_status": "sum of " + ("stated/derived counts" if kind == "point" else "lower bounds"),
            "denominator_period": "mixed (see entity rows)", "denominator_row_id": ";".join(r["denominator_row_id"] for r in sel),
            **rate_cols(n, g or None, years, ci),
            "rate_kind": "point estimate" if kind == "point" else "upper bound (denominators are lower bounds)",
            "fy2024_daf_grants_usd": "", "implied_avg_grant_usd": "", "rate_per_1bn_grants_p_gap19_13": "",
            "rate_per_10k_accounts_p_gap19_13": "", "record_ids": ""}


def build(rates: Sequence[Mapping], denoms: Sequence[Mapping], ci) -> tuple[dict, ...]:
    by_ein = {e: tuple(d for d in denoms if d["ein"] == e) for e in {d["ein"] for d in denoms}}
    chosen = {e: choose_denominator(rs) for e, rs in by_ein.items()}
    ent = tuple(entity_row(r, chosen.get(r["ein"]), ci) for r in rates
                if r["scope"] in SCOPES and not r["entity"].startswith("POOLED"))
    pooled = tuple(pooled_row(lbl, grp, s, ent, ci, kind)
                   for grp, lbl, kind in (("top15_sponsor", "sponsors with a stated or derived count", "point"),
                                          ("processor", "lower-bound denominators", "lower"))
                   for s in SCOPES)
    return ent + pooled


def main(argv: Sequence[str]) -> int:
    args = tuple(a for a in argv if not a.startswith("--"))
    root = os.path.abspath(args[0]) if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = os.path.join(root, REL_DATA)
    out = os.path.join(data, OUT_NAME)
    if os.path.exists(out) and "--force" not in argv:
        print(f"{out} exists; pass --force to rebuild it", file=sys.stderr)
        return 1
    rows = build(read_csv(os.path.join(data, RATES_IN)), read_csv(os.path.join(data, DENOM_IN)), load_poisson_ci(root))
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
