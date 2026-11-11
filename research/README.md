# DAF security and technology assurance research

**Baseline:** November 11, 2026. This is a dedicated extension to the general DAF landscape research foundation.

## Research
- [SOC 2 public-assurance assessment](soc2-assessment-2026-11-11.md)
- [Capability comparison](capabilities-2026-11-11.md)
- [Technology and control map](technology-control-map.md)
- [Prioritized diligence plan](next-steps.md)
- [Assurance-specific methodology](../docs/assurance-methodology.md)
- [Assurance matrix](../data/assurance.csv), [capability data](../data/capabilities.csv), [assurance-specific sources](../data/assurance-sources.csv)

The general market research data and source taxonomy are maintained in a separate foundational workstream. This package uses its own S01-S22 IDs in `data/assurance-sources.csv`; these IDs **are not** source IDs in any other research source register.


## Competitive platform investigation (2026-11-11)

- [Ren vs. TIFIN Give, with Chariot as infrastructure](ren-tifin-chariot-deep-dive-2026-11-11.md): verified organizational roles, capabilities, Chariot's confirmed TIFIN integration, operating-model tradeoffs and falsifiable competitive hypotheses.
- [Buyer-neutral evaluation protocol](platform-evaluation-protocol.md): sponsor, wealth institution and payments test scenarios; consistent timing definitions, control test fixtures and procurement questions.
- [Capability comparison dataset](../data/platform-comparison-2026-11-11.csv): 25 evidence-classified comparison dimensions, no invented winner scores.
- [Comparison source register](../data/platform-deep-dive-sources.csv): separate C001–C028 references with publication dates and limitations.

The clearest documented distinction is **Ren's integrated fund-accounting/administration and payments offering vs. TIFIN Give's advisor-oriented stack with GiveClear as sponsor and Chariot as an actual disbursements partner**. This is a public-source structural observation, not an audited performance comparison. Actual implementation and security maturity remain unverified.


## Donor tax-fit segmentation (2026)

- [DAF donor tax personas, 2026](donor-tax-personas-2026.md): 14 candidate and exclusion personas, 2026 income-tax rule changes, eligibility decision tree and an illustrative three-year bunching calculation that includes the new direct-giving nonitemizer deduction.
- [Persona dataset](../data/donor-tax-personas-2026.csv) and [tax source register](../data/donor-tax-sources-2026.csv): machine-readable targeting triggers, prerequisites, counterexamples and 12 cited sources.

**Critical 2026 distinction:** A cash donation to a DAF is **not** eligible for the new $1,000/$2,000 nonitemizer deduction, while a cash gift directly to an eligible charity may qualify. Do not imply DAFs are uniformly tax-efficient for every donor.


## Proactive donor tax-opportunity research (2026)

- [Ren vs TIFIN Give donor identification, planning, and execution](tax-opportunity-lifecycle-2026-11-11.md): a source-based life-cycle analysis that distinguishes Ren's public Benefit Estimator from TIFIN's announced Tax Intelligence and Single-Charity Funds, and correctly places Chariot downstream.
- [Tax opportunity comparison matrix](../data/tax-opportunity-capability-matrix-2026.csv): 22 lifecycle dimensions, classified by what public evidence actually establishes.
- [Synthetic evaluation protocol](tax-opportunity-evaluation-protocol-2026.md) and [18 cases](../data/tax-opportunity-test-cases-2026.csv): adversarial donor examples with **all vendor test outcomes unexecuted**, intended for independent tax-professional review and authorized demos.
- [Public source register](../data/tax-opportunity-sources-2026.csv): 22 primary references, with publication dates and scope limitations.

**Summary:** TIFIN Give announced portfolio-level Tax Intelligence in September 2025; Ren has a public DAF Benefit Estimator and documented advisor tax-planning guidance. This is an **evidence coverage difference**, not verified relative prediction accuracy. The required product test must compare DAF and direct giving, include 2026 tax rule changes, and sometimes recommend **no DAF**.


## Actual evaluation status (2026-11-11)

