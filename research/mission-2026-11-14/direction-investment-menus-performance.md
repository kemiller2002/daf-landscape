# Direction P-NEW-INV-01: investment menus and published pool performance at the top-20 DAF sponsors

**Date:** 2026-11-15 · **Queue item:** P-NEW-INV-01 (owner direction, batch42 N19) · **This is research, not investment advice.**

**Outputs:**
- [`data/mission-2026-11-14/sponsor-investment-menus-2026.csv`](../../data/mission-2026-11-14/sponsor-investment-menus-2026.csv): 20 rows, one per top-20 sponsor (FY2024 DAF-asset rank from `sponsor-terms-census-top20-2026.csv`).
- [`data/mission-2026-11-14/sponsor-pool-returns-2021-2025.csv`](../../data/mission-2026-11-14/sponsor-pool-returns-2021-2025.csv): 354 rows (R001–R354) of published pool and benchmark returns from 7 sponsors; 295 rows carry a computed pool-minus-benchmark difference.
- [`data/mission-2026-11-14/queue-proposals-batch42-n19.csv`](../../data/mission-2026-11-14/queue-proposals-batch42-n19.csv): P-B42N19-01 to -03.
- Scripts (stdlib): [`scripts/mission_pool_returns.py`](../../scripts/mission_pool_returns.py) builds the returns CSV from the fetched documents; [`scripts/mission_pool_returns_vc_parse.py`](../../scripts/mission_pool_returns_vc_parse.py) parses the Vanguard Charitable performance page.

**Method and rules.**
- **Sources:** sponsor-hosted performance PDFs and pages, program circulars, help-centre articles; repo rows reused where they already existed. No logins, forms or outreach.
- **robots.txt:** read before every host. Not fetched because robots.txt returned 403 or could not be read: dafgiving360.org, schwabcharitable.org, cct.org, raymondjames.com, rjcharitable.org (connection reset), morganstanley.com and gsdaf.org (unreadable this session; repo rows reused instead). jcfny.org allowed crawling but returned HTTP 403 to page fetches, so it was not pursued. Those sponsors carry [R] (search-index capture only) or [U].
- **Returns:** transcribed by script from the `pdftotext`/HTML text of each document. Differences are **pool minus stated benchmark, in percentage points, rounded to the inputs' precision**. Nothing was computed where either side is unpublished. No unpublished return was inferred.
- **Recency:** all sources 2021–2026. The one older document (Raymond James IAP guidelines, PDF created 2017-11-30) is recorded as context only.
- **Labels:** **[F]** first-party document; **[R]** search-engine capture, page not read; **[U]** not found; **[C]** my computation; **[I]** my inference.
- **Reused, not re-fetched:** `wealth-captive-terms-2026.csv` (GS DAF, MS GIFT, BofA terms), `infund-expense-nationals-2026.csv` (Fidelity pool assets and ERs N001–N030, CIAP fee N073–N077, ER ranges N061–N063), `daf-impact-pools-2026.csv` (IP01–IP20). Governing corrections applied: batch32 wave-17 (Fidelity all-in ≈50–52 bps; MS GIFT line-3 anomaly not proof of fee netting), batch30 wave-15, impact-matching wave-24A (ImpactAssets DAFRC row already replaced), and adviser-fees wave-11 (NPT $500k discretionary / $2m non-discretionary; Fidelity CIAP $100k minimum "varies by firm"; no sponsor publishes a numeric adviser-fee cap).

---

## 0. Answers in brief

