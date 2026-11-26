# Validation wave 40A: propagation (prop-0503-1915) and DAF grant schema / processor accounts (b40n13-03-g1913-03)

**Validator:** independent-validation-agent-wave40a · **Date:** 2026-11-19 · **Register:** [`validation-register-wave40a.csv`](../../data/mission-2026-11-14/validation-register-wave40a.csv) (34 claims)

**Checked:** [prop-0503-1915-propagation.md](prop-0503-1915-propagation.md) and `non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`; [b40n13-03-g1913-03-schema-and-processor-accounts.md](b40n13-03-g1913-03-schema-and-processor-accounts.md), `daf-grant-schema-map-2026-11-19.csv`, `processor-account-counts-2026-11-19.csv` and `scripts/mission_b40n13_03_g1913_03_build.py`. Nothing was committed or pushed.

## Counts

| Result | Claims |
|---|---|
| confirmed | 25 |
| partially_confirmed | 5 |
| contradicted | 4 |
| unverifiable | 0 |
| **Total** | **34** |

16 claims cover the propagation note (V40A-01 to -16) and 18 the schema and processor study (V40A-17 to -34).

| Items | Accept | Modify | Reject |
|---|---|---|---|
| Propagation (30) | 23 | 6 | 1 |
| Schema doc §6 (13) | 7 | 6 | 0 |
| **Total (43)** | **30** | **12** | **1** |

Eight further corrections apply to the two studies themselves (C01–C08), and one summary goes into the report (§11.51).

## Method

- **Uniqueness.** All 30 propagation Finds and all 13 schema-doc Finds were parsed from the notes and counted in the current target files, alone and with earlier items applied in order. All occur exactly once.
- **Propagation figures** were checked against `exception-proxy-refined-2026-11-19.csv` (all-scope, big-4 and four sponsor rows), the refinements note and the wave-39C report. The FY2024 totals were recomputed from `non-dafrc-daf-filers-990.csv` plus Groundswell’s XML, which was re-fetched (robots.txt 404; HTTP 200, 68,035 bytes).
- **Schema and processor study.** The validator checked robots.txt first, then fetched:
  - IRS i990si and i990sd;
  - Endaoment’s async-grant page and its OpenAPI JSON;
  - the two 360Giving pages and the GSDM v1.3 workbook;
  - Benevity’s SSI PDF;
  - the Chariot, For Good and Givinga pages.
- **XML.** The validator fetched 13 Form 990 XMLs: the study’s 12 plus Blackbaud’s CY2023 return, 202402119349300860.
- **Script re-run.** The build script was re-run in a scratch root on these downloads. Its outputs are byte-identical (md5 `784e7dab…`, `9164a0e6…`) and all 60 quotes match.
- **Corrected panel.** The corrected FY2024 DAFRC panel was rebuilt per EIN from the panel and `dafrc-corrections-itemized.csv`. It sums to 3,309,483.
- **Not used:** crt.sh, certspotter and sec.gov. There was no outreach, and the user agent was never changed. www.grants.gov again failed TLS verification at the proxy, so it was not read. PayPal’s 403 policy page was not retried.

## Findings

### Propagation (prop-0503-1915)

1. **The arithmetic is exact** (V40A-03, -04, -05).
   - The base rows give 413 filers, $343,808,451, 11,992 accounts, $151,316,519 and $110,820,269.
   - With Groundswell: 24,800 accounts, $353,892,765, $161,008,431 and 0.10794% of DAFRC’s $327.87bn. The median is $106,928, and 373 filers are under $1m.
   - The new CSV differs from the original only in the five FY2024 value columns, plus 11 added columns.
2. **Groundswell’s XML confirms every stated tag** (V40A-02).
   - It has no `DonorAdvisedFundsGrantsAmt`. Its Part I line 13 grants are **$4,463,378**, and Schedule I lists 56 grants totalling $1,814,318.
   - “Groundswell reports none” therefore overstates; the item is reworded to “line 3 blank” (P24, C01).
3. **Every refined exception-proxy value matches the CSV** to two decimals (V40A-06 to -08): the core, broad, time-correct, FY2023/24, per-sponsor and big-4 values. The column mapping reproduces the base gap19 table (Fidelity 1.79%, NPT 2.21%, DAFgiving360 0.88%, Vanguard 0.30%).
4. **One placement error** (V40A-09). Item 7 appends pooled-union figures to the *Sponsor median broad count* column of gap19 §3.2. The modified item annotates each pooled cell instead (broad 24.79% / 19.85%, gap −4.9; core 7.76% / 11.61%, +3.85).
5. **One item edits a history record** (V40A-10). Item 20 adds a note inside report §11.30, the wave-32A summary. Each §11.30–§11.50 paragraph carries only its own wave tag, wave 39C left §11.30 alone on purpose, and §11.50 already holds the refined figures. **Rejected.**
6. **Smaller fixes.**
   - Item 1 now carries the refined excl-SVCF / university-hospital core (7.56% / 10.27%).
   - Item 18 links its source.
   - Item 26 no longer says “same columns” (31 vs 20).
   - Items 24 and 30 give the $787 average per Groundswell account.
