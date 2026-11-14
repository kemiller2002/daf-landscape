# Red-team validation, wave 2A: AI economics, AI governance, AI-native entrant

**Date:** 2026-11-14 · **Validator:** red-team-agent-wave2a (independent; did not author the reviewed work) · **Register:** `data/mission-2026-11-14/validation-register-wave2a.csv` (31 claims, prefix V2A-)

**Documents reviewed:**
- `research/mission-2026-11-14/ai-economics-replacement-analysis.md`, with `ai-process-economics.csv` and `ai-use-case-inventory.csv`
- `research/mission-2026-11-14/ai-governance-failure-modes.md`, with `ai-failure-mode-register.csv`
- `research/mission-2026-11-14/ai-native-entrant-simulation.md`, with `ai-native-component-buy-build-matrix.csv` and `entry-strategy-comparison.csv`

**Method.** I chose the claims that drive a ranking or a recommendation. For each one I went back to the primary source myself rather than following the doc's link, and recorded exact values, dates and wording. I recomputed every row of `ai-process-economics.csv` and all nine entrant capital cells. I then ran my own sensitivity grid and break-even analysis, using the scripts in the scratchpad.

## Result counts

| Result | Count |
|---|---:|
| confirmed | 15 |
| partially_confirmed | 11 |
| contradicted | 3 |
| unable_to_verify | 2 |
| **Total** | **31** |

The sourced facts hold up well: prices, wages, statute, grant counts, TIFIN, Daffy, Endaoment, RCF, CEP and Circle Foundation all check out. The weak points are interpretive. Two headline framings are artifacts of how the models were built, and the two docs disagree with each other on the entrant's core product.

---

## Findings ranked by severity

### HIGH-1. "AI ranks last in all 16 processes" is true by construction, not a finding (V2A-04)

- **The arithmetic is exact.** All 16 rows reproduce with 0 mismatches (V2A-03).
- **The ranking is fixed by the inputs.** Under the base formulas, C can beat A only if 0.4·a − 0.05 > 0.15, which means a > 0.50. Every process is assigned a ≤ 0.45. C therefore cannot beat A in any process, whatever the volumes, minutes or QA.
- **The comparators are favored.** A is a 15% saving applied to every process with no evidence and no cost. D gets elimination shares of up to 0.9, against AI-amenability capped at 0.45 (`redesign_elimination_share`, `ai_amenability` in `data/mission-2026-11-14/ai-process-economics.csv`).
- **Option C is narrowly defined.** C is AI bolted onto an unchanged workflow. AI-enabled redesign is never modeled as an option, even though the entrant doc's S3 is exactly that.
- **P07 is a tie, not a ranking.** C is $155,441 and B is $155,953, a gap of $512 (0.3%) (`data/mission-2026-11-14/ai-process-economics.csv`). The doc's own §4.2 inequality also puts P07 *above* the C>B threshold (a = 0.45 > 1.25·0.25 + 0.125 = 0.4375). C loses only because of the $6,750 inference cost.

**Is the conclusion robust?** It is robust inside the model's parameter space. It is not robust as an empirical claim. The robustness comes from unsourced a and d values, not from any evidence about AI.

### HIGH-2. QA is not the driver of the ranking; the doc says it is (V2A-05)

The doc says QA intensity is "the single most important AI parameter". My sensitivity rerun (QA = share of touched cases re-reviewed at half the minutes) shows otherwise:

| s_C \ QA (rerun of `data/mission-2026-11-14/ai-process-economics.csv`) | 0% | 5% | 10% | 25% |
|---|---|---|---|---|
| 0.2 | C last 16/16 | 16/16 | 16/16 | 16/16 |
| 0.4 (base) | **12/16** | 14/16 | **16/16** | 16/16 |
| 0.6 (optimistic) | 8/16 (P03 first) | 9/16 (P03 first) | 10/16 (P03 first) | 15/16 |
| 0.8 | 3/16 (P03, P14 first) | 7/16 | 7/16 | 10/16 |

