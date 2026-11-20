# P-B4501-01: a larger tail community-foundation fee sample (60 more CFs)

**Date:** 2026-11-20 · **Task id:** b4501-01 · **Queue item:** P-B4501-01 (enlarge the tail-CF fee sample of `b45n33-01-long-tail-fee-census.md` §2.2 and §2.4, whose tail-CF medians rested on 6 schedules)

**Outputs**
- [`scripts/mission_b4501_01_tail_cf_fees.py`](../../scripts/mission_b4501_01_tail_cf_fees.py): a wrapper. It is stdlib only and written in a functional style. It imports `scripts/mission_long_tail_fee_census.py` and does not modify it. Reused unchanged: frame, strata, allocation, the original draw, the robots-checked crawler and fetcher (user agent `research-script/1.0`), the fee engine, the quote verifier and the Wilson intervals. Tasks are `sample`, `crawl`, `fetch`, `hits`, `robots` and `census`. `python3 -I scripts/mission_b4501_01_tail_cf_fees.py . --task census --cache-dir CACHE` writes the CSV and prints every table in the Appendix.
- [`data/mission-2026-11-14/tail-cf-fee-sample-2026-11-20.csv`](../../data/mission-2026-11-14/tail-cf-fee-sample-2026-11-20.csv): 60 rows, one per newly drawn CF. The data dictionary is in §6.
- [`data/mission-2026-11-14/queue-proposals-b4501-01.csv`](../../data/mission-2026-11-14/queue-proposals-b4501-01.csv): 5 follow-ups.
- No existing file was edited. The base census CSV was not rewritten.

**Labels:** **[F]** transcribed from a sponsor document (each quote verified against the cached text by the script); **[C]** script computation; **[I]** inference. This is research, not legal, tax or accounting advice.

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **Does the tail-CF median now rest on 20+ schedules?** | **Yes: exactly 20.** That is the 6 original schedules plus 14 new ones: 13 rates and 1 stated 0% (New Bremen) [C]. | High on the count |
| **New medians (extension alone, n = 14)** | **112.5 bps at $25k, $100k and $500k.** Bootstrap 95% interval: 100–150 at each balance. The design-weighted median is 100 / 100 / 100. Range: 0 (New Bremen) to 200 (Wichita and Skagit at $25k). Five of the 14 are a flat 100 bps at all three balances: Dubois, Yampa Valley, Horizon, Marion and Western Indiana [C]. | Medium |
| **Pooled with the original 6 (n = 20)** | **137.5 / 137.5 / 125 bps** at $25k / $100k / $500k. Bootstrap 95% interval: 100–150 at each balance. The design-weighted median is 150 / 150 / 125. Excluding the two 0% schedules (n = 18), the medians are 150 / 150 / 128. The original 6 alone were 150 / 150 / 138 [C]. | Medium |
| **What changed** | The new wave is cheaper than the original 6, and **the tail-CF median at $100k falls from 150 to about 138 bps.** Its bootstrap interval now reaches down to the top-100 CF median (100 bps), so "tail CFs charge more than the top 100" is **no longer established**. Read it as "about the same to somewhat higher" [C; I]. | Medium |
| **Found-schedule rate** | Extension: **14/60 = 23.3%** (Wilson 14.4–35.4%; bootstrap 13.3–35.0%). On readable sites: 14/53 = 26.4%. Pooled 91 CFs: **20/91 = 22.0%** (Wilson 14.7–31.5%). On readable sites: 20/79 = 25.3%. The design-weighted pooled rate is also 22.0%. Any fee term or linked schedule: extension 27/60 = 45.0%; pooled 39/91 = 42.9% [C]. | High on counts |
| **Share of tail CFs with no public fee schedule** | Of readable sites, **extension 38/53 = 71.7%** (Wilson 58.4–82.0%; bootstrap 58.5–83.0%). Pooled: **55/79 = 69.6%** (Wilson 58.8–78.7%). Counting unreadable sites as "no schedule seen", the shares are 45/60 = 75.0% and 67/91 = 73.6%. "No public schedule" here means `partial`, `no_published_fee` or `no_website_found` [C]. | Medium (crawl-based; §4) |
| **By size (extension)** | 2021+ rate found: 6/19 in the $10–50m band, 7/26 in $1–10m and 1/14 under $1m (31.6%, 26.9%, 7.1%). This has the same direction as the original census [C]. | Medium |
| **Realised tail-CF fee pool (~$49m)** | **Unchanged at $49.4m.** The b4427b-0405 pool is built from Form 990 all-fund fee rates and does not use published schedules, so a larger schedule sample cannot move it [C]. Two related figures do move:<br>(a) **Schedule ceiling.** The flat schedule-based CF ceiling at the pooled median falls to **$83.9m** (bootstrap $61.0m–$91.5m), from $89.9m at 147 bps [C].<br>(b) **Sensitivity [I].** 18 of the 20 sampled publishers carry a band-median *imputed* realised rate (median 111.7 bps), against a median published fee of 149 bps at their own average account. 10 of the 14 new publishers show no fee line on the 990 at all. Substituting the published fee for the imputation adds $1.25m in the sample, or **+$8.9m design-weighted (pool about $58m)**. This is not proposed as a revision: it mixes list prices with realised amounts. It does suggest the 990 capture rule may understate realised fees (P-B450101-04). | Medium on (a); low on (b) |
| **Opening minimums** | Extension median **$10,000** (n = 13; bootstrap $10,000–$25,000), against $5,000 for the original 11. Pooled: $10,000 (n = 24) [C]. | Medium |

---

## 1. Method

### 1.1 Draw [C]
- **Frame.** The 641 tail CFs: `community_foundation` rows of `daf-long-tail-sponsors-fy2021-2024.csv` in bands `t10_50`, `t1_10`, `t0_1` and `zero`. These come from the base `tail_frame`.
- **Exclusions.** The 31 CFs of the original draw (base `draw`, seed 20261119) are removed.
- **Allocation.** n = 60 over the four CF strata, using the base `allocate()` on the remaining sizes: proportional, floor 1, largest remainder. The result is 19 / 26 / 14 / 1.
- **Seed scheme.** Within stratum i (the same index as in the base 16-cell list, 0–3), the draw is `random.Random(20261120 + i).sample(remaining rows sorted by EIN, a_i)`. The base used `20261119 + i`. A new base seed is used so the extension is not correlated with the original selection, and the draw is reproducible (`--task sample`).
- **Weights.** Extension weights are N/n_ext (10.5–12). Pooled weights are N/(n_orig + n_ext) (6.0–7.1). Both are close to proportional, so the weighted and unweighted rates agree (22.0%). See table E1.

