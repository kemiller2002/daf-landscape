# Charity Navigator rating eligibility of top-50 DAF dollars, as of each grant year (P-B40N1202-B43N26-04)

**Date:** 2026-11-20 · **Task ID:** b40n1202-b43n26-04 · **Builds on:** [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md) §1.3, §4.1 and §5 item 7 ("Eligibility is assessed against filings available in November 2026, not at grant time"), and [b40n1202-b43n26-03-non-bmf-recipients.md](b40n1202-b43n26-03-non-bmf-recipients.md) (non-BMF EINs; Chan Zuckerberg LLCs, revised in [validation-wave46a-report.md](validation-wave46a-report.md))

**Outputs**
- Script: [`scripts/mission_cn_eligibility_by_year.py`](../../scripts/mission_cn_eligibility_by_year.py). It is new. It imports `build_numerator`, `cn_filing_test`, `cn_reason`, `per_period`, `load_history`, `load_bmf_extra`, `no_ein_lines` and `DLN_FORM` from `mission_recipient_basis_eligibility.py`, and `load_revocation`, `load_pub78`, `fetch_header` (cache read only) and `fy_bounds` from `mission_non_bmf_recipients.py`. Neither script is modified. It makes no network requests.
- Data: [`data/mission-2026-11-14/cn-eligibility-by-year-2026-11-20.csv`](../../data/mission-2026-11-14/cn-eligibility-by-year-2026-11-20.csv). 391 rows: 218 `share`, 79 `transition`, 94 `sponsor_year_cutoff`. The data dictionary is in §7.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b40n1202-b43n26-04.csv`](../../data/mission-2026-11-14/queue-proposals-b40n1202-b43n26-04.csv) (5 rows).

Tags: [F] computed by the script · [P] quoted primary source · [I] inference or assumption.

## 0. Answer in brief

- **Headline.** Tested against the filings the IRS had processed by the end of each sponsor's fiscal year, **72.66%** of top-50 FY2023–24 DAF-weighted Schedule I dollars went to recipients that were rating-eligible when the grant was made: $53.82bn of $74.07bn [F]. The current-status figure is **76.85%** ($56.93bn), which the script reproduces to six digits (0.768507). Grant-time eligibility is therefore **4.19 points lower** [F].
- **By grant year** [F]:

| Grant year | Dollars, $bn | Current status | As of FY end (headline) | As of FY start | Points lost, FY end vs current |
|---|---|---|---|---|---|
| FY2023 | 34.78 | 73.73% | **68.11%** | 64.75% | −5.62 |
| FY2024 | 39.29 | 79.62% | **76.68%** | 72.44% | −2.94 |
| Both | 74.07 | 76.85% | **72.66%** | 68.83% | −4.19 |

- **Why it falls.** $3.50bn (30,541 recipient × sponsor-year grant units, 15,294 recipients) went to recipients that are eligible now but were not at the end of the grant year. $0.39bn moves the other way [F].
  - Most of the drop is young organisations that had not yet filed three e-filed returns: $2.91bn fails the three-return rule at grant time. A further $0.34bn went to recipients with no e-filed return processed by the cut-off, and $0.22bn to recipients whose latest four returns then held fewer than two full 990s [F].
  - The largest are The 85 Fund ($144.9m; its third e-filed return, for tax year 2022, was processed in November 2023, after the sponsor's 30 June 2023 year end), Just Trust for Education ($126.7m), Our American Future Foundation ($116.5m), City Fund ($50.6m) and the Deitch Family Charitable Support Trust ($49.7m) [F].
  - The gains are $0.20bn to 1,148 EINs that have since left the BMF but are presumed to have been listed 501(c)(3) filers at the time (§1.4, [I]), and $0.17bn to organisations that filed 990s then but have stopped since. Examples are Compassion International ($35.7m; full 990s for tax years 2016–2019, then only 990-T), Biblica ($27.5m), Convoy of Hope ($26.1m) and InterVarsity Christian Fellowship ($15.3m) [F]. All four carry BMF foundation code 10 (church) today, and their last full 990s in the index are for tax periods ending in 2019 (Compassion), 2020 (InterVarsity) and 2021 (Convoy of Hope, Biblica); Compassion, InterVarsity and Convoy of Hope file only 990-T after that [F, TEOS index]. Why they stopped filing 990s is not stated in these files [I].
- **Range.** If grants were made on the first day of the fiscal year, the share is 68.83% (§3.2). Variants of the status reconstruction, the window and the index coverage give 72.36–72.66% (§3.1); a deliberately loose upper bound for missing early index rows gives 74.67%. The gap from current status is robust: no grant-time variant without CZ look-through comes within 2 points of 76.85% [F].
- **Chan Zuckerberg Biohub LLCs** (§4). The four LLCs received $1,594.0m DAF-weighted, all from Silicon Valley Community Foundation in its FY2023 (year end 31 December 2023). That is 2.15% of top-50 dollars [F].
  - The LLCs have no e-filed return, no BMF row and no revocation row, so they are ineligible on both dates under the central rules [F].
  - Their parent, Chan Zuckerberg Biohub Inc (EIN 81-1669175), passed every filing rule at 31 December 2023. It had five full 990s with tax periods in 2017–2022, and its latest return (tax year 2022) was processed on 14 November 2023 [F].
  - With the LLCs looked through to the parent, the grant-time share is **74.81%**, against **79.00%** on current status [F]. Look-through is the reading the owner must decide; CN's text ("nonprofit subsidiaries") does not settle it (wave 46A).
- **What is not possible.** No dated EO BMF or Pub 78 extract for 2023–24 is published (b40n1202-b43n26-03 §1.3). Status at grant time is reconstructed from dated IRS evidence (§1.4). CN's rules are held at their 2026 text (§5).

## 1. Method

### 1.1 Grant units and dollars

- The universe and dollars are exactly the parent's, imported through `build_numerator`: top-50 DAFRC sponsors by FY2024 DAF assets, FY2023–24 Schedule I Part II lines, totals rows dropped, DAF-to-DAF lines dropped, positive amounts, each sponsor-year's lines × its DAF share of grants.
- The parent sums each recipient's dollars across sponsors and years. Here a **grant unit** is one recipient × one sponsor-year (581,672 units; 174,220 recipients). Blank-EIN lines keep the parent's name keys and stay ineligible on every date.
- An assertion checks that the unit dollars sum to the parent's total ($74,073,755,051) to within $1.
- **Fiscal year.** Each sponsor-year's fiscal year is the 12 months ending on its chosen return's `tax_period_end` (`pick_returns`; `fy_bounds` from the -03 script). The 94 sponsor-years end on 12 different dates [F]:
  - 30 June (28 sponsor-years): $45.71bn (61.7% of dollars);
  - 31 December (52): $23.86bn (32.2%);
  - other month ends (14): $4.50bn.
- **Grant dates within the year are not public.** So the central cut-off is the end of the fiscal year, the task's "filings available at the end of FY2023 and FY2024". The start of the fiscal year is the sensitivity.

### 1.2 Which filings were "available"

- **Processing date.** The e-file DLN carries the IRS processing date as a Julian day; the TEOS `OBJECT_ID` repeats it (`OBJECT_ID[:4]` = year, `OBJECT_ID[5:8]` = Julian day).
  - The two agree on every 990, 990-EZ and 990-PF row of the 2017–2026 index files (0 mismatches in 5.5m rows; checked separately before the run).
- A return counts at a cut-off if it was processed on or before it. When CN actually received each return is not public (§5).
- **Release batches do not measure a lag.** The 2024–2026 index files carry `XML_BATCH_ID` (e.g. `2024_TEOS_XML_05A`). The batch month is the processing month itself: the median gap from processing date to the first day of the batch month is −11 days in each year [F]. The batch IDs therefore give no evidence of a publication lag, and none is assumed beyond the FY-start variant.
- **Index coverage.** The parent cached TEOS index files for 2019–2026. The 2019 file holds only part of processing year 2018 (88,373 rows) and nothing earlier [F]. At a 2023 cut-off, CN's six-year window reaches back to tax year 2017.
  - For this reason the as-of tests also read the **2017 and 2018 index files**, 146,340 matching rows (§8, S3b).
  - These are pre-2021 files, used only as filing history for windows that CN's own rule defines, as the parent used the 2019–2020 files. The owner may prefer the 2019-on-only variant (72.36%) under the 2021+ evidence rule (§3.1).

### 1.3 Filing rules at the cut-off

These are the parent's `cn_filing_test` and `cn_reason`, re-dated. The rules come from CN's help article (S6) [P]:
- **Three returns.** At least three distinct e-filed 990-series tax periods with a tax period ending in years Y−6 to Y−1, where Y is the cut-off year.
  - The parent's November 2026 window, 2020–2025, is the same formula with Y = 2026.
  - Amendments are collapsed to the latest object id per tax period, among returns processed by the cut-off.
  - The sensitivity uses processing years Y−5 to Y, the parent's index-year window re-dated.
- **Recent returns.** At least two of the four most recent periods are full 990s, and the latest is not a 990-PF.
- **Order and labels.** The order of tests and the reason labels are the parent's. The central reading excludes national and processor DAF sponsors.

### 1.4 IRS status at the cut-off (reconstructed)

**`current_bmf` variant (as the parent).** The November 2026 BMF row stands for status at grant time.

**`reconstructed` variants (headline).** These adjust the current BMF with dated IRS evidence:
- **Revoked at the cut-off.** An EIN in the current BMF with an automatic revocation effective on or before the cut-off and a reinstatement dated after it is treated as revoked at grant time (`revoked_at_cutoff_later_reinstated`). This affects 34 recipients and $1.09m [F].
- **Presumed listed.** An EIN absent from the current BMF is presumed to have been a listed 501(c)(3) at the cut-off when two conditions hold:
  - there is 501(c)(3) evidence: exemption type 03 on the revocation list, or `Organization501c3Ind` on a return header cached by the -03 run;
  - there is evidence that it left after the cut-off: a revocation effective after the cut-off, or a 990-series return processed after it.

  Its foundation code is unknown, but a 990-PF latest return still fails `latest_is_990pf`. Presumed-listed units total $318.9m across 2,503 recipients; $202.1m of that passes the filing rules [F]. **None of the 1,148 presumed-listed EINs that pass is in the current Pub 78** [F]. This is consistent with organisations that have since closed [I].
- **Ruling date (sensitivity only).** An EIN in the current BMF whose `RULING` (YYYYMM) is after the cut-off month is treated as not yet recognised. This rule is kept out of the headline because later determinations reset `RULING`. KIPP New York (ruling 202512), Christian Union (202505) and Pulse Outreach (202507) all pass the filing rules with returns processed before their ruling dates, and the Musical Instrument Museum (202508) was a 990-PF filer at grant time [F]. Applied anyway, the rule lowers the headline by 0.18 points, to 72.48%.

**Pub 78.** Only the current file exists, so it is a diagnostic only.

## 2. Results: headline (end of fiscal year, reconstructed status)

### 2.1 By first failing rule at grant time

All figures are [F]. Recipient counts are distinct recipients with at least one unit in the category, so a recipient with grants on several dates can appear in more than one row.

| Category | Grant units | Recipients | DAF-weighted $bn | **Share at grant time** | Share, current status | Change, points |
|---|---|---|---|---|---|---|
| **eligible** | 355,964 | 81,902 | 53.82 | **72.66%** | 76.85% | −4.19 |
| no_efiled_990_church | 91,829 | 29,534 | 6.16 | 8.31% | 8.34% | −0.03 |
| fewer_than_3_efiled_in_6y | 33,165 | 19,143 | 3.66 | 4.94% | 3.44% | +1.50 |
| no_efiled_990_other (no return processed by the cut-off) | 24,796 | 15,428 | 3.25 | 4.38% | 1.37% | +3.01 |
| not_in_bmf | 45,146 | 19,929 | 3.86 | 5.21% | 5.64% | −0.43 |
| private_foundation | 2,367 | 1,082 | 1.26 | 1.70% | 1.70% | 0.00 |
| no_efiled_990_group_subordinate | 3,949 | 1,173 | 0.67 | 0.90% | 0.87% | +0.03 |
| fewer_than_2_full_990_in_latest_4, 990-EZ filers | 18,703 | 12,227 | 0.45 | 0.61% | 0.53% | +0.08 |
| no_ein_domestic | 4,941 | 3,649 | 0.40 | 0.54% | 0.54% | 0.00 |
| daf_sponsor_national_or_processor | 188 | 13 | 0.35 | 0.47% | 0.47% | 0.00 |
| latest_is_990pf | 345 | 126 | 0.19 | 0.26% | 0.04% | +0.22 |
| not_501c3 | 162 | 100 | 0.01 | 0.02% | 0.02% | 0.00 |
| fewer_than_2_full_990_in_latest_4, other | 74 | 46 | 0.01 | 0.01% | 0.21% | −0.20 |
| revoked_at_cutoff_later_reinstated | 41 | 34 | <0.01 | <0.01% | — | 0.00 |
| no_ein_foreign | 2 | 2 | <0.01 | <0.01% | <0.01% | 0.00 |
| **Total** | **581,672** | **174,220** | **74.07** | 100% | 100% | |

On the as-filed Schedule I basis, the grant-time share is 72.12%, against 76.27% on current status [F].

### 2.2 What moves between current status and grant time

These are the largest flows by DAF-weighted dollars [F]. All flows are in the CSV (`row_type = transition`).

| Current status → grant time | Units | Recipients | $m | Points |
|---|---|---|---|---|
| eligible → fewer than 3 e-filed returns | 21,995 | 11,419 | 2,914.2 | 3.93 |
| fewer than 3 → no e-filed return processed yet | 5,624 | 3,910 | 1,827.1 | 2.47 |
| eligible → no e-filed return processed yet | 2,260 | 1,527 | 343.1 | 0.46 |
| eligible → fewer than 2 full 990s (EZ filers) | 5,998 | 3,639 | 215.5 | 0.29 |
| not in BMF → eligible (presumed listed then) | 2,806 | 1,148 | 202.1 | 0.27 |
| fewer than 3 → eligible (filed 990s then, stopped since) | 780 | 212 | 171.5 | 0.23 |
| fewer than 2 full 990s → latest is 990-PF | 137 | 31 | 151.2 | 0.20 |

**Reading [I].**
- **The gap is organisational age.** Recipients that are rateable today but were one or two returns short at grant time account for 4.4 of the 4.7 points lost.
- **They are disproportionately recent, large intermediary or advocacy vehicles.** The 85 Fund, Just Trust, Our American Future Foundation, City Fund, Murmuration Research Institute, Convergent Research, Arc Research Institute and UATX each received $29–145m, and none had three e-filed returns at the relevant year end [F for the amounts and tests; I for the characterisation].
- **Navigation Charitable Fund ($1.26bn; EIN 92-1117448, BMF ruling 202303)** is ineligible on both dates. Its first e-filed return (tax year 2023) was processed on 2024-11-15, so at earlier cut-offs it had none (part of the $1.83bn "fewer than 3 → no return yet" flow) and at later ones it had one [F].
- **FY2023 falls more than FY2024 (−5.6 against −2.9 points).** The FY2023 cut-offs come a year earlier, so more of today's young recipients were short of three returns. FY2023 also carries the CZ LLC dollars, which are ineligible on both dates [F].

### 2.3 By sponsor-year

Each sponsor-year's grant-time share is in the CSV (`row_type = sponsor_year_cutoff`). Among sponsor-years with over $1bn of DAF-weighted dollars, the lowest are [F]:
- Silicon Valley Community Foundation FY2023: 26.2% of $4.39bn. The CZ LLCs are $1.59bn of it.
- National Christian Charitable Foundation: 61.9% of $1.72bn (FY2023) and 62.7% of $2.21bn (FY2024). Churches with no e-filed 990 are ineligible on both dates [I].
- DAFgiving360 (Donor Advised Charitable Giving Inc): 69.7% (FY2023) and 72.8% (FY2024).
- Fidelity Charitable: 73.3% (FY2023) and 75.7% (FY2024).

## 3. Sensitivities

### 3.1 Same cut-off, different assumptions (eligible share of DAF-weighted $) [F]

| Variant | Both years | FY2023 | FY2024 |
|---|---|---|---|
| Current status (parent rules, Nov 2026 filings; reproduction) | 76.85% | 73.73% | 79.62% |
| **As of FY end, reconstructed status (headline)** | **72.66%** | **68.11%** | **76.68%** |
| As of FY end, current BMF status (no reconstruction) | 72.38% | 67.75% | 76.48% |
| As of FY end, processing-year window Y−5..Y | 72.63% | 68.04% | 76.70% |
| As of FY end, plus ruling-date rule | 72.48% | 67.90% | 76.53% |
| As of FY end, parent's 2019–2026 index only | 72.36% | 67.47% | 76.68% |
| … plus an upper bound for the missing 2017–2018 index rows | 74.67% | 70.90% | 78.00% |
| Current status, CZ LLCs looked through to Biohub Inc | 79.00% | 78.31% | 79.62% |
| As of FY end, CZ LLCs looked through to Biohub Inc | 74.81% | 72.69% | 76.68% |

- **Reconstructing status adds 0.27 points.** It adds the presumed-listed passers and the revocation-at-cut-off rule, against the current-BMF variant.
- **The 2017–2018 index files add 0.30 points** ($221.0m) against the 2019-on-only run, and remove nothing.
- **The gap bound was loose.** It assumed every missing early window year had been filed, and gave 74.67%; the actual files close only about a seventh of that bound (0.30 of 2.31 points).

### 3.2 Grant on the first day of the fiscal year [F]

- Using filings processed before the fiscal year began gives **68.83%** (FY2023 64.75%, FY2024 72.44%).
- A further $2.98bn (14,336 recipients) is eligible at the year end but not at its start.
- This also stands in for a twelve-month delay between IRS processing and CN's receipt [I].
- With an even spread of grants through the year, the expected share would lie between 68.83% and 72.66% [I]. DAF grant timing within the year is seasonal and was not modelled.

## 4. The Chan Zuckerberg Biohub LLC question

| EIN | Name as filed | Sponsor-year (cut-off) | DAF-weighted $m |
|---|---|---|---|
| 88-2242512 | CZ Institute for Advanced Biological Imaging LLC | SVCF FY2023 (2023-12-31) | 563.9 |
| 88-2010111 | CZ Biohub SF LLC | SVCF FY2023 | 554.3 |
| 93-1478843 | CZ Biohub New York LLC | SVCF FY2023 | 238.6 |
| 92-2259616 | CZ Biohub Chicago LLC | SVCF FY2023 | 237.2 |
| | **Total** | | **1,594.0** (2.15% of top-50 dollars) |

- **The LLCs themselves.** None has an e-filed return in the 2017–2026 index, a BMF row or a revocation row [F]. Under the central rules, which match the parent, they are `not_in_bmf` and ineligible on both dates.
- **The parent at the grant cut-off.** Chan Zuckerberg Biohub Inc (81-1669175) is in the BMF with foundation code 12 and ruling 201609, and in Pub 78 [F].
  - Its e-filed full 990s cover tax years 2016, 2017, 2018, 2020, 2021, 2022, 2023 and 2024. No tax year 2019 return is in the index.
  - At 31 December 2023 it had six periods processed, five of them in the 2017–2022 window, and its four latest were full 990s. The latest, for tax year 2022, was processed on 2023-11-14 [F].
  - So it was rating-eligible at grant time on every rule filings can test.
- **What look-through changes.**
  - Current status: 76.85% → 79.00% (+2.15 points).
  - Grant time: 72.66% → 74.81% (+2.15).
  - SVCF FY2023 alone: 26.2% → 62.6% [F, computed from the sponsor-year row plus $1.594bn].
- **The legal reading.** Validation wave 46A found the LLCs listed as disregarded entities on Biohub Inc's FY2023–24 Schedule R. IRS Notice 2012-52 treats gifts to a domestic single-member LLC wholly owned by a charity "as a charitable contribution to a branch or division of the U.S. charity" [P, as quoted in wave 46A]. Whether CN would credit those dollars to Biohub Inc is not stated. Its rules exclude "nonprofit subsidiaries" without defining them [P, S6].
- **Recommendation [I].** Report the central figure (72.66%) as the headline and the look-through figure (74.81%) beside it. The timing question and the CZ question are independent: each moves the share by roughly 2–4 points, and they add.

## 5. Limits

1. **CN's 2026 rules are applied to 2023–24 grants.** CN's eligibility text has changed over time.
   - The Spring 2024 release note introduced DAF-sponsor ineligibility (S9). Before it, DAF sponsors may have been rateable. Their whole share is 0.47 points, so that bounds the effect on the headline [F].
   - No earlier rule texts were read. The parent read the current release notes; archived versions are queued (P-B40N1202-B43N2604-01).
2. **The processing date is not CN's receipt date.** CN states it "must directly receive" the returns. The FY-start variant (68.83%) brackets a year's delay. When TEOS published each batch is not in the index files.
3. **Status at grant time is reconstructed, not observed.**
   - Foundation code, subsection and group status are taken from the November 2026 BMF for EINs still listed.
   - The presumed-listed rule for departed EINs is an inference [I]. It adds 0.27 points.
   - No dated BMF or Pub 78 snapshot was available (queued as P-B40N1202-B43N2603-05).
4. **Grant dates are not known.** Year-end and year-start cut-offs bracket the timing; neither is the true date.
5. **Rules filings cannot test.** "Giving Not Recommended" alerts, "nonprofit subsidiaries" and the expense rule (parent §4.1 diagnostics: 0.1% of sampled passers fail it) are not applied by date. This is a count of eligibility, not of ratings; no historical ratings were read.
6. **Index files.** Returns processed in 2016 (150,057 rows in the 2017 file) have tax periods before every window, so they can affect only the four-most-recent-returns rule, for organisations with few later returns. Returns processed before 2016 are absent, with the same limited reach [I].
7. **Recipient counts by category overlap** across dates, as noted in §2.1. Dollar shares do not overlap.

## 6. Reproduction

```
S=<scratchpad>
python3 scripts/mission_cn_eligibility_by_year.py . --np-cache $S/npcache --lines-cache $S/rcp/lines --bmf-dir $S/rcp/bmf \
    --index-dir $S/irs --early-index-dir $S/q0426/irs_early --xml-cache $S/nb03/xmlhdr
```

- `--index-dir` holds the parent's cached `index_2019.csv` … `index_2026.csv`, `data-download-revocation.txt` and `data-download-pub78.txt`.
- `--early-index-dir` holds `index_2017.csv` and `index_2018.csv`, downloaded 2026-11-20 (S3b).
- `--xml-cache` is the -03 run's header cache. It is read only, and nothing is fetched.
- A run takes about 2.5 minutes. Two runs, one with `PYTHONHASHSEED=7`, produce byte-identical CSVs.
- The script prints a JSON summary: the self-check share, the eligible share and dollars per variant, flows, the largest recipients lost and gained, the ruling-rule diagnostics and the CZ detail.

## 7. Data dictionary: `cn-eligibility-by-year-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_type | `share` (eligibility by category); `transition` (units whose category differs between two readings); `sponsor_year_cutoff` (one row per sponsor-year) |
| variant | **share rows:** `current_status_parent_rules` (reproduces the parent: Nov 2026 filings, current BMF); `asof_fy_end_reconstructed` (**headline**); `asof_fy_end_current_bmf`; `asof_fy_start_reconstructed`; `asof_fy_end_reconstructed_index_year_window`; `asof_fy_end_reconstructed_plus_ruling_date_rule`; `asof_fy_end_reconstructed_index_2019_on_only`; `asof_fy_end_reconstructed_index_2019_on_plus_gap_bound`; `current_status_cz_lookthrough`; `asof_fy_end_reconstructed_cz_lookthrough`. The first four have one row per category; the rest have `all` and `eligible` rows only. **transition rows:** `current_status -> asof_fy_end_reconstructed` or `current_status -> asof_fy_start_reconstructed`. **cutoff rows:** `asof_fy_end_reconstructed` |
| scope_type / scope | `all` / `all_recipients`; `grant_fy` / `fy2023` or `fy2024` (sponsor fiscal year of the grant); `sponsor_year` / `<sponsor EIN>:FY<year>` |
| category | `all`, `eligible`, or the first failing rule: the parent's labels (`not_in_bmf`, `not_501c3`, `private_foundation`, `daf_sponsor_national_or_processor`, `no_efiled_990_church`, `no_efiled_990_group_subordinate`, `no_efiled_990_other`, `fewer_than_3_efiled_in_6y`, `latest_is_990pf`, `fewer_than_2_full_990_in_latest_4[_ez_filer]`, `no_ein_domestic`, `no_ein_foreign`) plus `revoked_at_cutoff_later_reinstated` and, in the ruling-rule variant only, `not_yet_recognised_at_cutoff`. Transition rows hold `<current> -> <grant time>`. Cutoff rows hold `cutoff=<sponsor tax_period_end>` |
| grant_units | Recipient × sponsor-year units in the row |
| recipients | Distinct recipient keys (EIN, or name key for blank-EIN lines) in the row. They overlap across categories. |
| grant_unit_share | grant_units ÷ the scope's units (share rows) |
| usd_daf_weighted | DAF-weighted Schedule I dollars, USD |
| dollar_share_daf_weighted | Share of the scope's DAF-weighted dollars. In cutoff rows it is the **eligible** share of that sponsor-year's dollars; in transition rows it is the share of all top-50 dollars. |
| usd_sched_i, dollar_share_sched_i | The same on the as-filed Schedule I basis (dollar_share_sched_i blank on transition and cutoff rows) |
| source | Source note |

