#!/usr/bin/env python3
"""Confidence-gated routing variant of intervention C (AI on the existing workflow). Queue item P-G04-01.

The calibrated model (scripts/mission_ai_economics_calibrated.py, which imports v2 unchanged) values C as an
assistant on every AI-amenable case:

    C_assist = s * a_p * L - 0.5 * q_p * L - inference

The routing variant replaces that structure. Of the AI-amenable cases (share a_p of process labour L), a share h is
high-confidence and closed by AI alone; the rest go to humans, unchanged. A share k of AI-closed cases is sampled by
second-line QA at half handling time (the model's existing 0.5 convention). AI-closed cases carry an excess error rate
e over human handling. Sampled errors are reworked at full handling time; unsampled errors escape and cost m handling
units each. rho is any residual human time on an AI-closed case.

    C_route  = h * a_p * L * [(1 - rho) - 0.5 k - k e - (1 - k) e m] - inference
    C_hybrid = C_route + (1 - h) * (s * a_p * L - 0.5 * q_p * L)        (assist kept on the low-confidence rest)

Everything else (pools, A/B/D, fixed costs, inference, platform terms, sponsor bootstraps) is the calibrated model's,
on the same uniform draws (common random numbers, seed 42). Routing parameters come from a separate stream, so C_assist,
C_route and C_hybrid are compared draw by draw.

Routing-parameter evidence (data/mission-2026-11-14/ai-calibration-evidence-2026-11-19.csv and the E19 full text):
  h   uniform(0.21, 0.49)   E19 (Agarwal et al., NBER w31422, rev. Aug 2026, s6.3): with a high cost of a false
                            negative, the optimal policy leaves 21% of cases to the AI alone for Bayesian deciders and
                            involves humans in 51% (so 49% AI alone) with observed radiologist behaviour. The mapping to
                            a share of DAF back-office AI-amenable cases is an INFERENCE [I]. Swept 0.10-0.90.
  e   uniform(0.00, 0.10)   E19 (AI alone outperforms AI-assisted humans in the delegated range: excess error <= 0) to
                            E15 (auto-closing AML alerts misses about 10% of true positives). [I]. Swept 0-0.40; 0.20 and
                            0.40 equal the mode and top of the calibrated unconditional error range (confidence carries
                            no information).
  k   triangular(.03,.10,.30) v2's QA range, retained as UNSOURCED by the calibration (no source measures a second-line
                            QA sampling rate). k = 1 for P01/P07/P08/P14 under CAL_COMPLIANCE_FULL (E16). Swept 0.02-1.
  rho 0                     E19 defines AI-alone decisions at zero human time. Swept 0-0.50 [I].
  m   sweep only {0,1,5,20,50}  no evidence on the cost of an escaped back-office error; headline results are shown at
                            m = 1, 5 and 20 and labelled [I].
  F_C multiplier sweep {1, 1.5, 2} [I]: routing needs confidence calibration and monitoring; 1 = calibrated F_C draw.

Output (new file): data/mission-2026-11-14/ai-routing-variant-2026-11-19.csv
Usage: python3 scripts/mission_ai_routing_variant.py . [--draws 10000] [--out PATH]
Stdlib only; functional style (pure functions; I/O in main).
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
import mission_ai_economics_calibrated as cal  # noqa: E402

v2 = cal.v2
OUT_CSV = os.path.join(v2.DATA, "ai-routing-variant-2026-11-19.csv")
ROUTE_SEED = v2.SEED + 104729          # separate stream: leaves the calibrated draws untouched
SCENARIOS = ("CAL_CENTRAL", "CAL_FIELD_INLOOP", "CAL_TASK_REVIEW", "CAL_COMPLIANCE_FULL")
SWEEP_SCENARIO = "CAL_CENTRAL"
SWEEP_ARCHETYPES = ("NAT_LARGE", "NAT_MID", "CF_1BN")
VARIANTS = ("assist", "route", "hybrid")
OTHERS = ("A", "B", "D")
M_HEADLINE = (1.0, 5.0, 20.0)

ROUTE_RANGES = (
    ("h", "uniform", (0.21, 0.49), "E19 s6.3: 21% (Bayesian) to 49% (observed behaviour) of cases to AI alone at high false-negative cost [I mapping]"),
    ("e", "uniform", (0.00, 0.10), "E19 (AI alone <= AI-assisted human in delegated bins) to E15 (10% of true positives missed if auto-closed) [I]"),
    ("k", "triangular", (0.03, 0.10, 0.30), "v2 QA range, unsourced (calibration doc s3.2); k=1 for P01,P07,P08,P14 under CAL_COMPLIANCE_FULL (E16)"),
    ("rho", "fixed", (0.0,), "E19 defines AI-alone decisions at zero human time [definition]"),
    ("m", "sweep", (0.0, 1.0, 5.0, 20.0, 50.0), "no evidence: cost of an escaped error in handling units [I sweep]"),
    ("fc_mult", "sweep", (1.0, 1.5, 2.0), "routing calibration/monitoring cost multiplier on F_C [I sweep]"),
)
SWEEPS = (
    ("h", (0.10, 0.21, 0.35, 0.49, 0.70, 0.90)),
    ("e", (0.0, 0.02, 0.05, 0.10, 0.20, 0.40)),
    ("k", (0.02, 0.05, 0.10, 0.30, 1.0)),
    ("m", (0.0, 1.0, 5.0, 20.0, 50.0)),
    ("rho", (0.0, 0.10, 0.25, 0.50)),
    ("fc_mult", (1.0, 1.5, 2.0)),
)
GRID_H = (0.10, 0.21, 0.35, 0.49, 0.70, 0.90)
GRID_E = (0.0, 0.02, 0.05, 0.10, 0.20, 0.40)


# ------------------------------------------------------------------------------------------- routing draws (pure)
def draw_route(u: Sequence[float]) -> dict:
    """Map three uniforms to the evidence-bounded routing parameters."""
    return {"h": v2.uni(u[0], 0.21, 0.49), "e": v2.uni(u[1], 0.0, 0.10), "k": v2.tri(u[2], 0.03, 0.10, 0.30),
            "rho": 0.0}


def route_stream(n: int) -> tuple[dict, ...]:
    rng = random.Random(ROUTE_SEED)
    return tuple(draw_route((rng.random(), rng.random(), rng.random())) for _ in range(n))


def k_for(scn: str, pid: str, k: float) -> float:
    return 1.0 if scn == "CAL_COMPLIANCE_FULL" and pid in cal.COMPLIANCE_PROCS else k


def per_case_yield(rp: Mapping, k: float, m: float) -> float:
    """Net labour saved per AI-closed case, in handling units."""
    e = rp["e"]
    return (1.0 - rp["rho"]) - 0.5 * k - k * e - (1.0 - k) * e * m


# ------------------------------------------------------------------------------------------- compact draws (pure)
def compact(scn: str, g: Mapping, s: Mapping, procs: Sequence[Mapping]) -> dict:
    """Per-draw, per-process numbers that the routing formula needs (from one calibrated simulate() draw)."""
    def one(p):
        pid = p["id"]
        r = s["proc"][pid]
        gv = r["gross"]
        return {"pid": pid, "L": r["L"], "a": g["per"][pid]["a"], "inf": gv["_inf"], "assist": gv["C"],
                "others": {i: gv[i] for i in OTHERS}, "F": dict(g["per"][pid]["F"]),
                "assist_rest": g["s"] * g["per"][pid]["a"] * r["L"] - 0.5 * g["q_p"][pid] * r["L"]}
    return {"procs": tuple(one(p) for p in procs), "tau": g["tau"], "F_platform": g["F_platform"],
            "f_sponsor": g["f_sponsor"]}


def c_value(variant: str, cp: Mapping, rp: Mapping, scn: str, m: float) -> float:
    if variant == "assist":
        return cp["assist"]
    k = k_for(scn, cp["pid"], rp["k"])
    route = rp["h"] * cp["a"] * cp["L"] * per_case_yield(rp, k, m) - cp["inf"]
    return route + ((1.0 - rp["h"]) * cp["assist_rest"] if variant == "hybrid" else 0.0)


def eval_draw(d: Mapping, rp: Mapping, scn: str, variant: str, m: float, fc_mult: float) -> dict:
    """Ranking, net value and break-even h for one draw under one routing cell."""
    out = {}
    for cp in d["procs"]:
        c = c_value(variant, cp, rp, scn, m)
        fc = cp["F"]["C"] * (fc_mult if variant != "assist" else 1.0)
        gross = {**cp["others"], "C": c}
        net = {i: gross[i] - cp["F"][i] for i in OTHERS}
        net["C"] = c - fc
        k = k_for(scn, cp["pid"], rp["k"])
        y = cp["a"] * cp["L"] * per_case_yield(rp, k, m)
        out[cp["pid"]] = {"c": c, "first_gross": v2.argmax(gross), "first_net": v2.argmax({**net, "none": 0.0}),
                          "net_pos": net["C"] > 0,
                          "h_be_net": (fc + cp["inf"]) / y if y > 0 else math.inf,
                          "h_be_rank": (max(cp["others"].values()) + cp["inf"]) / y if y > 0 else math.inf}
    pool = sum(max(0.0, out[k]["c"]) for k in v2.SPONSOR_PROCS)
    return {"proc": out, "pool": pool,
            "n_be": v2.breakeven_n(pool, d["tau"], d["F_platform"], d["f_sponsor"])}


# ------------------------------------------------------------------------------------------- summaries (pure)
def wilson(p: float, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def row(scn, arch, variant, cell, metric, value, unit="", process_id="", lo=None, hi=None, note="") -> dict:
    rnd = lambda x: round(x, 6) if isinstance(x, float) and math.isfinite(x) else x  # noqa: E731
    return {"scenario": scn, "archetype": arch, "variant": variant, "cell": cell, "process_id": process_id,
            "metric": metric, "value": rnd(value), "lo": rnd(lo) if lo is not None else "",
            "hi": rnd(hi) if hi is not None else "", "unit": unit, "note": note}


def summarise(evals: Sequence[Mapping], procs: Sequence[Mapping], avail: int | None) -> dict:
    n = len(evals)
    per = {}
    for p in procs:
        pid = p["id"]
        rs = [e["proc"][pid] for e in evals]
        per[pid] = {"p_first_gross": sum(r["first_gross"] == "C" for r in rs) / n,
                    "p_first_net": sum(r["first_net"] == "C" for r in rs) / n,
                    "p_net_pos": sum(r["net_pos"] for r in rs) / n,
                    "c_p50": v2.quantile([r["c"] for r in rs], .5),
                    "modal_gross": cal.modal({i: sum(r["first_gross"] == i for r in rs) for i in OTHERS + ("C",)}),
                    "h_be_net_p50": v2.quantile([r["h_be_net"] for r in rs], .5),
                    "h_be_net_p25": v2.quantile([r["h_be_net"] for r in rs], .25),
                    "h_be_net_p75": v2.quantile([r["h_be_net"] for r in rs], .75),
                    "p_h_be_net_le_049": sum(r["h_be_net"] <= 0.49 for r in rs) / n,
                    "h_be_rank_p50": v2.quantile([r["h_be_rank"] for r in rs], .5)}
    pools = [e["pool"] for e in evals]
    nbe = [e["n_be"] for e in evals]
    fin = [x for x in nbe if math.isfinite(x)]
    return {"n": n, "per": per,
            "mean_p_first_gross": v2.mean([per[k]["p_first_gross"] for k in v2.SPONSOR_PROCS]),
            "mean_p_first_net": v2.mean([per[k]["p_first_net"] for k in v2.SPONSOR_PROCS]),
            "max_p_net_pos": max(per[k]["p_net_pos"] for k in v2.SPONSOR_PROCS),
            "pool_q": {lab: v2.quantile(pools, q) for lab, q in
                       (("p05", .05), ("p25", .25), ("p50", .5), ("p75", .75), ("p95", .95))},
            "p_be_finite": len(fin) / n, "n_be_p50": v2.quantile(fin, .5), "n_be_p25": v2.quantile(fin, .25),
            "n_be_p75": v2.quantile(fin, .75),
            "p_be_le_avail": (sum(x <= avail for x in nbe) / n) if avail else None}


def headline_rows(scn, arch, variant, cell, sm, base_modal) -> list[dict]:
    n = sm["n"]
    out = []
    for key, metric in (("mean_p_first_gross", "mean_p_C_rank_first_gross_P01_P15"),
                        ("mean_p_first_net", "mean_p_C_rank_first_net_P01_P15")):
        lo, hi = wilson(sm[key], n * len(v2.SPONSOR_PROCS))
        out.append(row(scn, arch, variant, cell, metric, sm[key], "prob", lo=lo, hi=hi,
                       note="lo/hi: 95% Wilson interval for Monte Carlo error only (process-draws pooled)"))
    q = sm["pool_q"]
    out += [row(scn, arch, variant, cell, "sponsor_ai_gross_value_p50", q["p50"], "usd/yr", lo=q["p25"], hi=q["p75"],
                note="lo/hi = p25/p75 across draws"),
            row(scn, arch, variant, cell, "sponsor_ai_gross_value_p05_p95", q["p50"], "usd/yr", lo=q["p05"], hi=q["p95"],
                note="lo/hi = p05/p95 across draws"),
            row(scn, arch, variant, cell, "max_process_p_C_net_positive", sm["max_p_net_pos"], "prob"),
            row(scn, arch, variant, cell, "p_vendor_breakeven_finite", sm["p_be_finite"], "prob",
                *(("",) + wilson(sm["p_be_finite"], n))),
            row(scn, arch, variant, cell, "vendor_breakeven_sponsors_p50_finite", sm["n_be_p50"], "sponsors",
                lo=sm["n_be_p25"], hi=sm["n_be_p75"], note="lo/hi = p25/p75 among finite draws")]
    if sm["p_be_le_avail"] is not None:
        out.append(row(scn, arch, variant, cell, "p_vendor_breakeven_le_available", sm["p_be_le_avail"], "prob",
                       *(("",) + wilson(sm["p_be_le_avail"], n))))
    changed = [pid for pid in v2.SPONSOR_PROCS if sm["per"][pid]["modal_gross"] != base_modal[pid]]
    out.append(row(scn, arch, variant, cell, "processes_modal_winner_changed_gross_vs_assist", float(len(changed)),
                   "count", note=";".join(f"{pid}:{base_modal[pid]}->{sm['per'][pid]['modal_gross']}" for pid in changed)))
    return out


def process_rows(scn, arch, variant, cell, sm) -> list[dict]:
    out = []
    for pid, d in sm["per"].items():
        out += [row(scn, arch, variant, cell, "p_C_rank_first_gross", d["p_first_gross"], "prob", pid,
                    *wilson(d["p_first_gross"], sm["n"])),
                row(scn, arch, variant, cell, "p_C_net_positive", d["p_net_pos"], "prob", pid, *wilson(d["p_net_pos"], sm["n"])),
                row(scn, arch, variant, cell, "C_gross_p50", d["c_p50"], "usd/yr", pid),
                row(scn, arch, variant, cell, "modal_winner_gross", d["modal_gross"], "", pid)]
        if variant == "route":
            out += [row(scn, arch, variant, cell, "breakeven_h_net_p50", d["h_be_net_p50"], "share of amenable cases", pid,
                        lo=d["h_be_net_p25"], hi=d["h_be_net_p75"],
                        note="h at which C_route clears F_C (others at cell values); lo/hi = p25/p75; inf = never"),
                    row(scn, arch, variant, cell, "p_breakeven_h_net_le_0.49", d["p_h_be_net_le_049"], "prob", pid,
                        note="share of draws where h <= 0.49 (E19 upper anchor) suffices to clear F_C"),
                    row(scn, arch, variant, cell, "breakeven_h_rank_first_p50", d["h_be_rank_p50"], "share of amenable cases",
                        pid, note="h at which C_route matches the best of A/B/D by gross")]
    return out


def network_rows(procs, sponsors, scn, draws, m, routes) -> list[dict]:
    """Observed FY2024 population break-even (calibrated network_rows logic) for each C variant."""
    spec = next(s for s in cal.CAL_SPECS if s["id"] == scn)
    rng, mrng = random.Random(v2.SEED), random.Random(v2.SEED + 7919)
    params = [cal.calibrate(v2.draw_params(rng, procs), procs, spec, 0 if mrng.random() < 0.5 else 1)
              for _ in range(draws)]
    pop = [s for s in sponsors if s["fy"] == v2.FY and s["daf_assets"]]

    def k_per_dollar(g, rp, variant):
        raws = {p["id"]: v2.raw_pool(p, g["per"][p["id"]]["e"], g["per"][p["id"]]["m"]) for p in procs}
        den = sum(raws[x] for x in v2.SPONSOR_PROCS)
        def val(pid):
            a = g["per"][pid]["a"]
            assist = g["s"] * a - 0.5 * g["q_p"][pid]
            if variant == "assist":
                return max(0.0, assist)
            r = rp["h"] * a * per_case_yield(rp, k_for(scn, pid, rp["k"]), m)
            return max(0.0, r + ((1 - rp["h"]) * assist if variant == "hybrid" else 0.0))
        return sum(raws[pid] / den * val(pid) for pid in v2.SPONSOR_PROCS)

    out = []
    for seg, pred in v2.NETWORK_SEGMENTS:
        base = [v2.sponsor_pool_base(s) for s in pop if pred(s)]
        for variant in VARIANTS:
            ns = [v2.network_breakeven([b * k_per_dollar(g, rp, variant) * g["phi"] for b in base], g["tau"],
                                       g["F_platform"], g["f_sponsor"]) for g, rp in zip(params, routes)]
            fin = [x for x in ns if math.isfinite(x)]
            p = len(fin) / len(ns)
            out += [row(scn, "OBSERVED_POPULATION", variant, f"main_m{m:g}", "p_breakeven_reachable", p, "prob",
                        seg, *wilson(p, len(ns)), note=f"{len(base)} FY2024 sponsors in segment (process_id column = segment)"),
                    row(scn, "OBSERVED_POPULATION", variant, f"main_m{m:g}", "breakeven_sponsors_p50_reachable",
                        v2.quantile(fin, .5), "sponsors", seg)]
    return out


def cell_routes(routes: Sequence[Mapping], par: str, val: float) -> tuple[dict, ...]:
    return routes if par in ("m", "fc_mult") else tuple({**r, par: val} for r in routes)


def spec_rows() -> list[dict]:
    return [row("ALL", "ALL", "spec", "spec", f"{n}_{kind}", "/".join(f"{x:g}" for x in vals), "", note=why)
            for n, kind, vals, why in ROUTE_RANGES]


def write_csv(path: str, rows: Sequence[Mapping]) -> None:
    cols = ("scenario", "archetype", "variant", "cell", "process_id", "metric", "value", "lo", "hi", "unit", "note")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


# ------------------------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (accepted for the repo CLI convention; unused)")
    ap.add_argument("--draws", type=int, default=10000)
    ap.add_argument("--net-draws", type=int, default=2000)
    ap.add_argument("--out", default=OUT_CSV)
    args = ap.parse_args(argv)
    procs = tuple(v2.v1_process(r) for r in v2.load_csv(v2.V1_CSV))
    sponsors = v2.load_sponsors(v2.load_csv(v2.COST_CSV))
    anchors = v2.grant_anchors(sponsors, v2.load_csv(v2.SUMMARY_CSV))
    anchor_by = {a["id"]: v2.archetype_anchor(a, sponsors, anchors) for a in v2.ARCHETYPES}
    routes = route_stream(args.draws)
    rows = spec_rows() + [row("ALL", "ALL", "meta", "meta", "draws", float(args.draws), "count",
                              note=f"calibrated draws Random({v2.SEED}); routing stream Random({ROUTE_SEED})")]
    for scn in SCENARIOS:
        spec = next(s for s in cal.CAL_SPECS if s["id"] == scn)
        for idx, a in enumerate(v2.ARCHETYPES):
            aid, avail = a["id"], anchor_by[a["id"]]["available_n"]
            sims = cal.simulate(a, idx, procs, anchor_by[aid], args.draws, spec, "v2", {})
            ds = tuple(compact(scn, g, s, procs) for g, s in sims)
            del sims
            base = summarise(tuple(eval_draw(d, rp, scn, "assist", 1.0, 1.0) for d, rp in zip(ds, routes)), procs, avail)
            base_modal = {pid: base["per"][pid]["modal_gross"] for pid in v2.SPONSOR_PROCS}
            rows += headline_rows(scn, aid, "assist", "calibrated", base, base_modal)
            rows += process_rows(scn, aid, "assist", "calibrated", base)
            msg = [f"assist C1st={base['mean_p_first_gross']:.4f} pool={base['pool_q']['p50']:,.0f}"]
            for m in M_HEADLINE:
                for variant in ("route", "hybrid"):
                    sm = summarise(tuple(eval_draw(d, rp, scn, variant, m, 1.0) for d, rp in zip(ds, routes)), procs, avail)
                    cell = f"main_m{m:g}"
                    rows += headline_rows(scn, aid, variant, cell, sm, base_modal) + process_rows(scn, aid, variant, cell, sm)
                    msg.append(f"{variant}/m{m:g} C1st={sm['mean_p_first_gross']:.4f} pool={sm['pool_q']['p50']:,.0f}")
            print(f"{scn:<20} {aid:<10} " + " | ".join(msg), flush=True)
            if scn == SWEEP_SCENARIO and aid in SWEEP_ARCHETYPES:
                for par, vals in SWEEPS:
                    for val in vals:
                        rs = cell_routes(routes, par, val)
                        m = val if par == "m" else 1.0
                        fcm = val if par == "fc_mult" else 1.0
                        sm = summarise(tuple(eval_draw(d, rp, scn, "route", m, fcm) for d, rp in zip(ds, rs)), procs, avail)
                        rows += headline_rows(scn, aid, "route", f"sweep_{par}={val:g}" + ("" if par == "m" else "_m1"),
                                              sm, base_modal)
                        rows += [r for r in process_rows(scn, aid, "route", f"sweep_{par}={val:g}" + ("" if par == "m" else "_m1"), sm)
                                 if r["process_id"] in ("P03", "P07", "P11", "P14") and r["metric"] in
                                 ("p_C_rank_first_gross", "p_C_net_positive")]
                if aid == "NAT_LARGE":
                    for hv in GRID_H:
                        for ev in GRID_E:
                            rs = tuple({**r, "h": hv, "e": ev} for r in routes)
                            sm = summarise(tuple(eval_draw(d, rp, scn, "route", 1.0, 1.0) for d, rp in zip(ds, rs)), procs, avail)
                            cell = f"grid_h={hv:g}_e={ev:g}_m1"
                            rows += [row(scn, aid, "route", cell, "mean_p_C_rank_first_gross_P01_P15", sm["mean_p_first_gross"], "prob"),
                                     row(scn, aid, "route", cell, "sponsor_ai_gross_value_p50", sm["pool_q"]["p50"], "usd/yr"),
                                     row(scn, aid, "route", cell, "p_C_net_positive", sm["per"]["P07"]["p_net_pos"], "prob", "P07"),
                                     row(scn, aid, "route", cell, "p_vendor_breakeven_le_available", sm["p_be_le_avail"], "prob")]
    for m in M_HEADLINE:
        net = network_rows(procs, sponsors, SWEEP_SCENARIO, min(args.net_draws, args.draws), m, routes[:args.net_draws])
        rows += net
        print("network m=%g " % m + "; ".join(f"{r['variant']}/{r['process_id']}={r['value']}" for r in net
                                              if r["metric"] == "p_breakeven_reachable"), flush=True)
    write_csv(args.out, rows)
    print(f"wrote {len(rows)} rows -> {os.path.relpath(args.out, v2.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
