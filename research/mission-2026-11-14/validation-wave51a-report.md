# Validation wave 51A: sector mix trend, grant size distribution, sponsor operating efficiency

**Validator:** validator wave 51A · **Date:** 2026-11-20 · **Register:** [`data/mission-2026-11-14/validation-register-wave51a.csv`](../../data/mission-2026-11-14/validation-register-wave51a.csv) (41 rows, V51A-01 to V51A-41)

**Studies validated**
- b51-01, sector mix trend: [`b51-01-sector-mix-trend.md`](b51-01-sector-mix-trend.md), `sector-mix-trend-2026-11-20.csv`, `scripts/mission_sector_mix_trend.py`, and the study's FY2021–22 line cache (`b5101/new`).
- b51-03, grant size distribution: [`b51-03-grant-size-distribution.md`](b51-03-grant-size-distribution.md), `grant-size-distribution-2026-11-20.csv`, `scripts/mission_grant_size_distribution.py`.
- b51-04, sponsor operating efficiency: [`b51-04-sponsor-operating-efficiency.md`](b51-04-sponsor-operating-efficiency.md), `sponsor-operating-efficiency-2026-11-20.csv`, `scripts/mission_sponsor_efficiency.py`.
- b51-02 (recipient concentration) was still running and was not touched.

## 1. Method

- **Reruns.** All three scripts were run with `python3 -B`. Outputs went to the session scratchpad: a `--out` path for b51-01, and a scratch root with symlinked inputs for b51-03 and b51-04. Existing caches were reused and nothing new was cached, apart from a 2.6 MB copy of the b51-04 extract cache.
  - b51-01: byte-identical CSV and `run.json`, cache only, 53 s.
  - b51-03: byte-identical CSV (md5 `a2d1008d50878684cdf476593b4cc38b`).
  - b51-04: every one of the 2,267 rows identical.
- **b51-01 independent checks.**
  - Own joins against the committed b39n4-01 CSV.
  - Shares and changes recomputed from the share rows.
  - Fixed-panel and contribution checks.
  - A trace of the Johns Hopkins lines by sponsor through the script's own annotation (read-only import).
  - A new stdlib XML parser, run with `python3 -I`, on 15 freshly fetched returns: 13 random FY2021–22 returns (seed 51), SVCF FY2022 and SVCF FY2023.
- **b51-03 independent checks.**
  - Own recount of all 1,102,444 cached lines with my own DAF-to-DAF whitelist join.
  - Own band counts for Fidelity, JCF and Morgan Stanley GIFT.
  - Re-read of the Fidelity 2022–2026 Giving Report PDFs, the JCF 2023 Giving Report and the MS GIFT 2024 report, extracted with `pdftotext`.
  - Own fit of the n = max(1, k·d^β) rule to JCF's FY2023 bands.
- **b51-04 independent checks.**
  - Own OLS with CR1 sponsor-clustered standard errors (stdlib matrix code), run on the committed CSV for M1, M4 and M5 and the affiliated group, and on `sponsor-cost-structure.csv` for R1.
  - Balanced panel rebuilt from the sponsor-year rows.
  - CPI-U deflation of the trend.
- **Constraints.** No commit or push. Only the two output files were written to the repo. User agent `research-script/1.0`. A path was fetched only when `*`, `research-script/1.0`, ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot were all allowed, or robots.txt returned 404.

