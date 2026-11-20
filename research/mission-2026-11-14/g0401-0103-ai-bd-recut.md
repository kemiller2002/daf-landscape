# P-G0401-01 and P-G0401-03: confidence-band evidence, and B and D held to C's evidence standard

*Prepared 2026-11-19. TASKID g0401-0103.*

**Outputs**
- [`scripts/mission_ai_bd_recut.py`](../../scripts/mission_ai_bd_recut.py). It imports `mission_ai_routing_variant.py`, which imports `mission_ai_economics_calibrated.py` and v2; none of them is modified. Stdlib only, functional style. It keeps the same seeds as the earlier scripts (calibrated draws 42, routing 42 + 104729) and adds a new stream, 42 + 15485863, for the realization factors.
- [`data/mission-2026-11-14/ai-bd-recut-2026-11-19.csv`](../../data/mission-2026-11-14/ai-bd-recut-2026-11-19.csv): 75,879 rows (the file has 75,880 lines including the header), from 10,000 draws per archetype (data dictionary in §D1).
- [`data/mission-2026-11-14/ai-confidence-band-evidence-2026-11-19.csv`](../../data/mission-2026-11-14/ai-confidence-band-evidence-2026-11-19.csv): 8 rows (data dictionary in §D2).
- [`data/mission-2026-11-14/queue-proposals-g0401-0103.csv`](../../data/mission-2026-11-14/queue-proposals-g0401-0103.csv): 6 proposals.
- No existing file was modified.

**Read first**
- [gap19-ai-calibration.md](gap19-ai-calibration.md), with its wave-31A corrections.
- [g0401-g0502-ai-routing-and-per-grant.md](g0401-g0502-ai-routing-and-per-grant.md), with its wave-36B corrections. In particular, the routing multiple depends on m and on ρ = 0, and the routing *gain* over assistance depends on s.

**Notation**
- **[F]** published value, quoted.
- **[C]** computed here.
- **[I]** inference or assumption.
- **[S]** scenario output, conditional on stated ranges.

---

## 0. Answers in brief

### (A) Confidence-band evidence (P-G0401-01)

Seven sources were retrieved. Only one of them yields **both** the share of cases auto-closed **and** the error rate inside the auto-closed band from field data, and it does so only through a computation: **E15** (bank AML alerts, retrospective).
- The E15 full text gives the prevalence the routing note lacked: suspicious accounts are "less than 3% of the alerted ones" [F].
- The triage operating point (alerting 20% of negatives while catching over 90% of true positives) therefore implies:
  - **an auto-closed share of about 0.78 of alerts**;
  - **a miss rate inside the closed band of at most 0.39% per closed alert**, or 0.77% at the baseline model's 80% recall [C].
- So the routing note's upper error bound, e = 0.10 attributed to E15, was a share of true positives missed (1 − recall), a denominator the routing note had already flagged as [I]. Per closed alert, E15 implies at most 0.39% (about 0.77% at the baseline’s ~80% recall), 13–26 times below 0.10. [V wave 37C]

The other evidence gives one side only:

| Source | Domain | Auto-closed share h | Error inside band e |
|---|---|---|---|
| E15 (Eddin et al. 2021) | AML alerts, one bank, retrospective | 0.78 [C] | ≤ 0.004 (≤ 0.008 at baseline recall) [C] |
| Gerlings & Constantiou (HICSS 2023) | AML alerts, one bank, in production test | ~0.20 of workload [F] | not reported; **every auto-closed alert re-checked by a dedicated team** (k = 1) [F] |
| FinCEN consent order, Bank of America (2026) | AML scoring threshold (rules, not ML) | — | **0.38–0.45** SAR yield just *below* the threshold, against 0.33–0.34 just above it in the bank’s earlier 2018–2020 testing [F]. The two yields come from different periods, so they show a threshold that had drifted out of calibration, not a same-period band in which it carried no information [V wave 37C] |
| OCBC (arXiv 2609.20110, 2026) | Invoice field extraction, public benchmark | 0.28 / 0.49 / 0.67 of fields at ≤ 5% / 10% / 20% error; native VLM confidence 0.001–0.07 at ≤ 10% [F] | bounded by construction (≤ the target) |
| US State Dept (2024 deck) | Document classification (declassification), production | ~0.80 ("reduced volume for humans to review (by 80%)") [F] | not reported; QC retained [F] |
| Foreign Service Journal (Oct 2023) | Same, 3-month pilot | > 0.65 [F] | overall agreement > 97% (all documents, not the band) [F] |
| E17 Choi & Xie | Bookkeeping | full text blocked (SSRN and Wiley both returned 403) | — |

