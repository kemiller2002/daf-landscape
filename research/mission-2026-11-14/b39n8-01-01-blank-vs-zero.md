# P-B39N8-01-01: blank vs zero 'Grants from DAFs' in IPS's FY2023 sponsor list

**Date:** 2026-11-20 · **Queue item:** P-B39N8-01-01, a follow-up to [b39n8-01-payout-definition-bridge.md](b39n8-01-payout-definition-bridge.md) §3.2.

**Outputs**
- [`data/mission-2026-11-14/blank-vs-zero-daf-grants-2026-11-20.csv`](../../data/mission-2026-11-14/blank-vs-zero-daf-grants-2026-11-20.csv): 386 rows, one per sponsor and population. 248 rows are the IPS blank-grants sponsors. 138 rows are the repo panel's FY2023 zero-grant sponsor-years, a secondary check. The data dictionary is in §6.
- [`scripts/mission_blank_vs_zero.py`](../../scripts/mission_blank_vs_zero.py): stdlib only, functional style. It reuses `mission_990_contractors` (IRS index loader, return selection, streamed Schedule D extract) and `mission_payout_bridge` (IPS xlsx reader, IPS screens, corrected panel, median) unchanged. The scenario medians in §3 are printed as JSON on stdout.
- [`data/mission-2026-11-14/queue-proposals-b39n8-01-01.csv`](../../data/mission-2026-11-14/queue-proposals-b39n8-01-01.csv): 5 proposals.

Evidence tags: [F] computed here from filed or IPS data, [Q] quoted from a primary source, [I] inference.

## 0. Headline answers

| Question | Answer |
|---|---|
| What do the 248 blank IPS cells look like on the filed return? | **All 248 are blank-filed** [F]. The same-period Form 990, as processed by the IRS by 2024, has a Schedule D whose Part I line 3(a) element (`DonorAdvisedFundsGrantsAmt`) is absent. Zero are zero-filed, zero are non-zero and zero have no return. Every one of the 248 matched on tax period (IPS fiscal year and month = `TAX_PERIOD`). On all 248, filed lines 1(a) and 4(a) equal IPS's 'DAF Accounts' and 'DAF Assets' cells, which confirms they are the same returns IPS read. |
| How much does the 9.7% median move with filed values? | **0.00 points.** No blank cell becomes a filed number, so IPS's formula on filed values gives 9.6751% (n = 1,487), exactly IPS's own rates. The published value is 0.0968 [F]. The repo's formulas don't move either: (a) beginning assets 12.19% (n = 1,365); (b) IRS formula 9.68%, 9.66% excluding processors, 10.04% at ≥ $1m. Every shift is 0.0000 [F]. |
| What about later (amended or late) returns? | 2 of the 248 have a newer same-period return processed after IPS's 31 January 2025 download. One, The Prosperity Foundation (EIN 47-4364468), amended in 2025 from blank to **$550,000** of DAF grants. On the newest returns the median is 9.6754% (n = 1,488), a shift of **+0.0003 points** [F]. |
| Is IPS's blank-cell exclusion the binding choice? | Yes. Counting the 248 blank-filed sponsors at 0% gives 7.72% (−1.95 points) on the IRS formula and 10.02% (−2.17 points vs 12.19%) on beginning assets [F]. Whether blank means zero cannot be read from Schedule D: 127 of 197 blank-filed sponsors with prior-year assets have a roll-forward with no room for outflow, but 55 have an implied outflow above 10% of prior assets (§3.5) [F]/[I]. |
| What does this mean for the repo panel? | DAFRC records **0** for 86 FY2023 sponsor-years whose line 3(a) is filed blank, and 52 that are truly zero-filed. Applying IPS's rule with filed evidence (drop the 81 blank-filed with assets > 0, keep the 51 zero-filed) moves the repo median from **9.33% to 9.86%**. The bridge's 9.33–10.20% bracket becomes a single number, 0.18 points above IPS's 9.68% instead of 0.35 below [F]. |

## 1. Question and inputs

The bridge (§3.2) found that IPS's FY2023 sponsor list has 1,735 sponsors but rates for only 1,487. The 248 without a rate have a blank 'Grants from DAFs' cell: 216 single-issue, 31 CF and 1 national (DonateStock Charitable Inc). Counting them as 0% gives 7.72%. The open question was whether the blank cells reflect filed blanks, filed zeros or missing data.

