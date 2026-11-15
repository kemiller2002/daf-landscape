# Validation wave 24B: new directions N5–N8 (DAF news and hiring signals, nonprofit donate pages, donor behaviour and crises, academic literature) and literature flags F1–F4

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave24b.
**Register:** [`validation-register-wave24b.csv`](../../data/mission-2026-11-14/validation-register-wave24b.csv), rows V24B-01 to V24B-29.
**Documents validated:**
- N5: [direction-news-hiring-signals.md](direction-news-hiring-signals.md)
- N6: [direction-nonprofit-donate-pages.md](direction-nonprofit-donate-pages.md)
- N7: [direction-donor-behaviour-crises.md](direction-donor-behaviour-crises.md)
- N8: [direction-academic-literature.md](direction-academic-literature.md)

**Method:** public sources only. I did not log in, submit forms, solve or bypass CAPTCHAs or bot challenges, make keyed API calls or contact anyone. I read robots.txt on each host before fetching a page (details under Limits). **I did not use crt.sh.** I did not scrape LinkedIn, Indeed or Glassdoor. I used a generic User-Agent. For each claim I formed a verdict from primary sources first and compared it with the documents afterwards. The sources were:
- **CSVs recomputed** independently:
  - `daf-news-volume-2021-2026.csv`: annual, half-year, Jan–Oct, Jan–Aug and Nov–Dec rates, theme shares and peak months;
  - `daf-hiring-signals-2026.csv`: segment and employer AI shares and AI titles;
  - `nonprofit-donate-page-daf-scan-2026.csv`: sample dollars, coverage, flag rates, sector and size cells, dollar weighting;
  - `donor-behaviour-metrics-2021-2026.csv`: row and category counts;
  - `daf-grant-recipient-sectors-top50.csv`: the DAF-to-DAF share by sponsor segment (for F3).
- **GDELT, re-queried live.** The base series (`timelinevolraw`) was tried 10 times over about 20 minutes with backoff, and every attempt returned HTTP 429. The news counts are therefore confirmed as CSV arithmetic only.
- **Hiring endpoints, re-fetched** after their robots.txt:
  - Greenhouse `tifin` and `renpsg`;
  - the Chariot and Benevity Ashby boards, via the robots-allowed `jobs.ashbyhq.com` HTML, plus two Chariot posting pages;
  - the Blackbaud search-results page;
  - the Fidelity jobs sitemap. Fidelity job pages now return a Cloudflare challenge, which I did not bypass.
- **Donate pages re-read** for a stratified random sample of 30 charities (seed 20261115): 10 of the 25 DAFpay positives and 20 of the 161 others.
  - Each donate host's robots.txt was read first, and redirect targets were re-checked.
  - One donate page per charity, fetched as raw HTML (curl) and rendered DOM (headless Chrome `--dump-dom`, images off).
  - Nothing was clicked or submitted.
  - 29 were fetched. stjude.org failed at the protocol level here, so it was not fetched.
- **Donor-behaviour sources:**
  - Fidelity Charitable Giving Reports 2022, 2023, 2025 and 2026 (pdftotext) and the H1 2022 release;
  - Vanguard Charitable releases of 2023-01-25, 2025-02-04, 2025-08-25 and 2026-03-02;
  - Daffy Year in Review 2025; the Chariot Daffy summary;
  - Pulse 2.0's DAFgiving360 reprint;
  - BofA's 2026 Study of Wealthy Americans page.
- **Literature:**
  - doi.org handle API for 24 DOIs, and Crossref works records with abstracts;
  - DAFRC 2024 executive summary (Johnson Center); DAFRC 2022 Patterns & Trends executive summary; DAFRC 2025 manager and donor survey executive summaries;
  - CA AG 2022 overview (39 pp.); IPS 2025 report (29 pp.); Leff 2025 full text (66 pp.);
  - NBER pages for w32737 and w27888.

## Headline

