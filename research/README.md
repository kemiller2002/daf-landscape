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

## Market demand, donor behavior, and decision-critical data gaps (2026-11-11)

- [Demand and evidence-gap synthesis](daf-market-demand-and-evidence-gaps-2026-11-11.md): revised 2024 market scale, 2024 longitudinal donor activity, 2025 donor/manager surveys, 2026 recipient and financial adviser findings, nonprofit attribution and pending tax guidance.
- [33 observed metrics, with denominator and date](../data/market-demand-observed-metrics-2026.csv): separates market-wide sponsor totals from historic account microdata, selected donor surveys, selected nonprofit gift data and vendor-specific account scale.
- [27 ranked missing-data questions](../data/decision-critical-data-backlog-2026.csv): **9 P0**, **10 P1**, **8 P2**; specifies metric, known/unknown state, best retrieval path, permission requirement and acceptance evidence.
- [Collection and causal-evaluation design](evidence-collection-design-2026.md): reproducible sponsor-year data mart, consent-safe lifecycle events, matched cost and grant performance metrics, and test protocols; no vendor systems executed.
- [18-source evidence register](../data/market-demand-evidence-sources-2026.csv): independent DAFRC studies and revised FY2024 data, NPT/Fidelity sponsor reports, nonprofit study with disclosed Chariot affiliation and 2026 IRS guidance-plan status.

**Critical market interpretation:** The DAFRC's Spring 2026 revised FY2024 baseline is **3.59 million reported DAF accounts**, **$327.87 billion charitable assets**, **$90.57 billion contributed**, and **$64.60 billion granted**. Account growth includes mass donation processors. This is **not** 3.59 million independent invested DAFs or an enterprise software subscription market. Historic account inactivity (**22% in 2020–22 in a voluntary sample**) is also not vendor churn, while nonprofit donor-retention premiums are not technology-company NRR. True platform economics require **paying contract cohorts and completed/settled grant costs**.

## Decision Intelligence: applying Clarity + EDF to DAF conclusions (2026-11-11)

The next differentiator is **conclusions that can be audited, challenged and reassessed**, not just collecting more DAF data. This is a **research-candidate application**, not a new version of either framework or a functioning inference engine.

- [Application architecture and exact framework boundaries](decision-intelligence-architecture-2026.md): EDF diagnoses observable outcomes, Clarity governs justified reasoning depth, decision posture and reassessment, and a separate execution layer implements decisions. Canonical Clarity/EDF repositories are unchanged.
- [Three worked decision results](decision-intelligence-pilot-2026-11-11.md): whether grant vetting is the best first product, whether 3.59m DAF accounts implies enterprise software TAM, and whether Ren's audited RCF fee proves superior profitability to Foundation Source. Conclusions include counterarguments, decision posture, unknowns and falsification triggers.
- [Three structured result cards](../data/decision-intelligence-results-v0.json): explicit Clarity/EDF usage plus GitHub **commit SHA pins** for original framework and evidence snapshots; no arbitrary numeric certainty or fabricated company financials.
- [Ten atomic claims and counterclaims](../data/decision-intelligence-claims-2026.csv): each includes scope, supporting citations, unjustified inferences, current state and reassessment evidence.
- [Twenty proposed adversarial regression cases](../data/decision-intelligence-regression-cases-2026.csv): denominator confusion, account vs client, false causality, outdated market snapshots, wrong payee attribution, fake agent independence, invalid confidence and framework version integrity. **Not executed against software.**

**Core product rule:** When a proposed vendor ranking lacks comparable evidence, **"not justified" is a positive decision result**. When a causal analysis is unwarranted, Clarity can stand alone without manufacturing an EDF origin network. Next engineering phase: minimal **F#** source/provenance validator, structured result renderer and tests; optional Limen/Forma view only after logic and regression behavior pass. Validate usefulness against a baseline data summary in blinded reviews before claiming a competitive edge.

## Comprehensive industry expansion and Clarity report audit (November 11, 2026)

The goal is a fully comprehensive DAF industry assessment across **legal sponsorship, economics, philanthropy, tax, donor/advisor behavior, nonprofit outcomes, governance, technology and resilience**. This stage delivers the research architecture and a critical audit, **not a claim that every topic has been fully empirically studied**.