Inputs:
- the IPS sponsor list and summary table, reused from the bridge's download (inequality.org; the robots.txt check is logged in the bridge §7);
- the IRS TEOS indexes `index_2023.csv` to `index_2026.csv`, reused from the repo's scratch IRS cache;
- `extract990/{oid}.json` Schedule D extracts, reused from the repo's earlier harvests;
- the corrected DAFRC panel (R1–R4), rebuilt with `mission_payout_bridge.corrected_panel`.

## 2. Method

1. **Universe.** Take every FY2023 IPS row with `Grants from DAFs == ""`: 248 rows. As a secondary check, take every FY2023 sponsor-year of the corrected repo panel with DAF grants = 0: 138 rows, 132 of them with assets > 0, which is the bridge's zero-grant set.
2. **Return selection.** Search the IRS TEOS index rows (2023–2026) for each EIN. The target tax period is IPS's 'Fiscal Year End' plus 'Fiscal Month End' (e.g. 202306).
   - The primary return is the newest Form 990 object for that exact period with an OBJECT_ID processing year ≤ 2024. IPS downloaded IRS data on 31 January 2025 (bridge §3.2), so this is the vintage IPS could have used.
   - The newest same-period object in the 2026 index is read as well (`latest_*` columns).
   - Repo-panel rows not on IPS's list have no target month, so they fall back to the newest 990 whose period ends in 2023.
   - The prior-year (FY2022) 990 is selected the same way, for line 4(a) as beginning assets.
3. **Extraction.** Read the Schedule D Part I column (a) elements from the e-file XML with `mission_990_contractors.extract_stream`. An absent element becomes `None` and a filed `0` becomes `0.0`.
   - Line 1(a): `DonorAdvisedFundsHeldCnt`
   - Line 2(a): `DonorAdvisedFundsContriAmt`
   - Line 3(a): `DonorAdvisedFundsGrantsAmt`
   - Line 4(a): `DonorAdvisedFundsVlEOYAmt`

   Of 570 object ids, 536 came from existing caches and 34 were fetched from the GivingTuesday 990 data-lake mirror. Four XMLs were also fetched raw and checked by hand (§7).
4. **Classification** of the primary return:

   | Class | Rule |
   |---|---|
   | `blank-filed` | Return found, line 3(a) element absent |
   | `zero-filed` | Element present and equal to 0 |
   | `non-zero` | Element present and > 0 |
   | `no-return-found` | No same-FY Form 990 in the index, or the XML could not be read |

   As a check, filed lines 1(a) and 4(a) are compared with IPS's accounts and assets cells (tolerance: $1 or 0.5%).
5. **Medians** (FY2023, by scenario; §3.1). IPS's 1,487 rates are always kept. Filed values are added for zero-filed and non-zero sponsors. Blank-filed and no-return sponsors stay out under IPS's rule, or are counted at 0% in the counterfactual scenarios. The formulas:
   - IPS = repo (b) `irs`: grants_t ÷ (DAF assets_t + grants_t). Run on all sponsors, excluding IPS 'Donation Processor', and at assets_t + grants_t ≥ $1m.
   - Repo (a) `beg`: grants_t ÷ DAF assets_{t−1}. Prior assets come from IPS's FY2022 sheet, or else from filed FY2022 line 4(a).
   - Repo panel, IRS formula, assets > 0, with the zero-grant sponsor-years split by filed class.

## 3. Results

### 3.1 Median payout, FY2023