### 1.2 Websites
- **Source.** Homepages come from `cf-vendor-map-by-ein-v2.csv`, which is the 990 `WebsiteAddressTxt`. 55 of 60 CFs have one.
- **No homepage.** For the other five (Oahe, Keokuk Area, Edwardsville, Community Foundation Realty, Devils Lake Area), web search was used only to look for an official site. None was found; only third-party listings and Keokuk's issuu brochures came up. All five are `no_website_found`.
- **Alternate host spellings.** Three 990 hosts failed TLS, and an alternate spelling of the same domain was used after its own robots check:
  - Marion: `marioncommunityfoundation.org` (certificate name mismatch on `www`);
  - CF Partnership: `www.cfpartner.org`, the redirect target;
  - Montrose: robots.txt read over `http`.

  Greater Taylor serves a self-signed certificate. TLS verification was not disabled, so that site is `site_unreachable`.

### 1.3 Crawl, robots.txt and manual follow-up [F]
1. **Robots first.** The base `crawl_site` reads robots.txt on every host before any page. It logs the verdict per URL, treats 401/403 as disallowed, and does not change the user agent. It then fetches the homepage, sitemap.xml and its page sub-sitemaps, and up to 16 fee-related candidate pages.
2. **Manual follow-up**, as in base §1.3 step 3:
   - The crawler's link filter missed many generic paths (`/give`, `/donors`, `/advise`, Wix and Squarespace pages). For every site without a fee result, up to 8 more same-site pages were fetched through the base `raw_get` (robots-checked). They were picked from the sitemap and the anchors (donor-advised, open/start/establish a fund, fund types, fees, policies, FAQ, give).
   - Fee and minimum contexts were then read by hand.
   - Source documents were re-fetched with the base `fetch_one` for quote verification.
3. **Robots log.** Every host touched is listed with its logged verdict in Appendix R (81 hosts). Outcomes:
   - One host disallows everything: `www.montrosecf.com` ("User-agent: * Disallow: /").
   - One off-site file host returns 403 on robots.txt: `cdn.prod.website-files.com`, the Boreal Waters fee PDF. Nothing was fetched from either.
   - Four hosts logged robots.txt "-1" (connection failure): `cfpartner.org`, `greatertaylorfoundation.org`, `www.marioncommunityfoundation.org`, `www.brooklinecommunity.org`. On the first three the page fetch failed too (TLS), so nothing was read there.
   - For `www.brooklinecommunity.org`, robots.txt timed out but the homepage then loaded. The base code treats an unreachable robots.txt as "allowed". robots.txt on both Brookline hosts was re-read on 2026-11-20 (200, allowed for `research-script/1.0`) before the fee page was used.
4. **Bot-verification pages.** These are new to this wave. Four hosts (Sturgis, Erie County OH, CF of Southern Wisconsin, Rhinelander) answered `research-script/1.0` with "Please wait while your request is being verified". robots.txt allows all four. They are coded `bot_challenge` and treated as unknown, like `robots_blocked`. No other agent was tried.
5. **Search engine.** Used only to look for the five missing homepages. No figure comes from search.

### 1.4 Status codes
These are the base codes (base §1.4) plus two unknowns:
- `bot_challenge`: a verification page instead of content.
- `site_unreachable`: TLS failure, or HTTP 500 on every inner page (Knox County OH).

"Readable sites" excludes `robots_blocked`, `bot_challenge` and `site_unreachable`.

**2021+ rule.** CF Partnership's only fee terms (a $25,000 DAF minimum and a reference to a fee schedule) are in a Gifts Acceptance Policy "Revised August 12, 2016". It is therefore coded `no_published_fee`, not `partial`.

### 1.5 Fee computation and statistics [C]
- **Fee engine.** The base engine (`effective_admin_fee`) is used at constant $25k, $100k and $500k balances: marginal or flat_on_total tiers, then the minimum annual fee, then any flat fee. Gift, grant and investment fees are recorded as text and excluded.
- **Medians.** Plain medians, as in the base census.
- **Bootstrap.** Percentile bootstrap of the median: 10,000 resamples with replacement, seed 4501, 2.5th–97.5th percentiles.
- **Shares.** Wilson 95% intervals, plus the same bootstrap.
- **Design-weighted medians.** The lower weighted median with N/(n_orig + n_ext) weights.
- **Original rows.** The 6 original schedules are read from `long-tail-fee-census-2026-11-19.csv` as filed (the base interpretation choices: Whatcom 2.00%, Athens band rate, Pikes Peak non-endowed).

### 1.6 Pools [C on stated assumptions]
- **Realised pool.** The sum of `pool_central_usd` over the 641 `B_tail_cf` rows of `tail-realised-fees-all-2026-11-20.csv` (b4427b-0405).
- **Flat schedule ceiling.** Pooled published median at $100k × FY2024 tail-CF DAF assets ($6,101.3m).
- **Sensitivity.** For sampled 2021+ publishers whose realised `pool_rate_bps` is a band-median imputation (no internal fee observed), the published fee at the CF's own FY2024 average account replaces the imputed rate on its DAF assets. The change is summed in the sample and design-weighted to the 641 CFs.

---

## 2. Results

### 2.1 Publication (E2, E3)

| Group | n | 2021+ rate found | Readable sites | Any fee term | No public schedule (readable) |
|---|---|---|---|---|---|
| Extension | 60 | 14 (23.3%; 14.4–35.4%) | 14/53 (26.4%) | 27 (45.0%) | 38/53 (71.7%; 58.4–82.0%) |
| Original CFs | 31 | 6 (19.4%; 9.2–36.3%) | 6/26 (23.1%) | 12 (38.7%) | 17/26 (65.4%) |
| **Pooled** | **91** | **20 (22.0%; 14.7–31.5%)** | **20/79 (25.3%)** | **39 (42.9%)** | **55/79 (69.6%; 58.8–78.7%)** |

- **[C] Status counts in the extension:**
  - 13 published schedules and 1 stated 0%;
  - 2 linked but unreadable schedules (Juneau, Boreal Waters/Duluth);
  - 11 partial (an opening minimum, or a fee described but not quantified);
  - 21 read with no DAF fee or minimum;
  - 5 with no website;
  - 7 unknown: 1 robots-blocked, 4 bot challenges, 2 unreachable.
