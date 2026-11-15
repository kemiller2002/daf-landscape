# Queue batch 35 A: panel screens (workplace DAF reclassification, public-support cliff, 2026 TEOS harvest fill, Fidelity/Vanguard FY2025 counterpart lines)

**Date:** 2026-11-15 · **Agent:** batch35 A · **Queue items:** P-B34B-01, P-B34B-02, P-B34A-01, P-STF-02 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs**
- [`data/mission-2026-11-14/daf-reclassification-screen.csv`](../../data/mission-2026-11-14/daf-reclassification-screen.csv): 8 flagged sponsor-year pairs (P-B34B-01).
- [`data/mission-2026-11-14/public-support-cliff-screen.csv`](../../data/mission-2026-11-14/public-support-cliff-screen.csv): 553 returns of 123 few-account / large-balance DAF sponsors, FY2021–25 (P-B34B-02).
- [`data/mission-2026-11-14/form990-harvest-2026-fill.csv`](../../data/mission-2026-11-14/form990-harvest-2026-fill.csv): the 144 `http_404` harvest rows, all filled from the IRS 2026 TEOS zips (P-B34A-01). The harvest file itself is unchanged.
- [`data/mission-2026-11-14/daf-to-daf-fy2025-counterparts.csv`](../../data/mission-2026-11-14/daf-to-daf-fy2025-counterparts.csv): 1,433 grantor × recipient rows, Fidelity Charitable FY2025 and Vanguard Charitable FY2025 Schedule I lines to DAFRC panel EINs (P-STF-02).
- [`data/mission-2026-11-14/queue-proposals-batch35a.csv`](../../data/mission-2026-11-14/queue-proposals-batch35a.csv): P-B35A-01 to P-B35A-03.
- **Script** (stdlib, functional style): [`scripts/mission_batch35_screens.py`](../../scripts/mission_batch35_screens.py). It promotes the batch-34 TEOS range reader into the repo (central directory → member byte range → `unzip -p` for Deflate64) and reuses `mission_990_contractors.extract_stream` / `return_row` unchanged.