| Scenario | Formula, sample | n | Median | Shift vs IPS own rates (pts) |
|---|---|---|---|---|
| S0 IPS's own 'Average DAF Payout' | irs, all | 1,487 | 9.6751% | 0 |
| S1 filed line 3(a), IPS assets (blank-filed stay out) | irs, all | 1,487 | 9.6751% | 0.0000 |
| S2 filed line 3(a), filed line 4(a) | irs, all | 1,487 | 9.6751% | 0.0000 |
| S3 S1 + IPS deficiency screens on added rows | irs, all | 1,487 | 9.6751% | 0.0000 |
| S6 newest same-period returns (post-IPS amendments) | irs, all | 1,488 | 9.6754% | +0.0003 |
| S4 S1 + blank-filed counted as 0% | irs, all | 1,735 | 7.7223% | −1.9528 |
| S5 all 248 blanks as 0% (bridge counterfactual) | irs, all | 1,735 | 7.7223% | −1.9528 |
| S0 / S1 excluding donation processors | irs, ex_proc | 1,477 / 1,477 | 9.6563% / 9.6563% | 0.0000 |
| S0 / S1, assets_t + grants_t ≥ $1m | irs, ge1m | 1,036 / 1,036 | 10.0359% / 10.0359% | 0.0000 |
| S0 IPS grants ÷ IPS FY2022 assets | beg, all | 1,365 | 12.1891% | 0 |
| S1 + filed line 3(a) | beg, all | 1,365 | 12.1891% | 0.0000 |
| S4 + blank-filed as 0% (where prior assets > 0) | beg, all | 1,562 | 10.0188% | −2.1703 |
| P0 repo panel, assets > 0, zeros kept (bridge 9.33%) | irs, repo panel | 1,481 | 9.3297% | 0 |
| P1 repo panel, all zero-grant years dropped (bound) | irs, repo panel | 1,349 | 10.1929% | +0.8632 |
| **P2 repo panel, blank-filed zero years dropped (IPS rule)** | irs, repo panel | 1,400 | **9.8587%** | +0.5290 |
| P3 P2 + no-return zero years dropped | irs, repo panel | 1,400 | 9.8587% | +0.5290 |

All values are [F]. IPS's published Summary Table value is 0.0968 [Q], which is S0 rounded. S0 is 0.0049 points below the rounded figure, so the "vs published" column in the script output differs by that constant. P1 has no IPS screens; the bridge's screened version is 10.20%.

**How much does the 9.7% median move?** Not at all on the returns IPS could have read (0.0000 points), and +0.0003 points on today's newest returns [F]. IPS's blank cells copy the filed element faithfully. The only lever on the median is the decision to exclude blank-filed sponsors rather than count them at zero: a 1.95-point swing on IPS's formula.

### 3.2 Classification of the 248

| | Blank-filed | Zero-filed | Non-zero | No return |
|---|---|---|---|---|
| Primary return (processed by 2024) | **248** | 0 | 0 | 0 |
| Newest same-period return (2026 index) | 247 | 0 | 1 | 0 |

- **By type:** 216 single-issue, 31 CF, 1 national; all are blank-filed [F].
- **Size:** 1,896 DAF accounts and $300.3m of DAF assets in total; median $148,679 (IPS cells) [F]. The largest are:
  - Foundation for Advanced Philanthropy, $132.4m;
  - Catholic Foundation of Greater Philadelphia, $30.1m;
  - Oregon Trail Community Foundation, $7.6m.
- **Filing year:** 211 returns were processed in 2024 and 37 in 2023 (OBJECT_ID prefix). All have a Schedule D [F].
- **Line 2(a):** 148 of the 248 also have a blank line 2(a), and IPS's 'Contributions to DAFs' cell is blank for the same 148 [F].
- **Newer same-period returns:** 2 of the 248 have one.
  - The Prosperity Foundation: amended return 202521259349300817 reports 3(a) = $550,000. It is IRS-formula 60.9% on IPS assets. The repo panel already carries $550,000.
  - Avenues Early Childhood Services: a 2026 re-filing with line 3(a) still blank.

### 3.3 Does IPS distinguish blank from zero the way the filing does?

Yes, on every case checked [F]:
- 248 of 248 blank IPS cells are blank-filed.
- 49 of 49 explicit IPS zeros that are also in the repo's zero-grant set are zero-filed.

IPS's other 51 explicit zeros were read in validation. All 51 are zero-filed, so 100 of 100 explicit IPS zeros carry a filed 0 (proposal -02 answered). [V wave 45A] DAFRC does not make the distinction: its panel has 0 for both [F].

### 3.4 Repo panel's FY2023 zero-grant sponsor-years (138)

| | Blank-filed | Zero-filed |
|---|---|---|
| IPS cell blank | 78 | 0 |
| IPS cell = 0 | 0 | 49 |
| Not on IPS list | 8 | 3 |
| **Total** | **86** (81 with assets > 0) | **52** (51 with assets > 0) |