**For the model [I]:**
- The evidence moves h **above** the E19 range used in the routing note (0.21–0.49). The new range is **h ~ U(0.20, 0.80)**, and e is narrowed to **U(0.004, 0.10)**. These are the "A01" ranges below.
- The upper half of the h range rests on a retrospective validation (E15) and an agency self-report (State). No source measures h and e together in production.
- The BofA order is a warning against assuming any e: by 2022–Q1 2023 the SAR yield just below the line (38–45%) exceeded the 33–34% the bank had measured just above it in 2018–2020, and was seven to nine times its later 5% false-negative tolerance. [V wave 37C]

### (B) B and D held to C's standard (P-G0401-03)

**Evidence.**
- The only 2021+ public evidence with denominators for conventional automation is two inspector-general audits of federal RPA. Both compare realized savings with the ex-ante estimate:
  - **HUD OIG (2023):** 7% realized, 15% if every finished bot ran, and 1–33% for individual bots, including a grant-recipient survey bot that realized 1%.
  - **GSA OIG (2023):** 9 of 10 sampled bots were off their estimate; one finance bot saved about 30 of the 90 minutes assumed (33%); 74% of bots reported no cost avoidance.
- For redesign, the only end-state evidence covers the move from paper checks to electronic payment (P09/P10). Treasury checks are "16 times more likely" than EFT to be reported lost, stolen, returned undeliverable or altered. That supports v1's high d for P10.
- No 2021+ evidence was found on how much of a planned redesign saving is realized in grant or compliance operations. D's realization is therefore borrowed from the RPA audits by analogy [I], or widened to an explicit sweep.

**Does C's probability of ranking first change? Yes in level; only partly in ranking.** Large national, CAL_CENTRAL, mean over P01–P15 of P(C ranks first, gross) [S]:

| C variant | V1 priors | B_FIELD | BD_FIELD | BD_WIDE | BD_PROGRAM | ABD_FIELD |
|---|---:|---:|---:|---:|---:|---:|
| Assist (calibrated) | 0.0021 | 0.0029 | 0.0153 | 0.0143 | 0.0377 | 0.0426 |
| Route, routing-note ranges, m = 1 | 0.0123 | 0.0169 | 0.0723 | 0.0680 | 0.1538 | 0.1612 |
| Route, routing-note ranges, m = 5 | 0.0049 | 0.0071 | 0.0390 | 0.0367 | 0.0939 | 0.1021 |
| Route, A01 ranges, m = 1 | 0.0668 | 0.0806 | 0.1926 | 0.1858 | 0.3089 | 0.2849 |
| Route, A01 ranges, m = 5 | 0.0336 | 0.0420 | 0.1182 | 0.1128 | 0.2094 | 0.2039 |
| Hybrid, A01 ranges, m = 1 | 0.0940 | 0.1127 | 0.2535 | 0.2454 | 0.3872 | 0.3486 |

1. **Assistance (the calibrated C) still wins no process.** Its rank-first probability rises sevenfold to twentyfold, from 0.2% to 1.5–4.3%, but C is the most likely winner in **no process at any archetype** under any B/D variant on CAL_CENTRAL.
2. **What replaces B and D is manual improvement (A), not AI.**
   - When B is cut to the RPA-audit realization range and D to the same range by analogy [I] (BD_FIELD), A becomes the modal gross winner in 6 of 15 processes at a large national (P01, P03, P07, P08, P13, P14). [V wave 37C]
   - A's α ~ U(0.05, 0.25) is also an uncalibrated v1 prior. g0403-01 found no 2021+ audit of realized labour savings from a manual fix. One self-report (IOPC, about 0.25 per unit) and one peer-reviewed management study (Fenizia 2022, 0.065–0.091) bracket α without narrowing it. Mapping NAO manual-casework throughput realization onto A as r_A ~ tri(0.475, 1.0, 1.2) [I] leaves A modal in the same 6 processes with assistance (g0403-01 §3) [V wave 41C]
   - Only when the same realization range is applied to A as well (ABD_FIELD) does C under routing become the modal winner. That happens in P03 and P07 with the routing-note ranges, and in P03, P07, P11, P13 and P14 with the A01 ranges at m = 1.
3. **Routing with the A01 ranges is the variant that changes the ranking**, and at V1 priors it already flips P03 to C.
   - With B and D recut (BD_FIELD), C is modal in P03, P07 and P11 at a large national, and in 4–5 processes at community-foundation archetypes.
   - Its rank-first probability is 19–31% across BD_FIELD, BD_WIDE and BD_PROGRAM.
   - This rests on h up to 0.80 and on m = 1. At m = 5 under BD_FIELD, C is modal in no process at a large national. The upper half of that h range (E15’s retrospective 0.78, State’s self-reported 80%) has not been cut to realized savings the way B and D were. If one common realization factor applied to A, B, C and D alike, the gross ranking would be the V1-priors one: A01 routing modal in P03 only, and assistance and routing-note routing in none [C]. [V wave 37C]

