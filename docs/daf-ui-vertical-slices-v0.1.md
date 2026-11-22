# DAF UI Vertical Slice Contracts v0.1

Status: **PROPOSED DESIGN CONTRACTS, NOT IMPLEMENTED**. Companion to [UI inventory](daf-enterprise-ui-requirements-v0.1.md) and [financial safety controls](financial-core-control-spec-v0.5.md). Target stack F#, Limen WASM, Forma UI, Folio reporting. Design direction: balanced charcoal/bronze; all contrast and interaction behavior must be verified.

## 0. Shared interaction contract

### Common shell
Every authenticated view includes (1) clear organization/legal-entity and fund context, (2) role and authority context where relevant, (3) navigation optimized for the current role, (4) notifications with unread/priority distinction, (5) help and accessible feedback, and (6) last refresh or as-of time when showing changing financial data. Context changes cancel pending reads, partition caches, discard sensitive view models, and revalidate all actions. Never rely on UI filtering for authorization.

### Design tokens and responsive behavior
Use semantic tokens, not hard-coded color meaning: background/surface/text-primary/text-secondary/border/action-primary/action-danger/status-success/status-warning/status-unknown/focus-ring. Charcoal/bronze is a brand theme, not a license for low contrast. Test at 320, 375, 768, 1024, 1440 CSS pixels, 200% and 400% zoom; reduced motion, high contrast, screen reader, keyboard, touch. Prefer 44px touch targets where practical, while WCAG 2.2 AA minimums remain binding. No horizontal *page* scroll on narrow devices; specialized financial grids may use explicitly labeled internal scroll regions with equivalent summary/drilldown.

### Common state matrix
Loading (nonblank branded shell, meaningful progress), Ready, Empty (explain how to begin), Partial (show which data is missing), Stale (time + explicit refresh), Offline (read-only vs queued draft clearly distinguished), ValidationError (field and summary), Conflict (what changed and safe resolution), Unauthorized (no sensitive detail), Held (why, owner, next step), UnknownExternalOutcome (no retry button unless safe), Success (reference + next step), FatalError (safe recovery and support reference). All command responses carry correlation ID; the UI does not invent success.

### Common component contracts
- Forma.AppShell: responsive nav, semantic landmarks, focus restoration, explicit entity context.
- Forma.MoneyWithBasis: value, currency, metric kind, as-of, precision, source, availability constraints, loading/stale.
- Forma.StatusExplanation: human-readable state, reason, responsible party, next action, effective/observed times.
- Forma.WorkflowStepper: step metadata, server draft revision, autosave status, conflict recovery, back/forward.
- Forma.AllocationEditor: source rows, fixed or percent allocation, valuation basis, rounding remainder, caps, restrictions, preview.
- Forma.DecisionPackage: primary facts, contradictory evidence, policy checks, AI-generated suggestions separately labeled.
- Forma.EvidenceViewer: source provenance, snapshot, freshness, contradictions, accessible document alternative.
- Forma.TransactionReview: authorized action, irreversible effects, exact resource/recipient, idempotency token, confirmation.
- Forma.ReconciliationDiff: three perspectives (custody observation, investment accounting, GL), discrepancy, tolerance, evidence.
- Forma.FolioPreview: permission-aware accessible preview/export, period, as-of, scope, watermarks.

### Telemetry and privacy
Instrument step completion, abandonment, latency, validation failure, retry, exception resolution, accessibility defects. Do not send charity banking information, sensitive donor notes, authentication tokens, full account numbers, or raw AI prompts into generic telemetry. Trace consequential actions to a policy/control evidence record, with actor, authorization decision, data revision and outcome.

### API conventions (proposed, not implemented)
All reads return `contextRevision`, `asOf`, `dataFreshness`, `permissions`, and typed status where applicable. Commands use `commandId`, `idempotencyKey`, `expectedRevision`, and `requestHash`; the server derives principal/tenant/legal authority from trusted authentication. The client may supply a requested context identifier but cannot assert authorization. Conflict is explicit; provider unknown state is distinct from failure. Data minimization applies to every response.

## 1. Donor home + grant recommendation (D01, D03-D07)

