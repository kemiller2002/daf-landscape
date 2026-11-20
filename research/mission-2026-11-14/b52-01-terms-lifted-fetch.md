# B52-01: Re-fetching sources that earlier studies skipped for site-terms reasons

- **Task ID:** b52-01. **Date:** 2026-11-20.
- **Data:** `data/mission-2026-11-14/terms-lifted-fetch-2026-11-20.csv` (58 rows, one per checked item).
- **Queue proposals:** `data/mission-2026-11-14/queue-proposals-b52-01.csv` (6 rows).
- **Evidence labels:** F = fetched from the primary source on 2026-11-20; C = computed from fetched values; R = carried from a repo file; B = blocked.
- **No existing repo file was edited.** Section 4 lists the corrections as proposals for the validator.

## Summary

1. **Charity Navigator: all four flagged quotes match verbatim.** CNAI-01, 02, 03 and 05 match after whitespace and quote-mark normalisation. CNAI-03's only difference is a link tag. The API Terms ("Last updated October 2026") still have **0** AI, LLM, machine-learning or training matches. The screen of all **18** press releases in CN's post sitemap reproduces the earlier result. The wave 48A provenance flag can be replaced (§4, C1).
2. **Vanguard Charitable: every repo figure checked is confirmed** (GC-006, 12 sponsor-published rows, the exception-share inputs). The reports also publish an average grant, which b51-03 listed as blocked:
   - CY2022: **$9,500**
   - CY2023: **$12,412**
   - CY2024: **$12,926**
   - CY2025: **$14,808**, with 267,838 grants
   - FY2023: **$10,972**
   - FY2025: about **$14,000**

   No median or size bands were found.
3. **NPT: repo figures confirmed, but NPT has restated its own counts.** The FY25 annual report restates FY21–FY24 grant counts 0.8–1.2% lower than the FY23 and FY24 reports printed them. GC-002 uses the restated FY24 figure (129,575); A-NPT-FY24 uses the original one (130,875). The FY25 report also publishes the mean grant for FY21–FY25: **$73,866, $53,804, $42,707, $42,387, $40,381**. The DAF Report has no grant-size statistic. NPT stopped producing it in 2025, and DAFRC produces it now.
4. **PR Newswire: GC-016 and GC-021 are confirmed.** GC-021's release is dated 2025-10-20; the repo row does not record a date. JCF's grant-size figures are now read at source:
   - FY2021: median **$501**, mean **$7,194**
   - FY2022: median **$601**
5. **NCF: the donate-page count is still not determinable.** NCF's sitemaps hold 0 donate pages among 659 URLs, all on www, and none of the 15 www pages read links to one. Of 35 quoted spans in 20 repo rows, 32 are verbatim on the cited page and 2 are verbatim on a different NCF page. The last one (PL-S10) is an elided paraphrase whose substance the guide confirms. NCF's www pages give no grant-size statistic.
6. **Every.org is still blocked.** Its robots.txt returns 429 with a "Vercel Security Checkpoint" JS challenge. Two attempts got the same result. The four AI-use cells stay "not determinable".

## 1. Owner decision (2026-11-20)

The shared rules record the owner decision of **2026-11-20**: the site-terms restriction is lifted. Sites whose terms ban automated extraction may now be fetched politely. That covers vanguardcharitable.org, nptrust.org, prnewswire.com, charitynavigator.org, www.ncfgiving.com, fortune.com and similar sites. The conditions are:
- specific named documents and pages only;
- at least 3 seconds between requests;
- a generic user agent;
- no bulk crawling.

These rules still apply in full:
- robots.txt, including the rule that a disallow for ClaudeBot, anthropic-ai, Claude-User, Claude-Web or Claude-SearchBot binds this client;
- a 403 or unreachable robots.txt counts as disallowed;
- CAPTCHAs, Cloudflare or other JS challenges, logins and forms are never bypassed.

This pass works under that decision. The sites' terms texts are unchanged (rows B5201-007 and -074; §3.2 and §3.3), and the reads rely on the owner's decision, not on any change in the terms.

## 2. Method

1. **Fetcher.** A stdlib Python fetcher, written in functional style (a `functools.reduce` over the URL list), with user agent `research-script/1.0`.
   - It sleeps 3.5 s before every request, robots files included.
   - For each new host it reads robots.txt first. A URL is allowed only if `urllib.robotparser` allows it for **every** one of ClaudeBot, anthropic-ai, Claude-User, Claude-Web, Claude-SearchBot and `*`.
   - A robots status of 401, 403, 429, 5xx or a network failure counts as disallowed.
   - A page with status 401, 403, 429 or 503, or HTML with challenge markers, is recorded as blocked and not retried.
   - The fetcher and the raw copies stay in the session scratchpad (`b5201/`). No page copy is committed.
