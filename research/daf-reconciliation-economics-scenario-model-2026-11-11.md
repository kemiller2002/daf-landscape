# DAF reconciliation economics: quantified hypothesis test
**Date:** 2026-11-11. **Status:** Scenario model, not measured savings, market sizing or willingness-to-pay study.

## Verified scale inputs
- Fidelity Charitable 2026 Giving Report states approximately **3 million donor-recommended grants in calendar 2025**. Source: https://www.fidelitycharitable.org/insights/2026-giving-report.html
- NPT FY2025 report states **159,543 grants** in FY July 1 2024 to June 30 2025. Source: https://www.nptrust.org/annual-reports/npt-annual-report/
- These are sponsor-specific counts with differing periods; do not add them as a uniform industry total.
- DAF Research Collaborative's 2025 DAF report was **revised in spring 2026**. Use updated memo/dataset for sector totals, not superseded 2025 headline numbers. Source https://www.dafresearchcollaborative.org/research/annual-daf-report

## Model
Annual potential labor savings = annual grants × share requiring manual intervention × minutes eliminated per intervention / 60 × fully loaded hourly cost.
**No reliable DAF-specific benchmark for exception rate, handling time or fully loaded cost was established in this pass. Every one of these is an illustrative assumption.** Do not represent output as current expenditure or an observed cost reduction.

| Illustrative case | Manual exception rate | Minutes eliminated per affected grant | Fully loaded hourly labor | Savings / 100,000 grants | Applied to Fidelity 3m grants | Applied to NPT 159,543 grants |
|---|---:|---:|---:|---:|---:|---:|
| Low | 5% | 5 | $30 | $12,500 | $375,000 | $19,943 |
| Base | 10% | 10 | $40 | $66,667 | $2,000,000 | $106,362 |
| High | 20% | 20 | $50 | $333,333 | $10,000,000 | $531,810 |

### Important unit of analysis
Sponsor grant counts are **not automatically recipient-side reconciliation events**. A single payment can aggregate grants; one grant may generate multiple attempts or ledger events; some recipient tasks happen for every grant, not just exceptions. The scenarios assume one grant as the exposure unit for simplicity and must be revised when real payment/event data is available.

## Who experiences the cost?
1. **Recipient nonprofit**: development operations and finance matching deposits, remittance, donor soft credit, restrictions and acknowledgements. May have the largest unpriced burden, but evidence insufficient to rank.
2. **DAF sponsor**: service desk, returned checks, address verification, donor communications, compliance escalation. Sponsor has direct incentive if exception handling consumes its own labor.
3. **Payment processor**: support, payout failures, unclaimed/expired grants, payment data exports. Incentive depends on contracts and volume.
4. **CRM/gift processing vendor**: support and data import quality, potential feature differentiation; may not capture donor-side benefit.
5. **Donor/adviser**: time, uncertainty and reputational friction; difficult to monetize without retention data.

**Economic incidence mismatch:** Recipient may bear cost while sponsor or processor controls data needed to solve it. This is a two-sided adoption barrier, not merely a technical integration problem.

## What a buyer would pay (hypothesis, not price evidence)
For a recipient with 1,000 DAF grants per year, base-case gross labor savings = $667/year. That may be too little for a standalone enterprise product after setup, training, integration and annual fees. For a sponsor with 100,000 grants, base-case modeled labor savings = $66,667/year **only if the sponsor itself captures the assumed savings**. If savings occur at charities instead, sponsor ROI cannot claim them.

At 100,000 grants and $66,667 modeled savings, a $50,000 annual product plus $20,000 integration cost would yield **negative first-year direct labor ROI**. A $10,000 subscription plus $5,000 annualized integration cost would yield positive modeled direct ROI, but real value depends on measured baseline and coverage. Neither is a market price quote.

## Distinct business models
- **Sponsor-paid service**: focus on support workload, faster issue resolution, donor retention and compliance. Strongest if sponsor can change data export and payment workflows.
- **Nonprofit-paid CRM integration**: focus on matching, fund attribution, restrictions and receipts. Needs enough transaction volume or bundling.
- **Processor/CRM embedded feature**: distribute at low marginal cost, monetize within existing platforms. Potentially lower acquisition friction.
- **Consortium standard**: shared grant reference and remittance schema; may produce greater sector welfare but weak direct revenue capture. Need governance and privacy rules.

## Clarity: claims and counterarguments
- 'Millions of grants imply a billion-dollar software market': **unsupported**. Volume is not revenue, and per-grant time savings may be small.
- 'Nonprofits will pay because they benefit': **unsupported**. Nonprofits may have low budgets and sponsors control critical data.
- 'Every grant requires manual reconciliation': **unsupported**. Some processors provide detailed remittance and automated imports.
- 'One industry-wide ID fixes the problem': **refuted as sufficient**. Processor IDs already exist; provenance, aggregation, privacy and exception handling remain.
- 'Sponsors capture all time savings': **unsupported**. Savings may accrue to nonprofit recipients.

## Interview/measurement protocol
Sample across small, midsize and large charities; donor-funded charities with different grant volumes; development operations and finance; sponsors; payment processors; CRM vendors. Ask for **last 30–90 days** (not lifetime recollections): number of DAF grants received, by rail, percentage automatically matched, number manually researched, median/p90 minutes, staff role and fully loaded cost, return/reissue count, unresolved exceptions, number of distinct grant IDs and remittance formats. Ask what *already works* and why.

Where possible, request **redacted aggregated metrics**, not donor records. Separate per-grant ordinary work from exceptional work. Track which institution can change the workflow. Explicitly measure one-to-many remittance mappings and anonymity controls.

## Gate before commercial conclusion
Do not recommend building a standalone product until: (1) observed baseline and savings; (2) buyer and budget owner identified; (3) access to representative source formats; (4) lawful data sharing and integration feasible; (5) evidence of willingness to pay; (6) comparison against existing processor and CRM features; (7) total implementation cost. This is a research opportunity, not validated product-market fit.

## Next source tasks
- Review DAFRC spring 2026 revised dataset for consistent sector grant volume.
- Review Salesforce Nonprofit Cloud, Blackbaud Raiser's Edge NXT, Bloomerang, PayPal Grant Payments and Fidelity nonprofit remittance features for preexisting matching automation.
- Recruit recipient finance staff and sponsors through permission-based public forums with role-specific questions.
- Test base-case assumptions with 10+ independent anonymized interviews and 2+ transaction samples before sizing an addressable market.