| Question | Answer |
|---|---|
| **Who publishes pool returns against benchmarks?** | **6 of the top 20:** Fidelity, Vanguard Charitable, FFTC, GKCCF, Greater Horizons (identical figures to GKCCF) and CJP [F]. **NPT** publishes returns with **no benchmark** [F]. **NCF** publishes **benchmark-only pro forma** figures because its pools were relaunched on 2026-09-01 [F]. **DAFgiving360** has a quarterly performance report per search captures [R], but its host could not be fetched. **The other 11 publish no public pool returns**: SVCF and BofA only on request or in the portal, ImpactAssets only to account holders, and AEF, RCF, MS GIFT, GS DAF are adviser- or account-level programmes. CCT, JCF and Raymond James were not fetched. |
| **Time window** | Sponsors publish **trailing** windows, not 2021–2025 calendar years. Two sources fit the 2021–2025 window exactly: **FFTC pool sheets** (calendar years 2021–2025, 6 pools) and the **GKCCF summary as of 2025-12-31** (trailing 5 years = 2021–2025). The rest are as of 2026-06-30 to 2026-10-31, so a "5-year" figure covers roughly mid/late 2021 to 2026. |
| **Pool minus benchmark** [C] | **Index-tracking menus sit within about 0.1 pp:** Vanguard 5-year median −0.04 pp (16 options); GKCCF core pools and mixes 5-year median −0.09 pp (to 2025-12-31); FFTC Passive LTG −0.1 to −0.2 pp each calendar year 2021–2025.<br>**Fidelity pools trail by more:** 5-year median −0.65 pp on 20 conventional pools, and **−0.58 to −0.76 pp on all 7 asset-allocation pools**. Fidelity says pool results include its admin fee; the benchmarks are not fee-adjusted. A gap about the size of a 0.60% admin fee is consistent with that [I]; GKCCF, CJP, FFTC and NPT figures exclude the admin fee and Vanguard does not say (P-B42N19-03).<br>**Active and alternative options vary widely:** CJP JCEP +2.8 pp and the Diversified Fund +1.1 pp over 5 years, against the CJP Equity Fund −3.6 pp; Fidelity International Equity −5.15 pp. |
| **ESG and impact options** [C] | **Every sponsor that publishes them shows them trailing their stated benchmarks over 3–5 years:**<br>- **GKCCF** impact pools and mixes (Environmental, Broad ESG): 5-year median **−2.4 pp** (10 rows). The 5-year window includes pro forma history before 2022-09-30.<br>- **Fidelity:** sustainable and impact pools 5-year median **−1.2 pp** (5 pools; Environmental Impact Access −5.5 pp).<br>- **FFTC:** ESG Long-Term Growth −1.5 pp over 3 years.<br>- **Vanguard:** ESG index options trail by only −0.06 to −0.34 pp over 5 years. Global Positive Impact (active) trails by −9.31 pp over 1 year.<br>**Exception:** GKCCF's Social Impact pool and mixes lead by +0.1 to +1.0 pp over 1 year.<br>These are trailing windows dominated by 2022–2023; P-B42N19-02 asks for calendar-year rows. |
| **Menu size** | From **0 sponsor pools** (AEF, where every account is adviser-managed) and **3 pools** (SVCF) up to **25 pools** (Fidelity) and **36 options** (Vanguard). Community foundations offer 3–7 pools and/or risk mixes. NCF, Vanguard (Hamilton Lane Private Assets Fund, ER 3.38%), CJP (JCEP) and FFTC (Diversified LTG) now offer private or alternative sleeves. |
| **Adviser-managed (CIAP-style) minimums** | AEF $25,000 (mandatory adviser); GKCCF and Greater Horizons $100,000; Fidelity CIAP $100,000 (varies by firm); DAFgiving360 $100,000 [R]; FFTC $250,000 (alliance managers); NPT $500,000 discretionary / $2m non-discretionary; GS IMAP $5m (philanthropic advisor programme $3m); SVCF IMF $5m ($10m with alternatives); RCF has no stated minimum ("SMAs for accounts of all sizes"); Vanguard has none (no programme). |
| **Pool expense ratios** | **Index menus:** Vanguard index 0.01–0.11%; GKCCF mixes 0.04–0.14%; FFTC Passive LTG 0.20%; Fidelity index pools 0.015–0.035%.<br>**Active and multi-asset pools:** 0.33–0.67% (Fidelity), 0.50–0.55% (NCF), 0.54–1.13% (FFTC).<br>**Alternatives:** CJP JCEP 1.5%; NCF Alternative Investments Pool 1.5% plus 10% over a 7% hurdle; Vanguard Private Assets 3.38%.<br>**Weighted figure:** only Fidelity's is computable, at 26.3 bps (repo N027). |

---

## 1. Menus at the top 20 (summary of `sponsor-investment-menus-2026.csv`)

