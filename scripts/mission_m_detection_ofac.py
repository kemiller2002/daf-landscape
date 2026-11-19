#!/usr/bin/env python3
"""Detection probability and OFAC analogue for the escaped-error cost m. Queue items P-G0403-04-01 and -04-04.

Task g0403-0104. Builds on research/mission-2026-11-14/g0403-04-escaped-error-cost.md (wave-38B corrected: central
composite m about 2.20 with P08 at its correction unit only, because IRC 4967 puts no tax on the sponsor).

(A) P-G0403-04-01: P(escaped DAF compliance error is detected and taxed).
    1. IRS Data Book FY2021-FY2025 (Table 3-5 / former Table 21): returns examined by type, incl. Form 990 series and
       Form 4720; Table 1-2 (returns filed); Table 2-6 (501(c)(3) organizations) [F].
    2. TE/GE Accomplishments Letters FY2021-FY2024 (EO filings examined, incl. related returns) and TIGTA 2026-1S0-042
       (FY2025 EO examinations 15% below FY2021) [F].
    3. IRS e-file index counts of Forms 990 / 990-EZ / 990-PF by processing year (denominator) [C from IRS files].
    4. SOI Form 4720 study, CY2021-CY2025: returns and amount of the IRC 4966 tax on taxable distributions of
       sponsoring organizations [F]; DAF sponsor count 1,512 (DAFRC FY2024, via repo) [F].
    -> exam-coverage and incidence bounds on P [C], used in place of the unsourced 0.01 / 0.1 / 1 sweep.
(B) P-G0403-04-04: OFAC enforcement releases 2021-2026 against payment processors, money transmitters, prepaid /
    rewards platforms and (separately) virtual-currency exchanges and wallets. No release in the period names a charity
    or donor platform. Penalty per apparent violation [C], in P14 handling units [C]; regime analogue for sanctions
    screening at a DAF sponsor (P01/P14) [I].
(C) Recomputed m: imports scripts/mission_escaped_error_cost.py (unchanged) and re-uses its pure functions
    (m_daf, handling_cost, weights, range_rows, row, write_csv, eval_draw_pm) and, with --route, the routing variant
    it imports (seed 42; routing stream 42+104729) for the large-national CAL_CENTRAL pool.

Output (new file): data/mission-2026-11-14/m-detection-ofac-2026-11-19.csv
Usage: python3 scripts/mission_m_detection_ofac.py . [--route] [--draws 10000] [--efile-dir DIR] [--out PATH]
Stdlib only; functional style (constants are immutable tuples / mappings; I/O only in main).
"""
from __future__ import annotations

import argparse
import collections
import csv
import os
import sys
from types import MappingProxyType as Frozen
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_escaped_error_cost as ee  # noqa: E402  (imported, not modified)

rv, cal, v2 = ee.rv, ee.cal, ee.v2
OUT_CSV = os.path.join(v2.DATA, "m-detection-ofac-2026-11-19.csv")

IRS_SOI = "https://www.irs.gov/pub/irs-soi/"
# ------------------------------------------------------------------------------------------- (A) IRS [F]
# Data Book Table 3-5 (FY2025; "Table 21" in FY2021-2024): number of returns examined, by type of return.
# Table 1-2 ("Table 2" before FY2025): tax-exempt organization returns filed (Form 990 series incl. 990-N, 990-PF, 990-T,
# 4720, 5227, 8871/8872 and, FY2025, the 8038 series). Table 2-6 ("Table 14"): recognized 501(c)(3) organizations.
DATA_BOOK = (
    Frozen({"fy": 2021, "ex_990": 1383, "ex_990pf": 203, "ex_4720": 301, "ex_total": 9067, "eo_filed": 1722803,
            "c3_orgs": 1431266, "t35": "21dbs03t21eo.xlsx", "t12": "21dbs01t02nr.xlsx", "t26": "21dbs02t14eo.xlsx"}),
    Frozen({"fy": 2022, "ex_990": 1343, "ex_990pf": 170, "ex_4720": 292, "ex_total": 9185, "eo_filed": 1751682,
            "c3_orgs": 1480565, "t35": "22dbs03t21eo.xlsx", "t12": "22dbs01t02nr.xlsx", "t26": "22dbs02t14eo.xlsx"}),
    Frozen({"fy": 2023, "ex_990": 1029, "ex_990pf": 81, "ex_4720": 231, "ex_total": 7666, "eo_filed": 1789884,
            "c3_orgs": 1514558, "t35": "23dbs03t21eo.xlsx", "t12": "23dbs01t02nr.xlsx", "t26": "23dbs02t14eo.xlsx"}),
    Frozen({"fy": 2024, "ex_990": 666, "ex_990pf": 72, "ex_4720": 210, "ex_total": 7013, "eo_filed": 1805833,
            "c3_orgs": 1548798, "t35": "24dbs03t21eo.xlsx", "t12": "24dbs01t02nr.xlsx", "t26": "24dbs02t14eo.xlsx"}),
    Frozen({"fy": 2025, "ex_990": 889, "ex_990pf": 77, "ex_4720": 188, "ex_total": 7914, "eo_filed": 1798413,
            "c3_orgs": 1596231, "t35": "25db-3-05-eo.xlsx", "t12": "25db-1-02-nr.xlsx", "t26": "25db-2-06-eo.xlsx"}),
)
# TE/GE Accomplishments Letters (Pub 5329): "EO completed examinations of N filings in fiscal year Y, including the
# Form 990 series (990, 990-EZ, 990-PF, 990-N, 990-T) and their associated employment and excise tax returns".
TEGE_EO_EXAMS = (
    Frozen({"fy": 2021, "closed": 3249, "change_pct": 82.3, "url": "https://www.irs.gov/pub/irs-prior/p5329--2021.pdf"}),
    Frozen({"fy": 2022, "closed": 3425, "change_pct": 77.5, "url": "https://www.irs.gov/pub/irs-prior/p5329--2022.pdf"}),
    Frozen({"fy": 2023, "closed": 2464, "change_pct": 75.7, "url": "https://www.irs.gov/pub/irs-prior/p5329--2023.pdf"}),
    Frozen({"fy": 2024, "closed": 1955, "change_pct": 74.5, "url": "https://www.irs.gov/pub/irs-access/p5329_accessible.pdf"}),
)
TIGTA_FY25 = Frozen({"pct_fewer_vs_fy2021": 15.0, "report": "TIGTA 2026-1S0-042 (19 Aug 2026)",
                     "url": "https://www.tigta.gov/sites/default/files/reports/2026-08/20261S0042fr.pdf",
                     "quote": "the Exempt Organizations and Employee Plans functions completed fewer examinations in "
                              "FY 2025 compared to FY 2021, by 15 and 16 percent, respectively"})
