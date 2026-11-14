# Analyst, consultancy and education landscape for DAFs and philanthropy technology

**Date:** 2026-11-14. **Workstream:** analyst-and-education (ANL). **Status:** desk research from public sources only. Nothing was bought and nothing was logged in to. Paywalled items are labelled **abstract only**, meaning we read only the title, date, abstract or press release. Figures reported second-hand are labelled **secondary**.

**Companion files:**
- [`data/mission-2026-11-14/analyst-education-sources.csv`](../../data/mission-2026-11-14/analyst-education-sources.csv): the source register, one row per source.
- [`data/mission-2026-11-14/queue-proposals-analyst-education.csv`](../../data/mission-2026-11-14/queue-proposals-analyst-education.csv): 12 proposed research questions, prefixed P-ANL-.

**Relation to the rest of the repo:** this note checks how outside analysts and educators line up with the evidence-based findings in [strategic-synthesis.md §A](strategic-synthesis.md). It does not re-derive DAFRC market figures. It adds adviser-adoption, HNW-penetration and teaching-claim evidence that the repo lacked. Before this note, the repo held only the "669 advisers / 75% discuss philanthropy" headline from the DAFRC adviser study ([daf-market-demand-and-evidence-gaps-2026-11-11.md](../daf-market-demand-and-evidence-gaps-2026-11-11.md)).

---

## 1. Bottom line

