# Bank of America Charitable Gift Fund: 10-K and Ren infrastructure evidence
**Date:** 2026-11-11
**Status:** Public-source documentary review; no contract or system access.

## Findings
1. Bank of America Corporation's FY2025 10-K (filed February 25, 2026) does not separately report Charitable Gift Fund DAF AUM, revenues, fees, operating costs, or grant payments. Search of filing text for "donor-advised" and "Philanthropic" returned no matches. GWIM is the relevant broad segment, but its figures are not DAF figures.
2. FY2025 GWIM reports $24.883 billion revenue net of interest expense, $4.7 billion net income, and 25% operating margin. These apply to all GWIM business, not the DAF program.
3. BofA's official Charitable Gift Fund guidelines (version 3.2024) name Bank of America, N.A. sole trustee and specify trustee discretion and donor advisory privileges; the fund has exclusive legal control of donated assets.
4. The public BofA DAF login at https://bofa.donorfirst.org/ explicitly instructs reactivating users to email **charitablegiftfund@reninc.com**. This is direct public evidence of a Ren-branded operational contact in the BofA portal environment, but does not establish the complete contractual relationship, legal sponsor, authoritative ledger, revenue, or product coverage.
5. BofA's public donor portal guide shows MyMerrill integration and donor portal workflows. This supports the hypothesis of a branded channel/front-end relationship but does not independently verify the underlying system architecture.
6. BofA's public 2026 Merrill description confirms DAF administration through Bank of America Private Bank, a division of Bank of America, N.A.; $25,000 initial and $250 additional contributions. These are program terms, not a vendor contract.

## Clarity assessment
**Claim:** Ren powers some BofA DAF servicing or portal experience.
**Observed:** BofA-branded donorfirst.org portal and explicit reninc.com support contact.
**Inference:** Ren is operationally connected to at least some portal support or access lifecycle.
**Unknown:** contractual supplier identity, which software modules, actual dates of adoption, revenue, data controller, full ledger ownership, reconciliation, SOC scope and portability.
**Counterexample:** A Ren-branded support mailbox may be used for a limited outsourced function even if BofA or another party operates other systems.
**Decision posture:** Investigate and add relationship to provider map; do not label full-platform dependency or customer revenue without contract evidence.

## EDF diagnostic hypotheses
Potential boundary between BofA trustee authority, Merrill distribution, branded donor portal, outsourced servicing, custody and grant settlement. Test how access revocation, transaction authorization, failed payment and donor history migration cross this boundary. No actual failures observed.

## Follow-up evidence requests
- BofA CGF sponsor/trustee program annual reporting and Form 990/related filings where applicable, plus trust agreement and fee schedule.
- Ren or BofA public customer case study, signed/authorized scope statement or procurement documentation confirming supplier and service scope.
- DonorFirstX technology ownership and product documentation; relationship to Ren and prior portal migrations.
- Current SOC scope, BofA complementary user controls, grant ledger authority, payment settlement, incident ownership and data export.
- Distinguish donor portal helpdesk from administrator, fund accountant, grant processor and legal trustee.
- Seek BofA-specific fee flows, account/grant counts and recipient settlement times; no estimation from GWIM segment totals.

## Sources
- [BofA FY2025 Form 10-K](https://investor.bankofamerica.com/regulatory-and-other-filings/select-sec-filings/content/0000070858-26-000157/bac-20251231.htm)
- [BofA CGF program guidelines, version 3.2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf)
- [BofA donor portal](https://bofa.donorfirst.org/)
- [BofA donor portal user guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)
- [BofA Charitable Gift Fund overview](https://www.bankofamerica.com/philanthropic/gift-fund-overview/)
- [Merrill January 8, 2026 CGF description](https://www.ml.com/articles/the-bank-of-america-charitable-gift-fund.html)