# IRS e-file index (apps.irs.gov/pub/epostcard/990/xml/<yr>/index_<yr>.csv), rows by RETURN_TYPE and processing year.
# Counted with collections.Counter over the full files (re-count with --efile-dir). Processing year ~ fiscal year.
EFILE = (
    Frozen({"yr": 2021, "990": 305173, "990EZ": 164035, "990PF": 108644}),
    Frozen({"yr": 2022, "990": 325555, "990EZ": 189690, "990PF": 117073}),
    Frozen({"yr": 2023, "990": 347337, "990EZ": 209957, "990PF": 124666}),
    Frozen({"yr": 2024, "990": 363100, "990EZ": 215355, "990PF": 126982}),
    Frozen({"yr": 2025, "990": 376920, "990EZ": 217102, "990PF": 130347}),
)
EFILE_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
# SOI Exempt Organizations Excise Tax study (Form 4720), Table 1: "Tax on taxable distributions of sponsoring
# organizations" (the IRC 4966(a)(1) tax on the sponsor). CY2025 cell deleted for disclosure ('d'); its amount is in
# the column total, so total minus the disclosed rows bounds it (with three other 'd' rows).
SOI_4720 = (
    Frozen({"cy": 2021, "n": 7, "usd": 112913, "total_n": 1547, "total_usd": 291129057, "file": "21pf00et.xlsx"}),
    Frozen({"cy": 2022, "n": 15, "usd": 179819, "total_n": 4524, "total_usd": 956547432, "file": "22pf00et.xlsx"}),
    Frozen({"cy": 2023, "n": 10, "usd": 1150071, "total_n": 3708, "total_usd": 994744987, "file": "23pf00et.xlsx"}),
    Frozen({"cy": 2024, "n": 6, "usd": 101894, "total_n": 3099, "total_usd": 733556694, "file": "24pf00et.xlsx"}),
    Frozen({"cy": 2025, "n": None, "usd": None, "total_n": 3027, "total_usd": 844996874, "file": "25pf00et.xlsx",
            "disclosed_usd": (18515547, 611877108, 1791059, 6441778, 204519267, 508305, 2702, 500000, 576349, 0)}),
)
DAF_SPONSORS = Frozen({"n": 1512, "label": "DAFRC FY2024 sponsors (repo: full-universe-990-harvest-and-corrected-totals.md)",
                       "url": "https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx"})
FIDELITY_GRANTS_2024 = Frozen({"n": 2_700_000, "qual": "nearly",
                               "src": "data/mission-2026-11-14/grant-rail-shares-panel-2026.csv (Fidelity Charitable 2024)"})

