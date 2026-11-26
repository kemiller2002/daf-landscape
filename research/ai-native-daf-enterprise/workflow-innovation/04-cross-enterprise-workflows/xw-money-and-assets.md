# Cross-enterprise workflows: money, assets and the ledger (XW-11 to XW-16, XW-31)

Notation as in [xw-shared-capabilities.md](xw-shared-capabilities.md).

---

## XW-11 Daily netting disbursement with itemized remittance

- **Legacy departments spanned:** payments (check runs and ACH batches), accounting (cash reconciliation), donor services (attribution letters), and *recipient* finance teams.
- **Trigger:** the daily netting cut-off (a calendar event) over grants in `Approved` state, with payee profiles verified.
- **Linked innovations:** INN-09, INN-08, INN-07. **Maturity:** L1. The volume premise is supported by about 12.5 grants per recipient at Fidelity; the recipient-side benefit is unmeasured. **Experiments:** E3, E9, E11.

```mermaid
sequenceDiagram
  participant G as Grants (Approved)
  participant N as Netting job NEW
  participant PG as Payment gate
  participant B as Bank (CCD+/CTX)
  participant R as Recipient
  participant L as Ledger
  N->>G: select Approved grants by recipient (cut-off T)
  N->>PG: NettedPaymentProposed NEW (recipient, grant IDs[], total)
  PG->>PG: D: every grant Approved by Rule/Person; payee verified; caps; dual control on total
  PG->>B: PaymentInstructed (one payment, CTX addenda: grant IDs, donor-chosen recognition per grant)
  B-->>PG: PaymentSettled / PaymentReturned
  PG->>L: per-grant settlement postings (each grant remains a distinct distribution)
  B->>R: one credit + itemized remittance; also GET /v1/recipient-inbox (XW-13)
  Note over PG: a return reverts ALL grants in the netted payment to Approved-unpaid; re-netting only after profile re-verification
```

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | Netting cut-off → `NettedPaymentProposed` **NEW** | D | Batch(proposed) | internal | — | CTL-029 |
| 2 | Gate checks on each grant and on the total | D | Pass or `PaymentGateDenied` | internal | — | CTL-003, CTL-005 |
| 3 | `PaymentInstructed` with itemized addenda | D | Grants Released | internal `POST /v1/payments` | — | CTL-032, CTL-043 |
| 4 | `PaymentSettled` → per-grant `JournalPosted` | D | Grants Paid | — | — | CTL-015, CTL-018 |
| 5 | `PaymentReturned` → all grants revert; the profile is marked suspect | D, then H (payments specialist) if repeated | Grants Approved-unpaid | — | AG-18 explains | CTL-004 |

**Human interventions:**
- Dual control on netted totals above the threshold (H).
- Repeated returns go to a payments specialist (H). They are a possible hijack.

**Eliminated:** most per-grant payments; ACT-025 cover letters; ACT-028 batching *as a staffing convention* (netting is automatic); ACT-077 manual recipient reconciliation.

**Moved:**
- One return now affects several grants (blast radius), which is mitigated by a per-recipient cap.
- Recipients must read CTX addenda. If their bank strips addenda, attribution falls back to the recipient inbox (XW-13).

---

## XW-12 Recipient payee registry: enrollment and bank-detail change

- **Legacy departments spanned:** payments (payee setup), fraud, grants compliance (identity of the entity), and recipient development offices.
- **Trigger:** a recipient enrolls proactively, a first grant prompts enrollment, or a recipient requests a bank-detail change.
- **Linked innovations:** INN-07, INN-29, INN-01. **Maturity:** L1. **Experiments:** E3.

