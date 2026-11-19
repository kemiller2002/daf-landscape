# Recipient-side follow-ups: DAF share on an individual-giving basis, and Charity Navigator rating eligibility of DAF dollars (P-B40N1202-03, P-B43N26-02)

**Date:** 2026-11-19 · **Task ID:** b40n1202-b43n26 · **Builds on:** [b40n12-daf-share-of-recipient-revenue.md](b40n12-daf-share-of-recipient-revenue.md) (P-B40N12-02) and its wave 33A corrections ([validation-wave33a-report.md](validation-wave33a-report.md))

**Outputs**
- Script: [`scripts/mission_recipient_basis_eligibility.py`](../../scripts/mission_recipient_basis_eligibility.py). It is new; `mission_daf_share_recipient_revenue.py` is imported, not modified.
- Data (A): [`data/mission-2026-11-14/daf-share-individual-basis-2026-11-19.csv`](../../data/mission-2026-11-14/daf-share-individual-basis-2026-11-19.csv). 126 summary rows (21 scopes × 6 denominator bases) and 2,352 sampled-recipient rows.
- Data (B): [`data/mission-2026-11-14/charity-rating-eligibility-share-2026-11-19.csv`](../../data/mission-2026-11-14/charity-rating-eligibility-share-2026-11-19.csv). 331 rows.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b40n1202-b43n26.csv`](../../data/mission-2026-11-14/queue-proposals-b40n1202-b43n26.csv)

Tags: [F] computed from filings by the script · [P] quoted primary source · [I] inference.

## 0. Answer in brief

**(A) DAF share on a denominator closer to individual giving**
- **Line 1f is where DAF grants are reported.** The IRS instructions say 1f "includes contributions from donor advised funds (unless the sponsoring organization is a related organization)" [P]. Part VIII cannot separate individuals from foundations and corporations: all three sit in 1f.
- **The closest basis the form allows** is 1a + 1b + 1c + 1f, which equals 1h − 1d − 1e: every contribution except government grants and related-organisation transfers. It is still a superset of individual giving, so shares on it are lower bounds against an "individual revenue" denominator [I].
- **The mix of line 1h** for weighted 990 filers, pooled: 1f 62.0%, 1e 31.7%, 1c 2.8%, 1d 2.0%, 1b 1.0%, 1a 0.5% [F]. Removing 1e is what moves the share; the other lines change it by under a point.
- **Headline, 1h − 1d − 1e basis** (all in-scope recipients, unscaled) [F]:
  - median **7.7%** (95% CI 5.9–8.9%);
  - pooled **10.3%** (9.2–11.7%);
  - on the 1h basis these were 5.9% and 6.9%, which reproduces the committed study.
- **Narrowest basis, 1f alone:** median 8.1% (6.4–9.7%), pooled 11.0% (9.8–12.5%) [F].
- **By size, 1h − 1d − 1e basis, pooled** [F]:
  - <$1m 21.0%; $1–5m 11.7%; $5–25m 12.5%; $25–100m 11.0%; ≥$100m 5.8%.
  - The large-recipient discount narrows sharply once government grants leave the denominator. ≥$100m goes from 3.7% to 5.8%; $25–100m from 6.3% to 11.0%.
- **Against Chariot's 12.6%** (pooled DAF share of "total giving", 54 nonprofits, about $97m of giving per participant-year):
  - The $25–100m band on 1h − 1d − 1e is 11.0% (10.0–12.3%) unscaled [F] and 16.4% scaled to all sponsors [I]. ≥$100m is 5.8% unscaled and 8.7% scaled [I].
  - All recipients: 10.3% unscaled [F], 15.4% scaled [I].
  - The repo's macro ratio of netted DAF grants to Giving USA individual giving is 14.88% (NPB097).
  - So unscaled, the filings sit just below Chariot. Scaled, they sit above it. The two numerators differ (top-50 Schedule I against CRM-coded gifts from all sponsors), so neither reading is like-for-like.
- **Against Chariot's 4–24% sector range of "individual revenue"** (line 1f basis, NTEE groups with ≥140 respondents):
  - Unscaled pooled shares run from 6.3% (international) to 19.3% (public and societal benefit) [F]. Scaled, 9.4–28.7% [I].
  - International still does not top the list. Chariot's 23.7% for International Relief is on total revenue [P].

**(B) Charity Navigator rating eligibility of top-50 DAF dollars**
- **The 2026 rules** [P]: a U.S. 501(c)(3) public charity, not a private foundation, subsidiary, revoked or inactive organisation; "at least three electronically filed IRS Form 990s within the past six years"; "at least two of the four most recent filings must be the standard Form 990"; the latest is not a 990-PF; functional expenses above zero, with program expenses not exceeding total; no "Giving Not Recommended" alert.
  - **The published rules contain no revenue threshold.** The 2023 release notes use revenue only to assign a "size classification" for scoring [P].
- **Result, central rule set** [F]: **76.9%** of top-50 FY2023–24 DAF-weighted Schedule I dollars ($56.93bn of $74.07bn) go to recipients that pass every rule CN publishes and filings can test. Those recipients are **51.2%** of recipient units (89,124 of 174,220). On the as-filed Schedule I basis the dollar share is 76.3%.
- **The remaining 23.1% of dollars:**
  - churches with no e-filed 990: 8.3%;
  - EINs not in the IRS BMF: 5.6%;
  - fewer than three e-filed returns in six years: 3.4%, of which Navigation Charitable Fund's $1.26bn is most;
  - private foundations: 1.7%;
  - other non-filers: 1.4%;
  - group-return subordinates: 0.9%;
  - blank-EIN lines: 0.5%;
  - 990-EZ filers that fail the two-full-990 rule: 0.5% of dollars but **7.3% of recipients**;
  - national and processor DAF sponsors: 0.5%.
- **By size, the dollar share is ≥89.6% in every BMF revenue band from $1m up, but 28.3% under $1m** [F]. That band holds the churches, whose BMF revenue is blank.
- **By sector** [F]:
  - religion is 34.0% eligible by dollars; 55.4% of its dollars go to churches with no e-filed 990;
  - no-NTEE recipients are 49.4%;
  - public and societal benefit is 76.4%, the Navigation line again;
  - every other major group is 89.5–96.2%.
- **Variants** [F]:
  - Applying the filing rules to every DAF-sponsor EIN raises the share to 77.3%.
  - Also excluding community foundations changes nothing (76.9%): every community foundation recipient line is already removed as DAF-to-DAF.
  - Counting the six-year window by IRS processing year instead of tax year gives 76.9%.

## 1. Method

### 1.1 Shared numerator

The numerator is the committed study's, imported unchanged from `mission_daf_share_recipient_revenue.py`:
- top-50 DAFRC sponsors by FY2024 DAF assets;
- 94 itemising sponsor-years of Schedule I Part II lines for FY2023–24;
- filer totals rows dropped, and DAF-to-DAF lines dropped (whitelist EINs, self-lines, unique whitelisted-name matches);
- `daf_weighted` = each sponsor-year's lines × its DAF share of grants.

The run reproduces the committed totals [F]:
- 170,569 recipient EINs;
- frame of 138,832 EINs;
- sample of 2,352 EINs;
- 4,315 recipient returns;
- coverage scale of 0.6727 (FY2024 top-50 DAF-weighted ÷ netted DAFRC central).

### 1.2 (A) Part VIII lines 1a–1h

- **Sample and returns.** The same sample (seed 20261119) and the same return choice: the latest object id per tax period, then the latest period per FY 2023 and 2024, taken from the IRS TEOS index files for 2023–2026.
- **Reading returns.** Each of the 4,315 returns was re-read in full from the GivingTuesday mirror of IRS TEOS XML: 4,314 parsed and 1 returned HTTP 404 [F]. A new cache holds the values (`q1226/f990p8/`). The committed `q1202/f990/` cache keeps only 1h and 1e, so it could not be reused.
- **Fields read.** The direct children of the `IRS990` element are read: `FederatedCampaignsAmt` (1a), `MembershipDuesAmt` (1b), `FundraisingAmt` (1c), `RelatedOrganizationsAmt` (1d), `GovernmentGrantsAmt` (1e), `AllOtherContributionsAmt` (1f), `NoncashContributionsAmt` (1g) and `TotalContributionsAmt` (1h).
  - Only direct children are read because `FundraisingAmt` also appears inside every Part IX expense group. For example, IRC's 2024 return 202401579349301440 has `FundraisingAmt` 144,290 at line 1c and further values inside Part IX groups. A manual grep of that XML matched the cached values for 1a, 1c, 1e, 1f and 1h.
- **Check.** In every in-scope 990, lines 1a–1f sum to 1h within $1 (0 failures) [F].
- **990-EZ filers.** Line 1 cannot be split, so it is used unchanged on every basis. 113 of 2,170 respondents have at least one EZ year. A `form_990_only` scope is reported.
- **Bases.**

| Basis | Formula | Meaning |
|---|---|---|
| b1_1h | 1h | Total contributions. This is the committed study's basis. |
| b2_1h_less_1e | 1h − 1e | Private contributions. This was the committed study's sensitivity. |
| **b3_1abcf** | 1a + 1b + 1c + 1f (= 1h − 1d − 1e) | **Headline.** All contributions except government grants and related-organisation transfers. |
| b4_1bcf | 1b + 1c + 1f (= 1h − 1a − 1d − 1e) | The definition in the queue item. It also drops federated campaigns. |
| b5_1af | 1a + 1f | The task's example. |
| b6_1f | 1f | The line the IRS assigns DAF grants to. It is the narrowest basis. |

- **Why b3 is the headline [I].** Individuals give through 1a (indirectly, via United Way and similar campaigns), 1b (dues in excess of benefits), 1c (event payments above retail value) and 1f. Only 1d and 1e are by definition non-individual. Dropping 1b and 1c, as b4–b6 do, removes individual money but leaves foundation and corporate grants in 1f. That moves the denominator away from Chariot's basis, not toward it.
- **Non-positive denominators.** A recipient whose basis denominator is ≤0 is left out of that basis's statistics. The count and its numerator share are reported in `den_nonpos_*`: at most 36 respondents and 0.5% of weighted numerator dollars, on b6.
- **Wave 33A corrections applied:**
  1. The 9 EINs whose returns all parse but carry no 1h or EZ line 1 are out of scope (`no_contributions_line`), not missing. The weighted in-scope population falls from 96,228 to 95,875.
  2. A sensitivity scope `ex_leaked_daf_sponsors` drops sampled DAF sponsors that are outside the DAFRC panel. It matches 9 names, including Jewish federations (Los Angeles, Hartford, Houston, Chicago JUF, Youngstown, JFNA), NCF Wisconsin, NCF Real Property and Navigation Charitable Fund. UJA-Federation of New York (BMF name "UNITED JEWISH APPEAL FEDERATION OF JEWISH PHILANTHROPIES OF NY INC") does not match the regex, which is a limit.
  3. Medians are not divided by coverage. Only pooled shares are scaled, and they are tagged [I].
- **Statistics.** Weights, the weighted quantiles and the pooled ratio estimator are as in the committed study. Intervals come from a stratified bootstrap with 500 replicates and seeds offset per scope × basis. The 1h median interval is 5.3–7.6% here against 5.3–7.4% in the committed file, which used a different seed.

### 1.3 (B) Charity Navigator eligibility from filing data

**Rules as published.** These are quoted from the [CN help article "Charity Navigator's rating system"](https://intercom.help/charity-navigator/en/articles/8557824-charity-navigator-s-rating-system), dated April 9, 2026 and fetched 2026-11-19 [P]:
> "To receive an Encompass Rating, a nonprofit must be a U.S.-based 501(c)(3) public charity. Private foundations, nonprofit subsidiaries, and organizations with revoked or inactive IRS status are not eligible."
> "Charity Navigator must directly receive at least three electronically filed IRS Form 990s within the past six years (these do not need to be consecutive)."
> "At least two of the four most recent filings must be the standard Form 990, and the most recent filing cannot be a Form 990-PF."
> "Report total functional expenses greater than zero, with program expenses not exceeding total expenses."
> "Have no Charity Navigator "Giving Not Recommended" alert."
> "A charity may be listed but not rated if it does not yet meet Form 990 filing requirements, is newly registered, files only Form 990-EZ or 990-N, or is otherwise ineligible for an Encompass Rating."

The [release notes](https://www.charitynavigator.org/about-us/our-methodology/ratings/release-notes/) add two points [P]:
- Spring 2024: "Donor Advised Funds (DAF) Rating Eligibility - DAFs were determined to be ineligible for a rating due to their unusual financial structure."
- Fall 2023: "All eligible organizations are given a size classification based on their e-filed 990 data. Size classifications are based on annual revenue."

No revenue floor appears in any of the three CN pages read. The [Spring 2026 methodology update](https://intercom.help/charity-navigator/en/articles/14471517-spring-2026-rating-methodology-update) changes scoring, not eligibility. The linked "Rating Methodology Guide (Updated March 2026)" PDF returned HTTP 404.

**Applied as tests:**

| CN rule | Test | Data |
|---|---|---|
| U.S. 501(c)(3) | In the IRS EO BMF (eo1–eo4, eo_pr, eo_xx) and SUBSECTION = 03 | BMF |
| Not a private foundation | BMF FOUNDATION not 02, 03 or 04 | BMF |
| Revoked or inactive | Not in the BMF. The revocation list is not applied as a rule: 784 BMF EINs also have a revocation row with no reinstatement date, mostly organisations re-recognised under a new ruling. | BMF; revocation list (diagnostic) |
| DAFs ineligible | **Central:** DAFRC-panel EINs in the `national` and `processor` segments. **Strict:** also `community_foundation`. **Lenient:** none, filing rules only. Universities, hospitals and single-issue charities on the panel are never excluded on this ground. | DAFRC 2025 panel |
| ≥3 e-filed 990s in 6 years | ≥3 distinct tax periods of 990, 990-EZ or 990-PF with a tax period ending 2020–2025. The sensitivity uses IRS index (processing) year 2021–2026. Amended returns are collapsed to the latest object id per tax period. | TEOS index 2019–2026 |
| ≥2 of the 4 most recent are full 990s; latest is not a 990-PF | The four most recent tax periods, at any date | TEOS index |
| Expenses > 0 and program ≤ total | Tested only on the (A) sample's latest FY2023/24 full 990 | Part IX line 25 |
| No "Giving Not Recommended" alert; "nonprofit subsidiaries" | Not testable from filings | — |

- **Form type.** Taken from the DLN prefix: 93493 = 990, 93492 = 990-EZ, 93491 = 990-PF.
  - In all three index years checked (2019, 2020, 2024), this matches `RETURN_TYPE`. It also resolves the 2019–2020 labels: `990O` is 93493, a full 990; `990EO` is 93492, an EZ (one XML was checked: `ReturnTypeCd` 990EZ); and `990PR` is 93491.
  - 990-T rows (93393) are ignored.
- **Recipient units.**
  - Each recipient EIN with a positive non-DAF-to-DAF numerator is one unit (170,569).
  - Each distinct normalised name on blank-EIN lines is another (3,651). Two of these have a foreign address.
- **Sector and band.** BMF NTEE major group and BMF `REVENUE_AMT` band, the same mapping as the committed study.
  - BMF `REVENUE_AMT` is the IRS's transcription of the latest filed return's total revenue. It is used for the full universe because only the 2,352 sampled recipients have a 990 read here.

## 2. Results (A): DAF share by denominator basis

### 2.1 All in-scope recipients and sensitivities

All figures are [F] except the scaled column [I]. Percentages are weighted, and 95% intervals follow in parentheses.

| Scope | Basis | Respondents | Median | Pooled | Weighted ≥20% | Scaled pooled [I] |
|---|---|---|---|---|---|---|
| all | 1h | 2170 | 5.9 (5.3–7.6) | 6.9 (6.1–7.8) | 20.4 | 10.3 |
| all | 1h − 1e | 2160 | 7.6 (6.2–8.8) | 10.1 (9.0–11.4) | 23.1 | 15.0 |
| **all** | **1h − 1d − 1e** | **2145** | **7.7 (5.9–8.9)** | **10.3 (9.2–11.7)** | **23.2** | **15.4** |
| all | 1b + 1c + 1f | 2143 | 7.7 (6.2–8.9) | 10.4 (9.3–11.8) | 23.4 | 15.5 |
| all | 1a + 1f | 2139 | 8.1 (6.5–9.8) | 11.0 (9.5–12.5) | 26.0 | 16.3 |
| all | 1f | 2134 | 8.1 (6.4–9.7) | 11.0 (9.8–12.5) | 26.2 | 16.4 |
| form_990_only | 1h − 1d − 1e | 2032 | 5.8 (5.1–7.2) | 10.3 (9.0–11.6) | 18.8 | 15.3 |
| ex_leaked_daf_sponsors | 1h − 1d − 1e | 2136 | 7.7 (6.2–8.7) | 9.9 (8.9–11.1) | 22.8 | 14.8 |
| non_certainty_only | 1h − 1d − 1e | 1785 | 7.7 (6.1–8.9) | 8.8 (7.6–10.2) | 23.0 | 13.1 |
| ex NTEE T and fund/foundation/trust names | 1h − 1d − 1e | 1728 | 8.0 (6.3–9.4) | 9.4 (8.3–10.7) | 23.0 | 13.9 |
| ex_leaked_daf_sponsors | 1h | 2161 | 5.9 (5.2–7.3) | 6.6 (5.9–7.3) | 20.1 | 9.8 |

- The `ex_leaked_daf_sponsors` 1h row reproduces wave 33A's correction: pooled 6.6%, median unchanged at 5.9%.
- Dropping 990-EZ filers lowers the median (7.7% → 5.8%) but not the pooled share. EZ filers are small, high-share recipients.

### 2.2 By revenue band (BMF REVENUE_AMT)

| Band | Median, 1h | Median, 1h − 1d − 1e | Median, 1f | Pooled, 1h | **Pooled, 1h − 1d − 1e** | Pooled, 1f | Scaled pooled, 1h − 1d − 1e [I] |
|---|---|---|---|---|---|---|---|
| <$1m | 10.1 | 11.3 (8.5–14.4) | 11.4 | 17.8 | **21.0 (13.6–30.1)** | 22.1 | 31.2 |
| $1–5m | 3.5 | 5.0 (3.9–6.2) | 5.7 | 9.5 | **11.7 (8.7–14.8)** | 12.7 | 17.3 |
| $5–25m | 3.2 | 5.7 (4.8–7.4) | 6.3 | 8.7 | **12.5 (10.1–15.7)** | 13.5 | 18.6 |
| $25–100m | 2.5 | 5.0 (4.1–6.1) | 5.6 | 6.3 | **11.0 (10.0–12.3)** | 11.9 | 16.4 |
| ≥$100m | 1.1 | 3.3 (2.6–4.2) | 3.7 | 3.7 | **5.8 (4.6–7.9)** | 6.1 | 8.7 |

Government grants are a larger share of 1h at larger recipients [I, from the gap between the columns], so the size gradient flattens on the private bases.
- From $1m to $100m the pooled share is 11–13%, flat within overlapping intervals.
- The median gradient also halves: ≥$100m is about 0.3× the <$1m median on b3, against 0.1× on 1h.

### 2.3 By NTEE major group, line 1f and 1h − 1d − 1e bases

| Group | Respondents (b3) | Median, b3 | Pooled, b3 | Median, 1f | **Pooled, 1f** | Scaled pooled, 1f [I] |
|---|---|---|---|---|---|---|
| arts_culture | 223 | 9.4 | 10.9 | 10.1 | **11.9** | 17.6 |
| education (ex universities) | 238 | 8.4 | 10.6 | 8.6 | **11.2** | 16.6 |
| environment_animals | 205 | 4.5 | 12.4 | 4.5 | **13.1** | 19.5 |
| health (ex hospitals) | 212 | 7.7 | 10.5 | 8.4 | **12.7** | 18.8 |
| human_services | 258 | 7.8 | 10.1 | 8.1 | **10.7** | 15.9 |
| international | 240 | 9.1 | 6.3 | 9.1 | **6.3** | 9.4 |
| public_societal_benefit | 258 | 7.5 | 18.2 | 7.8 | **19.3** | 28.7 |
| religion (990 filers) | 145 | 13.4 | 7.9 | 13.4 | **8.1** | 12.0 |
| mutual_membership | 38 | 12.3 | 8.0 | 12.7 | 8.7 | 13.0 |
| unknown_z | 149 | 5.6 | 10.2 | 7.9 | 11.7 | 17.4 |
| no_ntee | 179 | 5.5 | 8.0 | 5.8 | 8.6 | 12.8 |

Intervals for every cell are in the CSV.
- International moves little between bases (4.9% → 6.3% pooled on 1h → 1f), as does religion (7.6% → 8.1%). International's 1e share is large only at a few members such as IRC, where 1e is 64% of 1h [F, recipient rows].
- Health, human services and public and societal benefit move most (6.8% → 12.7%, 5.7% → 10.7% and 12.9% → 19.3%).

## 3. Comparison with Chariot and the repo's other figures

| Claim (repo id) | Basis as published | Closest filing counterpart here | Like-for-like? |
|---|---|---|---|
| DAFs "nearly 13%" of total giving; $3.3bn of $26.1bn = 12.6%, 54 nonprofits, 2021–25 pooled [P] (NPB001–002) | DAF revenue ÷ total giving, CRM gift files, all sponsors | All recipients, pooled, 1h − 1d − 1e: 10.3% unscaled [F], 15.4% scaled [I]. Size-matched (~$97m giving per participant-year [I]): $25–100m 11.0% / 16.4% [I]; ≥$100m 5.8% / 8.7% [I] | Denominators are now close: "total giving" against all non-government, non-related contributions. The numerators are not: top-50 Schedule I grants over $5,000 against all-sponsor CRM-coded gifts. Unscaled is a floor; scaled leans high (wave 33A V33A-09). Chariot's 12.6% sits inside the unscaled-to-scaled range for the $25–100m band and for all recipients, and above the ≥$100m range. |
| Median DAF share 12% of 2023 total giving, 20 orgs [S] (NPB038) | Median of per-org shares | Median, 1h − 1d − 1e: all 7.7%; $25–100m 5.0%; ≥$100m 3.3% [F] | Medians cannot be scaled. The gap at large recipients (3–5% against 12%) is the clearest disagreement left after the basis change. |
| 15% of revenue, participants under $10m, CY2024 [P] (NPB024) | DAF ÷ total revenue | <$1m 21.0%, $1–5m 11.7% pooled on 1h − 1d − 1e [F]. On total revenue the committed study's all-recipient pooled share is 4.2%. | No: Chariot's figure is on total revenue, and here the bands are BMF revenue. Not comparable without a total-revenue band cut (not computed). |
| Sector range 4–24% of individual revenue [P] (NPB020) | DAF ÷ individual revenue | Line 1f pooled by NTEE group (groups with ≥140 respondents): 6.3–19.3% unscaled [F]; 9.4–28.7% scaled [I] | Closest available. 1f still holds foundation and corporate grants, so true individual-revenue shares would be higher. The widths agree; the ordering does not. |
| International Relief 23.7% of total revenue [P] (NPB019) | DAF ÷ total revenue | International: 6.3% of 1f, 4.9% of 1h [F] | No: total-revenue basis. On any basis here, international is among the lowest pooled groups. |
| 9.6% DAF ÷ total revenue, 2025 edition [P] (NPB029) | Pooled | 6.9% of 1h; 10.3% of 1h − 1d − 1e [F] | Partly: total revenue against contributions. |
| Netted FY2024 DAF grants ÷ CY2024 Giving USA total giving 9.86% (NPB096) and individual giving 14.88% (NPB097), repo-derived | Macro, all charities | Scaled pooled 15.4% on 1h − 1d − 1e [I] | Order-of-magnitude check only: the macro denominator includes churches, universities and hospitals, which are excluded here. |

**Reading [I].**
- Moving from 1h to the private bases closes most of the pooled gap with Chariot. 6.9% becomes 10.3–11.0% unscaled, against 12.6%.
- The remaining gap is about the size of the top-50 coverage adjustment, so it cannot be attributed to the denominator any more.
- At the median and for ≥$100m recipients the filings still give materially lower shares. That points to selection: Chariot's participants opt in through a DAF-payments vendor. It could also be numerator definition. Denominator choice no longer explains it.

## 4. Results (B): rating-eligible share of top-50 DAF dollars

### 4.1 All recipients, by first failing rule (central rule set)

All figures are [F]. Dollars are top-50 FY2023–24 non-DAF-to-DAF Schedule I.

| Category | Recipients | Share of recipients | DAF-weighted $bn | **Share of DAF-weighted $** | Share of Schedule I $ |
|---|---|---|---|---|---|
| **eligible** | 89,124 | **51.2%** | 56.93 | **76.9%** | 76.3% |
| no_efiled_990_church (BMF FOUNDATION 10) | 29,469 | 16.9% | 6.18 | 8.3% | 8.1% |
| not_in_bmf | 22,269 | 12.8% | 4.18 | 5.6% | 5.6% |
| fewer_than_3_efiled_in_6y | 6,148 | 3.5% | 2.55 | 3.4% | 3.4% |
| private_foundation | 1,083 | 0.6% | 1.26 | 1.7% | 1.7% |
| no_efiled_990_other | 8,428 | 4.8% | 1.02 | 1.4% | 2.3% |
| no_efiled_990_group_subordinate | 1,125 | 0.6% | 0.64 | 0.9% | 0.9% |
| no_ein_domestic | 3,649 | 2.1% | 0.40 | 0.5% | 0.6% |
| fewer_than_2_full_990_in_latest_4, 990-EZ filers | 12,749 | 7.3% | 0.39 | 0.5% | 0.5% |
| daf_sponsor_national_or_processor | 13 | <0.1% | 0.35 | 0.5% | 0.5% |
| fewer_than_2_full_990_in_latest_4, other | 37 | <0.1% | 0.15 | 0.2% | 0.2% |
| latest_is_990pf | 24 | <0.1% | 0.03 | <0.1% | <0.1% |
| not_501c3 | 100 | 0.1% | 0.01 | <0.1% | <0.1% |
| no_ein_foreign | 2 | <0.1% | <0.01 | <0.1% | <0.1% |
| **Total** | **174,220** | 100% | **74.07** | 100% | ($78.08bn) |

**Variants (eligible share of DAF-weighted $)** [F]:
- lenient (all DAF-sponsor EINs by filing rules): 77.3%;
- strict (community foundations also ineligible): 76.9%;
- six-year window by IRS processing year: 76.9% (89,160 recipients).

**Diagnostics** [F]:
- **Expense rule.** On the 2,056 sampled recipients that pass the filing rules, 2,051 have a full FY2023/24 990 in the read set and 2 fail the expense rule (0.1%): one has program expenses above total, the other has zero expenses. Its effect on the full-universe share is negligible [I].
- **Not in the BMF.** 2,254 of the 22,269 not-in-BMF EINs have at least one e-filed return. 1,213 of them pass the filing rules, holding $0.29bn (0.4% of dollars). These are likely new or recently re-listed organisations [I], so the upper bound on eligibility is about 77.3% [I].
- **Largest ineligible recipients (DAF-weighted).**
  - Navigation Charitable Fund, $1.26bn: fewer than three e-filed returns.
  - Two EINs not in the BMF, $0.56bn each.
  - The Church of Jesus Christ of Latter-day Saints, $0.46bn: church, no e-filed 990.
  - Lucas Museum of Narrative Art, $0.20bn: private operating foundation (BMF FOUNDATION 03).
  - Come and See Foundation, $0.14bn, and Campus Crusade for Christ, $0.09bn: church code.
  - Mass General Brigham, $0.10bn: group subordinate with no own e-filed 990.

### 4.2 By sector and band (central rule set)

| Scope | Recipients | DAF-weighted $bn | **Eligible share of $** | Eligible share of recipients | Main ineligible reason (share of $) |
|---|---|---|---|---|---|
| arts_culture | 11,962 | 4.04 | **89.5%** | 74.7% | private foundation 6.6% |
| education | 16,099 | 17.61 | **95.3%** | 76.5% | fewer than 3 e-filed 1.5% |
| environment_animals | 8,418 | 3.92 | **96.2%** | 74.5% | fewer than 3 e-filed 2.1% |
| health | 10,387 | 5.73 | **90.1%** | 79.6% | group subordinate 5.7% |
| human_services | 30,775 | 10.32 | **94.0%** | 76.2% | private foundation 2.3% |
| international | 4,956 | 4.17 | **94.7%** | 74.3% | fewer than 3 e-filed 2.8% |
| public_societal_benefit | 12,123 | 10.41 | **76.4%** | 72.4% | fewer than 3 e-filed 14.3% (Navigation) |
| religion | 18,114 | 4.91 | **34.0%** | 28.5% | church, no e-filed 990: 55.4% |
| no_ntee | 34,486 | 8.02 | **49.4%** | 33.4% | church, no e-filed 990: 42.4% |
| not_in_bmf / no_ein | 25,920 | 4.58 | 0% | 0% | — |
| band <$1m (incl. blank revenue) | 98,442 | 14.13 | **28.3%** | 40.7% | church 43.7%; PF 8.9%; other non-filer 7.2% |
| band $1–5m | 29,190 | 8.39 | **96.9%** | 98.0% | fewer than 3 e-filed 2.9% |
| band $5–25m | 14,191 | 14.09 | **89.6%** | 99.1% | fewer than 3 e-filed 10.3% (Navigation) |
| band $25–100m | 4,600 | 12.29 | **97.2%** | 99.1% | fewer than 3 e-filed 1.9% |
| band ≥$100m | 1,877 | 20.61 | **98.2%** | 99.6% | — |

By recipient type, the eligible share of dollars is:
- other charities (the (A) frame): 80.4%;
- universities: 91.4%;
- hospitals: 84.9%;
- NTEE T20–T31 and private foundations: 52.9%;
- DAFRC-panel universities and hospitals: 100.0%;
- panel single-issue charities: 98.5% [F].

**Reading [I].**
- **Eligibility is mostly a church and new-organisation question, not a size question.** Above $1m of BMF revenue, at least 98% of recipients and at least 89.6% of dollars are eligible.
- **The unrated majority by count is real but small by dollars.** Recipients failing CN's filing rules are 48.8% of recipient units but 23.1% of dollars, and about half of those dollars go to churches.
- This is the shape the repo's ratings-integration note assumed: "Build the differentiator around the roughly 83% of Pub 78 entities with no rating". The DAF-dollar version is roughly one dollar in four.

## 5. Limits

1. **(A) Individual giving is still not isolated.** Line 1f holds foundation, corporate, trust and estate gifts, DAF grants and gaming contributions alike. Schedule B donor detail is not public, and the Schedule A Part II and III support lines were not parsed (P-B40N1202-B43N26-01).
2. **(A) 990-EZ filers.** Their line 1 includes government grants and is used unchanged on every basis.
3. **(A) Numerator and scaling.** The numerator, scaling and sample limits of the committed study all carry over: top-50 sponsors only, grants over $5,000, sponsor-level DAF weighting, BMF revenue bands and selection on DAF recipients. Scaled figures lean high (V33A-09).
4. **(A) Leaked sponsors.** The leaked-sponsor regex misses UJA-Federation of New York, so the sensitivity scope is incomplete.
5. **(B) Rules CN applies but filings cannot test.** "Giving Not Recommended" alerts, "nonprofit subsidiaries" (undefined in the help text) and whether "Charity Navigator must directly receive" each filing cannot be observed. The results are eligibility upper bounds on those rules. They are **not** a count of rated organisations; no ratings were read.
6. **(B) DAF-sponsor rule.** CN's DAF exclusion is one sentence. The central reading (national and processor sponsors only) is an interpretation [I]. The three variants span only 76.9–77.3%.
7. **(B) Timing.** Eligibility is assessed against filings available in November 2026, not at grant time (FY2023–24). The TEOS index for 2026 is partial: it was downloaded 2026-11-15.
8. **(B) The BMF stands in for "revoked or inactive".** EINs not in the BMF are treated as ineligible. 1,213 of them, holding $0.29bn, pass the filing rules.
9. **(B) Recipient units.** Blank-EIN lines are grouped by normalised name, so the recipient count for those 3,651 units is approximate.

## 6. Reproduction

```
S=<scratchpad>
python3 scripts/mission_recipient_basis_eligibility.py . --np-cache $S/npcache --lines-cache $S/rcp/lines \
    --bmf-dir $S/rcp/bmf --index-dir $S/irs --f990-cache $S/q1226/f990p8 [--fetch] [--boot 500]
