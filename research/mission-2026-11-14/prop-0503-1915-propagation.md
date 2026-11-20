# prop-0503-1915: propagating the refined exception proxy (P-G0503-06) and Groundswell's FY2024 accounts (P-G1915B04-02)

**Date:** 2026-11-19 · **Task:** prop-0503-1915 · **Queue items:** P-G0503-06 (from [queue-proposals-g0503-0501.csv](../../data/mission-2026-11-14/queue-proposals-g0503-0501.csv)) and P-G1915B04-02 (from [queue-proposals-g1915b-04.csv](../../data/mission-2026-11-14/queue-proposals-g1915b-04.csv)).
**Status:** proposal only. No existing document or CSV was edited. Every change is listed under **Exact corrections** (end of this note) for a later apply step.
**Builds on:** [g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md) with its wave-39C notes ([validation-wave39c-report.md](validation-wave39c-report.md)); [g1915b-04-line6-vs-schedule-d.md](g1915b-04-line6-vs-schedule-d.md) with its wave-39B notes ([validation-wave39b-report.md](validation-wave39b-report.md)); [full-universe-990-harvest-and-corrected-totals.md](full-universe-990-harvest-and-corrected-totals.md) §4 (P-MOR-01).

**Outputs**
- This note, with 30 Find / Replace items in 7 files (see **Exact corrections**). Every Find was checked by script to occur exactly once, including when the items are applied in order.
- [`data/mission-2026-11-14/non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`](../../data/mission-2026-11-14/non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv): 6 rows (FY2020–2025), 31 columns (§6).
- [`data/mission-2026-11-14/queue-proposals-prop-0503-1915.csv`](../../data/mission-2026-11-14/queue-proposals-prop-0503-1915.csv): P-P0503-1915-01..05.

**Labels:** **[F]** filed value; **[C]** computed by script; **[I]** inference.

---

## 1. Answers in brief

| Item | Result |
|---|---|
| **P-G0503-06**: where the old exception-proxy figures still stand without a governing note | **22 items in 4 files**: 18 in `gap19-exception-load-proxy.md` (§0 core and recent-ruling cells, §3.1 note, table rows and by-year line, §3.2 all-sponsor row, §4 four-national table, per-sponsor rows and reading, regeneration table); 2 in `DAF-INDUSTRY-REPORT-2026-11.md` (§4 exception share; §11.30 pointer); 2 in `strategic-synthesis.md` (claim A5; falsifier B). |
| … already carrying a governing note | Wave 39C's own items were all applied before this pass: gap19 §0 fiscal-sponsor bullet, four-national and count-side cells, reading note and §3.1 fiscal-sponsor row; strategic-synthesis §0 bullets and item 10; FINAL-STATUS exception bullet; g0401-g0502 limit 6; report §11.50. Nothing further is proposed for them. |
| **P-G1915B04-02**: FY2024 outside-DAFRC totals with Groundswell's amended TY2024 Schedule D Part I | **Accounts 11,992 → 24,800** (+12,808, +106.8%); **DAF assets $343,808,451 → $353,892,765** (+$10,084,314); contributions $151,316,519 → $161,008,431 (+$9,691,912); grants unchanged at $110,820,269 (Groundswell leaves Schedule D Part I line 3 blank; its Part I line 13 grants are $4,463,378) [V wave 40A]; share of DAFRC FY2024 assets 0.105% → 0.108% [C]. Filers reporting a DAF value: 413 → 414; median $106,122 → $106,928; 373 under $1m either way [C]. |
| … repo figures citing that total | **8 items in 4 files**: full-universe §4 FY2024 table row, footnote, limit and data dictionary; g1915b-04 §4; direction-long-tail-sponsors §2 and limits; FINAL-STATUS line-6 bullet. |
| Governing figures used (P-G0503-06, as instructed and as in the refinements note) | Core 7.76% of lines / 11.61% of dollars; new organisations only 6.80% / 11.00%; fiscal-sponsor dollar ÷ count ratio 4.4×, or 4.0× without the large-programme hosts; time-correct recent ruling 4.14% / 5.34%; four-national like-for-like about 4.2%, or about 3.9% without the large-programme hosts. |

---

