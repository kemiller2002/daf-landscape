# P-G0403-01: manual improvement (A) held to the evidence standard applied to B, C and D

*Prepared 2026-11-20. TASKID g0403-01.*

**Outputs**
- [`scripts/mission_ai_a_calibrated.py`](../../scripts/mission_ai_a_calibrated.py). It imports [`mission_ai_bd_recut.py`](../../scripts/mission_ai_bd_recut.py) without modifying it. Through that module it uses the routing variant, the calibrated model and v2, none of which is modified. Stdlib only, functional style. Run: `python3 scripts/mission_ai_a_calibrated.py . --draws 10000` (about 17 minutes for five archetypes).
- [`data/mission-2026-11-14/manual-improvement-evidence-2026-11-20.csv`](../../data/mission-2026-11-14/manual-improvement-evidence-2026-11-20.csv): 8 rows. The script writes it from an embedded table, so it is not hand-built (wave 37C noted this for the confidence-band CSV). Data dictionary in §D1.
- [`data/mission-2026-11-14/ai-ranking-a-calibrated-2026-11-20.csv`](../../data/mission-2026-11-14/ai-ranking-a-calibrated-2026-11-20.csv): 35,368 rows (35,369 lines with the header). Data dictionary in §D2.
- [`data/mission-2026-11-14/queue-proposals-g0403-01.csv`](../../data/mission-2026-11-14/queue-proposals-g0403-01.csv): 5 proposals.
- No existing file was modified.

**Read first**
- [g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md) and its wave-37C corrections ([validation-wave37c-report.md](validation-wave37c-report.md)).
- [gap19-ai-calibration.md](gap19-ai-calibration.md).
- [g0403-0104-m-detection-ofac.md](g0403-0104-m-detection-ofac.md) and its wave-39B corrections ([validation-wave39b-report.md](validation-wave39b-report.md)). The current m is low 1.0, central **1.56** (OFAC analogue) to **1.77** (bank-SAR transfer), and high **9.28** (OFAC analogue). Wave 39B adds that the composite "is not pinned down".

**Notation:** [F] published value, quoted; [C] computed here; [I] inference or assumption; [S] scenario output.

---

## 0. Answers in brief

### Evidence

- **No 2021+ audit was found that compares realized with planned *labour savings* from a non-technology fix in back-office finance or compliance work.** That is the same gap the recut found for redesign (D).
- **The closest evidence is two NAO audits of manual casework programmes in UK government.** Each compares realized with planned throughput:
  - **MI-E01, DWP Targeted Case Review** (manual review of benefit claims; cases picked by risk rules). Cases reviewed per agent per day were **0.57 against an expected 1.20** in 2023-24 (ratio **0.475**) and **1.07 against 0.89** in 2024-25 (**1.20**) [F/C]. Cases completed were **104%** of plan, and estimated savings **111%** (£581m against £525m) [F].
  - **MI-E02, Home Office asylum PACE** (process simplification: questionnaires, cohort rules, withdrawal rules). The plan was to raise decisions per caseworker per week from **1.4 to 2.5**. In April 2023 "the 640 active caseworkers … achieved the 2.5 decisions weekly", a headline realization of **1.0** [F/C]. But "72% of decisions in April 2023 were 'administrative decisions'" [F], so labour per substantive decision is not measured.
- **Evidence on the size of the saving (α) is weak, and it sits inside v1's range:**
  - IOPC's self-reported "productivity in one casework team may have increased by 33%" from workload re-allocation (MI-E03) is about **0.25** per unit [C], v1's upper bound.
  - Fenizia (Econometrica 2022), on an Italian social-security back office, finds +10% output for a one-standard-deviation better manager and +6.9% from reallocating managers (MI-E04). That is **0.065–0.091** per unit [C]. The abstract attributes the gain mainly to retirements, not to process fixes.
- **Three 2025–26 Lean case studies** (two from the Washington State Auditor, one in a journal on Malaysian payment processing) report quality or step counts, not labour (MI-E05 to MI-E07).
- **So α ~ U(0.05, 0.25) is kept as an [I] sweep.** A new realization range, **r_A ~ triangular(0.475, 1.00, 1.20)**, is mapped from MI-E01/E02 [I] (spec A_FIELD). A stress spec restricts α to the peer-reviewed level, U(0.065, 0.091) (A_LEVEL_A).

### Ranking

All figures are for a large national (NAT_LARGE), CAL_CENTRAL, gross, as the mean over P01–P15 of P(rank first) [S]. B and D are at the recut's BD_FIELD standard.

