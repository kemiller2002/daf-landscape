# Direction P-NEW-NPB-01: what share of nonprofit revenue comes from DAFs? Evidence from public fundraising benchmarks, 2021–2026

**Date:** 2026-11-15 · **Queue item:** P-NEW-NPB-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/nonprofit-daf-revenue-benchmarks-2021-2026.csv`](../../data/mission-2026-11-14/nonprofit-daf-revenue-benchmarks-2021-2026.csv): 102 dated metric rows (NPB001–NPB102). Each row has a source, a metric definition, a value, a period, a segment and an evidence status. Data dictionary in §7.
- [`data/mission-2026-11-14/queue-proposals-batch40-n12.csv`](../../data/mission-2026-11-14/queue-proposals-batch40-n12.csv): P-B40N12-01..03.

**Rules applied**
- **Read first:**
  - [direction-nonprofit-donate-pages.md](direction-nonprofit-donate-pages.md) with its wave-24B corrections. Its donate-page scan of the top 300 DAF recipients gives the comparison point in §3.6: any DAF option 41.2% after the link-choice correction, DAFpay 13.4–13.7%.
  - [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md) with its wave-24A corrections. The recipient universe and the Schedule I line cache are reused only in proposal P-B40N12-02.
  - [queue-all-in-cost-dafpay-access.md](queue-all-in-cost-dafpay-access.md) with its wave-10 and adviser-fee corrections. None of these corrections touches revenue benchmarks.
- **Recency:** only 2021–2026 values are tabulated. Pre-2021 base years (2019, 2020) appear only where a publisher states a change from them, and are marked as context.
- **Polite fetching:**
  - robots.txt was read on every host before any page on it.
  - **mrbenchmarks.com** names `ClaudeBot`, `anthropic-ai` and `Claude-Web` in `Disallow: /` groups. It was **not fetched**, so the 2026 M+R edition is cited through NonProfit PRO and TrueSense.
  - The yearly subdomains (`2025.mrbenchmarks.com` and earlier) return robots 404, meaning no rules. The 2025 PDF was fetched from that subdomain.
  - **ohiocpa.com** carries the same AI-agent block and was not fetched. **candid.org** robots returned 403, so it is unreadable and was not fetched.
  - No crt.sh use.
- **No forms:** the Chariot/K2D report PDFs (2024–2026) and the FreeWill and Bloomerang full reports sit behind HubSpot or download forms. They were **not** requested. Only the openly published pages are used.
- **Evidence labels:**
  - [P] primary page or PDF fetched and read.
  - [S] secondary trade-press page fetched and read.
  - [R] search-index snippet only; the page was not fetched.
  - [D] derived by this note from published numbers.
  - [C] repository computation.
  - [I] inference.

---

## 0. Answers in one table

| Question | Best public evidence (2021–2026) | Status |
|---|---|---|
| **DAF share of total nonprofit revenue** | **Chariot/K2D 2026: "nearly 13%" of $26.1bn total giving** across 54 large nonprofits, 2021–25 pooled ($3.3bn DAF; 12.6% derived) (NPB001–002). **2024 edition: median 12%** of giving in 2023 (20 orgs). 12 of 20 were at ≥10% and 6 of 20 at ≥20% (NPB038–040). **2025 edition: 15%** for participants under $10m revenue in 2024 (NPB024). | [P]/[S]; vendor-run, self-selected samples |
| **DAF share of online revenue** | No benchmark publishes this. **M+R 2025: $0.13 of DAF revenue per $1 raised online** (2024; the DAF revenue is not limited to online gifts). The sector range is $0.01 (Health) to $0.49 (Environmental) (NPB046–053). | [P] PDF |
| **DAF share of major gifts** | **Chariot/K2D 2026: DAFs are >22% of major-gift revenue, but only 2% of DAF gifts are major gifts** (NPB012–013). The threshold is in the gated report. | [P] |
| **DAF gift counts** | Chariot 2026: 907,000 DAF gifts, under 1% of gift count (NPB003–004). Chariot 2025: 417,000 (NPB027). M+R gift-count growth: +11% (2024), +23% (2025) (NPB062, NPB074). FreeWill: >25% of nonprofits receive 50+ DAF gifts a year (NPB079). | [P]/[S] |
| **Average DAF gift seen by nonprofits** | M+R: **$1,430** (2025) (NPB075). Chariot: **$2,751** (2024) (NPB030); $2,995 → $3,934 (2021 → 2025, snippet only) (NPB007–008); $3,638 derived pooled (NPB006). **Median $300** (NPB010). Two-thirds of DAF gifts (69% in the 2025 ed.) are under $1,000 (NPB011, NPB033). | mixed |
| **Trend 2021–2026** | Median DAF revenue +75% vs non-DAF +9% over 2021–25 (Chariot) (NPB014–015). M+R DAF revenue +6% (2024), then **+44% (2025)** (NPB054, NPB073). | [P]/[S] |
| **By size** | Only Chariot 2025 publishes a size cut: under $10m = 15%, the highest band (NPB024). Blackbaud Institute, FEP and M+R publish no DAF-by-size figure. | [P] |
| **By sector** | Chariot 2026: 4–24% of individual revenue by sector, with International Relief highest at 23.7% (NPB019–020). M+R 2025 ($ DAF per online $): Environmental 0.49, Rights 0.29, Public Media 0.16, Hunger 0.09, Wildlife 0.08, Disaster/Intl 0.07, Health 0.01 (NPB047–053). | [P] |
| **Plausibility vs repo totals** | FY2024 netted DAF grants of $58.41bn equal **9.9% of CY2024 Giving USA total giving**, 14.9% of individual giving and 13.3% of individual plus bequest giving (NPB096–098). This fits the vendor samples' ~10–13% (§4). | [D] |

---

## 1. Coverage: which benchmark series say anything about DAFs

| Publisher / series | DAF metric published? | What was used | Access |
|---|---|---|---|
| **Chariot / K2D Strategies, DAF Fundraising Report** (2024: 2019–23 data; 2025: 2020–24; 2026: 2021–25) | **Yes.** It is the only series built from nonprofits' own gift files. | Release pages and webinar summaries; NonProfit Times coverage | Full PDFs gated (HubSpot form); not requested |
| **M+R Benchmarks** | **Yes, from the 2025 edition (2024 data).** DAF figures do not appear in the 2022–2024 editions; text search of those PDFs finds none. | [2025 PDF](https://2025.mrbenchmarks.com/benchmarks2025_files/2025+M%2BR+Benchmarks.pdf), pp. 40–41 and 112–113; [key findings](https://2025.mrbenchmarks.com/key-findings.html) | 2026 edition: web chapter mrbenchmarks.com/fundraising/ read 2026-11-20 [P]; PDF behind reCAPTCHA form; no 2026 DAF-per-online-$ ratio published |
| **FreeWill 2026 DAF Report** | Prevalence and practice survey; no revenue share | [Blog summary](https://www.nonprofits.freewill.com/resources/blog/donor-advised-fund-statistics) | Full report behind a form |
| **Blackbaud Institute** (Charitable Giving Report, donorCentrics, State of Modern Fundraising) | **No DAF revenue share found.** One survey item: 43% of fundraisers saw DAF giving increase. | [2024 survey release](https://www.blackbaud.com/newsroom/article/latest-blackbaud-institute-report-shows-fundraisers-are-optimistic-about-the-future); the [2025 release](https://www.blackbaud.com/newsroom/article/the-state-of-modern-fundraising) mentions DAFs only qualitatively | `/wp-content/uploads/*.pdf` disallowed on blackbaud.com |
| **Fundraising Effectiveness Project** (AFP / GivingTuesday) | **No.** FEP reports dollars, donors and retention by gift band, with no gift-vehicle split. The underlying Growth in Giving data is restricted. | Searched 2025 coverage; [GivingTuesday DAF research page](https://data.givingtuesday.org/dafs) points to restricted DAFRC account data | — |
| **Giving USA** | **Not in the public release.** The DAF analysis sits in the paid report. Public totals are used as denominators. | [GUSA 2025](https://givingusa.org/giving-usa-2025-u-s-charitable-giving-grew-to-592-50-billion-in-2024-lifted-by-stock-market-gains/), [GUSA 2026](https://givingusa.org/giving-usa-charitable-giving-rose-to-617-20-billion-in-2025-surpassing-the-600-billion-mark-for-the-first-time/) | Report paywalled |
| **Bloomerang** (Giving Signals 2026) | Intent only: 64% of nonprofits prioritise DAFs or other tax-advantaged giving | [Blog](https://bloomerang.com/blog/smooth-giving-big-impact-easy-optimizations-from-the-2026-giving-signals-report) | — |
| **Bonterra / Network for Good, Neon One, Givebutter, Classy/GoFundMe Pro "Why America Gives"** | **None found** in 2021–2026 public material. Bonterra's 2026 Impact Report covers repeat giving; Neon One covers recurring giving; the only WAG hit is the 2021 edition, with no DAF figure. | Searches only | — |

**[I]** Public, nonprofit-side DAF revenue benchmarks come from two series: Chariot/K2D, a DAF payments vendor, and M+R, since 2025. The large CRM-data publishers (Blackbaud, FEP, Bonterra, Neon One) do not split revenue by gift vehicle in public output. This is consistent with the finding in [FreeWill's survey](https://www.nonprofits.freewill.com/resources/blog/donor-advised-fund-statistics) that only 33% of nonprofits flag DAF donors in their CRM (NPB081).

---

## 2. Dated metrics table (headline rows; full set in the CSV)

| ID | Publisher, edition | Metric (definition) | Value | Period | Status |
|---|---|---|---|---|---|
| NPB001 | Chariot/K2D 2026 | DAF revenue / total giving, 54 orgs pooled | nearly 13% | 2021–25 | [P] [webinar page](https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release) |
| NPB003 | Chariot/K2D 2026 | DAF gifts / all gifts | <1% | 2021–25 | [P] same |
| NPB004–005 | Chariot/K2D 2026 | DAF gifts; DAF revenue | 907,000; $3.3bn | 2021–25 | [P] same |
| NPB010 | Chariot/K2D 2026 | Median DAF gift (presenter quote) | $300 | 2025 | [P] same |
| NPB012–013 | Chariot/K2D 2026 | DAF share of major-gift revenue; major gifts as share of DAF gifts | >22%; 2% | 2021–25 | [P] [report page](https://www.givechariot.com/resources/toolkits/daf-fundraising-report) |
| NPB014–015 | Chariot/K2D 2026 | Median revenue growth, DAF vs non-DAF | +75% vs +9% | 2021→25 | [P] same |
| NPB019–021 | Chariot/K2D 2026 | Intl Relief DAF share of total revenue; sector range (of individual revenue); Health share growth | 23.7%; 4–24%; +99.4% | 2025; period | [P] same |
| NPB007–008 | Chariot/K2D 2026 via Candid | Average DAF gift | $2,995 → $3,934 | 2021 → 2025 | [S] [Candid](https://candid.org/blogs/daf-fundraising-report-nonprofit-takeaways/) (fetched 2026-11-20; dated 2026-06-08) |
| NPB024–025 | Chariot/K2D 2025 | DAF share of revenue, orgs < $10m; change since 2020 | 15%; +143% | 2024 | [P] [Chariot summary](https://www.givechariot.com/resources/insights/inside-the-2025-daf-fundraising-report-how-donor-advised-funds-are-transforming-philanthropy) |
| NPB027–028, 030 | Chariot/K2D 2025 | DAF transactions; DAF $; average DAF gift (non-DAF $105) | 417,000; $1.15bn; $2,751 | 2020–24; 2024 | [S] [NonProfit Times](https://thenonprofittimes.com/npt_articles/study-size-of-daf-donations-outpacing-other-avenues-of-giving/) |
| NPB033–034 | Chariot/K2D 2025 | DAF gifts < $1,000; median DAF revenue growth (non-DAF −1%) | 69%; +30% | 2024 | [P] Chariot summary |
| NPB038–041 | Chariot/K2D 2024 | Median DAF share; orgs ≥10%; orgs ≥20%; total DAF $ | 12%; 12/20; 6/20; $192m | 2023 | [S] [NonProfit Times](https://thenonprofittimes.com/npt_articles/daf-donors-making-their-presence-felt/) |
| NPB046 | M+R 2025 | DAF revenue per $1 online revenue | $0.13 | 2024 | [P] [PDF p.40](https://2025.mrbenchmarks.com/benchmarks2025_files/2025+M%2BR+Benchmarks.pdf) |
| NPB054, 062 | M+R 2025 | DAF revenue change; DAF gift-count change | +6%; +11% | 2023→24 | [P] PDF p.41 |
| NPB070 | M+R 2025 | Nonprofits offering DAF as a payment type on main donation page | 30% | 2024 | [P] PDF p.113 |
| NPB073–075 | M+R 2026 | DAF revenue change; gift-count change; average DAF gift | +44%; +23%; $1,430 | 2025 | [P] [M+R fundraising chapter](https://mrbenchmarks.com/fundraising/); also [S] [NonProfit PRO](https://www.nonprofitpro.com/article/mr-benchmarks-2026-what-online-giving-growth-means-for-your-donor-file/), [TrueSense](https://www.truesense.com/blog/what-the-2026-mr-benchmarks-reveal-about-nonprofit-fundraising) |
| NPB077–079 | FreeWill 2026 | Nonprofits receiving DAFs; with more DAF $ than 2024 (2% declined); receiving 50+ DAF gifts | 79%; 61%; >25% | 2025 | [P] [FreeWill blog](https://www.nonprofits.freewill.com/resources/blog/donor-advised-fund-statistics) |
| NPB083 | Blackbaud Institute 2024 | Fundraisers reporting DAF giving increased (n = 215; early tech adopters 58%) | 43% | FY to mid-2024 | [P] [Blackbaud release](https://www.blackbaud.com/newsroom/article/latest-blackbaud-institute-report-shows-fundraisers-are-optimistic-about-the-future) |

---

## 3. Findings

### 3.1 Share of total revenue: about one-eighth at DAF-active national charities
- **Pooled (2026 ed.):** $3.3bn DAF of $26.1bn total giving, which is 12.6% (NPB002). Gift count is under 1%.
- **Median (2024 ed., 2023):** 12%. The dispersion is wide: 6 of 20 organisations were at ≥20% (NPB038–040).
- **Derived (2025 ed.):** $1.15bn / $12bn = 9.6% (NPB029, [D], low confidence). The NonProfit Times gives the DAF total and Chariot gives the revenue total, so the period basis may differ.
- **Selection bias, against the market:**
  - Participants are national direct-response charities chosen for data completeness. Named 2024 participants include ACS, Komen, March of Dimes and ACLU. March of Dimes, ACLU and IRC appear as DAFpay case studies, and Chariot's release names ACS as a DAFpay customer.
  - **[I]** These are upper-half DAF users, not a random sample. The repo's donate-page scan found DAFpay on 13% of the top-300 DAF recipients' donate pages, so the Chariot panel over-represents DAFpay adopters.

### 3.2 Share of online revenue: no benchmark; M+R's ratio is the closest
- M+R reports **DAF revenue divided by online revenue**, not DAF online revenue. The ratio covers only participants that reported DAF revenue (NPB046).
- Using M+R's own direct-mail ratio ($0.78 per online $), DAF would be about **6.8%** of online + mail + DAF revenue (NPB072, [D]). This is illustrative only: the subsets differ, and major gifts, events and grants are excluded.
- **[I]** M+R's panel is digital and direct-response, so it captures smaller and more online-adjacent DAF gifts. That fits its lower average gift ($1,430 vs Chariot's $2,751–3,934).

### 3.3 Major gifts
- DAFs supply **>22% of major-gift revenue** while being only 2% of DAF gifts (NPB012–013).
- Case evidence points the same way:
  - The Public Theater: 25% of $5k+ campaign gifts came via DAF ([Chariot 2025 summary](https://www.givechariot.com/resources/insights/inside-the-2025-daf-fundraising-report-how-donor-advised-funds-are-transforming-philanthropy)).
  - ACLU: 40% of midlevel donors give through DAFs (NPB023).
- No non-vendor source gives a DAF share of major gifts.

### 3.4 Counts and gift size
| Source | Mean DAF gift | Median | Note |
|---|---|---|---|
| M+R 2026 | $1,430 (2025) | — | Digital panel; "remained steady" |
| Chariot 2025 | $2,751 (2024); $1,157 excl. > $25k [R] | 12× non-DAF median | Pooled $1.15bn / 417k = $2,758 |
| Chariot 2026 | $3,934 (2025) [R]; $3,638 pooled [D] | $300 | 23× non-DAF average |
| Fidelity Charitable (sponsor side, context) | $5,801 (CY2025, outliers removed) | — | repo `donor-behaviour-metrics-2021-2026.csv` DB061 |

- **[I]** The averages differ because of who is measured:
  - Nonprofit-side means sit at 25–70% of Fidelity's sponsor-side mean grant.
  - The largest DAF grants go to universities, hospitals, foundations and other sponsors. Those recipients are absent from these fundraising panels.
- The median is about $300, and two-thirds of DAF gifts are under $1,000. DAF gifts are mid-level rather than major on a count basis.

### 3.5 Trend, 2021–2026
- **Chariot (medians across organisations):**
  - +30% DAF revenue in 2024, against −1% non-DAF (NPB034).
  - +75% over 2021–25, against +9% non-DAF (NPB014–015).
- **M+R (pooled):** +6% in 2024 (+11% gifts), then +44% in 2025 (+23% gifts).
- **FreeWill:** 61% of nonprofits took in more DAF dollars in 2025 and only 2% saw a decline.
- **Repo comparison:**
  - Netted DAF grants rose 37.4% from FY2021 to FY2024 (NPB101).
  - FY2024 was +15.0% netted, against M+R's +6% for CY2024.
  - **[I]** The gap reflects fiscal-year timing (June-FYE sponsors), DAF-to-DAF flows already removed, and grants to non-panel recipients.
- The 2025 surge (+44%) postdates the repo's latest complete grant year (FY2024), so it cannot yet be checked against netted Schedule D totals.

### 3.6 Size and sector variation
- **Size:**
  - The only published size cut is Chariot 2025. Organisations under $10m had the highest DAF share (15%), up 143% since 2020 (NPB024–025).
  - There is no figure for large organisations, and no independent size cut.
  - **[I]** The under-$10m participants are survivors selected into a DAF-focused study, so this should not be read as "small charities get more DAF revenue".
- **Sector:** International Relief is highest in Chariot (23.7% of total revenue). M+R shows Environmental and Rights highest per online dollar, and Health lowest ($0.01).
  - **[I]** Health ranks low in M+R but grows fastest in Chariot (+99.4% share growth). This may reflect different panels: M+R's Health participants are measured against online revenue, and Chariot's Health participants are not named publicly.
- **Payment option:** 30% of M+R participants list DAF as a payment type on the main donation page (2024). The repo's top-300 DAF-recipient scan found 41.2% with any DAF option and 13.7% with DAFpay. These are different populations: the scan covers the charities receiving the most DAF dollars.

---

## 4. Reconciliation with the repository's DAF grant totals

Inputs:
- Repo FY2024 DAF grants: DAFRC $64.60bn; corrected $66.44bn; **netted (R5 central) $58.41bn**, range $57.02–59.49bn ([`dafrc-market-totals-netted.csv`](../../data/mission-2026-11-14/dafrc-market-totals-netted.csv); DAF-INDUSTRY-REPORT §1 and §11.14).
- Giving USA CY2024: total $592.50bn, individuals $392.45bn, bequests $45.84bn ([GUSA 2025](https://givingusa.org/giving-usa-2025-u-s-charitable-giving-grew-to-592-50-billion-in-2024-lifted-by-stock-market-gains/)).

| Ratio | Value | Row |
|---|---|---|
| Netted DAF grants / GUSA total | **9.86%** (9.62–10.04) | NPB096 |
| Netted / individual giving | 14.88% (14.53–15.16) | NPB097 |
| Netted / individual + bequest | 13.33% (13.01–13.57) | NPB098 |
| Corrected (un-netted) / GUSA total | 11.21% | NPB099 |
| DAFRC published / individual giving | 16.46% (Chariot's Dec-2025 reframing: "17%") | NPB100 |

**Reading:**
- **[D]/[I] Plausible and consistent.** A market-wide ratio of about 10% of total giving (13–15% of individual and bequest giving) matches the nonprofit-side benchmarks:
  - the Chariot pooled share of 12.6%;
  - the 2023 median of 12%;
  - FreeWill's framing that DAFs are "12% to 13% of all charitable giving".

  The vendor panels sit slightly above the market ratio, as expected from their selection of DAF-active nationals.
- **Using un-netted figures overstates DAF's role.** DAFRC's published $64.6bn implies 16.5% of individual giving. About 1.6 points of that is sponsor-to-sponsor transfer that never reaches an operating charity (§11.14). Benchmarks citing "17% of individual giving" inherit that inflation.
- **The ratios are not true shares:**
  - Giving USA's recipient estimates already include DAF grants received, and its source estimates count DAF contributions when made.
  - The ratio compares a fiscal-year grant total with a calendar-year giving total.
  - The GUSA "public-society benefit" line ($66.84bn) is smaller than netted DAF contributions ($84.74bn). Some DAF contributions must therefore sit under other GUSA recipient lines (for example "to foundations" for community foundations, or religion). The two series cannot be mapped line by line from public data.
- **Scale check:** the Chariot 2026 panel's $3.3bn (2021–25 pooled) is roughly 1% of the five-year netted grant flow. These benchmarks describe a small, DAF-forward slice of recipients.
- **AOGF reclassification (§11.16):** it cuts FY2024 grants by only about 1.2%, which does not change the ratios materially.

---

## 5. Limitations
- **Vendor provenance.** The only nonprofit-file series is produced by a DAF payments company and an agency client of DAF-forward charities. Definitions are not public: how DAF gifts are identified, the major-gift threshold, and whether totals are annual or pooled.
- **Gated detail.** Sector exhibits, size bands and year-by-year averages are in form-gated PDFs and were not obtained (P-B40N12-01).
- **Snippet values.** NPB007–009 and NPB031 come from search-index snippets of pages this agent could not fetch under robots rules. One snippet's non-DAF averages ($21→$25) conflict with the published 23× ratio, so those rows are flagged.
- **M+R 2026** is cited only through trade press, because the publisher's robots.txt blocks Claude agents.
- **No independent nonprofit-side denominator.** Form 990 does not separate DAF grants received. The repo's Schedule I recipient lines could produce one (P-B40N12-02).

## 6. Source register
| # | Source | URL | Read | Status / robots |
|---|---|---|---|---|
| S1 | Chariot, DAF Fundraising Report 2026 page (.md) | https://www.givechariot.com/resources/toolkits/daf-fundraising-report | 2026-11-15 | [P]; allowed (`/admin/*` only); PDF behind HubSpot form, not requested |
| S2 | Chariot, 2026 report release webinar (.md) | https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release | 2026-11-15 | [P] |
| S3 | Chariot, Inside the 2025 DAF Fundraising Report (.md) | https://www.givechariot.com/resources/insights/inside-the-2025-daf-fundraising-report-how-donor-advised-funds-are-transforming-philanthropy | 2026-11-15 | [P] |
| S4 | Chariot, 2024 report press release (.md) | https://www.givechariot.com/resources/insights/donor-advised-funds-increase-annual-giving-by-96-reveals-new-chariot-k2d-strategies-five-year-stud | 2026-11-15 | [P] |
| S5 | NonProfit Times, 2024-07-24 | https://thenonprofittimes.com/npt_articles/daf-donors-making-their-presence-felt/ | 2026-11-15 | [S]; robots has no `*` rules |
| S6 | NonProfit Times, 2025-06-27 | https://thenonprofittimes.com/npt_articles/study-size-of-daf-donations-outpacing-other-avenues-of-giving/ | 2026-11-15 | [S] |
| S7 | M+R Benchmarks 2025 PDF (69 pp., created 2025-06-05) and key findings | https://2025.mrbenchmarks.com/benchmarks2025_files/2025+M%2BR+Benchmarks.pdf ; https://2025.mrbenchmarks.com/key-findings.html | 2026-11-15 | [P]; subdomain robots 404 |
| S8 | M+R Benchmarks 2022–2024 PDFs (no DAF content found) | https://2024.mrbenchmarks.com/benchmarks2024_files/2024_Benchmarks_Study.pdf (and 2023, 2022 equivalents) | 2026-11-15 | [P]; subdomain robots 404 |
| S9 | NonProfit PRO on M+R 2026 (2026-04-23) | https://www.nonprofitpro.com/article/mr-benchmarks-2026-what-online-giving-growth-means-for-your-donor-file/ | 2026-11-15 | [S]; allowed |
| S10 | TrueSense on M+R 2026 | https://www.truesense.com/blog/what-the-2026-mr-benchmarks-reveal-about-nonprofit-fundraising | 2026-11-15 | [S]; only PDFs disallowed |
| S11 | FreeWill, Decoding DAFs (2026 report summary) | https://www.nonprofits.freewill.com/resources/blog/donor-advised-fund-statistics | 2026-11-15 | [P]; `*` allowed |
| S12 | Blackbaud newsroom, 2024 Institute survey (2024-07-16); 2025 State of Modern Fundraising | https://www.blackbaud.com/newsroom/article/latest-blackbaud-institute-report-shows-fundraisers-are-optimistic-about-the-future ; https://www.blackbaud.com/newsroom/article/the-state-of-modern-fundraising | 2026-11-15 | [P]; PDF uploads disallowed, none fetched |
| S13 | Bloomerang Giving Signals 2026 blog and landing page | https://bloomerang.com/blog/smooth-giving-big-impact-easy-optimizations-from-the-2026-giving-signals-report ; https://bloomerang.com/resources/giving-signals-report-2026 | 2026-11-15 | [P] |
| S14 | Giving USA 2025 and 2026 releases | https://givingusa.org/giving-usa-2025-u-s-charitable-giving-grew-to-592-50-billion-in-2024-lifted-by-stock-market-gains/ ; https://givingusa.org/giving-usa-charitable-giving-rose-to-617-20-billion-in-2025-surpassing-the-600-billion-mark-for-the-first-time/ | 2026-11-15 | [P]; cart and admin paths only disallowed |
| S15 | GivingTuesday Data Commons DAF page | https://data.givingtuesday.org/dafs | 2026-11-15 | fetched (404 body); allowed |
| S16 | Candid blogs on 2024 and 2026 Chariot reports | https://candid.org/blogs/daf-fundraising-report-nonprofit-takeaways/ ; https://candid.org/blogs/5-takeaways-2024-daf-donors-fundraising-report/ | — | [R] only; robots 403, not fetched |
| S17 | Ohio CPA on the 2025 Chariot report | https://ohiocpa.com/for-the-public/news/2025/07/25/5-takeaways-on-2024-trends-in-daf-giving | — | [R] only; robots blocks ClaudeBot/Claude-Web |
| S18 | mrbenchmarks.com (2026 edition) | https://mrbenchmarks.com/fundraising/ | — | not fetched; robots blocks ClaudeBot, anthropic-ai, Claude-Web |
| R1 | Repo netted totals | `data/mission-2026-11-14/dafrc-market-totals-netted.csv` | — | [C] |
| R2 | Repo sponsor grant metrics | `data/mission-2026-11-14/donor-behaviour-metrics-2021-2026.csv` (DB054, DB061) | — | [P] via repo |

## 7. Data dictionary: `nonprofit-daf-revenue-benchmarks-2021-2026.csv`
| Column | Meaning |
|---|---|
| metric_id | NPB001–NPB102 |
| category | `share_total_revenue`, `share_individual_revenue`, `share_major_gifts`, `share_gift_count`, `ratio_to_online`, `share_channels`, `gift_count`, `gift_count_growth`, `dollar_volume`, `avg_gift`, `median_gift`, `gift_size_mix`, `growth`, `retention`, `conversion`, `donor_value`, `donor_count`, `prevalence`, `practice`, `case_study`, `denominator`, `repo_total`, `reconciliation`, `sponsor_context` |
| publisher, report_edition | Who published it, and which edition |
| metric | Short name |
| definition | Numerator / denominator, or how the value is built, as far as the public source states it |
| value | As published. Ranges and ratios are kept as text (e.g. `4-24`, `2105 -> 2510`, `>22`) |
| unit | percent, percentage points, USD, gifts, x (multiple), USD per online USD, share |
| period | Data period (CY = calendar year; FY = sponsor fiscal year; "pooled" = multi-year total) |
| segment | `all`, `sector: …`, `size: …`, `org: …`, `US total`, `US DAF market` |
| sample | Panel description and size |
| published | Publication date of the source page or edition |
| evidence_status | [P] / [S] / [R] / [D] / [C] (see Rules) |
| source_url | Primary URL, or the repository path for [C] |
| notes | Caveats, page numbers, related values |
| retrieved | 2026-11-15 |

## 8. Reproduction
- **Robots:** each host's `/robots.txt` was fetched with curl and parsed for the `*` group and for named Claude agents before any page on the host.
- **Chariot pages:** the `.md` variants (`<page>.md`) were read.
- **M+R PDFs:** downloaded from the yearly subdomains and converted with `pdftotext -layout`. The DAF figures are on report pp. 40–41 (DAF chart spread) and 112–113 (payment types) of the 2025 edition.
- **CSV:** built by a short stdlib script from the values above. Derived rows show their arithmetic in the `definition` column, and the reconciliation inputs are cited by row.

## Validation corrections (wave 25B, 2026-11-15) — governing
Source: [validation-wave25b-report.md](validation-wave25b-report.md); register `data/mission-2026-11-14/validation-register-wave25b.csv`.

1. **Rules applied, robots.**
   - **Find:** "**candid.org** robots returned 403, so it is unreadable and was not fetched."
   - **Replace with:** "**candid.org** robots returned 403 in this run. On 2026-11-15 it returns 200 and names ClaudeBot and anthropic-ai under `Disallow: /`, so it is still not fetched [V wave 25B]."
2. **§5 Limitations, snippet values.**
   - **Find:** "One snippet's non-DAF averages ($21→$25) conflict with the published 23× ratio, so those rows are flagged."
   - **Replace with:** "One snippet's non-DAF averages ($21→$25) conflict with the published 23× ratio, so those rows are flagged. A 23× ratio at $3,934 implies a non-DAF mean of about $171. The 2025 edition's median ratio of \"12 times\" fits $300 / $25 exactly, so the $21 and $25 values are probably non-DAF medians. They should not be used as averages [V wave 25B]."
3. **§0, plausibility row.**
   - **Find:** "This fits the vendor samples' ~10–13% (§4). | [D] |"
   - **Replace with:** "This fits the vendor samples' ~10–13% (§4). | [D]; recomputed from Giving USA 2025 totals ($592.50bn, $392.45bn, $45.84bn) [V wave 25B] |"
