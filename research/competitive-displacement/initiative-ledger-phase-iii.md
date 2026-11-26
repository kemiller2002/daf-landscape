# Initiative ledger: Phase II decision implementation and Phase III research

Started 2026-11-26. This ledger records repository baselines, dependencies, decisions, changes and outstanding issues across the repositories this initiative touches. The Phase III research package keeps its own research ledger, starting with `research-ledger.md` in `research/competitive-advantage-creation/`.

## Repository baselines (main HEAD at start, 2026-11-26)

| Repository | Role | Baseline | Open PRs at start | Governance |
|---|---|---|---|---|
| kemiller2002/daf-landscape | Research | `10b92f4` (PR #92 merged; nothing later) | none | Repository conventions; F# package validators |
| kemiller2002/unbound | DAF product requirements | `79b9258` | none | Generated authoritative baseline (`tools/fs/Unbound.Convergence`); discovery packages |
| kemiller2002/transitus | Migration tooling | `d1b97be` (its PR #1 is merged) | #2 (CI batching) | Praxis |
| kemiller2002/praxis | Repository operating system | `e0f75e8` | 18, including #302 (governed improvement proposals) | Praxis |
| kemiller2002/echelon-foundry | Company site and Praxis pilot | `8c6b453` | #3, #4, #11 | Praxis |
| kemiller2002/echelon-organization-administration | Organization administration and business plan (private) | `c6118db` | none | README conventions |
| kemiller2002/clarity-framework | Clarity (private) | `200a9eb` | — | Read-only in this initiative |
| kemiller2002/echelon-diagnostic-framework | EDF | `710d54c` | — | Read-only (not attached for push) |
| kemiller2002/echelon-registry | Component registry | `91df6cc` | — | Read-only (not attached for push) |

**Superseding changes since Phase II.** daf-landscape `main` has no commits after the PR #92 merge, so no later change supersedes Phase II's conclusions. One input has changed:

- XRI-014 recorded that Transitus PR #1 was unmerged, and Phase II used it only as provisional evidence. It has since been merged (Transitus `d1b97be`). The XRI-014 disposition in [26](26-cross-repository-dispositions.md) records this.

## Dependencies

- Unbound's requirements depend on DEC-001 to DEC-007 and DEC-009 to DEC-010, through XRI-001 to XRI-008.
- Transitus depends on DEC-007, DEC-010 and DEC-011, through XRI-009 to XRI-014.
- The organization records depend on DEC-002, DEC-006 and DEC-008, through XRI-015 to XRI-017.
- Praxis depends on XRI-018 (where decision records are registered).
- Phase III research depends on the approved baseline (report 25), not on the original proposals.

## Log

| # | Step | Output | Verification |
|---|---|---|---|
| 1 | Repositories discovered, attached and cloned; baselines and open PRs recorded | this ledger | `git rev-parse`; GitHub PR lists |
| 2 | Owner approval recorded without changing the original proposals | [25](25-owner-approval-record.md), [decision-approvals.csv](data/registers/decision-approvals.csv), note in [23](23-executive-decision-register.md) | `validate`; ladder tests |
| 3 | Validator extended: approval coverage, ladder order, XRI disposition vocabulary and coverage | `model/src/CompetitiveDisplacement/Validate.fs`, 4 new tests | `dotnet test`: 20/20 |