7. **Interpretation.** 12,808 of the 24,800 accounts (52%) belong to one filer averaging $787. This is the same comparability problem the schema study raises for processors, so account totals that include Groundswell should say so (C03).

### Schema map and processor accounts (b40n13-03-g1913-03)

8. **The external sources confirm the schema map** (V40A-17 to -21).
   - **IRS Schedule I (Rev. 12/2024):** EIN in column (b), an annual cash total in (d), purpose in (h), only for domestic recipients over $5,000, with foreign grants excluded.
   - **Endaoment:** OAS 4.88.0; `requestedAmount` in USDC smallest units; `asyncStatus` is PendingLiquidation / Liquidated / Cancelled; `status` is deprecated, and its enum was PendingReview / Approved / Rejected. So **approval status is no longer exposed** in the API.
   - **360Giving:** 10 required fields, `classifications` and `disbursementTransaction/0/id`. There is no fund or status field, and no version string on the pages.
   - **GSDM FABS** elements and their Required / Conditional flags match.
   - **Benevity SSI (© 2024)** names “American Online Giving Foundation, Inc.” as its US foundation.
9. **All 13 XMLs match the processor CSV** (V40A-22 to -27).
   - Blackbaud’s CY2023 return, which the study did not cite, also has a blank line 1 (C05).
   - Givinga’s amendment changes only the dates, the amended flag and Schedule D Part I.
   - The DAFRC panel’s For Good FY2024 row is imputed from 2023. The CY2024 value of 1 comes from the XML, not the panel (C06).
10. **76.2% recomputes** (V40A-28): 2,522,661 / 3,309,483 = 0.76225. A2 reconciles: 787,978 − 787,517 = 461, which is Blackbaud’s 460 plus For Good’s 1.
11. **The “comparable series” still contains processors** (V40A-29).
    - The other 17 DAFRC processors hold **16,037** corrected FY2024 accounts, not 15,912 (the published figure; R1 moves Dechomai Asset Trust from 181 to 314).
    - All 22 processors hold 2,538,698 (76.7%).
    - The processor-free series is therefore **770,785**; 786,822 removes only the five (C04, C07, C08).
12. **Wrong processor set in two corrections** (V40A-31).
    - gap19-complaints’ five processors are AOGF, PPGF, Blackbaud, Dechomai and For Good, the top five by FY2024 grants. S04 lists Givinga and drops Dechomai.
    - S11 calls the study’s set “the five largest processors”, yet Givinga ranks 11th of 22 by grants, and Blackbaud and For Good are not top five by accounts.
13. **Formatting** (V40A-33).
    - S03 drops the table’s closing pipe and replaces a computed 0.10 with “n/c”.
    - S10 drops the Find’s semicolon, so two clauses run together, and it deletes a [V wave 5] tag.
    - S02’s “imputed rows carry the prior year’s end date” holds for 677 of 709 imputed rows (V40A-32).
14. **Recommendation not to pool processors with sponsors: supported** (V40A-34). None of the five counts “one fund per donor with ongoing advice”. Two qualifications:
    - The sponsor side also holds mass low-balance accounts. The repo’s A3 variant, which applies a unit-based screen, gives 750,473.
    - The DAFRC “Donation Processor” label alone is not a unit test.
    - The treatment should therefore pair the label with a unit screen and say which processors are excluded (C08).

## Accept / modify / reject

