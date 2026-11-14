#!/usr/bin/env python3
"""Corrected DAFRC market totals FY2020-FY2024 (queue items P-990-01, P-990-02).

Stdlib only; functional style (pure transforms, I/O at the edges). Reuses the IRS e-file index loader,
the streamed Form 990 extractor and its JSON cache from scripts/mission_990_contractors.py.

Inputs (never modified):
  data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv   DAFRC sponsor-level dataset (Spring 2026)
  data/mission-2026-11-14/daf-market-annual-series.csv               DAFRC published (memo, rounded) totals
  data/mission-2026-11-14/sponsor-exit-verification.csv              tier-A (ceased) sponsors with final return / Schedule N
  IRS TEOS e-file index  https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv
  Form 990 XML           https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml
Outputs:
  data/mission-2026-11-14/dafrc-corrected-market-totals.csv   FY x metric: published, dataset sum, corrected, deltas by rule
  data/mission-2026-11-14/dafrc-corrections-itemized.csv      one row per sponsor-year x metric tested (applied = 1 if changed)

Correction rules (applied per sponsor-year and per metric; a metric is touched only when DAFRC's own provenance
flag for that metric is 'Imputed', or when DAFRC has no row at all):
  R1_filed_replaces_imputed   the newest same-fiscal-year Form 990 (amended supersedes) reports the Schedule D Part I
                              field -> filed value replaces the imputed value (a filed 0 counts as filed).
  R2_terminated_double_count  tier-A sponsor (final/terminated return with Schedule N transfer, per
                              sponsor-exit-verification.csv) and FY >= the final-return FY -> filed value (the final
                              return's Part I) or 0 where the field is blank / no return exists.
                              The transferred assets are already counted at the recipient sponsors.
  R3_990_says_no_dafs         same-FY 990 answers Part IV line 6 'No' and Schedule D Part I is blank -> 0.
  R4_closed_but_filed         DAFRC treats the sponsor as closed (no row) but the same-FY 990 reports a positive
                              Schedule D Part I DAF value -> filed values added.
  Unresolved (kept as published, applied = 0): no same-FY 990 in the index, XML not mirrored, 990-EZ/PF only,
  Part IV 'Yes' with Part I blank, an implausible account count (mission_990_contractors.implausible_count), or a
  suspect Part I (negative amount; zero/blank value with a positive count).

Usage:
  python3 scripts/mission_dafrc_corrected_totals.py --irs-dir DIR --cache-dir CACHE [--fetch]
  (DIR holds index_2020.csv .. index_2026.csv; CACHE is the extract cache of mission_990_contractors.py)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as m990  # noqa: E402

DATA = m990.DATA
MARKET_CSV = os.path.join(DATA, "daf-market-annual-series.csv")
EXIT_CSV = os.path.join(DATA, "sponsor-exit-verification.csv")
OUT_TOTALS = os.path.join(DATA, "dafrc-corrected-market-totals.csv")
OUT_ITEMS = os.path.join(DATA, "dafrc-corrections-itemized.csv")
FYS = (2020, 2021, 2022, 2023, 2024)
INDEX_YEARS = tuple(range(2020, 2027))
MARKET_URL = "https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf"

# metric -> (DAFRC value column, DAFRC provenance column, extract field, memo metric name)
METRICS = {
    "daf_assets_eoy": ("eoy_daf_assets", "source_eoy_daf_assets", "sched_d_daf_eoy_value", "charitable_assets"),
    "daf_contributions": ("total_daf_contributions", "source_total_daf_contributions", "sched_d_daf_contributions", "contributions"),
    "daf_grants": ("total_daf_grants", "source_total_daf_grants", "sched_d_daf_grants", "grants"),
    "daf_accounts_eoy": ("number_of_daf_accounts", "source_number_of_accounts", "sched_d_daf_count", "daf_accounts"),
}
RULES = ("R1_filed_replaces_imputed", "R2_terminated_double_count", "R3_990_says_no_dafs", "R4_closed_but_filed")
num = m990.num


# ----------------------------------------------------------------------------- inputs
def terminated_sponsors(path: str = EXIT_CSV) -> dict[str, dict]:
    """Tier-A EINs -> final-return fiscal year and Schedule N total. The final return is the later e-filed 990 when one
    exists, otherwise the last DAFRC-filed period (the final return was itself the last filing)."""
    rows = m990.read_csv(path) if os.path.exists(path) else ()

    def final_fy(r):
        p = r["latest_later_efile_period"] or r["last_filed_period_end"].replace("-", "")[:6]
        return int(p[:4]) if p[:4].isdigit() else None
    return {m990.ein9(r["ein"]): {"final_fy": final_fy(r), "schedule_n_fmv_total": num(r["schedule_n_fmv_total"]),
                                  "schedule_n_recipients": r["schedule_n_recipients"], "outcome": r["outcome"]}
            for r in rows if r["outcome_tier"].startswith("A")}


def published_memo(path: str = MARKET_CSV) -> dict[tuple[int, str], float]:
    return {(int(r["fiscal_year"]), r["metric"]): num(r["value"]) for r in m990.read_csv(path)
            if r["series_id"] == "DAFRC_2025_UPDATED"}


# ----------------------------------------------------------------------------- pure classification
def is_imputed(row: Mapping, metric: str) -> bool:
    return row.get(METRICS[metric][1], "") == "Imputed"


def part_iv_no(ex: Mapping) -> bool:
    return str(ex.get("daf_ind_part_iv", "")).lower() in ("0", "false")


def part_i_blank(ex: Mapping) -> bool:
    return all(ex.get(METRICS[m][2]) is None for m in METRICS)


def suspect_part_i(ex: Mapping, filed: float) -> bool:
    """A filed amount is not used when it is negative, or when the year-end value is zero/blank while a positive
    account count is reported (count keyed without value, e.g. Universite de Montreal FY2024: 714 DAFs, $0)."""
    v, c = ex.get("sched_d_daf_eoy_value"), ex.get("sched_d_daf_count") or 0
    return filed < 0 or (v or 0) < 0 or (c > 0 and not v)


def evidence(ex: Mapping, f990: Mapping | None, other: Mapping | None) -> str:
    if f990 is None:
        return "no_990_in_index" + (f"_filed_{other['return_type']}" if other else "")
    if ex.get("xml_status") != "ok":
        return "990_xml_not_mirrored"
    if not part_i_blank(ex):
        return "990_part_i_reported"
    return "990_part_iv_no_part_i_blank" if part_iv_no(ex) else "990_part_iv_yes_or_blank_part_i_blank"


def correct_metric(metric: str, published: float | None, ex: Mapping, ev: str, term: Mapping | None, fy: int,
                   closed: bool) -> tuple[float | None, str, str]:
    """Returns (corrected value, rule, note). rule '' = unchanged / unresolved. Pure."""
    filed = ex.get(METRICS[metric][2]) if ev == "990_part_i_reported" else None
    if filed is not None and suspect_part_i(ex, filed):
        return published, "", "filed Part I suspect (negative amount, or zero/blank value with a positive account count); kept as published"
    if metric == "daf_accounts_eoy" and filed is not None and m990.implausible_count(ex.get("sched_d_daf_count"), ex.get("sched_d_daf_eoy_value")):
        return published, "", "filed account count implausible (implausible_count); kept as published"
    if closed:
        if ev == "990_part_i_reported" and (ex.get("sched_d_daf_eoy_value") or 0) > 0 and filed is not None:
            return filed, "R4_closed_but_filed", "DAFRC has no row (sponsor assumed closed); same-FY 990 reports DAFs"
        return published, "", "closed sponsor-year; no positive filed DAF value"
    if term and term["final_fy"] is not None and fy >= term["final_fy"]:
        return (filed if filed is not None else 0.0), "R2_terminated_double_count", (f"sponsor ceased (final return FY{term['final_fy']}); Schedule N transfers "
                                                    f"${(term['schedule_n_fmv_total'] or 0):,.0f} to: {term['schedule_n_recipients'][:200]}")
    if filed is not None:
        return filed, "R1_filed_replaces_imputed", ""
    if ev == "990_part_iv_no_part_i_blank":
        return 0.0, "R3_990_says_no_dafs", "Part IV line 6 = No and Schedule D Part I blank"
    return published, "", {"990_part_iv_yes_or_blank_part_i_blank": "Part IV line 6 Yes/blank but Part I blank; kept imputed",
                           "990_xml_not_mirrored": "same-FY 990 not yet mirrored; kept imputed",
                           }.get(ev, f"{ev}; kept imputed")


def test_universe(dafrc: Sequence[Mapping]) -> tuple[dict, ...]:
    """Every DAFRC FY2020-24 row with at least one imputed metric, plus every closed sponsor-year (no row) FY2020-24."""
    imputed = tuple({**r, "closed": False} for r in dafrc if r["fy"] in FYS and any(is_imputed(r, m) for m in METRICS))
    closed = tuple({"ein": g["ein"], "name": g["name"], "type": g["type"], "fy": g["dafrc_fy"], "closed": True,
                    "operating_status": g["dafrc_operating_status"]}
                   for g in m990.gap_universe(dafrc) if g["gap_kind"] == "dafrc_closed_no_row" and g["dafrc_fy"] in FYS)
    return imputed + closed


def items_for(row: Mapping, index: Mapping, extracts: Mapping, terms: Mapping) -> tuple[dict, ...]:
    fl = index.get(row["ein"], ())
    f990 = m990.latest_for_fy(fl, row["fy"], ("990",))
    other = m990.latest_for_fy(fl, row["fy"], ("990EZ", "990PF"))
    ex = extracts.get(f990["object_id"], {}) if f990 else {}
    ev = evidence(ex, f990, other)
    term = terms.get(row["ein"])
    ts = (ex.get("return_ts") or "")[:10]

    def one(metric):
        col, src, _, _ = METRICS[metric]
        if not row["closed"] and not is_imputed(row, metric):
            return None
        pub = None if row["closed"] else num(row.get(col))
        new, rule, note = correct_metric(metric, pub, ex, ev, term, row["fy"], row["closed"])
        applied = int(bool(rule) and (new or 0) != (pub or 0))
        return {"fiscal_year": row["fy"], "ein": row["ein"], "name": row["name"], "type": row["type"], "metric": metric,
                "dafrc_row": "none (assumed closed)" if row["closed"] else "present",
                "dafrc_operating_status": row.get("operating_status", ""),
                "dafrc_source": "" if row["closed"] else row.get(src, ""), "dafrc_value": pub,
                "corrected_value": new, "delta": (new or 0) - (pub or 0), "applied": applied, "rule": rule if applied else "",
                "evidence_class": ev, "part_iv_line6": ex.get("daf_ind_part_iv", ""),
                "filed_value": ex.get(METRICS[metric][2]), "return_object_id": (f990 or {}).get("object_id", ""),
                "tax_period": (f990 or {}).get("tax_period", ""), "return_ts": ts,
                "submitted_before_2026": int(ts < "2026-01-01") if ts else "",
                "amended_ind": ex.get("amended_ind", ""), "other_return_type_same_fy": (other or {}).get("return_type", ""),
                "note": note,
                "source_urls": " ; ".join(filter(None, (m990.DAFRC_URL, (f990 or {}).get("index_url"),
                                                         m990.XML_URL.format(oid=f990["object_id"]) if f990 else "")))}
    return tuple(x for x in map(one, METRICS) if x is not None and (not row["closed"] or x["applied"]))


def totals(dafrc: Sequence[Mapping], items: Sequence[Mapping], memo: Mapping) -> tuple[dict, ...]:
    def one(fy, metric):
        col, src, _, memo_name = METRICS[metric]
        rows = tuple(r for r in dafrc if r["fy"] == fy)
        ds = sum(num(r[col]) or 0 for r in rows)
        it = tuple(i for i in items if i["fiscal_year"] == fy and i["metric"] == metric)
        app = tuple(i for i in it if i["applied"])
        by_rule = {r: sum(i["delta"] for i in app if i["rule"] == r) for r in RULES}
        corr = ds + sum(by_rule.values())
        imputed_pub = sum(num(r[col]) or 0 for r in rows if r[src] == "Imputed")
        unresolved = tuple(i for i in it if not i["applied"] and i["dafrc_row"] == "present")
        return {"fiscal_year": fy, "metric": metric, "published_memo_value": memo.get((fy, memo_name)),
                "dataset_sum_as_published": ds, "corrected_value": corr, "delta": corr - ds,
                "delta_pct": (corr - ds) / ds if ds else None,
                **{f"delta_{r}": by_rule[r] for r in RULES},
                **{f"n_{r}": sum(1 for i in app if i["rule"] == r) for r in RULES},
                "imputed_value_as_published": imputed_pub,
                "imputed_value_remaining": sum(i["corrected_value"] or 0 for i in unresolved),
                "n_imputed_rows_unresolved": len(unresolved),
                "delta_from_returns_submitted_before_2026": sum(i["delta"] for i in app if i["submitted_before_2026"] == 1),
                "dataset_sponsor_rows": len(rows),
                "sources": f"{m990.DAFRC_URL} ; {MARKET_URL} ; data/mission-2026-11-14/dafrc-corrections-itemized.csv"}
    return tuple(one(fy, m) for fy in FYS for m in METRICS)


ITEM_FIELDS = ("fiscal_year", "ein", "name", "type", "metric", "dafrc_row", "dafrc_operating_status", "dafrc_source", "dafrc_value",
               "filed_value", "corrected_value", "delta", "applied", "rule", "evidence_class", "part_iv_line6", "return_object_id",
               "tax_period", "return_ts", "submitted_before_2026", "amended_ind", "other_return_type_same_fy", "note", "source_urls")
TOTAL_FIELDS = ("fiscal_year", "metric", "published_memo_value", "dataset_sum_as_published", "corrected_value", "delta", "delta_pct",
                *(f"delta_{r}" for r in RULES), *(f"n_{r}" for r in RULES), "imputed_value_as_published",
                "imputed_value_remaining", "n_imputed_rows_unresolved", "delta_from_returns_submitted_before_2026",
                "dataset_sponsor_rows", "sources")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--cache-dir", default=os.path.expanduser("~/.cache/daf-landscape"))
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    dafrc = m990.load_dafrc()
    uni = test_universe(dafrc)
    idx_paths = tuple(p for p in (os.path.join(a.irs_dir, f"index_{y}.csv") for y in INDEX_YEARS) if os.path.exists(p))
    index = m990.load_index(idx_paths, frozenset(r["ein"] for r in uni))
    want = tuple(f["object_id"] for r in uni for f in (m990.latest_for_fy(index.get(r["ein"], ()), r["fy"], ("990",)),) if f)
    extracts = m990.fetch_all(want, a.cache_dir, a.fetch)
    terms = terminated_sponsors()
    items = tuple(i for r in uni for i in items_for(r, index, extracts, terms))
    tot = totals(dafrc, items, published_memo())
    m990.write_csv(OUT_ITEMS, sorted(items, key=lambda i: (i["fiscal_year"], -int(i["applied"]), -abs(i["delta"]), i["ein"], i["metric"])),
                   ITEM_FIELDS)
    m990.write_csv(OUT_TOTALS, tot, TOTAL_FIELDS)
    print(json.dumps({"rows_tested": len(uni), "items": len(items), "applied": sum(i["applied"] for i in items),
                      "returns_needed": len(set(want)),
                      "returns_parsed": sum(1 for o in set(want) if extracts.get(o, {}).get("xml_status") == "ok"),
                      "totals": [{k: t[k] for k in ("fiscal_year", "metric", "dataset_sum_as_published", "corrected_value", "delta")}
                                 for t in tot]}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
