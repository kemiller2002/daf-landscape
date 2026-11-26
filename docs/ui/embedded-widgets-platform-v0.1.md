# DAF Embedded Experiences and Widget Platform v0.1

Status: exploratory architecture and requirements, NOT implemented or security-tested. Complements administration core, UI contracts and financial core.

## Product hypothesis
Deliver DAF capabilities inside third-party wealth management portals, sponsor sites, advisor applications and enterprise workspaces without duplicating business rules. Widget experiences are governed clients of the same authorization, policy, accounting, charity and custody APIs as first-party applications. Distribution is a product capability, not a reason to weaken sponsor control.

## Four delivery models
1. Hosted iframe widget (first implementation candidate): strong origin isolation, centrally updated UI, explicit trusted messaging. Third-party cookie behavior and embedded authentication require verification.
2. Headless API (first implementation candidate): partners implement UI with server-to-server or properly delegated API access. Contract tests, approval UX, and financial semantics mandatory.
3. Web Component wrapper (second candidate): custom element can mount secure iframe, communicate via typed events, and optionally host approved non-sensitive Forma elements. Verify Limen runtime loading, Shadow DOM, styling, CSS isolation and accessibility before promising direct in-DOM WASM rendering.
4. Native SDK/framework package (later): high partner flexibility but expensive version, security and accessibility maintenance. No independent financial logic.

## Candidate widget registry
| ID | Widget | Audience | Risk tier | Key requirements |
|---|---|---|---|---|
| W01 | Fund summary | donor/advisor | Confidential read | as-of, policy recommendable balance |
| W02 | Grant recommendation | donor/advisor | Transactional | four-step flow, preview, sponsor approval |
| W03 | Charity search | donor/advisor | Contextual read | internal registry, evidence freshness |
| W04 | Grant status | donor/advisor | Confidential read | separate recommendation/approval/payment states |
| W05 | Contribution initiation | donor/advisor | Transactional | gift acceptance state and secure intake |
| W06 | Giving history | donor/advisor | Confidential read | legal scope, filtering, export |
| W07 | Investment overview | donor/advisor | Confidential read | source/as-of and authority |
| W08 | Statements | donor/advisor | Sensitive export | Folio, authorization, redaction |
| W09 | Fund opening | sponsor/partner | High-sensitivity intake | agreements, signatures, activation distinct |
| W10 | Advisor multi-client view | wealth manager | Cross-fund read | each fund independently authorized |
| W11 | Service request | donor/partner | Personal data write | case receipt, privacy |
| W12 | Operations task | sponsor staff | Privileged | evidence, SoD, command authority |
| W13 | Fee explanation | donor/advisor | Confidential read | reproducible formula and basis |
| W14 | Fund contribution status | donor/advisor | Confidential read | received/accepted/valued distinct |
| W15 | Partner onboarding | partner admin | Privileged | registered origin, identity, contracts |
| W16 | Donation discovery | public/partner | Public | distinguish charity search from DAF grant |

## Host/guest trust boundaries
- The embedding host is not inherently trusted merely because it presents the widget.
- Server validates partner registration, origin allowlist, allowed widget, legal entity, user delegation and effective capability.
- Never pass long-lived secrets, financial data or identity assertions in iframe URL query parameters.
- Session bootstrap uses short-lived single-use server-issued code with audience, nonce, partner, origin, user context and expiration; server exchanges code for scoped session. Validate anti-replay and PKCE-like binding as appropriate to architecture. This is a design proposal, not a verified auth protocol.
- CSP frame-ancestors should restrict actual parent origins per tenant/partner; X-Frame-Options and CSP interactions must be tested. Protect widget from clickjacking, overlay and deceptive host UI.
- Parent/child postMessage uses exact targetOrigin, event origin and source validation, schema/version validation, nonce/session binding, replay protection, and strict message allowlist. Never transmit account numbers, credentials, charity banking details, donor notes or raw financial records.
- The host may receive lifecycle events (ready, resize, navigate request, command accepted, close, recoverable error) with opaque correlation IDs only; it cannot send approve/pay/transfer commands directly.
- No third-party cookie assumptions. Test Safari/iOS, Firefox, Chromium and storage partitioning; define top-level redirect or popup handoff for flows requiring stronger authentication.
- Cross-origin iframe isolates DOM but does not by itself prevent clickjacking, malicious overlay, phishing, fingerprinting, or compromised host. Threat model these explicitly.
- All commands are server-authoritative with effective-dated capability checks, sponsor policy, idempotency, expected revision, canonical request hash and durable audit.

## Proposed widget manifest
WidgetDefinition: id, semanticVersion, audience, riskTier, capabilities, inputSchema, outputEventSchema, supportedLocales, supportedThemes, minimumHostSize, accessibilityContract, authenticationMode, allowedPartnerOrigins, CSPProfile, retentionClass, telemetryClass, featureFlags, supportWindow.
WidgetInstance: opaqueId, partnerId, tenantId, legalEntityId, principalBinding, fundScope, manifestVersion, sessionExpiry, allowedActions, renderMode, lastActivity, revokedAt.
PartnerIntegration: partnerId, legalName, contractedSponsorScopes, registeredOrigins, environment, identityFederationConfig, callbackEndpoints, publicKeys, activeCapabilities, auditOwner, status.

