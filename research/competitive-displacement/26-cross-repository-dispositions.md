# 26 - Cross-repository dispositions and traceability (Stage I)

Status: record of Stage I of the Phase III initiative (2026-11-26). This report propagates the owner-approved decisions ([25](25-owner-approval-record.md)) and the eighteen cross-repository implications into the responsible repositories. The original implication proposals in [cross-repository-implications.csv](data/registers/cross-repository-implications.csv) are unchanged. Each implication's disposition, artifacts and open questions are in [xri-dispositions.csv](data/registers/xri-dispositions.csv).

The approvals authorize no implementation. Every new or refined requirement is **proposed**. Each repository's own rules govern when a proposal is ratified into its baseline. Until then, every decision's "requirements incorporated" stage stays at pending.

## 1. Branches produced

Every change is on branch `claude/fervent-galileo-bj4yk0` in its repository.

| Repository | Head | Content | Validation run |
|---|---|---|---|
| unbound | `17bfe50` | Discovery package `requirements/discovery/2026-11-26-competitive-displacement-decisions/`: 30 proposed UNB-CDD requirements, 5 owner decisions OD-CDD-01..05, F# validator `tools/fs/Unbound.CompetitiveDecisions` | Gates A1-A11 pass; 14/14 and 7/7 tests; question register 374 (9 new); existing validators pass. ReqAudit D9 (`RR-ADM-023-r2`) fails, as it already did on `79b9258` |
| transitus | `36e9e55` | DF-TRN-2026-0022..0026; 19 proposed requirements (171 total); dispositions document; pre-contract assessment specification | `praxis validate`, registry, provenance audit and `validate_specs.py` all pass (17/17) |
| echelon-organization-administration | `dede008` | `strategy/daf-entry/` 01-04: approved direction, five-entity separation, CAP-DAF-001/002, owner decision register, OD-DAF-IP-001, OD-DAF-CAP-001 | `npm test` passes |
| echelon-foundry | `fec24fe` | Draft standards DF-…-MTH-2026-48F0 (event-level economics) and DF-…-ENG-2026-6BEA (reproducible F# models); methodology proposals for Clarity, EDF and model validation | `praxis validate` passes; 12/12 tests |
| praxis | `ce7eca2` | Proposed RQ-ROS-2026-6C17 (authority stages and gates), 0863 (decision currency and invalidation), 6D60 (cross-repository propagation). DAF-agnostic | `praxis validate` passes; requirement tests 90/90; site 101/101 |
| daf-landscape | this branch | [25](25-owner-approval-record.md), this report, [decision-approvals.csv](data/registers/decision-approvals.csv), [xri-dispositions.csv](data/registers/xri-dispositions.csv), ledger, validator rules | `validate`; 20/20 tests |

## 2. Implication dispositions

| XRI | Target | Disposition | Artifacts |
|---|---|---|---|
| 001 | unbound | Requires a new owner decision | UNB-CDD-CMF-001/003; OD-CDD-01, OD-CDD-05 |
| 002 | unbound | New requirement added | UNB-CDD-CIV-001..003, 010..013 |
| 003 | unbound | Requirements updated | UNB-CDD-CIV-006..009 (the 180-day ceiling is preserved); OD-CDD-02 |
| 004 | unbound | New requirement added | UNB-CDD-CIV-004/005 |
| 005 | unbound | Already satisfied | UNB-CNET-003, UNB-TRN-002, UNB-CHAR-008 |
| 006 | unbound | New requirement added | UNB-CDD-OEM-001..004 |
| 007 | unbound | Requirements updated | UNB-CDD-OEM-005/006 |
| 008 | unbound | New requirement added | UNB-CDD-CMF-001/002/004/005/006; OD-CDD-03, OD-CDD-04 |
| 009 | transitus | New requirement added | MET-001/002 (maturity claims gated) |
| 010 | transitus | New requirement added | PRF-001..003, ASM-001..008; OD-TRN-P3-01, OQ-17 |
| 011 | transitus | Deferred behind an explicit gate | MET-003 (measurement only) |
| 012 | transitus | New requirement added | VR-014, MIG-005; VR-010 refined |
| 013 | transitus | Requirements updated | MP-010, MP-004, ARC-009 |
| 014 | transitus | Already satisfied | PR #1 merged; [18](18-transitus-implications.md) correction; DF-TRN-2026-0026 |
| 015 | echelon-foundry | New requirement added | DF-…-MTH-2026-48F0 (draft) |
| 016 | echelon-foundry | New requirement added | DF-…-ENG-2026-6BEA (draft) |
| 017 | echelon-organization-administration | New requirement added | CAP-DAF-001/002 (moved from echelon-foundry, which is public, because it holds capital figures) |
| 018 | echelon-organization-administration | Requirements updated | Owner decision register; Praxis RQ-ROS-2026-6C17/0863/6D60; Transitus DF-TRN records |

No implication was discarded. Placement decisions that departed from the original target:

- **XRI-017** moved from echelon-foundry to echelon-organization-administration, because echelon-foundry is public and the material holds capital figures.
- **XRI-018** registers the decisions in the organization's private register, with repository-specific DF records only where a decision binds a Praxis-governed repository. Praxis itself carries only DAF-agnostic mechanisms.

## 3. Decision-to-requirement trace

| Decision | Unbound | Transitus | Organization / methodology |
|---|---|---|---|
| DEC-001 | CMF-001/003/005/006; OD-CDD-01, OD-CDD-05 | — | 01 strategic direction |
| DEC-002 | CMF-001/002/005; OD-CDD-04 | — | CAP-DAF-001; entity separation |
| DEC-003 | CIV-006..009/012/013; OD-CDD-02 | — | — |
| DEC-004 | CIV-001/002/004/005/010; CMF-004 | — | — |
| DEC-005 | CIV-001..003/011/012; OEM-006 | Mapping suggestions are proposals only | Praxis 6C17 (no automatic advance) |
| DEC-006 | CMF-001/004/007; OEM-001..003; OD-CDD-03 | — | 01 strategic direction |
| DEC-007 | ONB-001/002 | MP-010; DF-TRN-2026-0023 | — |
| DEC-008 | (scope constraint) | DF-TRN-2026-0025/0026 | CAP-DAF-001/002; OD-DAF-CAP-001 |
| DEC-009 | OEM-005 (already CNV-PAY-001) | — | — |
| DEC-010 | ONB-001/003/004 | MET-001..003; DF-TRN-2026-0024 | — |
| DEC-011 | ONB-002 | DF-TRN-2026-0022 | — |
| DEC-012 | validation-gates.csv maps V-1..V-9 | V-4 is the Transitus gate | Phase III Track B |

(Unbound IDs carry the prefix UNB-CDD-.)

## 4. Conflicts found and how they were handled

| Conflict | Handling |
|---|---|
| DEC-001 partner-first vs the ratified entry route (CNV-ECO-004, OD-M-05) | Ratified text governs; OD-CDD-01 raised for after V-1/V-6 report |
| DEC-003 change-driven renewal vs the 180-day "deep review" (CNV-GRT-003) | Ceiling preserved; OD-CDD-02 asks whether a change-driven renewal may count as the deep review |
| DEC-006 licence-first vs ~20 bps assumptions (OD-CNO-10, FIL-OD-10) | Records not edited; OD-CDD-03 raised |
| DEC-002 anchor gate vs the OD-M-08 staffed-administration offer | OD-CDD-04 raised |
| Partner channel vs the CNV-ECO-004 25% concentration cap | OD-CDD-05 raised (measured per end sponsor or per partner) |
| Transitus DF-0016 kill criterion has no gating successor (UC-19) | Resolved by owner: OD-P3-02, the kill rule does not stop Transitus |
| Legal basis for assessment tiers (Phase II vs UNB-ONB-003) | Transitus applies the stricter references; OD-TRN-P3-01 raised |
| Rehearsal count (Phase II ≥2 mocks vs UNB-ONB-011 ≥3 trial runs) | Unbound owns the count; Transitus fixes none (UC-18) |
| Unbound OD-M-14 records that no design partner is available, vs the partner-first G1 timeline | Recorded for Phase III (P3-CLM-AB017) |

## 5. Owner decisions still open from Stage I

| ID | Question |
|---|---|
| OD-CDD-01 | Unbound: amend the CNV-ECO-004 entry route to partner-first after V-1 and V-6 report |
| OD-CDD-02 | Unbound: may a change-driven renewal count as the 180-day deep review |
| OD-CDD-03 | Unbound: restate the ~20 bps assumptions in OD-CNO-10 and FIL-OD-10 on a licence-first basis |
| OD-CDD-04 | Unbound: does the DEC-002 anchor gate apply to the OD-M-08 staffed-administration offer |
| OD-CDD-05 | Unbound: is the 25% concentration cap measured per end sponsor or per partner |
| OD-TRN-P3-01 | Transitus: which legal basis binds each assessment tier |
| OQ-17 | Transitus: disclosure thresholds for the T1 profile |
| OD-P3-03 threshold | Organization: what counts as "significant" expenses for the kill-rule clock |
| Standards | echelon-foundry: accept or reject the two draft standards |
| Praxis | Accept or reject RQ-ROS-2026-6C17, 0863 and 6D60 |
| Shared costs | Organization: the shared-cost allocation rule across the five entities; whether Unbound will ever be a separate entity |
| IP mechanics | Organization and counsel: assignment instruments, work created before formation, third-party components |
