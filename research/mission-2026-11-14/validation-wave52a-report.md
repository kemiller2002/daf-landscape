# Validation wave 52A: terms-lifted re-fetch (b52-01)

- **Study validated:** [`b52-01-terms-lifted-fetch.md`](b52-01-terms-lifted-fetch.md) with [`terms-lifted-fetch-2026-11-20.csv`](../../data/mission-2026-11-14/terms-lifted-fetch-2026-11-20.csv) (58 rows).
- **Register:** [`validation-register-wave52a.csv`](../../data/mission-2026-11-14/validation-register-wave52a.csv) (25 rows, V52A-01 to V52A-25).
- **Validator:** validator wave 52A. **Date:** 2026-11-20.
- **Basis:** the owner decision of 2026-11-20 lifting the site-terms restriction. robots.txt (including the Anthropic-agent rule) and the no-bypass rule still applied. No repo file other than this report and the register was written; the corrections below are proposals in Find/Replace form.

## Counts

| Result | Rows |
|---|---:|
| confirmed | 24 |
| partially confirmed | 1 |
| contradicted | 0 |
| unverifiable | 0 |
| **Total** | **25** |

| Proposal review (§4, C1–C12) | Count |
|---|---:|
| Accept | 6 |
| Modify | 6 |
| Reject | 0 |

Exact corrections: **31 items in 12 files** (including one new industry-report subsection, §11.79).

## Method

- **Fetcher.** A stdlib Python fetcher (functional style, `functools.reduce` over a URL list), user agent `research-script/1.0`, 3.5 s before every request. For each host it read robots.txt first and allowed a URL only if `urllib.robotparser` allowed it for ClaudeBot, anthropic-ai, Claude-User, Claude-Web, Claude-SearchBot and `*`. A non-200 robots status counted as disallowed. Raw copies stay in the session scratchpad; nothing was committed.
- **Requests (2026-11-20, about 17:25–17:34 UTC): 36 in all.** 28 named pages and sitemaps plus 8 robots.txt reads (one every.org check was repeated).

| Host | robots.txt | Anthropic-agent group | Pages fetched |
|---|---|---|---:|
| www.charitynavigator.org | 200 | none; all paths used allowed | 4 (3 releases, API terms) |
| www.vanguardcharitable.org | 200 | none | 5 (4 annual reports, FY23 release) |
| www.nptrust.org | 200 | none | 3 (FY23, FY24, FY25 reports) |
| www.prnewswire.com | 200 | none | 5 releases |
| www.ncfgiving.com | 200 (read twice) | none | 11 (sitemap index, 8 child sitemaps, guide, /giving-fund/) |
| www.every.org | **429**, “Vercel Security Checkpoint” (twice) | n/a | 0 (blocked) |

- **Matching.** HTML reduced to text (scripts and styles dropped, tags to spaces), whitespace collapsed, curly quotes and dashes normalised. Chart values were read from raw HTML attributes. Repo quotes were matched by script against the live text.
- **Not re-fetched in this wave:** the 18-release CN screen, CN site ToU, the 8 Vanguard share releases and nonprofit page, NPT DAF Report and for-nonprofits page, the NCF support/EFT/terms pages. Those rest on b52-01.

## Findings

### Charity Navigator (V52A-01 to -05)
- **CNAI-01, -02, -03 and -05 match verbatim** on the live pages. CNAI-03’s page prints “May 18, 2026” (metadata 2026-06-05), as b52-01 says.
- **API terms.** `/products-and-services/api/` redirects to `/products-and-services/graphql-api/api-terms-of-use/`, which reads “Last updated October 2026” and has 0 matches for AI, artificial intelligence, LLM, language model, machine learning, train*, model, generative, scrap* or data mining.
- The wave 48A provenance flag can be resolved; notes go to b43n26-03-0304 §4 item 6 and FINAL-STATUS.md (the wave 48A report is not edited).

### Vanguard Charitable (V52A-06 to -09, -15)
- **All values confirmed verbatim:** CY2024 240,064 grants, 62,586 charities, $3.1bn, average $12,926; CY2022 $9,500 (52,800; 196K units); CY2023 $12,412 (56,744; 209K); CY2025 $14,808, 267,838 grants, 66,785 charities, $3.96B; FY2023 release $10,972 (“more than 195,000 grants … $2.1 billion”).
- Each average is consistent with dollars / grants (for example $3.96B / 267,838 = $14,785) [C].
- b51-03’s computed FY2024 means ($13,782 and $13,524) sit 6.6% and 4.6% above the published CY2024 $12,926, as expected from the period and count-basis differences.
- FY2025 “approximately $14,000” was not re-fetched (carried from b52-01).

