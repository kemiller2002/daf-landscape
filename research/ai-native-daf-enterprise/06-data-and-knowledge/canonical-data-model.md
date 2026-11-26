# Canonical enterprise data model

**Status:** conceptual model, 2026-11-20. It is implemented as F# types in [`../models/Daf.Enterprise/Domain.fs`](../models/Daf.Enterprise/Domain.fs) for the reference proof of concept. It is compatible with the repository's draft open grant record ([`standards/daf-grant-record/schema-v0.1.json`](../../../standards/daf-grant-record/schema-v0.1.json)); the projection mapping is in §6.

## 1. Principles

1. **The event ledger is the system of record for change; entities are projections.** Every entity state is derivable by replaying the events that touched it. Corrections are new events (reversals or amendments), never in-place edits.
2. **One authoritative owner per entity.** The owning capability is the only writer. Everyone else reads a projection or subscribes to events.
3. **Bitemporal where it matters.** Financial and eligibility facts record:
   - *effective time*: when it was true in the world, for example gift completion date or IRS revocation date;
   - *recorded time*: when the enterprise learned it.

   This is required for questions like "what did we know when we approved this grant?", which is exactly what an auditor or an IRS examiner asks.
4. **Provenance on every external fact.** Each fact from outside (IRS BMF row, OFAC list entry, custodian confirmation, price) carries a source identifier, the source's version or date, retrieval time and content hash.
5. **Policy versions are data.** Every decision references the policy version and rule ID that produced it. Policies are immutable once published, and new versions supersede old ones.
6. **Requests are not instructions.** `Recommendation`, `InvestmentRequest` and `TransferRequest` are donor- or advisor-side entities. `GrantInstruction`, `TradeInstruction` and `PaymentInstruction` are sponsor-side, and only exist with a `Decision`. This is the data-model form of the exclusive-control requirement (O-03).
7. **Minimize and partition personal data.** Identity attributes live in the Party vault. Operational records reference a `PartyId`, and analytics use pseudonymous keys.

## 2. Entity catalog

