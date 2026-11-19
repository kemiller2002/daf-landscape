#!/usr/bin/env python3
"""Re-cut of redesign (D) and conventional automation (B) to the evidence standard used for AI (C). Queue item
P-G0401-03 (with the P-G0401-01 confidence-band evidence feeding a new routing range for C).

Why: the calibrated model (scripts/mission_ai_economics_calibrated.py) and the routing variant
(scripts/mission_ai_routing_variant.py) held C to published field evidence, but B = beta * b_p * L and D = d_p * L kept
v1 priors (beta ~ U(0.30, 0.70), b_p and d_p triangular around v1 values). Both earlier notes say C's last place may
reflect those uncalibrated priors. This script imports both scripts UNCHANGED, rebuilds the same draws (common random
numbers, seed 42; routing stream seed 42 + 104729) and changes only B and D (plus one new routing range for C).

B and D recut [I = inference; evidence ids refer to data/mission-2026-11-14/ai-bd-recut-2026-11-19.csv, record_type=evidence]
  Realization factor r: realized saving / planned (ex-ante) saving, applied to beta*b_p*L (B) and d_p*L (D).
    BD-E01 HUD OIG 2021-OE-0007 (Feb 2023): RPA program realized 1,015 of 13,644 estimated hours (7%); 2,091 (15%) if
           finished bots ran; individual bots 1%, 11%, 33% of estimate.
    BD-E02 GSA OIG A210057 (Nov 2023): 9 of 10 sampled bots varied from estimate; OCFO closeout bot ~30 of 90 minutes
           (33%); 74% of bots reported no cost avoidance.
  BD specs
    V1_PRIORS   v2 B and D unchanged (reproduces the calibrated / routing results).
    B_FIELD     B * r_B, r_B ~ triangular(0.07, 0.33, 1.00) (BD-E01/E02 [I mapping]); D unchanged.
    BD_FIELD    B as B_FIELD; D * r_D with the same triangular, except P09/P10 (r_D = 1): their d_p has end-state
                support (BD-E03/E04: paper checks 16x more exception-prone than EFT). No 2021+ realization evidence for
                redesign was found, so applying the RPA realization range to D is [I] by analogy.
    BD_WIDE     explicit ignorance sweep [I]: r_B, r_D ~ U(0.07, 1.00) and d_p lower bound widened from 0.3*d1 to 0
                for every process without redesign evidence (all but P09/P10).
    BD_PROGRAM  stress [I]: r_B, r_D ~ U(0.07, 0.15) (HUD program-level realization incl. unused bots); P09/P10 r_D = 1.
    ABD_FIELD   BD_FIELD plus the same realization range on A (manual improvement, also a v1 prior) [I].
  r_B, r_D (and r_A) are drawn once per iteration from an independent stream Random(42 + 15485863); independence is [I].

C variants (all on CAL_CENTRAL calibrated draws)
  ASSIST          calibrated C (assist every amenable case)
  ROUTE_G04_M1/M5 routing variant, routing-note ranges h ~ U(0.21, 0.49), e ~ U(0, 0.10), k as v2 QA (m = 1 / 5)
  ROUTE_A01_M1/M5 routing with P-G0401-01 ranges [I mapping]: h ~ U(0.20, 0.80) (bank auto-close ~20% of workload;
                  E15 computed auto-closed share ~0.78; State Dept review volume -80%); e ~ U(0.004, 0.10) (E15 computed
                  in-band miss <= 0.4% per closed alert; 10% accepted-tier error budget in the OCBC invoice benchmark);
                  k unchanged. Same uniforms as the routing stream, so k is identical draw by draw.
  HYBRID_A01_M1   route (A01 ranges, m = 1) plus assistance on the low-confidence rest.

Break-even realization: per (draw, process), r_be = C / max(B_v1, D_v1) when C > A and C > 0, else 0: the common
realization factor below which C ranks first by gross. Sweeps apply a fixed common r to B and D (SWEEP_R_BD) or to
A, B and D (SWEEP_R_ABD) in every process.

Output (new file): data/mission-2026-11-14/ai-bd-recut-2026-11-19.csv (evidence rows are written by
--evidence-only from the evidence table embedded below; the main run writes model rows and appends them).
Usage: python3 scripts/mission_ai_bd_recut.py . [--draws 10000] [--out PATH]
Stdlib only; functional style (pure functions; I/O only in main / write_csv).
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
import mission_ai_routing_variant as rv  # noqa: E402

cal = rv.cal
v2 = rv.v2
OUT_CSV = os.path.join(v2.DATA, "ai-bd-recut-2026-11-19.csv")
RECUT_SEED = v2.SEED + 15485863
MAIN_SCENARIO = "CAL_CENTRAL"
FRAMING_SCENARIOS = ("CAL_FIELD_INLOOP", "CAL_TASK_REVIEW", "CAL_COMPLIANCE_FULL")
FRAMING_ARCHETYPES = ("NAT_LARGE",)
D_EVIDENCE_PROCS = frozenset({"P09", "P10"})
R_FIELD = (0.07, 0.33, 1.00)
R_SWEEP = (1.0, 0.75, 0.50, 0.33, 0.20, 0.15, 0.07)

BD_SPECS = (
    {"id": "V1_PRIORS", "rB": None, "rD": None, "d_wide": False,
     "note": "v2 B and D unchanged (replication)"},
    {"id": "B_FIELD", "rB": ("tri", R_FIELD), "rD": None, "d_wide": False,
     "note": "B x r_B, r_B~tri(0.07,0.33,1.0) from HUD/GSA OIG realization (BD-E01, BD-E02) [I mapping]"},
    {"id": "BD_FIELD", "rB": ("tri", R_FIELD), "rD": ("tri", R_FIELD), "d_wide": False,
     "note": "B as B_FIELD; D x r_D same range except P09/P10 r_D=1 (BD-E03/E04); D realization by analogy [I]"},
    {"id": "BD_WIDE", "rB": ("uni", (0.07, 1.0)), "rD": ("uni", (0.07, 1.0)), "d_wide": True,
     "note": "ignorance sweep [I]: r~U(0.07,1.0); d_p lower bound 0 for processes without redesign evidence"},
    {"id": "BD_PROGRAM", "rB": ("uni", (0.07, 0.15)), "rD": ("uni", (0.07, 0.15)), "d_wide": False,
     "note": "stress [I]: program-level realization 7-15% (BD-E01); P09/P10 r_D=1"},
    {"id": "ABD_FIELD", "rB": ("tri", R_FIELD), "rD": ("tri", R_FIELD), "rA": ("tri", R_FIELD), "d_wide": False,
     "note": "BD_FIELD plus the same realization range on manual improvement A (alpha is also an uncalibrated v1 prior) [I]"},
)
C_VARIANTS = (
    {"id": "ASSIST", "kind": "assist", "ranges": None, "m": 1.0},
    {"id": "ROUTE_G04_M1", "kind": "route", "ranges": "G04", "m": 1.0},
    {"id": "ROUTE_G04_M5", "kind": "route", "ranges": "G04", "m": 5.0},
    {"id": "ROUTE_A01_M1", "kind": "route", "ranges": "A01", "m": 1.0},
    {"id": "ROUTE_A01_M5", "kind": "route", "ranges": "A01", "m": 5.0},
    {"id": "HYBRID_A01_M1", "kind": "hybrid", "ranges": "A01", "m": 1.0},
)
OPTS = ("A", "B", "C", "D")

# ------------------------------------------------------------------------------------------- evidence table (data)
# Each row: id, part, domain, source, year, url, retrieved_via, quote, parameter, value, value_basis, grade, limits.
EVIDENCE = (
    # ---- Part A: confidence-band evidence (P-G0401-01)
    ("CB-01", "A", "AML alert disposition",
     "Eddin AN et al. Anti-Money Laundering Alert Optimization Using Machine Learning with Graphs (arXiv 2112.07508)",
     "2021", "https://arxiv.org/abs/2112.07508", "arXiv PDF full text (arxiv.org/pdf/2112.07508; robots allowed, crawl-delay 15)",
     "The percentage of suspicious accounts in our dataset is less than 3% of the alerted ones, resulting in over 97% false positives. | "
     "we consider recall@20%FPR as our target metric, which translates to a reduction of the false positives by 80% compared to the rule system itself | "
     "allows us to alert only 20% of the events while capturing over 90% of the suspicious entities",
     "prevalence pi (share of alerts that are true positives)", "<0.03", "F", "B",
     "Retrospective validation on one bank's data; account-day labels inferred from SAR transactions; ML (LightGBM) triage, not gen-AI"),
    ("CB-01c", "A", "AML alert disposition", "Computed from CB-01", "2021", "https://arxiv.org/abs/2112.07508", "computed",
     "auto-closed share = 0.8(1-pi) + (1-recall)pi; miss rate inside closed band = (1-recall)pi / auto-closed share",
     "h (auto-closed share) and e (error inside auto-closed band)",
     "h = 0.779 and e <= 0.0039 at pi = 0.03, recall 0.90; e <= 0.0077 at recall 0.80 (baseline LightGBM)", "C", "B",
     "pi is an upper bound (<3%), so e is an upper bound; recall 'over 90%' is the graph-feature model, 'close to 80%' the baseline"),
    ("CB-02", "A", "AML alert disposition",
     "Gerlings J, Constantiou I. Machine Learning in Transaction Monitoring: The Prospect of xAI. HICSS-56 (arXiv 2210.07648)",
     "2023", "https://arxiv.org/abs/2210.07648", "arXiv PDF full text",
     "When closing alerts (A), the model reduces the workload of investigators by ~20%. | for now, auto-closed alerts are checked by "
     "dedicated investigators and risk owners to ensure the model is operating according to the agreed risk appetite",
     "h (auto-closed share of alert workload); k (QA on auto-closed band)", "h ~ 0.20; k = 1 during testing; e not reported", "F", "B",
     "Interview case study at one bank; random-forest risk score 1-100 on lower-complexity scenarios only; error inside band not disclosed"),
    ("CB-03", "A", "AML alert disposition (rules scoring threshold)",
     "FinCEN Consent Order 2026-03, Bank of America N.A.", "2026",
     "https://www.fincen.gov/system/files/2026-10/BoA-Consent-Order-Execution-Final.pdf", "fincen.gov PDF",
     "the SAR yield for Event Groups with 20-24 points (i.e., those either at or just above the threshold triggering investigation) was roughly "
     "33-34% ... the SAR yield for Event Groups with 16 to 19 points (i.e., those just below the threshold that would trigger investigation) "
     "were generally between 38% and 45% | introduced certain false negative thresholds, including a 5% tolerance level for false negatives | "
     "the revised threshold would result in an increase of 16,000 U.S. investigations each month, representing \"double [the] prior ongoing monthly volume\"",
     "e inside the band just below threshold; miss tolerance; cost of escaped errors (m)",
     "e = 0.38-0.45 in the 16-19 point band (2022-Q1 2023); tolerance 5% (7.5% board escalation); lookback ~8,900 missed SARs (~$4bn)", "F", "A",
     "Rules-based Event Processor scoring, not ML/AI; shows a miscalibrated threshold where confidence carries no information; regulator's findings"),
    ("CB-04", "A", "Invoice/AP field extraction",
     "Jin Y et al. (OCBC). Perception, Layout, and Validation: Calibrated Confidence for Reliable Straight-Through Processing of Financial Documents (arXiv 2609.20110)",
     "2026", "https://arxiv.org/abs/2609.20110", "arXiv PDF full text",
     "Even DocILE, the real and heterogeneous invoices, reaches 49% auto-approval at >= 90% precision from a near-zero baseline. | "
     "The native VLM confidence signals could clear only 0.1%-7.0% of fields under risk control at a target error of <= 10%",
     "h (auto-approved share of fields) at a bounded e", "DocILE cross-model: h = 0.281 (e<=5%), 0.494 (e<=10%), 0.665 (e<=20%); native VLM confidence h = 0.001-0.070 at e<=10%", "F", "C",
     "Benchmark on public datasets (500 DocILE docs), not a production field study; field-level not invoice-level; authors at a bank"),
    ("CB-05", "A", "Document classification (declassification review)",
     "US Department of State, AI Pilot Results (deck hosted by NARA), June 24 2024", "2024",
     "https://transforming-classification.blogs.archives.gov/wp-content/uploads/sites/10/2024/07/State-AI-Pilot-Results-June-24-2024.pdf",
     "NARA blog PDF",
     "Reduced volume for humans to review (by 80%) | Humans will always be in the loop to: ... Perform Quality Control (QC) checks ... Review cables the model is unsure of | 450,000 cables reviewed by AI",
     "h (share of documents decided without human review)", "h ~ 0.80 (production, 2023-24); k > 0 (QC retained, rate not stated); e not reported", "F", "B",
     "Agency self-report; slide deck; error inside the auto-decided band not reported"),
    ("CB-06", "A", "Document classification (declassification review)",
     "American Foreign Service Association, The Foreign Service Journal, October 2023, 'AI-Assisted Declassification'", "2023",
     "https://afsa.org/sites/default/files/flipping_book/1023/19", "afsa.org page",
     "With AI assistance, the workload stands to be reduced by more than 65 percent ... The AI's document review matched previous human declassification decisions at a rate of more than 97 percent.",
     "h (pilot); overall agreement", "h > 0.65 (3-month pilot); overall agreement > 0.97 (all documents, not the auto band)", "F", "C",
     "Secondary (association journal) report of the pilot; agreement is overall, not inside the confidence band"),
    ("CB-07", "A", "Bookkeeping / AP (E17 target)",
     "Choi JH, Xie C. Human + AI in Accounting: Early Evidence from the Field (Stanford GSB working-paper page; JAR 2026)", "2025",
     "https://www.gsb.stanford.edu/faculty-research/working-papers/human-ai-accounting-early-evidence-field", "GSB page (abstract)",
     "reallocation of approximately 8.5% of accountant time from routine data entry toward high-value tasks such as business communication and quality assurance ... "
     "expertise increases intervention when AI confidence scores signal uncertainty",
     "intervention rate by confidence (target); time reallocation", "No band-level rates available: full text blocked (SSRN 403, Wiley 403); 8.5% time reallocation", "F", "A",
     "Full text not retrieved; intervention rates by confidence score remain unknown"),
    # ---- Part B: B and D evidence (P-G0401-03)
    ("BD-E01", "B", "Conventional automation (RPA), federal back office",
     "HUD Office of Inspector General, Evaluation 2021-OE-0007, HUD's Robotic Process Automation Program Was Not Efficient or Effective", "2023",
     "https://www.hudoig.gov/sites/default/files/2023-02/2021-OE-0007.pdf", "hudoig.gov PDF",
     "only seven distinct bots were in use, and annual labor hour savings totaled approximately 1,015, or 7 percent of the amount HUD estimated | "
     "the total potential labor hour savings for HUD's RPA program would be approximately 2,091 hours, or 15 percent | "
     "A bot developed for OCFO was planned to save 2,100 hours annually by sending a survey form to grant recipients ... expected to save only 24 labor hours annually, or 1 percent",
     "r_B (realized / planned saving)", "0.07 program; 0.15 potential; per bot 0.01, 0.11, 0.33", "F", "A",
     "One agency; program-level ratio includes bots never deployed (partly a fixed-cost failure, not a per-case saving)"),
    ("BD-E02", "B", "Conventional automation (RPA), federal back office",
     "GSA Office of Inspector General, Audit A210057/B/5/F24001, GSA's RPA Program Lacks Evidence to Support Claimed Savings", "2023",
     "https://gsaig.gov/sites/default/files/audit-reports/A210057-1%20Final%20Report.pdf", "gsaig.gov PDF",
     "We found that the actual results varied from the estimates for 9 of the 10 bots we sampled | The OCFO Project Closeout bot had estimated savings based on the task taking 90 minutes, "
     "whereas users reported time savings only averaged approximately 30 minutes | The RPA program's survey of individual bot's owners indicated 74 percent of bots resulted in no cost avoidance",
     "r_B; beta at task level (b = 1)", "closeout bot 30/90 = 0.33; 1 of 10 bots matched estimate; 74% of bots no cost avoidance", "F", "A",
     "User-reported minutes; sample of the 10 largest claimed bots"),
    ("BD-E03", "B", "Redesign: paper check to electronic payment (P09/P10)",
     "Executive Order 14247, Modernizing Payments To and From America's Bank Account (25 March 2025)", "2025",
     "https://www.whitehouse.gov/presidential-actions/2025/03/modernizing-payments-to-and-from-americas-bank-account/", "whitehouse.gov page",
     "Historically, Department of the Treasury checks are 16 times more likely to be reported lost or stolen, returned undeliverable, or altered than an electronic funds transfer (EFT).",
     "d_p for P10 returned/uncashed checks (per converted payment)", "1 - 1/16 = 0.94 of exceptions eliminated per payment converted [C/I]", "F", "B",
     "Federal payments, not charitable grants; ratio of exception rates, not of labour; conversion share (adoption) not covered"),
    ("BD-E04", "B", "Redesign: paper check to electronic payment (P09/P10)",
     "Bureau of the Fiscal Service, 'Paper Checks Are Going Away' (news)", "2025",
     "https://fiscal.treasury.gov/about-us/news/paper-checks-going-away", "fiscal.treasury.gov page",
     "With paper checks over 16 times more likely to get lost, stolen, altered, or delayed, we encourage those still receiving paper checks to make the switch today.",
     "d_p for P10", "consistent with BD-E03", "F", "B", "As BD-E03"),
    ("BD-E05", "B", "Redesign of an AML review threshold (P14)",
     "FinCEN Consent Order 2026-03, Bank of America N.A. (see CB-03)", "2026",
     "https://www.fincen.gov/system/files/2026-10/BoA-Consent-Order-Execution-Final.pdf", "fincen.gov PDF",
     "the new model resulted in \"case load reduction,\" with the model reducing by over 8,200 the number of cases that would require investigation. The report went on to describe the associated \"SAR loss\" ... as \"permissible\" | "
     "requiring the Bank to increase staffing with an \"incremental 750\" personnel",
     "d_p for P14 (elimination of review volume) and its reversibility", "A threshold redesign that cut 8,200 cases was reversed; the corrected threshold doubled monthly investigations", "F", "A",
     "Bank, not a DAF; shows redesign savings in compliance review can be negative after supervision"),
    ("BD-E06", "B", "Document review redesign + AI (labour value)",
     "AFSA Foreign Service Journal, October 2023 (see CB-06)", "2023", "https://afsa.org/sites/default/files/flipping_book/1023/19", "afsa.org page",
     "Historically, manual page-by-page review, conducted year-round by a team of six, has been the only way",
     "pool scale cross-check", "team of six reviewers; >65% workload reduction", "F", "C", "Not a DAF process"),
)
EVIDENCE_COLS = ("evidence_id", "part", "domain", "source", "year", "url", "retrieved_via", "quote", "parameter", "value",
                 "value_basis", "grade", "limitations")


# ------------------------------------------------------------------------------------------- pure draws
def draw_r(u: float, dist) -> float:
    if dist is None:
        return 1.0
    kind, par = dist
    return v2.tri(u, *par) if kind == "tri" else v2.uni(u, *par)


def recut_stream(n: int) -> tuple[tuple[float, float, float], ...]:
    rng = random.Random(RECUT_SEED)
    return tuple((rng.random(), rng.random(), rng.random()) for _ in range(n))


def draw_route_a01(u: Sequence[float]) -> dict:
    """P-G0401-01 routing ranges on the same three uniforms as rv.draw_route (k identical)."""
    return {"h": v2.uni(u[0], 0.20, 0.80), "e": v2.uni(u[1], 0.004, 0.10), "k": v2.tri(u[2], 0.03, 0.10, 0.30), "rho": 0.0}


def route_stream_a01(n: int) -> tuple[dict, ...]:
    rng = random.Random(rv.ROUTE_SEED)
    return tuple(draw_route_a01((rng.random(), rng.random(), rng.random())) for _ in range(n))


def d_wide(u_d: float, d_drawn: float, d1: float) -> float:
    """Widened d_p: lower bound 0 instead of 0.3*d1, keeping the drawn adoption multiplier (recovered from d)."""
    base = v2.tri(u_d, 0.3 * d1, d1, min(0.95, d1 + 0.10))
    adopt = d_drawn / base if base > 0 else 1.0
    return v2.tri(u_d, 0.0, d1, min(0.95, d1 + 0.10)) * adopt


# ------------------------------------------------------------------------------------------- compact draw (pure)
def compact_plus(scn: str, g: Mapping, s: Mapping, procs: Sequence[Mapping]) -> dict:
    base = rv.compact(scn, g, s, procs)
    d1 = {p["id"]: p["redesign_elimination_share"] for p in procs}
    extra = {p["id"]: {"u_d": g["per"][p["id"]]["u_d"], "d": g["per"][p["id"]]["d"], "d1": d1[p["id"]]} for p in procs}
    return {**base, "procs": tuple({**cp, **extra[cp["pid"]]} for cp in base["procs"])}


def c_values(d: Mapping, cv: Mapping, rp: Mapping | None, scn: str) -> dict:
    return {cp["pid"]: (cp["assist"] if cv["kind"] == "assist" else rv.c_value(cv["kind"], cp, rp, scn, cv["m"]))
            for cp in d["procs"]}


def bd_values(cp: Mapping, spec: Mapping, rB: float, rD: float) -> tuple[float, float]:
    """Recut gross B and D for one process in one draw."""
    B = cp["others"]["B"] * rB
    has_ev = cp["pid"] in D_EVIDENCE_PROCS
    D0 = (d_wide(cp["u_d"], cp["d"], cp["d1"]) * cp["L"]) if (spec["d_wide"] and not has_ev) else cp["others"]["D"]
    return B, D0 * (1.0 if has_ev and spec["id"] in ("BD_FIELD", "BD_PROGRAM", "ABD_FIELD") else rD)


def eval_draw(d: Mapping, cvals: Mapping, spec: Mapping, ru: Sequence[float], fixed_r: float | None = None,
              r_on_a: bool = False) -> dict:
    rB = fixed_r if fixed_r is not None else draw_r(ru[0], spec["rB"])
    rD = fixed_r if fixed_r is not None else draw_r(ru[1], spec["rD"])
    rA = draw_r(ru[2], spec.get("rA")) if fixed_r is None else (fixed_r if r_on_a else 1.0)
    out = {}
    for cp in d["procs"]:
        B, D = (cp["others"]["B"] * rB, cp["others"]["D"] * rD) if fixed_r is not None else bd_values(cp, spec, rB, rD)
        gross = {"A": cp["others"]["A"] * rA, "B": B, "C": cvals[cp["pid"]], "D": D}
        net = {i: gross[i] - cp["F"][i] for i in OPTS}
        best_bd = max(cp["others"]["B"], cp["others"]["D"])
        c = gross["C"]
        r_be = (c / best_bd if best_bd > 0 else math.inf) if (c > gross["A"] and c > 0) else 0.0
        out[cp["pid"]] = {"gross": gross, "first_gross": v2.argmax(gross), "first_net": v2.argmax({**net, "none": 0.0}),
                          "r_be": r_be, "c_net_pos": net["C"] > 0}
    pools = {i: sum(max(0.0, out[k]["gross"][i]) for k in v2.SPONSOR_PROCS) for i in OPTS}
    best_other = sum(max(0.0, out[k]["gross"]["A"], out[k]["gross"]["B"], out[k]["gross"]["D"]) for k in v2.SPONSOR_PROCS)
    c_incr = sum(max(0.0, out[k]["gross"]["C"] - max(0.0, out[k]["gross"]["A"], out[k]["gross"]["B"], out[k]["gross"]["D"]))
                 for k in v2.SPONSOR_PROCS)
    return {"proc": out, "pools": pools, "best_other": best_other, "c_incr": c_incr,
            "n_be": v2.breakeven_n(pools["C"], d["tau"], d["F_platform"], d["f_sponsor"])}


# ------------------------------------------------------------------------------------------- summaries (pure)
def summarise(evals: Sequence[Mapping], avail: int | None) -> dict:
    n = len(evals)
    per = {}
    for pid in v2.SPONSOR_PROCS:
        rs = [e["proc"][pid] for e in evals]
        pg = {i: sum(r["first_gross"] == i for r in rs) / n for i in OPTS}
        pn = {i: sum(r["first_net"] == i for r in rs) / n for i in OPTS + ("none",)}
        per[pid] = {"pg": pg, "pn": pn, "modal_gross": cal.modal(pg), "modal_net": cal.modal(pn),
                    "r_be_p50": v2.quantile([r["r_be"] for r in rs], .5),
                    "p_r_be_ge_033": sum(r["r_be"] >= 0.33 for r in rs) / n,
                    "p_r_be_ge_007": sum(r["r_be"] >= 0.07 for r in rs) / n,
                    "c_net_pos": sum(r["c_net_pos"] for r in rs) / n}
    q = lambda xs: {lab: v2.quantile(xs, p) for lab, p in (("p25", .25), ("p50", .5), ("p75", .75))}  # noqa: E731
    nbe = [e["n_be"] for e in evals]
    return {"n": n, "per": per,
            "mean_pg": {i: v2.mean([per[k]["pg"][i] for k in v2.SPONSOR_PROCS]) for i in OPTS},
            "mean_pn": {i: v2.mean([per[k]["pn"][i] for k in v2.SPONSOR_PROCS]) for i in OPTS + ("none",)},
            "pools": {i: q([e["pools"][i] for e in evals]) for i in OPTS},
            "best_other": q([e["best_other"] for e in evals]), "c_incr": q([e["c_incr"] for e in evals]),
            "p_be_le_avail": (sum(x <= avail for x in nbe) / n) if avail else None,
            "n_be_p50": v2.quantile([x for x in nbe if math.isfinite(x)], .5)}


def row(scn, cvar, bd, arch, cell, metric, value, unit="", process_id="", intervention="", lo=None, hi=None, note="",
        record_type="model") -> dict:
    rnd = lambda x: round(x, 6) if isinstance(x, float) and math.isfinite(x) else x  # noqa: E731
    return {"record_type": record_type, "scenario": scn, "c_variant": cvar, "bd_variant": bd, "archetype": arch,
            "cell": cell, "process_id": process_id, "intervention": intervention, "metric": metric, "value": rnd(value),
            "lo": rnd(lo) if lo is not None else "", "hi": rnd(hi) if hi is not None else "", "unit": unit, "note": note}


def summary_rows(scn, cvar, bd, arch, cell, sm, ref_modal, ref_label, detail=True) -> list[dict]:
    n = sm["n"] * len(v2.SPONSOR_PROCS)
    out = [row(scn, cvar, bd, arch, cell, "mean_p_rank_first_gross_P01_P15", sm["mean_pg"][i], "prob", intervention=i,
               lo=rv.wilson(sm["mean_pg"][i], n)[0], hi=rv.wilson(sm["mean_pg"][i], n)[1],
               note="lo/hi: 95% Wilson, Monte Carlo error only") for i in OPTS]
    out += [row(scn, cvar, bd, arch, cell, "mean_p_rank_first_net_P01_P15", sm["mean_pn"][i], "prob", intervention=i)
            for i in OPTS + ("none",)]
    changed = [pid for pid in v2.SPONSOR_PROCS if sm["per"][pid]["modal_gross"] != ref_modal[pid]]
    out.append(row(scn, cvar, bd, arch, cell, "processes_modal_winner_changed_gross", float(len(changed)), "count",
                   note=f"vs {ref_label}: " + ";".join(f"{p}:{ref_modal[p]}->{sm['per'][p]['modal_gross']}" for p in changed)))
    out.append(row(scn, cvar, bd, arch, cell, "modal_winners_gross_P01_P15",
                   "".join(sm["per"][p]["modal_gross"] for p in v2.SPONSOR_PROCS), "", note="P01..P15 in order"))
    out.append(row(scn, cvar, bd, arch, cell, "modal_winners_net_P01_P15",
                   ",".join(sm["per"][p]["modal_net"] for p in v2.SPONSOR_PROCS), "", note="P01..P15 in order"))
    out.append(row(scn, cvar, bd, arch, cell, "n_processes_C_modal_gross",
                   float(sum(sm["per"][p]["modal_gross"] == "C" for p in v2.SPONSOR_PROCS)), "count"))
    if not detail:
        return out
    out += [row(scn, cvar, bd, arch, cell, "sponsor_gross_value_pool_p50", sm["pools"][i]["p50"], "usd/yr", intervention=i,
                lo=sm["pools"][i]["p25"], hi=sm["pools"][i]["p75"], note="sum of positive gross over P01-P15; lo/hi p25/p75")
            for i in OPTS]
    out += [row(scn, cvar, bd, arch, cell, "sponsor_best_non_AI_pool_p50", sm["best_other"]["p50"], "usd/yr",
                lo=sm["best_other"]["p25"], hi=sm["best_other"]["p75"], note="sum over P01-P15 of max(0,A,B,D)"),
            row(scn, cvar, bd, arch, cell, "sponsor_C_incremental_over_best_other_p50", sm["c_incr"]["p50"], "usd/yr",
                lo=sm["c_incr"]["p25"], hi=sm["c_incr"]["p75"], note="sum over P01-P15 of max(0, C - max(0,A,B,D))"),
            row(scn, cvar, bd, arch, cell, "vendor_breakeven_sponsors_p50_finite", sm["n_be_p50"], "sponsors",
                note="depends on C only (unchanged by B/D recut)")]
    if sm["p_be_le_avail"] is not None:
        out.append(row(scn, cvar, bd, arch, cell, "p_vendor_breakeven_le_available", sm["p_be_le_avail"], "prob"))
    for pid in v2.SPONSOR_PROCS:
        d = sm["per"][pid]
        out += [row(scn, cvar, bd, arch, cell, "p_rank_first_gross", d["pg"][i], "prob", pid, i) for i in OPTS]
        out += [row(scn, cvar, bd, arch, cell, "p_rank_first_net", d["pn"][i], "prob", pid, i) for i in OPTS + ("none",)]
        out += [row(scn, cvar, bd, arch, cell, "modal_winner_gross", d["modal_gross"], "", pid),
                row(scn, cvar, bd, arch, cell, "modal_winner_net", d["modal_net"], "", pid),
                row(scn, cvar, bd, arch, cell, "p_C_net_positive", d["c_net_pos"], "prob", pid, "C")]
        if bd == "V1_PRIORS":
            out += [row(scn, cvar, bd, arch, cell, "breakeven_realization_r_p50", d["r_be_p50"], "ratio", pid, "C",
                        note="common realization factor on B and D below which C ranks first by gross; 0 = never (A beats C)"),
                    row(scn, cvar, bd, arch, cell, "p_breakeven_realization_ge_0.33", d["p_r_be_ge_033"], "prob", pid, "C"),
                    row(scn, cvar, bd, arch, cell, "p_breakeven_realization_ge_0.07", d["p_r_be_ge_007"], "prob", pid, "C")]
    return out


def evidence_rows() -> list[dict]:
    return [{**{c: "" for c in ("scenario", "c_variant", "bd_variant", "archetype", "cell", "process_id", "intervention",
                                "lo", "hi", "unit")},
             "record_type": "evidence", "metric": e[0], "value": e[9], "note": " || ".join(
                 (e[1], e[2], e[3], e[4], e[5], e[8], e[10], e[12]))} for e in EVIDENCE]


def spec_rows() -> list[dict]:
    out = [row("ALL", "spec", sp["id"], "ALL", "spec", "bd_spec",
               f"rB={sp['rB']}; rD={sp['rD']}; rA={sp.get('rA')}; d_wide={sp['d_wide']}",
               note=sp["note"], record_type="spec") for sp in BD_SPECS]
    out += [row("ALL", cv["id"], "spec", "ALL", "spec", "c_spec", f"kind={cv['kind']}; ranges={cv['ranges']}; m={cv['m']:g}",
                note=("G04: h~U(.21,.49), e~U(0,.10)" if cv["ranges"] == "G04" else
                      "A01: h~U(.20,.80), e~U(.004,.10)" if cv["ranges"] == "A01" else "calibrated assist"),
                record_type="spec") for cv in C_VARIANTS]
    return out


def write_csv(path: str, rows: Sequence[Mapping], cols: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def run_archetype(scn, idx, a, procs, anchor, draws, sweeps: bool) -> tuple[list[dict], list[str]]:
    spec = next(s for s in cal.CAL_SPECS if s["id"] == scn)
    sims = cal.simulate(a, idx, procs, anchor, draws, spec, "v2", {})
    ds = tuple(compact_plus(scn, g, s, procs) for g, s in sims)
    del sims
    routes = {"G04": rv.route_stream(draws), "A01": route_stream_a01(draws), None: (None,) * draws}
    rus = recut_stream(draws)
    aid, avail = a["id"], anchor["available_n"]
    rows, log = [], []
    ref_assist = None
    for cv in C_VARIANTS:
        cvals = tuple(c_values(d, cv, rp, scn) for d, rp in zip(ds, routes[cv["ranges"]]))
        ref_same = None
        for sp in BD_SPECS:
            sm = summarise(tuple(eval_draw(d, cvl, sp, ru) for d, cvl, ru in zip(ds, cvals, rus)), avail)
            if sp["id"] == "V1_PRIORS":
                ref_same = {p: sm["per"][p]["modal_gross"] for p in v2.SPONSOR_PROCS}
                ref_assist = ref_assist or ref_same
            rows += summary_rows(scn, cv["id"], sp["id"], aid, "main", sm, ref_same, f"{cv['id']}/V1_PRIORS")
            if cv["id"] != "ASSIST":
                rows += [r for r in summary_rows(scn, cv["id"], sp["id"], aid, "vs_assist_v1", sm, ref_assist,
                                                 "ASSIST/V1_PRIORS", detail=False) if r["metric"] == "processes_modal_winner_changed_gross"]
            log.append(f"{scn} {aid:<9} {cv['id']:<13} {sp['id']:<10} P(C1st)={sm['mean_pg']['C']:.4f} "
                       f"B={sm['mean_pg']['B']:.3f} D={sm['mean_pg']['D']:.3f} A={sm['mean_pg']['A']:.3f} "
                       "modal " + "".join(sm["per"][p]["modal_gross"] for p in v2.SPONSOR_PROCS) +
                       f" C={sm['pools']['C']['p50']:,.0f} B={sm['pools']['B']['p50']:,.0f} D={sm['pools']['D']['p50']:,.0f}")
        if sweeps:
            for lab, on_a in (("SWEEP_R_BD", False), ("SWEEP_R_ABD", True)):
                for r in R_SWEEP:
                    sm = summarise(tuple(eval_draw(d, cvl, BD_SPECS[0], ru, fixed_r=r, r_on_a=on_a)
                                         for d, cvl, ru in zip(ds, cvals, rus)), avail)
                    rows += summary_rows(scn, cv["id"], lab, aid, f"sweep_r={r:g}", sm, ref_same,
                                         f"{cv['id']}/V1_PRIORS", detail=False)
                    rows += [row(scn, cv["id"], lab, aid, f"sweep_r={r:g}", "sponsor_gross_value_pool_p50",
                                 sm["pools"][i]["p50"], "usd/yr", intervention=i) for i in ("A", "B", "D")]
                    log.append(f"  {lab} r={r:<5g} {cv['id']:<13} P(C1st)={sm['mean_pg']['C']:.4f} nC_modal="
                               f"{sum(sm['per'][p]['modal_gross'] == 'C' for p in v2.SPONSOR_PROCS)} modal "
                               + "".join(sm["per"][p]["modal_gross"] for p in v2.SPONSOR_PROCS))
    return rows, log


# ------------------------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (accepted for the repo CLI convention; unused)")
    ap.add_argument("--draws", type=int, default=10000)
    ap.add_argument("--out", default=OUT_CSV)
    ap.add_argument("--archetypes", default="", help="comma list to restrict (testing)")
    args = ap.parse_args(argv)
    procs = tuple(v2.v1_process(r) for r in v2.load_csv(v2.V1_CSV))
    sponsors = v2.load_sponsors(v2.load_csv(v2.COST_CSV))
    anchors = v2.grant_anchors(sponsors, v2.load_csv(v2.SUMMARY_CSV))
    keep = set(filter(None, args.archetypes.split(",")))
    arch = tuple((i, a) for i, a in enumerate(v2.ARCHETYPES) if not keep or a["id"] in keep)
    anchor_by = {a["id"]: v2.archetype_anchor(a, sponsors, anchors) for _, a in arch}
    rows = evidence_rows() + spec_rows() + [row("ALL", "meta", "meta", "ALL", "meta", "draws", float(args.draws), "count",
                                                note=f"calibrated Random({v2.SEED}); routing Random({rv.ROUTE_SEED}); recut Random({RECUT_SEED})",
                                                record_type="meta")]
    for idx, a in arch:
        r, log = run_archetype(MAIN_SCENARIO, idx, a, procs, anchor_by[a["id"]], args.draws, sweeps=True)
        rows += r
        print("\n".join(log), flush=True)
    for scn in FRAMING_SCENARIOS:
        for idx, a in arch:
            if a["id"] in FRAMING_ARCHETYPES:
                r, log = run_archetype(scn, idx, a, procs, anchor_by[a["id"]], args.draws, sweeps=False)
                rows += r
                print("\n".join(log), flush=True)
    cols = ("record_type", "scenario", "c_variant", "bd_variant", "archetype", "cell", "process_id", "intervention", "metric",
            "value", "lo", "hi", "unit", "note")
    write_csv(args.out, rows, cols)
    print(f"wrote {len(rows)} rows -> {os.path.relpath(args.out, v2.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
