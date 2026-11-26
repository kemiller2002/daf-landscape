# Recurring and Future Contributions: Requirements and Challenged Decisions v0.1
Date: 2026-11-22
Status: PROPOSED; legal, payment-provider, tax, and sponsor-policy review required

## Goal
Make a $10-per-pay-period contribution as easy to establish and maintain as a large scheduled contribution, without obscuring fees or making unsupported tax or settlement promises. Share deterministic scheduling infrastructure with outgoing grants, but keep distinct inbound contribution authorization, acceptance, funding, tax acknowledgment and reconciliation.

## Proposed requirements
CON-REC-01 Future-dated one-time and recurring contribution instructions.
CON-REC-02 Weekly, every-two-weeks, semimonthly, monthly, quarterly, annually, custom calendars; explicit timezone, holidays, payroll calendar and cutoff semantics.
CON-REC-03 Payday-aligned schedule with user-confirmed anchor dates; employer payroll integration optional and not inferred from bank deposits without authorization.
CON-REC-04 Sponsor-approved funding rails including ACH; payroll deduction only through validated employer/provider arrangements.
CON-REC-05 Explicit, retained recurring debit mandate with amount, frequency, first date, payer, cancellation instructions, and material-change reauthorization under applicable rules.
CON-REC-06 Contribution minimums, caps, per-period and annual projections; prevent small-dollar fees consuming intended gifts.
CON-REC-07 Idempotent debit attempts, retry caps, payment return reason handling, no blind retry of unknown outcomes.
CON-REC-08 Pause, resume, edit and cancel with clear effective date and cutoff; separately handle in-flight payments.
CON-REC-09 Distinguish initiated, pending, received, accepted, cleared, invested, reversed and acknowledged; tax receipts only for sponsor-accepted gifts with validated tax treatment.
CON-REC-10 Configurable fee policies and fee payer, full advance disclosure, net/gross contribution distinction, cost-aware funding alternatives.
CON-REC-11 Accessible embedded contribution widgets and authenticated APIs, scoped authority, consent and anti-abuse controls.
CON-REC-12 Optional employer payroll integrations, reconciliation of remittances and individual allocations.
CON-REC-13 Bank verification, risk signals, return monitoring, PII minimization and tokenized funding credentials.
CON-REC-14 Immutable activity and accounting events, reconciled to bank/custody and fund ledger.
CON-REC-15 Donor notifications, upcoming debit preview, payment-failure recovery and annual summaries.
CON-REC-16 Support contributions by permitted third parties subject to sponsor acceptance, donor identity and acknowledgment rules.
CON-REC-17 Sponsor-configurable policy for small recurring gifts and minimum account thresholds.
CON-REC-18 Financial forecasting of planned contributions with no assumption that scheduled funds are cash available to grant.

## Decision challenges and reasoning
D1 Share schedule engine, not financial lifecycle. Why: recurring timing semantics overlap but incoming funds are not outgoing grants. Challenge: duplicate complexity. Resolution: common calendar and occurrence primitives; separate contribution state machine.
D2 Support true pay-period recurrence. Why: biweekly is 26/year, semimonthly is 24/year; actual payroll can shift for holidays. Challenge: donor payroll changes. Resolution: calendar preview, edit capability, optional employer-sourced schedule after consent; do not promise actual payday synchronization without integration.
D3 Default to low-cost bank debit where available, not universal payment rail. Why: $10 gifts are sensitive to transaction costs. Challenge: ACH can return or be unauthorized. Resolution: mandate controls, bank verification, bounded retries, reserves/settlement delay.
D4 Do not treat scheduled debit as a charitable contribution. Why: initiation, settlement, acceptance and acknowledgment differ. Challenge: users expect instant receipts. Resolution: show provisional state and issue tax acknowledgment only on validated event.
D5 Avoid automatic investment/grant funding based on pending money. Why: return and timing risk. Challenge: delays donor experience. Resolution: projections plus available settled/accepted balance semantics.
D6 Sponsor fee engine must be fair for micro-contributions. Why: flat processing charges may consume disproportionate share of $10. Challenge: cost recovery. Resolution: sponsor-subsidized/batched lower-cost rails where permissible, clearly disclosed gross/net.
D7 No uncontrolled retry loop. Why: repeated debits can harm donors and violate payment rules. Challenge: failed recurring plans. Resolution: controlled retry policy, clear alerts, manual intervention only for genuine exceptions.
D8 Permit third-party contributions only after acceptance controls. Why: not all gifts or sources can be accepted; tax receipt identity matters. Challenge: friction. Resolution: risk-tiered evidence and reusable donor profiles.
D9 AI can suggest better schedules and identify failures, not initiate new debits or change authorization without mandate. Why: consent and financial integrity. Challenge: reduces autonomy. Resolution: automated deterministic execution after valid authorization.
D10 Annual forecasts are estimates, not tax advice or guaranteed deductible amounts. Why: first year, missed payments, fees and acceptance alter totals. Challenge: perceived complexity. Resolution: plain-language display of scheduled versus completed totals.

## Minimum tests
- $10 every other Friday creates 26 expected occurrences in a full 52-week cycle, with calendar-edge nuance.
- $10 on 1st/15th produces 24 occurrences, not 26.
- Employer payday holiday shift follows explicit configured calendar rather than guessed dates.
- Donor revokes mandate before cutoff; future debits stop; in-flight handling shown.
- Duplicate webhook and processor timeout do not create duplicate charges.
- ACH return after provisional credit reverses applicable ledger entries and acknowledgment handling.
- Flat fee exceeds acceptable share of $10: warn or block per sponsor policy, no hidden deduction.
- Fund cannot grant against uncleared pending contribution unless sponsor has separately approved risk-backed availability.
- Annual tax summary excludes unaccepted or reversed gifts.
- Third-party payer and beneficiary DAF remain separately identified.

## Validation required
Sponsor counsel, payments compliance and provider must validate recurring ACH authorization, revocation, NACHA/Reg E applicability, and payroll mechanisms; CFO/external CPA validate accounting and tax acknowledgment events; sponsor board approves fee policy and minimums. These are design proposals, not claims of compliance.

## Crosslinks
Grant scheduling/fulfillment decision record; enterprise-wide fee engine; financial core control spec; donor UI D08/D09 and embedded widgets; charity assurance and grants. Add to authoritative typed requirements registry after consistency review.
