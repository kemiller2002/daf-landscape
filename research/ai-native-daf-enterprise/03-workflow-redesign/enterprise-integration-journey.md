# Enterprise-wide integration journey (addendum §24)

This document follows one donor through every stage of the enterprise, and shows that the organization runs as a single system. Each stage below names the authoritative data, events, APIs, agents, exceptions, evidence and human authorization involved.

The executable proof of concept for this journey is [`models/Daf.Enterprise/Journey.fs`](../models/Daf.Enterprise/Journey.fs). It is an F# model with tests that runs the happy path and the main exception branches against in-memory adapters. Where this document and the code disagree, the code's tests are the specification and this document should be corrected.

**API families:** every route is under `/v1/`. The families are:

| Area | Families |
|---|---|
| Parties and access | `parties`, `accounts`, `privileges` |
| Contributions and investments | `contribution-intents`, `contributions`, `positions`, `investment-requests` |
| Grants | `recommendations`, `recipients`, `eligibility`, `grants`, `payments` |
| Books | `ledger`, `reconciliation` |
| Control and audit | `policies`, `decisions`, `evidence`, `cases`, `events` |

The API catalog in [`../04-enterprise-apis/`](../04-enterprise-apis/) is authoritative for contracts.

## Stage table

| # | Stage | Authoritative data (owner) | Events | APIs | Agents (category) | Exceptions | Evidence | Human authorization and why |
|---|---|---|---|---|---|---|---|---|
| 1 | **Donor acquisition** | Party (C1.1), referral source, Program (C5.4) | `PartyRegistered` | `POST /v1/parties` (via advisor platform or portal) | Discovery agent (Cat 2): education with cited content, including the "direct gift may be better" comparison | Unsuitable-donor signal (for example a non-itemizer with small gifts): the content says so | Content version served | None. Marketing is informational; no tax advice is given |
| 2 | **Onboarding** | Party, Account, Agreement, PrivilegeGrant | `IdentityVerified`, `AgreementAccepted`, `AccountOpened`, `PrivilegeGranted` | `POST /v1/accounts`, `POST /v1/privileges` | Identity-risk model (Cat 2, score → D threshold) | Identity-verification failure → case | IdP reference, agreement hash, consent | Only identity exceptions (H, client ops). Account opening is D |
| 3 | **Contribution** | ContributionIntent, Contribution | `ContributionIntentDeclared`, `ContributionReceived`, `ContributionSettled`, `AcknowledgmentIssued` | `POST /v1/contribution-intents`, `GET /v1/contributions/{id}` | Reconciliation agent (Cat 2) only for unmatched receipts | Orphan, sanctions hit, complex asset → WF-03 | Settlement reference, acknowledgment hash | Sanctions true match (sanctions officer): legal liability; complex assets (specialist) |
| 4 | **Custody** | Position (custodian is authoritative; C2.3 holds a mirror) | `PositionChanged` | `GET /v1/positions?account=` | — | Unexplained position change → critical incident | Custodian record hash | — |
| 5 | **Accounting** | JournalEntry, Unit/NAV (C4.1) | `NavStruck`, `FeeAccrued` | `GET /v1/ledger/accounts/{id}/entries` | — | Price tolerance breach → controller | Posting rule version, NAV calc hash | Price exceptions (controller): a valuation judgment |
| 6 | **Investment** | Pool, InvestmentRequest, TradeInstruction (C2.4) | `InvestmentRequested`, `TradeInstructed`, `PolicyBandBreached` | `POST /v1/investment-requests` | — (DD-007) | Out of mandate → deny | Pre-trade check record | IPS and committee parameters (H): fiduciary duty. Execution is D |
| 7 | **Grant recommendation** | Recommendation (C3.2) | `RecommendationSubmitted` | `POST /v1/recommendations` | Donor's own agent (external, delegated principal; WF-11); resolution agent (Cat 2) for name-only input | Ambiguous recipient → donor confirms | Request attribution (person or agent principal) | Donor confirmation where the privilege requires it (the donor's authority) |
| 8 | **Eligibility verification** | Recipient, EligibilityFact (C3.1); screening index (C5.2) | `RecipientResolved`, `EligibilityEvaluated`, `ScreeningCompleted`, `GrantFlagged` | `GET /v1/recipients/{ein}`, `POST /v1/eligibility/evaluations` | Benefit-risk agent (Cat 2, flag-only) | Stale data → refer; potential sanctions match → sanctions case | Decision records with source versions | Potential sanctions match (sanctions officer only) |
| 9 | **Authorization** | Grant, Decision, Approval (C3.3) | `GrantApproved` / `GrantDeclined` | `GET /v1/decisions/{id}`, `POST /v1/cases/{id}/decision` | Dossier preparation for exceptions (Cat 2) | Non-routine → exception case with SLA | Policy version; approver plus the evidence they viewed | Non-routine grants (specialist): §4966/§4967 judgment and manager liability. Routine grants are D (DD-004) |
| 10 | **Disbursement** | PaymentInstruction, Payment, Remittance (C3.4) | `PaymentInstructed`, `PaymentSettled`, `PaymentReturned` | `POST /v1/payments` (internal only; the payment gate), `GET /v1/grants/{id}` | — (Cat 5: no agent may call it) | Profile in cooling-off, cap exceeded → hold | Gate decision, rail settlement reference, remittance hash | Dual control above the payment limit (two humans): irreversibility and fraud risk |
| 11 | **Reconciliation** | ReconciliationResult (C4.2) | `ReconciliationBreakDetected` / `Resolved` | `GET /v1/reconciliation/breaks` | Break-triage agent (Cat 2) | Break above threshold → controller | Match statistics, resolution records | Write-offs (controller plus a second approver): they change the books |
| 12 | **Reporting** | Reports derived from the ledger (C4.4); Evidence (C4.5) | `DocumentationDelivered`, `RegulatoryDeadlineApproaching` | `GET /v1/accounts/{id}/statements`, `GET /v1/evidence?subject=` | Service agent (Cat 3) answers questions about statements | Consistency test failure blocks sign-off | Report hash, lineage query | Filing sign-off (officer): legal attestation |