| Item | Target | Decision | Reason |
|---|---|---|---|
| P01 | `gap19-exception-load-proxy.md` | modify | Adds the refined excl-SVCF / university-hospital core (7.56% / 10.27%) that matches the Find’s 7.2% / 9.6% |
| P02 | `gap19-exception-load-proxy.md` | accept | 4.14 / 5.34%, 3.16 / 4.72% match the refined CSV |
| P03 | `gap19-exception-load-proxy.md` | accept | 7.76 / 11.61, 24.79 / 19.85, 7.69 / 10.37 match |
| P04 | `gap19-exception-load-proxy.md` | accept | 25,185 lines, $4.95bn match |
| P05 | `gap19-exception-load-proxy.md` | accept | 47,228, $10.77bn, +3.85 pp, 6.80 / 11.00 match |
| P06 | `gap19-exception-load-proxy.md` | accept | FY2023 7.84 / 13.08, FY2024 7.69 / 10.37 match |
| P07 | `gap19-exception-load-proxy.md` | modify | Original text lands in the Sponsor median broad count column; values moved into the matching pooled cells |
| P08 | `gap19-exception-load-proxy.md` | accept | 2.10%, 1.82%, 2.05% / 0.24% match |
| P09 | `gap19-exception-load-proxy.md` | accept | 4.2 / 3.9%, 10.62 / 7.55, 18.00 / 27.79 match |
| P10 | `gap19-exception-load-proxy.md` | accept | 0.67% matches wave 39C |
| P11 | `gap19-exception-load-proxy.md` | accept | All six values match CSV |
| P12 | `gap19-exception-load-proxy.md` | accept | All six values match |
| P13 | `gap19-exception-load-proxy.md` | accept | All six values match |
| P14 | `gap19-exception-load-proxy.md` | accept | All six values match |
| P15 | `gap19-exception-load-proxy.md` | accept | 4.2% / 3.9% match |
| P16 | `gap19-exception-load-proxy.md` | accept | 4.2 / 10.62 ≈ two-fifths |
| P17 | `gap19-exception-load-proxy.md` | accept | 0.67% matches |
| P18 | `gap19-exception-load-proxy.md` | modify | Governing regeneration note: link the source of the refined values |
| P19 | `DAF-INDUSTRY-REPORT-2026-11.md` | accept | All figures match the refinements note and §11.50 |
| P20 | `DAF-INDUSTRY-REPORT-2026-11.md` | reject | Edits §11.30, a per-wave validated summary (history record); §11.50 already carries the figures |
| P21 | `strategic-synthesis.md` | accept | Figures match |
| P22 | `strategic-synthesis.md` | accept | Figures match |
| P23 | `full-universe-990-harvest-and-corrected-totals.md` | accept | $0.35bn and 0.11% match the new CSV |
| P24 | `full-universe-990-harvest-and-corrected-totals.md` | modify | Groundswell does not report none: line 3 is blank and Part I line 13 grants are $4,463,378; adds the $787 average |
| P25 | `full-universe-990-harvest-and-corrected-totals.md` | accept | 24,800 exact |
| P26 | `full-universe-990-harvest-and-corrected-totals.md` | modify | New CSV has 31 columns, not the same columns |
| P27 | `g1915b-04-line6-vs-schedule-d.md` | accept | $343.8m → $353.9m matches |
| P28 | `direction-long-tail-sponsors.md` | accept | Matches |
| P29 | `direction-long-tail-sponsors.md` | accept | 414 filers, median $106,928, 24,800 match |
| P30 | `FINAL-STATUS.md` | modify | Adds the $787 average so the account total is read with its unit |
| S01 | `gap19-complaints-with-denominators.md` | modify | Filed values confirmed; same population is inference; column (a) also holds corporate DAFs |
| S02 | `gap19-complaints-with-denominators.md` | modify | 762 of 767 filed rows end in 2024; 32 imputed rows carry a 2024 end |
| S03 | `gap19-complaints-with-denominators.md` | modify | Keeps the closing pipe and the computed 0.10 instead of n/c |
| S04 | `gap19-complaints-with-denominators.md` | modify | gap19’s five are AOGF, PPGF, Blackbaud, Dechomai, For Good (no Givinga) |
| S05 | `queue-batch38-data-followups.md` | accept | $12,417,069 / 1,421,011 = $8.74; EOY $1,949,239 |
| S06 | `regulation-market-structure-portability.md` | accept | Amended 2025-11-13 1,421,011; original 2025-08-25 blank |
| S07 | `regulation-market-structure-portability.md` | accept | 380,644 and $97,016,071 confirmed |
| S08 | `regulation-market-structure-portability.md` | accept | Filed 380,644 confirmed |
| S09 | `regulation-market-structure-portability.md` | accept | SSI PDF quote confirmed |
| S10 | `strategic-synthesis.md` | modify | Original Replace drops the semicolon and the [V wave 5] tag; made additive |
| S11 | `DAF-INDUSTRY-REPORT-2026-11.md` | modify | Study set is not the five largest; Givinga is 11th by grants |
| S12 | `DAF-INDUSTRY-REPORT-2026-11.md` | accept | Quotes confirmed |
| S13 | `queue-assurance-everyorg-givinga-monitoring.md` | accept | $1.37 confirmed |

## Exact corrections

Final form of every accepted or modified item, plus corrections to the two studies. Apply in the order listed. Item codes: P = prop-0503-1915 item, S = schema-doc §6 item, C = study correction, R = report summary.

### `research/mission-2026-11-14/gap19-exception-load-proxy.md`

- **Find:** "7.2% / 9.6% excluding SVCF and university/hospital sponsors [V wave 32A]"
- **Replace with:** "7.2% / 9.6% excluding SVCF and university/hospital sponsors [V wave 32A]<br>With the EIN-keyed fiscal-sponsor list and time-correct rulings ($92.72bn base) the core is **7.76% / 11.61%** (gap +3.85 pp), or 6.80% / 11.00% counting only true new organisations as recent; 7.56% / 10.27% excluding SVCF and university/hospital sponsors; 7.74% / 11.35% without 50CAN, Global Impact, NEO Philanthropy and Myriad USA ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 40A]"

