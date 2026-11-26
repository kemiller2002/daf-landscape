# b51-03: The size distribution of DAF grants: Schedule I lines (top-50 sponsors, FY2021–FY2024), published grant-size statistics, and what they mean for processing workload

*Prepared 2026-11-20. TASKID b51-03. Nothing here is committed. No existing file was modified.*

**Outputs**
- [`scripts/mission_grant_size_distribution.py`](../../scripts/mission_grant_size_distribution.py): stdlib only, functional style. It imports the universe, return picker, line loader, DAF-to-DAF whitelist logic and totals-row filter of earlier scripts unchanged (`mission_daf_to_daf`, `mission_recipient_sectors`, `mission_net_payout`, `mission_exception_load`).
- [`data/mission-2026-11-14/grant-size-distribution-2026-11-20.csv`](../../data/mission-2026-11-14/grant-size-distribution-2026-11-20.csv): 728 rows. The data dictionary is in §7. Two consecutive runs from cache gave the same file (md5 `a2d1008d50878684cdf476593b4cc38b`).
- [`data/mission-2026-11-14/queue-proposals-b51-03.csv`](../../data/mission-2026-11-14/queue-proposals-b51-03.csv): six proposals.

**Run**
```
S=<scratchpad>
python3 scripts/mission_grant_size_distribution.py . --np-cache $S/npcache --lines-cache $S/b5103/lines \
  --read-cache $S/rcp/lines --read-cache $S/q120201/lines --read-cache $S/q2102/lines \
  --read-cache $S/v42b/w1/lines --read-cache $S/q2661/lines --xml-list $S/b5103_allxml.txt [--fetch]
```

**Labels:** **[F]** quoted from a first-party document fetched 2026-11-20. **[C]** computed by the script (a CSV row is named). **[R]** carried from another repo file and not re-read. **[I]** inference.

> **A Schedule I line is not a grant.** Form 990 Schedule I Part II has one line per recipient per return. The line is the **sum of every grant the filer paid that recipient in the tax year**, and a recipient is itemised only when that sum is **more than $5,000**. Every line-size figure in §1 and §3 is therefore a distribution of *recipient-year totals*. It overstates grant size, and it leaves out every recipient that received $5,000 or less in the year. §3.2 measures how far apart the two units are.

---

## 0. Answer

