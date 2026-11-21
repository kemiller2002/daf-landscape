# F. Finance, accounting and treasury

**Capabilities:**
- C4.1 Event ledger and fund accounting
- C4.2 Reconciliation
- C4.3 Fees and billing
- C4.4 Reporting and filings
- C2.5 Liquidity and treasury

**Outcomes:** O-05, O-12, O-14, O-07.

**Accountable:**
- CFO
- Controller, responsible for daily operation
- Audit Committee, responsible for oversight

## 1 Existing industry operating model

**Ledgers and recordkeeping.** Ledgers sit behind portals and are often outsourced:
- Give Interactive is Vanguard Charitable's ledger vendor ([industry report §11.2](../../../DAF-INDUSTRY-REPORT-2026-11.md)).
- Ren supplies administration and platform to RCF, which paid Ren $19.23m in FY2024, equal to 98% of its individual-fundholder admin-fee revenue (§2.2).
- Community foundations commonly run Foundant or Blackbaud. Santa Barbara's GL is on Blackbaud FE NXT (industry report §11.11).
- Repository work on ledgers: [`queue-ledgers-behind-portals.md`](../../../mission-2026-11-14/queue-ledgers-behind-portals.md), [`queue-batch38-vendors-ledgers-portals.md`](../../../mission-2026-11-14/queue-batch38-vendors-ledgers-portals.md).

**Filing and reconciliation.** Form 990 Schedule D Part I aggregates are the only regulator-facing DAF data. The repository's recomputation found 2,564 itemized adjustments between DAFRC's imputed rows and the filed values ([industry report §1](../../../DAF-INDUSTRY-REPORT-2026-11.md)). That shows how far filed and reported figures can diverge.

**Grant voids and refunds.** At least 17% of the top 200 sponsors itemize grant voids, refunds or recoveries, median about 0.3% of grants (industry report §11.9). That reflects accounting presentation, not void incidence.

**Fee mechanics.**
- Sponsors charge tiered bps: Fidelity, DAFgiving360 and Charityvest start at 0.60% on the first $500k; RCF 0.65% with a $250 minimum; BofA 0.90% flat.
- Affiliated sponsors pass fees to the parent: Fidelity Charitable pays FMR affiliates amounts equal to donors' administrative fees ([industry report §2.1, §3](../../../DAF-INDUSTRY-REPORT-2026-11.md)).

**Operating cost** ([`b51-04-sponsor-operating-efficiency.md`](../../../mission-2026-11-14/b51-04-sponsor-operating-efficiency.md) §0):

| Group | Median operating cost |
|---|---|
| Top-50 nationals | 23 bps of DAF assets; $1,395 per account |
| Top-50 community foundations (rule A) | 102 bps; $12,036 per account |

Scale economies exist for own-staff sponsors (elasticity 0.64 at CFs, 0.49 at nationals).

**No sponsor publishes close duration, reconciliation break rates or audit adjustments** (absence finding; GAP).

## 2 Actual required business outcomes

1. Fund-level balances are correct every business day (O-05).
2. Books agree with custodians, banks and rails, with every difference explained and aged (O-05).
3. Fees are computed exactly per the published schedule, including adviser caps and partner shares (O-05, O-14).
4. Financial statements, Form 990 and Schedule D, state filings and donor statements are produced correctly and on time (O-12).
5. Cash is positioned to pay grants and operating costs (O-04).
6. Segregation of duties and independent verification are preserved (O-08, O-10).

## 3 Legal and risk constraints

**Legal:**
- GAAP for not-for-profits (ASC 958).
- Form 990 including Schedule D Part I (§6033(k)).
- State audit thresholds and filings.
- Record retention.
- Unclaimed property for uncashed checks.

Confirm each in the [regulatory map](../../08-governance-and-compliance/regulatory-applicability-map.md).

**Risk:**
- Unit-price errors.
- Fee mis-accrual.
- Diversion through payment-creation and approval collusion.
- Breaks left unaged.
- Migration history loss.

## 4 Proposed AI-native operating model