## End-to-end sequence

```mermaid
sequenceDiagram
  autonumber
  actor Donor
  actor Advisor
  participant GW as API gateway (/v1)
  participant PTY as C1.1/C1.2 Party & Authorization
  participant INT as C2.1 Intake
  participant CUS as Custodian (EXT)
  participant SCR as C5.2 Screening
  participant LED as C4.1 Ledger
  participant INV as C2.4 Investments
  participant REC as C3.2 Recommendations
  participant ELG as C3.1 Registry/Eligibility
  participant BRA as Benefit-risk agent (Cat 2)
  participant DEC as C3.3 Decisioning (policy engine)
  participant CASE as C5.3 Cases
  participant PAY as C3.4 Payment gate
  participant BANK as Bank/rail (EXT)
  participant RCN as C4.2 Reconciliation
  participant EVD as C4.5 Evidence

  Advisor->>GW: POST /v1/parties (referral)
  Donor->>GW: POST /v1/accounts (agreement vN)
  GW->>PTY: verify identity, open account
  PTY-->>EVD: IdentityVerified, AgreementAccepted, AccountOpened
  Donor->>GW: POST /v1/privileges (advisor: view+recommend_investments)
  Donor->>GW: POST /v1/contribution-intents (100 sh XYZ)
  CUS->>INT: ContributionReceived (DTC, ref)
  INT->>SCR: screen donor
  SCR-->>INT: pass (list v)
  INT->>LED: ContributionSettled
  LED->>INV: units issued; allocation per instruction
  INV->>CUS: TradeInstructed (pre-trade check OK)
  LED-->>Donor: AcknowledgmentIssued (§170(f)(18) text)
  Donor->>GW: POST /v1/recommendations (EIN, $5,000, purpose)
  GW->>REC: RecommendationSubmitted (request)
  REC->>ELG: resolve + evaluate (facts fresh?)
  ELG-->>DEC: EligibilityEvaluated pass
  REC->>SCR: screen recipient
  SCR-->>DEC: ScreeningCompleted pass
  REC-)BRA: analyse purpose (async, flag-only)
  BRA--)DEC: no flag
  DEC->>DEC: policy vK: routine → GrantApproved
  alt any refer/flag
    DEC->>CASE: ExceptionCaseOpened (dossier, SLA)
    CASE-->>DEC: ExceptionCaseResolved (H, within authority)
  end
  DEC->>PAY: approved grant
  PAY->>PAY: profile verified, caps, balance → PaymentInstructed
  PAY->>BANK: payment + remittance (grant id)
  BANK-->>PAY: PaymentSettled
  PAY->>LED: post settlement
  BANK-->>RCN: settlement record
  RCN->>RCN: match by idempotency key → matched
  LED-->>EVD: decisions, gate, settlement, match → evidence
  Donor->>GW: GET /v1/grants/{id} (Paid, Reconciled)
```

## Data contract sketches

These sketches show the required fields only. The canonical schemas are in [`../04-enterprise-apis/`](../04-enterprise-apis/).

