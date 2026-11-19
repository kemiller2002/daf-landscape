#!/usr/bin/env python3
"""AI-economics v2/v2b re-run with evidence-calibrated ranges for s (AI time saving), q (QA re-review share) and a_p
(AI-amenability). Queue item P-GAP19-04.

The v2 model (scripts/mission_ai_economics_v2.py) and its v2b pool variants (scripts/mission_ai_economics_v2b.py) are
imported unchanged. Only the mapping from the SAME uniform draws to s, q and a_p changes, so every scenario uses common
random numbers with v2 (seed 42): sponsor bootstraps, fixed costs, alpha, beta, b_p, d_p, phi, touch rates and minutes are
identical draw by draw. Differences between scenarios therefore come only from the s / q / a_p ranges.

Evidence behind each range: data/mission-2026-11-14/ai-calibration-evidence-2026-11-19.csv (evidence_id in CAL_SPECS).
The mapping of a published measurement to a model parameter is an INFERENCE (see research/mission-2026-11-14/
gap19-ai-calibration.md §3); the ranges below are therefore calibrated assumptions, not measurements.

Scenarios
  V2_BASELINE          v2 distributions (replication check against ai-economics-v2-results.csv)
  CAL_FIELD_INLOOP     s from production field studies (net of the worker's own checking), q left at v2 (no direct
                       measurement of second-line QA sampling), a_p capped at the task-exposure evidence
  CAL_TASK_REVIEW      s from task-level experiments (time to first output, before downstream checking), q from measured
                       AI error / non-acceptance rates (errors must be caught downstream), a_p as above
  CAL_CENTRAL          50/50 mixture of the two framings per draw (separate stream, does not disturb CRN)
  CAL_COMPLIANCE_FULL  CAL_TASK_REVIEW, but q = 1 (every AI-touched case re-reviewed) for P01, P07, P08, P14
  ATTR_SQ_ONLY         CAL_CENTRAL s and q, v2 a_p          (attribution)
  ATTR_A_ONLY          v2 s and q, calibrated a_p           (attribution)
Models: v2 (all scenarios); v2b V2B_UNIFORM and V2B_BOTTOMUP (V2_BASELINE and CAL_CENTRAL only).

Output (new file; nothing existing is overwritten):
  data/mission-2026-11-14/ai-process-economics-calibrated-2026-11-19.csv
Usage: python3 scripts/mission_ai_economics_calibrated.py [--draws 10000]
Stdlib only; functional style.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import random
import sys
from typing import Callable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_ai_economics_v2 as v2  # noqa: E402
import mission_ai_economics_v2b as v2b  # noqa: E402

OUT_CSV = os.path.join(v2.DATA, "ai-process-economics-calibrated-2026-11-19.csv")
COMPLIANCE_PROCS = frozenset({"P01", "P07", "P08", "P14"})
OPTS_NET = v2.INTERVENTIONS + ("none",)

# ------------------------------------------------------------------------------------------- calibrated ranges
# Each entry: triangular (lo, mode, hi) and the evidence ids (ai-calibration-evidence-2026-11-19.csv) it rests on.
S_V2, Q_V2 = (0.15, 0.40, 0.70), (0.03, 0.10, 0.30)
S_FIELD = (0.00, 0.12, 0.30)   # E01/E02 0.09-0.15 per case; E08/E09 whole-day 3-6% floor-adjacent; E11 negative; E03 0.25
S_TASK = (0.10, 0.30, 0.56)    # E03 0.25, E04 0.40, E12 0.558; lower 0.10 = field-level
Q_ERR = (0.10, 0.20, 0.40)     # E15 ~0.10 TP miss; E06 0.15 notes not rated good; E13 0.17-0.33 hallucination; E01 0.62 non-adherence
A_CAP, A_UP = 0.60, 0.20       # E10 0.15 (LLM alone) / 0.47-0.56 (with tooling) share of tasks


def a_v2(u: float, a1: float) -> float:
    return v2.tri(u, 0.5 * a1, a1, min(0.9, a1 + 0.35))


def a_cal(u: float, a1: float) -> float:
    return v2.tri(u, 0.5 * a1, a1, min(A_CAP, a1 + A_UP))


CAL_SPECS = (
    {"id": "V2_BASELINE", "s": (S_V2,), "q": (Q_V2,), "a": a_v2, "q_override": None,
     "evidence": "v2 assumptions (ai-economics-v2-observed-costs.md §3.2)"},
    {"id": "CAL_FIELD_INLOOP", "s": (S_FIELD,), "q": (Q_V2,), "a": a_cal, "q_override": None,
     "evidence": "s: E01,E02,E03,E08,E09,E11; q: unchanged (no measurement of second-line QA); a: E10,E16"},
    {"id": "CAL_TASK_REVIEW", "s": (S_TASK,), "q": (Q_ERR,), "a": a_cal, "q_override": None,
     "evidence": "s: E03,E04,E12,E14; q: E01,E06,E13,E15; a: E10,E16"},
    {"id": "CAL_CENTRAL", "s": (S_FIELD, S_TASK), "q": (Q_V2, Q_ERR), "a": a_cal, "q_override": None,
     "evidence": "50/50 mixture of CAL_FIELD_INLOOP and CAL_TASK_REVIEW (framing drawn per iteration)"},
    {"id": "CAL_COMPLIANCE_FULL", "s": (S_TASK,), "q": (Q_ERR,), "a": a_cal, "q_override": (COMPLIANCE_PROCS, 1.0),
     "evidence": "CAL_TASK_REVIEW + q=1 for P01,P07,P08,P14: E16 (2% fully autonomous), E13"},
    {"id": "ATTR_SQ_ONLY", "s": (S_FIELD, S_TASK), "q": (Q_V2, Q_ERR), "a": a_v2, "q_override": None,
     "evidence": "attribution: CAL_CENTRAL s,q with v2 a_p"},
    {"id": "ATTR_A_ONLY", "s": (S_V2,), "q": (Q_V2,), "a": a_cal, "q_override": None,
     "evidence": "attribution: v2 s,q with calibrated a_p"},
)
V2B_SCENARIOS = ("V2_BASELINE", "CAL_CENTRAL")


# ------------------------------------------------------------------------------------------- calibrated draws
def calibrate(g0: Mapping, procs: Sequence[Mapping], spec: Mapping, branch: int) -> dict:
    """Re-map the v2 uniforms u_s, u_q, u_a to the scenario's s, q, a_p. Everything else in g0 is kept."""
    k = min(branch, len(spec["s"]) - 1)
    s = v2.tri(g0["u"]["s"], *spec["s"][k])
    q = v2.tri(g0["u"]["q"], *spec["q"][min(branch, len(spec["q"]) - 1)])
    per = {p["id"]: {**g0["per"][p["id"]], "a": spec["a"](g0["per"][p["id"]]["u_a"], p["ai_amenability"])}
           for p in procs}
    ov = spec["q_override"]
    q_p = {p["id"]: (ov[1] if ov and p["id"] in ov[0] else q) for p in procs}
    return {**g0, "s": s, "q": q, "per": per, "q_p": q_p, "branch": k}


