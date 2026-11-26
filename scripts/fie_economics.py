#!/usr/bin/env python3
"""File-ingestion and straight-through-processing (STP) economics model, version 2.

Research package: research/file-ingestion-and-straight-through-processing/ (2026-11-26).
Inputs:  data/file-ingestion-2026-11/workflow-inventory.csv   (volume drivers, conventional minutes, decision floor,
                                                               driver and basis labels)
         data/file-ingestion-2026-11/economics-parameters.csv (every parameter labelled measured/sourced/assumed/
                                                               scenario/decision)
Outputs: data/file-ingestion-2026-11/economics-results.csv    (annual, steady state, one sponsor)
         data/file-ingestion-2026-11/economics-onboarding.csv (marginal onboarding cost of one institution)

Design: pure functions over immutable tuples/dicts; file I/O only in main(). Deterministic: low / mode / high cost
cases are evaluated explicitly instead of sampled. Version 2 follows adversarial review R3 (see RESEARCH-LEDGER.md):

  * Units. Data files count records (or files when a workflow has no record driver); evidence documents count documents (fixed + per-fund files + per-fund
    records). Grant-driven rows scale with grants per fund; advisor-managed custody rows with advisor-managed
    funds (monthly reconciliation unit).
  * Human work per automatable unit: intrinsic investigations (class-specific share x minutes per investigation),
    routine touches (units not processed straight through) and file-level exceptions (a separate, rarer share of
    data files). Policy-mandated decisions (human_decision_floor) sit outside STP.
  * No free cost cliff. Investigations fall only in an explicit prevention scenario that carries its own cost per
    fund; `stp_rate` applies to routine (non-investigation) processing only. A dashboard-definition STP (units with
    no human action / all units) is reported beside it.
  * Balance is a separate dimension: revenue shares are reported for $50k, $150k and $300k books in every row.
  * Fixed costs: run cost per sponsor and onboarding of the sponsor's institutions amortised over its life, in two
    variants: pooled (a multi-tenant operator reusing profiles) and standalone (bespoke integrations and a minimum
    staffing floor, because dual control cannot be staffed below two people).
  * Migration is one-off and excluded from the annual model.

It measures nothing: handling times and volumes are assumptions (gaps G1, G2). Ingestion cost is a *slice* of a
sponsor's operating cost; do not add it to the staffing models in research/ai-native-daf-enterprise, which already
include exception and reconciliation labour.

Usage:  python3 -I -B scripts/fie_economics.py [--check]
"""
from __future__ import annotations

import csv
import io
import sys
from functools import reduce
from pathlib import Path
from typing import Iterable, Mapping, Sequence, Tuple

DATA = Path("data/file-ingestion-2026-11")
INVENTORY = DATA / "workflow-inventory.csv"
PARAMETERS = DATA / "economics-parameters.csv"
RESULTS = DATA / "economics-results.csv"
ONBOARDING = DATA / "economics-onboarding.csv"

FUND_COUNTS = (1_000, 10_000, 50_000, 100_000, 500_000, 1_000_000)
STP_RATES = (0.50, 0.75, 0.90, 0.95, 0.99)          # routine (non-investigation) straight-through rate
PREVENTION = ("none", "scenario")                    # share of investigations prevented upstream: 0 or prevention_share
CASES = ("low", "mode", "high")
BALANCES = (50_000, 150_000, 300_000)
EXCLUDED_DISPOSITIONS = ("eliminate-file", "merge")  # redesigned away: no inbound artifact remains
ONE_OFF_DOMAINS = ("migration",)                     # not annual
INPUT_BASIS = "handling times, volumes and investigation shares assumed; cloud prices measured; grants per fund sourced"

Row = Mapping[str, str]
Params = Mapping[str, float]


def read_csv(path: Path) -> Tuple[Row, ...]:
    with path.open(newline="", encoding="utf-8") as f:
        return tuple(csv.DictReader(f))


def params_for(rows: Iterable[Row], case: str) -> Params:
    return {r["parameter"]: float(r[case]) for r in rows}


def active(inventory: Iterable[Row]) -> Tuple[Row, ...]:
    return tuple(r for r in inventory
                 if r["redesign_disposition"] not in EXCLUDED_DISPOSITIONS and r["domain"] not in ONE_OFF_DOMAINS)


def is_document(row: Row) -> bool:
    return row["artifact_class"] == "evidence-document"


