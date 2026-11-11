# Decision Intelligence pilot: three real DAF conclusions

**Analyst-produced pilot, 2026-11-11. Not automated. No statistical confidence calibration, executed causal experiment, proprietary product test, real financial customer cohorts or regulatory opinion.** The aim is to demonstrate a defensible decision that is **not a rewritten data table**.

These cases depend on the actual [Clarity Framework](https://github.com/kemiller2002/clarity-framework/blob/main/README.md) and [EDF working v0.3 specification](https://github.com/kemiller2002/echelon-diagnostic-framework/blob/main/docs/edf/specification.md). EDF is used only when the question presents an observable outcome and benefits from causal modeling; Clarity governs justified understanding, appropriate commitment and reconsideration.

## Case DI-001: Should we make AI grant vetting our differentiating product?

### Evidence landscape
- [DAFRC sponsor manager survey, 128 respondents in 2023, published 2025](https://static1.squarespace.com/static/6011def87418a462fcb03978/t/67d8840c07c0bb1803701594/1742242829111/Executive%2BSummary%2BThe%2BNational%2BSurvey%2Bof%2BDonor%2BAdvised%2BFund%2BManagers.pdf) [B05] says **86%** self-rate grant review very/extremely effective [M21], **34%** say that about DAF contribution solicitation [M23], **55%** philanthropic advice [M22], **52%** say staffing sufficient [M20], **61%** IT sufficient [M19].
- These are **perception ratings**, not time/cost records, failure metrics or causal evidence; the sample is voluntary and older than the current procurement market.
- **Potential counterevidence:** Very high perceived effectiveness could coexist with high staff costs, inconsistent recipient validation or poor error recovery. A new grant workflow might be valuable, but it needs actual problem evidence, not vendor marketing.

### EDF-1: bounded diagnostic sketch

**System Context**
- **Primary System:** DAF sponsor's contribution/engagement, donor-advice and grant-review operation.
- **Context:** 2023 self-reported management practices across 128 selected sponsors; no single firm or modern software platform measured.
- **Focus:** *Observed differential in management confidence across operational functions*, not grant vetting's actual cost/quality.

**Outcome:** In this survey, 86% report highly effective grant review but only 34% highly effective contribution solicitation and 55% highly effective advising. This is a **survey outcome**, not a confirmed failure of all DAF sponsor processes.

**Manifestations:** 52% say staffing sufficient and 61% IT sufficient; a mismatch between high-rated processing and weaker relationship-oriented functions.

**Origin Network:** **Not established.** Candidate explanations include resource allocation, less standardized donor engagement work, weaker advisor integration, and perception/reporting bias. None has been causally tested in this dataset.

**Propagation:** **Proposed pathways only:** staff capacity/fragmented donor information may hamper follow-up and contribution solicitation while standardized rule-based grant review appears mature. No actual sequence of events has been observed.

**Evidence:** B05, M19–M23. Mixed observation and hypothetical mechanism explicitly separated.

**Candidate Control Points:**
1. Direct measurement of staff minutes and exceptions in grant review versus donor/advisor engagement.
2. Sponsor and adviser interviews about purchases actually deferred or approved.
3. A small consent-respecting engagement/workflow prototype compared with baseline.
4. Grant-review automation **only if actual cost, latency or control deficits are confirmed**.

**Control Point Ranking:** First measure actual costs and bottlenecks (high decision information, low cost, high correctability); then test one targeted engagement or reconciliation process; defer large build. Not a numerical ranking.

**Confidence:** **Moderate** that the *survey showed this difference*; **low** confidence that any proposed cause explains real sponsor bottlenecks in 2026.

**Diagnostic Sufficiency:** **Enough for bounded discovery**, not for selecting a permanent differentiated product.

**Unknowns:** Actual labor/exception cost by function, sponsor selection bias, grant accuracy, buyer budget, donor value and which intervention creates lift.

**Next Responsible Action:** A 5–10 sponsor/wealth buyer discovery sample and a quantified time/exception study. Do not start an AI vetting platform merely because it sounds technically sophisticated.

### Clarity Result

- **Executive Understanding:** Grant vetting is plausibly not the first unsolved need for many sponsors, but the surveyed perception gap **does not establish the best commercial product opportunity**.
- **Clarity Snapshot:** Sponsor manager self-ratings favor existing grant review over donor solicitation; no actual operating-cost or willingness-to-pay data.
- **Evidence / Assumptions:** Survey B05 supports the observed difference. Assumes enough of the current market resembles respondents for the finding to inform hypothesis selection; **not established**.
- **Calibration:** Qualitative *moderate* confidence in descriptive finding, *low* in commercial inference. No artificially precise probability.
- **Correctability:** A limited research/prototype program is reversible and cheaper than a full platform.
- **Recommended Posture:** **Experimental**. Testing a product hypothesis is justified; irreversible strategic investment isn't.
- **Current Best Understanding:** Prioritize **testing** engagement, account follow-up and end-to-end grant reconciliation ahead of committing to a standalone AI grant-vetting engine.
- **Reconsideration trigger:** A representative current sponsor sample reveals that grant review has demonstrably high correction labor, material delays, costly false positive/negative decisions, or a signed procurement willingness to pay **more** than engagement tools.
- **Consequence owner:** To be assigned by research/project owner before prototype spending.

**Conclusion card:** **Investigate donor engagement and end-to-end exceptions before building another grant vetting feature.** This is a conditional research priority, **not a proven market ranking**.

---

## Case DI-002: Are 3.59 million DAF accounts the enterprise software addressable market?

### Evidence landscape
The [DAFRC Spring 2026 revised FY2024 report](https://www.dafresearchcollaborative.org/research/annual-daf-report) [B01] finds **1,512 U.S. sponsoring charities** managing approximately **3.59 million reported DAF accounts**, **$327.87 billion** charitable assets, and **$64.60 billion** grants [M01–M05]. The authors explicitly say account growth was driven primarily by **donation processors**, and distinguish these from other national sponsoring charities.

### EDF-0: narrow count-meaning diagnosis

**System Context:** U.S. reported FY2024 DAF accounts (primary system: national sponsor-account reporting; context: IRS Schedule D classification and donation processors; focus: meaning of count when sizing a technology market).

**Outcome:** DAFRC reports about 3.59 million accounts; a single total spans meaningfully different product/business models.

**Manifestations:** Donation processors drive the count's growth; 103 national, 803 community and 606 single-issue legal sponsors [M07–M09]. A charitable account is not a paying enterprise technology customer.

**Origin Network:** **Documented classification heterogeneity** across legal sponsor programs and donation-processing services [B01]. The precise processor account count is not computed in `daf-landscape` yet.

**Propagation:** Aggregation of unlike account types makes the top-line count unsuited to an assumption of uniformly invested, advisor-managed accounts. Multiplying all accounts by one software price propagates a denominator error into TAM.

**Evidence:** B01 and M01–M09.

**Control Points and ranking:** (1) Download revised DAFRC sponsor data, (2) classify donation processors and sponsored asset/account types, (3) identify paying enterprise contracts. Their priority follows dependencies, not subjective attractiveness.

**Confidence:** **High** in the *published FY2024 total and report's own classification caveat*; **not established** for independent invested accounts or paying customer counts.

**Diagnostic Sufficiency:** **Yes to reject the naive market sizing extrapolation**. **No to publish an actual enterprise software TAM**.

**Unknowns:** Active investment-advised accounts, sponsor/vendor procurement penetration, recognizable vendor fee base.

**Next Responsible Action:** Build a sponsor-year segmented mart from the official revised dataset.

### Clarity Result

- **Current Understanding:** 3.59 million is a sponsor-reported **DAF account aggregate**, not a vendor software customer measure.
- **Justification:** DAFRC's own revised report states processor-driven growth and separates sponsor categories [B01].
- **Assumption / Counterargument:** Some donation processors do use sophisticated third-party technology. Excluding them from every software market would also be wrong; the necessary separation is by **buyer/product/economic unit**, not a universal ban.
- **Impact / Correctability:** An erroneous TAM sent to investors could cause consequential capital commitments and be difficult to unwind.
- **Posture:** **Strategic** for investment TAM decisions; a reversible **Experimental** activity is justified for collecting and reconciling source data.
- **Current Best Understanding:** The total **cannot be used as a proxy for purchased institutional DAF software market size**; we cannot presently give a numeric enterprise TAM.
- **Reassessment trigger:** Versioned, sponsor-level DAFRC records and matched platform revenue contracts make the market denominator estimable and reproducible.

**Conclusion card:** **Reject the 3.59 million × average software fee TAM shortcut.** Segment sponsor/accounts and paid technology contracts before valuation.

---

## Case DI-003: Does Ren's audited RCF fee stream prove higher profitability than Foundation Source?

### Evidence landscape
- [Audited RCF→Ren fee history](../data/rcf-ren-audited-admin-payments-2020-2024.csv), citing [FY2024/23 independent RCF statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf) [F01], shows **$19,225,546 FY2024 paid by RCF to Ren** for broad administration. This is a **named payee/sponsor expense**, not Ren's total company revenue or profit.
- [Charityvest 2024 sponsor expense bridge](../data/charityvest-provider-payment-bridge-2026.csv) [V03,V04] records **$811,940 total expenses other than grants** in the public Form 990 extracts, **not an established payment to Foundation Source**. Actual Foundation Source payee-specific amount remains unverified.
- The operating models, customer bases and cost centers differ; neither vendor's full audited operating cost/profit records or matched cohort retention is available in these sources.

### Clarity-only assessment: diagnosis would overstate the evidence

There is **no observed vendor-specific profitability outcome here requiring an EDF origin network**. The issue is a *comparison that is not supported by its measurement units*. Do **not** force an EDF-2 investigation or invent an explanation of why a particular firm's profit is higher.

- **Claim assessed:** "Ren is more profitable than Foundation Source because RCF pays Ren $19.23m and Charityvest reports $0.812m of non-grant expense."
- **Status:** **Insufficient / comparison not justified**. Numerator of one named service-provider payment is not comparable to the entire other charity's non-grant expense residual.
- **What is established:** RCF's audited Ren payment. Foundation Source is a documented Charityvest technology/administration partner, but amount paid and company margins are **unknown**.
- **Strongest possible alternative:** Foundation Source might operate at lower per-account cost or have profitable other clients; Ren might capture higher gross payments but incur greater people/operations costs; or the reverse. Current data do not discriminate among them.
- **Confidence:** High that **the comparisons are invalid**, not high confidence about either company's actual profitability.
- **Impact / Correctability:** Company valuation or acquisition thesis is high-impact, difficult-to-correct if based on false accounting equivalence.
- **Posture:** **Strategic** for capital allocation. Continue bounded **research/discovery**, not a ranking or investment commitment.
- **Learning priority:** Obtain (1) Charityvest's actual 2024 audited note or named vendor payment register, (2) Ren and Foundation Source company-recognized recurring revenue by SKU/customer, (3) direct cost of delivering contracted services and (4) customer retention.
- **Reconsideration trigger:** Audited/reconciled **same-period** vendor revenue and service costs, across **the same defined product and payer types**, with independent control of acquisition/related-party entries.
- **Consequence owner:** Investment decision-maker not yet designated in the `daf-landscape` project.

**Conclusion card:** **Ren has a verified material sponsor-admin fee stream. We cannot conclude it is more profitable than Foundation Source.** The economically honest answer is a counterparty-specific fact and a specific hold on comparative profitability.

---

## What these three pilots demonstrate

| Dimension | Raw research alone | Combined diagnostic/decision result |
|---|---|---|
| Supplier product opportunity | 86%, 34%, 52%, 61% survey table | **Experimental** posture: investigate engagement/exception workflows before committing to grant-vetting AI |
| Software market | 3.59m aggregate DAF account count | **Reject invalid TAM** until sponsor/processor and actual paying technology-contract units are separated |
| Vendor economics | $19.23m audited service fee vs $0.812m charity overhead | **Do not rank profitability**; specify named payee/recognized revenue and cost-to-serve proof required |

**Differentiation:** The outputs prohibit attractive unsupported extrapolations, prioritize discriminating tests, and make decision reversal explicit. They are **examples of better reasoning**, not yet proof a software product can do it reliably.

**Method validation:** Pre-register a blind reviewer trial comparing these outputs against a baseline data summary and an ordinary vendor ranking. Use held-out cases and wrong-denominator adversarial tests; check errors and reviewer actions, not eloquence or number of fields. Failure to improve judgments means the additional framework layer should remain a research candidate.

**References:** [Decision Intelligence architecture](decision-intelligence-architecture-2026.md), [18-source demand register](../data/market-demand-evidence-sources-2026.csv), [27-gap backlog](../data/decision-critical-data-backlog-2026.csv), [regression cases](../data/decision-intelligence-regression-cases-2026.csv).

_Pilot authorship and confidence labels reflect analysis only. Vendor testing, independent calibration and regulatory/tax advice were not performed._
