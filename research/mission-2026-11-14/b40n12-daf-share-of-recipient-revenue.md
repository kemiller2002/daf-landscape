# DAF share of recipient revenue: an independent estimate from Form 990 filings (P-B40N12-02)

**Date:** 2026-11-19 · **Queue item:** P-B40N12-02 (from [queue-proposals-batch40-n12.csv](../../data/mission-2026-11-14/queue-proposals-batch40-n12.csv)) · **Task ID:** b40n12-02

**Outputs**
- Script: [`scripts/mission_daf_share_recipient_revenue.py`](../../scripts/mission_daf_share_recipient_revenue.py)
- Data: [`data/mission-2026-11-14/daf-share-of-recipient-revenue-2026-11-19.csv`](../../data/mission-2026-11-14/daf-share-of-recipient-revenue-2026-11-19.csv). It holds 19 summary rows and 2,352 sampled-recipient rows. The data dictionary is in §6.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b40n12-02.csv`](../../data/mission-2026-11-14/queue-proposals-b40n12-02.csv) (P-B40N1202-01..05)

Tags: [F] computed from filings by the script · [P] quoted primary/vendor source · [I] inference.

## 0. Answer in brief

- **What it measures.** The numerator is DAF grants from the top-50 sponsors. The denominator is each recipient's own Form 990 Part VIII line 1h (total contributions), not total revenue: on total revenue the pooled share is 4.2% and the median 4.2%. Recipients that are universities, hospitals, foundations or DAFRC-panel DAF sponsors are excluded [V wave 33A]
  - Across the in-scope recipients, the **median recipient gets 5.9%** of its contributions from top-50 DAF grants (95% CI 5.3–7.4%). P25 is 2.2% and P75 is 16.5%. [F]
  - **Pooled, the share is 6.9%** (95% CI 6.1–7.8%). Pooled means total top-50 DAF dollars divided by total contributions across recipients. [F]
- **Size gradient.** The share falls steadily with recipient size:
  - <$1m revenue: median 10.1%, pooled 17.8%;
  - $1–5m: median 3.5%, pooled 9.5%;
  - $5–25m: median 3.2%, pooled 8.7%;
  - $25–100m: median 2.5%, pooled 6.3%;
  - ≥$100m: median 1.1%, pooled 3.7%. [F]
- **Sector spread is modest.** Pooled shares by NTEE major group run from 4.5% (no NTEE code) to 12.9% (public and societal benefit). Medians run from 4.2% (environment and animals) to 13.4% (religion; thin sample). [F]
- **Top-50 coverage.** The top-50 sponsors' non-DAF-to-DAF Schedule I grants (DAF-weighted) were **$39.29bn in FY2024. That is 67.3% of netted DAFRC FY2024 DAF grants** ($58.41bn) and 60.8% of the raw DAFRC total ($64.60bn). [F]
- **Scaled to all DAF grants [I].** Dividing by that coverage gives a pooled share of **≈10.2%**. Measured directly with every itemising panel sponsor instead, the pooled share is 8.4% (7.6–9.2%) on the same recipients and 7.3% (6.5–8.2%) with recipients that get only non-top-50 grants; both leave the 15.1% of netted grants that no itemised line reaches unassigned, so they are floors, and dividing the first by all-sponsor coverage (0.849) gives 9.9% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B] On a private-contributions denominator (1h less line 1e government grants), the scaled pooled share is **≈15.0%**. Both lean high, because the netted denominator includes Schedule F foreign grants, sub-$5,000 lines and grants to charities outside this frame. A median divided by coverage (≈8.8%) has no estimator behind it and is illustrative only [V wave 33A]
  - This is an inference. It assumes the other 32.7% of DAF grants reach recipients in the same proportions as top-50 grants.
- **Against Chariot's "nearly 13%".**
  - Unscaled, the independent figure is about half of Chariot's.
  - Scaled, it is in the same range: 10.2% of 1h, or 15.0% of private contributions.
  - Chariot's pages say "54 participating nonprofits" [P]; "large" is the repo's paraphrase, not a Chariot quote. Its $26.1bn of total giving over five years averages about $97m per participant-year [I]. For large recipients the filings give: ≥$100m pooled 3.7% (scaled 5.5% [I]; 8.4% [I] on the private basis), and $25–100m pooled 6.3% (scaled 9.3% [I]; 15.7% [I] on the private basis). The two private-basis figures bracket Chariot's 12.6% [V wave 33A]
- **Against Chariot's 4–24% sector range.** The filings give a narrower range: 4.5–12.9% pooled, or 6.7–19.1% scaled [I].
  - International, which Chariot puts highest at 23.7% [P], is among the lowest here: pooled 4.9%, scaled 7.2% [I]. Its median (8.9%) is above the all-sector median, however.

## 1. Method

### 1.1 Numerator: top-50 DAF grants by recipient EIN

The numerator reuses the repo machinery unchanged.

- **Universe and return choice.** Taken from `mission_daf_to_daf.py`: `top_n`, `pick_returns` and `FYS = (2023, 2024)`. The top 50 are DAFRC panel EINs ranked by FY2024 end-of-year DAF assets. The fiscal year is the calendar year in which the tax period ends.
- **Lines.** The Schedule I Part II line cache is read with `mission_recipient_sectors.load_lines`, the same cache used for the 94 itemising sponsor-years. Filer "totals" rows are dropped with `mission_exception_load.drop_totals_rows`.
- **DAF-to-DAF flag.** `mission_recipient_sectors.annotate` drops three kinds of line: lines to a whitelisted recipient EIN (`decision = include` in [`daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv)), self-lines, and blank-EIN lines whose name uniquely matches a whitelisted sponsor.
- **Two bases.**
  - `schedule_i`: all lines as filed.
  - `daf_weighted`: each sponsor-year's lines multiplied by its DAF share of grants from [`sponsor-cost-structure.csv`](../../data/mission-2026-11-14/sponsor-cost-structure.csv), capped at 1. All 94 sponsor-years have a share.
  - The headline uses `daf_weighted`, because community-foundation Schedule I lines include discretionary grants.
