# P-B40N14-04 and P-B44N27-02: sponsor economics (Dechomai's share of sponsor intake; audited DAF fee margins)

**Date:** 2026-11-19. **Task ID:** b4014-b4427.

**Outputs**
- [`dechomai-share-of-sponsor-contributions-2026-11-19.csv`](../../data/mission-2026-11-14/dechomai-share-of-sponsor-contributions-2026-11-19.csv) (190 rows): Part A.
- [`sponsor-fee-revenue-margin-2026-11-19.csv`](../../data/mission-2026-11-14/sponsor-fee-revenue-margin-2026-11-19.csv) (50 rows, 25 sponsors × FY2023–2024): Part B.
- Script: [`scripts/mission_sponsor_economics.py`](../../scripts/mission_sponsor_economics.py). Stdlib only, functional. Run it as `python3 scripts/mission_sponsor_economics.py . --xml-dir <dir of e-file XMLs> --audit-text-dir <dir of pdftotext output>`. Two runs gave byte-identical CSVs.
- Queue proposals: [`queue-proposals-b4014-b4427.csv`](../../data/mission-2026-11-14/queue-proposals-b4014-b4427.csv) (6 rows).

**Evidence tags:** [F] read from a filing or audited statement; [C] computed by the script; [I] inference.

**Conventions**
- **TY** is the IRS tax year, the calendar year in which a return's period *begins*.
- **FY** is the year in which the period *ends*. FY6/23 runs from July 2022 to June 2023.
- DAFRC's `fiscal_year_end` follows the FY convention. For example, DAFgiving360's DAFRC FY2023 is its FY6/23 return.

---

## 1. Headlines

1. **Dechomai is a large source of new money for only some sponsors [C].**
   - Under the primary fiscal-year match, Dechomai's 2021–24 grants equal these shares of each sponsor's Schedule D DAF contributions over the matched years:

     | Sponsor | Share |
     |---|---|
     | AEF | 2.97% |
     | BofA Charitable Gift Fund | 1.54% |
     | GS DAF | 1.44% |
     | DAFgiving360 | 1.18% |
     | Vanguard Charitable | 0.72% |
     | MS GIFT | 0.44% |
     | Fidelity Charitable | 0.33% |
     | NPT | 0.11% |

   - The largest single sponsor-years are:
     - AEF CY2023: 7.36%, or **13.88%** if the $76.4m "Schwab Charitable Trust" line is attributed by EIN;
     - BofA CY2022: 4.14%;
     - GS DAF CY2021: 4.06%;
     - AEF CY2022: 3.89%;
     - Vanguard FY6/23: 2.09%.
2. **The task's example [C]:** Dechomai's CY2022 grants of $119,459,204 to DAFgiving360 equal **1.63%** of DAFgiving360's FY6/23 DAF contributions ($7,319,326,897). The adjacent years give 1.22% (FY6/22) and 1.28% (FY6/24).
3. **The fiscal-year choice moves single years a lot but pooled ratios little at June-year sponsors [C].** For calendar-year sponsors the three-year t−1 pools differ by up to 0.74 points (AEF 2.97% vs 3.71%; BofA 1.54% vs 2.20%). [V wave 38B]
   - For June-year sponsors, the pooled 2021–24 ratio shifts by at most 0.14 points between the primary match and the t−1 alternative: DAFgiving360 1.18% vs 1.32%; Vanguard 0.72% vs 0.79%; Fidelity 0.33% vs 0.40%.
   - Single years can swing by a factor of two or more. Vanguard CY2022 is 2.09% under the primary match, 1.63% at t−1 and 0.86% at t+1.
4. **Schedule D read straight from the XML matches the corrected DAFRC panel exactly [C].** All 32 sponsor-year returns that both sources cover agree to the dollar. This includes the four DAFRC FY2024 values that were imputed and later replaced by filed values: GS DAF, MS GIFT, BofA and AEF.
5. **Audited DAF fee economics are public for only a handful of the top 25 [F].**
   - 13 of the 25 sponsors post statements that this pass could read. Greater Horizons is also covered, because it is consolidated in the GKCCF audit.
   - Only **5** of those statements disclose the internal DAF fee: Fidelity, Renaissance (RCF), NCF, JCF and CJP.
   - **No sponsor books the internal DAF fee as ordinary third-party revenue that reaches the 990 except RCF.** The others treat it in one of three ways:
     - as an expense passed through to the administrator (Fidelity);
     - as an interfund transfer eliminated in consolidation (NCF, JCF, CJP);
     - netted into investment income without disclosure (Vanguard).
6. **Audited fee margins [F/C]:**

   | Sponsor | Fee basis | FY2023 | FY2024 |
   |---|---|---|---|
   | Fidelity | Administrative fee paid to FMR "equal to" the fee charged | $121.2m charged; other expenses $11.3m (−9.3%) | $139.7m charged; other expenses $21.9m (−15.7%) |
   | RCF | 98% of fee revenue paid to Ren | $16.10m fee; +$0.28m surplus (+1.7%) | $19.62m fee; +$0.15m surplus (+0.8%) |
   | JCF | Fee credited to the operating fund | $11.03m fee; +$2.24m surplus (+20.3%) | $11.79m fee; +$3.85m surplus (+32.6%) |
   | NCF (NCCF entity) | Ministry support fees | $42.0m fee vs $111.5m G&A + fund-raising | $47.4m fee vs $124.2m |

   - For Fidelity, the percentages are other expenses as a share of the fee: **−9.3%** and **−15.7%**.
   - Under Note C, fees and interest income in excess of operating expenses, up to $2,000,000, are granted to UJA; the operating fund granted $2.0m to UJA in each year (Note E). [V wave 38B] After that grant the surplus is $0.24m (FY2023) and $1.85m (FY2024).
   - NCCF's fee does not cover G&A plus fund-raising, which is funded otherwise [I]. The NCCF column's G&A likely includes fee payments between group entities: the eliminations column removes $55.2m and $61.1m from G&A, and the column's G&A plus fund-raising exceeds NCCF's own 990 operating cost ($71.8m and $80.8m). Against that 990 cost the gap is −$29.8m (−71.0%) and −$33.4m (−70.4%). On the consolidated statement, all-entity fees of $55.2m and $61.1m compare with G&A plus fund-raising after eliminations of $117.5m and $106.1m [C]. [V wave 38B]
   - CJP's DAF fee is small: $1.58m and $1.64m.