def evaluate(procs, g, sp, pools: Mapping[str, float]) -> dict:
    res = {}
    for p in procs:
        pid = p["id"]
        pp = g["per"][pid]
        gv = v2.gross_values(p, pp, {**g, "q": g["q_p"][pid]}, pools[pid], sp["grants"])
        net = {i: gv[i] - pp["F"][i] for i in v2.INTERVENTIONS}
        res[pid] = {"L": pools[pid], "gross": gv, "net": net, "first_net": v2.argmax({**net, "none": 0.0}),
                    "first_gross": v2.argmax({i: gv[i] for i in v2.INTERVENTIONS})}
    pool_sp = sum(pools[k] for k in v2.SPONSOR_PROCS)
    saved = sum(g["s"] * g["per"][k]["a"] * pools[k] for k in v2.SPONSOR_PROCS)
    return {"proc": res, "pool_sponsor": pool_sp, "grants": sp["grants"], "it": sp.get("it"),
            "ai_value_wf": sum(max(0.0, res[k]["gross"]["C"]) for k in v2.SPONSOR_PROCS),
            "ai_value_after_d": sum(max(0.0, res[k]["gross"]["C_after_D"]) for k in v2.SPONSOR_PROCS),
            "implied_time_saving_share": saved / pool_sp if pool_sp else None}


