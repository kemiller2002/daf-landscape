# P-B42N21-02: community-foundation local share for the 100 largest CFs, and its relation to the DAF share of grants (FY2023–FY2024)

**Date:** 2026-11-19 · **Queue item:** P-B42N21-02 (proposed in [direction-grant-geography.md](direction-grant-geography.md) §3, "smaller CFs may be more local")

**Outputs**
- [`data/mission-2026-11-14/cf-local-share-top100-2026-11-19.csv`](../../data/mission-2026-11-14/cf-local-share-top100-2026-11-19.csv): 96 rows, one per top-100 CF with an itemised FY2023–24 Schedule I. Own-state, own-metro and own-county shares, DAF share of grants, purpose-text flags, return object IDs. This is the scatter data for §3.
- [`scripts/mission_cf_local_share_top100.py`](../../scripts/mission_cf_local_share_top100.py): stdlib, functional style. It reuses the geocoding and DAF-to-DAF functions of `mission_grant_geography.py` and `mission_recipient_sectors.py` unchanged.
- [`data/mission-2026-11-14/queue-proposals-b42n21-02.csv`](../../data/mission-2026-11-14/queue-proposals-b42n21-02.csv): 5 proposals.

Evidence tags: [F] filed figure, [C] computed here, [I] inference.

## 0. Headline answers

| Question | Answer |
|---|---|
| **Coverage** | 96 of the 100 largest CFs (by FY2024 DAF assets) have an itemised FY2023–24 Schedule I in XML: 190 returns, 173,088 lines after removing DAF-to-DAF lines, $22.07bn of US-located grant dollars. The other 4 CFs (Hawaii, Sacramento Region, Monterey County, SW Washington) file Schedule I as an attachment only [C]. |
| **Reproduces P-NEW-GEO-01** | For the 22 CFs in the earlier study, own-state shares match exactly (maximum absolute difference 0.0000). Own-metro shares differ by at most 0.0001 (CF of Tampa Bay, rounding) [C]. |
| **Local share, 96 CFs** | **Median own-state share 83.1%** (mean 78.3%, range 20.0% Chicago Community Trust to 98.8% Omaha CF). **Median own-metro share 69.4%** (n = 94). **Median own-county share 54.5%** (n = 94). Dollar-pooled own-state share 65.3%; SVCF and Chicago pull the pooled figure down [C]. |
| **Smaller CFs are more local** | The 74 CFs not in the earlier study have a median own-state share of 85.7%, against 71.2% for the earlier 22. CFs ranked 51–100 have a median of 86.0%, against 76.8% for ranks 1–50. Only 4 of the 96 CFs keep less than half their dollars in-state (Chicago, Greater Kansas City, CF of New Jersey, Greater Cincinnati); 55 keep 80% or more [C]. |
| **Does local share fall as the DAF share rises?** | **Yes, in the cross-section.** Pearson r = **−0.45** (95% CI −0.59 to −0.27, n = 95); Spearman ρ = −0.43 (bootstrap CI −0.60 to −0.23). OLS with log DAF assets and log Schedule I dollars as size controls: **−0.25 own-state share per unit DAF share** (HC1 95% CI −0.39 to −0.10). So 10 points more DAF share goes with about 2.5 points less in-state share. The size controls themselves are not significant [C]. |
| **Robustness** | The slope stays negative without SVCF (−0.25, CI −0.40 to −0.10). It also holds for the 74 newly added CFs alone (−0.23, CI −0.38 to −0.09), and without the 21 CFs whose home metro crosses a state line (−0.18, CI −0.31 to −0.04). For own-metro share the slope is −0.21 (CI −0.39 to −0.02). For own-county share it is −0.23, but the CI (−0.46 to +0.003) includes zero [C]. |
| **DAF vs discretionary split** | **Not possible for 93 of 96 CFs.** Purpose text marks DAF grants on only $118m of $22.07bn (0.5%), and discretionary grants on $7m. Three CFs label DAF grants line by line, and the within-CF comparison splits 2 to 1. DAF-flagged lines are less in-state at Birmingham (68.3% vs 98.8%) and Lancaster County (95.8% vs 98.1%), but more in-state at Minneapolis (78.0% vs 72.2%). So the cross-CF result uses the Schedule D DAF share of grants as a covariate, as the brief allowed [C]. |
| **Reading** | The relationship is an association across CFs, not a measured effect of DAF grants themselves. CFs whose grants are mostly DAF grants (Chicago 94%, CF of New Jersey 100%, SVCF 95%) also have national or metropolitan-commuter donor bases [I]. |

## 1. Question and definitions

