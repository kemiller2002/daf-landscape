# AI economics: calibrating time saving, re-review and amenability from published evidence

*Queue item P-GAP19-04. Prepared 2026-11-19.*

- **Calibrates:** the v2 and v2b models in [ai-economics-v2-observed-costs.md](ai-economics-v2-observed-costs.md) (§3.2 lists the assumptions) and `scripts/mission_ai_economics_v2b.py`.
- **Evidence table:** `data/mission-2026-11-14/ai-calibration-evidence-2026-11-19.csv` (21 sources, E01–E21, all 2021 or later).
- **Script:** `scripts/mission_ai_economics_calibrated.py`. It imports v2 and v2b unchanged, uses stdlib only, functional style and seed 42.
- **Output:** `data/mission-2026-11-14/ai-process-economics-calibrated-2026-11-19.csv` (23,577 rows; 10,000 draws per scenario and archetype). No existing file was overwritten.
- **Queue proposals:** `data/mission-2026-11-14/queue-proposals-g04.csv`.

**Notation.**
- **[F]** published measurement, as stated in the retrieved source.
- **[I]** inference. Every mapping from a published measurement to a model parameter is an inference.
- **[S]** scenario output. It is conditional on the calibrated ranges, which are still assumptions, though now bounded by evidence.

---

## 1. Bottom line

1. **The A/B/C/D ranking does not change.** [S]
   - In 156 comparisons (13 scenario-model runs, 3 of them the baselines themselves, × 6 archetypes × gross and net; 120 are non-trivial), the most likely winner changes in **no process**. That covers v2 and both v2b pool variants [V wave 31A].
   - Redesign (D) and conventional automation (B) still win by gross. Manual improvement (A) or "none" still wins by net.
   - The v2 conclusion that rankings "follow these assumptions" is therefore only half right. The ranking is robust to s, q and a. What the assumptions set is **how large the AI value is**.
2. **AI on the existing workflow (C) gets weaker, not stronger.** [S]
   - At a large national, the mean probability that C ranks first by gross falls from **0.029 to 0.002** (CAL_CENTRAL).
   - In the two processes where C was competitive it falls further: P07 non-standard due diligence from **0.16 to 0.013**, and P03 complex assets from **0.15 to 0.016**.
   - The probability that C clears its own fixed cost in P07 at a large national falls from **0.59 to 0.31**. It is 0.15 under the field framing, 0.45 under the task framing, and 0 if every AI-handled compliance case gets a human re-review.
3. **The AI value pool is about 60% smaller.** [S] Median sponsor AI gross value (sum of positive C across P01–P15) under CAL_CENTRAL against v2:

   | Archetype | v2 | Calibrated |
   |---|---:|---:|
   | Large national | $1.18m | **$445k** (p25–p75 $145k–$1.06m) |
   | $1bn community foundation | $164k | $69k |
   | $250m community foundation | $42k | $18k |
   | Community foundation, $10–100m | $5.9k | $2.4k |

   The range across framings is wide. At a large national the median runs from **$202k** (field framing) to **$793k** (task framing).
4. **v2's implied saving sits above every field measurement retrieved.** [S+I]
   - Across P01–P15, v2 implies that AI saves a median **17%** of process labour (p5–p95 10–27%).
   - The field evidence is lower:
     - Production customer-support AI: about **9–13%** per case (E01, E02).
     - Workers using general-purpose tools: about **3–5%** of all hours (E08, E09).
     - UK civil servants: **19 minutes a day** against a comparison group (E06).
   - The calibrated central median is **7.9%** (p5–p95 2–17%), inside the field-to-experiment range.
5. **The shared-platform case narrows.** [S]
   - With the vendor signing the most valuable sponsors first, break-even on the observed FY2024 population of community foundations plus nationals is reachable in **16%** of draws, against 43% in v2.
   - For community foundations alone it is reachable in **3.6%**, against 16% in v2.
   - A homogeneous large-national network needs a median of **17** sponsors, against 8 in v2. Only 5 exist.
