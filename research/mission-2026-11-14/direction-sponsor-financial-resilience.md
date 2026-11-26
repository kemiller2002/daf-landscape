# Direction: financial resilience of the 100 largest DAF sponsors, TY2021–2024

**Date:** 2026-11-15 · **Agent:** batch44 N27 · **Queue item:** P-NEW-RES-01 (owner direction)

**Outputs**
- [`data/mission-2026-11-14/sponsor-financial-resilience-2021-2024.csv`](../../data/mission-2026-11-14/sponsor-financial-resilience-2021-2024.csv): 430 rows, 206 columns. It holds 400 sponsor-year rows (100 sponsors × TY2021–2024), 24 `group_year` rows (5 groups plus an "all" row, × 4 years) and 6 `group_trend` rows. The data dictionary is in §10.
- [`data/mission-2026-11-14/queue-proposals-batch44-n27.csv`](../../data/mission-2026-11-14/queue-proposals-batch44-n27.csv): P-B44N27-01 to -03.
- **Script:** [`scripts/mission_sponsor_resilience.py`](../../scripts/mission_sponsor_resilience.py). It is new, stdlib only and functional in style. It reuses:
  - from `mission_990_contractors`: number, CSV and XML helpers;
  - from `mission_sponsor_cost_structure`: the Part IX line and column map;
  - from `mission_sponsor_marketing`: the universe, sponsor groups, IRS index reader, return picking and period months;
  - from `mission_sponsor_compensation`: the DAFRC panel with applied corrections.

**Conventions**
- **TY** is the year in which the tax period *begins* (IRS convention), read from the return header. **FY** is the year in which the period ends.
- **Recency:** every return is TY2021–2024.
- **Labels:** **[F]** filed value; **[C]** script computation; **[I]** inference or classification.
- **Governing corrections read first:**
  - [sponsor-cost-structure-and-sensitivities.md](sponsor-cost-structure-and-sensitivities.md), wave 5: "operating cost" excludes Part IX lines 1–4 and 11f. This file uses exactly that definition.
  - [direction-sponsor-marketing-spend.md](direction-sponsor-marketing-spend.md), wave 28: no item touches the fields used here. Servant Foundation's line 12 is campaign spending, so its operating cost is flagged `campaign_advertising_in_opcost`.
  - [direction-sponsor-executive-compensation.md](direction-sponsor-executive-compensation.md), wave 28: no item touches the fields used here. Its segment table is the basis for two group overrides (§1.1).
- **Access:**
  - robots.txt was read before fetching. The GivingTuesday S3 mirror returns 404 for robots.txt, so there are no restrictions. apps.irs.gov answered 302, and this run made no requests to it. The www.irs.gov robots file disallows only search, admin and user paths; nothing was fetched from www.irs.gov except the robots file itself.
  - 394 returns were streamed from the mirror. 6 came from TEOS zip members already cached locally by earlier batches.
  - No logins, forms or contact. **This is research, not legal, accounting or investment advice.**

---

## 0. Bottom line

1. **The 990 cannot show a national sponsor's own reserve directly. It can only bound it, and the bound is thin [C].** At nationals, DAF assets are 99–100% of total net assets, so "non-DAF net assets" (R1) is a small difference between two very large numbers.
   - **Affiliated-commercial nationals (15), TY2024:** median R1 covers **29.4 months** of operating cost (IQR 7.6–60.0). Against unrestricted net assets less DAFs (R2) the median is **17.2 months**.
   - **Independent nationals (11), TY2024:** median R1 covers **2.2 months** (IQR −10.0 to 21.2). Four of the 11 show R1 ≤ 0, meaning the Schedule D DAF value is larger than Part X total net assets:
     - NPT −$93m against $55.9bn of DAFs;
     - Greater Horizons −$38m;
     - American Gift Fund −$4m;
     - CAF America −$19m.
   - **Three affiliated nationals also show R1 ≤ 0:** Morgan Stanley GIFT (−$133m in every year, TY2021–2024), Renaissance (−$17m to −$81m) and Johnson Charitable Gift Fund (exactly $0).
   - **[F]** Fidelity Charitable's non-DAF net assets equal its Schedule D "other funds" column to the dollar in all four years ($381.0m in TY2024). After DAF and other donor funds, **no sponsor-owned equity is disclosed**. Bessemer, Tides and several community foundations look the same.
2. **Community foundations look reserve-rich only because the measure counts endowment [C].**
   - **TY2024, 55 community foundations:**
     - DAFs are a median **59%** of net assets;
     - median R1 = **417 months** (about 35 years) of operating cost;
     - median R2 = **242 months**.
   - Those figures include board-designated quasi-endowment, field-of-interest and designated funds, and the foundation's own endowment. Netting out net PP&E and the board-designated share of the Schedule D Part V endowment (R5) gives a median of **1.6 months**. 79 sponsor-years go negative under R5 because the Part V endowment overlaps fund types that Schedule D also counts (flag `board_endowment_gt_unrestricted_less_daf`).
   - **[I]** A community foundation's spendable operating reserve lies somewhere between R5 and R2. The 990 cannot place it more precisely.
   - **[C]** 9 of 55 community foundations have R2 ≤ 0, meaning DAFs exceed net assets without donor restrictions. They classify part of their DAFs, or of their endowment, as donor-restricted.
3. **The literal "unrestricted net assets" line overstates reserves by two to three orders of magnitude [C].** Part X line 27 holds the DAFs, because the sponsor legally owns them. Read as a reserve, it gives a median of **5,351 months** for affiliated nationals and **801 months** for community foundations (TY2024). R3 is kept in the file only to show why it must not be used.
4. **Fee income is almost invisible on the 990, because the DAF fee is an internal transfer [F/C].**
   - **[F]** Program-service revenue (Part VIII line 2g) is $0 at all 15 affiliated-commercial sponsors in every year.
   - **[C]** Program-service revenue is 0.03% of revenue at independent nationals and 0.8% at community foundations (TY2024, pooled).
   - **[C]** Description-matched fee lines ("administrative fees", "management fees" and similar, in Part VIII lines 2 and 11) cover the following share of operating cost (TY2024, pooled):

     | Group | Fee lines ÷ operating cost |
     |---|---|
     | Affiliated-commercial | **4.8%** (Renaissance $19.6m and Raymond James $28k are the only filers) |
     | Independent nationals | 2.7% |
     | Community foundations | 13.5% (median 4.5%) |
     | Faith / single-issue | 5.3% |
     | AOGF (processor) | 40% |

   - **[F]** The one place an internal fee is disclosed is Schedule D Part V, line 1e (administrative expenses charged to endowment funds). For community foundations it equals **24%** of operating cost (TY2024, pooled; for example NYCT $40.8m, Cleveland $18.5m, CCT $17.0m).
   - **[I]** No 990 line carries the equivalent DAF charge. Fee reliance cannot be inferred from the balance sheet: at the five sponsors with audited fee data the fee surplus is not identifiable in ΔR1 (item 6). It has to be read from audited statements (P-B44N27-02; [b4427-03-b43n23-proxy-and-parent-marketing.md](b4427-03-b43n23-proxy-and-parent-marketing.md)). [b4427-03] [V wave 40C]
5. **Revenue mix, TY2024 (pooled Part VIII) [C]:**

   | Group | Contributions | Investment income (lines 3–5) | Net gains (line 7d) |
   |---|---|---|---|
   | Affiliated-commercial | 88.6% | 6.4% | 5.0% |
   | Independent nationals | 86.7% | 7.3% | 5.9% |
   | Community foundations | 68.6% | 8.5% | 22.2% |
   | Faith / single-issue | 85.4% | 6.3% | 7.8% |

   - Investment income alone (lines 3–5) is a median **10.6×** operating cost at affiliated nationals and **1.6×** at community foundations. Most of it belongs to DAF accounts.
6. **Operating surplus: the 990 headline is uninformative, and the change in non-DAF net assets (ΔR1) is a balance-sheet movement, not an operating signal. At the five sponsors with audited fee data it follows Schedule D other-fund growth, endowment returns, campaign receipts and Schedule D reporting basis; the fee surplus is identifiable in it at none [C].** [V wave 38B] [b4427-03] [V wave 40C]
   - Part I line 19 (revenue less expenses) is positive in nearly every sponsor-year, because DAF inflows exceed DAF grants.
   - Stripping net DAF flows (S2), 9 of 96 sponsors ran a deficit in TY2024 (23 in TY2022).
   - Also stripping all investment income (S4), 78 of 96 ran a deficit in TY2024. This is mechanical: the fee that funds operations is not revenue on the 990.
   - Year-on-year change in non-DAF net assets (ΔR1), as a multiple of operating cost, median by group:

     | Group | TY2022 | TY2023 | TY2024 |
     |---|---|---|---|
     | Affiliated-commercial | +0.42 | +0.42 | +0.39 |
     | Independent nationals | +0.48 | +0.47 | **−0.35** |
     | Community foundations | **−3.6** | +4.2 | +3.1 |
     | Faith / single-issue | 0.0 | +0.56 | +0.82 |

   - Community-foundation ΔR1 follows the markets: 43 of 55 fell in TY2022.
   - In TY2024, 7 of 11 independent nationals had a falling R1.
7. **Trend, TY2021→TY2024, matched sponsors [C]:**
   - **Affiliated-commercial (15):**
     - pooled operating cost **+13.5%/yr**;
     - pooled R1 +9.8%/yr;
     - median R1 cover rose from 22.3 to 29.4 months, but median R2 cover fell from 19.6 to 17.2 months.
   - **Community foundations (55):** operating cost +6.7%/yr against R1 +4.9%/yr. Median R1 cover fell from 480 to 417 months, and median R2 cover from 293 to 242.
   - **Faith / single-issue (13):** operating cost +14.2%/yr against R1 +0.7%/yr. Median R1 cover fell from 176 to 125 months.
   - **Independent nationals (10 matched):** median R1 cover fell from 6.6 to 4.7 months. This group is small and noisy.
   - **[I]** Across the panel, costs are growing faster than sponsors' own balance sheets.
8. **Administrative (management & general) share [C].** Management & general is taken net of its line-11f cell. As a share of operating cost, the TY2024 median is:

   | Group | M&G ÷ operating cost | Operating cost, bps of DAF assets (median) |
   |---|---|---|
   | Affiliated-commercial | 40% | 22.5 |
   | Independent nationals | 37% | 60 |
   | Community foundations | 33% | 234 (whole organisation) |
   | Faith / single-issue | 60% | 175 |

   - Fidelity reports its entire Part IX in the program column (M&G = $0; flag `mgmt_column_zero`).
   - BofA Charitable Gift Fund reports $0.1m of operating cost on $4.7bn of DAFs (flag `opcost_lt_1bp_daf`), so its months-of-cover figures are meaningless.

## 1. Method

### 1.1 Universe and groups
- **Universe:** the 100 sponsors ranked 1–100 by FY2024 DAF assets (`fy2024_asset_rank` in `form990-returns-schedule-d-harvest-full.csv`). This is the same top 100 as the marketing direction. All 100 file Form 990 in every TY2021–2024.
- **Groups** follow `mission_sponsor_marketing.sponsor_group` [I], with two changes:
  - **The US Charitable Gift Trust (Eaton Vance / Morgan Stanley) and Renaissance** move from "independent" to `affiliated_commercial_national`, following the executive-compensation direction's segment table. Schedule O there states that the officers are employees of the affiliate, or that a for-profit administrator runs the programme.
  - **Universities and health systems** (DAFRC subtype "Universities and Healthcare": Stanford, UCLA Foundation, Université de Montréal, Notre Dame) are a separate `university_health` group. They are reported in the file but excluded from every statistic, because their whole-institution balance sheets swamp the ratios.
- **Group sizes:**

  | Group | Sponsors |
  |---|---|
  | Affiliated-commercial | 15 |
  | Independent nationals | 11 (including Servant Foundation and The Signatry, which DAFRC types "National") |
  | Community foundations | 55 |
  | Faith / single-issue | 13 |
  | Processors | 2 (Dechomai, AOGF) |
  | University / health | 4 |

### 1.2 Returns and extraction
- **Returns:** every `RETURN_TYPE = 990` row for the 100 EINs in IRS `index_2021`–`index_2026` (local copy), with tax periods ending 2021-12 to 2025-11.
- **One return per sponsor × TY:** the longest period wins, then the latest `ReturnTs`, so amendments supersede. 14 extra returns (fiscal-year changes and duplicates) were dropped; one 6-month return is kept and annualised.
- **Streaming parse:** the parser stops before Schedule E, so Schedule I tables are never read. It extracts:

  | Area | Fields |
  |---|---|
  | **Part I** | Total revenue, total expenses, line 19, net assets BOY/EOY |
  | **Part VIII** | 1h contributions; 2a–f rows with descriptions and 2g; 3 investment income; 4 bond proceeds; 5 royalties; 6d rent; 7d net gains; 8c; 9c; 10c; 11 rows with descriptions; 12 total |
  | **Part IX** | All lines, all four columns (`part_ix_from`) |
  | **Part X** | Lines 1–2 cash; 10c net PP&E; 16 total assets; 21 escrow / agency liability; 26 total liabilities; **27** net assets without donor restrictions; **28** with donor restrictions; 29–31; 32 total net assets (BOY and EOY) |
  | **Part XI** | Line 5 unrealised gains; line 9 other changes |
  | **Schedule D Part I** | Columns (a) DAFs and (b) "funds and other accounts": count, contributions, grants, **EOY value** |
  | **Schedule D Part V** | Current-year endowment EOY balance; line 1e administrative expenses; board-designated, permanent and term percentages |

- **DAF value:** Schedule D Part I line 4 aggregate value at end of year. Where it is blank (4 sponsor-years), the corrected DAFRC value for the same FY is used and flagged `daf_value_from_dafrc`.

### 1.3 Reserve measures (EOY; all [C])
DAF assets are legally owned by the sponsor and are usually booked **without donor restrictions**, because the sponsor holds variance power. Part X line 27 therefore contains the DAFs. Six alternatives are carried:

| Measure | Definition | What it answers | Main bias |
|---|---|---|---|
| **R1 non-DAF net assets** | Part X line 32 − Schedule D DAF value | Everything the sponsor holds that is not a DAF | Includes donor-restricted endowment and other donor funds; for nationals a small difference between two large numbers |
| **R2 unrestricted less DAFs** | Line 27 − DAF value | Net assets free of donor restriction, assuming every DAF is booked without restriction | Negative where a sponsor books DAFs as restricted; includes board-designated endowment |
| **R3 literal** | Line 27 | What a naive reading of the 990 gives | Contains the DAFs (**do not use**) |
| **R4** | R2 − net PP&E (line 10c) | Unrestricted, non-fixed-asset reserve | Same as R2 |
| **R5** | R4 − (Schedule D Part V EOY endowment × board-designated %) | Undesignated unrestricted reserve (lower bound) | Part V can overlap the DAF and other-fund columns, so it can go negative |
| **R6** | R1 − Schedule D column (b) value | Non-DAF net assets less other donor-advised-like funds | Depends on what each sponsor puts in column (b); ≈ 0 where every fund is reported in Schedule D |

- **Months of cover** = reserve ÷ (annualised operating cost ÷ 12).
  - **Operating cost** follows the governing definition: Part IX line 25 − lines 1–3 − line 4 − line 11f.
  - `months_l25_r1` uses line 25 including grants. `months_mgmt_r1` uses M&G only.
  - A negative reserve gives negative months. That is the size of the shortfall, not an error.
- **Administrative expense** = Part IX line 25 column C (management & general) less column C of line 11f. It is shown as a share of operating cost and of line 25, and in bps of DAF assets.

### 1.4 Revenue mix and fee reliance
- **Shares of Part VIII line 12** for: contributions (1h), program-service revenue (2g), investment income (3+4+5) and net gains (7d). The residual is "other".
  - Shares are left blank when total revenue is ≤ 0 (flag `total_revenue_le_0`; no top-100 row in TY2021–24).
- **Fee lines** = Part VIII line 2 and line 11 rows whose description matches `fees?|administrat|admin|service charge|management fee|mgmt fee`. The descriptions are kept verbatim in `psr_rows` and `misc_revenue_rows`.
- **Coverage ratios:**
  - `fee_income_cover_opcost` = fee lines ÷ operating cost;
  - `inv_income_cover_opcost` = lines 3–5 ÷ operating cost;
  - `endowment_admin_cover_opcost` = Schedule D Part V line 1e ÷ operating cost.

### 1.5 Surplus / deficit measures (all [C])
| Measure | Definition |
|---|---|
| **S1** | Part I line 19 (revenue less expenses) [F] |
| **S2** | S1 − (Schedule D DAF contributions − DAF grants): strips net DAF inflow |
| **S3** | S2 − line 7d net gains |
| **S4** | S3 − lines 3–5: the pre-investment result |
| **ΔR1** | R1(TY) − R1(TY−1). Change in non-DAF net assets: Schedule D column (b) funds, endowment returns, PP&E, donor-restricted and campaign funds, the sponsor’s own operating fund where it is not reported inside the Schedule D DAF value (as at NCF, not at JCF), and any gap between the Schedule D DAF value and the balance sheet. Not an operating result [b4427-03] [V wave 40C] |

- **[I]** ΔR1 was proposed as the operating-result proxy, on the view that a DAF administrative fee moves value from DAF balances into sponsor-owned funds without passing through Part VIII. Audited statements do not support it as a margin ([b4014-b4427-sponsor-economics.md](b4014-b4427-sponsor-economics.md)). ΔR1 exceeds audited fee less operating expense by $47.6m and $70.7m at Fidelity, which pays its fee to FMR one for one; by $6.3m and $57.0m at RCF, which books its fee as Part VIII revenue; and by $129.3m and $182.6m at NCF. Only at JCF is it within about $1.6m, and that is coincidence: JCF’s R1 is its board-designated endowment plus its reserve fund, while the operating fund that receives the fee is reported inside the Schedule D DAF value. Treat ΔR1 as a non-DAF balance-sheet movement, not an operating result. [V wave 38B] [b4427-03] [V wave 40C]
- ΔR1 is blank for TY2021 (no TY2020 row, under the recency rule) and wherever either year is flagged `daf_share_break`.

### 1.6 Quality screens
- **`daf_share_break`:** a national or processor row whose DAF value is under 85% of net assets while the neighbouring years are over 95%. These rows are excluded from group statistics:
  - **NPT TY2022 (FY Jun-2023):** Schedule D $22.84bn against Part X $27.92bn. A roll-forward from FY2022 gives about $26.3bn before market gains; see P-B44N27-01.
  - **Servant Foundation TY2021.**
  - **Dechomai TY2021:** Schedule D $268m against $1,148m of net assets.
- **Group statistics** use `analysable` rows: not university / health, operating cost > 0, DAF value known, and no `daf_share_break`. That leaves 381 of 400 rows.
- **Other flags (counts across 400 rows):**

  | Flag | Rows |
  |---|---|
  | `daf_gt_na_without_restr` | 82 |
  | `daf_gt_total_na` | 31 |
  | `board_endowment_gt_unrestricted_less_daf` | 79 |
  | `escrow_agency_liability` | 61 |
  | `affiliate_costs_off_990` (every affiliated-commercial row) | 60 |
  | `amended_return` | 13 |
  | `opcost_lt_1bp_daf` | 5 |
  | `mgmt_column_zero` | 4 |
  | `no_asc958_split` (UCLA Foundation) | 4 |
  | `short_or_long_period` | 1 |

## 2. Coverage
| TY | Sponsor rows | Analysable | Notes |
|---|---|---|---|
| 2021 | 100 | 94 | Dechomai and Servant TY2021 excluded (`daf_share_break`); 4 university / health |
| 2022 | 100 | 95 | NPT excluded (`daf_share_break`) |
| 2023 | 100 | 96 | |
| 2024 | 100 | 96 | |

- The IRS index listed 415 returns, and all 415 parsed (`xml_status = ok`).

## 3. Group results, TY2024 (`group_year` rows)
Medians are over sponsors, with the IQR in brackets. "Pooled" means Σ reserve ÷ Σ operating cost.

