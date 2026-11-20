# P-G04-01 and P-G05-02: confidence-gated AI routing, and the exception share per grant

*Prepared 2026-11-19. TASKID g0401-g0502.*

**Outputs**
- [`scripts/mission_ai_routing_variant.py`](../../scripts/mission_ai_routing_variant.py): imports `mission_ai_economics_calibrated.py` (and through it v2) unchanged. Stdlib only, functional style, seed 42 plus a separate routing stream.
- [`data/mission-2026-11-14/ai-routing-variant-2026-11-19.csv`](../../data/mission-2026-11-14/ai-routing-variant-2026-11-19.csv): 17,412 rows, 10,000 draws per scenario and archetype (data dictionary in §D1).
- [`scripts/mission_exception_per_grant.py`](../../scripts/mission_exception_per_grant.py): imports `mission_exception_load.py` (line flags, Schedule F reader, totals-row filter of the wave-32A regeneration) unchanged.
- [`data/mission-2026-11-14/exception-share-per-grant-2026-11-19.csv`](../../data/mission-2026-11-14/exception-share-per-grant-2026-11-19.csv): 10,156 rows (data dictionary in §D2).
- [`data/mission-2026-11-14/queue-proposals-g0401-g0502.csv`](../../data/mission-2026-11-14/queue-proposals-g0401-g0502.csv): six proposals.
- No existing file was modified.

**Read first**
- [gap19-ai-calibration.md](gap19-ai-calibration.md) with its [V wave 31A] corrections: 13 runs, not 12; and the q = r·a basis cuts the unsourced field-framing QA charge by about 60% ([validation-wave31a-report.md](validation-wave31a-report.md) items 2–3).
- [ai-economics-v2-observed-costs.md](ai-economics-v2-observed-costs.md) and [ai-economics-replacement-analysis.md](ai-economics-replacement-analysis.md) (intervention C).
- [gap19-exception-load-proxy.md](gap19-exception-load-proxy.md) with its [V wave 32A] corrections and the governing regeneration note: the Greater Horizons totals row is dropped, giving 608,610 lines, $92.72bn, and core 7.41% / 10.96%.

**Notation**
- **[F]** published or filed value.
- **[C]** computed by a script in this note.
- **[I]** inference or assumption. Every routing parameter mapping and every grant-size scaling rule is [I].
- **[S]** scenario output, conditional on stated ranges.

---

## 0. Answers in brief

### (A) Does C's weakness come from the assist-every-case formula or from AI? [S]

The answer is split: **the size of the value pool comes from the formula; the ranking does not.**

All figures below are for a large national under CAL_CENTRAL, on the same draws, and use the evidence-bounded routing ranges in §A2.

| Measure | C as assistant (calibrated) | Routing, m = 1 | Routing, m = 5 | Routing, m = 20 | Routing + assist on the rest, m = 1 |
|---|---:|---:|---:|---:|---:|
| Mean P(C ranks first, gross), P01–P15 | 0.0021 | 0.0123 | 0.0049 | 0.0014 | 0.0388 |
| Sponsor AI value pool, p50 (p25–p75) | $445k ($145k–$1.06m) | **$1.36m** ($724k–$2.61m) | $1.06m ($551k–$2.03m) | $44k ($0–$628k) | $1.79m ($969k–$3.41m) |
| P07 due diligence: P(C clears its fixed cost) | 0.31 | 0.64 | 0.55 | 0.19 | 0.73 |
| Vendor break-even: sponsors needed, p50 (p25–p75) | 17 (7–43) | 8 (4–16) | 10 (5–21) | 16 (7–40) | 6 (3–12) |
| P(break-even ≤ the 5 large nationals) | 0.13 | 0.38 | 0.29 | 0.09 | 0.48 |
| Observed FY2024 population (CF + all nationals): P(break-even reachable) | 0.165 | 0.47 | 0.34 | 0.10 | 0.65 |
| Processes whose most likely winner changes | — | 0 | 0 | 0 | 0 |

m is the cost of an escaped error, in units of one case's handling time. It has no direct public source, so it is a sweep [I]. The escaped-error study ([g0403-04-escaped-error-cost.md](g0403-04-escaped-error-cost.md)) bounds it at 1.0–106 from IRC §4966/§4967 rates and bank SAR penalties. Its central 2.4 is mostly assumption-driven, and at m = 2.42 the large-national routing pool is $1.26m [S]. [V wave 38B] Corrected: the central is 2.20 (wave 38B, $1.27m). Bounding detection with IRS exam and SOI §4966 data lowers it to 1.56–1.77 ($1.31m–$1.32m). It is still assumption-driven, through operational rework and the P01/P14 sanctions term ([g0403-0104-m-detection-ofac.md](g0403-0104-m-detection-ofac.md)) [C/S] [V wave 39B]

1. **The value pool depends on the formula.**
   - At the evidence-bounded share of high-confidence cases (h = 0.21–0.49, from E19), routing multiplies the pool by 2.7–3.4× when an escaped error costs one handling-time and by 2.1–2.6× at five (CAL_CENTRAL, across archetypes). Both m and ρ = 0 (no residual human time on AI-closed cases) are unsourced [I]; at ρ = 0.25 the large-national pool falls from $1.36m to $938k [S] [V wave 36B]
   - The routing pool does not depend on s: the routing formula never uses the disputed time-saving parameter, so the field and task framings give the same routing pool. The gain over assistance does depend on s: at a large national (m = 1) the routing pool is 6.8× the assist pool under the field framing, 3.1× under the central one and 1.7× under the task framing [C] [V wave 36B]
   - The 60% calibration cut came mostly from s and q. It is therefore a cut to **assistance**, not to AI as such.
