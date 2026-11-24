# Cross-industry DAF operating model findings

Date: 2026-11-23. Status: secondary research synthesis and hypothesis register, not independently validated industry evidence. Source: Unbound cross-industry requirements discovery, pinned revision 6cb102250900b1b1e859bd47fcb7e4aca82ec298. This report extracts transferable business knowledge only; product requirements, architecture decisions and acceptance criteria remain in Unbound.

## Executive synthesis

A DAF sponsor combines charitable stewardship, financial administration, investment operations, payments, customer service, compliance and relationship management. Comparing these functions with mature adjacent industries exposes missing operational mechanics more often than missing headline capabilities. The source project mapped 368 capabilities and reported 150 proposed requirements, 31 refinements, 38 conflicts and 148 failure catalog entries. These are counts from one product discovery exercise, not measurements of industry-wide deficiencies.

The principal opportunity is to reduce avoidable work without weakening charitable control, financial integrity or service quality. The principal risk is importing the overhead of every adjacent industry into one organization.

## Transferable capabilities

| Industry | Transferable practice | Boundary |
|---|---|---|
| Banking and payments | Reconciliation, payment authorization, returns, fraud controls, destination verification | Do not assume sponsors or vendors are banks or money transmitters |
| Accounting and fund administration | Authoritative journals, period close, corrections, fund attribution, external reconciliation | Management estimates are not accounting entries |
| Wealth management and custody | Asset settlement, valuation, advisor authority, relationship continuity | Donor advice is not ownership or unrestricted withdrawal authority |
| Contact centers | Case ownership, resolution cost, repeat contact, escalation, service recovery | Do not impose call-center staffing or productivity metrics indiscriminately |
| Insurance and claims | Restricted investigations, exception handling, evidence and reconsideration | Not every grant is a claim or needs human review |
| Enterprise SaaS | Tenant isolation, policy defaults, delegated authority, migration and exit | Avoid configuration proliferation and vendor lock-in |
| Nonprofit grantmaking | Eligibility evidence, restricted purposes, post-payment remediation | Sponsor-specific policies must not be confused with law |

## Operating economics and small accounts

The source models imply $244–$272 fully allocated annual cost per account. These figures are illustrative, not observed costs or industry benchmarks. At an assumed 0.60% annual asset fee, a $5,000 balance yields $30 and a $50,000 balance yields $300 before other revenue or expenses. A simplified break-even balance at the modeled cost is $40,667–$45,333. At a hypothetical $25 annual cost it is $4,167. Neither calculation establishes commercial viability.

Separate fixed, marginal, incremental, step-fixed and allocated costs. Distinguish sponsor, fund, platform and partner expense bearers. Measure per account-year, contribution, grant, resolved case, verification, exception, payment rail and AI run. Reconcile attribution to actual operating expenses and disclose unallocated residuals. Do not reward delayed grants, unsafe approvals or exclusion of low-balance donors. Evaluate fee floors, subscriptions, employer sponsorship, cross-subsidy and asset-based fees against donor outcomes and applicable law.

Test whether low-balance exclusion reflects unavoidable obligations, legacy technology, avoidable human touch, pricing or distribution economics. Compare digital-first and conventional sponsors using audited filings, disclosed fee schedules, account cohorts, actual workload and vendor contracts; do not equate payment-processor accounts with DAF accounts.

## Financial integrity and regulatory exposure

The source identifies questions around custody/title and commingling, money transmission, investment advice and transaction-based compensation, fundraising-platform obligations, recurring debit authorization, chargebacks, uncashed checks, post-payment violations and sponsor migration. Applicability depends on actual activities, entities, jurisdiction, contracts and exemptions. No categorical licensing conclusion is adopted here.

Research ASC 958 variance power, agency liabilities, grant recognition, Form 990 Schedule D reconciliation, donor acknowledgments and fee payer identity with CPA review. Investigate post-payment correction and excise reporting with counsel. Verify current primary authorities, including IRC 4966/4967, applicable payment-network rules and foreign-grant guidance; distinguish statutes, final rules, proposals, contractual rules and voluntary controls. The source's provisional legal decisions are not legal opinions.

## Organization, service and AI

Use shared case concepts but separate lifecycle, permissions, evidence retention and independence where required. Restrict fraud investigations and sensitive evidence from general service queues. Measure resolution rather than raw contacts. Evaluate default policy packs, exception-driven human involvement, outsourced specialists and seasonal capacity. The source's 6–8 person staffing floor is an unvalidated assumption, not an industry minimum.

