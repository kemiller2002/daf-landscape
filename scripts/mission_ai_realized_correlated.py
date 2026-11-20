#!/usr/bin/env python3
"""Routing h realization (P-G0403-01-05) and correlated realization (P-G0403-01-04). TASKID g0403-0105-04.

Imports scripts/mission_ai_a_calibrated.py UNCHANGED (and through it mission_ai_bd_recut.py, the routing variant, the
calibrated model and v2, all unchanged). It rebuilds exactly the same draws: calibrated Random(42), routing
Random(42 + 104729), recut Random(42 + 15485863), whose three uniforms drive r_B, r_D and r_A. Two NEW streams are added
and leave every existing draw untouched:
  RC_SEED     = 42 + 32452843  one uniform per draw for the routing realization factor r_C (part A)
  FACTOR_SEED = 42 + 49979687  one standard normal per draw: the common sponsor-execution factor Z (part B)

(A) P-G0403-01-05: realization on the upper half of routing h.
  The A01 routing range h ~ U(0.20, 0.80) has a lower half supported by the bank's ~20% auto-close test set-up (CB-02),
  E19's 0.21-0.49 and the OCBC benchmark's 0.28-0.49 (CB-04), and an upper half that rests on E15's retrospective 0.78
  (CB-01c) and the State Dept's self-reported 80% (CB-05). Wave 37C noted that B and D take an audited-realization cut
  and the upper half of h does not. Realized h:
      h_eff = min(h, H_SPLIT) + r_C * max(0, h - H_SPLIT),   H_SPLIT = 0.50 (midpoint of the A01 range)
  r_C is drawn once per draw (sponsor level, all processes), as r_B is. C_route / C_hybrid use h_eff in place of h
  (cases not realized as AI-closed return to humans; under hybrid they receive assistance).
  C realization specs [I = inference]
    C_V1          r_C = 1 (replication of g0403-01).
    C_UPPER_FIELD r_C ~ tri(0.07, 0.33, 1.00) on the upper half: the HUD OIG / GSA OIG RPA realized-vs-estimated range
                  used for B (BD-E01, BD-E02) [I mapping]. State's 80% is an agency-claimed saving of the kind the GSA
                  audit found off-estimate for 9 of 10 bots; E15's 0.78 is ex-ante (retrospective validation).
    C_UPPER_WIDE  r_C ~ U(0.07, 1.00) on the upper half: ignorance sweep matching BD_WIDE [I].
    C_ALL_FIELD   h_eff = r_C * h with r_C ~ tri(0.07, 0.33, 1.00) on the WHOLE range [I stress]: the lower half is also
                  test-set-up / benchmark / optimal-policy evidence, not audited production realization.
    SWEEP_RC      fixed r_C in R_C_SWEEP on the upper half (r_C = 0 caps h at 0.50).
  ROUTE_G04 (h <= 0.49) has no upper half above 0.50, so it is unaffected by construction and is not re-run in part A.

(B) P-G0403-01-04: correlated realization via a Gaussian copula (stdlib statistics.NormalDist).
  For draw n with recut uniforms (u_B, u_D, u_A), r_C uniform u_C and common factor Z_n:
      X_i = sqrt(rho) * Z_n + sqrt(1 - rho) * Phi^-1(u_i),   U_i = Phi(X_i),   r_i = F_i^-1(U_i)
  so each r_i keeps its marginal (BD_FIELD, A_FIELD, ...) and every pair has Gaussian-copula Pearson correlation rho on
  the latent scale. Target Spearman rank correlation rho_s maps to rho = 2 sin(pi rho_s / 6) (0.5 -> 0.5176; 1 -> 1).
  At rho_s = 1 all U_i = Phi(Z_n) (comonotone). At rho_s = 0 U_i = u_i, which reproduces the independent baseline.
  The idiosyncratic normals are the existing recut uniforms, so draws are common random numbers across rho_s.
  Sets: ABD (r_A, r_B, r_D on the factor, r_C = 1) and ABCD (also r_C under C_UPPER_FIELD on the factor).
  Note: comonotone r_A and r_B are NOT equal values (different marginals). Equal values arise with A_RPA_ANALOGY at
  rho_s = 1 (same marginal as r_B, r_D), the recut's "one common realization factor" case.

Outputs (new file): data/mission-2026-11-14/ai-ranking-realized-correlated-2026-11-20.csv
Replication: rows with c_real = C_V1 and rank_corr = 0 are compared with ai-ranking-a-calibrated-2026-11-20.csv
(record_type = replication rows give the number of values compared and mismatched).
Usage: python3 scripts/mission_ai_realized_correlated.py . [--draws 10000] [--archetypes NAT_LARGE,...]
Stdlib only; functional style (pure functions; I/O only in main / read / write).
"""
from __future__ import annotations

