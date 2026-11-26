# 18 - Transitus implications

Status: research (2026-11-26; revision 2). Transitus owns migration and integration requirements. Its research and requirements are on branch `claude/transitus-research-architecture-42a96z` (PR #1, **not merged**); this package treats them as provisional (XRI-014). No Transitus file was changed.

## 1. What this research confirms in Transitus

| Transitus element | Phase II evidence |
|---|---|
| Pure, total, versioned transformations; immutable content-addressed raw input; Merkle-sealed staging (TRN-REQ-TX/ST) | Matches the cross-industry pattern of deterministic replay and evidence before load (CLM-022) |
| "AI proposes, deterministic gates dispose" (DF-TRN-2026-0012) | Mapping suggestions reach F1 ~0.7 only with rule checks (CLM-034) |
| Mapping packages are configuration only (DF-TRN-2026-0014); basic packages in phase 1 (DF-TRN-2026-0019) | Reusable target package + per-source adapter split ([08](08-frictionless-onboarding.md) §4) |
| Generic reconciliation primitives (DF-TRN-2026-0011) | Exact money reconciliation is non-negotiable; sampling suits non-money attributes |
| Phase gating and kill criterion (DF-TRN-2026-0016) | Consistent with the gated, partner-first strategy ([16](16-commercial-entry-strategy.md)) |

## 2. Proposed additions (traceable)

| ID | Proposal | Basis |
|---|---|---|
| XRI-009 | Adopt the onboarding maturity model (levels 0-5) and its progression metrics as Transitus measurement targets; claim levels only from measured runs | Track D synthesis |
| XRI-010 | Specify pre-contract tiers: T0 (no install, sponsor-completed template), T1 (profiler after sponsor IT approval; minimum fund count; dominance suppression on money cells), T2+ only under MSA + DPA; synthetic runs are layout conformance checks, never data-quality ratings (revision 2, CHL-017/069/070) | Pre-contract constraints ([08](08-frictionless-onboarding.md) §3) |
| XRI-011 | Define a migration SLA whose clock starts on a conforming extract, with a published exclusions list and a sponsor-approved validation summary | Stripe PAN import pattern (SRC-044) |
| XRI-012 | Add statistical-sampling validation for non-money attributes alongside exact money reconciliation | JAMIA 2016 (SRC-045); GAO-22-103718 (SRC-046) |
| XRI-013 | Keep vendor-specific packages deferred; when the first sample arrives, cluster on one incumbent source to amortise one adapter | DEC-007, DEC-011; HYP-012 |

## 3. Commercial role of Transitus

Transitus is the migration engine of the **partner pilot** recommended in [16](16-commercial-entry-strategy.md): canonical import, basic packages, dry runs, reconciliation gates and evidence. That raises the importance of phase 1 and lowers the urgency of phases 2-4 until a customer-authorised export exists. The adversarial review (CHL-067, CHL-068, CHL-072) found that a migration assessment has no standalone buyer or price, that report adapters support balance-level conversion only, and that full history needs a contracted incumbent export; so Transitus should be judged by one reconciled live migration, not by assessment revenue. Adapters must be versioned per incumbent report version with drift tests (CHL-071), and SLAs should be process-only with capped liability (CHL-075).

## Post-merge correction (2026-11-26, Stage I)

Transitus PR #1 has since merged (Transitus `d1b97be`). Stage I re-checked this report's citations against the merged decision records. The original rows above are kept unchanged.

- **DF-TRN-2026-0014** is superseded by DF-TRN-2026-0019, which carries its rules forward. Read the mapping-package row as citing DF-TRN-2026-0019.
- **DF-TRN-2026-0016's kill criterion has no gating successor.** Its replacement, requirement PF-004, does not gate phase 1. The row above calling it "consistent" with the gated strategy therefore no longer holds. Transitus records this as conflict UC-19 and raises owner decision OD-TRN-P3-02 (whether the DEC-008 kill rule pauses Transitus work beyond phase 1). See [26](26-cross-repository-dispositions.md).