- **[C] The two waves agree on publication.** 19.4% and 23.3%, with overlapping intervals. The pooled 22.0% is the better estimate, and its interval (14.7–31.5%) is about 40% narrower than the original 9.2–36.3%.
- **[C] Size gradient.** In the extension the found-schedule rate is 31.6% ($10–50m), 26.9% ($1–10m) and 7.1% (under $1m). Under $1m, 4 of 14 publish only a partial term (three a minimum) and 3 have no website.

### 2.2 Published schedules in the extension (E5)

| Sponsor (band) | Schedule [F] | Min fee | Opening min | $25k / $100k / $500k bps [C] | Source date |
|---|---|---|---|---|---|
| Wichita Foundation (KS, $10–50m) | Charitable Funds: 2.0% to $50k ($200 floor below $10k), 1.5% to $250k, 1.0% to $2.5m, then 0.75 / 0.50 / 0.35 / 0.25% | $200 | – | 200 / 175 / 130 | live, undated (page and PDF) |
| Humboldt Area Fdn (CA, $10–50m) | "The fee for most funds is currently 1.75% of the fund balance" | – | – | 175 / 175 / 175 | live, undated |
| Horizon Community Funds (KY, $10–50m) | 100 bps first $1m, 80 to $2.5m, 60 above | $250 | $25,000 | 100 / 100 / 100 | page modified 2025-07-18; 2025 PDF |
| Yampa Valley CF (CO, $10–50m) | DAF: 1% first $1m, 0.75% next $4m, 0.5% next $5m, 0.25% above | $250 | – | 100 / 100 / 100 | "10/25/22"; DAF policy May 2024 |
| Dubois County CF (IN, $10–50m) | Non-endowed DAF: 1% a year (plus a one-time 1% gift fee) | – | $10,000 | 100 / 100 / 100 | undated PDF |
| Marion CF (OH, $10–50m) | "administrative fee rate of 1.0% for all fund types" | – | – | 100 / 100 / 100 | live, undated |
| Skagit CF (WA, $1–10m) | DAF: 2% ($10k–99k), 1.75% ($100k–499k), 1.5% ($500k+) | – | – | 200 / 175 / 150 | undated PDF |
| CF Greater Rome (GA, $1–10m) | 1.5% first $1m, 1.0% to $5m, 0.75% above | $250 | $5,000 | 150 / 150 / 150 | "November 2025" |
| Brookline CF (MA, $1–10m) | DAF 1.5% a year; $250 minimum (non-endowed) | $250 | $5,000 | 150 / 150 / 150 | live; policies page 2026-01-21 |
| Benton CF (OR, $1–10m) | DAF: 1.25% first $2m, 0.75% above | – | – | 125 / 125 / 125 | agreement template, 2025-04 |
| Western Indiana CF (IN, $1–10m) | "Annual Rate: 1%" (all funds) | – | – | 100 / 100 / 100 | live, undated |
| Yellow Springs CF (OH, $1–10m) | DAF 0.50% a year (plus 0.50% on gifts granted at once) | – | – | 50 / 50 / 50 | Board approved 2026-06-22 |
| New Bremen Fdn (OH, $1–10m) | "underwrites its fund fees, so there is no cost to maintain the fund" | – | – | 0 / 0 / 0 | live, undated |
| Broomfield CF (CO, <$1m) | "Most Donor Advised Funds are charged an annual fee of 1.5%" | – | – | 150 / 150 / 150 | live, undated |

**Interpretation choices [C]:**
- **Skagit.** Read as a band rate on the whole balance. A marginal reading gives 200 / 200 / 180.
- **Brookline.** The non-endowed DAF is used. The endowed DAF has a $750 minimum fee, so it would be 300 bps at $25k.
- **Dubois.** The non-endowed DAF is used. The endowed DAF is also 1% to $1m.
- **Gift fees** (Dubois, Yellow Springs) are excluded, as in the base census.
- **"Most funds" or "most DAFs" wording** (Humboldt, Broomfield) is taken at face value.

### 2.3 Unreadable, partial and no-fee CFs [F]
- **Published but unread:**
  - **Juneau CF.** The advisor page says funds "have a modest administrative fee" and links "Philanthropic Fund Fee Schedule 2025". The PDF request returned a bot-verification page.
  - **Boreal Waters CF (Duluth-Superior).** The advisor page links "View fees PDF" on the Webflow CDN, whose robots.txt returns 403. The site gives a $25,000 DAF minimum.
- **Partial, with a stated opening minimum:**

  | CF | DAF opening minimum |
  |---|---|
  | Bryan Area | $100,000 (Donor Handbook 7-1-2026) |
  | Martha's Vineyard | $25,000 |
  | Stateline | $20,000 |
  | Rochester Area | $10,000 |
  | Placer | $10,000 |
  | Lenawee | $10,000 |
  | Albion | $10,000 minimum principal; an administrative distribution is described but not quantified |

- **Partial, fee described without a number:**
  - Kitsap: fees "available upon request".
  - Dunn County: "low administrative fees".
  - CF of Western Pennsylvania & Eastern Ohio: fees "among the lowest"; "no minimums to set up a fund".
  - Dublin: a minimum given only as an example ("e.g., $25,000").
- **No DAF fee or minimum on a readable site (21):** listed in the CSV with what was read. Examples: North Dakota CF, Savannah, Gratiot, Heart of Illinois, Hastings, Muncie, Steuben.

### 2.4 Pools (E7)
- **[C] Realised CF pool: $49.4m, unchanged.** It is computed from Form 990 fee lines (b4427b-0405), not from schedules.
- **[C] Flat schedule ceiling: $83.9m** at the pooled 137.5 bps on $6,101.3m (bootstrap $61.0m–$91.5m). This replaces the b4501-04 CFs-only central of $89.9m (147 bps). The upper bound (150 bps) is about where the old central was. The lower bound is the top-100 median.
- **[I] Realised vs published.**
  - Only Hutchinson (original sample) has both a published rate and an observed internal fee (125 vs 83.2 bps).
  - The other 18 sampled publishers with an average-account figure carry an imputed band rate in the realised pool, a median 111.7 bps against a published median of 149 bps.
  - Substituting the published fee adds $1.25m in the sample and about **$8.9m design-weighted (about $58m)**.
  - This is a sensitivity, not a new estimate. A published rate is a list price; "most funds" wording and fee waivers mean the realised rate can be lower. The 990 capture rule also treats a CF that shows no fee line as unobserved, not as zero.
  - What it shows is that 10 of the 14 new publishers report no fee line on the 990 while publishing 50–200 bps. So the 990 is a weak instrument for realised DAF fees at small CFs (P-B450101-04).

