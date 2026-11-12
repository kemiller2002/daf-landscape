# Batch 2B: Ren, TIFIN Give, Chariot and IRS charity-verification infrastructure
**Research date:** 2026-11-12
**Workstream:** V07, V08, V09, V12, V13, V15, V17, V18
**Evidence:** Public primary product descriptions, API docs, provider contracts and IRS datasets. No vendor demos, internal systems, actual throughput, false-positive rates or signed sponsor contracts inspected.

## Executive findings
1. **Ren publicly separates grant vetting, sponsor staff approval/denial, and liquidation**. Its published administration service description explicitly lists 'Grant vetting for each grant recommendation', 'Submit vetted grant for staff approval/denial', and 'Initiate fund divestment for approved grants'. This establishes a workflow separation, NOT a manual-vetting percentage or product implementation proof.
2. **Chariot explicitly does not approve grants for DAF sponsors.** Its API and October 2026 provider agreement preserve sponsor decision authority. Chariot separately verifies nonprofit eligibility and donor identity.
3. **TIFIN Give makes an unusually direct relationship-retention proposition**, including 'retain and grow assets', family giving and advisor-managed portfolios. Its public page claims 15,000+ grant transactions and $90m granted in 2024, plus a client quote claiming grant processing reduced from weeks to days. These are vendor/client assertions, not independent timing data. Its publicly accessible 2025 Form ADV contains a concrete potential conflict: sponsored-portfolio marketing fees can incentivize recommendations.
4. **IRS charity data is not a complete grant approval engine**. Publication 78, Business Master File, automatic revocation, Form 990, determination letters have different semantics, update timing and exceptions (churches, government units, group exemptions). Negative lookup ≠ ineligible charity.

## Ren: source-grounded control and handoff map
Primary source: https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf
- DAF administration services include contribution processing, grant vetting, approval submission, divestment initiation, disbursement monitoring, grant checks/letters and accounting.
- Its product description explicitly sequences vetting → **staff approval/denial** → divestment for approved grants. Which legal entity's staff and delegated decision matrix can vary by sponsor; obtain agreements before assigning roles.
- DFX/DonorFirstX described as proprietary, configurable donor/staff interface, not evidence of a specific risk model or automated rules engine.
- Public Ren/LPL onboarding https://www.reninc.com/lpl-rcf-daf/ says donor/adviser uploads proof of funding (transaction statement/screenshot) and Ren performs final review before 'grant ready'; after a grant passes vetting, an invoice appears with instructions for funding grant. These are documented **funding handoffs**, not proof of inefficiency or average time.
- Public Ameriprise guide https://www.reninc.com/ampf-rcf-daf/ describes a nightly data feed to Ren, separate donor portal balance, annual managed account review with RCF, proof-of-funding by email and staff review. Shows sponsor/custodian reconciliation dependencies; do not infer all Ren programs use the same method.
- RCF itself states it has grant approval responsibility: https://www.reninc.com/rcf-giving-fund/
- Missing: actual software decision rules, screening suppliers, exception queue, percent straight-through, delegated signers, reviewer minutes, approval time distribution and customer-by-customer configuration.

## TIFIN Give: marketing, evidence and disclosed incentives
Primary product: https://tifin.com/product/give/
- White-label, digital, multi-custody DAF platform, pooled and adviser-managed investments; explicitly pitches retention of charitable dollars and multigenerational client relationships.
- Claims $90m granted and >15,000 grant transactions during 2024. The numbers do not establish independent unique grants, approval rate, processing time, or current share.
- AssetMark testimonial claims automated account opening and grantmaking times cut from weeks to days; a single testimonial is not a controlled comparative benchmark.
- Conversational AI can support cause exploration and donor action, but no public evidence it independently decides legal grant eligibility or replaces sponsor final authority.
- 2025 Form ADV: https://tifin.com/wp-content/uploads/TIFIN-Give-Part-2A-of-Form-ADV-Brochure-2025.pdf
  - Describes DAF-based investment recommendations, custodian statements and that investment advisory personnel do not actively monitor client positions directly.
  - Says third-party sponsored portfolios may pay TIFIN marketing/sponsorship fees to improve visibility; identifies a conflict of interest.
  - **Do not generalize** this conflict to every DAF grant or assert improper conduct; the disclosure concerns sponsored investment portfolio recommendations.
- Missing: sponsor-specific grant review architecture, automated decision share, staff authority, vetting data sources, measured turnaround and integration cost.

## Chariot: hard approval boundary, data controls and exceptional charities
Primary docs: https://docs.givechariot.com/guides/dafpay/donor-accounts/overview
Provider addendum: https://www.givechariot.com/dafpay-provider-addendum
Compliance: https://help.givechariot.com/onboarding/trust-and-safety/compliance
Unlisted charities: https://help.givechariot.com/onboarding/unlisted-organizations
- Donor Account must be approved via authorization token before its grant requests can be processed; donor-account approval is **not grant approval**.
- Sponsor controls which donor grant requests it approves/rejects; contract explicitly reserves reviewing, approving and executing to sponsor.
- Chariot says its compliance includes identity verification, gift eligibility and transaction monitoring, with proprietary database based on six primary sources (public page lists IRS BMF, Form 990, Pub 78, OFAC; do not invent remaining two).
- Its transaction monitoring statement applies to **Chariot Deposit Accounts**, not DAFpay grant requests. Do not conflate.
- Unlisted charity can manually onboard pending additional due diligence.
- Religious organizations without IRS database listing can submit EIN documents, organizational records and review against IRS 14-point church criteria.
- Chariot's status signals are *input evidence* for sponsor policy, not legal final approval.
- GoFundMe Pro Oct 2026 DAFpay beta integration describes a DAFpay grant as an offline transaction in its nonprofit fundraising system; useful example of payment/CRM semantic mismatch: https://prosupport.gofundme.com/hc/en-us/articles/49765186392731-Accept-donor-advised-fund-gifts-with-DAFpay