```

- The run takes about 2 minutes with a warm cache, plus about 1.5 minutes to fetch the 4,315 returns.
- Two runs produce byte-identical CSVs.
- It prints a JSON summary: statuses, line mix, leaked-sponsor names, eligibility diagnostics and the largest ineligible recipients.

## 7. Data dictionaries

### 7.1 `daf-share-individual-basis-2026-11-19.csv`

`row_type = summary` rows (126) use the first block of columns; `row_type = recipient` rows (2,352) use the second. Shares are fractions.

| Column | Meaning |
|---|---|
| row_type | `summary` or `recipient` |
| scope_type / scope | `all`; `sensitivity` (`form_990_only`, `ex_leaked_daf_sponsors`, `non_certainty_only`, `ex_ntee_T_and_fund_foundation_trust_names`); `ntee_major_group`; `revenue_band` (BMF REVENUE_AMT: a <$1m … e ≥$100m) |
| basis | `b1_1h`, `b2_1h_less_1e`, `b3_1abcf` (headline), `b4_1bcf`, `b5_1af`, `b6_1f` (§1.2) |
| sampled | Sampled EINs in scope |
| respondents | In-scope respondents (status `ok`) with a positive basis denominator |
| weighted_recipients | Σ weights over those respondents |
| den_nonpos_respondents, den_nonpos_num_share | `ok` respondents whose basis denominator is ≤0, and their share of weighted numerator dollars |
| p25_share, median_share, p75_share | Weighted quantiles of the per-recipient share (DAF-weighted numerator ÷ basis denominator) |
| median_ci95_lo/_hi, pooled_ci95_lo/_hi | Stratified bootstrap 95% interval (500 replicates) |
| pooled_share | Σw·num ÷ Σw·den over respondents |
| share_ge_20pct, share_gt_100pct | Weighted fraction of respondents with share ≥0.2 and >1 |
| scaled_pooled_inference | **[I]** pooled_share ÷ 0.6727 (top-50 FY2024 coverage) |
| ein, name, ntee_cd, ntee_major_group, revenue_band, stratum, stratum_N | As in the committed study |
| years_matched, forms, object_ids | FYs with a readable contributions total; IRS990 / IRS990EZ; TEOS object ids |
| num_daf_weighted_matched | Top-50 DAF-weighted numerator over matched FYs, USD |
| l1a_matched … l1h_matched | Part VIII lines 1a–1h summed over matched FYs. For EZ years, line 1 is in l1f and l1h, and the other lines are 0. |
| lines_sum_to_1h | True if 1a + … + 1f = 1h (±$1) in every 990 year |
| leaked_sponsor_name | Name matches the non-panel DAF-sponsor pattern (`LEAKED_SPONSOR` in the script) |
| den_b1_1h … den_b6_1f | Basis denominators, USD |
| share_b1_1h … share_b6_1f | Per-recipient shares (blank unless status `ok` and denominator >0) |
| status | `ok`; `no_fy2023_2024_990_or_ez_in_index`, `no_contributions_line` or `zero_or_negative_contributions` (out of scope); `xml_not_read` (missing; none in this run) |
| source | Source note |

### 7.2 `charity-rating-eligibility-share-2026-11-19.csv`

| Column | Meaning |
|---|---|
| row_type | `share` |
| scope_type / scope | `all` / `all_recipients`; `recipient_type`; `ntee_major_group`; `revenue_band`. `recipient_type` is `daf_panel_<segment>` for DAFRC panel EINs, else the committed exclusion class (`university`, `hospital`, `foundation`, `not_501c3`) or `other_charity`, plus `not_in_bmf` and `no_ein`. |
| rule_variant | `central_tax_year_window`: one row per category plus `all`. `lenient_all_daf_sponsors_by_filings`, `strict_cfs_also_ineligible` and `central_index_year_window`: `eligible` rows only. |
| category | `all`, `eligible`, or the first failing rule: `not_in_bmf`, `not_501c3`, `private_foundation`, `daf_sponsor_national_or_processor`, `daf_sponsor_community_foundation`, `no_efiled_990_church`, `no_efiled_990_group_subordinate`, `no_efiled_990_other`, `fewer_than_3_efiled_in_6y`, `latest_is_990pf`, `fewer_than_2_full_990_in_latest_4[_ez_filer]`, `no_ein_domestic`, `no_ein_foreign` |
| recipients, recipient_share | Recipient units in the category, and their share of the scope's units |
| usd_daf_weighted_fy2023_2024, dollar_share_daf_weighted | Top-50 FY2023–24 DAF-weighted non-DAF-to-DAF Schedule I dollars, and their share of the scope total |
| usd_sched_i_fy2023_2024, dollar_share_sched_i | The same on the as-filed Schedule I basis |
| source | Source note |

## 8. Source register

| ID | Source | URL | Accessed | Use |
|---|---|---|---|---|
| S1 | IRS, Instructions for Form 990 (2025), Part VIII line 1 | https://www.irs.gov/instructions/i990 | 2026-11-19 (robots.txt 200; `/instructions/` not disallowed) | Line 1a–1h definitions; 1f includes DAF grants |
| S2 | IRS Form 990 e-file XML, GivingTuesday mirror of IRS TEOS | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | 2026-11-19 (robots.txt 404) | Part VIII lines, Part IX totals for the 4,315 sampled returns |
| S3 | IRS TEOS e-file index 2019–2026 | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (and 2019–2026) | Cached 2026-11-14/15 | Filing history, form type (DLN), return location |
| S4 | IRS EO Business Master File | https://www.irs.gov/pub/irs-soi/eo1.csv (eo1–eo4, eo_pr, eo_xx) | Cached; Last-Modified 2026-11-09 | SUBSECTION, FOUNDATION, GROUP, AFFILIATION, NTEE_CD, REVENUE_AMT |
| S5 | IRS automatic revocation list | https://apps.irs.gov/pub/epostcard/data-download-revocation.zip | Cached 2026-11-11 | Diagnostic only |
| S6 | Charity Navigator Help Center, "Charity Navigator's rating system" | https://intercom.help/charity-navigator/en/articles/8557824-charity-navigator-s-rating-system | Dated 2026-04-09; fetched 2026-11-19 (robots 200; path not disallowed) | Eligibility rules |
| S7 | Charity Navigator, Spring 2026 Rating Methodology Update | https://intercom.help/charity-navigator/en/articles/14471517-spring-2026-rating-methodology-update | Dated 2026-04-09; fetched 2026-11-19 | No eligibility change |
| S8 | Charity Navigator, 2026 Rating Update Schedule | https://intercom.help/charity-navigator/en/articles/8566358-2026-rating-update-schedule | Dated 2026-09-10; fetched 2026-11-19 | Timing (November update published 11/17) |
| S9 | Charity Navigator Release Notes | https://www.charitynavigator.org/about-us/our-methodology/ratings/release-notes/ | Fetched 2026-11-19 (robots 200; only /search, /basket, /profile and similar disallowed) | DAF ineligibility (2024); revenue size classes (2023) |
| S10 | Charity Navigator Rating Methodology Guide (Updated March 2026) | https://www.charitynavigator.org/content/dam/cn/cn/landing-pages/Rating%20Methodology%20Guide%20(Updated%20March%202026).pdf | 2026-11-19: **HTTP 404** | Not read |
| S11 | DAFRC Annual DAF Report 2025 dataset (repo copy) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx; [dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | Repo | Top-50 universe; panel segments |
| S12 | Chariot/K2D DAF Fundraising Report pages, as recorded in the repo | https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release ; https://www.givechariot.com/resources/toolkits/daf-fundraising-report ; https://www.givechariot.com/resources/insights/inside-the-2025-daf-fundraising-report-how-donor-advised-funds-are-transforming-philanthropy | Not re-fetched; quoted from [nonprofit-daf-revenue-benchmarks-2021-2026.csv](../../data/mission-2026-11-14/nonprofit-daf-revenue-benchmarks-2021-2026.csv) (NPB001–002, 019–020, 024, 029, 038) as validated in waves 25B and 33A | Comparison figures |
| S13 | Repo derived macro ratios | [nonprofit-daf-revenue-benchmarks-2021-2026.csv](../../data/mission-2026-11-14/nonprofit-daf-revenue-benchmarks-2021-2026.csv) NPB096–097 | Repo | Comparison |
| S14 | Committed study and validation | [b40n12-daf-share-of-recipient-revenue.md](b40n12-daf-share-of-recipient-revenue.md); [validation-wave33a-report.md](validation-wave33a-report.md) | Repo | Method, corrections |

**Robots and fetch logs** are in the scratchpad: `q1226/robots/log.tsv` (www.irs.gov 200; intercom.help 200; www.charitynavigator.org 200; gt990datalake-rawdata.s3.amazonaws.com 404) and `q1226/pages/fetchlog.tsv`. All requests used user agent `research-script/1.0`. There was no outreach and no login, and crt.sh, certspotter and sec.gov were not used.
