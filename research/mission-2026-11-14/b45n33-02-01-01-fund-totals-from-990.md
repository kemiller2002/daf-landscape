# P-B45N33-02-01-01: fund totals from Form 990 narratives across the whole tail-CF frame, and rule F on a larger n

**Date:** 2026-11-20 · **Task id:** b45n33-02-01-01 · **Queue item:** P-B45N33-02-01-01 (from [b45n33-02-01-tail-cf-fund-counts.md](b45n33-02-01-tail-cf-fund-counts.md), validated in wave 47A)

**Outputs**
- [`data/mission-2026-11-14/fund-totals-from-990-2026-11-20.csv`](../../data/mission-2026-11-14/fund-totals-from-990-2026-11-20.csv): 641 rows, one per tail CF. It holds hit counts by class, the selected all-funds total, the Schedule D DAF count from the same return, the hand-check verdict, and rule F beside rules A and G. Counts only: the file holds no fund or donor names.
- [`scripts/mission_fund_totals_from_990.py`](../../scripts/mission_fund_totals_from_990.py): stdlib only, functional style. It imports `mission_tail_cf_fund_counts.py` (and through it `mission_long_tail_fee_census.py`) without modifying either. It prints every table in this note.
- [`data/mission-2026-11-14/queue-proposals-b45n33-02-01-01.csv`](../../data/mission-2026-11-14/queue-proposals-b45n33-02-01-01.csv): 5 follow-ups.

**Labels:** **[F]** filed value · **[C]** script computation · **[I]** inference. Every allocated DAF cost is **[I]**. This is research, not legal, tax or accounting advice.

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **Coverage** | Of 641 tail CFs, **36 (5.6%)** state an all-funds total in Part III or Schedule O of a FY2022–24 990. By band: 18 of 207 ($10–50m, 8.7%), 15 of 272 ($1–10m, 5.5%), 3 of 162 (under $1m, 1.9%). Adding Schedule A Part VI and Schedule D Part XIII text gives 40 [C]. | High [C] |
| **Search size** | 1,913 returns (one per EIN-FY), all XML read. 24,831 Part III and Schedule O text fields. 284 regex hits, of which 102 were classed as all-funds totals, in 95 returns [C]. | High [C] |
| **Precision (hand check of every CF-level total)** | **35 of 36** are statements of the filer's total fund count (0.972; Wilson 95% 0.858–0.995). 34 of 36 were right as extracted. One was corrected: Northern Alleghenies reports two affiliates, 257 + 81 = 338. One is ambiguous: Billings, "over 50 funds for charities". A random 40 of the hits classed as *not* totals were all correct exclusions (0 of 40 missed). None of the 17 spelled-out number phrases is a total [C]. | High [C] |
| **DAF share of all funds (rule-F share)** | Median **0.245** (IQR 0.130–0.352; n = 34; bootstrap 95% CI 0.170–0.290). The DAF count comes from Schedule D of the *same* return. The same CFs have rule A **0.178** and rule G **0.356**. Band-weighted: F 0.195, A 0.133, G 0.272 [C]. | Medium [C]; 16 of 34 totals are lower bounds |
| **Rule F cost per DAF account** | **[I] $4,500** median (IQR $2,832–$6,776; n = 31; CI $3,536–$5,215). The same CFs have rule A **$3,518** and rule G **$6,707**. Band-weighted: F $4,035, A $1,940, G $3,825. | Low–medium [I] |
| **Rule F cost per DAF dollar** | **[I] 258 bps** median (151–490; n = 34; CI 204–371). The same CFs have rule A **203 bps** and rule G **323 bps**. Band-weighted: F 307, A 181, G 338 bps. | Low–medium [I] |
| **F against A and G per CF** | F ÷ A has a median of **1.13** (0.88–1.59), and **F > A at 24 of 34**. F ÷ G has a median of **0.70** (0.47–0.98). Rule F sits between the asset rule and the grant rule [C]. | Medium [C] |
| **Does the larger n change the 02-01 reading?** | **[I] It firms up the direction and moves the level.** DAFs are a larger share of funds than of assets at most tail CFs; on 15 web totals the per-CF F ÷ A was 1.03 and F > A at 8 of 15. The 990 set leans toward the $10–50m band (17 of 34), so its per-account costs are higher than the 02-01 sample's ($4,500 vs $2,108). Per DAF dollar the two sets agree (258 vs 276 bps). The under-$1m band is thin (n = 3) and dominated by CFs with many tiny DAFs. | Low–medium [I] |
| **Whole-org opex per fund** | **$4,398** median ($2,768–$6,074; n = 34) [C]. The 15 web-sourced CFs had $2,108. | Medium [C] |