**Break-even realization [S].** Hold everything else fixed and scale realized B and D by a common factor r:
- **Assist:** C does not become the modal winner in any process at any r ≥ 0.07 if A keeps its prior. With A scaled too, C becomes modal in its first process at r = 0.33 and in 8 of 15 at r = 0.07.
- **Route, routing-note ranges, m = 1:** C becomes modal in its first processes (2 of 15) at r = 0.5 with A scaled too, and in 8 at r = 0.2.
- **Route, A01 ranges, m = 1:** C is modal in 1 process at r = 1, 3 at r ≤ 0.5 (A unscaled), and 7 at r = 0.33 (A scaled).
- **Per process:** with assistance at a large national, the share of draws in which C overtakes B and D at a realization of 0.33 or more is at most **8.7% (P07)**. With A01 routing it reaches 60% (P07), 52% (P11) and 51% (P03).
- The audited RPA realization is 0.07–0.33. That lies in the zone where routing C competes and assistance C does not.

**Value pools (sponsor p50, gross, CAL_CENTRAL) [S]**

| Large national | A | B | C | D | Best of A/B/D per process | C above the best alternative |
|---|---:|---:|---:|---:|---:|---:|
| V1 priors | $1.94m | $2.47m | $445k (assist); $1.36m (route G04 m1); $1.95m (route A01 m1); $2.33m (hybrid A01 m1) | $3.96m | $4.23m | $0 (assist); $166 (A01 m1) |
| B_FIELD | $1.94m | $1.06m | as above | $3.96m | $4.11m | $0; $7.4k |
| BD_FIELD | $1.94m | $1.06m | as above | $2.18m | $2.93m | $0; $114k |
| BD_WIDE | $1.94m | $1.16m | as above | $1.68m | $2.72m | $0; $100k |
| BD_PROGRAM | $1.94m | $270k | as above | $1.09m | $2.50m | $0; $189k |
| ABD_FIELD | $827k | $1.06m | as above | $2.18m | $2.46m | $0; $384k |

- **The recut shrinks the non-AI pools.** The best-alternative pool falls by 31% under BD_FIELD and by 42% under ABD_FIELD.
- **But the AI pool that goes beyond what the alternatives already deliver stays small.** In the median draw it is **$0 for assistance in every variant**. For A01 routing it is **$100k–$384k** at a large national across BD_FIELD, BD_WIDE, BD_PROGRAM and ABD_FIELD ($7.4k under B_FIELD), and $16k–$55k at a $1bn community foundation. [V wave 37C]
- **Vendor platform break-even depends on C only, so the B/D recut does not move it.** In p50 sponsors needed, with P(≤ 5 large nationals):
  - assist: 17, P = 0.13;
  - routing-note routing, m = 1: 8, P = 0.38;
  - A01 routing, m = 1: 5, P = 0.50;
  - A01 hybrid: 5, P = 0.58.

---

## 1. Method

### 1.1 Retrieval and robots.txt

- Every fetch went through one helper. The helper read the host's robots.txt with the generic user agent `research-script/1.0`, logged the result, and fetched only when access was allowed.
- A robots.txt that returned 403 or 406 was treated as a block.
- arXiv's crawl delay (15 s) and other stated delays were respected. Fetches to the same host were minutes apart.
- No user agent was changed, and nothing was fetched from sec.gov, crt.sh or certspotter.
- Discovery used a web search tool; every number used comes from the primary document fetched under the rule above.

**Robots log (2026-11-19).**

| Host | robots.txt | Use |
|---|---|---|
| arxiv.org | 200, allowed, crawl-delay 15 | E15, CB-02, CB-04 PDFs |
| www.fincen.gov | 200, allowed | BofA consent order |
| transforming-classification.blogs.archives.gov | 200, allowed | State Dept deck |
| afsa.org | 200, allowed | FSJ page |
| www.gsb.stanford.edu | 200, allowed, crawl-delay 10 | E17 abstract |
| mitsloan.mit.edu | 200, allowed | E17 summary (context only) |
| www.socialscienceregistry.org | 200, allowed | E17 registry (context only) |
| api.openalex.org | 200, allowed | E17 open-access locations |
| api.semanticscholar.org | 404, treated as allowed | E17 open-access locations |
| papers.ssrn.com | 200, allowed | **HTTP 403** (bot challenge), not used |
| onlinelibrary.wiley.com | 200, allowed | **HTTP 403** on both full-text URLs, not used |
| www.hudoig.gov | 200, allowed | HUD OIG report |
| gsaig.gov | 200, allowed | GSA OIG report |
| www.whitehouse.gov | 200, allowed | EO 14247 |
| fiscal.treasury.gov | 200, allowed | Fiscal Service news |
| tfx.treasury.gov | 200, allowed | **HTTP 403**, not used |
| www.federalregister.gov | 200, allowed | API ok; full text gated ("Request Access"), not used |
| www.govinfo.gov | 200, allowed | Uniform Guidance text (no burden numbers found) |
| www.apqc.org | 200, allowed | AP benchmark blog: dated 2018, excluded |
| www.frontiersin.org | 200, allowed | Sanctions screening paper: mock-up data, excluded |
| www.oversight.gov | **406**, blocked | GSA OIG copy not fetched (gsaig.gov used) |
| www.nationalacademies.org | **403**, blocked | State Dept slides copy not fetched |
| payablesplace.ardentpartners.com | **403**, blocked | AP straight-through benchmarks not fetched |
| www.hud.gov | 200, allowed | HUD promotional PDF returned 404 |