- **Result.** 170,569 recipient EINs have a positive FY2023–24 numerator: $77.64bn on the Schedule I basis and $73.68bn DAF-weighted. [F]

### 1.2 Frame and exclusions

Recipients are joined to the IRS EO BMF (`eo1–eo4`, `eo_pr`, `eo_xx`; Last-Modified 2026-11-09), giving `NTEE_CD`, `FOUNDATION`, `SUBSECTION` and `REVENUE_AMT`. Recipients are excluded in this order:

| Exclusion | Rule | EINs | FY2023–24 numerator (Schedule I) |
|---|---|---|---|
| Not in the BMF | No row in the EO BMF | 22,269 | $4.36bn |
| DAF sponsor | Any DAFRC 2025 panel EIN | 430 | $7.34bn |
| Not 501(c)(3) | BMF SUBSECTION ≠ 03 | 100 | $0.02bn |
| University | NTEE B40–B43 or B50, or name contains UNIVERSITY / UNIV / COLLEGE / REGENTS / INSTITUTE OF TECHNOLOGY | 3,428 | $7.86bn |
| Hospital | NTEE E20–E24, BMF FOUNDATION 12, or name contains HOSPITAL(S) / MEDICAL CENTER / HEALTH(CARE) SYSTEM | 1,874 | $2.38bn |
| Foundation | NTEE T20–T31 (private and public grantmaking foundations, community foundations), or BMF FOUNDATION 02/03/04 (private foundations) | 3,636 | $3.17bn |
| **Frame (kept)** | | **138,832** | **$52.51bn** |

### 1.3 Sample

Full coverage would have meant about 280,000 returns, so a stratified random sample was drawn with a fixed seed.

- **Certainty stratum.** The 400 largest frame recipients by FY2023–24 numerator. Each received at least $14.68m, and together they hold 31.5% of frame numerator dollars. [F]
- **Random strata.** For everyone else, a simple random sample of up to 40 EINs in each of 54 strata (NTEE major group × BMF revenue band), drawn with `random.Random(20261119)`. Strata with 40 or fewer members are taken whole.
- **Total sampled:** 2,352 EINs.

### 1.4 Denominator: recipients' own returns

