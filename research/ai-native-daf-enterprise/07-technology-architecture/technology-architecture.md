# Technology architecture

**Status:** strategic architecture, 2026-11-20. It separates *architectural commitments* (§2), which follow from the outcome and control model, from *implementation choices* (§6), which are provisional and re-evaluated in roadmap Phase 2.

**Inputs:**
- [canonical data model](../06-data-and-knowledge/canonical-data-model.md)
- [event catalog](../06-data-and-knowledge/event-catalog.md)
- [API catalog](../04-enterprise-apis/api-catalog.md)
- [agent architecture](../05-agent-architecture/agent-architecture.md)
- [security architecture](../08-governance-and-compliance/security-architecture.md)
- [Echelon component assessment](echelon-component-assessment.md)

## 1. Requirements that shape the architecture

| Requirement | Source | Architectural consequence |
|---|---|---|
| Exclusive sponsor control; requests are not instructions | O-03, DD-003 | Money-moving capabilities sit behind an internal payment gate that no external or agent credential can reach |
| Every decision reconstructable ("what did we know when?") | O-06, O-07, auditors | Event ledger plus bitemporal facts plus pinned policy and data versions |
| AI may add flags, never clear them | DD-005 | Tool broker with an agent scope type that has no clearance or authoritative-write capability (INV-A5, tested) |
| Modest transaction volume even at scale: 8m grants per year at 1m accounts ≈ 0.25 per second average, with year-end peaks perhaps 10–30× | 09 model | A single well-built deployable with one transactional database is sufficient; horizontal scale-out is not a primary driver |
| Multi-sponsor tenancy (Models C and D) | DD-016 | Tenant = sponsor, enforced in data, authorization and policy |
| Never hold funds; instruction-only | DD-008; regulatory map §14 | No pooled operating accounts. The provider instructs sponsor-titled bank and custody accounts through bank-approved channels |
| Exit and portability | O-16, O-11 | Full-fidelity export in open formats (open grant record v0.1 projection), testable restore |
| Small team | Org model | Few moving parts; managed services; no platform-engineering overhead without a demonstrated need |

## 2. Architectural commitments

1. **Modular monolith (DD-009).** One deployable unit, with modules aligned to capability domains: Relationship and Access, Asset Stewardship, Distribution, Record and Assurance, Policy and Risk, Intelligence. Modules communicate through in-process interfaces and the event outbox, never by sharing tables. A module can later be extracted into a service if evidence demands it; none is expected to need it.
2. **Functional core, imperative shell.**
   - Business rules are pure functions over immutable data: policy decisions, posting rules, fee calculation, state transitions. The reference model ([`../models/`](../models/)) is built this way, and its 59 tests run in about a second with no infrastructure.
   - Side effects sit at the edges, in adapters: bank, custodian, identity provider, model provider, email.
3. **Event ledger plus transactional outbox (DD-006).** Authoritative state changes and their events commit atomically in one database transaction. Projections, notifications and integrations consume the outbox.
4. **Durable workflows as persisted state machines.** Grant, contribution, complex-asset case, succession case, policy change and agent change each have explicit states and transitions. Timers are data.
5. **Policy engine as a module with versioned, back-testable rule sets (DD-011).** Same inputs plus same version gives the same decision (tested). Back-testing replays historical decision contexts against a candidate version and reports the diff.
6. **Internal payment gate.** The only component that can create a payment instruction:
   - it checks the approving actor, open flags, payee verification, cooling-off, caps and dual control;
   - it signs instructions with keys held in an HSM or KMS;
   - it is reachable only from the decisioning module's internal interface.
7. **Tool broker for agents.** Agents run out-of-process. They receive scoped, short-lived credentials for read and propose tools only. Every call is logged to `AgentRun`. Outputs are schema-validated before they can become a flag or a draft.
8. **Identity and authorization: one model for all principals.**
   - Principals are staff, donors, advisors, institutions, agents acting for donors, and internal agents.
   - Attribute-based authorization runs on the canonical PrivilegeGrant and delegation register, which also encodes the delegation of authority (DOA) and its thresholds.
