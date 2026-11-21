# Event catalog and event-driven operating model

**Catalog data:** [`events.csv`](events.csv) has 58 business events (50 original plus 8 added after cross-deliverable review: `PaymentGateDenied`, `DonorConfirmationRequested`/`Received`, `ScheduledGrantDue`, `KillSwitchActivated`, `JournalPosted`, `CharityEligibilityHoldApplied`, `PostPaymentReviewOpened`). Each row gives the producer, consumers, authoritative state change, required controls, exception handling, audit evidence, and whether the event can lead to money movement. It covers every example in addendum §20, as shown below.

| Addendum §20 example | Catalog event(s) |
|---|---|
| A contribution is received or settles | `ContributionReceived`, `ContributionSettled` |
| A donor changes an authorized instruction | `DonorInstructionChanged`, `PrivilegeGranted` / `PrivilegeRevoked` |
| A charity's eligibility changes | `CharityEligibilityChanged`, `SanctionsListUpdated` |
| A grant recommendation is submitted | `RecommendationSubmitted` |
| An investment position changes | `PositionChanged`, `PolicyBandBreached` |
| A payment fails | `PaymentReturned` |
| A reconciliation discrepancy occurs | `ReconciliationBreakDetected` / `Resolved` |
| A compliance policy changes | `ComplianceObligationChanged`, `PolicyPublished` |
| A donor requests documentation | `DocumentationRequested` / `Delivered` |
| A regulatory reporting deadline approaches | `RegulatoryDeadlineApproaching` |

## 1. Event envelope

```
EventId          UUIDv7 (time-ordered)
EventType        e.g. "grant.approved"
SchemaVersion    integer; consumers declare supported versions
Subject          entity type + id (e.g. Grant/G-…)
EffectiveAt      when it is true in the world
RecordedAt       when the enterprise recorded it
Actor            {kind: Rule|Person|Agent|External, id, authorityRef}
CausationId      the event/command that directly caused this
CorrelationId    the business journey (e.g. one recommendation end-to-end)
IdempotencyKey   producer-supplied; unique per (producer, intent)
PolicyRef        policy id@version when a decision is involved
PayloadHash      SHA-256 of canonical payload
Payload          typed per EventType
```

## 2. Delivery and processing guarantees

| Concern | Mechanism |
|---|---|
| No lost events | Transactional outbox. The state change and the event are written in the same database transaction, and a relay publishes from the outbox. |
| Duplicates | At-least-once delivery. Every consumer is idempotent on `(EventId)`, and every command on `(IdempotencyKey)`. Payment instructions carry the rail-level idempotency key, so a retried instruction cannot pay twice. |
| Ordering | Ordered per `Subject`. Cross-subject ordering is never assumed; workflows wait on explicit conditions, not on arrival order. |
| Replay | Projections are rebuildable from the ledger. Replays run against **side-effect-free consumers only**. Consumers with external side effects (payments, emails, custodian orders) record "effect issued" markers, so a replay does not re-issue effects (replay protection). |
| Long-running processes | Durable workflows (state machines persisted per correlation). Timers, such as SLA, cooling-off and deadlines, are durable state, not in-memory. |
| Polling | Avoided internally. Externally, where custodians or rails only offer files, a single ingestion adapter converts files into events, so the rest of the enterprise stays event-driven. |

## 3. How one event drives the enterprise: `ContributionSettled`

```mermaid
sequenceDiagram
  participant Cust as Custodian (EXT)
  participant Intake as C2.1 Intake
  participant Scr as C5.2 Screening
  participant Led as C4.1 Ledger
  participant Inv as C2.4 Investments
  participant Liq as C2.5 Liquidity
  participant Ack as Acknowledgment
  participant Svc as C1.4 Servicing
  participant Ev as C4.5 Evidence
  Cust->>Intake: settlement file / webhook
  Intake->>Intake: match to ContributionIntent (reference)
  Intake->>Scr: screen donor + source (list vN)
  Scr-->>Intake: pass (decision record)
  Intake->>Led: ContributionSettled (event)
  Led->>Led: post journal (rule vK); issue units at NAV
  Led-->>Inv: units credited
  Inv->>Inv: apply standing allocation (D); TradeInstructed if needed
  Led-->>Liq: cash/positions forecast update
  Led-->>Ack: generate acknowledgment (schema-tested)
  Ack-->>Svc: AcknowledgmentIssued → notify donor & advisor
  Led-->>Ev: control evidence: match, screen, posting, ack
```

The conventional alternative would have the contribution separately "discovered" by operations (matching), accounting (posting), investment operations (allocation), donor services (letter) and compliance (screen), each from its own report or file. Here **one verified fact produces each downstream effect once, with one correlation ID**.

## 4. Preventing uncontrolled cascades

Event-driven systems that include AI agents can loop or amplify. Controls:

1. **Agents consume events but cannot emit authoritative events.** An agent's output is an `AgentRunCompleted` event carrying *proposals* or *flags*. Only deterministic services and authorized humans emit state-changing events such as `GrantApproved` or `PaymentInstructed`.
2. **Causation-depth limit.** Any event whose causation chain exceeds a configured depth without a human or deterministic checkpoint is quarantined. The PoC enforces a depth of 8.
3. **Money-movement fan-out limits.** Policy-defined caps per window: payments per account per day, total value per recipient per day, and enterprise-wide payment volume against forecast. Breaching a cap holds the excess and opens a case. It does not fail silently, and it does not keep paying.
4. **Circuit breakers per consumer.** Error or flag rates above baseline trip the breaker. The workflow degrades to the human queue; it does not auto-approve.
5. **Eligibility and sanctions changes block but never release.** A `CharityEligibilityChanged` event can hold payments automatically. Releasing them requires a fresh evaluation under policy.
6. **Kill switches.** There is a per-agent kill switch and an enterprise "payments pause" switch. Both are human-operated and recorded, and both are tested in scenarios.

## 5. Event-driven vs scheduled

The design rejects polling as the integration pattern but keeps **calendar events** as first-class producers:
- `RegulatoryDeadlineApproaching` (from the obligation register);
- daily NAV;
- the inactivity stage clock.

Calendar facts are business events too, and modeling them as events keeps one mechanism.