# ------------------------------------------------------------------------------------------- (B) OFAC [F]
OFAC = "https://ofac.treasury.gov/media/{}/download?inline"
# group: processor = payment processor / money transmitter / prepaid-rewards / payments subsidiary / card issuer;
#        crypto = virtual-currency exchange or wallet. count_basis: stated (the release's own total) or
#        sum (sum of counts the release states by programme or kind; the release gives no single total).
OFAC_RELEASES = (
    Frozen({"id": "BITPAY_2021", "entity": "BitPay, Inc.", "date": "2021-02-18", "group": "processor",
            "kind": "crypto payment processor for merchants", "penalty": 507375.0, "count": 2102, "count_basis": "stated",
            "value": 129000.0, "value_q": "approximately", "vsd": "no", "egregious": "no", "stat_max": 619689816.0,
            "base": 2255000.0, "media": 54341}),
    Frozen({"id": "MONEYGRAM_2021", "entity": "MoneyGram Payment Systems, Inc.", "date": "2021-04-29",
            "group": "processor", "kind": "money transmitter", "penalty": 34328.78, "count": 359,
            "count_basis": "stated", "value": None, "value_q": "", "vsd": "yes", "egregious": "no",
            "stat_max": 302938437.0, "base": 52813.50, "media": 97356}),
    Frozen({"id": "PAYONEER_2021", "entity": "Payoneer Inc.", "date": "2021-07-23", "group": "processor",
            "kind": "online money transmitter and prepaid access", "penalty": 1385901.40, "count": 2220,
            "count_basis": "stated", "value": 793950.70, "value_q": "", "vsd": "partly (19 of 2,220)", "egregious": "no",
            "stat_max": 654357316.0, "base": 3849726.0, "media": 911571}),
    Frozen({"id": "AIRBNB_2022", "entity": "Airbnb Payments, Inc.", "date": "2022-01-03", "group": "processor",
            "kind": "payments subsidiary (registered MSB)", "penalty": 91172.29, "count": 3464 + 3076 + 44,
            "count_basis": "sum (3,464 + 3,076 extrapolated, 44 confirmed; 3,076 are record-keeping)",
            "value": None, "value_q": "", "vsd": "yes", "egregious": "no", "stat_max": 600601408.0,
            "base": 364689.0, "media": 917236}),
    Frozen({"id": "AMEX_2022", "entity": "American Express National Bank", "date": "2022-07-15", "group": "processor",
            "kind": "card issuer; one high-confidence screening alert closed in error", "penalty": 430500.0,
            "count": 214, "count_basis": "stated", "value": 155189.42, "value_q": "", "vsd": "no", "egregious": "no",
            "stat_max": 331288050.0, "base": 574000.0, "media": 924406, "missed_alerts": 1}),
    Frozen({"id": "TANGO_2022", "entity": "Tango Card, Inc.", "date": "2022-09-30", "group": "processor",
            "kind": "electronic rewards / stored value", "penalty": 116048.60, "count": 27720,
            "count_basis": "stated ('at least 27,720 stored value products')", "value": 386828.65, "value_q": "",
            "vsd": "yes", "egregious": "no", "stat_max": 9168949062.0, "base": 193414.33, "media": 928326}),
    Frozen({"id": "DAVINCI_2023", "entity": "Swift Prepaid Solutions, Inc. d/b/a daVinci Payments",
            "date": "2023-11-06", "group": "processor",
            "kind": "prepaid reward card programmes (corporate, non-profit, government clients)", "penalty": 206213.0,
            "count": 12391, "count_basis": "stated", "value": 549134.89, "value_q": "", "vsd": "yes",
            "egregious": "no", "stat_max": 4399759685.0, "base": 274950.0, "media": 932276}),
    Frozen({"id": "UPHOLD_2023", "entity": "Uphold HQ Inc.", "date": "2023-03-31", "group": "processor",
            "kind": "money services business; cross-border remittance and multi-asset platform", "penalty": 72230.32,
            "count": 152, "count_basis": "stated (152 transactions)", "value": 180575.80, "value_q": "", "vsd": "yes",
            "egregious": "no", "stat_max": 44468494.0, "base": 90288.90, "media": 931556}),
    Frozen({"id": "KRAKEN_2022", "entity": "Payward, Inc. d/b/a Kraken", "date": "2022-11-28", "group": "crypto",
            "kind": "virtual currency exchange", "penalty": 362158.70, "count": 826, "count_basis": "stated",
            "value": 1680577.10, "value_q": "approximately", "vsd": "yes", "egregious": "no",
            "stat_max": 272228964.0, "base": 840288.55, "media": 929541}),
    Frozen({"id": "BITTREX_2022", "entity": "Bittrex, Inc.", "date": "2022-10-11", "group": "crypto",
            "kind": "virtual currency exchange and hosted wallet", "penalty": 24280829.20, "count": 116421,
            "count_basis": "stated", "value": 263451600.13, "value_q": "approximately", "vsd": "no",
            "egregious": "no", "stat_max": 35773364108.57, "base": 485616584.0, "media": 928746}),
    Frozen({"id": "POLONIEX_2023", "entity": "Poloniex, LLC", "date": "2023-05-01", "group": "crypto",
            "kind": "digital asset trading platform", "penalty": 7591630.0, "count": 65942, "count_basis": "stated",
            "value": 15335349.0, "value_q": "", "vsd": "no", "egregious": "no", "stat_max": 19692872800.0,
            "base": 99237000.0, "media": 931701}),
    Frozen({"id": "COINLIST_2023", "entity": "CoinList Markets LLC", "date": "2023-12-13", "group": "crypto",
            "kind": "virtual currency exchange", "penalty": 1207830.0, "count": 989, "count_basis": "stated",
            "value": 1252280.0, "value_q": "", "vsd": "no", "egregious": "no", "stat_max": 327306583.0,
            "base": 3097000.0, "media": 932406}),
    Frozen({"id": "BINANCE_2023", "entity": "Binance Holdings, Ltd.", "date": "2023-11-21", "group": "crypto",
            "kind": "virtual currency exchange", "penalty": 968618825.0, "count": 1667153, "count_basis": "stated",
            "value": 706068127.0, "value_q": "approximately", "vsd": "no", "egregious": "yes",
            "stat_max": 592133829398.0, "base": None, "media": 932351}),
    Frozen({"id": "SHAPESHIFT_2025", "entity": "ShapeShift AG", "date": "2025-09-22", "group": "crypto",
            "kind": "digital asset exchange (defunct; ability to pay considered)", "penalty": 750000.0,
            "count": 39 + 16839 + 33 + 272, "count_basis": "sum (39 CACR + 16,839 ITSR + 33 SSR + 272 SySR = '17,183 instances')",
            "value": 12570956.0, "value_q": "", "vsd": "no", "egregious": "no", "stat_max": None,
            "base": 39515000.0, "media": 934641}),
    Frozen({"id": "EXODUS_2025", "entity": "Exodus Movement, Inc.", "date": "2025-12-16", "group": "crypto",
            "kind": "self-custody wallet software; staff advised Iran users on VPNs", "penalty": 3103360.0,
            "count": 254, "count_basis": "stated", "value": None, "value_q": "", "vsd": "no",
            "egregious": "12 of 254", "stat_max": None, "base": 4774400.0, "media": 934831}),
)
# Release rows on the OFAC 2021-2026 enforcement pages (index + five year pages), read 2026-11-19; no row names a
# charity, foundation, DAF sponsor or donor platform.
OFAC_PAGES = (("2021", 19), ("2022", 16), ("2023", 16), ("2024", 12), ("2025", 14), ("2026 YTD", 10))
OFAC_INDEX = "https://ofac.treasury.gov/civil-penalties-and-enforcement-information"