def simulate(a, idx, procs, anchor, draws, spec, model, ctx) -> tuple[tuple[dict, dict], ...]:
    prng = random.Random(v2.SEED)               # identical parameter stream to v2.simulate
    srng = random.Random(v2.SEED * 1000 + idx)  # identical sponsor stream
    mrng = random.Random(v2.SEED + 7919)        # framing-mixture stream (CAL_CENTRAL only)
    out = []
    for _ in range(draws):
        g0 = v2.draw_params(prng, procs)
        sp = v2.draw_sponsor(srng, a, anchor, g0)
        g = calibrate(g0, procs, spec, 0 if mrng.random() < 0.5 else 1)
        if model == "v2":
            pools = v2.process_pools(procs, g, sp, a["mode"])
        else:
            rate = math.nan if a["mode"] == "v1_reference" else \
                v2b.sponsor_rate(sp, a, ctx["anchors"], ctx["rates"], ctx["arate"][a["id"]])[0]
            pools = v2b.pools_v2b(procs, g, sp, a["mode"], model, rate, ctx["rbar"])[0]
        out.append((g, evaluate(procs, g, sp, pools)))
    return tuple(out)


# ------------------------------------------------------------------------------------------- summaries
def row(scn, model, rt, arch, metric, value, unit="", process_id="", intervention="", parameter="", bucket="",
        note="") -> dict:
    return {"scenario": scn, "model": model, "record_type": rt, "archetype": arch, "process_id": process_id,
            "intervention": intervention, "parameter": parameter, "bucket": bucket, "metric": metric,
            "value": round(value, 6) if isinstance(value, float) and math.isfinite(value) else value,
            "unit": unit, "note": note}


def modal(counts: Mapping[str, float]) -> str:
    return max(counts.items(), key=lambda kv: kv[1])[0]


def process_summary(sims, procs) -> dict:
    n = len(sims)
    out = {}
    for p in procs:
        res = [s["proc"][p["id"]] for _, s in sims]
        pg = {i: sum(r["first_gross"] == i for r in res) / n for i in v2.INTERVENTIONS}
        pn = {i: sum(r["first_net"] == i for r in res) / n for i in OPTS_NET}
        out[p["id"]] = {"pg": pg, "pn": pn, "C_net_pos": sum(r["net"]["C"] > 0 for r in res) / n,
                        "C_gross_p50": v2.quantile([r["gross"]["C"] for r in res], .5),
                        "C_net_p50": v2.quantile([r["net"]["C"] for r in res], .5),
                        "C_last": sum(min(v2.INTERVENTIONS, key=lambda i: r["gross"][i]) == "C" for r in res) / n,
                        "modal_gross": modal(pg), "modal_net": modal(pn)}
    return out


def process_rows(scn, model, aid, summ) -> list[dict]:
    out = []
    for pid, d in summ.items():
        for i in v2.INTERVENTIONS:
            out.append(row(scn, model, "process", aid, "p_rank_first_gross", d["pg"][i], "prob", pid, i))
        for i in OPTS_NET:
            out.append(row(scn, model, "process", aid, "p_rank_first_net", d["pn"][i], "prob", pid, i))
        out += [row(scn, model, "process", aid, "p_C_net_positive", d["C_net_pos"], "prob", pid, "C"),
                row(scn, model, "process", aid, "p_C_last_gross", d["C_last"], "prob", pid, "C"),
                row(scn, model, "process", aid, "C_gross_p50", d["C_gross_p50"], "usd/yr", pid, "C"),
                row(scn, model, "process", aid, "C_net_p50", d["C_net_p50"], "usd/yr", pid, "C"),
                row(scn, model, "process", aid, "modal_winner_gross", d["modal_gross"], "", pid),
                row(scn, model, "process", aid, "modal_winner_net", d["modal_net"], "", pid)]
    return out