**Event-sourced, continuously reconciled accounting (DD-006).** Month-end becomes a verification checkpoint rather than a project.

1. **The journal is derived from business events.** Each event (`ContributionSettled`, `GrantApproved`, `PaymentSettled`, `FeeAccrued`, `NavStruck`, `PaymentReturned`) maps through versioned posting rules to balanced entries. The journal is append-only: corrections are reversing entries with a reason and an approver.
2. **The sub-ledger and GL are one model.** Fund-level unit balances and the GL are projections of the same events. The invariant Σ(account units × NAV) = pool NAV is checked at every NAV strike.
3. **Continuous three-way reconciliation:**

| Pair | What is matched |
|---|---|
| Ledger ↔ custodian | Positions and transactions |
| Ledger ↔ bank | Cash |
| Ledger ↔ rail | Payment settlement by idempotency key |

   Matches are deterministic on keys. Residual breaks go to the reconciliation break triage agent (P classification and proposed resolution). Known patterns, such as timing differences inside the settlement window, close automatically by rule. Anything else is a case. Write-offs above a threshold need a second approver.
4. **Fees:** the fee engine computes daily accruals from schedule versions (sponsor, advisor, partner share) and enforces caps.
5. **Financial close:**
   - **Daily:** all reconciliations green, or breaks aged within SLO.
   - **Monthly checkpoint:** the controller reviews the exceptions report, accruals and judgments, then signs.
   - **Year-end:** auditor procedures run against the evidence ledger with read-only access (ACT-041 eliminated).
6. **Reporting:**
   - The Form 990 Schedule D Part I aggregates are computed from the ledger.
   - A cross-report consistency test enforces Schedule D = ledger aggregates.
   - Donor statements are generated on demand.
7. **Treasury:**
   - Rules-based sweeps between operating, grant-disbursement and investment cash within limits.
   - Liquidity forecast from area E.
   - Bank-account changes under dual control.
8. **Segregation of duties is enforced in the authorization model:**
   - Payee creator ≠ payment approver.
   - Posting-rule author ≠ deployer.
   - Reconciler ≠ write-off approver.
   - No person can both change a fee schedule and approve the fee revenue report.
9. **Independent verification:**
   - Internal audit reads the evidence ledger independently.
   - The external auditor reperforms reconciliations from the raw feeds, not from the enterprise's projections.

## 5 Eliminated activities

| Disposition | Activities |
|---|---|
| Transformed | ACT-037 batch unitization; ACT-038 manual reconciliation; ACT-039 multi-day close |
| Automated | ACT-040 spreadsheet fees; ACT-044 990 preparation (officer signs); ACT-068 manual sweeps; ACT-077 manual grant-payment reconciliation |
| Eliminated | ACT-041 audit sample pulling |
| Transformed, dual control retained for exceptions | ACT-069 dual human approval of every routine grant payment |

## 6 New workflows

- **WF-F1 Daily cycle:**
  1. Feeds ingested.
  2. `PositionChanged` and cash events.
  3. Matches.
  4. `ReconciliationBreakDetected` for residuals.
  5. `NavStruck` (tolerance checks).
  6. `FeeAccrued`.
  7. Invariant checks.
  8. Daily close status published to the COO, CFO and board dashboard.
- **WF-F2 Break resolution.** Agent classification, then auto-close by rule or a case, then resolution (adjusting entry if needed, approved by H above threshold) and `ReconciliationBreakResolved`.
- **WF-F3 Month checkpoint.** The controller reviews the exception summary, unusual entries, judgments and accruals; signs; and the period is locked (any later entry must be a prior-period adjustment).
- **WF-F4 Annual filings:**
  1. Ledger aggregates.
  2. 990 draft.
  3. Consistency tests.
  4. CFO review.
  5. Officer signature (H).
  6. Filing receipt recorded as evidence.
- **WF-F5 Uncashed check.** `CheckAged`, then reissue electronically if possible, otherwise the escheat schedule per state, with a filing signed by an officer.

## 7 Required data

