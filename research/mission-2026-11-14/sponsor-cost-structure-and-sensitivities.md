# Sponsor cost structure from Form 990 Part IX, and Givinga / SDG Impact Fund sensitivities

*Queue items P-99F-04, P-ASR-03, P-ASR-02 and P-99F-02. Prepared 2026-11-14. Builds on `full-universe-990-harvest-and-corrected-totals.md` (return universe and corrected totals), `queue-assurance-everyorg-givinga-monitoring.md` §3 (Givinga) and `sponsor-mortality-analysis.md` §6 (SDG Impact Fund). Script (stdlib only, functional style): `scripts/mission_sponsor_cost_structure.py`. It reuses helpers from `scripts/mission_990_contractors.py` but adds its own extended extractor and cache, so the earlier harvest outputs are untouched.*

Notation: **[F]** filed or published fact; **[C]** computed from the cited data; **[I]** inference.

## 1. Bottom line

1. **Real operating-cost data exists, and it is large compared with the AI model's labour pools.** All 5,272 parsed returns (1,512 sponsors, FY2022–FY2025) were re-read with full Part IX by column ([IRS e-file XML via the GivingTuesday mirror](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml)).
   - **[C]** In FY2024, operating cost (total functional expenses minus grants, excluding investment-management fees), allocated to DAFs by each sponsor's DAF share of assets, is **$2.14bn**, or **67 bps of DAF assets**. Allocated by DAF share of grants it is **$2.83bn (89 bps)**. Both figures exclude university and hospital foundations (§4.5).
   - **[C]** Standard nationals spend **32 bps** ($746m). Excluding Servant Foundation, whose $141m of "advertising" is campaign spending rather than overhead, they spend **25 bps**. Community foundations spend **127–177 bps** ($0.81–1.12bn) on the DAF-allocated share. Processors spend **456–805 bps** but only **$82–146 per account**.
2. **Cost per grant at the largest nationals is $55–$135.**
   - **[C]** Operating cost per self-reported grant: Fidelity Charitable **$68**, DAFgiving360 **$55**, Vanguard Charitable **$134**, NPT **$419**, Goldman Sachs Philanthropy Fund **$574**. Periods are matched with gaps of 0–18 months (§4.4).
   - **[C]** The AI-economics model's base sponsor-side labour pool is **$4.32 per grant** ($4.32m at 1M grants). That is 3–8% of the observed operating cost per grant at the 1M+ grant sponsors.
   - **[I]** The model's pool is therefore not implausibly large. It is a narrow slice of the cost base. Most of what a large national spends goes to affiliated administrators and staff, not to measured exception handling.
3. **IT is a small, visible line.**
   - **[C]** Line 14 is positive on 918 of 1,507 FY2024 returns. The median sponsor spends **2.8% of operating cost** on it (3.3% for community foundations).
   - **[C]** Median community-foundation IT spend is **$17k** for sponsors under $10m of DAF assets, **$55k** at $10–50m, **$116k** at $50–250m, **$468k** at $250m–1bn and **$1.28m** at $1–10bn.
   - **[C]** The AI doc's fixed-cost hurdle for an AI project is $150k–$750k [S]. For the 742 community foundations under $250m, that is **1.3–45× the median annual IT line** in their size band.
   - **[F]** Large platform costs mostly sit elsewhere, in line 11a or 11g. Fidelity reports **$0 IT and $139.7m of line 11a management fees** for FY2024 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml)).
4. **There are strong scale economies at nationals and moderate ones elsewhere.** **[C]** The FY2024 log-log elasticity of operating cost to DAF assets is **0.41** for standard nationals (n = 76, r² 0.37) and 0.47–0.48 in FY2022–23. For community foundations, operating cost against total assets is **0.84** (n = 798, r² 0.72). Median whole-organisation operating cost falls from **243 bps** (under $10m) to **84 bps** ($1–10bn) for community foundations, and to **18 bps** for the five nationals over $10bn.
5. **Givinga (P-ASR-03).** **[C]** Excluding Givinga changes the processor share of FY2022/23/24 accounts from **80.5/77.4/79.5%** to **63.0/67.0/66.0%** (published), or to **63.0/67.0/59.2%** on corrected data. FY2022 account growth changes from **+72.3% to −7.2%**. Assets move by less than $6m.
6. **What a Givinga "account" is (P-ASR-02).**
   - No Form PC or audited statement could be retrieved. The Massachusetts AG pages return HTTP 403 and the portal hosts are unreachable from this environment.
   - **[F]** The 990s point to an answer instead. Schedule G names **Golden Hearts Games Inc**, a charity sweepstakes casino, as Givinga's largest "online fundraising" agent: **$15.4m of $34.5m** contributions in CY2022, of which GHG retained **$13.2m** ([CY2022 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333199349323323_public.xml)).
   - **[F]** GHG's own release says "all GHG donations flow into a 501c3 donor-advised fund" ([PR Newswire, 2022-06-22](https://www.prnewswire.com/news-releases/boston-based-golden-hearts-games-the-worlds-first-charity-casino-surpasses-10m-in-donations-processes-over-6m-in-2022-alone-as-over-50-000-nonprofits-have-now-received-funding-from-the-platform-301573591.html)).
   - **[I]** The 1.5m "accounts" are most plausibly player and app-user records.