```mermaid
sequenceDiagram
  participant R as Recipient officer
  participant PR as Payee registry NEW
  participant AV as Account-validation provider
  participant PP as Passport
  participant F as Fraud (C5.2)
  R->>PR: enroll (EIN, officer identity, bank account, contacts, attestations)
  PR->>PP: EIN matches passport? officer authority evidence?
  PR->>AV: account ownership validation
  AV-->>PR: match/no-match
  PR->>PR: PayeeRegistryEnrollmentVerified NEW (D) or refer (H)
  R->>PR: change bank account
  PR->>F: PaymentProfileChanged → cooling-off; notify PRIOR contact out-of-band
  F->>F: AG-18 anomaly explanation (Cat. 2); D rules
  PR-->>PP: profile vN+1 active after cooling-off & verification
```

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | Enrollment submitted | D: EIN in passport; officer authority evidence; account validation | Profile(pending) | `POST /v1/payee-registry` **NEW** | AG-08 extracts documents | CTL-004 |
| 2 | `PayeeRegistryEnrollmentVerified` **NEW** | D, or H on mismatch | Profile(verified) | — | — | CTL-006 |
| 3 | Attestations: no goods or services for grants; accepts DAF grants (INN-29) | D: recorded | Passport attestation | `/v1/recipients/{id}/attestations` **NEW** | — | — |
| 4 | Change request → `PaymentProfileChanged` | D: cooling-off plus out-of-band verification to the prior contact | Profile(pending change) | `PATCH /v1/payee-registry/{id}` **NEW** | AG-18 | CTL-004, CTL-033 |
| 5 | Anomaly (change plus new officer plus large pending grants) | H: fraud analyst | Hold | `/v1/cases` | — | CTL-049 |

**Human interventions:** enrollment mismatches and suspicious changes (H, fraud judgment).

**Eliminated:** ACT-023 calling charities; ACT-070 positive-pay and payee setup done by hand per sponsor; most of ACT-024 checks, for enrolled recipients.

**Moved:** the enrollment burden moves to recipients. That is justified only if one enrollment serves many sponsors (XW-07 network) or many grants. For a single small grant it is a net *increase* in recipient work. Adversarial review must check this.

---

## XW-13 Recipient inbox: one place for every incoming DAF grant

- **Legacy departments spanned:** sponsor donor services (charity calls), payments, and recipient gift-processing offices.
- **Trigger:** `GrantApproved`, `PaymentInstructed` or `PaymentSettled` for an enrolled recipient.
- **Linked innovations:** INN-38, INN-10 (recipient-pull, as an option only), INN-08. **Maturity:** L0–L1. **Experiments:** E3.

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | `GrantApproved` → `RecipientInboxNoticePosted` **NEW**: amount, expected date, grant ID, donor-chosen recognition | D: anonymity choice applied | Inbox item | `GET /v1/recipient-inbox` **NEW** (recipient-authenticated) | — | CTL-043 |
| 2 | `PaymentSettled` → inbox item marked paid, with trace number | D | Paid | webhook to the recipient CRM | — | CTL-015 |
| 3 | Optional recipient-pull variant: a non-enrolled recipient claims to a verified account → `GrantClaimed` **NEW** | D: identity plus registry | Released | `POST /v1/recipient-inbox/{id}/claim` **NEW** | — | CTL-003, CTL-004 |
| 4 | Unclaimed after N days | D: escalate; H decides reissue or escheat path | Case | `/v1/cases` | — | CTL-044 |
| 5 | Recipient questions | P: AG-09 answers from state (grounded) | — | — | AG-09 (Cat. 3, read-only) | CTL-039 |

**Human interventions:** unclaimed or escheat decisions (H, under state law).

**Eliminated:** ACT-030 status inquiries from charities; ACT-025 letters; ACT-026 voiding and reissuing, for enrolled recipients.

