# P-B45N33-01: fee census of the long tail (sponsors under $50m)

**Date:** 2026-11-19 · **Queue item:** P-B45N33-01 (follow-up to `b45n33-long-tail-operating-cost.md`, which noted "no fee data for the tail")

**Outputs**
- [`data/mission-2026-11-14/long-tail-fee-census-2026-11-19.csv`](../../data/mission-2026-11-14/long-tail-fee-census-2026-11-19.csv): 60 rows, one per sampled sponsor (data dictionary in §6).
- [`scripts/mission_long_tail_fee_census.py`](../../scripts/mission_long_tail_fee_census.py): stdlib only, functional style. Tasks: `sample` (stratified draw, seed 20261119), `crawl` and `fetch` (robots-checked, generic user agent `research-script/1.0`, cache outside the repo), `census` (quote verification, fee engine, cost join, all tables). `python3 scripts/mission_long_tail_fee_census.py . --task census --cache-dir CACHE` reproduces every table in the Appendix. Without `--cache-dir` it still runs, but the `quote_check` and `robots` columns come out blank.
- [`data/mission-2026-11-14/queue-proposals-b45n33-01.csv`](../../data/mission-2026-11-14/queue-proposals-b45n33-01.csv): 5 follow-ups.

**Labels:** **[F]** transcribed from a sponsor document (quote verified against the cached text by the script); **[C]** script computation; **[I]** inference. Allocated operating costs come from the long-tail cost study and are **[I]** by construction (rules A, G and AM). This is research, not legal, tax or accounting advice.

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **How often do tail sponsors publish a fee?** | **7 of 60 (11.7%; Wilson 95% 5.8–22.2%)** publish a 2021-or-live balance-based admin rate (one of them a stated 0%). Counting one pre-2021 schedule: 8/60 (13.3%). **Counting any published fee term** (a rate, an opening minimum, a linked schedule, or an unquantified fee): **15/60 (25.0%; 15.8–37.2%)**. The design-weighted rate is 11.7%, the same, because allocation is close to proportional [C]. | High on the counts [C]. Medium on the "no published fee" calls (see §4) |
| **By type** | **CFs: 6/31 (19.4%; 9.2–36.3%)** publish a 2021+ rate, and 12/31 (38.7%) publish some fee term. Single-issue 0/13 (0–22.8%), faith 0/8 (0–32.4%), other 1/8 (Cal Poly Pomona's 2%). Among the 53 sites that could be read within robots rules, the rate is 7/53 (13.2%) overall and 6/26 (23.1%) for CFs [C]. | High [C] |
| **By size** | Publication falls with size: 2021+ rate published by 3/14 sponsors in the $10–50m band, 3/24 in $1–10m, 1/18 under $1m and 0/4 at zero assets. Any fee term: 7/14, 5/24, 3/18, 0/4 [C]. The intervals overlap. | Medium [C] |
| **What the publishers charge** | Effective annual admin fee, the 7 sponsors with a rate: median **150 bps at $25k, $100k and $500k** (IQR 138–175 at the first two). CFs only (n = 6, including the 0% Adirondack Trust Company Community Fund): **150 / 150 / 138 bps**. Range: 0 bps (ATC; a 0.5% bank investment fee instead) to 200 bps (Whatcom non-endowed; Cal Poly Pomona) [C]. Minimum annual fees, where stated: $150–$250. Opening minimums, where stated (13 of 60): median $5,000 ($0 to $100,000) [F/C]. | High on each schedule [F]; low on the distribution (n = 6–7) |
| **vs the top-100 CF census** | **Tail CFs publish less and charge more.** Top-100 CFs: 34/100 publish a 2021+ schedule (Wilson 25.5–43.7%), against 6/31 tail CFs (9.2–36.3%); the intervals overlap. Recomputed on the same balances with the same engine, top-100 medians are **118 / 100 / 100 bps** at $25k / $100k / $500k, against **150 / 150 / 138** for the tail CFs. Tail opening minimums are lower (median $5,000 vs $15,000) [C]. | Medium (tail n = 6) |
| **Do published fees cover the allocated cost?** | At each publisher's own FY2024 average account: **rule A, 1 of 7** (Hutchinson, fee 125 bps vs cost 101 bps); **rule G, 0 of 5**; **AM floor, 4 of 7**. Median fee ÷ cost: **0.52 (A), 0.22 (G), 1.18 (AM)** [C on the arithmetic; I on the costs]. So the published fee covers about half the rule-A cost. It covers the admin-only floor at a small majority of publishers. | Low–medium (n = 5–7) [I] |
| **Population view** | At the tail-CF published median (150 bps), **33.7%** of the 603 usable tail CFs have rule-A cost at or below the fee (27.3% under rule G, 75.6% under AM). At the 100 bps top-100 median the figures are 15.3% / 18.0% / 55.9%, the numbers in the cost study [C]. **[I] The tail does charge more than the top 100, but at its own median fee two thirds of tail CFs still do not recover rule-A cost from the DAF fee.** | Medium [I] |

---

## 1. Method

### 1.1 Frame, strata and draw [C]
- **Frame:** `daf-long-tail-sponsors-fy2021-2024.csv`, rows with `size_band_fy2024` in `t10_50`, `t1_10`, `t0_1` and `zero`. There are 1,240 such rows, identical to the cost study.
- **Type (4 classes)** from the DAFRC-based `sponsor_category`:
  - `community_foundation` becomes **cf** (641 sponsors).
  - `single_issue_other` becomes **single_issue** (283).
  - `religious` becomes **faith** (149).
  - `university_or_hospital`, `national_standard` and `donation_processor` become **other** (167).
- **Strata:** type × size band, 16 cells, all non-empty.
- **Allocation:** n = 60, proportional, with a floor of 1 per stratum and largest-remainder rounding. The weights N/n run from 20 to 26, except in the four zero-asset strata (3–12). That is why the weighted and unweighted rates hardly differ.
- **Draw:** `random.Random(20261119 + stratum index).sample()` over each stratum sorted by EIN. Re-running `--task sample` reproduces the same 60 EINs. The design table is T1 in the Appendix.

### 1.2 Finding the website [F]
- **CFs (30 of 31):** the homepage in `cf-vendor-map-by-ein-v2.csv`, which came from the 990 `WebsiteAddressTxt`.
- **Non-CFs:** `WebsiteAddressTxt` in the sponsor's FY2024 990 XML, read from the GivingTuesday mirror (object ids from the cost study).
- **Where the 990 gave none:**
  - Christian Aid Ministries Foundation was found by web search.
  - Catalyst Trust of Indiana, IDACORP Employee Community Services, Gordon Christian Trust and Cerity Partners Foundation have no website on the 990 ("N/A" or "NONE") and none was found by search. They are recorded as `no_website_found`.

### 1.3 Crawl and robots.txt [F]
1. **Robots check first.** For every host, robots.txt was read before any page, with the user agent `research-script/1.0`. The verdict is logged per row (`robots` column).
   - robots.txt returning **401 or 403** is treated as disallowed, and nothing further was fetched from that host.
   - No user agent was changed to get past a block.
2. **What was fetched.** The homepage, sitemap.xml (including WordPress CDATA and page sub-sitemaps), and up to 16 candidate pages or documents per site. Candidates are links whose URL or anchor text mentions fees, minimums, schedules, donor-advised funds, fund types, policies or opening a fund, followed to depth 2. PDFs were converted with `pdftotext`.
3. **Manual follow-up.** Each site was then checked by hand from the cache: keyword contexts, anchor lists and sitemaps. A few documents were read directly; each was robots-checked by the same code.
4. **Off-site file hosts.** Fee schedules on such hosts were fetched only where those hosts' robots.txt allowed it. Google Drive's `uc` download path is disallowed. The Wix `usrfiles.com` host returned 403.
5. **Search engine.** Web search was used only to find URLs. No figure in the census comes from a search snippet.

### 1.4 Status codes
| Status | Meaning | Counts as "published" in |
|---|---|---|
| `published_schedule` | A balance-based admin rate is published, dated 2021+ or live and undated | 2021+ rate, any rate, any term |
| `published_no_admin_fee` | Sponsor states it charges no admin fee (rate 0) | 2021+ rate, any rate, any term |
| `published_pre2021` | Rate published, but the document is dated before 2021 (kept, excluded from the 2021+ distribution) | any rate, any term |
| `published_unread` | Official site links a fee schedule, but its file host is disallowed by robots.txt | any term |
| `partial` | Some fee term is published (opening minimum, a fee described but not quantified, a ceiling, a card fee), no rate | any term |
| `no_published_fee` | Site read; no DAF fee or fee term found | – |
| `no_website_found` | No website on the 990 or by search | – (counted as no published fee) |
| `robots_blocked` | robots.txt 403: nothing could be read | – (unknown; excluded in the "readable sites" column) |

### 1.5 Fee computation [C]
- **Formula.** Effective annual admin fee at a constant balance B (in `effective_admin_fee`):
  - Marginal schedules apply each tier's rate to its slice of B.
  - `flat_on_total` schedules apply the rate of B's band to the whole balance.
  - The result is then max(fee, minimum annual fee), plus any flat fee. bps = fee ÷ B × 10⁴.
- **Balances:** $25k, $100k and $500k. Gift and grant fees are recorded as text and are **not** in the effective fee. Investment fees are recorded, also not included.
- **Top-100 comparison.** The 34 `published_schedule` rows of `cf-daf-fee-census-2026.csv` were re-run through the same engine at the same three balances. Their tiers were parsed from `admin_tiers`, with minimum and flat fees from the CSV as filed. Hybrid "flat over $X" bands are not in that column (OCCF), so the top-100 figures at $500k may differ slightly from that census's own arithmetic. At $100k the recomputed median (100 bps) matches the census note (§3.2 of `direction-cf-consolidation-fees.md`).

### 1.6 Comparison with allocated operating cost
- **Cost data.** From `long-tail-operating-cost-2026-11-19.csv`: per-account and per-DAF-dollar cost under rule A (assets share), rule G (grants share) and the AM admin-only floor. These are [I] by construction; see that note's §1.3.
- **Coverage test.** For each sponsor with a rate, the fee is computed at its own FY2024 average account (`avg_account_fy2024`) and compared with the allocated cost per screened account. The two are equivalent to comparing fee bps with cost bps at that balance.
- **Exclusions.** Rows with a missing or zero allocated cost are left out of that rule. Under rule G, Cal Poly Pomona's DAF grant share is 0, so its rule-G cost is 0; Homer has no rule-G figure.
- **Population view (T9).** Share of all 603 usable tail CFs in the cost study whose allocated cost per DAF dollar is at or below 100, 150 or 200 bps.

### 1.7 Verification [C]
Every transcribed figure has a verbatim quote in `FEES` in the script. `census` checks each quote, whitespace-normalised and case-insensitive, against the cached text of its source.
- **Result:** 15 of 15 sponsors with quotes are "verified n/n" (`quote_check` column).
- **Dates:** source dates are what the document shows (a "Revised" or "Last Updated" line, the version number, or the wp-content upload path), or "live 2026-11-19" for undated pages.

---

## 2. Results

### 2.1 Publication rates
See T2 and T3 in the Appendix. Headline:

| Group | n | 2021+ admin rate published | Any fee term or linked schedule |
|---|---|---|---|
| All sampled | 60 | **7 (11.7%; 5.8–22.2%)** | **15 (25.0%; 15.8–37.2%)** |
| Community foundations | 31 | 6 (19.4%; 9.2–36.3%) | 12 (38.7%; 23.7–56.2%) |
| Single-issue | 13 | 0 (0–22.8%) | 1 (7.7%) |
| Faith | 8 | 0 (0–32.4%) | 1 (12.5%) |
| Other (university/hospital, nationals, processors) | 8 | 1 (12.5%) | 1 (12.5%) |

- **[C] 34 of 60 sites were read and contain no DAF fee at all.** A further 7 hosts block robots (Wichita Falls, Clinton County OH, West Kentucky, Greene County PA, Clarinda, Williams College, Wheaton College), and 4 sponsors have no website.
- **[I] Outside CFs, a DAF is an accommodation, not a product.** Single-issue, faith and university sponsors in the sample do not market DAFs with terms. Examples:
  - IIE's "DAF" page is about giving *to* IIE from a DAF.
  - Christian Aid Ministries Foundation describes its DAF with no fee. A now-404 page indexed by search said it "generally" charges nothing; this is not used.
  - The one non-CF schedule is Cal Poly Pomona's: 2% of balance, a $100,000 opening minimum, and at least 50% of each year's distributions to the Foundation.

### 2.2 Published schedules (2021+ or live)

| Sponsor (band) | Schedule [F] | Min fee | Opening min | $25k / $100k / $500k bps [C] | Source date |
|---|---|---|---|---|---|
| Whatcom CF (WA, $10–50m) | Non-endowed: 2.00% to $500k, 1.50% to $1m, 1.25% to $5m, 1.00% above; same scale as a gift fee on short-term-pool gifts | – | $5,000 | 200 / 200 / 200 | T&C "Last Updated: 12/31/2025"; live page |
| Hutchinson CF (KS, $10–50m) | 1.25% to $2m ("or $250, whichever is greater"), 0.75% to $5m, 0.50% to $15m, 0.25% above | $250 | none (no grants until $10,000) | 125 / 125 / 125 | 2023 schedule, uploaded 2025-02 |
| Pikes Peak CF (CO, $10–50m) | Non-endowed DAF: 1.5% first $3m, 1.5% next $2m, 0.75% next $5m, 0.25% over $10m | $250 | not stated | 150 / 150 / 150 | uploaded 2025-01 |
| Homer Foundation (AK, $1–10m) | DAF 1.5%, not less than $150; −0.25 points above $1m | $150 | $10,000 | 150 / 150 / 150 | Funds Policy v.1.28.21 (Jan 2021), in a City of Homer board packet |
| Athens County Foundation (OH, $1–10m) | "1.5% to $500,000 or 1% for $500,000+" | – | $10,000 | 150 / 150 / 100 | live, undated |
| Adirondack Trust Co. Community Fund (NY, $1–10m) | Admin "at no charge"; bank investment fee 0.5% a year, waived in year 1 | – | $5,000 | 0 / 0 / 0 | live, undated |
| Cal Poly Pomona Philanthropic Fdn (CA, <$1m) | 2% of fund balance, charged quarterly | – | $100,000 | 200 / 200 / 200 | undated policy (example dated 2021-06-15) |
| *CF of West Texas (TX, $10–50m), pre-2021* | *1.0%, quarterly on average balance* | – | *$5,000* | *100 / 100 / 100* | *"Revised 12/01/16": excluded from the 2021+ distribution* |

**Interpretation choices, each with its sensitivity [C]:**
- **Whatcom.** The 2.00% non-endowed short-term scale is used. The same page lists 1.50% for endowed and long-term non-endowed funds. With 1.50%, Whatcom is 150 bps at all three balances, and the CF medians are unchanged (150 / 150 / 138).
- **Athens.** Read as a band rate on the whole balance, so it is 100 bps at $500k. Under a marginal reading it is 150 bps, which makes the CF median at $500k 150.
- **Pikes Peak.** The non-endowed column is used. The endowed DAF column (1.00% on the first $3m) would be 100 bps at all three balances.

### 2.3 Partial and unread publishers [F]
- **Published but unread** (the schedule exists; its host is disallowed by robots):
  - **CF of the Eastern Shore (MD):** the schedule is a Google Drive file. The page itself says non-endowed DAFs open at $5,000, and below a $50,000 balance "in lieu of a fee, CFES sweeps any interest earned".
  - **CF of Greater Muscatine (IA):** the schedule is on usrfiles.com. Non-endowed DAFs open at $2,500; minimum grant $250.
- **Partial** (no rate):
  - **Licking County Foundation:** $25,000 opening minimum (can be reached over 5 years). Costs are "paid from the fund's total return".
  - **CF of Mendocino County:** $10,000 minimum. An undated .doc gives "1.5% or less of Fund balance".
  - **CF of Central Wisconsin:** $1,000 minimum; 3% card-processing fee on online gifts.
  - **GlobalTrust Funds:** "charitable administration fees" on "a blended schedule" against average daily balance, rates not published.
  - **Jewish Federation Foundation of Greater RI:** $2,500 minimum; the Alliance's newspaper (2021-11 and 2022-11) says "Low administration fee" without a number.

### 2.4 Comparison with the top-100 CF census (T5)

| Measure | Tail CFs (sample) | Top-100 CFs |
|---|---|---|
| 2021+ schedule published | 6/31 = 19.4% (9.2–36.3%) | 34/100 = 34.0% (25.5–43.7%) |
| Any fee term or schedule | 12/31 = 38.7% (23.7–56.2%) | 52/100 = 52.0% (42.3–61.5%) |
| Admin bps, $25k | 150 (131–150; n=6) | 118 (100–188; n=34) |
| Admin bps, $100k | 150 (131–150; n=6) | 100 (100–125; n=34) |
| Admin bps, $500k | 138 (106–150; n=6) | 100 (100–125; n=34) |
| Opening minimum | $5,000 (n=11) | $15,000 (n=19) |

- **[C] Publication rates.** The tail-CF rate is lower, but the 95% intervals overlap. With n = 31 the difference is not statistically established.
- **[C] Fee levels.** The tail-CF medians are higher than the top-100 medians at $100k (150 vs 100 bps) and $500k (138 vs 100). Five of the six tail-CF rates (Whatcom, Hutchinson, Pikes Peak, Homer, Athens) are at or above the top-100 median at $100k.
- **[I] Size and price.** Higher rates and lower opening minimums fit small CFs whose DAFs are small and costly per dollar to run (cost study §2.1). Nothing here shows that the fee is set from cost.
- **[I] Selection.** The tail publishers are concentrated in the $10–50m band (3 of the 6 tail CFs with a rate), the end of the tail closest to the top 100.

### 2.5 Fees against allocated operating cost (T7–T9)
- **[C] At the sponsor's own average account** (7 sponsors with a rate and a cost figure):

  | Rule | Fee ≥ cost | Median fee ÷ cost |
  |---|---|---|
  | A | 1 of 7 | 0.52 |
  | G | 0 of 5 | 0.22 |
  | AM | 4 of 7 | 1.18 |

  - **Hutchinson** is the only sponsor whose fee covers rule-A cost: 125 bps on a $409k average account against 101 bps.
  - **Athens** does not cover even the AM floor: 150 bps against 313 bps.
  - **ATC** charges no admin fee, so it covers nothing. Its rule-A cost (41 bps) is among the lowest in the sample, consistent with administration sitting at the bank.
- **[C] The publishers are the costlier CFs.** Sampled CFs that publish a rate have higher allocated cost (rule A median 300 bps, $4,699 per account) than sampled CFs that do not (181 bps, $2,683). This holds with n = 6 vs 22.
- **[C] Population view.** At 150 bps, the observed tail-CF median fee, 33.7% of the 603 usable tail CFs have rule-A cost at or below the fee (27.3% under G, 75.6% under AM). At 100 bps the shares are 15.3% / 18.0% / 55.9%.
- **[I] What this implies.** The cost study's inference that "most run DAFs at a loss under either rule" holds with the observed fee level in place of the hypothetical 100 bps. Under the AM floor, most would break even. This says the DAF fee is priced nearer to overhead than to fully allocated cost. It needs the caveat that rules A and G load non-DAF activity onto DAFs.

---

## 3. What this changes in the repository
1. **`b45n33-long-tail-operating-cost.md` §2.4 and §4.**
   - "No fee data for the tail" is now answered. About 1 in 9 tail sponsors (1 in 5 CFs) publish a 2021+ admin rate.
   - The observed tail-CF median is 150 bps at $100k, not the hypothetical 100 bps.
   - At 150 bps, coverage of rule-A cost rises from 15.3% to 33.7% of tail CFs [C].
2. **`direction-long-tail-sponsors.md` §0 and `strategic-synthesis.md`.** The "$92m a year at the 100 bps CF median" admin-fee pool used a top-100 rate. The tail charges more where it publishes. At 150 bps, the same arithmetic on $9.18bn gives about $138m [C on that assumption]. That figure is not proposed for adoption: only 7 of 60 sponsors publish a rate, and the non-CF half of the tail mostly does not appear to sell DAFs at all.

---

## 4. Limits
1. **Small n.** Only 6–7 rates. Fee distributions and coverage counts are indicative; every interval in §2 is wide.
2. **"No published fee" is a crawl result, not a certainty.**
   - Pages rendered only by JavaScript, PDFs without a text layer, and pages reachable only through site search may hold fees the crawl did not see. Whatcom's schedule was found only on the second pass, through its page sitemap.
   - The census likely **understates** publication somewhat, especially for CFs.
   - The 7 robots-blocked sites (5 CFs) are unknown, not "no fee". Excluding them, the 2021+ rate is 7/53 and 6/26 for CFs.
3. **Dates.** Three schedules are undated live pages; one is undated with a 2021 worked example (Cal Poly Pomona). Homer's January 2021 policy is the sponsor's own document, but it was found on the City of Homer's site, not on the sponsor's.
4. **Constant-balance fees.** These exclude gift fees (Whatcom's short-term-pool gift fee, CFCW's 3% card fee), grant fees, investment fees, monthly or average-balance bases and household aggregation (Whatcom applies its scale to all of a donor's funds combined).
5. **Interpretation choices.** Whatcom, Athens and Pikes Peak each involve a choice of column or basis; see §2.2 for each sensitivity. None moves the tail-CF median at $100k.
6. **Top-100 comparator.**
   - It was recomputed from `cf-daf-fee-census-2026.csv` as filed. The 2026-11-19 refresh (`cf-daf-fee-census-refresh-2026-11-19.csv`) changes a few top-100 rows (Minneapolis, SFF) that are `pre2021` in the base file, so they are not in the 34.
   - Hybrid bands are not parsed.
   - The top-100 census also used manual search, so its publication rate is not measured identically.
7. **Allocated cost is [I].** Rules A and G load non-DAF cost onto DAFs; AM understates CFs (cost study §1.3).
8. **Single fiscal year.** Average accounts are for FY2024; fees are from 2021–2026 documents.

---

## 5. Source register (primary URLs; all retrieved 2026-11-19 by `research-script/1.0` after a robots.txt check)

| # | Sponsor (EIN) | URL | Used for |
|---|---|---|---|
| S1 | Whatcom CF (911726410) | https://whatcomcf.org/financial-oversight/investment-approach-fees/ | Schedule, gift fee, investment notes |
| S2 | Whatcom CF | https://whatcomcf.org/wp-content/uploads/2025/12/Non-Endowed-Funds-Terms-and-Conditions-12.2025.pdf | $5,000 DAF minimum; "Last Updated: 12/31/2025" |
| S3 | Hutchinson CF (481076910) | https://hutchcf.org/wp-content/uploads/2025/02/2023-fee-schedules_DAF.pdf | Schedule |
| S4 | Hutchinson CF | https://hutchcf.org/attorneysandadvisors/advisor-faq/ | No opening minimum; $10,000 before grants |
| S5 | CF of West Texas (751709180) | https://www.cfwtx.org/_files/ugd/416dfb_6eb9ed0847e14a06b62f37087d507867.pdf | 1.0%, revised 12/01/16 (pre-2021) |
| S6 | CF of West Texas | https://www.cfwtx.org/advisor-faqs | $5,000 minimum; investment fees tiered |
| S7 | CF of the Eastern Shore (521326014) | https://www.cfes.org/createafund ; https://www.cfes.org/advisors | $5,000 minimum, interest sweep; schedule link (Drive, robots-disallowed) |
| S8 | Pikes Peak CF (841339670) | https://www.ppcf.org/wp-content/uploads/2025/01/Fund-Types-Fee-Structure.pdf | Schedule, $250 minimum fee |
| S9 | Pikes Peak CF | https://www.ppcf.org/wp-content/uploads/2025/01/DAF-vs-PF.pdf | Own manager from $100,000 |
| S10 | Licking County Fdn (311760702) | https://www.thelcfoundation.org/file_download/dd22cd34-c547-4cee-990a-5658aa280b4c | $25,000 minimum; cost from total return |
| S11 | CF of Mendocino County (680330462) | https://communityfound.org/giving/become-donor/types-of-funds/donor-advised-funds/ ; https://communityfound.org/wp-content/uploads/Terminating-a-Private-Foundation-to-a-Donor-Advised-Fund.doc | $10,000 minimum; "1.5% or less" |
| S12 | Homer Foundation (920139183) | https://www.cityofhomer-ak.gov/sites/default/files/fileattachments/memo/72719/01-01_funds_policy_v.1.28.21.pdf | Funds Policy Appendix 3 fee structure |
| S13 | Adirondack Trust Co. Community Fund (266394395) | https://atccf.org/Donor-Options/donor-advised-fund | No admin charge; 0.5% investment fee; $5,000 minimum |
| S14 | Athens County Fdn (311040215) | https://www.athensfoundation.org/create-a-fund ; https://www.athensfoundation.org/daf | Rate, $10,000 minimum |
| S15 | CF of Central Wisconsin (390827885) | https://cfcwi.org/new-fund/ ; https://cfcwi.org/ways-to-give/ | $1,000 minimum; 3% card fee |
| S16 | CF of Greater Muscatine (421495980) | https://www.givinggreater.org/_files/ugd/0f7e19_e35188275f7b4f3aaf1a768995e4cc28.pdf ; https://www.givinggreater.org/giving | $2,500 minimum; schedule link (usrfiles.com, robots 403) |
| S17 | GlobalTrust Funds (472525808) | https://globaltrustfunds.org/faqs/ ; https://globaltrustfunds.org/wp-content/uploads/2024/07/Grant_recommendation_form.pdf | Fee basis described; $100 minimum grant |
| S18 | Jewish Federation Fdn of Greater RI (050259003) | https://www.jewishallianceri.org/support-us/giving-options/donor-advised-funds | $2,500 minimum |
| S19 | Jewish Alliance of Greater RI (newspaper) | https://www.jewishrhody.com/stories/jffs-donor-advised-funds-make-charitable-giving-easy,13866 (2021-11-07); https://jewishrhody.com/stories/jffs-donor-advised-funds-make-charitable-giving-easy,21321 (2022-11-06) | "Low administration fee" (no rate); read with WebFetch, not script-verified |
| S20 | Cal Poly Pomona Philanthropic Fdn (832300241) | https://www.cpp.edu/philanthropy/policies/504philanthropic-donorsadvisedfundpolicy.pdf | 2% fee; $100,000 minimum; 50% to the Foundation |
| S21 | Websites of non-CF sponsors | IRS e-file XML via https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml (object ids in the cost CSV) | `WebsiteAddressTxt` |
| R1 | Repo | `daf-long-tail-sponsors-fy2021-2024.csv`; `long-tail-operating-cost-2026-11-19.csv`; `cf-daf-fee-census-2026.csv`; `cf-vendor-map-by-ein-v2.csv` | Frame, costs, top-100 comparator, CF homepages |

The homepages of all 56 sponsors with a website are in the CSV (`website`), each with its robots verdict (`robots`).

---

## 6. Data dictionary: `long-tail-fee-census-2026-11-19.csv`

| Column | Meaning |
|---|---|
| `ein`, `name` | EIN and DAFRC name (as in the long-tail file) |
| `type4` | Stratification type: `cf`, `single_issue`, `faith`, `other` (mapping in §1.1) |
| `sponsor_category`, `size_band_fy2024` | From `daf-long-tail-sponsors-fy2021-2024.csv` |
| `stratum`, `stratum_N`, `stratum_n`, `weight` | Stratum key (type\|band), frame size, sample size, design weight N/n |
| `daf_assets_fy2024`, `accounts_fy2024_screened`, `avg_account_fy2024` | Corrected FY2024 DAF assets, screened account count, average account (long-tail file) |
| `website` | Official website used (homepage, or the DAF page where noted) |
| `fee_status` | Status code (§1.4) |
| `in_2021plus_distribution` | `yes` if the rate enters the 2021+ fee distribution (`published_schedule`, `published_no_admin_fee`) |
| `fee_basis` | `marginal` or `flat_on_total` (blank without a rate) |
| `admin_tiers` | Tiers as `lower-upper: rate%` (blank upper = open-ended) |
| `min_annual_fee_usd`, `flat_annual_fee_usd` | Minimum annual admin fee; flat annual fee (USD) |
| `opening_min_usd` | Minimum gift to open a DAF (0 = stated no minimum; blank = not stated) |
| `gift_fee`, `grant_fee`, `investment` | Gift or contribution fees, grant fees and investment options or fees as published (text) |
| `admin_fee_usd_25k/100k/500k` | Effective annual admin fee at a constant $25k / $100k / $500k balance [C] |
| `admin_bps_25k/100k/500k` | The same in bps of balance [C] |
| `activity_fee_bps_at_10pct_turnover` | Grant-fee-only schedules: stated % × 10% turnover (none in this sample) |
| `usable_cost` | `usable` flag from the cost study |
| `cost_bps_alloc_A/G/AM` | Allocated DAF operating cost per DAF dollar, bps (cost study) [I] |
| `cost_per_account_alloc_A/G/AM` | Allocated cost per screened DAF account, USD [I] |
| `fee_usd_at_avg_account`, `fee_bps_at_avg_account` | Published fee at the sponsor's own FY2024 average account [C] |
| `covers_alloc_A/G/AM` | `yes` if that fee ≥ allocated cost per account; blank if either is missing or cost is 0 |
| `coverage_ratio_alloc_A/G/AM` | Fee ÷ allocated cost per account |
| `source_url`, `source_date` | Primary document and the date it shows (or "live 2026-11-19") |
| `robots` | robots.txt verdict logged for the source or the homepage |
| `quote_check` | Script verification of the transcribed quotes against the cached source ("verified k/n") |
| `notes` | Interpretation choices and what was read |

---

## Appendix: script output (`--task census`)

## T1 Sample design

| Stratum (type|band) | Frame N | Sample n | Weight N/n |
|---|---|---|---|
| cf|t10_50 | 207 | 10 | 20.700 |
| cf|t1_10 | 272 | 13 | 20.923 |
| cf|t0_1 | 150 | 7 | 21.429 |
| cf|zero | 12 | 1 | 12.000 |
| single_issue|t10_50 | 21 | 1 | 21.000 |
| single_issue|t1_10 | 112 | 5 | 22.400 |
| single_issue|t0_1 | 138 | 6 | 23.000 |
| single_issue|zero | 12 | 1 | 12.000 |
| faith|t10_50 | 43 | 2 | 21.500 |
| faith|t1_10 | 63 | 3 | 21.000 |
| faith|t0_1 | 40 | 2 | 20.000 |
| faith|zero | 3 | 1 | 3.000 |
| other|t10_50 | 22 | 1 | 22.000 |
| other|t1_10 | 77 | 3 | 25.667 |
| other|t0_1 | 60 | 3 | 20.000 |
| other|zero | 8 | 1 | 8.000 |

## T2 Fee status by group

| Group | n | published_schedule | published_no_admin_fee | published_pre2021 | published_unread | partial | no_published_fee | no_website_found | robots_blocked |
|---|---|---|---|---|---|---|---|---|---|
| All 60 | 60 | 6 | 1 | 1 | 2 | 5 | 34 | 4 | 7 |
| cf | 31 | 5 | 1 | 1 | 2 | 3 | 13 | 1 | 5 |
| single_issue | 13 | 0 | 0 | 0 | 0 | 1 | 10 | 1 | 1 |
| faith | 8 | 0 | 0 | 0 | 0 | 1 | 6 | 1 | 0 |
| other | 8 | 1 | 0 | 0 | 0 | 0 | 5 | 1 | 1 |
| band t10_50 | 14 | 3 | 0 | 1 | 1 | 2 | 5 | 1 | 1 |
| band t1_10 | 24 | 2 | 1 | 0 | 0 | 2 | 15 | 0 | 4 |
| band t0_1 | 18 | 1 | 0 | 0 | 1 | 1 | 12 | 1 | 2 |
| band zero | 4 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 |

## T3 How often fees are published (k/n, Wilson 95% interval)

| Group | 2021+ admin rate published (k/n, Wilson 95%) | Any rate incl. pre-2021 | Any fee term or linked schedule | 2021+ rate, readable sites only | Design-weighted 2021+ rate |
|---|---|---|---|---|---|
| All 60 | 7/60 = 11.7% (5.8–22.2%) | 8/60 = 13.3% (6.9–24.2%) | 15/60 = 25.0% (15.8–37.2%) | 7/53 = 13.2% (6.5–24.8%) | 11.7% |
| cf | 6/31 = 19.4% (9.2–36.3%) | 7/31 = 22.6% (11.4–39.8%) | 12/31 = 38.7% (23.7–56.2%) | 6/26 = 23.1% (11.0–42.1%) | 19.5% |
| single_issue | 0/13 = 0.0% (0.0–22.8%) | 0/13 = 0.0% (0.0–22.8%) | 1/13 = 7.7% (1.4–33.3%) | 0/12 = 0.0% (0.0–24.2%) | 0% |
| faith | 0/8 = 0.0% (0.0–32.4%) | 0/8 = 0.0% (0.0–32.4%) | 1/8 = 12.5% (2.2–47.1%) | 0/8 = 0.0% (0.0–32.4%) | 0% |
| other | 1/8 = 12.5% (2.2–47.1%) | 1/8 = 12.5% (2.2–47.1%) | 1/8 = 12.5% (2.2–47.1%) | 1/7 = 14.3% (2.6–51.3%) | 12.0% |
| band t10_50 | 3/14 = 21.4% (7.6–47.6%) | 4/14 = 28.6% (11.7–54.6%) | 7/14 = 50.0% (26.8–73.2%) | 3/13 = 23.1% (8.2–50.3%) | 21.2% |
| band t1_10 | 3/24 = 12.5% (4.3–31.0%) | 3/24 = 12.5% (4.3–31.0%) | 5/24 = 20.8% (9.2–40.5%) | 3/20 = 15.0% (5.2–36.0%) | 12.0% |
| band t0_1 | 1/18 = 5.6% (1.0–25.8%) | 1/18 = 5.6% (1.0–25.8%) | 3/18 = 16.7% (5.8–39.2%) | 1/16 = 6.2% (1.1–28.3%) | 5.2% |
| band zero | 0/4 = 0.0% (0.0–49.0%) | 0/4 = 0.0% (0.0–49.0%) | 0/4 = 0.0% (0.0–49.0%) | 0/4 = 0.0% (0.0–49.0%) | 0% |

## T4 Effective annual admin fee, bps of balance: median (p25-p75; n)

| Sponsors with a 2021+ rate | n | $25k bps | $100k bps | $500k bps | Min annual fee $ (where stated) |
|---|---|---|---|---|---|
| All | 7 | 150 (138–175; n=7) | 150 (138–175; n=7) | 150 (112–175; n=7) | 250 (200–250; n=3) |
| CFs | 6 | 150 (131–150; n=6) | 150 (131–150; n=6) | 138 (106–150; n=6) | 250 (200–250; n=3) |
| Non-CF | 1 | 200 (200–200; n=1) | 200 (200–200; n=1) | 200 (200–200; n=1) | – |

| Group | Opening minimum stated | Opening minimum $ |
|---|---|---|
| All 60 | 13/60 | 5,000 (2,500–10,000; n=13) |
| CFs | 11/31 | 5,000 (3,750–10,000; n=11) |

## T5 Tail CFs vs top-100 CF census (top-100 recomputed at the same balances)

| Measure | Tail CFs (this sample) | Top-100 CFs (cf-daf-fee-census-2026.csv, as filed) |
|---|---|---|
| CFs | 31 | 100 |
| 2021+ balance-based schedule published | 6/31 = 19.4% (9.2–36.3%) | 34/100 = 34.0% (25.5–43.7%) |
| Any fee term / schedule (incl. pre-2021, partial) | 12/31 = 38.7% (23.7–56.2%) | 52/100 = 52.0% (42.3–61.5%) |
| Admin bps at $25k | 150 (131–150; n=6) | 118 (100–188; n=34) |
| Admin bps at $100k | 150 (131–150; n=6) | 100 (100–125; n=34) |
| Admin bps at $500k | 138 (106–150; n=6) | 100 (100–125; n=34) |
| Min annual fee $ (where stated) | 250 (200–250; n=3) | 250 (250–500; n=24) |
| Opening minimum $ (where stated) | 5,000 (3,750–10,000; n=11) | 15,000 (10,000–25,000; n=19) |

## T6 Sponsors publishing any fee term

| EIN | Sponsor | Type|band | Status | Tiers | Min fee $ | Opening min $ | $25k | $100k | $500k | Source date |
|---|---|---|---|---|---|---|---|---|---|---|
| 911726410 | WHATCOM COMMUNITY FOUNDATION | cf|t10_50 | published_schedule | 0-500,000: 2.0%; 500,000-1,000,000: 1.5%; 1,000,000-5,000,000: 1.25%; 5,000,000-: 1.0% | – | 5000 | 200.0 | 200.0 | 200.0 | live 2026-11-19; Non-Endowed Terms & Conditions 'Last Updated: 12/31/2025' |
| 481076910 | HUTCHINSON COMMUNITY FOUNDATION | cf|t10_50 | published_schedule | 0-2,000,000: 1.25%; 2,000,000-5,000,000: 0.75%; 5,000,000-15,000,000: 0.5%; 15,000,000-: 0.25% | 250 | 0 | 125.0 | 125.0 | 125.0 | 2023 schedule (file name), uploaded 2025-02 |
| 751709180 | COMMUNITY FOUNDATION OF WEST TEXAS | cf|t10_50 | published_pre2021 | 0-: 1.0% | – | 5000 | 100.0 | 100.0 | 100.0 | 'Revised 12/01/16' (live 2026-11-19, linked from /fund-types) |
| 521326014 | COMMUNITY FOUNDATION OF THE EASTERN SHOR | cf|t10_50 | published_unread | – | – | 5000 | – | – | – | live 2026-11-19 |
| 841339670 | PIKES PEAK COMMUNITY FOUNDATION | cf|t10_50 | published_schedule | 0-3,000,000: 1.5%; 3,000,000-5,000,000: 1.5%; 5,000,000-10,000,000: 0.75%; 10,000,000-: 0.25% | 250 | – | 150.0 | 150.0 | 150.0 | uploaded 2025-01 (wp-content path) |
| 311760702 | LICKING COUNTY FOUNDATION INC | cf|t10_50 | partial | – | – | 25000 | – | – | – | undated PDF (Donor Advised Fund Guide), live 2026-11-19 |
| 680330462 | COMMUNITY FOUNDATION OF MENDOCINO COUNTY | cf|t1_10 | partial | – | – | 10000 | – | – | – | live 2026-11-19 (the .doc is undated) |
| 920139183 | HOMER FOUNDATION | cf|t1_10 | published_schedule | 0-1,000,000: 1.5%; 1,000,000-: 1.25% | 150 | 10000 | 150.0 | 150.0 | 150.0 | Funds Policy #01-01 v.1.27.21 / 1.28.21 (January 2021) |
| 266394395 | THE ADIRONDACK TRUST COMPANY | cf|t1_10 | published_no_admin_fee | 0-: 0.0% | – | 5000 | 0.0 | 0.0 | 0.0 | live 2026-11-19 (undated page) |
| 311040215 | ATHENS COUNTY FOUNDATION | cf|t1_10 | published_schedule | 0-500,000: 1.5%; 500,000-: 1.0% | – | 10000 | 150.0 | 150.0 | 100.0 | live 2026-11-19 (undated page) |
| 390827885 | COMMUNITY FOUNDATION OF CENTRAL | cf|t1_10 | partial | – | – | 1000 | – | – | – | live 2026-11-19 |
| 421495980 | COMMUNITY FOUNDATION OF GREATER | cf|t0_1 | published_unread | – | – | 2500 | – | – | – | undated DAF guidelines PDF, live 2026-11-19 |
| 472525808 | GLOBALTRUST FUNDS | single_issue|t0_1 | partial | – | – | – | – | – | – | live 2026-11-19; forms uploaded 2024-07 |
| 050259003 | JEWISH FEDERATION FOUNDATION OF GREATER | faith|t10_50 | partial | – | – | 2500 | – | – | – | live 2026-11-19 |
| 832300241 | CAL POLY POMONA PHILANTHROPIC FOUNDATION | other|t0_1 | published_schedule | 0-: 2.0% | – | 100000 | 200.0 | 200.0 | 200.0 | undated policy (worked example dated June 15, 2021), live 2026-11-19 |

## T7 Published fee at the sponsor's own FY2024 average account vs allocated operating cost per account

| Rule | n with fee and allocated cost | Fee >= allocated cost per account | Fee / cost, median (IQR) |
|---|---|---|---|
| A | 7 | 1 of 7 | 0.52 (0.36–0.66) |
| G | 5 | 0 of 5 | 0.22 (0.09–0.35) |
| AM | 7 | 4 of 7 | 1.18 (0.43–2.02) |

| EIN | Sponsor | Status | Avg account $ | Fee at avg $ | Fee bps | Cost bps A / G / AM | Cost per account A / G / AM $ | Covers A/G/AM |
|---|---|---|---|---|---|---|---|---|
| 911726410 | WHATCOM COMMUNITY FOUNDATION | published_schedule | 133370 | 2667 | 200.0 | 383 / 2275 / 113 | 5105 / 30344 / 1507 | no/no/yes |
| 481076910 | HUTCHINSON COMMUNITY FOUNDATION | published_schedule | 409491 | 5119 | 125.0 | 101 / 353 / 55 | 4117 / 14450 / 2242 | yes/no/yes |
| 841339670 | PIKES PEAK COMMUNITY FOUNDATION | published_schedule | 262074 | 3931 | 150.0 | 217 / 375 / 127 | 5695 / 9826 / 3320 | no/no/yes |
| 920139183 | HOMER FOUNDATION | published_schedule | 110443 | 1657 | 150.0 | 389 / – / 383 | 4293 / – / 4235 | no/–/no |
| 266394395 | THE ADIRONDACK TRUST COMPANY | published_no_admin_fee | 198266 | 0 | 0.0 | 41 / 44 / 70 | 822 / 872 / 1385 | no/no/no |
| 311040215 | ATHENS COUNTY FOUNDATION | published_schedule | 173340 | 2600 | 150.0 | 460 / 694 / 313 | 7978 / 12029 / 5427 | no/no/no |
| 832300241 | CAL POLY POMONA PHILANTHROPIC FOUNDATION | published_schedule | 28302 | 566 | 200.0 | 321 / 0 / 77 | 910 / 0 / 217 | no/–/yes |

## T8 Allocated operating cost of the sampled sponsors (long-tail cost study)

| Group | n | Rule A bps | Rule G bps | AM bps | Rule A $/account |
|---|---|---|---|---|---|
| Sampled CFs, 2021+ rate published | 6 | 300 (130–387; n=6) | 375 (353–694; n=5) | 120 (81–266; n=6) | 4,699 (4,161–5,547; n=6) |
| Sampled CFs, no 2021+ rate | 25 | 181 (121–313; n=22) | 200 (95–735; n=21) | 49 (41–137; n=22) | 2,683 (1,420–4,020; n=21) |
| Sampled non-CF | 29 | 547 (107–2,479; n=24) | 289 (109–2,625; n=21) | 107 (73–334; n=24) | 2,212 (838–23,605; n=19) |

## T9 Share of all tail CFs whose allocated cost per DAF dollar is at or below a given fee (100 bps = top-100 median; middle cut = this sample's tail-CF median at $100k)

| All usable tail CFs in the cost study | cost <= 100 bps | cost <= 150 bps | cost <= 200 bps |
|---|---|---|---|
| Rule A | 92/603 = 15.3% (12.6–18.3%) | 203/603 = 33.7% (30.0–37.5%) | 294/603 = 48.8% (44.8–52.7%) |
| Rule G | 104/579 = 18.0% (15.0–21.3%) | 158/579 = 27.3% (23.8–31.1%) | 213/579 = 36.8% (33.0–40.8%) |
| Rule AM | 337/603 = 55.9% (51.9–59.8%) | 456/603 = 75.6% (72.0–78.9%) | 511/603 = 84.7% (81.7–87.4%) |
