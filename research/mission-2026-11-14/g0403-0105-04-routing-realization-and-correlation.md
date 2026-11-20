# P-G0403-01-05 and P-G0403-01-04: realization on routing h, and correlated realization

*Prepared 2026-11-20. TASKID g0403-0105-04.*

**Outputs**
- [`scripts/mission_ai_realized_correlated.py`](../../scripts/mission_ai_realized_correlated.py). It imports [`mission_ai_a_calibrated.py`](../../scripts/mission_ai_a_calibrated.py) without modifying it; through that module it uses the recut, the routing variant, the calibrated model and v2, none of which is modified. Stdlib only (the copula uses `statistics.NormalDist`), functional style. Run: `python3 scripts/mission_ai_realized_correlated.py . --draws 10000` (about 4–5 minutes per archetype; five archetypes were run).
- [`data/mission-2026-11-14/ai-ranking-realized-correlated-2026-11-20.csv`](../../data/mission-2026-11-14/ai-ranking-realized-correlated-2026-11-20.csv): __NROWS__ rows. Data dictionary in §D1.
- [`data/mission-2026-11-14/queue-proposals-g0403-0105-04.csv`](../../data/mission-2026-11-14/queue-proposals-g0403-0105-04.csv): 5 proposals.
- No existing file was modified. Nothing was committed.

**Read first**
- [g0403-01-manual-improvement-calibration.md](g0403-01-manual-improvement-calibration.md) with its wave-41C corrections ([validation-wave41c-report.md](validation-wave41c-report.md)).
- [g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md) with its wave-37C corrections ([validation-wave37c-report.md](validation-wave37c-report.md)), which raised the h asymmetry: "B and D take an audited-realization haircut. Routing's h upper half gets none."
- [g0403-0104-m-detection-ofac.md](g0403-0104-m-detection-ofac.md) with its wave-39B corrections ([validation-wave39b-report.md](validation-wave39b-report.md)): m central 1.56 (OFAC analogue) to 1.77 (bank-SAR transfer), high 9.28; the composite "is not pinned down" (Amex per-alert pricing gives 13.7 / 128 / 1,269).

**Notation:** [F] published value, quoted; [C] computed here; [I] inference or assumption; [S] scenario output. All results are CAL_CENTRAL, gross, mean over P01–P15 of P(rank first), 10,000 draws, unless stated.

---

## 0. Answers in brief

### (A) Realization on the upper half of routing h (P-G0403-01-05)

- **No new evidence was found or fetched.** No 2021+ audit compares realized with claimed auto-close share for an AI or ML triage programme. The factor for C is therefore taken from **the same HUD and GSA OIG RPA audits used for B** (BD-E01: 7% of estimated hours realized programme-wide; BD-E02: one bot at about 30 of 90 minutes, 0.33), as **r_C ~ tri(0.07, 0.33, 1.00)**, and labelled [I] mapping. It is swept from 1.0 to 0.
- **How it enters.** Realized h is h_eff = min(h, 0.50) + r_C · max(0, h − 0.50). Only the part of A01's h ~ U(0.20, 0.80) above 0.50 is cut: that is the part resting on E15's retrospective 0.78 and State's self-reported 80%. A stress spec (C_ALL_FIELD) cuts the whole h.
- **With A, B, C and D all carrying a realized/planned factor (A_FIELD × BD_FIELD × C_UPPER_FIELD), NAT_LARGE [S]:**

