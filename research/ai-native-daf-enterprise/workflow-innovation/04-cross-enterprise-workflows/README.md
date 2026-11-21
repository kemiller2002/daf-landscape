# Cross-enterprise workflow redesigns (XW-01 to XW-31)

There are **31 cross-enterprise workflows**, each spanning several legacy departments. They are **new relative to** the parent workstream's WF-01…WF-24 ([`../../03-workflow-redesign/`](../../03-workflow-redesign/)). The parent workflows redesign *one sponsor's* processes. These are built around reusable capabilities, inter-organization infrastructure and the radical innovations in the [innovation register](../02-creative-hypotheses/innovation-register.csv) (INN-01…INN-38).

Machine-readable index: [`workflows.csv`](workflows.csv). It has 31 rows, with departments spanned, trigger, innovations, maturity, experiments, human decisions, eliminated ACT-ids, work moved, new events and new endpoints. There are 16 mermaid sequence diagrams.

**Maturity reminder:** no workflow here is above **L3**, and an L3 workflow works only in a model. Most are L1. They are hypotheses that the experiments in [`../08-experiments/`](../08-experiments/) and the adversarial review in [`../07-adversarial-reviews/`](../07-adversarial-reviews/) test.

## Index

| ID | Workflow | File | Innovations | Maturity | Experiments |
|---|---|---|---|---|---|
| XW-01 | One verified identity, many authorized interactions | [shared](xw-shared-capabilities.md#xw-01-one-verified-identity-many-authorized-interactions) | INN-24, 25, 16, 26 | L1 (delegation L3) | E5 |
| XW-02 | One contribution event drives custody, accounting, investments, reporting and liquidity | [shared](xw-shared-capabilities.md#xw-02-one-contribution-event-drives-custody-accounting-investments-reporting-and-liquidity) | INN-23, 27, 22 | L3 fan-out / L1 references | E4, E9 |
| XW-03 | Recipient passport: one evidence record, many grants | [shared](xw-shared-capabilities.md#xw-03-recipient-passport-one-reusable-evidence-record-serves-many-grants) | INN-01, 03, 34, 07 | L2 | E1, E7 |
| XW-04 | One policy evaluation service across domains | [shared](xw-shared-capabilities.md#xw-04-one-policy-evaluation-service-across-onboarding-grants-payments-and-compliance) | INN-05, 21, 36 | L3 grants / L1 | E2 |
| XW-05 | One evidence system for audit, governance, reporting and improvement | [shared](xw-shared-capabilities.md#xw-05-one-operational-evidence-system-serves-audit-governance-reporting-and-improvement) | INN-20, 32, 30 | L3 partial | E11 |
| XW-06 | Pre-verified recipient universe | [grants](xw-grants-and-recipients.md#xw-06-pre-verified-recipient-universe-verification-happens-before-the-request) | INN-03, 01, 34, 05 | L2 | E1, E2 |
| XW-07 | Cross-sponsor verification network | [grants](xw-grants-and-recipients.md#xw-07-cross-sponsor-verification-network-join-contribute-consume) | INN-02, 01, 04, 36 | L1 (L2 if E7) | E7, E11 |
| XW-08 | Reusable determinations lifecycle | [grants](xw-grants-and-recipients.md#xw-08-reusable-non-routine-determinations-lifecycle) | INN-04, 28, 02 | L2 | E2, E6, E11 |
| XW-09 | Universe sanctions rescreen on list change | [grants](xw-grants-and-recipients.md#xw-09-universe-sanctions-rescreen-on-list-change) | INN-34 | L2 | E1 |
| XW-10 | Shared specialist pool across sponsors | [grants](xw-grants-and-recipients.md#xw-10-shared-specialist-pool-across-sponsors) | INN-28, 37, 04 | L1 | E6, E11 |
| XW-11 | Daily netting disbursement with itemized remittance | [money](xw-money-and-assets.md#xw-11-daily-netting-disbursement-with-itemized-remittance) | INN-09, 08, 07 | L1 | E3, E9, E11 |
| XW-12 | Recipient payee registry: enrollment and change | [money](xw-money-and-assets.md#xw-12-recipient-payee-registry-enrollment-and-bank-detail-change) | INN-07, 29, 01 | L1 | E3 |
| XW-13 | Recipient inbox | [money](xw-money-and-assets.md#xw-13-recipient-inbox-one-place-for-every-incoming-daf-grant) | INN-38, 10, 08 | L0–L1 | E3 |
| XW-14 | Complex asset pre-underwriting and liquidation partner | [money](xw-money-and-assets.md#xw-14-complex-asset-pre-underwriting-structured-documents-and-a-liquidation-partner) | INN-11, 12, 13, 28 | L1 | E5, E6 |
| XW-15 | Continuous close with controller attestation | [money](xw-money-and-assets.md#xw-15-continuous-close-with-controller-attestation) | INN-22, 23, 20 | L3 logic / L1 | E4, E9 |
| XW-16 | Pipeline liquidity planning and seasonal buffer | [money](xw-money-and-assets.md#xw-16-pipeline-based-liquidity-planning-and-seasonal-buffer) | INN-27, 37 | L2 | E6 |
| XW-17 | Continuous onboarding at first intent (KYC attestation reuse) | [relationships](xw-relationships-and-distribution.md#xw-17-continuous-onboarding-account-at-first-intent-with-upstream-kyc-attestation-reuse) | INN-25, 24, 23, 16 | L1 | E5 |
| XW-18 | Advisor-embedded invisible DAF | [relationships](xw-relationships-and-distribution.md#xw-18-advisor-embedded-invisible-daf) | INN-15, 16, 24 | L2 | E5, E11 |
| XW-19 | Donor agent delegation lifecycle | [relationships](xw-relationships-and-distribution.md#xw-19-donor-side-ai-agent-delegation-lifecycle) | INN-26, 16 | L3 | parent tests, E10 |
| XW-20 | DAF transfer protocol (ACATS-like) with history | [relationships](xw-relationships-and-distribution.md#xw-20-daf-transfer-protocol-acats-like-with-history) | INN-17, 18 | L1 | E8 |
| XW-21 | Spend-down horizon and charitable defaults | [relationships](xw-relationships-and-distribution.md#xw-21-spend-down-horizon-and-charitable-defaults) | INN-19, 33, 27 | L1 | desk, E6 |
| XW-22 | Year-end surge smoothing with execution windows | [relationships](xw-relationships-and-distribution.md#xw-22-year-end-surge-smoothing-with-execution-windows) | INN-37, 03, 28 | L1 | E6 |
| XW-23 | Zero-ticket servicing | [relationships](xw-relationships-and-distribution.md#xw-23-zero-ticket-servicing) | INN-14, 38 | L1 | E6 |
| XW-24 | Policy compiler change | [governance](xw-governance-and-learning.md#xw-24-policy-compiler-change-from-law-change-to-deployed-back-tested-rule) | INN-21, 36 | L3 partial | E2 |
| XW-25 | Continuous audit package | [governance](xw-governance-and-learning.md#xw-25-continuous-audit-package-and-external-audit) | INN-20, 22 | L3 partial | E11 |
| XW-26 | Board oversight with expiring governed parameters | [governance](xw-governance-and-learning.md#xw-26-board-oversight-with-expiring-governed-parameters) | INN-32, 30, 20 | L1 | desk |
| XW-27 | Twin-driven staffing and surge planning | [governance](xw-governance-and-learning.md#xw-27-twin-driven-staffing-and-surge-planning) | INN-30, 28, 37 | L3 (simulated) | E6 |
| XW-28 | Regulatory inquiry evidence pull | [governance](xw-governance-and-learning.md#xw-28-regulatory-inquiry-evidence-pull) | INN-20, 21 | L2 | E11 |
| XW-29 | Always-migrated: migration by event-log replay | [governance](xw-governance-and-learning.md#xw-29-always-migrated-system-of-record-change-by-event-log-replay) | INN-18, 17 | L2 | E8, E9 |
| XW-30 | Sponsor wind-down or program exit | [governance](xw-governance-and-learning.md#xw-30-sponsor-wind-down-or-program-exit) | INN-17, 18, 19 | L1 | E8 |
| XW-31 | Custodian or key-vendor failover | [money](xw-money-and-assets.md#xw-31-custodian-or-key-vendor-failover) | INN-27, 18 | L2 | E6, E9 |

## Categories of work eliminated across the enterprise

Several workflows together remove a whole *category* of work, not a single step. For each category, the table shows its legacy activities (ACT-ids), what **replaces its underlying function** (nothing is eliminated without a stated replacement), and what remains or moves.

| Category of work | Legacy activities | Workflows that remove it | What replaces the function | What remains or moves |
|---|---|---|---|---|
| **Transaction-level verification research** | ACT-017, 018, 019, 023, 031 | XW-03, 06, 07, 09 | Recipient passport plus pre-verified universe plus rescreen on list change; verification attached to the recipient, not the grant | Name-resolution confirmation (donor); churches and recipients without filings (enrollment or manual); network governance (XW-07) |
| **Repeated non-routine judgment** | Per-grant repeats of ACT-020, 021, 022 | XW-08, 10 | Versioned, expiring determinations reused per arrangement; pooled specialists | The judgment itself stays human; determination quality work increases per case |
| **Status inquiries (donor, advisor, charity)** | ACT-030, 051, 052 | XW-13, 23, 18 | Shared state projections, push notifications, recipient inbox, grounded answers | Service recovery; a guaranteed human path |
| **Matching and re-keying** | ACT-005, 006, 010, 031, 056, 059 | XW-01, 02, 17, 18 | Canonical Party; unique contribution references; structured channels; scoped delegations | Upstream reliance (attestation issuers); donors must use references |
| **Paper payment handling** | ACT-024, 025, 026, 070, 077 | XW-11, 12, 13 | Payee registry, netted electronic payments with itemized remittance, inbox | Recipient enrollment effort; checks for non-enrolled recipients |
| **Periodic reconstruction** (close, audit samples, board packs, filings assembly) | ACT-038, 039, 041, 044 (prep), 061, 073 | XW-05, 15, 25, 26 | Evidence by operation; continuous reconciliation; on-demand packages; expiring parameters | Monthly controller attestation (CTL-048); auditor re-performance; board review of deltas |
| **Prose-policy maintenance and retraining** | ACT-045, 046, 050, 072 | XW-04, 24 | Policy compiler with back-test and generated prose | Counsel interpretation; policy engineering |
| **Migration and exit projects** | ACT-055; one-off migrations | XW-20, 29, 30 | Transfer protocol; continuous event-log export and replay | Counterparties must adopt the protocol or event ingestion |
| **Surge firefighting and ratio-based staffing** | Part of ACT-071, 072 | XW-10, 22, 27 | Twin forecasts, execution windows, pooled specialists | Twin model risk; some donors wait (with consent) |
| **Manual cash and liquidity spreadsheets** | ACT-035, 068 | XW-16, 31 | Pipeline forecast, seasonal buffer, failover runbooks | Committee sets parameters; second-custodian cost |

**What is *not* eliminated anywhere:**
- Sanctions true-match decisions.
- Expenditure-responsibility and equivalency determinations.
- Complex-asset acceptance and the 8283 signature.
- Write-offs.
- Charitable-default distributions.
- Policy interpretation and publication.
- Board approvals.
- Audit judgment.
- Regulatory responses.

These are the H decisions the regulatory map keeps human.

## NEW events proposed (not yet in [`events.csv`](../../06-data-and-knowledge/events.csv))

| Event | Workflow(s) |
|---|---|
| `IdentityAttestationAccepted` | XW-01, 17 |
| `RecipientPassportRefreshed` | XW-03, 06 |
| `NetworkMemberAdmitted`, `NetworkEvidencePublished`, `NetworkEvidenceAccepted`, `NetworkEvidenceDisputed` | XW-07 |
| `DeterminationApplied`, `DeterminationIssued`, `DeterminationExpiring` | XW-08 |
| `SpecialistPoolCaseSubmitted` | XW-10 |
| `NettedPaymentProposed` | XW-11 |
| `PayeeRegistryEnrollmentVerified` | XW-12 |
| `RecipientInboxNoticePosted`, `GrantClaimed` | XW-13 |
| `IndicativeAcceptanceIssued`, `LiquidationBidRequested`, `LiquidationBidAccepted` | XW-14 |
| `ControllerAttestationSigned` | XW-15 |
| `LiquidityForecastPublished` | XW-16 |
| `CustodianFailoverActivated` | XW-31 |
| `DataNeeded` | XW-17 |
| `AdvisorEmbedSessionStarted` | XW-18 |
| `TransferInitiated`, `TransferRequestReceived`, `TransferAssetsDelivered`, `HistoryPackageDelivered` | XW-20 |
| `SpendDownPlanAdopted` | XW-21 |
| `ExecutionWindowAssigned` | XW-22 |
| `PolicyCompiled`, `PolicyBackTestCompleted` | XW-24 |
| `AuditPackageGenerated` | XW-05, 25 |
| `ImprovementProposed` | XW-05 |
| `ParameterExpiring`, `ParameterRenewed` | XW-26 |
| `TwinForecastPublished`, `StaffingRecommendationIssued` | XW-27 |
| `RegulatoryInquiryOpened`, `InquiryEvidenceExported` | XW-28 |
| `ReplayVerified`, `ReplayMismatch` | XW-29 |
| `WindDownPlanApproved` | XW-30 |

## NEW endpoints proposed (not yet in [`api-catalog.csv`](../../04-enterprise-apis/api-catalog.csv))

| Endpoint | Exposure (proposed) | Workflow(s) |
|---|---|---|
| `POST /v1/attestations/identity` | partner | XW-01, 17 |
| `GET /v1/recipients/{id}/passport` | internal; partner read for C-model sponsors | XW-03 |
| `POST/GET /v1/network/evidence`, `/v1/network/members` | network members (mTLS) | XW-07 |
| `GET/POST /v1/determinations` | internal; network for artifacts | XW-08 |
| `POST /v1/pool/cases` | tenant-internal | XW-10 |
| internal `POST /v1/payments` (netted variant) | **internal only** (payment gate) | XW-11 |
| `POST/PATCH /v1/payee-registry`, `/v1/recipients/{id}/attestations` | recipient-authenticated | XW-12 |
| `GET /v1/recipient-inbox`, `POST /v1/recipient-inbox/{id}/claim` | recipient-authenticated | XW-13 |
| `POST /v1/asset-classes/{id}/underwriting` | partner (advisors, attorneys) | XW-14 |
| `POST /v1/ledger/periods/{p}/attest` | internal (controller) | XW-15 |
| `GET /v1/positions/forecast` | internal | XW-16 |
| `/v1/parties/{id}/preferences` | public (donor) | XW-17 |
| `POST /v1/embed/sessions` | partner (wealth platforms) | XW-18 |
| `POST/GET /v1/transfers` | sponsor-to-sponsor (protocol) | XW-20, 30 |
| `GET /v1/exports/event-log` | donor (own account), sponsor (exit), auditor | XW-20, 29, 30 |
| `POST /v1/schedules` | public (donor), partner | XW-21 |
| `executionWindow` field on `POST /v1/recommendations` | public, partner | XW-22 |
| `POST /v1/policies/{id}/evaluate`, `/compile`, `/backtest`, `/v1/policies/obligations` | internal | XW-04, 24 |
| `POST /v1/evidence/packages`, `/v1/decisions/{id}/replay` | auditor, regulator-response (internal) | XW-05, 25, 28 |
| `GET /v1/parameters` | internal, board | XW-26 |
| `GET /v1/twin/forecasts` | internal | XW-27 |

## Cross-cutting findings for other deliverables

1. **Work moved, not eliminated, is common and must be priced.** Examples:
   - recipient enrollment effort (XW-12, 13);
   - reliance risk on upstream identity (XW-01, 17);
   - network governance (XW-07);
   - auditor methodology change (XW-25);
   - platform concentration (XW-18).

   Each is flagged in the per-workflow "Moved" section for [`../07-adversarial-reviews/`](../07-adversarial-reviews/).
2. **Three workflows depend on counterpart adoption, not technology:** XW-07 (network), XW-20 (transfer protocol) and XW-13 (inbox). Their value is conditional on network formation, which E7 tests only partly; overlap is necessary but not sufficient.
3. **Every workflow keeps the parent's hard rules:**
   - requests are not instructions (CTL-001);
   - AI is flag-only (CTL-008);
   - the payment gate is internal (CTL-003);
   - loosening a control is material (CTL-010).

   No redesign required breaking one, which is itself evidence that the radical ideas live in *where and when* work happens, not in who holds authority.