### NPT (V52A-10 to -14)
- **Both series confirmed.** FY25 report chart: 87,490 / 102,745 / 106,235 / 129,575 / 159,543 (FY21–FY25), dollars 6.46 / 5.53 / 4.54 / 5.49 / 6.44 ($bn). FY24 report: “NPT issued 130,875 individual grants in FY24” and 41,879 recipients; FY23 report: 107,385 and 36,361.
- **Restatement: partially confirmed.** The values are right, but:
  - the count revisions are −0.9% to −1.1%, not “0.8–1.2%”;
  - the finding is not new: wave 39A recorded the same restatement, and b4013-b4428 §2.2 already carries both series;
  - the dollar revisions run both ways (FY21 $6.41bn → $6.46bn, FY22 $5.57bn → $5.53bn, FY23 $4.50bn → $4.54bn, FY24 $5.62bn → $5.49bn). The FY23 report itself printed $4.52bn for FY23, so there are three vintages for FY23 dollars.
- **Mean-grant chart: read correctly.** The line chart has `data-category="Average Grant Size ,"`, `data-coords-y="73866, 53804, 42707, 42387, 40381"`, `data-xaxis-cats="FY21,…,FY25,"` and `data-prefix="$"`. Its subtitle reads “Mean value per grant recommended ($ in thousands)”; b52-01 dropped “($ in thousands)”. The values are dollars, not thousands: each is within 0.1% of NPT’s dollars / grants (for example $5.49bn / 129,575 = $42,369). The unit label is NPT’s error and does not change the reading.
- b51-03’s computed FY2024 mean ($42,935) is 1.3% above the published $42,387.

### NPT restatement: governing figure
- **129,575 governs for FY2024 (106,235 for FY2023).** Reasons:
  1. It is NPT’s latest first-party statement of its own history.
  2. The repo uses it with the dollars ($5.49bn) and international counts (406) from the same FY25 report, so switching only the count would mix vintages.
  3. Most repo uses already rely on it: GC-002, b51-03, b51-04, g0401-g0502, the complaint-rate and grant-size CSVs.
  4. The 990 narratives (“more than 129,000”; “approximately 107,000”) fit both series, so they do not decide it.
- **130,875 stays only** as the base of the FY24 report’s own “47% of grants were unrestricted” (b4013-b4428 §2.2 and A-NPT-FY24), where it is the matched denominator. Notes are added to g1913-02, g0401-g0502, b4013-b4428, b51-03 and b52-01. No figure in any repo file needs to change.

### PR Newswire (V52A-16 to -19)
- **GC-016:** “89,485 total grants distributed by Fundholders, a 15% increase over the previous year” (2024-08-22). Confirmed.
- **GC-021:** “more than 123,000 nonprofits worldwide in 2024”, dateline “CHARLESTON, S.C., Oct. 20, 2025”. Confirmed. The date is already recorded in g1913-02 S12.
- **JCF FY2021:** median $501 (2021 Giving Report release, 2022-01-10) and mean $7,194 (2021-10-28; 72,000 grants, $520m, fiscal year ending 2021-06-30). **FY2022:** median $601 (“In FY’ 2022 … 80,500 grants”, 2023-02-07). Confirmed. Mean/median 14.4, close to FY2023’s 15.5.

### NCF (V52A-20 to -23)
- **Sitemaps:** 8 children, 34 + 0 + 453 + 2 + 56 + 22 + 18 + 74 = **659** URLs, all on www. One URL contains “donate”: `/documents/donate-business-interests/`, an asset-giving document, not a fund donate page. Fund donate pages: 0. Confirmed.
- **Quote match 32/35: confirmed, with a bookkeeping note.** b52-01’s own check file labels the 35 spans 30 cited / 3 other page / 2 not found. The doc’s 32 / 2 / 1 follows once RA-11 is credited to its actual cited page (`ncfgiving.com/support`) and the donor-data-export span is matched without its wrapping single quotes. On the live guide every guide-cited span matches except the PL-S10 fragment.
- **donor-info-defaults row 10:** the fund-name quote is on the guide and 0 times on `/giving-fund/`. Confirmed.
- **PL-S10:** the page reads “Examples of what grants can't be used to provide you or someone related to you include: Event tickets or auction purchases Membership dues School tuition Fulfillment of legally binding pledges …”. The repo’s “Grants can't be used to provide you:” fragment is not on the page. Confirmed.