9. **Evidence by construction.** Controls emit evidence records as a side effect of operating, not as a separate reporting job.
10. **Open formats at the boundary.** machine-readable interface contracts (for example OpenAPI) written by the builder, problem+json errors, CloudEvents-style envelopes for webhooks, ISO 20022 / NACHA CCD+/CTX remittance with the grant ID, and open grant-record exports.

## 3. Logical architecture

```mermaid
flowchart TB
  subgraph Edge["Edge (public / partner)"]
    GW[API gateway<br/>OAuth2 · mTLS · rate limits · tenant routing]
    UI[Donor / advisor / staff UIs]
    WH[Webhook delivery]
  end
  subgraph Mono["Modular monolith (single deployable)"]
    REL[Relationship & Access<br/>parties · privileges · delegations]
    AST[Asset Stewardship<br/>intents · contributions · positions · investments]
    DIS[Distribution<br/>recommendations · grants · recipients · eligibility]
    POL[Policy & Risk<br/>policy engine · screening · cases]
    REC[Record & Assurance<br/>ledger · reconciliation · fees · reports · evidence]
    INT[Intelligence<br/>telemetry · twin · change control]
    GATE[[Payment gate<br/>internal only]]
    OUT[(Outbox)]
  end
  subgraph Data["Data"]
    DB[(Transactional DB<br/>events + projections)]
    OBJ[(Object store<br/>documents · WORM evidence)]
    WH2[(Analytics store<br/>pseudonymised)]
  end
  subgraph Agents["Agent runtime (out of process)"]
    TB[Tool broker<br/>read · propose · flag · draft]
    AG[Agent families ×19]
    MP[(Model provider(s))]
  end
  subgraph Ext["External"]
    BANK[Bank / ACH / wire]
    CUST[Qualified custodian]
    IRS[IRS BMF · Pub 78 · revocation]
    OFAC[OFAC lists]
    IDP[Identity provider]
  end
  UI --> GW --> REL & AST & DIS
  DIS --> POL
  POL --> DIS
  DIS --> GATE --> BANK
  AST --> CUST
  REL & AST & DIS & POL & REC --> DB
  DB --> OUT --> WH & WH2 & TB
  TB --> AG --> MP
  AG -. proposals/flags only .-> TB -. via propose API .-> POL
  IRS & OFAC --> POL
  IDP --> REL
  CUST & BANK --> REC
  REC --> OBJ
```

**Trust boundaries:**
1. Internet ↔ gateway.
2. Gateway ↔ monolith: tenant and principal are resolved here.
3. Monolith ↔ agent runtime: agents hold no database credentials. They use the broker with scoped tokens.
4. Payment gate ↔ bank: HSM-signed, allow-listed endpoints.
5. Model-provider boundary: data minimization, no training on customer data by contract, prompt-injection containment.

## 4. Deployment architecture (provisional, §6)

| Concern | Choice | Why |
|---|---|---|
| Hosting | One major managed cloud, two regions (active/passive) | Managed database PITR plus cross-region replica meets RPO/RTO targets [A] in the security architecture without operating our own clusters |
| Compute | Managed container service or PaaS for the monolith; separate isolated pool for the agent runtime | Isolation of agents from money-moving code; no Kubernetes unless operating needs are demonstrated |
| Database | Managed PostgreSQL (append-only event tables plus projections) | Mature, transactional outbox pattern, bitemporal queries, row-level security for tenancy |
| Documents and evidence | Object storage with object lock (WORM) for evidence and legal holds | Immutability for audit evidence |
| Secrets and keys | Cloud KMS plus HSM-backed keys for payment signing | No human holds standing payment credentials |
| Infrastructure definition | The cloud provider's native templates, or a small, reviewed script set | DD-009 spirit: no Terraform or Kubernetes without a demonstrated requirement |
| Observability | OpenTelemetry traces, metrics and logs → managed backend; business telemetry from events (C6.2) | One correlation ID from API call to bank settlement |
| CI/CD | Trunk-based, mandatory tests (domain, invariants, contract tests against OpenAPI), policy back-test gate, separate approval for policy and agent-permission changes | SoD in deployment: author ≠ approver |