**Conventions**
- FY = calendar year in which the tax period ends (DAFRC convention). **Recency:** everything is FY2021 or later.
- **Labels:** **[F]** filed value read from the XML; **[C]** script computation; **[I]** inference; **[U]** not found.
- **Governing corrections read first:** wave 19 (end of [queue-batch34-pass-through-channels.md](queue-batch34-pass-through-channels.md)). Item 2 applies here: PPGF's and NFG's filed FY2024 values already replace DAFRC imputations in the corrected totals (rule R1), so nothing below re-adjusts them. Items 1, 3 and 4 do not touch this batch.
- No logins, forms or contact. **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B34B-01** reclassification screen | **AOGF is the only sponsor in the screened filings that moved accounts out of the Schedule D DAF column.** All filed FY2021–26 returns of 128 sponsors (every sponsor with ≥500 DAFs in any year, plus the eight named intermediaries, GS DAPF and Ayco), and the series of every other panel sponsor, were screened [C].<br>- AOGF FYE 2026-03: DAF accounts 710,352 → 695; other-funds accounts 1 → 751,746, with $935.7m of grants in that column [F].<br>- Six other sharp count drops with stable grants are count-basis changes, with no column shift (Give Back Foundation 36,917 → 7,686; Goodstack US 7,268 → 3; Endaoment 6,000 → 1,213; and three small sponsors). Ayco's drop to 0 is its merger into GS DAPF.<br>- **No TY2025 return for PPGF, NFG, Givinga, Bright Funds or CAF America (FYE 2026-04) is in index_2026 yet** (Last-Modified 2026-10-21). BBGF CY2025 still reports its grants in the DAF column ($536.4m) [F].<br>**Market effect [C]:**<br>- Applying AOGF's FYE 2026 basis to FY2024 removes 719,850 accounts: **−21.8% of corrected FY2024 accounts** (3,309,483 → 2,589,633). It removes only $0.78bn of grants (−1.2%; $66.44bn → $65.66bn).<br>- **Three micro-account processors hold 76.2% of corrected FY2024 accounts:** Givinga 1,421,011 (with only $12.4m of grants), AOGF 720,545 and PPGF 380,644. Without them the market has 787,283 accounts. | High on filed values; medium on scope (TY2025 returns for most intermediaries are not yet filed) |
| **P-B34B-02** public-support cliff | **Only two sponsors in the screen show a failed public-support test.**<br>- **Jasper Ridge** (CY2022 13.15%; later a 990-PF) reproduces as the control [F].<br>- **Community Foundation of South Lake County**, FY9/2025: **30.04%** after 49.7%, 41.0%, 35.8% and 31.7% in FY2021–24. It ticked the Schedule A **private-foundation box** (`PrivateFoundation170Ind`), with no prior-year or facts-and-circumstances box; 50 DAFs [F]. The 2026-11 EO BMF still shows foundation code 15.<br>17 of the 123 screened sponsors fall below 33⅓% in at least one year. Most pass on the 10% facts-and-circumstances test: Pew, Warren County CF, the Archdiocese of Milwaukee foundation, Salem, Fuller, Weld and others.<br>**At risk (passed on the prior-year test only):**<br>- Community Foundations Inc: 46.4% → 25.6%, FY2021–24;<br>- Los Altos Community Foundation: 76.1% → 26.0%, FY6/2025;<br>- National Charitable Fund Inc: 14.1% in CY2023, DAFs = 99% of assets. It recovered to 29.4% in CY2024 on facts and circumstances. | High on filed values; [I] on risk |
| **P-B34A-01** harvest fill | **All 144 rows filled; every member was in `2026_TEOS_XML_05B.zip`** (index label "05A") [F].<br>- FY2025 sponsors parsed in the full harvest: **755 → 899** [C].<br>- The filled returns hold $33.79bn of DAF EOY value, $5.13bn of grants and $7.96bn of contributions. Vanguard is $27.01bn of the EOY value.<br>- Exceptions: 3 returns report negative DAF grants (UCLA Foundation −$109.8m and two small ones), 1 has no Schedule D (Christalis) and 1 is amended (India Home). Ayco reports 0 DAFs (final return). | High |
| **P-STF-02** Fidelity / Vanguard FY2025 | **Fidelity FY2025: $3.46bn to 927 panel EINs**. $2.23bn of it goes to whitelist-included sponsors and $1.24bn to excluded ones (universities and the like).<br>**Vanguard FY2025 (now parsed from the TEOS zip): $585.9m to 506 panel EINs**, of which $428.2m goes to included sponsors.<br>**Fidelity → Vanguard $480.1m against Vanguard → Fidelity $87.3m: net $392.8m to Vanguard** [F/C].<br>- Vanguard's own FY2025 return cannot itemise the inflow (Schedule B is redacted). Its DAF contributions were flat: $5,751.4m against $5,746.9m in FY2024. The Fidelity line equals 8.3% of them [C].<br>- BofA CGF and RCF Schedule I attachments are still not machine-readable (batch 34 §3, unchanged). | High on lines; [I] on composition |

---

## 1. Data and method (all items)

- **Inputs:**
  - DAFRC panel (`dafrc-sponsor-schedule-d-fy2019-2024.csv`);
  - the full harvest (`form990-returns-schedule-d-harvest-full.csv`, FY2022–25);
  - corrected market totals (`dafrc-corrected-market-totals.csv`);
  - IRS TEOS indexes 2021–2026 (index_2026 Last-Modified 2026-10-21);
  - the `netpayout990/` caches of `mission_net_payout.py` (Fidelity FY2025, Vanguard FY2025);
  - `daf-to-daf-flows-990.csv` and `daf-to-daf-recipient-whitelist.csv`.
- **New XML extract (`extract_ext`):**
  - header;
  - Part I grants, revenue and contributions, and Part X total assets;
  - **Schedule A**: Part II lines 14–15 (`PublicSupportCY170Pct`, `PublicSupportPY170Pct`), Part III equivalents, the support totals, and every ticked indicator;
  - **Schedule D Part I, both columns** (DAFs, and funds and other accounts: count, contributions, grants, EOY value).
  - For flagged reclassification pairs, a full parse also keeps Schedule O passages mentioning DAFs, micro-donations or workplace giving.
  - Extracts are cached as JSON, not raw XML.
- **Return choice:** every 990 submission for an EIN and tax period ending FY2021–26 is fetched, and the one with the latest `ReturnTs` is kept.
  - Object IDs are not chronological across batches. Givinga's CY2024 amendment 202503179349301975 sorts below its original 202522379349301497, and the original has a blank Schedule D count.
  - The repo helper `latest_per_period` (max object id) would have kept the original.
- **Retrieval:**
  - 1,142 submissions: 1,116 from the GivingTuesday mirror, and 26 from TEOS zips after a mirror 404.
  - The 144 fill rows come straight from the zips.
  - All extracts parsed (`ok`).
