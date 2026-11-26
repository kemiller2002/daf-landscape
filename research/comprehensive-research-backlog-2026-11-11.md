# Comprehensive DAF Research Backlog and Evidence Program
**Created:** 2026-11-11
**Status:** Research agenda, not verified findings
**Companion:** [Existing 45-topic blueprint](comprehensive-daf-research-blueprint-2026-11-11.md), [technology audit](daf-technology-audit-and-provider-exits-2026-11-11.md), [Clarity assumption audit](clarity-report-assumption-audit-2026-11-11.md)

## Operating rules
For every topic, produce: (1) precise decision/question, (2) population and legal entities, (3) source register with publication and observation dates, (4) observed facts separately from vendor claims, (5) competing hypotheses, (6) causal identification or explicit noncausal limitation, (7) denominators and sensitivity ranges, (8) contrary evidence, (9) Clarity assumption audit, (10) EDF diagnostic of incentives, failure mechanisms and interventions, (11) falsification criteria, (12) confidence and residual uncertainty, (13) practical implication and owner/next evidence request.

Never equate sponsor assets, donor contributions, grants, or vendor revenues. Never treat a vendor's public documentation as a verified production control. Avoid publishing private/NDA or former-employer information. Record exact entity, product, period, jurisdiction and provenance. Prioritize by decision impact × uncertainty × evidence accessibility; mark unknown rather than invent scores.

## Research topics (new and expanded)
Each numbered topic is a distinct work package; P0 = decision-critical, P1 = important, P2 = exploratory. Existing research should be linked and extended, not duplicated.

### A. Market boundaries, history and competitive map
- A01 P0: Define DAF market boundaries: sponsoring charities, enterprise administration software, payments, custody, advisory, direct giving and private foundations; avoid double counting.
- A02 P0: Reconcile historical annual series across National Philanthropic Trust, DAF Research Collaborative, IRS 990 and sponsor filings; explain differing denominators and revisions.
- A03 P0: Segment commercial buyers and economic decision makers: national sponsors, community foundations, wealth managers, workplace giving, nonprofit fundraising, affinity groups.
- A04 P0: Map ownership, partnerships, subservice vendors, sponsor affiliations, custody and banking dependencies for top providers.
- A05 P1: Track acquisitions, mergers, rebrands, product retirements, insolvencies and displaced customers with verified dates and successor entities.
- A06 P1: Compare DAF adoption and administration models internationally, with jurisdiction-specific tax and charitable law.
- A07 P1: Test barriers to entry, switching costs, procurement cycles and concentration using actual contracts and cohort data.
- A08 P2: Map adjacent substitutes: charitable trusts, private foundations, giving accounts, fiscal sponsorship, planned giving and direct gifts.

### B. Donor economics, taxation and behavior
- B01 P0: Model direct gift vs DAF vs private foundation vs charitable trust, separately by income, asset type, liquidity and goals; tax rules by year.
- B02 P0: Measure incremental giving vs timing substitution using donor-level longitudinal comparisons and credible controls.
- B03 P0: Analyze donation of appreciated securities, concentrated positions, restricted shares, real estate, business interests and complex assets, including acceptance and liquidation risk.
- B04 P0: Test donor tax-opportunity engines against edge cases: AGI limits, carryforwards, basis, holding period, itemization, state tax, substantiation and timing.
- B05 P1: Examine donor liquidity, behavioral commitment, recurring grants, choice overload and default settings.
- B06 P1: Evaluate successor advisors, multigenerational giving, inactive accounts and donor death.
- B07 P1: Quantify advisor compensation, referral economics and conflicts between asset retention and grantmaking.
- B08 P1: Assess anonymity, identity verification, donor privacy and accessible donor experience.
- B09 P1: Model legislative sensitivity including payout proposals, deduction limits and excise rules; distinguish enacted from proposed.
- B10 P2: Investigate donor regret, account closure, mistaken grants and disputed restrictions.

### C. Sponsor, vendor and custodian economics
- C01 P0: Build a complete transaction-level money and obligation waterfall from gift to nonprofit receipt.
- C02 P0: Reconcile vendor revenues to named payers and contract terms, not inferred assets-under-management market share.
- C03 P0: Compare sponsor administrative, investment, custody, advisor, transaction and payment fees on identical asset/transaction scenarios.
- C04 P0: Estimate servicing cost per account, complex gift, reviewed grant and settled grant; isolate fixed vs variable cost.
- C05 P0: Study financial resilience of sponsors and vendors under market declines, withdrawals, fee compression and concentration loss.
- C06 P1: Examine revenue retention, contract renewals, customer concentration, churn and migrations by cohort.
- C07 P1: Test economics of in-house builds vs outsourced platforms vs modular API stacks.
- C08 P1: Study float, investment allocation, liquidity management, cash drag and grant timing incentives.
- C09 P1: Analyze operating subsidy, cross-subsidy and below-cost product pricing.
- C10 P1: Trace legal ownership and creditor protections for donated assets, bank accounts and vendor insolvency.
- C11 P2: Evaluate financial effects of impact investments, recoverable grants and program-related structures where permitted.

