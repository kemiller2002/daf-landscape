#!/usr/bin/env python3
"""Exception share per GRANT, not per Schedule I recipient line (queue item P-G05-02).

The exception-load proxy (scripts/mission_exception_load.py; research/mission-2026-11-14/gap19-exception-load-proxy.md)
reports category shares of Schedule I recipient lines and of dollars. A Schedule I line is one recipient per return,
itemised only above $5,000, so neither share is a share of grants. This script converts the proxy to grants for the
top-50 sponsors that publish an annual grant count, using the sponsor's own count and, where published, its count
of distinct recipients.

Per sponsor-year the grant book is split into three recipient groups:
  itemised   Schedule I Part II lines (amount d_i > 0; flags from mission_exception_load.line_flags, unchanged);
  foreign    Schedule F foreign recipients (count and Part IX line 3 dollars, as in the proxy), each at the mean amount;
  unitemised R_U = R - (itemised + foreign) recipients that received $5,000 or less in aggregate, holding
             D_U = Part IX lines 1-3 - Schedule I - line 3 dollars, each at the mean amount D_U / R_U.
R is the sponsor's published count of distinct recipients; where none is published it is imputed from the
R / (itemised + foreign) ratios of the sponsors that publish one (min and max, labelled [I]).

ASSUMPTION (stated, swept): grants per recipient n_i = max(1, k * d_i^beta), with k solved so that the grants sum to
the sponsor's published count G. beta = 0 gives every recipient the same number of grants (recipient-weighted);
beta = 1 gives every grant the same size (dollar-weighted); the floor of 1 holds because every listed recipient got
at least one grant. Swept beta in {0, 0.25, 0.5, 0.75, 1}. Category shares by grant = sum of n_i over flagged
recipients / G.
Unitemised flag rules (swept): none (u_c = 0); small_band (each category's line share among itemised lines of
<= $10,000, the nearest observed size band); all_itemised (line share across all itemised lines).
Foreign rule (swept): model (Schedule F recipients follow the beta rule) or anchored (each Schedule F recipient
gets 528/323 = 1.63 grants: NPT FY2025 annual report, "528 international grants ... to 323 organizations").

Calibration moments reported (not used to pick a point value):
  Fidelity: grants of $1 million or more (2023, 2024, 2025 Giving Reports: 1,407 / 1,345 / 1,971 in CY2022-24);
  NPT: international grants (annual report chart: 335 in FY2023, 406 in FY2024).

Inputs: the same caches as mission_exception_load.py (--np-cache, --lines-cache, --bmf-dir, --pub78) plus the
published counts in GRANT_COUNTS below (each with its URL). Output (new file):
  data/mission-2026-11-14/exception-share-per-grant-2026-11-19.csv
Usage:
  python3 scripts/mission_exception_per_grant.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --pub78 data-download-pub78.txt [--out PATH]
Stdlib only; functional style (pure functions; I/O only in load_* / main).
"""
from __future__ import annotations

import argparse
import bisect
import csv
import math
import os
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_exception_load as xl  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, read_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_compliance import load_bmf_ext, load_pub78, period_of, screen  # noqa: E402
from mission_recipient_sectors import WHITELIST, annotate, load_lines  # noqa: E402

OUT = os.path.join(DATA, "exception-share-per-grant-2026-11-19.csv")
PROXY_CSV = os.path.join(DATA, "exception-load-proxy-2026-11-19.csv")
CATS = ("foreign", "not_c3_or_not_pub78", "not_c3_or_not_pub78_unexplained", "recent_ruling_24m",
        "fiscal_sponsor_name", "pf_or_er", "er_required", "any", "any_core")
