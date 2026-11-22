# DAF UX: Remaining Domain Journey Contracts v0.2

Status: proposed. This document completes the first-pass journey requirements beyond the three detailed vertical slices. Each journey must later receive role-specific wireframes, mock API fixtures, and tested accessibility behavior.

## J-ADV Professional advisor multi-client service
Actor: advisor with independently verified authority over multiple funds, potentially across sponsors. Start from an explicitly scoped client list, never a global list. Tasks: identify client, compare authorized funds, draft recommendation, obtain client/sponsor approval as required, review pending work. Show which legal entity owns each fund, which sponsor policy applies, and the advisor's effective rights. Context switching invalidates caches and queued commands. Failure cases: revoked rights, same-name clients, cross-sponsor data leakage, conflict between client instruction and advisor delegation. Tests: scoped search, role switch, permission expiry, deep-link denial.

## J-CON Contribution and complex asset intake
Actor: donor/gift officer. Select cash, marketable securities, closely held business interest, real estate, digital asset or other accepted category, based on sponsor policy. Explain that proposed, accepted, transferred, valued, disposed and acknowledged are distinct. Complex asset flow gathers ownership, restrictions, potential liabilities, valuation support and diligence; do not claim a deduction amount or issue a tax receipt prematurely. Provide a clear checklist of required documents, upload progress, security scan and source provenance. Failure: missing title, unsupported asset, custody delay, rejected acceptance, amended valuation. Tests: draft resume, file validation, role restrictions, acknowledgment timing.

## J-INV Investment and custody management
Actor: authorized investment manager, advisor, treasury or donor with view-only rights. Present mandates, custody account observations, positions, tax lots, liquidity, corporate actions, fees and performance with valuation timestamps. Separate investment recommendation from order authorization, provider submission, execution and settlement. Show account integration capabilities (read, order, cancel, transfer) only when contractually verified. Failure: stale feed, unsupported order, partial execution, price revision, missing corporate action, account mismatch. Tests: read-only role cannot trade, no implied real-time holdings, corporate action reconciliation, provider unknown status.

## J-CHA Charity registry and eligibility
Actor: charity analyst. Search canonical charity record, EIN, aliases, relationships, sources, eligibility history and source freshness. Internal registry owns canonical state; external data is ingested with provenance and does not automatically overwrite reviewed decisions. Evidence workspace highlights contradictions, source authority, review age, reason for status, and appeal/recheck route. Failure: duplicate EIN/identity, inactive charity, renamed organization, foreign equivalency, sanctions conflict, stale source. Tests: evidence traceability, versioned decision, no fabricated verified badge.

## J-PAY Payment preparation and returns
Actor: authorized operations/treasury. Begin from approved grant and funded obligation; display recipient destination verification, authorized amount, account source, hold flags and required second approval. Separate instruction creation, provider attempt, status observation, confirmed settlement, returned funds and reconciliation. Unknown provider outcome freezes unsafe retry and releases. Bank detail changes trigger independent verification. Failure: duplicate submission, partial return, rejected payment, sanctions hold, provider outage. Tests: no 'Paid' without evidence, no double pay, safe incident recovery, accessible review.

## J-REP Reporting, statements and Folio
Actor: donor, advisor, finance, auditor or sponsor executive. Define report purpose, legal scope, audience, period, accounting/valuation basis, confidentiality and redaction. Show preview, as-of time, data gaps, generation progress and document version. Folio output must be accessible and preserve reading order, tables, footnotes and provenance. Failure: source stale, large report delayed, permission revoked during generation, partially unavailable data, export interrupted. Tests: audience-specific redaction, report traceability, keyboard and screen reader, repeatable version.

## J-PART Partner and tenant onboarding
Actor: platform administrator and authorized partner. Configure legal entity, sponsorship model, brand tokens, disclosures, permitted workflows, custody/payment adapters, data residency, retention and tenant isolation. Use staged activation with explicit checklists. Mandatory controls cannot be disabled by branding or partner configuration. Failure: incompatible logo contrast, missing disclosures, unverified integration, wrong legal-entity mapping, tenant provisioning rollback. Tests: cross-tenant isolation, branded accessibility, safe configuration revision.

## J-AI Decision preparation and challenge
Actor: operations analyst and supervisor. AI may assemble evidence, propose next action, detect contradictory source data and draft communications. It cannot self-certify charity eligibility, approve grants, execute trades/payments or hide contradictory evidence. Display source-linked factual assertions, policy engine results separately, limitations, model/version and review feedback. Provide 'challenge recommendation' and correction path. Failure: fabricated citation, outdated policy, retrieved prompt injection, irrelevant recommendation, AI unavailable. Tests: deterministic denial still blocks AI-suggested action, evidence citations resolve, fallback without AI.

## J-OPS Incidents and resilience
Actor: donor or internal operations. Show actual service health, stale data, planned maintenance, safe read-only behavior, support reference and incident communication status. Distinguish client connectivity from provider processing. Never say an action failed merely because UI lost its connection. Staff can view incident-linked case backlog and recovery status. Failure: WASM load error, token expiry, partial service outage, event lag, duplicate notifications, inconsistent cross-region observations. Tests: safe retry, clear unsent vs accepted state, no secret leakage in support bundle.

## J-RES User research and feedback
Actor: product research, real donors, advisors and staff. Test comprehension of grant status, financial availability, evidence review, error recovery and mobile accessibility. Collect task success, time, help needed, error rates, confidence and qualitative comments. Segment by role, familiarity, accessibility needs and device. Treat conflicting observations as evidence of different user contexts rather than averaging away. Do not collect confidential financial data in session recordings without explicit governance. Tests: usability evidence linked to requirements and remediations.

## Remaining cross-domain questions to resolve
- What exact sponsor policy determines 'available to recommend' and percent denominators?
- Which rights can advisors exercise across sponsor/legal-entity boundaries?
- Which charity evidence sources are authoritative for each eligibility determination?
- What tax acknowledgment wording and timing is approved by counsel?
- Which custody/payment provider capabilities are contractually available?
- What reporting data lineage is required for audited and donor-facing statements?
- What retention and offline draft policy is acceptable for sensitive data?
- What are validated Forma/Limen/Folio API capabilities, not just desired features?
- Which actions require dual control, and can partner configuration only strengthen it?
- What user research thresholds justify design approval?

No technical or regulatory capability is asserted as verified here.
