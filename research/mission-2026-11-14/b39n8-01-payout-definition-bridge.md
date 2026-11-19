# P-B39N8-01: payout-definition bridge on the corrected FY2020–24 sponsor panel (23.9% vs 9.7% vs 9%)

**Date:** 2026-11-19 · **Queue item:** P-B39N8-01 (proposed in [direction-academic-literature.md](direction-academic-literature.md) F4: "The repo can publish a definition bridge")

**Outputs**
- [`data/mission-2026-11-14/payout-definition-bridge-2026-11-19.csv`](../../data/mission-2026-11-14/payout-definition-bridge-2026-11-19.csv): 2,621 rows in long format. It holds the panel payout grid, market totals, the IPS reproduction, the decomposition and the quoted benchmarks. The data dictionary is in §8.
- [`scripts/mission_payout_bridge.py`](../../scripts/mission_payout_bridge.py): stdlib only, functional style. It reuses the repo's R1–R4 merge and its R5 attribution (`mission_league_table.netting_by_sponsor`, which calls `mission_market_netting.py` unchanged).
- [`data/mission-2026-11-14/queue-proposals-b39n8-01.csv`](../../data/mission-2026-11-14/queue-proposals-b39n8-01.csv): 5 proposals.

Evidence tags: [F] computed here from filed/panel data, [Q] quoted from a primary source, [I] inference.

## 0. Headline answers

| Question | Answer |
|---|---|
| **Where does "23.9%" come from?** | It is **NPT's FY2023 aggregate payout**: all grants divided by all prior-year assets (NPT 2024 DAF Report; quoted by IPS 2025 p.14) [Q]. The repo's corrected panel gives **24.0%** on the same definition for FY2023 (market total $54.83bn / $228.14bn) [F]. The repo's other "23.9%" (pooled FY2021–24, excluding processors, itemised Schedule I sample; [queue-net-payout-fidelity-outliers.md](queue-net-payout-fidelity-outliers.md)) is a different statistic that happens to be equal. |
| **IPS 9.7% reproduced?** | **Exactly, from IPS's own sponsor file:** the median of its 1,487 FY2023 sponsor rates is 9.68%, the same as its Summary Table. Recomputing grants ÷ (assets + grants) from IPS's columns gives the same rates to within 5e-12 [F]. **On the repo panel, the same formula gives 9.33%** (1,481 sponsors with assets > 0). The gap is **entirely a difference in universe**. On the 1,315 EINs in both datasets, all 1,315 rates agree to within 0.05 points, and both medians are 9.77% [F]. |
| **Why the universes differ** | (1) IPS computes no rate for **248 sponsors whose DAF-grants cell is blank**, but keeps 100 with an explicit 0. Counting the blanks as 0% would give an IPS median of **7.72%** [F]. (2) IPS has **172 small sponsors that were never in the DAFRC panel** (169 single-issue; median DAF assets $126k; median rate 7.3%). (3) The repo has **166 sponsor-years outside IPS's rated set**: 79 have a blank grants cell in IPS, 87 are not on IPS's list, 83 have zero grants, and 23 still use imputed values [F]. The repo panel with DAF grants > 0 gives 10.20%. So the two bounds, 9.33% and 10.20%, bracket IPS's 9.68% [F]. |
| **(a) vs (b), FY2023** | Excluding processors: **beginning assets: median sponsor 11.2%, pooled 22.6%. IRS/IPS formula: median 9.2%, pooled 16.7%** [F]. Across FY2020–24, the IRS formula is 0.6–3.1 points below beginning assets at the median and 3.6–10.2 points below in the pooled figure (§3). |
| **(c) filters** | The ≥$1m filter raises the median by 0.3–0.7 points and barely moves the pooled figure. FY2023 medians are 11.8% (beginning assets) and 9.7% (IRS). Removing processors lowers the pooled beginning-asset figure by 1.4–1.8 points (FY2023: 24.0% → 22.6%) and moves the median by ≤0.2 points [F]. |
| **(d) net of R5 (central)** | FY2023, excluding processors: pooled beginning-assets payout falls from **22.6% to 20.8%** and the median from 11.2% to 11.1%. Pooled IRS falls from 16.7% to 15.6%; the median from 9.2% to 9.1%. Central-tier netting moves pooled figures by 1.1–3.2 points but medians by ≤0.4 points (≤0.8 in the upper tier) [F]. |
| **Bridge from 23.9% to 9%, FY2023** [I for the attribution] | Total gap 14.9 points. (i) Data/universe (NPT vs corrected panel): +0.1. (ii) Processors removed: −1.5. (iii) **Denominator** (beginning → IRS, Shapley): **−5.9**. (iv) **Sponsor weighting**: pooled → median sponsor −9.4, then median sponsor → median *account* if every account paid its sponsor's rate +8.3 (net −1.1). (v) **Within-sponsor distribution** (residual to 9%) **−6.6** [I]. If DAFRC's account rate is closer to beginning assets, the denominator step drops out and the within-sponsor residual becomes −12.5 [I]. |
| **Reading** [I] | The median sponsor on the IRS formula (9.3%) lands next to DAFRC's account median (9%) by coincidence, not because the two measure the same thing. Weighted by accounts, the median account sits at a fast-paying national: Fidelity's own rate in 4 of 5 years (FY2023: 15.6% IRS formula, 21.5% beginning assets). For the account median to be 9%, account rates within sponsors must be strongly right-skewed. That fits DAFRC's own mean of 18% against a median of 9%, and its 22% of inactive accounts [Q]. |