---

## 3. What this changes in the repository (proposed, not applied)
1. **`b45n33-01-long-tail-fee-census.md` §0, §2.4 and T5.** The tail-CF medians "150 / 150 / 138 (n = 6)" become **137.5 / 137.5 / 125 (n = 20; bootstrap 100–150)**.
   - "Tail CFs publish less and charge more" becomes: they publish a little less (pooled 22.0% vs 34.0% of the top 100; the intervals overlap). On price they are about the same as the top 100 at $100k (137.5 vs 100), with a bootstrap interval that reaches 100.
   - The tail-CF publication rate becomes 20/91 = 22.0% (14.7–31.5%).
2. **`b4427b-0405` and `direction-long-tail-sponsors.md` §0.** The realised CF pool stays at about $49m. The schedule ceiling moves from about $90m to **about $84m** ($61m–$92m). The phrase "these figures rest on 6–7 schedules" can read "20 tail-CF schedules".
3. **`b4501-04-tail-fee-pool-revision.md`.** The population coverage tables (T9 there) used the 150 bps median. At 137.5 bps the coverage shares fall between that note's 100 and 150 bps columns. This was not recomputed here.

---

## 4. Limits
1. **n = 20 is still small.** The extension and the original 6 differ (112.5 vs 150 bps at $100k). Their bootstrap intervals overlap (100–150 and 62–175). The pooled interval (100–150) is narrower, but it spans the whole range between the top-100 median and the old tail median.
2. **"No public schedule" is a crawl result.**
   - JavaScript-only pages, image-only PDFs and pages reachable only by site search can hide fees.
   - Several sites (Wix, Squarespace) expose little text. For some, the crawler's own filter found nothing, and only the manual follow-up (up to 8 extra pages) reached the fund pages.
   - The no-schedule share is an upper bound on true non-publication.
3. **12 of 91 pooled CFs are unknown:**
   - 6 robots-blocked: 5 original hosts plus Montrose;
   - 4 bot challenges;
   - 2 unreachable.

   A further 4 schedules are linked but unreadable. If the unknowns published at the readable-site rate, about 3 more schedules would exist [I].
4. **Dates.** Eight of the 14 new schedules are undated: six live pages (Wichita, Humboldt, Marion, Western Indiana, New Bremen, Broomfield) and two PDFs (Dubois, Skagit). The rest show a date:
   - Rome: November 2025;
   - Yellow Springs: June 2026;
   - Brookline: page updated 2026-01-21;
   - Horizon: 2025-07-18;
   - Benton: template uploaded 2025-04;
   - Yampa Valley: 10/25/22.

   One sponsor's only fee term was pre-2021 and was excluded (CF Partnership).
5. **Interpretation.** Skagit's band basis and the "most funds" wording at Humboldt and Broomfield are judgement calls (see §2.2). The pooled medians were not recomputed under the alternative readings.
6. **Constant-balance fees** exclude gift fees (Dubois 1%, Yellow Springs 0.5% on immediate grants), card fees and investment fees.
7. **Pools.** The realised pool uses all-fund 990 rates (b4427b-0405 §5). The flat ceiling applies one median to all assets and ignores tier breaks above $1m. The sensitivity in §2.4 is [I].
8. **Original rows** are taken from the base CSV as filed. The wave-34B reclassification there (Columbus Medical, a non-CF) does not affect CF figures.

---

## 5. Source register (primary URLs; retrieved 2026-11-20 by `research-script/1.0` after a robots.txt check)

| # | Sponsor (EIN) | URL | Used for |
|---|---|---|---|
| S1 | Dubois County CF (351990305) | https://www.dccommunityfoundation.org/s/Donor-Advised-Fund-Options-szda.pdf | Non-endowed 1% + 1% gift fee; $10,000 minimum |
| S2 | Yampa Valley CF (840794536) | https://yvcf.org/wp-content/uploads/2022/10/Professional-Services-Fee-Structure_10.25.22.pdf ; https://yvcf.org/wp-content/uploads/2025/12/DAF-Policies-and-Procedures-051724.pdf | DAF tiers, $250 minimum |
| S3 | Horizon Community Funds (821388190) | https://horizoncfnky.org/how-to-get-involved/types-of-giving/designated-funds/designated-funds-fee-schedule/ ; https://horizoncfnky.org/wp-content/uploads/2024/01/2025-Portfolio_Options_Fee_Schedule.pdf | Tiers, $250 minimum fee, $25,000 DAF minimum |
| S4 | Humboldt Area Fdn (237310660) | https://hafoundation.org/ways-to-support/giving-start-a-fund/ | 1.75% |
| S5 | Marion CF (314446189) | https://marioncommunityfoundation.org/resources/advisor-toolkit/ | 1.0% all funds |
| S6 | Wichita Foundation (481022361) | https://wichitafoundation.org/giving-and-investing/become-a-fund-holder ; https://wichitafoundation.org/assets/uploads/documents/WF_Support_Fee.pdf | Charitable-fund tiers, $200 floor |
| S7 | CF Greater Rome (474252695) | https://www.cffgr.org/s/Support-Fees-Minimums-12-2025.pdf | Tiers, $250 minimum fee, $5,000 minimum |
| S8 | Yellow Springs CF (237372791) | https://www.yscf.org/wp-content/uploads/2026/06/YSCF-Investment-Fee-Policy-2026-adopted.pdf | DAF 0.50% |
| S9 | Brookline CF (042103944) | https://brooklinecommunity.org/fund-fee-policy/ | DAF 1.5%, minimum fees, opening minimums |
| S10 | Benton CF (936022916) | https://bcfgives.org/wp-content/uploads/2025/04/BCF-Donor-Advised-Fund-Fund-Agreement-Template.pdf | DAF Schedule A |
| S11 | Western Indiana CF (351814927) | https://www.wicf-inc.org/administrative-fees | 1% |
| S12 | Skagit CF (911572414) | https://www.skagitcf.org/uploads/1/5/1/2/15121716/about_scf_fund_types.pdf | Band table |
| S13 | New Bremen Fdn (341837854) | https://www.newbremenfoundation.org/faq | No fund fees |
| S14 | Broomfield CF (841246756) | https://www.broomfieldfoundation.org/about/faqs | 1.5% |
| S15 | Juneau CF (522395867) | https://www.juneaucf.org/advisors/ (links Philanthropic-Fund-Fee-Schedule-2025.pdf, not readable) | Unread schedule |
| S16 | Boreal Waters / Duluth-Superior (411429402) | https://www.dsacommunityfoundation.com/giving/how-to-open-a-fund ; https://www.dsacommunityfoundation.com/giving/professional-advisor-services (links the CDN fee PDF, robots 403) | $25,000 minimum; unread schedule |
| S17 | Partial CFs | Lenawee https://lenaweecommunityfoundation.com/establish-a-fund/ ; Bryan https://www.bryanareafoundation.org/wp-content/uploads/2026/08/7-1-2026-DONOR-Handbook.pdf ; Rochester https://rochesterarea.org/giving/fundholder-resources/ ; Placer https://www.placercf.org/create-a-fund ; Kitsap https://www.kitsapfoundation.org/_files/ugd/a04714_d96affbd6e424ba3afe5b2e89d652998.pdf ; Dunn https://www.cfdunncounty.org/ ; Western PA & E Ohio https://www.comm-foundation.org/professional-advisors ; Martha's Vineyard https://marthasvineyardcf.org/donors/donors-faqs/ ; Albion https://albionfoundation.org/donate/establish-a-fund/ ; Dublin https://www.dublinfoundation.org/resources/establishing-a-donor-advised-fund/ ; Stateline https://statelinecf.org/give/ | Minimums and unquantified fees |
| S18 | CF Partnership (351889139) | https://www.cfpartner.org/s/Gift-Acceptance-Policy.pdf | 2016 policy (excluded) |
| R1 | Repo | `daf-long-tail-sponsors-fy2021-2024.csv`; `cf-vendor-map-by-ein-v2.csv`; `long-tail-fee-census-2026-11-19.csv`; `tail-realised-fees-all-2026-11-20.csv` | Frame, homepages, original 6, realised pool |