---

## 1. Method

### 1.1 Frame and returns
- **Frame:** the 641 tail CFs of `long-tail-operating-cost-2026-11-19.csv` (`group = tail_cf`), as in b45n33-02-01. Bands: $10–50m (`t10_50`, N = 207), $1–10m (`t1_10`, N = 272), under $1m (`t0_1` + `zero`, N = 162).
- **Returns:** every FY2022, FY2023 and FY2024 return of those EINs listed in `form990-returns-schedule-d-harvest-full.csv` or `sponsor-cost-structure.csv` (1,920 object ids). Where an EIN-FY had more than one return, the one with the latest `return_ts` was kept, as in the cost note. That leaves **1,913 returns**, and the XML of all 1,913 was read.
- **XML source:** the GivingTuesday mirror of IRS e-file XML (S1). 1,912 files came from local caches of that mirror written by earlier repo tasks (`{object_id}.xml` directories and `get()`-style JSON records). One file was fetched from the mirror through the robots-checked `get()` of `mission_tail_cf_fund_counts.py` (§1.6).

### 1.2 Text searched
- **Main (as specified):**
  - Part III: `IRS990/MissionDesc` (line 1), `IRS990/Desc` (line 4a), and `ProgSrvcAccomActy2Grp`, `…3Grp` and `…OtherGrp/Desc` (4b–4d).
  - Schedule O: `SupplementalInformationDetail/ExplanationTxt`.
  - In all, 24,831 fields.
- **Extension (reported separately):**
  - Schedule D Part XIII and Schedule A Part VI explanations, 5,153 fields.
  - Exploration showed that some CFs state their total only there. Examples are Weld ("over 175 separately identifiable funds", Schedule A Part VI) and Ventura ("fiduciary over more than 600 individual funds", Schedule D Part XIII).
- **DAF count:** Schedule D Part I line 1(a), `DonorAdvisedFundsHeldCnt`, read from the same XML.

### 1.3 Regex and scope classes
- **P1:** `<qualifier?> N<+?> <0–3 adjectives> funds`. Adjectives must come from a fixed list, such as individual, charitable, component, active or philanthropic, or be fund-type words. This drops "3 million to their funds" and financial-statement lines.
- **P2:** "total (number of) (active) funds (under management) to/of N" and "total under management to N". For example, "bringing the total number of funds to 370" and "bringing the total under management to 211".
- **P3:** a run of 4 or more "N <type> fund(s)" items joined only by commas, "and" or "&" is summed as a total by type. One CF qualifies: 59 agency + 17 endowment + 42 DAF + 7 corporate advised + 3 scholarship + 1 annuity + 7 pass-through = 136.
- **Classes**, assigned in this order:

| Class | Rule | Main-part hits |
|---|---|---|
| other | money ($ before, "million"), a year 1990–2030 with no qualifier, n < 2 or > 5,000, a financial line ("held for", "transferred", "revenue") or an adjective not on the list | 22 |
| new_funds | "new", "newly" or "established" among the adjectives | 39 |
| endowment_only | an endow*/permanent adjective, or "endowment consists of N funds", "deemed as endowment", "held on donor's behalf" | 20 |
| type_specific | a fund-type adjective (DAF, scholarship, agency, designated, FOI, custodial, fiscal, partner, pass-through …), or "<type> funds … (a total of N" | 90 |
| grantmaking | "grants … from/through N funds", "N funds that award / hosted" | 11 |
| **all_funds** | none of the above | **102** |

