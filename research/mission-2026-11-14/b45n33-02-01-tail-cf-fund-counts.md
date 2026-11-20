# P-B45N33-02-01: fund-count denominators for tail community foundations, and allocation rule F

**Date:** 2026-11-20 · **Task id:** b45n33-02-01 · **Queue item:** P-B45N33-02-01 (from [b45n33-long-tail-operating-cost.md](b45n33-long-tail-operating-cost.md) §2.1 and §4)

**Outputs**
- [`data/mission-2026-11-14/tail-cf-fund-counts-2026-11-20.csv`](../../data/mission-2026-11-14/tail-cf-fund-counts-2026-11-20.csv): 60 rows, one per sampled tail CF. Holds fund counts by type, Schedule D counts, rule F beside rules A and G, the source, and a quote check. Counts only: the file holds no donor or fund names.
- [`scripts/mission_tail_cf_fund_counts.py`](../../scripts/mission_tail_cf_fund_counts.py): stdlib only, functional style. It draws the sample, runs the robots-checked fetch tasks and verifies every quote against the cached source. `--task build` writes the CSV and prints every table in this note.
- [`data/mission-2026-11-14/queue-proposals-b45n33-02-01.csv`](../../data/mission-2026-11-14/queue-proposals-b45n33-02-01.csv): 5 follow-ups.

**Labels:** **[F]** filed or published value (quoted) · **[C]** script computation · **[I]** inference. Every allocated DAF cost is **[I]**. This is research, not legal, tax or accounting advice.

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **Coverage** | Of 60 sampled tail CFs, **15 publish a 2021+ count of all their component funds** (6 / 5 / 4 in the $10–50m / $1–10m / <$1m bands). Another 3 publish only endowed or cumulative counts, 9 publish counts for one or two fund types, and 19 publish no count. 12 could not be read: 6 robots-blocked, 2 bot challenges, 4 unreachable. 2 have no website [C]. | High [C] |
| **DAF counts** | Form 990 Schedule D Part I line 1(a) gives a DAF count for **59 of 60** (FY2024 return). Medians are **110 / 36 / 5** DAFs by band [F/C]. Column (b) is filled for 27 and counts *other advised* funds only, so it is not an all-funds count (IRS instructions, S2). | High [F] |
| **Fund-type detail** | Only **1 of 60** publishes counts for every type: Loudoun (2022) has 33 DAF, 26 designated, 21 field-of-interest, 7 scholarship, 12 agency, 10 unrestricted and 1 fiscal-sponsorship fund, so 110 in all and DAFs 30% of funds [F]. Morton's directory gives counts for the non-DAF types: 48 designated, 30 scholarship, 12 agency, 10 FOI, 4 unrestricted and 2 pass-through [C]. Scholarship counts exist for 11 CFs. | Medium [F/C] |
| **DAF share of funds (rule-F share)** | Median **0.181** (0.072–0.410; n = 15). On the same CFs, the asset share (rule A) is **0.209** and the grant share (rule G) is **0.233**. Per CF, F ÷ A has a median of **1.03** (0.74–1.46), and F > A at 8 of 15 [C]. | Medium [C]; 8 of 15 totals are lower bounds |
| **Rule F cost per DAF account** | **[I] $2,108** median (IQR $1,612–$4,864; n = 13; bootstrap 95% CI $1,612–$4,864). The same CFs have rule A **$2,607** and rule G **$3,516**. By band: **$4,647 / $2,157 / $1,612** (rule A $3,282 / $2,819 / $1,174). | Low–medium [I] |
| **Rule F cost per DAF dollar** | **[I] 276 bps** median (145–343; n = 15; CI 144–352). The same CFs have rule A **194 bps** and rule G **215 bps**. By band: **193 / 329 / 326 bps** (rule A 175 / 219 / 202). The stratum-weighted median gives the same values ($2,108; 276 bps). | Low–medium [I] |
| **Does F change the tail picture?** | **[I] At the median it does not change the share: DAFs hold about a fifth of the funds and a fifth of the assets.** It does shift cost toward the smallest CFs. In the <$1m band, rule F per dollar is about 1.6 times rule A (326 vs 202 bps), and rule F per account is $1,612 against $1,174. That fits the cost note's guess that DAF administration is partly a fixed cost per fund. The evidence is weak (n = 4–6 per band), and the F figures are upper bounds wherever the total is an "over N" figure. | Low [I] |
| **Whole-org opex per fund** | **$2,108** median ($1,596–$5,296; n = 15). It ranges from $895 (Cherokee Strip) to $18,145 (El Paso, whose "more than 600" total is a floor) [C]. | Medium [C] |