- **Series priority** for the reclassification screen: filed XML (this batch) > harvest (filed) > fill > DAFRC (flagged when imputed).

## 2. P-B34B-01: workplace pass-through reclassification

### 2.1 Screen
- **Universe:**
  - **U1, full filed series (128 sponsors):** every panel sponsor with ≥500 DAF accounts in any FY2021+ year, plus AOGF, CAF America, PPGF, BBGF, NFG, Bright Funds, Givinga, Goodstack US, GS DAPF and Ayco.
  - **All other panel sponsors** are screened on the DAFRC and harvest series.
- **Flag** (consecutive FYs), either of:
  - **(a) sharp drop with stable grants:** prior DAFs ≥100, current ≤50% of prior, and DAF grants at 0.5–2.0× prior;
  - **(b) column shift:** prior DAFs ≥100, current ≤75% of prior, and other-funds accounts up by ≥50% of the DAF drop.
- **Classes:** `reclassified_to_other_funds_column` (b); `terminated_or_merged` (0 DAFs and $0 at year end); `artifact_*` (imputed or mixed-source values; none occurred); otherwise `count_basis_change_no_column_shift`.
- **Threshold check:** a first run with (b) at any drop size flagged 14 community foundations whose DAF count moved by 1–85 accounts. These are routine drift, so (b) requires a ≥25% drop. AOGF is the only sponsor that passes it.

### 2.2 Results [F/C]

| Sponsor | FY pair | DAF accounts | DAF grants | Other-funds accounts | Class | Reading |
|---|---|---|---|---|---|---|
| **AOGF (Benevity)** | 2025 → 2026 | 710,352 → **695** | $2,124.1m → $1,390.0m | 1 → **751,746** ($935.7m grants) | reclassified | Schedule O now says AOGF is a sponsor "only with respect to its donor-advised funds"; micro-donors recommend grants "without ongoing advisory privileges" |
| Give Back Foundation | 2023 → 2024 | 36,917 → 7,686 | $49.7m → $50.2m | 1 → 1 | count basis | EOY ($14.5m → $14.2m) and contributions flat; no Schedule O note [I: recount of donor accounts] |
| Percent Impact Fdn (Goodstack US) | 2024 → 2025 | 7,268 → 3 | $1.2m → $1.7m | blank | count basis | Batch 34 B noted the same switch |
| Endaoment | 2024 → 2025 | 6,000 → 1,213 | $34.8m → $18.7m | blank | count basis | The 6,000 was a round figure. 1,213 matches batch 31 |
| Jewish Federation of Greater Atlanta (58-1021791) | 2021 → 2022 | 4,932 → 521 | $35.1m → $31.9m | blank → 232 | count basis | The shift (232) is under 50% of the drop |
| Community Fdn for Northeast Georgia (58-1557995) | 2022 → 2023 | 1,246 → 187 | $10.4m → $11.9m | 75 → 125 | count basis | — |
| Idaho Women's Charitable Fdn | 2022 → 2023 | 206 → 34 | $0.43m → $0.36m | — | count basis | harvest values |
| Ayco Charitable Foundation | 2024 → 2025 | 5,585 → 0 | $300.9m → $452.6m | 0 | terminated/merged | Final return; merged into GS DAPF 2025-07-01 |

**Named intermediaries, latest filed return [F]:**
- AOGF FYE 2026-03: see the table above.
- CAF America FYE 2025-04: 740 DAFs, $947.4m grants; other funds 235 accounts, $45.8m.
- PPGF CY2024: 380,644 DAFs, $795.7m.
- BBGF CY2025: DAF count blank, $536.4m grants, other funds blank. The Part III note says CSRconnect employee gifts "should not be treated" as DAF contributions (batch 34 B), but Schedule D has not followed yet.
- NFG CY2024: 1 DAF, $199.8m.
- Givinga CY2024 (amended): 1,421,011 DAFs, $12.4m grants.
- Goodstack US CY2025: 3 DAFs, $1.66m.
- Bright Funds: no Schedule D values in any year.
- **No CY2025 return** for PPGF, NFG, Givinga or Bright Funds is indexed, and CAF America's FYE 2026-04 return is not either.

### 2.3 Effect on market totals [C]