### 1.2 Model

- **Base.** The calibrated model's draws under CAL_CENTRAL, plus NAT_LARGE under CAL_FIELD_INLOOP, CAL_TASK_REVIEW and CAL_COMPLIANCE_FULL. The draws are rebuilt by importing `cal.simulate`; `rv.compact` and `rv.c_value` give C.
- **What changes.** B = β·b_p·L and D = d_p·L are multiplied by realization factors:
  - r_B, r_D, and r_A for ABD_FIELD;
  - drawn per iteration from Random(42 + 15485863), independently of each other [I].
- **D_WIDE** remaps d_p's uniform to triangular(0, d1, min(0.95, d1 + 0.10)) for processes without redesign evidence. It keeps the drawn adoption multiplier.
- **Specs.** BD and C specs are listed in the script docstring and in the `record_type=spec` rows.
- **Realization range [I mapping].**
  - Field: triangular(0.07, 0.33, 1.00). The low end is the HUD program level, the mode is the GSA closeout bot (the only GSA bot with a numeric ratio, about 30 of 90 minutes), and the top is a bot that meets its estimate (1 of 10 in the GSA sample). HUD’s billing-bot 33% is not used as support: it arises because a 500-hour estimate for all three bots was reported for each bot. [V wave 37C]
  - Program stress: U(0.07, 0.15).
  - Ignorance: U(0.07, 1.00).
- **A01 routing ranges [I mapping]:** h ~ U(0.20, 0.80) and e ~ U(0.004, 0.10).
  - h: the lower bound is the ~20% workload cut in the bank’s test set-up (CB-02: “Currently the bank is testing a set-up”); the upper bound is E15’s computed 0.78 (retrospective) and State’s self-reported 80%. [V wave 37C]
  - e: the lower bound is E15's computed in-band miss; the upper bound is the 10% accepted-tier error budget (CB-04).
  - k is drawn from the same uniforms as the routing note, so it is identical draw by draw; ρ = 0.
- **Break-even realization.** For each draw and process, r_be = C / max(B_v1, D_v1) when C > A and C > 0, and 0 otherwise. Sweeps apply a fixed r to B and D (`SWEEP_R_BD`) or to A, B and D (`SWEEP_R_ABD`).
- **Replication [C]:**
  - Assist / V1 priors, NAT_LARGE: P(C first) = 0.0021, pool $444,899, P(break-even ≤ 5) = 0.132. This matches the calibrated note (0.002, $445k, 0.13).
  - Route m = 1 (routing-note ranges): P(C first) = 0.0123, pool $1,364,949, P(break-even ≤ 5) = 0.378. This matches the routing note exactly.
  - Modal winners: BDABDDDDDDDBDBD, as in the calibrated note.

---

## 2. Part A: confidence-band evidence in detail

### 2.1 E15, full text (CB-01, CB-01c)

- **Prevalence:** "The percentage of suspicious accounts in our dataset is less than 3% of the alerted ones, resulting in over 97% false positives" [F].
- **Operating point:** "recall@20%FPR … translates to a reduction of the false positives by 80%". Elsewhere: "allows us to alert only 20% of the events while capturing over 90% of the suspicious entities" [F]. The baseline LightGBM model reaches "close to 80% recall@20%FPR" [F].
- **Computation [C]**, with prevalence π and recall ρ:
  - auto-closed share = 0.8(1 − π) + (1 − ρ)π;
  - miss rate inside the closed band = (1 − ρ)π divided by that share.
  - At π = 0.03 and ρ = 0.90: closed share 0.779, in-band miss 0.0039.
  - At ρ = 0.80: closed share 0.782, in-band miss 0.0077.
  - Because π < 0.03 and the graph model’s recall is “over 90%”, 0.39% is an upper bound. The 0.77% is approximate, because the baseline reaches “close to 80%” recall, possibly slightly below 0.80. Both count only SAR-label misses on account-days. [V wave 37C]
- **Caveats:**
  - A retrospective validation, not a deployment.
  - Labels are account-days derived from SAR-linked transactions.
  - ML triage, not gen-AI.
  - In production, closed alerts would still be sampled (see 2.2).