---

## 1. Method

### 1.1 Frame and sample
- **Frame:** the 641 tail CFs of `long-tail-operating-cost-2026-11-19.csv` (`group = tail_cf`). These are `community_foundation` sponsors with FY2024 corrected DAF assets under $50m (`daf-long-tail-sponsors-fy2021-2024.csv`).
- **Strata (assets band):** $10–50m (`t10_50`, N = 207), $1–10m (`t1_10`, N = 272), and <$1m (`t0_1` + `zero`, N = 162, as in the cost note's "under $1m" band). **n = 20 per stratum.**
- **Draw:** `random.Random(20261120201 + i).sample(stratum rows sorted by EIN, 20)` for stratum i = 0, 1, 2. Weights are N/n: 10.35, 13.6 and 8.1. 60 of 60 drawn CFs are `usable = 1` in the cost file.
- **Homepages:** `cf-vendor-map-by-ein-v2.csv` (the 990 `WebsiteAddressTxt`). One override was needed, for Chippewa County: the stored URL lacks a TLD.

### 1.2 Sources, in order of preference
1. **Form 990 (FY2024, the same return used for opex in the cost note)**, read from the GivingTuesday mirror of the IRS e-file XML:
   - Schedule D Part I line 1: `DonorAdvisedFundsHeldCnt` (column a, DAFs) and `FundsAndOtherAccountsHeldCnt` (column b).
   - Every narrative text field, searched for fund-count statements.
2. **The CF's own site:** annual reports and reports to the community, fund directories (counted, not transcribed), audited statements (notes) and homepage counters. The crawler scored links for "annual report", "our funds", "fund directory", "audit", "financial" and fund-type words. It fetched up to 18 pages per site plus the sitemap.
3. A count is used only if it is **2021 or later**: a live page read on 2026-11-20, or a dated report or return. The 1995–2020 Kearney impact report ("more than 260 funds") and pre-2021 Paso del Norte and Parkersburg reports were read but not used.

### 1.3 What counts as a total
- **`counted` / `all_funds`:** the source states the number of all component funds, or gives counts for every type. 15 CFs.
- **`endowment_only`:** for example, "administers 187 endowment funds" (Dearborn) and "endowments consist of approximately seventy-five individual funds" (Chippewa audit note). **`cumulative`:** "250+ Funds Established" (Hudson). These 3 are used only in the sensitivity row.
- **`partial`:** counts of one or two types only, such as scholarship, agency or temporary scholarship funds, or funds that made grants. Not used for rule F.
- **Qualifiers:** "over", "more than" and "+" are recorded as `lower_bound` (8 of the 15 totals). With a lower-bound total, the DAF share and the rule-F cost are **upper bounds**.
- **Conflicts:** the same-period 990 figure is preferred over site figures. Luzerne's site says 318, "more than 400", "nearly 500" and "700+" on different pages; its FY2024 990 says "over 400" and is used. Twin Tiers' homepage counter (178 funds in 2025) is preferred over a handbook line ("160 Individual Funds").

### 1.4 Directory counts (script-computed)
- **Morton** is the only directory counted. Its by-type directory ends each fund entry with the same link text ("CLICK HERE to learn more"). The script counts that marker between the type headings, starting after "Funds Organized by Type". Result: scholarship 30, designated 48, FOI 10, agency 12, unrestricted 4, pass-through 2.
- The divider count differs by 1 in 4 sections, so each type count is ±1.
- The DAF sections list holders' names only. They were not counted (and no names were recorded), so Morton's total is 106 directory funds + 17 Schedule D DAFs = **123** (`total_basis = directory_non_daf_plus_sched_d_daf`).
- Other directories (Kansas Rural Communities, Berrien, Oregon Trail, Two Rivers, Randolph) are free text with no reliable per-fund marker and were not counted (P-B45N33-02-01-03).

### 1.5 Rule F (new), beside rules A and G
| Rule | DAF cost = | Per account | Per DAF dollar | Assumes |
|---|---|---|---|---|
| A (assets, cost note) | opex × min(1, DAF assets ÷ total assets) | ÷ screened accounts | ÷ DAF assets | A DAF dollar costs what any balance-sheet dollar costs |
| G (grants, cost note) | opex × min(1, DAF grants ÷ Part IX grants) | ÷ screened accounts | ÷ DAF assets | Cost follows grantmaking |
| **F (fund count, this note)** | **opex × min(1, DAF funds ÷ all component funds)** | ÷ screened accounts | ÷ DAF assets | **Every fund costs the same to run, whatever its size or type** |

- **Opex** is the cost note's `opex_ex_11f`: Part IX line 25 less lines 1–4 and 11f.
- **DAF funds:** the source's own DAF count where it gives one (Loudoun, 33, FY2022). Otherwise Schedule D column (a) of the FY2024 return. `daf_share_F_sched_d` uses Schedule D for all.
- Where DAF funds = screened accounts (true for 13 of the 15), **F per account = opex ÷ all funds**. Rule F is then simply the whole-org cost per fund.
- All allocated figures are **[I]**. Totals are from 2021–2026 while opex and DAF counts are from FY2024. The mismatch is recorded in `source_period`.

### 1.6 Network conduct
- **Robots (hard rule):** each host's robots.txt was read once. It was parsed for research-script/1.0, ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot, and a URL was fetched only if **all** were allowed. robots.txt 401/403 was treated as disallowed.
- The listed off-limits hosts were never touched. User agent: "research-script/1.0". GET only: no logins, no forms, no query strings.
- **Terms:** where a homepage linked a terms page, it was read first and checked for clauses against automated access. Four linked pages were read (Rose, Eastmont, Two Rivers, and Dearborn, whose link led to a glossary); none forbids automated access.
- **Log:** 677 requests to 91 hosts on 2026-11-20 between 04:43 and 04:47 UTC, plus one IRS instructions fetch. Verdicts by host: 65 robots.txt 200 allowed for all agents; 17 with no robots.txt (404/400/connection error); 7 robots.txt 403; **2 disallow the Claude and anthropic agents** (occf.org, www.brooklinecommunity.org). 23 URLs were blocked and not fetched. They include three hosts serving sampled CFs' documents: cdn.prod.website-files.com (Duluth-Superior / Boreal Waters annual reports 2022–25), irp.cdn-website.com (Cedar Falls annual report and 990) and a usrfiles.com host (Kansas Rural Communities financials).
- The log is kept outside the repo (`<cache>/robots_log.tsv`); `--task robots` prints it.

---

## 2. Results

### 2.1 Coverage [C]

| Status | $10–50m | $1–10m | Under $1m | All |
|---|---|---|---|---|
| counted (all funds) | 6 | 5 | 4 | **15** |
| endowment_only | 0 | 1 | 1 | 2 |
| cumulative | 1 | 0 | 0 | 1 |
| partial (some types) | 4 | 3 | 2 | 9 |
| no_count_found | 4 | 6 | 9 | 19 |
| robots_blocked | 1 | 3 | 2 | 6 |
| bot_challenge | 2 | 0 | 0 | 2 |
| site_unreachable | 2 | 2 | 0 | 4 |
| no_website | 0 | 0 | 2 | 2 |

- **[C] Fund totals are published by a quarter of tail CFs, and the share falls with size:** 6 of 20 at $10–50m, 4 of 20 under $1m.
- **Where totals come from:** 7 homepage or page counters, 3 annual reports, 2 directory pages that state a total, 2 FY2024 990 narratives and 1 directory count (Morton).
- **[C] Audits rarely help.** Audits were read for Act for Alexandria, Summit, the Dayton Foundation, Chippewa County and Big Spring. Only Chippewa's notes give a count ("approximately seventy-five individual funds", endowment only). The others give balances by fund type in dollars, such as Act for Alexandria's designated, FOI and scholarship balances.

### 2.2 Schedule D counts and the rule-F set

**Schedule D Part I line 1, FY2024 return (all 60) [F/C]**

| Stratum | n with DAF count | DAFs, col (a): median (IQR) | n col (b) filled | Col (b) "other similar funds": median (IQR) |
|---|---|---|---|---|
| $10–50m | 20 | 110 (57–172) | 8 | 234 (36–286) |
| $1–10m | 20 | 36 (17–47) | 10 | 28 (14–134) |
| Under $1m | 19 | 5 (2–12) | 9 | 11 (7–33) |
| All | 59 | 36 (10–77) | 27 | 32 (10–172) |

Big Spring Area CF left column (a) blank. Column (b) is defined as funds "over which a donor, or person appointed by the donor, had advisory privileges", so it covers advised designated or scholarship funds and not all funds (S2).

**The 15 CFs with an all-funds total [F totals; C shares; I costs]**

| EIN | CF | Band | Total funds | Qual | DAF funds (basis) | Share F | Share A | Share G | F $/acct | A $/acct | F bps | A bps |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 550748246 | Parkersburg Area CF | $10–50m | 500 | over | 80 (Sch D) | 0.160 | 0.312 | 0.421 | 1,335 | 2,607 | 39 | 76 |
| 741839536 | El Paso CF | $10–50m | 600 | more than | 31 (Sch D) | 0.052 | 0.183 | 0.095 | – | – | 352 | 1,241 |
| 582360356 | CF of Northwest Georgia | $10–50m | 200 | over | 154 (Sch D) | 0.770 | 0.455 | 0.867 | 8,762 | 5,176 | 307 | 181 |
| 232765498 | Luzerne Foundation | $10–50m | 400 | over | 105 (Sch D) | 0.263 | 0.552 | 0.320 | 5,728 | 12,041 | 146 | 308 |
| 232773822 | Chester County CF | $10–50m | 430 | over | 232 (Sch D) | 0.540 | 0.381 | 0.468 | 4,647 | 3,282 | 239 | 169 |
| 426060414 | CF of Northeast Iowa | $10–50m | 1,000 | stated | 181 (Sch D) | 0.181 | 0.182 | 0.210 | 2,108 | 2,116 | 123 | 123 |
| 371397503 | Morton CF | $1–10m | 123 | computed | 17 (Sch D) | 0.138 | 0.209 | 0.282 | 1,865 | 2,819 | 100 | 151 |
| 731547637 | Cherokee Strip CF | $1–10m | 345 | stated | 24 (Sch D) | 0.070 | 0.051 | 0.233 | 895 | 654 | 144 | 105 |
| 541950727 | CF for Loudoun and N. Fauquier | $1–10m | 110 | computed | 33 (source, 2022) | 0.300 | 0.366 | 0.267 | 5,810 | 7,095 | 500 | 610 |
| 760821144 | CF of Will County | $1–10m | 68 | stated | 45 (Sch D) | 0.662 | 0.642 | 0.761 | 4,864 | 4,719 | 335 | 325 |
| 831970895 | CF for Oceana County | $1–10m | 200 | + | 64 (Sch D) | 0.320 | 0.213 | 0.142 | 2,157 | 1,438 | 329 | 219 |
| 233096312 | CF for the Twin Tiers | <$1m | 178 | stated | 5 (Sch D) | 0.028 | 0.014 | 0.031 | – | – | 376 | 188 |
| 351934464 | Owen County CF | <$1m | 250 | over | 11 (Sch D) | 0.044 | 0.036 | 0.034 | 1,444 | 1,174 | 276 | 224 |
| 931167214 | Dallas CF (PA) | <$1m | 28 | stated | 14 (Sch D) | 0.500 | 0.196 | 0.232 | 1,612 | 632 | 495 | 194 |
| 474465692 | Caring CF | <$1m | 40 | more than | 3 (Sch D) | 0.075 | 0.085 | 0.042 | 1,923 | 2,176 | 186 | 210 |

Per-account cells are blank where the cost file has no screened account count (El Paso, Twin Tiers). F ÷ A per CF equals share F ÷ share A, because opex and the denominators are the same.

### 2.3 Fund-type counts where published

| EIN | Total | DAF | Designated | FOI | Scholarship | Agency | Unrestricted | Other | Scholarship ÷ total | Sch D DAFs ÷ total |
|---|---|---|---|---|---|---|---|---|---|---|
| 541950727 Loudoun (2022 report) | 110 | 33 | 26 | 21 | 7 | 12 | 10 | 1 | 0.064 | 0.382 |
| 371397503 Morton (directory) | 123 | (17 Sch D) | 48 | 10 | 30 | 12 | 4 | 2 | 0.244 | 0.138 |
| 550748246 Parkersburg | 500+ | | | | 200+ | | | | 0.400 | 0.160 |
| 731547637 Cherokee Strip | 345 | | | | 15 | | | | 0.043 | 0.070 |
| 831970895 Oceana | 200+ | | | | 63 | | | | 0.315 | 0.320 |
| 351934464 Owen County | 250+ | | | | 61 (2022) | | | | 0.244 | 0.044 |
| 931167214 Dallas (PA) | 28 | | | | 18 | | | | 0.643 | 0.500 |

Other scholarship counts (no total): Greater Worcester 150+, Kearney 69, Summit 33 and Eastmont 6 endowed. Agency: Big Spring 5 (FY2024 990).

**[I] Reading:**
- Outside DAFs, the largest groups are designated funds (Morton 48 of 123; Loudoun 26 of 110) and scholarship funds, which are 4–64% of all funds where both counts are known.
- Those funds are many and small, and they are what makes fund count differ from the asset share.
- Loudoun's DAF share of funds (30%, FY2022 source) is below its DAF share of assets (37%). Its Schedule D DAF count rose from 33 (2022 report) to 42 (FY2024), so the 2024 share is likely nearer 0.35–0.38 if the total grew less.

### 2.4 Rule F against rules A and G (same CFs) [I]

| Stratum | Share F | Share A | Share G | F per account | A per account | G per account | F bps | A bps | G bps |
|---|---|---|---|---|---|---|---|---|---|
| $10–50m (n=6; 5 per account) | 0.222 (0.165–0.470) | 0.347 | 0.371 | **$4,647** ($2,108–$5,728) | $3,282 | $4,027 | **193** (129–290) | 175 | 193 |
| $1–10m (n=5) | 0.300 (0.138–0.320) | 0.213 | 0.267 | **$2,157** ($1,865–$4,864) | $2,819 | $3,806 | **329** (144–335) | 219 | 385 |
| Under $1m (n=4; 3 per account) | 0.059 (0.040–0.181) | 0.060 | 0.038 | **$1,612** ($1,528–$1,768) | $1,174 | $1,071 | **326** (254–406) | 202 | 222 |
| All, unweighted (n=15; 13) | **0.181** (0.072–0.410) | 0.209 | 0.233 | **$2,108** ($1,612–$4,864) | $2,607 | $3,516 | **276** (145–343) | 194 | 215 |
| All, stratum-weighted | | | | $2,108 | $2,607 | | 276 | 194 | 215 |

**Robustness [C]**
- Bootstrap 95% CI of the unweighted median (10,000 resamples, seed 20201): F per account $1,612–$4,864; F bps 144–352; share F 0.070–0.500.
- Using the Schedule D DAF count for Loudoun as well (42 ÷ 110) leaves the medians unchanged: share 0.181, $2,108, 276 bps.
- Adding the 3 endowment-only or cumulative totals (n = 18): share 0.222, $2,016 per account, 257 bps.
- **Representativeness:** the rule-F set's rule-A medians ($2,607; 194 bps) are close to the whole frame ($2,859; 205 bps; n = 549 / 603) and the full sample of 60 ($2,542; 203 bps). The counted CFs are not cheaper or dearer than the tail on rule A.

**Reading [I]**
- **Rule F is the whole-org cost per fund.** Its median is about $2,100 for tail CFs (IQR $1,600–$5,300). It moves far less across bands than cost per DAF dollar does.
  - Under $1m the four CFs sit at $1,444–$1,923 per fund.
  - At $10–50m the spread is wide: Parkersburg $1,335 against El Paso $18,145, whose "more than 600 funds" likely undercounts.
- **Rule F against rule A:**
  - **$10–50m:** both rules give similar cost per DAF dollar (193 vs 175 bps).
  - **Below $10m:** rule F puts more cost on DAFs per dollar than rule A (329 vs 219 bps at $1–10m; 326 vs 202 under $1m).
  - **Reason:** small CFs' DAFs are a larger share of their funds than of their assets. Examples are Dallas (PA), with 14 of 28 funds but 20% of assets, and Oceana, with 64 of 200+ funds but 21% of assets.
  - **What it suggests:** this is the direction the cost note expected if cost is per fund (§2.1, "the true per-account cost at the smallest CFs is above the rule-A figure"). With n = 4–5 per band it is suggestive, not shown.
- **Recomputed tail figures under rule F (central, [I]):**
  - **About $2.1k per DAF account and about 280 bps of DAF assets** (sample medians; weighted medians identical), against rule A's $2.6k and 194 bps on the same CFs.
  - By band: **$4.6k / $2.2k / $1.6k per account and about 190 / 330 / 330 bps.**
  - These do not replace the cost note's frame-wide figures. They come from 15 CFs whose totals are often lower bounds, so the F figures lean high.
  - The per-CF ratio F ÷ A (median 1.03) suggests the frame-wide rule-F median share would be close to rule A's. The difference is in which CFs carry the cost.

---

## 3. Limits
- **n is small:** 15 all-funds totals (4–6 per band), 13 with per-account figures. Bootstrap intervals are wide (F bps 144–352).
- **Totals are often lower bounds** (8 of 15) and rounded (Northeast Iowa "1000 Funds"). Rule-F shares and costs for these are upper bounds.
- **Period mismatch:** totals run from 2021 (Parkersburg) to live 2026 pages, while opex and Schedule D DAF counts are FY2024. Funds grow by a few percent a year at these CFs (Dearborn's endowed funds went 166 → 187 from 2021 to 2024), so the error is modest but one-directional: a later total lowers the share.
- **Definitions vary by CF.**
  - "Funds" may or may not include agency funds, affiliates' funds (Parkersburg includes three affiliates) or pass-through and fiscal-sponsorship funds.
  - A homepage "funds established" figure may be cumulative (Hudson, excluded from the main set).
- **Rule F's own assumption is strong.** Equal cost per fund ignores that DAFs generate more grant transactions than endowed designated funds, as rule G's higher shares show. F and G bracket the activity view.
- **Non-response:** 12 of 60 sampled CFs could not be read under the robots and terms rules or because the site failed, and 19 publish no count. Counted CFs look like the frame on rule A, but publishing a count may correlate with size or staffing within a band.
- **Directory counts:** only Morton was counted, ±1 per type; DAF sections were not counted, by design.
- **No outreach, logins or forms.** Two sites answered with bot challenges (Inland Empire, Sturgis) and were not retried with another client.

---

## 4. Data dictionary: `tail-cf-fund-counts-2026-11-20.csv`

| Column | Meaning | Label |
|---|---|---|
| ein, name | Sponsor EIN and name (cost file) | [F] |
| stratum, size_band_fy2024, stratum_N, stratum_n, weight | Sampling stratum (s0_10_50m, s1_1_10m, s2_lt1m), FY2024 band, stratum size, sample size, weight N/n | [C] |
| usable_cost | `usable` flag from the cost file | [C] |
| daf_assets_fy2024, daf_accounts_fy2024_screened, opex_ex_11f, total_assets_eoy, return_object_id | From `long-tail-operating-cost-2026-11-19.csv` | [F/C] |
| sched_d_tax_period_end, sched_d_daf_count, sched_d_other_funds_count | FY2024 990: TaxPeriodEndDt, Schedule D Part I line 1 column (a) DonorAdvisedFundsHeldCnt and column (b) FundsAndOtherAccountsHeldCnt | [F] |
| website, homepage_robots | Homepage used; robots verdict (all six agents) and HTTP status | [F/C] |
| count_status | counted, endowment_only, cumulative, partial, no_count_found, robots_blocked, bot_challenge, site_unreachable, no_website | [C] |
| source_type, source_url, source_period | annual_report, fund_directory, website_stat, form990_narrative or audit_note; the URL; the period the count describes | [F] |
| count_scope | all_funds, endowment_only, all_funds_cumulative, some_types or grantmaking_funds_only | [C] |
| n_daf, n_designated, n_field_of_interest, n_scholarship, n_agency, n_unrestricted, n_other | Published or directory-computed counts by type (blank = not published) | [F/C] |
| type_qual | Which type counts are lower bounds (e.g. `scholarship_lb`) | [C] |
| n_total_funds, total_basis, total_qual | All-funds total; `stated`, `sum_of_types` or `directory_non_daf_plus_sched_d_daf`; exact, lower_bound, approx or computed | [F/C] |
| daf_count_for_F, daf_count_basis | DAF count used in rule F; `source` or `sched_d_fy2024` | [F] |
| daf_share_F | min(1, DAF funds ÷ total); only for all_funds scope and usable rows | [C] |
| daf_share_F_sched_d | Same, with the Schedule D DAF count as numerator (any scope with a total) | [C] |
| daf_share_A, daf_share_G | Rule A and G shares (cost file) | [C] |
| daf_cost_alloc_F, daf_cost_per_account_alloc_F, daf_cost_bps_daf_assets_alloc_F | opex × share F; ÷ screened accounts; ÷ DAF assets × 10,000 | **[I]** |
| opex_per_fund | opex ÷ total funds | [C] |
| daf_cost_per_account_alloc_A / _G, daf_cost_bps_daf_assets_alloc_A / _G | From the cost file, for comparison | **[I]** |
| quote_check, type_quote_check | Quotes found in the cached source text or HTML (`verified k/n`) | [C] |
| notes | Source notes, conflicts and blocks | – |

---

## 5. Source register
All pages were retrieved on 2026-11-20 with research-script/1.0 after the robots check in §1.6. Quotes are in the script's `FUNDS` table, and every one verified against the cached text (27 sources, all `verified k/k`).

| # | Source | Primary URL | Used for |
|---|---|---|---|
| S1 | IRS Form 990 e-file XML (GivingTuesday mirror), FY2024 returns of all 60 sampled CFs (object ids in the CSV) | `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`, e.g. [Luzerne](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202512799349300406_public.xml), [NW Georgia](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523019349300037_public.xml), [Cherokee Strip](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502789349300005_public.xml), [Big Spring](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533249349300648_public.xml), [Dayton Foundation Depository](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501349349310815_public.xml), [Duluth-Superior](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523079349302892_public.xml), [Paso del Norte](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523149349306462_public.xml) | Schedule D line 1 counts; narrative fund counts (robots.txt 404) |
| S2 | IRS, Instructions for Schedule D (Form 990), Rev. December 2024 | [i990sd.pdf](https://www.irs.gov/pub/irs-pdf/i990sd.pdf) | Column (a) and (b) definitions |
| S3 | Parkersburg Area CF, 2021 annual report; scholarships page | [PACF_AnnualReport2021.pdf](https://stdidpacfwvprod.blob.core.windows.net/pacfwv/documents/publications/Annual-Reports/PACF_AnnualReport2021.pdf); [scholarships](https://pacfwv.com/initiatives/scholarships) | Total 500+; scholarship 200+ |
| S4 | El Paso CF, Report to the Community (2023) | [report-to-the-community](https://www.epcf.org/who-we-are/report-to-the-community) | Total 600+ |
| S5 | Hudson CF homepage | [myhcf.org](https://www.myhcf.org/) | 250+ funds established (cumulative) |
| S6 | Chester County CF homepage | [chescocf.org](https://www.chescocf.org/) | Total 430+ |
| S7 | CF of Northeast Iowa homepage | [cfneia.org](https://www.cfneia.org/) | Total 1,000 |
| S8 | Greater Worcester CF, scholarship funds page | [our-scholarship-funds](https://greaterworcester.org/for-students/scholarships-overview/our-scholarship-funds) | Scholarship 150+ |
| S9 | Morton CF, categorized funds directory; homepage | [categorized-funds](https://www.mortoncommunityfoundation.org/categorized-funds); [home](https://www.mortoncommunityfoundation.org/) | Directory counts by type; "more than 150 endowment funds" |
| S10 | Summit Foundation, scholarship page | [apply-for-a-scholarship](https://summitfoundation.org/students/apply-for-a-scholarship) | Scholarship 33 |
| S11 | Cherokee Strip CF homepage | [cherokeestripcf.com](https://www.cherokeestripcf.com/) | Total 345 |
| S12 | Kearney Area CF, scholarships PDF (Jan 2026) | [90548d_aea5…pdf](https://www.kearneyfoundation.org/_files/ugd/90548d_aea5b0537831467e85951a6db7f07ac7.pdf) | Scholarship 69 |
| S13 | CF for Loudoun and Northern Fauquier, 2022 Report to the Community | [2022-Report-to-the-Community.pdf](https://communityfoundationlf.org/wp-content/uploads/2023/09/2022-Report-to-the-Community.pdf) | Counts for all seven types |
| S14 | CF of Will County, view all funds | [view-all-funds](https://willcountycf.org/funds/view-all-funds/) | Total 68 |
| S15 | Dearborn CF, 2024 annual report | [2024-DCF-Annual-Report](https://www.dearborncf.org/wp-content/uploads/2026/02/2024-DCF-Annual-Report-12-2025-1.pdf) | 187 endowment funds |
| S16 | CF for Oceana County, our funds; scholarships | [our-funds](https://oceanafoundation.org/give/our-funds/); [scholarships](https://oceanafoundation.org/scholarships/) | Total 200+; scholarship 63 |
| S17 | Emporia CF, types of funds | [types-of-funds.cfm](https://www.emporiacf.org/types-of-funds.cfm) | DAFs set up since 1996 (cumulative) |
| S18 | CF for the Twin Tiers homepage | [twintierscf.org](https://www.twintierscf.org/) | 178 funds in 2025 (counter) |
| S19 | Eastmont CF, 2026 presentation | [ecf-2026-presentation.pdf](https://www.eastmontcf.com/s/ecf-2026-presentation.pdf) | 6 endowed scholarship funds |
| S20 | Owen County CF homepage; 2022 annual report | [owencountycf.org](https://www.owencountycf.org/); [a8e52d_772d…pdf](https://www.owencountycf.org/_files/ugd/a8e52d_772d975677cc4b5aa53cdb12d6e8b8a4.pdf) | Total 250+; scholarship 61 |
| S21 | Dallas CF (PA) homepage; scholarships page | [dallascommunityfoundation.com](https://dallascommunityfoundation.com/); [scholarships](https://dallascommunityfoundation.com/scholarships/) | Total 28; scholarship 18 |
| S22 | Chippewa County CF, FY2025 audited statements | [CCCF-12.31.25…pdf](https://www.chippewacountycommunityfoundation.org/wp-content/uploads/2026/11/CCCF-12.31.25-Audited-Financial-Statements.pdf) | About 75 endowed funds |
| S23 | Caring CF homepage | [ccfks.org](https://www.ccfks.org/) | Total 40+ |
| R1 | Repo: `long-tail-operating-cost-2026-11-19.csv`, `b45n33-long-tail-operating-cost.md` | – | Frame, opex, rules A and G, accounts, DAF assets |
| R2 | Repo: `cf-vendor-map-by-ein-v2.csv` | – | Homepages |

---

## Appendix: reproduce
```
python3 -I scripts/mission_tail_cf_fund_counts.py . --task sample
python3 -I scripts/mission_tail_cf_fund_counts.py . --task schedd --cache-dir CACHE --fetch
python3 -I scripts/mission_tail_cf_fund_counts.py . --task crawl  --cache-dir CACHE --fetch
python3 -I scripts/mission_tail_cf_fund_counts.py . --task build  --cache-dir CACHE
```
The cache (page text, robots log, Schedule D extracts) is kept outside the repository. Without it, `build` cannot re-verify quotes or recompute the Morton directory counts. The transcribed values in the script are kept either way.
