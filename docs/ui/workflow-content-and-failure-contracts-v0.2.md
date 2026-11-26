# DAF UX: Workflow, Content and Failure Contracts v0.2

Status: proposed requirements, not implemented. Applies to donor, advisor, operations, investment, finance, compliance, platform administration.

## Task-first workflow simplification protocol
For every step record: user intent, information required, authoritative source, whether the platform can retrieve it, whether policy can decide it, whether independent approval is mandatory, and evidence produced. Delete inherited administrative steps that serve no present legal, financial, safety or user purpose. If a step is removed, prove that required controls remain enforced.

## Workflow patterns
- Guided transaction: draft -> preview -> explicit submit -> accepted receipt -> asynchronous tracking.
- Evidence-led decision: case assembled -> contradictions shown -> deterministic policy checks -> authorized decision -> audit event.
- Reconciliation: compare independent observations -> classify variance -> propose correction -> approval -> posting -> recheck.
- Delegation: select legal scope -> choose capabilities and effective dates -> identity verification -> approval -> invite -> audit -> revoke.
- Report generation: select audience/scope/period -> preview/redaction -> asynchronous generation -> accessible Folio output -> audit.
- Complex gift: intake -> risk/diligence -> sponsor acceptance -> custody receipt -> valuation -> disposition -> acknowledgment. No premature tax receipt claim.
- Investment instruction: mandate checks -> exposure/liquidity preview -> independent authorization -> provider submission -> execution observation -> settlement -> reconcile.

## Failure-state catalog
| Code | State | User explanation | Required action |
|---|---|---|---|
| UX-F01 | WASM loading | 'Loading your workspace' plus meaningful progress | fallback and retry after defined timeout |
| UX-F02 | No data | Explain why empty and available first action | authorized creation/search |
| UX-F03 | Stale observation | Show source and last observed time | refresh or continue read-only |
| UX-F04 | Partial data | Identify missing sources and affected calculations | retry only missing reads |
| UX-F05 | Offline draft | 'Saved on this device' only if actually stored | resume/sync, never imply submitted |
| UX-F06 | Unsaved changes | Explicit save status and navigation warning | save/discard/stay |
| UX-F07 | Invalid field | Localized field message and error summary | correct and focus |
| UX-F08 | Revision conflict | What changed and which edits remain | compare/reapply safely |
| UX-F09 | Permission revoked | Action unavailable; preserve only permitted draft data | request access or return |
| UX-F10 | Eligibility changed | Source, effective date, changed rule | re-evaluate recipient |
| UX-F11 | Liquidity changed | Amount, basis and new constraints | re-preview allocations |
| UX-F12 | Command accepted | Reference ID and next expected state | track status |
| UX-F13 | Command rejected | Explain reason without sensitive disclosure | correct or escalate |
| UX-F14 | External status unknown | Distinguish from failed or settled | investigation, no unsafe retry |
| UX-F15 | Partial batch outcome | Per-item accepted/denied/unknown | inspect individual receipts |
| UX-F16 | Report generation delayed | Actual job status and request reference | resume/retry safely |
| UX-F17 | Inaccessible evidence | Alternative text/transcription request | escalate evidence accessibility |
| UX-F18 | Tenant context changed | Clear stale scoped views | re-fetch authorized data |
| UX-F19 | Security hold | Policy-safe reason and review owner | escalate, never bypass |
| UX-F20 | Incident/maintenance | Honest scope and data freshness | safe read-only if permitted |

## Financial language glossary
- Fund value: market/valuation-based assets net of applicable liabilities under a stated methodology.
- Recommendable amount: sponsor-policy amount eligible for recommendation; not necessarily settled cash.
- Confirmed settled cash: verified cash position under a defined cutoff.
- Reserved/encumbered: amount held against authorized pending obligations.
- Projected liquidity: forecast, not guaranteed available cash.
- Grant recommendation: donor/advisor request to sponsor; not a binding payment instruction.
- Approved grant: sponsor decision; not proof of payment.
- Payment instruction: authorized order; not proof provider received it.
- Payment processing: external state, subject to provider confirmation.
- Paid/settled: supported by verified settlement evidence and reconciliation policy.
- AUM/AUA/RAUM: distinct metrics with explicitly versioned definitions and eliminations.

## Accessibility details
- Every error linked to field and announced in an error summary.
- Status updates use restrained live regions, no noisy repeated announcements.
- Financial charts include table alternatives and patterns/labels, not color alone.
- Evidence PDFs require accessible text or equivalent alternate view; Folio export must preserve headings and reading order.
- Session expiry warnings are accessible and allow extension where policy permits.
- Authentication must support accessible methods; never require a puzzle without an alternative.
- Keyboard focus after wizard transitions, case tab changes, modal close and validation errors is deterministic.
- Language and reading level are tested with representative donors and staff; legal disclosures remain accurate.

## Privacy and ethical AI
- AI drafts and deterministic eligibility decisions are visually and semantically distinct.
- No AI confidence percentage without calibration evidence; prefer 'Source evidence incomplete' and explicit contradictions.
- Citation links open authorized source snapshots, not arbitrary public content that may change.
- The system must show when an AI suggestion was accepted, edited or rejected; no auto-approval from generated summaries.
- Users can challenge a decision and see the available review path.
- Prompt injection from external charity descriptions, uploaded files and emails must not alter policy or authority.

## User research and success measures
Recruit donors (including low technical familiarity), professional advisors, grant analysts, finance controllers, and accessibility users. Test realistic tasks with incomplete evidence, interrupted connectivity, and changing permissions. Measure completion rate, error rate, time, assistance requests, confidence in understanding financial status, and error recovery. Establish baselines before setting performance targets. Document user disagreement rather than flattening it into a single persona.

## Content governance
Every consequential label and template has an owner, revision, localization status, legal/policy review status, effective date and rollback path. White-label partners can customize tone and approved terms, not legal meanings or mandatory disclosures. Never put sensitive donor data in email subject lines or push notification previews.
