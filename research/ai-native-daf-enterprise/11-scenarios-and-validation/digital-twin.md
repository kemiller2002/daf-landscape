# Enterprise digital twin

**Code:** [`../models/Daf.Enterprise/Twin.fs`](../models/Daf.Enterprise/Twin.fs).
**Outputs:** [`outputs/twin-100k.csv`](outputs/twin-100k.csv) and [`outputs/twin-10k.csv`](outputs/twin-10k.csv).
**Tests:** determinism, work conservation, the volume-stress effect, the custodian-outage liquidity effect, and provenance labeling.

## 1. What it is and is not

The twin is an executable model of the enterprise's *human* work queues and its liquidity buffer. Its inputs are:
- capacity, taken from the staffing model;
- arrivals, taken from the volume drivers in [`../09-financial-models/`](../09-financial-models/).

It simulates 365 days with a seeded pseudo-random multiplier. Same seed, same result (tested). Deterministic work is not simulated: it has no human queue and adds no human time.

**It is not a measurement.** Every output carries `Provenance = "SIMULATED on assumed parameters"` (tested), as addendum §23 requires: the twin "should support decision-making, not create an illusion of certainty". It becomes a measured twin when telemetry (C6.2) replaces the assumed arrival rates and handling times. The design keeps both labels: each parameter is tagged *measured* or *assumed*, and reports show which.

## 2. Model

| Queue | Arrivals per day | Capacity per day | SLA (days) [A] |
|---|---|---|---|
| Grant exceptions | grants/365 × exception rate × surge × noise | grants-compliance FTE × 6.4 h ÷ 0.75 h | 2 |
| Complex-asset acceptance | contributions/365 × complex share × noise | specialist FTE × 6.4 h ÷ 12 h | 10 |
| Service recovery | accounts × 0.3/365 | service FTE × 6.4 h ÷ 0.33 h | 1 |
| Reconciliation breaks | (grants + contributions)/365 × 1% × surge (×3 during custodian outage) | (finance FTE − 1 controller) × 6.4 h ÷ 0.33 h | 3 |

**Liquidity:**
- The cash buffer starts at 2% of AUM [A].
- Daily grant outflow is 25% of AUM per year (about the FY2024 aggregate payout of 25.9%, EV-014) × surge.
- Liquidations normally refill the buffer. During a custodian outage they do not.

The year-end surge runs from day 330 to day 365 at ×3 [A]. The repository documents December concentration qualitatively but has no daily series.

## 3. Results at 100,000 accounts (seed 42)

| Stress | Grant-exception days over SLA | Max exception backlog | Complex-asset days over SLA | Recon days over SLA | Min liquidity buffer (days of outflow) | Buffer exhausted |
|---|---|---|---|---|---|---|
| Baseline (surge only) | **34** | 9,662 | 0 | 29 | 29.2 | no |
| Grant volume ×10 | 365 | 673,672 | 0 | 365 | 2.9 | no |
| Complex-asset gifts ×2 | 34 | 9,662 | **336** | 29 | 29.2 | no |
| Custodian outage, 5 business days, in surge | 34 | 9,662 | 0 | 29 | 8.8 | no |
| Custodian outage, 30 days, in surge | 34 | 9,662 | 0 | 30 | **−61.5** | **yes** |
| Manual reviews halved (exception rate ×0.5) | **0** | 471 | 0 | 29 | 29.2 | no |
| New regulation doubles exceptions | 359 | 59,982 | 0 | 29 | 29.2 | no |
| Staff capacity −40% | 346 | 20,647 | 286 | 33 | 29.2 | no |

## 4. What the twin teaches the design (and where it changed the design)

1. **The year-end surge, not the annual average, sizes the human organization.** A grants-compliance pool sized for average load breaches its two-day SLA for 34 days in December. *Design change:* the organization model gets a surge mechanism instead of permanent headcount. The options are cross-trained specialists from other pools, a pre-contracted reviewer bench, and pre-clearing known recipients ahead of December (determination reuse). The cost model is unchanged, but the [scenario register](scenarios.md) SC-07 (volume surge) relies on this.
2. **Human capacity scales linearly with exceptions; automation does not rescue a policy that creates exceptions.** A tenfold volume shock, or a regulation that doubles exceptions, swamps the queue. Halving the exception rate eliminates the surge breach entirely. *Design implication:* the highest-value improvement work targets the exception rate, through determination reuse, better recipient data and narrower rules. That is the improvement engine's "eliminate work before accelerating it" ordering ([`../08-governance-and-compliance/continuous-improvement-system.md`](../08-governance-and-compliance/continuous-improvement-system.md)).
3. **A single complex-asset specialist is a concentration risk.** Doubling complex gifts produces 336 days over SLA. *Design change:* at below about 50k accounts, complex-asset acceptance should be partnered with a non-cash processor, keeping the accept/decline authority in-house. This is recorded in the [SPOF register](scenarios.md).
4. **Liquidity under a custodian outage is the most dangerous stress.** A 5-business-day outage leaves 8.8 days of buffer. A 30-day outage during the December surge exhausts a 2% buffer. *Design change:*
   - a liquidity policy parameter, the buffer ≥ 30 days of peak outflow, approved by the investment committee, so the buffer rises seasonally;
   - a second custodian for cash sweeps, or a bank line;
   - the outage runbook pauses non-urgent grants first. The payment gate's daily caps already allow this without code changes.
5. **Reduced manual review is safe for capacity but not automatically safe for risk.** The twin shows the capacity benefit only. Whether halving reviews increases escaped errors is a risk question the twin cannot answer without the measured error baseline (GAP-004). So the change-control rule stands: loosening a control requires a back-test plus human approval ([control framework](../08-governance-and-compliance/control-framework.md)).

## 5. Questions the twin answers now, and those it cannot yet

| Addendum §23 question | Answered? | How |
|---|---|---|
| What happens if grant volume increases tenfold? | Yes [S] | Stress "grant volume ×10" |
| How many specialists if complex gifts double? | Yes [S] | Rerun with a capacity multiplier until days over SLA reach 0. The required complex-asset FTE roughly doubles, because work is linear in arrivals |
| What happens when a major custodian becomes unavailable? | Yes [S] | Outage stresses |
| How would a regulatory change affect workflows? | Partly | Exception-rate stress. Policy back-testing in the PoC (`Policy.decide` is pure and replayable) shows *which* grants a rule change would refer |
| Which bottleneck limits account growth? | Yes [S] | Grants compliance and complex assets, both linear in volume |
| What is the effect of reducing manual reviews? | Capacity yes; risk no | Needs GAP-004 |
| Where does automation create new concentration risks? | Qualitatively | Twin plus [SPOF register](scenarios.md). Concentration in the policy engine, the payment gate and the eligibility data feed is structural, not a queue effect |

## 6. Path to a measured twin

1. Emit `ExceptionCaseOpened` and `ExceptionCaseResolved` with timestamps and handling time (already in the event catalog).
2. Compute arrival rates and handling-time distributions per queue from those events.
3. Replace assumed parameters one at a time, keeping the label per parameter.
4. Back-test the twin: predict last month's backlog from last month's arrivals, and compare.
5. Only after the back-test error is acceptable (target set by the COO and CRCO) is the twin used for staffing decisions without a human sanity review.