- **Qualifiers:** over, more than and + are `lower_bound`; approximately and about are `approx`; nearly and almost are `upper_bound`; anything else is `stated`. As in 02-01, a lower-bound total makes share F and rule-F cost **upper bounds**.
- **Per return:** the largest all-funds hit is used (`multi_total` flags returns with more than one). **Per CF:** the latest FY with a total (2024, else 2023, else 2022) is used, paired with **the same return's** Schedule D DAF count. Unlike 02-01, the numerator and denominator therefore describe the same fiscal year.

### 1.4 Hand check
- **Every CF-level total that the extraction selects** (36 main and 4 extension) was read in context by the analyst. Verdict and reason are in `HANDCHECK` in the script:
  - **ok:** a statement of all funds the filer holds or administers;
  - **corrected:** an all-funds statement whose total had to be fixed;
  - **ambiguous**;
  - **reject**.
- Precision is (ok + corrected) ÷ n at the level that feeds rule F.
- **Missed totals:** a seeded random 40 (seed 2026112002) of the hits classed as *not* all-funds were read (`EXCL_CHECK`). Separately, every spelled-out number + "funds" phrase in the main parts (17 hits, 12 distinct) was listed and read.
- Only ok and corrected totals enter rule F.

### 1.5 Rule F, beside A and G
The rules are defined as in 02-01 §1.5:
- **F:** DAF cost = `opex_ex_11f` (FY2024, cost file) × min(1, DAF funds ÷ all funds).
- **Per account:** ÷ screened FY2024 DAF accounts.
- **Per DAF dollar:** ÷ FY2024 DAF assets (bps).
- **A and G:** taken from the cost file for the same CFs.

Two summaries are reported:
- **Plain medians** over the F set.
- **Band-weighted medians**, with weight = frame N of the band ÷ F-set n of the band, so the F set's lean toward large CFs is undone. Under $1m has only 3 CFs at weight 54 each.

All allocated figures are [I].

### 1.6 Network conduct
- **Mirror fetch:** one request, to `gt990datalake-rawdata.s3.amazonaws.com`, on 2026-11-20 at 05:41:51 UTC. robots.txt returned 404 (none published, so no rule applies to research-script/1.0 or any Claude or anthropic agent). Logged to `<cache>/robots_log.tsv`.
- **No other hosts.** sec.gov, the off-limits hosts and the sites whose terms ban extraction were not used. No logins, no forms, user agent "research-script/1.0".
- **Caches:** the local XML caches are copies of the same mirror, written by earlier repo tasks under the same robots rule.

---

## 2. Results

### 2.1 Coverage [C]

| Band | Frame N | With total (Part III / Sch O) | Share of band | Rule-F set | Lower-bound totals in F set |
|---|---|---|---|---|---|
| $10–50m | 207 | 18 | 0.087 | 17 | 10 |
| $1–10m | 272 | 15 | 0.055 | 14 | 5 |
| Under $1m | 162 | 3 | 0.019 | 3 | 1 |
| **All** | **641** | **36** | **0.056** | **34** | **16** |

