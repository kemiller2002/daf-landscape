# Validation wave 28: new directions N23–N26 (sponsor marketing spend, executive compensation, AI product census, charity ratings integrations)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave28.
**Register:** [`validation-register-wave28.csv`](../../data/mission-2026-11-14/validation-register-wave28.csv), rows V28-01 to V28-39.
**Documents validated:**
- N23: [direction-sponsor-marketing-spend.md](direction-sponsor-marketing-spend.md), `sponsor-marketing-spend-2021-2025.csv` (476 rows) and `scripts/mission_sponsor_marketing.py`
- N24: [direction-sponsor-executive-compensation.md](direction-sponsor-executive-compensation.md), `sponsor-executive-compensation-2021-2025.csv` (1,277 rows) and `scripts/mission_sponsor_compensation.py`
- N25: [direction-ai-product-census.md](direction-ai-product-census.md) and `philanthropy-ai-products-2026.csv` (30 rows)
- N26: [direction-charity-ratings-integrations.md](direction-charity-ratings-integrations.md), `charity-data-provider-integrations-2026.csv` and `relationship-graph-edges-additions-25.csv`

**Method:** public sources only. I did not log in, submit forms, solve or bypass CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching any page on it, checking the ClaudeBot, anthropic-ai and `*` groups; hosts whose robots.txt could not be read were not fetched. **I did not use crt.sh.** For each claim I formed a verdict from the primary source first and compared it with the documents afterwards. The sources were:
- **N23 and N24:**
  - a **re-run of both scripts** on a copy of the repo in scratch, each with a **fresh, empty cache** and `--fetch`, so all 455 (N23) and 225 (N24) returns were re-streamed from the GivingTuesday mirror (robots.txt 404, no rules) or IRS TEOS (apps.irs.gov robots.txt redirects to a 404 page, no rules);
  - an **independent regex parse of the full XML** of 13 returns for line 12 and line 11a, and of 13 TY2024 returns for Part VII columns D/E/F, institutional trustees, Schedule J Part II totals and Schedule O text.
- **N25:** 20 vendor and sponsor pages re-fetched (TIFIN release and GiveClear guidelines, Daffy MCP docs, Fidelity Virtual Assistant terms, Foundation Source interview, SmartSimple, Fluxx, YourCause, Blackbaud opt-in help and Development Agent, Givebutter Magic, recap and pricing, Bloomerang, Salesforce, Bonterra, GoFundMe newsroom, Charity Navigator Horizon release, Ren, Givinga); three Blackbaud releases on "Blackbaud Copilot" (nasdaq.com, nonprofitpro.com) found by web search.
- **N26:** Fidelity research and fraud pages; two Give Lively pages; the BofA donor guide PDF (bofa.donorfirst.org, robots 404); Groundswell's DAF page; CN API terms, attribution, plans and developer pages; CN about page; two CN help articles; the session's Pub 78 copy (Last-Modified 2026-11-11); irs.gov robots.txt.

## Headline

The four documents hold up on their numbers. Of 39 claims, 27 are confirmed, 9 partially confirmed and 3 contradicted; none is unverifiable. **Both 990 scripts reproduce byte-for-byte** from a fresh download of every return.

**What holds independently:**
- **N23 marketing spend:**
  - The re-run CSV is identical to the repo file (455 returns fetched, 438 rows, cost-cache check 290 / 0 / 148).
  - Pooled TY2021–24: affiliated-commercial $21.70m, 1.39 bps, $147 per net new account; ex-Schwab $1.36m, 0.11 bps, $14; independent $3.15m, 0.41 bps, $64; digital-first $0.17m, 1.70 bps (6.6 bps with line 24); CFs $67.2m, $7,981, allocated 12.7 bps and $5,237.
  - Schwab $20.34m, 5.43 bps, $389.7. Fidelity reports line 12 as **0** (not blank) and line 11a of $121.2–179.9m. Endaoment $648 with line-24 "SALES & MARKETING" ($216,226; $264,674).
  - Rank correlations: CF −0.252 (n=55), −0.044 (n=53); all −0.338 (n=99), −0.187 (n=97).
  - 13 of 13 line-12 values match the filed XML.