| Measure | Value |
|---|---|
| Corrected DAF accounts, FY2024 (`dafrc-corrected-market-totals.csv`) | 3,309,483 |
| AOGF FY2024 accounts (FYE 2024-03) less its FYE 2026 DAF-column count | −719,850 → **2,589,633 (−21.8%)** |
| AOGF FY2024 grants × FYE 2026 other-funds share of grants (40.2%) | −$0.78bn → **$65.66bn (−1.2%)** of $66.44bn corrected grants |
| Givinga + AOGF + PPGF FY2024 accounts | 2,522,200 = **76.2%** of corrected accounts |
| Accounts excluding those three | 787,283 |
| DAFRC FY2024 "Donation Processor" subtype, as published | 22 sponsors; 2.85m accounts (86% of corrected accounts); $4.24bn grants (6.4% of grants) |

- **Reading [I]:**
  - Market **account** totals are dominated by three processors' micro-accounts, and they swing with those processors' reporting choices. Givinga alone went from 42,307 (CY2021) to 1,543,203 (CY2022), 955,569 (CY2023) and 1,421,011 (CY2024).
  - Market **grants** are barely affected: the reclassification moves about 1% of grants.
  - Per-account averages and account growth rates built on DAFRC counts should exclude the processors, or state that they include them (P-B35A-01).
- The FY2026 AOGF figure is not in the corrected totals, which end at FY2024. The restatement applies AOGF's new basis backwards as a scenario; it is not a filed figure.

## 3. P-B34B-02: public-support cliff screen

### 3.1 Universe and fields
- **Universe:**
  - Sponsors with, in any FY2021+ year, **<50 DAFs and ≥$10m of DAF EOY value, or >$10m average per DAF**;
  - Jasper Ridge, added as a control;
  - Result: **123 sponsors and 553 returns (FY2021–25)**.
  - The queue's broader "<50 DAFs" alone would cover about 990 sponsors, mostly small ones, so this pass keeps the large-balance subset.
- **Fields:** Schedule A Part II line 14 (current-year public-support %) and line 15 (prior year); Part III percentages for 509(a)(2) filers; ticked boxes:
  - `ThirtyThrPctSuprtTests{CY,PY}170Ind` (lines 16a/b);
  - `TenPctFactsCrcmstncsTest{CY,PY}Ind` (17a/b);
  - `PrivateFoundation170Ind` (line 18);
  - `First5Years*`.
- **Coverage:** 462 returns carry a percentage. Of the rest, 77 are 509(a)(3) supporting organisations (no support test) and some are school/college or first-five-year filers.

### 3.2 Sponsors below 33⅓% in at least one year [F]

| Sponsor (EIN) | Subtype | Public support % CY, by FY | Latest DAFs / DAF EOY / DAF share of assets | How it qualified |
|---|---|---|---|---|
| **Jasper Ridge Charitable Fund** (47-2088631) | National | 21: 45.2 · **22: 13.15** | 0 / $0 (2022) | Prior-year test only; then 990-PF for 2023 (index tax period 202312) |
| **Community Fdn of South Lake County** (59-3343026) | Community | 49.7 · 41.0 · 35.8 · 31.7 · **25: 30.04** | 50 DAFs (FY9/2025) | 2024 prior-year only; **2025 private-foundation box ticked** |
| **Community Foundations Inc** (31-1197385) | Community | 46.4 · 42.9 · 34.1 · **24: 25.6** | 19 / $23.1m / 0.30 | Prior-year only in FY2024 |
| **Los Altos Community Foundation** (77-0273721) | Community | 66.0 · 69.4 · 72.9 · 76.1 · **25: 26.0** | 49 / $26.2m / 0.41 | Prior-year only. Total support $117.1m, of which $83.4m is excess over the 2% cap (one or a few very large gifts) |
| **National Charitable Fund Inc** (65-0462974) | Other | **23: 14.1** · 24: 29.4 | 30 / $17.7m / **0.99** | 2023 prior-year only; 2024 facts and circumstances |
| Shallow Ford Foundation (04-3795285) | Community | **21: 10.3** · 37.0 · 38.6 · 41.3 · 45.0 | 17 / $14.5m / 0.72 | 2021 facts and circumstances; recovered |
| Georgia Community Foundation (58-1960821) | Community | **21: 15.8** · 46.2 · 49.3 · 41.6 | 12 / $20.0m / 0.77 | 2021 facts and circumstances; recovered |
| Walker Area CF (63-1154984) | Community | **13.4 · 14.0** · 26.6 · 43.2 · 56.3 | 25–28 / $67m / 0.52–0.59 | Facts and circumstances; recovered |
| The Salem Foundation (93-6018523) | Community | 29.9 · 19.6 · 19.2 · 32.3 · **14.6** | 18 / $12.3m / 0.33 | Facts and circumstances |
| Legacy Foundation (35-1872803) | Community | 31.5 · 30.9 · 35.7 · 26.9 | 46 / $15.0m / 0.12 | Facts and circumstances / prior year |
| Weld Community Foundation (84-1315296) | Community | 36.5 · 30.6 · 32.0 · 32.7 · 33.5 | 36 / $18.8m / 0.28 | Facts and circumstances / prior year |
| Community Fdn of Warren County (25-1380549) | Community | 27.3 · 27.0 · 26.1 · 27.0 · 27.4 | 48 / $16.8m / 0.14 | Facts and circumstances every year |
| Sturgis Area CF (38-3649922) | Community | 29.6 · 30.9 · 41.9 · 57.8 · 58.9 | 16 / $14.3m / 0.37 | Facts and circumstances; recovered |
| Archdiocese of Milwaukee Catholic Community Fdn (39-2005163) | Religious | 30.8 · 27.4 · 21.4 · 17.5 · 38.7 | 20 / $12.5m / 0.07 | Facts and circumstances / prior year |
| The Fuller Foundation (95-4124436) | Religious | 24.5 · 25.5 · 27.1 · 28.8 | 39 / $8.7m / 0.04 | Facts and circumstances |
| The Pew Charitable Trusts (56-2307147) | Other | 18.7 · 17.1 · 18.8 · 18.3 · 19.1 | 2 / $90.6m / 0.06 | Facts and circumstances |
| Health First Fdn–Northern Arizona (81-3137336) | Univ./health | 39.5 · 30.0 · 28.6 · 33.1 | 1 DAF | Facts and circumstances / prior year |

