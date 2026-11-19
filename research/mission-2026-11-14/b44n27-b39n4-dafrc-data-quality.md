# DAFRC panel data quality: NPT FY2023 and the top-50 FY2024 imputed rows (P-B44N27-01, P-B39N4-02)

Task id b44n27-b39n4, 2026-11-19. Evidence tags: [F] filed or primary figure, [C] computed by script, [I] inference.

**Outputs**
- Script: [`scripts/mission_dafrc_r2_check.py`](../../scripts/mission_dafrc_r2_check.py).
- Proposed corrections: [`data/mission-2026-11-14/dafrc-corrections-r2-proposed-2026-11-19.csv`](../../data/mission-2026-11-14/dafrc-corrections-r2-proposed-2026-11-19.csv). It has 97 rows: 96 FY2024 rechecks and 1 NPT FY2023 sensitivity row.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b44n27-b39n4.csv`](../../data/mission-2026-11-14/queue-proposals-b44n27-b39n4.csv). It has 5 rows.
- The existing `dafrc-corrections-itemized.csv` was not edited.

## Summary

- **(A) NPT FY Jun-2023: the filed Schedule D value is internally inconsistent with the rest of the same return. The repo still keeps it as filed.**
  - **The filed figures** [F]. Schedule D Part I line 4 is **$22,843,599,245**. Part X net assets are **$27,919,223,352**. The gap is **$5.08bn**, which puts the DAF value at 81.8% of net assets.
  - **The neighbouring years** [C]:
    - In FY2022 and FY2024 the DAF value is 101.3% and 100.6% of net assets.
    - In all three years, Schedule D contributions equal Part VIII total contributions to the dollar, and Schedule D grants equal Part IX grants (to within $1).
    - Rolling the FY2022 DAF value forward by FY2023's net-asset change gives **$28.19bn**. Rolling FY2024 back gives **$28.16bn**.
  - **What does not explain the gap** [F]:
    - Non-DAF funds: column (b) of Part I is blank and every contribution is reported as DAF.
    - Affiliates: NPT Transatlantic is a disregarded entity with $163m of assets, and NPT UK is related but not controlled.
    - Timing: the June year end is the same in every year and no amended return exists.
  - **Recommendation.** Do not replace a filed value with an estimate in the headline series. Carry a flagged sensitivity instead: FY2023 market $261.44bn rather than $256.37bn, and FY2023→24 growth 23.6% rather than 26.1%. NPT's own consolidated statements for the year ended 2023-06-30 (https://www.nptrust.org/consolidated-statements-2023/, linked from the 2023 annual report page; PDF created 2024-05-15) report total assets of $28,876,243k and net assets of $28,514,324k. They agree with Part X and the roll-forwards, not with $22.84bn, so P-B44N27B39N4-01 is answered on first-party evidence. Whether to adopt the sensitivity in the headline series remains a repo policy decision [V wave 34A]
- **(B) Top-50 FY2024 imputed rows: nothing is left to replace.**
  - 24 sponsors in the union of the published and corrected top 50 have imputed FY2024 rows [C].
  - Each one has a filed FY2024 Form 990 in the IRS index. In 95 of the 96 sponsor-metric cells, the existing R1 correction already uses exactly the value in that return.
  - No newer or amended FY2024 return appears in the IRS `index_2026.csv` downloaded on 2026-11-19 [C].
  - ImpactAssets is already corrected to $2,896,880,396, a change of −$731,283,079 from object 202543169349307999.
  - The one cell R1 does not touch is UCLA Foundation's grants. The filed value is −$120.3m, so the imputed $169.9m is kept.
  - **No headline moves** [C]:
    - FY2024 market total: **$323.27bn**.
    - Corrected top-50 assets: **$276.27bn**, against $279.33bn as published.
    - League-table ranks: unchanged.
  - **Paper-submission rows (extra check).** All 13 top-50 "paper submission" rows, Fidelity included, match their FY2024 990 to the dollar (one exception below). Their 2023 `end_of_tax_period` is a stale label, not stale data.

## 1. Method

**Scope**
- The panel is `dafrc-sponsor-schedule-d-fy2019-2024.csv`, the DAFRC 2025 updated-analysis dataset with 1,512 FY2024 rows.
- The universe for (B) is the union of the FY2024 top 50 ranked two ways:
  - by published `eoy_daf_assets`;
  - by the repo-corrected value, which is DAFRC plus the applied rows in `dafrc-corrections-itemized.csv`.
- That union has 51 sponsors. Signatry enters the corrected top 50 at #35 (it is #75 as published), and Seattle Foundation leaves it (#42 → #52).
- A row is "imputed" when any of its four `source_*` provenance flags equals `Imputed`. Rows flagged `paper submission` were checked the same way as a cross-check.

**Return selection.** The rules are the same as R1 in `mission_dafrc_corrected_totals.py`:
- A row's fiscal year is the calendar year in which the tax period ends.
- The return used is the newest Form 990 for that period; a higher object id, such as an amended return, supersedes.
- The IRS TEOS indexes for 2019–2025 are the repo's 2026-11-14 downloads. `index_2026.csv` was downloaded again on 2026-11-19: it has 516,019 rows, against 472,357 in the 2026-11-15 copy.

**Extraction.** Each return's XML comes from the GivingTuesday mirror of IRS TEOS. The script parses:
- Schedule D Part I column (a): line 1 `DonorAdvisedFundsHeldCnt`, line 2 `…ContriAmt`, line 3 `…GrantsAmt`, line 4 `…VlEOYAmt`;
- Part IV line 6;
- the amended flag;
- for NPT, Part X (total assets, investments, cash, net assets BOY/EOY), Part VIII/IX totals, the Part XI reconciliation, Schedule R and Schedule O.

**Screens.** The R1 suspect screen is reused: a negative amount, or a zero year-end value beside a positive account count, means the cell is kept as published.

**Proposal file.**
- `applied = 1` only where the round-2 value differs from the value the repo already uses.
- `delta` follows the itemized file's convention: corrected value minus DAFRC's published value.

**Totals**
- The market after round 2 is the repo's corrected FY2024 total plus the sum of round-2 changes.
- The top 50 is re-ranked on the corrected values.
- The FY2023 sensitivity swaps the NPT value into the repo's FY2023 corrected total and recomputes growth, payout, NPT share, CR1/3/5 and HHI over the FY2023 sponsor list.

**Run**
```
python3 -I scripts/mission_dafrc_r2_check.py . --irs-dir <scratch>/irs --irs-dir <scratch>/q2704/irs \
    --xml-dir <scratch>/q2704/xml --fetch --out-json <scratch>/q2704/summary.json