LINE_CAT = {"foreign_si": "foreign", "any_si": "any", "any_core_si": "any_core"}
BETAS = (0.0, 0.25, 0.5, 0.75, 1.0)
BETA_FINE = tuple(i / 20 for i in range(0, 21))
U_RULES = ("none", "small_band", "all_itemised")
F_RULES = ("model", "anchored")
SMALL_BAND = 10_000.0
FOREIGN_GRANTS_PER_RECIPIENT = 528 / 323   # NPT FY2025 annual report
NPT_REPORT = "https://www.nptrust.org/annual-reports/npt-annual-report/"
FC = {2022: "https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf",
      2023: "https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf",
      2024: "https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf"}
VC = {y: f"https://www.vanguardcharitable.org/{y}annualreport" for y in (2022, 2023, 2024)}
GT = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml"


def mean2(a: float, b: float) -> float:
    return (a + b) / 2.0


# Published counts per DAFRC fiscal year (the Schedule I return's tax period). G = grants, R = distinct recipients,
# usd = the source's grant dollars (consistency check against Part IX). basis says how the period was matched.
# Fidelity and Vanguard publish calendar years; their 990 years end 30 June, so FY = mean of the two calendar years.
GRANT_COUNTS = (
    {"ein": "110303001", "sponsor": "Fidelity Charitable", "fy": 2023, "tier": "annual_report",
     "G": mean2(2_185_516, 2_340_165), "R": mean2(200_000, 199_000), "usd": mean2(11.20e9, 11.8e9),
     "basis": "mean of CY2022 (2,185,516; 'nearly 200,000' charities) and CY2023 (2,340,165; 199K charities)",
     "url": f"{FC[2022]} ; {FC[2023]}", "m1m": mean2(1_407, 1_345)},
    {"ein": "110303001", "sponsor": "Fidelity Charitable", "fy": 2024, "tier": "annual_report",
     "G": mean2(2_340_165, 2_664_446), "R": mean2(199_000, 213_476), "usd": mean2(11.8e9, 14.9e9),
     "basis": "mean of CY2023 (2,340,165; 199K) and CY2024 (2,664,446; 213,476 charities)",
     "url": f"{FC[2023]} ; {FC[2024]}", "m1m": mean2(1_345, 1_971)},
    {"ein": "237825575", "sponsor": "National Philanthropic Trust", "fy": 2023, "tier": "annual_report",
     "G": 106_235, "R": 36_000, "usd": 4.54e9, "intl_grants": 335,
     "basis": "FY ended 2023-06-30, same period; R 'approximately 36,000' from the same 990 Part III",
     "url": f"{NPT_REPORT} ; {GT.format('202431429349301368')}"},
    {"ein": "237825575", "sponsor": "National Philanthropic Trust", "fy": 2024, "tier": "annual_report",
     "G": 129_575, "R": 41_000, "usd": 5.49e9, "intl_grants": 406,
     "basis": "FY ended 2024-06-30, same period; R 'over 41,000' from the same 990 Part III",
     "url": f"{NPT_REPORT} ; {GT.format('202511339349301311')}"},
    {"ein": "232888152", "sponsor": "Vanguard Charitable", "fy": 2023, "tier": "annual_report",
     "G": mean2(196_000, 209_000), "R": mean2(52_800, 56_744), "usd": mean2(1.87e9, 2.6e9),
     "basis": "mean of CY2022 ('196K' grant units; 52,800 orgs) and CY2023 ('209K'; 56,744 orgs); counts rounded",
     "url": f"{VC[2022]} ; {VC[2023]}"},
    {"ein": "232888152", "sponsor": "Vanguard Charitable", "fy": 2024, "tier": "annual_report",
     "G": mean2(209_000, 240_064), "R": mean2(56_744, 62_586), "usd": mean2(2.6e9, 3.1e9),
     "basis": "mean of CY2023 ('209K'; 56,744) and CY2024 (240,064; 62,586 charities)",
     "url": f"{VC[2023]} ; {VC[2024]}"},
    {"ein": "311774905", "sponsor": "Goldman Sachs Philanthropy Fund", "fy": 2023, "tier": "form990_part_iii",
     "G": 24_800, "R": None, "usd": 2_135_242_000, "basis": "CY2023 return, same period; 'approximately 24,800 grants'",
     "url": GT.format("202413109349303336")},
    {"ein": "311774905", "sponsor": "Goldman Sachs Philanthropy Fund", "fy": 2024, "tier": "form990_part_iii",
     "G": 29_254, "R": None, "usd": 3_072_946_000, "basis": "CY2024 return, same period; 'approximately 29,254 grants'",
     "url": GT.format("202503109349303645")},
    {"ein": "141782466", "sponsor": "Ayco Charitable Foundation", "fy": 2023, "tier": "form990_part_iii",
     "G": 32_400, "R": None, "usd": 251_751_000, "basis": "CY2023 return, same period; 'approximately 32,400 grants'",
     "url": GT.format("202413109349304401")},
    {"ein": "141782466", "sponsor": "Ayco Charitable Foundation", "fy": 2024, "tier": "form990_part_iii",
     "G": 35_675, "R": None, "usd": 301_786_000, "basis": "CY2024 return, same period; 'approximately 35,675 grants'",
     "url": GT.format("202543109349303959")},
    {"ein": "311709466", "sponsor": "T. Rowe Price Program for Charitable Giving", "fy": 2023, "tier": "form990_part_iii",
     "G": 29_000, "R": 11_000, "usd": None, "basis": "FY ended 2023-03-31 return; 'nearly 29,000 grants to over 11,000'",
     "url": GT.format("202321949349300147")},
    {"ein": "311709466", "sponsor": "T. Rowe Price Program for Charitable Giving", "fy": 2024, "tier": "form990_part_iii",
     "G": 32_000, "R": 13_000, "usd": None, "basis": "FY ended 2024-03-31 return; 'nearly 32,000 grants to over 13,000'",
     "url": GT.format("202401949349301515")},
    {"ein": "581344646", "sponsor": "Community Foundation for Greater Atlanta", "fy": 2023, "tier": "form990_part_iii",
     "G": 12_000, "R": 3_300, "usd": 187e6, "basis": "CY2023 return; '12,000 grants awarded to over 3,300 nonprofits' (all grants, not DAF only)",
     "url": GT.format("202540559349301329")},
    {"ein": "581344646", "sponsor": "Community Foundation for Greater Atlanta", "fy": 2024, "tier": "form990_part_iii",
     "G": 11_835, "R": 3_000, "usd": 173e6, "basis": "CY2024 return; '11,835 grants awarded to over 3,000 nonprofits' (all grants)",
     "url": GT.format("202523219349322912")},
    {"ein": "222281783", "sponsor": "Community Foundation of New Jersey", "fy": 2023, "tier": "form990_part_iii",
     "G": 8_000, "R": None, "usd": 100e6, "basis": "CY2023 return; '8,000 individual grants in 2023 totaling $100 million'",
     "url": GT.format("202423209349302727")},
    {"ein": "222281783", "sponsor": "Community Foundation of New Jersey", "fy": 2024, "tier": "form990_part_iii",
     "G": 8_340, "R": None, "usd": 124e6, "basis": "CY2024 return; '8,340 individual grants in 2024 totaling $124 million'",
     "url": GT.format("202543189349311964")},
    {"ein": "956111928", "sponsor": "Jewish Community Foundation of Los Angeles", "fy": 2024, "tier": "form990_part_iii",
     "G": 14_000, "R": 3_320, "usd": 207e6, "basis": "CY2024 return; '$207 million through 14,000 grants to 3,320 nonprofits'",
     "url": GT.format("202533199349302138")},
)
REPORT_EINS = frozenset({"110303001", "237825575", "232888152"})
USD_TOLERANCE = 0.20   # source dollars within 20% of Part IX lines 1-3, else the row is kept but left out of pools
# A published R is also checked: the unitemised recipients' mean must be <= $5,000 (Schedule I threshold)