- **Ranking barely moves with QA.** Removing QA entirely still leaves C last in 12 of 16 processes.
- **Amenability moves it more.** Scaling ai_amenability by ×1.5 leaves C last in 10/16; ×2 leaves it last in 7/16.
- **Scoping QA to AI-handled cases only changes little.** At s_C = 0.4, C is last in 13/16 (QA 5%) to 16/16 (QA 25%) (rerun of `data/mission-2026-11-14/ai-process-economics.csv`).
- **What it takes for C to beat the best non-C option at QA 10%:** s_C ≥ 0.58 in P03, ≥ 0.87 in P14, and about 1.0 in P07, P11 and P13. For the other processes s_C would have to exceed 1, which is impossible (rerun of `data/mission-2026-11-14/ai-process-economics.csv`).
- **The pessimistic result is also mechanical.** "AI destroys value in every process" follows because 0.2·a ≤ 0.09 is always less than the 0.125 QA cost.

QA decides the **sign** of C. The unsourced parameters a and d decide its **rank**.

### HIGH-3. The entrant doc and the governance doc contradict each other on model-assisted clearing (V2A-22)

- **Governance doc (§5 item 3):** "AI may add flags… only humans or deterministic rules may remove flags or approve." It also prohibits AI on the P06 decision path.
- **Entrant doc (S3 MVP and falsifier):** tests for "zero false clears". It counts the strategy as falsified only if counsel "will not permit model-assisted clearing".
- **Why it matters:** S3's value depends on the very permission the companion doc says should not be granted.

### HIGH-4. The S3 recommendation targets a segment that is mostly below its own break-even (V2A-21)

- **Grant review alone.** The entrant's model saves $0.325 per grant. Break-even at $36k / $120k / $240k per year is **111k / 369k / 738k grants per year**.
- **Generous case.** Assume S3 captures *all* base redesign value plus AI-on-residual value in its scope (P05–P08, P10, P11, P15). Gross value is then about $1.58M per 1M grants, and break-even at $120k is about **76k grants per year**. (Optimistic AI assumptions: about 68k.)
- **The named example is below both thresholds.** Charityvest made 48,744 grants (confirmed; [Charityvest 2025 results](https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/)). Few US sponsors exceed about 76k grants a year, and the largest run in-house platforms. The base case needs 42 such customers.
- **What the doc already admits.** It says (§5.4, §8 condition 2) that the pool is unmeasured.
- **What it does not acknowledge.** Its own target segment fails on its own numbers. It also treats "lowest capital" as a reason to choose S3, but that is an input: S3 is *assumed* to need 9 FTE against S1's 32 (V2A-19). The capital comparison also ignores time to revenue: S3 needs 42 customers for $5m ARR, S1 needs 5 (`data/mission-2026-11-14/entry-strategy-comparison.csv`).

**Assessment:** S3 is a reasonable *research probe*. It is not yet a supported *recommendation*.

### MEDIUM-1. Sponsor-side AI is not entirely absent ([V2A-09](https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/))

Daffy operates its own sponsor, Daffy Charitable Fund (EIN 86-3177440, per the repo). In April 2025 it announced back-end AI that "unifies and enriches" charity data, "flagging issues for review". That is sponsor-side and eligibility-adjacent. The evidence class is announced only.

The economics doc's line that "the most agentic DAF claims sit on the donor recommendation side" should note this exception. I found no AI claims, beyond what is inventoried, for Fidelity Charitable (virtual assistant and thought leadership only), DAFgiving360, Vanguard Charitable, NPT, Ren, Foundation Source/Vennfi, Givinga or Endaoment. That remains absence of evidence.

### MEDIUM-2. Inventory and competitor omissions ([V2A-25](https://www.daffy.org/resources/daffy-for-developers), [V2A-26](https://www.businesswire.com/news/home/20251001579571/en/Bonterra-Launches-Que-The-First-Agentic-AI-Platform-for-Funders-Nonprofits-and-Supporters))