- **Near the line or falling fast** (≥10 points in a year, still above 33⅓%), DAF-heavy:
  - The Sterling Donor Advised Fund: 78.4% → 64.9% (FY2024; DAF share 0.97, 36 DAFs, $54.0m);
  - YHB Charitable Endowment: 100% → 54.0% (FY2023; 1.00);
  - VertuAssets Foundation: 93.6% → 61.7% (FY2023; 0.96);
  - Philanthropic Ventures Foundation: 94.0% → 82.8% (FY2024; 0.62);
  - Spur Community Foundation: 84.8% → 64.9% (FY2024; 0.88);
  - Hendricks County CF: 52.4% → 39.8% → 34.9% (FY2024–25);
  - Community Foundation of the Quincy Area (37-1366611): 46.3% → 36.5% (FY2025; 0.66).
- **Reading [I]:**
  - The Jasper Ridge pattern is a large sponsor holding few accounts whose public support comes from a few gifts that age out of the five-year window. It is rare in the 2021+ filings.
  - Most small sponsors below 33⅓% are community foundations with small DAF shares. They qualify on the 10% facts-and-circumstances test, which a single-family, adviser-run sponsor would find harder to meet.
  - The live cases are South Lake County (failed in FY2025), Community Foundations Inc and Los Altos (next return decides), and National Charitable Fund Inc (DAF-only, recovered on facts and circumstances).
  - South Lake County's DAF EOY value is blank on its FY2025 return, so its DAF balance is unknown.
- **EO BMF check** (local copy of the IRS EO BMF, downloaded 2026-11-14; `grep` by EIN): South Lake County, Community Foundations Inc, Los Altos and National Charitable Fund are all still foundation code 15 (170(b)(1)(A)(vi)) [F]. A failed test changes status for the following year, so the BMF can lag (P-B35A-02).

## 4. P-B34A-01: 2026 TEOS fill

- **Rows:** the 144 rows have `xml_status=http_404` and are FY2025 returns submitted in 2026: 7 national, 47 community foundation and 90 single-issue.
  - Tax periods: 105 June 2025, 38 December 2025, 1 September 2025.
  - The index labels all 144 "2026_TEOS_XML_05A".
- **Retrieval:** the script reads the central directories of `2026_TEOS_XML_05A.zip` and `05B.zip` (both Last-Modified 2026-06-17), then range-reads each member. **All 144 are in 05B** [F].
  - Each member is parsed with the unchanged `mission_990_contractors.extract_stream`, and rows are built with `return_row`, so the harvest columns match.
  - The fill adds Schedule D other-funds columns, Schedule A current-year support % and provenance.
