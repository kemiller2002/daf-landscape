# Ren iPhi: contractual, product and integration architecture audit
Date: 2026-11-12. Research streams T01–T08, V07–V15, M03. Source status: primary vendor documentation, NOT internal code or executed customer contract.

## Conclusion
**Verified multi-product portfolio, unverified unified architecture.** Ren acquired Stellar Technology Solutions and its iPhi CoreEnterprise system in Jan 2023. Ren separately publishes iPhi platform MSA and product definitions from its Renaissance Acquisition Company general MSA and product descriptions. iPhi has a central ledger/accounting and participant subaccounting system and a collection of real-time PrivateViews portals. Ren's acquisition strategy promised integration with Ren for Charities, especially ACH payment and charity interfaces. This is evidence of distinct product lineage and intended service integration, NOT proof of one unified database or proof the products remain entirely isolated today.

## Direct primary sources
1. iPhi MSA, June 20, 2023: https://www.reninc.com/wp-content/uploads/2023/07/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20.pdf
2. iPhi product schedule: https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Product-Descriptions-v1.pdf
3. Ren master agreement library: https://www.reninc.com/master-service-agreements/
4. Ren Stellar acquisition announcement Jan 20, 2023: https://www.reninc.com/blog/ren-bolsters-philanthropic-tech-services-offerings-with-acquisition-of-stellar-technology-solutions/
5. Ren strategic integration essay: https://www.reninc.com/blog/why-ren-and-stellar-are-combining/
6. Ren general RAC MSA: https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf
7. Ren Giving Platform: https://www.reninc.com/giving-platform/

## iPhi contract details (read actual sections)
- §1.8: 'Customer Content' is information the customer enters/submits/transmits through platform.
- §3.1: Ren owns platform and professional services; customer gets limited use license.
- §3.2: customer owns Customer Content; Ren obtains perpetual irrevocable right to use **anonymized** Customer Content for lawful purposes including benchmarking/improvement. This is not unrestricted use of identifiable donor records.
- §3.3: customer assigns feedback rights to Ren.
- §3.4: forbids use/view of services to create commercially competitive product, in addition to reverse-engineering.
- §4: order form/SOW determine actual fees, billed monthly in advance unless otherwise specified.
- §5.1: notification of suspected security incident within 72 hours of discovery.
- §6.2: no material degradation warranty, but no blanket promise of error-free uninterrupted platform.
- §8: generally fees-paid/payable 12-month liability cap, with exceptions.
- §9: insurance minima include cyber $2m, E&O $1m claim/$2m aggregate, umbrella $5m; coverage promised in template, not independently verified insurance in force.
- §10.2: annual auto-renewal and notice 'thirty (60)' days, an **internal drafting inconsistency**. Do not claim a clean 60-day provision without executed contract interpretation.
- §10.3: 30-day cure for material breach.
- §10.5: access ceases immediately on termination; customer content made available in **industry-standard format for 15 days**; no obligation to maintain thereafter. Customer content scope may not encompass all platform-generated audit events or approval provenance.
- §11.5: assignment allowed on notice (not consent) for affiliates, restructuring, merger, sale of substantially all assets.
- §11.9: order forms and SOWs prevail over conflicting MSA provisions.
- Exhibit A SLA is referenced in definitions (§1.25), but the public PDF appears to end at page 6 without SLA exhibit. **Cannot verify uptime target, credit formula, exclusions, RTO/RPO.**

## iPhi architecture based on product descriptions
- **CoreEnterprise**: central records, real-time transaction processing, participant subaccounting, daily NAV/unitization, general ledger and reconciliation, statements.
- **PrivateViews**: DonorView, Account Opening, ClientView, AdvisorView, GranteeView, ScholarView, CommitteeView, PlannedGivingView, InvestmentPartnerView.
- **Add-ons**: SSO, MFA configuration, GuideStar charity search API, business process outsourcing.
- **BPO**: financial oversight, contribution processing, grants and payment records. This is a product/service description, not proof every customer uses the services.
- Product document says iPhi administers ~30% of DAF market, but denominator, date, counting methodology and overlap with other Ren products not established. Treat as **unverified vendor assertion**.

## Ren versus iPhi, what is demonstrable?
| Dimension | iPhi | Ren general platform |
|---|---|---|
| Public MSA | Separate SaaS platform MSA | Separate services MSA |
| Core functions | Detailed subaccounting, unitization, G/L and PrivateViews | DonorFirstX / giving and administration services |
| Customer data | Expressly customer-owned Customer Content | General MSA defines narrower 'Customer Materials' |
| Exit provision | Explicit 15-day post-termination industry-standard content availability | General MSA requires return of customer-provided materials; complete export unspecified |
| APIs/integration | GuideStar, SSO, data exchanges with trust accounting; proposed Ren for Charities ACH | Ren offers separate API integration and data migration add-ons |
| Internal stack | Not verified | Not verified |
| Cross-product data model | Not verified | Not verified |
| Shared charity decision engine | Not verified | Not verified |

## Clarity challenges
1. Distinct contracts and modules strongly support product distinction; they do NOT prove entirely separate codebases as of 2026.
2. 'One platform' in marketing may mean a unified customer experience or operational network, not one underlying ledger/database.
3. iPhi's explicit export promise is narrower than full provenance/approval/financial reconciliation portability.
4. The MSA's 15-day window is a real contractual constraint, not proof actual clients are denied extensions.
5. The MSA's conflicting 'thirty (60)' nonrenewal text is a drafting ambiguity requiring legal review, not an adjudicated defect.
6. 30% market-share claim lacks a defined denominator, so cannot compare mechanically to Ren's 'half of DAF assets' marketing.
7. Product descriptions can be legacy; require release notes, architecture evidence, active customer deployments and current contracts.

## Research hypotheses and verification
H1: iPhi CoreEnterprise and Ren's Giving Platform retain distinct accounting stores, linked via APIs and batch files. **Plausible; unverified.** Request architecture diagram, system-of-record mapping, event schemas and reconciliation protocols.
H2: Ren for Charities acts as a shared payment and charity-facing service across distinct sponsor cores. **Announced plan in 2023; actual coverage unverified.** Verify production grants from both product lines and settlement evidence.
H3: iPhi's existing back-office financial depth is an important moat even if donor experience converges. **Reasonable inference; compare real exception workflows, daily unitization, period close, investment reconciliation, and sponsor audit evidence.**
H4: Complete vendor exit requires data beyond 'Customer Content'. **Contractual scope gap; test via actual authorized export, audit-log reconstruction and financial reconciliations.**

## Next
- Obtain current iPhi release documentation, API specifications and support articles.
- Determine whether Ren's 2026 'instant grant approval' claims apply to iPhi, DonorFirstX or a shared service, and what constitutes 'instant' vs sponsor approval.
- Identify independent iPhi sponsors and their donor portals, without assuming same code or brand.
- Request full Exhibit A SLA and negotiated order-form examples.
- Compare end-to-end grant lifecycle: eligibility snapshot, review, sponsor authorization, liquidation, ACH/check, exception and reversals.