def archetype_rows(scn, model, a, anchor, sims) -> list[dict]:
    aid, n = a["id"], len(sims)
    out = []
    pools = [s["pool_sponsor"] for _, s in sims]
    sav = [s["implied_time_saving_share"] for _, s in sims if s["implied_time_saving_share"] is not None]
    out += [row(scn, model, "archetype", aid, f"sponsor_pool_P01_P15_{lab}", v2.quantile(pools, q), "usd/yr")
            for lab, q in (("p05", .05), ("p50", .5), ("p95", .95))]
    out += [row(scn, model, "archetype", aid, f"implied_time_saving_share_{lab}", v2.quantile(sav, q), "ratio",
                note="sum(s*a_p*L)/sum(L) over P01-P15; compare whole-job field savings E07-E09")
            for lab, q in (("p05", .05), ("p50", .5), ("p95", .95))]
    for var, key in (("ai_on_workflow", "ai_value_wf"), ("ai_after_redesign", "ai_value_after_d")):
        vals = [s[key] for _, s in sims]
        nv = [v2.breakeven_n(s[key], g["tau"], g["F_platform"], g["f_sponsor"]) for g, s in sims]
        fin = [x for x in nv if math.isfinite(x)]
        out += [row(scn, model, "archetype", aid, f"sponsor_ai_gross_value_{lab}", v2.quantile(vals, q), "usd/yr",
                    parameter=var) for lab, q in (("p05", .05), ("p25", .25), ("p50", .5), ("p75", .75), ("p95", .95))]
        out += [row(scn, model, "archetype", aid, "p_self_build_platform_pays",
                    sum(s[key] > g["F_platform"] for g, s in sims) / n, "prob", parameter=var),
                row(scn, model, "archetype", aid, "p_vendor_breakeven_finite", len(fin) / n, "prob", parameter=var),
                row(scn, model, "archetype", aid, "vendor_breakeven_sponsors_p50_finite", v2.quantile(fin, .5),
                    "sponsors", parameter=var)]
        if anchor["available_n"]:
            out.append(row(scn, model, "archetype", aid, "p_vendor_breakeven_le_available",
                           sum(x <= anchor["available_n"] for x in nv) / n, "prob", parameter=var,
                           note=f"available sponsors = {anchor['available_n']}"))
    return out


SENS_GETTERS: dict[str, Callable] = {
    "s": lambda g, pid: g["u"]["s"], "q": lambda g, pid: g["u"]["q"], "a_p": lambda g, pid: g["per"][pid]["u_a"]}


def sensitivity_rows(scn, model, aid, sims) -> list[dict]:
    """Share of (draw, process) P01-P15 where C ranks first by gross, and sponsor AI value p50, by tercile of the
    parameter's underlying uniform (low/mid/high third of its calibrated range)."""
    out = []
    for par, get in SENS_GETTERS.items():
        for b in ("low", "mid", "high"):
            ws = [s["proc"][pid]["first_gross"] for g, s in sims for pid in v2.SPONSOR_PROCS if v2.tercile(get(g, pid)) == b]
            pos = [s["proc"][pid]["net"]["C"] > 0 for g, s in sims for pid in v2.SPONSOR_PROCS
                   if v2.tercile(get(g, pid)) == b]
            out.append(row(scn, model, "sensitivity", aid, "share_C_first_gross", ws.count("C") / len(ws) if ws else None,
                           "share of (draw,process)", parameter=par, bucket=b))
            out.append(row(scn, model, "sensitivity", aid, "share_C_net_positive", sum(pos) / len(pos) if pos else None,
                           "share of (draw,process)", parameter=par, bucket=b))
            if par != "a_p":
                vals = [s["ai_value_wf"] for g, s in sims if v2.tercile(get(g, "")) == b]
                out.append(row(scn, model, "sensitivity", aid, "sponsor_ai_gross_value_p50", v2.quantile(vals, .5),
                               "usd/yr", parameter=par, bucket=b))
    if scn == "CAL_CENTRAL":
        for k, lab in ((0, "field_inloop"), (1, "task_review")):
            ws = [s["proc"][pid]["first_gross"] for g, s in sims for pid in v2.SPONSOR_PROCS if g["branch"] == k]
            vals = [s["ai_value_wf"] for g, s in sims if g["branch"] == k]
            out.append(row(scn, model, "sensitivity", aid, "share_C_first_gross", ws.count("C") / len(ws) if ws else None,
                           "share of (draw,process)", parameter="framing", bucket=lab))
            out.append(row(scn, model, "sensitivity", aid, "sponsor_ai_gross_value_p50", v2.quantile(vals, .5), "usd/yr",
                           parameter="framing", bucket=lab))
    return out