# ----------------------------------------------------------------------------- recipient groups (pure)
def cats_of(flags: frozenset) -> frozenset:
    return frozenset(LINE_CAT.get(f, f) for f in flags) & frozenset(CATS)


def groups_of(lines: Sequence[tuple], sf: Mapping, part_ix: float, R: float | None) -> dict:
    """lines: (amount, cats) for itemised lines. Returns recipients as (amount, weight, cat-rate dict) groups."""
    pos = tuple((a, c) for a, c in lines if a > 0)
    nf = int(sf["f_recipients"]) or (1 if sf["f_usd"] > 0 else 0)
    f_amt = sf["f_usd"] / nf if nf else 0.0
    si_usd = sum(a for a, _ in pos)
    d_u = max(0.0, part_ix - si_usd - sf["f_usd"])
    r_u = max(0.0, (R or 0.0) - len(pos) - nf)
    small = tuple(c for a, c in pos if a <= SMALL_BAND)
    rate = lambda pool, c: (sum(1 for x in pool if c in x) / len(pool)) if pool else 0.0  # noqa: E731
    return {"itemised": pos, "nf": nf, "f_amt": f_amt, "d_u": d_u, "r_u": r_u,
            "u_amt": (d_u / r_u) if r_u else 0.0, "si_usd": si_usd, "n_zero": len(lines) - len(pos),
            "u_rates": {"none": {c: 0.0 for c in CATS},
                        "small_band": {c: rate(small, c) for c in CATS},
                        "all_itemised": {c: rate(tuple(c2 for _, c2 in pos), c) for c in CATS}},
            "n_small": len(small)}


