# NPT-pattern screen of the DAFRC panel (P-B44N27B39N4-02) and realised admin-fee rates in the long tail (P-B4501-02 / P-B450104-02)

**Date:** 2026-11-20 · **Task id:** b4427b-b4501 · **Labels:** **[F]** filed or primary figure; **[C]** computed by the script; **[I]** inference. This is research, not legal, tax or accounting advice.

**Outputs**
- [`scripts/mission_npt_screen_fees.py`](../../scripts/mission_npt_screen_fees.py): stdlib only, functional style. Tasks `fetch` (IRS index lookup, XML fetch and parse into a JSONL cache outside the repo), `screen` (part A) and `fees` (part B). Every table below is its stdout.
- [`data/mission-2026-11-14/npt-pattern-screen-2026-11-20.csv`](../../data/mission-2026-11-14/npt-pattern-screen-2026-11-20.csv): 5,963 rows, one per DAFRC sponsor-year FY2021–2024 (dictionary in §6.1).
- [`data/mission-2026-11-14/tail-realised-fee-rates-2026-11-20.csv`](../../data/mission-2026-11-14/tail-realised-fee-rates-2026-11-20.csv): 31 rows, one per community foundation in the fee-census sample (dictionary in §6.2).
- [`data/mission-2026-11-14/queue-proposals-b4427b-b4501.csv`](../../data/mission-2026-11-14/queue-proposals-b4427b-b4501.csv): 6 follow-ups.
- No existing file was edited.