- **Where the totals come from:** 33 from Part III and 3 from Schedule O. The FY of the total is 2024 for 33 CFs, 2023 for 1 and 2022 for 2.
- **Qualifiers:** 16 stated, 17 lower bound, 2 approximate. The 136 is a sum of types.
- **Two dropped from the F set:** Billings is ambiguous, and CF of Northern Illinois's FY2024 return has no Schedule D line 1(a) count.
- **Extension:** Schedule D XIII and Schedule A VI add 4 CFs (Legacy Foundation IN, Portland Foundation IN, Ventura County CF, Weld CF), giving 40 with a total.
- **[C] 990 narratives are a thinner source than CF websites.** Websites gave 15 of 60 sampled CFs (25%); 990 narratives give 5.6% of the frame. Because they cover the whole frame, they still yield more than twice as many totals (34 against 15) with no crawling.
- **Agreement with 02-01:**
  - Of the 60 CFs sampled in 02-01, the extractor finds totals for exactly the two whose 02-01 total came from a 990 narrative: Luzerne (over 400) and NW Georgia (over 200). Both match.
  - It finds no totals for the other 58, which fits 02-01's finding that only those two had 990 counts.
  - Morton, Dallas (PA) and the other 02-01 totals came from websites, so this pass cannot settle their inconsistencies. Luzerne's 990 again says "over 400", in each of FY2022–24.

### 2.2 Precision [C]
| Check | Result |
|---|---|
| CF-level totals read in context | 36 main + 4 extension |
| All-funds statement (ok + corrected) | **35 / 36 = 0.972** (Wilson 95% 0.858–0.995); extension 39 / 40 |
| Right as extracted (ok only) | 34 / 36 |
| Corrected | 1: EIN 251859637 (Northern Alleghenies). The filer reports Elk County CF "TOTAL OF 257 CHARITABLE FUNDS" and McKean County CF "TOTAL OF 81 FUNDS", and its Schedule D covers both, so the total is 338 |
| Ambiguous | 1: EIN 204286919 (Billings), "HAS OVER 50 FUNDS FOR CHARITIES". This may mean funds held for charities (agency). Its share would be 28 / 50 = 0.560; excluded |
| Sample of 40 excluded hits | 40 correct exclusions, 0 missed totals: 15 type-specific (including items of by-type lists), 9 endowment-only, 6 new-funds, 3 grantmaking and 7 other. Examples: "THE FOUNDATION'S ENDOWMENT CONSISTS OF 533 INDIVIDUAL FUNDS" (endowment); "MADE 12,699 GRANTS … FROM 1,283 FUNDS" (grantmaking) |
| Spelled-out phrases (17 hits) | None is an all-funds total. They include "TWENTY-NINE OF THESE FUNDS ARE DONOR ADVISED FUNDS", "SIX NEW FUNDS" and "THREE REGIONAL FUNDS" |

**Recall limit:** the checks above test the classifier, not phrasing the regex never matches. Recall against an independent count of totals in the narratives is not measured. Totals that appear only in other 990 parts were caught only by the extension (4 CFs).

### 2.3 Rule F against rules A and G (same CFs) [I]

| Band | n | Share F | Share A | Share G | F $/acct | A $/acct | G $/acct | F bps | A bps | G bps |
|---|---|---|---|---|---|---|---|---|---|---|
| $10–50m | 17 | 0.264 (0.195–0.387) | 0.261 | 0.458 | **$5,159** ($4,500–$7,830) | $5,176 | $9,868 | **255** (165–344) | 201 | 346 |
| $1–10m | 14 (11 per acct) | 0.184 (0.115–0.280) | 0.131 | 0.233 | **$2,703** ($1,896–$5,470) | $2,247 | $3,825 | **215** (106–508) | 208 | 210 |
| Under $1m | 3 | 0.078 (0.064–0.229) | 0.006 | 0.049 | **$4,035** ($3,864–$4,166) | $420 | $1,121 | **1,112** (1,017–5,592) | 140 | 574 |
| **All, unweighted** | 34 (31) | **0.245** (0.130–0.352) | 0.178 | 0.356 | **$4,500** ($2,832–$6,776) | $3,518 | $6,707 | **258** (151–490) | 203 | 323 |
| All, band-weighted | 34 | 0.195 | 0.133 | 0.272 | $4,035 | $1,940 | $3,825 | 307 | 181 | 338 |

Medians, with IQR in brackets. Three CFs lack a screened account count, so per-account n is 31.

