# DAF platform portability and switching-cost migration runbook

**Designed November 11, 2026. No vendor system executed.** This is a reference acceptance plan for sponsor-owned data and legally permissible grant/account transitions. It does not authorize or promise access to any proprietary Ren, TIFIN Give or Chariot production system. The tests use **only synthetic clients, gifts, grants and DAFs**, with participant consent and explicit written vendor permissions.

## Objectives

Measure **vendor-independent exit capability** separately from a sponsor's legal right to approve transfers:

1. **Sponsor-to-sponsor DAF transfer** by donor recommendation and sponsor approval. This is a charity grant, not a donor withdrawal [R01,R02,R03].
2. **Sponsor-kept platform replacement** with the same legal sponsor and custody records; AEF's real-world Ren migration is the motivating case study [R04–R06].
3. **Disbursement/DAFpay connectivity replacement** while the DAF ledger and legal sponsor continue; original provider approval remains mandatory [R12,R15].
4. **Wealth-advisor relationship transition** with valid delegated authorities and investment mandates. Avoid claiming the advisor owns donated assets.
5. **Contract and archival exit** with all rights, user credentials, transaction details and record-retention obligations reconciled before access is revoked [R09,R13,R22].

## Universal fixture

**Synthetic institution:** 2 sponsoring charities, 3 donor households per sponsor, 2 wealth advisers, 2 custodians, 1 disbursement provider, 5 years of dated transactions. Include 3 years of older archived statements, not just 2 recent years.

**Synthetic account states:** pooled and separately managed accounts; restricted investment, donated stock with basis, pending contribution, recurring grant, approved-but-unpaid grant, mailed check uncashed, rejected recipient, returned ACH, corrected grant, donor successor change, deceased donor, account hold, multi-year gift history, donor anonymization request.

**Test environments:** two authorized staging deployments or vendor-provided migration simulators with no live funds; use non-production payment/bank records. Where vendor sandbox unavailable, record `not_executed` instead of inferring a failure.

## Acceptance cases

| Test | Boundary | Execution | Required pass evidence |
|---|---|---|---|
| M01 | Full account export | Export all five synthetic years of contributions, grants, statements, tax receipts, investment and fee records | Counts, dates, identities and amounts reconcile exactly; independent hash/ID manifest |
| M02 | Older history in new UI | Confirm years 1–3 available, even if via sponsor archival portal | Documented retrieval procedure and SLA; no claim of automatic self-service without proof |
| M03 | Sponsor stays, platform changes | Rebuild portal identities and sponsor accounts, no re-donation of sponsor-owned assets | Same sponsor legal IDs, same authorized account balances, full ledger continuity |
| M04 | Sponsor-to-sponsor move | Donor recommends account-closing grant; both sponsors approve and receipt maps to new DAF | Legally valid fund grant; original account closure and opening match; no donor personal withdrawal |
| M05 | DAF transfer rejected | Original sponsor refuses closing grant or incoming sponsor rejects | No unauthorized transfer; document decision and permissible alternatives |
| M06 | Partially completed gift | Migrate pending in-kind stock gift without misrepresenting tax receipt | Confirm correct custodian, ownership transfer, tax-effective date and state |
| M07 | Adviser reassignment | Revoke old advisor; grant new advisor rights under sponsor policy | Old credentials fail, roles correct, no inherited unauthorized permissions |
| M08 | Successor preferences | Migrate post-death or successor rights and grant history | Sponsor-approved successor lineage and authorized access |
| M09 | Five-year ledger and NAV | Recompute holdings, fees, units, fund-level NAV and balance | Independent trial balance matches; every correcting entry traceable |
| M10 | Grant ID mapping | Process pending/rejected/reversed grants without duplicate payments | Single canonical grant per recommendation, old/new IDs cross-referenced |
| M11 | Payment cutover | Handle approved-but-unpaid grants, in-flight ACH and mailed check returns | Explicit owner/ledger for each pending item; no stranded cash or duplicated settlement |
| M12 | Nonprofit remittance | Match donor source, anonymous flag, EIN, address, external tracking ID | Charity receives accurate permitted data; reconciles payouts |
| M13 | Failure recovery | Simulate API/timeouts/custodian outages at cutover | Recover with idempotent replay and no lost event |
| M14 | DAFpay provider exit | Terminate integration under authorized terms; revoke tokens; complete pending requests | Provider grant decisions preserved; token revocation; documented data retention |
| M15 | Chariot nonprofit exit | Export historical remittance and withdraw permitted balances **before** loss of account access | Accurate reconciliation/export complete and new bank/payout permissions validated |
| M16 | TIFIN enterprise subscription exit | Review governing signed customer agreement; demonstrate data export before termination | Valid ownership, exit rights, transition assistance and retained history confirmed |
| M17 | GDPR/state privacy requests | Reconcile permitted deletion/revocation with records legally required to be retained | Retention exceptions documented; access scopes enforce constraints |
| M18 | Tax-receipt and donation history | Present same gift once even through duplicate platform history | No duplicate acknowledgement/deduction or missing signed receipt |
| M19 | Billing exit | Reconcile contract charges and dual-run/termination fees | Final invoice, refunds/credits where contractual, no surprise recurring access |
| M20 | Metrics and audit | Independently verify 100% of open exceptions and total amounts after cutover | Signed cutover record, donor/sponsor approval, evidence index and unresolved risks |

