# Queue batch 33 A: panel-wide 990 scans — blank Schedule D Part I (P-B32B-01), sweepstakes receipts in DAF totals (P-B32A-01), low line-3 investment income (P-B32A-03), DAF-to-DAF flows among the top 50 (P-B29C-02 / P-99F-06)

**Date:** 2026-11-15 · **Queue items:** P-B32B-01, P-B32A-01, P-B32A-03, P-B29C-02, P-99F-06 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs**
- [`data/mission-2026-11-14/blank-schedule-d-panel.csv`](../../data/mission-2026-11-14/blank-schedule-d-panel.csv): 185 returns (113 DAFRC sponsors) that answer Part IV line 6 "Yes" but leave the Schedule D Part I DAF count and value blank, TY2021 onward.
- [`data/mission-2026-11-14/sweepstakes-receipts-dafrc-share.csv`](../../data/mission-2026-11-14/sweepstakes-receipts-dafrc-share.csv): 12 sponsor-years (Givinga, Pledgeling, CAF America, Our Change). This file was not in the brief; it holds the P-B32A-01 arithmetic.
- [`data/mission-2026-11-14/low-investment-income-screen.csv`](../../data/mission-2026-11-14/low-investment-income-screen.csv): 467 flagged returns (247 sponsors) out of 4,910 screened.
- [`data/mission-2026-11-14/daf-to-daf-flows-top50.csv`](../../data/mission-2026-11-14/daf-to-daf-flows-top50.csv): 11,872 grantor→recipient edges, FY2023–FY2024, with reverse flows and pair net flows.
- [`data/mission-2026-11-14/queue-proposals-batch33a.csv`](../../data/mission-2026-11-14/queue-proposals-batch33a.csv): P-B33A-01 to P-B33A-03.
- **Scripts** (stdlib, functional style):
  - [`scripts/mission_panel_scans.py`](../../scripts/mission_panel_scans.py), with tasks `blank_sd`, `sweepstakes` and `lowinc`;
  - [`scripts/mission_daf_to_daf.py`](../../scripts/mission_daf_to_daf.py).

**Method and rules**
- **Sources.** No new parsing logic was written, and no logins, forms or contact were involved. The scripts transform caches of IRS e-file XML (GivingTuesday mirror of IRS TEOS) that earlier repo scripts built, plus repo CSVs:
  - `extract990/` (12,257 returns) from `mission_990_contractors.py`;
  - `netpayout990/` (Schedule I lines whose recipient EIN is in the DAFRC panel, FY2021–24) from `mission_net_payout.py`;
  - `extract990inv/` from `mission_infund_costs.fetch_inv`. This cache was extended from 13 to all 5,272 `sponsor-cost-structure.csv` returns (5,272 OK, 0 errors). Only Part VIII line 3 needed new fetching; the extractor is unchanged.
- **Conventions.**
  - Fiscal year (FY) is the calendar year in which the tax period ends, the DAFRC convention.
  - **Recency:** P-B32B-01 is restricted to filed TaxYr ≥ 2021. The other three items use FY2022–25 (cost-structure set) and FY2023–24 (Schedule I), so they are all TY2021 or later.
  - Pre-2021 values are used only to bracket a blank (a sponsor's last reported value).
- **Labels:** **[F]** filed value; **[C]** script computation; **[I]** inference; **[U]** not found.
- **Governing corrections applied:**
  - **Wave 17**, [queue-batch32-infund-costs.md](queue-batch32-infund-costs.md) items 4–7 and 10. MS GIFT's line-3 gap is *larger than the whole fee ceiling*, so a low line 3 is treated as an anomaly consistent with, but not proof of, fee netting. Income classified into gains is the competing explanation, and §3 tests it explicitly.
  - **Wave 17**, [queue-batch32-filing-reconciliations.md](queue-batch32-filing-reconciliations.md) item 1. It does not touch §3 (tier B) used here.
  - **Wave 15:** the original CY2024 Givinga return carried no Part I values.
  - **Wave 14**, [queue-batch29-complaints-voids.md](queue-batch29-complaints-voids.md) item 6. ImpactAssets' CY2024 return has a second, $10,000 NPT line, which is included below.
- **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B32B-01** Line 6 "Yes", Part I blank | **185 returns from 113 DAFRC sponsors** (3.5% of the 5,255 panel returns answering line 6 "Yes", TY2021+) [C].<br><br>**How DAFRC treats them:**<br>- **Imputed:** 78 returns from 62 sponsors. DAFRC fills them with imputed values, **$1.60bn summed over FY2021–24** ($0.49bn, $0.69bn, $0.22bn and $0.20bn).<br>- **Dropped as closed:** 77 returns from 31 sponsors. DAFRC has no row because it flags them "Assume Sponsor Closed". Carrying their last filed DAF assets forward, **the potentially missing assets are $41m, $78m, $172m and $151m in FY2021–24** (0.046–0.067% of DAFRC assets in FY2023–24; $183m across the 31 sponsors, counted once each).<br><br>**Later returns:**<br>- **33 sponsors report values again later.** Among the 31 dropped sponsors, only Helping Hands did ($5.5m, FY2023).<br>- Another 28 FY2025 returns fall outside DAFRC's window. They include Christian Community Foundation, last value $212.7m.<br><br>**Exit-rate bounds net of gaps, by mechanical re-test of the 100 exit candidates:**<br>- Central: 1.20% → **0.91%/yr**.<br>- Upper: 1.48% → **0.99%/yr**.<br>- Also removing gap-then-"No" cases: 0.80% and 0.89%. | High on counts [F/C]; carry-forward is an [I] proxy |
| **P-B32A-01** Sweepstakes and auction receipts in DAF totals | **Yes, they are inside DAFRC contributions.** All four sponsors are DAFRC panel members, and their Schedule D contributions equal DAFRC's (source "IRS 990").<br><br>**Gross line-2b receipts attributable to DAFs (pro rata to the Schedule D share of contributions):**<br>- FY2022: $91.5m (upper $133.0m), **0.12% (0.17%)** of DAFRC market contributions;<br>- FY2023: $70.7m, **0.11%**;<br>- FY2024: $41.3m, **0.05%**.<br><br>**Retained by the agents** (never reaching any charity): $71.0m, $42.8m and $20.5m (0.09%, 0.07%, 0.02%).<br>**Out of window:** Our Change's FY2025 $14.7m is outside DAFRC's window.<br>**Pledgeling's "accounts":** its 20,270–23,006 accounts match its own Part III text, "pass-through grants to approximately 23,000 [20,000] organizations". So they look like per-beneficiary records, not donor DAFs [I]. They are 0.5–0.7% of market accounts. | High on amounts [F/C]; account reading [I] |
| **P-B32A-03** Line 3 under 50 bps of average assets | **467 returns from 247 sponsors** (of 4,910 with average assets of at least $1m). The panel median is 164–237 bps.<br><br>**DAF-heavy hits:** 47 returns from 27 sponsors (DAF assets at least $10m and at least 50% of total assets).<br><br>**What the other lines say:**<br>- **13** have a normal total return (≥ 300 bps), so income probably sits in gains or pooled-unit values: MS GIFT, FFTC, Foundation for the Charlotte Jewish Community, Endaoment FY2024 and others.<br>- **12** have no gain lines at all: cash processors such as PayPal, AOGF, Givers Legacy and Venn.<br>- **18** are down-year returns (FY2022 or non-cash write-downs at Dechomai) and cannot be read.<br>- **4** have low yield and low total return.<br><br>**MS GIFT is the only broker or bank captive under 50 bps.** The next-lowest large captive is GS Charitable Gift Fund at 67 bps (FY2022); Bessemer is at 94–159. **No other broker captive shares the pattern.** Schedule D Part XII line 4a is filled in 7 of the 47 DAF-heavy hits. | High on the screen [F/C]; no hit is evidence of fee netting by itself [I] |
| **P-B29C-02 / P-99F-06** DAF-to-DAF flows | **Size:**<br>- **Top 50 → top 50 (DAF-holding recipients): $3.39bn in FY2023 and $6.03bn in FY2024**, equal to 6.2% and 9.3% of DAFRC market grants.<br>- **All panel grantors → DAF-holding recipients: $5.24bn and $9.56bn**, equal to 9.6% and 14.8% of grants and 8.0% and 10.6% of contributions, double-counted on both sides.<br><br>**Netting:** among the 436 top-50 pairs where both returns are itemised, gross flows of $8.45bn net to $4.31bn (51%). 212 of the pairs run both ways.<br><br>**Largest pairs:**<br>- SVCF → NPT $1.60bn against NPT → SVCF $0.62bn;<br>- Fidelity ↔ NPT $348m / $306m;<br>- Fidelity ↔ DAFgiving360 $284m / $249m;<br>- GS DAPF → NPT $437m;<br>- **Vanguard → ImpactAssets $335m** ($308.3m in FY2024);<br>- ImpactAssets → NPT $162.5m against NPT → ImpactAssets $24.5m.<br><br>**Net receivers over FY2023–24:** NPT +$1.89bn, ImpactAssets +$0.38bn.<br>**Net senders:** SVCF −$1.21bn, Vanguard −$0.39bn, GS DAPF −$0.33bn, AEF −$0.29bn. | High on filed lines [F]; that a line is DAF money is [I] |

---

## 1. P-B32B-01: line 6 "Yes" with Schedule D Part I blank

### 1.1 Method
- **Input.** `extract990/` holds 12,112 returns with XML OK. After keeping one return per (EIN, period), with the highest object id winning, 10,314 are TY2021+. 1,588 of the 1,594 DAFRC panel EINs appear.
- **Flag.** Part IV `DonorAdvisedFundInd` ∈ {true, 1} AND `DonorAdvisedFundsHeldCnt` and `DonorAdvisedFundsVlEOYAmt` both absent.
- **`blank_kind`:**
  - `part_i_daf_column_blank` (162 returns, 101 sponsors);
  - `other_funds_column_only` (13, 7): values sit only in the "funds and other accounts" column;
  - `count_and_value_blank_flows_reported` (10, 8): contributions or grants are filed, but not the count or value.
- **Matching to DAFRC.** Each flagged return is matched to the DAFRC row for the same FY and given a `dafrc_treatment`. It is then bracketed by the sponsor's last and next return carrying a value, and by DAFRC's last non-imputed value.
- **`est_missing_assets_carry_forward`.** The last reported DAF value, counted only where DAFRC has no row or a blank value. It is a proxy [I]; real balances may have moved.

### 1.2 Results [F/C]

| FY | Flagged returns (sponsors) | DAFRC imputed: returns, imputed $ | DAFRC "closed", no row: sponsors, carry-forward $ | Share of DAFRC FY assets (closed) |
|---|---|---|---|---|
| 2021 | 20 | 14, $492.3m | 6, $41.3m | 0.018% |
| 2022 | 38 | 22, $686.8m | 15, $78.4m | 0.034% |
| 2023 | 40 | 11, $222.0m | 29, $171.8m | 0.067% |
| 2024 | 59 | 31, $201.2m | 27, $151.1m | 0.046% |
| 2025 | 28 | outside window | outside window (last values $363.3m) | — |

**Other rows:**
- **Givinga FY2024:** DAFRC uses a "paper submission" value of $1.95m. The e-filed return is blank, which fits wave 15.
- **El Triunfo Conservation Foundation FY2022:** DAFRC row present, value blank.

**Largest imputed blanks:**
- Community Foundation of Middle Tennessee: FY2021–22 imputed $333m and $365m. Last filed $270m (FY2019); next filed $396m (FY2023).
- Christian Community Foundation: FY2022–23 imputed $181m and $195m. Filed $212.7m in FY2024; blank again in FY2025.
- Walker Area CF: FY2021 and FY2024 imputed $76m and $80m.
- Amalgamated Charitable Foundation: FY2021–22.
- TOP Jewish Foundation, Endaoment (FY2023) and CF of Northern Illinois.

In all 29 imputed rows that have a filed value on both sides, the imputed value lies within ±10% of the range between the bracketing filed values (Endaoment FY2023 is $17.8m against $15.3m and $17.1m), so DAFRC's treatment of this group looks reasonable [C/I].

**Sponsors dropped as closed while still answering "Yes":** 31 sponsors. The largest last values are:
- Truman Heartland CF $19.0m;
- CF of Snohomish County $18.4m (it answered "No" in FY2024);
- Jewish CF (EIN 470874376) $16.6m;
- Give2Asia $15.7m;
- Tompkins $13.5m;
- Kern $13.0m;
- Helping Hands $10.1m;
- Piqua $8.2m.

**Values reappearing:** 33 sponsors (44 returns) later file a value. The latest such values sum to $878.8m, mostly CFMT and Christian CF.

**Outside DAFRC:** 1,104 non-panel EINs filed 2,401 TY2021+ returns with line 6 "Yes" and Part I blank. This is the `flag_yes_but_no_sched_d_daf_data` population already in `non-dafrc-daf-filers-summary.csv`, and it is not re-sized here.

### 1.3 Exit-rate bounds net of reporting gaps [C]

**Method.**
- `exit_retest` re-reads every later return of the 100 candidates in `sponsor-exit-verification.csv`. The exposure base is 5,746 sponsor-years.
- **Gap rule:** a candidate counts as a non-exit when either
  - every later return has line 6 "Yes" with the DAF value blank; or
  - a later "Yes" return files a positive DAF value.
- **Ambiguous:** blank "Yes" years followed by "No".
- A zero-value closing return is not a gap.

| Treatment | Exits | Rate/yr |
|---|---|---|
| Central, original (A + B) | 69 | 1.20% |
| Central net of gaps (17 B removed) | 52 | **0.91%** |
| …also net of ambiguous (6 B) | 46 | 0.80% |
| Upper, original (A + B + C) | 85 | 1.48% |
| Upper net of gaps (17 B, 11 C removed) | 57 | **0.99%** |
| …also net of ambiguous | 51 | 0.89% |

**Agreement with batch 32's manual tier-B coding:**
- The mechanical rule picks up all 13 manual `reporting_gap_still_reports_dafs` cases, plus:
  - Gorge (its FY2025 return comes from the 05B zip and is not in this cache);
  - Marietta and CF of Dickinson County, which manual coding called reclassified and which report only the other-funds column;
  - CF of Morgan County, which manual coding called gap-then-"No". No "No" return is in the cache.
- **Manual non-exits the mechanical rule cannot see:** Goldstein (amended to "No") and Arctic Slope. That is why manual coding gives 51 (0.89%) where the rule gives 52 (0.91%).
- **Tier C (unresolved):** 10 now look like reporting gaps:
  - Truman Heartland, Jewish CF 470874376, Give2Asia, Piqua, Jewish Federation of Western … (EIN 042127023), Heartland Charitable Trust, Legacy Endowment, Rome, Durham-Chapel Hill and SharedImpact;
  - plus Helping Hands, whose values reappear.
- Exits reclassified as gaps held **$163m** of exit-reference DAF assets.
- **Asset-weighted rates** are not recomputed. Removing $163m against $765bn at risk changes the asset-weighted bound by less than 0.03 points.

---

## 2. P-B32A-01: sweepstakes and auction gross receipts in DAF totals

**Method.**
- `sweepstakes` joins `schedule-g-screen.csv` (P-COST-05; all screened years with line-2b gross > 0 for the four EINs) to the DAFRC panel and to `dafrc-corrected-market-totals.csv`.
- **Central estimate:** line-2b gross × (Schedule D DAF contributions ÷ Part I total contributions, capped at 1).
- **Upper estimate:** min(gross, DAF contributions).
- **Market denominator:** the DAFRC dataset sum as published.

| FY | Sponsor-years | DAF-attributable gross, central (upper) | Share of DAFRC contributions | Agent-retained, central | Share |
|---|---|---|---|---|---|
| 2022 | CAF America $64.2m (upper $105.6m); Givinga $25.2m; Our Change $1.2m; Pledgeling $0.9m | $91.5m ($133.0m) | 0.120% (0.174%) | $71.0m | 0.093% |
| 2023 | CAF America $25.7m; Givinga $7.4m; Our Change $1.1m; Pledgeling $36.6m | $70.7m ($76.6m) | 0.108% (0.117%) | $42.8m | 0.066% |
| 2024 | CAF America $0.8m; Our Change $1.7m; Pledgeling $38.9m | $41.3m ($41.4m) | 0.046% | $20.5m | 0.023% |
| 2025 | Our Change $14.7m | outside DAFRC window | — | — | — |

**Reading [I]:**
1. **The receipts are in the totals.** DAFRC contributions equal the filed Schedule D values for every sponsor-year, so the gross receipts are inside market contributions.
2. **The correction is small:** 0.05–0.17% of contributions. The agent-retained part (CAF America's Omaze, Givinga's Golden Hearts Games, Pledgeling's Charitybuzz and Prizeo) is about half to three-quarters of it.
3. **Accounts matter more than dollars:**
   - Givinga's 1.54m and 0.96m accounts are 47% and 32% of DAFRC market accounts (FY2022–23). This is already flagged in the repo.
   - Pledgeling's 20–23k accounts are 0.5–0.7% of market accounts, at $155–232 of assets per account.
   - Its Part III narrative counts pass-through grantee organisations in exactly that range: "approximately 23,000" in the TY2023 return and "approximately 20,000" in TY2024 ([TY2023 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202422769349300502_public.xml), [TY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542539349301674_public.xml)) [F].
   - The account count therefore most likely counts beneficiary funds, one per grantee organisation, not donor-advised accounts [I].
4. **CAF America's correction is the uncertain one.** Omaze receipts may have been booked to the non-DAF "funds" side; its DAF share of contributions was 61% in FY2022. Hence the gap between the central $64.2m and the upper $105.6m.
5. **Not covered:**
   - Givinga FY2024: no line-2b row in the screen; DAFRC uses a paper-submission value.
   - All FY2021 returns: the cost-structure set starts at FY2022.

---

## 3. P-B32A-03: Part VIII line 3 under 50 bps of average total assets

**Method.**
- `lowinc` takes line 3 (`InvestmentIncomeGrp/TotalRevenueColumnAmt`) over the mean of beginning and end-of-year total assets for every cost-structure return.
- **Hit kinds** (only where average assets are at least $1m):
  - `line3_under_50bps` (380);
  - `line3_negative` (28);
  - `line3_blank` (59).
- **Context recorded for each hit:** line 7d, Part XI line 5, a total-return proxy (line 3 + 7d + XI 5), 11f, fee-like line-24 items, and Schedule D Part XI/XII line 4a.
- **`context_pattern`:**
  - `no_gain_lines…`: 7d and XI 5 are both empty;
  - `normal_total_return…`: proxy ≥ 300 bps;
  - `down_year_ambiguous`: proxy < 0;
  - otherwise `low_yield_and_low_total_return`.
- **Focus group:** DAF assets ≥ $10m and DAF share of total assets ≥ 50%.

**Results [F/C]:**
- **Panel median line-3 yield:** 164, 214, 237 and 236 bps (FY2022–25).
- **All 467 hits by pattern:**
  - 99 normal total return;
  - 149 down year;
  - 112 low yield and low return;
  - 107 no gain lines.
- **Hits by category:** single-issue other 167, university/health 89, religious 84, community 75, processors 28, national standard 24.

| Pattern (focus group, 47 returns / 27 sponsors) | Returns | Sponsors (examples) |
|---|---|---|
| Normal total return; income probably in gains or pooled units | 13 | MS GIFT (4.2 bps FY2024, 35.2 FY2023; proxy 864 and 1,218); FFTC (32.6 and 33.8 bps; proxy 1,605 and 1,676); Foundation for the Charlotte Jewish Community (23–26 bps; proxy 1,044–1,406); Endaoment FY2024; NPT Charitable Asset Trust FY2022; VertuAssets; Legacy Global; West Bend CF; Jewish Federation of Greater Indianapolis; Schumacher |
| Down year | 18 | MS GIFT FY2022, FFTC FY2022, CJP Boston FY2022, Dechomai FY2023–24 (non-cash write-downs), Servant FY2023, United Charitable, Cornell University Foundation, Aspen CF |
| No gain lines (cash, processor, non-investing) | 12 | PayPal Charitable Giving Fund (0 bps), AOGF FY2022, Givers Legacy, Give Back, Venn (all 4 years), Endaoment FY2022–23 (line 3 blank), Foundation for Advanced … |
| Low yield, low total return | 4 | Crewe Endowment, Educational Endowment Fund, United Charitable FY2024 |

**Broker and bank captives** (national sponsors with average assets ≥ $500m, lowest line-3 yields):
- MS GIFT: 4.2, 13.7 and 35.2 bps;
- Dechomai: 11.6–12.0 bps (a non-cash processor);
- Servant: 12.1 bps;
- GS Charitable Gift Fund: 66.6 bps (FY2022);
- Rockefeller Philanthropy Advisors: 67.0 bps;
- Bessemer: 93.7 bps.

Every other broker or bank captive is at 131–641 bps in every year: Fidelity, Vanguard, GS DAPF, BofA, Raymond James, Stifel, T. Rowe, BNY Mellon, Comerica, USCGT, AEF, RCF and NPT.

**Schedule D Part XII line 4a** (investment expenses netted in the audit) is reported in only 7 of the 47 focus hits: United Charitable ×2, Cornell, CF of North …, Aspen, and Jewish Federation of Greater Indianapolis ×2. None is a broker captive.

**Reading [I]:**
- **MS GIFT stays an outlier among broker captives.** No other wealth or broker captive shares the pattern, so the screen gives no sign of a sector-wide fee-netting practice visible on line 3.
- **The closest analogues are not fee cases.** FFTC and the Charlotte Jewish foundation have normal total returns, which points to pooled-unit or partnership accounting that reports income inside gains. Applying wave 17, that is also the likeliest main cause at MS GIFT; fee netting cannot be told apart from it with filings alone.
- **Not done:** donor circulars and fee terms for the hits were **not** read. Only filed XML was used. P-B33A-03 proposes the audit check.

---

## 4. P-B29C-02 / P-99F-06: DAF-to-DAF flows

**Method.**
- `mission_daf_to_daf.py` ranks DAFRC EINs by FY2024 end-of-year DAF assets and takes the top 50:
  - 22 community foundations;
  - 18 national;
  - 1 processor (Dechomai);
  - 7 DAF-heavy single-issue sponsors (NCF, Jewish Communal Fund, CJP, Donors Trust, Thrivent, Jewish Community Federation of San Francisco and Jewish Community Foundation of Los Angeles);
  - 2 universities (Board of Trustees of the Leland Stanford Junior University and the UCLA Foundation).
- For each, it reads the chosen FY2023 and FY2024 return from `netpayout990/`. All 100 grantor-years are present.
- **Not itemised:** Schedule I points to an attachment at BofA CGF and RCF (both years), and at Greater Horizons and GKCCF (FY2023).
- **Edges** are summed Schedule I lines from a top-50 grantor to any DAFRC panel EIN; self-lines are dropped.
- **`daf_primary_recipient`:** the recipient is national, a processor or a community foundation, or is a non-university top-50 sponsor.
- **Pair statistics** count only top-50 pairs where neither side is a university and both returns are itemised in that FY. Flows excluded for coverage were $472m (FY2023) and $468m (FY2024).

**Totals [F/C]:**

| Flow | FY2023 | FY2024 |
|---|---|---|
| Top 50 → any panel EIN, all segments | $8.44bn | $11.61bn |
| …of which to university/hospital sponsors (mostly programme grants) | $3.15bn | $2.78bn |
| Top 50 → DAF-holding panel recipients | $4.55bn | $7.90bn |
| Top 50 → top 50, DAF-holding | **$3.39bn** (6.2% of DAFRC grants) | **$6.03bn** (9.3%) |
| All panel grantors (1,552 / 1,545 returns) → DAF-holding recipients | **$5.24bn** (9.6% of grants; 8.0% of contributions) | **$9.56bn** (14.8%; 10.6%) |
| DAFRC dataset grants / contributions | $54.77bn / $65.36bn | $64.60bn / $90.57bn |

**Largest pairs, FY2023 + FY2024, A→B / B→A:**

| Pair | A→B | B→A | Net |
|---|---|---|---|
| SVCF ↔ NPT | $1,598.5m | $623.4m | $975.1m to NPT |
| Fidelity ↔ NPT | $348.2m | $305.8m | $42.5m to NPT |
| Fidelity ↔ DAFgiving360 | $284.2m | $248.6m | $35.7m to DAFgiving360 |
| NPT ↔ GS DAPF | $24.3m | $437.3m | $413.0m to NPT |
| NPT ↔ DAFgiving360 | $148.9m | $263.8m | $115.0m to NPT |
| Vanguard ↔ ImpactAssets | $335.2m | $1.5m | $333.7m to ImpactAssets |
| Fidelity ↔ SVCF | $44.7m | $205.6m | $160.9m to Fidelity |
| Fidelity ↔ MS GIFT | $49.9m | $149.8m | $99.8m to Fidelity |
| NPT ↔ ImpactAssets | $24.5m | $162.5m | $138.0m to NPT |
| NPT ↔ AEF | $22.3m | $161.1m | $138.8m to NPT |

- **Single filed lines behind the largest flows [F]:**
  - SVCF CY2024 → NPT: $1,591,322,838, "General Nonprofit Support" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349305759_public.xml)). Already noted in `queue-net-payout-fidelity-outliers.md`.
  - NPT → SVCF: $257.1m (FY2023) and $366.4m (FY2024) ([FY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml)).
  - Vanguard FY2024 → ImpactAssets: $308,265,198 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511349349313096_public.xml)); $26,966,904 in FY2023.