def prepared(xs: Sequence[float]) -> tuple:
    s = tuple(sorted(xs))
    pre = (0.0,) + tuple(_accumulate(s))
    return (s, pre)


def _accumulate(s: Sequence[float]):
    tot = 0.0
    for x in s:
        tot += x
        yield tot


def floor_sum(prep: tuple, k: float) -> float:
    """sum over x of max(1, k * x) using the sorted powers and prefix sums."""
    s, pre = prep
    i = bisect.bisect_left(s, 1.0 / k)
    return i + k * (pre[-1] - pre[i])


def prepare(gr: Mapping, beta: float) -> dict:
    pw = tuple(a ** beta for a, _ in gr["itemised"])
    return {"all": prepared(pw),
            "cat": {c: prepared(tuple(x for x, (_, cs) in zip(pw, gr["itemised"]) if c in cs)) for c in CATS},
            "pw": pw}


def foreign_grants(gr: Mapping, k: float, beta: float, f_rule: str) -> float:
    if not gr["nf"]:
        return 0.0
    return gr["nf"] * (FOREIGN_GRANTS_PER_RECIPIENT if f_rule == "anchored" else max(1.0, k * gr["f_amt"] ** beta))


def unitemised_grants(gr: Mapping, k: float, beta: float) -> float:
    return gr["r_u"] * max(1.0, k * gr["u_amt"] ** beta) if gr["r_u"] and gr["u_amt"] > 0 else 0.0


def solve_k(gr: Mapping, prep: Mapping, G: float, beta: float, f_rule: str) -> tuple[float, bool]:
    """Bisection on log k so that total grants = G. Returns (k, feasible)."""
    total = lambda k: floor_sum(prep["all"], k) + foreign_grants(gr, k, beta, f_rule) + unitemised_grants(gr, k, beta)  # noqa: E731
    lo, hi = -80.0, 80.0
    if total(math.exp(lo)) > G:
        return math.exp(lo), False
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if total(math.exp(mid)) < G else (lo, mid)
    return math.exp((lo + hi) / 2), True


