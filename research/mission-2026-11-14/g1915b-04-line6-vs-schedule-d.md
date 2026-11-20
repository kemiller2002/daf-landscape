# Form 990 Part IV line 6 against Schedule D Part I, across every return the repo has parsed

**Queue item:** P-G1915B-04. **Task:** g1915b-04. **Prepared:** 2026-11-19.
**Status:** desk research from public filings only. No outreach, no logins.
**Script:** [`scripts/mission_line6_check.py`](../../scripts/mission_line6_check.py) (stdlib only, functional style). It fetches nothing; it re-reads the repo's harvest CSVs and the scratchpad caches of earlier validated runs. Two runs gave byte-identical CSV and summary output.
**Output:** [`data/mission-2026-11-14/line6-vs-schedule-d-2026-11-19.csv`](../../data/mission-2026-11-14/line6-vs-schedule-d-2026-11-19.csv): 3,341 rows, one per effective return in either disagreement case (44 forward, 3,297 reverse).
**Queue file:** [`data/mission-2026-11-14/queue-proposals-g1915b-04.csv`](../../data/mission-2026-11-14/queue-proposals-g1915b-04.csv) (5 rows).
**Builds on:** [gap1915-b4011-filing-frames.md](gap1915-b4011-filing-frames.md) §1 item 4 and its wave-38C corrections ([validation-wave38c-report.md](validation-wave38c-report.md)); [full-universe-990-harvest-and-corrected-totals.md](full-universe-990-harvest-and-corrected-totals.md) (P-MOR-01 outside-DAFRC scan); [queue-batch37-filing-questions.md](queue-batch37-filing-questions.md) (P-99F-03); [queue-batch38-data-followups.md](queue-batch38-data-followups.md) (P-B37B-01); [queue-batch33-panel-scans.md](queue-batch33-panel-scans.md) (P-B32B-01).

Run: `python3 scripts/mission_line6_check.py . --irs-dir <index_2019..2026.csv dir> --soi-dir <{yy}eoextract990.csv dir> --frames-cache <gap1915-b4011 cache> --ft-cache <batch-38 ft cache> --l6-cache <batch-37 l6 cache> --extract-cache <mission_990_contractors extract990 cache> --summary <out.json>`

---

## 1. Bottom line

1. **Forward case (line 6 not "Yes", Schedule D Part I DAF accounts > 0): 44 effective returns from 35 EINs, FY2021–FY2026** [C]. All 44 answer line 6 "No" (none is blank). They are 0.51% of the 8,572 effective returns that report accounts > 0. 33 returns (24 EINs) are plausible: 13,374 accounts and **$265.2m** of year-end DAF value. The other 11 put dollar amounts or other numbers in the count field (3,859,132 "accounts" and $0 of value).
2. **The Groundswell example reproduces.** Its amended TY2024 return (object 202640289349301029, e-filed 2026-01-28) reports 12,808 accounts and $10,084,314 with `DonorAdvisedFundInd` = 0; re-read from the mirror on 2026-11-19 [F]. Frame A's 17 positive "No" returns from 14 holders all reappear in this table, unchanged [C].
3. **One sponsor dominates the money.** Legacy Global Foundation's FY2023 return reports 347 DAFs and $218.9m with line 6 = 0 (object 202443209349326279; re-read 2026-11-19) [F]. Without it, the plausible forward returns hold $46.4m across six years.
4. **A screen keyed on line 6 drops every forward return. DAFRC does not key on line 6.**
   - **SOI:** the IRS SOI Form 990 extract carries line 6 as `dnradvisedfundscd` ("Donor advised funds?", 990 Core Pt IV-6) and has no Schedule D field. Of the 44 forward returns, 34 are "N" in the extract and 10 are not in any extract yet (filed in 2026, or tax periods not yet released). **None is "Y"** [C]. The repo's own outside-DAFRC scan (P-MOR-01) selected filers from that field, so it could not see the 12 plausible forward returns from filers outside the DAFRC panel.
   - **DAFRC:** its technical appendix selects on Schedule D Part I(a) filing with at least $1 of DAF assets, followed by manual vetting, and does not mention line 6 [F]. The data agree. DAFRC carries 17 forward returns from 11 panel sponsors at their filed values ($245.1m, including Legacy Global FY2023), although each answered "No". **So line 6 does not decide whether DAFRC counts a return; whether the sponsor passed vetting does.**