The question is whether the earlier finding (22 top-50 CFs: median 71% in-state) holds for the 100 largest CFs, and whether CFs with more DAF-heavy grantmaking keep less money local.

**Definitions are those of P-NEW-GEO-01 ([direction-grant-geography.md](direction-grant-geography.md) §1, items 1–8), unchanged:**
- **Own-state share** = net Schedule I Part II dollars to recipients in the CF's state ÷ net dollars to US-located recipients.
- **Own-metro share** = dollars to the CF's home CBSA ÷ CBSA-resolved dollars.
- "Net" means DAF-to-DAF lines are excluded: lines to `include` EINs of `daf-to-daf-recipient-whitelist.csv`, self-lines, and blank-EIN lines matching one whitelisted sponsor name.
- The CF's home is its EO BMF `STATE`/`ZIP`. All 96 were found in the BMF.

**Added here:**
- **Own-county share** = dollars to the CF's home county (ZIP → ZCTA → county) ÷ dollars on ZCTA-resolved lines. This is the "same-county" fallback the brief asked for. It is reported alongside the metro share, since metro mapping was feasible.
- **DAF share of grants** = Schedule D Part I DAF grants ÷ Part IX lines 1–3 grants, summed over the CF's itemised FYs and capped at 1. Both come from `sponsor-cost-structure.csv` for the same returns.

## 2. Method

1. **Universe.** Ranks 1–100 of [`cf-daf-fee-census-2026.csv`](../../data/mission-2026-11-14/cf-daf-fee-census-2026.csv), the repo's top-100 CF list by DAFRC FY2024 DAF assets; its 5 national comparator rows are dropped. Every EIN is in the DAFRC panel. 22 of the 100 are among the top-50 sponsors of P-NEW-GEO-01.
2. **Returns.** One return per EIN × FY via `mission_daf_to_daf.pick_returns` over the `netpayout990/` cache, for FY2023 and FY2024 (tax periods ending in 2023–2024, i.e. tax years 2022–2024).
   - 199 of 200 CF-years exist; Central New York CF FY2024 is missing from the cache.
   - 9 returns are non-itemising (`mission_net_payout.itemized`). These are both years of Hawaii CF, Sacramento Region CF, CF for Monterey County and CF for SW Washington, plus Greater Kansas City CF FY2023 (as in P-NEW-GEO-01).
   - That leaves 190 returns for 96 CFs.
3. **Lines.** Each return's Schedule I `RecipientTable` was re-read in full: EIN, name, state, ZIP, city, cash, non-cash and purpose.
   - 30 returns came from local XML copies in scratch; 160 were streamed from the GivingTuesday mirror of IRS TEOS (`https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`) with User-Agent `research-script/1.0`.
   - A return was accepted only when the line count equalled the cache's `sched_i_lines` and the dollar total was within 0.5% of `sched_i_total`. **All 190 passed.**
