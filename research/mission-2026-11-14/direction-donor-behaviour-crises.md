# Direction P-NEW-DON-01: DAF donor demographics, grant behaviour, timing and crisis response (2021–2026)

**Date:** 2026-11-15 · **Queue item:** P-NEW-DON-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/donor-behaviour-metrics-2021-2026.csv`](../../data/mission-2026-11-14/donor-behaviour-metrics-2021-2026.csv): 184 rows, one dated metric per row (§6).
- [`data/mission-2026-11-14/queue-proposals-batch39-n7.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n7.csv): P-B39N7-01..03.

**Rules applied**
- **Read first:** [DAF-INDUSTRY-REPORT-2026-11.md §1](../DAF-INDUSTRY-REPORT-2026-11.md) (market totals, account-count caveats, corrected FY2024 mean account $97,680); [queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md) (Fidelity Giving Report PDFs S5, Vanguard releases S6); [quantitative-datasets-and-data-dictionary.md](quantitative-datasets-and-data-dictionary.md) (DAFgiving360 FY2026 row). None of the governing corrections there changes any figure used here. The DAFRC and NPT account-size values come from the repo series [`daf-market-annual-series.csv`](../../data/mission-2026-11-14/daf-market-annual-series.csv). DAFRC was not re-fetched.
- **Recency:** every value covers 2021 or later.
- **robots.txt** was read on each host before fetching (§7). Three hosts could not be read and were **not fetched**: dafgiving360.org (403), businesswire.com (403) and dafresearchcollaborative.org (its robots.txt names Claude-family user-agents). DAFgiving360 values therefore come from reprints and search snippets, labelled **[S]**. No outreach, logins or forms.
- **Labels:**
  - **[P]**: sponsor's or publisher's own document. Self-reported and unaudited.
  - **[S]**: secondary reprint or search snippet.
  - **[C]**: computed here.
  - **[I]**: inference.
  - **[U]**: not found.
- **Never invented:** where a sponsor publishes nothing, the gap is stated (§4.3, §8).

---

## 0. Answers in brief

| Theme | Finding | Confidence |
|---|---|---|
| **Demographics** | **No sponsor publishes donor age or gender.** The only figure for DAF holders is from BofA's 2026 survey: **9%** of wealthy individuals (≥$3m investable) use a DAF, versus **20%** of Gen Z and Millennials aged 21–45 ([BofA 2026](https://www.privatebank.bankofamerica.com/articles/study-of-wealthy-americans-philanthropy.html)).<br>**Account size is mostly small:** Fidelity's median balance was **$24,086 → $19,442 → $21,267 → $23,534 → $27,860** (2021–25), with **48–56%** of accounts under $25k ([2022](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2022-giving-report.pdf)–[2026](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) Giving Reports).<br>**Industry *means* are $70k–$183k** depending on publisher and year. They are not comparable to a median. | Medium (sizes); Low (age) |
| **Grant behaviour** | **Typical grant:**<br>- **Fidelity** average **$4,407 → $5,801** (2021–25, outliers removed), about **12.3** grants per account a year, **88–91%** of accounts active;<br>- **DAFgiving360** median **$500** [S];<br>- **Daffy** median **$100**;<br>- **Vanguard** average **≈$14,000** (FY2025);<br>- **Charityvest** derived average **$772 → $2,445** [C].<br>**Recurring:** about **one-third** of grants are prescheduled at Fidelity (27% → 32%), **38–40%** at DAFgiving360 [S] and **>45%** at Daffy. Vanguard's "69% recurring" uses a different definition (§5).<br>**Loyalty:** **75–80%** of grants go to charities the donor has funded before (Fidelity 75–80%; DAFgiving360 85% [S]). | High (Fidelity); Medium (others) |
| **Timing** | **December share:**<br>- **Vanguard:** about **22%** of CY2024 grants by count were made in December; Nov–Dec 2025 was **$953m**, "more than a quarter" of the year;<br>- **Daffy:** December 2025 contributions of **>$200m** were about **43%** of the year's >$470m [C].<br>**GivingTuesday 2025 (single day):**<br>- **Fidelity:** 48,000 grants, >$129m (about 0.7% of annual dollars) [C];<br>- **DAFgiving360:** >24,000 grants, $80m [S].<br>**Markets:**<br>- **2022 drawdown:** grants *rose* (Fidelity +9%, Vanguard +5%). Balances fell: Fidelity's median −19%, and its cumulative investment growth fell from $21bn to $15bn.<br>- **2025:** grants rose (Fidelity +23%, Vanguard +27%). Fidelity attributes part of the rise to bunching ahead of the 2026 tax law. | Medium |
| **Crisis response** | **Ukraine 2022:**<br>- Fidelity **>$128m** in H1;<br>- Vanguard **>$70m**, mostly 28 Feb–8 Apr.<br>**Helene/Milton 2024:**<br>- Fidelity **~$50m**;<br>- Vanguard **$11.2m** for hurricanes (FY2025).<br>**LA wildfires 2025:** Vanguard **$10m** for wildfires (FY2025). No Fidelity number was published.<br>**Disaster totals:**<br>- DAFgiving360 **>$148m** (FY2025) and **>$200m** (CY2025) [S];<br>- Vanguard **$67.5–70m** (2023) and **$110m** (FY2025).<br>**Türkiye/Syria 2023, Maui 2023 and Gaza 2023–24:** **no national-sponsor dollar figure is published [U].** Receipt-side figures exist instead: HCF received **$62m** in incoming DAF grants in 2023; JCF NY's grants to Israeli charities rose **35% to $148m** in FY2024. | Medium (Ukraine, hurricanes); Low (others) |