Redesign workflows around desired outcomes: routine contribution and grant processing, recurring charity monitoring, reconciliation, donor service and sponsor onboarding. Use deterministic controls for known rules; use AI for ambiguous evidence and assistance where measured benefits exceed costs. Require authorized decisions, evidence provenance, fallback and escalation. Evaluate false approvals, false denials, rework, service accessibility and cost together. Never infer that automation removes legal responsibility.

## Clarity / EDF-style challenge (preliminary, not a formal framework execution)

| Hypothesis | Competing explanation | Evidence needed |
|---|---|---|
| Legacy processes drive high servicing cost | Fixed regulatory, custody or distribution costs dominate | Activity-level actuals and matched sponsor cohorts |
| Automation makes small accounts viable | Exception tails and acquisition costs erase savings | Marginal cost curves, retention, stress scenarios |
| Shared policy packs reduce overhead | Sponsor diversity creates expensive exceptions | Onboarding time, override frequency, policy maintenance |
| AI reduces human work | Review and correction merely shift work downstream | Controlled workflow comparison, total touch time, error and rework |
| Integrated operations reduce reconciliation | External books and settlement boundaries remain unavoidable | Reconciliation breaks and resolution times before/after |

Do not treat correlations as causal evidence. Define counterfactuals and falsification criteria before experiments. Report uncertainty and rejected hypotheses. Formal Clarity and EDF evaluation remains follow-up work.

## Research agenda

1. Collect audited sponsor expenses, account counts, asset distributions and grant volumes; normalize denominators and expense bearers.
2. Establish marginal cost curves and exception distributions across account sizes and payment types.
3. Compare sponsor pricing, minimums, distribution and service models, including digital challengers and employer programs.
4. Obtain legal and accounting review of the operating-model exposure matrix and payment obligations.
5. Investigate actual staffing, segregation of duties, outsourcing, seasonal demand and service accessibility.
6. Test zero-touch workflows against safety, accuracy, donor experience and total cost; quantify displaced rather than eliminated work.
7. Study sponsor exits, custody failures and migration controls using primary evidence, without treating individual failures as proof of industry prevalence.
8. Apply formal Clarity and EDF methods and integrate only supported conclusions into the industry report.

## Provenance and related research

Pinned source reports:
- [Executive findings](https://github.com/kemiller2002/unbound/blob/6cb102250900b1b1e859bd47fcb7e4aca82ec298/requirements/discovery/2026-11-23-cross-industry/10-EXECUTIVE-FINDINGS.md)
- [Capability atlas](https://github.com/kemiller2002/unbound/blob/6cb102250900b1b1e859bd47fcb7e4aca82ec298/requirements/discovery/2026-11-23-cross-industry/01-CAPABILITY-ATLAS.md)
- [Regulatory applicability](https://github.com/kemiller2002/unbound/blob/6cb102250900b1b1e859bd47fcb7e4aca82ec298/requirements/discovery/2026-11-23-cross-industry/07-REGULATORY-APPLICABILITY-MATRIX.md)
- [Operating economics](https://github.com/kemiller2002/unbound/blob/6cb102250900b1b1e859bd47fcb7e4aca82ec298/requirements/discovery/2026-11-23-cross-industry/11-OPERATING-ECONOMICS.md)
- [Business models](https://github.com/kemiller2002/unbound/blob/6cb102250900b1b1e859bd47fcb7e4aca82ec298/requirements/discovery/2026-11-23-cross-industry/13-BUSINESS-MODEL-ANALYSIS.md)
- [Adversarial review](https://github.com/kemiller2002/unbound/blob/6cb102250900b1b1e859bd47fcb7e4aca82ec298/requirements/discovery/2026-11-23-cross-industry/14-ADVERSARIAL-REVIEW.md)
- [Provisional legal/accounting decisions](https://github.com/kemiller2002/unbound/blob/6cb102250900b1b1e859bd47fcb7e4aca82ec298/requirements/discovery/2026-11-23-cross-industry/16-LEGAL-AND-ACCOUNTING-DECISIONS.md)

Existing landscape research to reconcile:
- [Cross-industry value chain](cross-industry-daf-economic-value-chain-2026-11-11.md)
- [Economics and distribution](daf-economics-and-distribution-2026-11-11.md)
- [Grant exception economics](daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md)
- [Challenger economics](challenger-economics-daffy-chariot-charityvest-2026-11-12.md)
- [AI-native enterprise](ai-native-daf-enterprise/)
- [Clarity assumption audit](clarity-report-assumption-audit-2026-11-11.md)

The source used same-model research and adversarial passes; no independent human validation or executed acceptance tests are established. Its requirements approval gate remained FAIL. Preserve this distinction when citing this synthesis. Future Unbound discoveries may generate landscape research questions, but landscape evidence and Unbound product decisions remain separately authoritative.
