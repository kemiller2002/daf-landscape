# Direction P-NEW-GEO-01: where DAF grant dollars land — state and metro geography of top-50 sponsors' grants, FY2023–FY2024

**Date:** 2026-11-15 · **Queue item:** P-NEW-GEO-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/daf-grant-geography-state-2023-2024.csv`](../../data/mission-2026-11-14/daf-grant-geography-state-2023-2024.csv): 3,907 rows. State rows (9 sponsor scopes) and CBSA rows (4 scopes): dollars, shares, per-capita and per-501(c)(3) dollars, address-source checks, top recipient.
- [`data/mission-2026-11-14/daf-grant-geography-cf-local-share.csv`](../../data/mission-2026-11-14/daf-grant-geography-cf-local-share.csv): 48 rows, one per itemising top-50 sponsor (22 community foundations, 16 national, 1 processor, 7 single-issue, 2 university/hospital). Own-state and own-metro shares.
- [`data/mission-2026-11-14/queue-proposals-batch42-n21.csv`](../../data/mission-2026-11-14/queue-proposals-batch42-n21.csv): P-B42N21-01..03.
- **Script:** [`scripts/mission_grant_geography.py`](../../scripts/mission_grant_geography.py) (stdlib, functional style).

**Rules applied**
- **Governing corrections read first:** [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md) with its wave-24A corrections (ImpactAssets DAFRC row already replaced; SVCF drives the community-foundation DAF-to-DAF share) and [direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md) with its wave-26 corrections (LLC-named recipients $1.68bn, of which CZ Biohub/Institute $1.66bn). Neither changes the Schedule I lines used here. The SVCF/CZ effect is shown as a separate `ex_svcf` scope throughout.
- **Recency:** DAFRC FY2023–FY2024 returns only (tax years ending 2023-03-31 to 2024-12-31, i.e. TY2022–TY2024 returns, the same window as P-NEW-RCP-01). Census Vintage 2024 (July 2023 and July 2024) population; EO BMF 2026-11 snapshot.
- **robots.txt read before fetching:** www2.census.gov (no rules for `*`), gt990datalake-rawdata.s3.amazonaws.com (404, no rules). IRS BMF files were reused from the P-NEW-RCP-01 scratch copy (www.irs.gov `/pub/` allowed). No outreach.
- Evidence tags: [F] filed/published figure, [C] computed here, [I] inference.

## 0. Headline answers

| Question | Answer (all top-50 itemising sponsors excluding university/hospital sponsors; FY2023–24 pooled; net of DAF-to-DAF) |
|---|---|
| **Size** | **$77.34bn** of Schedule I Part II dollars after removing $12.73bn DAF-to-DAF (all 48 sponsors, 94 sponsor-years: $78.29bn net). $77.13bn has a US state; $212m has no address (one blank Greater Horizons FY2024 line); $0.3m is foreign-address Part II; $2.8m goes to territories and military post codes [C]. Same net total as P-NEW-RCP-01 ($77.34bn). |
| **State shares** | **CA 20.0%, NY 13.6%, DC 6.4%, MA 6.0%, MD 4.7%**, TX 4.0%, IL 3.7%, FL 3.1%, NC 2.9%, VA 2.5%. **Top 5 states take 50.7% of dollars against 21.4% of population; top 10 take 66.9%.** State HHI 783 [C]. Without SVCF: CA 15.8%, NY 14.2%, top-5 47.8% [C]. |
| **Per capita** | **$112.87 per resident per year** nationally (median state $73). **DC $3,550**, MA $325, MD $292 (Johns Hopkins $2.61bn), NY $266, VT $207, CA $196. Lowest: MS $24.7, WV $25.0, LA $30.1, SC $31.1, NV $31.3 (PR $4.1). Highest-to-lowest ratio 13× across the 50 states [C]. |
| **Per registered 501(c)(3)** | **$23,240 per BMF 501(c)(3) per year** nationally. DC $224,525; MA $61,384; NY $48,904; MD $48,521; CA $42,937. Lowest: WV $4,780; MS $5,630; SC $5,851; LA $7,043 [C]. |
| **Metros** | 97.6% of US dollars resolve to a CBSA; 96.7% of those land in metropolitan (not micropolitan) areas. **Top 10 CBSAs take 58.1% of dollars against 21.5% of US population.** NYC metro 14.3%, SF–Oakland 11.2%, Washington 8.8%, Boston 5.5%, LA 4.4%, Baltimore 4.3%, Chicago 3.6%, San Jose 2.5% [C]. Per capita among metros ≥1m: SF–Oakland $913, Baltimore $563, Washington $518, San Jose $469, Boston $413, NYC $272; lowest Riverside $15.5, Fresno $15.9, Las Vegas $20.6 [C]. |
| **National vs community foundations** | **Community foundations keep 60.0% of their US dollars in their own state (median CF 71.2%, range 20.0% Chicago Community Trust to 91.7% San Diego Foundation); national sponsors 7.6% (median 4.6%).** Median CF sends 63.3% to its own metro. National sponsors send 39.3% of their US dollars to DC/NY/MA/CA outside their own state; CFs 18.6% [C]. |
| **Outliers** | DC, NY, MA and CA are **headquarters magnets**: 54% of DC dollars go to recipients funded by ≥10 different top-50 sponsors (NY 50%, MA 53%, CA 33%), and **100% of DC dollars and 77% of NY dollars come from sponsors headquartered in another state** [C]. CA's lead is partly one sponsor: SVCF's single lines to Navigation Charitable Fund ($1.31bn) and three CZ Biohub/Institute LLCs with CA addresses ($1.41bn) [F/C]. |
| **Caveats** | Foreign grants (Schedule F) are not included. The Schedule I address is often a remittance/lockbox or national-office address, not where the money is spent (IA $644m on the Schedule I basis vs $231m on the BMF-state basis) [C/I]. |

## 1. Method

1. **Universe.** Exactly that of [`mission_recipient_sectors.py`](../../scripts/mission_recipient_sectors.py): top-50 DAFRC sponsors by FY2024 DAF assets; one return per sponsor × FY via `mission_daf_to_daf.pick_returns` over the `netpayout990/` cache; 94 itemising sponsor-years (BofA CGF, Renaissance, Greater Horizons FY2023 and Greater Kansas City CF FY2023 file Schedule I as attachments only). Full Schedule I Part II line lists come from that script's line cache.
2. **Exclusions.** Lines to an EIN whose `decision` is `include` in [`daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv), self-lines, and blank-EIN lines whose normalised name matches one whitelisted sponsor (function `annotate`, reused unchanged). $12.73bn removed in all; $12.70bn in the ex-university/hospital scope, as in P-NEW-RCP-01.
3. **Address re-read.** The line cache keeps only the recipient state, so each return's `RecipientTable` was re-read for `USAddress/ZIPCd` and `CityNm`, plus the filer header address. 51 returns came from local XML copies and 43 were streamed from the GivingTuesday mirror of IRS TEOS (`…/EfileData/XmlFiles/{OBJECT_ID}_public.xml`). **A return's addresses were accepted only if the re-read matched the cache line for line (same count, same EIN and amount on every line). All 94 matched.**
4. **State.** The Schedule I recipient state (99.7% of dollars). Foreign-address Part II lines are set aside. Lines with no address fall back to the recipient's EO BMF `STATE`; in practice no line needed this (the only address-less dollars are the $212m blank-name Greater Horizons line, which also has no EIN).
5. **Metro (CBSA).** ZIP5 → 2020 ZCTA → the county with the largest land-area overlap ([Census rel2020 ZCTA520–county](https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt)) → CBSA (county rows of [cbsa-est2024-alldata.csv](https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/metro/totals/cbsa-est2024-alldata.csv), July 2023 delineations).
   - **Non-ZCTA ZIPs** (PO boxes, lockboxes, unique ZIPs; 10.3% of dollars) take the CBSA that holds at least half the ZCTAs of their ZIP3 (`zip3_fallback`, 8.8% of US dollars).
   - **Connecticut:** the 2020 file uses the old counties, the 2023 CBSAs use planning regions; old counties are mapped by a fixed table (`CT_OLD_COUNTY_CBSA`), which is approximate (New Haven County is split between New Haven and Waterbury CBSAs).
   - Result for the main scope: 88.8% by ZCTA, 8.8% by ZIP3 fallback, 1.3% in ZCTAs outside any CBSA (rural), 1.1% unresolved.
