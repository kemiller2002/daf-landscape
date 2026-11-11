# DAF Transaction Economics: Evidence Package 001
**Date:** 2026-11-11
**Status:** First-stage synthesis from existing repository evidence; no new vendor financial statements, interviews, or transaction ledgers obtained.
**Work packages:** C01–C05, A01, D01–D02, G01–G04, H01–H06.
**Decision:** Where does economic value accrue in a DAF lifecycle, which roles control it, and what evidence is required to compare Ren, TIFIN Give, Chariot and Foundation Source without misleading denominators?

## Executive findings (bounded)
1. **The DAF economic unit is not a single firm or a single fee.** A gift changes legal ownership to a sponsor; sponsor, service vendor, custodian, investment adviser, wealth adviser and disbursement provider may each perform different roles and collect fees. The fee schedule shown to donors may not identify all payees.
2. **One named audited supplier flow is established:** Renaissance Charitable Foundation (RCF) paid Ren **$19,225,546 in FY2024**, under a related-party services arrangement described as 98% of specified individual fundholder administrative fee income. This is a sponsor-to-service-provider payment, **not** a verified Ren consolidated revenue or profit figure. See [Ren concentration](ren-contract-durability-concentration-2026-11-11.md) and [audited payment series](../data/rcf-ren-audited-admin-payments-2020-2024.csv).
3. **TIFIN Give discloses multiple revenue mechanisms** in its March 31, 2025 Form ADV brochure: service/technology fees, investment management, optional subadvisory fees, SaaS implementation/subscriptions, model-portfolio sponsorship and guest-giving transaction fees. Actual 2026 contracts, entity-level payees and net profitability are unknown. See [economics report](daf-economics-and-distribution-2026-11-11.md).
4. **Chariot's payment/disbursement function is a different economic layer** from legal sponsorship and sponsor ledger control. Its published fee direction and API documentation establish marketed/contractual functionality, not independently observed settlement accuracy, fee yield or vendor margins.
5. **Foundation Source/Vennfi/Charityvest relationships must be disaggregated by legal entity.** A charity's total operating expense cannot be assumed to be the technology provider's revenue. Acquisitions do not establish fully integrated systems or shared sponsor obligations.
6. **No defensible vendor-wide profitability ranking is currently possible.** The strongest comparison is currently evidence transparency and specific observed fee mechanisms, not financial performance or product superiority.

## Legal and economic lifecycle: states, not a marketing funnel
| Step | Economic event | Legal/control question | Potential revenue/cost | Evidence needed |
|---|---|---|---|---|
| 1 | Donor contributes cash or noncash property | Which charity accepts legal ownership and issues substantiation? | Asset acceptance, liquidation, donor onboarding | Contribution receipt, sponsor EIN, asset transfer and disposition |
| 2 | Sponsor books fund balance | Who maintains authoritative fund-level double-entry ledger? | Sponsor admin and outsourced service charges | GL entries, statements, contract, reconciliation |
| 3 | Custodian invests assets | Who is account owner, adviser and authorized trader? | Custody, investment management, underlying fund expenses | Custody statements, mandates, investment-fee invoices |
| 4 | Donor/adviser interacts with portal | Who may view, recommend, approve or alter a record? | Platform license, servicing, distribution fees | Roles, work orders, logs, price schedule |
| 5 | Donor recommends a grant | Is this a request or a legally approved obligation? | Grant vetting, nonprofit verification, staff exceptions | Timestamped recommendation, approval, rejection and review logs |
| 6 | Sponsor authorizes payment | Who can release sponsor-owned charitable assets? | Payment fee, treasury and compliance costs | Authorization matrix, payment instruction, bank debit |
| 7 | Payment settles or returns | What is finality and who bears failed payment loss? | ACH/check/wire fees, returns, recovery | Bank/processor settlement, recipient acknowledgment, return entries |
| 8 | Nonprofit uses funds | What service or outcome changes vs counterfactual? | Nonprofit administrative costs and social outputs | Recipient ledger, program outputs, causal comparator |
| 9 | Sponsor/vendor relationship ends | Who retains legal assets and portable history? | Migration, replatforming, exit costs | Full export, replay/reconciliation, legal retention obligations |

**Accounting identity:** Donor contribution, sponsor assets, vendor service payments and nonprofit grant settlement are distinct flows and stock measures. They must never be added together as independent industry output. DAF-to-DAF transfers require explicit identification to prevent false charitable-recipient distribution counts.

