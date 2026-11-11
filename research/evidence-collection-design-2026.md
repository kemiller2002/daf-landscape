# DAF market evidence collection and measurement contract (proposed)

**Design date: November 11, 2026. Status: no live collection, third-party tests, data-room access or prospective interview participants enrolled.** Use public DAFRC revised source data when accessible, then permissioned synthetic/aggregated institutional data. This is a **measurement specification**, not an authorization to pull private donor information.

## Measurement design principles

1. **Every row has an entity and time boundary.** Legal sponsor EIN, platform vendor legal entity, wealth institution, fund/account ID (pseudonymized), nonprofit recipient EIN, grant status and reporting fiscal period must never be collapsed into a "customer" field.
2. **Every number states a denominator.** Grant count, donor people, DAF fund count, sponsor institutions, software-contract logos, dollar assets, donor CRM retention and paid transaction counts are different units.
3. **Assets are not revenue.** Report sponsor-held assets, invested billable AUM, billed contract fees, recognized software revenue, grant throughput and transfer-related balances separately.
4. **Self-reported metrics require quality class.** `auditor_statement`, `official_regulatory`, `independent_research`, `vendor_self_report`, `vendor_observed_test`, `derived_arithmetic`, `not_verified`. Marketing claims do not become actual measured products.
5. **Protect donor privacy and confidentiality.** No donor names, addresses, financial account IDs, tax returns or transaction-level person identifiers in public repositories. Use synthetic examples or authorized aggregates. Preserve anonymity, including donor restrictions on nonprofit acknowledgment.
6. **Human/legal control is part of the lifecycle.** Sponsor approval is distinct from donor recommendation or payment initiation. Irrevocable contribution, recipient eligibility and grant disbursement must have explicit proof before pass status.
7. **Version methods.** The DAFRC Spring 2026 revision replaces old FY2024 numbers; store source release, version, methodology and inclusion policy. Never interpolate between incomparable vintages.

## Public market data mart: sponsor-year table

Proposed schema (no real sponsor rows fetched yet):

| Field | Type / meaning |
|---|---|
| `sponsor_ein` | Canonical legal entity sponsor ID |
| `tax_fiscal_year_start/end` | Exact calendar dates |
| `sponsor_category` | National, community, single-issue plus subtype |
| `is_donation_processor` | Source-defined classification, not arbitrary heuristic |
| `accounts_year_end` | 990 Schedule D account count |
| `contributions_usd` | Same sponsor/fiscal-year DAF contributions |
| `grants_usd` | Grants *out of DAFs*, not full sponsor grants |
| `daf_assets_year_end_usd` | Charity-owned DAF assets |
| `origin_table_and_revision` | Full release and input row ID |
| `outlier_or_restatement_flag` | Document classification changes and amended filings |
| `platform_vendor` | `unknown` unless independent evidence supports mapping |
| `paying_platform_contract` | `not_verified` unless signed/independent evidence supports it |

Public-source acceptance: reproduce DAFRC's **1,512 FY2024 sponsors**, **3.59m accounts**, **$327.87bn assets**, **$90.57bn contributions** and **$64.60bn grants** within rounding, including processor separation. Any divergence requires reconciliation notes, not silent correction.

A dashboard must expose a **switch between all DAF sponsor types and excluding donation processors**, and show exactly which share of accounts and which share of assets changes. Vendor technology penetration must remain blank until legal entities are mapped to actual service contracts.

## Proposed operation-event grain

| Event | Critical fields | Required authority boundary |
|---|---|---|
| `donor_intent_recorded` | Pseudonymous donor; giving goal; no-DAF allowed; date | Donor provided/consented |
| `asset_offered` | Asset category; stated FMV; status; restrictions | Donor proposal, not donation |
| `sponsor_accepted_contribution` | Legal sponsor, accepted amount, legal ownership, effective tax date | Authorized sponsor/custodian proof |
| `fund_ledger_posted` | Fund ID, valuation, unitization, GL posting, corrections | Accounting approval |
| `grant_recommended` | Donor preference, recipient EIN, grant amount | Recommendation, not distribution |
| `grant_approved_or_refused` | Sponsor decision, policy, reasons, approver | Sponsor legally authorized |
| `payment_initiated` | Payment provider, rail, settlement destination pseudonym | Bank and sponsor-approved funding |
| `external_settlement_confirmed` | Recipient confirmation, timestamps, return/exception status | External recipient/financial provider evidence |
| `recipient_acknowledged` | Donor visibility preference, match status, acknowledgment | Nonprofit with consent constraints |
| `account_renewal_or_exit` | Sponsor legal contract, notice, data export | Contract and sponsor ownership, not donor fund closure by assumption |

All event timestamps must be unambiguous UTC or offset-aware timestamps plus the sponsor's local reporting period, with provenance and idempotent event IDs. Do not leak actual donor identifiers into a public artifact.

## Measurable outcomes by product/market