## 2. Method

### 2.1 P-G0503-06 (exception proxy)
1. Read the refinements note in full, including its 15 applied wave-39C notes, and the wave-39C report, whose Exact corrections cover gap19, strategic-synthesis, FINAL-STATUS, g0401-g0502 and the report.
2. Grepped `research/` (Markdown) for the nine strings named in the brief: `7.41%`, `10.96%`, `11.0%`, `10.7×`, `10.7x`, `1.30%`, `4.78%`, `3.6%`, `11.16%`. 117 hit lines outside the validation reports and the refinements note itself. Further greps covered variant phrasings: `10.72`, `11.2% of dollars`, `0.47% of`, `7.4% of`, `review-need`, `exception-load`.
3. Each hit was classed by reading its context (§3): an exception-proxy figure **with** a governing note on the same line or cell; one **without** (an item is proposed); or an **unrelated** use of the same number (for example 13.6% religion shares, 3.6% reply rates, 23.6% growth).
4. The values used in the new text are the governing figures above, plus values read directly from the refinements note (§3.1–§4) and, for the four per-sponsor rows of gap19 §4 and the FY2023/FY2024 core, from `exception-proxy-refined-2026-11-19.csv` (sponsor rows for EINs 110303001, 237825575, 311640316, 232888152; `fiscal_sponsor_any_share_of_sched_i_usd`, `any_core_*`, `any_*`). The base columns of the same rows reproduce the existing gap19 table exactly (for example Fidelity 1.79% and 7.55% / 8.32%), which confirms the column mapping [C].

### 2.2 P-G1915B04-02 (Groundswell)
1. Re-read Groundswell's amended TY2024 return from the GivingTuesday mirror (robots.txt HTTP 404, no rules; user agent `research-script/1.0`; HTTP 200, 68,035 bytes). It gives EIN 871530516, tax period end 2024-12-31, `AmendedReturnInd` X, `ReturnTs` 2026-01-28T13:35:16-06:00, `DonorAdvisedFundInd` 0, `DonorAdvisedFundsHeldCnt` 12808, `DonorAdvisedFundsContriAmt` 9691912, `DonorAdvisedFundsVlEOYAmt` 10084314, and no grants tag [F]. These match the repo's `line6-vs-schedule-d-2026-11-19.csv` row.
2. A stdlib, functional script (scratchpad `qprop/build_gs.py`) then:
   - recomputed the FY2024 sums of `non-dafrc-daf-filers-990.csv` (`reports_daf_value` rows) and matched the summary exactly: 413 filers, $343,808,451, 11,992 accounts, $151,316,519 contributions, $110,820,269 grants [C];
   - confirmed Groundswell is **not** already in `non-dafrc-daf-filers-990.csv` (its SOI line 6 is "N", so P-MOR-01 never selected it), so there is no double count;
   - wrote the new CSV: all original columns, the FY2024 value columns increased by Groundswell's amounts and the asset share recomputed on DAFRC's FY2024 $327,870,852,179; the SOI-only values kept in `soi_y_only_*` columns; the addition itself in `line6_no_additions_*` columns.
