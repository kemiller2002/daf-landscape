#!/usr/bin/env python3
"""Decompose the 15.1% coverage gap and bound the residual 1/0.849 scaling (P-B40N120201-01).

b40n1202-01 (mission_non_top50_numerator.py) measured the recipient DAF share with every itemising DAFRC 2025 panel
sponsor's Schedule I lines. Those lines reach 84.9% of netted FY2024 DAF grants (DAF-weighted, net of DAF-to-DAF).
This script splits the other 15.1% into parts measured from the same returns, then puts each part back into the
recipient numerator under explicit allocation rules, so that a bounded allocation replaces the 1/0.849 scaling.

Notation, per itemising sponsor-year: w = DAF weight used in b40n1202-01; D / Dc = DAFRC raw / corrected DAF grants;
L1, L2, L3 = Form 990 Part IX lines 1, 2, 3 (column A); SI = Schedule I Part II lines after totals rows are dropped,
split into DAF-to-DAF lines (d2d) and the rest.

Decomposition A (b40n1202-01 weights), exact identity per sponsor-year:
    Dc - w*SI_non_d2d = (Dc - D)            corrections_r1_r4 (dafrc-corrections-itemized.csv, applied rows)
                      + (D - w*(L1+L2+L3))  daf_weighting_haircut (zero when w = D / Part IX lines 1-3)
                      + w*L2                individual_grants_l2 (DAF grants cannot fund individuals, so this is a
                                            weighting artefact too)
                      + w*L3                foreign_grants_l3 (Part IX line 3; Schedule F)
                      + w*(L1 - SI)         non_itemised_domestic_l1_minus_sched_i (grants under $5,000 per recipient
                                            and any other line 1 dollars not itemised)
                      + w*SI_d2d            DAF-to-DAF lines dropped from the numerator
Decomposition B (re-weighted): w2 = min(1, Dc / (L1 + L3)), the DAF share of organisational grants on the same
DAFRC basis as the netted denominator. Then
    Dc - w2*SI_non_d2d = (Dc - w2*(L1+L3))  weight_cap_residual (only where Dc > L1 + L3)
                       + w2*L3 + w2*(L1 - SI) + w2*SI_d2d
    where w2*(L1 - SI) is reported separately for sponsor-years that itemise at least half of line 1
    (sub5k_full_itemisers) and for those that itemise less (sub5k_partial_itemisers: suspected partial itemisation,
    not small gifts).
Market, both: netted N = sum(Dc, all panel sponsors) - R5 netting (dafrc-market-totals-netted.csv, central), so
    N - covered = sum_itemising(terms) + sum_non_itemising(Dc) - R5 netting,
and the DAF-to-DAF terms are reported together as d2d_netting_residual = sum(weight*SI_d2d) - R5 netting.

Part IX lines 1-3 and Schedule F Part II are read from each panel sponsor-year's chosen return (the same return as
b40n1202-01: mission_daf_to_daf.pick_returns on the netpayout990 cache) on the GivingTuesday mirror of IRS TEOS, into
a new cache (--p9-cache).

Recipient side: the b40n1202-01 frames and samples are rebuilt with its helpers (same seeds; caches only). Each gap
component is spread over recipient-years by a key, as USD x key_r,fy / total key_fy, where the total includes blank-EIN
and out-of-frame destinations:
    all     DAF-weighted itemised numerator, all sponsors (the residual-scaling assumption)
    top50   the same, top-50 sponsors only (for BofA CGF and RCF, both top-50 national sponsors)
    small10 DAF-weighted itemised lines under $10,000 (closest observed analogue of sub-$5,000 gifts); used only for
            sub5k_full_itemisers; sub5k_partial_itemisers is always spread by `all`
    small5  DAF-weighted lines under $5,000 that some sponsors itemise voluntarily (sensitivity; small base)
Foreign grants, grants to individuals and the DAF-to-DAF residual reach no domestic recipient in every scenario.
Non-itemising sponsors' DAF grants are first cut to their domestic-organisation share L1/(L1+L3) (own return, else
the itemisers' ratio), then split like the itemisers' domestic grants into an itemised-like part, a sub-$5,000-like part
and a DAF-to-DAF-like part (which goes nowhere).

Pure functions; I/O only in the fetch/load helpers and `main`. Stdlib only. Imports mission_non_top50_numerator.py
and modifies nothing.

Usage:
  python3 scripts/mission_coverage_gap.py . --np-cache NPCACHE --lines-cache-top50 RCP_LINES --lines-cache Q120201_LINES \
      --bmf-dir BMF --index-dir IRSDIR --p8-cache Q1226_F990P8 --p8-cache-new Q120201_F990P8 --p9-cache NEW_P9 \
      [--fetch] [--boot 500]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from itertools import product
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_non_top50_numerator as n50  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_net_payout import norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import COST, WHITELIST, annotate, load_lines  # noqa: E402

base, rbe = n50.base, n50.rbe
OUT = os.path.join(DATA, "coverage-gap-decomposition-2026-11-20.csv")
CORR_CSV = os.path.join(DATA, "dafrc-corrections-itemized.csv")
BASES = n50.BASES
UA = "research-script/1.0"
P9_V = 1
P9_TAGS = {"GrantsToDomesticOrgsGrp": "l1", "GrantsToDomesticIndividualsGrp": "l2", "ForeignGrantsGrp": "l3",
           "TotalFunctionalExpensesGrp": "l25"}
SOURCE = ("Sponsors: IRS Form 990 Part IX lines 1-3, Schedule F Part II and Schedule I Part II of each DAFRC 2025 panel "
          "sponsor's chosen FY2023-24 return (GivingTuesday mirror of IRS TEOS XML, gt990datalake-rawdata.s3.amazonaws.com); "
          "DAFRC raw and corrected DAF grants (dafrc-sponsor-schedule-d-fy2019-2024.csv, dafrc-corrections-itemized.csv); "
          "R5 netting (dafrc-market-totals-netted.csv). Recipients: b40n1202-01 samples and Part VIII caches.")
COMP_A = ("corrections_r1_r4", "daf_weighting_haircut", "individual_grants_l2", "foreign_grants_l3",
          "non_itemised_domestic_l1_minus_sched_i", "non_itemising_sponsors", "d2d_netting_residual")
COMP_B = ("weight_cap_residual", "foreign_grants_l3", "sub5k_full_itemisers", "sub5k_partial_itemisers",
          "non_itemising_sponsors", "d2d_netting_residual")
PARTIAL = 0.5  # sponsor-year itemises less than this share of Part IX line 1: suspected partial itemisation


# ----------------------------------------------------------------------------- Part IX / Schedule F extract
def _amt(el, tag: str) -> float:
    return num(next((c.text for c in el if local(c.tag) == tag), None)) or 0.0


def parse_p9(stream) -> dict:
    """Part IX lines 1-3 and 25 (column A), Schedule F Part II and III row sums, Schedule I Part II row sums."""
    acc = {"l1": None, "l2": None, "l3": None, "l25": None, "sf_org_usd": 0.0, "sf_org_rows": 0, "sf_ind_usd": 0.0,
           "si_rows": 0, "si_usd": 0.0, "has_sched_f": False}
    for _, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        if tag in P9_TAGS and acc[P9_TAGS[tag]] is None:
            acc[P9_TAGS[tag]] = _amt(el, "TotalAmt")
        elif tag == "GrantsToOrgOutsideUSGrp":
            acc["sf_org_usd"] += _amt(el, "CashGrantAmt") + _amt(el, "NonCashAssistanceAmt")
            acc["sf_org_rows"] += 1
            el.clear()
        elif tag == "ForeignIndivGrantsGrp":
            acc["sf_ind_usd"] += _amt(el, "CashGrantAmt") + _amt(el, "NonCashAssistanceAmt")
            el.clear()
        elif tag == "RecipientTable":
            acc["si_usd"] += _amt(el, "CashGrantAmt") + _amt(el, "NonCashAssistanceAmt")
            acc["si_rows"] += 1
            el.clear()
        elif tag == "IRS990ScheduleF":
            acc["has_sched_f"] = True
            el.clear()
        elif tag.startswith("IRS990") and tag != "IRS990":
            el.clear()
    return acc


def fetch_p9(oid: str, cache: str, fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                c = json.load(fh)
        except (json.JSONDecodeError, OSError):
            c = {}
        if c.get("_v") == P9_V:
            return c
    if not fetch:
        return {"status": "not_fetched"}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=900) as resp:
                r = {**parse_p9(resp), "status": "ok", "_v": P9_V}
            os.makedirs(cache, exist_ok=True)
            with open(path + ".tmp", "w", encoding="utf-8") as fh:
                json.dump(r, fh)
            os.replace(path + ".tmp", path)
            return r
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"status": f"http_{e.code}"}
            time.sleep(3 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError):
            time.sleep(3 * (attempt + 1))
    return {"status": "error"}


def robots_check(cache: str) -> str:
    host = "gt990datalake-rawdata.s3.amazonaws.com"
    req = urllib.request.Request(f"https://{host}/robots.txt", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            code, body = r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        code, body = e.code, ""
    d = os.path.join(cache, "..", "robots")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "log.tsv"), "a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{host}\t{code}\t{len(body)}\n")
    blocked = code == 200 and any(l.strip().lower() in ("disallow: /", "disallow: /efiledata") for l in body.splitlines())
    return "blocked" if blocked else f"allowed_{code}"




# ----------------------------------------------------------------------------- sponsor-side decomposition
def corrected_deltas(rows: Sequence[Mapping]) -> dict:
    """(ein, fy) -> sum of applied R1-R4 deltas to DAF grants."""
    use = tuple(r for r in rows if r["metric"] == "daf_grants" and r["applied"] == "1")
    return {k: sum(num(r["delta"]) or 0.0 for r in v)
            for k, v in _group_by_fast(use, lambda r: (ein9(r["ein"]), int(r["fiscal_year"]))).items()}


def sponsor_row(k: tuple, p9: Mapping, x: Mapping, w: float, d_raw: float, d_corr: float, lines: Sequence[Mapping]) -> dict:
    """One itemising sponsor-year: identity terms of decompositions A and B, USD."""
    si_non = sum(r["amount"] for r in lines if not r["d2d"])
    si_d2d = sum(r["amount"] for r in lines if r["d2d"])
    ok = p9.get("status") == "ok"
    l1 = (p9.get("l1") or 0.0) if ok else (x.get("part_ix_line1_grants_domestic_orgs") or 0.0)
    l2, l3 = ((p9.get("l2") or 0.0), (p9.get("l3") or 0.0)) if ok else (0.0, 0.0)
    w2 = min(1.0, max(0.0, d_corr / (l1 + l3))) if l1 + l3 > 0 else 0.0
    nonitem = l1 - si_non - si_d2d
    return {"ein": k[0], "fiscal_year": k[1], "w": w, "w2": w2, "partial": l1 > 0 and si_non + si_d2d < PARTIAL * l1, "d_raw": d_raw, "d_corr": d_corr, "l1": l1, "l2": l2,
            "l3": l3, "si_non_d2d": si_non, "si_d2d": si_d2d, "p9_status": p9.get("status", ""),
            "sf_org_usd": p9.get("sf_org_usd", 0.0) if ok else 0.0,
            "si_lines_lt5k_non_d2d": sum(r["amount"] for r in lines if not r["d2d"] and 0 < r["amount"] < 5000),
            "A": {"corrections_r1_r4": d_corr - d_raw, "daf_weighting_haircut": d_raw - w * (l1 + l2 + l3),
                  "individual_grants_l2": w * l2, "foreign_grants_l3": w * l3,
                  "non_itemised_domestic_l1_minus_sched_i": w * nonitem, "d2d_lines": w * si_d2d, "covered": w * si_non},
            "B": {"weight_cap_residual": d_corr - w2 * (l1 + l3), "foreign_grants_l3": w2 * l3,
                  "non_itemised_domestic_l1_minus_sched_i": w2 * nonitem, "d2d_lines": w2 * si_d2d, "covered": w2 * si_non}}


def decompose(rows_item: Sequence[Mapping], non_item: Sequence[Mapping], netted: Mapping, netting: Mapping,
              fy: int, which: str) -> dict:
    full = tuple(r for r in rows_item if r["fiscal_year"] == fy)
    it = tuple(r[which] for r in full)
    names = COMP_A if which == "A" else COMP_B
    comp = {c: sum(t[c] for t in it) for c in names if c in it[0]}
    sub = "non_itemised_domestic_l1_minus_sched_i"
    comp["sub5k_full_itemisers"] = sum(r[which][sub] for r in full if not r["partial"])
    comp["sub5k_partial_itemisers"] = sum(r[which][sub] for r in full if r["partial"])
    comp["non_itemising_sponsors"] = sum(r["d_corr"] for r in non_item if r["fiscal_year"] == fy)
    comp["d2d_netting_residual"] = sum(t["d2d_lines"] for t in it) - netting[fy]
    covered = sum(t["covered"] for t in it)
    comp = {c: comp[c] for c in names}
    return {"fy": fy, "netted": netted[fy], "covered": covered, "gap": netted[fy] - covered, "components": comp,
            "unreconciled": netted[fy] - covered - sum(comp.values())}


def domestic_split(rows_item: Sequence[Mapping], non_item: Sequence[Mapping], fy: int) -> dict:
    """Shares used for non-itemising sponsors (decomposition B weights)."""
    it = tuple(r for r in rows_item if r["fiscal_year"] == fy and not r["partial"])
    wl1 = sum(r["w2"] * r["l1"] for r in it)
    wl13 = sum(r["w2"] * (r["l1"] + r["l3"]) for r in it)
    ni = tuple(r for r in non_item if r["fiscal_year"] == fy)
    tot = sum(r["d_corr"] for r in ni)
    dom = sum(r["d_corr"] * (r["dom_share"] if r["dom_share"] is not None else wl1 / wl13) for r in ni) / tot if tot else 0.0
    return {"non_itemisers_domestic_share": dom, "itemisers_domestic_share": wl1 / wl13,
            "itemised_like": sum(r["B"]["covered"] for r in it) / wl1,
            "sub5k_like": sum(r["B"]["non_itemised_domestic_l1_minus_sched_i"] for r in it) / wl1,
            "d2d_like": sum(r["B"]["d2d_lines"] for r in it) / wl1}


# ----------------------------------------------------------------------------- allocation keys and scenarios
def line_keys(ann: Mapping, weights: Mapping, tiers: Mapping) -> dict:
    """key -> {"by": {ein: {fy: dw}}, "total": {fy: dw incl. blank-EIN}}, positive non-d2d lines."""
    preds = {"all": lambda k, r: True, "top50": lambda k, r: tiers[k] == "top50",
             "small10": lambda k, r: r["amount"] < 10000, "small5": lambda k, r: r["amount"] < 5000}

    def build(pred):
        flat = tuple((r["ein"], k[1], r["amount"] * weights.get(k, 1.0))
                     for k, rs in ann.items() for r in rs if not r["d2d"] and r["amount"] > 0 and pred(k, r))
        return {"by": reduce(lambda acc, t: _add(acc, *t), (t for t in flat if t[0]), {}),
                "total": {fy: sum(t[2] for t in flat if t[1] == fy) for fy in FYS}}
    return {name: build(p) for name, p in preds.items()}


def _add(acc: dict, e: str, fy: int, v: float) -> dict:
    # accumulator-local mutation inside a reduce step; callers only see the finished mapping
    d = acc.setdefault(e, {})
    d[fy] = d.get(fy, 0.0) + v
    return acc


def grid() -> dict:
    """Plausible re-weighted allocations: cap residual x sub-$5,000 key x non-itemiser keys."""
    caps = {"cap0": None, "capall": "all"}
    subs = {"s10": ("small10", "all"), "sall": ("all", "all")}
    nis = {"ni50": ("top50", "small10"), "niall": ("all", "all")}
    return {f"rw_{c}_{s}_{n}": {"weights": "w2", "rule": {"weight_cap_residual": cv,
                                                         "sub5k_full_itemisers": sv[0], "sub5k_partial_itemisers": sv[1],
                                                         "non_itemising_sponsors": nv}}
            for (c, cv), (s, sv), (n, nv) in product(caps.items(), subs.items(), nis.items())}


CENTRAL = "rw_capall_s10_ni50"
SCENARIOS = {
    "measured_floor": {"weights": "w", "rule": {}},
    "residual_scaling_equivalent": {"weights": "w", "rule": {c: "all" for c in COMP_A}},
    "reweighted_only": {"weights": "w2", "rule": {}},
    **grid(),
    "only_sub5k_small10": {"weights": "w2", "rule": {"sub5k_full_itemisers": "small10", "sub5k_partial_itemisers": "all"}},
    "only_non_itemising_top50": {"weights": "w2", "rule": {"non_itemising_sponsors": ("top50", "small10")}},
    "sens_plus_d2d_residual_all": {"weights": "w2", "rule": {**grid()[CENTRAL]["rule"], "d2d_netting_residual": "all"}},
    "sens_small5_key": {"weights": "w2", "rule": {"weight_cap_residual": "all",
                                                  "sub5k_full_itemisers": "small5", "sub5k_partial_itemisers": "all",
                                                  "non_itemising_sponsors": ("top50", "small5")}},
}
BOOT_SCEN = frozenset({"measured_floor", "residual_scaling_equivalent", "reweighted_only", *grid()})


def allocations(dec: Mapping, split: Mapping, rule: Mapping) -> dict:
    """fy -> {key: USD to spread by that key}."""
    def parts(fy, c, r):
        x = dec[fy]["components"].get(c, 0.0)
        if r is None:
            return ()
        if isinstance(r, str):
            return ((r, x),)
        s = split[fy]
        dom = x * s["non_itemisers_domestic_share"]
        return ((r[0], dom * s["itemised_like"]), (r[1], dom * s["sub5k_like"]))

    def one(fy):
        flat = tuple(p for c, r in rule.items() for p in parts(fy, c, r))
        return {k: sum(v for kk, v in flat if kk == k) for k in sorted({kk for kk, _ in flat})}
    return {fy: one(fy) for fy in FYS}


def alloc_num(e: str, base_fy: Mapping, keys: Mapping, alloc: Mapping) -> dict:
    """Recipient numerator {fy: {si, dw}} = measured + allocated."""
    def add(fy):
        a = sum(usd * keys[k]["by"].get(e, {}).get(fy, 0.0) / keys[k]["total"][fy]
                for k, usd in alloc[fy].items() if keys[k]["total"][fy])
        b = base_fy.get(fy, {"si": 0.0, "dw": 0.0})
        return {"si": b["si"], "dw": b["dw"] + a}
    return {fy: add(fy) for fy in FYS}


# ----------------------------------------------------------------------------- recipient statistics
def scenario_rows(units: Sequence[Mapping], filings: Mapping, f990: Mapping, nums: Mapping) -> tuple[dict, ...]:
    return tuple({**rbe.recipient_a({**u, "num": nums[u["ein"]]}, filings[u["ein"]], f990), "sample_part": u["part"]}
                 for u in units)


def scen_summaries(name: str, rows: Sequence[Mapping], w: Mapping, reps: int, seed: int, floor: Mapping) -> list:
    frames = {"committed": lambda r: r["sample_part"] == "committed", "expanded": lambda r: True}
    scopes = ([("all", "all_ex_excluded", lambda r: True, reps)]
              + [("revenue_band", b, (lambda r, b=b: r["revenue_band"] == b), 0) for _, _, b in base.BANDS])

    def one(fr, st, sc, pred, n, i, j):
        s = rbe.summary_a(st, sc, BASES[j], [r for r in rows if frames[fr](r) and pred(r)], w, 1.0, n, seed + 31 * i + j)
        f = floor.get((fr, sc, BASES[j]))
        return {"row_type": "recipient_share", "scenario": name, "frame": fr, "basis": BASES[j], "scope_type": st,
                "scope": sc, **{x: s.get(x) for x in ("respondents", "weighted_recipients", "median_share",
                                                      "median_ci95_lo", "median_ci95_hi", "pooled_share",
                                                      "pooled_ci95_lo", "pooled_ci95_hi")},
                "implied_scaling_factor": (s["pooled_share"] / f) if f and s.get("pooled_share") is not None else None,
                "source": SOURCE}
    return [one(fr, *sc, i, j) for fr in frames for i, sc in enumerate(scopes) for j in range(len(BASES))]


def bounds(summ: Sequence[Mapping]) -> list:
    """Lower / upper of the re-weighted grid per frame x basis x scope (point estimates and interval ends)."""
    g = frozenset(grid())
    by = _group_by_fast((s for s in summ if s["scenario"] in g and s["pooled_share"] is not None),
                        lambda s: (s["frame"], s["basis"], s["scope_type"], s["scope"]))
    cen = {(s["frame"], s["basis"], s["scope_type"], s["scope"]): s for s in summ if s["scenario"] == CENTRAL}

    def one(k, v):
        lo, hi = min(v, key=lambda s: s["pooled_share"]), max(v, key=lambda s: s["pooled_share"])
        return {"row_type": "bound", "frame": k[0], "basis": k[1], "scope_type": k[2], "scope": k[3],
                "pooled_share": cen[k]["pooled_share"], "median_share": cen[k]["median_share"],
                "bound_lower_pooled": lo["pooled_share"], "bound_lower_scenario": lo["scenario"],
                "bound_upper_pooled": hi["pooled_share"], "bound_upper_scenario": hi["scenario"],
                "bound_lower_ci95": lo.get("pooled_ci95_lo"), "bound_upper_ci95": hi.get("pooled_ci95_hi"),
                "median_lower": min(s["median_share"] for s in v if s["median_share"] is not None),
                "median_upper": max(s["median_share"] for s in v if s["median_share"] is not None),
                "scenario": CENTRAL, "source": SOURCE}
    return [one(k, v) for k, v in sorted(by.items())]


# ----------------------------------------------------------------------------- main
FIELDS = ("row_type", "decomposition", "fiscal_year", "component", "usd", "share_of_netted", "share_of_gap",
          "scenario", "frame", "basis", "scope_type", "scope", "respondents", "weighted_recipients", "median_share",
          "median_ci95_lo", "median_ci95_hi", "pooled_share", "pooled_ci95_lo", "pooled_ci95_hi",
          "implied_scaling_factor", "bound_lower_pooled", "bound_lower_scenario", "bound_upper_pooled",
          "bound_upper_scenario", "bound_lower_ci95", "bound_upper_ci95", "median_lower", "median_upper",
          "key", "allocated_usd", "key_share_to_committed_frame",
          "ein", "sponsor_name", "tier", "status", "w", "w2", "d_raw", "d_corr", "l1", "l2", "l3",
          "si_non_d2d", "si_d2d", "sf_org_usd", "si_lines_lt5k_non_d2d",
          *(f"A_{c}" for c in ("corrections_r1_r4", "daf_weighting_haircut", "individual_grants_l2", "foreign_grants_l3",
                               "non_itemised_domestic_l1_minus_sched_i", "d2d_lines", "covered")),
          *(f"B_{c}" for c in ("weight_cap_residual", "foreign_grants_l3", "non_itemised_domestic_l1_minus_sched_i",
                               "d2d_lines", "covered")),
          "partial", "dom_share", "p9_status", "source")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; repo CLI convention)")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache-top50", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True)
    ap.add_argument("--p8-cache", required=True)
    ap.add_argument("--p8-cache-new", required=True)
    ap.add_argument("--p9-cache", required=True, help="new cache for Part IX / Schedule F extracts")
    ap.add_argument("--fetch", action="store_true", help="fetch missing Part IX extracts (sponsor returns only)")
    ap.add_argument("--fetch-only", action="store_true")
    ap.add_argument("--seed", type=int, default=20261119)
    ap.add_argument("--per-stratum", type=int, default=40)
    ap.add_argument("--certainty", type=int, default=400)
    ap.add_argument("--supp-per-stratum", type=int, default=30)
    ap.add_argument("--supp-certainty", type=int, default=100)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    sy = n50.sponsor_years(pick_returns(load_np(a.np_cache)), panel, rank)
    robots = robots_check(a.p9_cache) if a.fetch else "not_checked_cache_only"
    if robots == "blocked":
        raise SystemExit("robots.txt disallows the mirror")
    sy_keys = sorted(sy)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        p9 = dict(zip(sy_keys, ex.map(lambda k: fetch_p9(sy[k]["x"]["oid"], a.p9_cache, a.fetch), sy_keys)))
    p9_status = {s: len(v) for s, v in _group_by_fast(p9.values(), lambda x: x.get("status")).items()}
    if a.fetch_only:
        print(json.dumps({"robots": robots, "p9_status": p9_status}))
        return 0

    # ---- numerator side, exactly as b40n1202-01 (caches only)
    item = {k: v for k, v in sy.items() if v["pre"] == "itemised"}

    def lines(k):
        v = item[k]
        return load_lines(v["x"]["oid"], v["x"]["sched_i_lines"],
                          a.lines_cache_top50 if v["tier"] == "top50" else a.lines_cache, [], False)
    keys = sorted(item)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        loaded = dict(zip(keys, ex.map(lines, keys)))
    good = {k: drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    tiers = {k: item[k]["tier"] for k in good}
    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    groups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in groups.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    cost = read_csv(COST)
    weights, wsrc = n50.weight_fallback(base.sponsor_weights(cost, good), {k: item[k] for k in good}, 1.0)

    # ---- sponsor-side decomposition
    net_rows = [r for r in read_csv(base.NETTED_CSV) if r["metric"] == "daf_grants" and r["tier"] == "central"]
    netted = {int(r["fiscal_year"]): num(r["netted_value"]) for r in net_rows}
    netting = {int(r["fiscal_year"]): num(r["r5_netting_amount"]) for r in net_rows}
    corr_tot = {int(r["fiscal_year"]): num(r["corrected_value"]) for r in net_rows}
    deltas = corrected_deltas(read_csv(CORR_CSV))
    d_raw = {(ein9(r["ein"]), int(r["fiscal_year_end"])): num(r.get("total_daf_grants")) or 0.0
             for r in dafrc if r["fiscal_year_end"] in tuple(map(str, FYS))}
    rows_item = tuple(sponsor_row(k, p9.get(k, {}), item[k]["x"], weights[k], d_raw.get(k, 0.0),
                                  d_raw.get(k, 0.0) + deltas.get(k, 0.0), ann[k]) for k in sorted(good))
    w2 = {(r["ein"], r["fiscal_year"]): r["w2"] for r in rows_item}
    w_all = base.sponsor_weights(cost, sy)

    def non_item_row(k):
        x = sy.get(k)
        q = p9.get(k, {}) if x else {}
        ok = q.get("status") == "ok"
        l13 = ((q.get("l1") or 0.0) + (q.get("l3") or 0.0)) if ok else 0.0
        return {"ein": k[0], "fiscal_year": k[1], "tier": "top50" if k[0] in rank else "other",
                "status": "not_in_cache" if x is None else ("lines_" + loaded[k]["status"]) if k in loaded else x["pre"],
                "d_raw": d_raw.get(k, 0.0), "d_corr": d_raw.get(k, 0.0) + deltas.get(k, 0.0), "w": w_all.get(k),
                "l1": q.get("l1") if ok else None, "l2": q.get("l2") if ok else None, "l3": q.get("l3") if ok else None,
                "sf_org_usd": q.get("sf_org_usd") if ok else None, "p9_status": q.get("status", ""),
                "dom_share": ((q.get("l1") or 0.0) / l13) if l13 > 0 else None}
    ni_keys = sorted(k for k in set(d_raw) | {k for k in deltas if k[1] in FYS} if k not in good and k[0] in panel)
    non_item = tuple(r for r in map(non_item_row, ni_keys) if r["d_corr"])
    dec = {w_: {fy: decompose(rows_item, non_item, netted, netting, fy, w_) for fy in FYS} for w_ in ("A", "B")}
    split = {fy: domestic_split(rows_item, non_item, fy) for fy in FYS}

    # ---- recipient side, frames and samples exactly as b40n1202-01
    def numer(wts):
        a50 = {k: v for k, v in ann.items() if tiers[k] == "top50"}
        aot = {k: v for k, v in ann.items() if tiers[k] == "other"}
        return n50.combine(base.numerators(a50, wts), base.numerators(aot, wts))
    comb = {"w": numer(weights), "w2": numer(w2)}
    keysets = {"w": line_keys(ann, weights, tiers), "w2": line_keys(ann, w2, tiers)}
    panel_eins = frozenset(panel)
    bmf = base.load_bmf(a.bmf_dir, frozenset(comb["w"]))
    cw = comb["w"]

    def unit(e, c):
        b = bmf[e]
        return {**b, "group": base.group_of(b["ntee"]), "band": base.band_of(b["revenue"]), "num": c["top50"],
                "num_si_total": n50.tot(c["top50"], "si"), "num_oth_si": n50.tot(c["other"], "si"),
                "excl": base.exclusion(b, panel_eins)}
    universe = tuple(unit(e, c) for e, c in cw.items() if e in bmf)
    frame = tuple(u for u in universe if not u["excl"] and u["num_si_total"] > 0)
    new_only = tuple({**u, "num_si_total": u["num_oth_si"]} for u in universe if not u["excl"] and u["num_si_total"] <= 0
                     and u["num_oth_si"] > 0)
    sample = base.draw_sample(frame, a.certainty, a.per_stratum, a.seed)
    supp = tuple({**s, "stratum": "new|" + s["stratum"]}
                 for s in base.draw_sample(new_only, a.supp_certainty, a.supp_per_stratum, a.seed + 1))
    units = tuple({**s, "part": "committed"} for s in sample) + tuple({**s, "part": "new_only"} for s in supp)
    idx = base.load_index(a.index_dir, frozenset(s["ein"] for s in units))
    filings = {s["ein"]: base.choose_filings(idx.get(s["ein"], ())) for s in units}
    oids = sorted({f["oid"] for fs in filings.values() for f in fs.values()})
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        f990 = dict(zip(oids, ex.map(lambda o: n50.p8_lookup(o, a.p8_cache, a.p8_cache_new, False), oids)))

    frame_eins = frozenset(u["ein"] for u in frame)
    kshare = {(wn, k, fy): sum(v.get(fy, 0.0) for e, v in ks[k]["by"].items() if e in frame_eins) / ks[k]["total"][fy]
              for wn, ks in keysets.items() for k in ks for fy in FYS}

    floor_rows = scenario_rows(units, filings, f990, {u["ein"]: cw[u["ein"]]["all"] for u in units})
    wts = rbe.weights_a(floor_rows)

    def run(i, name, spec):
        d = dec["A" if spec["weights"] == "w" else "B"]
        al = allocations(d, split, spec["rule"])
        c = comb[spec["weights"]]
        nums = {u["ein"]: alloc_num(u["ein"], c[u["ein"]]["all"], keysets[spec["weights"]], al) for u in units}
        rows = floor_rows if name == "measured_floor" else scenario_rows(units, filings, f990, nums)
        return name, rows, al
    runs = [run(i, n, s) for i, (n, s) in enumerate(SCENARIOS.items())]
    floor0 = scen_summaries("measured_floor", runs[0][1], wts, 0, a.seed, {})
    floor = {(s["frame"], s["scope"], s["basis"]): s["pooled_share"] for s in floor0}
    with ThreadPoolExecutor(max_workers=4) as ex:
        summ = [s for part in ex.map(lambda t: scen_summaries(t[1][0], t[1][1], wts, a.boot if t[1][0] in BOOT_SCEN else 0,
                                                              a.seed + 1000 * t[0], floor), enumerate(runs)) for s in part]
    bnd = bounds(summ)
    alloc_rows = [{"row_type": "allocation", "scenario": n, "decomposition": "A" if SCENARIOS[n]["weights"] == "w" else "B",
                   "fiscal_year": fy, "key": k, "allocated_usd": round(v), "share_of_netted": v / netted[fy],
                   "key_share_to_committed_frame": kshare[(SCENARIOS[n]["weights"], k, fy)], "source": SOURCE}
                  for n, _, al in runs for fy in FYS for k, v in al[fy].items()]
    comp_rows = ([{"row_type": "component", "decomposition": w_, "fiscal_year": fy, "component": c, "usd": round(v),
                   "share_of_netted": v / dec[w_][fy]["netted"], "share_of_gap": v / dec[w_][fy]["gap"], "source": SOURCE}
                  for w_ in ("A", "B") for fy in FYS for c, v in dec[w_][fy]["components"].items()]
                 + [{"row_type": "component", "decomposition": w_, "fiscal_year": fy, "component": c, "usd": round(v),
                     "share_of_netted": v / dec[w_][fy]["netted"], "source": SOURCE}
                    for w_ in ("A", "B") for fy in FYS
                    for c, v in (("netted_daf_grants_central", dec[w_][fy]["netted"]),
                                 ("covered_itemised_daf_weighted", dec[w_][fy]["covered"]), ("gap", dec[w_][fy]["gap"]),
                                 ("unreconciled", dec[w_][fy]["unreconciled"]))]
                 + [{"row_type": "component", "decomposition": "split", "fiscal_year": fy, "component": k, "share_of_netted": v,
                     "source": SOURCE} for fy in FYS for k, v in split[fy].items()])
    names = {e: p["name"] for e, p in panel.items()}
    flat = lambda r: {**{k: v for k, v in r.items() if k not in ("A", "B")},  # noqa: E731
                      **{f"A_{k}": v for k, v in r.get("A", {}).items()}, **{f"B_{k}": v for k, v in r.get("B", {}).items()}}
    rnd0 = lambda d: {k: (round(v) if isinstance(v, float) and k not in ("w", "w2", "dom_share") else v) for k, v in d.items()}  # noqa: E731
    sp_rows = ([{"row_type": "sponsor_itemised", **rnd0(flat(r)), "sponsor_name": names.get(r["ein"], ""),
                 "tier": tiers[(r["ein"], r["fiscal_year"])], "status": "itemised", "source": SOURCE} for r in rows_item]
               + [{"row_type": "sponsor_non_itemising", **rnd0(r), "sponsor_name": names.get(r["ein"], ""), "source": SOURCE}
                  for r in non_item])
    write_csv(a.out, comp_rows + bnd + summ + alloc_rows + sp_rows, FIELDS)

    # ---- diagnostics
    pick = lambda sc, fr, b, scope="all_ex_excluded": next(s for s in summ if s["scenario"] == sc and s["frame"] == fr and s["basis"] == b and s["scope"] == scope)  # noqa: E731
    r4 = lambda v: round(v, 4) if isinstance(v, float) else v  # noqa: E731
    it24 = tuple(r for r in rows_item if r["fiscal_year"] == 2024)
    ni24 = tuple(r for r in non_item if r["fiscal_year"] == 2024)
    seg = lambda pred: {"n": sum(1 for r in it24 if pred(r)), **{c: round(sum(r["A"][c] for r in it24 if pred(r)))  # noqa: E731
                        for c in ("foreign_grants_l3", "non_itemised_domestic_l1_minus_sched_i", "covered")}}
    out = {
        "robots": robots, "p9_status": p9_status, "corrected_total_check": {fy: round(corr_tot[fy] - sum(
            r["d_corr"] for r in rows_item if r["fiscal_year"] == fy) - sum(r["d_corr"] for r in non_item if r["fiscal_year"] == fy)) for fy in FYS},
        "decomposition": {f"{w_}|{fy}": {**{k: round(v) for k, v in dec[w_][fy]["components"].items()},
                                         "gap": round(dec[w_][fy]["gap"]), "covered": round(dec[w_][fy]["covered"]),
                                         "unreconciled": round(dec[w_][fy]["unreconciled"])} for w_ in ("A", "B") for fy in FYS},
        "points": {f"{w_}|{fy}": {k: round(100 * v / netted[fy], 2) for k, v in dec[w_][fy]["components"].items()}
                   for w_ in ("A", "B") for fy in FYS},
        "coverage_B": {fy: r4(dec["B"][fy]["covered"] / netted[fy]) for fy in FYS},
        "split": {fy: {k: r4(v) for k, v in s.items()} for fy, s in split.items()},
        "key_share_to_committed_frame": {f"{wn}|{k}|{fy}": r4(v) for (wn, k, fy), v in kshare.items()},
        "key_totals_w2": {f"{k}|{fy}": round(keysets["w2"][k]["total"][fy]) for k in keysets["w2"] for fy in FYS},
        "itemisers_2024": {"sponsor_years": len(it24), "w_source": {s: sum(1 for k, v in wsrc.items() if k[1] == 2024 and v == s)
                                                                     for s in set(wsrc.values())},
                           "w2_capped": sum(1 for r in it24 if r["d_corr"] > r["l1"] + r["l3"] > 0),
                           "l1_l2_l3_raw": [round(sum(r[c] for r in it24)) for c in ("l1", "l2", "l3")],
                           "sched_f_part2_raw": round(sum(r["sf_org_usd"] for r in it24)),
                           "si_raw": round(sum(r["si_non_d2d"] + r["si_d2d"] for r in it24)),
                           "lines_lt5k_raw": round(sum(r["si_lines_lt5k_non_d2d"] for r in it24)),
                           "sub5k_neg_sponsor_years": sum(1 for r in it24 if r["A"]["non_itemised_domestic_l1_minus_sched_i"] < 0),
                           "sub5k_neg_usd": round(sum(r["A"]["non_itemised_domestic_l1_minus_sched_i"] for r in it24
                                                      if r["A"]["non_itemised_domestic_l1_minus_sched_i"] < 0)),
                           "partial_itemisation_si_lt_half_l1": seg(lambda r: r["l1"] > 0 and r["si_non_d2d"] + r["si_d2d"] < 0.5 * r["l1"]),
                           "top50": seg(lambda r: tiers[(r["ein"], 2024)] == "top50"),
                           "other": seg(lambda r: tiers[(r["ein"], 2024)] == "other")},
        "largest_foreign_2024": sorted(({"name": names.get(r["ein"], "")[:40], "w": r4(r["w"]), "l3": round(r["l3"]),
                                         "w_l3": round(r["A"]["foreign_grants_l3"])} for r in it24), key=lambda d: -d["w_l3"])[:10],
        "largest_sub5k_2024": sorted(({"name": names.get(r["ein"], "")[:40], "w": r4(r["w"]), "l1": round(r["l1"]),
                                       "si": round(r["si_non_d2d"] + r["si_d2d"]),
                                       "w_sub5k": round(r["A"]["non_itemised_domestic_l1_minus_sched_i"])} for r in it24),
                                     key=lambda d: -d["w_sub5k"])[:10],
        "largest_haircut_2024": sorted(({"name": names.get(r["ein"], "")[:40], "w": r4(r["w"]), "w2": r4(r["w2"]),
                                         "d_corr": round(r["d_corr"]), "net": round(r["d_corr"] - r["w"] * (r["l1"] + r["l3"]))}
                                        for r in it24), key=lambda d: -abs(d["net"]))[:10],
        "non_itemising_2024_by_status": {s: {"n": len(v), "d_corr": round(sum(r["d_corr"] for r in v)),
                                             "d_raw": round(sum(r["d_raw"] for r in v))}
                                         for s, v in _group_by_fast(ni24, lambda r: r["status"]).items()},
        "non_itemising_2024_largest": sorted(({"name": names.get(r["ein"], "")[:40], "status": r["status"], "d_raw": round(r["d_raw"]),
                                               "d_corr": round(r["d_corr"]), "l1": r["l1"], "l3": r["l3"]} for r in ni24),
                                             key=lambda d: -d["d_corr"])[:8],
        "headline": {f"{sc}|{fr}|{b}": {x: r4(pick(sc, fr, b)[x]) for x in ("pooled_share", "pooled_ci95_lo", "pooled_ci95_hi",
                                                                             "median_share", "median_ci95_lo", "median_ci95_hi",
                                                                             "implied_scaling_factor")}
                     for sc in SCENARIOS for fr in ("committed", "expanded") for b in BASES},
        "bounds": [{k: r4(v) for k, v in b_.items() if k not in ("source", "row_type")} for b_ in bnd],
    }
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
