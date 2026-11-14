#!/usr/bin/env python3
"""P-COST-02: test the AI model's loaded labour rates against Form 990 Part IX salaries per employee.

The AI-economics model prices process labour at BLS May 2025 median wages grossed up by the ECEC June 2026
compensation/wage ratio (1.4287): customer service $21.53 -> $30.76/h, bookkeeping $24.36 -> $34.80/h,
compliance $38.81 -> $55.45/h (research/mission-2026-11-14/ai-economics-replacement-analysis.md).
This script compares them with what sponsors actually pay per W-2 employee:

  wage_l7_per_emp      = Part IX line 7 (other salaries and wages) / Part I line 5 (TotalEmployeeCnt)
                         -> lower bound for non-officer pay (paid officers sit in the denominator, not numerator)
  wage_all_per_emp     = lines 5+6+7 / employees  -> all W-2 pay incl. officers (upper bound for staff pay)
  loaded_all_per_emp   = lines 5..10 / employees  -> wages + pension + benefits + payroll tax
  load_factor          = lines 5..10 / lines 5..7 -> observed benefits gross-up, compare with ECEC 1.4287
Hourly figures divide by 2,080 h (one FTE). Part I line 5 counts every W-2 employee in the calendar year,
including part-time and seasonal staff, so per-head figures understate FTE pay (bias is downward).

Inputs (read only):
  data/mission-2026-11-14/sponsor-cost-structure.csv   (one row per parsed sponsor return; category, size band)
  CACHE/extract990cost/{object_id}.json                (Part IX line detail cached by mission_sponsor_cost_structure.py)
Output:
  data/mission-2026-11-14/sponsor-salary-per-employee.csv  record_type = return | summary | model_rate

Usage:  python3 scripts/mission_labour_rate_check.py --cache-dir CACHE
Stdlib only; functional style.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as m990  # noqa: E402

DATA = m990.DATA
COST_CSV = os.path.join(DATA, "sponsor-cost-structure.csv")
OUT = os.path.join(DATA, "sponsor-salary-per-employee.csv")
HOURS = 2080.0
ECEC_FACTOR = 46.89 / 32.82  # BLS ECEC June 2026, private industry: total comp / wages
MODEL = (  # (label, BLS May 2025 median wage $/h, model loaded $/h, source)
    ("customer_service", 21.53, 30.76, "https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm"),
    ("bookkeeping", 24.36, 34.80, "https://www.bls.gov/ooh/office-and-administrative-support/bookkeeping-accounting-and-auditing-clerks.htm"),
    ("compliance", 38.81, 55.45, "https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm"),
)
LINES = ("l05_comp_officers_directors", "l06_comp_disqualified", "l07_other_salaries_wages",
         "l08_pension", "l09_other_benefits", "l10_payroll_taxes")
MIN_EMP_STAFFED = 5
num, fmt, read_csv, write_csv = m990.num, m990.fmt, m990.read_csv, m990.write_csv


def div(a, b):
    return a / b if a is not None and b not in (None, 0) else None


def quantile(xs: Sequence[float], q: float):
    s = sorted(xs)
    if not s:
        return None
    i = (len(s) - 1) * q
    lo, hi = int(i), min(int(i) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (i - lo)


def load_extract(cache_dir: str, oid: str) -> dict:
    path = os.path.join(cache_dir, "extract990cost", f"{oid}.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def line_total(x: Mapping, key: str) -> float:
    return ((x.get("part_ix") or {}).get(key) or {}).get("total") or 0.0


def flags(emp, w7, wall) -> str:
    out = ()
    out += ("employees_lt_5",) if emp is not None and emp < MIN_EMP_STAFFED else ()
    out += ("no_line7",) if not w7 else ()
    out += ("wage_lt_20k_parttime_heavy",) if wall is not None and wall < 20000 else ()
    out += ("wage_gt_300k_outlier",) if wall is not None and wall > 300000 else ()
    return ";".join(out)


def return_row(r: Mapping, x: Mapping) -> dict:
    ln = {k: line_total(x, k) for k in LINES}
    emp = num(((x.get("part_i") or {}).get("TotalEmployeeCnt"))) if x else num(r.get("employees"))
    wages = ln["l05_comp_officers_directors"] + ln["l06_comp_disqualified"] + ln["l07_other_salaries_wages"]
    loaded = wages + ln["l08_pension"] + ln["l09_other_benefits"] + ln["l10_payroll_taxes"]
    w7 = div(ln["l07_other_salaries_wages"], emp)
    wall = div(wages, emp)
    lall = div(loaded, emp)
    return {"record_type": "return", "ein": r["ein"], "sponsor_name": r["sponsor_name"], "category": r["category"],
            "size_band_daf_assets": r["size_band_daf_assets"], "fiscal_year": r["fiscal_year"],
            "employees": emp, **ln, "wages_l5_7": wages, "loaded_l5_10": loaded,
            "wage_l7_per_emp": w7, "wage_all_per_emp": wall, "loaded_all_per_emp": lall,
            "wage_l7_hourly": div(w7, HOURS), "wage_all_hourly": div(wall, HOURS), "loaded_all_hourly": div(lall, HOURS),
            "load_factor": div(loaded, wages), "officer_share_of_wages": div(ln["l05_comp_officers_directors"], wages),
            "flags": flags(emp, ln["l07_other_salaries_wages"], wall),
            "return_object_id": r["return_object_id"], "source_url": r["source_url"]}


def staffed(row: Mapping) -> bool:
    return (row["employees"] or 0) >= MIN_EMP_STAFFED and row["l07_other_salaries_wages"] > 0 \
        and "outlier" not in row["flags"]


def latest_per_ein(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    best: dict = {}
    for r in rows:  # pick max fiscal_year per EIN (pure in effect: local accumulator)
        if r["ein"] not in best or int(r["fiscal_year"]) > int(best[r["ein"]]["fiscal_year"]):
            best[r["ein"]] = r
    return tuple(best.values())


def summary(rows: Sequence[Mapping], scope: str, category: str, band: str) -> dict:
    def q(metric, p):
        return quantile(tuple(r[metric] for r in rows if r[metric] is not None), p)
    emp = sum(r["employees"] for r in rows)
    pooled = lambda k: div(sum(r[k] for r in rows), emp)  # noqa: E731
    pooled_l7 = div(sum(r["l07_other_salaries_wages"] for r in rows), emp)
    lf = tuple(r["load_factor"] for r in rows if r["load_factor"])
    out = {"record_type": "summary", "scope": scope, "category": category, "size_band_daf_assets": band,
           "n_returns": len(rows), "employees": emp,
           "wage_l7_hourly_p25": div(q("wage_l7_per_emp", .25), HOURS),
           "wage_l7_hourly_p50": div(q("wage_l7_per_emp", .5), HOURS),
           "wage_l7_hourly_p75": div(q("wage_l7_per_emp", .75), HOURS),
           "wage_all_hourly_p50": div(q("wage_all_per_emp", .5), HOURS),
           "loaded_all_hourly_p25": div(q("loaded_all_per_emp", .25), HOURS),
           "loaded_all_hourly_p50": div(q("loaded_all_per_emp", .5), HOURS),
           "loaded_all_hourly_p75": div(q("loaded_all_per_emp", .75), HOURS),
           "wage_l7_hourly_pooled": div(pooled_l7, HOURS),
           "loaded_all_hourly_pooled": div(pooled("loaded_l5_10"), HOURS),
           "load_factor_p50": statistics.median(lf) if lf else None,
           "share_loaded_below_30_76": div(sum(1 for r in rows if r["loaded_all_hourly"] is not None and r["loaded_all_hourly"] < 30.76), len(rows)),
           "share_loaded_above_55_45": div(sum(1 for r in rows if r["loaded_all_hourly"] is not None and r["loaded_all_hourly"] > 55.45), len(rows))}
    return out


def summaries(rows: Sequence[Mapping], scope: str) -> tuple[dict, ...]:
    cats = sorted({r["category"] for r in rows})
    bands = sorted({r["size_band_daf_assets"] for r in rows})
    by_cat = tuple(summary(tuple(r for r in rows if r["category"] == c), scope, c, "all") for c in cats)
    by_band = tuple(summary(tuple(r for r in rows if r["size_band_daf_assets"] == b), scope, "all", b) for b in bands)
    cross = tuple(summary(sub, scope, c, b) for c in cats for b in bands
                  for sub in (tuple(r for r in rows if r["category"] == c and r["size_band_daf_assets"] == b),)
                  if len(sub) >= 5)
    return (summary(tuple(rows), scope, "all", "all"),) + by_cat + by_band + cross


def model_rows() -> tuple[dict, ...]:
    return tuple({"record_type": "model_rate", "scope": lbl, "wage_l7_hourly_p50": w, "loaded_all_hourly_p50": l,
                  "load_factor_p50": ECEC_FACTOR, "source_url": src} for lbl, w, l, src in MODEL)


FIELDS = ("record_type", "scope", "ein", "sponsor_name", "category", "size_band_daf_assets", "fiscal_year",
          "n_returns", "employees") + LINES + (
          "wages_l5_7", "loaded_l5_10", "wage_l7_per_emp", "wage_all_per_emp", "loaded_all_per_emp",
          "wage_l7_hourly", "wage_all_hourly", "loaded_all_hourly", "load_factor", "officer_share_of_wages",
          "wage_l7_hourly_p25", "wage_l7_hourly_p50", "wage_l7_hourly_p75", "wage_all_hourly_p50",
          "loaded_all_hourly_p25", "loaded_all_hourly_p50", "loaded_all_hourly_p75",
          "wage_l7_hourly_pooled", "loaded_all_hourly_pooled", "load_factor_p50",
          "share_loaded_below_30_76", "share_loaded_above_55_45", "flags", "return_object_id", "source_url")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", required=True)
    a = ap.parse_args(argv)
    cost = read_csv(COST_CSV)
    rets = tuple(return_row(r, load_extract(a.cache_dir, r["return_object_id"])) for r in cost)
    with_emp = tuple(r for r in rets if (r["employees"] or 0) > 0)
    st = tuple(r for r in with_emp if staffed(r))
    latest = latest_per_ein(st)
    out = model_rows() + summaries(latest, "latest_return_per_ein_staffed") + summaries(st, "all_fy2022_2025_staffed") \
        + tuple({**r, "scope": "return"} for r in sorted(with_emp, key=lambda r: (r["category"], r["ein"], r["fiscal_year"])))
    write_csv(OUT, out, FIELDS)
    print(f"returns={len(rets)} with_employees={len(with_emp)} staffed={len(st)} latest_eins={len(latest)} "
          f"missing_extract={sum(1 for r in cost if not os.path.exists(os.path.join(a.cache_dir, 'extract990cost', r['return_object_id'] + '.json')))}")
    for s in (x for x in out if x["record_type"] == "summary" and x["scope"].startswith("latest")
              and (x["size_band_daf_assets"] == "all" or x["category"] == "all")):
        print(s["category"], s["size_band_daf_assets"], s["n_returns"], s["employees"],
              *(fmt(round(s[k], 2)) if s[k] is not None else "" for k in
                ("wage_l7_hourly_p50", "wage_all_hourly_p50", "loaded_all_hourly_p25", "loaded_all_hourly_p50",
                 "loaded_all_hourly_p75", "loaded_all_hourly_pooled", "load_factor_p50",
                 "share_loaded_below_30_76", "share_loaded_above_55_45")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
