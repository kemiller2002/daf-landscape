# Direction P-NEW-FGN-01: foreign grants of the top-50 DAF sponsors (Form 990 Schedule F), FY2023–FY2024

**Date:** 2026-11-15 · **Queue item:** P-NEW-FGN-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/daf-foreign-grants-schedule-f-2023-2024.csv`](../../data/mission-2026-11-14/daf-foreign-grants-schedule-f-2023-2024.csv): 3,199 rows in long format, keyed by `row_type`:
  - 100 sponsor-year rows;
  - 24 scope totals;
  - region (Schedule F Parts I–III), purpose bucket and purpose text, manner of disbursement, Part III assistance type, and Part I activity rows, each by scope × FY;
  - 27 intermediary rows.
- [`data/mission-2026-11-14/queue-proposals-batch45-n31.csv`](../../data/mission-2026-11-14/queue-proposals-batch45-n31.csv): P-B45N31-01..03.
- **Script:** [`scripts/mission_foreign_grants.py`](../../scripts/mission_foreign_grants.py) (stdlib, functional style). It reuses the universe and DAF-to-DAF logic of `mission_recipient_sectors.py`.

**Rules applied**
- **Governing corrections read first:**
  - [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md) with its wave-24A corrections: the ImpactAssets DAFRC row is already replaced, and SVCF drives the community-foundation DAF-to-DAF share.
  - [direction-grant-geography.md](direction-grant-geography.md) with its wave-27 corrections (population-base wording; reproduction note).
  - [direction-international-comparison.md](direction-international-comparison.md) with its wave-24A corrections (UK Gift Aid transition dates; Australian fund counts).
  - None of these changes the Schedule I lines used here. SVCF is shown as a separate `ex_svcf` scope, as in the geography direction.
- **Recency (TY2021+):**
  - The returns are the DAFRC FY2023–FY2024 returns (fiscal year = calendar year in which the tax period ends; tax periods ending 2023-03-31 to 2024-12-31). This is the same window as P-NEW-RCP-01 and P-NEW-GEO-01, so "TY2023–2024" in the brief is read as FY2023–FY2024 in the repo's convention.
  - The intermediaries' own returns cover tax periods ending in 2023 and 2024.
  - IRS EO BMF: 2026-11 snapshot.
- **robots.txt read before fetching:**
  - `gt990datalake-rawdata.s3.amazonaws.com/robots.txt` returned 404 (no rules).
  - `www.irs.gov/robots.txt` was read. Nothing was fetched from irs.gov: the BMF and the TEOS index CSVs were reused from earlier scratch copies.
  - No outreach.
- **Evidence tags:** [F] filed figure, [C] computed here, [I] inference.

## 0. Headline answers

Main scope: top-50 sponsors excluding the two university/hospital sponsors (Stanford, UCLA Foundation), as in P-NEW-RCP-01. FY2023–24 pooled, 96 sponsor-years.

| Question | Answer |
|---|---|
| **Total foreign grants and share** | **$1.891bn of $98.27bn total grants = 1.92%** (Form 990 Part IX line 3 ÷ lines 1–3) [F/C].<br>- By year: FY2023 $845.0m (1.86%); FY2024 $1,045.8m (1.98%), +24%.<br>- All 50 sponsors (100 sponsor-years): $1.917bn of $100.65bn (1.90%).<br>- DAF-weighted (sponsor-year × DAF share of grants): $1.837bn of $93.77bn (1.96%).<br>- Without SVCF: 1.71% [C].<br>- 68 of 96 sponsor-years reported any foreign grants; 77 filed Schedule F [F]. |
| **Concentration** | **One sponsor accounts for 39%.**<br>- National Philanthropic Trust: $742.8m (7.4% of its grants).<br>- SVCF: $352.4m (4.2%).<br>- GS DAF Philanthropy Fund: $179.8m (3.4%).<br>- These top 3 hold **67.4%**; the top 10 hold 96.1%.<br>- Fidelity Charitable: $114.2m, 0.50% of its $23.0bn of grants. DAFgiving360: 0.93%. Vanguard Charitable: 0.21% [C]. |
| **By sponsor type** | - National: 1.75% ($1,213.7m).<br>- Community foundation: **2.60%** ($510.2m; SVCF is 69% of it).<br>- Single-issue: 1.98% ($166.9m; Jewish Communal Fund and Jewish Community Foundation of LA: 18.6% of its grants).<br>- Processor (Dechomai): 0.<br>- University/hospital: 1.08% [C]. |
| **By region** (Schedule F Part II, $1.891bn) | - **Europe 49.6%**;<br>- Middle East and North Africa 12.4%;<br>- South America 8.8%;<br>- South Asia 7.9%;<br>- North America (Canada/Mexico) 6.5%;<br>- Sub-Saharan Africa 6.1%;<br>- East Asia and the Pacific 5.9%;<br>- "Latin America" (unspecified) 1.7%;<br>- Central America and the Caribbean 0.9%;<br>- Russia and the Newly Independent States 0.3% [C].<br><br>NPT supplies 35% of the Europe dollars, SVCF 26%. Single-issue sponsors are 79% Middle East and North Africa. |
| **Purposes** | Free text, usually generic; shares are dollars by the keyword bucket of the *reported* text, not donor restrictions or uses (P-B40N13-01).<br>- Generic text (\<br>- Environment and animals 13.7%; education 11.4%; arts and culture 10.1%; human services and civic 8.7%; health 6.7%.<br>- Development and poverty 2.9%; research 1.8%; religion 0.5%.<br>- Relief/humanitarian **0.05%**, by keyword [C]. |
| **Manner of disbursement** | Wire 77.1%, ACH/EFT 18.9%, check 3.7% of Part II dollars [C]. |
| **Equivalency determination (ED) vs expenditure responsibility (ER)** | **Part V narratives:** of the 70 sponsor-years with foreign grants, 41 describe ED and/or ER (31 ED, 27 ER). Together they hold 94.7% of the foreign dollars [C].<br><br>**Part II line 2 recipient counts:** 2,543 recipients are in the "501(c)(3)" column (an IRS determination, or an ED / equivalency letter) and **672 are "other organisations"**, which typically need ER [F/I].<br>- SVCF has 539 of the 672.<br>- National sponsors report 1,600 vs 5. |
| **US-intermediary route** (Schedule I) | **Nine named cross-border intermediaries received $215.6m gross** from top-50 sponsors over FY2023–24.<br>- CAF America $58.6m from 30 sponsors; this is a whitelisted DAF-to-DAF flow.<br>- Myriad USA (formerly KBFUS) $46.5m; GlobalGiving $33.0m; Global Greengrants $27.9m; Global Fund for Women $17.2m; Give2Asia $12.0m; Global Fund for Children $11.2m; and others.<br><br>Applying each intermediary's own foreign-grant share gives **≈$165m passed abroad**, about **8.7% on top of** the $1.891bn direct route [C/I].<br><br>Two wider routes go through US recipients:<br>- "American/US friends of" names: $432.9m (Friends of the IDF $54.5m, AF Tel Aviv University $40.7m, AF Winchester College $40.0m);<br>- all NTEE Q (international) recipients: $4.32bn [C]. |
| **Compared with the NTEE sector analysis** | P-NEW-RCP-01 put "international" (NTEE Q recipients) at **5.6% of net Schedule I** ($4.32bn of $77.34bn).<br>- Direct foreign grants add **2.4% of net Schedule I + line 3**, so international (NTEE Q + direct) is **7.8%**.<br>- Adding friends-of and named intermediaries outside Q gives 8.1% [C].<br>- **International is therefore understated by about 2.2–2.5 points in the Schedule-I-only sector shares.**<br>- Some NTEE Q recipients spend in the US (e.g. international-affairs groups), so 7.8% is an upper-leaning combination, not a measure of money leaving the US [I]. |

## 1. Method

1. **Universe.** Exactly that of [`mission_recipient_sectors.py`](../../scripts/mission_recipient_sectors.py):
   - top-50 DAFRC sponsors by FY2024 DAF assets;
   - one return per sponsor × FY via `mission_daf_to_daf.pick_returns` over the `netpayout990/` cache;
   - all **100** sponsor-years. Schedule F is filed independently of Schedule I, so the six attachment-only Schedule I sponsor-years are kept (BofA CGF and Renaissance in both years; Greater Horizons and Greater Kansas City CF in FY2023).
2. **Extraction (streamed).** For each return the script reads the IRS e-file XML:
   - `ReturnHeader`;
   - Form 990 Part IX lines 1–3 (`GrantsToDomesticOrgsGrp`, `GrantsToDomesticIndividualsGrp`, `ForeignGrantsGrp`);
   - Part IV lines 14a, 14b, 15 and 16;
   - all of Schedule F:
     - Part I `AccountActivitiesOutsideUSGrp`, plus the line 1 grant-records indicator;
     - Part II `GrantsToOrgOutsideUSGrp` (region, purpose, cash, manner, non-cash), plus line 2 `Total501c3OrgCnt` / `TotalOtherOrgCnt`;
     - Part III `ForeignIndividualsGrantsGrp`;
     - Part IV, the six foreign-entity questions;
     - Part V `SupplementalInformationDetail`.
   - Parsing stops at the first schedule after F, so Schedule I is not re-downloaded.
   - **Sources:** 67 returns came from local XML copies already in scratch; 33 were streamed from the GivingTuesday mirror of IRS TEOS (`…/EfileData/XmlFiles/{OBJECT_ID}_public.xml`).
   - **Checks:** all 100 parsed, and every filer EIN matches the sponsor.
3. **Totals.**
   - "Foreign grants" means Part IX line 3. Its denominator is Part IX lines 1–3 (all grants, gross of DAF-to-DAF).
   - Schedule F Part II + Part III equal line 3 to within $0.5m or 5% in 99 of 100 sponsor-years. The exception is Morgan Stanley GIF FY2024: Part II $17.9m vs line 3 $16.7m.
   - Raymond James FY2024 reports $200 on line 3 and no Schedule F.
4. **Normalisation.**
   - **Region:** the 10 Schedule F regions. Filer variants are mapped by region-name patterns applied before any " - country list"; for example "South Asia - Afghanistan, …, India" becomes South Asia, and "NORTH AMERICA - CANADA AND MEXICO" becomes North America. Then single-country texts are mapped by a fixed table. "Latin America", "Africa" and "Asia" without a sub-region are kept as `(unspecified)`.
   - **Manner:** wire / ACH-EFT-transfer / check / not stated / other.
   - **Purpose:** keyword buckets, first match wins (order in `PURPOSE_RULES`). The raw text is kept in `purpose_text_part2` (top 25 per scope).
   - **Column-shift repair:** NPT's FY2024 Part II has purpose in the manner field and manner in the valuation field. The script detects this (blank purpose, a non-method manner, a method-like valuation) and shifts it back. This affected $410.3m of lines, all NPT FY2024.
5. **Part V flags** (regex on the narrative):
   - ED: "equivalency determination" or Treas. Reg. 53.4945-5(a)(5);
   - ER: "expenditure responsibility" or 4945(h);
   - NGOsource;
   - a named intermediary.
6. **Schedule I routes.** The full Schedule I Part II lines come from the P-NEW-RCP-01 line cache. They are annotated with `mission_recipient_sectors.annotate` (same DAF-to-DAF exclusion and NTEE join), so the net total ($77,343,717,758) equals P-NEW-RCP-01's exactly. Three routes are measured:
   - **(a) Named intermediaries** (fixed EIN list taken from the IRS EO BMF):
     - CAF America 43-1634280;
     - GlobalGiving 30-0108263;
     - Give2Asia 94-3373670;
     - Myriad USA (formerly King Baudouin Foundation US) 58-2277856;
     - Global Fund for Children 56-1834887;
     - Friends of Fondation de France 13-3966503;
     - British Schools and Universities Foundation 13-6161189;
     - Global Fund for Women 77-0155782;
     - Global Greengrants Fund 84-1612422.
     - These are counted gross, because CAF America is a whitelisted DAF-to-DAF recipient (batch 34) and so drops out of net Schedule I.
   - **(b) Friends-of names:** an "American/US friends of" pattern, plus "American Committee/Associates for/of the", plus "Friends of … Israel/Jerusalem/…" (regex `FRIENDS`).
   - **(c) NTEE Q:** recipients whose EO BMF NTEE code begins with Q.
   - `sched_i_intl_union_net_usd` is the union of (a)–(c) on net lines.
7. **Pass-through.**
   - Each named intermediary's own Form 990 for tax periods ending in 2023 and 2024 is located in the IRS TEOS index CSVs (`index_2023`–`index_2026`; latest e-file per period) and parsed the same way. All 18 returns parsed.
   - foreign share = its line 3 ÷ lines 1–3; estimated pass-through = inbound top-50 dollars × that share.
   - This is a proportional assumption [I]. It ignores timing: Global Fund for Children's FY2023 inbound ($10.8m) exceeds its FY2023 grants ($5.6m).
8. **Scopes.** All top-50; all excluding university/hospital (main); the same excluding SVCF; each DAFRC segment; each sponsor. FY2023, FY2024 and pooled.
9. **DAF weighting.** Each sponsor-year's dollars × its DAF share of grants (`sponsor-cost-structure.csv`, capped at 1), as in P-NEW-RCP-01.

## 2. Coverage and checks [F/C]

- 100 of 100 sponsor-years extracted, with no fetch failures and no filer-EIN mismatches.
- **990 Part IV:**
  - line 14b (foreign activities > $10k): yes in 79;
  - line 15 (> $5k to a foreign organisation): yes in 70;
  - line 16 (> $5k to foreign individuals): yes in 5;
  - foreign office (14a): yes in 10.
- 12 sponsor-years file Schedule F with line 3 = 0, and in every one of them Part I shows investment rows only. They include NCF FY2024, Oregon CF, Servant Foundation, Thrivent, Saint Paul & Minnesota, and UCLA Foundation.
- **Schedule F Part I is mostly investments.** Part I region totals across the main scope are $29.17bn, of which **93.5% is rows whose activity is "Investments"** (offshore funds held in the Cayman Islands and similar). Only $1.888bn is grantmaking, which matches line 3.
  - Part I region totals therefore **must not be read as foreign grants**. The CSV keeps grantmaking Part I rows separately (`region_part1_grantmaking`).
  - Schedule F Part IV answers reflect the same investment exposure: transfers to a foreign corporation yes in 67 of 81 Schedule F filers, foreign partnership 63, PFIC 56.
- **Part III (foreign individuals)** is negligible:
  - main scope $0.13m (Minneapolis Foundation hardship assistance and scholarships, Marin $10k);
  - Stanford (university/hospital) $2.6m to 286 individuals.
- **Grant-records indicator (Part I line 1) answered "No":** American Endowment Foundation (both years; $0.15m and $0.01m foreign), DonorsTrust (both years), Seattle Foundation FY2024.

## 3. Results

### 3.1 Totals by scope, FY2023–24 pooled [F/C]

| Scope | Sponsor-years (with foreign grants) | Foreign grants (line 3) | Total grants (lines 1–3) | Foreign share | NTEE Q share of net Sched I + L3 | Q + direct foreign share | Broad (Q ∪ friends ∪ named) + direct |
|---|---|---|---|---|---|---|---|
| All excl. university/hospital | 96 (68) | $1,890.8m | $98,265.4m | **1.92%** | 5.45% | **7.83%** | 8.14% |
| … excl. SVCF | 94 (66) | $1,538.4m | $89,857.6m | 1.71% | 5.53% | 7.64% | 7.97% |
| National | 36 (25) | $1,213.7m | $69,343.8m | 1.75% | 5.34% | 7.53% | 7.81% |
| Community foundation | 44 (33) | $510.2m | $19,608.3m | 2.60% | 4.30% | 7.46% | 7.74% |
| Single-issue | 14 (10) | $166.9m | $8,423.4m | 1.98% | 8.71% | 10.88% | 11.41% |
| Processor | 2 (0) | $0 | $889.8m | 0% | 0% | 0% | 0% |
| University/hospital | 4 (2) | $25.8m | $2,389.4m | 1.08% | 0.26% | 2.66% | — |
| All top-50 | 100 (70) | $1,916.6m | $100,654.8m | 1.90% | 5.38% | — | 8.08% |

The three right-hand columns use only itemising sponsor-years, on the base of net Schedule I + line 3, which matches P-NEW-RCP-01's base.

**By year (main scope):**
- FY2023: $845.0m of $45.32bn (1.86%).
- FY2024: $1,045.8m of $52.94bn (1.98%).
- By segment, FY2023 → FY2024: national 1.74% → 1.76%; community foundations 2.25% → 3.01%; single-issue 1.95% → 2.01% [C].

### 3.2 Largest foreign grantmakers, FY2023–24 pooled (main scope) [F/C]

| Rank (FY2024 DAF assets) | Sponsor (DAFRC name) | Segment | Foreign $m | % of own grants | % of scope foreign $ |
|---|---|---|---|---|---|
| 2 | National Philanthropic Trust | national | 742.8 | 7.42% | 39.3% |
| 6 | Silicon Valley Community Foundation | CF | 352.4 | 4.19% | 18.6% |
| 5 | GS Donor Advised Philanthropy Fund | national | 179.8 | 3.45% | 9.5% |
| 1 | Fidelity Investments Charitable Gift Fund | national | 114.2 | 0.50% | 6.0% |
| 15 | Jewish Communal Fund | single-issue | 110.5 | 5.71% | 5.8% |
| 3 | Donor Advised Charitable Giving (DAFgiving360) | national | 108.2 | 0.93% | 5.7% |
| 12 | The Chicago Community Trust | CF | 58.2 | 1.91% | 3.1% |
| 34 | Marin Community Foundation | CF | 56.2 | 15.29% | 3.0% |
| 37 | Jewish Community Foundation of LA | single-issue | 49.6 | 18.60% | 2.6% |
| 8 | Morgan Stanley Global Impact Funding Trust | national | 44.3 | 1.56% | 2.3% |
| 4 | Vanguard Charitable | national | 11.0 | 0.21% | 0.6% |

**Notes on the table:**
- **Consistency with the repo's FY2025 figure:** the "big-4" nationals (Fidelity, DAFgiving360, Vanguard, NPT) give **1.96%** here over FY2023–24 ($976.1m). [breadth-community-faith-infrastructure-emerging.md](breadth-community-faith-infrastructure-emerging.md) §6.3 reports 1.46% for FY2025. The fall is mainly NPT ($410.6m in FY2024 vs $310.5m in FY2025 per that file) [C].
- **No foreign grants in either year:** NCF, BofA CGF, Foundation for the Carolinas, Dechomai, the US Charitable Gift Trust, Oregon CF, Servant Foundation, American Gift Fund, the Denver Foundation (FY2023), Community Foundation (rank 40), T. Rowe Price, Thrivent, CF of Tampa Bay, Saint Paul & Minnesota, and UCLA Foundation.
- **Negligible foreign grants:** Renaissance Charitable ($5k and $89k) and American Endowment Foundation ($153k and $10k).

### 3.3 Regions (Schedule F Part II dollars) [C]

| Region | Main scope $m | Share | National | CF | Single-issue | FY2023 share | FY2024 share |
|---|---|---|---|---|---|---|---|
| Europe (incl. Iceland, Greenland) | 938.7 | **49.6%** | 48.0% | 65.3% | 14.1% | 52.8% | 47.1% |
| Middle East and North Africa | 234.2 | 12.4% | 7.4% | 2.5% | **79.0%** | 10.8% | 13.7% |
| South America | 165.6 | 8.8% | 10.9% | 6.0% | 1.5% | 7.1% | 10.1% |
| South Asia | 149.0 | 7.9% | 11.8% | 1.1% | — | 5.8% | 9.6% |
| North America (Canada, Mexico) | 122.5 | 6.5% | 6.1% | 9.3% | 1.0% | 5.3% | 7.4% |
| Sub-Saharan Africa | 115.8 | 6.1% | 7.5% | 3.6% | 4.0% | 8.8% | 3.9% |
| East Asia and the Pacific | 111.4 | 5.9% | 4.7% | 10.5% | 0.2% | 7.8% | 4.3% |
| Latin America (unspecified) | 31.5 | 1.7% | 2.6% | — | — | — | 3.0% |
| Central America and the Caribbean | 16.5 | 0.9% | 0.8% | 1.4% | 0.1% | 1.3% | 0.5% |
| Russia and the Newly Independent States | 5.8 | 0.3% | 0.3% | 0.5% | — | 0.2% | 0.4% |

**Who drives each region:**
- **Europe:** NPT $328.5m, SVCF $241.7m, GS $113.0m, DAFgiving360 $56.3m, Fidelity $54.7m, Marin $45.4m, Chicago Community Trust $32.9m.
- **Middle East and North Africa:** NPT $87.3m, Jewish Communal Fund $82.3m, Jewish Community Foundation of LA $44.4m.
- **South America:** NPT $70.1m, GS $38.5m.
- **Without SVCF:** Europe 45.3%, Middle East and North Africa 14.9%.
- **Interpretation [I]:** Europe's lead is consistent with gifts to UK and European universities, arts bodies and sponsor affiliates. Schedule F does not name recipients, so this cannot be confirmed here (P-B45N31-02).

### 3.4 Purposes and manner (Part II) [C]

- **Purpose buckets (main scope).** These are dollars by the keyword bucket of the *reported* purpose text. The general-support bucket is the last rule and also catches \
  - general support $417.6m (22.1%);
  - "international" (unspecified; NPT's NTEE-style label) $351.0m (18.6%);
  - environment and animals $259.0m (13.7%);
  - education $215.8m (11.4%);
  - arts and culture $190.4m (10.1%);
  - human services and civic $164.7m (8.7%);
  - health $127.2m (6.7%);
  - other $64.4m (3.4%);
  - development and poverty $55.4m (2.9%);
  - research $33.5m (1.8%);
  - religion $10.3m (0.5%);
  - relief/humanitarian $1.0m (0.05%).
- **Top raw purpose texts:**
  - "INTERNATIONAL" $349.3m (254 lines);
  - "EDUCATION" $204.5m;
  - "CULTURE & ARTS" $175.5m;
  - "ENVIRONMENT & ANIMAL PROTECTION" $140.4m;
  - "IN FURTHERANCE OF GRANTEE'S TAX-EXEMPT PURPOSE" $111.1m;
  - "HEALTH" $104.4m;
  - "PUBLIC, SOCIETAL BENEFIT" $74.1m;
  - "GENERAL SUPPORT" $63.6m (511 lines).
- **Purpose by segment:**
  - Nationals: "international" 28.9%, environment 18.5%, arts 15.3%.
  - Community foundations: general support 33.1%, education 18.7%, health 17.2%.
  - Single-issue: general-support bucket 96.0%. This is generic reported text, led in FY2023 by \
- **Manner:**
  - wire $1,458.3m (77.1%), ACH/EFT $357.4m (18.9%), check $70.1m (3.7%).
  - Nationals use wire for 98.4%; community foundations ACH/EFT for 69.7%; single-issue sponsors check for 29.7%.

### 3.5 Reliance on US intermediaries and friends-of organisations (Schedule I) [F/C/I]

| Intermediary | Inbound from top-50, FY2023–24 | Top-50 grantors | Intermediary's own foreign share (FY2023–24) | Est. passed abroad |
|---|---|---|---|---|
| CAF America (DAF-to-DAF whitelisted) | $58.6m | 30 | 36.1% | $21.1m |
| Myriad USA (formerly KBFUS) | $46.5m | 30 | 98.2% | $45.7m |
| GlobalGiving | $33.0m | 24 | 72.2% | $23.9m |
| Global Greengrants Fund | $27.9m | 13 | 95.2% | $26.5m |
| Global Fund for Women | $17.2m | 15 | 94.0% | $16.2m |
| Give2Asia | $12.0m | 11 | 91.8% | $11.0m |
| Global Fund for Children | $11.2m | 9 | 98.8% | $11.1m |
| British Schools and Universities Foundation | $6.6m | 14 | 100% | $6.6m |
| Friends of Fondation de France | $2.5m | 8 | 100% | $2.5m |
| **Total** | **$215.6m** (FY2023 $120.0m; FY2024 $95.6m) | | | **$164.7m** |

- **Size of the intermediary route:**
  - The named-intermediary route is **≈0.2% of top-50 grants**, and its estimated pass-through is **8.7% of the direct Schedule F route**.
  - CAF America's own grants are only 36% foreign by Part IX; the rest is domestic line-1 grants.
  - Leading users: Fidelity $63.6m, NPT $36.9m, Vanguard $20.5m, ImpactAssets $14.4m, GS $13.1m, Chicago Community Trust $12.9m, SVCF $11.3m.
  - For Fidelity and Vanguard, which make few direct foreign grants, the intermediary route is **56% and 187% of their direct foreign grants** respectively [C].
- **Friends-of names:**
  - $432.9m (main scope).
  - Leading users: Fidelity $103.8m, Jewish Communal Fund $62.2m, Vanguard $49.3m, NPT $41.6m.
  - Largest recipients: Friends of the IDF $54.5m, AF Tel Aviv University $40.7m, AF Winchester College $40.0m, AF Magen David Adom $36.3m, AF University College Oxford $17.4m.
  - These organisations re-grant to the named foreign institution, but their foreign share was not parsed (P-B45N31-01).
- **NTEE Q recipients:**
  - $4.32bn net (main scope); see P-NEW-RCP-01 for its sub-codes (Q30 $1.27bn, Q33 relief $1.26bn).
  - Relief/humanitarian giving runs almost entirely through US Q-coded charities (e.g. MSF USA, World Central Kitchen), while direct foreign grants carry 0.05% relief purpose text [C/I]. The 0.05% is a floor: 22.1% of these dollars carry generic text and 18.6% the bare label \
- **Fidelity and Vanguard compared:**
  - Fidelity: direct foreign $114.2m, named intermediaries $63.6m, friends-of $103.8m. Friends-of plus named intermediaries are 1.5× its direct foreign dollars.
  - Vanguard: direct foreign $11.0m, named intermediaries $20.5m, friends-of $49.3m.
  - [I] The low-cost nationals route a large share of their overseas-directed giving through US 501(c)(3)s rather than making ED/ER grants themselves.

### 3.6 Equivalency determination vs expenditure responsibility [F/C/I]

- **Part V narratives:**
  - Of the 70 sponsor-years with any foreign grants, 41 describe ED and/or ER: ED 31, ER 27.
  - They hold $1,814.6m, 94.7% of top-50 foreign dollars.
  - By segment: national 17 of 25 (ED 15, ER 14); community foundations 20 of 33 (ED 12, ER 13); single-issue 4 of 10 (ED 4, ER 0).
  - NGOsource is named in 3 sponsor-years (Denver Foundation FY2024; Minneapolis Foundation FY2023–24).
  - Fidelity and NPT state both methods.
- **Part II line 2 counts** (main scope): 2,543 recipients in the 501(c)(3) column vs **672 "other organisations"**.
  - The form's "other" column is for recipients not shown to be 501(c)(3)-equivalent. [I] Grants to them need expenditure responsibility.
  - SVCF: 539 of the 672 (231 in FY2023, 308 in FY2024).
  - Other community foundations: 51.
  - National sponsors: 5.
  - Single-issue: 77, all Jewish Community Federation of SF (17 in FY2023, 60 in FY2024).
- **Implication [I]:** ER-type grantmaking is concentrated at SVCF and a few community foundations. The nationals' foreign grants go almost entirely to ED-qualified or IRS-recognised recipients, consistent with the reading in breadth-community-faith-infrastructure-emerging.md §6.4.
- **Boycott question (Schedule F Part IV line 6) answered yes:** NPT FY2024, Community Foundation of New Jersey (both years), Stanford (both years). This is filed as such; the reason is not given.

## 4. Limitations

1. **Region, not country.** Schedule F reports regions only, and recipient names are not in the public e-file. Country-level or recipient-level analysis needs other sources (sponsors' grant lists, affiliates' accounts). "North America" means Canada, Mexico, Bermuda and similar, never the US.
2. **Friends-of and US intermediaries hide foreign giving.** Grants to US 501(c)(3)s that re-grant abroad are on Schedule I as domestic grants. The pass-through estimate covers only nine named intermediaries and assumes their inbound DAF money leaves the US at their average foreign share in the same year [I]. Friends-of and NTEE Q recipients are measured by inbound dollars only.
3. **NTEE Q is not "spent abroad".** Q includes US-based international-affairs, exchange and policy organisations. The 7.8–8.1% combined shares therefore mix money that leaves the US with money spent on international causes in the US [I].
4. **Sponsor-to-affiliate transfers.** Foreign grants may include transfers to a sponsor's own overseas affiliate (e.g. NPT UK), which are the cross-border analogue of DAF-to-DAF flows. They are not netted here because Schedule F has no recipient name (P-B45N31-02).
5. **Gross vs DAF.** Line 3 covers all of a sponsor's grants, including non-DAF funds at community foundations. The DAF-weighted variant (1.96%) assumes the same foreign mix for DAF and non-DAF grants [I].
6. **Purpose text is free-form and often generic.** The keyword buckets are inference. NPT uses NTEE-style labels; other filers write "general support" or "tax-exempt purpose".
7. **Filing errors.** NPT FY2024's shifted columns were repaired ($410.3m). Morgan Stanley FY2024's Part II exceeds line 3 by $1.2m. Shares use line 3.
8. **Fiscal-year convention.** A June-FYE FY2024 return covers July 2023–June 2024. The intermediaries' fiscal years differ (CAF America April, GFC/GFW/Greengrants June), so their pass-through matching is approximate.
9. **Part I is not a grant measure.** Part I region totals include investments ($27.3bn of $29.2bn in the main scope). Only `region_part1_grantmaking` rows relate to grants.

## 5. Data dictionary — `daf-foreign-grants-schedule-f-2023-2024.csv`

| Column | Meaning |
|---|---|
| row_type | `scope_total`, `sponsor_year`, `region_part2`, `region_part3`, `region_part1_grantmaking`, `activity_part1`, `purpose_bucket_part2`, `purpose_text_part2` (top 25 per scope; not for sponsor scopes), `manner_part2`, `manner_part3`, `assistance_type_part3`, `intermediary` |
| scope, scope_type | `all_top50`, `all_ex_university_hospital`, `all_ex_university_hospital_ex_svcf` (type `all`); a DAFRC segment (type `segment`); a sponsor name (type `sponsor`); an intermediary name (type `intermediary`) |
| ein, segment, sponsor_rank_fy2024 | Sponsor (or intermediary) EIN; DAFRC segment; FY2024 DAF-asset rank |
| fiscal_year | `2023`, `2024` or `2023-2024` (pooled); FY = calendar year in which the tax period ends |
| object_id, tax_period_end | IRS e-file object id(s) and tax period end of the return(s) used |
| category | Dimension value: region (10 Schedule F regions plus `Latin America/Africa/Asia (unspecified)`), purpose bucket or raw text, manner (`wire`, `ach_eft_transfer`, `check`, `not_stated`, `other`), Part III assistance type, or Part I activity (`grantmaking`, `investments`, `program_or_other`) |
| amount_usd, share, denominator_usd, lines, sponsor_years | Dimension rows: dollars (cash + non-cash), share of the scope's dimension total, that total, line count, sponsor-years pooled. Intermediary rows: `amount_usd` = gross inbound Schedule I dollars from top-50 sponsors |
| grantors | Intermediary rows: number of distinct top-50 sponsors granting to it |
| sched_i_itemised | 1 if the return itemises Schedule I (not attachment-only) |
| part_ix_l1_domestic_orgs_usd, part_ix_l2_domestic_indiv_usd, part_ix_l3_foreign_usd, total_grants_usd | Form 990 Part IX lines 1, 2, 3 (column A) and their sum |
| foreign_share_of_grants | line 3 ÷ (lines 1–3) |
| foreign_daf_weighted_usd, total_grants_daf_weighted_usd, daf_weight | Scope totals × each sponsor-year's DAF share of grants (`sponsor-cost-structure.csv`, capped at 1); weight blank → 1 |
| sponsor_years_with_foreign_grants, sponsor_years_sched_f | Counts of sponsor-years with line 3 > 0 and with a Schedule F |
| sched_f_present | 1 if the return includes Schedule F |
| sched_f_part1_regions, sched_f_part1_total_usd, sched_f_part1_grantmaking_usd, sched_f_part1_total_spent_reported_usd | Part I: region rows, sum of region expenditures (all activities), of grantmaking rows only, and the filed `TotalSpentAmt` |
| sched_f_part2_lines, sched_f_part2_usd, sched_f_part2_501c3_cnt, sched_f_part2_other_org_cnt | Part II: line count, dollars, line 2 counts (501(c)(3)/equivalent vs other organisations; blank if not filed) |
| sched_f_part3_lines, sched_f_part3_usd, sched_f_part3_recipients | Part III (grants to foreign individuals) |
| p4_ForeignOfficeInd, p4_ForeignActivitiesInd, p4_MoreThan5000KToOrgInd, p4_MoreThan5000KToIndividualsInd | Form 990 Part IV lines 14a, 14b, 15, 16 (1/0) |
| sf_GrantRecordsMaintainedInd, sf_TransferToForeignCorpInd, sf_InterestInForeignTrustInd, sf_ForeignCorpOwnershipInd, sf_PassiveForeignInvestmestCoInd, sf_ForeignPartnershipInd, sf_BoycottCountriesInd | Schedule F Part I line 1 and Part IV lines 1–6 (1/0; blank if absent). The tag spelling `Investmest` is the IRS schema's |
| ed_text, er_text, ngosource_text, intermediary_text, part5_chars | Part V narrative flags (1/0) for equivalency determination, expenditure responsibility, NGOsource, a named intermediary; narrative length |
| ed_text_sponsor_years, er_text_sponsor_years | Scope totals: sponsor-years with each flag |
| sched_i_gross_usd, sched_i_net_usd | Schedule I Part II dollars, all lines and net of DAF-to-DAF (P-NEW-RCP-01 rules) |
| sched_i_named_intermediary_usd | Gross Schedule I dollars to the nine named intermediaries |
| sched_i_friends_of_usd | Schedule I dollars to friends-of names (excluding named intermediaries) |
| sched_i_ntee_q_usd, sched_i_ntee_q_net_usd | Schedule I dollars to NTEE Q recipients, gross and net |
| sched_i_intl_union_net_usd | Net Schedule I dollars to the union of named, friends-of and NTEE Q recipients |
| itemising_part_ix_l3_foreign_usd | Line 3 summed over itemising sponsor-years only (matches the Schedule I base) |
| foreign_share_of_net_sched_i_plus_l3, ntee_q_share_of_net_sched_i_plus_l3, broad_intl_share_of_net_sched_i_plus_l3 | line 3, NTEE Q net, and (line 3 + union) ÷ (net Schedule I + line 3), itemising sponsor-years |
| intermediary_total_grants_usd, intermediary_part_ix_l3_foreign_usd, intermediary_foreign_share, est_foreign_pass_through_usd | Intermediary rows: its own Part IX lines 1–3 and line 3 for the matching FY(s), the ratio, and inbound × ratio |
| status, via | Extraction status (`ok`) and source (`local` copy or `mirror` stream) |
| source | Source note |

## 6. Sources

| # | Source | Date | robots.txt |
|---|---|---|---|
| S1 | IRS Form 990 e-file XML (Part IX, Part IV, Schedule F), GivingTuesday mirror of IRS TEOS. 100 top-50 returns (object ids in `sponsor_year` rows) + 18 intermediary returns (`intermediary` rows) | read 2026-11-15 | gt990datalake-rawdata.s3.amazonaws.com → 404 (no rules) |
| S2 | IRS TEOS e-file index CSVs `index_2023`–`index_2026` (https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv), scratch copies | earlier batches | n/a (not re-fetched) |
| S3 | IRS EO BMF eo1–eo4, eo_pr, eo_xx (Last-Modified 2026-11-09), scratch copy from P-NEW-RCP-01 | 2026-11 | www.irs.gov read 2026-11-15; `/pub/` not disallowed |
| S4 | Repo: Schedule I line cache and `annotate` (P-NEW-RCP-01), `daf-to-daf-recipient-whitelist.csv` (batch 34), `sponsor-cost-structure.csv`, `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `netpayout990/` cache | repo | n/a |