| C variant (current m) | A spec | A | B | C | D | Modal winners P01–P15 | A's share of what B and D lose |
|---|---|---:|---:|---:|---:|---|---:|
| Assist | A_V1 (recut) | 0.385 | 0.186 | 0.015 | 0.413 | ADABDDAADDDBAAB | 0.96 |
| Assist | **A_FIELD** | **0.324** | 0.209 | **0.020** | 0.447 | **ADABDDAADDDBAAB** | **0.94** |
| Assist | A_LEVEL_A | 0.089 | 0.292 | 0.042 | 0.577 | BDABDDDDDDDBDBD | 0.70 |
| Route, routing-note ranges, m = 1.77 | A_FIELD | 0.292 | 0.199 | 0.081 | 0.428 | ADABDDAADDDBAAB | 0.78 |
| Route, A01 ranges, m = 1.56 | A_FIELD | 0.228 | 0.180 | 0.204 | 0.388 | ADCBDDCADDCBCCB | 0.58 |
| Route, A01 ranges, m = 1.77 | **A_FIELD** | **0.230** | 0.181 | **0.200** | 0.389 | **BDCBDDCADDCBCCB** | **0.58** |
| Route, A01 ranges, m = 1.77 | A_V1 | 0.291 | 0.164 | 0.178 | 0.368 | ADABDDCADDCBAAB | 0.67 |
| Route, A01 ranges, m = 1.77 | A_LEVEL_A | 0.021 | 0.235 | 0.280 | 0.464 | BDCBDDCDDDCBCCD | 0.09 |
| Route, A01 ranges, m = 9.28 | A_FIELD | 0.294 | 0.200 | 0.077 | 0.429 | ADABDDAADDDBAAB | 0.81 |
| Hybrid, A01 ranges, m = 1.77 | A_FIELD | 0.197 | 0.170 | 0.263 | 0.369 | CDCBDDCADDCBCCD | 0.49 |

**Does A still absorb what B and D lose? Yes, under the only audited realization evidence for manual work. The answer turns on r_A.**

1. **Under A_FIELD, A keeps almost all of its gain.**
   - With assistance as C, A takes **94%** of the rank-first probability that B and D lose. It stays modal in **6 of 15 processes** (P01, P03, P07, P08, P13, P14), the same set as under the unsourced prior.
   - The NAO casework ratios centre on 1.0, against 0.07–0.33 for the RPA audits. Holding A to "audited realization" therefore barely moves it, because the audited realization of manual programmes is close to plan.
2. **With routing at the A01 ranges, C takes P13 and P14 from A at the current m.** At m = 1.77, C is modal in **5 processes** (P03, P07, P11, P13, P14) and A in **1** (P08). A still takes **58%** of what B and D lose. At m = 9.28 (wave-39B high), C is modal nowhere and A is back to 6 processes.
3. **A stops absorbing only if manual realization falls below plan, or if α falls to the peer-reviewed level.**
   - In the fixed-r_A sweep under BD_FIELD with assistance, A is modal in 6 processes at r_A = 1.0, in 3 at 0.75, in 1 at 0.5 and in 0 at 0.33.
   - With A01 routing at m = 1.77, A is modal in 5 processes at r_A = 1.0 and in none at 0.75.
   - Under A_LEVEL_A, A is modal in at most 1 process in any C variant.
   - The only audited manual-programme ratio that low is DWP's 2023-24 productivity, 0.475, and it reversed to 1.20 the next year.
4. **Assistance remains modal nowhere** in any A × B/D cell at a large national. Its rank-first probability is at most **0.140** (A_LEVEL_A_FIELD × BD_PROGRAM).
5. **Archetypes.** Under BD_FIELD × A_FIELD:
   - With assistance, A is modal in **6** processes at every archetype checked (NAT_LARGE, NAT_MID, CF_1BN, CF_250M, CF_SMALL), with absorption 0.92–0.94.
   - With A01 routing at m = 1.77, C is modal in 2–6 processes (NAT_MID 2; the others 5–6).

**Value pools (NAT_LARGE, sponsor p50, gross, BD_FIELD) [S]:**
- The A pool falls from **$1.94m** (A_V1) to **$1.71m** (A_FIELD), **$1.06m** (A_LEVEL_A) or **$827k** (RPA analogy).
- The value AI adds beyond what A, B or D already deliver (median draw) is:
  - **assistance:** $0 in every A spec;
  - **A01 routing, m = 1.77:** $80k (A_V1), **$133k (A_FIELD)**, $364k (A_LEVEL_A);
  - **A01 hybrid, m = 1.77:** $237k / $313k / $595k.

---

## 1. Method

### 1.1 Retrieval and robots.txt

- One helper (scratchpad `tools/fetch.py`) fetched every primary document with user agent `research-script/1.0`. It read each host's robots.txt with `urllib.robotparser`, fetched only allowed URLs and logged each request to `robots-log.tsv`.
- A robots.txt that returned 403 or 406, or a connection the host closed, was treated as a block.
- Discovery used a web search tool. No figure comes from a search snippet.
- No user agent was changed. Nothing was fetched from sec.gov, crt.sh or certspotter. There was no login, form or outreach.