### 2.2 Production AML auto-close (CB-02)

- The bank's random-forest model scores lower-complexity scenarios from 1 to 100. "Lowest-scoring alerts … within the bank's risk appetite are auto-closed" [F].
- "When closing alerts (A), the model reduces the workload of investigators by ~20%" [F].
- "For now, auto-closed alerts are checked by dedicated investigators and risk owners to ensure the model is operating according to the agreed risk appetite" [F].
- So in production testing, k = 1 on the closed band.
- The interviews give no in-band error rate.

### 2.3 E17 (CB-07): what is and is not available

- The Stanford GSB abstract page says: "reallocation of approximately 8.5% of accountant time from routine data entry … expertise increases intervention when AI confidence scores signal uncertainty" [F].
- The rates of intervention by confidence score are in the full text only.
- OpenAlex and Semantic Scholar list the Wiley version as hybrid open access under CC BY. However, both Wiley URLs and the SSRN page returned HTTP 403 (bot challenge), so the paper was not read. This remains open (P-G0403-03).

### 2.4 Other domains

- **Invoices (CB-04).** OCBC's calibrated gate auto-approves 28.1% / 49.4% / 66.5% of DocILE fields at error targets of ≤ 5% / 10% / 20%. Native VLM confidence clears 0.1–7.0% at ≤ 10% [F].
  - This is a benchmark on 500 documents, not a field study.
  - Field-level approval implies a lower invoice-level straight-through rate [I].
- **Document classification (CB-05, CB-06).**
  - The State Department reports an 80% cut in human review volume in production. Humans review "cables the model is unsure of" and perform QC [F].
  - The pilot matched past human decisions in more than 97% of cases [F].
  - Neither source gives the error inside the auto-decided band.
- **KYC onboarding.** No 2021+ source with denominators was found. The one sanctions-screening paper retrieved (Frontiers in AI, 2024) uses mock-up data and was excluded.
- **Miscalibrated thresholds (CB-03).**
  - The BofA order shows the opposite case. Event groups scoring 16–19 points, just below the investigation threshold, had a 38–45% SAR yield in 2022–Q1 2023, against 33–34% just above it in the bank’s 2018–2020 testing. The order compares the two periods; it gives no same-period yield above the threshold. [V wave 37C]
  - The bank's later false-negative tolerance was 5% (7.5% for Board escalation).
  - Correcting the threshold was expected to add 16,000 investigations a month, "double [the] prior ongoing monthly volume", and 750 staff [F].

---

## 3. Part B: B and D evidence in detail

### 3.1 Conventional automation

- **HUD OIG, 2021-OE-0007 (17 Feb 2023).**
  - "only seven distinct bots were in use, and annual labor hour savings totaled approximately 1,015, or 7 percent of the amount HUD estimated" [F].
  - A potential 2,091 hours (15%) if finished bots ran [F].
  - A grants bot "planned to save 2,100 hours annually by sending a survey form to grant recipients" was "expected to save only 24 labor hours annually, or 1 percent" [F].
  - Three internal-billing bots: 33% of the reported estimate [F]. The 500-hour estimate covered all three bots combined but was reported for each (report p. 5) [F], so this is an over-report, not a realized-against-planned shortfall. [V wave 37C]
- **GSA OIG, A210057/B/5/F24001 (30 Nov 2023).**
  - "actual results varied from the estimates for 9 of the 10 bots we sampled" [F].
  - The OCFO Project Closeout bot: "estimated savings based on the task taking 90 minutes, whereas users reported time savings only averaged approximately 30 minutes" [F].
  - "74 percent of bots resulted in no cost avoidance" [F].
  - GSA's claimed 240,000 hours a year was "inaccurate and unreliable" [F].
- **Agency claims without denominators.** GSA's 430,000 hours and Fiscal Service's 65,000 hours, both as quoted by HUD OIG, are recorded but not used. GSA OIG found GSA's own figure unreliable.

**Mapping [I].**
- v1's β·b_p·L is an ex-ante estimate of the same kind the audits test, so realized B = r_B·β·b_p·L.
- The GSA closeout bot is a task-level check. With b = 1 (a fully rule-based task) it saved 0.33 of task time, which sits inside v2's β range of 0.30–0.70 near its lower end.
- The HUD program ratio (0.07) also counts bots that were never used. That is partly a fixed-cost failure, not a per-case shortfall. It is therefore kept as a stress case (BD_PROGRAM), not as the central case.

### 3.2 Redesign