**Per CF [C]:**
- F ÷ A: median 1.13 (0.88–1.59); F > A at 24 of 34.
- F ÷ G: median 0.70 (0.47–0.98).
- Whole-org opex per fund: $4,398 ($2,768–$6,074).
- Total funds: median 296 (172–372). Schedule D DAFs: median 54 (37–102).

**Examples (filed counts [F], shares [C]):**

| Band | Sched D DAFs ÷ total = share F | Share A |
|---|---|---|
| $10–50m: CF for the Greater Capital Region, FY2024 | 213 ÷ "more than 472" = 0.451 | 0.267 |
| $10–50m: Communities of Coastal Georgia | 87 ÷ 160 = 0.544 | 0.739 |
| $1–10m: CF of Southern Wisconsin | 96 ÷ 871 = 0.110 | 0.106 |
| Under $1m: Phelps County CF | 38 ÷ "approximately 100" = 0.380 | 0.005 |

Coastal Georgia is a case where DAFs hold a larger share of assets than of funds.

### 2.4 Robustness [C]

| Variant | n | Share F | Share A | F $/acct | A $/acct | F bps | A bps |
|---|---|---|---|---|---|---|---|
| Main (above) | 34 | 0.245 | 0.178 | $4,500 | $3,518 | 258 | 203 |
| Stated or approx totals only (drop lower bounds) | 17 | 0.162 | 0.125 | $4,036 | $2,944 | 280 | 212 |
| FY2024 totals only (same FY as opex) | 31 | 0.256 | 0.187 | $4,577 | $3,453 | 261 | 205 |
| Drop the multi-total return (Northern Alleghenies) | 33 | 0.249 | 0.170 | $4,577 | $3,778 | 261 | 205 |
| Extension (+ Sch D XIII / Sch A VI), n = 38 | 38 | 0.223 | 0.171 | $4,577 | $4,270 | 241 | 198 |

- **Bootstrap 95% CIs** (10,000 resamples, seed 20201): share F 0.170–0.290; F per account $3,536–$5,215; F bps 204–371.
- **No CF in the F set has a DAF count above its total.** The Dallas-type inconsistency of 02-01 does not recur here, because numerator and denominator come from one return.
- **Representativeness:** the F set's rule-A medians ($3,518; 203 bps) compare with the whole frame's ($2,859, n = 549; 205 bps, n = 603). Per DAF dollar the F set looks like the frame. Per account it is dearer, because half the F set is in the $10–50m band, against 32% of the frame. The band-weighted row corrects for that, and it widens the F–A gap per account ($4,035 vs $1,940).

### 2.5 Reading [I]
- **Rule F sits between A and G:**
  - **Share:** at the median, DAFs are about a quarter of the funds (0.245) but under a fifth of the assets (0.178), while they make about a third of the grants (0.356).
  - **Per DAF dollar:** rule F (258 bps) is about 1.3 times rule A (203) and 0.8 times rule G (323).
  - **Per CF:** the ordering A < F < G holds for most CFs (F > A at 24 of 34; F < G at 26 of 34, F ÷ G median 0.70).
- **The size gradient seen in 02-01 is there, but rests on few CFs:**
  - At **$10–50m**, F ≈ A per account ($5,159 vs $5,176), and F is above A per dollar (255 vs 201 bps).
  - At **$1–10m**, F is modestly above A ($2,703 vs $2,247; 215 vs 208 bps).
  - **Under $1m**, F is several times A (1,112 vs 140 bps), but n = 3. All three CFs (Stateline, Polk County, Phelps County) have far more funds than DAF dollars would suggest, and Phelps alone gives 10,073 bps under F. This band should not be quoted without the n.
- **Against 02-01:**
  - **Agreement:** per DAF dollar the two sets agree (258 vs 276 bps), as does the conclusion that F ≥ A at the median CF (F ÷ A of 1.13 here against 1.03).
  - **Difference:** per account the 990 set is about twice as high ($4,500 vs $2,108), because it holds larger CFs and fewer of the cheap small ones. The 02-01 per-account figure is not confirmed as a frame-wide value. The band-weighted rule-F estimate here is about **$4.0k per DAF account and about 310 bps**, against rule A's $1.9k and 181 bps on the same CFs.
