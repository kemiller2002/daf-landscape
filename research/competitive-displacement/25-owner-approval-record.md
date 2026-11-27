# 25 - Owner approval record (2026-11-26)

Status: record of an owner decision, added after Phase II merged (PR #92, `10b92f4`). The original proposals in [23](23-executive-decision-register.md) and [decisions.csv](data/registers/decisions.csv) are unchanged and remain the historical record of what research recommended.

## What the owner approved

On 2026-11-26 the owner approved all twelve proposed decisions, DEC-001 to DEC-012, and authorized the progression of all eighteen cross-repository implications, XRI-001 to XRI-018, subject to their documented conditions. Each decision's approved direction and its conditions in the owner's wording (`owner_conditions`) are in [decision-approvals.csv](data/registers/decision-approvals.csv). Constraints that agents derived from the Phase II reports or the repositories are kept apart, in `derived_constraints`, with their source; they are not owner wording. The outcome measures, review cadences and reconsideration triggers are agent proposals awaiting owner acceptance (`measures_status`).

**The approval authorizes** strategic direction, requirements refinement, research and planning.

**It does not authorize** expenditure, contractual commitments, production deployment, removal of mandatory controls, or unsupported legal conclusions.

The owner changed or tightened the research recommendations in four places:

| Decision | Research recommendation (report 23) | Approved direction |
|---|---|---|
| DEC-002 | Form a custodial administrator only behind a signed $0.5-1.0B anchor | Same, and the threshold is an **approved conditional planning assumption**, not an established market requirement |
| DEC-003 | Replace the 180-day full re-review policy with change-driven re-vetting and expiry | Change-driven re-vetting, but the owner's **180-day validity policy is preserved**: eligibility must stay current within 180 days unless a later explicit decision changes that |
| DEC-007 | Cluster first migrations on one source, e.g. NPact/FIMS or iPhi community foundations | One source **where commercially practical**, and **no incumbent selected without supporting evidence** (the examples are not a selection) |
| DEC-008 | Fund G0 ($0.15-0.35M), then a G1 pilot ($1.0-1.5M cumulative) | Staged, gated investment with kill rules; the **modelled amounts are not approved expenditures** and must be challenged and minimized |

## Status ladder

A decision moves through six distinct stages. Approval at one stage never implies a later one, and the validator rejects any row that marks a stage "yes" while an earlier stage is not.

1. **Strategically approved:** the owner accepted the direction.
2. **Requirements incorporated:** the responsible repositories' requirements reflect it.
3. **Evidence gate satisfied:** the named validation tests (V-1 to V-9) passed.
4. **Implementation authorized:** the owner authorized building or spending.
5. **Implemented**
6. **Validated**

| Decision | Strategically approved | Requirements incorporated | Evidence gate | Implementation authorized | Implemented | Validated |
|---|---|---|---|---|---|---|
| DEC-001 to DEC-012 | yes (2026-11-26) | see [decision-approvals.csv](data/registers/decision-approvals.csv) | no | no | no | no |

As of this record, no decision has passed an evidence gate: none of V-1 to V-9 has been run. No implementation is authorized.

## Cross-repository implications

Each implication's disposition, with the requirement or record it produced, is in [xri-dispositions.csv](data/registers/xri-dispositions.csv). The traceability matrix and the reconciliation narrative are in [26](26-cross-repository-dispositions.md).

## Validation

`dotnet run --project model/src/CompetitiveDisplacement -c Release -- validate .` checks these rules:

- every decision has exactly one approval row;
- every implication has a disposition from the eight allowed classes;
- every ladder value is one of yes, no, partial or pending;
- no stage is marked "yes" ahead of an earlier stage.

Unit tests: `dotnet test model/tests/CompetitiveDisplacement.Tests`.

## Later owner decisions (2026-11-26)

These decisions were made after the approval above, in response to questions Stage I raised. They are separate from DEC-001 to DEC-012.

| ID | Question raised | Owner's decision (owner's words) | Recorded in |
|---|---|---|---|
| OD-P3-01 | Who owns intellectual property the initiative creates? | "EF owns all property we make": Echelon Foundry owns all intellectual property created (Unbound, Transitus, shared components, research models) | echelon-organization-administration `strategy/daf-entry/02` as OD-DAF-IP-001 (owner's intent, not legal effect; assignment mechanics open for counsel) |
| OD-P3-02 | Does the DEC-008 kill rule pause Transitus beyond phase 1? (Transitus OD-TRN-P3-02) | "Kill rule doesn't stop Transitus" | Transitus decision records; [xri-dispositions.csv](data/registers/xri-dispositions.csv) XRI-014 |
| OD-P3-03 | When does the "no named partner by month 6" clock start? | "No named partner rule starts when we have significant expenses" | [decision-approvals.csv](data/registers/decision-approvals.csv) DEC-008; echelon-organization-administration `strategy/daf-entry/03` as OD-DAF-CAP-001 |

**OD-P3-04 (threshold for OD-P3-03).** In the owner's words: "Significant is when it becomes its own cost center." The kill-rule clock starts when DAF commercialization becomes its own cost center at Echelon Foundry, with its own budget and expense tracking. It is not tied to a dollar amount. Recorded in echelon-organization-administration as OD-DAF-CAP-002.

Transitus scope stays as DEC-011 sets it (phase 1, with vendor packages deferred). OD-P3-02 lifts a possible pause; it does not authorize expenditure or implementation.

## Owner directions of 2026-11-27 (ratification)

The owner posted directions on each Stage I pull request, headed "Owner direction relayed from the approved November 26 review", and confirmed them in the working session on 2026-11-27. Each direction ends: "Update authoritative records through normal governance, validate and merge only when required checks pass. No production implementation or expenditure authorized."

| ID | Repository / PR | Owner direction (summary; full text on the PR) |
|---|---|---|
| OD-P3-05 | daf-landscape #93 | Record owner approval of the recommendations in the latest review. Ratify proposed requirements subject to existing evidence gates. Zero-based economics is a separate first deliverable (completed Unbound; 1, 2, 5, 10 and 100 institutional customers; every expense justified by obligation, workload or capacity trigger; incremental cash, founder time, shared allocation, and mandatory, conditional and volume-triggered costs distinguished; prior estimates reconciled; reproducible F# models). Sensitive internal details stay in the private repository |
| OD-P3-06 | unbound #22 | Ratify the 30 proposed requirements; resolve OD-CDD-01..05 (see the next table); resolve the existing D9 failure before merge |
| OD-P3-07 | transitus #2 | Ratify the proposed requirement rows subject to existing gates; preserve exact monetary reconciliation and authorized data access; resolve the legal-basis and disclosure-threshold questions through evidence-based proposals, without inventing legal conclusions or waiving gates |
| OD-P3-08 | echelon-organization-administration #22 | Separate incremental cash from fully loaded shared-cost allocation; keep a machine-readable spend and founder-time ledger in the organization repository; defer a separate Unbound entity until there is a demonstrated need; start **both** commercialization clocks when DAF commercialization becomes its own cost center; ratify the capital rules; keep IP legal mechanics unresolved pending evidence |
| OD-P3-09 | echelon-foundry #13 | Ratify both draft standards; extend event-level costing with zero-based costing (every expense needs a justified obligation, workload or capacity trigger; incremental cash and fully loaded costs kept separate) |
| OD-P3-10 | praxis #314 | Ratify the three proposed decision lifecycle, currency and cross-repository propagation requirements |

**Unbound open decisions resolved by OD-P3-06:**

| ID | Resolution |
|---|---|
| OD-CDD-01 | Partner-first, with V-1 and V-6 retained |
| OD-CDD-02 | Change-driven renewal within the 180-day ceiling, with evidence freshness and targeted review |
| OD-CDD-03 | Model licensing and 20 bps independently |
| OD-CDD-04 | The anchor gate applies to full-service administration, not to limited support |
| OD-CDD-05 | Measure concentration at both the end-sponsor and partner levels |

**Effects on this register:**
- **DEC-008's month-24 pilot clock:** answered. It also starts at the cost-center month (OD-P3-08).
- **Ladder:** a decision moves to "requirements incorporated" only when its repository has ratified the requirements through its own governance and the change has merged. Evidence gates, implementation authorization, implementation and validation stay at "no".
- **The referenced review document:** "the latest review" is not held in these repositories. This record keeps the owner's wording as posted rather than restating that review.
- **Still open:** who performs the 180-day deep review (Phase III P3-DEC-MOD005). OD-CDD-02 does not decide it.
