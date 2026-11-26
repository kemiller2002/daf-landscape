#!/usr/bin/env python3
"""Payout-definition bridge on the corrected FY2020-24 DAFRC sponsor panel (queue item P-B39N8-01).

Stdlib only; functional style (pure transforms, I/O at the edges). Nothing is parsed anew from Form 990 XML.

Inputs
  * data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv   DAFRC 2025 panel, as published
  * data/mission-2026-11-14/dafrc-corrections-itemized.csv             rules R1-R4; applied = 1 rows override DAFRC
                                                                        (same merge as scripts/mission_league_table.py)
  * data/mission-2026-11-14/dafrc-corrected-market-totals.csv          check: rebuilt sums = corrected totals
  * data/mission-2026-11-14/dafrc-market-totals-netted.csv             check: rebuilt R5 outbound = netting amounts
  * --np-cache DIR: the netpayout990/ Schedule I cache of scripts/mission_net_payout.py. R5 DAF-to-DAF lines are
    attributed to each grantor with scripts/mission_league_table.netting_by_sponsor (which reuses
    scripts/mission_market_netting.py unchanged). Without it the net rows are skipped.
  * --ips-dir DIR: IPS "Independent Report on DAFs" (April 2025) supporting files
      Independent-DAF-Report-Sponsor-Lists.xlsx   (one sheet per year 2020-2023, one row per sponsor)
      Independent-DAF-Report-Summary-Table.xlsx   (published medians)
    --fetch-ips downloads them from inequality.org after checking robots.txt (urllib.robotparser) and logs the result.

Definitions (FY = calendar year in which the sponsor's tax period ends; DAFRC, NPT and IPS convention)
  beg   (a) grants_t / EOY DAF assets_{t-1}                 sponsor needs a row in t-1 with assets_{t-1} > 0
  irs   (b) grants_t / (EOY DAF assets_t + grants_t)          IRS SOI / IPS formula; needs assets_t >= 0, denominator > 0
  Statistics per (FY, formula, sample, netting): median, pooled (sum numerators / sum denominators over the same
  sponsor-years), p25, p75, mean, share below 5%, account-weighted median (each sponsor-year weighted by its
  corrected EOY account count = the rate of the median account if every account paid its sponsor's rate).
  Samples
    all_incl_proc       every sponsor-year meeting the formula's condition (processors included, as NPT and IPS)
    ex_proc             processors (DAFRC subtype 'Donation Processor') removed
    ex_proc_ge1m        ex_proc and the formula's asset term >= $1m (beg: assets_{t-1}; irs: assets_t + grants_t)
    incl_proc_ge1m      all_incl_proc with the same $1m filter
    ex_proc_ge1m_filed  ex_proc_ge1m restricted to sponsor-years whose grants and asset values are not imputed
                        after correction (the repo's earlier 11-12.5% median used filed values only)
    *_matched           sponsor-years that qualify for BOTH formulas (assets_{t-1} > 0, assets_t >= 0); the $1m
                        filter then needs both asset terms >= $1m. The decomposition uses only matched samples.
  Netting: gross, or R5 lower / central / upper (FY2021-24 only): grants_t minus the grantor's capped R5 outbound
  amount, floored at 0 (same floor as scripts/mission_batch38_data.py triad). Assets are not changed.
  IPS reproduction: (i) IPS's own sponsor list -> median of its 'Average DAF Payout' and of grants/(assets+grants);
  (ii) the repo panel with IPS's universe rules where the panel allows them (assets_t > 0, processors in, IPS's
  Schedule D deficiency screens); (iii) EIN-matched comparison and a universe/value split of the gap.
  Decomposition (FY2023 headline; every FY in the CSV): 2 denominators x 3 weightings (pooled, median sponsor,
  account-weighted median), Shapley averages over the other factor; residual to the DAFRC 2024 account median [I].

Usage
  python3 scripts/mission_payout_bridge.py . --np-cache NPCACHE --ips-dir IPSDIR [--fetch-ips]
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import statistics
import sys
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_URL, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_net_payout import segment_of  # noqa: E402

FYS_PANEL = (2019, 2020, 2021, 2022, 2023, 2024)
FYS_CORR = (2020, 2021, 2022, 2023, 2024)
FYS_OUT = (2020, 2021, 2022, 2023, 2024)
FYS_NET = (2021, 2022, 2023, 2024)
TIERS = ("lower", "central", "upper")
MIN_ASSETS = 1e6
METRICS = {"daf_assets_eoy": ("eoy_daf_assets", "source_eoy_daf_assets"),
           "daf_contributions": ("total_daf_contributions", "source_total_daf_contributions"),
           "daf_grants": ("total_daf_grants", "source_total_daf_grants"),
           "daf_accounts_eoy": ("number_of_daf_accounts", "source_number_of_accounts")}
SAMPLES = ("all_incl_proc", "ex_proc", "ex_proc_ge1m", "incl_proc_ge1m", "ex_proc_ge1m_filed",
           "all_incl_proc_matched", "ex_proc_matched", "ex_proc_ge1m_matched")
FORMULAS = {"beg": "grants_t / EOY DAF assets_(t-1)", "irs": "grants_t / (EOY DAF assets_t + grants_t)"}

IPS_HOST = "https://inequality.org"
IPS_FILES = {"lists": "Independent-DAF-Report-Sponsor-Lists.xlsx", "summary": "Independent-DAF-Report-Summary-Table.xlsx"}
IPS_URL = IPS_HOST + "/wp-content/uploads/2025/04/{f}"
IPS_PDF = "https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf"
IPS_PAGE = "https://www.ips-dc.org/independent-report-on-dafs/"
NPT_URL = "https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/"
DAFRC_ACCT_URL = "https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf"
DAFRC_STUDY_URL = "https://www.dafresearchcollaborative.org/s/DAFRC-National-Study-DAFs-Feb-2024.pdf"
UA = "research-script/1.0"

# Quoted external benchmarks (value as a ratio). Each is quoted, not computed.
BENCH = (
    ("npt_aggregate_fy2023", 2023, "beg", "pooled", 0.239, "NPT 2024 DAF Report: aggregate payout, all sponsors, grants / prior-year assets (as quoted by IPS 2025 p.14; repo daf-market-annual-series.csv)", NPT_URL + " ; " + IPS_PDF),
    ("ips_median_fy2023_text", 2023, "irs", "median", 0.097, "IPS 2025: 'median DAF payout rate across all sponsors was 9.7 percent in 2023' (p.14)", IPS_PDF),
    ("dafrc_account_median_all", 2022, "dafrc_3yr_account", "median_account", 0.09, "DAFRC 2024 National Study: median 3-year (2020-22) account payout, all accounts, 111 programs, >50,000 accounts", DAFRC_ACCT_URL + " ; " + DAFRC_STUDY_URL),
    ("dafrc_account_median_active", 2022, "dafrc_3yr_account", "median_account_active", 0.15, "DAFRC 2024: median for accounts that made grants (inactive removed)", DAFRC_ACCT_URL),
    ("dafrc_account_mean_all", 2022, "dafrc_3yr_account", "mean_account", 0.18, "DAFRC 2024: mean payout rate, all accounts", DAFRC_ACCT_URL),
    ("dafrc_account_inactive_share", 2022, "dafrc_3yr_account", "share_zero_payout", 0.22, "DAFRC 2024: about 22% of DAFs inactive (zero payout) in 2020-22", DAFRC_ACCT_URL),
)


# ----------------------------------------------------------------------------- generic pure helpers
def ratio(n: float | None, d: float | None) -> float | None:
    return n / d if n is not None and d not in (None, 0) else None


def median(xs: Sequence[float]) -> float | None:
    return statistics.median(xs) if xs else None


def quantile(xs: Sequence[float], q: float) -> float | None:
    """Linear-interpolation quantile (statistics.quantiles 'inclusive')."""
    if len(xs) < 2:
        return xs[0] if xs else None
    return statistics.quantiles(xs, n=100, method="inclusive")[round(q * 100) - 1]


def weighted_median(pairs: Sequence[tuple[float, float]]) -> float | None:
    """Lower weighted median: smallest x whose cumulative weight reaches half the total weight."""
    ps = sorted((x, w) for x, w in pairs if w and w > 0)
    if not ps:
        return None
    tot = sum(w for _, w in ps)
    return next(x for (x, _), c in zip(ps, itertools.accumulate(w for _, w in ps)) if c >= tot / 2)


def stats_of(items: Sequence[Mapping]) -> dict:
    """items: {'num','den','acc'} -> statistics dict."""
    rs = sorted(i["num"] / i["den"] for i in items)
    return {"n": len(rs), "median": median(rs), "pooled": ratio(sum(i["num"] for i in items), sum(i["den"] for i in items)),
            "p25": quantile(rs, 0.25), "p75": quantile(rs, 0.75), "mean": statistics.fmean(rs) if rs else None,
            "share_below_5pct": ratio(sum(1 for r in rs if r < 0.05), len(rs)),
            "account_weighted_median": weighted_median([(i["num"] / i["den"], i["acc"] or 0) for i in items]),
            "numerator": sum(i["num"] for i in items), "denominator": sum(i["den"] for i in items),
            "accounts": sum(i["acc"] or 0 for i in items)}


# ----------------------------------------------------------------------------- corrected panel (repo R1-R4 method)
def corrected_panel(dafrc: Sequence[Mapping], items: Sequence[Mapping]) -> dict:
    """(ein, fy) -> metric values + imputed flags + segment. DAFRC as published, overridden by applied R1-R4 rows
    (FY2020-24; FY2019 is the published baseline used only as beginning assets for FY2020)."""
    latest = {e: max(rs, key=lambda r: r["fiscal_year_end"]) for e, rs in _group_by_fast(dafrc, lambda r: ein9(r["ein"])).items()}
    seg_d = {e: segment_of(r["type"], r["subtype"]) for e, r in latest.items()}
    seg_i = {ein9(r["ein"]): segment_of(r["type"], "") for r in items}
    base = {(ein9(r["ein"]), int(r["fiscal_year_end"])): {
        **{m: num(r[c[0]]) for m, c in METRICS.items()},
        **{f"{m}_imputed": r[c[1]] == "Imputed" for m, c in METRICS.items()}}
        for r in dafrc if int(r["fiscal_year_end"]) in FYS_PANEL}
    over = _group_by_fast((r for r in items if r["applied"] == "1" and int(r["fiscal_year"]) in FYS_CORR),
                          lambda r: (ein9(r["ein"]), int(r["fiscal_year"])))

    def merge(k):
        b = base.get(k, {**{m: None for m in METRICS}, **{f"{m}_imputed": False for m in METRICS}})
        o = {r["metric"]: num(r["corrected_value"]) or 0.0 for r in over.get(k, ())}
        return {**b, **o, **{f"{m}_imputed": b[f"{m}_imputed"] and m not in o for m in METRICS},
                "rules": ";".join(sorted({r["rule"] for r in over.get(k, ())})), "in_dafrc": k in base,
                "segment": seg_d.get(k[0]) or seg_i.get(k[0], "single_issue"),
                "name": latest[k[0]]["name"] if k[0] in latest else next(r["name"] for r in items if ein9(r["ein"]) == k[0])}
    return {k: merge(k) for k in set(base) | set(over)}


def panel_check(panel: Mapping, totals: Sequence[Mapping]) -> dict:
    tot = {(int(r["fiscal_year"]), r["metric"]): float(r["corrected_value"]) for r in totals}
    return {f"{fy}_{m}": {"rebuilt": round(sum(v[m] or 0 for (e, y), v in panel.items() if y == fy)), "corrected_total": round(tot[(fy, m)])}
            for fy in FYS_CORR for m in ("daf_assets_eoy", "daf_grants")}


# ----------------------------------------------------------------------------- sponsor-year rate items
def rate_item(panel: Mapping, ein: str, fy: int, formula: str, out_amt: float) -> dict | None:
    cur, prev = panel.get((ein, fy)), panel.get((ein, fy - 1))
    if not cur or cur["daf_grants"] is None:
        return None
    g = max(cur["daf_grants"] - out_amt, 0.0)
    if formula == "beg":
        a0 = (prev or {}).get("daf_assets_eoy")
        if a0 is None or a0 <= 0:
            return None
        den, asset_term, imp = a0, a0, cur["daf_grants_imputed"] or prev["daf_assets_eoy_imputed"]
    else:
        a1 = cur["daf_assets_eoy"]
        if a1 is None or a1 < 0 or (a1 + g) <= 0:
            return None
        den, asset_term, imp = a1 + g, a1 + g, cur["daf_grants_imputed"] or cur["daf_assets_eoy_imputed"]
    a0, a1 = (prev or {}).get("daf_assets_eoy"), cur["daf_assets_eoy"]
    both = a0 is not None and a0 > 0 and a1 is not None and a1 >= 0 and (a1 + g) > 0
    return {"ein": ein, "fy": fy, "num": g, "den": den, "asset_term": asset_term, "imputed": imp,
            "segment": cur["segment"], "acc": cur["daf_accounts_eoy"], "both": both,
            "matched_size": min(a0, a1 + g) if both else 0.0}


def in_sample(it: Mapping, sample: str) -> bool:
    proc_ok = sample.startswith("all") or sample.startswith("incl") or it["segment"] != "processor"
    matched = sample.endswith("matched")
    size_ok = "ge1m" not in sample or (it["matched_size"] if matched else it["asset_term"]) >= MIN_ASSETS
    filed_ok = not sample.endswith("filed") or not it["imputed"]
    return proc_ok and size_ok and filed_ok and (not matched or it["both"])


def grid_rows(panel: Mapping, outs: Mapping | None) -> tuple[dict, ...]:
    eins = sorted({e for e, _ in panel})
    nettings = ("gross",) + (tuple(f"r5_{t}" for t in TIERS) if outs else ())

    def items(fy, formula, net):
        out = (lambda e: 0.0) if net == "gross" else (lambda e: outs[net[3:]]["out"].get((e, fy), 0.0))
        return tuple(x for x in (rate_item(panel, e, fy, formula, out(e)) for e in eins) if x)

    def rows(fy, formula, net):
        its = items(fy, formula, net)
        return tuple({"section": "panel_payout", "fiscal_year": fy, "formula": formula, "sample": s, "netting": net,
                      **stats_of(tuple(i for i in its if in_sample(i, s)))} for s in SAMPLES)
    return tuple(r for fy in FYS_OUT for f in FORMULAS for net in nettings
                 if net == "gross" or fy in FYS_NET for r in rows(fy, f, net))


def market_rows(panel: Mapping, outs: Mapping | None) -> tuple[dict, ...]:
    """Market-total beginning-asset payout (all grants_t / all assets_{t-1}, every sponsor-year): the NPT/DAFRC
    convention, which also counts grants of sponsors without a prior-year row."""
    def one(fy, net):
        g = sum(v["daf_grants"] or 0 for (e, y), v in panel.items() if y == fy)
        a0 = sum(v["daf_assets_eoy"] or 0 for (e, y), v in panel.items() if y == fy - 1)
        o = 0.0 if net == "gross" else sum(x for (e, y), x in outs[net[3:]]["out"].items() if y == fy)
        return {"section": "market_total", "fiscal_year": fy, "formula": "beg", "sample": "market_all_rows", "netting": net,
                "pooled": ratio(g - o, a0), "numerator": g - o, "denominator": a0}
    nets = ("gross",) + (tuple(f"r5_{t}" for t in TIERS) if outs else ())
    return tuple(one(fy, n) for fy in FYS_OUT for n in nets if n == "gross" or fy in FYS_NET)


# ----------------------------------------------------------------------------- IPS files (stdlib xlsx reader)
XNS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def _colidx(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref).group(0)
    return sum((ord(c) - 64) * 26 ** i for i, c in enumerate(reversed(letters))) - 1


def read_xlsx(path: str) -> dict[str, tuple[tuple[str, ...], ...]]:
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        ss = tuple("".join(t.text or "" for t in si.iter(f"{{{XNS['m']}}}t"))
                   for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", XNS)) if "xl/sharedStrings.xml" in names else ()
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
        sheets = ET.fromstring(z.read("xl/workbook.xml")).find("m:sheets", XNS)

        def cell(c):
            v, t = c.find("m:v", XNS), c.get("t")
            if t == "inlineStr":
                return "".join(x.text or "" for x in c.iter(f"{{{XNS['m']}}}t"))
            return "" if v is None else (ss[int(v.text)] if t == "s" else v.text)

        def row(r):
            d = {_colidx(c.get("r")): cell(c) for c in r.findall("m:c", XNS)}
            return tuple(d.get(i, "") for i in range(max(d) + 1)) if d else ()

        def sheet(s):
            tgt = rels[s.get(f"{{{XNS['r']}}}id")].lstrip("/")
            tgt = tgt if tgt.startswith("xl/") else "xl/" + tgt
            return tuple(row(r) for r in ET.fromstring(z.read(tgt)).iter(f"{{{XNS['m']}}}row"))
        return {s.get("name"): sheet(s) for s in sheets}


def ips_sponsors(book: Mapping) -> dict[int, tuple[dict, ...]]:
    def recs(rows):
        hdr = rows[0]
        return tuple(dict(zip(hdr, r + ("",) * (len(hdr) - len(r)))) for r in rows[1:] if r and r[0])
    return {int(k): recs(v) for k, v in book.items() if k.isdigit()}


def ips_published_medians(book: Mapping) -> dict[int, float]:
    rows = next(iter(book.values()))
    years = rows[0]
    med = next(r for r in rows if r and r[0] == "Median aggregate DAF payout rate")
    return {int(y): float(v) for y, v in zip(years, med) if y.isdigit() and v}


def ips_deficient(acc: float | None, contrib: float | None, grants: float | None, assets: float | None) -> bool:
    """IPS Appendix A screens that the Schedule D panel can apply (total-grants, 501(c)(3) and submission-date
    screens need the full return and are not applied)."""
    return any((grants is not None and grants < 0, contrib is not None and contrib < 0, acc is None or acc <= 0,
                acc is not None and acc == contrib, acc is not None and acc == grants,
                acc is not None and assets is not None and acc >= assets, assets is not None and assets == grants))


def ips_rows(panel: Mapping, sponsors: Mapping, published: Mapping) -> tuple[dict, ...]:
    def ips_rate(r):
        a, g = num(r["DAF Assets"]), num(r["Grants from DAFs"])
        return ratio(g, (a or 0) + (g or 0)) if g is not None and a is not None else None

    def repo_items(fy, screens, filed_only, grants_pos=False):
        def ok(e, v):
            return (v["daf_assets_eoy"] or 0) > 0 and v["daf_grants"] is not None and (not grants_pos or v["daf_grants"] > 0) and \
                (not screens or not ips_deficient(v["daf_accounts_eoy"], v["daf_contributions"], v["daf_grants"], v["daf_assets_eoy"])) and \
                (not filed_only or not (v["daf_grants_imputed"] or v["daf_assets_eoy_imputed"]))
        return {e: v["daf_grants"] / (v["daf_assets_eoy"] + v["daf_grants"]) for (e, y), v in panel.items() if y == fy and ok(e, v)}

    def year(fy):
        ips = {ein9(r["EIN"]): r for r in sponsors.get(fy, ())}
        ips_pub = {e: num(r["Average DAF Payout"]) for e, r in ips.items() if num(r["Average DAF Payout"]) is not None}
        ips_re = {e: ips_rate(r) for e, r in ips.items() if ips_rate(r) is not None}
        recompute_diff = max((abs(ips_pub[e] - ips_re[e]) for e in ips_pub if e in ips_re), default=None)
        base = {"section": "ips_reproduction", "fiscal_year": fy, "formula": "irs", "netting": "gross"}
        out = [
            {**base, "sample": "ips_published_summary_table", "median": published.get(fy), "basis": "Q",
             "note": "IPS Summary Table 'Median aggregate DAF payout rate', all sponsors"},
            {**base, "sample": "ips_sponsor_list_published_rate", "n": len(ips_pub), "median": median(sorted(ips_pub.values())),
             "pooled": ratio(sum(num(ips[e]["Grants from DAFs"]) for e in ips_pub), sum(num(ips[e]["Grants from DAFs"]) + num(ips[e]["DAF Assets"]) for e in ips_pub)),
             "basis": "F", "note": f"median of IPS's own 'Average DAF Payout' column; max |published - recomputed g/(a+g)| = {recompute_diff}"},
            {**base, "sample": "ips_sponsor_list_ex_proc", "n": sum(1 for e in ips_pub if ips[e]["Sponsor Type"] != "Donation Processor"),
             "median": median(sorted(v for e, v in ips_pub.items() if ips[e]["Sponsor Type"] != "Donation Processor")), "basis": "F",
             "note": "IPS list without IPS-classified donation processors"},
        ]
        blank = [e for e, r in ips.items() if r["Grants from DAFs"] == ""]
        out.append({**base, "sample": "ips_sponsor_list_blank_grants_as_zero", "n": len(ips_pub) + len(blank),
                    "median": median(sorted([*ips_pub.values(), *[0.0] * len(blank)])), "basis": "F",
                    "note": f"counterfactual: IPS list with the {len(blank)} sponsors whose DAF-grants cell is blank (no payout computed, so "
                            "outside IPS's median) counted as 0% payout"})
        variants = (("repo_assets_gt0_no_screens", False, False, False), ("repo_assets_gt0_ips_screens", True, False, False),
                    ("repo_assets_gt0_ips_screens_filed_only", True, True, False),
                    ("repo_assets_gt0_grants_gt0_ips_screens", True, False, True))
        for label, scr, filed, gpos in variants:
            rp = repo_items(fy, scr, filed, gpos)
            inter = sorted(set(rp) & set(ips_pub))
            m_repo, m_ips = median(sorted(rp.values())), median(sorted(ips_pub.values()))
            m_int_repo, m_int_ips = median(sorted(rp[e] for e in inter)), median(sorted(ips_pub[e] for e in inter))
            only_repo, only_ips = sorted(set(rp) - set(ips_pub)), sorted(set(ips_pub) - set(rp))
            same = sum(1 for e in inter if abs(rp[e] - ips_pub[e]) < 0.0005)
            out.append({**base, "sample": label, "n": len(rp), "median": m_repo, "basis": "F",
                        "ips_n": len(ips_pub), "ips_median": m_ips, "n_intersection": len(inter),
                        "median_intersection_repo_values": m_int_repo, "median_intersection_ips_values": m_int_ips,
                        "n_repo_only": len(only_repo), "median_repo_only": median(sorted(rp[e] for e in only_repo)),
                        "n_ips_only": len(only_ips), "median_ips_only": median(sorted(ips_pub[e] for e in only_ips)),
                        "n_intersection_rate_within_0_05pt": same,
                        "gap_total": None if None in (m_repo, m_ips) else m_repo - m_ips,
                        "gap_universe_repo_side": None if None in (m_repo, m_int_repo) else m_repo - m_int_repo,
                        "gap_values_on_intersection": None if None in (m_int_repo, m_int_ips) else m_int_repo - m_int_ips,
                        "gap_universe_ips_side": None if None in (m_int_ips, m_ips) else m_int_ips - m_ips,
                        "note": "repo corrected panel, sponsor-years with EOY DAF assets > 0" +
                                (", IPS Schedule D deficiency screens" if scr else "") + (", grants and assets not imputed" if filed else "") +
                                (", DAF grants > 0 (bound for IPS dropping blank grants cells)" if gpos else "")})
        return tuple(out)
    return tuple(r for fy in sorted(sponsors) for r in year(fy))


def ips_universe_profile(panel: Mapping, sponsors: Mapping, fy: int = 2023) -> dict:
    """Who is in the repo-only and IPS-only sets (same sets as ips_rows, no screens), for the gap explanation."""
    ips_all = {ein9(r["EIN"]): r for r in sponsors.get(fy, ())}
    ips_pub = {e: num(r["Average DAF Payout"]) for e, r in ips_all.items() if num(r["Average DAF Payout"]) is not None}
    rp = {e: v for (e, y), v in panel.items() if y == fy and (v["daf_assets_eoy"] or 0) > 0 and v["daf_grants"] is not None}
    rate = lambda v: v["daf_grants"] / (v["daf_assets_eoy"] + v["daf_grants"])  # noqa: E731
    only_repo = {e: rp[e] for e in rp if e not in ips_pub}
    only_ips = {e: ips_all[e] for e in ips_pub if e not in rp}
    cnt = lambda xs, f: {k: len(v) for k, v in _group_by_fast(xs, f).items()}  # noqa: E731
    in_dafrc_ever = lambda e: any((e, y) in panel for y in FYS_PANEL)  # noqa: E731
    blank = {e for e, r in ips_all.items() if r["Grants from DAFs"] == ""}
    return {"fy": fy, "ips_rows_total": len(ips_all), "ips_rows_with_payout": len(ips_pub),
            "ips_rows_blank_grants_dropped": len(blank),
            "ips_rows_zero_grants_kept": sum(1 for e in ips_pub if ips_pub[e] == 0),
            "ips_median_blank_grants_as_zero": median(sorted([*ips_pub.values(), *[0.0] * len(blank)])),
            "repo_n": len(rp), "repo_zero_grants": sum(1 for v in rp.values() if (v["daf_grants"] or 0) == 0),
            "repo_only_n": len(only_repo), "repo_only_by_segment": cnt(list(only_repo.values()), lambda v: v["segment"]),
            "repo_only_in_ips_with_blank_grants": sum(1 for e in only_repo if e in blank),
            "repo_only_absent_from_ips_list": sum(1 for e in only_repo if e not in ips_all),
            "repo_only_zero_grants": sum(1 for v in only_repo.values() if (v["daf_grants"] or 0) == 0),
            "repo_only_imputed_grants_or_assets": sum(1 for v in only_repo.values() if v["daf_grants_imputed"] or v["daf_assets_eoy_imputed"]),
            "repo_only_median_rate": median(sorted(map(rate, only_repo.values()))),
            "repo_only_absent_from_ips_median_rate": median(sorted(rate(v) for e, v in only_repo.items() if e not in ips_all)),
            "ips_only_n": len(only_ips), "ips_only_by_type": cnt(list(only_ips.values()), lambda r: r["Sponsor Type"]),
            "ips_only_in_dafrc_same_fy": sum(1 for e in only_ips if (e, fy) in panel),
            "ips_only_in_dafrc_other_fy_only": sum(1 for e in only_ips if (e, fy) not in panel and in_dafrc_ever(e)),
            "ips_only_never_in_dafrc": sum(1 for e in only_ips if not in_dafrc_ever(e)),
            "ips_only_median_rate": median(sorted(ips_pub[e] for e in only_ips)),
            "ips_only_median_daf_assets": median(sorted(num(r["DAF Assets"]) or 0 for r in only_ips.values())),
            "ips_type_counts": cnt(list(ips_all.values()), lambda r: r["Sponsor Type"])}


# ----------------------------------------------------------------------------- decomposition
def decomposition_rows(grid: Sequence[Mapping], market: Sequence[Mapping]) -> tuple[dict, ...]:
    """2 denominators (beg, irs) x 3 weightings (pooled P, median sponsor M, account-weighted median W).
    Shapley split of P_beg -> W_irs into denominator D and weighting (W1: P->M, W2: M->W); residual to the DAFRC
    account median (9%) is attributed to within-sponsor distribution plus sample/definition differences [I]."""
    g = {(r["fiscal_year"], r["formula"], r["sample"], r["netting"]): r for r in grid}
    mk = {(r["fiscal_year"], r["netting"]): r for r in market}
    acct = 0.09

    def one(fy, sample, net):
        a, b = g.get((fy, "beg", sample, net)), g.get((fy, "irs", sample, net))
        if not a or not b or None in (a["pooled"], b["pooled"], a["median"], b["median"]):
            return ()
        Pa, Pb, Ma, Mb, Wa, Wb = a["pooled"], b["pooled"], a["median"], b["median"], a["account_weighted_median"], b["account_weighted_median"]
        D = ((Pa - Pb) + (Wa - Wb)) / 2
        W1 = ((Pa - Ma) + (Pb - Mb)) / 2
        W2 = ((Ma - Wa) + (Mb - Wb)) / 2
        D_at_median = ((Pa - Pb) + (Ma - Mb)) / 2
        base = {"section": "decomposition", "fiscal_year": fy, "sample": sample, "netting": net, "basis": "F"}
        comp = (("P_beg", Pa), ("P_irs", Pb), ("M_beg", Ma), ("M_irs", Mb), ("W_beg", Wa), ("W_irs", Wb),
                ("market_total_beg", (mk.get((fy, net)) or {}).get("pooled")),
                ("D_denominator_shapley_P_to_W", D), ("W1_pooled_to_median_sponsor", W1),
                ("W2_median_sponsor_to_account_weighted", W2),
                ("D_denominator_shapley_P_to_M", D_at_median),
                ("check_Pbeg_minus_Wirs", Pa - Wb), ("check_D_plus_W1_plus_W2", D + W1 + W2))
        resid = (("R_within_sponsor_vs_W_irs", Wb - acct), ("R_within_sponsor_vs_W_beg", Wa - acct))
        return tuple({**base, "component": c, "value": v} for c, v in comp) + \
            tuple({**base, "component": c, "value": v, "basis": "I",
                   "note": "residual to DAFRC 2024 account median 9% (2020-22, 111 programs): within-sponsor distribution plus sample, period and definition differences"}
                  for c, v in resid)
    return tuple(r for fy in FYS_OUT for s in ("all_incl_proc_matched", "ex_proc_matched", "ex_proc_ge1m_matched") for n in ("gross", "r5_central")
                 if n == "gross" or fy in FYS_NET for r in one(fy, s, n))


def window_mean_rows(decomp: Sequence[Mapping], fys: Sequence[int] = (2020, 2021, 2022)) -> tuple[dict, ...]:
    """Mean of each decomposition component over FY2020-22, the DAFRC account study's three-year window (gross only)."""
    by = _group_by_fast((r for r in decomp if r["fiscal_year"] in fys and r["netting"] == "gross"),
                        lambda r: (r["sample"], r["component"]))
    return tuple({**rs[0], "fiscal_year": f"{fys[0]}-{fys[-1]}_mean",
                  "value": statistics.fmean(r["value"] for r in rs) if all(r["value"] is not None for r in rs) else None}
                 for (s, c), rs in by.items() if len(rs) == len(fys))