# ------------------------------------------------------------------------------------------- (C) settings [I]
# P07 detection: exam coverage of Form 990/990-EZ filers is the main channel by which an escaped taxable distribution
# reaches a 4966 assessment; q (P(exam finds and taxes it | exam)) <= 1 is set to 1, so the bounds are upper bounds.
P_OFAC = Frozen({"low": 0.01, "central": 0.1, "high": 1.0})  # P(OFAC enforcement | sanctions miss): no source [I]


# ------------------------------------------------------------------------------------------- pure helpers
def coverage_rows_data() -> tuple[dict, ...]:
    """Per FY exam-coverage ratios [C]."""
    ef = {e["yr"]: e for e in EFILE}
    tg = {t["fy"]: t["closed"] for t in TEGE_EO_EXAMS}
    tg25 = round(tg[2021] * (1 - TIGTA_FY25["pct_fewer_vs_fy2021"] / 100))
    tg = {**tg, 2025: tg25}
    return tuple({"fy": d["fy"],
                  "narrow": d["ex_990"] / (ef[d["fy"]]["990"] + ef[d["fy"]]["990EZ"]),
                  "narrow_c3": d["ex_990"] / d["c3_orgs"],
                  "broad": tg[d["fy"]] / (ef[d["fy"]]["990"] + ef[d["fy"]]["990EZ"] + ef[d["fy"]]["990PF"]),
                  "tege_closed": tg[d["fy"]], "tege_basis": "F" if d["fy"] in {t["fy"] for t in TEGE_EO_EXAMS} else "C (TIGTA %)",
                  "ex_4720_per_eo_filed": d["ex_4720"] / d["eo_filed"]} for d in DATA_BOOK)


def soi_4966() -> tuple[dict, ...]:
    """Sponsor 4966 tax by CY; CY2025 bounded by the residual of suppressed rows [C]."""
    def one(s):
        if s["n"] is not None:
            return {**s, "usd_hi": float(s["usd"]), "per_return": s["usd"] / s["n"],
                    "implied_distribution": s["usd"] / s["n"] / ee.IRC_4966["sponsor_rate"],
                    "share_sponsors": s["n"] / DAF_SPONSORS["n"]}
        resid = s["total_usd"] - sum(s["disclosed_usd"])
        return {**s, "usd_hi": float(resid), "per_return": None, "implied_distribution": None, "share_sponsors": None}
    return tuple(map(one, SOI_4720))


def p_bounds(cov: Sequence[Mapping], soi: Sequence[Mapping]) -> dict:
    """P(detected and taxed) settings for P07 [C on F, with q = 1]."""
    narrow = sorted(c["narrow"] for c in cov)
    max_n = max(s["n"] for s in soi if s["n"] is not None)
    return {"low": min(narrow), "central": ee.median(narrow),
            "high": max(max(c["broad"] for c in cov), max_n / DAF_SPONSORS["n"]),
            "sponsor_incidence_max": max_n / DAF_SPONSORS["n"]}


