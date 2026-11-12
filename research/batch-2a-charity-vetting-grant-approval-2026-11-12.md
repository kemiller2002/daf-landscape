# Batch 2A: Charity vetting and grant approval across DAF sponsors and infrastructure providers
**Research date:** 2026-11-12. **Status:** Public-policy and workflow evidence; no authenticated tests, internal rules, vendor contracts or measured exception rates.
**Research IDs:** NEW V01–V18; complements T01–T04, X02–X05, L02 and C01–C04.

## Executive synthesis
**Charity eligibility is not grant approval.** A sponsor must determine eligible legal recipient, permissible use, donor/private benefit, funding authority, liquidity and disbursement controls. Most public websites describe the policy, not the software architecture or actual human-versus-automated decision rate. Treat a 'charity database' or 'AI vetting' claim as a component, not an end-to-end control.

## Publicly documented sponsor processes
| Sponsor | Charity eligibility and purpose | Documented workflow / speed | What remains unknown |
|---|---|---|---|
| Fidelity Charitable | Verifies IRS-qualified charity, proper charitable purpose and no impermissible donor/third-party benefit; considers IRS, litigation/government records, news, donor/grantee evidence. May reject organizations facing investigations, noncharitable activity, binding obligations. | Review every recommendation, trustee policies; processing may take **10+ business days**; charity or donor contact can extend. | Automated screening vendor, risk scoring, human reviewer fraction, approval authority matrix, true median and exception rate. |
| Vanguard Charitable | Verifies tax-exempt status under IRS Rev Proc 2011-33, grant use, impermissible benefit; may research public records, watch groups, charity contacts. | Most grants reviewed and issued within **2 business days**; *new charity suggested* due diligence **2–10 business days**, followed by grant review. These are different cohorts/clocks. | Internal vendor stack, escalation thresholds, number of manual reviews, false positives. |
| DAFgiving360 | Generally approves recommendations to IRS-classified 501(c)(3) public charities complying with program policies; extra diligence for new/changed charities. | Online/Schwab app, repeat grant; checks on average mailed **7–10 business days**, USPS delivery another **7–10 business days**. | Median approvals, exact automated/human split, ACH adoption and settlement clocks. |
| National Philanthropic Trust | Reviews charity eligibility and grant purposes; international grants may use equivalency determination or expenditure responsibility. | GivingPoint online/form; usually review/process **2–5 days**; additional due diligence, holidays, closing account longer. Approved grants funded by redeeming investment pro rata. | Current internal verification tools, approval rules, exception workload. |
| American Endowment Foundation | IRS status plus grant purpose; AEF explicitly contacts adviser for grant liquidity after review. | DonorCentral recommendation → AEF diligence → advisor liquidity request → advisor transfers → AEF pays charity; **5–10 business days**. | Which stages automated; adviser delay share; data validation and approval delegation. |

### Primary sources
- Fidelity review: https://www.fidelitycharitable.org/legal/granting-due-diligence.html
- Fidelity timing: https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html
- Fidelity program guidelines: https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf
- Vanguard policies: https://www.vanguardcharitable.org/company-policies/policies-and-guidelines
- Vanguard process: https://www.vanguardcharitable.org/granting
- Vanguard new charity: https://www.vanguardcharitable.org/faq/i-cant-find-charity-id-grant-my-vanguard-charitable-account-can-i-suggest-it-be-added
- DAFgiving360 FAQ: https://www.dafgiving360.org/features/faqs
- NPT guide: https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf
- NPT diligence explanation: https://www.nptrust.org/wp-content/uploads/2019/09/What-Is-Due-Diligence-The-Things-NPT-Asks-Before-Approving-Your-Grant-2.pdf
- AEF process: https://www.aefonline.org/donors/grant-recommendation-process-donors/

## Vendor and infrastructure evidence, NOT sponsor approval authority
- **Chariot** publicly describes identity verification, gift eligibility and transaction monitoring, and organization eligibility checks, including fraud/misdirection prevention. These payment/checkout controls do **not** establish that Chariot exercises the sponsor's fiduciary grant-approval discretion. https://help.givechariot.com/onboarding/trust-and-safety/compliance
- **Ren** markets donor/adviser grant recommendations and automated updates. This does **not** disclose a verifiable production rules engine, approval automation percentage, case queues or human overrides. https://www.reninc.com/giving-vehicles/donor-advised-fund/
- **TIFIN Give, Foundation Source/Vennfi, Charityvest, Stellar/iPhi, proprietary sponsor systems**: product-level claims and sponsor-specific delegated controls require separate source and demonstration review. Do not infer architecture or vendors from logos, client associations or old DNS links.
- **Fidelity Foundation** is a separate grantmaking foundation, **not Fidelity Charitable's donor-advised grant approval process**. Its proposal reviews should not be used as a DAF benchmark.

