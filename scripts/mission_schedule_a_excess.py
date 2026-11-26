#!/usr/bin/env python3
"""P-B40N1202-B43N26-01: Schedule A support-schedule lines for the 2,352-EIN recipient DAF-share sample, used to
estimate how much of Form 990 Part VIII line 1f comes from donors above the 2% public-support limit, and the DAF share
of 1f net of that excess.

Sample and weights  The committed recipient rows of data/mission-2026-11-14/daf-share-individual-basis-2026-11-19.csv
                    (mission_recipient_basis_eligibility.py, seed 20261119): same EINs, strata, stratum_N, status,
                    object ids (the FY2023/FY2024 returns already chosen), DAF-weighted top-50 numerator and Part VIII
                    line totals. Weights are the pipeline's N_h / (n_h - xml_not_read) (weights_a), recomputed here.
Schedule A          Each chosen return is re-read from the GivingTuesday mirror of IRS TEOS XML and the
                    IRS990ScheduleA leaves (depth <= 2) are cached. Part II (170(b)(1)(A)(iv)/(vi)):
                        line 1  GiftsGrantsContriRcvd170Grp  (five year columns + total)
                        line 5  SubstantialContributorsTotAmt (total column only: the 5-year excess over 2% of
                                line 11(f), per donor other than governmental units and (vi) organisations)
                        line 11 TotalSupportAmt
                    Part III (509(a)(2)):
                        line 1  GiftsGrantsContrisRcvd509Grp
                        line 7a AmountsRcvdDsqlfyPersonGrp (per year: amounts on lines 1-3 from disqualified
                                persons; omitted = 0). Part III has no 2% line (7b, SubstantialContributorsAmtGrp,
                                covers lines 2-3 receipts only), so 7a is a separate, looser proxy.
Year alignment      Line 5 spans five years; Part VIII 1f is one year. Three allocations per return:
                        cy  (central) E = line5 x line1(e) / line1(f): the 5-year excess ratio applied to the
                            current-year column (assumes a constant excess share across the five years)
                        avg E = line5 / (number of the five columns with positive line 1): per-year average
                        all E = line5: the whole 5-year excess charged to the current year (upper bound)
                    E is capped at the return's 1f (EZ: line 1). Per recipient, E and 1f sum over matched FYs.
Shares              share_net = DAF-weighted numerator / (1f - E); large_share = E / 1f. Respondents are the b6_1f set
                    (status ok, 1f > 0) for every measure; where E absorbs all of 1f the net share is +inf (ranked top
                    in quantiles, numerator kept in pooled ratios; counted in share_den_absorbed). Recipients without a Part II
                    in a matched year get E = 0 for that year in the all-recipient scope (flagged), and are excluded
                    from the part_ii_all_years scope. Pooled ratio and weighted median as in the pipeline; stratified
                    bootstrap (respondents resampled within stratum, weights fixed), seeds offset per scope x measure.

Pure functions; I/O only in fetch/load helpers and `main`. Stdlib only.

Usage:
  python3 scripts/mission_schedule_a_excess.py . --sa-cache DIR --bmf-dir BMF [--fetch] [--boot 500]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402

IN_A = os.path.join(DATA, "daf-share-individual-basis-2026-11-19.csv")
OUT = os.path.join(DATA, "schedule-a-excess-2026-11-20.csv")
UA = "research-script/1.0"
SA_V = 1
YCOLS = ("CurrentTaxYearMinus4YearsAmt", "CurrentTaxYearMinus3YearsAmt", "CurrentTaxYearMinus2YearsAmt",
         "CurrentTaxYearMinus1YearAmt", "CurrentTaxYearAmt")
P2_L1 = "GiftsGrantsContriRcvd170Grp"
P2_L5 = "SubstantialContributorsTotAmt"
P2_L11 = "TotalSupportAmt"
P3_L1 = "GiftsGrantsContrisRcvd509Grp"
P3_L7A = "AmountsRcvdDsqlfyPersonGrp"
ALLOC = ("cy", "avg", "all")
FOUNDATION_CODES = {"10": "church 170(b)(1)(A)(i)", "11": "school 170(b)(1)(A)(ii)", "12": "hospital 170(b)(1)(A)(iii)",
                    "13": "governmental-unit support 170(b)(1)(A)(iv)", "14": "governmental unit 170(b)(1)(A)(v)",
                    "15": "publicly supported 170(b)(1)(A)(vi)", "16": "509(a)(2)", "17": "supporting org 509(a)(3)"}
SRC = ("Sample, weights, numerator and Part VIII 1f: data/mission-2026-11-14/daf-share-individual-basis-2026-11-19.csv "
       "(mission_recipient_basis_eligibility.py). Schedule A Part II lines 1, 5, 11 / Part III lines 1, 7a: IRS990ScheduleA "
       "in the GivingTuesday mirror of IRS TEOS XML (gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/"
       "{oid}_public.xml). Line definitions: www.irs.gov/instructions/i990sa.")


# ----------------------------------------------------------------------------- fetch / parse (I/O)
def parse_sched_a(stream) -> dict:
    """Leaves of IRS990ScheduleA up to depth 2 ({path: text}), plus the main form tag."""
    form = ""
    try:
        for ev, el in ET.iterparse(stream, events=("start", "end")):
            tag = local(el.tag)
            if ev == "start" and tag in ("IRS990", "IRS990EZ") and not form:
                form = tag
            if ev == "end" and tag == "IRS990ScheduleA":
                def leaves(e, pre):
                    kids = list(e)
                    return ({pre: (e.text or "").strip()} if not kids
                            else reduce(lambda a, c: {**a, **leaves(c, (pre + "/" if pre else "") + local(c.tag))}, kids, {}))
                lv = {k: v for k, v in leaves(el, "").items() if k.count("/") <= 1 and len(v) <= 40}
                return {"status": "ok", "form": form, "leaves": lv}
    except ET.ParseError:
        return {"status": "parse_error", "form": form}
    return {"status": "no_schedule_a", "form": form}


def fetch_sched_a(oid: str, cache: str, fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == SA_V:
            return c
    if not fetch:
        return {"status": "not_fetched", "oid": oid}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    r = {"status": "error"}
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                r = parse_sched_a(resp)
            break
        except urllib.error.HTTPError as e:
            r = {"status": f"http_{e.code}"}
            if e.code in (403, 404):
                break
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            r = {"status": "error"}
            time.sleep(2 * (attempt + 1))
    obj = {**r, "oid": oid, "_v": SA_V}
    if r["status"] in ("ok", "http_404", "no_schedule_a", "parse_error"):
        os.makedirs(cache, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh)
    return obj


def load_bmf_foundation(bmf_dir: str, eins: frozenset) -> dict:
    def rows(f):
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple((ein9(r["EIN"]), (r.get("FOUNDATION") or "").strip()) for r in csv.DictReader(fh) if ein9(r["EIN"]) in eins)
    return dict(x for f in ("eo1.csv", "eo2.csv", "eo3.csv", "eo4.csv", "eo_pr.csv", "eo_xx.csv") for x in rows(f))


# ----------------------------------------------------------------------------- per-return values (pure)
def sched_a_values(sa: Mapping) -> dict:
    """Part II / Part III line values from cached leaves; part = 'II', 'III', 'II+III' or 'none'."""
    lv = sa.get("leaves", {}) if sa.get("status") == "ok" else {}
    g = lambda grp: {c: num(lv.get(f"{grp}/{c}")) for c in YCOLS + ("TotalAmt",)}  # noqa: E731
    p2 = g(P2_L1)
    p3 = g(P3_L1)
    has2 = (any(v is not None for v in p2.values()) or lv.get(P2_L5) not in (None, "") or lv.get(P2_L11) not in (None, "")
            or lv.get("PublicSupportTotal170Amt") not in (None, "") or any(k.startswith("TotalCalendarYear170Grp/") for k in lv))
    has3 = (any(v is not None for v in p3.values()) or any(k.startswith(P3_L7A + "/") for k in lv)
            or lv.get("PublicSupportTotal509Amt") not in (None, "") or any(k.startswith("Total509Grp/") for k in lv))
    l7a = g(P3_L7A)
    return {"sa_status": sa.get("status", "missing"), "part": ("II+III" if has2 and has3 else "II" if has2 else "III" if has3 else "none"),
            "p2_l1": p2, "p2_l5": num(lv.get(P2_L5)) or 0.0, "p2_l11": num(lv.get(P2_L11)),
            "p3_l1": p3, "p3_l7a": l7a,
            "p1_inds": ";".join(sorted(k for k, v in lv.items() if "/" not in k and k.endswith("Ind") and v.lower() in ("x", "true", "1")))}


def excess_of(v: Mapping, l1f: float) -> dict:
    """Allocated current-year excess (cy / avg / all), each capped at the return's 1f, for a Part II return."""
    l1 = v["p2_l1"]
    tot = l1.get("TotalAmt") or sum(l1.get(c) or 0.0 for c in YCOLS)
    cy = l1.get("CurrentTaxYearAmt") or 0.0
    npos = sum(1 for c in YCOLS if (l1.get(c) or 0.0) > 0)
    l5 = v["p2_l5"]
    raw = {"cy": (l5 * cy / tot) if tot > 0 else 0.0, "avg": (l5 / npos) if npos else 0.0, "all": l5}
    cap = max(l1f, 0.0)
    return {**{f"e_{k}": min(max(x, 0.0), cap) for k, x in raw.items()},
            **{f"capped_{k}": raw[k] > cap + 1 for k in ALLOC},
            "l1_cy": cy, "l1_tot": tot, "l5": l5, "excess_ratio_5y": (l5 / tot) if tot > 0 else None}


def year_record(fy: str, oid: str, l1f: float, sa: Mapping) -> dict:
    v = sched_a_values(sa)
    p2 = v["part"] in ("II", "II+III")
    ex = excess_of(v, l1f) if p2 else {**{f"e_{k}": 0.0 for k in ALLOC}, **{f"capped_{k}": False for k in ALLOC},
                                       "l1_cy": None, "l1_tot": None, "l5": 0.0, "excess_ratio_5y": None}
    p3_cy = v["p3_l1"].get("CurrentTaxYearAmt")
    p3_7a = v["p3_l7a"].get("CurrentTaxYearAmt")
    return {"fy": fy, "oid": oid, "l1f": l1f, "sa_status": v["sa_status"], "part": v["part"], "p1_inds": v["p1_inds"],
            **ex, "p3_l1_cy": p3_cy, "p3_l7a_cy": p3_7a, "p3_l7a_tot": v["p3_l7a"].get("TotalAmt"),
            "p3_l1_tot": v["p3_l1"].get("TotalAmt")}


# ----------------------------------------------------------------------------- per-recipient (pure)
def l1f_by_year(oids: Sequence[str], l1f_total: float, p8: Mapping) -> dict:
    """Per-return 1f: from the committed Part VIII cache when present, else split the recipient total evenly."""
    vals = {o: p8.get(o) for o in oids}
    if all(v is not None for v in vals.values()):
        return vals
    return {o: l1f_total / len(oids) for o in oids}


