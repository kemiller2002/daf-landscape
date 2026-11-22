# Embedded DAF Experiences: Test Traceability and Implementation Plan v0.2

Status: proposed verification plan; no tests executed.

## Test suites
SEC-01 exact origin allowlist; SEC-02 CSP frame-ancestors; SEC-03 launch artifact replay; SEC-04 expired launch; SEC-05 partner suspended; SEC-06 subject mismatch; SEC-07 fund scope mismatch; SEC-08 message forged origin; SEC-09 message forged source; SEC-10 message schema mismatch; SEC-11 nonce replay; SEC-12 wildcard target origin forbidden; SEC-13 host compromised/overlay; SEC-14 sensitive data leakage URL/console/telemetry; SEC-15 third-party cookies disabled; SEC-16 session revocation while mounted; SEC-17 multiple instances isolation; SEC-18 partner key rotation; SEC-19 cross-tenant read denial; SEC-20 command authorization after role change.

UX-01 320px compact fund; UX-02 400% zoom; UX-03 keyboard iframe entry/exit; UX-04 screen reader landmarks; UX-05 focus restoration; UX-06 reduced motion; UX-07 high contrast; UX-08 iframe resize bounds; UX-09 host SPA route changes; UX-10 offline/reconnect; UX-11 startup meaningful loading; UX-12 no blank WASM; UX-13 accessible error summary; UX-14 mobile keyboard obscuring action; UX-15 localization/number formatting; UX-16 multiple widgets on page; UX-17 top-level auth handoff; UX-18 Safari/iOS; UX-19 Firefox; UX-20 Chromium.

FIN-01 fund value basis; FIN-02 recommendable distinct from NAV; FIN-03 stale custody feed; FIN-04 null not zero; FIN-05 pending not paid; FIN-06 percent denominator; FIN-07 rounding across sources; FIN-08 source restriction; FIN-09 shared liquidity claims; FIN-10 eligibility change; FIN-11 policy version change; FIN-12 advisor authority revoked; FIN-13 draft conflict; FIN-14 duplicate submit; FIN-15 accepted after timeout; FIN-16 unknown payment outcome; FIN-17 sponsor approval separate; FIN-18 accounting receipt lineage; FIN-19 no double-count in advisor aggregate; FIN-20 no unsupported fee or settlement promise.

OPS-01 sandbox registration; OPS-02 origin approval; OPS-03 branding contrast; OPS-04 widget manifest version; OPS-05 rollback; OPS-06 feature kill switch; OPS-07 incident runbook; OPS-08 access review; OPS-09 control evidence; OPS-10 decommission with in-flight commands.

## Traceability matrix fields
TestId; RequirementIds; WidgetIds; Risk; Fixture; Device/Browser; Actor; SponsorScope; APIContractVersion; ExpectedVisibleState; ExpectedServerState; ExpectedAuditEvidence; AutomationOwner; ExecutionResult; EvidenceUrl. Do not mark 'pass' without executed evidence. Link existing W01 and W02 acceptance IDs to suites above.

## Phase 0: feasibility spike
- Inspect current Limen WASM and Forma APIs, module startup behavior, bundle size, component packaging and routing.
- Prove iframe render with multiple instances and responsive sizing.
- Validate authentication without third-party cookies across Safari/iOS, Firefox and Chromium.
- Verify CSP, origin messaging, keyboard/screen-reader behavior and reduced-motion.
- Threat model parent compromise, clickjacking, replay, session confusion, data leakage and denial of service.
Exit: technical feasibility report with measured findings, code references, risks and go/no-go.

## Phase 1: read-only Fund Summary
- F# typed manifest and view models; trusted backend launch and scoped read.
- Synthetic fund fixtures: funded, unfunded, restricted, stale, partial, revoked, multi-custody, pooled investment.
- Forma compact/standard/expanded layouts, nonblank Limen loading.
- Integration harness and documentation.
Exit: security/accessibility tests and contract fixtures pass in sandbox, no production claims.

## Phase 2: Grant Recommendation sandbox
- Reuse first-party grant experience contract.
- Canonical charity search, drafts, amount/percentage, multi-source allocations, policy preview.
- Server-side authority and sponsor acceptance semantics; idempotent submission receipt.
- Failure fixtures: revoked rights, stale NAV, ambiguous charity, accepted-after-timeout, parent reload, lost connection.
Exit: integrated negative tests pass; sponsor operations can review recommendation independently.

## Phase 3: partner pilot
- Sponsor-approved partner and legal terms, origin/federation onboarding, support and incident ownership.
- Accessibility and usability testing with actual users, safe synthetic or approved pilot data.
- Monitor completion, latency, errors, support burden, command receipt resolution and user comprehension.
Exit: documented sponsor, security, privacy, legal and operations signoff.

## Phase 4: extension
- Fund opening, contribution, reports, giving history, advisor multi-client.
- Web Component wrapper only after proof of need and security.
- Headless APIs with partner conformance certification and audited UX responsibility.
- Operations widgets only after separate privileged threat model and SoD enforcement.

## Release blockers
No live financial command until trusted authorization, policy revalidation, double-spend prevention, durable outbox, provider unknown-state handling, audit evidence and reconciliation are verified. Existing financial-core design identified unresolved release risks; UI success cannot override them. No claims of SOC 2 compliance from a document or logging alone.

## Additional design research
Test whether a compact summary encourages mistaken interpretation of available funds; whether partner users understand who the sponsor is; whether embedded workflows suffer from authentication handoff; whether multi-widget dashboards create excessive WASM startup cost; whether custom element integration genuinely reduces partner work; and whether headless partners can preserve legal disclosures and accessibility. Use controlled experiments and record contrary evidence.