import argparse
import bisect
import csv
import math
import os
import random
import statistics
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_ai_a_calibrated as ac  # noqa: E402

bd, rv, cal, v2 = ac.bd, ac.rv, ac.cal, ac.v2
OUT_CSV = os.path.join(v2.DATA, "ai-ranking-realized-correlated-2026-11-20.csv")
BASE_CSV = ac.OUT_CSV
SCENARIO = ac.SCENARIO
RC_SEED = v2.SEED + 32452843
FACTOR_SEED = v2.SEED + 49979687
H_SPLIT = 0.50
R_C_SWEEP = (1.0, 0.75, 0.50, 0.33, 0.20, 0.07, 0.0)
RANK_CORRS = (0.0, 0.5, 1.0)
DETAIL_ARCHETYPES = ("NAT_LARGE",)
NORMAL = statistics.NormalDist()
OPTS = ac.OPTS

C_BY_ID = {c["id"]: c for c in ac.C_VARIANTS}
ROUTE_CVS = tuple(C_BY_ID[i] for i in ("ROUTE_A01_M1.56", "ROUTE_A01_M1.77", "ROUTE_A01_M9.28", "HYBRID_A01_M1.77"))
CORR_CVS = tuple(C_BY_ID[i] for i in ("ASSIST", "ROUTE_G04_M1.77")) + ROUTE_CVS
A_BY_ID = {s["id"]: s for s in ac.A_SPECS}
BD_BY_ID = ac.BD_BY_ID
C_REAL = (
    {"id": "C_V1", "mode": None, "dist": None, "note": "r_C = 1 (replication of g0403-01)"},
    {"id": "C_UPPER_FIELD", "mode": "upper", "dist": ("tri", bd.R_FIELD),
     "note": "h above 0.50 realized at r_C ~ tri(0.07,0.33,1.0): HUD/GSA OIG RPA realized/estimated (BD-E01/E02) [I mapping]"},
    {"id": "C_UPPER_WIDE", "mode": "upper", "dist": ("uni", (0.07, 1.0)),
     "note": "h above 0.50 realized at r_C ~ U(0.07,1.0): ignorance sweep as BD_WIDE [I]"},
    {"id": "C_ALL_FIELD", "mode": "all", "dist": ("tri", bd.R_FIELD),
     "note": "whole h realized at r_C ~ tri(0.07,0.33,1.0) [I stress]"},
)
CR_BY_ID = {c["id"]: c for c in C_REAL}
AB_COMBOS_A = (("A_V1", "V1_PRIORS"), ("A_V1", "BD_FIELD"), ("A_FIELD", "BD_FIELD"), ("A_RPA_ANALOGY", "BD_FIELD"))
AB_COMBOS_B = (("A_FIELD", "V1_PRIORS"), ("A_FIELD", "BD_FIELD"), ("A_FIELD", "BD_WIDE"), ("A_RPA_ANALOGY", "BD_FIELD"))
COLS = ("record_type", "study", "scenario", "c_variant", "c_real", "bd_variant", "a_variant", "corr_set", "rank_corr",
        "archetype", "cell", "process_id", "intervention", "metric", "value", "lo", "hi", "unit", "note")


# ------------------------------------------------------------------------------------------- pure draws
def clamp(u: float) -> float:
    return min(1.0 - 1e-12, max(1e-12, u))