Reading **[I]**:
- Crisis surges are visible mainly as *counts of supporting accounts* and *rank jumps*, for example UNICEF USA +14 places in 2022 and No One Left Behind +2,367% more supporting accounts in 2021. Dollar surges are small next to annual flows. Fidelity's $128m for Ukraine is about 2.7% of its H1 2022 grants [C], and its $50m for Helene/Milton is about 0.3% of its 2024 grants [C].
- Rank jumps revert within a year: the 2022 Ukraine responders fell 5–7 places in 2023.

---

## 1. Donor demographics

### 1.1 Fidelity Charitable, the only multi-year first-party panel [P]

Values are at 31 Dec of each year. Sources are the Giving Reports for [2022](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2022-giving-report.pdf), [2023](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf), [2024](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf), [2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) and [2026](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf).

| Year | Donors¹ | Funded DAFs | Median balance | <$25k | $25k–250k | >$250k |
|---|---|---|---|---|---|---|
| 2021 | 286,849 | 174,592 | $24,086 | 51% | 38% | 11% |
| 2022 | 303,781 | 185,640 | **$19,442** | **56%** | 35% | 9% |
| 2023 | 322,139 | 197,834 | $21,267 | 53% | 37% | 10% |
| 2024 | 352,052 | 217,402 | $23,534 | 51% | 38% | 11% |
| 2025 | 395,515 | 246,006 | **$27,860** | **48%** | 40% | 12% |

¹ "Donors" here counts all account holders, including secondary holders and corporate contacts. Elsewhere in the reports "donor" means the primary holder (methodology pages).

- **New-account trend:** the number of DAFs grew **+13.4%** in 2025 by the report text. The table in the same report says +13.1%, and the arithmetic gives +13.2% [C]. The report attributes this partly to donors "bunching donations in the face of tax law changes that took effect in 2026" ([2026 report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf)). Average yearly growth over 2021–24 was about 7.6% [C].
- **Wealth spread:** about half of accounts hold under $25k, while 9–12% hold over $250k. The mean is far above the median: the industry means in §1.2 are about 3–8 times Fidelity's median for the same year [C].

### 1.2 Industry mean account size [P; repo series]

