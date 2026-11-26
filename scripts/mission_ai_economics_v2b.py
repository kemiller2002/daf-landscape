#!/usr/bin/env python3
"""AI-economics v2b: re-run of the v2 model with OBSERVED loaded labour cost per employee instead of BLS-based rates.

Queue item P-LND-03. v2 (scripts/mission_ai_economics_v2.py) is imported unchanged; this script only changes how the
per-process loaded labour rate enters the model. The observed rate is each bootstrapped sponsor's own Form 990
loaded labour cost per employee (Part IX lines 5-10 / Part I line 5 / 2,080 h), from
data/mission-2026-11-14/sponsor-salary-per-employee.csv (record_type=return).

Where the rate enters v2: the dollar pool of an anchored archetype is observed opex x observed labour share x phi;
the v1 bottom-up pools (volume x touch rate x minutes x RATE) only set the MIX across P01-P15. So a rate swap can act
in two ways, and both are run (same seed 42, same parameter and bootstrap streams as v2 -> common random numbers):

  V2B_SCALED   each v1 process rate x (sponsor observed rate / v1 hours-weighted mean rate). Keeps the occupation
               relativities; mix unchanged, so results must equal v2 exactly (checked; written as a meta row only).
  V2B_UNIFORM  every process at the sponsor's single observed all-staff rate (the literal swap). Mix changes because
               the BLS occupation differentials ($30.76 / $34.80 / $55.45) disappear; level unchanged (phi-anchored).
  V2B_BOTTOMUP pool level built bottom-up at the observed rate (scaled as V2B_SCALED) x v1 touch rates and minutes x
               archetype grant volume, capped at observed DAF-allocated labour cost (opex x share x labour share).
               phi is NOT used; the implied phi (pool / labour cost) is reported. This is the variant in which the
               observed rate changes pool size.

Rate source per draw: the sponsor's own valid return (FY2024 preferred, else the nearest year); else the median valid
rate of the archetype window (NAT_LARGE: nationals > $10bn). Fidelity Charitable reports 0 employees and always uses
the fallback. Valid = no flag in INVALID_FLAGS.

Input (comparison only): data/mission-2026-11-14/ai-economics-v2-results.csv (v2 output; record_type=compare_v2 rows).
Output: data/mission-2026-11-14/ai-economics-v2b-results.csv (v2 columns plus leading `variant`).
Usage:  python3 scripts/mission_ai_economics_v2b.py [--draws 10000]
Stdlib only; functional style.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import random
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_ai_economics_v2 as v2  # noqa: E402

SAL_CSV = os.path.join(v2.DATA, "sponsor-salary-per-employee.csv")
OUT_CSV = os.path.join(v2.DATA, "ai-economics-v2b-results.csv")
V2_CSV = v2.OUT_CSV
INVALID_FLAGS = ("employees_lt_5", "no_line7", "wage_lt_20k_parttime_heavy", "wage_gt_300k_outlier")
VARIANTS = ("V2B_UNIFORM", "V2B_BOTTOMUP")


# ---------------------------------------------------------------------------------------------- observed rates
def valid_return(r: Mapping) -> bool:
    return (r["record_type"] == "return" and v2.fnum(r["loaded_all_hourly"]) is not None
            and not any(f in (r["flags"] or "").split(";") for f in INVALID_FLAGS))


def rates_by_ein(rows: Sequence[Mapping], fy: str = v2.FY) -> dict[str, tuple[float, str, str]]:
    """EIN -> (loaded $/h, fiscal year used, return object id); FY2024 preferred, else nearest year (later wins ties)."""
    out = {}
    for r in sorted((r for r in rows if valid_return(r)),
                    key=lambda r: (-abs(int(r["fiscal_year"]) - int(fy)), int(r["fiscal_year"]))):
        out[r["ein"]] = (v2.fnum(r["loaded_all_hourly"]), r["fiscal_year"], r["return_object_id"])
    return out


def window_eins(a: Mapping, anchor: Mapping, sponsors: Sequence[Mapping]) -> tuple[str, ...]:
    if a["mode"] == "grant_anchor":
        return tuple(s["ein"] for s in v2.window_rows(sponsors, a["category"], *a["it_window"]))
    return tuple(s["ein"] for s in anchor["rows"])


def archetype_rate(a: Mapping, anchor: Mapping, sponsors: Sequence[Mapping], rates: Mapping) -> dict:
    eins = window_eins(a, anchor, sponsors)
    vals = tuple(rates[e][0] for e in eins if e in rates)
    return {"fallback": v2.median(vals), "n_window": len(eins), "n_with_rate": len(vals),
            "p25": v2.quantile(vals, .25), "p75": v2.quantile(vals, .75)}


def v1_mean_rate(procs: Sequence[Mapping]) -> float:
    """Hours-weighted mean of the v1 BLS-based rates over P01-P15 at base touch rate and minutes."""
    hrs = {p["id"]: p["scenario_volume_base"] * p["touch_rate_base"] * p["minutes_base"] / 60 for p in procs}
    return (sum(hrs[p["id"]] * p["loaded_rate_usd_hr"] for p in procs if p["id"] in v2.SPONSOR_PROCS)
            / sum(hrs[k] for k in v2.SPONSOR_PROCS))


def sponsor_rate(sp: Mapping, a: Mapping, anchors: Sequence[Mapping], rates: Mapping, arate: Mapping) -> tuple[float, str]:
    ein = next((x["ein"] for x in anchors if x["name"] == sp["src"]), None) if a["mode"] == "grant_anchor" else sp["src"]
    return (rates[ein][0], "own_return") if ein in rates else (arate["fallback"], "archetype_median")


# ---------------------------------------------------------------------------------------------- model variants
def raws_at(procs: Sequence[Mapping], g: Mapping, rate_of) -> dict[str, float]:
    return {p["id"]: p["scenario_volume_base"] * g["per"][p["id"]]["e"] * g["per"][p["id"]]["m"] / 60.0 * rate_of(p)
            for p in procs}


def pools_v2b(procs: Sequence[Mapping], g: Mapping, sp: Mapping, mode: str, variant: str, rate: float,
              rbar: float) -> tuple[dict[str, float], float, bool]:
    """(pools by process, total P01-P15 labour cost ceiling, cap binding). P16 as in v2 (v1 rates, linear)."""
    v1raws = raws_at(procs, g, lambda p: p["loaded_rate_usd_hr"])
    p16 = v1raws.get("P16", 0.0) * sp["grants"] / 1e6
    if mode == "v1_reference":
        return {k: v * sp["grants"] / 1e6 for k, v in v1raws.items()}, math.nan, False
    labour = sp["opex_daf"] * sp["labour_share"]
    if variant == "V2B_UNIFORM":
        raws = raws_at(procs, g, lambda p: rate)
        total, capped = labour * g["phi"], False
    elif variant == "V2B_BOTTOMUP":
        raws = v1raws
        bottom = sum(v1raws[k] for k in v2.SPONSOR_PROCS) * sp["grants"] / 1e6 * rate / rbar
        total, capped = min(bottom, labour), bottom > labour
    else:  # V2B_SCALED: per-process v1 rate x rate/rbar -> identical mix to v2
        raws = raws_at(procs, g, lambda p: p["loaded_rate_usd_hr"] * rate / rbar)
        total, capped = labour * g["phi"], False
    denom = sum(raws[k] for k in v2.SPONSOR_PROCS)
    return {**{k: total * raws[k] / denom for k in v2.SPONSOR_PROCS}, "P16": p16}, labour, capped


def evaluate_v2b(procs, g, sp, mode, variant, rate, rbar) -> dict:
    """Same outputs as v2.evaluate_draw, with v2b pools; extra keys: rate, implied_phi, cap_binding."""
    pools, labour, capped = pools_v2b(procs, g, sp, mode, variant, rate, rbar)
    res = {}
    for p in procs:
        pp = g["per"][p["id"]]
        L = pools[p["id"]]
        gv = v2.gross_values(p, pp, g, L, sp["grants"])
        net = {i: gv[i] - pp["F"][i] for i in v2.INTERVENTIONS}
        res[p["id"]] = {"L": L, "gross": gv, "net": net, "first_net": v2.argmax({**net, "none": 0.0}),
                        "first_gross": v2.argmax({i: gv[i] for i in v2.INTERVENTIONS}),
                        "fc_over_it": {i: (pp["F"][i] / sp["it"]) if sp.get("it") else None for i in v2.INTERVENTIONS}}
    pool_sp = sum(pools[k] for k in v2.SPONSOR_PROCS)
    return {"proc": res, "pool_sponsor": pool_sp,
            "ai_value_wf": sum(max(0.0, res[k]["gross"]["C"]) for k in v2.SPONSOR_PROCS),
            "ai_value_after_d": sum(max(0.0, res[k]["gross"]["C_after_D"]) for k in v2.SPONSOR_PROCS),
            "inference_total": sum(res[k]["gross"]["_inf"] for k in v2.SPONSOR_PROCS),
            "grants": sp["grants"], "it": sp.get("it"), "opex_daf": sp.get("opex_daf"), "rate": rate,
            "implied_phi": pool_sp / labour if labour and math.isfinite(labour) else None, "cap_binding": capped}


def simulate_v2b(a, idx, procs, anchor, anchors, rates, arate, rbar, variant, draws):
    prng = random.Random(v2.SEED)               # identical streams to v2.simulate
    srng = random.Random(v2.SEED * 1000 + idx)
    out, src = [], {"own_return": 0, "archetype_median": 0}
    for _ in range(draws):
        g = v2.draw_params(prng, procs)
        sp = v2.draw_sponsor(srng, a, anchor, g)
        rate, how = (math.nan, "") if a["mode"] == "v1_reference" else sponsor_rate(sp, a, anchors, rates, arate)
        if how:
            src[how] += 1
        out.append((g, evaluate_v2b(procs, g, sp, a["mode"], variant, rate, rbar)))
    return tuple(out), src


# ---------------------------------------------------------------------------------------------- network break-even
def network_rows_v2b(procs, sponsors, rates, rbar, variant, draws) -> list[dict]:
    """v2.network_rows with v2b pools: UNIFORM changes the mix (value per pool $); BOTTOMUP changes each sponsor's pool
    to min(grants x hours/grant x own observed rate (scaled), observed labour cost). Sponsors without a valid rate use
    the median of the segment's valid rates."""
    rng = random.Random(v2.SEED)
    params = [v2.draw_params(rng, procs) for _ in range(draws)]
    pop = [s for s in sponsors if s["fy"] == v2.FY and s["daf_assets"]]
    out = []
    for seg, pred in v2.NETWORK_SEGMENTS:
        members = [s for s in pop if pred(s)]
        fb = v2.median(rates[s["ein"]][0] for s in members if s["ein"] in rates)
        rate_s = [rates[s["ein"]][0] if s["ein"] in rates else fb for s in members]
        labour = [v2.sponsor_pool_base(s) for s in members]
        for var, after_d in (("ai_on_workflow", False), ("ai_after_redesign", True)):
            ns, phis = [], []
            for g in params:
                if variant == "V2B_UNIFORM":
                    k = value_per_pool_dollar(procs, g, after_d, lambda p: 1.0) * g["phi"]
                    vals = [b * k for b in labour]
                else:
                    k = value_per_pool_dollar(procs, g, after_d, lambda p: p["loaded_rate_usd_hr"])
                    hpg_cost = sum(raws_at(procs, g, lambda p: p["loaded_rate_usd_hr"])[pid] for pid in v2.SPONSOR_PROCS) / 1e6
                    pools = [min((s["daf_grants"] or 0.0) / g["avg_grant"] * hpg_cost * r / rbar, b)
                             for s, r, b in zip(members, rate_s, labour)]
                    phis.append(sum(pools) / sum(labour) if sum(labour) else math.nan)
                    vals = [x * k for x in pools]
                ns.append(v2.network_breakeven(vals, g["tau"], g["F_platform"], g["f_sponsor"]))
            fin = [x for x in ns if math.isfinite(x)]
            kw = {"parameter": var, "bucket": seg}
            out.append(v2.row("platform_network", "OBSERVED_POPULATION", "segment_sponsors_fy2024", len(members), "count",
                              "observed", **kw))
            out.append(v2.row("platform_network", "OBSERVED_POPULATION", "p_breakeven_reachable", len(fin) / len(ns), "prob",
                              "assumption-driven x observed population x observed rates", **kw))
            for lab, q in (("p10", .1), ("p50", .5), ("p90", .9)):
                out.append(v2.row("platform_network", "OBSERVED_POPULATION", f"breakeven_sponsors_{lab}_reachable",
                                  v2.quantile(fin, q), "sponsors", "assumption-driven x observed population", **kw))
            if phis:
                out += v2.dist_rows("platform_network", "OBSERVED_POPULATION", "segment_implied_phi", phis, "ratio",
                                    "bottom-up pool / observed labour cost (segment total)", **kw)
    return out