- **N24 executive compensation:**
  - The re-run CSV is identical (225 of 225 returns, 1,019 person rows). Elasticity 0.225 (r² 0.341, n=21); 0.081 / 0.046 across 34.
  - 10 of 12 affiliated sponsors carry a $0 top officer or only an institutional trustee. DAFgiving360 $967,879 and Vanguard $608,684 equal Schedule J.
  - The three Schedule O employer statements are verbatim. BofA's trustee line is $24,062,159.
  - Pooled staff cost: 2.88 bps (affiliated) vs 78.67 bps (CFs). Per $bn of DAF assets: NPT $14,336, DAFgiving360 $20,440, Vanguard $22,534; CF median $733,697. CF median top pay $725,134.
  - Column-E shares: Greater Horizons 90.2%, The Signatry 93.5%, UCLA Foundation 84.9%. Column E is never positive at an affiliated sponsor.
  - Trends: CF pay +6.6%/yr against DAF assets +4.5%; independent pay +3.4% against assets +25.5%.
  - 13 sponsors' Part VII and Schedule J values match the XML; 39 of 39 TY2024 top officers over $150k reconcile to Schedule J.
- **N25 AI census:** the TIFIN Louise, Daffy MCP, Fidelity assistant, Foundation Source (dated 2026-10-28), SmartSimple, Fluxx Finn, YourCause, Blackbaud opt-in, Blackbaud Development Agent, Bloomerang Penny, Salesforce Agentforce, Bonterra Que and Givebutter quotes were all found on the live pages, as was Givebutter Plus "Starting at $29/month". Ren and Givinga pages carry no AI terms. RED = 0 is consistent with §7.
- **N26 ratings integrations:**
  - CN Giving Basket: "The Chariot processing fee is 2.9% on all DAF payments".
  - BofA's 9/2025 guide: "search the GuideStar database". Groundswell: "Built-In Integration with Candid's Guidestar".
  - CN API terms ("Last updated October 2026"): "non-sublicensable"; linkback required; ratings "may not be used in any other calculation or manipulated"; 30-day termination.
  - CN rates "more than 245,000 charities" of 1.7 million; 245,000 ÷ 1,437,291 Pub 78 lines = 17.05%.
  - The $2.17bn church code-10 figure matches the recipient-screen table.

**What needs correcting or qualifying:**
1. **"Blackbaud Copilot" (N25, V28-31) — contradicted.** Blackbaud named its generative-AI assistant "Blackbaud Copilot": in Impact Edge (2024-07-29), as a technical preview in Raiser's Edge NXT and Financial Edge NXT (2024-10-07), and as "an early look at Blackbaud Copilot" for RE NXT (2025-05-06). Whether Chat for Blackbaud AI is its rename was not established.
2. **irs.gov access log (N26, V28-39) — contradicted.** irs.gov's robots.txt disallows `/charities-non-profits/tax-exempt-organization-search` for all agents, and that prefix covers the TEOS bulk-downloads page the doc cites as [F]. The page should not have been fetched. The facts it supports are carried in the repo already.
3. **Prior-count provenance (N23, V28-10) — contradicted.** The first-year DAFRC priors are not "filed in all but Endaoment's FY2021 row". Schwab's TY2021 prior (76,310) is also "NPT historical data", and four priors are DAFRC "Imputed".
4. **Schwab functional split (N23, V28-05).** Schwab is 100% in the fundraising column. 97% is the affiliated group's share.
5. **CF 18.4 bps basis (N23, V28-04).** This ratio uses only rows with Schedule D contributions ($66.17m of line 12). $67.2m ÷ $35.96bn = 18.7 bps.
6. **N24 wording (V28-19, V28-20, V28-21):**
   - The independent row's DAF-asset growth is over 6 matched sponsors, not the "4 paid".
   - NPT's former President & CEO's $1,035,821 is column D; D+E+F is $1,063,757.
   - "6–9×" self-staffed nationals is 3.5–9× once AEF (15.0 bps) is included.
7. **Givebutter GREEN (N25, V28-28, V28-30):**
   - Stretch goals "automatically increase" and suggested amounts are "automatically matched to … donor's device". This is not a flag-only role under §7, so the row is a GREEN/AMBER boundary case.
   - The sub-labels (low, unverified, boundary) are local to the census; §7 defines only GREEN, AMBER and RED.
8. **Quote fixes (N25):**
   - Fluxx says "1:1 credit to dollar", not "1 credit per dollar".
   - Bloomerang's text is "… assign follow-ups, or create donor segments".
   - The GoFundMe Pro release does not mention ask amounts or nudges.
9. **Fidelity "for reference purposes only" (N26, V28-33).** The phrase qualifies the CHIP high-impact list, not the CN and GuideStar links. The Giving Compass widget sentence was not in either page's static HTML on re-fetch.

## Limits