| FY | NPT DAF Report | DAFRC 2025 Updated memo |
|---|---|---|
| 2021 | $182,842 ([2022 report](https://www.nptrust.org/2022-daf-report/)) | $123,862 |
| 2022 | $117,466 ([2023 report](https://www.nptrust.org/2023-daf-report/)) | $70,459 |
| 2023 | $141,120 ([2024 report](https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/)) | $84,578 |
| 2024 | — (NPT handed the series to DAFRC) | $91,300 ([memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)); the repo-corrected value is **$97,680** |

The two series differ because DAFRC counts donation-processor accounts: 79.5% of 3.59m FY2024 accounts hold 0.9% of assets ([industry report §1](../DAF-INDUSTRY-REPORT-2026-11.md)). Neither series gives a median.

### 1.3 Newer sponsors [P]

- **Daffy:**
  - >15,700 accounts at end-2025, and "over 16,000" in Jan 2026;
  - median incoming DAF transfer about $10,000 ([Year in Review 2025](https://www.daffy.org/resources/year-in-review-2025), unaudited).
- **Charityvest:** accounts grew **14,128 → 15,963 → 18,496 → 20,656** (2022–25). Average contribution per active donor was ">$100K" in 2025, driven by wealth-manager partnerships ([2022](https://www.charityvest.org/annual-report-2022), [2023](https://www.charityvest.org/annual-report-2023), [2024](https://www.charityvest.org/annual-report-2024), [2025](https://www.charityvest.org/annual-report-2025)).

### 1.4 Age, generation and women

- **BofA 2026 Study of Wealthy Americans** (1,431 respondents with ≥$3m investable assets, age 21+, ±2.5 points; [article 2026-09-29](https://www.privatebank.bankofamerica.com/articles/study-of-wealthy-americans-philanthropy.html)) [P]:
  - **9%** use a DAF; **20%** of Gen Z and Millennials do;
  - **21%** of DAF users contributed more than $100k in the past year;
  - 75% of users expect to increase contributions; 28% of non-users are likely to open a DAF within three years.
- **BofA 2025 Study of Philanthropy** (1,514 affluent households; [page](https://www.privatebank.bankofamerica.com/articles/bank-of-america-study-of-philanthropy.html)) [P]:
  - **18%** of 2024 gifts went through giving vehicles, up from 11% nine years earlier;
  - **81%** of affluent households gave, down from 85% in 2022;
  - a DAF-only share is not on the public page; a 10% share appears in secondary press only [S].
- **Vanguard Charitable / Harris Poll, Oct 2023** (2,073 US adults; general population, not DAF holders; [release](https://www.vanguardcharitable.org/news/new-survey-3-5-millennial-and-gen-z-donors-plan-give-more-charity-next-12-months)) [P]:
  - 60% of Millennial and Gen Z donors expected to give more, against 40% of Gen X and 39% of Boomers;
  - 54% of Millennials and 53% of Gen Z gave to disaster relief.
- **Women:** Fidelity's [2021 Women and Giving](https://www.fidelitycharitable.org/insights/2021-women-and-giving.html) page gives attitudes only: 86% of women wish they could do more, and 14% have spoken to an advisor about charitable planning against one in five men. It has **no DAF-holder gender statistic [U].**

---

## 2. Grant behaviour

### 2.1 Fidelity Charitable [P]

| Year | Grants | Dollars | Avg grant² | Grants/acct | Active accts | Distinct charities | $1m+ grants | Scheduled / regrant / new |
|---|---|---|---|---|---|---|---|---|
| 2021 | 2,171,636 | $10.3bn | $4,407 | 12.4 | 91% | 187,328 | 1,180 | 27 / 48 / 25 |
| 2022 | 2,185,516 | $11.20bn | $4,798 | 11.8 | 88% | 188,777 | 1,407 | 31 / 46 / 23 |
| 2023 | ">2.3m" | $11.8bn | $4,625 | 11.8 | 88% | ~199,000 | 1,345 | 31 / 47 / 22 |
| 2024 | 2,664,446 | $14.9bn | $5,422 | 12.3 | 88% | 213,476 | 1,971 | 31 / 46 / 23 |
| 2025 | ~3.0m | $18.3bn | $5,801 | 12.28 | n/p | 226,823 | 2,141 | 32 / 45 / 23 |

² Outliers are removed from the average each year, and the excluded amount varies:
- one grant over $500m (2021 and 2022);
- four grants totalling more than $970m (2023);
- one $430m grant (2024);
- $727m of grants (2025).

The averages therefore move partly with what is excluded.

Further facts from the same reports:
- About 64% of grants are designated "where needed most".
- 95–96% carry the donor's or account's name.
- 54.3% of 2025 grants by count went to the donor's home state (38% of dollars).
- 42% of each contributed $100 is granted within one year and 73% within five, on a first-in, first-out basis (2025).
- Corporate DAFs (556 in 2025) average **$20,732** a grant.

### 2.2 Other sponsors

| Sponsor | Period | Size statistic | Recurring | Other | Source |
|---|---|---|---|---|---|
| DAFgiving360 | FY2025 (Jul–Jun) | n/p | 38% | $8.9bn; 1.4m grants; 155k charities; 85% to previously supported | [FWR reprint](https://www.familywealthreport.com/printarticle.php?id=205183); [Chariot](https://givechariot.com/resources/insights/breaking-down-the-dafgiving360-fy25-annual-report) [S] |
| DAFgiving360 | CY2025 | **median $500** | 38% | $9.9bn; ~1.5m grants; >165k charities | [Pulse 2.0 reprint](https://pulse2.com/dafgiving360-donors-grant-nearly-10-billion-to-charities-in-most-active-year-on-record/) [S] |
| DAFgiving360 | FY2026 | median $500 | 40% | >$10bn (+22%); >170k charities, >30k of them new; homepage snippet $10.85bn / 1.69m grants | [release](https://www.dafgiving360.org/press-release/fiscal-year-2026-results) (search text only) [S] |
| Vanguard Charitable | FY2025 | **mean ≈$14,000** | "69% of annual grants are recurring" | ~248k grants; >$3.5bn; 62,950 nonprofits | [release 2025-08-25](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-deepen-their-impact-driving-another-year-record-granting) [P] |
| Vanguard Charitable | CY2022–25 | n/p | n/p | $1.87bn / 196k grants (2022); $2.6bn / 209k (2023); $3.1bn (2024); $3.9bn, ~67k nonprofits (2025) | releases [2023-01-25](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-set-new-granting-record-despite-economic-challenges), [2024-01-30](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-granted-2-billion-2023), [2025-02-04](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-eighth-record-granting-year), [2026-03-02](https://www.vanguardcharitable.org/news/vanguard-charitable-2025-record-granting) [P] |
| Daffy | CY2025 | **median $100** | >45% of donations | >$125m granted; payout "more than 37%" of end-2024 assets | [Year in Review](https://www.daffy.org/resources/year-in-review-2025) [P] |
| Charityvest | CY2022–25 | derived mean $772 / $994 / $1,328 / $2,445 [C] | n/p | 25,659 → 48,744 grants; 5,875 → 9,412 charities | annual reports [2022](https://www.charityvest.org/annual-report-2022)–[2025](https://www.charityvest.org/annual-report-2025) [P] |

- **Daffy payout correction:** an editor's note dated 2026-07-28 corrected the payout claim from 55% to "more than 37%". Chariot's [55% summary](https://givechariot.com/resources/insights/daffy-is-now-a-top-10-daf--and-we-couldnt-be-more-excited) is superseded.
- **Charityvest payout method change:** the payout rate was 54–58% "Foundation Center method" in 2022–24 and **118%** in 2025, with no method stated. The years are not comparable.

---

## 3. Timing

| Metric | Value | Source |
|---|---|---|
| Vanguard: share of grants by count made 1 Jan–30 Nov 2024 | **78%**, so about **22%** in December [C]. The release text says "nearly three-quarters" | [2025-02-04](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-eighth-record-granting-year) [P] |
| Vanguard: giving season, 1 Nov–31 Dec 2025 | **$953m**, "more than a quarter" of 2025 grants. Against $3.9bn that is 24.4% [C]; the gap is unreconciled rounding. +130% over five years | [2026-03-02](https://www.vanguardcharitable.org/news/vanguard-charitable-2025-record-granting) [P] |
| Daffy: December 2025 contributions | **>$200m**, against about $194m for all of 2024 and >$470m for 2025 (about 43% [C]) | [Year in Review](https://www.daffy.org/resources/year-in-review-2025) [P] |
| Fidelity: GivingTuesday 2025 | **48,000 grants, >$129m in one day** | [2026 report p.13](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) [P] |
| DAFgiving360: GivingTuesday 2024 | 22,000 grants, >$69m | [FWR reprint of FY2025 release](https://www.familywealthreport.com/printarticle.php?id=205183) [S] |
| DAFgiving360: GivingTuesday 2025 | >24,000 grants, $80m to >15,000 charities. The release says "+37% YoY", but against >$69m the rise is about +16% [C]; unreconciled | [Pulse 2.0 reprint](https://pulse2.com/dafgiving360-donors-grant-nearly-10-billion-to-charities-in-most-active-year-on-record/) [S] |

### Market response

- **2022 drawdown (S&P 500 down about 20%):**
  - **Grants rose at both sponsors.** Fidelity granted $4.8bn in H1 2022, +11% on H1 2021 ([release 2022-07-20](https://www.fidelitycharitable.org/about-us/news/fidelity-charitable-donors-recommended-4-8-billion-in-first-half-of-2022.html)); the full year was $11.2bn, +9%. Vanguard's CY2022 grants rose 5%.
  - **Balances fell.** Fidelity's median account fell **−19%** ($24,086 → $19,442) and accounts under $25k rose from 51% to 56%. Cumulative investment growth fell from **$21bn to $15bn**.
  - **Non-cash giving held:** 57% of contributions were non-cash.
  - **Industry contributions declined** in FY2022–23 ([industry report §1](../DAF-INDUSTRY-REPORT-2026-11.md)).
- **2025 (April drawdown, then a strong year and the OBBBA tax change):**
  - Vanguard's grants rose 30% year on year in H1 2025.
  - Full-year grants rose at Fidelity (+23%, accounts +13.4%) and Vanguard (+27%).
  - Fidelity's cumulative investment growth reached $41.1bn.
  - Giving USA attributes the 4.1% rise in individual giving to "a strong stock market" ([Giving USA 2026](https://givingusa.org/giving-usa-charitable-giving-rose-to-617-20-billion-in-2025-surpassing-the-600-billion-mark-for-the-first-time/)).
- **Reading [I]:** grants respond to market moves with a lag and are cushioned by balances already contributed. Contributions and balances absorb the shock.

---

## 4. Crisis responsiveness, 2021+

### 4.1 Sponsor statements with numbers

| Event | Sponsor | Figure | Source |
|---|---|---|---|
| Afghan refugees, Haiti earthquake, Hurricane Ida (2021) | Fidelity | Change in supporting accounts: No One Left Behind **+2,367%**, Women for Afghan Women +1,917%, Hope for Haiti +865%, Greater New Orleans Foundation +418% | [2022 report pp.16–17](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2022-giving-report.pdf) [P] |
| Ukraine (2022) | Fidelity | **>$128m** earmarked in H1 2022; International Medical Corps supporting DAFs more than ten times H1 2021; WCK more than five times. In the 2022 ranking: UNICEF USA +14 places, CARE +77, Save the Children +25, WCK +23 (to #3) | [release](https://www.fidelitycharitable.org/about-us/news/fidelity-charitable-donors-recommended-4-8-billion-in-first-half-of-2022.html); [2023 report p.13](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf) [P] |
| Ukraine (2022) | Vanguard | **>$70m**, mostly 28 Feb–8 Apr 2022; grant count in that window +45% on a year earlier | [2023-01-25](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-set-new-granting-record-despite-economic-challenges) [P] |
| 2023 disasters (Türkiye/Syria, Maui and others) | Vanguard | $67.5m in 10,578 grants over the 12 months to about Oct 2023; >$70m in CY2023 to >1,000 nonprofits; **no split by event** | [2023-11-16](https://www.vanguardcharitable.org/news/new-survey-americans-increasingly-support-disaster-relief-major-share-charitable-giving); [2024-01-30](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-granted-2-billion-2023) [P] |
| Ukraine surge reverting (2023) | Fidelity | UNICEF USA −7, IRC −7, WCK −5, Samaritan's Purse −5 places; "a return to more typical levels". No 2023 dollar figures for Türkiye, Maui or Gaza | [2024 report p.12](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf) [P] |
| Helene / Milton (2024) | Fidelity | **~$50m** ("nearly $50 million" in the summary; "$50 million" on p.11) | [2025 report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) [P] |
| Hurricanes and wildfires (FY2025) | Vanguard | $110m in about 13,000 disaster grants to 1,800 nonprofits, including **$11.2m** for hurricanes and **$10m** for wildfires. The release says "California and Texas" and does not name LA | [2025-08-25](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-deepen-their-impact-driving-another-year-record-granting) [P] |
| All disasters | DAFgiving360 | **>$148m** in FY2025 (including >$4m for the July 2025 Texas floods); **>$200m in about 56,000 grants in CY2025 (+16%)** | [FWR](https://www.familywealthreport.com/printarticle.php?id=205183); [Pulse 2.0](https://pulse2.com/dafgiving360-donors-grant-nearly-10-billion-to-charities-in-most-active-year-on-record/) [S] |

### 4.2 Receipt side: community foundations and faith-based sponsors

- **Hawai'i Community Foundation (2023):** >250,000 incoming DAF grants worth >$62m, nearly 25% of HCF's grants. The Maui Strong Fund received nearly $32m in DAF grants ([NPT blog 2024-08-13](https://www.nptrust.org/philanthropic-resources/philanthropist/finding-help-and-healing-in-the-wake-of-tragedy-with-hawaii-community-foundation/), citing HCF) [S].
- **Jewish Communal Fund NY (FY2024):** grants to Israeli charities reached **$148m, +35%**. UJA-Federation NY received nearly $50m through >1,400 grants (+87% in dollars) ([release 2024-08-22](https://prnewswire.com/news-releases/jewish-communal-fund-donors-grant-record-breaking-1-billion-in-fiscal-year-2024-302227664.html)) [P]. JCF's cumulative figure of ">$53m in >5,000 grants" for emergency relief comes from search text only; jcfny.org returned 403.
- **Community Foundation of Henderson County, NC (Helene):** $1.4m distributed, of which $950k went to 44 nonprofits; the remainder (about $450k [C]) went through DAFs ([Hendersonville Lightning](https://www.hendersonvillelightning.com/news/14934-community-foundation-has-given-1-4-million-in-helene-grants.html)) [S].

### 4.3 Not found [U]

- No national sponsor published a dollar figure for **Türkiye/Syria 2023**, **Maui 2023** or **Gaza 2023–24**, or for the **LA wildfires** by name.
- Fidelity's and Vanguard's guidance pages for these events carry no figures: Vanguard [Israel/Gaza](https://www.vanguardcharitable.org/news/disaster-relief-israel-gaza-strip), [Helene](https://www.vanguardcharitable.org/news/hurricane-helene) and [California wildfires](https://www.vanguardcharitable.org/news/california-wildfires-disaster-relief); Fidelity's [2025 California fires page](https://www.fidelitycharitable.org/guidance/disaster-relief/how-to-help-2025-california-fires.html).
- CAF America's Türkiye figures are not on the fetched page, so they are not used.

---

## 5. Definitional differences across sponsors (read before comparing)

| Concept | Fidelity | DAFgiving360 | Vanguard | Daffy | Charityvest | DAFRC / NPT |
|---|---|---|---|---|---|---|
| **Period** | Calendar year | FY ending 30 Jun **and** a CY release | FY ending 30 Jun **and** a CY release | Calendar year | Calendar year | Sponsors' Form 990 FY ending in the labelled year |
| **Grant size** | **Mean**, outliers removed ($430m–$970m excluded a year) | **Median** | **Mean**, no stated outlier rule | **Median** | Not published; mean derived here [C] | Not published |
| **"Recurring"** | "Prescheduled" share of grant count (27–32%); separate "regrant" category (45–48%) | Share of grants "set up as recurring" (38–40%) | "69% of annual grants are recurring": undefined, apparently repeat grants manual or automatic (24% automatic / 76% manual over 10 years, per secondary [S]) | Share of donations recurring (>45%) | n/p | n/p |
| **Donor / account** | Funded accounts at year-end; "donors" counts all holders | n/p | n/p | Unique accounts | Total accounts | Sponsor-reported accounts. DAFRC includes processors; NPT mostly excludes them |
| **Balance** | **Median** account | n/p | n/p | n/p | AUM only | **Mean** account |
| **Payout** | 1-, 5- and 10-year FIFO of contributions | n/p | n/p | Grants over prior year-end assets (37%, corrected) | 54–58% "Foundation Center" in 2022–24; 118% in 2025, method unstated | Grants over beginning assets |
| **Disaster totals** | Per event (Helene/Milton) | All-disaster total for FY and CY | All-disaster total per FY or trailing 12 months, with hurricane and wildfire subtotals | n/p | n/p | n/p |

Consequences:
- **Vanguard's $14k mean against DAFgiving360's $500 median does *not* show that Vanguard donors give 28 times more.** A mean is pulled up by large grants and a median is not.
- **Fidelity's FY and CY figures do not mix with DAFgiving360's or Vanguard's.** DAFgiving360 and Vanguard publish both bases, so always match the period basis.

---

## 6. Data dictionary: `donor-behaviour-metrics-2021-2026.csv`

| Column | Meaning |
|---|---|
| `metric_id` | `DB001`… stable row id |
| `sponsor_or_publisher` | Sponsor, publisher or survey owner |
| `category` | `demographics`, `grant_behaviour`, `timing`, `market_response` or `crisis` |
| `metric` | Plain-language metric name. Includes the definition qualifier, such as "(outliers removed)" or "(derived)" |
| `value` | Number as published. Some cells hold text, such as ">10x", a rank string or a payout with its method. USD in units, not millions |
| `unit` | Unit. "(lower bound)" marks "more than" or "over" wording; "(approx.)" marks "nearly" or "about" |
| `period` | Period the value covers (CY, FY with months, H1, single day, event window or survey fieldwork) |
| `period_basis` | calendar year / fiscal year ending June / single day / survey / cumulative and so on |
| `published` | Publication date of the source (YYYY, YYYY-MM or YYYY-MM-DD) |
| `evidence_label` | [P] / [S] / [C] as defined above |
| `source_url` | Primary URL. Where the primary host was unreadable, the reprint URL |
| `definition_note` | Outlier rules, comparability warnings and internal inconsistencies |
| `retrieved` | 2026-11-15 |

Row counts by category: grant_behaviour 95, demographics 50, crisis 21, timing 9, market_response 9. By evidence: [P] 160, [S] 20, [C] 4 (Charityvest derived means). Other derived values appear in notes, marked [C]. Recount with `python3 -c "import csv,collections;print(collections.Counter(r['category'] for r in csv.DictReader(open('data/mission-2026-11-14/donor-behaviour-metrics-2021-2026.csv'))))"`.

---

## 7. Source register

| # | Source | Host robots.txt | Fetched | Used in |
|---|---|---|---|---|
| S1 | Fidelity Charitable Giving Reports 2022–2026 (PDF), as linked above; pdftotext. PDF creation dates: 2022-02-14, 2024-04-15 (2023 report re-export), 2024-03-06, 2025-02-19, 2026-04-21 | fidelitycharitable.org: only /retired/, /sample-email/, /nuance/ and /vessel/ disallowed | 2026-11-15 | §1–4 |
| S2 | Fidelity H1 2022 release; 2021 Women and Giving page; 2023-11-28 year-end survey release; OBBB guidance page; 2026 Impact Snapshot PDF (no new figures) | same | 2026-11-15 | §3–4, §1.4 |
| S3 | Vanguard Charitable news pages (CY2022–25 and FY2024–25 results; disaster pages; Harris surveys of 2023-11-16 and 2023-11-29) | vanguardcharitable.org: only /core/, /profiles/ and READMEs disallowed | 2026-11-15 | §2–4 |
| S4 | DAFgiving360 via reprints: [Pulse 2.0](https://pulse2.com/dafgiving360-donors-grant-nearly-10-billion-to-charities-in-most-active-year-on-record/) (CY2025), [Family Wealth Report](https://www.familywealthreport.com/printarticle.php?id=205183) (FY2025; the page's date of "2 July 2026" conflicts with the 2025-07-29 release), [Chariot](https://givechariot.com/resources/insights/breaking-down-the-dafgiving360-fy25-annual-report); FY2026 from search text | dafgiving360.org 403 and businesswire.com 403, so not fetched; pulse2, familywealthreport and givechariot allow | 2026-11-15 | §2–4 |
| S5 | [Daffy Year in Review 2025](https://www.daffy.org/resources/year-in-review-2025) (last updated 2026-07-29; editor's note 2026-07-28); Chariot summary (superseded payout) | daffy.org: /resources allowed | 2026-11-15 | §1–3 |
| S6 | Charityvest annual reports 2022–2025 (embedded page JSON) | charityvest.org: Allow / | 2026-11-15 | §1–2 |
| S7 | BofA 2025 Study of Philanthropy and 2026 Study of Wealthy Americans (HTML only; robots.txt disallows *.pdf) | privatebank.bankofamerica.com | 2026-11-15 | §1.4 |
| S8 | [Giving USA 2026 release](https://givingusa.org/giving-usa-charitable-giving-rose-to-617-20-billion-in-2025-surpassing-the-600-billion-mark-for-the-first-time/) | givingusa.org: admin and cart paths disallowed | 2026-11-15 | §3 |
| S9 | NPT blog on HCF; JCF FY2024 release (PR Newswire); Hendersonville Lightning (search text) | nptrust.org: Disallow empty for *; prnewswire: templates only; hendersonvillelightning: /stats/ and /administrator/ | 2026-11-15 | §4.2 |
| S10 | Repo: [`daf-market-annual-series.csv`](../../data/mission-2026-11-14/daf-market-annual-series.csv) (NPT and DAFRC account sizes); [industry report §1](../DAF-INDUSTRY-REPORT-2026-11.md) | — | repo | §1.2 |
| S11 | Not fetched: dafresearchcollaborative.org (robots.txt names Claude-family agents); jcfny.org (403); milkeninstitute LA-fires PDF (404 at the searched URL); cafamerica.org page (no Türkiye content) | — | — | §4.3 |

---

## 8. Gaps and limits

- **Self-reported:** all sponsor figures are unaudited marketing or annual-report numbers. Only market totals tie to Form 990 (industry report §1).
- **Comparability:** no sponsor publishes age or gender, monthly grant dollars, grant-size bands beyond Fidelity's $1m+ count, or a recurring definition that matches another sponsor's.
- **Crisis splits:** disaster totals are not split by event except Fidelity's Helene/Milton figure and Vanguard's hurricane and wildfire subtotals.
- **Follow-ups:** proposed in [`queue-proposals-batch39-n7.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n7.csv):
  - P-B39N7-01: first-party DAFgiving360 values;
  - P-B39N7-02: a cross-sponsor seasonality series;
  - P-B39N7-03: DAF-holder demographics.

## Validation corrections (wave 24B, 2026-11-15) — governing
Source: [validation-wave24b-report.md](validation-wave24b-report.md); register `data/mission-2026-11-14/validation-register-wave24b.csv`.

1. **Rules applied, robots.**
   - **Find:** "and dafresearchcollaborative.org (its robots.txt names Claude-family user-agents)."
   - **Replace with:** "and dafresearchcollaborative.org (not fetched in this run). Its robots.txt lists ClaudeBot and anthropic-ai in the same group as `User-agent: *`, so `/s/` documents are allowed. The DAFRC values here still come from the repo series [V wave 24B]."
2. **§2.2, Daffy payout correction.**
   - **Find:** "an editor's note dated 2026-07-28 corrected the payout claim from 55% to \"more than 37%\"."
   - **Replace with:** "an editor's note dated 2026-07-28 says an earlier version \"misstated the donation payout rate\". The text now says \"more than 37 cents of every dollar held in Daffy funds at the end of 2024 was distributed to charity in 2025\". The earlier figure appears as 55% in Chariot's summary; the note itself does not state it [V wave 24B]."
3. **§7, S11.**
   - **Find:** "dafresearchcollaborative.org (robots.txt names Claude-family agents)"
   - **Replace with:** "dafresearchcollaborative.org (not fetched; its robots.txt gives Claude agents the same rules as `*`, which allow `/s/` [V wave 24B])"
