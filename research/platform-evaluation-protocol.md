# Vendor-neutral DAF platform evaluation protocol
**Designed 2026-11-11 | No live demos or tests conducted yet**

## Objective and scope

Compare Ren and TIFIN Give on the **same legal/operating use case**, with Chariot **Disbursements** or another payment module evaluated separately. A fair comparison must state which sponsor, platform product, accounting engine, custodians, payment provider, legal entity, and third parties are actually included. **Marketing documentation does not count as an execution test**.

Results must distinguish:
- **Observed in test**: reproducible output with timestamp, environment, fixture and evidence.
- **Documented by public vendor**: a claim/feature described in an accessible source.
- **Asserted by seller in private demo**: unverified until tested; store only if authorized.
- **Unknown**: no evidence either way.
- **Not applicable**: buyer scenario does not require it.

Do not store confidential pricing, restricted audit reports, NDA material, client interview transcripts, or private employer information in this public research project. Private diligence can refer to restricted evidence IDs held elsewhere.

## Scenario definitions

**Scenario S1: independent sponsoring charity with complex back office**
- 1 sponsoring charity; 10 programs; 300 pooled funds + 100 separately managed accounts; 3 custodians; donor, sponsor approver, advisor and auditor roles.
- Need secure donor access, core general ledger and daily unitization, corporate action support, revenue/expense allocation, approved disbursements, statements and exact audit reconciliation.
- Event fixtures are *synthetic workloads* for testing, not observed vendor volumes.

**Scenario S2: advisor-led wealth firm with outsourced sponsor**
- 1 wealth firm + legal sponsor; 30 advisors; 60 donors, 2 branded variants; support broker-dealer custody and an advisor-managed account; donor contribution, family successor, grantee approval and grant settlement.
- Need integration with planning/CRM, permissible investment options, cross-advisor role segregation, digital onboarding, consistent branding and reporting.

**Scenario S3: payment-only modernization**
- Existing sponsor/platform and ledger continue. 200 approved grants: 100 nonprofits with claimed electronic accounts, 70 without Chariot accounts, 20 ineligible/ambiguous, 10 with simulated operational errors. Include high/low dollar amounts and duplicate retries.
- Compare Ren Rapid Disbursement Engine where offered as a discrete service versus Chariot Disbursements. Both have sponsor authority external to payment layer.

Scenario sizes are *illustrative*, not representative of industry distributions, benchmarks or vendor production capacity.

## Runbook: required control exercises

| Test ID | Exercise | Pass condition | What evidence to save |
|---|---|---|---|
| T01 | Donor starts application, completes contribution, selects eligible investments | Clear identity and legal sponsor acceptance; rights recorded | Redacted event trail and authority screen |
| T02 | Separate grant recommender and sponsor approver roles | Donor/advisor cannot self-approve sponsor decision | Role policy, event history and rejected unauthorized request |
| T03 | Submit identical grant 3x through retry | Exactly one accepted recommendation/payment | Idempotency keys, API logs, ledger references |
| T04 | Charity passes initial vetting then becomes ineligible before approval | Sponsor hold/review blocks payout and records reason | Rule version, timestamps, override permissions |
| T05 | Corporate action/SMA trade/custody correction | Position, NAV, subledger and GL converge; discrepancies isolated | Input files, correction journal, reconciliation |
| T06 | One month-end close with postdated adjustment | Trial balance and donor statement reconcile; correction trace preserved | GL statements and change control logs |
| T07 | Multiple custodians and advisor-managed versus pooled funds | Funds match right custodian, investment policy, allocation and fee basis | Positions and allocations comparison |
| T08 | Approved grant to verified nonprofit | Track sponsor approval, funds reserved, delivery, recipient availability and completed reconciliation | Chain of custody and five timestamps |
| T09 | Grant to unclaimed nonprofit | Document fallback (check) cost, delivery time, exceptions and recipient identity | Mailing/return metadata and communications |
| T10 | Returned/voided/stale check and ACH return | Idempotent correction, reversed entries, staff queue, donor/nonprofit notification | Return codes, ledger reversal, resolution timing |
| T11 | Payment processor or sponsor portal outage | Safe recovery, consistent event state, no loss or duplicate | Retry records, reconciled ledgers and recovery evidence |
| T12 | Revoke adviser; repeat donor session/API token | Access denied immediately or per documented policy | Token expiry, authorization decision, access logs |
| T13 | Export all funds and historical transactions; re-import to neutral format | Complete reconcilable export, portable IDs and ownership map | Data dictionary, export/replay reconciliation |
| T14 | AI recommends grant/recipient or creates pending recommendation | Explicit authorization, accurate rationale, safe refusal and sponsor approval retained | Tool permissions, LLM logs policy and approval event |
| T15 | Confirm SOC 2/SOC 1 in-scope systems and CUECs | Current reports match named product/entity and responsible controls | Restricted-report metadata only in public repository |