6. **What moves the result most is how re-review is costed** (§5). [S]
   - If the measured error rates were charged to *every* touched case, as the literal v2 definition of q allows, the large-national pool would fall to **$110k**.
   - If v2's q range were charged to every case alongside field-measured s, the pool would fall to **$0**.
   - The central case charges review only to AI-handled cases. That is a modelling choice (§3.2). It is not a measurement. In the field framing it also scales v2's unsourced QA range by a (≈0.37), cutting that charge by about 60% without new evidence. So the field-framing $202k, and half of the central $445k, depend on the basis as much as on the evidence [V wave 31A].

---

## 2. Evidence collected

### 2.1 Retrieval

- Sources were read through open endpoints whose robots.txt was read first:
  - OpenAlex DOI records, including the abstract.
  - arXiv `/abs` pages, with the 15-second crawl delay respected.
  - NBER working-paper PDFs.
  - The GOV.UK Content API.
  - Bank of England pages.
- Each row of the evidence CSV records the endpoint used.
- **Hosts not used:**
  - `api.crossref.org`: its robots.txt returns an error, so it was not fetched.
  - `export.arxiv.org`: robots.txt disallows all access.
  - SSRN: abstract pages returned HTTP 403. For the Choi and Xie paper, the abstract of the published *Journal of Accounting Research* version was used instead.
  - `assets.publishing.service.gov.uk`: robots.txt returns 404, so the DBT Copilot PDF was not fetched.
  - `www.aph.gov.au`: blocked by its firewall, so the ASIC summarisation trial was not retrieved.
- OpenAlex search was paused for anonymous users, and the free daily budget then ran out. That ended open discovery: no further relevant studies could be found.

### 2.2 Evidence table (summary; full rows in the CSV) [F]

| ID | Source (year) | Setting, sample | Measured effect | Parameter |
|---|---|---|---|---|
| E01 | Brynjolfsson, Li & Raymond, NBER w31161 (2023) | Customer-support chat, 5,179 agents, staggered roll-out | Chats/hour +14% (0.37 on 2.6); handle time −9% (−3.8 min); resolution +1.3 pp on 82%; **38%** of AI suggestions followed (IQR 23–50%) | s (field), r |
| E02 | Same authors, *QJE* (2025), doi:10.1093/qje/qjae044 | 5,172 agents | Resolutions/hour **+15%**; top-skill agents see small quality declines | s (field) |
| E03 | Dell'Acqua et al., *Organization Science* (2026; WP 2023) | 758 BCG consultants, randomised | Inside the AI frontier: **25.1% faster**, 12.2% more tasks. Outside it: **19%** less likely to be correct | s (task), r, a |
| E04 | Noy & Zhang, *Science* (2023) | 453 professionals, writing tasks, randomised | Time **−40%**, quality +18% | s (task) |
| E05 | Dillon et al., NBER w33795 (2025) | 66 firms, 7,137 workers, randomised Copilot | Users spend 2 fewer hours a week on email; no detected change in task mix | s·a (whole job) |
| E06 | DWP Copilot evaluation, GOV.UK (2026) | 3,549 licences; 1,716 users against 2,535 comparison | **19 min/day** saved (SUR); 85% rate meeting-note accuracy good or better; users report verification overhead | s·a, r |
| E07 | GDS cross-government Copilot experiment, GOV.UK (2025) | 20,000 licences, self-report, no control | 26 min/day self-reported | s·a (upper bound) |
| E08 | Bick, Blandin & Deming, NBER w32966 (2024) | US representative survey | Users save **5.4%** of work hours; 1.4% across all workers | s·a |
| E09 | Humlum & Vestergaard, NBER w33777 (2025) | Denmark, 11 exposed occupations including accountants and customer support; about 25,000 responses per round linked to administrative data | Adopters save about **3%** of hours. Null effect on earnings and hours (rules out >2%). New workloads for 12% of users, including AI quality-review tasks | s·a, q |
| E10 | Eloundou et al., *Science* (2024) | O*NET task exposure | **15%** of tasks faster with an LLM alone; **47–56%** with LLM-based software | a (ceiling) |
| E11 | Becker et al. (METR), arXiv 2507.09089 (2025) | 16 experienced developers, 246 tasks, RCT | AI **increased** time by 19%; developers believed it saved 20% | s (lower tail) |
| E12 | Peng et al., arXiv 2302.06590 (2023) | Developers, one scoped task, controlled | **55.8%** faster | s (upper bound) |
| E13 | Magesh et al., *Journal of Empirical Legal Studies* (2025) | Commercial RAG legal research tools | Hallucinate **17–33%** of the time | r |
| E14 | Martin et al., arXiv 2401.16212 (2024) | LLMs against junior lawyers on contract review | Accuracy matches or exceeds; seconds instead of hours; −99.97% cost, excluding human verification | ceiling only |
| E15 | Eddin et al., arXiv 2112.07508 (2021) | Real-bank AML alerts, ML triage (not gen-AI) | **−80%** false positives while detecting **>90%** of true positives | s, r for P14 |
| E16 | Bank of England & FCA AI survey (2024) | 118 UK financial firms | 55% of use cases have some automated decision-making; **2%** fully autonomous | HITL share |
| E17 | Choi & Xie, *Journal of Accounting Research* (2026) | 277 accountants; 79 SMEs, >200k transactions | Productivity gains (magnitude not in the abstract); effort shifts to QA; accountants intervene when **AI confidence is low**; following non-consensus AI raises error | review design |
| E18 | Angelova, Dobbie & Yang, NBER w31747 (2023) | Bail decisions | **90%** of judges do worse than the algorithm when they override it | override value |
| E19 | Agarwal et al., NBER w31422 (2023) | Radiologists, randomised | AI assistance does not uniformly help; best design routes each case to AI or to a human | C design |
| E20 | Liang et al., *NEJM AI* (2024) | 308 researchers | 57.4% find GPT-4 feedback helpful | grant-review analogue |
| E21 | Choi, Monahan & Schwarcz, *Minnesota Law Review* (2024) | Law students, RCT | Large, consistent speed gains; magnitude not retrieved | direction only |

