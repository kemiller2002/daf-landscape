# Interface completeness: "APIs for everything" (DD-019)

**Scope:** analysis of what the company would need to build and how it should work. This is not an implementation; no API contracts are written.

**Owner requirement (2026-11-21):** APIs for everything.

**What that means here:**
1. **Every capability has an API.** Coverage is in [`capability-api-coverage.csv`](capability-api-coverage.csv).
2. **Every business event is published by an API.** Clients receive events as signed, organization-scoped webhooks or through the event API.
3. **Every user interface is a client of the same APIs.** Staff consoles, donor portals and partner embeds use the same APIs. There are no private UI back-ends, so anything a person can do on screen, an authorized system can do through the API, and vice versa.
4. **Exposure is a separate decision from existence.** Some APIs are **internal-only** because exposing them externally would bypass a legal or segregation-of-duties control. These are payment instruction, ledger write, policy publish, flag clearance and custody instruction (see the [API catalog](api-catalog.md) §"Never exposed externally"). They are still APIs: versioned, authenticated, audited and called by internal services and authorized people through governed workflows. "APIs for everything" does not mean "everything is callable by anyone with a token".

These are enforced by tests in `models/Daf.Enterprise.Tests/IdentityTests.fs`: every capability has an API, every event is published by an API, and every API declares exposure and an authorization boundary.

## What was missing and was added (2026-11-21)

**Before:** 23 API domains. 7 of 30 capabilities had no API, and 16 of 58 events were not published by any API.
**After:** 36 domains. All 30 capabilities are covered and all 58 events are published.

| New API | Domain | Fills the gap for | Exposure |
|---|---|---|---|
| API-24 | Partner organizations and tenancy (`/v1/organizations`) | Partner-owned programmes; Model C tenancy | partner (own organization) / internal |
| API-25 | Federation and SCIM (`/scim/v2`, `/v1/federation`) | Partner IdP login; joiner and leaver provisioning (DD-021) | partner |
| API-26 | Sessions and step-up (`/v1/sessions`, `/oauth2`) | MFA assurance, RFC 9470 step-up, RFC 8693 token exchange | public / partner |
| API-27 | Liquidity and treasury (`/v1/treasury`) | C2.5 | internal / partner (read) |
| API-28 | Post-grant obligations (`/v1/grants/{id}/obligations`) | C3.5 | partner / public (grantee submit) |
| API-29 | Screening and fraud (`/v1/screening`) | C5.2; screening-as-a-service | internal / partner |
| API-30 | Governance and delegations (`/v1/governance`) | C5.4; parameter expiry (CTL-047) | internal / auditors (read) |
| API-31 | Vendors and concentration (`/v1/vendors`) | C5.5 | internal |
| API-32 | Simulation and digital twin (`/v1/simulations`) | C6.3 | internal |
| API-33 | Change control (`/v1/changes`) | C6.4 | internal |
| API-34 | Sponsor-to-sponsor transfers (`/v1/transfers`) | Portability (INN-17) | public / partner |
| API-35 | Determinations (`/v1/determinations`) | Reusable costly determinations (INN-04) | internal / partner (network, counsel-gated) |
| API-36 | Agent runs and evaluations (`/v1/agents`) | Agent oversight; kill switches | internal |

**The 16 previously unpublished events, now assigned:**

| Event | API |
|---|---|
| `RelationshipInferred`, `DonorDeceased` | API-02 |
| `AccountInactivityThresholdReached` | API-03 |
| `NoncashAssetDisposed` | API-06 |
| `PolicyBandBreached` | API-08 |
| `DonorConfirmationRequested`, `DonorConfirmationReceived`, `ScheduledGrantDue` | API-09 |
| `CharityEligibilityHoldApplied` | API-10 |
| `EligibilityEvaluated` | API-11 |
| `PaymentProfileChanged`, `PaymentGateDenied` | API-14 |
| `JournalPosted` | API-15 |
| `PostPaymentReviewOpened` | API-28 |
| `ComplianceObligationChanged`, `RegulatoryDeadlineApproaching` | API-30 |

## Cross-cutting API standards (apply to all 36)

- **Security:** OAuth 2.0 with the FAPI 2.0 security profile for partner and money-adjacent APIs. Machine clients use sender-constrained tokens (mTLS or DPoP). Step-up uses RFC 9470. See [identity and partner federation](../08-governance-and-compliance/identity-and-partner-federation.md).
- **Contracts:**
  - A machine-readable contract (for example OpenAPI) for every API, written by whoever builds the platform. Five illustrative contracts from earlier work are kept in [`openapi/`](openapi/) as worked examples; no more will be written here.
  - Idempotency-Key on every state-changing request.
  - RFC 9457 problem details for errors.
  - Additive versioning with a deprecation window.
- **Events:** CloudEvents-style envelopes, signed webhooks, replay by cursor, organization-scoped filtering.
- **Vendor rule:** the platform integrates only with vendors whose own APIs meet the same bar. See the [vendor API assessment](../07-technology-architecture/vendor-api-assessment.md) and DD-020.