def latent_rho(rank_corr: float) -> float:
    """Gaussian-copula Pearson correlation giving Spearman rank correlation rank_corr."""
    return 1.0 if rank_corr >= 1.0 else 2.0 * math.sin(math.pi * rank_corr / 6.0)


def copula_u(us: Sequence[float], z: float, rho: float) -> tuple[float, ...]:
    """Map independent uniforms to uniforms loading sqrt(rho) on a common standard normal z."""
    if rho <= 0.0:
        return tuple(us)
    if rho >= 1.0:
        uc = NORMAL.cdf(z)
        return tuple(uc for _ in us)
    a, b = math.sqrt(rho), math.sqrt(1.0 - rho)
    return tuple(NORMAL.cdf(a * z + b * NORMAL.inv_cdf(clamp(u))) for u in us)


def rc_stream(n: int) -> tuple[float, ...]:
    rng = random.Random(RC_SEED)
    return tuple(rng.random() for _ in range(n))


def factor_stream(n: int) -> tuple[float, ...]:
    rng = random.Random(FACTOR_SEED)
    return tuple(NORMAL.inv_cdf(clamp(rng.random())) for _ in range(n))


def h_eff(h: float, rC: float, mode: str | None) -> float:
    if mode is None:
        return h
    if mode == "all":
        return h * rC
    return min(h, H_SPLIT) + rC * max(0.0, h - H_SPLIT)


def realized_route(rp: Mapping | None, rC: float, mode: str | None) -> Mapping | None:
    return rp if rp is None or mode is None else {**rp, "h": h_eff(rp["h"], rC, mode)}


def c_vals(ds, cv, routes, rCs, mode) -> tuple[dict, ...]:
    return tuple(bd.c_values(d, cv, realized_route(rp, rc, mode), SCENARIO) for d, rp, rc in zip(ds, routes, rCs))


def ranks(xs: Sequence[float]) -> list[float]:
    """Average ranks (ties share the mean rank)."""
    sv = sorted(xs)
    return [(bisect.bisect_left(sv, x) + bisect.bisect_right(sv, x) - 1) / 2.0 for x in xs]


def spearman(xs: Sequence[float], ys: Sequence[float]) -> float:
    rx, ry = ranks(xs), ranks(ys)
    mx, my = statistics.fmean(rx), statistics.fmean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den > 0 else float("nan")


# ------------------------------------------------------------------------------------------- rows (pure)
def tag(rows: Sequence[Mapping], **kw) -> list[dict]:
    return [{**{c: "" for c in COLS}, **r, **kw} for r in rows]


def summarise_cell(ds, cvals, aspec, bdspec, rus, avail):
    return bd.summarise(tuple(ac.eval_cell(d, cvl, aspec, bdspec, ru) for d, cvl, ru in zip(ds, cvals, rus)), avail)


def changed_row(base_ms: str, ms: str) -> tuple[float, str]:
    diff = [f"P{i + 1:02d}:{a}->{b}" for i, (a, b) in enumerate(zip(base_ms, ms)) if a != b]
    return float(len(diff)), ";".join(diff)


def extra_rows(sm_ref, sm, cv, bdv, av, arch, cell, ref_label) -> list[dict]:
    n, note = changed_row(ac.modal_string(sm_ref), ac.modal_string(sm))
    return [ac.row(cv, bdv, av, arch, cell, "n_processes_modal_changed_gross", n, "count", note=f"vs {ref_label}: {note}")]


