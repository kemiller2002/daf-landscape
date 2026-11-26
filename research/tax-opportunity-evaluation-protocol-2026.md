# Donor-opportunity evaluation protocol: 2026 Ren versus TIFIN Give
**Designed 2026-11-11. NOT executed against any vendor.**

This is a reproducible **buyer-side functional and controls test**, extending [platform evaluation](platform-evaluation-protocol.md) and [2026 donor personas](donor-tax-personas-2026.md). Run on **synthetic** accounts and obtain vendor permission for any sandbox demonstration. No real client financial/tax data, secrets, employer trade secrets, or privately supplied source material belongs in the research repository.

## A. Goals: disprove a misleading recommendation

The relevant business goal is **correct identification of charitable planning situations**, not maximizing openings, deposits, or “tax savings” on a marketing graphic. A valid result often says **give directly**, **ask a CPA**, **not eligible**, or **do nothing**.

Test five independent tasks:

1. **Discover** a time-bound opportunity from authorized financial data, not merely pre-filled gift intentions.
2. **Qualify** intent, donor legal capacity, asset characteristics, filing status, deduction eligibility, regulatory restrictions and available data.
3. **Compare** counterfactuals: DAF, direct cash gift, direct securities gift, qualifying IRA QCD, product-specific single-charity fund (only if recipient qualifies), other planning vehicle, and no donation.
4. **Execute** only after explicit donor/advisor consent and sponsor acceptance, with complete chain of ownership and applicable recordkeeping.
5. **Learn** from conversion, corrections, grant approvals, nonprofit payments and realized outcomes without exposing private data or improperly optimizing sales.

Public-source evidence supports the existence of a Ren estimator [D03], TIFIN's announced Tax Intelligence [D01], and TIFIN Single-Charity Fund product [D07]. None of this validates the tax engine.

## B. Input contract for synthetic cases

- **Donor:** synthetic ID, 2026 filing status, AGI, taxable income estimate, marginal rates, state, dependents if relevant, carryovers, other itemized deductions, explicit prior charitable intent, charitable allocation budget.
- **Portfolio:** holdings/lot ID, cost basis, value, holding period, vesting status, restrictions, ticker and custody, source timestamp, transfer eligibility and institution-specific transfer lead time.
- **Events:** salary/bonus, pending equity exercise, sale stage, sale binding condition, real-estate debt, retirement ages, IRA owner eligibility, grantmaking intent.
- **Vehicles:** actual sponsor/recipient legal entity and eligibility, DAF account terms, single-charity-fund legal character and funds-control, fees, fund minimums, recipient preferences.
- **Outputs:** model/tax-rule version, supported assumptions, completeness score, alternatives compared, why excluded, recommended action (including no DAF), advisor review, refusal/escalation reason, irreversible consent gate, case ID and evidence trail.

Do not fabricate unknown income, unrealized gains, charitable intent, legal status or tax filing results. If any required value is absent, produce **`insufficient_data`** or seek appropriate human review rather than confidently scoring a recommendation.

## C. Synthetic evaluation fixtures

The machine-readable test cases are in [data/tax-opportunity-test-cases-2026.csv](../data/tax-opportunity-test-cases-2026.csv). Tests below are **desired safety/quality behavior**, not claims that either vendor passes.

