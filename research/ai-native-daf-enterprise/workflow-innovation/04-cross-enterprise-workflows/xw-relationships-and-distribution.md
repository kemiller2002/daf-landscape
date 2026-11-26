# Cross-enterprise workflows: relationships, distribution and donor journeys (XW-17 to XW-23)

Notation as in [xw-shared-capabilities.md](xw-shared-capabilities.md).

---

## XW-17 Continuous onboarding: account at first intent, with upstream KYC attestation reuse

- **Legacy departments spanned:** marketing (applications), onboarding, compliance (KYC), contributions, donor services.
- **Trigger:** a donor or advisor declares a first contribution intent. No application exists.
- **Inversion applied:** *what if the donor never completed a form?*
- **Linked innovations:** INN-25, INN-24, INN-23, INN-16. **Maturity:** L1. **Experiments:** E5.

```mermaid
sequenceDiagram
  participant D as Donor (via advisor platform or direct)
  participant ID as Identity (XW-01)
  participant AC as Accounts (C1.1)
  participant IN as Intake
  participant P as Policy
  D->>ID: attestation from custodian/identity wallet (or provider check)
  ID-->>AC: IdentityAttestationAccepted NEW
  D->>AC: accept agreement vN (one screen)
  AC->>AC: AccountOpened (minimum data: identity, agreement, contact)
  D->>IN: ContributionIntentDeclared (reference issued)
  Note over AC: later decisions request data just-in-time: successor at first grant >$X or at 12 months; investment selection at settlement (default pool otherwise); advisor delegation when advisor first acts
  AC->>P: DataNeeded NEW (field, reason, deadline) → donor prompt
```

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | `IdentityAttestationAccepted` **NEW** or `IdentityVerified` | D | Party(assured) | `POST /v1/attestations/identity` **NEW** | — | CTL-033 |
| 2 | `AgreementAccepted` | D: E-SIGN consent recorded | Agreement bound | `/v1/accounts` | — | — |
| 3 | `AccountOpened` with the minimal profile | D | Account(active, minimal) | `POST /v1/accounts` | — | CTL-006 |
| 4 | `ContributionIntentDeclared` | D | Intent | `/v1/contribution-intents` | — | CTL-021 |
| 5 | `DataNeeded` **NEW**: a just-in-time request triggered by policy (successor, investment choice, privileges) | D: policy declares which decisions need which fields | Pending data item | `/v1/parties/{id}/preferences` **NEW** | AG-11 explains why the data is needed (Cat. 2) | CTL-039 |
| 6 | Missing data at a decision point | D: default (for example the default pool) or block | — | — | — | — |

**Human interventions:** none routinely. Identity mismatches go to client operations (H).

**Eliminated:** ACT-005 forms; ACT-006 re-keying; ACT-009 welcome kits; most of ACT-007.

**Moved:**
- Data collection is spread over time, which creates a risk of incomplete records at critical moments, such as no named successor at the donor's death.
- This is mitigated by a deadline-based `DataNeeded` with escalation. Adversarial review should test the death-before-successor case.

---

## XW-18 Advisor-embedded, invisible DAF

- **Legacy departments spanned:** sales and wholesaling, advisor services, onboarding, investments (advisor-managed), donor services, reporting.
- **Trigger:** an advisor acts inside their own wealth platform (an embed session or partner API call).
- **Contrarian hypothesis:** *advisors become the primary interface while the DAF platform stays invisible.*
- **Linked innovations:** INN-15, INN-16, INN-24. **Maturity:** L2. The distribution premise rests on the RCF–Ren spine of about 11 wealth-firm programs and on channel-led growth [I]. Acceptance is untested. **Experiments:** E5, E11 (CAC sensitivity).