1. **Mainstream technology analysts do not cover DAF technology.**
   - We found no Gartner Magic Quadrant, Hype Cycle or Peer Insights market, no Forrester Wave or Now Tech, and no IDC, Celent, Datos Insights or Javelin landscape that treats DAF sponsor platforms (recordkeeping, grant processing, donor and adviser portals) as a category.
   - Gartner Peer Insights reaches adjacent categories only: non-profit accounting, university alumni advancement and state/local grant management ([Gartner Peer Insights: Blackbaud in non-profit accounting](https://www.gartner.com/reviews/market/non-profit-accounting-software/vendor/blackbaud); [Gartner Peer Insights: Raiser's Edge NXT in alumni advancement](https://www.gartner.com/reviews/market/university-alumni-advancement-systems/vendor/blackbaud/product/raiser-s-edge-nxt); [Gartner Peer Insights: state and local grant management](https://www.gartner.com/reviews/market/us-state-and-local-grant-management-solutions)).
   - The last philanthropy-specific analyst titles we found are Celent's *World of Philanthropy* (2003), which is about private foundations ([Celent](https://www.celent.com/en/insights/312707366)), and an Aite-Novarica (now Datos Insights) Impact Report from September 2021 ([Datos Insights](https://datos-insights.com/?p=13920)).
   - The absence is itself a finding. A market with about $328bn in assets ([DAFRC Annual DAF Report 2025 on ScholarWorks](https://scholarworks.gvsu.edu/jcppubs/116); [InvestmentNews, Oct 28 2026](https://www.investmentnews.com/practice-management/charitable-giving-season/268629)) has no independent vendor evaluation. Vendor share claims such as Ren's (synthesis §A4) therefore go unchallenged by any analyst.
2. **The research that does exist is adviser- and donor-behaviour research, and most of it is commissioned by sponsors.** The main 2024–26 sources are:
   - the DAFRC adviser study (669 advisers);
   - TPI's 2026 Study of the Philanthropic Conversation, co-sponsored by DAFgiving360 and Foundation Source;
   - Fidelity Charitable's 2024 adviser study;
   - the Bank of America / Lilly School Study of Philanthropy (2025);
   - Goldman Sachs' *Philanthropy in Focus* (2026);
   - Schwab's RIA Benchmarking.

   Each is cited in §4. They supply adviser-adoption and HNW-penetration figures the repo did not have.
3. **Teaching repeats aggregate payout without its denominator.** The director of the American College's Center for Philanthropy and Social Impact launched the new DAFCP credential in 2026. His trade article "Five core truths" tells advisers that DAFs "pay out more than commonly assumed" (about 25.2% against 8.1% for private foundations) and that sponsor inactivity rules "keep money moving" ([WealthManagement.com, Jul 29 2026](https://www.wealthmanagement.com/philanthropy/five-core-truths-about-donor-advised-funds)). These are the beliefs that synthesis §A2 finds misleading as stated. Account counts are taught with the wrong denominator too: CCS's 2024 landscape report says "2 million DAFs" ([CCS Philanthropic Landscape 2024](https://hub.ccsfundraising.com/hubfs/Images%20and%20Files/Corporate%20Meeting%20Team/Publications/Philanthropic%20Landscape/2024%20Landscape/2024-Philanthropic-Landscape-13th-Edition_CCS-Fundraising.pdf)).
4. **The 2026 tax changes are taught correctly in current material.** IRS guidance, CPA firms and sponsor learning centres all state that DAF gifts are excluded from the new nonitemizer deduction and that the 0.5%-of-AGI floor applies ([IRS newsroom](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize); [Fidelity Learning Center](https://fidelity.com/learning-center/personal-finance/charitable-giving-tax-changes); [CPA Practice Advisor, Feb 18 2026](https://www.cpapracticeadvisor.com/2026/02/18/planning-for-charitable-contributions-in-2026/178317/)). The risk lies in older "evergreen" explainers still in circulation (§5, T6).

---

## 2. Method and access

- **Searches:** run 2026-11-14 across analyst sites (Gartner, Forrester, IDC, Celent, Datos, Javelin, Cerulli, Morningstar, Kitces, T3), consultancies (BCG, McKinsey, Deloitte, Bain, Stax, CCS), academic and sector research (Lilly School, DAFRC/Johnson Center, CEP, Philanthropy Roundtable, IPS, NBER, Urban, Stanford PACS), curricula (The American College CAP and DAFCP, FINRA, law school syllabi, CE providers) and secondary trade press (InvestmentNews, ThinkAdvisor, WealthManagement.com, Chronicle of Philanthropy).
- **Access labels** (used in the CSV):
  - `free`: full text read.
  - `abstract-only`: we read the title, abstract or summary page only, and the full text is behind a client login or paywall.
  - `paywalled`: blocked, and only secondary coverage was used.
  - `secondary`: reported via trade press because the primary source returned HTTP 403 to our fetcher. Examples: the DAFRC adviser report's executive summary on dafgiving360.org, ThinkAdvisor and Morningstar.
- **What we did not do:** we did not buy any report, register for any summary form, or log in to Gartner, Forrester or Cerulli. When a search surfaced no relevant title from a firm, we record that the search found none. We do not claim the firm has never published on the topic.

---

## 3. What analysts cover and what they do not

### 3.1 Coverage map

| Firm / source | What it publishes that touches DAFs or philanthropy tech | DAF platforms evaluated? | Access |
|---|---|---|---|
| **Gartner** | (1) Peer Insights review pages for Blackbaud products in "non-profit accounting software" and "university alumni advancement systems". Raiser's Edge NXT has a 3.9 rating from 19 ratings; Financial Edge NXT 3.4; YourCause CSRconnect 4.0 from 3 ratings ([Raiser's Edge NXT](https://www.gartner.com/reviews/product/raiser-s-edge-nxt); [YourCause CSRconnect](https://www.gartner.com/reviews/product/yourcause-crsconnect); [Financial Edge NXT](https://external.pi.gpi.aws.gartner.com/reviews/product/blackbaud-financial-edge-nxt)). (2) A "US state and local grant management solutions" market with 36 products ([Gartner](https://www.gartner.com/reviews/market/us-state-and-local-grant-management-solutions)). (3) *AI Agents: Use-Case Examples for Investment Services* (Oct 16 2025), aimed at asset- and wealth-management CIOs ([Gartner abstract](https://www.gartner.com/en/documents/7078098)). (4) The 2025 AI Hype Cycle places AI agents at the Peak of Inflated Expectations ([BigDATAwire coverage](https://www.hpcwire.com/bigdatawire/2025/09/12/ai-agents-debut-atop-gartner-hype-cycle-for-emerging-tech/)). A site search for "philanthropy", "donor-advised" or "charitable giving" returned only Gartner's own employee-giving pages ([Gartner careers](https://jobs.gartner.com/life-at-gartner/gartner-gives/gartner-s-season-of-giving/)). | **No.** No DAF category, no Magic Quadrant, no Hype Cycle entry found. Software Advice (a Gartner company) runs "FrontRunners for Nonprofit Donor Management" ([Givelify blog](https://www.givelify.com/blog/givelify-leading-nonprofit-donor-management/)). | Peer Insights free; research abstract only |
| **Forrester** | *Now Tech: Digital Wealth Management Platforms, Q4 2021* ([Forrester](https://www.forrester.com/report/now-tech-digital-wealth-management-platforms-q4-2021/RES176506)) and *Top wealth management technology investments in 2021* ([Forrester](https://www.forrester.com/report/the-top-wealth-management-technology-investments-in-2021/RES160675)). Neither abstract mentions philanthropy. A Forrester wealth-transfer finding is known to us only through a Foundation Source blog ([Foundation Source](https://foundationsource.com/blog/forrester-finds-half-of-firms-expected-to-lose-assets-during-the-great-wealth-transfer/)). | No | abstract only / secondary |
| **IDC / IDC Financial Insights** | No DAF or philanthropy-technology title found. | No | n/a |
| **Celent** | *World of Philanthropy: Entering the Mainstream?* (Mar 7 2003) covers private foundations as an alternative to DAFs and profiles Foundation Source ([Celent](https://www.celent.com/en/insights/312707366)). Current wealth research covers IT spending and technology trends with no philanthropy title ([Celent 2025 trends](https://celent.com/insights/554588578)). | No | abstract only |
| **Datos Insights (formerly Aite-Novarica)** | *Expanding Delivery of Philanthropic Advisory Across Wealth Management* (Sep 2021): 33 pages, 18 executive interviews. It says philanthropy "really can't be left out of wealth plans anymore" and that the sector "lags in fintech investment" ([Datos Insights](https://datos-insights.com/?p=13920)). | No vendor scoring visible | abstract only |
| **Javelin** | Wealth coverage (digital advice, custody, retirement) has no philanthropy title ([Javelin](https://javelinstrategy.com/wealth-management)). | No | n/a |
| **Cerulli Associates** | Projects $124tn in wealth transfer through 2048, with about $18tn going to charity (*U.S. HNW and UHNW Markets 2024*, via [NAPA-Net](https://www.napa-net.org/news/2024/12/wealth-transfers-expected-to-hit-%24124-trillion-through-2048/)). Finds that 18.7% of advisory practices by assets are "full wealth managers", the group most likely to integrate giving ([InvestmentNews, May 4 2026](https://www.investmentnews.com/practice-management/philanthropy-talk-is-now-standard-in-wealth-advising-but-advisors-are-still-misreading-client-motivations/266429)). The same article gives per-practice averages ($963.8bn per practice) that are implausible and probably a unit error, so do not reuse them. *State of U.S. Wealth Management Technology 2025* exists ([Cerulli](https://www.cerulli.com/reports/state-of-us-wealth-management-technology-2025)); we did not check whether it covers philanthropy. | No DAF-specific study found | secondary / abstract only |
| **Morningstar** | Personal-finance comparisons of Fidelity, Schwab and Vanguard Charitable. Vanguard charges 0.60% admin on the first $500k and 0.30% on the next $500k, has a $25k minimum and is rated lowest cost; expense tables are as of 9/30/2023 ([Morningstar on Vanguard's program](https://www.morningstar.com/personal-finance/our-take-vanguards-charitable-endowment-program); [Morningstar on Schwab](https://www.morningstar.com/funds/closer-look-schwabs-donor-advised-fund)). | Sponsor (product) comparison, not technology | free / 403 to fetcher on some pages |
| **Kitces** | (1) *Rules, strategies and tactics when using DAFs* (2015) says "not all donor-advised funds cooperate with outbound transfers" and that advisers can often be paid to manage DAF assets, subject to minimums ([Kitces](https://www.kitces.com/blog/rules-strategies-and-tactics-when-using-donor-advised-funds-for-charitable-giving/)). (2) A piece on custodian versus community-foundation DAFs that reports a planned 5% Schwab fee rise, from 25 to 26.25 bp (abstract only; [Kitces](https://www.kitces.com/?p=234336)). (3) The AdvisorTech Map; Foundation Source says it is listed there ([Foundation Source](https://foundationsource.com/blog/on-the-fintech-map-foundation-sources-tech-enabled-solutions-included-on-kitces-and-modus-news/)). We could not confirm a dedicated DAF category ([Kitces map](https://kitces.com/fintechmap/)). | Mapped at most, not evaluated | free / abstract only |
| **T3 / Inside Information** | The 2025 survey (more than 2,100 advisers) finds 41% use search or generative AI tools ([Financial Planning](https://www.financial-planning.com/news/ai-adoption-surging-in-wealth-management-t3-survey-shows); [Fintech Futures release](https://www.fintechfutures.com/press-releases/advyzon-named-best-all-in-one-software-solution-for-8th-consecutive-year-in-2025-advisor-software-survey-from-t3-and-inside-information)). We found no charitable-giving category in public summaries. | No | secondary |
| **BCG / McKinsey / Deloitte** | *AI is rewiring the wealth management business model* (BCG, 2026) ([BCG PDF](https://www.bcg.com/assets/2026/white-paper-ai-is-rewiring-the-wealth-management-business-model.pdf)). McKinsey argues AI commoditises technical planning and that about 80% of affluent households still prefer human advice ([Tribune India coverage](https://www.tribuneindia.com/news/business/nearly-80-affluent-households-still-prefer-humans-for-financial-advice-as-ai-reshapes-industry-value-mckinsey/)). Deloitte's 2026 prediction says agentic AI in wealth is mostly at pilot scale ([Deloitte Insights](https://www.deloitte.com/us/en/insights/industry/financial-services/financial-services-industry-predictions/2026/agentic-ai-wealth-management-productivity.html)). Philanthropy is not mentioned in the material surfaced. | No | free (not fully read) |
| **Bain / EY / KPMG / PwC** | No 2025–26 US DAF or philanthropy-technology report surfaced. | No | n/a |

### 3.2 Why the absence matters

- **No independent check on vendor claims.** Analyst coverage usually disciplines vendor share claims through briefings and reference checks. Without it, the share figures circulating in the trade press (Ren ">60%"; "powers half of US DAF assets") have no independent counterweight. That is why this repo had to bound them from Form 990 Schedule D data (synthesis §A4).
- **Buyers have no published criteria.** Sponsors have no published evaluation criteria for recordkeepers. Gartner's Peer Insights categories place DAF-adjacent vendors in other buyer markets: nonprofit accounting (Blackbaud), CSR and workplace giving (YourCause), and public-sector grants (Euna, SmartSimple). None of these is the DAF sponsor's buying decision.
- **The review evidence that exists is thin.** Ratings rest on 1–19 reviews per product ([Gartner Raiser's Edge NXT](https://www.gartner.com/reviews/product/raiser-s-edge-nxt); [Euna/SmartSimple comparison](https://www.gartner.com/reviews/market/us-state-and-local-grant-management-solutions/compare/product/euna-grants-vs-smartsimple-cloud-for-grants-management)). The recurring complaint themes are still usable as qualitative evaluation criteria (§6): cost for small organisations, an outdated interface, data-export limits, and fragmentation across modules. The Bonterra fragmentation theme comes via an aggregator ([RFP.wiki Bonterra vs Blackbaud](https://www.rfp.wiki/vendors/bonterra/blackbaud)).
- **AI coverage stops at the edge of DAFs.** Analysts cover AI in wealth management (Gartner, BCG, McKinsey, Deloitte, T3) and in nonprofits:
  - Salesforce's 7th Nonprofit Trends Report: 55% of 1,229 nonprofits piloting or using AI ([Salesforce PDF](https://www.salesforce.com/en-us/wp-content/uploads/sites/4/2025/05/s-org-7th-edition-nonprofit-trends-report-2025.pdf?d=pb)).
  - Virtuous/Fundraising.AI: 7% report major strategic impact ([NonProfit PRO](https://www.nonprofitpro.com/article/nonprofit-ai-adoption-hits-92-but-only-7-see-major-impact/)).
  - Bonterra: 91% of funders see AI transforming philanthropy and 92% worry about data ethics ([Business Wire, Nov 10 2025](https://www.businesswire.com/news/home/20251110626529/en/Bonterra-Report-91-of-Funders-See-AI-Transforming-Philanthropy-But-92-Worry-About-Data-Use-and-Ethics)).

  None covers AI inside DAF sponsor operations. The repo's AI-economics work (synthesis §B) therefore has no external analyst benchmark to test against. That is a gap, not a contradiction.

---

## 4. Data points the repo lacked

All figures are as reported by the named source. "Sponsor-commissioned" means a DAF sponsor funded or co-sponsored the work.

### 4.1 Adviser adoption and behaviour

| Metric | Value | Source / date | Notes and caveats |
|---|---|---|---|
| Advisers recommending DAFs "most of the time or always" | **35%**; 21% about half the time; 10% never | DAFRC, *Financial Planning in the Age of Donor Advised Funds* (2026), 669 advisers plus 6 focus groups ([WealthManagement.com](https://www.wealthmanagement.com/philanthropy/five-core-truths-about-donor-advised-funds); [ThinkAdvisor, May 13 2026](https://www.thinkadvisor.com/amp/2026/05/13/dafs-gaining-importance-in-advisor-client-relationships-report/)) | Secondary: the executive summary page returned 403. A sponsor (DAFgiving360) hosts it. |
| Advisers recommending private foundations most of the time or always | **4%** | same ([WealthManagement.com](https://www.wealthmanagement.com/philanthropy/five-core-truths-about-donor-advised-funds)) | DAFs are the second most recommended approach after direct giving. |
| Advisers' reasons for recommending DAFs | tax benefits 83%; flexible timing 69%; convenience 69%; estate planning 63% | DAFRC 2026 via search summary of the [DAFgiving360 release](https://www.dafgiving360.org/press-release/dafrc-advisor-study) | Secondary. |
| Who starts the philanthropy conversation | **61%** of clients say they do; **6%** say the adviser does | DAFRC 2026 via [InvestmentNews, Oct 28 2026](https://www.investmentnews.com/practice-management/charitable-giving-season/268629) | Conflicts with sponsor framing of advisers "driving" growth (T8). |
| Advisers who say raising philanthropy is standard practice | **90%** (80% in 2018); 96% call it an obligation | TPI 2026, 300 advisers and 103 HNW clients, Dec 2025–Jan 2026; co-sponsored by DAFgiving360 and Foundation Source ([InvestmentNews](https://www.investmentnews.com/practice-management/philanthropy-talk-is-now-standard-in-wealth-advising-but-advisors-are-still-misreading-client-motivations/266429); [TPI release, Apr 16 2026](https://tpi.org/?p=3256)) | Self-reported. Compare with the 6% figure above. |
| Advisers who have taken philanthropy education | **73%**; 85% plan to learn more | TPI 2026 ([TPI](https://tpi.org/?p=3256)) | Demand signal for curricula (§5). |
| Share of clients advisers discuss charitable planning with | **under 60%** | Fidelity Charitable 2024 adviser and investor surveys ([Fidelity Charitable](https://www.fidelitycharitable.org/insights/differentiating-with-charitable-planning.html)) | Sponsor-commissioned. Search coverage names Bellomy Research and 401 RIAs/BDs; the page does not. 2019 equivalent: 58% ([Fidelity Charitable 2019](https://www.fidelitycharitable.org/about-us/news/nearly-half-of-advisors-report-clients-adjusted-charitable-giving-strategy-in-response-to-tax-reform.html)). |
| Advisers who say charitable conversations attract new clients | 60% | Fidelity Charitable 2024 ([Fidelity Charitable](https://www.fidelitycharitable.org/insights/differentiating-with-charitable-planning.html)) | Sponsor-commissioned. |
| RIA firms offering charitable planning | **86%** (firms with $250m+ AUM); 80% in 2017; 63% in 2013 | Schwab RIA Benchmarking 2025 (1,288 firms) ([Schwab 2025 study page](https://advisorservices.schwab.com/insights-hub/perspectives/ria-benchmarking-study-2025); [Business Wire 2018](https://www.businesswire.com/news/home/20180712005176/en)) | The figure came from search summaries; the page returned 403. "Offered" is not "used". |
| Share of DAF assets associated with an adviser at DAFgiving360 | **77%**; more than 5,200 advisers | DAFgiving360 FY2025 Giving Report ([DAFgiving360](https://dafgiving360.org/giving-report)) | Sponsor self-report, via search summary (403 to fetcher). |
| Advisers recommending DAFs (New York area) | 70% | Stax, Jun 28 2023; 50 interviews and 70 surveys ([Stax](https://www.stax.com/insights/donor-advised-fund-survey)) | Small, regional sample. |
| Advisers using any generative or search AI tool | 41% | T3/Inside Information 2025 ([Financial Planning](https://www.financial-planning.com/news/ai-adoption-surging-in-wealth-management-t3-survey-shows)) | General adviser technology, not DAF-specific. |

### 4.2 HNW and affluent DAF penetration

| Metric | Value | Source / date | Notes |
|---|---|---|---|
| Affluent households holding a DAF | **~7% (2020)**, up from ~5% (2017). Unrounded: 6.6% and 4.5% | BofA / Lilly School 2021 study, 1,626 respondents ([Merrill summary](https://pbigaem.fs.ml.com/articles/2021-bank-of-america-study-how-affluent-households-gave-back-in-2020.html); [Pentera summary](https://pentera.com/blog/survey-affluent-donors-reveals-generous-giving-and-increased-use-planned-giving-instruments)) | Affluent means net worth ≥$1m or income ≥$200k. The decimals are secondary. |
| Affluent households with **any** giving vehicle | **24%** (2024) | 2025 BofA Study of Philanthropy ([BofA study page](https://www.privatebank.bankofamerica.com/articles/bank-of-america-study-of-philanthropy.html); [InvestmentNews, Sep 30 2025](https://www.investmentnews.com/practice-management/affluent-americans-are-leading-the-way-in-philanthropy-finds-bofa-study/262336)) | Covers all vehicles, not DAFs alone. 48% of $5–20m households have or plan one within 3 years. |
| Share of affluent **gifts** made through a DAF | **10%** (2024); all vehicles 18% (11% in 2015) | 2025 BofA study via [Chronicle of Philanthropy](https://www.philanthropy.com/article/fewer-rich-donors-gave-last-year-while-young-donors-gained-ground); [Family Wealth Report](https://www.familywealthreport.com/article.php/Affluent-US-Citizens-Give-More%2C-Volunteer-More%2C-But-Participation-Slips-%E2%80%93-BoA-Study-?id=205764) | Gift count share, not dollar share (secondary). |
| Advised HNW clients using a DAF | **51%**; 78% use at least one structured vehicle (43% in 2018) | TPI 2026, n=103 HNW clients ([TPI](https://tpi.org/?p=3256)) | Advised and sponsor-linked sample. Not population penetration. |
| UHNW giving, total | $250bn in 2025 | Goldman Sachs *Philanthropy in Focus* (2026), n=569 clients ([InvestmentNews, Nov 11 2026](https://www.investmentnews.com/practice-management/ultra-wealthy-donors-step-up-as-government-funding-retreats/268977)) | Its in-house GS DAF average grant rose from $17,500 (2016) to $77,500 (2025). |
| UHNW respondents citing tax deductions as a reason to give | 12%; 6% say taxes affect gift size | Goldman Sachs 2026 (same) | Compare with advisers' 83% "tax benefits" rationale (T9). |

**Reconciling these:** population penetration (about 7% of affluent households in 2020) and advised-client penetration (51% of TPI's HNW clients) differ by about 7×. These are different populations, not conflicting data. Any TAM or penetration statement should name which denominator it uses, following synthesis §A's denominator-substitution warning.

### 4.3 Fees: what analysts and educators circulate

- **Morningstar:** Vanguard 0.60% / 0.30%, with a $25k minimum, as of 2023 ([Morningstar](https://www.morningstar.com/personal-finance/our-take-vanguards-charitable-endowment-program)).
- **Chronicle survey (2009):** community foundations "typically 1% of assets or more". Minimum fees can push a small fund's effective rate to about 6%, as with Seattle Foundation's $1,500 minimum on a $25k fund ([Chronicle, Aug 20 2009](https://www.philanthropy.com/news/fees-vary-greatly-at-organizations-that-operate-donor-advised-funds/)).
- **Kitces:** a planned 5% Schwab fee increase, from 25 to 26.25 bp on the first tier (abstract only; [Kitces](https://www.kitces.com/?p=234336)).

The repo's [`sponsor-fee-schedules.csv`](../../data/mission-2026-11-14/sponsor-fee-schedules.csv) is more current than any analyst table we found. No analyst publishes an all-in cost (admin plus investment plus adviser fee) across sponsors. That is a gap the repo can fill (P-ANL-05).

### 4.4 Market-size figures as circulated

| Figure | Who circulates it | Status against repo |
|---|---|---|
| "$328B in DAF assets, 19% average annual growth, $91B contributed in 2024" | American College DAFCP page, citing DAFRC 2025 ([DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp)) | Consistent with DAFRC revised FY2024: $327.87bn assets and $90.57bn contributions ([InvestmentNews](https://www.investmentnews.com/practice-management/charitable-giving-season/268629)). |
| "2 million DAFs in the US" | CCS Philanthropic Landscape 2024, citing NPT ([CCS PDF](https://hub.ccsfundraising.com/hubfs/Images%20and%20Files/Corporate%20Meeting%20Team/Publications/Philanthropic%20Landscape/2024%20Landscape/2024-Philanthropic-Landscape-13th-Edition_CCS-Fundraising.pdf)) | Stale and denominator-blind. FY2024 reported accounts are 3.59m, of which 79.5% are processor pass-throughs (synthesis §A1). |
| "$617.2bn total US giving in 2025"; public-society benefit up 11.5% to $72.06bn, "driven in part by DAFs" | Giving USA 2026 via [Foundation Source](https://foundationsource.com/blog/key-takeaways-from-giving-usas-2026-report-on-philanthropy/) and [Bloomerang](https://bloomerang.com/blog/giving-usa-2026-report-nonprofit-fundraising-trends) | Giving USA counts DAF *contributions* as gifts to the public-society-benefit subsector. Adding DAF grants on top double counts (T10). Full report paywalled ([Giving USA](https://givingusa.org/product/2026-annual-report/)). |
| "$124tn wealth transfer, $18tn to charity" | Cerulli via [NAPA-Net](https://www.napa-net.org/news/2024/12/wealth-transfers-expected-to-hit-%24124-trillion-through-2048/); repeated by Goldman Sachs and TIFIN ([TIFIN](https://tifin.com/news/wealth-transfer-18-trillion-philanthropy-opportunity)) | A projection, not a DAF forecast. Vendors use it as a TAM. Treat it as `unsupported` for DAF-revenue purposes. |

---

## 5. How DAFs are taught, compared with the repo's evidence

### 5.1 The teaching ecosystem

- **The American College of Financial Services:**
  - *CAP®* (Chartered Advisor in Philanthropy) has a DAF unit, "Donor Advised Funds and Organizations Providing Them". Its readings draw on Fidelity Charitable and NPT reports ([Pittsburgh Foundation CAP overview](https://pittsburghfoundation.org/sites/default/files/CAP%20Course%20overview.pdf); [NCFP-hosted CAP overview 2020](https://www.ncfp.org/wp-content/uploads/2021/01/CAP-Course-Overview-2020-v-2.pdf)).
  - *DAFCP™*, launched 2026, is a 30-hour, six-module course. It costs $1,495, or $1,195 for nonprofit staff. Its modules are: Fundamentals; Tax (including OBBBA); Gift Acceptance; Investing and Grant Management (Notice 2017-73, international grants); Estate and Planned Giving (succession, versus private foundations and supporting organizations); and Ethics, Compliance and Technology ([DAFCP page](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp); [InvestmentNews](https://www.investmentnews.com/practice-management/dafcp-designation-launches-as-donor-advised-fund-giving-hits-record-pace/267580)).
  - The program director says the curriculum drew on 22 experts ([WealthManagement.com](https://www.wealthmanagement.com/philanthropy/five-core-truths-about-donor-advised-funds)).
- **Sponsor-run CE:**
  - Fidelity Charitable's Practice Management & Consulting curriculum offers free CE for CFP®, CIMA® and CPWA® credit ([Fidelity Charitable curriculum](https://fidelitycharitable.org/advisors/practice-management/curriculum.html); [virtual resource guide](https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/virtual-resource-guide.pdf)).
  - DAFgiving360 hosts the DAFRC adviser study and TPI "conversations" material ([DAFgiving360 TPI page](https://www.dafgiving360.org/tpi-conversations)).
  - NPT publishes adviser white papers ([NPT](https://www.nptrust.org/philanthropic-planning-and-the-client-review-npt)).
  - Other CE: Orion, NAPFA (an OBBBA/DAF webinar expiring Dec 31 2026) and my-cpe ([NAPFA](https://education.napfa.org/Listing/The-Future-of-Charitable-Giving-Tax-Efficient-Strategies-and-OBBBA-Impacts-12994); [Orion](https://orion.com/node/2723)).
  - **Implication:** much of the adviser education on DAFs is produced or paid for by DAF sponsors. That is an incentive alignment to note in [industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md).
- **Universities:**
  - The Lilly School's PHST-P 323 *Donor Motivation I* lists DAFs among donor vehicles ([IU bulletin 2025–26](https://bulletins.iu.edu/iuin/2025-2026/schools/philanthropy/courses/index.shtml)). The Fund Raising School runs a DAF research webinar with Shaker and Heist ([Lilly School](https://philanthropy.indianapolis.iu.edu/professional-development/courses-seminars/the-fund-raising-school/september-webinar.html)).
  - NYU Law's Tax-Exempt Organizations course teaches DAFs as a "private foundation alternative" ([NYU NCPL course descriptions](https://ncpl.law.nyu.edu/?p=36); [Spring 2026 syllabus](https://ncpl.law.nyu.edu/wp-content/uploads/2026/06/Complete-Spring-2026-TEO-Syllabus.pdf)).
  - UF Law's Willis syllabus lists "advising a donor advised fund" as an objective (2021 version) ([UF Law 2021](https://www.law.ufl.edu/law/wp-content/uploads/Willis-Tax-Exempt-Organizations-Fall-2021-Syllabus.pdf)).
  - We found no Stanford GSB, Columbia or Harvard Hauser DAF syllabus publicly.
- **Regulators:**
  - FINRA's "Investing with Charitable Giving in Mind" (Sep 4 2024) says the sponsor "has the final say on which charity receives the donations" ([FINRA](https://www.finra.org/investors/insights/charitable-giving)).
  - Investor.gov has a glossary entry, which returned 403 to our fetcher ([Investor.gov](https://www.investor.gov/introduction-investing/investing-basics/glossary/donor-advised-funds)).
  - We found no FINRA or SEC rule specific to DAFs, consistent with repo Q-B09.
- **Explainers:** NerdWallet, SoFi and Inside Philanthropy say that contributions are irrevocable, fees vary, and there is "no mandatory distribution" ([NerdWallet](https://www.nerdwallet.com/taxes/learn/donor-advised-funds); [SoFi](https://www.sofi.com/learn/content/donor-advised-funds/); [Inside Philanthropy](https://www.insidephilanthropy.com/explainers/what-is-a-donor-advised-fund)). Investopedia could not be fetched, so we make no claim about its text.

### 5.2 Teaching claims compared with repo findings

| # | Claim as taught | Where taught | Repo evidence (synthesis §A) | Verdict |
|---|---|---|---|---|
| **T1** | "DAFs pay out more than commonly assumed": about **25.2%** of assets a year, against **8.1%** for private foundations | DAFCP program director, [WealthManagement.com, Jul 29 2026](https://www.wealthmanagement.com/philanthropy/five-core-truths-about-donor-advised-funds). Also Philanthropy Roundtable: national sponsors 25.4% and community foundations 17.1% (2022 data) ([Philanthropy Roundtable](https://www.philanthropyroundtable.org/resource/donor-advised-funds-payout-trends-inactivity-policies-and-accessibility/)) | §A2: the aggregate is real but dominated by the largest nationals. The **median sponsor** with ≥$1m pays out about 11–12.5%, and **19–24%** of such sponsors pay out under 5%. Further evidence: DAF-to-DAF transfers count as payout, and removing 2023 national transfers moves the rate from 24.1% to 22.8% ([Chronicle, Mar 6 2026](https://www.philanthropy.com/news/caught-in-a-web-of-daf-transfers/)). The industry method may overstate payout ([NBER w27888](https://nber.org/papers/w27888)). | **Repeats a belief the repo found misleading as stated** (aggregate without denominator). The numbers are right; the inference "DAFs pay out more than foundations" does not hold at the median sponsor or for individual accounts. |
| **T2** | "Major sponsors encourage grantmaking": inactivity rules (Fidelity every 2 years, Vanguard every 3, NPT $250 per 36 months) "keep money moving"; "every sponsor analyzed enforces stringent inactivity policies" | [WealthManagement.com](https://www.wealthmanagement.com/philanthropy/five-core-truths-about-donor-advised-funds); [Philanthropy Roundtable](https://www.philanthropyroundtable.org/the-power-of-donor-advised-funds-trends-and-transformative-impact/) | §A2: a $250 grant every 36 months on a large balance is compatible with near-zero payout. One columnist found a sponsor rule of $500 over three years (via search summary of [Chronicle opinion](https://www.philanthropy.com/opinion/donor-advised-fund-payout-numbers-dont-add-up/)). Fund-level payout is not public. | **Unsupported as an inference.** An inactivity policy is not a payout floor. |
| **T3** | "About 2 million DAFs" or "3.6 million DAF accounts" treated as a donor count | [CCS 2024](https://hub.ccsfundraising.com/hubfs/Images%20and%20Files/Corporate%20Meeting%20Team/Publications/Philanthropic%20Landscape/2024%20Landscape/2024-Philanthropic-Landscape-13th-Edition_CCS-Fundraising.pdf) (citing NPT); trade press summarising "3.6 million DAF accounts" ([Chronicle](https://www.philanthropy.com/article/how-big-are-donor-advised-fund-accounts-new-report-reassesses-data)) | §A1: 79.5% of FY2024 accounts are at processor sponsors holding 0.9% of assets. Traditional invested accounts are at most 737k. | **Contradicted as a donor or TAM count.** |
| **T4** | Transfers between sponsors: most explainers are silent or imply easy moves; Kitces (2015) warns "not all DAFs cooperate with outbound transfers" | [Kitces](https://www.kitces.com/blog/rules-strategies-and-tactics-when-using-donor-advised-funds-for-charitable-giving/); the DAFCP module list shows succession but no portability item ([DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp)) | §A8: none of 12 sponsors publishes an outbound policy; transfers are liquidated, take 10 days to 4 weeks, and carry no grant history. | Kitces is **consistent** with the repo. Mainstream curricula have a **gap**: portability is not a visible teaching item. |
| **T5** | Sponsor control: "the sponsoring organization ... has the final say"; in practice established DAFs follow donor advice | [FINRA](https://www.finra.org/investors/insights/charitable-giving); [Kitces](https://www.kitces.com/blog/rules-strategies-and-tactics-when-using-donor-advised-funds-for-charitable-giving/) | §A6: in 2026 three national sponsors restricted grants to a charity after an indictment ([California AG](https://oag.ca.gov/node/623769)). Control is exercised, not merely formal. | Legally **correct**. Teaching that frames control as a formality is **outdated**; 2026 practice shows it has teeth. |
| **T6** | 2026 tax changes: DAF gifts excluded from the $1,000/$2,000 nonitemizer deduction; 0.5%-of-AGI floor; 35% cap | Taught correctly by the IRS, Fidelity Learning Center, CPA Practice Advisor, InvestmentNews and DAFCP Module 2 ([IRS](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize); [Fidelity](https://fidelity.com/learning-center/personal-finance/charitable-giving-tax-changes); [InvestmentNews](https://www.investmentnews.com/practice-management/charitable-giving-season/268629); [DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp)) | Matches the repo (regulation note, Q-B09). The risk is stale evergreen content: Kitces' 2015 explainer still states the pre-2018 50%/30% AGI limits ([Kitces](https://www.kitces.com/blog/rules-strategies-and-tactics-when-using-donor-advised-funds-for-charitable-giving/)). Donor confusion is visible in a TurboTax community thread asking whether a DAF qualifies ([Intuit community](https://ttlc.intuit.com/community/deductions-credits-9/2026-charitable-deductions-for-non-itemizers-can-i-donate-using-a-daf-807822)). | **Consistent** in current curricula. No misstatement found in 2026 teaching material. |
| **T7** | "Fees are about 0.6%" | Morningstar (2023 data); sponsor pages | Repo `sponsor-fee-schedules.csv`. Minimum fees and adviser-managed layers raise effective cost; DAFgiving360 allows adviser fees up to 1% on professionally managed accounts ([batch-1a note](../batch-1a-relationship-retention-fee-waterfall-2026-11-12.md)). Small community-foundation funds can face much higher effective rates ([Chronicle 2009](https://www.philanthropy.com/news/fees-vary-greatly-at-organizations-that-operate-donor-advised-funds/)). | **Simplified.** Headline admin rate, not all-in cost. |
| **T8** | "Financial advisors have driven DAF growth" | [WealthManagement.com](https://www.wealthmanagement.com/philanthropy/five-core-truths-about-donor-advised-funds); DAFgiving360: 77% of assets adviser-associated ([DAFgiving360](https://dafgiving360.org/giving-report)) | DAFRC 2026: 61% of clients initiate philanthropy talks and 6% say the adviser does ([InvestmentNews](https://www.investmentnews.com/practice-management/charitable-giving-season/268629)). Fidelity: advisers discuss giving with under 60% of clients. | **Mixed.** Advisers are associated with assets, but the evidence that they cause adoption is weak. Association is not initiation. |
| **T9** | Tax benefit is the main reason to use a DAF (advisers: 83% cite tax) | DAFRC 2026 adviser reasons | Clients: tax is a motive for 21% (TPI) and 12% (Goldman Sachs). Advisers rank tax 40% versus clients 21% ([InvestmentNews](https://www.investmentnews.com/practice-management/philanthropy-talk-is-now-standard-in-wealth-advising-but-advisors-are-still-misreading-client-motivations/266429); [InvestmentNews GS](https://www.investmentnews.com/practice-management/ultra-wealthy-donors-step-up-as-government-funding-retreats/268977)) | **Adviser-client perception gap**, documented by sponsor-funded research itself. |
| **T10** | Giving USA totals presented as money reaching charities | Widely repeated; commentators flag DAF intermediation ([NLCTB](https://nlctb.org/beyond-giving-usa-2026-headlines/); [PG Calc](https://pgcalc.com/insight-training/pg-calc-featured-articles/has-the-great-wealth-transfer-finally-begun)) | DAF contributions are counted as gifts at entry. Adding DAF grants to Giving USA totals double counts. | **Simplification** to flag in any industry report. |
| **T11** | "DAFs have no payout requirement" | NerdWallet, SoFi, Kitces | Correct under federal law. The 2023 proposed regulations are not final (§A9). | **Consistent.** |

**Pattern:** the errors are not in the legal mechanics, which curricula teach well. They are in **quantitative framing**: payout, account counts, fees, and who drives adoption. These are the same denominator substitutions synthesis §A identifies. Curricula and their sponsor-funded data sources share an incentive to frame DAFs favourably ([industry-incentives-structural-analysis.md](industry-incentives-structural-analysis.md)). The DAFCP has no named sponsor partner on its page ([DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp)), but its director's public article reuses the aggregate payout claim.

---

## 6. Frameworks and metrics the repo could adopt

1. **Adviser adoption funnel with explicit denominators.** This turns repo backlog Q11 into a measurable chain:
   - firms offering charitable planning: 86% of RIAs ≥$250m ([Schwab](https://advisorservices.schwab.com/insights-hub/perspectives/ria-benchmarking-study-2025));
   - advisers who discuss it moderately or substantially: 75% ([DAFRC via DAFgiving360](https://www.dafgiving360.org/press-release/dafrc-advisor-study));
   - clients actually covered: under 60% ([Fidelity Charitable](https://www.fidelitycharitable.org/insights/differentiating-with-charitable-planning.html));
   - advisers recommending DAFs most of the time or always: 35%;
   - client-initiated conversations: 61% versus 6%;
   - accounts opened and funded: **no public data**, which is the gap.
   - Each stage uses a different population (firms, advisers, clients) and should not be multiplied together.
2. **Population versus advised-client penetration.** Track two penetration series separately: affluent-household DAF ownership (BofA/Lilly: 5% → 7%, 2017–2020) and advised-HNW use (TPI: 51%). Require any TAM to state which it uses.
3. **Perception-gap metric (adviser view minus client view).** TPI reports paired adviser and client rankings of motives and barriers, for example tax 40% vs 21% and "not enough money" 32% vs 9% ([InvestmentNews](https://www.investmentnews.com/practice-management/philanthropy-talk-is-now-standard-in-wealth-advising-but-advisors-are-still-misreading-client-motivations/266429)). Product teams can use it to test whether adviser tooling addresses what clients actually value.
4. **Payout triad.** Report three payout measures together:
   - aggregate payout;
   - median sponsor payout (repo `derived-metrics.csv`);
   - payout excluding DAF-to-DAF transfers ([Chronicle](https://www.philanthropy.com/news/caught-in-a-web-of-daf-transfers/)).

   Add the *flow rate* (grants over contributions), as Philanthropy Roundtable distinguishes ([Philanthropy Roundtable](https://www.philanthropyroundtable.org/the-power-of-donor-advised-funds-trends-and-transformative-impact/)).
5. **Hype Cycle phase labels for AI claims.** Tag each vendor AI capability in [`ai-use-case-inventory.csv`](../../data/mission-2026-11-14/ai-use-case-inventory.csv) with a Gartner-style phase (Trigger, Peak, Trough, Slope, Plateau). Gartner put AI agents at the Peak in 2025 ([BigDATAwire](https://www.hpcwire.com/bigdatawire/2025/09/12/ai-agents-debut-atop-gartner-hype-cycle-for-emerging-tech/)). Virtuous's "efficiency plateau" finding (7% major impact) is a nonprofit-sector reference point ([NonProfit PRO](https://www.nonprofitpro.com/article/nonprofit-ai-adoption-hits-92-but-only-7-see-major-impact/)).
6. **Recordkeeper and portal evaluation criteria.** Since no analyst publishes criteria, combine three sources:
   - (a) Peer Insights complaint themes: total cost for small organisations, UI age, data export, cross-module fragmentation ([Gartner Blackbaud](https://www.gartner.com/reviews/market/non-profit-accounting-software/vendor/blackbaud); [RFP.wiki](https://www.rfp.wiki/vendors/bonterra/blackbaud));
   - (b) the repo's own portability tests (`sponsor-transfer-portability-terms.csv`): grant-history export and in-kind transfer;
   - (c) DAFCP Module 6, "DAF technology tools", as the curriculum's own taxonomy ([DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp)).
7. **DAFCP's six modules as a coverage checklist.** Map repo coverage onto the six modules (fundamentals, tax, gift acceptance, investing and grants, estate and succession, ethics, compliance and technology). Succession is the module the repo covers least.

---

## 7. Gaps and what they imply for an industry report

- **No independent vendor landscape.** The report can present its Schedule-D-based bounds on vendor footprint as the first independent assessment. It must label them as such and not imply analyst corroboration.
- **No public conversion data from adviser conversation to funded account.** Every adviser study measures attitudes and recommendations, not openings or funding. This is the largest gap for any adviser-channel strategy (P-ANL-01).
- **Sponsor-funded evidence base.** The 2026 adviser research is largely sponsor-funded or sponsor-hosted: the DAFRC adviser study is hosted by DAFgiving360, TPI is co-sponsored by DAFgiving360 and Foundation Source, and the Fidelity Charitable and Goldman Sachs studies are their own. Findings unfavourable to sponsors, such as the 6% adviser-initiation figure and the tax-motive gap, are more credible because they appear despite that funding. Favourable framings deserve discounting.
- **Curricula lag the evidence on portability, sponsor discretion and payout distribution.** These three areas are where the repo has original evidence. They are candidates for practitioner-facing outputs (P-ANL-08).
- **Older evergreen content persists.** The 2015 Kitces explainer (pre-2018 AGI limits), the 2009 Chronicle fee survey, and Morningstar expense tables as of 2023 still rank in search. Any report citing educators should check the date of each source.

---

## 8. Source register

The full register is in [`analyst-education-sources.csv`](../../data/mission-2026-11-14/analyst-education-sources.csv). These are the principal sources. IDs match the CSV; the CSV holds 44 rows, so the IDs here are not consecutive.

| ID | Source | Type | Date | Access | URL |
|---|---|---|---|---|---|
| ANL-01 | DAFRC, *Financial Planning in the Age of DAFs* (via press) | academic (sponsor-hosted) | 2026 | secondary | https://www.dafgiving360.org/press-release/dafrc-advisor-study |
| ANL-02 | WealthManagement.com, "Five core truths about DAFs" (Caspersen) | curriculum / media | 2026-07-29 | free | https://www.wealthmanagement.com/philanthropy/five-core-truths-about-donor-advised-funds |
| ANL-03 | The American College, DAFCP program page | curriculum | 2026 | free | https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp |
| ANL-04 | TPI 2026 Study of the Philanthropic Conversation (release) | sponsor-research | 2026-04-16 | free | https://tpi.org/?p=3256 |
| ANL-05 | InvestmentNews on TPI 2026 | media | 2026-05-04 | free | https://www.investmentnews.com/practice-management/philanthropy-talk-is-now-standard-in-wealth-advising-but-advisors-are-still-misreading-client-motivations/266429 |
| ANL-06 | InvestmentNews on DAFRC adviser study and OBBBA | media | 2026-10-28 | free | https://www.investmentnews.com/practice-management/charitable-giving-season/268629 |
| ANL-07 | Fidelity Charitable, *Differentiating with charitable planning* | sponsor-research | 2024 | free | https://www.fidelitycharitable.org/insights/differentiating-with-charitable-planning.html |
| ANL-08 | 2025 BofA Study of Philanthropy (coverage) | academic / sponsor-research | 2025-09-30 | free | https://www.investmentnews.com/practice-management/affluent-americans-are-leading-the-way-in-philanthropy-finds-bofa-study/262336 |
| ANL-10 | Goldman Sachs *Philanthropy in Focus* (coverage) | sponsor-research | 2026-11-11 | free | https://www.investmentnews.com/practice-management/ultra-wealthy-donors-step-up-as-government-funding-retreats/268977 |
| ANL-11 | Celent, *World of Philanthropy* | analyst | 2003-03-07 | abstract-only | https://www.celent.com/en/insights/312707366 |
| ANL-12 | Datos Insights, *Expanding Delivery of Philanthropic Advisory* | analyst | 2021-09 | abstract-only | https://datos-insights.com/?p=13920 |
| ANL-13 | Gartner Peer Insights, Blackbaud non-profit accounting | analyst | 2026 | free | https://www.gartner.com/reviews/market/non-profit-accounting-software/vendor/blackbaud |
| ANL-15 | Gartner, *AI Agents: Use-Case Examples for Investment Services* | analyst | 2025-10-16 | abstract-only | https://www.gartner.com/en/documents/7078098 |
| ANL-17 | Forrester Now Tech: Digital Wealth Management Platforms Q4 2021 | analyst | 2021 | abstract-only | https://www.forrester.com/report/now-tech-digital-wealth-management-platforms-q4-2021/RES176506 |
| ANL-18 | Cerulli HNW/UHNW 2024 (wealth-transfer projection, via NAPA) | analyst | 2024-12 | secondary | https://www.napa-net.org/news/2024/12/wealth-transfers-expected-to-hit-%24124-trillion-through-2048/ |
| ANL-19 | Morningstar, Vanguard Charitable review | analyst | 2023 data | free | https://www.morningstar.com/personal-finance/our-take-vanguards-charitable-endowment-program |
| ANL-20 | Kitces, Rules/strategies/tactics for DAFs | curriculum / media | 2015-06-17 | free | https://www.kitces.com/blog/rules-strategies-and-tactics-when-using-donor-advised-funds-for-charitable-giving/ |
| ANL-23 | FINRA, Investing with Charitable Giving in Mind | curriculum (regulator) | 2024-09-04 | free | https://www.finra.org/investors/insights/charitable-giving |
| ANL-24 | CCS Philanthropic Landscape 2024 | consultancy | 2024 | free | https://hub.ccsfundraising.com/hubfs/Images%20and%20Files/Corporate%20Meeting%20Team/Publications/Philanthropic%20Landscape/2024%20Landscape/2024-Philanthropic-Landscape-13th-Edition_CCS-Fundraising.pdf |
| ANL-25 | Chronicle, "Caught in a web of DAF transfers" | media | 2026-03-06 | free (partial) | https://www.philanthropy.com/news/caught-in-a-web-of-daf-transfers/ |
| ANL-26 | Philanthropy Roundtable, DAF payout trends and inactivity policies | academic / advocacy | 2024 (2022 data) | free | https://www.philanthropyroundtable.org/resource/donor-advised-funds-payout-trends-inactivity-policies-and-accessibility/ |
| ANL-27 | NBER w27888, Calculating DAF payout | academic | 2020 | free | https://nber.org/papers/w27888 |
| ANL-28 | Schwab RIA Benchmarking 2025 | sponsor-research | 2025 | secondary (403) | https://advisorservices.schwab.com/insights-hub/perspectives/ria-benchmarking-study-2025 |
| ANL-31 | Salesforce Nonprofit Trends Report, 7th ed. | sponsor-research (vendor) | 2025-05 | free | https://www.salesforce.com/en-us/wp-content/uploads/sites/4/2025/05/s-org-7th-edition-nonprofit-trends-report-2025.pdf?d=pb |
| ANL-36 | DAFRC Annual DAF Report 2025 (ScholarWorks record) | academic | 2025 | free | https://scholarworks.gvsu.edu/jcppubs/116 |
| ANL-37 | DAFRC National Survey of DAF Donors | academic | 2025 | free | https://scholarworks.gvsu.edu/jcppubs/104 |
| ANL-30 | Stax DAF adviser survey (NY) | consultancy | 2023-06-28 | free | https://www.stax.com/insights/donor-advised-fund-survey |
| ANL-42 | Giving USA 2026 (product page; coverage) | academic | 2026-06 | paywalled | https://givingusa.org/product/2026-annual-report/ |

---

## 9. Data dictionary

### 9.1 `data/mission-2026-11-14/analyst-education-sources.csv`

| Column | Type | Definition |
|---|---|---|
| `source_id` | string | `ANL-NN`, matching §8. |
| `source` | string | Publisher or organisation. |
| `type` | enum | `analyst` (technology or financial-industry research firm), `consultancy`, `academic` (university or academic collaborative, including DAFRC), `curriculum` (designation, course, CE or regulator investor education), `sponsor-research` (research commissioned, funded or co-sponsored by a DAF sponsor or vendor), `media` (trade press or secondary coverage). |
| `title` | string | Title of the report, page or course. |
| `date` | string | Publication date (ISO where known; year or year-month otherwise). |
| `access` | enum | `free`, `abstract-only`, `paywalled` or `secondary` (the primary returned 403 and press coverage was used). |
| `key_claims` | string | The source's claims relevant to DAFs, quoted or closely paraphrased. Numbers as reported. |
| `relevance` | string | How the item bears on repo conclusions, with §A or teaching-claim (T#) cross-references. |
| `url` | string | Primary URL consulted. |

### 9.2 `data/mission-2026-11-14/queue-proposals-analyst-education.csv`

Columns and scales follow [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md) and `research-priority-inputs.csv`:
- `importance`, `gap`, `commercial`, `availability` and `effort` are 1–5.
- `p_change` is 0–1.
- `state` is `open`.
- `proposed_by` is `analyst-education agent`.
- `evidence_pointer` cites this note's section or a source ID.

---

## 10. Confidence and limits

- **Absence findings** (no analyst DAF landscape; no IDC, Javelin or Bain title): Medium. They rest on public search and site abstracts. Client-only research portals may hold titles that public search does not index.
- **Adviser and HNW figures:** Medium. Most come via press coverage of sponsor-funded studies; primary PDFs returned 403 or sit behind forms. Exact wording should be re-checked against the primary reports before publication (P-ANL-02).
- **Teaching-claim comparison:** Medium-High for the claims quoted verbatim (T1, T2, T3, T5). Medium for the absence findings (T4).

## Validation corrections (wave 4, 2026-11-14) — governing
Source: [validation-wave4-report.md](validation-wave4-report.md). Where these conflict with the text above, these govern.

- **W4-12** (research/mission-2026-11-14/analyst-and-education-landscape.md line 107 and lines 111, 187): replace "Advised HNW clients using a DAF … Advised and sponsor-linked sample" / "advised-client penetration (51% of TPI's HNW clients)" → "Philanthropically active HNW individuals ($5m+) using a DAF: 51% (TPI 2026, n=103; not screened for having an adviser)"