| Question | Finding |
|---|---|
| **Line-size distribution** (top-50 itemising sponsors, 182 sponsor-years, 1,102,439 lines with a positive amount, $167.6bn, FY2021–24 pooled) [C] | - **Under $10k:** 22.6% of lines, 1.0% of dollars.<br>- **$10k–$100k:** 62.7% of lines, 11.6% of dollars.<br>- **$100k–$1m:** 12.8% of lines, 21.3% of dollars.<br>- **$1m–$10m:** 1.7% of lines, 27.7% of dollars.<br>- **$10m or more:** 0.17% of lines (1,903), 38.3% of dollars.<br>- Median line: $18,650. Mean line: $152,053. |
| **Mega-line dollar share and its trend** [C] | - **Lines of $1m or more:** 1.9% of lines and **66.0% of dollars** pooled. By year: 68.3% (FY2021), 65.7%, 65.0%, 65.5% (FY2024).<br>- **Lines of $10m or more:** 0.17% of lines and **38.3% of dollars**. By year: 42.6%, 37.6%, 37.2%, 36.7%.<br>- Without DAF-to-DAF lines: 60.8% ($1m+) and 30.4% ($10m+) pooled. The $10m+ share falls from 34.0% to 27.1%.<br>- Fixed panel of 44 sponsors itemising in all four years: $1m+ 68.3% → 66.1%; $10m+ 42.6% → 37.3%.<br>- **No upward trend in concentration.** The count of $1m+ lines rose from 4,309 to 6,292 (nominal dollars), but their dollar share stayed at 65–68%. The $10m+ share drifted down, mostly because of a few very large FY2021 lines. |
| **By sponsor type** (FY2021–24, all lines) [C] | - **National sponsors** (16): median line $17,450; 86.7% of lines under $100k; $1m+ = 65.1% of dollars; $10m+ = 38.5%.<br>- **Community foundations** (22): median $23,400; 80.1% under $100k; $1m+ = 70.1%; $10m+ = 38.7%.<br>- **Single-issue sponsors** (7): median $21,000; 82.5% under $100k; $1m+ = 56.6%; $10m+ = 22.8%.<br>- **University/hospital** (Stanford, UCLA Foundation) and the **one processor in the top 50** (Dechomai Asset Trust) have only a few hundred and 34 lines respectively. Their Schedule I is mostly not DAF grantmaking (affiliate transfers; Dechomai's pass-through to its sister foundation), so they are reported but not interpreted. |
| **Published grant-size statistics, 2021+** [F] | - **Fidelity Charitable, average grant:** $4,407 (2021), $4,798 (2022), $4,625 (2023), $5,422 (2024), $5,801 (2025), each with outliers removed.<br>- **Fidelity, grants of $1m or more:** 1,180, 1,407, 1,345, 1,971, 2,141.<br>- **Morgan Stanley GIFT:** "$11,000 Average Grant Size" (2024).<br>- **Jewish Communal Fund (FY2023):** median grant $750; average $11,639. Of 77,364 grants, 75,380 were under $50,000, 1,908 were $50,000–$1 million and 76 were over $1 million.<br>- **DAFRC National Study (2024):** median grant $1,000, on 2014–2022 transaction data (context only).<br>- **Vanguard Charitable, average grant** (annual reports, calendar year): $9,500 (2022), $12,412 (2023), $12,926 (2024), $14,808 (2025, 267,838 grants); FY2023 release $10,972. No median or size bands.<br>- **NPT, mean grant** (FY25 report chart): $73,866 (FY21), $53,804, $42,707, $42,387, $40,381 (FY25). No median or size bands.<br>- **JCF:** median $501 and average $7,194 (FY2021); median $601 (FY2022).<br>- These three were read at source on 2026-11-20 under the owner decision lifting the site-terms rule (b52-01; §2.1 rows B5201-030 to -064) [V wave 52A] |
| **Average grant = DAF grants / stated count** (12 sponsors) [C] | - Using DAFRC FY2024 DAF grants: **$4.5k (RCF), $4.8k (Fidelity), $6.0k (DAFgiving360)**; $11k–15k (JCF, MS GIFT, Vanguard, AEF, ImpactAssets); $31k (FFTC); **$43k (NPT)**; $92k (GS); $211k (SVCF, count covers all SVCF grants).<br>- Using the dollars stated in the same source as the count: Fidelity $5,592 (**$5,431 after removing the $430m outlier, against the published $5,422**); MS GIFT $10,656 (published $11,000); JCF $11,175 (published FY2023 average $11,639). |
| **Average vs median, and line vs grant** [C/F] | - **Mean grant is about 15 times the median** at the one sponsor that publishes both (JCF: $11,639 / $750).<br>- **The median Schedule I line ($17k–$25k at the nationals) is 20–30 times the published median grant ($750; $1,000 in the DAFRC sample).**<br>- **Grants per line average 7–33** at the sponsors with counts (Fidelity 33, DAFgiving360 20, JCF 19, Vanguard 9, NPT 7). The ratio divides grants to all recipients, itemised or not, by itemised lines. Per recipient it is lower: Fidelity’s 2,664,446 CY2024 grants went to 213,000 unique nonprofits (12.5 each; 2025 Giving Report), and JCF’s 77,364 FY2023 grants to more than 10,600 charities (about 7.3). [V wave 51A] |
| **What a line is at each end** [C/F] | - **Top end: about one $1m+ grant per $1m+ line** (how many smaller grants share the line is not observed). [V wave 51A] Fidelity's lines of $1m or more (1,183, 1,280, 1,295, 1,708 in FY2021–24) track its published grants of $1m or more (1,180, 1,407, 1,345, 1,971 in CY2021–24): **a ratio of 1.00–1.15 grants per line**, with a half-year period offset.<br>- **Bottom end: one line bundles many grants.** In JCF's same fiscal year (FY2023), 2,955 lines under $50k stand for 75,380 grants under $50k (**25.5 grants per line**). JCF reports grants to more than 10,600 charities against 4,340 itemised lines, so about 6,260 recipients of $5,000 or less share those grants: about 8 grants per small recipient. [V wave 51A] 1,276 lines of $50k–$1m stand for 1,908 grants (1.5 per line). 109 lines over $1m stand for 76 grants over $1m (0.7 per line). |
| **Workload implication** [I] | Grant *count* drives processing work, and dollars drive risk and value. They sit at opposite ends of the distribution:<br>- **About 97% of grants are under $50k** (JCF).<br>- **Grants of $1m or more are 0.07–0.10% of grants** (Fidelity 1,971 of 2,664,446; JCF 76 of 77,364), yet **lines of $1m or more carry about two-thirds of itemised dollars**.<br>- So per-grant automation is a small-grant problem, while dollar-weighted risk review is a mega-grant problem.<br>- The evidence also cuts against high values of the β grant-size rule used in the per-grant exception work (§5). |

---

## 1. Method

### 1.1 Filings (Schedule I)
1. **Universe.** This is unchanged from P-NEW-REC-01 and P-GAP19-05: the top-50 DAFRC sponsors by FY2024 end-of-year DAF assets ([`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)), with one return per sponsor × DAFRC fiscal year (`mission_daf_to_daf.pick_returns` over the `netpayout990/` cache). The years are extended here to **FY2021–FY2024**, giving 200 sponsor-years in scope.
2. **Exclusions.** 18 sponsor-years are dropped because Schedule I points to an attachment instead of itemising (`mission_net_payout.itemized` is False). They are listed in the CSV as `excluded_return`:
   - BofA Charitable Gift Fund (FY2021–24);
   - Renaissance Charitable Foundation (FY2021–24);
   - Greater Kansas City CF (FY2021–23);
   - Greater Horizons (FY2021–23);
   - New York Community Trust (FY2021–22);
   - US Charitable Gift Trust (FY2021–22).

   That leaves **182 itemising sponsor-years**: 44 in FY2021 and FY2022, 46 in FY2023 and 48 in FY2024.
3. **Lines.**
   - All RecipientTable lines (`[ein, name, where, irc, cash, noncash]`) were taken from the existing full-line caches of `mission_recipient_sectors.py`, which cover the 94 FY2023–24 returns. They were read only, never rewritten.
   - For FY2021–22, lines came from a local e-file XML copy whose line count matched netpayout990's `sched_i_lines` (58 returns). The other 30 returns came from the GivingTuesday mirror of IRS TEOS, `gt990datalake-rawdata.s3.amazonaws.com` (robots.txt 404, so no rules apply; UA `research-script/1.0 (stdlib urllib)`).
   - All 182 parses gave status `ok`, meaning the line count equals the count in the cache.
   - E-filed totals rows are dropped with `mission_exception_load.drop_totals_rows` (the Greater Horizons FY2024 pattern).
4. **Amount and bins.**
   - Amount = cash + non-cash.
   - Bins: <$10k, $10k to <$100k, $100k to <$1m, $1m to <$10m, ≥$10m.
   - Three lines with a zero or negative amount are counted in `lines_nonpositive` and left out of the bins.
   - 29,796 positive lines are $5,000 or less (`lines_le_5k`; some filers itemise below the threshold). They fall in the <$10k bin.
5. **Bases.**
   - `all_lines`.
   - `excl_d2d`: lines to a sponsor EIN marked `include` in [`daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv), plus self-lines, are removed (same rule as P-NEW-RCP-01).
6. **Scopes.**
   - all top-50;
   - a fixed panel (the 44 sponsors itemising in all four years);
   - all top-50 excluding SVCF (a sensitivity check for its very large FY2023 lines);
   - the five DAFRC segments;
   - each sponsor-year (`sponsor_year` rows).
7. **No DAF weighting.** Community-foundation and university Schedule I lines include non-DAF grants. Bin shares are not reweighted by DAF share, because a sponsor-level weight would not change within-sponsor bin shares, and the line-level fund type is unknown.

### 1.2 Sponsor reports
- **Search.** Web search was used only to find URLs.
- **Gate.** Before any fetch, each host's robots.txt was read with the repo's hard rule applied (a ClaudeBot / anthropic-ai / Claude-* group counts; 403 or unreachable counts as disallowed), and the site's terms of use were checked for bans on automated extraction (§8).
- **Extraction.** PDFs were read with `pdftotext` in layout and raw modes.
- **Quote check.** A check in the scratchpad confirmed that all 19 quotes in `PUBLISHED` occur verbatim in the fetched text, after whitespace normalisation. `[...]` and `[chart]` mark elisions between layout fragments.

### 1.3 Combine
- **Counts.** Primary stated counts come from [`grant-count-denominators-2026-11-20.csv`](../../data/mission-2026-11-14/grant-count-denominators-2026-11-20.csv) (`is_primary = 1`, 12 sponsors).
- **Two averages:**
  - `avg_grant_dafrc_usd` = DAFRC FY2024 `total_daf_grants` / count;
  - `avg_grant_stated_usd` = the dollar total stated in the same source as the count / count. These dollar totals are taken only from that file's `quote`, `notes` or URL slug (`STATED_USD` in the script).
- **Period match.** This is carried from the counts file. Fidelity's CY2024 count against its June-2024 return is a partial match.
- **Band checks.** `band_check` rows set published size-band counts against Schedule I lines in the same bands.
- **Derived rows.** `derived_published` rows hold the arithmetic on published figures, and each names its operands.

---

## 2. Published grant-size statistics (verbatim)

### 2.1 Found and quoted [F]

| ID | Sponsor | Period | Statistic | Verbatim | Source |
|---|---|---|---|---|---|
| PS-01 | Fidelity Charitable | CY2021 | Average grant $4,407 | chart "Average grant size … $4,407 2021"; "One outlier grant of more than $500 million was removed from calculations for average grant size" | [2022 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2022-giving-report.pdf) |
| PS-02 | Fidelity | CY2021 | 1,180 grants ≥$1m | "Individual grants of $1 million or more grew to 1,180 last year, an increase of 10%." | same |
| PS-03 | Fidelity | CY2022 | Average $4,798 | chart "Average grant size … $4,018 $4,798 2013 2022" | [2023 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf) |
| PS-04 | Fidelity | CY2022 | 1,407 ≥$1m | "Individual grants of $1 million or more grew to 1,407 last year, an increase of 19%." | same |
| PS-05 | Fidelity | CY2023 | Average $4,625 | "while the average grant size has grown to $4,625." Four outlier grants totaling more than $970 million removed | [2024 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf) |
| PS-06 | Fidelity | CY2023 | 1,345 ≥$1m | "Individual grants of $1 million or more grew to 1,345, a 500% increase over the past decade." (1,345 is below the prior report's 1,407 despite "grew") | same |
| PS-07 | Fidelity (corporate accounts) | CY2023 | ≈$11,000 | "Of the more than 23,000 corporate grants, the average granted amount was nearly $11,000." | same |
| PS-08 | Fidelity | CY2024 | Average $5,422 | "Since 2015, the average grant size has grown nearly 30%, from $4,180 to $5,422." "One outlier grant of $430 million was removed from calculations for the average grant size" | [2025 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) |
| PS-09 | Fidelity | CY2024 | 1,971 ≥$1m | "Additionally, there were 1,971 grants of $1 million or more" | same |
| PS-10/11 | Fidelity | CY2025 | Average $5,801; 2,141 ≥$1m | "The average grant size rose 7% to $5,801, and donors recommended 2,141 grants of $1 million or more"; "The volume of grants of $1 million or more increased by 9% to 2,141" | [2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) |
| PS-12 | Morgan Stanley GIFT | CY2024 | Average $11,000 | "$11,000 Average Grant Size" (footnote: "Figures provided by Renaissance Administration LLC as of December 31, 2024.") | [MS GIFT 2024 Year in Review](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-impact-report.pdf) |
| PS-13 | Jewish Communal Fund | FY2023 (Jul 2022–Jun 2023) | Median $750 | "Made an average of 17 grants per fund year, with a median grant amount of $750." | [2023 JCF Giving Report](https://jcfny.org/app/uploads/2024/04/2023-JCF-Giving-Report.pdf) |
| PS-14 | JCF | FY2023 | Average $11,639 | "Average Grant Amount … Median Grant Amount … $11,639 … $750" | same |
| PS-15–18 | JCF | FY2023 | Grants by size band | "UNDER $50,000 … 75,380 GRANTS"; "$50,000 –$1 MILLION … 1,908 GRANTS"; "OVER $1 MILLION … 76 GRANTS"; "77,364 Grants Distributed in 2023"; "These nearly 80,000 individual grants ranged from $36 to transformative gifts reaching tens of millions of dollars." | same |
| PS-19 | DAF Research Collaborative (multi-sponsor sample) | 2014–2022 data, published 2024 | Median $1,000 | "both anonymous and non-anonymous grants had a median grant amount of $1,000" | [2024 National Study on DAFs](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Report.pdf) |
| B5201-030 | Vanguard Charitable | CY2022 | Average $9,500 | “Total grant dollars given $1.87B Unique organizations supported 52,800 Average grant size $9,500 Total grant units given 196K” | [2022 annual report](https://www.vanguardcharitable.org/2022annualreport) |
| B5201-031 | Vanguard Charitable | CY2023 | Average $12,412 | “Unique organizations supported 56,744 Average grant size $12,412 Total grant units given 209K” | [2023 annual report](https://www.vanguardcharitable.org/2023annualreport) |
| B5201-032 | Vanguard Charitable | CY2024 | Average $12,926 | “Total dollars granted $3.1 billion Unique charities supported 62,586 Average grant size $12,926 Total grants issued 240,064” | [2024 annual report](https://www.vanguardcharitable.org/2024annualreport) |
| B5201-033 | Vanguard Charitable | CY2025 | Average $14,808 | “Total dollars granted $3.96B Unique charities supported 66,785 Average grant size $14,808 Total grants issued 267,838” | [2025 annual report](https://www.vanguardcharitable.org/2025annualreport) |
| B5201-034 | Vanguard Charitable | FY2023 | Average $10,972 | “The average grant amount was $10,972, a 17% increase over the year prior.” | [FY23 release, 2023-08-10](https://www.vanguardcharitable.org/news/vanguard-charitable-FY23-granting-record) |
| B5201-035 | Vanguard Charitable | FY2025 | Average ≈$14,000 | “nearly 248,000 grants that averaged approximately $14,000” (b52-01; not re-fetched in wave 52A) | [FY25 release, 2025-08-25](https://www.vanguardcharitable.org/news/vanguard-charitable-donors-deepen-their-impact-driving-another-year-record-granting) |
| B5201-052 | NPT | FY21–FY25 | Mean $73,866, $53,804, $42,707, $42,387, $40,381 | chart “AVERAGE GRANT SIZE • FY21 – FY25 / Mean value per grant recommended ($ in thousands)”, attribute `data-coords-y`: 73866, 53804, 42707, 42387, 40381; the values are dollars despite the “in thousands” label (they match $ / grants within 0.1%) | [FY25 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/) |
| B5201-062 | Jewish Communal Fund | FY2021 | Median $501 | “JCF Fundholders make an average of 17 grants per fund per year, with a median grant amount of $501.” | [PR Newswire, 2022-01-10](https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-record-number-of-grants-to-charity-totaling-520-million-in-fy-21-301456454.html) |
| B5201-063 | Jewish Communal Fund | FY2021 | Average $7,194 | “The average grant amount was $7,194.” (72,000 grants, $520m; mean/median 14.4 [C]) | [PR Newswire, 2021-10-28](https://www.prnewswire.com/news-releases/jewish-communal-fund-sends-out-520-million-in-grants-in-fy-2021-301409897.html) |
| B5201-064 | Jewish Communal Fund | FY2022 | Median $601 | “JCF Fundholders make an average of 18 grants per fund per year, with a median grant amount of $601.” | [PR Newswire, 2023-02-07](https://www.prnewswire.com/news-releases/jewish-communal-fund-releases-50th-anniversary-giving-report-301740253.html) |

- **Excluded.** The Fidelity 2021 Giving Report (CY2020 data) was fetched but is not used (pre-2021 data).
- **Rows B5201-030 to B5201-064** come from b52-01 (`terms-lifted-fetch-2026-11-20.csv`), read at source on 2026-11-20 under the owner decision lifting the site-terms rule and re-checked live by wave 52A (except B5201-035). They are not yet `published_stat` rows in `grant-size-distribution-2026-11-20.csv`; Vanguard figures are calendar-year (annual reports) or fiscal-year (releases), and none is a median or a size band. [V wave 52A]
- **Fidelity derived figures** [C, `derived_published`]:
  - Average grant grew **31.6%** from CY2021 to CY2025.
  - Grants of $1m or more grew **81.4%** over the same period.
  - **0.074%** of CY2024 grants were $1m or more.
  - Those grants are at least **13.2%** of CY2024 dollars. This is a lower bound: 1,971 × $1m / $14.9bn.
- **JCF derived figures** [C, `derived_published`]:
  - **97.4%** of grants were under $50k.
  - **0.098%** were over $1m.
  - The mean-to-median ratio is **15.5**.
  - Average × count = **$900.4m**, consistent with the report's "over $900 million".

### 2.2 Not obtained (blocked or off-limits)

| Source | Why not | What the repo already holds [R] |
|---|---|---|
| Vanguard Charitable impact / annual report | Site terms ([terms and conditions](https://www.vanguardcharitable.org/company-policies/terms-and-conditions)) forbid "systematically extracting data contained in the Site to populate databases". Not fetched in this pass (P-B5103-02). Fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01): averages only, see §2.1 rows B5201-030 to -035 [V wave 52A] | GC-005: 221,825 grants (FY2024 990 Part III) |
| NPT annual report and DAF Report | NPT Terms (on [nptrust.org/privacy-policy/](https://www.nptrust.org/privacy-policy/)) forbid "harvesting data from the Site using robots, spiders, scripts". Not fetched in this pass (P-B5103-02). Fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01) [V wave 52A] | GC-002: 129,575 grants FY2024 (the FY25 report’s restated count, which governs; the FY24 report printed 130,875) [V wave 52A] A web-search snippet suggested a "typical grant" chart near $74k (FY21) and $40k (FY25); it was not read at source in this pass. Read at source 2026-11-20 (b52-01): $73,866 (FY21) to $40,381 (FY25), §2.1 row B5201-052; the 2024 DAF Report has no grant-size statistic [V wave 52A] |
| Schwab / DAFgiving360 report | dafgiving360.org and schwabcharitable.org robots.txt return 403, and the hosts are off-limits for this task | "median grant $500" (FY2026 release) is carried in [g0403-04-escaped-error-cost.md](g0403-04-escaped-error-cost.md) S19 [R, not re-read] |
| NCF, charitynavigator.org | Off-limits under the shared rules in this pass. NCF www pages re-read 2026-11-20 (b52-01): no grant-size statistic; Charity Navigator publishes none for sponsors [V wave 52A] | — |
| Candid DAF fundraising reports | candid.org robots.txt returns 403, treated as disallowed | — |
| PR Newswire releases (JCF FY2021 median $501, etc.). Fetched 2026-11-20 under the owner decision (b52-01): FY2021 median $501 and average $7,194, FY2022 median $601, §2.1 rows B5201-062 to -064 [V wave 52A] | Terms forbid "any robot, spider … to … data mine" | — |
| Chronicle of Philanthropy | robots.txt disallows ClaudeBot and anthropic-ai | — |
| Benefaction Foundation | robots.txt (squarespace) disallows ClaudeBot | — |
| AEF impact map, FFTC annual report | Fetched (robots allow); **no grant-size statistic** in either | Counts only (GC-010, GC-017) |
| Community foundations generally | No robots- and terms-allowed CF report with a size statistic was found this pass (P-B5103-05). A search snippet for one small CF (Mahoning Valley, average $11,569, not DAF-specific) was not read at source | — |

---

## 3. Results from filings

### 3.1 Line-size distribution, all top-50 itemising sponsors [C]

Rows: `row_type=line_size_bin`, `scope=all_top50`.

| Bin | Lines FY2021–24 | Share of lines | Share of $ (all lines) | Share of $ (excl. DAF-to-DAF) |
|---|---:|---:|---:|---:|
| < $10k | 249,287 | 22.6% | 1.0% | 1.2% |
| $10k–$100k | 691,743 | 62.7% | 11.6% | 13.5% |
| $100k–$1m | 140,818 | 12.8% | 21.3% | 24.5% |
| $1m–$10m | 18,688 | 1.7% | 27.7% | 30.4% |
| ≥ $10m | 1,903 | 0.17% | 38.3% | 30.4% |
| **Total** | **1,102,439** | | **$167.63bn** | **$142.73bn** |

### 3.2 Line vs grant: how far apart the units are [C/F]

**Grants per line, 12 sponsors with a stated count (FY2024 lines; `avg_grant_from_count` rows).**

| Sponsor | Stated count (period) | Avg grant: DAFRC $ / count | Avg grant: stated $ / count | Published | Sch. I lines | Median line | Mean line | Grants per line |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Fidelity | 2,664,446 (CY2024; partial match) | $4,751 | $5,592 ($5,431 ex-outlier) | $5,422 (avg) | 80,308 | $19,803 | $155,832 | 33.2 |
| DAFgiving360 | >1.1m (FY2024) | $6,019 | $6,000 | ($500 median [R]) | 55,292 | $17,584 | $115,165 | 19.9 |
| RCF | >160,000 (CY2024) | $4,491 | — | — | not itemised | — | — | — |
| JCF | 89,485 (FY2024) | $11,446 | $11,175 | $11,639 avg / $750 median (FY2023) | 4,673 | $24,148 | $204,002 | 19.1 |
| MS GIFT | 122,000 (CY2024) | $12,416 | $10,656 | $11,000 (avg) | 19,253 | $11,000 | $63,604 | 6.3 |
| Vanguard | 221,825 (FY2024) | $13,782 | $13,524 | $12,926 avg (CY2024 annual report; $14,808 CY2025) [V wave 52A] | 24,269 | $16,504 | $122,889 | 9.1 |
| AEF | 109,708 (US only, CY2024) | $14,160 | $11,873 | — | 14,380 | $17,344 | $87,493 | 7.6 |
| ImpactAssets | >13,500 (CY2024) | $14,573 | $29,630 | — | 2,733 | $25,000 | $212,248 | 4.9 |
| FFTC | 16,531 (all funds, CY2024) | $30,873 | $55,141 | — | 1,605 | $25,000 | $379,478 | 10.3 |
| NPT | 129,575 (FY2024) | $42,935 | — | $42,387 mean (FY24, FY25 report chart) [V wave 52A] | 18,583 | $22,500 | $276,759 | 7.0 |
| GS Philanthropy Fund | ≈29,254 (CY2024) | $92,160 | $105,044 | — | 7,424 | $25,000 | $398,367 | 3.9 |
| SVCF | >14,500 (all SVCF grants) | $211,337 | $106,207 | — | 3,576 | $51,717 | $883,179 | 4.1 |

- **The three sponsors that publish an average agree with the computed values.**
  - Fidelity: $5,431 against $5,422.
  - MS GIFT: $10,656 against $11,000.
  - JCF: $11,175 (FY2024) against $11,639 (FY2023).
  - Vanguard (read 2026-11-20, b52-01): $13,782 and $13,524 (FY2024, 990 count 221,825) against $12,926 (CY2024 annual report, 240,064 grants), a 4.6–6.6% gap on different periods and count bases [C].
  - NPT (read 2026-11-20, b52-01): $42,935 (DAFRC FY2024 dollars / 129,575) against $42,387 (FY25 report chart), a 1.3% gap; NPT’s own $5.49bn / 129,575 = $42,369 [C]. Both sponsors keep their place in the retail vs high-touch ordering. [V wave 52A]
- **Averages separate retail and high-touch sponsors.** RCF, Fidelity and DAFgiving360 average $4.5k–$6k. NPT, Goldman Sachs and SVCF average $43k–$211k [C].
- **Caveat on scope.** ImpactAssets' DAFRC FY2024 DAF grants ($196.7m) are about half its stated $400m, and SVCF's and FFTC's counts include non-DAF grants. Treat those averages as indicative.

**Band checks (`band_check` rows).**

| Check | Band | Sch. I lines | Lines' share of $ | Published grants | Grants per line |
|---|---|---:|---:|---:|---:|
| JCF FY2023 (same fiscal year) | < $50k | 2,955 | 6.1% | 75,380 | **25.5** |
| | $50k–$1m | 1,276 | 27.3% | 1,908 | 1.5 |
| | > $1m | 109 | 66.6% | 76 | **0.70** |
| Fidelity FY2021 vs CY2021 | ≥ $1m | 1,183 | 67.3% | 1,180 | 1.00 |
| Fidelity FY2022 vs CY2022 | ≥ $1m | 1,280 | 67.2% | 1,407 | 1.10 |
| Fidelity FY2023 vs CY2023 | ≥ $1m | 1,295 | 62.3% | 1,345 | 1.04 |
| Fidelity FY2024 vs CY2024 | ≥ $1m | 1,708 | 65.2% | 1,971 | 1.15 |

**Reading [I].**
- **Top end.** At Fidelity, Schedule I lines of $1m or more and published grants of $1m or more agree to within 0–15% in every year. A $1m+ line is therefore usually a single grant.
- **Bottom end.** Small lines are bundles: about 25 grants per sub-$50k line at JCF.
- **JCF's top band.** JCF has more lines over $1m than grants over $1m (109 vs 76), so some $1m+ recipient totals are built from several smaller grants. The line distribution overstates the mega-grant share of dollars, but not by an order of magnitude. Fidelity's published lower bound for $1m+ grants is 13.2% of dollars, against 65% of line dollars, and the true figure lies between the two.
- **Itemised dollars cover almost everything.** Fidelity's FY2024 Schedule I lines total $12.51bn against $12.66bn of DAFRC FY2024 DAF grants (`sponsor_year` / `avg_grant_from_count` rows). Recipients under the $5,000 threshold, plus foreign grants, are a small share of dollars even though they are a large share of grants.

### 3.3 By sponsor type, FY2021–24 [C]

`line_size_summary` rows, `scope_type=segment`.

| Segment (sponsors) | Lines | Median line | Lines < $100k | $ in ≥ $1m (all / excl. D2D) | $ in ≥ $10m (all / excl. D2D) |
|---|---:|---:|---:|---:|---:|
| National (16) | 848,596 | $17,450 | 86.7% | 65.1% / 59.4% | 38.5% / 30.0% |
| Community foundation (22) | 152,879 | $23,400 | 80.1% | 70.1% / 67.0% | 38.7% / 33.2% |
| Single-issue (7) | 100,243 | $21,000 | 82.5% | 56.6% / 53.8% | 22.8% / 19.6% |
| University/hospital (2) | 687 | $75,000 | 52.3% | 96.1% | 88.3% |
| Processor (1: Dechomai) | 34 | $311,311 | 29.4% | 99.8% | 99.1% |

- **Community foundations** have higher median lines, but the most dollar-concentrated tail among the main segments.
- **CF Schedule I includes non-DAF competitive and designated grants**, so a CF line is less purely a DAF line than a national sponsor's line is.
- **SVCF matters.** Without it, the pooled ≥$10m share is 36.3% instead of 38.3% (`scope=all_top50_excl_svcf`).

### 3.4 Trend, FY2021–FY2024 [C]

| FY | Sponsor-years | Lines | $bn | Median line | $ ≥ $1m | $ ≥ $10m | $ ≥ $1m excl. D2D | $ ≥ $10m excl. D2D | Fixed panel $ ≥ $1m / ≥ $10m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2021 | 44 | 236,088 | 37.44 | $18,000 | 68.3% | 42.6% | 62.7% | 34.0% | 68.3% / 42.6% |
| 2022 | 44 | 261,438 | 39.38 | $18,860 | 65.7% | 37.6% | 60.3% | 29.4% | 65.7% / 37.6% |
| 2023 | 46 | 282,142 | 41.53 | $18,500 | 65.0% | 37.2% | 61.3% | 31.9% | 65.4% / 37.4% |
| 2024 | 48 | 322,771 | 49.28 | $19,256 | 65.5% | 36.7% | 59.5% | 27.1% | 66.1% / 37.3% |

- **Line counts grew faster than the median line.** Lines rose 37% (from 236,088 to 322,771; 30% on the fixed panel, 236,088 to 307,818; doc arithmetic on CSV values) while the median line rose only 7%. Part of the all-sponsor rise comes from four more sponsor-years in FY2024.
- **Concentration did not rise.** The $1m+ dollar share is flat at about 65–66% after FY2021, and the $10m+ share is lower in FY2022–24 than in FY2021.
- **Bins are nominal**, so inflation pushes lines upward across bin edges (P-B5103-06).

---

## 4. Combining counts with published medians

1. **The mean grant is about 15 times the median.** JCF FY2023 gives $11,639 against $750 [F]. If that ratio held elsewhere, Fidelity's $5.4k average would imply a median of a few hundred dollars [I]. DAFgiving360's "$500" [R] and the DAFRC sample's $1,000 [F] fit this.
2. **Dollar averages from counts reproduce the published averages within about 4%** where both exist ($5,431 vs $5,422; $10,656 vs $11,000; $11,175 vs $11,639) [C]. The counts file is therefore consistent with the sponsors' own grant-size reporting.
3. **The median Schedule I line is a poor proxy for the typical grant.** The median line is $11k–$25k at nationals and community foundations, against published medians of $500–$1,000 [C/F/R]. The mean line ($64k–$400k) also overstates the average grant ($4.5k–$43k) by a factor of 7–33, matching the grants-per-line ratios.
4. **Line distributions are a fair proxy for the mega-grant tail.** The Fidelity $1m+ counts match (§3.2).

---

## 5. What this means for grant-processing workload (links to exception-load and AI-economics work)

1. **Most grants are small; most dollars are in a few large grants** [C/F].
   - About 97% of JCF grants are under $50k, and 0.07–0.10% of grants are $1m or more at Fidelity and JCF.
   - Lines of $1m or more, mostly single grants at the top end, carry about 60–66% of itemised dollars (excluding or including DAF-to-DAF), and lines of $10m or more carry 27–38%.
   - So a sponsor processing about 2.7m grants (Fidelity CY2024) does fewer than 2,000 grants that hold a large share of its money, and over 2.6m grants that each move a few thousand dollars [I].
2. **Per-grant workload is a count problem** [I].
   - Handling time per grant (eligibility check, OFAC, payment, acknowledgement) is roughly size-invariant at the low end.
   - Cost per dollar granted therefore falls steeply with grant size.
   - Automating the many small, repetitive grants, rather than reviewing a few large ones faster, is what moves processing cost. The [AI-economics replacement analysis](ai-economics-replacement-analysis.md) makes this point qualitatively: per-grant re-verification of charity status should give way to a continuous status feed.
3. **Exception load per grant vs per line.**
   - The [exception-load proxy](gap19-exception-load-proxy.md) measures shares of lines and dollars.
   - [g0401-g0502 §B](g0401-g0502-ai-routing-and-per-grant.md) converts them to grants with an assumed rule, n_i = max(1, k·d_i^β), swept over β ∈ [0, 1], and finds that the broad per-grant exception share (17–31%) depends on β.
   - This pass gives the first direct evidence on that rule [I]:
     - At the top, a $1m+ line holds about one grant of $1m or more (Fidelity 1.00–1.15; JCF 0.70); how many smaller grants share it is not observed. Under β = 1 (equal-size grants) a $1m line would hold on the order of 200 grants of about $5k and no grant of $1m or more, so **β near 1 is ruled out within the model’s equal-size-per-line assumption**. A validator fit of the same rule to JCF FY2023 (4,340 lines plus about 6,260 unitemised recipients sharing $49.6m; 77,364 grants) reproduces the published bands (75,380 / 1,908 / 76) best at β = 0–0.2 (β = 0: 75,444 / 1,832 / 88), gives no grant over $1m from β = 0.35 and none of $50k or more from β = 0.75. [V wave 51A]
     - At the bottom, sub-$50k lines hold about 25 grants each at JCF, so grants are concentrated in small recipients.
     - That is closer to the low-β, recipient-weighted end, with many grants per small recipient. It favours the per-grant shares in which **categories with many small, repeated grants (churches, group subordinates not in Pub 78, recent rulings) dominate the exception count**.
   - P-B5103-01 proposes fitting n(d) to these bands and rerunning.
4. **Risk and value review is a dollar problem** [I].
   - [g0403-04 escaped-error cost](g0403-04-escaped-error-cost.md) prices an escaped error in units of handling time. For a $1m+ grant the dollar exposure is three orders of magnitude above that of the median grant.
   - A size-tiered rule is consistent with the distribution: straight-through or light-touch processing for the small-grant mass, and full human review for the roughly 0.1% of grants of $1m or more.
   - The current [AI-economics v2](ai-economics-v2-observed-costs.md) input, a log-uniform $5–40k average grant size, treats size as a single average. The data show a two-tier mixture (P-B5103-04).
5. **Sponsor archetypes** [C/I].
   - Retail nationals (Fidelity, DAFgiving360, RCF) average about $4.5–6k per grant and 20–33 grants per line, so they are the most count-heavy and stand to gain most from per-grant automation.
   - High-touch sponsors (NPT, GS, SVCF, FFTC) average $31k–$211k per grant and 4–10 grants per line. Their workload is in fewer, larger, more bespoke grants, where review quality matters more than throughput.

---

## 6. Limits

- **Unit.** Schedule I lines are recipient-year totals, itemised above $5,000 and US recipients only (foreign grants are on Schedule F). Every line figure overstates grant size. The size of that bias varies by sponsor (4–33 grants per line).
- **Coverage.** 18 non-itemising sponsor-years are excluded (BofA CGF, RCF and others). RCF is a large retail-style sponsor, so the pooled distribution under-represents small-grant platforms.
- **Mixed grantmaking.** Community foundations, single-issue sponsors and university/hospital filers report non-DAF grants on Schedule I. Line-level fund type is unknown.
- **Periods.** DAFRC fiscal years mix tax periods ending from March to December. Most sponsor reports use calendar years. The Fidelity checks carry a half-year offset.
- **Nominal bins.** There is no inflation adjustment.
- **Published statistics are sparse.**
  - Only Fidelity, MS GIFT and JCF publish first-party grant-size figures that could be fetched.
  - Vanguard and NPT were terms-blocked in this pass. Both were read at source on 2026-11-20 under the owner decision (b52-01) and publish averages only, with no median or size bands. Schwab is off-limits. [V wave 52A]
  - No community-foundation statistic was found.
  - The single median used ($750) is one single-issue sponsor's figure for one year. The DAFRC $1,000 median rests on 2014–2022 data.
- **Outliers.** Fidelity's averages exclude outliers ($430m in 2024; $727m in 2025; more than $970m in 2023), while Schedule I includes them.
- **Stated-dollar values** in `STATED_USD` come from the counts file. Two of them (JCF and DAFgiving360) are from URL slugs of PR Newswire and nonprofitpro pages that were fetched by an earlier pass and not re-read here (see P-B5103-03). Resolution 2026-11-20: the owner lifted the site-terms rule, and b52-01 re-read the Vanguard, NPT and PR Newswire values at source (GC-002, GC-006, GC-016, GC-021, the 21 sponsor-published-share rows and the 4 exception-share G rows); wave 52A re-fetched a sample and confirmed it. The terms-restricted provenance flag (P-B5103-03; validation-wave51a-report.md) is replaced by “re-fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01; live re-check, wave 52A)”. The DAFgiving360 slug (nonprofitpro) was not re-read. [V wave 52A]
- **Workload inferences** in §5 are [I]. No sponsor publishes handling time by grant size.

---

## 7. Data dictionary: `grant-size-distribution-2026-11-20.csv`

**Row types**

| row_type | Rows | Meaning |
|---|---:|---|
| `line_size_bin` | one per scope × fy × basis × bin | Count and dollars of Schedule I lines in a size bin |
| `line_size_summary` | one per scope × fy × basis | Totals, mean, median, ≥$1m and ≥$10m shares |
| `sponsor_year` | 182 | Per sponsor-year summary (all lines) |
| `avg_grant_from_count` | 12 | Average grant from stated counts, with FY2024 line statistics |
| `published_stat` | 19 | Verbatim published grant-size statistics |
| `derived_published` | 10 | Arithmetic on published figures (operands in `note`) |
| `band_check` | 7 | Published grant counts by size band vs Schedule I lines in the same band |
| `excluded_return` | 18 | Sponsor-years not itemised, with the reason |

**Columns**

| Column | Meaning |
|---|---|
| `scope` | One of: `all_top50`; `fixed_panel`; `all_top50_excl_svcf`; `segment:<seg>`; `sponsor:<ein>`; `industry` |
| `scope_type` | One of: all, fixed_panel, sensitivity, segment, sponsor, published |
| `segment` | DAFRC segment: national, processor, community_foundation, single_issue, university_hospital |
| `sponsor`, `ein`, `rank_fy2024` | Sponsor name (DAFRC or counts file), 9-digit EIN, and rank by FY2024 DAF assets |
| `fy` | DAFRC fiscal year (2021–2024) or `2021-2024` pooled. For published rows, the sponsor's stated period |
| `basis` | `all_lines` or `excl_d2d`. For `avg_grant_from_count`: `stated_count`. For `published_stat` and `derived_published`: the metric name. For `band_check`: the check id |
| `bin` | `lt_10k`, `10k_100k`, `100k_1m`, `1m_10m`, `ge_10m` (lower bound inclusive), or `all`. For `band_check` rows: the published band |
| `unit` | What is counted. A Schedule I recipient-year line is **not** a grant |
| `sponsor_years` | Number of returns pooled |
| `lines`, `line_share` | Positive-amount lines, and their share of lines in scope |
| `usd`, `usd_share` | Cash + non-cash dollars, and their share of dollars in scope |
| `mean_line_usd`, `median_line_usd` | Mean and median positive line |
| `lines_le_5k` | Positive lines of $5,000 or less (itemised below the threshold) |
| `lines_nonpositive` | Lines with a zero or negative amount (left out of the bins) |
| `lines_ge_1m`, `line_share_ge_1m`, `usd_share_ge_1m` | Lines of $1m or more: count, share of lines, share of dollars |
| `lines_ge_10m`, `line_share_ge_10m`, `usd_share_ge_10m` | The same for lines of $10m or more |
| `line_share_lt_100k`, `usd_share_lt_100k` | Lines under $100k: share of lines and share of dollars |
| `count_row_id`, `grant_count`, `count_qualifier`, `period_match` | From grant-count-denominators-2026-11-20.csv. In `band_check` rows, `grant_count` is the published band count |
| `dafrc_fy2024_daf_grants_usd`, `avg_grant_dafrc_usd` | DAFRC FY2024 total DAF grants, and that total / `grant_count` |
| `stated_usd`, `stated_usd_note`, `avg_grant_stated_usd` | Dollars stated in the count's source, and those dollars / `grant_count` |
| `grants_per_line` | `grant_count` / FY2024 Schedule I lines, or (in `band_check` rows) / lines in the band |
| `stat_id`, `value`, `quote` | Published or derived statistic id, its value and the verbatim quote |
| `source_url` | Return XML on the GivingTuesday mirror, or the published document |
| `note` | Qualifiers, period mismatches, exclusion reasons |

---

## 8. Source register and robots / terms log

| # | Source | Use | Robots / terms result (checked 2026-11-20) |
|---|---|---|---|
| S1 | IRS Form 990 e-file XML, GivingTuesday mirror of IRS TEOS: `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml` (one URL per sponsor-year in `source_url`) | Schedule I lines (30 FY2021–22 returns fetched; others from local copies and caches) | robots.txt 404, so no rules |
| S2 | DAFRC Annual DAF Report 2025 dataset via [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) ([source](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | Universe, segments, FY2024 DAF grants | repo file |
| S3 | [`grant-count-denominators-2026-11-20.csv`](../../data/mission-2026-11-14/grant-count-denominators-2026-11-20.csv) (each row carries its primary URL) | Stated counts and dollars | repo file (see P-B5103-03) |
| S4 | [`daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv) | DAF-to-DAF exclusion | repo file |
| S5 | Fidelity Charitable Giving Reports [2022](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2022-giving-report.pdf), [2023](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf), [2024](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf), [2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf), [2026](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) | PS-01 to PS-11 | robots 200; `*` disallows only /retired/, /sample-email/, /nuance/, /content/dam/fc-public/docs/vessel/; no Claude-specific group. [Legal note](https://www.fidelitycharitable.org/legal/legal-note.html): copyright notice, no automated-extraction ban found |
| S6 | [MS GIFT 2024 Year in Review](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-impact-report.pdf) | PS-12 | robots 200: ClaudeBot / anthropic-ai / Claude-Web `Allow: /`; `*` allows /content/dam/msdotcom/. [/terms](https://www.morganstanley.com/terms): no extraction ban found |
| S7 | [JCF 2023 Giving Report](https://jcfny.org/app/uploads/2024/04/2023-JCF-Giving-Report.pdf) | PS-13 to PS-18 | robots 200 (disallows /wp/wp-admin/ only). jcfny.org HTML pages, including any terms page, return 403 to a scripted client, so the **terms could not be verified**. One PDF fetched; three guessed URLs for other years returned 404 |
| S8 | [DAFRC 2024 National Study on DAFs](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Report.pdf) | PS-19 (context) | robots 200, empty Disallow |
| S9 | [AEF DAF Impact Map](https://www.aefonline.org/wp-content/uploads/2025/10/AEF_DAFImpactMap_V3.4.pdf); [FFTC 2024–25 Annual Report](https://www.fftc.org/sites/default/files/2025-04/FFTC_2024-2025_Annual_Report.pdf) | Searched; no size statistic | robots 200, allowed |
| B1 | vanguardcharitable.org | not fetched | robots allow, but [terms](https://www.vanguardcharitable.org/company-policies/terms-and-conditions) ban systematic extraction, so **blocked** in this pass (terms page read once to establish this); fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01) [V wave 52A] |
| B2 | nptrust.org | not fetched | robots allow, but Terms ([privacy-policy page](https://www.nptrust.org/privacy-policy/)) ban robots, spiders and scripts, so **blocked** in this pass; fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01) [V wave 52A] |
| B3 | www.dafgiving360.org, www.schwabcharitable.org | not fetched | robots.txt 403, so disallowed; off-limits per task |
| B4 | www.prnewswire.com | not fetched | robots allow, but [terms](https://www.prnewswire.com/terms-of-use/) ban robots, spiders and data mining, so **blocked** in this pass; fetched 2026-11-20 under the owner decision lifting the site-terms rule (b52-01) [V wave 52A] |
| B5 | candid.org, blog.candid.org | not fetched | robots.txt 403, so disallowed |
| B6 | www.philanthropy.com | not fetched | robots: ClaudeBot and anthropic-ai `Disallow: /` |
| B7 | benefaction-foundation.squarespace.com | not fetched | robots: ClaudeBot group, so blocked |
| — | charitynavigator.org, ncfgiving.com and NCF hosts | not touched | shared rules |

The raw log is in the scratchpad (`b5103/robots_log.tsv`; robots files in `b5103/robots/`; terms pages in `b5103/terms/`).