def ofac_unit(o: Mapping, hc: float) -> dict:
    per = o["penalty"] / o["count"]
    return {"per_violation": per, "units": per / hc,
            "per_value": (o["penalty"] / o["value"]) if o["value"] else None,
            "share_base": (o["penalty"] / o["base"]) if o["base"] else None,
            "per_missed_alert": (o["penalty"] / o["missed_alerts"]) if o.get("missed_alerts") else None}


def ofac_stats(hc: float) -> dict:
    def grp(g):
        xs = sorted(o["penalty"] / o["count"] for o in OFAC_RELEASES if g in ("all", o["group"]))
        return {"min": xs[0], "median": ee.median(xs), "max": xs[-1], "n": len(xs)}
    return {g: grp(g) for g in ("processor", "crypto", "all")}


def m_by_process(procs: Mapping, s: Mapping, p07: float, p0114: Mapping, bank_units: float) -> dict[str, float]:
    """Process m with P07 at the IRS-bounded P, P08 at its correction unit (wave 38B), P01/P14 per p0114 spec."""
    hc07 = ee.handling_cost(procs["P07"], "base")
    hc14 = ee.handling_cost(procs["P14"], "base")

    def one(pid):
        if pid == "P07":
            return ee.m_daf("P07", s["grant"], p07, hc07)
        if pid == "P08":
            return ee.CORRECTION_UNITS
        if pid in ("P01", "P14"):
            if p0114["kind"] == "bank":
                return p0114["p"] * s["t"] * s["alloc"] * bank_units + ee.CORRECTION_UNITS
            return p0114["p"] * p0114["usd"] / hc14 + ee.CORRECTION_UNITS
        return s["m_oper"]
    return {pid: one(pid) for pid in v2.SPONSOR_PROCS}


def composite(w: Mapping[str, float], mb: Mapping[str, float]) -> float:
    return sum(w[p] * mb[p] for p in v2.SPONSOR_PROCS)


def variants(procs: Mapping, pb: Mapping, ost: Mapping, bank_units: float) -> dict:
    """Composite settings: 38B-corrected baseline, IRS-bounded (bank analogue for P01/P14 kept), IRS + OFAC."""
    out = {}
    for name, s in ee.SETTINGS.items():
        ofac_usd = {"low": ost["processor"]["min"], "central": ost["processor"]["median"],
                    "high": ost["processor"]["max"]}[name]
        specs = {
            "w38b_baseline": (s["p"], {"kind": "bank", "p": s["p"]}),
            "irs_bounded": (pb[name], {"kind": "bank", "p": s["p"]}),
            "irs_bounded_ofac": (pb[name], {"kind": "ofac", "p": P_OFAC[name], "usd": ofac_usd}),
        }
        for vname, (p07, spec) in specs.items():
            mb = m_by_process(procs, s, p07, spec, bank_units)
            out[f"{vname}_{name}"] = {"m_by": mb, "composite": composite(ee.weights(procs), mb), "p07": p07,
                                      "spec": spec, "setting": dict(s)}
    return out


# ------------------------------------------------------------------------------------------- row builders
R = ee.row


