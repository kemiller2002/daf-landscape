# Recipient sector mix of DAF grant dollars, FY2021 to FY2024 (b51-01)

**Date:** 2026-11-20 · **Task ID:** b51-01 · **Builds on:** [b39n4-01-sector-join-all-sponsors.md](b39n4-01-sector-join-all-sponsors.md) (pooled FY2023–24 join; validated byte-identical in [wave 43A](validation-wave43a-report.md), whose corrections are applied here: t_b is a size-only fit and its base double counts; the plus_foreign layer is $75.99bn, not $77.91bn; the t_a / t_c convention is [I])

**Outputs**
- Script: [`scripts/mission_sector_mix_trend.py`](../../scripts/mission_sector_mix_trend.py). It is new. It imports `mission_sector_join_all.py`, `mission_recipient_sectors.py` and `mission_coverage_gap.py` and modifies none of them.
- Data: [`data/mission-2026-11-14/sector-mix-trend-2026-11-20.csv`](../../data/mission-2026-11-14/sector-mix-trend-2026-11-20.csv), 23,568 rows (data dictionary in §7).
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b51-01.csv`](../../data/mission-2026-11-14/queue-proposals-b51-01.csv) (P-B5101-01 to 06).

**Tags:** [F] computed from filings by the script · [I] inference or allocation assumption.

**Rules applied.** All data are FY2021–FY2024 returns. robots.txt was checked before fetching (§6). sec.gov was not used. No outreach, logins or forms. No existing repo file was modified; nothing was committed.

---

## 0. Answers in brief

Headline basis: all itemising DAFRC panel sponsors excluding university/hospital sponsors (the b39n4-01 headline scope), DAF-weighted, treatment t_a (DAF-to-DAF excluded, NTEE T inside public-society benefit), full layer (Schedule I + foreign line 3 + allocated sub-$5,000 grants). Changes are FY2024 minus FY2021, in percentage points [F].

| Sector | FY2021 | FY2022 | FY2023 | FY2024 | Change | Robust? |
|---|---|---|---|---|---|---|
| Education | 23.55 | 22.20 | 23.35 | 22.66 | −0.89 | Sign robust, but one recipient (Johns Hopkins, +1.44) masks a larger underlying fall |
| Religion | 12.15 | 13.73 | 13.38 | 14.65 | **+2.50** | **Yes**: +2.16 to +2.67 in every variant; broad-based |
| Human services | 17.66 | 16.25 | 13.87 | 15.24 | **−2.42** | **Yes**: −2.35 to −2.57 in every variant; broad-based; FY2021 may be a pandemic-era high |
| Health | 7.12 | 8.43 | 10.57 | 8.00 | +0.88 | Endpoint yes (+0.76 to +1.21); the FY2023 spike is the CZ LLC grants |
| Arts and culture | 6.61 | 6.00 | 5.08 | 5.91 | −0.70 | Yes (−0.49 to −0.86) |
| International (NTEE Q) | 4.89 | 6.46 | 5.15 | 5.44 | +0.55 | Small; FY2022 peak |
| Environment and animals | 4.79 | 4.99 | 5.14 | 6.02 | **+1.23** | **Yes** (+1.14 to +1.56); rises every year |
| Public-society benefit (incl. T) | 13.89 | 11.54 | 13.63 | 12.76 | −1.13 | Sign yes (−0.63 to −1.44); FY2023 inflated by one $1.31bn grant |
| of which NTEE T (t_c) | 6.66 | 5.69 | 5.49 | 5.93 | −0.73 | |
| Foreign grants (Schedule F) | 2.40 | 3.28 | 3.06 | 3.17 | +0.77 | Yes |
| Unclassified | 6.40 | 6.47 | 6.25 | 5.61 | −0.79 | Partly classification drift (§5) |
| Base, $bn | 38.40 | 44.27 | 47.09 | 53.93 | | |

- **Top-50 sponsors** (46 ex university/hospital in FY2024, 42 in FY2021–22) show the same pattern: religion +2.13, human services −2.68, environment +1.33, health +1.35, public-society benefit −1.22, education −0.68 [F].
- **Sponsor mix does not drive the changes.** On a fixed panel of sponsors itemising in all four years (1,161 sponsors; 42 at the top 50), every FY2021–24 change is within 0.15 pts of the changing-panel figure [F].
- **Structural breaks.** The FY2023 Chan Zuckerberg LLC grants from SVCF ($1.66bn filed; **$1.59bn DAF-weighted**) raise health by 3.15 pts in FY2023 alone and leave the FY2021–24 endpoints unchanged. One $1.31bn FY2023 SVCF grant to Further Future Foundation lifts public-society benefit by 2.7 pts that year. SVCF's FY2022 return leaves $1.57bn of line 1 unitemised, which the sub-$5,000 rule allocates (§4) [F].
- **t_b** (DAF-to-DAF kept; comparable with sponsor-published splits, base double counts): public-society benefit 26.78 → 25.29 (−1.49), religion +2.05, human services −1.90 [F].

---

## 1. Method

### 1.1 Reuse of the validated pipeline
- **Universe.** Every DAFRC 2025 panel sponsor-year FY2021–FY2024 in the netpayout990 cache, return chosen with `mission_daf_to_daf.pick_returns`, and itemising Schedule I Part II (`mission_net_payout.itemized` and a non-zero line count). This is the b40n1202-01 / b39n4-01 rule (`mission_non_top50_numerator.sponsor_years`) with FY2021–22 added. FY = calendar year of the tax-period end.
- **Top 50** is the fixed FY2024 DAF-asset ranking (`top_n`), as in b39n4-01, so "top-50" in FY2021 means the same 50 organisations, not the FY2021 top 50.
- **Scopes.** `top50_ex_university_hospital` and `all_ex_university_hospital` (b39n4-01's headline scopes; university/hospital sponsors are operating institutions with small DAF books).
- **Lines.**
  - FY2023–24: the committed caches `rcp/lines` and `q120201/lines`, read with `mission_recipient_sectors.load_lines` (no fetch).
  - FY2021–22: not cached before this study. Each chosen return's XML was streamed once from the GivingTuesday mirror of IRS TEOS, parsing every Schedule I `RecipientTable` with `mission_recipient_sectors.line_of` and Part IX lines 1–3 with `mission_coverage_gap.P9_TAGS`, into a gzip cache. A sponsor-year is used only when the parsed line count equals the cache's `sched_i_lines`: **all 2,660 FY2021–22 itemising sponsor-years matched** (5,365 of 5,365 across the four years loaded `ok`).
  - Filer totals rows are dropped (`drop_totals_rows`).
- **Join.** `rs.load_bmf` + `rs.annotate`, unchanged: DAF-to-DAF whitelist flags, NTEE major group, BMF FOUNDATION-code and name-rule fallbacks. One BMF snapshot (IRS EO BMF, Last-Modified 2026-11-09) is used for all years.
- **DAF weight** w2 = min(1, corrected DAFRC DAF grants ÷ (L1 + L3)).
  - FY2023–24: from `coverage-gap-decomposition-2026-11-20.csv`, as b39n4-01.
  - FY2021–22: `mission_coverage_gap.sponsor_row` on the new Part IX extract, DAFRC raw DAF grants and the applied `dafrc-corrections-itemized.csv` deltas. Four FY2021–22 sponsor-years lacked a Part IX line 1 tag and fall back to the cache's line 1 with L3 = 0 (Alabama Civil Justice Foundation, Greater Milwaukee Foundation and Greater Poweshiek CF FY2021; Puerto Rico CF FY2022).
- **Shares.** `sja.sy_aggregate`, `scaled`, `scope_fy` and `vector`, per FY. The sub-$5,000 component (L1 − Schedule I) is allocated per FY and scope by the `small10` key for full itemisers and pro rata for partial itemisers (b40n120201-01 / wave-41B rules).
- **Treatments.** t_a (primary), t_b (DAF-to-DAF kept, classed by the receiving sponsor's NTEE; base double counts, so never a market share, per wave 43A), t_c (NTEE T as its own line). **Layers:** `sched_i`, `plus_foreign`, `plus_foreign_sub5k` (headline). **Bases:** `daf_weighted` (headline) and `schedule_i`.

### 1.2 Reproduction check
For FY2023 and FY2024, the changing-panel, base-variant rows reproduce b39n4-01's committed CSV: **620 of 620 overlapping rows** (both scopes, both bases, treatments t_a, t_b and t_c, every layer; b39n4-01’s 152 t_d_t_excluded rows for these cells are not carried) [V wave 51A] **match to the dollar** [F].

### 1.3 Robustness variants
- **Panels.** `changing`: every itemising sponsor-year in the scope that FY. `fixed`: only sponsors itemising (lines loaded) in all four FYs: 1,161 sponsors (all ex university/hospital) and 42 (top 50).
- **Variants.**
  - `base`.
  - `ex_cz`: lines to Chan Zuckerberg LLC recipients are removed (name rule `BIOHUB | ^CZ | CHAN ZUCKERBERG`). The same dollars are removed from that sponsor-year's line 1, so they do not re-enter as sub-$5,000 grants. The rule also catches CZ Wellness Group (a camp, $8–100k a year) and Charlottesville Biohub ($25k), immaterial.
  - `ex_svcf`: Silicon Valley Community Foundation dropped entirely.
- **Recipient contributions.** For FY pairs, each recipient's contribution to its sector's share change = a(r, FY1) ÷ T(FY1) − a(r, FY0) ÷ T(FY0) (t_a, DAF-weighted, changing panel, base). Summed over a sector, this equals the change in the sector's itemised share; the remainder of the sector change is the sub-$5,000 allocation.

## 2. Coverage [F]

| | FY2021 | FY2022 | FY2023 | FY2024 |
|---|---|---|---|---|
| Panel sponsor-years with a return | 1,523 | 1,541 | 1,552 | 1,545 |
| Itemising, lines loaded ok | 1,334 | 1,326 | 1,347 | 1,358 |
| Of which ex university/hospital | 1,231 | 1,222 | 1,242 | 1,253 |
| Of which top 50 ex university/hospital | 42 | 42 | 44 | 46 |
| Schedule I lines (all itemising) | 445,196 | 489,820 | 520,170 | 572,639 |
| DAF-weighted base, all ex u/h (t_a, full layer) | $38.40bn | $44.27bn | $47.09bn | $53.93bn |
| DAF-weighted base, top 50 ex u/h | $30.57bn | $34.97bn | $36.31bn | $41.60bn |

- **Distinct recipient EINs** over the four years: 326,476, of which 266,249 are in the BMF.
- **Classification mix** (filed, non-DAF-to-DAF): NTEE-coded 77.1% / 78.3% / 75.7% / 79.4%; EIN not in BMF 2.2% / 1.9% / 1.8% / 1.9%; name rule 8.3% / 7.1% / 10.0% / 6.7%. The FY2023 name-rule peak is the CZ LLCs, which are not in the BMF and are classed health by the `BIOHUB` / `BIOLOGICAL` rule.

## 3. Results

### 3.1 Year-by-year shares (t_a, DAF-weighted, full layer, changing panel) [F]
The all-sponsor table is in §0. Top 50 ex university/hospital:

| Sector | FY2021 | FY2022 | FY2023 | FY2024 | Change |
|---|---|---|---|---|---|
| Education | 25.38 | 23.57 | 25.51 | 24.70 | −0.68 |
| Religion | 12.26 | 14.63 | 13.43 | 14.39 | +2.13 |
| Human services | 17.28 | 15.50 | 13.28 | 14.60 | −2.68 |
| Health | 6.86 | 8.42 | 11.48 | 8.21 | +1.35 |
| Arts and culture | 6.84 | 6.05 | 4.93 | 5.92 | −0.92 |
| International | 4.89 | 6.57 | 5.25 | 5.60 | +0.71 |
| Environment and animals | 4.62 | 4.81 | 4.96 | 5.95 | +1.33 |
| Public-society benefit | 14.34 | 11.46 | 13.99 | 13.12 | −1.22 |
| of which NTEE T (t_c) | 7.00 | 5.65 | 4.93 | 5.97 | −1.03 |
| Foreign (Schedule F) | 1.56 | 2.58 | 2.27 | 2.43 | +0.87 |
| Unclassified | 5.48 | 5.78 | 4.39 | 4.59 | −0.89 |

**t_b, all ex u/h** (DAF-to-DAF kept): education 19.94 → 19.43, religion 10.62 → 12.67, human services 14.94 → 13.04, public-society benefit 26.78 → 24.99 → 21.79 → 25.29. DAF-weighted DAF-to-DAF dollars were $7.03bn, $8.21bn, $5.14bn and $9.36bn. The FY2022 figure includes Jasper Ridge Charitable Fund's $1.30bn to Schwab and Fidelity Charitable [F].

### 3.2 Robustness: FY2021→FY2024 change in pts, all ex university/hospital, t_a [F]

| Sector | Changing | Fixed panel | Changing ex CZ | Changing ex SVCF | Fixed ex SVCF | Sched I layer only | Filed (unweighted) basis |
|---|---|---|---|---|---|---|---|
| Education | −0.89 | −0.93 | −0.89 | −0.89 | −0.92 | −0.63 | −0.57 |
| Religion | +2.50 | +2.42 | +2.50 | +2.25 | +2.16 | +2.67 | +2.19 |
| Human services | −2.42 | −2.46 | −2.42 | −2.53 | −2.57 | −2.49 | −2.35 |
| Health | +0.88 | +0.86 | +0.88 | +1.21 | +1.19 | +1.00 | +0.76 |
| Arts and culture | −0.70 | −0.68 | −0.70 | −0.86 | −0.84 | −0.71 | −0.49 |
| International | +0.55 | +0.58 | +0.55 | +0.71 | +0.74 | +0.66 | +0.56 |
| Environment and animals | +1.23 | +1.23 | +1.23 | +1.54 | +1.56 | +1.28 | +1.14 |
| Public-society benefit | −1.13 | −1.04 | −1.13 | −1.44 | −1.36 | −1.01 | −0.63 |
| Foreign (Schedule F) | +0.77 | +0.79 | +0.77 | +0.92 | +0.94 | n/a | +0.53 |
| Unclassified | −0.79 | −0.79 | −0.79 | −0.94 | −0.94 | −0.77 | −1.13 |

- **Robust across all seven columns** (same sign, similar size): religion up, human services down, environment up, education down, arts down, public-society benefit down, health up (endpoints only).
- **Fixed against changing panel.** No change differs by more than 0.09 pts (all sponsors) or 0.13 pts (top 50). Entering and leaving itemisers are too small to move shares: changing-only sponsors carried $0.13bn to $1.43bn of DAF-weighted L1+L3 a year, and the $1.43bn in FY2022 is mostly Jasper Ridge's DAF-to-DAF grants, excluded under t_a.
- **Excluding SVCF** strengthens health, environment and public-society benefit trends by 0.3 pts and weakens religion by 0.25.

### 3.3 Which recipients drive the shifts (FY2021→FY2024, all ex u/h, full layer) [F]
Itemised-share change by sector, against the summed contributions of its largest movers (CSV `row_type = recipient_contribution`):

| Sector | Itemised change | Top-1 | Top-5 | Top-10 | Largest single mover (DAF-weighted $m, FY2021 → FY2024) |
|---|---|---|---|---|---|
| Education | −1.24 | +1.44 | +1.49 | +1.13 | Johns Hopkins University 192 → 1,044 |
| Religion | +2.12 | +0.17 | +0.35 | +0.29 | Come and See Foundation 0 → 91 |
| Human services | −2.77 | +0.26 | +0.34 | +0.09 | Come Near Media 0 → 141 |
| Health | +0.72 | +0.41 | −0.17 | −0.35 | Memorial Sloan-Kettering 19 → 245 |
| Environment and animals | +1.05 | +0.35 | +0.10 | +0.21 | Climate Imperative Foundation 19 → 214 |
| Public-society benefit | −1.32 | +0.22 | +0.58 | +0.22 | US Energy Foundation 10 → 135 |
| Arts and culture | −0.84 | −0.26 | −0.59 | −0.51 | Museum of Science and Industry 101 → 1 |

- **Religion and human services** move across tens of thousands of recipients; their ten largest movers explain under 0.3 pts. These are **broad shifts**, not single-grant effects [F].
- **Education's −0.9 pts** headline hides a larger fall: Johns Hopkins alone adds +1.44 pts, so the rest of education lost about 2.7 pts of itemised share [F/I]. The Johns Hopkins dollars sit on a few very large lines at four June-year-end nationals (DAF-weighted): FY2023 Fidelity $827.3m, Schwab Charitable $481.8m, JCF $140.7m, NPT $68.8m; FY2024 Schwab $517.2m, Fidelity $272.4m, NPT $188.2m, JCF $28.0m (FY2021: Schwab $116.5m, JCF $32.3m). [V wave 51A]
- **Arts** loss is partly concentrated: the top five movers explain 0.59 of 0.84 pts (Museum of Science and Industry, Lucas Museum, Crystal Bridges) [F].

### 3.4 Year-on-year breaks and the single grants behind them [F]
- **FY2022→FY2023, health +2.36 pts itemised** (all ex u/h): the four CZ LLCs explain +2.88 (CZ Institute for Advanced Biological Imaging +1.20, CZ Biohub SF +1.18, CZ Biohub New York +0.51, CZ Biohub Chicago). All reverse in FY2023→FY2024 (health −2.70; top 5 −3.00).
- **Public-society benefit FY2022→FY2023, +2.29 pts**: Further Future Foundation ($1.26bn DAF-weighted, from SVCF's $1.309bn line) contributes +2.68. In FY2023→FY2024 it contributes −2.68.
- **Education FY2022→FY2023, +1.54 pts**: Johns Hopkins (DAF-weighted $272m → $1,557m) +2.69. In FY2023→FY2024 its contribution is −1.37.
- **Arts FY2022→FY2023, −0.72 pts**: Lucas Museum of Narrative Art ($250m → $35m) −0.49.

## 4. Structural breaks

### 4.1 The CZ grants (FY2023, SVCF)
SVCF's FY2023 return itemises four Chan Zuckerberg LLC recipients: CZ Institute for Advanced Biological Imaging LLC $586,007,469; CZ Biohub SF LLC $576,046,150; CZ Biohub New York LLC $248,000,000; CZ Biohub Chicago LLC $246,500,000. They total **$1,656,553,619 filed**, of which $1,070,546,150 is to the three Biohub LLCs [F].
- **DAF-weighted** (SVCF w2) they are **$1,594,822,149**, the brief's "about $1.59bn" [F].
- **Classification.** None is in the BMF; all are classed health by the name rule (`BIOHUB`, `BIOLOGICAL`).
- **Earlier years.** SVCF granted Chan Zuckerberg Biohub Inc (a BMF-listed 501(c)(3), NTEE health) $1.2m in FY2021 and $4.5m in FY2022; nothing to CZ entities is itemised in FY2024.
- **Effect.** Health in FY2023 is 10.57% with them and 7.42% without (all ex u/h; top 50: 11.48% and 7.42%). Excluding them changes no FY2021–24 endpoint change (§3.2), but it turns health's path from 7.1 / 8.4 / 10.6 / 8.0 into a flat 7.1 / 8.4 / 7.4 / 8.0.
- **Caveat.** A filed SVCF line of $1,591,322,838 to National Philanthropic Trust in FY2024 is a different item: a DAF-to-DAF grant, excluded under t_a, which appears only in t_b.

### 4.2 SVCF more broadly
- **Further Future Foundation.** SVCF's FY2023 $1.309bn line to it is classed public-society benefit.
- **Unitemised FY2022 line 1.** SVCF's FY2022 Part IX line 1 ($3.63bn) exceeds its Schedule I ($2.06bn) by $1.57bn. It itemises 57%, so the b40n120201-01 rule treats it as a full itemiser and spreads the gap by the small-gift (`small10`) key. The top-50 sub-$5,000 component is therefore $2.31bn in FY2022, against $0.67–1.25bn in other years. The raw return (object 202333189349318948) confirms line 1 of $3,626,886,828 against 3,580 Schedule I lines totalling $2,055,660,472, the largest $108.2m. A $1.57bn residual cannot be grants of $5,000 or less, so spreading it by the small-gift key is an artefact. It adds about $1.48bn DAF-weighted to the all-sponsor FY2022 allocation (full-itemiser sub-$5,000 component $2.55bn with SVCF, $1.07bn without), 3.3% of the $44.27bn base. The FY2021 and FY2024 endpoints are untouched. [V wave 51A]
- **Use the variants.** The `sched_i` layer and the `ex_svcf` variant avoid this; FY2022 full-layer shares should be read with them (P-B5101-02).

### 4.3 Sponsors entering or leaving itemisation [F]
- **Top 50 (FY2024 ranking).**
  - Six do not itemise in FY2021–22 (Bank of America CGF, Renaissance CF, Greater Horizons, Greater Kansas City CF, NY Community Trust, US Charitable Gift Trust).
  - Four start itemising in FY2023 (NY Community Trust, US Charitable Gift Trust) or FY2024 (Greater Horizons, Greater Kansas City CF).
  - Bank of America CGF and Renaissance never itemise in FY2021–24.
  - The 4 entrants carry $0.21bn (FY2023) and $0.90bn (FY2024) of DAF-weighted L1+L3.
- **All ex u/h.** 31–41 sponsors enter and 20–40 leave the itemising set each year. Fixed-panel sponsors hold 97–99.7% of DAF-weighted L1+L3 in every year.
- **Effect.** It is negligible (§3.2), because the non-itemisers are mostly outside both panels in every year. Their recipients are unobserved in all years, so the trend describes itemising sponsors only.

## 5. Limits
- **Start year.** FY2021 is the first year, and human services may be at a pandemic-era high in it (P-B5101-01). Fidelity Charitable’s 2022 Giving Report supports this: “In 2020, urgent needs related to the COVID-19 pandemic created a surge of granting activity to the human services sector” and in 2021 grant volumes “remained elevated from pre-pandemic norms”. Its human-services share of grant dollars is 14% (2021), 16% (2022), 14% (2023), 13% (2024) and 12.2% (2025). FY2021 here includes July 2020–June 2021 at June-year-end nationals, so read −2.42 as an upper bound on the structural decline. [V wave 51A] "Since FY2021" is not "long-run".
- **One 2026 BMF snapshot** for all years.
  - Recipients that lost status before November 2026 fall to the name rule or unclassified; EIN-not-in-BMF dollars are 2.2% in FY2021 against 1.9% in FY2024.
  - Part of unclassified's −0.8 pts is this drift. NTEE codes can also be re-assigned, so a recipient's sector is its 2026 code in every year.
- **The DAF weight is a sponsor-level ratio.** It assumes a sponsor's DAF grants have the same sector mix as all its grants (as in b39n4-01). It matters most for community foundations.
- **The sub-$5,000 allocation is an assumption** (wave-41B envelope); the `sched_i` layer is the low-end bound and gives the same signs.
- **Fiscal years are not aligned.** FY = year of tax-period end, so FY2021 includes returns for July 2020 – June 2021 at June-year-end sponsors (Fidelity, Vanguard).
- **Fixed top-50 list.** Top 50 is the FY2024 ranking, applied to all years.
- **Classification limits.** t_a/t_c is the validated convention for where DAF money ends up [I]; t_b double counts. CZ and other LLCs not in the BMF depend on the name rule.
- **Recipient contributions** are on itemised dollars; the sub-$5,000 part of each sector change is not attributed to recipients.

## 6. Source register
| Source | URL | Use | robots / access |
|---|---|---|---|
| IRS Form 990 e-file XML (GivingTuesday mirror of IRS TEOS) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml (e.g. SVCF FY2023: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413129349304911_public.xml) | FY2021–22 Schedule I lines and Part IX lines 1–3, fetched for this study; FY2023–24 from committed caches | robots.txt checked 2026-11-20 with UA `research-script/1.0`: HTTP 404 (no robots file; S3 NoSuchKey), logged in the study cache; treated as no restriction, as in b40n1202-01 and b40n120201-01. No ClaudeBot / anthropic-ai group exists |
| IRS EO Business Master File | https://www.irs.gov/pub/irs-soi/eo1.csv … eo4.csv, eo_pr.csv, eo_xx.csv (Last-Modified 2026-11-09) | NTEE codes (existing extract `rcp/bmf`) | not re-fetched |
| IRS e-file index | https://apps.irs.gov/pub/epostcard/990/xml/2021/index_2021.csv (and other years) | Object IDs (via existing netpayout990 cache) | not re-fetched |
| DAF Research Collaborative 2025 dataset | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Panel, DAF grants (via `dafrc-sponsor-schedule-d-fy2019-2024.csv`, with `dafrc-corrections-itemized.csv`) | not re-fetched |
| b39n4-01 / wave 43A | repo files linked above | Pipeline, conventions, FY2023–24 reproduction | — |

Not used: sec.gov, crt.sh and certspotter. No other host was contacted.

## 7. Data dictionary: `sector-mix-trend-2026-11-20.csv`
| Column | Meaning |
|---|---|
| `row_type` | `share` (a sector's share in one FY); `change` (between two FYs); `recipient_contribution` (largest movers); `panel` (itemisation status and entry/exit) |
| `scope` | `top50_ex_university_hospital` or `all_ex_university_hospital` |
| `panel` | `changing` (all itemisers that FY) or `fixed` (sponsors itemising all four FYs) |
| `variant` | `base`, `ex_cz` (CZ LLC lines removed, and from line 1), `ex_svcf` (SVCF dropped) |
| `basis` | `daf_weighted` (× w2) or `schedule_i` (filed dollars) |
| `fiscal_year` | `2021`…`2024` for share and panel rows; `YYYY-YYYY` (from–to) for change and contribution rows: 2021-2024, 2021-2022, 2022-2023, 2023-2024 |
| `treatment` | `t_a_base`, `t_b_d2d_included`, `t_c_t_separate` (b39n4-01 §1.6) |
| `layer` | `sched_i`, `plus_foreign`, `plus_foreign_sub5k` |
| `sector` | NTEE major group (`education`, `religion`, `human_services`, `health`, `arts_culture`, `international`, `environment_animals`, `public_societal_benefit`, `philanthropy_t` (t_c only), `mutual_membership`, `unknown_z`, `unclassified`, `foreign_schedule_f`) or `ALL`. For panel rows: `status:<pre-status>`, `fixed_panel_sponsors`, `changing_only_sponsors`, `entered_vs_prior_fy`, `left_vs_prior_fy` |
| `amount_usd` | Share and ALL rows: sector dollars (USD, rounded). Change rows: difference in dollars. Contribution rows: the recipient's DAF-weighted itemised dollars in the end year. Panel rows: DAF-weighted Part IX L1+L3, gross of DAF-to-DAF |
| `share` | Share of the layer total (0–1); in change rows the end-year share |
| `share_from` | Change rows: start-year share |
| `change_pp` | Change rows: (end − start) × 100. Contribution rows: the recipient's (or, at rank 0, the sector's itemised) share change in pts |
| `lines` | Schedule I line count in the sector (ALL row: total) |
| `sponsor_years`, `sponsors` | Counts in the cell (ALL and panel rows) |
| `sched_i_total_usd`, `d2d_usd`, `ntee_t_non_d2d_usd`, `part_ix_l1_usd`, `foreign_l3_usd`, `sub5k_full_usd`, `sub5k_partial_usd` | ALL rows: the components on the row's basis (as b39n4-01) |
| `rank` | Contribution rows: 0 = sector summary, 1–5 = largest movers by absolute contribution |
| `recipient_name`, `recipient_ein` | Contribution rows: as filed (EIN blank for blank-EIN lines) |
| `amount_from_usd` | Contribution rows: start-year DAF-weighted dollars |
| `recipients`, `top1_pp`, `top5_pp`, `top10_pp` | Rank-0 rows: recipients in the sector and the summed contribution of the largest 1 / 5 / 10 movers |
| `source` | Provenance (share rows) |

**Reproduce:** `python3 scripts/mission_sector_mix_trend.py . --np-cache NPCACHE --lines-cache-top50 RCP_LINES --lines-cache Q120201_LINES --bmf-dir BMF --new-cache NEW [--fetch]`. Cache-only, it takes about 52 s.
