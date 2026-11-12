# DAF discretionary grant review: policy divergence, explainability and exception economics
**Research date:** 2026-11-12. **Evidence:** current primary sponsor policies plus independent reporting. **Research streams:** V03–V20, C01–C10, X02, T07.

## Executive finding
Tax eligibility is not the complete DAF grant decision. Major sponsors explicitly reserve authority to review allegations, litigation, reputational and legal concerns, donor benefit, purpose and the recipient's response to requests. The key unmet research question is not whether automated IRS lookup exists, but whether discretionary decisions are reproducible, fair across similar cases, policy-grounded, and supported by adequate evidence and appeals.

## Primary sources
- Fidelity grant review/due diligence: https://www.fidelitycharitable.org/legal/granting-due-diligence.html
- Fidelity giving account guide: https://www.fidelitycharitable.org/giving-account-guide/recommending-a-grant.html
- Fidelity nonbinding pledge FAQ: https://www.fidelitycharitable.org/faqs/all/grant-pledge.html
- Vanguard policies: https://www.vanguardcharitable.org/company-policies/policies-and-guidelines
- AEF denial reasons: https://www.aefonline.org/thought-leadership/when-grant-recommendation-not-approved/
- DAFgiving360 2024 program policy: https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf
- ProPublica 2026 investigation on inconsistent sponsor freezes: https://www.propublica.org/article/donor-advised-funds-charity-contributions
- RCF grantmaking due diligence policy: https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf

## Sponsor comparison
| Sponsor | Published decision criteria | Implication |
|---|---|---|
| Fidelity Charitable | IRS eligibility, donor benefit, nonbinding vs binding pledge, litigation/government proceedings, public records and news; board policies | IRS positive result is necessary for some categories but insufficient for automatic approval |
| Vanguard Charitable | IRS status and charitable use, donor benefit; additional news/charity watch/public record review; recurring grants reviewed anew; custom grant agreements possible | Eligibility is time-varying, not permanent; one prior approval does not bind a future grant |
| DAFgiving360 | Program policy excludes donor benefit, bifurcated gifts, binding pledges and restricted grants | Structured purpose questions can prevent avoidable exceptions |
| AEF | Public article describes several donor contacts weekly to explain declined recommendations, including event-ticket/benefit issues | Donor education and better intake can prevent costly avoidable review |
| RCF / Ren | 2023 risk-tier policy and Charity Check; >$500k officer review under dated policy; Ren markets instant approval for many grants | Distinguish charity validation, sponsor authorization, and payment |

## Critical distinction: legal eligibility vs sponsor discretion
1. **Legal disqualification**: revoked status, impermissible donor benefit, individual benefit or other prohibited purpose. Must be evidence-based, current and sponsor-specific.
2. **Incomplete documentation**: church, government, supporting org, foreign organization; route to evidence collection rather than auto-denial.
3. **Discretionary sponsor hold**: legal or reputational concern not amounting to disqualification. Requires source reliability assessment, materiality, policy authority, comparable cases, reviewer accountability, notice and reconsideration options.
4. **Operational hold**: insufficient cleared cash, unconfirmed bank details, returned payment, custodian settlement; not an eligibility denial.
5. **Administrative delay**: queue or staffing capacity; should not be presented as a policy rejection.

## Evidence from independent reporting
ProPublica reported in 2026 that major sponsors have inconsistently paused grants to certain charities amid allegations or controversy, and reported sponsor responses emphasizing independent review. This supports existence of disputed discretionary cases; it does not establish that any specific restriction was illegal or that all sponsors apply the same policy. Use independently reported cases as **adversarial test fixtures**, with the sponsor's own statement and public records linked, rather than treating allegations as facts.

## Clarity: invalid assumptions
- 'IRS-approved charity means sponsor must approve': false; sponsor has independent fiduciary/policy discretion.
- 'Every rejection is compliance-mandated': false; separate statutory prohibitions from sponsor policy and operational holds.
- 'News coverage proves wrongdoing': false; allegations require corroboration, recency and right to respond.
- 'Fast approval means complete due diligence': not established.
- 'Once approved, always approved': contradicted by Vanguard's recurring-grant review policy.
- 'AI can resolve contested allegations objectively': unproven; models may amplify source bias and opacity.

## Proposed EDF/Clarity decision record
Each grant case should capture:
- immutable grant recommendation ID and sponsor ID;
- legal recipient identity/EIN, current tax source and retrieval timestamp;
- grant purpose, donor-benefit/pledge answers and evidence;
- classification: legal block, missing evidence, discretionary hold, operational hold, administrative delay, approved;
- exact sponsor policy rule/version and delegated approval authority;
- evidence assertions, provenance, recency, contradictions, source reliability and what would falsify them;
- comparable past decisions, rationale for departures and documented human judgment;
- donor/charity notification, appeal/reconsideration route, review deadline and final outcome;
- liquidity, payment and settlement records separate from approval decision.
**This is a proposed data model, not an existing product implementation.**

## Proposed controlled evaluation
Run 24 cases: 12 standard scenarios from prior benchmark plus 12 discretionary cases with paired counterfactuals (identical IRS status, different allegation evidence quality; same purpose but different donor-benefit wording; church absent BMF; public allegation later retracted; two charities with equivalent documented risk; recurring charity status changed). Blind reviewers to charity brand where possible.
Compare (A) current unstructured intake, (B) improved intake and deterministic triage, (C) Clarity/EDF evidence ledger with human discretionary review, (D) AI-assisted evidence extraction and contradiction detection under the same human authority.
Metrics: legal false approvals (zero tolerance), unsupported holds, inconsistent paired decisions, reviewer minutes, p50/p90/p99 resolution, source traceability, appeal reversal rate, donor contacts per 1,000 recommendations, cost per exception. **No experimental results yet.**

## Technology differentiation
The defensible proposition is **decision governance infrastructure** rather than another charity lookup API: versioned sponsor policies, provenance-backed review, counterfactual consistency tests, portable audit trails, and reconciliation from decision to payment. The economic hypothesis is fewer avoidable escalations and more reliable handling of rare, expensive exceptions, not automatic approval of contested cases.

## Next investigation
1. Obtain sponsor-specific counts of recommendations, holds, denials, reversals, exceptions and staff hours; ask for definitions.
2. Research actual appeal/notification processes and legal boundaries for discretionary DAF sponsor refusals.
3. Build a public-source casebook of disputed charity holds, preserving competing perspectives and dates.
4. Quantify whether sponsor discretionary policy variation is a source of product differentiation or switching behavior.
5. Test policy-as-code plus human judgment against AI-assisted workflow with blinded matched cases.