def irs_rows(cov, soi, pb) -> list[dict]:
    rows = []
    for d in DATA_BOOK:
        src = f"{IRS_SOI}{d['t35']}"
        rows += [R("irs_exam", f"FY{d['fy']}", "returns_examined_990_990EZ_990N", float(d["ex_990"]), "returns", "F",
                   source=src, note="Data Book Table 3-5 (FY2021-24: Table 21), Forms 990, 990-EZ and 990-N"),
                 R("irs_exam", f"FY{d['fy']}", "returns_examined_990PF_1041A_1120POL_5227", float(d["ex_990pf"]),
                   "returns", "F", source=src),
                 R("irs_exam", f"FY{d['fy']}", "returns_examined_form_4720", float(d["ex_4720"]), "returns", "F",
                   source=src, note="related taxable returns: Form 4720 (excise taxes on exempt orgs and related persons)"),
                 R("irs_exam", f"FY{d['fy']}", "returns_examined_tege_total", float(d["ex_total"]), "returns", "F",
                   source=src, note="all TE/GE incl. employee plans, employment tax, bonds"),
                 R("irs_filed", f"FY{d['fy']}", "tax_exempt_org_returns_filed", float(d["eo_filed"]), "returns", "F",
                   source=f"{IRS_SOI}{d['t12']}", note="Table 1-2 (FY2021-24: Table 2); incl. 990-N, 990-PF, 990-T, 4720"),
                 R("irs_filed", f"FY{d['fy']}", "recognized_501c3_orgs", float(d["c3_orgs"]), "organizations", "F",
                   source=f"{IRS_SOI}{d['t26']}", note="Table 2-6 (FY2021-24: Table 14); incl. private foundations")]
    rows += [R("efile", f"PY{e['yr']}", f"efile_index_rows_{k}", float(e[k]), "returns", "C",
               source=EFILE_URL.format(y=e["yr"]), note="rows by RETURN_TYPE in the IRS e-file index (processing year)")
             for e in EFILE for k in ("990", "990EZ", "990PF")]
    rows += [R("tege_exam", f"FY{t['fy']}", "eo_filings_examined_closed", float(t["closed"]), "filings", "F",
               source=t["url"], note=f"TE/GE Accomplishments Letter; change rate {t['change_pct']}%; incl. related "
                                     "employment and excise returns") for t in TEGE_EO_EXAMS]
    rows.append(R("tege_exam", "FY2025", "eo_filings_examined_closed", float(next(c for c in cov if c["fy"] == 2025)["tege_closed"]),
                  "filings", "C", source=TIGTA_FY25["url"],
                  note=f"FY2021 x (1 - 15%); {TIGTA_FY25['report']}: \"{TIGTA_FY25['quote']}\" (rounded percent)"))
    for c in cov:
        fy = f"FY{c['fy']}"
        rows += [R("coverage", fy, "exam_rate_990_990EZ", c["narrow"], "share of filers", "C",
                   assumption="Data Book 990/990-EZ/990-N exams / e-filed 990 + 990-EZ (same processing year)",
                   note="990-N exams in the numerator, not the denominator: slight overstatement"),
                 R("coverage", fy, "exam_rate_990series_per_501c3_org", c["narrow_c3"], "share of orgs", "C",
                   assumption="Data Book 990-series exams / recognized 501(c)(3) organizations"),
                 R("coverage", fy, "exam_rate_eo_filings_broad", c["broad"], "share of filers", "C",
                   assumption="TE/GE EO filings examined (incl. related returns) / e-filed 990 + 990-EZ + 990-PF",
                   note=f"upper-side: numerator counts related employment/excise returns as separate filings; numerator basis {c['tege_basis']}"),
                 R("coverage", fy, "form4720_exams_per_eo_return_filed", c["ex_4720_per_eo_filed"], "ratio", "C")]
    for s in soi:
        src = f"{IRS_SOI}{s['file']}"
        cy = f"CY{s['cy']}"
        if s["n"] is not None:
            rows += [R("soi_4966", cy, "returns_reporting_4966_sponsor_tax", float(s["n"]), "returns", "F", source=src,
                       note="SOI Form 4720 study Table 1: 'Tax on taxable distributions of sponsoring organizations'"),
                     R("soi_4966", cy, "4966_sponsor_tax_usd", float(s["usd"]), "usd", "F", source=src),
                     R("soi_4966", cy, "4966_tax_per_return", s["per_return"], "usd", "C", source=src),
                     R("soi_4966", cy, "implied_taxable_distribution_per_return", s["implied_distribution"], "usd", "C",
                       source=src, assumption="tax / 20% (IRC 4966(a)(1))"),
                     R("soi_4966", cy, "share_of_daf_sponsors_reporting_4966", s["share_sponsors"], "share", "C",
                       source=f"{src}; {DAF_SPONSORS['url']}",
                       assumption=f"returns / {DAF_SPONSORS['n']:,} sponsors (FY2024); one return per sponsor")]
        else:
            rows += [R("soi_4966", cy, "returns_reporting_4966_sponsor_tax", "d", "returns", "F", source=src,
                       note="deleted to avoid disclosure; included in totals"),
                     R("soi_4966", cy, "4966_sponsor_tax_usd_upper_bound", s["usd_hi"], "usd", "C", source=src,
                       note="total organizational taxes minus all disclosed rows; shared with 3 other 'd' rows")]
        rows += [R("soi_4966", cy, "form4720_total_org_tax_returns", float(s["total_n"]), "returns", "F", source=src),
                 R("soi_4966", cy, "form4720_total_org_tax_usd", float(s["total_usd"]), "usd", "F", source=src)]
    taxed_max = max(s["n"] for s in soi if s["n"] is not None)
    rows += [R("p_detect", k, "p_detected_and_taxed", v, "prob", "C",
               assumption={"low": "min FY2021-25 exam_rate_990_990EZ; q=1",
                           "central": "median FY2021-25 exam_rate_990_990EZ; q=1",
                           "high": "max(max broad EO exam rate, max sponsors reporting 4966 / 1,512); q=1",
                           "sponsor_incidence_max": f"{taxed_max} returns / {DAF_SPONSORS['n']:,} sponsors; an upper bound "
                                                    "on P if every sponsor has >= 1 escaped taxable distribution a year [I]"}[k],
               note="replaces the unsourced 0.01 / 0.1 / 1 sweep; q = P(exam finds and taxes the error | exam) set to 1")
             for k, v in pb.items()]
    rows.append(R("p_detect", "fidelity_grant_check", "taxed_4966_returns_per_fidelity_grant",
                  taxed_max / FIDELITY_GRANTS_2024["n"], "ratio", "C", source=FIDELITY_GRANTS_2024["src"],
                  note="all sponsors' max yearly 4966 returns / Fidelity's 'nearly 2.7m' 2024 grants alone; an upper "
                       "bound on taxed events per grant across the industry"))
    return rows