- **Bonterra is missing from the AI inventory.** Bonterra Que (2025-10-01) is an agentic AI platform for funders that includes application scoring ([Business Wire, 2025-10-01](https://www.businesswire.com/news/home/20251001579571/en/Bonterra-Launches-Que-The-First-Agentic-AI-Platform-for-Funders-Nonprofits-and-Supporters)). Bonterra Grantmaker (2026-02-19) is powered by Que (source: no primary URL in register).
- **The entrant doc omits several relevant players:**
  - Daffy for Developers open APIs (May 2023): a second sponsor-of-record API besides Endaoment ([Daffy for Developers](https://www.daffy.org/resources/daffy-for-developers)).
  - Goodstack (formerly Percent): a nonprofit verification and eligibility API, a direct S2 competitor ([Goodstack docs](https://docs.goodstack.io/docs/guides/Cause%20verification/)).
  - Every.org: nonprofit search and donate APIs on a DAF structure ([Every.org docs](https://docs.every.org/docs/intro)).
  - Givinga, Stellar/iPhi, DAFtech and Give Interactive: DAF-technology vendors.
  - Benevity, Blackbaud and Bonterra: AI-native incumbents able to bundle S3-like features.
- **Effect:** the distribution and competition rows for S2 and S3 understate the competitive set.

### MEDIUM-3. The two docs describe the §4966 regulatory status differently ([V2A-17](https://kpmg.com/us/en/taxnewsflash/news/2026/09/exempt-organization-projects-irs-priority-guidance-plan.html))

- **Primary-adjacent source (KPMG):** the 2026–27 Priority Guidance Plan, released 2026-09-29 ([KPMG](https://kpmg.com/us/en/taxnewsflash/news/2026/09/exempt-organization-projects-irs-priority-guidance-plan.html); [IRS PGP](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf)), lists "Guidance under sections 4966 and 6033 regarding certain donor advised fund arrangements". The prior plan listed final §4966 regulations.
- **Governance doc:** correct.
- **Entrant doc R9:** says only that "§4966 guidance remains listed".
- **Entrant doc condition 4:** "Final §4966 regulations favor system-of-record owners". This is now a less likely path than the doc implies.

### MEDIUM-4. Smaller source misstatements

- **Benevity ([V2A-12](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026)).** "500+ clients" covers Grant Summaries *and* Match Assurance together, not Match Assurance alone. The decline-rate metric is "external match decline rates".
- **Chariot ([V2A-13](https://givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits)).** The release does not attribute "over 1,200 different DAFs" to DAFRC.
- **Candid ([V2A-14](https://www.philanthropy.com/news/candid-cuts-staff-bets-its-future-on-ai/)).** The figure of 42 staff (one-fifth) could not be verified because the article is paywalled. The Chronicle headline says Candid "Bets Its Future on **Data**", not on AI.
- **Circle Foundation ([V2A-15](https://www.philanthropy.com/news/ai-recommends-humans-decide-circle-foundations-bet-on-agentic-philanthropy/)).** "AI agents generate DAF grant recommendations at institutional scale" overstates the evidence: it is one corporate DAF with a handful of announced grants.
- **McGovern ([V2A-16](https://www.mcgovern.org/how-foundations-are-using-ai-to-vet-grantees/)).** The inventory dates U20 to 2025-01-31 (`data/mission-2026-11-14/ai-use-case-inventory.csv`), but the source is dated 2025-07-22.

### LOW

- **Fixed-cost table (V2A-06).** P09 is missing from the list for A: P09's gross A is $26,100 (`data/mission-2026-11-14/ai-process-economics.csv`), which clears the $25k low end.
- **Labor rates ([V2A-20](https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/)).** The two docs use different rates ($55.45/h and $65/h) and different exception models (`data/mission-2026-11-14/ai-process-economics.csv`; `research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`).
- **Failure-mode headline (V2A-30).** "13 of 16 failure modes created" measures the rubric. It reflects no observed incidents and does not net against human error rates.
- **Endaoment custodians ([V2A-18](https://endaoment.org/institutions)).** The page's line "the DAF follows the assets" about Altruist, Schwab, Fidelity and BNY is marketing copy, not evidence of custodial agreements.
- **Candid Charity Check and OFAC.** The RCF policy states that Charity Check "Includes the result of GuideStar's OFAC verification". That answers the entrant doc's open question 7.
- **P06 update cadence.** Charity Check also includes "weekly updates from the Internal Revenue Bulletin", which weakens the "monthly IRS files" framing.

---

## Reproduced calculations

**Process economics**
- **Sponsor pools (P01–P15):** low / base / high = $865,679 / $4,319,458 / $18,723,933 (`data/mission-2026-11-14/ai-process-economics.csv`).
- **Base gross capture:** A $647,919, B $805,102, C $329,404, D $1,809,438. All match the doc (`data/mission-2026-11-14/ai-process-economics.csv`).
- **P07 base:** pool $1,247,625 (1M × 1.5% × 90/60 × $55.45). C = (0.4×0.45 − 0.05) × L − $6,750 = $155,441 (`data/mission-2026-11-14/ai-process-economics.csv`).
- **P03 pessimistic:** (0.2×0.35 − 0.125) × $532,320 − $1,440 = −$30,718 (`data/mission-2026-11-14/ai-process-economics.csv`).
- **Inference:** P07 = (60k × $2 + 3k × $10) / 1M × 3 = $0.45 per case. That matches Anthropic list pricing ([V2A-01](https://platform.claude.com/docs/en/about-claude/pricing)).

**Entrant capital (2 × FTE × cost + 2 × non-headcount, $m)**

| Strategy | Low | Base | High |
|---|---:|---:|---:|
| S1 | 8.8 | 17.04 | 29.4 |
| S2 | 3.18 | 6.64 | 12.36 |
| S3 | 2.3 | 4.98 | 9.68 |

All match the doc.

**Grant-review savings:** 48,744 × 3% × 25/60 × $65 × 40% = $15,842. The same formula at 3.0M grants gives $975,000 (inputs: [Charityvest 2025 results](https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/); [Fidelity Charitable 2026 Giving Report](https://www.fidelitycharitable.org/insights/2026-giving-report.html); `research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`).

**Wages:** BLS May 2025 compliance-officer median $38.81. ECEC June 2026 ratio $46.89 / $32.82 = 1.4287, giving a loaded rate of $55.45 ([BLS OOH](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm); [BLS ECEC](https://www.bls.gov/news.release/ecec.nr0.htm)).

## Sensitivity result (key driver)

**"AI ranks last" is robust to QA and to s_C up to 0.5.** It changes only when ai_amenability is raised: ×2 leaves C last in 7/16. It also changes when s_C ≥ 0.6, and then only in P03, plus P14 at 0.8.

The conclusion is therefore an artifact of the assumed amenability and redesign shares, and of how option C is defined. It does not come from QA or from any measured evidence. The directional point, "prevent exceptions before automating their handling", is reasonable. The specific ranking should not be cited as a result.

## Overconfidence flags

1. **Economics doc, Exec #2.** "the structural reason is robust". In fact the ranking is fixed by the parameter caps.
2. **Economics doc, §4.3.** "QA intensity is the single most important AI parameter". This is contradicted by the sensitivity grid.
3. **Economics doc, §7.** "per-process AI cases fail at sub-Fidelity scale under every base assumption". The base assumptions are themselves unsourced.
4. **Entrant doc, Exec #3 and §8.** S3 has "the lowest scenario capital… fastest falsifiable test". The capital is an input, and the target segment is below break-even.
5. **Governance doc, Exec #2.** "AI mostly creates new risk". This is a rubric output with no incident evidence and no human-error baseline.
6. **Economics doc, §6.3.** The Circle Foundation case is described as "at institutional scale".

## Exact recommended corrections

1. **`ai-economics-replacement-analysis.md`, Exec #2.** Replace "This ranking is driven by stated assumptions (Section 5), but the structural reason is robust" with:
   > "This ranking is determined by stated assumptions: with A fixed at 15% and AI-amenability capped at 0.45, C cannot exceed A in any process (that requires a > 0.50). It is not evidence about AI performance. The directional point — prevent exceptions before automating their handling — rests on reasoning, not on the model." (`data/mission-2026-11-14/ai-process-economics.csv`)
2. **Same doc, §4.3 readings.** Replace "QA intensity is the single most important AI parameter" with:
   > "QA intensity decides whether AI value is positive; the ranking is driven mainly by the assumed AI-amenability (a) and redesign share (d), both unsourced. With QA = 0, C still ranks last in 12/16 processes at s_C = 40%." (rerun of `data/mission-2026-11-14/ai-process-economics.csv`)
3. **Same doc, §3 table and CSV `rank_base` for P07.** Annotate: "B and C within $512 (0.3%); treat as tied." (`data/mission-2026-11-14/ai-process-economics.csv`)
4. **Same doc, §4.4.** Add P09 to the list of processes where A clears $25k (`data/mission-2026-11-14/ai-process-economics.csv`).
5. **Same doc, §1 #5 and §6.3.** Add:
   > "Exception: Daffy, which operates its own sponsor (Daffy Charitable Fund), announced back-end AI that unifies charity data and 'flags issues for review' (2025-04-09; announced only)." ([FF News, 2025-04-09](https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/))

   Also change "at institutional scale" to "at one corporate DAF".
6. **Same doc, Benevity mentions.** Change "500+ clients" to "500+ clients across Grant Summaries and Match Assurance". Change "match decline rate" to "external match decline rate".
7. **Same doc, Chariot.** Replace "(vendor citing DAFRC)" with "(vendor figure, unattributed)".
8. **Same doc, Candid.** Change the text to:
   > "cut staff (Chronicle reports 42, about one-fifth; count not independently verified) and is repositioning as a data supplier to AI platforms."
9. **`ai-use-case-inventory.csv`.** Add Bonterra Que (2025-10-01, adjacent, act/recommend, announced, https://www.businesswire.com/news/home/20251001579571/en) and Bonterra Grantmaker (2026-02-19, announced). Change U20 `date_announced` to 2025-07-22, or note why it differs. Recount the §6.2 table.
10. **`ai-native-entrant-simulation.md`, Exec #3 and §8.** Replace "Recommended entry: Strategy 3" with:
    > "Preferred research probe: Strategy 3, conditional on measuring operating cost pools. On the repo's own parameters, $120k/yr requires ≈369k grants/yr from grant review alone, or ≈76k grants/yr if S3 captured all redesign and AI value in its scope; most independent and community-foundation sponsors are below both." (`research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`; `data/mission-2026-11-14/ai-process-economics.csv`; `data/mission-2026-11-14/entry-strategy-comparison.csv`)

    Replace "lowest scenario capital" with:
    > "lowest assumed capital (by headcount assumption; S3 needs ~42 customers for $5m ARR vs 5 for S1)." (`data/mission-2026-11-14/entry-strategy-comparison.csv`)
11. **Same doc, §6 S3 row and the CSV `falsifiable_signal_6_12m` (`data/mission-2026-11-14/entry-strategy-comparison.csv`).** Replace "zero false clears… model-assisted clearing" with:
    > "routine-tier clearing by deterministic, sponsor-approved rules only; AI may add flags or evidence but not clear (consistent with ai-governance-failure-modes.md §5)."
12. **Same doc, R9 and §8 condition 4.** Replace "Commentary… says §4966 guidance remains listed" with:
    > "The 2026–27 Priority Guidance Plan (2026-09-29) lists 'Guidance under sections 4966 and 6033 regarding certain donor advised fund arrangements', replacing the prior plan's final §4966 regulations item." ([KPMG](https://kpmg.com/us/en/taxnewsflash/news/2026/09/exempt-organization-projects-irs-priority-guidance-plan.html))

    Change condition 4 to "Forthcoming §4966/6033 guidance…".
13. **Same doc, §4 and §5.2.** Add the missing players:
    - Daffy for Developers (open APIs, 2023) as a second sponsor-of-record API ([Daffy for Developers](https://www.daffy.org/resources/daffy-for-developers)).
    - Goodstack (nonprofit verification and eligibility API) as an S2 competitor.
    - Every.org APIs.
    - Bonterra Que, Benevity and Blackbaud as incumbents able to bundle S3 features.
    - Givinga, Stellar/iPhi, DAFtech and Give Interactive as DAF-tech vendors.
14. **Same doc, §9 Q7.** Answer it: the RCF policy states that Charity Check "Includes the result of GuideStar's OFAC verification".
15. **Same doc, Endaoment custodians.** Replace "are named as supporting Endaoment DAF accounts" with "are named on Endaoment's institutions page ('The DAF follows the assets…'); custodial agreements not verified".
16. **Same doc, §5.4.** Note that the $65/h rate and exception model differ from the economics doc's $55.45/h model, and reconcile them (`research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`; `data/mission-2026-11-14/ai-process-economics.csv`).
17. **`ai-governance-failure-modes.md`, Exec #2.** Add:
    > "These counts are rubric ratings against unconstrained AI, with no observed DAF AI incidents and no baseline for human error rates."

## Do the headline conclusions survive?

- **Survive:**
  - Inference cost is immaterial.
  - Sponsor approval authority stays human or deterministic.
  - The agentic risk surface is donor-side (TIFIN, Daffy MCP).
  - Redesign before AI is directionally sound.
  - The §4966 proposed rules are not final.
- **Survive only as assumption-bound statements:** "AI ranks last" and "AI pays only as a shared platform".
- **Do not survive as written:**
  - "QA is the most important parameter".
  - The unconditional S3 recommendation.
  - The cross-doc inconsistency on model-assisted clearing.

## Primary sources consulted (2026-11-14)

- **Pricing and wages:** [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing); [BLS OOH compliance officers](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm); [BLS ECEC Sept 2026 release](https://www.bls.gov/news.release/ecec.nr0.htm).
- **Grant volumes and sponsor sources:** [Fidelity Charitable 2026 impact snapshot](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-impact-snapshot.pdf); [DAFgiving360 2025 results](https://www.dafgiving360.org/press-release/2025-results); [Charityvest 2025 results](https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/) (Foundation Source); [RCF Grantmaking Due Diligence Policy PDF](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf) (text extracted).
- **AI and product announcements:** [TIFIN Louise PR Newswire](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); [Daffy MCP docs](https://docs.daffy.org/agents/mcp); [Daffy AI release (FF News)](https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/); [Endaoment institutions](https://endaoment.org/institutions); [Benevity Live 2026](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026); [Chariot gift processing release](https://givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits); Chronicle on [Candid](https://www.philanthropy.com/news/candid-cuts-staff-bets-its-future-on-ai/) (headline only) and on [Circle Foundation](https://www.philanthropy.com/news/ai-recommends-humans-decide-circle-foundations-bet-on-agentic-philanthropy/); [McGovern Grant Guardian](https://www.mcgovern.org/how-foundations-are-using-ai-to-vet-grantees/); [Anthropic Claude for Nonprofits](https://www.anthropic.com/news/claude-for-nonprofits); [CEP 2025](https://cep.org/news/press-releases/as-ai-use-proliferates-in-the-social-sector-new-study-reveals-lagging-support-for-equitable-ai/); [Blackbaud Development Agent GA](https://www.nasdaq.com/press-release/blackbaud-launches-new-category-ai-agent-general-availability-its-first-agent-goodtm); [Bonterra Que (Business Wire 2025-10-01)](https://www.businesswire.com/news/home/20251001579571/en/Bonterra-Launches-Que-The-First-Agentic-AI-Platform-for-Funders-Nonprofits-and-Supporters).
- **Regulation:** [KPMG summary of the 2026–27 Priority Guidance Plan](https://kpmg.com/us/en/taxnewsflash/news/2026/09/exempt-organization-projects-irs-priority-guidance-plan.html); [GT Law on the Colorado AI Act](https://www.gtlaw.com/en/insights/2025/9/colorado-delays-comprehensive-ai-law-with-further-changes-anticipated).
- **Missing-player evidence:** [Daffy for Developers](https://www.daffy.org/resources/daffy-for-developers); [Goodstack docs](https://docs.goodstack.io/docs/guides/Cause%20verification/); [Every.org docs](https://docs.every.org/docs/intro).

URLs are in the register.
