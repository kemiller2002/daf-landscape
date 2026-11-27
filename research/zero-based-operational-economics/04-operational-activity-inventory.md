# 04 — Operational activity inventory

Register: [`operational-activities.csv`](data/registers/operational-activities.csv) — **183 activities** (180 from the inventory track plus OA-TEC-022 defect correction, OA-TEC-023 shared integration upkeep and OA-TEC-024 regulatory change, added after adversarial review; OA-TEC-010, OA-TEC-006, OA-TEC-007 and OA-ACN-008 revised, each with a `REV-A`/`REV-B` note in `evidence_sources`), 35 fields each (identifier, description, trigger, driver, frequency low/base/high, seasonality, Unbound requirements, responsible entity, authority, qualification, controls, classification, human role, exception rate and minutes low/base/high, independent authorization, SLA, peak characteristics, dependencies, external cost, evidence class, confidence, sources, validation method, why it exists, legal status, elimination challenge). Method notes: [activity-inventory-notes.md](data/evidence/activity-inventory-notes.md). Unbound was read at commit `79b9258`; nothing in Unbound was changed.

## 1. Coverage

| Domain | Activities | Examples |
|---|---:|---|
| COMPLIANCE | 32 | sanctions alert disposition, policy packs, control testing, regulatory monitoring, retention, sponsor reporting, incident escalation |
| GRANT | 24 | intake and affirmation, Tier-2 exception review, release authorization, ACH/check/wire execution, returns, uncashed checks and escheat, cancellations, fraud |
| ACCOUNT | 23 | opening, identity, advisors and successors, delegation, changes, death/incapacity, inquiries, accessibility, closure |
| TECHOPS | 21 | monitoring and on-call, incidents, backups and DR drills, vulnerabilities, maintenance, deployments, two-approver review, AI change control, SOC evidence |
| CONTRIB | 19 | cash/ACH/wire, securities, recurring, payroll, attribution, unidentified receipts, valuation, acknowledgments, refunds |
| ACCOUNTING | 18 | ledger, journal validation, bank and custodial reconciliation, close, statements, audit support, corrections |
| COMMERCIAL | 17 | sales, procurement questionnaires, onboarding, migration assessment and execution, training, retention, exit and portability |
| INVEST | 16 | allocation, custodial integration, valuation ingestion, reconciliation, liquidity, fees and accruals, loss attribution |
| CHARITY | 10 | identity resolution, transaction-time checks, 180-day revalidation, adverse-event monitoring, fiscal sponsorship, payment destination enrolment |

Activities discovered beyond the mission's list include: two-approver code review (CNV-PLT-010), AI agent change control, break-glass and kill-switch activation, operator access requests to tenant data, sponsor exit and bulk transfer, first-sponsor economic evidence obligations, California AG/FTB status ingestion, donor hypercare after cutover, answer-corpus maintenance.

**Not modelled** (see notes §4): grant agreements/milestones/impact reports (no baseline); sponsor enterprise overhead outside DAF administration (internal audit, board, HR); Echelon corporate finance/legal/hiring (handled in fixed lines). Deferred scope (cards, foreign/expenditure-responsibility grants, UBIT) is listed as ELIMINATED with zero frequency.

## 2. Classification

| Class | Activities | Hours at 10k accounts / 90k grants / 5 sponsors (agent reference) |
|---|---:|---:|
| AUTO-EXCEPTION | 54 | 4,249 |
| HUMAN-JUDGMENT | 24 | 7,702 |
| DETERMINISTIC | 22 | 647 |
| SHARED-ECHELON | 20 | 2,152 |
| SPONSOR-OWNED | 19 | 1,420 |
| AI-ASSISTED | 18 | 5,115 |
| INDEPENDENT-AUTHORIZATION | 13 | 1,236 |
| EXTERNAL-PROVIDER | 7 | 836 |
| ELIMINATED | 3 | 0 |
| PREVENTED | 0 | — (prevention is modelled inside rows) |

Responsible entity: sponsor 59, shared Echelon 51, administrator 45, software provider 14, bank/payment provider 5, custodian 3, external professional 3. Legal status: not legally required 71, contractual 47, legally required 41, uncertain 21. Independent authorization required: 15.

## 3. Where the hours are (reference: 10k accounts, 90k grants, 25k contributions, 5 sponsors)

About 23,400 human hours a year across all parties before configuration splits. The top 15 activities are 57% of minutes:

| Rank | Activity | Responsible | Hours/yr | Share |
|---|---|---|---:|---:|
| 1 | OA-GRT-005 Exception grant review and decision (Tier 2 / reserved) | **sponsor** | 5,670 | 24.3% |
| 2 | OA-ACG-007 Monthly close and controller sign-off | sponsor | 1,250 | 5.4% |
| 3 | OA-ACN-008 Human-handled donor and advisor contacts | administrator | 1,133 | 4.9% |
| 4 | OA-ACG-004 Reconciliation break investigation | administrator | 708 | 3.0% |
| 5 | OA-ACG-011 Year-end external audit support | sponsor | 600 | 2.6% |
| 6 | OA-CON-004 Unidentified receipt attribution | administrator | 550 | 2.4% |
| 7 | OA-COM-007 Sponsor implementation and configuration | shared Echelon | 500 | 2.1% |
| 8 | OA-GRT-013 Paper check grants (positive pay, mailing) | bank/payment | 428 | 1.8% |
| 9 | OA-CON-005 Securities gift receipt and valuation | custodian | 408 | 1.7% |
| 10 | OA-ACN-023 Major-donor stewardship (optional) | sponsor | 400 | 1.7% |
| 11 | OA-TEC-021 AI agent configuration, evaluation, change control | shared Echelon | 384 | 1.6% |
| 12 | OA-COM-009 Data migration execution | shared Echelon | 367 | 1.6% |
| 13 | OA-GRT-012 Electronic grant payment execution | bank/payment | 314 | 1.3% |
| 14 | OA-GRT-016 Uncashed/voided checks, reissue, escheat | administrator | 285 | 1.2% |
| 15 | OA-GRT-001 Grant recommendation intake and affirmation | software provider | 260 | 1.1% |

The single most important number in the whole model is the **Tier-2 trigger incidence (9% of grants) × 42 minutes** in OA-GRT-005. It is anchored to EV-E10, unmeasured for Unbound, and — under Unbound's own requirements (CNV-GRT-011, CNV-GOV-004) — performed by sponsor-appointed reviewers, not by Echelon.

## 4. Model run at the reference scenario

At the reference ($500M AUA, 2,000 accounts, 1 sponsor, full administration CFG-5) the model generates about 304,000 events a year, of which **96.7% complete without a person**. About 9,950 are human-handled and about 1,220 independently authorised (after review corrections). See [`activity-loads-reference.csv`](data/model-outputs/activity-loads-reference.csv) for every activity's events, human events, minutes and vendor share.

## 5. Data quality

93 rows are ASSUMPTION, 80 INFERENCE, 4 VERIFIED-FACT, 3 UNKNOWN; 92 low confidence, 84 medium, 4 high. Known anchor problems: EV-E03 and EV-E10 "native" minutes exceed conventional minutes per touch (fewer, harder residual cases); ACT-S01/S05 units ambiguous (per sponsor-year used); SPW complex-gift volume is 13× ACT-A05 (ACT-A05 used). Every activity carries a validation method; [25](25-evidence-gaps-and-validation-plan.md) orders them.