2. **The ranking does not depend on the formula.**
   - The probability that C ranks first rises from 0.2% to only 1.2% (route) or 3.9% (hybrid). The most likely winner changes in **no process** at any archetype or scenario.
   - Redesign (D) and conventional automation (B) still win on gross value. C overtakes them only when h ≥ 0.70, which is above the evidence range: then P03 and P07 flip to C, and at h = 0.90 so do P13 and P14 (and P08 at CF_1BN) [V wave 36B]
   - So C's last place in the ranking reflects the comparison set (uncalibrated B and D priors) and the amenable share a_p ≤ 0.6. It does not reflect how AI is deployed. The B/D recut ([g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md)) only partly confirms this: cutting B and D to RPA-audit realization (D by analogy [I]) raises routing’s P(C first) from 0.012 to 0.072, but manual improvement (A), whose α is also an unsourced prior, becomes the modal winner in 6 of 15 processes. C becomes modal only if A is cut too or h runs up to 0.80 [S]. With A held to NAO manual-casework throughput realization (g0403-01, r_A ~ tri(0.475, 1.0, 1.2) [I]) at the current m = 1.77, A01 routing is modal in 5 processes (P03, P07, P11, P13, P14) and A in 1 (P08); assistance is still modal nowhere [S] [V wave 41C] [V wave 37C]
3. **The result turns on two unmeasured numbers.**
   - **The escaped-error cost (m).** At m = 20 the routing pool ($44k) falls below the assist pool. At m = 50 it is $0.
   - **The share of high-confidence cases (h).** At h = 0.10 the routing pool ($328k) is below assist. At h ≥ 0.21 it is above.
   - Under full QA of compliance processes (k = 1, CAL_COMPLIANCE_FULL), routing still clears P07's fixed cost in 38% of draws, against 0.03% for assistance.

### (B) Exception share per grant rather than per recipient line [C/I]

- **Coverage.**
  - Six top-50 sponsors are in the pools.
  - Three publish annual counts in their own reports: Fidelity, NPT and Vanguard.
  - Three state counts in their own Form 990 Part III: Goldman Sachs Philanthropy Fund, Ayco and T. Rowe Price.
  - That is 12 sponsor-years and 5.61m grants.
  - Three more sponsors were read but kept out of the pools because their dollar or recipient figures fail a consistency check (§B4).
- **Core proxy.** About **7–8.5% of grants** at the three report sponsors, against 7.5% of recipient lines and 10.2% of dollars for the same sponsor-years.
  - The figure is stable across the grant-size rule (β = 0 to 1), provided unitemised small recipients are flagged at the rate of the smallest itemised lines.
  - If none of the unitemised recipients is flagged, it falls to 2.8–7.9%.
- **Broad proxy.** **17–31% of grants**, against 28.0% of lines and 17.5% of dollars. Here the grant-size rule decides the answer.
- **By category, the per-grant shares rank differently from the line shares.**
  - **Foreign:** 0.05–0.9% of grants. NPT publishes **0.31%** (335 of 106,235 grants in FY2023; 406 of 129,575 in FY2024), against 2.6% of its recipient lines and 7.5% of its dollars on its whole-entity Form 990. The annual report covers the US DAF program only; on its own figures international grants are 5.9% (FY2023) and 6.4% (FY2024) of grant dollars [F/C] [V wave 36B]
  - **Fiscal sponsors:** 0.01–1.6%.
  - **PF/ER:** 0.4–0.8%.
  - **Recent rulings:** 4.6–5.7%.
  - **Not in Pub 78:** 10–25%, made up mostly of churches and group subordinates.
- **What drives the count.** The categories that dominate the count of exceptions are those with many small, repeated grants. Large-ticket categories shrink when counted by grant.

---

## Part A. Confidence-gated routing variant of intervention C (P-G04-01)

### A1. What is being tested

The calibrated model values C as an assistant on every AI-amenable case:

> C_assist = s·a_p·L − 0.5·q_p·L − inference

Here q_p = r·a_p, and it is charged only to AI-handled cases ([gap19-ai-calibration.md](gap19-ai-calibration.md) §3).

The calibration doc itself names the gap (§6 item 5). E19 and E17 indicate that routing (AI alone on high-confidence cases, humans alone on the rest) can beat assistance, and the model does not represent routing.

The variant below replaces the structure of C and keeps everything else the same, on common random numbers. The parts kept are:
- the pools, A, B and D;
- the fixed costs and inference;
- the platform terms and sponsor bootstraps.

### A2. Method

**Formula [I]**

```
C_route  = h·a_p·L·[(1 − ρ) − 0.5·k − k·e − (1 − k)·e·m] − inference
C_hybrid = C_route + (1 − h)·(s·a_p·L − 0.5·q_p·L)
```

