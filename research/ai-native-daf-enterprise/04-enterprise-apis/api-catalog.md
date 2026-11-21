# Enterprise API catalog

**Status:** requirements analysis, 2026-11-20; scope clarified 2026-11-21. This catalog describes the interfaces an AI-native DAF company **would need to build** and how they should behave. It is analysis, not an implementation: no API contracts are written here, and none are planned in this research.

**Machine-readable catalog:** [`api-catalog.csv`](api-catalog.csv) (36 interface domains, each with all twelve required attributes).

**Contracts:** none. Five draft OpenAPI documents written on 2026-11-20 were removed on 2026-11-21, when the owner set the scope as analysis only. They remain in git history.

**Consistency with other artifacts:**
- Resource families match the workflows in [`../03-workflow-redesign/`](../03-workflow-redesign/).
- Events match [`../06-data-and-knowledge/events.csv`](../06-data-and-knowledge/events.csv).
- Owning capabilities match [`../02-business-capabilities/capability-map.md`](../02-business-capabilities/capability-map.md).

## 1. Principles

1. **API-first is not microservices-first.** Every capability publishes its contract before it has a UI, and the portal is just one more client. All capabilities still deploy as **one modular monolith** with one transactional store and an outbox (DD-009). A module boundary is enforced in code (module-private types, a contract assembly per module, architecture tests). A network boundary is added only when a measured need appears.
2. **The contract follows the canonical model.** Every resource is a projection of a canonical entity, and every write is a command that produces an event. The same command may not be exposed under two resource names.
3. **Requests, not instructions (DD-003).** External write endpoints create *requests*: `Recommendation`, `InvestmentRequest`, `ContributionIntent`, `TransferRequest`. External callers get no endpoint that creates a `GrantApproved`, `TradeInstructed` or `PaymentInstructed`.
4. **One authorization model** spans humans, institutions and AI agents. An agent is a principal acting under a delegation (DD-017), never a borrowed credential.
5. **Evidence by default.** Every mutating call returns the `decision_id` or `event_id` it produced. Every decision is retrievable through the Evidence API by authorized parties.
6. **Tenant = sponsor (DD-016).** Every token is bound to one sponsor tenant. Cross-tenant reads are impossible by construction (row-level tenancy plus tenant in the token audience), including for shared eligibility data, which is the one deliberately *shared* dataset and is published read-only.

## 2. Exposure model

| Tier | Who | Examples | Transport and authentication |
|---|---|---|---|
| **Public** | Any registered developer; donors via apps | Eligibility lookups (commercial key), recommendation submission through a donor's own delegation, recipient profiles | OAuth2 authorization code + PKCE (users); API keys only for the public eligibility tier (rate-limited, no personal data) |
| **Partner** | Contracted institutions: wealth platforms, custodians, RIAs, other sponsors, auditors | Accounts, privileges, contributions, positions (read), investment requests, grants, webhooks, evidence (auditors) | OAuth2 client credentials with **mTLS certificate-bound tokens** (RFC 8705); per-institution scopes; IP allow-lists optional |
| **Internal** | Modules within the monolith; operations staff tools | Payments, ledger write, policy publish, cases, the raw event stream | In-process module contracts; staff via SSO with phishing-resistant MFA and just-in-time privilege |

### Never exposed externally, and why

| Capability | Why not |
|---|---|
| **Payment instruction** (`/v1/payments` writes) | Money moves only through the payment gate after `GrantApproved` (O-03 exclusive control; segregation of duties). An external endpoint would be a path around the decision record. Rails reach the enterprise *inbound* (settlement webhooks) only. |
| **Ledger write** (`/v1/ledger` POST) | The journal is derived from events by versioned posting rules (DD-006). Direct writes would break the replay identity and the audit lineage. Corrections are reversing events produced by authorized internal workflows. |
| **Policy publish** (`/v1/policies` POST/PUT) | Publishing requires back-test, independent test and change-board approval, with author ≠ approver (DD-011). Licensed sponsors in Model C publish through the same governed workflow inside their own tenant, never over a raw API. |
| **Flag clearance** | Flags are cleared only by a rule or a person (DD-005). No API accepts a clearance from an agent principal. |
| **Custody instructions** | Only the internal rebalancer and mandate checker issue `TradeInstructed` (DD-007, DD-008). |
| **Raw event stream** | It contains cross-account data. Partners receive filtered, signed webhooks instead. |