- **Results [C]:**
  - 143 of 144 have Schedule D.
  - Sums: DAF EOY $33.79bn (national $27.15bn, CF $3.34bn, single-issue $3.30bn), grants $5.13bn, contributions $7.96bn.
  - 40 returns report other-funds accounts ($160.6m of other-funds grants).
  - Sponsors with a parsed FY2025 return in the full harvest rise from **755 to 899**.
- **Flags:**
  - UCLA Foundation: −$109.8m DAF grants (suspect Part I, as batch 34 found);
  - Your Community Foundation of North Central WV (−$176,914) and Northern Kentucky University Foundation (−$12,500): also negative;
  - Christalis Inc: no Schedule D;
  - India Home Inc: amended return;
  - Ayco: 0 DAFs.
- **Ayco and R2 (queue text):**
  - Ayco's final FY6/2025 return reports $452.6m of DAF grants and $408.1m of contributions, and sends $1,162.2m to GS DAPF on Schedule I.
  - Its Schedule O says GS DAF accounted for the merger as "a change in reporting entity… Prior period amounts are presented as if the merger had occurred at the beginning of 2024" [F].
  - GS DAPF's CY2025 return is not yet indexed. Its latest parsed return is CY2024: 4,134 DAFs, $5.83bn contributions, $3.07bn grants, $12.64bn EOY.
  - An FY2025 R2 adjustment therefore cannot be computed yet. The risk is that GS DAPF's CY2025 Schedule D repeats Ayco's January–June 2025 flows (P-B35A-03).

## 5. P-STF-02: Fidelity and Vanguard FY2025 counterpart lines

- **Lines:**
  - Fidelity FY2025 (FYE 6/2025; [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml)): 89,891 Schedule I lines, $15.07bn [F].
  - Vanguard FY2025 (FYE 6/2025; TEOS 05B member 202621329349306657): 27,221 lines, $3.43bn [F].
  - Lines to DAFRC panel EINs come from the `netpayout990/` caches and are aggregated per recipient. Each recipient gets its batch-34 whitelist decision and its own FY2025 (or FY2026) filed Schedule D contributions.

| Grantor | Panel recipients | Total | Whitelist include | Exclude | Not in whitelist |
|---|---|---|---|---|---|
| Fidelity Charitable | 927 | $3,462.8m | $2,225.4m | $1,235.4m | $2.0m |
| Vanguard Charitable | 506 | $585.9m | $428.2m | $157.7m | $0.01m |

**Largest sponsor-to-sponsor lines, with counterparts [F/C]:**

| Grantor → recipient | Amount | Reverse flow, FY2025 | Recipient FY2025 DAF contributions | Line share of them |
|---|---|---|---|---|
| Fidelity → Vanguard | $480.1m | Vanguard → Fidelity $87.3m | $5,751.4m | 8.3% |
| Fidelity → NPT | $346.8m | NPT → Fidelity $284.9m | $15,153.7m | 2.3% |
| Fidelity → ImpactAssets | $203.7m | — | CY2025 not filed | — |
| Fidelity → GS DAPF | $159.9m | — | CY2025 not filed | — |
| Fidelity → SVCF | $147.5m | — | CY2025 not filed | — |
| Fidelity → DAFgiving360 | $117.8m | DAFgiving360 → Fidelity $976.6m | $11,100.1m | 1.1% |
| Fidelity → AOGF | $99.4m | — | $2,052.9m (FYE 3/2025) | 4.8% |
| Vanguard → RCF | $85.1m | — | CY2025 not filed | — |
| Vanguard → National Charitable Endowment | $50.0m | — | not filed | — |
| Vanguard → DAFgiving360 | $46.3m | DAFgiving360 → Vanguard $8.7m | $11,100.1m | 0.4% |
| Vanguard → NPT | $31.6m | NPT → Vanguard $3.4m | $15,153.7m | 0.2% |

- **Does Vanguard's return show the $480.1m inflow?** Not separately.
  - Schedule B is redacted, and Schedule D gives one contributions total.
  - Vanguard's FY2025 DAF contributions ($5,751.4m) equal FY2024's ($5,746.9m) almost to the dollar. FY2024 had already jumped from $2,359.7m in FY2023.
  - [I] If the Fidelity line is one or a few account transfers, Vanguard's other contributions fell by about the same amount. This needs the audited statements or Vanguard's annual report.
