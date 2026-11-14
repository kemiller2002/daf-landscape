# AI economics and replacement analysis for DAF operations

> **Red-team status (2026-11-14):** this document was independently reviewed in [red-team-wave2a-ai-and-entrant.md](red-team-wave2a-ai-and-entrant.md). The corrections in the final section govern where they conflict with the text.


**Date:** 2026-11-14. **Status:** desk research plus a transparent SCENARIO model. No sponsor operational data, no vendor demos, no measured exception rates. **Data:** `data/mission-2026-11-14/ai-process-economics.csv`, `data/mission-2026-11-14/ai-use-case-inventory.csv`. **Builds on (does not repeat):** `research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md` (exception labor formula, grant-volume baselines), `research/daf-reconciliation-economics-scenario-model-2026-11-11.md`, `research/batch-2a-…`, `research/batch-2c-…` (decision state machine, 20 synthetic cases), `research/ren-instant-grant-approval-rcf-policy-clarity-audit-2026-11-12.md` (three-metric distinction, A/B/C benchmark design), `research/tax-opportunity-lifecycle-2026-11-11.md` (TIFIN Tax Intelligence).

Notation: **[F]** = sourced fact; **[I]** = inference by this analysis; **[S]** = SCENARIO assumption or output. Every [S] number is an assumption chosen to make the logic inspectable, not an estimate of any sponsor's costs.

---

## 1. Executive findings

