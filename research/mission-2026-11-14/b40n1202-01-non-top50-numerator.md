# Non-top-50 DAF sponsors in the recipient-share numerator: measured, not inferred (P-B40N1202-01)

**Date:** 2026-11-19 · **Task ID:** b40n1202-01 · **Queue item:** P-B40N1202-01 (from [queue-proposals-b40n12-02.csv](../../data/mission-2026-11-14/queue-proposals-b40n12-02.csv)) · **Builds on:** [b40n12-daf-share-of-recipient-revenue.md](b40n12-daf-share-of-recipient-revenue.md) and its wave 33A corrections ([validation-wave33a-report.md](validation-wave33a-report.md)); [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md) and its wave 34B corrections ([validation-wave34b-report.md](validation-wave34b-report.md))

**Outputs**
- Script: [`scripts/mission_non_top50_numerator.py`](../../scripts/mission_non_top50_numerator.py). It is new. It imports `mission_daf_share_recipient_revenue.py` and `mission_recipient_basis_eligibility.py` and modifies neither.
- Data: [`data/mission-2026-11-14/non-top50-numerator-2026-11-19.csv`](../../data/mission-2026-11-14/non-top50-numerator-2026-11-19.csv). It has 3,851 rows: 190 summary, 9 disposition, 28 coverage and 3,624 recipient rows. The data dictionary is in §6.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b40n1202-01.csv`](../../data/mission-2026-11-14/queue-proposals-b40n1202-01.csv)

Tags: [F] computed from filings by the script · [P] quoted primary source · [I] inference.

## 0. Answer in brief

- **Scope: the full panel, with no sponsor sampling.** Every DAFRC 2025 panel sponsor whose FY2023 or FY2024 return itemises Schedule I was read. That is 1,331 sponsors beyond the top 50, in 2,611 sponsor-years with 487,896 lines, all re-read from the GivingTuesday mirror with the top-50 parser. Together with the top 50's 94 sponsor-years, this covers **84.9%** of netted FY2024 DAF grants (DAF-weighted, net of DAF-to-DAF), against 67.3% for the top 50 alone [F]. The non-top-50 sponsors add 17.6 points. The 32.7 points the scaling filled cover everything outside top-50 itemised lines, including the 15.1-point gap that no itemised line reaches, so they are not a like-for-like target for these sponsors [V wave 40B]
- **The scaled estimate leaned high, but most of the fall below is not a measured overstatement [F/I].** On the line 1h basis, the committed 1/0.673 inference gives a pooled share of **10.3%** (implied interval 9.0–11.6%). Like for like (committed frame, both sides divided by their coverage) the measured figure is 9.9%, a fall of 0.4 point (14.8% against 15.4% on 1h − 1d − 1e, 0.6 point). Leaving the 15.1% unitemised gap unassigned takes 1h to 8.4% (−1.5 points), so the direct figures are floors. Allocating the gap by component (foreign grants and the DAF-to-DAF residual to no recipient) gives 9.2% on 1h and 13.7% on 1h − 1d − 1e. The assumption envelope is about 8.8–9.4% and 13.2–14.1% (b40n120201-01) [V wave 41B] Adding the new-only recipients changes the population and takes it to 7.3% (−1.0 point). The direct shares on each frame: [V wave 40B]

  | Frame | Pooled share | 95% CI | Change from 10.3% |
  |---|---|---|---|
  | Expanded: the committed frame plus 70,008 recipients that get only non-top-50 grants | **7.3%** | 6.5–8.2% | −2.9 points (−28%) |
  | Committed frame | 8.4% | 7.6–9.2% | −1.9 points |

- **On the headline private basis (1h − 1d − 1e), from b40n1202-b43n26 [F].** The scaled 15.4% becomes **12.1%** (10.9–13.4%) on the expanded frame and 12.6% (11.3–14.0%) on the committed frame. That is −3.3 points.
- **Why the scaling overshot [F].** Among committed-frame recipients, non-top-50 grants add **21.4%** to the top-50 numerator (weighted, matched years). The 1/0.673 scaling assumed **48.6%**. Of that, 26.2 points (0.176 ÷ 0.673) is the non-top-50 sponsors’ own measured coverage and 22.4 points is the unitemised gap. Like for like, the measured 21.4% is 0.82 of the 26.2% that proportional allocation would give [V wave 40B]
  - Only 58.9% of non-top-50 DAF-weighted dollars reach committed-frame recipients. A further 13.7% reaches recipients that no top-50 sponsor itemises, and 27.4% goes to excluded types, not-in-BMF EINs or blank-EIN lines. Blank-EIN lines are 5.9% of non-top-50 dollars, against 0.5% for the top 50.
  - The scaling also credited to recipients the 15.1% of netted grants that no itemised line reaches: foreign grants, sub-$5,000 gifts, non-itemising sponsors and the DAF-weighting haircut.
- **Residual scaling [I].** Dividing the direct figures by the all-panel coverage (0.849) gives 8.7% on 1h and 14.2% on 1h − 1d − 1e. These still lean high, for the same reasons wave 33A gave (V33A-09).
- **The median rises [F].** Non-top-50 money is spread across many small recipients. The all-sponsor median is 9.3% (8.0–10.7%) on the committed frame and **6.8%** (6.2–8.0%) on the expanded frame, against 5.9% for the top 50 alone. On 1h − 1d − 1e it is 11.4% and 8.9%, against 7.7%.
- **The size gradient holds, and the inference overstated large recipients [F].** Expanded-frame pooled shares on 1h, all sponsors, by band:

  | Band | Direct, all sponsors | Old scaled inference |
  |---|---|---|
  | <$1m | 17.9% | 26.4% |
  | $1–5m | 10.8% | 14.2% |
  | $5–25m | 9.2% | 13.0% |
  | $25–100m | 6.5% | 9.3% |
  | ≥$100m | 3.7% | 5.5% |

  On 1h − 1d − 1e, ≥$100m is 6.8% (5.4–8.9%) and $25–100m is 12.3% (11.1–13.8%).
- **Against Chariot's 12.6% [I].** The direct all-recipient figure on 1h − 1d − 1e (12.1%, 10.9–13.4%) now contains Chariot's figure. For the size-matched ≥$100m band (6.8%), Chariot's figure is still about twice as high, as wave 34B noted (V34B-08). The numerators still differ: Schedule I lines over $5,000 here, against all CRM-coded DAF gifts there.

## 1. Method

### 1.1 Sponsor universe and lines

- **Universe.** All 1,594 DAFRC 2025 panel EINs (`mission_net_payout.panel_from`).
- **Return choice.** As in the committed study, from the netpayout990 cache via `mission_daf_to_daf.pick_returns`: one return per sponsor and fiscal year, where the fiscal year is the calendar year in which the tax period ends. The cache holds 3,097 panel sponsor-years for FY2023–24 [F]:

  | Sponsor-years | Top 50 | Others |
  |---|---|---|
  | Itemised, lines read | 94 | 2,611 |
  | Not itemised: Schedule I points to an attachment (`mission_net_payout.itemized`) | 6 | 54 |
  | No Schedule I lines | 0 | 332 |

- **Lines.** Read with `mission_recipient_sectors.load_lines`, the parser used for the top 50.
  - The top-50 sponsor-years come from the committed cache (`rcp/lines`).
  - All 2,611 other sponsor-years were re-read from the GivingTuesday mirror of IRS TEOS into a new cache (`q120201/lines`). All 2,611 returned status `ok`, so every line count matched the netpayout990 count; there were no count mismatches or fetch failures [F].
  - Lines loaded: top 50, 604,913; others, 487,896.
- **Totals rows** were dropped with `mission_exception_load.drop_totals_rows`.
- **DAF-to-DAF netting** used `mission_recipient_sectors.annotate`. It drops lines to `decision = include` EINs in [`daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv), self-lines, and blank-EIN lines that uniquely match a whitelisted sponsor name. FY2024 non-top-50 lines dropped as DAF-to-DAF total $2.24bn [F].