### 2.3 Coverage against the brief

| Brief area | Retrieved | Gap |
|---|---|---|
| Customer support | E01, E02 (strong field evidence) | — |
| Document and legal review | E03, E13, E14, E21 | Production field study with time and error measured together |
| KYC/AML alerts | E15 (ML triage; one bank); E16 (regulator survey) | No public gen-AI field study of KYC onboarding or alert disposition with stated denominators |
| Invoice/AP processing | E17 (bookkeeping; magnitudes not in the abstract) | No AP field measurement retrieved |
| Grant review | E20 (perception only) | No time or error measurement |
| Error and re-review rates | E01 (non-adherence), E06, E13, E15, E03 | No measured **second-line QA sampling rate** in any source |
| Human-in-the-loop overrides | E16, E17, E18, E19 | No financial-services override rate |

---

## 3. Mapping evidence to parameters [I]

The model sets C = s·a_p·L − 0.5·q·L − inference ([v2 §2](ai-economics-v2-observed-costs.md)).

### 3.1 s, AI time saving

The sources measure two different things, so they are kept as two framings rather than averaged.

- **Field framing (CAL_FIELD_INLOOP): s ~ triangular(0.00, 0.12, 0.30).**
  - Production deployments measure saving **net of the worker's own checking**:
    - E01: −9% handle time, about 12% from throughput.
    - E02: about 13% from +15% resolutions per hour.
  - The lower bound is 0. Expert, context-heavy work can be slowed (E11), and E09 rules out large changes in hours.
  - The upper bound of 0.30 sits just above the in-frontier experiment (E03, 0.25).
- **Task framing (CAL_TASK_REVIEW): s ~ triangular(0.10, 0.30, 0.56).**
  - Task experiments measure time to a first output **before any downstream check**:
    - E03: 0.25.
    - E04: 0.40.
    - E12: 0.558, a single scoped coding task, used as the upper bound.
  - E14's near-100% machine-time saving excludes verification, so it is not used.
- v2 used triangular(0.15, 0.40, 0.70). Its mode equals the writing experiment (E04), and its upper half lies above every measured value.