The four new-direction documents are accurate on their numbers. Every filed figure I could reach reproduces, and the quotes are verbatim. No claim is contradicted.

**What holds independently:**
- **N5 news.** All annual counts (9,486 in total), the per-million rates (all twelve half-years), the theme shares and the peak months recompute exactly from the CSV.
  - The 2026 rebound in normalised volume does not depend on GDELT's collapsing late-2026 base. Jan–Aug 2026 runs at 21.9 per million against 12.7 in Jan–Aug 2025.
- **N5 hiring.**
  - The CSV gives 168 roles at 12 employers, 46 of 166 mentioning AI (27.7%), vendors 29.1% and sponsors 13.3%.
  - The live boards match: Chariot's 19 titles, Benevity's 23 postings and 14 titles, Ren's 6 roles (the same 3 with AI terms), TIFIN's 3 roles, and Blackbaud's `totalHits` of 86.
  - Chariot's "Applied AI Engineer" and "Software Engineer, Agentic Infrastructure" postings are live. Its Compliance Operations posting reads "Use AI and documentation to speed up compliance customer support".
- **N6.** The sample totals $24,080,513,150 with a cutoff of $24,718,654. Every headline rate and every sector and size cell reproduces from the CSV.
  - In my 29-page re-read, the "donor-advised" flag matched on 29 of 29 pages, the own-EIN flag on 29 of 29 and "any DAF option" on 28 of 29.
  - 7 of 10 DAFpay positives reproduced directly. The other 3 render their donation form inside an iframe that `--dump-dom` cannot read; the scan read child frames.
  - No DAFpay appeared on any of the 19 negatives.
- **N7.** Every figure checked is verbatim in its source:
  - BofA 9% / 20%;
  - Fidelity medians $24,086 → $19,442 (−19.3%) → $27,860; average grant $4,407 → $5,801; prescheduled 27% → 32%;
  - GivingTuesday 2025: 48,000 grants and more than $129m;
  - Ukraine: more than $128m (Fidelity) and more than $70m (Vanguard); Helene/Milton "nearly $50 million";
  - Vanguard's average grant of about $14,000 and the "78% ... by 11/30/2024" footnote (about 22% in December); $953m in Nov–Dec 2025;
  - Daffy's $100 median, more than 45% recurring, and more than $200m of more than $470m in December;
  - DAFgiving360's $500 median, which comes from a reprint and is labelled [S].
- **N8.**
  - 24 DOIs resolve, and 22 Crossref records match the cited authors, titles, venues, volumes and pages.
  - Main findings are stated fairly for 16 works checked against their abstract or full text.
  - **F1** (DAFRC: 9% median, 15% excluding inactive accounts, 18% mean, 22% inactive in 2020–22) is confirmed verbatim.
  - **F4** is confirmed: IPS uses grants ÷ (year-end assets + grants), and its 9.7% is a median of sponsors' rates, against NPT's 23.9% on beginning assets.

**Qualifications (partially confirmed):**
1. **"The 2026 rebound is policy-led" (N5) is not shown by the theme data.** The legislation share fell from 38.2% (2025) to 36.3% (2026). The two biggest 2026 months are 2026-03 (33% legislation) and 2026-06 (26%), both below the year's share. In 2026-01, 17 of 47 DAF articles match the AI group, an outlier for the planned precision check.
2. **The ATS robots handling is RFC-defensible but inconsistent with the repo convention (N5).**
   - `api.ashbyhq.com/robots.txt` returns **401**, which the script treats as allow-all.
   - `workforcenow.adp.com/robots.txt` **302-redirects to an ADP login page**, which is parsed as an empty rule set.
   - N6 and wave 23 treat 401/403 or a login wall as unreadable and do not fetch the host.
   - The Chariot and Benevity lists reproduce from the robots-allowed `jobs.ashbyhq.com` boards. Vanguard Charitable's 4 roles have no robots-clean route.