### 1.2 DAF weighting

Each sponsor-year's lines are multiplied by a DAF share of its grants:
1. The `daf_share_of_grants` in [`sponsor-cost-structure.csv`](../../data/mission-2026-11-14/sponsor-cost-structure.csv), capped to [0, 1], as in the committed study. This covers 2,477 sponsor-years and $114.82bn of non-DAF-to-DAF Schedule I.
2. Otherwise, Schedule D DAF grants ÷ Part IX line 1 from the same cached return, capped. This applies to 2 sponsor-years.
3. Otherwise, 1. This applies to 226 sponsor-years with $0.78bn of Schedule I: 111 community foundations, 74 single-issue charities, 27 universities and hospitals, 13 nationals and 1 processor. None has Schedule D DAF grants in the cache.
   - A sensitivity with weight 0 for these sponsor-years is in §3.

### 1.3 Recipients and frames

- **Committed frame and sample.** The frame is BMF-listed recipient EINs with a positive top-50 numerator, excluding universities, hospitals, foundations, DAFRC-panel sponsors and non-501(c)(3)s (`mission_daf_share_recipient_revenue.exclusion`). The run rebuilds it at 138,832 EINs and redraws the same 2,352-EIN sample (seed 20261119, 400 certainty units, 40 per stratum) [F].
- **New-only frame.** The same filters applied to EINs with **no** top-50 grant but a positive non-top-50 numerator: 70,008 EINs holding $4.85bn of non-top-50 Schedule I (FY2023–24) [F].
  - A supplementary sample was drawn with `mission_daf_share_recipient_revenue.draw_sample`: a certainty stratum of the 100 largest by non-top-50 numerator, then up to 30 per NTEE major group × BMF revenue band, with `random.Random(20261120)`.
  - That gives 1,272 EINs in 52 strata, labelled `new|…`.
