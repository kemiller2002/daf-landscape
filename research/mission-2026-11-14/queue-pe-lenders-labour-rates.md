# Queue P-PE-02 and P-COST-02: lenders to DAF-ecosystem software, and sponsor labour rates

**Date:** 2026-11-14 · **Queue items:** P-PE-02 (lenders and debt terms), P-COST-02 (loaded labour rates vs Form 990) · **Recency:** 2021+ filings only
**Data:** [`bdc-loans-daf-ecosystem.csv`](../../data/mission-2026-11-14/bdc-loans-daf-ecosystem.csv) (650 rows) · [`sponsor-salary-per-employee.csv`](../../data/mission-2026-11-14/sponsor-salary-per-employee.csv) (4,030 rows) · [`queue-proposals-lenders-labour.csv`](../../data/mission-2026-11-14/queue-proposals-lenders-labour.csv) (P-LND-01..05)
**Scripts:** [`scripts/mission_bdc_loans.py`](../../scripts/mission_bdc_loans.py) · [`scripts/mission_labour_rate_check.py`](../../scripts/mission_labour_rate_check.py)
**Builds on:** [private-equity-daf-ecosystem-map.md](private-equity-daf-ecosystem-map.md) (and its wave-7 corrections) · [sponsor-cost-structure-and-sensitivities.md](sponsor-cost-structure-and-sensitivities.md) (and its wave-5 corrections) · [ai-economics-v2-observed-costs.md](ai-economics-v2-observed-costs.md)

Evidence tags: **[F]** read from a filing · **[S]** computed by a script from filed data · **[I]** inference.

---

## 1. Key findings

### P-PE-02: lenders