def recipient(r: Mapping, sa_cache: Mapping, p8: Mapping) -> dict:
    oids = tuple(o for o in r["object_ids"].split(";") if o)
    fys = tuple(y for y in r["years_matched"].split(";") if y)
    num_dw = float(r["num_daf_weighted_matched"] or 0)
    l1f_tot = float(r["l1f_matched"] or 0)
    l1f_y = l1f_by_year(oids, l1f_tot, p8) if oids else {}
    yrs = tuple(year_record(fy, o, l1f_y[o], sa_cache.get(o, {"status": "missing"})) for fy, o in zip(fys, oids))
    parts = tuple(y["part"] for y in yrs)
    e = {k: sum(y[f"e_{k}"] for y in yrs) for k in ALLOC}
    p3_ok = bool(yrs) and all(y["part"] in ("III", "II+III") for y in yrs)
    p3_dq = sum(min(max(y["p3_l7a_cy"] or 0.0, 0.0), max(y["l1f"], 0.0)) for y in yrs) if p3_ok else None
    sum_ = lambda k: sum(y[k] or 0.0 for y in yrs)  # noqa: E731
    l1_cy = sum_("l1_cy")
    l1f_p2 = sum(y["l1f"] for y in yrs if y["part"] in ("II", "II+III"))
    group = ("part_ii_all_years" if yrs and all(p in ("II", "II+III") for p in parts)
             else "part_iii_all_years" if yrs and all(p == "III" for p in parts)
             else "no_support_schedule" if yrs and all(p == "none" for p in parts)
             else "mixed_or_missing" if yrs else "no_return")
    ratio = lambda a, b: (a / b) if b and b > 0 else None  # noqa: E731
    # net denominator fully absorbed by the excess (cap hit): share is unbounded; kept as +inf so that the recipient
    # stays in the 1f respondent set (ranked top for quantiles, full numerator kept in pooled ratios)
    net = lambda a, d: (a / d) if d > 0 else (float("inf") if l1f_tot > 0 else None)  # noqa: E731
    ok = r["status"] == "ok"
    return {"row_type": "recipient", "ein": r["ein"], "name": r["name"], "ntee_major_group": r["ntee_major_group"],
            "revenue_band": r["revenue_band"], "stratum": r["stratum"], "stratum_N": int(r["stratum_N"]),
            "status": r["status"], "years_matched": r["years_matched"], "object_ids": r["object_ids"],
            "forms": r["forms"], "schedule_a_parts": ";".join(parts), "schedule_a_status": ";".join(y["sa_status"] for y in yrs),
            "support_group": group, "part1_indicators": "|".join(y["p1_inds"] for y in yrs),
            "num_daf_weighted_matched": num_dw, "l1f_matched": l1f_tot, "l1h_matched": float(r["l1h_matched"] or 0),
            "l1g_noncash_matched": float(r["l1g_matched"] or 0),
            "sa_l1_cy_over_1h": ratio(l1_cy, float(r["l1h_matched"] or 0)) if l1f_p2 and len(set(parts)) == 1 else None,
            "sa_p2_l1_cy_matched": l1_cy if l1f_p2 else None, "sa_p2_l1_5y_matched": sum_("l1_tot") if l1f_p2 else None,
            "sa_p2_l5_matched": sum_("l5") if l1f_p2 else None,
            "excess_ratio_5y": ratio(sum_("l5"), sum_("l1_tot")) if l1f_p2 else None,
            "sa_l1_cy_over_1f": ratio(l1_cy, l1f_p2) if l1f_p2 else None,
            **{f"excess_{k}": e[k] for k in ALLOC},
            **{f"capped_{k}": any(y[f"capped_{k}"] for y in yrs) for k in ALLOC},
            "sa_p3_l1_cy_matched": sum_("p3_l1_cy") if p3_ok else None, "sa_p3_l7a_cy_matched": p3_dq,
            "share_1f": ratio(num_dw, l1f_tot) if ok else None,
            **{f"share_1f_net_{k}": net(num_dw, l1f_tot - e[k]) if ok else None for k in ALLOC},
            "share_1f_net_p3_7a": net(num_dw, l1f_tot - p3_dq) if ok and p3_dq is not None else None,
            **{f"large_share_{k}": ratio(e[k], l1f_tot) if ok else None for k in ALLOC},
            "large_share_p3_7a": ratio(p3_dq, l1f_tot) if ok and p3_dq is not None else None,
            "source": SRC}