- **Excluded recipients:** the largest Fidelity lines to excluded recipients are universities: Johns Hopkins $340.3m, Harvard $113.8m, Brown $60.1m, MIT $49.8m, Stanford $48.2m, Dartmouth $43.8m. They exceed those universities' own Schedule D DAF contributions many times over (e.g. JHU $85,521), which confirms they are programme grants, not DAF transfers (rule W1).
- **BofA CGF and RCF:** their Schedule I lines are still a single "see attached" row, and the ProPublica PDF images still return a security check (batch 34 §3). Not retried in this batch.

## 6. Limitations
- **Index cut-off.** index_2026 is Last-Modified 2026-10-21, so most TY2025 returns of calendar-year intermediaries (PPGF, NFG, Givinga, Bright Funds, BBGF follow-up) and CAF America FYE 2026-04 are not yet available. The reclassification screen is complete only to that date.
- **Thresholds are judgement:** 50% count drop, 0.5–2× grants and a ≥25% drop for column shifts. A sponsor that reclassified gradually, or that also lost grants, would be missed.
- **U1 covers ≥500-account sponsors.** Smaller sponsors rely on DAFRC and the harvest, without the other-funds column.
- **Support screen scope:** large-balance, few-account sponsors only (123). The full "<50 DAFs" universe (~990 sponsors) was not screened. 509(a)(3) supporting organisations have no support test and are listed without a percentage.
- **The facts-and-circumstances test** cannot be judged from the XML. Only the box is read.
- **South Lake County's DAF value** is blank on its FY2025 return. Its box reading rests on one filing.
- **Counterpart contributions** are totals. No return itemises which contributions came from another sponsor.
- **The restated account totals** are scenarios (AOGF's FYE 2026 basis applied to FY2024), not filed values.

## 7. Source register

| ID | Source | Accessed | Used in |
|---|---|---|---|
| S1 | IRS TEOS indexes [index_2021–2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) (2026 Last-Modified 2026-10-21) | local cache, 2026-11-15 | all |
| S2 | IRS e-file XML via the GivingTuesday mirror `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml` (1,116 submissions) | 2026-11-15 | §2–3 |
| S3 | [2026_TEOS_XML_05A.zip](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05A.zip) and [05B.zip](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip) (Last-Modified 2026-06-17), range reads; 144 fill members and 26 screen members | 2026-11-15 | §2–4 |
| S4 | AOGF FYE 2026-03 [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642259349301349_public.xml); FYE 2025-03 amended [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202641969349302754_public.xml) | 2026-11-15 | §2 |
| S5 | Givinga CY2024 amended [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml) | 2026-11-15 | §2.3 |
| S6 | Community Fdn of South Lake County FY9/2025 [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202641629349301714_public.xml); Los Altos CF FY6/2025 [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202630589349300128_public.xml); National Charitable Fund CY2023 [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501349349300915_public.xml) and CY2024 [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202620339349301107_public.xml); Jasper Ridge CY2022 [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202313149349304316_public.xml) | 2026-11-15 | §3 |
| S7 | IRS EO BMF extract (eo1–eo4.csv), local copy dated 2026-11-14 | 2026-11-15 | §3.2 |
| S8 | Repo: `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `dafrc-corrected-market-totals.csv`, `dafrc-corrections-itemized.csv`, `daf-to-daf-flows-990.csv`, `daf-to-daf-recipient-whitelist.csv`; `netpayout990/` caches (Fidelity 202601389349301700, Vanguard 202621329349306657) | repo | §2–5 |

## 8. Data dictionary

### `daf-reclassification-screen.csv` (one row per flagged sponsor × consecutive FY pair)

| Column | Meaning |
|---|---|
| ein, sponsor_name, dafrc_type, dafrc_subtype, named_pass_through | Identity; named_pass_through is the P-B34B-01 label if the sponsor is one of the eight named intermediaries |
| fy_prev, fy_cur | FY pair |
| source_prev, source_cur | `filed_xml` (this batch), `harvest_filed`, or `dafrc:<source>` |
| object_id_prev, object_id_cur, source_url_cur | Returns used |
| daf_count_*, daf_grants_*, daf_contributions_*, daf_eoy_* | Schedule D Part I column (a), prev/cur |
| daf_count_drop, daf_count_ratio, daf_grants_ratio | Drop and ratios |
| other_count_*, other_grants_*, other_count_shift | Schedule D Part I column (b) "funds and other accounts"; shift = cur − prev |
| combined_grants_ratio | (DAF + other) grants cur ÷ prev, when column (b) is known |
| flag_sharp_drop_stable_grants, flag_column_shift | Screen flags (§2.1) |
| imputed_value_involved, mixed_sources | Artifact checks |
| classification | §2.1 classes |
| sched_o_daf_text_prev/cur | Schedule O passages matching DAF / micro-donation / workplace wording (truncated) |

### `public-support-cliff-screen.csv` (one row per screened sponsor × FY return)

| Column | Meaning |
|---|---|
| ein, sponsor_name, dafrc_type, dafrc_subtype, dafrc_operating_status_latest | Identity (DAFRC) |
| fiscal_year, tax_period_end, object_id, xml_status, amended_ind, xml_url | Return |
| daf_count, daf_eoy, daf_grants, daf_contributions, avg_eoy_per_daf | Schedule D Part I DAF column |
| total_assets_eoy, daf_share_of_total_assets | Part X line 16 EOY; DAF EOY ÷ total assets |
| sched_a_present, support_basis | Schedule A filed; public-charity basis from the ticked Part I box |
| public_support_cy_pct, public_support_py_pct | Part II lines 14/15 (or Part III lines 15/16 for 509(a)(2)), as a fraction |
| public_support_total_170, total_support_170, substantial_contributors_excess | Part II lines 6 (public support), 11 (total support), 5 (amounts over the 2% limit) |
| investment_income_cy_pct_509 | Part III line 17 |
| sched_a_indicators | All ticked Schedule A boxes (element names) |
| flags | `below_33_cy`, `near_33_cy` (33⅓–40%), `drop_10pts` (PY − CY ≥ 0.10), `passed_on_prior_year_only`, `facts_circumstances`, `pf_status_ind`, `first_5_years` |
| later_990pf_tax_periods | Tax periods of any later 990-PF by the same EIN in index 2021–2026 |

### `form990-harvest-2026-fill.csv` (one row per filled harvest row)
- **Harvest columns:** identical to `form990-returns-schedule-d-harvest-full.csv`.
  - `xml_status` = `ok_teos_zip`.
  - `xml_url` = `<zip URL>#<member>`.
- **Added columns:**

| Column | Meaning |
|---|---|
| harvest_xml_status_before | `http_404` |
| teos_zip_url, teos_member, teos_compressed_bytes, xml_bytes | Provenance |
| sched_d_other_funds_count/contributions/grants/eoy_value | Schedule D Part I column (b) |
| public_support_cy_pct | Schedule A current-year % |
| fill_note | Exceptions (negative grants, 0 DAFs, no Schedule D, amended) |

### `daf-to-daf-fy2025-counterparts.csv` (one row per grantor × panel recipient EIN)

| Column | Meaning |
|---|---|
| grantor, grantor_ein, grantor_object_id, grantor_tax_period_end | Fidelity or Vanguard FY2025 return |
| recipient_ein, recipient_name, recipient_dafrc_type/subtype | Panel recipient |
| whitelist_decision, whitelist_rule | From `daf-to-daf-recipient-whitelist.csv` (`not_in_whitelist` if absent) |
| lines, amount_usd, cash_usd, noncash_usd, largest_line_usd, match_methods, purpose_sample | Schedule I Part II lines (EIN or unique-name match) |
| recipient_filed_fy, recipient_daf_contributions_filed_fy, recipient_source, line_share_of_recipient_daf_contributions | Recipient's own FY2025 (else FY2026) Schedule D contributions |
| reverse_lines_fy2025_usd | Recipient → grantor FY2025–26 lines, from `daf-to-daf-flows-990.csv` or the other grantor in this file |

### `queue-proposals-batch35a.csv`
- Format per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- IDs: P-B35A-01 (account-metric restatement and TY2025 intermediary returns), P-B35A-02 (support-test watchlist) and P-B35A-03 (Ayco/GS DAPF FY2025 R2).

## 9. Reproduction
```
python3 scripts/mission_batch35_screens.py --irs-dir IRS --work-dir WORK \
    --np-cache NPCACHE1/netpayout990 --np-cache NPCACHE2/netpayout990 --fetch
```
- IRS holds index_2021.csv–index_2026.csv. WORK receives `ext/` (JSON extracts), `teos/` (zip members) and `zipcd/` (zip central directories).
- The script prints a JSON summary; every figure in §0–5 comes from it or from the four CSVs.
- The §3.2 BMF check is a `grep` of the four EINs in the local EO BMF files (FOUNDATION column). Full names of DAFRC-truncated sponsors (Jewish Federation of Greater Atlanta, Community Foundation for Northeast Georgia, Community Foundation of the Quincy Area, Your Community Foundation of North Central WV) are from the same BMF files.
