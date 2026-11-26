# DAF grant visibility and settlement: primary-source comparison
**Date:** 2026-11-11. **Status:** Verified published features; no authenticated platform testing, independent latency measurement, or current satisfaction survey.

## Critical correction
Earlier 2024 Reddit complaints about Vanguard grant-check visibility do **not** establish that the 2026 platform lacks grant tracking or electronic grant payments. Vanguard's official current documentation explicitly shows online grant status and PayPal grant payments. Reframe the research question as **granularity, timeliness, reliability and exception resolution** rather than existence of features.

## Published feature matrix
| Sponsor | Donor-facing | Nonprofit/settlement | Source and uncertainty |
|---|---|---|---|
| Vanguard Charitable | Manage Grants status column, searchable grant activity | PayPal Grant Payments for enrolled charities; page claims funds can arrive within minutes | https://www.vanguardcharitable.org/faq/how-do-i-check-status-my-grant ; https://www.vanguardcharitable.org/nonprofit-organizations ; 'minutes' is vendor claim for eligible payments, not end-to-end median |
| Fidelity Charitable | Grant history, processing status; grant recommendations may take **10 or more business days** | Stripe or ACH EFT, published 1–2-day delivery after processing; weekly Stripe notices versus daily ACH notices; downloadable remittance detail | https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html ; https://www.fidelitycharitable.org/nonprofits/faqs.html ; distinguish review queue from payment rails |
| DAFgiving360 (formerly Schwab Charitable) | Account grant history, status, grant letters; adviser portal includes check-clearance visibility and export | Payment method, nonprofit remittance and reconciliation detail not verified in this pass | https://www.dafgiving360.org/content/how-recordkeeping-works ; https://www.dafgiving360.org/content/how-recordkeeping-works-advisor |
| National Philanthropic Trust | GivingPoint grant activity, filters, status, Excel export; edits/cancel while recommendation submitted | NPT guide describes PayPal Grant Payments for enrolled charities, mailed check otherwise; NPT says ordinary grant review usually 2–5 days, with exceptions | https://www.nptrust.org/wp-content/uploads/2022/09/NPT-GivingPoint-at-a-glance-NPT.pdf ; https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf ; https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf |

## Measurement model: do not collapse clocks
T0 contribution initiated
T1 assets accepted and available
T2 grant recommendation submitted
T3 eligibility/diligence approved
T4 investment redemption complete and payment authorized
T5 payment issued (check/ACH/PayPal/Stripe)
T6 funds settled/received by charity
T7 recipient reconciles transaction to grant letter, donor/fund and restriction
T8 donor/recipient receives confirmation; exception resolved where relevant.

Report **T2→T3 review**, **T3→T5 disbursement**, **T5→T6 settlement**, **T6→T7 reconciliation**, and **T2→T8 end-to-end** separately. Vendor 'minutes' and '1–2 days' generally describe a narrower part of the process. Capture distribution (median, 90th percentile, exception rate), not anecdotes alone.

## Cross-platform architectural insight
Vanguard and NPT both publicly document PayPal charity payment paths, while Fidelity documents Stripe and ACH. This is an infrastructure convergence, not proof the sponsors use identical administration systems. A payment rail may standardize transfer speed while leaving recipient identity, grant purpose, donor anonymity, exception handling and ledger reconciliation unresolved.

## EDF opportunities
1. **Transaction ID across organizations:** Sponsor, processor, bank and nonprofit CRM need a durable matching key; identify whether each provider exposes one in remittance.
2. **Exception ownership:** Who is responsible for unclaimed PayPal transfers, stale checks, invalid charity addresses, returned ACH and missing grant letters?
3. **Status semantics:** Submitted, approved, issued, settled, deposited, reconciled and acknowledged are distinct; do not call 'complete' an objectively identical event across sponsors without documentation.
4. **Recipient visibility:** A polished donor portal can coexist with missing or hard-to-match nonprofit remittance data.
5. **Payment rail dependence:** Sponsor experiences may depend on nonprofit enrollment in PayPal, Stripe or ACH; assess coverage and fallback paths.
6. **Accessibility and portability:** Test keyboard/screen-reader flows and donor/adviser export formats rather than treating UI appearance as usability.

## Clarity challenges
- **Vendor capability ≠ adoption:** Availability of EFT does not establish percentage of grants delivered electronically.
- **Advertised payment speed ≠ grant approval speed:** Distinct clocks.
- **Historical complaint ≠ current defect:** Date features and corroborate current state.
- **Check cleared ≠ charity correctly attributed gift:** Settlement is not reconciliation.
- **Same payment processor ≠ same backend ledger:** Distinct system layers.

## Next evidence tasks
- Capture exact status labels and semantic definitions from official guides for each sponsor.
- Verify DAFgiving360 nonprofit remittance/payment rails and Vanguard recipient export fields.
- Obtain representative redacted remittance examples or official sample reports.
- Gather current 2025–2026 donor and recipient reports focused on exception resolution.
- Build 5-case scenario tests: routine domestic EFT; mailed check; address correction; anonymous donor; recurring grant with changed nonprofit banking details.
- Compare sponsor and investment fees separately in a second track; don't conflate payment experience with economic efficiency.

## Primary sources
https://www.vanguardcharitable.org/faq/how-do-i-check-status-my-grant
https://www.vanguardcharitable.org/nonprofit-organizations
https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html
https://www.fidelitycharitable.org/nonprofits/faqs.html
https://www.dafgiving360.org/content/how-recordkeeping-works-advisor
https://www.nptrust.org/wp-content/uploads/2022/09/NPT-GivingPoint-at-a-glance-NPT.pdf
https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf
https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf
