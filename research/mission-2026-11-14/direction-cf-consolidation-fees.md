# Community-foundation consolidation 2021–2026 and the CF DAF fee census

**Date:** 2026-11-15 · **Queue item:** P-NEW-CFC-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/cf-consolidation-2021-2026.csv`](../../data/mission-2026-11-14/cf-consolidation-2021-2026.csv): 19 events (C001–C019). Nine come from press and CF sites; ten are Schedule N transfers filed with the IRS.
- [`data/mission-2026-11-14/cf-daf-fee-census-2026.csv`](../../data/mission-2026-11-14/cf-daf-fee-census-2026.csv): 100 CF rows, ranked by FY2024 DAF assets, plus five national comparator rows.
- [`data/mission-2026-11-14/queue-proposals-batch40-n11.csv`](../../data/mission-2026-11-14/queue-proposals-batch40-n11.csv): P-B40N11-01 to P-B40N11-03.
- Script (stdlib only, functional style): [`scripts/mission_cf_fee_census.py`](../../scripts/mission_cf_fee_census.py). The transcribed constants live in [`scripts/mission_cf_fee_data.py`](../../scripts/mission_cf_fee_data.py). Tasks:
  - `crawl`: robots.txt, then homepage and sitemap discovery of fee pages.
  - `urls`: fetches the fee pages found by search, after a robots check.
  - `census`: checks every quote against the cached copy of its page, then computes fees.
  - `schedn`: the Schedule N screen.
  - `consol`: builds the consolidation CSV.

**Rules followed**
- **Access:** no logins, no form submissions and no outreach.
- **robots.txt:** read before any fetch on a host and obeyed. A 401/403 on robots.txt counts as "disallow all". The GivingTuesday S3 mirror returns 404 for robots.txt, so it publishes no restrictions. crt.sh and fcsuite.com were not used.
- **Recency:** fee sources dated before 2021 are recorded but kept out of the distribution. Events dated before 2021 are excluded; Southfield CF into CFSEM (2014) and Sunbury into Community Giving Foundation (2020) were dropped on this rule.
- **Governing corrections respected:**
  - `queue-batch32-infund-costs.md` wave 17: the Fidelity all-in floor is "about 50–52 bps", not 51.5.
  - `sponsor-cost-structure-and-sensitivities.md` wave 5: the Fidelity cost figures are labelled "latest 990". They are not used here.
  - `queue-batch30-cf-coverage-give.md` wave 15 and the crt.sh compliance note: nothing here relies on certificate data.

**Labels:** [F] first-party page, PDF or filing, with the quote verified against the script cache · [W] first-party page read through WebFetch only (cannot be verified by script) · [R] search-engine capture · [C] my computation · [I] my inference.

---

## 0. Headline answers

| Question | Answer | Confidence |
|---|---|---|
| **How much CF consolidation was there in 2021–2026?** | **It was small and local. I found 19 events and no combination of two top-100 CFs.**<br>- **Largest press-documented merger:** Community Foundation of Orange & Sullivan with Rockland CF (NY), effective 2026-01-01, with about $71m of combined assets [F press].<br>- **Filed transfers:** ten Schedule N transfers to or from CFs, each $0.5m–$21.6m [F].<br>- **Acquirers:** San Diego Foundation (top-100 #15) absorbed Coastal CF ($10.07m, 2024-07-15). The other filed acquirers are regional CFs outside the top 100: Eau Claire CF took Rusk County CF ($2.14m, 2023); the Community Foundation of the Upper Peninsula took Keweenaw CF ($10.5m, 2021); Hamilton CF took Fairfield CF (OH; $4.46m, 2022); CommunityGiving (MN) took Greater White Bear Lake CF's DAF, endowment and designated balances ($4.97m, 2025).<br>- **Examples the owner named:** I found no 2021–2026 affiliation by the Community Foundation of Greater Memphis and no combination by the Greater Houston Community Foundation. The Saint Paul & Minnesota merger is dated 2020-01-01, outside the window. | High for filed rows; medium for search-capture rows |
| **How many top-100 CFs publish a DAF fee schedule?** | **34 publish a full schedule for a standard DAF from a 2021+ source. They hold 43.0% of top-100 CF DAF assets.**<br>- 5 more publish only pre-2021 schedules.<br>- 13 publish partial terms or non-comparable structures: 10 partial, 1 flat fee on a non-invested fund, 2 charged on grants or gifts.<br>- 7 have a fee page with no rates.<br>- 41 had no fee terms found. They hold 40.3% of assets, including SVCF, which alone holds 17.3%.<br>- **Quote checks:** 56 of 56 checkable quotes verified against the cached source text. One schedule (Pittsburgh) is WebFetch-only, and two partial rows rest on search captures. | High [F/C] |
| **What is the effective admin fee at $100k / $1m / $10m?** | **Median 100 / 100 / 67 bps across the 34 published schedules** (interquartile ranges 100–131, 100–125 and 47–85). The DAF-asset-weighted means are 99.5 / 90.6 / 59.5 bps.<br>- **Range:** 50 bps (NYCT, a flat rate) up to 250 bps (Seattle at $100k, because of its $2,500 minimum).<br>- **Sacramento:** its expendable DAF is 200 bps at $1m and 165 bps at $10m. | High [F/C] |
| **How do CFs compare with the national sponsors?** | **On the admin layer alone, the CF median is about 1.7x the nationals at $100k, 2.2x at $1m and about 3.5–4.5x at $10m.**<br>- Fidelity, Vanguard, DAFgiving360 and Charityvest are 60 / 45 bps at $100k / $1m, and Vanguard is 14.3 bps at $10m.<br>- **Every published CF schedule is above 45 bps at $1m.** Only NYCT (50 bps) and CCT (60 bps) are at or below the nationals' 60 bps at $100k. | High [C]; comparison excludes investment layers [I] |
| **Minimums** | Median minimum annual fee **$250** (n=24; range $50–$2,500). Median opening minimum **$10,000** (n=26; range $0–$100k). Median minimum grant **$250** (n=10). | High [F] |

---

## 1. Method

### 1.1 Consolidation (task `schedn` and `consol`)

1. **Press and CF sites.** I ran about 20 web searches: generic merger, affiliation and dissolution phrasing, regional searches for the Midwest, the Mountain West and the coasts, and the owner's named examples (Memphis, Houston, Minnesota, Iowa). Each candidate was read on the source page where the host allowed it. Rows read only through a search capture are labelled "medium (search capture)".
2. **Filed Schedule N.** I scanned two sets of returns:
   - **Local XML:** 2,094 IRS e-file XMLs already in this session's scratch caches.
   - **CF filers' own returns:** all 2,795 returns for tax years 2021 and later filed by the 809 CF filers in `cf-vendor-map-by-ein-v2.csv`, using the return list in `form990-returns-schedule-d-harvest-full.csv`. These were read from the GivingTuesday mirror.

   Each return was streamed only as far as `</IRS990>`, to read two indicators: Part I line 2 (`ContractTerminationInd`, "discontinued operations or disposed of more than 25% of net assets") and the final-return box (`FinalReturnInd`). The full XML was fetched only when one of them was set.
   - **Tags:** the e-file returns carry no separate Part IV line 31/32 tags, so Part I line 2 is the screen. All 2,795 returns were read without error, and 5 were flagged.
   - **Rows kept:** Schedule N lines are summed per return and transferee. A row is kept when the filer or the transferee is a CF (EIN in the CF map, or a CF-style name) and the distribution date is 2021 or later.
   - **Exclusion:** National Christian Community Foundation is excluded because it is a faith-based DAF sponsor, not a geographic CF.

### 1.2 Fee census (tasks `crawl`, `urls`, `census`)

1. **Universe.** The top 100 CFs by `fy2024_daf_assets_usd` in `cf-vendor-map-by-ein-v2.csv` (DAFRC FY2024): $55.35bn of the file's $66.14bn.
2. **Discovery.**
   - **Crawl:** robots.txt, homepage and sitemap. Fee-like links were followed: up to 10 pages and 6 PDFs per CF. Homepages returned 200 for 90 of the 100.
   - **Site-restricted searches:** 14 batched searches of 10 domains each, using two phrasings, followed by targeted searches for the largest gaps.
   - **Fetching:** every page found was fetched by the script (`urls` task) and cached. PDFs were converted with `pdftotext -layout`.
3. **Transcription.** Values were transcribed by hand into `FEE_DATA`, each with verbatim quotes. The census task checks each quote against the cached text of its own URL after normalising whitespace, case and quotation marks.
   - **Result:** 56 of 56 quotes checked were verified.
   - **Baltimore:** its PDF reset the script's connection but was saved by WebFetch, so the script checks it from a local copy.
   - **Pittsburgh:** the site returns 403 to the script, so the row is WebFetch-only [W].
4. **Fund type.** Each row uses the CF's standard, invested DAF. Where a CF offers both endowed and non-endowed DAFs, I used the non-endowed fund, which is the comparable product (for example Maine, Rochester, Baltimore, Sacramento, NCCF and OCCF).
5. **Fee engine.** The effective annual admin fee is computed at a constant balance:
   - **Tier basis:** `marginal` (each rate applies to its slice) or `flat_on_total` (one rate on the whole balance). Omaha is the only flat-on-total CF.
   - **Hybrid:** OCCF is marginal to $5m, then charges a flat rate on the whole balance above $5m, $7.5m, $10m and so on.
   - **Cap:** above a stated cap (GKCCF $7m; GHCF and Birmingham $10m) the fee is blank, because the CF prices it individually.
   - **Floor and add-ons:** the minimum annual fee is applied as a floor, then any flat annual fee is added.
   - **Basis not stated:** six schedules do not say whether their tiers are marginal (Columbus, Oregon, Pittsburgh, GiveWell, Lincoln, Monterey). They are computed as marginal, and the `_alt_flat` columns give the flat-on-total alternative. The median at $10m falls from 67.2 to 55.0 bps under the alternative, and the medians at $100k and $1m do not change.
6. **National comparators.** These are transcribed from `sponsor-fee-schedules.csv` (repo, retrieved 2026-11-14) and computed with the same engine:
   - **Fidelity:** no price at $10m (balances of $5m or more are quoted by phone).
   - **DAFgiving360:** the breakpoint of its 0.15% tier is unverified in the repo.
   - **Bank of America:** flat rate by band.

---

## 2. Consolidation results (2021–2026)

| ID | Date | Event | Assets moved | Source |
|---|---|---|---|---|
| C010 | 2021-01-01 | Shelby CF (MI) liquidates into Four County CF | $0.88m | [F] Schedule N, [object 202242839349300309](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202242839349300309_public.xml) |
| C011 | 2021-09-01 | Keweenaw CF transfers more than 25% of net assets to the Community Foundation of the Upper Peninsula (MI) | $10.55m | [F] Schedule N ([object 202321939349300617](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202321939349300617_public.xml)) |
| C009 | 2022-05 | Lodi CF affiliates with CF of San Joaquin; more than $5m moved from Sacramento Region CF (top-100 #81) | >$5m | [R] [Lodi News-Sentinel](https://www.pressreader.com/usa/lodi-news-sentinel/20220511/281487869941301); [SRCF 2022 Year in Review](https://www.sacregcf.org/year-in-review-2022/) |
| C012 | 2022-06-30 | Fairfield CF (OH) transfers its funds to Hamilton CF | $4.46m | [F] Schedule N |
| C013 | 2022-12-31 | Milbank CF (SD) liquidates (transferee is a school foundation) | $0.55m | [F] Schedule N |
| C014 | 2023-03-31 | Rusk County CF (WI) dissolves into Eau Claire CF ("net assets transfer upon dissolution") | $2.14m | [F] Schedule N, [object 202303209349302295](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202303209349302295_public.xml) |
| C008 | 2023-07-01 | Dunkirk Foundation's 14 funds merge into The Portland Foundation (IN) | $2.06m | [R] [Commercial Review](https://thecr.com/news/2023/jun/21/foundation-merger-okd) |
| C015–16 | 2023-08-30 | Oracle Health Foundation winds down with "donor advised fund distribution" lines to Catholic Community Foundation ($0.77m) and GKCCF ($0.55m) | $1.32m to CFs | [F] Schedule N. The same return sends $12.3m to NPT and $0.29m to Schwab Charitable. |
| C017 | 2024-07-15 | Coastal CF (Encinitas, CA) liquidates into San Diego Foundation (top-100 #15). Press: integrated from 2024-08-26 and keeps its brand | $10.07m | [F] Schedule N ([object 202530559349300993](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202530559349300993_public.xml)); [Coast News](https://thecoastnews.com/coastal-community-foundation-merges-with-san-diego-foundation/) |
| C003 | 2024-11 | Idaho Nonprofit Center merges into Idaho CF (#91) | n/a | [F] [ICF release 2024-10-09](https://www.idahocf.org/docs/press/100924-Merger-Announcement.pdf) (read from a WebFetch-saved copy of the PDF); [Murdock Trust](https://murdocktrust.org/2026/08/merging-from-strength-idaho-community-foundation-and-idaho-nonprofit-center) |
| C002 | 2025-01-01 | Three Rivers Area CF becomes an affiliate of Sturgis Area CF (MI), under SACF's EIN | not stated | [F press] [Watershed Voice](https://watershedvoice.com/2024/12/09/three-rivers-sturgis-area-community-foundations-merging-on-january-1/) |
| C018 | 2025-01-31 | Greater White Bear Lake CF (MN) transfers "fund balances related to DAF, endowment funds and designated funds" to CommunityGiving | $4.97m | [F] Schedule N ([object 202610829349301016](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610829349301016_public.xml)) |
| C006 | 2025-05-27 | Jewish Community Foundation San Diego and Leichtag Foundation announce a merger of operations | not stated | [R] [Times of San Diego](https://timesofsandiego.com/life/2025/05/27/influential-san-diego-jewish-philanthropic-foundations-merge/) |
| C007 | 2025-06-12 | Home Health Care Foundation (a BCCF affiliate since 2020) merges into Berks County CF | $7.3m | [F] [BCCF](https://bccf.org/home-health-care-foundation-entrusts-assets-to-berks-county-community-foundation/) |
| C005 | 2025 | Maine Women's Fund dissolves into Maine CF as two field-of-interest funds | about $3m | [R] [Mainebiz](https://mainebiz.biz/article/maine-womens-fund-to-dissolve-transfer-assets-to-maine-community-foundation/) |
| C019 | 2025-12-18 (as filed) | Watertown Area CF (SD) transfers more than 25% of net assets to "Watertown Community Foundation Inc" | $21.58m | [F] Schedule N (TY2024 return; the date is as filed) |
| C001 | 2026-01-01 | Community Foundation of Orange & Sullivan and Rockland CF merge into the Community Foundation of Orange, Sullivan and Rockland (NY AG approval) | about $71m combined | [F press] [Radio Catskill](https://radiocatskill.org/new-regional-community-foundation-forms-managing-71-million-in-local-giving/) |
| C004 | 2026-04-01 | Community Foundation of Teton Valley leaves Jackson Hole CF to become independent (a reverse move) | not stated | [R] [Buckrail](https://buckrail.com/community-foundation-of-teton-valley-becomes-independent-organization/) |

**Findings.**
1. **Size [C].** No event combines two top-100 CFs. Top-100 CFs appear only as acquirers or counterparties: San Diego (Coastal), Idaho (Idaho Nonprofit Center), Maine (Maine Women's Fund), GKCCF (as a recipient of DAF distributions) and Sacramento (the source of the Lodi assets). The largest filed transfer is $21.6m (Watertown), about 0.04% of top-100 CF DAF assets.
2. **Base rate [C].** Only 5 of the 809 DAFRC CF filers (2,795 returns for 2021+) set Part I line 2 or filed a final return in the window. That is about 0.6% of CF filers over roughly four years. Small CFs below the DAFRC list were not screened (P-B40N11-02).
3. **DAF assets moved [F].** Only two filings name DAFs: Greater White Bear Lake ("fund balances related to DAF, endowment ... designated funds", $4.97m) and Oracle Health's "donor advised fund distribution" lines. Schedule N reports total assets, not DAF-only balances, so `daf_or_asset_usd_moved` is an all-asset figure unless the asset description says otherwise.
4. **Owner's named examples.** I found no 2021–2026 affiliation by the Community Foundation of Greater Memphis and no Greater Houston combination. Houston's 2023–26 items are partnerships (the Greater Houston Disaster Alliance with United Way) [R]. Minnesota's notable merger (Saint Paul Foundation with Minnesota Community Foundation) is dated 2020-01-01 [R], and WCA Foundation joined the Minneapolis Foundation as a signature fund in 2020 [R]; both are excluded by the recency rule. In Minnesota the 2021–26 evidence is the White Bear Lake transfer (C018); in Iowa I found no 2021–26 CF merger.
5. **Why [I].** The Idaho case study and the NY merger both describe mergers made from strength rather than distress. The Idaho study cites competition from commercial DAFs. Small CFs dissolve into regional CFs (MI, WI, OH, SD, IN). The direction is regional pooling of back-office work, and the counts are not large enough to call a trend.

---

## 3. CF DAF fee census results

### 3.1 Coverage (top 100 by FY2024 DAF assets, $55.35bn)

| Status | CFs | Share of top-100 DAF assets |
|---|---|---|
| `published_schedule` (2021+, standard DAF) | 34 | 43.0% |
| `published_schedule_pre2021` (SFF 2019, Minneapolis 2020, Greater Cincinnati 2020, Toledo 2016, San Antonio 2020) | 5 | 3.6% |
| `partial` (Marin, SPMCF, CFSEM, Sioux Falls, Dayton, EBCF, CFWNC, Ozarks, Hampton Roads [R], Triangle [R]) | 10 | 5.9% |
| `noninvested_flat` (Winston-Salem: $120 a year, income kept by the CF) | 1 | 0.6% |
| `grant_or_gift_based` (Fort Wayne 2% of grants, $500 minimum; Arkansas 2% gift fee) | 2 | 0.8% |
| `no_rates_published` (Collier, St. Louis, Cleveland, Greater Washington, Boston, CFT, Greater Salina) | 7 | 5.7% |
| `not_found` (includes SVCF, California CF, CFNJ, Denver, San Diego, Memphis, Tulsa, Tampa Bay, NH Charitable, Louisville, Arizona, North Texas, Richmond) | 41 | 40.3% |

Two notes on this table:
- **Non-publishing sites [F].** CalFund's fee PDFs returned 502, and FFTC's older URL returned 404. Tampa's "Community Investment Fee Schedule" link (2022) now redirects to the homepage. Several CFs state that the schedule is "available upon request" (Boston, Lancaster).
- **Selection bias [I].** The largest CFs are over-represented among non-publishers: 3 of the top 10 (SVCF, California CF, Boston) have no published schedule.

### 3.2 Effective annual admin fee, published schedules (n=34; n=33 at $10m)

| Balance | Min | P25 | Median | P75 | Max | Mean | DAF-asset-weighted mean |
|---|---|---|---|---|---|---|---|
| $100k | 50 | 100 | **100** | 131 | 250 | 117 | 99.5 |
| $1m | 50 | 100 | **100** | 125 | 200 | 110 | 90.6 |
| $10m | 28.8 | 46.5 | **67.2** | 85 | 165 | 71.6 | 59.5 |

Units are bps of balance [C]. Under the flat-on-total alternative for the six schedules that do not state a basis, the medians are 100 / 100 / 55 bps.

**Shape [C].**
- At $100k, 30 of 34 are at 100 bps or more.
- At $1m, 27 of 34 are still at 100 bps or more: most CF tiers do not break until $1–2m.
- At $10m, 13 of 33 are at 60 bps or less.

### 3.3 Per-CF results vs nationals (bps at $100k / $1m / $10m)

| Rank | CF | Min fee ($) | $100k | $1m | $10m | Source date |
|---|---|---|---|---|---|---|
| 2 | Chicago Community Trust | 360 | 60 | 60 | 40.5 | undated PDF, live |
| 3 | Foundation For The Carolinas | 500 | 85 | 85 | 48.0 | undated PDF, live |
| 4 | Greater Kansas City CF | 250 | 100 | 80 | – (cap $7m) | undated PDF, live |
| 5 | Columbus Foundation | 600 | 90 | 85 | 43.5 | 2025–26 |
| 6 | New York Community Trust | 100 | 50 | 50 | 50 | 2025 policies (or 2.5% of grants if greater) |
| 7 | Oregon CF | 500 | 100 | 100 | 76.0 | live |
| 10 | CF for Greater Atlanta | 1,000 | 100 | 85 | 64.0 | 2022-08 |
| 11 | Greater Houston CF | 1,500 | 150 | 118.8 | 60.9 | April 2023 |
| 18 | Seattle Foundation | 2,500 | 250 | 112.5 | 73.8 | 2025 |
| 25 | Pittsburgh Foundation [W] | 275 | 110 | 110 | 79.5 | live |
| 26 | Omaha CF (flat by band) | 750 | 100 | 100 | 50.0 | 2022 |
| 28 | GiveWell CF | – | 150 | 131.2 | 85.6 | live |
| 29 | CF for Northeast Florida | 250 | 100 | 100 | 76.0 | 2022-10 |
| 32 | CF of Middle Tennessee | – | 125 | 125 | 125 | live |
| 33 | Orange County CF (hybrid) | – | 200 | 200 | 75.0 | 2024 |
| 35 | Rhode Island Foundation | – | 100 | 100 | 100 | 2026-07 |
| 42 | CF of Greater Des Moines | 250 | 100 | 100 | 28.8 | 2025-03 |
| 43/97 | Central Indiana CF / Indianapolis Fdn | 250 | 100 | 100 | 45.0 | 2026-02 |
| 49 | Maine CF | 200 | 125 | 125 | 52.0 | 2022-09 schedule |
| 51 | CF for the Fox Valley Region | – | 100 | 100 | 45.0 | 2026-01-01 |
| 52 | CF of the Chattahoochee Valley (cfcv.com; name per site) | 50 | 100 | 100 | 65.0 | 2026-03 |
| 53 | Hawaii CF (+3% on additions) | – | 150 | 150 | 150 | live (conflicts with a 2025 one-sheet: 1%) |
| 56 | Dallas Foundation (+0.15–0.30% oversight) | – | 110 | 110 | 67.2 | 2021-06 |
| 60 | North Carolina CF | 250 | 100 | 100 | 100 | 2025-09 |
| 63 | Baltimore CF | 375 | 150 | 137.5 | 51.2 | 2025-02 |
| 66 | CF of Greater Birmingham | 250 | 100 | 100 | 40.0 | live |
| 68 | Rochester Area CF | 250 | 100 | 90 | 68.5 | live |
| 75 | Philadelphia Foundation (+1% gift fee) | 250 | 100 | 100 | 100 | 2023 form |
| 78 | CF of Utah (+1% contribution fee) | – | 105 | 105 | 105 | 2026 |
| 81 | Sacramento Region CF | 250 | 200 | 200 | 165 | live |
| 89 | Delaware CF | 250 | 100 | 100 | 35.0 | 2023-12 |
| 94 | Lincoln CF | – | 150 | 143.8 | 84.4 | live |
| 95 | CF for Monterey County | – | 125 | 125 | 67.5 | 2025-09 |
| — | **Fidelity Charitable** | 100 | 60 | 45 | – (≥$5m by phone) | repo |
| — | **Vanguard Charitable (Premier)** | – | 60 | 45 | 14.3 | repo |
| — | **DAFgiving360** | – | 60 | 45 | 18.8 | repo |
| — | **Bank of America CGF** | – | 90 | 50 | 15.0 | repo |
| — | **Charityvest (invested)** | 100 | 60 | 45 | 16.2 | repo |

Sources: each row's `source_url` in the CSV. Examples: [CCT](https://donorportal.cct.org/ma/docs/cct/CCT-DAF-Application.pdf), [FFTC](https://www.fftc.org/sites/default/files/documents/FFTC_Personal_Fees.pdf), [GKCCF](https://www.growyourgiving.org/documents/administrative-fees.pdf), [Columbus](https://columbusfoundation.org/media/5vpaw45n/dsd-handouts-admin-fees-2025-202620260213193902651.pdf), [NYCT](https://thenytrust.org/advisors/fees/), [Oregon](https://www.oregoncf.org/fees), [Atlanta](https://cfgreateratlanta.org/wp-content/uploads/2023/08/DAF-Options_20220808.pdf), [GHCF](https://ghcf.org/wp-content/uploads/2024/04/Updated-Fee-Schedule-2023.pdf), [Seattle](https://www.seattlefoundation.org/wp-content/uploads/2025/09/SeaFdn-DAF-Collateral-2.pdf), [Pittsburgh](https://pittsburghfoundation.org/admin-fees), [Des Moines](https://www.desmoinesfoundation.org/filesimages/2025/New%20Admin%20Fee%20Sheets/AdminFee_DonorAdvisedFund_March2025.pdf), [CICF](https://www.cicf.org/wp-content/uploads/2026/02/Minimums-and-Fees-Quick-Reference-CICF-Collaborative_.pdf), [Sacramento](https://www.sacregcf.org/fees), [OCCF](https://www.oc-cf.org/about-us/financials/fees/), [Rochester](https://www.racf.org/giving/policies-and-fees/), [Baltimore](https://www.bcf.org/wp-content/uploads/2025/02/Administrative-Fees_Utilitarian_2025.pdf).

### 3.4 Comparison with the national sponsors

- **Admin layer [C].**
  - At **$100k** the CF median (100 bps) is 1.67x the 60 bps charged by Fidelity, Vanguard, DAFgiving360 and Charityvest. 32 of 34 CFs charge more.
  - At **$1m** it is 2.2x the 45 bps (Bank of America 50). All 34 CFs charge more.
  - At **$10m** it is 3.6–4.7x the 14–19 bps nationals. All 33 CFs charge more.
- **Where the gap comes from.** The gap widens with balance because national tiers break at $500k and $1m, while CF tiers commonly hold 1% to $1–2m.
- **Investment layer [F/I].** CF admin fees generally exclude investment costs, so the all-in gap depends on the investment layer:
  - Atlanta's pool is about 92 bps. GHCF's pools are 18–50 bps. GiveWell's are 5–66 bps. Birmingham's are "usually" 10–60 bps. SPMCF's options are 14–53 bps.
  - Dallas charges its own 15–30 bps "investment oversight fee" on top of manager fees.
  - On the national side, the repo's in-fund layer at Fidelity is 26.3 bps (asset-weighted pool ratio, FY2025), with an all-in floor of about 50–52 bps per invested dollar (`queue-batch32-infund-costs.md`, wave-17 governing text).

  An all-in CF comparison is proposed as P-B40N11-03.
- **Other add-ons [F].** Contribution or gift fees (Hawaii 3% on non-endowed additions, Utah 1%, Philadelphia 1%) and grant-based legs (NYCT: greater of 0.5% or 2.5% of grants; Fort Wayne 2% of grants) raise the cost for active givers. Nationals in the repo charge none of these on standard grants.
- **Context [I].** CF admin fees fund community programmes as well as administration: Utah splits its 1.05% into 44 bps fund management and 61 bps community impact. The repo's 196 bps median of CF Part IX operating cost per DAF dollar (`queue-batch32-infund-costs.md`) is not the same measure. It covers all fund types and is not a donor-facing price.

---

## 4. Limitations

1. **Coverage bias.** 41 not-found CFs plus 7 with no published rates hold 46% of top-100 DAF assets. SVCF, the largest at 17.3%, publishes no schedule that was found. Published lists may also differ from negotiated rates for large funds: several CFs say large-fund fees are "individually determined", "negotiable" or subject to "rebates". P-B40N11-01 proposes a realised-rate check from audited statements.
2. **Dating.** Several PDFs carry no date. They are labelled "undated, live 2026-11-15", and the `source_date` column records what the document shows. Hawaii's live page conflicts with its 2025 one-sheet; the live page was used.
3. **Interpretation.**
   - **Basis:** six schedules do not state their tier basis (see §1.2).
   - **Monterey:** the source prints "$2-$3 million: 1.0%", which I read as $1–3m.
   - **Omaha:** a balance of exactly $10m is put in its "above $10m" band.
   - **CICF and the Indianapolis Foundation:** they share one schedule (the Indianapolis Foundation is a CICF affiliate), so it enters the distribution twice. This has no effect on the medians.
4. **Constant-balance fees.** Fees are computed on a constant balance. They ignore contribution and grant fees, peak-value or 36-month-average bases (Baltimore, Pittsburgh, Minneapolis) and quarterly rounding.
5. **Consolidation sources.** The press side is search-based and certainly incomplete. The Schedule N side covers only the 809 DAFRC CF filers and the local caches. Watertown's distribution date (2025-12-18) on a TY2024 return is reproduced as filed. Several rows rely on a search-engine summary because the publisher blocked fetches (Dunkirk, Lodi, Maine Women's Fund, Teton Valley, Leichtag); these are labelled medium or low confidence.
6. **Council on Foundations and CF Insights.** No public page with merger counts was found. The CF Insights results pages list assets only.

---

## 5. Data dictionary

### `cf-daf-fee-census-2026.csv`

The file has 100 CF rows and 5 `national_comparator` rows.

| Column | Meaning |
|---|---|
| `rank`, `ein`, `name`, `fy2024_daf_assets_usd` | Rank by FY2024 DAF assets, from `cf-vendor-map-by-ein-v2.csv` (DAFRC) |
| `status` | `published_schedule` · `published_schedule_pre2021` · `partial` · `noninvested_flat` · `grant_or_gift_based` · `no_rates_published` · `not_found` · `national_comparator` |
| `fund_type` | The DAF product the row describes. Non-endowed or invested is preferred. |
| `fee_basis`, `basis_stated` | `marginal` or `flat_on_total`. `basis_stated`=no means the source does not say which. |
| `admin_tiers` | Tiers as `lower-upper: rate%`. A blank upper bound means open-ended. |
| `min_annual_fee_usd`, `flat_annual_fee_usd` | Minimum annual admin fee, and any flat annual fee |
| `min_opening_usd`, `min_grant_usd` | Minimum initial contribution or maintained balance, and minimum grant |
| `investment_fee_pass_through` | What the source says about investment costs |
| `admin_fee_usd_{100,1000,10000}k`, `admin_bps_*` | Effective annual admin fee at a constant balance [C]. Blank means not priced, or a non-comparable status. |
| `admin_bps_*_alt_flat` | Flat-on-total alternative, only where `basis_stated`=no |
| `cap_usd` | Balance above which the CF prices individually |
| `contribution_fee_pct`, `grant_fee_note` | Fees on gifts or grants that are not in the balance-based figure |
| `source_url`, `source_date`, `source_method` | Source and how it was read: `script_fetch`, `webfetch`, `webfetch_saved_pdf` or `search_capture` |
| `quote_check` | `verified k/n` (quotes found in the cached text) · `not_verifiable(...)` · `no_quote` |
| `notes`, `retrieved` | Free-text notes and the retrieval date |

### `cf-consolidation-2021-2026.csv`

| Column | Meaning |
|---|---|
| `event_id` | C001–C019 |
| `event_type` | Press-sourced rows: `cf_cf_merger`, `cf_affiliation`, `cf_affiliation_with_asset_transfer`, `cf_cf_fund_transfer`, `cf_absorbs_*`, `cf_disaffiliation` and so on.<br>Filed rows: `schedule_n_liquidation` (Part I) and `schedule_n_disposition_over_25pct` (Part II). |
| `party_a`, `party_b` | Transferor or joining entity, and the acquirer or transferee (with EIN where filed) |
| `date`, `year` | Effective, distribution or announcement date |
| `daf_or_asset_usd_moved`, `asset_basis` | Dollar amount and what it measures. For Schedule N it is the summed FMV of assets distributed, which is all assets unless the description names DAFs. |
| `description`, `geography`, `cf_role` | Event summary, location, and which party is a CF |
| `source_url`, `source_type`, `confidence`, `notes` | Source (e-file XML URL for Schedule N), its type, the confidence level and notes |

### Reproduce

```
C=<cache dir>
python3 scripts/mission_cf_fee_census.py --task crawl  --cache-dir $C --fetch
python3 scripts/mission_cf_fee_census.py --task urls   --cache-dir $C --fetch --url-file <urls.txt>
python3 scripts/mission_cf_fee_census.py --task census --cache-dir $C
python3 scripts/mission_cf_fee_census.py --task schedn --cache-dir $C --xml-dir <dir with 990 XML> --fetch
python3 scripts/mission_cf_fee_census.py --task consol --cache-dir $C
```

## Validation corrections (wave 25A, 2026-11-15) — governing
Source: [validation-wave25a-report.md](validation-wave25a-report.md); register `data/mission-2026-11-14/validation-register-wave25a.csv`.

1. **§0, national comparison row (governing replacement).**
   - **Find:** "and about 3.5–4.5x at $10m.**"
   - **Replace with:** "and about 3.6–4.7x at $10m (67.2 bps against 18.8 and 14.3 bps).** [V wave 25A]"
2. **§0, minimums row.**
   - **Find:** "Median opening minimum **$10,000** (n=26; range $0–$100k). Median minimum grant **$250** (n=10)."
   - **Replace with:** "Median opening minimum **$10,000** (n=26; range $0–$100k) and median minimum grant **$250** (n=10). Both pool all statuses, not just published schedules. On the 34 published schedules alone the opening median is $15,000 (n=19) and the grant median $250 (n=4) [V wave 25A]."
3. **§1.1, CF filers' returns.**
   - **Find:** "filed by the 809 CF filers in"
   - **Replace with:** "filed by the 803 CF filers (803 distinct EINs) in"
4. **§2, Findings, item 2 (governing replacement).**
   - **Find:** "Only 5 of the 809 DAFRC CF filers (2,795 returns for 2021+) set Part I line 2 or filed a final return in the window. That is about 0.6% of CF filers over roughly four years."
   - **Replace with:** "Only 5 of the 803 DAFRC CF filers (2,795 returns for 2021+) set Part I line 2 or filed a final return in the window. That is about 0.6% of CF filers over roughly four years. A wave-25A re-run with an empty cache reproduced the 2,795 returns and the same 5 flags (Rusk County, Keweenaw, Watertown Area, Coastal, Greater White Bear Lake) [V wave 25A]."
5. **§2, Findings, item 1.**
   - **Find:** "The largest filed transfer is $21.6m (Watertown), about 0.04% of top-100 CF DAF assets."
   - **Replace with:** "The largest filed transfer is $21.6m (Watertown), about 0.04% of top-100 CF DAF assets. Its transferee, 'Watertown Community Foundation Inc', is in the same town and has no EIN on Schedule N, and the filer did not file a final return. It may be a same-community successor or affiliate rather than a combination of two CFs [V wave 25A]."
6. **§4, Limitations, item 5.**
   - **Find:** "The Schedule N side covers only the 809 DAFRC CF filers"
   - **Replace with:** "The Schedule N side covers only the 803 DAFRC CF filers"
7. **§0, consolidation row.**
   - **Find:** "with about $71m of combined assets [F press]."
   - **Replace with:** "with about $71m of combined assets [F press]. The NY AG's approval is confirmed by Mid-Hudson News (2026-01-30); the $71m and the effective date were not re-read in wave 25A [V wave 25A]."