- **Find:** "- Recent ruling: 4.8% vs 5.9% (1.2×)."
- **Replace with:** "- Recent ruling: 4.8% vs 5.9% (1.2×). Dated with archived monthly BMF files ($92.72bn base), rulings recent at grant time are 4.14% vs 5.34%, and true new organisations 3.16% vs 4.72% ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 40A]"

- **Find:** "core is 7.41% / 10.96% (gap +3.55 pp); and FY2024 core is 7.36% / 9.73% [V wave 32A]"
- **Replace with:** "core is 7.41% / 10.96% (gap +3.55 pp); and FY2024 core is 7.36% / 9.73% [V wave 32A]. With the EIN-keyed fiscal-sponsor list and time-correct rulings: core 7.76% / 11.61%, broad 24.79% / 19.85%, FY2024 core 7.69% / 10.37% ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 40A]"

- **Find:** "| BMF ruling ≤24 months before the grant year (or later) | 29,082 | $5.52bn | 4.78% | 5.94% | +1.16 | 1.24×"
- **Replace with:** "| BMF ruling ≤24 months before the grant year (or later) | 29,082 | $5.52bn | 4.78% | 5.94% | +1.16 | 1.24× (recent at grant time on archived BMF snapshots, $92.72bn base: 25,185 lines, $4.95bn, 4.14% / 5.34%; true new organisations 3.16% / 4.72%) [V wave 40A]"

- **Find:** "| **Any (core union)** | **45,104** | **$10.37bn** | **7.41%** | **11.16%** | **+3.75** | **1.51×**"
- **Replace with:** "| **Any (core union)** | **45,104** | **$10.37bn** | **7.41%** | **11.16%** | **+3.75** | **1.51×** (refined on $92.72bn: 47,228 lines, $10.77bn, 7.76% / 11.61%, +3.85 pp; new organisations only 6.80% / 11.00%) [V wave 40A]"

- **Find:** "- Core: FY2023 7.5% / 12.4%; FY2024 7.4% / 10.1%."
- **Replace with:** "- Core: FY2023 7.5% / 12.4%; FY2024 7.4% / 10.1%. Refined ($92.72bn base): FY2023 7.84% / 13.08%; FY2024 7.69% / 10.37% ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 40A]"

- **Find:** "| *All* | 48 (94) | 608,612 | $92.94bn | 25.08% | 19.90% | −5.2 | 7.41% | 11.16% | +3.8"
- **Replace with:** "| *All* | 48 (94) | 608,612 | $92.94bn | 25.08% (refined, $92.72bn base: 24.79%) | 19.90% (19.85%) | −5.2 (−4.9) | 7.41% (7.76%) | 11.16% (11.61%) | +3.8 (+3.85) [V wave 40A]"

- **Find:** "| Named fiscal sponsors ÷ Schedule I $ | ≈1.20% | **1.50%** (same 19-host list) | 1.47% of $, 0.04% of lines"
- **Replace with:** "| Named fiscal sponsors ÷ Schedule I $ | ≈1.20% | **1.50%** (same 19-host list; 2.10% on the EIN-keyed host list, 1.82% without 50CAN, Global Impact, NEO Philanthropy and Myriad USA) | 1.47% of $, 0.04% of lines (EIN-keyed list: 2.05% of $, 0.24% of lines) [V wave 40A]"

- **Find:** "| **Sum / union** | **≈2.5–3%** of $ | **≈3.6%** of $ (simple sum, as in the existing method) | **Core 10.0% of $, 7.3% of lines; broad 17.8% of $, 28.3% of lines**"
- **Replace with:** "| **Sum / union** | **≈2.5–3%** of $ | **≈3.6%** of $ (simple sum, as in the existing method; ≈4.2% with the EIN-keyed fiscal-sponsor list, ≈3.9% without the four large-programme hosts) | **Core 10.0% of $, 7.3% of lines; broad 17.8% of $, 28.3% of lines** (refined: core 10.62% / 7.55%; broad 18.00% / 27.79%) [V wave 40A]"

- **Find:** "Foreign + fiscal-sponsor lines: 0.47% of big-4 lines"
- **Replace with:** "Foreign + fiscal-sponsor lines: 0.47% of big-4 lines (0.67% with the EIN-keyed fiscal-sponsor list) [V wave 40A]"

- **Find:** "| Fidelity Charitable | 0.50% (FY6/2025: 0.48%) | 1.79% (1.27%) | 7.55% / 8.32% | 30.20% / 16.78%"
- **Replace with:** "| Fidelity Charitable | 0.50% (FY6/2025: 0.48%) | 1.79% (1.27%) | 7.55% / 8.32% | 30.20% / 16.78% (refined: named FS 2.39%, core 7.76% / 8.95%, broad 29.65% / 17.04%) [V wave 40A]"