def uses_ai(row: Row) -> bool:
    return row["ai_applicability"].split(" ")[0] in ("medium", "high")


def driver_units(row: Row, funds: int, p: Params) -> float:
    """Annual count of the row's volume driver for a sponsor of `funds` funds."""
    return {
        "fund": float(funds),
        "grant": funds * p["grants_per_fund"],
        "advisor-managed-fund": funds * p["advisor_managed_share"],
    }[row["scales_with"]]


def annual_volume(row: Row, funds: int, p: Params) -> Tuple[float, float]:
    """(files, records) per year for one workflow at one sponsor."""
    files = float(row["files_per_year_fixed"]) + float(row["files_per_fund_per_year"]) * funds
    records = float(row["records_per_fund_per_year"]) * driver_units(row, funds, p)
    return files, records


def investigation_share(row: Row, p: Params) -> float:
    return p["investigation_share_observation"] if row["artifact_class"] == "observation-set" else p["investigation_share_other"]


def workflow_costs(row: Row, funds: int, stp: float, prevention: float, p: Params) -> Mapping[str, float]:
    files, records = annual_volume(row, funds, p)
    # Every document is a unit of review; for data files the unit is the record, or the file itself when the
    # workflow has no per-record driver (configuration files, journal batches) so decisions are never silently zero.
    units = files + records if is_document(row) else (records if records > 0 else files)
    unit_minutes = float(row["conventional_minutes_per_record"])
    decisions = units * float(row["human_decision_floor"])
    automatable = units - decisions
    intrinsic = automatable * investigation_share(row, p)
    investigations = intrinsic * (1.0 - prevention)
    touches = (automatable - investigations) * (1.0 - stp)     # prevented investigations become routine units
    data_files = 0.0 if is_document(row) else files
    file_exceptions = data_files * p["file_exception_share"]
    assist = p["ai_assist_factor"] if uses_ai(row) else 1.0
    conv_minutes = (units * unit_minutes + intrinsic * p["minutes_per_exception"]
                    + data_files * float(row["conventional_minutes_per_file"]))
    residual_minutes = (decisions * unit_minutes * assist + investigations * p["minutes_per_exception"]
                        + touches * unit_minutes + file_exceptions * p["minutes_per_file_exception"])
    megabytes = files * (p["mb_per_document"] if is_document(row) else p["mb_per_data_file"])
    pages = units * p["pages_per_document"] if (is_document(row) and uses_ai(row)) else 0.0
    return {
        "files": files, "records": records, "units": units, "decisions": decisions,
        "human_units": decisions + investigations + touches, "file_exceptions": file_exceptions,
        "conventional_hours": conv_minutes / 60.0, "residual_hours": residual_minutes / 60.0,
        "gb": megabytes / 1024.0, "objects": files, "ai_pages": pages,
    }


def add(a: Mapping[str, float], b: Mapping[str, float]) -> Mapping[str, float]:
    return {k: a.get(k, 0.0) + b.get(k, 0.0) for k in set(a) | set(b)}


def totals(inventory: Sequence[Row], funds: int, stp: float, prevention: float, p: Params) -> Mapping[str, float]:
    return reduce(add, (workflow_costs(r, funds, stp, prevention, p) for r in inventory), {})


def labour(hours: float, p: Params) -> float:
    return hours / p["productive_hours_per_fte"] * p["loaded_cost_per_fte"]


def metered_cloud(t: Mapping[str, float], p: Params) -> float:
    storage = t["gb"] * p["retention_years"] * p["storage_usd_per_gb_month"] * 12.0
    scanning = t["gb"] * p["scan_usd_per_gb"] + t["objects"] / 1000.0 * p["scan_usd_per_1000_objects"]
    ai = t["ai_pages"] / 1000.0 * p["ai_usd_per_1000_pages"] * p["ai_passes_per_page"]
    return storage + scanning + ai


def onboarding_day_usd(p: Params) -> float:
    return p["loaded_cost_per_fte"] / p["productive_hours_per_fte"] * 8.0


def fixed_costs(p: Params, standalone: bool) -> float:
    """Annual fixed cost per sponsor: run cost plus onboarding of its institutions amortised over its life."""
    days = p["onboarding_days_bespoke"] if standalone else p["onboarding_days_reused_profile"]
    onboarding = p["institutions_per_sponsor"] * days * onboarding_day_usd(p) / p["amortisation_years"]
    return p["run_cost_per_sponsor_usd"] + onboarding