# ------------------------------------------------------------------------------------------- run (pure given inputs)
def run_archetype(idx, a, procs, anchor, draws) -> tuple[list[dict], list[str]]:
    spec = next(s for s in cal.CAL_SPECS if s["id"] == SCENARIO)
    sims = cal.simulate(a, idx, procs, anchor, draws, spec, "v2", {})
    ds = tuple(bd.compact_plus(SCENARIO, g, s, procs) for g, s in sims)
    del sims
    routes = {"G04": rv.route_stream(draws), "A01": bd.route_stream_a01(draws), None: (None,) * draws}
    rus = bd.recut_stream(draws)
    ucs = rc_stream(draws)
    zs = factor_stream(draws)
    aid, avail = a["id"], anchor["available_n"]
    detail = aid in DETAIL_ARCHETYPES
    rows, log = [], []
    fmt = lambda sm: " ".join(f"{i}={sm['mean_pg'][i]:.3f}" for i in OPTS) + " modal " + ac.modal_string(sm)  # noqa: E731

    # ---------------- copula uniforms (B, D, A, C) per rank correlation
    cu = {rs: tuple(copula_u((ru[0], ru[1], ru[2], uc), z, latent_rho(rs)) for ru, uc, z in zip(rus, ucs, zs))
          for rs in RANK_CORRS}
    for rs in RANK_CORRS:
        rB = [bd.draw_r(u[0], ("tri", bd.R_FIELD)) for u in cu[rs]]
        rD = [bd.draw_r(u[1], ("tri", bd.R_FIELD)) for u in cu[rs]]
        rA = [bd.draw_r(u[2], ("tri", ac.R_A_FIELD)) for u in cu[rs]]
        rC = [bd.draw_r(u[3], ("tri", bd.R_FIELD)) for u in cu[rs]]
        sp = {"rA_rB": spearman(rA, rB), "rB_rD": spearman(rB, rD), "rA_rD": spearman(rA, rD), "rC_rB": spearman(rC, rB)}
        maxdiff = max(max(abs(x - y) for x, y in zip(c[:3], ru)) for c, ru in zip(cu[rs], rus))
        rows += tag([ac.row("meta", "meta", "meta", aid, f"corr_rs={rs:g}", f"spearman_{k}", v, "rho",
                            note="empirical Spearman of drawn r (BD_FIELD / A_FIELD / C_UPPER_FIELD marginals)",
                            record_type="meta", scn="ALL") for k, v in sp.items()],
                    study="B_CORR", rank_corr=rs, corr_set="ABCD")
        rows += tag([ac.row("meta", "meta", "meta", aid, f"corr_rs={rs:g}", "max_abs_u_shift_vs_recut", maxdiff, "",
                            note="max |U_i - u_i| over draws for B, D, A uniforms", record_type="meta", scn="ALL")],
                    study="B_CORR", rank_corr=rs, corr_set="ABCD")
        log.append(f"{aid} rs={rs:g} latent={latent_rho(rs):.4f} " + " ".join(f"{k}={v:.3f}" for k, v in sp.items())
                   + f" max|U-u|={maxdiff:.2e}")

    # ---------------- part A: realization on routing h (independent draws, existing uniforms)
    for cv in ROUTE_CVS:
        base_sm = {}
        for cr in C_REAL:
            rCs = tuple(bd.draw_r(u, cr["dist"]) for u in ucs)
            cvals = c_vals(ds, cv, routes[cv["ranges"]], rCs, cr["mode"])
            for av, bdv in AB_COMBOS_A:
                sm = summarise_cell(ds, cvals, A_BY_ID[av], BD_BY_ID[bdv], rus, avail)
                base_sm.setdefault((av, bdv), sm)
                rows += tag(ac.cell_rows(cv["id"], bdv, av, aid, "main", sm, detail),
                            study="A_HCUT", c_real=cr["id"], corr_set="independent", rank_corr=0.0)
                rows += tag(extra_rows(base_sm[(av, bdv)], sm, cv["id"], bdv, av, aid, "main", "C_V1"),
                            study="A_HCUT", c_real=cr["id"], corr_set="independent", rank_corr=0.0)
                log.append(f"A {aid:<9} {cv['id']:<16} {cr['id']:<13} {av:<13} {bdv:<9} " + fmt(sm))
        for r in R_C_SWEEP:
            cvals = c_vals(ds, cv, routes[cv["ranges"]], (r,) * draws, "upper")
            sm = summarise_cell(ds, cvals, A_BY_ID["A_FIELD"], BD_BY_ID["BD_FIELD"], rus, avail)
            rows += tag(ac.cell_rows(cv["id"], "BD_FIELD", "A_FIELD", aid, f"sweep_rC={r:g}", sm, False),
                        study="A_HCUT", c_real="SWEEP_RC", corr_set="independent", rank_corr=0.0)
            log.append(f"A {aid:<9} {cv['id']:<16} SWEEP_RC r={r:<5g} A_FIELD×BD_FIELD " + fmt(sm))

    # ---------------- part B: correlated r_A, r_B, r_D (and r_C)
    for cv in CORR_CVS:
        cvals = c_vals(ds, cv, routes[cv["ranges"]], (1.0,) * draws, None)
        ref = {}
        for rs in RANK_CORRS:
            rus_c = tuple(u[:3] for u in cu[rs])
            sms = {}
            for av, bdv in AB_COMBOS_B:
                sm = summarise_cell(ds, cvals, A_BY_ID[av], BD_BY_ID[bdv], rus_c, avail)
                sms[(av, bdv)] = sm
                ref.setdefault((av, bdv), sm)
                rows += tag(ac.cell_rows(cv["id"], bdv, av, aid, "main", sm, detail),
                            study="B_CORR", c_real="C_V1", corr_set="ABD", rank_corr=rs)
                rows += tag(extra_rows(ref[(av, bdv)], sm, cv["id"], bdv, av, aid, "main", "rank_corr=0"),
                            study="B_CORR", c_real="C_V1", corr_set="ABD", rank_corr=rs)
                log.append(f"B {aid:<9} {cv['id']:<16} rs={rs:<3g} {av:<13} {bdv:<9} " + fmt(sm))
            ab = ac.absorption(sms[("A_FIELD", "V1_PRIORS")], sms[("A_FIELD", "BD_FIELD")])
            rows += tag(ac.absorption_rows(cv["id"], "A_FIELD", aid, ab), study="B_CORR", c_real="C_V1",
                        corr_set="ABD", rank_corr=rs)
            log.append(f"  absorption {cv['id']} rs={rs:g}: lost_BD={ab['lost_BD']:.3f} share_A={ab['share_A']:.3f} "
                       f"share_C={ab['share_C']:.3f}")
        if cv["kind"] == "assist" or cv["ranges"] != "A01":
            continue
        cr = CR_BY_ID["C_UPPER_FIELD"]
        ref_c = None
        for rs in RANK_CORRS:
            rCs = tuple(bd.draw_r(u[3], cr["dist"]) for u in cu[rs])
            cvals_c = c_vals(ds, cv, routes[cv["ranges"]], rCs, cr["mode"])
            sm = summarise_cell(ds, cvals_c, A_BY_ID["A_FIELD"], BD_BY_ID["BD_FIELD"], tuple(u[:3] for u in cu[rs]), avail)
            ref_c = ref_c or sm
            rows += tag(ac.cell_rows(cv["id"], "BD_FIELD", "A_FIELD", aid, "main", sm, detail),
                        study="B_CORR", c_real=cr["id"], corr_set="ABCD", rank_corr=rs)
            rows += tag(extra_rows(ref_c, sm, cv["id"], "BD_FIELD", "A_FIELD", aid, "main", "rank_corr=0"),
                        study="B_CORR", c_real=cr["id"], corr_set="ABCD", rank_corr=rs)
            log.append(f"B {aid:<9} {cv['id']:<16} rs={rs:<3g} ABCD C_UPPER_FIELD A_FIELD×BD_FIELD " + fmt(sm))
    return rows, log


