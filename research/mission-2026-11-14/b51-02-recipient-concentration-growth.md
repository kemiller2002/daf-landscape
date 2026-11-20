# B51-02: how concentrated DAF grant dollars are among recipients, and who grew fastest (FY2021–FY2024)

**Date:** 2026-11-20 · **Task ID:** b51-02

**Outputs**
- Script: [`scripts/mission_recipient_concentration.py`](../../scripts/mission_recipient_concentration.py). It is new, stdlib only and functional in style. It imports the repo's universe, return choice, line parser, DAF-to-DAF netting and DAF weighting unchanged from `mission_daf_to_daf.py`, `mission_net_payout.py` and `mission_recipient_sectors.py`. Two runs of the final script from cache gave byte-identical CSVs.
- Data: [`data/mission-2026-11-14/recipient-concentration-growth-2026-11-20.csv`](../../data/mission-2026-11-14/recipient-concentration-growth-2026-11-20.csv). 386 rows: 30 `concentration` and 356 `grower` (50 `abs`, 50 `pct`, 50 `pct_p1_1m`, 206 `entrant`; a recipient can appear in more than one list). The data dictionary is in §6.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b51-02.csv`](../../data/mission-2026-11-14/queue-proposals-b51-02.csv) (5 rows, P-B5102-01..05).

Tags: **[F]** computed by the script from filed data · **[P]** quoted primary source · **[I]** inference or judgement.

---

## 0. Answer in brief

**Concentration (balanced panel of 44 sponsors, Schedule I filed dollars, net of DAF-to-DAF) [F]**

| FY | Net $bn | Recipients | Top-10 | Top-100 | Top-1,000 | Gini | HHI (0–10,000) |
|---|---|---|---|---|---|---|---|
| 2021 | 31.23 | 118,266 | 6.6% | 20.7% | 54.3% | 0.891 | 9.1 |
| 2022 | 33.43 | 125,328 | 7.7% | 23.3% | 52.0% | 0.885 | 11.1 |
| 2023 | 36.53 | 130,328 | 15.4% | 29.4% | 53.7% | 0.890 | 43.1 |
| 2024 | 40.29 | 143,551 | 8.4% | 22.9% | 49.1% | 0.885 | 14.6 |

- **Trend.** The broad shape of the distribution is stable. Gini stays between 0.885 and 0.891. The **top-1,000 share falls by 5.2 points** (54.3% → 49.1%) as the number of recipients grows by 21%. So the middle and the tail gained share. [F]
- **The top of the distribution is lumpy, not trending.** Top-10 share and HHI spike in FY2023 and fall back in FY2024. The FY2023 spike comes from a few very large single-sponsor lines:
  - Johns Hopkins University, $1.56bn;
  - the Navigation Charitable Fund, $1.31bn (one SVCF line);
  - four Chan Zuckerberg Biohub LLCs, $1.66bn together (SVCF).
  These are $4.53bn of the $5.64bn top-10 total in FY2023 [F].
- On the all-itemising scope (44, 44, 46 and 48 sponsor-years), FY2023 and FY2024 **reproduce the repo's sector file exactly**: $36.872bn and $41.416bn; top-10 0.1532 and 0.0827; HHI 42.5 and 14.4 (`daf-grant-recipient-sectors-top50.csv`) [F].

**Fastest growers (balanced panel; P1 = FY2021+22, P2 = FY2023+24; floor P2 ≥ $5m) [F]**

- Balanced-panel net dollars rose from **$64.66bn (P1) to $76.82bn (P2), +$12.17bn (+18.8%)**. 2,167 recipients clear the $5m floor.
- **Top 50 by absolute growth:** P1 $3.91bn → P2 $12.62bn, **+$8.71bn**. That equals 72% of the panel's net growth; the top 10 alone add $5.82bn.
  - Types (rule, first match): **11 universities**, 7 NTEE-T grantmakers, 6 listed pass-through intermediaries, 4 CZ Biohub LLCs (disregarded entities), 4 international, 3 fiscal sponsors, 3 other education, 2 hospitals, 2 human services, 2 blank-EIN churches, 2 arts and culture, 1 NTEE U research body (Navigation), 1 policy or advocacy (NTEE code 01), 1 religious, 1 community development (W60).
  - **New organisations (BMF ruling 2020 or later): 10 of 50.**
  - **Fiscal sponsors: 3** (Rockefeller Philanthropy Advisors, 50CAN, Global Impact; all on the repo's fiscal-sponsor list). **Intermediaries of any kind: 16** (fiscal sponsors + pass-through list + NTEE T grantmakers). It is 17 if the Navigation Charitable Fund is counted as a re-granting intermediary, as b40n12 describes it [I].
- **Top 50 by percentage growth (P1 > 0):** dominated by recipients with a tiny P1. 44 of 50 had P1 under $100k, and 15 owe their P2 mostly to The Chicago Community Trust. 11 of 50 are new organisations; 0 are fiscal sponsors; 3 are intermediaries.
- **Sensitivity: percentage growth among P1 ≥ $1m.** 8 of 50 are new organisations, 2 are fiscal sponsors (50CAN, Global Impact), 7 are intermediaries. The most common types are human services (14) and schools and other education (7).
- **Entrants (P1 = 0, P2 ≥ $5m): 206 recipients took $5.59bn in P2**, 46% of net growth. 77 of them are new organisations; 20 have no BMF ruling. Most entrant dollars are the Navigation Charitable Fund and the CZ LLCs ($2.97bn).

---

## 1. Method

### 1.1 Universe and lines (repo rules, imported)
- **Sponsors.** Top 50 DAFRC sponsors by FY2024 DAF assets (`mission_daf_to_daf.top_n`).
- **Returns.** One per sponsor × fiscal year (`pick_returns` over the netpayout990 cache). Only returns that itemise Schedule I count (`mission_net_payout.itemized`). Fiscal year = calendar year the tax period ends.
- **Itemising sponsor-years:** FY2021 44, FY2022 44, FY2023 46, FY2024 48 (all 50 sponsors have returns each year; the rest point to an attachment) [F].
- **Lines.** Every Schedule I Part II line, via `mission_recipient_sectors.load_lines`. The 94 FY2023–24 returns came from existing caches. **The 88 FY2021–22 returns were read for this study** from the GivingTuesday mirror of IRS TEOS e-file XML; each matched the expected line count. 1,102,444 lines in total [F].

### 1.2 DAF-to-DAF netting (repo rule)
- `mission_recipient_sectors.annotate`, unchanged: lines to an EIN whose decision is `include` in `daf-to-daf-recipient-whitelist.csv`, self-lines, and blank-EIN lines whose name matches exactly one whitelisted panel name are dropped.
- Netted out per year [F]: FY2021 $6.21bn, FY2022 $5.95bn, FY2023 $4.65bn, FY2024 $8.08bn (all-itemising scope).
- The whitelist was built on FY2021–24 inbound lines (its `inbound_gross_fy2021..2024` columns), so it applies to the earlier years without change.

### 1.3 Bases
- **schedule_i** (filed dollars) is the headline basis.
- **daf_weighted** multiplies each sponsor-year's lines by `daf_share_of_grants` from `sponsor-cost-structure.csv`, capped at 1. That file has **no FY2021 shares** (0/44), so DAF-weighted rows are written only for FY2022–24 (full coverage those years). On FY2022–24, DAF-weighted shares differ from filed shares by at most 0.3 points on top-100 [F]. Growth lists use the filed basis.

### 1.4 Scopes
- **all_itemising**: every itemising top-50 sponsor-year in that FY.
- **balanced_panel**: the 44 sponsors that itemise in all four years. **This is the trend and growth basis**, so coverage changes do not show up as growth. The four sponsors outside it (Greater Horizons, Greater Kansas City CF, The New York Community Trust, US Charitable Gift Trust) itemise only in FY2023–24 [F]. For FY2021–22 the two scopes are identical.
- **Sensitivities** (filed basis): `*_cz_merged` merges the four Chan Zuckerberg LLC EINs (88-2010111, 88-2242512, 92-2259616, 93-1478843) into CZ Biohub Inc (81-1669175). These LLCs are disregarded entities of Biohub per the repo's non-BMF note. `*_net_non_dafrc_daf_filers` additionally drops lines to the 2,468 EINs in `non-dafrc-daf-filers-990.csv` (DAF-holding filers outside the DAFRC panel). This is **not** the repo's netting rule; it is a bound.

### 1.5 Metrics
- Recipients are keyed by EIN; blank-EIN lines by normalised name (repo convention, `key` in `annotate`).
- Top-N share = sum of the N largest recipients ÷ net total.
- **Gini** over recipients with a positive total that year: G = 2Σ i·x(i) / (nΣx) − (n+1)/n, x ascending. It describes inequality among recipients that received anything, not among all charities.
- **HHI** = Σ (100 × share)², scale 0–10,000 (the repo's convention).

### 1.6 Growth lists
- Balanced panel, filed basis. P1 = FY2021+FY2022, P2 = FY2023+FY2024; eligible if P2 ≥ $5m.
- `abs`: top 50 by P2 − P1. `pct`: top 50 by P2/P1 − 1 among P1 > 0. `pct_p1_1m`: the same among P1 ≥ $1m (sensitivity added because the `pct` list is dominated by near-zero bases). `entrant`: every eligible recipient with P1 = 0.

### 1.7 Classification
Joined to the IRS EO BMF (eo1–4, eo_pr, eo_xx; cached 2026-11-14) for NTEE_CD, SUBSECTION, FOUNDATION and RULING. Neutral by design: types come from NTEE codes, IRS fields and repo lists only, and say nothing about viewpoint.

`org_type`, first match wins:
1. `blank_ein_name_keyed`: line has no EIN.
2. `disregarded_entity_llc`: `subsidiary_or_disregarded` in `non-bmf-recipients-2026-11-20.csv`.
3. `not_in_bmf_<category>`: EIN absent from the BMF; category from the same file.
4. `fiscal_sponsor`: EIN on `fiscal-sponsor-ein-list-2026-11-19.csv` (grantmaker hosts excluded, as in the refined flag) or `de_facto_intermediary = True` in `de-facto-fiscal-sponsors-2026-11-20.csv` (338 EINs).
5. `intermediary_pass_through`: `pass_through_class = regranting_intermediary` in `pass-through-recipients-2026-11-20.csv`.
6. `daf_sponsor_not_netted`: DAFRC panel national, processor or community foundation EIN not netted by the whitelist (none among the growers).
7. `university_college`: NTEE B4x/B5x, or university/college name (foundation code 11 or no NTEE).
8. `hospital_health_system`: NTEE E2x or foundation code 12.
9. `grantmaking_intermediary_ntee_t`: NTEE T (philanthropy, federated giving, grantmaking public charities, supporting trusts).
10. `policy_or_advocacy_ntee`: NTEE R; W01–W05 or W20–W24; or common code 01 (alliances & advocacy) in any major group.
11. `research_institute_ntee_u_v`: NTEE U or V.
12. `school_or_other_education`: other NTEE B.
13. `religious`: NTEE X or foundation code 10.
14. `medical_research_or_health`: other NTEE E–H.
15. `international`: NTEE Q.
16. `operating_<major group>`: everything else (`unclassified` = in BMF with blank NTEE).

Flags: `is_new_org` = BMF RULING ≥ 202001; `is_fiscal_sponsor` = rule 4; `is_intermediary` = rule 4, a pass-through `fiscal_sponsor` or `regranting_intermediary` class, or NTEE T.

## 2. Overlap with other studies (read, not edited)

| Study | Overlap | What this note adds |
|---|---|---|
| [P-NEW-RCP-01 sector file](b39n4-01-sector-join-all-sponsors.md) (`daf-grant-recipient-sectors-top50.csv`) | Same universe, lines and netting for FY2023–24; top-10/top-100/HHI reproduced exactly | FY2021–22, top-1,000, Gini, balanced panel |
| [b51-01 sector-mix trend](b51-01-sector-mix-trend.md) | Also reads FY2021–22 lines; reports top movers within sectors (ex-university/hospital, DAF-weighted) | Recipient-level concentration across all sectors; growth lists with types |
| [b39n6-03 pass-through recipients](b39n6-03-pass-through-recipients.md) | Source of `pass_through_class` and `hand_subtype` | Which pass-through EINs are among the fastest growers |
| [b40n1202-b43n26-03 non-BMF recipients](b40n1202-b43n26-03-non-bmf-recipients.md) | Source of the CZ LLC identification (Schedule R, disregarded entities of CZ Biohub Inc) | CZ-merged sensitivity |
| [b40n12 DAF share of recipient revenue](b40n12-daf-share-of-recipient-revenue.md), [b41n17 unlisted recipients](b41n17-g0505-unlisted-recipients.md) | Navigation Charitable Fund identification (filed as "Further Future Foundation", renamed 2023-11-01) | Its weight in FY2023 concentration |

## 3. Results: concentration

### 3.1 All rows [F]

| Scope | Basis | FY | Net $bn | DAF-to-DAF netted $bn | Recipients | Top-10 | Top-100 | Top-1,000 | Gini | HHI |
|---|---|---|---|---|---|---|---|---|---|---|
| all_itemising | filed | 2021 | 31.23 | 6.21 | 118,266 | 6.55% | 20.67% | 54.30% | 0.891 | 9.1 |
| all_itemising | filed | 2022 | 33.43 | 5.95 | 125,328 | 7.67% | 23.27% | 51.95% | 0.885 | 11.1 |
| all_itemising | filed | 2023 | 36.87 | 4.65 | 132,329 | 15.32% | 29.23% | 53.50% | 0.890 | 42.5 |
| all_itemising | filed | 2024 | 41.42 | 8.08 | 147,116 | 8.27% | 22.97% | 48.84% | 0.885 | 14.4 |
| all_itemising | DAF-wtd | 2022 | 31.83 | 5.85 | 125,328 | 7.33% | 23.07% | 51.97% | 0.886 | 10.6 |
| all_itemising | DAF-wtd | 2023 | 34.78 | 4.54 | 132,316 | 15.23% | 29.05% | 53.60% | 0.891 | 44.5 |
| all_itemising | DAF-wtd | 2024 | 39.50 | 7.76 | 147,104 | 8.10% | 22.73% | 48.69% | 0.884 | 14.5 |
| balanced_panel | filed | 2023 | 36.53 | 4.63 | 130,328 | 15.44% | 29.36% | 53.72% | 0.890 | 43.1 |
| balanced_panel | filed | 2024 | 40.29 | 8.01 | 143,551 | 8.40% | 22.94% | 49.06% | 0.885 | 14.6 |
| balanced_panel | DAF-wtd | 2023 | 34.61 | 4.52 | 130,315 | 15.30% | 29.15% | 53.76% | 0.891 | 44.9 |
| balanced_panel | DAF-wtd | 2024 | 38.51 | 7.69 | 143,538 | 8.15% | 22.66% | 48.87% | 0.884 | 14.6 |

Balanced-panel FY2021–22 rows equal the all-itemising rows (same 44 sponsors).

### 3.2 What sits at the top [F]
Largest recipients, balanced panel, filed $m:
- **FY2021:** Regents of the University of California 330; New Venture Fund 327; Stanford 242; Lucas Museum of Narrative Art 200; Johns Hopkins 190. Top-10 total $2.05bn.
- **FY2022:** Dayton Foundation Plus 386 (one Marin Community Foundation line; see §3.3); Regents of UC 337; Stanford 323; Johns Hopkins 269; Lucas Museum 250. Top-10 total $2.56bn.
- **FY2023:** Johns Hopkins 1,558; Navigation Charitable Fund 1,309; CZ Institute for Advanced Biological Imaging LLC 586; CZ Biohub SF LLC 576; Regents of UC 379. Top-10 total $5.64bn.
- **FY2024:** Johns Hopkins 1,030; Regents of UC 381; Stanford 324; New Venture Fund 267; Blue Meridian Partners 256. Top-10 total $3.38bn.

### 3.3 Sensitivities [F]
- **CZ LLCs merged into CZ Biohub Inc:** FY2023 top-10 rises from 15.44% to 16.64% and HHI from 43.1 to 57.7 (balanced). Biohub becomes the #1 recipient. Other years are unchanged (the LLCs receive only in FY2023).
- **Also netting non-DAFRC DAF filers** (2,468 EINs): FY2022 total falls by $1.20bn and top-100 from 23.27% to 21.97% (all-itemising). Top-10 shares move by at most 0.6 points in any year, and the top-1,000 decline (54.25% → 48.50%) is unchanged in direction. The single largest item is Marin Community Foundation's FY2022 line of $385.7m to Dayton Foundation Plus Inc (EIN 54-2101090), which is in that file for FY2021–2024. Whether such lines are DAF-to-DAF is queued (P-B5102-01).

### 3.4 Reading the trend [I]
- Dollars spread more widely: more recipients each year, and the top-1,000 share down 5 points. Gini is flat because it is dominated by the very long tail of small grants, which also grew.
- The top-10 and HHI series move with a handful of very large one-sponsor gifts, so they are not a stable trend measure on four years of data. Top-1,000 and Gini are the more robust indicators here.

## 4. Results: fastest growers

### 4.1 Top 50 by absolute growth (filed $m) [F]
Full rows (NTEE, ruling, grantor counts, top grantor and its share) are in the CSV, `rank_list = abs`. The type is the rule type of §1.7.

| # | Recipient | NTEE | Ruling | Type | P1 | P2 | Growth |
|---|---|---|---|---|---|---|---|
| 1 | Johns Hopkins University | B430 | 1935 | university | 458.6 | 2,588.3 | +2,129.7 |
| 2 | Navigation Charitable Fund | U05 | 2023 | research (U/V) | 0 | 1,309.0 | +1,309.0 |
| 3–6 | Four CZ Biohub LLCs | — | — | disregarded LLC | 0 | 1,656.5 | +1,656.5 |
| 7 | Memorial Sloan-Kettering Cancer Center | E120 | 1962 | hospital | 49.1 | 263.2 | +214.1 |
| 8 | Climate Imperative Foundation | C12 | 2021 | pass-through intermediary | 60.0 | 247.1 | +187.1 |
| 9 | United States Energy Foundation | T30 | 2019 | pass-through intermediary | 25.0 | 190.4 | +165.4 |
| 10 | Cornell University | B430 | 1951 | university | 152.3 | 307.8 | +155.5 |
| 11 | California Institute of Technology | B430 | 1937 | university | 60.4 | 215.7 | +155.3 |
| 12 | Just Trust for Education | I50 | 2023 | human services | 0 | 131.6 | +131.6 |
| 13 | The Clear Fund | T30 | 2007 | NTEE T grantmaker | 57.2 | 182.2 | +125.0 |
| 14 | Our American Future Foundation | R40 | 2022 | pass-through intermediary | 0 | 118.8 | +118.8 |
| 15 | The 85 Fund | I01 | 2011 | policy/advocacy (code 01) | 212.9 | 311.9 | +99.0 |
| 16 | Blue Meridian Partners | P12 | 2017 | pass-through intermediary | 269.3 | 363.0 | +93.7 |
| 17 | Regents of the University of California | — | 1970 | university | 666.6 | 759.5 | +92.9 |
| 18 | City Fund | T30 | 2018 | NTEE T grantmaker | 11.0 | 100.8 | +89.8 |
| 19 | Rockefeller Philanthropy Advisors | T500 | 1991 | fiscal sponsor | 153.1 | 242.6 | +89.5 |
| 20 | Come and See Foundation | X20 | 2022 | religious | 50.1 | 139.5 | +89.4 |
| 21–50 | see CSV | | | | | | |

Ranks 21–50 include, among others:
- Universities: Harvard, Duke, Stanford, USC, Rockefeller University, Kyiv School of Economics, California Academy of Studio Arts.
- Fiscal sponsors: 50CAN, Global Impact.
- Schools: Jackson Hole Classical School, Ransom Everglades, XQ Institute.
- International relief and health: MSF USA, Save the Children, Vital Strategies, Follow Your Dream Foundation.
- Supporting trusts and grantmakers: UJA-Federation, James Family Charitable Trust, Deitch Family Charitable Support Trust, Founders Pledge, RF Catalytic Capital.
- Pass-through and other: Charter Fund and Worthington Scholarship Foundation (pass-through list), two blank-EIN Baptist churches (National Christian Charitable Foundation lines), and the Barack Obama Foundation (A80).

Counts [F]:
- **New organisations: 10.** Navigation, Climate Imperative, Just Trust for Education, Our American Future Foundation, Come and See Foundation, California Academy of Studio Arts, RF Catalytic Capital, Charter Fund, Deitch Family Charitable Support Trust, Founders Pledge. Charter Fund's ruling (2025-08) post-dates its P1 receipts; ruling dates can be retroactive.
- **The CZ LLCs have no BMF row and are not counted as new.** They are disregarded entities of a 2016-ruled parent (non-BMF note).
- **Fiscal sponsors: 3.** Recipients on the b39n6-03 pass-through list: 8. Intermediaries of any kind: 16.

### 4.2 Percentage growth [F]
- **`pct` (P1 > 0):** median P1 is $25,000, and 44 of 50 have P1 under $100k. The list measures first large gifts rather than growth. 15 have The Chicago Community Trust as top FY2023–24 grantor; 20 have a single grantor for 100% of P2. Types: 10 schools and other education, 8 human services, 6 blank-NTEE operating charities, 5 public/societal benefit, 3 each NTEE T, religious and health. New organisations 11, fiscal sponsors 0, intermediaries 3.
- **`pct_p1_1m` (P1 ≥ $1m):** the top five by growth_pct are Edesia (K30; +6,243%), Murmuration Research Institute (W99; +3,947%), Jackson Hole Classical School (+2,889%), BeyGood Foundation (T30; +2,566%) and Ransom Everglades School (+2,325%). Human services lead (14), then schools and other education (7) and NTEE T (5). New organisations 8, fiscal sponsors 2, intermediaries 7.

### 4.3 Entrants [F]
206 recipients had no top-50 DAF dollars in FY2021–22 and at least $5m in FY2023–24, totalling $5.59bn.
- Types: 30 human services, 24 NTEE T grantmakers, 22 health, 18 public/societal benefit, 17 education, 16 hospitals, 15 policy or advocacy by NTEE, and others.
- 77 have a ruling in 2020 or later.

### 4.4 Concentration of sponsors behind the growth [F]
- Many of the largest gains come from one sponsor:
  - Navigation, the CZ LLCs and Just Trust for Education: 100% SVCF;
  - XQ Institute: 100% NPT;
  - RF Catalytic Capital: 100% GS DAPF;
  - Lakeview Health Foundation: 99% Saint Paul & Minnesota Foundation.
- By contrast, the large research universities draw on many sponsors: Johns Hopkins 29, Cornell 31, Harvard and Stanford 38 each.
- So recipient growth at the top mostly reflects a few large donor recommendations [I].

## 5. Limits
- **Coverage.** Itemised Schedule I only (grants over $5,000 per recipient). Six of the 50 sponsors do not itemise in FY2021–22, and four itemise only in FY2023–24; the balanced panel removes the coverage effect but omits those four.
- **Netting.** The repo's whitelist nets only DAFRC panel EINs. Lines to other DAF holders (e.g. Dayton Foundation Plus) stay in; the sensitivity bounds the effect (§3.3). Some kept lines to universities or religious bodies may fund their own DAFs; this cannot be seen in Schedule I.
- **No FY2021 DAF weighting.** The filed basis is used for trend and growth (§1.3).
- **Fiscal-year mixing.** FY = year the tax period ends, so June filers' FY2021 covers July 2020 to June 2021. A single gift can fall in different FYs at different sponsors.
- **EIN keys.** Recipients are counted by EIN as filed. Affiliates (university foundations and their universities, the CZ LLCs and Biohub) are separate unless merged in a sensitivity. Typo EINs split one organisation into two. Blank-EIN lines are keyed by name.
- **Classification is rule-based** on NTEE codes, which are assigned by the IRS or by NCCS and can be stale or broad. "Policy or advocacy" means an NTEE R/W-policy or 01 code, nothing more. The BMF is a 2026 snapshot, so it shows current, not historical, NTEE and ruling. Ruling dates can be retroactive or reflect a reorganisation rather than a new organisation.
- **No viewpoint characterisation** was made or intended. Mission descriptions are limited to NTEE codes.
- **Gini** is computed among recipients that received at least one itemised grant, so it understates inequality relative to all eligible charities.

## 6. Data dictionary: `recipient-concentration-growth-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_type | `concentration` or `grower` |
| scope | `all_itemising`, `balanced_panel`, or a sensitivity suffix `_cz_merged` / `_net_non_dafrc_daf_filers` |
| basis | `schedule_i` (filed $) or `daf_weighted` (× sponsor-year DAF share of grants) |
| fiscal_year | FY (concentration rows) |
| sponsor_years | itemising sponsor-years included |
| gross_sched_i_usd | all Schedule I lines before netting |
| d2d_excluded_usd | dollars netted out (repo rule, plus the sensitivity set where named) |
| total_usd | net dollars |
| recipients | recipients with positive net dollars |
| top10_share, top100_share, top1000_share | share of net dollars held by the N largest recipients |
| gini | Gini among recipients with positive dollars |
| hhi | Herfindahl index, 0–10,000 |
| top1_recipient | EIN (or name key) of the largest recipient |
| rank_list | `abs`, `pct`, `pct_p1_1m`, `entrant` (grower rows) |
| rank | rank within the list |
| ein, name_as_filed | recipient EIN; filed name carrying the most dollars |
| bmf_name, state, ntee_cd, subsection, foundation_code, ruling | IRS EO BMF fields (RULING = yyyymm) |
| ntee_major | NTEE major group (repo mapping) |
| is_new_org | 1 if RULING ≥ 202001 |
| org_type, org_type_basis | rule type of §1.7 and the rule that fired |
| is_fiscal_sponsor, fs_source | on the fiscal-sponsor list (`directory`, `q_b15`) or de-facto file (`de_facto_intermediary`) |
| is_intermediary | fiscal sponsor, pass-through intermediary or NTEE T |
| pass_through_class, pass_through_subtype | from pass-through-recipients-2026-11-20.csv |
| non_bmf_category | from non-bmf-recipients-2026-11-20.csv |
| usd_fy2021..usd_fy2024 | balanced-panel filed $ by FY |
| usd_p1, usd_p2, growth_usd, growth_pct | P1 = FY2021+22; P2 = FY2023+24; growth_pct blank when P1 = 0 |
| grantors_p1, grantors_p2 | distinct top-50 sponsors paying in each period |
| top_grantor_p2, top_grantor_share_p2 | largest P2 sponsor and its share of P2 |
| source | provenance string |