3. Grepped the whole repo (`.md`, `.csv`, `.py`, `.json`) for `11,992`, `11992`, `343.8`, `343,808`, `151,316`, `110,820` and `24,800`, and research Markdown for "non-DAFRC" / "outside DAFRC" near FY2024 figures. Every research-document hit that states the FY2024 total gets an item; hits in other meanings (GS Philanthropy Fund's ~24,800 grants, a $24,800 tax bracket, numeric substrings in unrelated CSVs) are left alone.

### 2.3 Checks on the corrections (scratchpad `qprop/corrections.py`)
- Each Find occurs exactly once in its file, also when all 30 items are applied in order to an in-memory copy.
- No Find or Replace value contains a straight double quote or a raw newline; the one multi-line Replace writes newlines as `\n`.
- Every Replace ends with `[prop-0503-1915]`. Table-row Finds stop before the row's final ` |`, so the cell boundary stays outside the replaced text.

---

## 3. Hit-by-hit decisions (P-G0503-06)

| File | Hits (line) | Decision |
|---|---|---|
| `gap19-exception-load-proxy.md` | §0 core cell (40); recent-ruling bullet (41); §3.1 note (125); recent-ruling row (132); core-union row (136); §3.1 by-year core (166); §3.2 all-sponsor row (185); §4 named-FS row (282), sum row (286), count row (287), per-sponsor rows (293–296), reading 1, 2 and 3 (299, 300, 304); regeneration table (407) | **No governing note → 18 items** |
| same | fiscal-sponsor bullet (41), four-national cell (45), count-side cell (46), reading (49), fiscal-sponsor row (133) | Already carry [V wave 39C] notes; none proposed |
| `DAF-INDUSTRY-REPORT-2026-11.md` | §4 exception share (161) | **No note → 1 item** (the brief's named target) |
| same | §11.30 (992: 7.4% / 11.0%, 3.6%) | Validated batch summary; wave 39C left it and put the refined figure in §11.50. **1 short pointer item** to §11.50, no figures replaced. Wave 40A rejects this item: §11.30 is a per-wave validated summary (each §11.30–§11.50 paragraph carries only its own wave tag), and wave 39C left it unchanged on purpose [V wave 40A] |
| same | §11.50 | Is the governing summary; nothing proposed |
| same | 810, 840, 1326–1327 (13.6% religion / NY) | Unrelated |
| `strategic-synthesis.md` | A5 row (112), falsifier B row (223) | **No note → 2 items** |
| same | §0 bullets (30–31), item 10 (94) | Already carry [V wave 39C] notes |
| `FINAL-STATUS.md` | exception-load bullet (180) | Already carries [V wave 39C] note |
| `g0401-g0502-ai-routing-and-per-grant.md` | inputs line (16: 7.41% / 10.96%) | Describes the base the study used, which is correct; limit 6 (line 382) carries the governing note. No item. Its per-grant results rest on the base flags (queue P-P0503-1915-04) |
| same | 197 (3.6% of draws), 317 (1.30% unexplained) | Unrelated |
| `gap19-11-consistency-pass.md` | 112, 149, 309, 313, 496–497, 560, 573 | A dated consistency-pass record whose Find / Replace texts quote earlier wording; treated as a history record and not edited |
| `gap19-ai-calibration.md` (47) and 37 other files | 3.6%, 11.0%, 1.30%, 4.78%, 13.6%, 23.6%, 43.6% and similar | Unrelated uses (reachability shares, NTEE or band shares, growth rates, reply rates, fee tiers, DAF money abroad 4.78%) |
| `validation-wave*-report.md`, registers, changelogs | — | History records; excluded by rule |

**Not changed on purpose.** The parent figures (7.41% / 10.96%, 25.08% / 19.72%, 10.7×, 3.6%) remain correct on their own definitions, as wave 39C noted. Every item adds the refined value beside the old one rather than deleting it.

---

## 4. Results (P-G1915B04-02)

FY2024 outside-DAFRC totals [C] (`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`):

| Measure | SOI line-6 "Yes" filers only (P-MOR-01) | + Groundswell amended TY2024 | Change |
|---|---|---|---|
| Filers reporting a DAF value | 413 | 414 | +1 |
| DAF accounts | 11,992 | **24,800** | +12,808 (+106.8%) |
| DAF assets (EOY) | $343,808,451 | **$353,892,765** | +$10,084,314 |
| … excluding filers ≥ $1bn | $343,808,451 | $353,892,765 | same |
| DAF contributions | $151,316,519 | $161,008,431 | +$9,691,912 |
| DAF grants | $110,820,269 | $110,820,269 | 0 (no grants amount filed) |
| Share of DAFRC FY2024 DAF assets ($327.87bn) | 0.105% | 0.108% | +0.003 pp |
| Median DAF value per filer | $106,122 | $106,928 | +$806 |
| Filers under $1m | 373 | 373 | 0 |

- The arithmetic of wave 39B (11,992 + 12,808 = 24,800) is exact, so "about 24,800" becomes "24,800" in the proposed text.
- Groundswell's accounts average $787 ($10,084,314 / 12,808) [C]. These low-balance accounts raise the same comparability question as processor accounts (b40n13-03-g1913-03 §4.3), so account totals that include them should say so [V wave 40A] Whether they are DAFs in the DAFRC sense is not settled here (queue P-P0503-1915-02).
- FY2020–2023 and FY2025 rows are unchanged; their `line6_no_additions_returns` is 0.

---

## 5. Limits

- **Only Groundswell is added**, as briefed. g1915b-04 found two further plausible FY2024 outside-panel line-6 "No" returns (together 2 accounts and about $5k) and smaller FY2021–23 ones; they are not in the new CSV (P-P0503-1915-01).
- **FY2024 stays incomplete.** The SOI selection lacks returns processed in 2026 (`fy_complete_in_soi` = 0). Groundswell came in only by reading Schedule D directly (P-P0503-1915-03).
- **Status counts are SOI counts.** In the new CSV the status-count columns (`n_reports_daf_value` and so on) still describe SOI line-6 "Yes" returns; the added return sits in `line6_no_additions_*`. A reader summing filers should add `line6_no_additions_returns`.
- **Groundswell's sponsor status is inference.** Its accounts are low-value and it answers line 6 "No"; g1915b-04 classes it with "possibly Samaritan Bethany" as the only likely sponsor among the outside-panel rows [I].
- **Exception proxy items are additive notes.** They do not recompute anything; they carry figures already computed and validated (wave 39C) or read from the refined CSV. The per-grant figure (7–8.5% of grants) is still on base flags.
- **Grep coverage.** The search was literal on the listed strings and variants. A figure restated in other words (for example "about a tenth of dollars") would be missed.
- **Nothing was applied.** The 30 items are proposals; the apply step must re-run the uniqueness check, since other agents may edit the same files first.

---

## 6. Data dictionary: `non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`

One row per FY 2020–2025 (6 rows). Columns 1–20 are those of `non-dafrc-daf-filers-summary.csv` ([full-universe §data dictionary](full-universe-990-harvest-and-corrected-totals.md)); only FY2024's value columns differ.

| Column | Meaning |
|---|---|
| `fiscal_year`, `fy_complete_in_soi` | DAFRC fiscal year; 1 if the SOI extracts for that FY are complete |
| `soi_yes_returns_dafrc_eins`, `soi_yes_returns_non_dafrc` | SOI line-6 "Yes" returns at DAFRC / non-DAFRC EINs |
| `n_reports_daf_value` … `n_xml_not_mirrored` | Status counts of the non-DAFRC SOI "Yes" returns (unchanged; SOI universe only) |
| `non_dafrc_daf_assets`, `non_dafrc_daf_assets_excl_ge_1bn` | Sum of Schedule D Part I EOY DAF value; FY2024 **includes** Groundswell |
| `non_dafrc_daf_accounts`, `non_dafrc_daf_contributions`, `non_dafrc_daf_grants` | Sums of Part I lines 1, 2, 3; FY2024 includes Groundswell |
| `dafrc_sponsors_fy`, `dafrc_daf_assets_fy` | DAFRC sponsor count and DAF assets for the FY |
| `non_dafrc_assets_pct_of_dafrc` | `non_dafrc_daf_assets` ÷ `dafrc_daf_assets_fy` (FY2024 recomputed) |
| `filers_ge_1bn` | Non-DAFRC filers with ≥ $1bn of DAF value |
| `soi_y_only_non_dafrc_daf_assets`, `_accounts`, `_contributions`, `_grants`, `soi_y_only_non_dafrc_assets_pct_of_dafrc` | The original P-MOR-01 values (SOI line-6 "Yes" selection only) |
| `line6_no_additions_returns` | Returns added from outside the SOI "Yes" selection (1 in FY2024, else 0) |
| `line6_no_additions_accounts`, `_daf_assets`, `_contributions`, `_grants` | Their Schedule D Part I values (FY2024: Groundswell; grants 0 because the tag is absent) |
| `line6_no_additions_detail` | Name, EIN, OBJECT_ID, e-file date, filed line 6 value and XML URL |

---

## 7. Source register

| ID | Source | URL | Use | robots.txt (2026-11-19) |
|---|---|---|---|---|
| S1 | Groundswell Charitable Foundation, amended TY2024 Form 990 (OBJECT_ID 202640289349301029) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640289349301029_public.xml | 12,808 DAFs; $10,084,314 EOY; $9,691,912 contributions; line 6 = 0; amended X; e-filed 2026-01-28 | HTTP 404 (no rules); user agent `research-script/1.0` |
| S2 | IRS SOI Form 990 extract 2025 (P-MOR-01 selection; Groundswell "N") | https://www.irs.gov/pub/irs-soi/25eoextract990.zip | Why Groundswell is absent from the SOI selection (via repo CSV) | per g1915b-04 §2.3; not re-fetched |
| S3 | DAFRC Annual DAF Report 2025, Updated Analysis dataset | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | FY2024 DAFRC DAF assets $327.87bn (repo copy via the summary CSV) | per g1915b-04 §2.3; not re-fetched |
| S4 | Fiscal Sponsor Directory, NCCS BMF archive, IRS revocation list and e-file index (governing figures) | https://fiscalsponsordirectory.org/all-fiscal-sponsors-alpha-ordered/ ; https://nccs.urban.org/nccs/catalogs/catalog-bmf.html ; https://apps.irs.gov/pub/epostcard/data-download-revocation.zip ; https://www.irs.gov/charities-non-profits/form-990-series-downloads | Sources of the refined proxy (refinements note §8); not re-fetched here | as recorded in the refinements note §8 |
| R1 | Repo: `exception-proxy-refined-2026-11-19.csv`, `exception-load-proxy-2026-11-19.csv` | repo | Per-sponsor and by-year refined values; column mapping check | — |
| R2 | Repo: `non-dafrc-daf-filers-summary.csv`, `non-dafrc-daf-filers-990.csv`, `line6-vs-schedule-d-2026-11-19.csv` | repo | FY2024 base totals, recomputation check, Groundswell row | — |
| R3 | Repo: refinements note, g1915b-04 note, validation waves 39B and 39C reports | repo | Governing figures and already-applied notes | — |

- Not used: sec.gov, crt.sh, certspotter. No outreach, no logins.

---

## Exact corrections

### `research/mission-2026-11-14/gap19-exception-load-proxy.md`

- **Find:** "7.2% / 9.6% excluding SVCF and university/hospital sponsors [V wave 32A]"
- **Replace with:** "7.2% / 9.6% excluding SVCF and university/hospital sponsors [V wave 32A]<br>With the EIN-keyed fiscal-sponsor list and time-correct rulings ($92.72bn base) the core is **7.76% / 11.61%** (gap +3.85 pp), or 6.80% / 11.00% counting only true new organisations as recent; 7.74% / 11.35% without 50CAN, Global Impact, NEO Philanthropy and Myriad USA ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [prop-0503-1915]"

- **Find:** "- Recent ruling: 4.8% vs 5.9% (1.2×)."
- **Replace with:** "- Recent ruling: 4.8% vs 5.9% (1.2×). Dated with archived monthly BMF files ($92.72bn base), rulings recent at grant time are 4.14% vs 5.34%, and true new organisations 3.16% vs 4.72% ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [prop-0503-1915]"

- **Find:** "core is 7.41% / 10.96% (gap +3.55 pp); and FY2024 core is 7.36% / 9.73% [V wave 32A]"
- **Replace with:** "core is 7.41% / 10.96% (gap +3.55 pp); and FY2024 core is 7.36% / 9.73% [V wave 32A]. With the EIN-keyed fiscal-sponsor list and time-correct rulings: core 7.76% / 11.61%, broad 24.79% / 19.85%, FY2024 core 7.69% / 10.37% ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [prop-0503-1915]"

- **Find:** "| BMF ruling ≤24 months before the grant year (or later) | 29,082 | $5.52bn | 4.78% | 5.94% | +1.16 | 1.24×"
- **Replace with:** "| BMF ruling ≤24 months before the grant year (or later) | 29,082 | $5.52bn | 4.78% | 5.94% | +1.16 | 1.24× (recent at grant time on archived BMF snapshots, $92.72bn base: 25,185 lines, $4.95bn, 4.14% / 5.34%; true new organisations 3.16% / 4.72%) [prop-0503-1915]"

- **Find:** "| **Any (core union)** | **45,104** | **$10.37bn** | **7.41%** | **11.16%** | **+3.75** | **1.51×**"
- **Replace with:** "| **Any (core union)** | **45,104** | **$10.37bn** | **7.41%** | **11.16%** | **+3.75** | **1.51×** (refined on $92.72bn: 47,228 lines, $10.77bn, 7.76% / 11.61%, +3.85 pp; new organisations only 6.80% / 11.00%) [prop-0503-1915]"

- **Find:** "- Core: FY2023 7.5% / 12.4%; FY2024 7.4% / 10.1%."
- **Replace with:** "- Core: FY2023 7.5% / 12.4%; FY2024 7.4% / 10.1%. Refined ($92.72bn base): FY2023 7.84% / 13.08%; FY2024 7.69% / 10.37% ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [prop-0503-1915]"

- **Find:** "| 7.41% | 11.16% | +3.8 | 16.36% (13.39–21.08%) | 19.68% (15.48–25.18%)"
- **Replace with:** "| 7.41% | 11.16% | +3.8 | 16.36% (13.39–21.08%) | 19.68% (15.48–25.18%) (refined on $92.72bn: core 7.76% / 11.61%, broad 24.79% / 19.85%) [prop-0503-1915]"

- **Find:** "| Named fiscal sponsors ÷ Schedule I $ | ≈1.20% | **1.50%** (same 19-host list) | 1.47% of $, 0.04% of lines"
- **Replace with:** "| Named fiscal sponsors ÷ Schedule I $ | ≈1.20% | **1.50%** (same 19-host list; 2.10% on the EIN-keyed host list, 1.82% without 50CAN, Global Impact, NEO Philanthropy and Myriad USA) | 1.47% of $, 0.04% of lines (EIN-keyed list: 2.05% of $, 0.24% of lines) [prop-0503-1915]"

- **Find:** "| **Sum / union** | **≈2.5–3%** of $ | **≈3.6%** of $ (simple sum, as in the existing method) | **Core 10.0% of $, 7.3% of lines; broad 17.8% of $, 28.3% of lines**"
- **Replace with:** "| **Sum / union** | **≈2.5–3%** of $ | **≈3.6%** of $ (simple sum, as in the existing method; ≈4.2% with the EIN-keyed fiscal-sponsor list, ≈3.9% without the four large-programme hosts) | **Core 10.0% of $, 7.3% of lines; broad 17.8% of $, 28.3% of lines** (refined: core 10.62% / 7.55%; broad 18.00% / 27.79%) [prop-0503-1915]"

- **Find:** "Foreign + fiscal-sponsor lines: 0.47% of big-4 lines"
- **Replace with:** "Foreign + fiscal-sponsor lines: 0.47% of big-4 lines (0.67% with the EIN-keyed fiscal-sponsor list) [prop-0503-1915]"

- **Find:** "| Fidelity Charitable | 0.50% (FY6/2025: 0.48%) | 1.79% (1.27%) | 7.55% / 8.32% | 30.20% / 16.78%"
- **Replace with:** "| Fidelity Charitable | 0.50% (FY6/2025: 0.48%) | 1.79% (1.27%) | 7.55% / 8.32% | 30.20% / 16.78% (refined: named FS 2.39%, core 7.76% / 8.95%, broad 29.65% / 17.04%) [prop-0503-1915]"

- **Find:** "| NPT | 7.42% (4.84%) | 2.21% (1.70%) | 9.55% / 15.75% | 22.70% / 20.69%"
- **Replace with:** "| NPT | 7.42% (4.84%) | 2.21% (1.70%) | 9.55% / 15.75% | 22.70% / 20.69% (refined: named FS 3.27%, core 9.84% / 16.74%, broad 22.46% / 21.19%) [prop-0503-1915]"

- **Find:** "| DAFgiving360 | 0.93% (1.23%) | 0.88% (1.05%) | 6.93% / 9.56% | 28.88% / 18.99%"
- **Replace with:** "| DAFgiving360 | 0.93% (1.23%) | 0.88% (1.05%) | 6.93% / 9.56% | 28.88% / 18.99% (refined: named FS 1.21%, core 7.17% / 9.90%, broad 28.43% / 18.99%) [prop-0503-1915]"

- **Find:** "| Vanguard Charitable | 0.21% (0.12%) | 0.30% (0.45%) | 5.68% / 7.34% | 24.54% / 14.17%"
- **Replace with:** "| Vanguard Charitable | 0.21% (0.12%) | 0.30% (0.45%) | 5.68% / 7.34% | 24.54% / 14.17% (refined: named FS 0.62%, core 5.96% / 7.65%, broad 24.20% / 13.77%) [prop-0503-1915]"

- **Find:** "plus slightly higher fiscal-sponsor shares at Fidelity and NPT."
- **Replace with:** "plus slightly higher fiscal-sponsor shares at Fidelity and NPT. On the EIN-keyed fiscal-sponsor list the like-for-like sum is about 4.2% (3.9% without 50CAN, Global Impact, NEO Philanthropy and Myriad USA) ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [prop-0503-1915]"

- **Find:** "**On the briefed categories, it covers only about a third of the core dollar proxy** (3.6% of 10.0%)."
- **Replace with:** "**On the briefed categories, it covers only about a third of the core dollar proxy** (3.6% of 10.0%; about two-fifths, 4.2% of 10.6%, on the refined lists). [prop-0503-1915]"

- **Find:** "is right for foreign and fiscal-sponsor grants (0.47% of lines)."
- **Replace with:** "is right for foreign and fiscal-sponsor grants (0.47% of lines; 0.67% with the EIN-keyed fiscal-sponsor list). [prop-0503-1915]"

- **Find:** "| Core share (lines / dollars) | 7.41% / 10.96%"
- **Replace with:** "| Core share (lines / dollars) | 7.41% / 10.96% (7.76% / 11.61% with the EIN-keyed fiscal-sponsor list and time-correct rulings; 6.80% / 11.00% new organisations only) [prop-0503-1915]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "is 10.0% of their dollars and 11.0% across the top 50 (10.96% after the Greater Horizons correction). [V wave 33B] It measures recipients, not observed review (§11.30; [V wave 32A]). [gap19-11]"
- **Replace with:** "is 10.0% of their dollars and 11.0% across the top 50 (10.96% after the Greater Horizons correction). [V wave 33B] It measures recipients, not observed review (§11.30; [V wave 32A]). [gap19-11] With fiscal sponsors keyed by EIN (the 19 named hosts plus the Fiscal Sponsor Directory) and rulings dated with archived IRS BMF files, the like-for-like measure is about 4.2% (about 3.9% without four hosts with large programmes of their own), and the top-50 core proxy is 7.76% of lines and 11.61% of dollars, or 6.80% / 11.00% counting only true new organisations as recent. Fiscal sponsors' dollar share is 4.4× their count share (4.0× without those hosts), not 10.7×, and rulings recent at grant time are 4.14% of lines and 5.34% of dollars (§11.50; repo [`g0503-0501-exception-proxy-refinements.md`](mission-2026-11-14/g0503-0501-exception-proxy-refinements.md)) [prop-0503-1915]"

- **Find:** "reproduces at 3.6%, about a third of their core 10.0%."
- **Replace with:** "reproduces at 3.6%, about a third of their core 10.0%. (Refined in §11.50: about 4.2% like-for-like and a top-50 core of 7.76% / 11.61%.) [prop-0503-1915]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "FY2023–24 filings reproduce the measure at about 3.6%, and a broader review-need proxy is 10.0% of the four nationals' dollars and 11.0% across the top 50."
- **Replace with:** "FY2023–24 filings reproduce the measure at about 3.6%, and a broader review-need proxy is 10.0% of the four nationals' dollars and 11.0% across the top 50. With EIN-keyed fiscal sponsors and time-correct rulings these become about 4.2% (3.9% without four large-programme hosts), 10.6% and 11.61% (7.76% of lines; 6.80% / 11.00% counting only true new organisations) ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [prop-0503-1915]"

- **Find:** "3.6% like-for-like in FY2023–24 [V wave 33B])."
- **Replace with:** "3.6% like-for-like in FY2023–24 [V wave 33B]). On the EIN-keyed fiscal-sponsor list the like-for-like share is about 4.2% (3.9% without four large-programme hosts) and the review-need proxy 10.6% of the four nationals' dollars and 11.61% across the top 50; neither is a measured exception rate [prop-0503-1915]"

### `research/mission-2026-11-14/full-universe-990-harvest-and-corrected-totals.md`

- **Find:** "| 2024* | 1,235 | 413 | 106 | 42 | 140 | 529 | 4 | $0.34bn | $0.34bn | 11,992 | 0.10%"
- **Replace with:** "| 2024* | 1,235 | 413 | 106 | 42 | 140 | 529 | 4 | $0.34bn (with Groundswell $0.35bn) | $0.34bn ($0.35bn) | 11,992 (with Groundswell 24,800) | 0.10% (0.11%) [prop-0503-1915]"

- **Find:** "which appear only on an amended return e-filed 2026-01-28 that answers line 6 “No” [F] [V wave 39B]"
- **Replace with:** "which appear only on an amended return e-filed 2026-01-28 that answers line 6 “No” [F] [V wave 39B]. Adding that return gives FY2024 totals of 24,800 accounts, $353.9m of DAF assets (0.108% of DAFRC), $161.0m of DAF contributions and unchanged DAF grants of $110.8m (Groundswell reports none) ([`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`](../../data/mission-2026-11-14/non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv)) [prop-0503-1915]"

- **Find:** "FY2024 non-DAFRC accounts roughly double, from 11,992 to about 24,800 [C] [V wave 39B]"
- **Replace with:** "FY2024 non-DAFRC accounts roughly double, from 11,992 to 24,800 (11,992 + Groundswell’s 12,808; `non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`) [C] [V wave 39B] [prop-0503-1915]"

- **Find:** "`dafrc_daf_assets_fy`; `non_dafrc_assets_pct_of_dafrc`; `filers_ge_1bn`; `fy_complete_in_soi`."
- **Replace with:** "`dafrc_daf_assets_fy`; `non_dafrc_assets_pct_of_dafrc`; `filers_ge_1bn`; `fy_complete_in_soi`.\n\n### `non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv` (one row per FY 2020–2025)\nSame columns and rows. In FY2024 the value columns (`non_dafrc_daf_assets`, `_excl_ge_1bn`, accounts, contributions, grants, `non_dafrc_assets_pct_of_dafrc`) add Groundswell Charitable Foundation’s amended TY2024 Schedule D Part I; the status counts stay SOI line-6 “Yes” counts. `soi_y_only_*` keep the original values; `line6_no_additions_*` give the added return ([prop-0503-1915-propagation.md](prop-0503-1915-propagation.md)) [prop-0503-1915]"

### `research/mission-2026-11-14/g1915b-04-line6-vs-schedule-d.md`

- **Find:** "so the outside-DAFRC account total for FY2024 roughly doubles (to about 24,800)."
- **Replace with:** "so the outside-DAFRC account total for FY2024 roughly doubles, to 24,800 (11,992 + 12,808), and its DAF assets rise from $343.8m to $353.9m (`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`). [prop-0503-1915]"

### `research/mission-2026-11-14/direction-long-tail-sponsors.md`

- **Find:** "FY2024 non-DAFRC accounts roughly double (11,992 to about 24,800) [C] [V wave 39B]"
- **Replace with:** "FY2024 non-DAFRC accounts roughly double (11,992 to 24,800 with Groundswell’s 12,808) [C] [V wave 39B] [prop-0503-1915]"

- **Find:** "(`non-dafrc-daf-filers-990.csv`; FY2023: 424 filers, $0.15bn)."
- **Replace with:** "(`non-dafrc-daf-filers-990.csv`; FY2023: 424 filers, $0.15bn). Adding Groundswell Charitable Foundation, which reports DAFs only on an amended return answering line 6 “No”, gives 414 filers, $0.35bn, median $107k and 24,800 accounts (`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`) [prop-0503-1915]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "- Non-DAFRC FY2024 accounts are about 24,800."
- **Replace with:** "- Non-DAFRC FY2024 accounts are 24,800: 11,992 at line-6 “Yes” filers plus Groundswell’s 12,808, with $353.9m of DAF assets (`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`) [prop-0503-1915]"