- **Find:** "| NPT | 7.42% (4.84%) | 2.21% (1.70%) | 9.55% / 15.75% | 22.70% / 20.69%"
- **Replace with:** "| NPT | 7.42% (4.84%) | 2.21% (1.70%) | 9.55% / 15.75% | 22.70% / 20.69% (refined: named FS 3.27%, core 9.84% / 16.74%, broad 22.46% / 21.19%) [V wave 40A]"

- **Find:** "| DAFgiving360 | 0.93% (1.23%) | 0.88% (1.05%) | 6.93% / 9.56% | 28.88% / 18.99%"
- **Replace with:** "| DAFgiving360 | 0.93% (1.23%) | 0.88% (1.05%) | 6.93% / 9.56% | 28.88% / 18.99% (refined: named FS 1.21%, core 7.17% / 9.90%, broad 28.43% / 18.99%) [V wave 40A]"

- **Find:** "| Vanguard Charitable | 0.21% (0.12%) | 0.30% (0.45%) | 5.68% / 7.34% | 24.54% / 14.17%"
- **Replace with:** "| Vanguard Charitable | 0.21% (0.12%) | 0.30% (0.45%) | 5.68% / 7.34% | 24.54% / 14.17% (refined: named FS 0.62%, core 5.96% / 7.65%, broad 24.20% / 13.77%) [V wave 40A]"

- **Find:** "plus slightly higher fiscal-sponsor shares at Fidelity and NPT."
- **Replace with:** "plus slightly higher fiscal-sponsor shares at Fidelity and NPT. On the EIN-keyed fiscal-sponsor list the like-for-like sum is about 4.2% (3.9% without 50CAN, Global Impact, NEO Philanthropy and Myriad USA) ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 40A]"

- **Find:** "**On the briefed categories, it covers only about a third of the core dollar proxy** (3.6% of 10.0%)."
- **Replace with:** "**On the briefed categories, it covers only about a third of the core dollar proxy** (3.6% of 10.0%; about two-fifths, 4.2% of 10.6%, on the refined lists). [V wave 40A]"

- **Find:** "is right for foreign and fiscal-sponsor grants (0.47% of lines)."
- **Replace with:** "is right for foreign and fiscal-sponsor grants (0.47% of lines; 0.67% with the EIN-keyed fiscal-sponsor list). [V wave 40A]"

- **Find:** "| Core share (lines / dollars) | 7.41% / 10.96%"
- **Replace with:** "| Core share (lines / dollars) | 7.41% / 10.96% (7.76% / 11.61% with the EIN-keyed fiscal-sponsor list and time-correct rulings; 6.80% / 11.00% new organisations only; [g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 40A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "is 10.0% of their dollars and 11.0% across the top 50 (10.96% after the Greater Horizons correction). [V wave 33B] It measures recipients, not observed review (§11.30; [V wave 32A]). [gap19-11]"
- **Replace with:** "is 10.0% of their dollars and 11.0% across the top 50 (10.96% after the Greater Horizons correction). [V wave 33B] It measures recipients, not observed review (§11.30; [V wave 32A]). [gap19-11] With fiscal sponsors keyed by EIN (the 19 named hosts plus the Fiscal Sponsor Directory) and rulings dated with archived IRS BMF files, the like-for-like measure is about 4.2% (about 3.9% without four hosts with large programmes of their own), and the top-50 core proxy is 7.76% of lines and 11.61% of dollars, or 6.80% / 11.00% counting only true new organisations as recent. Fiscal sponsors' dollar share is 4.4× their count share (4.0× without those hosts), not 10.7×, and rulings recent at grant time are 4.14% of lines and 5.34% of dollars (§11.50; repo [`g0503-0501-exception-proxy-refinements.md`](mission-2026-11-14/g0503-0501-exception-proxy-refinements.md)) [V wave 40A]"

- **Find:** "about 66% (59.2% on corrected data) if Givinga, whose account unit is undefined, is excluded (§11.1)"
- **Replace with:** "about 66% (59.2% on corrected data) if Givinga, whose 1,421,011 accounts are described only as those of “INDIVIDUAL ACCOUNT HOLDERS” and average $1.37 of year-end value, is excluded (§11.1). The five processors examined in b40n13-03-g1913-03 (AOGF, PPGF, Givinga, Blackbaud Giving Fund, For Good) hold 76.2% of corrected FY2024 accounts, none counts the same unit as sponsors, and their accounts belong in a separate series [V wave 40A]"