- **Expanded frame.** The committed frame plus the new-only frame: 208,840 EINs. The two samples cover disjoint strata, so the combined estimator is the usual stratified one.

### 1.4 Denominators

- **Returns.** Located as before, through the IRS TEOS index for 2023–2026 (`choose_filings`: the latest object id per tax period, then the latest period per FY). Read with the b40n1202-b43n26 Part VIII parser (`mission_recipient_basis_eligibility.fetch_part8`), which takes lines 1a–1h as direct children of `IRS990`, or EZ line 1.
- **Cache reuse.** All 4,315 committed-sample returns come from the **q1226 cache** (`q1226/f990p8`) with no re-fetch. Their 1h values were cross-checked against the **q1202 cache** (`q1202/f990`): 4,124 full-990 returns were compared and none differed by more than $1 [F].
- **Supplementary returns.** The 2,203 supplementary-sample returns were fetched into `q120201/f990p8`. Across all 6,518 returns, 6,512 parsed, 5 returned HTTP 404 (one of them already in the committed set) and 1 failed to parse [F].
- **Bases.**
  - `b1_1h`: Part VIII line 1h, the committed basis.
  - `b3_1abcf`: 1a + 1b + 1c + 1f = 1h − 1d − 1e, the b40n1202-b43n26 headline.
- **Wave 33A corrections** are those built into `recipient_a` and `weights_a`:
  - EINs whose returns parse but carry no 1h are out of scope (`no_contributions_line`), not missing;
  - weights are N_h / (n_h − xml_not_read_h);
  - medians are never divided by coverage.

### 1.5 Numerator variants and statistics

| Variant | Numerator | Recipients |
|---|---|---|
| `top50_old_frame` | Top 50 (committed) | Committed sample. Reproduces 6.9% / 10.3%. |
| `all_old_frame` | All itemising panel sponsors | Committed sample |
| `all_expanded_frame` | All itemising panel sponsors | Committed + supplementary samples |
| `other_expanded_frame` | Non-top-50 sponsors only | Committed + supplementary |
| `all_new_only` | All (= non-top-50) | Supplementary sample only |

- Numerators are matched to the recipient's readable fiscal years exactly as before.
- Pooled shares use the combined ratio estimator. Medians and quartiles are weighted.
- 95% intervals come from a stratified bootstrap with 500 replicates. NTEE group rows have no intervals.
- `scaled_pooled_inference` = pooled ÷ coverage of that variant's numerator: 0.6727 for the top 50, 0.8492 for all sponsors and 0.1765 for the others alone [I].

### 1.6 Robots and requests