### robots.txt log (2026-11-20)

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (NoSuchKey): no rules | 15 return XMLs, parsed in memory, not saved |
| www.fidelitycharitable.org | 200; all checked agents allowed | 5 Giving Report PDFs (2022–2026) |
| jcfny.org | 200; all checked agents allowed | 1 PDF (the study's). Terms not verifiable (HTML pages return 403, per b51-03) |
| www.morganstanley.com | 200; ClaudeBot / anthropic-ai / Claude-Web `Allow: /` | 1 PDF |
| www.minneapolisfed.org | 200; all checked agents allowed | 1 page (CPI-U table, 1913–). Two guessed legal-notice URLs returned 404; no terms page was located |
| www.bls.gov, download.bls.gov | **403, treated as disallowed** | Not fetched |
| data.bls.gov, api.bls.gov | 200, but **disallowed** for every checked agent | Not fetched |
| fred.stlouisfed.org | robots.txt timed out, treated as disallowed | Not fetched |

Not contacted: vanguardcharitable.org, nptrust.org, prnewswire.com (terms ban scripted extraction), sec.gov, crt.sh, certspotter and every off-limits host.

## 2. Counts

| Result | b51-01 | b51-03 | b51-04 | Total |
|---|---|---|---|---|
| Confirmed | 12 | 9 | 9 | 30 |
| Partially confirmed | 2 | 4 | 2 | 8 |
| Contradicted | 0 | 0 | 2 | 2 |
| Unverifiable | 0 | 1 | 0 | 1 |
| **Rows** | **14** | **14** | **13** | **41** |

## 3. Findings

### 3.1 b51-01, sector mix trend: accept, with a judgement on FY2022 and the base year

- **Reproduction.**
  - The rerun is byte-identical.
  - FY2023–24 reproduces b39n4-01 on 620 of 620 overlapping t_a/t_b/t_c rows, amount and line count.
  - b39n4-01 also reports 152 `t_d_t_excluded` rows that are not carried, so "every treatment" is loose.
- **Headline and top-50 tables.** Every share cell reproduces. The change column is the difference of the rounded shares. The CSV change rows give public-society benefit −1.123 (table −1.13), top-50 religion +2.123 (table +2.13) and top-50 health +1.343 (table +1.35). This is immaterial.
- **Robustness.** Same sign in all seven columns for every sector named. Eight §3.2 cells are 0.01 off the CSV; for example, religion's low end is +2.168, so the range is +2.17 to +2.67. The fixed panel holds 1,161 and 42 sponsors. The largest fixed-vs-changing gap is 0.087 pts (all sponsors) and 0.132 pts (top 50).
- **Movers.** The top-1, top-5 and top-10 contributions all match.
  - **Johns Hopkins** rises from $192.3m to $1,044.4m (+1.4359 pts).
  - Traced by sponsor, the FY2023 peak of $1,556.6m is:
    - Fidelity $827.3m;
    - Schwab Charitable $481.8m;
    - JCF $140.7m;
    - NPT $68.8m.
  - It sits on a few very large lines at four June-year-end nationals, so it reflects a few donors, not a sector shift.
- **Structural breaks (raw XML).**
  - **CZ lines (SVCF FY2023):** $586,007,469, $576,046,150, $248,000,000 and $246,500,000.
    - Total $1,656,553,619, of which the three Biohubs $1,070,546,150.
    - DAF-weighted $1,594,822,148 at w2 0.962735 (the doc's $…149 uses the unrounded w2).
  - **Further Future Foundation:** $1,309,000,000.
- **Spot check.** 15 of 15 FY2021–22 lines found in raw XML with the same name and amount. 14 of 14 returns match the cache on line count and on Part IX lines 1 and 3.
- **Judgement: the FY2022 SVCF artefact.**
  - SVCF's FY2022 return has a line 1 of $3,626,886,828 against 3,580 Schedule I lines totalling $2,055,660,472.
  - Its largest line is $108.2m (Evidence Action), and every itemised line exceeds $5,000.
  - The $1.57bn residual therefore cannot be grants of $5,000 or less, and spreading it by the small-gift key is an artefact. It adds about $1.48bn DAF-weighted (3.3% of the $44.27bn base) to the all-sponsor FY2022 allocation.
  - It distorts FY2022 full-layer shares only. For example, public-society benefit is 11.54 (base), 11.70 (ex SVCF) and 12.27 (`sched_i`). The FY2021 and FY2024 endpoints are untouched.
  - The doc already points readers to the variants. **Accept**, and add the size of the effect.
- **Judgement: a pandemic-high FY2021 base.**
  - **The risk is real.** Fidelity's 2022 Giving Report says 2020 saw "a surge of granting activity to the human services sector" and that 2021 grant volumes "remained elevated from pre-pandemic norms" while dollars "retracted somewhat".
  - **Fidelity's own dollar share** for human services: 14% (2021), 16% (2022), 14% (2023), 13% (2024) and 12.2% (2025).
  - **Why FY2021 is exposed.** FY2021 here includes July 2020 – June 2021 at the June-year-end nationals.
  - **Reading.** −2.42 pts is best read as an upper bound on the structural decline. The religion (+2.50) and environment (+1.23) gains do not depend on this.

### 3.2 b51-03, grant size distribution: accept the numbers; modify the line-vs-grant and β readings

- **All computed figures reproduce.**
  - Bins and shares.
  - Median line $18,650 and mean $152,053.
  - Mega-line shares by year: 68.3 / 65.7 / 65.0 / 65.5% and 42.6 / 37.6 / 37.2 / 36.7%.
  - Without DAF-to-DAF: 60.8% / 30.4%.
  - Segment rows.
  - Average grant from stated counts.
  - My independent recount differs only by the two Greater Horizons totals rows ($0.21bn) that the study drops.
- **Published figures re-read verbatim.**
  - Fidelity averages $4,407 / $4,798 / $4,625 / $5,422 / $5,801, and $1m+ grants 1,180 / 1,407 / 1,345 / 1,971 / 2,141. The 2026 report restates CY2023 as $4,614.
  - JCF FY2023: median $750, average $11,639, bands 75,380 / 1,908 / 76 of 77,364.
  - MS GIFT: "$11,000 Average Grant Size", 122,000 grants in 2024.
- **Line vs grant (modify).**
  - The ratio of grants to lines divides grants to *all* recipients by *itemised* lines.
  - **Fidelity:** 2,664,446 CY2024 grants went to 213,000 unique nonprofits (2025 Giving Report), which is 12.5 per recipient, not 33 per line.
  - **JCF:** grants went to more than 10,600 charities against 4,340 itemised lines. Its 75,380 sub-$50k grants therefore spread over about 9,200 recipients, about 8 each, not 25.5.
  - **The top-end match (Fidelity 1.00–1.15) shows about one $1m+ grant per $1m+ line.** It does not show that the line holds only one grant.
- **β (modify).**
  - Under the model's own assumption (equal-size grants within a recipient line), β ≈ 1 is indeed ruled out. My fit to JCF FY2023 gives these predicted counts for under $50k / $50k–$1m / over $1m, against the published 75,380 / 1,908 / 76:

    | β | Predicted counts |
    |---|---|
    | 0 | 75,444 / 1,832 / 88 |
    | 0.2 | 79 over $1m |
    | 0.35 and above | 0 over $1m |
    | 0.75 and above | 0 of $50k or more |

  - That agrees with g0401-g0502 §B5 (Fidelity: zero modelled $1m+ grants for β ≥ 0.40).
  - **The pooled broad per-grant exception share is therefore about 28–31%** (31.2% at β = 0, 29.6% at β = 0.25), not 17–31%. The core share (7–8.5%) is unaffected.
  - **Caveats.** One single-issue sponsor-year. Within-line heterogeneity (one large grant plus many small ones) is not identified, so β ≤ 0.35 is a working range, not an estimate.
- **AI-economics docs.** No correction. The β in [`ai-economics-v2-observed-costs.md`](ai-economics-v2-observed-costs.md) is the conventional-automation efficiency share, a different parameter. Its log-uniform $5–40k grant-size input spans the observed averages ($4.5k at RCF to $43k at NPT). P-B5103-04 (a two-tier size model) stays open.
- §11 paragraphs of earlier waves are not edited.

### 3.3 b51-04, sponsor operating efficiency: accept the core results; correct stale regression values; modify the trend reading

- **Confirmed independently.** I re-estimated these with my own OLS and clustered SE code:
  - CF M1 0.636 (SE 0.0549; 451 / 113; r² 0.6915);
  - R1 CF universe 0.5559 (SE 0.0353; 2,076 / 703);
  - M4 total assets 0.7767 (SE 0.0928), DAF terms 0.0314 (SE 0.0834);
  - affiliated nationals 1.0135 (SE 0.0761, r² 0.917).
- **Contradicted (stale values).**
  - The doc prints several values from an earlier run. The script was changed and the CSV regenerated at 16:29, after the doc (16:28). The scratch run logs show the change between run4 and run5.
  - **Committed and reproducible:**
    - M5 dummy **−1.809** (SE 0.391), not −1.818 (0.398);
    - M5 sum 0.404;
    - single-issue M1 0.070 (SE 0.156; 163 obs), not 0.094 (0.146; 166);
    - single-issue M4 −0.464 / total assets 1.143;
    - affiliate/zero nationals 0.564 (62 obs);
    - affiliate/zero CF + single-issue 0.553 (80 / 25), not 0.453 (77 / 24).
  - No reading changes. "84% less" still holds (exp(−1.809) = 0.164).
- **Confirmed (other).**
  - The 15 zero-employee top-50 sponsors (14 `affiliate_staffed` and American Gift Fund).
  - Balanced-panel changes:
    - opex +35.0%;
    - DAF assets +9.4%;
    - accounts +6.4%;
    - employees +14.0%;
    - bps **+21.3%**;
    - per account **+25.0%**.
  - Bands: rule-A medians of 79.9 / 117.9 / 149.2 / 372.7 bps.
  - Agreement checks: 392/392, 183/183 and 183/183, and 165/165 with b45n33 (102 bps, $12,036).
  - Grants per employee: 117 to 5,670.
- **Fee vs cost (partially).** The numbers match the CF fee census (100 / 100 / 67 bps; 1.7× / 2.2× / 3.5–4.5×). But the national 23 bps is a Part IX floor (the study's own M5 puts affiliate/zero-staff opex at 0.16×). The comparison also mixes account-balance fee tiers with sponsor-size cost bands. The conclusion "CFs are not pricing above cost relative to nationals" is therefore weak.
- **"Efficiency fell" (modify).** BLS hosts are robots-blocked, so I used CPI-U annual averages from the Minneapolis Fed table, which tabulates the BLS series: 271.0 (2021), 292.7, 304.7 and 313.7 (2024), +15.8%. On the same 112 CFs, the median within-sponsor changes are:

  | Measure | Change |
  |---|---|
  | Real opex | +16.6% |
  | Real DAF assets | −5.5% |
  | Employees | +14.0% |
  | Real opex per employee | **−0.1%** |
  | Real opex per account | **+8.0%** (pooled +2.7%) |
  | Opex per DAF grant dollar | **+0.7%** (n = 103) |
  | Whole-org bps from FY2021 | +21.3% |
  | Whole-org bps from FY2022 | −4.0% |
  | Whole-org bps from FY2023 | −2.8% |

  - Pooled DAF assets were $39.17bn, $33.53bn, $33.80bn and $39.77bn.
  - **Reading.** The bps deterioration is mostly the FY2021 market-peak base plus headcount growth at flat real cost per head. "Efficiency fell" survives only as a modest real rise in cost per account. Cost per grant dollar did not worsen.

## 4. Accept / modify / reject

| Study | Claim | Decision | Note |
|---|---|---|---|
| b51-01 | FY2023–24 reproduces b39n4-01 (620/620) | Accept | Wording fix: t_d rows not carried (V51A-01) |
| b51-01 | Headline changes (religion +2.50, human services −2.42, environment +1.23, …) | Accept | Rounded-share convention; CSV PSB −1.123 (V51A-02) |
| b51-01 | Robust across 7 variants | Accept | 8 cells 0.01 off; signs hold (V51A-04) |
| b51-01 | Fixed panel 1,161 / 42; within 0.09 / 0.13 pts | Accept | V51A-05 |
| b51-01 | Johns Hopkins +1.44 pts masks a larger education fall | Accept | Add sponsor trace (V51A-07) |
| b51-01 | CZ $1.66bn / $1.59bn; Further Future $1.309bn | Accept | Raw XML (V51A-08, -09) |
| b51-01 | FY2022 SVCF allocation; use variants | Modify | Quantify: about $1.48bn (3.3% of base) is an artefact (V51A-12) |
| b51-01 | FY2021 may be a pandemic high | Modify | Supported by Fidelity; read −2.42 as an upper bound (V51A-13) |
| b51-03 | Bins, median $18,650, mean $152,053, mega shares, 60.8% / 30.4%, segments | Accept | V51A-16 to -20 |
| b51-03 | Published Fidelity, JCF, MS GIFT statistics | Accept | Re-read verbatim (V51A-21, -23, -24) |
| b51-03 | Top end: one line ≈ one grant | Modify | About one $1m+ grant per $1m+ line (V51A-22) |
| b51-03 | 25.5 grants per sub-$50k line; 7–33 grants per line | Modify | Includes unitemised recipients; about 8 and 12.5 per recipient (V51A-23, -26) |
| b51-03 | β near 1 ruled out | Modify | Holds within the model; the fit gives β ≈ 0–0.3, so broad share is about 28–31% (V51A-27) |
| b51-04 | CF elasticity 0.636; universe 0.556; M4 0.777 / 0.031; affiliated 1.014 | Accept | Independent OLS (V51A-30 to -32) |
| b51-04 | Dummy −1.818 and other single-issue / affiliate subset values | Reject (as printed) | Stale run; use the CSV values (V51A-33, -34) |
| b51-04 | 15 zero-employee; balanced-panel changes; band bps; repo agreement; grants per employee | Accept | V51A-35 to -39 |
| b51-04 | Fees vs cost: CFs not pricing above cost | Modify | National cost is a floor; weak (V51A-40) |
| b51-04 | Efficiency fell at CFs | Modify | Real cost per employee flat; real cost per account +8% (V51A-41) |

## Terms-restricted provenance (owner decision)

- **What b51-03 flags (P-B5103-03).** Earlier repo values were fetched from hosts whose site terms ban automated extraction. The rule sheet lists www.vanguardcharitable.org, www.nptrust.org and www.prnewswire.com.
- **What this wave did.** Nothing was re-read and nothing is corrected or deleted here. The rows below are recorded for the owner, who can choose to:
  - keep them as owner-verified;
  - re-read them manually;
  - or drop them.

| File | Rows | Host | Used downstream by |
|---|---|---|---|
| `grant-count-denominators-2026-11-20.csv` | GC-002 (NPT 129,575 grants, FY2024; primary) | nptrust.org | b51-03 NPT average grant ($42,935) and grants per line (7.0); b51-04 NPT grants per employee (453) and opex per grant ($474) |
| same | GC-006 (Vanguard 2024 annual report; not primary) | vanguardcharitable.org | none as primary (the Vanguard primary row GC-005 is from its Form 990) |
| same | GC-016 (JCF 89,485 grants and $1bn, FY2024; primary) | prnewswire.com | b51-03 JCF average ($11,175) and grants per line (19.1); b51-04 JCF grants per employee (3,891) and opex per grant ($89) |
| same | GC-021 (Blackbaud Giving Fund; not primary) | prnewswire.com | none in these studies |
| `sponsor-published-grant-stats-2026-11-19.csv` (b4013-b4428) | 21 rows: A-NPT-FY15, -FY20, -FY21, -FY23, -FY24, -FY25; A-VC-CY2020, -CY2021, -2022-12, -CY2022, -2023-04, -FY2023, -CY2023, -FY2024, -FY2025, -CY2025; B-VC-anon-4, -5; B-NPT-FY20, -FY21, -qual | nptrust.org, vanguardcharitable.org | unrestricted and anonymous grant-share statistics. A-NPT-FY15, A-NPT-FY20, A-VC-CY2020 and B-NPT-FY20 are also pre-2021 |
| `exception-share-per-grant-2026-11-19.csv` (g0401-g0502) | 4 `published_grants_G` rows: NPT FY2023 106,235 and FY2024 129,575; Vanguard 202,500 and 224,532 | nptrust.org, vanguardcharitable.org | the three-sponsor per-grant pools (§B4), including the β discussion above |

- **Wider footprint (context only).** Other data files cite these hosts. Most are citation, link-health or watchlist records rather than extracted values, for example:
  - `sponsor-pool-returns-2021-2025.csv`: 72 vanguardcharitable.org and 21 nptrust.org mentions;
  - `daf-market-annual-series.csv`: 130 nptrust.org mentions;
  - `company-timeline-events.csv`: 11 prnewswire.com mentions.
- They were not reviewed row by row. That review is part of the same owner decision.

## 5. Limits

- **Pandemic base (b51-01).** I did not build FY2019–20 sector shares. The pandemic-base judgement rests on Fidelity's published text and shares, not on filings.
- **β fit (b51-03).**
  - It uses one sponsor-year.
  - It uses JCF's ">10,600 charities", and the unitemised recipients are taken as that figure minus the itemised lines (Schedule F recipients ignored).
  - It uses JCF's stated "over $900 million" (as average × count) for unitemised dollars.
- **CPI (b51-04).**
  - Annual averages are matched to the calendar year of each fiscal-year end.
  - Monthly matching of June year-ends was not possible without a BLS host.
  - CPI-U is a price index, not a nonprofit wage index (the Employment Cost Index was not reachable).
- **Terms-restricted rows** were not re-read.

## Exact corrections

23 items. Each Find occurs exactly once in its file, alone and after the earlier items for that file are applied in order (checked by script). `\n` denotes a newline.

### `research/mission-2026-11-14/b51-01-sector-mix-trend.md`

**Find:** "(both scopes, both bases, every treatment and layer b39n4-01 reports per FY)"
**Replace with:** "(both scopes, both bases, treatments t_a, t_b and t_c, every layer; b39n4-01’s 152 t_d_t_excluded rows for these cells are not carried) [V wave 51A]"

**Find:** "so the rest of education lost about 2.7 pts of itemised share [F/I]."
**Replace with:** "so the rest of education lost about 2.7 pts of itemised share [F/I]. The Johns Hopkins dollars sit on a few very large lines at four June-year-end nationals (DAF-weighted): FY2023 Fidelity $827.3m, Schwab Charitable $481.8m, JCF $140.7m, NPT $68.8m; FY2024 Schwab $517.2m, Fidelity $272.4m, NPT $188.2m, JCF $28.0m (FY2021: Schwab $116.5m, JCF $32.3m). [V wave 51A]"

**Find:** "The top-50 sub-$5,000 component is therefore $2.31bn in FY2022, against $0.67–1.25bn in other years."
**Replace with:** "The top-50 sub-$5,000 component is therefore $2.31bn in FY2022, against $0.67–1.25bn in other years. The raw return (object 202333189349318948) confirms line 1 of $3,626,886,828 against 3,580 Schedule I lines totalling $2,055,660,472, the largest $108.2m. A $1.57bn residual cannot be grants of $5,000 or less, so spreading it by the small-gift key is an artefact. It adds about $1.48bn DAF-weighted to the all-sponsor FY2022 allocation (full-itemiser sub-$5,000 component $2.55bn with SVCF, $1.07bn without), 3.3% of the $44.27bn base. The FY2021 and FY2024 endpoints are untouched. [V wave 51A]"

**Find:** "FY2021 is the first year, and human services may be at a pandemic-era high in it (P-B5101-01)."
**Replace with:** "FY2021 is the first year, and human services may be at a pandemic-era high in it (P-B5101-01). Fidelity Charitable’s 2022 Giving Report supports this: “In 2020, urgent needs related to the COVID-19 pandemic created a surge of granting activity to the human services sector” and in 2021 grant volumes “remained elevated from pre-pandemic norms”. Its human-services share of grant dollars is 14% (2021), 16% (2022), 14% (2023), 13% (2024) and 12.2% (2025). FY2021 here includes July 2020–June 2021 at June-year-end nationals, so read −2.42 as an upper bound on the structural decline. [V wave 51A]"

### `research/mission-2026-11-14/b51-03-grant-size-distribution.md`

**Find:** "**Top end: one line ≈ one grant.**"
**Replace with:** "**Top end: about one $1m+ grant per $1m+ line** (how many smaller grants share the line is not observed). [V wave 51A]"

**Find:** "stand for 75,380 grants under $50k (**25.5 grants per line**)."
**Replace with:** "stand for 75,380 grants under $50k (**25.5 grants per line**). JCF reports grants to more than 10,600 charities against 4,340 itemised lines, so about 6,260 recipients of $5,000 or less share those grants: about 8 grants per small recipient. [V wave 51A]"

**Find:** "at the sponsors with counts (Fidelity 33, DAFgiving360 20, JCF 19, Vanguard 9, NPT 7)."
**Replace with:** "at the sponsors with counts (Fidelity 33, DAFgiving360 20, JCF 19, Vanguard 9, NPT 7). The ratio divides grants to all recipients, itemised or not, by itemised lines. Per recipient it is lower: Fidelity’s 2,664,446 CY2024 grants went to 213,000 unique nonprofits (12.5 each; 2025 Giving Report), and JCF’s 77,364 FY2023 grants to more than 10,600 charities (about 7.3). [V wave 51A]"

**Find:** "     - At the top, a $1m+ line holds about one grant (Fidelity 1.00–1.15; JCF 0.70). Under β = 1 (equal-size grants) a $1m line would hold on the order of 200 grants at a $5k average, so **β near 1 is ruled out**."
**Replace with:** "     - At the top, a $1m+ line holds about one grant of $1m or more (Fidelity 1.00–1.15; JCF 0.70); how many smaller grants share it is not observed. Under β = 1 (equal-size grants) a $1m line would hold on the order of 200 grants of about $5k and no grant of $1m or more, so **β near 1 is ruled out within the model’s equal-size-per-line assumption**. A validator fit of the same rule to JCF FY2023 (4,340 lines plus about 6,260 unitemised recipients sharing $49.6m; 77,364 grants) reproduces the published bands (75,380 / 1,908 / 76) best at β = 0–0.2 (β = 0: 75,444 / 1,832 / 88), gives no grant over $1m from β = 0.35 and none of $50k or more from β = 0.75. [V wave 51A]"

### `research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md`

**Find:** "- **Broad proxy.** **17–31% of grants**, against 28.0% of lines and 17.5% of dollars. Here the grant-size rule decides the answer."
**Replace with:** "- **Broad proxy.** **17–31% of grants**, against 28.0% of lines and 17.5% of dollars. Here the grant-size rule decides the answer. Size-band evidence from b51-03 (JCF FY2023 bands; Fidelity $1m+ counts) favours β of about 0–0.3, which puts the pooled broad share at about 28–31% (31.2% at β = 0, 29.6% at β = 0.25). [V wave 51A]"

**Find:** "so the broad share (17–31%) depends on an assumption that is swept, not estimated (P-G0502-01)."
**Replace with:** "so the broad share (17–31%) depends on an assumption that is swept, not estimated (P-G0502-01). Later evidence narrows it. Fitted with this rule, JCF’s FY2023 grant-size bands (75,380 / 1,908 / 76 grants under $50k / $50k–$1m / over $1m; b51-03) match best at β = 0–0.2, and β ≥ 0.35 gives no grant over $1m, consistent with the Fidelity moment in §B5. On that reading the pooled broad share is about 28–31%, not the low end of the range; the core share (7–8.5%) is unaffected. The basis is one single-issue sponsor-year and the equal-size-per-line assumption, so treat β ≤ 0.35 as a working range, not an estimate. [V wave 51A]"

### `research/mission-2026-11-14/b51-04-sponsor-operating-efficiency.md`

**Find:** "The DAF-scale elasticity is 0.09 (SE 0.15), and opex follows total assets (1.15) [C]."
**Replace with:** "The DAF-scale elasticity is 0.07 (SE 0.16), and opex follows total assets (1.14) [C] (committed-CSV values; the earlier figures came from a superseded run). [V wave 51A]"

**Find:** "operating cost (dummy −1.82, SE 0.40) [C]."
**Replace with:** "operating cost (dummy −1.81, SE 0.39) [C]. [V wave 51A]"

**Find:** "| Single-issue, own staff | M1 opex | 0.094 | 0.146 | 166 / 45 | 0.26 | 0.824 | −0.730"
**Replace with:** "| Single-issue, own staff | M1 opex | 0.070 | 0.156 | 163 / 45 | 0.27 | 0.839 | −0.769 [V wave 51A]"

**Find:** "| Single-issue, own staff | M4 + ln total assets | −0.457 (DAF terms) | 0.132 | 166 / 45 | 0.72 | – | – (total assets **1.146**)"
**Replace with:** "| Single-issue, own staff | M4 + ln total assets | −0.464 (DAF terms) | 0.134 | 163 / 45 | 0.72 | – | – (total assets **1.143**) [V wave 51A]"

**Find:** "| Affiliate/zero staff, nationals ex processors | M1 opex | 0.568 | 0.089 | 60 / 17 | 0.74 | 0.185 | 0.383"
**Replace with:** "| Affiliate/zero staff, nationals ex processors | M1 opex | 0.564 | 0.091 | 62 / 17 | 0.72 | 0.216 | 0.348 [V wave 51A]"

**Find:** "| Affiliate/zero staff, CFs and single-issue | M1 opex | 0.453 | 0.137 | 77 / 24 | 0.48 | 0.963 | −0.511"
**Replace with:** "| Affiliate/zero staff, CFs and single-issue | M1 opex | 0.553 | 0.118 | 80 / 25 | 0.50 | 0.923 | −0.371 [V wave 51A]"

**Find:** "| All usable | M5 pooled, with dummies | 0.394 | 0.056 | 800 / 206 | 0.55 | 0.631 | −0.237"
**Replace with:** "| All usable | M5 pooled, with dummies | 0.404 | 0.056 | 800 / 206 | 0.55 | 0.619 | −0.215 [V wave 51A]"

**Find:** "| All usable | M5 **affiliate/zero-staff dummy** | **−1.818** | 0.398"
**Replace with:** "| All usable | M5 **affiliate/zero-staff dummy** | **−1.809** | 0.391 [V wave 51A]"

**Find:** "- **[C] The pooled dummy of −1.82 means affiliate- and zero-staff sponsors report exp(−1.82) = 0.16 times the opex of an own-staff sponsor of the same type, assets and accounts.**"
**Replace with:** "- **[C] The pooled dummy of −1.81 means affiliate- and zero-staff sponsors report exp(−1.81) = 0.16 times the opex of an own-staff sponsor of the same type, assets and accounts.** [V wave 51A]"

**Find:** "FY2021 year-end asset values sit near a market peak, which flatters the FY2021 bps figures [I]."
**Replace with:** "FY2021 year-end asset values sit near a market peak, which flatters the FY2021 bps figures [I]. Deflated by CPI-U (271.0 → 313.7, +15.8%), real opex rose 16.6%, real opex per employee was flat (−0.1%), real opex per account rose 8.0% and opex per DAF grant dollar 0.7%; bps fell 4.0% from FY2022. Most of the bps rise is the FY2021 base and headcount growth. [V wave 51A]"

**Find:** "The bps figures peak in FY2023, not FY2024."
**Replace with:** "The bps figures peak in FY2023, not FY2024. Validator check on the same 112 CFs, with CPI-U annual averages 271.0 / 292.7 / 304.7 / 313.7 (2021–24; the BLS series as tabulated by the Minneapolis Fed, because bls.gov robots.txt returns 403 to a scripted client): median within-sponsor real opex +16.6%, real DAF assets −5.5%, employees +14.0%, real opex per employee −0.1%, real opex per account +8.0% (pooled +2.7%), opex per DAF grant dollar +0.7% (n = 103). Whole-org bps rose 21.3% from FY2021 but fell 4.0% from FY2022 and 2.8% from FY2023, while pooled DAF assets were $39.17bn, $33.53bn, $33.80bn and $39.77bn. So “efficiency fell” holds only as a modest real rise in cost per account; cost per employee and per grant dollar did not worsen. [V wave 51A]"

**Find:** "CFs are not pricing above their cost relative to nationals [I]."
**Replace with:** "CFs are not pricing above their cost relative to nationals [I]. This is weak: the 23 bps national figure is a Part IX floor (the M5 dummy puts affiliate- and zero-staff opex at 0.16 times own-staff opex at equal scale), and fees are by account balance while costs are by sponsor size. [V wave 51A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.77 DAF grant sectors, grant sizes and sponsor efficiency (validated, wave 51A)\n\n**DAF grant sectors, grant sizes and sponsor efficiency** (validated, wave 51A). Scratch reruns reproduced the three wave-51 CSVs exactly, and fresh raw-XML reads matched 15 of 15 sampled FY2021–22 Schedule I lines. Among itemising sponsors outside universities and hospitals, religion’s share of DAF-weighted grant dollars rose 2.50 points from FY2021 to FY2024 and human services fell 2.42, in every variant; part of that fall may reflect a pandemic-high FY2021 base, which Fidelity Charitable’s 2022 report describes. SVCF items (the FY2023 CZ and Further Future grants and a $1.57bn unitemised FY2022 residual) move single years, not the endpoints. Lines of $1m or more carry about two-thirds of itemised dollars, but a Schedule I line is a recipient-year total: Fidelity made 12.5 grants per recipient in 2024. JCF’s size bands fit a grant-size elasticity of 0–0.3, which puts the broad per-grant exception share near 28–31%. Community-foundation cost per DAF dollar rose 21% in nominal terms; deflated by CPI-U, cost per employee was flat and cost per account rose 8% (repo [`validation-wave51a-report.md`](mission-2026-11-14/validation-wave51a-report.md)). [V wave 51A]\n\n---\n\n## Source register"