- **Find:** "- Givinga's account unit is undefined [V wave 5]."
- **Replace with:** "- Givinga’s filings define its account unit only as “INDIVIDUAL ACCOUNT HOLDERS” (CY2024 990 Part III), and its site offers employers “Optional individual employee accounts”; which population the 1,421,011 count covers is still unconfirmed [V wave 40A]"

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.51 Propagation, DAF grant schema and processor accounts (validated, wave 40A)\n\n**Propagation, DAF grant schema and processor accounts** (validated, wave 40A). Independent checks confirm the FY2024 outside-DAFRC totals with Groundswell Charitable Foundation’s amended TY2024 Schedule D: 24,800 accounts (11,992 + 12,808), $353,892,765 of DAF assets (0.108% of DAFRC), $161,008,431 of contributions and unchanged grants of $110,820,269, because Groundswell leaves Part I line 3 blank. Its 12,808 accounts average $787. The refined exception-proxy figures (core 7.76% / 11.61%; about 4.2% like-for-like, 3.9% without four large-programme hosts) reproduce from the refined CSV. One table placement was fixed, and the proposed pointer in §11.30 was dropped because that section is a per-wave record. In the schema study, IRS Schedule I requires only the recipient EIN in full, plus an annual amount and a free-text purpose for domestic recipients above $5,000. Endaoment’s OpenAPI 4.88.0 states amounts in USDC micro-units. The five processors examined hold 2,522,661 of 3,309,483 corrected FY2024 accounts (76.2%). All 22 processors hold 2,538,698 (76.7%), so the processor-free series is 770,785, not 786,822. Their units differ from sponsor accounts, so they belong in a separate series (repo [`validation-wave40a-report.md`](mission-2026-11-14/validation-wave40a-report.md)) [V wave 40A]\n\n---\n\n## Source register"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "FY2023–24 filings reproduce the measure at about 3.6%, and a broader review-need proxy is 10.0% of the four nationals' dollars and 11.0% across the top 50."
- **Replace with:** "FY2023–24 filings reproduce the measure at about 3.6%, and a broader review-need proxy is 10.0% of the four nationals' dollars and 11.0% across the top 50. With EIN-keyed fiscal sponsors and time-correct rulings these become about 4.2% (3.9% without four large-programme hosts), 10.6% and 11.61% (7.76% of lines; 6.80% / 11.00% counting only true new organisations) ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 40A]"

- **Find:** "3.6% like-for-like in FY2023–24 [V wave 33B])."
- **Replace with:** "3.6% like-for-like in FY2023–24 [V wave 33B]). On the EIN-keyed fiscal-sponsor list the like-for-like share is about 4.2% (3.9% without four large-programme hosts) and the review-need proxy 10.6% of the four nationals' dollars and 11.61% across the top 50; neither is a measured exception rate [V wave 40A]"

- **Find:** "**Uncertainty:** Givinga's account unit is undefined **[V wave 5]**"
- **Replace with:** "**Uncertainty:** Givinga's account unit is undefined **[V wave 5]** (its filings describe only “INDIVIDUAL ACCOUNT HOLDERS”, its site offers employers “Optional individual employee accounts”, and at $1.37 of year-end value per account in CY2024 the count measures enrolment, not active advising) [V wave 40A]"

### `research/mission-2026-11-14/full-universe-990-harvest-and-corrected-totals.md`

- **Find:** "| 2024* | 1,235 | 413 | 106 | 42 | 140 | 529 | 4 | $0.34bn | $0.34bn | 11,992 | 0.10%"
- **Replace with:** "| 2024* | 1,235 | 413 | 106 | 42 | 140 | 529 | 4 | $0.34bn (with Groundswell $0.35bn) | $0.34bn ($0.35bn) | 11,992 (with Groundswell 24,800) | 0.10% (0.11%) [V wave 40A]"

- **Find:** "which appear only on an amended return e-filed 2026-01-28 that answers line 6 “No” [F] [V wave 39B]"
- **Replace with:** "which appear only on an amended return e-filed 2026-01-28 that answers line 6 “No” [F] [V wave 39B]. Adding that return gives FY2024 totals of 24,800 accounts, $353.9m of DAF assets (0.108% of DAFRC), $161.0m of DAF contributions and unchanged DAF grants of $110.8m (Groundswell leaves Schedule D Part I line 3 blank, although its Part I line 13 grants are $4,463,378); its 12,808 accounts average $787 ([`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`](../../data/mission-2026-11-14/non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv)) [V wave 40A]"

- **Find:** "FY2024 non-DAFRC accounts roughly double, from 11,992 to about 24,800 [C] [V wave 39B]"
- **Replace with:** "FY2024 non-DAFRC accounts roughly double, from 11,992 to 24,800 (11,992 + Groundswell’s 12,808; `non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`) [C] [V wave 39B] [V wave 40A]"

- **Find:** "`dafrc_daf_assets_fy`; `non_dafrc_assets_pct_of_dafrc`; `filers_ge_1bn`; `fy_complete_in_soi`."
- **Replace with:** "`dafrc_daf_assets_fy`; `non_dafrc_assets_pct_of_dafrc`; `filers_ge_1bn`; `fy_complete_in_soi`.\n\n### `non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv` (one row per FY 2020–2025)\nThe same 6 rows and first 20 columns, plus 11 columns (31 in all). In FY2024 the value columns (`non_dafrc_daf_assets`, `_excl_ge_1bn`, accounts, contributions, `non_dafrc_assets_pct_of_dafrc`) add Groundswell Charitable Foundation’s amended TY2024 Schedule D Part I (grants unchanged: its line 3 is blank); the status counts stay SOI line-6 “Yes” counts. `soi_y_only_*` keep the original values; `line6_no_additions_*` give the added return ([prop-0503-1915-propagation.md](prop-0503-1915-propagation.md)) [V wave 40A]"