- `gt990datalake-rawdata.s3.amazonaws.com/robots.txt` returned 404 on 2026-11-19 at 23:40 UTC, which places no restriction (logged in scratchpad `q120201/robots/log.tsv`).
- No other host was contacted. The IRS index and BMF files were already cached (Last-Modified 2026-11-09 for the BMF).
- User agent: `research-script/1.0`. sec.gov, crt.sh and certspotter were not used.

## 2. Results

### 2.1 Coverage of netted DAF grants

| Item (DAF-weighted, non-DAF-to-DAF, itemised Schedule I) | FY2024 | FY2023 |
|---|---|---|
| Top 50 | $39.29bn | $34.78bn |
| Other itemising panel sponsors | $10.31bn | $9.45bn |
| All itemising panel sponsors | $49.60bn | $44.23bn |
| Netted DAFRC DAF grants, central tier | $58.41bn | $50.78bn |
| **Top-50 coverage** | **67.3%** | 68.5% |
| **Others' coverage** | **17.6%** | 18.6% |
| **All-panel coverage** | **84.9%** | 87.1% |

All figures are [F].
- On the as-filed basis, the others' FY2024 non-DAF-to-DAF Schedule I is $19.63bn. DAF weighting roughly halves it, because these are mostly community foundations with discretionary grantmaking.
- **What no itemised line reaches.**
  - Of raw DAFRC FY2024 DAF grants ($64.60bn), sponsors with itemised FY2024 lines account for $62.53bn. Sponsors without them account for $2.07bn [F]. The largest are Bank of America Charitable Gift Fund ($1.04bn) and Renaissance Charitable Foundation ($0.72bn), both of which file Schedule I as an attachment, and Stifel Charitable ($0.05bn).
  - The whole 15.1-point gap is $8.8bn ($58.41bn × 0.151, netted and DAF-weighted); the non-itemising sponsors’ $2.07bn (raw) is part of it, not additional. The remainder is foreign grants, sub-$5,000 grants not itemised, timing, the $1.84bn by which corrected DAFRC grants ($66.44bn) exceed the raw total ($64.60bn) used for that split, and the difference between DAF weighting and netting. [V wave 40B] The cached data cannot separate these (P-B40N120201-01).

### 2.2 Headline shares, all in-scope recipients

All figures are [F] except the scaled column [I]. Percentages are weighted, with 95% bootstrap intervals in parentheses.

| Variant | Basis | Respondents | Weighted population | Median | Pooled | Weighted share ≥20% | Scaled pooled [I] |
|---|---|---|---|---|---|---|---|
| top50_old_frame (committed) | 1h | 2,170 | 95,875 | 5.9 (5.3–7.6) | 6.9 (6.1–7.8) | 20.4 | **10.3** (÷0.673) |
| top50_old_frame (committed) | 1h−1d−1e | 2,145 | 94,852 | 7.7 (5.9–8.9) | 10.3 (9.2–11.8) | 23.2 | **15.4** (÷0.673) |
| all_old_frame | 1h | 2,170 | 95,875 | 9.3 (8.0–10.7) | 8.4 (7.6–9.2) | 27.4 | 9.9 (÷0.849) |
| all_old_frame | 1h−1d−1e | 2,145 | 94,852 | 11.4 (9.9–13.3) | 12.6 (11.3–14.0) | 31.9 | 14.8 (÷0.849) |
| **all_expanded_frame** | **1h** | 3,264 | 140,573 | **6.8 (6.2–8.0)** | **7.3 (6.5–8.2)** | 24.7 | 8.7 (÷0.849) |
| **all_expanded_frame** | **1h−1d−1e** | 3,193 | 138,791 | **8.9 (7.8–10.1)** | **12.1 (10.9–13.4)** | 28.9 | 14.2 (÷0.849) |
| other_expanded_frame | 1h | 3,264 | 140,573 | 1.1 (0.9–1.3) | 1.5 (1.3–1.8) | — | — |
| other_expanded_frame | 1h−1d−1e | 3,193 | 138,791 | 1.6 (1.3–2.1) | 2.5 (2.2–2.9) | — | — |
| all_new_only | 1h | 1,094 | 44,698 | 3.9 (3.2–5.3) | 1.8 (1.1–3.0) | — | — |
| all_new_only | 1h−1d−1e | 1,048 | 43,938 | 5.6 (4.2–6.7) | 6.0 (4.3–8.4) | — | — |