# ----------------------------------------------------------------------------- statistics (pure)
def wquantile(pairs: Sequence[tuple], q: float):
    xs = sorted((v, w) for v, w in pairs if v is not None)
    tot = sum(w for _, w in xs)
    if not xs or tot <= 0:
        return None
    cum = reduce(lambda acc, vw: acc + [acc[-1] + vw[1]], xs, [0.0])[1:]
    return next(v for (v, _), c in zip(xs, cum) if c >= q * tot)


def weights_a(rows: Sequence[Mapping]) -> dict:
    """As mission_recipient_basis_eligibility.weights_a: N_h / (n_h - xml_not_read)."""
    by = _group_by_fast(rows, lambda r: r["stratum"])
    return {k: v[0]["stratum_N"] / (len(v) - sum(r["status"] == "xml_not_read" for r in v))
            for k, v in by.items() if any(r["status"] == "ok" for r in v)}


MEASURES = {
    # name: (numerator fn, denominator fn, per-recipient share key)
    "daf_share_1f": (lambda r: r["num_daf_weighted_matched"], lambda r: r["l1f_matched"], "share_1f"),
    **{f"daf_share_1f_net_{k}": ((lambda r: r["num_daf_weighted_matched"]),
                                 (lambda r, k=k: r["l1f_matched"] - r[f"excess_{k}"]), f"share_1f_net_{k}") for k in ALLOC},
    **{f"large_donor_share_of_1f_{k}": ((lambda r, k=k: r[f"excess_{k}"]), (lambda r: r["l1f_matched"]), f"large_share_{k}")
       for k in ALLOC},
    "daf_share_1f_net_p3_7a": ((lambda r: r["num_daf_weighted_matched"]),
                               (lambda r: r["l1f_matched"] - (r["sa_p3_l7a_cy_matched"] or 0.0)), "share_1f_net_p3_7a"),
    "dq_share_of_1f_p3_7a": ((lambda r: r["sa_p3_l7a_cy_matched"] or 0.0), (lambda r: r["l1f_matched"]), "large_share_p3_7a"),
}


