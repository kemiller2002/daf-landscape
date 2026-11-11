# Comprehensive DAF Industry Report: research architecture and critical hypotheses
**Research blueprint | November 11, 2026 | This is a coverage plan, not a completed 42-topic empirical study**

## Purpose

A serious donor-advised fund industry report should follow **charitable capital, tax treatment, sponsor governance, technology, financial incentives, distribution and observed recipient impact**. Company/product comparison is necessary but not sufficient.

The decision problems are:
1. **Does DAF intermediation increase socially beneficial charitable activity or shift the timing, location and accounting of existing gifts?**
2. **Who earns fees, holds obligations and has genuine governance control at each step?**
3. **What drives institutional adoption, costs, operating quality and customer retention?**
4. **How well do DAFs respond to donor intent, nonprofit need, economic shocks and regulatory changes?**
5. **Which technical and organizational interventions create incremental value versus moving work between actors?**
6. **Which claims are supported now, which need counterfactuals, and what would change our conclusions?**

No universal "DAFs good" or "DAFs bad" answer is assumed. The value of a DAF depends on donor intent, sponsor structure, operating decisions, recipient context and counterfactual giving paths. Similarly the best platform for one institution may be inferior for a charity with different needs.

## Evidence architecture

\`\`\`mermaid
flowchart TD
 A[Donor: resources, intent, constraints] --> B[Vehicle choice: direct, DAF, other, or none]
 B --> C[Sponsor charitable ownership and legal controls]
 C --> D[Investments, custody, fees and optional advisors]
 D --> E[Grant recommendation and sponsor approval]
 E --> F[Payment, settlement and nonprofit acknowledgement]
 F --> G[Recipient services and social outcome]
 H[Tax deductions, public subsidy and law] -.-> B
 I[Vendor technology, labor and infrastructure] -.-> C
 I -.-> E
 I -.-> F
 J[Market competition and board incentives] -.-> C
 J -.-> D
 K[Community need, resilience and policy] -.-> G
 G -.-> L[Validated outcomes and counterfactuals]
 L --> M[Clarity judgments and periodic reassessment]
 M -.-> A
\`\`\`

**Accounting convention:** at every arrow, identify legal payer and payee, whether it is a charitable contribution, sponsor asset, distribution, vendor fee, investment return, transfer, or program outcome. Never count donor deposits, sponsor assets and nonprofit payments as independent economic output.

## Seven interconnected research pillars (42 topics)

| Pillar | Topics | Key work | Decision enabled |
|---|---:|---|---|
| **Market structure** | 5 | Sponsor types, donation processing vs invested accounts, mergers, procurement, substitute operating models | Who really buys which kind of platform? |
| **Financial economics** | 8 | Capital-flow reconciliation, delay and duration, fee waterfall, pricing, market stress, complex assets, impact investing, **bankruptcy protection of charitable funds** | Where are capital and value retained or dissipated? |
| **Donor economics** | 6 | Tax incrementality, fit, behavior, advisor incentives, succession, accessibility | Which vehicle creates real donor/recipient value? |
| **Nonprofit outcomes** | 7 | Settlement/recognition, geographic need, government shocks, privacy, impact, disasters, community networks | What changes after funds reach charities? |
| **Public policy** | 6 | Payout approaches, taxable benefits, oversight, cross-border giving, privacy, regulatory changes | Which controls and tradeoffs remain legal and justified? |
| **Technology** | 6 | Fund accounting, portability, security, AI evidence, accessible interfaces and **independent vendor technology audit** | Does software improve correct completed outcomes? |
| **Future and uncertainty** | 4 | Tax/market scenarios, global adjacent models, consolidation/systemic dependency and **provider mortality/data continuity** | What survives shocks and changed incentives? |

See the [42-row topic and source coverage matrix](../data/comprehensive-daf-research-coverage-2026.csv) for topic-level priority, current coverage and required measurement.

### Suggested final report table of contents

1. **Executive findings and Clarity conclusion registry:** 10 high-value evidence-bounded conclusions, objections and current action.
2. **Methodology and epistemic controls:** what each metric can prove, sample selection, source revisions, assumptions and correctness tests.
3. **Legal and organizational architecture:** donor, sponsor, advisor, custodian, technology vendor, nonprofit and government roles.
4. **Market and competitors:** full 25-entity baseline, sponsor category denominator, independent platform buyers and substitutes.
5. **Charitable capital economics:** tax recognition, contributions, account balances, investment returns, fees, grant approval and actual settlement.
6. **Donor and advisor decisions:** causality vs substitution; behavioral economics; grant and contribution timing; suitable vehicle choices; successor options.
7. **Technology and operations:** fund accounting, brokerage/custody feeds, payment, exceptions, independent security, data migration and access.
8. **Independent provider technology audit:** legal asset/fund segmentation, APIs, identity, grant settlement and returns, independent scope of assurance, real operational tests and falsification.
9. **Provider mortality, acquisitions and continuity:** Flipcause, Everfund, Kambeo, Blackbaud and DonorPerfect as adjacent failure/incident lessons; Vennfi, Giving Place, Benevity Alaya and other product transitions carefully distinguished; full legal sponsor and donor record exit continuity.
10. **Nonprofit effects:** recipient engagement, privacy, philanthropy additionality, geographic gaps, social output measures and failure cases.
11. **Competitive business economics:** named payee revenues, financial incentives, operating costs, customer retention and consolidation, without invented margins.
12. **Regulatory and tax scenarios:** direct vs DAF giving, pending legislation, governance and excise taxes, cross-border grants and enforcement evidence.
13. **Stress and resilience:** market downturn, government funding shock, disaster deployment, sponsor exits and digital infrastructure outages.
14. **Falsifiable future outlook:** what would change conclusions, data acquisition plan, modeled scenarios and limitations.

## Priority work that can change conclusions

**P0 (21 topics)** across market structure (3), financial economics (4), donor economics (4), nonprofit outcomes (4), public policy (2), technology (3), future/uncertainty (1). P1 includes 16 topics; P2 includes five. These classifications reflect **information value and decision consequences**, not how interesting the subject sounds.

### First evidence packages

**1. Donor-level incrementality vs substitution.** The most debated DAF claim is whether the tax-favored vehicle causes more charitable activity or delays/concentrates prior intent. Existing nonprofit recipient studies document different giving patterns [C21]; TCJA elasticity work is general charitable behavior, not a DAF-specific causal effect [C09]. We need donor-wide grants/donations, comparison groups, gift timing, privacy-safe linkage, and real-world counterfactuals.

**2. Recipient service and need geography.** GivingTuesday [C02,C03] offers new nonprofit geographic/mission data but explicitly notes major missingness. We need actual **DAF grant recipient EIN and service location**, not only nonprofit headquarters and modeled missions. Avoid measuring "impact" as grants received without knowing actual services delivered and what would happen otherwise.

**3. Economics and business incentives.** We already established a named RCF→Ren service fee in audited statements, but don't know consolidated vendor profit or other provider fee splits. We need complete cash/fee/operating waterfall at matched same-period legal entity scale, not symbolic market share.

**4. Sponsor operational capacity and grant reliability.** The 128-manager DAFRC survey [C08] reports perceived differences among grant review, solicitation and staffing. Test actual cost, reviewer effort, errors, disbursement delays and corrections before choosing an AI/automation hypothesis.

**5. Risk, shocks and policy.** Urban's 2026 study [C04] identifies disruptions among operating charities. The relevant DAF question is **whether accessible DAF assets can reach affected recipients soon enough**, given donor discretion and sponsor approval, and whether giving is truly additional. Regulatory rules and planned guidance must be dated and reviewed independently [C10–C14,C26].

**6. Donor succession and social time horizon.** Existing policy research [C15] documents varied successor and beneficiary choices, but not actual elections or completed grants. Measure **asset-duration, donor control, grant distributions, successor policy and changed social needs**, then evaluate more than one defensible ethical perspective rather than forcing a single ideology into the result.

## Clarity as a research-quality gate

For **every major conclusion** in the final report, attach:
- **Claim statement and scope.** Legal entity, population, time, unit and geography.
- **Evidence landscape.** Direct support, contradictory evidence, independence of sources, original methodological caveats.
- **Assumption landscape.** Explicit and shadow assumptions; plausible alternative causes and model choices.
- **Current best understanding.** Describe only what data actually justify.
- **Confidence calibration.** Qualitative or validated quantitative; distinguish confidence in a reported statistic from a new business or causal inference.
- **Impact/correctability.** A low-risk exploratory hypothesis and an irreversible donor/tax or investment decision need different standards.
- **Recommended posture.** Fast, Experimental, Guardrail or Strategic as appropriate, not an arbitrary score.
- **Monitoring plan.** Signal, threshold, owner, trigger and conditions for reconsidering the trigger itself.
- **Reassessment plan.** Specific evidence capable of strengthening, weakening or reversing the conclusion.

See [Clarity 32-point assumption audit](clarity-report-assumption-audit-2026-11-11.md) and [10 conclusion records](../data/clarity-conclusion-register-2026.csv). A useful "we cannot yet tell" is an actionable outcome when it prevents a high-consequence unsupported commitment.

## What makes this research distinctive

- **Cross-domain evidence:** tax microeconomics, portfolio finance, institutional governance, behavioral donor choice, nonprofit organizational resilience, social outcomes and software systems are analyzed on common legal/entity/time axes.
- **Explicit disconfirming pathways:** every hypothesis has a plausible rival account and a test that could *reverse* it.
- **Lifecycle observations:** not merely DAF funds opened or grants requested, but accepted donor assets, sponsor authority, payment settlement, recipient cash receipt and real program outcomes.
- **Separate valuations:** public benefit, donor utility, nonprofit value and private financial capture are not collapsed into an undifferentiated "impact" rating.
- **Decision traceability:** Clarity governs warranted inference and commitment; EDF investigates actual observed failures and pathways where appropriate. Neither framework creates nonexistent data.
- **Historical immutability:** when DAFRC reclassifies donor account groups, a company changes vendor, or law changes, prior dated conclusions remain intact and are explicitly superseded, never silently overwritten.

## What is not complete

This blueprint and the claim audit **do not** mean all 39 domains are already researched, raw DAFRC sponsor data collected, vendor platforms independently tested or causal effects proved. The sources register has **27 qualified source leads**, but some sources are references for **future** primary extraction. Current available public summaries, published methodology and our prior repository reports support only a subset of the eventual analysis.

The new [independent DAF technology and provider failure study](daf-technology-audit-and-provider-exits-2026-11-11.md) adds operational evidence and closure/insolvency distinctions. Its first-stage public review is **not a code audit or penetration test**.

The final report should never assert a policy/technology investment winner from this planning stage. Its credibility will depend on preserving the difference between what has been established and what remains worth testing.

## Source, audit and report index

- [42-topic coverage matrix](../data/comprehensive-daf-research-coverage-2026.csv)
- [27 qualified independent/regulatory/industry source leads](../data/comprehensive-research-source-catalog-2026.csv)
- [32 Clarity assumption evaluations](../data/clarity-report-assumption-audit-2026.csv)
- [10 decision-ready Clarity conclusions](../data/clarity-conclusion-register-2026.csv)
- [Clarity assessment with 3 fully worked cases](clarity-report-assumption-audit-2026-11-11.md)
- [Prior DAF research index](README.md)