## 8. Source register

| ID | Source | URL | Accessed | Use |
|---|---|---|---|---|
| S1 | Parent study and data | [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md); [charity-rating-eligibility-share-2026-11-19.csv](../../data/mission-2026-11-14/charity-rating-eligibility-share-2026-11-19.csv) | Repo | Universe, rules, 76.85% (0.768507) reproduced |
| S2 | Non-BMF study and wave 46A validation | [b40n1202-b43n26-03-non-bmf-recipients.md](b40n1202-b43n26-03-non-bmf-recipients.md); [validation-wave46a-report.md](validation-wave46a-report.md) | Repo | CZ LLC EINs; Schedule R finding; 79.00% look-through; no dated BMF |
| S3 | IRS TEOS e-file index 2019–2026 | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (and each year 2019–2026) | Cached 2026-11-14/15 (parent) | Filing history; processing date (OBJECT_ID/DLN); form by DLN prefix |
| S3b | IRS TEOS e-file index 2017 and 2018 | https://apps.irs.gov/pub/epostcard/990/xml/2017/index_2017.csv ; https://apps.irs.gov/pub/epostcard/990/xml/2018/index_2018.csv | 2026-11-20, HTTP 200 (62,311,681 and 58,185,653 bytes; Last-Modified 11 Jul 2023) | Filing history for windows reaching back to tax year 2017 |
| S4 | IRS EO Business Master File | https://www.irs.gov/pub/irs-soi/eo1.csv (eo1–eo4, eo_pr, eo_xx) | Cached (parent); Last-Modified 2026-11-09 | SUBSECTION, FOUNDATION, GROUP, AFFILIATION, RULING |
| S5 | IRS automatic revocation list | https://apps.irs.gov/pub/epostcard/data-download-revocation.zip | Cached 2026-11-11 | Revocation and reinstatement dates; exemption type |
| S6 | IRS Pub 78 data | https://apps.irs.gov/pub/epostcard/data-download-pub78.zip | Cached 2026-11-11 | Diagnostic (current only) |
| S7 | Return headers, GivingTuesday mirror of IRS TEOS XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | Cached by the -03 run (2026-11-20); not fetched here | `Organization501c3Ind` for non-BMF EINs |
| S8 | Charity Navigator Help Center, "Charity Navigator's rating system" | https://intercom.help/charity-navigator/en/articles/8557824-charity-navigator-s-rating-system | Dated 2026-04-09; quoted from the parent §1.3 (not re-fetched) | Eligibility rules |
| S9 | Charity Navigator Release Notes | https://www.charitynavigator.org/about-us/our-methodology/ratings/release-notes/ | Quoted from the parent §1.3 (not re-fetched) | DAF ineligibility from Spring 2024 |
| S10 | DAFRC sponsor panel (repo copy) | [dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | Repo | Sponsor names |

**Robots and fetch log** (scratchpad `q0426/robots/log.tsv`, `q0426/fetchlog.tsv`):
- apps.irs.gov/robots.txt returned 302 to www.irs.gov/404, so the host has no robots file.
- www.irs.gov/robots.txt returned 200. It has only a `User-agent: *` group, with no ClaudeBot, anthropic-ai or Claude-* groups, and `/pub/` is not disallowed.

Only the two index files above were downloaded, with user agent `research-script/1.0`. There was no outreach and no login, and sec.gov, crt.sh and certspotter were not used.

## 9. Headline claims for validation

1. On grant-time filings (processed by the end of each sponsor's fiscal year), 72.66% of top-50 FY2023–24 DAF-weighted dollars ($53.82bn of $74.07bn) went to CN-eligible recipients, against 76.85% on current status (CSV `share` rows, `asof_fy_end_reconstructed` and `current_status_parent_rules`, `eligible`).
2. By grant year: FY2023 68.11% against 73.73%; FY2024 76.68% against 79.62% (CSV `grant_fy` rows).
3. $3.50bn eligible now was not eligible at grant time, $2.91bn of it on the three-return rule (CSV `transition` rows; JSON `lost_by_asof_reason`).
4. The 85 Fund (20-2466871, $144.9m) had two e-filed returns processed at its sponsor's 2023-06-30 year end; its tax year 2022 return was processed on 2023-11-15 (TEOS index 2023, OBJECT_ID 202313199349307191; the tax year 2023 return is 202433209349321903 in index 2024).
5. Compassion International (36-2423707) filed full 990s for tax years 2016–2019 and only 990-T from tax year 2021. It was eligible at its FY2023 grant cut-off but not now (TEOS index 2017–2025).
6. Grant on day one of the fiscal year: 68.83% (CSV `asof_fy_start_reconstructed`).
7. The four CZ LLCs received $1,594.0m, all from SVCF in FY2023. Chan Zuckerberg Biohub Inc passed every filing rule at 2023-12-31, and look-through gives 74.81% at grant time against 79.00% now (CSV `cz_lookthrough` rows; JSON `cz`).
8. In every TEOS index file for 2017–2026, OBJECT_ID[5:8] equals the DLN's Julian day (§1.2). The 2024–2026 batch month equals the processing month (median −11 days).
9. BMF `RULING` dates postdate the filing history for KIPP New York (202512) and Christian Union (202505), so RULING cannot date first recognition (JSON `ruling_rule_top`).