```mermaid
sequenceDiagram
  participant ADV as Advisor in wealth platform
  participant WP as Wealth platform (partner)
  participant GW as API gateway (mTLS, partner scopes)
  participant DAF as Sponsor services
  ADV->>WP: "open DAF for client" inside planning tool
  WP->>GW: AdvisorEmbedSessionStarted NEW (partner token + advisor identity)
  GW->>DAF: XW-17 continuous onboarding with custodian KYC attestation
  DAF-->>WP: account + delegation (advisor: view, recommend, manage within mandate; fee cap)
  ADV->>WP: recommend grant / move assets
  WP->>DAF: RecommendationSubmitted / InvestmentRequested (requests only)
  DAF->>DAF: Policy.decide; mandate checks (D)
  DAF-->>WP: webhooks: positions, grant status, statements (projections)
```

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | `AdvisorEmbedSessionStarted` **NEW** | D: partner scope, advisor identity | Session | `POST /v1/embed/sessions` **NEW** | — | CTL-034 |
| 2 | Account via XW-17; `PrivilegeGranted` to the advisor with fee cap and mandate | D; donor consent captured in the embed flow | Delegation | `/v1/privileges` | — | CTL-025, CTL-006 |
| 3 | `InvestmentRequested` → mandate check → `TradeInstructed` | D | Positions | `/v1/investment-requests` | — | CTL-023 |
| 4 | `RecommendationSubmitted` → policy | D / H | Grant | `/v1/recommendations` | AG-10 advisor copilot drafts (Cat. 2) | CTL-001 |
| 5 | Position and grant feeds into the advisor's systems | D | Projections | `/v1/events` webhooks | — | CTL-034 |
| 6 | Advisor fee accrual within the cap | D | Fee | `/v1/fees` | — | CTL-025 |

**Human interventions:**
- Partnerships approve each platform integration (H).
- Mandate breaches beyond tolerance go to the CIO (H).

**Eliminated:** ACT-004 wholesaling; ACT-056 LOAs; ACT-034 after-the-fact trade review; most advisor re-keying.

**Moved:**
- The donor experience is controlled by the platform. The sponsor brand recedes, and with it the direct donor relationship.
- Platform concentration risk.
- The proposed §4966 rule on personal investment advisers is *proposed only*, but it would change the advisor's legal status if finalized.

---

## XW-19 Donor-side AI agent delegation lifecycle

- **Legacy departments spanned:** donor services, fraud, compliance, IT security.
- **Trigger:** a donor authorizes a personal AI agent, which later submits requests.
- **Linked innovations:** INN-26, INN-16. **Maturity:** L3. Parent PoC INV-A6 is tested: confirmation above the cap, undelegated agents rejected, only the donor delegates. **Experiments:** parent tests; E10 for anomaly classification.

```mermaid
sequenceDiagram
  participant DN as Donor
  participant AZ as Authorization (C1.2)
  participant AGT as Donor's agent (external principal)
  participant I as Intake
  participant F as Fraud
  DN->>AZ: PrivilegeGranted (agent principal, scope=recommend, confirm_above=$1,000, expiry)
  AGT->>I: RecommendationSubmitted (ViaAgent)
  alt amount ≤ cap
    I->>I: Submitted → policy (D)
  else amount > cap
    I->>DN: DonorConfirmationRequested (prior channel)
    DN->>I: DonorConfirmationReceived (step-up auth)
  end
  F->>F: velocity/pattern rules; AG-18 explains anomalies
  DN->>AZ: PrivilegeRevoked (immediate token revocation)
```

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | `PrivilegeGranted` (agent principal; caps; expiry) | D: only the donor may delegate | Delegation | `/v1/privileges` | — | CTL-034 |
| 2 | `RecommendationSubmitted` (via agent) | D: delegation exists; amount vs cap | Submitted or AwaitingDonorConfirmation | `/v1/recommendations` | — | CTL-001 |
| 3 | `DonorConfirmationRequested` / `Received` | D: only the delegating person; step-up | Submitted | `/v1/recommendations/{id}/confirmation` | — | CTL-033 |
| 4 | Velocity and anomaly rules | D; P explanation | Hold if rule hit | — | AG-18 (Cat. 2) | CTL-029, CTL-049 |
| 5 | `PrivilegeRevoked` | D | Tokens revoked | `/v1/privileges/{id}` | — | CTL-034 |