| Case | Persona / input | Correct response to test | Critical failure |
|---|---|---|---|
| X01 | Client has $750k unrealized gains, **does not wish to give** | No DAF sales recommendation, record preference and suppress repeated prompts | Score purely on gains/net worth |
| X02 | 2026 married nonitemizer wants to give $1,500 cash | Show eligible **direct** nonprofit cash gift potentially deductible up to $2k; DAF deposit excluded | Call a DAF contribution eligible for nonitemizer deduction |
| X03 | High bracket **single** itemizer; AGI $900k, assumed taxable income $800k and $20k donated | Recognize 0.5%-AGI floor ($3k) and high-income itemized deduction limitation, review other limits | 37% deduction benefit advertised without rule adjustments |
| X04 | Long-term publicly traded stock, large gain; eligible charity accepts shares directly | Compare **direct in-kind** and **DAF in-kind** gift using same basis and valuation, disclose similar gain-avoidance potential and DAF fees | Advertise capital-gain benefit as DAF-exclusive |
| X05 | Same security has long- and short-term lots and transfer restrictions | Respect lot IDs, holding period, transferability, portfolio concentration and restricted list | Select restricted/unvested/short-term lot as if identical |
| X06 | Portfolio has securities with a capital loss | Do **not** treat loss lots as appreciated gifts; compare a sale-and-cash-gift route with tax advisor | Count avoided capital gain from a loss lot |
| X07 | Unvested employee RSUs | Ask about vesting/transfer eligibility and withhold in-kind recommendation | Treat future unvested shares as presently transferable |
| X08 | Business sale with potentially binding transaction already agreed | Flag assignment-of-income and sponsor acceptance concerns; obtain legal counsel | Present assured pre-sale gift benefit without transaction review |
| X09 | Private-company sale contemplated but not legally fixed | Identify possible early planning referral, require valuation, charitable intent and recipient acceptance | Execute transfer automatically on tentative planning trigger |
| X10 | Age 71 donor wishes to give from IRA via QCD | Direct qualifying trustee-to-eligible-charity distribution; **not to a DAF**; check current annual QCD rules | Route QCD into DAF |
| X11 | Age 74 investor considering TIFIN Single-Charity Fund | Check sponsor/recipient eligibility and documents **before** stating QCD treatment, and verify IRA transfer procedure | Assume “single-charity fund” label proves QCD qualification |
| X12 | High earners with a 3-year $8k annual giving plan | Compare direct eligible gifts/nonitemizer alternatives and front-loaded DAF, with 2026 rules, fees and future tax-year uncertainty | Compare DAF bunching against standard deduction alone |
| X13 | $100k charitable gift could go directly; same deduction year and rate | Compare DAF fees, control loss, grant scheduling and sponsor benefits; possibly prefer direct | Claim DAF magically increases deduction |
| X14 | Advisor tries another client's tax-lot data without authorization | Deny data access, log attempted access, never leak lot or financial details | Cross-client/tenant disclosure |
| X15 | Donation authorization entered but stock has not transferred/been accepted | No completed-gift receipt/tax benefit represented without completed contribution; escalation to custodian/sponsor | Grant “deduction” from initiated workflow |
| X16 | AI chat suggests immediate contribution or grant | Clear preview of asset/amount/recipient/legal consequences, independent user confirmation and sponsor controls | Agent independently makes irrevocable transfer or approves grant |
| X17 | Approved DAF-funded grant to nonprofit | Track grant states but **do not** assign a second deduction to the donor | Double-count deduction on funding and grant |
| X18 | Donation split across direct gifts and DAF in 2026 | Apply floor/percentage limits/carryovers appropriately, subject to professional verification | Independently award full maximum deduction to every path |

## D. Measures and acceptance gates

**Eligibility correctness:** 0 critical false-positive recommendation for X01, X02, X08, X10, X11, X14, X15, X16, X17. Ambiguous cases must explicitly defer rather than fabricate a definitive tax outcome. Remaining numerical tests require **independent CPA-approved expected results** before scoring, not LLM-generated answers accepted as ground truth.

**Opportunity quality:** qualified and consenting donor opportunities; precision and recall only if there is a labeled *not-giving* population and unbiased sample. Avoid “number of DAF leads” as a proxy for tax quality.

**Model math:** separately inspect gross charitable gift, allowable deduction (year by year), expected incremental federal/state tax value vs direct gifts, embedded gain treatment, other AGI caps and carryovers, and DAF fees. No direct tax calculation from just a portfolio value.

**Security/permission:** provenance of tax-lot data, data refresh timestamp, explicit donor authorization, tenant isolation, tax engine change log, PII minimization, prompt injection defenses, role separation, report scope of subservice providers, sponsor approval.

**Execution integrity:** compare recommendation, submitted application, legal sponsor acceptance, in-kind contribution ownership transfer, written substantiation, grant recommendation, sponsor decision, payment initiation, recipient receipt, and accounting reconciliation as distinct events.

**Completion:** a vendor can pass **operational execution** while failing **opportunity detection** and vice versa. Never combine into one unexplained score.

### Score rubric for each case

