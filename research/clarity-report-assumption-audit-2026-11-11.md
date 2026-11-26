# Clarity Assumption Audit: DAF research reports and our own conclusions

**Evidence reviewed:** November 11, 2026. **Scope:** 20 candidate external-report interpretations and 12 from existing \`daf-landscape\` documents, each classified as a publisher overreach, downstream misinterpretation risk, normative/modeling assumption, or appropriately qualified internal hypothesis. The [32-record register](../data/clarity-report-assumption-audit-2026.csv) contains claim, evidence, shadow assumption, alternatives, justified conclusion, decision consequence, posture and reassessment test.

This is a **critical reading of claims and accessible methodology**, not a claim to have exhaustively reproduced each underlying proprietary research dataset, inspected every full PDF, or independently recalculated its published statistics. For Chariot/K2D, we assessed the **public 2026 report promotional/summary page**; its underlying full report and raw transaction data were not reproduced in this audit. For peer-reviewed succession research and GivingTuesday, we examined the detailed openly accessible HTML methodology and limitations. For the annual DAFRC study we examined the Spring 2026 revised online summary and our already indexed data; direct raw sponsor-year microdata has **not** been downloaded. This distinction is necessary before claiming any methodological failure of an author.

## A. What Clarity changes

The canonical [Clarity Framework](https://github.com/kemiller2002/clarity-framework/blob/main/README.md), [assessor guide](https://github.com/kemiller2002/clarity-framework/blob/main/docs/assessor-guide.md) and [result template](https://github.com/kemiller2002/clarity-framework/blob/main/docs/templates/clarity-result-template.md) ask:

1. What claim is being treated as true? Is it the publisher's actual claim, a headline simplification, **our** inference, or a normative preference?
2. What evidence supports it, from **exactly which population, time frame, legal entity, instrument and denominator**?
3. What must additionally be true for that evidence to support the next conclusion? Which assumptions are explicit and which remain shadow assumptions?
4. What are the strongest plausible alternatives, selection mechanisms, or counterexamples?
5. Is confidence proportional to evidence *and the consequence of error*? Is the contemplated action correctable?
6. What should be monitored, by whom, with what threshold? What would cause reassessment of the claim **or the trigger itself**?

We must distinguish **descriptive truth, causal explanation, commercial conclusion and normative judgment**. A donor study can measure a truthful correlation while its promotion implies an unproven cause. An excellent report can also be misused by a reader who removes its caveats. Do not assign a report a simplistic pass/fail or arbitrary numerical Clarity score.

**Issue categories in the matrix:** \`publisher_claim_overreach\` is reserved for an external public-facing assertion that appears stronger than its presented evidence; \`downstream_generalization_risk\` means the publisher's original scoped statistic should not be exported elsewhere; \`methodological_scope_risk\` / \`model_measurement_risk\` refer to known data boundaries; \`normative_assumption\` denotes transparent value judgments; \`hypothesis_needing_test\` is an internal proposal; \`well_qualified_dont_extend\` highlights an assumption **we already expressly rejected**, not an error in our original report.

## B. Major findings across external reports

| Report / accessible evidence | Finding the report actually supports | Assumption at risk | Best current understanding |
|---|---|---|---|
| **2026 K2D/Chariot fundraiser summary** [C21] | Selected nonprofits recorded a large increase for donors who switched to DAF giving | DAF use **caused** net total charitable giving to increase | Reported donor/nonprofit association; **no donor-wide causal incrementality estimate** established [A001] |
| **K2D/Chariot** [C21] | Participant DAF revenue median +75%, nonDAF +9% | DAFs grew faster than *all* giving vehicles nationally | Sample channel comparison, not representative giving-vehicle ranking [A002] |
| **K2D/Chariot** [C21] | DAF-identified donors had a 13-point retention difference at participant nonprofits | DAF platforms have superior customer retention, or DAFs cause loyalty | Recipient-side correlation, **not sponsor/software retention** [A003] |
| **DAFRC Annual Report, Spring 2026 revision** [C01] | 3.59m FY2024 reported accounts, with donation processors dominating account growth | They are 3.59m independent invested/advised DAF funds or enterprise SaaS clients | National sponsor account tally, not vendor TAM [A005] |
| **DAFRC** [C01,C06] | Aggregate FY2024 DAF payout 25.2% | Median individual DAF account distributes 25.2% annually | Different aggregate vs account-level weighting and time periods [A006] |
| **DAFRC longitudinal donor/account research** [C06] | 22% of sampled accounts made no grant in most recent three-year period to 2022 | 22% of all 2026 accounts are dormant; inactivity implies tax abuse | Sampled historic behavior only, no moral/compliance conclusion [A008] |
| **DAFRC manager survey** [C08] | 86% of managers *felt* highly effective at grant review | Grant vetting is fast, cheap, error-free, or solved | Self-perceived effectiveness does **not** measure operational economics [A010] |
| **DAFRC donor/advisor research** [C06,C07] | Donor survey 9% outside DAF investment manager; adviser survey 669 respondents | Only 9% use philanthropy advisors or 75% of advisor discussions become funded DAFs | Three different denominators: investment management, advice conversation, conversion [A009,A011] |
| **GivingTuesday ecosystem 2026** [C02,C03] | Exploratory place-based concentration and support patterns in modeled IRS data | Geographic proxy equals where charities serve all beneficiaries | **Fewer than one-third** reliably geographically placed; true service coverage unknown [A012,A013] |
| **GivingTuesday ML annotation** [C03] | Model-inferred cause/beneficiary fields with confidence | Confidence scores are calibrated ground truth and stable across groups | Validate by cause, geography, size, missingness and drift [A014] |
| **Urban Institute 2026 disruption survey** [C04] | 49% of *government-funded charities* in study scope had 2025 funding disruption | 49% of every US nonprofit had one; DAFs cured the shock | Defined weighted survey universe, no observed DAF intervention [A015,A016] |
| **NBER tax-incentive study** [C09] | Econometric estimate that TCJA diminished *general charitable giving* | This establishes a specific 2026 DAF feature's net incremental grants | Strong general tax-response literature, **not DAF-specific experiment** [A017] |
| **Succession/intergenerational paper** [C15] | Among accessible policies, 96% successor advisers / 48% named beneficiary options | Rates describe every sponsor and exact donor use | Different policy-specific denominators and nonrandom missingness; ethical framing explicitly normative [A018,A019] |

**Two distinct critiques of K2D/Chariot:** The public-facing page itself uses a causal formulation about DAFs increasing individual giving [A001]. In the underlying selected transaction records, a real increase *could* exist; no error in the underlying calculation is demonstrated. By contrast, even a causally cautious description of the 13-point donor-retention difference could still be misappropriated by a third party as software-company NRR [A003]. Only the former is flagged as **publisher-level overreach on the inspected landing page**.

**Two examples of authors explicitly getting the epistemics right:** DAFRC's Spring 2026 site acknowledges changed classifications and says the revision replaces earlier FY2024 results; GivingTuesday explicitly describes geographic missingness, shortcomings of Form 990 and the risk of releasing sensitive inferred demographics. We should **preserve those authors' caveats, not claim they hid them**.

### Especially important technical corrections

- **The "96% successor / 48% beneficiary" comparison has unequal denominators.** In the open-access policy paper, successor advisers were allowed by **114/119 policies with observable yes/no information** and charitable beneficiaries by **48/101 observable policies**, against a total sampling frame of **158 organizations** with substantial missingness. The authors themselves note policy availability is not missing at random [C15]. Our final report must retain denominators and not imply 48% of all US sponsors categorically disallow a charitable beneficiary.
- **A 2026 Urban statistic needs two denominator labels.** The report estimates **49% of respondents receiving any government funding** experienced a 2025 disruption, equivalent to **35% of nonprofits overall within its nationally weighted eligible operating-charity universe**. Its frame excludes several classes such as churches, hospitals, private foundations and higher education [C04]. We cannot apply it directly to every DAF grantee without an entity crosswalk.
- **A 2026 GivingTuesday map is not a DAF grant map.** Even if lower private grant support and geographic needs correlate in some areas, the report does not identify the portion made through DAFs or establish what share reached the actual service beneficiaries. A DAF-specific impact conclusion requires *grant recipient and service-area evidence*, not just headquarters ZIP or NTEE code.

## C. Clarity assessment 1: Does DAF use **cause** more individual giving?

### Executive Understanding
**The observed improvement in recorded donations among DAF-switching donors does not, by itself, establish a causal increase in donors' total charitable giving.** K2D/Chariot's 2026 public summary says 50,000 existing donors in 54 participant organizations switched channels and recorded substantially increased giving [C21]. Its landing page uses a broad causal headline, and advises nonprofits to adopt a DAF button.

### Clarity Snapshot / Current Understanding
A larger gift to an observed nonprofit after a donor shifts to a DAF is a meaningful fundraising observation. **"More to one recipient"**, **"more across recipients"**, **"more in a given year"**, **"more across the life of the donor"**, and **"caused by the DAF"** are five separate propositions. The page does not present a donor-wide causal counterfactual.

### Evidence Landscape
- K2D/Chariot 2026 published promotional summary, participant nonprofit donation histories and 54-organizational sample [C21].
- A nonDAF comparison group and historical adjustment may be available in the full report, but **we have not independently reproduced its models**. Do not claim the full report has no controls solely from a marketing webpage.
- DAFRC older donor microdata [C06] confirms that timing and account-level giving can vary, but is not an independent causal replication of this study.

### Assumption Landscape
1. **Selection**: Donors who adopt DAFs may be entering a higher-giving life stage before channel selection.
2. **Time**: The first DAF contribution or grant after an asset sale might be a one-time spike, not persistent giving.
3. **Accounting**: Giving at nonprofits in the participating dataset is an incomplete view of all individual donations.
4. **Causal arrow**: Donor intention to increase giving could cause *both* DAF choice and higher donations, rather than the reverse.
5. **Identity matching**: DAF grants can be anonymous or have imperfect CRM linkage, affecting numerator and cohort construction.

### Calibration and Correctability
**Descriptive result:** reasonably credible within the authors' stated 54-participant sample, conditional on dataset and classification validity. **Causal contribution:** not established from the accessible public summary. **Correctability:** low if mistaken incrementality is used to justify tax subsidies or large irreversible product spending. **Posture:** Strategic for a policy/tax conclusion, Experimental for a bounded nonprofit DAF-channel optimization trial.

### Monitoring and Reassessment
**Signals:** donor-total charitable dollars across channels; pre-switch trends; non-switcher comparison; donor-level grant-year and 3-year sums; income/wealth events if legitimately available; recipient matching/opt-out rates.  
**Trigger:** a preregistered controlled/matched analysis finds a durable differential in donor-total giving *net of substitution*, robust to selection and timing; or finds no difference.  
**Trigger claim:** recipient-specific observed changes can be distinguished from counterfactual donor-wide changes.  
**Trigger reassessment:** if data linkage omits a large or systematically different donor segment, replace the estimated effect and monitoring threshold.

### Learning Priority and Current Best Understanding
Obtain an authorized, privacy-safe longitudinal donor panel across giving channels and a credible non-switcher comparison. **Current conclusion:** DAF switching is *associated* with recorded gift increases among selected nonprofits; any stronger causal or national conclusion is pending.

---

## D. Clarity assessment 2: Do DAF grants correct philanthropic geographic underservice?

### Executive Understanding
GivingTuesday's 2026 report makes an important case that charitable and civic infrastructure does not always align with deprivation [C02,C03]. **It does not yet establish where DAF grants are directed relative to unmet need.**

### Clarity Snapshot / Current Understanding
The 990-derived geographic study is an **exploratory landscape of nonprofit organizations and funding**, not the national DAF grant-recipient graph or a direct map of beneficiaries served.

### Evidence Landscape
The openly published methodology says **fewer than one-third of organizations can be geographically located by described service area**. Headquarters mailing address is insufficient; multi-region charities and unregistered mutual aid groups are incompletely observed [C02,C03]. The authors openly acknowledge this.

### Assumption Landscape
- Inferred home ZIP coincides with the place beneficiaries are served.
- Missing organizations are geographically representative.
- Cause coding captures actual services and subpopulation needs accurately.
- Relative private grants approximate relative DAF grant availability.
- Government grant offsets to larger entities effectively satisfy needs of small or emerging local groups.

### Alternative Explanations
A national nonprofit headquartered in a major city may serve underserved rural areas. Conversely, a locally headquartered organization may serve outside its ZIP. Government funding and civic institutions might crowd in or out private funding depending on institutional capacity. Observed grant funding per 990 does not identify need met or the **marginal impact** of an additional DAF grant.

### Calibration, Correctability, Posture
**Confidence:** high that the report provides a transparent, technically interesting proxy with major explicitly acknowledged missingness; low that it can directly predict DAF program impacts without new data.  
**Posture:** Experimental for exploration of inequity hypotheses; **Guardrail** for publishing any place-specific claim of underserved DAF beneficiaries or targeting interventions.  
**Correctability:** wrongful regional targeting or unsupported stigmatization of small organizations can cause material harm.

### Monitoring, Triggers and Learning
**Signals:** nonprofit operational service geography, actual recipient EIN/locations, cause-code validation, geographic sample response and DAF grant-flow data.  
**Trigger:** held-out ground-truth studies show adequate positive predictive value for the geographic use case and linked DAF grant data demonstrate gaps persist under alternative geography allocations.  
**Trigger reassessment:** sensitivity to omitted groups changes the identified "underserved" region rankings materially.

**Current conclusion:** A valuable **research hypothesis** about geographic need, **not yet an established DAF allocation failure or solution**. EDF should diagnose an actual localized funding bottleneck only after an observed outcome is available.

---

## E. Clarity assessment 3: Should donor-engagement technology outrank AI grant vetting?

### Executive Understanding
Our own research [\`daf-market-demand-and-evidence-gaps-2026-11-11.md\`](daf-market-demand-and-evidence-gaps-2026-11-11.md) uses DAFRC sponsor-manager survey evidence [C08] to propose investigating donor-engagement tools before committing to standalone AI grant-vetting software. This is a **reasonable research priority, not a verified market opportunity ranking**.

### Clarity Snapshot / Evidence
The 2023 manager survey's 128 respondents report higher perceived effectiveness at grant review (86%) than at contribution solicitation (34%). Only 52% consider staffing sufficient, and 61% IT sufficient [C08]. These metrics differ in question wording and task complexity; they do not measure **hours of manual review, serious errors, approved grants, donor conversion, buyer willingness to pay or product gross margins**.

### Hidden Assumptions
- Subjective perceived effectiveness is inversely proportional to unmet software value.
- Poor solicitation effectiveness is correctable by a software workflow, rather than institution strategy, donor supply or advice skills.
- Sponsors can and will procure a new product despite staffing or budget constraints.
- More contribution activity is appropriate even for donors for whom **direct giving or no DAF** is better.
- A multi-step "decision-to-outcome" platform is less costly than specialist components and existing procurement.

### Alternatives and Counterexamples
Highly effective grant reviewers may still be costly and manual. A new integration can shift work rather than reduce it. Donor engagement initiatives can increase DAF conversions while lowering donor suitability. A provider can have excellent grant controls but weak sales because its sponsor is regional or intentionally specialized.

### Calibration / Correctability
**Descriptive survey:** justified with sample limits. **Comparative ROI/product choice:** unsupported. **Posture:** Experimental. Avoid Strategic capital commitments. A narrow research or workflow pilot is inexpensive to correct; building an entire software platform would not be.

### Monitoring / Reassessment
**Signals:** actual handling cost by function, sponsor procurement ranking, signed buyer budget, 2026 donor decision outcomes, cost per completed lawful grant, participant quality, pilot effect.  
**Trigger:** representative sponsor buyers' observed willingness to pay and error/cost impact favor an intervention after full labor and implementation costs; or show grant review more valuable than engagement.  
**Trigger reassessment:** the initial sponsor sample overrepresents users who already implemented grant automation or the 2023 survey no longer describes market needs.

### Current Best Understanding
**Test the engagement hypothesis first because it is underexplored and potentially inexpensive to falsify, not because we have proven it is commercially superior.** Any claim that Clarity+EDF improves decision accuracy also remains an untested product hypothesis until an independent blinded comparison is performed [I002,I011].

---

## F. Our own earlier research: audit results, not retroactive rewriting

The [32-record matrix](../data/clarity-report-assumption-audit-2026.csv) includes **12 internal** points. Several are **correctly constrained in the existing reports**; retaining those qualifications is part of research quality:

| Our report | Current justified conclusion | What would invalidate an overreach |
|---|---|---|
| **Audited Ren fee history** | RCF paid Ren $19.23m in FY2024; service relationship observed | Inferring Ren consolidated recurring revenue, profit, company concentration or organic growth from one payer's fees [I004] |
| **Ren public MSA study** | Published unsigned standard service template contemplates annual renewals | Assuming signed enterprise work orders use these provisions or measuring actual churn from templates [I005] |
| **Foundation Source competitive map** | Verified technology acquisitions and named institutional partners | Treating distinct acquisitions as a technically integrated profitable product or proof of actual won contracts [I003] |
| **Sponsor governance study** | Board/vendor overlap and conflict policies disclosed | Assuming the overlap establishes unapproved related-party contracts or wrongdoing [I006] |
| **Charityvest bridge** | $811,940 is sponsor total **non-grant expense**, not named provider payment | Reclassifying it as Foundation Source technology ARR or a complete cash payment ceiling [I007] |
| **TIFIN tax opportunity** | More explicit public claim of automated lot detection than accessible Ren evidence | Claiming TIFIN's real engine is more accurate or Ren lacks private features [I008] |
| **18 synthetic tax tests** | Independent limited reference arithmetic, **zero live vendor runs** | Claiming any vendor passed tax accuracy or security [I009] |
| **Decision Intelligence pilot** | Three worked, manually authored examples show framework application | Claiming measured superiority, reliable autonomous reasoning, or validated calibration [I002,I011] |

**Possible corrections in the final comprehensive report:** Avoid presenting a vendor relationship graph as a revenue-flow network unless an actual payer/payee amount is known. Avoid making product prioritization sound settled. Label standard MSAs, tax cases, and financial sensitivities by what they **do not** prove. Do not remove contrary evidence merely because the narrative is compelling.

## G. Research conclusions with decision posture

1. **Not justified:** "DAFs cause increased total charitable generosity" from K2D/Chariot's publicly reported switcher comparison alone. **Strategic** posture for tax-policy or investment commitments; **Experimental** for a small fundraising test.
2. **Justified descriptively, not causally:** Donation processors heavily influence reported DAF account growth. Market sizing requires sponsor-year and contract-level segmentation. **Guardrail** against invalid denominators; **Strategic** for capital allocation.
3. **Not justified:** "Donor loyalty lifts DAF platform NRR by 13 points." Wrong unit of retention entirely. **Guardrail** in any investor deck.
4. **Provisional:** Geographic philanthropic underservice observed in modeled nonprofit 990 data could motivate new DAF allocation research, **not a published DAF grant discrimination conclusion**.
5. **Provisional:** Sponsor/recipient operations and informed donor engagement may offer better software differentiation than another AI vetting dashboard. Product investment requires actual cost, quality and customer adoption.
6. **Not justified:** Ren vs Foundation Source profit ranking from audited RCF transfers and Charityvest total overhead. Better comparative disclosure for Ren's one relationship is **not** a company profitability advantage.
7. **Justified, bounded:** 2025 government funding disruptions and succession-policy options create useful testable DAF policy questions; neither research item directly proves DAF mitigation or actual succession behavior.
8. **Provisional:** A Clarity+EDF conclusion registry may improve decision quality. We **cannot** claim superiority until unbiased held-out comparisons and practical user outcomes are measured.

The **report's differentiation** should be a transparent chain:

**Source observation → scoped claim → hidden assumptions → rival explanations → current justified understanding → confidence/impact/correctability → action → falsifier/reassessment signal**.

This is not a universal algorithm for calculating social impact. Different causes, donor intent, years, policies and stakeholder values may genuinely conflict. The point is to make those conflicts visible and testable rather than hiding them behind a single vendor or impact score.

## H. Quality-control protocol for future comprehensive-report chapters

Before a chapter's conclusion is accepted, require:
- Exact **quote context/position** from a publicly accessible source and copy-independent paraphrase; label publisher vs analyst inference.
- Defined sponsor EIN / vendor entity / donor / nonprofit recipient / year / method / unit.
- A source and denominator for **every numeric assertion**, including sample and missingness.
- At least one **meaningful counterargument or alternative causal model**, not an AI-generated straw man.
- Written distinction between descriptive, causal, normative, contractual and tax/legal claims.
- Evidence posture with **impact if wrong** and **correctability**, per Clarity's actual posture model.
- Triggers and owner for reviewing the conclusion when new data arrive, plus conditions for reassessing the trigger itself.
- No false independence: multiple AI personas reading the same publication do not independently replicate a study.
- A visible **"not established"** result where the requested conclusion cannot honestly be supported.

**EDF is optional and downstream of the Clarity depth decision.** Use it when there is an actual observed outcome requiring a causal origin/propagation/control analysis. Do not force EDF to invent mechanisms for a vendor economics comparison that has no observed profit outcome.

### Follow-up research priorities

1. **DAF causal incrementality:** Acquire consented donor-total longitudinal grant/gift data and matched controls for switching channels.
2. **Account-type taxonomy:** Download the DAFRC Spring 2026 revised raw sponsor-year data to separate donation processors and invested funds; reconcile historic source vintages.
3. **DAF geographic impact:** Link actual DAF grant-recipient EINs to independently validated nonprofit service geography and community-needs data, with sensitivity to unclassified organizations.
4. **Operating cost vs buyer need:** Real sponsor time/cost and sponsor procurement outcomes across grant vetting, donor engagement, investment accounting and recipient receipts.
5. **Tax and succession policy counterfactuals:** Include direct giving, no-DAF options, future recipient needs, actual successor elections and distribution deadlines.

The [39-topic comprehensive research coverage map](../data/comprehensive-daf-research-coverage-2026.csv) allocates chapters across market structure, financial economics, donor behavior, nonprofit outcomes, public policy, technology and future risks; the [27-source discipline register](../data/comprehensive-research-source-catalog-2026.csv) anchors the new expansion. These are **planning and source registers**, not independent execution results.