## 7. Reproduction

```
S=<scratch>
python3 scripts/mission_recipient_concentration.py . --np-cache $S/npcache --bmf-dir $S/rcp/bmf \
  --lines-cache $S/rcp/lines --lines-cache $S/q120201/lines --lines-cache $S/q2102/lines \
  --lines-cache $S/b51-02/lines [--fetch] --summary $S/b51-02/summary.json
```

## 8. Source register and access log

| Source | URL | Use |
|---|---|---|
| IRS Form 990 e-file XML, GivingTuesday mirror of IRS TEOS | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml (e.g. Fidelity Charitable FY2021: …/202221339349302787_public.xml; Schwab Charitable FY2021: …/202230499349301028_public.xml; SVCF FY2021: …/202223199349318287_public.xml) | Schedule I Part II lines, 182 returns |
| IRS TEOS e-file index (upstream of the netpayout990 cache) | https://apps.irs.gov/pub/epostcard/990/xml/2023/index_2023.csv | Object IDs (cached, not re-read) |
| IRS EO Business Master File | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf ; files https://www.irs.gov/pub/irs-soi/eo1.csv … eo4.csv, eo_pr.csv, eo_xx.csv | NTEE, subsection, ruling, foundation code (cached 2026-11-14, not re-read) |
| IRS EO BMF field definitions | https://www.irs.gov/pub/irs-soi/eo_info.pdf | Meaning of RULING, FOUNDATION, NTEE_CD |
| Repo files | daf-to-daf-recipient-whitelist.csv, sponsor-cost-structure.csv, dafrc-sponsor-schedule-d-fy2019-2024.csv, fiscal-sponsor-ein-list-2026-11-19.csv, de-facto-fiscal-sponsors-2026-11-20.csv, pass-through-recipients-2026-11-20.csv, non-bmf-recipients-2026-11-20.csv, non-dafrc-daf-filers-990.csv | Netting, weights, universe, lists |

**Robots and access log (2026-11-20).**
- `gt990datalake-rawdata.s3.amazonaws.com/robots.txt` returned HTTP 404 at 16:16 UTC, so no rules apply (as in earlier repo notes). It was the only host fetched.
- User agent: `research-script/1.0 (stdlib urllib)`.
- No sec.gov, no logins, no forms. No fiscal-sponsor or Charity Navigator site was contacted.