## Hypotheses and competing explanations
### H-ECO-01: Sponsor AUM growth is a good proxy for technology vendor revenue growth.
- **Competing explanations:** Market appreciation, account mix, donation processor growth, changed pricing tiers, contract fee shares, acquisitions and insourcing.
- **Current assessment:** Unsupported as a general rule; RCF→Ren historical fee changes cannot isolate organic volume or margin.
- **Falsifier/verification:** Matched sponsor/vendor invoices, contract prices, AUM cohorts and acquisition-adjusted revenue for 3+ years.

### H-ECO-02: More integrated vendors necessarily have lower total operating cost.
- **Competing explanations:** Integrated systems may reduce reconciliation but increase platform switching costs and bundled price opacity; modular providers may lower build costs but add integration exceptions.
- **Current assessment:** Not established.
- **Test:** Same sponsor, same workload, full implementation + ongoing labor + exception + vendor + exit cost, ideally matched deployment or controlled pilot.

### H-ECO-03: Grant-vetting AI is the strongest product opportunity.
- **Competing explanations:** Incomplete donor intake, manual reconciliation, sponsor/adviser engagement, settlement failures and account portability may be higher-value bottlenecks.
- **Current assessment:** Insufficient operational data; survey self-ratings are not unit-cost measurements.
- **Test:** Time-motion and quality measurement across all workflow stages; A/B test redesigned intake, rules-only, AI-assisted review, and baseline.

### H-ECO-04: Large sponsor service payments imply high technology margins.
- **Competing explanations:** Service vendor may bear substantial human labor, compliance, infrastructure, implementation, customer support and acquisition costs.
- **Current assessment:** Rejected as an inference; payee revenue alone does not establish margin.
- **Test:** Consolidated vendor statements, service cost allocation, contracts and labor volumes.

### H-ECO-05: A technology provider exit threatens donor charitable ownership.
- **Competing explanations:** Sponsor may retain legal ownership and custody while portal, ledger history and payment operations become inaccessible.
- **Current assessment:** Distinguish asset title risk from operational continuity risk; cannot generalize without each entity's agreements.
- **Test:** Sponsor-custodian title confirmation and end-to-end export/restore after simulated vendor loss.

## Provider comparison: verified scope vs unknowns
| Provider or grouping | Established in existing repository | Missing for like-for-like economics |
|---|---|---|
| Ren / RCF | Audited FY2024 RCF payment to Ren; public Ren/RCF template contracts; fee schedule examples | Ren consolidated revenue, actual enterprise client fee schedules, costs, gross margin, customer cohorts, current signed contract terms |
| TIFIN Give | March 2025 ADV describes fee streams, investment-adviser legal role and sponsor clients | Current sponsor contracts, realized 2026 fee receipts, costs, client cohorts, complete all-in donor expenses |
| Chariot | Public disbursement fee direction and API behavior; payments layer separate from sponsor authority | Actual take rate, sponsor and nonprofit settlement outcomes, contract SLAs, return costs, profitability |
| Foundation Source / Vennfi | Public acquisition and integration announcements, named multi-custody initiative | Consolidated economics, migration cost, payee-specific technology invoices, product-level operating performance |
| Charityvest | Sponsor-level expense information and entity-specific reports | Supplier-specific Foundation Source payments and complete sponsor/vendor financial bridge |

## Three illustrative scenarios (NOT observed vendor prices)
For a hypothetical $1m average invested balance:
- A 10 bps annual charge equals $1,000; 30 bps equals $3,000; 60 bps equals $6,000. These are *arithmetic examples*, not quoted all-in provider fees.
- An additional $20 per settled grant at 100 grants adds $2,000 annually. Actual per-grant fees are unknown here.
- A sponsor that processes 100 grants with 15 staff minutes each uses 25 hours of direct handling; at 60 minutes each it uses 100 hours. This excludes supervisory, exception, compliance and payment labor. No actual vendor labor benchmark is established.

**Decision implication:** A headline AUM-bps comparison can reverse after adviser/custody charges, grant volume, labor and migration costs. Test the *same legal and operating workload*, not provider marketing tiers.

