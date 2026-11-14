# DAF quantitative datasets and data dictionary (mission 2026-11-14)

> **Red-team status (2026-11-14):** independently reviewed in [red-team-wave2b-graph-data-incentives.md](red-team-wave2b-graph-data-incentives.md). The corrections in the final section govern where they conflict with the text.


Prepared 2026-11-14. This file covers the machine-readable datasets in `data/mission-2026-11-14/` and the two scripts that build them and compute metrics from them. All values come from the cited sources. A blank cell means the value was not published or could not be retrieved, and the reason is in `notes`.

## 0. Reuse of existing repo data (no duplication)

| Existing file | How it is used here |
|---|---|
| `data/market-demand-observed-metrics-2026.csv` (M01–M09) | The DAFRC Spring-2026 FY2024 totals already in the repo ($327.87b assets, $90.57b contributions, $64.60b grants, 3.59m accounts, 1,512 sponsors) are carried into `DAFRC_2025_UPDATED` ([DAFRC updated memo, Apr 2026](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)). The script then recomputes them exactly from the sponsor-level dataset. M10–M15 (account-level 9% median payout, 22% inactive) are cited only for contrast. They are not re-entered. |
| `data/expanded-sponsor-activity-benchmarks-2026.csv` (U02, U12–U14, U41, U43) | Re-entered in `sponsor-level-metrics.csv` as `sponsor_self_report` rows marked "Reused (Uxx)", so the share and year-matching logic can process them. |
| `data/rcf-ren-audited-admin-payments-2020-2024.csv` | Gives the actual FY2024 RCF account count (25,824). DAFRC imputes 22,366, so this is the check on DAFRC's imputation. |
| `data/daf-admin-fee-scenarios-2026.csv` (E03–E07) | Supplies the RCF/Ren and DAFgiving360 fee tiers, marked `repo_prior_review`. Fidelity, Vanguard, BofA, Charityvest, NCF, NPT and Daffy were fetched fresh on 2026-11-14. |
| `data/sponsor-expense-category-comparison-2024.csv`, `national-heritage-foundation-filing-trajectory-2014-2022.csv` | Not duplicated. They are expense-category and NHF-specific, which this mission does not cover. |
| `technology-provider-exits-and-incidents-2026.csv`, `expanded-ecosystem-*` (U04, U05, U10, U32, TA20) | Foundation Source, GTCR, Vennfi and PG Calc transactions are re-entered in `company-funding.csv` with the same URLs. Giving Place's closing date has been corrected to 2025-04-21. |

## 1. Files

| File | Rows | Built by | Content |
|---|---|---|---|
| `daf-market-annual-series.csv` | 174 | hand transcription from report PDFs / memo | US market totals from NPT DAF Reports (2015–2024 editions, FY2013–FY2023) and DAFRC (Dec-2025 initial and Apr-2026 updated, FY2020–FY2024) |
| `dafrc-sponsor-schedule-d-fy2019-2024.csv` | 8,751 | `scripts/mission_build_source_extracts.py` | Verbatim DAFRC Spring-2026 sponsor-level dataset: Form 990 Schedule D Part I by EIN × FY, about 1,500 sponsors |
| `sponsor-level-metrics.csv` | 841 | same script | Long format for 18 named sponsors: DAFRC Schedule D rows, ProPublica Form 990 extracts and curated self-reports |
| `sponsor-fee-schedules.csv` | 59 | hand-curated | Admin fee tiers, minimums and investment-expense ranges as of 2026 |
| `company-funding.csv` | 19 | hand-curated | Funding and ownership transactions for DAF tech companies |
| `derived-metrics.csv` | 1,372 | `scripts/mission_daf_metrics.py` | YoY growth, CAGR, payout, shares, concentration and cross-source checks |

Source count: 78 distinct source URLs across the five input files. Every input row has a `source_url`. Derived rows cite their input files in `inputs`.

### Reproduce

```bash
python3 scripts/mission_build_source_extracts.py          # downloads DAFRC xlsx + ProPublica JSON
#   (offline: --dafrc-xlsx PATH --propublica-cache DIR)
python3 scripts/mission_daf_metrics.py                    # writes derived-metrics.csv; prints mismatch count (0)
```