| Group (n) | DAF % of net assets (median) | Months R1 | Months R2 | Months R5 | Months R6 | Pooled months R1 / R2 | R1 ≤ 0 | R2 ≤ 0 | M&G % of operating cost (median / pooled) | Operating cost bps of DAF (median) |
|---|---|---|---|---|---|---|---|---|---|---|
| Affiliated-commercial (15) | 99.6% | **29.4** (7.6–60.0) | 17.2 | 17.2 | 0.9 | 35.2 / 19.0 | 3 | 4 | 40% / 20% | 22.5 |
| Independent national (11) | 99.7% | **2.2** (−10.0–21.2) | 2.2 | 0.7 | −3.0 | 0.7 / 0.1 | 4 | 4 | 37% / 38% | 60.1 |
| Community foundation (55) | 59.2% | **417** (288–630) | 242 | 1.6 | 264 | 452 / 283 | 0 | 9 | 33% / 32% | 234 |
| Faith / single-issue (13) | 88.9% | **125** (43–194) | 72 | 3.8 | 30 | 112 / 63 | 1 | 3 | 60% / 55% | 175 |
| Processor (2) | 128% | 70.6 | 70.6 | 70.6 | 70.6 | 4.4 / 4.4 | 1 | 1 | 26% / 14% | 1,948 |
| All excluding university / health (96) | 75.8% | 245 | 74 | 6.1 | 36 | 245 / 152 | 9 | 21 | 37% / 33% | 171 |

- **Literal R3 (Part X line 27), median months:** affiliated-commercial 5,351; independent 1,984; community foundations 801; faith / single-issue 731.
- **Sponsors with R2 cover under 3 months:** 24 of 96.

### 3.1 Trend (TY2021 → TY2024; `group_year` medians)
| Group | Months R1 2021 / 22 / 23 / 24 | Months R2 2021 / 24 | M&G % of operating cost 2021 / 24 | Pooled operating cost growth / yr | Pooled R1 growth / yr |
|---|---|---|---|---|---|
| Affiliated-commercial | 22.3 / 26.7 / 27.5 / 29.4 | 19.6 / 17.2 | 42% / 40% | +13.5% | +9.8% |
| Independent national | 6.6 / 11.1 / 10.4 / 2.2 | 6.6 / 2.2 | 33% / 37% | −8.3% (CAF America and Greater Horizons cut costs) | n/a (R1 ≤ 0 in the pooled base) |
| Community foundation | 480 / 397 / 436 / 417 | 293 / 242 | 32% / 33% | +6.7% | +4.9% |
| Faith / single-issue | 176 / 163 / 132 / 125 | 73 / 72 | 58% / 60% | +14.2% | +0.7% |

The growth columns come from the `group_trend` rows: sponsors analysable in both TY2021 and TY2024 (15, 10, 55 and 13).

## 4. Nationals, processors and faith / single-issue sponsors: TY2024
- **Values:** $m are [F] (Schedule D, Part X) or [C] (R1, R2, R6, operating cost, ratios).
- **Columns:** "Fee lines" are description-matched Part VIII fee rows. ΔR1/op is the year-on-year change in R1 divided by annualised operating cost.

