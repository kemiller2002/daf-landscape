# Large-donor share of recipients' line 1f, and the DAF share net of the 2% excess (P-B40N1202-B43N26-01)

**Date:** 2026-11-20 · **Task ID:** b40n1202-b43n26-01 · **Builds on:** [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md) §1.2 and §5 item 1

**Outputs**
- Script: [`scripts/mission_schedule_a_excess.py`](../../scripts/mission_schedule_a_excess.py) (new; reads the committed recipient rows and imports helpers only)
- Data: [`data/mission-2026-11-14/schedule-a-excess-2026-11-20.csv`](../../data/mission-2026-11-14/schedule-a-excess-2026-11-20.csv). 93 summary rows, 4 sponsor-status rows and 2,352 recipient rows
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b40n1202-b43n26-01.csv`](../../data/mission-2026-11-14/queue-proposals-b40n1202-b43n26-01.csv)

Tags: [F] computed from filings by the script · [P] quoted primary source · [I] inference.

## 0. Answer in brief

- **What line 5 measures.** Schedule A Part II line 5 is "the portion of total contributions by each individual, trust, or corporation included on line 1 for the years reported that exceeds 2% of the amount reported in line 11, column (f)" [P]. It is a five-year total and has no year columns.
- **Most DAF grants are outside line 5. The task brief assumed the opposite.** The IRS instructions say "the 2% limitation doesn't apply to contributions from organizations qualifying as publicly supported organizations under section 170(b)(1)(A)(vi)" or from governmental units [P]. Sponsors coded 170(b)(1)(A)(vi) in the BMF (FOUNDATION 15) account for **98.4%** of the top-50 sponsors' FY2024 DAF grants ($49.85bn): 47 of the 50 sponsors [F]. So under the instructions, a recipient's DAF grants stay in its public support and are **not** in line 5. Line 5 therefore holds large individuals, family trusts, private foundations and corporations. It catches a DAF sponsor only when the sponsor is not a (vi) organisation, or when the filer attributes the grant to the underlying donor [I].
- **Coverage.** 1,496 of the 2,170 in-scope respondents (54,914 weighted recipients) file Part II in every matched year. They receive **84.3%** of the weighted DAF numerator [F]. Part III filers (509(a)(2)) receive 11.1%; Part III has no 2% line. Organisations with no support schedule (schools, hospitals, churches, supporting organisations) receive 3.8%.
- **Year alignment.** Part II line 1 column (e) equals Part VIII line 1h in every quartile (weighted quartiles of the ratio are 1.00, 1.00 and 1.00) [F]. The five-year excess is put on a single-year basis in three ways (§1.3). The central method applies the five-year ratio line 5 ÷ line 1(f) to the current-year column.
- **Large-donor share of 1f (central, current-year allocation)** [F]:
  - **Part II filers: pooled 18.5%** (95% CI 15.2–22.5%), **median 1.8%** (0.0–4.6%). 46.1% of them (weighted; 500 of 1,496) report line 5 = 0.
  - All in-scope recipients, counting the excess as zero where no Part II exists: pooled 15.3% (12.5–18.5%).
  - Pooled shares are high because a few in-kind relief charities dominate them. Good360, Feeding America, Direct Relief and Americares together hold 23.5% of the weighted Part II excess. Leaving out recipients whose noncash gifts (1g) are 25% or more of 1h still gives a pooled 16.0% (14.3–17.7%).
  - The per-year-average allocation gives a pooled 16.0% (Part II). Charging the whole five-year excess to the current year, an upper bound, gives 47.0%.
- **DAF share of 1f net of the excess (central)** [F]:

| Scope | 1f basis: median / pooled | Net of excess (cy): median / pooled |
|---|---|---|
| All in-scope (2,134 respondents) | 8.1% (6.9–9.8) / 11.0% (9.7–12.4) | **8.9% (7.6–10.8) / 13.0% (11.6–14.7)** |
| Part II filers (1,484) | 9.2% (7.3–12.4) / 11.4% (9.7–13.3) | **12.0% (9.1–13.6) / 13.9% (12.2–16.0)** |
| Part II, non-certainty strata | 8.9% / 9.7% | 11.6% (8.9–13.7) / 11.7% (10.0–13.5) |
| Part II, noncash < 25% of 1h | 10.2% / 14.4% | 12.9% (9.4–14.4) / 17.1% (14.9–19.4) |

  - The per-year-average allocation is within half a point of these figures: all in-scope pooled 12.7%, Part II pooled 13.5%.
  - The upper-bound allocation gives a Part II pooled 21.5% (18.6–24.9%), but the excess then absorbs the whole of 1f for 17.4% of recipients (weighted).
  - The 1f-basis row reproduces the committed `b6_1f` figures exactly (median 8.09%, pooled 11.04%).
- **By size (Part II, pooled, 1f → net)** [F]: <$1m 29.9% → 34.2%; $1–5m 14.0% → 16.7%; $5–25m 14.1% → 17.2%; $25–100m 12.4% → 14.5%; ≥$100m 6.2% → 8.0%. The large-donor share of 1f is 13–22% in every band, so netting it moves every band up by about a fifth, and the size gradient stays.
- **Part III filers** [F]: line 7a (amounts on lines 1–3 from disqualified persons), current year, is 7.6% of 1f pooled (5.4–10.1%). Net of it, the DAF share moves from 9.9% to 10.7% pooled (8.8–12.9%).
- **What the net figure means.** 1f net of the line 5 excess is the sub-2% "public support" part of 1f. It is **not** individual giving:
  - it still contains each large donor's gifts up to the 2% threshold, every grant from a (vi) organisation (including the DAF grants themselves) and smaller foundation and corporate gifts;
  - it no longer contains large individual donors.
  - Measured against an all-individual denominator the bias can run either way. Measured against small-donor giving plus grants from public charities, it is a lower bound.
  - Read 13.0–13.9% as "the DAF share of contributions from donors below the 2% limit", not as an individual-only share [I].

## 1. Method

### 1.1 Sample, weights, numerator
- **Inputs.** The 2,352 recipient rows of [`daf-share-individual-basis-2026-11-19.csv`](../../data/mission-2026-11-14/daf-share-individual-basis-2026-11-19.csv) are read unchanged. This gives the EIN, stratum, `stratum_N`, status, FY2023/FY2024 object ids, the top-50 DAF-weighted numerator and the Part VIII line totals.
- **Weights.** The pipeline's weights are recomputed: N_h ÷ (n_h − `xml_not_read`), as in `weights_a` in `mission_recipient_basis_eligibility.py`. Respondents are the `b6_1f` set (status `ok`, 1f > 0): 2,134 recipients, 93,949 weighted.
- **Per-return 1f** comes from the committed Part VIII cache (`q1226/f990p8`). All 4,281 returns were found there. For 990-EZ years, line 1 stands in for 1f, as in the pipeline.

### 1.2 Schedule A
- **Source.** Each of the 4,281 returns was re-read from the GivingTuesday mirror of IRS TEOS XML. Schedule A leaves up to depth 2 are cached in `sa01/schA/`.
- **Parse results.** 4,279 parsed. One return has no Schedule A (202412289349301926) and one gave an XML parse error (202411219349302356) [F].
- **Fields read:**

| Line | XML element | Columns |
|---|---|---|
| Part II line 1 (gifts, grants, contributions, membership fees) | `GiftsGrantsContriRcvd170Grp` | 5 years + total |
| Part II line 5 (excess over 2%) | `SubstantialContributorsTotAmt` | total only; absent = 0 |
| Part II line 11 (total support) | `TotalSupportAmt` | total |
| Part III line 1 | `GiftsGrantsContrisRcvd509Grp` | 5 years + total |
| Part III line 7a (disqualified persons, lines 1–3) | `AmountsRcvdDsqlfyPersonGrp` | 5 years + total; absent = 0 |
| Part III line 7b (not used) | `SubstantialContributorsAmtGrp` | covers receipts on lines 2–3 only |

- **Part detection.** A return counts as Part II when it has any of these: Part II line 1, 5 or 11, `PublicSupportTotal170Amt`, or `TotalCalendarYear170Grp`. The Part III equivalents are used for Part III. Recipients are grouped as `part_ii_all_years`, `part_iii_all_years`, `no_support_schedule` or `mixed_or_missing`.
- **Why Part III has no line-5 analogue.** Its line 7a covers "amounts that are included on lines 1, 2, and 3 that the organization received from disqualified persons" [P]. Line 7b covers lines 2–3 receipts above the greater of $5,000 or 1% [P]. 7a is reported as a separate, looser proxy and is not pooled with Part II.

### 1.3 The five-year window
Line 5 covers tax years t−4 to t, while 1f covers year t. For each Part II return:
- **cy (central):** E = line 5 × line 1(e) ÷ line 1(f). This assumes a large donor's share of contributions is the same in every year of the window.
- **avg:** E = line 5 ÷ the number of positive line-1 year columns, i.e. the per-year average excess.
- **all (upper bound):** E = line 5, the whole window charged to year t.
- **Cap.** E is capped at the return's 1f, since the excess must sit in contributions other than government grants. The cap binds for 25, 56 and 472 returns under cy, avg and all respectively.
- **Two matched years.** E and 1f are summed over the recipient's matched FYs.
- **Window dates.** For FY2023–24 returns the window runs from 2019/2020 to 2023/2024. The pre-2021 columns are as reported in 2023+ filings.

### 1.4 Statistics
- **Share definitions.** share_net = DAF-weighted numerator ÷ (1f − E). large_share = E ÷ 1f.
- **Absorbed denominators.** Where E absorbs all of 1f, the net share is +inf. Such a recipient stays in the respondent set: it ranks top for quantiles, and its numerator stays in pooled ratios. The weighted share of these cases is reported as `share_den_absorbed`.
- **Estimators.** The weighted median and pooled ratio estimator are the pipeline's.
- **Intervals.** A stratified bootstrap with 500 replicates resamples respondents within stratum, with weights fixed. Seeds are 20261120 + 31·scope + measure.
- **Reproducibility.** Two runs produced byte-identical CSVs (md5 0d880582…).

## 2. Results

### 2.1 Coverage by support schedule (in-scope `ok` respondents)

| Group | Respondents | Weighted | Share of weighted DAF numerator |
|---|---|---|---|
| Part II every year | 1,496 | 54,914 | 84.3% |
| Part III every year | 472 | 31,262 | 11.1% |
| No support schedule | 175 | 7,209 | 3.8% |
| Mixed or missing | 27 | 2,491 | 0.7% |

### 2.2 Part II: large-donor share of 1f (E ÷ 1f)

| Allocation | Median (CI) | Pooled (CI) |
|---|---|---|
| cy (central) | 1.8% (0.0–4.6) | 18.5% (15.2–22.5) |
| avg | 0.8% (0.1–3.8) | 16.0% (13.6–18.5) |
| all (upper) | 4.0% (0.0–16.9) | 47.0% (42.0–52.5) |

By revenue band (cy, pooled; median): <$1m 12.7% (0.0%); $1–5m 16.0% (7.3%); $5–25m 18.1% (7.9%); $25–100m 14.5% (2.1%); ≥$100m 22.0% (1.0%).

### 2.3 DAF share net of the excess

Part II filers:

| Measure | Median (CI) | Pooled (CI) | Share > 100% (weighted) |
|---|---|---|---|
| 1f | 9.2% (7.3–12.4) | 11.4% (9.7–13.3) | 5.0% |
| Net, cy | 12.0% (9.1–13.6) | 13.9% (12.2–16.0) | 6.9% |
| Net, avg | 11.7% (8.9–13.7) | 13.5% (11.8–15.5) | 6.3% |
| Net, all | 21.4% (16.2–27.1) | 21.5% (18.6–24.9) | 27.3% (17.4% absorbed) |

All in-scope recipients, with E = 0 where there is no Part II:

| Measure | Median (CI) | Pooled (CI) |
|---|---|---|
| 1f | 8.1% (6.9–9.8) | 11.0% (9.7–12.4) |
| Net, cy | 8.9% (7.6–10.8) | 13.0% (11.6–14.7) |
| Net, avg | 9.0% (7.4–11.0) | 12.7% (11.3–14.3) |
| Net, all | 13.0% (10.2–15.0) | 18.1% (16.0–20.5) |

Part II by band, pooled, 1f → net cy (CI of net):

| Band | 1f | Net cy | Median 1f → net |
|---|---|---|---|
| <$1m | 29.9% | 34.2% (21.2–49.8) | 15.0% → 16.6% |
| $1–5m | 14.0% | 16.7% (11.0–22.6) | 5.5% → 6.2% |
| $5–25m | 14.1% | 17.2% (13.4–22.8) | 5.4% → 7.2% |
| $25–100m | 12.4% | 14.5% (12.4–17.0) | 5.9% → 7.5% |
| ≥$100m | 6.2% | 8.0% (6.2–10.5) | 3.5% → 4.4% |

**Part III** (452 respondents): 1f median 7.6% and pooled 9.9% (8.2–12.0%); net of 7a, median 8.2% and pooled 10.7% (8.8–12.9%). **No support schedule** (171): pooled 8.7%, unchanged.

### 2.4 Who is in line 5
- **Top contributors.** The four largest contributors to the weighted Part II excess are in-kind relief and redistribution charities: Good360 9.1%, Feeding America 7.2%, Direct Relief 3.9% and Americares 3.3%. Their five-year excess ratios are 0.46–0.74. This fits corporate product donations above the 2% limit [I].
- **Restricted scope.** In the scope restricted to noncash below 25% of 1h, the pooled large-donor share is 16.0%. The net DAF share is 17.1%, up from 14.4%.
- **DAF sponsors' status.** Top-50 FY2024 sponsors weighted by DAFRC FY2024 DAF grants: FOUNDATION 15 [(vi)] 98.4% (47 sponsors); 17 [509(a)(3)] 0.8% (1); 11 [school] 0.2% (1); not in the BMF 0.6% (1) [F].

## 3. Interpretation limits

1. **Not an individual-only basis.** 1f − E removes large individuals and keeps smaller institutional gifts, so its bias against an all-individual denominator has no fixed sign. It is better described as the DAF share of sub-2% contributions [I].
2. **The 2% excess is a floor on large-donor money.** Each large donor's first 2% of five-year total support stays in public support. Line 5 is per donor, including related persons aggregated under section 4946 [P]. Large-donor gifts are therefore understated, and so is the net DAF share against a "small donor" basis.
3. **DAF sponsors are mostly outside line 5 under the instructions, but filer practice varies.** A filer may attribute DAF grants to the advising donor, or a sponsor may not be (vi). In those cases DAF dollars sit in E and 1f − E can fall below the numerator. Part II net shares above 100% rise from 5.0% to 6.9% (weighted). For example, Grounded Solutions Network has an $11.2m numerator against 1f of $19.8m and a cy excess of $10.7m. This cannot be confirmed without the donor list, which the instructions tell filers not to file [P].
4. **Line 5 = 0 for 46.1% of Part II filers (weighted).** The filings cannot separate "no donor above 2%" from "not computed". Organisations in their first five years complete Part II too (`First5Years170Ind`, 157 leaves), but the 33⅓% test is not binding for them [I].
5. **Window mismatch.** The cy allocation assumes the excess ratio is constant across the five years. Large one-off gifts in t−4 to t−1 move E even when year t had none. The avg and all variants bracket this.
6. **Coverage.** Part III filers (11.1% of the numerator) have no 2% line, and schools, hospitals and churches have no support schedule at all. The all-recipient figure treats both groups as having no excess.
7. **Carry-over limits.** All numerator, scaling and sample limits of the parent study carry over (top-50 sponsors, grants over $5,000, sponsor-level DAF weighting, BMF bands). BMF FOUNDATION codes are as of November 2026, not grant time.

## 4. Reproduction

```
S=<scratchpad>
python3 scripts/mission_schedule_a_excess.py . --sa-cache $S/sa01/schA --p8-cache $S/q1226/f990p8 \
    --bmf-dir $S/rcp/bmf [--fetch] [--boot 500]