- [Comprehensive research blueprint](comprehensive-daf-research-blueprint-2026-11-11.md): 15 proposed report chapters; **45 cross-disciplinary topics** with 23 P0, 17 P1 and 5 P2 priorities; separation of charitable capital, commercial revenue and actual nonprofit outcomes.
- [Clarity assumption audit of external and internal reports](clarity-report-assumption-audit-2026-11-11.md): **32 reviews**, including 20 external-report claims/interpretation hazards and 12 of our own findings. Three detailed Clarity case studies cover DAF-caused giving, geographic underserved need and donor engagement versus AI grant vetting.
- [Structured 32-item claim, assumption, alternative and reassessment matrix](../data/clarity-report-assumption-audit-2026.csv): publisher-level overreach is distinguished from reader misinterpretation, appropriately scoped methods and our provisional hypotheses.
- [Ten high-value Clarity conclusions](../data/clarity-conclusion-register-2026.csv): justified statement, open assumptions, posture, next action and concrete reassessment trigger.
- [45-topic coverage matrix](../data/comprehensive-daf-research-coverage-2026.csv) and [27 qualified sources/research leads](../data/comprehensive-research-source-catalog-2026.csv).

**Central correction:** The 2026 K2D/Chariot public report page goes beyond showing selected DAF switchers gave more at participating nonprofits to claiming DAFs cause increased giving; an actual donor-wide counterfactual remains unproven. DAFRC's 2026 revision and GivingTuesday's 2026 geographic report, by contrast, **openly disclose** many of their denominator, classification and missingness limitations. The challenge is often preserving these caveats when other analysts turn observations into market size, strategy, or tax policy claims.


## DAF provider technology, exits, insolvency and data continuity (2026-11-11)

- [DAF Technology Audit and Provider Failure/Exit Study](daf-technology-audit-and-provider-exits-2026-11-11.md): public technical evidence and bounded Clarity/EDF interpretations, actual shutdown and bankruptcy distinctions, active API/ledger evidence, security incidents and recovery/exit test scenarios. **Public documentation review, not a penetration test or production system certification**.
- [Twelve-provider technology evidence matrix](../data/provider-technology-evidence-matrix-2026.csv): Ren, Foundation Source, TIFIN Give, DAFtech, Chariot, Daffy, NPT and adjacent platforms. Unexecuted technical checks remain **not_verified**, not scored failed.
- [24 technology diligence controls](../data/technology-audit-control-matrix-2026.csv): 13 P0 / 9 P1 / 2 P2, spanning legal sponsor fund ownership, segregated payments, accounting, grant idempotency, cyber security, exits and disaster recovery.
- [11 dated company, product and incident cases](../data/technology-provider-exits-and-incidents-2026.csv): Flipcause bankruptcy, Everfund/Kambeo shutdowns, planned Benevity Alaya sunset, Vennfi and Giving Place acquisitions, CyberGrants and Classy rebrands/continuity, DonorPerfect November 2026 disruption, Blackbaud historical security enforcement, JustGiving dependency end of life.
- [34 qualified sources](../data/technology-audit-source-register-2026.csv) and [16 Clarity falsification checks](../data/technology-audit-clarity-challenges-2026.csv): no false claim that a core DAF vendor failed when only an adjacent fundraising service did.

**Critical distinction:** We have confirmed *adjacent fundraiser technology* insolvency/shutdown cases, not a statistically complete mortality history of core DAF administration platforms. Separate a charitable sponsor's legal ownership of assets from software or payment intermediary funds, vendor corporate IP, program continuity and donor accounting records. Actual legal/technical failure mechanisms require evidence; no provider's hidden runtime stack or current quality is inferred from public brochure.

The comprehensive industry matrix now covers **45 topics with 23 P0 / 17 P1 / 5 P2**, including provider survival and technology validation, and the [15-chapter report blueprint](comprehensive-daf-research-blueprint-2026-11-11.md) indexes their work.

## Faith-based, megachurch and special-interest DAF networks (November 11, 2026)

