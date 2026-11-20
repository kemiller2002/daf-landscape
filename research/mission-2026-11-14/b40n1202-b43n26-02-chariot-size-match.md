# Size-matching Chariot's participants on contributions, not on BMF revenue (P-B40N1202-B43N26-02)

**Date:** 2026-11-20 · **Task ID:** b40n1202-b43n26-02 · **Builds on:** [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md) §2.2 and §3, [b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md) and [b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md)

**Outputs**
- Script: [`scripts/mission_chariot_size_match.py`](../../scripts/mission_chariot_size_match.py). It is new. It imports `mission_coverage_gap.py`, and through it the committed recipient-share modules, and modifies nothing. It reads caches only and makes no network calls.
- Data: [`data/mission-2026-11-14/chariot-size-match-2026-11-20.csv`](../../data/mission-2026-11-14/chariot-size-match-2026-11-20.csv). 407 rows: 7 `chariot_band`, 180 `summary` and 220 `recipient`. The data dictionary is in §6.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b40n1202-b43n26-02.csv`](../../data/mission-2026-11-14/queue-proposals-b40n1202-b43n26-02.csv) (5 rows).

Tags: [F] computed from filings by the script · [P] quoted primary source · [I] inference or assumption.

## 0. Answer in brief

- **The band [P/I].** Chariot's 2026 report "analyzed $26.1 billion in total giving across 54 participating nonprofits" [P]. It covers 2021–2025 ("across all five years in this study") [P]. That gives $26.1bn ÷ 54 ÷ 5 = **$96.7m per participant-year**, but only if every participant contributed all five years [I].
  - The $50m–$200m band is 0.52× to 2.07× that mean. Its geometric centre is $100m, so the band is centred on the mean. It holds up.
  - If participants averaged 4 years of data the mean is $120.8m; at 3 years it is $161.1m. Both still fall in the band [I].
- **The size-matched result.** Recipients whose own FY2023–24 1h − 1d − 1e averages $50m–$200m a year: 220 respondents, 115 of them certainty units, about 358 frame recipients after weighting [F]. These figures are on the committed frame, with 1,000 bootstrap replicates; the domain is applied after each resample.

  | Numerator | Pooled, 1h − 1d − 1e | Median, 1h − 1d − 1e | Pooled, 1h | Median, 1h |
  |---|---|---|---|---|
  | **Central (b40n120201-01 allocation)** | **10.0% (8.2–12.1%)** | **5.8% (3.4–6.8%)** | **8.1% (6.6–10.0%)** | 5.0% (2.5–6.3%) |
  | Envelope low / high | 9.9% / 10.3% | 5.7% / 6.0% | 8.0% / 8.3% | 4.9% / 5.2% |
  | All-panel measured floor | 9.5% (7.7–11.4%) | 5.4% | 7.6% (6.2–9.4%) | 4.7% |
  | Top-50 unscaled (committed study basis) | 8.1% (6.5–9.9%) | 4.5% | 6.6% (5.2–8.2%) | 3.6% |

- **Against the repo's current all-recipient figures** [F]:
  - The run reproduces those figures exactly: central 9.16% on 1h and 13.71% on 1h − 1d − 1e.
  - Size-matched recipients sit **3.7 points lower on 1h − 1d − 1e** (10.0% against 13.7%) and **1.1 points lower on 1h** (8.1% against 9.2%).
  - The size-matched median (5.8%) is less than half the all-recipient median (14.2%).
- **Against Chariot's 12.6%** [F/I]:
  - On the central numerator, the size-matched pooled share is **2.6 points below Chariot**. The bootstrap interval of the gap is 0.6–4.4 points, so the interval for the share (8.2–12.1%) **excludes** 12.6%, though only just. The interval reflects recipient sampling only. It resamples the 400-unit certainty stratum as if it were a sample, which widens it (holding certainty units fixed gives 8.9–11.5%), and it carries no numerator-allocation, definition or period uncertainty. [V wave 44A]
  - Across the allocation envelope (9.9–10.3%) the gap stays between 2.3 and 2.8 points.
- **Does the repo's Chariot comparison change? Yes** [I]:
  - **What the repo says now.** In b40n1202-b43n26 §0 and §3, Chariot's 12.6% "sits inside the unscaled-to-scaled range for the $25–100m band and for all recipients, and above the ≥$100m range". Its size-matched figures are $25–100m at 11.0% unscaled and 16.4% scaled, and ≥$100m at 5.8% and 8.7%.
  - **What changes.** Matching on the recipient's own contributions removes the bracketing. With the central numerator in place of 1/0.6727 scaling, the filings sit **below Chariot, not around it**.
  - **Why the old match bracketed.** The BMF band $25–100m on the same numerator and basis is 13.7%, because that band picks up government-funded organisations whose contributions are much smaller than their revenue. The legacy 1/0.6727 scaling of the size-matched top-50 figure gives 12.1%. That number is superseded by the central allocation, but it explains why earlier readings looked consistent with Chariot.
  - **Proposed wording:** "Size-matched on contributions (own 1h − 1d − 1e of $50m–$200m a year), the filings give a pooled DAF share of 10.0% (8.2–12.1%) and a median of 5.8%, against Chariot's pooled 12.6%. The remaining gap of about 2.6 points (0.6–4.4) is consistent with selection of DAFpay-using participants, with numerator definition or with the period difference; denominator choice does not explain it, and size matching on contributions does not close it. The 0.6–4.4 range is a sampling interval only. [V wave 44A]"
- **Selection signal [F/I].** Two organisations the Chariot webinar names in the study are in the size-matched domain, and both sit above 12.6% on central filing shares:
  - ACLU Foundation: 35.2% of 1h − 1d − 1e, average $176.6m a year;
  - Share Our Strength (No Kid Hungry): 18.0%, average $78.9m a year.

  The webinar names ACLU, not specifically the Foundation EIN, so this is an illustration and not a match.

## 1. Method

### 1.1 Re-deriving the band
- **Inputs, quoted [P].** "$26.1 billion in total giving across 54 participating nonprofits and represented $3.3 billion in DAF revenue". Growth runs "from 2021 to 2025", and a presenter speaks of "all five years in this study" (Chariot webinar page, fetched 2026-11-20).
- **Arithmetic [I].**
  - 26.1e9 / 54 / 5 = 96,666,667.
  - 3.3 / 26.1 = 12.64%.
  - Band edges ÷ mean: 0.517 and 2.069.
  - `chariot_band` rows in the CSV.
- **Assumptions [I].**
  - The $26.1bn spans all five years and the participant panel is balanced; the page says neither. Read as one year, it is $483m per participant, where the ≥$200m band gives 7.3%, further below Chariot. [V wave 44A]
  - "Total giving" in a CRM is close to Form 990 1h − 1d − 1e. Both exclude government grants. CRM totals may book pledges and affiliate gifts differently.
  - The page also calls the same ratio "nearly 13% of total revenue" [P]. The repo reads it as total giving, following NPB001–002.

### 1.2 Domain
- **Size variable.** For each sampled recipient, the size variable is `avg_b3` = (sum of 1a + 1b + 1c + 1f, or 990-EZ line 1, over its matched FY2023/2024 returns) ÷ (number of matched years). The returns and lines are exactly those used by b40n1202-b43n26 and b40n120201-01 (cache `q1226/f990p8`).
- **Headline domain.** `chariot_b3avg_50m_200m`: $50m ≤ avg_b3 < $200m.
- **Sensitivities.**
  - narrower ($75–125m) and half-to-double ($48.3–193.3m) bands;
  - ≥$50m, $25–100m, ≥$100m and ≥$200m;
  - matching on own 1h instead (`b1avg_50m_200m`);
  - the committed BMF REVENUE_AMT bands, for contrast;
  - the headline band excluding NTEE T and fund, foundation or trust names (the repo's intermediary screen), excluding leaked DAF-sponsor names, and 990-only.
- **Frames.** The committed frame is the main one. The expanded frame (adding recipients of non-top-50 grants only) is a sensitivity, run for the central numerator only.

### 1.3 Numerators (all from `mission_coverage_gap.py` state, caches only)
| Name | Definition | Repo all-recipient value (1h / 1h − 1d − 1e) |
|---|---|---|
| top50_unscaled | Top-50 DAFRC sponsors, Schedule I FY2023–24, net of DAF-to-DAF, DAF-weighted | 6.9% / 10.3% |
| all_panel_floor | Every itemising DAFRC panel sponsor (`measured_floor`) | 8.4% / 12.6% |
| **central** | `rw_capall_s10_ni50`: re-based weight w2 plus bounded allocation of the coverage gap | **9.2% / 13.7%** |
| env_low | `only_non_itemising_top50` (sub-$5,000 component dropped) | 8.8% / 13.2% |
| env_high | `sens_plus_d2d_residual_all` (DAF-to-DAF residual also allocated) | 9.4% / 14.05% |

The run reproduces every value in the right-hand column to the reported precision [F] (`repo_reference_share` on the `all_recipients` rows).

### 1.4 Statistics
- **Point estimates.**
  - Stratum weights are N_h ÷ (n_h − unread), as `rbe.weights_a`.
  - The pooled share is Σw·num ÷ Σw·den over usable respondents in the domain.
  - The median is the weighted median of per-recipient shares (`base.wquantile`).
- **Bootstrap.** 1,000 replicates, seed 20261120.
  - Each stratum's full sample is resampled with replacement, and only then is the domain applied. The number of respondents in the domain therefore varies across replicates, which a domain estimate requires. The repo's `rbe.boot` instead resamples inside a fixed subset, which understates variance for a domain.
  - Weights are held fixed. The 2.5th and 97.5th percentiles are reported.
- **Influence.** A leave-one-out pass on the headline and all-recipient rows records the recipient whose removal moves the pooled share most.

### 1.5 Robots and network
- **givechariot.com.** Its robots.txt (fetched 2026-11-20) disallows only `/admin/*`, so the webinar page is allowed. It was fetched once with the generic user agent.
- **No other host was contacted.** The IRS index files, the GivingTuesday-mirror XML extracts, the BMF and the sponsor caches were all read from the scratchpad caches built by the earlier tasks.
- sec.gov was not used.

## 2. Results: all recipients (reproduction)

| Numerator | Basis | Respondents | Pooled (95% CI) | Median (95% CI) |
|---|---|---|---|---|
| central | 1h | 2,170 | 9.2% (8.3–10.1%) | 11.9% (10.5–13.4%) |
| central | 1h − 1d − 1e | 2,145 | 13.7% (12.3–15.2%) | 14.2% (12.9–15.9%) |
| all_panel_floor | 1h − 1d − 1e | 2,145 | 12.6% (11.3–14.0%) | 11.4% |
| top50_unscaled | 1h − 1d − 1e | 2,145 | 10.3% (9.2–11.7%) | 7.7% |

These match b40n120201-01 and b40n1202-b43n26 §2.1 [F]. The intervals differ in the third digit because the seed and the bootstrap design differ.

## 3. Results: size-matched

### 3.1 Headline domain ($50m ≤ own 1h − 1d − 1e average < $200m)
See the table in §0. Further points [F]:
- **Composition by BMF revenue band** (weighted recipients): 220.7 are ≥$100m and 133.7 are $25–100m. One respondent each falls in the <$1m band and three in the $5–25m band; their BMF revenue is stale or blank.
- **Composition by NTEE group:** public and societal benefit 42, international 39, human services 25, arts 25, education 23, no NTEE 23, environment 21, health 9, religion 6.
- **No 990-EZ filers** fall in the band, so `form990_only` is identical to the headline.
- **Expanded frame, central:** 9.8% (8.1–11.9%) on 1h − 1d − 1e; 6.2% on 1h.
- **Coverage scaling.** The legacy 1/0.6727 scaling of the top-50 figure gives 12.1% [I]. This is the number that previously sat on top of Chariot's 12.6%. The central allocation replaces it at 10.0%.

### 3.2 Sensitivities, central numerator, 1h − 1d − 1e (committed frame)

| Domain | Respondents | Pooled (95% CI) | Median (95% CI) |
|---|---|---|---|
| **Own 1h − 1d − 1e $50–200m (headline)** | **220** | **10.0% (8.2–12.1%)** | **5.8% (3.4–6.8%)** |
| · excluding intermediary names and NTEE T | 159 | 8.0% (6.4–9.8%) | 3.6% (2.3–5.8%) |
| · excluding leaked DAF-sponsor names | 218 | 10.0% (8.2–12.1%) | 5.8% |
| Own $75–125m | 83 | 9.9% (7.4–12.7%) | 7.1% (3.7–9.9%) |
| Own $48.3–193.3m (0.5–2× mean) | 225 | 10.2% (8.4–12.3%) | 6.0% |
| Own $25–100m | 337 | 12.9% (11.3–14.8%) | 6.9% |
| Own ≥$50m | 287 | 8.5% (6.5–11.4%) | 5.7% |
| Own ≥$100m | 146 | 7.5% (5.2–11.0%) | 3.6% |
| Own ≥$200m | 67 | 7.3% (4.4–12.2%) | 5.0% |
| Own 1h $50–200m | 287 | 10.6% (8.7–12.7%) | 6.5% |
| BMF revenue $50–200m (old variable) | 458 | 11.4% (9.7–13.4%) | 6.8% |
| BMF revenue $25–100m (old band) | 531 | 13.7% (12.3–15.7%) | 8.7% |
| BMF revenue ≥$100m (old band) | 421 | 7.4% (5.8–9.4%) | 5.9% |

**Reading [I].**
- Every bounded contribution band centred near the $96.7m mean ($50–200m, $75–125m, $48.3–193.3m) gives a pooled share of 9.9–10.2%, below 12.6%. Open-ended bands from $48m up give 7.3–8.5%. The $25–100m band, which also contains the mean, gives 12.9% (11.3–14.8%) and is the only one to reach Chariot’s level. [V wave 44A]
- Matching on BMF revenue instead pulls in organisations whose contributions are far below their revenue: the $50–200m BMF band has twice the respondents of the contribution band. That raises the pooled share on 1h − 1d − 1e and lowers it on 1h.

### 3.3 Influence and intermediaries
- **The 85 Fund.** It is the largest leave-one-out influence on the headline 1h − 1d − 1e share: removing it takes the central share from 10.0% to 9.6% [F]. Its central filing share exceeds 100% (106.6%): the DAF-weighted grants it was paid are larger than the 1h − 1d − 1e it reported, plausibly because of timing or booking differences [I]. Top-50 Schedule I grants alone, DAF-weighted, equal 100.1% of its two-year 1h − 1d − 1e ($311.8m against $311.6m), and the central allocation adds 6.5% on top. The numerator comes from sponsors’ returns for their own fiscal years and the denominator from the recipient’s, so a per-recipient share is not bounded at 100%. Capping every share at 100% moves the pooled figure from 10.04% to 10.01%. [V wave 44A]
- **Shares above 50%.** 10 of the 220 domain respondents exceed 50% [F]:
  - The 85 Fund 107%;
  - San Antonio Valley Ranch LLC 99%;
  - Our American Future Foundation 96%;
  - Bright Funds Foundation 70%;
  - 50CAN 61%;
  - Lucile Packard Foundation for Children's Health 61%;
  - Southern Environmental Law Center 58%;
  - Vital Strategies 54%;
  - Medical Debt Resolution 52%;
  - ACE Scholarships 51%.

  Hopewell Fund is at 44%. Several of these are re-granting or pass-through vehicles, not fundraising charities like Chariot's participants [I].
- **Effect of the intermediary screen.** The repo's screen drops 61 respondents and takes the share to 8.0% [F]. The screen is crude: it removes "foundation"-named university and hospital foundations too (queue P-B40N1202-B43N2602-03).
- **On 1h** the largest influence is Action for Boston Community Development, a government-funded organisation; removing it raises the share from 8.1% to 8.5%.

### 3.4 Named Chariot participants in the domain (illustration only)
The webinar names the ACLU and No Kid Hungry as organisations in the study [P]. In the size-matched domain [F]:
- ACLU Foundation Inc: average 1h − 1d − 1e $176.6m; central share 35.2%.
- Share Our Strength (No Kid Hungry's parent): $78.9m; 18.0%.

Both exceed both the domain's pooled 10.0% and Chariot's 12.6%. This is consistent with Chariot's panel over-representing organisations that court DAF gifts, as DAFpay users do [I]. Two organisations prove nothing about the other 52.

## 4. Limits
- **Mean matching.** Chariot publishes only an aggregate; the size distribution of the 54 participants is unknown. A pooled share is dominated by the largest participants. If a few very large organisations make up most of the $26.1bn, the right comparison is nearer the ≥$100m or ≥$200m rows (7.3–7.5%), and the gap widens [I].
- **Balanced-panel assumption.** It is unverified. Unbalanced panels raise the mean per participant-year, still inside the band up to a 3-year average.
- **Period mismatch.** Chariot covers 2021–25 pooled. The filings cover FY2023–24. DAF shares rose over the period (Chariot's median DAF growth is +75% against +9%), so Chariot's pooled figure leans lower than its 2023–24 value would. Correcting for that would widen the gap [I].
- **Numerators differ.** CRM-coded DAF gifts from all sponsors on one side; Schedule I lines (≥$5,000 per recipient per sponsor) plus a modelled allocation of the coverage gap on the other. The central allocation's envelope is reported, but the allocation keys are assumptions (b40n120201-01).
- **Precision.** About half the domain is certainty units; the rest come from BMF-band strata of up to 40 draws, so domain intervals are about ±2 points. The domain bootstrap holds weights fixed.
- **Domain defined on the denominator.** Selecting on 1h − 1d − 1e can admit years with unusual one-off gifts. Averaging two years damps this but does not remove it.
- **Re-granting vehicles.** These are in the frame and inflate pooled shares; the name screen is a blunt tool.

## 5. What changes in the repo
- **b40n1202-b43n26 §0 and §3, Chariot row.** Replace the BMF-band size match ($25–100m 11.0% / 16.4%; ≥$100m 5.8% / 8.7%) with the contribution-matched central figure: 10.0% (8.2–12.1%) pooled and 5.8% median on 1h − 1d − 1e, 8.1% pooled on 1h.
  - Old conclusion: "Chariot's 12.6% sits inside the unscaled-to-scaled range for the $25–100m band and for all recipients".
  - New conclusion: "Chariot's 12.6% is above the size-matched filing estimate by about 2.6 points (0.6–4.4)".
- **The all-recipient central figures (9.2% / 13.7%) are unchanged.** They describe the whole frame, whose pooled share is dominated by recipients smaller than Chariot's participants. They should not be set beside Chariot's 12.6% as a like-for-like comparison.
- **NPB038 (median 12%, 20 organisations).** The size-matched median of 5.8% (3.4–6.8%) confirms the earlier reading that medians disagree most.

## 6. Data dictionary: `chariot-size-match-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_type | `chariot_band` (band arithmetic), `summary` (domain × numerator × basis), `recipient` (headline-domain members, committed frame) |
| frame | `committed` (b40n1202-b43n26 sample) or `expanded` (plus non-top-50-only supplementary sample; central only) |
| domain | Domain name (§1.2) |
| size_variable | `avg_b3` own (1h − 1d − 1e)/yr; `avg_b1` own 1h/yr; `bmf_rev` BMF REVENUE_AMT |
| size_lo_usd, size_hi_usd | Domain bounds, lower inclusive and upper exclusive; blank = unbounded |
| domain_filter | Extra filter: `not_intermediary`, `not_leaked`, `form990_only`; blank = none |
| numerator | top50_unscaled, all_panel_floor, central, env_low, env_high (§1.3) |
| basis | `b1_1h` = 1h; `b3_1abcf` = 1a + 1b + 1c + 1f = 1h − 1d − 1e (EZ line 1 on both) |
| respondents | Usable respondents (status ok, denominator > 0) in domain |
| certainty_respondents | Of which in the certainty stratum |
| weighted_recipients | Σ stratum weights (estimated frame recipients) |
| median_share, p25_share, p75_share | Weighted quantiles of per-recipient share |
| pooled_share | Σw·num ÷ Σw·den |
| *_ci95_lo / _hi | 2.5th and 97.5th percentiles of the domain bootstrap |
| boot_reps_used | Replicates with a defined estimate (of 1,000) |
| scaled_pooled_inference | top50_unscaled only: pooled ÷ 0.6727 (legacy scaling, [I]) |
| repo_reference_share | all_recipients rows: the repo figure being reproduced |
| chariot_pooled_share | 3.3 ÷ 26.1 (on b3 rows) |
| chariot_minus_pooled_pts | Chariot minus pooled share, percentage points |
| loo_max_ein, loo_max_name, loo_max_pooled_share | Leave-one-out: most influential recipient and the pooled share without it |
| ein, name, stratum, stratum_weight | Recipient identity and weight (recipient rows) |
| revenue_band_bmf, bmf_revenue_usd, ntee_major_group | BMF attributes |
| forms, years_matched | Matched FY2023/2024 returns |
| avg_1h_usd, avg_1h_less_1d_1e_usd | Own average per matched year |
| num_<numerator> | Numerator on matched years, USD |
| share_central_b1_1h, share_central_b3_1abcf, share_top50_b3_1abcf | Per-recipient shares |
| metric, value | chariot_band rows: giving_per_participant_year, pooled_daf_share, band ratios, per-participant-year at 4 or 3 average years |
| source | Provenance string |

## 7. Reproduction
```
S=<scratchpad>
python3 scripts/mission_chariot_size_match.py . --np-cache $S/npcache --lines-cache-top50 $S/rcp/lines \
    --lines-cache $S/q120201/lines --bmf-dir $S/rcp/bmf --index-dir $S/irs --p8-cache $S/q1226/f990p8 \
    --p8-cache-new $S/q120201/f990p8 --p9-cache $S/q12011/p9 --boot 1000
```
- The run is cache-only and takes several minutes; most of the time goes to rebuilding the numerators and to the 1,000-replicate bootstrap.
- The output CSV has md5 `fc2ad5b7…`.
- stdout is a JSON diagnostic: the band, headline cells, every domain under the central numerator, and the BMF-band profile of the headline domain.

## 8. Source register

| # | Source | URL | Used for |
|---|---|---|---|
| S1 | Chariot, "2026 DAF Fundraising Report" release webinar page (fetched 2026-11-20; robots.txt allows) | https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release | $26.1bn, 54 participants, $3.3bn, 2021–2025, "all five years", "nearly 13%"; ACLU and No Kid Hungry named |
| S2 | IRS Form 990 instructions, Part VIII lines 1a–1h | https://www.irs.gov/instructions/i990 | Line definitions (1f includes DAF grants) |
| S3 | IRS TEOS e-file index files | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (and 2023, 2025, 2026) | Return location (cached) |
| S4 | GivingTuesday mirror of IRS TEOS XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/ | Recipient Part VIII; sponsor Schedule I and Part IX (cached) |
| S5 | IRS Exempt Organizations Business Master File | https://www.irs.gov/pub/irs-soi/eo1.csv (eo1–eo4) | Revenue band, NTEE (cached) |
| S6 | Repo: b40n120201-01 coverage-gap decomposition | research/mission-2026-11-14/b40n120201-01-coverage-gap-decomposition.md | Central numerator and envelope |
| S7 | Repo: b40n1202-b43n26 recipient basis | research/mission-2026-11-14/b40n1202-b43n26-recipient-basis-and-rating-eligibility.md | Basis, sample, prior Chariot comparison |
| S8 | Repo: nonprofit benchmarks NPB001–002, NPB038 | data/mission-2026-11-14/nonprofit-daf-revenue-benchmarks-2021-2026.csv | Chariot figures as recorded |