### 3.2 q, re-review share

The model charges re-review at half the handling minutes. v2 defines q as a share of **all** touched cases.

**Inference:** only AI-handled cases carry AI-output risk. So a measured rate r of outputs needing correction should enter as **q_p = r·a_p**. Both calibrated framings use this basis.

- **Field framing:**
  - The worker's own checking is already inside the measured s. Only second-line QA sampling remains.
  - No source measures a sampling rate, so v2's range (0.03–0.30) is kept unchanged, applied to AI-handled cases. **This parameter is still unsourced.**
- **Task framing: r ~ triangular(0.10, 0.20, 0.40).**
  - 0.10: share of true AML positives missed if triage auto-closes (E15).
  - 0.15: meeting notes not rated good (E06).
  - 0.17–0.33: legal RAG hallucination rate (E13).
  - 0.19: correctness penalty outside the AI frontier (E03).
  - The upper bound of 0.40 is inference. E01's 62% non-acceptance of suggestions shows rework can be higher, but in E01 that rework is already inside measured time.
- **Compliance stress (CAL_COMPLIANCE_FULL):** r = 1 for P01 KYC, P07 due diligence, P08 benefit review and P14 AML, so every AI-handled case is re-reviewed.
  - Basis: E16 finds only 2% of financial-firm AI use cases fully autonomous.
  - E17 and E19 suggest that confidence-gated routing is the cheaper design actually used. So this is an upper-cost bound, not the expected case.

### 3.3 a_p, AI amenability

- **a_p ~ triangular(0.5a₁, a₁, min(0.60, a₁ + 0.20)).**
  - v2 used min(0.9, a₁ + 0.35).
  - The cap follows E10: 47–56% of tasks with LLM-based tooling, 15% with an LLM alone.
- The cost-weighted mean a across P01–P15 moves from 0.43 (v2) to 0.37. That sits inside E10's 0.15–0.56.
- Customer support in E01 ran the assistant on effectively all chats, so P11 may be under-capped. ATTR_A_ONLY bounds this effect.

### 3.4 Combined check

Under each scenario, the implied share of the P01–P15 pool saved, Σs·a·L / ΣL, is compared with the whole-job field measures (large-national archetype) [S]:

| Scenario | p05 | p50 | p95 | Evidence band [F] |
|---|---:|---:|---:|---|
| V2_BASELINE | 0.096 | **0.174** | 0.268 | — |
| CAL_FIELD_INLOOP | 0.016 | 0.050 | 0.092 | Whole job 0.03–0.054 (E08, E09); customer-support deployment 0.09–0.13 (E01, E02) |
| CAL_TASK_REVIEW | 0.061 | 0.116 | 0.181 | Task experiments 0.25–0.40 × a |
| CAL_CENTRAL | 0.022 | **0.079** | 0.167 | — |

v2's median sits above even the dedicated customer-support deployment. In that deployment a is close to 1.

---

## 4. Results

All scenarios use the same uniform draws as v2 (common random numbers). Sponsor bootstraps, fixed costs, α, β, b, d, φ, touch rates and minutes are identical draw by draw. V2_BASELINE reproduces v2 exactly: the maximum difference in P(first, gross) is 0 (`record_type=meta`).

### 4.1 Ranking (`record_type=process`, `compare_baseline`) [S]

Large national. Mean over P01–P15 of P(rank first):

| Scenario | Gross A / B / C / D | Net A / B / C / D / none |
|---|---|---|
| V2_BASELINE | .064 / .293 / **.029** / .614 | .390 / .100 / **.014** / .089 / .408 |
| CAL_FIELD_INLOOP | .073 / .297 / **.000** / .630 | .399 / .103 / **.000** / .091 / .408 |
| CAL_TASK_REVIEW | .071 / .296 / **.004** / .628 | .397 / .102 / **.002** / .091 / .408 |
| CAL_CENTRAL | .072 / .297 / **.002** / .629 | .398 / .102 / **.001** / .091 / .408 |
| ATTR_SQ_ONLY (s, q calibrated; a as v2) | .071 / .296 / .005 / .628 | .397 / .102 / .002 / .091 / .408 |
| ATTR_A_ONLY (a calibrated; s, q as v2) | .068 / .295 / .013 / .624 | .395 / .101 / .006 / .090 / .408 |