- [Execution report: what was checked, calculated, and blocked](vendor-test-execution-2026-11-11.md). **No live Ren, TIFIN Give or Chariot vendor test was executed**; no vendor may be scored as pass/fail.
- [Independent reference-case results](../data/reference-check-results-2026-11-11.csv): five synthetic arithmetic sanity checks executed, 13 rule or escalation expectations documented, not CPA-validated.
- [Per-case vendor access review](../data/vendor-test-access-2026-11-11.csv): 36 Ren/TIFIN cases and one Chariot downstream case, all live tests not executed, with public UI input gaps recorded.
- [Prepared vendor access requests](vendor-access-request-2026.md): ready for approved outreach; not sent.

**Fixture correction:** X03 had inconsistent high-rate/AGI assumptions. Corrected to 2026 single filing, $900,000 AGI, assumed $800,000 taxable income; the 0.5%-AGI floor is $4,500 and a $20,000 eligible cash gift leaves $15,500 before other restrictions. Original 18-case evaluation now uses that corrected fixture.


## Economics, fees, and distribution control (2026-11-11)

- [DAF platform fee waterfall and business-model investigation](daf-economics-and-distribution-2026-11-11.md): TIFIN Give's **2025** Form ADV fee and conflict disclosures, Ren/RCF fee models, sponsor/technology/payment separation, distribution economics and unresolved 2026 revenue questions.
- [16 reproducible sponsor administration fee scenarios](../data/daf-admin-fee-scenarios-2026.csv): tier-by-tier estimates for balances from $10k to $2m, annual administration fees **only**. Includes Ren Direct/RCF advisor-managed, RCF donor-directed, Fidelity Charitable and DAFgiving360's published tiers; third-party fees excluded and unknown minima identified.
- [20 economics evidence gaps](../data/daf-economics-evidence-gaps-2026.csv): prioritized contract questions including custody rights, SaaS, model sponsorship, adviser fees, transactions and exit costs.
- [20 public sources](../data/daf-economics-sources-2026.csv): SEC registration, TIFIN's dated Form ADV, charity fee schedules, GiveClear self-reports and Chariot API documents.

**Crucial warning:** TIFIN's 2025 adviser AUM, GiveClear's 2025 sponsoring-charity assets, Ren's platform-serviced asset claim and an investor's donor account balance are different economic units. Do **not** rank platform economics or derive market share by dividing incomparable amounts.


## Revenue quality, renewal and exit diligence (2026-11-11)

- [Revenue quality and switching assessment](revenue-retention-and-switching-2026-11-11.md): investor-grade distinction among sponsor ownership, payer contracts, adviser relationships, fixed/asset-linked/transaction revenue, and evidence of migration.
- [Public contract and source register](../data/revenue-retention-sources-2026.csv): 22 verifiable source entries with scope and caveats.
- [Switching-cost control matrix](../data/switching-cost-control-matrix-2026.csv): 30 contract and operational boundaries with explicit unexecuted tests.
- [Migration acceptance runbook](migration-runbook-2026.md): 20 synthetic exit, platform-swap, payment-cutover and data portability cases; no vendor tests performed.
- [Recurring revenue sensitivity](../data/revenue-cohort-sensitivity-2026.csv) and [asset-linked/DAFpay fee scenarios](../data/revenue-stream-sensitivity-2026.csv): purely synthetic calculations; do not mistake for company ARR, churn or profit.

**New evidence:** AEF's actual portal migration left donors with only two years of directly accessible account history in the new Ren platform. Chariot's October 2026 nonprofit terms specify a default 2.9% DAFpay donation fee in the absence of other fundraising-platform agreements, with subscription alternatives; that is **not** its separate grantmaker Disbursements charge. Current signed institution-level terms and revenue cohorts are unverified.

**Source correction:** AEF's July 2025 press release genuinely claimed Type II for philanthropic Ren; April 2026 said Type I. Earlier Type I-only summaries were incomplete and have been corrected in the assurance register and comparative files.


## Audited financial evidence: direct RCF → Ren payments (2020–2024)