def per_grant(gr: Mapping, G: float, beta: float, f_rule: str, prep: Mapping | None = None) -> dict:
    """Grant counts by group and per-grant category shares under each unitemised rule."""
    prep = prep or prepare(gr, beta)
    k, ok = solve_k(gr, prep, G, beta, f_rule)
    n_it = floor_sum(prep["all"], k)
    n_f = foreign_grants(gr, k, beta, f_rule)
    n_u = unitemised_grants(gr, k, beta)
    total = n_it + n_f + n_u
    def shares(u_rule):
        u = gr["u_rates"][u_rule]
        return {c: (floor_sum(prep["cat"][c], k) + (n_f if c in ("foreign", "any", "any_core") else 0.0)
                    + n_u * u[c]) / total for c in CATS}
    m1m = sum(max(1.0, k * x) for (a, _), x in zip(gr["itemised"], prep["pw"]) if a / max(1.0, k * x) >= 1e6) + \
        (n_f if gr["nf"] and gr["f_amt"] * gr["nf"] / max(n_f, 1e-9) >= 1e6 else 0.0)
    return {"k": k, "feasible": ok, "total": total, "shares_by_u": {u: shares(u) for u in U_RULES},
            "n_itemised": n_it, "n_foreign": n_f, "n_unitemised": n_u, "grants_ge_1m": m1m,
            "avg_unitemised_grant": (gr["d_u"] / n_u) if n_u else None}


def line_and_dollar_shares(gr: Mapping) -> dict:
    """Recompute the proxy's recipient-line and dollar shares (reproduction check)."""
    lines = len(gr["itemised"]) + gr["nf"]
    usd = gr["si_usd"] + gr["f_amt"] * gr["nf"]
    def num(c):
        it = tuple(a for a, cs in gr["itemised"] if c in cs)
        add_f = c in ("foreign", "any", "any_core")
        return (len(it) + (gr["nf"] if add_f else 0), sum(it) + (gr["f_amt"] * gr["nf"] if add_f else 0.0))
    return {c: {"line_share": num(c)[0] / lines if lines else None, "usd_share": num(c)[1] / usd if usd else None}
            for c in CATS}


def ratio_bounds(rows: Sequence[Mapping], groups: Mapping) -> tuple[float, float]:
    rs = [r["R"] / (len(groups[(r["ein"], r["fy"])]["itemised"]) + groups[(r["ein"], r["fy"])]["nf"])
          for r in rows if r["R"] and (r["ein"], r["fy"]) in groups]
    return (min(rs), max(rs))


def with_R(gr_raw: Mapping, R: float) -> dict:
    """Rebuild the unitemised group for a given R (used for imputed R)."""
    nf, pos = gr_raw["nf"], gr_raw["itemised"]
    r_u = max(0.0, R - len(pos) - nf)
    return {**gr_raw, "r_u": r_u, "u_amt": (gr_raw["d_u"] / r_u) if r_u else 0.0}


# ----------------------------------------------------------------------------- rows (pure)
def out_row(scope, sponsor, ein, fy, tier, beta, u_rule, f_rule, r_case, metric, category, value, unit="", note=""):
    v = round(value, 8) if isinstance(value, float) and math.isfinite(value) else value
    return {"scope": scope, "sponsor": sponsor, "ein": ein, "fiscal_year": fy, "source_tier": tier, "beta": beta,
            "unitemised_rule": u_rule, "foreign_rule": f_rule, "r_case": r_case, "metric": metric,
            "category": category, "value": v, "unit": unit, "note": note}


def input_rows(c: Mapping, gr: Mapping, sy: Mapping, part_ix: float, r_case: str, R: float) -> list[dict]:
    base = ("sponsor_year", c["sponsor"], c["ein"], c["fy"], c["tier"], "", "", "", r_case)
    usd_ratio = (c["usd"] / part_ix) if c["usd"] and part_ix else None
    vals = (("published_grants_G", c["G"], "grants", c["basis"] + " | " + c["url"]),
            ("distinct_recipients_R", R, "recipients", "published" if r_case == "published" else "imputed [I]: R/(itemised+foreign) ratio bound"),
            ("source_grant_usd", c["usd"], "usd", ""),
            ("part_ix_total_grants_usd", part_ix, "usd", "Form 990 Part IX lines 1-3 (proxy CSV)"),
            ("source_usd_over_part_ix", usd_ratio, "ratio", f"pooled scopes require |ratio-1| <= {USD_TOLERANCE}"),
            ("schedule_i_lines_positive", float(len(gr["itemised"])), "lines", f"{gr['n_zero']} zero/negative lines excluded"),
            ("schedule_f_foreign_recipients", float(gr["nf"]), "recipients", ""),
            ("unitemised_recipients_R_U", gr["r_u"], "recipients", "R - itemised - foreign"),
            ("unitemised_usd_D_U", gr["d_u"], "usd", "Part IX lines 1-3 - Schedule I - line 3"),
            ("unitemised_mean_per_recipient", gr["u_amt"], "usd", "must be <= $5,000 for consistency"),
            ("tax_period_end", sy["tax_period_end"], "", sy["object_id"]))
    return [out_row(*base, m, "", v, u, n) for m, v, u, n in vals]