- **P09/P10, paper check to EFT.** EO 14247: "Department of the Treasury checks are 16 times more likely to be reported lost or stolen, returned undeliverable, or altered than an electronic funds transfer" [F]. Fiscal Service: "over 16 times more likely to get lost, stolen, altered, or delayed" [F].
  - Per payment converted, 1 − 1/16 = 0.94 of exceptions are avoided [C].
  - That is consistent with v1's d = 0.85 for P10 and 0.80 for P09, before the coordination-adoption multiplier U(0.3, 1.0).
  - These two processes keep r_D = 1 in BD_FIELD and BD_PROGRAM.
- **P14, AML review threshold (BD-E05).**
  - The bank's 2021 recalibration claimed "case load reduction" of over 8,200 cases with "permissible" SAR loss [F].
  - The supervisory outcome was a $1.2bn penalty, and correcting the threshold doubled investigation volume [F].
  - So a redesign saving in compliance review can be negative once supervision applies. v1's d = 0.20 for P14 has no floor below zero [I].
- **Other processes.** No 2021+ source states realized redesign savings for KYC, eligibility verification, due diligence, receipts or reporting.
  - The Uniform Guidance 2024 rule raised the single-audit threshold, but its text gives no burden estimate. Federal Register full text was gated, and the govinfo text had no figures.
  - Ardent Partners' AP straight-through benchmarks were robots-blocked. APQC's AP cost ratio dates from 2018 and was excluded.
  - Hence BD_WIDE.

---

## 4. Results [S]

All results are for CAL_CENTRAL unless stated. Full rows are in the CSV.

### 4.1 Ranking

**Modal gross winners, P01–P15, large national** (A manual improvement, B conventional automation, C AI, D redesign):

| C variant / BD | V1 priors | BD_FIELD | ABD_FIELD |
|---|---|---|---|
| Assist | BDABDDDDDDDBDBD | ADABDDAADDDBAAB | BDABDDDDDDDBDBD |
| Route, routing-note ranges, m = 1 | BDABDDDDDDDBDBD | ADABDDAADDDBAAB | BDCBDDCDDDDBDBD |
| Route, A01 ranges, m = 1 | BDCBDDDDDDDBDBD | ADCBDDCADDCBAAB | BDCBDDCDDDCBCCD |
| Hybrid, A01 ranges, m = 1 | BDCBDDDDDDDBDBD | ADCBDDCADDCBCCB | CDCBDDCDDDCBCCD |

All strings are from the CSV rows `modal_winners_gross_P01_P15`.

**Archetypes.**
- Rank-first probabilities are almost the same across archetypes, because B, C and D all scale with L.
- Assist is never modal anywhere.
- At community-foundation archetypes, A01 routing under BD_FIELD is modal in 4–5 processes (CF_250M 4; CF_1BN and CF_SMALL 5), and hybrid in 8.

**Framing (large national).**
- Under CAL_FIELD_INLOOP, assist stays at or below 0.7% in every B/D variant.
- Under CAL_TASK_REVIEW with ABD_FIELD, assist reaches 7.8% and is modal in 1 process.
- Routing results are identical across framings (they do not use s), except under compliance stress (k = 1 on P01, P07, P08 and P14). There A01 routing under BD_FIELD falls to 11.9% and 2 modal processes.

**Net ranking.**
- "None" or A remains the most likely net winner.
- Under ABD_FIELD, "none" is first in 60% of process-draws, because every intervention's gross value shrinks against unchanged fixed costs.
- C's net rank-first probability is at most 11.2% (A01 hybrid, ABD_FIELD); for A01 routing it is at most 8.8%.

### 4.2 Why A matters

- Cutting only B and D hands most processes to A (P(A first) rises from 0.07 to 0.39 under assistance).
- That outcome tests A's prior, not AI. α ~ U(0.05, 0.25) has no source. g0403-01 holds A to throughput realization from two NAO casework audits [I]: with assistance A still takes 94% of what B and D lose. With A01 routing at m = 1.77, C is modal in 5 processes and A in 1. If α is set to the peer-reviewed level, A is modal in at most 1 process. The r_A evidence is throughput against plan, not realized labour savings [V wave 41C]
- ABD_FIELD applies the same realization range to A. It is the closest available "same standard for every option" case, and it is also [I] (P-G0403-01). g0403-01 retains it as a lower-bound stress test (A_RPA_ANALOGY) because the RPA range is a technology-programme realization [V wave 41C]

### 4.3 Value pools and break-even

- Value pools are in §0(B), with p25–p75 in the CSV.
- Vendor break-even is in §0(B).
- Per-process break-even realization rows are `breakeven_realization_r_p50` and `p_breakeven_realization_ge_0.33` / `ge_0.07`. The median r_be is 0 in every process except P03, P07 and P11 under A01 routing (0.43, 0.62 and 0.37). In all other cases A beats C in more than half of draws whatever B and D realize.

---

## 5. What changes in earlier conclusions

