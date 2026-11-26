#!/usr/bin/env python3
"""AI-economics scenario model v2: observed-cost anchors, elasticity scaling, Monte Carlo over unsourced parameters.

Queue item P-COST-06 (with P-COST-01/-02 context). Rebuilds the 16-process model of
research/mission-2026-11-14/ai-economics-replacement-analysis.md (v1) so that:
  (a) cost pools are anchored to observed Form 990 Part IX operating cost by sponsor archetype;
  (b) scaling between sponsor sizes uses observed log-log cost elasticities, not linear grant scaling;
  (c) the unsourced parameters (AI-amenability a, redesign share d, QA rate q, AI time saving s, plus the other
      v1 assumptions: manual saving alpha, conventional factor beta and rules-amenability b, process-labour share phi,
      touch rates and minutes, fixed costs) are drawn from stated distributions with random.Random(42);
  (d) per-process fixed costs are compared with observed median IT spend (Part IX line 14) by archetype;
  (e) outputs: probability that each intervention ranks first per process and archetype, net-value distributions,
      ranking sensitivity by parameter tercile, and break-even sponsor count for a shared vendor AI platform.

Every number that is not read from an input file is an ASSUMPTION and is listed in ASSUMPTIONS below.
Stdlib only; functional style (pure functions; I/O only in load_* / write_* / main).

Inputs (read only):
  data/mission-2026-11-14/ai-process-economics.csv          v1 process parameters (scenario values)
  data/mission-2026-11-14/sponsor-cost-structure.csv        FY2024 Part IX rows by sponsor (observed)
  data/mission-2026-11-14/sponsor-cost-structure-summary.csv grant-count anchors (observed counts / 990 cost)
Output:
  data/mission-2026-11-14/ai-economics-v2-results.csv       long-format results (record_type, metric, value, basis)

Usage:
  python3 scripts/mission_ai_economics_v2.py [--draws 10000]
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import random
import statistics
import sys
from typing import Callable, Iterable, Mapping, Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "mission-2026-11-14")
V1_CSV = os.path.join(DATA, "ai-process-economics.csv")
COST_CSV = os.path.join(DATA, "sponsor-cost-structure.csv")
SUMMARY_CSV = os.path.join(DATA, "sponsor-cost-structure-summary.csv")
OUT_CSV = os.path.join(DATA, "ai-economics-v2-results.csv")

SEED = 42
FY = "2024"
INTERVENTIONS = ("A", "B", "C", "D")
SPONSOR_PROCS = tuple(f"P{i:02d}" for i in range(1, 16))  # P16 is recipient-side
COORDINATION_PROCS = frozenset({"P07", "P09", "P10", "P16"})  # v1 §3: redesign needs counterparties
PRICE_IN, PRICE_OUT, LOOP = 2.0, 10.0, 3.0  # Sonnet 5.5 list $/M tokens (v1, Anthropic pricing page) x v1 loop multiplier

# ---------------------------------------------------------------------------------------------- assumptions
# (name, distribution, parameters, applies_to, why) -- every entry is unsourced unless the 'why' says observed.
ASSUMPTIONS = (
    ("s", "triangular", (0.15, 0.40, 0.70), "global per draw", "AI handling-time saving; v1 pess/base/opt 0.20/0.40/0.60 widened"),
    ("q", "triangular", (0.03, 0.10, 0.30), "global per draw", "QA re-review share of touched cases at half minutes; v1 0.05/0.10/0.25 widened"),
    ("a_p", "triangular", ("0.5*a_v1", "a_v1", "min(0.9,a_v1+0.35)"), "per process", "right-skewed to remove v1 cap at 0.45 (red-team #1)"),
    ("d_p", "triangular", ("0.3*d_v1", "d_v1", "min(0.95,d_v1+0.10)"), "per process", "left-skewed: v1 assumed counterparties adopt"),
    ("adoption", "uniform", (0.3, 1.0), "multiplies d_p for P07,P09,P10,P16", "cross-institution redesign needs counterparties"),
    ("alpha", "uniform", (0.05, 0.25), "global per draw", "manual-improvement saving; v1 fixed 0.15"),
    ("beta", "uniform", (0.30, 0.70), "global per draw", "conventional-automation efficiency; v1 fixed 0.50"),
    ("b_p", "triangular", ("0.7*b_v1", "b_v1", "min(0.95,1.2*b_v1)"), "per process", "rules-amenability around v1"),
    ("e_p,m_p", "triangular", ("low", "base", "high"), "per process", "v1 touch-rate and minutes ranges; set process MIX only in v2"),
    ("phi", "triangular", (0.05, 0.15, 0.35), "global per draw", "share of DAF labour+outsourced-admin cost that is handling in P01-P15; v1 base implies ~0.08-0.15"),
    ("F_A", "loguniform", (25e3, 100e3), "per process project / yr", "v1 §4.4 range"),
    ("F_B", "loguniform", (100e3, 500e3), "per process project / yr", "v1 §4.4 range"),
    ("F_C", "loguniform", (150e3, 750e3), "per process project / yr", "v1 §4.4 range"),
    ("F_D", "loguniform", (200e3, 2e6), "per process project / yr", "v1 §4.4 range"),
    ("avg_grant_usd", "loguniform", (5e3, 40e3), "non-NAT_LARGE archetypes", "range of observed anchors: Fidelity ~$5.1k, DAFgiving360 ~$5.5k, Vanguard ~$11.4k, NPT ~$40k (Schedule D grants / self-reported count)"),
    ("eps_nat", "uniform", (0.41, 0.48), "national scaling", "OBSERVED range FY2022-24 opex~DAF assets (cost-structure §4.6); applied to grants as proxy"),
    ("eps_cf", "uniform", (0.84, 0.86), "community scaling", "OBSERVED range FY2022-24 opex~total assets (cost-structure §4.6)"),
    ("eps_it", "fixed", (0.44, 0.83), "IT scaling nat / cf", "OBSERVED FY2024 IT~assets elasticities"),
    ("alloc_basis", "coin", ("A", "G"), "community archetypes", "DAF share of assets vs of grants, both OBSERVED per row"),
    ("F_platform", "loguniform", (1.5e6, 6e6), "vendor platform / yr", "multi-process AI platform incl. evaluation, model-risk, security; ~10x v1 per-process C low end to 8x mid"),
    ("f_sponsor", "loguniform", (10e3, 100e3), "vendor per-sponsor / yr", "integration, onboarding, support"),
    ("tau", "uniform", (0.20, 0.50), "vendor", "share of sponsor gross AI value the vendor can charge"),
)

# Archetypes: observed window of FY2024 sponsors to bootstrap from, and the scale to move them to.
ARCHETYPES = (
    {"id": "NAT_LARGE", "label": "National, ~1-3m grants/yr", "category": "National-Standard",
     "mode": "grant_anchor", "grants": (1e6, 3e6), "eps": "eps_nat", "eps_it": 0.44,
     "it_window": (1e10, 1e13)},
    {"id": "NAT_MID", "label": "National, $1-10bn DAF assets", "category": "National-Standard",
     "mode": "window_asis", "window": (1e9, 1e10), "eps": "eps_nat", "eps_it": 0.44},
    {"id": "CF_1BN", "label": "Community foundation, $1bn DAF assets", "category": "Community",
     "mode": "window_scaled", "window": (5e8, 2e9), "target": 1e9, "eps": "eps_cf", "eps_it": 0.83},
    {"id": "CF_250M", "label": "Community foundation, $250m DAF assets", "category": "Community",
     "mode": "window_scaled", "window": (1.25e8, 5e8), "target": 2.5e8, "eps": "eps_cf", "eps_it": 0.83},
    {"id": "CF_SMALL", "label": "Community foundation, $10-100m DAF assets", "category": "Community",
     "mode": "window_asis", "window": (1e7, 1e8), "eps": "eps_cf", "eps_it": 0.83},
    {"id": "REF_V1_1M", "label": "v1 reference: 1m grants, bottom-up pools, linear (comparison only)",
     "category": None, "mode": "v1_reference", "grants": (1e6, 1e6), "eps": "eps_nat", "eps_it": 0.44},
)

# Grant-count anchors used for NAT_LARGE (observed): name fragment -> (count, count source)
GRANT_ANCHOR_NAMES = ("Fidelity", "DAFgiving360")


# ---------------------------------------------------------------------------------------------- pure helpers
def fnum(v) -> float | None:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def tri(u: float, lo: float, mode: float, hi: float) -> float:
    """Inverse CDF of a triangular distribution (u in [0,1))."""
    if hi <= lo:
        return lo
    c = (mode - lo) / (hi - lo)
    return lo + math.sqrt(u * (hi - lo) * (mode - lo)) if u < c else hi - math.sqrt((1 - u) * (hi - lo) * (hi - mode))


def logu(u: float, lo: float, hi: float) -> float:
    return math.exp(math.log(lo) + u * (math.log(hi) - math.log(lo)))


def uni(u: float, lo: float, hi: float) -> float:
    return lo + u * (hi - lo)


def quantile(xs: Sequence[float], q: float) -> float | None:
    s = sorted(x for x in xs if x is not None and math.isfinite(x))
    if not s:
        return None
    pos = q * (len(s) - 1)
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def median(xs: Iterable[float]) -> float | None:
    s = [x for x in xs if x is not None]
    return statistics.median(s) if s else None


def mean(xs: Sequence[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def argmax(d: Mapping[str, float]) -> str:
    return max(d.items(), key=lambda kv: kv[1])[0]


def cost_per_case(tin: float, tout: float) -> float:
    return (tin * PRICE_IN + tout * PRICE_OUT) / 1e6 * LOOP


# ---------------------------------------------------------------------------------------------- loading
def load_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


def v1_process(r: Mapping) -> dict:
    keys = ("scenario_volume_base", "touch_rate_low", "touch_rate_base", "touch_rate_high", "minutes_low",
            "minutes_base", "minutes_high", "loaded_rate_usd_hr", "rules_amenability", "ai_amenability",
            "redesign_elimination_share", "inference_tokens_in", "inference_tokens_out",
            "inference_cost_per_case_usd", "inference_cost_annual_base_usd", "labor_pool_base_usd",
            "gross_A_base_usd", "gross_B_base_usd", "gross_C_base_usd", "gross_D_base_usd")
    p = {k: fnum(r[k]) for k in keys}
    touched = p["scenario_volume_base"] * p["touch_rate_base"]
    # inference basis in v1: share of volume run through the model (all cases or touched cases only)
    p["inference_basis"] = p["inference_cost_annual_base_usd"] / (p["inference_cost_per_case_usd"] * p["scenario_volume_base"])
    p["touched_base"] = touched
    return {"id": r["process_id"], "name": r["process"], "rank_base": r["rank_base"], **p}


def analysable(r: Mapping) -> bool:
    flags = r["quality_flags"].split(";")
    return not any(f in flags for f in ("tfe_missing", "opex_nonpositive", "givinga_undefined_account_unit"))


def sponsor_record(r: Mapping) -> dict:
    opex = fnum(r["operating_cost_ex_invest_mgmt"]) or 0.0
    staff = fnum(r["staff_share_of_opex"]) or 0.0
    outside = fnum(r["outside_ex_invest_share_of_opex"]) or 0.0
    return {"ein": r["ein"], "name": r["sponsor_name"], "category": r["category"], "fy": r["fiscal_year"],
            "opex": opex, "it": fnum(r["it_l14"]), "daf_assets": fnum(r["daf_assets_eoy"]),
            "daf_grants": fnum(r["daf_grants"]), "share_a": fnum(r["daf_share_of_total_assets"]),
            "share_g": fnum(r["daf_share_of_grants"]), "labour_share": min(1.0, staff + outside),
            "employees": fnum(r["employees"])}


def load_sponsors(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    return tuple(sponsor_record(r) for r in rows if analysable(r) and (fnum(r["operating_cost_ex_invest_mgmt"]) or 0) > 0)


def grant_anchors(sponsors: Sequence[Mapping], summary: Sequence[Mapping]) -> tuple[dict, ...]:
    """Observed self-reported grant counts matched to 990 cost (summary dimension=grant_count_anchor)."""
    rows = [r for r in summary if r["dimension"] == "grant_count_anchor"]
    out = []
    for frag in GRANT_ANCHOR_NAMES:
        hit = [r for r in rows if frag.lower() in r["note"].lower()]
        if not hit:
            continue
        r = hit[0]
        opex, grants = fnum(r["numerator_sum"]), fnum(r["denominator_sum"])
        ein = r["note"].split("(")[1].split(")")[0]
        match = [s for s in sponsors if s["ein"] == ein and s["fy"] == r["fiscal_year"]]
        lab = match[0]["labour_share"] if match else None
        it = match[0]["it"] if match else None
        out.append({"name": frag, "ein": ein, "fy": r["fiscal_year"], "opex": opex, "grants": grants,
                    "labour_share": lab, "it": it, "daf_grants": match[0]["daf_grants"] if match else None,
                    "note": r["note"]})
    return tuple(out)


# ---------------------------------------------------------------------------------------------- archetype anchors
def window_rows(sponsors: Sequence[Mapping], cat: str, lo: float, hi: float) -> tuple[dict, ...]:
    return tuple(s for s in sponsors if s["fy"] == FY and s["category"] == cat and s["daf_assets"]
                 and lo <= s["daf_assets"] < hi)


def archetype_anchor(a: Mapping, sponsors: Sequence[Mapping], anchors: Sequence[Mapping]) -> dict:
    if a["mode"] == "v1_reference":
        return {"rows": (), "n": 0, "it_med_pos": None, "it_med_all": None, "assets_med": None, "available_n": None}
    if a["mode"] == "grant_anchor":
        it_rows = window_rows(sponsors, a["category"], *a["it_window"])
        return {"rows": tuple(anchors), "n": len(anchors),
                "it_med_pos": median(s["it"] for s in it_rows if (s["it"] or 0) > 0),
                "it_med_all": median((s["it"] or 0.0) for s in it_rows),
                "assets_med": median(s["daf_assets"] for s in it_rows), "available_n": len(it_rows)}
    rows = window_rows(sponsors, a["category"], *a["window"])
    return {"rows": rows, "n": len(rows),
            "it_med_pos": median(s["it"] for s in rows if (s["it"] or 0) > 0),
            "it_med_all": median((s["it"] or 0.0) for s in rows),
            "assets_med": median(s["daf_assets"] for s in rows), "available_n": len(rows)}


# ---------------------------------------------------------------------------------------------- draws
def draw_params(rng: random.Random, procs: Sequence[Mapping]) -> dict:
    """One Monte Carlo draw of all unsourced parameters. Uniforms kept (u_*) for tercile sensitivity."""
    u = {k: rng.random() for k in ("s", "q", "alpha", "beta", "phi", "eps_nat", "eps_cf", "F_platform",
                                   "f_sponsor", "tau", "avg_grant")}
    g = {"s": tri(u["s"], 0.15, 0.40, 0.70), "q": tri(u["q"], 0.03, 0.10, 0.30),
         "alpha": uni(u["alpha"], 0.05, 0.25), "beta": uni(u["beta"], 0.30, 0.70),
         "phi": tri(u["phi"], 0.05, 0.15, 0.35), "eps_nat": uni(u["eps_nat"], 0.41, 0.48),
         "eps_cf": uni(u["eps_cf"], 0.84, 0.86), "F_platform": logu(u["F_platform"], 1.5e6, 6e6),
         "f_sponsor": logu(u["f_sponsor"], 10e3, 100e3), "tau": uni(u["tau"], 0.20, 0.50),
         "avg_grant": logu(u["avg_grant"], 5e3, 40e3)}
    per = {}
    for p in procs:
        uu = {k: rng.random() for k in ("a", "d", "adopt", "b", "e", "m", "FA", "FB", "FC", "FD")}
        a1, d1, b1 = p["ai_amenability"], p["redesign_elimination_share"], p["rules_amenability"]
        d = tri(uu["d"], 0.3 * d1, d1, min(0.95, d1 + 0.10))
        if p["id"] in COORDINATION_PROCS:
            d *= uni(uu["adopt"], 0.3, 1.0)
        per[p["id"]] = {
            "a": tri(uu["a"], 0.5 * a1, a1, min(0.9, a1 + 0.35)), "d": d,
            "b": tri(uu["b"], 0.7 * b1, b1, min(0.95, 1.2 * b1)),
            "e": tri(uu["e"], p["touch_rate_low"], p["touch_rate_base"], p["touch_rate_high"]),
            "m": tri(uu["m"], p["minutes_low"], p["minutes_base"], p["minutes_high"]),
            "F": {"A": logu(uu["FA"], 25e3, 100e3), "B": logu(uu["FB"], 100e3, 500e3),
                  "C": logu(uu["FC"], 150e3, 750e3), "D": logu(uu["FD"], 200e3, 2e6)},
            "u_a": uu["a"], "u_d": uu["d"], "u_FC": uu["FC"]}
    return {**g, "u": u, "per": per}


def draw_sponsor(rng: random.Random, a: Mapping, anchor: Mapping, g: Mapping) -> dict:
    """Bootstrap an observed sponsor from the archetype window and scale it to the archetype by elasticity."""
    eps = g[a["eps"]]
    if a["mode"] == "v1_reference":
        return {"grants": 1e6, "opex_daf": None, "labour_share": None, "it": None, "scale": 1.0, "src": "v1"}
    if a["mode"] == "grant_anchor":
        s = anchor["rows"][rng.randrange(len(anchor["rows"]))]
        grants = logu(rng.random(), *a["grants"])
        k = (grants / s["grants"]) ** eps
        # IT denominator: median line 14 (IT>0) of nationals >$10bn, unscaled (same population as the anchors)
        return {"grants": grants, "opex_daf": s["opex"] * k, "labour_share": s["labour_share"],
                "it": anchor["it_med_pos"] or 0.0, "scale": k, "src": s["name"]}
    s = anchor["rows"][rng.randrange(len(anchor["rows"]))]
    target = a["target"] if a["mode"] == "window_scaled" else s["daf_assets"]
    ratio = target / s["daf_assets"]
    k = ratio ** eps
    if a["category"] == "Community":
        basis = "A" if rng.random() < 0.5 else "G"
        share = (s["share_a"] if basis == "A" else s["share_g"])
        share = share if share is not None else (s["share_a"] or 0.0)
    else:
        share = s["share_a"] if s["share_a"] is not None else 1.0
    daf_grants_usd = (s["daf_grants"] or 0.0) * ratio  # grant dollars ~ assets (payout ratio held)
    grants = max(1.0, daf_grants_usd / g["avg_grant"])
    it_med_scaled = (anchor["it_med_pos"] or 0.0) * ((target / anchor["assets_med"]) ** a["eps_it"]
                                                    if a["mode"] == "window_scaled" else 1.0)
    return {"grants": grants, "opex_daf": s["opex"] * k * share, "labour_share": s["labour_share"],
            "it": it_med_scaled, "scale": k, "src": s["ein"]}


# ---------------------------------------------------------------------------------------------- model
def raw_pool(p: Mapping, e: float, m: float) -> float:
    """v1 bottom-up labour pool at v1 volume (1m grants)."""
    return p["scenario_volume_base"] * e * m / 60.0 * p["loaded_rate_usd_hr"]


def process_pools(procs: Sequence[Mapping], g: Mapping, sp: Mapping, mode: str) -> dict[str, float]:
    raws = {p["id"]: raw_pool(p, g["per"][p["id"]]["e"], g["per"][p["id"]]["m"]) for p in procs}
    grant_ratio = sp["grants"] / 1e6
    p16 = raws.get("P16", 0.0) * grant_ratio  # recipient-side: linear, no observed anchor
    if mode == "v1_reference":
        return {k: v * grant_ratio for k, v in raws.items()}
    total = sp["opex_daf"] * sp["labour_share"] * g["phi"]
    denom = sum(raws[k] for k in SPONSOR_PROCS)
    pools = {k: total * raws[k] / denom for k in SPONSOR_PROCS}
    return {**pools, "P16": p16}


def gross_values(p: Mapping, pp: Mapping, g: Mapping, L: float, grants: float) -> dict[str, float]:
    cases = p["scenario_volume_base"] * grants / 1e6 * p["inference_basis"]
    inf = cases * cost_per_case(p["inference_tokens_in"], p["inference_tokens_out"])
    return {"A": g["alpha"] * L, "B": g["beta"] * pp["b"] * L,
            "C": g["s"] * pp["a"] * L - 0.5 * g["q"] * L - inf, "D": pp["d"] * L, "_inf": inf,
            "C_after_D": (g["s"] * pp["a"] - 0.5 * g["q"]) * (1 - pp["d"]) * L - inf * (1 - pp["d"])}


def evaluate_draw(procs: Sequence[Mapping], g: Mapping, sp: Mapping, mode: str) -> dict:
    pools = process_pools(procs, g, sp, mode)
    res = {}
    for p in procs:
        pp = g["per"][p["id"]]
        L = pools[p["id"]]
        gv = gross_values(p, pp, g, L, sp["grants"])
        net = {i: gv[i] - pp["F"][i] for i in INTERVENTIONS}
        first_net = argmax({**net, "none": 0.0})
        first_gross = argmax({i: gv[i] for i in INTERVENTIONS})
        res[p["id"]] = {"L": L, "gross": gv, "net": net, "first_net": first_net, "first_gross": first_gross,
                        "fc_over_it": {i: (pp["F"][i] / sp["it"]) if sp.get("it") else None for i in INTERVENTIONS}}
    ai_wf = sum(max(0.0, res[k]["gross"]["C"]) for k in SPONSOR_PROCS)
    ai_ad = sum(max(0.0, res[k]["gross"]["C_after_D"]) for k in SPONSOR_PROCS)
    return {"proc": res, "pool_sponsor": sum(pools[k] for k in SPONSOR_PROCS), "ai_value_wf": ai_wf,
            "ai_value_after_d": ai_ad, "inference_total": sum(res[k]["gross"]["_inf"] for k in SPONSOR_PROCS),
            "grants": sp["grants"], "it": sp.get("it"), "opex_daf": sp.get("opex_daf")}


def breakeven_n(value: float, fee_share: float, F: float, f: float) -> float:
    margin = fee_share * value - f
    return math.ceil(F / margin) if margin > 0 else math.inf


def simulate(a: Mapping, idx: int, procs: Sequence[Mapping], anchor: Mapping, draws: int) -> tuple[tuple[dict, dict], ...]:
    prng = random.Random(SEED)                 # common random numbers: same parameter draws in every archetype
    srng = random.Random(SEED * 1000 + idx)    # sponsor bootstrap stream, archetype-specific
    out = []
    for _ in range(draws):
        g = draw_params(prng, procs)
        sp = draw_sponsor(srng, a, anchor, g)
        out.append((g, evaluate_draw(procs, g, sp, a["mode"])))
    return tuple(out)


# ---------------------------------------------------------------------------------------------- summarising
def row(rt, arch, metric, value, unit="", basis="", process_id="", process="", intervention="", parameter="",
        bucket="", note="") -> dict:
    return {"record_type": rt, "archetype": arch, "process_id": process_id, "process": process,
            "intervention": intervention, "parameter": parameter, "bucket": bucket, "metric": metric,
            "value": (round(value, 6) if isinstance(value, float) and math.isfinite(value) else value),
            "unit": unit, "basis": basis, "note": note}


def dist_rows(rt, arch, name, xs, unit, basis, **kw) -> list[dict]:
    return [row(rt, arch, f"{name}_{lab}", quantile(xs, q), unit, basis, **kw)
            for lab, q in (("p05", .05), ("p25", .25), ("p50", .5), ("p75", .75), ("p95", .95))] + \
           [row(rt, arch, f"{name}_mean", mean(xs), unit, basis, **kw)]


def anchor_rows(a: Mapping, anchor: Mapping, sims, procs) -> list[dict]:
    aid = a["id"]
    v1_per_grant = sum(p["labor_pool_base_usd"] for p in procs if p["id"] in SPONSOR_PROCS) / 1e6
    grants = [s["grants"] for _, s in sims]
    pools = [s["pool_sponsor"] for _, s in sims]
    per_grant = [s["pool_sponsor"] / s["grants"] for _, s in sims]
    g_med = quantile(grants, .5)
    eps = 0.84 if a["category"] == "Community" else 0.445
    out = [row("archetype_anchor", aid, "label", a["label"], basis="definition"),
           row("archetype_anchor", aid, "window_sponsors_fy2024", anchor["n"], "count", "observed",
               note="FY2024 analysable Part IX rows in the archetype window (sponsor-cost-structure.csv)"),
           row("archetype_anchor", aid, "it_median_positive", anchor["it_med_pos"], "usd/yr", "observed",
               note="median Part IX line 14 among window rows with IT>0"),
           row("archetype_anchor", aid, "it_median_incl_zero", anchor["it_med_all"], "usd/yr", "observed"),
           row("archetype_anchor", aid, "daf_assets_median_window", anchor["assets_med"], "usd", "observed")]
    if a["mode"] != "v1_reference":
        out += dist_rows("archetype_anchor", aid, "daf_opex_scaled", [s["opex_daf"] for _, s in sims], "usd/yr",
                         "observed x elasticity (allocation basis randomised for CF)")
        out += dist_rows("archetype_anchor", aid, "it_hurdle_denominator", [s["it"] for _, s in sims], "usd/yr",
                         "observed median x IT elasticity")
    out += dist_rows("archetype_anchor", aid, "grants_per_year", grants, "grants",
                     "observed (NAT_LARGE) / observed DAF grant $ / assumed avg grant size")
    out += dist_rows("archetype_anchor", aid, "sponsor_pool_P01_P15", pools, "usd/yr",
                     "observed opex x observed labour share x assumed phi x assumed mix")
    out += dist_rows("archetype_anchor", aid, "sponsor_pool_per_grant", per_grant, "usd/grant", "computed")
    out += [row("archetype_anchor", aid, "v1_linear_pool_at_median_grants", v1_per_grant * g_med, "usd/yr",
                "v1 assumption", note="v1 base $4.32/grant x median grants (linear)"),
            row("archetype_anchor", aid, "v1_elasticity_pool_at_median_grants",
                v1_per_grant * 1e6 * (g_med / 1e6) ** eps, "usd/yr", "v1 assumption x observed elasticity",
                note=f"v1 $4.32m at 1m grants x (grants/1m)^{eps}"),
            row("archetype_anchor", aid, "inference_share_of_pool_p50",
                quantile([s["inference_total"] / s["pool_sponsor"] for _, s in sims if s["pool_sponsor"] > 0], .5),
                "ratio", "computed"),
            row("archetype_anchor", aid, "available_sponsors_fy2024", anchor["available_n"], "count", "observed",
                note="sponsors in window (NAT_LARGE: nationals >$10bn)")]
    return out


def process_rows(a: Mapping, sims, procs) -> list[dict]:
    aid, out, n = a["id"], [], len(sims)
    for p in procs:
        pid, pname = p["id"], p["name"]
        side = "recipient-side, linear, no observed anchor" if pid == "P16" else ""
        res = [s["proc"][pid] for _, s in sims]
        kw = {"process_id": pid, "process": pname}
        out.append(row("process_intervention", aid, "pool_p50", quantile([r["L"] for r in res], .5), "usd/yr",
                       "anchored pool (see archetype_anchor)", note=side, **kw))
        out.append(row("process_intervention", aid, "v1_rank_base", p["rank_base"], "", "v1 assumption", **kw))
        winners_net = [r["first_net"] for r in res]
        winners_gross = [r["first_gross"] for r in res]
        for i in INTERVENTIONS:
            kwi = {**kw, "intervention": i}
            nets = [r["net"][i] for r in res]
            gross = [r["gross"][i] for r in res]
            out.append(row("process_intervention", aid, "p_rank_first_net", winners_net.count(i) / n, "prob",
                           "assumption-driven", note="incl. 'none' option at 0", **kwi))
            out.append(row("process_intervention", aid, "p_rank_first_gross", winners_gross.count(i) / n, "prob",
                           "assumption-driven", note="before fixed costs", **kwi))
            out.append(row("process_intervention", aid, "p_net_positive", sum(x > 0 for x in nets) / n, "prob",
                           "assumption-driven", **kwi))
            out += dist_rows("process_intervention", aid, "net_value", nets, "usd/yr", "assumption-driven", **kwi)
            out.append(row("process_intervention", aid, "gross_p50", quantile(gross, .5), "usd/yr",
                           "assumption-driven", **kwi))
            fcs = [r["fc_over_it"][i] for r in res if r["fc_over_it"][i] is not None]
            if fcs:
                out.append(row("process_intervention", aid, "fixed_cost_over_it_median_p50", quantile(fcs, .5),
                               "ratio", "assumed fixed cost / observed IT median", **kwi))
                out.append(row("process_intervention", aid, "p_fixed_cost_gt_it_median",
                               sum(x > 1 for x in fcs) / len(fcs), "prob", "assumed fixed cost / observed IT median", **kwi))
            out.append(row("process_intervention", aid, "v1_gross_base_1m", p[f"gross_{i}_base_usd"], "usd/yr",
                           "v1 assumption", **kwi))
            out.append(row("process_intervention", aid, "p_rank_last_gross",
                           sum(min(r["gross"], key=lambda k: r["gross"][k] if k in INTERVENTIONS else math.inf) == i
                               for r in res) / n, "prob", "assumption-driven", **kwi))
        out.append(row("process_intervention", aid, "p_C_beats_B_gross",
                       sum(r["gross"]["C"] > r["gross"]["B"] for r in res) / n, "prob", "assumption-driven",
                       **{**kw, "intervention": "C"}))
        out.append(row("process_intervention", aid, "p_rank_first_net", winners_net.count("none") / n, "prob",
                       "assumption-driven", note="no intervention clears its fixed cost",
                       **{**kw, "intervention": "none"}))
    return out


PARAM_GETTERS: dict[str, Callable] = {
    "s": lambda g, pid: g["u"]["s"], "q": lambda g, pid: g["u"]["q"], "alpha": lambda g, pid: g["u"]["alpha"],
    "beta": lambda g, pid: g["u"]["beta"], "phi": lambda g, pid: g["u"]["phi"],
    "a_p": lambda g, pid: g["per"][pid]["u_a"], "d_p": lambda g, pid: g["per"][pid]["u_d"],
    "F_C": lambda g, pid: g["per"][pid]["u_FC"],
}


def tercile(u: float) -> str:
    return "low" if u < 1 / 3 else ("mid" if u < 2 / 3 else "high")


def sensitivity_rows(a: Mapping, sims) -> list[dict]:
    aid, out = a["id"], []
    for par, get in PARAM_GETTERS.items():
        for basis_key in ("first_net", "first_gross"):
            buckets: dict[str, list[str]] = {"low": [], "mid": [], "high": []}
            for g, s in sims:
                for pid in SPONSOR_PROCS:
                    buckets[tercile(get(g, pid))].append(s["proc"][pid][basis_key])
            for b, ws in buckets.items():
                for i in INTERVENTIONS + (("none",) if basis_key == "first_net" else ()):
                    out.append(row("sensitivity", aid, f"share_{basis_key}", ws.count(i) / len(ws) if ws else None,
                                   "share of (draw,process) P01-P15", "assumption-driven", intervention=i,
                                   parameter=par, bucket=b))
    return out


def per_process_c_sensitivity(a: Mapping, sims, procs) -> list[dict]:
    """P(C first by gross) per process by tercile of a_p and of s: the levers that decide C vs the rest."""
    aid, out = a["id"], []
    for p in procs:
        pid = p["id"]
        for par in ("a_p", "s", "d_p"):
            get = PARAM_GETTERS[par]
            for b in ("low", "high"):
                ws = [s["proc"][pid]["first_gross"] for g, s in sims if tercile(get(g, pid)) == b]
                out.append(row("sensitivity_process", aid, "p_C_first_gross", ws.count("C") / len(ws) if ws else None,
                               "prob", "assumption-driven", process_id=pid, process=p["name"], intervention="C",
                               parameter=par, bucket=b))
    return out


def platform_rows(a: Mapping, anchor: Mapping, sims) -> list[dict]:
    aid, out = a["id"], []
    avail = anchor["available_n"]
    for var, key in (("ai_on_workflow", "ai_value_wf"), ("ai_after_redesign", "ai_value_after_d")):
        vals = [s[key] for _, s in sims]
        n_vendor = [breakeven_n(s[key], g["tau"], g["F_platform"], g["f_sponsor"]) for g, s in sims]
        n_social = [breakeven_n(s[key], 1.0, g["F_platform"], g["f_sponsor"]) for g, s in sims]
        self_build = [s[key] - g["F_platform"] > 0 for g, s in sims]
        fee_over_it = [g["tau"] * s[key] / s["it"] for g, s in sims if s.get("it")]
        grants_be = [nv * s["grants"] for nv, (_, s) in zip(n_vendor, sims) if math.isfinite(nv)]
        kw = {"parameter": var}
        out += dist_rows("platform", aid, "sponsor_ai_gross_value", vals, "usd/yr per sponsor", "assumption-driven", **kw)
        out.append(row("platform", aid, "p_self_build_platform_pays", sum(self_build) / len(sims), "prob",
                       "assumption-driven", note="one sponsor carries the full platform cost", **kw))
        out.append(row("platform", aid, "p_vendor_breakeven_finite", sum(math.isfinite(x) for x in n_vendor) / len(sims),
                       "prob", "assumption-driven", note="tau x value > per-sponsor cost", **kw))
        fin = [x for x in n_vendor if math.isfinite(x)]
        for lab, q in (("p10", .1), ("p50", .5), ("p90", .9)):
            out.append(row("platform", aid, f"vendor_breakeven_sponsors_{lab}_finite", quantile(fin, q), "sponsors",
                           "assumption-driven", note="among draws with finite break-even", **kw))
            out.append(row("platform", aid, f"social_breakeven_sponsors_{lab}",
                           quantile([x if math.isfinite(x) else 1e9 for x in n_social], q), "sponsors",
                           "assumption-driven", note="tau=1 (all value counted); 1e9 = never", **kw))
            out.append(row("platform", aid, f"vendor_breakeven_grants_{lab}_finite", quantile(grants_be, q),
                           "grants/yr across network", "assumption-driven", **kw))
        for nmax in (10, 50, 200, 1000):
            out.append(row("platform", aid, f"p_vendor_breakeven_le_{nmax}", sum(x <= nmax for x in n_vendor) / len(sims),
                           "prob", "assumption-driven", **kw))
        if avail:
            out.append(row("platform", aid, "p_vendor_breakeven_le_available", sum(x <= avail for x in n_vendor) / len(sims),
                           "prob", "assumption-driven x observed count", note=f"available sponsors in window = {avail}", **kw))
        if fee_over_it:
            out.append(row("platform", aid, "vendor_fee_over_it_median_p50", quantile(fee_over_it, .5), "ratio",
                           "assumed fee / observed IT median", **kw))
    return out


def v1_replication(procs: Sequence[Mapping]) -> float:
    """Recompute v1 base gross values deterministically; returns max absolute difference vs v1 CSV."""
    diffs = []
    for p in procs:
        L = raw_pool(p, p["touch_rate_base"], p["minutes_base"])
        inf = p["scenario_volume_base"] * p["inference_basis"] * cost_per_case(p["inference_tokens_in"], p["inference_tokens_out"])
        g = {"A": .15 * L, "B": .5 * p["rules_amenability"] * L,
             "C": .4 * p["ai_amenability"] * L - .5 * .1 * L - inf, "D": p["redesign_elimination_share"] * L}
        diffs += [abs(g[i] - p[f"gross_{i}_base_usd"]) for i in INTERVENTIONS]
    return max(diffs)


def assumption_rows() -> list[dict]:
    return [row("assumption", "ALL", "distribution", f"{dist}{params}", basis="assumption" if "OBSERVED" not in why
                else "observed range", parameter=name, note=f"{applies}; {why}") for name, dist, params, applies, why in ASSUMPTIONS]


def anchor_detail_rows(anchors: Sequence[Mapping], procs: Sequence[Mapping]) -> list[dict]:
    v1_per_grant = sum(p["labor_pool_base_usd"] for p in procs if p["id"] in SPONSOR_PROCS) / 1e6
    out = []
    for a in anchors:
        cpg = a["opex"] / a["grants"]
        out.append(row("grant_anchor", "NAT_LARGE", f"opex_per_grant:{a['name']}", cpg, "usd/grant", "observed",
                       note=f"opex {a['opex']:.0f}; grants {a['grants']:.0f}; {a['note'][:150]}"))
        out.append(row("grant_anchor", "NAT_LARGE", f"labour_share_of_opex:{a['name']}", a["labour_share"], "ratio",
                       "observed", note="Part IX (staff lines 5-10 + outside services ex-11f) / operating cost ex-11f"))
        out.append(row("grant_anchor", "NAT_LARGE", f"v1_implied_phi:{a['name']}", v1_per_grant / (cpg * a["labour_share"]),
                       "ratio", "v1 assumption / observed", note="v1 base $4.32/grant / (opex per grant x labour share)"))
    return out


# ---------------------------------------------------------------------------------------------- network break-even
NETWORK_SEGMENTS = (
    ("cf_lt_250m", lambda s: s["category"] == "Community" and s["daf_assets"] < 2.5e8),
    ("cf_all", lambda s: s["category"] == "Community"),
    ("national_lt_10bn", lambda s: s["category"] == "National-Standard" and s["daf_assets"] < 1e10),
    ("cf_and_national_lt_10bn", lambda s: s["category"] in ("Community", "National-Standard") and s["daf_assets"] < 1e10),
    ("cf_and_national_all", lambda s: s["category"] in ("Community", "National-Standard")),
)


def ai_value_per_pool_dollar(procs: Sequence[Mapping], g: Mapping, after_d: bool) -> float:
    """AI gross value per $ of P01-P15 pool (inference ignored: <1% of pool, see archetype_anchor rows)."""
    raws = {p["id"]: raw_pool(p, g["per"][p["id"]]["e"], g["per"][p["id"]]["m"]) for p in procs}
    denom = sum(raws[k] for k in SPONSOR_PROCS)
    def k(pid):
        pp = g["per"][pid]
        v = g["s"] * pp["a"] - 0.5 * g["q"]
        return max(0.0, v * ((1 - pp["d"]) if after_d else 1.0))
    return sum(raws[pid] / denom * k(pid) for pid in SPONSOR_PROCS)


def sponsor_pool_base(s: Mapping) -> float:
    shares = [x for x in (s["share_a"], s["share_g"]) if x is not None]
    share = (sum(shares) / len(shares)) if (shares and s["category"] == "Community") else (s["share_a"] or 1.0)
    return s["opex"] * share * s["labour_share"]


def network_breakeven(values: Sequence[float], tau: float, F: float, f: float) -> float:
    cum = 0.0
    for n, v in enumerate(sorted(values, reverse=True), start=1):
        m = tau * v - f
        if m <= 0:
            return math.inf
        cum += m
        if cum >= F:
            return float(n)
    return math.inf


def network_rows(procs: Sequence[Mapping], sponsors: Sequence[Mapping], draws: int) -> list[dict]:
    rng = random.Random(SEED)
    params = [draw_params(rng, procs) for _ in range(draws)]
    out = []
    pop = [s for s in sponsors if s["fy"] == FY and s["daf_assets"]]
    for seg, pred in NETWORK_SEGMENTS:
        base = [sponsor_pool_base(s) for s in pop if pred(s)]
        for var, after_d in (("ai_on_workflow", False), ("ai_after_redesign", True)):
            ns = []
            for g in params:
                k = ai_value_per_pool_dollar(procs, g, after_d) * g["phi"]
                ns.append(network_breakeven([b * k for b in base], g["tau"], g["F_platform"], g["f_sponsor"]))
            fin = [x for x in ns if math.isfinite(x)]
            kw = {"parameter": var, "bucket": seg}
            out.append(row("platform_network", "OBSERVED_POPULATION", "segment_sponsors_fy2024", len(base), "count",
                           "observed", **kw))
            out.append(row("platform_network", "OBSERVED_POPULATION", "p_breakeven_reachable", len(fin) / len(ns), "prob",
                           "assumption-driven x observed population",
                           note="vendor signs highest-value sponsors first; stops when marginal sponsor loses money", **kw))
            for lab, q in (("p10", .1), ("p50", .5), ("p90", .9)):
                out.append(row("platform_network", "OBSERVED_POPULATION", f"breakeven_sponsors_{lab}_reachable",
                               quantile(fin, q), "sponsors", "assumption-driven x observed population", **kw))
    return out


def write_csv(path: str, rows: Sequence[Mapping]) -> None:
    cols = ("record_type", "archetype", "process_id", "process", "intervention", "parameter", "bucket", "metric",
            "value", "unit", "basis", "note")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------------------------------------- console digest
def digest(a: Mapping, anchor: Mapping, sims, procs) -> list[str]:
    n = len(sims)
    lines = [f"\n== {a['id']} ({a['label']}) window n={anchor['n']} IT med(>0)={anchor['it_med_pos']}"]
    pools = [s["pool_sponsor"] for _, s in sims]
    grants = [s["grants"] for _, s in sims]
    lines.append(f"  grants p50={quantile(grants,.5):,.0f}  pool P01-15 p10/p50/p90={quantile(pools,.1):,.0f}/"
                 f"{quantile(pools,.5):,.0f}/{quantile(pools,.9):,.0f}  per grant p50={quantile([s['pool_sponsor']/s['grants'] for _,s in sims],.5):.2f}")
    for p in procs:
        res = [s["proc"][p["id"]] for _, s in sims]
        wn = {i: sum(r["first_net"] == i for r in res) / n for i in INTERVENTIONS + ("none",)}
        wg = {i: sum(r["first_gross"] == i for r in res) / n for i in INTERVENTIONS}
        lines.append(f"  {p['id']} net " + " ".join(f"{k}{v:.2f}" for k, v in wn.items()) +
                     " | gross " + " ".join(f"{k}{v:.2f}" for k, v in wg.items()) + f" | v1 {p['rank_base']}")
    for key in ("ai_value_wf", "ai_value_after_d"):
        nv = [breakeven_n(s[key], g["tau"], g["F_platform"], g["f_sponsor"]) for g, s in sims]
        fin = [x for x in nv if math.isfinite(x)]
        lines.append(f"  platform {key}: value p50={quantile([s[key] for _,s in sims],.5):,.0f} "
                     f"P(finite)={len(fin)/n:.2f} N*p50={quantile(fin,.5)} P(selfbuild)="
                     f"{sum(s[key]>g['F_platform'] for g,s in sims)/n:.2f}")
    return lines


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--draws", type=int, default=10000)
    ap.add_argument("--out", default=OUT_CSV)
    args = ap.parse_args(argv)

    procs = tuple(v1_process(r) for r in load_csv(V1_CSV))
    sponsors = load_sponsors(load_csv(COST_CSV))
    anchors = grant_anchors(sponsors, load_csv(SUMMARY_CSV))
    print(f"v1 replication max abs diff: {v1_replication(procs):.2f} USD")
    print("grant anchors:", [(x["name"], round(x["opex"] / x["grants"], 2), x["labour_share"]) for x in anchors])

    rows: list[dict] = assumption_rows() + anchor_detail_rows(anchors, procs)
    rows.append(row("meta", "ALL", "draws", args.draws, "count", "definition", note=f"random.Random({SEED}); parameter stream common to all archetypes"))
    rows.append(row("meta", "ALL", "v1_replication_max_abs_diff", v1_replication(procs), "usd", "computed"))
    for idx, a in enumerate(ARCHETYPES):
        anchor = archetype_anchor(a, sponsors, anchors)
        sims = simulate(a, idx, procs, anchor, args.draws)
        rows += anchor_rows(a, anchor, sims, procs)
        rows += process_rows(a, sims, procs)
        rows += sensitivity_rows(a, sims)
        rows += per_process_c_sensitivity(a, sims, procs)
        rows += platform_rows(a, anchor, sims)
        print("\n".join(digest(a, anchor, sims, procs)))
    net = network_rows(procs, sponsors, min(args.draws, 2000))
    for r in net:
        if r["metric"] in ("p_breakeven_reachable", "breakeven_sponsors_p50_reachable"):
            print(f"  network {r['bucket']:<24} {r['parameter']:<18} {r['metric']:<34} {r['value']}")
    rows += net
    write_csv(args.out, rows)
    print(f"\nwrote {len(rows)} rows -> {os.path.relpath(args.out, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
