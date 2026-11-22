# Grant Scheduling, Fulfillment, External IDs, and Service Fees: Decision Record v0.1
Date: 2026-11-22
Status: PROPOSED, challenged, pending sponsor legal/accounting/control validation
Scope: requirements and decision rationale, not implementation authorization
Related: docs/daf-enterprise-ui-requirements-v0.1.md; financial core control specification; sponsor delegation-of-authority registry

## Method
For each question record recommendation, reasoning, strongest objection, mitigation, alternatives, reconsideration trigger, and acceptance evidence. Do not confuse product preference with legal/accounting fact. This is a hypothesis-backed design baseline.

## Decision matrix

### DR-GR-01: Separate plan, schedule, occurrence, grant, and fulfillment?
**Recommend:** Distinct entities: GivingPlan (optional budget/strategy), GrantSchedule (versioned instruction), ScheduleOccurrence (uniquely keyed due event), GrantRecommendation (independent approval), GrantFulfillment (payment/custody/settlement). An occurrence may produce no grant if blocked.
**Why:** Independent lifecycle, clear authority, retries, cancellations, and accurate reporting.
**Challenge:** Five entities increase complexity for a simple annual gift. **Response:** donor UI presents one flow; domain separation remains internal. **Alternative:** single grant record with recurrence flags; rejected due to conflated states.
**Reconsider if:** measured complexity exceeds benefits and equivalent controls can be proven with a simpler model.
**Evidence:** lifecycle and property tests for all transition combinations.

### DR-GR-02: When does future scheduling authorize payment?
**Recommend:** Schedule is a donor recommendation instruction, not sponsor approval, irrevocable commitment, payable, or disbursement. Each occurrence must pass current sponsor policy, delegated authority, eligibility, sanctions, purpose, liquidity, restrictions, and payment checks. Sponsor may allow bounded standing approval only if legally validated, versioned, and revocable.
**Why:** Eligibility, donor authority, and balances change.
**Challenge:** Reapproval of every small recurring grant creates manual work. **Response:** automate policy revalidation and approved risk-based decision paths; do not assume blanket approval.
**Reconsider if:** legal opinion and control testing validate a broader standing-approval model.
**Evidence:** decision trace and adverse-change test.

### DR-GR-03: Frequency and dates?
**Recommend:** One-time, weekly, monthly, quarterly, semiannual, annual, custom interval and selected-date schedules; timezone and calendar explicitly stored. Default business-day policy sponsor-configurable, with preview of actual processing date and delivery estimate. Define month-end, Feb 29, DST, holiday, and cutoff behavior.
**Challenge:** Arbitrary rules are hard to explain. **Response:** start with common templates, advanced rules in secondary UI.
**Evidence:** deterministic schedule golden tests across leap years, DST, and holidays.

### DR-GR-04: Funding and liquidity?
**Recommend:** Default no hard reserve for distant recommendations. Show projected available-to-recommend and sponsor-configured optional reservations only when approved. At execution recheck actual eligible liquidity, restrictions, minimums, and investment settlement. Define insufficient-funds policy as hold + notify, not silent partial payment.
**Challenge:** No reserve creates false expectations. **Response:** clear provisional language, forecasts, alerts, and optional funded commitments.
**Reconsider if:** sponsor policy requires advance reservation for specific grant classes.
**Evidence:** concurrent grant stress tests and ledger reconciliation.

### DR-GR-05: Failed occurrences and retries?
**Recommend:** Unique schedule-version/occurrence idempotency key; at-least-once orchestration with effectively-once financial outcomes via idempotent posting, external reconciliation, and manual resolution of unknown outcomes. Never blindly retry a payment of unknown status.
**Challenge:** 'Exactly once' cannot be guaranteed across banks. **Response:** explicitly model unknown and reconciliation states.
**Evidence:** crash/replay, duplicate webhook, and timeout tests.

### DR-GR-06: Modification, cancellation, and succession?
**Recommend:** Version schedules, preserve generated instances, record who changed what and when; modifications affect future ungenerated occurrences by default. Approved/committed/issued grants require separate controlled cancellation. Suspend on account closure, loss of authority, death/incapacity or successor transition pending applicable policy review, not automatic permanent cancellation.
**Challenge:** Suspension may interrupt charitable intent. **Response:** governed successor/standing instruction policy with legal review and clear notification.
**Evidence:** authorization and transition tests.