### Actor, job, outcome
Donor or delegated advisor with effective-dated grant-recommendation rights. Job: recommend an eligible charitable grant and understand its progress. Outcome: accepted **recommendation**, not an approval or payment. The sponsor retains approval authority.

### Navigation and information hierarchy
Home: fund name and current context > available-to-recommend amount with policy basis > prominent 'Recommend a grant' > pending requests requiring attention > giving history > portfolio overview. Show total fund value separately; never label market value as spendable cash. If availability cannot be calculated, display 'Unavailable as of [time]' with a reason, not $0.

Grant wizard as one route with four logical steps:
1. Recipient: verified identity and EIN, aliases, geography, eligibility evidence/freshness, previous giving. Ambiguous matches require explicit selection. Ineligible or unresolved charities show explanation and possible review request, not false approval.
2. Amount and purpose: fixed dollar amount or percentage with an explicit denominator and valuation timestamp; donor purpose and anonymity/preferences; grant frequency if enabled. Explain policy minimums and restrictions.
3. Funding: allocate a fixed amount or percent across permitted cash/portfolios/positions. Source-specific available capacity, settlement lag, pricing uncertainty, fees, concentration and restrictions. Live validation sums to 100% (or exactly the grant amount), deterministic rounding remainder, prevent stale preview from being treated as a lock.
4. Review and submit: recipient legal identity, total amount, source allocation, valuation basis, purpose, sponsor approval requirement, potential liquidation, estimated timing only when evidence supports it. Explicit 'Submit recommendation'; confirmation shows recommendation ID and tracking link.

### Mobile composition
Sticky accessible step indicator, one primary action at a time, compact recipient summary, expandable allocation cards with percentage/dollar toggle, numeric keypad appropriate to locale, persistent draft-save state, bottom action area that does not obscure keyboard or content. Desktop can show recipient/evidence side panel and allocation table. No reliance on drag-only interactions.

### Data dependencies
`GET /ui/funds/{fundId}/home` -> FundHomeView {fundValue, recommendableAmount, calculationPolicyVersion, asOf, outstandingRequests, roleRights}.
`GET /ui/charities/search?q=` -> CharityCandidate {canonicalId, name, EIN, aliases, eligibilityState, evidenceAsOf, matchReason}.
`POST /ui/grant-drafts`, `PATCH /ui/grant-drafts/{id}` -> Draft {revision, validationIssues, autosaveAt}.
`POST /ui/grant-drafts/{id}/funding-preview` -> FundingPreview {basis, valuationAsOf, allocations, limits, warnings, expiresAt, revision}.
`POST /commands/grant-recommendations` -> CommandReceipt {recommendationId, state, correlationId}; must revalidate eligibility, authority, and liquidity at execution boundary.
`GET /ui/grants/{id}/timeline` -> independent recommendation/approval/funding/payment states.

### Failure/edge states
Charity record ambiguous; charity eligibility changes between preview and submission; insufficient liquidity; percentage basis changes as NAV moves; portfolio restriction; grant draft saved offline but not submitted; delegated rights revoked mid-flow; two concurrent edits; duplicate taps; timeout after accepted command; backend returns unknown command status; cross-fund context change; browser back; screen reader announces validation; 400% zoom allocation.

### Acceptance tests
D-GR-01 Fixed-amount recommendation with accessible confirmation and ID.
D-GR-02 Percentage basis displays denominator and as-of; changed valuation requires renewed preview.
D-GR-03 Multi-source amounts and percentages sum exactly after rounding; disallowed source blocked.
D-GR-04 Server rejects stale authority/eligibility regardless of client state.
D-GR-05 Double submit/timeout returns same command receipt, not two recommendations.
D-GR-06 Draft resumes after refresh/offline; no offline financial submission claim.
D-GR-07 Full keyboard/screen-reader/400% zoom workflow.
D-GR-08 Tracking distinguishes submitted, approved, funding, paid, returned, held, unknown.
D-GR-09 No financial value rendered without currency, basis, and freshness.

## 2. Operations case workbench (O01-O07, O10-O12)

### Actor, job, outcome
Grant officer, charity verification analyst, payment operations specialist, or supervisor. Job: safely resolve an actionable case without navigating disconnected systems. Outcome: documented decision with evidence and correct handoff; no unauthorized execution.