## IRS data: source taxonomy and update constraints
Primary: https://www.irs.gov/charities-non-profits/tax-exempt-organization-search
Bulk: https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads
- Pub 78: listed organizations eligible for deductible contributions; generally legal names, not DBA aliases.
- Exempt Organization BMF: cumulative classification, filing requirements, status fields; not a definitive grant-purpose approval.
- Auto-revocation list: entities automatically revoked for three consecutive years missing required filing; must also check reinstatement.
- Form 990/990-N: financial/filing records; absence is not proof of ineligibility.
- Determination letters: status and dates, not present payment account identity.
- IRS bulk data described as updated monthly; sources have different as-of dates. No assumption that every DAF vendor uses the same refresh.
- Churches and some other eligible entities may not appear in Pub 78; manual alternate verification needed.
- OFAC sanctions and bank account identity are distinct from tax-exempt status.

## Comparison by decision layer
| Layer | Ren | TIFIN Give | Chariot | IRS |
|---|---|---|---|---|
| Charity status lookup | Vetting service claimed; source details unknown | Not publicly verified | IRS-based eligibility + exceptions documented | Primary public source |
| Grant purpose/private benefit | Sponsor-specific controls not disclosed | Sponsor-specific controls not disclosed | Gift eligibility screening; sponsor remains final authority | Not decided by charity status |
| Donor identity/authentication | Portal access, account funding review documented | Donor/adviser experience marketed | Authorization-token and donor-account approval API documented | None |
| Legal grant approval | Vetting submitted for staff approval/denial | Not publicly verified; sponsor retains legal control | Explicitly sponsor decision | None |
| Investment liquidation | Ren initiates for approved grants | Multi-custody/adviser-managed options | Not established as universal sponsor liquidation system | None |
| Payment and reconciliation | Grant checks, letters, account monitoring described | Grants processed, detailed rails unknown | Deposit/disbursement/payment integration | None |
| Evidence of actual manual workload | No | No | No | Not applicable |

## Clarity hypotheses and tests
- **H1:** 'Charity vetting is solved.' Partial truth: IRS eligibility data widely available; false if taken to mean purpose, donor benefit, fraud, approval and settlement are solved.
- **H2:** 'Ren automates all approvals.' Unsupported; public service description distinguishes vetting from staff approval/denial. This does not prove *all* grants are manually reviewed.
- **H3:** 'Chariot approves grants.' Contradicted by its provider agreement and docs.
- **H4:** 'TIFIN's claimed 15k transactions are 15k unique approved grants.' Unsupported.
- **H5:** 'A missing IRS listing is an ineligible charity.' Contradicted by IRS exceptions and Chariot's documented alternative religious verification.
- **H6:** 'AI screening has high ROI.' Unsupported until compared with structured intake, rules, sponsor authority and exception handling on common cases.
- **H7:** 'TIFIN's sponsored portfolio marketing fees make its grants biased.' Unsupported inference; disclosure relates to investment portfolio recommendations, not proven grant outcomes.

## EDF bottleneck hypothesis
Failure-prone handoffs: donor form→charity legal identity→status snapshot→purpose/benefit→sponsor reviewer→investment liquidation→bank/check payee→recipient CRM. Operational improvements may come from (a) structured intake and sponsor policy templates, (b) persistent evidence and policy versions, (c) exception routing with accountable owner, (d) prevalidated payee, (e) separately measured approval, funding and settlement clocks. AI should be tested as an optional assistive layer, not assumed to replace authorization.

## Next executable research tests
1. Download Ren's full product descriptions and extract DFX staff workflow fields and API claims, comparing current Ren product pages.
2. Retrieve TIFIN's current ADV and identify precise legal entities and sponsor relationships; verify 2024 metrics and 2026 applicability.
3. Trace Chariot's full grant request states and webhooks, rejection reasons, retry/idempotency and audit logging from versioned docs.
4. Build a source-by-source charity status reconciliation test using synthetic examples, including churches, revoked/reinstated entities, fiscal sponsorship and parent/subordinate mismatches.
5. Collect grant-review forms and documented policies for Fidelity, Vanguard, NPT, DAFgiving360, AEF and Ren/RCF, run the same 20-case matrix.
6. Request anonymized sponsor operational distributions (median/P90, straight-through, escalation, false approvals, returns, reviewer minutes) before any performance ranking.
7. Evaluate an intake-only redesign against rules engine and AI assistance on held-out synthetic cases with measured labor/error, not claims.