3. **Fidelity Charitable 0 of 11 (N5)** cannot be re-observed. The sitemap lists 789 `en/jobs` URLs, including the cited titles, but the job pages are now behind a Cloudflare challenge.
4. **Four scanned "donate pages" are not donate pages (N6):** rank 77 (a UA Foundation news item), 84 (a Rockefeller Foundation news item), 165 (a USCCB news article) and 244 (Boston Children's "donate-blood"). Without them, the rates are any option 75/182 = **41.2%** and DAFpay 25/182 = **13.7%**. Two donate URLs still carry tracking parameters.
5. **The $76.70bn denominator (N6)** is consistent with the repo's $77.34bn non-DAF-to-DAF pool, which includes blank-EIN lines, but cannot be rebuilt without the lines cache.
6. **The Daffy "55% → 37%" correction (N7).** The editor's note says only that an earlier version "misstated the donation payout rate". The 55% figure is Chariot's summary of it.
7. **The DAFRC robots reason (N7) is inaccurate.** `dafresearchcollaborative.org/robots.txt` lists ClaudeBot and anthropic-ai in the same group as `User-agent: *`, so `/s/` PDFs are allowed. N8's reads from that host were compliant.
8. **F2.** Flannery & Mittendorf's abstract says, among nationals, that donor-benefit website language predicts larger assets "largely attributable ... to lower payout rates". The measure is marketing language, not fees. It supports *suggestive* for orientation and payout, not for the asset-based fee mechanism.
9. **F3.**
   - **The quotation is exact:** 11% overall (10.8%), 18% at CFs (17.8%), 10% commercial and 5% mission-based.
   - **The data are not current or national:** they cover 2016-07 to 2020-12 and 57 California-registered sponsors.
   - **The definition is unclear:** the report does not say whether its "grants to other DAFs" include fund-to-fund transfers inside the same sponsor.
   - **The repo's own top-50 Schedule I data point the other way:** CFs excluding SVCF send **5.1%** of FY2023–24 Schedule I dollars to other DAF sponsors, against **13.7%** for nationals. CFs including SVCF send 14.2%, driven by SVCF's FY2024 23.9%.
   - "CFs may send the largest share" is therefore not supported nationally except through SVCF.
10. **Wording in N8:**
    - "39% of sponsors lack sufficient IT" is a complement, not a reported figure.
    - Leff does not call the spread "unresolved". He says the range "illustrates disputes over the proper methodology" and declines to join the debate.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V24B-01 | GDELT 9,486 articles; annual counts | **Partially confirmed** | CSV exact; live API 429 throughout, so not re-pulled |
| V24B-02 | Per-million normalisation; 2026 rebound | **Confirmed** | All half-years exact; Jan–Aug 2026 21.9 vs 12.7 |
| V24B-03 | Theme shares; "policy-led" rebound | **Partially confirmed** | Shares exact (legislation 34.0%, payout 20.3%, AI 1.2→5.8%); legislation share fell in 2026 |
| V24B-04 | 168 roles, 27.7%, vendors 29.1%, sponsors 13.3% | **Confirmed** | CSV exact; live boards match |
| V24B-05 | Fidelity Charitable 0 of 11; 787 pages, 10.2% | **Partially confirmed** | Sitemap 789 URLs with titles; pages behind Cloudflare now |
| V24B-06 | Named AI roles (Chariot, Blackbaud, TIFIN, Benevity) | **Confirmed** | Chariot quote verbatim; TIFIN roles are TIFIN.ai / @Work |
| V24B-07 | ATS robots compliance | **Partially confirmed** | Ashby API robots 401 and ADP robots redirects to login, both read as allow |
| V24B-08 | Sample $24.08bn, 31.4%, cutoff $24.7m | **Partially confirmed** | Sum and cutoff exact; $76.70bn not rebuilt |
| V24B-09 | DAFpay 13.4% (25/186) | **Partially confirmed** | 7/10 positives reproduced; 3 iframe-only; 0/19 false negatives |
| V24B-10 | Any option 40.3%; donor-advised 34.9%; EIN 36.0% | **Partially confirmed** | Flags match 28–29/29; 4 non-donate pages in the denominator |
| V24B-11 | DAF Direct 3; sponsor 8 | **Confirmed** | Accion OF matches all flags |
| V24B-12 | Sector and size splits | **Confirmed** | All cells exact |
| V24B-13 | Scan conduct (robots, URL stripping) | **Partially confirmed** | Robots verdicts agree; 2 URLs keep tracking parameters |
| V24B-14 | BofA 9% / 20% | **Confirmed** | Verbatim |
| V24B-15 | Fidelity medians; −19% 2022 | **Confirmed** | $24,086 / $19,442 / $27,860 |
| V24B-16 | Average grant $4,407 → $5,801; prescheduled 27% → 32% | **Confirmed** | 2022 and 2026 reports |
| V24B-17 | DAFgiving360 median $500 [S] | **Confirmed** | Pulse 2.0 reprint |
| V24B-18 | Daffy $100; >45%; December ≈43% | **Confirmed** | Verbatim; 200/470 = 42.6% |
| V24B-19 | Vanguard ≈$14k; December ≈22%; $953m | **Confirmed** | Verbatim; 78% footnote |
| V24B-20 | Fidelity GivingTuesday 2025 48,000 / $129m | **Confirmed** | 2026 report p.13 |
| V24B-21 | Ukraine $128m / $70m | **Confirmed** | Verbatim |
| V24B-22 | Helene/Milton ≈$50m | **Confirmed** | "nearly $50 million" |
| V24B-23 | Daffy payout 55% → 37% | **Partially confirmed** | The note gives no prior figure; 55% is Chariot's |
| V24B-24 | Literature citations resolve; findings fair | **Confirmed** | 24 DOIs, 22 Crossref matches, 16 findings checked; one complement wording |
| V24B-25 | F1 DAFRC account-level payout | **Confirmed** | 9% / 15% / 18% / 22%; 111 programs incl. nationals |
| V24B-26 | F2 Flannery & Mittendorf 2025 | **Partially confirmed** | Abstract exact; language, not fees; correlational |
| V24B-27 | F3 CA AG: CFs 18% vs 11% | **Partially confirmed** | Quote exact; 2016–20, CA-registered; repo CFs ex-SVCF 5.1% vs nationals 13.7% |
| V24B-28 | F4 payout formula differences | **Confirmed** | IPS IRS formula, median of sponsors; NPT beginning assets; Leff fn 95 |
| V24B-29 | DAFRC robots (N7 reason vs N8 fetches) | **Partially confirmed** | Claude agents share the `*` group; `/s/` allowed |

### Rulings on the documents' proposals and flags

- **F1:** **supported**. The §1 sentence should keep "not public" for filings and add the voluntary-sample account medians. The aggregate is not contradicted.
- **F2:** **partially supported**.
  - The §3 row should stay **Mixed** with confidence **Low on effect**.
  - Replace "effect on payout unsupported" with wording that cites the correlational study and says what it measures.
  - Do not upgrade the fee-alignment mechanism to *suggestive*.
- **F3:** **not supported as a re-framing**. Record the CA AG figure as dated, self-reported and definitionally unclear. Note that the repo's own filings show CF transfers to other sponsors at about 5% outside SVCF. P-B39N8-02 remains a useful test.
- **F4:** **supported**. A definition bridge (P-B39N8-01) is worthwhile.
- **N5 §2.4 limitation:** the GDELT figures could not be re-pulled in wave 24B (429). They stand on the run cache.

## Exact corrections

### `research/mission-2026-11-14/direction-news-hiring-signals.md`
1. **§1 Summary, news reading.**
   - **Find:** "AI is an emerging but minor news frame, and the 2026 rebound is policy-led."
   - **Replace with:** "AI is an emerging but minor news frame. The 2026 rebound in normalised volume is real: Jan–Aug 2026 runs at 21.9 per million against 12.7 in Jan–Aug 2025. The theme data do not show it is policy-led. The legislation share fell from 38.2% (2025) to 36.3% (2026), and the largest 2026 months, 2026-03 and 2026-06, carry 33% and 26% legislation matches [V wave 24B]."
2. **§1 Summary, AI titles.**
   - **Find:** "Blackbaud (4, including \"AI Governance Principal\") and TIFIN (2)."
   - **Replace with:** "Blackbaud (4, including \"AI Governance Principal\") and TIFIN (2: \"AI Engineering, TIFIN.ai\" and \"Senior AI Engineer, TIFIN @Work\", group roles rather than TIFIN Give) [V wave 24B]."
3. **§3.1 Method, robots.**
   - **Find:** "The decision log is in the work directory (`robots-log-hiring.json`)."
   - **Replace with:** "The decision log is in the work directory (`robots-log-hiring.json`). Two sources had no readable robots.txt:\n  - `api.ashbyhq.com/robots.txt` returns 401, read here as no rules. This covers Chariot and Benevity.\n  - `workforcenow.adp.com/robots.txt` redirects to an ADP login page, parsed as an empty rule set. This covers Vanguard Charitable.\n\n  Both readings follow RFC 9309, but they differ from the repo convention (N6, wave 23), under which 401/403 or a login wall means unreadable and the host is not fetched. The Chariot and Benevity role lists reproduce from the robots-allowed `jobs.ashbyhq.com/<board>` pages (robots disallows only `/api/`, `/b/` and `/meeting/` there). Vanguard Charitable's 4 roles have no robots-clean route. Fidelity job pages now return a Cloudflare challenge to scripted clients, so the 0-of-11 result could not be re-observed in wave 24B [V wave 24B]."
4. **§2.4 Limitations, rate limits.**
   - **Find:** "- **[L] Rate limits.** GDELT throttled this session heavily. Every number comes from a completed API response cached in the work directory; no value was imputed."
   - **Replace with:** "- **[L] Rate limits.** GDELT throttled this session heavily. Every number comes from a completed API response cached in the work directory; no value was imputed. Wave 24B could not re-pull the base series: all 10 attempts over about 20 minutes returned HTTP 429. The counts are confirmed as CSV arithmetic only [V wave 24B]."

### `research/mission-2026-11-14/direction-nonprofit-donate-pages.md`
1. **§5 Limitations, new bullet after the snapshot bullet.**
   - **Find:** "- **One-day snapshot** (2026-11-15). Year-end campaigns can change forms."
   - **Replace with:** "- **One-day snapshot** (2026-11-15). Year-end campaigns can change forms.\n- **Link choice.** At least four scanned \"donate pages\" are not donate pages: rank 77 (a UA Foundation news item), 84 (a Rockefeller Foundation news item), 165 (a USCCB news article) and 244 (Boston Children's \"donate-blood\" page). None shows a DAF option. Without them, any DAF option is 75/182 (41.2%) and DAFpay 25/182 (13.7%). Two `donate_url` values still carry tracking parameters (e.g. `_ga`) [V wave 24B].\n- **Wave 24B re-read.** A stratified sample of 30 charities was re-read (10 of 25 DAFpay positives, 20 others; 29 fetched).\n  - The \"donor-advised\" and own-EIN flags matched on 29 of 29 pages, and \"any DAF option\" on 28 of 29.\n  - 7 of 10 DAFpay positives reproduced from the page and rendered DOM. The other 3 (IPPF, Per Scholas, Edesia) carry the form in an iframe, which only a frame-level read sees.\n  - No negative showed DAFpay [V wave 24B]."

### `research/mission-2026-11-14/direction-donor-behaviour-crises.md`
1. **Rules applied, robots.**
   - **Find:** "and dafresearchcollaborative.org (its robots.txt names Claude-family user-agents)."
   - **Replace with:** "and dafresearchcollaborative.org (not fetched in this run). Its robots.txt lists ClaudeBot and anthropic-ai in the same group as `User-agent: *`, so `/s/` documents are allowed. The DAFRC values here still come from the repo series [V wave 24B]."
2. **§2.2, Daffy payout correction.**
   - **Find:** "an editor's note dated 2026-07-28 corrected the payout claim from 55% to \"more than 37%\"."
   - **Replace with:** "an editor's note dated 2026-07-28 says an earlier version \"misstated the donation payout rate\". The text now says \"more than 37 cents of every dollar held in Daffy funds at the end of 2024 was distributed to charity in 2025\". The earlier figure appears as 55% in Chariot's summary; the note itself does not state it [V wave 24B]."
3. **§7, S11.**
   - **Find:** "dafresearchcollaborative.org (robots.txt names Claude-family agents)"
   - **Replace with:** "dafresearchcollaborative.org (not fetched; its robots.txt gives Claude agents the same rules as `*`, which allow `/s/` [V wave 24B])"

### `research/mission-2026-11-14/direction-academic-literature.md`
1. **§2, F1 handling.**
   - **Find:** "Keep the sentence for *public filings*, and add that voluntary account samples put the median account at about 9%."
   - **Replace with:** "Keep the sentence for *public filings*, and add that voluntary account samples put the median account at about 9%. [V wave 24B: confirmed verbatim. The DAFRC 2024 executive summary gives a 9% median, 15% excluding inactive accounts and an 18% mean; 22% of accounts were inactive in 2020–22; 111 programs, including nationals.]"
2. **§2, F2 handling.**
   - **Find:** "Candidate to move from *unsupported* to *suggestive*, with the caveat that the measure is marketing language, not fee structure, and the result is correlational. Needs a validator decision."
   - **Replace with:** "Validator decision (wave 24B): keep the row **Mixed** (Low on effect). Cite this study as correlational evidence that a donor-benefit orientation goes with lower payout among nationals. Do not treat it as evidence on asset-based fees, because the measure is website language, not fee structure."
3. **§2, F3 handling.**
   - **Find:** "The overall share agrees with the repo's 10–18%. The CF result could mean R5 under-nets CF payout. Queue proposal P-B39N8-02."
   - **Replace with:** "The overall share agrees with the repo's 10–18%. The CF figure does not carry over nationally:\n- It is self-reported for 2016-07 to 2020-12 by 57 California-registered sponsors.\n- It does not say whether fund-to-fund transfers inside the same sponsor count as \"grants to other DAFs\".\n- The repo's top-50 Schedule I data put CFs excluding SVCF at 5.1% of FY2023–24 dollars to other DAF sponsors, against 13.7% for nationals; including SVCF, 14.2% [V wave 24B].\n\nQueue proposal P-B39N8-02 tests it."
4. **§2, F4.**
   - **Find:** "Leff (2025) calls the spread unresolved."
   - **Replace with:** "Leff (2025, fn. 95) says the 9.7%–23.9% range \"illustrates disputes over the proper methodology\" and does not resolve it [V wave 24B]."
5. **§6, §3 challengers row.**
   - **Find:** "Manager survey: 39% of sponsors lack sufficient IT."
   - **Replace with:** "Manager survey: 61% of sponsors report sufficient IT (74% policies, 60% budget, 52% staffing) [V wave 24B]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **§1, payout (F1, F4).**
   - **Find:** "Fund-level payout is not public ((source: repo inference — no primary URL))."
   - **Replace with:** "Fund-level payout is not public in filings ((source: repo inference — no primary URL)). Voluntary account-level samples exist:\n- DAFRC's 2024 National Study (111 programs, over 50,000 accounts) puts the median three-year account payout at 9% (15% excluding inactive accounts) and the mean at 18%. 22% of accounts made no grants in 2020–22 ([executive summary](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf); doi:10.4087/ymfd7624).\n- This does not contradict the 23.9% aggregate, because a few large, fast-paying accounts carry the aggregate. Published payout figures also differ by definition: IPS's 9.7% is a median of sponsors' rates on grants ÷ (year-end assets + grants), while NPT's 23.9% is an aggregate on beginning assets ([IPS 2025](https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf)) [V wave 24B]."
2. **§1, transfers bullet (F3).**
   - **Find:** "They inflate apparent payout and double-count in market sums."
   - **Replace with:** "They inflate apparent payout and double-count in market sums. California's 2022 AG audit reports 18% of community-foundation DAF grants going to other DAFs. That figure covers 2016–20 and 57 California-registered sponsors, and its definition is unclear. In the repo's top-50 filings, community foundations other than SVCF send about 5% of Schedule I dollars to other DAF sponsors ([CA AG 2022](https://oag.ca.gov/system/files/media/donor-advised-funds-overview.pdf); [`daf-grant-recipient-sectors-top50.csv`](../data/mission-2026-11-14/daf-grant-recipient-sectors-top50.csv)) [V wave 24B]."
3. **§3 incentive table, fee-alignment row (F2).**
   - **Find:** "incentive documented, effect on payout unsupported **[RT]**"
   - **Replace with:** "incentive documented. No evidence links fee structure to payout; one correlational study finds that national sponsors whose websites stress donor benefits have lower payout ([Flannery & Mittendorf 2025, NVSQ](https://doi.org/10.1177/08997640251331853)) **[RT; V wave 24B]**"
4. **New subsection after §11.18.** Add "### 11.19 New directions N5–N8 (validated, wave 24B)", containing the paragraph below. If wave 24A has already added an §11.19, renumber this one as the next free number.

   > **New directions N5–N8 (validated, wave 24B).**
   > - **News.** GDELT counts 9,486 English articles naming donor-advised funds in 2021 to 2026-11-14. Per million articles monitored, coverage fell from 22–27 (2021–22) to 12.1 (2025H1) and recovered to about 22 in 2026. Legislation and tax framing dominates (34% of articles), payout reform peaked in 2021 (20%), and AI is a small but rising frame (1.2% → 5.8%). The themes do not show the 2026 rebound is policy-led.
   > - **Hiring.** A snapshot of 168 open roles at 12 employers finds AI named in 29% of vendor roles against 13% at sponsors. None of Fidelity Charitable's 11 roles mentions AI. Chariot is hiring an Applied AI Engineer and an agentic-infrastructure engineer. Job ads show intent, not deployment.
   > - **Donate pages.** Among the 300 charities receiving the most DAF dollars ($24.08bn), 186 donate pages could be scanned. 13–14% show DAFpay, about 2% DAF Direct, and about 41% any DAF option. Most of those offer text instructions only.
   > - **Donor behaviour.** No sponsor publishes donor age or gender; BofA finds 9% of wealthy individuals, and 20% of those aged 21–45, use a DAF. Fidelity's median account was $27,860 in 2025, after a 19% fall in 2022, and its average grant $5,801. Medians are small: DAFgiving360 $500 [S], Daffy $100. Crisis responses are modest next to annual flows: Fidelity's more than $128m for Ukraine (H1 2022) and about $50m for Helene/Milton.
   > - **Literature.** Account-level studies (DAFRC 2024: a 9% median account payout, 22% of accounts inactive in 2020–22) qualify, but do not contradict, the 23.9% aggregate. The spread of published payout rates is largely definitional.

## Data-file notes (not .md; for the owning agent)

- **`nonprofit-donate-page-daf-scan-2026.csv`:**
  - Flag ranks 77, 84, 165 and 244 as `donate_link_not_a_donate_page`, or re-pick their link.
  - Strip the residual `_ga` / `utm_` parameters from 2 `donate_url` values.
- **`daf-hiring-signals-2026.csv`:**
  - Add a `robots_note` for the Chariot and Benevity rows (`api.ashbyhq.com` robots 401; reproduced from `jobs.ashbyhq.com`) and the Vanguard Charitable rows (ADP robots redirects to login).
  - TIFIN rows: note "TIFIN group (TIFIN.ai, TIFIN @Work), not TIFIN Give".
- **`daf-literature-2021-2026.csv`:**
  - L23 `main_finding`/`comparison_note`: use "61% report sufficient IT", not "39% lack".
  - L20: replace "unresolved" with "attributes the range to methodological disputes (fn. 95)".
  - L29: add "data 2016-07 to 2020-12; 'grants to other DAFs' undefined (may include intra-sponsor transfers)".
- **`donor-behaviour-metrics-2021-2026.csv`:** the Daffy payout row's `definition_note` should say that the 55% comes from Chariot's summary, not from Daffy's note.
- **`daf-news-volume-2021-2026.csv`:** no change. It recomputes exactly.

## Limits

- **Robots and access.**
  - **robots.txt read first** on every host fetched:
    - api.gdeltproject.org (404); boards-api.greenhouse.io (`/embed/` only); jobs.ashbyhq.com (allows boards; `/api/` disallowed);
    - jobs.fidelity.com (Allow /); careers.blackbaud.com (search results allowed); bonterra.wd1.myworkdayjobs.com (allows `/bonterratech/`); recruiting.paylocity.com (404); daffy.org (`/resources` allowed); givinga.com (allows);
    - fidelitycharitable.org (only `/retired/`, `/sample-email/`, `/nuance/` and `/vessel/` disallowed); vanguardcharitable.org (`/core/`, `/profiles/` and admin paths);
    - privatebank.bankofamerica.com (`*.pdf` disallowed; HTML only read); pulse2.com (none); givechariot.com (`/admin/*`);
    - doi.org (404); api.crossref.org (404 after one 429; nothing fetched while it was 429);
    - johnsoncenter.org (allows all); oag.ca.gov (crawl-delay 10; `/system/files/` allowed); ips-dc.org (allows all); nyujlpp.org (`/wp-admin/` only); nber.org (`/papers/` allowed);
    - dafresearchcollaborative.org (Claude agents share the `*` group; `/s/` allowed);
    - and the 29 charity donate hosts in the sample.
  - **Not fetched:**
    - **crt.sh**, per instruction.
    - **api.ashbyhq.com** (robots 401).
    - **workforcenow.adp.com** (robots redirects to login).
    - **Fidelity job pages** (Cloudflare challenge, not bypassed).
    - **stjude.org** (robots.txt protocol error here).
    - **dafgiving360.org** and **businesswire.com** (not attempted; N7 records 403).
    - **philanthropy.com**, **theconversation.com** and **jstor.org** (not attempted; N8 records AI-agent disallows).
    - No LinkedIn, Indeed or Glassdoor.
- **Not re-run:**
  - `scripts/mission_signals.py` (GDELT 429; job boards re-read directly instead);
  - `scripts/mission_donate_page_scan.py` (its `rank` stage needs the Schedule I lines cache, which is not in the repo; pages re-read with my own fetcher, without frame-level DOM);
  - the N5 headline sample;
  - the Vanguard Charitable ADP roles; the Bonterra Workday detail JSON; the full Blackbaud role list (first page only, plus `totalHits`);
  - the Charityvest reports; NPT and DAFRC account-size series; HCF, JCF and Henderson County figures;
  - for L02, L03–L11, L14, L21, L22, L25, L27, L30, L31 and M01–M06, metadata and DOI resolution only.
- **Method caveat.** My donate re-read used `--dump-dom`, which does not include iframe documents. Positives that live only inside a donation-form iframe were therefore not reproducible here (3 of 10). This is a limit of the check, not evidence against the scan.
- **Scratch.** Caches were kept under the wave scratch directory (about 35 MB) and deleted at the end.

This is research, not legal advice.