**Robots log (2026-11-20).**

| Host | robots.txt | Use |
|---|---|---|
| www.gao.gov | **403 (blocked)** | **Still blocked**, as in g0403-0104. No GAO report used |
| www.nao.org.uk | 200, allowed | MI-E01, MI-E02, MI-E03; also Efficiency in government (2021), Cabinet Office functional savings (2023), Smarter delivery (2025), all read and not used for parameters |
| www.anao.gov.au | **connection closed on robots.txt (treated as blocked)** | DVA claims-backlog and efficiency audits not fetched (P-G0403-01-02) |
| www.uspsoig.gov | **406 (blocked)** | USPS OIG continuous-improvement audit not fetched |
| eutils.ncbi.nlm.nih.gov | 200; disallows the generic agent for E-utilities | PMC search not run |
| www.econometricsociety.org | 200, allowed | MI-E04 abstract (full text needs a login: not read) |
| sao.wa.gov | 200, allowed | MI-E05, MI-E06, Lean resource library |
| e-journal.uum.edu.my | 200, allowed | MI-E07 |
| www.oversight.gov | 406 in the earlier waves; not retried | — |

### 1.2 What "same evidence standard" means for A

- The recut held B to *realized against planned* savings from inspector-general audits (RPA: 0.07 program-level, 0.33 for one bot). It borrowed that range for D by analogy [I].
- For A the equivalent evidence would be an audit of a non-technology improvement (checklist, standard work, triage rule, queue or workload change) that compares realized with estimated labour saving. None was found (§2).
- The closest substitute is an audit of a manual casework programme that compares **throughput realized against throughput planned**. Two NAO reports provide this (MI-E01, MI-E02).
- **Mapping [I]:** realized A = r_A·α·L. Here r_A is drawn from triangular(0.475, 1.00, 1.20):
  - low end: DWP TCR 2023-24 productivity, 0.57/1.20;
  - mode: the PACE headline (2.5 of 2.5) and TCR cases completed (1.04);
  - top: TCR 2024-25 productivity, 1.07/0.89.
  - r_A is drawn from the recut stream's third uniform, the one ABD_FIELD used, so the specs are comparable draw by draw.
- **α level:** MI-E03 (0.25, self-report) and MI-E04 (0.065–0.091, peer-reviewed, management rather than process) bracket v1's U(0.05, 0.25) without narrowing it. α is therefore kept as an [I] sweep. A_LEVEL_A restricts it to the peer-reviewed level as a stress test.

### 1.3 Model

- **Base.** CAL_CENTRAL draws are rebuilt by importing `bd.compact_plus` (calibrated seed 42). C uses `bd.c_values`, with routing streams 42 + 104729 (routing-note and A01 ranges). B and D use `bd.eval_draw`, with BD specs taken unchanged from `bd.BD_SPECS` and the recut stream 42 + 15485863.
- **What changes.** In each draw and process, A is replaced by α′·L·r_A:
  - α is recovered from the drawn A as A/L;
  - its v1 uniform is recovered as (α − 0.05)/0.20 and, for A_LEVEL_*, remapped to the new range on the same uniform.
- **A specs:** A_V1, A_RPA_ANALOGY, A_FIELD, A_FIELD_CAPPED, A_LEVEL_A, A_LEVEL_A_FIELD (script docstring; `record_type=spec` rows).
- **B/D specs:** V1_PRIORS, BD_FIELD, BD_WIDE, BD_PROGRAM.
- **C specs at the current m (wave 39B):** ASSIST; ROUTE_G04 at m = 1.77; ROUTE_A01 at m = 1 (replication), 1.56, 1.77 and 9.28; HYBRID_A01 at m = 1.77.
- **Sweep.** SWEEP_RA applies a fixed r_A ∈ {1.2, 1.0, 0.75, 0.5, 0.33, 0.2, 0.07} under BD_FIELD, with α as in v1.
- **Absorption.** For each (C, A) pair, take the change in mean P(rank first) from V1_PRIORS to BD_FIELD. share_A = ΔA / −(ΔB + ΔD), and share_C likewise.
- **Archetypes:** NAT_LARGE, NAT_MID, CF_1BN, CF_250M and CF_SMALL, with 10,000 draws each. Per-process rows are written for NAT_LARGE only.

### 1.4 Replication [C]

At NAT_LARGE, A_V1 reproduces the recut CSV:
- Assist: V1_PRIORS 0.0021, BD_FIELD 0.0153, BD_WIDE 0.0143, BD_PROGRAM 0.0377.
- A01 routing at m = 1: 0.0668, 0.1926, 0.1858, 0.3089.
- A_RPA_ANALOGY × BD_FIELD reproduces the recut's ABD_FIELD: assist 0.0426; A01 routing at m = 1, 0.2849 and modal string BDCBDDCDDDCBCCD.
- The modal strings match the recut table: Assist/BD_FIELD ADABDDAADDDBAAB; A01 m = 1/BD_FIELD ADCBDDCADDCBAAB.