| # | Sponsor | Grp | Total NA $m | DAF $m | DAF % NA | R1 $m | R2 $m | R6 $m | Op. cost $m | M&G % op. | Months R1 | Months R2 | Months R6 | Fee lines $m | ΔR1/op | Months R1 TY2021 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable | AC | 85,862.7 | 85,481.7 | 100% | 381.0 | 291.6 | 0.0 | 203.1 | 0% † | 22.5 | 17.2 | 0.0 | 0.0 | 0.19 | 23.1 |
| 2 | NPT | IN | 55,802.4 | 55,895.4 | 100% | −93.0 | −93.0 | −93.0 | 66.9 | 50% | −16.7 | −16.7 | −16.7 | 0.6 | 2.15 | −69.1 |
| 3 | DAFgiving360 | AC | 47,423.9 | 47,352.6 | 100% | 71.3 | 71.3 | 6.2 | 87.4 | 10% | 9.8 | 9.8 | 0.9 | 0.0 | −0.45 | 22.3 |
| 4 | Vanguard Charitable | AC | 27,212.5 | 27,012.1 | 99% | 200.4 | 200.4 | 160.9 | 38.0 | 22% | 63.2 | 63.2 | 50.8 | 0.0 | 1.85 | 34.0 |
| 5 | GS DAPF | AC | 12,673.7 | 12,640.9 | 100% | 32.8 | 32.8 | 32.8 | 13.4 | 81% | 29.4 | 29.4 | 29.4 | 0.0 | 0.39 | 22.8 |
| 7 | AEF | IN | 8,403.4 | 8,378.0 | 100% | 25.4 | 25.4 | 25.4 | 22.9 | 19% | 13.3 | 13.3 | 13.3 | 0.0 | 0.07 | 4.8 |
| 8 | Morgan Stanley GIFT | AC | 8,975.7 | 9,109.1 | 101% | −133.4 | −133.4 | −133.4 | 18.4 | 100% | −86.8 | −86.8 | −86.8 | 0.0 | −2.56 | −68.4 |
| 9 | Renaissance | AC | 5,896.7 | 5,913.6 | 100% | −16.9 | −19.9 | −16.9 | 19.5 | 100% | −10.4 | −12.3 | −10.4 | 19.6 | 2.94 | −12.8 |
| 10 | NCF | SI | 6,030.4 | 5,683.7 | 94% | 346.7 | 346.7 | 202.0 | 80.8 | 79% | 51.5 | 51.5 | 30.0 | 0.0 | 1.31 | 101.0 |
| 11 | BofA Charitable Gift Fund | AC | 5,038.1 | 4,733.9 | 94% | 304.2 | 246.4 | 189.0 | 0.1 ‡ | — | ‡ | ‡ | ‡ | 0.0 | ‡ | ‡ |
| 13 | ImpactAssets | IN | 2,959.7 | 2,896.9 | 98% | 62.8 | 61.6 | −6.5 | 25.9 | 37% | 29.1 | 28.6 | −3.0 | 2.6 | −2.33 | 29.9 |
| 15 | Jewish Communal Fund | SI | 3,436.8 | 3,405.2 | 99% | 31.6 | 31.6 | 2.8 | 8.9 | 60% | 42.8 | 42.8 | 3.8 | 0.0 | 0.53 | 30.4 |
| 17 | Greater Horizons | IN | 2,492.7 | 2,531.1 | 102% | −38.4 | −38.4 | −332.2 | 4.8 | 27% | −96.2 | −96.2 | −832.9 | 0.0 | −10.21 | 8.4 |
| 18 | Dechomai | PR | 1,518.8 | 1,432.2 | 94% | 86.7 | 86.7 | 86.7 | 6.8 | 40% | 153.2 | 153.2 | 153.2 | 0.0 | 19.20 | (break) |
| 19 | CJP Boston | SI | 2,536.9 | 2,145.7 | 85% | 391.2 | 146.4 | 391.2 | 37.6 | 14% | 124.8 | 46.7 | 124.8 | 0.7 | 1.01 | 104.8 |
| 20 | Raymond James | AC | 2,360.3 | 2,324.8 | 98% | 35.6 | −0.2 | 24.7 | 7.6 | 27% | 55.8 | −0.4 | 38.8 | 0.0 | −0.26 | 10.1 |
| 21 | Ayco | AC | 1,164.8 | 1,158.0 | 99% | 6.8 | 6.8 | 6.8 | 2.5 | 27% | 32.5 | 32.5 | 32.5 | 0.0 | 0.59 | 17.8 |
| 22 | US Charitable Gift Trust | AC | 1,483.2 | 1,188.6 | 80% | 294.7 | 2.7 | −666.7 | 14.5 | 44% | 243.3 | 2.2 | −550.5 | 0.0 | 2.88 | 289.6 |
| 26 | DonorsTrust | SI | 1,362.8 | 1,211.8 | 89% | 151.0 | 150.6 | 21.0 | 5.3 | 30% | 341.9 | 341.1 | 47.7 | 0.0 | −0.86 | 449.8 |
| 30 | Servant Foundation | IN | 785.6 | 782.3 | 100% | 3.3 | 3.3 | 0.9 | 17.9 § | 36% | 2.2 | 2.2 | 0.6 | 0.8 | −0.53 | (break) |
| 31 | JCF San Francisco | SI | 1,787.6 | 1,358.5 | 76% | 429.2 | 163.1 | 429.2 | 26.6 | 62% | 193.7 | 73.6 | 193.7 | 2.7 | 0.89 | 205.1 |
| 32 | Bessemer Giving Fund | AC | 948.2 | 931.4 | 98% | 16.8 | 16.8 | 0.0 | 1.3 | 75% | 159.9 | 159.9 | 0.0 | 0.0 | 0.81 | 271.9 |
| 36 | American Gift Fund | IN | 638.8 | 642.6 | 101% | −3.8 | −3.8 | −3.8 | 3.9 | 89% | −11.8 | −11.8 | −11.8 | 0.0 | −0.47 | −3.9 |
| 37 | JCF Los Angeles | SI | 939.8 | 709.7 | 76% | 230.1 | 67.3 | 230.1 | 9.1 | 53% | 302.1 | 88.3 | 302.1 | 1.1 | 4.17 | 304.4 |
| 46 | T. Rowe Price | AC | 648.2 | 645.5 | 100% | 2.7 | 2.7 | 2.7 | 1.5 | 39% | 22.2 | 22.2 | 22.2 | 0.0 | −0.41 | 14.3 |
| 47 | Thrivent Charitable | SI | 800.5 | 594.3 | 74% | 206.2 | 168.1 | −17.9 | 14.4 | 81% | 172.2 | 140.3 | −15.0 | 0.0 | 1.48 | 587.8 |
| 51 | Independent Charitable Gift Fund | IN | 575.4 | 574.5 | 100% | 0.8 | 0.8 | 0.8 | 1.2 | 52% | 8.2 | 8.2 | 8.2 | 0.0 | −0.14 | 19.0 |
| 52 | Christian Community Foundation | SI | 676.3 | 674.3 | 100% | 2.0 | −19.7 | 0.5 | 13.9 | 53% | 1.7 | −17.0 | 0.5 | 7.4 | −0.72 | 39.5 |
| 53 | JCF San Diego | SI | 654.8 | 588.8 | 90% | 66.0 | 27.0 | 66.0 | 4.3 | 60% | 183.0 | 74.9 | 183.0 | 0.6 | 1.12 | 175.8 |
| 58 | Goldman Sachs Charitable Gift Fund | AC | 637.1 | 636.4 | 100% | 0.7 | 0.7 | 0.7 | 1.5 | 40% | 5.3 | 5.3 | 5.3 | 0.0 | 0.09 | 0.0 |
| 62 | Stifel Charitable | AC | 507.9 | 493.6 | 97% | 14.4 | 14.4 | −0.6 | 3.0 | 100% | 56.9 | 56.9 | −2.2 | 0.0 | 2.16 | 45.0 |
| 69 | CAF America | IN | 479.0 | 498.2 | 104% | −19.2 | −24.9 | −22.7 | 28.3 | 28% | −8.2 | −10.6 | −9.6 | 0.8 | −0.35 | 1.9 |
| 72 | Tides Foundation | SI | 476.9 | 324.5 | 68% | 152.3 | 152.3 | 0.0 | 25.4 | 87% | 72.0 | 72.0 | 0.0 | 0.3 | −0.76 | 267.2 |
| 74 | Impact Investing Charitable Trust | IN | 431.1 | 429.9 | 100% | 1.2 | 1.2 | 1.2 | 13.0 | 0% | 1.1 | 1.1 | 1.1 | 0.0 | 0.03 | −0.1 |
| 75 | The Signatry | IN | 815.5 | 796.8 | 98% | 18.6 | 18.6 | 8.8 | 4.2 | 100% | 53.1 | 53.1 | 25.0 | 0.0 | −4.65 | (tiny base) |
| 85 | FJC | IN | 422.0 | 369.1 | 87% | 52.9 | 50.1 | −39.0 | 2.9 | 47% | 219.7 | 208.0 | −161.9 | 0.3 | 1.28 | 35.0 |
| 88 | Johnson Charitable Gift Fund | AC | 383.4 | 383.4 | 100% | 0.0 | −78.6 | 0.0 | 0.9 | 100% | 0.0 | −1,086 | 0.0 | 0.0 | 0.00 | 0.0 |
| 89 | Jewish Federation of Metropolitan Chicago | SI | 863.3 | 392.6 | 45% | 470.7 | 198.2 | 470.7 | 27.4 | 16% | 205.9 | 86.7 | 205.9 | 1.0 | 0.82 | 250.1 |
| 90 | CCF-LA Supporting Organization | SI | 186.4 | 186.4 | 100% | 0.0 | 0.0 | 0.0 | 1.1 | 100% | 0.0 | 0.0 | 0.0 | 0.0 | 0.00 | 0.0 |
| 94 | Jewish Federation of Greater (as filed) | SI | 353.8 | 327.0 | 92% | 26.8 | −11.2 | 0.0 | 13.9 | 8% | 23.1 | −9.7 | 0.0 | 0.4 | −0.14 | 26.8 |
| 97 | AOGF | PR | 98.6 | 160.3 | 163% | −61.7 | −61.7 | −61.7 | 61.7 | 11% | −12.0 | −12.0 | −12.0 | 27.5 | −0.12 | −28.1 |