- **Netting [C]:**
  - 436 covered pairs; 212 run both ways.
  - Gross $8.45bn over two years nets to $4.31bn. In two-way pairs, $8.07bn nets to $3.93bn.
- **Net positions over FY2023–24 [C]:**
  - Receivers: NPT +$1,892m, ImpactAssets +$377m, Dechomai +$98m (Donors Trust → Dechomai $100.7m), NCF +$90m, JCF +$62m, Fidelity +$54m.
  - Senders: SVCF −$1,211m, Vanguard −$392m, GS DAPF −$332m, AEF −$286m, Servant −$116m, CCT −$78m, MS GIFT −$59m, Donors Trust −$57m.

**Reading [I]:**
1. **Inter-sponsor flows are large relative to the market,** about 10–15% of DAFRC grants on the panel-wide DAF-holding measure. Half of the gross top-50 flow cancels in pairs, so gross-only readings overstate migration.
2. **ImpactAssets is a net receiver.** Vanguard's $308m FY2024 line to ImpactAssets is larger than the $160.8m ImpactAssets → NPT line that prompted P-WAT-02. That fits two-way donor-recommended movement rather than a program migration away from ImpactAssets (batch 29 §4).
3. **NPT is the system's main net receiver.** Its inflows come from SVCF, GS DAPF, AEF, DAFgiving360 and ImpactAssets.
4. **Netting P-99F-06 out of aggregate contributions and grants** would reduce both by up to $5.2bn (FY2023) and $9.6bn (FY2024) if every line to a DAF-holding sponsor is DAF money. Some lines fund a community foundation's own or designated funds, so this is an upper bound. Lines to universities and other single-issue charities are excluded from it.