- **Locating returns.** The IRS TEOS e-file index (`index_2023`–`index_2026.csv`; already in the scratchpad, downloaded 2026-11-14) gives each sampled EIN's 990 or 990-EZ returns. Per tax period, the latest object id is kept, so amendments supersede. Per fiscal year (tax period ending in 2023 or 2024), the latest period is kept.
- **Reading returns.** Each return's XML is streamed from the GivingTuesday mirror of IRS TEOS (`gt990datalake-rawdata.s3.amazonaws.com`), and reading stops at the end of the main form. The fields kept are:
  - `TotalContributionsAmt`: Form 990 Part VIII line 1h, the denominator;
  - `ContributionsGiftsGrantsEtcAmt`: 990-EZ line 1, the denominator for EZ filers;
  - `GovernmentGrantsAmt`: line 1e;
  - `CYTotalRevenueAmt` or `TotalRevenueAmt`: total revenue.
- **Fetch results.** 4,315 returns were requested: 4,313 parsed, 1 was missing from the mirror (HTTP 404) and 1 failed to parse. [F]
- **Per-recipient share.** The sum of the numerator over the fiscal years that have a readable return, divided by the sum of the denominator over the same years.
  - Both years matched for 2,102 in-scope respondents and one year for 68. Form mix: 2,008 used two 990s, 71 two 990-EZs, 23 one of each, 49 a single 990 and 19 a single 990-EZ. [F]

### 1.5 Weights, statistics, scaling

- **Weights.** Each respondent's weight is N_h / (n_h − unreadable_h).
  - Some sampled EINs have no FY2023–24 990 or 990-EZ in the index: churches, 990-N filers and government units (169 EINs). Others reported zero contributions (4). Both groups are treated as **out of scope** for a line-1h share, not as missing. The weighted in-scope population is therefore about 96,228 recipients, against a frame of 138,832.
  - Nine EINs are treated as missing at random within their stratum. All 16 of their returns parsed but report no line 1h or EZ line 1, so they belong with the zero-contribution out-of-scope group. The effect on the estimates is negligible [V wave 33A]
- **Statistics.** Weighted P25, median and P75 of per-recipient shares. The pooled share is a combined ratio estimator: Σw·num / Σw·den.
- **Intervals.** 95% intervals come from a stratified bootstrap with 500 replicates, resampling within strata with weights held fixed.
- **Sensitivity variants:**
  - a capped pooled share (each numerator capped at its denominator);
  - a private-contributions denominator (1h − 1e);
  - non-certainty recipients only;
  - excluding NTEE T and names containing FOUNDATION / FUND / TRUST / FDN.
- **Scaling [I].** Coverage is FY2024 top-50 DAF-weighted non-DAF-to-DAF Schedule I ($39.29bn) divided by the netted DAFRC FY2024 DAF grants, central tier ($58.41bn, [`dafrc-market-totals-netted.csv`](../../data/mission-2026-11-14/dafrc-market-totals-netted.csv)). That gives 0.673; FY2023 is 0.685. `scaled_*` = share / 0.673.

Robots log: `q1202/robots/log.tsv` in the scratchpad, 2026-11-19.
- `gt990datalake-rawdata.s3.amazonaws.com` returned 404 for robots.txt, which places no restriction.
- `www.irs.gov` returned 200; the BMF and index were already cached.
- `projects.propublica.org` returned 200 but was not used.
- `apps.irs.gov` returned a 302 redirect; its index files were already cached and were not re-fetched.

## 2. Results

### 2.1 Full distribution table

The basis is `daf_weighted` and the denominator is line 1h, unless the column says otherwise. "Frame EINs" counts the frame before the out-of-scope adjustment. Scaled columns are **[I]**.