| # | Sponsor | Pools / options | ESG / impact | Adviser programme (minimum) | Pool ERs | Returns public? |
|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable | 25 in [performance summary](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/monthly-pool-performance-summary.pdf) (+ Impact Investing and Charitable Cash pools in the FY2025 audit) | 5 sustainable/impact pools + Impact Investing Pool | [CIAP](https://www.fidelitycharitable.org/giving-account/investment-options/charitable-investment-advisor-program.html) ($100k; varies) | 0.015–0.93% net | Yes, vs benchmark [F] |
| 2 | NPT | 7 model portfolios ([IDAP 0926](https://www.nptrust.org/investment-descriptions-and-performance-npt/)) | Broad Social Impact Portfolio | Segregated account ($500k / $2m) | 0.07–0.61% + 0.10–0.15% advisory | Yes, no benchmark [F] |
| 3 | DAFgiving360 | not verified | SRI pools [R] | Professionally managed ($100k) [R] | ~0.03–0.67% [R] | Report exists [R] |
| 4 | Vanguard Charitable | 36 ([performance page](https://www.vanguardcharitable.org/investments/investments-performance)) | 3 ESG index + Global Positive Impact | None | 0.01–3.38% | Yes, vs benchmark [F] |
| 5 | GS DAF | 4 objectives × 4 menus (circular, repo) | Passive ESG ETF option | IMAP ($5m); advisor programme ($3m) | 0.18–0.67% + advisory layers | No |
| 6 | SVCF | 3 ([page](https://www.svcf.org/donors/investment-options)) | ESG-aligned pools; impact investing via advising | IMF ($5m; $10m with alternatives) | not published | By email only |
| 7 | AEF | 0 (adviser-managed) ([FAQ](https://www.aefonline.org/advisors/)) | — | Mandatory ($25k fund minimum) | n/a | No |
| 8 | MS GIFT | Select UMA, Portfolio Management; Legacy Pools closed 2021-07-21 | MSISV; closed Impact pools | FA-run (advisory fee ≤ 1.00%) | Legacy 0.60–1.24% | No |
| 9 | RCF | pools for donor-directed DAFs (count not stated) ([page](https://renaissancecharitable.org/donor-directed-dafs/)) | none found | Advisor-managed SMAs, any size ([page](https://renaissancecharitable.org/advisor-managed-dafs/)) | not published | No |
| 10 | NCF | 4 core pools + Alternative Investments Pool + giver alternatives + SMA ([chart](https://site.ncfgiving.com/wp-content/uploads/2026/11/Investment-pools-comparison-chart.pdf)) | Faith-based screening | SMA (minimum not stated) | 0.50–0.55%; AIP 1.5% + carry | Benchmark only (new pools) [F] |
| 11 | BofA CGF | 8 objectives, active-sustainable or passive ([ml.com](https://www.ml.com/articles/the-bank-of-america-charitable-gift-fund.html)) | Active version is "sustainable" | — | est. 0.17–0.29% | Portal only |
| 12 | Chicago Community Trust | 2 pools + 1 for >$1m [R] | [R] | [U] | [U] | [R] Growth Pool factsheets |
| 13 | ImpactAssets | 4 menu types + client-recommended deals ([FAQ](https://impactassets.freshdesk.com/support/solutions/articles/62000232304-what-investment-options-are-available-through-the-impactassets-donor-advised-fund-)) | All impact | — | private funds 0.40% + manager fees | Account holders only |
| 14 | FFTC | 7 ([performance](https://www.fftc.org/sites/default/files/documents/FFTC_Performance_Report.pdf); [pool sheets](https://www.fftc.org/sites/default/files/documents/All_Pool_Sheets.pdf)) | ESG Long-Term Growth | Alliance managers ($250k); custom pools ($2m) | 0.10–1.13% | Yes, incl. calendar years [F] |
| 15 | Jewish Communal Fund | primary MM/short bond + pooled equity + pre-set portfolios [R] | [U] | Private client ($1m) [R] | [U] | [R] |
| 16 | GKCCF | 5 pools + 5 mixes; 3 impact pools + 12 impact mixes ([investing](https://growyourgiving.org/investing)) | Social, Environmental, Broad ESG | FA-managed ($100k) | mixes 0.04–0.14% | Yes, monthly [F] |
| 17 | Greater Horizons | same as GKCCF ([page](https://www.greaterhorizons.org/individual-family-giving/investment-options-performance/)) | same | FA-managed ($100k) | same | Yes (identical) [F] |
| 18 | Dechomai | no menu found ([home](https://dechomai.org/)) | [U] | [U] | [U] | No |
| 19 | CJP | 7 ([DAF report](https://www.cjp.org/hubfs/DAF_Report.pdf?hsLang=en)) | Sustainable Fund | none found ([policies](https://ma.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf)); JCEP $500k | 0.1–1.5% | Yes, vs benchmark [F] |
| 20 | Raymond James Charitable | [U] (hosts not fetched) | [U] | IAP ($500k in 2017; context only) | [U] | [U] |

**Notes on individual sponsors.**
- **Fidelity.** The 2026 summary lists "Sustainable U.S. Index Access", which is not among the 26 pools in the FY2025 audit. The Impact Investing Pool ($220.7m at 2025-06-30) is in the audit but has no row in the performance summary [C]. CIAP rules come from the repo (wave-11 corrected). The live CIAP page adds that CIAP balances are liquidated if a grant "cannot be funded with balances in the Fidelity Charitable investment pools" [F].
- **BofA.** The 2026 Merrill article says each objective comes as an "Actively managed sustainable portfolio" or a "Passive (all ETF) portfolio" [F]. This resolves the batch30 limit about the fee chart's "Sustainable" column header [I for the mapping].
- **NCF.** Redesigned pools went live on 2026-09-01. Actual pool performance "will be reported in the next quarterly report" ([Q3 2026 report](https://site.ncfgiving.com/wp-content/uploads/2026/10/Quarterly-Charitable-Investment-Report-Q3-2026.pdf)) [F].
  - The pre-September Q1/Q2 2026 reports return 404 at the site host, and a script stub at www.
  - A search snippet shows old-pool returns, but the column headers could not be confirmed, so it was **not used**.
- **CJP.** JCEP needs a DAF of $500,000, with $100,000 in JCEP. The 2026-04 policies also allow an S&P 500 index option for DAFs of $10m or more in JCEP [F].

---

## 2. Published returns and pool-minus-benchmark differences [F data, C differences]

### 2.1 Coverage

| Sponsor | As of | Horizons | Benchmark | Rows | Basis (as stated) |
|---|---|---|---|---|---|
| Fidelity Charitable | 2026-09-30 | 1y, 3y, 5y (also 10y, life) | per pool | 75 | Includes Fidelity admin fee; benchmarks "not adjusted for fees" |
| Vanguard Charitable | 2026-09-30 (Private Assets 2026-02-28) | 1y, 5y (no 3y published) | per option | 72 | Not stated whether net of the 0.60% admin fee |
| NPT | 2026-06-30 | 1y, 3y, "7-YEAR" header / 5-year footnote | none | 21 | Model + actual blend; net of advisory fee and trading, gross of admin fee |
| NCF | 2026-09-30 | 1y, 3y, 5y | composite, pro forma | 9 | Benchmark only; pools have no history |
| FFTC | 2026-09-30; calendar 2021–2025 | 1y, 3y, 5y; calendar years | per pool | 51 | Preliminary; net of investment fees; admin fees separate |
| GKCCF | 2025-12-31 and 2026-10-31 | 1y, 3y, 5y | per pool and mix | 105 | Gross of GKCCF admin fees; net of investment costs |
| CJP | 2026-09-30 | 1y, 3y, 5y | per option (none for the Sustainable Fund) | 21 | Net of investment and custody fees, not admin fees |

### 2.2 Differences (median, pp) [C]

| Sponsor, as of | Group | 1y | 3y | 5y |
|---|---|---|---|---|
| Fidelity 2026-09-30 | Conventional pools (n=20) | −0.30 | −0.10 | −0.65 (1 of 20 positive) |
| | Sustainable/impact pools (n=5) | −0.89 | −1.33 | −1.22 (0 of 5 positive) |
| | 7 asset-allocation pools | +0.65 to +2.79 | −0.11 to +0.16 | **−0.58 to −0.76** |
| Vanguard 2026-09-30 | Non-ESG options with a value (1y n=31; 5y n=16) | −0.04 | n/p | −0.04 |
| | ESG/impact (1y n=4; 5y n=3) | −0.52 | n/p | −0.07 |
| FFTC 2026-09-30 | 6 conventional pools | −0.10 | −0.10 | −0.15 |
| | ESG LTG | −1.9 | −1.5 | n/a (inception 2021-11-30) |
| GKCCF 2025-12-31 | 5 pools + 5 mixes | −0.07 | −0.06 | −0.09 |
| GKCCF 2026-10-31 | 5 pools + 5 mixes | −0.11 | −0.11 | −0.08 |
| | 3 impact pools + 12 impact mixes | −0.34 | −0.48 | **−2.41** (n=10; includes pro forma before 2022-09-30) |
| CJP 2026-09-30 | 6 options with a benchmark | 0.0 | −0.1 | +0.5 |

**FFTC calendar years 2021–2025** (pool sheets; 6 pools × 5 years = 30 rows) [F/C]:
- **Median:** −0.1 pp; 11 of 30 rows are positive.
- **Largest gaps:** Active LTG −1.4 pp in 2023, Diversified LTG −1.3 pp in 2023 and −1.0 pp in 2021, Low Duration −0.9 pp in 2021.
- **Passive LTG:** −0.1 to −0.2 pp in every year.

**Single rows that a reader should not over-read.** These are as published; the sources do not explain them [F]:
- **Fidelity U.S. Equity Access:** 1y 6.42% against the S&P 500 at 15.74% (−9.32 pp), while its underlying T. Rowe Price fund shows 15.89%.
- **Fidelity International Equity:** 1y −12.02 pp and 5y −5.15 pp, consistent with its underlying Overseas fund's own figures.
- **CJP US Equity Index Fund:** 1y 12.5% against the S&P 500 at 15.7%, despite holding 100% Fidelity 500 Index; inception 2025-06-20.
- **Vanguard Windsor II, Commodity Strategy and Global Positive Impact:** −8.9 to −9.3 pp over 1 year.

### 2.3 Readings [I]
- **Fee basis drives much of the cross-sponsor spread.** Fidelity's pool returns include its admin fee, and its asset-allocation pools trail their composites by 0.58–0.76 pp a year over 5 years. That is about the size of its 0.60% first-tier admin fee. GKCCF, CJP, FFTC and NPT report returns before admin fees, and Vanguard does not say. Raw gaps are therefore not like-for-like (P-B42N19-03).
- **Low-cost index menus deliver their benchmarks.** Vanguard, GKCCF and FFTC Passive land within about 0.1–0.2 pp a year before admin fees.
- **Active, alternative and ESG options carry tracking risk in both directions.** The 2021–2026 trailing windows include 2022, when growth-tilted ESG and environmental strategies lagged broad indices. Only calendar-year data can show whether the lag persists (P-B42N19-02).

---

## 3. Data dictionary

### 3.1 `sponsor-investment-menus-2026.csv`

| Column | Meaning |
|---|---|
| rank_fy2024, sponsor, ein, fy2024_daf_assets_usd_bn | From `sponsor-terms-census-top20-2026.csv` |
| pools_or_options_count, count_basis | Number of sponsor pools or options, and the document it comes from |
| asset_classes | Asset classes covered by the menu |
| esg_impact_options | Named ESG or impact options |
| adviser_program, adviser_program_minimum_usd, adviser_program_rules | Adviser-managed (CIAP-style) programme, its minimum and its rules or fees |
| pool_expense_ratio_range, pool_expense_weighted | Published expense-ratio range; asset-weighted figure where computable |
| returns_published, return_horizons_published, benchmark_published, return_basis, returns_as_of | Whether and how returns are published |
| returns_csv_rows | Pointer to rows in the returns CSV |
| source_urls, evidence_label, robots | Provenance; [R]/[U] where the host was not fetched |
| reused_repo_rows | Repo rows reused instead of re-fetching |
| notes | Caveats |

### 3.2 `sponsor-pool-returns-2021-2025.csv`

| Column | Meaning |
|---|---|
| row_id | R001–R354 |
| sponsor, pool, pool_type, esg_impact | Identity; esg_impact = yes for options the sponsor labels sustainable, ESG or impact |
| as_of, period | Period end; `trailing Ny` (annualised for N>1) or `calendar year YYYY` |
| pool_return_pct, benchmark_return_pct | As published, in %; blank where not published |
| benchmark_name | As labelled by the sponsor; Vanguard composite definitions come from the page footnotes |
| pool_minus_benchmark_pp | pool − benchmark in percentage points [C]; blank where either side is missing |
| return_basis | Fee basis as the sponsor states it |
| source_url, evidence_label, retrieved, notes | Provenance and caveats |

### 3.3 `queue-proposals-batch42-n19.csv`
- Columns per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- IDs are P-B42N19-01..03.

---

## 4. Source register

| ID | Source | Date | robots | Used for |
|---|---|---|---|---|
| S01 | [Fidelity Pool Performance Summary](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/monthly-pool-performance-summary.pdf) | as of 2026-09-30 (PDF 2026-10-09) | allowed | returns, ERs, pool list |
| S02 | [Fidelity pool performance page](https://www.fidelitycharitable.org/giving-account/investment-options/pool-performance.html); [CIAP page](https://www.fidelitycharitable.org/giving-account/investment-options/charitable-investment-advisor-program.html); [sustainable & impact page](https://www.fidelitycharitable.org/giving-account/investment-options/impact-investing-pool.html) | live 2026-11-15 | allowed | menu, CIAP |
| S03 | [Vanguard Charitable investments](https://www.vanguardcharitable.org/investments); [performance](https://www.vanguardcharitable.org/investments/investments-performance); [fees](https://www.vanguardcharitable.org/fees-and-expenses) | 2026-09-30 / 2026-11-14 | allowed | options, ERs, returns |
| S04 | [NPT Investment Descriptions and Performance](https://www.nptrust.org/investment-descriptions-and-performance-npt/) (NPT FOR IDAP 0926) | as of 2026-06-30 | allowed | portfolios, fees, returns |
| S05 | [NCF investments page](https://www.ncfgiving.com/investments/); [pools comparison chart](https://site.ncfgiving.com/wp-content/uploads/2026/11/Investment-pools-comparison-chart.pdf); [Q3 2026 report](https://site.ncfgiving.com/wp-content/uploads/2026/10/Quarterly-Charitable-Investment-Report-Q3-2026.pdf) | 2026-10/11 | allowed | menu, benchmark rows |
| S06 | [SVCF investment options](https://www.svcf.org/donors/investment-options); [advisor options](https://www.svcf.org/advisors/advisor-investment-options) | live | allowed | menu, IMF |
| S07 | [AEF advisors FAQ](https://www.aefonline.org/advisors/) | live | allowed | adviser model |
| S08 | [RCF advisor-managed](https://renaissancecharitable.org/advisor-managed-dafs/); [donor-directed](https://renaissancecharitable.org/donor-directed-dafs/) | live | allowed | menu |
| S09 | [Merrill CGF article](https://www.ml.com/articles/the-bank-of-america-charitable-gift-fund.html); [BofA overview](https://www.bankofamerica.com/philanthropic/gift-fund-overview/) | live | allowed | BofA menu |
| S10 | ImpactAssets help centre: [options](https://impactassets.freshdesk.com/support/solutions/articles/62000232304-what-investment-options-are-available-through-the-impactassets-donor-advised-fund-) (2025-10-03); [minimums and fees](https://impactassets.freshdesk.com/support/solutions/articles/62000220213-account-minimums-fees) (2021-10-13); [platform folder](https://impactassets.freshdesk.com/support/solutions/folders/62000167177) | as dated | allowed | menu |
| S11 | [FFTC performance report](https://www.fftc.org/sites/default/files/documents/FFTC_Performance_Report.pdf); [All Pool Sheets](https://www.fftc.org/sites/default/files/documents/All_Pool_Sheets.pdf); [investments](https://www.fftc.org/investments) | 2026-09-30 / PDF 2026-11-03 | allowed | returns, calendar years, ERs, alliance programme |
| S12 | GKCCF [investing page](https://growyourgiving.org/investing); summaries [Oct 2026](https://www.growyourgiving.org/wp-content/uploads/2026/11/Investment-Performance-Summary-Oct-2026-GKCCF.pdf), [ESG Oct 2026](https://www.growyourgiving.org/wp-content/uploads/2026/11/ESG-Investment-Performance-Summary-Oct-2026-GKCCF.pdf), [Dec 2025](https://www.growyourgiving.org/wp-content/uploads/2026/01/Investment-Performance-Summary-Dec-2025-GKCCF.pdf) | as dated | allowed | returns, mixes, fees |
| S13 | Greater Horizons [page](https://www.greaterhorizons.org/individual-family-giving/investment-options-performance/); [Oct 2026 summary](https://www.greaterhorizons.org/wp-content/uploads/2026/11/Investment-Performance-Summary-Oct-2026-GH.pdf); [ESG Oct 2026](https://www.greaterhorizons.org/wp-content/uploads/2026/11/ESG-Investment-Performance-Summary-Oct-2026-GH.pdf) | 2026-10-31 | allowed | identical-figures check |
| S14 | [CJP DAF report](https://www.cjp.org/hubfs/DAF_Report.pdf?hsLang=en) (PDF 2026-10-26); [CJP DAF Policies and Procedures](https://ma.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf) (2026-04-29) | 2026-09-30 | allowed | returns, options, JCEP rules |
| S15 | [Dechomai home](https://dechomai.org/) | live | allowed | absence of menu |
| S16 | [Raymond James IAP guidelines (third-party host)](https://www.aesinternational.com/hubfs/Independent%20Reviews/Raymond%20James/Donor%20Advised%20Fund%20IAP%20Investment%20Guidelines.pdf) | 2017-11-30 (pre-2021, context only) | allowed | RJ context |
| S17 | Search-index captures only [R]: dafgiving360.org quarterly performance report; cct.org investment-pools page; jcfny.org investment FAQs and forms; ncfgiving.com 2026 Q2 report (not used) | — | not fetched (403 / unreadable / page 403) | [R] cells |
| S18 | Repo: `wealth-captive-terms-2026.csv`, `infund-expense-nationals-2026.csv`, `daf-impact-pools-2026.csv`, `queue-adviser-fees-pools-npact.md` §1.1–§2, `sponsor-fee-schedules.csv`, `sponsor-terms-census-top20-2026.csv` | repo | n/a | reused rows |

---

## 5. Limits
- **Trailing windows, not calendar years.** The brief asked for 2021–2025. Only FFTC (calendar years) and GKCCF (trailing to 2025-12-31) match it; every other return row ends between 2026-06 and 2026-10.
- **Fee bases differ.** See §2.3. No adjustment was applied, because doing so would mean inferring returns that are not published.
- **Pro forma history.** GKCCF impact pools and mixes are pro forma before 2022-09-30, and its equity pools before 2019-06-30. NPT returns blend model and actual figures. NCF figures are benchmark-only.
- **Four of 20 sponsors rest on [R]/[U]:** DAFgiving360, CCT, JCF and Raymond James (P-B42N19-01). MS GIFT and GS DAF rely on repo rows that were not re-fetched.
- **Transcription.** Values were parsed from text layers. FFTC's ESG pool calendar rows are chart images and were not transcribed. Vanguard values were parsed from page HTML (36 options; the composite benchmark names for the 6 portfolio solutions come from the page footnotes).

## 6. Reproduction
```
# fetch (robots-checked) into DL/{fid,vc,npt,ncf,fftc,gk,cjp}; pdftotext -layout each PDF; FFTC pool sheet per page -> DL/fftc/p1..p12.txt
python3 scripts/mission_pool_returns_vc_parse.py DL/vc/perf.txt > DL/vc/parsed.jsonl   # Vanguard page text from HTML
python3 scripts/mission_pool_returns.py DL data/mission-2026-11-14/sponsor-pool-returns-2021-2025.csv
```
The menus CSV was entered by hand from the cited pages and repo rows.
