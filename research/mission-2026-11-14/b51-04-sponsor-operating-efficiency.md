# b51-04: Operating efficiency and scale economies at DAF sponsors, FY2021–FY2024

**Date:** 2026-11-20 · **Task:** b51-04

**Outputs**
- [`data/mission-2026-11-14/sponsor-operating-efficiency-2026-11-20.csv`](../../data/mission-2026-11-14/sponsor-operating-efficiency-2026-11-20.csv): 832 sponsor-year rows, plus regression, trend, band and comparison rows (2,267 rows in all).
- [`scripts/mission_sponsor_efficiency.py`](../../scripts/mission_sponsor_efficiency.py): stdlib only, functional style. It imports the earlier scripts read-only and modifies none of them (§1.5).
- [`data/mission-2026-11-14/queue-proposals-b51-04.csv`](../../data/mission-2026-11-14/queue-proposals-b51-04.csv): P-B5104-01 to P-B5104-06.

**Labels:** **[F]** value as filed · **[C]** script computation · **[I]** inference or classification. Dollars are nominal. This is research, not legal, tax or accounting advice.

---

## 0. Bottom line

| Question | Answer | Confidence |
|---|---|---|
| **Are there scale economies?** | **Yes, for sponsors that employ their own staff.** Holding the year fixed, a 1% larger sponsor (in both DAF assets and accounts) has this much more operating cost [C]:<br>- **community foundations (CFs): 0.64%** (SE 0.05; 451 sponsor-years, 113 CFs; r² 0.69);<br>- **nationals, excluding processors, any staffing: 0.49%** (SE 0.08; 98 sponsor-years, 25 sponsors).<br>The full FY2022–24 universe gives 0.56% for CFs (703 CFs). Every estimate is well below 1. | High [C] on the coefficients; Medium [I] on reading them as cost curves |
| **What drives CF cost?** | **The size of the whole foundation, not of its DAF book.** When total assets are added to the model, they carry the elasticity (0.78, SE 0.09), and the two DAF terms together fall to 0.03 (SE 0.08) [C]. DAFs are 28–63% of a CF's balance sheet, by size band. CF cost is mostly a whole-organisation cost. | High [C] |
| **Single-issue sponsors** | **There is no usable DAF cost curve.** The DAF-scale elasticity is 0.07 (SE 0.16), and opex follows total assets (1.14) [C] (committed-CSV values; the earlier figures came from a superseded run). [V wave 51A] Their Part IX pays for the charity's mission, not for its DAFs. | High [C] |
| **Affiliate-staffed sponsors** | **14 of the top 50 report zero employees in FY2024 and have documented affiliate staffing**, the 14 that, with American Gift Fund, make up the 15 zero-employee top-50 sponsors in b49-05. Thrivent (one employee) is also affiliate-staffed in substance, and American Gift Fund (zero employees) has no evidence either way.<br>- **Lower cost on their own 990:** after controlling for scale and type, affiliate- and zero-staff sponsors report **84% less** operating cost (dummy −1.81, SE 0.39) [C]. [V wave 51A]<br>- **What the 990 records:** at the median such top-50 national, **63% of FY2024 opex is Part IX 11a + 11g fees**, which is the price paid to the parent [C].<br>- **Scaling:** the affiliated-commercial group's opex scales **one-for-one** with DAF scale (elasticity 1.01, SE 0.08, r² 0.92) [C]. That is the pattern of asset-based fee contracts [I].<br>- **Per-employee metrics are blank for all of them.** Naively computed, they would show 3,782 accounts per employee at T. Rowe Price (FY2021, one employee) and 8,346 at Thrivent (FY2024). | High [F/C]; Medium [I] |
| **Levels, FY2024 (medians)** | **Top-50 nationals:** 23 bps of DAF assets and $1,395 per DAF account.<br>**Top-50 CFs:** 162 bps whole-organisation, or 102 bps and $12,036 per account with the asset-share allocation (rule A).<br>**CFs by size:** rule-A cost falls from 373 bps (under $10m) to 149 bps ($10–100m), 118 bps ($100m–1bn) and 80 bps ($1bn and over) [C].<br>**Accounts per employee:** about 8–11 at CFs of $10m and over, against 85 at own-staff top-50 nationals (Schwab 578, Vanguard 232) [C]. | High [C] |
| **Trend FY2021→24** | **Efficiency fell at CFs (nominal).** On a balanced panel of 112 own-staff CFs, the median within-sponsor changes are [C]:<br>- operating cost **+35%**;<br>- DAF assets **+9%**;<br>- accounts **+6%**;<br>- employees **+14%**;<br>- cost per DAF dollar **+21%** (median 511 → 557 bps whole-org; rule A 123 → 154 bps);<br>- cost per account **+25%** ($17.3k → $21.4k).<br>At affiliate-staffed affiliated nationals, cost per DAF dollar was flat (+0.5%; 26 → 22 bps). FY2021 year-end asset values sit near a market peak, which flatters the FY2021 bps figures [I]. Deflated by CPI-U (271.0 → 313.7, +15.8%), real opex rose 16.6%, real opex per employee was flat (−0.1%), real opex per account rose 8.0% and opex per DAF grant dollar 0.7%; bps fell 4.0% from FY2022. Most of the bps rise is the FY2021 base and headcount growth. [V wave 51A] | High [C]; the inflation share is not measured |
| **Agreement with repo work** | **The data agree exactly where the populations overlap.**<br>- **Part I line 5 employees:** match on 392 of 392 b49-05 returns and on 183 of 183 compensation returns. Line 25 also matches on all 183.<br>- **Operating cost:** matches b45n33 on 165 of 165 shared returns.<br>- **Top-50 CF rule-A cost:** 102 bps and $12,036 per account, the same as b45n33. Top-50 nationals are 23 bps and $1,357 here, against 24 bps and $1,425 there.<br>- **Elasticities:** the repo's earlier figures (nationals 0.41, FY2024; CF opex on total assets 0.84) bracket this note's estimates. | High [C] |

