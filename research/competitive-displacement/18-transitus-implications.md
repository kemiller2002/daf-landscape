# 18 - Transitus implications

Status: research (2026-11-26). Transitus owns migration and integration requirements. Its research and requirements are on branch `claude/transitus-research-architecture-42a96z` (PR #1, **not merged**); this package treats them as provisional (XRI-014). No Transitus file was changed.

## 1. What this research confirms in Transitus

| Transitus element | Phase II evidence |
|---|---|
| Pure, total, versioned transformations; immutable content-addressed raw input; Merkle-sealed staging (TRN-REQ-TX/ST) | Matches the cross-industry pattern of deterministic replay and evidence before load (CLM-022) |
| "AI proposes, deterministic gates dispose" (DF-TRN-2026-0012) | Mapping suggestions reach F1 ~0.7 only with rule checks (CLM-034) |
| Mapping packages are configuration only (DF-TRN-2026-0014); basic packages in phase 1 (DF-TRN-2026-0019) | Reusable target package + per-source adapter split ([08](08-frictionless-onboarding.md) §4) |
| Generic reconciliation primitives (DF-TRN-2026-0011) | Exact money reconciliation is non-negotiable; sampling suits non-money attributes |
| Phase gating and kill criterion (DF-TRN-2026-0016) | Consistent with the evidence-first strategy ([16](16-commercial-entry-strategy.md)) |

## 2. Proposed additions (traceable)

| ID | Proposal | Basis |
|---|---|---|
| XRI-009 | Adopt the onboarding maturity model (levels 0-5) and its progression metrics as Transitus measurement targets; claim levels only from measured runs | Track D synthesis |
| XRI-010 | Specify a T0/T1 pre-contract assessment that runs inside the sponsor's environment and emits only k-suppressed structural aggregates (field coverage, null rates, fund-type counts) and a synthetic rehearsal | Pre-contract constraints ([08](08-frictionless-onboarding.md) §3) |
| XRI-011 | Define a migration SLA whose clock starts on a conforming extract, with a published exclusions list and a sponsor-approved validation summary | Stripe PAN import pattern (SRC-044) |
| XRI-012 | Add statistical-sampling validation for non-money attributes alongside exact money reconciliation | JAMIA 2016 (SRC-045); GAO-22-103718 (SRC-046) |
| XRI-013 | Keep vendor-specific packages deferred; when the first sample arrives, cluster on one incumbent source to amortise one adapter | DEC-007, DEC-011; HYP-012 |

## 3. Commercial role of Transitus

Transitus is the engine of the **minimum viable commercial entry point** (migration assessment + reconciliation report at contract-end windows). That raises the importance of its phase 1 (canonical import, basic packages, dry runs, reconciliation gates, evidence) and lowers the urgency of phases 2-4 until a customer-authorised export exists. As a standalone product (route ER-2) it does not pay for itself (CLM-028).
