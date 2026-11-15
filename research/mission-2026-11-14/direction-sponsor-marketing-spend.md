# Sponsor marketing spend: Form 990 Part IX line 12 against Schedule D growth, TY2021–2025

**Date:** 2026-11-15 · **Agent:** batch43 N23 · **Queue item:** P-NEW-MKT-01 (owner direction, 2026-11-15)

**Outputs**
- [`data/mission-2026-11-14/sponsor-marketing-spend-2021-2025.csv`](../../data/mission-2026-11-14/sponsor-marketing-spend-2021-2025.csv): 476 rows. There are 438 sponsor-year return rows, 30 group × tax-year rows and 8 pooled TY2021–24 group rows.
- [`data/mission-2026-11-14/queue-proposals-batch43-n23.csv`](../../data/mission-2026-11-14/queue-proposals-batch43-n23.csv): P-B43N23-01 to -03.
- **Script** (stdlib, functional style): [`scripts/mission_sponsor_marketing.py`](../../scripts/mission_sponsor_marketing.py).
  - It reuses the number, CSV and XML helpers in `mission_990_contractors.py`, and the Part IX group map and `part_ix_from` in `mission_sponsor_cost_structure.py`.
  - It checks every line-12 value against the cost-structure JSON cache: 290 returns match, 0 mismatch, and 148 are not in that cache (mostly TY2021 calendar-year returns, which the harvest did not cover).
  - Its JSON printout (stdout and stderr) is the source of every figure below.

**Conventions**
- **Tax year (TY)** = the year the return's period *begins*, read from the XML header (IRS convention). A June-2022 year end is therefore TY2021.
- **Recency:** TY2021 onward. The only earlier value used is the DAFRC FY2020/FY2021 account count that serves as the starting stock for a sponsor's first TY2021 year.
- **Labels:** **[F]** filed value; **[C]** script computation; **[I]** inference or classification.
- **bps of DAF contributions** = line 12 ÷ Schedule D Part I line 2 (contributions to DAFs) × 10,000. 1 bp = $0.0001 of advertising per $1 contributed, so 10 bps = $1 per $1,000.
- **Governing corrections read first:**
  - [sponsor-cost-structure-and-sensitivities.md](sponsor-cost-structure-and-sensitivities.md), wave 5:
    - Servant Foundation's line 12 is campaign spending, not overhead. It is excluded from every group statistic and kept in the rows with the flag `campaign_advertising_not_overhead`.
    - The operating-cost definition (line 25 less lines 1–4 and 11f) is used unchanged.
  - [queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md), wave 21, and its §1.3 reading:
    - Account growth must not rest on micro-account processors.
    - Givinga, PayPal Giving Fund and AOGF carry `account_unit_undefined` and are left out of every per-account statistic, which is the A2 basis.
    - None of the wave 21 textual corrections touch the figures used here.
- **Access:**
  - robots.txt was read on 2026-11-15. `gt990datalake-rawdata.s3.amazonaws.com` returns 404 (no rules). The XML was streamed and parsing stopped after Schedule D.
  - IRS TEOS indexes 2021–2026 and the eight TEOS zip members came from earlier batches' caches, so apps.irs.gov was not fetched.
  - No logins and no contact with anyone.
- This is research, not tax or legal advice.

---

## 1. Bottom line

1. **Reported advertising is tiny for nationals and visible mainly at community foundations.** Pooled TY2021–24, line 12 per $ of new DAF money **[C]**:

   | Group | Line 12 | Line 12 per $ contributed |
   |---|---|---|
   | Affiliated-commercial nationals (13) | $21.7m | 1.39 bps |
   | Independent nationals (12, ex-Servant) | $3.1m | 0.41 bps |
   | Digital-first (7) | $0.17m | 1.70 bps |
   | Processors (3) | $0.12m | 0.10 bps |
   | Community foundations (55), whole organisation | $67.2m | **18.4 bps** |
   | Community foundations, allocated to DAFs by share of contributions | | 12.7 bps |

   - For digital-first sponsors, about 6.6 bps once Endaoment's "Sales & marketing" on line 24 is added.
   - The median sponsor in every national group reports **$0** on line 12. Only 13 of 52 affiliated-commercial and 17 of 48 independent sponsor-years report any.