# ------------------------------------------------------------------------------------------- replication (pure)
REP_KEY = ("c_variant", "bd_variant", "a_variant", "archetype", "cell", "process_id", "intervention", "metric")


def as_num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return x


def replication(rows: Sequence[Mapping], base: Mapping) -> tuple[int, int, list[str]]:
    mine = [r for r in rows if r["record_type"] == "model" and r["c_real"] == "C_V1" and float(r["rank_corr"]) == 0.0
            and r["cell"] in ("main", "absorption") and r["metric"] != "n_processes_modal_changed_gross"]
    pairs = [(r, base.get(tuple(str(r[k]) for k in REP_KEY))) for r in mine]
    found = [(r, b) for r, b in pairs if b is not None]

    def same(x, y):
        x, y = as_num(x), as_num(y)
        return abs(x - y) <= 1e-6 * max(1.0, abs(y)) if isinstance(x, float) and isinstance(y, float) else str(x) == str(y)
    bad = [f"{'/'.join(str(r[k]) for k in REP_KEY)}: {r['value']} vs {b}" for r, b in found if not same(r["value"], b)]
    return len(found), len(bad), bad[:20]


def rep_rows(n_cmp, n_bad, arch_ids) -> list[dict]:
    return tag([ac.row("replication", "replication", "replication", ",".join(arch_ids), "main", k, float(v), "count",
                       note="rows with c_real=C_V1, rank_corr=0, cell=main vs ai-ranking-a-calibrated-2026-11-20.csv "
                            "(same c_variant, bd_variant, a_variant, archetype, process, intervention, metric); "
                            "floats within 1e-6 relative", record_type="replication", scn="ALL")
                for k, v in (("values_compared", n_cmp), ("values_mismatched", n_bad))], study="REPLICATION")


