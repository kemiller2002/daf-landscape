#!/usr/bin/env python3
"""Escaped-error cost m for compliance processes, from 2021+ BSA/AML enforcement orders. Queue item P-G0403-04.

m is the routing variant's cost of an error that escapes review, in units of one case's handling time
(scripts/mission_ai_routing_variant.py: C_route = h*a_p*L*[(1-rho) - 0.5k - k e - (1-k) e m] - inference).

Steps (all pure functions; I/O only in main):
  1. ORDERS: penalty and stated count of missed/late SARs or missed alerts, quoted from each order (FinCEN
     consent orders 2021-2026; OCC and Federal Reserve figures where the FinCEN order or agency release states them).
     Every number in ORDERS is quoted from the primary URL in the row; nothing is estimated here.
  2. Dollars per missed SAR (or per alert), conditional on enforcement [C].
  3. Conversion to handling units with the model's own case-handling cost: minutes (low/base/high) x loaded rate
     from data/mission-2026-11-14/ai-process-economics.csv (P14 AML alert handling for the bank anchor) [C].
  4. Assumption sweeps [I]: penalty allocation to the missed SARs, probability that an escaped error is
     detected and penalised, lookback labour (BofA's 800 consultants) duration, and regime transfer to DAF sponsors.
  5. DAF-side m from the excise-tax regime (IRC 4966: 20% of a taxable distribution on the sponsor; 4967: 10% of a
     prohibited benefit on the fund manager), using grant-size anchors already in the repo [C + I].
  6. A process-weighted m for the routing model (one m for all processes) and a process-specific variant.
  7. Re-run of the routing variant at the proposed m values. scripts/mission_ai_routing_variant.py is IMPORTED,
     not modified: its pure functions (compact, eval_draw, c_value, per_case_yield, summarise, route_stream) are
     reused on the calibrated model's common random numbers (seed 42; routing stream 42+104729).

Output (new file): data/mission-2026-11-14/escaped-error-cost-2026-11-19.csv
Usage: python3 scripts/mission_escaped_error_cost.py . [--draws 10000] [--out PATH]
Stdlib only; functional style.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import math
import os
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_ai_routing_variant as rv  # noqa: E402

cal, v2 = rv.cal, rv.v2
OUT_CSV = os.path.join(v2.DATA, "escaped-error-cost-2026-11-19.csv")

FINCEN = "https://www.fincen.gov"
# ------------------------------------------------------------------------------------------- 1. orders [F]
# count_kind: missed_sar (never filed until a lookback), late_sar (filed late), sar_transactions (transactions on which
# a SAR should have been filed; not a SAR count), unreviewed_alerts, alerts_not_generated.
# qualifier: the order's own word before the count ("nearly", "over", "at least", "around", "well over").
ORDERS = (
    {"id": "BOFA_2026", "institution": "Bank of America, N.A.", "sector": "depository", "matter": "FinCEN 2026-03",
     "date": "2026-10-13", "period": "2018-01-01 to 2025-07-01", "fincen_cmp": 1_200_000_000,
     "credited": 750_000_000, "credited_to": "OCC", "other_agencies": {"OCC": 750_000_000},
     "count": 8_900, "count_kind": "missed_sar", "qualifier": "nearly", "sar_cap": 286_184,
     "quote": "the Bank had failed to identify and file nearly 8,900 SARs, with transaction activity totaling nearly "
              "$4 billion ... FinCEN is imposing a Civil Money Penalty of $1,200,000,000 ... credit against the Civil "
              "Money Penalty payment of $750,000,000 to the OCC",
     "url": FINCEN + "/system/files/2026-10/BoA-Consent-Order-Execution-Final.pdf"},
    {"id": "BOFA_2026_FILED", "institution": "Bank of America, N.A.", "sector": "depository",
     "matter": "FinCEN 2026-03", "date": "2026-10-13", "period": "2018-01-01 to 2025-07-01",
     "fincen_cmp": 1_200_000_000, "credited": 750_000_000, "credited_to": "OCC", "other_agencies": {"OCC": 750_000_000},
     "count": 8_000, "count_kind": "late_sar", "qualifier": "over", "sar_cap": 286_184,
     "quote": "This review resulted in the Bank filing over 8,000 SARs totaling approximately $3.96 billion in "
              "unreported suspicious activity",
     "url": FINCEN + "/system/files/2026-10/BoA-Consent-Order-Execution-Final.pdf"},
    {"id": "TD_2024", "institution": "TD Bank, N.A. and TD Bank USA, N.A.", "sector": "depository",
     "matter": "FinCEN 2024-02", "date": "2024-10-10", "period": "2012 to 2024-05-09", "fincen_cmp": 1_300_000_000,
     "credited": 543_000_000, "credited_to": "DOJ and OCC",
     "other_agencies": {"DOJ": 1_890_000_000, "FRB": 123_500_000, "OCC": 450_000_000},
     "count": 6_000, "count_kind": "late_sar", "qualifier": "over", "sar_cap": 278_937,
     "quote": "TD Bank willfully failed to timely file over 6,000 SARs. The aggregate value of this late-reported "
              "suspicious activity exceeded $500 million ... approximately $1.89 billion to DOJ, $123.5 million to "
              "the Federal Reserve Board, and $450 million to the OCC ... Civil Money Penalty of $ 1.3 billion ... "
              "credit ... payments of $543 million to DOJ and the OCC",
     "url": FINCEN + "/system/files/enforcement_action/2024-10-10/FinCEN-TD-Bank-Consent-Order-508FINAL.pdf"},
    {"id": "USAA_2022", "institution": "USAA Federal Savings Bank", "sector": "depository",
     "matter": "FinCEN 2022-01", "date": "2022-03-17", "period": "2016-01-01 to 2021-04-30",
     "fincen_cmp": 140_000_000, "credited": 60_000_000, "credited_to": "OCC", "other_agencies": {"OCC": 60_000_000},
     "count": 3_873, "count_kind": "late_sar", "qualifier": "at least", "sar_cap": 250_759,
     "quote": "willful failures to timely and accurately file at least 3,873 SARs ... filed late, with an average "
              "filing time of 226 days ... Civil Money Penalty of $140,000,000 ... credit the $60,000,000 ... OCC",
     "url": FINCEN + "/system/files/enforcement_action/2023-04-05/USAA_Consent_Order_Final_508_2.pdf"},
    {"id": "USAA_2022_ALERTS", "institution": "USAA Federal Savings Bank", "sector": "depository",
     "matter": "FinCEN 2022-01", "date": "2022-03-17", "period": "backlog at end-2021", "fincen_cmp": 140_000_000,
     "credited": 60_000_000, "credited_to": "OCC", "other_agencies": {"OCC": 60_000_000},
     "count": 90_000, "count_kind": "unreviewed_alerts", "qualifier": "around", "sar_cap": None,
     "quote": "a total backlog of around 90,000 un-reviewed alerts and 6,900 un-reviewed cases",
     "url": FINCEN + "/system/files/enforcement_action/2023-04-05/USAA_Consent_Order_Final_508_2.pdf"},
    {"id": "CBOT_2021", "institution": "CommunityBank of Texas, N.A.", "sector": "depository",
     "matter": "FinCEN 2021-03", "date": "2021-12-16", "period": "2015-01-01 to 2019-12-31", "fincen_cmp": 8_000_000,
     "credited": 1_000_000, "credited_to": "OCC", "other_agencies": {"OCC": 1_000_000},
     "count": 17, "count_kind": "missed_sar", "qualifier": "at least", "sar_cap": None,
     "quote": "the Bank willfully failed to file at least 17 SARs ... Civil Money Penalty of $8,000,000 ... credit the "
              "$1,000,000 ($1 million) civil penalty imposed by the OCC",
     "url": FINCEN + "/system/files/enforcement_action/2023-04-05/CBOT_Enf_Action_121621_508_FINAL.pdf"},
    {"id": "SHINHAN_2023_ALERTS", "institution": "Shinhan Bank America", "sector": "depository",
     "matter": "FinCEN 2023-03", "date": "2023-09-29", "period": "2016-04-01 to 2021-03-29", "fincen_cmp": 15_000_000,
     "credited": 5_000_000, "credited_to": "FDIC", "other_agencies": {"FDIC": 5_000_000},
     "count": 468, "count_kind": "alerts_not_generated", "qualifier": "exact (parallel test)", "sar_cap": None,
     "quote": "a parallel testing report issued in November 2020 identified 468 alerts that led to SAR filings under the "
              "old TM system but which failed even to generate an alert in the new TM system ... willful failure to "
              "timely file several hundred SARs",
     "url": FINCEN + "/system/files/enforcement_action/2023-09-29/SHBA_9-28_FINAL_508.pdf"},
    {"id": "BANCREDITO_2023", "institution": "Bancredito International Bank and Trust Corporation",
     "sector": "depository (Puerto Rico IFE)", "matter": "FinCEN 2023-02", "date": "2023-09-15", "period": "per order",
     "fincen_cmp": 15_000_000, "credited": 0, "credited_to": "", "other_agencies": {},
     "count": 300, "count_kind": "sar_transactions", "qualifier": "over", "sar_cap": None,
     "quote": "the independent lookback review supported OCIF's original findings that the over 300 transactions were "
              "suspicious, and resulted in Bancredito belatedly filing SARs",
     "url": FINCEN + "/system/files/enforcement_action/2023-09-15/Bancredito_Consent_FINAL_091523_508C.pdf"},
    {"id": "CANACCORD_2026", "institution": "Canaccord Genuity LLC", "sector": "broker-dealer",
     "matter": "FinCEN 2026-01", "date": "2026-03-06", "period": "2018-03-02 to 2024-06-30", "fincen_cmp": 80_000_000,
     "credited": 40_000_000, "credited_to": "SEC and FINRA", "other_agencies": {"SEC": 20_000_000, "FINRA": 20_000_000},
     "count": 160, "count_kind": "missed_sar", "qualifier": "at least (preliminary lookback)", "sar_cap": 286_184,
     "quote": "Based on preliminary results from a SAR Lookback, Canaccord failed to file at least 160 SARs ... Civil "
              "Money Penalty of $80 million ... suspend $5 million ... credit ... $20 million to the SEC and $20 "
              "million to FINRA",
     "url": FINCEN + "/system/files/2026-03/Canaccord-Consent-Order-No-2026-01.pdf"},
    {"id": "BITMEX_2021", "institution": "HDR Global Trading Ltd et al. (BitMEX)", "sector": "futures commission merchant",
     "matter": "FinCEN 2021-02", "date": "2021-08-10", "period": "2014-11-01 to 2020-12-12", "fincen_cmp": 100_000_000,
     "credited": 0, "credited_to": "", "other_agencies": {},
     "count": 588, "count_kind": "sar_transactions", "qualifier": "at least", "sar_cap": None,
     "quote": "FinCEN's initial assessment identified at least 588 transactions on which BitMEX should have filed a SAR "
              "... BitMEX agrees to pay a civil penalty in the amount of $100 million",
     "url": FINCEN + "/system/files/enforcement_action/2021-08-10/Assessment_BITMEX_508_FINAL_0.pdf"},
    {"id": "BINANCE_2023", "institution": "Binance Holdings Ltd et al.", "sector": "money services business",
     "matter": "FinCEN 2023-04", "date": "2023-11-21", "period": "per order", "fincen_cmp": 3_400_000_000,
     "credited": 0, "credited_to": "", "other_agencies": {},
     "count": 100_000, "count_kind": "sar_transactions", "qualifier": "well over", "sar_cap": None,
     "quote": "FinCEN identified well over a hundred thousand suspicious transactions that Binance failed to timely and "
              "accurately report ... Civil Money Penalty of $3.4 billion",
     "url": FINCEN + "/system/files/enforcement_action/2023-11-21/FinCEN_Consent_Order_2023-04_FINAL508.pdf"},
)
CORE_BANK = ("BOFA_2026", "TD_2024", "USAA_2022", "CBOT_2021")  # depository institutions, SAR counts stated

# 2021+ FinCEN orders read in full that state NO usable count (kept for the register; excluded from the range).
EXCLUDED = (
    ("CAPITAL_ONE_2021", "FinCEN 2021-01", 390_000_000, "no SAR count; counts given are 50,000+ unfiled CTRs and 75 alerts on one customer group",
     FINCEN + "/system/files/enforcement_action/2023-04-05/Assessment_CONA_508_0.pdf"),
    ("KINGDOM_TRUST_2023", "FinCEN 2023-01", 1_500_000, "'hundreds of suspicious transactions' (no number)",
     FINCEN + "/system/files/enforcement_action/2023-04-27/FinCEN_KTC_ConsentOrder_FINAL_042523.pdf"),
    ("SHINHAN_2023_SARS", "FinCEN 2023-03", 15_000_000, "'several hundred SARs' filed late (no number); alerts row kept",
     FINCEN + "/system/files/enforcement_action/2023-09-29/SHBA_9-28_FINAL_508.pdf"),
    ("BITTREX_2022", "FinCEN 2022-03", 29_280_829, "no count of unfiled SARs",
     FINCEN + "/system/files/enforcement_action/2023-04-04/Bittrex_Consent_Order_10.11.2022.pdf"),
    ("LAKE_ELSINORE_2024", "FinCEN 2024-03", None, "'dozens of instances' (no number)",
     FINCEN + "/system/files/enforcement_action/2024-10-23/FinCEN-Consent-Order-Lake-Elsinore-508.pdf"),
    ("BRINKS_2025", "FinCEN 2025-01", 37_000_000, "filed no SARs; no count of reportable transactions",
     FINCEN + "/system/files/enforcement_action/2025-02-06/FinCEN-Brinks-FINALv508.pdf"),
    ("PAXFUL_2025", "FinCEN 2025-02", 3_500_000, "'hundreds of suspicious transactions' (no number)",
     FINCEN + "/system/files/2025-12/PaxfulConsentOrder.pdf"),
    ("UBS_2026", "FinCEN 2026-02", 125_000_000, "'hundreds of suspicious transactions' (no number)",
     FINCEN + "/system/files/2026-07/UBS-Consent-Order.pdf"),
    ("TD_2024_FRB", "FRB order 2024-10-10", 123_500_000, "Federal Reserve order states no SAR or alert count",
     "https://www.federalreserve.gov/newsevents/pressreleases/files/enf20241010a1.pdf"),
    ("TD_2024_OCC", "OCC NR 2024-116", 450_000_000, "OCC release: 'numerous violations', no count",
     "https://www.occ.gov/news-issuances/news-releases/2024/nr-occ-2024-116.html"),
    ("BOFA_2026_OCC", "OCC NR 2026-89", 750_000_000, "OCC release: 'large numbers of late SARs', no count",
     "https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-89.html"),
)

# ------------------------------------------------------------------------------------------- DAF regime [F]
IRC_4966 = {"sponsor_rate": 0.20, "manager_rate": 0.05, "manager_cap": 10_000,
            "url": "https://www.law.cornell.edu/uscode/text/26/4966"}
IRC_4967 = {"advisor_rate": 1.25, "manager_rate": 0.10, "manager_cap": 10_000,
            "url": "https://www.law.cornell.edu/uscode/text/26/4967"}
# Grant-size anchors already in the repo (quoted there with primary URLs).
GRANT_ANCHORS = (
    ("DAFgiving360 median grant FY2026", 500.0, "research/mission-2026-11-14/quantitative-datasets-and-data-dictionary.md; https://www.dafgiving360.org/press-release/fiscal-year-2026-results"),
    ("JCF NY median grant FY2023", 750.0, "research/mission-2026-11-14/direction-faith-giving-platforms.md; https://jcfny.org/app/uploads/2024/04/2023-JCF-Giving-Report.pdf"),
    ("Fidelity Charitable mean grant (about)", 5_100.0, "research/mission-2026-11-14/ai-economics-v2-observed-costs.md (grant anchors)"),
    ("Vanguard Charitable mean grant", 11_400.0, "research/mission-2026-11-14/ai-economics-v2-observed-costs.md (grant anchors)"),
    ("NPT mean grant", 40_000.0, "research/mission-2026-11-14/ai-economics-v2-observed-costs.md (grant anchors)"),
)

# ------------------------------------------------------------------------------------------- assumptions [I]
ALLOC = (0.25, 0.5, 1.0)          # share of the penalty attributed to the missed SARs (rest: program, CDD, etc.)
P_ENF = (0.01, 0.1, 1.0)          # probability an escaped error is detected and penalised (1 = conditional on enforcement)
LOOKBACK_YEARS = (0.5, 1.0, 2.0)  # duration of BofA's 800-consultant lookback (not stated in the order)
FTE_HOURS = 2_080.0               # hours per full-time year (52 x 40), a convention
TRANSFER = (0.0, 0.01, 0.1)       # share of a bank's per-missed-SAR cost that carries to a DAF sponsor's P01/P14
M_OPER = (1.0, 2.0, 5.0)          # escaped operational error: >= 1 handling unit of rework, up to 5 with donor contact
CORRECTION_UNITS = 1.0            # an escaped compliance error, once found, is reworked at one handling unit (model convention)
SETTINGS = {  # low / central / high composite settings (one value from each sweep)
    "low": {"p": 0.01, "grant": 500.0, "m_oper": 1.0, "t": 0.0, "alloc": 0.25},
    "central": {"p": 0.1, "grant": 5_100.0, "m_oper": 2.0, "t": 0.01, "alloc": 0.5},
    "high": {"p": 1.0, "grant": 40_000.0, "m_oper": 5.0, "t": 0.1, "alloc": 1.0},
}
M_GRID = (0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0, 50.0, 100.0)
ROUTE_SCENARIOS = ("CAL_CENTRAL", "CAL_COMPLIANCE_FULL")


# ------------------------------------------------------------------------------------------- pure helpers
def handling_cost(p: Mapping, which: str) -> float:
    """USD per case = minutes x loaded rate / 60 (ai-process-economics.csv)."""
    return p[f"minutes_{which}"] * p["loaded_rate_usd_hr"] / 60.0


def unique_total(o: Mapping) -> float:
    """FinCEN penalty plus other agencies' amounts not credited against it (computed from the order's own figures)."""
    return o["fincen_cmp"] + sum(o["other_agencies"].values()) - o["credited"]


def per_unit(o: Mapping) -> dict:
    tot = unique_total(o)
    return {"fincen": o["fincen_cmp"] / o["count"], "all_agency": tot / o["count"], "all_agency_total": tot,
            "cap_share": (o["fincen_cmp"] / (o["count"] * o["sar_cap"])) if o["sar_cap"] else None}


def m_bank(usd_per_sar: float, hc: float, alloc: float, p: float) -> float:
    return p * alloc * usd_per_sar / hc


def lookback_units(o: Mapping, years: float, hc_minutes: float) -> float:
    """BofA: 800 consultants for the one-time lookback, per missed SAR, in handling units of hc_minutes."""
    return 800.0 * years * FTE_HOURS * 60.0 / o["count"] / hc_minutes


def m_daf(proc: str, grant: float, p: float, hc: float) -> float:
    """Sponsor-side cost of an escaped DAF compliance error, in handling units, expected over detection p."""
    if proc == "P07":
        tax = IRC_4966["sponsor_rate"] * grant
    elif proc == "P08":
        tax = min(IRC_4967["manager_rate"] * grant, IRC_4967["manager_cap"])
    else:
        tax = 0.0
    return p * tax / hc + CORRECTION_UNITS


def median(xs: Sequence[float]) -> float:
    return v2.quantile(sorted(xs), 0.5)


def process_m(procs: Mapping[str, Mapping], s: Mapping, bank_cond_units: float) -> dict[str, float]:
    """m by process for one composite setting."""
    out = {}
    for pid in v2.SPONSOR_PROCS:
        if pid in ("P07", "P08"):
            out[pid] = m_daf(pid, s["grant"], s["p"], handling_cost(procs[pid], "base"))
        elif pid in ("P01", "P14"):
            out[pid] = s["p"] * s["t"] * s["alloc"] * bank_cond_units + CORRECTION_UNITS
        else:
            out[pid] = s["m_oper"]
    return out


def weights(procs: Mapping[str, Mapping]) -> dict[str, float]:
    """AI-amenable labour pool share by process (v1 base pool x ai_amenability), P01-P15."""
    raw = {pid: procs[pid]["labor_pool_base_usd"] * procs[pid]["ai_amenability"] for pid in v2.SPONSOR_PROCS}
    tot = sum(raw.values())
    return {pid: v / tot for pid, v in raw.items()}


def breakeven_m(rp: Mapping, k: float) -> float:
    """m at which an AI-closed case saves nothing: (1 - rho - 0.5k - k e) / ((1 - k) e)."""
    den = (1.0 - k) * rp["e"]
    num = 1.0 - rp["rho"] - 0.5 * k - k * rp["e"]
    return num / den if den > 0 else math.inf


def eval_draw_pm(d: Mapping, rp: Mapping, scn: str, variant: str, m_by: Mapping[str, float]) -> dict:
    """rv.eval_draw with a process-specific m (re-uses rv.c_value and rv.per_case_yield unchanged)."""
    out = {}
    for cp in d["procs"]:
        m = m_by.get(cp["pid"], 1.0)
        c = rv.c_value(variant, cp, rp, scn, m)
        gross = {**cp["others"], "C": c}
        net = {i: gross[i] - cp["F"][i] for i in rv.OTHERS}
        net["C"] = c - cp["F"]["C"]
        y = cp["a"] * cp["L"] * rv.per_case_yield(rp, rv.k_for(scn, cp["pid"], rp["k"]), m)
        out[cp["pid"]] = {"c": c, "first_gross": v2.argmax(gross), "first_net": v2.argmax({**net, "none": 0.0}),
                          "net_pos": net["C"] > 0,
                          "h_be_net": (cp["F"]["C"] + cp["inf"]) / y if y > 0 else math.inf,
                          "h_be_rank": (max(cp["others"].values()) + cp["inf"]) / y if y > 0 else math.inf}
    pool = sum(max(0.0, out[k]["c"]) for k in v2.SPONSOR_PROCS)
    return {"proc": out, "pool": pool, "n_be": v2.breakeven_n(pool, d["tau"], d["F_platform"], d["f_sponsor"])}


def row(rt, rid, metric, value, unit="", basis="", entity="", assumption="", source="", note="") -> dict:
    v = round(value, 6) if isinstance(value, float) and math.isfinite(value) else value
    return {"record_type": rt, "id": rid, "entity": entity, "metric": metric, "value": v, "unit": unit,
            "basis": basis, "assumption": assumption, "source": source, "note": note}


# ------------------------------------------------------------------------------------------- record builders
def order_rows(procs) -> list[dict]:
    hc = {w: handling_cost(procs["P14"], w) for w in ("low", "base", "high")}
    out = []
    for o in ORDERS:
        u = per_unit(o)
        src = o["url"]
        out += [row("order", o["id"], "fincen_cmp_usd", float(o["fincen_cmp"]), "usd", "F", o["institution"], source=src,
                    note=f"{o['matter']}; {o['date']}; {o['sector']}; period {o['period']}; quote: {o['quote']}"),
                row("order", o["id"], "count", float(o["count"]), o["count_kind"], "F", o["institution"], source=src,
                    note=f"qualifier: {o['qualifier']}"),
                row("order", o["id"], "all_agency_total_usd", u["all_agency_total"], "usd", "C", o["institution"],
                    source=src, note="FinCEN CMP + other agencies stated in the FinCEN order - FinCEN credit; "
                                     f"credited to {o['credited_to'] or 'none'}; may double count where agencies overlap"),
                row("order", o["id"], "usd_per_unit_fincen", u["fincen"], f"usd per {o['count_kind']}", "C",
                    o["institution"], source=src),
                row("order", o["id"], "usd_per_unit_all_agency", u["all_agency"], f"usd per {o['count_kind']}", "C",
                    o["institution"], source=src)]
        if u["cap_share"] is not None:
            out.append(row("order", o["id"], "fincen_cmp_share_of_per_sar_statutory_max", u["cap_share"], "ratio", "C",
                           o["institution"], source=src,
                           note=f"CMP / (count x per-violation cap ${o['sar_cap']:,} quoted in the order)"))
        for w in ("low", "base", "high"):
            out.append(row("order", o["id"], f"m_conditional_full_alloc_hc_{w}", u["fincen"] / hc[w], "handling units",
                           "C", o["institution"], f"P14 handling {procs['P14'][f'minutes_{w}']:g} min x "
                           f"${procs['P14']['loaded_rate_usd_hr']}/h; alloc 1; P(enforce)=1", src))
    for eid, matter, pen, why, url in EXCLUDED:
        out.append(row("excluded", eid, "penalty_usd", float(pen) if pen else "", "usd", "F", matter, source=url,
                       note=f"excluded from range: {why}"))
    return out


def range_rows(procs) -> tuple[list[dict], dict]:
    hc = handling_cost(procs["P14"], "base")
    core = [per_unit(o)["fincen"] for o in ORDERS if o["id"] in CORE_BANK]
    sar_like = [per_unit(o)["fincen"] for o in ORDERS if o["count_kind"] in ("missed_sar", "late_sar", "sar_transactions")
                and not o["id"].endswith("_FILED")]
    alerts = [per_unit(o)["fincen"] for o in ORDERS if "alerts" in o["count_kind"]]
    stats = {"core_min": min(core), "core_median": median(core), "core_max": max(core),
             "all_min": min(sar_like), "all_median": median(sar_like), "all_max": max(sar_like),
             "alert_min": min(alerts), "alert_max": max(alerts)}
    out = [row("range", k, "usd_per_missed_unit", v, "usd", "C",
               note="core = 4 depository orders with SAR counts (BofA, TD, USAA, CBOT); all = every SAR or "
                    "SAR-transaction count incl. non-banks; alert = per unreviewed / not-generated alert")
           for k, v in stats.items()]
    out += [row("range", k, "m_conditional_full_alloc", v / hc, "handling units", "C",
                assumption="P14 base handling 15 min x $55.45/h; allocation 1; P(enforce)=1") for k, v in stats.items()]
    for a, p in itertools.product(ALLOC, P_ENF):
        out.append(row("bank_m_grid", f"alloc={a:g}_p={p:g}", "m_expected_core_median",
                       m_bank(stats["core_median"], hc, a, p), "handling units", "I",
                       assumption=f"penalty allocation {a:g}; P(detected and penalised) {p:g}; P14 base handling"))
    bofa = next(o for o in ORDERS if o["id"] == "BOFA_2026")
    for yrs in LOOKBACK_YEARS:
        out.append(row("lookback", f"BOFA_years={yrs:g}", "lookback_units_per_missed_sar",
                       lookback_units(bofa, yrs, procs["P14"]["minutes_base"]), "handling units", "I",
                       "BofA", f"800 consultants x {yrs:g} yr x {FTE_HOURS:g} h / 8,900 SARs / 15-min P14 case",
                       bofa["url"], "duration not stated in the order; consultant hours priced at the P14 handling rate "
                                    "(a lower bound on consultant cost)"))
    return out, stats


def daf_rows(procs) -> list[dict]:
    out = []
    for (lab, g, src), pid, p in itertools.product(GRANT_ANCHORS, ("P07", "P08"), P_ENF):
        hc = handling_cost(procs[pid], "base")
        out.append(row("daf_m", f"{pid}_G={g:g}_p={p:g}", "m_expected", m_daf(pid, g, p, hc), "handling units", "C+I",
                       lab, f"{'IRC 4966 20% sponsor tax' if pid == 'P07' else 'IRC 4967 10% manager tax (cap $10k)'}; "
                            f"P(detected and taxed) {p:g}; +{CORRECTION_UNITS:g} correction unit; handling "
                            f"{procs[pid]['minutes_base']:g} min x ${procs[pid]['loaded_rate_usd_hr']}/h",
                       f"{IRC_4966['url'] if pid == 'P07' else IRC_4967['url']}; {src}"))
    return out


def composite_rows(procs, stats) -> tuple[list[dict], dict]:
    w = weights(procs)
    hc = handling_cost(procs["P14"], "base")
    bank_units = stats["core_median"] / hc
    wc = sum(w[p] for p in cal.COMPLIANCE_PROCS)
    out = [row("weights", pid, "ai_amenable_pool_share", w[pid], "share", "C",
               note="v1 labor_pool_base_usd x ai_amenability, P01-P15") for pid in v2.SPONSOR_PROCS]
    out.append(row("weights", "COMPLIANCE", "ai_amenable_pool_share", wc, "share", "C",
                   note="P01, P07, P08, P14 (cal.COMPLIANCE_PROCS)"))
    res = {}
    for name, s in SETTINGS.items():
        mp = process_m(procs, s, bank_units)
        comp = sum(w[p] * mp[p] for p in v2.SPONSOR_PROCS)
        res[name] = {"m_by": mp, "composite": comp}
        txt = "; ".join(f"{k}={v:g}" for k, v in s.items())
        out += [row("composite", name, f"m_{pid}", mp[pid], "handling units", "I", assumption=txt)
                for pid in v2.SPONSOR_PROCS]
        out.append(row("composite", name, "m_weighted_P01_P15", comp, "handling units", "I", assumption=txt,
                       note="AI-amenable-pool-weighted mean of process m; the routing model's single m"))
    return out, res


def route_rows(procs, sponsors, anchors, draws, comp) -> list[dict]:
    anchor_by = {a["id"]: v2.archetype_anchor(a, sponsors, anchors) for a in v2.ARCHETYPES}
    routes = rv.route_stream(draws)
    out = []
    bm = [breakeven_m(r, r["k"]) for r in routes]
    for lab, q in (("p05", .05), ("p25", .25), ("p50", .5), ("p75", .75), ("p95", .95)):
        out.append(row("breakeven_m", lab, "m_at_zero_saving_per_ai_closed_case", v2.quantile(sorted(bm), q),
                       "handling units", "C", note="(1 - rho - 0.5k - k e)/((1-k) e) over routing draws (k, e, rho=0)"))
    for name, r in comp.items():
        out.append(row("breakeven_m", name, "share_draws_m_above_breakeven",
                       sum(r["composite"] > x for x in bm) / len(bm), "prob", "S",
                       note=f"composite m={r['composite']:.3g}"))
    for scn in ROUTE_SCENARIOS:
        spec = next(s for s in cal.CAL_SPECS if s["id"] == scn)
        archs = v2.ARCHETYPES if scn == "CAL_CENTRAL" else tuple(a for a in v2.ARCHETYPES if a["id"] == "NAT_LARGE")
        for a in archs:
            idx = v2.ARCHETYPES.index(a)
            aid, avail = a["id"], anchor_by[a["id"]]["available_n"]
            sims = cal.simulate(a, idx, procs, anchor_by[aid], draws, spec, "v2", {})
            ds = tuple(rv.compact(scn, g, s, procs) for g, s in sims)
            del sims
            base = rv.summarise(tuple(rv.eval_draw(d, rp, scn, "assist", 1.0, 1.0) for d, rp in zip(ds, routes)),
                                procs, avail)
            cells = [(f"m={m:g}", "route", lambda d, rp, m=m: rv.eval_draw(d, rp, scn, "route", m, 1.0)) for m in M_GRID]
            cells += [(f"m={m:g}", "hybrid", lambda d, rp, m=m: rv.eval_draw(d, rp, scn, "hybrid", m, 1.0))
                      for m in (1.0, 5.0, 20.0)]
            cells += [(f"composite_{n}_m={r['composite']:.3g}", "route",
                       lambda d, rp, m=r["composite"]: rv.eval_draw(d, rp, scn, "route", m, 1.0)) for n, r in comp.items()]
            cells += [(f"process_specific_{n}", v, lambda d, rp, mb=r["m_by"], v=v: eval_draw_pm(d, rp, scn, v, mb))
                      for n, r in comp.items() for v in ("route", "hybrid")]
            msg = [f"assist pool={base['pool_q']['p50']:,.0f}"]
            out += summary_rows(scn, aid, "assist", "calibrated", base)
            for cell, variant, fn in cells:
                sm = rv.summarise(tuple(fn(d, rp) for d, rp in zip(ds, routes)), procs, avail)
                out += summary_rows(scn, aid, variant, cell, sm)
                msg.append(f"{variant}/{cell} C1st={sm['mean_p_first_gross']:.4f} pool={sm['pool_q']['p50']:,.0f}")
            print(f"{scn:<20} {aid:<10} " + " | ".join(msg), flush=True)
    return out


def summary_rows(scn, aid, variant, cell, sm) -> list[dict]:
    rid = f"{scn}|{aid}|{variant}|{cell}"
    q = sm["pool_q"]
    rows = [row("route", rid, "mean_p_C_rank_first_gross_P01_P15", sm["mean_p_first_gross"], "prob", "S"),
            row("route", rid, "mean_p_C_rank_first_net_P01_P15", sm["mean_p_first_net"], "prob", "S"),
            row("route", rid, "sponsor_ai_gross_value_p50", q["p50"], "usd/yr", "S",
                note=f"p25={q['p25']:.0f}; p75={q['p75']:.0f}"),
            row("route", rid, "max_process_p_C_net_positive", sm["max_p_net_pos"], "prob", "S"),
            row("route", rid, "p_vendor_breakeven_finite", sm["p_be_finite"], "prob", "S"),
            row("route", rid, "P07_p_C_net_positive", sm["per"]["P07"]["p_net_pos"], "prob", "S"),
            row("route", rid, "P14_p_C_net_positive", sm["per"]["P14"]["p_net_pos"], "prob", "S")]
    if sm["p_be_le_avail"] is not None:
        rows.append(row("route", rid, "p_vendor_breakeven_le_available", sm["p_be_le_avail"], "prob", "S"))
    return rows


def replication_rows(rows: Sequence[Mapping]) -> list[dict]:
    """Compare m = 1 / 5 / 20 route cells with the routing variant's published CSV (same seeds)."""
    ref_path = rv.OUT_CSV
    if not os.path.exists(ref_path):
        return [row("meta", "replication", "status", "reference CSV missing")]
    with open(ref_path, newline="", encoding="utf-8") as fh:
        ref = {(r["scenario"], r["archetype"], r["variant"], r["cell"], r["metric"]): float(r["value"])
               for r in csv.DictReader(fh) if r["process_id"] == "" and r["value"] not in ("", "inf", "nan")
               and r["metric"] in ("sponsor_ai_gross_value_p50", "mean_p_C_rank_first_gross_P01_P15")}
    mine = {r["id"] + "|" + r["metric"]: r["value"] for r in rows if r["record_type"] == "route"}
    diffs = []
    for (scn, aid, var, cell, metric), v in ref.items():
        if var == "route" and cell in ("main_m1", "main_m5", "main_m20") and scn in ROUTE_SCENARIOS:
            key = f"{scn}|{aid}|route|m={cell[6:]}|{metric}"
            if key in mine:
                diffs.append(abs(mine[key] - v) / max(1.0, abs(v)))
    return [row("meta", "replication", "max_rel_diff_vs_ai-routing-variant-2026-11-19.csv",
                max(diffs) if diffs else math.nan, "ratio", "C", note=f"{len(diffs)} cells compared")]