**Human interventions:**
- The donor confirms large requests, as delegating principal rather than staff.
- A fraud analyst handles holds (H).

**Eliminated:** credential-sharing workarounds, which sponsor terms ban (EV-122). Shared credentials have no ACT; they are an unsafe current practice.

**Moved:** social-engineering risk moves to the donor's confirmation channel, which is mitigated by the prior-channel requirement.

---

## XW-20 DAF transfer protocol (ACATS-like), with history

- **Legacy departments spanned:** donor services (sending and receiving), grants (transfer as a grant), investments (liquidation), accounting, compliance — at two sponsors.
- **Trigger:** the receiving sponsor submits a transfer request on the donor's behalf. That is the ACATS pattern: the receiving side initiates.
- **Linked innovations:** INN-17, INN-18. **Maturity:** L1. It requires counterpart adoption; the open grant record v0.1 exists as a draft. **Experiments:** E8.

```mermaid
sequenceDiagram
  participant RS as Receiving sponsor
  participant P as Transfer protocol hub NEW
  participant SS as Sending sponsor
  RS->>P: TransferInitiated NEW (donor attestation, account ids, in-kind or cash, receiving sponsor EIN)
  P->>SS: TransferRequestReceived NEW
  SS->>SS: D: receiving sponsor eligible public charity sponsor; account validated; no holds
  SS->>SS: GrantApproved (transfer is a grant; sponsor decision) — H if policy requires
  SS->>P: TransferAssetsDelivered NEW (cash or in-kind positions) + HistoryPackageDelivered NEW (open grant record export, signed)
  P->>RS: assets + history
  RS->>RS: ContributionSettled; history imported (read-only provenance)
  P->>P: SLA clock (e.g., T+5 business days design target [A])
```

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | `TransferInitiated` **NEW** at the receiving sponsor | D: donor identity, consent | Transfer(requested) | `POST /v1/transfers` **NEW** | — | CTL-033 |
| 2 | `TransferRequestReceived` **NEW** at the sending sponsor | D: eligibility of the receiving sponsor (passport) | Under review | `/v1/transfers/{id}` **NEW** | — | CTL-011 |
| 3 | `GrantApproved` (transfer grant) | D, or H per policy (for example large or contested) | Grant | `/v1/grants` | — | CTL-001, CTL-045 |
| 4 | `TransferAssetsDelivered` **NEW**, in kind where both sides support the pool | D | Positions out / in | internal | — | CTL-002, CTL-015 |
| 5 | `HistoryPackageDelivered` **NEW** (signed open grant record) | D: schema and signature | History imported | `GET /v1/exports/event-log` **NEW** | — | CTL-035 |

**Human interventions:** sending-sponsor approval for policy cases (H). The sending sponsor retains the legal decision.

**Eliminated:** ACT-055 the manual outbound transfer; cash liquidation (where in kind is permitted); loss of history.

**Moved:** sponsors must maintain protocol conformance. Incumbents' asset-fee incentive opposes this (industry report §3), so adoption is the barrier, not technology.

---

## XW-21 Spend-down horizon and charitable defaults

- **Legacy departments spanned:** donor services, grants, program staff (inactivity), investments (liquidity), philanthropic advising.
- **Trigger:** at opening, or at any time, a donor optionally selects a horizon, a recurring plan, or a charitable default. A calendar event fires each period.
- **Contrarian:** *the DAF as a plan with an end date rather than an indefinite account.*
- **Linked innovations:** INN-19, INN-33, INN-27. **Maturity:** L1. The problem is evidenced (22% of accounts made no grants in 2020–22; median three-year payout 9%, EV-015); the mechanism is untested. **Experiments:** desk analysis plus E6 for the liquidity effect.

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | `SpendDownPlanAdopted` **NEW** (horizon, cadence, default recipients or causes) | D: validate recipients against passports | Plan | `POST /v1/schedules` **NEW** | AG-11 helps the donor explore options (Cat. 2, no tax advice) | CTL-039 |
| 2 | `ScheduledGrantDue` each period | D | Recommendation instance | — | — | CTL-001 |
| 3 | Policy evaluation as usual | D / H | Grant | `/v1/grants` | — | CTL-011 |
| 4 | `AccountInactivityThresholdReached` with no plan → nudges per policy | D | Stage | — | — | — |
| 5 | Final inactivity stage → charitable default (per agreement) | **H**: program officer | Default grants | `/v1/cases` | — | CTL-045 |