- **Not fetched:** candid.org, give.org, dafgiving360.org and the other hosts N26 lists as blocked; the Fluxx and Bonterra press releases (aggregator/robots issues, as in the docs); pro.gofundme.com.
- **Carried figures:** the $2.17bn church code-10 figure was checked against the screen's table and aggregates, not re-aggregated from Schedule I lines.
- **Not re-checked:**
  - N23: the CF top-8 table and the line-24 broad matches.
  - N24: the five-highest-paid role tallies (§7).
  - N25: Chariot, Instrumentl, Candid, DonorSearch and Submittable rows.
  - N26: Goodstack, Pledge, Every.org and Benevity coverage claims, and edges EY003–EY020.
- **Vendor pages change.** All quotes are as of 2026-11-15.

## Exact corrections

### `research/mission-2026-11-14/direction-sponsor-marketing-spend.md`
1. **§1 item 2, Schwab functional split.**
   - **Find:** "and it is 97% in the fundraising column **[F/C]**."
   - **Replace with:** "and it is 100% in the fundraising column (97% for the affiliated group as a whole) **[F/C; V wave 28]**."
2. **§1 item 1, CF bps basis.**
   - **Find:** "   - For digital-first sponsors, about 6.6 bps once Endaoment's \"Sales & marketing\" on line 24 is added."
   - **Replace with:** "   - For digital-first sponsors, about 6.6 bps once Endaoment's \"Sales & marketing\" on line 24 is added.\n   - The bps column is Σ/Σ over rows with Schedule D DAF contributions > 0. For community foundations that numerator is $66.2m. $67.2m ÷ $36.0bn would give 18.7 bps [V wave 28]."
3. **§2.5, prior-count provenance.**
   - **Find:** "That row is flagged `prior_count_from_dafrc` and is filed in all but Endaoment's FY2021 row, whose source is \"NPT historical data\"."
   - **Replace with:** "That row is flagged `prior_count_from_dafrc`. Of 108 such priors, 102 are DAFRC \"IRS 990\" values. Two are \"NPT historical data\": Schwab TY2021 (76,310, the base of its $390) and Endaoment TY2021. Four are DAFRC \"Imputed\": one community foundation TY2021–23 and Endaoment TY2023, whose Schedule D count of 6,000 is out of line with 331 and 1,213 [V wave 28]."

### `research/mission-2026-11-14/direction-sponsor-executive-compensation.md`
1. **§0 item 6, trends table.**
   - **Find:** "| Independent nationals (4 paid) | +3.4% | +16.1% | **+25.5%** | fell from $140,879 to $124,880 |"
   - **Replace with:** "| Independent nationals (4 paid; DAF assets over all 6 matched) | +3.4% | +16.1% | **+25.5%** | fell from $140,879 to $124,880 |"
2. **§0 item 4, multiple.**
   - **Find:** "per $bn, community-foundation pay is 10–51× that of the four self-staffed nationals."
   - **Replace with:** "per $bn, community-foundation pay is about 10–51× that of the four self-staffed nationals (9.6× AEF, 51× NPT) [V wave 28]."
3. **§3 notes, NPT former officer.**
   - **Find:** "a former President & CEO is also listed, with $1,035,821 [F]."
   - **Replace with:** "a former President & CEO is also listed, with $1,035,821 in column D ($1,063,757 D+E+F) [F; V wave 28]."
4. **§9, CF vs self-staffed staff cost.**
   - **Find:** "That is still 6–9× the self-staffed nationals."
   - **Replace with:** "That is still about 3.5–9× the self-staffed nationals: 6–9× against NPT, DAFgiving360 and Vanguard, and 3.5× against AEF's 15.0 bps [V wave 28]."

### `research/mission-2026-11-14/direction-ai-product-census.md`
1. **§1 item 4, Fluxx pricing.**
   - **Find:** "Pricing is \"1 credit per dollar\" in credit bundles"
   - **Replace with:** "Pricing is \"1:1 credit to dollar\", with credits \"purchased as bundles\" [V wave 28]"
2. **§1 item 5, Bloomerang quote.**
   - **Find:** "\"launch campaigns, assign follow-ups, and create donor segments\""
   - **Replace with:** "\"launch campaigns, assign follow-ups, or create donor segments\""
3. **§1 item 5, Givebutter boundary.**
   - **Find:** "Most features are free, and AI custom reports need Givebutter Plus \"starts at $29/month\""
   - **Replace with:** "Two AI outputs change without per-action approval: stretch goals \"automatically increase as you raise more\", and suggested amounts are \"automatically matched to your campaign type, cause, and donor's device\". The GREEN call is therefore a GREEN/AMBER boundary case under §7's \"flag-only\" test [V wave 28]. Most features are free, and AI custom reports need Givebutter Plus \"starts at $29/month\""