- **What it means for the cost note:**
  - If cost is per fund, the cost note's rule-A tail figures understate DAF cost per account. On these 34 CFs the understatement is about 1.1–2 times, depending on weighting.
  - The direction is now supported by n = 34 rather than 15. The level stays an inference: nearly half the totals (16 of 34) are "over N" figures that push F up, and dropping them gives share 0.162 against A 0.125, the same ratio of about 1.3.

---

## 3. Limits
- **Low coverage and selection.** Only 5.6% of tail CFs state a total in Part III or Schedule O, falling to 1.9% under $1m. CFs that write fuller narratives may be larger or better staffed, so the F set leans to the $10–50m band. Band weighting helps but leans on 3 CFs under $1m.
- **Lower bounds.** 16 of 34 rule-F totals (17 of the 36 CFs with a total) are "over / more than / +" figures, so their shares and rule-F costs are upper bounds. Several repeat unchanged across years (Luzerne "over 400" in FY2022–24), which suggests stale round numbers (P-B45N33-02-01-01-02).
- **Recall is not measured.** The precision checks test the classifier. A total phrased in a way the regex does not match (for example "the number of funds we hold grew to …") would be missed. The extension shows that some totals sit in other 990 parts.
- **Definitions vary.** "Funds" may include affiliates' funds (Northern Alleghenies; Capital Region "more than 472"), agency, pass-through or fiscal-sponsorship funds. Schedule D column (a) may count dormant or tiny DAFs, as Phelps County's 38 DAFs at 0.5% of assets suggest (P-B45N33-02-01-01-03).
- **Period.** Totals and DAF counts come from one return. 31 of 34 are FY2024, matching opex; 3 are FY2022 or FY2023 and are applied to FY2024 opex and accounts.
- **Rule F's assumption.** Equal cost per fund is strong. Rule G's higher shares show that DAFs are more transaction-heavy than the average fund.
- **One correction and one exclusion are judgment calls.** Northern Alleghenies was summed and Billings was excluded. Neither moves the medians beyond the robustness rows.
- **Caches.** 1,912 of 1,913 XML files came from local caches of the mirror, written by earlier tasks. Rerunning needs those caches or a robots-checked refetch (`--fetch`). The script reads the XML afresh on every run, so its results do not depend on stored extracts.

---

## 4. Data dictionary: `fund-totals-from-990-2026-11-20.csv`
One row per tail CF (641). Blank = not applicable or not found.

