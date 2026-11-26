#!/usr/bin/env python3
"""Sponsor-level Canadian DAF panel from CRA T3010 open data (queue item P-B39N3-01).

Stdlib only; functional style (pure transforms, I/O at the edges, no mutable global state).

Source: CRA "List of charities" open-data releases on open.canada.ca (one dataset per year;
the year is the calendar year of the fiscal period end, FPE). Files used per year Y:
  {Y}_abc_financial_section_a_b_and_c_{Y}_updated.csv   Section C lines 5860-5864 (DAF lines)
  {Y}_ident_ident_{Y}_updated.csv                      legal name, designation, province
  {Y}_fin_financial_d_and_schedule_6_{Y}_updated.csv   line 4200 total assets, 4700 total revenue
Dataset pages (CKAN ids): 2023 05b3abd0-e70f-4b3b-a9c5-acc436bd15b6,
  2024 80c00cdb-1358-415c-bb8b-0de7f12675b8, 2025 4b60228a-2b78-45d3-8e05-f7150b8fe8d8
  https://open.canada.ca/data/en/dataset/<id>

T3010 DAF lines (CRA open-data dictionary v2.0, form version 27 = T3010 E (24)):
  5860 Y/N  Did the charity hold any donor advised funds (DAF) during the fiscal period?
  5861 n    Total number of accounts held at the end of the fiscal period
  5862 $    Total value of all accounts held at the end of the fiscal period
  5863 $    Total value of donations to DAF accounts received during the fiscal period
  5864 $    Total value of qualifying disbursements from DAFs during the fiscal period

Output: one row per (charity BN, dataset year) where line 5860 = Y. If a charity filed more than
one return with an FPE in the same calendar year, the latest FPE is kept and DUP_RETURN flagged.

Usage:
  python3 scripts/mission_canada_daf_panel.py . --data-dir DIR [--blumberg-txt FILE]
      [--out data/mission-2026-11-14/canada-daf-panel-2026-11-19.csv] [--summary FILE.json]
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import statistics
from functools import reduce
from typing import Iterable

YEARS = (2023, 2024, 2025)
DAF_LINES = ("5860", "5861", "5862", "5863", "5864")
DESIGNATION = {"A": "public foundation", "B": "private foundation", "C": "charitable organization"}
# Flags that make line 5861 (account count) unusable; the others are informational.
ACCOUNT_ERROR_FLAGS = frozenset({"ACC_EQ_DOLLAR", "ACC_GT_ASSETS", "AVG_LT_100", "ACC_NO_DOLLARS_LARGE"})

FIELDS = [
    "dataset_year", "bn", "fpe", "form_id", "legal_name", "account_name", "designation",
    "designation_label", "category_code", "province",
    "line_5860", "accounts_5861", "daf_assets_5862", "daf_donations_5863", "daf_disbursements_5864",
    "total_assets_4200", "total_revenue_4700", "n_returns_in_year",
    "avg_account", "payout_same_year", "prior_fpe", "prior_daf_assets_5862", "payout_on_prior_assets",
    "disbursements_to_donations", "daf_share_of_total_assets",
    "accounts_ge_10", "rank_assets_in_year", "flags", "accounts_clean",
]


# ---------- pure helpers ----------
def num(v: str | None) -> float | None:
    v = (v or "").strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def ratio(a: float | None, b: float | None) -> float | None:
    return None if a is None or not b else a / b


def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() and abs(v) < 1e15 else f"{v:.4f}"
    return str(v)


def strip_keys(row: dict) -> dict:
    return {(k or "").strip(): v for k, v in row.items()}


def latest_by_bn(rows: Iterable[dict]) -> dict:
    """BN -> (latest row by FPE, count of returns with an FPE in the year)."""
    def step(acc: dict, r: dict) -> dict:
        prev, n = acc.get(r["BN"], (None, 0))
        keep = r if prev is None or r["FPE"] >= prev["FPE"] else prev
        return {**acc, r["BN"]: (keep, n + 1)}
    return reduce(step, rows, {})


def flags_for(r: dict) -> list[str]:
    acc, ast, don, dis = r["accounts_5861"], r["daf_assets_5862"], r["daf_donations_5863"], r["daf_disbursements_5864"]
    tot = r["total_assets_4200"]
    dollars = [x for x in (ast, don, dis) if x]
    other_dollars = [x for x in (tot, r["total_revenue_4700"]) if x]
    avg = ratio(ast, acc)
    checks = [
        # account count equals a dollar figure on the same return (DAF lines or total assets/revenue)
        ("ACC_EQ_DOLLAR", bool(acc) and acc > 1 and acc in dollars + other_dollars),
        ("ACC_GT_ASSETS", bool(acc) and bool(ast) and acc > ast),  # incl. negative DAF assets
        ("AVG_LT_100", avg is not None and 0 < avg < 100),
        ("ACC_NO_DOLLARS_LARGE", bool(acc) and acc >= 100 and not dollars),
        ("ACC_NO_DOLLARS", bool(acc) and acc < 100 and not dollars),
        ("DOLLARS_NO_ACC", bool(dollars) and not acc),
        ("ALL_BLANK", acc is None and ast is None and don is None and dis is None),
        ("ASSETS_GT_TOTAL", bool(ast) and bool(tot) and ast > 1.05 * tot),
        ("PAYOUT_GT_100", bool(ast) and bool(dis) and dis > ast),
        ("DUP_RETURN", r["n_returns_in_year"] > 1),
    ]
    return [name for name, hit in checks if hit]


# ---------- I/O ----------
def read_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [strip_keys(r) for r in csv.DictReader(fh)]


def find(data_dir: str, year: int, kind: str) -> str:
    hits = sorted(glob.glob(os.path.join(data_dir, f"{year}_{kind}_*.csv")))
    if not hits:
        raise SystemExit(f"missing {kind} file for {year} in {data_dir}")
    return hits[0]


def load_year(data_dir: str, year: int) -> list[dict]:
    abc = [r for r in read_csv(find(data_dir, year, "abc")) if r.get("5860") == "Y"]
    latest = latest_by_bn(abc)
    bns = set(latest)
    ident = {r["BN"]: r for r in read_csv(find(data_dir, year, "ident")) if r["BN"] in bns}
    fin = {(r["BN"], r["FPE"]): r for r in read_csv(find(data_dir, year, "fin")) if r["BN"] in bns}

    def build(bn: str) -> dict:
        r, n = latest[bn]
        i = ident.get(bn, {})
        f = fin.get((bn, r["FPE"]), {})
        return {
            "dataset_year": year, "bn": bn, "fpe": r["FPE"], "form_id": r.get("Form ID", ""),
            "legal_name": i.get("Legal Name", ""), "account_name": i.get("Account Name", ""),
            "designation": i.get("Designation", ""),
            "designation_label": DESIGNATION.get(i.get("Designation", ""), ""),
            "category_code": i.get("Category", ""), "province": i.get("Province", ""),
            "line_5860": r["5860"], "accounts_5861": num(r.get("5861")),
            "daf_assets_5862": num(r.get("5862")), "daf_donations_5863": num(r.get("5863")),
            "daf_disbursements_5864": num(r.get("5864")),
            "total_assets_4200": num(f.get("4200")), "total_revenue_4700": num(f.get("4700")),
            "n_returns_in_year": n,
        }
    return [build(bn) for bn in sorted(bns)]


# ---------- panel transforms ----------
def enrich(rows: list[dict]) -> list[dict]:
    prior = {(r["dataset_year"], r["bn"]): r for r in rows}
    rank = {
        (r["dataset_year"], r["bn"]): i + 1
        for y in YEARS
        for i, r in enumerate(sorted((x for x in rows if x["dataset_year"] == y),
                                     key=lambda x: -(x["daf_assets_5862"] or 0)))
    }

    def one(r: dict) -> dict:
        p = prior.get((r["dataset_year"] - 1, r["bn"]))
        fl = flags_for(r)
        return {
            **r,
            "avg_account": ratio(r["daf_assets_5862"], r["accounts_5861"]),
            "payout_same_year": ratio(r["daf_disbursements_5864"], r["daf_assets_5862"]),
            "prior_fpe": p["fpe"] if p else None,
            "prior_daf_assets_5862": p["daf_assets_5862"] if p else None,
            "payout_on_prior_assets": ratio(r["daf_disbursements_5864"], p["daf_assets_5862"]) if p else None,
            "disbursements_to_donations": ratio(r["daf_disbursements_5864"], r["daf_donations_5863"]),
            "daf_share_of_total_assets": ratio(r["daf_assets_5862"], r["total_assets_4200"]),
            "accounts_ge_10": bool(r["accounts_5861"]) and r["accounts_5861"] >= 10,
            "rank_assets_in_year": rank[(r["dataset_year"], r["bn"])],
            "flags": ";".join(fl),
            "accounts_clean": not (ACCOUNT_ERROR_FLAGS & set(fl)),
        }
    return [one(r) for r in rows]


def total(rows: Iterable[dict], key: str) -> float:
    return sum((r[key] or 0) for r in rows)


def concentration(rows: list[dict], key: str = "daf_assets_5862") -> dict:
    vals = sorted(((r[key] or 0) for r in rows), reverse=True)
    t = sum(vals) or 1.0
    return {
        "n": len(vals), "total": sum(vals),
        **{f"top{k}_share": sum(vals[:k]) / t for k in (1, 3, 5, 10, 20)},
        "hhi": sum((v / t * 100) ** 2 for v in vals),
    }


def payout_measures(rows: list[dict]) -> dict:
    with_assets = [r for r in rows if (r["daf_assets_5862"] or 0) > 0]
    per = [r["payout_same_year"] for r in with_assets if r["payout_same_year"] is not None]
    matched = [r for r in rows if r["prior_daf_assets_5862"]]
    big = [r for r in with_assets if r["daf_assets_5862"] >= 10_000_000]
    return {
        "aggregate_same_year_5864_over_5862": ratio(total(rows, "daf_disbursements_5864"), total(rows, "daf_assets_5862")),
        "median_sponsor_same_year": statistics.median(per) if per else None,
        "median_sponsor_same_year_assets_ge_10m": statistics.median(
            [r["payout_same_year"] for r in big if r["payout_same_year"] is not None]) if big else None,
        "n_matched_prior_year": len(matched),
        "aggregate_on_prior_year_assets_matched": ratio(total(matched, "daf_disbursements_5864"),
                                                        total(matched, "prior_daf_assets_5862")),
        "disbursements_to_donations": ratio(total(rows, "daf_disbursements_5864"), total(rows, "daf_donations_5863")),
        "share_sponsors_payout_ge_5pct": (sum(1 for x in per if x >= 0.05) / len(per)) if per else None,
    }


def year_summary(rows: list[dict], y: int) -> dict:
    yr = [r for r in rows if r["dataset_year"] == y]
    clean = [r for r in yr if r["accounts_clean"]]
    flag_counts = reduce(lambda acc, f: {**acc, f: acc.get(f, 0) + 1},
                         (f for r in yr for f in r["flags"].split(";") if f), {})
    acc_err = [r for r in yr if not r["accounts_clean"]]
    return {
        "year": y, "charities_5860_Y": len(yr),
        "fpe_min": min(r["fpe"] for r in yr), "fpe_max": max(r["fpe"] for r in yr),
        "accounts_5861": total(yr, "accounts_5861"), "accounts_5861_clean": total(clean, "accounts_5861"),
        "accounts_in_flagged_rows": total(acc_err, "accounts_5861"), "n_account_flag_rows": len(acc_err),
        "daf_assets_5862": total(yr, "daf_assets_5862"), "daf_donations_5863": total(yr, "daf_donations_5863"),
        "daf_disbursements_5864": total(yr, "daf_disbursements_5864"),
        "avg_account_all": ratio(total(yr, "daf_assets_5862"), total(yr, "accounts_5861")),
        "avg_account_clean": ratio(total(clean, "daf_assets_5862"), total(clean, "accounts_5861")),
        "n_with_assets_gt0": sum(1 for r in yr if (r["daf_assets_5862"] or 0) > 0),
        "flag_counts": flag_counts,
        "concentration_assets": concentration(yr),
        "payout": payout_measures(yr),
        "top15": [{k: r[k] for k in ("rank_assets_in_year", "bn", "legal_name", "designation", "accounts_5861",
                                     "daf_assets_5862", "daf_donations_5863", "daf_disbursements_5864",
                                     "payout_same_year", "payout_on_prior_assets", "flags")}
                  for r in sorted(yr, key=lambda r: r["rank_assets_in_year"])[:15]],
    }


def describe(sel: list[dict]) -> dict:
    return {
        "n": len(sel), "accounts": total(sel, "accounts_5861"), "daf_assets": total(sel, "daf_assets_5862"),
        "donations": total(sel, "daf_donations_5863"), "disbursements": total(sel, "daf_disbursements_5864"),
        "concentration": concentration(sel),
        "n_from_2025_release": sum(1 for r in sel if r["dataset_year"] == 2025),
    }


def wellfunded_replica(rows: list[dict]) -> dict:
    """WellFunded's stated rule: latest filing per BN (FYE 2024 or 2025), line 5860 = Y, >= 10 accounts.
    Variants show how far account-count errors and the 2024 carry-overs move the result."""
    latest = reduce(lambda acc, r: {**acc, r["bn"]: r} if r["dataset_year"] in (2024, 2025) and (
        r["bn"] not in acc or r["fpe"] > acc[r["bn"]]["fpe"]) else acc, rows, {})
    lv = list(latest.values())
    return {
        "stated_rule": describe([r for r in lv if r["accounts_ge_10"]]),
        "stated_rule_excl_account_errors": describe([r for r in lv if r["accounts_ge_10"] and r["accounts_clean"]]),
        "release_2025_only_ge10_clean": describe([r for r in rows if r["dataset_year"] == 2025
                                                  and r["accounts_ge_10"] and r["accounts_clean"]]),
        "latest_any_accounts": describe(lv),
    }


def blumberg_match(rows: list[dict], text: str) -> dict:
    """Which 2024 rows' line-5862 values appear verbatim ($1,234 form) in the Blumberg-Pasha PDF text."""
    norm = text.replace("$ ", "$")
    yr = [r for r in rows if r["dataset_year"] == 2024 and (r["daf_assets_5862"] or 0) > 0]
    hit = [r for r in yr if f"${int(r['daf_assets_5862']):,}" in norm]
    miss = sorted((r for r in yr if r not in hit), key=lambda r: -(r["daf_assets_5862"] or 0))
    return {
        "rows_with_assets": len(yr), "matched": len(hit), "matched_assets": total(hit, "daf_assets_5862"),
        "unmatched_assets": total(miss, "daf_assets_5862"),
        "largest_unmatched": [{k: r[k] for k in ("bn", "legal_name", "fpe", "accounts_5861", "daf_assets_5862")}
                              for r in miss[:10]],
    }