## 1. Question and sources of the three figures

The literature pass ([direction-academic-literature.md](direction-academic-literature.md) F4; [validation-wave24b-report.md](validation-wave24b-report.md) V24B-28) found three payout figures in use, built on different definitions:
- **23.9%**: NPT, FY2023. Aggregate grants_t ÷ aggregate assets_{t−1}, all sponsors, with processors included [Q] ([NPT 2024 DAF Report](https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/); repo `daf-market-annual-series.csv` row NPT_DAFR_HEADLINE FY2023 = 23.9; IPS 2025 p.14 quotes the same figure).
- **9.7%**: IPS, FY2023. The median across sponsors of grants_t ÷ (EOY assets_t + grants_t), all sponsor types including processors [Q] ([IPS report p.14 and Appendix A](https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf)). The Summary Table gives 0.0968 ([xlsx](https://inequality.org/wp-content/uploads/2025/04/Independent-DAF-Report-Summary-Table.xlsx)).
- **9%**: DAFRC 2024 National Study. The median of account-level three-year (2020–22) payout across more than 50,000 accounts at 111 voluntarily reporting programmes. It is 15% excluding inactive accounts; the mean is 18%; about 22% of accounts were inactive (zero payout) in 2020–22 [Q] ([executive summary](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf); [full study](https://www.dafresearchcollaborative.org/s/DAFRC-National-Study-DAFs-Feb-2024.pdf), slides 13–14). Neither document states the account-level denominator.

## 2. Method

**Panel.** The panel is DAFRC's 2025 sponsor dataset (`dafrc-sponsor-schedule-d-fy2019-2024.csv`), overridden by every `applied = 1` row of `dafrc-corrections-itemized.csv` (R1–R4, FY2020–24), plus R4 additions. This is the same merge as `mission_league_table.corrected`. FY2019 is used as published, only as beginning assets for FY2020. **Check:** rebuilt FY2020–24 sums of EOY assets and grants equal `dafrc-corrected-market-totals.csv` to the dollar (10 of 10). The FY2021–24 beginning-asset results also reproduce `payout-triad-2021-2024.csv`: for example, FY2023 has n = 1,439, median 11.34% and market total 24.03% [F].

**R5.** Per-grantor capped outbound DAF-to-DAF amounts come from the Schedule I cache, via `mission_league_table.netting_by_sponsor` (lower, central and upper tiers). **Check:** the rebuilt FY2021–24 totals equal `dafrc-market-totals-netted.csv` to the dollar (12 of 12). Net grants = max(grants − R5 outbound, 0); assets are unchanged. R5 is not defined for FY2020.

**Formulas.**
- (a) `beg`: grants_t ÷ EOY assets_{t−1}. Requires assets_{t−1} > 0.
- (b) `irs`: grants_t ÷ (EOY assets_t + grants_t). Requires assets_t ≥ 0.

**Statistics per (FY, formula, sample, netting).**
- Median and pooled (Σ numerators ÷ Σ denominators over the same sponsor-years).
- p25, p75, mean, and the share below 5%.
- Account-weighted median: sponsor-years weighted by corrected EOY account count.
- Separately, the market total (all grants_t ÷ all assets_{t−1}, NPT/DAFRC convention).

**Samples.**

| Sample | Definition |
|---|---|
| `all_incl_proc` | All sponsors meeting the formula's condition (processors included) |
| `ex_proc` | DAFRC subtype "Donation Processor" removed |
| `ex_proc_ge1m` | The formula's asset term ≥ $1m: assets_{t−1} for `beg`, assets_t + grants_t for `irs` |
| `incl_proc_ge1m` | `all_incl_proc` with the same $1m filter |
| `ex_proc_ge1m_filed` | No imputed grants or assets left after correction (the basis of the repo's earlier 11–12.5% median) |
| `*_matched` | Qualifies for both formulas. Used for the decomposition so that only one factor changes at a time |

**IPS reproduction.**
1. Download IPS's sponsor lists and summary table, after a robots.txt check (§7). Take the median of IPS's own "Average DAF Payout" column, then recompute grants ÷ (assets + grants) from its columns.
2. Apply IPS's Appendix A rules to the repo panel where Schedule D alone allows it:
   - DAF assets > 0, with processors kept;
   - the deficiency screens (negative grants or contributions; accounts ≤ 0; accounts equal to contributions or grants; accounts ≥ assets; assets = grants).
   The 501(c)(3), total-grants and submission-date screens need the full return and are not applied.
3. Variants: filed-only, and DAF grants > 0.
4. Match EINs. Split the median gap into a repo-side universe term, a value term on the intersection and an IPS-side universe term.

**Decomposition** (matched samples). The two denominators (beg, irs) are crossed with three weightings:
- P = pooled;
- M = median sponsor;
- W = account-weighted median, i.e. the rate of the median account if every account paid its sponsor's rate.

The steps between them:
- Denominator effect D = ½[(P_beg − P_irs) + (W_beg − W_irs)].
- Weighting W1 (P → M) = ½[(P_beg − M_beg) + (P_irs − M_irs)].
- Weighting W2 (M → W) = ½[(M_beg − W_beg) + (M_irs − W_irs)].
- D + W1 + W2 = P_beg − W_irs exactly (checked in the CSV).
- Residual: W − 9% is attributed to the within-sponsor distribution. It also contains sample, window and definition differences [I].

## 3. Results: payout grid, FY2020–24 (median / pooled; n = sponsor-years for the median)

**(a) Beginning assets**

| Sample, netting | FY2020 | FY2021 | FY2022 | FY2023 | FY2024 |
|---|---|---|---|---|---|
| all incl. processors, gross | 11.3% / 24.8% (1,325) | 11.6% / 28.1% (1,411) | 10.4% / 23.7% (1,429) | 11.3% / 24.0% (1,439) | 12.3% / 25.7% (1,479) |
| excl. processors, gross | 11.1% / 23.0% | 11.5% / 26.4% | 10.2% / 22.2% | 11.2% / 22.6% | 12.1% / 24.2% |
| excl. processors, ≥$1m, gross | 11.5% / 22.9% (917) | 11.8% / 26.4% (986) | 10.5% / 22.2% (1,020) | 11.8% / 22.5% (1,011) | 12.5% / 24.2% (1,055) |
| excl. processors, ≥$1m, filed only | 11.7% / 23.0% | 11.8% / 26.4% | 10.5% / 22.2% | 11.9% / 22.5% | 12.8% / 24.2% |
| excl. processors, R5 central | – | 11.2% / 23.2% | 9.9% / 19.5% | 11.1% / 20.8% | 11.9% / 21.2% |
| excl. processors, ≥$1m, R5 central | – | 11.6% / 23.1% | 10.4% / 19.5% | 11.5% / 20.8% | 12.2% / 21.1% |
| excl. processors, R5 lower / upper (pooled) | – | 24.0% / 22.6% | 20.2% / 19.1% | 21.1% / 20.5% | 21.6% / 20.7% |
| **market total** (all grants ÷ all prior assets), gross | 26.9% | 28.5% | 23.8% | 24.0% | 25.9% |
| market total, R5 central | – | 25.2% | 21.0% | 22.3% | 22.8% |

**(b) IRS/IPS formula, grants ÷ (EOY assets + grants)**

| Sample, netting | FY2020 | FY2021 | FY2022 | FY2023 | FY2024 |
|---|---|---|---|---|---|
| all incl. processors, gross | 9.6% / 17.4% (1,434) | 8.6% / 17.0% (1,452) | 9.7% / 19.6% (1,469) | 9.4% / 17.6% (1,486) | 10.2% / 17.0% (1,484) |
| excl. processors, gross | 9.4% / 16.4% | 8.4% / 16.2% | 9.6% / 18.6% | 9.2% / 16.7% | 10.0% / 16.2% |
| excl. processors, ≥$1m, gross | 10.1% / 16.4% (1,037) | 8.9% / 16.2% (1,070) | 10.3% / 18.6% (1,063) | 9.7% / 16.7% (1,098) | 10.5% / 16.2% (1,112) |
| excl. processors, ≥$1m, filed only | 10.2% / 16.5% | 8.9% / 16.2% | 10.3% / 18.6% | 9.7% / 16.7% | 10.6% / 16.2% |
| excl. processors, R5 central | – | 8.3% / 14.5% | 9.4% / 16.7% | 9.1% / 15.6% | 9.8% / 14.5% |
| excl. processors, ≥$1m, R5 central | – | 8.7% / 14.5% | 10.1% / 16.7% | 9.6% / 15.6% | 10.3% / 14.5% |
| incl. processors, ≥$1m, gross | 10.2% / 17.4% | 9.0% / 17.0% | 10.4% / 19.6% | 9.7% / 17.6% | 10.6% / 17.0% |

All values are [F]. Further rows are in the CSV: R5 lower and upper for every sample, p25, p75, mean, share below 5%, and the account-weighted median.

**What the grid shows** [F]:
- The denominator moves medians only modestly (0.6–3.1 points) but moves pooled figures a lot (3.6–10.2 points). Pooled payout is driven by large, fast-paying sponsors, whose grants are a large fraction of their year-end assets plus grants.
- The ≥$1m filter and the filed-only filter each move the median by under 1 point.
- R5 central netting lowers pooled payout by 1.1–3.2 points (FY2022 excluding processors: 22.2% → 19.5%) but medians by ≤0.4 points (≤0.8 in the upper tier). Most small sponsors make few or no DAF-to-DAF grants.
- FY2020's market total (26.9%) is above the matched pooled figure (24.8%). Its denominator is the uncorrected FY2019 panel, and its numerator includes sponsors without a FY2019 row.

### 3.1 IPS reproduction by year (IRS formula, all sponsor types)

| FY | IPS published median | IPS file, recomputed | Repo, assets > 0 (+ IPS screens) | Repo, grants > 0 | EINs in both | Rates equal on intersection | Median on intersection (repo = IPS) | Repo-only n (median) | IPS-only n (median) |
|---|---|---|---|---|---|---|---|---|---|
| 2020 | 10.09% | 10.09% (1,298) | 9.54% (9.56%) | n/a | 1,181 | 1,177 | 10.33% | 247 (3.7%) | 117 (3.1%) |
| 2021 | 8.80% | 8.80% (1,358) | 8.52% (8.62%) | n/a | 1,227 | 1,223 | 9.08% | 221 (3.1%) | 131 (3.6%) |
| 2022 | 10.13% | 10.13% (1,404) | 9.62% (9.62%) | n/a | 1,267 | 1,266 | 10.40% | 196 (3.6%) | 137 (4.2%) |
| **2023** | **9.68%** | **9.68% (1,487)** | **9.33% (9.34%)** | **10.20%** | **1,315** | **1,315** | **9.77%** | **166 (0.05%)** | **172 (7.3%)** |

All values are [F] except the IPS published column [Q]. The "grants > 0" variant is in the CSV for every year; it is shown here for FY2023 only.

**FY2023 gap of −0.35 points (repo 9.33% − IPS 9.68%):**
- universe on the repo side: −0.44;
- values on the intersection: 0.00;
- universe on the IPS side: +0.10.

### 3.2 Why the repo cannot hit 9.68% exactly

These are universe differences that Schedule D Part I and the DAFRC panel cannot resolve [F]:
- **Blank vs zero grants.** IPS's FY2023 file has 1,735 sponsors (the Summary Table count), but rates for only 1,487. The 248 without a rate all have a blank "Grants from DAFs" cell (216 single-issue, 31 CF, 1 national). Another 100 sponsors with an explicit 0 are kept at 0%. Counting the blanks as 0 gives a median of 7.72%. The DAFRC panel does not distinguish blank from 0 (132 zero-grant sponsor-years in FY2023). A bracket follows:
  - keeping all zero-grant sponsors gives 9.33%;
  - dropping them all gives 10.20%;
  - IPS, dropping only the blanks, gives 9.68%.
- **IPS-only sponsors (172).** None appears in the DAFRC panel in any year from FY2019 to FY2024. They are 169 single-issue sponsors and 3 CFs, with median DAF assets of $126k. IPS draws on every e-filed 990 reporting DAF assets; DAFRC's sponsor universe is narrower.
- **Repo-only sponsor-years (166).**
  - 79 are on IPS's list but with a blank grants cell.
  - 87 are not on IPS's list at all (median rate 12.2%). IPS's other rules plausibly exclude them: the submission cutoff of 31 January of the second year, the 501(c)(3) flag, and the total-grants screen [I]. 23 of the 166 still carry DAFRC-imputed values, i.e. no usable same-FY e-file.
- **Screens that cannot be applied:** the 501(c)(3) indicator, Part I line 13 total grants, and the signature-date cutoff. IPS's data were downloaded from the IRS on 31 January 2025; the repo's corrections use returns filed up to 2026.

## 4. Benchmarks side by side (FY2023 unless stated)

| Measure | Value | Basis |
|---|---|---|
| NPT aggregate, beginning assets, all sponsors | 23.9% | [Q] NPT 2024 report |
| Repo market total, beginning assets, corrected | 24.0% (R5 central 22.3%) | [F] |
| Repo pooled, beginning assets, excl. processors | 22.6% (R5 central 20.8%) | [F] |
| Repo pooled, IRS formula, excl. processors | 16.7% (R5 central 15.6%) | [F] |
| Repo median sponsor, beginning assets, excl. processors, ≥$1m | 11.8% (R5 central 11.5%) | [F] |
| IPS median sponsor, IRS formula (published) | 9.68% | [Q] |
| Repo median sponsor, IRS formula, all types | 9.4% (assets > 0 only, IPS screens: 9.33–9.34%) | [F] |
| Repo account-weighted median of sponsor rates, IRS, excl. processors | 15.6% (= Fidelity Charitable's rate) | [F] |
| DAFRC 2024 account median, 3-year 2020–22 | 9% (15% active only; mean 18%; 22% inactive) | [Q] |

## 5. Decomposition of the 23.9% → 9% gap

### 5.1 FY2023, excluding processors, matched sample (n = 1,417), gross

| Weighting ↓ / denominator → | Beginning assets | IRS (EOY + grants) |
|---|---|---|
| Pooled (P) | 22.58% | 16.75% |
| Median sponsor (M) | 11.23% | 9.28% |
| Account-weighted median (W) | 21.53% | 15.63% |

| Step | Points | Basis |
|---|---|---|
| NPT 23.9% → repo market total 24.03% (data/universe) | +0.1 | [F]/[Q] |
| Remove processors (matched pooled 24.04% → 22.58%) | −1.5 | [F] |
| **Denominator**, beginning → IRS (Shapley, P and W) | **−5.9** | [F] |
| **Sponsor weighting, pooled → median sponsor** (W1) | **−9.4** | [F] |
| **Sponsor weighting, median sponsor → median account at sponsor rates** (W2) | **+8.3** | [F] |
| = account-weighted median, IRS formula (W_irs) | 15.63% | [F] |
| **Within-sponsor distribution + sample/definition residual** (W_irs − 9%) | **−6.6** | [I] |
| = DAFRC account median | 9% | [Q] |

**Shares of the 14.9-point gap:**
- data/universe: ≈0;
- processors: 10%;
- denominator: 39%;
- net sponsor weighting: 7% (−9.4 + 8.3);
- within-sponsor: 44% [I].

If the account-level rate is assumed to be on beginning balances, the account-weighted median is 21.53%. The denominator step then disappears, net weighting is −1.05 points, and the within-sponsor residual is −12.5 points (84% of the gap) [I]. Because DAFRC does not state its denominator in the published documents, the defensible statement is: **denominator 0–6 points, net sponsor weighting about 1 point, within-sponsor distribution 6.6–12.5 points** [I].

**Alternative path through the median sponsor**, which is what IPS reports. From pooled beginning assets (22.58%) to median sponsor on the IRS formula (9.28%) is 13.3 points: 3.9 from the denominator (Shapley over P and M) and 9.4 from sponsor weighting [F]. The median sponsor (9.28%) is then 0.3 points from DAFRC's account median. This is numerical proximity, not identity [I]. The median sponsor is a small community or single-issue foundation, while the median account sits at a large national.

### 5.2 Robustness

- **FY2020–22 mean** (DAFRC's account window, excluding processors, matched):
  - P_beg 23.9%, P_irs 17.2%;
  - M_beg 11.0%, M_irs 9.1%;
  - W_beg 23.8%, W_irs 17.2%;
  - D −6.7, W1 −10.5, W2 +10.5;
  - within-sponsor residual −8.2 (IRS) or −14.8 (beginning assets) [F]/[I].
- **R5 central, FY2023:** D −5.2, W1 −8.1, W2 +7.0, residual −5.6 (IRS) or −10.8 (beginning assets). Netting shrinks every step a little but changes no ranking [F]/[I].
- **≥$1m matched:** M_irs 9.69%, W1 −8.8, W2 +7.8 [F].
- **Pivot sponsor.** Excluding processors, the account-weighted median is Fidelity Charitable's own rate in FY2020, 2022, 2023 and 2024. Fidelity's FY2023 rate is 15.63% on the IRS formula, which matches IPS's row for Fidelity. W2 therefore rests on one sponsor (proposal P-B39N8-01-04).
- **With processors**, the account-weighted median is a processor rate (FY2023 W_irs 86%), because processors hold most accounts (mostly micro-accounts). That row is in the CSV but is not meaningful for the bridge [F].

## 6. Limits

- **DAFRC's account-level denominator is not stated** in the executive summary or the study slides. The within-sponsor residual is therefore a range, and it also absorbs:
  - the voluntary 111-programme sample (no processors; its mix of national and CF programmes is not published here);
  - the three-year 2020–22 window, against single fiscal years here;
  - the definition [I].
- **The account-weighted median assumes every account in a sponsor pays the sponsor rate.** It is a construction, not data. Fund-level payout is not public in Form 990 filings.
- **IPS's 501(c)(3), total-grants and submission-date screens could not be applied.** The blank-vs-zero distinction is not in the DAFRC panel.
- **FY2019 is uncorrected.** R1–R4 cover FY2020–24 only, so FY2020 beginning-asset figures use the published FY2019 values.
- **R5 uses the Schedule I cache** built by `mission_net_payout.py`, from an earlier session's scratch directory. The rebuild matches the published netting totals exactly, but the cache itself is not in the repository.
- **Net (d) floors net grants at 0** and leaves assets unchanged. Inbound DAF-to-DAF contributions are not removed from recipients' assets (they are a stock).
- **The ≥$1m filter applies to the formula's own asset term.** For the matched samples it applies to both asset terms.

## 7. Reproduction and robots log

```
S=<scratch dir>
# IPS files (robots checked first; the script can do it with --fetch-ips)
python3 scripts/mission_payout_bridge.py . --np-cache $S/npcache --ips-dir $S/ips [--fetch-ips]
```

The script prints JSON with the rebuild checks (panel 10/10 equal, R5 12/12 equal), the FY2023 grid, the IPS comparison and universe profile, and the FY2023 and FY2020–22 decompositions.

| Host | robots.txt (fetched 2026-11-19, UA `research-script/1.0`) | Fetched |
|---|---|---|
| ips-dc.org / www.ips-dc.org | `User-agent: * / Disallow:` (empty), so all allowed | report page (`/independent-report-on-dafs/`), report PDF |
| inequality.org | `User-agent: * / Disallow:` (empty), so all allowed | Sponsor-Lists.xlsx, Summary-Table.xlsx |
| johnsoncenter.org | `User-agent: * / Disallow:` (empty), `Crawl-delay: 10` | DAFRC executive summary PDF (one request) |
| www.dafresearchcollaborative.org | `User-agent: *` disallows /config, /search, /account, /api, /static and query patterns; `/s/` allowed | national-study-dafs page, DAFRC-National-Study-DAFs-Feb-2024.pdf |

No logins, forms or outreach were used. No other hosts were contacted.

## 8. Data dictionary: `payout-definition-bridge-2026-11-19.csv`

| Column | Meaning |
|---|---|
| `row_id` | PB0001…, stable within this file |
| `section` | `panel_payout` (grid), `market_total` (all grants ÷ all prior assets), `ips_reproduction`, `decomposition`, `external_benchmark` |
| `fiscal_year` | Calendar year in which the tax period ends; `2020-2022_mean` for the window means in `decomposition` |
| `formula` | `beg` = grants_t ÷ EOY assets_{t−1}; `irs` = grants_t ÷ (EOY assets_t + grants_t); `beg_vs_irs` for decomposition rows; `dafrc_3yr_account` for DAFRC benchmarks |
| `sample` | See §2. Panel samples: `all_incl_proc`, `ex_proc`, `ex_proc_ge1m`, `incl_proc_ge1m`, `ex_proc_ge1m_filed`, `*_matched`. IPS rows: `ips_published_summary_table`, `ips_sponsor_list_published_rate`, `ips_sponsor_list_ex_proc`, `ips_sponsor_list_blank_grants_as_zero`, `repo_assets_gt0_*`. Benchmark rows: the benchmark key |
| `netting` | `gross`, `r5_lower`, `r5_central`, `r5_upper` (FY2021–24) |
| `statistic` | Grid: `median`, `pooled`, `p25`, `p75`, `mean`, `share_below_5pct`, `account_weighted_median`. IPS rows: `median`, `pooled`, `ips_median`, `n_intersection`, `median_intersection_repo_values`, `median_intersection_ips_values`, `n_repo_only`, `median_repo_only`, `n_ips_only`, `median_ips_only`, `n_intersection_rate_within_0_05pt`, `gap_total`, `gap_universe_repo_side`, `gap_values_on_intersection`, `gap_universe_ips_side`. Decomposition: `P_beg`, `P_irs`, `M_beg`, `M_irs`, `W_beg`, `W_irs`, `market_total_beg`, `D_denominator_shapley_P_to_W`, `W1_pooled_to_median_sponsor`, `W2_median_sponsor_to_account_weighted`, `D_denominator_shapley_P_to_M`, `check_*`, `R_within_sponsor_vs_W_irs`, `R_within_sponsor_vs_W_beg` |
| `value` | Ratio (0.239 = 23.9%), a count, or a difference in ratio points. Six significant digits |
| `n_sponsor_years` | Sponsor-years behind the statistic (grid and IPS rows) |
| `numerator_usd`, `denominator_usd` | Pooled rows only: Σ grants (net, if netted) and Σ denominator, in USD |
| `basis` | `F` computed here, `Q` quoted from the source, `I` inference |
| `note` | Definition notes and caveats |
| `source` | Input files and primary URLs |

## 9. Source register

| # | Source | URL | Used for |
|---|---|---|---|
| S1 | DAFRC Annual DAF Report 2025, Updated Analysis dataset (Spring 2026) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Sponsor panel FY2019–24 (repo copy `dafrc-sponsor-schedule-d-fy2019-2024.csv`) |
| S2 | Repo corrections R1–R4 (IRS TEOS index and Form 990 XML) | https://apps.irs.gov/pub/epostcard/990/xml/2021/index_2021.csv ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | `dafrc-corrections-itemized.csv` (per-row URLs) |
| S3 | Repo R5 netting (Form 990 Schedule I Part II) | as S2; [full-universe-990-harvest-and-corrected-totals.md](full-universe-990-harvest-and-corrected-totals.md), [queue-net-payout-fidelity-outliers.md](queue-net-payout-fidelity-outliers.md) | Per-grantor DAF-to-DAF outbound |
| S4 | IPS, *The Independent Report on DAFs*, April 2025 (pp.14–15, Appendix A pp.24–26) | https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf | Method, 9.7% median, NPT 23.9% quotation |
| S5 | IPS report landing page | https://www.ips-dc.org/independent-report-on-dafs/ | Summary statement of 9.7% |
| S6 | IPS sponsor lists (Appendix C) | https://inequality.org/wp-content/uploads/2025/04/Independent-DAF-Report-Sponsor-Lists.xlsx | Per-sponsor rates FY2020–23 |
| S7 | IPS summary table (Appendix B) | https://inequality.org/wp-content/uploads/2025/04/Independent-DAF-Report-Summary-Table.xlsx | Published medians (FY2023 0.0968), sponsor counts |
| S8 | NPT 2024 DAF Report | https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/ | 23.9% FY2023 (via repo `daf-market-annual-series.csv`; not re-fetched) |
| S9 | DAFRC, 2024 National Study on DAFs, executive summary | https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf | 9% median, 15% active, 18% mean, 22% inactive, 111 programmes, >50,000 accounts |
| S10 | DAFRC, National Study on DAFs (Feb 2024 slides) | https://www.dafresearchcollaborative.org/s/DAFRC-National-Study-DAFs-Feb-2024.pdf | Confirms the figures and the 3-year window; mean by sponsor type |