| Column | Meaning | Label |
|---|---|---|
| ein, name | Sponsor EIN and name (cost file) | [F] |
| band, size_band_fy2024 | $10–50m / $1–10m / Under $1m; FY2024 band code | [C] |
| usable_cost | `usable` flag from the cost file | [C] |
| returns_fy2022_24, returns_xml_ok | EIN-FY returns indexed (latest per FY); returns whose XML parsed | [C] |
| narrative_fields | Part III + Schedule O text fields searched, summed over the CF's returns | [C] |
| hits_all_funds … hits_other | Regex hits in Part III + Schedule O by class (all_funds, endowment_only, type_specific, new_funds, grantmaking, other), summed over returns | [C] |
| total_fy, total_object_id, total_period_end | FY, IRS e-file object id and TaxPeriodEndDt of the return giving the selected total | [F] |
| total_part, total_pattern | part_iii or sched_o; P1, P2 or P3 (sum of types) | [C] |
| n_total_funds_extracted | Total as extracted | [F] |
| n_total_funds | Total after the hand check (differs only where `handcheck = corrected`) | [F/C] |
| total_qual | stated, lower_bound, approx, upper_bound or sum_of_types | [C] |
| multi_total | 1 if the return had more than one distinct all-funds hit | [C] |
| fys_with_total | FYs (2024, 2023, 2022) whose return has a total | [C] |
| sched_d_daf_count_same_return | Schedule D Part I line 1(a) DonorAdvisedFundsHeldCnt in the same return | [F] |
| daf_gt_total | 1 if the DAF count exceeds the total | [C] |
| handcheck | ok, corrected, ambiguous, reject (analyst reading; reasons in the script) | [C] |
| daf_share_F | min(1, DAF count ÷ total); only for ok/corrected, usable rows with a DAF count | [C] |
| daf_share_A, daf_share_G | Rule A and G shares (cost file) | [C] |
| opex_ex_11f, daf_accounts_fy2024_screened, daf_assets_fy2024 | From the cost file (FY2024) | [F/C] |
| daf_cost_alloc_F, daf_cost_per_account_alloc_F, daf_cost_bps_daf_assets_alloc_F | opex × share F; ÷ screened accounts; ÷ DAF assets × 10,000 | **[I]** |
| opex_per_fund | opex ÷ total funds | [C] |
| daf_cost_per_account_alloc_A / _G, daf_cost_bps_daf_assets_alloc_A / _G | From the cost file | **[I]** |
| *_ext columns | Same fields when Schedule D Part XIII and Schedule A Part VI text are also searched (extension) | as above |
| prior_02_01_total, prior_02_01_status | Total and status in b45n33-02-01 (sampled CFs only) | [F/C] |

---

## 5. Source register

| # | Source | Primary URL | Used for |
|---|---|---|---|
| S1 | IRS Form 990 e-file XML, GivingTuesday mirror (robots.txt 404); 1,913 FY2022–24 returns of the 641 tail CFs (object ids in `total_object_id` and the repo harvest files) | `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`, e.g. [TFEC FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202540839349300504_public.xml), [Capital Region FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202512729349300936_public.xml), [Northern Alleghenies FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501719349300820_public.xml), [The Community Foundation for … (sum of types) FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523179349300617_public.xml), [Billings FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501919349300600_public.xml), [Phelps County FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202422689349300037_public.xml), [Weld FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501409349301380_public.xml), [Ventura FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502249349300445_public.xml), [Luzerne FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202512799349300406_public.xml) | Narrative fund totals; Schedule D line 1(a) DAF counts |
| S2 | IRS, Instructions for Schedule D (Form 990) (not re-fetched; read in 02-01) | [i990sd.pdf](https://www.irs.gov/pub/irs-pdf/i990sd.pdf) | Line 1 column (a) definition |
| S3 | IRS, Instructions for Form 990 (Part III layout; not re-fetched) | [i990.pdf](https://www.irs.gov/pub/irs-pdf/i990.pdf) | Part III lines 1 and 4a–4d |
| R1 | Repo: `long-tail-operating-cost-2026-11-19.csv`, `b45n33-long-tail-operating-cost.md` | – | Frame, opex, rules A and G, accounts, DAF assets |
| R2 | Repo: `form990-returns-schedule-d-harvest-full.csv`, `sponsor-cost-structure.csv` | – | Object ids of the FY2022–24 returns and return timestamps |
| R3 | Repo: `tail-cf-fund-counts-2026-11-20.csv`, `b45n33-02-01-tail-cf-fund-counts.md` | – | 02-01 totals for the overlap check; rule F definition |

---

## Appendix: reproduce
```
python3 -I scripts/mission_fund_totals_from_990.py . --xml-dir XMLCACHE [--xml-dir …] [--json-cache JSONCACHE …] \
    --cache-dir CACHE [--fetch]                    # build: writes the CSV, prints the tables
python3 -I scripts/mission_fund_totals_from_990.py . … --task hits     # every selected total with its snippet (for the hand check)
python3 -I scripts/mission_fund_totals_from_990.py . … --task sample   # the seeded sample of excluded hits
```
The XML caches are kept outside the repository. Without them, `--fetch` refetches from the mirror after the six-agent robots check.