| Entity | Description | Authoritative owner (capability) | Key attributes | Temporal? |
|---|---|---|---|---|
| **Party** | Person or organization: donor, advisor, successor, institution, staff, agent principal | C1.1 | PartyId, kind, verified identity reference, assurance level | Versioned |
| **Relationship** | Typed edge between parties (spouse, family member, controls entity, investment advisor of, employee of, board member of) | C1.1 | from, to, type, source (declared/derived), effective period | Bitemporal |
| **Sponsor** | The sponsoring organization (one, or many in the infrastructure model) | C5.4 | EIN, legal name, policy set reference | Versioned |
| **Program** | A branded program under a sponsor (for example a wealth firm's DAF) | C5.4 | sponsor, distribution partner, fee schedule, investment menu | Versioned |
| **Account (Fund)** | The donor-advised fund | C1.1 / C4.1 | AccountId, program, account type, status, agreement version | Versioned |
| **PrivilegeGrant** | Who may do what on an account (recommend grants, recommend investments, view, act as agent) | C1.2 | grantee party, scope, limits, expiry, consent event | Bitemporal |
| **Agreement** | A versioned program agreement or policy disclosure text | C5.1 | version, hash, effective dates | Immutable |
| **ContributionIntent** | A donor's declared upcoming contribution, with a unique reference | C2.1 | account, asset descriptor, expected quantity, reference | Lifecycle |
| **Contribution** | A completed gift | C2.1 | intent, settlement evidence, completed-gift date, book value, valuation method | Bitemporal |
| **Asset** | An instrument or property: security, crypto asset, real property, entity interest | C2.2 | identifier scheme, classification, acceptance policy class | Versioned |
| **Position** | Holdings by pool, account and custody account | C2.3 (mirror of the custodian) | quantity, cost basis, custody reference | Bitemporal |
| **Pool / Portfolio** | Investment pool or model, with targets and bands | C2.4 | IPS reference, targets, bands, manager | Versioned |
| **InvestmentRequest → TradeInstruction** | Donor or advisor request → sponsor-approved order | C2.4 | decision reference, pre-trade check results | Lifecycle |
| **Unit / NAV** | Unit price per pool per valuation date | C4.1 | pool, date, NAV, method version | Immutable per date |
| **Recipient** | A charitable or other recipient organization | C3.1 | EIN or foreign identifier, legal name, aliases, payment profile reference | Versioned |
| **EligibilityFact** | Status fact from a source: Pub 78 listing, BMF foundation code, revocation, OFAC listing, equivalency determination | C3.1 | recipient, fact type, value, source and version, effective date | Bitemporal |
| **Determination** (added 2026-11-21) | A reusable judgment about a recipient: an equivalency determination, a fiscal-sponsor host review or a new-organization review. Not used for expenditure responsibility, which is per grant (REG-002) | C3.3 (grants compliance) | recipient, type (ED / FS-host / new-org), scope, valid from/to, invalidation triggers, author (person), evidence | Bitemporal |
| **PaymentProfile** | Verified rail endpoint for a recipient | C3.4 | rail, account token (never the raw number in the operational store), verification evidence, change cooling-off end | Versioned |
| **Recommendation** | Donor or advisor grant request | C3.2 | account, recipient candidate, amount, purpose, restrictions, recognition, channel, requesting party (incl. agent principal) | Lifecycle |
| **Grant** | The sponsor's grant | C3.3 | recommendation, decision, purpose, restriction, ER requirement | Lifecycle (state machine) |
| **PaymentInstruction / Payment** | Instruction to a rail and its settlement | C3.4 | grant(s), rail, amount, idempotency key, settlement reference, return code | Lifecycle |
| **Remittance** | Machine-readable advice to the recipient | C3.4 | grant ID, donor information per anonymity choice, purpose | Immutable |
| **Fee / Charge** | Computed fees: sponsor, advisor, partner share | C4.3 | schedule version, basis, period | Immutable per period |
| **JournalEntry** | Double-entry posting derived from events | C4.1 | debits/credits, source event, posting rule version | Immutable |
| **ReconciliationResult** | Match or break between internal and external records | C4.2 | sources compared, keys, status, aging | Lifecycle |
| **Policy** | A versioned rule set: eligibility, thresholds, acceptance, fees, routing, agent permissions | C5.1 | ID, version, rules, approval reference, back-test result reference | Immutable versions |
| **Decision** | Output of any gate: pass/flag/refer/deny/approve | Issuing capability | subject, decision type (D/P/H), actor (rule or person or model), policy version, inputs snapshot hash, rationale, evidence links | Immutable |
| **Flag** | A risk indicator raised by a rule or model | C5.2 / C3.3 | subject, code, raised by, severity, cleared by (human or rule ID; **never a model**) | Lifecycle |
| **ExceptionCase** | Human work item | C5.3 | subject, flags, SLA, assignee, delegated authority required, outcome decision | Lifecycle |
| **Approval** | Human authorization within delegated authority | C5.4 | approver, authority reference, decision reference, evidence viewed | Immutable |
| **Obligation** | A machine-readable legal or regulatory requirement | C5.1 / GC | citation, scope, control references, status (current law or proposed) | Versioned |
| **Control** | A designed control satisfying obligations or risks | CRCO | type (preventive/detective), automation, evidence spec | Versioned |
| **Evidence** | An artifact proving that a control operated | C4.5 | control, subject, hash, timestamp, producing component | Immutable |
| **AgentRun** | One execution of an AI agent | CTO (agent owner) | agent ID and version, model ID, prompt and tool policy version, inputs references, outputs, flags raised, cost, latency | Immutable |
| **Document** | Agreements, appraisals, acknowledgments, statements, ER reports | Owning capability | type, hash, retention class, legal hold | Immutable |
| **Event** | Envelope for all the above changes (see the [event catalog](event-catalog.md)) | Producer | event ID, type, version, subject, causation and correlation IDs, effective/recorded time, actor, payload hash | Immutable |

## 3. Core relationships

```mermaid
erDiagram
  SPONSOR ||--o{ PROGRAM : runs
  PROGRAM ||--o{ ACCOUNT : contains
  PARTY ||--o{ PRIVILEGEGRANT : holds
  ACCOUNT ||--o{ PRIVILEGEGRANT : scopes
  PARTY ||--o{ RELATIONSHIP : "from/to"
  ACCOUNT ||--o{ CONTRIBUTION : receives
  CONTRIBUTION }o--|| ASSET : of
  ACCOUNT ||--o{ POSITION : "units in pools"
  POOL ||--o{ POSITION : holds
  ACCOUNT ||--o{ RECOMMENDATION : "requests from"
  RECOMMENDATION ||--o| GRANT : "becomes (only via DECISION)"
  GRANT }o--|| RECIPIENT : to
  RECIPIENT ||--o{ ELIGIBILITYFACT : has
  RECIPIENT ||--o| PAYMENTPROFILE : "paid via"
  GRANT ||--o{ PAYMENT : "settled by"
  PAYMENT ||--|| REMITTANCE : carries
  DECISION }o--|| POLICY : "made under version"
  DECISION ||--o{ FLAG : raises
  FLAG }o--o| EXCEPTIONCASE : "routed to"
  EXCEPTIONCASE ||--o| APPROVAL : "resolved by"
  EVENT ||--o{ JOURNALENTRY : "posts"
  CONTROL ||--o{ EVIDENCE : produces
  OBLIGATION }o--o{ CONTROL : "satisfied by"
  AGENTRUN ||--o{ FLAG : "may raise (never clear)"
```

## 4. Authoritative sources and copies

| Fact | Authoritative source | Enterprise copy | Reconciled how |
|---|---|---|---|
| Security positions | Qualified custodian | Position mirror (C2.3) | Daily (or event-driven) position and transaction reconciliation |
| Cash | Bank | Treasury ledger | Bank feed (BAI2/camt or API) continuous match |
| Grant payment settlement | Rail / bank | Payment entity | Settlement and return files or webhooks, matched by idempotency key |
| Public-charity status | IRS (Pub 78, EO BMF, auto-revocation list) | EligibilityFact | Refresh on IRS publication cadence; diff → events |
| Sanctions status | OFAC SDN and consolidated lists | EligibilityFact / screening index | List-version-pinned screening; re-screen on list change |
| Identity | Identity provider + documents | Party vault | Re-verification on risk triggers |
| Fund balances | **The enterprise** (event ledger) | — | It is the authority; tested by invariant: Σ account units × NAV = pool NAV |
| Policy | **The enterprise** (Policy registry) | — | Approval records |

## 5. Knowledge representation for agents and services

The enterprise compiles human-authored knowledge into validated, machine-readable artifacts. Agents and deterministic services both consume these artifacts; neither reads the prose directly at decision time.

| Source (human-authored, reviewed) | Compiled artifact | Consumer | Validation before publish |
|---|---|---|---|
| Statutes, regulations, guidance (via counsel) | `Obligation` records with citations and status (current, proposed) | Policy authors, evidence coverage tests | Citation resolves; owner and control assigned |
| Sponsor grant policy (prose) | Policy rules (decision tables) plus a natural-language rendering generated *from* the rules | Policy engine (D); service agent (explanations) | Back-test against the historical grant corpus; diff report reviewed |
| Program agreement and FAQs | Approved-answer corpus with clause IDs | Service agent retrieval | Every clause has a GC approval; answers must cite clause IDs |
| Recipient information | Recipient profile with evidence-grade labels | Discovery agent, donors | Source provenance; grade rubric |
| Operating procedures | Workflow definitions (state machines) | Workflow engine | Model-checked for unreachable or deadlocked states (simple exhaustive tests in the PoC) |

**Reuse of the Echelon Knowledge Store:** the [component assessment](../07-technology-architecture/echelon-component-assessment.md) found it in research phase, with no stable schema and no releases. The *pattern* is worth following, but there is no dependency (DD-014). The pattern: authored knowledge → compiled, validated artifact with provenance → consumed by agents.

## 6. Projection to the open grant record (standards/daf-grant-record v0.1)

| Open record field | Canonical source |
|---|---|
| `grant_id`, `fund_id`, `sponsor_id` | Grant.id, Account.id, Sponsor.EIN |
| `recipient.ein` / `alternative_id` | Recipient |
| `amount`, `purpose`, `restriction_text` | Grant |
| `anonymity` | Recommendation recognition preference → Remittance |
| `status` (pending, approved, paid, rejected, canceled, returned) | Grant state machine (finer-grained internally; see the event catalog) |
| `payment_reference` | Payment settlement |
| `dates` | Event effective times |

The internal grant state machine has more states (for example `Screening`, `AwaitingHumanDecision`, `Released`) than the open record. The projection is lossy by design: internal routing is not disclosed to third parties.

## 7. Data quality controls

- **Schema validation at every boundary.** API inputs, partner files and external data.
- **Referential invariants.** For example, no Grant without a Decision, and no Payment without a Grant in `Approved`.
- **Accounting invariants.** Debits = credits per entry; the unit-ledger identity; cash in transit = sum of unsettled payment instructions.
- **Freshness SLOs on external facts.** Eligibility data older than its refresh SLO blocks the D path and forces a refer; it does not silently pass.
- **Lineage.** Every report cell traces to events by query.
- **Data contracts with partners.** Versioned schemas; breaking changes require a new version.