7. **SDG Impact Fund (P-99F-02).** **Recommendation: exclude it from headline totals and footnote it.**
   - **[C]** Including it adds **+4.3% (FY2021)** and **+4.4% (FY2022)** to assets. It inflates FY2020→21 growth from 38.9% to **44.6%**, and it cuts FY2022→23 growth from 11.6% to **6.9%** (12.4% → 7.6% corrected), because the fund stops filing.
   - **[C]** It would rank **#6 and #5** by DAF assets in those years. It lowers CR5 by about 2 points and HHI by 42–45 points.

## 2. Method

### 2.1 Data
| Source | Use |
|---|---|
| `data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv` (5,416 located / 5,272 parsed returns; object IDs) | Return universe and sponsor classification (DAFRC FY2024 type/subtype) |
| Form 990 XML, `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml` (all 5,272 re-fetched; 0 failures) | Part I summary, Part III narrative, **Part IX lines 1–25 in all four columns**, Schedule D Part I, Schedule I recipient counts |
| `dafrc-sponsor-schedule-d-fy2019-2024.csv` ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | Fallback DAF assets/accounts, published panel |
| `dafrc-corrections-itemized.csv`, `dafrc-corrected-market-totals.csv` | Corrected panel (rebuilt; it reproduces the corrected asset and account totals exactly for FY2020–24) |
| `non-dafrc-daf-filers-990.csv` (EIN 462368538 rows) | SDG Impact Fund FY2020–22 Schedule D values |
| `sponsor-level-metrics.csv` (`grant_count` rows) | Self-reported grant counts (Fidelity, DAFgiving360, Vanguard, NPT, Charityvest, GS) |

The earlier extractor kept only four Part IX totals (lines 11a, 11f, 11g, 14). The new extractor streams the whole return. It captures every Part IX group that is a direct child of `IRS990`, with total, program, management and fundraising columns. Repeating line-24 groups are summed. Coverage across the 5,272 returns: line 25 5,272; line 11c 4,621; line 11f 3,911; line 11g 3,786; line 14 3,502; line 7 4,193; line 11e 1,014; Schedule I 4,928.

### 2.2 Definitions (per sponsor-year)
- **Operating cost** = Part IX line 25(A) − lines 1–3 (grants) − line 4. The headline uses **operating cost excluding line 11f** (investment-management fees). Line 11f scales with asset management, not DAF administration. Many sponsors net it inside fund returns, so it appears on the 990 only sometimes.
- **Staff** = lines 5–10. **Outside services** = lines 11a–g, also shown excluding 11f. **IT** = line 14.
- **Ratios to assets** use average total assets (Part I begin- and end-of-year).
- **Allocation sensitivity (labelled).** Most community and single-issue sponsors run non-DAF programs. The DAF-allocated cost is whole-organisation cost × DAF share. Two shares are used:
  - **A** = Schedule D DAF value ÷ total assets;
  - **G** = Schedule D DAF grants ÷ Part IX grants.
  Both are clipped to [0, 1]. Under A, the allocated cost per $ of DAF assets equals the whole-organisation cost ratio. The per-account figures differ by basis.
- **Size band** is by DAF assets (Schedule D, or the DAFRC same-FY value if blank): <$10m, $10–50m, $50–250m, $250m–1bn, $1–10bn, >$10bn.
- **Category**: National-Standard (81), National-Processor (22), Community (803), Single-issue Religious (184), Other (294), University/Health (128).
- **Exclusions from statistics:** Givinga (undefined account unit), returns with no line 25, and returns with operating cost ≤ 0. Per-account statistics need at least 1 account.
- **Grant counts.** Schedule I lists only recipients receiving more than $5,000, aggregated per recipient. "Per Schedule I recipient" is therefore a ratio per *recipient organisation*, not per grant. True per-grant figures use the self-reported counts, matched to the 990 with the nearest period end. The month gap is stated.
- **Scale economies:** OLS of log cost on log scale. A slope below 1 means cost grows less than proportionally.

## 3. Coverage

| FY | Returns parsed | Line 14 > 0 | Line 25 present |
|---|---|---|---|
| 2022 | 1,494 | 875 | 1,494 |
| 2023 | 1,513 | 897 | 1,513 |
| 2024 | 1,507 | 918 | 1,507 |
| 2025 (partial) | 758 | 467 | 758 |

Source: `sponsor-cost-structure.csv`.

## 4. Findings: cost structure (P-99F-04)

### 4.1 By category, FY2024
Source: `sponsor-cost-structure-summary.csv` (`dimension = category`, FY2024). Values are medians, with the aggregate (Σ numerator ÷ Σ denominator) in brackets.