- [Audited Ren counterparty fee and customer-cohort investigation](audited-revenue-and-client-cohorts-2026-11-11.md): five years of actual Renaissance Charitable Foundation payments to Ren, vendor-side accounting limitations, GiveClear/TIFIN IRS comparison, Chariot pricing, and institutional diligence asks.
- [Five-year RCF–Ren payment history](../data/rcf-ren-audited-admin-payments-2020-2024.csv): $7.51m disclosed payment in 2020 rising to $19.23m in 2024; 95% fundholder-fee basis in 2020–22, 98% in 2023–24; linked 990 year-end DAF account counts.
- [Public audited/IRS source register](../data/audited-contract-evidence-sources-2026.csv): four audited RCF financial reports plus Form 990, sponsor and published pricing sources.
- [Contract/cohort evidence classification](../data/contract-and-cohort-evidence-2026.csv): known actual service fee payments vs unknown company ARR, retention, margins, contract term, and pricing on other sponsors.

**Correction to prior economics analysis:** RCF's independent audits disclose **$19,225,546 paid to Ren in FY2024** under a related-party administration agreement. This is stronger than a mere retail fee schedule, but **not** total Ren corporate revenue, software ARR, gross margin or cohort NRR. Other vendors do not have a comparable observed counterparty-paid five-year series in this scoped public review. No private financial records were used.


## Ren service-contract and counterparty concentration follow-up (2026-11-11)

- [Ren contract durability and concentration investigation](ren-contract-durability-concentration-2026-11-11.md): public June 2023 standard Ren/RCF agreements, work-order renewals, termination and ownership clauses; 2023 Bain/Valeas and 2025 Great Hill financing; exact limitations on estimating Ren's dependence on RCF.
- [Public standard agreement/contract controls](../data/ren-public-contract-clauses-2026.csv): 20 documented or unresolved items with explicit contractual-party distinctions. The public Ren provider template **is not** the RCF-to-Ren related-party agreement observed in audited statements.
- [Conditional concentration and servicing cost sensitivities](../data/ren-rcf-dependence-sensitivity-2026.csv): 17 algebraic *what-if* cases grounded on one observed $19,225,546 FY2024 RCF payment. No actual Ren total company revenue, RCF concentration percentage, EBITDA or unit costs are claimed.
- [Public MSA/financing source register](../data/ren-contract-concentration-sources-2026.csv): 14 source records, including audited RCF fee transfers, unsigned published templates, equity investment announcements and the FY2024 latest listed sponsor audit.

**Highest-value next document:** the actual RCF-to-Ren signed related-party services agreement plus Ren's consolidated FY2024–2025 statements and customer-cohort bridges. The current publicly posted **Renaissance Acquisition Company MSA** does identify default one-year renewals/60-day notice, certain through-quarter charges, materials return, limited licenses and liability allocation, but cannot prove that AEF or RCF signed those exact terms.


## Expanded market universe (2026-11-11)

- [Expanded DAF ecosystem research](expanded-daf-ecosystem-2026-11-11.md): moves beyond Ren/TIFIN/Chariot to Foundation Source/Charityvest, NPT private-label, GivingTech DAFtech, major national sponsors, digital-first platforms, workplace processors and enabling infrastructure.
- [25-company and organization market map](../data/expanded-daf-market-map-2026.csv): legal sponsorship, technology/administration roles, customer types, public evidence, current report availability and next diligence priorities.
- [21 sponsor/technology/acquisition relationships](../data/expanded-ecosystem-relationships-2026.csv): identify common infrastructure rather than treating legal sponsors and vendors as independent tech rivals.
- [9 dated sponsor / cross-product activity benchmarks](../data/expanded-sponsor-activity-benchmarks-2026.csv): preserve actual calendar/fiscal periods, units, legal entities and self-reported versus audited limitations.
- [54-source register](../data/expanded-ecosystem-sources-2026.csv) and [expanded provider diligence protocol](expanded-provider-diligence-2026.md): priority verification for Foundation Source/Charityvest, NPT institutional white label, GivingTech DAFtech, and other market categories.