4. **DAF-to-DAF exclusion:** `mission_recipient_sectors.annotate`, unchanged. $2.88bn of lines were removed (the largest is SVCF's).
5. **Geocoding:** `mission_grant_geography.geo_line` with the same Census files.
   - The files are the 2020 ZCTA520–county relationship (largest land overlap) and cbsa-est2024-alldata (July 2023 delineations).
   - The same ZIP3 fallback for non-ZCTA ZIPs and the same Connecticut table are used.
   - 97.7% of US dollars resolve to a CBSA ($21.56bn of $22.07bn).
   - Two CFs have a home ZIP outside any CBSA (Maine CF, Ellsworth; Vermont CF, Middlebury), so they have no own-metro share.
6. **Purpose-text split.** Each line's purpose text was matched against a DAF regex (`DONOR[- ]?ADVISED|\bDAF\b|ADVISED FUND|DONOR[- ]ADVISOR|ADVISED GRANT`) and a discretionary regex (`DISCRETIONARY|COMPETITIVE|RESPONSIVE GRANT|COMMUNITY GRANT|BOARD[- ]DESIGNATED|FIELD[- ]OF[- ]INTEREST|UNRESTRICTED FUND|IMPACT GRANT|STRATEGIC INITIATIVE`).
   - A within-CF split (DAF-flagged lines vs all other lines) is reported only where DAF-flagged lines hold 10–90% of a CF's US dollars.
   - This follows [b40n13-01-grant-purpose-panel.md](b40n13-01-grant-purpose-panel.md) §4 "Cannot" 3 with its wave-35A corrections: Schedule I covers all of a filer's grants, and purpose text is a reporting regime, not a record of fund type.
7. **Covariate checks.** Two CFs have Schedule D DAF grants above Part IX grants (CF of New Jersey, GiveWell CF), so their share is capped at 1 and flagged `capped_at_1`. The CF for Southeast Michigan files negative Schedule D DAF grants in every FY (−$64.3m FY2023, −$129.3m FY2024, per `sponsor-cost-structure.csv`). Its covariate is left blank (`negative_sched_d_daf_grants`), so regressions use 95 CFs.
8. **Statistics** (all in the script):
   - Pearson r with a Fisher-z 95% CI and a percentile bootstrap CI (2,000 resamples, seed 2026111902); Spearman ρ with a bootstrap CI.
   - OLS of each share on DAF share, bivariate and with log10 FY2024 DAF assets and log10 US Schedule I dollars as size controls. Classical and HC1 standard errors; normal 95% intervals on HC1.
   - Subsets: all; ex SVCF; the 74 CFs not in P-NEW-GEO-01; and ex the 21 CFs whose home CBSA spans more than one state, where the own-state share is mechanically low (Kansas City MO-KS, New York NY-NJ, Philadelphia PA-NJ-DE-MD and others).

## 3. Results

### 3.1 Local share across the 100 largest CFs [C]

| Group | CFs | Median own state | Pooled own state | Median own metro | Median own county | Median DAF share of grants |
|---|---|---|---|---|---|---|
| All with itemised Schedule I | 96 | **83.1%** | 65.3% | **69.4%** | 54.5% | 65.5% |
| … the 22 of P-NEW-GEO-01 | 22 | 71.2% | 60.0% | 63.3% | 46.3% | 74.0% |
| … the 74 added here | 74 | **85.7%** | 78.1% | 71.1% | 58.1% | 62.3% |
| Ranks 1–50 | 49 | 76.8% | 63.0% | 69.1% | 52.0% | 74.0% |
| Ranks 51–100 | 47 | 86.0% | 82.0% | 70.6% | 61.3% | 59.5% |
| Ex multi-state home CBSA | 75 | 85.1% | 74.4% | 70.2% | 58.0% | 63.9% |

- The median CF reaches 37.5 states and territories, and sends a median 5.6% of its US dollars to DC/NY/MA/CA outside its home state.
- **Lowest own-state shares:** Chicago Community Trust 20.0% (DAF share 94%), Greater Kansas City CF 35.9% (83%; largest other state KS), CF of New Jersey 38.6% (100%; NY), Greater Cincinnati Foundation 42.5% (86%), Delaware CF 53.2%, Foundation For The Carolinas 53.8%.
  - Kansas City, New Jersey, Cincinnati and Delaware sit in metros that cross state lines.
- **Highest:** Omaha CF 98.8%, Idaho CF 98.0%, Lancaster County CF 97.3% (DAF share 19%), Greater Kanawha Valley 97.0%, Central New York CF 95.4%, Grand Rapids CF 94.6%.
- **Own-metro outliers:**
  - SVCF 4.4%: its largest lines go to San Mateo County, which is in the SF–Oakland CBSA.
  - South Dakota CF 5.9%: it is headquartered in Pierre (Pierre micropolitan area) but grants statewide.

### 3.2 Local share vs DAF share of grants [C]

**Tertiles of DAF share (95 CFs):**

| Tertile | DAF share range | CFs | Median own state | Median own metro | Median DAF assets |
|---|---|---|---|---|---|
| T1 (low) | 18.8–56.5% | 31 | 86.0% | 76.0% | $174m |
| T2 | 56.6–76.9% | 32 | 82.0% | 62.7% | $257m |
| T3 (high) | 77.4–100% | 32 | 74.6% | 64.2% | $470m |

**Correlation and regression (own-state share):**

| Sample | n | Pearson r (Fisher 95% CI) | Spearman ρ (bootstrap 95% CI) | OLS slope, bivariate (HC1 CI) | OLS slope with size controls (HC1 CI) | R² (controls) |
|---|---|---|---|---|---|---|
| All | 95 | **−0.447** (−0.595, −0.269) | −0.432 (−0.605, −0.231) | −0.344 (−0.504, −0.183) | **−0.249 (−0.394, −0.103)** | 0.35 |
| Ex SVCF | 94 | −0.443 (−0.593, −0.264) | −0.424 (−0.599, −0.218) | −0.344 (−0.510, −0.179) | −0.251 (−0.398, −0.103) | 0.37 |
| 74 added CFs | 73 | −0.381 (−0.562, −0.166) | −0.359 (−0.574, −0.120) | −0.243 (−0.386, −0.100) | −0.235 (−0.381, −0.089) | 0.23 |
| Ex multi-state CBSA | 74 | −0.408 (−0.582, −0.198) | −0.416 (−0.603, −0.194) | −0.229 (−0.352, −0.107) | −0.177 (−0.312, −0.042) | 0.24 |

- In the full model, neither size control has a significant coefficient: log10 DAF assets −0.059 (HC1 CI −0.195 to +0.078); log10 US Schedule I dollars −0.075 (−0.172 to +0.023).
  - Size and DAF share are correlated: T3's median DAF assets are 2.7 times T1's. The two size terms together move the DAF-share slope from −0.34 to −0.25.

**Own-metro and own-county shares:**

| Sample | Own-metro: r (CI) | Own-metro slope with controls (HC1 CI) | Own-county: r (CI) | Own-county slope with controls (HC1 CI) |
|---|---|---|---|---|
| All | −0.314 (−0.486, −0.117), n = 93 | −0.207 (−0.394, −0.019) | −0.285 (−0.462, −0.086), n = 93 | −0.229 (−0.461, +0.003) |
| Ex SVCF | −0.280 (−0.459, −0.080) | −0.203 (−0.389, −0.017) | −0.257 (−0.439, −0.056) | −0.226 (−0.458, +0.007) |
| 74 added CFs | −0.241 (−0.449, −0.008) | −0.212 (−0.430, +0.006) | −0.231 (−0.439, +0.001) | −0.241 (−0.503, +0.021) |

Own-metro and own-county relationships have the same sign but are weaker. With size controls, the intervals reach zero in the smaller samples.

### 3.3 Scatter data
The CSV is the scatter: x = `daf_share_of_grants`, y = `own_state_share` (or `own_cbsa_share_of_resolved`, `own_county_share_of_resolved`), with size = `fy2024_daf_assets_usd`. Rows with a blank x (SE Michigan) are excluded from §3.2.

### 3.4 Line-level DAF vs discretionary split [C]
- **12 CFs** have any DAF-flagged purpose text and **22** have any discretionary-flagged text. Flagged dollars total **$118.0m DAF** and **$7.3m discretionary**, out of $22.07bn of US dollars (0.5% and 0.03%).
- Only **three CFs** label DAF grants systematically, with 10–90% of dollars flagged:

| CF | DAF-flagged $m / US $m | Typical string | Own state: DAF-flagged vs other lines | Own metro: DAF-flagged vs other lines |
|---|---|---|---|---|
| Minneapolis Foundation | 75.5 / 170.7 | "DONOR-ADVISED, HUMAN SERVICES" | 78.0% vs 72.2% | 75.4% vs 70.8% |
| CF of Greater Birmingham | 29.7 / 72.5 | "EDUCATION; DAF FUNDED" | **68.3% vs 98.8%** | 64.1% vs 97.4% |
| Lancaster County CF | 8.5 / 26.4 | "… DONOR RECOMMENDED GRANT FROM DONOR ADVISED FUND …" | 95.8% vs 98.1% | 88.5% vs 87.1% |

- Minneapolis strings such as "HUMAN SERVICES, DONOR-ADVISED, HUMAN SERVICES" merge DAF and non-DAF grants to one recipient into a single Schedule I line. Its "other" lines are therefore not purely discretionary [I].
- At most CFs (SVCF, Greater Kansas City and others), purpose text holds only a sector label, which is why the purpose-panel study classed them `sector_taxonomy`. These CFs cannot be split.

## 4. Limits
- **Association, not effect.**
  - The covariate is a CF-level share, not a line-level split.
  - CFs with high DAF shares may have different donors (national wealth holders in Chicago, commuters in New Jersey) whose preferences drive both the DAF share and the geography [I].
  - The within-CF evidence (§3.4) is three CFs and is mixed.
- **Recipient address, not place of benefit.** The Schedule I address is the recipient's legal or remittance address. National charities and intermediaries in DC/NY/MA/CA receive "out-of-state" dollars that may be spent locally, e.g. through a local chapter (P-NEW-GEO-01 §3).
- **Multi-state metros** mechanically lower own-state shares. The ex-multi-state sensitivity shows the slope survives, at −0.18.
- **Itemisation.** Schedule I lists only recipients receiving more than $5,000. Small local grants are under-counted, which probably understates local shares [I].
  - Foreign grants (Schedule F) are excluded.
  - Four top-100 CFs file Schedule I as attachments and are missing.
  - Greater Kansas City CF has FY2024 only; Central New York CF has FY2023 only.
- **Covariate quality.**
  - The DAF share mixes Schedule D (DAF grants) with Part IX lines 1–3 (all grants, including to individuals and foreign recipients).
  - It exceeds 1 for two CFs (capped).
  - SE Michigan's negative Schedule D figures look like a sign error and are left blank (see P-B4221-02-03).
- **Size ranking.** The universe is ranked by DAF assets, not total assets. A CF with a large endowment but a small DAF book can be missing from the "100 largest".
- **Statistics.**
  - The intervals are normal approximations; t-intervals at n = 95 differ in the third decimal.
  - The bootstrap uses a fixed seed.
  - The CFs are not a random sample, so the intervals describe sampling-like noise around this population, not inference to all CFs.
- **Purpose regexes** are hand-built; a missed DAF phrasing would under-count flagged lines. The conclusion that the split is infeasible for 93 of 96 CFs does not depend on fine regex choices: most CFs use sector labels only.

## 5. Data dictionary: `cf-local-share-top100-2026-11-19.csv`

| Column | Meaning |
|---|---|
| cf_rank_fy2024 | Rank in `cf-daf-fee-census-2026.csv` (DAFRC FY2024 DAF assets) |
| sponsor_ein, sponsor_name | CF identity (census list) |
| fy2024_daf_assets_usd | FY2024 DAF assets as in the census list |
| in_top50_geo_study | 1 if the CF is one of the 22 in `daf-grant-geography-cf-local-share.csv` |
| sponsor_state, sponsor_home_source | Home state; `bmf` (EO BMF STATE/ZIP) for all rows |
| sponsor_county_fips, sponsor_cbsa, sponsor_cbsa_name | Home county (via ZCTA) and 2023 CBSA (blank where the home ZIP is outside any CBSA) |
| fiscal_years | Itemised FYs used |
| return_status | `FY:status:object_id` for each return; the XML is at the mirror URL in §6 |
| lines_net | Schedule I lines after DAF-to-DAF exclusion |
| net_usd, d2d_excluded_usd, us_located_usd | Net dollars (cash + non-cash); DAF-to-DAF dollars removed; net dollars to US-located recipients |
| own_state_usd, own_state_share | Dollars to recipients in the home state; share of US-located dollars |
| own_state_share_fy2023, own_state_share_fy2024 | The same by FY (blank when that FY is not itemised) |
| cbsa_resolved_usd, own_cbsa_usd, own_cbsa_share_of_resolved | CBSA-resolved US dollars; dollars to the home CBSA; share |
| county_resolved_usd, own_county_usd, own_county_share_of_resolved | ZCTA-resolved US dollars; dollars to the home county; share |
| states_reached | Distinct state/territory codes receiving dollars |
| top_other_state | Largest recipient state other than the home state |
| dc_ny_ma_ca_out_of_state_share | Share of US dollars to DC, NY, MA or CA, excluding the home state |
| daf_grants_sched_d_usd, total_grants_part_ix_usd | Schedule D Part I DAF grants and Part IX lines 1–3 grants, summed over the itemised FYs (`sponsor-cost-structure.csv`) |
| daf_share_of_grants | Ratio of the two, capped at 1; blank if Schedule D is negative or missing |
| daf_share_flag | `capped_at_1`, `negative_sched_d_daf_grants`, `missing` or blank |
| purpose_daf_flag_usd, purpose_disc_flag_usd, purpose_flag_coverage | US dollars on lines whose purpose text matches the DAF / discretionary regex; their combined share of US dollars |
| own_state_share_daf_flagged, own_state_share_not_daf_flagged | Within-CF split, only where DAF-flagged lines hold 10–90% of US dollars |
| own_cbsa_share_daf_flagged, own_cbsa_share_not_daf_flagged | The same for the home CBSA |
| source | Provenance string |

## 6. Source register

| # | Source | URL | Version / access | robots.txt |
|---|---|---|---|---|
| S1 | IRS Form 990 Schedule I Part II e-file XML, 190 returns (GivingTuesday mirror of IRS TEOS) | `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`; one object ID per return in CSV `return_status`, e.g. [SVCF FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349305759_public.xml) | 160 streamed 2026-11-19; 30 local copies from earlier batches | 404 at 2026-11-19T20:06:38Z (no rules) |
| S2 | IRS EO BMF eo1–eo4, eo_pr, eo_xx | https://www.irs.gov/pub/irs-soi/eo1.csv (and siblings) | Last-Modified 2026-11-09; scratch copy from P-NEW-RCP-01 | not re-fetched (www.irs.gov `/pub/` not disallowed, per P-NEW-GEO-01) |
| S3 | Census 2020 ZCTA520–county relationship file | https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt | Last-Modified 2021-12-09, 6,821,287 bytes (scratch copy from P-NEW-GEO-01) | www2.census.gov robots.txt 200 at 2026-11-19T20:06:40Z, no `User-agent: *` group |
| S4 | Census cbsa-est2024-alldata (county rows give 2023 CBSA delineations) | https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/metro/totals/cbsa-est2024-alldata.csv | Last-Modified 2025-03-13, 718,043 bytes | same |
| S5 | Repo: `cf-daf-fee-census-2026.csv` (top-100 CF list), `dafrc-sponsor-schedule-d-fy2019-2024.csv` (DAFRC panel; [DAFRC 2025 dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)), `sponsor-cost-structure.csv`, `daf-to-daf-recipient-whitelist.csv`, `daf-grant-geography-cf-local-share.csv`, `netpayout990/` cache | repo | n/a | n/a |

Robots log: `$SCRATCH/q2102/robots/log.tsv`. No outreach, logins or forms.

## 7. Reproduce
```
python3 scripts/mission_cf_local_share_top100.py . --np-cache $SCRATCH/npcache --bmf-dir $SCRATCH/rcp/bmf \
  --census-dir $SCRATCH/n21/census --line-cache $SCRATCH/q2102/lines --xml-list $SCRATCH/q2102/allxml_found.txt \
  [--fetch] --summary $SCRATCH/q2102/summary.json
```
- The script writes the CSV and prints a JSON summary; every figure above comes from that summary or from the CSV.
- With cached lines the run takes about 12 s. The first run with `--fetch` streamed 160 XMLs.

## Appendix: all 96 CFs [C]

| Rank | CF | State | US $m | Own state % | Own metro % | Own county % | DAF share of grants % | In GEO-01 |
|---|---|---|---|---|---|---|---|---|
| 1 | Silicon Valley Community Foundation | CA | 5,970 | 69.3 | 4.4 | 4.0 | 94.6 | yes |
| 2 | The Chicago Community Trust | IL | 2,832 | 20.0 | 20.3 | 18.4 | 94.3 | yes |
| 3 | Foundation For The Carolinas | NC | 1,111 | 53.8 | 33.9 | 19.1 | 87.7 | yes |
| 4 | Greater Kansas City Community Foundation | MO | 342 | 35.9 | 47.6 | 28.5 | 83.0 | yes |
| 5 | Columbus Foundation | OH | 500 | 74.3 | 70.0 | 69.1 | 72.4 | yes |
| 6 | The New York Community Trust | NY | 376 | 65.5 | 64.8 | 46.3 | 34.7 | yes |
| 7 | The Oregon Community Foundation | OR | 355 | 90.1 | 53.9 | 43.0 | 41.4 | yes |
| 8 | Boston Foundation Inc | MA | 325 | 72.2 | 69.6 | 49.8 | 78.8 | yes |
| 9 | California Community Foundation | CA | 572 | 74.2 | 58.7 | 58.5 | 79.2 | yes |
| 10 | The Community Foundation For Greater | GA | 292 | 70.2 | 68.1 | 40.2 | 74.5 | yes |
| 11 | Greater Houston Community Foundation | TX | 382 | 62.7 | 44.9 | 41.1 | 88.4 | yes |
| 12 | Marin Community Foundation | CA | 277 | 61.3 | 46.5 | 15.5 | 73.4 | yes |
| 13 | Community Foundation Of New Jersey | NJ | 151 | 38.6 | 47.8 | — | 100.0 (capped) | yes |
| 14 | The Denver Foundation | CO | 230 | 80.2 | 71.0 | 53.7 | 69.2 | yes |
| 15 | The San Diego Foundation | CA | 217 | 91.7 | 84.3 | 84.3 | 56.5 | yes |
| 16 | Community Foundation | TN | 225 | 85.0 | 85.4 | 85.3 | 89.8 | yes |
| 17 | Tulsa Community Foundation | OK | 321 | 66.7 | 64.1 | 61.1 | 51.5 | yes |
| 18 | Seattle Foundation | WA | 295 | 65.8 | 58.5 | 58.0 | 69.9 | yes |
| 19 | The Minneapolis Foundation | MN | 171 | 74.8 | 72.9 | 55.2 | 72.8 | yes |
| 20 | The San Francisco Foundation | CA | 335 | 79.0 | 62.6 | 26.8 | 65.5 | yes |
| 21 | Community Foundation Of Tampa Bay Inc | FL | 57 | 80.7 | 73.5 | 51.9 | 64.9 | yes |
| 22 | Saint Paul & Minnesota Foundation | MN | 283 | 89.3 | 83.9 | 25.9 | 80.5 | yes |
| 23 | Communities Foundation Of Texas Inc | TX | 289 | 85.2 | 77.3 | 54.3 | 45.3 |  |
| 24 | East Bay Community Foundation | CA | 227 | 78.0 | 39.5 | 28.9 | 94.9 |  |
| 25 | The Pittsburgh Foundation | PA | 115 | 87.3 | 83.1 | 73.8 | 45.1 |  |
| 26 | Omaha Community Foundation | NE | 1 | 98.8 | 90.2 | 86.1 | 88.4 |  |
| 27 | The Greater Cincinnati Foundation | OH | 315 | 42.5 | 42.4 | 39.1 | 85.9 |  |
| 28 | Givewell Community Foundation Inc | FL | 127 | 92.9 | 88.0 | 89.2 | 100.0 (capped) |  |
| 29 | The Community Foundation For | FL | 150 | 76.4 | 69.1 | 63.5 | 97.8 |  |
| 30 | New Hampshire Charitable Foundation | NH | 112 | 81.0 | 28.3 | 25.1 | 62.7 |  |
| 31 | The Cleveland Foundation | OH | 326 | 92.6 | 88.0 | 83.8 | 26.5 |  |
| 32 | The Community Foundation Of Middle | TN | 151 | 78.6 | 71.7 | 60.5 | 41.1 |  |
| 33 | Orange County Community Foundation | CA | 173 | 63.7 | 48.0 | 41.5 | 87.8 |  |
| 34 | The Community Foundation Of | KY | 159 | 56.8 | 39.9 | 38.7 | 89.5 |  |
| 35 | The Rhode Island Community Foundation | RI | 151 | 88.8 | 89.8 | 71.8 | 42.4 |  |
| 36 | Arizona Community Foundation | AZ | 131 | 67.0 | 54.9 | 52.0 | 58.0 |  |
| 37 | Community Foundation Of North Texas (Tax | TX | 71 | 87.8 | 71.5 | 62.3 | 84.4 |  |
| 38 | Greater Washington Community Foundation | DC | 165 | 56.7 | 76.3 | 58.1 | 84.1 |  |
| 39 | St Louis Community Foundation Inc | MO | 116 | 66.2 | 65.6 | 24.2 | 87.1 |  |
| 40 | The Community Foundation Inc | VA | 119 | 79.5 | 71.0 | 19.7 | 81.4 |  |
| 41 | Austin Community Foundation Inc | TX | 99 | 76.8 | 72.6 | 67.0 | 78.0 |  |
| 42 | Community Fdn Of Greater Des Moines | IA | 107 | 89.6 | 69.1 | 52.4 | 50.9 |  |
| 43 | Central Indiana Community Foundation Inc | IN | 50 | 78.3 | 73.2 | 66.8 | 67.0 |  |
| 44 | The Winston-Salem Foundation | NC | 146 | 57.0 | 32.8 | 29.5 | 83.7 |  |
| 45 | Arkansas Community Foundation Inc | AR | 86 | 87.2 | 21.4 | 16.2 | 58.8 |  |
| 46 | The Greater New Orleans Foundation | LA | 67 | 86.0 | 76.7 | 64.4 | 56.2 |  |
| 47 | Community Foundation For Southeast | MI | 184 | 85.1 | 70.2 | 48.2 | — (neg. Sch D) |  |
| 49 | Maine Community Foundation Inc | ME | 110 | 69.3 | — | 9.0 | 73.4 |  |
| 50 | Greater Milwaukee Foundation Inc | WI | 110 | 91.7 | 81.9 | 73.5 | 38.4 |  |
| 51 | Community Foundation For The Fox Valley | WI | 53 | 89.6 | 60.6 | 45.2 | 66.8 |  |
| 52 | Community Foundation Of The | GA | 42 | 69.7 | 59.7 | 63.2 | 75.7 |  |
| 54 | Oklahoma City Community Foundation Inc | OK | 107 | 88.0 | 76.0 | 66.1 | 42.1 |  |
| 55 | Community Foundation For Greater Buffalo | NY | 62 | 89.8 | 80.2 | 76.3 | 59.5 |  |
| 56 | The Dallas Foundation | TX | 148 | 69.5 | 60.6 | 56.2 | 65.9 |  |
| 57 | Hartford Foundation For Public Giving | CT | 98 | 85.7 | 80.0 | 78.2 | 42.9 |  |
| 58 | Charlottesville Area Community | VA | 50 | 61.1 | 47.2 | 41.9 | 84.4 |  |
| 59 | Triangle Community Foundation Inc | NC | 46 | 83.1 | 49.0 | 28.0 | 85.6 |  |
| 60 | North Carolina Community Foundation | NC | 51 | 89.9 | 30.4 | 15.9 | 60.4 |  |
| 61 | South Dakota Community Foundation | SD | 68 | 94.2 | 5.9 | 4.3 | 42.2 |  |
| 62 | Sioux Falls Area Community | SD | 64 | 93.0 | 84.8 | 70.8 | 63.7 |  |
| 63 | Baltimore Community Foundation Inc | MD | 53 | 83.3 | 80.0 | 61.2 | 69.8 |  |
| 64 | The Miami Foundation Inc | FL | 153 | 57.3 | 56.4 | 54.6 | 37.6 |  |
| 65 | San Antonio Area Foundation | TX | 61 | 90.5 | 80.5 | 76.8 | 44.6 |  |
| 66 | The Community Foundation Of Greater | AL | 72 | 86.3 | 84.1 | 70.7 | 86.5 |  |
| 67 | Central New York Community Foundation | NY | 19 | 95.4 | 83.8 | 77.8 | 58.4 |  |
| 68 | Rochester Area Community Foundation | NY | 47 | 75.4 | 71.1 | 63.5 | 56.4 |  |
| 69 | Hampton Roads Community Foundation | VA | 55 | 84.0 | 76.1 | 50.5 | 55.3 |  |
| 70 | Coastal Community Foundation | SC | 44 | 85.7 | 47.9 | 39.9 | 63.0 |  |
| 71 | Princeton Area Community Foundation Inc | NJ | 43 | 75.0 | 56.0 | 54.4 | 83.7 |  |
| 72 | Santa Barbara Foundation | CA | 118 | 90.8 | 84.1 | 84.0 | 85.7 |  |
| 73 | Armstrong County Community | PA | 1 | 77.5 | 77.1 | 76.5 | 38.2 |  |
| 74 | Gulf Coast Community Foundation Inc | FL | 74 | 86.0 | 69.1 | 61.4 | 76.1 |  |
| 75 | The Philadelphia Foundation | PA | 80 | 69.9 | 68.7 | 53.2 | 50.9 |  |
| 76 | The Vermont Community Foundation | VT | 81 | 89.7 | — | 6.8 | 64.8 |  |
| 77 | Community Foundation Of Acadiana | LA | 30 | 86.0 | 66.9 | 52.8 | 77.4 |  |
| 78 | The Community Foundation Of Utah | UT | 76 | 86.3 | 68.0 | 67.5 | 82.4 |  |
| 79 | Toledo Community Foundation Inc | OH | 33 | 83.0 | 76.2 | 53.5 | 53.2 |  |
| 80 | Nevada Community Foundation Inc | NV | 16 | 63.6 | 62.8 | 62.8 | 92.8 |  |
| 82 | Blue Grass Community Foundation Inc | KY | 40 | 81.6 | 63.7 | 36.8 | 49.9 |  |
| 83 | The Community Foundation | NC | 36 | 88.1 | 62.8 | 44.2 | 64.8 |  |
| 84 | The Greater Kanawha Valley Foundation | WV | 16 | 97.0 | 74.8 | — | 42.4 |  |
| 85 | Greater Salina Community Foundation | KS | 36 | 88.5 | 54.3 | 45.8 | 62.3 |  |
| 86 | Community Foundation Of The Ozarks Inc | MO | 33 | 85.8 | 60.1 | 41.2 | 50.4 |  |
| 87 | Central Carolina Community | SC | 39 | 90.9 | 70.2 | 58.1 | 41.3 |  |
| 88 | Lancaster County Community Foundation | PA | 26 | 97.3 | 87.6 | 87.9 | 18.8 |  |
| 89 | Delaware Community Foundation Inc | DE | 68 | 53.2 | 49.8 | 36.0 | 59.1 |  |
| 90 | Grand Rapids Community Foundation | MI | 28 | 94.6 | 88.4 | 82.1 | 34.7 |  |
| 91 | Idaho Community Foundation Inc | ID | 23 | 98.0 | 58.1 | 40.2 | 57.3 |  |
| 92 | Community Foundation Of Greater | NC | 24 | 86.1 | 71.3 | 74.3 | 76.9 |  |
| 93 | Fairfield County'S Community Foundation | CT | 46 | 56.1 | 48.1 | 50.2 | 69.6 |  |
| 94 | Lincoln Community Foundation Inc | NE | 41 | 92.7 | 87.9 | 85.2 | 78.1 |  |
| 96 | The Dayton Foundation | OH | 81 | 92.9 | 86.1 | 81.3 | 20.4 |  |
| 97 | The Indianapolis Foundation Inc | IN | 86 | 87.3 | 84.0 | 81.2 | 56.6 |  |
| 98 | Collier Community Foundation Inc | FL | 84 | 84.3 | 73.1 | 72.5 | 33.1 |  |
| 99 | Community Foundation Of Greater | IN | 19 | 81.9 | 74.3 | 77.4 | 54.4 |  |
| 100 | Community Foundation Of Northern | CO | 21 | 83.0 | 72.2 | 71.6 | 60.3 |  |