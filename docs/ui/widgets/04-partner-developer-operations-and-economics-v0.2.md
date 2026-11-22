# Embedded DAF Experiences: Partner, Operations and Commercial Requirements v0.2

Status: proposed, no integration commitments or commercial terms verified.

## Partner lifecycle
Prospect -> qualification -> sponsor authorization -> legal/data agreement -> identity federation -> origin registration -> sandbox -> contract and accessibility tests -> security approval -> pilot -> production -> ongoing review -> suspension/termination. Every stage has owner, evidence, prerequisites, expiry and rollback. Partner cannot self-enable privileged scopes.

## Partner console
P-01 Register organization and verified domains.
P-02 Bind sponsor/legal entity and contractual service scope.
P-03 Register exact allowed origins per environment, with change approval.
P-04 Configure OIDC/SAML or other supported federation and subject mapping; prove actual capability.
P-05 Select permitted widgets and capabilities; no broader than sponsor grant.
P-06 Configure branding tokens, logos, legal disclosures and locale with accessibility preview.
P-07 Configure webhook endpoints and verification keys where needed.
P-08 Generate sandbox credentials and synthetic fixtures; never expose production secrets.
P-09 View integration health, source freshness, failed launches and safe audit traces.
P-10 Request additional capabilities with review/approval.
P-11 View version compatibility, deprecation notices and change logs.
P-12 Manage support contacts, incident escalation and on-call responsibility.
P-13 Inspect usage/billing metrics with reconciliation and dispute path.
P-14 Revoke keys, suspend widget, rotate signing keys, and terminate integration safely.

## Partner SDK and documentation
Provide minimal embed snippet, versioned loader, typed events, supported browser matrix, CSP guidance, accessibility checklist, example responsive layouts, secure session bootstrap backend examples, error catalog, sandbox examples, webhook replay fixtures and test harness. F# reference implementation for partner server where possible; other languages may be documented without changing core F# preference. Do not promise Web Components until Limen/Forma behavior validated.

## Commercial hypotheses
H1 Sponsoring organization pays platform and widget license.
H2 Wealth manager pays for embedded distribution and advisor workspace.
H3 Infrastructure partner pays usage and platform minimum.
H4 Administration-as-a-service bundles staff operations and software.
H5 Transaction-based pricing only when lawful, commercially appropriate and not incentivizing unsafe behavior.
Measure per-partner implementation cost, maintenance, security support, active users, session starts, accepted recommendations, support load, conversion to funded funds, and sponsor net revenue. Separate commercial attribution from donor-sensitive telemetry.

## Support responsibility matrix
Authentication failure: partner identity team plus platform widget support.
Authorization/policy denial: sponsor service owner, platform provides evidence.
Grant recommendation state: sponsor grants operations.
Financial values: sponsor accounting/custody team.
Widget rendering/accessibility: platform engineering.
Provider payment unknown: sponsor treasury/payment operations.
Incident notification: named platform and partner communications owners.
Fraud/privacy incident: incident command under contract, with regulatory obligations reviewed by counsel.

## Operational control requirements
- Monitor launch exchange success, unauthorized attempts, session expiry, data freshness, UI errors, command receipt lag, provider reconciliation and cross-origin violations.
- Feature flags scoped by partner/widget/version, with emergency disable that preserves accepted commands and audit.
- Support reproducible synthetic fixture without exposing donor data.
- Retain actual SOC 2 control execution evidence for origin approvals, key rotation, access reviews, deployment, incident drills, change management, and third-party reviews.
- Version migration must preserve legal disclosures and ability to retrieve historic receipts.
- Decommission must revoke access, preserve required records, and reconcile in-flight operations.

## Partner research questions
Which wealth-management portals allow iframe embedding? Which require approved app marketplaces? Which support delegated user identity? Who is legally permitted to recommend grants? Which partner wants full fund opening versus a simple giving card? Is there a commercial need for headless only? What customer support brand should appear? What consent and data sharing is required? Interview partners rather than assume platform capabilities.