---

## 1. Method

### 1.1 Population
| Group | Rule | Sponsors |
|---|---|---|
| `top50` | 50 largest by corrected FY2024 DAF assets (`mission_sponsor_compensation.top_sponsors`; same set as b49-05 and the compensation direction) | 50 |
| `sample` | The b49-05 seeded random sample (`random.Random(4905).sample`, 100 of 1,429 FY2024 sponsors ranked 51+ with DAF assets > 0). It is reused so the employee data compare one-to-one | 100 (61 CF, 34 single-issue, 5 national) |
| `supplement` | New seeded draw (`SUPP_SEED = 5104`) from the same frame. It is limited to FY2024 corrected DAF assets of $10m or more, excludes the b49-05 sample, and draws 40 CFs (from 319) with `Random(5104)` and 20 other sponsors (from 155) with `Random(5105)`. It offsets the b49-05 sample's lean towards sponsors under $10m (P-B4905-01). Ranks 54–559; $10.5m–$535.9m | 60 (40 CF, 15 single-issue, 5 national) |

Sponsor type (`sponsor_type`, [I]) is the DAFRC FY2024 type, with two adjustments:
- **`national_affiliated`:** the 12 sponsors that the compensation direction's `SEGMENT` table marks `affiliated_commercial` (Fidelity, Schwab/DAFgiving360, Vanguard, GS, Morgan Stanley, BofA, Raymond James, US Charitable Gift Trust, Ayco, Bessemer, T. Rowe Price, Renaissance).
- **`processor`:** DAFRC Donation Processor subtype.

The other groups are `national_other`, `community_foundation` and `single_issue` (the Single Issue Charity type, all subtypes).

### 1.2 Returns and extraction
- **Locating returns.** Every `RETURN_TYPE = 990` row in IRS `index_2021`–`index_2026` for these EINs whose tax period ends in 2021–2024.
  - FY is the calendar year in which the period ends, the DAFRC convention. b49-05 and the compensation work use the tax year (the year the period begins), so June-FYE sponsors are one year apart in label.
  - One return per EIN × FY. Where two periods end in the same year, the script prefers the sponsor's modal FYE month. This resolves DAFGiving360's FY2021, which has a 2021-06 return and a 2021-12 short-period return. After that it takes the later period, then the highest OBJECT_ID.
- **Coverage.** 832 returns: FY2021 205, FY2022 207, FY2023 210, FY2024 210. Five EIN-FYs have only a 990-EZ or 990-PF. All 832 XMLs parsed [C].
- **Extraction.** `mission_sponsor_cost_structure.extract_cost_stream` (full Part IX by column, Part I, Schedule D Part I, Schedule I counts), same extractor version. Sources:
  - 627 returns from that script's existing extract cache;
  - 112 from local XML copies already in the session caches;
  - 94 FY2021 returns streamed from the GivingTuesday mirror.

### 1.3 Measures (per sponsor-year)
| Measure | Definition |
|---|---|
| Total functional expenses | Part IX line 25 column A [F] |
| Management & general | Part IX line 25 column C [F] |
| **Operating cost (opex)** | Line 25 − lines 1–3 (grants) − line 4 − line 11f (investment-management fees): the repository standard (`cost_row.operating_cost_ex_invest_mgmt`) [C] |
| Core opex (sensitivity) | Opex − line 12 (advertising) − line 11e (professional fundraising). This takes out pass-through items such as Servant Foundation's $219.9m of FY2023 advertising and CAF America's $97.7m of FY2021 fundraising fees [C] |
| Employees | Part I line 5 `TotalEmployeeCnt` [F] |
| DAF accounts, assets, contributions, grants | Schedule D Part I lines 1 and 2–4 as filed. Where blank or zero, the corrected DAFRC value is used and flagged [F] |
| Expense per DAF account; bps of DAF assets | opex ÷ accounts; opex ÷ EOY DAF assets × 10⁴. These are **whole-organisation ceilings** for CFs and single-issue sponsors [C] |
| Rule A (allocated) | opex × min(1, DAF assets ÷ total assets), per account and in bps. This is the b45n33 rule A [I] |
| M&G per account and bps | line 25(C) ÷ accounts or DAF assets [C] |
| Assets, accounts, $ grants, $ contributions per employee | Only where `staffing_model = own_staff` [C] |
| Grants per employee; opex per grant | FY2024 only. Uses the primary stated grant counts in `grant-count-denominators-2026-11-20.csv` (`is_primary = 1`, 12 sponsors in this population). Counts are calendar or fiscal 2024 as labelled; `period_match` in that file gives the overlap [C] |

### 1.4 Affiliate-staffed sponsors (`staffing_model`) [I]
- **Affiliate evidence (sponsor-level, any year):**
  - `segment_affiliated_commercial`, or a `SEGMENT` note naming an affiliate (Greater Horizons/GKCCF, Thrivent);
  - a compensation-direction flag `*_affiliate_staffed`, `top_officer_paid_by_related_org` or `split_org_and_related`;
  - b49-05 Part VI line 3 = Yes (management delegated);
  - **or**, for the year itself, zero staff cost (lines 5–10) with 11a/11g fees paid.
- **`own_staff`:** more than 5 employees, or 1–5 employees with no affiliate evidence.
- **`token_staff_affiliate`:** 1–5 employees **and** sponsor-level affiliate evidence (T. Rowe Price FY2021–22; Thrivent FY2022–24).
- **`affiliate_staffed`:** zero employees with evidence.
- **`zero_employee_unexplained`:** zero employees with none.
- Every model except `own_staff` is analysed separately, and its per-employee metrics are left blank, so that efficiency is not overstated.
- DAFgiving360 and Vanguard have their own employees but buy services from their founder. They stay in `own_staff` with the flag `affiliated_commercial_costs_partly_at_parent`.