---

## 2. Evidence in detail

| Id | Domain | Intervention | Measure | Value | Grade | Model use |
|---|---|---|---|---|---|---|
| MI-E01 | UK benefit compliance review (DWP TCR), NAO HC 1336 (Oct 2025) | Rule-based triage plus manual review | Realized ÷ planned throughput | Productivity 0.475 (2023-24), 1.202 (2024-25); cases 1.043; hit rate 0.833; savings 1.107 [F/C] | A | r_A bounds |
| MI-E02 | UK asylum decisions (Home Office PACE), NAO HC 1375 (Jun 2023) | Process simplification, no new technology | Realized ÷ planned productivity gain | 1.00 headline (2.5 of 2.5 per active caseworker per week, against 1.4 at baseline); 72% administrative decisions [F/C] | A (figures), B (mapping) | r_A mode |
| MI-E03 | UK police-complaint casework (IOPC), NAO guide (Mar 2021) | Workload allocation by self-organising teams | Productivity change | "may have increased by 33%" → 0.248 per unit [F/C] | C | consistent with v1 α top |
| MI-E04 | Italian social-security back office, Econometrica 2022 | Manager quality and allocation | Output per office | +10% per 1-SD manager; +6.9% from reallocation → 0.091 / 0.065 per unit [F/C] | A (study), I (mapping) | A_LEVEL_A |
| MI-E05 | Accounts payable, City of Monroe (WA SAO, Aug 2025) | Kaizen: roles, guide, flowcharts | Compliance | reconciled-transaction compliance +86%; 98% of receipts within a day [F] | C | none (no labour measure) |
| MI-E06 | HR hiring and onboarding, two school districts (WA SAO, Apr 2026) | Kaizen: standard forms, checklists, focus time | — | no number reported [F] | C | none |
| MI-E07 | Payment processing, Malaysian GLC (GBMR 2025) | Lean, kaizen, value-stream mapping | Steps, SLA | 6 → 4 steps; SLA > 82% [F] | C | none |
| MI-REF | US federal RPA (HUD OIG, GSA OIG 2023) | Comparator from the recut | Realized ÷ estimated | 0.07; 0.33 [F] | A | A_RPA_ANALOGY |

### 2.1 MI-E01: DWP Targeted Case Review

- **Process.** "Agents are allocated cases for review based on rules that are generated by using data and analytics to look for activity, behaviour or circumstances that suggest a higher risk of error" (para 3.18) [F]. Each review is manual: a preview, a request for evidence, a telephone interview and an outcome (Figure 8).
- **Against plan (Figure 9; paras 3.27–3.28):**

| | 2022-23 | 2023-24 | 2024-25 | Total |
|---|---|---|---|---|
| Agents (FTE), expected / actual | 430 / 946 | 3,430 / 3,039 | 5,930 / 6,061 | — |
| Cases per agent per day, expected / actual | n/a / 0.58 | 1.20 / 0.57 | 0.89 / 1.07 | — |
| Cases completed, expected / actual | 30,000 / 25,000 | 337,000 / 202,000 | 737,000 / 924,000 | 1,104,000 / 1,151,000 |
| Hit rate, expected / actual | 34% / 32% | 25% / 24% | 24% / 20% | — |
| AME savings £m, expected / actual | 9 / 14 | 115 / 89 | 401 / 478 | 525 / 581 |

- **Ratios [C]:**
  - productivity 0.475 (2023-24) and 1.202 (2024-25);
  - cases completed 0.833, 0.599 and 1.254 by year, and 1.043 in total;
  - savings 1.107 in total.
- **Caveats.** This is the throughput of a new programme against its own plan, not the labour saved by fixing an existing process. Case selection uses analytics-built rules. The savings are benefit outcomes, not administrative cost. The agents are outsourced.

### 2.2 MI-E02: Home Office asylum PACE

- **The plan.** "The Programme will increase caseworker weekly decisions from its July 2022 performance of 1.4 to 2.5" (Figure 9) [F]. PACE was set up "to simplify decision-making and improve productivity", with consultants on a £24m contract (para 3.9) [F].
- **The outcome.** "In April 2023, the 640 active caseworkers (those making decisions) achieved the 2.5 decisions weekly" (para 3.9). But "72% of decisions in April 2023 were 'administrative decisions'", which include explicit and implicit withdrawals (para 3.12) [F].
- **The headline realization** is (2.5 − 1.4) / (2.5 − 1.4) = 1.00 [C].
  - The planned gain is a 1.79-fold rise in decisions per caseworker. As labour per decision that is 1 − 1.4/2.5 = 0.44, outside v1's α range. Much of it came from administrative closures and rule changes (demand removal), not from faster handling.
  - Only about 50% of caseworkers were deciding claims. The IPA reported "an acknowledgement within the Home Office that publicly stated targets around productivity levels of caseworkers are not realistic" [F].