def value_per_pool_dollar(procs, g, after_d: bool) -> float:
    raws = {p["id"]: v2.raw_pool(p, g["per"][p["id"]]["e"], g["per"][p["id"]]["m"]) for p in procs}
    denom = sum(raws[k] for k in v2.SPONSOR_PROCS)
    def k(pid):
        pp = g["per"][pid]
        v = g["s"] * pp["a"] - 0.5 * g["q_p"][pid]
        return max(0.0, v * ((1 - pp["d"]) if after_d else 1.0))
    return sum(raws[pid] / denom * k(pid) for pid in v2.SPONSOR_PROCS)


def network_rows(scn, procs, sponsors, spec, draws) -> list[dict]:
    rng, mrng = random.Random(v2.SEED), random.Random(v2.SEED + 7919)
    params = [calibrate(v2.draw_params(rng, procs), procs, spec, 0 if mrng.random() < 0.5 else 1) for _ in range(draws)]
    pop = [s for s in sponsors if s["fy"] == v2.FY and s["daf_assets"]]
    out = []
    for seg, pred in v2.NETWORK_SEGMENTS:
        base = [v2.sponsor_pool_base(s) for s in pop if pred(s)]
        for var, after_d in (("ai_on_workflow", False), ("ai_after_redesign", True)):
            ns = [v2.network_breakeven([b * value_per_pool_dollar(procs, g, after_d) * g["phi"] for b in base],
                                       g["tau"], g["F_platform"], g["f_sponsor"]) for g in params]
            fin = [x for x in ns if math.isfinite(x)]
            out += [row(scn, "v2", "network", "OBSERVED_POPULATION", "p_breakeven_reachable", len(fin) / len(ns), "prob",
                        parameter=var, bucket=seg, note=f"{len(base)} FY2024 sponsors in segment"),
                    row(scn, "v2", "network", "OBSERVED_POPULATION", "breakeven_sponsors_p50_reachable",
                        v2.quantile(fin, .5), "sponsors", parameter=var, bucket=seg)]
    return out


def compare_rows(scn, model, aid, summ, base) -> list[dict]:
    out = []
    for basis, key, opts in (("gross", "pg", v2.INTERVENTIONS), ("net", "pn", OPTS_NET)):
        for i in opts:
            new = v2.mean([summ[pid][key][i] for pid in v2.SPONSOR_PROCS])
            old = v2.mean([base[pid][key][i] for pid in v2.SPONSOR_PROCS])
            out.append(row(scn, model, "compare_baseline", aid, f"mean_p_rank_first_{basis}_P01_P15", new, "prob",
                           intervention=i, note=f"V2_BASELINE={round(old, 6)}; diff={round(new - old, 6)}"))
        changed = [pid for pid in v2.SPONSOR_PROCS if summ[pid][f"modal_{basis}"] != base[pid][f"modal_{basis}"]]
        out.append(row(scn, model, "compare_baseline", aid, f"processes_modal_winner_changed_{basis}", float(len(changed)),
                       "count", note=";".join(f"{pid}:{base[pid][f'modal_{basis}']}->{summ[pid][f'modal_{basis}']}"
                                              for pid in changed)))
    return out


def replication_check(procs, sponsors, anchors, draws) -> float:
    """Max |P(first gross) difference| between V2_BASELINE here and v2.simulate at the same draws."""
    worst = 0.0
    spec = CAL_SPECS[0]
    for idx, a in enumerate(v2.ARCHETYPES):
        anchor = v2.archetype_anchor(a, sponsors, anchors)
        mine = process_summary(simulate(a, idx, procs, anchor, draws, spec, "v2", {}), procs)
        ref = v2.simulate(a, idx, procs, anchor, draws)
        n = len(ref)
        for p in procs:
            for i in v2.INTERVENTIONS:
                r = sum(s["proc"][p["id"]]["first_gross"] == i for _, s in ref) / n
                worst = max(worst, abs(r - mine[p["id"]]["pg"][i]))
    return worst


