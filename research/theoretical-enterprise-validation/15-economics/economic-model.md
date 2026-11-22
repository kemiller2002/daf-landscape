# Economic model: assumptions, surge, failure costs, sensitivity

**Status:** assumption-driven analytical model. Closed-form arithmetic only; nothing was simulated or executed. **No operational measurement exists for any parameter below.** Labels: [A] assumption, [S] scenario, [V] sourced, with the source named. Baseline: [financial and staffing models](../ai-native-daf-enterprise/09-financial-models/financial-and-staffing-models.md) and its parameter register.

## 1. Why a second model

The baseline staffing model computes FTE from **annual average** volume (09 l.22). The same executive report says "the December surge, not the average, sizes the human organization" (TVC-017). The baseline also does not model:
- correlated failure;
- incident cost;
- multi-step agentic inference cost (acknowledged in AC-13 but not modelled).

This model adds those terms analytically. Its parameters reuse the baseline's where they exist, so the two models can be compared.

## 2. Exception specialist demand

Let:
- *A* = accounts;
- *g* = grants per account per year;
- *e* = share of grants needing human decision;
- *m* = minutes per exception;
- *H* = productive hours per FTE per year.

**FTE_avg = A · g · e · m / (60 · H)**

The elasticity is 1 in each of *A, g, e, m*, and −1 in *H*. Every parameter matters equally at the margin. The **ranges** are what differ.

| Parameter | Low | Expected | High | Source of range |
|---|---|---|---|---|
| g (grants/account/yr) | 6.2 | 8 | 13.0 | [V] observed RCF to Fidelity range, baseline 09 l.18 |
| e (exception share) | 2.8% | 8% | 17% | Low corrected in review: 4.2% is a **dollar** share; the per-grant figure is 2.8% [S]. 7–8.5% core proxy [S]. 17% is outside the baseline's own 3–15% falsification band; the broad proxy is "likely 28–31%" [S]. None is observed review. |
| m (minutes per exception) | 30 | 45 | 135 | 45 [A] baseline; 135 from FM-15 "real" alternative [A] |
| H (productive hours) | 1,600 | 1,600 | 1,400 | [A] |
| Loaded cost per FTE | $124.5k | $165k | $250k | $124,507 Vanguard comparator [V per baseline]; others [A] |

At A = 100,000 (g = 8, H = 1,600 unless noted):

| Case | Exceptions/yr | Hours | FTE_avg | Cost | Per account |
|---|---|---|---|---|---|
| Low (e 2.8%, m 30) | 22,400 | 11,200 | 7.0 | $0.87m | $9 |
| Expected (e 8%, m 45) | 64,000 | 48,000 | **30** (matches baseline) | $4.95m | $50 |
| High (e 17%, m 135, H 1,400, $250k) | 136,000 | 306,000 | 219 | $54.6m | $546 |

Replacing the baseline's $50 per account exception cost with the high case gives 272 − 50 + 546 ≈ **$768 per account** [S]. That is close to, but still below, the Fidelity-derived frontier of ~$790. **Corrected in review:** the AI-native cost advantage *approaches parity* in the high case; it does not disappear.

Per-account exception cost = 8 · e · m / (60 · H) · C. Holding everything else at baseline, the frontier is reached when:
- **e·m ≈ 24** (e as a fraction, m in minutes) under pessimistic labour (H = 1,400, C = $250k);
- **e·m ≈ 41** under base labour.

Two further caveats:
- The high case combines four extremes, so it is a stress test, not a range end.
- Its m = 135 is FM-15's 3× stress multiplier. The only evidence is EV-106 (90 minutes unaided), which gives ~$587 per account.

**Not modelled, in either direction:**
- Pessimistic labour cost applied to *all* staff, not only exceptions. That gives ~$842 and crosses the frontier.
- Grant intensity. Fidelity runs ~13 grants per account against 8 here; per grant, the high case (~$96) is already worse than Fidelity (~$61).
- Determination reuse, which biases every case upward.

## 3. Surge amplification (missing from the baseline staffing model)

Assume December carries a multiplier *k* on daily arrivals for 25 of 250 working days.
- Base daily rate = N / (225 + 25k).
- Peak-to-average ratio = **250k / (225 + 25k)**.