### `research/mission-2026-11-14/g1915b-04-line6-vs-schedule-d.md`

- **Find:** "so the outside-DAFRC account total for FY2024 roughly doubles (to about 24,800)."
- **Replace with:** "so the outside-DAFRC account total for FY2024 roughly doubles, to 24,800 (11,992 + 12,808), and its DAF assets rise from $343.8m to $353.9m (`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`). [V wave 40A]"

### `research/mission-2026-11-14/direction-long-tail-sponsors.md`

- **Find:** "FY2024 non-DAFRC accounts roughly double (11,992 to about 24,800) [C] [V wave 39B]"
- **Replace with:** "FY2024 non-DAFRC accounts roughly double (11,992 to 24,800 with Groundswell’s 12,808) [C] [V wave 39B] [V wave 40A]"

- **Find:** "(`non-dafrc-daf-filers-990.csv`; FY2023: 424 filers, $0.15bn)."
- **Replace with:** "(`non-dafrc-daf-filers-990.csv`; FY2023: 424 filers, $0.15bn). Adding Groundswell Charitable Foundation, which reports DAFs only on an amended return answering line 6 “No”, gives 414 filers, $0.35bn, median $107k and 24,800 accounts (`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`) [V wave 40A]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "- Non-DAFRC FY2024 accounts are about 24,800."
- **Replace with:** "- Non-DAFRC FY2024 accounts are 24,800: 11,992 at line-6 “Yes” filers plus Groundswell’s 12,808 (average $787 per account), with $353.9m of DAF assets (`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`) [V wave 40A]"

### `research/mission-2026-11-14/gap19-complaints-with-denominators.md`

- **Find:** "AOGF's 720,545 (IRS 990) almost certainly counts workplace donor accounts."
- **Replace with:** "AOGF’s 720,545 is its filed Schedule D Part I line 1 column (a) for the year ended 31 March 2024, where its own note says “AOGF HAS A MICRODONATION DAF MODEL VERSUS A CONVENTIONAL DAF ENDOWMENT MODEL.” Its FYE 2026 return reports 695 DAFs in column (a) and 751,746 other accounts in column (b), and says individual donors recommend grants “WITHOUT ONGOING ADVISORY PRIVILEGES”, so the 720,545 are mostly individual workplace donor accounts [I]. Blackbaud Giving Fund filed no line 1 count for CY2023–CY2025 (DAFRC’s 460 is imputed; the last filed count is 359 for CY2022), and its funds are employer and campaign programs [I]. For Good’s 1 is filed and counts one pooled fund that every donor gives through, so its per-account rate is undefined rather than implausible (b40n13-03-g1913-03 §4) [V wave 40A]"

- **Find:** "- **DAFRC FY2024 timing** means fiscal years ending in 2024 or early 2025 (AOGF's year ends 31 March)."
- **Replace with:** "- **DAFRC FY2024 timing** means fiscal years ending in calendar 2024 (762 of the 767 panel rows sourced to an IRS 990); 677 of the 709 imputed rows carry a 2023 year end. AOGF’s year ends 31 March, so its FY2024 row is the year ended 31 March 2024 (return 202530159349302758), not a year ending in early 2025 [V wave 40A]"

- **Find:** "| PPGF | 380,644 | 0.10 | 4.64"
- **Replace with:** "| PPGF | 380,644 (consumer donor accounts; not comparable with sponsor accounts) | 0.10 (not comparable) | 4.64 [V wave 40A]"

- **Find:** "- **Denominator quality.** Two of the five processor account counts are imputed or implausible."
- **Replace with:** "- **Denominator quality.** Of the five processors here (AOGF, PPGF, Blackbaud Giving Fund, Dechomai, For Good), Blackbaud has no filed line 1 count (DAFRC-imputed 460) and For Good’s filed 1 is one pooled fund. AOGF and PPGF count individual donor accounts and Blackbaud employer and campaign programs [I]; Dechomai’s unit (314 accounts after correction) has not been classified. Per-account rates for processors should be read as not comparable (b40n13-03-g1913-03 §4.3) [V wave 40A]"

### `research/mission-2026-11-14/queue-batch38-data-followups.md`

- **Find:** "Givinga's 1,421,011 accounts average $8.73 (EOY $12.4m)."
- **Replace with:** "Givinga’s 1,421,011 accounts average $8.74 of CY2024 DAF grants ($12.4m) and $1.37 of year-end value ($1.95m); the $12.4m is grants, not EOY value [V wave 40A]"

### `research/mission-2026-11-14/regulation-market-structure-portability.md`