## Clarity: conclusions and revision conditions
| Claim | Evidence posture | What we can conclude | What changes the conclusion |
|---|---|---|---|
| Ren has a material audited RCF supplier payment | Documented specific FY2024 payment | One material fee stream is observed | Restated audit or corrected payee/period |
| Ren is most profitable | Unestablished | No ranking | Comparable consolidated financials and cost allocations |
| TIFIN has more monetization mechanisms | Historical disclosure supports several mechanisms | More disclosed mechanisms, not necessarily more realized income | Current contracts and revenue breakdown |
| Chariot is cheaper than a full platform | Invalid comparison without scope | Infrastructure layer and full platform have different jobs | Comparable full-stack operating cost |
| DAF tech improves charity outcomes | Not causally established | Operational hypotheses only | Controlled time, error, grant settlement and recipient outcomes |

## EDF diagnostic: proposed failure chain
**Observed system:** Donor → sponsor acceptance → custodian/ledger → donor recommendation → sponsor approval → payment → nonprofit receipt.
**Candidate origin mechanisms:** mismatched data definitions, fragmented ownership, unobserved exceptions, incentive to retain assets, incomplete recipient data, and vendor portability constraints. These are **hypotheses**, not observed universal causes.
**Propagation:** An unreconciled custody or payment event can create misleading donor balances, erroneous grant status, bad nonprofit stewardship data, and broken historical exports.
**Control points:** authoritative legal-entity mapping; one transaction ID across stages; event timestamp and actor; independent settlement reconciliation; export and restore proof; audit of exceptions.
**Intervention ranking:** first instrument and measure the existing chain, then redesign input/exception handling, then evaluate AI only where it improves net correct completion.

## Evidence acquisition requests
**Sponsor CFO/COO:** audited sponsor statements, chart of accounts, legal sponsor/custody map, admin fee waterfall, outsourced vendor invoices, payment returns, fund-level balance reconciliation, staffing by workflow, cohort grant volumes.
**Vendor finance/operations:** executed anonymized order forms, pricing, service units, implementation and support labor, renewal cohort and termination terms, revenue recognition boundaries, supplier costs.
**Custodian/payment processor:** settlement and reconciliation contract, exception codes, latency distribution, loss and liability allocation, signed ownership and mandate.
**Nonprofit:** received vs promised dates, fees and return reasons, CRM matching, anonymous donation handling, staff minutes, program outcomes.
**Compliance/legal:** grant authorization, donor benefits, prohibited grants, audit evidence and record retention.

## First research dataset specification
One row per legal entity × product × fiscal year × economic flow, with:
`flow_id,period_start,period_end,payer_legal_entity,payee_legal_entity,payer_role,payee_role,product,flow_type,amount,currency,denominator,rate_basis,accounting_basis,source_id,source_url,source_date,observation_date,verification_status,limitations`.
A separate event table must capture grant recommendation/approval/payment/settlement/return with stable anonymized IDs, timestamps, amount, sponsor and recipient.

## Next actions
1. Reconcile the existing audited RCF→Ren payment series and RCF fundholder-fee denominator; test whether any source provides a clean fee and grant-volume bridge.
2. Extract dated TIFIN ADV disclosures into a role-by-role fee matrix and flag 2026 confirmation requests.
3. Build the same legal-entity/fee map for Foundation Source, Charityvest and Chariot; do not fill unknown cells by analogy.
4. Produce 3 identical hypothetical buyer cases: small national sponsor, community foundation, advisor-led program. Model implementation, service, investment, payment, exception and exit costs separately.
5. Obtain actual grant lifecycle events for a controlled pilot. Until then, avoid claiming faster settlement, lower operating cost or improved charitable outcomes.
6. Apply Clarity and EDF to every provider conclusion; record what could falsify it.

## Source trail
- [Existing DAF economics study](daf-economics-and-distribution-2026-11-11.md)
- [Audited RCF payments](../data/rcf-ren-audited-admin-payments-2020-2024.csv)
- [Ren contract and concentration study](ren-contract-durability-concentration-2026-11-11.md)
- [Charityvest bridge](charityvest-foundation-source-tiaa-financial-bridge-2026-11-11.md)
- [Provider technology audit](daf-technology-audit-and-provider-exits-2026-11-11.md)
- [Decision intelligence pilot](decision-intelligence-pilot-2026-11-11.md)
- [RCF FY2024 audited financial statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)
- [Ren public legal documents](https://www.reninc.com/master-service-agreements/)
