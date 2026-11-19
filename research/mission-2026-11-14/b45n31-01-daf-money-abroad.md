# P-B45N31-01: how much DAF money ends up abroad through US-registered recipients, FY2023–FY2024

**Date:** 2026-11-19 · **Queue item:** P-B45N31-01 (extends the nine-intermediary pass-through in [direction-foreign-grants-schedule-f.md](direction-foreign-grants-schedule-f.md) §3.5)

**Outputs**
- [`data/mission-2026-11-14/daf-money-abroad-2026-11-19.csv`](../../data/mission-2026-11-14/daf-money-abroad-2026-11-19.csv): 273 rows. There are 150 recipient rows, 41 summary rows, 9 comparison rows, 14 region rows, 14 combined-region rows and 45 sponsor rows.
- [`data/mission-2026-11-14/queue-proposals-b45n31-01.csv`](../../data/mission-2026-11-14/queue-proposals-b45n31-01.csv): 5 follow-up items.
- **Script:** [`scripts/mission_daf_money_abroad.py`](../../scripts/mission_daf_money_abroad.py). It is stdlib only and written in a functional style. It reuses the line handling of `mission_exception_load.py` and the extractor of `mission_foreign_grants.py`.

**Rules applied**
- **Prior work read first:**
  - The direction file, including its wave-30 corrections. Those corrections touch only the ED/ER row and the "understated by" wording; neither changes an input used here.
  - The P-NEW-FGN-01 intermediary rows.
- **Recency:** recipients' own returns cover tax periods ending in 2023 and 2024. FY is the calendar year in which the tax period ends, the same convention as the sponsors.
- **robots.txt:** `gt990datalake-rawdata.s3.amazonaws.com/robots.txt` returned HTTP 404 on 2026-11-19, which means no rules. Nothing else was fetched. The IRS index CSVs and the EO BMF are earlier scratch copies.
- **User agent:** `research-script/1.0`. No outreach.
- **Evidence tags:** [F] filed figure; [C] computed here; [I] inference or extrapolation.

## 0. Headline answers

Main scope: top-50 sponsors excluding the two university/hospital sponsors, the same scope as the $1.89bn direct figure. There are 90 itemising sponsor-years. Dollars are FY2023–24 pooled.

