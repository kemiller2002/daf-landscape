# Integrated Giving Plans: Automated Contributions and Grants
Date: 2026-11-22
Status: PROPOSED design requirements and challenged decisions; not implemented

## Outcome
Enable donor instruction such as: "Contribute $10 every payday and recommend $100 to Charity X every quarter." Coordinate incoming contributions and outgoing grants without confusing pending funds, sponsor authority, charity eligibility, or settlement.

## Domain model
GivingPlan is a versioned donor strategy and UI aggregate, not an irrevocable commitment. It references one or more ContributionSchedules and GrantSchedules, each with immutable ScheduleOccurrences and separately governed ContributionAttempts or GrantRecommendations. FundingProjection is derived, not ledger cash. FundAvailability is server-authoritative. GrantApproval, PaymentFulfillment and AccountingRecognition remain distinct. Link all with plan ID, schedule ID, occurrence ID and provenance. Use stable idempotency keys and event-time plus recorded-time.

## Requirements
GP-01 Create, preview, activate, pause, modify, resume and terminate an integrated plan through donor, advisor, administrator and scoped embedded widget interfaces.
GP-02 Permit one-to-many recurring contribution schedules, fixed and custom pay-period calendars, employer-supplied schedules only when integrated and consented.
GP-03 Permit one-to-many recurring and future grant schedules, recipient allocations, purpose and sponsor policy conditions.
GP-04 Support independent plan, contribution and grant schedule versions, limits, effective dates and audit trails.
GP-05 Forecast next 12 months with gross contributions, expected fees, accepted/cleared balance assumptions, planned grants, liquidity and minimum-balance policy; explicitly label forecasts uncertain.
GP-06 On each grant occurrence, revalidate current advisor authority, charity assurance, grant purpose, restrictions, liquidity, approvals and payment destination as applicable. Reuse 180-day charity assurance with material-change monitoring, never equate 180-day age with guaranteed eligibility.
GP-07 Default insufficient available funds to Hold and Notify, not automatic debit, partial grant, borrowing or liquidation; sponsor-approved alternatives may be offered for donor authorization.
GP-08 Support explicit donor-authorized fallback rules (skip occurrence, hold for N days, defer to next cycle), with capped retries, expiry and no duplicate grants.
GP-09 Keep incoming contribution mandate, bank verification, initiation, receipt, sponsor acceptance, clearing, reversal and acknowledgment distinct from grant recommendation, approval, payable recognition, issuance and settlement.
GP-10 Show fee quotes and recurring fee ceilings for paper checks, mailing, manual processing and contributions; avoid fees silently reducing charity grant amount or micro-gift principal.
GP-11 Expose a single plain-language calendar and dashboard: next contribution, next recommended grant, available-to-recommend, held items, estimated fees, next action and schedule health.
GP-12 Offer accessibility-first mobile UX, WCAG 2.2 AA, nonblank WASM startup, clear confirmation, no duplicate submission, and sponsor white-label widgets without weaker controls.
GP-13 Automated reminders and risk alerts with digest preferences; mandatory adverse/consent notices remain deliverable and auditable.
GP-14 Sponsor-scoped deterministic policy engine for straight-through processing; humans handle unresolved exceptions and discretionary sponsor decisions only.
GP-15 AI may propose optimizations, forecast gaps and summarize exceptions with provenance but cannot change debit mandates, recipient, grant amount, bank destination or fee authority without valid authorization.
GP-16 Cross-sponsor segregation, consent and role-bound access; succession, death/incapacity, fund closure and revoked authority suspend affected instructions pending policy.
GP-17 Reconciliation and immutable correction of all contribution, fee, grant and payment events, with CFO/CPA-validated ASC 958 recognition policies; scheduling or donor approval is not a universal accounting trigger.
GP-18 Metrics: manual touches per 1,000 plan occurrences, straight-through rate, payment losses, incorrect clearances, false holds, cost per event, donor abandonment, funding forecast error, and exceptions.
GP-19 Donor may allocate incoming contributions among authorized funds only under sponsor rules; do not silently transfer assets between funds.
GP-20 Support planned contributions from authorized third parties while preserving payer identity, sponsor acceptance, tax acknowledgment recipient and fund credit semantics.