1. **Inference cost is not the economic constraint; oversight, integration and the size of the residual human workload are.** [F] Published Claude Sonnet 5.5 API pricing is $2 per million input tokens and $10 per million output tokens; Haiku 5.5 is $0.10/$0.50; Opus 5.5 is $4/$20; Batch API halves both ([Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), read 2026-11-14). [S] A heavy non-standard-grantee document review (60k tokens in, 3k out, ×3 for retries/agent steps) costs about **$0.45 per case** on Sonnet 5.5, versus about **$83** of reviewer time at 90 minutes and a loaded compliance-officer rate of $55.45/hour (BLS median $38.81/hour, May 2025 ([BLS OOH](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm)), grossed up by the private-industry wage share of compensation, $32.82 of $46.89, June 2026 ([BLS ECEC](https://www.bls.gov/news.release/ecec.nr0.htm))). Inference is <1% of the labor it might displace. The economic question is how much labor exists to displace and what QA it creates.

2. **For most DAF processes the most attractive intervention is redesign (D) or conventional automation (B), not AI on the existing workflow (C).** [S] In the base scenario for an illustrative sponsor with 1M grants/year, C ranks last of four interventions in all 16 processes; under optimistic AI assumptions (60% time saving, 5% QA sampling) it ranks first only for **noncash complex-asset intake (P03)**. This ranking is driven by stated assumptions (Section 5), but the structural reason is robust: AI on top of a workflow inherits the workflow's waste and adds QA, while D removes whole exception classes.

3. **Several processes should not exist in their current form; speeding them up is the wrong goal.** [I] (a) Per-grant re-verification of charity status already available as monthly IRS bulk data and the OFAC list ([IRS bulk downloads](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads); [IRS Auto-Revocation List](https://www.irs.gov/autorevocationlist)); (b) check-based disbursement and the returned/uncashed-check reconciliation it generates; (c) nonprofit-side manual DAF gift attribution caused by 1,200+ DAF providers using separate portals and formats (vendor citing DAFRC, [Chariot, 2026-01-28](https://givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits)); (d) repeated equivalency/expenditure-responsibility work on the same foreign grantee across sponsors; (e) "where is my grant" service contacts caused by opaque status.

4. **AI's best economic fit is narrow: reading unstructured documents in low-volume, high-minute, judgment-heavy work** (complex-asset gifts, non-standard grantee due diligence, succession documents, agent-assist for service contacts). Even there, [S] the AI layer's annual gross value at 1M grants (P07 base $155k; optimistic $299k) is of the same order as a plausible governance-and-integration fixed cost, so **AI pays as a shared platform across processes or at Fidelity-scale volume, not as a per-process project.**

5. **Market evidence shows no publicly evidenced AI in sponsor-side grant approval or eligibility determination.** Of 30 AI use cases inventoried, 10 are DAF-direct; of those, 6 are announced only, 1 demonstrated, 2 deployed-with-evidence (a navigation-only website assistant at Fidelity Charitable; a corporate grantmaker running agents on the donor side of a Fidelity Charitable DAF) and 1 unverified. The most agentic DAF claims (TIFIN Give's Louise executing donor requests; Daffy's write-capable MCP server) sit on the **donor recommendation side**, upstream of sponsor authority. The best quantified AI eligibility evidence comes from an adjacent market (Benevity Match Assurance: vendor-reported match decline rate 30%→<3%, 500+ clients) ([Benevity, 2026-06-04](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026)).

---

## 2. Method

1. Enumerate 16 processes (15 sponsor-side plus nonprofit-side attribution) and, for each, gather public evidence of volume, effort, technology, compliance hooks and exceptions.
2. Where evidence is absent (most cases), set **explicit SCENARIO parameters**: annual volume V, share of cases needing human touch e, minutes per touched case m (low/base/high), labor role, rules-amenability b, AI-amenability a, redesign elimination share d, and tokens per case.
3. Compute the **annual human labor pool** L = V × e × m/60 × loaded rate, then the **gross annual capture** of each intervention before its fixed cost:
   - A (improve manual workflow): 15% × L ([S] assumption; model: `data/mission-2026-11-14/ai-process-economics.csv`)
   - B (conventional automation): 50% × b × L ([S] assumption; model: `data/mission-2026-11-14/ai-process-economics.csv`)
   - C (AI on existing workflow): s_C × a × L − QA − inference, with s_C = 40% base, QA = 10% of touched cases re-reviewed at half the original minutes, inference = cases × tokens × Sonnet 5.5 price ([Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)) × 3 ([S]; model: `data/mission-2026-11-14/ai-process-economics.csv`)
   - D (eliminate/redesign): d × L ([S]; model: `data/mission-2026-11-14/ai-process-economics.csv`)
4. Compare gross capture with plausible fixed-cost ranges per intervention type and test the ranking against optimistic/pessimistic AI assumptions.

**Why gross capture rather than net value:** fixed costs (build, licences, governance, model-risk management, integration) are unknown and usually shared across processes. Gross capture tells a buyer the **maximum annual spend an intervention can justify**, which is a more defensible output than an invented net figure. Because L scales linearly with V, e and m, the **ranking of interventions within a process does not change between the low/base/high labor scenarios**; only whether any intervention clears its fixed cost does. Sensitivity therefore focuses on pool size and on the AI parameters.

**Volume anchors [F]:** Fidelity Charitable reports ~3.0M grants in calendar 2025 ([2026 Giving Report](https://www.fidelitycharitable.org/insights/2026-giving-report.html)); DAFgiving360 1.5M in calendar 2025 ([press release, 2026-01-27](https://www.dafgiving360.org/press-release/2025-results)); NPT 159,543 grants in FY2025 ([NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)). The model uses 1M grants as an illustrative mid-to-large sponsor; scale grant-linked results linearly (×3 for a Fidelity-sized volume, ×0.16 for NPT) **only if** the same assumptions held, which is unknown. Volumes for non-grant processes (accounts opened, contributions, service contacts, succession events) have **no public anchor** and are pure [S].

**Labor rates [F→S]:** BLS May 2025 medians: compliance officers $38.81/h, bookkeeping/accounting clerks $24.36/h ([BLS](https://www.bls.gov/ooh/office-and-administrative-support/bookkeeping-accounting-and-auditing-clerks.htm)), customer service representatives $21.53/h ([BLS](https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm)); loaded ×1.429 using the ECEC wage share. Loaded rates: $55.45, $34.80, $30.76. Real DAF staff may be paid more (e.g., counsel on complex assets) or less; that would move pools, not rankings.

---

## 3. Process-by-process assessment

Full parameters and evidence fields are in the CSV. "Pool" is the base-case annual human labor in the scenario at 1M grants (or the stated non-grant volume).

| # | Process | Public evidence on effort / exceptions | Judgment | Base pool [S] | Rank of gross capture [S] | Should the process exist as is? [I] |
|---|---|---|---|---:|---|---|
| P01 | Account opening / KYC | None published (pool [S]: `data/mission-2026-11-14/ai-process-economics.csv`) | Low-Med | $55k | B > D > A > C | Redesign: reuse custodian/adviser KYC |
| P02 | Cash & public-securities intake | 170(f)(8)/(18) acknowledgments required ([26 USC 170](https://www.law.cornell.edu/uscode/text/26/170)); no exception data | Low | $44k | D > B > A > C | Redesign: pre-announced transfers with structured fund reference |
| P03 | Noncash complex assets | Qualified appraisal / Form 8283 ([IRS](https://www.irs.gov/instructions/i8283)); 4943 holdings ([26 USC 4943](https://www.law.cornell.edu/uscode/text/26/4943)) | High | $532k | A > D > B > C (C first if optimistic) | Keep; judgment is the product |
| P04 | Investment allocation / rebalancing | None (pool [S]: `data/mission-2026-11-14/ai-process-economics.csv`) | Low | $9k | B > D > A > C | Keep, automated |
| P05 | Grant recommendation intake | DAFgiving360 FY2025: 38% recurring, 70%+ unrestricted ([press release](https://www.dafgiving360.org/press-release/fiscal-year-2025-results)) | Low-Med | $174k | D > B > A > C | Redesign: structured purpose and attestation |
| P06 | Routine eligibility verification | RCF 2023 policy: Charity Check adequate for >98% of historical grants (coverage, not exception rate) ([RCF policy](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf)); IRS files monthly | Low | $139k | D > B > A > C | **Should not exist per grant** |
| P07 | Non-standard grantee due diligence | 4966(c)(1)(B) expenditure responsibility; 4966(d)(4) disqualified supporting orgs ([26 USC 4966](https://www.law.cornell.edu/uscode/text/26/4966)); RCF 2023: ~$4k typical international cost, $50k minimum | High | $1.25M | D > A > B > C | Partially redesign (shared determinations) |
| P08 | Prohibited/excess-benefit review | 4967: 125% tax on benefited person ([26 USC 4967](https://www.law.cornell.edu/uscode/text/26/4967)); 4958(c)(2) automatic excess benefit ([26 USC 4958](https://www.law.cornell.edu/uscode/text/26/4958)) | Med-High | $462k | D > B > A > C | Keep control; move upstream |
| P09 | Disbursement & payment | Fidelity: Stripe/ACH paths; review may take 10+ business days ([FAQ](https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html)) | Low | $174k | D > B > A > C | **Checks should be phased out** |
| P10 | Returned/uncashed checks & reconciliation | No public data; repo model bounded under assumptions (`research/daf-reconciliation-economics-scenario-model-2026-11-11.md`; pool [S]: `data/mission-2026-11-14/ai-process-economics.csv`) | Low-Med | $348k | D > B > A > C | **Largely should not exist** |
| P11 | Donor/advisor service inquiries | Fidelity routes servicing to phone; site assistant is navigation-only ([terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html)) | Med | $656k | D > A > B > C | Reduce via proactive status |
| P12 | Tax receipts & statements | 170(f)(8), (f)(18) content rules ([26 USC 170](https://www.law.cornell.edu/uscode/text/26/170)) | Low | $26k | B > D > A > C | Keep, deterministic |
| P13 | Succession | None (pool [S]: `data/mission-2026-11-14/ai-process-economics.csv`) | Med-High | $222k | D > A > B > C | Reduce via pre-registered successors |
| P14 | Fraud/AML/sanctions alerts | OFAC Framework is risk-based ([OFAC 2019](https://ofac.treasury.gov/media/16331/download)); BSA applicability to standalone sponsors not established | Med | $139k | B > D > A > C | Keep |
| P15 | 990 Schedule D / audit data | 6033(k) DAF reporting ([26 USC 6033](https://www.law.cornell.edu/uscode/text/26/6033)) | Low-Med | $92k | D > B > A > C | Keep; fix data upstream |
| P16 | Nonprofit-side DAF gift attribution | 1,200+ DAF formats (Chariot citing DAFRC); Chariot AI agent codes gifts ([Chariot, 2026-01-28](https://givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits)) | Low | $1.04M (sector-side) | D > B > A > C | **Largely should not exist** |

**Totals [S]:** sponsor-side pools (P01–P15) sum to **$0.87M / $4.32M / $18.7M** (low/base/high) at 1M grants. Base gross capture: A $0.65M, B $0.81M, C $0.33M, D $1.81M. These figures are as uncertain as the touch rates and minutes behind them (Section 5). The spread (21×) is itself the main message: **no one can price DAF AI replacement until exception rates and handling times are measured.**

### Notes on the twelve dimensions requested

- **Current human effort and exception rates:** no sponsor publishes either. The only quantified rate-like figure (RCF's >98% Charity Check adequacy, [RCF policy](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf)) measures data coverage, and the repo has already rejected using it as an exception rate.
- **Technology expense:** undisclosed in public sources for every sponsor; repo fee-audit documents cover vendor fees, not operations-technology cost per process.
- **Compliance:** the federal hooks concentrate in P05–P08 (4966/4967/4958) and P02/P03/P12 (substantiation). Penalties fall on the sponsor (20% of a taxable distribution) and managers (5%, capped at $10,000 per distribution) under 4966, and on donors/advisors (125%) and managers (10%) under 4967 ([26 USC 4966](https://www.law.cornell.edu/uscode/text/26/4966); [26 USC 4967](https://www.law.cornell.edu/uscode/text/26/4967)). These asymmetric stakes are why automated *approval* is the wrong target even where automated *screening* is cheap.
- **Judgment, oversight cost, QA burden:** high-judgment processes (P03, P07, P08, P13) are exactly where AI output needs the most expensive review, which offsets AI's appeal there.
- **Inference cost:** $0.01–$0.60 per case at Sonnet 5.5 in all 16 processes [S]. Highest annual inference arises where AI screens 100% of volume rather than exceptions: P08 ($54k/yr) and P05 ($18k/yr) at 1M grants. Haiku 5.5 would cut these ~20×; Opus 5.5 would double them. None is material against labor.
- **Integration complexity:** highest where the process spans institutions (P09, P10, P16, P07) — the same processes where redesign has the highest payoff but needs counterparties.
- **Customer-relationship impact:** highest in P03, P11, P13 (largest donors, bereavement, everyday contact). These are also the places where a wrong or tone-deaf AI response carries the most relationship cost; see the governance document.

---

## 4. Intervention comparison

### 4.1 Why D usually wins on gross capture, and why that is not the end of the analysis

[I] Redesign removes the *cause* of exceptions: a continuous charity-status subscription removes per-grant lookups; electronic payment to a verified payee removes stale checks; a structured remittance identifier removes attribution guesswork; structured attestations at intake remove purpose interpretation. AI applied to the existing workflow can only shorten the handling of exceptions that redesign would have prevented.

But D carries constraints the dollar figures omit:
- **Coordination:** P07 (shared equivalency determinations), P10/P16 (remittance standard) need other sponsors, processors or charities to participate. The repo's reconciliation model already identified an incidence mismatch: recipients bear costs that sponsors control. [I]
- **Time-to-value:** standards and payee-enrollment campaigns take years; AI can be deployed by a single institution now. For a single nonprofit facing 1,200 DAF formats today, Chariot-style AI coding (C) is rational even though a sector standard (D) would be better for the system.
- **Residual tail:** charities without electronic banking, foreign grantees, churches not in IRS files (RCF policy accepts supplemental documentation for churches and governmental units) remain manual after D.

### 4.2 When C beats B

[S] With the base formulas, C's gross capture exceeds B's when s_C × a − 0.05 > 0.5 × b. With s_C = 40%, that requires AI-amenability a to exceed roughly 1.25 × b + 0.125. Only document-heavy, weakly-structured work meets this: P03 (a 0.35 vs b 0.20) and P07 (0.45 vs 0.25) come close; P11 (0.45 vs 0.30) comes close. Rule-friendly processes (P04, P06, P09, P12, P15) never do.

### 4.3 Sensitivity of AI value (base pool, gross, USD/yr at 1M grants) [S]

| Process [S] (`data/mission-2026-11-14/ai-process-economics.csv`) | C pessimistic (s_C 20%, QA 25%) | C base (40%, 10%) | C optimistic (60%, 5%) | Best non-C (base) |
|---|---:|---:|---:|---:|
| P03 Complex assets | −30,718 | 46,469 | 97,039 | 79,848 (A or D) |
| P07 Non-standard DD | −50,417 | 155,441 | 298,918 | 499,050 (D) |
| P08 Benefit review | −79,415 | −12,412 | 31,485 | 138,625 (D) |
| P10 Reconciliation | −23,400 | 23,580 | 53,160 | 295,800 (D) |
| P11 Service inquiries | −32,567 | 75,708 | 151,172 | 262,485 (D) |
| P13 Succession | −13,159 | 19,002 | 40,073 | 66,540 (D) |
| P16 Attribution (sector) | −54,180 | 107,640 | 217,260 | 835,200 (D) |
| Sponsor total P01–P15 | −314,282 | 329,408 | 757,120 | — |

Readings:
- [S] Under pessimistic assumptions (AI saves 20% of handling time and a quarter of AI-touched cases need re-review), **AI destroys value in every process.** QA intensity is the single most important AI parameter; it is unmeasured anywhere in the DAF market.
- [S] Under optimistic assumptions, sponsor-wide AI gross capture (~$0.76M/yr at 1M grants; ~$2.3M if every grant-linked figure scaled ×3 to Fidelity volume) would fund a modest shared AI platform, but **not** a per-process build for each of 15 processes.

### 4.4 Fixed-cost hurdle (illustrative ranges, [S])

| Intervention | Plausible annual fixed/governance cost range | Processes whose base gross capture clears the low end at 1M grants |
|---|---|---|
| A manual improvement | $25k–$100k [S] | P03, P05, P07, P08, P10, P11, P13 (gross values: `data/mission-2026-11-14/ai-process-economics.csv`) |
| B conventional automation | $100k–$500k [S] | P07 only clears at the low end; most B value requires a shared platform (gross values: `data/mission-2026-11-14/ai-process-economics.csv`) |
| C AI on workflow | $150k–$750k incl. evaluation, model-risk, security review [S] | P07 only (base); none at the high end (gross values: `data/mission-2026-11-14/ai-process-economics.csv`) |
| D redesign | $200k–$2M plus coordination [S] | P07, P10, P11 (and P16 sector-side) (gross values: `data/mission-2026-11-14/ai-process-economics.csv`) |

These ranges are assumptions; their purpose is to show that **per-process business cases fail for most DAF processes at sub-Fidelity scale**, which pushes economics toward (i) shared utilities (registry, payment network, remittance standard) and (ii) vendor platforms that amortize AI governance across many sponsors (Ren, TIFIN, Foundation Source/Vennfi, Stellar/iPhi). [I] This is a structural argument for AI being bought from a DAF technology vendor or infrastructure provider rather than built by a mid-sized sponsor.

### 4.5 Sequencing

[I] The rational order is **D where the sponsor controls the redesign → B on the remaining structured work → C on the residual unstructured tail**. For P07, if redesign removed 40% of the pool, C on the residual would capture roughly $93k/yr at base assumptions [S], below the C fixed-cost range at 1M grants and near it at 3M. AI "on the existing workflow" (the brief's option C) is therefore the wrong comparator for most sponsors; the relevant AI case is AI-after-redesign.

---

## 5. Assumptions and what would change the conclusions

| Parameter | Base [S] | Why it matters | What would overturn the ranking |
|---|---|---|---|
| A saving 15% uniform | 15% [S] (`data/mission-2026-11-14/ai-process-economics.csv`) | A could be larger where practice varies across reviewers | Measured reviewer-variance studies |
| B saving 50% × rules-amenability | 0.2–0.85 [S] (`data/mission-2026-11-14/ai-process-economics.csv`) | Encodes mature lookups/validation | Evidence that rules are already maxed out (then B ≈ 0 and C rises) |
| C saving s_C × AI-amenability | 40% × 0.1–0.45 [S] (`data/mission-2026-11-14/ai-process-economics.csv`) | Single largest AI uncertainty | Time-and-motion trial showing s_C × a > 0.3 with QA ≤ 5% |
| QA re-review | 10% of touched cases at half minutes [S] | Automation bias pressures QA down; regulators push it up | Measured error/override rates |
| Redesign elimination | 0.15–0.9 | Assumes counterparties adopt | Failure of standards adoption; charities refusing electronic payment |
| Touch rates and minutes | see CSV | Set pool size, not ranking | Any sponsor time study |
| Inference multiplier | ×3 [S] (`data/mission-2026-11-14/ai-process-economics.csv`; price per [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)) | Agents loop | Irrelevant unless >100× (inference remains <1% of labor) |

**The most important unknowns (to be measured, not modeled):** true exception incidence by type; handling minutes; reviewer error and override rates; share of grants still paid by check; share of service contacts that are status inquiries.

---

## 6. AI use-case inventory and adoption evidence

### 6.1 Evidence classes (definitions used in the CSV)

- **announced:** vendor/organization statement of launch, availability or plan, without independent observation, usage metric or named customer.
- **demonstrated:** public, inspectable documentation or interface showing the capability exists (API docs, help-center pages, connector listings), without usage evidence.
- **deployed-with-evidence:** in operation with a named user, a usage/adoption metric, GA plus earnings commentary, or a published operating policy. Vendor-sourced metrics still qualify but are flagged.
- **unverified:** only secondary/marketing content or a source that could not be retrieved.

### 6.2 Counts (30 use cases)

| Evidence class | DAF-direct | Adjacent philanthropy-tech | Enabling | Total |
|---|---:|---:|---:|---:|
| announced | 6 | 7 | 0 | **13** |
| demonstrated | 1 | 6 | 0 | **7** |
| deployed-with-evidence | 2 | 5 | 1 | **8** |
| unverified | 1 | 1 | 0 | **2** |
| **Total** | **10** | **19** | **1** | **30** |

### 6.3 What the inventory shows

- **Sponsor-side AI is nearly absent from the public record.** [F] No AI product or statement was found for DAFgiving360, Vanguard Charitable or NPT in searches on 2026-11-14 (absence of evidence, not evidence of absence). Fidelity Charitable publishes AI thought-leadership by third-party authors (e.g., a summary of an August 2024 survey of 1,006 donors in which 93% rated transparency about AI use important and 39.8% were uneasy about data use, [article](https://www.fidelitycharitable.org/articles/donor-perceptions-of-ai.html)), and operates a website "Virtual Assistant" described as an "automated natural language search engine" with no account servicing and no accuracy guarantee ([terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html)). No public AI claim by Ren was found; per repo convention this is `not_verified`, not absence.
- **The agentic frontier is donor-side.** [F] TIFIN Give's Louise (2025-10-27) is described as executing requests such as "Set up a monthly recurring $100 grant" and "Contribute 100 shares of NVDA stock to my DAF"; the release states no guardrails or human review ([PR Newswire](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html)). Daffy documents an MCP server with seven read tools and two write tools (`make_donation`, which "moves real money", and `cancel_donation`), sign-in via OAuth or API key, and no documented per-donation limit ([Daffy docs](https://docs.daffy.org/agents/mcp), undated, read 2026-11-14). Daffy's April 2025 release also claims AI that unifies charity data and "flags issues for review" ([FF News, 2025-04-09](https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/)).
- **A DAF is already being run by agents on the advisor side.** [F] The Circle Foundation's assets sit in a DAF at Fidelity Charitable; an intake agent screens and scores proposals and leaders state "AI recommends … humans decide" ([Chronicle of Philanthropy, 2026-11-06](https://www.philanthropy.com/news/ai-recommends-humans-decide-circle-foundations-bet-on-agentic-philanthropy/)). [I] This is the first public case found where AI agents generate DAF grant recommendations at institutional scale; sponsor approval still sits downstream.
- **Infrastructure and data providers are positioning for AI channels.** [F] Anthropic's Claude for Nonprofits (2025-12-02) launched connectors for Blackbaud, Candid and Benevity ([Anthropic](https://www.anthropic.com/news/claude-for-nonprofits)). Candid, a principal data source behind charity vetting, cut 42 staff (about one-fifth) and is repositioning as a data supplier to AI platforms ([Chronicle, 2026-02-12](https://www.philanthropy.com/news/candid-cuts-staff-bets-its-future-on-ai/)). [I] If the vetting data layer becomes an AI-mediated channel, the sponsor's evidence trail (which snapshot was relied on) must survive that mediation.
- **Recipient-side AI is the most deployed.** [F] Chariot's gift processing platform uses "customizable LLMs" and an AI agent to code donations for CRMs, naming American Cancer Society, Dallas Jewish Community Foundation and Central Park Conservancy as customers ([Chariot, 2026-01-28](https://givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits)). [I] This is AI compensating for the attribution problem (P16) that a remittance standard would remove.
- **Adjacent grantmaking evidence is the best proxy for due-diligence AI.** [F] McGovern's Grant Guardian reports 189 organizations supported and a user reporting review time of "two to three minutes per grantee" with human-in-the-loop ([McGovern, 2025-07-22](https://www.mcgovern.org/how-foundations-are-using-ai-to-vet-grantees/)). Benevity's Match Assurance reads receipts, verifies eligibility and auto-submits matches (vendor: 500+ clients, decline rate 30%→<3%) ([Benevity](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026)). Blackbaud's Development Agent reached GA on 2026-03-17 for U.S. Raiser's Edge NXT ([Nasdaq/Blackbaud](https://www.nasdaq.com/press-release/blackbaud-launches-new-category-ai-agent-general-availability-its-first-agent-goodtm)).
- **Sector adoption is broad but shallow.** [F] CEP's 2025 survey (451 nonprofit and 215 foundation leaders) found most organizations use AI, mostly internally, and only 11% of funders support grantees' AI implementation ([CEP, 2025-09-30](https://cep.org/news/press-releases/as-ai-use-proliferates-in-the-social-sector-new-study-reveals-lagging-support-for-equitable-ai/)).

---

## 7. Implications for the repo's existing conclusions

- Consistent with the 2026-11-12 exception model ("prevention before complex AI"; `research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`) and Ren/RCF audit ("instant approval ≠ AI"; `research/ren-instant-grant-approval-rcf-policy-clarity-audit-2026-11-12.md`): this analysis extends the point to 16 processes and adds that **inference cost is negligible, QA cost decisive**.
- New: the **unit of AI investment is a shared platform**; per-process AI cases fail at sub-Fidelity scale under every base assumption. This favors vendors that serve many sponsors and infrastructure that serves many charities.
- New: the **agentic risk surface has moved upstream** (donor-side agents creating recommendations), increasing the importance of the repo's recommendation-vs-approval state separation.

## 8. Open questions

1. What share of grants at each major sponsor still pays by check, and what fraction of those are reissued or escheated?
2. What are the true exception incidence and minutes for P06–P08 at any sponsor? (A 90-day time study, as designed in the 2026-11-12 exception document (`research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`), is the gating evidence.)
3. Does TIFIN's Louise execution path stop at a sponsor approval state, and with what limits?
4. Will Daffy or others add per-agent spending limits, and how do sponsors receiving agent-originated recommendations distinguish them?
5. Would a Candid/IRS-based continuous status feed be accepted by sponsors' auditors as replacing per-grant verification?

---

## Sources (accessed 2026-11-14 unless noted)

Pricing and wages: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing); [BLS compliance officers](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm); [BLS bookkeeping clerks](https://www.bls.gov/ooh/office-and-administrative-support/bookkeeping-accounting-and-auditing-clerks.htm); [BLS customer service representatives](https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm); [BLS ECEC June 2026](https://www.bls.gov/news.release/ecec.nr0.htm).
Volumes: [Fidelity Charitable 2026 Giving Report](https://www.fidelitycharitable.org/insights/2026-giving-report.html); [DAFgiving360 2025 results](https://www.dafgiving360.org/press-release/2025-results); [DAFgiving360 FY2025](https://www.dafgiving360.org/press-release/fiscal-year-2025-results); [NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/).
Law and data: [26 USC 170](https://www.law.cornell.edu/uscode/text/26/170); [26 USC 4943](https://www.law.cornell.edu/uscode/text/26/4943); [26 USC 4958](https://www.law.cornell.edu/uscode/text/26/4958); [26 USC 4966](https://www.law.cornell.edu/uscode/text/26/4966); [26 USC 4967](https://www.law.cornell.edu/uscode/text/26/4967); [26 USC 6033](https://www.law.cornell.edu/uscode/text/26/6033); [IRS Form 8283 instructions](https://www.irs.gov/instructions/i8283); [IRS bulk data](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads); [IRS Auto-Revocation List](https://www.irs.gov/autorevocationlist); [OFAC Framework 2019](https://ofac.treasury.gov/media/16331/download); [RCF Due Diligence Policy (Mar 2023)](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf); [Fidelity grant timeline FAQ](https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html).
Market: [TIFIN Louise PR (2025-10-27)](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); [TIFIN Tax Intelligence (2025-09-10)](https://tifin.com/news/tifin-give-launches-first-of-its-kind-tax-intelligence-for-philanthropy/18820/); [Daffy MCP docs](https://docs.daffy.org/agents/mcp); [Daffy AI release (2025-04-09)](https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/); [Fidelity Charitable donor perceptions](https://www.fidelitycharitable.org/articles/donor-perceptions-of-ai.html); [Fidelity virtual assistant terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html); [Circle Foundation (2026-11-06)](https://www.philanthropy.com/news/ai-recommends-humans-decide-circle-foundations-bet-on-agentic-philanthropy/); [Chariot (2026-01-28)](https://givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits); [Blackbaud Development Agent GA (2026-03-17)](https://www.nasdaq.com/press-release/blackbaud-launches-new-category-ai-agent-general-availability-its-first-agent-goodtm); [Anthropic Claude for Nonprofits (2025-12-02)](https://www.anthropic.com/news/claude-for-nonprofits); [Candid–Anthropic](https://candid.org/press/candid-partners-with-anthropic-to-bring-trusted-data-to-claude-for-nonprofits/); [Candid staff cuts (2026-02-12)](https://www.philanthropy.com/news/candid-cuts-staff-bets-its-future-on-ai/); [Benevity Live 2026](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026); [Benevity–Claude](https://benevity.com/press-releases/benevity-integrates-global-nonprofit-network-with-anthropics-claude); [McGovern Grant Guardian (2025-07-22)](https://www.mcgovern.org/how-foundations-are-using-ai-to-vet-grantees/); [CEP AI survey (2025-09-30)](https://cep.org/news/press-releases/as-ai-use-proliferates-in-the-social-sector-new-study-reveals-lagging-support-for-equitable-ai/). Additional inventory sources are listed per row in the CSV.

---

## Data dictionary

### `data/mission-2026-11-14/ai-process-economics.csv` (one row per process)

| Column | Meaning |
|---|---|
| process_id, process, unit | Identifier, name, unit of volume |
| scenario_volume_base | Annual volume V used in the scenario [S] |
| volume_anchor_note, volume_anchor_url | Public anchor for V where one exists |
| touch_rate_low/base/high | Share of volume needing human handling e [S] |
| minutes_low/base/high | Handling minutes per touched case m [S] |
| labor_role, loaded_rate_usd_hr | Role proxy and loaded hourly rate (BLS median ×1.429) |
| labor_pool_low/base/high_usd | V × e × m/60 × rate |
| current_human_effort_evidence, technology_expense_evidence, exception_rate_evidence | Public evidence found (or its absence) |
| compliance_requirements, compliance_source_url | Main legal/regulatory hooks |
| judgment_required, oversight_cost, integration_complexity, qa_burden, customer_relationship_impact | Qualitative ratings [I] |
| rules_amenability, ai_amenability, redesign_elimination_share | b, a, d parameters [S] |
| inference_tokens_in/out, inference_cost_per_case_usd, inference_cost_annual_base_usd | Tokens per case; cost at Sonnet 5.5 list price ×3 loop multiplier |
| gross_A/B/C/D_base_usd | Gross annual capture before fixed costs at base [S] |
| rank_base | Ranking of gross capture |
| best_if_C_optimistic / best_if_C_pessimistic | Best intervention if s_C=60%/QA=5% or s_C=20%/QA=25% [S] |
| recommended_intervention, should_process_exist, rationale | Analytical judgment [I] |
| evidence_status | Which fields are sourced vs scenario |

### `data/mission-2026-11-14/ai-use-case-inventory.csv` (one row per use case)

| Column | Meaning |
|---|---|
| use_case_id, organization, org_type, product_or_initiative | Identification |
| ai_function | What the AI is claimed to do |
| daf_relevance | direct (DAF sponsor/vendor/DAF account), adjacent (philanthropy tech), enabling (model provider) |
| action_capability | inform / recommend / generate content / read / act |
| date_announced | Announcement or launch date |
| evidence_class | announced / demonstrated / deployed-with-evidence / unverified (Section 6.1) |
| evidence_basis | Why that class was assigned |
| human_oversight_stated | Oversight language in the source, if any |
| source_url, source_date | Primary or best available source and its date |
| notes | Caveats |

## Red-team corrections (wave 2A, 2026-11-14) — governing

1. **`ai-economics-replacement-analysis.md`, Exec #2.** Replace "This ranking is driven by stated assumptions (Section 5), but the structural reason is robust" with:
   > "This ranking is determined by stated assumptions: with A fixed at 15% and AI-amenability capped at 0.45, C cannot exceed A in any process (that requires a > 0.50). It is not evidence about AI performance. The directional point — prevent exceptions before automating their handling — rests on reasoning, not on the model." ([S]; model: `data/mission-2026-11-14/ai-process-economics.csv`)
2. **Same doc, §4.3 readings.** Replace "QA intensity is the single most important AI parameter" with:
   > "QA intensity decides whether AI value is positive; the ranking is driven mainly by the assumed AI-amenability (a) and redesign share (d), both unsourced. With QA = 0, C still ranks last in 12/16 processes at s_C = 40%." ([S]; model: `data/mission-2026-11-14/ai-process-economics.csv`)
3. **Same doc, §3 table and CSV `rank_base` for P07.** Annotate: "B and C within $512 (0.3%); treat as tied." ([S]; P07 `gross_B_base_usd` 155,953 vs `gross_C_base_usd` 155,441 in `data/mission-2026-11-14/ai-process-economics.csv`)
4. **Same doc, §4.4.** Add P09 to the list of processes where A clears $25k ([S]; P09 `gross_A_base_usd` 26,100 in `data/mission-2026-11-14/ai-process-economics.csv`).
5. **Same doc, §1 #5 and §6.3.** Add:
   > "Exception: Daffy, which operates its own sponsor (Daffy Charitable Fund), announced back-end AI that unifies charity data and 'flags issues for review' (2025-04-09; announced only)." ([FF News, 2025-04-09](https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/))

   Also change "at institutional scale" to "at one corporate DAF".
6. **Same doc, Benevity mentions.** Change "500+ clients" to "500+ clients across Grant Summaries and Match Assurance". Change "match decline rate" to "external match decline rate".
7. **Same doc, Chariot.** Replace "(vendor citing DAFRC)" with "(vendor figure, unattributed)".
8. **Same doc, Candid.** Change the text to:
   > "cut staff (Chronicle reports 42, about one-fifth; count not independently verified) and is repositioning as a data supplier to AI platforms."
9. **`ai-use-case-inventory.csv`.** Add Bonterra Que (2025-10-01, adjacent, act/recommend, announced, https://www.businesswire.com/news/home/20251001579571/en) and Bonterra Grantmaker (2026-02-19, announced). Change U20 `date_announced` to 2025-07-22, or note why it differs. Recount the §6.2 table.