def ofac_rows(procs) -> tuple[list[dict], dict]:
    hc = ee.handling_cost(procs["P14"], "base")
    rows = [R("ofac_scope", y, "release_rows_read", float(n), "releases", "F", source=OFAC_INDEX if y == "2026 YTD" else
              f"{OFAC_INDEX}/{y}-enforcement-information", note="no release names a charity, foundation, DAF sponsor "
              "or donor platform") for y, n in OFAC_PAGES]
    for o in OFAC_RELEASES:
        u = ofac_unit(o, hc)
        src = OFAC.format(o["media"])
        meta = f"{o['date']}; {o['kind']}; VSD {o['vsd']}; egregious {o['egregious']}"
        rows += [R("ofac", o["id"], "penalty_usd", o["penalty"], "usd", "F", o["entity"], source=src, note=meta),
                 R("ofac", o["id"], "apparent_violations", float(o["count"]), "count", "F" if o["count_basis"].startswith("stated") else "C",
                   o["entity"], source=src, note=f"group {o['group']}; count basis: {o['count_basis']}"),
                 R("ofac", o["id"], "usd_per_violation", u["per_violation"], "usd", "C", o["entity"], source=src),
                 R("ofac", o["id"], "m_conditional_P14_units", u["units"], "handling units", "C", o["entity"],
                   assumption="P14 base handling 15 min x $55.45/h; P(enforce)=1", source=src)]
        rows += [R("ofac", o["id"], k, float(o[f]), "usd", "F", o["entity"], source=src)
                 for k, f in (("violating_value_usd", "value"), ("statutory_max_usd", "stat_max"), ("base_penalty_usd", "base"))
                 if o[f] is not None]
        if u["per_value"] is not None:
            rows.append(R("ofac", o["id"], "penalty_per_usd_violating_value", u["per_value"], "ratio", "C", o["entity"], source=src))
        if u["share_base"] is not None:
            rows.append(R("ofac", o["id"], "penalty_share_of_base", u["share_base"], "ratio", "C", o["entity"], source=src))
        if u["per_missed_alert"] is not None:
            rows += [R("ofac", o["id"], "usd_per_missed_alert", u["per_missed_alert"], "usd", "C", o["entity"], source=src,
                       note="one high-confidence alert closed by an analyst; 214 violations followed"),
                     R("ofac", o["id"], "m_conditional_P14_units_per_missed_alert", u["per_missed_alert"] / hc,
                       "handling units", "C", o["entity"], source=src)]
    st = ofac_stats(hc)
    for g, d in st.items():
        rows += [R("ofac_range", f"{g}_{k}", "usd_per_violation", d[k], "usd", "C", note=f"n={d['n']}") for k in ("min", "median", "max")]
        rows += [R("ofac_range", f"{g}_{k}", "m_conditional_P14_units", d[k] / hc, "handling units", "C",
                   assumption="P(enforce)=1") for k in ("min", "median", "max")]
    return rows, st


def m_rows(var: Mapping) -> list[dict]:
    rows = []
    for name, r in var.items():
        sp = r["spec"]
        txt = (f"P07 p={r['p07']:.5g}; P08=correction unit; P01/P14 {sp['kind']} p={sp['p']:g}"
               + (f" usd={sp['usd']:.2f}" if sp["kind"] == "ofac" else "") + "; "
               + "; ".join(f"{k}={v:g}" for k, v in r["setting"].items() if k != "p"))
        rows += [R("m_process", name, f"m_{pid}", m, "handling units", "C+I", assumption=txt)
                 for pid, m in r["m_by"].items() if pid in ("P01", "P07", "P08", "P14")]
        rows.append(R("m_composite", name, "m_weighted_P01_P15", r["composite"], "handling units", "C+I", assumption=txt,
                      note="AI-amenable-pool-weighted (ee.weights); P08 at its correction unit per wave 38B"))
    return rows