2. **One sponsor is almost the whole national total.** Schwab Charitable (EIN 31-1640316) reports $20.3m of the affiliated group's $21.7m. That is 5.4 bps of its DAF contributions and about **$390 per net new account**, and it is 97% in the fundraising column **[F/C]**.
   - Without Schwab, the affiliated group is **0.11 bps** and about **$14 per net new account**.
   - Fidelity Charitable reports **$0** on line 12 in every year. Its administrator fees on line 11a are $121–180m a year **[F]**.
3. **Cost per net new account [C]:**
   - Community foundations are highest: Σ line 12 ÷ Σ positive account change = **$7,981**. Allocated to DAFs, it is $5,237. The median sponsor over TY2021–24 is $12,406.
   - The other groups:

     | Sponsor or group | Per net new account |
     |---|---|
     | Affiliated-commercial group | $147 |
     | Schwab | $390 |
     | Vanguard | $253 |
     | Independent nationals | $64 |
     | NPT | $254 |
     | Independent Charitable Gift Fund | $195 |
     | Endaoment (line 12 only) | $103 |
     | Endaoment (with line-24 marketing) | $648 |
     | Daffy (TY2022–24) | $4 |

   - The CF figure is high mainly because CF accounts grow slowly (median +8.3% over three years) and CF advertising also serves non-DAF programs.
4. **More advertising does not go with faster growth in this cross-section [C/I].**
   - Across the 55 community foundations, the Spearman rank correlation between advertising intensity (line 12 ÷ operating cost) and account growth over TY2021–24 is **−0.25**. Against growth in DAF contributions it is −0.04.
   - Across all 99 sponsors with a defined account unit it is −0.34.
   - This is a correlation with no controls. It does not show that advertising fails; the fastest-growing sponsors (Signatry, Daffy, Charityvest, Renaissance) are channel- or platform-led, not ad-led.
5. **The 990 does not show most national and digital acquisition spend. This is the main limit (§5).**
   - Affiliated nationals (Fidelity, Schwab, Vanguard, Goldman Sachs, Morgan Stanley, BofA, Raymond James and others) can have the parent firm pay for brand and adviser marketing.
   - Digital-first sponsors (Daffy, Charityvest, Givinga, GiveClear/TIFIN Give, GoFundMe.org, Goodstack) run on platform companies whose marketing sits off the charity's return.
   - Each such row carries a flag and an `outside_990_marketing_basis` text. Read nationals' and digital sponsors' line 12 as a **lower bound**, not as their marketing budget.

## 2. Method

### 2.1 Universe (109 sponsors; 108 with Form 990 rows)
- **Top 100 by FY2024 DAF assets:** the `fy2024_asset_rank` field of `form990-returns-schedule-d-harvest-full.csv` (DAFRC FY2024 values).
- **Digital-first:** the repo's list (batch 35; `digital-sponsor-entities-2026.csv`): Daffy, Charityvest, Endaoment, Givinga, GiveClear (TIFIN Give), and Percent Impact Foundation (Goodstack). GoFundMe.org (GoFundMe Giving Funds) is added as the batch-35 app comparator.
  - Every.org files Form 990-PF, which has no line 12, so it has no rows.
- **Comparator:** PayPal Giving Fund, in the processor group.

### 2.2 Sponsor groups [I]

| Group | Members (n) | Rule |
|---|---|---|
| `affiliated_commercial_national` | Fidelity, Schwab (Donor Advised Charitable Giving Inc), Vanguard, GS DAPF, Goldman Sachs CGF, Ayco, Morgan Stanley GIFT, BofA CGF, Raymond James, Bessemer, T. Rowe Price, Stifel, Johnson CGF (13) | Named for, and branded with, a for-profit financial firm |
| `independent_national` | NPT, AEF, Renaissance, ImpactAssets, Greater Horizons, US Charitable Gift Trust, Servant, American Gift Fund, Independent CGF, CAF America, Impact Investing Charitable Trust, Signatry, FJC (13; Servant excluded from statistics) | DAFRC "National", no commercial parent in name or branding. US Charitable Gift Trust, Independent CGF and Impact Investing CT are flagged "affiliation not checked". Greater Horizons is a Greater Kansas City CF affiliate |
| `digital_first` | the seven above | Repo list |
| `community_foundation` | 55 | DAFRC type |
| `processor` | Dechomai, AOGF, PPGF (3) | DAFRC "Donation Processor", not on the digital list |
| `single_issue` | 17 rows: 13 analysed, plus 4 university/hospital entities (Stanford, UCLA Foundation, Université de Montréal, Notre Dame) excluded as whole-institution advertising, as in the cost-structure work | DAFRC "Single Issue Charity" |