1. **GTCR-era Foundation Source is financed by Audax, which is still a lender.** [F] Audax Private Credit Fund lists "Foundation Source" with:
   - a 1st-lien term loan at S+5.00%, maturing 9/6/2030;
   - a delayed-draw term loan at the same spread and maturity;
   - a revolver maturing 9/6/2029;
   - Class A and Class B LP interests.

   All debt is marked at par (100%). The term loan is $13.37m, the DDTL $4.21m and the revolver $0.34m in the first schedule of the Q3-2026 10-Q ([10-Q, filed 2026-11-12](https://www.sec.gov/Archives/edgar/data/2033362/000119312526458521/ck0002033362-20260930.htm); [10-Q, filed 2025-08-14](https://www.sec.gov/Archives/edgar/data/2033362/000095017025108733/ck0002033362-20250630.htm)).
   - The LP interests cost $2.00m and carry a fair value of $2.76–2.88m across the two schedules in that 10-Q, about 1.4× cost.
   - [I] The 9/6/2030 maturity is seven years from GTCR's September 2023 buyout, so this is probably the GTCR acquisition facility. Audax also arranged Incline's 2020 unitranche.
   - **This contradicts wave-7 correction 5** ("probably refinanced at GTCR's 2023 buyout, not a current lender"). Audax remains a lender; the 2020 facility itself was most likely replaced.
   - The fund's "acquisition date" of 10/10/2024 is when this fund bought into the loan, not when the loan was made.
   - Only this one Audax vehicle shows the loan in EDGAR. The rest of the syndicate is not visible.
2. **Bonterra (Apax) has the most stressed credit history in the set.** [F] The CyberGrants Holdings unitranche (CyberGrants was renamed Bonterra LLC) was made around 9/8/2021, matures **9/8/2027** and was priced at L+6.50% with a 0.75% floor.
   - **Lenders:**
     - Golub (one-stop) across Golub Capital BDC, GBDC 3 and Golub Capital Direct Lending Corp;
     - Monroe Capital Corp and Monroe Capital Income Plus;
     - BlackRock TCP Capital, BlackRock Capital Investment and BlackRock Direct Lending;
     - AB Private Credit Investors and AB Private Lending Fund.
     - In 2021, EveryAction Intermediate Holdings (Golub, L+7.00%) and EveryAction, Inc. (Monroe, L+7.00%) had separate loans maturing 4/2027 ([Golub 10-Q 2021-08-09](https://www.sec.gov/Archives/edgar/data/1476765/000147676521000153/gbdcfy202110-qq3.htm); [Monroe 10-Q 2021-08-03](https://www.sec.gov/Archives/edgar/data/1512931/000110465921099472/tm2118615d1_10q.htm)).
   - **Marks fell below par in 2022–23.** At December 2022 the term loan was at 96.9% and the revolver at 91.75% ([BlackRock Capital Investment 10-K, filed 2023-03-01](https://www.sec.gov/Archives/edgar/data/1326003/000095017023005502/bkcc-20221231.htm); [BlackRock TCP 10-K, filed 2023-02-28](https://www.sec.gov/Archives/edgar/data/1370755/000095017023004871/tcpc-20221231.htm)).
   - **An amendment followed.** By December 2023 the spread had moved to SOFR+7.25%, and an "Amendment 4" incremental term loan was added at **8.00% PIK** (paid in kind). The revolver was still marked at 91.5% ([BlackRock Capital Investment 10-K, filed 2024-03-05](https://www.sec.gov/Archives/edgar/data/1326003/000095017024025850/bkcc-20231231.htm)).
   - **Marks recovered by late 2025.** At September–December 2025 the main term loan was at SOFR+7.00% and marked 98.5–99.1%. An incremental tranche at 7.75% PIK matures 9/27/2027 ([Golub Capital BDC 10-K, filed 2025-11-18](https://www.sec.gov/Archives/edgar/data/1476765/000147676525000096/gbdc-20250930.htm); [BlackRock TCP 10-K, filed 2026-02-27](https://www.sec.gov/Archives/edgar/data/1370755/000119312526079299/tcpc-20251231.htm); [Monroe Capital 10-K, filed 2026-03-05](https://www.sec.gov/Archives/edgar/data/1512931/000151293126000011/mrcc-20251231.htm)). Golub Capital BDC alone holds about $92.9m par of the main term-loan line (in thousands, period 2025-09-30).
   - [I] The facility matures in about 10 months, so a refinancing or extension is imminent.
3. **A same-name "Bonterra LLC" facility maturing 3/5/2032 is not confirmed as Apax's Bonterra.** [F]
   - **Lenders and terms:** FS KKR Capital, KKR FS Income Trust, KKR FS Income Trust Select, KKR Enhanced US Direct Lending, Crescent Private Credit Income, AB Private Credit Investors, AB Private Lending Fund and CCS IX Portfolio Holdings hold it at S+4.75–5.00% with a 0.75% floor, marked 96–100%.
   - **Size:** FS KKR's largest line is $133.4m par, in millions ([FS KKR 10-Q, filed 2026-11-05](https://www.sec.gov/Archives/edgar/data/1422183/000162828026070499/fsk-20260930.htm); [Crescent 10-Q, filed 2026-11-13](https://www.sec.gov/Archives/edgar/data/1954360/000119312526460859/na-20260930.htm); [AB Private Lending Fund 10-Q, filed 2026-11-13](https://www.sec.gov/Archives/edgar/data/1982701/000119312526460564/ck0001982701-20260930.htm)).
   - **Evidence the borrower may differ:** FS KKR classes it "Software & Services". AB classes it "**Diversified Consumer Services**", although AB classed the 2027 Apax loan "Software & Tech Services" in 2024. The 2027 Apax facility was also still held by Golub, BlackRock and Monroe at the same dates.
   - The identity is left unconfirmed (`identity_note`) and queued as P-LND-01.
4. **Orion's debt is broadly syndicated and priced tight.** [F]
   - **First lien:** S+2.75% and S+3.25% tranches maturing 09/2030, marked 99.3–100.7%. Holders are Blue Owl (OBDC, OBDC II, OCIC, OTF, OTIC), Golub (GCRED, GPIF), New Mountain and North Haven/Morgan Stanley.
   - **Second lien:** SOFR+5.75%, maturing 12/31/2030, held by Stone Point Credit.
   - **Further OHA facilities:** S+4.50% maturing 11/26/2032 and S+5.50% maturing 10/10/2033. Their low marks (about 52%) are on partly drawn delayed-draw commitments, not credit marks.
   - Sources: [Blue Owl Capital Corp 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/1655888/000165588826000069/blueowlcreditslfllc-093020.htm); [Stone Point Credit 10-Q, filed 2026-11-12](https://www.sec.gov/Archives/edgar/data/1825384/000182538426000003/none-20260930.htm); [T. Rowe Price OHA 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/1901164/000190116426000022/oha-20260630.htm).
   - In 2023 an older OHA position at L+8.50% (9/24/2028) was marked 93.0% ([OHA 10-Q 2023-08-09](https://www.sec.gov/Archives/edgar/data/1901164/000162828023028587/oha-20230630.htm)).
5. **Bloomerang (JMI/Warburg) is a Golub and Monroe one-stop borrower.** [F] The loan was made in December 2023 at SF+6.00%, maturing 12/27/2029, with roughly 98–99% marks at close. It sits in seven Golub/Monroe vehicles ([Golub Capital BDC 10-Q, filed 2024-02-05](https://www.sec.gov/Archives/edgar/data/1476765/000147676524000016/gbdc-20231231.htm); [Monroe Capital Income Plus 10-K, filed 2024-03-12](https://www.sec.gov/Archives/edgar/data/1742313/000174231324000006/mcip-20231231.htm)).
   - By late 2025 the 2029 facility had SF+6.50% tranches flagged with PIK.
   - 2026 schedules add an SF+5.50% tranche at "6.23% cash / 3.00% PIK", marked 99.0% ([Golub Capital BDC 10-Q, filed 2026-08-03](https://www.sec.gov/Archives/edgar/data/1476765/000147676526000048/gbdc-20260630.htm); [Monroe Capital Income Plus 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1742313/000174231326000066/mcip-20260930.htm)).
   - [I] A PIK component on a growth-equity-backed borrower is a mild liquidity signal. The marks do not show stress.
   - This adds Golub and Monroe as current lenders alongside the CIBC facility already in the map.
6. **Community Brands → Momentive:** [F]
   - **Old facility:** a 2/24/2028 first lien at S+5.50–5.75%. Holders were Blackstone (BCRED, BXSL), Blue Owl/Owl Rock, Golub, FS KKR, KKR FS Income Trusts, AB, Audax Credit BDC and T. Rowe OHA. Ares holds Class A units in Community Brands ParentCo.
   - **Momentive-era facility:** a 07/2031 unitranche at S+5.25–5.3%, held by FS KKR, the KKR FS Income Trusts and T. Rowe OHA.
   - **Credit signal:** FS KKR and KKR FS Income Trust mark the largest 2031 tranches at **96.1%** at 2026-09-30 ([FS KKR 10-Q, filed 2026-11-05](https://www.sec.gov/Archives/edgar/data/1422183/000162828026070499/fsk-20260930.htm)). This is the only current below-97 credit mark found outside Bonterra.
7. **Not found in any BDC 10-K/10-Q (2021-01-01 to 2026-11-14).** [F] EDGAR full-text search returned zero BDC hits for:
   - Ren (as "Renaissance Philanthropic" or "RenPSG");
   - Benevity (10 hits, all from non-BDC filers such as TPG, Ziff Davis and F5);
   - Foundant, Fundraise Up, OneCause, Neon One, Virtuous, GiveSmart, SofterWare and Submittable.

   Each target has a `no_bdc_hit` row with its query URL. [I] These companies either carry no institutional term debt, borrow from banks or non-BDC funds, or appear under an unsearched legal name. Ren and Benevity remain open (P-LND-02).
8. **Envestnet (Bain, via BCPE Pequod Buyer, dba Envestnet), for context.** [F]
   - **Holders:** Ares Capital and Ares Strategic Income at SOFR+3.50% (09/2031, 2024). Blue Owl vehicles and BlackRock Private Credit were repriced to S+2.75–3.00% (11/2031) by 2026.
   - **Marks:** 98.6–100.3%.
   - This confirms the map's Ares and Blue Owl lenders; Benefit Street was not found in BDC filings.

### P-COST-02: labour rates

Scope: 898 sponsors with at least 5 W-2 employees and line 7 > 0, using each sponsor's latest return (FY2022–2025). [S]

9. **Across all sponsors, the model's band is about right.** [S] Median loaded labour cost per employee (Part IX lines 5–10 ÷ Part I line 5 ÷ 2,080 h) is **$38.87/h**, with an interquartile range of $26.84–$52.91/h. Both ends sit inside the model's $30.76–$55.45/h band. The median line-7 wage per head is $21.78/h, close to the BLS customer-service ($21.53) and bookkeeping ($24.36) medians.
10. **Where DAFs are large, the band is too low.** [S] Median loaded rate by DAF-asset band:

    | DAF-asset band | Median loaded rate |
    |---|---|
    | $50–250m | $50.53/h |
    | $250m–1bn | $57.35/h |
    | $1–10bn | $73.28/h |
    | >$10bn | $60.05/h |

    - National-Standard sponsors (n = 20) have a median of $49.51/h and an employee-weighted rate of $69.18/h.
    - Named large sponsors, latest return [S]:
      - DAFgiving360: $84.60–86.35/h (FY2024–25);
      - National Philanthropic Trust: $60.05–60.47/h;
      - Vanguard Charitable: $59.86/h;
      - CAF America: $55.65–56.46/h;
      - American Endowment Foundation: $40.51/h.
    - [I] For the archetypes that decide network-scale AI break-even, the $55.45/h compliance rate is the floor, not the ceiling. On the observed cost of comparable sponsor staff, the v2 pools at large nationals are understated by roughly 8–55% (P-LND-03). Fidelity reports 0 employees and buys its labour through line 11a, so it cannot be tested this way.
11. **The model's gross-up for benefits does not match 990 data.** [S] On the 990, lines 5–10 ÷ lines 5–7 has a median of 1.19 (1.26 at >$10bn), against the model's ECEC factor of 1.4287. [I] The two are not like-for-like:
    - ECEC "wages" exclude paid leave and supplemental pay, while 990 wages include them.
    - The right test is therefore total loaded cost per head (finding 10), not the multiplier.
12. **Biases (direction known).**
    - Part I line 5 counts every W-2 employee in the year, including part-time and seasonal staff. That pushes per-head rates *down*: 246 of 3,953 returns with staff show under $20k per head.
    - Paid officers sit in the denominator of the line-7 measure, also pushing it *down*.
    - Officer pay in the all-wage measure pushes that measure *up*.
    - Converting per head to per FTE is queued as P-LND-04.

## 2. Method

**P-PE-02** (`mission_bdc_loans.py`, stdlib):
1. Query EDGAR full-text search (`efts.sec.gov/LATEST/search-index`) for 21 borrower phrases in 10-K and 10-Q filings dated 2021-01-01 to 2026-11-14 (1,284 hits). Keep only filers with an `814-` file number (BDCs).
2. For each phrase–BDC pair, keep the earliest and latest filing (189 filings, 168 unique documents).
3. Parse every `<tr>` whose first cell matches the borrower regex, plus the instrument-only continuation rows under it. Extract the reference rate, spread, floor, PIK flag, maturity, and par / cost / fair value (the numbers after the maturity date).
4. Drop small "% of net assets" decimals and trailing footnote markers.

**Limitations:**
- The parser is heuristic. 11 rows are flagged `parse_check = check_raw`, and `row_cells_raw` governs any disputed value.
- 10-K and 10-Q documents also contain the prior-period schedule, so one filing can show two periods. Do not sum par across rows without de-duplicating.
- `units_hint` is document-level (thousands, millions, or dollars/unstated).
- Rows for revolvers and DDTLs whose par is a commitment are typed `revolver_or_ddtl_commitment_basis`, and no below-par signal is computed for them.
- "Momentive" hits for Momentive Performance Materials are excluded by the borrower regex (they appear as `text_hit_no_table_row`).
- No paid databases, trustee reports or rating releases were used.

**P-COST-02** (`mission_labour_rate_check.py`, stdlib):
1. Reuse the cached Part IX line extracts behind `sponsor-cost-structure.csv` (5,272 returns; no extract was missing) and their category and DAF-asset size bands.
2. "Staffed" means employees ≥ 5, line 7 > 0, and all-wage pay per head ≤ $300k (24 outliers excluded).
3. Hourly rate = annual ÷ 2,080.
4. Summaries are produced for two scopes: the latest return per EIN, and all FY2022–2025 returns.

## 3. Data dictionary

### `bdc-loans-daf-ecosystem.csv` (one row per schedule-of-investments line, or one `no_bdc_hit` row per target)

| Column | Meaning |
|---|---|
| target_company | Repo company the search was for (Bonterra lineage rows are split by search phrase) |
| identity_note | Rule-based confidence that the borrower as listed is the target (confirmed / linked / probable / unconfirmed) |
| edgar_phrase | Exact phrase searched |
| borrower_name_as_listed | First cell of the row, verbatim (footnote markers included) |
| lender_bdc, lender_cik, file_num | BDC entity name, CIK and 814- file number |
| form, filing_date, period_ending | 10-K or 10-Q; filing date; period of the filing (the row may belong to the prior-period comparative schedule) |
| which_filing | earliest / latest filing kept for the phrase–BDC pair |
| row_type | debt; equity; revolver_or_ddtl_commitment_basis (par is a commitment); possible_unfunded_commitment; unfunded_or_zero_position; name_or_subtotal_row; text_hit_no_table_row; no_bdc_hit |
| instrument | Instrument text (first lien, one stop, revolver, DDTL, LP interests, …) |
| ref_rate, spread_pct, floor_pct, pik_flag | Reference rate (S/SF/SOFR/L), spread in %, floor in % where parsed, "PIK" if the row mentions PIK |
| dates_in_row, maturity | All date cells; last date treated as maturity (blank for equity) |
| par_or_principal, amortized_cost, fair_value | As listed, in `units_hint` units |
| units_hint | thousands / millions / dollars_or_unstated (document-level heuristic) |
| fv_pct_of_par, fv_pct_of_cost | Fair value ÷ par (debt rows only) and ÷ cost, in % |
| below_par_signal | yes_lt_97 / slight_97_99.5 / no (debt rows only) |
| parse_check | check_raw where the parsed values are implausible |
| table_row_index | Index of the `<tr>` in the document |
| row_cells_raw | Row cells joined with " \| " (≤600 chars), the audit trail |
| filing_url, efts_query_url | Filing document; EDGAR search that found it |

### `sponsor-salary-per-employee.csv`

| Column | Meaning |
|---|---|
| record_type | `model_rate` (BLS wage and model loaded rate per occupation); `summary`; `return` (one per sponsor-year with employees > 0) |
| scope | Summary scope (`latest_return_per_ein_staffed`, `all_fy2022_2025_staffed`), `return`, or the occupation label |
| ein, sponsor_name, category, size_band_daf_assets, fiscal_year | As in sponsor-cost-structure.csv |
| n_returns, employees | Count of returns; employees (Part I line 5, summed for summaries) |
| l05…l10 | Part IX lines 5–10, total column |
| wages_l5_7, loaded_l5_10 | Sums of lines 5–7 and 5–10 |
| wage_l7_per_emp, wage_all_per_emp, loaded_all_per_emp | Line 7, lines 5–7 and lines 5–10, each ÷ employees |
| *_hourly | The same ÷ 2,080 |
| load_factor | Lines 5–10 ÷ lines 5–7 |
| officer_share_of_wages | Line 5 ÷ lines 5–7 |
| *_p25/_p50/_p75 | Quartiles across returns in a summary group |
| *_pooled | Employee-weighted (sum ÷ sum) |
| share_loaded_below_30_76, share_loaded_above_55_45 | Share of returns below or above the model band |
| flags | employees_lt_5; no_line7; wage_lt_20k_parttime_heavy; wage_gt_300k_outlier |
| return_object_id, source_url | IRS e-file object id; ProPublica return page |

## 4. Source register

| ID | Source | Date |
|---|---|---|
| L01 | [Audax Private Credit Fund 10-Q (Q3 2026)](https://www.sec.gov/Archives/edgar/data/2033362/000119312526458521/ck0002033362-20260930.htm) | 2026-11-12 |
| L02 | [Audax Private Credit Fund 10-Q (Q2 2025)](https://www.sec.gov/Archives/edgar/data/2033362/000095017025108733/ck0002033362-20250630.htm) | 2025-08-14 |
| L03 | [BlackRock Capital Investment 10-K FY2022](https://www.sec.gov/Archives/edgar/data/1326003/000095017023005502/bkcc-20221231.htm) | 2023-03-01 |
| L04 | [BlackRock Capital Investment 10-K FY2023](https://www.sec.gov/Archives/edgar/data/1326003/000095017024025850/bkcc-20231231.htm) | 2024-03-05 |
| L05 | [BlackRock TCP Capital 10-K FY2022](https://www.sec.gov/Archives/edgar/data/1370755/000095017023004871/tcpc-20221231.htm) | 2023-02-28 |
| L06 | [BlackRock TCP Capital 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1370755/000119312526079299/tcpc-20251231.htm) | 2026-02-27 |
| L07 | [Golub Capital BDC 10-K FY Sep-2025](https://www.sec.gov/Archives/edgar/data/1476765/000147676525000096/gbdc-20250930.htm) | 2025-11-18 |
| L08 | [Golub Capital BDC 10-Q Q2 2021 (EveryAction)](https://www.sec.gov/Archives/edgar/data/1476765/000147676521000153/gbdcfy202110-qq3.htm) | 2021-08-09 |
| L09 | [Monroe Capital Corp 10-Q Q2 2021 (EveryAction)](https://www.sec.gov/Archives/edgar/data/1512931/000110465921099472/tm2118615d1_10q.htm) | 2021-08-03 |
| L10 | [Monroe Capital Corp 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1512931/000151293126000011/mrcc-20251231.htm) | 2026-03-05 |
| L11 | [FS KKR Capital 10-Q Q3 2026](https://www.sec.gov/Archives/edgar/data/1422183/000162828026070499/fsk-20260930.htm) | 2026-11-05 |
| L12 | [Crescent Private Credit Income 10-Q Q3 2026](https://www.sec.gov/Archives/edgar/data/1954360/000119312526460859/na-20260930.htm) | 2026-11-13 |
| L13 | [AB Private Lending Fund 10-Q Q3 2026](https://www.sec.gov/Archives/edgar/data/1982701/000119312526460564/ck0001982701-20260930.htm) | 2026-11-13 |
| L14 | [AB Private Lending Fund 10-Q Q2 2024](https://www.sec.gov/Archives/edgar/data/1982701/000119312524223732/d872687d10q.htm) | 2024-09-23 |
| L15 | [Blue Owl Capital Corp 10-Q Q3 2026](https://www.sec.gov/Archives/edgar/data/1655888/000165588826000069/blueowlcreditslfllc-093020.htm) | 2026-11-04 |
| L16 | [Stone Point Credit 10-Q Q3 2026](https://www.sec.gov/Archives/edgar/data/1825384/000182538426000003/none-20260930.htm) | 2026-11-12 |
| L17 | [T. Rowe Price OHA Select 10-Q Q2 2026](https://www.sec.gov/Archives/edgar/data/1901164/000190116426000022/oha-20260630.htm) | 2026-08-13 |
| L18 | [T. Rowe Price OHA Select 10-Q Q2 2023](https://www.sec.gov/Archives/edgar/data/1901164/000162828023028587/oha-20230630.htm) | 2023-08-09 |
| L19 | [Golub Capital BDC 10-Q Q1 FY2024 (Bloomerang)](https://www.sec.gov/Archives/edgar/data/1476765/000147676524000016/gbdc-20231231.htm) | 2024-02-05 |
| L20 | [Golub Capital BDC 10-Q Q3 FY2026 (Bloomerang)](https://www.sec.gov/Archives/edgar/data/1476765/000147676526000048/gbdc-20260630.htm) | 2026-08-03 |
| L21 | [Monroe Capital Income Plus 10-K FY2023](https://www.sec.gov/Archives/edgar/data/1742313/000174231324000006/mcip-20231231.htm) | 2024-03-12 |
| L22 | [Monroe Capital Income Plus 10-Q Q3 2026](https://www.sec.gov/Archives/edgar/data/1742313/000174231326000066/mcip-20260930.htm) | 2026-11-06 |
| L23 | [EDGAR full-text search API](https://efts.sec.gov/LATEST/search-index?q=%22Foundation%20Source%22&forms=10-K,10-Q&dateRange=custom&startdt=2021-01-01&enddt=2026-11-14) (per-phrase query URLs in the CSV) | read 2026-11-14 |
| C01 | Form 990 Part IX lines 5–10 and Part I line 5, IRS e-file XML via [`sponsor-cost-structure.csv`](../../data/mission-2026-11-14/sponsor-cost-structure.csv) (`xml_url` per row) | FY2022–2025 |
| C02 | [BLS OOH, compliance officers](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm); [bookkeeping clerks](https://www.bls.gov/ooh/office-and-administrative-support/bookkeeping-accounting-and-auditing-clerks.htm); [customer service representatives](https://www.bls.gov/ooh/office-and-administrative-support/customer-service-representatives.htm); [BLS ECEC](https://www.bls.gov/news.release/ecec.nr0.htm), as used by the model | May 2025 / June 2026 |

## 5. Corrections to existing files (proposed, not applied)

1. **[private-equity-daf-ecosystem-map.md](private-equity-daf-ecosystem-map.md), wave-7 correction 5.**
   - Replace with: "(the 2020 facility was replaced; Audax Private Credit Fund holds a GTCR-era first-lien term loan, DDTL and revolver at S+5.00%, maturing 9/6/2030 / 9/6/2029, at par, plus LP interests, per its Q3-2026 10-Q)."
2. **Same file, line 203 ("Not found … lenders to … GTCR-era Foundation Source, Bonterra").**
   - Replace with: Foundation Source: Audax (L01). Bonterra: the Golub-led one-stop with Monroe, BlackRock and AB (9/8/2027; PIK amendment 2023) (L03–L07, L10).
   - Add Bloomerang: Golub and Monroe (L19–L22).
3. **[pe-ownership-by-company.csv](../../data/mission-2026-11-14/pe-ownership-by-company.csv)**: add `lender` rows from §1 when the owning agent next writes that file.