| Category | n | Operating cost bps of total assets | IT % of operating cost | Outside services ex-11f % of operating cost | Staff % of operating cost | DAF share of assets | DAF-allocated cost per account (A) | (G) | IT per account (A) |
|---|---|---|---|---|---|---|---|---|---|
| National-Standard | 79 | **66** (52) | 2.3% (5.4%) | 32.4% | 24.4% (28.3%) | 0.98 | **$2,556** ($1,389) | $2,536 ($1,411) | $139 |
| National-Processor | 20 | 1,160 (638) | 0.7% | 54.7% | 6.3% | 0.76 | $13,683 (**$82**) | $20,344 ($146) | $17 |
| Community | 799 | **196** (165) | 3.3% (3.5%) | 10.0% | 54.5% (50.2%) | 0.23 | **$3,803** ($7,954) | $5,602 ($11,122) | $130 |
| SI-Religious | 184 | 196 (422) | 2.7% | 8.0% | 58.7% | 0.20 | $2,725 ($3,769) | $7,669 ($5,478) | $88 |
| SI-Other | 291 | 1,057 (1,157) | 1.7% | 12.1% | 53.0% | 0.13 | $9,345 ($1,350) | $8,491 ($2,546) | $198 |
| SI-Univ/Health | 128 | 501 (1,759) | 1.8% | 8.2% | 55.8% | 0.007 | $10,227 | $11,166 | $210 |

**Contrasts [C/I]:**
- **Standard nationals** are almost pure DAF (median DAF share 0.98). They mostly buy rather than employ. The median standard national has **0 employees**, outside services are a third of operating cost, and IT is a small line. The cost sits in line 11a/11g payments to affiliated administrators. Examples: Fidelity $139.7m in line 11a; RCF $11.7m in 11f and $19.2m in 11g.
- **Community foundations** are labour businesses. Staff are 54% of operating cost, and they spend 196 bps of total assets. They are a DAF business only in part (median DAF share 23%). Allocated per DAF account they cost about **$3.8k (A) to $5.6k (G)** a year at the median, against about $2.6k at nationals.
- **Processors** look expensive per $ of assets (their balances are tiny) but cheap per account: **$82–146 per account in aggregate**. Their cost is outside services: AOGF $54.6m in line 11, $87 per account ([FY2024 990 via harvest](../../data/mission-2026-11-14/sponsor-cost-structure.csv)). PayPal Charitable Giving Fund's operating cost is $36 per account.
- **Single-issue charities**: the DAF program is a sideline (DAF share 0.7–20%). Whole-organisation ratios say nothing about DAF cost, so only the allocated figures should be used, and those are weak (§6).

### 4.2 Community foundations by size band, FY2024 (medians)

| DAF assets | n | Operating cost (level) | Operating cost bps of total assets | IT (level) | IT % of operating cost | Accounting fees 11c | Employees | DAF share of assets | DAF cost per account (A) | (G) |
|---|---|---|---|---|---|---|---|---|---|---|
| <$10m | 427 | $406k | **243** | $17k | 3.1% | $16k | 3 | 0.12 | $2,163 | $3,003 |
| $10–50m | 207 | $1.55m | 189 | $55k | 3.3% | $29k | 9 | 0.28 | $4,689 | $7,504 |
| $50–250m | 108 | $4.05m | 162 | $116k | 3.0% | $53k | 21 | 0.37 | $6,746 | $9,894 |
| $250m–1bn | 43 | $10.5m | 119 | $468k | 4.6% | $99k | 54 | 0.55 | $9,586 | $12,204 |
| $1–10bn | 10 | $28.6m | **84** | $1.28m | 5.6% | $242k | 124 | 0.63 | $13,588 | $16,452 |

**Reading [C/I]:**
- Cost per $ of assets falls by about two-thirds across the range (243 → 84 bps), so there are scale economies on assets.
- **Cost per DAF account rises with size** (the elasticity of allocated cost to accounts is 1.22). Bigger community foundations hold larger, more serviced funds. Their unallocated cost per account is flat at about $18–21k. "Cost per account" is therefore not a scale-free unit for pricing software.
- The IT share of operating cost rises with size (3% → 6%). Large community foundations buy more technology per dollar of cost; small ones barely have an IT line.

### 4.3 Standard nationals by size band, FY2024 (medians)

| DAF assets | n | Operating cost (level) | bps of total assets | IT (level) | Employees | Operating cost per account (unallocated) |
|---|---|---|---|---|---|---|
| <$10m | 19 | $282k | 1,635 | $5k | 0 | $27,712 |
| $10–50m | 15 | $199k | 111 | $5k | 0 | $3,894 |
| $50–250m | 17 | $812k | 57 | $69k | 0 | $3,952 |
| $250m–1bn | 12 | $2.19m | 46 | $153k | 0 | $1,686 |
| $1–10bn | 10 | $16.5m | 33 | $342k | 0 | $1,100 |
| >$10bn | 5 | $61.4m | **18** | $3.65m | 119 | $1,302 |

The five nationals over $10bn ([F] FY2024 990s via `sponsor-cost-structure.csv`):

| Sponsor | Operating cost ex-11f bps (incl. 11f) | Operating cost per account | IT | Employees |
|---|---|---|---|---|
| Fidelity Charitable | 26 (37) | $790 | $0 | 0 |
| NPT | 17 (38) | $3,425 | $3.65m | 286 |
| DAFgiving360 | 21 (34) | $681 | $20.1m | 194 |
| Vanguard Charitable | 18 (18) | $1,302 | $14.3m | 119 |
| GS DAF Philanthropy Fund | 12 (29) | $3,236 | $2.8m | 0 |