---

## 5. Limitations
- **Cache coverage.** `extract990/` misses returns that the mirror does not hold, e.g. IRS 05B-zip members such as Gorge FY2025. Its pre-2021 coverage is partial, which is why DAFRC's last filed value backs up the bracket.
- **Blank rule.** Part I blank means both the count and value tags are absent. Returns with a count but no value are not flagged in §1.2, but they count as "value blank" in the §1.3 exit re-test.
- **Carry-forward** assumes balances stayed at the last filed level. It is an indicator, not a measurement.
- **Exit re-test.** It cannot see amendments to "No" (Goldstein) or DAF-labelled grants under "No" (Arctic Slope), so it complements manual coding rather than replacing it.
- **Line-3 screen.**
  - Average assets are whole-organisation figures; community foundations hold non-DAF endowments.
  - Line 3 omits partnership and K-1 income reported elsewhere.
  - The context patterns are heuristics.
  - Fee terms in circulars were not read.
- **Schedule I.**
  - It lists only grants above $5,000 (per the form instructions). Non-itemising sponsors (BofA, RCF) are invisible as grantors.
  - A recipient-side match by EIN does not prove the money went into a DAF.
  - Name matching was used for 1 edge.
  - FY2025 is not in the cache (NPT FY2025 → ImpactAssets $40.6m is therefore outside the window).