Modal winners at a large national are unchanged in every scenario:
- Gross: P01–P15 = B D A B D D D D D D D B D B D.
- Net: A for P03, P05, P07–P11, P13 and P14; "none" for the rest.

C's probability of ranking first, and of clearing its fixed cost, in the processes where it mattered (large national):

| Process | v2: P(C first gross) / P(C net > 0) | CAL_FIELD | CAL_TASK | CAL_CENTRAL | CAL_COMPLIANCE_FULL |
|---|---|---|---|---|---|
| P03 complex assets | .151 / .182 | .000 / .013 | .032 / .111 | .016 / .062 | .032 / .111 |
| P07 non-standard due diligence | .160 / .586 | .000 / .154 | .026 / .453 | .013 / .307 | .000 / .000 |
| P11 service inquiries | .029 / .292 | .000 / .033 | .001 / .177 | .001 / .105 | .001 / .177 |
| P14 AML alerts | .040 / .045 | .000 / .002 | .002 / .020 | .001 / .010 | .000 / .000 |
| P16 recipient attribution (unanchored) | .016 / .317 | .000 / .030 | .000 / .186 | .000 / .104 | .000 / .186 |

- At mid nationals and all community-foundation archetypes, C clears its fixed cost in **at most 1.5%** of draws in any process under any calibrated scenario. The maximum is P07 at a $1bn community foundation under CAL_TASK_REVIEW. v2 had at most 5.1%.
- At community foundations under $250m, "none" remains the modal net winner in every process.

### 4.2 Value pool (`record_type=archetype`) [S]

Median sponsor AI gross value, AI on the existing workflow:

| Scenario | NAT_LARGE | NAT_MID | CF_1BN | CF_250M | CF_SMALL |
|---|---:|---:|---:|---:|---:|
| V2_BASELINE | $1,177k | $131k | $164k | $42.0k | $5.85k |
| CAL_FIELD_INLOOP | $202k | $21.9k | $34.6k | $8.9k | $1.16k |
| CAL_TASK_REVIEW | $793k | $92.4k | $115.5k | $29.9k | $4.20k |
| **CAL_CENTRAL** | **$445k** | **$49.2k** | **$69.4k** | **$17.8k** | **$2.40k** |
| CAL_COMPLIANCE_FULL | $386k | $43.5k | $53.9k | $14.1k | $1.97k |
| ATTR_SQ_ONLY | $526k | $57.2k | $80.5k | $20.5k | $2.76k |
| ATTR_A_ONLY | $874k | $96.4k | $125.5k | $32.6k | $4.48k |

- After redesign, CAL_CENTRAL at a large national is $323k, against $854k in v2.
- **Attribution:**
  - Calibrating a alone cuts the pool by about 26%.
  - Calibrating s and q, including the move of q to AI-handled cases, cuts it by about 55%.
  - Together the cut is about 62%. The s and q calibration dominates.

**v2b (`model=V2B_UNIFORM`, `V2B_BOTTOMUP`).**
- The proportional cut carries through.
- V2B_UNIFORM at a large national falls from $1.18m to $448k.
- V2B_BOTTOMUP falls from $1.42m to $551k at a large national, from $6.4k to $2.3k at a $1bn community foundation, and from $1.3k to $0.45k at $250m.
- No modal winner changes in either variant.

### 4.3 Platform and network break-even [S]

**Homogeneous network.** The table shows P(break-even finite), the median N of sponsors among finite draws, and P(N ≤ sponsors available):

| Scenario | NAT_LARGE (5 available) | CF_1BN (20) | CF_250M (58) |
|---|---|---|---|
| V2_BASELINE | .95 / 8 / .34 | .66 / 59 / .12 | .24 / 236 / .02 |
| CAL_CENTRAL | .77 / 17 / .13 | .40 / 104 / .03 | .09 / 349 / .004 |
| CAL_FIELD_INLOOP | .62 / 30 / .04 | .24 / 164 / .005 | .03 / 600 / .000 |
| CAL_TASK_REVIEW | .92 / 12 / .22 | .56 / 85 / .06 | .15 / 305 / .007 |

