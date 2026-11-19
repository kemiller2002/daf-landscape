# P-B4531-01-03: DAF money reaching abroad through large recipients outside NTEE Q, FY2023–FY2024

**Date:** 2026-11-19 · **Queue item:** P-B4531-01-03 (proposed in [b45n31-01-daf-money-abroad.md](b45n31-01-daf-money-abroad.md) §4 limit 3)

**Outputs**
- [`data/mission-2026-11-14/non-q-foreign-spending-2026-11-19.csv`](../../data/mission-2026-11-14/non-q-foreign-spending-2026-11-19.csv): 1,028 rows. There are 500 recipient rows, 215 summary rows, 7 component rows, 20 comparison rows, 28 region rows, 196 region-by-NTEE rows, 16 combined-region rows and 46 sponsor rows.
- [`data/mission-2026-11-14/queue-proposals-b4531-01-03.csv`](../../data/mission-2026-11-14/queue-proposals-b4531-01-03.csv): 5 follow-up items.
- **Script:** [`scripts/mission_non_q_foreign.py`](../../scripts/mission_non_q_foreign.py). It imports `mission_daf_money_abroad.py` and uses its `measures`, `estimate`, `recipient_row`, `summary_row`, `region_rows`, `sponsor_rows`, `target_lines` and `inbound` unchanged. The base script was not modified. Stdlib only, functional style.

**Rules applied**
- **Prior work read first:** the P-B45N31-01 document, including its wave-37A corrections. These are: the $1.868bn top-150 figure; the AIEF Schedule F caveat; the note that 11 of the top 150 are DAFRC-panel sponsors; the untested ranks 151+; and the Friends of the IDF timing example. This run inherits all of them.
- **Allocation is [I]:** each recipient's in-year foreign share is applied to the DAF dollars it received, exactly as in the base run.
- **Recency:** recipients' own returns for tax periods ending in 2023 and 2024.
- **robots.txt:** `gt990datalake-rawdata.s3.amazonaws.com/robots.txt` returned HTTP 404 on 2026-11-19, which means no rules. It was checked again for this run and logged. Nothing else was fetched.
- **User agent:** `research-script/1.0`. No outreach.
- **Cache reuse:** the 291 cached returns in `q3101/ext` were copied, not moved, into this run's cache. None of them was needed, because they belong to the top-150 recipients, which this run excludes. 850 new returns were fetched.
- **Evidence tags:**
  - [F] filed figure;
  - [C] computed here;
  - [I-alloc] DAF dollars × the recipient's filed foreign share (the proportional assumption);
  - [I-extrap] extrapolation beyond recipients whose returns were read.

## 0. Headline answers

Scope: the same as the base run. Top-50 sponsors excluding the two university/hospital sponsors; 90 itemising sponsor-years; net Schedule I $77.13bn. Dollars are FY2023–24 pooled.

