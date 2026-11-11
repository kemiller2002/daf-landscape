# Bank of America and Morgan Stanley: institutional DAF economics and Ren relationships
**Date:** 2026-11-11
**Status:** Public documentary evidence; no private contracts, scoped SOC reports, production access, or verified vendor payments.

## Executive findings
1. **Morgan Stanley explicitly identifies RenPSG** as the unaffiliated back-office administrator of Morgan Stanley Global Impact Funding Trust (MS GIFT) on its official program site. Morgan Stanley Smith Barney LLC supplies investment management. This is a confirmed public statement of a functional supplier relationship, not proof of fee amount or complete ledger/control scope. https://www.morganstanley.com/what-we-do/wealth-management/gift
2. **Ren's 2025 Giving Season FAQ explicitly references Morgan Stanley GIFT** and says its donors access DAFs through Morgan Stanley Online, not separate credentials. This supports integration/operational connection; it does not independently prove SSO protocol, security boundaries or contract terms. https://www.reninc.com/giving-season-2025-commonly-asked-questions/
3. **Bank of America's Charitable Gift Fund donor portal** at https://bofa.donorfirst.org/ points users needing account reactivation to charitablegiftfund@reninc.com. This is an observable Ren-branded support connection, not yet a signed statement of the exact service scope.
4. **BofA Charitable Gift Fund FY2024 Form 990** reports $5,038,097,658 net assets, $1,489,652,673 contributions, $993,629,953 total expenses, and $24,062,159 listed as trustee compensation for Bank of America. This last amount should be checked in the original Part VII/Schedule context before describing it as a specific DAF administrative-fee flow. https://projects.propublica.org/nonprofits/organizations/46010342
5. **MS GIFT FY2024 Schedule D** secondary extracted table reports ~$9.11 billion end-of-year DAF assets, 21,800 funds, and ~$1.65 billion grants. FY2024 Part IX reports approximately $16.0 million 'other fees for services', $4.2 million investment management fees and $22.7 million management expenses. These are expense *categories*, not established Ren payments; exact original-return values and named payees require verification. https://philanthropy.org/990/report/527082731/morgan-stanley-global-impact-funding-trust-inc
6. **BofA FY2025 10-K / Morgan Stanley 10-K** consolidated wealth segment reporting does not substitute for sponsor Form 990, trustee accounts, and supplier invoices. Do not infer DAF supplier economics from bank segment revenue.

## Evidence-strength comparison
| Claim | Status | Basis | What remains unknown |
|---|---|---|---|
| MS GIFT uses RenPSG for back-office administration | Explicitly disclosed by institution | Morgan Stanley official GIFT disclosures | Signed contract, services, current pricing, ledger scope, term |
| MS GIFT donor portal integrates with Morgan Stanley Online | Vendor operational statement | Ren Giving Season 2025 FAQ | Authentication design, data boundaries, SSO security |
| BofA CGF has Ren-linked portal support | Directly observable | BofA donorfirst.org login instructions | Full administration contract, supplier scope and amounts |
| BofA trustee compensation $24.06m FY2024 | Form 990 extracted disclosure | ProPublica BofA CGF FY2024 | Precise legal accounting characterization and split |
| MS GIFT other services fees ~$16m FY2024 | Form 990 secondary extraction | Philanthropy.org FY2024 Part IX | Named vendors, whether Ren receives any/all, exact value |
| Ren earns combined fees from both programs | Unverified | No signed payment evidence | Payee-specific statements or filings |
| Ren is the ledger of record for both | Unverified | Portal and back-office relationship alone insufficient | System controls and reconciliation tests |

## Scale without overclaiming
- The two FY2024 charitable organizations' reported asset measures are not exactly the same: BofA **net assets** ~$5.038b, MS GIFT **DAF assets/end-of-year** ~$9.11b. Their approximate sum (~$14.15b) is a **mixed-definition exposure indicator**, *not* Ren-administered assets, revenue, customer concentration, software AUM, or a precise comparable total.
- MS GIFT 21,800 funds and ~$1.65b grants are meaningful sponsor scale, but no number of Ren-processed transactions or settled payments has been independently verified.
- Ren's existing audited **RCF→Ren FY2024 $19.225546m** payment is a *different, specifically identified supplier fee flow*. Do not apply its 98%-of-fundholder-fees contract to BofA or Morgan Stanley.

