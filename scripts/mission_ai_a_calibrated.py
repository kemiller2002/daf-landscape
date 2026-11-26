#!/usr/bin/env python3
"""Manual improvement (A) held to the evidence standard already applied to B, C and D. Queue item P-G0403-01.

Why: the B/D recut (scripts/mission_ai_bd_recut.py, wave 37C) cut conventional automation (B) to RPA-audit realization
and redesign (D) to the same range by analogy, and found that manual improvement A = alpha * L, alpha ~ U(0.05, 0.25)
(an unsourced v1 prior), absorbed most of what B and D lost. This script imports mission_ai_bd_recut.py UNCHANGED,
rebuilds exactly the same draws (calibrated seed 42; routing 42 + 104729; recut 42 + 15485863) and changes only A,
using the evidence table embedded below (written to data/mission-2026-11-14/manual-improvement-evidence-2026-11-20.csv).

A specs [I = inference; evidence ids MI-E** refer to the evidence CSV]
  A_V1            alpha ~ U(0.05, 0.25), r_A = 1 (replication of the recut).
  A_RPA_ANALOGY   r_A ~ tri(0.07, 0.33, 1.00) on the recut's third uniform: identical to the recut's ABD_FIELD when
                  combined with BD_FIELD (replication check). RPA realization borrowed for manual work [I].
  A_FIELD         r_A ~ tri(0.475, 1.00, 1.20) [I mapping]: realized / planned throughput of manual casework
                  programmes audited by the NAO. MI-E01 DWP Targeted Case Review: cases per agent per day 0.57 vs 1.20
                  expected (2023-24) and 1.07 vs 0.89 (2024-25); cases completed 104% of plan. MI-E02 Home Office PACE
                  (process simplification, no new technology): 2.5 decisions per active caseworker per week planned and
                  achieved (April 2023), mode 1.0. No audit measures realized/planned LABOUR SAVINGS of a manual fix.
  A_FIELD_CAPPED  r_A ~ U(0.475, 1.00): as A_FIELD but no over-delivery [I].
  A_LEVEL_A       alpha ~ U(0.065, 0.091) [I stress]: only the peer-reviewed field level (MI-E04 Fenizia 2022,
                  Italian social-security back office: +10% output for a 1-SD better manager, +6.9% from reallocating
                  managers; as labour per unit 1 - 1/1.10 = 0.091 and 1 - 1/1.069 = 0.065). Mapped on the same uniform
                  as v1 alpha (common random numbers). r_A = 1.
  A_LEVEL_A_FIELD alpha as A_LEVEL_A and r_A as A_FIELD [I stress].
  The only other level datum, IOPC's self-reported 33% productivity in one team (MI-E03, 0.25 per unit), sits at v1's
  upper bound; together MI-E03/E04 neither narrow nor contradict U(0.05, 0.25), so A_V1's alpha range is kept as an
  [I] sweep in every spec except A_LEVEL_*.

B/D specs: V1_PRIORS, BD_FIELD, BD_WIDE, BD_PROGRAM from the recut (unchanged definitions).
C variants (current m: wave-39B central 1.56 OFAC analogue / 1.77 bank-SAR transfer; high 9.28 OFAC analogue):
  ASSIST; ROUTE_G04_M1.77; ROUTE_A01_M1 (replication); ROUTE_A01_M1.56; ROUTE_A01_M1.77; ROUTE_A01_M9.28;
  HYBRID_A01_M1.77.
Sweep SWEEP_RA: fixed r_A in R_A_SWEEP with BD_FIELD, alpha as v1.
Absorption: for a (C, A) pair, with D_x = mean over P01-P15 of P(x first, gross) under BD_FIELD minus V1_PRIORS,
  share_A = D_A / (-(D_B + D_D)) and share_C = D_C / (-(D_B + D_D)): the share of rank-first probability lost by B and D
  that goes to A (resp. C).

Outputs (new files): data/mission-2026-11-14/ai-ranking-a-calibrated-2026-11-20.csv and the evidence CSV.
Usage: python3 scripts/mission_ai_a_calibrated.py . [--draws 10000] [--archetypes NAT_LARGE,...]
Stdlib only; functional style (pure functions; I/O only in main / write_csv).
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_ai_bd_recut as bd  # noqa: E402

rv, cal, v2 = bd.rv, bd.cal, bd.v2
OUT_CSV = os.path.join(v2.DATA, "ai-ranking-a-calibrated-2026-11-20.csv")
EVIDENCE_CSV = os.path.join(v2.DATA, "manual-improvement-evidence-2026-11-20.csv")
SCENARIO = "CAL_CENTRAL"
ALPHA_V1 = (0.05, 0.25)
R_A_FIELD = (0.475, 1.00, 1.20)
R_A_SWEEP = (1.20, 1.00, 0.75, 0.50, 0.33, 0.20, 0.07)
DETAIL_ARCHETYPES = ("NAT_LARGE",)

A_SPECS = (
    {"id": "A_V1", "alpha": None, "rA": None, "note": "v1 alpha ~ U(0.05,0.25), r_A = 1 (replication)"},
    {"id": "A_RPA_ANALOGY", "alpha": None, "rA": ("tri", bd.R_FIELD),
     "note": "r_A ~ tri(0.07,0.33,1.0), RPA audits by analogy (= recut ABD_FIELD with BD_FIELD) [I]"},
    {"id": "A_FIELD", "alpha": None, "rA": ("tri", R_A_FIELD),
     "note": "r_A ~ tri(0.475,1.0,1.2): NAO manual-casework realized/planned throughput (MI-E01, MI-E02) [I mapping]"},
    {"id": "A_FIELD_CAPPED", "alpha": None, "rA": ("uni", (0.475, 1.00)),
     "note": "r_A ~ U(0.475,1.0): as A_FIELD without over-delivery [I]"},
    {"id": "A_LEVEL_A", "alpha": (0.065, 0.091), "rA": None,
     "note": "alpha ~ U(0.065,0.091): peer-reviewed field level only (MI-E04) [I stress]"},
    {"id": "A_LEVEL_A_FIELD", "alpha": (0.065, 0.091), "rA": ("tri", R_A_FIELD),
     "note": "alpha as A_LEVEL_A, r_A as A_FIELD [I stress]"},
)
BD_IDS = ("V1_PRIORS", "BD_FIELD", "BD_WIDE", "BD_PROGRAM")
BD_BY_ID = {s["id"]: s for s in bd.BD_SPECS}
C_VARIANTS = (
    {"id": "ASSIST", "kind": "assist", "ranges": None, "m": 1.0},
    {"id": "ROUTE_G04_M1.77", "kind": "route", "ranges": "G04", "m": 1.77},
    {"id": "ROUTE_A01_M1", "kind": "route", "ranges": "A01", "m": 1.0},
    {"id": "ROUTE_A01_M1.56", "kind": "route", "ranges": "A01", "m": 1.56},
    {"id": "ROUTE_A01_M1.77", "kind": "route", "ranges": "A01", "m": 1.77},
    {"id": "ROUTE_A01_M9.28", "kind": "route", "ranges": "A01", "m": 9.28},
    {"id": "HYBRID_A01_M1.77", "kind": "hybrid", "ranges": "A01", "m": 1.77},
)
OPTS = bd.OPTS

# ------------------------------------------------------------------------------------------- evidence table (data)
# id, domain, intervention_type, source, year, url, retrieved_via, quote, parameter, value, value_basis, grade,
# limitations, model_use
EVIDENCE = (
    ("MI-E01", "Benefit compliance review (UK Universal Credit), manual casework with rule-based triage",
     "triage rules + manual review programme; realized vs planned",
     "National Audit Office, Tackling benefit overpayments due to fraud and error, HC 1336, Session 2024-2026 (Oct 2025), paras 3.18, 3.27-3.28, Figure 9",
     "2025", "https://www.nao.org.uk/wp-content/uploads/2025/10/Tackling-benefit-overpayments-due-to-fraud-and-error.pdf",
     "nao.org.uk PDF (robots allowed)",
     "Agents are allocated cases for review based on rules that are generated by using data and analytics to look for activity, behaviour or "
     "circumstances that suggest a higher risk of error. | Average productivity: the number of cases reviewed per agent per day was 1.07 in "
     "2024-25, above DWP's expectation of 0.89. This was an improvement on the previous year when average productivity fell short of "
     "expectation. | Figure 9, 2023-24: average productivity expected 1.20, actual 0.57 | Cases completed: 1,151,000 cases were reviewed "
     "from 2022-23 to 2024-25, 104% of DWP's expectation of 1,104,000. | In 2024-25, the hit rate was 20%, which was less than the "
     "expectation of 24%. | DWP achieved an estimated £581 million in AME savings from TCR, 11% more than its expectation of £525 million",
     "r_A (realized / planned throughput of a manual compliance process)",
     "productivity 0.57/1.20 = 0.475 (2023-24); 1.07/0.89 = 1.202 (2024-25); cases 1,151/1,104 = 1.043; hit rate 0.20/0.24 = 0.833; "
     "savings 581/525 = 1.107", "F/C", "A",
     "Throughput of a new manual review programme against its own plan, not labour saved by improving an existing process; triage rules are "
     "built with data analytics; outsourced agents; savings are benefit outcomes (AME), not admin cost; DWP management information analysed by NAO",
     "A_FIELD lower bound 0.475 and upper bound 1.20; mode 1.0 with MI-E02"),
    ("MI-E02", "Asylum casework (UK Home Office), eligibility decisions",
     "process simplification (PACE: questionnaires, cohort rules, withdrawal rules), consultant-led; realized vs planned",
     "National Audit Office, The asylum and protection transformation programme, HC 1375, Session 2022-23 (June 2023), Figure 9, paras 3.9, 3.12",
     "2023", "https://www.nao.org.uk/wp-content/uploads/2023/06/the-asylum-and-protection-transformation-programme.pdf",
     "nao.org.uk PDF (robots allowed)",
     "The Programme will increase caseworker weekly decisions from its July 2022 performance of 1.4 to 2.5. | established the Prioritising "
     "Asylum Customers' Experience (PACE) project to simplify decision-making and improve productivity. It engaged consultants, Newton, to "
     "support this work, on a contract worth £24 million. The Home Office hoped to increase productivity so each caseworker made an average "
     "of 2.5 decisions a week by the end of May 2023. In April 2023, the 640 active caseworkers (those making decisions) achieved the 2.5 "
     "decisions weekly. | 72% of decisions in April 2023 were 'administrative decisions' | The Infrastructure and Projects Authority (IPA) "
     "reported that there was an acknowledgement within the Home Office that publicly stated targets around productivity levels of "
     "caseworkers are not realistic.",
     "r_A (realized / planned productivity gain of a non-technology process fix)",
     "headline (2.5-1.4)/(2.5-1.4) = 1.00 among active caseworkers; planned gain 2.5/1.4 = 1.79x", "F/C", "A",
     "Headline met largely through administrative decisions (withdrawals; 72% in April 2023), so labour per substantive decision is not "
     "measured; only ~50% of caseworkers were deciding claims; not finance; consultants' cost £24m",
     "A_FIELD mode 1.0 (headline realization of the planned productivity)"),
    ("MI-E03", "Complaint-review casework (UK Independent Office for Police Conduct)",
     "workload balancing / self-organising allocation of cases; agency self-report",
     "National Audit Office, Improving operational delivery in government: a good practice guide for senior leaders (March 2021), IOPC case; "
     "repeated in NAO, Efficiency in government, HC 303, Session 2021-22 (July 2021), Figure 7",
     "2021", "https://www.nao.org.uk/wp-content/uploads/2021/03/Improving-operational-delivery-in-government-main.pdf",
     "nao.org.uk PDF (robots allowed); also https://www.nao.org.uk/wp-content/uploads/2021/07/Efficiency-in-government.pdf",
     "The leadership team experimented with giving casework teams ownership of how to manage their workload. | Total output has remained the "
     "same despite fewer people working in the team and spending more time on project work and additional responsibilities. IOPC says that "
     "productivity in one casework team may have increased by 33% compared with 12 months ago.",
     "alpha (end-state labour saving per unit of output)", "1 - 1/1.33 = 0.248 per unit [C]", "F/C", "C",
     "Self-report ('may have increased'), one team, no denominator or method; measured over the 12 months before March 2021 (edge of the "
     "2021+ window); complaint review, not finance",
     "Not used to set a range; consistent with v1 alpha upper bound 0.25"),
    ("MI-E04", "Social-security claims processing back office (Italy, INPS)",
     "management quality / allocation of managers (no technology change); peer-reviewed, administrative output data",
     "Fenizia A. Managers and Productivity in the Public Sector. Econometrica 90(3):1063-1084 (May 2022), doi:10.3982/ECTA19244",
     "2022", "https://www.econometricsociety.org/publications/econometrica/2022/05/01/managers-and-productivity-public-sector",
     "econometricsociety.org abstract page (robots allowed); full text not read",
     "Exploiting the rotation of managers across sites, I find that a one standard deviation increase in managerial talent raises office "
     "productivity by 10%. These gains are driven primarily by the exit of older workers who retire when more productive managers take over. "
     "| assigning better managers to the largest and most productive offices would increase output by at least 6.9%.",
     "alpha (end-state labour saving per unit of output)", "1 - 1/1.10 = 0.091; 1 - 1/1.069 = 0.065 per unit [C]", "F/C", "A",
     "Management effect, mostly via composition (retirements), not a process fix; output-based productivity on claims; Italy; abstract only",
     "A_LEVEL_A alpha ~ U(0.065, 0.091) [I stress]"),
    ("MI-E05", "Accounts payable (City of Monroe, WA)", "kaizen: roles, reference guide, flowcharts; auditor-run Lean service",
     "Washington State Auditor's Office, Center for Government Innovation, City of Monroe: AP Process Improvement Success (Aug 2025)",
     "2025", "https://sao.wa.gov/sites/default/files/2025-11/Lean%20Case%20Study%20Monroe_August%202025_1.pdf",
     "sao.wa.gov PDF (robots allowed)",
     "Just one month after the kaizen, Monroe saw strong progress in their AP processes. Most notably, agency staff: Increased compliance "
     "with reconciled transactions by 86% | Now consistently submit 98% of receipts within one day of purchase",
     "none (quality / compliance outcome; no labour or time measure)", "no labour measure", "F", "C",
     "One month after; base not stated for the 86%; facilitator's own case study", "Not used: no alpha or r_A information"),
    ("MI-E06", "HR hiring and onboarding (two WA school districts)", "kaizen: standard forms, checklists, focus time, exception rules",
     "Washington State Auditor's Office, Case study: Faster, clearer hiring and onboarding through Lean process improvement (April 2026)",
     "2026", "https://sao.wa.gov/sites/default/files/2026-05/FINAL_2026%20Lean%20Case%20Study%20Clover%20Park%20Bellingham.pdf",
     "sao.wa.gov PDF (robots allowed)",
     "Updated and standardized forms and checklists | Set protected focus time for file processing | Both Clover Park and Bellingham staff "
     "reported faster workflows, fewer mistakes and clearer expectations",
     "none (no quantified outcome)", "no number reported", "F", "C",
     "Qualitative; staff-reported; not finance", "Not used: shows that auditor-facilitated Lean work publishes no labour denominators"),
    ("MI-E07", "Payment processing (Malaysian government-linked company)", "Lean / kaizen, value-stream mapping",
     "Duriraj B. Transforming payment processing through lean and kaizen management: a Malaysian public service perspective. Global Business "
     "Management Review 17(1):63-95 (2025), doi:10.32890/gbmr2025.17.1.4",
     "2025", "https://e-journal.uum.edu.my/index.php/gbmr/article/view/26274", "journal PDF (robots allowed)",
     "SLA performance scores fluctuating between 54.68% and 95.16% from January to July 2020 | SLA performance stabilized above 82% | "
     "direct treatment lead time, which was streamlined from six steps to four",
     "none (step count and SLA; no labour or time measure)", "steps 6 -> 4; SLA > 0.82", "F", "C",
     "Single case, baseline 2020, no labour measure, no counterfactual", "Not used"),
    ("MI-REF", "Conventional automation (RPA), US federal back office (comparator, from the recut)",
     "RPA realized vs estimated (BD-E01 HUD OIG 2023; BD-E02 GSA OIG 2023)",
     "See data/mission-2026-11-14/ai-bd-recut-2026-11-19.csv record_type=evidence BD-E01, BD-E02", "2023",
     "https://www.hudoig.gov/sites/default/files/2023-02/2021-OE-0007.pdf", "repo (not re-fetched)",
     "annual labor hour savings totaled approximately 1,015, or 7 percent of the amount HUD estimated | users reported time savings only "
     "averaged approximately 30 minutes [of 90]",
     "r_B (comparator)", "0.07 program; 0.33 one GSA bot", "F", "A", "Technology programme; as in the recut",
     "A_RPA_ANALOGY (= ABD_FIELD)"),
)
EVIDENCE_COLS = ("evidence_id", "domain", "intervention_type", "source", "year", "url", "retrieved_via", "quote", "parameter",
                 "value", "value_basis", "grade", "limitations", "model_use", "retrieved_on")


# ------------------------------------------------------------------------------------------- pure transforms
def alpha_u(a_val: float, L: float) -> float:
    """Recover the v1 alpha uniform from A = alpha * L (alpha = 0.05 + 0.20 u)."""
    alpha = a_val / L if L > 0 else ALPHA_V1[0]
    return min(1.0, max(0.0, (alpha - ALPHA_V1[0]) / (ALPHA_V1[1] - ALPHA_V1[0])))


def a_value(cp: Mapping, spec: Mapping, rA: float) -> float:
    a0, L = cp["others"]["A"], cp["L"]
    alpha = v2.uni(alpha_u(a0, L), *spec["alpha"]) if spec["alpha"] else (a0 / L if L > 0 else 0.0)
    return alpha * L * rA


def with_a(d: Mapping, spec: Mapping, rA: float) -> dict:
    return {**d, "procs": tuple({**cp, "others": {**cp["others"], "A": a_value(cp, spec, rA)}} for cp in d["procs"])}


def eval_cell(d: Mapping, cvals: Mapping, aspec: Mapping, bdspec: Mapping, ru: Sequence[float],
              fixed_rA: float | None = None) -> dict:
    rA = fixed_rA if fixed_rA is not None else bd.draw_r(ru[2], aspec["rA"])
    return bd.eval_draw(with_a(d, aspec, rA), cvals, bdspec, ru)


def absorption(sm_v1: Mapping, sm_bd: Mapping) -> dict:
    delta = {i: sm_bd["mean_pg"][i] - sm_v1["mean_pg"][i] for i in OPTS}
    lost = -(delta["B"] + delta["D"])
    return {"lost_BD": lost, "dA": delta["A"], "dC": delta["C"],
            "share_A": delta["A"] / lost if lost > 1e-12 else float("nan"),
            "share_C": delta["C"] / lost if lost > 1e-12 else float("nan")}


# ------------------------------------------------------------------------------------------- rows (pure)
COLS = ("record_type", "scenario", "c_variant", "bd_variant", "a_variant", "archetype", "cell", "process_id", "intervention",
        "metric", "value", "lo", "hi", "unit", "note")


def row(cvar, bdv, av, arch, cell, metric, value, unit="", process_id="", intervention="", lo=None, hi=None, note="",
        record_type="model", scn=SCENARIO) -> dict:
    rnd = lambda x: round(x, 6) if isinstance(x, float) and math.isfinite(x) else x  # noqa: E731
    return {"record_type": record_type, "scenario": scn, "c_variant": cvar, "bd_variant": bdv, "a_variant": av,
            "archetype": arch, "cell": cell, "process_id": process_id, "intervention": intervention, "metric": metric,
            "value": rnd(value), "lo": rnd(lo) if lo is not None else "", "hi": rnd(hi) if hi is not None else "",
            "unit": unit, "note": note}


def modal_string(sm: Mapping) -> str:
    return "".join(sm["per"][p]["modal_gross"] for p in v2.SPONSOR_PROCS)


def cell_rows(cvar, bdv, av, arch, cell, sm, detail: bool) -> list[dict]:
    n = sm["n"] * len(v2.SPONSOR_PROCS)
    ms = modal_string(sm)
    out = [row(cvar, bdv, av, arch, cell, "mean_p_rank_first_gross_P01_P15", sm["mean_pg"][i], "prob", intervention=i,
               lo=rv.wilson(sm["mean_pg"][i], n)[0], hi=rv.wilson(sm["mean_pg"][i], n)[1],
               note="lo/hi: 95% Wilson, Monte Carlo error only") for i in OPTS]
    out += [row(cvar, bdv, av, arch, cell, "mean_p_rank_first_net_P01_P15", sm["mean_pn"][i], "prob", intervention=i)
            for i in OPTS + ("none",)]
    out.append(row(cvar, bdv, av, arch, cell, "modal_winners_gross_P01_P15", ms, note="P01..P15 in order"))
    out += [row(cvar, bdv, av, arch, cell, "n_processes_modal_gross", float(ms.count(i)), "count", intervention=i)
            for i in OPTS]
    out += [row(cvar, bdv, av, arch, cell, "sponsor_gross_value_pool_p50", sm["pools"][i]["p50"], "usd/yr", intervention=i,
                lo=sm["pools"][i]["p25"], hi=sm["pools"][i]["p75"], note="lo/hi p25/p75") for i in OPTS]
    out += [row(cvar, bdv, av, arch, cell, "sponsor_best_non_AI_pool_p50", sm["best_other"]["p50"], "usd/yr",
                lo=sm["best_other"]["p25"], hi=sm["best_other"]["p75"]),
            row(cvar, bdv, av, arch, cell, "sponsor_C_incremental_over_best_other_p50", sm["c_incr"]["p50"], "usd/yr",
                lo=sm["c_incr"]["p25"], hi=sm["c_incr"]["p75"])]
    if detail:
        for pid in v2.SPONSOR_PROCS:
            d = sm["per"][pid]
            out += [row(cvar, bdv, av, arch, cell, "p_rank_first_gross", d["pg"][i], "prob", pid, i) for i in OPTS]
            out.append(row(cvar, bdv, av, arch, cell, "modal_winner_gross", d["modal_gross"], "", pid))
    return out


def absorption_rows(cvar, av, arch, ab: Mapping) -> list[dict]:
    note = "BD_FIELD minus V1_PRIORS, mean over P01-P15 of P(rank first, gross)"
    return [row(cvar, "BD_FIELD-V1_PRIORS", av, arch, "absorption", k, v, "prob" if k.startswith(("lost", "d")) else "share",
                note=note) for k, v in ab.items()]


def evidence_rows() -> list[dict]:
    return [dict(zip(EVIDENCE_COLS, e + ("2026-11-20",))) for e in EVIDENCE]


def spec_rows() -> list[dict]:
    out = [row("spec", "spec", s["id"], "ALL", "spec", "a_spec", f"alpha={s['alpha']}; rA={s['rA']}", note=s["note"],
               record_type="spec", scn="ALL") for s in A_SPECS]
    out += [row(c["id"], "spec", "spec", "ALL", "spec", "c_spec", f"kind={c['kind']}; ranges={c['ranges']}; m={c['m']:g}",
                record_type="spec", scn="ALL") for c in C_VARIANTS]
    out += [row("spec", b, "spec", "ALL", "spec", "bd_spec", "see ai-bd-recut-2026-11-19.csv", note=BD_BY_ID[b]["note"],
                record_type="spec", scn="ALL") for b in BD_IDS]
    return out


# ------------------------------------------------------------------------------------------- run (pure given inputs)
def run_archetype(idx, a, procs, anchor, draws) -> tuple[list[dict], list[str]]:
    spec = next(s for s in cal.CAL_SPECS if s["id"] == SCENARIO)
    sims = cal.simulate(a, idx, procs, anchor, draws, spec, "v2", {})
    ds = tuple(bd.compact_plus(SCENARIO, g, s, procs) for g, s in sims)
    del sims
    routes = {"G04": rv.route_stream(draws), "A01": bd.route_stream_a01(draws), None: (None,) * draws}
    rus = bd.recut_stream(draws)
    aid, avail = a["id"], anchor["available_n"]
    detail = aid in DETAIL_ARCHETYPES
    rows, log = [], []
    for cv in C_VARIANTS:
        cvals = tuple(bd.c_values(d, cv, rp, SCENARIO) for d, rp in zip(ds, routes[cv["ranges"]]))
        for asp in A_SPECS:
            sms = {b: bd.summarise(tuple(eval_cell(d, cvl, asp, BD_BY_ID[b], ru) for d, cvl, ru in zip(ds, cvals, rus)),
                                   avail) for b in BD_IDS}
            for b, sm in sms.items():
                rows += cell_rows(cv["id"], b, asp["id"], aid, "main", sm, detail)
                log.append(f"{aid:<9} {cv['id']:<16} {b:<10} {asp['id']:<15} "
                           + " ".join(f"{i}={sm['mean_pg'][i]:.3f}" for i in OPTS) + " modal " + modal_string(sm))
            ab = absorption(sms["V1_PRIORS"], sms["BD_FIELD"])
            rows += absorption_rows(cv["id"], asp["id"], aid, ab)
            log.append(f"  absorption {cv['id']} {asp['id']}: lost_BD={ab['lost_BD']:.3f} share_A={ab['share_A']:.3f} "
                       f"share_C={ab['share_C']:.3f}")
        for r in R_A_SWEEP:
            sm = bd.summarise(tuple(eval_cell(d, cvl, A_SPECS[0], BD_BY_ID["BD_FIELD"], ru, fixed_rA=r)
                                    for d, cvl, ru in zip(ds, cvals, rus)), avail)
            rows += cell_rows(cv["id"], "BD_FIELD", "SWEEP_RA", aid, f"sweep_rA={r:g}", sm, False)
            log.append(f"  SWEEP_RA r={r:<5g} {cv['id']:<16} " + " ".join(f"{i}={sm['mean_pg'][i]:.3f}" for i in OPTS)
                       + " modal " + modal_string(sm))
    return rows, log


def write_csv(path: str, rows: Sequence[Mapping], cols: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (accepted for the repo CLI convention; unused)")
    ap.add_argument("--draws", type=int, default=10000)
    ap.add_argument("--out", default=OUT_CSV)
    ap.add_argument("--evidence-out", default=EVIDENCE_CSV)
    ap.add_argument("--archetypes", default="NAT_LARGE,NAT_MID,CF_1BN,CF_250M,CF_SMALL")
    args = ap.parse_args(argv)
    procs = tuple(v2.v1_process(r) for r in v2.load_csv(v2.V1_CSV))
    sponsors = v2.load_sponsors(v2.load_csv(v2.COST_CSV))
    anchors = v2.grant_anchors(sponsors, v2.load_csv(v2.SUMMARY_CSV))
    keep = set(filter(None, args.archetypes.split(",")))
    arch = tuple((i, a) for i, a in enumerate(v2.ARCHETYPES) if a["id"] in keep)
    write_csv(args.evidence_out, evidence_rows(), EVIDENCE_COLS)
    rows = spec_rows() + [row("meta", "meta", "meta", "ALL", "meta", "draws", float(args.draws), "count", record_type="meta",
                              scn="ALL", note=f"calibrated Random({v2.SEED}); routing Random({rv.ROUTE_SEED}); "
                                              f"recut Random({bd.RECUT_SEED}); r_A uses the recut stream's third uniform")]
    for idx, a in arch:
        r, log = run_archetype(idx, a, procs, v2.archetype_anchor(a, sponsors, anchors), args.draws)
        rows += r
        print("\n".join(log), flush=True)
    write_csv(args.out, rows, COLS)
    print(f"wrote {len(rows)} rows -> {os.path.relpath(args.out, v2.ROOT)}; evidence {len(EVIDENCE)} rows -> "
          f"{os.path.relpath(args.evidence_out, v2.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