- **Market denominators** are DAFRC dataset sums as published (imputations included).

## 6. Source register

| ID | Source | Accessed | Used in |
|---|---|---|---|
| S1 | IRS e-file XML, GivingTuesday mirror `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`; object ids in each CSV | 2026-11-15 (inv extracts); earlier caches | All |
| S2 | [DAFRC Annual DAF Report 2025 – Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx), via `dafrc-sponsor-schedule-d-fy2019-2024.csv` | repo | §1, §2, §4 |
| S3 | Repo: `schedule-g-screen.csv`, `dafrc-corrected-market-totals.csv`, `sponsor-exit-verification.csv`, `tier-b-daf-exit-reasons.csv`, `sponsor-cost-structure.csv` | repo | §1–3 |
| S4 | Repo reports: queue-batch32-filing-reconciliations.md §3, queue-batch32-infund-costs.md §3–4 (wave-17 corrections), queue-batch29-complaints-voids.md §4 (wave-14 corrections), queue-net-payout-fidelity-outliers.md | repo | context |

## 7. Data dictionary

### `blank-schedule-d-panel.csv` (one row per flagged return; DAFRC panel EINs; TY2021+)

| Column | Meaning |
|---|---|
| ein, sponsor_name, dafrc_type, dafrc_subtype, dafrc_last_operating_status | From the sponsor's latest DAFRC row |
| tax_year, fiscal_year, tax_period_end | Filed TaxYr; FY = year the period ends |
| line6_raw | Part IV line 6 as filed (true or 1) |
| blank_kind | `part_i_daf_column_blank` / `other_funds_column_only` / `count_and_value_blank_flows_reported` / `no_schedule_d` |
| daf_contributions_filed, daf_grants_filed, other_funds_count, other_funds_eoy_value, total_assets_eoy | Values that were filed |
| dafrc_treatment | `dafrc_row_imputed` / `dafrc_row_filed_value` / `dafrc_row_value_blank` / `dafrc_no_row_sponsor_closed` / `dafrc_no_row_other` / `outside_dafrc_window_fy2025plus` |
| dafrc_eoy_daf_assets_same_fy, dafrc_accounts_same_fy, dafrc_source_same_fy | The DAFRC row for the same FY |
| prior_reported_period / _daf_count / _daf_eoy | Last earlier return in the cache with a count or value |
| dafrc_last_filed_fy_before, dafrc_last_filed_daf_assets_before | Last non-imputed DAFRC value before this FY |
| next_reported_period / _daf_count / _daf_eoy | First later return with a count or value |
| later_returns_line6 | Later returns as `YYYY-MM:` followed by Y or N (b = Part I blank, v = values present) |
| est_missing_assets_carry_forward | Last reported value, used only where DAFRC has no row or a blank value |
| amended_ind, return_ts, return_object_id, xml_url, source_url | Provenance |