### 1.5 Regression
- **Model:** OLS of ln(opex) on ln(DAF assets) and ln(DAF accounts), with FY dummies (FY2021 is the base).
- **Standard errors** are clustered by sponsor (CR1). `scale_elasticity_sum_daf_terms` is the sum of the two DAF coefficients, with its clustered SE and a t-test of H0: sum = 1.
- **Specifications:**
  - M1: assets and accounts;
  - M2: assets only (comparable with the repo's 0.41);
  - M3: management & general as the dependent variable;
  - M4: adds ln(total assets);
  - M5: all sponsors pooled, with an affiliate/zero-staff dummy and type dummies;
  - M6: employees as the dependent variable;
  - M7: core opex;
  - R1: the same M1 on the whole `sponsor-cost-structure.csv` universe for FY2022–24 (employees > 0).
- **Usable rows** (`usable = 1`): opex > 0, DAF assets > 0, a plausible account count (average account $1k–$1bn, not Givinga) and opex of at least 1 bp of DAF assets.
  - 800 of 832 rows qualify.
  - 23 fail the account screen, mainly processors (AOGF, PayPal).
  - 6 have opex under 1 bp (BofA in all four years, The Signatry FY2021, Marion Area CF FY2022).
  - 3 have opex ≤ 0 (FBT for a Brighter Tomorrow).

**Reuse.** Imported read-only:
- `mission_sponsor_compensation` (`panel`, `SEGMENT`);
- `mission_sponsor_governance` (`population`, `scan_xml_cache`);
- `mission_sponsor_cost_structure` (`extract_cost_stream`, `cost_row`, `quantile`);
- `mission_990_contractors` (helpers).

The script writes only its own CSV and its own JSON extract cache (outside the repository).

**Reproduce**
```
python3 scripts/mission_sponsor_efficiency.py . --irs-dir <dir with index_2021..2026.csv> \
    --cache-dir <own extract cache> --extract-cache <…/extract990cost> --xml-cache <dir(s) with {oid}.xml> [--fetch]
```
The script prints coverage, the zero-employee list, every regression, the trends, the comparisons and the grant-count table.

---

## 2. Coverage and flags

| FY | Returns | Usable | own_staff | affiliate_staffed | token_staff_affiliate | zero_employee_unexplained |
|---|---|---|---|---|---|---|
| 2021 | 205 | 196 | 164 | 29 | 1 | 11 |
| 2022 | 207 | 197 | 165 | 27 | 2 | 13 |
| 2023 | 210 | 203 | 167 | 29 | 1 | 13 |
| 2024 | 210 | 204 | 166 | 31 | 1 | 12 |

**Top 50, FY2024 [F/I]**
- **`affiliate_staffed` (14):** Fidelity, GS DAPF, Morgan Stanley GIFT, BofA, Ayco, Bessemer, Raymond James, Renaissance, US Charitable Gift Trust, T. Rowe Price, Dechomai, Greater Horizons, The Signatry and UCLA Foundation.
- **`token_staff_affiliate` (1):** Thrivent.
- **`zero_employee_unexplained` (1):** American Gift Fund.
- **The other 34 are `own_staff`.**
- **Match with b49-05:** the 15 zero-employee sponsors here are exactly the 15 that b49-05 lists for TY2024.
- **Year-to-year switches:** DAFgiving360 reports zero employees in FY2021 (FYE 2021-06) and 165–194 from FY2022. T. Rowe Price reports 1 employee in FY2021–22 and 0 from FY2023.

**Sample and supplement, FY2024:** 17 `affiliate_staffed` and 11 `zero_employee_unexplained`. Most are small single-issue sponsors and CFs that pay a related entity or have no staff (CSV `affiliate_evidence`).

---

## 3. Results

### 3.1 Scale elasticities (sum of DAF-asset and DAF-account coefficients; clustered SE) [C]

| Sample | Spec | Elasticity | SE | Obs / sponsors | r² | Assets coef | Accounts coef |
|---|---|---|---|---|---|---|---|
| CF, own staff | M1 opex | **0.636** | 0.055 | 451 / 113 | 0.69 | 0.315 | 0.321 |
| CF, own staff | M2 opex, assets only | 0.504 | 0.041 | 451 / 113 | 0.68 | 0.504 | – |
| CF, own staff | M3 management & general | 0.711 | 0.062 | 451 / 113 | 0.75 | 0.431 | 0.280 |
| CF, own staff | M4 + ln total assets | 0.031 (DAF terms) | 0.083 | 451 / 113 | 0.80 | −0.183 | 0.214 (total assets **0.777**, SE 0.093) |
| CF, own staff | M6 employees | 0.519 | 0.058 | 451 / 113 | 0.65 | 0.219 | 0.300 |
| Single-issue, own staff | M1 opex | 0.070 | 0.156 | 163 / 45 | 0.27 | 0.839 | −0.769 [V wave 51A] |
| Single-issue, own staff | M4 + ln total assets | −0.464 (DAF terms) | 0.134 | 163 / 45 | 0.72 | – | – (total assets **1.143**) [V wave 51A] |
| National (non-affiliated), own staff | M1 opex | 0.360 | 0.135 | 29 / 8 | 0.45 | −0.264 | 0.624 |
| National (non-affiliated), own staff | M7 core opex | 0.336 | 0.091 | 29 / 8 | 0.67 | – | – |
| **Nationals ex processors, any staffing** | M1 opex | **0.489** | 0.081 | 98 / 25 | 0.52 | 0.359 | 0.129 |
| Nationals ex processors, any staffing | M2 assets only | 0.477 | 0.072 | 98 / 25 | 0.52 | 0.477 | – |
| Nationals ex processors, any staffing | M7 core opex | 0.487 | 0.082 | 98 / 25 | 0.60 | 0.399 | 0.088 |
| **Affiliated commercial, any staffing** | M1 opex | **1.014** | 0.076 | 44 / 11 | **0.92** | 0.503 | 0.510 |
| Affiliate/zero staff, nationals ex processors | M1 opex | 0.564 | 0.091 | 62 / 17 | 0.72 | 0.216 | 0.348 [V wave 51A] |
| Affiliate/zero staff, CFs and single-issue | M1 opex | 0.553 | 0.118 | 80 / 25 | 0.50 | 0.923 | −0.371 [V wave 51A] |
| All usable | M5 pooled, with dummies | 0.404 | 0.056 | 800 / 206 | 0.55 | 0.619 | −0.215 [V wave 51A] |
| All usable | M5 **affiliate/zero-staff dummy** | **−1.809** | 0.391 [V wave 51A] | | | | |
| *Robustness:* cost-structure universe FY2022–24, employees > 0 | R1, CF | 0.556 | 0.035 | 2,076 / 703 | 0.55 | 0.309 | 0.246 |
| *Robustness:* same | R1, National-Standard | 0.229 | 0.090 | 73 / 26 | 0.27 | 0.520 | −0.291 |
| *Robustness:* same | R1, single-issue | 0.014 | 0.053 | 1,131 / 401 | 0.11 | 0.466 | −0.452 |

**Reading**
- **[C] Every own-staff elasticity is below 1, with t < −4 against H0 = 1, except two:**
  - the affiliated-commercial group (1.01);
  - the 8-sponsor national M4 (0.66, SE 0.68).
- **[C] CF cost rises about 0.64% for each 1% of DAF scale, split evenly between assets and accounts.** Employees rise 0.52%.
- **[I] M4 changes the reading of that elasticity.** Once total assets are in the model, the DAF book adds almost nothing. A CF's cost follows the size of the foundation (its endowments, scholarships and programmes as well as its DAFs). The DAF elasticity in M1 is mostly a proxy for that.
- **[I] Affiliated nationals have no scale economies on their own 990.** Opex is close to proportional to scale (1.01, r² 0.92), because what the 990 records is mostly a fee to the parent priced on assets or accounts. Any scale economies sit at the parent.
- **[C] The pooled dummy of −1.81 means affiliate- and zero-staff sponsors report exp(−1.81) = 0.16 times the opex of an own-staff sponsor of the same type, assets and accounts.** [V wave 51A]
- **[C] Non-affiliated nationals with their own staff are few** (NPT, AEF, ImpactAssets and Servant Foundation; three smaller nationals, CAF America, Amalgamated and Philanthropic Ventures; and Charitable Gift America in FY2024). The estimate (0.36) is imprecise and sensitive to pass-through items. Core opex gives 0.34.

### 3.2 Levels by size band, FY2024 (medians; FY2024 corrected DAF assets band) [C]

| Cell | n | Whole-org bps | Rule-A bps | M&G bps | Opex / account | Rule-A / account | Avg account | Accounts / employee | DAF assets / employee | Employees | DAF share of total assets |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CF ≥ $1bn (own staff) | 10 | 154 | **80** | 92 | $21,285 | $13,588 | $1.35m | 9.7 | $15.9m | 124 | 63% |
| CF $100m–1bn | 27 | 323 | **118** | 145 | $21,242 | $8,004 | $683k | 7.9 | $6.6m | 58 | 47% |
| CF $10–100m | 53 | 633 | **149** | 259 | $19,754 | $4,358 | $328k | 10.6 | $2.6m | 9 | 28% |
| CF < $10m | 23 | 3,678 | **373** | 1,220 | $39,668 | $2,630 | $71k | 3.3 | $240k | 6 | 6% |
| CF top 50 (all staffing) | 21 | 162 | **102** | 100 | $20,245 | **$12,036** | $1.14m | 9.2 | $11.2m | 97 | 65% |
| CF non-top-50, < $50m | 77 | 893 | **186** | 331 | $21,477 | $3,870 | $204k | 6.8 | $1.5m | 6 | 22% |
| Single-issue, own staff | 42 | 972 | 352 | 340 | $25,203 | $5,608 | $221k | 7.4 | $1.6m | 19 | 24% |
| Nationals top 50, all staffing | 18 | **23** | 23 | 24 | **$1,395** | $1,357 | $376k | – | – | 0 | 99% |
| – own staff | 6 | 23 | 23 | 6 | $2,431 | $2,423 | $659k | **85** | $101.7m | 134 | 99% |
| – affiliate/zero staff | 12 | 23 | 23 | 30 | $1,100 | $814 | $317k | blank | blank | 0 | 99% |
| Affiliate/zero staff, CF and single-issue | 22 | 501 | 151 | 329 | $11,721 | $2,831 | $217k | blank | blank | 0 | 45% |

**Reading**
- **[C] Across CF bands, cost per account is flat ($20–40k whole-org) while cost per DAF dollar falls steeply with size.** That is the b45n33 identity (cost per account = cost ratio × average account) showing up across size bands. Larger CFs have larger accounts, not cheaper ones.
- **[C] Accounts per employee hardly move with size at CFs (about 8–11 from $10m upwards).** They are about 85 at own-staff top-50 nationals. A CF employee looks after about a tenth as many accounts as a national employee.
- **[C] Top-50 nationals cost the same per DAF dollar (23 bps) whatever their staffing model.** Per account, affiliate-staffed nationals report less ($1,100 vs $2,431) and their M&G is higher (30 vs 6 bps), because fees to the parent are booked mostly in column C.

### 3.3 Trend FY2021–24 [C]

**Balanced panel (sponsors usable in all four years); medians by FY**

| Group (n) | Metric | FY2021 | FY2022 | FY2023 | FY2024 | Median within-sponsor change 21→24 |
|---|---|---|---|---|---|---|
| **CF, own staff (112)** | Whole-org bps | 511 | 540 | 582 | 557 | **+21.3%** |
| | Rule-A bps | 123 | 151 | 161 | 154 | |
| | Pooled bps (Σ opex ÷ Σ DAF assets) | 162 | 204 | 222 | 202 | |
| | Opex per account | $17,255 | $17,499 | $19,145 | $21,390 | **+25.0%** |
| | Accounts per employee | 8.9 | 8.9 | 8.2 | 7.8 | |
| | DAF assets per employee | $2.76m | $2.53m | $2.78m | $2.88m | |
| | DAF grants $ per employee | $252k | $275k | $303k | $343k | |
| | Employees | 11 | 11.5 | 13.5 | 14.5 | **+14.0%** |
| | Opex / DAF assets / accounts | | | | | **+35.0% / +9.4% / +6.4%** |
| **Single-issue, own staff (40)** | Whole-org bps | 825 | 1,202 | 1,002 | 803 | +21.1% |
| | Opex / DAF assets / accounts / employees | | | | | +32.5% / +8.7% / +12.0% / +16.7% |
| **Affiliated nationals, affiliate-staffed (10; change n = 9)** | bps | 25.8 | 28.0 | 23.8 | 22.5 | **+0.5%** |
| | Per account | $723 | $761 | $853 | $790 | +7.7% |
| | Opex / DAF assets / accounts | | | | | +46.9% / +34.4% / +31.7% |
| **Own-staff affiliated nationals** (Vanguard; DAFgiving360 joins from FY2022) | bps | 16.3 | 20.2 | 20.8 | 17.5 | |
| | Accounts per employee | 227 | 395 | 371 | 405 | FY2021 is Vanguard alone |
| **Non-affiliated nationals, affiliate/zero staff (5)** | bps | 261 | 194 | 79 | 60 | −51.7% (Greater Horizons, Dechomai and GiveClear grew DAF assets while opex fell) |

FY medians use each year's staffing model. The 2021→24 change groups sponsors by their FY2024 staffing model.

**Reading**
- **[C] At CFs, costs grew nearly four times as fast as DAF assets.** The median CF's operating cost rose 35% while its DAF assets rose 9% and its accounts 6%. Headcount rose 14%, and accounts per employee slipped from 8.9 to 7.8. DAF grant dollars per employee rose 36% (from $252k to $343k), so grantmaking volume per head did rise.
- **[I] Part of the rise is nominal wage and price inflation, which this note does not deflate (P-B5104-04). The FY2021 denominator is also flattered**, because many CFs have a December year-end and their FY2021 balances were taken near the 2021 market peak. The bps figures peak in FY2023, not FY2024. Validator check on the same 112 CFs, with CPI-U annual averages 271.0 / 292.7 / 304.7 / 313.7 (2021–24; the BLS series as tabulated by the Minneapolis Fed, because bls.gov robots.txt returns 403 to a scripted client): median within-sponsor real opex +16.6%, real DAF assets −5.5%, employees +14.0%, real opex per employee −0.1%, real opex per account +8.0% (pooled +2.7%), opex per DAF grant dollar +0.7% (n = 103). Whole-org bps rose 21.3% from FY2021 but fell 4.0% from FY2022 and 2.8% from FY2023, while pooled DAF assets were $39.17bn, $33.53bn, $33.80bn and $39.77bn. So “efficiency fell” holds only as a modest real rise in cost per account; cost per employee and per grant dollar did not worsen. [V wave 51A]
- **[C] Affiliated nationals held cost per DAF dollar flat.** Their opex rose roughly in step with assets and accounts, which is consistent with asset-priced fees (§3.1).

### 3.4 Affiliate-staffed sponsors: why their efficiency must not be read off their own 990 [F/C/I]

**Top-50 affiliate/zero-staff nationals, FY2021 → FY2024 (opex bps of DAF assets; 11a + 11g share of opex)**

| Sponsor | Model | FY2021 bps | FY2024 bps | 11a+11g share FY2024 | Note |
|---|---|---|---|---|---|
| Fidelity Charitable | affiliate_staffed | 24.3 | 24.4 | 86% | 2.66m grants in CY2024; **$60.64 opex per grant** |
| GS DAPF | affiliate_staffed | 11.5 | 10.6 | 19% | |
| Morgan Stanley GIFT | affiliate_staffed | 30.6 | 20.3 | 87% | $151 per grant |
| Renaissance | affiliate_staffed | 36.3 | 32.9 | 99% | $122 per grant |
| Raymond James | affiliate_staffed | 32.2 | 33.2 | 92% | |
| Ayco | affiliate_staffed | 13.5 | 21.6 | 73% | |
| Bessemer | affiliate_staffed | 7.2 | 13.6 | 53% | |
| US Charitable Gift Trust | affiliate_staffed | 103.5 | 122.3 | 4% | Costs not booked as fees |
| T. Rowe Price | token (FY21) → affiliate | 27.3 | 22.5 | 12% | 1 employee in FY2021 = 3,782 accounts per reported employee |
| Bank of America CGF | affiliate_staffed | 0.12 | 0.15 | 0% | **Excluded** (opex < 1 bp); costs sit at the parent |
| The Signatry | affiliate_staffed | 0.63 | 52.8 | 0% | FY2021 excluded (< 1 bp) |
| Greater Horizons (GKCCF) | affiliate_staffed | 261.2 | 18.9 | 90% | |
| Dechomai | affiliate_staffed | 524.7 | 47.4 | 84% | |
| American Gift Fund | zero_employee_unexplained | 54.6 | 60.1 | 0% | No staff and no fees: who does the work is not shown (P-B5104-05) |

**Reading**
- **[I] There are three patterns.**
  - **Fee-for-service:** Fidelity, Morgan Stanley, Renaissance, Raymond James and Greater Horizons. 11a/11g carries the parent's price, so bps are meaningful as a price but not as a resource cost.
  - **Absorbed:** BofA and The Signatry in FY2021. The parent bears the cost, so the 990 understates cost to near zero.
  - **Mixed:** GS DAPF and US CGT. Costs sit in other lines.
- **[I] In none of the three can the 990 support "assets or accounts per employee".**
- **[C] Same scale, much lower reported cost.** Own-staff top-50 nationals and affiliate-staffed ones both sit at 23 bps (median FY2024). But the pooled model, which compares like with like in scale and type, puts affiliate/zero-staff opex at 0.16 times own-staff opex. That gap is the cost the 990 does not see.

### 3.5 Grants processed per employee, FY2024 (stated counts) [C]

| Sponsor | Staffing | Employees | Grants (period) | Grants per employee | Opex per grant | Accounts per employee |
|---|---|---|---|---|---|---|
| DAFgiving360 | own (costs partly at Schwab) | 194 | 1,100,000 (FY2024) | **5,670** | $69 | 578 |
| Jewish Communal Fund | own | 23 | 89,485 (FY2024) | 3,891 | $89 | 211 |
| Vanguard Charitable | own (affiliated) | 119 | 221,825 (FY2024) | 1,864 | $162 | 232 |
| American Endowment Foundation | own | 149 | 109,708 (CY2024, derived) | 736 | $209 | 107 |
| National Philanthropic Trust | own | 286 | 129,575 (FY2024) | 453 | $474 | 63 |
| ImpactAssets | own | 54 | 13,500 (CY2024) | 250 | $1,917 | 41 |
| Silicon Valley CF | own | 110 | 14,500 (CY2024) | 132 | $2,487 | 9 |
| Foundation For The Carolinas | own | 141 | 16,531 (CY2024) | 117 | $2,319 | 7 |
| Fidelity Charitable | affiliate | 0 | 2,664,446 (CY2024) | blank | $61 | blank |
| Renaissance | affiliate | 0 | 160,000 (CY2024) | blank | $122 | blank |
| Morgan Stanley GIFT | affiliate | 0 | 122,000 (CY2024) | blank | $151 | blank |
| GS DAPF | affiliate | 0 | 29,254 (CY2024) | blank | $457 | blank |

**Reading**
- **[C] Grants per employee range almost 50-fold**, from 117 at a large CF to 5,670 at DAFgiving360.
- **[I] The ordering follows grant size and service model** (high-touch, multi-fund CFs against self-service platforms). The DAFgiving360 figure is high partly because Schwab supplies brokerage and administration under its services agreement (b49-05 §3.4).
- **[C] CF opex per grant also covers non-DAF activity.**
- **[C] Calendar-year counts are matched to FY2024 returns that end on 30 June** where the source says so (see that file's `period_match`).

---

## 4. Comparison with existing repo work

### 4.1 Governance (b49-05) and compensation data [C]
- **Part I line 5 employees agree on every shared return:**
  - 392 of 392 b49-05 returns (same object id);
  - 183 of 183 compensation-direction returns.
- **Line 25 also agrees on all 183 compensation returns.**
- **Zero-employee sponsors:** 39 of the 41 that b49-05 lists for TY2024 are also zero in this note's FY2024. The 2 others (Charitable Gift America and Christian Community Foundation) have non-calendar years: their TY2024 return ends in 2025, which is this note's FY2025 and outside the window. Their FY2024 returns report 1 and 4 employees.
- **b49-05 sets employees beside governance answers;** this note sets them beside output.
  - The b49-05 medians (top 50: 70; sample: 6) sit in the same range as this note's FY2024 medians: 97 at top-50 CFs; 6–9 at CFs under $100m.
  - The affiliate-staffed top-50 group answers "No" to the Part VI 15a/15b compensation-process questions by construction (b49-05 §3.2). Here, that group has blank per-employee efficiency by construction.

### 4.2 CF cost and fee gap (direction-cf-consolidation-fees.md; b45n33) [C/I]
- **b45n33 (long-tail operating cost), same definitions:**
  - Its top-50 CF figures are rule A 102 bps and $12,036 per account (FY2024). This note gives **102 bps and $12,036**, from the same 21 CFs and identical opex: 165 of 165 shared returns match to $1.
  - Its top-50 national figures are 24 bps and $1,425; this note gives **23 bps and $1,357**. The difference is the account source: b45n33 used screened DAFRC accounts, this note Schedule D as filed.
  - Its tail-CF figure (under $50m, FY2024) is 205 bps under rule A. This note's sampled non-top-50 CFs under $50m give **186 bps** (n = 77). The direction and order agree; this sample is smaller and drawn differently.
- **Fees against cost by size [I]:**
  - The CF fee census gives median published admin fees of **100 / 100 / 67 bps** at $100k / $1m / $10m.
  - Rule-A DAF cost here is **80 bps at CFs of $1bn and over** (average account $1.35m), **118 bps at $100m–1bn** ($683k), **149 bps at $10–100m** ($328k) and **373 bps under $10m** ($71k).
  - So a 100 bps fee covers rule-A cost at the largest CFs, roughly covers it in the $100m–1bn band, and falls short below $100m. This matches the b45n33 finding that a 150 bps tail fee covers about 73% of tail cost.
  - The bands are medians, not matched pairs (P-B5104-03).
- **CF against national ratio:**
  - **Fees:** the census puts CF fees at 1.7× the nationals at $100k, 2.2× at $1m and about 3.5–4.5× at $10m.
  - **Costs:** rule-A cost at top-50 CFs is 4.4× top-50 nationals (102 vs 23 bps), and 3.4× for CFs of $1bn and over (80 vs 23 bps).
  - The cost gap is therefore at least as wide as the fee gap at mid-sized balances. CFs are not pricing above their cost relative to nationals [I]. This is weak: the 23 bps national figure is a Part IX floor (the M5 dummy puts affiliate- and zero-staff opex at 0.16 times own-staff opex at equal scale), and fees are by account balance while costs are by sponsor size. [V wave 51A]

### 4.3 Earlier scale elasticities (sponsor-cost-structure-and-sensitivities.md) [C]
- **Nationals:** the earlier note gives FY2024 opex on DAF assets of 0.41 (FY2022–23: 0.47–0.48) for DAFRC National-Standard sponsors. This note gives **0.48** (M2, nationals excluding processors, FY2021–24 pooled, clustered SE 0.07), within that range.
- **CFs:** the earlier note gives 0.84 for opex on total assets. This note's M4 total-assets coefficient is **0.78**, net of the DAF terms.
- **What is new here:**
  - the affiliated-commercial elasticity of 1.0;
  - the separate treatment of affiliate-staffed sponsors;
  - FY2021;
  - sponsor-clustered standard errors.

---

## 5. Limits
1. **Cross-sectional elasticities are not cost curves.**
   - With 4 years and FY dummies, the estimates are mostly between-sponsor.
   - Larger sponsors also differ in mission, account size and service model.
   - No sponsor fixed effects are used, because 4 years of a slow-moving scale variable give little within-sponsor variation (P-B5104-06).
2. **Whole-organisation cost.**
   - Part IX does not split DAF from non-DAF cost.
   - CF and single-issue whole-org ratios are ceilings, and rule A is an allocation [I].
   - Single-issue Part IX is mostly mission delivery.
3. **Affiliate-staffed sponsors.**
   - Their 990s show a price (fees) or nothing, not the parent's resource cost.
   - The classification depends on prior repo evidence (`SEGMENT`, compensation flags, b49-05 Part VI line 3) and on a Part IX fee pattern.
   - Sample sponsors outside b49-05 and the compensation work have only the Part IX test. Some `zero_employee_unexplained` sponsors may be affiliate-staffed.
4. **Employees are a headcount, not FTE.** Part I line 5 counts W-2 employees, including part-time staff, in the calendar year that ends with or within the tax year.
5. **Accounts.**
   - Schedule D account counts are as filed.
   - Processors' counts (AOGF, PayPal) fail the plausibility screen.
   - Network for Good files 1 account against $50–147m. It passes the $1k–$1bn screen, so its per-account figures are meaningless; processors are left out of every interpretation (n ≤ 3).
6. **Pass-through items.**
   - Servant Foundation ($219.9m advertising, FY2023) and CAF America ($97.7m professional fundraising fees, FY2021) carry large Part IX items that are not DAF administration.
   - Core opex (M7) handles them for the national regressions; medians handle them elsewhere.
7. **Nominal dollars; FY2021 is near a market peak.**
8. **Grant counts.** These exist for FY2024 only and for 12 sponsors. Some are calendar-year counts matched to June-FYE returns.
9. **Sample design.**
   - The b49-05 sample is a simple random sample and leans towards sponsors under $10m.
   - The supplement adds CFs of $10m and over.
   - Band medians are unweighted, with no confidence intervals. Band C has n = 53 and band A n = 10.

---

## 6. Source register and access log

### 6.1 Sources
| # | Source | URL | Use |
|---|---|---|---|
| S1 | IRS Form 990 e-file XML via the GivingTuesday 990 data lake mirror | `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml` (per-row `xml_url` in the CSV) | Part I, Part IX, Schedule D, Schedule I |
| S2 | IRS e-file index files `index_2021.csv`–`index_2026.csv` (local copies from earlier batches; not re-fetched) | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (pattern `{year}/index_{year}.csv`) | Locating returns |
| S3 | ProPublica Nonprofit Explorer filing pages (reference links only; not fetched) | `https://projects.propublica.org/nonprofits/organizations/{EIN}/{OBJECT_ID}/full` (per-row `source_url`) | Human-readable view of each return |
| S4 | DAFRC Annual DAF Report 2025 – Updated Analysis dataset (via repo CSV) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Population, type, fallback values |
| S5 | Grant counts (via repo `grant-count-denominators-2026-11-20.csv`), e.g. Fidelity Charitable 2025 Giving Report | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf ; https://www.nptrust.org/annual-reports/npt-annual-report/ ; other URLs per row in that file | Grants per employee |
| R1 | Repo: `sponsor-cost-structure.csv`, `scripts/mission_sponsor_cost_structure.py` | – | Extractor, opex definition, R1 universe |
| R2 | Repo: `b49-05-sponsor-governance-quality.md`, `sponsor-governance-quality-2026-11-20.csv`, `scripts/mission_sponsor_governance.py` | – | Sample, employees, Part VI line 3 |
| R3 | Repo: `direction-sponsor-executive-compensation.md`, `sponsor-executive-compensation-2021-2025.csv`, `scripts/mission_sponsor_compensation.py` | – | Top 50, `SEGMENT`, affiliate-pay flags |
| R4 | Repo: `b45n33-long-tail-operating-cost.md`, `long-tail-operating-cost-2026-11-19.csv` | – | Rule A; tail and top-50 comparison |
| R5 | Repo: `direction-cf-consolidation-fees.md` | – | CF published fee medians; CF against national fee ratios |
| R6 | Repo: `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `dafrc-corrections-itemized.csv` | – | Corrected FY2024 DAF assets |

### 6.2 robots.txt log (checked 2026-11-20, user agent `research-script/1.0`)
| Host | Result | Action |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404, no robots file, so no restrictions published | 94 FY2021 XMLs streamed |
| apps.irs.gov | 302 to an irs.gov 404 page, so no robots file | Not fetched in this task; index files reused from earlier batches |
| projects.propublica.org | 200. `User-agent: *` disallows `/nonprofits/search*`, `/download-xml*` and similar; there is no ClaudeBot or anthropic group, and `/nonprofits/organizations/` is not disallowed | Not fetched; URLs cited as references only |

sec.gov and the off-limits hosts in the shared rules were not used.

---

## 7. Data dictionary: `sponsor-operating-efficiency-2026-11-20.csv`

### 7.1 Every row
| Column | Meaning |
|---|---|
| `record_type` | `sponsor_year` (832), `regression` (194), `trend` (752), `band` (484), `comparison` (5) |

### 7.2 `sponsor_year` rows
| Column | Meaning |
|---|---|
| `ein`, `sponsor_name`, `group` | Identity; `group` = `top50`, `sample` (b49-05, seed 4905) or `supplement` (seed 5104) |
| `rank_fy2024`, `fy2024_daf_assets_corrected` | Rank and value on corrected FY2024 DAFRC DAF assets |
| `dafrc_type`, `dafrc_subtype` | DAFRC FY2024 classification |
| `sponsor_type` | `national_affiliated`, `national_other`, `processor`, `community_foundation` or `single_issue` (§1.1) [I] |
| `segment` | Compensation-direction segment, where one exists |
| `fy`, `tax_period`, `object_id`, `index_year` | FY = year the period ends; return identifiers |
| `extract_source`, `xml_status` | `cache` / `local_xml` / `gt_mirror`; `ok` |
| `staffing_model`, `affiliate_evidence` | §1.4 [I]; semicolon list of evidence labels |
| `employees` | Part I line 5 [F] |
| `total_functional_expenses`, `mgmt_general_l25c` | Part IX line 25 columns A and C [F] |
| `operating_cost_ex_invest_mgmt` | Opex: line 25 − lines 1–4 − 11f [C] |
| `operating_cost_incl_invest_mgmt`, `operating_cost_core` | Opex with 11f; opex − 12 − 11e [C] |
| `advertising_l12`, `fees_prof_fundraising_l11e`, `staff_cost_l5_10`, `fees_mgmt_l11a`, `fees_other_l11g`, `fees_invest_mgmt_l11f` | Part IX lines [F] |
| `total_assets_eoy` | Part X / Part I EOY total assets [F] |
| `sched_d_daf_accounts`, `sched_d_daf_assets_eoy`, `sched_d_daf_contributions`, `sched_d_daf_grants` | Schedule D Part I lines 1–4, as filed [F] |
| `daf_*_used` | Schedule D, with DAFRC fallback where Schedule D is blank or 0 (flags `daf_value_from_dafrc`, `accounts_from_dafrc`) |
| `dafrc_daf_assets_same_fy`, `dafrc_accounts_same_fy` | Corrected DAFRC values for the same FY |
| `daf_share_of_total_assets` | min(1, DAF assets ÷ total assets) [C] |
| `avg_account_usd` | DAF assets ÷ accounts (blank if the account count fails the screen) [C] |
| `opex_per_daf_account`, `opex_bps_daf_assets`, `tfe_bps_daf_assets`, `mg_per_daf_account`, `mg_bps_daf_assets` | Whole-organisation ratios [C] |
| `daf_opex_alloc_assets`, `daf_opex_alloc_per_account`, `daf_opex_alloc_bps_daf_assets` | Rule A (assets share) [I] |
| `fees_11a_11g_share_of_opex` | (11a + 11g) ÷ opex [C] |
| `daf_assets_per_employee`, `daf_accounts_per_employee`, `daf_grants_usd_per_employee`, `daf_contributions_per_employee`, `opex_per_employee` | Own-staff rows only [C] |
| `daf_accounts_per_reported_employee` | Accounts ÷ employees for any row with employees > 0, including token-staff rows. Shows the overstatement [C] |
| `grant_count_fy2024`, `grant_count_row`, `grant_count_period` | Primary stated grant count and its row id in `grant-count-denominators-2026-11-20.csv` (FY2024 rows only) |
| `grants_per_employee`, `opex_per_grant` | [C]; per employee only for own-staff rows |
| `sched_i_recipients`, `sched_i_recipients_per_employee` | Schedule I recipient counts; a lower bound on grants, not a grant count [C] |
| `usable` | 1 if included in medians and regressions (§1.5) |
| `quality_flags` | `account_count_implausible_or_missing`, `short_period_or_two_returns_in_fy`, `opex_nonpositive`, `opex_below_1bp_of_daf_assets`, `affiliated_commercial_costs_partly_at_parent`, `givinga_undefined_account_unit`, plus the cost-structure flags (`daf_value_gt_total_assets`, `daf_grants_gt_part_ix_grants`, `amended_return`, …) |
| `xml_url`, `source_url` | Mirror XML; ProPublica filing page |

### 7.3 `regression` rows
| Column | Meaning |
|---|---|
| `model` | M1–M7, R1 (§1.5) |
| `reg_sample` | `<staffing>:<type>` subset |
| `dependent` | Dependent variable (logged) |
| `term` | `const`, `ln_daf_assets_used`, `ln_daf_accounts_used`, `ln_total_assets_eoy`, `fy2022`…`fy2024`, dummies, or `scale_elasticity_sum_daf_terms` |
| `coef`, `se_cluster`, `t` | Coefficient, sponsor-clustered SE (CR1), t. For the sum row, t tests H0: sum = 1 |
| `n_obs`, `n_sponsors`, `r2` | Observations, clusters, R² |
| `note` | `too few observations` where a cell has < 5 sponsors |

### 7.4 `trend`, `band` and `comparison` rows
| Column | Meaning |
|---|---|
| `trend_panel` | Trend: `all_usable` or `balanced_fy2021_24`. Band: the cell label (§3.2) |
| `staffing_model`, `sponsor_type` | Trend cell: `own_staff` or `affiliate_or_zero_staff` × type |
| `fy` | 2021–2024, or `2021->2024` for within-sponsor change rows |
| `metric` | Metric name. `pooled_*` = Σ numerator ÷ Σ denominator; `median_log_change:<field>` = median of ln(FY2024 ÷ FY2021) within sponsor |
| `n_obs`, `p25`, `median`, `p75` | Count and quantiles (linear interpolation). For `comparison` rows, `n_obs` is the number compared and `median` the number that match |
| `note` | Comparison description |
