# DAF grant exceptions: unit economics, market scale, and evidence gaps
**Date:** 2026-11-12. **Research streams:** M03–M09, V11–V20, C04–C10. **Status:** documented grant-volume baselines plus explicitly hypothetical sensitivity model. No measured exception cost or rate available.

## Finding
The large-scale DAF opportunity is not proven by a claim that '98% of charities pass' or 'half of grants approved instantly.' These are different denominators. **We do not have credible published per-grant exception frequencies, reviewer minutes, blended labor cost, appeal rates or error costs.** Model only scenarios until actual operational data is acquired.

## Source baselines
- Fidelity Charitable **2026 Giving Report** reports **3.0 million grants in calendar 2025**, $18.3 billion granted. https://www.fidelitycharitable.org/insights/2026-giving-report.html
- DAFgiving360 **January 27, 2026** report reports **1.5 million grants in calendar 2025**, $9.9 billion granted. https://www.dafgiving360.org/press-release/2025-results
- DAFgiving360 **FY2025** report reports **1.4 million grants**, 38% scheduled as recurring, and 70%+ unrestricted. Different fiscal-year window from CY2025. https://www.dafgiving360.org/press-release/fiscal-year-2025-results
- Fidelity's 2025 Giving Report (for 2024) records **2,664,446** grants; historical baseline only. https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf
- Ren/RCF historical charity verification coverage and Ren 'instant approval' claims are **not exception rates**. See research/ren-instant-grant-approval-rcf-policy-clarity-audit-2026-11-12.md.

## A transparent annual model
Let N = grant recommendations; e = true substantive exception incidence; m = manual review minutes per exception; c = fully loaded reviewer hourly cost; s = share of exception review time actually saved by a change; f = fixed annual platform/implementation/maintenance costs; a = added annual audit/security/quality costs.
Annual **gross reviewer labor value** = N × e × (m/60) × c × s.
Annual **net labor value** = gross − f − a. This excludes donor service contacts, wrong decisions, payment exceptions and legal/compliance losses unless independently measured.
Example only: N=1,000,000, e=3%, m=25 min, c=$65/hr, s=40% → **$325,000 gross**. If f+a=$250k, **$75k net**. These are hypothetical assumptions, not DAF industry averages.

### Sensitivity grid, gross annual labor savings for 1m grants
Assume c=$65/hr, 40% review-time savings.
| True exception rate | 10 min per case | 25 min | 60 min |
|---|---:|---:|---:|
| 0.5% | $21,667 | $54,167 | $130,000 |
| 2% | $86,667 | $216,667 | $520,000 |
| 5% | $216,667 | $541,667 | $1,300,000 |
| 10% | $433,333 | $1,083,333 | $2,600,000 |

**Scaling illustration only:** At Fidelity's reported 3m grants, multiply the relevant 1m-grant gross savings by three **if the same assumed exception rates and costs applied**. We have no evidence they do.

### Compare prevention with investigation
Scenario A: Better intake prevents 20% of avoidable exceptions (e.g. pledge, gala benefit, incomplete church documentation) and saves 15 minutes of reviewer time on each prevented case.
Scenario B: Clarity/EDF evidence packet reduces 40% of review time on remaining substantive cases but incurs evidence ingestion/QA costs.
Scenario C: AI extraction reduces 50% of document handling time on remaining cases but needs human verification and may add false-positive holds.
**These effects are not additive** without measuring overlap, error rates, case-mix shifts and new workflow costs.

## Operational taxonomy and denominators
- N0: submitted grant recommendations, including duplicates and withdrawals.
- N1: unique eligible recommendations received with complete intake.
- N2: automated legal-eligibility checks completed.
- N3: sponsor-authorized recommendations (automated delegated vs human).
- N4: manual **substantive** reviews: eligibility ambiguity, donor benefit, sanctions match, allegations, foreign grants.
- N5: manual **operational** interventions: insufficient settled cash, custodian order, ACH return, incorrect bank, reconciliation.
- N6: donor follow-up: missing info, clarification, repeated submission.
- N7: final payments settled; N8: reopened/appealed/reversed.
Track cohorts, overlaps, case age and outcome. Never add overlapping N4+N5+N6 to derive an exception rate.

## Economic priority test
The greatest benefit may come from:
1. **Preventing** avoidable cases at the point of entry through contextual questions and recipient identity validation.
2. **Triage** by risk and source confidence with sponsor-specific deterministic rules.
3. **Decision packets** for rare discretionary cases: evidence lineage, contradictions, comparable precedent and policy version.
4. **Postapproval operations**: cash availability, disbursement, ACH return, reconciled audit trail.
5. **AI extraction** only for complex, unstructured documents where blinded test shows net benefit after verification.

## Research design: 90-day operational study
Recruit 3–5 sponsors or administrators with diverse scale, including one Ren/iPhi/DFX customer and one independent sponsor. Obtain de-identified case event exports under NDA. For every recommendation: intake completeness, tax-status evidence version, reviewer touches/minutes, approval authority, elapsed time, exception reason, donor follow-ups, liquidation/payment events, reversals and final status. Sample all unusual cases and a stratified sample of routine cases; preserve denominator to avoid selection bias. Record labor fully loaded costs and vendor fees separately. Analyze median, p90, p99, total cost per grant and per exception, by risk class and platform.
Compare **baseline**, **structured intake**, **rules + policy versioning**, **Clarity/EDF review packet**, and **AI-assisted review**, randomized where permitted. Safety: no live automatic authorizations or payment instructions from experimental models. Use blinded replay and human signoff.
Success: statistically meaningful improvement in reviewer time with no increase in false approvals, unsupported holds, reversal or donor follow-up rates.

## Evidence-grade conclusions
**Observed:** very large annual grant volumes; recurring and unrestricted grants represent large shares at DAFgiving360; different sponsors have discretionary policies.
**Inferred:** economies may favor cheap prevention and structured intake before complex AI.
**Unknown:** exception frequency, reviewer effort, true cost, degree of automation, staffing mix, model error rate, vendor implementation cost and willingness to pay.
**Rejected:** using RCF's 98% Charity Check adequacy figure as a 2% manual exception rate; treating Ren's instant approval percentage as human review percentage.

## Next actions
1. Request sponsor operational datasets with common event schema and cost allocation.
2. Find published charity-grant denial/hold rates from IRS 990 narrative, board minutes, independent audits or regulatory studies, noting survivorship and selection bias.
3. Investigate recurring-grant exception treatment and impact of unrestricted purpose on screening.
4. Build a spreadsheet calculator with editable inputs only after agreeing cost accounting definitions.
5. Evaluate exception costs beyond labor: delayed charity receipt, donor churn, operational loss, wrongful denial and governance exposure.