```
- About 1.5 minutes to fetch 4,281 returns (12 workers) and 70 seconds to compute with 500 replicates.
- Prints a JSON summary of coverage, cap counts, line 1(e) ÷ 1h quartiles and line-5-zero counts.

## 5. Data dictionary: `schedule-a-excess-2026-11-20.csv`

Shares are fractions. `row_type` is `summary`, `sponsor_status` or `recipient`.

| Column | Meaning |
|---|---|
| row_type | `summary` (scope × measure), `sponsor_status` (top-50 sponsors by BMF FOUNDATION), `recipient` |
| scope | `all_ex_excluded`; `part_ii_all_years` (+ `_non_certainty`, `_form_990_only`, `_noncash_lt_25pct_of_1h`); `part_iii_all_years`; `no_support_schedule`; `mixed_or_missing`; `part_ii_band_<BMF band>`; `top50_fy2024_daf_assets` |
| measure | `daf_share_1f`; `daf_share_1f_net_{cy,avg,all}`; `large_donor_share_of_1f_{cy,avg,all}`; Part III: `daf_share_1f_net_p3_7a`, `dq_share_of_1f_p3_7a`; sponsor rows: `bmf_foundation_<code>` |
| sampled | Sampled EINs in scope (sponsor rows: number of sponsors) |
| respondents, weighted_recipients | Status `ok` with 1f > 0, and the sum of their weights |
| dropped_1f_nonpos | `ok` recipients with 1f ≤ 0 |
| p25, median, p75 | Weighted quantiles of the per-recipient share (+inf counts as the top value) |
| median_ci95_lo/_hi, pooled_ci95_lo/_hi | Stratified bootstrap 95% interval (500 replicates) |
| pooled | Σw·num ÷ Σw·den (sponsor rows: share of top-50 FY2024 DAF grants) |
| share_gt_100pct | Weighted share of respondents whose share is above 1 |
| share_den_absorbed | Weighted share whose net denominator is ≤ 0 (E took all of 1f) |
| weighted_num_usd, weighted_den_usd | Σw·numerator and Σw·denominator (sponsor rows: FY2024 DAF grants, USD) |
| ein, name, ntee_major_group, revenue_band, stratum, stratum_N, status, years_matched, object_ids, forms | As in the parent file |
| schedule_a_parts, schedule_a_status | Per matched return: `II`, `III`, `II+III` or `none`; cache status |
| support_group | `part_ii_all_years`, `part_iii_all_years`, `no_support_schedule`, `mixed_or_missing`, `no_return` |
| part1_indicators | Schedule A Part I checkboxes per return (`|` separates returns) |
| num_daf_weighted_matched, l1f_matched, l1h_matched, l1g_noncash_matched | Parent numerator and Part VIII lines over matched FYs, USD |
| sa_p2_l1_cy_matched, sa_p2_l1_5y_matched, sa_p2_l5_matched | Part II line 1 column (e), line 1 column (f) and line 5, summed over matched returns |
| excess_ratio_5y | Σ line 5 ÷ Σ line 1(f) |
| sa_l1_cy_over_1f, sa_l1_cy_over_1h | Line 1(e) ÷ 1f and ÷ 1h (alignment checks) |
| excess_cy, excess_avg, excess_all | Allocated current-year excess E (§1.3), capped at 1f, USD |
| capped_cy/_avg/_all | True if the cap bound in any matched return |
| sa_p3_l1_cy_matched, sa_p3_l7a_cy_matched | Part III line 1(e), and line 7a(e) capped at 1f |
| share_1f, share_1f_net_{cy,avg,all}, share_1f_net_p3_7a | Per-recipient shares (`inf` = denominator absorbed) |
| large_share_{cy,avg,all}, large_share_p3_7a | E ÷ 1f |
| source | Source note |

## 6. Source register

| ID | Source | URL | Accessed | Use |
|---|---|---|---|---|
| S1 | IRS, Instructions for Schedule A (Form 990) (2025) | https://www.irs.gov/instructions/i990sa | 2026-11-20 (robots.txt 200; `/instructions/` not disallowed) | Line 5 definition and 2% exemptions; Part III lines 7a and 7b |
| S2 | IRS Form 990 e-file XML, GivingTuesday mirror of IRS TEOS | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | 2026-11-20 (robots.txt 404) | Schedule A for 4,281 returns |
| S3 | Parent sample file | [daf-share-individual-basis-2026-11-19.csv](../../data/mission-2026-11-14/daf-share-individual-basis-2026-11-19.csv) | Repo | Sample, strata, weights, numerator, Part VIII lines |
| S4 | IRS EO Business Master File | https://www.irs.gov/pub/irs-soi/eo1.csv (eo1–eo4, eo_pr, eo_xx) | Cached (Last-Modified 2026-11-09) | Sponsor FOUNDATION codes |
| S5 | DAFRC Annual DAF Report 2025 dataset (repo copy) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx; [dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | Repo | Top-50 sponsors; FY2024 DAF grants |
| S6 | IRS TEOS e-file index (via the parent study) | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv | Cached 2026-11-14/15 | Return choice (inherited) |

**Robots and fetch logs** are in the scratchpad at `sa01/robots/log.tsv` (gt990datalake-rawdata.s3.amazonaws.com 404; www.irs.gov 200; apps.irs.gov 302) and `sa01/fetchlog.tsv`. All requests used user agent `research-script/1.0`. sec.gov, crt.sh and certspotter were not used, and there was no outreach or login.