| Scope | Frame EINs | Sampled / in-scope respondents | P25 | Median (95% CI) | P75 | Pooled (95% CI) | Pooled, capped | Pooled, private contrib. (1h−1e) | Weighted share ≥20% | Weighted share >100% | Scaled pooled [I] | Scaled median [I] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **all_ex_excluded** | 138,832 | 2352 / 2170 | 2.2% | **5.9%** (5.3%–7.4%) | 16.5% | **6.9%** (6.1%–7.8%) | 6.8% | 10.1% | 20.4% | 2.8% | **10.2%** | **8.8%** |
| non_certainty_only | 138,432 | 1952 / 1807 | 2.2% | 5.9% (5.2%–7.5%) | 16.4% | 5.6% (4.9%–6.4%) | 5.5% | 8.5% | 20.2% | 2.8% | 8.3% | 8.8% |
| ex_ntee_T_and_fund_foundation_trust_names | 119,105 | 1906 / 1747 | 2.3% | 6.0% (5.3%–7.8%) | 16.4% | 5.9% (5.3%–6.6%) | 5.8% | 9.1% | 20.2% | 2.4% | 8.8% | 8.9% |
| arts_culture | 11,821 | 227 / 223 | 3.1% | 7.2% (4.7%–10.1%) | 17.7% | 8.1% (6.1%–10.1%) | 8.1% | 10.5% | 19.8% | 1.6% | 12.1% | 10.7% |
| education (ex universities) | 13,614 | 251 / 242 | 2.2% | 6.6% (4.6%–8.6%) | 19.0% | 6.9% (5.5%–8.9%) | 6.8% | 10.5% | 24.6% | 3.1% | 10.2% | 9.8% |
| environment_animals | 8,331 | 211 / 205 | 2.5% | 4.2% (3.6%–7.6%) | 17.0% | 10.2% (7.7%–13.2%) | 10.0% | 12.2% | 18.4% | 1.7% | 15.1% | 6.3% |
| health (ex hospitals) | 8,657 | 229 / 219 | 1.4% | 5.3% (3.6%–8.9%) | 16.3% | 6.9% (4.8%–9.8%) | 6.8% | 9.8% | 19.4% | 0.7% | 10.2% | 7.9% |
| human_services | 30,456 | 274 / 262 | 1.2% | 5.4% (4.3%–8.1%) | 14.8% | 5.7% (4.0%–7.7%) | 5.5% | 9.9% | 21.2% | 4.4% | 8.4% | 8.0% |
| international | 4,828 | 252 / 241 | 3.6% | 8.9% (5.3%–11.0%) | 19.0% | 4.9% (3.6%–6.3%) | 4.7% | 6.0% | 22.3% | 1.9% | 7.2% | 13.2% |
| public_societal_benefit | 8,924 | 268 / 263 | 2.6% | 6.9% (4.0%–10.7%) | 19.1% | 12.9% (9.8%–17.1%) | 12.8% | 17.9% | 24.9% | 3.2% | 19.1% | 10.2% |
| religion (990 filers only) | 17,957 | 194 / 146 | 2.7% | 13.4% (4.4%–16.6%) | 17.6% | 7.6% (4.4%–13.0%) | 6.6% | 8.0% | 24.7% | 5.1% | 11.4% | 19.9% |
| mutual_membership | 77 | 58 / 38 | 2.6% | 8.9% (5.0%–13.9%) | 18.2% | 6.5% (1.9%–9.2%) | 6.5% | 7.7% | 24.3% | 3.0% | 9.7% | 13.3% |
| unknown_z | 875 | 155 / 150 | 2.2% | 4.9% (3.6%–8.0%) | 12.6% | 6.5% (4.9%–8.3%) | 6.5% | 10.2% | 16.7% | 0.0% | 9.6% | 7.3% |
| no_ntee (BMF NTEE blank) | 33,292 | 233 / 181 | 1.5% | 4.3% (2.4%–5.9%) | 8.7% | 4.5% (3.3%–6.3%) | 4.5% | 7.8% | 7.2% | 0.0% | 6.7% | 6.3% |
| band <$1m | 94,042 | 482 / 321 | 3.9% | 10.1% (7.8%–13.3%) | 24.7% | 17.8% (11.3%–26.1%) | 16.4% | 21.0% | 27.7% | 4.5% | 26.4% | 15.0% |
| band $1–5m | 27,407 | 415 / 410 | 1.3% | 3.5% (2.9%–4.8%) | 10.6% | 9.5% (7.1%–12.2%) | 9.3% | 11.7% | 12.4% | 0.9% | 14.2% | 5.1% |
| band $5–25m | 12,925 | 477 / 471 | 0.7% | 3.2% (2.2%–4.2%) | 10.5% | 8.7% (6.9%–11.0%) | 8.6% | 12.2% | 12.4% | 0.8% | 12.9% | 4.8% |
| band $25–100m | 3,634 | 543 / 537 | 0.4% | 2.5% (2.1%–3.5%) | 7.5% | 6.3% (5.5%–7.1%) | 6.2% | 10.5% | 7.8% | 0.2% | 9.3% | 3.8% |
| band ≥$100m | 824 | 435 / 431 | 0.2% | 1.1% (0.7%–1.4%) | 4.5% | 3.7% (3.0%–4.7%) | 3.7% | 5.6% | 6.2% | 0.1% | 5.5% | 1.7% |