**Highest-value finding:** Foundation Source acquired **Vennfi** (Charityvest's technology) in 2024 and TIFIN's **Giving Place** product in 2025. Charityvest remains an **independent charitable DAF sponsor**, Foundation Source is a for-profit technology/admin provider, and TIFIN continues operating its separate advisor-led DAF platform. Their 2025 reported charitable assets and grant flows are not vendor ARR. Foundation Source's 2025 announced BridgeFT multi-custody integration warrants detailed data-freshness tests before assessing competitive tax-lot features.


## Charityvest / Foundation Source / TIAA financial bridge (2026-11-11)

- [Charityvest / Vennfi / Foundation Source financial evidence and TIAA wealth distribution](charityvest-foundation-source-tiaa-financial-bridge-2026-11-11.md): 2019 draft-stamped auditor description of Vennfi percent-based services agreement, 2022 Form 990 delegated provider responsibilities, FY2024 IRS expense/grant comparison and 2026 TIAA advisor conflicts.
- [12-row provider payment and expense bridge](../data/charityvest-provider-payment-bridge-2026.csv): unknown named provider payments preserved as unknown; sponsor 2024 **$811,940 expenses other than grants** explicitly labelled a calculated aggregate, *not a Foundation Source fee*.
- [16-source evidence register](../data/charityvest-financial-and-tiaa-sources-2026.csv): original Charityvest IRS filings, TIAA March 2026 Form ADV, May 2026 Reg BI, September 2026 launch and Charityvest adviser pricing.

**Material channel addition:** **TIAA Wealth Management's September 28, 2026 DAF** is sponsored by independent Charityvest, powered by Foundation Source technology and advised by a TIAA affiliate. TIAA's public documents explicitly disclose asset-linked adviser fees and proprietary-fund incentives. The same sources **do not show actual charitable account adoption, dollar contract fees paid to Foundation Source, or misconduct**. The new 24-entity expanded market map includes TIAA as a wealth/adviser distribution channel, not as a second technology platform or legal sponsor.

## Sponsor governance and expense transparency (2026-11-11)

- [Charitable sponsor governance, vendor relationships and operating expense review](sponsor-governance-and-fee-transparency-2026-11-11.md): Charityvest/Foundation Source board overlap, public conflict policy, RCF/Ren audited related-party fees, GiveClear/TIFIN, and NPT expense distinctions.
- [OneAscent's OneGive and indirect Foundation Source economics](oneascent-onegive-charityvest-disclosed-incentives-2026-11-11.md): public August 2026 Form ADV documents a waivable 55bps advisor fee, a fund's indirect equity interest in the tech vendor, investment model incentives and sales award criteria. These are *disclosed potential conflicts*, not proof of unsuitable conduct. [12 synthetic cases](../data/onegive-adviser-suitability-test-cases-2026.csv) and [four fee illustrations](../data/onegive-55bps-fee-illustrations-2026.csv) are unexecuted and hypothetical.
- [20 governance and oversight controls](../data/sponsor-governance-controls-2026.csv): observed vendor-board roles, recusal policies, actual fee payee verification, related-party contracts and access limitations.
- [Four-sponsor FY2024 expense comparison](../data/sponsor-expense-category-comparison-2024.csv): reports grants, non-grant residuals and 990 fee categories **without** treating them as vendor fees; includes the separately audited RCF→Ren $19.2255m payment.
- [Six GiveClear 2025 wealth and technology partners](../data/giveclear-wealth-partner-observations-2025.csv): AssetMark, Blue Trust, Ingalls & Snyder, Arlington, Zions Bank and TIFIN, with sponsor-reported evidence but **no inferred partner ARR**.
- [20-source governance and expense evidence register](../data/sponsor-governance-sources-2026.csv): government filing instructions, board disclosures, actual policies, 990 information and inaccessible audit indexes.

**Important governance distinction:** Charityvest publicly lists **Stephen Kump (Foundation Source DAF Technology President)** on its own board while Foundation Source is its fee-paid technology/admin provider. Its public policy requires disclosure and director recusal for conflicts, but actual meeting records and specific vendor approvals have **not been examined**. Overlap is a reason to test disinterested decision-making, **not proof of wrongdoing**. Charityvest and GiveClear's full 2024 audit attachments remain uninspected, so precise vendor fees are still unknown.

## Principal findings

- For philanthropic Ren at `reninc.com`, **AEF's July 2025 announcement asserts SOC 2 Type II**, while **AEF's April 2026 announcement asserts Type I**. This is a **public-source conflict**; no actual audit report inspected. A separate Type II claim by `tryren.com` remains unrelated.
- Chariot markets **SOC 2 Type II**.
- TIFIN Give markets **SOC 2 security compliance**, but public evidence reviewed does not specify type.
- **No independent auditor report was inspected.** All other organizations remain unverified in this scoped review; no negative assurance conclusion follows.

No confidential or client-specific material is included.