## 7. Reproduction

```
python3 scripts/mission_foreign_grants.py --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF --irs-dir IRS \
    --extract-cache EC [--xml-list XMLPATHS ...] [--fetch] [--workers 6]
```

- `NPCACHE`, `LINES` and `BMF` are those of `mission_recipient_sectors.py`.
- `IRS` holds the TEOS `index_YYYY.csv` files.
- `EC` caches one Schedule F extract JSON per object id (about 4 MB in total).
- `XMLPATHS` lists local XML copies, one path per line.
- Run time is about 20 s with a warm cache. Two consecutive runs gave identical totals.
- Every figure in §0–3 comes from the script's printed JSON summary or the CSV. Ratios such as the top-3 share, the big-4 share and pass-through ÷ direct are arithmetic on those outputs.

## Validation corrections (wave 30, 2026-11-15) — governing
Source: [validation-wave30-report.md](validation-wave30-report.md); register `data/mission-2026-11-14/validation-register-wave30.csv`.

1. **§0, ED vs ER row.**
   - **Find:** "**Part V narratives:** of the 70 sponsor-years with foreign grants, 41 describe ED and/or ER (31 ED, 27 ER). Together they hold 94.7% of the foreign dollars [C]."
   - **Replace with:** "**Part V narratives:** of the 70 top-50 sponsor-years with foreign grants (68 in the main scope), 41 describe ED and/or ER (31 ED, 27 ER). Together they hold 94.7% of all top-50 foreign dollars, or 96.0% in the main scope [C; V wave 30]."
2. **§0, comparison with the NTEE sector analysis.**
   - **Find:** "**International is therefore understated by about 2.2–2.5 points in the Schedule-I-only sector shares.**"
   - **Replace with:** "**International is therefore understated by about 2.2–2.6 points against the published 5.6% (2.4–2.7 points like-for-like, since NTEE Q is 5.45% on the Schedule I + line 3 base) in the Schedule-I-only sector shares** [C; V wave 30]."