def shares(prefix: str, cost: float, funds: int, p: Params) -> Mapping[str, float]:
    return {f"{prefix}_share_of_20bps_at_{b // 1000}k": round(cost / (funds * b * p["servicing_fee_bps"] / 10_000.0), 4)
            for b in BALANCES}


def scenario(inventory: Sequence[Row], funds: int, stp: float, prevention_label: str, case: str, p: Params) -> Mapping[str, object]:
    prevention = p["prevention_share"] if prevention_label == "scenario" else 0.0
    t = totals(inventory, funds, stp, prevention, p)
    residual_fte = t["residual_hours"] / p["productive_hours_per_fte"]
    residual = labour(t["residual_hours"], p)
    cloud = metered_cloud(t, p)
    prevention_cost = funds * p["prevention_cost_per_fund_usd"] if prevention else 0.0
    pooled = residual + cloud + prevention_cost + fixed_costs(p, standalone=False)
    standalone = (max(residual_fte, p["standalone_min_fte"]) * p["loaded_cost_per_fte"] + cloud + prevention_cost
                  + fixed_costs(p, standalone=True))
    conventional = labour(t["conventional_hours"], p)
    return {
        "funds": funds, "stp_rate": stp, "prevention": prevention_label, "case": case,
        "records_per_year": round(t["records"]), "files_per_year": round(t["files"]), "units_per_year": round(t["units"]),
        "human_units_per_year": round(t["human_units"]), "policy_decisions_per_year": round(t["decisions"]),
        "dashboard_stp": round(1.0 - t["human_units"] / t["units"], 4) if t["units"] else 0.0,
        "conventional_fte": round(t["conventional_hours"] / p["productive_hours_per_fte"], 1),
        "residual_fte": round(residual_fte, 1),
        "conventional_labour_usd": round(conventional), "residual_labour_usd": round(residual),
        "metered_cloud_usd": round(cloud), "prevention_usd": round(prevention_cost),
        "pooled_cost_usd": round(pooled), "standalone_cost_usd": round(standalone),
        "pooled_cost_per_fund_usd": round(pooled / funds, 2), "standalone_cost_per_fund_usd": round(standalone / funds, 2),
        **shares("pooled", pooled, funds, p),
        **shares("standalone", standalone, funds, p),
        "residual_cost_per_human_unit_usd": round(residual / (t["human_units"] + t["file_exceptions"]), 2) if t["human_units"] else 0.0,
        "input_basis": INPUT_BASIS,
    }


def onboarding_rows(p_rows: Sequence[Row]) -> Tuple[Mapping[str, object], ...]:
    def row(case: str) -> Mapping[str, object]:
        p = params_for(p_rows, case)
        day = onboarding_day_usd(p)
        return {
            "case": case,
            "bespoke_days": p["onboarding_days_bespoke"], "bespoke_usd": round(p["onboarding_days_bespoke"] * day),
            "new_profile_days": p["onboarding_days_new_profile"], "new_profile_usd": round(p["onboarding_days_new_profile"] * day),
            "reused_profile_days": p["onboarding_days_reused_profile"], "reused_profile_usd": round(p["onboarding_days_reused_profile"] * day),
            "shadow_run_days_elapsed": p["shadow_run_business_days"],
            "input_basis": "engineer-days assumed; anchored on vendor-reported EDI onboarding time",
        }
    return tuple(row(c) for c in CASES)


def render(rows: Sequence[Mapping[str, object]]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def compute() -> Tuple[str, str]:
    inventory = active(read_csv(INVENTORY))
    p_rows = read_csv(PARAMETERS)
    results = tuple(scenario(inventory, n, s, v, c, params_for(p_rows, c))
                    for c in CASES for v in PREVENTION for n in FUND_COUNTS for s in STP_RATES)
    return render(results), render(onboarding_rows(p_rows))


def main(argv: Sequence[str]) -> int:
    results, onboarding = compute()
    if "--check" in argv:
        stale = [str(p) for p, text in ((RESULTS, results), (ONBOARDING, onboarding))
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        print("stale: " + ", ".join(stale) if stale else "economics outputs current")
        return 1 if stale else 0
    RESULTS.write_text(results, encoding="utf-8")
    ONBOARDING.write_text(onboarding, encoding="utf-8")
    print(f"wrote {RESULTS} and {ONBOARDING}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