**Human interventions:** the charitable default distribution (H). It overrides advisory expectations and must follow the agreement.

**Eliminated:** ACT-074 inactivity letters done by hand, now event-driven. A dormant-capital function is *created* where none existed.

**Moved:** revenue under asset-based fees declines as assets are granted out. The incentive conflict is explicit, which makes this a differentiator only for mission-driven sponsors.

---

## XW-22 Year-end surge smoothing with execution windows

- **Legacy departments spanned:** grants operations, grants compliance, payments, donor services, HR (temporary staff).
- **Trigger:** in October to December, donors submit year-end recommendations, and the system offers execution windows.
- **Linked innovations:** INN-37, INN-03, INN-28. **Maturity:** L1. The twin shows 34 days over SLA at the surge when staffed for the average. **Experiments:** E6.

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | November pre-clear: passports refreshed and determinations renewed for last year's December recipients | D, H for renewals | Passports current | XW-03, XW-08 | AG-04 | CTL-047 |
| 2 | `RecommendationSubmitted` with `ExecutionWindowAssigned` **NEW** (donor chooses "by Dec 31" or "any time in Q1") | D: forecast specialist load | Grant scheduled | `/v1/recommendations` (window field **NEW**) | — | — |
| 3 | Routine grants execute immediately regardless of window | D | Paid | — | — | CTL-003 |
| 4 | Exceptions are leveled across the window; overflow goes to the shared pool (XW-10) | D routing | Case | `/v1/cases` | — | CTL-046 |

**Human interventions:** exceptions, as usual.

**Eliminated:** temporary year-end staffing (part of ACT-071).

**Moved:** some donors wait longer for non-routine grants, with consent. Grant timing does not affect the donor's deduction, which was taken at contribution. The communication must be accurate (CTL-039).

---

## XW-23 Zero-ticket servicing

- **Legacy departments spanned:** call center, donor services, advisor services, grants operations (status), finance (statements).
- **Trigger:** state changes are pushed proactively. Questions are answered from state.
- **Inversion applied:** *what if no ticket queue existed?*
- **Linked innovations:** INN-14, INN-38. **Maturity:** L1. The contact-mix premise is unmeasured (GAP-006). **Experiments:** E6.

**Sequence:**

| # | Event | Decision | State change | API | Agent | Controls |
|---|---|---|---|---|---|---|
| 1 | Any donor-relevant event → notification per preferences | D | Notice | `/v1/events` webhooks, notifications | — | — |
| 2 | Donor question → grounded answer from the state snapshot plus approved clauses | P (grounded) | — | API-02 / API-10 read | AG-09 (Cat. 3: templated sends, read-only) | CTL-039 |
| 3 | Answer needs a change (address, successor) → self-service with step-up | D | Profile | `/v1/parties` | — | CTL-033 |
| 4 | Dissatisfaction or complaint signal → `ExceptionCaseOpened` (service recovery) | D routing; H resolves | Case | `/v1/cases` | — | CTL-040 |
| 5 | QA sampling of answers | H | QA findings | — | — | CTL-040 |

**Human interventions:** service recovery, goodwill credits and complaints (H).

**Eliminated:** ACT-030; ACT-051 routine phone and email; ACT-052 statement mailing; ACT-053 profile changes done by hand.

**Moved:** donors who prefer people may experience this as reduced access. A guaranteed human path is retained as a design requirement.