### Layout and priority
Desktop: left case queue, center case narrative/timeline, right evidence/decision panel. Mobile: one-pane stack with explicit Queue / Case / Evidence / Decision tabs, preserving focus and selection. Queue shows actionable priority, due time, owner, current blocker, and policy-based sorting; AI priority score is explainable and never sole decision criterion.

Case header: legal entity, fund, recipient, amount/basis, state, authority, SLA, latest evidence timestamp, hold flags. Decision panel: required policy checks, contradictions, missing evidence, previous decisions, authorized actions, mandatory review separation. AI summary is marked 'Draft analysis' and links each factual assertion to evidence.

### Operations sequence
Intake -> identity resolution -> eligibility evidence -> policy checks -> sponsor approval -> funding plan -> verified destination -> payment preparation -> external status observation -> reconciliation -> close. These are independently stateful; an approval cannot imply settlement. The UI must not collapse an unknown provider status into 'Failed'.

### Decision actions
Approve, request information, hold, decline, escalate, assign, prepare payment, release hold (only under authorized recovery policy). Each action has a consequence preview, reason taxonomy, supporting evidence, policy version, separation-of-duties check, and immutable receipt. Batch actions must report per-item outcomes and refuse heterogeneous authority/eligibility assumptions.

### Data dependencies
`GET /ui/work-queue` -> prioritized CaseSummary with role-filtered actions.
`GET /ui/cases/{id}` -> CasePackage {facts, evidence, contradictions, policyChecks, proposedActions, stateRevision, externalStates}.
`GET /ui/cases/{id}/evidence` -> source metadata and access-controlled snapshots.
`POST /commands/case-decisions` -> command receipt with authorization and expected revision.
`GET /ui/payments/{id}` -> payment instruction, attempts, provider observations, settlement evidence, returns.
All AI outputs include model/version, prompt-template version, retrieval provenance, timestamp, and deterministic policy-check result separately.

### Failure/edge states
AI cites nonexistent source; conflicting charity identities; changed bank destination; evidence expires while case open; two analysts decide concurrently; approver also prepared case (separation-of-duties); legal entity changes; external provider timeout; payment return; inaccessible scanned document; stale queue; batch partial success; malicious text in retrieved charity data attempting prompt injection.

### Acceptance tests
O-CASE-01 All facts and contradictory evidence inspectable from one case workspace.
O-CASE-02 AI suggestions never become decisions without authorized explicit command.
O-CASE-03 Missing evidence blocks decisions according to versioned policy.
O-CASE-04 Separation-of-duties enforced server-side even if client modified.
O-CASE-05 Provider timeout displays Unknown; no unsafe retry action.
O-CASE-06 Case assignment and concurrent decision conflict are recoverable.
O-CASE-07 Mobile and keyboard users can inspect evidence and decide.
O-CASE-08 Changed payment destination triggers independent verification.
O-CASE-09 Batch result is per item, including skipped/denied/unknown.

## 3. Financial control workspace (E03-E06, E07-E08, E16, E18)

### Actor, job, outcome
Controller, treasury officer, reconciliation analyst, auditor, security administrator. Job: see whether financial positions reconcile, understand resource constraints, close periods safely, and resolve exceptions with traceable evidence.

### Core tabs
Overview (financial health, held resources, unresolved differences, stale feeds), Liquidity (fund/pool/custody resource hierarchy), Reconciliation (custody observation vs investment accounting vs general ledger), Journals (posted/reversed, no editing), Period Close (preflight/approvals/close status), Audit (control execution and evidence). Role-dependent tabs; all API calls still authorize independently.

### Financial metrics
Every metric declares measurement kind (confirmed settled cash, projected liquidity, encumbered, available, fund NAV, AUM, AUA, regulatory AUM), unit, effective date, observation time, freshness, source and consolidation rule. AUM/AUA/RAUM are distinct, with pooled holdings eliminated from aggregate double count. Reconciliation displays source timing and tolerance, not simply a green/red match.

### Liquidity hierarchy
Represent shared constraints as a directed acyclic graph, not an assumed tree. Show each resource's capacity, claims, inherited constraints, other competing obligations, data freshness and remaining headroom. UI projections cannot establish capacity; reservation commands must lock all constrained scopes and revalidate server-side. Visual warning when constraints overlap; avoid double counting in rollups.