All quotes are in `FEES_EXT` in the script. 28 of 28 sponsors with quotes verify (`quote_check` "verified k/k").

---

## 6. Data dictionary: `tail-cf-fee-sample-2026-11-20.csv`

| Column | Meaning |
|---|---|
| `ein`, `name` | EIN and DAFRC name (long-tail file) |
| `sample` | `ext_b4501_01` (all rows) |
| `stratum`, `size_band_fy2024` | `cf|band`; FY2024 DAF size band |
| `stratum_N`, `stratum_n_orig`, `stratum_n_ext` | Frame size; CFs in the original draw; CFs in this draw |
| `weight_ext`, `weight_pooled` | N/n_ext; N/(n_orig+n_ext) |
| `daf_assets_fy2024`, `accounts_fy2024_screened`, `avg_account_fy2024` | From the long-tail file |
| `website` | Site used (the 990 homepage or the alternate host noted) |
| `fee_status` | Base codes plus `bot_challenge` and `site_unreachable` (§1.4) |
| `in_2021plus_distribution` | `yes` for `published_schedule` and `published_no_admin_fee` |
| `fee_basis`, `admin_tiers` | `marginal` / `flat_on_total`; tiers as `lower-upper: rate%` |
| `min_annual_fee_usd`, `flat_annual_fee_usd`, `opening_min_usd` | USD; opening 0 = "no minimum" stated; blank = not stated |
| `gift_fee`, `grant_fee`, `investment` | As published (text) |
| `admin_bps_25k/100k/500k` | Effective annual admin fee at a constant balance, bps [C] |
| `fee_bps_at_avg_account` | Same at the CF's own FY2024 average account [C] |
| `realised_capture`, `realised_internal_bps_ta`, `realised_visible_bps_ta`, `realised_pool_rate_bps` | Joined from `tail-realised-fees-all-2026-11-20.csv` (b4427b-0405) |
| `source_url`, `source_date` | Primary document and the date it shows |
| `robots` | robots.txt verdict for the source (or the homepage) |
| `quote_check` | Script verification of the transcribed quotes |
| `notes` | What was read and the interpretation choices |

---

## Appendix: script output (`--task census`)

## E1 Extension design

| Stratum | Frame N | Original n | Remaining | Extension n | Weight (ext) | Weight (pooled) |
|---|---|---|---|---|---|---|
| cf|t10_50 | 207 | 10 | 197 | 19 | 10.895 | 7.138 |
| cf|t1_10 | 272 | 13 | 259 | 26 | 10.462 | 6.974 |
| cf|t0_1 | 150 | 7 | 143 | 14 | 10.714 | 7.143 |
| cf|zero | 12 | 1 | 11 | 1 | 12.000 | 6.000 |

## E2 Fee status

| Group | n | published_schedule | published_no_admin_fee | published_pre2021 | published_unread | partial | no_published_fee | no_website_found | robots_blocked | bot_challenge | site_unreachable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Extension (60) | 60 | 13 | 1 | 0 | 2 | 11 | 21 | 5 | 1 | 4 | 2 |
| Original CFs (31) | 31 | 5 | 1 | 1 | 2 | 3 | 13 | 1 | 5 | 0 | 0 |
| Pooled CFs (91) | 91 | 18 | 2 | 1 | 4 | 14 | 34 | 6 | 6 | 4 | 2 |
| ext band t10_50 | 19 | 6 | 0 | 0 | 2 | 4 | 4 | 1 | 0 | 1 | 1 |
| ext band t1_10 | 26 | 6 | 1 | 0 | 0 | 3 | 12 | 1 | 0 | 2 | 1 |
| ext band t0_1 | 14 | 1 | 0 | 0 | 0 | 4 | 4 | 3 | 1 | 1 | 0 |
| ext band zero | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

## E3 Found-schedule rate and no-public-schedule share

