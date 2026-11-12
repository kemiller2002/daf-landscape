# Ren instant grant approval: evidence audit and Clarity benchmark
**Date:** 2026-11-12. **Scope:** Ren claims, RCF sponsor policy, process definitions, counterfactual AI value. **Status:** documentary research, no production access or empirical benchmark.

## Executive conclusion
Ren currently markets **'over half' of grants approved instantaneously** and charity vetting reused across its platform. Its sponsor RCF's **March 2023** public Grantmaking Due Diligence Policy supplies a detailed risk-tiered basis for screening, including GuideStar Charity Check as sufficient risk mitigation for **more than 98% of RCF's historical grants** (not a current instant-approval rate). This is compatible with rules-based straight-through processing for routine grants, but does not prove the current architecture, approval authority delegation or actual automation percentage.

## Primary sources
- Ren giving platform: https://www.reninc.com/giving-platform/
- Ren 'About Ren': https://www.reninc.com/resources/about-ren-piece/
- Ren FAQs: https://www.reninc.com/faqs/
- RCF Grantmaking Due Diligence Policy, March 2023 revision: https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf
- RCF sponsor FAQ: https://renaissancecharitable.org/faqs/
- Ren DAF service descriptions: https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf
- Historical RCF 2023 Pershing year-end guidance: https://www.reninc.com/wp-content/uploads/2023/10/2023-Pershing-Year-End-Timeline.pdf

## Three separate metrics
1. **Charity validation coverage**: RCF 2023 policy says GuideStar Charity Check adequate for more than 98% of historical grants. Denominator: grants for which risk mitigation is adequate, not percent approved automatically. Charity verification does not establish purpose, donor benefit, liquidity or payment readiness.
2. **Grant approval latency**: Ren 2026 site states 'over half' of grants instantaneously approved, but does not define timestamp start/end, policy cohort, reviewer role, exclusions or denominator. A search result transiently showed '80%' while a fresh open showed 'over half'; record **current directly opened page** rather than treating search snippet as reliable time series.
3. **Grant payment latency**: Ren FAQ says most grants processed/sent within 2–3 business days; RCF FAQ says approve/send many within 2–3 business days after a complete recommendation is received and reviewed. This is not inconsistent with an instantaneous *approval* event because investment liquidation, bank settlement and recipient delivery are later steps.

## RCF risk policy, March 2023
- Foundation asserts full authority and control over every DAF grant; grant checks assess recipient identity, amount and charitable purpose.
- Uses GuideStar Charity Check for IRS BMF, Pub 78, supporting organization status and OFAC checks.
- **Grant over $500,000:** an RCF officer personally reviews grant due-diligence paperwork and authorizes.
- Risk segments: domestic IRS-registered, domestic nonregistered (including churches and governmental units), US Friends-of, US conduit, foreign organizations not IRS-registered.
- Churches and governmental units may be qualified despite not appearing in GuideStar; policy calls for supplemental documentation rather than blanket denial.
- International direct grants have significant additional requirements; policy states minimum $50k and expected ~$4k cost in typical efficient case. These are **2023 policy terms**, not confirmed current pricing.
- Grant purpose restrictions: donor benefit, dues, tuition, auction goods, political campaigns, lobbying; pledge handling is conditional and nuanced.
- 'More than 98%' historical reliance on Charity Check is **not** a measure of percent automated or risk-free.
- Published policy's date matters: may have been amended since March 2023; do not assert current policy unchanged.

## Reconstructed decision graph (proposed, not verified Ren implementation)
1. Intake required fields and donor certification (recipient, amount, purpose, pledge, donor benefit, anonymous/recurring).
2. Normalize charity identity; verify current status with dated source and watchlists.
3. Check sponsor eligibility and recipient class; send missing church/government documentation to exceptions.
4. Check donor benefit, prohibited purpose, pledge and conflict triggers.
5. Apply amount threshold; officer review if >$500k under 2023 policy.
6. Check sufficient settled funds and investment liquidation constraints.
7. Sponsor authorizes via defined delegation and logged identity, policy version, evidence snapshot.
8. Send disbursement instructions; reconcile ACH/check settlement and exception/return events.
Only steps 1–5 are relevant to eligibility; 6–8 govern funding/payment and may consume days.

## Clarity evaluation of marketing
| Claim | Evidence | Unsupported extrapolation |
|---|---|---|
| 'Instant approval' | Ren vendor assertion, 'over half' | All programs, every grant, no sponsor review, funds paid instantly |
| 'Automatic charity vetting' | Ren vendor assertion + RCF 2023 policy on GuideStar | Every grant purpose or exception automatically approved |
| '98% covered by Charity Check' | RCF March 2023 policy | 98% auto-approval or zero false negatives |
| '2–3 business days' | Ren/RCF FAQs | End-to-end grant approval is slow; may include settlement |
| 'One validated charity trusted across platform' | Ren public claim | One legal sponsor's approval automatically binds every other sponsor |
| 'Instant = AI' | No evidence | AI is required; deterministic rules can support routine decisions |

## Proposed comparative benchmark
**A: better intake** (clear structured form, donor-benefit questions, recipient normalization, no auto authorization).
**B: deterministic policy** (risk tiers, source snapshots, sponsor-specific delegation, exceptions).
**C: AI-assisted** (LLM extracts facts, summarizes unusual cases, suggests review questions, never independently overrides sponsor authority).
Cases: G01 repeat domestic IRS public charity; G02 revoked; G03 church absent IRS; G04 government agency; G05 >$500k; G06 gala/benefit; G07 pledge; G08 foreign charity; G09 Friends-of/conduit; G10 insufficient cash; G11 returned ACH; G12 sanctions near match.
Measure: unauthorized approvals (hard zero), exception detection, false rejection, reviewer minutes, full audit reconstruction, approval latency p50/p90/p99, payment latency, source freshness and cost/grant. Cohort denominators and dates mandatory.
**No benchmark has been run.**

## Competitive implication
A new platform is unlikely to differentiate solely on 'instant charity verification'. A stronger proposition is sponsor-specific **policy-as-code + reproducible grant decisions + independently exportable evidence + reconciliation**, with AI restricted to exception investigation and document extraction where demonstrated useful. Test this rather than presuming superiority.

## Next evidence requests
1. Obtain Ren's definition of instant approval and sample grant approval log with policy delegation, timestamps, cohort denominator.
2. Confirm RCF's current (2026) policy version and whether >$500k officer review still applies.
3. Ask whether validated charity status is shared across legal sponsors and how sponsor-specific eligibility is applied.
4. Request independent measurement of instant-approval claims, exception rates, reversal rates, payment settlement times and false-positive vetting.
5. Compare rival DAF vendors on same cases using public workflows and authorized demonstrations.