**Moved:**
- Recipients adopt one portal or API. The adoption barrier is real (Chariot's DAFpay network is an incumbent on the donate side).
- The claim variant shifts payout initiation to the recipient, which risks unclaimed backlogs.

---

## XW-14 Complex asset: pre-underwriting, structured documents and a liquidation partner

- **Legacy departments spanned:** gift planning, complex-asset specialists, legal, investments, accounting (8283/8282), donor or advisor services.
- **Trigger:** a contribution intent for a non-standard asset class.
- **Linked innovations:** INN-11, INN-12, INN-13, INN-28. **Maturity:** L1. **Experiments:** E5, E6.

```mermaid
sequenceDiagram
  participant A as Advisor/attorney
  participant UW as Underwriting rules NEW
  participant AG7 as AG-07 asset dossier
  participant S as Complex-asset specialist
  participant LP as Liquidation partner (standing agreement)
  participant L as Ledger
  A->>UW: ContributionIntentDeclared (asset class, structured gift packet NEW)
  UW-->>A: IndicativeAcceptanceIssued NEW (D: class rules; docs list; known issues) or Refer
  A->>AG7: documents (appraisal, operating agreement, title)
  AG7-->>S: dossier + flags (liabilities, UBTI, 4943(e) holdings) (Cat. 2)
  S->>S: accept/decline (H; committee above threshold)
  S->>LP: LiquidationBidRequested NEW
  LP-->>S: bid
  S->>S: accept bid (H; conflicts checked)
  LP->>L: proceeds → ContributionSettled / NoncashAssetDisposed → 8282 tracking
```

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | Intent plus structured gift packet | D: class rules → `IndicativeAcceptanceIssued` **NEW** or refer | Case(indicative) | `POST /v1/asset-classes/{id}/underwriting` **NEW** | — | CTL-021 |
| 2 | Documents → dossier | P | Dossier | `/v1/documents` | AG-07, AG-08 (Cat. 2) | CTL-008 |
| 3 | Acceptance decision | **H**: specialist; committee above threshold | Accepted / Declined | `/v1/cases/{id}` | — | CTL-021, CTL-007 |
| 4 | Donee acknowledgment of Form 8283 | **H**: officer signature | Obligation | `/v1/documents` | — | CTL-022 |
| 5 | `LiquidationBidRequested` / `LiquidationBidAccepted` **NEW** | H: prudence and conflict check | Sale pending | partner API | — | CTL-042 |
| 6 | Proceeds → `ContributionSettled` (cash) or `NoncashAssetDisposed` | D | Ledger; 8282 obligation if within 3 years | — | — | CTL-022, CTL-015 |

**Human interventions:** acceptance, the 8283 signature, and sale approval (H). These are fiduciary and legal acts.

**Eliminated:** part of ACT-014, the repeated diligence on standard classes. The judgment itself is retained, and ACT-013 is automated.

**Moved:** underwriting-rule maintenance becomes specialist work. Price risk moves to partner bids, and a conflict-of-interest control is required.

---

## XW-15 Continuous close with controller attestation

- **Legacy departments spanned:** fund accounting, treasury, investment operations, controller, external audit.
- **Trigger:** each custodian, bank or rail feed arrival (continuous), plus a monthly checkpoint.
- **Linked innovations:** INN-22, INN-23, INN-20. **Maturity:** L3 for reconciliation logic (parent `reconcile`, tested); L1 for the operating model. **Experiments:** E4, E9.

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | Feed ingested → invariant evaluation (three-way) | D | Recon results | `/v1/reconciliation` | — | CTL-015, CTL-018 |
| 2 | `ReconciliationBreakDetected` | D: known-pattern auto-resolution | Break(open) or auto-closed with rule ID | — | — | CTL-016 |
| 3 | Unknown pattern | P: AG-06 triages and proposes a cause | Break with proposal | `/v1/cases` | AG-06 (Cat. 2) | CTL-008 |
| 4 | Resolution or write-off | H: controller; second approver above threshold | `ReconciliationBreakResolved` | `/v1/reconciliation/{id}` | — | CTL-016, CTL-006 |
| 5 | Month checkpoint → `ControllerAttestationSigned` **NEW** | H: controller reviews the variance pack | Period locked (reversing entries only afterwards) | `/v1/ledger/periods/{p}/attest` **NEW** | AG-19 narrates variances | CTL-048, CTL-019 |

**Human interventions:**
- Break resolution and write-offs (H).
- The monthly attestation (H). It restores the forced review the old close provided (Clarity AC-14).

**Eliminated:** ACT-038 manual reconciliation; ACT-039 the multi-day close project; ACT-041 PBC pulls.

**Moved:** feed-quality monitoring becomes an operational duty. A feed outage masks breaks, so freshness alerts are required (CTL-015).

---

## XW-16 Pipeline-based liquidity planning and seasonal buffer

- **Legacy departments spanned:** treasury, investment operations, grants operations, investment committee.
- **Trigger:** every `RecommendationSubmitted`, `ScheduledGrantDue`, `ContributionIntentDeclared` and `PositionChanged`, plus a daily forecast run.
- **Linked innovations:** INN-27, INN-37. **Maturity:** L2. Twin result: a 30-day custodian outage during the surge exhausts a 2% buffer (parent [digital twin](../../11-scenarios-and-validation/digital-twin.md)). **Experiments:** E6.

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | Pipeline events update the outflow forecast → `LiquidityForecastPublished` **NEW** | D: model | Forecast | `/v1/positions/forecast` **NEW** | — | CTL-023 |
| 2 | Buffer below the policy (≥30 days of peak outflow) → `PolicyBandBreached` | D | Breach | — | — | CTL-023 |
| 3 | Raise cash: `TradeInstructed` within the rebalancer's authority | D | Positions | internal | — | CTL-024 |
| 4 | Beyond authority or market disruption | H: CIO / investment committee | Playbook decision | `/v1/cases` | AG-16 proposes buffer recalibration (Cat. 2) | CTL-010 |

**Human interventions:** the committee sets the buffer parameters and decides on actions outside the playbook (H, fiduciary).

**Eliminated:** ACT-035 spreadsheet cash forecasting; ACT-068 manual sweeps.

**Moved:** the opportunity cost of a higher seasonal buffer is borne by investment returns. That trade-off is made explicit to the committee.

---

## XW-31 Custodian or key-vendor failover

- **Legacy departments spanned:** treasury, operations, IT, vendor management, donor services, board.
- **Trigger:** `CustodianUnavailable` from vendor telemetry, or a payment-rail outage or data-provider (IRS feed) failure.
- **Linked innovations:** INN-27, INN-18, plus parent CTL-035. **Maturity:** L2 (twin outage stresses; parent scenario SC-09 / SC-17). **Experiments:** E6, E9.

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | `CustodianUnavailable` → degraded-mode flag | D | Trading suspended; contributions queue | API-22 | — | CTL-035 |
| 2 | Grants funded from the cash buffer only; non-urgent grants deferred by policy | D: caps | Deferred list | — | — | CTL-029 |
| 3 | Rail outage → switch to secondary rail through the payment gate (same controls) | D | Rail = secondary | internal | — | CTL-003 |
| 4 | IRS feed stale → D-path blocked (refer) per the freshness SLO | D | Refers rise | — | — | CTL-011 |
| 5 | Outage beyond RTO → `CustodianFailoverActivated` **NEW**: activate the secondary cash custodian or bank line | H: CFO / COO; board notified | Secondary active | `/v1/positions` | AG-09 updates the status banner from state | CTL-036 |
| 6 | Recovery → backfill ingestion; reconciliation catch-up | D, H for breaks | Normal mode | — | AG-06 | CTL-015 |

**Human interventions:** activating failover and notifying the board (H). These are material counterparty decisions.

**Eliminated:** ad hoc incident coordination by email (part of ACT-080). It is replaced by runbooks tested through DR exercises.

**Moved:** a second custodian or bank line adds a contract and reconciliation stream. That is ongoing cost in exchange for resilience.