Scaled pooled shares on the private-contributions basis [I] are:
- all: 15.0%;
- by revenue band: <$1m 31.2%, $1–5m 17.3%, $5–25m 18.1%, $25–100m 15.7%, ≥$100m 8.4%;
- international: 8.9%; public and societal benefit: 26.6%.

These are in the `scaled_pooled_private_inference` column.

### 2.2 Reading the table

- **The pooled share exceeds the median.** A minority of recipients are heavily DAF-funded and pull the pooled figure up: 20.4% of in-scope recipients (weighted) get ≥20% of contributions from top-50 DAF grants. [F]
- **Size gradient.** Size is the main source of variation; sector differences are small and mostly inside overlapping intervals. For the median recipient, the share at ≥$100m is about a tenth of the share at <$1m (1.1% against 10.1%). [F]
  - The small band partly reflects selection. The frame contains only charities that received at least one itemised (>$5,000) top-50 grant, so a small charity in the frame has, by construction, a large DAF gift relative to its size.
- **Public and societal benefit (NTEE R–W) has the highest pooled share** (12.9%). The group includes fiscal sponsors and re-granting vehicles: S, T (other than foundations), U and W codes. Dropping NTEE T and fund/foundation/trust names lowers the all-recipient pooled share from 6.9% to 5.9%. [F]
- **Capping each recipient at 100% barely moves the pooled share** (6.9% → 6.8%), so over-100% outliers do not drive the estimate. [F]

### 2.3 Largest recipients in the certainty stratum

These figures are [F], from the CSV `stratum = certainty` rows. Numerators are DAF-weighted over the matched years.

| Recipient (NTEE) | Top-50 DAF grants, matched FYs | Line 1h, matched FYs | Share |
|---|---|---|---|
| Navigation Charitable Fund (U05), FY2023 only | $1,259.5m | $1,309.0m | 96.2% |
| New Venture Fund (C05) | $426.3m | $1,251.0m | 34.1% |
| Blue Meridian Partners (P12) | $362.5m | $470.2m | 77.1% |
| The 85 Fund (I01) | $311.8m | $311.6m | 100.1% |
| Climate Imperative Foundation (C12) | $232.7m | $472.1m | 49.3% |
| Médecins Sans Frontières USA (Q30) | $195.9m | $1,496.3m | 13.1% |
| ClimateWorks Foundation (U12) | $168.9m | $590.9m | 28.6% |
| UJA-Federation of New York (T70) | $159.1m | $633.4m | 25.1% |
| Hopewell Fund (T12) | $143.9m | $353.5m | 40.7% |
| Young Life (O55) | $133.4m | $847.1m | 15.8% |
| International Rescue Committee (Q71) | $130.4m | $2,791.7m | 4.7% |

The largest numerators belong to re-granting intermediaries. The Navigation Charitable Fund line is SVCF's single FY2023 Schedule I line of $1.309bn. It is filed as "Further Future Foundation" (EIN 921117448), and `mission_exception_load.py` also flags it. Proposal P-B40N1202-02 would classify these intermediaries properly.

### 2.4 Top-50 coverage of all DAF grants

| Item | FY2024 | FY2023 |
|---|---|---|
| Top-50 Schedule I, net of DAF-to-DAF (as filed) | $41.20bn | $36.87bn |
| … DAF-weighted | $39.29bn | $34.78bn |
| DAF-to-DAF lines dropped | $8.08bn | $4.65bn |
| DAFRC total DAF grants, raw | $64.60bn | $54.77bn |
| Netted DAFRC DAF grants, central tier | $58.41bn | $50.78bn |
| **Top-50 coverage (DAF-weighted / netted)** | **67.3%** | **68.5%** |
| Top-50 coverage (DAF-weighted / raw DAFRC) | 60.8% | — |

All figures are [F]. The coverage ratio also absorbs Schedule I's $5,000 itemisation threshold, because recipients under $5,000 from a given sponsor do not appear. On the raw DAFRC basis the scaling would be 1/0.608. That would raise the scaled pooled share to about 11.3% [I]: 6.9%/0.608, which is not a script output.

## 3. Comparison with vendor and sector claims