**Governing inputs.** Part A follows [`b44n27-b39n4-dafrc-data-quality.md`](b44n27-b39n4-dafrc-data-quality.md) as corrected by validation wave 34A (the NPT FY2023 consolidated statements, $28,514,324k of net assets, settle that Schedule D line 4 is the outlier). Part B uses the census sample of [`b45n33-01-long-tail-fee-census.md`](b45n33-01-long-tail-fee-census.md) with its wave-34B corrections (Columbus Medical Association Foundation reclassified to `partial`; it is not a CF, so it is outside this CF-only study), and tests the assumption in [`b4501-04-tail-fee-pool-revision.md`](b4501-04-tail-fee-pool-revision.md) as corrected by wave 35A (whole-tail central $138m vs CFs-only $89.9m; the CFs-only figure is "as defensible a central figure as the whole-tail one").

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **(A) How many sponsor-years show the NPT pattern?** | Of 5,963 DAFRC sponsor-years FY2021–24, **4,633 could be tested** (filed 990s for t−1, t and t+1 with Schedule D line 4 and positive Part X net assets). They hold $849.9bn of filed line 4 value. **101 have a ratio break** (more than 10 points against both neighbours, in the same direction). **44 also keep contributions and grants consistent**, so they show the NPT pattern [C]. | High on the counts [C] |
| **Breaks above $250m** | **Two.** (1) **NPT FY2023**: filed $22,843.6m against $27,919.2m of net assets (ratio 101.3% / 81.8% / 100.6%). The gap is −$5,333.7m at the neighbours' ratio. (2) **Dechomai Asset Trust FY2021**: filed $267.7m against $1,148.1m of net assets (60.3% / 23.3% / 100.0%). The gap is −$652.5m [C]. No ratio break above $250m fails only the flow test. A one-sided check of the 1,036 sponsor-years with only one usable neighbour (mostly FY2024) finds none above $250m [C]. | High [C] |
| **Roll-forward test** | **Both fail it.** NPT: the forward roll gives $28,216.2m and the backward roll $28,120.1m; they agree, and the filed figure is 19% below both. The net-asset-change roll gives $28,191.8m / $28,156.1m, which reproduces b44n27-b39n4 §2.2 ($28.19bn / $28.16bn). Dechomai: forward $935.2m, backward $1,148.2m; the filed $267.7m is more than 70% below both. The two rolls differ by 19%, partly because the FY2020 anchor (60.3% of net assets) looks low too [C; I on the cause]. | High on NPT (it also agrees with NPT's own statements); medium on Dechomai (no first-party statements read) |
| **What it would change** | As a sensitivity (the repo keeps filed values), each roll-forward midpoint would raise the corrected market by **$774.0m in FY2021** (to $234.79bn; growth FY2020→21 38.7%→39.1%, FY2021→22 −2.5%→−2.8%) and **$5,324.6m in FY2023** (to $261.69bn; FY2023→24 growth 26.1%→23.5%) [C]. Below $250m, 27 more NPT-pattern sponsor-years fail the roll-forward. They net to about +$29m, but they include Servant Foundation FY2022 (−$202.0m), Thrivent FY2021 (−$118.2m), BNY Mellon FY2022 (−$67.8m) and FJC FY2021 (−$61.5m) [C]. | Medium |
| **(B) Do non-publishing tail CFs charge?** | **Yes, wherever the filing shows it.** 18 of the 25 non-publishing sampled CFs report some administrative or management fee income on the 990, and **7 disclose internal fees charged to their own funds**. At the 6 publishers the figures are 4 and 1. The remaining 7 non-publishers show no fee line. That is non-disclosure, not evidence of zero fees [C on counts; I on reading]. | Medium |
| **Realised rates** | Internal fee income ÷ average total assets, FY2022–24 pooled over disclosure years: **non-publishers median 104 bps (IQR 86–122; n = 7)**; 112 bps (102–123; n = 6) excluding Central Florida, whose visible item looks partial. **The one publisher that discloses internal fees, Hutchinson, realises 83 bps** on all funds against its published 125 bps DAF rate. Schedule D Part V administrative expenses on endowment funds: non-publishers median **116 bps (85–162; n = 14)**, publishers 91 bps (n = 2: Whatcom 139, Athens 43) [C]. | Medium on the levels (small n; all-fund, not DAF-only) |
| **Test of the whole-tail pool's assumption** | **For CFs the assumption holds in direction and roughly in size.** Non-publishing tail CFs do charge, at realised all-fund rates no lower than the one publisher observed on the same basis. These rates cover all funds and sit below the 150 bps published DAF median, but published DAF rates are top-tier list prices and realised all-fund rates include endowed and agency funds. [I] The data support charging non-publishing CFs a CF-type fee, so they support the CFs-only central ($89.9m). If every tail CF realised the median internal-fee rate on its DAF assets, the CF pool would be **$62.9m** ($10.7m–$79.0m across the observed internal-fee rates) [C on that assumption]. **The non-CF half of the whole-tail assumption ($3.08bn) is not tested here** (P-B4427B4501-05). | Low–medium |

---

## 1. Method

### 1.1 Part A: data and return selection [C]
- **Panel.** `dafrc-sponsor-schedule-d-fy2019-2024.csv`, the rows for FY2021–2024: 5,963 sponsor-years and 1,566 EINs. The repo value is DAFRC's value, or the applied row in `dafrc-corrections-itemized.csv` where one exists. Both are carried in the CSV, but the screen runs on **filed** values.
- **Part X source.** Neither the harvest CSVs (`form990-returns-schedule-d-harvest-full.csv`, the 2026 fill and the FY2025 refresh) nor `sponsor-cost-structure.csv` carries Part X net assets; they have total assets only. Following the task, the script therefore parses the XMLs.
- **Return selection.** The rule is the repo's R1 rule (`mission_dafrc_corrected_totals.py`, `mission_dafrc_r2_check.py`):
  - the fiscal year is the calendar year in which the tax period ends;
  - the return is the newest Form 990 for that year, and a higher object id supersedes.
  - The indexes are the IRS TEOS `index_2019`–`index_2025` (repo downloads of 2026-11-14) plus `index_2026.csv` downloaded on 2026-11-19 (516,019 rows).
  - FY2020 and FY2025 returns are fetched so that FY2021 and FY2024 have both neighbours.
  - Where the newest return is missing from the mirror, the next-newest for the same year is used (1 case).
- **Fetch.** 8,532 returns were selected:
  - 813 came from earlier scratch copies and 7,636 from the GivingTuesday mirror of IRS TEOS;
  - 83 are not on the mirror (HTTP 404), so those sponsor-years are untested.
- **Parsed fields.**
  - Schedule D Part I lines 1–4.
  - Part X line 33 net assets (BOY and EOY) and total assets.
  - Part VIII line 1h total contributions.
  - Part I line 13 / Part IX lines 1–3 grants (`CYGrantsAndSimilarPaidAmt`).
  - Schedule D Part I column (b).

### 1.2 Part A: the screen [C]
For each sponsor-year t with filed returns for t−1, t and t+1:

| Step | Definition |
|---|---|
| Ratio | r = Schedule D I-4 ÷ Part X net assets EOY; requires positive net assets |
| Ratio break | \|r_t − r_(t−1)\| > 10 points **and** \|r_t − r_(t+1)\| > 10 points, **same sign** (a spike or dip, not a trend) |
| Flows consistent | Contribution share (Sch D I-2 ÷ Part VIII 1h) and grant share (Sch D I-3 ÷ Part IX 1–3) in year t each lie within [min, max] of the two neighbours' shares ± 10 points |
| NPT pattern | Ratio break **and** flows consistent |
| Size | gap = I-4_t − mean(r_(t−1), r_(t+1)) × net assets_t; listed when \|gap\| > $250m |
| Roll-forward | ρ_t = (NA_t − NA_(t−1) − (Part VIII contributions_t − Part IX grants_t)) ÷ NA_(t−1), i.e. the year's net-asset return apart from contributions and grants.<br>Forward = I-4_(t−1) × (1 + ρ_t) + I-2_t − I-3_t.<br>Backward = (I-4_(t+1) − I-2_(t+1) + I-3_(t+1)) ÷ (1 + ρ_(t+1)).<br>Also the NPT net-asset-change roll I-4_(t−1) + ΔNA_t, for comparison with b44n27-b39n4 |
| Verdict | "Filed fails roll-forward" when the filed value is more than 10% from both rolls. The `rolls_agree` flag says whether the two rolls are within 10% of each other |
| One-sided supplement | Sponsor-years with exactly one usable neighbour: the ratio test against that neighbour alone, with \|gap\| > $250m and both flow shares within 10 points. Listed separately; it is not the NPT pattern as defined |

**Sensitivity.** Each listed break that fails the roll-forward is replaced by the roll midpoint in the repo's corrected market totals (`dafrc-corrected-market-totals.csv`). The repo keeps the filed values.

### 1.3 Part B: sample, sources and rates
- **Sample.** All 31 CFs in the fee-census sample:
  - the 6 publishers with a 2021+ rate (Whatcom, Hutchinson, Pikes Peak, Homer, Athens, Adirondack Trust Company at 0%);
  - the 25 other CFs, which are the non-publishers. They include CF of West Texas (pre-2021 rate), two `published_unread`, three `partial`, five `robots_blocked` and one with no website.
  - The task asked for about 20 non-publishers. All 25 were read, because the 990 route needs no website access.
- **Form 990 (all 31; FY2022–24 returns, with FY2021 for the opening DAF balance).** The script reads three things:
  1. **Part VIII revenue lines** (program service revenue and other revenue) whose description names an administrative, management, philanthropic or fund fee, or "fee income".
  2. **Schedule D Part XI line 2d items** naming administrative fees. These are revenue in the audited statements but not on Part VIII, typically internal fees charged to component funds and eliminated or netted.
  3. **Schedule D Part V line 1f**, administrative expenses paid from endowment funds, against the average of lines 1a and 1g.
- **Audited statements.** The 30 CF websites were crawled for posted audits:
  - robots.txt was checked first for each host, with UA `research-script/1.0`, the homepage plus sitemaps, and up to 45 pages per site;
  - §5 has the robots log.
  - Only two CFs post audits: Pikes Peak (2023, 2024 and 2025) and Licking County (2024 with 2023 comparatives).
  - Licking's note gives the fee charged to all its funds. The two quotes are verified by the script against the cached PDF text ("verified").
  - Pikes Peak's audits show only "Management Fee, Charged to Others" (external). Its internal fees are not disclosed.
- **Scope.** Each CF with a visible fee is classed `internal`, `external` or `unknown` from the filer's own wording (`SCOPE` in the script; reason in `scope_basis`):
  - **internal** means fees the CF charges its own funds;
  - **external** means fees from agency or other organisations;
  - **unknown** means a fee line whose base is not stated.
- **Realised rate** = fee income ÷ average of BOY and EOY Part X total assets (all funds under management, agency funds included), and also ÷ average net assets.
  - It is pooled over FY2022–24, over the years in which a fee was visible. A blank year at a CF that discloses in other years is treated as non-disclosure, not as zero (Hutchinson FY2022, Licking FY2022).
  - Fee income ÷ average DAF balance (Schedule D I-4) is reported only as an upper bound on a DAF-specific rate.

---

## 2. Results, part A

### 2.1 Coverage (S1) [C]

| FY | DAFRC sponsor-years | Tested | Ratio break | NPT pattern | Pattern, \|gap\| > $250m | Filed line 4 tested, $bn |
|---|---|---|---|---|---|---|
| 2021 | 1,469 | 1,209 | 31 | 14 | 1 | 181.68 |
| 2022 | 1,489 | 1,316 | 28 | 14 | 0 | 198.92 |
| 2023 | 1,493 | 1,325 | 28 | 10 | 1 | 253.52 |
| 2024 | 1,512 | 783 | 14 | 6 | 0 | 215.82 |

Untested sponsor-years:
- 1,070 lack one neighbour;
- 209 have no Schedule D line 4 in year t;
- 32 have non-positive or missing net assets;
- 19 have no filed 990 for year t.

Most of the FY2024 gap is FY2025 returns not yet filed or not yet on the mirror ($106.6bn of FY2024 repo value untested). The one-sided supplement covers these years and finds no break above $250m. One large FY2021 row is untested: Schwab (Donor Advised Charitable Giving). Its FY2021 return is the 202112 short-period return, which has no Schedule D line 4 [C].

### 2.2 Breaks above $250m and the roll-forward (S2) [C]

| Sponsor | FY | Line 4 filed $m | Net assets $m | Ratio t−1 / t / t+1 | Gap $m | Contrib. / grant share t−1/t/t+1 | Roll fwd / bwd $m | NA-change roll fwd / bwd $m | Verdict | Filed − roll mid $m |
|---|---|---|---|---|---|---|---|---|---|---|
| National Philanthropic Trust (237825575) | 2023 | 22,843.6 | 27,919.2 | 101.3% / 81.8% / 100.6% | −5,333.7 | 100/100/100 · 100/100/100 | 28,216.2 / 28,120.1 | 28,191.8 / 28,156.1 | fails; rolls agree | −5,324.6 |
| Dechomai Asset Trust (260724604) | 2021 | 267.7 | 1,148.1 | 60.3% / 23.3% / 100.0% | −652.5 | 100/100/100 · 100/100/100 | 935.2 / 1,148.2 | 931.3 / 1,148.2 | fails; rolls differ by 19% | −774.0 |

**NPT FY2023** is the case that defined the pattern. The screen finds it unaided, and its roll-forwards match b44n27-b39n4. NPT's own consolidated statements at 2023-06-30 ($28,514,324k of net assets; wave 34A) agree with the rolls, not with the filed figure.

**Dechomai Asset Trust FY2021** (object 202243199349331259, period ending 2021-12-31) [F]:
- **The return.** Schedule D contributions ($985,904,717) equal Part VIII total contributions, and Schedule D grants ($374,029,609) equal Part IX grants. Column (b) is zero. Total assets EOY are $1,237,997,188, of which "other assets" are $1,077,260,674.
- **What does not explain it.** No other amount in the return equals $267,690,026. Reading the XML's numeric fields, no line between $100m and $1.5bn matches it.
- **The neighbours.** FY2022 line 4 ($1,123.5m) equals FY2022 net assets ($1,123.3m). The FY2020 ratio (60.3%: $329.2m on $546.0m) is itself low.
- **[I]** The FY2021 line 4 is very likely a filer error, understated by about $0.65–0.88bn. FY2020 may be understated too; it is outside the FY2021–24 window and was not screened.
- **Status in the repo.** The value is DAFRC "IRS 990" and enters the repo's FY2021 total unchanged. No first-party Dechomai statements were read (P-B4427B4501-01).

### 2.3 Below the listing threshold (S2b) and the sensitivity (S6) [C]

| Sponsor | FY | Line 4 filed $m | Net assets $m | Ratio t−1 / t / t+1 | Gap $m | Roll fwd / bwd $m | Verdict |
|---|---|---|---|---|---|---|---|
| Servant Foundation | 2022 | 1,153.9 | 1,365.4 | 98.8% / 84.5% / 100.7% | −207.7 | 1,333.8 / 1,378.0 | fails |
| Thrivent Charitable Impact & Investing | 2021 | 426.9 | 681.6 | 85.6% / 62.6% / 74.9% | −120.1 | 579.5 / 510.8 | fails |
| BNY Mellon Charitable Gift Fund | 2022 | 456.6 | 482.3 | 115.4% / 94.7% / 106.2% | −77.7 | 536.3 / 512.5 | fails |
| Network for Good | 2021 | 146.8 | 2.8 | 4885.3% / 5309.6% / 200.1% | 76.5 | −534.1 / 7.3 | fails (net assets near zero: a processor, ratio not meaningful) |
| FJC | 2021 | 218.1 | 319.7 | 85.7% / 68.2% / 88.9% | −61.1 | 269.4 / 289.7 | fails |
| The Indianapolis Foundation | 2022 | 87.8 | 60.7 | 82.1% / 144.5% / 23.8% | 55.6 | 52.4 / 15.1 | fails |
| University Impact | 2022 | 134.6 | 134.5 | 32.9% / 100.0% / 85.4% | 54.9 | 101.7 / 123.7 | consistent |

**Verdicts across the 44 NPT-pattern sponsor-years:**
- 20 dips and 24 spikes;
- 29 fail the roll-forward, 9 are consistent with it and 6 are untestable [C].

| FY | Repo corrected $bn | Sensitivity $bn | Change $m | Growth, repo | Growth, sensitivity |
|---|---|---|---|---|---|
| 2020 | 168.74 | 168.74 | 0.0 | – | – |
| 2021 | 234.01 | 234.79 | +774.0 | 38.7% | 39.1% |
| 2022 | 228.14 | 228.14 | 0.0 | −2.5% | −2.8% |
| 2023 | 256.37 | 261.69 | +5,324.6 | 12.4% | 14.7% |
| 2024 | 323.27 | 323.27 | 0.0 | 26.1% | 23.5% |

**[I] Reading.**
- The NPT case is not unique, but it is by far the largest. Only one other filed line 4 breaks from its own net-asset ratio by more than $250m with consistent flows.
- The R1–R4 rules let filed errors through. Outside NPT they move the market by under 0.5% in any year.
- A repo rule for "filed but inconsistent" values would matter for FY2023 (NPT) and, much less, for FY2021 (Dechomai). It is a policy choice, as b44n27-b39n4 §2.4 says.

---

## 3. Results, part B

### 3.1 Publishers against non-publishers (F1) [C]
Median (IQR; n) over CFs with a positive value, in bps:

| Group | CFs | Any fee visible | Internal fee disclosed | Visible fee ÷ avg total assets | Internal-fee CFs ÷ avg total assets | Internal-fee CFs ÷ avg net assets | Part V admin ÷ avg endowment |
|---|---|---|---|---|---|---|---|
| Publishers | 6 | 4 | 1 | 10 (9–29; n=4) | 83 (n=1) | 84 (n=1) | 91 (67–115; n=2) |
| Non-publishers | 25 | 18 | 7 | 21 (4–115; n=18) | **104 (86–122; n=7)** | 109 (90–128; n=7) | **116 (85–162; n=14)** |

- **Sensitivity.** Central Florida Foundation's Part XI item ("Internal administrative fees", about $190k a year) is 17.5 bps of total assets, while its Part V endowment administrative expense is 187.8 bps, so its capture looks partial. Excluding it, the non-publisher internal median is **112 bps (102–123; n = 6)** [C].
- **Visible fee ÷ total assets** mixes complete internal-fee disclosure with small agency or external fee lines. It is a lower bound and should not be read as a rate.

### 3.2 Each CF (F2; FY2022–24 pooled over years with a visible fee) [C]

| Sponsor | Group | Census status | Published bps @$100k | Years with fee | Fee income $ | ÷ avg TA | ÷ avg NA | Part V admin ÷ endowment | Fee ÷ avg DAF (upper bound) | Scope |
|---|---|---|---|---|---|---|---|---|---|---|
| Hutchinson CF | pub. | published_schedule | 125 | 2/3 | 1,712,611 | 83.2 | 83.5 | – | 312.4 | internal |
| Whatcom CF | pub. | published_schedule | 200 | 3/3 | 199,168 | 10.5 | 11.5 | 139.4 | 56.9 | unknown |
| Pikes Peak CF | pub. | published_schedule | 150 | 3/3 | 212,082 | 8.8 | 9.7 | – | 14.7 | external |
| Athens County Fdn | pub. | published_schedule | 150 | 2/3 | 17,089 | 8.5 | 8.9 | 42.8 | 33.3 | unknown |
| Homer Fdn | pub. | published_schedule | 150 | 0/3 | 0 | – | – | −179.4 (negative as filed) | – | none visible |
| Adirondack Trust Co. CF | pub. | no admin fee | 0 | 0/3 | 0 | – | – | – | – | none visible |
| Cape Coral CF | non-pub. | no_published_fee | – | 3/3 | 537,179 | 141.0 | 141.7 | 243.5 | 715.8 | unknown |
| Madison County CF | non-pub. | no_published_fee | – | 3/3 | 1,102,053 | 129.8 | 140.8 | 166.4 | 888.1 | unknown |
| CF of Monroe | non-pub. | no_published_fee | – | 3/3 | 550,431 | 129.4 | 135.7 | 198.4 | 11,686.1 | internal |
| CF of Greene County PA | non-pub. | robots_blocked | – | 3/3 | 319,076 | 124.2 | 132.8 | 101.0 | 1,540.2 | internal |
| Decatur County CF | non-pub. | no_published_fee | – | 3/3 | 992,405 | 118.9 | 122.8 | 133.0 | 1,499.6 | internal |
| Four Way CF | non-pub. | no_published_fee | – | 3/3 | 373,406 | 104.5 | 109.2 | 70.0 | 728.9 | internal |
| Clinton County Fdn (OH) | non-pub. | robots_blocked | – | 3/3 | 962,911 | 101.6 | 102.3 | – | 534.0 | internal |
| Licking County Fdn | non-pub. | partial | – | 2/3 | 2,016,004 | 69.7 | 76.9 | – | 578.1 | internal (audit) |
| CF of the Eastern Shore | non-pub. | published_unread | – | 3/3 | 1,168,888 | 24.7 | 35.2 | – | 158.5 | unknown |
| Central Florida Fdn | non-pub. | no_published_fee | – | 3/3 | 590,152 | 17.5 | 18.1 | 187.8 | 39.5 | internal (partial?) |
| CF of Central Wisconsin | non-pub. | partial | – | 3/3 | 53,707 | 5.5 | 5.9 | – | 36.6 | unknown |
| CF of Mendocino County | non-pub. | partial | – | 3/3 | 73,087 | 4.8 | 5.1 | 128.2 | 81.3 | unknown |
| Findlay-Hancock County CF | non-pub. | no_published_fee | – | 3/3 | 175,954 | 3.6 | 3.8 | – | 25.8 | unknown |
| Clarinda Fdn | non-pub. | robots_blocked | – | 2/3 | 4,224 | 3.5 | 3.5 | 102.8 | 68.0 | unknown |
| CF of West Texas | non-pub. | published_pre2021 | 100 | 3/3 | 62,491 | 3.0 | 3.2 | 46.6 | 10.8 | unknown |
| Mackinac Island CF | non-pub. | no_published_fee | – | 3/3 | 14,128 | 2.6 | 2.7 | 150.7 | 35.6 | unknown |
| Wichita Falls Area CF | non-pub. | robots_blocked | – | 3/3 | 46,650 | 2.0 | 2.0 | 81.2 | 3.6 | unknown |
| Jasper Newton Fdn | non-pub. | no_published_fee | – | 3/3 | 12,285 | 1.6 | 1.6 | – | 66.1 | external |
| Greater Lowell CF; CF of South Lake County; CF of West KY; South Pacific County CF; Columbine CF; CF of Greater Muscatine; Catalyst Trust of Indiana | non-pub. | various | – | 0/3 | 0 | – | – | West KY 77.0; South Pacific 97.1; others – | – | none visible |

Fee lines are taken as filed [F]. The line descriptions and Part XI items for each CF are in the CSV (`fee_lines_seen`, `recon_items_seen`). Examples:
- Hutchinson FY2024, Schedule D Part XI 2d: "ADMINISTRATIVE FEES RECEIVED FROM NONOPERATING FUNDS 935,785".
- Decatur County FY2024: "ADMINISTRATIVE FEES 340,412".
- Clinton County FY2024: Part VIII "ADMINISTRATIVE FEE REVENUE" $355,351, with a Part IX 11g "ADMINISTRATIVE FEES" expense of $345,293.
- Licking County audit 2024: "The administrative fee amounted to $1,058,361 and $957,643 during the years ended December 31, 2024 and 2023".
- Pikes Peak audit: "Management Fee, Charged to Others".

### 3.3 What the test shows [I]
1. **Non-publishers charge.**
   - Every one of the 8 sampled CFs whose filings disclose internal fees charges a realised **70–141 bps of total assets a year**, with one exception: Central Florida, whose disclosed item is partial.
   - 7 of those 8 publish no rate. Their median (104 bps; 112 bps without Central Florida) is above the one publisher measured the same way (Hutchinson, 83 bps).
   - On Schedule D Part V, 14 non-publishers charge their endowment funds a median 116 bps in administrative expenses, against 91 bps at the two publishers that report it.
   - Not publishing a rate is not evidence of not charging one.
2. **Realised all-fund rates sit below published DAF rates.**
   - Hutchinson realises 83 bps on all funds against a published DAF rate of 125 bps on the first $2m. It also charges agency endowments, and its schedule falls to 0.25% above $15m.
   - All-fund rates blend endowed, agency and designated funds, which are often priced lower than non-endowed DAFs, so a realised all-fund rate is a floor for the DAF rate rather than an estimate of it.
   - The fee ÷ DAF balance column is a ceiling: 312 bps at Hutchinson and 534–1,540 bps at the non-publishers with small DAF books. The true DAF rate lies between the two, and is unobserved (P-B4427B4501-06).
3. **For the pool.**
   - The wave-35A note's CFs-only central ($89.9m at the median published schedule on tail CF DAF assets) is supported in kind: tail CFs that do not publish do charge, at rates similar to those that do.
   - Applied to tail CF DAF assets ($6.10bn), the realised all-fund rates give $10.7m–$79.0m, median **$62.9m** [C on that assumption]. Read this as a floor-type figure, because DAF rates likely exceed all-fund rates.
   - Together, the two bracket the CF pool at roughly **$63m–$90m**.
   - **The step from the CFs-only to the whole-tail pool ($138m), which adds CF-type fees on $3.08bn of non-CF DAF assets, is not tested here and remains the unevidenced part** (P-B4427B4501-05).

---

## 4. Limits
1. **Part A uses filed values only.** A ratio break is a symptom. The roll-forward assumes the DAF book earns the same return as the whole balance sheet (ρ), which is approximate where DAFs are a minority of net assets. The 10-point and $250m cut-offs are the queue item's. Sub-threshold cases are listed but not resolved.
2. **Part A coverage.**
   - 22% of sponsor-years are untested. FY2024 is the weakest year (783 of 1,512), pending FY2025 returns.
   - 83 selected returns are not on the mirror.
   - Schwab FY2021 is untested: its short-period return has no line 4.
   - The FY2020 and FY2025 neighbours were not themselves screened.
3. **Dechomai is not confirmed by first-party statements.** Its FY2020 anchor looks low too, so the roll-forward midpoint ($1,041.7m) is uncertain by about ±$100m.
4. **Part B measures all-fund fees.** No source gives DAF-only fee income. Realised rates are fee income ÷ total assets, which include agency funds, operating assets and, at some CFs, real estate or split-interest assets. The net-asset denominator is shown alongside.
5. **Capture is incomplete.** Internal fees are often eliminated without disclosure: of 31 CFs, 8 disclose them. "Unknown"-scope lines may be agency fees only, such as Whatcom's "PHILANTHROPIC FEES" or Pikes Peak's fees "Charged to Others". "None visible" is not zero.
6. **Scope classes are judgements** from the filer's wording, recorded in `scope_basis`. Central Florida's disclosed item is likely partial; Eastern Shore's Part XI shows "MANAGEMENT FEES −195,882" netted against its fee revenue.
7. **Audits are rarely posted.** Only 2 of 30 CF sites post an audit, and 5 CF hosts refuse the study's UA at robots.txt (403), so they were not read. The 990 route covers them.
8. **Small n.** There is 1 publisher with internal disclosure, 7 non-publishers with it, and 14 and 2 with Part V. The publisher-against-non-publisher comparison is indicative.
9. **Part V line 1f** is the filer's "administrative expenses" from endowment funds. At Decatur it equals the internal fee to the dollar in FY2021 ($354,818). Elsewhere it may include other charges. Homer reports negative values.

---

## 5. Robots and access log (2026-11-19/20, UA `research-script/1.0`, unchanged)

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404, so no robots file (no restriction) | 7,636 XML returns; 83 objects 404 |
| apps.irs.gov | 302 to www.irs.gov/404, so no robots file | IRS TEOS index CSVs (repo/scratch copies of 2026-11-14 and 2026-11-19) |
| whatcomcf.org, hutchcf.org, www.hutchcf.org, www.cfwtx.org, www.cfes.org, www.ppcf.org, www.thelcfoundation.org, www.glcfoundation.org, communityfound.org, www.homerfoundation.org, fourwaycommunityfoundation.org, micf.org, www.madisonccf.org, cfslc.org, atccf.org, www.athensfoundation.org, spccf.org, cfcwi.org, dccfound.org, www.grandfoundation.com, www.jaspernewtonfoundation.org, givinggreater.org, www.capecoralcf.org | 200, with the fetched paths allowed | Audit and annual-report discovery |
| cffound.org, cfmonroe.org, www.community-foundation.com | 404, so no robots file | Discovery; no audit posted |
| www.wfacf.org, clintoncountyohiofoundation.org, www.cfwestky.org, www.cfgcpa.org, clarindafoundation.com | 403, treated as disallowed; nothing fetched | – (990 route only) |
| assets.nlcnet.net, irp.cdn-website.com (file hosts linked from Findlay and Athens) | 403, treated as disallowed; nothing fetched | – |

No logins, forms or outreach were used. No user agent was changed. sec.gov, crt.sh and certspotter were not used.

---

## 6. Data dictionaries

### 6.1 `npt-pattern-screen-2026-11-20.csv` (one row per DAFRC sponsor-year FY2021–24)

| Column | Meaning |
|---|---|
| ein, name, type | DAFRC identifiers |
| fiscal_year, tax_period_t | DAFRC fiscal year; YYYYMM of the selected year-t return |
| status | `tested`; `neighbour_missing`; `no_sched_d_line4_year_t`; `net_assets_nonpositive_or_missing_t`; `no_filed_990_year_t` |
| dafrc_source, dafrc_value, repo_value | DAFRC provenance flag and published value; repo value (applied itemized correction, else DAFRC) |
| line4_prev / _t / _next | Filed Schedule D Part I line 4 (DAF value EOY) for t−1, t, t+1 |
| net_assets_prev / _t / _next | Filed Part X line 33 net assets EOY |
| ratio_prev / _t / _next | line 4 ÷ net assets |
| dpts_vs_prev, dpts_vs_next | ratio_t − neighbour ratio (fractions; 0.10 = 10 points) |
| ratio_break | 1 if both exceed 10 points with the same sign |
| contrib_share_*, grant_share_* | Sch D I-2 ÷ Part VIII 1h; Sch D I-3 ÷ Part IX lines 1–3 |
| contrib_consistent, grants_consistent | 1 if year-t share lies within the neighbours' range ± 10 points |
| npt_pattern | ratio_break and both flows consistent |
| gap_vs_neighbour_ratio | line4_t − mean(neighbour ratios) × net_assets_t |
| over_250m | npt_pattern and \|gap\| > $250m |
| contributions_t, grants_t | Sch D I-2, I-3 in year t |
| other_funds_eoy_prev / _t / _next | Sch D Part I column (b) value EOY |
| rho_t, rho_next | Net-asset return other than contributions and grants (§1.2) |
| roll_forward, roll_backward, roll_mid | DAF roll-forward from t−1, roll-back from t+1, and their mean (ratio breaks only) |
| na_roll_forward, na_roll_backward | NPT net-asset-change roll (b44n27-b39n4 method) |
| roll_verdict, rolls_agree | `filed fails roll-forward` / `filed consistent with roll-forward` / `untestable`; 1 if the two rolls are within 10% |
| filed_minus_roll_mid | line4_t − roll_mid (negative = filed understated) |
| one_sided_* | One-neighbour supplement: which neighbour, its ratio, ratio move, gap, flows check, flag (\|move\| > 10 points, \|gap\| > $250m, flows within 10 points) |
| oid_prev, oid_t, oid_next, xml_url_t | IRS object ids of the three returns; mirror URL of year t |

### 6.2 `tail-realised-fee-rates-2026-11-20.csv` (one row per sampled CF)

| Column | Meaning |
|---|---|
| ein, name, size_band_fy2024, fee_status | From the fee census (wave-34B corrected CSV) |
| group | `publisher` (2021+ rate in the census distribution) or `non_publisher` |
| published_bps_100k | Census effective admin bps at $100k (blank for non-publishers; CF of West Texas shows its pre-2021 100) |
| daf_assets_fy2024 | Census FY2024 corrected DAF assets |
| years_read, years_with_fee, fee_years | FY2022–24 returns read; years with visible fee income; which years |
| fee_total_fy22_24 | Sum of the three components below, FY2022–24 |
| fee_rev_990_fy22_24 | Part VIII revenue lines named as administrative, management, philanthropic or fund fees, or "fee income" |
| fee_recon_990_fy22_24 | Schedule D Part XI line 2d administrative-fee items |
| fee_audit_fy22_24 | Fee income from posted audited statements (Licking County only) |
| realised_bps_total_assets, realised_bps_net_assets | Fee income ÷ average (BOY, EOY) Part X total assets, or net assets, pooled over fee_years; bps |
| fee_per_daf_bps_upper | Fee income ÷ average Sch D I-4 balance; an upper bound on a DAF-only rate (all fees attributed to DAFs) |
| endow_admin_bps, endow_years | Sch D Part V line 1f ÷ average of lines 1a and 1g, pooled FY2022–24; years with data |
| scope, scope_basis | `internal` / `external` / `unknown` / `none visible`, and the filer wording behind it |
| fee_lines_seen, recon_items_seen | The fee lines and Part XI items read, as filed |
| return_object_ids | IRS object ids of the FY2022–24 returns read |
| audit_source_url | Audit used, where any |

The queue-proposals CSV uses the header and format of `queue-proposals-gap19-13.csv`.

---

## 7. Source register

| ID | Source | URL | Accessed | Used in |
|---|---|---|---|---|
| S1 | DAFRC Annual DAF Report 2025, updated-analysis dataset (repo copy `dafrc-sponsor-schedule-d-fy2019-2024.csv`) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | repo | §1.1 |
| S2 | IRS TEOS e-file indexes 2019–2025 | https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv | 2026-11-14 (copies) | §1.1 |
| S3 | IRS TEOS e-file index 2026 | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv | 2026-11-19 (copy) | §1.1 |
| S4 | Form 990 XMLs, all selected returns (object ids in both CSVs) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml | 2026-11-20 | §2, §3 |
| S5 | NPT Form 990 FY Jun-2022 / 2023 / 2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202311359349313966_public.xml ; …/202431429349301368_public.xml ; …/202511339349301311_public.xml | 2026-11-20 | §2.2 |
| S6 | NPT consolidated statements at 2023-06-30 (via wave 34A) | https://www.nptrust.org/consolidated-statements-2023/ | wave 34A | §2.2 |
| S7 | Dechomai Asset Trust Form 990, CY2021 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202243199349331259_public.xml | 2026-11-20 | §2.2 |
| S8 | Dechomai Form 990 CY2020 / CY2022 (object ids in CSV row oid_prev / oid_next) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml | 2026-11-20 | §2.2 |
| S9 | Licking County Foundation, consolidated audited statements 2024 and 2023 (note: administrative fees) | https://www.thelcfoundation.org/file_download/inline/9bb96e42-95b4-48f2-8b7a-cd7a4c2a0c28 | 2026-11-20 | §3 |
| S10 | Pikes Peak CF audited statements 2023, 2024 and 2025 ("Management Fee, Charged to Others") | https://www.ppcf.org/wp-content/uploads/2024/06/PPCF-2023-Final-Audited-Financial-Statements.pdf ; https://www.ppcf.org/wp-content/uploads/2025/06/Signed-Final-Report-and-Financial-Statements-PPCF-2024.pdf ; https://www.ppcf.org/wp-content/uploads/2026/06/PPCF-2025-Audit.pdf | 2026-11-20 | §1.3, §3 |
| S11 | Hutchinson CF Form 990 CY2023 and CY2024 (Sch D Part XI 2d) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423179349300637_public.xml ; …/202523189349310207_public.xml | 2026-11-20 | §3 |
| S12 | Decatur County CF Form 990 CY2021 and CY2024 | …/202242369349301514_public.xml ; …/202501979349300800_public.xml | 2026-11-20 | §3, §4 |
| S13 | Clinton County Foundation (OH) Form 990 CY2024 | …/202512939349301356_public.xml | 2026-11-20 | §3 |
| S14 | Central Florida Foundation Form 990 CY2022–24 (Sch D Part XI 2d "Internal administrative fees") | …/202232559349302258_public.xml ; …/202332499349301958_public.xml ; …/202402439349301500_public.xml | 2026-11-20 | §3 |
| S15 | Census CF homepages (robots log, §5) | `website` column of `long-tail-fee-census-2026-11-19.csv` | 2026-11-20 | §1.3 |
| R1 | Repo | `dafrc-corrections-itemized.csv`; `dafrc-corrected-market-totals.csv`; `long-tail-fee-census-2026-11-19.csv`; `daf-long-tail-sponsors-fy2021-2024.csv`; `b44n27-b39n4-dafrc-data-quality.md`; `b4501-04-tail-fee-pool-revision.md`; validation waves 34A, 34B, 35A | repo | throughout |

**Reproduce** (the cache paths are outside the repo):
```
python3 -I scripts/mission_npt_screen_fees.py . --task fetch  --irs-dir IRS --irs-dir IRS_2026_11_19 --cache CACHE.jsonl --fetch
python3 -I scripts/mission_npt_screen_fees.py . --task screen --irs-dir IRS --irs-dir IRS_2026_11_19 --cache CACHE.jsonl
python3 -I scripts/mission_npt_screen_fees.py . --task fees   --irs-dir IRS --irs-dir IRS_2026_11_19 --cache CACHE.jsonl --text-dir FEEDIR [--fetch]
```
`FEEDIR/audit_txt/` must hold the `pdftotext -layout` text of S9 for the quote check. Without it, the quote check reports "text not cached".