def pooled(rows: Sequence[Mapping], w: Mapping, nf, df):
    d = sum(w[r["stratum"]] * df(r) for r in rows)
    return sum(w[r["stratum"]] * nf(r) for r in rows) / d if rows and d > 0 else None


def boot(rows: Sequence[Mapping], w: Mapping, nf, df, key: str, reps: int, seed: int) -> dict:
    if len(rows) < 10 or reps <= 0:
        return {}
    by = _group_by_fast(rows, lambda r: r["stratum"])
    rng = random.Random(seed)
    draws = tuple(tuple(x for k in sorted(by) for x in rng.choices(by[k], k=len(by[k]))) for _ in range(reps))
    p = sorted(x for x in (pooled(d, w, nf, df) for d in draws) if x is not None)
    m = sorted(x for x in (wquantile([(r[key], w[r["stratum"]]) for r in d], 0.5) for d in draws) if x is not None)
    pct = lambda xs, q: xs[min(len(xs) - 1, int(q * len(xs)))] if xs else None  # noqa: E731
    return {"median_ci95_lo": pct(m, 0.025), "median_ci95_hi": pct(m, 0.975),
            "pooled_ci95_lo": pct(p, 0.025), "pooled_ci95_hi": pct(p, 0.975)}


def summary(scope: str, measure: str, rows: Sequence[Mapping], w: Mapping, reps: int, seed: int) -> dict:
    nf, df, key = MEASURES[measure]
    ok = tuple(r for r in rows if r["status"] == "ok")
    use = tuple(r for r in ok if r["l1f_matched"] > 0 and r[key] is not None)
    wt = lambda r: w[r["stratum"]]  # noqa: E731
    tw = sum(wt(r) for r in use)
    q = lambda p: wquantile([(r[key], wt(r)) for r in use], p)  # noqa: E731
    return {"row_type": "summary", "scope": scope, "measure": measure, "sampled": len(rows), "respondents": len(use),
            "weighted_recipients": round(tw), "dropped_1f_nonpos": len(ok) - len(use),
            "p25": q(0.25), "median": q(0.5), "p75": q(0.75), "pooled": pooled(use, w, nf, df),
            "share_gt_100pct": (sum(wt(r) for r in use if r[key] > 1) / tw) if tw else None,
            "share_den_absorbed": (sum(wt(r) for r in use if df(r) <= 0) / tw) if tw else None,
            "weighted_num_usd": round(sum(wt(r) * nf(r) for r in use)), "weighted_den_usd": round(sum(wt(r) * df(r) for r in use)),
            **boot(use, w, nf, df, key, reps, seed), "source": SRC}