7. **Effective fee as bps of average DAF assets [C]:**

   | Sponsor | Effective fee |
   |---|---|
   | Fidelity | 22.9–23.4 bps, against a 0.60% headline: tier price credits and lower large-account rates [I] |
   | RCF | 38.7–43.7 bps |
   | JCF | 42.2–42.7 bps |
   | NCF | 88.8–89.0 bps |
   | CJP | 8.7–8.9 bps |

8. **The 990 balance-sheet proxy (ΔR1) is not an operating margin [C].** At the four sponsors with a computable audited surplus:
   - **Fidelity:** ΔR1 is +$36.3m and +$48.8m, while fee less opex is −$11.3m and −$21.9m. ΔR1 here is the growth of Schedule D "other funds".
   - **RCF:** ΔR1 is +$6.6m and +$57.2m, against a fee surplus of $0.28m and $0.15m.
   - **NCF:** ΔR1 is +$59.8m and +$105.8m, against −$69.5m and −$76.8m.
   - **JCF** is the closest match: ΔR1 of +$1.8m and +$3.0m against a fee surplus of $2.2m and $3.8m (after the UJA grant, $0.2m and $1.8m). Because the UJA grant leaves the operating fund, the like-for-like figure is the post-grant surplus, which ΔR1 exceeds by $1.56m and $1.18m [C]. [V wave 38B] The match is coincidental: JCF’s R1 equals its board-designated endowment (Schedule D column (b), the Special Gifts Fund) plus its reserve fund to the dollar, and the operating fund that receives the fee is reported inside the Schedule D DAF value. Endowment growth ($1.87m and $2.90m) is 104% and 96% of ΔR1 [C]. The audit’s Note C allows surplus above the $2.0m UJA grant to go to the Special Gifts Fund or a capital reserve, both inside R1, but the Note G roll-forward shows only investment return less appropriations in FY2023–24 [F]. [b4427-03] [V wave 40C]
   - The earlier direction ([direction-sponsor-financial-resilience.md](direction-sponsor-financial-resilience.md) §0 item 6) called ΔR1 "the preferred operating-result proxy". The audits show it mostly measures other-fund and endowment movements; the b4427-03 decomposition confirms this at Fidelity and JCF, finds Schedule D reporting-basis gaps at RCF and NCF, and finds endowment returns and Israel Emergency Fund campaign receipts at CJP [C]. [b4427-03] [V wave 40C] This qualifies the resilience study rather than contradicting it: that study already showed Fidelity’s R1 equal to its “other funds” and defined ΔR1 to include returns on own funds. What the audits do contradict is its reading that ΔR1 of about +0.4× operating cost at affiliated nationals means “fees retained exceed costs”: Fidelity retains none of its fee, and RCF retains 2%. [V wave 38B]

---

## 2. Part A: Dechomai grants as a share of sponsor DAF contributions (P-B40N14-04)

### 2.1 Method
- **Dechomai side [F→C]**
  - Schedule I lines from Dechomai Asset Trust and Dechomai Foundation, taken from `dechomai-dafpay-2026-11-19.csv` (`record_type = sched_i`, `selected = 1`, excluding intra-Dechomai lines).
  - Amount = cash + non-cash (`amount_usd + amount2_usd`), so AEF 2024 includes the $45.9m of LEGH shares.
  - The six national groups use the source study's name-first `sponsor_group` labels. Vanguard and BofA are matched by EIN (23-2888152, 04-6010342) or by name.
  - The script reproduces every group-year in the source study's routing table (`routing check: all group-years reproduced`), Vanguard's $121,486,348 and BofA's $74,372,113.
- **Wave 37B corrections applied** ([validation-wave37b-report.md](validation-wave37b-report.md)):
  - **Routing confirmed (V37B-06..09).** The one EIN/name conflict, DF TY2023 "SCHWAB CHARITABLE TRUST" for $76,391,938 under AEF's EIN, is carried in both forms: `attribution = name` (primary, as in the study) and `attribution = ein`.
  - **The Schedule M corrections (842 gifts, $3,274.2m) do not touch Schedule I** and so do not affect Part A.
- **Sponsor side [F]**
  - Schedule D Part I line 2, column (a), is read directly from each sponsor's e-file XML (one 990 per EIN × TY; period ≥ 300 days; latest `ReturnTs`, so amendments supersede).
  - Four returns were not selected:
    - Fidelity's superseded FY6/22 original;
    - BofA's CY2022 and CY2023 originals, both amended;
    - a 2-day DAFgiving360 period (2021-12-30 to 2021-12-31) with no Schedule D values.
  - Each value is cross-checked against the DAFRC panel plus the applied rows of `dafrc-corrections-itemized.csv`.