Both scripts use only the Python standard library. The xlsx file is parsed with `zipfile` and `xml.etree`. Transformations are pure functions, and I/O happens only in `main()`.

## 2. Data dictionary

### 2.1 `daf-market-annual-series.csv`
| Column | Meaning |
|---|---|
| `series_id` | `NPT_DAFR_HEADLINE`: each edition's current-year estimate. `NPT_DAFR_REVISED_PRIOR`: the same edition's revised prior-year column. `DAFRC_2025_UPDATED`: the April 2026 memo ([DAFRC updated memo, Apr 2026](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)), which replaces the earlier figures. `DAFRC_2025_INITIAL`: the December 2025 report ([DAFRC Annual DAF Report, Dec 2025](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-DAF-Research-Collaborative.pdf)), now superseded. |
| `publisher`, `report_edition` | Who published the figure and which edition it comes from |
| `fiscal_year` | FY label used by the publisher (see section 3) |
| `fiscal_year_definition` | Publisher's FY rule and payout formula, copied into every row |
| `value_status` | `edition_current_year_estimate`, `revised_prior_year_in_next_edition`, `revised_current`, `superseded_initial`, `edition_sponsor_file` |
| `metric` | `charitable_assets`, `contributions`, `grants` (USD); `daf_accounts`; `avg_account_size` (USD, as printed); `payout_rate_pct` (percent, as printed); `sponsors_in_analysis`, `sponsors`, `national_sponsors`, `community_foundations`, `single_issue_sponsors` |
| `value`, `unit` | NPT and DAFRC $-billion figures are converted to USD, e.g. 54.77 becomes 54,770,000,000 ([NPT 2024 DAF Report](https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/)), so precision is $10m |
| `sponsor_universe` | Sponsor file or universe behind the value |
| `notes` | Table or figure reference, plus any caveat |

### 2.2 `dafrc-sponsor-schedule-d-fy2019-2024.csv`
These are the DAFRC dictionary columns, unchanged: `ein`, `fiscal_year_end` (the Form 990 year label), `end_of_tax_period`, `name`, `number_of_daf_accounts` (Sch D I-1), `total_daf_contributions` (I-2), `total_daf_grants` (I-3), `eoy_daf_assets` (I-4). Each value also has a `source_*` column taking the value IRS 990, Imputed, NPT historical data or paper submission. The remaining columns are `operating_status`, `vetted_status`, `type` (National / Community Foundation / Single Issue Charity) and `subtype` (Standard, Donation Processor, Community, Religiously-Affiliated, Universities and Healthcare, Other). I added `dataset_edition` and `source_url`. The EIN is zero-padded to 9 characters.