### DR-GR-07: Amount logic and giving plans?
**Recommend:** Fixed amounts first; percentage-of-eligible-balance and capped annual budgets with explicit valuation basis/as-of, rounding, floor/ceiling, and aggregate caps. Inflation-linked escalation only after validated data-source and disclosure rules. GivingPlan is advisory unless sponsor separately approves enforceable commitments.
**Challenge:** Percentage schedules are volatile and may liquidate investments unexpectedly. **Response:** preview, safeguards, no unapproved forced sales.
**Evidence:** scenario tests with valuation changes and concurrent allocations.

### DR-GR-08: External grant IDs?
**Recommend:** Immutable internal grant ID plus zero-to-many external references with issuer namespace, reference type, provenance, visibility, and correction history. Scoped duplicate warnings rather than universal uniqueness. Do not treat a donor-supplied ID as proof of recipient identity or payment.
**Challenge:** Arbitrary free text can leak personal data or be abused. **Response:** length/character limits, permissions, data minimization, safe rendering, retention.
**Evidence:** round-trip API/import and collision tests.

### DR-GR-09: Donor hand-delivery?
**Recommend:** Sponsor-issued check payable to approved charity; donor or approved representative acts as physical presenter, never legal grantmaker or personal payee. Separate check issue, custody transfer, charity delivery confirmation, deposit/clearing, and exception states. Sponsor policy may prohibit this method for high-risk cases.
**Challenge:** Loss, fraud, delayed deposit, misleading donor tax acknowledgment, and difficulty proving receipt. **Response:** identity verification, chain-of-custody receipt, expiry/stop-payment, independent reconciliation, donor-facing acknowledgment guidance.
**Evidence:** lost-check, misdelivery, stale-check, and fraud tabletop tests.

### DR-GR-10: Paper-check and handling fees?
**Recommend:** Shared sponsor-scoped service fee engine with effective-dated schedules, fixed/actual-cost/cost-plus/tiered rules, caps, disclosure, approvals, waivers, refunds, and distinct ledger postings. Charge donor-advised fund balance only if sponsor policy, fund agreement, law, and accounting treatment permit; preserve charity's approved grant amount. Fees can vary for recurring grants, but disclose change rules and cap or obtain renewed authorization.
**Challenge:** Fees may disincentivize giving, be disproportionate, or obscure operating expenses. **Response:** compare cost recovery to experience and offer electronic alternatives; no undisclosed charges.
**Evidence:** fee schedule versioning, pricing previews, reversal tests, sponsor CFO/legal signoff.

### DR-GR-11: Fees for recurring occurrences?
**Recommend:** Calculate a fee quote for each occurrence from the applicable effective policy, show forecast and material-change notices; define consent threshold and maximum fee guardrail in schedule. Never silently reduce grant to pay fees. Distinguish estimate, assessed, earned, posted, waived, reversed, refunded.
**Challenge:** Repricing could make donor's standing instruction open-ended. **Response:** hard ceiling or pause for renewed consent.
**Evidence:** mid-schedule fee-change tests.

### DR-GR-12: Accounting recognition?
**Recommend:** Event ledger distinguishes schedule creation, occurrence, recommendation, sponsor approval, reservation, external commitment, payable recognition, payment initiation, delivery, clearing, and fee recognition. Apply CFO/external-CPA validated ASC 958 recognition policy, not a universal event trigger; immutable corrections and event-time/accounting-period attribution.
**Challenge:** More states create reporting complexity. **Response:** explicit semantics prevent misstatements.
**Evidence:** cross-period, backdated, unknown, reversed and late-arriving events reconciled.

### DR-GR-13: APIs and widgets?
**Recommend:** Server-authoritative F# APIs for schedules, preview, fees, grant occurrences, and fulfillment. Embeddable widgets may draft and recommend within sponsor-approved capability scopes; never bypass host authentication, sponsor controls, consent, or financial authorization. Signed events, scoped tokens, CSP, accessibility, idempotency, tenant isolation.
**Challenge:** Embedding expands attack surface. **Response:** least-privilege, audited cross-origin integration, no secrets in browser.
**Evidence:** threat model, penetration tests, cross-tenant denial tests.

### DR-GR-14: AI role?
**Recommend:** AI may suggest giving plans, predict liquidity, flag unusual schedules, recommend cheaper fulfillment, and explain exceptions with provenance. No autonomous grant approval, payment redirection, fee waiver, or modification of donor instructions absent explicit delegated authority and validated controls.
**Challenge:** This limits automation value. **Response:** automate deterministic low-risk checks and retain human accountability for discretionary decisions.
**Evidence:** adversarial tests, reproducible policy decisions, human override logs.