def value_per_pool_dollar(procs, g, after_d, rate_of) -> float:
    raws = raws_at(procs, g, rate_of)
    denom = sum(raws[k] for k in v2.SPONSOR_PROCS)
    def k(pid):
        pp = g["per"][pid]
        v = g["s"] * pp["a"] - 0.5 * g["q"]
        return max(0.0, v * ((1 - pp["d"]) if after_d else 1.0))
    return sum(raws[pid] / denom * k(pid) for pid in v2.SPONSOR_PROCS)


# ---------------------------------------------------------------------------------------------- summaries
def rate_rows(a, arate, sims, src) -> list[dict]:
    aid = a["id"]
    out = [v2.row("labour_rate", aid, "window_sponsors", arate["n_window"], "count", "observed"),
           v2.row("labour_rate", aid, "window_sponsors_with_valid_rate", arate["n_with_rate"], "count", "observed"),
           v2.row("labour_rate", aid, "window_rate_p25", arate["p25"], "usd/h", "observed"),
           v2.row("labour_rate", aid, "window_rate_median_fallback", arate["fallback"], "usd/h", "observed",
                  note="used when the drawn sponsor has no valid return"),
           v2.row("labour_rate", aid, "window_rate_p75", arate["p75"], "usd/h", "observed")]
    n = sum(src.values())
    if n:
        out.append(v2.row("labour_rate", aid, "share_draws_own_return_rate", src["own_return"] / n, "share", "computed"))
        out += v2.dist_rows("labour_rate", aid, "draw_rate", [s["rate"] for _, s in sims], "usd/h", "observed (bootstrapped)")
        phis = [s["implied_phi"] for _, s in sims if s["implied_phi"] is not None]
        out += v2.dist_rows("labour_rate", aid, "implied_phi", phis, "ratio", "pool / observed labour cost")
        out.append(v2.row("labour_rate", aid, "share_draws_cap_binding", sum(s["cap_binding"] for _, s in sims) / n,
                          "share", "computed", note="bottom-up pool exceeded observed labour cost and was capped"))
    return out


