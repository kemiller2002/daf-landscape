# Batch 3: Ren related-party economics and migration/portability evidence
**Research date:** 2026-11-12. **Status:** PRIMARY AUDITED EVIDENCE for RCF-to-Ren payments; documented portability limitations in one sponsor migration. **Research:** M01–M04, T01–T06, V07, V15, R04.

## Executive findings
1. **RCF's audited FY2024 statements, Note 9 (p17), disclose a 98% administrative-fee sharing formula and $19,225,546 paid to Renaissance Acquisition Company LLC (Ren) in 2024, versus $15,543,682 in 2023.** This is directly attributable to the related-party service arrangement, NOT a profit figure or Edward Jones-specific payment.
2. **Historical FY2020 audit, Note 9 (p17), disclosed a 95% fee-sharing formula with RenPSG and $7,514,718 paid in 2020 ($7,431,300 in 2019).** Formula changed between 2020 and 2023, but exact effective date and contractual rationale not established.
3. **AEF has migrated from DonorCentral to Ren's DAF platform.** Its transition notice says access to DonorCentral ended Oct 31, 2026 and the new platform has only **two years of historical account activity**, with older reports available through AEF staff. This is direct evidence of a *user-visible historical data migration constraint*, not proof of loss of sponsor records, bad data migration, or Ren vendor lock-in.
4. **Ren's public product description offers Data Migration, SSO Setup, API Integration and DFX Branding as separately named add-on services.** This demonstrates the vendor supports migration into DFX and integration options; it does NOT demonstrate contractual right or technical ability to export all data out of DFX.
5. **Morgan Stanley GIFT explicitly identifies RenPSG as an unaffiliated back-office administrator**, while Morgan Stanley Smith Barney LLC provides investment management. This is a separate sponsor model from RCF's related-party arrangement.

## Audited RCF evidence and arithmetic
**Source** https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf
Note 1 p8: RCF contracted with **Renaissance Acquisition Company LLC (Ren)** for accounting, transaction processing, donor-account contributions/distributions, customer service, tax and regulatory reports and charitable planning.
Note 9 p17: RCF and Ren are related parties but not financially interrelated organizations; two Ren employees sit on RCF board; payments equal **98% of administrative fee revenue from individual fundholder accounts** for FY2024 and FY2023.
Payments: 2024 $19,225,546; 2023 $15,543,682. Change $3,681,864 / $15,543,682 = **23.69%**.
Derived fee-revenue base under literal 98% formula (assuming no other contract adjustments): 2024 ~$19,617,904; 2023 ~$15,860,900. These are **inferences**, not separately audited total revenue or exact contractual billings; prefer audited direct payments.
The same 2024 audit has total management/general expenses $19,454,266, but this must **not** be added to Ren payments because Ren fees are included in expenses. The remaining amount is not automatically sponsor margin: other revenues, costs, restrictions and service obligations matter.
FY2024 RCF DAF assets ~$5.914b in IRS 990; no reliable inference of Ren's entire company revenue or margin from this one contract.

**Historical source** https://renaissancecharitable.org/wp-content/uploads/2026/01/2020AUDITFINAL.pdf
Note 9 p17: 2020 and 2019 formula **95%** of RCF administrative fee revenue from individual fundholders. 2020 $7,514,718; 2019 $7,431,300.
Historical legal entity described as RenPSG, formerly Renaissance Administration LLC. 2024 legal counterparty is Renaissance Acquisition Company LLC; investigate legal succession and any entity changes rather than assuming same corporation across years.

## Migration evidence: AEF
**Source** https://engage.aefonline.org/dc-sunset/
AEF states:
- DonorCentral access ended Oct 31 2026.
- AEF moved its technology to **Ren's donor-advised fund platform**.
- New platform displays **only the prior two years of account history**; users needing older grants and gifts must request records from AEF staff.
- This is **not** proof that older records were destroyed, that migration failed, or that AEF cannot export data internally.
- It is evidence that data continuity for donors is not necessarily preserved in the new interface, creating customer-service and reporting friction.
- Note: page appeared in search but a direct open returned 404 during this session; archive screenshot/working AEF link should be obtained for durable corroboration.

## Ren's migration product
**Source** https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf
Named add-ons: DFX branding, SSO setup, data migration of accounts and transaction history onto DFX, API integration and premium analytics. **Inbound migration** does not prove full outbound export, open data standards, or transition assistance on termination.
Need data model: donor/fund identities, contribution tax receipts, grant recommendations, screening evidence, approval decisions, transaction and NAV histories, grants payable, recipient identifiers, payment references, audit logs, account authorizations, correspondence and attachments.

## Legal/operational distinctions
- Ren receives service fee revenue from RCF, but **RCF retains sponsor grant discretion**. Related-party board overlap deserves governance review; no evidence of wrongdoing.
- Ren's RCF contract is not proof Morgan Stanley GIFT, Edward Jones, Northwestern Mutual, Ameriprise or LPL use identical fee sharing.
- Program-specific service fees and donor assets must not be double-counted as Ren revenue.
- AEF migration shows **switching onto Ren**, not evidence of switching away. We cannot yet quantify the cost of leaving Ren.
- RCF's audited 2024 grants payable $13,771,634 (vs $32,581,390 in 2023) are year-end liabilities, not an approval backlog count or evidence of processing delays.

## Clarity conclusions
**Verified:** 98% RCF admin-fee sharing with Ren for 2023–24; payments $19.23m in 2024.
**Verified:** 95% historical fee sharing with RenPSG for 2019–20.
**Verified:** Ren offers inbound data migration, SSO and API integration services.
**Supported with access caveat:** AEF publicly stated a switch to Ren and two-year portal-history limit.
**Unverified:** Ren's operating margin, total revenue, customer-specific profitability, concentration by institution, exit fees, contract term, historical data retention, sponsor grant automation rates, system availability and recovery objectives.

## Research priorities
1. Retrieve RCF 2021–22 audited Note 9 to date 95→98% formula transition and track legal counterparties.
2. Inspect 2024 RCF Form 990 Schedule L/O/R to reconcile governance and payments with audit.
3. Quantify the separate administrative-fee flows for Morgan Stanley GIFT and other institutional Ren customers where audited notes name Ren.
4. Verify AEF migration notice through archived source and donor-facing help center; distinguish user-visible history from sponsor archival records.
5. Obtain Ren export/termination clauses and a technical data-portability checklist; do not assert exit lock-in without evidence.
6. Compare independent vendors on grant approval provenance, exception management and liquidation/payment integration.