def continuity_2024_2025(rows: list[dict], filers_2025: dict) -> dict:
    """2024 DAF holders (5860=Y) by what their 2025-release return says: Y again, N, blank, or no return yet."""
    y25 = {r["bn"] for r in rows if r["dataset_year"] == 2025}
    prev = [r for r in rows if r["dataset_year"] == 2024]
    status = lambda r: ("Y" if r["bn"] in y25 else "no_2025_return" if r["bn"] not in filers_2025
                        else f"2025_answer_{filers_2025[r['bn']] or 'blank'}")
    groups = reduce(lambda acc, r: {**acc, status(r): acc.get(status(r), []) + [r]}, prev, {})
    new_2025 = [r for r in rows if r["dataset_year"] == 2025 and r["bn"] not in {p["bn"] for p in prev}]
    return {
        **{k: {"n": len(v), "assets_2024": total(v, "daf_assets_5862")} for k, v in groups.items()},
        "new_in_2025": {"n": len(new_2025), "assets_2025": total(new_2025, "daf_assets_5862")},
    }


def to_csv_rows(rows: list[dict]) -> list[dict]:
    return [{k: fmt(r[k]) for k in FIELDS}
            for r in sorted(rows, key=lambda r: (r["dataset_year"], r["rank_assets_in_year"]))]


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", help="repo root ('.')")
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--blumberg-txt", default=None, help="pdftotext -layout output of the Blumberg-Pasha 2026 PDF")
    ap.add_argument("--out", default="data/mission-2026-11-14/canada-daf-panel-2026-11-19.csv")
    ap.add_argument("--summary", default=None)
    a = ap.parse_args(argv)

    rows = enrich([r for y in YEARS for r in load_year(a.data_dir, y)])
    out = os.path.join(a.root, a.out)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(to_csv_rows(rows))

    summary = {
        "years": [year_summary(rows, y) for y in YEARS],
        "wellfunded_replica": wellfunded_replica(rows),
        "continuity_2024_2025": continuity_2024_2025(
            rows, {r["BN"]: r.get("5860", "") for r in read_csv(find(a.data_dir, 2025, "abc"))}),
        **({"blumberg_match": blumberg_match(rows, open(a.blumberg_txt, encoding="utf-8").read())}
           if a.blumberg_txt else {}),
    }
    text = json.dumps(summary, indent=1, default=str)
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