def with_variant(variant: str, rows: Sequence[Mapping]) -> list[dict]:
    return [{"variant": variant, **r} for r in rows]


def scaled_equals_v2(procs, sponsors, anchors, rates, rbar, draws) -> float:
    """Max |difference| of pool_sponsor and AI value between V2B_SCALED and v2.evaluate_draw over all archetypes."""
    worst = 0.0
    for idx, a in enumerate(v2.ARCHETYPES):
        anchor = v2.archetype_anchor(a, sponsors, anchors)
        arate = archetype_rate(a, anchor, sponsors, rates)
        sims_b, _ = simulate_v2b(a, idx, procs, anchor, anchors, rates, arate, rbar, "V2B_SCALED", draws)
        sims_0 = v2.simulate(a, idx, procs, anchor, draws)
        worst = max([worst] + [abs(sb[k] - s0[k]) / max(1.0, abs(s0[k])) for (_, sb), (_, s0) in zip(sims_b, sims_0)
                               for k in ("pool_sponsor", "ai_value_wf", "ai_value_after_d")])
    return worst


# ---------------------------------------------------------------------------------------------- comparison with v2
def keyed(rows: Sequence[Mapping]) -> dict:
    return {(r["record_type"], r["archetype"], r["process_id"], r["intervention"], r["parameter"], r["bucket"],
             r["metric"]): v2.fnum(r["value"]) for r in rows}