## Widget lifecycle
Discover widget -> register partner and origin -> configure permitted theme/locale -> authenticate user through partner -> obtain scoped bootstrap code from trusted backend -> mount iframe -> exchange code -> load Forma/Limen app -> fetch authorized data -> complete read or command workflow -> return opaque result -> expire/revoke session -> clean up state. Errors and recovery are first-class states.

## Accessibility and design
- Widget must be operable with keyboard and screen reader within iframe; parent should supply descriptive iframe title and ensure tab sequence and focus handoff are tested.
- Dynamic iframe resizing requires validated messaging and limits; avoid nested scrolling where possible.
- 320px narrow embeds, 400% zoom, reduced motion, high contrast, touch and localized number/date formats.
- Branding via approved semantic tokens, logos and disclosures; host CSS must not silently override legal content or financial semantics.
- Widget has meaningful Limen loading state and own branded identity even if host page loads slowly.
- Show source, currency, as-of, valuation and policy basis for financial metrics.

## APIs and contracts (proposed)
GET /widget-registry/{widgetId}/manifest
POST /widget-sessions/bootstrap (server-authenticated)
POST /widget-sessions/exchange (one-time code, bound to partner/session/origin)
POST /widget-sessions/revoke
GET /widget-sessions/current (scoped)
GET /ui/widget/fund-summary
POST /ui/widget/grant-drafts
POST /ui/widget/grant-preview
POST /commands/grant-recommendations
GET /ui/widget/command-receipts/{opaqueId}
Event envelope: {protocolVersion, widgetInstanceId, nonce, eventType, correlationId, payload}; payload is strictly typed and privacy-limited.

## Partner developer experience
- Sandbox, sample host HTML/React/Vue/Angular snippets, typed SDK, test identities, synthetic funds/charities, accessible demo, signed manifests, version compatibility matrix, contract test kit, error catalog and integration health dashboard.
- Developer portal should explain fund ownership semantics, legal authority, read vs recommend vs approve vs pay, data freshness, webhooks, rate limits and incident procedures.
- Partner-specific usage metering should distinguish render, active session, read, submitted recommendation, accepted command, support, and actual settlement; no double billing.
- Version policy: additive event/schema evolution, explicit deprecation windows, rollback, canary rollout, compatibility tests and tenant-specific freeze options.
- Support SLA and incident response specify which party owns end-user support, authentication issues, fraud escalation and data breaches.

## Non-goals and anti-patterns
- No embedding raw privileged administration screens by default.
- No client-side partner token that grants financial commands.
- No trust in postMessage content without server authorization.
- No financial state mirrored as authoritative in partner local storage.
- No assumption that all Forma components can run as native Web Components without feasibility work.
- No direct API mutation of sponsor-owned financial records from a host application.
- No misleading 'paid' or 'approved' status when only recommendation submitted.

## Threat and acceptance tests
EW-T01 unregistered origin blocked; T02 registered origin but wrong sponsor blocked; T03 stolen bootstrap code replay rejected; T04 expired session; T05 parent forged postMessage rejected; T06 child forged source rejected; T07 unsafe wildcard targetOrigin prohibited; T08 cross-tenant context switch; T09 revoked advisor mid-grant; T10 clickjacking/overlay risk test; T11 third-party cookie disabled; T12 Safari/iOS embedded auth; T13 mobile 320px and 400% zoom; T14 keyboard focus in/out of iframe; T15 accessible error and validation; T16 duplicate grant command after timeout; T17 stale NAV and recommendable basis; T18 unknown external payment state; T19 malicious charity description XSS/prompt injection; T20 CSP frame-ancestors test; T21 sensitive data absent from URL and events; T22 partner theme fails contrast and is rejected; T23 multiple widgets on one host page; T24 widget version rollback; T25 revoked partner origin while mounted; T26 iframe resize storm bounded; T27 host SPA route change; T28 deep link and top-level handoff; T29 screen reader nested navigation; T30 API rate limit and error recovery.

## Phased implementation
P0 research and threat model: verify Limen/Forma embedding, browser auth, origin CSP, screen-reader behavior; choose first partner archetype and widget.
P1 read-only fund summary + grant status iframe with synthetic data, secure bootstrap and origin restrictions.
P2 charity search and grant recommendation, full server command safeguards, idempotency, sponsor authority, draft resume.
P3 contribution/fund opening, documents/Folio, multi-client advisor.
P4 Web Component wrapper and SDK, if technical feasibility and security validated.
P5 privileged sponsor operations widgets only with explicit policy, audit, SoD and partner contracts.

## Decision and economics questions
Who pays: sponsor, wealth manager, advisor platform, or usage-based? Is embedding a distribution channel, white-label service, or API platform? Who handles support and fraud? Can partner analytics observe user behavior without receiving donor-sensitive data? Which custodians/advisor CRMs provide contractual integration access? Are widget licensing and white-label capabilities independent? Which financial events trigger billable usage? Validate through partner interviews and cost-to-serve modeling, not assumptions.

## Required go/no-go
A security-reviewed, cross-browser, accessible hosted read-only widget is the first executable proof. Do not promise production transactional embedding until authentication, trusted command boundary, sponsor approval semantics, financial controls, and recovery tests pass.