def bench_rows() -> tuple[dict, ...]:
    return tuple({"section": "external_benchmark", "row_label": k, "fiscal_year": fy, "formula": f, "statistic": st,
                  "value": v, "basis": "Q", "note": note, "source": src} for k, fy, f, st, v, note, src in BENCH)


# ----------------------------------------------------------------------------- long-format output
STAT_COLS = ("median", "pooled", "p25", "p75", "mean", "share_below_5pct", "account_weighted_median")
FIELDS = ("row_id", "section", "fiscal_year", "formula", "sample", "netting", "statistic", "value", "n_sponsor_years",
          "numerator_usd", "denominator_usd", "basis", "note", "source")
SRC_PANEL = ("DAFRC 2025 sponsor dataset (dafrc-sponsor-schedule-d-fy2019-2024.csv) + rules R1-R4 (dafrc-corrections-itemized.csv, applied=1)"
             " ; " + DAFRC_URL)
SRC_NET = " ; R5: Schedule I lines (netpayout990 cache) via scripts/mission_league_table.netting_by_sponsor = scripts/mission_market_netting.py"


def long_rows(grid, market, ips, decomp, bench) -> tuple[dict, ...]:
    def g_rows(r):
        src = SRC_PANEL + ("" if r["netting"] == "gross" else SRC_NET)
        return tuple({"section": r["section"], "fiscal_year": r["fiscal_year"], "formula": r["formula"], "sample": r["sample"],
                      "netting": r["netting"], "statistic": s, "value": r[s], "n_sponsor_years": r["n"],
                      "numerator_usd": round(r["numerator"]) if s == "pooled" else "",
                      "denominator_usd": round(r["denominator"]) if s == "pooled" else "", "basis": "F",
                      "note": "account weights = corrected EOY DAF accounts" if s == "account_weighted_median" else "", "source": src}
                     for s in STAT_COLS)
    m_rows = tuple({"section": r["section"], "fiscal_year": r["fiscal_year"], "formula": "beg", "sample": r["sample"], "netting": r["netting"],
                    "statistic": "pooled", "value": r["pooled"], "numerator_usd": round(r["numerator"]), "denominator_usd": round(r["denominator"]),
                    "basis": "F", "note": "all corrected grants_t / all corrected EOY assets_(t-1) (NPT/DAFRC market convention)",
                    "source": SRC_PANEL + ("" if r["netting"] == "gross" else SRC_NET)} for r in market)
    ips_src = f"{IPS_URL.format(f=IPS_FILES['lists'])} ; {IPS_URL.format(f=IPS_FILES['summary'])} ; {IPS_PDF} ; " + SRC_PANEL
    i_rows = tuple({"section": r["section"], "fiscal_year": r["fiscal_year"], "formula": "irs", "sample": r["sample"], "netting": "gross",
                    "statistic": k, "value": r.get(k), "n_sponsor_years": r.get("n", ""), "basis": r.get("basis", "F"),
                    "note": r.get("note", ""), "source": ips_src}
                   for r in ips for k in ("median", "pooled", "ips_median", "n_intersection", "median_intersection_repo_values",
                                          "median_intersection_ips_values", "n_repo_only", "median_repo_only", "n_ips_only",
                                          "median_ips_only", "n_intersection_rate_within_0_05pt", "gap_total",
                                          "gap_universe_repo_side", "gap_values_on_intersection", "gap_universe_ips_side")
                   if r.get(k) is not None)
    d_rows = tuple({"section": r["section"], "fiscal_year": r["fiscal_year"], "formula": "beg_vs_irs", "sample": r["sample"],
                    "netting": r["netting"], "statistic": r["component"], "value": r["value"], "basis": r["basis"],
                    "note": r.get("note", ""), "source": SRC_PANEL + " ; " + DAFRC_ACCT_URL} for r in decomp)
    b_rows = tuple({"section": r["section"], "fiscal_year": r["fiscal_year"], "formula": r["formula"], "sample": r["row_label"],
                    "netting": "gross", "statistic": r["statistic"], "value": r["value"], "basis": "Q", "note": r["note"],
                    "source": r["source"]} for r in bench)
    allr = tuple(x for r in grid for x in g_rows(r)) + m_rows + i_rows + d_rows + b_rows
    return tuple({**r, "row_id": f"PB{i + 1:04d}", "value": _fmt(r["value"])} for i, r in enumerate(allr))


