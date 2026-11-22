# Widget W02: Grant Recommendation Detailed Contract v0.2

Status: proposed transactional widget contract, not implemented or authorized for live funds.

## Purpose and legal semantics
Enable authorized donor/advisor to **recommend** a grant within an embedded portal while the sponsor retains discretion and approval. Never describe submitting a recommendation as executing payment, approving a grant or guaranteeing tax treatment.

## Workflow
Step 0: validate session, effective advisory authority, sponsor/fund policy, widget capability and context.
Step 1 Recipient: internal charity registry search, canonical legal name/EIN, aliases, eligibility source, contradictions, ambiguous identity resolution, foreign or special recipient restrictions. Evidence freshness and sponsor review path.
Step 2 Grant: fixed amount or percentage with explicit denominator and as-of; purpose, anonymity, acknowledgement preferences, optional recurrence if policy supports.
Step 3 Funding allocation: choose permitted portfolios/accounts/investment pools, allocate by dollars or percentages, see restrictions, pending claims, settlement lag, valuation uncertainty and fees. Sum and rounding must be deterministic; preview is not a reservation or guaranteed available cash.
Step 4 Review: full recipient identity, sponsor, fund, actor capacity, amount and currency, valuation basis, allocations, purpose, restrictions, potential liquidation, sponsor approval disclaimer. Accessible explicit 'Submit grant recommendation'.
Step 5 Receipt: sponsor-accepted recommendation ID and tracking. If response is unknown, query idempotent command receipt; do not offer a fresh submit until status reconciled.

## Proposed typed DTOs
GrantDraft { DraftId; FundId; SponsorId; RecipientId option; AmountMode [FixedMoney|PercentOfPolicyBasis]; RequestedAmount decimal option; RequestedPercent decimal option; DenominatorKind option; ValuationAsOf option; Purpose; AnonymityChoice; AllocationLines; Revision; SavedAt; Expiry; ValidationIssues }
AllocationLine { SourceId; SourceType; AllocationMode; Amount decimal option; Percent decimal option; Currency; ValuationBasis; SourceAsOf; RestrictionCodes }
GrantPreview { DraftRevision; SponsorPolicyVersion; RecipientEligibilityVersion; AuthorityRevision; AllocationPreview; CalculatedAmount; RoundingMethod; Warnings; BlockingIssues; ExpiresAt; PreviewHash }
SubmitGrantRecommendation { DraftId; ExpectedRevision; PreviewHash; IdempotencyKey; RequestHash; AcknowledgedWarnings }
GrantRecommendationReceipt { RecommendationId option; CommandId; State [Accepted|Rejected|Unknown]; ReceivedAt; CorrelationId; StatusUrl }
Server derives actor and scope; client may not assert them.

## Financial invariants
- Currency and decimals typed; no floating-point money.
- Percent denominator defined: fund NAV, sponsor policy spendable base, specified portfolio value, or other approved basis. Never simply 'percent of account' without exact definition.
- Sum of allocation shares exactly 100% or requested amount under explicit rounding policy. Prevent negative, restricted, duplicate or stale sources.
- Shared liquidity ancestors and competing reservations evaluated by authoritative backend at command boundary.
- Revalidate recipient eligibility, authority, fund restrictions, policy and available capacity on submission. Expired preview must be regenerated.
- Recommendations do not necessarily reserve cash; whether and when a reserve occurs is a separate sponsor-approved financial state transition.
- Payment processing and settlement are downstream asynchronous workflows and never inferred from widget receipt.

## Security and session continuity
- Short-lived widget launch bound to partner, origin, subject, fund and W02 capability.
- Explicit step-up authentication or top-level handoff for high-risk cases as sponsor policy requires; no assumption that embedded login is sufficient.
- Autosave drafts only to approved server-side scoped store; any local draft caching must pass privacy/threat review and expiry controls.
- Revocation, fund switch, role change or partner suspension blocks submit and clears forbidden data.
- The parent may receive opaque accepted-command event but not recipient financial details, amount, purpose, bank destination or donor note.
- Idempotent command receipt lookup must resolve accepted-after-timeout and prevent duplicate recommendations.

## UX and accessibility
Mobile-first 320px+, four-step workflow with persistent save status, clear next/back, progress, error summary, accessible charity picker, numeric entry, allocation cards, explicit review. Desktop may show recipient/evidence side panel. At 400% zoom preserve actions; avoid drag-only allocation; announce status without excessive live-region noise.
Unknown status message: 'We cannot confirm whether your recommendation was received. Please check its status before trying again.' Link to actual command receipt investigation. Do not say provider payment failed.

## Failure matrix
GRW-F01 partner launch denied; F02 advisory rights expired; F03 charity identity ambiguous; F04 charity became ineligible; F05 fund restriction; F06 amount exceeds policy; F07 stale valuation; F08 insufficient liquidity; F09 allocation sum mismatch; F10 draft revision conflict; F11 session expires mid-review; F12 offline after autosave; F13 duplicate submit; F14 accepted but response lost; F15 sponsor policy changes; F16 parent host reload; F17 malicious charity text; F18 downstream payment unknown; F19 source custody feed missing; F20 unavailable accessibility evidence.
Each requires user explanation, safe action, command/audit semantics and test fixture.

## Acceptance criteria
GRW-01 correct legal language and sponsor disclosure.
GRW-02 canonical charity identity with ambiguity handling.
GRW-03 fixed amount valid and percentage denominator visible.
GRW-04 rounding deterministic across multiple allocations.
GRW-05 restricted source rejected server-side.
GRW-06 stale valuation invalidates preview.
GRW-07 eligibility change blocks stale submission.
GRW-08 revoked advisor blocked despite active iframe.
GRW-09 duplicate tap and lost response resolve to one command.
GRW-10 offline draft never falsely marked submitted.
GRW-11 review screen contains exact effect and limitations.
GRW-12 accepted receipt shows recommendation ID, not paid status.
GRW-13 partner bridge exposes only safe opaque events.
GRW-14 keyboard, screen reader, touch, zoom and reduced-motion pass.
GRW-15 host overlay/clickjacking controls tested.
GRW-16 multi-widget sessions isolated.
GRW-17 prompt injection in charity content does not affect policy.
GRW-18 fund switch invalidates draft submit capability.
GRW-19 concurrent edit conflict presents compare/reapply.
GRW-20 Folio confirmation/report available only under authorized scope.

## Rollout gates
Phase A: synthetic-data prototype with all error fixtures.
Phase B: secure launch, origin/session enforcement and server-side read-only data.
Phase C: server-side draft, preview, policy/authority validation and idempotent submission in sandbox.
Phase D: end-to-end sponsor review and financial invariants tested, independent security review.
Phase E: limited partner pilot with measured task success, accessibility, incident and recovery evidence.
Production requires verified financial core and sponsor/legal approval, not merely successful UI testing.