### D. Nonprofit recipient experience and outcomes
- D01 P0: Measure end-to-end grant initiation, approval, payment, settlement and recipient acknowledgment time.
- D02 P0: Investigate unclaimed, returned, misdirected and failed grants, reconciliation and exception resolution.
- D03 P0: Test whether DAF giving increases nonprofit resources or displaces other channels, with counterfactual controls.
- D04 P0: Map geographic and cause allocation using recipient EIN and actual service geography rather than headquarters alone.
- D05 P0: Measure donor anonymity effects on stewardship, nonprofit CRM reconciliation and repeat giving.
- D06 P1: Examine grant restrictions, reporting burdens and recipient administrative costs.
- D07 P1: Study emergency response and whether DAF balances are deployed during shocks when recipients need liquidity.
- D08 P1: Compare grant predictability and unrestricted support with direct donations and institutional grants.
- D09 P1: Test nonprofit discovery, recommendation ranking and inequities in distribution.
- D10 P2: Link grants to defensible service outputs and outcomes without claiming that payments alone equal impact.

### E. Governance, law and public interest
- E01 P0: Map legal sponsor discretion, donor advisory rights, prohibited benefits and decision accountability.
- E02 P0: Examine IRS enforcement, sponsor governance, Form 990 reporting limitations and related-party risks.
- E03 P0: Compare payout rate methodologies: aggregate, cohort, account, asset-weighted, transfer-adjusted and actual charitable settlement.
- E04 P0: Evaluate DAF-to-DAF transfers and circular flows, including double counting and delay.
- E05 P1: Study fiscal sponsorship, affinity/faith groups, community funds and donor-benefit boundaries.
- E06 P1: Examine cross-border grants, sanctions screening, equivalency determination and expenditure responsibility.
- E07 P1: Model policy tradeoffs using distributional, fiscal and nonprofit liquidity effects, not advocacy assumptions.
- E08 P1: Assess donor privacy, public transparency and governance accountability tradeoffs.
- E09 P2: Compare state charitable oversight and variations in enforcement.

### F. Technology architecture, security and continuity
- F01 P0: Independently map legal fund ledger, custody feeds, tax-lot accounting, grants, payment rails and reconciliation controls by vendor.
- F02 P0: Validate current scoped SOC 1/SOC 2 evidence, CUECs, subservice organizations, exceptions and audit periods.
- F03 P0: Test role and tenant isolation, sponsor authorization, advisor privileges, consent, impersonation and audit trails.
- F04 P0: Test API/webhook idempotency, retries, replay, event ordering, duplicate payment prevention and reversals.
- F05 P0: Verify data export, event history, portability and recovery in vendor failure, acquisition or product sunset.
- F06 P0: Run operational resilience scenarios: custodian feed failure, banking outage, stale positions, failed settlement and restore.
- F07 P0: Evaluate AI recommendations and agent actions against held-out cases, hallucinations, authority boundaries and human override.
- F08 P1: Map actual deployed stack and integration architecture only where verified; distinguish marketing from observed production.
- F09 P1: Measure time to implement, integration burden, deployment frequency, defects and change failure rate.
- F10 P1: Audit accessibility, mobile performance, onboarding and usability using observed tasks.
- F11 P1: Assess data governance, lineage, retention, encryption, data residency and vendor/subprocessor exposure.
- F12 P1: Study identity federation, SSO, MFA, delegated access, revocation and key lifecycle.
- F13 P1: Compare build vs buy and vendor lock-in using reproducible migration exercises.
- F14 P2: Investigate open protocols, portable transaction schemas and interoperability opportunities.

### G. Provider deep dives and failures
- G01 P0: Ren: legal entities, product scope, sponsor contracts, revenue concentration, technology audit, portability and assurance.
- G02 P0: TIFIN Give: white-label operations, custody, tax intelligence, buyer economics, AI controls and implementation evidence.
- G03 P0: Chariot: DAFpay vs Donor Accounts roles, sponsor dependencies, API correctness and payment reconciliation.
- G04 P0: Foundation Source/Vennfi and Charityvest: acquisition integration, sponsorship boundaries, custody and exit paths.
- G05 P1: Fidelity Charitable, Schwab Charitable, National Philanthropic Trust, AEF and community foundation platforms: sponsor-operated vs outsourced.
- G06 P1: Daffy, GivingTech, GiveClear and other emerging vendors: actual availability, entity structure, revenue model and differentiated capabilities.
- G07 P1: Research shutdowns, insolvencies, breaches and sunsets as separate event classes; collect primary closure, court and customer-migration evidence.
- G08 P1: Identify shared vendors and correlated failure exposure across nominal competitors.
- G09 P2: Build buyer-specific substitution tests and procurement RFP comparisons.