| C variant | r_C spec | A | B | C | D | Modal winners P01–P15 | n modal A / C |
|---|---|---:|---:|---:|---:|---|---|
| Route A01, m = 1.56 | none (g0403-01) | 0.228 | 0.180 | 0.204 | 0.388 | ADCBDDCADDCBCCB | 2 / 5 |
| Route A01, m = 1.56 | **C_UPPER_FIELD** | **0.244** | 0.185 | **0.172** | 0.399 | **ADCBDDCADDDBACB** | **3 / 3** |
| Route A01, m = 1.77 | none (g0403-01) | 0.230 | 0.181 | 0.200 | 0.389 | BDCBDDCADDCBCCB | 1 / 5 |
| Route A01, m = 1.77 | **C_UPPER_FIELD** | **0.246** | 0.186 | **0.168** | 0.400 | **ADCBDDCADDDBAAB** | **4 / 2** |
| Route A01, m = 9.28 | none | 0.294 | 0.200 | 0.077 | 0.429 | ADABDDAADDDBAAB | 6 / 0 |
| Route A01, m = 9.28 | C_UPPER_FIELD | 0.303 | 0.203 | 0.060 | 0.434 | ADABDDAADDDBAAB | 6 / 0 |
| Hybrid A01, m = 1.77 | none | 0.197 | 0.170 | 0.263 | 0.369 | CDCBDDCADDCBCCD | 1 / 6 |
| Hybrid A01, m = 1.77 | **C_UPPER_FIELD** | **0.210** | 0.175 | **0.237** | 0.378 | **BDCBDDCADDCBCCB** | **1 / 5** |
| Assist | (no h) | 0.324 | 0.209 | 0.020 | 0.447 | ADABDDAADDDBAAB | 6 / 0 |

1. **Routing at m = 1.77 loses 3 of its 5 modal processes.** C keeps P03 and P07; P11 goes to D, P13 and P14 go back to A. Its rank-first probability falls from 0.200 to 0.168, and A becomes modal in 4 processes (P01, P08, P13, P14). At m = 1.56, C keeps 3 (P03, P07, P14).
2. **Hybrid routing is robust to the cut:** it stays modal in 5 processes (P01 goes from C to B; P15 from D to B) with P(C first) 0.237.
3. **D has the highest mean rank-first probability in every cell of the table** (0.369–0.434); B is never above 0.21.
4. **The cut on the upper half is milder than its mean suggests.** r_C's mean is 0.47, but even r_C = 0 (h capped at 0.50) leaves A01 routing modal in P07 and hybrid modal in 5 processes (§3.2). Most of routing's advantage comes from the lower half of h.
5. **Cutting the whole of h (C_ALL_FIELD, stress) removes routing and hybrid as modal winners** in every A_V1 and A_FIELD cell (A modal in 6, C in 0). Only A_RPA_ANALOGY × BD_FIELD with hybrid keeps C modal (2 processes). Whether the lower half (bank test set-up 0.20, E19 optimal-policy 0.21–0.49, OCBC benchmark) also needs a realization factor is the larger open question (P-G0403-0105-02).
6. **Value [S]:** the median value routing adds beyond the best of A, B and D falls from $133k to **$84k** a year at m = 1.77 (hybrid: $313k to $249k).

### (B) Correlated realization (P-G0403-01-04)

- r_A, r_B and r_D are redrawn through a **Gaussian copula with a common sponsor-execution factor** at rank correlation 0.5 (latent Pearson 0.5176) and 1.0 (comonotone). Empirical Spearman at NAT_LARGE: 0.497–0.518 at 0.5 and 1.000 at 1.0 [C]. Each marginal is unchanged.
- **Correlation does not revert the ranking to the V1 priors. It moves rank-first probability from B (and to a lesser degree D) to A and C, and changes at most 2 modal winners in any A_FIELD × BD_FIELD cell at NAT_LARGE.**