- **Find:** "| Givinga Foundation (47-4172718) | 1,421,011 | $1.95M | paper submission |"
- **Replace with:** "| Givinga Foundation (47-4172718) | 1,421,011 | $1.95M | DAFRC: paper submission. The same count is in the e-filed amended CY2024 return of 2025-11-13 (202503179349301975); the original of 2025-08-25 left Part I blank [V wave 40A]"

- **Find:** "| 694,979 | $151.2M | **Imputed** (last FYE Dec 2023) |"
- **Replace with:** "| 694,979 | $151.2M | **Imputed** (last FYE Dec 2023). The filed CY2024 return (202533079349301308) reports 380,644 accounts and $97.0M, which replace the imputation under R1 [V wave 40A]"

- **Find:** "- **Sensitivity 2: also drop PayPal's imputed count.**"
- **Replace with:** "- **Sensitivity 2: also drop PayPal’s count** (imputed 694,979 as published; corrected work should use the filed 380,644) [V wave 40A]"

- **Find:** "We did not verify that American Online Giving Foundation is the Benevity-affiliated entity; it is commonly reported as such."
- **Replace with:** "Benevity’s Software and Service Information lists “American Online Giving Foundation, Inc.” as its United States foundation, and AOGF’s FYE 2024 return calls its model a “MICRODONATION DAF MODEL” (b40n13-03-g1913-03 §4.2) [V wave 40A]"

### `research/mission-2026-11-14/queue-assurance-everyorg-givinga-monitoring.md`

- **Find:** "- Any FY2022-2024 national DAF *account* total or processor-share figure that includes Givinga moves by about 1.0-1.5m accounts on an undefined unit."
- **Replace with:** "- Any FY2022-2024 national DAF *account* total or processor-share figure that includes Givinga moves by about 1.0-1.5m accounts of a unit Givinga describes only as individual (and optional employee) giving accounts, averaging $1.37 of year-end value in CY2024 [V wave 40A]"

### `research/mission-2026-11-14/prop-0503-1915-propagation.md`

- **Find:** "grants unchanged at $110,820,269 (Groundswell files no grants amount)"
- **Replace with:** "grants unchanged at $110,820,269 (Groundswell leaves Schedule D Part I line 3 blank; its Part I line 13 grants are $4,463,378) [V wave 40A]"

- **Find:** "**1 short pointer item** to §11.50, no figures replaced"
- **Replace with:** "**1 short pointer item** to §11.50, no figures replaced. Wave 40A rejects this item: §11.30 is a per-wave validated summary (each §11.30–§11.50 paragraph carries only its own wave tag), and wave 39C left it unchanged on purpose [V wave 40A]"

- **Find:** "Groundswell's accounts average $787 ($10,084,314 / 12,808) [C]."
- **Replace with:** "Groundswell's accounts average $787 ($10,084,314 / 12,808) [C]. These low-balance accounts raise the same comparability question as processor accounts (b40n13-03-g1913-03 §4.3), so account totals that include them should say so [V wave 40A]"

### `research/mission-2026-11-14/b40n13-03-g1913-03-schema-and-processor-accounts.md`

- **Find:** "Without them the comparable series is **786,822** accounts"
- **Replace with:** "Without them the comparable series is **786,822** accounts (it still includes 16,037 corrected accounts at the other 17 DAFRC processors; 770,785 without any processor) [V wave 40A]"

- **Find:** "**Blank** for CY2023, CY2024 and CY2025; last filed **359** (CY2022)"
- **Replace with:** "**Blank** for CY2023 (return 202402119349300860, read by wave 40A), CY2024 and CY2025; last filed **359** (CY2022) [V wave 40A]"

- **Find:** "- **For Good:** filed 1 in every year 2019–2024 (DAFRC panel) [R]."
- **Replace with:** "- **For Good:** filed 1 in every year 2019–2023 (DAFRC panel) and in its CY2024 return (202513039349301631); DAFRC’s FY2024 row is imputed from the 2023 return [V wave 40A]"

- **Find:** "The other 17 DAFRC processors (15,912 FY2024 accounts as published) are not yet classified (P-G1913-03-02)."
- **Replace with:** "The other 17 DAFRC processors (15,912 FY2024 accounts as published; 16,037 after the R1 corrections, mainly Dechomai Asset Trust 181 → 314) are not yet classified (P-G1913-03-02). Removing all 22 processors (2,538,698 accounts, 76.7%) leaves 770,785 [V wave 40A]"

- **Find:** "The 786,822 comparable figure removes only the five."
- **Replace with:** "The 786,822 comparable figure removes only the five; the other 17 hold 16,037 corrected FY2024 accounts. The sponsor side also holds mass low-balance accounts: the repo’s A3 variant (AOGF restated, then sponsor-years with at least 5,000 accounts and average year-end value under $500 removed) gives 750,473, so a unit-based screen should accompany the DAFRC type label [V wave 40A]"