- The top-50 rows reproduce the committed figures exactly: 6.9% and 5.9% on 1h, and 10.3% and 7.7% on 1h − 1d − 1e.
- The new-only recipients have low pooled shares. The group includes large organisations that simply had no itemised top-50 grant: Hexagon Foundation has a 1h of $600m over its two matched years ($95.9m and $503.8m) and received $29.0m DAF-weighted ($50.7m as filed) from Christian Community Foundation. Hexagon reports that money on line 1d as related-organisation support (1d: $7.50m and $43.23m, the same $50.73m in total), so on 1h − 1d − 1e its numerator keeps a gift its denominator removes [V wave 40B] They add denominator faster than numerator, which is why the expanded pooled share (7.3%) sits below the committed-frame all-sponsor share (8.4%).

### 2.3 How much the scaled estimate moves

| Basis | Committed inference (top 50 ÷ 0.673) [I] | Direct, committed frame [F] | Direct, expanded frame [F] | Move, inference → direct expanded | Residual-scaled, expanded (÷0.849) [I] |
|---|---|---|---|---|---|
| 1h | 10.3% (9.0–11.6) | 8.4% (7.6–9.2) | **7.3% (6.5–8.2)** | **−2.9 points (−28%)** | 8.7% |
| 1h − 1d − 1e | 15.4% (13.6–17.6) | 12.6% (11.3–14.0) | **12.1% (10.9–13.4)** | **−3.3 points (−22%)** | 14.2% |
| 1h, ≥$100m band | 5.5% | 4.4% | 3.7% (3.0–4.8) | −1.8 points | 4.4% |
| 1h − 1d − 1e, ≥$100m | 8.7% | 7.0% | 6.8% (5.4–8.9) | −1.9 points | 8.1% |
| 1h − 1d − 1e, $25–100m | 16.4% | 12.7% | 12.3% (11.1–13.8) | −4.1 points | 14.5% |

- The interval for the inference is the committed pooled interval divided by 0.673. For both main bases it does not overlap the direct expanded-frame interval. It does overlap the direct committed-frame interval (1h: 7.6–9.2% against 9.0–11.6%; 1h − 1d − 1e: 11.3–14.0% against 13.6–17.6%), and all figures rest on the same sample, so non-overlap is not a significance test [V wave 40B]
- **Mechanism [F].**
  - Within the committed frame, Σw·(non-top-50 numerator) ÷ Σw·(top-50 numerator) = **0.214**. The scaling assumes 1/0.673 − 1 = **0.486**.
  - Dollar disposition of FY2023–24 DAF-weighted grants, from the full universe with no sampling:

| Where the dollars land | Top 50 | Others |
|---|---|---|
| Committed-frame recipients | 67.7% ($50.17bn) | 58.9% ($11.64bn) |
| New-only frame recipients | — | 13.7% ($2.71bn) |
| Universities | 9.2% | 6.2% |
| Hospitals | 3.1% | 1.9% |
| Foundations (NTEE T20–31, private foundations) | 4.2% | 3.4% |
| DAFRC-panel DAF sponsors not on the whitelist | 9.6% | 3.6% |
| Not 501(c)(3) | <0.1% | 0.6% |
| Not in BMF | 5.6% | 5.8% |
| Blank EIN | 0.5% | 5.9% |
| **Total** | $74.07bn | $19.76bn |

- The others put a smaller share of their dollars into the committed frame (58.9% against 67.7%). Some of their money goes to recipients outside it, and some to blank-EIN lines that cannot be placed.
- The larger effects are the unassigned gap and the frame, not where non-top-50 dollars land. On the committed frame with both sides divided by coverage, the move is 10.3% → 9.9% (1h) and 15.4% → 14.8% (1h − 1d − 1e). The rest of the move to the direct expanded figures comes from leaving the 15.1% gap unassigned (−1.5 and −2.2 points) and from adding new-only recipients (−1.0 and −0.5 point) [V wave 40B]

### 2.4 By revenue band (BMF REVENUE_AMT), all sponsors, expanded frame

Shares are [F] unless marked [I].