1 of the 86 has DAFRC-imputed grants; the other 137 are DAFRC "filed" values [F]. The bridge's "79 repo sponsor-years with a blank IPS cell" are these 78 plus The Prosperity Foundation, whose panel value comes from the 2025 amendment. P2 in §3.1 drops the 81 blank-filed sponsor-years with assets > 0.

### 3.5 Is a blank line 3(a) a zero? (descriptive only)

Schedule D does not say. As a plausibility screen, the roll-forward implied outflow = assets_{t−1} + line 2(a) − line 4(a), with a blank 2(a) read as 0 and investment return ignored. For the 197 blank-filed sponsors with prior assets > 0 [F]:
- 127 have an implied outflow ≤ 0, compatible with no grants; 35 of them are exactly 0, and 28 report identical assets in both years;
- 55 have an implied outflow above 10% of prior assets;
- the median implied outflow is 0.0% of prior assets.

This screen cannot show that blank means zero. It ignores investment return, and most FY2023 periods had positive market returns [I], so a fund whose grants roughly offset its gains also shows an outflow ≤ 0. An outflow ≤ 0 is necessary for zero grants, not sufficient. The 35 exact zeros and 28 identical year-on-year asset values look more like stale entries than evidence of no grants [I]. [V wave 45A] The 55 could reflect grants, fees, transfers or investment losses; 2022–23 market moves alone cannot be separated with these fields. This is why S4/S5 (7.72%) is a lower bound, not a corrected estimate [I].

## 4. Limits

- **Blank ≠ zero is not resolved.** The task's question (what is filed) is answered; whether blank-filed sponsors actually made DAF grants is not (§3.5; proposal -04).
- **Vintage rule is approximate.** "Processed by 2024" uses the OBJECT_ID year prefix. IPS's exact cut-off was 31 January 2025, and IPS's data source (IRS e-file bulk XML) may have lagged. All 248 primary returns are 2023/2024 objects, so the rule does not affect any classification.
- **IPS's FY2023 universe only.** FY2020–22 blanks (150, 186 and 212) were not read (proposal -01). IPS's 1,487 rated sponsors were not re-read; their rates are taken as published, and the bridge verified them to within 5e-12 of grants ÷ (assets + grants).
- **IPS-only screens.** The 501(c)(3), total-grants and submission-date screens cannot be applied from Schedule D. They are irrelevant here because no row was added.
- **Prior-year assets for `beg`.** They come from IPS's FY2022 sheet where present, which mixes IPS FY2022 rows with filed FY2022 line 4(a) for the rest. Only S4(beg) uses the fallback.
- **Mirror.** XML was read from the GivingTuesday data-lake mirror of IRS e-file objects, not from the IRS TEOS zips. The four raw checks (§7) match the extracts. Validation re-read all 248 primary returns as raw XML and got the same classification on every one. [V wave 45A]
- **What blank means in e-file XML.** The 990 e-file format allows both forms. 103 distinct returns read carry an explicit DonorAdvisedFundsGrantsAmt of 0, and MeF accepted 256 without the element, so it is optional. Every one of the 248 blank-filed returns contains other explicit zero-valued elements. An absent element records a preparer or software choice for that line, not a separate fact about grants. The XSD itself was not read. [V wave 45A]

## 5. Reproduce

```
python3 scripts/mission_blank_vs_zero.py . --ips-dir <dir with the two IPS xlsx> --irs-dir <dir with index_2023..2026.csv> \
    --work <cache dir> --reuse-cache <dir with extract990/> [--reuse-cache ...] --fetch
```

Without `--fetch`, only cached extracts are used; on this run, 34 of 570 would be `not_fetched`.

## 6. Data dictionary: `blank-vs-zero-daf-grants-2026-11-20.csv`

