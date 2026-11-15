# Market signals: DAF news coverage 2021–2026 and AI hiring at sponsors and vendors (P-NEW-SIG-01)

**Date:** 2026-11-15. **Queue item:** P-NEW-SIG-01 (owner direction, 2026-11-15). **Script:** `scripts/mission_signals.py` (stdlib only; tasks `discover`, `news`, `hiring`). **Data:** [`daf-news-volume-2021-2026.csv`](../../data/mission-2026-11-14/daf-news-volume-2021-2026.csv), [`daf-hiring-signals-2026.csv`](../../data/mission-2026-11-14/daf-hiring-signals-2026.csv). **Proposals:** [`queue-proposals-batch39-n5.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n5.csv).

**Read with:** report §7 ([DAF-INDUSTRY-REPORT-2026-11.md](../DAF-INDUSTRY-REPORT-2026-11.md)), which says there is no public evidence of AI in sponsor-side approval or eligibility determination, and that the agentic frontier is on the donor side (TIFIN Louise, the Daffy MCP server). Also read [ai-governance-failure-modes.md](ai-governance-failure-modes.md): AI may add a flag but never clear one, and its counts are rubric ratings, not observed incidents (red-team correction 17). Nothing below changes those findings. Job postings show what employers say they want to hire. They do not show what is deployed.

Notation: **[F]** fact from a fetched source; **[I]** inference; **[L]** limitation.

---

## 1. Summary

**News (GDELT DOC 2.0, English, 2021-01-01 to 2026-11-14).** GDELT counts 9,486 articles matching "donor(-)advised fund(s)".
- **[F] Raw volume fell** from 2,972 (2021) and 2,518 (2022) to 849 in 2026 (to Nov 14). Most of the fall reflects GDELT monitoring fewer articles.
- **[F] Normalised volume** (per million articles GDELT monitored) went from 22–27 (2021–22) to a trough of 12.1 in 2025H1, then recovered to 20.0 (2025H2), 21.1 (2026H1) and 24.1 (Jul–Nov 2026).
  - Jan–Oct 2026 runs at 22.1 per million against 14.0 in Jan–Oct 2025, back to about 2021–22 levels.
- **[F] Themes.** Shares are of DAF articles; full-text keyword matches overlap.
  - **Legislation and tax policy** dominates every year: 40.2% in 2021, a trough of 23.8% in 2024, then 38.2% in 2025 and 36.3% in 2026.
  - **Payout/reform** peaked in 2021 at 20.3% (July 2021 is the single largest month for the theme) and has run at 6–8% since 2023.
  - **Giving records** fell from 15.3% to 7–9%.
  - **Crypto** peaked in 2021–22 at 6–8% and was 3.1% in 2026.
  - **AI** rose from 1.2% (2021–22) to 5.7% (2024) and 5.8% (2026), but is never more than 19 articles a month.
  - **Controversial grantees** (SPLC, hate groups, dark money) is small but at its highest share in 2026: 4.9%, against 2.3% in 2021.
- **[I]** Coverage has shifted from the 2021 payout-reform debate (ACE Act) to tax-law and IRS framing in 2025–26. AI is an emerging but minor news frame, and the 2026 rebound is policy-led.

**Hiring (snapshot fetched 2026-11-15).** There are 168 distinct open roles at 12 employers: 17 at sponsors and 151 at vendors.
- **[F]** Of the 166 roles with readable text, **27.7%** mention AI, machine learning or LLMs (46). **26.5%** mention automation, **53.6%** mention "data", and **68.7%** mention at least one of the five terms.
- **[F]** AI is concentrated at vendors: **29.1%** of vendor roles mention it (44/151), against **13.3%** at sponsors (2/15).
  - Fidelity Charitable has 11 open roles whose description names Fidelity Charitable. **None** of them mentions AI, ML or LLMs.
  - Across all 787 Fidelity job pages, the share is 10.2%.
  - Vanguard Charitable's two AI mentions are both "use AI tools" roles: answer-engine web content, and platform reliability and automation.
- **[F]** Only 9 role titles name AI. All are at vendors: Chariot (Applied AI Engineer; Software Engineer, Agentic Infrastructure), Benevity (Senior AI Systems Engineer), Blackbaud (4, including "AI Governance Principal") and TIFIN (2).
- **[F]** Blackbaud also lists two "Agents for Good" engineering roles. Chariot's Compliance Operations role asks the hire to "use AI and documentation to speed up compliance customer support".
- **[I]** The AI work being hired for is **vendor-side product building** (agents, LLM features, AI governance) plus **general "use AI tools" expectations** in non-technical roles. No sponsor posting names AI for grant review, eligibility or due diligence. This is consistent with report §7. It adds one forward signal: at least one DAF rail (Chariot) is staffing agentic infrastructure and AI-assisted compliance operations.

---

## 2. News coverage 2021–2026 (GDELT DOC 2.0)

### 2.1 Method

- **Source [F]:** GDELT DOC 2.0 API, `http://api.gdeltproject.org/api/v2/doc/doc`. robots.txt returned 404 on that host, so no rules apply. GDELT's terms ask for at most one request every 5 seconds. The script waits at least 12 s between requests and backs off on HTTP 429.
  - The https endpoint reset connections from this session, so http was used.
  - GDELT's 429 responses were frequent from this session's shared egress, so the run needed long backoffs (see §2.4).
- **Base query:** `("donor-advised fund" OR "donor-advised funds" OR "donor advised fund" OR "donor advised funds") sourcelang:english`, run in `mode=timelinevolraw` over 2021-01-01 to 2026-11-14.
  - The API returns raw matching-article counts and the total number of articles GDELT monitored in each bucket (`norm`).
  - Counts are summed to calendar months.
- **Themes:** the base query AND one keyword group per theme. GDELT matches anywhere in the article text.

| Theme | Keyword group |
|---|---|
| payout_reform | payout, "payout rate", reform, "ACE Act", "Accelerating Charitable Efforts", warehousing |
| controversial_grantees | SPLC, "Southern Poverty", "hate group(s)", extremist(s), "dark money" |
| crypto | crypto, cryptocurrency, bitcoin, ethereum, NFT |
| ai | "artificial intelligence", "generative AI", ChatGPT, chatbot, "machine learning", "AI agent" |
| giving_records | record, "record-breaking", "giving report", "all-time high" |
| legislation | Congress, Senate, IRS, Treasury, legislation, "proposed regulations", "tax bill", "One Big Beautiful Bill" |

- **Headline sample:** 250 articles per calendar year for the base query (`mode=artlist`, `sort=hybridrel`). Titles are classified with title-level regex mirrors of the themes, plus a headline-only `explainer_howto` genre (e.g., "right for you", "how to", "tips", "year-end").
  - Per-theme article lists were dropped to save requests under GDELT throttling.
  - The 2026 list request failed after retries, so 2026 has no headline sample. That gap is recorded in the run output and not filled.

### 2.2 Results

**Annual totals [F]** (from `daf-news-volume-2021-2026.csv`; theme shares are of DAF articles in the year and overlap):

| Year | DAF articles | Per million monitored | Payout/reform | Controversial grantees | Crypto | AI | Giving records | Legislation |
|---|---|---|---|---|---|---|---|---|
| 2021 | 2,972 | 24.7 | 602 (20.3%) | 67 (2.3%) | 179 (6.0%) | 36 (1.2%) | 456 (15.3%) | 1,195 (40.2%) |
| 2022 | 2,518 | 24.4 | 234 (9.3%) | 87 (3.5%) | 208 (8.3%) | 31 (1.2%) | 357 (14.2%) | 812 (32.2%) |
| 2023 | 1,230 | 18.1 | 80 (6.5%) | 40 (3.3%) | 71 (5.8%) | 21 (1.7%) | 164 (13.3%) | 323 (26.3%) |
| 2024 | 999 | 16.7 | 81 (8.1%) | 41 (4.1%) | 24 (2.4%) | 57 (5.7%) | 111 (11.1%) | 238 (23.8%) |
| 2025 | 918 | 16.4 | 56 (6.1%) | 35 (3.8%) | 44 (4.8%) | 31 (3.4%) | 67 (7.3%) | 351 (38.2%) |
| 2026 (to 11-14) | 849 | 22.1 | 53 (6.2%) | 42 (4.9%) | 26 (3.1%) | 49 (5.8%) | 80 (9.4%) | 308 (36.3%) |
| **Total** | **9,486** | — | 1,106 (11.7%) | 312 (3.3%) | 552 (5.8%) | 225 (2.4%) | 1,235 (13.0%) | 3,227 (34.0%) |

**Half-year normalised volume [F]** (articles per million monitored):

| Period | Per million monitored |
|---|---|
| 2021 H1 / H2 | 22.3 / 27.4 |
| 2022 H1 / H2 | 21.8 / 27.4 |
| 2023 H1 / H2 | 15.0 / 22.1 |
| 2024 H1 / H2 | 16.5 / 17.0 |
| 2025 H1 / H2 | 12.1 / 20.0 |
| 2026 H1 / Jul–Nov 14 | 21.1 / 24.1 |

**Peaks and seasonality [F]:**
- **Largest raw months:** 2021-10 (374), 2021-04 (366), 2022-02 (349) and 2022-12 (334).
- **Largest normalised months:** 2022-12 (43.6), 2023-11 (42.6), 2022-02 (39.7), 2023-12 (39.0), 2021-10 (37.6) and 2026-06 (36.2).
- **Year-end giving season:** November–December carried 18–21% of annual DAF articles in 2021–22 and 30–32% in 2023–25. Coverage has become more seasonal.
- **Theme peaks:**

| Theme | Peak months (articles) |
|---|---|
| Payout/reform | 2021-07 (158), 2021-08 (93), 2021-10 (84) |
| Legislation | 2021-10 (249), 2021-07 (192); 2025-12 (85) and 2026-07 (66) are the post-2022 highs |
| Crypto | 2021-11 (60), 2022-07 (51) |
| AI | 2022-02 (19), 2026-01 (17), 2024-06 (16) |
| Controversial grantees | 2022-01 (27), 2026-05 (17) |

**Interpretation [I]:**
- **2021.** The payout and legislation peaks of July–October 2021 coincide with the Accelerating Charitable Efforts (ACE) Act, introduced in the Senate in June 2021 ([S.1981, 117th Congress](https://www.congress.gov/bill/117th-congress/senate-bill/1981)), and with that year's tax-bill negotiations. Individual peaks are not attributed to single stories here, because GDELT's article lists were throttled (§2.4).
- **2025–26.** The legislation share rebounded in 2025–26, alongside the 2025 tax law and the proposed regulations still pending (report §6). Payout reform as a named frame did not return.
- **AI.** AI coverage is real but small. A share of the matches will be incidental, for example "artificial intelligence" in a general philanthropy-trends article.
- **Controversial grantees.** The theme's higher 2026 share is a weak signal on very small numbers (42 articles).

### 2.3 Sample headlines

The headline sample covers 2021–2025, 250 titles per year. GDELT's relevance sort returned articles almost entirely from **October–December** of each year (249–250 of 250), so the sample shows the year-end giving season, not the whole year.

- **[F] Genre.** Most sampled titles match none of the six themes: 207/250 (2021), 113 (2022), 174 (2023), 176 (2024) and 176 (2025). The largest identifiable genre is the personal-finance **explainer or how-to**: 35, 99, 61, 69 and 68 titles. Syndicated advisor columns such as "Is a donor-advised fund right for you?" appear in many local outlets.
- **[F] Theme examples** (picked by hand from the sample; title, outlet, date as seen by GDELT):

| Theme | Examples |
|---|---|
| Payout/reform | "[Measure on Donor-Advised Funds Misses Opportunity to Produce Genuine Societal Benefits](https://www.philanthropy.com/article/measure-on-donor-advised-funds-misses-opportunity-to-produce-genuine-societal-benefits)" (philanthropy.com, 2021-10-28); "[Fight Erupts Over Whether Donor-Advised Fund Bill Would Help or Hurt Community Foundations](https://www.philanthropy.com/article/fight-erupts-over-whether-donor-advised-fund-bill-would-help-or-hurt-community-foundations)" (philanthropy.com, 2021-11-18); "[An Unlikely Event: the Israel-Hamas War Could Finally Spark DAF Reform](https://www.philanthropy.com/article/an-unlikely-event-the-israel-hamas-war-could-finally-spark-daf-reform)" (philanthropy.com, 2023-12-06) |
| Legislation / IRS | "[Proposed IRS Regulations of Donor-Advised Funds Fall Short, Critics Say](https://www.philanthropy.com/article/proposed-irs-regulations-of-donor-advised-funds-fall-short-critics-say)" (philanthropy.com, 2023-11-15); "[New IRS Proposed Regs Target Donor-Advised Funds](https://www.wealthmanagement.com/philanthropy/new-irs-proposed-regs-target-donor-advised-funds)" (wealthmanagement.com, 2023-11-29); "[Should you donate to charity this year or wait? It depends](https://www.seattletimes.com/business/should-you-donate-to-charity-this-year-or-wait-it-depends/)" (seattletimes.com, 2025-12-21; 2025 tax-law timing) |
| Controversial grantees | "[Hate Groups Are Getting Millions Through Raleigh-Based Fidelity Nonprofit Charity Fund](https://indyweek.com/news/wake/hate-groups-are-getting-millions-through-raleigh-based-fidelity-nonprofit-fund/)" (indyweek.com, 2021-11-24); "[SPLC Tries to Blacklist Turning Point USA, Project Veritas](https://www.dailysignal.com/2023/10/22/splc-tries-blacklist-turning-point-usa-project-veritas-donor-advised-funds/)" (dailysignal.com, 2023-10-22) |
| Crypto | "[Fidelity: Cryptocurrency traders are more charitable](https://www.fastcompany.com/90691172/fidelity-crypto-charity-2021-report)" (fastcompany.com, 2021-10-28); "Fidelity Charitable launches NFT raffle amid crypto downturn" (AP, syndicated, e.g. [taiwannews.com.tw](https://www.taiwannews.com.tw/en/news/4734393), 2022-11-28); "[As crypto fortunes swell, Robinhood announces tie-up with charity platform Daffy](https://fortune.com/crypto/2024/11/13/as-crypto-fortunes-swell-robinhood-announces-tie-up-with-charity-platform-daffy/)" (fortune.com, 2024-11-13) |
| Giving records | "[DAFs Report Record Contributions, Grants](https://www.thenonprofittimes.com/news/dafs-report-record-contributions-grants/)" (thenonprofittimes.com, 2021-11-09); "[Controversial Philanthropy Accounts Known As DAFs Had Record Inflows And Outflows Last Year, New Report Finds](https://www.forbes.com/sites/phoebeliu/2023/11/14/controversial-philanthropy-accounts-known-as-dafs-had-record-inflows-and-outflows-last-year-new-report-finds/)" (forbes.com, 2023-11-14) |
| AI | "[AI Impact on Fundraising in 2026](https://www.philanthropy.com/opinion/ais-impact-on-fundraising-in-2026/)" (philanthropy.com, 2025-11-12). This is the only on-topic AI title in the sample; the other 2025 AI title is a false positive (below). |

- **[F] Noise examples** show why the theme counts are upper bounds:
  - "AI": "[Nvidia CEO Jensen Huang cashes out $1 billion as AI chip demand fuels massive stock rally](https://www.livemint.com/companies/news/nvidia-ceo-jensen-huang-cashes-out-1-billion-as-ai-chip-demand-fuels-massive-stock-rally-11761980012)" (livemint.com, 2025-11-01) presumably mentions a DAF gift in passing.
  - "Records": "[Data Axle Announces 100+ Million New Audience Indicator Records](https://www.pr-inside.com/data-axle-announces-100-million-new-audience-indicator-records-in-r4949956.htm)" (2023-10-17).
  - Non-news pages GDELT indexed: a charity donation form ([donate.hrw.org](https://donate.hrw.org/page/31965/action/1?ea.tracking.id=EA2024FCbd4wb), 2024) and public-radio "make a grant from your DAF" pages ([wlrh.org](https://wlrh.org/donor-advised-fund/), 2025).
  - A 2020 NewsBusters post re-seen in Dec 2025 shows that GDELT's "seen" date is not always the publication date.

The full sample (titles, URLs and title-level themes) is in the run's `news-headlines.json` in the work directory. Raw GDELT responses are cached in `gdelt-cache/`.

### 2.4 Limitations

- **[L] Coverage.** GDELT monitors a large but changing set of online news sources, weighted to outlets it crawls. It under-covers paywalled trade press (Chronicle of Philanthropy, Barron's, WSJ), and it excludes newsletters, podcasts and social media.
  - Raw counts move with GDELT's source universe. The `daf_per_million_monitored` column normalises for that and is the better trend measure.
- **[L] Keyword noise.** Full-text matching counts passing mentions: a personal-finance article that lists a DAF among year-end tax tips counts as DAF coverage.
  - The theme filters are broad. "record" matches "track record", and "IRS" appears in almost any tax article. The theme counts are therefore **upper bounds on topical coverage** and overlap one another; they do not sum to the total.
  - P-B39N5-02 proposes a hand-coded precision check.
- **[L] Headline sample bias.** `sort=hybridrel` returned Q4-dated articles almost exclusively, and 2026 has no sample. Headlines illustrate the themes; they are not a random sample.
- **[L] Syndication.** One AP or wire story republished by dozens of local sites counts dozens of times (e.g., the Nov 2022 "Fidelity Charitable launches NFT raffle" AP story). Spikes can reflect one syndicated story.
- **[L] Bucket size.** Each series was fetched in one call over the whole window. GDELT returned daily buckets (`date_resolution: day`, 2,100 points), which were summed exactly to calendar months.
- **[L] GDELT's own coverage dropped in late 2026.** Monitored English volume was about 4–5 million articles a month through mid-2026, then 2.6m (Sep 2026), 1.4m (Oct 2026) and 0.22m (Nov 1–14). There was a similar dip in Jun 2025 (2.3m). Raw counts for those months are not comparable, and even the normalised rate is noisy on such small bases (Oct 2026: 48 articles).
- **[L] Rate limits.** GDELT throttled this session heavily. Every number comes from a completed API response cached in the work directory; no value was imputed.

---

## 3. Hiring signals (public postings, fetched 2026-11-15)

### 3.1 Method

- **robots.txt first [F].** The script reads robots.txt on every host before any other request to it, using RFC 9309 status handling: 2xx is parsed; 4xx other than 429 means no rules; 429, 5xx or unreachable means disallow. The decision log is in the work directory (`robots-log-hiring.json`).
- **No job boards.** No LinkedIn, Indeed or Glassdoor. No logins, form submissions or POST requests: every request is a GET.
- **User-Agent.** A generic one.
- **Data minimisation.** No personal data was collected. Rows hold the public job title, team or department, location, posting date and keyword flags, plus a ≤200-character context snippet of the first AI-family match for audit.

| Employer | Segment | Source (public, GET) | Roles |
|---|---|---|---|
| Fidelity Charitable | sponsor | [jobs.fidelity.com sitemap](https://jobs.fidelity.com/sitemap.xml) (robots: `Allow: /`). All 787 job pages were read, and a role is kept if its *job-description body* names "Fidelity Charitable". | 11 |
| Vanguard Charitable | sponsor | ADP Workforce Now public career-center JSON (linked from [vanguardcharitable.org/careers](https://www.vanguardcharitable.org/careers)) | 4 |
| Greater Kansas City CF | sponsor (CF) | [Paylocity public job board](https://recruiting.paylocity.com/Recruiting/Jobs/All/caf479db-2051-4124-a5db-d0bbf0a5300d/Greater-Kansas-City-Community-Foundation) (title and teaser only) | 1 |
| New York Community Trust | sponsor (CF) | [thenytrust.org/careers-fellowships](https://thenytrust.org/careers-fellowships/) (title only; President search) | 1 |
| Ren | vendor | [Greenhouse boards-api `renpsg`](https://boards-api.greenhouse.io/v1/boards/renpsg/jobs) (linked from reninc.com/careers) | 6 |
| Chariot | vendor | [Ashby posting API `chariot`](https://api.ashbyhq.com/posting-api/job-board/chariot) (descriptions name Chariot's nonprofit payment infrastructure) | 19 |
| Daffy | vendor | [daffy.org/careers](https://www.daffy.org/careers) and its role pages | 4 |
| Givinga | vendor | [givinga.com/careers](https://www.givinga.com/careers) and its role page | 1 |
| Benevity | vendor | [Ashby posting API `benevity`](https://api.ashbyhq.com/posting-api/job-board/benevity) (23 postings, 14 distinct roles) | 14 |
| Blackbaud | vendor | [careers.blackbaud.com search results](https://careers.blackbaud.com/us/en/search-results) (Phenom; the embedded JSON carries a teaser and skills, not the full description) | 86 |
| Bonterra | vendor | [Workday sitemap](https://bonterra.wd1.myworkdayjobs.com/bonterratech/siteMap.xml) plus the public job-detail JSON (GET) | 18 |
| TIFIN | vendor | [Greenhouse boards-api `tifin`](https://boards-api.greenhouse.io/v1/boards/tifin/jobs) (TIFIN group, not only TIFIN Give) | 3 |

**Not collected [L]** (from the robots log and fetch status):

| Employer | Reason |
|---|---|
| Schwab / DAFgiving360 | robots.txt disallows `/search-jobs/` on schwabjobs.com |
| National Philanthropic Trust | the site links no careers page, and `/careers/` and `/about-us/careers/` return 404. Third-party boards point to a Paycor page that was not located from first-party links. |
| Chicago Community Trust; Foundant | HTTP 403 to the script |
| Silicon Valley CF; Tulsa CF | no openings in the static HTML |
| Endaoment | the careers page is a JS app with no static listing, and no Greenhouse, Lever or Ashby board was found |
| Every.org | robots.txt returned 429, treated as disallow |

**Keyword flags.** All regexes are in the script.
- **Terms:** `ai` matches AI, "artificial intelligence", GenAI, generative or agentic. `ml` matches "machine learning", ML or MLOps. `llm` matches LLM, "large language model", GPT, ChatGPT, "prompt engineering", RAG, OpenAI or Anthropic. `automation` matches automat\*. `data` matches the word data.
- **`desc_*`:** computed on title, team and description.
- **`role_*`:** the same flags after removing employer boilerplate, defined as sentences repeated in at least 40% of an employer's postings (employers with at least 4 postings).
  - Removing boilerplate changed no AI flag. Bonterra's "we're building AI-powered tools" paragraph appears in only a minority of its postings, so it is kept as a role-level signal.
  - On Fidelity pages, the site-wide "AI Guidelines" link would have flagged every role, so the description body is sliced out first.
- **`ai_mention_type`:** a heuristic.
  - `build_ai`: an engineering, data or product role whose text describes building AI, LLM, agent or ML features.
  - `use_ai_tools`: the text asks the hire to use AI tools.
  - `other_mention`: any other AI mention.

### 3.2 Results

| Group | Roles | With text | AI/ML/LLM | Automation | Data | Any of five | AI in title |
|---|---|---|---|---|---|---|---|
| **All** | 168 | 166 | **46 (27.7%)** | 44 (26.5%) | 89 (53.6%) | 114 (68.7%) | 9 |
| Sponsors (FC, VC, GKCCF, NYCT) | 17 | 15 | 2 (13.3%) | 3 (20.0%) | 7 (46.7%) | 8 (53.3%) | 0 |
| — Fidelity Charitable | 11 | 11 | 0 (0%) | 1 | 4 | 5 | 0 |
| — Vanguard Charitable | 4 | 4 | 2 | 2 | 3 | 3 | 0 |
| DAF-core vendors (Ren, Chariot, Daffy, Givinga) | 30 | 30 | 9 (30.0%) | 6 (20.0%) | 11 (36.7%) | 14 (46.7%) | 2 |
| — Chariot | 19 | 19 | 4 | 3 | 5 | 5 | 2 |
| Broad nonprofit/wealth tech (Benevity, Blackbaud, Bonterra, TIFIN) | 121 | 121 | 35 (28.9%) | 35 (28.9%) | 71 (58.7%) | 92 (76.0%) | 7 |
| — Benevity | 14 | 14 | 8 (57.1%) | 5 | 10 | 13 | 1 |
| — Blackbaud (teaser text only) | 86 | 86 | 16 (18.6%) | 26 | 44 | 60 | 4 |
| — Bonterra | 18 | 18 | 8 (44.4%) | 3 | 14 | 16 | 0 |
| — TIFIN | 3 | 3 | 3 | 1 | 3 | 3 | 2 |

The table uses role-level flags; shares are of roles with text. Per-employer counts for Ren (3/6 AI), Daffy (2/4) and Givinga (0/1) are in the CSV.

- **By function [F]:**
  - Technical roles (engineering, data, product and design; n=64 with text): 39.1% mention AI.
  - Non-technical roles (n=102): 20.6% mention AI.
- **By mention type [F]:** of the 46 AI-mentioning roles, 16 are `build_ai`, 19 `use_ai_tools` and 11 `other_mention`.
  - The heuristic misfiles at least one case: Ren's "Senior People Platform & Enablement Manager" ("using AI to remove friction for employees") is tagged `build_ai` because "platform" puts it in engineering.
- **Recency [F]:** 147 of 151 dated postings were posted or updated in Jul–Nov 2026. This is a current snapshot, not a history.

### 3.3 What this implies about AI adoption [I]

1. **Sponsors are not yet hiring for AI.** Fidelity Charitable is the largest sponsor and runs a navigation-only virtual assistant ([terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html)). None of its 11 open roles mentions AI, including two compliance roles and a philanthropy product director. Its parent's job pages do mention AI (10.2% of all 787). This fits report §7's finding of no public AI in sponsor approval or eligibility determination.
2. **Vendors carry AI adoption, and it is product-side.** About three in ten vendor roles mention AI.
   - The explicit AI titles are at Chariot (agentic infrastructure, applied AI), Blackbaud ("Agents for Good", AI governance, knowledge and AI transformation), Benevity (AI systems engineer, building LLM search, assistants and agents) and TIFIN (AI engineering for advisor copilots using RAG and evaluation harnesses).
   - This matches §7's view that agentic capability arrives through vendors and the donor or advisor side before sponsors build it.
3. **Governance demand is starting to show.** Blackbaud's "AI Governance Principal" and Benevity's Security Architect ("AI security risks and securing AI-enabled systems") are the first hiring evidence in the repo of AI-governance roles at DAF-adjacent vendors. They map onto failure modes F09, F10 and F15 in the governance register.
4. **"Data" and "automation" are ubiquitous and weakly informative.** "Data" appears in about half of all roles. "Automation" appears in about a quarter, mostly as workflow or RevOps language. Neither term separates AI adopters from others.
5. **Caveat.** The sample is small, especially at sponsors (17 roles), and Schwab, NPT and most community foundations are missing. A posting expresses intent, not deployment, and an employer can use AI without saying so in job ads. Treat the sponsor–vendor contrast as directional.

---

## 4. Data dictionary

### `data/mission-2026-11-14/daf-news-volume-2021-2026.csv` (one row per calendar month, 2021-01 to 2026-11)

| Column | Meaning |
|---|---|
| month | YYYY-MM |
| articles_daf | GDELT raw count of English-language articles matching the base DAF phrase query |
| articles_monitored_total | GDELT `norm`: total English articles GDELT monitored in the month (summed over buckets) |
| daf_per_million_monitored | articles_daf / articles_monitored_total × 10^6 (the trend measure that normalises for coverage) |
| articles_payout_reform … articles_legislation | Raw count of articles matching the base query AND the theme keyword group (§2.1). Themes overlap, so the counts are not additive. |
| partial_month | `yes` for 2026-11 (data to 2026-11-14) |

### `data/mission-2026-11-14/daf-hiring-signals-2026.csv` (one row per distinct open role)

| Column | Meaning |
|---|---|
| org, segment | Employer; `sponsor`, `sponsor_cf` or `vendor` |
| source | Public endpoint or page the row came from |
| date_fetched | 2026-11-15 |
| title, team, location, posted_or_updated | As published (team is the department or category where the source gives one) |
| function | Heuristic bucket from title and team: data, engineering, product_design, sales_gtm or operations_other |
| description_available, desc_chars | Whether description text was available, and its length |
| title_{ai,ml,llm,automation,data}, title_any_ai_ml_llm | Keyword flags on title and team only |
| desc_{ai,ml,llm,automation,data}, desc_any_ai_ml_llm, desc_any_of_five | Flags on title, team and description (blank if no description) |
| ai_context | ≤200-character snippet around the first AI, ML or LLM match (for audit) |
| role_{ai,ml,llm,automation,data}, role_any_ai_ml_llm | Flags after removing employer boilerplate sentences (§3.1); the headline measure |
| ai_mention_type | build_ai, use_ai_tools or other_mention (heuristic; blank if no AI mention) |

Reproduce with `python3 scripts/mission_signals.py news --work-dir WORK` and `python3 scripts/mission_signals.py hiring --work-dir WORK`. Job postings change daily, so a re-run gives a new snapshot.