```
The script is stdlib-only and functional. It prints a markdown table (§3.1) and the totals line.

**Robots log, 2026-11-19, user agent `research-script/1.0`**

| Host | robots.txt result | Use |
|---|---|---|
| apps.irs.gov | 302 to www.irs.gov/404, so there is no robots file | TEOS index CSV |
| www.irs.gov | 200; disallows only /core/, /admin/, search paths and similar; nothing under /pub/ | – |
| gt990datalake-rawdata.s3.amazonaws.com | 404 NoSuchKey, so there is no robots file | 41 XML returns |
| www.nptrust.org | 200; `User-agent: *` / `Disallow:` (empty), so everything is allowed | annual-report pages and sitemap |

## 2. (A) NPT FY Jun-2023: is the Schedule D value understated?

### 2.1 Filed figures, FY2022–FY2024 [F]

All values are from Form 990 for EIN 237825575. There is one 990 per period and no amended return; the only other filings in those periods are 990-Ts.

| Line | FY Jun-2022 (202311359349313966) | FY Jun-2023 (202431429349301368) | FY Jun-2024 (202511339349301311) |
|---|---|---|---|
| Sch D I-1 DAFs held | 14,372 | 15,407 | 17,940 |
| Sch D I-2 contributions | 13,187,326,338 | 9,212,356,693 | 14,523,915,937 |
| Sch D I-3 grants | 5,554,630,445 | 4,446,854,186 | 5,563,257,811 |
| **Sch D I-4 DAF value EOY** | **21,522,060,225** | **22,843,599,245** | **42,119,335,128** |
| Sch D I column (b) (other funds) | blank | blank | blank |
| Part VIII total contributions | 13,187,326,338 | 9,212,356,693 | 14,523,915,937 |
| Part IX grants (line 1–3 total) | 5,554,630,445 | 4,446,854,186 | 5,563,257,810 |
| Part X investments, publicly traded | 13,586,842,779 | 18,150,235,321 | 31,380,733,953 |
| Part X investments, other securities | 4,037,782,498 | 4,553,523,398 | 4,946,629,914 |
| Part X savings and temporary cash | 3,979,945,814 | 5,478,323,545 | 5,780,641,385 |
| Part X total assets EOY | 21,633,283,286 | 28,241,290,750 | 42,227,968,504 |
| **Part X net assets EOY** (all without donor restriction) | **21,249,469,104** | **27,919,223,352** | **41,882,463,155** |
| Part X net assets BOY | 15,654,008,855 | 21,249,469,104 | 27,919,223,352 |
| Part XI revenue less expenses | 8,745,623,035 | 5,498,669,312 | 10,176,755,999 |
| Part XI unrealized gains | −3,144,455,976 | 1,168,398,323 | 3,815,112,334 |
| Return submitted | 2023-05-15 | 2024-05-21 | 2025-05-13 |

### 2.2 Consistency tests [C]

| Test | FY2022 | FY2023 | FY2024 |
|---|---|---|---|
| DAF value ÷ net assets | 101.3% | **81.8%** | 100.6% |
| DAF value − net assets | +$0.273bn | **−$5.076bn** | +$0.237bn |
| Sch D contributions = Part VIII contributions | yes | yes | yes |
| Sch D grants − Part IX grants | $0 | $0 | $1 |

Implied FY2023 DAF value:
- FY2022 DAF value plus FY2023's change in net assets (+$6.670bn) gives **$28.19bn**.
- FY2024 DAF value minus FY2024's change in net assets (+$13.963bn) gives **$28.16bn**.
- Contributions less grants only, with no investment return, gives $26.29bn. This matches the queue item's $26.29bn.

Return needed in FY2024, measured as (EOY − (contributions − grants) − BOY) ÷ BOY [V wave 34A]
- **45.2%** on the filed $22.84bn;
- **18.8%** on Part X net assets.

The FY2024 return records $1.35bn of investment income and $3.82bn of unrealized gains, which fits the second figure.

No other amount between $20bn and $30bn in the FY2023 XML equals $22,843,599,245 [C]:
- Part X lines and BOY/EOY totals do not.
- The Schedule A public-support total ($23.65bn) does not.
- Publicly traded plus other securities ($22.70bn) does not.

So the figure cannot be traced to a mis-keyed neighbouring line. One near match is worth recording [I]: total assets less savings and temporary cash ($28,241,290,750 − $5,478,323,545 = $22,762,967,205) is within $80.6m (0.35%) of the filed $22,843,599,245, and the $5.08bn gap is 93% of that cash line. A line 4 that left out cash and temporary investments in FY2023 only would fit. In FY2022 and FY2024, total assets less cash is far below line 4, so cash was included in those years. This is not proven [V wave 34A]

### 2.3 Can the filing explain the gap? [F]

**Non-DAF funds: no.**
- Schedule D Part I column (b), "funds and other accounts", is blank in all three years.
- Schedule D contributions and grants equal the whole organisation's Part VIII and Part IX figures.
- So NPT reports all of its activity as DAF activity.
- Schedule O describes NPT as offering "donor-advised funds (DAFs), designated funds, supporting organizations and specialized field of interest funds". However:
  - the supporting organisations (Saint Agatha Foundation, NPT Charitable Asset Trust, NPT Donor Fund B and others) are separate 509(a)(3) filers listed in Schedule R Part II, and are not in NPT's Part X;
  - non-DAF funds inside NPT would have to total $5.1bn in FY2023 only, and be about −$0.24bn to −$0.27bn in the adjacent years.

**UK and international affiliates: no.**
- NPT Transatlantic Limited (London; EIN 981125584) is a **disregarded entity** in Schedule R Part I, so its assets are already inside NPT's Part X. Its year-end assets were $130.5m in FY2022, $163.1m in FY2023 and $245.3m in FY2024.
- National Philanthropic Trust UK Limited is listed as related but `ControlledOrganizationInd = 0`, with no financial data. It is not in Part X.
- Both are at least an order of magnitude smaller than the $5.08bn gap.

**Timing: no.**
- All three returns cover July–June years.
- FY2024's Part X BOY net assets equal FY2023's EOY net assets exactly. The FY2024 Schedule D value of $42.12bn is consistent with a starting DAF value of about $28.2bn, not $22.8bn.
- There is no amended FY2023 990 in any index through the 2026-11-19 `index_2026.csv`.

**Reporting basis.** The return ticks "consolidated" audited statements (`ConsolidatedAuditFinclStmtInd = 1`). The 990, however, is the US entity plus its disregarded entities, and that is the same basis every year.

**Conclusion** [I]. The FY2023 Schedule D line 4 is very likely a filer error, understated by about $5.1–5.3bn. The filing alone cannot prove which line is wrong.

Public NPT material does not settle it:
- NPT's [2023 annual report page](https://www.nptrust.org/annual-reports/the-2023-annual-report/) gives grants (
- No FY2023 financial statements are listed in the nptrust.org sitemap (528 URLs checked). However, the 2023 annual report page links a two-page 

### 2.4 Decision and effect

**Repo figures should not change in the headline series.**
- The R1–R4 correction rules replace only imputed values with filed ones. Replacing a filed figure with an estimate would be a new kind of correction.
- The CSV therefore carries one row, `SENS_filed_inconsistent_with_part_x`, with `applied = 0`. Its corrected value is the filed Part X net assets of $27,919,223,352, a lower bound because NPT's DAF value ran 0.6–1.3% above net assets in the other years.
- NPT's consolidated FY2023 statements (net assets $28,514,324k) support it. Adopting it in the headline series is a policy decision. Because the consolidated basis covers NPT and its affiliates, Part X ($27,919,223,352) stays the conservative value (P-B44N27B39N4-01) [V wave 34A]

What would move if the sensitivity were adopted [C]. The repo values match `direction-league-table-concentration.md`, whose FY2023 row is $256.37bn, CR1 21.7%, CR3 42.9%, CR5 52.9% and HHI 801.

| FY2023 metric | Repo now | NPT = Part X net assets | NPT = roll-forward $28.19bn |
|---|---|---|---|
| Corrected market DAF assets | $256.37bn | $261.44bn | $261.72bn |
| FY2022→23 growth | 12.4% | 14.6% | 14.7% |
| FY2023→24 growth (to $323.27bn) | 26.1% | 23.6% | 23.5% |
| FY2024 payout (grants ÷ prior-year assets) | 25.9% | 25.4% | 25.4% |
| NPT share / rank | 8.9% / #3 | 10.7% / #3 | 10.8% / #3 |
| CR1 / CR3 / CR5 | 21.7% / 42.9% / 52.9% | 21.3% / 44.0% / 53.8% | 21.2% / 44.1% / 53.9% |
| HHI | 801 | 808 | 808 |

FY2024 figures are not affected.

## 3. (B) Top-50 FY2024 imputed rows

### 3.1 Every top-50 sponsor whose FY2024 row is imputed [C]

There are 24 sponsors. In all of them all four metrics are imputed.
- "#" is the rank on repo-corrected FY2024 assets.
- Dollar amounts are in $m and come from the filed FY2024 Form 990 Schedule D Part I.
- "DAFRC imputed" is the published value.

| # | Sponsor | Object id | Period | Submitted | I-1 DAFs | I-2 contrib. | I-3 grants | I-4 EOY value | DAFRC imputed EOY | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | GS Donor Advised Philanthropy Fund | 202503109349303645 | 202412 | 2025-11-06 | 4,134 | 5,833.8 | 3,071.8 | 12,640.9 | 11,843.0 | R1 confirmed |
| 7 | Morgan Stanley Global Impact Funding Trust | 202503239349300435 | 202412 | 2025-11-19 | 21,800 | 2,959.4 | 1,649.1 | 9,109.1 | 9,429.5 | R1 confirmed |
| 8 | American Endowment Foundation | 202513219349310376 | 202412 | 2025-11-17 | 15,947 | 1,690.2 | 1,305.3 | 8,378.0 | 9,480.2 | R1 confirmed |
| 9 | Renaissance Charitable Foundation | 202543189349301959 | 202412 | 2025-11-14 | 25,824 | 2,159.9 | 770.8 | 5,913.6 | 5,634.0 | R1 confirmed |
| 10 | National Christian Charitable Fdn | 202513109349303201 | 202412 | 2025-11-06 | 31,943 | 2,907.6 | 2,433.0 | 5,683.7 | 5,459.7 | R1 confirmed |
| 11 | Bank of America Charitable Gift Fund | 202503219349318170 | 202412 | 2025-11-17 | 17,840 | 1,489.7 | 965.6 | 4,733.9 | 5,108.7 | R1 confirmed |
| 13 | ImpactAssets | 202543169349307999 | 202412 | 2025-11-12 | 2,197 | 611.9 | 432.5 | 2,896.9 | 3,628.2 | R1 confirmed |
| 15 | Foundation For The Carolinas | 202543219349306689 | 202412 | 2025-11-17 | 1,047 | 390.8 | 721.8 | 2,617.7 | 2,948.1 | R1 confirmed |
| 20 | Dechomai Asset Trust | 202523159349304782 | 202412 | 2025-11-11 | 314 | 674.6 | 552.3 | 1,432.2 | 2,219.1 | R1 confirmed |
| 22 | Columbus Foundation | 202513189349305651 | 202412 | 2025-11-14 | 1,533 | 147.8 | 171.9 | 1,232.3 | 1,326.8 | R1 confirmed |
| 23 | DonorsTrust | 202513179349312256 | 202412 | 2025-11-13 | 579 | 285.5 | 283.5 | 1,211.8 | 1,176.5 | R1 confirmed |
| 24 | US Charitable Gift Trust | 202533189349305673 | 202412 | 2025-11-14 | 10,740 | 314.1 | 258.4 | 1,188.6 | 1,364.1 | R1 confirmed |
| 25 | Ayco Charitable Foundation | 202543109349303959 | 202412 | 2025-11-06 | 5,585 | 317.7 | 300.9 | 1,158.0 | 1,382.8 | R1 confirmed |
| 26 | Oregon Community Foundation | 202503189349314430 | 202412 | 2025-11-14 | 1,394 | 108.3 | 94.3 | 1,106.4 | 1,192.9 | R1 confirmed |
| 29 | CF for Greater Atlanta | 202523219349322912 | 202412 | 2025-11-17 | 744 | 244.2 | 140.4 | 1,025.4 | 1,062.2 | R1 confirmed |
| 31 | Jewish Community Federation of SF | 202531349349310023 | 202406 | 2025-05-14 | 1,008 | 82.0 | 101.3 | 972.5 | 995.2 | R1 confirmed |
| 32 | Bessemer Giving Fund | 202513179349306881 | 202412 | 2025-11-13 | 861 | 254.7 | 141.2 | 931.4 | 961.8 | R1 confirmed |
| 35 | Signatry Charitable Trust | 202543189349315279 | 202412 | 2025-11-14 | 2,564 | 997.9 | 559.5 | 796.8 | 403.7 | R1 confirmed |
| 36 | CF of New Jersey | 202543189349311964 | 202412 | 2025-11-14 | 626 | 124.1 | 99.1 | 738.2 | 819.8 | R1 confirmed |
| 38 | Jewish Community Fdn of Los Angeles | 202533199349302138 | 202412 | 2025-11-15 | 1,192 | 134.8 | 145.6 | 709.7 | 728.9 | R1 confirmed |
| 40 | Tulsa Community Foundation | 202533219349318548 | 202412 | 2025-11-17 | 803 | 159.0 | 92.2 | 701.0 | 693.6 | R1 confirmed |
| 43 | American Gift Fund | 202523219349320222 | 202412 | 2025-11-17 | 1,661 | 123.8 | 107.5 | 642.6 | 747.8 | R1 confirmed |
| 44 | UCLA Foundation | 202521349349311822 | 202406 | 2025-05-14 | 10 | 90.1 | **−120.3** | 607.8 | 605.7 | R1 confirmed; grants kept imputed |
| 52 | Seattle Foundation (published #42) | 202503189349315665 | 202412 | 2025-11-14 | 557 | 97.8 | 155.4 | 573.8 | 687.7 | R1 confirmed |

Notes on the table:
- "CF for Greater Atlanta" is the panel's "THE COMMUNITY FOUNDATION FOR GREATER", EIN 581344646.
- "R1 confirmed" means the existing itemized R1 row uses the same object id and the same value, for all four lines.
- None of the 24 has a second FY2024 Form 990, 990-EZ or 990-PF in the indexes (the `other_return_type_same_fy` column is empty).

### 3.2 Proposed corrections [C]

- **0 new or changed values.** The proposed CSV has 96 FY2024 rows (24 sponsors × 4 metrics), all `applied = 0`:
  - 95 are `R1 confirmed`;
  - 1 is UCLA grants, a negative filed value that the R1 suspect screen keeps as imputed (P-B44N27B39N4-03).
- **ImpactAssets.** The task's example, $3.628bn imputed against the filed CY2024 value, is already handled. `dafrc-corrections-itemized.csv` applies R1 using object 202543169349307999, for a change of −$731,283,079. The validation-wave-24A report had already noted this.
- **Against DAFRC as published**, the 24 sponsors' R1 replacements add up to **−$2.898bn** of FY2024 year-end assets. That change is already inside the repo's $323.27bn.

### 3.3 Cross-check: top-50 "paper submission" rows [C]

There are 18 FY2024 rows panel-wide whose provenance resolves to paper submission (a paper flag on at least one metric and no `Imputed` flag), holding $90.43bn. 21 rows carry a paper flag on at least one metric [V wave 34A]. 15 of them carry an `end_of_tax_period` that ends in 2023. The original queue wording flagged Fidelity's 2023-06-30 period on this basis.

All 13 such rows in the top 50 were matched to their FY2024 Form 990:

| # | Sponsor | DAFRC period label | Filed period | Object id | EOY $bn | Match on lines 1–4 |
|---|---|---|---|---|---|---|
| 1 | Fidelity Investments Charitable Gift Fund | 2023-06-30 | 202406 | 202521349349310887 | 66.200 | all four equal |
| 6 | Silicon Valley CF | 2023-12-31 | 202412 | 202543149349305759 | 9.578 | all four equal |
| 16 | Greater Kansas City CF | 2023-12-31 | 202412 | 202533189349314033 | 2.574 | all four equal |
| 17 | Greater Horizons | 2023-12-31 | 202412 | 202513189349309621 | 2.531 | all four equal |
| 18 | Combined Jewish Philanthropies | 2023-06-30 | 202406 | 202541259349302634 | 1.930 | all four equal |
| 21 | New York Community Trust | 2023-12-31 | 202412 | 202523149349305672 | 1.255 | all four equal |
| 27 | Boston Foundation | 2023-06-30 | 202406 | 202531329349304083 | 1.097 | all four equal |
| 28 | California Community Foundation | 2023-06-30 | 202406 | 202531359349303988 | 1.091 | all four equal |
| 33 | Greater Houston CF | 2023-12-31 | 202412 | 202543219349315304 | 0.922 | filed grants +$17,400, assets +$1 |
| 34 | Marin CF | 2023-06-30 | 202406 | 202541349349313719 | 0.875 | all four equal |
| 39 | San Diego Foundation | 2023-06-30 | 202406 | 202541209349303454 | 0.708 | all four equal |
| 48 | San Francisco Foundation | 2023-06-30 | 202406 | 202541339349302554 | 0.591 | all four equal |
| 49 | CF of Tampa Bay | 2023-06-30 | 202406 | 202541329349303559 | 0.590 | all four equal |

The values are FY2024 data; only DAFRC's period label is stale [I]. No value change is proposed. The Greater Houston difference is immaterial and is not proposed.

### 3.4 Totals and headline figures [C]

| Figure | Before round 2 | After round 2 |
|---|---|---|
| FY2024 market DAF assets (corrected) | $323,269,551,062 | $323,269,551,062 (Δ $0) |
| FY2024 top-50 assets (corrected, re-ranked) | $276,266,253,487 | $276,266,253,487 |
| FY2024 top-50 assets as published by DAFRC | $279,334,361,954 | – |
| FY2024 market as published | $327,870,852,179 | – |
| Top-50 membership and ranks | – | unchanged (no rank moves) |

**Headlines that would move: none for FY2024.**
- The $323.27bn total stands.
- The corrected league table stands, including Signatry at #35 and Seattle at #52.
- CR and HHI for FY2024 stand.

The only candidate movement is the FY2023 NPT sensitivity in §2.4, which is not applied.

## 4. Limits

- **NPT's FY2023 consolidated statements were found by the validator** at https://www.nptrust.org/consolidated-statements-2023/, linked from the 2023 annual report page but absent from the sitemap. They show net assets of $28,514,324k at 2023-06-30, in line with Part X and the roll-forwards, so the error is in Schedule D line 4, not Part X. The two-page PDF carries no auditor's opinion, and it reports no DAF-only figure [V wave 34A]
- **Schedule D Part I is self-reported**, and R1 trusts it. The UCLA grants cell shows that filed values can be wrong.
- **Universe.** Only the top 50 (union of 51 sponsors) was rechecked. The 57 unresolved FY2024 imputed rows ($1.10bn, mostly long tail) were not re-run against the newer index (P-B44N27B39N4-05).
- **Index coverage.** Returns filed after the 2026-11-19 `index_2026.csv` snapshot are not covered.
- **Rank definition.** "Top 50" is by year-end DAF assets only.

## 5. Data dictionary: `dafrc-corrections-r2-proposed-2026-11-19.csv`

The columns are the same as `dafrc-corrections-itemized.csv`; the round-2 meaning of each is noted.

| Column | Meaning |
|---|---|
| fiscal_year | DAFRC fiscal year: the calendar year the tax period ends. 2024 for rechecks; 2023 for the NPT sensitivity row |
| ein, name, type | DAFRC identifiers (EIN zero-padded to 9) |
| metric | daf_accounts_eoy (Sch D I-1), daf_contributions (I-2), daf_grants (I-3), daf_assets_eoy (I-4) |
| dafrc_row | "present": the sponsor has a DAFRC row |
| dafrc_operating_status | DAFRC `operating_status` |
| dafrc_source | DAFRC provenance flag for that metric (`Imputed`; `IRS 990` for the NPT row) |
| dafrc_value | DAFRC published value |
| filed_value | Value in the selected Form 990 XML (blank if not reported) |
| corrected_value | Round-2 value: the filed value where usable, else the value the repo already uses. For the SENS row, Part X net assets |
| delta | corrected_value − dafrc_value (same convention as the itemized file) |
| applied | 1 = round 2 changes the value the repo currently uses; 0 = confirms the existing value, or sensitivity only |
| rule | R1_filed_replaces_imputed where a usable filed value exists for an imputed metric; SENS_filed_inconsistent_with_part_x for the NPT sensitivity; blank if the filed value is unusable |
| evidence_class | 990_part_i_reported / 990_part_i_blank / no_990_in_index |
| part_iv_line6 | Form 990 Part IV line 6 (DonorAdvisedFundInd) as filed |
| return_object_id, tax_period, return_ts | Selected return (newest for the period; amended supersedes), its YYYYMM period and its submission date |
| submitted_before_2026 | 1 if return_ts is before 2026-01-01 |
| amended_ind | AmendedReturnInd as filed |
| other_return_type_same_fy | Other 990/990-EZ/990-PF filings for the same FY (type:period:object id); empty for all rows |
| note | Line reference, recheck status, the repo value before round 2 and the itemized R1 object id; for the SENS row, the ratios and roll-forwards |
| source_urls | DAFRC dataset; IRS index file; XML URL(s) |

The queue-proposals CSV uses the header and format of `queue-proposals-gap19-13.csv`.

## 6. Source register

| ID | Source | URL | Accessed | Used in |
|---|---|---|---|---|
| S1 | DAFRC Annual DAF Report 2025, updated-analysis dataset (repo copy: `dafrc-sponsor-schedule-d-fy2019-2024.csv`) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | repo | §1, §3 |
| S2 | IRS TEOS e-file index 2024 (NPT FY2023 return) | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv | 2026-11-14 (repo copy) | §2 |
| S3 | IRS TEOS e-file index 2025 (FY2024 returns) | https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv | 2026-11-14 (repo copy) | §3 |
| S4 | IRS TEOS e-file index 2026 (fresh download) | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | 2026-11-19 | §1, §3 |
| S5 | NPT Form 990 FY Jun-2022 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202311359349313966_public.xml | 2026-11-19 | §2 |
| S6 | NPT Form 990 FY Jun-2023 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202431429349301368_public.xml | 2026-11-19 | §2 |
| S7 | NPT Form 990 FY Jun-2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml | 2026-11-19 | §2 |
| S8 | FY2024 Form 990 XML for the 24 imputed sponsors (object ids in §3.1) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml | 2026-11-19 | §3.1 |
| S9 | FY2024 Form 990 XML for the 13 paper-submission sponsors (object ids in §3.3); Fidelity example: | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml | 2026-11-19 | §3.3 |
| S10 | NPT 2023 annual report page (FY23 grants $4.52bn; no asset figure) | https://www.nptrust.org/annual-reports/the-2023-annual-report/ | 2026-11-19 | §2.3 |
| S11 | NPT 2024 annual report page (FY24 grants $5.62bn; no asset figure) | https://www.nptrust.org/annual-reports/the-2024-annual-report/ | 2026-11-19 | §2.3 |
| S12 | NPT sitemap index (528 URLs; no FY2023 financial statements) | https://www.nptrust.org/sitemap_index.xml | 2026-11-19 | §2.3, §4 |
| S13 | Repo: R1–R4 method and outputs | `scripts/mission_dafrc_corrected_totals.py`; `data/mission-2026-11-14/dafrc-corrections-itemized.csv`; `dafrc-corrected-market-totals.csv` | repo | §1, §3.4 |
| S14 | Repo: FY2023 concentration row checked against | `research/mission-2026-11-14/direction-league-table-concentration.md` (FY2023 $256.37bn, CR5 52.9%, HHI 801) | repo | §2.4 |