## Normalized decision stages
1. **Request validation:** donor/adviser authority, fund identity, balance, amount, repeat vs new grant, purpose, anonymity and required fields.
2. **Recipient identity:** legal name, EIN or jurisdictional identifier, address, parent/affiliate mapping, active entity and payment destination; an EIN alone is not bank-account ownership proof.
3. **Legal eligibility:** IRS classification and status, supporting-organization rules, government and religious entity exceptions, foreign charity eligibility or intermediary.
4. **Purpose and private benefit:** donor benefit, tickets, membership, scholarships, enforceable pledges, earmarking, political activity, donor-related parties.
5. **Risk/exception investigation:** contradictory records, fraud signals, sanctions, changed status, new charity, high-risk purpose, public allegations; distinguish allegation from finding.
6. **Approval and authority:** documented sponsor policy, delegated reviewer, conflict controls, human escalation and final authorization.
7. **Funding:** redeem investments, liquidity and custody handoff, advisor authorization where applicable.
8. **Payment and reconciliation:** ACH/check/payment processor, payee verification, remittance, retries, return, settlement and nonprofit acknowledgment.

## Clarity: competing hypotheses
H1: Charity vetting is solved because IRS data exists. **False as an end-to-end claim:** status alone does not decide purpose, benefit, payee, fraud or grant settlement.
H2: Most grants are reviewed manually. **Unverified:** sponsors say review occurs, not that each grant requires human judgment.
H3: Automated approval is necessarily better. **Unproven:** measure speed and cost against false approvals, false denials and appeals.
H4: A two-day Vanguard process is universally faster than Fidelity. **Invalid comparison:** 'most reviewed and issued' versus 'may take 10+ days' and new-charity subpopulation; different denominators.
H5: Every sponsor should apply the same rules. **Incorrect:** legal requirements overlap, but sponsor policy, risk tolerance, grant types and review authority differ.
H6: Screening a charity once eliminates repeat review. **Unproven:** status, purpose, payment details and risk change over time.
H7: AI is the most important optimization. **Unproven:** better intake, clear restrictions, exception routing, prevalidated payees and integration may outperform AI.
H8: An outside vendor that vets a charity approves the grant. **Incorrect without documented delegation:** sponsor retains legal discretion.

## EDF: failure mechanisms and controls
- **Input quality:** incomplete grant purpose, mismatched EIN, bad address or recipient legal name → guided intake, validation and versioned identity.
- **Authority confusion:** donor recommendation mistaken for sponsor approval → separate immutable decision states and signatures.
- **Stale eligibility:** tax status or supporting-organization classification changes → timestamped source, review expiry and change alerts.
- **Purpose ambiguity:** tickets, pledges, donor-benefit and scholarship edge cases → explicit purpose classification and escalation.
- **External allegations:** reputational data creates false positives → source reliability, human appeal and proportional risk controls.
- **Investment/liquidity coupling:** approved grant awaits adviser transfer → independent approval, liquidation, funding and payment clocks.
- **Payment identity:** correct charity but wrong banking/payee → account verification, change controls and settlement reconciliation.
- **Vendor lock-in:** opaque approval history and missing decision provenance → portable case record and evidence export.

## Proposed evidence-gathering protocol
For each provider obtain: public policies; current donor submission form; eligibility taxonomy; grant purpose schema; review state machine; authority and delegation; exception classes; international grant treatment; sanctions/fraud controls; third-party data sources; re-screen frequency; appeals; payee validation; grant funding and payment clocks; cost per reviewed grant; median/P90/P99 processing time; percent straight-through; false positives/denials; independent assurance; data portability; subcontractors. Mark **not publicly verified** rather than speculate.

## Proposed comparative experiment (not executed)
Use 20 synthetic cases: ordinary US public charity, church without 990, school district, private operating foundation, Type III supporting organization, recently revoked charity, new unlisted charity, name/EIN mismatch, parent/local chapter, foreign NGO, US intermediary, general support, tickets/gala, enforceable pledge, nonbinding pledge, scholarship with donor selection, political purpose, alleged fraud with weak source, bank-detail change, repeat recurring grant. Test expected disposition **under each sponsor's actual policy**, not an assumed universal answer. Use synthetic data only, no live submissions or misleading impersonation. Record manual steps and reviewer questions; require qualified legal review for ambiguous cases.

## Strategic conclusion
The commercial opportunity is likely in **decision provenance, intake quality, exception handling, interoperable case data and payment reconciliation**, rather than a generic 'AI charity vetting' score. Sponsor-specific authority and policy controls are essential. This is a hypothesis for validation, not proof of vendor deficiencies.