### 2.3 `sponsor-level-metrics.csv`
| Column | Meaning |
|---|---|
| `sponsor`, `ein` | Display name and 9-digit EIN. DAFgiving360 = 31-1640316 (legal name "Donor Advised Charitable Giving Inc"). GS Philanthropy Fund = 31-1774905. MS GIFT = 52-7082731. NPT = 23-7825575. |
| `fiscal_year`, `period_end`, `period_basis` | `form990_tax_year_DAFRC_label`; `form990_tax_period_end_month` (ProPublica `tax_prd`); `calendar_year_self_report`; `fiscal_year_self_report`; `point_in_time_self_report`; `form990_*` |
| `metric` | DAFRC: `daf_accounts_eoy`, `daf_contributions`, `daf_grants`, `daf_assets_eoy`. ProPublica: `form990_total_contributions_gifts_grants`, `form990_total_revenue`, `form990_total_functional_expenses`, `form990_total_assets_eoy`, all whole-organisation and not DAF-only. Self-reports: `grants_paid`, `grant_count`, `median_grant`, `donors`, `charities_supported`, `daf_assets`, … |
| `value_qualifier` | `exact`, `rounded`, `lower_bound` (for "more than X"), `approximate`, `missing` |
| `data_source_type` | `dafrc_schedule_d_dataset`, `propublica_form990_extract`, `sponsor_self_report`, `form990_other` |
| `value_provenance` | Filed, imputed, self-reported, etc. |
| `notes` | Caveats and conflicts. Two examples: NPT FY2025 grants are $6.44b in the annual report ([NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)) but $6.61b in the press release ([NonProfit Times on NPT release](https://thenonprofittimes.com/?p=215695)), and DAFgiving360 FY2026 grants are ">$10b" in the release ([DAFgiving360 FY2026 release](https://www.dafgiving360.org/press-release/fiscal-year-2026-results)) but $10.85b on the homepage ([DAFgiving360](https://www.dafgiving360.org/)). |

### 2.4 `sponsor-fee-schedules.csv`
| Column | Meaning |
|---|---|
| `fee_component` | `admin_fee_tier`, `min_annual_admin_fee`, `min_initial_contribution`, `min_grant`, `investment_expense_range`, `investment_management_fee`, `investment_expense_example`, `subscription_fee`, `grant_processing_fee` |
| `tier_lower_usd`, `tier_upper_usd` | Balance band. For Daffy, `tier_upper_usd` is the cap on annualized contributions, not on balance. |
| `rate_pct` / `flat_amount_usd` | Percentage rate or dollar amount. Ranges are stored as text, e.g. "0.015-0.93". |
| `fee_basis` | **This determines how to compute the fee.** `marginal_tier…` (Fidelity, DAFgiving360, RCF) applies each rate only to the slice of balance in its band. `tiered_weighted…` (Vanguard) works the same way. **BofA is `flat_rate_applied_to_first_dollar_by_band`**: the band's rate applies to the whole balance. `monthly_flat_membership` (Daffy). |
| `source_type`, `retrieved`, `as_of_note` | Official page or PDF, search snippet, third party or repo prior review, plus the retrieval date |

### 2.5 `company-funding.csv`
The columns are `company`, `role_in_daf_ecosystem`, `transaction_date`, `transaction_type` (seed / series_x / growth_equity / buyout / acquisition / option_or_warrant), `amount_usd`, `amount_status`, `lead_investors_or_acquirer`, `other_investors`, `post_money_valuation_usd`, `source_type`, `source_url` and `notes`. `amount_status` takes the values disclosed, undisclosed, company_self_reported, secondary, aggregator_unverified or not_found.

### 2.6 `derived-metrics.csv`
The columns are `metric_id`, `computation`, `entity`, `ein`, `fiscal_year`, `value`, `unit`, `numerator`, `denominator`, `coverage_share`, `check_status`, `definition` and `inputs`.

| `computation` | What it is |
|---|---|
| `yoy_growth` | Within one `series_id` only. NPT has two variants: a headline chain across editions (unrevised, flagged) and a within-edition comparison of the current year with the revised prior year. |
| `cagr` | First to last FY within one series |
| `recompute_total` | Sum of DAFRC sponsor rows compared with the published total. All 21 checks match. |
| `coverage_share` | Share of each DAFRC total that comes from filed values rather than imputed ones |
| `payout_ratio` | Market and sponsor level. Beginning-assets definition: grants_t / assets_{t−1}. Average-assets definition: grants_t / mean(assets_{t−1}, assets_t); for sponsor rows this value is stored in `coverage_share`. |
| `payout_distribution_across_sponsors` | P25, median, P75 and share below 5% of sponsor-level payout, filed values only (`data/mission-2026-11-14/derived-metrics.csv`). This is a distribution across sponsors, not across accounts. |
| `sponsor_share_of_market` | Named sponsor value divided by the DAFRC total for the same FY label. **The value is left blank when periods do not match**, e.g. a CY2025 self-report against the FY2024 total. `check_status` records the match result. |
| `concentration` | CR1, CR3, CR5, CR10 and HHI (0–10,000) of sponsor assets, grants, contributions and accounts. Each is computed three ways: all rows, filed-only, and national-only. `coverage_share` gives the share of the DAFRC total that is covered. |
| `segment_share` | Share by DAFRC type and national subtype |
| `cross_publisher_ratio` | DAFRC divided by NPT for the same FY. Flagged `DIFFERENT_UNIVERSES_do_not_splice`. |
| `cross_source_ratio` | DAFRC Schedule D value divided by the ProPublica whole-organisation Form 990 value |

## 3. Normalization assumptions and incompatibilities

1. **NPT and DAFRC are separate series.** NPT stopped publishing after its 2024 edition (FY2023; [NPT 2024 DAF Report](https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/)), and DAFRC took over in 2025 ([DAFRC Annual DAF Report, Dec 2025](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-DAF-Research-Collaborative.pdf)). They overlap for FY2020–FY2023. Dollar totals agree within about 2%: DAFRC/NPT assets run 1.003–1.019, grants 0.996–1.001 and contributions 0.988–1.007, except FY2023 contributions at 1.10 (`cross_publisher_ratio` rows in `data/mission-2026-11-14/derived-metrics.csv`). **Account counts do not agree.** DAFRC/NPT accounts are 1.55× in FY2020, 1.84× in FY2022 and 1.70× in FY2023, because DAFRC counts donation-processor accounts (Givinga, American Online Giving Foundation, PayPal Giving Fund) and NPT's file evidently did not to the same degree. Normalization rule: do not splice the two account series or the two average-account-size series. Dollar series can be shown side by side, but if a chained series is needed, link at FY2020 using the ratio in `RATIO_DAFRC_TO_NPT_*` and say so explicitly. No spliced series is published here.
2. **Vintages.** Each NPT edition revises the prior year, sometimes heavily. NPT's FY2022 accounts were 1,948,545 in the 2023 edition ([NPT 2023 DAF Report](https://www.nptrust.org/2023-daf-report/)) and 1,771,709 in the 2024 edition ([NPT 2024 DAF Report](https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/)). FY2022 contributions moved from $85.53b to $75.94b. Use `NPT_DAFR_REVISED_PRIOR` when it exists, or within-edition YoY. DAFRC FY2024 contributions were $89.64b initially ([DAFRC Annual DAF Report, Dec 2025](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-DAF-Research-Collaborative.pdf)) and $90.57b after the update ([DAFRC updated memo, Apr 2026](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)). Urban Institute's $89.6b ([Urban giving dashboard](https://apps.urban.org/features/giving-dashboard/)) matches the initial vintage.
3. **Fiscal versus calendar year.** Both publishers label a year by the Form 990 tax year, so "FY2023" covers periods from as early as 2022-03-01 to as late as 2023-12-31 ([DAFRC updated memo, Apr 2026](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); `end_of_tax_period` in [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Fidelity, NPT, Vanguard and DAFgiving360 use June fiscal year-ends. Their FY2024 is July 2023 to June 2024 ([Fidelity Charitable FY2025 audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)). Sponsor self-reports are often calendar-year (Fidelity CY2025, Vanguard CY2025, Daffy) and are **never** divided by DAFRC totals. The script blanks those rows and sets `period_definition_mismatch_calendar_vs_990_FY`.
4. **DAFRC FY2024 is about 30% imputed.** Filed values make up 70.2% of FY2024 assets, 68.1% of grants and 74.3% of accounts (`coverage_share` in `data/mission-2026-11-14/derived-metrics.csv`; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). FY2023 filed coverage is 99.8%. In FY2024 several large sponsors are imputed: GS Philanthropy Fund, AEF, MS GIFT, BofA, NCF, RCF and Daffy. RCF's imputed FY2024 count of 22,366 accounts ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) sits beside an actual 25,824 ([RCF FY2024 audit](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)). Fidelity's FY2024 row comes from a "paper submission" whose `end_of_tax_period` field still reads 2023-06-30. That label lag is flagged.
5. **Payout definitions.** The published DAFRC and NPT payout is aggregate grants_t / assets_{t−1} ([DAFRC updated memo, Apr 2026](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)). That is not the median account payout (about 9% over 3 years, repo M12; [DAFRC National Study](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf)) or the median sponsor payout (about 12%, below). In a high-inflow year the average-assets variant comes out lower: 22.1% versus 25.2% for FY2024 (`data/mission-2026-11-14/derived-metrics.csv`).
6. **Sponsor-level versus account-level.** Every payout in this pack is at sponsor level. Sponsor P25–P75 cannot be read as account behaviour, because each sponsor's ratio is weighted toward its large accounts.
7. **Schedule D versus Form 990 totals.** For the large national sponsors, Schedule D contributions are within about 0.3% of total Form 990 contributions (ImpactAssets FY2022: +3%) (`cross_source_ratio` in `data/mission-2026-11-14/derived-metrics.csv`; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); [ProPublica Nonprofit Explorer API](https://projects.propublica.org/nonprofits/api/v2/organizations/110303001.json)). DAF assets are 92–99.5% of total assets (BofA about 92%; Fidelity, Vanguard and Ayco about 98–99%). Community foundations hold much more non-DAF money: SVCF's DAF assets are 72–86% of its total assets. NPT's FY2023 DAF assets are 81% of total, so NPT also holds non-DAF vehicles. Whole-organisation 990 totals are not a stand-in for DAF activity at community foundations or multi-vehicle sponsors.
8. **Self-reports.** Lower bounds ("more than") are stored as the bound with `value_qualifier=lower_bound`. Rounded figures are tagged as rounded. None of these values is audited.

## 4. Key quantitative findings (with caveats)

**Market growth**
- DAFRC updated figures for FY2020→FY2024: assets $168.76b→$327.87b (CAGR 18.1%), grants $35.54b→$64.60b (16.1%), contributions $49.50b→$90.57b (16.3%), accounts 1.57m→3.59m (23.0%, driven by donation processors). FY2024 YoY was +38.6% for contributions, +17.9% for grants and +27.9% for assets. FY2022 and FY2023 contributions fell 1.3% and 14.6%. *Source: DAFRC 2025 Updated Analysis memo ([DAFRC updated memo, Apr 2026](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)); recomputed exactly from the DAFRC dataset ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); `data/mission-2026-11-14/derived-metrics.csv`).*
- NPT headline estimates for FY2014→FY2023: grants $12.49b→$54.77b (CAGR 17.9%), assets $70.70b→$251.52b (15.1%). These chain first estimates across editions. FY2023 contributions fell 21.7% within the 2024 edition. *Source: NPT DAF Reports 2015–2024, Table 1 ([NPT 2015 DAF Report](https://www.nptrust.org/2015-donor-advised-fund-report-npt/) … [NPT 2024 DAF Report](https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/); all editions listed in `data/mission-2026-11-14/daf-market-annual-series.csv`).*

**Concentration** (DAFRC sponsor dataset; HHI in points)
- FY2023 assets (99.8% filed): CR3 42.9%, CR5 52.9%, HHI 800, across 1,482 sponsors (`data/mission-2026-11-14/derived-metrics.csv`; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). The top four are Fidelity, DAFgiving360, NPT and Vanguard.
- FY2024 assets, all rows: CR1 20.2% (Fidelity), CR3 45.5%, CR5 55.8%, CR10 67.9%, HHI 830 (`data/mission-2026-11-14/derived-metrics.csv`; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Among national sponsors only: CR3 63.2%, HHI 1,566. Concentration has risen since FY2019, when CR3 was 40.9% and HHI 817. The filed-only FY2024 figures (CR3 64.9%) overstate concentration because the imputed small sponsors drop out, so do not quote them as market concentration.
- Accounts are far more concentrated than assets (FY2023 account HHI 2,034), but this reflects donation processors. They hold 79.5% of FY2024 accounts and 0.9% of assets. Standard national sponsors hold 71.1% of assets and 14.4% of accounts. Community foundations hold 20.2% of assets (`data/mission-2026-11-14/derived-metrics.csv`; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
- Year-matched FY2024 asset shares: Fidelity 20.2%, NPT 12.8%, DAFgiving360 12.5%, Vanguard 6.7%, then GS PF 3.6%, SVCF 2.9%, AEF 2.9% and MS GIFT 2.9%, the last three imputed or label-lagged (`data/mission-2026-11-14/derived-metrics.csv`; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).

**Payout distribution**
- Market (beginning assets): 26.8%, 28.4%, 23.7%, 23.8% and 25.2% for FY2020–FY2024 ([DAFRC updated memo, Apr 2026](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); `data/mission-2026-11-14/derived-metrics.csv`). The average-assets version is 22–24%.
- Across sponsors with at least $1m of prior DAF assets and filed values (n=529–973 per year), the median sponsor payout is 10.7–12.5%, P25 is about 5.2–6.0% and P75 about 19–22%. **19–24% of these sponsors pay out under 5%.** Sponsors with at least $1bn have a median of 21–24% and almost none below 5%. Payout is high in aggregate because the largest national sponsors dominate the totals (`data/mission-2026-11-14/derived-metrics.csv`; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
- Named sponsors, FY2024 beginning-assets payout: Fidelity 22.8%, DAFgiving360 21.0%, NPT 24.4%, Vanguard 18.2%, JCF 37.7%, SVCF 41.0%. The NCF figure (47.6%) is imputed (`data/mission-2026-11-14/derived-metrics.csv`; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).

**Fees (as of 2026)** (`data/mission-2026-11-14/sponsor-fee-schedules.csv`)
Fidelity ([fees](https://www.fidelitycharitable.org/giving-account/what-it-costs.html)), DAFgiving360 ([fees](https://www.dafgiving360.org/features/fees-and-minimums)) and the Charityvest invested account ([fees](https://pcadafguide.foundationsource.com/how-client-fees-work)) all start at 0.60% on the first $500k, with tiered marginal rates after that. The minimum annual fee is $100 at Fidelity and Charityvest. RCF/Ren charges 0.65% with a $250 minimum ([RCF](https://renaissancecharitable.org/advisor-managed-dafs/)). BofA CGF charges 0.90% on balances up to $100k, applied flat to the first dollar, plus 0.12% investment management ([BofA fee schedule](https://www.bankofamerica.com/content/documents/philanthropic/cgf_fee_schedule.pdf)). Vanguard Premier drops to 0.12% above $1m ([Vanguard Charitable](https://www.vanguardcharitable.org/fees-and-expenses)). Daffy charges flat memberships of $0, $3, $5, $20 and $40 per month ([Daffy help](https://help.daffy.org/en/articles/6323771-what-are-daffy-s-membership-fees)). NPT, MS GIFT, GS PF and AEF do not publish admin schedules (blank). Minimum initial contributions: $0 (Fidelity), $10k (NPT, [NPT FAQ](https://www.nptrust.org/?p=206)), $25k (BofA, MS GIFT, GS PF, and Vanguard per third parties, e.g. [Morningstar](https://www.morningstar.com/personal-finance/our-take-vanguards-charitable-endowment-program)).

**Company funding**
Disclosed rounds are small next to sponsor assets (`data/mission-2026-11-14/company-funding.csv`): Daffy $4.8m seed ([Daffy](https://www.daffy.org/answers/how-much-did-daffy-raise-in-their-series-a-funding-round-and-who-backed-it)) and $17.1m Series A ([Business Wire](https://www.businesswire.com/news/home/20220208005152/en)); Chariot $11m Series A ([Chariot](https://givechariot.com/resources/insights/chariot-announces-11-million-series-a-investment-round-led-by-maveron)); Groundswell $15m seed ([Business Wire](https://www.businesswire.com/news/home/20211130005365/en/Groundswell-Announces-A-Total-of-15M-in-Seed-Funding-To-Democratize-Philanthropy)); Charityvest $2.2m seed ([Hypepotamus](https://www.hypepotamus.com/charityvest-seed-round-2022/)); Givefront $2m seed ([TechCrunch](https://techcrunch.com/2025/12/18/these-21-year-old-dropouts-raised-2m-to-build-givefront-a-fintech-for-nonprofits/)). TIFIN raised $109m at an $842m valuation, but at company level ([TechCrunch](https://techcrunch.com/2022/05/12/data-driven-fintech-tifin-valued-at-842m-in-new-109m-series-d-round)). Ren (Bain 2023, [Bain Capital](https://www.baincapital.com/news/ren-secures-strategic-growth-investment-led-bain-capital-tech-opportunities); Great Hill 2025, [Business Wire](https://www.businesswire.com/news/home/20251028702541/en/Great-Hill-Partners-Announces-Strategic-Growth-Investment-in-Philanthropy-Tech-Platform-Ren)) and Foundation Source (GTCR 2023, [Foundation Source](https://foundationsource.com/newsroom/press-releases/gtcr-announces-acquisition-of-foundation-source/)) are private-equity owned with undisclosed terms. Ren claims "> $175b in charitable funding" ([Ren giving platform](https://www.reninc.com/giving-platform/)), about half of US DAF assets ([DAFRC updated memo, Apr 2026](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)). That is a vendor claim. The repo's audited RCF fee data shows that administered assets are not the same as Ren's revenue.

## 5. Grant processing and AI-adoption evidence (self-reported only)

| Sponsor | Period | Grant count | Other operational metric | Qualifier |
|---|---|---|---|---|
| Fidelity Charitable | CY2025 | ~3,000,000 | $18.25b grants; 226,823 charities | rounded, self-reported ([2026 Giving Report](https://www.fidelitycharitable.org/insights/2026-giving-report.html)) |
| DAFgiving360 | FY ended 2026-06 | >1,600,000 | >4,300 grants/day; median grant $500 | lower bound, self-reported ([DAFgiving360 FY2026 release](https://www.dafgiving360.org/press-release/fiscal-year-2026-results)) |
| Vanguard Charitable | CY2025 | 267,838 | ~67,000 nonprofits | self-reported ([2025 annual report](https://www.vanguardcharitable.org/2025annualreport); [NonProfit Times](https://thenonprofittimes.com/npt_articles/vanguard-daf-granted-3-9-billion-for-2025/)) |
| NPT | FY ended 2025-06 | 159,543 | 20,561 accounts | self-reported ([NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)) |
| Charityvest | CY2025 | 48,744 | $119.2m grants | self-reported ([Foundation Source release](https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/)) |
| GS Philanthropy Fund | CY2023 | ~24,800 | ~$2.14b grants | Form 990 narrative via aggregator ([Cause IQ](https://www.causeiq.com/organizations/goldman-sachs-philanthropy-fund,311774905/)) |
| GiveClear | 2025 | 16,249 (repo U26) | $83.2m grants | self-reported ([GiveClear reports](https://www.giveclear.org/reports-and-financials)) |

No sponsor publishes a grant turnaround time or processing SLA in the sources reviewed, so none is recorded. Published AI-adoption evidence is limited to the DAFRC manager survey already in the repo (M19: 61% self-rate IT capacity as sufficient; [DAFRC manager survey](https://static1.squarespace.com/static/6011def87418a462fcb03978/t/67d88760d1a3881c88fc3b12/1742243688227/The%2BNational%2BSurvey%2Bof%2BDonor%2BAdvised%2BFund%2BManagers.pdf)). No sponsor-level AI-usage metric was found.

## 6. Gaps

- No current published admin fee schedule was found for NPT, MS GIFT, GS PF, AEF or NCF (only the $30/month minimum for NCF, [NCF fees](https://www.ncfgiving.com/fees/)). DAFgiving360's page blocks automated fetch, so its 0.15% tier breakpoints are unverified ([DAFgiving360 fees](https://www.dafgiving360.org/features/fees-and-minimums)). Vanguard's minimums come from third parties ([Morningstar](https://www.morningstar.com/personal-finance/our-take-vanguards-charitable-endowment-program)).
- DAFRC FY2024 sponsor values are imputed for many large sponsors. FY2025 Form 990 Schedule D data is not yet public, and the GivingTuesday data mart is "coming soon".
- ProPublica extracted financials lag (latest is FY2023 for most sponsors), and they report no DAF-only grants.
- "Pave" could not be identified as a DAF-ecosystem company; the search found only unrelated firms with that name, so no row was added. No disclosed funding was found for GivingIQ (row left blank). TIFIN Give has no segment-level disclosures.
- NPT's FY2025 grants conflict between $6.44b ([NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)) and $6.61b ([NonProfit Times on NPT release](https://thenonprofittimes.com/?p=215695)). Daffy's 2026 figures come via a secondary outlet.
- There is no sponsor-level evidence on account-level payout. Use the repo's DAFRC National Study (M10–M15).

## Red-team corrections (wave 2B, 2026-11-14) — governing
- **§4 / §6, NPT.** Replace "NPT's FY2025 grants conflict between $6.44b and $6.61b" with "NPT FY2025 grants: $6.44b for the U.S. DAF program only (annual report); $6.61b in the Dec-2025 release likely includes NPT UK/Transatlantic (inferred). Use $6.44b." ([NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/); [NonProfit Times on NPT release](https://thenonprofittimes.com/?p=215695))
- **§3.** Add: "Never divide June-2025 sponsor values by the DAFRC FY2024 total; DAFRC FY2024 = period ending June 2024 for June-FYE sponsors (verified against the Fidelity and Vanguard audits)." ([Fidelity Charitable FY2025 audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf))