4. **§1 item 8, Blackbaud Copilot.**
   - **Find:** "**\"Blackbaud Copilot\":** no product by that name. The nearest are Chat for Blackbaud AI and the Blackbaud agent for Microsoft 365 Copilot (2026-08-10 [R])."
   - **Replace with:** "**\"Blackbaud Copilot\":** Blackbaud used this name for its generative-AI assistant: in Impact Edge (release 2024-07-29), as a technical preview in Raiser's Edge NXT and Financial Edge NXT (2024-10-07), and as \"an early look at Blackbaud Copilot\" for RE NXT (2025-05-06) [V wave 28]. The current RE NXT features found are Chat for Blackbaud AI and the Blackbaud agent for Microsoft 365 Copilot (2026-08-10 [R]). Whether Chat is a rename of Blackbaud Copilot was not established."
5. **§1 item 8, Classy.**
   - **Find:** "Its AI features are personalised ask amounts and nudges, and the release cites"
   - **Replace with:** "The release says GoFundMe Pro \"fuses AI innovation with millions of fundraising data points\". The personalised ask amounts and nudges are not in this release (secondary source only) [V wave 28]. It cites"
6. **§2, overlay notes.**
   - **Find:** "- **\"AMBER (low)\"** marks read, search, scoring or drafting features with undocumented controls."
   - **Replace with:** "- The sub-labels below and in the table are local to this census. evidence-quadrant-methodology.md §7 defines only GREEN, AMBER and RED [V wave 28].\n- **\"AMBER (low)\"** marks read, search, scoring or drafting features with undocumented controls."

### `research/mission-2026-11-14/direction-charity-ratings-integrations.md`
1. **§0, CN embedding row, Fidelity.**
   - **Find:** "\"for reference purposes only\" and points to"
   - **Replace with:** "under \"Tools and resources\" (the page's \"for reference purposes only\" disclaimer qualifies its CHIP high-impact list, not these links [V wave 28]) and points to"
2. **§0, CN embedding row, widget.**
   - **Find:** "(\"The Giving Compass Widget is provided by an independent third party\") [F]."
   - **Replace with:** "(\"The Giving Compass Widget is provided by an independent third party\") [F; not in the static HTML on the wave-28 re-fetch, so possibly script-rendered]."
3. **§0, search row, Groundswell.**
   - **Find:** "- **Groundswell:** \"Candid GuideStar integration\" [C: E155]."
   - **Replace with:** "- **Groundswell:** \"Built-In Integration with Candid's Guidestar\" [F wave 28; C: E155]."
4. **§0, Gaps row, churches.**
   - **Find:** "and another **$1.19bn** of church-labelled lines are absent from both [C]."
   - **Replace with:** "and another **$1.19bn** of church-labelled lines are absent from both [C]. Almost all of the $2.17bn is group-ruling subordinates (screen §5: church + group subordinate $2.15bn), so their exemption is verifiable through the central organisation; the gap is in ratings, not eligibility [V wave 28]."
5. **§0, Coverage row, 17%.**
   - **Find:** "That is **about 17% of the 1,437,291 Pub 78 records** [I; C: recipient screen]."
   - **Replace with:** "That is **about 17% of the 1,437,291 Pub 78 records** [I; C: recipient screen; V wave 28]. Pub 78 also lists private foundations and others CN does not rate, so this is a share of all records, not of rateable charities."
6. **§1, access log.**
   - **Find:** "docs.endaoment.org, www.irs.gov, www.prnewswire.com, www.nptechforgood.com."
   - **Replace with:** "docs.endaoment.org, www.prnewswire.com, www.nptechforgood.com. **Correction (wave 28):** www.irs.gov's robots.txt disallows `/charities-non-profits/tax-exempt-organization-search` for all agents, a prefix covering the TEOS bulk-downloads page. That page should not have been fetched, and its facts are relabelled [C]."
7. **§2.10, bulk files.**
   - **Find:** "([TEOS bulk downloads, reviewed 2026-09-16](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads)) [F]."
   - **Replace with:** "([TEOS bulk downloads](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads); path disallowed by irs.gov robots.txt, so not to be fetched) [C: repo IRS file use; V wave 28]."
