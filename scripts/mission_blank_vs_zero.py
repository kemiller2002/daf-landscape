#!/usr/bin/env python3
"""Blank vs zero 'Grants from DAFs' in IPS's FY2023 sponsor list (queue item P-B39N8-01-01).

IPS's FY2023 sponsor list (Independent-DAF-Report-Sponsor-Lists.xlsx, sheet 2023) has 1,735 sponsors but rates for
only 1,487: the 248 others have a blank 'Grants from DAFs' cell, so IPS computes no payout for them and they fall
outside its 9.68% (published 9.7%) median. This script reads the same-fiscal-year Form 990 Schedule D Part I for
each of the 248 from the IRS e-file XML and classifies the line 3(a) cell as filed blank, filed zero, filed
non-zero, or no return found. It then recomputes the FY2023 median under IPS's formula and the repo's two formulas
(scripts/mission_payout_bridge.py: beg = grants_t / assets_(t-1); irs = grants_t / (assets_t + grants_t)).

Secondary check: the same read for every FY2023 sponsor-year of the repo's corrected panel with DAF grants = 0
(the 9.33%-10.20% bracket in the bridge's section 3.2), so the repo panel can apply IPS's blank-only exclusion
with filed evidence.

Stdlib only; functional style. Reuses, unchanged:
  * mission_990_contractors.load_index / latest_per_period / fetch_extract (IRS TEOS index, GivingTuesday mirror,
    streamed Schedule D extract; absent XML element -> None, filed 0 -> 0.0)
  * mission_payout_bridge.read_xlsx / ips_sponsors / ips_published_medians / ips_deficient / corrected_panel / median

Schedule D Part I column (a) (donor advised funds) elements:
  line 1  DonorAdvisedFundsHeldCnt      line 2  DonorAdvisedFundsContriAmt
  line 3  DonorAdvisedFundsGrantsAmt    line 4  DonorAdvisedFundsVlEOYAmt

Usage
  python3 scripts/mission_blank_vs_zero.py . --ips-dir IPSDIR --irs-dir IRSDIR --work WORK \
      [--reuse-cache DIR ...] [--fetch]
  --reuse-cache: directories holding extract990/{oid}.json from earlier repo runs (same EXTRACT_VERSION).
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as cn  # noqa: E402
import mission_payout_bridge as pb  # noqa: E402
from mission_990_contractors import ein9, fmt, num, read_csv, write_csv  # noqa: E402

FY = 2023
INDEX_YEARS = (2023, 2024, 2025, 2026)
MONTHS = {m: i for i, m in enumerate(("January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"), start=1)}
LINES = {"line1a_daf_count": "sched_d_daf_count", "line2a_contributions": "sched_d_daf_contributions",
         "line3a_grants": "sched_d_daf_grants", "line4a_eoy_value": "sched_d_daf_eoy_value"}
CLASSES = ("blank-filed", "zero-filed", "non-zero", "no-return-found")
IPS_VINTAGE = "2024"  # IPS downloaded IRS e-file data on 31 Jan 2025 (bridge section 3.2): prefer objects processed by 2024
OUT_CSV = "data/mission-2026-11-14/blank-vs-zero-daf-grants-2026-11-20.csv"
IPS_LISTS = pb.IPS_URL.format(f=pb.IPS_FILES["lists"])
FIELDS = ("population", "ein", "name", "ips_sponsor_type", "ips_fiscal_year_end", "ips_fiscal_month_end",
          "target_tax_period", "ips_daf_accounts", "ips_daf_assets", "ips_contributions", "ips_grants_cell",
          "ips_daf_assets_fy2022", "panel_daf_grants_fy2023", "panel_daf_assets_fy2023", "panel_grants_imputed",
          "object_id", "return_type", "tax_period", "tax_period_match", "index_year", "n_returns_same_period",
          "xml_status", "sched_d_present", "line1a_daf_count", "line2a_contributions", "line3a_grants",
          "line4a_eoy_value", "filed_assets_match_ips", "filed_accounts_match_ips", "classification", "return_vintage",
          "latest_object_id", "latest_classification", "latest_line3a_grants",
          "other_forms_same_fy", "prior_object_id", "prior_line4a_eoy_value", "rate_irs_ips_assets",
          "rate_irs_filed_assets", "rate_beg", "ips_screen_deficient", "xml_url", "index_url", "source")


# ----------------------------------------------------------------------------- pure transforms
def target_period(r: Mapping) -> str:
    m = MONTHS.get(r["Fiscal Month End"], 0)
    return f"{r['Fiscal Year End']}{m:02d}" if m else ""


def pick_return(filings: Sequence[Mapping], tp: str, fy: int, max_year: str = "9999") -> tuple[dict | None, str, int]:
    """Same tax period first (newest object id = amended supersedes); else any 990 whose period ends in fy.
    max_year limits to objects the IRS processed by that year (OBJECT_ID starts with the processing year)."""
    pool = tuple(f for f in filings if f["object_id"][:4] <= max_year)
    same = tuple(f for f in pool if f["return_type"] == "990" and f["tax_period"] == tp)
    if same:
        return max(same, key=lambda f: f["object_id"]), "exact", len(same)
    anyfy = cn.latest_per_period(pool, (fy,), ("990",))
    return (anyfy[-1], "same_fy_other_month", len(anyfy)) if anyfy else (None, "", 0)


def classify(found: bool, ext: Mapping) -> str:
    if not found or ext.get("xml_status") != "ok":
        return "no-return-found"
    g = ext.get("sched_d_daf_grants")
    return "blank-filed" if g is None else ("zero-filed" if g == 0 else "non-zero")


def irs_rate(g: float | None, a: float | None) -> float | None:
    return pb.ratio(g, a + g) if g is not None and a is not None and a >= 0 and a + g > 0 else None


def beg_rate(g: float | None, a0: float | None) -> float | None:
    return pb.ratio(g, a0) if g is not None and a0 is not None and a0 > 0 else None


def close(a: float | None, b: float | None) -> str:
    return "" if a is None or b is None else ("1" if abs(a - b) <= max(1.0, 0.005 * abs(b)) else "0")


def build_row(pop: str, ein: str, base: Mapping, filings: Sequence[Mapping], exts: Mapping, prior_a: float | None) -> dict:
    tp = base["target_tax_period"]
    latest, _, _ = pick_return(filings, tp, FY)
    vint, vmatch, vn = pick_return(filings, tp, FY, IPS_VINTAGE)
    ret, match, nsame = (vint, vmatch, vn) if vint else pick_return(filings, tp, FY)
    ext = exts.get(ret["object_id"], {}) if ret else {}
    cls = classify(ret is not None, ext)
    lext = exts.get(latest["object_id"], {}) if latest else {}
    vals = {k: ext.get(v) for k, v in LINES.items()} if cls != "no-return-found" else {k: None for k in LINES}
    prev = cn.latest_per_period(filings, (FY - 1,), ("990",))
    prev_ext = exts.get(prev[-1]["object_id"], {}) if prev else {}
    prior_line4 = prev_ext.get("sched_d_daf_eoy_value") if prev_ext.get("xml_status") == "ok" else None
    a0 = prior_a if prior_a is not None else prior_line4
    g = vals["line3a_grants"]
    others = sorted({f["return_type"] for f in filings if f["return_type"] != "990" and f["tax_period"][:4] == str(FY)})
    return {**base, "population": pop, "ein": ein,
            "object_id": ret["object_id"] if ret else "", "return_type": ret["return_type"] if ret else "",
            "tax_period": ret["tax_period"] if ret else "", "tax_period_match": match,
            "index_year": ret["index_year"] if ret else "", "n_returns_same_period": nsame,
            "xml_status": ext.get("xml_status", "") if ret else "no_990_in_index",
            "sched_d_present": ext.get("sched_d_present", "") if ret else "", **vals,
            "filed_assets_match_ips": close(vals["line4a_eoy_value"], num(base.get("ips_daf_assets"))),
            "filed_accounts_match_ips": close(vals["line1a_daf_count"], num(base.get("ips_daf_accounts"))),
            "classification": cls, "return_vintage": "processed_by_2024" if vint else ("processed_2025_or_later" if ret else ""),
            "latest_object_id": latest["object_id"] if latest else "", "latest_classification": classify(latest is not None, lext),
            "latest_line3a_grants": lext.get("sched_d_daf_grants") if latest else None, "other_forms_same_fy": ";".join(others),
            "prior_object_id": prev[-1]["object_id"] if prev else "", "prior_line4a_eoy_value": prior_line4,
            "rate_irs_ips_assets": irs_rate(g, num(base.get("ips_daf_assets"))),
            "rate_irs_filed_assets": irs_rate(g, vals["line4a_eoy_value"]),
            "rate_beg": beg_rate(g, a0),
            "ips_screen_deficient": ("1" if pb.ips_deficient(num(base.get("ips_daf_accounts")), num(base.get("ips_contributions")),
                                                              g, num(base.get("ips_daf_assets"))) else "0") if g is not None else "",
            "xml_url": ext.get("xml_url", cn.XML_URL.format(oid=ret["object_id"])) if ret else "",
            "index_url": ret["index_url"] if ret else ";".join(cn.INDEX_URL.format(y=y) for y in INDEX_YEARS),
            "source": IPS_LISTS if pop == "ips_blank_grants" else "dafrc-sponsor-schedule-d-fy2019-2024.csv + dafrc-corrections-itemized.csv (applied=1)"}


def ips_base(r: Mapping, prior: Mapping, panel: Mapping) -> dict:
    e = ein9(r["EIN"])
    p = panel.get((e, FY), {})
    return {"name": r["Sponsor"], "ips_sponsor_type": r["Sponsor Type"], "ips_fiscal_year_end": r["Fiscal Year End"],
            "ips_fiscal_month_end": r["Fiscal Month End"], "target_tax_period": target_period(r),
            "ips_daf_accounts": r["DAF Accounts"], "ips_daf_assets": r["DAF Assets"],
            "ips_contributions": r["Contributions to DAFs"], "ips_grants_cell": r["Grants from DAFs"] or "(blank)",
            "ips_daf_assets_fy2022": prior.get(e, ""), "panel_daf_grants_fy2023": p.get("daf_grants"),
            "panel_daf_assets_fy2023": p.get("daf_assets_eoy"), "panel_grants_imputed": p.get("daf_grants_imputed", "")}


def panel_base(e: str, v: Mapping, ips: Mapping) -> dict:
    r = ips.get(e)
    return {"name": v["name"], "ips_sponsor_type": r["Sponsor Type"] if r else "", "ips_fiscal_year_end": r["Fiscal Year End"] if r else "",
            "ips_fiscal_month_end": r["Fiscal Month End"] if r else "", "target_tax_period": target_period(r) if r else "",
            "ips_daf_accounts": r["DAF Accounts"] if r else "", "ips_daf_assets": r["DAF Assets"] if r else "",
            "ips_contributions": r["Contributions to DAFs"] if r else "",
            "ips_grants_cell": (r["Grants from DAFs"] or "(blank)") if r else "(not on IPS list)", "ips_daf_assets_fy2022": "",
            "panel_daf_grants_fy2023": v["daf_grants"], "panel_daf_assets_fy2023": v["daf_assets_eoy"],
            "panel_grants_imputed": v["daf_grants_imputed"]}


def rollforward(r: Mapping) -> dict | None:
    """Implied outflow = assets_(t-1) + line 2(a) - line 4(a) (blank 2(a) read as 0); ignores investment return.
    Used only to describe whether a blank line 3(a) is arithmetically compatible with zero grants [inference]."""
    a0 = num(r["ips_daf_assets_fy2022"]) if r["ips_daf_assets_fy2022"] not in ("", None) else r["prior_line4a_eoy_value"]
    a1 = r["line4a_eoy_value"]
    if a0 is None or a1 is None or a0 <= 0:
        return None
    out = a0 + (r["line2a_contributions"] or 0) - a1
    return {"implied_outflow": out, "implied_outflow_share_of_a0": out / a0}


def med_row(scenario: str, formula: str, sample: str, rates: Sequence[float], note: str, published: float) -> dict:
    m = pb.median(sorted(rates))
    return {"scenario": scenario, "formula": formula, "sample": sample, "n": len(rates), "median": m,
            "shift_vs_ips_published_pts": None if m is None else round((m - published) * 100, 4), "note": note}


def with_shift(meds: Sequence[dict]) -> tuple[dict, ...]:
    """Adds the shift in points against S0 (IPS's own rates) for the same formula and sample."""
    s0 = {(m["formula"], m["sample"]): m["median"] for m in meds if m["scenario"].startswith(("S0", "P0"))}
    return tuple({**m, "shift_vs_s0_pts": None if m["median"] is None or s0.get((m["formula"], m["sample"])) is None
                  else round((m["median"] - s0[(m["formula"], m["sample"])]) * 100, 4)} for m in meds)


def scenarios(ips: Sequence[Mapping], ips22: Mapping, rows: Mapping, panel: Mapping, panel_rows: Mapping, published: float) -> tuple[dict, ...]:
    """Medians under IPS's formula and the repo's beg/irs formulas.
    ips: FY2023 IPS rows; ips22: ein -> FY2022 IPS DAF assets; rows: ein -> classified row for the 248."""
    base = {ein9(r["EIN"]): r for r in ips if num(r["Average DAF Payout"]) is not None}
    pub = {e: num(r["Average DAF Payout"]) for e, r in base.items()}
    typ = {ein9(r["EIN"]): r["Sponsor Type"] for r in ips}
    by = lambda c: {e: r for e, r in rows.items() if r["classification"] == c}  # noqa: E731
    nz, zf, bf, nr = by("non-zero"), by("zero-filed"), by("blank-filed"), by("no-return-found")
    filed = {**nz, **zf}
    ok = lambda r: r["ips_screen_deficient"] != "1"  # noqa: E731
    out = [med_row("S0_ips_published_rates", "irs", "all", list(pub.values()), "IPS's own 1,487 'Average DAF Payout' values", published),
           med_row("S1_filed_grants_ips_assets", "irs", "all",
                   [*pub.values(), *(r["rate_irs_ips_assets"] for r in filed.values() if r["rate_irs_ips_assets"] is not None)],
                   "IPS 1,487 + zero-filed and non-zero sponsors at filed line 3(a) / (IPS DAF assets + line 3(a)); blank-filed and no-return stay out (IPS's rule applied to the filed cell)", published),
           med_row("S2_filed_grants_filed_assets", "irs", "all",
                   [*pub.values(), *(r["rate_irs_filed_assets"] for r in filed.values() if r["rate_irs_filed_assets"] is not None)],
                   "as S1 but denominator uses filed line 4(a) instead of IPS's DAF-assets cell", published),
           med_row("S3_filed_grants_ips_screens", "irs", "all",
                   [*pub.values(), *(r["rate_irs_ips_assets"] for r in filed.values() if r["rate_irs_ips_assets"] is not None and ok(r))],
                   "as S1, dropping added sponsors that fail IPS's Schedule D deficiency screens (accounts<=0, accounts=contributions or grants, accounts>=assets, assets=grants)", published),
           med_row("S4_filed_plus_blank_filed_as_zero", "irs", "all",
                   [*pub.values(), *(r["rate_irs_ips_assets"] for r in filed.values() if r["rate_irs_ips_assets"] is not None), *[0.0] * len(bf)],
                   "as S1, plus blank-filed sponsors counted as 0% (no-return-found still out)", published),
           med_row("S6_latest_returns_filed_grants", "irs", "all",
                   [*pub.values(), *(x for x in (irs_rate(r["latest_line3a_grants"], num(r["ips_daf_assets"])) for r in rows.values()
                                                 if r["latest_classification"] in ("zero-filed", "non-zero")) if x is not None)],
                   "as S1 but reading the newest same-period return in the index as of 2026-11 (amended/late returns processed after IPS's 31 Jan 2025 download included)", published),
           med_row("S5_all_248_as_zero", "irs", "all", [*pub.values(), *[0.0] * len(rows)],
                   "bridge counterfactual: every blank IPS cell counted as 0% (reproduces 7.72%)", published)]
    ex = lambda d: [v for e, v in d if typ.get(e) != "Donation Processor"]  # noqa: E731
    out += [med_row("S0_ips_published_rates", "irs", "ex_proc", ex(pub.items()), "IPS rates without IPS-classified donation processors", published),
            med_row("S1_filed_grants_ips_assets", "irs", "ex_proc",
                    ex([*pub.items(), *((e, r["rate_irs_ips_assets"]) for e, r in filed.items() if r["rate_irs_ips_assets"] is not None)]),
                    "S1 without donation processors", published)]
    # repo's $1m filter on the irs asset term (assets_t + grants_t)
    ge1m_base = [pub[e] for e, r in base.items() if (num(r["DAF Assets"]) or 0) + (num(r["Grants from DAFs"]) or 0) >= pb.MIN_ASSETS]
    ge1m_add = [r["rate_irs_ips_assets"] for r in filed.values()
                if r["rate_irs_ips_assets"] is not None and (num(r["ips_daf_assets"]) or 0) + r["line3a_grants"] >= pb.MIN_ASSETS]
    out += [med_row("S0_ips_published_rates", "irs", "ge1m", ge1m_base, "IPS rates, assets_t + grants_t >= $1m", published),
            med_row("S1_filed_grants_ips_assets", "irs", "ge1m", [*ge1m_base, *ge1m_add], "S1 with the $1m filter", published)]
    # repo formula (a): grants_t / EOY assets_(t-1); prior assets from IPS's FY2022 sheet, else filed FY2022 line 4(a)
    beg_base = [x for x in (beg_rate(num(r["Grants from DAFs"]), ips22.get(e)) for e, r in base.items()) if x is not None]
    beg_add = [r["rate_beg"] for r in filed.values() if r["rate_beg"] is not None]
    out += [med_row("S0_ips_published_rates", "beg", "all", beg_base, "IPS FY2023 grants / IPS FY2022 DAF assets, for IPS's 1,487 rated sponsors with FY2022 assets > 0", published),
            med_row("S1_filed_grants_ips_assets", "beg", "all", [*beg_base, *beg_add],
                    "S0(beg) + zero-filed and non-zero sponsors: filed line 3(a) / prior-year assets (IPS FY2022 sheet, else filed FY2022 line 4(a))", published),
            med_row("S4_filed_plus_blank_filed_as_zero", "beg", "all",
                    [*beg_base, *beg_add, *(0.0 for r in bf.values() if beg_rate(0.0, num(r["ips_daf_assets_fy2022"]) if r["ips_daf_assets_fy2022"] != "" else r["prior_line4a_eoy_value"]) is not None)],
                    "S1(beg) + blank-filed counted as 0% where prior-year assets > 0", published)]
    # repo corrected panel, irs formula, assets_t > 0 (bridge 'repo_assets_gt0_no_screens'), with the filed blank/zero read
    pan = {e: v for (e, y), v in panel.items() if y == FY and v["daf_grants"] is not None and v["daf_assets_eoy"] is not None and v["daf_assets_eoy"] > 0}
    prate = {e: irs_rate(v["daf_grants"], v["daf_assets_eoy"]) for e, v in pan.items()}
    blank_eins = {e for e, r in panel_rows.items() if r["classification"] == "blank-filed"}
    noret_eins = {e for e, r in panel_rows.items() if r["classification"] == "no-return-found"}
    zero_eins = {e for e, v in pan.items() if v["daf_grants"] == 0}
    out += [med_row("P0_repo_panel_assets_gt0", "irs", "repo_panel", list(prate.values()), "bridge: repo corrected panel FY2023, assets > 0, zero grants kept (9.33%)", published),
            med_row("P1_repo_panel_grants_gt0", "irs", "repo_panel", [v for e, v in prate.items() if e not in zero_eins], "bridge bound: all zero-grant sponsor-years dropped (10.20%)", published),
            med_row("P2_repo_panel_drop_blank_filed", "irs", "repo_panel", [v for e, v in prate.items() if e not in blank_eins],
                    "IPS's rule on the panel with filed evidence: drop only zero-grant sponsor-years whose same-FY line 3(a) is filed blank", published),
            med_row("P3_repo_panel_drop_blank_and_noreturn", "irs", "repo_panel", [v for e, v in prate.items() if e not in blank_eins | noret_eins],
                    "as P2, also dropping zero-grant sponsor-years with no same-FY e-filed 990 found", published)]
    return with_shift(out)


# ----------------------------------------------------------------------------- I/O edges
def cached_extract(oid: str, reuse: Sequence[str], work: str, fetch: bool) -> dict:
    hit = next((p for p in (os.path.join(d, "extract990", f"{oid}.json") for d in reuse) if os.path.exists(p)), None)
    if hit:
        with open(hit, encoding="utf-8") as fh:
            d = json.load(fh)
        if d.get("_v") == cn.EXTRACT_VERSION:
            return {**d, "_cache": hit}
    return cn.fetch_extract(oid, work, fetch)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--ips-dir", required=True)
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--reuse-cache", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--out", default=OUT_CSV)
    ap.add_argument("--summary-out", default=None)
    a = ap.parse_args(argv)
    data = os.path.join(a.root, "data", "mission-2026-11-14")
    book = pb.read_xlsx(os.path.join(a.ips_dir, pb.IPS_FILES["lists"]))
    published = pb.ips_published_medians(pb.read_xlsx(os.path.join(a.ips_dir, pb.IPS_FILES["summary"])))[FY]
    sponsors = pb.ips_sponsors(book)
    ips23 = sponsors[FY]
    ips_by = {ein9(r["EIN"]): r for r in ips23}
    ips22 = {ein9(r["EIN"]): num(r["DAF Assets"]) for r in sponsors[FY - 1] if num(r["DAF Assets"]) is not None}
    panel = pb.corrected_panel(read_csv(os.path.join(data, "dafrc-sponsor-schedule-d-fy2019-2024.csv")),
                               read_csv(os.path.join(data, "dafrc-corrections-itemized.csv")))
    blanks = {ein9(r["EIN"]): r for r in ips23 if r["Grants from DAFs"] == ""}
    pzero = {e: v for (e, y), v in panel.items() if y == FY and v["daf_grants"] == 0}
    eins = frozenset(blanks) | frozenset(pzero)
    idx = cn.load_index(tuple(os.path.join(a.irs_dir, f"index_{y}.csv") for y in INDEX_YEARS
                              if os.path.exists(os.path.join(a.irs_dir, f"index_{y}.csv"))), eins)
    oids = sorted({f["object_id"] for e in eins for f in idx.get(e, ()) if f["return_type"] == "990"
                   and f["tax_period"][:4] in (str(FY), str(FY - 1))})
    with ThreadPoolExecutor(max_workers=8) as ex:
        exts = dict(zip(oids, ex.map(lambda o: cached_extract(o, a.reuse_cache, a.work, a.fetch), oids)))
    ips_rows = {e: build_row("ips_blank_grants", e, ips_base(r, ips22, panel), idx.get(e, ()), exts, ips22.get(e)) for e, r in blanks.items()}
    pan_rows = {e: build_row("repo_panel_zero_grants", e, panel_base(e, v, ips_by), idx.get(e, ()), exts, None) for e, v in pzero.items()}
    # panel rows: when not on IPS list, target period = newest 990 period ending in FY (pick_return falls back)
    rows = [*sorted(ips_rows.values(), key=lambda r: r["ein"]), *sorted(pan_rows.values(), key=lambda r: r["ein"])]
    write_csv(os.path.join(a.root, a.out), [{k: fmt(r.get(k)) for k in FIELDS} for r in rows], FIELDS)
    meds = scenarios(ips23, ips22, ips_rows, panel, pan_rows, published)
    cnt = lambda rs, k: dict(collections.Counter(r[k] for r in rs))  # noqa: E731
    xtab = lambda pairs: {" | ".join(map(str, k)): v for k, v in collections.Counter(pairs).most_common()}  # noqa: E731
    summary = {
        "ips_published_median": published, "n_ips_rows": len(ips23), "n_blank": len(blanks), "n_panel_zero_fy2023": len(pzero),
        "oids_needed": len(oids), "extract_sources": cnt([{"s": "reused_cache" if "_cache" in x else x.get("xml_status")} for x in exts.values()], "s"),
        "ips_blank_classification": cnt(ips_rows.values(), "classification"),
        "ips_blank_class_by_type": xtab((r["ips_sponsor_type"], r["classification"]) for r in ips_rows.values()),
        "ips_blank_period_match": cnt(ips_rows.values(), "tax_period_match"),
        "ips_blank_vintage": xtab((r["classification"], r["return_vintage"]) for r in ips_rows.values()),
        "ips_blank_latest_vs_vintage": xtab((r["classification"], r["latest_classification"], r["object_id"] == r["latest_object_id"]) for r in ips_rows.values()),
        "panel_zero_latest_vs_vintage": xtab((r["classification"], r["latest_classification"], r["object_id"] == r["latest_object_id"]) for r in pan_rows.values()),
        "ips_blank_sched_d_present": xtab((r["classification"], r["sched_d_present"]) for r in ips_rows.values()),
        "ips_blank_assets_match": xtab((r["classification"], r["filed_assets_match_ips"]) for r in ips_rows.values()),
        "ips_blank_accounts_match": xtab((r["classification"], r["filed_accounts_match_ips"]) for r in ips_rows.values()),
        "ips_blank_contrib_blank": xtab((r["classification"], r["ips_contributions"] == "") for r in ips_rows.values()),
        "ips_blank_other_forms": xtab((r["classification"], r["other_forms_same_fy"]) for r in ips_rows.values()),
        "ips_blank_in_panel": xtab((r["classification"], r["panel_daf_grants_fy2023"] is not None) for r in ips_rows.values()),
        "blank_filed_rollforward": (lambda xs: {"n_with_prior_assets": len(xs),
                                                "n_implied_outflow_le_0": sum(1 for x in xs if x["implied_outflow"] <= 0),
                                                "n_implied_outflow_gt_10pct_of_a0": sum(1 for x in xs if x["implied_outflow_share_of_a0"] > 0.10),
                                                "median_implied_outflow_share_of_a0": pb.median(sorted(x["implied_outflow_share_of_a0"] for x in xs))})(
            [x for x in (rollforward(r) for r in ips_rows.values() if r["classification"] == "blank-filed") if x is not None]),
        "nonzero_filed_grants": {"n": len([r for r in ips_rows.values() if r["classification"] == "non-zero"]),
                                 "sum": sum(r["line3a_grants"] for r in ips_rows.values() if r["classification"] == "non-zero"),
                                 "median_rate_irs_ips_assets": pb.median(sorted(r["rate_irs_ips_assets"] for r in ips_rows.values()
                                                                                if r["classification"] == "non-zero" and r["rate_irs_ips_assets"] is not None))},
        "nonzero_screen_deficient": cnt([r for r in ips_rows.values() if r["classification"] in ("non-zero", "zero-filed")], "ips_screen_deficient"),
        "panel_zero_classification": cnt(pan_rows.values(), "classification"),
        "panel_zero_by_ips_cell": xtab((r["ips_grants_cell"] if r["ips_grants_cell"] in ("(blank)", "(not on IPS list)") else "ips_value", r["classification"]) for r in pan_rows.values()),
        "panel_zero_imputed": xtab((r["classification"], r["panel_grants_imputed"]) for r in pan_rows.values()),
        "medians": meds,
    }
    if a.summary_out:
        with open(a.summary_out, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=1, default=str)
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