### 2.3 MI-E03 and MI-E04: level of the saving

- **IOPC (MI-E03).** "Total output has remained the same despite fewer people working in the team … IOPC says that productivity in one casework team may have increased by 33% compared with 12 months ago" [F].
  - Per unit this is 1 − 1/1.33 = 0.248 [C].
  - It is a self-report about one team, with no stated method, measured over the 12 months to March 2021, at the edge of the 2021+ window.
- **Fenizia (MI-E04).** "a one standard deviation increase in managerial talent raises office productivity by 10%. These gains are driven primarily by the exit of older workers who retire when more productive managers take over … assigning better managers to the largest and most productive offices would increase output by at least 6.9%" [F].
  - Per unit this is 0.091 and 0.065 [C].
  - The study is peer-reviewed and uses administrative output data, but the mechanism is composition, not process. Only the abstract was read (P-G0403-01-01).

### 2.4 Searched but not usable

- **NAO, *Efficiency in government* (HC 303, 2021).** Its optimism-bias examples (shared services 2016; Prison Unit Cost Programme to 2016) predate 2021.
- **NAO, *Cabinet Office functional savings* (2023).** GIAA gave a "moderate" assurance rating and found that processes "did not sufficiently mitigate the risk of claims being under- or overstated" [F]. It gives no realized-against-planned ratio for process work.
- **NAO, *Smarter delivery* (2025).** Its case studies report outcomes (FCDO AI tool, −60% written enquiries; DWP Scotland attendance) but no labour saving from manual fixes.
- **State Lean programmes** (Wisconsin FY18, Nebraska 2022, Results Washington 2014). These are self-reported "hours saved", pre-2021 or without denominators. Not fetched as evidence.
- **VA OIG on the VBA National Work Queue (2021, 2024).** Search snippets describe the workload distribution strategy qualitatively. The reports are hosted on oversight.gov or vaoig.gov and were not retrieved; no ratio was used.

---

## 3. Results [S]

All results are CAL_CENTRAL, gross, unless stated. Full rows are in the CSV.

### 3.1 P(rank first) per option, NAT_LARGE, BD_FIELD

| C variant | A spec | A | B | C | D | n modal A / C |
|---|---|---:|---:|---:|---:|---|
| Assist | A_V1 | 0.385 | 0.186 | 0.015 | 0.413 | 6 / 0 |
| Assist | A_RPA_ANALOGY | 0.101 | 0.288 | 0.043 | 0.568 | 1 / 0 |
| Assist | A_FIELD | 0.324 | 0.209 | 0.020 | 0.447 | 6 / 0 |
| Assist | A_FIELD_CAPPED | 0.239 | 0.240 | 0.027 | 0.494 | 3 / 0 |
| Assist | A_LEVEL_A | 0.089 | 0.292 | 0.042 | 0.577 | 1 / 0 |
| Assist | A_LEVEL_A_FIELD | 0.066 | 0.300 | 0.045 | 0.588 | 1 / 0 |
| Route A01, m = 1.77 | A_V1 | 0.291 | 0.164 | 0.178 | 0.368 | 5 / 2 |
| Route A01, m = 1.77 | A_RPA_ANALOGY | 0.048 | 0.228 | 0.270 | 0.454 | 0 / 5 |
| Route A01, m = 1.77 | A_FIELD | 0.230 | 0.181 | 0.200 | 0.389 | 1 / 5 |
| Route A01, m = 1.77 | A_FIELD_CAPPED | 0.148 | 0.202 | 0.231 | 0.419 | 0 / 5 |
| Route A01, m = 1.77 | A_LEVEL_A | 0.021 | 0.235 | 0.280 | 0.464 | 0 / 5 |
| Hybrid A01, m = 1.77 | A_FIELD | 0.197 | 0.170 | 0.263 | 0.369 | 1 / 6 |

- **Without any B/D cut (V1_PRIORS), A_FIELD alone takes P03 from A** (assist modal string BDDBDDDDDDDBDBD), because r_A's mean is 0.89.
- **Under BD_PROGRAM (B and D at 7–15%), A dominates in every A spec with assistance** (12–13 modal processes). With A01 routing, C is modal in 5 (A_FIELD) to 12 (RPA analogy) processes.

### 3.2 Modal winners (NAT_LARGE, P01–P15)

