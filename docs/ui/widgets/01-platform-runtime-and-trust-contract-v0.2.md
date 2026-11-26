# Embedded DAF Experiences: Platform, Runtime and Trust Contract v0.2

Status: **proposed implementation contract**. No code, security assessment, browser test or provider integration is claimed. Builds on embedded-widgets-platform-v0.1.md, DAF administration core, financial controls and UX contracts.

## Product architecture
- The domain layer owns fund, grant, charity, authority, accounting, investment and policy semantics. No widget duplicates policy or monetary calculations.
- The experience layer owns typed view models, workflow orchestration, validation presentation, state explanations, accessible interaction and drafts.
- The delivery layer adapts an experience to full first-party app, hosted cross-origin iframe, optional Web Component wrapper, or headless partner API.
- The platform layer owns partner onboarding, federated identity, scoped sessions, widget registry, telemetry, billing, versioning, compliance evidence and incident response.
- Use F# for platform code and Limen WASM/Forma for the hosted interface where technically validated. Folio remains the controlled report/document renderer. A thin JavaScript embedding loader is permissible as a distribution artifact; no separate JS business logic.

## Delivery modes and priority
M1 Hosted iframe: P0. Isolated origin, centrally patched, host integrates via minimal loader or iframe.
M2 Headless API: P0 contract design, P1 partner availability. Partner's server and client independently integrate; financial commands still require sponsor-side authority and UX standards.
M3 Web Component: P1 wrapper around iframe, e.g. custom element for lifecycle and sizing; native in-DOM rendering requires feasibility proof.
M4 Native framework packages: P2 and only if justified by customer demand and maintenance cost.
M5 Mobile native host: P2, authenticated top-level handoff or supported secure browser view; no assumption that web iframe behavior carries over.

## Widget manifest schema (proposed typed F# record)
WidgetManifest: WidgetId; SemanticVersion; Family; Audience; RiskTier; AllowedOperations; RequiredScopes; RequiredPolicyCapabilities; SupportedModes; MinWidth; ResponsiveBreakpoints; SupportedLocales; ThemeTokenSchemaVersion; AccessibilityContractVersion; EventSchemaVersion; SessionProfile; CSPProfile; SupportWindow; DeprecatedAt option.
PartnerRegistration: PartnerId; ContractedSponsorScopes; ApprovedOrigins; Environment; IdentityFederationMethod; PublicKeys; PermittedWidgetIds; PermittedCapabilities; SupportOwner; IncidentContact; LegalDisclosures; BrandingPolicy; Status.
WidgetInstance: InstanceId; ManifestVersion; PartnerId; TenantId; LegalEntityId; PrincipalId; EffectiveAuthorityRevision; FundScope; SessionId; Expiry; ParentOrigin; State; CreatedAt.
All identifiers opaque and strongly typed. Never infer fund or tenant authority from a parent-provided display identifier.

## Trust boundaries and protocol
1. Partner backend authenticates user and requests one-time launch grant using a trusted service credential. The server verifies contract, sponsor/legal entity, subject mapping, delegated rights, widget capability, requested fund and registered origin.
2. Browser receives only an ephemeral one-use launch artifact; no reusable partner secrets in URL, DOM, local storage or messages. Avoid URL exposure where possible and explicitly test history, referrer, logs and redirects.
3. Widget server exchanges launch artifact with replay protection, binding to partner/origin/widget/subject and nonce; returns narrowly scoped, short-lived session.
4. Browser embedding is subject to third-party cookie restrictions. Test token handling, storage partitioning, refresh, Safari ITP, Firefox and Chromium. Define accessible top-level reauthentication fallback.
5. CSP frame-ancestors is generated from exact approved origins; avoid wildcard allowlists. Enforce response protections and test compatibility.
6. postMessage must validate origin, source, instance, schema version, nonce and event type. Use exact targetOrigin; no wildcard. Do not accept a parent 'approve', 'submit grant', 'pay', 'change authority' or 'change fund' command as proof of authorization.
7. Events exposed to host are minimal: ready, resize, navigationRequested, userAttentionRequired, commandAccepted (opaque ID), commandStatusChanged (non-sensitive category), closeRequested, sessionExpired, fatalError (safe code). Detailed data stays within widget origin.
8. All commands reauthorize server-side using trusted identity and current effective-dated policy, expected revision, canonical request hash and idempotency key.
9. Origin verification is a defense in depth, not user authentication. A registered origin may still be compromised. The widget must display trusted sponsor identity and relevant transaction details.

## Session states
Uninitialized -> LaunchPending -> Exchanging -> Authenticated -> Active -> ReauthRequired -> Expired/Revoked/Closed. Failures: OriginRejected, PartnerSuspended, SubjectUnmapped, ScopeDenied, CapabilityUnavailable, ReplayRejected, SessionConflict, ProviderUnavailable. No sensitive state from previous instance may remain visible after scope change or revocation.

## API contract proposals
POST /partner/widget-launches (server-authenticated; partner/user/fund/widget/origin, correlation ID)
POST /widget/sessions/exchange (single-use artifact, nonce)
GET /widget/sessions/current
POST /widget/sessions/refresh (only where safe and supported)
POST /widget/sessions/revoke
GET /widgets/{id}/manifest
GET /widget/capabilities
GET /widget/health (safe operational status)
GET /widget/command-receipts/{id}
GET /widget/audit-events (authorized admin only)
Command receipt: commandId, idempotencyKeyHash, requestHash, state [Rejected|Accepted|Processing|Succeeded|Failed|Unknown], correlationId, acceptedAt, updatedAt, nextCheckAt option. Succeeded must be defined by domain-specific outcome; do not equate accepted recommendation with paid grant.

## Runtime and rendering
- Nonblank, branded Limen startup and meaningful loading, timeout, failure and recovery states.
- Multiple widget instances on one host page with independent state, focus, sessions and event IDs.
- Parent-host CSS cannot alter widget controls or disclosures. Branding is via approved tokens and assets, validated contrast and limits.
- Container query or explicit viewport size behavior must be measured. Resize messages throttled and bounded; avoid infinite feedback loops.
- Parent cannot observe sensitive keystrokes or internal navigation through event bridge. Do not expose private data in error strings, console output or analytics.
- Accessible iframe title, keyboard focus entry/exit, dialog focus trap, screen-reader announcements, zoom/reflow, touch and reduced motion.
- Prefer explicit full-screen handoff for complex high-risk flows if embedding creates unresolvable security or usability defects.

## Developer experience and governance
Sandbox partner onboarding, origin validation, example embed, synthetic donors/funds, documented scopes, version compatibility, local test harness, signed manifests, operational dashboard, rate-limit guidance, webhook verification, incident escalation, support attribution and deprecation policy.
Partner self-service must not enable privileged operations, broad scopes, unrestricted origins or bypass sponsor disclosures. Security review for partner changes and sensitive widget activation.
Versioning: semantic widget manifest + event schema + view model/API version + policy revision. Rollback plans and contract tests before deployment; central update does not waive partner compatibility obligations.