def spec_rows() -> list[dict]:
    fmt = lambda t: "/".join(f"triangular{x}" for x in t)  # noqa: E731
    out = []
    for sp in CAL_SPECS:
        a_txt = ("tri(0.5a1, a1, min(0.9, a1+0.35))" if sp["a"] is a_v2
                 else f"tri(0.5a1, a1, min({A_CAP}, a1+{A_UP}))")
        q_txt = fmt(sp["q"]) + (f"; q=1 for {','.join(sorted(sp['q_override'][0]))}" if sp["q_override"] else "")
        out += [row(sp["id"], "spec", "spec", "ALL", "s_distribution", fmt(sp["s"]), parameter="s", note=sp["evidence"]),
                row(sp["id"], "spec", "spec", "ALL", "q_distribution", q_txt, parameter="q"),
                row(sp["id"], "spec", "spec", "ALL", "a_distribution", a_txt, parameter="a_p")]
    return out


def write_csv(path: str, rows: Sequence[Mapping]) -> None:
    cols = ("scenario", "model", "record_type", "archetype", "process_id", "intervention", "parameter", "bucket",
            "metric", "value", "unit", "note")
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
    rates = v2b.rates_by_ein(v2.load_csv(v2b.SAL_CSV))
    rbar = v2b.v1_mean_rate(procs)
    anchor_by = {a["id"]: v2.archetype_anchor(a, sponsors, anchors) for a in v2.ARCHETYPES}
    ctx = {"anchors": anchors, "rates": rates, "rbar": rbar,
           "arate": {a["id"]: v2b.archetype_rate(a, anchor_by[a["id"]], sponsors, rates) for a in v2.ARCHETYPES}}
    rep = replication_check(procs, sponsors, anchors, min(args.draws, 1000))
    print(f"V2_BASELINE vs v2.simulate: max |P(first gross)| difference = {rep:.2e}")
    rows = spec_rows() + [row("ALL", "meta", "meta", "ALL", "draws", args.draws, "count",
                              note="random.Random(42) common random numbers with v2; mixture stream Random(42+7919)"),
                          row("V2_BASELINE", "v2", "meta", "ALL", "replication_max_abs_diff_p_first_gross", rep, "prob",
                              note="first 1,000 draws per archetype vs mission_ai_economics_v2.simulate")]
    runs = [(sp, "v2") for sp in CAL_SPECS] + [(sp, m) for sp in CAL_SPECS if sp["id"] in V2B_SCENARIOS
                                                 for m in v2b.VARIANTS]
    base_summ: dict[tuple[str, str], dict] = {}
    for sp, model in runs:
        print(f"\n######## {sp['id']} / {model}")
        for idx, a in enumerate(v2.ARCHETYPES):
            sims = simulate(a, idx, procs, anchor_by[a["id"]], args.draws, sp, model, ctx)
            summ = process_summary(sims, procs)
            if sp["id"] == "V2_BASELINE":
                base_summ[(model, a["id"])] = summ
            rows += process_rows(sp["id"], model, a["id"], summ) + archetype_rows(sp["id"], model, a, anchor_by[a["id"]], sims)
            rows += sensitivity_rows(sp["id"], model, a["id"], sims)
            rows += compare_rows(sp["id"], model, a["id"], summ, base_summ[(model, a["id"])])
            vals = [s["ai_value_wf"] for _, s in sims]
            cfirst = v2.mean([summ[pid]["pg"]["C"] for pid in v2.SPONSOR_PROCS])
            print(f"  {a['id']:<10} AI value p50={v2.quantile(vals, .5):>12,.0f}  mean P(C first gross)={cfirst:.3f}  "
                  "modal gross " + "".join(summ[pid]["modal_gross"] for pid in v2.SPONSOR_PROCS) +
                  "  modal net " + ",".join(summ[pid]["modal_net"] for pid in v2.SPONSOR_PROCS))
        if model == "v2":
            net = network_rows(sp["id"], procs, sponsors, sp, min(args.draws, 2000))
            rows += net
            for r in net:
                if r["metric"] == "p_breakeven_reachable" and r["parameter"] == "ai_on_workflow":
                    print(f"  network {r['bucket']:<24} P(reachable)={r['value']}")
    write_csv(args.out, rows)
    print(f"\nwrote {len(rows)} rows -> {os.path.relpath(args.out, v2.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