### Every.org (V52A-24)
- robots.txt returned **429** with the “Vercel Security Checkpoint” challenge twice. Still blocked; terms unread.

### Provenance flags (V52A-25)
- The terms-restricted flags in validation-wave48a-report.md (CN) and validation-wave51a-report.md (Vanguard, NPT, PRN) are resolved by the owner decision plus confirmed content. Validation reports are not edited. Resolution notes go to b43n26-03-0304, b51-03, g1913-02, g0401-g0502, b4013-b4428 and FINAL-STATUS.md (“Additional terms-restricted provenance”, the CN bullet, and “Open owner decisions”).
- Still open: A-NPT-FY21 and B-NPT-FY21 (cited page 404), B-NPT-FY20 (no URL), and the DAFgiving360 nonprofitpro slug in b51-03.

## Proposed corrections (§4): decisions

| # | Proposal | Decision | Where and how |
|---|---|---|---|
| C1 | CN provenance flag replaced | **Modify** | Accepted in substance. The wave 48A report is not edited; notes go to b43n26-03-0304 §4 item 6 and three FINAL-STATUS.md bullets |
| C2 | GC-002 note: FY24 report printed 130,875 / 41,879 | **Modify** | CSV not edited; expressed as a note in g1913-02 §3, with the governing-figure reason |
| C3 | A-NPT-FY24 note: 130,875 is the FY24 report’s base | **Modify** | Already in b4013-b4428 §2.2 since wave 39A; one note added there on governing figure and provenance |
| C4 | Exception-share NPT G notes | **Accept** | As a note in g0401-g0502 (consistency checks); CSV not edited |
| C5 | GC-021 dated 2025-10-20 | **Modify** | Date already in g1913-02 S12; folded into the g1913-02 note; CSV not edited |
| C6 | b51-03 §2.2, §3.2, snippet note, §8 B1/B2/B4 | **Modify** | Rows annotated in place rather than moved out of “Not obtained”, so the record of what was blocked survives; §0, §3.2 comparison bullets and §6 limits also updated |
| C7 | Add PS-20+ rows to the grant-size CSV | **Accept** | As md rows B5201-030 to -064 in b51-03 §2.1 (not given PS ids, since the CSV is not edited) |
| C8 | PL-S10 quote | **Accept** | As a note in b41n16-b42n20 after the pledge table |
| C9 | donor-info-defaults row 10 source | **Accept** | As a note on b44n28-01 S19 |
| C10 | Every.org still 429 | **Accept** | b43n26-03-charity-data-terms-ai.md §2.3 and S11 |
| C11 | P-B4222-02-02 stays blocked | **Accept** | Queue CSVs not edited; note in b4222-02-01-01 §2.3 |
| C12 | NCF early reads “within policy” | **Modify** | The decision is dated 2026-11-20 and is not described as retroactive; the note says the pages were re-read under it, not that the earlier reads were within policy |

Also added: a validator note in b52-01 §3.3 (wave 39A precedent, revision ranges, two-way dollar revisions, the “$ in thousands” label).

## Limits

- Sample only: 28 pages and sitemaps. The rows listed under Method as not re-fetched rest on b52-01.
- Static HTML only; script-rendered content was not executed.
- The NCF quote re-check used live copies of the guide and /giving-fund/ only.
- NPT gives no reason for its restatement; the governing-figure choice is a judgement.

## Source register