| C variant | BD_FIELD × A_V1 | BD_FIELD × A_FIELD | BD_FIELD × A_LEVEL_A | BD_FIELD × A_RPA_ANALOGY |
|---|---|---|---|---|
| Assist | ADABDDAADDDBAAB | ADABDDAADDDBAAB | BDABDDDDDDDBDBD | BDABDDDDDDDBDBD |
| Route routing-note ranges, m = 1.77 | ADABDDAADDDBAAB | ADABDDAADDDBAAB | BDCBDDCDDDDBDBD | BDCBDDCDDDDBDBD |
| Route A01, m = 1.56 | ADABDDCADDCBAAB | ADCBDDCADDCBCCB | BDCBDDCDDDCBCCD | BDCBDDCDDDCBCCD |
| Route A01, m = 1.77 | ADABDDCADDCBAAB | BDCBDDCADDCBCCB | BDCBDDCDDDCBCCD | BDCBDDCDDDCBCCB |
| Route A01, m = 9.28 | ADABDDAADDDBAAB | ADABDDAADDDBAAB | BDCBDDCDDDDBDBD | BDCBDDCDDDDBDBD |
| Hybrid A01, m = 1.77 | ADCBDDCADDCBCCB | CDCBDDCADDCBCCD | CDCBDDCDDDCBCCD | CDCBDDCDDDCBCCD |

All strings come from the CSV rows `modal_winners_gross_P01_P15`.

### 3.3 Absorption (NAT_LARGE, BD_FIELD minus V1_PRIORS)

| C variant | A_V1 | A_FIELD | A_FIELD_CAPPED | A_RPA_ANALOGY | A_LEVEL_A |
|---|---:|---:|---:|---:|---:|
| Assist | 0.96 | 0.94 | 0.90 | 0.70 | 0.70 |
| Route routing-note ranges, m = 1.77 | 0.84 | 0.78 | 0.66 | 0.33 | 0.20 |
| Route A01, m = 1.77 | 0.67 | 0.58 | 0.44 | 0.18 | 0.09 |
| Route A01, m = 9.28 | 0.86 | 0.81 | 0.72 | 0.43 | 0.38 |
| Hybrid A01, m = 1.77 | 0.58 | 0.49 | 0.34 | 0.13 | 0.04 |

Each value is A's share of the rank-first probability lost by B and D. C's share is 1 minus it (the rows are `metric=share_C`).

### 3.4 Sweep: fixed r_A under BD_FIELD (NAT_LARGE)

| r_A | Assist A / C, modal | Route A01 m = 1.77 A / C, modal |
|---|---|---|
| 1.20 | 0.479 / 0.011, ADAADDAADDAAAAA | 0.397 / 0.140, ADAADDAADDAAAAA |
| 1.00 | 0.385 / 0.015, ADABDDAADDDBAAB | 0.291 / 0.178, ADABDDCADDCBAAB |
| 0.75 | 0.248 / 0.025, BDABDDADDDDBDAB | 0.149 / 0.230, BDCBDDCDDDCBCCB |
| 0.50 | 0.102 / 0.041, BDABDDDDDDDBDBD | 0.037 / 0.274, BDCBDDCDDDCBCCD |
| 0.33 | 0.029 / 0.051, BDDBDDDDDDDBDBD | 0.005 / 0.287, BDCBDDCDDDCBCCD |
| 0.20 | 0.004 / 0.055, BDDBDDDDDDDBDBD | 0.000 / 0.289, BDCBDDCDDDCBCCD |

- **A stops being modal between r_A = 1.0 and 0.75** for A01 routing (5 processes at 1.0, none at 0.75) and between 0.5 and 0.33 for assistance.
- **The NAO manual-casework ratios (mode 1.0) sit at or above both switch points. The RPA ratios (0.07–0.33) sit below.** The ranking therefore depends on which realization class manual improvement belongs to, and the 2021+ evidence on that is indirect.

### 3.5 Net and value (NAT_LARGE, BD_FIELD, p50)

| C variant | A spec | A pool | Best of A/B/D | C pool | C beyond best of A/B/D (p25–p75) | Net first: A / C / none |
|---|---|---:|---:|---:|---:|---|
| Assist | A_V1 | $1.94m | $2.93m | $445k | $0 | 0.517 / 0.002 / 0.422 |
| Assist | A_FIELD | $1.71m | $2.80m | $445k | $0 | 0.478 / 0.003 / 0.452 |
| Route A01, m = 1.77 | A_V1 | $1.94m | $2.93m | $1.86m | $80k ($0–$489k) | 0.484 / 0.040 / 0.422 |
| Route A01, m = 1.77 | A_FIELD | $1.71m | $2.80m | $1.86m | $133k ($0–$590k) | 0.440 / 0.048 / 0.451 |
| Route A01, m = 1.77 | A_LEVEL_A | $1.06m | $2.44m | $1.86m | $364k ($75k–$968k) | 0.279 / 0.079 / 0.554 |
| Hybrid A01, m = 1.77 | A_FIELD | $1.71m | $2.80m | $2.24m | $313k ($40k–$875k) | 0.425 / 0.065 / 0.450 |