### `sweepstakes-receipts-dafrc-share.csv`

| Column | Meaning |
|---|---|
| sg_gross_receipts, sg_retained_by_agent, sg_retained_share, sg_fundraisers | Schedule G Part I line 2b sums and names (from schedule-g-screen.csv) |
| total_contributions_part_i, sched_d_daf_contributions, daf_share_of_contributions | Part I line 8; Schedule D I-2; their ratio, capped at 1 |
| daf_gross_central_prorata, daf_gross_upper, daf_retained_central_prorata | Gross × share; min(gross, DAF contributions); retained × share |
| sched_d_daf_accounts, sched_d_daf_assets_eoy, assets_per_account, contributions_per_account | Schedule D Part I |
| dafrc_* , in_dafrc_totals | DAFRC same-FY row |
| market_contributions_published_dataset / _corrected, share_of_market_central / _upper | DAFRC market contributions and shares |
| market_accounts_published_dataset, share_of_market_accounts | DAFRC accounts and the sponsor's share |

### `low-investment-income-screen.csv` (hits only)

| Column | Meaning |
|---|---|
| hit_kind | `line3_under_50bps` / `line3_negative` / `line3_blank` (average assets ≥ $1m) |
| focus_daf_heavy | 1 if DAF assets ≥ $10m and DAF share of total assets ≥ 50% |
| sponsor_years_hit / _screened | The sponsor's hit years / years in the cost-structure set |
| l3_investment_income, l3_reported, avg_total_assets, l3_bps_of_avg_assets | Part VIII line 3; mean of beginning and end-of-year total assets |
| panel_median_l3_bps_same_fy | Median line-3 yield of screened returns in that FY |
| l7d_net_gain, xi5_unrealized, total_return_proxy_bps, total_return_normal_flag, context_pattern | Other investment lines and the §3 heuristics |
| l11f_invest_mgmt_fees, l11f_bps_of_avg_assets, l11g_other_fees, l24_fee_like_items | Part IX fee lines |
| sd_xii_4a_inv_exp_not_in_990, sd_xi_4a_inv_exp | Schedule D Part XII line 4a / Part XI line 4a |
| daf_assets_eoy, daf_accounts, daf_share_of_total_assets, category | From sponsor-cost-structure.csv |