| Group | 2021+ rate found (all) | 2021+ rate found (readable sites) | Any fee term or linked schedule | No public fee schedule (readable sites) | No public fee schedule incl. unreadable |
|---|---|---|---|---|---|
| Extension (60) | 14/60 = 23.3% (Wilson 14.4–35.4%; bootstrap 13.3–35.0%) | 14/53 = 26.4% (Wilson 16.4–39.6%; bootstrap 15.1–39.6%) | 27/60 = 45.0% (Wilson 33.1–57.5%; bootstrap 31.7–58.3%) | 37/53 = 69.8% (Wilson 56.5–80.5%; bootstrap 56.6–81.1%) | 44/60 = 73.3% (Wilson 61.0–82.9%; bootstrap 61.7–83.3%) |
| Original CFs (31) | 6/31 = 19.4% (Wilson 9.2–36.3%; bootstrap 6.5–35.5%) | 6/26 = 23.1% (Wilson 11.0–42.1%; bootstrap 7.7–38.5%) | 12/31 = 38.7% (Wilson 23.7–56.2%; bootstrap 22.6–54.8%) | 17/26 = 65.4% (Wilson 46.2–80.6%; bootstrap 46.2–84.6%) | 22/31 = 71.0% (Wilson 53.4–83.9%; bootstrap 54.8–87.1%) |
| Pooled CFs (91) | 20/91 = 22.0% (Wilson 14.7–31.5%; bootstrap 14.3–30.8%) | 20/79 = 25.3% (Wilson 17.0–35.9%; bootstrap 16.5–35.4%) | 39/91 = 42.9% (Wilson 33.2–53.1%; bootstrap 33.0–52.7%) | 54/79 = 68.4% (Wilson 57.5–77.6%; bootstrap 58.2–78.5%) | 66/91 = 72.5% (Wilson 62.6–80.6%; bootstrap 63.7–81.3%) |
| ext band t10_50 | 6/19 = 31.6% (Wilson 15.4–54.0%; bootstrap 10.5–52.6%) | 6/17 = 35.3% (Wilson 17.3–58.7%; bootstrap 11.8–58.8%) | 12/19 = 63.2% (Wilson 41.0–80.9%; bootstrap 42.1–84.2%) | 9/17 = 52.9% (Wilson 31.0–73.8%; bootstrap 29.4–76.5%) | 11/19 = 57.9% (Wilson 36.3–76.9%; bootstrap 36.8–78.9%) |
| ext band t1_10 | 7/26 = 26.9% (Wilson 13.7–46.1%; bootstrap 11.5–46.2%) | 7/23 = 30.4% (Wilson 15.6–50.9%; bootstrap 13.0–52.2%) | 10/26 = 38.5% (Wilson 22.4–57.5%; bootstrap 19.2–57.7%) | 16/23 = 69.6% (Wilson 49.1–84.4%; bootstrap 47.8–87.0%) | 19/26 = 73.1% (Wilson 53.9–86.3%; bootstrap 53.8–88.5%) |
| ext band t0_1 | 1/14 = 7.1% (Wilson 1.3–31.5%; bootstrap 0.0–21.4%) | 1/12 = 8.3% (Wilson 1.5–35.4%; bootstrap 0.0–25.0%) | 5/14 = 35.7% (Wilson 16.3–61.2%; bootstrap 14.3–57.1%) | 11/12 = 91.7% (Wilson 64.6–98.5%; bootstrap 75.0–100.0%) | 13/14 = 92.9% (Wilson 68.5–98.7%; bootstrap 78.6–100.0%) |
| ext band zero | 0/1 = 0.0% (Wilson 0.0–79.3%; bootstrap 0.0–0.0%) | 0/1 = 0.0% (Wilson 0.0–79.3%; bootstrap 0.0–0.0%) | 0/1 = 0.0% (Wilson 0.0–79.3%; bootstrap 0.0–0.0%) | 1/1 = 100.0% (Wilson 20.7–100.0%; bootstrap 100.0–100.0%) | 1/1 = 100.0% (Wilson 20.7–100.0%; bootstrap 100.0–100.0%) |

Design-weighted 2021+ rate, pooled 91 CFs (weights N/(n_orig+n_ext)): 22.0%

## E4 Effective annual admin fee, bps: median (95% percentile bootstrap, 10,000 draws, seed 4501)

| Set | n | $25k | $100k | $500k | IQR $100k | Design-weighted median $25k / $100k / $500k |
|---|---|---|---|---|---|---|
| Extension only | 14 | 112 (100–150) | 112 (100–150) | 112 (100–150) | 112 (100–150; n=14) | 100 / 100 / 100 |
| Original 6 | 6 | 150 (62–175) | 150 (62–175) | 138 (50–175) | 150 (131–150; n=6) | 150 / 150 / 150 |
| Pooled | 20 | 138 (100–150) | 138 (100–150) | 125 (100–150) | 138 (100–150; n=20) | 150 / 150 / 125 |
| Pooled, excl. 0% schedules | 18 | 150 (100–150) | 150 (100–150) | 128 (100–150) | 150 (100–150; n=18) | 150 / 150 / 130 |

## E5 Extension CFs publishing any fee term