**No test has been run against a vendor; the acceptance criteria do not constitute current feature claims.**

## Data portability schema

Require a versioned export with at minimum:
- `sponsor_legal_id`, `account_id`, `fund_id`, `donor_advisor_role`, `adviser_id`, `permission_effective_from/to`.
- `contribution_id`, `asset_id`, `custodian_transaction_id`, `accepted_at`, `tax_receipt_ref`, `restriction_code`.
- `fund_ledger_entry_id`, `security_lot_id`, `basis_metadata_if_permitted`, `valuation_timestamp`, `NAV`, `fee_component`.
- `grant_recommendation_id`, `sponsor_decision_ref`, `EIN`, `privacy_flag`, `payment_initiated_at`, `settled_at`, `charity_acknowledgment`.
- `legacy_source_system_id`, `migration_batch_id`, `old_id_to_new_id`, `correction_chain`, `provenance`, `archival_location`.
- `consent_record`, `document_hash`, `retention_class`, `status`, `effective_date`.

This is a **proposed interchange schema**, not a native Ren, TIFIN or Chariot API specification. The source of truth for legal ownership and charitable granting remains the authorized sponsoring organization.

## Switching-cost measurement

Record, for each scenario:

| Metric | Unit | Must specify |
|---|---|---|
| Planned and actual implementation | calendar days | Critical path and committed milestones |
| Vendor/customer implementation | hours or contracted dollars | Role, rate, source and invoice |
| Parallel system run | days and dollars | Duplicated licenses, custody, staffing |
| Data export | files, records, exception count | Data scope, schema, missing history |
| Reconciliation discrepancies | count and dollars | Age of backlog, severity |
| Sponsor and advisor downtime | minutes | Real user effect and recovery |
| Nonprofit delayed grants | grant count, dollars, days | Approval vs initiation vs receipt |
| Donor support intervention | cases and minutes | Previously accessible versus manual history |
| Legal/contract exit costs | dollars | Actual executed contract only |
| Recreated donor/account permissions | records | Revocations, successors, role mapping |
| Customer attrition *after migration* | verified accounts/institutions | Separate voluntary moves from grant drawdowns |

**Do not fabricate dollar estimates** for Ren, TIFIN, AEF or Chariot. Use a neutral, real-life simulation where authorized. The only directly verified specific migration discontinuity in public sources here is AEF's prior-two-years donor-history limit [R06].

## Commercial and legal evidence checklist

Before signing any platform contract, verify:
- Nonexclusive access, exit rights, and termination for convenience with fixed notice.
- What happens to donor data, sponsor-owned accounting, historical statements, identities, tax acknowledgments and derived/aggregated data after exit.
- Data export **before and after** termination, including format, frequency and cost.
- Renewal terms, fee resets, price indexation, SaaS versus sponsor-service fees and transition assistance.
- Key third-party providers, authorized DAF sponsors, custodians, nonprofit disbursement partners, and banking.
- How late grants, check reissues and returns can be reconciled by the new provider.
- Necessary rights to publish benchmark results from *authorized tests*; TIFIN and Chariot generic service terms restrict some competitive evaluations [R09,R13].

## Retention economics linkage

If a sponsor migrates software but retains its donor funds and advisors, this is **platform-provider churn**, not necessarily sponsor or wealth-firm churn. If a donor recommends grants from a DAF over multiple years, falling balance is **philanthropic payout**, not automatically churn. If asset markets fall, billable AUM revenue can contract while the software customer is still present. The research dataset must record each transition as a different causal event.

## Status and dependencies

- **Public proof:** IRS ownership, public transfer-in instructions from Fidelity/RCF, AEF actual platform migration, TIFIN and Chariot generic contract mechanisms [R01–R15].
- **Unknown:** customer-specific legal service agreements, completed current vendor exports, exit fees, actual 2026 contracted platform ARR, customer churn and net retention.
- **Ready for execution:** synthetic fixtures and proposed acceptance tests defined.
- **Not executed:** all M01–M20 against vendors.