| k | Peak/average | Expected-case peak FTE (no deferral) | High-case peak FTE |
|---|---|---|---|
| 2 | 1.82 | 55 | 398 |
| 3 (twin's value [A]) | 2.50 | 75 | 548 |
| 5 | 3.57 | 107 | 782 |

**Backlog if staffed at the annual average** (k = 3, expected case):
- arrivals during the surge are 640 per day against capacity of 256 per day;
- the backlog grows by ~384 per day;
- after 25 days it is ~9,600 cases.
- After December the surplus capacity is only 256 − 213 ≈ 43 per day, so clearance takes **~223 working days**. That is most of the following year. **Corrected in review:** an earlier draft said "37 days", which is the backlog expressed in days of capacity, not the time to clear it.
- Staffing at the annual average means 100% utilisation: any variation in arrivals makes the backlog permanent.
- Staffing to a **service level** instead [S]: ~54 FTE clears the surge within ~10 days; ~63 FTE within ~5 days. These are review-derived figures.

The twin reports "34 days over SLA" [S]. This agreement is **not corroboration**: both use the same assumed k = 3 (TVA-004). The mechanism is arithmetic. The baseline *staffing table* does not include it. The complex-asset specialist pool, also December-heavy, has no surge term in either model.

**Levers ranked by effect on peak FTE** (expected case, k = 3):

| Lever | Effect | Evidence |
|---|---|---|
| Halve *e* (better routine coverage, reuse of determinations) | 75 → 38 | Baseline twin agrees; GAP-001/034 |
| Giving plan moves *p* share of December exceptions to Q3 | 75 → 75(1 − p) + spread | *p* unmeasured (TVA-030) |
| Deferral windows | E6: 35 → 25 [X] | Donor acceptance untested (INN-37) |
| Seasonal specialists | Linear | Supply of legally competent reviewers unmeasured |
| Halve *m* (better evidence packages) | 75 → 38 | Automation-bias risk (FM-04) |

The tech architecture's "10–30× peaks" (TVC-017) refers to throughput per second, not daily volume [I]. It affects infrastructure, not staffing.

## 4. AI inference

Baseline: $0.90 per exception dossier, $0.05 per service interaction. At 100k accounts, $78k per year (0.3% of cost).

**Break-even of significance (exception dossiers).** AI cost reaches 1% of total cost ($272k at 100k accounts) when the per-dossier cost × 64k ≈ $250k, i.e. ≈ **$4 per dossier**. The human cost it supports is about 45 min × $55–103/h ≈ **$42–77**. The labour-rate range is unreconciled: GAP-040; the baseline uses $55.45/h elsewhere.

**Corrected in review:** the benefit-risk agent runs on **all ~800k grants**, not only exceptions. For routine runs, the 1% threshold is ≈ **$0.31 per run**. Per-grant agents are where inference cost becomes material first.

Multi-step agentic runs (retrieval, many tool calls, long context) plausibly cost single-digit dollars per case [A]. Such costs would be material but not decisive. The model choice for agents should therefore be driven by error rates, not by price. AC-13 holds in this range, with the caveat that agent **re-runs** (on every eligibility or list refresh, if done by agent instead of D) multiply run counts. Requirement TVR-ECON-002: list refreshes are re-evaluated by deterministic rules, never by agents.

## 5. Correlated failure and incident cost (not in the baseline model)

Routine grant dollar flow at 100k accounts ≈ 800k grants × $5k [S; the $4.5–6k average is V per baseline] ≈ **$4bn per year ≈ $16m per business day**.

**Policy misconfiguration (FM-01).** A misconfiguration approves a fraction *f* of routine grants that should have been referred, for *D* business days before detection:
- exposure ≈ $16m × *f* × *D*;
- at *f* = 1%, *D* = 5 → $0.8m of grants needing post-payment review (~160 grants at $5k);
- if a share of them are taxable distributions, §4966 imposes 20% on the sponsor and 5% on approving managers (REG-001 [F]), plus recovery and reputational cost.

**Shared policy pack across *s* sponsors (Model C/D, INN-36).** Exposure scales by *s* while detection time does not shrink. This is the correlated-error term absent from the Model C economics (TVF-062).

**§4966 manager tax.** It is capped per distribution (reviewers cite $10,000 [unverified, check statute]). The sponsor-level 20% tax is the dominant term.

**Sanctions miss.** Strict liability (REG-036). Cost is not reducible to a per-case multiple; the baseline bounds escaped-error cost at 1.0–88.5× handling time, and a sanctions miss near 128×.

**Incident cost formula (proposed):**
`E[annual incident cost] = Σ_i p_i · (direct loss_i + remediation hours_i · rate + penalty_i + recovery cost_i)`.

No *p_i* is known. The requirement is to **measure** rather than assume (TVR-ECON-003): record, for every post-payment review case, the hours and recovery outcome, from the first pilot.

## 6. Other volume-dependent costs at 10× (1m accounts)

| Item | Scaling | Concern |
|---|---|---|
| Reconciliation breaks | volume × break rate (0.01 [A]) × 20 min [A] | 10m tx → 100k breaks → ~21 FTE. Break rate is unmeasured (GAP-005). |
| Provider rate limits | Peak submissions per second | Unknown per provider (DD-020 rubric) |
| Unknown-state cases | Submissions × timeout rate | Each Unknown needs PA-2 handling; no provider timeout rates measured |
| Contact volume | Accounts × contact rate | GAP-006; proactive status (alt 6C) is the lever |
| Over-commitment cases in a drawdown | Funds near full reservation × drawdown depth | Proportional to recommendation intensity in a falling market; unmeasured |

## 7. Cash sleeve cost (alternative 1D)

Cash drag ≈ sleeve share × (expected pool return − cash yield). At 5% × 2% = **10 bps of AUM** [A]: ~$300 per account per year at a $300k average balance, borne by **funds**, not the sponsor. That is ~20× the modelled custody cost (0.5 bps). A sleeve sized to 90 days of forecast grants still costs ~$197 per account [S, review-derived].

**Corrected in review:** an earlier draft called this "comparable" to sponsor costs, which compared costs borne by different parties. The sleeve's justification would be correctness and simplicity, not cost. The architecture review disputes even that: a sleeve plus currency reservation keeps every reservation state, and the sleeve runs out in December. See [alternatives §1](../14-alternative-operating-models/alternatives.md).

## 8. Sensitivity summary

| Conclusion | Robust? | Flips when |
|---|---|---|
| AI inference cost is immaterial | Yes, below ~$4 per dossier | Agents re-run on every refresh, or per-case cost > ~$10 |
| AI-native cost per account beats the conventional frontier at ≥100k accounts | Narrowly, in the modelled high case (~$768 vs ~$790) | e·m ≥ ~24 (pessimistic labour) or ~41 (base labour); or pessimistic labour applied to all staff; or comparing per grant |
| Average-volume staffing is adequate | **No** | Always: k ≥ 2 creates backlog unless levers apply |
| Specialist pool is the binding human constraint | Yes, across all cases | — |
| Correlated failure is a material cost for multi-sponsor models | Probably [I] | Blast-radius analysis shows small *f·D·s* |