def scopes() -> tuple:
    p2 = lambda r: r["support_group"] == "part_ii_all_years"  # noqa: E731
    return (("all_ex_excluded", lambda r: True),
            ("part_ii_all_years", p2),
            ("part_ii_all_years_non_certainty", lambda r: p2(r) and r["stratum"] != "certainty"),
            ("part_ii_all_years_form_990_only", lambda r: p2(r) and "IRS990EZ" not in r["forms"]),
            ("part_ii_all_years_noncash_lt_25pct_of_1h",
             lambda r: p2(r) and r["l1h_matched"] > 0 and r["l1g_noncash_matched"] / r["l1h_matched"] < 0.25),
            ("part_iii_all_years", lambda r: r["support_group"] == "part_iii_all_years"),
            ("no_support_schedule", lambda r: r["support_group"] == "no_support_schedule"),
            ("mixed_or_missing", lambda r: r["support_group"] == "mixed_or_missing"),
            *((f"part_ii_band_{b}", (lambda r, b=b: p2(r) and r["revenue_band"] == b))
              for b in ("a_lt_1m", "b_1m_5m", "c_5m_25m", "d_25m_100m", "e_ge_100m")))


def measures_for(scope: str) -> tuple:
    base = ("daf_share_1f",) + tuple(f"daf_share_1f_net_{k}" for k in ALLOC) + tuple(f"large_donor_share_of_1f_{k}" for k in ALLOC)
    return base + (("daf_share_1f_net_p3_7a", "dq_share_of_1f_p3_7a") if scope == "part_iii_all_years" else ())


def build_summaries(rows: Sequence[Mapping], reps: int, seed: int) -> list:
    w = weights_a(rows)
    return [summary(sc, m, [r for r in rows if pred(r)], w, reps, seed + 31 * i + j)
            for i, (sc, pred) in enumerate(scopes()) for j, m in enumerate(measures_for(sc))]


def sponsor_status(dafrc: Sequence[Mapping], found: Mapping, n: int = 50) -> list:
    """Top-n FY2024 DAFRC sponsors (by DAF assets) by BMF FOUNDATION code, weighted by FY2024 DAF grants."""
    fy24 = sorted((r for r in dafrc if r["fiscal_year_end"] == "2024" and r["eoy_daf_assets"]), key=lambda r: -float(r["eoy_daf_assets"]))[:n]
    tot = sum(float(r["total_daf_grants"] or 0) for r in fy24)
    by = _group_by_fast(fy24, lambda r: found.get(ein9(r["ein"]), "not_in_bmf"))
    return [{"row_type": "sponsor_status", "scope": "top50_fy2024_daf_assets", "measure": f"bmf_foundation_{code}",
             "sampled": len(v), "weighted_num_usd": round(sum(float(r["total_daf_grants"] or 0) for r in v)),
             "pooled": sum(float(r["total_daf_grants"] or 0) for r in v) / tot if tot else None,
             "source": "DAFRC 2025 dataset (FY2024 total_daf_grants) x IRS EO BMF FOUNDATION ("
                       + FOUNDATION_CODES.get(code, code) + ")"}
            for code, v in sorted(by.items())]


# ----------------------------------------------------------------------------- main
FIELDS = ("row_type", "scope", "measure", "sampled", "respondents", "weighted_recipients", "dropped_1f_nonpos",
          "p25", "median", "median_ci95_lo", "median_ci95_hi", "p75", "pooled", "pooled_ci95_lo", "pooled_ci95_hi",
          "share_gt_100pct", "share_den_absorbed", "weighted_num_usd", "weighted_den_usd",
          "ein", "name", "ntee_major_group", "revenue_band", "stratum", "stratum_N", "status", "years_matched",
          "object_ids", "forms", "schedule_a_parts", "schedule_a_status", "support_group", "part1_indicators",
          "num_daf_weighted_matched", "l1f_matched", "l1h_matched", "l1g_noncash_matched", "sa_p2_l1_cy_matched", "sa_p2_l1_5y_matched", "sa_p2_l5_matched",
          "excess_ratio_5y", "sa_l1_cy_over_1f", "sa_l1_cy_over_1h", "excess_cy", "excess_avg", "excess_all", "capped_cy", "capped_avg",
          "capped_all", "sa_p3_l1_cy_matched", "sa_p3_l7a_cy_matched", "share_1f", "share_1f_net_cy", "share_1f_net_avg",
          "share_1f_net_all", "share_1f_net_p3_7a", "large_share_cy", "large_share_avg", "large_share_all",
          "large_share_p3_7a", "source")


