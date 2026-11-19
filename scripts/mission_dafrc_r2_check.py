#!/usr/bin/env python3
"""DAFRC round-2 data-quality check (tasks P-B44N27-01 and P-B39N4-02).

Stdlib only; functional style (pure transforms; I/O only in the small fetch/read/write helpers and main()).

(A) P-B44N27-01  NPT (EIN 237825575): reads the filed Form 990 XML for FY2022, FY2023 and FY2024 and sets Schedule D
    Part I lines 1-4 beside Part X (total assets, investments, net assets), Part VIII / IX totals and the Part XI
    net-asset reconciliation, and rolls the DAF value forward and backward from the neighbouring years.
(B) P-B39N4-02   every FY2024 DAFRC row in the top 50 (by published and by repo-corrected year-end DAF assets) whose
    provenance flag is 'Imputed' (and, as a cross-check, 'paper submission'): looks up the newest FY2024 Form 990 in
    the IRS TEOS index (amended supersedes; fiscal year = calendar year in which the tax period ends, as in
    mission_dafrc_corrected_totals.py), parses Schedule D Part I lines 1-4 from the XML, compares with the existing
    R1 correction in dafrc-corrections-itemized.csv, and writes proposed round-2 corrections in the same format.

Inputs (never modified):
  data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv
  data/mission-2026-11-14/dafrc-corrections-itemized.csv
  data/mission-2026-11-14/dafrc-corrected-market-totals.csv
  IRS TEOS index  https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv   (--irs-dir; several dirs allowed,
                  a later dir's copy of the same year wins, so a freshly downloaded index_2026.csv supersedes an old one)
  Form 990 XML    https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml (--xml-dir cache)
Outputs:
  data/mission-2026-11-14/dafrc-corrections-r2-proposed-2026-11-19.csv   (--out-csv)
  JSON summary (--out-json) used by the research note; markdown tables on stdout.

Usage:
  python3 -I scripts/mission_dafrc_r2_check.py . --irs-dir IRSDIR [--irs-dir NEWER] --xml-dir XMLDIR [--fetch]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Iterable, Mapping, Sequence

UA = "research-script/1.0"
NS = "{http://www.irs.gov/efile}"
INDEX_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
DAFRC_URL = "https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx"
PANEL = "data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv"
ITEMS = "data/mission-2026-11-14/dafrc-corrections-itemized.csv"
TOTALS = "data/mission-2026-11-14/dafrc-corrected-market-totals.csv"
OUT_CSV = "data/mission-2026-11-14/dafrc-corrections-r2-proposed-2026-11-19.csv"
NPT_EIN = "237825575"
TOP_N = 50
FY = 2024

# metric -> (panel value column, panel provenance column, Schedule D Part I XML tag, form line)
METRICS = {
    "daf_accounts_eoy": ("number_of_daf_accounts", "source_number_of_accounts", "DonorAdvisedFundsHeldCnt", "Sch D I-1(a)"),
    "daf_contributions": ("total_daf_contributions", "source_total_daf_contributions", "DonorAdvisedFundsContriAmt", "Sch D I-2(a)"),
    "daf_grants": ("total_daf_grants", "source_total_daf_grants", "DonorAdvisedFundsGrantsAmt", "Sch D I-3(a)"),
    "daf_assets_eoy": ("eoy_daf_assets", "source_eoy_daf_assets", "DonorAdvisedFundsVlEOYAmt", "Sch D I-4(a)"),
}
# extra fields read from each return: name -> path of tags under IRS990 / Schedule D
FORM_FIELDS = {
    "total_assets_boy": ("TotalAssetsGrp", "BOYAmt"), "total_assets_eoy": ("TotalAssetsGrp", "EOYAmt"),
    "net_assets_boy": ("NetAssetsOrFundBalancesBOYAmt",), "net_assets_eoy": ("NetAssetsOrFundBalancesEOYAmt",),
    "net_assets_no_restr_eoy": ("NoDonorRestrictionNetAssetsGrp", "EOYAmt"),
    "net_assets_restr_eoy": ("DonorRestrictionNetAssetsGrp", "EOYAmt"),
    "inv_public_eoy": ("InvestmentsPubTradedSecGrp", "EOYAmt"), "inv_other_eoy": ("InvestmentsOtherSecuritiesGrp", "EOYAmt"),
    "inv_program_eoy": ("InvestmentsProgramRelatedGrp", "EOYAmt"),
    "cash_savings_eoy": ("SavingsAndTempCashInvstGrp", "EOYAmt"), "total_liabilities_eoy": ("TotalLiabilitiesGrp", "EOYAmt"),
    "contributions_total": ("TotalContributionsAmt",), "total_revenue": ("CYTotalRevenueAmt",),
    "grants_paid": ("CYGrantsAndSimilarPaidAmt",), "total_expenses": ("CYTotalExpensesAmt",),
    "rev_less_exp": ("ReconcilationRevenueExpnssAmt",), "unrealized_gains": ("NetUnrlzdGainsLossesInvstAmt",),
    "other_changes_net_assets": ("OtherChangesInNetAssetsAmt",), "part_iv_line6": ("DonorAdvisedFundInd",),
    "amended_ind": ("AmendedReturnInd",), "consolidated_fs": ("ConsolidatedAuditFinclStmtInd",),
}
SCHED_D_FIELDS = {"other_funds_count": ("FundsAndOtherAccountsHeldCnt",), "other_funds_eoy": ("FundsAndOtherAccountsVlEOYAmt",)}


# ----------------------------------------------------------------------------- small pure helpers
def num(x) -> float | None:
    try:
        return float(str(x).replace(",", "")) if x not in (None, "") else None
    except ValueError:
        return None


def ein9(x: str) -> str:
    return re.sub(r"\D", "", x or "").zfill(9)


def fy_of(tax_period: str) -> int:
    return int(tax_period[:4])


def bn(x: float | None) -> str:
    return "" if x is None else f"{x / 1e9:,.3f}"


def fmt(x) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


# ----------------------------------------------------------------------------- I/O edges
def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows({k: fmt(r.get(k)) for k in fields} for r in rows)


def index_paths(dirs: Sequence[str]) -> dict[str, str]:
    """year -> path; later dirs win."""
    found = ((m.group(1), os.path.join(d, f)) for d in dirs for f in sorted(os.listdir(d))
             for m in (re.fullmatch(r"index_(\d{4})\.csv", f),) if m)
    return reduce(lambda acc, kv: {**acc, kv[0]: kv[1]}, found, {})


def load_index(paths: Mapping[str, str], eins: frozenset[str]) -> dict[str, tuple[dict, ...]]:
    def recs(year, p):
        with open(p, newline="", encoding="latin-1") as fh:
            return tuple({"ein": ein9(d["EIN"]), "tax_period": d["TAX_PERIOD"], "return_type": d["RETURN_TYPE"],
                          "object_id": d["OBJECT_ID"], "index_year": year, "index_url": INDEX_URL.format(y=year)}
                         for d in csv.DictReader(fh) if ein9(d.get("EIN", "")) in eins)
    allrecs = {r["object_id"]: r for y, p in sorted(paths.items()) for r in recs(y, p)}
    return reduce(lambda acc, r: {**acc, r["ein"]: acc.get(r["ein"], ()) + (r,)}, allrecs.values(), {})


def fetch_xml(oid: str, xml_dir: str, fetch: bool) -> str | None:
    path = os.path.join(xml_dir, f"{oid}.xml")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    if not fetch:
        return None
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=180) as r, open(path + ".part", "wb") as fh:
            fh.write(r.read())
        os.replace(path + ".part", path)
        time.sleep(0.3)
        return path
    except Exception as e:  # noqa: BLE001 - logged, treated as 'not mirrored'
        print(f"fetch failed {oid}: {e}", file=sys.stderr)
        return None


def parse_return(path: str | None) -> dict:
    """Schedule D Part I + selected Form 990 lines. Returns {} when the XML is missing or unparsable."""
    if not path:
        return {}
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return {}

    def first(base, tags):
        node = None if base is None else base.find(".//" + "/".join(NS + t for t in tags))
        return (node.text or "").strip() if node is not None and node.text else None
    form = root.find(f".//{NS}IRS990")
    sd = root.find(f".//{NS}IRS990ScheduleD")
    hdr = root.find(f"{NS}ReturnHeader")
    vals = {
        "tax_period_end": first(hdr, ("TaxPeriodEndDt",)), "return_ts": (first(hdr, ("ReturnTs",)) or "")[:10],
        "return_type_cd": first(hdr, ("ReturnTypeCd",)), "sched_d_present": int(sd is not None),
        **{k: first(form, p) for k, p in FORM_FIELDS.items()},
        **{m: num(first(sd, (spec[2],))) for m, spec in METRICS.items()},
        **{k: num(first(sd, p)) for k, p in SCHED_D_FIELDS.items()},
    }
    numeric = set(FORM_FIELDS) - {"part_iv_line6", "amended_ind", "consolidated_fs"}
    return {k: (num(v) if k in numeric else v) for k, v in vals.items()}


# ----------------------------------------------------------------------------- pure selection
def fy2024_rows(panel: Iterable[Mapping]) -> tuple[dict, ...]:
    return tuple({**r, "ein": ein9(r["ein"])} for r in panel if r["fiscal_year_end"] == str(FY))


def corrections_by_key(items: Iterable[Mapping], fy: int) -> dict[tuple[str, str], dict]:
    return {(ein9(i["ein"]), i["metric"]): i for i in items if i["fiscal_year"] == str(fy)}


def current_value(row: Mapping, metric: str, corr: Mapping) -> float:
    """Repo-corrected value: the itemized correction when applied, else DAFRC as published."""
    c = corr.get((row["ein"], metric))
    return num(c["corrected_value"]) if c and c["applied"] == "1" else (num(row[METRICS[metric][0]]) or 0.0)


def ranked(rows: Sequence[Mapping], value) -> tuple[dict, ...]:
    return tuple(sorted(rows, key=lambda r: (-value(r), r["ein"])))


def rank_map(rows: Sequence[Mapping], value) -> dict[str, int]:
    return {r["ein"]: i for i, r in enumerate(ranked(rows, value), 1)}


def provenance(row: Mapping) -> str:
    srcs = {row[METRICS[m][1]] for m in METRICS}
    return "Imputed" if "Imputed" in srcs else ("paper submission" if "paper submission" in srcs else "/".join(sorted(srcs)))


def latest_fy_return(filings: Sequence[Mapping], fy: int) -> dict | None:
    """Newest Form 990 whose tax period ends in calendar year fy; amended (higher object id) supersedes."""
    cand = tuple(f for f in filings if f["return_type"] == "990" and fy_of(f["tax_period"]) == fy)
    return max(cand, key=lambda f: (f["tax_period"], f["object_id"])) if cand else None


def other_fy_returns(filings: Sequence[Mapping], fy: int, chosen: Mapping | None) -> str:
    return ";".join(f"{f['return_type']}:{f['tax_period']}:{f['object_id']}" for f in filings
                    if fy_of(f["tax_period"]) == fy and f["return_type"] in ("990", "990EZ", "990PF")
                    and (not chosen or f["object_id"] != chosen["object_id"]))


def suspect(metric: str, filed: float | None, ret: Mapping) -> bool:
    """Same screen as mission_dafrc_corrected_totals.suspect_part_i: negative amounts, or a zero/blank
    year-end value beside a positive account count."""
    v, c = ret.get("daf_assets_eoy"), ret.get("daf_accounts_eoy") or 0
    return filed is not None and (filed < 0 or (v or 0) < 0 or (c > 0 and not v))


def item_row(row: Mapping, metric: str, ret: Mapping, f990: Mapping | None, corr: Mapping, others: str) -> dict:
    """One proposed-corrections row in the dafrc-corrections-itemized.csv format.
    applied = 1 only when the round-2 value differs from what the repo already uses (existing R1 or published)."""
    col, src, _, line = METRICS[metric]
    pub = num(row[col])
    have = current_value(row, metric, corr)
    prior = corr.get((row["ein"], metric))
    filed = ret.get(metric) if ret.get("sched_d_present") else None
    usable = filed is not None and not suspect(metric, filed, ret)
    new = filed if usable else have
    oid = (f990 or {}).get("object_id", "")
    prior_oid = (prior or {}).get("return_object_id", "")
    changed = int(usable and new != have)
    status = ("no FY2024 Form 990 in the index" if not f990 else "XML not parsed" if not ret
              else "Schedule D Part I blank" if filed is None
              else "filed value suspect (negative or zero value with accounts); kept" if not usable
              else "confirms existing R1" if not changed and prior and prior["applied"] == "1" and prior_oid == oid
              else "confirms existing R1 (same value, newer object id)" if not changed and prior and prior["applied"] == "1"
              else "filed equals published" if not changed
              else "new: filed replaces repo value")
    return {"fiscal_year": FY, "ein": row["ein"], "name": row["name"], "type": row["type"], "metric": metric,
            "dafrc_row": "present", "dafrc_operating_status": row["operating_status"], "dafrc_source": row[src],
            "dafrc_value": pub, "filed_value": filed, "corrected_value": new, "delta": (new or 0) - (pub or 0),
            "applied": changed, "rule": "R1_filed_replaces_imputed" if usable and row[src] == "Imputed" else "",
            "evidence_class": "990_part_i_reported" if filed is not None else ("no_990_in_index" if not f990 else "990_part_i_blank"),
            "part_iv_line6": ret.get("part_iv_line6") or "", "return_object_id": oid,
            "tax_period": (f990 or {}).get("tax_period", ""), "return_ts": ret.get("return_ts", ""),
            "submitted_before_2026": int(ret.get("return_ts", "") < "2026-01-01") if ret.get("return_ts") else "",
            "amended_ind": ret.get("amended_ind") or "", "other_return_type_same_fy": others,
            "note": f"r2 recheck {line}: {status}; repo value before r2 = {fmt(have)}"
                    + (f" (itemized R1 object {prior_oid})" if prior and prior["applied"] == "1" else ""),
            "source_urls": " ; ".join(filter(None, (DAFRC_URL, (f990 or {}).get("index_url"),
                                                     XML_URL.format(oid=oid) if oid else "")))}


def npt_rollforward(years: Mapping[int, Mapping]) -> dict:
    """DAF value implied for FY2023 from each neighbour, using the year's change in Part X net assets
    (NPT reports every contribution and grant as DAF activity, so net-asset change ~ DAF change)."""
    y22, y23, y24 = years[2022], years[2023], years[2024]
    d23 = y23["net_assets_eoy"] - y23["net_assets_boy"]
    d24 = y24["net_assets_eoy"] - y24["net_assets_boy"]
    flow23 = y23["daf_contributions"] - y23["daf_grants"]
    return {
        "daf_to_net_assets": {fy: y["daf_assets_eoy"] / y["net_assets_eoy"] for fy, y in years.items()},
        "daf_minus_net_assets": {fy: y["daf_assets_eoy"] - y["net_assets_eoy"] for fy, y in years.items()},
        "sched_d_contrib_eq_part_viii": {fy: y["daf_contributions"] == y["contributions_total"] for fy, y in years.items()},
        "sched_d_grants_minus_part_ix_grants": {fy: y["daf_grants"] - y["grants_paid"] for fy, y in years.items()},
        "fy2023_forward_from_fy2022": y22["daf_assets_eoy"] + d23,
        "fy2023_backward_from_fy2024": y24["daf_assets_eoy"] - d24,
        "fy2023_contrib_minus_grants_only": y22["daf_assets_eoy"] + flow23,
        "fy2023_net_asset_change": d23, "fy2024_net_asset_change": d24,
        "fy2024_growth_needed_on_filed": (y24["daf_assets_eoy"] - (y24["daf_contributions"] - y24["daf_grants"])) / y23["daf_assets_eoy"] - 1,
        "fy2024_growth_needed_on_part_x": (y24["daf_assets_eoy"] - (y24["daf_contributions"] - y24["daf_grants"])) / y23["net_assets_eoy"] - 1,
        "gap_part_x_minus_sched_d_fy2023": y23["net_assets_eoy"] - y23["daf_assets_eoy"],
    }


def totals_view(rows: Sequence[Mapping], before, after, market_before: float) -> dict:
    rb, ra = ranked(rows, before), ranked(rows, after)
    ranks_b, ranks_a = rank_map(rows, before), rank_map(rows, after)
    delta = sum(after(r) - before(r) for r in rows)
    return {"top50_before": sum(map(before, rb[:TOP_N])), "top50_after": sum(map(after, ra[:TOP_N])),
            "market_before": market_before, "market_after": market_before + delta, "market_delta": delta,
            "rank_moves": tuple({"ein": r["ein"], "name": r["name"], "rank_before": ranks_b[r["ein"]], "rank_after": ranks_a[r["ein"]]}
                                for r in rows if ranks_b[r["ein"]] != ranks_a[r["ein"]] and min(ranks_b[r["ein"]], ranks_a[r["ein"]]) <= TOP_N),
            "top50_set_change": {"in": sorted(set(r["ein"] for r in ra[:TOP_N]) - set(r["ein"] for r in rb[:TOP_N])),
                                 "out": sorted(set(r["ein"] for r in rb[:TOP_N]) - set(r["ein"] for r in ra[:TOP_N]))}}


def concentration(values: Sequence[float], market: float) -> dict:
    s = sorted(values, reverse=True)
    return {"cr1": s[0] / market, "cr3": sum(s[:3]) / market, "cr5": sum(s[:5]) / market,
            "hhi": sum((v / market * 100) ** 2 for v in s)}


def fy2023_sensitivity(panel: Sequence[Mapping], items: Sequence[Mapping], totals: Sequence[Mapping], alt_values: Mapping[str, float]) -> dict:
    """FY2023 market total, growth, NPT share and concentration with the repo-corrected values, and with NPT FY2023
    replaced by each alternative value (Part X net assets; roll-forward). Sponsor-level corrected values = DAFRC +
    applied itemized corrections (rows with no DAFRC row, R4, are added to the market but not to the sponsor list)."""
    tot = {(int(t["fiscal_year"]), t["metric"]): num(t["corrected_value"]) for t in totals}
    rows = tuple({**r, "ein": ein9(r["ein"])} for r in panel if r["fiscal_year_end"] == "2023")
    corr = corrections_by_key(items, 2023)
    vals = {r["ein"]: current_value(r, "daf_assets_eoy", corr) for r in rows}
    m22, m23, m24 = (tot[(y, "daf_assets_eoy")] for y in (2022, 2023, 2024))

    def view(npt_value: float) -> dict:
        market = m23 + (npt_value - vals[NPT_EIN])
        v = {**vals, NPT_EIN: npt_value}
        return {"npt_fy2023": npt_value, "market_fy2023": market, "growth_fy22_23": market / m22 - 1, "growth_fy23_24": m24 / market - 1,
                "payout_fy2024_on_prior_assets": tot[(2024, "daf_grants")] / market,
                "npt_share": npt_value / market, "npt_rank": 1 + sum(1 for x in v.values() if x > npt_value), **concentration(tuple(v.values()), market)}
    return {"repo": view(vals[NPT_EIN]), **{k: view(x) for k, x in alt_values.items()}}


# ----------------------------------------------------------------------------- main
FIELDS = ("fiscal_year", "ein", "name", "type", "metric", "dafrc_row", "dafrc_operating_status", "dafrc_source", "dafrc_value",
          "filed_value", "corrected_value", "delta", "applied", "rule", "evidence_class", "part_iv_line6", "return_object_id",
          "tax_period", "return_ts", "submitted_before_2026", "amended_ind", "other_return_type_same_fy", "note", "source_urls")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--irs-dir", action="append", required=True)
    ap.add_argument("--xml-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--out-csv", default=OUT_CSV)
    ap.add_argument("--out-json", default="")
    a = ap.parse_args(argv)
    at = lambda p: os.path.join(a.root, p)  # noqa: E731
    os.makedirs(a.xml_dir, exist_ok=True)

    rows = fy2024_rows(read_csv(at(PANEL)))
    items = read_csv(at(ITEMS))
    corr = corrections_by_key(items, FY)
    market_before = next(num(t["corrected_value"]) for t in read_csv(at(TOTALS))
                         if t["fiscal_year"] == str(FY) and t["metric"] == "daf_assets_eoy")
    pub = lambda r: num(r["eoy_daf_assets"]) or 0.0  # noqa: E731
    cur = lambda r: current_value(r, "daf_assets_eoy", corr)  # noqa: E731
    top_pub, top_cur = ranked(rows, pub)[:TOP_N], ranked(rows, cur)[:TOP_N]
    universe = tuple({r["ein"]: r for r in top_pub + top_cur}.values())
    checked = tuple(r for r in universe if provenance(r) in ("Imputed", "paper submission"))

    index = load_index(index_paths(a.irs_dir), frozenset(r["ein"] for r in checked) | {NPT_EIN})
    chosen = {r["ein"]: latest_fy_return(index.get(r["ein"], ()), FY) for r in checked}
    rets = {e: parse_return(fetch_xml(f["object_id"], a.xml_dir, a.fetch)) if f else {} for e, f in chosen.items()}

    imputed = tuple(r for r in checked if provenance(r) == "Imputed")
    proposals = tuple(item_row(r, m, rets[r["ein"]], chosen[r["ein"]], corr, other_fy_returns(index.get(r["ein"], ()), FY, chosen[r["ein"]]))
                      for r in imputed for m in METRICS)
    prop_by = {(p["ein"], p["metric"]): p for p in proposals}
    new_val = lambda r: num(prop_by[(r["ein"], "daf_assets_eoy")]["corrected_value"]) if (r["ein"], "daf_assets_eoy") in prop_by else cur(r)  # noqa: E731

    paper = tuple({"ein": r["ein"], "name": r["name"], "dafrc_period": r["end_of_tax_period"], "rank_cur": rank_map(rows, cur)[r["ein"]],
                   **{f"paper_{m}": num(r[METRICS[m][0]]) for m in METRICS},
                   **{f"filed_{m}": rets[r["ein"]].get(m) for m in METRICS},
                   "object_id": (chosen[r["ein"]] or {}).get("object_id", ""), "tax_period": (chosen[r["ein"]] or {}).get("tax_period", "")}
                  for r in checked if provenance(r) == "paper submission")

    # NPT FY2022-FY2024
    npt_f = {fy: latest_fy_return(index.get(NPT_EIN, ()), fy) for fy in (2022, 2023, 2024)}
    npt = {fy: {**parse_return(fetch_xml(f["object_id"], a.xml_dir, a.fetch)), "object_id": f["object_id"], "tax_period": f["tax_period"],
                "other_returns": other_fy_returns(index.get(NPT_EIN, ()), fy, f)} for fy, f in npt_f.items()}
    npt_calc = npt_rollforward(npt)
    npt_row = next(r for r in rows if r["ein"] == NPT_EIN)  # FY2024 row, for metadata
    npt_sens = {"fiscal_year": 2023, "ein": NPT_EIN, "name": npt_row["name"], "type": npt_row["type"], "metric": "daf_assets_eoy",
                "dafrc_row": "present", "dafrc_operating_status": npt_row["operating_status"], "dafrc_source": "IRS 990",
                "dafrc_value": npt[2023]["daf_assets_eoy"], "filed_value": npt[2023]["daf_assets_eoy"],
                "corrected_value": npt[2023]["net_assets_eoy"], "delta": npt[2023]["net_assets_eoy"] - npt[2023]["daf_assets_eoy"],
                "applied": 0, "rule": "SENS_filed_inconsistent_with_part_x",
                "evidence_class": "990_part_i_reported", "part_iv_line6": npt[2023].get("part_iv_line6") or "",
                "return_object_id": npt[2023]["object_id"], "tax_period": npt[2023]["tax_period"], "return_ts": npt[2023]["return_ts"],
                "submitted_before_2026": 1, "amended_ind": npt[2023].get("amended_ind") or "", "other_return_type_same_fy": npt[2023]["other_returns"],
                "note": ("SENSITIVITY ONLY, not applied: filed Sch D I-4(a) is "
                         f"{npt_calc['daf_to_net_assets'][2023]:.1%} of Part X net assets (FY2022 {npt_calc['daf_to_net_assets'][2022]:.1%}, "
                         f"FY2024 {npt_calc['daf_to_net_assets'][2024]:.1%}); roll-forward from FY2022 gives {bn(npt_calc['fy2023_forward_from_fy2022'])}bn, "
                         f"back from FY2024 {bn(npt_calc['fy2023_backward_from_fy2024'])}bn; corrected_value = filed Part X net assets (lower bound)"),
                "source_urls": " ; ".join((DAFRC_URL, npt_f[2023]["index_url"], XML_URL.format(oid=npt[2023]["object_id"]),
                                           XML_URL.format(oid=npt[2022]["object_id"]), XML_URL.format(oid=npt[2024]["object_id"])))}

    write_csv(at(a.out_csv), sorted(proposals, key=lambda p: (-abs(p["delta"]), p["ein"], p["metric"])) + [npt_sens], FIELDS)
    summary = {
        "fy2024_rows": len(rows), "universe_top50_union": len(universe),
        "imputed_in_universe": [{"ein": r["ein"], "name": r["name"], "rank_pub": rank_map(rows, pub)[r["ein"]], "rank_cur": rank_map(rows, cur)[r["ein"]],
                                 "object_id": (chosen[r["ein"]] or {}).get("object_id", ""), "tax_period": (chosen[r["ein"]] or {}).get("tax_period", ""),
                                 "return_ts": rets[r["ein"]].get("return_ts", ""),
                                 **{f"pub_{m}": num(r[METRICS[m][0]]) for m in METRICS},
                                 **{f"filed_{m}": rets[r["ein"]].get(m) for m in METRICS},
                                 **{f"status_{m}": prop_by[(r["ein"], m)]["note"].split(": ", 1)[1].split(";")[0] for m in METRICS}}
                                for r in imputed],
        "proposals_applied": sum(p["applied"] for p in proposals),
        "proposal_delta_by_metric": {m: sum(p["corrected_value"] - current_value(next(r for r in imputed if r["ein"] == p["ein"]), m, corr)
                                            for p in proposals if p["metric"] == m) for m in METRICS},
        "assets": totals_view(rows, cur, new_val, market_before),
        "published_top50": sum(map(pub, top_pub)), "published_market": sum(map(pub, rows)),
        "paper_rows_panel": {"n": sum(1 for r in rows if provenance(r) == "paper submission"),
                             "n_period_not_fy2024": sum(1 for r in rows if provenance(r) == "paper submission" and not r["end_of_tax_period"].startswith(str(FY))),
                             "eoy_assets": sum(pub(r) for r in rows if provenance(r) == "paper submission")},
        "paper_checks": paper, "npt": {str(k): v for k, v in npt.items()}, "npt_calc": npt_calc,
        "fy2023_sensitivity": fy2023_sensitivity(read_csv(at(PANEL)), items, read_csv(at(TOTALS)),
                                                 {"part_x_net_assets": npt[2023]["net_assets_eoy"],
                                                  "rollforward_from_fy2022": npt_calc["fy2023_forward_from_fy2022"]}),
        "index_files": index_paths(a.irs_dir),
    }
    if a.out_json:
        with open(a.out_json, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=1, default=str)
    s = summary["assets"]
    print(f"top-50 union {len(universe)}; imputed {len(imputed)}; paper {len(paper)}; proposals applied {summary['proposals_applied']}")
    print(f"top50 assets before {bn(s['top50_before'])}bn after {bn(s['top50_after'])}bn; market before {bn(s['market_before'])}bn "
          f"after {bn(s['market_after'])}bn (delta {s['market_delta']:,.0f})")
    print("| # pub | # cur | EIN | Sponsor | Object id | Period | Published EOY $bn | Filed EOY $bn | Status (EOY) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for x in sorted(summary["imputed_in_universe"], key=lambda x: x["rank_cur"]):
        print(f"| {x['rank_pub']} | {x['rank_cur']} | {x['ein']} | {x['name']} | {x['object_id']} | {x['tax_period']} | "
              f"{bn(x['pub_daf_assets_eoy'])} | {bn(x['filed_daf_assets_eoy'])} | {x['status_daf_assets_eoy']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