**1. `RecommendationSubmitted` (request, not instruction)**
```json
{
  "eventId": "01JD3X…", "eventType": "grant.recommendation.submitted", "schemaVersion": 1,
  "subject": {"type": "Recommendation", "id": "REC-7f3c"},
  "effectiveAt": "2026-12-28T15:02:11Z", "recordedAt": "2026-12-28T15:02:11Z",
  "actor": {"kind": "Person", "id": "PTY-donor-1", "authorityRef": "PG-0091"},
  "correlationId": "J-2026-000184", "idempotencyKey": "portal-5c1e-…",
  "payload": {
    "accountId": "ACC-1042",
    "recipient": {"ein": "13-1234567"},
    "amount": {"value": "5000.00", "currency": "USD"},
    "purpose": {"codes": ["general_support"], "text": null},
    "recognition": "full_contact",
    "requestedBy": {"kind": "Person", "id": "PTY-donor-1"},
    "onBehalfOf": null
  }
}
```

**2. `EligibilityEvaluated` (decision record with source provenance)**
```json
{
  "eventType": "grant.eligibility.evaluated", "subject": {"type": "Grant", "id": "GRT-91a0"},
  "actor": {"kind": "Rule", "id": "eligibility.public_charity", "authorityRef": "POL-ELIG@12"},
  "payload": {
    "outcome": "pass",
    "facts": [
      {"type": "pub78_listed", "value": true, "source": "IRS Pub 78", "sourceVersion": "2026-12-08", "retrievedAt": "2026-12-09T03:00:00Z", "hash": "sha256:…"},
      {"type": "revoked", "value": false, "source": "IRS Auto-Revocation List", "sourceVersion": "2026-12-08"},
      {"type": "foundation_code", "value": "15", "source": "IRS EO BMF", "sourceVersion": "2026-11"}
    ],
    "freshnessSloMet": true
  }
}
```

**3. `GrantApproved` (sponsor decision; the only source of a grant instruction)**
```json
{
  "eventType": "grant.approved", "subject": {"type": "Grant", "id": "GRT-91a0"},
  "actor": {"kind": "Rule", "id": "grant.routine_approval", "authorityRef": "POL-GRANT@7"},
  "causationId": "evt-screening-…", "correlationId": "J-2026-000184",
  "payload": {
    "decisionType": "D",
    "gates": {"eligibility": "pass", "sanctions": "pass", "flags": [], "threshold": "within", "balance": "sufficient"},
    "earmark": {"units": "41.2235", "pool": "POOL-BAL", "nav": "121.29"},
    "humanApproval": null
  }
}
```

**4. `PaymentInstructed` (payment gate output)**
```json
{
  "eventType": "payment.instructed", "subject": {"type": "Payment", "id": "PAY-33d2"},
  "actor": {"kind": "Rule", "id": "payment.gate", "authorityRef": "POL-PAY@4"},
  "idempotencyKey": "GRT-91a0:1",
  "payload": {
    "grantIds": ["GRT-91a0"], "rail": "ACH_CCD_PLUS",
    "payeeProfile": {"id": "PP-5521", "verifiedAt": "2026-03-02", "coolingOffEnds": null},
    "amount": {"value": "5000.00", "currency": "USD"},
    "remittance": {"grantId": "GRT-91a0", "donorShare": "full_contact", "purpose": "general_support"},
    "checks": {"fanOutCap": "ok", "dualControlRequired": false}
  }
}
```

**5. `ExceptionCaseResolved` (human decision within delegated authority)**
```json
{
  "eventType": "case.resolved", "subject": {"type": "ExceptionCase", "id": "CASE-2207"},
  "actor": {"kind": "Person", "id": "STAFF-grants-02", "authorityRef": "DELEG-GC-SPEC@3"},
  "payload": {
    "caseType": "benefit_risk", "subject": {"type": "Grant", "id": "GRT-88f1"},
    "decision": "approve_with_condition",
    "condition": "Recognition limited to name listing; no event tickets",
    "flagsCleared": [{"flagId": "FLG-77", "clearedBy": "STAFF-grants-02"}],
    "evidenceViewed": ["DOS-1182", "AGR-ticket-terms-2026"],
    "relatedPartyCheck": "none", "slaMet": true
  }
}
```

Note the `flagsCleared[].clearedBy` field. It is always a person or a rule ID, and schema validation rejects an agent ID there (DD-005).

## Where the conventional enterprise breaks this journey

| Stage | Conventional seam | What carries the journey instead |
|---|---|---|
| 3→5 | The contribution is re-discovered by operations, accounting and investment operations from separate files | One `ContributionSettled` event drives all three |
| 7→9 | The recommendation waits in a review queue regardless of risk | Exception-only routing |
| 8 | A per-grant lookup at a point in time | Continuous eligibility; WF-09 reaches back into in-flight grants |
| 10→11 | Payments reconciled by hand because remittance lacks identifiers | Idempotency key carried end-to-end |
| 12 | Reports assembled from extracts | Reports generated from the ledger with lineage |
