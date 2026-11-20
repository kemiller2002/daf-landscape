# Recipient DAF share on an enlarged sample: thin-stratum supplements and a census of recipients with revenue of $25m or more (P-B40N1202-04)

**Date:** 2026-11-20 · **Task ID:** b40n1202-04 · **Queue item:** P-B40N1202-04 · **Builds on:** [b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md) (central bounded allocation) and [b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md) (frames, samples, Part VIII reader)

**Outputs**
- Script: [`scripts/mission_recipient_census.py`](../../scripts/mission_recipient_census.py). It is new. It imports `mission_coverage_gap.py` (and through it `mission_non_top50_numerator.py`, `mission_recipient_basis_eligibility.py` and `mission_daf_share_recipient_revenue.py`) and modifies none of them.
- Data: [`data/mission-2026-11-14/recipient-census-2026-11-20.csv`](../../data/mission-2026-11-14/recipient-census-2026-11-20.csv). It has 4,039 rows: 128 estimate, 24 se_component, 107 stratum and 3,780 recipient rows. The data dictionary is in §5.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b40n1202-04.csv`](../../data/mission-2026-11-14/queue-proposals-b40n1202-04.csv) (5 rows).

Tags: [F] computed from filings by the script · [I] inference or method choice.

## 0. Answer in brief

**Headline: committed frame, central bounded allocation (`rw_capall_s10_ni50`), pooled [F]**

| Basis | Sample | EINs sampled | Respondents | Pooled share | 95% CI (repo bootstrap) | SE, repo bootstrap | 95% CI, census strata fixed | SE, census strata fixed |
|---|---|---|---|---|---|---|---|---|
| 1h | old (committed) | 2,352 | 2,170 | **9.16%** | 8.30–10.15%¹ | 0.495 pt | 8.34–10.03% | 0.413 pt |
| 1h | **new (enlarged)** | 6,132 | 5,699 | **8.81%** | 7.94–9.70% | 0.475 pt | 8.21–9.41% | 0.303 pt |
| 1h − 1d − 1e | old (committed) | 2,352 | 2,145 | **13.71%** | 12.26–15.22%¹ | 0.761 pt | 12.59–14.83% | 0.576 pt |
| 1h − 1d − 1e | **new (enlarged)** | 6,132 | 5,609 | **13.58%** | 12.24–14.97% | 0.726 pt | 12.69–14.52% | 0.463 pt |

¹ This is the committed run reproduced with its own bootstrap seed. The point estimates and CIs match b40n120201-01 (9.2%, 8.3–10.2%; 13.7%, 12.3–15.2%). The SE columns use a fresh 500-replicate bootstrap (seed 20261119 + 7 × basis index). Its percentile CI for the old sample is 8.21–10.21% and 12.29–15.16%.

- **The point estimates move down, inside the old intervals [F].** 1h goes from 9.16% to 8.81% (−0.35 points). 1h − 1d − 1e goes from 13.71% to 13.58% (−0.14 points). The measured floor moves the same way: 8.39% to 8.08% on 1h, and 12.56% to 12.45% on 1h − 1d − 1e.
- **Change in standard error [F].**
  - *Repo method* (with-replacement bootstrap within every stratum, as in `rbe.boot`): 1h falls from 0.495 to 0.475 points (−0.020; ratio 0.96). 1h − 1d − 1e falls from 0.761 to 0.726 (−0.036; ratio 0.95).
  - *Census strata held fixed* (every stratum whose whole membership is sampled, including the certainty 400, gets no sampling variance): 1h falls from 0.413 to 0.303 points (ratio 0.73, −27%). 1h − 1d − 1e falls from 0.576 to 0.463 (ratio 0.80, −20%).
  - The repo method barely registers the census, because it resamples a complete stratum as if it were a sample [I]. The census-fixed figure is the right measure of what the census bought (§2.2).
- **Expanded frame (adds recipients with only non-top-50 grants) [F].** 1h goes from 8.05% (7.21–9.00%) to 7.81% (6.99–8.69%), with SE 0.453 → 0.429 (census-fixed 0.343 → 0.283). 1h − 1d − 1e goes from 13.23% to 13.12% (11.99–14.45%), with SE 0.727 → 0.659 (census-fixed 0.551 → 0.459).
- **The thin strata get much tighter, but most of their members are out of scope [F].**
  - no_ntee <$1m: in-scope respondents go from 4 to 33 of 190, and the stratum's pooled 1h share (central) from 15.8% (10.2–38.1%) to 11.9% (9.3–15.4%), SE 6.1 → 1.6 points.
  - religion <$1m: in-scope respondents go from 15 to 56 of 190, and the share from 33.8% (11.8–86.7%) to 28.8% (14.7–45.3%), SE 19.6 → 8.0 points.
  - 228 of the 300 supplementary EINs have no FY2023–24 990 or 990-EZ in the IRS TEOS index.
- **The ≥$25m bands [F].**
  - The $25–100m band (central, 1h) goes from 7.83% (7.07–8.79%) to 8.02% (7.65–8.48%), SE 0.46 → 0.22 points (census-fixed 0.13).
  - The ≥$100m band goes from 4.67% (3.84–5.66%) to **4.17%** (3.49–5.12%).
  - On 1h − 1d − 1e, $25–100m goes from 13.75% to 13.71% and ≥$100m from 7.39% to 7.22%.
- **Recommendation [I].** Report 8.8% (95% CI 7.9–9.7%; census-corrected 8.2–9.4%) on 1h and 13.6% (12.2–15.0%; 12.7–14.5%) on 1h − 1d − 1e for the committed frame. Keep 9.2% / 13.7% as the 2,352-EIN result. The remaining sampling variance is in the <$25m bands, not in the large recipients (§2.3), so a further gain needs more small and mid-size EINs (queue P-B40N120204-02).

## 1. Method

### 1.1 What is reused unchanged
The script rebuilds exactly what `mission_coverage_gap.main` builds, by calling that module's functions and the functions it imports, from caches only:
- the sponsor universe, return choice and Schedule I lines (`rcp/lines`, `q120201/lines`);
- DAF weights (`weight_fallback`), the re-weighted w2 and the decomposition B (`q12011/p9` Part IX cache);
- the gap split, line keys and the central allocation `rw_capall_s10_ni50` (`cg.allocations`, `cg.alloc_num`);
- the BMF frame and exclusions, and the committed sample: certainty 400 plus up to 40 per NTEE major group × BMF revenue band (`base.draw_sample`, seed 20261119);
- the new-only supplementary sample (seed 20261120, 100 + 30 per stratum);
- IRS TEOS index lookup and return choice (`base.load_index`, `base.choose_filings`);
- the streamed Part VIII reader (`rbe.fetch_part8` / `rbe.parse_part8`, which stops after the main form);
- per-recipient rows (`rbe.recipient_a` via `cg.scenario_rows`);
- weights N_h / (n_h − xml_not_read) (`rbe.weights_a`);
- the pooled estimator (`rbe.pooled`).

The old headline is reproduced to the reported precision (§0, note 1) before anything is added [F].

### 1.2 What is added
- **(a) Thin-stratum supplements.** For each of `no_ntee|a_lt_1m` (N_h = 26,777) and `religion|a_lt_1m` (N_h = 16,073), the script draws a simple random sample of 150 from the stratum members not already sampled, with `random.Random(20261120 + i)` (i = 0, 1 in that order) over EIN-sorted members.
  - The union of an SRS of 40 and an SRS of 150 from the remainder is an SRS of 190 [I].
  - So the stratum keeps its key and N_h, and its weight becomes N_h / (190 − unreadable): 140.9 and 84.6, against 669.4 and 401.8 before [F].
- **(b) Census of recipients with BMF revenue of $25m or more.** The committed frame has **4,458** recipients with BMF REVENUE_AMT ≥ $25m (revenue bands d and e) [F].
  - 282 are in the certainty stratum and keep that place.
  - 696 were already in the old SRS.
  - The other **3,480** are added, so every group × d/e stratum is complete. Each such stratum now has weight 1, or N_h / (N_h − 1) where one return could not be read [F].
- **Recipient returns.** The enlarged sample needs 13,588 FY2023–24 returns (old 6,518; added 7,070).
  - Old caches (`q1226/f990p8`, `q120201/f990p8`) held 6,518. The script fetched 7,070 from the GivingTuesday mirror of IRS TEOS into a new cache (`b40n120204/f990p8`).
  - All 13,588 statuses: 13,573 `ok`, 7 `parse_error`, 8 `http_404` [F].
  - The added census recipients matched 6,899 returns, the supplements 134.
- **Numerators.** The central allocation and the measured floor are computed for every unit with the same functions as the committed run. Added units therefore get the same treatment as sampled ones.

### 1.3 Standard errors
- **Bootstrap.** For each estimate the script draws 500 stratified bootstrap replicates of the pooled share, resampling respondents with replacement within stratum as `rbe.boot` does. The SE is the replicate SD and the CI the 2.5th–97.5th percentiles. Seed: 20261119 + 7 × basis index, the same for old and new.
- **Two variants.**
  - `repo`: every stratum is resampled (the committed method).
  - `fpc0`: strata sampled in full are held fixed. These are the certainty stratum, the ≥$25m census strata in the new sample, and small strata with N_h ≤ 40 in both samples. A complete stratum has no sampling variance; other strata keep with-replacement resampling and no finite-population correction [I].
- **Variance location (`se_component` rows).** These give the repo-method SE when only one block of strata is resampled and all others are held fixed. The blocks are the certainty stratum and each revenue band's non-certainty strata.

## 2. Results

### 2.1 Headline and frames
See §0. The CSV `estimate` rows hold all of these combinations:
- old and new samples;
- the central and floor scenarios;
- the committed and expanded frames;
- both bases;
- the overall scope, each revenue band and the two thin strata.

### 2.2 Why the repo-method SE barely moves
- **Large recipients carry little of the variance [F].** In the old sample, the repo-method SE from resampling only one block (central, 1h) is 0.283 points for the certainty stratum, 0.227 for $1–5m, 0.191 for <$1m, 0.191 for $5–25m, 0.175 for ≥$100m and 0.115 for $25–100m.
- **What the census changes [F].** After the census, $25–100m falls to 0.038 and ≥$100m stays at 0.187. Under the repo method, a complete stratum is still resampled with replacement, so a census of heterogeneous large recipients still shows variance there.
- **What removes it [F].** Holding complete strata fixed removes the certainty term and the ≥$25m terms entirely. That is why the census-fixed SE falls by 27% on 1h, while the repo SE falls by 4%.

### 2.3 Where the remaining variance sits (new sample, central)

| Block resampled alone | SE 1h, old | SE 1h, new | SE 1h−1d−1e, old | SE 1h−1d−1e, new |
|---|---|---|---|---|
| certainty | 0.283 | 0.263 | 0.457 | 0.441 |
| <$1m | 0.191 | 0.165 | 0.279 | 0.254 |
| $1–5m | 0.227 | 0.215 | 0.319 | 0.310 |
| $5–25m | 0.191 | 0.180 | 0.274 | 0.266 |
| $25–100m | 0.115 | 0.038 | 0.149 | 0.056 |
| ≥$100m | 0.175 | 0.187 | 0.352 | 0.248 |

Points of share, repo-method bootstrap [F].
- **Why the certainty and ≥$100m rows do not fall.** Both blocks are complete in the new sample, so under `fpc0` they contribute nothing.
- **What is left.** The census-fixed remainder (about 0.30 points on 1h) is almost all in the <$1m, $1–5m and $5–25m bands. Their squared contributions sum to roughly 0.32 points [F].
- **Small changes to untouched strata.** The $1–5m and $5–25m rows change slightly between samples because the overall pooled ratio changed, even though those strata were not touched.

### 2.4 Strata
- **No-NTEE <$1m [F].** Of the 150 supplementary EINs, 29 were in scope with a usable return and 121 had no FY2023–24 990 or 990-EZ in the index. The stratum floor share is 9.0% (old, 4 respondents) and 8.5% (new, 33).
- **Religion <$1m [F].** Of the 150, 41 were in scope, 107 had no 990 or 990-EZ, one had no contributions line and one had zero contributions. The floor share is 28.8% (old, 15 respondents) and 25.9% (new, 56). The two thin strata together move the <$1m band (central, 1h) from 23.3% to 22.3%, with SE 4.19 → 3.62 points.
- **Census strata [F].**
  - The largest single-stratum move is health ≥$100m: the floor 1h share goes from 2.21% (39 respondents of 40) to 0.75% (142 of 144).
  - Human services $25–100m goes from 2.42% to 2.96% (1,139 respondents), and education $25–100m from 6.94% to 7.41% (636).
  - Of the 3,480 added census recipients, 3,459 were `ok`, 12 had no contributions line, 3 had zero or negative contributions, 5 had no FY2023–24 990 or 990-EZ and 1 return could not be read.

## 3. Limits
- **Out of scope is not missing [I].** Most EINs in the two thin strata (81% of no-NTEE and 71% of religion supplements) file no 990 or 990-EZ: they are congregations or 990-N filers. The 1h share is undefined for them, and the weights keep them in n_h as out of scope. The thin-stratum shares describe only filers. The larger supplement improves precision but cannot fix that scope (queue P-B40N120204-03).
- **Census by BMF revenue, not filed revenue.** The census band uses the current BMF REVENUE_AMT, as the committed strata do. Recipients whose FY2023–24 filed revenue was ≥$25m but whose BMF figure is lower are not in the census.
- **Bootstrap.**
  - Neither variant applies a finite-population correction to partially sampled strata, so both overstate variance slightly where n_h/N_h is large.
  - With-replacement resampling of strata with very few respondents (e.g. the old no-NTEE <$1m with 4) gives unstable intervals.
  - 500 replicates leave Monte Carlo error of roughly 3% in each SE [I].
- **Allocation and coverage are unchanged.** Only sampling precision changes. The allocation envelope from b40n120201-01 (about ±0.3 points on 1h) and every frame and numerator assumption still apply, and the new CIs do not include them.
- **Unreadable returns.** 7 parse errors and 8 HTTP 404s at the mirror were not re-fetched from the IRS bulk zips. Only one affects a census recipient (status `xml_not_read`, health ≥$100m). It is treated as missing at random within its stratum, as in the committed method.
- **Reproducibility.** Two cache-only runs produced byte-identical CSVs (md5 `4798a3af…`) (§6).

## 4. Interpretation [I]
- **The direction.** The enlarged sample lowers the headline a little. The census replaces a 40-EIN sample in each large stratum with the full stratum, and in the ≥$100m band the full strata have lower DAF reliance than the sampled 40, notably in health.
- **The size.** The move (−0.35 points on 1h) is about 0.7 old SEs, which is consistent with sampling noise in the old estimate.
- **The 1h − 1d − 1e basis** moves less (−0.14). The script does not decompose why. One candidate is that the census strata whose shares fell most (health ≥$100m) carry large line 1d/1e amounts, so their fall weighs less on the narrower denominator; this is untested.

## 5. Data dictionary (`recipient-census-2026-11-20.csv`)

| Column | Meaning |
|---|---|
| row_type | `estimate` (pooled share for one sample × scenario × frame × basis × scope), `se_component` (SE with only one block resampled), `stratum` (per-stratum design and shares), `recipient` (one row per added EIN) |
| sample | `old` = committed 2,352 + 1,272 new-only EINs; `new` = old + 300 supplementary + 3,480 census EINs |
| scenario | `rw_capall_s10_ni50` (central bounded allocation, b40n120201-01) or `measured_floor` (no gap allocated) |
| frame | `committed` (recipients with top-50 grants) or `expanded` (adds new-only recipients) |
| basis | `b1_1h` = Form 990 Part VIII line 1h (990-EZ line 1); `b3_1abcf` = 1a + 1b + 1c + 1f = 1h − 1d − 1e |
| scope | `all_ex_excluded`, `revenue_band=<band>`, `stratum=<group|band>`, `resampled_only=<block>` (se_component), or the stratum key (stratum rows) |
| sampled, respondents | EINs in scope of the estimate; respondents with status ok and a positive denominator |
| pooled_share | Σ w × numerator / Σ w × denominator (rbe.pooled), as a fraction |
| ci95_lo, ci95_hi, se_boot | 2.5th / 97.5th percentile and SD of 500 stratified bootstrap replicates, every stratum resampled (central; floor overall only) |
| ci95_lo_fpc0, ci95_hi_fpc0, se_boot_fpc0 | the same with complete strata held fixed |
| complete_strata | number of strata in scope sampled in full |
| se_change, se_ratio | new minus old se_boot, and new / old (new rows only) |
| stratum_N | N_h, frame members in the stratum (certainty: 400) |
| sampled_old / sampled_new, respondents_old / respondents_new | per-stratum counts |
| out_of_scope_new, xml_not_read_new | new-sample EINs with no usable FY2023–24 return (out of scope) / with a return that could not be read |
| weight_old, weight_new | N_h / (n_h − xml_not_read) |
| pooled_b1_1h_old … pooled_b3_1abcf_new | per-stratum pooled floor share by basis and sample |
| ein, name, ntee_cd, ntee_major_group, revenue_band, bmf_revenue_amt | recipient identity and BMF classification (EO BMF eo1–eo4) |
| stratum, added | stratum key; `supp_a` (thin-stratum supplement) or `census_b` (≥$25m census) |
| years_matched, forms, object_ids | fiscal years with a usable return, form types, IRS TEOS object IDs |
| num_daf_weighted_central, num_daf_weighted_floor | FY2023–24 DAF-weighted numerator over matched years (USD), central allocation / floor |
| den_b1_1h, den_b3_1abcf | denominators over matched years (USD) |
| share_b1_1h, share_b3_1abcf | per-recipient central share (blank unless status ok) |
| status | `ok`, `no_fy2023_2024_990_or_ez_in_index`, `no_contributions_line`, `zero_or_negative_contributions`, `xml_not_read` |
| source | source statement |

## 6. Reproduction and robots log
```
S=<scratchpad>
python3 scripts/mission_recipient_census.py . --np-cache $S/npcache --lines-cache-top50 $S/rcp/lines \
    --lines-cache $S/q120201/lines --bmf-dir $S/rcp/bmf --index-dir $S/irs --p8-cache $S/q1226/f990p8 \
    --p8-cache-mid $S/q120201/f990p8 --p8-cache-new $S/b40n120204/f990p8 --p9-cache $S/q12011/p9 [--fetch] [--boot 500]