| Question | Answer |
|---|---|
| **New DAF money abroad via the 458 largest non-Q, non-sponsor recipients** | **$1.347bn** central [I-alloc on F/C shares].<br>- FY2023 $478.7m; FY2024 $868.1m.<br>- Floor (line 3 ÷ total expenses): $945.1m. High (line 3 ÷ lines 1–3): $2.176bn.<br>- DAF-weighted: $1.318bn. |
| **Share of their inbound** | **5.9%** of $22.646bn [C].<br>- **7.6%** of the $17.702bn received by the 387 that file a Form 990.<br>- For comparison, the Q/friends top 150 sent 58.8% abroad. |
| **Concentration** | - The 10 largest account for 42.8% of the $1.347bn and the 25 largest for 65.8%.<br>- 188 of the 387 parsed recipients report no foreign spending. |
| **By NTEE major group** | - **C Environment $250.1m** (15.7% of inbound);<br>- **T Philanthropy/grantmaking $248.9m** (12.8%);<br>- **B Education $206.1m** (4.2% of $4.95bn);<br>- P Human Services $147.5m (12.2%);<br>- X Religion $92.0m (6.7%);<br>- U Science $81.1m;<br>- E Health $66.1m (3.7%) [I-alloc]. |
| **Where it goes** | - **Europe 42.1%**;<br>- Sub-Saharan Africa 17.4%;<br>- East Asia and Pacific 10.5%;<br>- Middle East and North Africa 8.3%;<br>- South America 6.4%;<br>- North America 5.1%. |
| **Combined share of total grants** (sponsors' lines 1–3, $98.27bn) | - Direct line 3: **1.92%** [F].<br>- + Q/friends top 150: **3.82%** [I-alloc].<br>- + non-Q 500: **5.20%** ($5.105bn) [I-alloc]. This is the measured headline.<br>- With [I-extrap] for recipients not read: 6.15% → 6.53% → **8.41%**.<br>- On the itemising base (net Schedule I + line 3): 2.39% → 4.74% → **6.44%** measured, 10.42% [I-extrap]. |
| **DAF sponsors among the 500** (reported separately) | - 42 recipients, $6.460bn inbound, **$187.4m abroad** (2.9%).<br>- Largest: Johns Hopkins $58.3m, Rockefeller Philanthropy Advisors $47.0m, Nature Conservancy $18.8m, Global Greengrants Fund $18.5m.<br>- Adding them would give 5.39%. |

**Reading [I].** Large recipients outside the Q / friends-of frame add about 72% as much as the 150 Q / friends recipients of the base run ($1.347bn vs $1.868bn), on seven times the inbound. Their foreign share is low (6–8% vs 59–62%), but they are much larger. Measured DAF money reaching abroad rises from 3.8% to 5.2% of total grants. This is 2.7 times the direct share.

## 1. Method

1. **Schedule I lines.** The step is identical to the base run and re-run in the new script:
   - top-50 DAFRC sponsors;
   - one return per sponsor × FY;
   - itemising sponsor-years only;
   - university/hospital sponsors excluded;
   - totals rows dropped;
   - DAF-to-DAF lines (batch-34 whitelist, self-lines) dropped.
   - Net Schedule I is $77,131,527,070, identical to the base run [C].
2. **Excluding the Q/friends top 150.** The base frame was rebuilt with the base script's own `target_lines`, `inbound` and ranking. It matches the 150 recipient EINs in `daf-money-abroad-2026-11-19.csv` exactly (`frame_check`: equal, 0 differences) [C]. Those 150 EINs are removed from the pool.
3. **Ranking.** All other net recipients with an EIN (170,393) are ranked by pooled FY2023–24 net inbound. The largest 500 are kept.
   - They received **$29.106bn**, 37.7% of net Schedule I.
   - The 500th received $16.16m.
   - Recipients beyond rank 500 received $44.416bn, and blank-EIN non-Q lines $431.2m.
4. **Groups.** Each of the 500 is in exactly one group:
   - **`dafrc_sponsor` (42):** the EIN, or a unique normalised Schedule I / BMF name, is in the DAFRC sponsor panel (1,594 EINs, any segment). These hold DAFs themselves, so part of their inbound may sit in a DAF before moving on. They are reported separately and never included in the headline. One match is by name only.
   - **`q_friends_rest` (0):** Q or friends-of recipients ranked 151+ in the base frame. None reach the 500 cut-off: the 150th of the base frame received $4.58m, so rank 151 received at most that, against the $16.16m cut-off here. All $1.519bn of the base run's remaining Q/friends inbound therefore stays in its [I] extrapolation, unchanged.
   - **`non_q` (458):** all other recipients. This is the new money.
   - **Second sponsor test, from the recipient's own return:** Form 990 Part IV line 6 (`DonorAdvisedFundInd`, "did the organization maintain any donor advised funds"). It is read from the same e-file XML (850 returns, 0 failures). 11 non-Q recipients answer Yes ($973.8m inbound, $20.1m abroad), for example UJA-Federation of New York, Founders Pledge, Hopewell Fund and Princeton. They are kept in non-Q and flagged (`own_daf_ind`). A strict variant drops them.
5. **Returns and shares.** These steps are as in the base run:
   - Filings come from the IRS TEOS index CSVs: the latest object id per tax period, FY = the year the period ends.
   - Parsing uses `mission_foreign_grants.load_extract`.
   - Shares come from `mission_daf_money_abroad.measures` and `estimate`:
     - central = min(line 25, max(line 3, Schedule F Part I non-investment)) ÷ line 25;
     - floor = line 3 ÷ line 25;
     - high = line 3 ÷ lines 1–3.
   - Each FY's inbound is multiplied by that FY's share. If one FY's return is missing, the other FY's share is borrowed; this happened for 6 non-Q recipients.
   - Coverage: 850 returns parsed and 1 Form 990-EZ (Leadership Network, FY2023), with no filer-EIN mismatches. 72 of the 500 have no Form 990 in the index for either year.
6. **Regions.** Schedule F Part I non-investment rows are used, falling back to Parts II + III, normalised with `region_of`, as in the base run.
   - Rows are produced by NTEE major group (EO BMF `NTEE_CD` first letter) and by major group × region.
   - Combined regions add this run's non-Q dollars to the base run's `region_combined` rows (direct Schedule F Part II + top 150).
7. **Combined share.** The direct-route and base figures are read from the two existing CSVs, not recomputed:
   - direct line 3 $1.891bn; lines 1–3 $98.27bn; itemising base $79.23bn;
   - top-150 $1.868bn; top-150 share 61.68%.
   - Each component is a separate `component` row tagged F, I-alloc or I-extrap, and cumulative `comparison` rows follow.
8. **Cap check.** In 2 recipient-years Part I or line 3 exceeds total expenses, so the central share is capped at 100%:
   - Wesleyan University FY2023: a $444.0m "Program services" row for Central America and the Caribbean, against $352.2m of total expenses. It looks like a mislabelled offshore-investment row.
   - Yad Eliezer FY2023.
   - Re-scoring these years at line 3 ÷ line 25 lowers non-Q by $11.1m, to $1.336bn (`abroad_expense_cap_adj_usd`; comparison row `sensitivity_non_q_capped_years_at_line3`).
9. **Determinism.** Two consecutive offline runs gave byte-identical CSVs [C].

## 2. Results

### 2.1 Totals [C; dollars abroad are I-alloc]

| Scope | Recipients | Inbound $m | Abroad central $m | Share | Floor $m | High $m |
|---|---|---|---|---|---|---|
| All 500 | 500 | 29,105.8 | 1,534.2 | 5.3% | 1,057.8 | 2,604.4 |
| **Non-Q (headline)** | **458** | **22,645.6** | **1,346.8** | **5.9%** | 945.1 | 2,176.4 |
| … with a Form 990 | 387 | 17,702.4 | 1,346.8 | 7.6% | | |
| … no Form 990 | 71 | 4,943.2 | 0 (measured) | — | | |
| … own Part IV line 6 = Yes | 11 | 973.8 | 20.1 | 2.1% | | |
| … strict, excluding those | 447 | 21,671.8 | 1,326.7 | 6.1% | | |
| DAFRC sponsors (separate) | 42 | 6,460.3 | 187.4 | 2.9% | 112.7 | 427.9 |
| … university/hospital segment | 28 | 5,757.9 | 94.7 | 1.6% | | |
| … national segment | 4 | 345.6 | 54.3 | 15.7% | | |
| … single-issue segment | 10 | 356.8 | 38.4 | 10.8% | | |

**By year (non-Q):**
- Inbound: FY2023 $11.280bn; FY2024 $11.366bn.
- Abroad: $478.7m and $868.1m.
- The FY2024 rise comes from a few recipients. ClimateWorks Foundation went from $7.4m to $72.9m on inbound of $17.4m and $152.2m. The Clear Fund (GiveWell) went from $15.9m to $65.0m. The US Olympic and Paralympic Foundation went from $0.0m to $24.1m (Europe; FY2024 is the Paris 2024 year [I]).

**Share bands (non-Q, central, by recipient):**
- ≥ 90%: 3 recipients, $67.1m inbound;
- 50–90%: 17 recipients, $757.1m inbound, $496.0m abroad;
- 10–50%: 41 recipients, $2,010.2m inbound, $613.0m abroad;
- < 10%: 326 recipients, $14,868.0m inbound, $172.4m abroad;
- no Form 990: 71 recipients, $4,943.2m inbound.

### 2.2 By NTEE major group (non-Q) [I-alloc]

| Major group | Recipients | Inbound $m | Abroad $m | Share |
|---|---|---|---|---|
| C Environment | 25 | 1,589.1 | 250.1 | 15.7% |
| T Philanthropy, Voluntarism and Grantmaking | 36 | 1,943.4 | 248.9 | 12.8% |
| B Education | 119 | 4,952.1 | 206.1 | 4.2% |
| P Human Services | 27 | 1,212.8 | 147.5 | 12.2% |
| X Religion-Related | 22 | 1,377.3 | 92.0 | 6.7% |
| U Science and Technology | 7 | 1,682.6 | 81.1 | 4.8% |
| E Health Care | 39 | 1,766.3 | 66.1 | 3.7% |
| A Arts, Culture and Humanities | 19 | 909.0 | 40.8 | 4.5% |
| No NTEE code (name-classified; mostly unclassified) | 56 | 3,267.5 | 44.1 | 1.3% |
| D Animal-Related | 4 | 94.3 | 33.8 | 35.8% |
| R Civil Rights, Social Action and Advocacy | 18 | 701.5 | 33.1 | 4.7% |
| N Recreation and Sports | 4 | 105.4 | 27.7 | 26.3% |
| S Community Improvement | 14 | 367.3 | 21.4 | 5.8% |
| K Food and Agriculture | 8 | 288.7 | 16.4 | 5.7% |
| H Medical Research | 4 | 257.9 | 13.1 | 5.1% |
| G Diseases and Disorders | 5 | 215.1 | 11.9 | 5.5% |
| Other (O, V, W, J, Z, I, M, F, L) | 51 | 1,915.2 | 12.6 | 0.7% |

Group rows and NTEE subgroups (first three characters) are in the CSV (`row_type_detail` = `ntee_major`, `ntee_subgroup`).

**Notable subgroups:**
- T30 (grantmaking public foundations, e.g. The Clear Fund) $118.0m;
- X20 (Christian, e.g. Samaritan's Purse) $83.0m;
- C30 (natural-resource conservation) $82.0m;
- U12 (ClimateWorks) $80.3m;
- T20 (private grantmaking) $79.6m;
- P60 (GiveDirectly) $72.7m;
- B43 (universities, 30 recipients, $1.751bn inbound) $68.5m (3.9%).

**Universities with foreign campuses (non-Q, not DAFRC sponsors)** [F shares; I-alloc dollars; campus names are context, not read from the returns]:
- Cornell (Weill Cornell Medicine–Qatar, MENA Part I $155–157m a year): share 3.3%, $10.2m abroad of $308.8m inbound.
- New York University (Abu Dhabi, Europe and Shanghai sites; Part I $583–642m pooled): 3.0%, $2.5m of $83.4m.
- Georgetown (Qatar): 7.3%, $4.7m.
- Carnegie Mellon (Qatar): 6.8%, $1.9m.
- Duke (Kunshan, East Asia and Pacific): 1.3%, $2.2m.
- Northwestern (Qatar) is a DAFRC-panel sponsor, so it is in the separate group ($2.1m).
- All 86 university/college-named or B4x non-Q recipients together: $3.891bn inbound and $140.4m abroad (3.6%). The largest share is the Kyiv School of Economics ($49.8m, 85%).

### 2.3 Largest non-Q pass-through recipients [F/C; I-alloc]

| Rank | Recipient | NTEE | Inbound $m | Central share | Abroad $m | Main region |
|---|---|---|---|---|---|---|
| 23 | The Clear Fund (GiveWell) | T30 | 182.7 | 45.9% | 80.9 | Europe |
| 25 | ClimateWorks Foundation | U12 | 169.5 | 45.5% | 80.3 | Europe |
| 54 | GiveDirectly | P60 | 96.6 | 77.0% | 72.7 | Sub-Saharan Africa |
| 40 | Samaritan's Purse | X20 | 129.3 | 54.4% | 70.2 | Sub-Saharan Africa |
| 69 | Jeremy and Hannelore Grantham Environmental Trust | T20 | 84.2 | 65.6% | 57.5 | Europe |
| 14 | Climate Imperative Foundation | C12 | 247.1 | 24.1% | 56.9 | Europe |
| 96 | Kyiv School of Economics | B40 | 59.6 | 85.0% | 49.8 | Europe |
| 8 | New Venture Fund | C05 | 431.9 | 9.5% | 43.0 | Europe |
| 82 | RF Catalytic Capital | T30 | 70.0 | 52.6% | 36.5 | Europe |
| 141 | Friends of United Hatzalah | A70 | 41.9 | 84.1% | 28.9 | MENA |
| 95 | Breakthrough Energy Catalyst Foundation | C35 | 60.0 | 41.7% | 28.7 | Europe |
| 90 | Partners In Health | E70 | 65.6 | 23.0% | 15.1 | Central America/Caribbean |

Shares are pooled over the two returns; dollars use each year's own share. Rank is within the 170,393-recipient pool outside the top 150.

**Brief examples:**
- **Global Greengrants Fund (C12)** is a DAFRC-panel sponsor: $18.5m abroad of $27.9m.
- **Global Fund for Children (A33Z)** ranks 791st ($11.2m inbound), so it is outside the 500.
- **CAF America** is on the DAF-to-DAF whitelist, so its inbound is not net Schedule I at all. It never enters this frame.
- Friends of United Hatzalah is coded A70 but named "Friends of", which the base FRIENDS pattern does not match (no country word).

### 2.4 Regions [I-alloc]

| Region | Non-Q $m | Non-Q share | Direct + top 150 $m (base) | Combined $m | Combined share |
|---|---|---|---|---|---|
| Europe | 567.6 | **42.1%** | 1,185.1 | 1,752.8 | 34.3% |
| Sub-Saharan Africa | 233.7 | 17.4% | 773.7 | 1,007.4 | 19.7% |
| Middle East and North Africa | 111.5 | 8.3% | 691.1 | 802.6 | 15.7% |
| East Asia and the Pacific | 141.7 | 10.5% | 201.4 | 343.2 | 6.7% |
| South Asia | 45.8 | 3.4% | 268.7 | 314.5 | 6.2% |
| South America | 86.8 | 6.4% | 217.3 | 304.1 | 6.0% |
| North America (Canada, Mexico) | 68.1 | 5.1% | 163.2 | 231.3 | 4.5% |
| Russia and the NIS | 26.5 | 2.0% | 122.3 | 148.9 | 2.9% |
| Central America and the Caribbean | 47.1 | 3.5% | 95.6 | 142.7 | 2.8% |
| Unmapped / unspecified | 18.0 | 1.3% | 40.1 | 58.1 | 1.1% |

**Region mix within each NTEE major group:**
- B Education: 62.9% Europe (Oxford, Kyiv School of Economics, Minerva), with MENA campuses 7.4%.
- C Environment: 49.1% Europe, 16.1% East Asia and Pacific, 15.9% South America.
- T Grantmaking: 58.4% Europe, 14.4% Sub-Saharan Africa.
- P Human Services: 56.3% Sub-Saharan Africa (GiveDirectly) and 22.6% MENA.
- X Religion: 35.8% Sub-Saharan Africa and 16.1% MENA.
- E Health: 39.7% Sub-Saharan Africa and 18.7% Central America/Caribbean.

**[I] Interpretation:**
- The non-Q route looks like the direct route: about 42% Europe. Much of it is climate and effective-altruism grantmakers re-granting to European-registered bodies.
- The Q route, by contrast, is Africa- and MENA-heavy.
- Adding non-Q dollars raises Europe's combined share from 31.5% (base run, direct + top 150) to 34.3%.

### 2.5 Combined share of total grants [F / I-alloc / I-extrap kept separate]

| Step | Tag | Adds $bn | Cumulative $bn | Share of lines 1–3 ($98.27bn) | Share of itemising base ($79.23bn) |
|---|---|---|---|---|---|
| Direct, sponsors' Part IX line 3 | F | 1.891 | 1.891 | 1.92% | 2.39% |
| + Q/friends top 150 (base run) | I-alloc | 1.868 | 3.759 | 3.82% | 4.74% |
| **+ non-Q 500 (this run)** | I-alloc | **1.347** | **5.105** | **5.20%** | **6.44%** |
| + Q/friends ranks 151+ and 3 top-150 non-filers at 61.68% | I-extrap | 0.937 | 6.042 | 6.15% | 7.63% |
| + non-Q in the 500 with no Form 990 ($4.943bn) at the non-Q share 7.61% | I-extrap | 0.376 | 6.418 | 6.53% | 8.10% |
| + non-Q beyond rank 500 ($42.846bn incl. blank-EIN lines) at the share of the last 100 parsed non-Q ranks, 4.30% | I-extrap | 1.842 | 8.260 | 8.41% | 10.42% |

**Sensitivities on the measured 5.20%:**
- Adding the 42 DAFRC sponsors gives 5.39%.
- Dropping the 11 non-Q recipients with their own DAFs gives 5.17%.
- Re-scoring the 2 capped years gives 5.18%.

**Not added:** the base run's $58.8m "named intermediaries outside the frame" (CAF America, Global Greengrants, Global Fund for Children). Global Greengrants is measured here in the sponsor group, Global Fund for Children is outside the 500, and CAF America is a whitelisted DAF-to-DAF recipient. Adding that row as well would count Greengrants twice.

**Reading [I]:**
- The measured figure (5.20%; 6.44% on the itemising base) is now close to the 7.83% "every Q recipient + direct" bound that the base run called about 2 points too high. Its meaning is different, though: the earlier bound counted all Q inbound as foreign, while this one counts only filed foreign spending.
- The last extrapolation step is the weakest. It applies a 4.3% share to $42.8bn spread over about 170,000 smaller recipients, most of them local schools, churches, hospitals and US charities. A zero-to-4.3% range on that step (5.20%/6.53% to 8.41%) is the honest statement.

### 2.6 Which sponsors route money abroad through non-Q recipients [I-alloc]

Non-Q pass-through compared with each sponsor's own line 3 (FY2023–24):
- Fidelity Charitable $310.0m (direct $114.2m);
- NPT $224.9m (direct $742.8m);
- Vanguard Charitable $172.7m (direct $11.0m);
- Goldman Sachs Philanthropy Fund $168.2m (direct $179.8m);
- SVCF $103.7m (direct $352.4m);
- DAFgiving360 $84.2m (direct $108.2m);
- NCF $48.6m (no direct);
- Chicago Community Trust $48.3m;
- Morgan Stanley GIFT $47.8m.

The 46 sponsor rows sum to $1,346.8m.

## 3. Limits

1. **Proportional allocation [I-alloc].** Each recipient's average foreign share is applied to its DAF dollars. This matters more here than for Q recipients. A DAF grant to a university or a fiscal sponsor (New Venture Fund, Windward, Hopewell) is usually earmarked for a specific programme or project, whose foreign share may be zero or 100%. Timing is ignored, as in the base run.
2. **Recipients with no Form 990 count as zero in the measured figure.** There are 71 non-Q recipients with $4.943bn inbound. They include:
   - four Chan Zuckerberg Biohub / Institute LLCs ($1.657bn);
   - The Church of Jesus Christ of Latter-day Saints entities ($465.6m + $32.4m);
   - Campus Crusade for Christ (Cru) $96.0m;
   - Wycliffe Bible Translators $44.4m;
   - Salvation Army entities;
   - Catholic Relief Services $40.8m;
   - state universities and hospitals that file no 990 (University of Michigan, UT Austin, Mayo Clinic).

   Some of these, notably CRS, Cru, Wycliffe and LDS humanitarian work, spend heavily abroad. The [I-extrap] step at 7.6% may understate them, and it overstates the CZ Biohubs. The Chicago Community Foundation line ($38.2m, no 990 under that EIN) looks like a DAF sponsor that neither test catches.
3. **DAF-sponsor tests are partial.**
   - The DAFRC panel catches 42 recipients.
   - Part IV line 6 catches 11 more among non-Q.
   - Some re-granting platforms answer No to Part IV line 6 and stay in non-Q: Bright Funds Foundation ($19.8m abroad), Gates Philanthropy Partners ($16.2m) and RF Catalytic Capital ($36.5m). They are pass-through vehicles, but not DAF sponsors on the filed test.
4. **Schedule F Part I is self-labelled.**
   - The investment exclusion is the base script's text rule. Wesleyan's capped row shows that "Program services" can hide investments; the cap sensitivity covers the two years where this binds.
   - Caltech reports $58–98m a year of Europe "Program services" (central share 2.5%, $6.1m abroad). It was not verified.
   - Non-Q recipients' Part I investment rows total $136.8bn pooled and are excluded; almost all of this is university endowments.
5. **Universities' foreign campuses may sit in related entities.** Examples are NYU Abu Dhabi and Weill Cornell–Qatar. Where a campus is a separate legal entity, its spending appears on Schedule R, not Schedule F Part I, so university shares may be understated.
6. **Double counting.** Each DAF dollar is counted once, at its first recipient, and only to the extent that recipient reports foreign spending.
   - A non-Q grantmaker's grants to a US Q organisation (for example a grant from The Clear Fund to a US-registered charity) are domestic grants (line 1) on its return, so they are not counted in its share.
   - The two routes cannot overlap at the sponsor.
   - The Q/friends top 150 are excluded by EIN, and the excluded set matches the base CSV exactly.
   - The 42 DAF sponsors are excluded from the headline, so the only overlap risk is the sensitivity row that adds them.
7. **FY2024 completeness.** FY2024 returns come from index files to 2026. Six non-Q recipients borrow the other year's share.
8. **Frame.**
   - The 500 cut-off ($16.16m) leaves $42.8bn of non-Q inbound unread.
   - Recipients ranked 501–1,000 include known international operators: Global Fund for Children is 791st.
   - Ranks 151+ of the Q/friends frame are still extrapolated, not measured; no Q/friends recipient beyond 150 reaches $16.16m.
9. **Mixed denominator.** As in the base run, the numerator is net of DAF-to-DAF, while lines 1–3 are gross.

## 4. Data dictionary — `non-q-foreign-spending-2026-11-19.csv`

All columns of `daf-money-abroad-2026-11-19.csv` keep the meaning given in [b45n31-01-daf-money-abroad.md §5](b45n31-01-daf-money-abroad.md). The additions and changes are below.

| Column / value | Meaning |
|---|---|
| row_type | One of the following: `summary`; `component` (one addition to the combined share); `comparison` (cumulative or sensitivity share; `itemising_` prefix = net Schedule I + line 3 base); `region`; `region_by_ntee` (scope = NTEE major letter); `region_combined` (direct Part II + top 150 + non-Q); `sponsor` (non-Q pass-through by top-50 sponsor); `recipient` |
| group | `non_q`, `q_friends_rest`, `dafrc_sponsor`, or `all` |
| ntee_major | IRS EO BMF NTEE_CD first letter; `(no NTEE: <sector>)` when there is no code, with the name-based sector of `mission_recipient_sectors.classify` |
| ntee_major_name | NCCS NTEE major-group label for the letter |
| own_daf_ind | Recipient's own Form 990 Part IV line 6 (`DonorAdvisedFundInd`) on either FY return: 1 Yes, 0 No, blank if not read |
| cap_bound_fys | FYs where max(line 3, Schedule F Part I non-investment) > line 25, so the central share was capped at 100% |
| abroad_expense_cap_adj_usd | Central estimate with capped years re-scored at line 3 ÷ line 25 |
| evidence | `F`, `I-alloc` or `I-extrap` (component, comparison and region rows); recipient rows read "F (inbound, Part IX, Sched F) / I-alloc (abroad_*)" |
| selection_basis | `other` for non-Q recipients (`q`/`friends`/`q+friends` would mark Q/friends) |
| segment | DAFRC segment for `dafrc_sponsor` recipients and sponsor rows |
| rank | Recipient rank in the pool outside the top 150 (1 to 500), by pooled net inbound |
| summary scopes | `top500_all_groups`; `non_q`, `q_friends_rest`, `dafrc_sponsor` and their `_with_form990` variants; `non_q_own_part_iv_l6_yes`; `non_q_excl_own_part_iv_l6_yes`. Group summaries carry `row_type_detail` = `ntee_major`, `ntee_subgroup`, `dafrc_segment` or `share_band` |
| component / comparison scopes | `direct_line3`, `plus_top150_q_friends`, `plus_non_q_measured`, `plus_q_friends_rest_measured`, `plus_q_friends_remainder_extrap`, `plus_non_q_no990_extrap`, `plus_non_q_beyond_top_extrap` (comparison rows prefixed `cum_`); `sensitivity_plus_dafrc_sponsors`, `sensitivity_non_q_capped_years_at_line3`, `sensitivity_strict_excl_own_daf_holders` |
| denominator_usd, share_of_denominator, note | Base of the share and its value; `note` gives the inputs of each extrapolation |

## 5. Source register

| # | Source | URL | Accessed | robots.txt |
|---|---|---|---|---|
| S1 | IRS Form 990 e-file XML for 428 recipients, 850 returns (Part IV line 6, Part IX, Schedule F), GivingTuesday mirror of IRS TEOS. Object ids are in the recipient rows | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | 2026-11-19 | 404, no rules (checked and logged 2026-11-19) |
| S2 | IRS TEOS e-file index CSVs 2023–2026 (scratch copies) | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (one per year) | earlier batch | not re-fetched |
| S3 | IRS EO BMF eo1–eo4, eo_pr, eo_xx (2026-11 snapshot, scratch copy) | https://www.irs.gov/pub/irs-soi/eo1.csv | earlier batch | not re-fetched |
| S4 | Form 990 instructions (Part IV line 6; Schedule F Part I) | https://www.irs.gov/pub/irs-pdf/i990.pdf ; https://www.irs.gov/pub/irs-pdf/i990sf.pdf | not fetched in this run (definitions only) | — |
| S5 | NTEE major-group labels (NCCS) | https://urbaninstitute.github.io/nccs-legacy/ntee/ntee.html | not fetched in this run (labels only) | — |
| S6 | Base run and frame: `data/mission-2026-11-14/daf-money-abroad-2026-11-19.csv` (P-B45N31-01, V wave 37A) | repo | — | — |
| S7 | Direct route: `data/mission-2026-11-14/daf-foreign-grants-schedule-f-2023-2024.csv` (P-NEW-FGN-01) | repo | — | — |
| S8 | `dafrc-sponsor-schedule-d-fy2019-2024.csv` (DAFRC panel), `daf-to-daf-recipient-whitelist.csv`, `sponsor-cost-structure.csv`, top-50 Schedule I line cache | repo / via S1 | — | — |

## 6. Reproduction

```
S=<scratchpad>
python3 scripts/mission_non_q_foreign.py . --np-cache $S/npcache --lines-cache $S/rcp/lines --bmf-dir $S/rcp/bmf \
    --index-dir $S/irs --extract-cache $S/q3113/ext --daf-cache $S/q3113/dafind [--fetch] [--workers 8] [--top 500]
```

- The cold run (850 returns, twice: extract and Part IV line 6) takes about 50 s per pass. The warm run takes about 25 s.
- The script writes the CSV and prints JSON with these fields: `frame_check`, `groups`, `filings`, `named_intermediaries`, `cap_bound`, `inputs`, `summary`, `comparison`, `regions`, `sponsors` and `recipients`.
- Every figure above comes from that output or the CSV. Ratios such as 2.7× and 37.7% are arithmetic on it.