def load_p8(cache: str, oids: Sequence[str]) -> dict:
    def one(o):
        p = os.path.join(cache, f"{o}.json")
        if not os.path.exists(p):
            return o, None
        with open(p, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("status") != "ok":
            return o, None
        return o, (c.get("ez_l1") if c.get("form") == "IRS990EZ" else (c.get("l1f") or 0.0))
    return dict(one(o) for o in oids)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--sa-cache", required=True)
    ap.add_argument("--p8-cache", default="", help="committed Part VIII per-return cache (q1226/f990p8) for per-year 1f")
    ap.add_argument("--bmf-dir", default="")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args(argv)
    os.chdir(a.root)
    rec_in = tuple({**r, "stratum_N": int(r["stratum_N"])} for r in read_csv(IN_A) if r["row_type"] == "recipient")
    oids = tuple(o for r in rec_in for o in r["object_ids"].split(";") if o)
    with ThreadPoolExecutor(a.workers) as ex:
        sa = dict(zip(oids, ex.map(lambda o: fetch_sched_a(o, a.sa_cache, a.fetch), oids)))
    p8 = load_p8(a.p8_cache, oids) if a.p8_cache else {}
    rows = tuple(recipient(r, sa, p8) for r in rec_in)
    summ = build_summaries(rows, a.boot, a.seed)
    dafrc = read_csv(DAFRC_CSV)
    found = load_bmf_foundation(a.bmf_dir, frozenset(ein9(r["ein"]) for r in dafrc)) if a.bmf_dir else {}
    spons = sponsor_status(dafrc, found) if found else []
    write_csv(OUT, summ + spons + list(rows), FIELDS)
    st = _group_by_fast(sa.values(), lambda x: x.get("status"))
    ok = tuple(r for r in rows if r["status"] == "ok")
    w = weights_a(rows)
    print(json.dumps({
        "returns": len(oids), "sched_a_status": {k: len(v) for k, v in st.items()},
        "p8_per_year_1f_found": sum(v is not None for v in p8.values()),
        "support_group_ok": {k: len(v) for k, v in _group_by_fast(ok, lambda r: r["support_group"]).items()},
        "support_group_ok_weighted": {k: round(sum(w[r["stratum"]] for r in v)) for k, v in _group_by_fast(ok, lambda r: r["support_group"]).items()},
        "support_group_ok_num_share": {k: sum(w[r["stratum"]] * r["num_daf_weighted_matched"] for r in v) / sum(w[r["stratum"]] * r["num_daf_weighted_matched"] for r in ok)
                                       for k, v in _group_by_fast(ok, lambda r: r["support_group"]).items()},
        "capped_counts": {k: sum(r[f"capped_{k}"] for r in ok) for k in ALLOC},
        "sa_l1_cy_over_1f_weighted_median_part_ii": wquantile([(r["sa_l1_cy_over_1f"], w[r["stratum"]]) for r in ok if r["support_group"] == "part_ii_all_years"], 0.5),
        "sa_l1_cy_over_1h_weighted_quartiles_part_ii": [wquantile([(r["sa_l1_cy_over_1h"], w[r["stratum"]]) for r in ok if r["support_group"] == "part_ii_all_years"], q) for q in (0.25, 0.5, 0.75)],
        "part_ii_l5_zero_weighted_share": sum(w[r["stratum"]] for r in ok if r["support_group"] == "part_ii_all_years" and not r["sa_p2_l5_matched"]) / sum(w[r["stratum"]] for r in ok if r["support_group"] == "part_ii_all_years"),
        "part_ii_l5_zero_count": sum(1 for r in ok if r["support_group"] == "part_ii_all_years" and not r["sa_p2_l5_matched"]),
        "rows": len(summ) + len(spons) + len(rows)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