### 2.3 Returns
- All Form 990 filings for these EINs in IRS TEOS indexes 2021–2026 with a period ending 2021-12 or later: 455 filings, all parsed.
  - Of the 438 rows kept, 430 were streamed from the GivingTuesday mirror.
  - The other 8 are TEOS zip members already cached by batches 35/38 (not mirrored).
  - Parsing stops after Schedule D.
- One row per sponsor and TY. The longest period is kept, then the latest `ReturnTs`, so an amendment beats the original even when its object ID is lower (Givinga CY2024). 17 superseded filings were dropped.
- **Coverage:** TY2021 107 sponsors · TY2022 107 · TY2023 108 · TY2024 108 · **TY2025 8** (index Last-Modified 2026-10-21; most CY2025 returns are not yet indexed).
  - TY2025 is reported but left out of the pooled statistics.
  - Two rows are 6-month periods (flag `short_or_long_period`).

### 2.4 Fields
- **Line 12 Advertising and promotion:** total, program, management and fundraising columns.
- **Line 11:** a management, b legal, c accounting, d lobbying, e professional fundraising, f investment management, g other.
- **Line 14:** information technology, all columns.
- **Line 25** and operating cost excluding line 11f.
- **Line 24 "other expenses" descriptions** are scanned for marketing wording:
  - *strict*: market, advertis, promot, brand, sponsorship, public relation, "/PR";
  - *broad*: communications, outreach, media, donor engagement/development, events;
  - false positives excluded: "fiscal sponsorship", "grant", "telephone", "board communications".
  - `adv_plus_l24_strict` = line 12 + strict line-24 amounts.
- **Schedule D Part I:** DAF count, contributions, grants, EOY value. **Part I:** total contributions (line 8).

### 2.5 Growth and cost ratios
- **Net new accounts** = Schedule D count(TY) − count(TY−1).
  - The prior count is the sponsor's previous return in the set.
  - For the first year it is the DAFRC row for the fiscal year before the period end. That row is flagged `prior_count_from_dafrc` and is filed in all but Endaoment's FY2021 row, whose source is "NPT historical data".
- **Cost per net new account** is defined only when the change is positive and the account unit is defined (A2 basis).
  - The group value is Σ line 12 ÷ Σ net new accounts over qualifying rows. The median is per sponsor-year.
  - For the pooled per-sponsor view, a sponsor with no starting stock (Daffy) starts from its TY2021 EOY count, and TY2021 spend is dropped from that ratio.
- **Allocation:** whole-organisation line 12 × DAF share of contributions (Schedule D line 2 ÷ Part I line 8, clipped to [0, 1]).
  - This matters for community and single-issue sponsors.
  - Some nationals report Schedule D contributions above Part I line 8 (flag `daf_contrib_gt_total_contrib`); the clip sets their share to 1.
- **Blank line 12** counts as $0 in sums, flagged `l12_blank`. 94 of 438 rows are blank, 34 are $0 and 310 are positive.

## 3. Results

### 3.1 By group, TY2021 and TY2024, and pooled TY2021–24 [C]