A demo that shows only a front-end confirmation is a **failure to provide evidence**, not automatic evidence that the feature is broken.

## Metrics: all vendors must use same event definitions

**Funnel:** accepted sponsor account → completed contribution → fund available for granting → grant recommendation submitted → sponsor approved → payment initiated → accepted by processor → recipient account funds available → recipient external account funds cleared → nonprofit acknowledges → sponsor GL reconciled.

Collect:
- Median, p90, p99 elapsed time and error/return rate for *each transition*, not one generic “speed.”
- Percentage of grants needing manual review or additional donor/nonprofit data.
- Total staff minutes per settled grant, including retries, exceptions, support and reporting.
- Total dollar and count amount of unmatched reconciling items at close (zero tolerance should be explicitly stated where required).
- Audit exceptions, privileged account count, availability during failure injection, disaster recovery test results.
- Tax/compliance accuracy on a labelled fixture set reviewed by a qualified professional; do not use generative suggestions as an unreviewed legal/tax answer.
- Implementation duration and one-time effort, ongoing licensing/asset and per-grant fees, migration/exit, custody and payment costs.
- Recipient experience: claimed-account rate, paper-check fallback, donor name remittance completeness, CRM match rate, and real external bank availability.

Keep five distinct clocks: **recommendation**, **approval**, **initiation**, **recipient deposit availability**, **external-bank settlement**. An “instant” claim must identify which clock stopped.

## Decision criteria by buyer (proposed weights, not vendor scores)

| Dimension | S1 sponsor | S2 wealth firm | S3 payments |
|---|---:|---:|---:|
| Operational/financial correctness | 25% | 15% | 10% |
| Legal responsibility / approvals / compliance | 20% | 15% | 20% |
| Accounting, investment and custody integrations | 20% | 20% | 5% |
| Donor/advisor/nonprofit experience | 10% | 20% | 10% |
| Payment settlement and exception handling | 10% | 10% | 30% |
| Security/independent assurance | 10% | 10% | 15% |
| Total cost, migration and exit flexibility | 5% | 10% | 10% |
| **Total** | **100%** | **100%** | **100%** |

These are **illustrative weights**, chosen to demonstrate how buyer priorities change decisions. Do not publish a vendor score until a stakeholder has ratified weights and observable evidence exists for every critical criterion.

**Hard gates** (cannot be traded away for feature points): sponsor legal control of grants, separable authorizations, accurate accounting and position data, irreversibility/reversal controls, data privacy, auditable settlement and critical third-party security evidence.

## Interview/RFP questions

1. Name legal sponsor(s), admin vendor(s), asset custodian(s), payments provider and processor/bank; which entity owns account at each phase?
2. Can you provide a product/module map and sample system-of-record diagram that reflects this exact deployment, not a generalized architecture slide?
3. Which services are optional add-ons versus standard? Which product line provides daily unitization, general ledger, complex gifts, accounting and custom reporting?
4. What is the **minimal** implementation to launch a sponsored branded DAF with advisor-managed custody? What migration history is portable?
5. How are sponsor approval and disbursement authorization represented, audited, delegated and reversed?
6. How do multiple custodian feeds, stale NAVs, corporate actions, closed accounts, fee changes and postdated corrections affect donor and sponsor reports?
7. How do payment rails work for claimed vs unclaimed nonprofits? Who owns bank accounts and bears settlement, check, fraud, return and loss responsibilities?
8. What API docs, version policies, webhooks, event IDs, retries, idempotency and sandbox fixtures are available? Do these vary by service plan?
9. Which AI actions can affect real assets or grant recommendations? How are identity, consent, sponsor gate, hallucination and prompt injection handled?
10. Provide in-scope SOC 2, SOC 1 where applicable, bridge letter, subservice carve-outs and sponsor complementary controls. Who handles incidents?
11. What are your **actual** median/p90 times for approval, release and recipient availability, broken down by exception/rail? State denominator and period.
12. Show the full 3-year total cost of ownership under identical asset, account, contribution, grant and support volumes, including payment fees and migration/termination.
13. What does an exit look like: contractual data rights, timelines, file formats, audit evidence portability, donor authorization and switched sponsors?
14. Provide 2 references in the same sponsor/custody/client segment, with permission to discuss reversals, accounting, cash settlement and implementation support.

## Evidence gate before publishing a winner

- Both implementations tested against comparable legal structure and fixture suite.
- Critical security/financial reporting report coverage verified under appropriate controls.
- Accounting and payment exceptions reproduced and closed, not waived.
- Pricing and business metrics drawn from compatible time periods and denominators.
- No protected client intelligence, private vendor sources or undisclosed obligations used.
- Sensitivity analysis on approved weights completed; caveats and residual unknowns published.

Until these are satisfied, conclude **fit hypotheses and verification priorities**, not a ranked “best DAF platform.”
