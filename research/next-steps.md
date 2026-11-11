# Next diligence steps: November 2026

The baseline is public-source research, not independently verified SOC 2 compliance. These are ranked investigation priorities.

## P0 — validate assurance, scope, and control ownership

**Ren (`reninc.com`)**
- Request the **current** SOC 2 report and explicitly ask whether a **Type II** report exists for the DAF technology and administrative services in scope. Public April 2026 language says Type I.
- Identify named legal entity, report date/period, DAF product(s), subservice organizations, CUECs, exceptions, and auditor opinion.
- Request separate SOC 1 Type II if the services support fund accounting / financial statements; ask how custody position feeds, grant authorizations and bank reconciliation are controlled.
- Verify whether the reported system applies to Ren-powered AEF, institutional programs, legacy products, and payments or only a subset.

**Chariot**
- Request current SOC 2 Type II report through its trust center. Verify whether DAFpay, Donor Accounts, API hosting, payment accounts, identity, webhooks and banking dependencies are in scope.
- Trace an end-to-end transaction from initiation through actual receipt, refund/return, and reconciliation. Document who can change each state and whether webhook retries are idempotent.
- Confirm which Donor Accounts functionality is generally available versus beta/pilot. [2026 changelog](https://docs.givechariot.com/changelog/2026/5/8) indicates beta during May 2026; do not presume production-wide access.

**TIFIN Give**
- Request current SOC 2 report and specify type, period, audited legal entity/product, auditor opinion, exceptions, covered trust criteria.
- Obtain a live integration/operations demo: white-label tenant configuration, donor/advisor permissions, custody synchronization, grant review authority, reporting and payment reconciliation.
- Clarify who the legal sponsoring charity is in each institutional implementation, and how its controls differ from TIFIN's.
- Clarify whether conversational AI can take an action, what authorization gates are enforced, and how prompt/data retention and audit trails work.

## P1 — sponsor-specific verification

**AEF:** map outsourced Ren technology against AEF's own grant decisions, custodial duties, exception handling and report responsibility. Determine data export and history accessibility after the 2026 portal migration.

**Fidelity Charitable, NPT, Schwab Charitable, Greater Horizons:** request current sponsor-level security documentation and the applicable report(s) covering the actual donor portal and transaction environment. Do not borrow attestations from parent/affiliate institutions. Determine subcontractor and platform dependencies.

**Daffy:** request scoped assurance for donor funds, API/agent permissions and payments; evaluate reversible authorization, destructive action confirmation and access revocation.

## P2 — quantitative vendor selection and economics

Construct buyer-specific (sponsor / wealth institution / nonprofit) weighted criteria after defining requirements:

| Dimension | Example tests |
|---|---|
| Security / assurance | Report scope matches purchased services; clear CUECs; no unresolved significant exceptions |
| Operational integrity | Grant cannot settle without sponsor approval; idempotent events; auditable exception resolution |
| Accounting correctness | Custody feeds reconcile; positions and grants reflect same ledger; audited reporting |
| Integration | Documented APIs/exports, SSO, event versioning, reproducible error handling |
| Donor and advisor experience | Onboarding completion, donor grant journey, advisor role separation |
| Change and portability | Data access, exit costs, historical migration, separation from vendor-specific workflows |
| Economics | Total implementation, custody economics, fees, servicing cost, cost per settled grant |
| AI controls | AI suggests but cannot bypass role-based authorization; explainable/citable decisions |

Use actual requirements and tested evidence before numeric scoring. In particular, the number of advertised features does **not** measure operational maturity or security.

## Sample security-information request (for authorized vendor diligence)

> Please provide the current independent SOC 2 report applicable to the specific DAF platform and services we would use, including report type, audit period, system scope, trust criteria, auditor opinion and exceptions. Please identify key subservice organizations, complementary user entity controls, and whether financial reporting processes are covered by a separate SOC 1 report. If the report is not publicly distributable, please describe the authorized process for reviewing it under NDA.

## Working hypotheses to test, not conclusions

1. Sponsors and asset managers may retain distribution relationships while outsourcing substantial technology operations.
2. Connectors may commoditize grant initiation but do not inherently replace sponsor approval or accounting.
3. Workflow redesign and complete intake data may outperform AI-only vetting automation for cost and latency.
4. SOC 2 evidence quality and platform capability may vary independently.
5. Shared infrastructure may mean apparent competitors have some common technology dependencies.

Each hypothesis needs counterexamples, quantitative operational metrics and a falsification plan before publication as a market conclusion.

## Refresh cadence

- Check assurance claims and source availability quarterly, and immediately after material vendor announcements.
- Record report *period* and *scope*, not just the latest trust badge.
- Reassess dated claims on product features and general availability before client-facing use.
- Keep private client inquiries, material under NDA and former-employer information outside this repository.