| # | Source | Date | URL |
|---|---|---|---|
| S1 | CN release: Horizon AI Search | 2025-11-24 | https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search/ |
| S2 | CN release: Allegory | 2026-05-18 | https://www.charitynavigator.org/about-us/press-release/allegory-integrates-cn-api/ |
| S3 | CN release: board | 2025-07-15 | https://www.charitynavigator.org/about-us/press-release/charity-navigator-expands-board/ |
| S4 | CN API terms (redirect target) | Oct 2026 | https://www.charitynavigator.org/products-and-services/api/ → https://www.charitynavigator.org/products-and-services/graphql-api/api-terms-of-use/ |
| S5 | Vanguard Charitable annual reports 2022–2025 | CY2022–25 | https://www.vanguardcharitable.org/2022annualreport ; /2023annualreport ; /2024annualreport ; /2025annualreport |
| S6 | Vanguard Charitable FY23 release | 2023-08-10 | https://www.vanguardcharitable.org/news/vanguard-charitable-FY23-granting-record |
| S7 | NPT FY25, FY24, FY23 annual reports | FY2023–25 | https://www.nptrust.org/annual-reports/npt-annual-report/ ; https://www.nptrust.org/annual-reports/the-2024-annual-report/ ; https://www.nptrust.org/annual-reports/the-2023-annual-report/ |
| S8 | JCF FY2024 release (GC-016) | 2024-08-22 | https://www.prnewswire.com/news-releases/jewish-communal-fund-donors-grant-record-breaking-1-billion-in-fiscal-year-2024-302227664.html |
| S9 | Blackbaud Giving Fund release (GC-021) | 2025-10-20 | https://www.prnewswire.com/news-releases/the-blackbaud-giving-fund-surpasses-550m-in-charitable-giving-in-2024--reaching-2-75b-in-lifetime-giving-302588766.html |
| S10 | JCF 2021 Giving Report release | 2022-01-10 | https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-record-number-of-grants-to-charity-totaling-520-million-in-fy-21-301456454.html |
| S11 | JCF FY2021 grants release | 2021-10-28 | https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-out-520-million-in-grants-in-fy-2021-301409897.html |
| S12 | JCF 50th-anniversary Giving Report release | 2023-02-07 | https://www.prnewswire.com/news-releases/jewish-communal-fund-releases-50th-anniversary-giving-report-301740253.html |
| S13 | NCF sitemap index and 8 child sitemaps | live | https://www.ncfgiving.com/sitemap.xml |
| S14 | NCF guide to giving; Giving Fund page | live | https://www.ncfgiving.com/guide-to-giving-at-NCF ; https://www.ncfgiving.com/giving-fund/ |
| S15 | Every.org robots.txt | 2026-11-20 | https://www.every.org/robots.txt (429, challenge) |

## Exact corrections

31 items in 12 files. Each Find occurs exactly once in its file, both on its own and after the earlier items for that file are applied in order (checked by script). `\n` denotes a newline. No earlier wave’s §11 paragraph is edited; §11.78 is the current last subsection, so the new one is §11.79.

### `research/mission-2026-11-14/b51-03-grant-size-distribution.md`

**Find:** "median grant $1,000, on 2014–2022 transaction data (context only)."
**Replace with:** "median grant $1,000, on 2014–2022 transaction data (context only).<br>- **Vanguard Charitable, average grant** (annual reports, calendar year): $9,500 (2022), $12,412 (2023), $12,926 (2024), $14,808 (2025, 267,838 grants); FY2023 release $10,972. No median or size bands.<br>- **NPT, mean grant** (FY25 report chart): $73,866 (FY21), $53,804, $42,707, $42,387, $40,381 (FY25). No median or size bands.<br>- **JCF:** median $501 and average $7,194 (FY2021); median $601 (FY2022).<br>- These three were read at source on 2026-11-20 under the owner decision lifting the site-terms rule (b52-01; §2.1 rows B5201-030 to -064) [V wave 52A]"