**Multi-tenancy for Models C and D:**
- Pool tenants by default: row-level security, tenant-scoped keys and per-tenant policy sets.
- Offer cell isolation, meaning a separate deployment of the same monolith, to large sponsors or banks that require it.
- The monolith design makes "one more cell" an operational task, not a re-architecture.

## 5. Integration architecture

| Counterparty | Pattern | Notes |
|---|---|---|
| Custodian(s) | Files (positions, transactions) and APIs where offered → ingestion adapter → events | Custodians commonly provide batch files. The adapter turns them into events so the rest stays event-driven. Daily three-way reconciliation |
| Bank / ACH | Bank API or host-to-host; NACHA CCD+/CTX with grant ID in addenda; positive pay for any checks; returns and NOC files → events | Instruction-only: accounts are titled to the sponsor (regulatory map §14) |
| Payment networks for nonprofits (Chariot DAFpay, PayPal Grant Payments) | Optional rails behind the payment gate | Avoid single-rail dependence (industry report §2.7: Chariot on Column N.A.) |
| IRS data | Scheduled bulk downloads (EO BMF, Pub 78, auto-revocation) → diff → `CharityEligibilityChanged` | Free, authoritative, with an upstream single point of failure (industry report §2.7). A freshness SLO blocks the deterministic path if stale |
| OFAC | List downloads, version-pinned; rescreen on change | |
| Identity | Identity provider for KYC-style verification (a risk control, not a BSA mandate: regulatory map §13) | |
| Advisor platforms and wealth firms | Partner APIs, SSO (OIDC/SAML), embedded components, data feeds of DAF positions to advisor systems | DD-010 |
| Sponsor systems (Model C) | Sponsor's recordkeeper, if retained, through APIs or files. Policy engine and eligibility can run as services beside an incumbent system of record | Data-rights clauses are the gating risk (GAP-002) |
| Model providers | Provider-agnostic interface. At least two providers qualified per agent family before production reliance | Avoid correlated errors and lock-in |

## 6. Implementation choices: provisional, with reasons

| Choice | Status | Reasoning | Re-evaluate when |
|---|---|---|---|
| **F# for the domain core** (DD-015) | Provisional | Discriminated unions and exhaustive matching make illegal states unrepresentable. The PoC types forbid agent flag-clearance and agent approval at compile time, and a test enumerates agent tool scopes. Immutable-by-default fits event sourcing. The repository owner's functional-programming preference. **Not** required by Echelon Foundry (component assessment) | Phase 2, if the hiring market or vendor SDK coverage makes a mainstream alternative (C#, Kotlin, TypeScript) materially cheaper to staff. The functional-core design transfers to any of them |
| **WebAssembly** | Not adopted for regulated runtime | Limen ships no WASM engine (assessment). WASM sandboxing for *agent tools* or *partner-authored policy extensions* is a plausible future use, but there is no current need | A partner requires running sponsor-authored rule extensions in our runtime |
| **Forma (UI CSS/HTML), Folio (HTML→PDF)** | Evaluate later, non-critical paths only | 1.0.2 and 0.4.x, single maintainer, PolyForm Noncommercial license; a commercial sponsor would need a commercial license | License resolved, second maintainer, production references |
| **Praxis, Dokimos** | Developer tooling only | They govern engineering work and code quality. They do not verify compliance | — |
| **Echelon Knowledge Store** | Pattern only (DD-014) | Research phase | Stable schema and releases |
| **Security** | Use established commercial and open-source security tooling | Aegis is failure handling, not security. "Tutela" was not inspected | — |
| **Managed PostgreSQL, managed containers, one cloud** | Provisional | Lowest operational burden for a small team | Measured load, isolation or regulatory data-residency needs |

## 7. Non-functional targets [A]