| Group | TY | Returns (line 12 > 0) | Line 12 total | Split prog / mgmt / FR (pooled) | DAF contributions | bps of DAF contributions (Σ/Σ; median) | Allocated bps | Σ net new accounts (rows) | Line 12 per net new account (Σ/Σ; allocated) |
|---|---|---|---|---|---|---|---|---|---|
| Affiliated-commercial | 2021 | 13 (3) | $3.04m | | $35.6bn | 0.85; 0 | 0.97 | 41,124 (12) | $74 |
| | 2024 | 13 (4) | $7.28m | | $55.9bn | 1.30; 0 | 1.43 | 47,117 (13) | $154 |
| | **pooled** | 52 (13) | **$21.7m** | 2% / 1% / 97% | $156.3bn | **1.39**; 0 | 1.54 | 147,709 (51) | **$147**; $147 |
| — ex-Schwab | pooled | 48 (9) | $1.36m | 39% / 10% / 51% | $118.8bn | **0.11**; 0 | 0.13 | 95,522 (47) | **$14** |
| Independent nationals | 2021 | 12 (4) | $1.05m | | $19.6bn | 0.54; 0 | 0.53 | 13,236 (10) | $41 |
| | 2024 | 12 (5) | $0.63m | | $23.1bn | 0.27; 0 | 0.32 | 12,837 (10) | $49 |
| | **pooled** | 48 (17) | **$3.15m** ($3.59m with line 24) | 23% / 11% / 67% | $76.6bn | **0.41**; 0 | 0.46 | 40,895 (42) | **$64** |
| Digital-first | 2021 | 6 (2) | $0.003m ($0.22m with line 24) | | $0.10bn | 0.28; 0 | 0.03 | 6,101 (2) | $0 |
| | 2024 | 7 (3) | $0.056m | | $0.56bn | 1.01; 0 | 0.89 | 6,705 (2) | $0.18 |
| | **pooled** | 26 (10) | **$0.17m** ($0.65m with line 24) | 1% / 18% / 81% | $0.99bn | **1.70**; 0 | 2.07 | 28,194 (10) | **$3.54** |
| Community foundations | 2021 | 55 (48) | $13.8m | | $11.1bn | 11.9; 18.5 | 7.9 | 1,898 (43) | $5,060; $3,078 |
| | 2024 | 55 (50) | $19.8m | | $9.6bn | 20.7; 21.8 | 14.0 | 1,505 (40) | $9,417; $6,393 |
| | **pooled** | 220 (196) | **$67.2m** ($71.3m with line 24) | 38% / 36% / 26% | $36.0bn | **18.4**; 22.3 | **12.7** | 5,792 (159) | **$7,981**; $5,237 |
| Processors (A2: no per-account) | pooled | 12 (5) | $0.12m | 0% / 2% / 98% | $12.8bn | 0.10; 0 | 0.15 | n/a | n/a |
| Single-issue (ex-university) | pooled | 52 (44) | $16.8m | 17% / 32% / 51% | $21.6bn | 7.8; 5.7 | 9.8 | 14,422 (40) | $948; $754 |
| All (ex-PPGF) | pooled | 406 (281) | $109.1m | 27% / 28% / 45% | $302.2bn | 3.57; 5.03 | 3.16 | 237,253 (306) | $355; $277 |

- Line 12 rose from TY2021 to TY2024 in the affiliated group (+139%, almost all Schwab) and at community foundations (+44%). It fell at independent nationals (−40%).
- **Related lines, pooled TY2021–24 [F/C]:**