**Table notes**
- † Fidelity books all of Part IX in the program column. Its R1 equals its Schedule D column (b) value to the dollar [F].
- ‡ BofA reports operating cost of $0.1m against $4.73bn of DAFs (flag `opcost_lt_1bp_daf`). Months of cover are 51,554 (R1) and meaningless: its costs sit with the trustee bank, outside Part IX (cost-structure §8).
- § Servant Foundation's operating cost includes campaign advertising (the governing marketing correction). TY2024 is $17.9m against $169–237m in TY2022–23.

**Readings [I]**
- **Morgan Stanley GIFT:** the Schedule D DAF value exceeds net assets by exactly its total liabilities in every year ($107.0m, $97.7m, $86.2m, $133.4m). Schedule D appears to report DAF value before liabilities (grants payable), so its true own equity is about $0.
- **Renaissance:** books $19.6m of "administration fees" as Part VIII revenue, matching its $19.5m operating cost. It is the only affiliated sponsor whose fee economy is visible on the 990.
- **AOGF:** shows a $27.5m "administrative service fee" and has DAF value above net assets, with $171m of liabilities.

## 5. Community foundations (55): TY2024 detail
- **Balance sheet (medians) [C]:**
  - DAFs 59% of net assets;
  - donor-restricted net assets 7.7%;
  - Schedule D Part V endowment 38% of net assets (53 of 55 report one);
  - Schedule D column (b) other funds 6.8%.
- **R2 ≤ 0 (DAFs exceed net assets without donor restriction):** Foundation for the Carolinas, Marin, San Diego, Pittsburgh, Omaha, two foundations filed as "The Community Foundation …", Community Foundation for SW Washington, and Community Foundation for Greater (as filed) [C].
  - **[I]** These foundations classify part of their DAFs, or their endowment, as donor-restricted. R1 is the right comparator for them.
- **R2 cover under 12 months [C]:**

  | Foundation | Months (R2) |
  |---|---|
  | Communities Foundation of Texas | 11.2 |
  | East Bay | 10.8 |
  | Orange County | 8.7 |

- **R5 (excluding board-designated endowment) [C]:**
  - median 1.6 months;
  - negative at 26 of 55;
  - the flag `board_endowment_gt_unrestricted_less_daf` is set in 79 sponsor-years across all groups.
- **Fees [F]:** 36 of 55 report description-matched fee lines.
  - The largest are San Diego "Charitable gift admin" $26.4m, Foundation for the Carolinas "Administrative fees" $18.0m, Marin "Admin alloc – Buck Trust" $11.4m and Omaha "Administrative fees" $10.1m.
  - Most fee lines are fees from supporting organisations, agencies or other charities, not from the foundation's own DAFs.
- **Endowment administrative expenses (Schedule D Part V line 1e):** a pooled 24% of community-foundation operating cost [C].
- **ΔR1 [C]:** follows the markets. The median is −3.6× operating cost in TY2022, +4.2× in TY2023 and +3.1× in TY2024. 43 of 55 fell in TY2022; 2 fell in each of TY2023 and TY2024.

## 6. Revenue mix and fee reliance (pooled Part VIII shares, `group_year`)
| Group | TY | Contributions | Program service | Investment income (3–5) | Net gains (7d) | Fee lines ÷ op. cost (pooled / median) | Investment income ÷ op. cost (median) |
|---|---|---|---|---|---|---|---|
| Affiliated-commercial | 2021 | 84.5% | 0.0% | 4.5% | 11.0% | 4.1% / 0 | 6.0× |
| Affiliated-commercial | 2024 | 88.6% | 0.0% | 6.4% | 5.0% | 4.8% / 0 | 10.6× |
| Independent national | 2021 | 92.2% | 0.03% | 2.3% | 5.5% | 1.7% / 0 | 2.1× |
| Independent national | 2024 | 86.7% | 0.03% | 7.3% | 5.9% | 2.7% / 0 | 4.2× |
| Community foundation | 2021 | 74.4% | 0.5% | 4.7% | 20.4% | 12.3% / 4.5% | 1.2× |
| Community foundation | 2024 | 68.6% | 0.8% | 8.5% | 22.2% | 13.5% / 4.5% | 1.6× |
| Faith / single-issue | 2021 | 92.2% | 0.5% | 2.8% | 4.5% | 7.6% / 3.5% | 1.6× |
| Faith / single-issue | 2024 | 85.4% | 0.5% | 6.3% | 7.8% | 5.3% / 1.8% | 1.9× |
| Processor | 2024 | 107.0% | 1.1% | 0.5% | −8.7% | 40.1% / 22.3% | 0.2× |

- **[I]** The DAF administrative fee is the main operating revenue of every national sponsor, by their own fee schedules (`sponsor-fee-schedules.csv`). The 990 does not show it, because the fee is a transfer between funds the sponsor already owns.
- **[I]** "Reliance on fee income" therefore cannot be measured from Part VIII. It has no reliable balance-sheet trace: the fee surplus is not identifiable in ΔR1 at any of the five sponsors with audited fee data. [b4427-03] [V wave 40C] At affiliated nationals ΔR1 runs at about +0.4× operating cost each year. That does not show that fees retained exceed costs. Fidelity pays FMR an amount equal to its fee, and its other costs exceed the fee by $11.3m (FY2023) and $21.9m (FY2024). RCF passes 98% of its fee from fund holder accounts to Ren, leaving a $0.15–0.28m surplus (audits read in wave 38B). [V wave 38B]
- **[I]** Rising rates lifted investment income from 4.5% to 6.4% of revenue at affiliated nationals between TY2021 and TY2024, and from 2.3% to 7.3% at independents. Under asset-based fees, sponsor revenue tracks DAF asset values and market returns, not account activity.

## 7. Surplus and deficit (TY2024; `group_year`)
| Group | S2 deficits (ex net DAF flows) | Median S2 ÷ op. cost | S4 deficits (ex DAF flows and all investment) | Median S4 ÷ op. cost | ΔR1 < 0 | Median ΔR1 ÷ op. cost |
|---|---|---|---|---|---|---|
| Affiliated-commercial | 0 / 15 | +18.8 | 13 / 15 | −1.42 | 4 / 15 | +0.39 |
| Independent national | 3 / 11 | +5.5 | 10 / 11 | −1.01 | 7 / 11 | −0.35 |
| Community foundation | 3 / 55 | +3.5 | 41 / 55 | −0.66 | 2 / 55 | +3.07 |
| Faith / single-issue | 1 / 13 | +3.2 | 12 / 13 | −1.12 | 4 / 13 | +0.82 |
| All excluding university / health | 9 / 96 | +4.4 | 78 / 96 | −1.01 | 18 / 96 | +1.46 |