| Band | Respondents (1h) | Median, 1h | Pooled, 1h | Median, 1h−1d−1e | Pooled, 1h−1d−1e | Committed scaled pooled, 1h [I] | Committed scaled pooled, 1h−1d−1e [I] |
|---|---|---|---|---|---|---|---|
| <$1m | 530 | 9.8 | 17.9 (13.1–24.5) | 10.7 | 21.3 (15.8–27.6) | 26.4 | 31.2 |
| $1–5m | 729 | 5.0 | 10.8 (8.4–13.5) | 6.9 | 13.9 (10.9–17.2) | 14.2 | 17.3 |
| $5–25m | 748 | 4.2 | 9.2 (7.6–11.1) | 7.9 | 14.6 (12.0–17.5) | 13.0 | 18.6 |
| $25–100m | 718 | 2.9 | 6.5 (5.7–7.2) | 6.9 | 12.3 (11.1–13.8) | 9.3 | 16.4 |
| ≥$100m | 539 | 1.3 | 3.7 (3.0–4.8) | 4.9 | 6.8 (5.4–8.9) | 5.5 | 8.7 |

On the committed frame, all-sponsor pooled shares on 1h are 20.5%, 12.7%, 10.7%, 7.3% and 4.4% from the smallest band to the largest. Non-top-50 money lifts the <$1m and $1–5m bands most in relative terms [F].

### 2.5 By NTEE major group, all sponsors, expanded frame, pooled [F]

| Group | 1h | 1h − 1d − 1e | Top-50 committed (1h) |
|---|---|---|---|
| Arts and culture | 9.3 | 12.5 | 8.1 |
| Education (excluding universities) | 7.4 | 12.5 | 6.9 |
| Environment and animals | 11.6 | 14.3 | 10.2 |
| Health (excluding hospitals) | 7.0 | 11.8 | 6.8 |
| Human services | 6.1 | 11.5 | 5.7 |
| International | 6.5 | 8.4 | 4.9 |
| Public and societal benefit | 10.2 | 20.3 | 12.9 |
| Religion (990 filers) | 8.8 | 9.1 | 7.6 |
| No NTEE | 4.9 | 9.2 | 4.6 |

- These rows have no bootstrap intervals. Group respondents number 209–413 apart from mutual membership and unknown_z (see the CSV).
- The ordering is little changed from the top-50 study. International remains among the lowest by pooled share.

## 3. Sensitivities

| Scope | Expanded, all sponsors, 1h | Expanded, all sponsors, 1h − 1d − 1e |
|---|---|---|
| All (headline) | 7.3% | 12.1% |
| Excluding leaked non-panel DAF sponsors (name regex from b40n1202-b43n26) | 7.0% | 11.6% |
| Non-certainty recipients only | 6.1% | 10.6% |
| Default DAF weight 0 instead of 1 for the 226 unweighted sponsor-years (scratch run, no bootstrap) | 7.3% (0.0731 against 0.0735) | 12.0% |

- The default-weight choice moves all-panel FY2024 coverage from 84.9% to 84.3%, which is immaterial [F].
- The largest non-top-50 recipient in the sample is the Jewish Federations of North America, with $90.5m in matched years. It is a leaked non-panel sponsor, already flagged in waves 33A and 34B.

## 4. Limits

1. **The direct figure is a floor for all DAF grants.** 15.1% of netted FY2024 DAF grants never appears on an itemised panel Schedule I line. That covers foreign grants (Schedule F), grants under $5,000 per recipient, and non-itemising sponsors such as BofA CGF and RCF ($2.07bn raw). The residual-scaled figures (8.7% and 14.2%) assume that money reaches frame recipients in the measured proportions. Foreign grants and sub-$5,000 gifts make that lean high.
2. **DAF weighting is sponsor-level.** It matters more here than for the top 50: weighting halves the others' Schedule I ($19.63bn as filed against $10.31bn weighted, FY2024), because community-foundation discretionary grants are removed pro rata. CFs whose DAF grants go disproportionately to particular recipients are misallocated.
3. **The netpayout990 cache defines the sponsor universe.** Panel sponsor-years with no cached FY2023–24 return are not represented. 332 other sponsor-years have no Schedule I lines and 60 are attachment-only (6 of them top 50). Their DAF grants are in the coverage gap, not the numerator.
4. **Classification.** Exclusions, bands and groups are as in the committed study: BMF revenue from the latest filing, and name-based university and hospital rules. Non-panel DAF sponsors (federations, NCF affiliates) remain in the frame except in the leaked-sponsor sensitivity, and that regex misses UJA-Federation.
5. **New-only sample size.** 1,094 in-scope respondents (weighted population 44,698) give wide intervals for that sub-frame (pooled 1.1–3.0% on 1h). Its strata hold 30 each, against 40 in the committed sample.
6. **Blank-EIN lines** are 5.9% of non-top-50 dollars, against 0.5% for the top 50. They cannot be assigned to recipients, so they are absent from every share. This is a downward bias of at most 5.9% of the others' dollars [I].
7. **Timing, pledges and EZ filers** carry over unchanged from the committed study: 2.6% (weighted) of expanded-frame recipients have shares above 100% on 1h.
8. **Sampling.** The bootstrap covers sampling error only, not the definitional choices above.