| EIN | Sponsor | Band | Status | Tiers | Min fee $ | Opening min $ | $25k | $100k | $500k | Realised internal bps | Source date | Quotes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 522395867 | JUNEAU COMMUNITY FOUNDATION | t10_50 | published_unread | – | – | – | – | – | – | – | live 2026-11-20; linked 'Philanthropic Fund Fee Schedule 2025' (wp-content upload 2025-02) | verified 2/2 |
| 386095474 | LENAWEE COMMUNITY FOUNDATION | t10_50 | partial | – | – | 10000 | – | – | – | – | live 2026-11-20 | verified 1/1 |
| 351990305 | DUBOIS COUNTY COMMUNITY FOUNDATION | t10_50 | published_schedule | 0-: 1.0% | – | 10000 | 100.0 | 100.0 | 100.0 | – | undated PDF, live 2026-11-20 | verified 4/4 |
| 840794536 | YAMPA VALLEY COMMUNITY FOUNDATION | t10_50 | published_schedule | 0-1,000,000: 1.0%; 1,000,000-5,000,000: 0.75%; 5,000,000-10,000,000: 0.5%; 10,000,000-: 0.25% | 250 | – | 100.0 | 100.0 | 100.0 | – | '10/25/22' (fee structure); DAF policy 'Board Approved May 17, 2024' points to it | verified 4/4 |
| 821388190 | Horizon Community Funds of Northern | t10_50 | published_schedule | 0-1,000,000: 1.0%; 1,000,000-2,500,000: 0.8%; 2,500,000-: 0.6% | 250 | 25000 | 100.0 | 100.0 | 100.0 | – | page modified 2025-07-18; '2025-Portfolio_Options_Fee_Schedule.pdf' | verified 5/5 |
| 251407396 | COMMUNITY FOUNDATION OF WESTERN | t10_50 | partial | – | – | 0 | – | – | – | – | live 2026-11-20 | verified 2/2 |
| 411429402 | DULUTH-SUPERIOR AREA COMMUNITY | t10_50 | published_unread | – | – | 25000 | – | – | – | – | live 2026-11-20 (now Boreal Waters CF); fee PDF on cdn.prod.website-files.com | verified 1/1 |
| 237041310 | BRYAN AREA FOUNDATION INC | t10_50 | partial | – | – | 100000 | – | – | – | – | Donor Handbook dated 7-1-2026 (upload 2026-08) | verified 2/2 |
| 416017740 | ROCHESTER AREA FOUNDATION | t10_50 | partial | – | – | 10000 | – | – | – | – | live 2026-11-20 | verified 1/1 |
| 237310660 | HUMBOLDT AREA FOUNDATION | t10_50 | published_schedule | 0-: 1.75% | – | – | 175.0 | 175.0 | 175.0 | – | live 2026-11-20 (undated page) | verified 2/2 |
| 314446189 | MARION COMMUNITY FOUNDATION | t10_50 | published_schedule | 0-: 1.0% | – | – | 100.0 | 100.0 | 100.0 | – | live 2026-11-20 (undated page) | verified 1/1 |
| 481022361 | WICHITA FOUNDATION | t10_50 | published_schedule | 0-50,000: 2.0%; 50,000-250,000: 1.5%; 250,000-2,500,000: 1.0%; 2,500,000-5,000,000: 0.75%; 5,000,000-10,000,000: 0.5%; 10,000,000-25,000,000: 0.35%; 25,000,000-: 0.25% | 200 | – | 200.0 | 175.0 | 130.0 | – | live 2026-11-20 (undated page and PDF) | verified 5/5 |
| 474252695 | COMMUNITY FOUNDATION OF GREATER ROME INC | t1_10 | published_schedule | 0-1,000,000: 1.5%; 1,000,000-5,000,000: 1.0%; 5,000,000-: 0.75% | 250 | 5000 | 150.0 | 150.0 | 150.0 | – | 'November 2025' (file name 12-2025) | verified 4/4 |
| 237372791 | YELLOW SPRINGS COMMUNITY FOUNDATION | t1_10 | published_schedule | 0-: 0.5% | – | – | 50.0 | 50.0 | 50.0 | – | 'Effective: June 2026 | Revised 2026 | Board Approved: June 22, 2026' | verified 2/2 |
| 201485011 | Placer Community Foundation | t1_10 | partial | – | – | 10000 | – | – | – | – | live 2026-11-20 | verified 1/1 |
| 042103944 | BROOKLINE COMMUNITY FOUNDATION INC | t1_10 | published_schedule | 0-: 1.5% | 250 | 5000 | 150.0 | 150.0 | 150.0 | – | live 2026-11-20 (policies page updated 2026-01-21) | verified 1/1 |
| 943205217 | KITSAP COMMUNITY FOUNDATION | t1_10 | partial | – | – | – | – | – | – | – | undated PDF, live 2026-11-20 | verified 1/1 |
| 936022916 | BENTON COMMUNITY FOUNDATION | t1_10 | published_schedule | 0-2,000,000: 1.25%; 2,000,000-: 0.75% | – | – | 125.0 | 125.0 | 125.0 | – | DAF agreement template uploaded 2025-04 | verified 4/4 |
| 351814927 | WESTERN INDIANA COMMUNITY | t1_10 | published_schedule | 0-: 1.0% | – | – | 100.0 | 100.0 | 100.0 | – | live 2026-11-20 (undated page) | verified 2/2 |
| 911572414 | THE SKAGIT COMMUNITY FOUNDATION | t1_10 | published_schedule | 0-100,000: 2.0%; 100,000-500,000: 1.75%; 500,000-: 1.5% | – | – | 200.0 | 175.0 | 150.0 | – | undated PDF, live 2026-11-20 | verified 4/4 |
| 341837854 | NEW BREMEN FOUNDATION INC | t1_10 | published_no_admin_fee | 0-: 0.0% | – | – | 0.0 | 0.0 | 0.0 | – | live 2026-11-20 (undated page) | verified 2/2 |
| 391819945 | COMMUNITY FOUNDATION OF DUNN COUNTY INC | t1_10 | partial | – | – | – | – | – | – | – | live 2026-11-20 | verified 1/1 |
| 842084322 | MARTHA'S VINEYARD COMMUNITY | t0_1 | partial | – | – | 25000 | – | – | – | – | live 2026-11-20 | verified 1/1 |
| 237019029 | ALBION COMMUNITY FOUNDATION | t0_1 | partial | – | – | 10000 | – | – | – | – | live 2026-11-20 | verified 2/2 |
| 200194557 | THE DUBLIN FOUNDATION | t0_1 | partial | – | – | – | – | – | – | – | live 2026-11-20 | verified 1/1 |
| 841246756 | BROOMFIELD COMMUNITY FOUNDATION | t0_1 | published_schedule | 0-: 1.5% | – | – | 150.0 | 150.0 | 150.0 | – | live 2026-11-20 (undated page) | verified 1/1 |
| 391585271 | THE STATELINE COMMUNITY FOUNDATION INC | t0_1 | partial | – | – | 20000 | – | – | – | – | live 2026-11-20 | verified 1/1 |

## E6 Opening minimum (where stated): median (bootstrap 95%)

| Set | n stating | Median $ |
|---|---|---|
| Extension | 13 | 10,000 (10,000–25,000) |
| Original CFs | 11 | 5,000 (2,500–10,000) |
| Pooled | 24 | 10,000 (5,000–10,000) |

## E7 Fee pools (tail CFs, FY2024 DAF assets)

| Measure | Value |
|---|---|
| Tail CF DAF assets FY2024 (641 CFs) | $6,101.3m |
| Realised all-fund pool, b4427b-0405 (sum of pool_central_usd; unchanged by this sample) | $49.4m |
| Pooled published median at $100k, bps (bootstrap 95%) | 138 (100–150) |
| Flat schedule ceiling at the pooled $100k median | $83.9m |
| Flat schedule ceiling, bootstrap bounds | $61.0m–$91.5m |