By net value, A or "none" remains the most likely winner in every cell. Under BD_FIELD, C's net rank-first probability is at most 0.108 (hybrid, A_LEVEL_A_FIELD).

---

## 4. What changes in earlier conclusions

| Earlier conclusion | Status |
|---|---|
| Recut: "What replaces B and D is manual improvement (A), not AI"; α is an uncalibrated prior | **Holds under the only audited manual-programme realization (A_FIELD).** A takes 94% of the lost rank-first probability with assistance and stays modal in 6 of 15 processes. It no longer holds if manual improvement realizes well below plan (r_A ≤ 0.5 with assistance; ≤ 0.75 with A01 routing) or if α is at the peer-reviewed level |
| Recut: ABD_FIELD (RPA range on A) as the "same standard" case | **Revised.** The RPA range is a technology-programme realization. The manual-casework audits (MI-E01/E02) centre on 1.0, not 0.33. ABD_FIELD is now a lower-bound stress test (A_RPA_ANALOGY) |
| Recut: routing at the A01 ranges modal in P03, P07 and P11 under BD_FIELD (m = 1) | **At the current m = 1.56–1.77 with A_FIELD, C is modal in P03, P07, P11, P13 and P14.** A_FIELD (mean 0.89) loosens A's hold on P13 and P14. At m = 9.28, C is modal nowhere. The h-asymmetry caveat (wave 37C) still applies: routing's h upper half is not haircut |
| Assistance wins no process | **Unchanged** in every A × B/D cell. Maximum P(C first) is 0.140 (A_LEVEL_A_FIELD × BD_PROGRAM) |

---

## 5. Limits

1. **No realization of manual labour savings was measured.** MI-E01/E02 measure throughput against plan for new or re-scoped casework programmes. The mapping to r_A on α·L is [I], as the recut's mapping of RPA audits onto β·b_p was.
2. **Neither NAO case is a pure manual fix.** DWP's triage rules are built with analytics. PACE's headline relied on administrative decisions (withdrawals) and rule changes, which are closer to redesign (D) than to A.
3. **Domain transfer.** UK benefit and asylum casework and an Italian social-security office stand in for DAF grant, KYC and compliance back offices. No finance or AP study with labour denominators was found.
4. **α level.** One self-report and one peer-reviewed management study do not calibrate α. A_LEVEL_A is a stress test, not a central case.
5. **r_A above 1.** A_FIELD allows over-delivery (up to 1.2, as DWP 2024-25 shows). A_FIELD_CAPPED bounds this; it takes A from 6 to 3 modal processes with assistance.
6. **Independence.** r_A, r_B and r_D are drawn independently (P-G0403-01-04). With a common factor, ranks among A, B and D revert towards V1 priors (wave 37C).
7. **Fixed costs and α's shape are unchanged.** F_A ~ logU($25k, $100k) is untouched.
8. **m is not pinned down** (wave 39B). Results at m = 9.28 differ materially from those at 1.56–1.77. The Amex-priced composite (128 central) was not run, because at m = 9.28 routing is already modal nowhere.
9. **Monte Carlo error only** in the Wilson intervals. Assumption ranges are shown by specs and sweeps.
10. **Blocked or missing:**
    - GAO (robots 403);
    - ANAO (connection closed on robots.txt);
    - USPS OIG (406) and oversight.gov (406 earlier);
    - NCBI E-utilities (robots disallow);
    - Fenizia full text (login);
    - no PMC, NBER or SSRN 2021+ field study of checklists, standard work or queue rules in finance operations with labour denominators was found through search.

---

## D. Data dictionaries

### D1. `manual-improvement-evidence-2026-11-20.csv`

| Column | Meaning |
|---|---|
| evidence_id | MI-E01 … MI-E07; MI-REF (RPA comparator from the recut) |
| domain | operation audited or studied |
| intervention_type | kind of non-technology fix, and whether realized against planned |
| source, year, url | citation, publication year, primary URL |
| retrieved_via | endpoint fetched and robots result |
| quote | verbatim quotes, separated by ` \| ` |
| parameter | model parameter informed (r_A, α, or none) |
| value | stated or computed value |
| value_basis | F (published), C (computed here), F/C (both) |
| grade | A: auditor or peer-reviewed field evidence; B: agency data with weak mapping; C: self-report or case study |
| limitations | main caveats |
| model_use | how the row enters the model |
| retrieved_on | 2026-11-20 |

### D2. `ai-ranking-a-calibrated-2026-11-20.csv` (long format)