def _fmt(v):
    return "" if v is None else (f"{v:.6g}" if isinstance(v, float) else v)


# ----------------------------------------------------------------------------- I/O edges
def fetch_ips(ips_dir: str) -> list[dict]:
    """Download the two IPS supporting files after a robots.txt check; returns a log."""
    rp = urllib.robotparser.RobotFileParser(IPS_HOST + "/robots.txt")
    rp.read()
    os.makedirs(ips_dir, exist_ok=True)

    def one(f):
        url = IPS_URL.format(f=f)
        allowed = rp.can_fetch(UA, url)
        if allowed:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r, open(os.path.join(ips_dir, f), "wb") as fh:
                fh.write(r.read())
        return {"url": url, "robots_allowed": allowed, "fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    return [one(f) for f in IPS_FILES.values()]


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--np-cache", default=None)
    ap.add_argument("--ips-dir", default=None)
    ap.add_argument("--fetch-ips", action="store_true")
    ap.add_argument("--out", default="data/mission-2026-11-14/payout-definition-bridge-2026-11-19.csv")
    a = ap.parse_args(argv)
    data = os.path.join(a.root, "data", "mission-2026-11-14")
    dafrc = read_csv(os.path.join(data, "dafrc-sponsor-schedule-d-fy2019-2024.csv"))
    items = read_csv(os.path.join(data, "dafrc-corrections-itemized.csv"))
    panel = corrected_panel(dafrc, items)
    check = panel_check(panel, read_csv(os.path.join(data, "dafrc-corrected-market-totals.csv")))
    outs = None
    if a.np_cache:
        import mission_league_table as lt  # noqa: E402
        outs = lt.netting_by_sponsor(a.np_cache, dafrc, items)
    net_pub = {(int(r["fiscal_year"]), r["tier"]): round(float(r["r5_netting_amount"]))
               for r in read_csv(os.path.join(data, "dafrc-market-totals-netted.csv")) if r["metric"] == "daf_grants"}
    net_check = {f"{fy}_{t}": {"rebuilt": round(sum(v for (e, y), v in outs[t]["out"].items() if y == fy)), "published": net_pub[(fy, t)]}
                 for fy in FYS_NET for t in TIERS} if outs else {}
    grid = grid_rows(panel, outs)
    market = market_rows(panel, outs)
    fetch_log = fetch_ips(a.ips_dir) if a.fetch_ips and a.ips_dir else []
    have_ips = a.ips_dir and all(os.path.exists(os.path.join(a.ips_dir, f)) for f in IPS_FILES.values())
    sponsors = ips_sponsors(read_xlsx(os.path.join(a.ips_dir, IPS_FILES["lists"]))) if have_ips else {}
    published = ips_published_medians(read_xlsx(os.path.join(a.ips_dir, IPS_FILES["summary"]))) if have_ips else {}
    ips = ips_rows(panel, sponsors, published) if have_ips else ()
    decomp = decomposition_rows(grid, market)
    decomp = decomp + window_mean_rows(decomp)
    rows = long_rows(grid, market, ips, decomp, bench_rows())
    write_csv(os.path.join(a.root, a.out), rows, FIELDS)
    pick = lambda fy, f, s, n="gross": next((r for r in grid if (r["fiscal_year"], r["formula"], r["sample"], r["netting"]) == (fy, f, s, n)), {})  # noqa: E731
    print(json.dumps({
        "panel_rebuild_check": check, "r5_rebuild_check": net_check, "rows_written": len(rows), "ips_fetch_log": fetch_log,
        "fy2023_headline": {f"{f}_{s}_{n}": {k: pick(2023, f, s, n).get(k) for k in ("n", "median", "pooled", "account_weighted_median")}
                            for f in FORMULAS for s in SAMPLES for n in ("gross", "r5_central")},
        "ips": [{k: r.get(k) for k in ("fiscal_year", "sample", "n", "median", "ips_n", "ips_median", "n_intersection",
                                       "median_intersection_repo_values", "median_intersection_ips_values", "n_repo_only", "median_repo_only",
                                       "n_ips_only", "median_ips_only", "n_intersection_rate_within_0_05pt", "gap_total",
                                       "gap_universe_repo_side", "gap_values_on_intersection", "gap_universe_ips_side", "note")} for r in ips],
        "ips_universe_profile_fy2023": ips_universe_profile(panel, sponsors) if have_ips else None,
        "decomposition_fy2023": [{k: r[k] for k in ("sample", "netting", "component", "value")} for r in decomp if r["fiscal_year"] == 2023],
        "decomposition_fy2020_22_mean": [{k: r[k] for k in ("sample", "component", "value")} for r in decomp
                                         if r["fiscal_year"] == "2020-2022_mean" and r["sample"] == "ex_proc_matched"],
    }, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