**Find:** "on DAFs](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Report.pdf) |\n\n- **Excluded.** The Fidelity 2021 Giving Report (CY2020 data) was fetched but is not used (pre-2021 data)."
**Replace with:** "on DAFs](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Report.pdf) |\n| B5201-030 | Vanguard Charitable | CY2022 | Average $9,500 | “Total grant dollars given $1.87B Unique organizations supported 52,800 Average grant size $9,500 Total grant units given 196K” | [2022 annual report](https://www.vanguardcharitable.org/2022annualreport) |\n| B5201-031 | Vanguard Charitable | CY2023 | Average $12,412 | “Unique organizations supported 56,744 Average grant size $12,412 Total grant units given 209K” | [2023 annual report](https://www.vanguardcharitable.org/2023annualreport) |\n| B5201-032 | Vanguard Charitable | CY2024 | Average $12,926 | “Total dollars granted $3.1 billion Unique charities supported 62,586 Average grant size $12,926 Total grants issued 240,064” | [2024 annual report](https://www.vanguardcharitable.org/2024annualreport) |\n| B5201-033 | Vanguard Charitable | CY2025 | Average $14,808 | “Total dollars granted $3.96B Unique charities supported 66,785 Average grant size $14,808 Total grants issued 267,838” | [2025 annual report](https://www.vanguardcharitable.org/2025annualreport) |\n| B5201-034 | Vanguard Charitable | FY2023 | Average $10,972 | “The average grant amount was $10,972, a 17% increase over the year prior.” | [FY23 release, 2023-08-10](https://www.vanguardcharitable.org/news/vanguard-charitable-FY23-granting-record) |\n| B5201-035 | Vanguard Charitable | FY2025 | Average ≈$14,000 | “nearly 248,000 grants that averaged approximately $14,000” (b52-01; not re-fetched in wave 52A) | [FY25 release, 2025-08-25](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-deepen-their-impact-driving-another-year-record-granting) |\n| B5201-052 | NPT | FY21–FY25 | Mean $73,866, $53,804, $42,707, $42,387, $40,381 | chart “AVERAGE GRANT SIZE • FY21 – FY25 / Mean value per grant recommended ($ in thousands)”, attribute `data-coords-y`: 73866, 53804, 42707, 42387, 40381; the values are dollars despite the “in thousands” label (they match $ / grants within 0.1%) | [FY25 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/) |\n| B5201-062 | Jewish Communal Fund | FY2021 | Median $501 | “JCF Fundholders make an average of 17 grants per fund per year, with a median grant amount of $501.” | [PR Newswire, 2022-01-10](https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-record-number-of-grants-to-charity-totaling-520-million-in-fy-21-301456454.html) |\n| B5201-063 | Jewish Communal Fund | FY2021 | Average $7,194 | “The average grant amount was $7,194.” (72,000 grants, $520m; mean/median 14.4 [C]) | [PR Newswire, 2021-10-28](https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-out-520-million-in-grants-in-fy-2021-301409897.html) |\n| B5201-064 | Jewish Communal Fund | FY2022 | Median $601 | “JCF Fundholders make an average of 18 grants per fund per year, with a median grant amount of $601.” | [PR Newswire, 2023-02-07](https://www.prnewswire.com/news-releases/jewish-communal-fund-releases-50th-anniversary-giving-report-301740253.html) |\n\n- **Excluded.** The Fidelity 2021 Giving Report (CY2020 data) was fetched but is not used (pre-2021 data).\n- **Rows B5201-030 to B5201-064** come from b52-01 (`terms-lifted-fetch-2026-11-20.csv`), read at source on 2026-11-20 under the owner decision lifting the site-terms rule and re-checked live by wave 52A (except B5201-035). They are not yet `published_stat` rows in `grant-size-distribution-2026-11-20.csv`; Vanguard figures are calendar-year (annual reports) or fiscal-year (releases), and none is a median or a size band. [V wave 52A]"

**Find:** "Not fetched; for the owner to read manually (P-B5103-02)"
**Replace with:** "Not fetched in this pass (P-B5103-02). Fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01): averages only, see §2.1 rows B5201-030 to -035 [V wave 52A]"

**Find:** "Not fetched (P-B5103-02)"
**Replace with:** "Not fetched in this pass (P-B5103-02). Fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01) [V wave 52A]"

**Find:** "GC-002: 129,575 grants FY2024."
**Replace with:** "GC-002: 129,575 grants FY2024 (the FY25 report’s restated count, which governs; the FY24 report printed 130,875) [V wave 52A]"

**Find:** "it was not read at source and is not used"
**Replace with:** "it was not read at source in this pass. Read at source 2026-11-20 (b52-01): $73,866 (FY21) to $40,381 (FY25), §2.1 row B5201-052; the 2024 DAF Report has no grant-size statistic [V wave 52A]"

**Find:** "| PR Newswire releases (JCF FY2021 median $501, etc.)"
**Replace with:** "| PR Newswire releases (JCF FY2021 median $501, etc.). Fetched 2026-11-20 under the owner decision (b52-01): FY2021 median $501 and average $7,194, FY2022 median $601, §2.1 rows B5201-062 to -064 [V wave 52A]"

**Find:** "| NCF, charitynavigator.org | Off-limits under the shared rules"
**Replace with:** "| NCF, charitynavigator.org | Off-limits under the shared rules in this pass. NCF www pages re-read 2026-11-20 (b52-01): no grant-size statistic; Charity Navigator publishes none for sponsors [V wave 52A]"

**Find:** "| $13,782 | $13,524 | blocked"
**Replace with:** "| $13,782 | $13,524 | $12,926 avg (CY2024 annual report; $14,808 CY2025) [V wave 52A]"