- **Matching rule (primary)**
  - Dechomai calendar year *t* is matched to the sponsor return whose tax period **begins in calendar year *t*** (the sponsor's TY *t*).
  - Calendar-year sponsors (AEF, GS DAF, MS GIFT, BofA) are matched to CY *t* exactly.
  - June-year sponsors (DAFgiving360, Fidelity, NPT, Vanguard) are matched to FY July *t* – June *t*+1. CY2022 goes to FY6/23, as in the task's example.
  - [I] The rule gives every sponsor the same "starts in *t*" convention. It credits a grant paid in July–December *t* correctly, and errs only for January–June grants. The source data has no payment dates, so the timing of Dechomai's grants within the year is unknown.
- **Alternatives (both adjacent years)**
  - `alt_ty_t_minus_1` and `alt_ty_t_plus_1` use the sponsor's TY *t*−1 and *t*+1.
    - For June-year sponsors these are FY6/*t* and FY6/*t*+2.
    - For calendar-year sponsors they are CY *t*−1 and CY *t*+1.
  - June-year sponsors also get an `overlap_weighted` variant: 0.5 × FY6/*t* + 0.5 × FY6/*t*+1, the two fiscal years that each overlap six months of CY *t*.
- **Recency rule**
  - Sponsor periods ending before 2021-01-01 are not used. That excludes CY2020 for calendar-year sponsors, so their *t*−1 for 2021 is blank.
  - FY6/21 (period July 2020 – June 2021) is used.
  - No TY2025 return is public at 2026-11-19, so *t*+1 for 2024 is blank for every sponsor. The IRS `index_2026` lists GS Charitable Gift Fund FY6/25 but none of the calendar-year sponsors' CY2025 returns.
- **Pooled ratios**
  - `pooled_2021_2024` sums grants and contributions over the four years. It is left blank when any matched year is missing.
  - `pooled_available_years` gives the same ratio over the years that do exist, with the years listed.

### 2.2 Results: primary match and both adjacent alternatives (name attribution) [C]

Share = Dechomai grants in CY *t* ÷ the sponsor's Schedule D DAF contributions in the matched year.

| Sponsor | CY *t* | Dechomai grants | Matched sponsor year (primary): contributions | **Primary** | Alt *t*−1 | Alt *t*+1 | Overlap-weighted |
|---|---|---|---|---|---|---|---|
| DAFgiving360 | 2021 | $111.4m | FY6/22: $9,756m | **1.14%** | 1.56% | 1.52% | 1.32% |
| DAFgiving360 | 2022 | $119.5m | FY6/23: $7,319m | **1.63%** | 1.22% | 1.28% | 1.40% |
| DAFgiving360 | 2023 | $76.4m† | FY6/24: $9,301m | **0.82%** | 1.04% | 0.69% | 0.92% |
| DAFgiving360 | 2024 | $136.0m | FY6/25: $11,100m | **1.23%** | 1.46% | n/a | 1.33% |
| Fidelity | 2021 | $91.3m | FY6/22: $15,196m | **0.60%** | 0.60% | 0.72% | 0.60% |
| Fidelity | 2022 | $89.2m | FY6/23: $12,620m | **0.71%** | 0.59% | 0.56% | 0.64% |
| Fidelity | 2023 | $24.4m | FY6/24: $15,915m | **0.15%** | 0.19% | 0.09% | 0.17% |
| Fidelity | 2024 | $29.8m | FY6/25: $26,464m | **0.11%** | 0.19% | n/a | 0.14% |
| AEF | 2021 | $13.3m | CY2021: $2,574m | **0.52%** | n/a (CY2020) | 1.02% | – |
| AEF | 2022 | $50.8m | CY2022: $1,306m | **3.89%** | 1.98% | 4.34% | – |
| AEF | 2023 | $86.2m† | CY2023: $1,171m | **7.36%** | 6.60% | 5.10% | – |
| AEF | 2024 | $50.2m‡ | CY2024: $1,690m | **2.97%** | 4.28% | n/a | – |
| GS DAF | 2021 | $86.2m | CY2021: $2,125m | **4.06%** | n/a | 5.19% | – |
| GS DAF | 2022 | $24.8m | CY2022: $1,660m | **1.50%** | 1.17% | 1.01% | – |
| GS DAF | 2023 | $40.3m | CY2023: $2,449m | **1.64%** | 2.43% | 0.69% | – |
| GS DAF | 2024 | $21.9m | CY2024: $5,834m | **0.38%** | 0.89% | n/a | – |
| MS GIFT | 2021 | $1.4m | CY2021: $2,390m | **0.06%** | n/a | 0.12% | – |
| MS GIFT | 2022 | $2.1m | CY2022: $1,250m | **0.17%** | 0.09% | 0.11% | – |
| MS GIFT | 2023 | $33.5m | CY2023: $1,876m | **1.79%** | 2.68% | 1.13% | – |
| MS GIFT | 2024 | $0.5m | CY2024: $2,959m | **0.02%** | 0.03% | n/a | – |
| NPT | 2021 | $12.3m | FY6/22: $13,187m | **0.09%** | 0.14% | 0.13% | 0.11% |
| NPT | 2022 | $5.9m | FY6/23: $9,212m | **0.06%** | 0.04% | 0.04% | 0.05% |
| NPT | 2023 | $7.4m | FY6/24: $14,524m | **0.05%** | 0.08% | 0.05% | 0.06% |
| NPT | 2024 | $31.2m | FY6/25: $15,154m | **0.21%** | 0.21% | n/a | 0.21% |
| Vanguard | 2021 | $18.4m | FY6/22: $3,021m | **0.61%** | 0.43% | 0.78% | 0.51% |
| Vanguard | 2022 | $49.4m | FY6/23: $2,360m | **2.09%** | 1.63% | 0.86% | 1.83% |
| Vanguard | 2023 | $24.9m | FY6/24: $5,747m | **0.43%** | 1.06% | 0.43% | 0.61% |
| Vanguard | 2024 | $28.9m | FY6/25: $5,751m | **0.50%** | 0.50% | n/a | 0.50% |
| BofA | 2021 | $1.0m | CY2021: $1,367m | **0.07%** | n/a | 0.10% | – |
| BofA | 2022 | $39.3m | CY2022: $949m | **4.14%** | 2.87% | 3.85% | – |
| BofA | 2023 | $14.9m | CY2023: $1,021m | **1.46%** | 1.57% | 1.00% | – |
| BofA | 2024 | $19.2m | CY2024: $1,490m | **1.29%** | 1.88% | n/a | – |

† Name attribution: the DF line "SCHWAB CHARITABLE TRUST" ($76,391,938) filed under AEF's EIN is credited to DAFgiving360. ‡ Includes $45,942,000 of LEGH shares granted in kind.

**Pooled 2021–2024 [C]**

| Sponsor | Grants 2021–24 | Primary | Alt *t*−1 | Alt *t*+1 | Overlap-weighted |
|---|---|---|---|---|---|
| AEF | $200.5m | **2.97%** | 3.71% (2022–24) | 3.61% (2021–23) | – |
| BofA | $74.4m | **1.54%** | 2.20% (2022–24) | 1.59% (2021–23) | – |
| GS DAF | $173.2m | **1.44%** | 1.40% (2022–24) | 1.52% (2021–23) | – |
| DAFgiving360 | $443.2m | **1.18%** | 1.32% | 1.11% (2021–23) | 1.25% |
| Vanguard | $121.5m | **0.72%** | 0.79% | 0.67% (2021–23) | 0.75% |
| MS GIFT | $37.5m | **0.44%** | 0.65% (2022–24) | 0.61% (2021–23) | – |
| Fidelity | $234.7m | **0.33%** | 0.40% | 0.37% (2021–23) | 0.36% |
| NPT | $56.8m | **0.11%** | 0.12% | 0.07% (2021–23) | 0.12% |

Ranges in brackets are the `pooled_available_years` rows; the other cells cover all four years.

### 2.3 The EIN-attribution alternative [C]
If the $76.4m DF TY2023 line follows its EIN to AEF:
- **AEF CY2023:** 13.88% under the primary match, 12.45% at *t*−1 and 9.62% at *t*+1. AEF's pooled ratio becomes 4.11%.
- **DAFgiving360 CY2023:** 0.00%. Its pooled ratio becomes 0.98%, against 1.18% by name.

Wave 37B notes that "Schwab Charitable Trust" is not the name Schwab uses elsewhere, so either field could be wrong. That is why both versions are kept (proposal P-B4014-01).

### 2.4 Reading the ratios [I]
- **They are upper bounds on "Dechomai's share of new DAF money".** Schedule D Part I line 2 counts contributions *to DAFs*. A Dechomai grant to a sponsor may land in a non-DAF fund, and Dechomai's Schedule I purpose for these lines is "unrestricted". Sponsors' Schedule B is redacted, so the receipt cannot be traced.
- **Money also flows back.** The sponsors granted $138.0m back to Dechomai in FY6/21–FY6/25 (b40n14-b38c §3.3): DAFgiving360 $73.3m and Fidelity $57.2m. Net of these flows, DAFgiving360's and Fidelity's ratios would be lower. This pass did not compute net ratios, because the reverse flows are not matched by year in the source CSV.
- **Dechomai is lumpy.** One sponsor-year can be 4–7% and the next under 1%. Use the pooled figure for any statement about dependence.

---

## 3. Part B: internal DAF fee revenue and margin, top-25 sponsors, FY2023–2024 (P-B44N27-02)

### 3.1 Method
- **Universe.** The top 25 by FY2024 DAF assets (`fy2024_asset_rank` in `sponsor-financial-resilience-2021-2024.csv`). Each sponsor is shown for FY2023 and FY2024, where FY is the year the fiscal period ends.
- **Audit search.**
  - For each sponsor: (1) the repo's prior audit links (`sponsor-audit-notes.csv` and research docs); (2) the sponsor's own financials page; (3) a web search for the PDF.
  - Every host's robots.txt was read before any fetch, with the generic agent `research-script/1.0`. A robots.txt that could not be reached (connection error) was treated as **disallow**. A 4xx robots response was treated as allow, but any page that itself returned 403 was not retried or bypassed. The full log is in §4.2.
  - No logins, forms, requests or outreach were made.
- **Fields read [F].** These come from the statement of activities, the functional-expense statement, and the notes on the administrative fee, related parties and liquidity.
  - **Internal DAF fee:** the fee charged to the sponsor's own DAF and other component funds, whether booked as revenue, as an expense pass-through, as an eliminated interfund transfer, or netted.
  - **External fee revenue:** fees from third parties, shown separately.
  - **Operating expenses:** the non-grant expense lines as printed. The components are listed in the CSV and investment-management fees are excluded.
  - **Liquidity:** where read.
- **Computed [C].**
  - `audit_fee_less_opex` = internal fee − operating expenses, and the margin = that figure ÷ fee. It is computed only where the fee is disclosed and the opex lines exist.
  - `internal_fee_bps_of_avg_daf_value` = fee ÷ the mean of the BOY and EOY Schedule D DAF value. The rates are not like-for-like across sponsors. NCF assesses ministry support fees on DAFs and other charitable funds, “typically based on a standard percentage of assets donated”, so its 89 bps is not an asset-based rate. CJP’s figure is an interfund fee from the DAF area to CJP Operations, not the donor fee. Compare bps only for Fidelity, RCF and JCF [I]. [V wave 38B]
  - Every figure was checked against the pdftotext output of its document (`figures_verified_in_text`, e.g. 5/5). All checks passed.
- **990 side.**
  - From the resilience CSV: ΔR1, where R1 = Part X line 32 − Schedule D DAF value, plus operating cost and ΔR1 ÷ operating cost.
  - From the XML [F]: `FSAuditedInd`, Part IX line 11g and Schedule O explanation lines that mention fees, administrative services or reimbursement.

### 3.2 Results by sponsor

**Audit availability, FY2024 rows [F]**

| Status | Sponsors |
|---|---|
| Statements read | 12: Fidelity, Vanguard (FY2024 only), SVCF, RCF, NCF, CCT, FFTC, JCF, GKCCF, CJP, Columbus, NYCT |
| Summary only, no auditor's report | 1: NPT |
| Consolidated in another sponsor's audit | 1: Greater Horizons (in GKCCF) |
| On request only | 2: AEF, ImpactAssets |
| Not posted | 4: GS DAF, MS GIFT, BofA, Dechomai |
| Blocked: HTTP 403 to a generic client | 2: DAFgiving360, US Charitable Gift Trust |
| Blocked: robots.txt disallows the path | 1: Oregon CF (`Disallow: /assets`) |
| Blocked: robots.txt unreachable | 2: Raymond James Charitable, Ayco (domains tried: rjcef.com, raymondjamescharitable.com, aycocharitable.com) |

All 25 FY2024 990s answer `FSAuditedInd` = true or 1, so every sponsor is audited. Most do not publish the audit.

**Where the internal fee is disclosed [F/C]**

| Rank | Sponsor | FY | Fee treatment (audit) | Internal fee | Opex as reported | Fee − opex | Margin | Fee bps of avg DAF | 990 ΔR1 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable | 2023 | Expense "Administrative fees" paid to FMR "equal to the administrative fee the Gift Fund charged its donors" | $121,190,522 | $132,481,848 | −$11,291,326 | −9.3% | 23.4 | +$36,318,324 |
| 1 | Fidelity Charitable | 2024 | same | $139,686,600 | $161,573,385 | −$21,886,785 | −15.7% | 22.9 | +$48,777,905 |
| 9 | Renaissance (RCF) | 2023 | Revenue line "Administrative fees"; 98% paid to Ren ($15,543,682) | $16,097,870 | $15,818,065 | +$279,805 | +1.7% | 43.7 | +$6,565,543 |
| 9 | Renaissance (RCF) | 2024 | same; Ren paid $19,225,546 | $19,617,095 | $19,467,587 | +$149,508 | +0.8% | 38.7 | +$57,191,335 |
| 10 | NCF (NCCF column) | 2023 | "Administrative fees and assessments", eliminated on consolidation ($55.2m all entities) | $42,004,000 | $111,478,000 (G&A + fund-raising) | −$69,474,000 | −165% | 89.0 | +$59,823,419 |
| 10 | NCF (NCCF column) | 2024 | same ($61.1m all entities) | $47,411,000 | $124,191,000 | −$76,780,000 | −162% | 88.8 | +$105,781,004 |
| 15 | Jewish Communal Fund | 2023 | Note C: fee "reduces the value of the donor-advised funds and increases the value of JCF's operating fund" | $11,032,543 | $8,794,758 | +$2,237,785 | +20.3% | 42.7 | +$1,800,400 |
| 15 | Jewish Communal Fund | 2024 | same | $11,789,740 | $7,944,558 | +$3,845,182 | +32.6% | 42.2 | +$3,022,727 |
| 19 | CJP (Boston) | 2023 | Consolidating schedule: fees paid by the DAF area to CJP Operations, eliminated | $1,582,000 | n/a (federation-wide operations) | – | – | 8.9 | +$15,644,129 |
| 19 | CJP (Boston) | 2024 | same | $1,642,000 | n/a | – | – | 8.7 | +$75,811,673 |

Notes:
- **Fidelity.** Opex = administrative fees + professional fees + other expenses. It equals the 990 operating cost to the dollar in both years. The negative figure is the cost *beyond* the pass-through fee: $1.2–1.3m of professional fees plus $10.0–20.7m of "other expenses". The sponsor itself earns no margin on the fee, because the contract sets the payment to FMR equal to the fee.
- **RCF.** Opex = M&G + fundraising. Note 9 bases Ren’s fee on 98% of administrative fee revenue “from individual fund holder accounts”. The FY2023 payment ($15,543,682) is 96.6% of the $16,097,870 fee line, and the FY2024 payment is 98.0% [C]. [V wave 38B] "Program services" ($568.7m and $770.8m) are grants. M&G + fundraising equals the 990 operating cost exactly in 2023 and to within $4 in 2024.
- **NCF.**
  - NCCF's "Program activities" ($2.05bn and $2.59bn) mix grants with programme cost, so opex here is G&A + fund-raising only.
  - G&A probably includes the share of ministry-support fees passed to Affiliates [I]. Treat the margin as a lower bound on what NCCF keeps.
  - Figures are in thousands in the source.
- **JCF.**
  - Opex = programme expenses other than grants + M&G + fund-raising. FY2024 equals the 990 operating cost ($7,944,558).
  - The operating fund also grants $2.0m a year to UJA (Note E[1]), which leaves +$237,785 (FY2023) and +$1,845,182 (FY2024).
  - Liquidity available within one year: $2.71bn and $2.78bn (Note H).
- **CJP.** Figures are in thousands in the source.

**Where the internal fee is not disclosed (statements read) [F]**

| Rank | Sponsor | FY2023 opex as reported | FY2024 opex as reported | External / other fee revenue | What the audit says about the DAF fee |
|---|---|---|---|---|---|
| 2 | NPT (summary statements) | $105.7m | $135.0m | "Administrative and maintenance fees" $0.90m and $0.99m | Not shown. The summary has no notes and no auditor's report |
| 4 | Vanguard Charitable | not found | $36.8m | – | Note 7: the 0.60% base fee "is wrapped in with investment income"; the amount is not disclosed. Vanguard's own service fee is $3.9m (FY2024) |
| 6 | SVCF | $72.6m | $69.0m | Other income $2.8m and $2.4m | Only the endowed-fund "support fee" policy (0.5–1.5%) is described |
| 12 | Chicago Community Trust (FY Sep) | $34.6m | $32.0m | – | Not disclosed. The reported "excess of operating support… over expenses" ($107.0m and $152.2m) reflects grant-matching transfers, not a fee margin |
| 14 | Foundation For The Carolinas | $48.8m | $52.2m | "Administrative fees received" (others' funds) $4.04m and $3.98m | Internal fees are eliminated. The endowment roll-forward shows admin fees and expenses of $3.5m and $4.4m |
| 16 | GKCCF (incl. Greater Horizons) | $21.4m | $23.3m | "Income from services" $1.92m and $1.81m | Operating fund pays all operating expenses. The operating reserve is $8.08m and $8.69m, against a target of ≥ 50% of a year's operating expenses |
| 23 | Columbus Foundation | $16.2m | $17.3m | – | Not disclosed (combined statements) |
| 24 | NYCT | $13.3m | $16.1m (admin + development only) | "Program" revenue $0.95m and $0.99m | Not disclosed |

Notes:
- **Vanguard.** FY2023 statements were not found on the site.
- **SVCF.** Figures are in thousands. The statements are consolidated with supporting organisations: net assets are $14.35bn against $10.53bn on the 990.

### 3.3 Audit figures against the 990 balance-sheet proxy [C]

`delta_r1_minus_audit_fee_less_opex` in the CSV:

| Sponsor | FY2023 | FY2024 | Reading [I] |
|---|---|---|---|
| Fidelity | +$47.6m | +$70.7m | R1 at Fidelity equals the Schedule D "other funds" column (wave 29), so ΔR1 is growth in non-DAF donor funds, not a sponsor margin. The fee itself nets to zero at the sponsor |
| RCF | +$6.3m | +$57.0m | ΔR1 is driven by the gap between Part X and Schedule D DAF value (R1 is negative throughout), not by operations. R1 = (total assets − Schedule D DAF value) − liabilities; at end-2024 the Schedule D DAF value equals total assets to the dollar, so R1 equals minus liabilities [C] [b4427-03] [V wave 40C] |
| NCF | +$129.3m | +$182.6m | ΔR1 includes NCCF's non-DAF charitable funds and annuity reserves. In 2024 NCCF’s audited operating net assets fell $4.8m while ΔR1 rose $105.8m; $110.5m of the rise is funds the audit counts as donor-advised or charitable beyond the Schedule D DAF value [C] [b4427-03] [V wave 40C] |
| JCF | −$0.4m | −$0.8m | Close by coincidence: R1 is the board-designated endowment (Schedule D column (b)) plus the reserve fund, and the operating fund sits inside the Schedule D DAF value, so ΔR1 is mostly endowment growth (104% and 96% of ΔR1) [C] [b4427-03] [V wave 40C] |

- **ΔR1 does not reproduce an audited fee margin at three of the four sponsors where one can be computed.** It should not be used as an "operating margin" at all: the decomposition in [b4427-03-b43n23-proxy-and-parent-marketing.md](b4427-03-b43n23-proxy-and-parent-marketing.md) finds the audited fee surplus identifiable in ΔR1 at none of the five sponsors. [b4427-03] [V wave 40C]
- **The 990 does capture the fee *paid to an administrator* in some cases [F]:**
  - RCF's Part IX line 11g ($15,667,168 and $19,225,546) equals or approaches the Ren payment;
  - MS GIFT's 11g is $13.1m and $16.0m;
  - Fidelity's administrative fee sits on a different Part IX line, and its 11g is $0.
- **Schedule O fee language [F].** 12 of 50 sponsor-year returns (6 sponsors × 2 years) have a Schedule O line mentioning fees, administrative services, reimbursement or an administrator:
  - DAFgiving360 describes its workforce as "employees of Charles Schwab & Co." under an administrative services agreement, reimbursed by the sponsor;
  - Fidelity says it "engages FMR LLC";
  - Raymond James Charitable engages Raymond James Trust N.A. under a service agreement;
  - RCF names Renaissance Administration LLC;
  - DAT says administrative services are provided by Charitable Solutions, LLC;
  - Vanguard's line is its mission text.
  - In the returns checked, none of these lines states a fee amount or rate (only years appear as numbers).

### 3.4 What this says about pricing headroom [I]
- **At bank- and broker-affiliated nationals the DAF fee is a transfer to the affiliate.** Fidelity passes it to FMR one for one. RCF keeps 2%, which is $0.15–0.28m on $16–20m. The economics sit at the affiliate, not in the charity's audit.
- **Where an independent or faith sponsor keeps the fee, the audited operating surplus is a modest share of it.** JCF keeps 20–33% before its UJA grant and 2–16% after. NCCF's fee covers well under half of G&A and fund-raising.
- **Effective fee rates are far below headline rates at the largest sponsor.** Fidelity's 0.60% headline produces about 23 bps of average DAF assets, because tier credits and advisor-managed pricing cut it [C/I].

---

## 4. Limits
- **Schedule D line 2 includes every DAF contribution**, so the Part A ratios are shares of gross intake. They are upper bounds if any Dechomai grant was booked outside DAFs (§2.4). Dechomai grant timing within the year is unknown, which is why both adjacent alternatives are shown.
- **TY2025 returns are not yet public**, so *t*+1 for 2024 is blank. CY2020 is excluded by the recency rule, so *t*−1 for 2021 is blank for calendar-year sponsors.
- **Part B covers 13 of 25 sponsors.** The fee is disclosed at 5 of them, and a fee margin is computable at 4 (Fidelity, RCF, NCF, JCF).
  - Statements are missing for 11 sponsors: not posted, on request only, or blocked (§3.2). DAFgiving360, the third-largest sponsor, returned HTTP 403 to the generic client and was not bypassed.
  - Vanguard FY2023 was not located.
- **"Operating expenses" follow each audit's own presentation.**
  - NYCT and NCF opex exclude programme costs that cannot be separated from grants on the face of the statements.
  - SVCF, Columbus and GKCCF statements are consolidated or combined with supporting organisations, so they are not the same scope as the 990.
  - NPT's document is a summary without notes or an auditor's report.
- **Auditor names and opinion types were not re-recorded here.** For Fidelity, Vanguard, RCF and NCF they are in `sponsor-audit-notes.csv`.
- **NPT FY6/23 Schedule D DAF value** carries the `daf_share_break` flag (P-B44N27-01), so ΔR1 for NPT FY2023 and FY2024 is blank in the source CSV and here.

### 4.1 Reproducibility
- XML inputs: 113 files. 84 were copied from earlier batches' local caches. 29 were fetched from the GivingTuesday mirror in this pass: 2 BofA returns for Part A and 27 top-25 returns for Part B. The mirror's robots.txt returns 404, so there are no restrictions.
- Audit text: `pdftotext -layout` output of each PDF listed in §5.
- The script runs offline from these two folders and the repo CSVs.

### 4.2 robots.txt and fetch log (2026-11-19, agent `research-script/1.0`)

| Host | robots.txt | Result |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | 29 XML, 200 |
| www.fidelitycharitable.org | 200, allowed | 2 PDFs |
| www.vanguardcharitable.org | 200, allowed | 1 PDF; `/about-us/financials` and `/financials` 404 |
| renaissancecharitable.org | 200, allowed | 2 PDFs |
| jcfny.org | 200, allowed | 1 PDF |
| www.cjp.org | 200, allowed | financials page + 2 PDFs |
| site.ncfgiving.com / www.ncfgiving.com | 200, allowed | 2 PDFs (FY2024, FY2025) + attachment page |
| www.fftc.org | 200, allowed | 1 PDF; `/financials` 403 |
| growyourgiving.org, www.greaterhorizons.org | 200, allowed | 2 PDFs (GKCCF 2024; Greater Horizons/GKCCF 2023) |
| www.svcf.org | 200, allowed | 2 PDFs + page |
| columbusfoundation.org / www.columbusfoundation.org | 404 (no rules) | financials page + 1 PDF |
| thenytrust.org | 200, allowed | page + 2 PDFs |
| www.cct.org | 200, allowed | 2 PDFs; `/about/financials/` 403 |
| www.nptrust.org | 200, allowed | 2 summary PDFs; `/about-npt/financials/` 404 |
| oregoncf.org | 200 | financials page allowed; **PDF path `/assets/...` disallowed, not fetched** |
| www.aefonline.org, impactassets.org, dechomai.org, www.morganstanley.com | 200, allowed | pages only (no statements posted) |
| www.dafgiving360.org | **403** | page 403, not bypassed |
| www.uscharitablegifttrust.org | **403** | page 403, not bypassed |
| www.rjcef.com, www.raymondjamescharitable.com, www.aycocharitable.com, www.gsphilanthropyfund.org | **unreachable** (connection error; guessed domains) | nothing fetched |

sec.gov, crt.sh, certspotter and ProPublica were not used.

---

## 5. Source register

| ID | Source | Date | Used in |
|---|---|---|---|
| S1 | Dechomai Schedule I lines: repo `data/mission-2026-11-14/dechomai-dafpay-2026-11-19.csv` (DAT/DF e-file XML, e.g. https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202343179349310654_public.xml) | 2026-11-19 | §2 |
| S2 | Validation wave 37B: `research/mission-2026-11-14/validation-wave37b-report.md` | 2026-11 | §2.1, §2.3 |
| S3 | Sponsor Schedule D Part I: e-file XML `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`. Per-row object IDs are in the Part A CSV. Vanguard 202211339349310116, 202331359349303108, 202441359349309439, 202511349349313096, 202621329349306657. BofA 202222869349300202, 202441809349301264, 202520169349301042, 202503219349318170. Others as in b40n14-b38c S6 | filed 2022–2026 | §2 |
| S4 | DAFRC dataset (repo panel `dafrc-sponsor-schedule-d-fy2019-2024.csv`; original https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) and `dafrc-corrections-itemized.csv` | 2025 ed. / 2026-11 | §2.1 |
| S5 | Fidelity Charitable audited statements FY2024/2023: https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf (also FY2025/2024: …/audited-financial-statements-2025-2024.pdf) | fetched 2026-11-19 | §3 |
| S6 | Vanguard Charitable statements FY2025/2024: https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf | fetched 2026-11-19 | §3 |
| S7 | RCF audited statements 2024 (with 2023): https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf ; 2023: …/2023RCFAuditedFinancialStatements.pdf | fetched 2026-11-19 | §3 |
| S8 | JCF statements FY2024/2023: https://jcfny.org/app/uploads/2025/07/JCF-FINAL-FS-FY2024.pdf | fetched 2026-11-19 | §3 |
| S9 | CJP audited statements 2023–2024: https://www.cjp.org/hubfs/Financial%20Statements/2024/Audited%20Financial%20Statements%202023%E2%80%932024.pdf ; 2022–2023: https://www.cjp.org/hubfs/Financial%20Statements/2023/Audited%20Financial%20Statements%202022%E2%80%932023.pdf | fetched 2026-11-19 | §3 |
| S10 | NCF consolidated statements 2024 (with 2023): https://site.ncfgiving.com/wp-content/uploads/2026/07/NCF-24-Consolidated-FS-Final.pdf (page https://www.ncfgiving.com/ncf-24-consolidated-fs-final/) | fetched 2026-11-19 | §3 |
| S11 | FFTC audited statements 2024 (with 2023): https://www.fftc.org/sites/default/files/2025-09/Foundation_For_The_Carolinas_12-31-24_Audited_Financials.pdf | fetched 2026-11-19 | §3 |
| S12 | GKCCF audit 2024 (with 2023; includes Greater Horizons): https://growyourgiving.org/wp-content/uploads/2025/11/Audit-Report-2024.pdf | fetched 2026-11-19 | §3 |
| S13 | SVCF audited statements 2024 (with 2023): https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2024.pdf | fetched 2026-11-19 | §3 |
| S14 | Columbus Foundation combined statements 2024 (with 2023): https://columbusfoundation.org/media/lnobyvu5/2024-columbus-foundation-combined-final-financial-statements-12-31-24.pdf | fetched 2026-11-19 | §3 |
| S15 | NYCT audited statements 2024 (with 2023): https://thenytrust.org/wp-content/uploads/2025/11/2024-Issued-Audited-Financial-Statements.pdf | fetched 2026-11-19 | §3 |
| S16 | CCT consolidated statements FY9/24 (with FY9/23): https://www.cct.org/wp-content/uploads/2025/03/2024_TheChicagoCommunityTrust_FS.pdf | fetched 2026-11-19 | §3 |
| S17 | NPT consolidated statements FY2024 (summary): https://www.nptrust.org/consolidated-statements-2024-npt | fetched 2026-11-19 | §3 |
| S18 | 990 proxy: repo `sponsor-financial-resilience-2021-2024.csv` (ΔR1, operating cost); top-25 e-file XML (FSAuditedInd, Part IX 11g, Schedule O), object IDs per row in the Part B CSV | 2026-11-15 / 2026-11-19 | §3.3 |
| S19 | Sponsor pages without statements: https://impactassets.org/required-state-disclosures/ ; https://www.aefonline.org/about-aef/ ; https://www.morganstanley.com/gift ; https://dechomai.org/faqs/ ; https://oregoncf.org/about/financials | fetched 2026-11-19 | §3.2 |
| S20 | IRS e-file index (local copy): https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv and earlier years | local copies 2026-11-14/15 | §2.1 |

---

## 6. Data dictionary

### 6.1 `dechomai-share-of-sponsor-contributions-2026-11-19.csv`

| Column | Meaning |
|---|---|
| row_type | `year` (one Dechomai year × match variant); `pooled_2021_2024` (all four years; blank if any missing); `pooled_available_years` (years with a matched return, listed in `dechomai_year`/`flags`) |
| sponsor, sponsor_ein | Recipient sponsor; GS DAF = Goldman Sachs Philanthropy Fund (31-1774905), the only GS entity Dechomai granted to |
| sponsor_fy_end_month | 6 = June fiscal year, 12 = calendar year |
| dechomai_year | Dechomai calendar (tax) year of the Schedule I grants |
| attribution | `name` (name-first, as in the source study and wave 37B) or `ein` (the DF TY2023 Schwab/AEF line follows its EIN; only AEF and DAFgiving360 have these rows) |
| match_variant | `primary_ty_t` (sponsor period begins in CY *t*); `alt_ty_t_minus_1`; `alt_ty_t_plus_1`; `overlap_weighted_fy_end_t_and_t_plus_1` (June-year sponsors only) |
| sponsor_tax_year, sponsor_period_begin, sponsor_period_end, sponsor_object_id | The matched sponsor return |
| dechomai_grants_usd | Cash + non-cash Schedule I grants from DAT and DF to the sponsor in `dechomai_year` |
| dechomai_schedule_i_lines | Number of Schedule I lines summed |
| sponsor_daf_contributions_sched_d_usd | Schedule D Part I line 2(a), read from the XML; blank if missing or pre-2021 |
| dafrc_fy | DAFRC fiscal year (year the period ends) used in the cross-check |
| dafrc_corrected_daf_contributions_usd, dafrc_value_source | DAFRC panel value after applied corrections, and its source (e.g. "IRS 990", "corrected: R1_filed_replaces_imputed") |
| sched_d_minus_dafrc_usd | XML value − DAFRC corrected value (0 for every comparable row) |
| share_of_sponsor_daf_contributions | dechomai_grants_usd ÷ sponsor_daf_contributions_sched_d_usd (fraction) |
| flags | `pre_2021_period_excluded_not_read`, `no_return_filed_or_not_yet_public`, `amended_return`, `sched_d_ne_dafrc`, pooled-coverage notes |
| source_url | Mirror URL of the sponsor return(s) |

### 6.2 `sponsor-fee-revenue-margin-2026-11-19.csv`

| Column | Meaning |
|---|---|
| rank_fy2024_daf_assets, ein, sponsor_name, sponsor_group | From the resilience CSV (groups as in that study) |
| fiscal_year, fy_end | FY (year the period ends) and the period end date |
| audit_status | `read`; `summary_only_no_auditor_report`; `year_not_found`; `on_request`; `not_public`; `consolidated_in_gkccf`; `blocked_http_403`; `blocked_robots_disallow`; `blocked_robots_unreachable` |
| audit_document_url | Statement read, or the page checked |
| reported_in_thousands | `yes` if the source prints thousands (values in the CSV are converted to USD) |
| fee_recognition | `revenue_line`; `expense_passthrough`; `eliminated_interfund`; `netted_not_disclosed`; `not_disclosed` |
| internal_daf_fee_usd | Administrative / ministry-support fee charged to the sponsor's own funds, as reported |
| external_fee_revenue_usd | Fee revenue from third parties, as reported |
| audit_operating_expenses_usd, audit_operating_expenses_components | Non-grant operating expenses as printed (components `label=value`); investment-management fees excluded |
| audit_fee_less_opex_usd, audit_fee_margin_pct | Internal fee − opex, and ÷ fee (%), where both exist |
| internal_fee_bps_of_avg_daf_value | Internal fee ÷ mean of BOY/EOY Schedule D DAF value, in bps |
| audit_other_figure_usd, audit_other_figure_label | One further reported figure (e.g. JCF's $2.0m operating-fund grant to UJA; GKCCF operating reserve; CCT reported operating excess; NCF all-entity eliminated fees) |
| liquidity_available_1yr_usd | Financial assets available within one year (liquidity note), where read |
| figures_verified_in_text | Count of cited figures found verbatim in the document text / count checked |
| tax_year_990, object_id_990 | The 990 for the same fiscal period |
| fs_audited_ind_990 | Form 990 Part XII `FSAuditedInd` |
| r1_nondaf_na_eoy_990_usd, delta_r1_990_usd, operating_cost_990_usd, delta_r1_per_opcost_990 | From `sponsor-financial-resilience-2021-2024.csv` (R1 = Part X line 32 − Schedule D DAF value) |
| part_ix_11g_other_fees_990_usd | Part IX line 11g total (fees for services – other) |
| sched_o_fee_lines_n, sched_o_fee_line_refs | Schedule O explanation lines matching fee / administrative services / reimbursement / administrator (first three, truncated) |
| delta_r1_minus_audit_fee_less_opex_usd | 990 proxy − audited fee less opex |
| note | Verbatim-anchored notes on the audit treatment |
| source_990_url | Mirror URL of the 990 |
