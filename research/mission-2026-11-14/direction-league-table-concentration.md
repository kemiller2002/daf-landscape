# Direction P-NEW-LGT-01: DAF sponsor league table and market concentration, FY2021–FY2025

**Date:** 2026-11-15 · **Queue item:** P-NEW-LGT-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv): 267 rows. The top 50 by DAF assets for each of FY2021–24, plus one row per top-50 exit; for FY2025, the FY2024 top-50 sponsors (filed or not yet filed) and six provisional entrants.
- [`data/mission-2026-11-14/daf-concentration-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-concentration-fy2021-2025.csv): 44 rows. CR1/CR3/CR5/CR10/CR50 and HHI by FY × metric × basis (gross corrected; R5-netted lower/central/upper; FY2025 covered filers only).
- [`data/mission-2026-11-14/queue-proposals-batch44-n30.csv`](../../data/mission-2026-11-14/queue-proposals-batch44-n30.csv): P-B44N30-01 and P-B44N30-02.
- **Script** (stdlib, functional style): [`scripts/mission_league_table.py`](../../scripts/mission_league_table.py). It reads repository data only and fetches nothing.

**Rules applied**
- **Governing corrections read first:**
  - wave 5 and wave 19 (end of [full-universe-990-harvest-and-corrected-totals.md](full-universe-990-harvest-and-corrected-totals.md)). Neither changes a sponsor value used here. Wave 19 only rewords the Jasper Ridge Schedule N amounts.
  - batch 34 ([queue-batch34-netting-filings.md](queue-batch34-netting-filings.md)): R5 netting and the W1–W5 whitelist are used unchanged.
  - wave 20 (end of [queue-batch35-panel-screens.md](queue-batch35-panel-screens.md)): support-test wording only, not used here. The batch-35 findings on AOGF's reclassification and Ayco's merger are used for churn reasons.
  - wave 24A (end of [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md)): ImpactAssets FY2024 is the filed **$2.897bn** (R1). The corrected totals already contain it, and so does this table (rank 13).
- **Recency:** the league table covers FY2021–FY2025. FY2020 corrected values are used only as the baseline for FY2021 entrants and exits.
- **Labels:** **[F]** filed value; **[C]** script computation; **[I]** inference.
- No fetching, logins, forms or outreach. **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **Who leads** | **The top four are national sponsors throughout: Fidelity, DAFgiving360 (Schwab), NPT and Vanguard** [C].<br>- Fidelity is #1 every year with 20.5–21.7% of corrected assets ($49.26bn FY2021 → $66.20bn FY2024).<br>- NPT overtook DAFgiving360 for #2 in FY2024: $42.12bn against $40.94bn.<br>- GS DAPF overtook SVCF for #5 in FY2023 and stayed there.<br>- 43 of the FY2021 top 50 are still in the top 50 in every year through FY2024. | High [C] |
| **Top-50 share** | **The top 50 hold 83–86% of assets and contributions and 78–81% of grants** [C]:<br>- assets 83.1%, 83.1%, 83.6%, **85.5%** (FY2021–24);<br>- contributions 82.7%, 82.2%, 81.3%, 82.9%;<br>- grants 81.3%, 78.9%, 78.6%, 77.9%;<br>- accounts only 14.5–22.2%, because micro-account processors (Givinga, AOGF, PPGF) sit outside the asset top 50.<br>The rank-50 entry threshold rose from $0.46bn (FY2021) to **$0.58bn** (FY2024). | High [C] |
| **Concentration** | **The market is concentrated at the top but unconcentrated by HHI** [C]:<br>- FY2024 assets: CR1 20.5%, CR3 46.2%, CR5 56.9%, CR10 68.8%, **HHI 853**;<br>- FY2024 contributions: CR5 55.3%, HHI 776;<br>- FY2024 grants: CR5 46.6%, HHI 653.<br>**Asset concentration is rising:** CR5 went 51.0% → 52.6% → 52.9% → 56.9% and HHI 734 → 853 (FY2021–24).<br>**Grant concentration is falling:** CR5 went 53.6% → 46.6% and HHI 803 → 653.<br>An HHI below 1,000 is "unconcentrated" on the conventional antitrust scale [I]. | High [C]; the HHI reading is [I] |
| **Gross vs netted grants** | **R5 netting barely moves market-level concentration**: FY2024 grant CR5 is 46.6% gross and 46.9% netted (central), and HHI is 653 against 669 (lower–upper 674–683). Central-tier HHI shifts are −53 to +16 points a year, and every tier stays within ±60 [C].<br>**It does move individual sponsors:**<br>- GS DAPF FY2021: 6.6% of gross grants → 3.0% netted, because $1.86bn went to other DAF sponsors (mostly NPT);<br>- SVCF FY2024: 4.6% → 2.5% ($1.61bn of outbound DAF-to-DAF);<br>- NPT 8.4% → 7.8% in FY2024.<br>Fidelity gains share after netting in FY2021 and FY2024 (to 22.1% and 19.9%). | High [C]; the tier weights are [I] (batch 34) |
| **Entrants and exits** | **2–3 changes a year in the top 50, all at the bottom of the table except two structural events** [C]:<br>- **Jasper Ridge** (#18 in FY2021) leaves in FY2022: R2 terminated, $0 at year end after Schedule N transfers to Schwab and Fidelity.<br>- **BNY Mellon CGF** (#48 in FY2023) leaves in FY2024: terminated December 2024 and wound into RCF; FY2024 year-end $4.7m (R1).<br>- **Ayco** (#25 in FY2024) files $0 for FY6/2025: it merged into GS DAPF on 2025-07-01.<br>**Notable entrants:**<br>- BofA CGF enters at #10 in FY2021. It has no DAFRC row before FY2021.<br>- Dechomai Asset Trust goes from #83 to #22 in FY2022 (+320%).<br>- UCLA Foundation goes from #66 to #41 in FY2023.<br>- Signatry goes from #81 to #35 in FY2024 after R1 replaced an imputed value.<br>All the other changes are drift of $0.4–0.6bn sponsors around the cut-off. | High [F/C] |
| **AOGF reclassification** | **It does not affect any FY2021–25 asset rank.** AOGF ranks below the top 50 by assets in every year ($0.27bn FY2024). Its account reclassification (710,352 → 695 DAFs) is in the FYE 2026-03 return, outside the window. It is #1 by accounts in FY2021 and in the FY2025 covered set, so the **accounts** concentration series will break in FY2026 [F/I]. | High [F] |
| **FY2025** | **Partial: 899 sponsors holding 67.6% of FY2024 corrected assets (62.4% of grants) have a parsed FY2025 return; 24 of the FY2024 top 50 do** (70.6% of top-50 assets) [C].<br>- Filed FY2025 year-end values: Fidelity **$85.48bn**, NPT **$55.90bn**, DAFgiving360 **$47.35bn**, Vanguard **$27.01bn** (all FY6/2025) [F].<br>- The 24 covered top-50 sponsors together: assets +23.2%, contributions +26.9%, grants +16.0% (FY2025 filed against FY2024 corrected) [C].<br>- **Not yet filed:** 26 top-50 sponsors, including GS DAPF, SVCF, MS GIFT, AEF, RCF, NCF and BofA CGF.<br>- **Provisional entrants:** six filers are already above the FY2024 rank-50 value, for example the Independent Charitable Gift Fund ($0.92bn) and Stifel Charitable ($0.71bn).<br>**No FY2025 market share, rank or CR is reported as a market figure, and nothing is extrapolated.** | High on filed values; FY2025 is incomplete by construction |

---

## 1. Method

### 1.1 Values
1. **FY2021–24: corrected sponsor-year values.** These are the DAFRC 2025 panel rows (`dafrc-sponsor-schedule-d-fy2019-2024.csv`), overridden by every `applied = 1` row of `dafrc-corrections-itemized.csv` (rules R1–R4).
   - R4 sponsor-years with no DAFRC row (Donors Fund FY2024, Greater Pike FY2024, Helping Hands and Christian Ministries FY2023) are added.
   - **Check [C]:** the rebuilt sums equal `dafrc-corrected-market-totals.csv` to the dollar for all 20 FY × metric cells (FY2020–24). FY2024 assets are $323,269,551,062.
2. **FY2025: filed Schedule D Part I values.**
   - Sources: `form990-returns-schedule-d-harvest-full.csv` (FY2025 rows with `xml_status = ok`) and `form990-harvest-2026-fill.csv` (the 144 rows from the 2026 TEOS zip).
   - Rows are chosen as follows:
     - one return per EIN, the latest submission (3 amended returns supersede their originals);
     - fill rows replace the harvest's `http_404` rows.
   - FY2025 values are **not corrected** (no R1–R4 pass exists for FY2025), **not a market total**, and not extrapolated.
   - **Plausibility screen (accounts only):** a filed count above 1,000 with an average below $5 per account is set blank. Two filers fail: California Home for the Aged files 3,168,551 "accounts", which equals its DAF dollar value, and Communities in Schools Gulf South files 101,046 accounts on $198k. Negative filed values, such as UCLA Foundation grants of −$109.8m, are kept as filed.
3. **Fiscal year** is the calendar year in which the tax period ends (DAFRC convention).

### 1.2 Ranking, shares and concentration
- **Rank:** by year-end DAF assets, ties broken by EIN. `rank_contributions` and `rank_grants` give the same sponsor's rank on the flows.
- **Share (FY2021–24):** sponsor value ÷ corrected market total, for each metric.
- **Share (FY2025):** sponsor value ÷ the positive sum over FY2025 filers only. These shares are labelled `fy2025_filed_covered_total_only` and are not market shares.
- **CRn:** sum of the top n positive values ÷ market total, for n = 1, 3, 5, 10 and 50.
- **HHI:** Σ(100 × share)² over all sponsors, on a 0–10,000 scale. Negative sponsor values count as 0.

### 1.3 Gross vs netted (R5)
- **Market level:** the netted totals are those of `dafrc-market-totals-netted.csv`, in all three tiers.
- **Sponsor level:** the script rebuilds the R5 lines using the functions of `mission_market_netting.py`, unchanged, over the cached `netpayout990/` Schedule I extracts.
  - Each capped line is attributed to its **grantor**: netted grants = corrected grants − outbound R5.
  - It is also attributed to its **recipient**: netted contributions = corrected contributions − inbound R5.
  - **Check [C]:** the rebuild reproduces the published R5 amounts to the dollar for all 12 FY × tier cells. For example, FY2024 central is $8,031,010,978.
- Netting applies to grants and contributions only. Assets and accounts are stocks.

### 1.4 Entrants, exits and reasons
- **FY2021–24:** entrants are sponsors in the year's top 50 but not the prior year's; exits are the reverse.
- **Reason classes:**
  - `termination`, `merger` or `late_filer_r4`: a documented event from the repository, with the source named in the row;
  - `new_to_panel`: no positive prior-year row;
  - `rank_drift`: the prior and current ranks and the asset change.
- **FY2025 is not re-ranked against FY2024**, because 26 of the top 50 have not filed. Instead:
  - each FY2024 top-50 sponsor is shown as `filed_fy2025`, `not_yet_filed` or `exit` (a documented event with $0 filed);
  - non-top-50 filers whose FY2025 assets exceed the FY2024 rank-50 value ($581,066,147) are shown as `provisional_entrant`.

---

## 2. League table, FY2021–FY2024 (top 10; the full top 50 is in the CSV)

Values are corrected (R1–R4). "Grant share" is gross corrected → netted (R5 central). "DAFgiving360" is DAFRC's "Donor Advised Charitable Giving Inc" (Schwab Charitable). GS DAPF is the Goldman Sachs Philanthropy Fund.

### FY2024 (market: assets $323.27bn, contributions $92.77bn, grants $66.44bn, 3,309,483 accounts)

| # | Sponsor | Assets | Share | Contrib. | Grants | Accounts | Grant share gross → netted |
|---|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable | $66.20bn | 20.5% | $15.91bn | $12.66bn | 204,614 | 19.1% → 19.9% |
| 2 | National Philanthropic Trust | $42.12bn | 13.0% | $14.52bn | $5.56bn | 17,940 | 8.4% → 7.8% |
| 3 | DAFgiving360 | $40.94bn | 12.7% | $9.30bn | $6.62bn | 112,188 | 10.0% → 10.1% |
| 4 | Vanguard Charitable | $21.95bn | 6.8% | $5.75bn | $3.06bn | 27,660 | 4.6% → 4.5% |
| 5 | GS DAPF | $12.64bn | 3.9% | $5.83bn | $3.07bn | 4,134 | 4.6% → 4.6% |
| 6 | Silicon Valley CF | $9.58bn | 3.0% | $2.84bn | $3.06bn | 1,011 | 4.6% → **2.5%** |
| 7 | Morgan Stanley GIFT | $9.11bn | 2.8% | $2.96bn | $1.65bn | 21,800 | 2.5% → 2.8% |
| 8 | American Endowment Foundation | $8.38bn | 2.6% | $1.69bn | $1.31bn | 15,947 | 2.0% → 1.7% |
| 9 | Renaissance Charitable Foundation | $5.91bn | 1.8% | $2.16bn | $0.77bn | 25,824 | 1.2% → 1.3% |
| 10 | National Christian Foundation | $5.68bn | 1.8% | $2.91bn | $2.43bn | 31,943 | 3.7% → 3.9% |

- **Ranks 11–15:** BofA CGF ($4.73bn), Chicago Community Trust ($4.65bn), ImpactAssets ($2.90bn, filed per wave 24A), Jewish Communal Fund ($2.87bn) and Foundation for the Carolinas ($2.62bn).
- **Composition:** 20 national, 21 community-foundation and 9 single-issue sponsors.
- **Corrections in the top 50:** 23 top-50 rows carry an R1 replacement. One metric is still imputed: UCLA Foundation grants.

### Top-10 ranks by year (assets, $bn; share of corrected assets)

| # | FY2021 | FY2022 | FY2023 | FY2024 |
|---|---|---|---|---|
| 1 | Fidelity 49.26 (21.1%) | Fidelity 47.84 (21.0%) | Fidelity 55.60 (21.7%) | Fidelity 66.20 (20.5%) |
| 2 | DAFgiving360 25.50 (10.9%) | DAFgiving360 26.30 (11.5%) | DAFgiving360 31.54 (12.3%) | **NPT 42.12 (13.0%)** |
| 3 | Vanguard 16.00 (6.8%) | **NPT 21.52 (9.4%)** | NPT 22.84 (8.9%) | DAFgiving360 40.94 (12.7%) |
| 4 | NPT 15.94 (6.8%) | Vanguard 15.05 (6.6%) | Vanguard 16.84 (6.6%) | Vanguard 21.95 (6.8%) |
| 5 | SVCF 12.75 (5.4%) | SVCF 9.39 (4.1%) | **GS DAPF 8.87 (3.5%)** | GS DAPF 12.64 (3.9%) |
| 6 | GS DAPF 8.62 (3.7%) | GS DAPF 7.46 (3.3%) | SVCF 7.48 (2.9%) | SVCF 9.58 (3.0%) |
| 7 | AEF 7.06 (3.0%) | AEF 6.23 (2.7%) | AEF 7.10 (2.8%) | MS GIFT 9.11 (2.8%) |
| 8 | MS GIFT 6.13 (2.6%) | MS GIFT 5.63 (2.5%) | MS GIFT 7.06 (2.8%) | AEF 8.38 (2.6%) |
| 9 | NCF 4.57 (2.0%) | NCF 4.44 (1.9%) | NCF 5.00 (1.9%) | RCF 5.91 (1.8%) |
| 10 | BofA CGF 3.54 (1.5%) | BofA CGF 3.23 (1.4%) | RCF 4.22 (1.6%) | NCF 5.68 (1.8%) |

**Flow ranks differ from asset ranks** [C]:
- NPT is #2 by contributions in FY2021–24 and #2 by grants in FY2021–22.
- SVCF is #3 by grants in FY2023 ($4.89bn) while #6 by assets.
- NCF is #5–#8 by grants on #9–#10 assets.
- AEF and RCF rank lower on grants (#10–#11 and #16–#20) than on assets.

### Top-50 aggregates

| FY | Top-50 share: assets | Contributions | Grants (gross) | Grants (netted central) | Accounts | Rank-50 threshold | Rank-50 sponsor |
|---|---|---|---|---|---|---|---|
| 2021 | 83.1% | 82.7% | 81.3% | 79.7% | 22.2% | $0.46bn | Pittsburgh Foundation |
| 2022 | 83.1% | 82.2% | 78.9% | 79.6% | 14.5% | $0.44bn | Communities Foundation of Texas |
| 2023 | 83.6% | 81.3% | 78.6% | 77.5% | 16.7% | $0.51bn | T. Rowe Price Program for Charitable Giving |
| 2024 | 85.5% | 82.9% | 77.9% | 77.0% | 17.0% | $0.58bn | Saint Paul & Minnesota Foundation |

---

## 3. Entrants and exits

| FY | Entrants (prior rank → rank) | Exits (prior rank → rank) | Reason class |
|---|---|---|---|
| 2021 | **BofA CGF (new → 10)**; T. Rowe Price Program (54 → 48); Communities Foundation of Texas (52 → 49) | Thrivent Charitable (42 → 55, assets −12.1%); Greater Cincinnati Foundation (49 → 63); Omaha CF (50 → 54) | BofA: `new_to_panel` (no DAFRC row before FY2021). Others: drift |
| 2022 | **Dechomai Asset Trust (83 → 22, +320%)**; BNY Mellon CGF (61 → 49) | **Jasper Ridge (18 → $0)**; Pittsburgh Foundation (50 → 60) | Jasper Ridge: `termination` (R2; Schedule N to Schwab and Fidelity; 990-PF from 2023) |
| 2023 | UCLA Foundation (66 → 41, +72%); Tulsa CF (53 → 43); American Gift Fund (52 → 47) | Tides Foundation (39 → 66, −36%); East Bay CF (47 → 55); Communities Foundation of Texas (50 → 53) | Drift |
| 2024 | **Signatry (81 → 35, +164%, R1 filed value)**; Thrivent (51 → 47); CF of Tampa Bay (64 → 49) | **BNY Mellon CGF (48 → 745)**; Seattle Foundation (44 → 52); Goldman Sachs Charitable Gift Fund (49 → 57) | BNY: `termination` (December 2024, wound into RCF, $619.8m granted to RCF; FY2024 year-end $4.7m) |
| 2025 (partial) | Provisional: Independent Charitable Gift Fund ($0.92bn), Stifel Charitable ($0.71bn), Christian Community Foundation ($0.67bn), Goldman Sachs Charitable Gift Fund ($0.64bn), JCF San Diego ($0.59bn), Communities Foundation of Texas ($0.58bn) | **Ayco (25 → $0)**; 26 others `not_yet_filed` | Ayco: `merger` into GS DAPF, 2025-07-01 (final FY6/2025 return; $1,162.2m transfer to GS DAPF) |

**Other structural events in the window**
- **TIAA Charitable** (FY2021, R2) and **Donors Fund** (FY2024, R4: $315.8m) are outside the top 50, so they cause no churn.
- **AOGF's reclassification** is outside the window (§0).
- **SDG Impact Fund**, which is not in DAFRC, filed $10.10bn of DAF assets in FY2021 and FY2022. It would rank #6 in FY2021 and #5 in FY2022 if it were in the panel. It is **not** added here, so the DAFRC universe is kept (see P-99F-02 and proposal P-B44N30-02).
- **GS DAPF + Ayco (common control):** together they held $13.80bn of corrected FY2024 assets. That would still be #5 [C].

**Stability:** 43 of the FY2021 top 50 are in the top 50 in each of FY2022–24. Every change in the top 10 is a reordering among the same 11 sponsors (BofA CGF drops from #10 to #11 when RCF enters at #10 in FY2023).

---

## 4. Concentration

### 4.1 Gross corrected (FY2021–24)

| FY | Metric | Market | CR1 | CR3 | CR5 | CR10 | CR50 | HHI |
|---|---|---|---|---|---|---|---|---|
| 2021 | Assets | $234.01bn | 21.1% | 38.8% | 51.0% | 63.8% | 83.1% | 734 |
| 2022 | Assets | $228.14bn | 21.0% | 41.9% | 52.6% | 64.5% | 83.1% | 766 |
| 2023 | Assets | $256.37bn | 21.7% | 42.9% | 52.9% | 65.0% | 83.6% | 801 |
| 2024 | Assets | $323.27bn | 20.5% | 46.2% | **56.9%** | 68.8% | 85.5% | **853** |
| 2021 | Contributions | $77.52bn | 19.7% | 40.0% | 50.3% | 65.2% | 88.2% | 718 |
| 2022 | Contributions | $76.48bn | 19.9% | 49.9% | 56.8% | 68.1% | 88.3% | 922 |
| 2023 | Contributions | $65.37bn | 19.3% | 44.6% | 52.0% | 64.9% | 88.3% | 783 |
| 2024 | Contributions | $92.77bn | 17.2% | 42.8% | 55.3% | 69.2% | 89.7% | 776 |
| 2021 | Grants | $48.03bn | 20.9% | 42.0% | 53.6% | 68.2% | 87.6% | 803 |
| 2022 | Grants | $55.61bn | 20.5% | 39.0% | 49.5% | 64.0% | 87.7% | 718 |
| 2023 | Grants | $54.83bn | 18.8% | 36.9% | 48.9% | 64.3% | 86.8% | 669 |
| 2024 | Grants | $66.44bn | 19.1% | 37.4% | 46.6% | 62.4% | 86.9% | 653 |
| 2021 | Accounts | 1,888,462 | 40.6% | 74.6% | 80.9% | 87.2% | 93.9% | 2,405 |
| 2022 | Accounts | 3,258,113 | 47.4% | 79.2% | 87.5% | 91.4% | 96.3% | 2,906 |
| 2023 | Accounts | 3,030,383 | 31.5% | 75.9% | 85.4% | 89.9% | 95.9% | 2,034 |
| 2024 | Accounts | 3,309,483 | 42.9% | 76.2% | 85.8% | 89.7% | 96.0% | 2,505 |

**Reading [C/I]**
- **Assets concentrate at ranks 2–5, not at #1.** CR1 is flat at about 21%. CR3 rose 7.4 points (38.8% → 46.2%), mostly through NPT: 6.8% → 13.0%.
- **Grants de-concentrate.** Fidelity's grant share is flat at 19–21%. The rest of the top five lost share: NPT went from 13.3% to 8.4%, while DAFgiving360 gained (7.7% → 10.0%).
- **Contributions are the most volatile.** FY2022 CR3 is 49.9% because NPT received $13.19bn that year.
- **The account series is not a sponsor-size measure.** #1 is AOGF in FY2021 and Givinga in FY2022–24 (micro-account processors; see P-B35A-01). Use it only with the batch-35 caveats.

### 4.2 Gross vs netted grants and contributions (R5)

| FY | Grants CR5 gross → central [lower; upper] | Grants HHI gross → central [lower; upper] | Contributions CR5 gross → central | Contributions HHI gross → central |
|---|---|---|---|---|
| 2021 | 53.6% → 51.2% [51.7; 51.7] | 803 → 817 [823; 834] | 50.3% → 48.7% | 718 → 707 |
| 2022 | 49.5% → 48.6% [49.6; 48.6] | 718 → 665 [701; 661] | 56.8% → 56.8% | 922 → 924 |
| 2023 | 48.9% → 48.3% [48.4; 48.5] | 669 → 658 [657; 665] | 52.0% → 52.2% | 783 → 788 |
| 2024 | 46.6% → 46.9% [47.1; 47.4] | 653 → 669 [674; 683] | 55.3% → 56.0% | 776 → 782 |

- **Netting changes concentration by less than 3 CR points and 60 HHI points in every year and tier** [C].
- R5 removes 7–12% of grants, but the removal is spread across the large sponsors that send DAF-to-DAF transfers (Fidelity, NPT, DAFgiving360, GS DAPF and SVCF), so the shape barely changes.
- **The individual effect is large where one year holds one big transfer:**
  - GS DAPF FY2021: $1.86bn outbound, grant share 6.6% → 3.0%;
  - SVCF FY2024: $1.61bn outbound, 4.6% → 2.5%;
  - Fidelity FY2022: $2.08bn outbound, 20.5% → 18.9%.
- **Recipient side:** NPT received $2.07bn (FY2021) and $2.42bn (FY2024) of netted inbound transfers. That is why its netted contributions share is below its gross share.

### 4.3 FY2025 (covered filers only; not market concentration)
- The concentration CSV carries FY2025 rows with basis `fy2025_filed_covered_only`. For example, the assets CR5 among covered filers is 82.9%.
- **These are not comparable with FY2021–24.** The covered set has all four of the largest sponsors but lacks GS DAPF, SVCF, MS GIFT, AEF, RCF and NCF, so its CRs are inflated by construction.
- **Coverage:**
  - 899 sponsors with a parsed FY2025 return;
  - 67.6% of FY2024 corrected assets and 62.4% of grants;
  - 24 of the FY2024 top 50, holding 70.6% of top-50 assets.
  - The latest index used, index_2026, is Last-Modified 2026-10-21 (batch 35).
- **Same-sponsor change:** the 24 covered top-50 sponsors moved from $194.99bn of corrected FY2024 assets to $240.14bn filed for FY2025 (+23.2%). Grants went from $33.76bn to $39.16bn (+16.0%) [C]. This describes those 24 sponsors only and is not a market growth rate.

---

## 5. Limitations
- **The universe is DAFRC's.** About 400–540 small non-DAFRC filers a year, and SDG Impact Fund in FY2021–22, are excluded (full-universe report §4). Shares are of the corrected DAFRC market.
- **The ranking is by EIN, not by sponsor family.** Affiliates appear separately: GS DAPF, Ayco and the Goldman Sachs Charitable Gift Fund; Dechomai Asset Trust and Dechomai Foundation; NPT and NPT CAT. See P-B44N30-02.
- **Imputation remains in a few rows.** In FY2024, 48 asset rows ($593.5m) are still imputed (batch 37 P-99F-01). In the top 50 only one metric is (UCLA Foundation FY2024 grants). The batch-37 Highland Park filed value ($44,864) is not applied, because the governing corrected totals predate it. The effect is immaterial.
- **FY2025 is filed and uncorrected**, from a partial index. FY2025 ranks are ranks among filers, and its shares are shares of the covered total.
- **R5 sponsor attribution inherits batch-34 assumptions.** These are the tier weights, the caps and the whitelist [I], plus the gap from attachment-only Schedule I filers (RCF and BofA CGF, about $0.16–0.32bn a year of unseen netting).
- **Fiscal years mix period ends.** Fidelity, NPT, DAFgiving360 and Vanguard close in June, while most community foundations close in December. A "year" is not a common 12-month window (DAFRC convention).
- **HHI is computed on EIN-level shares, on a 0–10,000 scale.** Antitrust thresholds apply to defined product and geographic markets, so they are a reference only [I].

---

## 6. Data dictionary

### `daf-sponsor-league-table-fy2021-2025.csv` (267 rows)
| Column | Meaning |
|---|---|
| fiscal_year | FY (calendar year in which the tax period ends) |
| row_type | `top50`; `exit` (prior-year top-50 member not in the top 50 this FY); FY2025: `fy2025_filed_fy2024_top50`, `fy2025_not_yet_filed`, `fy2025_filed_above_fy2024_cutoff` |
| rank_assets | Rank by EOY DAF assets in this FY (FY2025: among filers only) |
| ein, name, type, subtype | Sponsor. Name and type are DAFRC's latest row, or the corrections file for R4-only EINs |
| daf_assets_eoy, daf_contributions, daf_grants, daf_accounts_eoy | Corrected values (FY2021–24) or filed values (FY2025). Blank means no value |
| share_* | Value ÷ market total (FY2021–24) or ÷ covered filed total (FY2025), per `share_basis` |
| share_basis | `corrected_market_total_R1_R4` or `fy2025_filed_covered_total_only` |
| rank_contributions, rank_grants | Same sponsor's rank on the flows |
| prev_rank_assets, rank_change, assets_growth_yoy | Against the prior FY (FY2025 against corrected FY2024) |
| churn_status | `stayed`, `entrant`, `exit`, `filed_fy2025`, `not_yet_filed`, `provisional_entrant` |
| churn_reason_class, churn_reason | `termination`, `merger`, `late_filer_r4`, `new_to_panel`, `rank_drift`, `not_yet_filed`, `provisional`, `filed`; text with the cited repo source for documented events |
| daf_grants_netted_central, share_daf_grants_netted_central | Corrected grants − outbound R5 (central); share of the netted market |
| daf_contributions_netted_central | Corrected contributions − inbound R5 (central) |
| r5_outbound_central, r5_inbound_central | R5 central amounts attributed to the sponsor as grantor and as recipient |
| corrections_applied | R1–R4 rules applied to this sponsor-year |
| imputed_kept_metrics | Metrics still DAFRC-imputed after correction |
| fy2025_tax_period_end, fy2025_return_object_id, fy2025_flags | FY2025 return evidence; `accounts_implausible_avg_lt_5usd` when the count screen blanked the accounts |
| value_basis, source | `corrected_R1_R4` or `filed_fy2025_uncorrected`; input files |

### `daf-concentration-fy2021-2025.csv` (44 rows)
| Column | Meaning |
|---|---|
| fiscal_year, metric | FY; `daf_assets_eoy`, `daf_contributions`, `daf_grants`, `daf_accounts_eoy` |
| basis | `gross_corrected`; `netted_r5_lower`, `netted_r5_central` or `netted_r5_upper` (grants and contributions, FY2021–24); `fy2025_filed_covered_only` |
| market_total | Corrected total, netted total, or positive covered FY2025 sum |
| sum_values, n_sponsors_positive | Sum of sponsor values and the number of sponsors with a positive value |
| cr1, cr3, cr5, cr10, cr50 | Concentration ratios (fractions) |
| hhi | Σ(100 × share)², 0–10,000 |
| top1_ein, top1_name, source | Largest sponsor; inputs |

### `queue-proposals-batch44-n30.csv`
- Format per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- **P-B44N30-01:** complete FY2025 once the remaining TY2025 returns are indexed, after an FY2025 correction pass (depends on P-B35A-03).
- **P-B44N30-02:** a parent-group league table with an SDG Impact Fund sensitivity.

## 7. Reproduction
```
python3 scripts/mission_league_table.py --np-cache NPCACHE   # NPCACHE holds netpayout990/ (mission_net_payout.py)
python3 scripts/mission_league_table.py                      # without the cache: gross tables only, no sponsor-level R5
```
- The script prints a JSON summary covering:
  - the corrected-totals rebuild check (20 cells);
  - the R5 rebuild check (12 cells);
  - churn counts;
  - FY2025 coverage;
  - the top 10 by year.
- Every figure in §0–4 comes from that summary or from the two CSVs. It runs in about 2 seconds.
