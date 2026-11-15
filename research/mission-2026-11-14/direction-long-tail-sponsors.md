# Direction P-NEW-TAIL-01: the long tail of DAF sponsors (under $50m of DAF assets), FY2021–FY2024

**Date:** 2026-11-15 · **Queue item:** P-NEW-TAIL-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv`](../../data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv): 1,585 rows, one per sponsor EIN with a corrected row in FY2020–FY2024. It covers all 1,514 FY2024 sponsors (top 50, middle and tail, so that the comparison can be rebuilt) and 71 sponsors with no FY2024 row. FY2020 is used only as the baseline for FY2021 exits.
- [`data/mission-2026-11-14/queue-proposals-batch45-n33.csv`](../../data/mission-2026-11-14/queue-proposals-batch45-n33.csv): P-B45N33-01 to P-B45N33-03.
- **Script** (stdlib only, functional style): [`scripts/mission_long_tail.py`](../../scripts/mission_long_tail.py). It reads repository data and a local copy of the IRS EO Business Master File. It makes no network request.

**Rules applied**
- **Governing corrections read first:**
  - [full-universe-990-harvest-and-corrected-totals.md](full-universe-990-harvest-and-corrected-totals.md), waves 5 and 19. Neither changes a sponsor value used here.
  - [direction-league-table-concentration.md](direction-league-table-concentration.md), wave 29. This only concerns NPT's FY2023 value, which is a top-50 row and is not used in a tail figure.
  - [direction-cf-consolidation-fees.md](direction-cf-consolidation-fees.md), wave 25A. The 803 CF filers and the fee medians are used as corrected.
  - [queue-batch35-panel-screens.md](queue-batch35-panel-screens.md), wave 20. The public-support screen is used only as a flag count.
  - The crt.sh compliance note: no figure here rests on crt.sh. The CF vendor map rows used here come from homepage links, portal pages and DNS.
- **Values:** FY2021–24 sponsor values are DAFRC's, overridden by rules R1–R4. The script rebuilds them with `mission_league_table.corrected()`.
  - **Check [C]:** the rebuilt sums equal `dafrc-corrected-market-totals.csv` exactly (difference 0) in all 16 FY2021–24 × metric cells.
  - FY2024 market: assets $323.27bn, contributions $92.77bn, grants $66.44bn, 3,309,483 accounts.
- **Recency:** FY2021–FY2024 only.
- **Labels:** **[F]** filed or published value · **[C]** script computation · **[I]** inference.
- No logins, forms or outreach. **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **How big is the tail?** | **1,240 of the 1,514 FY2024 sponsors (81.9%) hold under $50m of DAF assets. Together they hold $9.18bn, which is 2.84% of corrected market assets** [C].<br>- **Under $10m:** 947 sponsors (62.6%) holding $2.22bn (0.69%).<br>- **Under $1m:** 423 sponsors (27.9%) holding $0.12bn (0.04%). 35 of these report $0 or less.<br>- **The top 50** are 3.3% of sponsors and hold 85.5% of assets.<br>- Median tail sponsor: $2.36m. Median top-50 sponsor: $1.13bn. | High [C] |
| **Share of flows and accounts** | **Contributions 2.98% and grants 4.66% of the market. Accounts appear to be 46.4%, but that is an artefact** [C]:<br>- Givinga, a micro-account processor, reports 1,421,011 "DAFs" on $1.95m.<br>- BNY Mellon CGF, terminated in December 2024, sits in the tail at $4.7m but granted $725.6m in FY2024, including $619.8m to RCF.<br>- **Without these two:** the tail holds 2.84% of assets, 2.79% of contributions, 3.55% of grants and **3.49% of accounts**. | High [C] |
| **Who is in the tail?** | **Community foundations are about half by count and two-thirds by assets** [C]:<br>- CF 641 (51.7% of tail sponsors; 66.5% of tail assets);<br>- other single-issue charities 283 (22.8%; 9.1%);<br>- religious 149 (12.0%; 15.6%);<br>- universities and hospitals 115 (9.3%; 3.7%);<br>- national (standard) 36 (2.9%; 4.5%);<br>- donation processors 16 (1.3%; 0.7%).<br>**Lower down the tail the mix shifts away from CFs.** Under $1m it is 38.3% CFs and 35.5% other single-issue charities.<br>**The top 50 are mostly national sponsors:** 19 national (81.7% of top-50 assets) and 21 CFs (12.3%). | High [C] on DAFRC types |
| **Age and geography** | **The tail is no younger than the top 50** [C]:<br>- Median IRS ruling year 1995 and median age 29 years (IQR 21–43). The top 50: ruling year 1996, age 28.<br>- 9.7% of tail sponsors were ruled in 2015 or later (12.1% under $1m), against 6.1% of the top 50.<br>**It is spread across 52 state codes** (BMF). The most common are CA 96, IN 90, OH 79, MI 73, NY 64, PA 60 and IL 53. Under $1m, Indiana leads with 39. The top 50 sit in 23 states. | High [F/C] |
| **Accounts and account size** | **The median tail sponsor runs 24 DAFs** (IQR 7–62) with a median average account of **$133k** (IQR $61k–$263k) [C]:<br>- under $10m: 13 accounts, $98k;<br>- under $1m: 6 accounts, $40k;<br>- top 50: 1,464 accounts, $836k;<br>- middle (rank above 50, $50m or more): 261 accounts, $489k.<br>University and hospital tail sponsors run a median of **5** DAFs; other single-issue charities run 7; CFs run 36. | High [C]; n=1,028 tail sponsors with non-imputed, plausible counts |
| **Payout** | **The tail's median payout is lower and its spread much wider** [C]. Payout is grants ÷ prior-year assets.<br>- FY2024 median: **11.7%** (IQR 4.7–26.8%) in the tail, against 14.3% in the middle and **19.6%** in the top 50.<br>- **Share under 5%:** 26.8% of the tail, 32.0% under $10m and **37.6% under $1m**. The figure is 6.5% in the middle and **0%** in the top 50.<br>- 7.7% of the tail paid out nothing (15.9% under $1m), while 7.2% paid out more than 100%. Those are flow-through sponsors such as the OJC Fund, Mightycause and Pledgeling.<br>- **Persistence:** 165 tail sponsors ($0.72bn) were under 5% in each of FY2022, FY2023 and FY2024, out of the 992 with three valid years. | High [C]; definitions in §1 |
| **Entries and exits FY2021–24** | **The tail is where sponsors come and go** [C]:<br>- **Entries:** 138 sponsors entered the panel in FY2021–24. 134 of them are below $50m in FY2024, and 92 entered below $1m. 109 are existing organisations new to the panel; only 26 were ruled exempt within a year of entering, among them DonateStock, Manifold for Charity and GoodCoin.<br>- **Exits:** 85 of the 90 candidate exits dated FY2021–23 had less than $50m at their last filing. Panel exit rates by prior-year size are 2.6% a year under $1m, 1.9% at $1–10m, 1.5% at $10–50m and 0.44% at $50m or more.<br>- **Verified outcomes for the 85 tail exits:** 9 ceased (tier A); 49 still file a 990 but report no DAFs (tier B); 14 unresolved (tier C); 13 reporting artefacts (tier D). | High [F/C] on the counts; candidate exits are not all true exits |
| **Vendor** | **Where a CF's vendor is identified, it is Foundant 80% of the time. But the smaller the CF, the less often any vendor shows** [C]:<br>- **Tail CFs:** 351 of 641 (54.8%) have a high- or medium-confidence vendor in the CF map. Of these, Foundant has 282, akoyaGO 41, Ren/Stellar 11, Foundation Cloud 9, Salesforce 4 and Blackbaud 3.<br>- **Unmapped:** 242 tail CFs (37.8%), rising to 108 of the 162 CFs under $1m (66.7%).<br>- **Top-50 CFs:** 19 of 21 are mapped, across seven vendors. Foundant has 5.<br>- **Part VII-B lines:** only 27 of 1,240 tail sponsors (2.2%) list a DAF-relevant contractor over $100k. 12 are Blackbaud lines, all at single-issue charities (CRM). There are 5 Ren lines and 1 Northeast Retirement Services line. | Medium: the map is website-based and covers CFs only |
| **Published fee** | **None of the 1,240 tail sponsors has a published fee in the repository** [C]:<br>- the CF fee census stops at the 100th-largest CF ($101.4m);<br>- the national schedules cover 11 sponsors, all above $50m.<br>For comparison, 16 of the top 50 have a published schedule in the repository. **This is the largest gap in this profile** (P-B45N33-01). | High on the absence |
| **What an AI-native platform could offer** | See §5. **[I] throughout.** In short: the tail's problem is fixed cost per account, not technology per se. The data show 24 accounts per sponsor, weak and lagging Schedule D reporting, low or zero payout at a quarter of sponsors, and a CF vendor field dominated by one incumbent with a third unmapped. Its revenue pool is small: about $92m a year if the whole tail charged the 100 bps CF median [C on that assumption]. | [I] |

---

## 1. Method

### 1.1 Universe and bands
1. **Sponsor-years:** every corrected FY2021–24 row, built as DAFRC plus R1–R4, including the R4 additions such as the Donors Fund and Greater Pike FY2024. **FY2024 has 1,514 sponsors.**
2. **Rank:** by FY2024 corrected year-end DAF assets, ties broken by EIN. The rank-50 value is $581,066,147, which matches the league table.
3. **Bands (FY2024):**

   | Band | Rule | Sponsors |
   |---|---|---|
   | `top50` | rank 1–50 | 50 |
   | `mid` | rank above 50 and $50m or more | 224 |
   | `t10_50` | $10m to under $50m | 293 |
   | `t1_10` | $1m to under $10m | 524 |
   | `t0_1` | above $0 and under $1m | 388 |
   | `zero` | $0 or less | 35 |

   The three tails are cumulative: under $50m = `t10_50 + t1_10 + t0_1 + zero` (1,240); under $10m (947); under $1m (423).
4. **Sensitivity (`*_ex_structural`):** the same groups without the two documented outliers.
   - **BNY Mellon CGF (300748315):** terminated in December 2024 and wound into RCF (`mission_league_table.EVENTS`).
   - **Givinga (474172718):** a micro-account processor (P-B35A-01).
5. **Sponsor type:** DAFRC `type` × `subtype`, as follows:
   - Community Foundation → `community_foundation`;
   - Single Issue/Other → `single_issue_other`;
   - Single Issue/Religiously-Affiliated → `religious`;
   - Single Issue/Universities and Healthcare → `university_or_hospital`;
   - National/Standard → `national_standard`;
   - National/Donation Processor → `donation_processor`.

### 1.2 Measures
- **Shares:** sponsor sums ÷ the FY2024 corrected market totals.
- **Payout (FY t):** corrected grants FY t ÷ corrected year-end assets FY t−1. This is the repository's market payout definition.
  - It is computed only where neither value is still DAFRC-imputed and prior assets are above 0.
  - The tail has 1,097 valid FY2024 payouts. The pooled FY2022–24 figures use every valid sponsor-year.
- **Accounts and average account:** used only where neither the assets nor the count is imputed, and the count passes the league-table plausibility screen. The screen blanks counts above 1,000 that average under $5 per account.
- **Ruling year, state and NTEE:** from the IRS EO BMF, files eo1–eo4, eo_pr and eo_xx ([eo1.csv](https://www.irs.gov/pub/irs-soi/eo1.csv); Last-Modified 2026-11-09).
  - The copy was saved earlier in this session on 2026-11-15 under the `/pub/irs-soi/` path, which earlier batches fetched after the robots check. This run made no request.
  - 1,507 of the 1,514 FY2024 sponsors match. Age is 2024 minus the ruling year.
- **Entries:** the mortality panel's first panel FY (`sponsor-entry-exit-panel.csv`, `is_entry_year`) falling in FY2021–24, with its ruling-based entry class.
- **Exits:** the mortality study's candidate exits dated FY2021–23:
  - `panel_exit`;
  - `imputation_masked_candidate`;
  - `zero_daf_assets_terminal`.

  Exits dated FY2024 cannot yet be observed (right-censored).
  - Outcome tiers A–D come from `sponsor-exit-verification.csv`, and tier-B reasons from `tier-b-daf-exit-reasons.csv`.
  - Exit rates are exits dated t ÷ at-risk sponsor-years: sponsors with a row in t−1 that have not already exited, banded on corrected t−1 assets.
- **Vendor:**
  - `cf-vendor-map-by-ein-v2.csv` (CFs only). A vendor counts when its confidence is high or medium.
  - DAF-relevant Part VII-B lines, FY2022–25, from `form990-contractors-harvest-full.csv`. The categories counted are DAF tech and admin, giving platform or outsourced admin, payment processor, grant due diligence and investment accounting software.
- **Fee:** `cf-daf-fee-census-2026.csv` by EIN, and `sponsor-fee-schedules.csv` by a name fragment that the script checks is unique (11 nationals match).
- **Data-quality flags:**
  - returns in `blank-schedule-d-panel.csv`, FY2021–24;
  - flags in `public-support-cliff-screen.csv`, FY2021–24 (that screen covers only 123 few-account, large-balance sponsors).
- **Outside-DAFRC context:** `non-dafrc-daf-filers-990.csv`, `reports_daf_value` rows.

---

## 2. Size and share (FY2024, corrected)

| Group | Sponsors | % of sponsors | DAF assets | % assets | % contributions | % grants | Accounts | % accounts | Median sponsor assets |
|---|---|---|---|---|---|---|---|---|---|
| Top 50 | 50 | 3.3% | $276.27bn | 85.5% | 82.9% | 77.9% | 563,997 | 17.0% | $1,132m |
| Middle (rank above 50, $50m or more) | 224 | 14.8% | $37.82bn | 11.7% | 14.1% | 17.4% | 1,209,072 | 36.5% | $113.9m |
| **Under $50m** | **1,240** | **81.9%** | **$9.18bn** | **2.84%** | **2.98%** | **4.66%** | 1,536,414 | 46.4% | **$2.36m** |
| – $10–50m | 293 | 19.4% | $6.96bn | 2.15% | 1.96% | 2.53% | 53,158 | 1.6% | $20.6m |
| – $1–10m | 524 | 34.6% | $2.10bn | 0.65% | 0.94% | 2.02% | 1,471,810 | 44.5% | $3.19m |
| **Under $10m** | **947** | **62.6%** | **$2.22bn** | **0.69%** | **1.02%** | **2.13%** | 1,483,256 | 44.8% | **$1.24m** |
| **Under $1m** (35 at $0 or less) | **423** | **27.9%** | **$0.12bn** | **0.04%** | **0.08%** | **0.11%** | 11,446 | 0.35% | **$0.17m** |
| Under $50m, without BNY and Givinga | 1,238 | 81.8% | $9.17bn | 2.84% | 2.79% | 3.55% | 115,402 | **3.49%** | – |
| Under $10m, without BNY and Givinga | 945 | 62.4% | $2.21bn | 0.68% | 0.83% | 1.02% | 62,244 | 1.88% | – |

**Reading [C/I]**
- **The tail is 82% of sponsors and under 3% of the money.** Its grant share is above its asset share (3.55% against 2.84%, even without BNY), so tail DAFs pay out a little faster in aggregate.
- **The account column is unusable without the sensitivity row.** One processor (Givinga) carries 1.42m of the tail's 1.54m "accounts".
- **The DAFRC tail is not the whole tail.** In FY2024, a further **413 non-DAFRC filers** report a Schedule D DAF value: $0.34bn in total, median $106k, 373 of them under $1m and all under $50m (`non-dafrc-daf-filers-990.csv`; FY2023: 424 filers, $0.15bn). With them, the number of sponsors under $1m roughly doubles, while the asset picture barely moves.

---

## 3. Profile

### 3.1 Sponsor type mix (count; share of the group's assets)

| Type | Top 50 | Middle | Under $50m | Under $10m | Under $1m |
|---|---|---|---|---|---|
| Community foundation | 21 (12.3%) | 142 (62.7%) | **641 (66.5%)** | 434 (56.0%) | 162 (47.5%) |
| Single-issue, other | 1 (0.4%) | 10 (3.0%) | 283 (9.1%) | 262 (17.0%) | 150 (28.5%) |
| Religious | 6 (4.6%) | 29 (12.2%) | 149 (15.6%) | 106 (14.0%) | 43 (11.5%) |
| University or hospital | 2 (0.5%) | 11 (4.7%) | 115 (3.7%) | 110 (9.7%) | 51 (9.0%) |
| National (standard) | 19 (81.7%) | 27 (15.9%) | 36 (4.5%) | 21 (1.6%) | 11 (2.7%) |
| Donation processor | 1 (0.5%) | 5 (1.4%) | 16 (0.7%) | 14 (1.7%) | 6 (0.8%) |

**NTEE codes (BMF, tail).** T (philanthropy) 730, B (education) 117, X (religion) 50, S 48, P 46, E (health) 34 and Q 22. 95 tail sponsors have no NTEE code in the BMF. The DAFRC type is the better guide. For example, many university foundations carry T or B codes.

### 3.2 Age and state

| Measure | Top 50 | Middle | Under $50m | Under $10m | Under $1m |
|---|---|---|---|---|---|
| Median ruling year | 1996 | 1988 | 1995 | 1995 | 1995 |
| Median age (years at 2024; IQR) | 28 (24–49) | 36 (26–54) | 29 (21–43) | 29 (20–42) | 29 (20–41) |
| Ruled 2015 or later | 6.1% | 7.6% | 9.7% | 11.0% | 12.1% |
| Ruled before 1990 | 36.7% | 52.7% | 37.2% | 37.1% | 36.1% |
| State codes | 23 | 48 | 52 | 51 | 48 |
| Most common states | CA 9, MA 5, NY 4 | CA 16, FL 14, NY 13 | CA 96, IN 90, OH 79, MI 73, NY 64 | IN 76, CA 72, MI 58, OH 54 | IN 39, CA 32, IL 25, MI 25, OH 23 |

- **[C]** The tail is not a cohort of start-ups. Its median sponsor is 29 years old, and only about one in ten was ruled exempt after 2014.
- **[I]** Indiana and Michigan stand out at the bottom of the tail. This is consistent with the dense networks of county community foundations in those states, but the reason is not tested here.
- **Caveat:** state is the BMF's current address, not the location of the donors.

### 3.3 Accounts and account size (FY2024; non-imputed, plausible counts)

| Measure | Top 50 | Middle | Under $50m | Under $10m | Under $1m |
|---|---|---|---|---|---|
| Sponsors with a valid count | 50 | 213 | 1,028 | 746 | 300 |
| Median accounts (IQR) | 1,464 (769–5,399) | 261 (157–479) | **24 (7–62)** | 13 (5–33) | 6 (2–12) |
| Median average account (IQR) | $836k ($370k–$1.39m) | $489k ($329k–$735k) | **$133k ($61k–$263k)** | $98k ($43k–$187k) | $40k ($16k–$76k) |

**Within the tail [C]:**
- **Median accounts by type:** CF 36, religious 35, national 33, other single-issue 7, university or hospital **5**.
- **Median average account by type:** university or hospital $191k, national $187k, CF $144k, religious $121k, other single-issue $90k.

### 3.4 Payout (grants ÷ prior-year assets)

| Measure | Top 50 | Middle | Under $50m | Under $10m | Under $1m |
|---|---|---|---|---|---|
| Valid FY2024 payouts | 49 | 216 | 1,097 | 813 | 340 |
| Median FY2024 (IQR) | **19.6%** (15.4–25.3) | 14.3% (10.0–24.8) | **11.7%** (4.7–26.8) | 10.7% (3.7–30.6) | 10.7% (1.9–49.0) |
| Share under 5% | **0%** | 6.5% | **26.8%** | 32.0% | **37.6%** |
| Share at 0% or less | 0% | 0.5% | 7.7% | 10.2% | 15.9% |
| Share above 100% (flow-through) | 2.0% | 5.6% | 7.2% | 9.4% | 14.7% |
| Pooled FY2022–24 median | 19.0% | 13.7% | 10.5% | 9.0% | 8.4% |
| Pooled share under 5% | 0.7% | 7.5% | 30.4% | 35.9% | 41.4% |

**By type within the tail (FY2024 median; share under 5%) [C]:**
- religious 18.4%; 19.4%
- other single-issue 14.8%; 34.8%
- community foundation 10.8%; 23.6%
- university or hospital **6.6%; 42.0%**
- national 25.9%; 20.0%

**Persistence:** 165 of the 992 tail sponsors with three valid years were under 5% in every year from FY2022 to FY2024. They hold $0.72bn: 83 CFs, 37 other single-issue charities, 29 universities or hospitals, 15 religious sponsors and 1 processor.

**Reading [I]**
- The tail's distribution is bimodal. It contains quiet funds at university, hospital and small CF sponsors, alongside pass-through vehicles (Matbia, the OJC Fund, Pledgeling, Mightycause, FrontStream, Give Back) whose grants are several times their assets.
- Low tail payout may partly be a classification effect: endowed or designated funds reported in the DAF column. P-B45N33-03 tests this.

### 3.5 Entries and exits, FY2021–24

**Entries (138 in FY2021–24; 41 / 42 / 36 / 19 by year):**
- **Size at entry:** 92 entered below $1m, 36 at $1–10m, 7 at $10–50m, 2 at $50m or more and 1 at $0.
- **Where they are in FY2024:** 134 are in the under-$50m tail (`t0_1` 70, `t1_10` 49, `t10_50` 8, `zero` 7), 3 in the middle and 1 in the top 50 (BofA CGF).
- **Class:** 109 are existing organisations new to the panel; 26 were ruled exempt within a year of entry; 3 were reinstated or reorganised.
- **Tail entrants by type:** other single-issue 58, CF 36, university or hospital 16, religious 12, national 10, processor 2.
- **New organisations include online giving-platform sponsors [I]:** DonateStock Charitable, Manifold for Charity, the GoodCoin Giving Fund and GivingTrax Foundation. Daffy Charitable Fund (FY2021) is the one new organisation of this window that has grown out of the tail: $334.5m in FY2024 (filed, R1).

**Exits (candidate exits dated FY2021–23: 90; 85 had less than $50m at the last filing):**

| Prior-year band | At-risk sponsor-years | Exits | Exit rate per year |
|---|---|---|---|
| Under $1m | 1,248 | 33 | **2.6%** |
| $1–10m | 1,552 | 29 | 1.9% |
| $10–50m | 848 | 13 | 1.5% |
| $50m or more | 686 | 3 | 0.44% |
| $0 | 60 | 12 | (20%; a degenerate band) |

**Verified outcomes for the 85 tail exits** (`sponsor-exit-verification.csv`):

| Tier | Count | Detail |
|---|---|---|
| A: organisation ceased or converted | 9 | |
| B: survives, reports no DAFs | 49 | Reasons from `tier-b-daf-exit-reasons.csv`: undetermined 16; reporting gap but still reports DAFs 12; reporting gap, then line 6 "No" 6; transferred out (documented) 5; granted out to zero 4; reclassified as not a DAF 2; other 4 |
| C: unresolved | 14 | |
| D: reporting artefact | 13 | |

- **By type:** CF 42, other single-issue 18, religious 12, university or hospital 8, national 4, processor 1.
- **Reading [I]:** most tail "exits" are sponsors that stop running or stop reporting a DAF line, not failed organisations. Where the money's destination is documented, it went to another charity.
- **Consistency:** the size gradient matches the mortality study (2.2%, 1.3%, 0.7% and 0.2% for FY2020–23 on the older band cuts).

### 3.6 Vendor and fee

| Measure | Top 50 | Middle | Under $50m | Under $10m | Under $1m |
|---|---|---|---|---|---|
| CFs in group | 21 | 142 | 641 | 434 | 162 |
| CFs with a high- or medium-confidence vendor | 19 | 132 | 351 (54.8%) | 188 (43.3%) | 41 (25.3%) |
| – of which Foundant | 5 | 86 | **282** | 155 | 35 |
| – of which akoyaGO | 0 | 11 | 41 | 24 | 6 |
| CFs `Unmapped` in the CF map | 0 | 8 | 242 (37.8%) | 214 (49.3%) | 108 (66.7%) |
| Sponsors with a DAF-relevant Part VII-B line, FY2022–25 | 17 | 26 | 27 (2.2%) | 17 | 7 |
| Sponsors with a published fee in the repo | 16 | 28 | **0** | 0 | 0 |

**Tail Part VII-B lines (names as filed) [F]:**
- **Ren/Stellar:** CF of Greater Flint, Southwest Florida CF, Catholic Community Foundation (Los Angeles), Jewish Federation of Greater Seattle and RSF Social Finance.
- **Others:** Northeast Retirement Services (Advisors Charitable Gift Fund), TASC (Give Back Foundation), Mightycause (Colorado Gives Foundation and its own fund), FrontStream (United Way Worldwide and FrontStream Global Fund), and Stripe (CF of the Texas Hill Country, Pledgeling, University of Minnesota Foundation).
- **Blackbaud:** 12 lines, all at non-CF single-issue charities, which points to CRM rather than DAF administration.

**Reading [C/I]**
- In the tail the CF vendor market looks like a near-monopoly for Foundant among identified CFs (80%). The top-50 CFs, by contrast, spread over seven vendors.
- A third of tail CFs, and two-thirds of those under $1m, show no vendor at all. The likeliest reason is that they have no donor portal: their sites link no vendor host [I].
- Part VII-B cannot see tail vendors, because few tail sponsors pay any contractor more than $100k.
- **Fee:** the repo has no tail fee observation. P-B45N33-01 fills this.

### 3.7 Reporting quality

| Measure | Top 50 | Middle | Under $50m |
|---|---|---|---|
| Sponsors with any FY2024 metric still DAFRC-imputed after R1–R4 | 1 | 12 | **228** (assets 52, grants 98, accounts 172) |
| Sponsors with a blank Schedule D Part I return in FY2021–24 | 0 | 5 | **59** |
| Sponsors with a public-support-screen flag | 0 | 6 | 35 (screen covers 123 sponsors only) |

**[C]** Almost all of the data defects in the corrected panel sit in the tail.

---

## 4. Tail against the top 50 (one table)

| Dimension | Top 50 | Under $50m |
|---|---|---|
| Sponsors / share of assets | 50 / 85.5% | 1,240 / 2.84% |
| Dominant type | National (81.7% of assets) | CF (51.7% of count, 66.5% of assets) |
| Median age | 28 years | 29 years |
| Median accounts / average account | 1,464 / $836k | 24 / $133k |
| Median payout / share under 5% | 19.6% / 0% | 11.7% / 26.8% |
| Entries / exits FY2021–24 | 1 FY2021–24 panel entrant (BofA CGF) / 5 candidate exits had $50m or more at last filing (Jasper Ridge, TIAA, Goldstein, Omaha CF and Donors Fund; the last two are reporting artefacts) | 134 entrants / 85 candidate exits |
| Identified CF vendors | 7 vendors across 19 CFs | Foundant has 80% of the 351 identified |
| Published fee | 16 sponsors | 0 |

---

## 5. What an AI-native platform could offer this tail ([I], inference throughout)

These are hypotheses drawn from the profile above. No sponsor was contacted, and nothing here was tested with users.

1. **Make 24 accounts economical.** The median tail sponsor runs 24 DAFs ($2.4m) and, under $1m, 6 DAFs ($0.17m). It cannot spread a staff member, an annual software contract or an audit-grade fund-accounting process over that base.
   - **Offer:** an administration layer priced per account or per transaction with no fixed floor. It would cover gift intake, grant due diligence (BMF, Pub 78 and revocation checks), grant payment and donor statements.
   - **Evidence it matters:** the repo's top-100 CF minimum annual fees of $50–$2,500 imply that tail donors face minimum-fee pricing.
   - **Not yet shown:** the tail's actual fees (P-B45N33-01) and its cost base (P-B45N33-02).
2. **Filing-grade data as a by-product.** 228 tail sponsors still carry an imputed FY2024 value after correction, and 59 filed a blank Schedule D Part I.
   - Most tail "exits" are reporting gaps (tier B: 49 of 85).
   - A system that keeps the fund ledger and produces the Schedule D Part I lines and the Part IV line 6 answer directly addresses a visible failure.
3. **Payout activation without breaching advisory privilege.** A quarter of tail sponsors pay out under 5% a year, and 165 do so three years running.
   - Grant recommendations drawn from local nonprofit data, inactivity reminders and successor-advisor workflows are the obvious agent tasks.
   - Whether the low payout is real dormancy or a reporting artefact is open (P-B45N33-03).
4. **Coexist with or replace Foundant.** Among identified tail CFs Foundant dominates (282 of 351).
   - An entrant would either integrate with that installed base or target the 242 CFs that show no vendor.
   - Those unmapped CFs are smaller, at a median under $10m, and so are cheaper to serve but pay less.
5. **"DAF-as-a-feature" for non-CF charities.** 547 of the tail sponsors are religious, university, hospital or other single-issue charities.
   - The university and hospital sponsors run a median of 5 DAFs and are the least active payers (6.6% median; 42% under 5%).
   - For them, a white-label DAF run by an outside platform competes with simply referring donors to a national sponsor.
6. **Clean wind-downs and transfers.** Exits are frequent in the tail (1.5–2.6% a year), and where the destination is documented the money moves to another charity.
   - Tools that make a Schedule N transfer, or a fund-by-fund move to a successor sponsor, cheap and auditable serve the sponsors that are leaving. They also serve whichever platform receives the funds.
7. **Size the prize honestly.** The tail holds $9.18bn.
   - At the 100 bps median CF admin rate (top-100 census, $100k–$1m), the tail's entire admin-fee pool would be about **$92m a year** [C on that assumption].
   - A platform taking a fraction of that is a small business unless it also serves the 413+ sponsors outside DAFRC, the middle band ($37.8bn), or non-DAF fund types at the same CFs.
   - New entrants already present at the tail (DonateStock, Manifold, GoodCoin, GivingTrax, Endaoment) show that the low-cost end is contested.

---

## 6. Limitations
- **The universe is DAFRC's corrected panel.** Some 413–538 small non-DAFRC filers a year are excluded from the tail figures (§2 gives them as context). Sponsors that answer Part IV "No", file a 990-EZ or file on paper are invisible.
- **Imputation persists in the tail.** 228 tail sponsors carry at least one imputed FY2024 metric. Payout and account statistics exclude those values, so the valid n is given in each table.
- **Type is DAFRC's classification.** "Single-issue, other" mixes federations, social-finance funds, giving platforms and service charities.
- **The BMF is a November 2026 snapshot.** Ruling dates can postdate reorganisations, and state is the current mailing address. Seven FY2024 sponsors are not in the BMF.
- **Vendor coverage is uneven.** The CF map covers CFs only and rests on website evidence. "Unmapped" can mean no portal or an unrecognised vendor. Part VII-B lists only contractors paid over $100k (top five). No vendor is known for the non-CF tail beyond Part VII-B.
- **Fee coverage is zero for the tail.**
- **Payout is grants ÷ prior-year assets on mixed fiscal years.** It is distorted for flow-through sponsors and for sponsors with tiny prior-year balances, which is why medians are reported and the >100% share is shown separately.
- **Exits are candidate exits dated FY2021–23.** FY2024 is right-censored. Tiers B–D show that most candidates are not organisational deaths.
- **The structural outliers** (BNY Mellon CGF and Givinga) are left in the headline rows, and the sensitivity rows show their effect.
- **Section 5 is inference.** It is not a market test.

---

## 7. Data dictionary: `daf-long-tail-sponsors-fy2021-2024.csv` (1,585 rows)

| Column | Meaning |
|---|---|
| ein, name, dafrc_type, dafrc_subtype | Sponsor (DAFRC latest row; corrections file for R4-only EINs) |
| sponsor_category | community_foundation, single_issue_other, religious, university_or_hospital, national_standard or donation_processor (§1.1) |
| fy2024_rank_assets, size_band_fy2024 | FY2024 rank; band `top50` / `mid` / `t10_50` / `t1_10` / `t0_1` / `zero`, or `not_in_fy2024` |
| in_lt50m, in_lt10m, in_lt1m | 1 if in the cumulative tail |
| daf_assets_fy2021 … daf_assets_fy2024 | Corrected year-end DAF assets (blank means no row) |
| daf_contributions_fy2024, daf_grants_fy2024, daf_accounts_fy2024 | Corrected FY2024 values as stored, including imputed values |
| accounts_fy2024_screened, avg_account_fy2024 | Count and assets ÷ count, only where non-imputed and plausible |
| payout_fy2022, payout_fy2023, payout_fy2024 | Grants FY t ÷ assets FY t−1 (non-imputed, prior assets above 0) |
| imputed_kept_fy2024, corrections_fy2024 | Metrics still DAFRC-imputed; R1–R4 rules applied |
| entry_fy, entry_in_fy2021_24, entry_class | Mortality-panel entry FY; class for FY2021–24 entrants |
| exit_kind, exit_fy, exit_in_fy2021_23 | Mortality candidate exit and its dated FY |
| exit_outcome, exit_outcome_tier, exit_ref_daf_assets | Verification outcome, tier A–D, and last positive filed DAF assets |
| tierb_exit_reason | Reason class from `tier-b-daf-exit-reasons.csv` |
| bmf_ruling, ruling_year, age_years_at_2024 | IRS BMF RULING (YYYYMM), its year, 2024 − year |
| bmf_state, bmf_ntee, ntee_major, bmf_foundation_cd, in_bmf_2026 | BMF state, NTEE code and major group, foundation code, presence |
| cf_vendor_family, cf_vendor_confidence, cf_vendor_evidence_type | From `cf-vendor-map-by-ein-v2.csv` (CFs only) |
| vendors_990_daf_relevant_fy2022_25 | Vendor groups on DAF-relevant Part VII-B lines (FY2022–25) |
| fee_status, fee_bps_100k, fee_bps_1m, fee_source, fee_url | Fee census row (CF) or national schedule match. Blank means no fee in the repo |
| blank_part_i_returns_fy2021_24 | Count of returns in `blank-schedule-d-panel.csv` |
| support_cliff_flags_fy2021_24 | Union of flags in `public-support-cliff-screen.csv` |
| source | Inputs |

## 8. Reproduction
```
python3 scripts/mission_long_tail.py --bmf-dir DIR   # DIR holds eo1.csv..eo4.csv, eo_pr.csv, eo_xx.csv (and optionally eo1.hdr)
python3 scripts/mission_long_tail.py                 # without BMF: ruling, state and NTEE columns are blank
```
- The script prints a JSON summary. Every figure in §0–§4 comes from it or from the CSV. The summary contains:
  - the corrected-totals check (16 cells, difference 0);
  - the band counts;
  - the group statistics (`groups`, including the `*_ex_structural` sensitivities);
  - `entry_exit` and the exit rates;
  - the outside-DAFRC context;
  - the persistent low-payout set.
- It runs in a few seconds.