### Institutional sponsor operations
- **Primary:** actual dollars and staff time per **successfully settled and reconciled** grant, measured by total completed cases including correction work.
- **Secondary:** P50/P95 `approved → externally received` days, exceptions per 1,000 grant attempts, ledger discrepancy dollars, audit remediation time, last-five-years export completeness.
- **Caution:** Speed from `initiation → in-network account available` is **not external receipt**.

### Advisor donor decision technology
- **Primary:** fraction of independently reviewed cases where tool correctly recommends **DAF / direct / cash DAF / invested DAF / no gift**, based on donor intent and law, with no unauthorized irreversibility.
- **Secondary:** appropriate securities lot identification, tax input completeness, fully disclosed annual costs, actual signed gift/funding conversion among *eligible interested donors*.
- **Caution:** Number of DAFs sold is not enough to measure suitability or donor benefit.

### Nonprofit grant recipient infrastructure
- **Primary:** fraction of donor-authorized grants correctly matched to the intended supporter and reconciled to the correct donation/acknowledgment, within legal privacy choice.
- **Secondary:** missing recipient bank details, claim/return rate, time to actual receipt, grant-donor continuity, total correction labor.
- **Caution:** Full donor disclosure is **not** always the correct outcome; respect intentional anonymity.

### Revenue quality
- **Primary:** enterprise-customer **gross and net revenue retention**, based on *contractually paying legal entities* and recurring revenue with separately disclosed fixed, AUM-based and usage-linked components.
- **Secondary:** fully loaded customer margin and actual all-in donor fee allocation.
- **Caution:** Donor grants, sponsor asset changes and fintech gross payment throughput do not equal churn or technology recognized revenue.

## Experimental falsification tests

| Hypothesis | Minimum credible contrast | Falsifier |
|---|---|---|
| Improved grant portal activates dormant donor funds | Random assignment of opted-in eligible inactive accounts to redesigned portal vs control, measure *approved actual grant* | No significant difference after program or giving-season adjustment |
| Donor attribution creates nonprofit retention value | Random/stepped rollout of consent-respecting donor match, measure accurate acknowledgment and 12-month next grant | Identity matched no better than baseline, or unacceptable privacy/error costs |
| AI improves sponsor economics | Blind same-grant comparison AI + human vs existing human-first workflow, independent accuracy adjudication | No lower total fully-loaded cost **at equal or better correctness** |
| Tax Intelligence improves recommendations | Uniform synthetic inputs, CPA-reviewed expected answer, live vendor sandbox output | DAF only recommended when direct/no DAF clearly preferred; inaccurate 2026 law |
| Alternative payment infrastructure reduces cost/lag | Random/order-controlled same segment/recipient/rail, both providers, paid invoices | High exception rate or no improvement in **external** receipt/cost |
| Vendor contract moat leads to customer retention | Signed initial paying customer cohort with GRR and NRR, control for acquisitions/asset returns | Renewals weak, no repeat usage, low migration cost despite marketed integration depth |

Design choices (assignment, sample sizes, CPA reviews, sponsor approvals) must be agreed with actual permitted partners *before execution*. No statistical lift is currently claimed.

## P0 collection checklist for next work

- **Q01:** Download DAFRC 2026 revised sponsor-year dataset; reconcile source revision and donation processors.
- **Q02:** Build vendor-to-paying-legal-customer edge data from signed or otherwise attributable contracts; don't infer from partnership logos.
- **Q03:** Observe independently selected sponsor buyer process and stated pain points; collect rejection reasons as well as wins.
- **Q04/Q06/Q07:** Obtain permissioned anonymized grant **start, sponsor approval, recipient settlement and donor-match** events with explicit exception categories; reconcile to costs.
- **Q05:** Get vendor enterprise contract revenue and price tiers with recognized revenue bridges and cost data.
- **Q08:** Authorize testing the existing 18 donor suitability cases with an independent tax-review oracle; no synthetic tax-value estimates represented as vendor outcomes.
- **Q09:** Extract segmented account balance/activity distributions by institution, with consistent date and sampled population.

Each task has **source IDs, access class and acceptance criterion** in [the ranked backlog](../data/decision-critical-data-backlog-2026.csv).

## Reporting contract

Every published vendor observation must contain:
- Vendor/legal entity, specific product, version, environment, observation date, authorized tester.
- Source (auditor/IRS/independent study/vendor claim/direct benchmark), numeric observation/denominator and methodology.
- Whether the result is **actual observed**, **self-reported**, **inferred**, **derived arithmetic**, **not executed** or **unsupported**.
- Counterexample: donor fit where **not recommending a DAF** is a correct product output.
- Explicit scope of donor identity data, privacy and data use permissions.
- Independent reviewer and outstanding blockers where high-stakes tax, compliance or security conclusions are involved.

**Primary research and definitions:** [DAF market/demand report](daf-market-demand-and-evidence-gaps-2026-11-11.md), [dated observed metrics](../data/market-demand-observed-metrics-2026.csv) and [18-source register](../data/market-demand-evidence-sources-2026.csv).