| Question | Answer |
|---|---|
| **DAF dollars reaching abroad via the 150 largest Q / friends-of recipients** | **$1.868bn** [C for the arithmetic; allocating DAF dollars at each recipient's average foreign-expense share is an assumption, I]. [V wave 37A]<br>- FY2023 $865.4m; FY2024 $1,002.3m.<br>- Bounds on other share definitions: floor $1.341bn (foreign grants only, line 3 ÷ total expenses); high $2.321bn (line 3 ÷ lines 1–3, the P-NEW-FGN-01 intermediary basis).<br>- DAF-weighted: $1.801bn. |
| **Share of their inbound DAF dollars** | **58.8%** of $3.179bn inbound [C].<br>- The 147 recipients that file a Form 990: **61.7%**.<br>- Three church-affiliated recipients file no 990 (Compassion International, OneHope, Convoy of Hope; $150.5m inbound). They count as zero here. |
| **Where it goes** (central estimate, Schedule F Part I) | - **Sub-Saharan Africa 35.2%**;<br>- Middle East and North Africa 24.5%;<br>- Europe 13.2%;<br>- South Asia 6.4%;<br>- Russia/NIS 6.2%;<br>- East Asia and Pacific 4.8%;<br>- Central America/Caribbean 4.2%;<br>- South America 2.8%;<br>- North America 2.2% [C].<br><br>The direct route is 49.6% Europe. |
| **Combined with the direct route** ($1.891bn, 1.92% of total grants) | **Measured:** direct + top-150 = **$3.759bn = 3.82% of total grants** (lines 1–3). That is **double the direct share** [C].<br>- Adding the P-NEW-FGN-01 pass-through of the three named intermediaries outside the Q/friends frame (CAF America, Global Greengrants, Global Fund for Children; $58.8m) gives 3.88%.<br>- **Extrapolated [I]:** with the remaining Q/friends inbound ($1.519bn) at the top-150 share, $4.695bn = **4.78%**.<br>- On P-NEW-FGN-01's net Schedule I + line 3 base: 2.39% direct → **4.74%** measured → **5.93% [I]**. The 7.83% "NTEE Q + direct" upper bound is therefore about 2 points too high as a measure of money leaving the US. |
| **Which sponsors rely on the indirect route** | Top-150 pass-through (central) compared with each sponsor's own line 3:<br>- **Fidelity** $456.2m (4.0× its direct $114.2m);<br>- **Vanguard** $161.8m (14.8× its direct $11.0m);<br>- DAFgiving360 $217.2m (2.0×);<br>- NCF $95.2m (no direct foreign grants);<br>- NPT $182.5m (0.25×) [C]. |

## 1. Method

1. **Schedule I lines.** The universe, return choice and lines are exactly those of `mission_exception_load.py`:
   - top-50 DAFRC sponsors by FY2024 DAF assets;
   - one return per sponsor × FY (`mission_daf_to_daf.pick_returns`);
   - itemising sponsor-years only;
   - filer totals rows dropped (`drop_totals_rows`, V wave 32A);
   - DAF-to-DAF lines (batch-34 whitelist, self-lines, whitelisted blank-EIN names) flagged by `mission_recipient_sectors.annotate` and excluded.
   - The main scope drops the university/hospital segment, which leaves 90 sponsor-years.
   - Net Schedule I comes to $77.13bn. P-NEW-FGN-01 had $77.34bn; the difference is the totals rows ($212m) [C].
2. **Targets.** A target is a recipient EIN that meets either test:
   - its IRS EO BMF `NTEE_CD` major group is Q; or
   - its Schedule I name or BMF name matches the `FRIENDS` pattern of `mission_foreign_grants.py`. The pattern covers "American/US friends of", "American Committee/Associates for the", and "Friends of … Israel/Jerusalem/…".
   - **Counts:** 5,420 recipient keys with $4.547bn of net inbound. Two have blank EINs ($18k).
   - **Ranking:** by pooled net inbound, keeping the top 150. These received $3.179bn, 69.9% of target inbound. The 150th received $4.58m.
   - **Composition of the 150:** 133 Q only, 9 Q and friends, 8 friends only (non-Q codes B11, B43, T30, P20, G90, B58 and one with no NTEE).
3. **Recipient returns.**
   - Each target's Form 990 filings are found in the IRS TEOS index CSVs (`index_2023`–`index_2026`). The latest object id per tax period is used; for each FY, the latest tax period ending in that year.
   - Returns are parsed with `mission_foreign_grants.load_extract`, streamed from the GivingTuesday mirror. The parser reads Part IX lines 1, 2, 3 and 25 (column A) and Schedule F Parts I–III.
   - 291 returns were parsed, with no failures and no filer-EIN mismatches. 147 recipients have both years, except Floresta USA and Prevail Foundry (FY2024 only) and ACANI (FY2023 only). Those three borrow the other year's share.
4. **Foreign share, per recipient-year.** Three definitions are computed:
   - **Central ("expense"):** min(line 25, max(line 3, Schedule F Part I non-investment expenditures)) ÷ line 25.
     - Part I rows whose activity text contains "invest" are excluded, except programme-related investments.
     - This counts grants abroad plus programme spending abroad, which matters for operating NGOs that run their own field offices. Examples: One Acre Fund (line 3 $18.5m vs Part I $425.5m), World Central Kitchen, International Justice Mission.
   - **Floor ("l3_of_exp"):** line 3 ÷ line 25, i.e. foreign grants only.
   - **High ("grant_mix"):** line 3 ÷ lines 1–3. This was P-NEW-FGN-01's basis for the nine intermediaries. It overstates for operating NGOs whose small grant budgets are wholly foreign.
5. **Pass-through.** For each FY, the recipient's inbound net Schedule I dollars are multiplied by its own foreign share for the same FY. The result is summed over FY2023 and FY2024.
6. **Regions.** Each recipient-year's central dollars are split by its Schedule F Part I non-investment rows. Where Part I has no such rows, Parts II + III are used. Region names are normalised with `mission_foreign_grants.region_of`, so the categories match the direct-route table.
7. **Comparison.** Direct-route figures (line 3, lines 1–3, itemising line 3, net Schedule I, and Part II regions) are read from `daf-foreign-grants-schedule-f-2023-2024.csv` (`scope_total`, `region_part2`, `intermediary` rows).
8. **Extrapolation [I].** Two inbound amounts are extrapolated:
   - targets outside the top 150 ($1.369bn);
   - the three top-150 recipients that file no 990 ($150.5m).
   - Both are multiplied by the dollar-weighted share of the 147 parsed recipients (61.7%). As a sensitivity, ranks 101–150 give 61.6% and almost the same total. Neither tests ranks 151 and below (5,270 recipients, $1.369bn, about $0.26m each), where small US-based Q-coded groups may weigh more. [V wave 37A]
9. **DAF weighting.** A variant multiplies each sponsor-year's lines by its DAF share of grants (`sponsor-cost-structure.csv`, capped at 1), as in P-NEW-RCP-01.

Two consecutive runs produced byte-identical CSVs.

## 2. Coverage and Schedule F cross-checks [F/C]

- **Coverage:** 291 recipient-years parsed. 287 file Schedule F, and 259 report line 3 > 0.
- **Part II + III against line 3:** within $0.5m or 5% in 235 of 259 [C]. Most gaps are filers whose Part II omits non-cash aid or lists only part of the grants.
- **Part I against line 3:**
  - Grantmaking rows reach at least 95% of line 3 in 189 of 259.
  - All non-investment rows reach line 3 in 227.
  - In 156 recipient-years Part I non-investment spending exceeds line 3. These are field programmes, and Part I drives the central share.
  - 19 recipient-years report Part I non-investment spending below 95% of line 3, for example American Friends of Yeshiva Dmir ($0.2m Part I vs $33.6m line 3) and AFSNC. For these, line 3 is used.
- **Part I row totals:**
  - In all 287 Schedule F filers they equal the filed `TotalSpentAmt`.
  - $2.53bn of Part I is investment rows, excluded. The largest are the Council on Foreign Relations ($699.3m, all of its Part I), the Rotary Foundation ($408.7m), the American Jewish Joint Distribution Committee ($326.9m), the American Society for Technion ($242.6m) and the Carnegie Endowment ($217.3m).
- **Cap:** the line-25 cap binds in 8 recipient-years (DKT International, Association for Cultural Interchange, Impact Community Foundation and others).
- **Zero foreign spending as filed:**
  - Mission Mutual ($49.4m inbound): no Schedule F, line 3 = 0. It is a missionary fiscal sponsor.
  - American Israel Education Foundation ($28.8m): Part IV line 14b answered Yes, but Schedule F Part I reports $0. Its Schedule F Part IV answers Yes to both a transfer to a foreign corporation and ownership of one in FY2023 and FY2024, so the zero probably understates its foreign spending. [V wave 37A]
  - Council on Foreign Relations ($14.4m) and Union of Concerned Scientists ($14.5m): US-based Q05 policy groups.
  - These are kept at zero as filed.

## 3. Results

### 3.1 Totals [C]

| Scope | Recipients | Inbound FY2023–24 | Abroad (central) | Share | Floor (line 3 ÷ exp.) | High (line 3 ÷ lines 1–3) |
|---|---|---|---|---|---|---|
| Top 150 | 150 | $3,178.8m | **$1,867.7m** | **58.8%** | $1,341.2m (42.2%) | $2,320.9m (73.0%) |
| … with a Form 990 | 147 | $3,028.3m | $1,867.7m | 61.7% | 44.3% | 76.6% |
| … no Form 990 | 3 | $150.5m | — | — | — | — |
| Q only | 133 | $2,880.2m | $1,606.2m | 55.8% | | |
| Q and friends-of | 9 | $175.3m | $143.2m | 81.7% | | |
| Friends-of, not Q | 8 | $123.2m | $118.4m | 96.1% | | |
| Five named intermediaries in the frame | 5 | $115.4m | $90.1m | 78.1% | | $103.1m |
| All Q / friends targets | 5,420 | $4,547.3m | [I] $2,804.6m | [I] 61.7% | | |

- **By year:** FY2023 $865.4m of $1,433.4m (60.4%); FY2024 $1,002.3m of $1,745.4m (57.4%).
- **DAF-weighted:** $1,801.0m of $3,070.1m.
- **Named intermediaries:** the five in the frame are Myriad USA/KBFUS, GlobalGiving, Global Fund for Women, Give2Asia and BSUF. On the grant_mix basis they come to $103.1m. P-NEW-FGN-01 gave $103.4m for the same five. The small difference comes from the totals-row drop and the main-scope restriction.
- **Friends-of, all 17 in the top 150:** $298.6m inbound and $261.5m abroad (87.6%).

**Share bands (central, by recipient):**
- ≥ 90% foreign: 26 recipients, $424.7m inbound;
- 50–90%: 74 recipients, $1,668.1m;
- 10–50%: 37 recipients, $766.4m;
- < 10%: 10 recipients, $169.1m (CFR, UCS, Mission Mutual, AIEF, Nuclear Threat Initiative, Childrens Hunger Fund and others).

**By NTEE subgroup (central share):**
- Q30 (international development) 67.1% of $944.3m;
- Q33 (relief) 53.1% of $853.0m;
- Q12 (fund raising / fund distribution, e.g. Central Fund of Israel, Friends of the IDF) 73.3%;
- Q11 (single-organisation support, mostly friends-of bodies) 67.2%;
- Q70 (human rights) 36.2%;
- Q71 (migration/refugee) 44.5%;
- **Q05 (international-affairs research and policy) 12.3%**;
- Q01 (alliances/advocacy) 12.4%, Q40 (peace and security) 23.5%, Q41 (arms control) 6.4% [C].

### 3.2 Largest pass-through recipients [F/C]

| Rank | Recipient | NTEE | Inbound $m | Central share | Abroad $m | Main region |
|---|---|---|---|---|---|---|
| 1 | Médecins Sans Frontières USA | Q30 | 201.6 | 81.6% | 163.7 | Sub-Saharan Africa |
| 5 | World Central Kitchen | Q33 | 92.3 | 84.7% | 77.6 | MENA |
| 3 | Save the Children Federation | Q33 | 105.8 | 66.6% | 70.8 | Sub-Saharan Africa |
| 2 | International Rescue Committee | Q71 | 138.4 | 47.6% | 65.9 | Sub-Saharan Africa |
| 7 | US Fund for UNICEF | Q42 | 71.0 | 81.9% | 58.2 | Sub-Saharan Africa |
| 12 | Central Fund of Israel | Q12 | 55.7 | 97.0% | 54.1 | MENA |
| 8 | Helen Keller International | Q30 | 70.9 | 72.1% | 51.4 | Sub-Saharan Africa |
| 11 | Friends of the IDF | Q12 | 56.3 | 85.9% | 45.3 | MENA |
| 10 | World Vision | Q33 | 61.8 | 73.2% | 45.2 | Sub-Saharan Africa |
| 17 | Myriad USA / KBFUS | Q30 | 46.5 | 95.9% | 44.6 | Europe |

Shares in the table are pooled over the recipient's two returns. The dollar figures use each year's own share.

### 3.3 Regions [C]

| Region | Via top-150 $m | Share | Direct (Part II) $m | Combined $m | Combined share |
|---|---|---|---|---|---|
| Europe | 246.5 | 13.2% | 938.7 | 1,185.1 | **31.5%** |
| Sub-Saharan Africa | 658.0 | **35.2%** | 115.8 | 773.7 | 20.6% |
| Middle East and North Africa | 456.9 | 24.5% | 234.2 | 691.1 | 18.4% |
| South Asia | 119.7 | 6.4% | 149.0 | 268.7 | 7.2% |
| South America | 51.7 | 2.8% | 165.6 | 217.3 | 5.8% |
| East Asia and the Pacific | 90.1 | 4.8% | 111.4 | 201.4 | 5.4% |
| North America (Canada, Mexico) | 40.8 | 2.2% | 122.5 | 163.2 | 4.3% |
| Russia and the NIS | 116.6 | 6.2% | 5.8 | 122.3 | 3.3% |
| Central America and the Caribbean | 79.1 | 4.2% | 16.5 | 95.6 | 2.5% |
| Latin America (unspecified) / other unspecified | 8.5 | 0.5% | 31.5 | 40.1 | 1.1% |

- **[I] Interpretation:** the two routes reach different places.
  - Direct sponsor grants go mostly to Europe: universities, arts bodies and affiliates.
  - US-registered NGOs carry DAF money to Africa, the Middle East (Israel-focused friends bodies, and relief in Gaza, which is World Central Kitchen's largest Part I region in the filings read) and Ukraine (Russia/NIS: Nova Ukraine, Razom, Spirit of America, JDC).
  - Counting only the direct route therefore understates DAF money reaching Sub-Saharan Africa almost sevenfold (combined $773.7m ÷ direct $115.8m = 6.7×).

### 3.4 Combined international share [C/I]

| Measure | Abroad $bn | Base | Share |
|---|---|---|---|
| Direct line 3 (P-NEW-FGN-01) | 1.891 | lines 1–3, $98.27bn | 1.92% |
| + top-150 pass-through (central) | 3.759 | same | **3.82%** |
| + named intermediaries outside the frame (CAF America, Greengrants, GFC) | 3.817 | same | 3.88% |
| + [I] remaining Q/friends inbound at 61.7% | 4.695 | same | **[I] 4.78%** |
| Direct, itemising | 1.890 | net Schedule I + line 3, $79.23bn | 2.39% |
| + top-150 | 3.758 | same | 4.74% |
| + [I] remaining Q/friends | 4.695 | same | [I] 5.93% |

- **Reading [I]:** the brief asked whether DAF dollars ending abroad are closer to the 2.4% direct share or to the 7.8–8.1% "every international-coded recipient" share.
  - On the same base the answer is about **4.7% measured and 5.9% extrapolated**. That is 43% (measured) to 65% [I] of the way from the direct share (2.39%) to the Q-inclusive share (7.83%).
  - Roughly 40% of the inbound dollars of Q / friends-of recipients is spent in the US: fundraising, US programmes, policy work and overhead.
- **Mixed denominator:** the pass-through numerator is net of DAF-to-DAF, while lines 1–3 are gross. On that base the 3.82% is conservative.

## 4. Limits

1. **Proportionality and fungibility [I].** Each recipient's average foreign share is applied to its DAF money. Designated DAF gifts (e.g. "Ukraine relief") may be more or less foreign than the average. Timing is ignored: a gift booked in FY2024 may be spent later. For example, Friends of the IDF's FY2023 revenue ($282.0m) was 1.97 times its total expenses ($143.2m). [V wave 37A] P-B4531-01-04 proposes a test.
2. **Expense share includes overhead in the denominator.** Line 25 includes fundraising and management. Allocating DAF dollars pro rata to all expenses lowers the share compared with a programme-only basis. The floor and high variants bracket this.
3. **Frame.**
   - Only NTEE Q and friends-of names are in the frame. Non-Q recipients that work abroad are outside it: medical NGOs coded E, faith missions coded X, Global Greengrants (C12), Global Fund for Children (A33Z) and universities' overseas programmes. Their foreign spend is uncounted, apart from the three named intermediaries added from P-NEW-FGN-01.
   - The 3.8–4.8% is therefore a floor for "DAF money reaching abroad" (P-B4531-01-03).
4. **Recipients with no 990.** Compassion International, OneHope and Convoy of Hope ($150.5m) file no Form 990. They are zero in the measured figure and imputed in [I].
5. **Schedule F quality.**
   - Part I reports regions, not countries, and AIEF-type zeros are taken as filed.
   - The "investment" exclusion is a text rule: a row such as "investment in affiliates" (14 rows across all parsed returns) is excluded even when the affiliate runs programmes.
   - Region shares follow Part I spending, not specifically the DAF-funded part.
6. **Double counting with the direct route is unlikely but not ruled out.** Validation found none: the central measure takes the larger of line 3 and Part I, never their sum, and the two routes cannot overlap at the sponsor. 11 of the 150 recipients ($178.3m abroad) are themselves DAFRC-panel DAF sponsors (e.g. KBFUS, JNF, World Vision, Rotary Foundation), so some inbound may sit in a DAF there before going abroad. [V wave 37A]
   - Direct foreign grants go to foreign organisations, and this route covers US organisations, so the two do not overlap at the sponsor.
   - A recipient's re-grant to another US target (e.g. a friends-of body granting to a Q organisation) would count twice only if both are in the top 150 and the first reports it on line 3, which by definition it would not.
7. **Sponsor scope.** University/hospital sponsors are excluded, as in the direct figure. The six attachment-only sponsor-years have no Schedule I lines, so their indirect routes are not measured.
8. **DAF vs non-DAF.** Community foundations' Schedule I includes non-DAF grants. The DAF-weighted variant ($1.801bn) addresses this proportionally.

## 5. Data dictionary — `daf-money-abroad-2026-11-19.csv`

| Column | Meaning |
|---|---|
| row_type | `summary`, `comparison`, `region`, `region_combined`, `sponsor`, `recipient` |
| row_type_detail | Summary sub-type: `selection_basis`, `ntee_subgroup` (first 3 characters of NTEE_CD), `named_intermediary`, `share_band`. Blank for headline summaries |
| scope | Recipient name (Schedule I spelling), sponsor name, summary scope (`top150`, `top150_with_form990`, `top150_no_form990`, `all_q_or_friends_targets_net`, or a group value), comparison measure, or region scope |
| rank | Recipient rank by pooled net inbound (1–150); sponsor rank by FY2024 DAF assets |
| ein, bmf_name, ntee_cd | Recipient (or sponsor) EIN; IRS EO BMF name and NTEE_CD |
| segment | Sponsor DAFRC segment (sponsor rows) |
| selection_basis | `q`, `friends` or `q+friends` |
| named_intermediary | 1 if one of the nine P-NEW-FGN-01 intermediaries |
| grantors | Distinct top-50 sponsors granting to the recipient |
| recipients | Summary rows: recipients pooled |
| category | Region (Schedule F names, normalised as in mission_foreign_grants.region_of) |
| inbound_fy2023_usd, inbound_fy2024_usd, inbound_usd | Net Schedule I dollars from main-scope top-50 sponsors (DAF-to-DAF and totals rows dropped) |
| inbound_daf_weighted_usd | Same × each sponsor-year's DAF share of grants (capped at 1) |
| object_id_fy2023/2024, tax_period_fy2023/2024 | Recipient Form 990 e-file object id and tax period used |
| return_status | `FY:ok` or `FY:no_filing` per FY |
| part_ix_l1_usd, part_ix_l2_usd, part_ix_l3_foreign_usd, part_ix_l25_total_expenses_usd | Recipient Form 990 Part IX lines 1, 2, 3 and 25 (column A), summed over the returns used |
| sched_f_present | One character per FY (2023, 2024): 1 = Schedule F filed, 0 = not, - = no return |
| sched_f_part1_total_usd, _noninv_usd, _grantmaking_usd, _investments_usd, _spent_reported_usd | Schedule F Part I: all region rows; rows not classed as investments; grantmaking rows; investment rows; filed TotalSpentAmt |
| sched_f_part2_3_usd | Schedule F Part II + Part III grants (cash + non-cash) |
| foreign_expense_usd | min(line 25, max(line 3, Part I non-investment)) |
| grant_mix_share, l3_of_exp_share, expense_share | Pooled ratios: line 3 ÷ lines 1–3; line 3 ÷ line 25; foreign_expense ÷ line 25. Blank where there is no return |
| share_basis, region_basis | Per FY: `same_fy`, `other_fy` (borrowed) or `none`; region source `part1_noninv`, `part2_3` or `none` |
| abroad_expense_usd, abroad_l3_of_exp_usd, abroad_grant_mix_usd | Σ over FY of inbound × that FY's share (central, floor, high) |
| abroad_expense_daf_weighted_usd, abroad_expense_fy2023_usd, abroad_expense_fy2024_usd | Central estimate on DAF-weighted inbound; by FY |
| abroad_share_of_inbound | abroad_expense ÷ inbound. In summary rows, `l3_of_exp_share` / `grant_mix_share` hold the same ratio for the floor and high methods |
| top_region | Region with the most central dollars for the recipient |
| region_share | Share of the row's region total |
| direct_l3_usd | Sponsor rows: sponsor's Part IX line 3 FY2023–24. region_combined rows: direct Schedule F Part II dollars |
| indirect_to_direct_ratio | Sponsor rows: abroad via top-150 ÷ direct line 3 |
| denominator_usd, share_of_denominator, note | Comparison rows: base and share; `note` says the base and any [I] |
| source | Source note |

## 6. Source register

| # | Source | URL | Accessed | robots.txt |
|---|---|---|---|---|
| S1 | IRS Form 990 e-file XML of 147 recipients, 291 returns (Part IX, Schedule F), GivingTuesday mirror of IRS TEOS. Object ids are in the recipient rows | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | 2026-11-19 | 404, no rules (logged 2026-11-19) |
| S2 | IRS TEOS e-file index CSVs 2023–2026 (scratch copies) | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (one per year) | earlier batches | not re-fetched |
| S3 | IRS EO BMF eo1–eo4, eo_pr, eo_xx (2026-11 snapshot, scratch copy) | https://www.irs.gov/pub/irs-soi/eo1.csv | earlier batch | not re-fetched |
| S4 | Top-50 sponsors' Schedule I lines (P-NEW-RCP-01 line cache) | via S1 | earlier batch | — |
| S5 | Direct route and intermediary pass-through: `data/mission-2026-11-14/daf-foreign-grants-schedule-f-2023-2024.csv` (P-NEW-FGN-01) | repo | — | — |
| S6 | `daf-to-daf-recipient-whitelist.csv`, `sponsor-cost-structure.csv`, DAFRC panel | repo | — | — |

## 7. Reproduction

```
S=<scratchpad>
python3 scripts/mission_daf_money_abroad.py . --np-cache $S/npcache --lines-cache $S/rcp/lines --bmf-dir $S/rcp/bmf \
    --index-dir $S/irs --extract-cache $S/q3101/ext [--fetch] [--workers 6] [--top 150]
```

- The cold run (291 returns fetched) takes about 30 s. The warm run takes about 17 s.
- The script writes the CSV and prints a JSON summary: cross-checks, extrapolation inputs, comparison, regions, sponsors and recipients.
- Every figure above comes from that output or the CSV. Ratios such as 4.0× and 69.9% coverage are arithmetic on those outputs.