- [Megachurch and affinity DAF study](affinity-dafs-megachurches-and-special-interest-organizations-2026-11-11.md): religious/affinity grant ecosystems and legal distinctions across direct giving, donor-advised, organization-advised and endowment structures. Covers NCF, Signatry, WaterStone, JCF, Catholic foundations, AMCF, community/issue programs and tax boundaries. **No claim that ordinary cash church giving should be converted to DAFs.**
- [30 affinity sources](../data/affinity-daf-source-register-2026.csv), [18 segmented fund and institution models](../data/affinity-daf-segments-and-models-2026.csv), [18 Clarity assumption checks](../data/affinity-daf-clarity-audit-2026.csv), and [12 qualified B2B opportunity tests](../data/affinity-daf-commercial-opportunity-tests-2026.csv). Source rows cover current IRS church Form 990 exceptions, 2026 nonitemizer direct cash deductions excluding DAF contributions, c3/c4/c6/527 boundaries and disclosed provider fees, including unresolved AMCF competing public fee pages.
- [Historical DAF sponsor and platform lifecycle, 2011–2026](historical-daf-sponsor-technology-lifecycle-2011-2026.md): 2011 Blackbaud→Renaissance DAF software lineage, Ren and Foundation Source acquisitions, 2009/2011 National Heritage Foundation bankruptcy/revocation with later sponsor filings, AEF's 2024/2026 donor portal migrations and October 2026 DonorCentral closure. **Known-case ledger, not population mortality rate.**
- [24 dated historical events](../data/historical-daf-lifecycle-events-2011-2026.csv), [33 history sources](../data/historical-daf-lifecycle-sources-2011-2026.csv), [18 historical Clarity checks](../data/historical-daf-lifecycle-clarity-challenges-2026.csv), [5 selected NHF asset observations](../data/national-heritage-foundation-filing-trajectory-2014-2022.csv).

**New distinction:** Faith communities can be 501(c)(3) grant recipients, independent DAF sponsors, outreach distribution networks, or organizations advised on funds they do **not** legally own. Public church Form 990 exceptions mean ordinary 990 datasets cannot show the complete church-grant market. NCF reports $468m FY2025 grants **to churches**, not specifically megachurches, and that figure is not technology revenue. Hartford megachurch attendance is not paying SaaS contracts. Religion or individual giving intent must not be inferred for commercial donor targeting.

The comprehensive industry research plan now has **45 topics across eight pillars, 23 P0 / 17 P1 / 5 P2, and 15 proposed report chapters**. The new evidence and opportunity analyses remain **public-source hypotheses**, without vendor sandbox tests, actual church procurement contracts, full historical vendor populations, or causal donor-giving proof.

## Principal findings

- For philanthropic Ren at `reninc.com`, **AEF's July 2025 announcement asserts SOC 2 Type II**, while **AEF's April 2026 announcement asserts Type I**. This is a **public-source conflict**; no actual audit report inspected. A separate Type II claim by `tryren.com` remains unrelated.
- Chariot markets **SOC 2 Type II**.
- TIFIN Give markets **SOC 2 security compliance**, but public evidence reviewed does not specify type.
- **No independent auditor report was inspected.** All other organizations remain unverified in this scoped review; no negative assurance conclusion follows.

No confidential or client-specific material is included.

## Mission 2026-11-14: consolidated report, AI economics, dependency graph, validation

- **[Consolidated DAF industry report (Nov 2026)](DAF-INDUSTRY-REPORT-2026-11.md)**, the current top-level synthesis across all research.
- [Strategic synthesis A–G](mission-2026-11-14/strategic-synthesis.md): mistaken industry beliefs, what AI changes, incumbent vulnerabilities, what entrants should not build, value shift, falsification criteria, top ten discoveries.
- [Final status report](mission-2026-11-14/FINAL-STATUS.md) and [baseline inventory and plan](mission-2026-11-14/00-baseline-inventory-and-mission-plan.md).
- Workstreams:
  - [AI economics](mission-2026-11-14/ai-economics-replacement-analysis.md)
  - [AI failure modes](mission-2026-11-14/ai-governance-failure-modes.md)
  - [AI-native entrant](mission-2026-11-14/ai-native-entrant-simulation.md)
  - [vendor dependency graph](mission-2026-11-14/vendor-dependency-concentration.md)
  - [industry incentives](mission-2026-11-14/industry-incentives-structural-analysis.md)
  - [competitive histories](mission-2026-11-14/competitive-history-timelines.md)
  - [quantitative datasets](mission-2026-11-14/quantitative-datasets-and-data-dictionary.md)
  - [regulation, processor share and portability](mission-2026-11-14/regulation-market-structure-portability.md)
  - [breadth: community, faith, infrastructure](mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md)
- Validation: [wave 1](mission-2026-11-14/validation-wave1-report.md), [red team 2A](mission-2026-11-14/red-team-wave2a-ai-and-entrant.md), [red team 2B](mission-2026-11-14/red-team-wave2b-graph-data-incentives.md); registers in `data/mission-2026-11-14/validation-register*.csv`.
- Frameworks: [Clarity/EDF application guide](mission-2026-11-14/clarity-edf-application-guide.md), pinned to the canonical repositories.
- Reproducible scripts:
  - `scripts/mission_inventory.py`
  - `scripts/mission_coverage.py`
  - `scripts/mission_prioritize.py`
  - `scripts/mission_daf_metrics.py`
  - `scripts/mission_build_source_extracts.py`