def share_rows(c, r_case, res_by, ls) -> list[dict]:
    out = []
    for (beta, u_rule, f_rule), res in res_by.items():
        base = ("sponsor_year", c["sponsor"], c["ein"], c["fy"], c["tier"], beta, u_rule, f_rule, r_case)
        out += [out_row(*base, "per_grant_share", cat, res["shares"][cat], "share of grants") for cat in CATS]
        if u_rule == "small_band" and f_rule == "model":
            out += [out_row(*base, "model_grants_itemised", "", res["n_itemised"], "grants"),
                    out_row(*base, "model_grants_unitemised", "", res["n_unitemised"], "grants"),
                    out_row(*base, "model_grants_foreign", "", res["n_foreign"], "grants"),
                    out_row(*base, "model_avg_unitemised_grant", "", res["avg_unitemised_grant"], "usd"),
                    out_row(*base, "model_grants_ge_1m", "", res["grants_ge_1m"], "grants",
                            "lines whose mean grant is >= $1m; compare Fidelity's published count"),
                    out_row(*base, "solver_feasible", "", float(res["feasible"]), "flag",
                            "0 = G below one grant per recipient")]
    base = ("sponsor_year", c["sponsor"], c["ein"], c["fy"], c["tier"], "", "", "", r_case)
    out += [out_row(*base, "recipient_line_share", cat, ls[cat]["line_share"], "share of lines",
                    "Schedule I lines + Schedule F recipients (proxy basis)") for cat in CATS]
    out += [out_row(*base, "itemised_dollar_share", cat, ls[cat]["usd_share"], "share of $",
                    "Schedule I + line 3 dollars (proxy basis)") for cat in CATS]
    return out


def pooled_rows(scope, members, results, totals) -> list[dict]:
    out = []
    keys = {k for m in members for k in results[m]}
    for key in sorted(keys, key=str):
        beta, u_rule, f_rule = key
        G = sum(totals[m] for m in members)
        for cat in CATS:
            num = sum(results[m][key]["shares"][cat] * totals[m] for m in members)
            out.append(out_row(scope, f"{len(members)} sponsor-years", "", "", "", beta, u_rule, f_rule, "published_or_low",
                               "per_grant_share", cat, num / G, "share of grants", "grant-weighted: sum flagged grants / sum G"))
    return out


# ----------------------------------------------------------------------------- loading (I/O)
def load_screened(a, eins: frozenset) -> dict:
    """Replicates mission_exception_load.main up to the line flags, for the given sponsors only."""
    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    present = {(e, fy): chosen[(e, fy)] for e in rank if e in eins for fy in FYS if (e, fy) in chosen}
    item = {k: x for k, x in present.items() if itemized(x)}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: xl.drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    groups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in groups.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    irc = {k: tuple(l[3] for l in v["lines"]) for k, v in good.items()}
    all_eins = frozenset(r["ein"] for rs in ann.values() for r in rs if r["ein"])
    bmf = load_bmf_ext(a.bmf_dir, all_eins)
    p78, _ = load_pub78(a.pub78, all_eins, frozenset())
    period = {k: dict(zip(("start", "end"), period_of(item[k]["tax_period_end"]))) for k in good}
    screened = {k: tuple(screen(r, irc[k][i], period[k], bmf, p78, {}, {}) for i, r in enumerate(ann[k])) for k in ann}
    flags = {k: tuple(xl.line_flags(r, period[k]["start"], period[k]["end"]) for r in rs) for k, rs in screened.items()}
    sf_rows = {(ein9(r["ein"]), int(r["fiscal_year"])): r for r in read_csv(xl.SCHED_F_CSV) if r["row_type"] == "sponsor_year"}
    return {k: {"lines": tuple((r["amount"], cats_of(f)) for r, f in zip(screened[k], flags[k])),
                "sf": xl.sched_f_of(sf_rows.get(k)), "oid": present[k]["oid"], "tpe": present[k]["tax_period_end"]}
            for k in good}