def route_rows(procs_t, var: Mapping, draws: int) -> list[dict]:
    """Large-national CAL_CENTRAL route pool at the new m values (rv / ee functions, same seeds)."""
    procs = {p["id"]: p for p in procs_t}
    sponsors = v2.load_sponsors(v2.load_csv(v2.COST_CSV))
    anchors = v2.grant_anchors(sponsors, v2.load_csv(v2.SUMMARY_CSV))
    a = next(x for x in v2.ARCHETYPES if x["id"] == "NAT_LARGE")
    anc = v2.archetype_anchor(a, sponsors, anchors)
    spec = next(s for s in cal.CAL_SPECS if s["id"] == "CAL_CENTRAL")
    routes = rv.route_stream(draws)
    sims = cal.simulate(a, v2.ARCHETYPES.index(a), procs_t, anc, draws, spec, "v2", {})
    ds = tuple(rv.compact("CAL_CENTRAL", g, s, procs_t) for g, s in sims)
    cells = [("assist", "calibrated", lambda d, rp: rv.eval_draw(d, rp, "CAL_CENTRAL", "assist", 1.0, 1.0))]
    cells += [("route", f"m={m:g}", lambda d, rp, m=m: rv.eval_draw(d, rp, "CAL_CENTRAL", "route", m, 1.0)) for m in (1.0, 2.2)]
    cells += [("route", f"composite_{n}", lambda d, rp, m=r["composite"]: rv.eval_draw(d, rp, "CAL_CENTRAL", "route", m, 1.0))
              for n, r in var.items() if not n.startswith("w38b") or n.endswith("central")]
    cells += [(v, f"process_specific_{n}", lambda d, rp, mb=r["m_by"], v=v: ee.eval_draw_pm(d, rp, "CAL_CENTRAL", v, mb))
              for n, r in var.items() if n.endswith(("central", "high")) for v in ("route", "hybrid")]

    def summ(variant, cell, fn):
        sm = rv.summarise(tuple(fn(d, rp) for d, rp in zip(ds, routes)), procs_t, anc["available_n"])
        rid = f"CAL_CENTRAL|NAT_LARGE|{variant}|{cell}"
        print(f"{variant:<7}{cell:<38} pool p50 {sm['pool_q']['p50']:>12,.0f}  P(C 1st) {sm['mean_p_first_gross']:.4f}", flush=True)
        return [R("route", rid, "sponsor_ai_gross_value_p50", sm["pool_q"]["p50"], "usd/yr", "S",
                  note=f"p25={sm['pool_q']['p25']:.0f}; p75={sm['pool_q']['p75']:.0f}"),
                R("route", rid, "mean_p_C_rank_first_gross_P01_P15", sm["mean_p_first_gross"], "prob", "S"),
                R("route", rid, "P07_p_C_net_positive", sm["per"]["P07"]["p_net_pos"], "prob", "S")]
    return [r for v, c, fn in cells for r in summ(v, c, fn)]


def recount_efile(d: str) -> list[dict]:
    """Optional: re-count e-file index rows by RETURN_TYPE from local copies of the IRS index files."""
    def one(y):
        p = os.path.join(d, f"index_{y}.csv")
        with open(p, newline="", encoding="utf-8", errors="replace") as fh:
            c = collections.Counter(r["RETURN_TYPE"] for r in csv.DictReader(fh))
        return [R("meta", f"efile_recount_PY{y}", f"efile_index_rows_{k}", float(c.get(k, 0)), "returns", "C",
                  source=EFILE_URL.format(y=y)) for k in ("990", "990EZ", "990PF")]
    return [r for e in EFILE if os.path.exists(os.path.join(d, f"index_{e['yr']}.csv")) for r in one(e["yr"])]


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (CLI convention; paths come from v2)")
    ap.add_argument("--route", action="store_true", help="re-run the large-national CAL_CENTRAL route pool")
    ap.add_argument("--draws", type=int, default=10000)
    ap.add_argument("--efile-dir", default=None, help="directory holding IRS index_<yr>.csv files to re-count")
    ap.add_argument("--out", default=OUT_CSV)
    args = ap.parse_args(argv)
    procs_t = tuple(v2.v1_process(r) for r in v2.load_csv(v2.V1_CSV))
    procs = {p["id"]: p for p in procs_t}
    _, stats = ee.range_rows(procs)
    bank_units = stats["core_median"] / ee.handling_cost(procs["P14"], "base")
    cov = coverage_rows_data()
    soi = soi_4966()
    pb = p_bounds(cov, soi)
    orows, ost = ofac_rows(procs)
    var = variants(procs, pb, ost, bank_units)
    rows = [R("meta", "run", "draws", float(args.draws) if args.route else 0.0, "count", "",
              note="imports scripts/mission_escaped_error_cost.py unchanged; route rows only with --route")]
    rows += irs_rows(cov, soi, pb) + orows + m_rows(var)
    if args.efile_dir:
        rows += recount_efile(args.efile_dir)
    for c in cov:
        print(f"FY{c['fy']} exam rate 990/990EZ {c['narrow']:.5f}  per 501c3 {c['narrow_c3']:.5f}  broad {c['broad']:.5f}")
    print("P bounds:", {k: round(v, 5) for k, v in pb.items()})
    print("OFAC usd/violation:", {g: {k: round(v, 1) for k, v in d.items()} for g, d in ost.items()})
    for n, r in var.items():
        print(f"{n:<28} m = {r['composite']:.3f}  P07={r['m_by']['P07']:.3f} P14={r['m_by']['P14']:.2f}")
    if args.route:
        rows += route_rows(procs_t, var, args.draws)
    ee.write_csv(args.out, rows)
    print(f"wrote {len(rows)} rows -> {os.path.relpath(args.out, v2.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