| Earlier conclusion | Status |
|---|---|
| Calibrated note: the ranking is robust; C is weak | **Holds for assistance.** C wins no process under any B/D standard tried; its rank-first probability rises at most to 4%. |
| Routing note: C's last place reflects B and D's uncalibrated priors | **Partly confirmed.** Cutting B to RPA-audit realization and D to the same range by analogy [I] raises C's rank-first probability about sixfold (route m = 1: 0.012 → 0.072). The first beneficiary is A, whose prior is also unsourced. C becomes modal only with routing and either A recut too or the A01 h range, whose upper half is not haircut. [V wave 37C] |
| Routing note: e up to 0.10 from E15 | **Revised.** E15's per-closed-alert miss rate is ≤ 0.4–0.8%. 0.10 now rests on a benchmark error budget (CB-04). |
| Routing note: h from one radiology study, 0.21–0.49 | **Widened.** Field-adjacent back-office evidence spans 0.20–0.80 (AML in-bank testing 0.20; AML retrospective 0.78; document classification 0.65–0.80, an agency self-report and a pilot). [V wave 37C] In-band error is measured only in the retrospective AML case. |

---

## 6. Limits

1. **Cross-domain transfer [I].** No source is a DAF back office. Two RPA audits (both federal) stand in for conventional automation; one AML validation, one bank case study, one State Department program and one invoice benchmark stand in for confidence-gated routing.
2. **Realization is not the same object as β.** The audits measure realized against planned hours, including bots never deployed. Mapping that onto v1's β·b_p, itself already a "conventional efficiency", may double-count pessimism. BD_WIDE (r up to 1) bounds this.
3. **D realization is borrowed.** No redesign audit was found (P-G0403-02). P09/P10 keep r_D = 1 on end-state evidence that covers exceptions, not labour.
4. **A is still a prior.** ABD_FIELD applies the RPA realization range to A by analogy.
5. **Independence.** r_A, r_B and r_D are drawn independently. Positively correlated realization (one sponsor's execution quality) would move ranks less.
6. **Fixed costs are unchanged.** HUD spent $489,885 on a bot expected to save 100 hours a year. F_B is not recut (P-G0403-05).
7. **h and e for C** are global per draw. m is now bounded ([g0403-04-escaped-error-cost.md](g0403-04-escaped-error-cost.md)). Conditional on enforcement, a missed SAR at the four core depository banks cost $36k–$471k in FinCEN penalty (2,600–34,000 P14 handling units). The DAF excise regime gives 1–174 units per escaped P07/P08 error, and the composite central m is 2.4 [C/I]. [V wave 38B] P08 carries no sponsor tax, so the composite central is 2.20. With IRS-bounded detection (P ≈ 0.0018), an escaped P07 error costs about 1.02 units at a $5,100 grant, and the central m is 1.56–1.77 [C/I] [V wave 39B]
8. **Interval types.** Wilson intervals in the CSV cover Monte Carlo error only. Assumption ranges are shown by variants and sweeps.
9. **Blocked or missing sources:**
   - E17 full text (SSRN and Wiley 403).
   - Ardent Partners (robots 403).
   - State Department slides on nationalacademies.org (robots 403).
   - oversight.gov copies (robots 406).
   - Treasury TFM bulletin (403).
   - Federal Register full text (gated).
   - No 2021+ KYC onboarding, AP production or grant-review study reporting both h and e.

---

## D. Data dictionaries

### D1. `ai-bd-recut-2026-11-19.csv` (long format)

| Column | Meaning |
|---|---|
| record_type | `evidence` (CB-* and BD-* sources), `spec` (B/D or C variant definitions), `meta` (draws and seeds), `model` (results) |
| scenario | calibrated scenario: CAL_CENTRAL (all archetypes), or CAL_FIELD_INLOOP / CAL_TASK_REVIEW / CAL_COMPLIANCE_FULL (NAT_LARGE only) |
| c_variant | ASSIST, ROUTE_G04_M1, ROUTE_G04_M5, ROUTE_A01_M1, ROUTE_A01_M5, HYBRID_A01_M1 (§1.2) |
| bd_variant | V1_PRIORS, B_FIELD, BD_FIELD, BD_WIDE, BD_PROGRAM, ABD_FIELD; SWEEP_R_BD and SWEEP_R_ABD for the realization sweeps |
| archetype | NAT_LARGE, NAT_MID, CF_1BN, CF_250M, CF_SMALL, REF_V1_1M (as in v2) |
| cell | `main`; `vs_assist_v1` (modal changes against Assist / V1 priors); `sweep_r=<r>` |
| process_id | P01–P15 for per-process metrics; blank for sponsor-level metrics |
| intervention | A, B, C, D or none, where the metric is per option |
| metric | `mean_p_rank_first_gross_P01_P15`, `mean_p_rank_first_net_P01_P15`, `p_rank_first_gross`, `p_rank_first_net`, `modal_winner_gross` / `_net`, `modal_winners_gross_P01_P15` / `net` (strings in process order), `n_processes_C_modal_gross`, `processes_modal_winner_changed_gross`, `sponsor_gross_value_pool_p50` (sum of positive gross over P01–P15), `sponsor_best_non_AI_pool_p50`, `sponsor_C_incremental_over_best_other_p50`, `vendor_breakeven_sponsors_p50_finite`, `p_vendor_breakeven_le_available`, `p_C_net_positive`, `breakeven_realization_r_p50`, `p_breakeven_realization_ge_0.33`, `p_breakeven_realization_ge_0.07`. For evidence rows, metric holds the evidence id |
| value | metric value; for evidence rows, the parameter value or bound |
| lo, hi | 95% Wilson interval (Monte Carlo error) for probabilities, or p25 / p75 for pools |
| unit | prob, usd/yr, count, sponsors, ratio |
| note | comparison basis, or for evidence rows: part, domain, source, year, URL, parameter, value basis, limitations (separated by ` \|\| `) |

### D2. `ai-confidence-band-evidence-2026-11-19.csv`

| Column | Meaning |
|---|---|
| evidence_id | CB-01 … CB-07 (CB-01c is computed from CB-01) |
| part | A (P-G0401-01) |
| domain | AML alerts, invoice fields, document classification, bookkeeping |
| source, year, url | citation, publication year, primary URL |
| retrieved_via | endpoint actually fetched |
| quote | verbatim quote(s), separated by ` \| ` |
| parameter | what the quote informs (prevalence, h, e, k, m) |
| value | stated or computed value |
| value_basis | F (published) or C (computed here) |
| grade | A: regulator, auditor or peer-reviewed field evidence; B: real-data single institution or agency self-report; C: benchmark or secondary report |
| limitations | main caveats |
| routing_parameter | routing-model parameter(s) informed |
| retrieved_on | 2026-11-19 |

### D3. `queue-proposals-g0401-0103.csv`

Same header and format as `queue-proposals-gap19-13.csv`.

---

## Source register (all primary URLs; retrieved 2026-11-19)

| Id | Source | URL |
|---|---|---|
| CB-01 | Eddin et al., *Anti-Money Laundering Alert Optimization Using Machine Learning with Graphs*, arXiv 2112.07508 (2021) | https://arxiv.org/abs/2112.07508 |
| CB-02 | Gerlings & Constantiou, *Machine Learning in Transaction Monitoring: The Prospect of xAI*, HICSS-56 (2023), arXiv 2210.07648 | https://arxiv.org/abs/2210.07648 |
| CB-03, BD-E05 | FinCEN Consent Order 2026-03, Bank of America N.A. (Oct 2026) | https://www.fincen.gov/system/files/2026-10/BoA-Consent-Order-Execution-Final.pdf |
| CB-04 | Jin et al. (OCBC), *Perception, Layout, and Validation …*, arXiv 2609.20110 (2026) | https://arxiv.org/abs/2609.20110 |
| CB-05 | US Department of State, *AI Pilot Results*, 24 June 2024 | https://transforming-classification.blogs.archives.gov/wp-content/uploads/sites/10/2024/07/State-AI-Pilot-Results-June-24-2024.pdf |
| CB-06, BD-E06 | AFSA, *The Foreign Service Journal*, Oct 2023 | https://afsa.org/sites/default/files/flipping_book/1023/19 |
| CB-07 | Choi & Xie, *Human + AI in Accounting* (Stanford GSB page); JAR doi 10.1111/1475-679x.70052 (not read: 403) | https://www.gsb.stanford.edu/faculty-research/working-papers/human-ai-accounting-early-evidence-field |
| BD-E01 | HUD OIG, *HUD's Robotic Process Automation Program Was Not Efficient or Effective*, 2021-OE-0007 (Feb 2023) | https://www.hudoig.gov/sites/default/files/2023-02/2021-OE-0007.pdf |
| BD-E02 | GSA OIG, *GSA's RPA Program Lacks Evidence to Support Claimed Savings*, A210057/B/5/F24001 (Nov 2023) | https://gsaig.gov/sites/default/files/audit-reports/A210057-1%20Final%20Report.pdf |
| BD-E03 | Executive Order 14247, *Modernizing Payments To and From America's Bank Account* (Mar 2025) | https://www.whitehouse.gov/presidential-actions/2025/03/modernizing-payments-to-and-from-americas-bank-account/ |
| BD-E04 | Bureau of the Fiscal Service, *Paper Checks Are Going Away* | https://fiscal.treasury.gov/about-us/news/paper-checks-going-away |
| Model inputs | gap19-ai-calibration.md; g0401-g0502-ai-routing-and-per-grant.md; scripts/mission_ai_economics_calibrated.py; scripts/mission_ai_routing_variant.py | repo |