### DR-GR-15: UI?
**Recommend:** Donor mobile-first progressive disclosure: one-time vs recurring, amount, charity, date/frequency, funding, delivery, fees, review, confirmation. Calendar with upcoming/paused/blocked, next action, separate grant and schedule status, projected versus actual amounts. Admin exception queue and custody timeline. WCAG 2.2 AA, 320px reflow, 400% zoom, nonblank WASM startup, resumable drafts, safe retries.
**Challenge:** Advanced configuration overwhelms donors. **Response:** templates and advanced options on demand; user tests.
**Evidence:** usability studies including screen-reader and mobile users.

### DR-GR-16: Notifications?
**Recommend:** Event-driven opt-in channels with mandatory operational notices; upcoming execution, eligibility hold, insufficient liquidity, fee increase, check custody, failed delivery, settlement, schedule expiration. Avoid implying a check issued equals charity received or settled.
**Challenge:** Notification fatigue. **Response:** configurable digest and severity, immutable delivery evidence for mandatory notices.
**Evidence:** communication matrix and suppression tests.

### DR-GR-17: Scope and tenancy?
**Recommend:** Sponsor/legal entity controls policy, fee schedule, approval authority, payment methods, calendars, retention, and account privileges. No cross-sponsor leakage. AUM-based liquidity forecasting is optional and does not automatically imply cash availability.
**Challenge:** Excessive per-sponsor customization. **Response:** constrained policy DSL with approved templates and typed validations.
**Evidence:** multi-sponsor differential tests.

### DR-GR-18: Privacy, evidence and retention?
**Recommend:** Minimal external IDs and custody PII, redaction in logs/AI, role-based access, tamper-evident event provenance, retention schedules with legal hold. Do not store check images or mailing addresses in analytics.
**Challenge:** Auditability versus data minimization. **Response:** separated secure evidence store with access logs.
**Evidence:** privacy threat model and retention tests.

## Rejected defaults and counterfactuals
1. Automatically reserve all future grant amounts: rejected because speculative long-horizon grants would unnecessarily immobilize AUM.
2. Treat recurring schedule as perpetual sponsor approval: rejected because recipient and fund conditions change.
3. Treat handoff to donor as completed payment: rejected because custody is not receipt or settlement.
4. Deduct service fees from charity proceeds: rejected as default because donor expectations and grant approvals should remain intact.
5. Recompute past occurrences after schedule edits: rejected because it destroys historical auditability.
6. Automatically retry ambiguous bank transfers: rejected because duplicate payouts are more damaging than a review queue.
7. Let AI modify giving instructions without authority: rejected because explainability does not equal authorization.
8. Use external reference as primary key: rejected because reference namespaces collide and can change.

## Open questions requiring external validation, not arbitrary product decisions
- Sponsor counsel: recurring recommendation validity, donor authority after death/incapacity, pledge restrictions, hand-delivery and acknowledgment language.
- CFO/external CPA: ASC 958 grant and fee recognition, accruals, reversal policy, fee payer, multi-period attribution.
- Treasury/payment operations: check custody insurance, loss allocation, stale checks, bank settlement and escheatment policies.
- Compliance: jurisdiction-specific screening, recipient revalidation cadence, retention and privacy.
- Product research: donor preference for recurring giving, fee transparency comprehension, schedule preview usability.
- Sponsor board: delegated approval boundaries, exception thresholds, fee schedules, waiver authority.

## Acceptance scenarios (minimum)
A. Monthly grant with balance falling below required minimum: hold, alert, no duplicate.
B. Annual grant due Feb 29 and holiday conflict: deterministic preview and execution.
C. Schedule edit while occurrence approved: past/approved record immutable, future schedule versioned.
D. Charity loses eligibility after schedule creation: execution blocked and audited.
E. Donor loses authorization: schedule suspended, no unapproved payment.
F. Hand-delivered check lost: stop-payment, chain-of-custody evidence, governed replacement, no double payout.
G. Fee changes after recurring instruction: threshold guardrail, clear notice, pause/renew consent.
H. Same external ID from two different issuers: both preserved without false collision.
I. Payment provider timeout with unknown settlement: no blind retry; reconcile.
J. Sponsor A user attempts Sponsor B schedule/fee data: access denied.
K. Cross-year approval, commitment, clearing and fee posting: correct period attribution per validated policy.
L. AI proposes payment method change: cannot execute without appropriate authority.

## Traceability and next steps
Proposed IDs: GR-SCH-01..14; GR-EXT-01..02; GR-DEL-01..08; GR-FEE-01..07; DR-GR-01..18. Cross-link donor UI D06/D07/D14, operations O03/O10/O11/O12/O15/O17, financial core, board delegation registry, reconciliation, and widget/API requirements. All decisions remain PROPOSED until reviewed and entered into authoritative typed registry. Do not claim implementation or legal validation.