5. **What a line-6 filter would miss, by year (plausible forward returns, filed values)** [C]:

   | FY | Returns | Accounts | DAF value | Of which outside DAFRC (no panel row) |
   |---|---|---|---|---|
   | 2021 | 5 | 60 | $12.85m | 2 returns, 14 accounts, $0.67m |
   | 2022 | 6 | 45 | $3.34m | 1, 1, $2,000 |
   | 2023 | 9 | 401 | $228.00m | 1, 1, $68,114 |
   | 2024 | 6 | 12,831 | $16.07m | 3, 12,810, $10.09m (Groundswell $10.08m) |
   | 2025 | 6 | 36 | $4.97m | 6, 36, $4.97m (after DAFRC's FY2024 window) |
   | 2026 | 1 | 1 | $8,462 | 1, 1, $8,462 |
   | **All** | **33** | **13,374** | **$265.25m** | **14, 12,863, $15.81m** |

   - Two further FY2024 returns are in the DAFRC panel at imputed values: Mitchell Hamline filed $4.27m, DAFRC imputed $3.68m; Quakerdale filed $28,468, DAFRC imputed $77,657.
   - Against DAFRC's market totals the miss is negligible. Even the FY2023 peak is 0.089% of DAFRC's $256.39bn.
   - DAFRC's only true FY2021–FY2024 miss is 7 returns, 12,826 accounts and $10.83m, and Groundswell is 93% of that money. **As in batch 37 and batch 38, the line-6 tail adds accounts and sponsors, not money.**
6. **Year-level versus filer-level screens.** 8 of the 24 plausible EINs answer "Yes" in some other return read, so an EIN-level screen across years would still find the sponsor (11 returns, $235.0m, mostly Legacy Global). **16 EINs never answer "Yes" in any return read (22 returns, 12,935 accounts, $30.2m)**, and only reading Schedule D finds them [C].
7. **Reverse case (line 6 "Yes", Part I DAF accounts missing or zero): 3,297 effective returns from 1,511 EINs, FY2021–FY2026.** Not all are disagreements. Line 6 also asks about “any similar funds or accounts”, and at least 567 of these returns (226 EINs) are P-MOR-01’s “other funds column only” rows, which fill Schedule D Part I column (b) instead of (a); in a 60-return XML sample, 8 had column (b) > 0. A further 341 report column (a) DAF contributions or grants with no or zero year-end count, as a sponsor winding down would (Ayco FY2025, Jasper Ridge FY2022, TIAA Charitable FY2021). At most 2,389 returns (1,153 EINs) show no Part I activity at all [C] [V wave 39B] That is 27.9% of the 11,825 effective line-6 "Yes" returns [C].
   - 2,546 returns (1,114 EINs) leave the Part I DAF column blank.
   - 596 (345 EINs) report zero or blank count and value.
   - 155 (88 EINs) report a value but no count. Their values total $455.7m, of which $332.6m is at DAFRC panel members such as The Blackbaud Giving Fund.
   - **None of the returns read answered "Yes" without attaching Schedule D**, among the sources that record whether Schedule D is present.
   - By year: 720, 761, 804, 773, 235 and 4 returns in FY2021–FY2026; FY2025–26 are incomplete.
   - 282 returns (153 EINs) are DAFRC panel members and 3,015 (1,358 EINs) are not.
   - A line-6 sponsor count therefore over-counts: 3,837 EINs answer "Yes" in some return, while 2,720 EINs report accounts > 0. Part of the gap is column-(b) filers whose “Yes” is correct under line 6’s “similar funds or accounts” wording, so what is over-counted is DAF sponsors, not wrong answers [I] [V wave 39B]
8. **The reverse case hides little money, but more than the forward case, and only as a proxy.** Of the reverse returns, 428 come from EINs that reported positive DAF values in an earlier return. Carrying that earlier value forward gives $53.2m (FY2022), $358.0m (FY2023), $453.8m (FY2024) and $1,771.4m (FY2025) [I].
   - The FY2025 figure is mostly Ayco Charitable Foundation ($1.158bn). Ayco's FY2025 return reports zero DAFs at year end, so for Ayco a carry-forward is wrong. Its line 6 “Yes” is also correct: the return reports $408.1m of DAF contributions and $452.6m of DAF grants during the year, with zero DAFs and zero total assets at year end. It is a wind-down, not a reporting gap [F] [V wave 39B]
   - Treat these figures as an upper bound on Part I gaps, not as missing assets. DAFRC handles the FY2021–24 panel part through imputation or "closed" flags (batch 33, P-B32B-01).

---

## 2. Method

### 2.1 Inputs (no new fetches except spot checks and documentation)

| Source tag | What it is | Universe it covers | Records |
|---|---|---|---|
| `harvest` | `form990-returns-schedule-d-harvest-full.csv`, `form990-harvest-fy2025-refresh.csv`, `form990-harvest-2026-fill.csv` | All 1,512 DAFRC FY2024 sponsors, FY2022–FY2025 returns | Part IV `daf_ind_part_iv`, Schedule D Part I count / contributions / grants / EOY |
| `extract` | `mission_990_contractors.py` extract cache (12,257 JSON) | DAFRC sponsor returns filed 2020–2026 | same fields; blank kept distinct from 0 |
| `nondafrc` | `non-dafrc-daf-filers-990.csv` (P-MOR-01) | Every non-DAFRC (EIN, tax period) answering line 6 "Y" in SOI extracts 20–25 | Part I values, XML line 6 |
| `frames` | gap1915-b4011 full-read cache (99,134 JSON) | Frame A: all 990s 2022–2026 of 501(c)(3)s ruled 2021+; frame B: CF-named or NTEE T31 filers 2021–2026 | `daf_ind`, Part I (0 stands for absent) |
| `l6` | batch-37 line-6 cache (9,647 JSON, validation rerun of wave 22) | Newest FY2022+ return of T30/T31/T70 or DAF-named non-DAFRC EINs | line 6, Part I |
| `ft` | batch-38 full-text cache (126,736 JSON) | Newest FY2022+ return of every 501(c)(3) answering line 6 "N" in SOI with ≥ $1m assets | line 6, Part I |

- **Supporting data.** The IRS TEOS index 2019–2026 supplies EIN, tax period, return type and taxpayer name where a cache lacks them. It also gives the denominator (all Form 990 EIN-periods by FY) and later returns for the same EIN and period. The SOI extracts 20–25 give `dnradvisedfundscd` as the SOI file carries it. The DAFRC dataset gives panel membership and the published row for the same FY.
- **Merging.**
  - Records are merged by OBJECT_ID. The first non-empty value is taken in the source order harvest > extract > l6 > ft > nondafrc > frames, so blank-aware sources win over the frames cache, which stores 0 for an absent tag.
  - Where two sources read the same OBJECT_ID they never disagreed: 0 line-6 conflicts and 0 count conflicts.
  - Names come from the index, because the ft/l6 extracts sometimes captured the paid preparer's firm name.
- **Scope.** Form 990 only (990-EZ has no Schedule D Part I). FY = the calendar year of the tax-period end, as in DAFRC. FY ≥ 2021.
- **Effective return.** Per (EIN, tax period), the return read with the highest OBJECT_ID is used. The ID leads with the IRS processing year, so a later amended return supersedes the original. For all 3,341 flagged rows, no later 990 for the same EIN and period exists in the index without having been read (`unread_later_return_in_index` = no).
- **Line 6.** `1`/`true`/`X` = Yes; `0`/`false` = No; anything else = blank.

### 2.2 Case rules

| Case | Rule | Subcases |
|---|---|---|
| forward | line 6 ≠ Yes and `DonorAdvisedFundsHeldCnt` > 0 | `line6_no`, `line6_blank` |
| reverse | line 6 = Yes and count missing or 0 | `no_schedule_d`; `part_i_daf_blank` (count and value both absent); `count_missing_or_zero_value_positive`; `count_and_value_zero_or_blank` |

- **Plausible** (forward only): count > 0, EOY value > 0 and value ≥ count (at least $1 per account). This rules out the dollar-in-count-field errors noted in frame A.
- **`line6_screen_drops`:** yes when the SOI value (or, if the return is not in SOI, the XML value) is not "Y". It is yes for all 44.
- **`dafrc_captures_same_fy`:** `panel_row_irs_990` when DAFRC carries the same FY with source "IRS 990". The other values are `panel_row_imputed`, `panel_no_row_same_fy` and `outside_panel`.

### 2.3 Spot checks and robots log (2026-11-19, user agent `research-script/1.0`)

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | HTTP 404 (no rules) | Re-read 3 XMLs: Legacy Global 202443209349326279, Groundswell 202640289349301029 and Mitchell Hamline 202531329349301983. All three have `DonorAdvisedFundInd` 0 and Part I counts 347, 12,808 and 4 |
| www.dafresearchcollaborative.org | 200. The `User-agent: *` group disallows only /config, /search, /account, /api, /static and query-string formats; `/s/` is allowed | Updated-analysis memo, both technical appendices, the annual-report page and the sitemap |
| www.irs.gov | 200. Disallows search paths, `/*/downloads/` and others; `/statistics/` and `/pub/irs-soi/` are allowed | SOI extract page and `25eofinextractdoc.xlsx` |

- **Not used:** sec.gov, crt.sh and certspotter.

---

## 3. Results

### 3.1 Coverage

| FY | Form 990 EIN-periods in the IRS index | Effective returns read here | Share |
|---|---|---|---|
| 2021 | 327,282 | 9,744 | 3.0% |
| 2022 | 340,996 | 16,952 | 5.0% |
| 2023 | 351,699 | 24,541 | 7.0% |
| 2024 | 360,056 | 67,960 | 18.9% |
| 2025 | 250,022 (still filling) | 101,804 | 40.7% |
| 2026 | 11,981 | 2,717 | 22.7% |
| **All** | **1,642,036** | **223,718** (164,996 EINs; 225,510 returns before de-duplication) | **13.6%** |

- **Line-6 "Yes" filers (the reverse universe) are covered almost completely.** Of the SOI (EIN, period) rows answering "Y", these were read: FY2022 2,809/2,823, FY2023 2,818/2,820, FY2024 2,726/2,730, FY2025 309/311. **FY2021 is weaker: 2,152 of 2,778 (77.5%)**, because the DAFRC harvest starts at FY2022.
- **Line-6 "No" filers (the forward universe) are covered only where DAFs are likely:**
  - all DAFRC sponsors;
  - all new 501(c)(3)s ruled 2021+ (frame A);
  - all CF-named or T31 filers (frame B);
  - the newest return of T30/T31/T70 and DAF-named filers (batch 37);
  - the newest FY2022+ return of every 501(c)(3) with ≥ $1m assets (batch 38).
- **Not read:** line-6 "No" filers under $1m that fall outside those frames, and the older returns of ≥ $1m filers. **The forward counts are therefore a floor** on returns that put a count in Part I column (a) while answering “No”. They are not a floor on DAF assets missed: most plausible outside-panel rows are operating charities (Long Island Children’s Museum alone is $2.60m of the $15.81m). The batch-38 rate (5 plausible returns, $3.0m, in 126,736 large-filer returns) is an estimate for the unread remainder, not a bound [I] [V wave 39B]
  - The batch-38 frame gives a rough rate for the unread remainder: 9 forward returns among 126,736 newest returns of large line-6 "No" filers, 5 of them plausible and worth $3.0m together.

### 3.2 Forward case, all 44 rows by DAFRC treatment

| DAFRC treatment | Returns | EINs | Accounts | DAF value |
|---|---|---|---|---|
| Panel row at filed value (`panel_row_irs_990`) | 17 | 11 | 501 | $245.14m |
| Panel row imputed | 2 | 2 | 10 | $4.30m (filed) |
| Panel member, no row that FY (all FY2025, after the panel) | 2 | 2 | 16 | $1.97m |
| Outside the panel | 23 | 23 | 3,871,979 | $13.84m |

- **What the outside-panel rows are.**
  - 11 of the 23 outside-panel returns are implausible (counts of 7,900 to 2.9m with no value).
  - The plausible outside-panel rows are, by value: Groundswell (12,808, $10.08m); Long Island Children's Museum (2, $2.60m; batch 38 calls it an unexplained Part I entry); Rivet Global (1, $0.50m); Samaritan Bethany Foundation (14, $0.27m); Washington Heights UMC (13, $0.17m); Reston Raiders Hockey Club (3, $84,689); Engelhard VFD, Girl Grom Surf Club, Challenged Athletes, The Queen's Community Workers, Central Sands Amateur Radio Club and Mercy Flights (one account each, $1,000–$68,114).
  - Except for Groundswell and possibly Samaritan Bethany, these are operating charities using the DAF column [I], as batch 38 found.
- **Panel sponsors answering "No" while DAFRC uses their filed values:**
  - Legacy Global Foundation, FY2023;
  - Community Foundation of Greater New Britain, FY2022–23;
  - Three Valleys Community Foundation, FY2022–24 (FY2025 too, after the panel);
  - Fremont Area Community Foundation, FY2021;
  - Foundation for Appalachian Kentucky, FY2021;
  - Virginia Tech Foundation, FY2021;
  - The Cure Starts Now, FY2023;
  - Leaders of Many, FY2023;
  - Korean American Foundation, FY2022–23;
  - Alpha Epsilon Pi Foundation, FY2022–23;
  - Josiah White's Quakerdale Foundation, FY2022–23.

### 3.3 Reverse case by year and panel

| FY | Returns (in panel / outside) | Value reported without a count |
|---|---|---|
| 2021 | 720 (47 / 673) | $57.96m |
| 2022 | 761 (54 / 707) | $49.71m |
| 2023 | 804 (51 / 753) | $123.20m |
| 2024 | 773 (74 / 699) | $126.41m |
| 2025 | 235 (55 / 180) | $98.25m |
| 2026 | 4 (1 / 3) | $0.14m |

- **Panel overlap.** The panel part overlaps with `blank-schedule-d-panel.csv` (185 blank-only returns, TY2021+). This table is wider: it also counts zero-count and value-only returns.
- **SOI agreement.** The SOI value agrees with the XML for 3,160 reverse returns ("Y"). 3 are "N" in SOI, and 134 are not in SOI yet.

---

## 4. Does DAFRC or SOI drop these returns?

- **DAFRC.** DAFRC's data come from the GivingTuesday 990 Data Lake, which "contains select 990 fields for all Part I, Schedule D filers".
  - A filer counts as a sponsor if it "filed Part I (a) of Schedule D in FY 2024 or FY 2023, reported at least $1 of DAF assets", subject to vetting. The rules for non-respondents are "$1 million or more in DAF assets", or all four Part I fields filled and DAF grants ≤ organisational grants for three consecutive years.
  - The vetting text does not mention Part IV line 6 ([Updated Analysis Technical Appendix](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Technical-Appendix.pdf), pp. 2–4) [F].
  - So a line-6 "No" return is in scope for DAFRC whenever its Part I is filled. The data confirm this: 17 returns ($245.1m) are carried at filed value.
  - DAFRC misses forward-case filers for other reasons. The filer may not be vetted (Groundswell had no FY2023 Part I and its FY2024 Part I arrived by amendment on 2026-01-28), or it may not be a sponsor. Groundswell’s original TY2024 return (202513219349318726) was e-filed on 2025-11-17, after DAFRC’s 1 October 2025 cut-off, with line 6 = 0 and no Part I. The spring 2026 update replaced only submitted or imputed values with data available by 1 March 2026 and did not re-vet [F] [V wave 39B]
  - DAFRC's data-quality rules delete counts ≤ 0 and assets < $1 and then impute. Reverse-case returns at panel sponsors are therefore imputed or closed, not taken as zero (batch 33).
- **IRS SOI annual extract.**
  - The Form 990 extract documentation lists `dnradvisedfundscd`, "Donor advised funds?", from 990 Core Pt IV-6. It has no Schedule D field: every schedule field in the documentation is Schedule A ([25eofinextractdoc.xlsx](https://www.irs.gov/pub/irs-soi/25eofinextractdoc.xlsx), sheet "990") [F].
  - Any DAF universe drawn from the extract can only key on line 6. All 34 forward returns that appear in the extract carry "N" there, and the other 10 are not yet in any extract.
  - The page also says IRS processing "can result in differences between the information as originally reported and the data on this extract" ([SOI extract page](https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data)) [F]. Here that made no difference to the forward rows.
  - **SOI keyed on line 6 therefore drops all 44 forward returns** and admits all 3,160 reverse returns that it lists.
- **Repo consequence.** P-MOR-01's outside-DAFRC estimate used the SOI "Y" selection (`non-dafrc-daf-filers-summary.csv`). It therefore omits the plausible outside-panel forward returns [C]:
  - FY2021: $0.67m against $477.0m excluding SDG Impact Fund (0.14%);
  - FY2022: $2,000 against $383.7m;
  - FY2023: $68,114 against $152.7m (0.04%);
  - FY2024: $10.09m against $343.8m (2.9%), almost all Groundswell.
  - On assets no headline changes. **On accounts it matters for FY2024:** Groundswell's 12,808 accounts exceed P-MOR-01's entire FY2024 non-DAFRC account count (11,992), so the outside-DAFRC account total for FY2024 roughly doubles, to 24,800 (11,992 + 12,808), and its DAF assets rise from $343.8m to $353.9m (`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`). [V wave 40A]

---

## 5. Limits

- **Forward coverage.** Forward coverage is 13.6% of Form 990 EIN-periods, concentrated where DAFs are likely (§3.1). The forward counts are a floor. Small (under $1m), old, non-CF operating charities answering "No" were not read.
- **FY2025–26 are partial.** The IRS index for those periods is still filling, and several 2026 filings are not in any SOI extract.
- **The frames cache cannot separate blank from 0.** For frame-only returns, the reverse subcases `part_i_daf_blank` and `count_and_value_zero_or_blank` may be swapped. Both count as reverse.
- **`no_schedule_d` is never observed,** but only some sources record whether Schedule D is present.
- **Plausibility is mechanical.** Plausible means value ≥ count > 0. It does not establish that the filer is a sponsor. The sponsor verdicts are those of batch 37, batch 38 and frame A [I].
- **The reverse carry-forward is a proxy [I].** It is wrong for sponsors that really emptied their DAFs (Ayco).
- **Effective-return rule.** The rule uses OBJECT_ID order, not the e-file timestamp, because one cache lacks timestamps.
- **No new XML scan was run.** The only new reads were the three spot checks.

---

## 6. Data dictionary: `line6-vs-schedule-d-2026-11-19.csv`

One row per effective Form 990 return (FY ≥ 2021) in the forward or reverse case. Sorted by case, EIN and tax period.

| Column | Meaning |
|---|---|
| case | `forward` (line 6 not Yes, Part I count > 0) or `reverse` (line 6 Yes, count missing or 0) |
| subcase | forward: `line6_no` or `line6_blank`. reverse: `no_schedule_d`, `part_i_daf_blank`, `count_missing_or_zero_value_positive` or `count_and_value_zero_or_blank` |
| ein, name | Filer EIN (9 digits); name from the IRS index, else from the XML |
| fiscal_year, tax_period | Year of the tax-period end (DAFRC convention); YYYYMM |
| return_object_id, amended, return_ts | Effective return; amended indicator as parsed; e-file timestamp (blank where the cache lacks it) |
| line6_raw, line6 | `DonorAdvisedFundInd` as filed; normalised Y / N / blank |
| soi_line6, soi_extract_file | `dnradvisedfundscd` in the SOI extract for (EIN, tax period); `not_in_soi` if absent; file name |
| sched_d_present | 1/0 where the source records it, else blank |
| daf_count, daf_eoy, daf_contributions, daf_grants | Schedule D Part I lines 1–4, column (a); blank = not filed |
| total_assets_eoy | Form 990 Part X line 16(B) |
| plausible | forward only: yes if count > 0, value > 0 and value ≥ count |
| in_dafrc_panel, dafrc_row_same_fy | EIN anywhere in DAFRC FY2019–2024; DAFRC row for the same FY |
| dafrc_source_eoy_same_fy, dafrc_eoy_same_fy, dafrc_accounts_same_fy, dafrc_status_same_fy | DAFRC's provenance flag, asset value, account count and operating status for that FY |
| line6_screen_drops | forward only: yes if a line-6-keyed screen (SOI value, else XML value) would exclude the return |
| dafrc_captures_same_fy | forward only: `panel_row_irs_990`, `panel_row_imputed`, `panel_no_row_same_fy` or `outside_panel` |
| prior_positive_period, prior_positive_daf_count, prior_positive_daf_eoy | reverse only: latest earlier effective return of the same EIN with count and value > 0 (carry-forward proxy) |
| ein_line6_yes_in_any_return_read | yes if any effective return read for the EIN answers line 6 Yes |
| returns_read_same_period | Returns read for the same EIN and period (more than 1 = original plus amended) |
| unread_later_return_in_index | yes if the index lists a later 990 OBJECT_ID for the EIN and period that was not read |
| sources | Inputs that parsed this OBJECT_ID (§2.1 tags) |
| xml_url | GivingTuesday mirror URL of the return |

---

## 7. Source register

| Source | URL | Used for |
|---|---|---|
| DAFRC Annual DAF Report 2025, Updated Analysis, Technical Appendix | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Technical-Appendix.pdf | Data acquisition (GT 990 Data Lake, "all Part I, Schedule D filers"), vetting rules, data checks, imputation |
| DAFRC Annual DAF Report 2025, Technical Appendix (original) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Technical-Appendix.pdf | Same rules in the first edition |
| DAFRC Updated Analysis memo | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf | FY2023 market total ($256.39bn) context |
| DAFRC dataset (repo copy `dafrc-sponsor-schedule-d-fy2019-2024.csv`) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Panel membership, same-FY rows and provenance |
| IRS SOI annual extract page | https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data | Extract scope and processing caveat |
| IRS SOI extract documentation 2025 | https://www.irs.gov/pub/irs-soi/25eofinextractdoc.xlsx | `dnradvisedfundscd` = Pt IV-6; no Schedule D fields |
| IRS SOI Form 990 extracts 2020–2025 | https://www.irs.gov/pub/irs-soi/{20..25}eoextract990.zip | SOI line-6 value per (EIN, tax period) |
| IRS TEOS e-file index | https://apps.irs.gov/pub/epostcard/990/xml/{2019..2026}/index_{YYYY}.csv | EIN and period mapping, denominators, unread later returns |
| Legacy Global Foundation FY2023 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443209349326279_public.xml | 347 DAFs, $218,867,001, line 6 = 0 |
| Groundswell amended TY2024 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640289349301029_public.xml | 12,808 DAFs, $10,084,314, line 6 = 0 |
| Mitchell Hamline FY2024 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202531329349301983_public.xml | 4 DAFs, $4,266,549, line 6 = 0 (DAFRC imputed $3,679,466) |
| Every other row | the `xml_url` column of the CSV | Return-level evidence |