def write_csv(path: str, rows: Sequence[Mapping]) -> None:
    cols = ("record_type", "id", "entity", "metric", "value", "unit", "basis", "assumption", "source", "note")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (CLI convention; paths come from v2)")
    ap.add_argument("--draws", type=int, default=10000)
    ap.add_argument("--out", default=OUT_CSV)
    args = ap.parse_args(argv)
    proc_t = tuple(v2.v1_process(r) for r in v2.load_csv(v2.V1_CSV))
    procs = {p["id"]: p for p in proc_t}
    sponsors = v2.load_sponsors(v2.load_csv(v2.COST_CSV))
    anchors = v2.grant_anchors(sponsors, v2.load_csv(v2.SUMMARY_CSV))
    rows = order_rows(procs)
    rr, stats = range_rows(procs)
    rows += rr + daf_rows(procs)
    cr, comp = composite_rows(procs, stats)
    rows += cr
    for k, v in stats.items():
        print(f"{k:<14} ${v:>12,.0f}  m(cond, alloc 1, P14 base) = {v / handling_cost(procs['P14'], 'base'):>10,.0f}")
    for n, r in comp.items():
        print(f"composite {n:<8} m = {r['composite']:.3f}  by process: " +
              ", ".join(f"{p}={m:.2f}" for p, m in r["m_by"].items()))
    rows += route_rows(proc_t, sponsors, anchors, args.draws, comp)
    rows += replication_rows(rows)
    rows.insert(0, row("meta", "run", "draws", float(args.draws), "count", "",
                       note=f"calibrated draws Random({v2.SEED}); routing stream Random({rv.ROUTE_SEED})"))
    print(next(r for r in rows if r["id"] == "replication"))
    write_csv(args.out, rows)
    print(f"wrote {len(rows)} rows -> {os.path.relpath(args.out, v2.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