```
- **Fetch run.** `--fetch --fetch-only` read 7,070 recipient returns in under ten minutes (12 workers).
- **Cache-only run.** A cache-only run takes about 4 minutes. stdout is a JSON diagnostic: counts, statuses, the committed-run reproduction, SE components and headline.
- **Robots.**
  - `gt990datalake-rawdata.s3.amazonaws.com/robots.txt` returned HTTP 404 on 2026-11-20T04:46:53Z, so it has no rules for any agent, including ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot. It was logged in `b40n120204/robots/log.tsv`.
  - The IRS TEOS index files and EO BMF were read from the existing local cache, not fetched.
  - sec.gov and the IRS bulk zips were not used. The user agent was `research-script/1.0`.

## 7. Source register
| Source | URL | Used for |
|---|---|---|
| GivingTuesday 990 data lake (mirror of IRS TEOS e-file XML) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml | Recipient Form 990 Part VIII lines 1a–1h and 990-EZ line 1, FY2023–24 (13,588 returns) |
| IRS TEOS e-file index | https://apps.irs.gov/pub/epostcard/990/xml/2023/index_2023.csv (and 2024–2026) | Locating each recipient's FY2023–24 returns (local cache) |
| IRS Exempt Organizations Business Master File | https://www.irs.gov/pub/irs-soi/eo1.csv … eo4.csv | Frame, NTEE major group, REVENUE_AMT bands, exclusions (local cache) |
| Committed numerator, allocation and samples | [b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md); [coverage-gap-decomposition-2026-11-20.csv](../../data/mission-2026-11-14/coverage-gap-decomposition-2026-11-20.csv) | Old headline (9.2% / 13.7%) and its reproduction |
| Committed share CSV | [daf-share-of-recipient-revenue-2026-11-19.csv](../../data/mission-2026-11-14/daf-share-of-recipient-revenue-2026-11-19.csv) | Thin-strata starting counts (no_ntee <$1m 4 of 40; religion <$1m 15 of 40) |
| DAFRC 2025 panel and corrections | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx; [dafrc-corrections-itemized.csv](../../data/mission-2026-11-14/dafrc-corrections-itemized.csv) | Sponsor panel, netted denominator for the allocation (via the reused modules) |