| Column | Meaning |
|---|---|
| record_type | `spec` (A, B/D and C definitions), `meta` (draws and seeds), `model` (results) |
| scenario | CAL_CENTRAL (ALL for spec and meta rows) |
| c_variant | ASSIST, ROUTE_G04_M1.77, ROUTE_A01_M1, ROUTE_A01_M1.56, ROUTE_A01_M1.77, ROUTE_A01_M9.28, HYBRID_A01_M1.77 |
| bd_variant | V1_PRIORS, BD_FIELD, BD_WIDE, BD_PROGRAM (as in the recut); `BD_FIELD-V1_PRIORS` for absorption rows |
| a_variant | A_V1, A_RPA_ANALOGY, A_FIELD, A_FIELD_CAPPED, A_LEVEL_A, A_LEVEL_A_FIELD; SWEEP_RA |
| archetype | NAT_LARGE, NAT_MID, CF_1BN, CF_250M, CF_SMALL |
| cell | `main`; `absorption`; `sweep_rA=<r>` |
| process_id | P01–P15 for per-process rows (NAT_LARGE main only); blank otherwise |
| intervention | A, B, C, D or none, where the metric is per option |
| metric | `mean_p_rank_first_gross_P01_P15`, `mean_p_rank_first_net_P01_P15`, `modal_winners_gross_P01_P15` (string in process order), `n_processes_modal_gross`, `sponsor_gross_value_pool_p50`, `sponsor_best_non_AI_pool_p50`, `sponsor_C_incremental_over_best_other_p50`, `p_rank_first_gross`, `modal_winner_gross`; absorption: `lost_BD`, `dA`, `dC`, `share_A`, `share_C` |
| value | metric value |
| lo, hi | 95% Wilson interval (Monte Carlo error) for mean probabilities; p25 / p75 for pools |
| unit | prob, share, count, usd/yr |
| note | basis of the metric |

### D3. `queue-proposals-g0403-01.csv`

Same header and format as `queue-proposals-gap19-13.csv`.

---

## Source register (primary URLs; retrieved 2026-11-20)

| Id | Source | URL |
|---|---|---|
| MI-E01 | NAO, *Tackling benefit overpayments due to fraud and error*, HC 1336 (Oct 2025) | https://www.nao.org.uk/wp-content/uploads/2025/10/Tackling-benefit-overpayments-due-to-fraud-and-error.pdf |
| MI-E02 | NAO, *The asylum and protection transformation programme*, HC 1375 (Jun 2023) | https://www.nao.org.uk/wp-content/uploads/2023/06/the-asylum-and-protection-transformation-programme.pdf |
| MI-E03 | NAO, *Improving operational delivery in government* (Mar 2021); NAO, *Efficiency in government*, HC 303 (Jul 2021) | https://www.nao.org.uk/wp-content/uploads/2021/03/Improving-operational-delivery-in-government-main.pdf ; https://www.nao.org.uk/wp-content/uploads/2021/07/Efficiency-in-government.pdf |
| MI-E04 | Fenizia A., *Managers and Productivity in the Public Sector*, Econometrica 90(3) (2022) | https://www.econometricsociety.org/publications/econometrica/2022/05/01/managers-and-productivity-public-sector |
| MI-E05 | Washington State Auditor's Office, *City of Monroe: AP Process Improvement Success* (Aug 2025) | https://sao.wa.gov/sites/default/files/2025-11/Lean%20Case%20Study%20Monroe_August%202025_1.pdf |
| MI-E06 | Washington State Auditor's Office, *Faster, clearer hiring and onboarding through Lean* (Apr 2026) | https://sao.wa.gov/sites/default/files/2026-05/FINAL_2026%20Lean%20Case%20Study%20Clover%20Park%20Bellingham.pdf |
| MI-E07 | Duriraj B., *Transforming payment processing through lean and kaizen management*, GBMR 17(1) (2025) | https://e-journal.uum.edu.my/index.php/gbmr/article/view/26274 |
| MI-REF | HUD OIG 2021-OE-0007 (2023); GSA OIG A210057 (2023), via the recut | https://www.hudoig.gov/sites/default/files/2023-02/2021-OE-0007.pdf ; https://gsaig.gov/sites/default/files/audit-reports/A210057-1%20Final%20Report.pdf |
| Context (not used for parameters) | NAO, *Cabinet Office functional savings* (Oct 2023); NAO, *Lessons learned: Smarter delivery* (Jun 2025) | https://www.nao.org.uk/wp-content/uploads/2023/10/Report-cabinet-office-functional-savings.pdf ; https://www.nao.org.uk/wp-content/uploads/2025/06/ll-smarter-delivery.pdf |
| Model inputs | mission_ai_bd_recut.py, g0401-0103-ai-bd-recut.md, g0403-0104-m-detection-ofac.md (wave 39B m) | repo |
