# 01 - Approved strategic baseline

Status: research (2026-11-26). This report sets out the decision baseline that Phase III starts from. It distinguishes what the owner has approved from what research proposes. Every Phase III finding is read against this baseline, not against the original Phase II proposals.

## 1. Approved decisions (owner, 2026-11-26)

The owner approved all twelve Phase II decisions as **strategic direction only**. The approval does not authorize expenditure, contractual commitments, production deployment, removal of mandatory controls, or unsupported legal conclusions. The full record is Phase II report 25 and `decision-approvals.csv`, both under `research/competitive-displacement/` and added in PR #93.

| Decision | Approved direction | Owner conditions that bind Phase III |
|---|---|---|
| DEC-001 | Partner-first entry through a module or capability inside a channel partner's offering, followed by licensing | OD-M-05 (Unbound's ratified entry segment) stays a possible long-term destination; V-1 and V-6 preserved |
| DEC-002 | No custodial administrator as the initial commercial vehicle | The $0.5-1.0B anchor is a conditional planning assumption, not a market fact |
| DEC-003 | Change-driven re-vetting, evidence expiry and targeted re-vetting | Eligibility stays current within the **180-day validity policy**; investigate sample audits; V-3 and V-9 preserved |
| DEC-004 | No non-redistributable data in shared or resold layers | Source-specific rights and provenance enforced |
| DEC-005 | AI and inferred records are advisory | They never silently become authoritative |
| DEC-006 | Licensing or subscription before asset-based fees | V-2 preserved |
| DEC-007 | Concentrate early migrations on one incumbent source | Where commercially practical; V-5 preserved; no arbitrary selection |
| DEC-008 | Staged, gated investment with termination criteria | **Modelled amounts are not approved expenditures**; Phase III must challenge and minimize them |
| DEC-009 | No proprietary charity payment network | Charities need no account merely to receive payments |
| DEC-010 | Process SLAs only after successful rehearsals and validation | V-4 and contract review preserved |
| DEC-011 | Transitus scope discipline | Public-specification and canonical capabilities; vendor packages deferred until authorized data exists |
| DEC-012 | Adopt the validation plan and its gates | Develop lower-cost ways to satisfy them |

**Status ladder.** Every decision is at "strategically approved". None is at "requirements incorporated": the requirements Stage I wrote are proposals awaiting ratification. None has passed an evidence gate, because no validation test (V-1..V-9) has run. None is authorized for implementation.

## 2. Later owner decisions (2026-11-26)

| ID | Owner's words | Effect on Phase III |
|---|---|---|
| OD-P3-01 | "EF owns all property we make" | Unbound, Transitus, components and models are Echelon Foundry assets. A future servicing entity would license, not own (economic entity 4 in the organization record) |
| OD-P3-02 | "Kill rule doesn't stop Transitus" | Transitus spend is outside the kill rule in every sequence model ([14](14-commercial-sequencing.md)) |
| OD-P3-03 | "No named partner rule starts when we have significant expenses" | The kill-rule clock does not start at approval |
| OD-P3-04 | "Significant is when it becomes its own cost center" | The clock starts in the month DAF commercialization becomes its own cost center. The model treats that month as a parameter (P3-DEC-MOD001) |

**Still open for the owner:** whether OD-P3-03/04 also start the month-24 "referenceable live pilot" clock (organization record CAP-DAF-001).

## 3. Requirements state after Stage I

| Repository | State (all proposed, none ratified) | Source |
|---|---|---|
| Unbound | 30 UNB-CDD requirements; OD-CDD-01..05 open | `requirements/discovery/2026-11-26-competitive-displacement-decisions/` (unbound PR #22) |
| Transitus | DF-TRN-2026-0022..0026; 19 requirements including the pre-contract assessment tiers | transitus PR #2 |
| Organization | Approved direction; five economic entities; CAP-DAF-001/002 | `strategy/daf-entry/` (echelon-organization-administration PR #22) |
| echelon-foundry | Draft standards for event-level costing and reproducible F# models | echelon-foundry PR #13 |
| Praxis | RQ-ROS-2026-6C17, 0863, 6D60 (domain-agnostic) | praxis PR #314 |

Phase III uses these as the requirements baseline. It does not rely on any superseded requirement.

- **Transitus DF-TRN-2026-0014** is superseded by DF-TRN-2026-0019.
- **The Transitus DF-0016 kill criterion** has no successor that gates phase 1. OD-P3-02 makes that moot.
- **Unbound's ratified entry route (CNV-ECO-004)** still governs until OD-CDD-01 is decided. Phase III therefore treats partner-first as the approved strategy and OD-M-05 as the ratified long-term destination.

## 4. Phase II conclusions checked for supersession

daf-landscape `main` has no commits after PR #92 (`10b92f4`). No later change supersedes Phase II's conclusions. Phase III re-examines them as the owner asked:

| Phase II premise | Phase III treatment |
|---|---|
| Public charity data is not a moat | Re-tested: [07](07-architectural-competitive-advantages.md), [11](11-continuous-charity-intelligence.md) |
| Distribution and relationships are the binding barrier | Re-tested: [06](06-customer-acquisition-without-displacement.md), [12](12-institutional-distribution.md), [13](13-incumbent-response-model.md) |
| AI is about 6% of the modelled saving | Re-tested with work categories: [10](10-structural-cost-elimination.md) |
| Full administration needs about $1.9-2.3B in assets | Kept as context; Phase III models licensing and existing-Unbound states: [02](02-existing-unbound-economics.md), [14](14-commercial-sequencing.md) |
| Capital about $6.5M (P50) to a self-sustaining niche | Reconstructed line by line, with double counts found: [03](03-capital-requirements-reconstruction.md) |
| G0 $0.15-0.35M; G1 $1.0-1.5M cumulative | Challenged: [04](04-low-cost-commercial-validation.md) |

## 5. Separation of economic entities

Organization record 02 separates five entities:

1. Echelon Foundry as the technology creator.
2. Unbound as a product.
3. A customer or partner operating a DAF program.
4. A possible future DAF servicing organization.
5. Shared infrastructure and independently sellable components.

Phase III models keep their costs, revenues and liabilities apart, and allocate shared infrastructure only through an explicit rule (P3-DEC-MOD002, [15](15-shared-infrastructure-economics.md)).
