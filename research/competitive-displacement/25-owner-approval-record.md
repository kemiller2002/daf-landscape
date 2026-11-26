# 25 - Owner approval record (2026-11-26)

Status: record of an owner decision, added after Phase II merged (PR #92, `10b92f4`). The original proposals in [23](23-executive-decision-register.md) and [decisions.csv](data/registers/decisions.csv) are unchanged and remain the historical record of what research recommended.

## What the owner approved

On 2026-11-26 the owner approved all twelve proposed decisions, DEC-001 to DEC-012, and authorized the progression of all eighteen cross-repository implications, XRI-001 to XRI-018, subject to their documented conditions. The owner's wording for each decision, with its conditions, is in [decision-approvals.csv](data/registers/decision-approvals.csv).

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
