# Cross-institution DAF grant reconciliation: evidence and architecture
**Date:** 2026-11-11
**Status:** Primary-source desk research and EDF diagnostic; no production integration or customer interviews.

## Executive finding
A transaction identifier is **not universally absent**. PayPal Grant Payments already supplies a transaction ID, grant status, grant details and CSV download capabilities to participating charities. The unresolved opportunity is **interoperability**: whether sponsor IDs, processor IDs, bank settlements, grant letters and nonprofit CRM records can be matched consistently, especially with anonymity and exceptions.

## Primary evidence
1. PayPal Grant Payments help: charity receives notification, can accept/decline, has grant details, grant letter, donor information when provided, downloadable data, transaction ID for support, and expiration/retry process. https://www.paypal.com/us/cshelp/article/what-are-grant-payments-help883
2. PayPal confirmed-charity terms: grantmaker shares charity EIN/contact data; charity's use of donor information limited to grant-related purpose without further consent. https://www.paypal.com/us/legalhub/paypal/pp-confirmed-charity-tnc?locale.x=en_US
3. Vanguard current nonprofit page confirms PayPal Grant Payments; https://www.vanguardcharitable.org/nonprofit-organizations
4. Vanguard policies: grants may be electronic or mailed checks, sponsor has legal discretion, distribution includes purpose and donor/fund details only as allowed; anonymous grants withhold adviser identity. https://www.vanguardcharitable.org/company-policies/policies-and-guidelines
5. Fidelity nonprofit FAQ: Stripe deposits show 'Fidelity grant', ACH shows 'Fidelity Charitable'; detailed individual grants are in Stripe dashboard/export or separately emailed ACH grant detail report, not necessarily bank description. Nonprofit can ask to void a lost check but reissue requires recommending donor action. https://www.fidelitycharitable.org/nonprofits/faqs.html
6. National Council of Nonprofits: thank recommending donor if disclosed, but do not issue a second tax-deductible acknowledgement; anonymous donor may not be identifiable. https://www.councilofnonprofits.org/running-nonprofit/fundraising-and-resource-development/gift-acknowledgments-saying-thank-you-donors
7. Indianapolis University research report provides mock grant correspondence/check and illustrates sponsor hard credit versus donor adviser soft credit, not a universal accounting mandate. https://scholarworks.indianapolis.iu.edu/bitstreams/e329ae0d-aa5a-4600-b976-a7f59c6391b9/download
8. PayPal Giving Fund is a separate DAF/charitable intermediary, **not** the same service as PayPal Grant Payments. Do not apply its consolidated monthly payouts or enrollment rules to Vanguard/NPT Grant Payments. https://www.paypal.com/us/cshelp/article/how-does-paypal-giving-fund-grant-donations-to-charities-help969

## End-to-end data model (proposal, not claimed industry standard)
Entities:
- `Sponsor`: legal charity, EIN
- `AdvisedFund`: sponsor-local fund ID; never assume publicly shareable
- `DonorAdviser`: optional, consented, possibly anonymous
- `GrantRecommendation`: sponsor-local request ID, purpose, restrictions
- `GrantAward`: approval, beneficiary EIN, approved amount, sponsor decision
- `PaymentInstruction`: check/ACH/PayPal/Stripe, issue ID, expected amount
- `Settlement`: processor transaction ID, bank reference, received amount, date
- `RecipientAllocation`: nonprofit CRM gift ID, sponsor hard credit, optional donor soft credit, restriction, acknowledgement
- `ExceptionCase`: lost/expired/returned/declined/unmatched/duplicate, owner, SLA, resolution

**Correlation model:** preserve all original IDs in a many-to-many crosswalk. A single grant may have multiple payment attempts, a replacement check, or processor-specific IDs; one deposit may aggregate multiple grants. Do not assume one grant = one bank deposit or use amount/date alone as a unique identifier.

## Proposed event sequence
`RecommendationSubmitted -> SponsorApproved -> PaymentIssued -> RecipientNotified -> PaymentAccepted -> Settled -> Reconciled -> Acknowledged`
With exception branches: `Declined`, `Expired`, `Returned`, `Reissued`, `Unmatched`, `DonorAnonymous`, `PurposeConflict`. Each event includes source system, source ID, event timestamp, effective timestamp, actor role, audit provenance, and privacy classification.

## EDF root-cause hypotheses
**R1 Information loss:** donor/sponsor/fund/purpose identifiers not present in bank statement or accessible remittance.
**R2 Ownership discontinuity:** grantmaker, processor, donor and recipient have different authority to initiate a reissue.
**R3 Temporal ambiguity:** 'sent', 'available', 'accepted', 'settled' and 'acknowledged' are different milestones.
**R4 Identity collision:** nonprofit legal name, EIN, local CRM constituent record and donor-adviser identity are distinct.
**R5 Privacy conflict:** donor anonymity and PayPal's permitted-purpose restrictions constrain information sharing and downstream marketing.
**R6 Integration heterogeneity:** electronic payment processors can supply richer structured data than mailed checks, but each export/report differs.

## Falsifiable scenarios
1. PayPal Grant Payments accepted, with transaction ID: can nonprofit import and match the sponsor grant letter automatically?
2. Fidelity ACH: does one bank description correspond to multiple grant details? How is allocation reconciled?
3. Fidelity lost check: how long from nonprofit notification to donor-approved reissue, and who sees status?
4. Vanguard anonymous grant: can recipient match amount/purpose without exposing donor identity?
5. Expired PayPal grant: is fallback payment linked to the same award without double-booking?
6. Multiple same-dollar grants from same sponsor on same day: can match avoid false positives?
7. Wrong nonprofit address or EIN: who can correct record and how is corrected provenance retained?

## Proposed industry opportunity, subject to validation
An **interoperability and reconciliation layer**, not another donor portal: ingest sponsor grant letters, processor exports, settlement records and CRM entries; preserve source IDs; generate explainable match suggestions; flag unmatched/duplicate/expired payments; track exception ownership and consent. Do not assert demand or product-market fit before recipient interviews, access to representative anonymized files, and integration cost analysis.

## Clarity conclusions
- Claim 'DAFs have no transaction IDs': **refuted** for PayPal Grant Payments.
- Claim 'electronic grant delivery solves reconciliation': **not established**.
- Claim 'faster payment means faster end-to-end grants': **invalid without separating sponsor approval from payment processing**.
- Claim 'recipient can reissue lost grant check': **not generally true**; Fidelity explicitly conditions reissue on recommending donor.
- Claim 'donor identity should always be passed through': **conflicts with anonymity and privacy restrictions**.
- Claim 'one payment equals one grant': **unsafe assumption**, test aggregation and retries.

## Next actions
- Obtain official CSV schemas for PayPal Grant Payments and Fidelity Stripe/ACH; request sample reports without personal data.
- Find published NPT and DAFgiving360 recipient exception rules.
- Collect nonprofit finance staff interviews on unmatched grants, reconciliation hours, duplicate entries and privacy handling.
- Build a mock fixture suite with split/aggregated payments, anonymous grants, expired/reissued payments and same-amount collisions.
- Compare integration effort and commercial incentives: sponsors, processors, CRM vendors, fundraisers and nonprofit finance teams.
- Test whether a standard grant reference can be carried across systems or whether a provenance-preserving crosswalk is more practical.