| Column | Meaning |
|---|---|
| population | `ips_blank_grants` (the 248) or `repo_panel_zero_grants` (FY2023 corrected-panel sponsor-years with DAF grants = 0). An EIN can appear in both |
| ein, name | 9-digit EIN; IPS sponsor name (panel name for the panel population) |
| ips_sponsor_type, ips_fiscal_year_end, ips_fiscal_month_end | IPS cells (blank if not on IPS list) |
| target_tax_period | YYYYMM from IPS fiscal year and month |
| ips_daf_accounts, ips_daf_assets, ips_contributions | IPS cells as published (blank = blank cell) |
| ips_grants_cell | IPS 'Grants from DAFs': `(blank)`, a value, or `(not on IPS list)` |
| ips_daf_assets_fy2022 | IPS FY2022 'DAF Assets' for the EIN (IPS population only) |
| panel_daf_grants_fy2023, panel_daf_assets_fy2023, panel_grants_imputed | Corrected DAFRC panel values for FY2023 (blank if not in panel) |
| object_id, return_type, tax_period, index_year | Primary return (IRS TEOS index) |
| tax_period_match | `exact` (same YYYYMM) or `same_fy_other_month` |
| n_returns_same_period | Form 990 objects for that period at the vintage limit |
| xml_status | `ok`, an HTTP error, or `no_990_in_index` |
| sched_d_present | 1 if the return has a Schedule D |
| line1a_daf_count, line2a_contributions, line3a_grants, line4a_eoy_value | Schedule D Part I column (a), lines 1–4. Blank = element absent |
| filed_assets_match_ips, filed_accounts_match_ips | 1 if line 4(a) / 1(a) equals the IPS cell (±$1 or 0.5%), 0 if not, blank if either is missing |
| classification | `blank-filed`, `zero-filed`, `non-zero` or `no-return-found` (primary return) |
| return_vintage | `processed_by_2024` (OBJECT_ID prefix ≤ 2024) or `processed_2025_or_later` |
| latest_object_id, latest_classification, latest_line3a_grants | The same, for the newest same-period object in the 2026 index |
| other_forms_same_fy | Non-990 returns (e.g. 990T) with a FY2023 period |
| prior_object_id, prior_line4a_eoy_value | FY2022 Form 990 and its line 4(a) |
| rate_irs_ips_assets | line 3(a) ÷ (IPS DAF assets + line 3(a)); blank if 3(a) is blank |
| rate_irs_filed_assets | line 3(a) ÷ (line 4(a) + line 3(a)) |
| rate_beg | line 3(a) ÷ prior assets (IPS FY2022, else filed FY2022 line 4(a)) |
| ips_screen_deficient | 1 if the IPS Schedule D deficiency screens fail with filed 3(a); blank if 3(a) is blank |
| xml_url | GivingTuesday mirror URL of the primary XML |
| index_url | IRS TEOS index file listing the primary return |
| source | IPS sponsor-list URL or panel source files |

## 7. Source register and robots log

| Source | URL | Use |
|---|---|---|
| IPS sponsor lists (April 2025) | https://inequality.org/wp-content/uploads/2025/04/Independent-DAF-Report-Sponsor-Lists.xlsx | FY2023 and FY2022 sheets |
| IPS summary table | https://inequality.org/wp-content/uploads/2025/04/Independent-DAF-Report-Summary-Table.xlsx | Published median 0.0968 [Q] |
| IPS report (Appendix A method, p.14 median) | https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf | Formula, screens |
| IRS TEOS e-file indexes | https://apps.irs.gov/pub/epostcard/990/xml/2023/index_2023.csv (likewise 2024, 2025, 2026) | Return lookup (cached copies) |
| IRS e-file XML (GivingTuesday data-lake mirror) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | Schedule D Part I |
| Raw check: Foundation for Advanced Philanthropy FY2023 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433199349318978_public.xml | Lines 1, 2, 4 present; 3 absent |
| Raw check: Oregon Trail Community Foundation FY2023 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202412009349300201_public.xml | Lines 1, 2, 4 present; 3 absent |
| Raw check: The Prosperity Foundation FY2023, original | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413209349308606_public.xml | 3 absent |
| Raw check: The Prosperity Foundation FY2023, 2025 amendment | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521259349300817_public.xml | 3 = 550000 |
| IRS Instructions for Schedule D (Form 990) | https://www.irs.gov/instructions/i990sd | Part I line definitions |
| DAFRC 2025 sponsor dataset | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Repo panel (with R1–R4) |

**Robots log (2026-11-20).**
- `gt990datalake-rawdata.s3.amazonaws.com/robots.txt` returned HTTP 404, so no rules apply. 34 extracts and 4 raw XMLs were fetched with UA `research-script/1.0`.
- inequality.org and apps.irs.gov were not contacted in this task. Cached copies were used; inequality.org's robots check is in the bridge §7.
- sec.gov was not used.