## Clarity challenges
**C1:** 'Morgan Stanley is a Ren customer' → supported only in the bounded sense that its sponsored GIFT program publicly names RenPSG as administrator; legal contractual customer may be the sponsor entity, not Morgan Stanley corporate parent.
**C2:** 'BofA also outsources its entire DAF to Ren' → overreach. Ren-linked support is evidence of operational involvement, not complete outsourcing.
**C3:** 'MS GIFT other services expenses are Ren revenue' → unproven without Part IX/Schedule O detail or supplier invoice.
**C4:** 'Banks own the DAF assets' → legally distinguish sponsor charitable entity/trustee from donors, bank wealth clients and custodian.
**C5:** 'Large asset base proves platform moat' → assets and fund count indicate exposure, not switching cost, margins, retention or product quality.

## EDF system boundary
Actors: donor, Morgan Stanley adviser, MS GIFT sponsor/board, Morgan Stanley Smith Barney investment management, RenPSG back-office administration, custody/banking, payment processor, recipient nonprofit. Potential diagnostic failure boundaries: account onboarding and identity handoff, investment-position synchronization, grant authorization, return/reversal reconciliation, historical record portability, vendor shutdown. No actual incident inferred.

## Follow-up diligence
1. Obtain original FY2024 and FY2025 (when filed) 990 XML/PDF for both charitable programs. Extract Part IX, Schedule D, Schedule O, Schedule L, related-party and independent-contractor disclosures; identify named payees and grant totals.
2. Compare 2020–2024 fund counts, contribution flows, payout, investment returns, admin expenses and trustee/related-party payments, using consistent accounting definitions.
3. Verify exact MS GIFT RenPSG contract scope and whether administrative costs in Form 990 include payments to Ren or another affiliate.
4. Verify BofA's Ren relationship via official disclosure or authorized contract and identify which services Ren operates.
5. Trace Morgan Stanley Online → Ren back-office authentication and data responsibility only via authorized evidence.
6. Extend institutional relationship mapping to Wells Fargo, JPMorgan, UBS, Goldman Sachs, BNY, Citi, Fidelity, Schwab, SEI and independent sponsors. Each relationship must be individually evidenced; never assume Ren from sector similarity.
7. Add sponsor–supplier–payer–payee edges to an entity-level graph with confidence, period, source, role and unknown amount.

## Source register
- MS1 Morgan Stanley official GIFT page https://www.morganstanley.com/what-we-do/wealth-management/gift
- MS2 Morgan Stanley official GIFT content https://www.morganstanley.com/what-we-do/wealth-management/gift/content-hub
- MS3 Ren 2025 GIFT operational FAQ https://www.reninc.com/giving-season-2025-commonly-asked-questions/
- MS4 MS GIFT Form 990 archive https://projects.propublica.org/nonprofits/organizations/527082731
- MS5 MS GIFT secondary 990 tables https://philanthropy.org/990/report/527082731/morgan-stanley-global-impact-funding-trust-inc
- BA1 BofA CGF Form 990 archive https://projects.propublica.org/nonprofits/organizations/46010342
- BA2 BofA donor portal https://bofa.donorfirst.org/
- BA3 BofA 2025 10-K https://investor.bankofamerica.com/regulatory-and-other-filings/select-sec-filings/content/0000070858-26-000157/bac-20251231.htm
- Prior internal evidence [BofA review](bofa-charitable-gift-fund-10k-ren-relationship-2026-11-11.md) and [transaction economics](transaction-economics-evidence-package-001-2026-11-11.md).

**Methodology caution:** Secondary extracted 990 values should be treated as provisional until matched to original IRS return line items. Public disclosures establish functional relationships, not current contractual terms, vendor financial performance, or independent operational correctness.