## 5. Reproduction

```
S=<scratchpad>; Q=$S/q120201
python3 scripts/mission_non_top50_numerator.py . --np-cache $S/npcache --lines-cache-top50 $S/rcp/lines \
    --lines-cache $Q/lines --bmf-dir $S/rcp/bmf --index-dir $S/irs --p8-cache $S/q1226/f990p8 \
    --p8-cache-new $Q/f990p8 --f990-check $S/q1202/f990 [--fetch] [--boot 500] [--default-weight 1]
```
- The first run, with `--fetch`, re-read 2,611 sponsor returns and 2,203 recipient returns in about 6 minutes.
- A cache-only rerun takes about 2.5 minutes. The fetch run and two cache-only reruns produced the same CSV; the two cache-only reruns were byte-identical (md5 435ac483…).
- stdout is a JSON diagnostic: sponsor-year status, weight sources, coverage, frame sizes, fetch status, the q1202 cross-check, uplift, disposition, headline, bands and the largest non-top-50 recipients.

## 6. Data dictionary: `non-top50-numerator-2026-11-19.csv`

Shares are fractions (0.073 = 7.3%). The `row_type` column decides which columns are used.

**`summary` rows** (190 = 5 variants × 19 scopes × 2 bases)

| Column | Meaning |
|---|---|
| variant | `top50_old_frame`, `all_old_frame`, `all_expanded_frame`, `other_expanded_frame`, `all_new_only` (§1.5) |
| numerator | `top50`, `all` or `other` |
| frame | `committed`, `expanded` or `new_only` |
| basis | `b1_1h` or `b3_1abcf` (1h − 1d − 1e) |
| scope_type / scope | `all`/`all_ex_excluded`; `sensitivity` (`ex_leaked_daf_sponsors`, `non_certainty_only`); `revenue_band` (a <$1m … e ≥$100m, BMF REVENUE_AMT); `ntee_major_group` |
| sampled, respondents, weighted_recipients | Sampled EINs in scope; `ok` respondents with a positive basis denominator; Σ weights |
| p25_share, median_share, p75_share | Weighted quantiles of per-recipient share |
| median_ci95_lo/_hi, pooled_ci95_lo/_hi | Stratified bootstrap 95% interval, 500 replicates. Blank for NTEE group rows. |
| pooled_share | Σw·numerator ÷ Σw·denominator |
| share_ge_20pct, share_gt_100pct | Weighted fraction of respondents with share ≥0.2 and >1 |
| coverage_used | FY2024 coverage of the variant's numerator: 0.6727 top 50, 0.8492 all, 0.1765 other |
| scaled_pooled_inference | **[I]** pooled_share ÷ coverage_used |
| den_nonpos_respondents, den_nonpos_num_share | `ok` respondents with a basis denominator ≤0, and their share of weighted numerator |

**`disposition` rows** (9): `category` is where FY2023–24 DAF-weighted, non-DAF-to-DAF Schedule I dollars land: `frame_committed`, `frame_new_only`, `excluded_*`, `not_in_bmf` or `blank_ein`. Columns `recipients_top50`, `recipients_other`, `usd_top50_daf_weighted`, `usd_other_daf_weighted`, `share_of_top50_usd` and `share_of_other_usd` give the counts, dollars and shares. Blank-EIN recipients are counted by normalised name.