| Sensitivity (publishers with an imputed realised rate) | Value |
|---|---|
| n sampled 2021+ publishers with imputed realised rate | 18 |
| Median published fee at own avg account vs median imputed band rate, bps | 149 vs 111.7 |
| Sample-level change in pool if published fee replaces imputation | $+1.25m |
| Design-weighted to the 641 tail CFs (weights N/(n_orig+n_ext)) [I] | $+8.9m |
| Realised pool with that substitution [I] | $58.3m |

Publishers with an observed realised internal rate (b4427b-0405):

| Sponsor | Published bps at $100k | Realised internal bps of total assets |
|---|---|---|
| HUTCHINSON COMMUNITY FOUNDATION | 125 | 83.2 |


## Appendix R: robots.txt log (every host touched; first logged verdict, from the cache)

| Host | Verdict (user agent research-script/1.0) |
|---|---|
| albionfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| bcfgives.org | robots.txt 200: allowed for research-script/1.0 |
| brooklinecommunity.org | robots.txt 200: allowed for research-script/1.0 |
| buckscountyfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| cdn.prod.website-files.com | robots.txt 403: treated as disallowed |
| cfbmc.org | robots.txt 200: allowed for research-script/1.0 |
| cfdunncounty.org | robots.txt 200: allowed for research-script/1.0 |
| cfowc.org | robots.txt 200: allowed for research-script/1.0 |
| cfpartner.org | robots.txt -1: none published, fetch allowed |
| chesapeakecharities.org | robots.txt 200: allowed for research-script/1.0 |
| crawfordheritage.org | robots.txt 200: allowed for research-script/1.0 |
| greatertaylorfoundation.org | robots.txt -1: none published, fetch allowed |
| hafoundation.org | robots.txt 200: allowed for research-script/1.0 |
| horizoncfnky.org | robots.txt 200: allowed for research-script/1.0 |
| johnsoncenter.org | robots.txt 200: allowed for research-script/1.0 |
| lenaweecommunityfoundation.com | robots.txt 200: allowed for research-script/1.0 |
| marioncommunityfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| marthasvineyardcf.org | robots.txt 200: allowed for research-script/1.0 |
| mountdoracommunitytrust.com | robots.txt 200: allowed for research-script/1.0 |
| newbremenfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| rhinelandercommunityfoundation.com | robots.txt 200: allowed for research-script/1.0 |
| rochesterarea.org | robots.txt 200: allowed for research-script/1.0 |
| savfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| southmadisonfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| statelinecf.org | robots.txt 200: allowed for research-script/1.0 |
| sturgisfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| wichitafoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.albionfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.bcfgives.org | robots.txt 200: allowed for research-script/1.0 |
| www.borealwaters.org | robots.txt 200: allowed for research-script/1.0 |
| www.brooklinecommunity.org | robots.txt -1: none published, fetch allowed |
| www.broomfieldfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.bryanareafoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.buckscountyfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.cfbmc.org | robots.txt 200: allowed for research-script/1.0 |
| www.cfdunncounty.org | robots.txt 200: allowed for research-script/1.0 |
| www.cffgr.org | robots.txt 200: allowed for research-script/1.0 |
| www.cfmdin.org | robots.txt 200: allowed for research-script/1.0 |
| www.cfogd.org | robots.txt 200: allowed for research-script/1.0 |
| www.cfpartner.org | robots.txt 200: allowed for research-script/1.0 |
| www.cfsw.org | robots.txt 200: allowed for research-script/1.0 |
| www.chesapeakecharities.org | robots.txt 200: allowed for research-script/1.0 |
| www.comm-foundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.crawfordheritage.org | robots.txt 200: allowed for research-script/1.0 |
| www.cuerocommunityfoundation.com | robots.txt 200: allowed for research-script/1.0 |
| www.dccommunityfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.dsacommunityfoundation.com | robots.txt 200: allowed for research-script/1.0 |
| www.dublinfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.eriefoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.ggvcf.org | robots.txt 200: allowed for research-script/1.0 |
| www.gratiotfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.hafoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.hastingscommunityfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.heartofillinois.org | robots.txt 200: allowed for research-script/1.0 |
| www.horizoncfnky.org | robots.txt 200: allowed for research-script/1.0 |
| www.juneaucf.org | robots.txt 200: allowed for research-script/1.0 |
| www.kitsapfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.klamathcommunityfoundation.com | robots.txt 404: none published, fetch allowed |
| www.knoxcf.org | robots.txt 200: allowed for research-script/1.0 |
| www.lenaweecommunityfoundation.com | robots.txt 200: allowed for research-script/1.0 |
| www.marioncommunityfoundation.org | robots.txt -1: none published, fetch allowed |
| www.marthasvineyardcf.org | robots.txt 200: allowed for research-script/1.0 |
| www.merrick-foundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.merrickfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.montrosecf.com | robots.txt 200: disallowed for research-script/1.0 |
| www.ndcf.net | robots.txt 200: allowed for research-script/1.0 |
| www.newbremenfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.placercf.org | robots.txt 200: allowed for research-script/1.0 |
| www.rhinelandercommunityfoundation.com | robots.txt 200: allowed for research-script/1.0 |
| www.rochesterarea.org | robots.txt 200: allowed for research-script/1.0 |
| www.savfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.skagitcf.org | robots.txt 200: allowed for research-script/1.0 |
| www.southmadisonfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.steubenfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.sturgisfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| www.wicf-inc.org | robots.txt 200: allowed for research-script/1.0 |
| www.yscf.org | robots.txt 200: allowed for research-script/1.0 |
| www.yvcf.org | robots.txt 200: allowed for research-script/1.0 |
| yorkcommunityfoundation.org | robots.txt 200: allowed for research-script/1.0 |
| yscf.org | robots.txt 200: allowed for research-script/1.0 |
| yvcf.org | robots.txt 200: allowed for research-script/1.0 |

The hosts logged "-1" (cfpartner.org, greatertaylorfoundation.org, www.marioncommunityfoundation.org, www.brooklinecommunity.org) are explained in §1.3: either nothing was fetched from them (TLS failure), or robots.txt was re-read as allowed (Brookline). www.montrosecf.com disallows all agents, and cdn.prod.website-files.com returns 403; nothing was fetched from either.