8. **Source register, R27.**
   - **Find:** "| R27 | [IRS TEOS bulk downloads](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads) | government | reviewed 2026-09-16 | F |"
   - **Replace with:** "| R27 | [IRS TEOS bulk downloads](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads) | government | robots-disallowed path; not to be fetched | C |"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.24.** Add "### 11.25 New directions N23–N26 (validated, wave 28)", containing the paragraph below. If §11.25 is already taken, use the next free number.

   > **New directions N23–N26 (validated, wave 28).**
   > - **Sponsor marketing spend (Form 990 line 12, TY2021–24; both scripts reproduce exactly).**
   >   - Reported advertising is tiny at nationals: affiliated-commercial sponsors $21.7m (1.39 bps of DAF contributions), of which Schwab is $20.3m (about $390 per net new account). Without Schwab it is $1.36m.
   >   - Independent nationals: $3.1m (0.41 bps). Digital-first: $0.17m (1.7 bps; 6.6 bps with Endaoment's line-24 marketing).
   >   - Fidelity reports $0 on line 12 and $121–180m a year of administrator fees on line 11a. Parent- and platform-paid marketing is off the 990, so line 12 is a lower bound.
   >   - Community foundations: $67.2m, about 18 bps of DAF contributions (12.7 bps allocated) and $7,981 per net new account. Across CFs, advertising intensity is not positively ranked with account growth (ρ −0.25, n=55).
   > - **Executive compensation (top 50, TY2024).**
   >   - 10 of 12 affiliated-commercial sponsors carry no paid executive on their own 990. Staff are the parent's (Schedule O: FMR services agreement; 474 MS Services/Eaton Vance; Schwab employees), or a bank trustee is paid (BofA $24.1m).
   >   - Pooled staff cost: 2.9 bps of DAF assets for affiliated sponsors against 78.7 bps at community foundations.
   >   - Top-officer pay per $bn of DAF assets: NPT $14k, DAFgiving360 $20k and Vanguard $23k, against a CF median of $734k. Median CF top pay is $725k and barely scales with size (elasticity 0.23).
   >   - Related-organisation pay is concentrated at Greater Horizons (90%), The Signatry (93%) and the UCLA Foundation (85%).
   > - **AI products (30 rows).**
   >   - No product meets the RED test. Only TIFIN Louise and Daffy's MCP server can move DAF money, and both end in sponsor review. Fidelity's assistant is search only. Foundation Source's CEO (2026-10-28) describes a roadmap AI screening tool framed as a flag for review.
   >   - Grantmaking tools (SmartSimple, Fluxx Finn, YourCause) document opt-in, no-training and human-decision controls (provisional GREEN). Givebutter Magic is a GREEN/AMBER boundary case.
   >   - "Blackbaud Copilot" did exist as a Blackbaud assistant name in 2024–25. Classy is now GoFundMe Pro.
   > - **Charity ratings in DAF platforms.**
   >   - No top-20 sponsor shows CN ratings in its grant flow. Where a search vendor is named, it is Candid/GuideStar (BofA's 2025 guide; Groundswell). CN's own Giving Basket takes DAF grants via Chariot DAFpay at 2.9%.
   >   - CN's API licence is non-sublicensable, requires a linkback and bars using ratings "in any other calculation", which constrains AI rankers.
   >   - CN rates 245,000+ charities, about 17% of Pub 78 records.
   >   - Church grants in the BMF but not Pub 78 ($2.17bn in the top-50 sample) are mostly group-ruling subordinates: a ratings gap, not an eligibility gap.

## Data-file notes (not .md; for the owning agent)

- **`sponsor-marketing-spend-2021-2025.csv`:** no value changes; all 13 spot-checked line-12 values match the XML. Consider a `group_pooled` note that `adv_bps_of_daf_contrib` uses the rows-with-contributions numerator. The Endaoment TY2023 `sd_daf_count` 6,000 is as filed but anomalous.
- **`sponsor-executive-compensation-2021-2025.csv`:** no change; 13 sponsors' Part VII/Schedule J values match.
- **`philanthropy-ai-products-2026.csv`:**
  - AIP13 `pricing_published`: use "'1:1 credit to dollar'".
  - AIP25 `what_it_does`: use "or" in the Penny quote if quoted.
  - AIP28 `ai_overlay`: "GREEN (provisional; AMBER boundary: auto stretch goals and suggested amounts)".
  - AIP18: add the 2024–25 "Blackbaud Copilot" name history.
  - AIP29: tag ask amounts and nudges [R] unless pro.gofundme.com is read.
- **`charity-data-provider-integrations-2026.csv`:** CDP-049 `evidence_tag` F → C (irs.gov path disallowed by robots.txt).
- **`relationship-graph-edges-additions-25.csv`:** EY001 and EY002 confirmed (2.9% and 2.5% verbatim); others not re-checked.