COMPARE_PLATFORM = ("sponsor_ai_gross_value_p50", "p_vendor_breakeven_finite", "vendor_breakeven_sponsors_p50_finite",
                    "p_vendor_breakeven_le_available", "p_self_build_platform_pays")
COMPARE_NETWORK = ("p_breakeven_reachable", "breakeven_sponsors_p50_reachable")


def compare_rows(variant: str, new: Sequence[Mapping], old: Sequence[Mapping]) -> list[dict]:
    """record_type=compare_v2: value = v2b, note carries v2 and the difference. Rank probabilities are averaged over
    P01-P15 (mean share of processes in which each option ranks first)."""
    n, o, out = keyed(new), keyed(old), []
    def emit(rt_key, metric, val_new, val_old, **kw):
        d = (val_new - val_old) if val_new is not None and val_old is not None else None
        out.append({"variant": variant, **v2.row("compare_v2", rt_key, metric, val_new, basis="v2b vs v2",
                                                 note=f"v2={val_old}; diff={None if d is None else round(d, 6)}", **kw)})
    for a in v2.ARCHETYPES:
        aid = a["id"]
        for basis, opts in (("p_rank_first_net", v2.INTERVENTIONS + ("none",)), ("p_rank_first_gross", v2.INTERVENTIONS)):
            for i in opts:
                ks = [("process_intervention", aid, pid, i, "", "", basis) for pid in v2.SPONSOR_PROCS]
                emit(aid, f"mean_{basis}_P01_P15", v2.mean([n[k] for k in ks if k in n]), v2.mean([o[k] for k in ks if k in o]),
                     intervention=i)
            winners = [max(opts, key=lambda i: n.get(("process_intervention", aid, pid, i, "", "", basis)) or 0) !=
                       max(opts, key=lambda i: o.get(("process_intervention", aid, pid, i, "", "", basis)) or 0)
                       for pid in v2.SPONSOR_PROCS]
            emit(aid, f"processes_modal_winner_changed_{basis}", float(sum(winners)), 0.0)
        k = ("archetype_anchor", aid, "", "", "", "", "sponsor_pool_P01_P15_p50")
        emit(aid, "sponsor_pool_P01_P15_p50", n.get(k), o.get(k))
        for var in ("ai_on_workflow", "ai_after_redesign"):
            for m in COMPARE_PLATFORM:
                k = ("platform", aid, "", "", var, "", m)
                if k in n or k in o:
                    emit(aid, m, n.get(k), o.get(k), parameter=var)
    for seg, _ in v2.NETWORK_SEGMENTS:
        for var in ("ai_on_workflow", "ai_after_redesign"):
            for m in COMPARE_NETWORK:
                k = ("platform_network", "OBSERVED_POPULATION", "", "", var, seg, m)
                emit("OBSERVED_POPULATION", m, n.get(k), o.get(k), parameter=var, bucket=seg)
    return out