### `daf-to-daf-flows-top50.csv` (one row per grantor × recipient × FY)

| Column | Meaning |
|---|---|
| grantor_ein, grantor_name, grantor_rank_fy2024, grantor_segment | Top-50 grantor (rank by DAFRC FY2024 DAF assets) |
| recipient_ein, recipient_name_filed, recipient_panel_name, recipient_type/_subtype/_segment | Recipient as filed and as classed by DAFRC |
| recipient_rank_fy2024, recipient_in_top50, daf_primary_recipient | See §4 |
| match_method | `ein` or `name` |
| schedule_i_lines, cash_usd, noncash_usd, amount_usd, largest_line_usd, purpose_text | Summed Schedule I lines |
| reverse_return_covered, reverse_amount_same_fy, net_amount_same_fy | Top-50 recipients only: B→A in the same FY and A→B minus B→A |
| pair_a_to_b_fy2023_2024, pair_b_to_a_fy2023_2024, pair_net_fy2023_2024 | Pair sums over both years |
| grantor_sched_i_total, grantor_sched_i_itemized, grantor_daf_grants_sched_d, share_of_grantor_daf_grants | Grantor-return context |
| return_object_id, xml_url, source | Provenance |

### `queue-proposals-batch33a.csv`
- Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- IDs are P-B33A-01..03.

## 8. Reproduction
```
python3 scripts/mission_panel_scans.py --task all --extract990-dir CACHE990/extract990 --inv-cache CACHE [--fetch]
python3 scripts/mission_daf_to_daf.py --np-cache NPCACHE        # NPCACHE holds netpayout990/
```
- `CACHE990/extract990` comes from `mission_990_contractors.py --cache-dir CACHE990`.
- `NPCACHE/netpayout990` comes from `mission_net_payout.py --cache-dir NPCACHE`.
- `CACHE/extract990inv` is filled by `--fetch`. That run streams each of the 5,272 returns only up to Schedule D.
- Both scripts print a JSON summary; every figure above comes from those summaries.