2. **Scope.** Only named URLs were fetched: those cited in the repo rows (found from the full row text), sitemaps the sites publish themselves, and four PR Newswire release URLs found by a web search for the JCF figures. No on-site search, no URL guessing, no crawl.
   - **Requests:** 92 in all, between 17:11 and 17:21 UTC. By host:

     | Host | Requests |
     |---|---:|
     | www.charitynavigator.org | 27 |
     | www.ncfgiving.com | 26 |
     | www.nptrust.org | 16 |
     | www.vanguardcharitable.org | 15 |
     | www.prnewswire.com | 6 |
     | www.every.org | 2 (robots only) |

   - **Robots-disallowed:** 4 URLs were refused by the robots check and not requested.
3. **Text and matching.**
   - HTML was reduced to text: scripts and styles were dropped and tags replaced with spaces.
   - Whitespace was collapsed, and curly quotes and en/em dashes were normalised. A space before punctuation that comes from a closing link tag was removed.
   - PDFs were read with `pdftotext -layout`.
   - Every quote in the output CSV was checked by script against the fetched copy (text or raw HTML for chart attributes). All 51 quotes matched.
4. **Repo quotes for NCF.** For every CSV row in `data/mission-2026-11-14/` that cites a fetched www.ncfgiving.com page, a script took the quote columns and any double-quoted span of 25 or more characters, then looked for each span on the cited page and on the other NCF pages.
5. **Privacy.** No NCF fund or fund-holder name was recorded; only counts.
6. **Computations** (C) are simple ratios and sums shown in the CSV notes, for example $5.49bn / 129,575 = $42,369, and the FY25 field-of-interest volumes summing to 159,543.

## 3. Results

Status codes in the tables:
- **conf** = confirmed;
- **conf+note** = confirmed, with a caveat;
- **corr** = repo text needs a correction;
- **new** = new figure;
- **n/f** = not found;
- **blk** = blocked.

### 3.1 Charity Navigator (www.charitynavigator.org)