**Find:** "| $42,935 | — | blocked"
**Replace with:** "| $42,935 | — | $42,387 mean (FY24, FY25 report chart) [V wave 52A]"

**Find:** "  - JCF: $11,175 (FY2024) against $11,639 (FY2023)."
**Replace with:** "  - JCF: $11,175 (FY2024) against $11,639 (FY2023).\n  - Vanguard (read 2026-11-20, b52-01): $13,782 and $13,524 (FY2024, 990 count 221,825) against $12,926 (CY2024 annual report, 240,064 grants), a 4.6–6.6% gap on different periods and count bases [C].\n  - NPT (read 2026-11-20, b52-01): $42,935 (DAFRC FY2024 dollars / 129,575) against $42,387 (FY25 report chart), a 1.3% gap; NPT’s own $5.49bn / 129,575 = $42,369 [C]. Both sponsors keep their place in the retail vs high-touch ordering. [V wave 52A]"

**Find:** "  - Vanguard and NPT are terms-blocked. Schwab is off-limits."
**Replace with:** "  - Vanguard and NPT were terms-blocked in this pass. Both were read at source on 2026-11-20 under the owner decision (b52-01) and publish averages only, with no median or size bands. Schwab is off-limits. [V wave 52A]"

**Find:** "fetched by an earlier pass and not re-read here (see P-B5103-03)."
**Replace with:** "fetched by an earlier pass and not re-read here (see P-B5103-03). Resolution 2026-11-20: the owner lifted the site-terms rule, and b52-01 re-read the Vanguard, NPT and PR Newswire values at source (GC-002, GC-006, GC-016, GC-021, the 21 sponsor-published-share rows and the 4 exception-share G rows); wave 52A re-fetched a sample and confirmed it. The terms-restricted provenance flag (P-B5103-03; validation-wave51a-report.md) is replaced by “re-fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01; live re-check, wave 52A)”. The DAFgiving360 slug (nonprofitpro) was not re-read. [V wave 52A]"

**Find:** "so **blocked** (terms page read once to establish this)"
**Replace with:** "so **blocked** in this pass (terms page read once to establish this); fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01) [V wave 52A]"

**Find:** "ban robots, spiders and scripts, so **blocked**"
**Replace with:** "ban robots, spiders and scripts, so **blocked** in this pass; fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01) [V wave 52A]"

**Find:** "ban robots, spiders and data mining, so **blocked**"
**Replace with:** "ban robots, spiders and data mining, so **blocked** in this pass; fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01) [V wave 52A]"

### `research/mission-2026-11-14/b43n26-03-0304-pledge-mcp-cn-ai.md`

**Find:** "Keeping, flagging or withdrawing the www quotes is the owner’s decision (validation-wave48a-report.md) [V wave 48A]"
**Replace with:** "Keeping, flagging or withdrawing the www quotes is the owner’s decision (validation-wave48a-report.md) [V wave 48A] Resolution (2026-11-20): the owner lifted the site-terms rule. b52-01 re-read the CN pages, and wave 52A re-fetched the three releases and the API terms: CNAI-01, -02, -03 and -05 match verbatim; the API terms URL redirects to /products-and-services/graphql-api/api-terms-of-use/, reads “Last updated October 2026” and has 0 AI, LLM, machine-learning or training matches; b52-01 reproduced the 18-release screen. The wave 48A flag is replaced by “re-fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01; live re-check, wave 52A)”. The quotes may enter synthesis, and CNAI-01 needs no re-sourcing to Giving Compass. [V wave 52A]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

**Find:** "are listed in validation-wave51a-report.md. They are flagged, not deleted."
**Replace with:** "are listed in validation-wave51a-report.md. They are flagged, not deleted. Resolved 2026-11-20: the owner lifted the site-terms rule; b52-01 re-read these values at source and wave 52A re-fetched a sample (Vanguard, NPT, PR Newswire): all match, so the flag becomes “re-fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01; live re-check, wave 52A)”. NPT’s FY25 report restates FY21–FY24 grant counts about 1% lower; 129,575 governs FY2024 (validation-wave52a-report.md). [V wave 52A]"