### 4.4 Cost per grant (self-reported counts matched to the nearest 990)
Source: `sponsor-cost-structure-summary.csv`, `dimension = grant_count_anchor`. Counts come from `sponsor-level-metrics.csv`, with the URL given per row.

| Sponsor | Count (period, qualifier) | 990 period (gap) | Operating cost / grant | Staff / grant | IT / grant | Outside services ex-11f / grant |
|---|---|---|---|---|---|---|
| Fidelity Charitable | 3.0m (CY2025, rounded; [report](https://www.fidelitycharitable.org/insights/2026-giving-report.html)) | FY Jun-2025 (6 mo) | **$67.70** | $0 | $0 | $60.59 |
| DAFgiving360 | 1.6m (FY Jun-2026, lower bound; [release](https://www.dafgiving360.org/press-release/fiscal-year-2026-results)) | FY Jun-2025 (12 mo) | **$54.59** | $25.37 | $11.84 | $2.87 |
| Vanguard Charitable | 267,838 (CY2025; [report](https://www.vanguardcharitable.org/2025annualreport)) | FY Jun-2024 (18 mo) | $134.50 | $55.32 | $53.48 | $10.80 |
| NPT | 159,543 (FY Jun-2025; [report](https://www.nptrust.org/annual-reports/npt-annual-report/)) | FY Jun-2025 (0 mo) | $419.24 | $242.71 | $36.80 | $22.41 |
| Charityvest | 48,744 (CY2025; [release](https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/)) | CY2024 (12 mo) | $16.66 | $0 | $0.99 | $1.27 |
| GS Philanthropy Fund | ~24,800 (2023, aggregator summary of 990; [CauseIQ](https://www.causeiq.com/organizations/goldman-sachs-philanthropy-fund,311774905/)) | CY2023 (0 mo) | $573.70 | $0 | $87.90 | $139.87 |

Period gaps bias the figures. Where grant volume grows (DAFgiving360 +21%, Charityvest more than doubling), a later count against an earlier cost understates cost per grant. Operating cost includes everything except grants and line 11f: marketing, donor service, investment operations and compliance. It is a ceiling on any process pool.

### 4.5 Market-level DAF cost pool, FY2024
Source: `dimension = daf_cost_pool`. Allocated sums; bps of the DAF assets of contributing rows.

| Group | Operating cost ex-11f, A | G | Staff A | Outside ex-11f A | IT A | IT G | 11f A |
|---|---|---|---|---|---|---|---|
| All excl. Univ/Health | **$2,136m / 67 bps** | $2,826m / 89 bps | $791m | $527m | **$97m / 3.3 bps** | $116m | $537m |
| National-Standard | $746m / 32 bps (excl. Servant $579m / 25 bps) | $757m | $162m | $252m | $48m | $48m | $329m |
| Community | $807m / 127 bps | $1,120m / 177 bps | $402m | $137m | $29m | $40m | $163m |
| National-Processor | $92m / 456 bps | $163m | $2m | $56m | $3m | $5m | $0 |
| SI-Religious | $298m / 158 bps | $423m | $151m | $39m | $13m | $16m | $40m |
| SI-Other | $194m / 606 bps | $364m | $74m | $43m | $4m | $6m | $5m |

University and hospital foundations are shown separately in the CSV ($435m A / $1,536m G). These allocations multiply nine- to ten-figure organisational budgets by DAF shares under 1%, so the figures are not meaningful.

**[I]** Sponsors' own DAF-attributable spend on line 14 IT is about **$0.1bn a year**, while outside services are about $0.5bn and staff about $0.8bn. The DAF software and outsourced-administration market visible in Part IX is therefore the outside-services and IT lines together, about **$0.6–0.8bn**. That is a ceiling on sponsor-paid vendor spend, before investment-management fees. This is consistent with Part VII-B naming only $119m of Ren payments over four years (`full-universe-990-harvest-and-corrected-totals.md` §3.2).

### 4.6 Scale elasticities (log-log OLS)

| Group | Relationship | FY2022 | FY2023 | FY2024 (n, r²) |
|---|---|---|---|---|
| National-Standard | operating cost ~ DAF assets | 0.47 | 0.48 | **0.41** (76, 0.37) |
| National-Standard | operating cost ~ DAF accounts | 0.48 | 0.49 | 0.43 (77, 0.32) |
| National-Standard | IT ~ DAF assets (IT > 0) | 0.53 | 0.50 | 0.44 (36, 0.31) |
| Community | operating cost ~ total assets | 0.84 | 0.86 | **0.84** (798, 0.72) |
| Community | IT ~ total assets | 0.85 | 0.83 | 0.83 (517, 0.63) |
| Community | allocated operating cost ~ DAF accounts | 1.19 | 1.23 | 1.22 (792, 0.69) |
| Community | operating cost ~ employees | 1.12 | 1.10 | 1.12 (700, 0.82) |
| All excl. processors | operating cost ~ total assets | 0.85 | 0.85 | 0.83 (1,477, 0.61) |

**[I]** Doubling a national's assets raises its operating cost by about 33% (2^0.41). Doubling a community foundation's raises it by about 79%. Nationals' costs scale with what they buy (platform fees, often asset-based). Community foundations' costs scale with headcount, at roughly $144k of operating cost per employee (median, FY2024).

## 5. Findings: Givinga sensitivity (P-ASR-03) and account definition (P-ASR-02)

### 5.1 Sensitivity table
Source: `data/mission-2026-11-14/market-sensitivity-givinga-sdg.csv`, rebuilt from the [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) and `dafrc-corrections-itemized.csv`.

| FY | Variant | Accounts | Processor share of accounts | Account growth | Avg assets per account | Givinga share of accounts |
|---|---|---|---|---|---|---|
| 2022 | published | 3,258,359 | **80.5%** | +72.3% | $70,492 | 47.4% |
| 2022 | excl. Givinga | 1,715,156 | **63.0%** | **−7.2%** | $133,913 | – |
| 2022 | corrected excl. Givinga | 1,714,910 | 63.0% | −7.1% | $133,032 | – |
| 2023 | published | 3,030,552 | **77.4%** | −7.0% | $84,601 | 31.5% |
| 2023 | excl. Givinga | 2,074,983 | **67.0%** | **+21.0%** | $123,560 | – |
| 2024 | published | 3,590,067 | **79.5%** | +18.5% | $91,327 | 39.6% |
| 2024 | excl. Givinga | 2,169,056 | **66.0%** | +4.5% | $151,157 | – |
| 2024 | excl. Givinga and imputed PayPal | 1,474,077 | 50.0% | – | $222,321 | – |
| 2024 | corrected (PayPal filed 380,644) | 3,309,483 | 76.7% | +9.2% | $97,680 | 42.9% |
| 2024 | **corrected excl. Givinga** | 1,888,472 | **59.2%** | **−9.0%** | $171,179 | – |

Assets, contributions, grants, payout and concentration move by less than 0.01 pp in every year: Givinga's DAF value is $2–5m. Non-processor accounts are unaffected: 635,008 / 685,289 / 737,159 published, and 770,785 corrected for FY2024.

**Recommended statement [C]:** "Donation processors hold **59–80%** of reported US DAF accounts in FY2024: 79.5% as published, 66.0% excluding Givinga, and 59.2% on corrected filed data excluding Givinga. They hold under 1% of assets in every variant." This replaces the 50–79.5% range in `regulation-market-structure-portability.md`. The 50% figure removed PayPal's imputed count but kept nothing in its place. The filed count of 380,644 now exists, so the defensible floor is 59.2%. Account *trend* statements (for example "accounts nearly doubled in 2022") should be made only without Givinga: on that basis accounts fell 7% in FY2022.

### 5.2 What a Givinga "account" is

**Massachusetts AG Form PC / audited statements: not retrievable here.**
- `mass.gov` charity-filing pages return HTTP 403 to this environment, and the AG portal hosts fail at the proxy (CONNECT 502).
- No copy of Givinga's audited statements was found on Candid, ProPublica or Givinga's sites. Searches were run on 2026-11-14.
- **[F]** The CY2022 amended 990 confirms that audited statements exist: Part XII line 2b is "Yes", Schedule D Part XI reconciles "revenue per audited financial statements" of $34,461,768, and the preparer is Nisivoccia LLP ([Candid copy of 990 render](https://docs.candid.org/edoc/10562785/document.pdf); [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202420369349301017_public.xml)). The audit itself remains unseen.
- So the question as posed is **open**, and a manual request to the AG Non-Profit/Public Charities Division is needed (proposal P-COST-04).

**What the 990s show instead [F]: Schedule G professional fundraisers.**

| Tax year (return) | Fundraiser | Gross receipts | Retained by fundraiser | To Givinga |
|---|---|---|---|---|
| 2020 ([orig.](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202123199349306837_public.xml)) | SoftGiving Inc / Golden Hearts Games / Britesiders | $1.39m / $0.09m / $0.05m | $0.29m / $0.07m / $0.01m | $1.10m / $0.02m / $0.04m |
| 2021 ([amended](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202330979349300728_public.xml)) | SoftGiving / Golden Hearts Games | $5.08m / $3.72m | $2.35m / $3.19m | $2.73m / $0.53m |
| 2022 ([orig.](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333199349323323_public.xml)) | **Golden Hearts Games** / SoftGiving | **$15.43m** / $3.56m | **$13.22m** / $1.65m | $2.21m / $1.92m |
| 2022 (amended, [Candid render](https://docs.candid.org/edoc/10562785/document.pdf)) | Golden Hearts Games / SoftGiving | $18.15m / $7.05m | $15.32m / $3.32m | $2.83m / $3.72m |
| 2023 ([orig.](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403139349303260_public.xml)) | Brandfluence / Golden Hearts Games | $4.37m / $3.42m | $2.24m / $2.99m | $2.14m / $0.43m |
| 2024 ([amended](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml)) | none listed; line 11e $6,462 | – | – | – |

- **[F]** Golden Hearts Games describes itself as "the world's first charity casino". Players buy virtual coins, part of each purchase goes to a player-chosen charity, and "all GHG donations flow into a 501c3 donor-advised fund" ([PR Newswire, 2022-06-22](https://www.prnewswire.com/news-releases/boston-based-golden-hearts-games-the-worlds-first-charity-casino-surpasses-10m-in-donations-processes-over-6m-in-2022-alone-as-over-50-000-nonprofits-have-now-received-funding-from-the-platform-301573591.html)).
- **[F]** Third-party reviews report that the charity program was paused in July 2024 (search summary 2026-11-14; not first-party, so unverified).
- **[F]** In CY2022, Givinga's line 11e professional fundraising fees ($14.87m original, $18.64m amended) were **73–92% of its operating cost**. The Foundation reports **0 employees** in every year.
- **[I] Answer.** Givinga's CY2022 account jump (42,307 → 1,543,203) coincides with GHG gross receipts rising from $3.7m to $15.4–18.2m. The most consistent reading is that each player or app user who directs a donation gets a Givinga ledger record, and that these records are counted as DAF "accounts".
  - That fits the $1.37–$3.40 average balance, the "no minimum" handbook, and the persistence of the 1.42m count in CY2024 after the fundraiser lines vanish (dormant records carried forward).
  - **Data-quality consequence:** Givinga's Schedule D "DAF contributions" equal gross receipts *including* the share the gaming company retains (86% for GHG in CY2022). Its contribution and payout figures are not comparable with other sponsors'.
  - This is still inference. Only the audited notes or the AG filing could confirm the account definition.

## 6. Findings: SDG Impact Fund (P-99F-02)

| FY | Assets: published → plus SDG | Δ | Asset growth: published → plus SDG | Corrected growth → plus SDG | CR5 | HHI | SDG rank |
|---|---|---|---|---|---|---|---|
| 2020 | $168.76bn → $169.00bn | +0.14% | 27.2% → 27.3% | 27.2% → 27.3% | 49.4 → 49.3% | 705 → 703 | 77 |
| 2021 | $234.33bn → **$244.43bn** | **+4.31%** | 38.9% → **44.6%** | 38.7% → 44.5% | 51.0 → 48.9% | 732 → 690 | 6 |
| 2022 | $229.69bn → **$239.79bn** | **+4.40%** | −2.0% → −1.9% | −2.5% → −2.4% | 52.3 → 50.4% | 756 → 711 | 5 |
| 2023 | $256.39bn (no SDG filing) | 0 | 11.6% → **6.9%** | 12.4% → **7.6%** | unchanged | unchanged | – |

Payout (grants ÷ prior-year assets) falls by about 1 pp in FY2022–23 with SDG (23.7% → 22.7%; 23.8% → 22.8%). Source: `market-sensitivity-givinga-sdg.csv`; SDG values from its [FY2021](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202242139349301369_public.xml) and [FY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202342799349301349_public.xml) 990s.

**Recommendation: exclude it from headline totals, growth and concentration; disclose it in a standing footnote; carry an "including SDG" line only in the sensitivity table.** Reasons:
1. **The value is unverified and probably not realisable.** **[F]** The $10.077bn is one "various digital and non-cash assets" line, unchanged between FY2021 and FY2022. No independent audit was obtained in any year. Grants over 2019–22 total $18.8m, 0.08% of the reported value (`sponsor-mortality-analysis.md` §6).
2. **A regulator has acted.** **[F]** The Georgia Secretary of State issued a cease-and-desist order and the Georgia AG has filed a receivership suit (`failed-daf-startups-deep-research.md` FD01).
3. **Including it distorts the time series more than it informs the level.** **[C]** It manufactures +5.8 pp of FY2021 growth and −4.7 pp of FY2023 growth (−4.8 pp corrected) out of one sponsor's appearance and disappearance. It also lowers measured concentration by about 2 CR5 points.
4. **DAFRC's universe already excludes it.** Keeping our headline aligned with DAFRC's vetted panel avoids a definitional break with the published series.
5. **Footnote text:** "Excludes SDG Impact Fund (EIN 46-2368538), which reported $10.10bn of DAF assets on Schedule D for FY2021–22. The value is unaudited, almost entirely non-cash, and inconsistent with its $18.8m of grants over 2019–22; the fund is subject to Georgia enforcement. Including it would raise FY2021–22 DAF assets by 4.3–4.4%."

## 7. How this updates the AI-economics cost assumptions

References are to `ai-economics-replacement-analysis.md` and `data/mission-2026-11-14/ai-process-economics.csv`.

| [S] assumption or statement (quoted) | Evidence here | Verdict |
|---|---|---|
| "Technology expense: undisclosed in public sources for every sponsor" (§3 notes) | **[F]** Line 14 IT is present on 3,502 of 5,272 returns and positive on 3,157. FY2024 medians run from $17k (small community foundation) to $3.65m (nationals over $10bn), with DAFgiving360 at $20.1m and Vanguard Charitable at $14.3m. Not by process, and large platforms book it in 11a/11g. | **Refuted as stated.** Total IT is public; per-process cost is not. |
| "sponsor-side pools (P01–P15) sum to $0.87M / $4.32M / $18.7M (low/base/high) at 1M grants" [S] | **[C]** Observed operating cost per grant is $55 (DAFgiving360) to $68 (Fidelity) at 1.6–3m grants, i.e. $55–68m per 1M grants. Staff cost alone at DAFgiving360 is $25.37 per grant, $25m per 1M. | **Consistent (not contradicted):** the base pool is 6–8% of operating cost at those sponsors and 17% of DAFgiving360's staff cost. The *high* pool ($18.7/grant) is still below observed staff cost per grant at Vanguard ($55) and NPT ($243). The spread can now be bounded above: no sponsor-side process pool can exceed about $55–135 per grant at large nationals. |
| Fixed-cost hurdle "C AI on workflow: $150k–$750k incl. evaluation, model-risk, security review" [S]; "per-process AI cases fail at sub-Fidelity scale" (§7) | **[C]** Annual IT spend: community foundation medians $17k–$116k below $250m DAF assets (742 of 795 with values); $153k for nationals at $250m–1bn; $342k at $1–10bn. | **Confirmed and sharpened.** For the median sponsor in every community-foundation band below $250m, a single AI project would exceed the whole annual IT line. In FY2024, 79 sponsors report line 14 above $1m, but only 23 of them are DAF-centred (7 standard nationals, 2 processors and 14 community foundations). 38 are university or hospital foundations whose IT serves non-DAF operations. |
| "AI pays as a shared platform across processes or at Fidelity-scale volume" (exec #4) and "favors vendors that serve many sponsors" (§7) | **[C]** Strong scale economies at nationals (elasticity 0.41); outside services are 32% of national operating cost and 10% of community-foundation operating cost; the sponsor-paid outside-services plus IT pool is about $0.6–0.8bn | **Confirmed.** The buying unit for AI is the administrator or vendor (Ren, FMR, Schwab, Vanguard affiliates), not the sponsor. |
| Loaded labour rates $30.76–$55.45/h [F→S] | **[C]** Median operating cost per employee at community foundations is $144k. At nationals with staff it is $274k, and that figure includes non-staff costs. Not a wage, so not a direct test. | **Not testable** with Part IX. Line 7 ÷ employees could test it (P-COST-02). |
| P11 donor/advisor service pool $656k [S] at 200k contacts | No contact volumes in any 990 | **Untested.** |
| Implicit: sponsor cost scales linearly with grants ("scale grant-linked results linearly (×3 for a Fidelity-sized volume)") | **[C]** Operating cost per grant ranges 8× ($55–$419) across large nationals, and operating cost rises only 0.41–0.48% per 1% of assets | **Refuted as a default.** Linear scaling overstates labour pools at large sponsors and understates them at small ones. Pools should scale with an elasticity of about 0.4–0.5, or be anchored per sponsor. |

## 8. Limitations
- **Part IX shows functional cost by line, not by process.** Nothing here measures exception rates or minutes, which remain the AI model's binding unknowns.
- **Whole-organisation cost.** Community and single-issue figures depend on the allocation basis, and A and G differ by 30–40% for community foundations. Neither basis captures the real cost-to-serve of a DAF relative to an endowment or scholarship fund.
- **Costs outside Part IX.** Investment-management fees netted inside funds, and costs borne by affiliated firms and recovered through fund expense ratios, are invisible. Some sponsors show almost no operating cost (BofA Charitable Gift Fund: $0.1m on $4.73bn in FY2024). Part IX understates the all-in donor cost at bank and broker nationals.
- **Program-like non-grant spending.** Servant Foundation's FY2024 "advertising" of $141.3m is DAF-directed campaign spending, not overhead. Similar items may exist elsewhere, so medians are preferred to aggregates.
- **Grant counts.** There are only six anchors, all self-reported or from an aggregator, with 0–18 month period gaps. Schedule I counts are recipients receiving more than $5k, not grants.
- **Givinga.** It is excluded from cost statistics. Its FY2024 harvest row is the original return; the amendment carrying the Schedule D values has a lower object ID. The account definition is an inference until the audited notes are seen.
- **FY2025** is partial: 758 returns, the 144 unmirrored returns are missing, and it is not used for headline statistics.
- **No invented values.** Every number comes from a cited XML, the DAFRC dataset, a repo CSV or a cited release.

## 9. Data dictionary

### `data/mission-2026-11-14/sponsor-cost-structure.csv` (5,272 rows; one per parsed return)
| Column(s) | Meaning |
|---|---|
| `ein`, `sponsor_name`, `category`, `type`, `subtype`, `fiscal_year`, `tax_period` | Sponsor-year. Category as in §2.2. FY = year the period ends |
| `size_band_daf_assets` | Band by `daf_assets_eoy` |
| `total_functional_expenses` | Part IX line 25(A) (Part I line 18 if absent) |
| `grants_part_ix_l1_3`, `benefits_l4` | Lines 1–3 and line 4 |
| `operating_cost`, `operating_cost_ex_invest_mgmt` | Line 25 − lines 1–4; same, less line 11f |
| `staff_cost_l5_10`, `comp_officers_l5`, `salaries_l7` | Staff lines |
| `outside_services_l11`, `fees_mgmt_l11a`, `fees_legal_l11b`, `fees_accounting_l11c`, `fees_prof_fundraising_l11e`, `fees_invest_mgmt_l11f`, `fees_other_l11g` | Line 11 total and components (11d lobbying is included in the total) |
| `it_l14`, `advertising_l12`, `occupancy_office_ins_depr` (13 + 16 + 22 + 23), `other_expense_lines` (residual) | Other lines |
| `program_col_total`, `program_col_ex_grants`, `mgmt_col_total`, `fundraising_col_total`, `it_program_col`, `it_mgmt_col` | Part IX functional columns |
| `employees`, `total_revenue`, `total_assets_eoy`, `total_assets_avg` | Part I |
| `daf_assets_eoy`, `daf_accounts`, `daf_contributions`, `daf_grants` | Schedule D Part I (DAFRC same-FY value if blank or 0; flagged) |
| `dafrc_daf_assets_same_fy`, `dafrc_accounts_same_fy` | DAFRC values for reference |
| `daf_share_of_total_assets`, `daf_share_of_grants` | Allocation shares A and G, clipped to [0, 1] |
| `opex_share_of_tfe`, `opex_bps_of_total_assets`, `opex_incl_invest_bps_of_total_assets`, `it_share_of_opex`, `outside_ex_invest_share_of_opex`, `staff_share_of_opex`, `it_bps_of_total_assets` | Whole-organisation ratios (operating cost = ex-11f unless "incl_invest") |
| `daf_alloc_opex_by_assets`, `daf_alloc_opex_by_grants` | Allocated DAF operating cost (ex-11f) |
| `opex_per_account_unallocated`, `daf_opex_per_account_assets_alloc`, `daf_opex_per_account_grants_alloc`, `daf_it_per_account_assets_alloc`, `daf_opex_bps_of_daf_assets_grants_alloc` | Per-account and per-$ DAF metrics |
| `opex_per_employee`, `daf_assets_per_employee` | Labour intensity |
| `sched_i_recipients`, `sched_i_recipient_rows`, `opex_per_sched_i_recipient` | Schedule I 501(c)(3) + other organisation counts + individual recipient counts; RecipientTable rows; cost per recipient |
| `narrative_grant_mention`, `narrative_grant_snippet` | Largest "N grants" mention in Part III text (unverified, for follow-up) |
| `audited_fs_ind` | Part IV/XII audited-statements flag as filed |
| `quality_flags` | `givinga_undefined_account_unit`, `tfe_missing`, `opex_nonpositive`, `no_daf_value`, `daf_value_gt_total_assets`, `daf_grants_gt_part_ix_grants`, `daf_share_assets_lt_5pct`, `daf_value_from_dafrc`, `accounts_from_dafrc`, `amended_return` |
| `return_object_id`, `return_ts`, `xml_url`, `source_url` | Evidence |

### `data/mission-2026-11-14/sponsor-cost-structure-summary.csv` (3,544 rows)
| Column | Meaning |
|---|---|
| `fiscal_year`, `dimension`, `category`, `size_band`, `metric` | `dimension` ∈ `all`, `category`, `size_band`, `category_x_size_band`, `elasticity`, `daf_cost_pool`, `grant_count_anchor`. Metrics ending `_level` are distributions of absolute dollars or headcount |
| `n`, `p25`, `median`, `p75` | Distribution across analysable sponsor-years (exclusions §2.2) |
| `aggregate_ratio`, `numerator_sum`, `denominator_sum` | Σ/Σ ratio, scaled as the metric. For `daf_cost_pool`, aggregate = bps of DAF assets, and `median` holds the Σ/Σ cost per DAF account |
| `elasticity`, `r2` | Log-log OLS (elasticity rows) |
| `staff_cost_per_grant`, `it_per_grant`, `outside_services_ex_invest_per_grant` | Grant-anchor rows only |
| `note` | Specification, or sources and period gap |

### `data/mission-2026-11-14/market-sensitivity-givinga-sdg.csv` (42 rows; 7 variants × FY2019–2024)
| Column | Meaning |
|---|---|
| `variant` | `published`, `published_excl_givinga`, `published_excl_givinga_and_imputed_paypal`, `corrected`, `corrected_excl_givinga`, `published_plus_sdg`, `corrected_plus_sdg` |
| `sponsors`, `accounts`, `processor_accounts`, `non_processor_accounts`, `processor_share_accounts`, `assets`, `processor_share_assets`, `contributions`, `grants` | Totals (processor = DAFRC subtype "Donation Processor") |
| `avg_assets_per_account`, `avg_assets_per_non_processor_account`, `assets_growth_yoy`, `accounts_growth_yoy`, `payout_grants_over_prior_assets` | Derived |
| `cr1_assets`, `cr5_assets`, `cr10_assets`, `hhi_assets`, `sdg_asset_rank` | Concentration of DAF assets |
| `givinga_accounts_published`, `givinga_assets_published`, `givinga_accounts_source`, `sdg_assets_added`, `paypal_accounts_imputed_this_fy`, `sources` | Context |

### `data/mission-2026-11-14/queue-proposals-cost-structure.csv`
Six proposals, P-COST-01 to P-COST-06, in the format of `queue-proposals-README.md`.

### Reproduce
```
python3 scripts/mission_sponsor_cost_structure.py --cache-dir CACHE --fetch --task all   # first run: ~1.8 GB of XML streamed, 24 threads
python3 scripts/mission_sponsor_cost_structure.py --cache-dir CACHE --task all           # offline re-run from the JSON cache
```