def spec_rows() -> list[dict]:
    out = tag([ac.row("spec", "spec", "spec", "ALL", "spec", "c_real_spec",
                      f"mode={c['mode']}; dist={c['dist']}; H_SPLIT={H_SPLIT:g}", note=c["note"], record_type="spec",
                      scn="ALL") | {"c_real": c["id"]} for c in C_REAL], study="A_HCUT")
    out += tag([ac.row("spec", "spec", "spec", "ALL", "spec", "corr_spec",
                       f"rank_corr={rs:g}; latent_pearson={latent_rho(rs):.6f}",
                       note="Gaussian copula: X_i = sqrt(rho) Z + sqrt(1-rho) Phi^-1(u_i); r_i = F_i^-1(Phi(X_i))",
                       record_type="spec", scn="ALL") | {"rank_corr": rs} for rs in RANK_CORRS], study="B_CORR")
    out += tag([ac.row("meta", "meta", "meta", "ALL", "meta", "seeds", "see note", record_type="meta", scn="ALL",
                       note=f"calibrated Random({v2.SEED}); routing Random({rv.ROUTE_SEED}); recut Random({bd.RECUT_SEED}) "
                            f"(u_B, u_D, u_A); r_C Random({RC_SEED}); factor Z Random({FACTOR_SEED}) via inv_cdf")])
    return out


# ------------------------------------------------------------------------------------------- I/O edge
def read_base(path: str) -> dict:
    with open(path, newline="", encoding="utf-8") as fh:
        return {tuple(r[k] for k in REP_KEY): r["value"] for r in csv.DictReader(fh)
                if r["record_type"] == "model" and r["scenario"] == SCENARIO}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (accepted for the repo CLI convention; unused)")
    ap.add_argument("--draws", type=int, default=10000)
    ap.add_argument("--out", default=OUT_CSV)
    ap.add_argument("--archetypes", default="NAT_LARGE,NAT_MID,CF_1BN,CF_250M,CF_SMALL")
    args = ap.parse_args(argv)
    procs = tuple(v2.v1_process(r) for r in v2.load_csv(v2.V1_CSV))
    sponsors = v2.load_sponsors(v2.load_csv(v2.COST_CSV))
    anchors = v2.grant_anchors(sponsors, v2.load_csv(v2.SUMMARY_CSV))
    keep = set(filter(None, args.archetypes.split(",")))
    arch = tuple((i, a) for i, a in enumerate(v2.ARCHETYPES) if a["id"] in keep)
    rows = spec_rows() + tag([ac.row("meta", "meta", "meta", "ALL", "meta", "draws", float(args.draws), "count",
                                     record_type="meta", scn="ALL")])
    for idx, a in arch:
        r, log = run_archetype(idx, a, procs, v2.archetype_anchor(a, sponsors, anchors), args.draws)
        rows += r
        print("\n".join(log), flush=True)
    n_cmp, n_bad, bad = replication(rows, read_base(BASE_CSV)) if args.draws == 10000 else (0, 0, ["draws != 10000"])
    rows += rep_rows(n_cmp, n_bad, [a["id"] for _, a in arch])
    print(f"replication vs {os.path.relpath(BASE_CSV, v2.ROOT)}: compared {n_cmp}, mismatched {n_bad}", *bad, sep="\n")
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {os.path.relpath(args.out, v2.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