| Attribute | Target | Basis |
|---|---|---|
| Routine grant: recommendation → payment instruction | p50 < 1 minute; p95 < 15 minutes (business hours); exceptions SLA 2 business days | Design target; no sponsor publishes P50/P90 (EV-076) |
| Contribution settlement → units credited and acknowledgment issued | Same business day as custodian settlement | |
| Eligibility data freshness | ≤ 35 days old for the deterministic path (matching the PoC policy); OFAC ≤ 1 day | IRS publication cadence; OFAC changes |
| Availability (donor/advisor APIs) | 99.9% monthly | |
| RPO / RTO | ≤ 5 min / ≤ 4 h (security architecture) | |
| Ledger integrity | 100% balanced entries; daily three-way reconciliation with zero unexplained breaks aged > 3 days | Invariants tested in the PoC |
| Evidence completeness | 100% of decisions have a policy version, data versions and actor | Coverage test |

## 8. What the reference implementation demonstrates (and does not)

**Demonstrates** (59 passing tests; see [`../models/`](../models/)):
- the journey from onboarding to grant to reconciliation to Schedule D aggregates;
- deterministic routine approval;
- referral and human decision with role and authority limits;
- an agent cannot approve or clear;
- donor-agent confirmation above the cap;
- payment-gate controls (cooling-off, verification, dual control, caps, idempotency);
- returns, orphan receipts and the eligibility-change hold;
- a 2,000-grant burst;
- ledger identity and balanced entries;
- causation-depth quarantine;
- economics and twin outputs.

**Does not demonstrate:**
- persistence, concurrency or durability, since the model is in-memory and pure;
- real integrations;
- security controls in operation;
- performance at production scale;
- UI;
- AI agents (agents are represented by their *outputs* and the constraints on them).

These are Phase 2–5 deliverables in the [roadmap](../12-implementation-roadmap/).

## Update (2026-11-21): vendor selection by API quality (DD-020)

The [vendor API assessment](vendor-api-assessment.md) scored 75 vendors on 12 criteria. Each criterion is marked Yes, Partial, No or Unknown, with sources; unproven cells stay Unknown.

**Verdicts:** 23 select-candidate, 28 conditional, 18 unverified, 4 reject, and 2 file-only exceptions.

**Effect on §5 (integration architecture):**

| Area | Primary | Second | Note |
|---|---|---|---|
| Custody | Apex | IBKR (conditional) | Schwab, Fidelity and Pershing API docs are login-gated, so they are unverified. **The custodian file adapter remains mandatory** |
| Payments (instruction-only) | Modern Treasury, in bring-your-own-bank mode only. The contract must exclude Modern Treasury holding funds | Column or Increase | J.P. Morgan is conditional until ACH idempotency keys are confirmed (E9 makes counterparty idempotency load-bearing) |
| Charity rail | Chariot | — | Chariot runs on Column N.A. **Do not also use Column as the direct-ACH bank:** that concentrates risk in one bank (industry report §2.7) |
| Bank account verification | Plaid Auth | Finicity or MX | — |
| KYC | Persona | Alloy or Entrust | — |
| Sanctions | OpenSanctions, self-hosted, with a commercial data licence | World-Check One or ComplyAdvantage | — |
| Charity data | IRS bulk files (file-only exception) | Goodstack | Candid only with written consent for AI use; Charity Navigator rejected as a decision input (licence) |
| Crypto | Anchorage (conditional) | Coinbase Prime (conditional) | — |
| E-signature | DocuSign | Dropbox Sign | — |
| Accounting (if an external GL is kept) | QuickBooks Online or Dynamics 365 Business Central | NetSuite or Sage Intacct (conditional) | — |
| Advisor platforms | Addepar, Wealthbox, Salesforce FSC, Orion | — | Envestnet, Black Diamond, Redtail and Morningstar are gated |
| LLM providers | Anthropic API | Amazon Bedrock or OpenAI | Two providers qualified per agent family |

**Rejected:**
- Stripe Treasury/Connect for grant payments (Stripe holds the funds, which conflicts with instruction-only, DD-008).
- Charity Navigator as a decision input.
- NGOsource (no API).
- Non-cash asset processors (none has an API).

**No API-capable vendor exists for:**
- IRS eligibility data and OFAC lists (files only, so download-and-diff adapters emit events);
- non-cash assets and equivalency determinations (manual partner process, recorded as evidence events);
- PayPal Grant Payments and Engiven (no grantmaker API reference published).

These gaps are accepted under DD-020 and tracked as integration risks.