## 3. Authentication and authorization model

**Token types:**

| Token | Subject | Key claims | Typical lifetime |
|---|---|---|---|
| User token | A person (donor, advisor, staff) | `sub`, `tenant`, `scope`, `acr` (assurance level), `amr` | 15 min, with refresh rotation |
| Institution token | A contracted organization (service) | `sub` = client, `tenant`, `scope`, `cnf.x5t#S256` (mTLS binding) | 5–15 min |
| **Agent-principal token** | An AI agent acting for a person under a `PrivilegeGrant` | `sub` = agent client, `act` = {delegating party} (RFC 8693 token exchange), `delegation_id`, `caps` {max_amount_per_grant, max_amount_per_day, recipients_allowlist?}, `confirm_above` (amount needing human confirmation) | ≤ 15 min; no refresh without a live grant |

**Scopes (examples):** `accounts:read`, `recommendations:write`, `grants:read`, `grants:cancel`, `investment-requests:write`, `privileges:manage`, `eligibility:read`, `evidence:read`, `webhooks:manage`.

**Agent-principal tokens are restricted:**
- They never receive `privileges:manage`. An agent cannot widen its own authority.
- They never receive `grants:cancel` on grants they did not originate.

**Authorization evaluation** (policy engine, decision type D):

`allow = tenant matches ∧ scope present ∧ PrivilegeGrant(subject, account, action) active ∧ caps satisfied ∧ step-up satisfied when risk band requires`