def write_csv(path: str, rows: Sequence[Mapping]) -> None:
    cols = ("variant", "record_type", "archetype", "process_id", "process", "intervention", "parameter", "bucket",
            "metric", "value", "unit", "basis", "note")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--draws", type=int, default=10000)
    ap.add_argument("--out", default=OUT_CSV)
    args = ap.parse_args(argv)
    procs = tuple(v2.v1_process(r) for r in v2.load_csv(v2.V1_CSV))
    sponsors = v2.load_sponsors(v2.load_csv(v2.COST_CSV))
    anchors = v2.grant_anchors(sponsors, v2.load_csv(v2.SUMMARY_CSV))
    rates = rates_by_ein(v2.load_csv(SAL_CSV))
    rbar = v1_mean_rate(procs)
    print(f"valid observed rates: {len(rates)} EINs; v1 hours-weighted mean rate P01-P15 = ${rbar:.2f}/h")
    rel = scaled_equals_v2(procs, sponsors, anchors, rates, rbar, min(args.draws, 2000))
    print(f"V2B_SCALED vs v2: max relative difference in pool / AI value = {rel:.3e}")
    rows = [{"variant": "ALL", **v2.row("meta", "ALL", "draws", args.draws, "count", "definition",
                                        note=f"random.Random({v2.SEED}); identical streams to v2")},
            {"variant": "ALL", **v2.row("meta", "ALL", "v1_hours_weighted_mean_rate", rbar, "usd/h", "v1 assumption",
                                        note="P01-P15 at base touch rate and minutes")},
            {"variant": "ALL", **v2.row("meta", "ALL", "valid_rate_eins", len(rates), "count", "observed",
                                        note="sponsor-salary-per-employee.csv returns without " + "/".join(INVALID_FLAGS))},
            {"variant": "V2B_SCALED", **v2.row("meta", "ALL", "max_rel_diff_vs_v2", rel, "ratio", "computed",
                                               note="first 2,000 draws per archetype; 0 = rate level cancels in v2")}]
    for variant in VARIANTS:
        print(f"\n######## {variant}")
        for idx, a in enumerate(v2.ARCHETYPES):
            anchor = v2.archetype_anchor(a, sponsors, anchors)
            arate = archetype_rate(a, anchor, sponsors, rates)
            sims, src = simulate_v2b(a, idx, procs, anchor, anchors, rates, arate, rbar, variant, args.draws)
            rows += with_variant(variant, rate_rows(a, arate, sims, src) + v2.anchor_rows(a, anchor, sims, procs)
                                 + v2.process_rows(a, sims, procs) + v2.platform_rows(a, anchor, sims))
            print("\n".join(v2.digest(a, anchor, sims, procs)))
            if a["mode"] != "v1_reference":
                print(f"  rate p50=${v2.quantile([s['rate'] for _, s in sims], .5):.2f}/h own-return share="
                      f"{src['own_return'] / args.draws:.2f} implied phi p50="
                      f"{v2.quantile([s['implied_phi'] for _, s in sims if s['implied_phi'] is not None], .5):.3f}")
        net = network_rows_v2b(procs, sponsors, rates, rbar, variant, min(args.draws, 2000))
        for r in net:
            if r["metric"] in ("p_breakeven_reachable", "breakeven_sponsors_p50_reachable", "segment_implied_phi_p50"):
                print(f"  network {r['bucket']:<24} {r['parameter']:<18} {r['metric']:<34} {r['value']}")
        rows += with_variant(variant, net)
    old = v2.load_csv(V2_CSV)
    for variant in VARIANTS:
        rows += compare_rows(variant, [r for r in rows if r["variant"] == variant], old)
    write_csv(args.out, rows)
    print(f"\nwrote {len(rows)} rows -> {os.path.relpath(args.out, v2.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
