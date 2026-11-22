# DAF UX: Requirements Traceability, Challenges and Build Gates v0.2

Status: design plan, no implementation claims.

## Traceability schema
Every requirement must map to:
- requirement ID, version, owner, rationale, role and legal scope
- journey and screen IDs
- Forma component IDs and design tokens
- F# view model / command DTO and API contract
- domain policy and authorization controls
- normal/empty/loading/stale/offline/conflict/error states
- accessibility criteria and tested assistive technologies
- privacy classification and retention/telemetry rules
- acceptance test IDs and evidence links
- release gate and current verified status

No requirement is 'Done' merely because a mockup exists. Valid status values: Proposed, Reviewed, Approved, Implemented, Tested, Evidence-verified, Released, Deferred (with reason).

## Risk-weighted backlog
P0: common shell/context isolation; donor grant flow; charity search/identity; multi-source allocation; case evidence/decision; financial status; reconciliation; liquidity hierarchy; payment unknown states; authorization and audit. These are safety- and trust-critical.
P1: contributions, complex gift, investment mandates, reporting, family access, professional advisor workspace, accessibility refinements, notification center.
P2: sponsor analytics, advanced white labeling, bulk operations, workflow personalization, cross-organization benchmarking where legally permitted.

## 36 executable test scenarios to author
T01 startup visible without blank; T02 320px navigation; T03 400% zoom; T04 keyboard-only wizard; T05 screen reader labels; T06 high contrast; T07 reduced motion; T08 no color-only status; T09 donor fund switch cache isolation; T10 unauthorized deep link; T11 recipient alias ambiguity; T12 stale charity evidence; T13 ineligible charity; T14 amount minimum; T15 percentage denominator changes; T16 allocation rounding; T17 insufficient resource; T18 draft refresh resume; T19 offline draft no submit; T20 duplicate tap idempotency; T21 network timeout after command accepted; T22 revoked advisor authority; T23 concurrent draft conflict; T24 case evidence contradictions; T25 AI hallucinated source; T26 prompt injection in charity text; T27 separation of duties; T28 provider unknown status; T29 changed banking destination; T30 stale custody feed; T31 reconciliation timing variance; T32 shared pool constraint display; T33 close/post race; T34 read-only auditor; T35 Folio accessible report; T36 cross-tenant search/notification leakage.

Each test records fixture, device/browser, actor and legal context, API revision, expected visible outcome, expected server outcome, audit evidence and actual result. Tests are currently **specifications only**.

## Explicit assumptions and counterexamples
A1 'Mobile first means every dense table fits on a phone.' False: progressive disclosure and equivalent capability are required.
A2 'The donor balance is what can be granted.' False: sponsor policy, restrictions, reserves and timing govern recommendations.
A3 'A unified dashboard eliminates navigation.' False: decision context and task continuity matter more than dashboard density.
A4 'AI can summarize evidence sufficiently for approval.' False: citations can be incomplete or contradictory; humans need source inspection.
A5 'Role-based hiding is secure.' False: API and database authorization must be independent.
A6 'An external provider timeout is a failure.' False: it may have executed; retry is unsafe without reconciliation.
A7 'White-label customization is harmless.' False: it can degrade contrast, disclosures, terminology and support.
A8 'One design system ensures consistency.' False: version drift and unverified component contracts undermine consistency.
A9 'A successful demo proves accessibility.' False: assistive technology and keyboard tests are required.
A10 'More configuration means more enterprise value.' Not necessarily: each option adds policy and support complexity.
A11 'AI should be visible everywhere.' False: AI is valuable where it reduces work and exposes evidence; unnecessary chatbot surfaces distract.
A12 'A percentage allocation is self-explanatory.' False: denominator, timing, rounding and source restrictions must be explicit.

## Required UX governance
- Design system steward owns component contracts and accessibility.
- Product owner owns workflow simplification and measurable user outcomes.
- Domain policy owner approves financial semantics and irreversible actions.
- Security/privacy owner approves telemetry, caching, context switching and external content rendering.
- Compliance/legal reviews sponsor claims, tax acknowledgments, disclosures and role permissions.
- Evidence owner maintains SOC 2 control execution records with audit trail.
- Every proposed automation must show what it replaced, what controls remain, and how exceptions are escalated.

## Release gates
UX-G0 Requirements approved with role and policy ownership.
UX-G1 Forma/Limen/Folio capability audit complete; no assumed API features.
UX-G2 Design tokens, responsive shells, component interaction and accessibility tests pass.
UX-G3 Three vertical slices work with mocked API responses for all failure states.
UX-G4 Representative user testing, including assistive technologies, produces measured findings and remediation.
UX-G5 Integrated API authorization, financial invariants, idempotency and crash-recovery tests pass.
UX-G6 Security review covers cross-tenant caches, prompt injection, XSS, sensitive telemetry and export scope.
UX-G7 SOC 2 controls have executed evidence; operational readiness and incident drill pass.
UX-G8 Sponsor policy/legal signoff for live financial actions, separately gated from UI release.

## Next detailed requirement expansions
1. Professional advisor multi-client journey, household/entity rights and delegation.
2. Contributions and complex asset intake with due diligence and tax-acknowledgment semantics.
3. Investment portfolio and custody journey with mandate controls and corporate actions.
4. Charity registry evidence/eligibility operations and source freshness.
5. Payment preparation, bank-change verification, return and unknown outcome.
6. Reporting/Folio accessibility, statements, disclosures and data lineage.
7. Partner white-label onboarding and tenant provisioning with non-bypassable controls.
8. AI workflow decision package evaluation and evidence quality metrics.
9. Operational resilience: disaster recovery, stale feeds, incidents, support and status messaging.
10. End-to-end user research and design review feedback loop.

## Implementation prohibition
Do not enable live grants, trades, payment instructions, accounting closes, or AI financial decisions based solely on these UX documents. Financial core release gates remain independent and mandatory.