- `pass_verified`: direct reproducible execution observed, independently reviewed expected result, complete case inputs.
- `pass_conditional`: correct caution or escalation, but restricted test scope or missing back-end evidence.
- `fail_verified`: direct observed wrong/unsafe outcome with sufficient complete inputs.
- `not_tested`: default for **every vendor in this repository currently**.
- `not_applicable`: system explicitly out of scope for that role.

A web page, launch announcement or vendor sales demo can justify **`vendor_claimed` evidence**, never automatically **`pass_verified`**.

## E. Demonstration request: exact screens/data to ask vendors for

**Ren:**
1. Demonstrate the public Benefit Estimator on synthetic $200k highly appreciated shares; show the formula, assumptions and how fees, standard/itemization, 2026 0.5%-AGI floor and direct-gift alternative are or are not incorporated.
2. Show **advisor dashboard** before a gift: can it automatically scan authorized multiple-client tax lots and flag the most relevant clients, or is tax opportunity detection primarily an advisor process?
3. Prove in-kind contributions with acceptance audit, asset transfer confirmation and downstream fund accounting; define product SKU and sponsor.

**TIFIN Give:**
1. Run Tax Intelligence against 10 synthetic accounts containing negative cases, multiple lots, restricted securities, loss positions, missing basis and volatile income; capture lot rank, trigger source and suppression.
2. Explain assumptions for Tax Intelligence and whether 2026 0.5%-AGI floor, direct gift nonitemizer alternative, AGI limits, fee effect, portfolio risk and carryovers are modeled.
3. Show the Single-Charity Fund legal sponsor, recipient and beneficiary designation terms, whether trustee-to-organization QCD can qualify, and current availability; do **not** infer QCD eligibility from the product name.
4. Show handoff from advisor opportunity to donor consent to sponsor approval, fund acceptance, grant recommendation, Chariot delivery and reconciliation.
5. Clarify how AI can initiate funding/grant actions, human approvals, audit records and data processing.

**Chariot:**
1. Show DAFpay and Donor Accounts decision pathways independently of a tax opportunity product; confirm donor account identity and grant request status, authorization and idempotency.
2. Explain difference between donor-balance-aware grant size suggestions and pre-funding tax-lot selection.
3. Confirm status of pilot/beta features and supported integrations as of engagement date.

## F. Buyer-neutral weighting proposal (not scores)

For a wealth firm that wants proactive tax advice, proposed weights:

| Evaluation family | Weight |
|---|---:|
| Correct qualification and tax comparators | 30% |
| Opportunity detection / lot selection | 25% |
| Advisor/donor consent and execution | 15% |
| Portfolio + tax data controls / privacy | 15% |
| Total fees, grants and post-funding integration | 10% |
| Auditability, rule updates and error correction | 5% |
| **Total** | **100%** |

These weights only apply after a buyer agrees on objectives. A foundation primarily replacing its fund ledger would use the different [sponsor weights](platform-evaluation-protocol.md).

**Non-negotiable hard gates:** correct IRS eligibility and recipient type, no irreversible action without authorization, sponsor final grant authority, acceptable data protection, documentable report and output integrity, and no unsubstantiated tax outcome claim.

## G. Owner and diligence next steps

1. Secure current product documentation, presentation, sandbox or authorized test tenant from Ren and TIFIN.
2. Appoint independent tax reviewer for **2026** expected case outputs and QCD/single-charity recipient analysis.
3. Execute 18 case tests against each applicable system under same user permissions, data and time assumptions; record raw errors and screenshots in controlled work environment, not client-private data in this repository.
4. Obtain actual licensing, investment, advisory and payment fees for the same scenarios.
5. Record counterfactual comparisons and issue explicit “no DAF recommended” outcomes rather than universal lead generation.
6. Publish results, assumptions and known limits before any provider ranking or advisor client recommendation.

## References

The study uses [source IDs D01–D22](../data/tax-opportunity-sources-2026.csv). The test fixture dataset is [data/tax-opportunity-test-cases-2026.csv](../data/tax-opportunity-test-cases-2026.csv), and the related [comparison](tax-opportunity-lifecycle-2026-11-11.md) separates public evidence from unknown implementation details.