| Item | Status | Verbatim / finding | URL | Date |
|---|---|---|---|---|
| CNAI-01 | conf | "The first phase of this collaboration brings together Charity Navigator’s trusted ratings with Giving Compass’s modern search technology …" (full repo quote matched) | https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search/ | 2025-11-24 |
| CNAI-02 | conf | "Giving Compass’s search engine uses a hybrid approach — word matching plus meaning matching — to rank nonprofits based on relevance, clarity, and donor intent." | same | 2025-11-24 |
| CNAI-03 | conf | "Charity Navigator, the nation’s leading nonprofit ratings organization, and Allegory, the first AI-powered operating system for grant funding, announced the integration of Charity Navigator’s ratings API into Allegory’s platform." Both AI mentions describe Allegory itself. | https://www.charitynavigator.org/about-us/press-release/allegory-integrates-cn-api/ | printed 2026-05-18 (page metadata 2026-06-05) |
| CNAI-05 | conf | "Andrew’s deep understanding of leveraging technology and AI for social impact, combined with Matt’s extensive experience in nonprofit leadership and organizational transformation, are precisely the expertise we need." | https://www.charitynavigator.org/about-us/press-release/charity-navigator-expands-board/ | 2025-07-15 |
| API Terms | conf | "Last updated October 2026". 0 matches for AI, artificial intelligence, LLM, language model, machine learning, train*, model, generative, scrap* or data mining. The URL redirects to `/products-and-services/graphql-api/api-terms-of-use/` | https://www.charitynavigator.org/products-and-services/api/ | Oct 2026 |
| Release screen | conf | 18 releases in post-sitemap.xml. AI wording appears in 5: the 3 in-window CN statements, Carefull 2024-05-15 ("Our Financial Safety platform is built around our proprietary financial monitoring AI", which is Carefull's boilerplate) and Anthem 2026-11-05 (Webby boilerplate "Creators and AI") | https://www.charitynavigator.org/post-sitemap.xml | 2022–2026 |
| Site ToU | conf | "data mining, robots, or similar data gathering and extraction methods", "Last updated November 1, 2022" | https://www.charitynavigator.org/about-us/financials-and-policies/terms-of-use/ | 2022-11-01 |
| Wave 48A provenance flag | conf | Every flagged item re-read; all match | — | — |

### 3.2 Vanguard Charitable (www.vanguardcharitable.org)

| Item | Status | Verbatim / finding | URL | Date |
|---|---|---|---|---|
| GC-006 | conf | "Total dollars granted $3.1 billion Unique charities supported 62,586 Average grant size $12,926 Total grants issued 240,064". Footnote: "All calendar year numbers reported as of December 31, 2024, unless otherwise stated." | https://www.vanguardcharitable.org/2024annualreport | CY2024 |
| Exception-share FY2023 inputs | conf | 2022 AR: "Total grant dollars given $1.87B Unique organizations supported 52,800 Average grant size $9,500 Total grant units given 196K". 2023 AR: "… Unique organizations supported 56,744 Average grant size $12,412 Total grant units given 209K". Means 202,500 and 54,772 recomputed [C] | /2022annualreport; /2023annualreport | CY2022, CY2023 |
| Exception-share FY2024 inputs | conf | 240,064 and 62,586 (above). Means 224,532 and 59,665 recomputed [C] | /2024annualreport | CY2024 |
| A-VC-CY2020, A-VC-CY2021 | conf | "In 2021, more than half of all giving was unrestricted, up from 42% of grant dollars in 2020." | /news/vanguard-charitable-donors-build-record-charitable-giving-year-granting-total-over-178-billion | 2022-01-25 |
| A-VC-2022-12 | conf | "Today, more than half of the grants recommended by Vanguard Charitable donors are unrestricted" | /news/vanguard-charitable-celebrates-25-years-and-15-billion-granted | 2022-12-08 |
| A-VC-CY2022 | conf | "over half of dollars granted by Vanguard Charitable donors were unrestricted" | /news/vanguard-charitable-donors-set-new-granting-record-despite-economic-challenges | 2023-01-25 |
| A-VC-2023-04 | conf | "now representing more than half the dollars granted annually" | /news/unrestricted-giving-increased-over-past-5-years | 2023-04-26 |
| A-VC-FY2023 | conf | "More than 50% of all grants recommended by Vanguard Charitable donors in fiscal year 2023 were unrestricted." | /news/vanguard-charitable-FY23-granting-record | 2023-08-10 |
| A-VC-CY2023 | conf | "More than half of the total dollars granted by donors were unrestricted" | /news/vanguard-charitable-donors-granted-2-billion-2023 | 2024-01-30 |
| A-VC-FY2024, A-VC-FY2025 | conf | "more than half of grant dollars (51.7%) were unrestricted, an increase from 48.3% last year" | /news/vanguard-charitable-donors-deepen-their-impact-driving-another-year-record-granting | 2025-08-25 |
| A-VC-CY2025 | conf | "half of all grants issued last year were unrestricted, accounting for $2 billion"; headline "Donor Grants Exceeding $3.9 Billion In 2025" | /news/vanguard-charitable-2025-record-granting | 2026-03-02 |
| B-VC-anon-4, B-VC-anon-5 | conf | "Only 4% of grants are completely anonymous." and "Anonymous granting: Only 5% of grants are completely anonymous". Both are still on the same live page | /nonprofit-organizations | live |
| **New:** average grant CY2022–CY2025 | new | $9,500 / $12,412 / $12,926 / $14,808. CY2025: "Total dollars granted $3.96B Unique charities supported 66,785 Average grant size $14,808 Total grants issued 267,838" | /2022annualreport … /2025annualreport | CY |
| **New:** FY2023 average | new | "Vanguard Charitable donors issued more than 195,000 grants to over 53,000 individual nonprofits, totaling $2.1 billion. The average grant amount was $10,972, a 17% increase over the year prior." | /news/vanguard-charitable-FY23-granting-record | 2023-08-10 |
| **New:** FY2025 average | new | "This record granting included nearly 248,000 grants that averaged approximately $14,000, up 2.5% from fiscal year 2024." | /news/vanguard-charitable-donors-deepen-their-impact-driving-another-year-record-granting | 2025-08-25 |
| **New:** live nonprofit page | new | "Our grant minimum is $500. Our average grant is $10,000." The $10,000 figure is stale against the annual reports | /nonprofit-organizations | live |
| Median or size bands | n/f | None on the 4 annual reports, 8 releases or the nonprofit page | — | — |
| Terms | context | The terms still forbid "systematically extracting data contained in the Site to populate databases for internal or external use" | /company-policies/terms-and-conditions | — |

All page dates in the table match the repo's `source_date` values (from `<time datetime>` on each release).

### 3.3 NPT (www.nptrust.org)

| Item | Status | Verbatim / finding | URL | Date |
|---|---|---|---|---|
| GC-002 | conf+note | Chart attribute `data-data="87490,102745,106235,129575,159543,"` (FY21–FY25) | https://www.nptrust.org/annual-reports/npt-annual-report/ | FY25 report |
| FY24 count as first published | new (conflict) | "NPT issued 130,875 individual grants in FY24." and "NPT grants supported 41,879 unique nonprofit organizations." FY20–FY24 chart: 73883, 88289, 103816, 107385, 130875; dollars 2.32, 6.41, 5.57, 4.50, 5.62 ($bn) | https://www.nptrust.org/annual-reports/the-2024-annual-report/ | FY24 report |
| FY23 count as first published | context | "NPT issued 107,385 individual grants in FY23." and "Grants supported 36,361 unique nonprofit organizations." | https://www.nptrust.org/annual-reports/the-2023-annual-report/ | FY23 report |
| A-NPT-FY15 | conf | "A decade ago, that share was just 13%." | npt-annual-report | FY25 report |
| A-NPT-FY20 | conf | `data-category="FY15,FY20,FY25," data-data="13,63,66,"` | npt-annual-report | FY25 report |
| A-NPT-FY21, B-NPT-FY21 | unverifiable | https://www.nptrust.org/?p=6867 still returns 404 | — | — |
| B-NPT-FY20 | not re-checked | The row gives no fetchable URL | — | — |
| A-NPT-FY23 | conf | "more than half of all grant recommendations were unrestricted" | the-2023-annual-report | FY23 |
| A-NPT-FY24 | conf+note | "47% of grants were unrestricted, providing flexibility and agency to nonprofits." The 130,875 denominator is confirmed on this page, but it differs from GC-002 | the-2024-annual-report | FY24 |
| A-NPT-FY25 | conf | "In FY25, 105,909 grants, or 66% of the total, were unrestricted". The FY25 field-of-interest volumes sum to 159,543 [C] | npt-annual-report | FY25 |
| B-NPT-qual | conf | "The majority of grants from donor-advised funds are not anonymous." (/for-charities/ now redirects to /for-nonprofits/) | https://www.nptrust.org/for-charities/ | live |
| Exception-share NPT FY2023 / FY2024 | conf+note | G 106,235 and 129,575, international grants 335 and 406 (`data-data="274,286,335,406,528,"`), dollars 4.54 and 5.49 (`data-data="6.46,5.53,4.54,5.49,6.44,"`), all from the FY25 report. The FY23 and FY24 reports print 107,385 / $4.52bn and 130,875 / $5.62bn, and publish R = 36,361 and 41,879 | npt-annual-report | FY25 report |
| **New:** mean grant FY21–FY25 | new | Chart "AVERAGE GRANT SIZE • FY21 – FY25 / Mean value per grant recommended": `data-coords-y="73866, 53804, 42707, 42387, 40381"`. Caption: "the typical grant peaked near $74K in FY21 and settled around $40K in FY25 as participation widened." FY24 check: $5.49bn / 129,575 = $42,369 [C] | npt-annual-report | FY25 report |
| DAF Report grant size | n/f | "Starting in 2025, the Donor Advised Fund Research Collaborative (DAFRC) is independently producing the Annual DAF Report." The 2024 DAF Report PDF (20 pp.) gives account-size averages (e.g. $141,120 for 2023) but no average or median grant | https://www.nptrust.org/reports/daf-report/ ; https://www.nptrust.org/wp-content/uploads/2024/11/2024-DAF-Report-NPT.pdf | 2024-11 |
| Median or size bands | n/f | None published | — | — |
| Terms | context | The terms still bar "harvesting data from the Site using robots, spiders, scripts, software or any manual or automatic device, tool or process to populate databases or collect Site Content" | https://www.nptrust.org/privacy-policy/ | — |

**NPT restatement.** The FY25 report's series is lower than the earlier reports for every year:

| Year | FY25 report | Earlier report | Change |
|---|---:|---:|---:|
| FY21 | 87,490 | 88,289 | −0.9% |
| FY22 | 102,745 | 103,816 | −1.0% |
| FY23 | 106,235 | 107,385 | −1.1% |
| FY24 | 129,575 | 130,875 | −1.0% |

Grant dollars were restated too: FY24 is $5.49bn against $5.62bn printed earlier. NPT gives no explanation. Both series are first-party. The repo mixes them (queue P-B5201-01). Validator note: wave 39A had already recorded this restatement (b4013-b4428 §2.2). The count revisions are −0.9% to −1.1%; the dollar revisions run both ways (FY21 $6.41bn → $6.46bn, FY22 $5.57bn → $5.53bn, FY23 $4.50bn → $4.54bn, FY24 $5.62bn → $5.49bn). The repo keeps 129,575 as the governing FY2024 count. The mean-grant chart’s subtitle reads “Mean value per grant recommended ($ in thousands)”, but its values are dollars. [V wave 52A]

### 3.4 PR Newswire (www.prnewswire.com)

| Item | Status | Verbatim | URL | Date |
|---|---|---|---|---|
| GC-016 | conf | "89,485 total grants distributed by Fundholders, a 15% increase over the previous year" | https://www.prnewswire.com/news-releases/jewish-communal-fund-donors-grant-record-breaking-1-billion-in-fiscal-year-2024-302227664.html | 2024-08-22 |
| GC-021 | conf | "The Blackbaud Giving Fund securely disbursed funds from individuals and corporations to more than 123,000 nonprofits worldwide in 2024." | https://www.prnewswire.com/news-releases/the-blackbaud-giving-fund-surpasses-550m-in-charitable-giving-in-2024--reaching-2-75b-in-lifetime-giving-302588766.html | 2025-10-20 (dateline) |
| JCF FY2021 median | new | "JCF Fundholders make an average of 17 grants per fund per year, with a median grant amount of $501." | https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-record-number-of-grants-to-charity-totaling-520-million-in-fy-21-301456454.html | 2022-01-10 |
| JCF FY2021 mean | new | "The average grant amount was $7,194." (72,000 grants, $520m). Mean/median 14.4 [C] | https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-out-520-million-in-grants-in-fy-2021-301409897.html | 2021-10-28 |
| JCF FY2022 median | new | "JCF Fundholders make an average of 18 grants per fund per year, with a median grant amount of $601." Also: "JCF Fundholders recommended a record-breaking 80,500 grants totaling nearly $600 million" | https://www.prnewswire.com/news-releases/jewish-communal-fund-releases-50th-anniversary-giving-report-301740253.html | 2023-02-07 |

### 3.5 NCF (www.ncfgiving.com)

| Item | Status | Finding | URL |
|---|---|---|---|
| Donate pages (P-B4222-02-02) | n/f | The sitemap index lists 8 child sitemaps with 659 URLs, all on www: page 34, post 0, story 453, event 2, document 56, video 22, podcast 18, book 74. None is a fund donate page. The 15 pages read link off-site only to secure.ncfgiving.com (`/`, `/agreement`, `/legacy`; robots-disallowed) and site.ncfgiving.com (images, PDFs). **Count not determinable**; the queue item stays blocked | https://www.ncfgiving.com/sitemap.xml |
| Guide and other cited www pages | conf | 35 quoted spans in 20 repo rows: 32 verbatim on the cited page, 2 verbatim on another NCF page, 1 elided paraphrase (PL-S10, below). Example: "Including a donate button can make it easy for others to give directly to your fund online." | https://www.ncfgiving.com/guide-to-giving-at-NCF |
| PL-S10 | corr | The repo has an elided paraphrase. The page reads: "Examples of what grants can't be used to provide you or someone related to you include: Event tickets or auction purchases Membership dues School tuition Fulfillment of legally binding pledges …" | guide |
| donor-info-defaults row 10 | corr | The quote "This name appears alongside your name and address on correspondence, including the letter that accompanies each grant issued by the fund." is on the guide, not on /giving-fund/ | guide |
| Terms (D07) | conf | "Use automated means, including bots, crawlers, or spiders, to extract data from the Public Website without NCF's permission" | https://www.ncfgiving.com/terms-and-disclosures |
| Grant-size statistic | n/f | The www impact-report pages are download stubs. The 2024 story gives "$2.6 billion to more than 36,000 churches, ministries, and other charities" and no grant count. The 2025 PDF is on site.ncfgiving.com, outside this task's scope (queue P-B5201-04) | https://www.ncfgiving.com/stories/2024-impact-report-shining-like-stars |

The redirects seen were /about/ → /why-ncf, /givingfund → /giving-fund, and /fees/ → /fees.

### 3.6 Every.org

| Item | Status | Finding |
|---|---|---|
| /terms, /charity-api (P-B43N26-03-02) | blk | https://www.every.org/robots.txt returned HTTP 429 with a "Vercel Security Checkpoint" JS-challenge page at 17:11 and again at 17:21 UTC. Under the rules this counts as disallowed and as a challenge. Neither page was requested. The four AI-use cells remain "not determinable" |

### 3.7 b51-03 blocked list

| b51-03 entry | Reason then | This pass |
|---|---|---|
| B1 Vanguard | terms | Fetched; averages found (§3.2) |
| B2 NPT | terms | Fetched; FY21–FY25 means found; DAF Report has none (§3.3) |
| B4 PR Newswire (JCF $501) | terms | Fetched; FY21 $501 and FY22 $601 medians, FY21 $7,194 mean (§3.4) |
| NCF, charitynavigator.org | shared-rule terms | NCF www has no statistic (§3.5). CN publishes no sponsor grant-size statistic, so nothing was fetched for this |
| B3 Schwab/DAFgiving360, B5 Candid, B6 Chronicle, B7 Benefaction | robots | Not attempted (still robots-blocked) |

**Effect on b51-03 §3.2 [C].**
- **Vanguard.** The published CY2024 mean is $12,926. The table's computed means are $13,782 (DAFRC FY2024 dollars ÷ 990 count 221,825) and $13,524. These are FY and CY on different count bases, so a 4–7% gap is expected.
- **NPT.** The published FY24 mean is $42,387, against the computed $42,935, a 1.3% gap.
- **Ordering.** Both sponsors keep their place in the retail vs high-touch ordering.

## 4. Proposed corrections (for the validator; not applied)

C1. **Charity Navigator provenance.** Applies to `research/mission-2026-11-14/b43n26-03-0304-pledge-mcp-cn-ai.md` §4 item 6, `validation-wave48a-report.md` (CN terms compliance) and `FINAL-STATUS.md` line 131. Replace "flagged pending the owner's manual read" with: "re-fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01); CNAI-01/02/03/05, the API Terms keyword count (0) and the 18-release screen match verbatim." CNAI-01 no longer needs re-sourcing to Giving Compass. The quotes may now go into synthesis.

C2. **`grant-count-denominators-2026-11-20.csv` GC-002 `notes`.** Append: "NPT's FY24 annual report (https://www.nptrust.org/annual-reports/the-2024-annual-report/) prints 130,875 grants and 41,879 recipients for FY24; the FY25 report restates FY24 as 129,575 [b52-01]."

C3. **`sponsor-published-grant-stats-2026-11-19.csv` A-NPT-FY24 `notes`.** Append: "Denominator 130,875 is the FY24 report's figure; the FY25 report restates FY24 to 129,575 (GC-002) [b52-01]."

C4. **`exception-share-per-grant-2026-11-19.csv`, NPT `published_grants_G` notes.**
- FY2023: append "106,235 is the FY25 report's restated value; the FY23 report printed 107,385 and 36,361 recipients".
- FY2024: append "129,575 restated; FY24 report printed 130,875 and 41,879 recipients".

C5. **GC-021 `notes`.** Append "Release dated 2025-10-20 (dateline CHARLESTON, S.C., Oct. 20, 2025) [b52-01]."

C6. **`b51-03-grant-size-distribution.md`.**
- §2.2: move the Vanguard, NPT and PR Newswire rows out of "Not obtained".
- §3.2 table, "Published" column: Vanguard "blocked" → "$12,926 avg (CY2024 AR; $14,808 CY2025; ≈$14,000 FY2025)"; NPT "blocked" → "$42,387 mean (FY24, FY25 AR chart)".
- The NPT snippet note ("near $74k (FY21) and $40k (FY25) … not read at source") → "read at source: $73,866 (FY21) to $40,381 (FY25)".
- §8 B1, B2 and B4: "fetched 2026-11-20 under owner decision (b52-01)".

C7. **`grant-size-distribution-2026-11-20.csv`.** Add `published_stat` rows PS-20 onward. Quotes and URLs are in the b52-01 CSV:

| CSV row | Sponsor | Period | Statistic |
|---|---|---|---|
| B5201-030 | Vanguard | CY2022 | $9,500 average |
| B5201-031 | Vanguard | CY2023 | $12,412 average |
| B5201-032 | Vanguard | CY2024 | $12,926 average |
| B5201-033 | Vanguard | CY2025 | $14,808 average |
| B5201-034 | Vanguard | FY2023 | $10,972 average |
| B5201-035 | Vanguard | FY2025 | ≈$14,000 average |
| B5201-052 | NPT | FY21–FY25 | Means $73,866 to $40,381 |
| B5201-062 | JCF | FY2021 | $501 median |
| B5201-063 | JCF | FY2021 | $7,194 average |
| B5201-064 | JCF | FY2022 | $601 median |

C8. **`daf-pledge-policy-2026-11-19.csv` PL-S10 quote.** Replace with: "Examples of what grants can't be used to provide you or someone related to you include: … Fulfillment of legally binding pledges".

C9. **`donor-info-defaults-top20-2026-11-19.csv` row 10.** Add https://www.ncfgiving.com/guide-to-giving-at-NCF as the source of the fund-name/anonymity quote. The quote is not on /giving-fund/.

C10. **`b43n26-03-charity-data-terms-ai.md` §2.3 and S11.** Append: "2026-11-20 (b52-01): robots.txt still 429, now serving a Vercel Security Checkpoint challenge; terms still unread."

C11. **`research-priority-inputs.csv` / `research-priority-queue.csv` P-B4222-02-02.** Keep it blocked and append: "2026-11-20 b52-01 re-check (terms lifted): 0 donate pages in 659 sitemap URLs or links; not determinable."

C12. **`b4222-02-01-01-foundant-docs-ncf-donate.md` §3 "Pages read before the terms".** Append: "Owner lifted the site-terms rule 2026-11-20; those reads are within policy (b52-01)."

## 5. Limits

- **Static HTML only.** Script-rendered content was not executed. NPT's chart values come from HTML data attributes. A script-only figure on Vanguard's pages would have been missed.
- **NPT restatement unexplained.** NPT does not say why the FY25 report revises earlier years. Which series is "right" for a denominator is a judgement call (P-B5201-01).
- **Vanguard periods are mixed.** The averages are calendar-year (annual reports) or fiscal-year (releases), and some are rounded ("approximately $14,000", "$10K"). No median or size distribution is published.
- **JCF release URLs came from a web search**, not from PR Newswire's own search. Only those named pages were fetched.
- **NCF.** Quote checks covered CSV quote columns and quoted spans in `data/`, not prose in research Markdown. The 2025 impact-report PDF (site.ncfgiving.com) was out of scope.
- **Every.org** is untested beyond its robots.txt.
- **Inherited caveats.** B-NPT-FY20 and the A-NPT-FY21 / B-NPT-FY21 snippets remain unverified.
- **Recency.** Pre-2021 values (Vanguard 2020 share, NPT FY15/FY20) are context only, as in the source rows.

## 6. Data dictionary: `terms-lifted-fetch-2026-11-20.csv`

| Column | Meaning |
|---|---|
| check_id | B5201-nnn; numbering is grouped by target (001–008 CN, 010–037 Vanguard, 040–054 NPT, 060–064 PRN, 070–075 NCF, 080 Every.org, 090 scope) |
| target | Task target (T1–T7) |
| item_type | repo_quote_check, repo_value_check, repo_source_check, terms_keyword_check, terms_text, release_screen, provenance_flag, new_grant_size_stat, new_conflicting_value, count, not_found, access, scope |
| repo_file | Repo file (or files) whose content the row checks or would extend |
| repo_row_id | Row id or section in that file |
| item | What was checked |
| repo_value | Value or text the repo holds |
| fetched_value | What the fetched source shows |
| result | confirmed, confirmed_with_note, corrected, new, not_found, unverifiable, blocked |
| quote | Verbatim text from source_url, script-checked against the fetched copy. Chart attributes are quoted from raw HTML |
| source_url | URL requested (redirects noted in notes) |
| source_date | Date printed on, or applying to, the source |
| retrieved | 2026-11-20 |
| http_status | HTTP status of the fetch |
| robots | robots.txt result for the host |
| notes | Context, computations [C] and cross-references |

## 7. Robots log (2026-11-20, user agent `research-script/1.0`)

| Host | robots.txt | Anthropic-agent group | Decision | Requests |
|---|---|---|---|---:|
| www.charitynavigator.org | 200. `*`: Disallow /cgi-bin/, /search, /confirmation/. Sitemaps declared | none | allowed for all paths used | 27 (4 robots, 3 sitemaps, 18 releases, 2 terms pages) |
| www.vanguardcharitable.org | 200. `*` group (Allow /core/*.css etc.; disallows /core/ and /profiles/ paths) | none | allowed | 15 (1 robots, 14 pages) |
| www.nptrust.org | 200. YisouSpider and Baiduspider Disallow /; `*` empty Disallow | none | allowed | 16 (4 robots, 3 sitemaps, 9 pages incl. 1 404) |
| www.prnewswire.com | 200. `*`: Disallow /templates/…, /widget-landing-page.html, /multivu/ | none | allowed | 6 (1 robots, 5 releases) |
| www.ncfgiving.com | 200. `User-agent: *` / `Disallow:` (empty) | none | allowed | 26 (2 robots, 9 sitemaps, 15 pages) |
| www.every.org | **429**, "Vercel Security Checkpoint" challenge (×2) | n/a | **disallowed / blocked** | 2 (robots only) |
| secure.ncfgiving.com | not requested (shared rules: disallows all) | — | off-limits | 0 |
| site.ncfgiving.com | not requested (outside www-only scope) | — | not checked | 0 |

robots.txt was re-read at the start of each fetch batch, so hosts show more than one robots request. No page returned a CAPTCHA, a challenge, 403, a login or a form. The one 404 was NPT `?p=6867`.

## 8. Source register

| # | Source | Date | URL | Label |
|---|---|---|---|---|
| S1 | CN release: Horizon AI Search | 2025-11-24 | https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search/ | F |
| S2 | CN release: Allegory | 2026-05-18 | https://www.charitynavigator.org/about-us/press-release/allegory-integrates-cn-api/ | F |
| S3 | CN release: board | 2025-07-15 | https://www.charitynavigator.org/about-us/press-release/charity-navigator-expands-board/ | F |
| S4 | CN API Terms of Use | Oct 2026 | https://www.charitynavigator.org/products-and-services/api/ (→ /products-and-services/graphql-api/api-terms-of-use/) | F |
| S5 | CN website Terms of Use | 2022-11-01 | https://www.charitynavigator.org/about-us/financials-and-policies/terms-of-use/ | F |
| S6 | CN sitemap index and post sitemap (18 releases) | live | https://www.charitynavigator.org/sitemap_index.xml ; https://www.charitynavigator.org/post-sitemap.xml | F |
| S7 | Vanguard Charitable annual reports 2022–2025 | CY2022–CY2025 | https://www.vanguardcharitable.org/2022annualreport ; /2023annualreport ; /2024annualreport ; /2025annualreport | F |
| S8 | Vanguard Charitable news releases (8) | 2022-01-25 to 2026-03-02 | URLs in §3.2 (prefix https://www.vanguardcharitable.org) | F |
| S9 | Vanguard Charitable nonprofit page | live | https://www.vanguardcharitable.org/nonprofit-organizations | F |
| S10 | Vanguard Charitable terms | live | https://www.vanguardcharitable.org/company-policies/terms-and-conditions | F |
| S11 | NPT FY25 annual report | FY2025 | https://www.nptrust.org/annual-reports/npt-annual-report/ | F |
| S12 | NPT FY24 annual report | FY2024 | https://www.nptrust.org/annual-reports/the-2024-annual-report/ | F |
| S13 | NPT FY23 annual report | FY2023 | https://www.nptrust.org/annual-reports/the-2023-annual-report/ | F |
| S14 | NPT DAF Report hub and 2024 DAF Report | 2024-11 | https://www.nptrust.org/reports/daf-report/ ; https://www.nptrust.org/reports/the-2024-daf-report/ ; https://www.nptrust.org/wp-content/uploads/2024/11/2024-DAF-Report-NPT.pdf | F |
| S15 | NPT for-nonprofits page | live | https://www.nptrust.org/for-charities/ (→ /for-nonprofits/) | F |
| S16 | NPT terms (privacy-policy page) | live | https://www.nptrust.org/privacy-policy/ | F |
| S17 | NPT sitemaps | live | https://www.nptrust.org/sitemap_index.xml ; /reports-sitemap.xml ; /annual-reports-sitemap.xml | F |
| S18 | JCF FY2024 release (GC-016) | 2024-08-22 | https://www.prnewswire.com/news-releases/jewish-communal-fund-donors-grant-record-breaking-1-billion-in-fiscal-year-2024-302227664.html | F |
| S19 | Blackbaud Giving Fund 2024 release (GC-021) | 2025-10-20 | https://www.prnewswire.com/news-releases/the-blackbaud-giving-fund-surpasses-550m-in-charitable-giving-in-2024--reaching-2-75b-in-lifetime-giving-302588766.html | F |
| S20 | JCF 2021 Giving Report release | 2022-01-10 | https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-record-number-of-grants-to-charity-totaling-520-million-in-fy-21-301456454.html | F |
| S21 | JCF FY2021 grants release | 2021-10-28 | https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-out-520-million-in-grants-in-fy-2021-301409897.html | F |
| S22 | JCF 50th-anniversary Giving Report release | 2023-02-07 | https://www.prnewswire.com/news-releases/jewish-communal-fund-releases-50th-anniversary-giving-report-301740253.html | F |
| S23 | NCF guide to giving | live | https://www.ncfgiving.com/guide-to-giving-at-NCF | F |
| S24 | NCF www pages (support, EFT sign-up, AI search, terms, fees, about, giving fund, assets, charities, single-charity fund) | live | https://www.ncfgiving.com/support ; /eft-charity-sign-up ; /ai-search ; /terms-and-disclosures ; /fees/ ; /about/ ; /giving-fund/ ; /givingfund ; /assets ; /charities/ ; /single-charity-fund-for-charities | F |
| S25 | NCF impact pages | 2025-01-01; live | https://www.ncfgiving.com/stories/2024-impact-report-shining-like-stars ; /impact-report-2025 ; /documents/expedition-generosity-2025-impact-report/ | F |
| S26 | NCF sitemap index and 8 child sitemaps | live | https://www.ncfgiving.com/sitemap.xml (sitemap-page, -post, -story, -event, -document, -video, -podcast, -book .xml) | F |
| S27 | Every.org robots.txt | — | https://www.every.org/robots.txt | B (429 challenge) |
| S28 | Repo inputs | 2026-11-19/20 | data/mission-2026-11-14/pledge-mcp-cn-ai-2026-11-20.csv; grant-count-denominators-2026-11-20.csv; sponsor-published-grant-stats-2026-11-19.csv; exception-share-per-grant-2026-11-19.csv; grant-size-distribution-2026-11-20.csv; research/mission-2026-11-14/validation-wave48a-report.md; b43n26-03-charity-data-terms-ai.md; b43n26-03-0304-pledge-mcp-cn-ai.md; b51-03-grant-size-distribution.md; b4222-02-01-01-foundant-docs-ncf-donate.md | R |