def write_rows(path: str, rows: Sequence[Mapping]) -> None:
    cols = ("scope", "sponsor", "ein", "fiscal_year", "source_tier", "beta", "unitemised_rule", "foreign_rule", "r_case",
            "metric", "category", "value", "unit", "note")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (accepted for the repo CLI convention; unused)")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--pub78", required=True)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    eins = frozenset(c["ein"] for c in GRANT_COUNTS)
    data = load_screened(a, eins)
    proxy = {(r["ein"], int(r["fiscal_year"])): r for r in read_csv(PROXY_CSV) if r["row_type"] == "sponsor_year"}
    counts = tuple(c for c in GRANT_COUNTS if (c["ein"], c["fy"]) in data)
    part_ix = {(c["ein"], c["fy"]): float(proxy[(c["ein"], c["fy"])]["part_ix_total_grants_usd"] or 0) for c in counts}
    raw = {(c["ein"], c["fy"]): groups_of(data[(c["ein"], c["fy"])]["lines"], data[(c["ein"], c["fy"])]["sf"],
                                          part_ix[(c["ein"], c["fy"])], c["R"]) for c in counts}
    r_lo, r_hi = ratio_bounds(counts, raw)
    cases = {(c["ein"], c["fy"]): ((("published", c["R"]),) if c["R"] else
                                   (("imputed_low", r_lo * (len(raw[(c["ein"], c["fy"])]["itemised"]) + raw[(c["ein"], c["fy"])]["nf"])),
                                    ("imputed_high", r_hi * (len(raw[(c["ein"], c["fy"])]["itemised"]) + raw[(c["ein"], c["fy"])]["nf"]))))
             for c in counts}
    rows = [out_row("meta", "", "", "", "", "", "", "", "", "R_over_listed_ratio_bounds", "", f"{r_lo:.4f}/{r_hi:.4f}",
                    "ratio", "min/max of published R / (Schedule I lines + Schedule F recipients); used to impute R [I]")]
    results, totals, usd_ok = {}, {}, {}
    for c in counts:
        k = (c["ein"], c["fy"])
        sy = proxy[k]
        ls = line_and_dollar_shares(raw[k])
        # reproduction check against the proxy CSV (line shares of the core and broad unions)
        for cat in ("any", "any_core"):
            rows.append(out_row("sponsor_year", c["sponsor"], c["ein"], c["fy"], c["tier"], "", "", "", "",
                                "check_line_share_minus_proxy", cat,
                                (ls[cat]["line_share"] or 0) - float(sy[f"{cat}_count_share"] or 0), "share",
                                "0 = reproduces exception-load-proxy-2026-11-19.csv"))
        for r_case, R in cases[k]:
            gr = with_R(raw[k], R)
            preps = {b: prepare(gr, b) for b in set(BETAS) | set(BETA_FINE)}
            solved = {(b, f): per_grant(gr, c["G"], b, f, preps[b]) for b in BETAS for f in F_RULES}
            res = {(b, u, f): {**solved[(b, f)], "shares": solved[(b, f)]["shares_by_u"][u]}
                   for b in BETAS for u in U_RULES for f in F_RULES}
            rows += input_rows(c, gr, sy, part_ix[k], r_case, R) + share_rows(c, r_case, res, ls)
            fine = {b: (lambda r: {**r, "shares": r["shares_by_u"]["small_band"]})(per_grant(gr, c["G"], b, "model", preps[b]))
                    for b in BETA_FINE}
            rows += [out_row("sponsor_year", c["sponsor"], c["ein"], c["fy"], c["tier"], b, "small_band", "model", r_case,
                             m, cat, val, unit)
                     for b, r in fine.items()
                     for m, cat, val, unit in (("per_grant_share_fine", "any_core", r["shares"]["any_core"], "share of grants"),
                                               ("per_grant_share_fine", "foreign", r["shares"]["foreign"], "share of grants"),
                                               ("model_grants_ge_1m_fine", "", r["grants_ge_1m"], "grants"))]
            if r_case in ("published", "imputed_low"):
                results[k], totals[k] = res, c["G"]
        if c.get("m1m"):
            rows.append(out_row("sponsor_year", c["sponsor"], c["ein"], c["fy"], c["tier"], "", "", "", "",
                                "published_grants_ge_1m", "", c["m1m"], "grants", "Fidelity Giving Reports; FY = mean of CYs"))
        if c.get("intl_grants"):
            rows.append(out_row("sponsor_year", c["sponsor"], c["ein"], c["fy"], c["tier"], "", "", "", "",
                                "published_international_grant_share", "foreign", c["intl_grants"] / c["G"],
                                "share of grants", f"{c['intl_grants']} international grants / {c['G']:,} (NPT annual report chart)"))
        ratio = (c["usd"] / part_ix[k]) if c["usd"] and part_ix[k] else None
        u_ok = not c["R"] or (raw[k]["u_amt"] <= 5_000.0 and raw[k]["d_u"] > 0)
        usd_ok[k] = (ratio is None or abs(ratio - 1) <= USD_TOLERANCE) and u_ok
        rows.append(out_row("sponsor_year", c["sponsor"], c["ein"], c["fy"], c["tier"], "", "", "", "", "pool_eligible", "",
                            float(usd_ok[k]), "flag", f"needs |source $/Part IX - 1| <= {USD_TOLERANCE} and, where R is "
                            "published, unitemised dollars > 0 with a mean <= $5,000 per unitemised recipient"))
    keep = tuple(k for k in results if usd_ok[k])
    scopes = (("pooled_all_usd_consistent", keep),
              ("pooled_annual_report_sponsors", tuple(k for k in keep if k[0] in REPORT_EINS)),
              ("pooled_990_narrative_sponsors", tuple(k for k in keep if k[0] not in REPORT_EINS)),
              ("pooled_ex_fidelity", tuple(k for k in keep if k[0] != "110303001")))
    for scope, members in scopes:
        if members:
            rows += pooled_rows(scope, members, results, totals)
            rows.append(out_row(scope, "members", "", "", "", "", "", "", "", "members", "",
                                ";".join(f"{e}:{fy}" for e, fy in members), "", ""))
    write_rows(a.out, rows)
    print(f"sponsor-years with counts and lines: {len(counts)}; pooled (usd-consistent): {len(keep)}; "
          f"excluded (dollar or unitemised check): {sorted(k for k in results if not usd_ok[k])}; R ratio bounds {r_lo:.3f}-{r_hi:.3f}")
    for scope, members in scopes:
        for key in ((0.0, "small_band", "model"), (0.5, "small_band", "model"), (1.0, "small_band", "model"),
                    (0.5, "small_band", "anchored")):
            G = sum(totals[m] for m in members) or 1
            core = sum(results[m][key]["shares"]["any_core"] * totals[m] for m in members) / G
            broad = sum(results[m][key]["shares"]["any"] * totals[m] for m in members) / G
            print(f"  {scope:<32} beta={key[0]:<4} {key[2]:<8} core={core:.4f} broad={broad:.4f}")
    print(f"wrote {len(rows)} rows -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