### Period close interaction
Preflight lists unposted journals, open reconciliations, pending external settlements, adjustment policy, unresolved holds, approver requirements. Preview includes impacted books, effective accounting dates, and exceptions. Close command requires expected revision and approved authority; concurrent backdated postings must be blocked by database policy. Confirmation shows period ID, close timestamp, actor and evidence reference. Reopening, if permitted, is a separate audited workflow.

### Reconciliation interaction
Side-by-side sources with aligned instrument/account/currency/date, variances and provenance. User can classify timing difference, missing observation, incorrect mapping, unresolved provider event, or accounting adjustment proposal. No direct overwrite of a custodian observation or posted journal. Proposed corrections require an independent posting workflow and approvals.

### Data dependencies
`GET /ui/finance/overview`, `GET /ui/liquidity/resources`, `GET /ui/reconciliations/{id}`, `GET /ui/ledger/journals/{id}`, `GET /ui/periods/{id}/preflight`, `POST /commands/period-close`, `POST /commands/adjustment-proposals`, `GET /ui/controls/evidence`. API must return legal-entity/book scope and data freshness; no synthetic reconciled status when provider feed is missing.

### Failure/edge states
Stale custody observation, inconsistent valuation times, duplicate external event, unbalanced draft journal, close race with posting, attempted direct journal mutation, cross-entity aggregation without elimination, pool constraint cycle, missing SOC 2 control evidence, auditor read-only access, concurrent resolution conflict, inaccessible wide grid.

### Acceptance tests
E-FIN-01 Three financial perspectives displayed without conflation.
E-FIN-02 Unknown/stale feeds prevent false reconciled indicators.
E-FIN-03 Shared liquidity ancestor shown with aggregate competing claims.
E-FIN-04 Close preflight blocks incomplete dependencies and unauthorized action.
E-FIN-05 Concurrent close/post cannot both violate period policy.
E-FIN-06 Journal corrections use reversals, not edits.
E-FIN-07 Read-only auditor cannot mutate any financial resource.
E-FIN-08 AUM/AUA/RAUM labeling and pooled eliminations tested.
E-FIN-09 SOC 2 evidence shows executed control, owner, period and exceptions.
E-FIN-10 Mobile and accessible desktop provide equivalent decisions with progressive disclosure.

## 4. Design decision register

DEC-UI-01: Primary navigation is task/role-oriented, not technical domain-oriented. Proposed.
DEC-UI-02: Grant recommendation is a four-step single workflow; status tracked independently. Proposed.
DEC-UI-03: Case workbench merges queue, evidence and decision, with responsive one-pane mobile. Proposed.
DEC-UI-04: Finance UI preserves distinct observations, positions, ledger, and liquidity claims. Proposed.
DEC-UI-05: No AI-only financial decisions or automatic execution without verified delegated authority. Mandatory.
DEC-UI-06: No fabricated freshness, payment success, availability, or policy evidence. Mandatory.
DEC-UI-07: Performance budgets require measured device/network baselines. Pending.
DEC-UI-08: Percentage-based grant allocation basis and rounding rules require sponsor policy signoff. Pending.
DEC-UI-09: Brand tokens require accessible contrast verification. Pending.
DEC-UI-10: Shared Forma components must be verified in their current version before claiming implementation. Pending.

## 5. Acceptance gate and build sequence

Gate UX0: screen contracts, user journeys and permission matrices reviewed.
Gate UX1: Forma component API inventory verified; missing primitives specified.
Gate UX2: accessible static prototypes for all three slices; 320px and 400% zoom.
Gate UX3: mocked API contract tests including failure states, stale data and auth changes.
Gate UX4: user testing with donors, operations analysts and controllers; measure success, errors, confusion, and task duration.
Gate UX5: integrated financial engine tests, audit evidence, and role/tenant isolation; production release blocked until financial safety gates pass.

Sequence: implement shared shell and status primitives -> donor grant wizard -> operations case package -> finance reconciliation and liquidity -> cross-slice accessibility/performance tests -> consolidate design learnings into remaining 54 capabilities.

**No UI implementation, F# compilation, database test, or usability validation is claimed by this document.**