**Confirmation rule for agents:** a recommendation from an agent principal above `confirm_above` enters the `AwaitingDonorConfirmation` state, and the donor confirms through a separate channel (a push to the user's authenticated app). This is the explicit confirmation step the repository found missing from public agentic products. The repository records it as open: Daffy MCP had no documented limits ([industry report §7](../../DAF-INDUSTRY-REPORT-2026-11.md)).

**Segregation in authorization:** separation-of-duties constraints from [`accountability-matrix.csv`](../02-business-capabilities/accountability-matrix.csv) are enforced as deny rules. Two examples: the creator of a payee cannot approve a payment to it, and an approver cannot decide a case about a related party.

## 4. Cross-cutting contract rules

| Concern | Rule |
|---|---|
| **Idempotency** | Every mutating request requires `Idempotency-Key` (a UUID). The server stores `(client, key) → response` for 7 days. A replay with the same body returns the original response; a different body returns `409` with `problem type /problems/idempotency-key-reuse`. |
| **Validation** | JSON Schema 2020-12 at the edge, then domain validation inside the module. Domain failures return problem types with machine-readable `errors[]`. |
| **Errors** | RFC 9457 `application/problem+json`. Stable `type` URIs under `https://api.example-daf.org/problems/…`, with `title`, `status`, `detail`, `instance`, and extension members `decision_id` and `errors`. |
| **Versioning** | Major version in the path (`/v1`). Changes within a major version are additive only. Deprecation carries the `Deprecation` and `Sunset` headers with a minimum notice of 12 months for partner APIs. Each event type carries its own `schema_version`. |
| **Pagination** | Cursor-based (`page[after]`) for all lists. |
| **Concurrency** | `ETag` / `If-Match` on mutable resources such as privileges and profiles. |
| **Events and webhooks** | Signed with HMAC-SHA256 over `timestamp.body`, with a 5-minute replay window. The `event_id` is the subscriber's dedupe key. Delivery is at-least-once, with exponential backoff and a dead-letter queue. |
| **Audit** | Every call is logged as (actor, `act` chain, scope, tenant, resource, decision_id). PII reads are logged at field-group level. |
| **Privacy** | Responses are minimized by scope. Recipients see donor information only per the anonymity choice. Analytics consumers get pseudonymous keys. |

## 5. API domains

Each domain below repeats the CSV in prose for review. The CSV is authoritative.

### API-01 Identity and authorization
- **Purpose:** issue and validate tokens, and map scopes and delegations.
- **Consumers:** all.
- **Boundary:** buy an IdP; this enterprise owns only the DAF-specific scope and delegation model.
- **Commercial potential:** low.

### API-02 Donor and advisor profiles (`/v1/parties`)
- **Purpose:** the canonical Party and its Relationships.
- **Boundary:** advisors read client parties only through a privilege.
- **Privacy:** the PII vault and field-level redaction.
- **Events:** `PartyRegistered`, `IdentityVerified`, `RelationshipDeclared`.
- **Commercial potential:** low.

### API-03 Account establishment (`/v1/accounts`)
- **Purpose:** opening fails with `/problems/prerequisite-missing` unless `IdentityVerified` and `AgreementAccepted` exist.
- **Commercial potential:** **high.** This is the embedded-DAF primitive for wealth platforms and fintechs (Model C). Buyers are the same institutions that today run branded programs on RCF + Ren ([industry report §2.2](../../DAF-INDUSTRY-REPORT-2026-11.md)).

### API-04 Delegated privileges (`/v1/privileges`)
- **Purpose:** grants for advisors, family members, successors and **AI agent principals**.
- **Validation:** caps must be ≤ the program maximum, and the grantee must be verified.
- **Commercial potential:** medium. It could become an open delegation profile for philanthropy, which lowers integration cost for donor-side agent products without credential sharing (DD-017).

### API-05 Contributions (`/v1/contribution-intents`, `/v1/contributions`)
- **Purpose:** intents carry a unique reference that the custodian transfer must quote. This removes most orphan-deposit work (ACT-010).
- **Commercial potential:** medium, as intake and matching for sponsors.

### API-06 Asset acceptance (`/v1/contribution-intents/{id}/acceptance`)
- **Purpose:** complex-asset case submission. The decision is H.
- **Commercial potential:** medium. It overlaps with non-cash processors ([`b40n14-03-b38c-03-noncash-vendors-dpn.md`](../../mission-2026-11-14/b40n14-03-b38c-03-noncash-vendors-dpn.md)).

### API-07 Custody and positions (`/v1/positions`)
- **Purpose:** a read-only mirror of the qualified custodian.
- **Commercial potential:** low.

### API-08 Investment instructions (`/v1/investment-requests`)
- **Purpose:** requests that the deterministic mandate checker accepts or rejects (`/problems/out-of-mandate`).
- **Commercial potential:** medium, as pre-trade compliance for advisor-managed DAF programs.

### API-09 Grant recommendations (`/v1/recommendations`)
- **Purpose:** the highest-volume external write.
- **Idempotency:** mandatory. Duplicate submissions from portals, agents and retries are the common failure.
- **Commercial potential:** **high.**

### API-10 Grants (`/v1/grants`)
- **Purpose:** the state machine is readable by donors, advisors and the recipient (for its own grants). Cancellation is allowed only before release.
- **Projection:** to the repository's [open DAF grant record v0.1](../../../standards/daf-grant-record/schema-v0.1.json).
- **Commercial potential:** **high.** A shared grant-status network answers the main nonprofit-side complaint about fragmented rails and status ([strategic synthesis §0 G4](../../mission-2026-11-14/strategic-synthesis.md)).

### API-11 Charity eligibility (`/v1/recipients`, `/v1/eligibility`)
- **Purpose:** returns **dated, sourced, bitemporal** facts plus a policy evaluation, so a sponsor can prove "what we knew when we approved".
- **Commercial potential:** **high.** Buyers are sponsors, donation processors and giving platforms. The alternatives are Candid Charity Check and in-house BMF loads ([industry report §2.6](../../DAF-INDUSTRY-REPORT-2026-11.md)). The differentiation is evidence retention and continuous change events, not the underlying IRS data, which is public.

### API-12 Due diligence (`/v1/recipients/{id}/diligence`)
- **Purpose:** dossiers for foreign recipients, expenditure responsibility (ER) and fiscal sponsors.
- **Commercial potential:** medium. Shared equivalency and ER work could cut duplicated cost across sponsors, but whether another sponsor may rely on it is a legal question (GAP; see 08-).

### API-13 Policy evaluation (`/v1/policies`, `/v1/decisions:evaluate`)
- **Purpose:** pure, deterministic evaluation against an immutable policy version. Publishing is internal only.
- **Commercial potential:** **high**, as policy-as-code with back-testing (C5.1).

### API-14 Grant payments (`/v1/payments`)
- **Exposure:** **internal only.** Rails post settlements and returns inbound.
- **Commercial potential:** medium. It is sellable only in combination with a regulated rail partner, given money-transmission constraints (see 08- regulatory map).

### API-15 Fund accounting (`/v1/ledger`)
- **Exposure:** read-only externally.
- **Commercial potential:** low as a standalone product.

### API-16 Reconciliation (`/v1/reconciliation`)
- **Commercial potential:** medium. Cross-institution reconciliation pain is documented in [`daf-cross-institution-reconciliation-evidence-2026-11-11.md`](../../daf-cross-institution-reconciliation-evidence-2026-11-11.md).

### API-17 Fees (`/v1/fees`)
- **Purpose:** schedule versions and caps, including advisor-fee caps. Only 3 programs publish a cap ([strategic synthesis §0 A](../../mission-2026-11-14/strategic-synthesis.md)).
- **Commercial potential:** low.

### API-18 Reporting and documents (`/v1/reports`, `/v1/documents`)
- **Purpose:** statements, tax documents and **full-history portability export** (O-16).
- **Commercial potential:** low.

### API-19 Notifications and webhooks (`/v1/events` subscriptions)
- **Purpose:** filtered, signed, minimized event deliveries.
- **Commercial potential:** medium, as part of the grant-status network.

### API-20 Audit evidence (`/v1/evidence`, `/v1/decisions`)
- **Purpose:** read-only, time-boxed auditor scopes.
- **Commercial potential:** **high**, as continuous evidence for sponsors and their auditors (C4.5).

### API-21 Exception cases (`/v1/cases`)
- **Purpose:** decisions are allowed only within delegated authority, never on one's own or a related party's case.
- **Commercial potential:** medium.

### API-22 Operational events (internal stream)
- **Purpose:** the enterprise backbone. It feeds the digital twin.
- **Commercial potential:** low.

### API-23 Philanthropic intelligence (`/v1/recipients/{id}/profile`)
- **Purpose:** evidence-graded recipient information with disclosed ranking criteria and no paid placement.
- **Commercial potential:** medium.

## 6. APIs that could become independent commercial products

| Product | APIs | Likely buyers | Why it could stand alone | Main risk |
|---|---|---|---|---|
| **Eligibility and evidence service** | API-11, API-20 (subset) | Mid-size sponsors, community foundations (Foundant holds the tail: 282 of 351 tail CFs with an identified vendor), donation processors, giving platforms | Every disbursing charity needs dated eligibility evidence. No public product found retains bitemporal evidence as its core promise [I] | Low price ceiling; IRS data is free; Candid incumbent |
| **Grant recommendation and status network** | API-09, API-10, API-19 | Wealth platforms, fintechs, nonprofits (status), donor-side agent products | Fills the "no open multi-sponsor grant-request standard" gap ([strategic synthesis §0 D](../../mission-2026-11-14/strategic-synthesis.md)) | Network effects need several sponsors; incumbents' terms restrict automation |
| **Embedded DAF accounts** | API-03, API-04, API-05, API-08 | RIAs, broker-dealers, banks, wealth platforms (Model C) | Distribution-led growth [I] | Needs a sponsor of record (own or partner); long sales cycles |
| **Policy-as-code and decisioning** | API-13, API-21 | Sponsors modernizing grant review | Back-testable policy shrinks exception queues | The value pool per sponsor is thin: calibrated large-national AI pool $445k [S] ([strategic synthesis §0 B](../../mission-2026-11-14/strategic-synthesis.md)) |
| **Continuous audit evidence** | API-20 | Sponsors' finance and audit teams; audit firms | Lowers audit cost and preparation | Auditor acceptance is unproven |
| **Disbursement and reconciliation** | API-14 (via partner), API-16 | Sponsors without in-house rails | Chariot proves demand ([industry report §2.5](../../DAF-INDUSTRY-REPORT-2026-11.md)) | Money-transmission licensing; competes with Chariot, PayPal and Ren RDE |

The full commercial evaluation is in [`../10-market-and-business-model/`](../10-market-and-business-model/).
