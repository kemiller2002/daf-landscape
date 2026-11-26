# Initiative ledger: Phase II decision implementation and Phase III research

Started 2026-11-26. This ledger records repository baselines, dependencies, decisions, changes and outstanding issues across the repositories this initiative touches. The Phase III research package keeps its own research ledger, starting with `research-ledger.md` in `research/competitive-advantage-creation/`.

## Repository baselines (main HEAD at start, 2026-11-26)

| Repository | Role | Baseline | Open PRs at start | Governance |
|---|---|---|---|---|
| kemiller2002/daf-landscape | Research | `10b92f4` (PR #92 merged; nothing later) | none | Repository conventions; F# package validators |
| kemiller2002/unbound | DAF product requirements | `79b9258` | none | Generated authoritative baseline (`tools/fs/Unbound.Convergence`); discovery packages |
| kemiller2002/transitus | Migration tooling | `d1b97be` (its PR #1 is merged) | none | Praxis |
| kemiller2002/praxis | Repository operating system | `e0f75e8` | 18, including #302 (governed improvement proposals) | Praxis |
| kemiller2002/echelon-foundry | Company site and Praxis pilot | `8c6b453` | #2 (CI batching) | Praxis |
| kemiller2002/echelon-organization-administration | Organization administration and business plan (private) | `c6118db` | #3, #4, #11 | README conventions |
| kemiller2002/clarity-framework | Clarity (private) | `200a9eb` | — | Read-only in this initiative |
| kemiller2002/echelon-diagnostic-framework | EDF | `710d54c` | — | Read-only (not attached for push) |
| kemiller2002/echelon-registry | Component registry | `91df6cc` | — | Read-only (not attached for push) |

**Superseding changes since Phase II.** daf-landscape `main` has no commits after the PR #92 merge, so no later change supersedes Phase II's conclusions. One input has changed:

- XRI-014 recorded that Transitus PR #1 was unmerged, and Phase II used it only as provisional evidence. It has since been merged (Transitus `d1b97be`). The XRI-014 disposition in [26](26-cross-repository-dispositions.md) records this.

## Dependencies

- Unbound's requirements trace to all twelve decisions (DEC-008 and DEC-012 only as scope and validation constraints), through XRI-001 to XRI-008.
- Transitus depends on DEC-005, DEC-007, DEC-008, DEC-010, DEC-011 and DEC-012, through XRI-009 to XRI-014.
- echelon-foundry receives XRI-015 and XRI-016 (methodology and engineering standards).
- The organization records depend on DEC-001, DEC-002, DEC-006 and DEC-008, through XRI-017 and XRI-018 (XRI-018's decision register is held there).
- Praxis receives only DAF-agnostic requirement proposals arising from XRI-018 (authority stages, decision currency, cross-repository propagation).
- Phase III research depends on the approved baseline (report 25), not on the original proposals.

## Log

| # | Step | Output | Verification |
|---|---|---|---|
| 1 | Repositories discovered, attached and cloned; baselines and open PRs recorded | this ledger | `git rev-parse`; GitHub PR lists |
| 2 | Owner approval recorded without changing the original proposals | [25](25-owner-approval-record.md), [decision-approvals.csv](data/registers/decision-approvals.csv), note in [23](23-executive-decision-register.md) | `validate`; ladder tests |
| 3 | Validator extended: approval coverage, ladder order, XRI disposition vocabulary and coverage | `model/src/CompetitiveDisplacement/Validate.fs`, 4 new tests | `dotnet test`: 20/20 |
| 4 | Stage I agents finish: Transitus (`36e9e55`), organization administration (`dede008`), echelon-foundry (`fec24fe`), Praxis (`ce7eca2`), Unbound (`17bfe50`) | [26](26-cross-repository-dispositions.md) | Each repository's own validators (see 26 §1) |
| 5 | Owner decisions OD-P3-01..03 (IP ownership; kill rule does not stop Transitus; kill-rule start) recorded in daf-landscape, organization administration and Transitus; Unbound, Transitus and echelon-foundry IP notes added after review finding S1-08 | [25](25-owner-approval-record.md) | `validate` |
| 6 | Report 18 annotated: DF-TRN-2026-0014 superseded; the DF-0016 kill criterion has no gating successor | [18](18-transitus-implications.md) | — |
| 7 | XRI dispositions complete (18/18); decision-to-requirement trace | [xri-dispositions.csv](data/registers/xri-dispositions.csv) | `validate OK: 48 CSV, 37 Markdown`; 20/20 tests; `check` reproduces |
| 8 | Owner decision OD-P3-04 ("Significant is when it becomes its own cost center") recorded | [25](25-owner-approval-record.md); org OD-DAF-CAP-002 | `validate`; `npm test` |
| 9 | Independent Stage I review: 16 findings (1 blocking), all resolved | [26](26-cross-repository-dispositions.md) §6 | Fix commits: daf-landscape `fcdcc8c`; unbound `edbcd0d`; transitus `dda2134`/`0d089a2`; org `ea9ff34`; foundry `1071e25`/`c0ed458`. All validators re-run and pass |
| 10 | Stage I PRs opened (draft): daf-landscape #93, unbound #22, transitus #2, praxis #314, echelon-foundry #13, echelon-organization-administration #22. Baseline table corrected (open PRs at start had been attributed to the wrong repositories) | — | GitHub |