## Decision record: recommendation, strongest objection, mitigation
D01 Unified donor plan, separate financial state machines. Reason: seamless experience without collapsing distinct legal lifecycles. Objection: complex domain graph. Mitigation: shared schedule primitives and simple UI; verify against one-off workflows.
D02 Grant occurrences do not depend on same-day contributions clearing. Reason: ACH return/settlement risk. Objection: donor expects immediate pass-through. Mitigation: show expected available date and hold/retry options, never spend projected money.
D03 Default hold on insufficient funds. Reason: avoids unapproved overdrafts, forced asset sales and donor surprise. Objection: charitable distribution delayed. Mitigation: pre-alert donor, optionally authorize deterministic fallback with strict cap.
D04 No automatic top-up debit triggered by grant shortfall unless separately and explicitly authorized with applicable mandate. Reason: prevents surprise withdrawals. Objection: higher friction. Mitigation: optional bounded auto-top-up product only after payment compliance validation.
D05 Separate plan forecast from accounting. Reason: scheduled instructions are not cash, payables or commitments by default. Objection: additional complexity. Mitigation: derived projections with transparent assumptions.
D06 Reuse charity assurance across grants, but validate critical conditions per occurrence. Reason: eliminates repeat vetting while catching adverse changes. Objection: data-source outage can stall grants. Mitigation: source-specific bounded retries and sponsor-approved risk policy.
D07 Fee ceilings and donor consent. Reason: recurring fees may change over time, especially for small gifts. Objection: fees may rise above ceiling. Mitigation: pause affected service or offer cheaper approved channel and renewed consent.
D08 Versioned changes affect future ungenerated occurrences only by default. Reason: auditability and no retroactive mutation. Objection: pending items need editing. Mitigation: explicit governed change/cancel process per financial state.
D09 AI suggestions only, deterministic authorized execution. Reason: minimizes staff touches without unauthorized financial actions. Objection: slower adaptive automation. Mitigation: versioned rules, policy experiments and independent testing.
D10 Start with fixed amounts and simple calendar rules. Reason: reliable and understandable. Objection: misses complex donor strategies. Mitigation: extensible types for percent-of-balance, escalators and budget caps after usability/risk validation.

## Example lifecycle
Plan P: $10 every two weeks starting on user-confirmed payday; $100 grant recommendation quarterly. Each contribution occurrence generates a debit attempt under its own mandate. Once accepted and cleared under sponsor policy, it updates available-to-recommend. Quarterly grant occurrence produces a recommendation; current eligibility/authority/liquidity/purpose checks run. If sufficient, sponsor-approved automatic path progresses; otherwise hold and notify. Never assume 26 deposits by every calendar year or that three months of $10 biweekly deposits always cover $100.

## Acceptance scenarios
1. Biweekly $10 contributions and quarterly $100 grants: quarterly shortfall holds, never creates an unauthorized bank debit.
2. ACH contribution returns after provisional receipt: reverse applicable postings; no double credit; reevaluate held grants.
3. Charity loses eligibility on day 30 of a 180-day cycle: future grant occurrence blocked.
4. Fee schedule changes above donor ceiling: do not charge silently; request consent or use authorized lower-cost option.
5. Donor pauses contributions but leaves grants active: forecast warns, grant policy independently evaluated.
6. Donor pauses grants but leaves contributions active: incoming debits continue only under still-valid mandate.
7. Duplicate schedule tick, webhook, timeout: no duplicate debit or payment.
8. Advisor authority revoked: affected instructions suspended without corrupting past audit history.
9. Sponsor A widget cannot access Sponsor B plan, recipient, account or fee data.
10. Donor sees next three contribution dates and next three grant dates, with processing versus settlement distinctions.
11. Cross-year contribution receipt, acceptance and grant payable recognition follow validated sponsor accounting policy.
12. Third-party payer's tax acknowledgment identity does not default to the fund advisor.

## Open validation questions
Legal/payment compliance: recurring ACH mandates, payroll linkage, tax acknowledgment, third-party contributions, revocation cutoff, sponsor approval delegation.
CFO/CPA: recognition, fee allocation, provisional cash, reversals and settlement.
Treasury: liquidity policy, reserve use and failed payment recovery.
Product: small-dollar minimums, donor comprehension, consent and default shortfall behavior.
Sponsor governance: risk thresholds and standing approval boundaries.

## Integration map
Existing donor UI D08/D09/D14 and D06/D07, operational O03/O05/O10/O11/O12, 180-day charity assurance, fee engine, grant scheduling record, recurring contributions record, financial core, embedded widget contracts. Proposed IDs GP-01..20 must be transcribed to authoritative typed registry with traceable tests after conflict review.