| Group | Line 11a management | Line 11f investment management | Line 11g other | Line 14 IT | Line 11b legal | Line 11c accounting |
|---|---|---|---|---|---|---|
| Affiliated-commercial | $616.3m (mostly Fidelity's administrator fees) | $625.3m | $72.1m | $138.4m | $7.6m | $12.4m |
| Independent | $26.4m | $479.3m | $119.4m | $30.8m | $8.2m | $19.5m |
| Community foundations | $62.4m | $868.3m | $497.1m | $139.7m | $27.8m | $30.6m |
| Digital-first | $0.14m | $1.69m | $2.20m | $1.08m | $0.65m | $1.05m |

  - Line 12 is 1.75% of affiliated operating cost (excluding 11f), 0.36% of independent, 0.35% of digital-first and 2.0% of community-foundation operating cost.

### 3.2 Nationals and digital-first, per sponsor, pooled TY2021–24 [F/C]

| Sponsor | Line 12 (with line 24) | bps of DAF contributions | Accounts: start → TY2024 (growth) | Line 12 per net new account | Note |
|---|---|---|---|---|---|
| Schwab Charitable | $20.34m | 5.43 | 76,310 → 128,497 (+68%) | **$390** | 100% fundraising column; $2.65m → $6.88m a year |
| Vanguard Charitable | $1.33m | 0.79 | 24,034 → 29,305 (+22%) | $253 | 40/10/50 split |
| NPT | $2.13m ($2.57m) | 0.41 (0.49) | 12,298 → 20,691 (+68%) | $254 ($306) | Line 24 "Public relations" TY2022–23 |
| Independent Charitable Gift Fund | $0.24m | 3.93 | 240 → 1,469 (+512%) | $195 | |
| CAF America | $0.60m | 2.01 | 742 → 740 | n/a (≤ 0) | |
| AEF | $0.11m | 0.17 | 10,306 → 15,947 (+55%) | $20 | Line 12 first reported TY2024 |
| Renaissance | $0.04m | 0.07 | 10,119 → 25,824 (+155%) | $3 | White-label administrator |
| Stifel / T. Rowe Price / FJC | $0.008m / $0.021m / $0.019m | 0.15 / 0.39 / 1.10 | +1,072 / +561 / +179 | $7 / $37 / $107 | |
| Fidelity, GS DAPF, Goldman Sachs CGF, Ayco, Raymond James, Morgan Stanley GIFT, BofA CGF, Bessemer, Johnson CGF | $0 (reported 0 or blank) | 0 | Fidelity 160,403 → 224,884 (+40%); Morgan Stanley +95%; GS DAPF +96% | $0 | Parent-paid marketing likely (§5) |
| ImpactAssets, US CGT, American Gift Fund, Signatry, Greater Horizons, Impact Investing CT | $0 | 0 | Signatry 74 → 2,564 | $0 | |
| Endaoment | $0.09m (**$0.57m**) | 8.66 (**54.6**) | 331 → 1,213 (+266%) | $103 (**$648**) | "Sales & marketing" on line 24 in TY2021–22 ($216k, $265k); line 12 from TY2023 |
| Daffy | $0.036m | 1.08 | 577 (TY2021 EOY) → 8,905 | $4 | Membership fees go to the platform |
| GoFundMe.org | $0.042m | 82.0 | 1 pooled fund | n/a | 70% management column |
| Charityvest | $0 | 0 | 4,346 → 18,427 (+324%) | $0 | Line 24 "platform fee" $507k (TY2023) and $653k (TY2024), payee not named |
| GiveClear (TIFIN Give) | $0 | 0 | 52 → 228 | $0 | Contributions $0.54m → $210m |
| Givinga | $0 | 0 | account unit undefined | excluded | Line 11e professional fundraising $5.5m / $18.6m / $5.2m (TY2021–23) [F] |
| Percent Impact (Goodstack) | $0 | 0 | 7,268 (TY2024) | n/a | |
| PPGF (comparator) | $0.12m | 0.63 | account unit undefined | excluded | 98% fundraising column |

- **Reading [I]:** Givinga's line 11e (paid fundraisers, mainly game and app fundraising; cost-structure §5) is the clearest filed acquisition cost among the digital sponsors, but it buys gifts and not ongoing-advisory accounts (batch 36 A2). Charityvest's platform fee and Daffy's membership fees route the platform's costs, marketing included, outside the charity's Part IX.

### 3.3 Community foundations [F/C]
- **Pooled per-sponsor medians (55 CFs):**
  - line 12 is 1.55% of operating cost and 26.5 bps of DAF contributions;
  - $12,406 per net new account;
  - accounts grew 8.3% over TY2021–24.
- **Largest line 12, pooled:**

| Sponsor | Line 12 | Per net new account | Notes |
|---|---|---|---|
| New York Community Trust | $6.69m | n/a (−54 accounts) | 173.5 bps of DAF contributions; 7.4% of opex |
| Silicon Valley CF | $6.01m | n/a (−142 accounts) | 6.0 bps |
| Oregon CF | $3.97m | $22,697 | |
| Pittsburgh Foundation | $3.39m | $49,898 | |
| Foundation for the Carolinas | $3.34m | $32,783 | |
| Boston Foundation | $3.17m | $27,825 | |
| Communities Foundation of Texas | $2.94m | $59,952 | |
| Rhode Island Foundation | $2.49m | $178,156 | |

- The CF functional split is balanced (38% program, 36% management, 26% fundraising). CF advertising serves community programs and the foundation's brand as well as donor acquisition, which is why the allocated figures (12.7 bps; $5,237 per account) are the fairer comparison.
- Line-24 marketing adds $4.1m pooled, including:
  - Austin CF "Marketing & communications" ($141k, $201k);
  - CF of North Texas "Marketing and outside P…";
  - sponsorship lines at Arizona, Seattle and East Bay;
  - Chicago Community Trust "Public relations consultant" ($370k, TY2021);
  - Greater New Orleans "Development/PR" ($30–79k).
  - Tulsa CF's "Hunger Free Oklahoma PR…" line ($4.3m, TY2022) is a program pass-through. The final pattern excludes it.
- **Rank correlations (Spearman, line 12 ÷ opex) [C]:**

| Sample | Against account growth | Against DAF-contribution growth |
|---|---|---|
| CFs | −0.25 (n = 55) | −0.04 (n = 53) |
| All sponsors | −0.34 (n = 99) | −0.19 (n = 97) |

  - Many sponsors report $0, so ties are frequent.

## 4. What this means for the landscape [I]
- **Nationals compete on distribution, not on charity-paid advertising.** The national DAF market grew by adviser channel, brokerage platform and white-label administration. Schwab is the only large national that books substantial paid media on its own 990.
  - An entrant cannot read competitors' acquisition budgets from the 990. It can read that the nationals' marginal acquisition cost **charged to the charity** is near zero: their parents carry it.
- **Community foundations spend far more per $ contributed than nationals on reported advertising.**
  - CFs allocated (12.7 bps) are about 9 times the affiliated group (1.39 bps).
  - CFs unallocated (18.4 bps) are about 45 times the independent nationals (0.41 bps).
  - Their cost per net new DAF is in the thousands of dollars.
  - This is consistent with the cost-structure finding that CFs spend 127–177 bps on DAF-allocated operating cost.
  - It also suggests a market for shared or white-label donor acquisition (adviser outreach, content, referral programs) among CFs.
- **Digital-first sponsors report almost nothing because their costs sit in the platform company.** Unit acquisition economics for Daffy, Charityvest or TIFIN Give therefore cannot be derived from public 990s. Proposal P-B43N23-02 sets out what can be.

## 5. Limitations
- **Affiliate-paid and platform-paid marketing (labelled in every row):**
  - `affiliate_paid_marketing_possible` covers the 13 affiliated-commercial nationals. Parent firms (FMR, Schwab, Vanguard, Goldman Sachs, Morgan Stanley, Bank of America, Raymond James and others) may pay brand, adviser and digital marketing directly, or recover it through administrator fees (line 11a; Fidelity $121–180m a year) or fund expense ratios. Neither route reaches line 12. Fidelity's $0 does **not** mean Fidelity Charitable is not marketed.
  - `platform_paid_marketing_possible` covers Daffy, Charityvest, Givinga, GiveClear, GoFundMe.org, Goodstack, PPGF and AOGF. Each has an `outside_990_marketing_basis` sentence ([F] where the repo has a filed or published basis, [I] otherwise).
- **Line 12 is defined narrowly.** Staff time on marketing (lines 5–10), agency fees (line 11g), events (line 24), and adviser commissions or revenue-share are all excluded. The line-24 scan adds only line items that are labelled as marketing.
- **Whole-organisation figures.** CF and single-issue advertising also serves non-DAF programs, so the allocated variant is shown. Allocation by contribution share is a proxy.
- **Account counts:**
  - Schedule D counts are year-end stocks, so net new accounts = openings − closures. Gross openings are not filed, so cost per *gross* new account would be lower.
  - The first-year prior comes from DAFRC (flagged).
  - Givinga, PPGF and AOGF are excluded from per-account statistics (batch 36 A2 basis). GoFundMe.org reports a single pooled fund.
- **Timing.** Advertising may drive growth with a lag. The ratios are same-year and the rank tests are cross-sectional without controls.
- **TY2025** has only 8 returns and is not used in pooled statistics.
- **Classification.** The affiliated, independent and digital grouping is a judgement [I]. Three nationals' affiliations were not checked (flagged).
- **No invented values.** Every number is a filed XML value, a DAFRC dataset value, or a computation on them.

## 6. Data dictionary — `sponsor-marketing-spend-2021-2025.csv`

| Column(s) | Meaning |
|---|---|
| `row_type` | `return` (one sponsor-year), `group_year` (group × TY), `group_pooled` (group, TY2021–2024) |
| `ein`, `sponsor_name`, `dafrc_type`, `dafrc_subtype`, `fy2024_asset_rank` | Sponsor identity; DAFRC FY2024 rank and type |
| `sponsor_group`, `group_basis`, `selection` | Group (§2.2) and why; `top100_fy2024_daf_assets`, `digital_first` or `comparator`. Group rows also use `affiliated_commercial_national_ex_schwab` and `all_ex_comparator` |
| `tax_year`, `tax_period_begin`, `tax_period_end`, `period_months` | TY = year the period begins (header). Group rows: the TY or `2021-2024` |
| `return_object_id`, `return_ts`, `amended_ind`, `xml_source`, `xml_url` | Evidence: `gt_mirror` (URL) or `teos_zip_member_cached` (member file name) |
| `adv_l12_total`, `adv_l12_program`, `adv_l12_mgmt`, `adv_l12_fundraising` | Part IX line 12, columns A–D (blank = not reported) |
| `adv_l12_cost_cache_check` | Line 12 against the `mission_sponsor_cost_structure.py` cache: `match`, `mismatch` or `not_in_cost_cache` |
| `l24_marketing_strict_amt`, `l24_marketing_strict_desc`, `l24_marketing_broad_amt`, `l24_marketing_broad_desc` | Line 24 items whose description matches marketing wording (§2.4); `desc=amount` list |
| `adv_plus_l24_strict` | Line 12 + strict line-24 marketing |
| `fees_mgmt_l11a` … `fees_other_l11g`, `fees_l11_total` | Line 11a–g totals (column A) and their sum |
| `it_l14_total`, `it_l14_program`, `it_l14_mgmt`, `it_l14_fundraising` | Line 14 by column |
| `total_functional_expenses_l25`, `fundraising_col_l25`, `operating_cost_ex_invest`, `adv_share_of_opex` | Line 25(A), 25(D); line 25 − lines 1–4 − 11f; line 12 ÷ that |
| `total_contributions_part_i`, `total_assets_eoy`, `employees` | Part I line 8, line 20 EOY, line 5 |
| `sd_present`, `sd_daf_count`, `sd_daf_contributions`, `sd_daf_grants`, `sd_daf_eoy_value` | Schedule D Part I, column (a) |
| `daf_share_of_contributions` | Schedule D line 2 ÷ Part I line 8, clipped to [0, 1] |
| `prior_daf_count`, `prior_count_source`, `net_new_accounts`, `account_growth_pct` | Prior count (`prior_return` or `dafrc_fy{FY}:{source}`); change; change ÷ prior |
| `adv_per_dollar_daf_contrib`, `adv_bps_of_daf_contrib`, `adv_bps_of_total_contrib` | Line 12 per $ of DAF contributions (also in bps) and in bps of all contributions |
| `adv_alloc_daf`, `adv_alloc_per_new_dollar_bps` | Line 12 × DAF share; ÷ DAF contributions in bps |
| `adv_per_net_new_account`, `adv_alloc_per_net_new_account` | Defined only when net new accounts > 0 |
| `outside_990_marketing_basis` | Why marketing may be paid off this 990 (parent or platform), with [F]/[I] |
| `quality_flags` | `affiliate_paid_marketing_possible`, `platform_paid_marketing_possible`, `account_unit_undefined`, `campaign_advertising_not_overhead`, `university_health_whole_org`, `pooled_single_fund`, `short_or_long_period`, `amended_return`, `sched_d_blank`, `prior_count_from_dafrc`, `net_new_accounts_le_0`, `l12_blank`, `l24_marketing_lines`, `daf_contrib_gt_total_contrib` |
| Group rows: `n_returns`, `n_sponsors`, `n_l12_positive`, `share_l12_positive` | Analysable rows (Servant and university/hospital rows excluded) |
| Group rows: sums of the line columns | Σ over analysable rows; blank = 0 |
| Group rows: `adv_bps_of_daf_contrib` (Σ/Σ), `adv_bps_of_daf_contrib_median`, `_p25`, `_p75` | Over rows with DAF contributions > 0 |
| Group rows: `net_new_accounts`, `n_returns_net_new_positive`, `adv_per_net_new_account` (Σ/Σ), `adv_per_net_new_account_median`, `adv_alloc_per_net_new_account` | Over rows with a positive change and a defined account unit |

## 7. Reproduction
```
python3 scripts/mission_sponsor_marketing.py --irs-dir IRS --cache-dir CACHE --cost-cache COSTCACHE \
    --teos-dir B35/work/teos --teos-dir B38/work/teos --teos-dir V22/work/teos --fetch
```
- IRS holds `index_2021.csv` to `index_2026.csv`. CACHE receives `extract990mkt/{OID}.json` (about 2 MB for 455 returns).
- COSTCACHE holds the `extract990cost/` cache of `mission_sponsor_cost_structure.py`.
- A re-run without `--fetch` works offline from CACHE. The first run streamed the mirrored returns in about 20 seconds because parsing stops after Schedule D.