6. **Denominators.**
   - Population: [NST-EST2024-ALLDATA](https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/state/totals/NST-EST2024-ALLDATA.csv) (Last-Modified 2024-12-19) and cbsa-est2024-alldata (2025-03-13). Per-capita = pooled dollars ÷ 2 ÷ mean of July 2023 and July 2024 population.
   - 501(c)(3) count: EO BMF rows with `SUBSECTION` 03 by `STATE` (1,659,404 in the 50 states, DC and PR) and by ZIP5 → CBSA with the same ZIP rules (92% resolve to a CBSA). This count **includes private foundations and group-ruling subordinates with their own EIN**, and is a 2026-11 snapshot.
7. **Scopes.** All top-50 itemising; all excluding university/hospital sponsors (main scope, as in P-NEW-RCP-01); the same excluding SVCF; and each DAFRC segment. A `daf_weighted` amount (each sponsor-year's lines × its DAF share of grants from `sponsor-cost-structure.csv`, capped at 1) is given alongside.
8. **Own-state share** (CF local share) = a sponsor's net dollars to recipients in its own state ÷ its net dollars to US-located recipients. The sponsor's home is its EO BMF `STATE`/`ZIP` (filer header address for The Ayco Charitable Foundation, which is not in the BMF). **Own-metro share** = dollars to the sponsor's home CBSA ÷ CBSA-resolved dollars.
9. **Sensitivity.** Every state row also gives `amount_bmf_state_basis_usd`: the same dollars re-keyed to the recipient's EO BMF state wherever the EIN is in the BMF.

## 2. Results

### 2.1 State shares and per-capita dollars, FY2023–24 pooled [C]
Main scope (excluding university/hospital sponsors). "Per capita" and "per 501(c)(3)" are per year.

| State | $m | Share of US dollars | Per capita ($) | Rank per capita | Per 501(c)(3) ($) | 501(c)(3)s per 10k residents | BMF-state basis $m | Top recipient ($m) |
|---|---|---|---|---|---|---|---|---|
| CA | 15,401 | 20.0% | 196 | 6 | 42,937 | 45 | 15,364 | Navigation Charitable Fund (1,309) |
| NY | 10,516 | 13.6% | 266 | 4 | 48,904 | 54 | 10,925 | Blue Meridian Partners (363) |
| DC | 4,933 | 6.4% | 3,550 | 1 | 224,525 | 156 | 4,824 | New Venture Fund (429) |
| MA | 4,612 | 6.0% | 325 | 2 | 61,384 | 53 | 4,461 | Harvard (441) |
| MD | 3,648 | 4.7% | 292 | 3 | 48,521 | 60 | 3,500 | Johns Hopkins (2,609) |
| TX | 3,121 | 4.0% | 50 | 38 | 11,585 | 43 | 3,348 | UT Austin (55) |
| IL | 2,863 | 3.7% | 113 | 16 | 24,250 | 46 | 2,773 | Obama Foundation (122) |
| FL | 2,359 | 3.1% | 51 | 37 | 11,325 | 45 | 2,402 | Campus Crusade for Christ (96) |
| NC | 2,240 | 2.9% | 102 | 19 | 21,449 | 47 | 2,074 | Duke (160) |
| VA | 1,918 | 2.5% | 109 | 17 | 20,988 | 52 | 2,103 | Nature Conservancy (131) |
| CO | 1,900 | 2.5% | 160 | 7 | 30,345 | 53 | 2,128 | World Literature Crusade (90) |
| … | | | | | | | | |
| MS | 146 | 0.2% | 25 | 51 | 5,630 | 44 | 142 | Hope Enterprise Corp (36) |
| WV | 88 | 0.1% | 25 | 50 | 4,780 | 52 | 92 | Coalfield Development (11) |
| **US** | **77,128** | 100% | **113** | — | **23,240** | 49 | | |

All 50 states, DC, PR and the territories are in the CSV.
- **Per capita vs nonprofit density.** Per-capita dollars vary 13-fold across the 50 states (MA $325 vs MS $25; 143-fold including DC); the count of 501(c)(3)s per resident varies far less (about 33–89 per 10k outside DC and PR). The differences are therefore in dollars per organisation ($4,780 to $61,384 outside DC and PR), not in how many organisations exist [C].
- **Year split.** CA fell from $8.63bn (FY2023) to $6.77bn (FY2024) as SVCF's one-off CZ lines dropped out; NY rose from $4.46bn to $6.05bn and DC from $2.11bn to $2.82bn [C].
- **DAF-weighted basis** moves no main-scope state share by more than 0.25 pt (all-sponsor scope: CA 20.7% filed vs 19.8% weighted) [C].

### 2.2 Concentration [C]

| Scope | Top-5 states | Top-10 states | State HHI | Top-10 CBSAs | CBSA HHI | Top-5 states' population share |
|---|---|---|---|---|---|---|
| All ex university/hospital | 50.7% | 66.9% | 783 | 58.1% | 525 | 21.4% |
| … ex SVCF | 47.8% | 64.8% | 669 | 55.6% | 481 | 21.4% |
| National sponsors | 51.2% | 67.3% | 721 | 58.7% | 523 | 21.4% |
| Community foundations | 60.6% | 75.7% | 1,622 | 65.8% | 979 | 24.4% |
| … ex SVCF | 45.4% | 66.6% | 667 | 55.0% | 392 | 24.4% |
| Single-issue | 44.4% | 63.7% | 597 | 54.1% | 536 | 29.9% |

- Grant dollars are far more concentrated geographically than population: the top five states hold about a fifth of residents but half the dollars.
- With SVCF in, community-foundation dollars are the most concentrated (CA 37.4%). Without SVCF they are slightly *less* concentrated than national-sponsor dollars, because 21 CFs spread across 18 home states.

**Largest CBSAs (main scope):**

| CBSA | $bn | Share of CBSA-resolved | Per capita ($/yr) | Top recipient |
|---|---|---|---|---|
| New York–Newark–Jersey City | 10.80 | 14.3% | 272 | Blue Meridian Partners |
| San Francisco–Oakland–Fremont | 8.46 | 11.2% | 913 | Navigation Charitable Fund |
| Washington–Arlington–Alexandria | 6.62 | 8.8% | 518 | New Venture Fund |
| Boston–Cambridge–Newton | 4.12 | 5.5% | 413 | Harvard |
| Los Angeles–Long Beach–Anaheim | 3.31 | 4.4% | 128 | Caltech |
| Baltimore–Columbia–Towson | 3.21 | 4.3% | 563 | Johns Hopkins |
| Chicago–Naperville–Elgin | 2.69 | 3.6% | 143 | Obama Foundation |
| San Jose–Sunnyvale–Santa Clara | 1.86 | 2.5% | 469 | Stanford |
| Atlanta–Sandy Springs–Roswell | 1.39 | 1.8% | 109 | Boys & Girls Clubs of America |
| Seattle–Tacoma–Bellevue | 1.28 | 1.7% | 156 | UW Foundation |

Per-capita figures for all 917 CBSAs are in the CSV (`geo_type = cbsa`).

### 2.3 National sponsors vs community foundations: local share [C]

| Segment | Sponsors | Pooled own-state share | Median own-state | Range | Median own-metro | Pooled share to DC/NY/MA/CA (outside home state) |
|---|---|---|---|---|---|---|
| Community foundations | 22 | **60.0%** | **71.2%** | 20.0–91.7% | 63.3% | 18.6% |
| … ex SVCF | 21 | 54.2% | 72.2% | 20.0–91.7% | 64.1% | 20.7% |
| National sponsors | 16 | **7.6%** | **4.6%** | 0.5–26.4% | 3.3% | 39.3% |
| Single-issue | 7 | 26.0% | 36.2% | 12.9–54.1% | 40.8% | 16.2% |

**Community foundations (own state / own metro, % of US-located dollars):**

| Sponsor | State | US $m | Own state | Own metro | Largest other state |
|---|---|---|---|---|---|
| Silicon Valley CF | CA | 5,970 | 69.3 | 4.4 | NY |
| Chicago Community Trust | IL | 2,832 | **20.0** | 20.3 | CA |
| Foundation for the Carolinas | NC | 1,111 | 53.8 | 33.9 | DC |
| California CF | CA | 572 | 74.2 | 58.7 | NY |
| Columbus Foundation | OH | 500 | 74.3 | 70.0 | NY |
| Greater Houston CF | TX | 382 | 62.8 | 44.9 | NY |
| New York Community Trust | NY | 376 | 65.5 | 64.8 | CT |
| Oregon CF | OR | 355 | 90.1 | 53.9 | CA |
| Greater Kansas City CF | MO | 342 | 35.9 | 47.6 | KS |
| San Francisco Foundation | CA | 335 | 79.0 | 62.6 | DC |
| Boston Foundation | MA | 325 | 72.2 | 69.6 | NY |
| Tulsa CF | OK | 321 | 66.7 | 64.1 | MO |
| Seattle Foundation | WA | 295 | 65.8 | 58.5 | CA |
| CF for Greater Atlanta | GA | 292 | 70.2 | 68.1 | FL |
| Saint Paul & Minnesota Foundation | MN | 283 | 89.3 | 83.9 | FL |
| Marin CF | CA | 277 | 61.3 | 46.5 | NY |
| Denver Foundation | CO | 230 | 80.2 | 71.0 | CA |
| Community Foundation (Middle Tennessee) | TN | 225 | 85.0 | 85.4 | CO |
| San Diego Foundation | CA | 217 | **91.7** | 84.3 | NY |
| Minneapolis Foundation | MN | 171 | 74.8 | 72.9 | NY |
| CF of New Jersey | NJ | 151 | 38.6 | 47.8 | NY |
| CF of Tampa Bay | FL | 57 | 80.7 | 73.5 | DC |

- **Typical CF: about 70% in-state and 60–70% in-metro.** Even so, the median CF reaches 49 states and territories.
- **Outliers among CFs:**
  - The Chicago Community Trust (20% in Illinois; 37% to DC/NY/MA/CA, CA largest: e.g. Tides Foundation $26m, Climate Imperative $20m) behaves like a national sponsor. This is consistent with a DAF book of mobile, national donors [I].
  - SVCF is 69% in California but only 4.4% in its own San Jose CBSA, because its largest lines go to San Mateo County (SF–Oakland CBSA) entities.
  - Cross-border metros lower the own-state share without lowering own-metro share: Kansas City (MO/KS) and New Jersey (NYC metro).
- **National sponsors:** 2–10% in their home state, except GS DAPF (NY, 22%), T. Rowe Price (MD, 26%) and Ayco (NY, 16%). These look like donor-base clustering near the sponsor, not a local mandate [I]. Own-metro figures for national sponsors depend on a BMF mailing address and mean little (e.g. Morgan Stanley GIFT's BMF address is in Westfield, NY).

### 2.4 Outliers: DC, NY, CA, MA (and MD) [C/F]

| State | $bn | From sponsors HQ'd elsewhere | Share to recipients with ≥10 top-50 sponsors | Top-5 recipient share | Largest recipients ($m, number of sponsors) |
|---|---|---|---|---|---|
| DC | 4.93 | **100%** | 54% | 22% | New Venture Fund 429 (21); The 85 Fund 312 (5); Hopewell Fund 132 (20); Our American Future Fdn 119 (18); 50CAN 94 (10); World Central Kitchen 92 (42) |
| NY | 10.52 | 77% | 50% | 11% | Blue Meridian Partners 363 (3); Memorial Sloan Kettering 264 (24); Rockefeller Philanthropy Advisors 246 (21); MSF USA 166 (22); UJA-Federation 161 (25); Columbia 130 (33) |
| CA | 15.40 | 65% | 33% | 22% | Navigation Charitable Fund 1,309 (1, SVCF); Stanford 626 (42); CZ Institute for Advanced Biological Imaging 586 (1); CZ Biohub SF 576 (1); CZ Biohub NY 248 (1, CA address); Climate Imperative 247 (4) |
| MA | 4.61 | 50% | 53% | 20% | Harvard 441 (41); MIT 188 (31); Mass General Brigham 106 (24); Broad Institute 95 (10); Grantham Environmental Trust 84 (2); Dana-Farber 72 (31) |

- **DC** ($3,550 per resident; 156 501(c)(3)s per 10k residents, three times the US level) is almost entirely a headquarters effect.
  - National advocacy, policy and fiscal-sponsor intermediaries dominate. The DC-registered fiscal sponsors New Venture Fund and Hopewell Fund alone take 11%.
  - The money is then re-granted or spent nationally [I].
  - Its sector mix is public-society benefit 22.7%, environment 19.1%, human services 18.5% and international 10.8%.
- **NY:**
  - 13.8% of NY dollars go to NTEE-international recipients (MSF USA and others) that spend abroad.
  - Fiscal sponsors and intermediaries (Rockefeller Philanthropy Advisors, Blue Meridian) re-grant nationally.
  - On the BMF-state basis NY gains $0.41bn, because several national charities use out-of-state remittance addresses.
- **CA:**
  - Excluding SVCF, CA falls from $196 to $143 per capita (rank 6 → 8) and from 20.0% to 15.8% of dollars.
  - SVCF's FY2023 CZ LLC and Navigation lines make up most of the drop.
- **MA:** concentrated in universities and academic medicine (education 37.4%, health 16.3%). Massachusetts-headquartered sponsors (chiefly Fidelity Charitable, Boston) supply half of the dollars.
- **MD** ranks 3rd per capita only because of Johns Hopkins ($2.61bn from 32 sponsors; 72% of Maryland's dollars).

### 2.5 Address-source checks [C]
- **Schedule I vs BMF state.** Where both exist, the Schedule I state equals the recipient's BMF state for **94.4%** of $73.27bn EIN-matched dollars.
  - Much of the remaining 5.6% is **remittance or lockbox addresses**. Cornell, the Red Cross and others use ZIP 50037 Boone, IA; national sponsors as recipients use Cincinnati/Covington lockboxes, among others.
- **State effect of the BMF-state basis:**
  - **IA $644m → $231m**: Cornell's $194m is the largest IA "recipient".
  - NY +$409m; CO +$228m; TX +$226m; VA +$184m.
  - NC −$166m; MA −$152m; MD −$148m; DC −$109m.
  - Top-state ranks do not change.
- **Recency of the BMF address.** The BMF is a 2026-11 snapshot. A recipient that moved after the grant is placed at its current address in the sensitivity column only.

## 3. Limitations
- **Foreign grants are excluded.** Schedule I Part II covers domestic organisations. Grants to foreign organisations and individuals are on **Schedule F**, which was not parsed (foreign-address Part II lines total $0.3m). International work therefore appears only through US intermediaries, located at their US office (e.g. MSF USA in NY, World Central Kitchen in DC). See P-B42N21-03.
- **Headquarters-address bias.** Grants are located where the recipient's legal or remittance address is, not where the money is spent. National charities, fiscal sponsors (New Venture Fund, Hopewell, Tides, Rockefeller Philanthropy Advisors), federated campaigns and university systems concentrate dollars in DC, NY, MA, CA and MD. Per-capita figures for those places measure where intermediaries are based, not local benefit [I].
- **Lockbox addresses** move dollars to processing locations (IA, OH, KY, FL). The BMF-state column bounds this at the state level; the metro level uses Schedule I ZIPs only. See P-B42N21-01.
- **Itemisation thresholds.** Schedule I lists grants over $5,000 per recipient. Small local grants, which are probably more local [I], are under-represented. P-NEW-RCP-01 found the Schedule I total ≈ 98% of Part IX line 1 for this universe.
- **Mixed DAF and non-DAF grants.** Community-foundation Schedule I lines mix DAF and discretionary grants; the `daf_weighted` column is an approximation, not a line-level split. Own-state shares for CFs therefore describe the whole grant book.
- **Sponsor home** is the EO BMF address (filer header for Ayco), which can be a mailing address (Morgan Stanley GIFT → Westfield, NY). Own-metro shares for national sponsors are not meaningful.
- **Denominators.** BMF 501(c)(3) counts include private foundations, group subordinates with their own EIN and dormant organisations, and come from a 2026 snapshot rather than the grant years. Population is Census Vintage 2024. Pooled dollars ÷ 2 understate per-year amounts slightly for the few sponsors with one itemised year (Greater Horizons, Greater Kansas City CF).
- **Metro geocoding.** The ZCTA-to-county assignment uses largest land overlap, not population. The ZIP3 fallback (8.8% of dollars) and the Connecticut table are approximations. 1.1% of dollars do not resolve.
- **Universe.** Top-50 DAFRC sponsors only. The 22 community foundations are the largest and most DAF-heavy; smaller CFs may be more local (P-B42N21-02).

## 4. Data dictionary

**`daf-grant-geography-state-2023-2024.csv`** (one row per scope × geography)

| Column | Meaning |
|---|---|
| scope | `all_top50_itemising`, `all_ex_university_hospital` (main), `all_ex_uh_ex_svcf`, `national`, `processor`, `community_foundation`, `community_foundation_ex_svcf`, `single_issue`, `university_hospital` (state rows); CBSA rows for `all_ex_university_hospital`, `all_ex_uh_ex_svcf`, `national`, `community_foundation` |
| geo_type, geo_code, geo_name | `state` (USPS code; also `FOREIGN_PART_II`, `UNKNOWN`, territory/military codes) or `cbsa` (2023 CBSA code and Census name) |
| fiscal_years | `2023-2024` (DAFRC FY convention; pooled) |
| amount_usd, share_of_net, share_of_us_located | Net (non-DAF-to-DAF) Schedule I dollars (cash + non-cash); share of the scope's net total; share of dollars located in the 50 states + DC + PR (state rows) or of CBSA-resolved dollars (CBSA rows) |
| amount_fy2023_usd, amount_fy2024_usd | The same by fiscal year |
| amount_daf_weighted_usd, share_daf_weighted | Each sponsor-year's lines × DAF share of grants (`sponsor-cost-structure.csv`, capped at 1) |
| rank_by_amount, rank_per_capita | Rank among geographies with a population denominator |
| lines, recipients, sponsors | Schedule I lines; distinct recipient keys (EIN, else normalised name); distinct sponsors |
| pop_2023, pop_2024 | Census Vintage 2024 July 1 estimates |
| usd_per_capita_per_year | amount_usd ÷ 2 ÷ mean(pop_2023, pop_2024) |
| c3_orgs_bmf, usd_per_c3_per_year, c3_per_10k_pop | EO BMF SUBSECTION 03 count (2026-11) by state or ZIP→CBSA; dollars per organisation per year; organisations per 10,000 residents (2024) |
| state_from_sched_i_usd, state_from_bmf_usd | Dollars whose state came from the Schedule I address vs the BMF fallback |
| amount_bmf_state_basis_usd | State rows: dollars re-keyed to the recipient's EO BMF state where the EIN is in the BMF (sensitivity for remittance/HQ addresses) |
| cbsa_via_zip3_fallback_usd | CBSA rows: dollars placed by the ZIP3 rule (non-ZCTA ZIPs) |
| top_recipient, top_recipient_usd, top5_recipient_share | Largest recipient (BMF name, else Schedule I name), its dollars, and the top-5 recipients' share of the geography |
| source | Provenance string |

**`daf-grant-geography-cf-local-share.csv`** (one row per itemising top-50 sponsor; all segments, for contrast)

| Column | Meaning |
|---|---|
| sponsor_ein, sponsor_name, segment, sponsor_rank_fy2024 | DAFRC panel identity, segment (`mission_net_payout.segment_of`) and FY2024 DAF-asset rank |
| sponsor_state, sponsor_home_source, sponsor_cbsa, sponsor_cbsa_name | Home state/CBSA from EO BMF STATE/ZIP (`bmf`), or the return's Filer address (`filer_header`) |
| fiscal_years | Itemised FYs included |
| net_usd, d2d_excluded_usd | Net Schedule I dollars; DAF-to-DAF dollars removed |
| us_located_usd, foreign_part_ii_usd, unknown_state_usd | Split of net dollars by location status (US includes territories) |
| own_state_usd, own_state_share | Dollars to recipients in the sponsor's state; share of US-located dollars (**the CF local share**) |
| cbsa_resolved_usd, own_cbsa_usd, own_cbsa_share_of_resolved | CBSA-resolved US dollars; dollars to the sponsor's home CBSA; share |
| states_reached | Distinct state/territory codes receiving dollars |
| top_other_state, top_other_state_usd | Largest state outside the home state |
| dc_ny_ma_ca_out_of_state_share | Share of US dollars going to DC, NY, MA or CA, excluding the home state |
| recipients, source | Distinct recipients; provenance |

## 5. Sources

| # | Source | Version / date | robots.txt |
|---|---|---|---|
| S1 | IRS Form 990 Schedule I Part II, e-file XML (GivingTuesday mirror of IRS TEOS), 94 returns; line cache from `mission_recipient_sectors.py` | as in P-NEW-RCP-01 | gt990datalake-rawdata.s3.amazonaws.com → 404 (no rules) |
| S2 | [IRS EO BMF](https://www.irs.gov/pub/irs-soi/eo1.csv) eo1–eo4, eo_pr, eo_xx | Last-Modified 2026-11-09 (scratch copy from P-NEW-RCP-01) | www.irs.gov `/pub/` not disallowed |
| S3 | [Census NST-EST2024-ALLDATA](https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/state/totals/NST-EST2024-ALLDATA.csv) | Last-Modified 2024-12-19, 41,378 bytes | www2.census.gov: no `*` rules |
| S4 | [Census cbsa-est2024-alldata](https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/metro/totals/cbsa-est2024-alldata.csv) | Last-Modified 2025-03-13, 718,043 bytes | same |
| S5 | [Census 2020 ZCTA520–county relationship](https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt) | Last-Modified 2021-12-09, 6,821,287 bytes | same |
| S6 | Repo: `daf-to-daf-recipient-whitelist.csv`, `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `sponsor-cost-structure.csv`, `netpayout990/` cache | repo | n/a |

## 6. Reproduction
```
python3 scripts/mission_grant_geography.py --np-cache NPCACHE --bmf-dir BMF --lines-cache LINES \
    --census-dir CENSUS --zip-cache ZIPS [--xml-list XMLPATHS] [--fetch]
```
- `NPCACHE`, `BMF` and `LINES` are those of `mission_recipient_sectors.py`.
- `CENSUS` holds the three Census files of S3–S5.
- `ZIPS` caches each return's verified ZIP/city list and filer address, one JSON per object id.
- `--xml-list` is an optional list of local XML copies; `--fetch` streams any other return from the mirror.
- The script writes both CSVs and prints a JSON summary (coverage, address checks, scope concentration, per-capita rankings, outlier detail, local-share statistics). Every figure above comes from that summary or the CSVs.
- Run time is about 65 s.