| C variant (A_FIELD × BD_FIELD) | rank corr | A | B | C | D | Modal winners | n modal A / C | share_A |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Assist | 0 | 0.324 | 0.209 | 0.020 | 0.447 | ADABDDAADDDBAAB | 6 / 0 | 0.94 |
| Assist | 0.5 | 0.343 | 0.191 | 0.024 | 0.442 | ADABDDAADDDBAAD | 6 / 0 | 0.93 |
| Assist | 1.0 | 0.367 | 0.164 | 0.029 | 0.440 | ADABDDAADDDBAAD | 6 / 0 | 0.92 |
| Route A01, m = 1.77 | 0 | 0.230 | 0.181 | 0.200 | 0.389 | BDCBDDCADDCBCCB | 1 / 5 | 0.58 |
| Route A01, m = 1.77 | 0.5 | 0.236 | 0.165 | 0.217 | 0.382 | ADCBDDCADDCBCCD | 2 / 5 | 0.56 |
| Route A01, m = 1.77 | 1.0 | 0.246 | 0.141 | 0.235 | 0.378 | ADCBDDCADDCBCCD | 2 / 5 | 0.55 |
| Hybrid A01, m = 1.77 | 0 | 0.197 | 0.170 | 0.263 | 0.369 | CDCBDDCADDCBCCD | 1 / 6 | 0.49 |
| Hybrid A01, m = 1.77 | 1.0 | 0.208 | 0.133 | 0.302 | 0.357 | CDCBDDCADDCBCCD | 1 / 6 | 0.45 |

7. **Why B loses.** Under independence, a process that B and D both serve has two chances that one of them realizes well; under a common factor those chances coincide, so max(B, D) is lower in expectation. When the factor is low, A (whose r_A range sits near 1) and C (no factor) win; when it is high, B and D win in their V1 order. The modal changes are in B-modal processes with a narrow margin (P01 B→A, P15 B→D).
8. **The wave-37C expectation holds only when the marginals are equal.** With A at the RPA analogy (A_RPA_ANALOGY, same marginal as r_B and r_D), rank correlation 1 means one common value on A, B and D. Then the ordering among A, B and D does revert to V1 (A falls to 0.018), and C, which carries no factor, gains: A01 routing at m = 1.77 goes from 0.270 and 5 modal processes to **0.321 and 6** [S].
9. **Putting r_C on the same factor (set ABCD) offsets the h cut.** Route A01 at m = 1.77 under C_UPPER_FIELD: 0.168 and 2 modal processes at rank correlation 0, 0.183 and 3 at 0.5, **0.200 and 5** at 1.0, the same count as without any cut. Correlation makes C's bad draws coincide with A's, B's and D's bad draws, so the cut matters less to the ranking.
10. **Assistance remains modal nowhere** in every correlation cell (maximum P(C first) 0.065, A_RPA_ANALOGY × BD_FIELD at rank correlation 1).

### Replication

- **The A_FIELD/BD_FIELD baseline reproduces `ai-ranking-a-calibrated-2026-11-20.csv`.** All rows with c_real = C_V1 and rank correlation 0 (main and absorption cells) were matched against that CSV on c_variant, bd_variant, a_variant, archetype, process, intervention and metric: __NCMP__ values compared, **__NBAD__ mismatches** (floats within 1e-6 relative; modal strings exact). This covers A_V1 × V1_PRIORS, A_V1 / A_FIELD / A_RPA_ANALOGY × BD_FIELD, the A_FIELD absorption shares, for ASSIST, ROUTE_G04_M1.77, ROUTE_A01_M1.56 / M1.77 / M9.28 and HYBRID_A01_M1.77, at all five archetypes (per-process values at NAT_LARGE).

---

## 1. Method

### 1.1 Retrieval

- No web retrieval was done for this task and no robots.txt was checked: every input is already in the repo, quoted and validated in earlier waves (HUD and GSA OIG audits: BD-E01/E02, validated in wave 37C; E15, State Dept, CB-02 and CB-04: CB-01 to CB-05, wave 37C; NAO casework audits: MI-E01/E02, wave 41C). Primary URLs are in the source register.
- Nothing was fetched from sec.gov, crt.sh or certspotter. No outreach, logins or forms.

### 1.2 Model base (unchanged)