- S2 still contains investment income on DAF assets, so it is large and positive at nationals. S4 removes all investment income and is negative almost everywhere.
- **[I]** S4 does not show distress. It shows that operating costs are paid from returns on, or fees charged to, assets the 990 does not separate.
- **S2 deficits by year (all groups):** 5 (TY2021), 23 (TY2022), 19 (TY2023), 9 (TY2024).

## 8. Reading [I]
- **Nationals operate with thin, sometimes undisclosed, own equity.** Continuity rests on the fee stream and, for affiliated sponsors, on the parent's services agreement, not on a reserve.
  - A sponsor with zero or negative R1 (MS GIFT, Renaissance, Johnson, NPT, CAF America, AOGF) has no 990-visible buffer.
  - An entrant that partners with such a sponsor relies on the sponsor's contract and, for the affiliates, on the parent (P-B44N27-03).
- **Community foundations are balance-sheet rich but operationally fee-dependent.** Their 990 reserves are mostly endowment and designated funds. The undesignated cushion (R5) is a few months at the median, and their operating cost per $ of DAF is about 10× the affiliated nationals' (234 against 22.5 bps).
- **Cost growth outpaces own-equity growth** at affiliated nationals (13.5% against 9.8%/yr), community foundations (6.7% against 4.9%) and faith / single-issue sponsors (14.2% against 0.7%). Months of cover by R2 fell in every group with a stable sample.

## 9. Limitations
- **The DAF value basis differs from Part X.**
  - Schedule D Part I line 4 is "aggregate value at end of year" as each sponsor defines it. Some appear to report it before liabilities (MS GIFT) or before pending items.
  - Small R1 values at nationals (under 1% of net assets) are therefore within measurement error. Read the sign as "≈ 0", not as insolvency.
  - The `daf_share_break` rows are excluded, and NPT TY2022 is referred for verification (P-B44N27-01).
- **Classification is not on the 990.** Whether DAFs sit in line 27 or 28 is inferred from `daf_gt_na_without_restr`. Board designations beyond Schedule D Part V, liquidity (cash versus illiquid gifts) and lines of credit are not visible.
- **Costs off the 990.**
  - Affiliated-commercial sponsors buy staff, technology and fundraising from the parent under services agreements (compensation direction §5; cost-structure §8). The filings that speak show the charity paying the parent: Fidelity’s payment to FMR equals its donor fee and covers services that include fundraising, though FMR’s own cost of those services is “not separately stated”; Raymond James’s service agreement covers fundraising; DAFgiving360 reimburses Schwab for its workforce and books its own advertising; and Vanguard Charitable books its own fundraising expense while receiving $0.8–1.0m a year of in-kind professional services from Vanguard. Whether any parent spends more than it recovers, and any brand marketing it bears on its own account, are not disclosed. [b4427-03] [V wave 40C]
  - Their operating cost, and therefore their months of cover, describes the charity's bill from the affiliate, not the economic cost.
  - BofA's figures are unusable for months of cover.
- **Fee income is not reported as revenue.** The fee-line screen is description-based. It catches agency, supporting-organisation and consulting fees, but not internal DAF fees.
- **Whole-organisation figures.** Community-foundation, faith and federation ratios cover every programme, not only DAFs. University / health sponsors are excluded.
- **Groups are classifications [I]:**
  - Servant Foundation and The Signatry are "independent national" here (DAFRC type), but faith / single-issue in the compensation direction.
  - USCGT and Renaissance follow the compensation direction (affiliated-commercial).
- **No TY2020 base** under the recency rule, so ΔR1 starts in TY2022.
- **No invented values.** Every figure is computed from the cited e-file XML, the DAFRC panel or repo CSVs.

## 10. Data dictionary: `sponsor-financial-resilience-2021-2024.csv`
`row_type` is one of `sponsor_year` (400), `group_year` (24) or `group_trend` (6). Monetary columns are USD, rounded to the dollar. Ratios have 4 decimals; months and bps have 2.

**Sponsor-year: identification**

| Column | Meaning |
|---|---|
| `ein`, `sponsor_name`, `fy2024_asset_rank`, `dafrc_type`, `dafrc_subtype` | From the full harvest; rank is by FY2024 DAF assets |
| `sponsor_group`, `group_basis` | Group (§1.1) and its basis [I] |
| `tax_year`, `fiscal_year`, `tax_period_begin`, `tax_period_end`, `period_months` | Period of the return |
| `object_id`, `return_ts`, `xml_source` | IRS e-file object id; mirror (`gt_mirror`) or cached TEOS member |

**Sponsor-year: balance sheet [F]**

| Column | Meaning |
|---|---|
| `total_assets_eoy`, `total_liabilities_eoy`, `escrow_agency_liab_eoy`, `cash_and_savings_eoy`, `ppe_net_eoy` | Part X lines 16, 26, 21, 1+2 and 10c |
| `na_total_boy`, `na_total_eoy` | Part X line 32 (Part I fallback) |
| `na_without_restr_eoy`, `na_without_restr_boy`, `na_with_restr_eoy`, `na_lines_29_31_eoy`, `fasb_ind` | Part X lines 27, 28 and 29–31; ASC 958 checkbox |
| `daf_value_eoy`, `daf_value_source`, `daf_count`, `daf_contributions`, `daf_grants` | Schedule D Part I column (a), lines 1–4; source `990_sched_d` or `dafrc_corrected` |
| `other_funds_value_eoy`, `other_funds_count` | Schedule D Part I column (b) |
| `endowment_eoy`, `endowment_board_designated_pct`, `endowment_permanent_pct`, `endowment_term_pct`, `endowment_admin_expenses_cy` | Schedule D Part V, current year (line 1g, line 2, line 1e) |

**Sponsor-year: reserves and cover [C]**

| Column | Meaning |
|---|---|
| `daf_share_of_total_na` | DAF value ÷ line 32 |
| `r1_nondaf_na` … `r6_nondaf_na_less_other_funds` | Reserve measures (§1.3) |
| `months_opcost_r1` … `months_opcost_r6` | Reserve ÷ (annualised operating cost ÷ 12) |
| `months_mgmt_r1`, `months_l25_r1` | R1 against M&G only, and against line 25 |

**Sponsor-year: expenses**

| Column | Meaning |
|---|---|
| `l25_total_expenses`, `l25_program`, `l25_mgmt_general`, `l25_fundraising` | Part IX line 25, columns A–D [F] |
| `grants_l1_3`, `l04_member_benefits`, `l11f_invest_mgmt_fees`, `l11f_mgmt_column` | Part IX lines [F] |
| `admin_mgmt_ex_11f` | M&G less its line-11f cell [C] |
| `operating_cost`, `operating_cost_annualised` | Line 25 − lines 1–4 − 11f; annualised to 12 months [C] |
| `mgmt_share_of_l25`, `mgmt_share_of_opcost`, `opcost_bps_daf`, `mgmt_bps_daf` | Ratios [C] |