**`coverage` rows** (28)
- `item` is one of:
  - `{top50|other|all}_{sched_i_non_d2d|daf_weighted_non_d2d|d2d_dropped}` (USD);
  - `{…}_share_of_netted_daf_weighted`;
  - `netted_dafrc_daf_grants_central`;
  - `dafrc_raw_daf_grants`.
- `fiscal_year` is 2023 or 2024, and `value` holds the figure.

**`recipient` rows** (3,624)

| Column | Meaning |
|---|---|
| sample_part | `committed` (2,352) or `new_only` (1,272 supplementary) |
| ein, name, ntee_cd, ntee_major_group, revenue_band | From the IRS EO BMF |
| stratum, stratum_N | Sampling stratum (`certainty`, `group\|band`, `new\|certainty`, `new\|group\|band`) and its frame size |
| top50_grantors, other_grantors | Distinct top-50 and other panel sponsors granting in FY2023–24 |
| num_top50_dw_fy2023_2024_all, num_other_dw_fy2023_2024_all | DAF-weighted numerators over both FYs, regardless of matching |
| years_matched, forms, object_ids | FYs with a readable contributions total; form types; TEOS object ids |
| num_top50_dw_matched, num_other_dw_matched, num_all_dw_matched | DAF-weighted numerators over matched FYs, USD |
| den_b1_1h, den_b3_1abcf | Denominators over matched FYs, USD |
| share_{top50,other,all}_{b1_1h,b3_1abcf} | Per-recipient shares (blank unless status `ok` and denominator >0) |
| leaked_sponsor_name | Name matches the non-panel DAF-sponsor regex of b40n1202-b43n26 |
| status | `ok`; `no_fy2023_2024_990_or_ez_in_index`, `no_contributions_line` or `zero_or_negative_contributions` (out of scope); `xml_not_read` (missing; 1, in the new-only sample) |
| source | Source note |

## 7. Source register

| ID | Source | URL | Accessed / version | Use |
|---|---|---|---|---|
| S1 | IRS Form 990 e-file XML, GivingTuesday mirror of IRS TEOS | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | 2026-11-19 (robots.txt 404) | Sponsor Schedule I Part II lines (2,611 sponsor-years re-read); recipient Part VIII (2,203 new returns) |
| S2 | IRS TEOS e-file index | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (and 2023, 2025, 2026) | Cached 2026-11-14/15 | Locating recipient returns |
| S3 | IRS EO Business Master File | https://www.irs.gov/pub/irs-soi/eo1.csv (eo1–eo4, eo_pr, eo_xx) | Cached; Last-Modified 2026-11-09 | NTEE, FOUNDATION, SUBSECTION, REVENUE_AMT |
| S4 | IRS Instructions for Form 990 and Schedule I | https://www.irs.gov/instructions/i990 ; https://www.irs.gov/pub/irs-pdf/i990si.pdf | Current editions (as cited in the committed studies) | Line 1a–1h definitions; $5,000 itemisation threshold |
| S5 | DAFRC Annual DAF Report 2025 updated dataset (repo copy) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx ; [dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | Repo | Panel, top-50 ranking, raw DAF grants |
| S6 | Repo netted market totals | [dafrc-market-totals-netted.csv](../../data/mission-2026-11-14/dafrc-market-totals-netted.csv) | Repo | Netted FY2023–24 DAF grants (central) |
| S7 | Repo DAF-to-DAF whitelist and sponsor cost structure | [daf-to-daf-recipient-whitelist.csv](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv); [sponsor-cost-structure.csv](../../data/mission-2026-11-14/sponsor-cost-structure.csv) | Repo | Netting; DAF weights |
| S8 | Committed studies and validations | [b40n12-daf-share-of-recipient-revenue.md](b40n12-daf-share-of-recipient-revenue.md); [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md); [validation-wave33a-report.md](validation-wave33a-report.md); [validation-wave34b-report.md](validation-wave34b-report.md) | Repo | Method, corrections, comparison figures |
| S9 | Chariot/K2D DAF Fundraising Report 2026 (as recorded in the repo) | https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release | Not re-fetched; repo NPB001–002 as validated in waves 25B and 33A | 12.6% comparison only |
