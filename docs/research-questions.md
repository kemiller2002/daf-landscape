# Research questions and hypothesis backlog

Questions are organized around decisions the research should eventually support. Hypotheses below are explicitly **unverified** and must not be repeated as findings.

## Sponsor and operating models

1. Which legal entity sponsors each program, and which affiliates or contractors perform administration, custody, investment management, grant review, and payment?
2. Which sponsors offer their legal infrastructure under private/white-label arrangements, and where do final approval and control remain?
3. How do national, community-foundation, and mission-oriented sponsors differ in product requirements and buying processes?
4. What functions are kept in-house because of legal duty, risk, service differentiation, or economics?
5. What happens operationally when a sponsor changes an administrator, platform, custodian, or brand?

## Product and architecture

6. What is the system of record for the fund ledger, customer identity, charity eligibility, investment positions, and grant status?
7. Are sponsor platforms multi-tenant, configurable, or custom-coded, and how is one sponsor's policy isolated from another's?
8. What APIs, batch files, webhooks, and manual queues connect sponsor, custodian, bank, charity-data provider, CRM, and nonprofit?
9. How are pooled investments, separately managed accounts, fees, stale prices, and reconciliation breaks handled?
10. Which data and documents can a sponsor export if it changes vendors?

## Contributions and complex assets

11. Which asset types are truly processed in-house versus referred to an intermediary?
12. What are median cycle time, failure points, and economics for cash, securities, private interests, real estate, and crypto?
13. Who owns valuation, appraisal, liquidation, and receipt decisions?
14. How do advisor-managed investments change custody integration, fee collection, oversight, and service?

## Grant compliance and operations

15. Which data sources and rules support charity eligibility, supporting-organization checks, sanctions, fraud, private benefit, equivalency determination, and expenditure responsibility?
16. What percentage of recommendations are straight-through, manually reviewed, cured, declined, or later returned?
17. Can the decision and policy version for every grant be reconstructed for audit?
18. How are recurring grants, anonymous grants, succession, inactivity, and restricted purposes handled?

## Disbursement and nonprofit experience

19. Who initiates the recommendation, who approves it, who moves money, and who supplies remittance data in each integration?
20. What proportion of grants travels by ACH, check, wire, intermediary charity, or other rail?
21. How often can nonprofits match a payment to the donor, purpose, and campaign without manual outreach?
22. How are returned ACH, uncashed checks, bad addresses, refunds, reissues, and unclaimed funds resolved?
23. Which tools improve donor attribution without overriding anonymity choices?

## Market and commercial questions

24. Who buys each layer: sponsor, wealth manager, community foundation, employer, nonprofit, fundraiser, or donor?
25. What are pricing units, implementation costs, minimums, revenue shares, custody economics, and switching costs?
26. Which capabilities win competitive deals, and which are table stakes?
27. How concentrated are sponsor assets and platform dependencies when measured with a common year and definition?
28. Which disclosed customers can be verified, and what workloads actually run on each platform?

## Security, resilience, and governance

29. What assurance reports, penetration testing, availability history, recovery objectives, and incident disclosures exist?
30. How are donor credentials handled in embedded grant-initiation flows?
31. Which subcontractors can access identity, account, investment, grant, or nonprofit banking data?
32. How do boards oversee outsourced administrators and resolve conflicts with financial-services affiliates?
33. How would pending IRS guidance under sections 4966 and 6033 change definitions, advisor/vendor relationships, reporting, controls, and product economics?

## Hypotheses — unverified

| ID | Hypothesis | Evidence needed to test | Status |
| --- | --- | --- | --- |
| HYP-001 | Most scaled DAF programs use a modular stack across sponsor, custody, ledger/portal, charity data, and disbursement rather than one vertically integrated system. | Named architecture maps from at least 10 sponsors; contracts; integration evidence | Untested |
| HYP-002 | Wealth managers buy white-label DAF programs primarily to retain advisor/client relationships and assets, while sponsor operations are a secondary buying concern. | Buyer interviews, RFP criteria, win/loss evidence, pricing and custody terms | Untested |
| HYP-003 | Grant payment and remittance reconciliation is a larger nonprofit pain point than submitting the donor's recommendation. | Nonprofit finance interviews; unmatched-payment rate; time-to-reconcile data | Untested |
| HYP-004 | Complex-asset capability is concentrated in operational teams and intermediaries that are not visible in the donor-facing brand. | Asset-by-asset workflow maps, referrals, service contracts, case-volume data | Untested |
| HYP-005 | Community foundations place more weight on integrated fund accounting and local donor service than national sponsor programs do. | Segmented RFPs, demos, interviews, implementation and renewal evidence | Untested |
| HYP-006 | “Open architecture” differs materially by provider and may refer separately to custodian choice, advisor management, investment choice, APIs, or sponsor choice. | Contract definitions and capability tests across providers | Untested |
| HYP-007 | Vendor-reported asset or market-share figures are not directly comparable because sponsor assets, administered assets, platform assets, and affiliate programs use different denominators. | Metric definitions, dates, customer lists, audited or third-party corroboration | Untested |
| HYP-008 | Sponsor switching costs are driven more by data conversion, ledger reconciliation, custody changes, and donor communication than by the donor portal itself. | Migration plans, implementation effort, reconciliation defects, sponsor interviews | Untested |

## Interview evidence standard

Capture interviewee role, organization type, date, direct experience, product/version, and whether statements may be attributed. Treat a single interview as a lead, not a market fact. Promote a hypothesis only after triangulation across different roles and documentary evidence.