- h is the share of AI-amenable cases closed by AI alone.
- k is the second-line QA sampling share of AI-closed cases, charged at half handling time (the model's existing 0.5 convention).
- e is the excess error rate of AI-closed cases over human handling.
- Sampled errors are reworked at full handling time. Unsampled errors escape and cost m handling-units each.
- ρ is any residual human time on an AI-closed case.
- The low-confidence remainder is handled by humans as today in `route`, and is AI-assisted in `hybrid`.
- Inference is charged on every amenable case, as in C.
- The fixed cost is the calibrated F_C draw; the sweep raises it ×1.5 and ×2.

**Routing parameters.** These are drawn per iteration from `Random(42 + 104729)`, so the calibrated draws are untouched.

| Parameter | Main Monte Carlo | Evidence | Sweep [I] |
|---|---|---|---|
| h | uniform(0.21, 0.49) | **E19** Agarwal, Moehring, Rajpurkar & Salz, NBER w31422 (rev. Aug 2026), §6.3 [F]: at high false-negative cost, "21% of cases are delegated to the AI" for Bayesian deciders; with observed behaviour "humans are involved in 51% of cases" (so 49% go to AI alone). At low cost "the AI decides almost all cases". Mapping radiology cases to DAF AI-amenable back-office cases is [I] | 0.10, 0.21, 0.35, 0.49, 0.70, 0.90 |
| e | uniform(0, 0.10) | Lower end: E19, where AI alone outperforms AI-assisted humans in the delegated range (excess error ≤ 0). Upper end: E15, where auto-closing AML alerts would miss about 10% of true positives (a share of positives, not of closed alerts, so [I]; per closed alert E15 implies at most 0.39%, so the 0.10 now rests on the OCBC invoice benchmark’s 10% error budget, CB-04) [V wave 37C] | 0, 0.02, 0.05, 0.10, 0.20, 0.40. The values 0.20 and 0.40 are the mode and top of the calibrated unconditional error range: confidence carries no information |
| k | triangular(0.03, 0.10, 0.30); k = 1 for P01, P07, P08 and P14 under CAL_COMPLIANCE_FULL | v2's QA range, which the calibration keeps as **unsourced**. No source measures a second-line QA sampling rate. E16 (2% of financial-firm AI use cases fully autonomous) is the basis for the k = 1 stress | 0.02, 0.05, 0.10, 0.30, 1.0 |
| ρ | 0 | Definition in E19: AI-alone decisions take zero human time | 0, 0.10, 0.25, 0.50 |
| m | sweep only: 1, 5, 20 in the headline | **No evidence** | 0, 1, 5, 20, 50 |
| F_C multiplier | 1 | — | 1, 1.5, 2 |

**Scenarios and outputs**
- Four calibrated scenarios: CAL_CENTRAL, CAL_FIELD_INLOOP, CAL_TASK_REVIEW and CAL_COMPLIANCE_FULL.
- Six archetypes, 10,000 draws each.
- One-at-a-time sweeps for NAT_LARGE, NAT_MID and CF_1BN under CAL_CENTRAL, plus an h × e grid for NAT_LARGE.
- The observed-population network break-even uses 2,000 draws.

**Intervals**
- Probabilities carry 95% Wilson intervals for Monte Carlo error.
- Value pools carry p25–p75 and p05–p95 across draws.
- Sponsor counts carry p25–p75.
- The assumption range is shown by the sweeps, not by these intervals.

**Replication**
- The `assist` rows reproduce the calibrated model draw for draw.
- Large national: $444,899 against $445k (CAL_CENTRAL); $202,101 against $202k (FIELD); $793,371 against $793k (TASK).
- P(C first) 0.0021 against 0.002.
- Observed-population P(reachable): 0.1645 against 0.165, and 0.036 against 0.036 for all community foundations [C].

### A3. Results [S]

**Value pool by archetype, CAL_CENTRAL.** Each cell is the p50 of the sponsor AI gross value (sum of positive C over P01–P15); p25–p75 are in the CSV.

| Archetype | Assist | Route m=1 | Route m=5 | Route m=20 | Hybrid m=1 |
|---|---:|---:|---:|---:|---:|
| NAT_LARGE | $445k | $1.36m | $1.06m | $44k | $1.79m |
| NAT_MID | $49.2k | $165k | $127k | $0 | $215k |
| CF_1BN | $69.4k | $191k | $151k | $10.7k | $246k |
| CF_250M | $17.8k | $48.0k | $38.0k | $2.2k | $61.9k |
| CF_SMALL | $2.40k | $7.06k | $5.58k | $0.29k | $9.08k |

**Mean P(C ranks first, gross), P01–P15, CAL_CENTRAL**

| Archetype | Assist | Route m=1 | Route m=5 | Route m=20 | Hybrid m=1 |
|---|---:|---:|---:|---:|---:|
| NAT_LARGE | 0.0021 (0.0019–0.0024) | 0.0123 (0.0118–0.0129) | 0.0049 | 0.0014 | 0.0388 (0.0379–0.0398) |
| NAT_MID | 0.0021 | 0.0122 | 0.0051 | 0.0014 | 0.0377 |
| CF_1BN | 0.0023 | 0.0140 | 0.0058 | 0.0016 | 0.0432 |
| CF_250M | 0.0023 | 0.0138 | 0.0058 | 0.0015 | 0.0428 |

**Break-even, CAL_CENTRAL.** Each cell is P(vendor break-even ≤ the sponsors available in the archetype window).

| Archetype (available) | Assist | Route m=1 | Route m=5 | Route m=20 | Hybrid m=1 |
|---|---:|---:|---:|---:|---:|
| NAT_LARGE (5) | 0.13 | 0.38 | 0.29 | 0.09 | 0.48 |
| NAT_MID | 0.002 | 0.016 | 0.007 | 0.002 | 0.036 |
| CF_1BN (20) | 0.029 | 0.112 | 0.070 | 0.020 | 0.184 |
| CF_250M (58) | 0.004 | 0.020 | 0.011 | 0.003 | 0.041 |

**Observed FY2024 population** (vendor signs the most valuable sponsors first). Each cell is P(break-even reachable).

| Segment | Assist | Route m=1 | Route m=5 | Route m=20 | Hybrid m=1 |
|---|---:|---:|---:|---:|---:|
| Community foundations under $250m | 0.000 | 0.002 | 0.000 | 0.000 | 0.004 |
| All community foundations | 0.036 | 0.154 | 0.088 | 0.021 | 0.275 |
| Nationals under $10bn | 0.001 | 0.017 | 0.005 | 0.002 | 0.051 |
| CF + nationals under $10bn | 0.066 | 0.264 | 0.170 | 0.043 | 0.408 |
| CF + all nationals | 0.165 | 0.473 | 0.335 | 0.101 | 0.646 |

**Processes where C was competitive**

All rows are large national, CAL_CENTRAL. "Break-even h" is the h at which C_route clears F_C, with the other routing parameters at their drawn values. Values above 1 mean unreachable.

| Process | Assist: P(first) / P(net > 0) | Route m=1: P(first) / P(net > 0) | Break-even h, p50 (p25–p75) | P(break-even h ≤ 0.49) | h needed to rank first (p50) |
|---|---|---|---|---|---|
| P03 complex assets | .016 / .062 | .094 / .207 | 0.77 (0.40–1.45) | 0.32 | 0.58 |
| P07 non-standard due diligence | .013 / .307 | .075 / .635 | **0.24 (0.12–0.45)** | **0.77** | 0.62 |
| P11 service inquiries | .0005 / .105 | .004 / .305 | 0.57 (0.30–1.08) | 0.44 | 0.96 |
| P14 AML alerts | .001 / .010 | .005 / .043 | 2.04 (0.97–4.23) | 0.09 | 0.82 |
| P01 KYC | 0 / 0 | .0002 / 0 | 8.5 | 0 | 1.17 |

- **Smaller sponsors.** At mid nationals and community foundations, routing lets C clear its fixed cost in at most **3.6%** of draws in any process (P07 at CF_1BN, m = 1). For assistance the maximum is 0.7%. At CF_250M it is 0%.
- **Compliance stress (k = 1 on P01, P07, P08 and P14).**
  - Routing at a large national gives a pool of $985k (m = 1) and $455k (m = 20).
  - Full sampling removes escaped errors, so the result barely moves with m.
  - P07 clears its fixed cost in 37.6% of draws, against 0.03% for assistance.

**Sweeps** (large national, CAL_CENTRAL, route, m = 1 unless stated)

| Parameter | Values → mean P(C first) / pool p50 |
|---|---|
| h | 0.10 → 0 / $328k; 0.21 → 0.0001 / $773k; 0.35 → 0.008 / $1.37m; 0.49 → 0.044 / $1.98m; 0.70 → 0.146 / $2.89m; 0.90 → 0.262 / $3.77m |
| e | 0 → 0.016 / $1.45m; 0.05 → 0.012 / $1.36m; 0.10 → 0.009 / $1.28m; 0.20 → 0.004 / $1.10m; 0.40 → 0.0004 / $764k |
| k | 0.02 → 0.018 / $1.47m; 0.10 → 0.014 / $1.40m; 0.30 → 0.008 / $1.23m; 1.0 → 0.0001 / $642k |
| m | 0 → 0.016 / $1.44m; 1 → 0.012 / $1.36m; 5 → 0.005 / $1.06m; 20 → 0.0014 / $44k; 50 → 0.0005 / $0 |
| ρ | 0.10 → 0.007 / $1.19m; 0.25 → 0.002 / $938k; 0.50 → 0.00004 / $522k |
| F_C × | P07 P(net > 0): 0.635 (×1), 0.484 (×1.5), 0.372 (×2) |

**h × e grid** (large national, m = 1; full grid in the CSV, `cell = grid_h=…_e=…_m1`)
- The routing pool exceeds the assist pool ($445k) for every e ≤ 0.20 once h ≥ 0.21.
- P(C first) exceeds assistance's 0.002 only from h = 0.35 (with e ≤ 0.10; at e = 0.20 it equals it).
- P(C first) reaches 0.15 or more only at h ≥ 0.70.

### A4. Verdict on the hypothesis [S/I]

- **Supported for value and break-even.**
  - Under assistance, C's value is capped at s·a_p. With s calibrated to 0–0.30 (field) or 0.10–0.56 (task), that cap was the main source of the 60% cut.
  - Routing replaces s with h·(1 − ρ − QA − error cost) per amenable case. At E19's h range this is 0.2–0.5 of amenable labour.
  - Hence a large-national pool 2.4–3.1× the assist pool and a platform break-even rising from 13% to 29–38% of draws (m = 5 to 1). Both depend on the unsourced m and on ρ = 0 [V wave 36B]
- **Not supported for ranking.**
  - Even with routing, C ranks first in about 1% of process-draws, and no modal winner changes inside the evidence range.
  - C's weakness in ranking is therefore not an artefact of the assist formula. It comes from a_p ≤ 0.6 and from the v1 priors of A, B and D: cutting B and D alone hands processes to A, not to C [S] ([g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md)). [V wave 37C]
  - Those priors were never calibrated (proposal P-G0401-03).
- **The new weak point is different.**
  - Routing swaps one inference (s from production field studies) for another: h from one radiology experiment, and m from no source at all.
  - The routing case is only as strong as the evidence that a DAF back office can close 20–50% of amenable cases without review and that an escaped error costs a few handling-times, not tens.

### A5. Limits (Part A)

1. **The h evidence is one study in another domain** (E19, radiology; with E15's single-bank ML triage as context). No public DAF or financial back-office study reports the share of cases auto-closed under a confidence threshold together with the error rate in that band (P-G0401-01).
2. **e is bounded, not measured.** E15's 10% is a share of true positives missed. The E15 full text gives the prevalence (“less than 3% of the alerted ones”, p. 3), which converts it to at most 0.39% per closed alert (about 0.77% at the baseline’s ~80% recall) [C] ([g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md) CB-01c). The 0.10 upper end therefore no longer rests on E15. [V wave 37C]
3. **m (the cost of an escaped error) is only indirectly sourced** and dominates the result (P-G0401-02). Wave 38B bounds it at 1.0–106 (central 2.4), but detection probability, the bank-to-DAF transfer and operational rework remain unsourced (P-G0403-04). [V wave 38B] After wave 38B’s P08 correction the range is 1.0–88.5 (central 2.20). Detection probability is now bounded from IRS data at 0.0012–0.0099 (average-filer coverage), which lowers the central to 1.56–1.77. The bank-transfer or sanctions-pricing term and operational rework remain unsourced [V wave 39B] k is still v2's unsourced QA range.
4. **Structure.** Routing is applied per process with one global h per draw. In practice h would differ by process, being higher for P11 and P02-type intake and lower for P07 and P08.
5. **Unchanged assumptions.** The calibrated model's other assumptions (φ, d, β, b, fixed costs, τ) are unchanged and still set net results and network break-even.
6. **Interval types.** The intervals in §A3 are Monte Carlo error (Wilson) or the across-draw spread. Neither is a confidence interval on the routing parameters, whose uncertainty is shown only by the sweeps.

---

## Part B. Exception share per grant (P-G05-02)

### B1. The question

The exception-load proxy reports shares of **recipient lines** (one Schedule I line per recipient per return, itemised only above $5,000) and of **dollars**. A grant-count share needs three things:
- the sponsor's own grant count;
- an allocation of grants across recipients;
- the grants to recipients below the $5,000 itemisation threshold, which Schedule I omits.

### B2. Grant counts collected

robots.txt was read for each host first (§S2).

| Sponsor (rank) | DAFRC FY | Grants G | Distinct recipients R | Source and period match |
|---|---|---:|---:|---|
| Fidelity Charitable (1) | 2023 | 2,262,841 | 199,500 | Mean of CY2022 (2,185,516 grants; "nearly 200,000" charities) and CY2023 (2,340,165; "199K") [F → C]. 990 year ends 30 June |
| Fidelity Charitable | 2024 | 2,502,306 | 206,238 | Mean of CY2023 and CY2024 (2,664,446 grants; 213,476 charities) [F → C] |
| National Philanthropic Trust (2) | 2023 | 106,235 | 36,000 | Annual report chart, FY ended June 2023 (same period). R from the FY2023 990 Part III ("approximately 36,000") [F] |
| NPT | 2024 | 129,575 | 41,000 | Annual report chart, FY ended June 2024. R "over 41,000" (990 Part III) [F] |
| Vanguard Charitable (4) | 2023 | 202,500 | 54,772 | Mean of CY2022 ("196K" grant units; 52,800 organizations) and CY2023 ("209K"; 56,744) [F → C]. Rounded counts |
| Vanguard Charitable | 2024 | 224,532 | 59,665 | Mean of CY2023 and CY2024 (240,064; 62,586) [F → C] |
| Goldman Sachs Philanthropy Fund (5) | 2023 / 2024 | ~24,800 / ~29,254 | not published (imputed [I]) | Form 990 Part III, same CY returns [F] |
| Ayco Charitable Foundation (21) | 2023 / 2024 | ~32,400 / ~35,675 | not published (imputed [I]) | Form 990 Part III [F] |
| T. Rowe Price Program (46) | 2023 / 2024 | "nearly 29,000" / "nearly 32,000" | "over 11,000" / "over 13,000" | Form 990 Part III, FY ending March [F] |
| *Excluded from pools* | | | | |
| CF for Greater Atlanta (29) | 2023 / 2024 | 12,000 / 11,835 | 3,300 / 3,000 | Fails the unitemised check: $11.5k–$13.2k per unitemised recipient, above $5,000 |
| CF of New Jersey (35) | 2023 / 2024 | 8,000 / 8,340 | — | Stated dollars ($100m / $124m) are 1.5× and 1.2× Part IX ($64.7m / $100.6m) |
| Jewish Community Foundation of LA (37) | 2024 | 14,000 | 3,320 | Stated dollars ($207m) are 1.6× Part IX ($130.9m), and Schedule I exceeds Part IX |

**Consistency checks [C]**
- **NPT's two sources agree.** The 990 narratives ("approximately 107,000"; "more than 129,000") match the annual report's 106,235 and 129,575.
- **Source dollars against Part IX lines 1–3:**
  - Fidelity: 1.11 and 1.05;
  - NPT: 1.02 and 0.99;
  - Vanguard: 1.06 and 0.93;
  - Goldman Sachs and Ayco: exact.
- **Sponsors not used:**
  - DAFgiving360 and Schwab Charitable: their robots.txt returns HTTP 403, so they were not fetched.
  - AEF and NCF: their current pages and impact report give dollars and charities, not grant counts.
  - Renaissance and BofA CGF: they state counts (Renaissance: "over 130,000" and "over 160,000" grants) but have no e-file Schedule I lines.

### B3. Method and assumptions

1. **Recipient groups per sponsor-year.**
   - **Itemised:** Schedule I lines with amount > 0, using the proxy's flags unchanged (`line_flags`). For the 12 pooled sponsor-years, the line shares of the core and broad unions reproduce the proxy CSV to within ±5×10⁻⁷ (maximum 4.8×10⁻⁷), which is CSV rounding [C].
   - **Foreign:** Schedule F recipients, each at the mean of line 3 dollars.
   - **Unitemised:** R_U = R − itemised − foreign recipients, sharing D_U = Part IX lines 1–3 − Schedule I − line 3.
   - Where R is unpublished (Goldman Sachs, Ayco), R is imputed from the published R ÷ (itemised + foreign) ratios, which run from 2.12 to 5.24. The pools use the low end; the CSV carries both ends [I].
2. **Grants per recipient (the key assumption) [I].**
   - n_i = max(1, k·d_iᵝ), where d_i is the recipient's dollars and k is solved so that Σn_i equals the sponsor's published G.
   - β = 0: every recipient gets the same number of grants, so exception categories scale with recipients.
   - β = 1: every grant has the same size, so categories scale with dollars.
   - The floor of 1 is logical: every listed recipient received at least one grant.
   - β is swept over {0, 0.25, 0.5, 0.75, 1}, with a finer 0.05 grid for the calibration moments.
3. **Flags for unitemised recipients [I], swept:**
   - `none`: no unitemised recipient is flagged (lower bound).
   - `small_band`: each category's line share among itemised lines of ≤ $10,000, the nearest observed size band.
   - `all_itemised`: the line share across all itemised lines.
4. **Foreign rule [I].**
   - `model`: Schedule F recipients follow the β rule.
   - `anchored`: each Schedule F recipient gets 528/323 = 1.63 grants, from NPT's FY2025 annual report ("528 international grants worth $310.0 million to 323 organizations"). This transfers one sponsor's ratio to all sponsors.
5. **Pooling.** Pools are grant-weighted (Σ flagged grants ÷ Σ G). They include only sponsor-years whose source dollars are within 20% of Part IX and whose unitemised mean is ≤ $5,000. T. Rowe Price states no dollar figure, so only the unitemised test applies to it [V wave 36B]

### B4. Results [C under stated assumptions]

**Pooled, three annual-report sponsors** (6 sponsor-years, 5.43m grants; Fidelity is 88% of the grants)

The comparison bases for the same sponsor-years are recipient lines (233,431) and dollars ($37.78bn).

| Category | Lines | Dollars | Per grant: β = 0 | β = 0.5 | β = 1 | Range over all rules (excluding `none`) |
|---|---:|---:|---:|---:|---:|---:|
| Foreign | 0.52% | 2.31% | 0.12% | 0.67% | 0.69% | 0.05–0.87% |
| Not 501(c)(3) / not in Pub 78 (raw) | 22.18% | 7.68% | 25.11% | 19.97% | 10.11% | 9.96–25.13% |
| … unexplained | 2.35% | 1.02% | 2.77% | 2.11% | 1.30% | 1.26–2.77% |
| Recent ruling (≤ 24 months) | 4.96% | 4.47% | 5.70% | 5.14% | 4.64% | 4.59–5.70% |
| Fiscal-sponsor name | 0.04% | 1.65% | 0.01% | 0.20% | 1.56% | 0.01–1.58% |
| PF / ER | 0.42% | 1.47% | 0.47% | 0.50% | 0.82% | 0.42–0.83% |
| **Broad union** | **27.97%** | **17.47%** | **31.24%** | **26.33%** | **17.71%** | **16.98–31.24%** |
| **Core union** | **7.49%** | **10.15%** | **8.21%** | **7.84%** | **8.46%** | **6.99–8.46%** (2.80% with `none`) |

The per-grant columns use the `small_band` unitemised rule and the `model` foreign rule.

**Other pools**, under `small_band` and `model`, as core / broad at β = 0, 0.5 and 1:
- **Six sponsors** (12 sponsor-years): core 8.08 / 7.74 / 8.33%; broad 30.8 / 26.0 / 17.6%.
- **Excluding Fidelity:** core 6.33 / 8.10 / 8.32%; broad 23.3 / 21.7 / 17.1%.
- **The three 990-narrative sponsors:** core 4.38 / 4.79 / 4.53%; broad 17.8 / 16.9 / 13.9%. Their lines are 4.98% core and 15.38% broad; their dollars 10.36% and 14.26%.

**Per sponsor-year**

| Sponsor | FY | Lines: core / broad | Dollars: core / broad | Per grant, core: β = 0 / 0.5 / 1 | Per grant, broad: β = 0 / 0.5 / 1 |
|---|---|---|---|---|---|
| Fidelity | 2023 | 7.5 / 30.6 | 8.0 / 17.0 | 8.4 / 7.7 / 8.1 | 32.6 / 27.6 / 17.9 |
| Fidelity | 2024 | 7.6 / 29.9 | 8.5 / 16.6 | 8.4 / 7.6 / 8.6 | 31.7 / 26.1 / 17.5 |
| NPT | 2023 | 9.6 / 23.0 | 15.7 / 21.3 | 8.7 / 14.0 / 13.7 | 23.0 / 24.7 / 21.7 |
| NPT | 2024 | 9.5 / 22.5 | 15.8 / 20.2 | 8.4 / 14.3 / 13.8 | 22.7 / 24.4 / 20.8 |
| Vanguard | 2023 | 5.5 / 25.0 | 5.7 / 12.6 | 6.0 / 5.8 / 5.8 | 27.0 / 22.5 / 15.4 |
| Vanguard | 2024 | 5.8 / 24.1 | 8.4 / 15.3 | 5.9 / 6.5 / 8.0 | 25.1 / 22.0 / 17.1 |
| Goldman Sachs (R imputed low) | 2023 | 6.5 / 13.1 | 13.7 / 17.3 | 6.2 / 8.6 / 10.2 | 12.8 / 14.6 / 15.2 |
| Goldman Sachs (R imputed low) | 2024 | 6.5 / 12.7 | 10.0 / 13.1 | 6.7 / 8.1 / 8.5 | 12.8 / 13.5 / 12.9 |
| Ayco (R imputed low) | 2023 | 3.3 / 14.6 | 1.5 / 8.4 | 3.6 / 3.0 / 1.9 | 14.3 / 13.2 / 9.2 |
| Ayco (R imputed low) | 2024 | 3.1 / 14.0 | 1.8 / 7.5 | 3.6 / 3.0 / 2.1 | 14.2 / 12.7 / 8.6 |
| T. Rowe Price | 2023 | 4.2 / 25.0 | 3.3 / 16.6 | 3.6 / 3.8 / 3.3 | 25.7 / 23.8 / 19.4 |
| T. Rowe Price | 2024 | 3.8 / 24.3 | 3.0 / 16.0 | 3.2 / 3.5 / 3.0 | 26.4 / 23.9 / 19.5 |

All values are percentages. "Dollars" are itemised dollars, i.e. Schedule I plus line 3.

**Unitemised group [C]**
- Per sponsor-year the mean per unitemised recipient is:
  - Fidelity: $1,449 (FY2023) and $849 (FY2024);
  - NPT: $1,088 and $439;
  - Vanguard: $1,715 and $1,843;
  - T. Rowe Price: $1,241 and $1,094.
- All are below $5,000, so the group is consistent with the itemisation threshold.
- Unitemised recipients are 126,000–127,000 at Fidelity, about 20,000–22,000 at NPT and 33,000–35,000 at Vanguard. They take between 1 grant each (β = 1) and the sponsor's average grants per recipient (β = 0).

### B5. Calibration moments: what the public data say about β [F/C]

- **Fidelity's grants of $1 million or more.**
  - Published: 1,407 in 2022, 1,345 in 2023 and 1,971 in 2024; FY means 1,376 and 1,658.
  - The model, counting lines whose mean grant is ≥ $1m, gives 930–1,370 at β = 0–0.05. It falls to 350–670 at β = 0.25–0.35 and to 0 for β ≥ 0.40.
  - The line-mean approximation understates large grants, so this only weakly favours β ≤ 0.35. It does not fix β.
- **NPT's international grants.**
  - Published per-grant share: 0.315% (FY2023) and 0.313% (FY2024).
  - The modelled foreign share is 1.2% at β = 0 and 5.6% at β = 1; the anchored rule gives 0.63–0.69%.
  - **No β fits.** NPT's 990 lists more Schedule F foreign recipients (413 and 488) than its report lists international grants (335 and 406, "U.S. donor-advised fund program only"). Schedule F counts therefore cannot be read as grant counts (P-G0502-02).
  - Foreign grants are **0.31% of grants** on NPT's annual-report basis (US DAF program only), and **2.6% of recipient lines and 7.5% of dollars** on its whole-entity Form 990 (FY2023–24). The report's own international dollar share is 5.9% and 6.4% ($269.08m of $4.54bn; $352.23m of $5.49bn), so the two bases should not be compared directly [F/C] [V wave 36B]
- **Reading [I].**
  - The two moments point the same way. Large-ticket exception categories (foreign, fiscal sponsors, private foundations) are a much smaller share of grants than of dollars, and at or below their share of lines.
  - The count-heavy categories (recipients absent from Pub 78, recent rulings) are at least their line share.
  - The core union stays near 7–8.5% because these two effects offset.

### B6. Limits (Part B)

1. **β is not identified.** No public source gives grants per recipient against recipient dollars, so the broad share (17–31%) depends on an assumption that is swept, not estimated (P-G0502-01).
2. **Period mismatch.** Fidelity and Vanguard publish calendar years, while their 990 years end in June. Fidelity's 2023 Giving Report charts 188,777 charities for CY2022 (its text says “189,000” three times and “nearly 200,000” once); the 200,000 used here overstates FY2023 R by about 5,600. With 188,777, the pooled core range is unchanged and broad shares move by at most 0.02 pp [C] [V wave 36B] The FY counts are means of two calendar years [C], and Vanguard's FY2022–23 counts are rounded ("196K", "209K").
3. **Imputed R.** R is imputed for Goldman Sachs and Ayco. The imputation range (2.1–5.2×) moves Goldman Sachs' core per-grant share from 6.0% to 10.2% (CSV `r_case`).
4. **Within-recipient heterogeneity is ignored.** The unitemised group uses a mean amount, and every grant on a line is treated as equal in size.
5. **Narrow coverage.** Only six sponsors are pooled, and Fidelity is 88% of report-sponsor grants. DAFgiving360, the second-largest by count, could not be fetched (robots.txt 403). Community foundations are absent from the pools because their stated counts fail the consistency checks.
6. **Inherited proxy limits.** The proxy's own limits are inherited: Pub 78 and BMF snapshots, name-rule fiscal-sponsor matching (replaced by an EIN-keyed host list in [g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md), which moves the core to 7.76% / 11.61%) [V wave 39C], and a screen of review need rather than observed review ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md) §5).

---

## Reproduction

```
python3 scripts/mission_ai_routing_variant.py .            # about 17 min; --draws N for a quicker run
python3 scripts/mission_exception_per_grant.py . --np-cache $S/npcache --lines-cache $S/rcp/lines \
    --bmf-dir $S/rcp/bmf --pub78 $S/irs/data-download-pub78.txt   # ~25 s
```

- `$S` holds the same caches as `mission_exception_load.py`.
- The grant counts are constants in `GRANT_COUNTS`, each with its URL.
- Re-running the per-grant script reproduced its CSV byte for byte.

## D1. Data dictionary: `ai-routing-variant-2026-11-19.csv`

| Column | Meaning |
|---|---|
| scenario | CAL_CENTRAL, CAL_FIELD_INLOOP, CAL_TASK_REVIEW or CAL_COMPLIANCE_FULL (calibrated model scenarios); `ALL` for spec and meta rows |
| archetype | NAT_LARGE, NAT_MID, CF_1BN, CF_250M, CF_SMALL, REF_V1_1M; `OBSERVED_POPULATION` for network rows |
| variant | `assist` (calibrated C, replication), `route` (C_route), `hybrid` (C_route plus assistance on the low-confidence rest); `spec` / `meta` |
| cell | `calibrated` (assist); `main_m{1,5,20}` (main Monte Carlo at escaped-error cost m); `sweep_{param}={value}[_m1]` (one-at-a-time sweep, other routing parameters at their main draws, m = 1 unless the sweep is m); `grid_h={h}_e={e}_m1` |
| process_id | P01–P16 for process rows; the network segment for `OBSERVED_POPULATION` rows; blank for sponsor-level rows |
| metric | `mean_p_C_rank_first_{gross,net}_P01_P15`; `sponsor_ai_gross_value_p50` (lo/hi = p25/p75); `sponsor_ai_gross_value_p05_p95` (lo/hi = p05/p95); `max_process_p_C_net_positive`; `p_vendor_breakeven_finite`; `vendor_breakeven_sponsors_p50_finite` (lo/hi = p25/p75); `p_vendor_breakeven_le_available`; `processes_modal_winner_changed_gross_vs_assist` (note lists the changes); process-level `p_C_rank_first_gross`, `p_C_net_positive`, `C_gross_p50`, `modal_winner_gross`, `breakeven_h_net_p50`, `p_breakeven_h_net_le_0.49`, `breakeven_h_rank_first_p50`; network `p_breakeven_reachable`, `breakeven_sponsors_p50_reachable`; spec rows `{param}_{distribution}` |
| value, lo, hi | Value and interval. Probabilities: 95% Wilson interval for Monte Carlo error. Values and sponsor counts: quantiles as stated in `note` |
| unit, note | Unit; interval definition or evidence basis |

## D2. Data dictionary: `exception-share-per-grant-2026-11-19.csv`

| Column | Meaning |
|---|---|
| scope | `sponsor_year`; `pooled_all_usd_consistent`, `pooled_annual_report_sponsors`, `pooled_990_narrative_sponsors`, `pooled_ex_fidelity` (grant-weighted); `meta` |
| sponsor, ein, fiscal_year | Sponsor, EIN, DAFRC fiscal year of the Schedule I return |
| source_tier | `annual_report` (sponsor's own report) or `form990_part_iii` (sponsor's own 990 narrative) |
| beta | Grant-size elasticity in n_i = max(1, k·d_iᵝ) [I] |
| unitemised_rule | `none`, `small_band` (line share among itemised lines ≤ $10,000) or `all_itemised` [I] |
| foreign_rule | `model` (β rule) or `anchored` (1.63 grants per Schedule F recipient, NPT FY2025) [I] |
| r_case | `published` R, or `imputed_low` / `imputed_high` (ratio bounds) [I] |
| metric | Inputs: `published_grants_G`, `distinct_recipients_R`, `source_grant_usd`, `part_ix_total_grants_usd`, `source_usd_over_part_ix`, `schedule_i_lines_positive`, `schedule_f_foreign_recipients`, `unitemised_recipients_R_U`, `unitemised_usd_D_U`, `unitemised_mean_per_recipient`, `tax_period_end` (note = object id), `pool_eligible`. Results: `per_grant_share` (by category), `per_grant_share_fine` (0.05 β grid), `recipient_line_share` and `itemised_dollar_share` (proxy basis, recomputed), `check_line_share_minus_proxy`, `model_grants_{itemised,unitemised,foreign}`, `model_avg_unitemised_grant`, `model_grants_ge_1m(_fine)`, `solver_feasible`, `published_grants_ge_1m`, `published_international_grant_share`; `members` and `R_over_listed_ratio_bounds` |
| category | foreign, not_c3_or_not_pub78, not_c3_or_not_pub78_unexplained, recent_ruling_24m, fiscal_sponsor_name, pf_or_er, er_required, any (broad), any_core (core), as defined in the proxy §1.4 |
| value, unit, note | Value, unit, provenance (URLs on `published_grants_G` rows) |

## S1. Source register

| ID | Source | Used for | Access |
|---|---|---|---|
| E19 | Agarwal N, Moehring A, Rajpurkar P, Salz T. *Combining Human Expertise with Artificial Intelligence: Experimental Evidence from Radiology*. NBER WP 31422 (July 2023, revised August 2026), §6.3 and Figure 10. https://www.nber.org/system/files/working_papers/w31422/w31422.pdf (doi:10.3386/w31422) | h range (21% and 49% AI-alone shares); e lower bound | PDF fetched 2026-11-19; nber.org robots.txt does not disallow /system/files/ |
| E15 | Eddin AN et al. *Anti-Money Laundering Alert Optimization Using Machine Learning with Graphs*. arXiv 2112.07508 (2021). https://arxiv.org/abs/2112.07508 | e upper bound (about 10% of true positives missed) | Quoted from `ai-calibration-evidence-2026-11-19.csv`; not re-fetched |
| E16 | Bank of England and FCA. *Artificial intelligence in UK financial services – 2024*. https://www.bankofengland.co.uk/report/2024/artificial-intelligence-in-uk-financial-services-2024 | k = 1 compliance stress (2% of use cases fully autonomous) | Quoted from the evidence CSV |
| E17 | Choi JH, Xie C. *Human + AI in Accounting*. *Journal of Accounting Research* (2026). https://doi.org/10.1111/1475-679x.70052 | Confidence-gated review as observed practice (no magnitude used) | Quoted from the evidence CSV |
| — | Calibrated model and its evidence: [gap19-ai-calibration.md](gap19-ai-calibration.md); `ai-calibration-evidence-2026-11-19.csv` (E01–E21) | s, q, a ranges and all non-routing parameters | Repo |
| F1 | Fidelity Charitable *2023 Giving Report*: https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf | CY2022: 2,185,516 grants, $11.20B; "nearly 200,000 unique nonprofits"; 1,407 grants ≥ $1m | Fetched 2026-11-19 |
| F2 | Fidelity Charitable *2024 Giving Report*: https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf | CY2023: 2,340,165 grants, $11.8B; 199K unique charities; 1,345 grants ≥ $1m | Fetched 2026-11-19 |
| F3 | Fidelity Charitable *2025 Giving Report*: https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf | CY2024: 2,664,446 grants, $14.9B; 213,476 charities; 1,971 grants ≥ $1m | Fetched 2026-11-19 |
| N1 | NPT annual report (FY2025 edition, with FY21–FY25 charts): https://www.nptrust.org/annual-reports/npt-annual-report/ | Grants FY21–FY25: 87,490, 102,745, 106,235, 129,575, 159,543. Grant value: $6.46, 5.53, 4.54, 5.49, 6.44bn. International grants: 274, 286, 335, 406, 528. FY2025: 528 international grants to 323 organizations; 47,676 organizations | Fetched 2026-11-19; values read from the page's chart data attributes |
| V1 | Vanguard Charitable annual reports: https://www.vanguardcharitable.org/2022annualreport, /2023annualreport, /2024annualreport, /2025annualreport | Grants: 196K (2022), 209K (2023), 240,064 (2024), 267,838 (2025). Organizations: 52,800, 56,744, 62,586, 66,785 | Fetched 2026-11-19 |
| X1 | Sponsors' own Form 990 Part III narratives, e-file XML via the GivingTuesday mirror of IRS TEOS, `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`. Object ids: NPT 202431429349301368, 202511339349301311; GS 202413109349303336, 202503109349303645; Ayco 202413109349304401, 202543109349303959; T. Rowe Price 202321949349300147, 202401949349301515; CF Greater Atlanta 202540559349301329, 202523219349322912; CFNJ 202423209349302727, 202543189349311964; JCF LA 202533199349302138 | Grant and recipient counts | First 400 kB of each fetched by HTTP range request, 2026-11-19 |
| X2 | Exception-load proxy inputs: Schedule I and F lines, Pub 78 (Last-Modified 2026-11-11) and EO BMF (2026-11-09), per [gap19-exception-load-proxy.md](gap19-exception-load-proxy.md) §8 | Line flags and denominators | Existing scratch caches; no new bulk download |
| A1 | AEF home page https://www.aefonline.org/ and NCF *2025 Impact Report* https://site.ncfgiving.com/wp-content/uploads/2026/07/Impact-report-2025-compressed.pdf | Checked for grant counts: none published (AEF: "47,000+ distinct charities" in 2025; NCF: 38,507 charities) | Fetched 2026-11-19 |

## S2. robots.txt log (2026-11-19, UTC; user agent `research-script/1.0`)

| Host | robots.txt | Decision |
|---|---|---|
| www.nber.org | 200; `/system/files/` not disallowed | Fetched the E19 PDF |
| arxiv.org | 200; crawl-delay 15; /abs and /pdf allowed | Not fetched (E15 quoted from the repo) |
| www.fidelitycharitable.org | 200; disallows only /retired/, /sample-email/, /nuance/ and one /content/dam/…/vessel/ path | Fetched three Giving Report PDFs and the 2026 page |
| www.nptrust.org | 200; `User-agent: *` `Disallow:` (empty) | Fetched the annual report page |
| www.vanguardcharitable.org | 200; disallows /core/ and /profiles/ only | Fetched four annual-report pages |
| www.dafgiving360.org | **403** (Access Denied) | Not fetched; treated as disallowed |
| www.schwabcharitable.org | **403** | Not fetched |
| www.aefonline.org | 200; crawl-delay 10; empty Disallow | Two pages, 11 s apart |
| aefimpact.org | 200 (Bitly; empty Disallow) | One HEAD request (redirect only) |
| www.ncfgiving.com / site.ncfgiving.com | 200; empty Disallow / disallows /wp-admin/ only, crawl-delay 10 | Impact-report page and PDF |
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | Range requests for 100 Form 990 XML heads |
| www.trowepricecharitable.org | 404 (no rules) | Home page only; no grant count found |
| www.cfnj.org | 301 | Not fetched further |

- crt.sh, certspotter and sec.gov were not used.
- There was no outreach, no login and no form.
- All evidence is 2021 or later. Fidelity's 2015 baseline values appear in the reports but are not used.