### H. Clarity and EDF decision intelligence
- H01 P0: Create a machine-readable claim → evidence → assumption → inference → conclusion → decision graph with provenance.
- H02 P0: Audit every published industry report for denominator changes, selection bias, survivorship bias, timing mismatch and causal overreach.
- H03 P0: Develop competing-hypothesis matrices for DAF additionality, payout, tax subsidy, vendor moat and AI efficiency.
- H04 P0: Apply EDF to identify root causes, incentive conflicts, bottlenecks, failure propagation and intervention leverage.
- H05 P0: Construct falsification tests and evidence thresholds for every major conclusion; maintain unresolved and contradicted status.
- H06 P0: Build buyer-specific decision scenarios and sensitivity analysis; refuse false precision or unsupported ordinal vendor rankings.
- H07 P1: Use workflow redesign vs AI automation controlled comparisons, including intake completeness, labor minutes, errors and outcomes.
- H08 P1: Build an evidence-quality rubric covering source independence, entity scope, recency, sample bias, reproducibility and contrary evidence.
- H09 P1: Test counterfactual recommendations and decision regret using historical cases and blinded expert review.
- H10 P1: Create a dated conclusion register with automatic review triggers and explicit what-would-change-my-mind fields.
- H11 P2: Evaluate causal graphs, Bayesian updating and value-of-information methods where data supports them.

### I. Forecasting, shocks and future structure
- I01 P0: Stress-test DAF assets, sponsor revenue and nonprofit grants against equity downturns and liquidity shocks.
- I02 P1: Model tax-policy scenarios without treating pending proposals as law.
- I03 P1: Examine bank/custodian consolidation, platform acquisitions and infrastructure concentration.
- I04 P1: Forecast adoption by buyer segment under explicit assumptions and sensitivity ranges.
- I05 P1: Study effects of AI commoditization on implementation cost, differentiation and switching.
- I06 P1: Evaluate demographic succession and advisor channel shifts.
- I07 P2: Compare resilience and portability of centralized vs modular platform models.

### J. Evidence acquisition and research execution
- J01 P0: Maintain entity/product/contract/period/source IDs and reproducible extraction scripts.
- J02 P0: Create an interview and document-request protocol for sponsors, nonprofits, donors, advisors, vendors and regulators.
- J03 P0: Establish evidence access levels: public, permissioned, NDA, confidential; prohibit confidential material in public repo.
- J04 P0: Reconcile source totals and data lineage with independent cross-checks.
- J05 P1: Design a stratified sample across sponsor size, product type, nonprofit mission and donor segment.
- J06 P1: Maintain research gap, contradiction, retraction and dated source-refresh registers.
- J07 P1: Define replicable operational test harness and vendor demo score sheets.
- J08 P1: Establish editorial review: subject-matter, legal/tax, statistical, technical and adversarial.
- J09 P2: Create public data appendix and methodological limitations for report readers.

## Cross-cutting questions that deserve explicit investigation
1. Are reported grants measured at recommendation, approval, payment or nonprofit receipt?
2. Are annual payout rates inflated by DAF-to-DAF transfers, re-grants, or mismatched beginning/end assets?
3. Does a platform actually control the sponsor ledger, or only present a front end?
4. Who bears the loss when a grant is misdirected, a complex gift fails or a vendor shuts down?
5. Do donor and advisor incentives systematically delay distributions?
6. Is a tax optimization feature actually a tax-law decision engine, a rules checklist or marketing?
7. Are claimed AI labor savings net of verification, exception handling, security and changed workflow?
8. Does an acquisition preserve five years of audit history and portable fund-level data?
9. What is the marginal nonprofit benefit compared with a direct gift or an alternative donor vehicle?
10. What evidence would cause us to recommend against a DAF or against a particular provider?

## Initial execution waves
**Wave 1, evidence integrity:** A01-A04, B01-B04, C01-C05, D01-D05, E01-E04, F01-F07, H01-H06, J01-J04. Reconcile existing files and register gaps first.

**Wave 2, provider and customer verification:** G01-G08, C06-C10, F08-F13, B05-B09, D06-D09, E05-E08, J05-J08. Obtain permissioned documents and run controlled tests before scoring.

**Wave 3, synthesis and scenarios:** I01-I07, H07-H11, remaining P2 topics. Publish conclusions only with scope, competing hypotheses, evidence strength and falsification.

## Required work-package deliverable
```yaml
id: A01
question: ""
decision_supported: ""
priority: P0
scope: {entities: [], products: [], jurisdictions: [], observation_period: ""}
claims: []
sources: [] # source ID, URL, publication date, observation date, independence
observations: []
assumptions: []
competing_hypotheses: []
tests: []
counterfactual: ""
denominator: ""
limitations: []
contrary_evidence: []
clarity_assessment: ""
edf_diagnosis: ""
falsification: ""
confidence: unassessed
status: not_started
next_evidence: []
conclusion: null
review_trigger: ""
```

## Publication gates
No empirical conclusion without traceable evidence. No causal language without identification strategy. No security certification from a marketing badge. No provider failure classification without verified corporate event. No vendor ranking without equivalent tested scope. All unknowns remain visible. Separate tax/legal educational models from individualized professional advice.