**Find:** "  - Four quotes from scripted reads of www.charitynavigator.org, whose terms ban robots, are flagged pending the owner's manual read. They are kept out of synthesis."
**Replace with:** "  - Four quotes from scripted reads of www.charitynavigator.org, whose terms ban robots, were flagged pending the owner's manual read. Resolved 2026-11-20: the owner lifted the site-terms rule, and b52-01 and wave 52A re-fetched them; CNAI-01, -02, -03 and -05 match verbatim, so they may enter synthesis. [V wave 52A]"

**Find:** "  - CN terms-restricted quotes;"
**Replace with:** "  - CN terms-restricted quotes: resolved 2026-11-20 (owner lifted the site-terms rule; re-read verbatim by b52-01 and wave 52A); [V wave 52A]"

### `research/mission-2026-11-14/g1913-02-grant-count-denominators.md`

**Find:** "So Schedule I lines understate grants by about 4 to 33 times. Processor upper bounds built on them (AOGF, PPGF) are correspondingly loose."
**Replace with:** "So Schedule I lines understate grants by about 4 to 33 times. Processor upper bounds built on them (AOGF, PPGF) are correspondingly loose.\n\n**Terms-restricted rows re-read (2026-11-20).** Under the owner decision lifting the site-terms rule, b52-01 re-read rows 2 (NPT 129,575), 4 (Vanguard CY2024 240,064), 14 (JCF 89,485) and P3 (Blackbaud Giving Fund, more than 123,000 nonprofits; release dated 2025-10-20) at source, and wave 52A re-fetched them: all match. NPT’s FY25 report restates its earlier counts about 1% lower without a note; its FY24 report printed 130,875 grants and 41,879 recipients for FY2024. Row 2 keeps 129,575: it is NPT’s latest first-party figure and belongs to the same FY21–FY25 series as the dollars ($5.49bn) and international grants (406) the repo uses with it. [V wave 52A]"

### `research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md`

**Find:** "**Consistency checks [C]**"
**Replace with:** "**Consistency checks [C]**\n- **NPT restatement (wave 52A note).** The 106,235 and 129,575 used here are the FY25 report’s restated values. NPT’s FY23 report printed 107,385 grants and 36,361 recipients for FY2023, and its FY24 report printed 130,875 and 41,879 for FY2024 (b52-01, re-fetched by wave 52A). The restated series governs because the international counts (335, 406) and dollars come from the same FY25 report; the share changes by about 0.003 percentage points either way. [V wave 52A]"

### `research/mission-2026-11-14/b4013-b4428-sponsor-published-grant-stats.md`

**Find:** "| Grants (denominator) | | | 88,289 [R] | | 130,875 | 159,543 |"
**Replace with:** "| Grants (denominator) | | | 88,289 [R] | | 130,875 | 159,543 |\n\n- **Terms-restricted provenance resolved (2026-11-20).** The NPT and Vanguard rows of `sponsor-published-grant-stats-2026-11-19.csv` were re-read at source by b52-01 under the owner decision lifting the site-terms rule, and wave 52A re-fetched the NPT FY23, FY24 and FY25 reports. The 130,875 above is the FY24 report’s own base for its 47% statement; the repo’s governing FY2024 count is the FY25 report’s restated 129,575 (GC-002). A-NPT-FY21 and B-NPT-FY21 remain unverified (the cited page returns 404). [V wave 52A]"

### `research/mission-2026-11-14/b41n16-b42n20-daf-tax-guidance.md`

**Find:** "| Not read | 4 | Goldman Sachs PF [R]; Renaissance [U: site terms; search found no rule]; ImpactAssets [U: circular 403, FAQ 404]; FFTC [U: site terms] |"
**Replace with:** "| Not read | 4 | Goldman Sachs PF [R]; Renaissance [U: site terms; search found no rule]; ImpactAssets [U: circular 403, FAQ 404]; FFTC [U: site terms] |\n\n**NCF quote (wave 52A note).** The NCF guide reads “Examples of what grants can’t be used to provide you or someone related to you include: … Fulfillment of legally binding pledges” (https://www.ncfgiving.com/guide-to-giving-at-NCF, re-read 2026-11-20). PL-S10 in `daf-pledge-policy-2026-11-19.csv` holds an elided paraphrase of this sentence; the substance is confirmed. [V wave 52A]"

### `research/mission-2026-11-14/b44n28-01-donor-info-defaults.md`