| Claim | Source | Basis | Independent counterpart (this note) |
|---|---|---|---|
| DAFs "nearly 13%" of total giving; $3.3bn of $26.1bn (12.6% derived), 2021–25 pooled, 54 large nonprofits [P] | Chariot/K2D 2026 ([webinar page](https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release); [report page](https://www.givechariot.com/resources/toolkits/daf-fundraising-report)); repo NPB001–002 in [direction-nonprofit-daf-benchmarks.md](direction-nonprofit-daf-benchmarks.md) | Vendor-run CRM gift files; self-selected large participants; denominator "total giving" | Pooled 6.9% of 1h unscaled and 10.2% scaled [I]. On a 1h−1e basis, 10.1% unscaled and 15.0% scaled [I]. Large recipients: $25–100m pooled 6.3% (scaled 9.3% [I]); ≥$100m pooled 3.7% (scaled 5.5% [I]; 8.4% [I] on 1h−1e). |
| Median DAF share 12% of 2023 giving (20 orgs; 12 of 20 at ≥10%, 6 of 20 at ≥20%) [S] | Chariot/K2D 2024 via [NonProfit Times](https://thenonprofittimes.com/npt_articles/daf-donors-making-their-presence-felt/) (repo NPB038–040) | Vendor sample | Median 5.9% unscaled, 8.8% scaled [I]. Of in-scope recipients, 20.4% are at ≥20%. |
| 15% for participants under $10m revenue (2024) [P] | [Chariot 2025 summary](https://www.givechariot.com/resources/insights/inside-the-2025-daf-fundraising-report-how-donor-advised-funds-are-transforming-philanthropy) (repo NPB024) | Vendor sample | <$1m pooled 17.8% and median 10.1%. $1–5m pooled 9.5% and median 3.5%. Bands are by BMF revenue, not identical to <$10m. |
| Sector range 4–24% of individual revenue; International Relief highest at 23.7% [P] | Chariot/K2D 2026 [report page](https://www.givechariot.com/resources/toolkits/daf-fundraising-report) (repo NPB019–021) | Individual revenue only | NTEE pooled 4.5–12.9% (scaled 6.7–19.1% [I]). International pooled 4.9% (scaled 7.2% [I]), near the bottom. International median 8.9%, second only to religion (13.4%) among groups with more than 100 frame EINs. |

**Interpretation [I]**
- **The two sources are consistent on the order of magnitude.** Once the scaling for non-top-50 sponsors and a private-contributions denominator are applied, the independent figure (≈10–15% pooled) brackets Chariot's 12.6%.
- **They are not consistent on large organisations.** Filed returns show that DAF grants are a *smaller* share of contributions at ≥$100m charities (3.7% pooled, 1.1% median, unscaled) than at small ones. Chariot's participants average about $97m of total giving a year [I], between the two largest bands. On the private basis, the scaled figures of 15.7% ($25–100m) and 8.4% (≥$100m) bracket its 12.6%, so the gap is clear only against the ≥$100m band. The comparison is not like-for-like: CRM-coded gifts from all sponsors over 2021–25, against top-50 Schedule I over FY2023–24 [V wave 33A]
  - Several explanations remain open: participant self-selection, the denominator (individual giving against 1h), and the definition of DAF gifts (vendor matching of DAF-originated gifts against Schedule I).
  - The participant list and definitions are gated (P-B40N12-01).
- **The sector ordering does not replicate.** On filings, international is not the most DAF-dependent sector by dollars. Its large members (IRC 4.7%, MSF 13.1%) carry big denominators, often government grants: IRC is 13.1% of 1h−1e because line 1e is 64% of its 1h. Chariot's 23.7% for International Relief is stated on total revenue, not individual revenue [V wave 33A]

## 4. Limits

1. **The numerator is a floor.** It covers top-50 sponsors only, and only Schedule I lines over $5,000 per recipient. The scaling in §2.4 is an inference that assumes the remaining sponsors' grants reach recipients in top-50 proportions. Community-foundation money is probably more local and smaller-recipient-weighted, so the size gradient may be steeper than shown (P-B40N1202-01).
2. **DAF weighting is sponsor-level.** A community foundation's DAF share of grants is applied uniformly to all its Schedule I lines. The `schedule_i` basis (all-recipient pooled 7.3%, median 6.5%) is the upper bound on this point.
3. **Denominator scope.** Line 1h includes government grants (1e), foundation and corporate grants, federated campaigns and related-organisation transfers. The 1h−1e variant is reported, but individual giving cannot be isolated from Part VIII (P-B40N1202-03).
4. **Timing.** Sponsor fiscal years are matched to recipient fiscal years by the calendar year in which the tax period ends, and two years are pooled. Recipients book pledges on an accrual basis and sponsors report cash grants, so 2.8% (weighted) of recipients exceed 100%.
5. **Out-of-scope recipients.**
   - Churches, 990-N filers and government units have no line 1h, so the religion figures cover only religious organisations that file a 990.
   - 22,269 recipient EINs ($4.36bn) are not in the BMF and are excluded.
   - The no-NTEE <$1m stratum has only 4 in-scope respondents of 40 sampled, and religion <$1m has 15. Their weights are large and their intervals wide (P-B40N1202-04).
6. **Classification.**
   - Revenue bands use BMF `REVENUE_AMT` from the latest filing, not FY2023–24; zero or blank values are placed in <$1m.
   - Exclusions rely partly on names. "COLLEGE" also drops some college-access charities, and university foundations that use other words survive.
   - Re-granting intermediaries are not excluded in the headline; see the sensitivity rows.
7. **Selection.** The frame is charities that received at least one itemised top-50 DAF grant. The figures describe the DAF share of revenue **among DAF recipients**, not across all US charities.
8. **Sampling.** The sample is stratified, 2,352 EINs with seed 20261119, not a census. The bootstrap intervals cover sampling error only, not the definitional uncertainties above.

## 5. Reproduction

```
S=<scratchpad>
python3 scripts/mission_daf_share_recipient_revenue.py . --np-cache $S/npcache --lines-cache $S/rcp/lines \
    --bmf-dir $S/rcp/bmf --index-dir $S/irs --f990-cache $S/q1202/f990 [--fetch] \
    [--seed 20261119 --per-stratum 40 --certainty 400 --boot 500]
```
- The run takes about 35 seconds with a warm cache, and about 2 minutes to fetch the 4,315 returns.
- It writes the CSV and prints a JSON summary to stdout: exclusion mix, coverage, status counts and the largest certainty recipients.

## 6. Data dictionary: `daf-share-of-recipient-revenue-2026-11-19.csv`

`row_type = summary` rows (19) use the first block of columns. `row_type = recipient` rows (2,352) use the second. Shares are fractions (0.059 = 5.9%).

**Summary columns**

| Column | Meaning |
|---|---|
| row_type | `summary` or `recipient` |
| scope_type / scope | `all`, `sensitivity`, `ntee_major_group` (NTEE first letter mapped as in mission_recipient_sectors.MAJOR; `no_ntee` = blank BMF NTEE) or `revenue_band` (BMF REVENUE_AMT: a <$1m, b $1–5m, c $5–25m, d $25–100m, e ≥$100m) |
| frame_recipients | Frame EINs in scope (before the out-of-scope adjustment) |
| frame_num_sched_i_fy2023_2024 | Frame numerator, Schedule I basis, USD |
| sampled / respondents | Sampled EINs; in-scope respondents (status `ok`) |
| weighted_recipients | Σ weights over respondents (estimated in-scope population) |
| p25_ / median_ / p75_share_daf_weighted | Weighted quantiles of per-recipient share (DAF-weighted numerator / 1h) |
| median_ci95_lo / _hi, pooled_ci95_lo / _hi | Stratified bootstrap 95% interval (500 replicates) |
| median_share_sched_i, pooled_share_sched_i | Same, on the as-filed Schedule I numerator |
| pooled_share_daf_weighted | Σw·num / Σw·1h |
| pooled_share_daf_weighted_capped | Same, with each numerator capped at its denominator |
| pooled_share_of_private_contrib | Σw·num / Σw·(1h − 1e) |
| share_gt_100pct, share_ge_20pct | Weighted fraction of respondents with share >1 and ≥0.2 |
| scaled_pooled_share_inference, scaled_pooled_capped_inference, scaled_median_share_inference, scaled_pooled_private_inference | **[I]** The corresponding share divided by top-50 FY2024 coverage (0.6727) |
| source | Source note |

**Recipient columns**

| Column | Meaning |
|---|---|
| ein, name, state, ntee_cd, bmf_revenue_amt | From the IRS EO BMF |
| ntee_major_group, revenue_band | Classification used for stratification and reporting |
| stratum, stratum_N | `certainty` or `group\|band`; frame size of the stratum |
| top50_grantors | Number of distinct top-50 sponsors granting FY2023–24 |
| num_sched_i_fy2023 / _fy2024 / _fy2023_2024_all | Numerator by sponsor FY, Schedule I basis, USD |
| years_matched, forms, object_ids | FYs with a readable recipient return; IRS990/IRS990EZ; TEOS object ids |
| num_sched_i_matched, num_daf_weighted_matched | Numerator over matched FYs |
| den_contributions_matched | Part VIII line 1h (990) or line 1 (990-EZ), summed over matched FYs |
| den_gov_grants_1e_matched | Part VIII line 1e over matched FYs (990 only; 0 for EZ) |
| total_revenue_matched | Part I line 12 (990) or line 9 (990-EZ) |
| share_sched_i, share_daf_weighted, share_of_private_contrib, share_of_total_revenue | Per-recipient shares (blank unless status `ok`) |
| status | `ok`; `no_fy2023_2024_990_or_ez_in_index` (out of scope); `xml_not_read` (missing); `zero_or_negative_contributions` (out of scope) |

## 7. Source register

| ID | Source | URL | Accessed / version | Use |
|---|---|---|---|---|
| S1 | IRS Form 990 e-file XML, GivingTuesday mirror of IRS TEOS | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | 2026-11-19 (robots.txt 404) | Recipient Part VIII 1h / 1e, total revenue; sponsor Schedule I lines (cached earlier) |
| S2 | IRS TEOS e-file index | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (and 2023, 2025, 2026) | Cached 2026-11-14 | Locating recipient returns |
| S3 | IRS Exempt Organizations Business Master File | https://www.irs.gov/pub/irs-soi/eo1.csv (eo1–eo4, eo_pr, eo_xx) | Last-Modified 2026-11-09 | NTEE, FOUNDATION, SUBSECTION, REVENUE_AMT |
| S4 | IRS Form 990 instructions (Part VIII line 1; Schedule I $5,000 threshold) | https://www.irs.gov/pub/irs-pdf/i990.pdf ; https://www.irs.gov/pub/irs-pdf/i990si.pdf | Current editions | Field definitions |
| S5 | DAFRC Annual DAF Report 2025 updated dataset | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Repo copy: dafrc-sponsor-schedule-d-fy2019-2024.csv | Top-50 universe; raw FY2024 DAF grants |
| S6 | Repo netted market totals | [dafrc-market-totals-netted.csv](../../data/mission-2026-11-14/dafrc-market-totals-netted.csv) | Repo | Netted FY2023–24 DAF grants (central) |
| S7 | Chariot/K2D DAF Fundraising Report 2026 page | https://www.givechariot.com/resources/toolkits/daf-fundraising-report | As recorded in the repo, 2026-11-15 | Sector range 4–24%; International Relief 23.7% |
| S8 | Chariot 2026 report release webinar | https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release | As recorded in the repo, 2026-11-15 | "nearly 13%"; $3.3bn of $26.1bn; 54 nonprofits |
| S9 | Chariot, Inside the 2025 DAF Fundraising Report | https://www.givechariot.com/resources/insights/inside-the-2025-daf-fundraising-report-how-donor-advised-funds-are-transforming-philanthropy | As recorded in the repo, 2026-11-15 | 15% for orgs <$10m |
| S10 | NonProfit Times on Chariot/K2D 2024 | https://thenonprofittimes.com/npt_articles/daf-donors-making-their-presence-felt/ | As recorded in the repo, 2026-11-15 | Median 12% (20 orgs) |
| S11 | Repo benchmark compilation | [direction-nonprofit-daf-benchmarks.md](direction-nonprofit-daf-benchmarks.md); [nonprofit-daf-revenue-benchmarks-2021-2026.csv](../../data/mission-2026-11-14/nonprofit-daf-revenue-benchmarks-2021-2026.csv) | Repo | NPB001–002, 019–021, 024, 038–040 |

The Chariot figures (S7–S10) were not re-fetched for this note. They are quoted as verified in [validation-wave25b-report.md](validation-wave25b-report.md).