**Sponsor-year: revenue**

| Column | Meaning |
|---|---|
| `rev_total`, `rev_contributions_1h`, `rev_program_service_2g`, `rev_investment_income_3_4_5`, `rev_net_gains_7d`, `rev_net_rent_6d`, `rev_fundraising_events_8c` | Part VIII [F] |
| `rev_other_residual` | Line 12 minus the listed components [C] |
| `psr_rows`, `misc_revenue_rows` | Part VIII line 2 and line 11 rows, "description: amount", verbatim [F] |
| `fee_like_psr_rows`, `fee_like_misc_revenue`, `fee_income_on_990` | Description-matched fee lines (§1.4) [C] |
| `share_contributions`, `share_program_service`, `share_investment_income`, `share_net_gains` | Shares of line 12 (blank if line 12 ≤ 0) [C] |
| `fee_income_cover_opcost`, `inv_income_cover_opcost`, `endowment_admin_cover_opcost` | Coverage of operating cost [C] |

**Sponsor-year: surplus and flags**

| Column | Meaning |
|---|---|
| `s1_rev_less_exp_line19`, `daf_net_inflow`, `s2_ex_daf_flows`, `s3_ex_daf_flows_ex_gains`, `s4_ex_daf_flows_ex_all_investment`, `s2_per_opcost`, `s3_per_opcost`, `s4_per_opcost` | Surplus measures (§1.5) [F/C] |
| `xi05_unrealized_gains`, `xi09_other_changes` | Part XI lines 5 and 9 [F] |
| `r1_change_yoy`, `r1_change_per_opcost` | ΔR1 against the previous TY [C] |
| `daf_rollforward_residual_pct` | (DAF_t − (DAF_t−1 + contributions − grants)) ÷ DAF_t−1: implied investment return plus any break; blank where either year is flagged `daf_share_break` [C] |
| `quality_flags` | Pipe-separated (§1.6) |

**Group rows** (`group_year`: one per group × TY; `all_ex_university_health` is the sum of groups)

| Column | Meaning |
|---|---|
| `n_returns`, `n_sponsors` | Analysable rows |
| `n_r1_le_0`, `n_r2_le_0`, `n_months_r2_lt_3`, `n_r1_change_negative`, `n_r1_change_known`, `n_opcost_lt_1bp_daf`, `n_s2_deficit`, `n_s4_deficit`, `n_s4_known`, `n_psr_positive`, `n_fee_lines_positive`, `n_mgmt_column_zero`, `n_daf_gt_na_without_restr` | Counts |
| `sum_*` | Σ of the sponsor-year column |
| `med_*`, `p25_*`, `p75_*` | Median and quartiles over sponsors (non-blank values only; `med_endowment_admin_cover_opcost` covers only sponsors with Schedule D Part V) |
| `pooled_*` | Σ ÷ Σ: months of R1, R2 and R5; M&G share; revenue shares; fee and endowment-admin cover; DAF share of net assets; ΔR1 ÷ operating cost |

**Group rows** (`group_trend`: sponsors analysable in both TY2021 and TY2024)

| Column | Meaning |
|---|---|
| `med_<metric>_2021`, `med_<metric>_2024` | Medians for months R1, R2 and R5; M&G share; operating cost bps; program-service share; fee cover; S2 and S4 ÷ operating cost |
| `pooled_opcost_growth_pa`, `pooled_r1_growth_pa` | Compound annual growth |
| `n_s2_deficit_2021`, `n_s2_deficit_2024` | Counts |

## 11. Reproduce
```
python3 scripts/mission_sponsor_resilience.py --irs-dir IRS --cache-dir CACHE \
    --teos-dir B35/work/teos --teos-dir B38/work/teos --teos-dir V22/work/teos --fetch
```
- IRS holds `index_2021.csv` to `index_2026.csv`.
- CACHE receives `extract990res/{OID}.json` (about 3 MB for 415 returns). A re-run without `--fetch` works offline.
- The first run took 23 seconds, because parsing stops before Schedule E.

## Sources
- IRS Form 990 e-file XML via the GivingTuesday mirror, `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`. Examples:
  - Fidelity Charitable TY2024, [202601389349301700](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml);
  - NPT TY2022, [202431429349301368](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202431429349301368_public.xml);
  - NPT TY2023, [202511339349301311](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml);
  - Morgan Stanley GIFT TY2024, [202503239349300435](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml);
  - Renaissance TY2024, [202543189349301959](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml).
- IRS TEOS e-file index files `index_2021`–`index_2026` (local copies from earlier batches).
- DAFRC panel `dafrc-sponsor-schedule-d-fy2019-2024.csv` with `dafrc-corrections-itemized.csv` (fallback DAF values, 4 rows).

## Validation corrections (wave 29, 2026-11-15) — governing
Source: [validation-wave29-report.md](validation-wave29-report.md); register `data/mission-2026-11-14/validation-register-wave29.csv`.

1. **§0 item 1, affiliated R1 ≤ 0.**
   - **Find:** "Morgan Stanley GIFT (−$133m in every year, TY2021–2024), Renaissance (−$17m to −$81m) and Johnson Charitable Gift Fund (exactly $0)."
   - **Replace with:** "Morgan Stanley GIFT (−$86m to −$133m every year, TY2021–2024, each equal to its total liabilities), Renaissance (−$12m to −$81m) and Johnson Charitable Gift Fund (−$1, i.e. $0) [C; V wave 29]."
2. **§1.6, NPT break.**
   - **Find:** "  - **NPT TY2022 (FY Jun-2023):** Schedule D $22.84bn against Part X $27.92bn. A roll-forward from FY2022 gives about $26.3bn before market gains; see P-B44N27-01."
   - **Replace with:** "  - **NPT TY2022 (FY Jun-2023):** Schedule D $22.84bn against Part X $27.92bn. A roll-forward from FY2022 gives about $26.3bn before market gains; see P-B44N27-01.\n    - Wave 29 checked the XML: `DonorAdvisedFundsVlEOYAmt` is 22843599245 in return 202431429349301368, the only Form 990 for that period (no amendment). It is a real filed value, not a parse error. It is most likely a filer error [I]: reaching FY2024's $42.12bn from it would need a 32% return. DAFRC carries the same value, so N30's FY2023 uses it [V wave 29]."
3. **§4 Readings, MS GIFT.**
   - **Find:** "Schedule D appears to report DAF value before liabilities (grants payable), so its true own equity is about $0."
   - **Replace with:** "Schedule D appears to report DAF value before liabilities (grants payable), so its true own equity is about $0. The same identity holds for American Gift Fund in all four years and for Renaissance in TY2021 and TY2024 [C; V wave 29]."