**Find:** "| S19 | NCF, Guide to giving | live | https://ncfgiving.com/guide"
**Replace with:** "| S19 | NCF, Guide to giving | live | https://ncfgiving.com/guide. The fund-name quote “This name appears alongside your name and address on correspondence, including the letter that accompanies each grant issued by the fund.” is on https://www.ncfgiving.com/guide-to-giving-at-NCF, not on S20 (/giving-fund/); row 10 of `donor-info-defaults-top20-2026-11-19.csv` should cite the guide (b52-01; re-checked live 2026-11-20) [V wave 52A]"

### `research/mission-2026-11-14/b43n26-03-charity-data-terms-ai.md`

**Find:** "This repeats the 403/429 result of 2026-11-15 ([queue-batch30-everyorg-givinga-goodstack.md](queue-batch30-everyorg-givinga-goodstack.md))."
**Replace with:** "This repeats the 403/429 result of 2026-11-15 ([queue-batch30-everyorg-givinga-goodstack.md](queue-batch30-everyorg-givinga-goodstack.md)). On 2026-11-20 (b52-01, and again in wave 52A) robots.txt still returned 429, now serving a “Vercel Security Checkpoint” JS challenge, so the terms remain unread even after the owner lifted the site-terms rule. [V wave 52A]"

**Find:** "| https://www.every.org/terms | not read (robots 429)"
**Replace with:** "| https://www.every.org/terms | not read (robots 429; still 429 with a Vercel Security Checkpoint challenge on 2026-11-20, b52-01 and wave 52A) [V wave 52A]"

### `research/mission-2026-11-14/b4222-02-01-01-foundant-docs-ncf-donate.md`

**Find:** "NCF's terms bar automated extraction in any case (§2.5)."
**Replace with:** "NCF's terms bar automated extraction in any case (§2.5). Re-check 2026-11-20 after the owner lifted the site-terms rule (b52-01; sitemaps re-fetched in wave 52A): still 659 sitemap URLs, 0 fund donate pages, and no link to one, so P-B4222-02-02 stays blocked as not determinable. [V wave 52A]"

**Find:** "Queue P-B4222-020101-04 proposes manual-only practice for this host."
**Replace with:** "Queue P-B4222-020101-04 proposes manual-only practice for this host. On 2026-11-20 the owner lifted the site-terms rule for such hosts (polite, named-page fetches only); b52-01 re-read the same pages under that decision, so these results no longer rest only on the earlier reads. [V wave 52A]"

### `research/mission-2026-11-14/b52-01-terms-lifted-fetch.md`

**Find:** "Both series are first-party. The repo mixes them (queue P-B5201-01)."
**Replace with:** "Both series are first-party. The repo mixes them (queue P-B5201-01). Validator note: wave 39A had already recorded this restatement (b4013-b4428 §2.2). The count revisions are −0.9% to −1.1%; the dollar revisions run both ways (FY21 $6.41bn → $6.46bn, FY22 $5.57bn → $5.53bn, FY23 $4.50bn → $4.54bn, FY24 $5.62bn → $5.49bn). The repo keeps 129,575 as the governing FY2024 count. The mean-grant chart’s subtitle reads “Mean value per grant recommended ($ in thousands)”, but its values are dollars. [V wave 52A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.79 Terms-lifted re-reads of sponsor and rating-site pages (validated, wave 52A)\n\n**Terms-lifted re-reads of sponsor and rating-site pages** (validated, wave 52A). After the owner lifted the site-terms rule on 2026-11-20, b52-01 re-read the Charity Navigator, Vanguard Charitable, NPT, PR Newswire and NCF pages that earlier studies had skipped or flagged, and a live re-fetch of 28 named pages and sitemaps confirmed every sampled value. Charity Navigator’s four AI quotes match verbatim, and its API terms (“Last updated October 2026”) still contain no AI wording. Vanguard’s annual reports give an average grant of $9,500, $12,412, $12,926 and $14,808 for 2022–2025; NPT’s mean grant fell from $73,866 in FY21 to $40,381 in FY25; JCF’s median grant was $501 in FY2021 and $601 in FY2022. Neither Vanguard nor NPT publishes a median or size bands. NPT’s FY25 report restates its earlier grant counts about 1% lower (FY2024: 129,575 against 130,875), as wave 39A had noted; 129,575 governs in the repo. NCF’s sitemaps still list no fund donate pages, and Every.org remains behind a bot challenge (repo [`validation-wave52a-report.md`](mission-2026-11-14/validation-wave52a-report.md)). [V wave 52A]\n\n---\n\n## Source register"