**Observed FY2024 population**, with the vendor signing the most valuable sponsors first. The table shows P(reachable) for AI on the workflow:

| Segment | V2 | CAL_CENTRAL | CAL_FIELD | CAL_TASK |
|---|---:|---:|---:|---:|
| Community foundations under $250m | .004 | .000 | .000 | .000 |
| All community foundations | .160 | .036 | .004 | .072 |
| Nationals under $10bn | .035 | .001 | .000 | .005 |
| Community foundations plus nationals under $10bn | .263 | .066 | .011 | .119 |
| Community foundations plus all nationals | .433 | .165 | .043 | .264 |

### 4.4 Sensitivity (`record_type=sensitivity`, large national, CAL_CENTRAL) [S]

Rows are terciles of each parameter's calibrated range.

| Parameter tercile | AI value p50 (low / mid / high) | Share of (draw, process) where C > 0 net (low / high) |
|---|---|---|
| s | $124k / $463k / $878k | .013 / .067 |
| q | $612k / $444k / $280k | .051 / .028 |
| a_p | — | .026 / .051 |
| Framing (field / task) | $205k / $790k | — |

- s is the lever that matters, and its range is set mainly by **which kind of evidence is believed**: production field studies or task experiments.
- Even in the top tercile of s, C clears its fixed cost in under 7% of process-draws.

---

## 5. Which conclusions change

| Earlier conclusion | Status after calibration |
|---|---|
| v2: gross ranking from v1 survives; C weak | **Strengthened.** C's chance of ranking first falls about tenfold. No modal winner changes |
| v2: C competes only in P03, P07 and P11 at large nationals | **Narrowed.** Only P07 keeps a material chance of clearing fixed cost (.31 central). In compliance-review conditions P07 never does |
| v2: platform needs about 8 large-national equivalents | **Weakened.** About 17 needed against 5 available; P(≤ available) falls from .34 to .13 |
| Synthesis B / top-10 #10: operations-AI value pool thin | **Strengthened.** The value pool is roughly 40% of v2's (field to task framing: 17–67%) |
| Red team: rankings follow the assumptions | **Refined.** Rankings are robust to evidence-bounded s, q and a. Value size and break-even are not |

---

## 6. Limitations

1. **Cross-industry transfer [I].** No source is a DAF or philanthropic back office. The closest analogues are E01 (service inquiries), E13 (rule interpretation), E15 (AML alert triage, which is ML rather than gen-AI) and E17 (bookkeeping).
2. **Self-report.**
   - E06–E09 rest on self-reported time.
   - E11 shows self-reports can have the wrong sign. Developers believed AI saved 20% when it cost 19%.
3. **Technology vintage.** Most measurements use 2023–24 models. Newer agentic tools could raise s or lower r. No 2025–26 field study of agentic back-office work with stated denominators was found.
4. **The re-review basis is a modelling choice, not a measurement.**
   - Charging error rates to all touched cases instead of AI-handled cases cuts the large-national pool to $110k (ALT_Q_ON_ALL_TOUCHED).
   - Charging v2's q that way alongside field s cuts it to $0 (ALT_FIELD_Q_TOUCHED).
   - Second-line QA sampling rates remain **unsourced**.
5. **Structure unchanged.**
   - The C formula treats AI as an assistant on every amenable case.
   - E19 and E17 indicate that routing (AI-only on high-confidence cases, human-only otherwise) can beat assistance. The model does not represent routing. That probably understates C where confidence scores are informative.
6. **Other assumptions untouched.** φ, d, the fixed costs and τ still drive net results and platform break-even more than s, q and a do.
7. **Discovery was cut short** (§2.1). OpenAlex search was unavailable, SSRN blocked access, and Crossref's robots.txt could not be read. Evidence for KYC onboarding, AP processing and grant review is therefore thin or missing. It is not shown to be absent.