- CAL_CENTRAL draws are rebuilt via `ac.bd.compact_plus` (calibrated Random(42)); routing parameters come from Random(42 + 104729), with the A01 ranges h ~ U(0.20, 0.80), e ~ U(0.004, 0.10), k ~ tri(0.03, 0.10, 0.30); B, D and A realization uniforms (u_B, u_D, u_A) come from the recut stream Random(42 + 15485863). A, B, D specs are imported from `mission_ai_a_calibrated.py` (A_V1, A_FIELD, A_RPA_ANALOGY) and `mission_ai_bd_recut.py` (V1_PRIORS, BD_FIELD, BD_WIDE). The C variants and m values are g0403-01's: ASSIST, ROUTE_G04_M1.77, ROUTE_A01 at m = 1.56, 1.77 and 9.28, HYBRID_A01_M1.77.
- Two new streams are added, so no existing draw changes: **Random(42 + 32452843)** gives u_C (one per draw), and **Random(42 + 49979687)** gives the common factor Z = Φ⁻¹(u) (one per draw).

### 1.3 (A) Realization factor on routing h

- **Why only the upper half.** The A01 range's lower bound is CB-02 (about 20% of alert workload auto-closed in a bank's *test* set-up), close to E19's 0.21–0.49 (optimal-policy simulation) and CB-04's 0.28–0.49 (OCBC benchmark at ≤ 5–10% error). The upper half rests on two numbers: E15's computed 0.78 (retrospective validation on one bank's data) and State's "Reduced volume for humans to review (by 80%)" (agency deck) [F]. Wave 37C asked for these two to be cut. The split is set at **H_SPLIT = 0.50**, the midpoint of U(0.20, 0.80) [I].
- **Mapping [I].** h_eff = min(h, 0.50) + r_C · max(0, h − 0.50). r_C is drawn once per draw and applies to every process, as r_B does. C_route and C_hybrid are evaluated with h_eff (the routing script's formula, unchanged): cases not realized as AI-closed return to human handling; under hybrid they receive assistance. Inference cost is unchanged.
- **Why the RPA range.** B's realization range comes from audits of automation programmes whose claimed savings were realized at 7% (HUD, programme) and about 33% (GSA closeout bot), with 9 of 10 GSA bots varying from estimate [F]. State's 80% is the same kind of claim: an agency-reported volume reduction with no audited realization. E15's 0.78 is an ex-ante figure from retrospective validation. Treating both like an RPA estimate is an analogy [I]: the audits measured labour hours saved by bots, not auto-close shares of an ML classifier.
- **Specs:** C_V1 (r_C = 1; replication), **C_UPPER_FIELD** (r_C ~ tri(0.07, 0.33, 1.00), main), C_UPPER_WIDE (r_C ~ U(0.07, 1.00), as BD_WIDE), C_ALL_FIELD (h_eff = r_C · h, stress), SWEEP_RC (fixed r_C ∈ {1, 0.75, 0.5, 0.33, 0.2, 0.07, 0} on the upper half, A_FIELD × BD_FIELD).
- **A/B/D combinations run with each C spec:** A_V1 × V1_PRIORS, A_V1 × BD_FIELD, **A_FIELD × BD_FIELD** (the cell where A, B, C and D all carry a factor), A_RPA_ANALOGY × BD_FIELD.
- ROUTE_G04 (h ≤ 0.49) has no h above 0.50, so (A) does not change it; it is run only in (B). ASSIST has no h.

### 1.4 (B) Gaussian copula

- For draw n: X_i = √ρ · Z_n + √(1 − ρ) · Φ⁻¹(u_i), U_i = Φ(X_i), r_i = F_i⁻¹(U_i), for i ∈ {B, D, A} (and C in set ABCD). Φ and Φ⁻¹ are `statistics.NormalDist().cdf` / `.inv_cdf`; uniforms are clamped to [1e-12, 1 − 1e-12] before Φ⁻¹.
- **Rank correlation → latent ρ:** for a Gaussian copula Spearman ρ_s = (6/π) arcsin(ρ/2), so ρ = 2 sin(πρ_s/6): ρ_s = 0.5 → ρ = 0.517638; ρ_s = 1 → ρ = 1, where every U_i = Φ(Z_n) (comonotone). At ρ_s = 0 the map is the identity (U_i = u_i), so the independent baseline is reproduced exactly; at ρ_s > 0 the idiosyncratic parts are the existing recut uniforms (common random numbers across ρ_s).
- **Marginals are preserved.** At ρ_s = 1 r_B = r_D (same triangular), but r_A = F_A⁻¹(U) is not equal to r_B: comonotone, not identical. The case of a single common value on A, B and D is A_RPA_ANALOGY at ρ_s = 1.
- **Sets:** ABD (r_A, r_B, r_D on the factor; C unchanged) with A_FIELD × V1_PRIORS (absorption base), A_FIELD × BD_FIELD, A_FIELD × BD_WIDE and A_RPA_ANALOGY × BD_FIELD for all six C variants; ABCD (r_C under C_UPPER_FIELD also on the factor) with A_FIELD × BD_FIELD for the four A01 variants.
- **Checks [C]:** the CSV records the empirical Spearman of the drawn r values (r_A–r_B, r_B–r_D, r_A–r_D, r_C–r_B) and max |U − u| for each archetype and ρ_s (`record_type=meta`).

### 1.5 Archetypes

All five were run (NAT_LARGE, NAT_MID, CF_1BN, CF_250M, CF_SMALL), 10,000 draws each. NAT_LARGE was run first on its own (4 min 19 s) and gave the same values as the five-archetype run. Per-process rows are written for NAT_LARGE only.

---

## 2. Evidence used (no new evidence)

| Id | Source | Value used | Grade | Use here |
|---|---|---|---|---|
| BD-E01 | HUD OIG 2021-OE-0007 (Feb 2023) | "annual labor hour savings totaled approximately 1,015, or 7 percent of the amount HUD estimated" [F] | A | r_C lower bound 0.07 (as r_B) |
| BD-E02 | GSA OIG A210057 (Nov 2023) | "estimated savings based on the task taking 90 minutes, whereas users reported time savings only averaged approximately 30 minutes" (0.33) [F/C]; "actual results varied from the estimates for 9 of the 10 bots" [F] | A | r_C mode 0.33 (as r_B) |
| CB-01c | E15, Eddin et al. 2021 (arXiv 2112.07508), computed | auto-closed share 0.779 at π = 0.03, recall 0.90 [C] | B | the upper-half anchor being cut |
| CB-05 | US State Dept AI Pilot Results deck (June 2024) | "Reduced volume for humans to review (by 80%)" [F] | B | the upper-half anchor being cut |
| CB-02 | Gerlings & Constantiou, HICSS-56 (arXiv 2210.07648) | "the model reduces the workload of investigators by ~20%" in a test set-up [F] | B | lower-half anchor (not cut, except C_ALL_FIELD) |
| CB-04 | Jin et al. (OCBC), arXiv 2609.20110 | DocILE h = 0.281 (e ≤ 5%), 0.494 (e ≤ 10%) [F] | C | lower-half anchor |
| MI-E01/E02 | NAO HC 1336 (2025), HC 1375 (2023) | r_A ~ tri(0.475, 1.0, 1.2) [I mapping] | A (figures) | A_FIELD, unchanged |

---

## 3. Results [S]

### 3.1 (A) Full grid, NAT_LARGE

P(rank first) A / B / C / D, modal string, and n modal A / C. "C beyond best" is the median over draws of Σ max(0, C − max(0, A, B, D)) across P01–P15 (usd/yr).

__T1__

- **Under A_V1 × BD_FIELD** (A without a factor), C_UPPER_FIELD leaves A01 routing modal in 1 process (P07) at both m = 1.56 and 1.77, against 2 without the cut.
- **Under A_RPA_ANALOGY × BD_FIELD** (A, B and D all at the RPA range), A01 routing stays modal in 4–5 processes after the cut and hybrid in 6. The RPA range on A is a lower-bound stress (g0403-01), so this is the most favourable cell for C.
- **C_UPPER_WIDE** gives results within 0.005 of C_UPPER_FIELD in C's rank-first probability and differs by at most 1 modal process.
- **V1_PRIORS (no factor on A, B or D) with C_UPPER_FIELD:** routing is modal nowhere; hybrid in P03 only (as without the cut).

### 3.2 (A) Sweep of a fixed r_C on the upper half (A_FIELD × BD_FIELD, NAT_LARGE)

P(C first) and (number of processes where C is modal), modal string.

__T2__

- **A01 routing at m = 1.77 drops from 5 to 3 modal processes at r_C = 0.5 and to 1 (P07) at r_C ≤ 0.33.** C_UPPER_FIELD's mode (0.33) sits at the second switch point.
- **Hybrid stays modal in 5–6 processes at every r_C,** including r_C = 0 (h capped at 0.50).
- At m = 9.28 routing is modal nowhere at any r_C.

### 3.3 (B) Correlation, NAT_LARGE, all A/B/D cells

"Changed" is the number of processes whose modal winner differs from the same cell at rank correlation 0.

__T3__

- **B is the loser in every cell.** Its rank-first probability falls by 0.031–0.066 from rank correlation 0 to 1. D falls by 0.007–0.021 under A_FIELD (D's P09/P10 carry no factor in BD_FIELD) and rises by 0.004–0.052 under A_RPA_ANALOGY.
- **A gains under A_FIELD and loses under A_RPA_ANALOGY.** With A_FIELD, r_A rarely falls far (range 0.475–1.2), so A wins the draws in which the common factor is low. With A_RPA_ANALOGY, A shares B's and D's marginal and moves with them.
- **C gains in every cell**, by 0.009–0.057. A changes by +0.010 to +0.071 (A_FIELD) and −0.025 to −0.044 (A_RPA_ANALOGY). Under A_RPA_ANALOGY with A01 routing, C becomes modal in 6 processes (adds P01).
- **Absorption.** A's share of what B and D lose (BD_FIELD − V1_PRIORS, A_FIELD) falls slightly with correlation: assist 0.94 → 0.92; routing A01 m = 1.77 0.58 → 0.55; hybrid 0.49 → 0.45. B and D lose more in total (routing m = 1.77: 0.327 → 0.378), and C takes a larger share of it.

### 3.4 (B) Set ABCD: r_C on the common factor too (A_FIELD × BD_FIELD × C_UPPER_FIELD, NAT_LARGE)

__T5__

### 3.5 Archetypes

A_FIELD × BD_FIELD. For (A): P(C first) and n modal A / C under C_V1, C_UPPER_FIELD and C_ALL_FIELD. For (B): P(C first), n modal A / C and A's absorption share at rank correlation 0 / 0.5 / 1 (set ABD).

__T6__

---

## 4. What changes in earlier conclusions

| Earlier conclusion | Status |
|---|---|
| g0403-01: with A01 routing at the current m = 1.56–1.77 under A_FIELD × BD_FIELD, C is modal in 5 large-national processes (P03, P07, P11, P13, P14); h-asymmetry caveat (wave 37C) | **Revised [S].** With the upper half of h held to the RPA realization range [I] (C_UPPER_FIELD), A01 routing is modal in **2** processes at m = 1.77 (P03, P07) and **3** at m = 1.56 (P03, P07, P14); A in 4 and 3. Hybrid stays modal in 5. Holding the whole of h to that range removes routing and hybrid as modal winners under A_V1 and A_FIELD |
| Wave 37C: "If one common realization factor applied to A, B, C and D alike, the gross ranking would be the V1-priors one" | **Holds only for equal marginals.** With A_FIELD's marginal, a rank-correlation-1 factor does not revert A, B and D to V1; it moves probability from B to A and C. With A at the RPA range (equal values), the A–B–D order does revert to V1 and C, carrying no factor, gains (5 → 6 modal processes). With r_C also on the factor (ABCD, ρ_s = 1) routing returns to 5 modal processes |
| g0403-01 §5 item 6: "With a common factor, ranks among A, B and D revert towards V1 priors (wave 37C)" and "Independence [I] maximises re-ordering" (P-G0403-01-04 rationale) | **Not supported for A_FIELD.** In mean probabilities correlation moves B and D further from their V1 levels, not back. Modal winners change in 0–2 large-national processes per cell (set ABD), every change taking a process away from B: some move away from V1 (P01 B→A or C), one returns to it (P15 B→D, D in V1) |
| Assistance wins no process | **Unchanged** in every cell of both studies |
| Routing is modal nowhere at m = 9.28 | **Unchanged** under every r_C and correlation in A_FIELD cells |

---

## 5. Limits

1. **r_C is borrowed, not measured.** The HUD and GSA audits measure labour hours saved by RPA bots against estimates. Mapping them onto the realized share of AI auto-closes is [I], as was the mapping onto D (recut) and the NAO throughput mapping onto A (g0403-01). No 2021+ audit of a production AI or ML auto-close programme was found in the repo's evidence; none was searched for in this task (P-G0403-0105-01).
2. **The split point (0.50) is a choice.** It is the midpoint of the A01 range. The lower half is also test-set-up, benchmark or optimal-policy evidence, not audited production. C_ALL_FIELD shows the result is sensitive to this: cutting all of h removes routing everywhere (P-G0403-0105-02).
3. **Only h is cut.** e (in-band error), k (QA rate) and m are unchanged. The e range's lower end (0.4%) is also a retrospective bound.
4. **One factor per sponsor draw.** r_A, r_B, r_C and r_D are each drawn once per draw and applied to all 15 processes. Per-process dispersion (HUD bot ratios 0.01–0.33) is not modelled (P-G0403-0105-04).
5. **The copula is a choice.** A Gaussian copula has no tail dependence; a t- or Clayton copula would make joint failures more likely. The rank correlations 0.5 and 1.0 are the queue item's values, not estimates (P-G0403-0105-03).
6. **Empirical Spearman under independence is not exactly 0** (r_A–r_D 0.023 at NAT_LARGE, about 2.3 standard errors at n = 10,000): sampling noise in the existing recut stream, kept for replication.
7. **Monte Carlo error only** in the Wilson intervals (`lo`/`hi`). Assumption ranges are shown by specs and sweeps.
8. **m is not pinned down** (wave 39B). Results at m = 9.28 differ from 1.56–1.77; the Amex-priced composites (13.7 / 128 / 1,269) were not run, because routing is already modal nowhere at 9.28.
9. **Blocked or missing:** nothing was blocked, because no retrieval was attempted. Missing: any audited realized-vs-claimed figure for AI auto-close; any evidence on the correlation of realization across interventions in one organisation.

---

## D. Data dictionary

### D1. `ai-ranking-realized-correlated-2026-11-20.csv` (long format)

| Column | Meaning |
|---|---|
| record_type | `spec` (C realization and correlation definitions), `meta` (draws, seeds, empirical Spearman, max U shift), `model` (results), `replication` (comparison with ai-ranking-a-calibrated-2026-11-20.csv) |
| study | `A_HCUT` (P-G0403-01-05), `B_CORR` (P-G0403-01-04), `REPLICATION`; blank for global meta |
| scenario | CAL_CENTRAL; ALL for spec, meta and replication rows |
| c_variant | ASSIST, ROUTE_G04_M1.77, ROUTE_A01_M1.56, ROUTE_A01_M1.77, ROUTE_A01_M9.28, HYBRID_A01_M1.77 (as g0403-01) |
| c_real | C_V1, C_UPPER_FIELD, C_UPPER_WIDE, C_ALL_FIELD, SWEEP_RC |
| bd_variant | V1_PRIORS, BD_FIELD, BD_WIDE (recut definitions); `BD_FIELD-V1_PRIORS` for absorption rows |
| a_variant | A_V1, A_FIELD, A_RPA_ANALOGY (g0403-01 definitions) |
| corr_set | `independent` (study A), `ABD` (r_A, r_B, r_D on the factor), `ABCD` (also r_C) |
| rank_corr | target Spearman rank correlation of the realization factors: 0, 0.5, 1 |
| archetype | NAT_LARGE, NAT_MID, CF_1BN, CF_250M, CF_SMALL; comma list on replication rows |
| cell | `main`; `absorption`; `sweep_rC=<r>`; `corr_rs=<rho_s>` on meta rows |
| process_id | P01–P15 for per-process rows (NAT_LARGE only); blank otherwise |
| intervention | A, B, C, D or none where the metric is per option |
| metric | as g0403-01: `mean_p_rank_first_gross_P01_P15`, `mean_p_rank_first_net_P01_P15`, `modal_winners_gross_P01_P15`, `n_processes_modal_gross`, `sponsor_gross_value_pool_p50`, `sponsor_best_non_AI_pool_p50`, `sponsor_C_incremental_over_best_other_p50`, `p_rank_first_gross`, `modal_winner_gross`; absorption `lost_BD`, `dA`, `dC`, `share_A`, `share_C`; new: `n_processes_modal_changed_gross` (vs C_V1 in study A, vs rank_corr 0 in study B; note lists changes), `spearman_rA_rB` etc., `max_abs_u_shift_vs_recut`, `values_compared`, `values_mismatched`, `c_real_spec`, `corr_spec`, `seeds`, `draws` |
| value | metric value |
| lo, hi | 95% Wilson interval (Monte Carlo error) for mean probabilities; p25 / p75 for pools |
| unit | prob, share, count, usd/yr, rho |
| note | basis of the metric |

### D2. `queue-proposals-g0403-0105-04.csv`

Same header and format as `queue-proposals-gap19-13.csv`.

---

## Source register (primary URLs; all quoted from the repo's validated evidence tables; not re-fetched 2026-11-20)

| Id | Source | URL |
|---|---|---|
| BD-E01 | HUD OIG, Evaluation 2021-OE-0007, *HUD's Robotic Process Automation Program Was Not Efficient or Effective* (Feb 2023) | https://www.hudoig.gov/sites/default/files/2023-02/2021-OE-0007.pdf |
| BD-E02 | GSA OIG, Audit A210057/B/5/F24001, *GSA's RPA Program Lacks Evidence to Support Claimed Savings* (Nov 2023) | https://gsaig.gov/sites/default/files/audit-reports/A210057-1%20Final%20Report.pdf |
| CB-01 / E15 | Eddin AN et al., *Anti-Money Laundering Alert Optimization Using Machine Learning with Graphs* (2021) | https://arxiv.org/abs/2112.07508 |
| CB-02 | Gerlings J, Constantiou I, *Machine Learning in Transaction Monitoring: The Prospect of xAI*, HICSS-56 (2023) | https://arxiv.org/abs/2210.07648 |
| CB-04 | Jin Y et al. (OCBC), *Perception, Layout, and Validation: Calibrated Confidence for Reliable Straight-Through Processing of Financial Documents* (2026) | https://arxiv.org/abs/2609.20110 |
| CB-05 | US Department of State, *AI Pilot Results* (deck hosted by NARA), 24 June 2024 | https://transforming-classification.blogs.archives.gov/wp-content/uploads/sites/10/2024/07/State-AI-Pilot-Results-June-24-2024.pdf |
| E19 | Agarwal N et al., NBER Working Paper w31422 (rev. Aug 2026) | https://www.nber.org/papers/w31422 |
| MI-E01 | NAO, *Tackling benefit overpayments due to fraud and error*, HC 1336 (Oct 2025) | https://www.nao.org.uk/wp-content/uploads/2025/10/Tackling-benefit-overpayments-due-to-fraud-and-error.pdf |
| MI-E02 | NAO, *The asylum and protection transformation programme*, HC 1375 (Jun 2023) | https://www.nao.org.uk/wp-content/uploads/2023/06/the-asylum-and-protection-transformation-programme.pdf |
| m | g0403-0104 (wave 39B): OFAC enforcement releases and IRS Data Book via that study | https://ofac.treasury.gov/civil-penalties-and-enforcement-information ; https://www.irs.gov/statistics/soi-tax-stats-irs-data-book |
| Model inputs | mission_ai_a_calibrated.py, mission_ai_bd_recut.py, mission_ai_routing_variant.py; ai-ranking-a-calibrated-2026-11-20.csv | repo |