- Events.
- Posting rules (versioned).
- Chart of accounts.
- Custodian, bank and rail feeds with provenance.
- Prices.
- Fee schedules.
- Adviser and partner fee terms.
- Escheat rules per state.
- Filing calendar.

## 8 Required APIs

`/v1/ledger`, `/v1/reconciliation`, `/v1/fees`, `/v1/reports`, `/v1/evidence`, `/v1/events`, `/v1/cases`, `/v1/payments`, `/v1/positions`.

The auditor role gets read-only `/v1/evidence` and `/v1/ledger`.

## 9 Event triggers

**Consumed:** all financial events.
**Produced:** `NavStruck`, `FeeAccrued`, `ReconciliationBreakDetected` / `Resolved`, `CheckAged`, `RegulatoryDeadlineApproaching`, `DocumentationDelivered`.

## 10 AI agent responsibilities

| Agent | Category | Responsibility | Prohibited |
|---|---|---|---|
| Reconciliation break triage | 2 | Classify breaks and propose a resolution with evidence | Posting adjustments; write-offs |
| Document extraction agent | 2 | Extract data from custodian statements and bank letters where no structured feed exists | Changing balances |
| Improvement agent | 2 | Detect recurring break patterns and propose posting-rule or feed fixes | Deploying rule changes |

## 11 Deterministic automation responsibilities

- Posting.
- Unitization and NAV.
- Fee accrual and caps.
- Key-based matching.
- Timing-difference auto-close rules.
- Invariant checks.
- Report generation.
- Consistency tests.
- Sweeps.
- Escheat timing.

## 12 Human oversight requirements

- Accounting policies (CFO, Audit Committee).
- Write-offs and adjustments above threshold (controller plus second approver).
- Monthly sign-off.
- Financial statement judgments.
- Filing signatures.
- Bank account changes (dual control).
- External audit appointment (Audit Committee).

## 13 Exception management

| Item | Rule |
|---|---|
| Break aging SLOs [A] | Timing breaks auto-close within T+2. Others need a case by T+1 and resolution by T+5 |
| Unexplained position change with no instruction | Critical: treated as a security incident and a reconciliation case |
| NAV tolerance breach | Hold the NAV and open a controller case |

## 14 Security and compliance controls

- Append-only journal.
- Reversing-entry-only corrections.
- SoD enforced in authorization.
- Dual control on treasury and bank changes.
- Evidence ledger hashing.
- Auditor reperformance from raw feeds.
- Period locks.
- Production access to the ledger store is just-in-time and logged.

## 15 Estimated staffing implications

**Drivers:**
- the residual break rate × minutes per break;
- the number of custodian, bank and rail counterparties (feed maintenance);
- the number of filings and states;
- the complexity of fee and partner arrangements.

**Direction:**
- Reconciliation clerks and close teams shrink sharply.
- The controller, a fund accountant and the CFO remain.
- SoD requires at least two finance people even at the smallest scale (see the [organization model](../organization-model.md) §4).

Numeric FTE is in [`../../09-financial-models/`](../../09-financial-models/).

## 16 Cost and performance model

**Cost drivers:**
- External audit fee [A; no repository benchmark].
- Bank and custodian fees.
- Feed integration maintenance.
- Fund accountant time per break.

**Design targets [A]:**
- Daily auto-match rate above 99% of transactions.
- Month checkpoint within 2 business days.
- Zero audit adjustments from reconciliation.
- Schedule D equals ledger aggregates exactly.

## 17 Implementation dependencies

- Custodian and bank feeds.
- Chart of accounts.
- Posting-rule library.
- Fee schedules approved by the board.
- Audit firm willing to rely on the evidence ledger.
- Period-lock and authorization model (area K).

## 18 Measurable success criteria

1. Auto-match rate.
2. Break aging distribution.
3. Days to month checkpoint.
4. Audit adjustments and management-letter findings.
5. Fee errors found after the fact (target: zero).
6. Filings on time: 100%.
7. Invariant violations: zero, and any violation is an incident.
