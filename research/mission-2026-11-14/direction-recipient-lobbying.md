# Direction P-NEW-ADV-01: lobbying and political-campaign reporting by DAF grant recipients (top-50 sponsors, FY2023–2024)

**Date:** 2026-11-15 · **Queue item:** P-NEW-ADV-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/daf-recipient-lobbying-2023-2024.csv`](../../data/mission-2026-11-14/daf-recipient-lobbying-2023-2024.csv): 18,441 rows. 2,442 `aggregate` rows (scope × FY × NTEE major group × metric) and 15,999 `recipient` rows (one per selected recipient EIN, numeric fields only, no names).
- [`data/mission-2026-11-14/queue-proposals-batch45-n32.csv`](../../data/mission-2026-11-14/queue-proposals-batch45-n32.csv): P-B45N32-01..03.
- **Script:** [`scripts/mission_recipient_lobbying.py`](../../scripts/mission_recipient_lobbying.py) (stdlib, functional style). It reuses `mission_recipient_sectors.py`'s universe, Schedule I line cache, DAF-to-DAF flag (`annotate`) and NTEE classification.

**Rules applied**
- **Read first:** [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md) with its wave-24A governing corrections, and [direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md) with its wave-26 governing corrections. None of the corrections changes the Schedule I lines, the DAF-to-DAF whitelist or the sector classification used here.
- **Recency:** grant lines are DAFRC FY2023–FY2024 sponsor returns (tax periods ending 2023-03-31 to 2024-12-31). Recipient returns are restricted to tax periods ending 2021-12 or later; 98.8% of those parsed end in 2024 (§1.3).
- **robots.txt** read on 2026-11-15 before any fetch (§6). No outreach, logins or forms.
- **Neutral framing.** Lobbying by 501(c)(3) organisations is lawful within the limits of §501(c)(3) ("no substantial part") or, for electing organisations, §501(h)/§4911. Schedule C is a self-disclosure. Nothing here says any recipient or grant was improper, and no recipient is characterised by viewpoint. Recipients are not named in the findings; the CSV carries EINs only.
- **Labels:** **[F]** filed value; **[C]** script computation; **[I]** inference.
- This is research, not legal or tax advice.

---

## 0. Answers in brief

Universe: 94 itemising top-50 sponsor-years, **$78.29bn of Schedule I dollars net of DAF-to-DAF** to 170,569 recipient EINs (plus $0.64bn on blank-EIN lines) [C]. Headline figures below are for all sponsors excluding the four university/hospital sponsor-years ($77.34bn), matching the sectors note; the all-sponsor figures differ by under 0.3 pts.

| Question | Answer [C] |
|---|---|
| **Coverage** (share of net dollars with a parseable 501(c)(3) Form 990/990-EZ) | **71.2%** ($55.03bn). Fetch cap: the 15,999 recipients covering the top 85% of all net dollars and the top 80% within each sponsor segment ($66.12bn, 84.5%). Of the selected dollars, 83.5% had a parseable 501(c)(3) return; the rest (all sponsors) are mostly churches ($5.16bn), EINs not in the BMF ($2.89bn, of which the four SVCF→CZ Biohub/Institute LLC lines are $1.66bn), 990-PF filers ($1.18bn) and governmental units ($1.12bn, of which $0.74bn from the university/hospital sponsors) — none of which file Schedule C. |
| **Share of DAF dollars to recipients reporting any lobbying** | **42.2% of covered dollars** ($23.20bn). As a share of *all* net dollars this is **30.0%** if every uncovered dollar is treated as non-lobbying, and at most 58.8% if every uncovered dollar went to a lobbying recipient. By recipient count, **20.0%** of covered recipients report lobbying: lobbying is more common among large recipients. |
| … 501(h) electors | 18.6% of covered dollars went to recipients that file Part II-A (1,632 of 12,985 covered recipients); 1,308 of them report Part II-A lobbying above zero. The other lobbying recipients (1,250) report under Part II-B, the "no substantial part" test; 44 answer Part IV line 4 "Yes" with no parsed Part II. |
| **By NTEE sector** (lobbying share of covered dollars) | Environment/animals **61.1%**; education **54.7%**; health **50.5%**; public-society benefit 37.3%; international 34.4%; human services 29.4%; arts/culture 24.8%; **religion 6.9%** (coverage only 15.1%, since most religious recipients are churches with no Form 990). |
| **By sponsor type** | National **45.9%** of covered dollars (coverage 71.3%); community foundations **34.7%** (72.8%), or 39.5% excluding SVCF; single-issue sponsors **31.0%** (66.4%); processors 0%. |
| **Lobbying intensity** (lobbying expenditures ÷ total expenses) | Low. Among recipients reporting lobbying with an amount: median **0.20%**, 75th percentile 0.76%, 90th 2.1%, 99th 7.0%, maximum 16.1%. **No recipient exceeds 20%.** Dollar-weighted: 0.60% for the lobbying recipients, 0.25% across all covered dollars. Of covered dollars, 58.4% go to recipients reporting none, 23.2% to >0–0.1%, 12.1% to 0.1–1%, 4.2% to 1–5%, 1.7% to 5–20%. |
| **Part I-A political campaign activity** | **36 of 12,985 covered 501(c)(3) recipients** (0.28%) reported something: 19 answered Part IV line 3 "Yes" and 24 entered a positive Schedule C Part I amount (7 did both). They received **$73.5m (0.13% of covered dollars)**. The reported Part I amounts sum to $4.6m (median $48k); one return shows §4955 tax. These are self-disclosures that need review; some may be lobbying amounts entered in Part I-A (26 of the 36 also report lobbying) [I]. Separately, 8 selected recipients ($45.2m) file as non-501(c)(3) (five BMF subsection 04, one 06), where Part I-C political activity is permitted; four of them report it ($40.3m). |
| **Robustness** | (a) Return year: for the 1,479 largest covered recipients ($35.8bn) the TY2023-period return gives the same lobbying yes/no for **97.1% of dollars** (lobbying share 53.4% vs 53.8%). (b) Excluding the 10 largest recipients ($7.72bn), the lobbying share of covered dollars falls to 39.0%. (c) FY2023 vs FY2024 grants: 42.5% vs 41.8%. |

**Reading [I]**
- Reporting *some* lobbying is common among the large, established charities that receive most DAF dollars: research universities, academic medical centres, large environmental organisations and fiscal sponsors. For almost all of them it is a very small share of spending. The dollar-weighted share of recipients' budgets spent on lobbying is about 0.25%.
- The sector ordering (environment, education, health high; religion, arts, human services low) follows which organisations file Form 990 and run government-relations functions, not only what they work on.
- Political campaign disclosures by 501(c)(3) recipients are rare in both count and dollars.

---

## 1. Method

### 1.1 Universe and grant dollars
- Top-50 DAFRC sponsors by FY2024 DAF assets, one return per sponsor and FY via `mission_daf_to_daf.pick_returns`. All 94 itemising sponsor-years (46 top-50 sponsors plus Stanford and UCLA Foundation). The attachment-only sponsors (BofA CGF, Renaissance, Greater Horizons FY2023, Greater Kansas City CF FY2023) are absent, as in the earlier notes.
- Every Schedule I Part II line from the cached line JSON of `mission_recipient_sectors.py` (604,915 lines). DAF-to-DAF lines are excluded using [`daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv) decisions `include`, self-lines, and unique whitelisted names on blank-EIN lines.
- Sector: recipient EIN → IRS EO BMF `NTEE_CD` major group, with the BMF foundation-code and name-rule fallbacks of the sectors note (its `group` field, reused unchanged).
- Sponsor type: the DAFRC segment (national, community_foundation, single_issue, processor, university_hospital).

### 1.2 Fetch cap (targets)
- Net dollars were summed per recipient EIN, pooled over FY2023–2024. The target set is the union of the EINs covering the top **85%** of all net dollars and those covering the top **80%** within each sponsor segment. That gives **15,999 EINs, $66.12bn (84.5% of net dollars)**.
- The remaining 154,570 EINs ($11.53bn, 14.7%) and blank-EIN lines ($0.64bn) stay in every denominator as `not_selected` / `blank_ein`.

### 1.3 Locating each recipient's return
- **Index:** IRS TEOS e-file index `index_2021.csv` … `index_2026.csv` (apps.irs.gov). Local copies were used after a HEAD request confirmed identical Content-Length (2023–2026 checked).
- **Choice:** one Form 990 or 990-EZ per EIN. Preference: tax period ending 2023-01..2024-12 (latest first), then 2025–2026, then 2022, then 2021-12. Within a period, the latest object id; Form 990 before 990-EZ. 990-PF filers are recorded but not parsed (no Schedule C).
- **Result:** 13,155 targets have a TY2021+ e-filed return; 13,011 are 990/990-EZ. The parsed returns' period ends: 2024 12,831; 2023 102; 2022 31; 2021 12; 2025 9. So for most recipients the return covers the FY2024 grant year; FY2023 grants are matched to the following year's return (see the sensitivity in §2.5).
- **Fetch:** XML from the GivingTuesday mirror of IRS TEOS (`gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`), 13,000 via the mirror and 11 from local copies. **18 returned HTTP 404** ($48.4m). Each XML was streamed and reading stopped at the end of Schedule C. Only the parsed values were cached (58 MB); no XML was kept.
- **No return (BMF classification of the 2,844 EINs without a TY2021+ 990/990-EZ/990-PF):** church (BMF foundation 10 or filing requirement 06/13), 990-N (filing requirement 02), group-return subordinate (affiliation 9, filing requirement 03 or a group code), government (subsection 01, filing requirement 14 or "GOV" in the name), other in BMF, not in BMF.

### 1.4 Classification of each parsed return
| Status | Rule |
|---|---|
| `lobby_501h` | Schedule C Part II-A present (any filing-organisation amount in lines 1a–1f) and total lobbying expenditures (line 1c, `TotalLobbyingExpendGrp`; else direct + grassroots) > 0 |
| `lobby_ii_b` | Part II-B: any of lines 1a–1i answered Yes, or line 1j total > 0 |
| `lobby_part_iv_only` | No Part II parsed, but Form 990 Part IV line 4 (`LobbyingActivitiesInd`) or 990-EZ line 47 = Yes. Counted as lobbying, amount unknown |
| `none_501h_zero` | Part II-A filed with zero lobbying |
| `none_ii_b_all_no` | Part II-B filed with every line No and no amount |
| `none_part_iv_no` | No Part II and Part IV line 4 = No (or a 990-EZ with no Schedule C) |
| `parsed_non_501c3` | The return is for a non-501(c)(3) organisation (`Organization501cInd`). Part IV line 4 does not apply. Excluded from the 501(c)(3) coverage, reported separately |

- **Covered** = the six 501(c)(3) statuses above `parsed_non_501c3`.
- **Intensity** = lobbying expenditures ÷ total expenses (990 Part I line 18 `CYTotalExpensesAmt`; 990-EZ line 17). Part II-B line 1j includes grants to other organisations for lobbying (line 1f), which can dominate for intermediaries and fiscal sponsors.
- **Political:** Part IV line 3 (`PoliticalCampaignActyInd`) = Yes, or any positive amount in Schedule C Part I. The Part I fields seen were `PoliticalExpendituresAmt` (72 returns), `Section4955OrganizationTaxAmt` (57), `Section4955ManagersTaxAmt` (56), `VolunteerHoursCnt` (54) and one `Section527PoliticalOrgGrp` amount; most were zero.
- **XML conventions:** both `1/0` and `true/false` indicator encodings occur; both are handled.

### 1.5 Note on 990-EZ, 990-N and churches
- **990-EZ filers do file Schedule C** when they answer Yes to line 46 (political) or, for 501(c)(3)s, line 47 (lobbying or a 501(h) election). 41 covered recipients filed 990-EZ; none had a Schedule C, and all 41 answered line 47 No.
- **990-N (e-Postcard) filers, churches** (not required to file), **governmental units** and **group-return subordinates** have no Schedule C of their own. Private foundations file 990-PF, which has no Schedule C (lobbying by a private foundation is a taxable expenditure under §4945). These dollars are reported as uncovered, not as "no lobbying".

## 2. Results

### 2.1 Coverage of net DAF dollars, FY2023–2024 pooled [C]
| Status | All top-50 itemising $ | Share of $78.29bn |
|---|---|---|
| Covered 501(c)(3) return | 55.21bn | **70.5%** |
| … reports lobbying | 23.31bn | 29.8% |
| … reports no lobbying | 31.90bn | 40.7% |
| Not selected (below the fetch cap) | 11.53bn | 14.7% |
| No return: church | 5.16bn | 6.6% |
| No return: not in BMF | 2.89bn | 3.7% |
| 990-PF filer | 1.18bn | 1.5% |
| No return: government | 1.12bn | 1.4% |
| Blank or placeholder EIN | 0.64bn | 0.8% |
| No return: group subordinate / 990-N / other in BMF | 0.19bn / 0.19bn / 0.07bn | 0.6% |
| Parsed, non-501(c)(3) | 0.05bn | 0.06% |
| Fetch failed (HTTP 404) | 0.05bn | 0.06% |

University/hospital sponsors' recipients are mostly governmental (public universities, $0.74bn), so their coverage is 19.9%.

### 2.2 Share of covered dollars to recipients reporting lobbying, by sector and sponsor type [C]
Pooled FY2023–2024. Each cell: lobbying share of covered dollars (coverage share of net dollars in brackets).

| NTEE major group | All ex univ./hosp. | National | Community foundations | Single-issue |
|---|---|---|---|---|
| **All** | **42.2%** (71.2) | **45.9%** (71.3) | **34.7%** (72.8) | **31.0%** (66.4) |
| Education | 54.7% (86.3) | 58.6% (86.8) | 38.1% (82.3) | 43.6% (88.4) |
| Health | 50.5% (62.4) | 53.7% (78.3) | 43.3% (36.2) | 44.2% (80.2) |
| Environment/animals | 61.1% (86.0) | 62.2% (84.1) | 59.5% (89.4) | 55.1% (95.5) |
| Public-society benefit | 37.3% (88.1) | 44.5% (85.8) | 21.8% (91.2) | 44.4% (93.4) |
| International | 34.4% (88.3) | 33.8% (87.3) | 52.1% (95.1) | 16.9% (85.7) |
| Human services | 29.4% (77.7) | 29.6% (76.9) | 32.7% (81.0) | 16.7% (75.0) |
| Arts/culture | 24.8% (73.6) | 25.2% (72.7) | 22.5% (75.4) | 28.8% (81.7) |
| Religion | 6.9% (15.1) | 9.1% (11.0) | 5.1% (17.7) | 4.4% (27.4) |
| Unclassified | 29.4% (56.8) | 28.3% (53.2) | 35.4% (62.7) | 17.9% (69.6) |

**Notes**
- **Community-foundation health coverage is 36%** because SVCF's four CZ Biohub/Institute LLC lines ($1.66bn, name-rule health) have no return. Excluding SVCF, the community-foundation lobbying share is **39.5%** (coverage 76.8%).
- **By recipient count**, the share reporting lobbying is lower and flatter: 20.0% overall; environment 38.6%; health 27.3%; public benefit 23.8%; human services 18.5%; arts 18.5%; education 17.8%; international 10.9%; religion 3.2%. Community foundations' covered recipients report lobbying more often by count (25.5%) than national sponsors' (20.6%), but less by dollars, because national sponsors' dollars are more concentrated in large universities and health systems.
- **501(h) electors** take 18.6% of covered dollars overall: 32.6% in environment, 26.1% in public benefit, 12.3% in education, 1.1% in religion.

### 2.3 Lobbying intensity [C]
**Distribution of covered dollars by recipient intensity** (lobbying expenditures ÷ total expenses):

| Intensity | All ex univ./hosp. | National | Community foundations | CF ex SVCF | Single-issue |
|---|---|---|---|---|---|
| 0 (none reported) | 58.4% | 54.8% | 65.7% | 60.8% | 69.2% |
| >0–0.1% | 23.2% | 26.3% | 16.0% | 18.0% | 16.2% |
| 0.1–1% | 12.1% | 12.4% | 11.9% | 14.4% | 10.2% |
| 1–5% | 4.2% | 4.2% | 5.0% | 5.5% | 2.5% |
| 5–20% | 1.7% | 2.0% | 0.9% | 0.8% | 1.7% |
| >20% | 0 | 0 | 0 | 0 | 0 |
| Lobbying, amount unknown | 0.3% | 0.3% | 0.5% | 0.5% | 0.2% |

**Recipient counts** (2,474 lobbying recipients with a computable ratio, of 2,602): >0–0.1% 920; 0.1–1% 1,029; 1–5% 457; 5–20% 68; >20% 0.
- **Quantiles** among those 2,474: p10 0.006%, p25 0.036%, **median 0.20%**, p75 0.76%, p90 2.1%, p99 7.0%.
- **Dollar-weighted mean intensity:** 0.25% across all covered dollars; 0.60% across dollars to lobbying recipients. By sector (lobbying recipients only): environment 1.9%, public benefit 1.2%, human services 0.55%, health 0.44%, international 0.38%, religion 0.35%, arts 0.31%, education 0.18%.
- **Excluding the 10 largest recipients** ($7.72bn), the 5–20% band falls from 1.7% to 1.1% of covered dollars, because one of the ten is an intermediary whose Part II-B total is mostly grants to other organisations.

**501(h) electors' use of their limit** [C]:
- Lobbying ÷ the single-year lobbying nontaxable amount (Part II-A line 1f): median **11%**, p90 61%.
- 28 of 1,632 electors report lobbying above the single-year amount. In 18 of the 28, line 1e (total exempt-purpose expenditures) equals or is below line 1c (lobbying), which points to a form-entry error rather than lobbying of that size [I]. Electors are tested on a four-year average (Part II-A line 2), and an excess is taxed under §4911, so this is not a finding about exemption.

### 2.4 Political campaign activity [C]
- **501(c)(3) recipients:** 36 of 12,985 covered recipients reported something in Part I-A or Part IV line 3; they received $73.5m, **0.13%** of covered dollars.
  - 19 answered Part IV line 3 Yes ($31.2m of DAF grants).
  - 24 entered a positive Part I amount: sum $4.58m, median $48k.
  - 7 did both. One return reports §4955 organisation tax.
  - 26 of the 36 also report lobbying. Part I-A entries can be lobbying amounts filed in the wrong part, so each case needs a reading of the return before any conclusion [I].
  - **By sector:** human services $20.8m, health $14.4m, education $10.5m, environment $8.1m, arts $6.6m, religion $5.5m, unclassified $3.7m, public benefit $3.2m, international $0.
- **Non-501(c)(3) recipients:** 8 selected recipients file as other §501(c) organisations (BMF: five subsection 04, one 06, two not in the BMF). They received $45.2m, mostly one $37.5m line from a national sponsor. Four report political activity under Part I-C ($40.3m of grants). Grants by a DAF sponsor to a non-501(c)(3) are permitted with expenditure responsibility and a charitable-purpose restriction; whether these were DAF grants or met those conditions is not visible in Schedule I (cf. the compliance-screen note, §2.4).

### 2.5 Robustness [C]
| Test | Result |
|---|---|
| **Return year:** top 1,479 covered recipients ($35.8bn) re-scored on their TY2023-period return (period end in 2023) | 1,416 agree on lobbying yes/no (**97.1% of dollars**). 38 report lobbying only in the chosen (mostly 2024) return and 25 only in the 2023 return. Lobbying share of these dollars: 53.8% (chosen) vs 53.4% (2023). Median absolute change in intensity where both years lobby: 0.03 pts |
| **Grant year** (all ex univ./hosp.) | FY2023 42.5% (coverage 69.9%); FY2024 41.8% (72.3%) |
| **Ex top-10 recipients** ($7.72bn, all ex univ./hosp.) | 39.0% of covered dollars (coverage 70.3%); 501(h) share 20.9% |
| **Bounds on all net dollars** (all ex univ./hosp.) | Lower 30.0% (uncovered = none); upper 58.8% (uncovered = lobbying). The uncovered pool is mostly churches, governmental units, private foundations and LLCs, which do not file Schedule C, plus the small-recipient tail below the cap |

## 3. Limitations
- **Coverage is 71% of net dollars.** The fetch cap leaves out 154,570 small recipients (14.7% of dollars). Recipients reporting lobbying are larger on average (20% by count vs 42% by dollars among covered recipients), so the tail probably has a lower lobbying share. This is not measured (P-B45N32-01).
- **One return per recipient, mostly the 2024-period return,** is applied to both grant years. The sensitivity in §2.5 shows little effect.
- **Schedule C is self-reported and unaudited.**
  - Part II-B has no statutory definition of "substantial" and no required method for allocating staff time.
  - Some organisations report $0 while describing activity.
  - Part II-B line 1j includes grants to other organisations for lobbying, so an intermediary's intensity can reflect regranting rather than its own lobbying.
  - Part II-A figures cover the filing organisation only; affiliated-group totals are not used.
- **Large recipients' lobbying is not caused by, or traceable to, the DAF grant.** Schedule I gives purposes only in free text, and whether any grant was earmarked for lobbying is not observable. This note measures recipient *characteristics*, not the use of DAF dollars.
- **Churches, governmental units, LLCs and private foundations** (about 13% of net dollars) cannot be scored. The religion sector is therefore covered at only 15%.
- **Name-rule sectors** (6% of dollars) are inference, as in the sectors note.
- **The 18 HTTP 404 returns** ($48m) were not retried from another source.
- **Political-activity fields** need case-by-case reading. Entry errors (lobbying amounts in Part I-A; "Yes" in Part IV line 3 with no Part I-A amount) are plausible for several of the 36.

## 4. Data dictionary: `daf-recipient-lobbying-2023-2024.csv`

**Aggregate rows** (`record_type = aggregate`)

| Column | Meaning |
|---|---|
| scope, scope_type | `all_top50_itemising`, `all_ex_university_hospital` (all); a DAFRC segment or `community_foundation_ex_svcf` (segment); `all_ex_uh_ex_top10_recipients` (sensitivity: excludes the 10 largest recipient EINs) |
| fiscal_year | DAFRC FY `2023`, `2024` or `2023-2024` (pooled) |
| ntee_major_group | `ALL`, or the recipient's NTEE major group per `mission_recipient_sectors.py` |
| metric | `summary` (one per cell); `intensity_bin` (pooled cells and every `ALL` cell); `status` (same cells) |
| net_usd | Schedule I cash + non-cash dollars, net of DAF-to-DAF lines |
| covered_usd, coverage_share | Dollars to recipients with a parsed 501(c)(3) Form 990/990-EZ (six covered statuses, §1.4), and their share of net_usd |
| lobbying_usd_to | Dollars to covered recipients reporting lobbying (`lobby_*` statuses) |
| lobbying_share_of_covered | lobbying_usd_to ÷ covered_usd |
| lobbying_share_of_net_lower_bound | lobbying_usd_to ÷ net_usd |
| elector_501h_share_of_covered | Share of covered dollars to recipients filing Part II-A |
| political_reported_usd, part_iv_line3_yes_usd | Dollars to covered 501(c)(3) recipients with Part IV line 3 Yes or a positive Schedule C Part I amount; the line-3-Yes subset |
| non_501c3_parsed_usd, non_501c3_political_usd | Dollars to parsed non-501(c)(3) recipients; of which reporting political activity |
| dollar_weighted_mean_intensity | Σ(dollars × lobbying/expenses) ÷ Σ dollars over covered recipients with a computable ratio |
| dollar_weighted_mean_intensity_lobbying_only | The same, over recipients with intensity > 0 |
| recipients, recipients_covered, recipients_lobbying, recipient_count_share_lobbying | Distinct recipient EINs in the cell; covered; reporting lobbying; lobbying ÷ covered |
| bin_or_status, bin_usd, bin_share_of_covered | For `intensity_bin`: the band and its dollars, as a share of covered_usd. For `status`: the status (§1.4, §1.3) and its dollars, **as a share of net_usd** |

**Recipient rows** (`record_type = recipient`; numeric fields only)

| Column | Meaning |
|---|---|
| ein | Recipient EIN (9 digits) |
| object_id | IRS e-file object id of the return used (blank if none) |
| return_form_code | 1 = 990, 2 = 990-EZ, 3 = 990-PF, 0 = none |
| tax_period_yyyymm | Tax-period end of that return |
| status_code | 1 lobby_501h, 2 lobby_ii_b, 3 lobby_part_iv_only, 4 none_501h_zero, 5 none_ii_b_all_no, 6 none_part_iv_no, 7 parsed_no_lobby_data, 8 no_sched_c_990pf, 9 no_return_church, 10 no_return_990n, 11 no_return_group_subordinate, 12 no_return_government, 13 no_return_other_in_bmf, 14 no_return_not_in_bmf, 15 fetch_or_parse_failed, 18 parsed_non_501c3 |
| sector_code | 1 education, 2 religion, 3 human_services, 4 health, 5 arts_culture, 6 international, 7 environment_animals, 8 public_societal_benefit, 9 mutual_membership, 10 unknown_z, 11 unclassified |
| net_daf_grant_usd, net_usd_fy2023, net_usd_fy2024 | Net Schedule I dollars received from top-50 sponsors, pooled and by FY |
| net_usd_national, net_usd_community_foundation, net_usd_single_issue, net_usd_other_segments | The same, by sponsor segment (other = processor + university/hospital) |
| reports_lobbying, elector_501h | 0/1 flags |
| lobbying_usd | Part II-A line 1c (filing organisation) or Part II-B line 1j |
| total_expenses_usd | 990 Part I line 18 / 990-EZ line 17 |
| lobby_to_expenses | lobbying_usd ÷ total_expenses_usd |
| lobby_to_nontaxable_501h | Electors: line 1c ÷ line 1f (single year) |
| ii_b_yes_count, ii_b_grants_other_orgs, ii_b_direct_contact | Part II-B: number of Yes answers on lines 1a–1i; line 1f Yes; line 1g Yes |
| part_iv_line3_political, part_iv_line4_lobbying | Form 990 Part IV lines 3–4 (990-EZ lines 46–47): 1 Yes, 0 No, blank absent |
| sched_c_part_i_amount_usd, political_reported | Sum of positive Schedule C Part I dollar fields; 0/1 political flag (§1.4) |

## 5. Reproduction
```
python3 scripts/mission_recipient_lobbying.py --np-cache NPCACHE --bmf-dir BMF --lines-cache LINES \
    --irs-dir IRS --ret-cache RC [--xml-dir DIR ...] --fetch [--workers 16] [--share-all 0.85 --share-seg 0.80]
```
- `NPCACHE`, `BMF` and `LINES` are those of `mission_recipient_sectors.py`.
- `IRS` holds `index_2021.csv` … `index_2026.csv`.
- `RC` caches the parsed Part IV / Schedule C values per object id.
- The script prints a JSON summary (status counts and dollars, period mix, quantiles, political detail, return-year sensitivity, per-scope aggregates). Every figure above comes from that summary or the CSV. Run time is about 4 minutes with a cold cache (13,000 fetches at about 65 per second with 16 threads), and about 2 minutes warm.

## 6. Sources
| ID | Source | Version | robots.txt (read 2026-11-15) |
|---|---|---|---|
| S1 | Recipient returns: IRS e-file XML, [GivingTuesday mirror of IRS TEOS](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/) | 13,011 object ids | Host returns 404 (`NoSuchKey`) for /robots.txt: no rules |
| S2 | [IRS TEOS e-file index](https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv) 2021–2026 | 2026 file Last-Modified 2026-10-21 (58,906,208 bytes; local copy identical); 2025 2026-01-21 | apps.irs.gov/robots.txt redirects to a 404 page: no rules |
| S3 | [IRS EO BMF](https://www.irs.gov/pub/irs-soi/eo1.csv) eo1–eo4, eo_pr, eo_xx | Last-Modified 2026-11-09 (copy from the sectors run) | www.irs.gov: `/pub/` not disallowed (disallows include `/charities-non-profits/tax-exempt-organization-search`, which was not used) |
| S4 | Repo: `mission_recipient_sectors.py` line cache and classification; `daf-to-daf-recipient-whitelist.csv`; DAFRC panel; `netpayout990/` cache | repo | n/a |
| S5 | Form 990 Schedule C and Part IV structure (Parts I-A/I-B/I-C, II-A, II-B; 990-EZ lines 46–47) | IRS form and e-file schema field names as observed in the XML | n/a |

## Validation corrections (wave 30, 2026-11-15) — governing
Source: [validation-wave30-report.md](validation-wave30-report.md); register `data/mission-2026-11-14/validation-register-wave30.csv`.

1. **§0, lobbying intensity row.**
   - **Find:** "Among recipients reporting lobbying with an amount: median **0.20%**, 75th percentile 0.76%, 90th 2.1%, 99th 7.0%, maximum 16.1%."
   - **Replace with:** "Among the 2,531 recipients reporting lobbying with a computable ratio (57 of them at $0): median **0.20%**, 75th percentile 0.76%, 90th 2.1%, 99th 7.0%, maximum 16.1%. Over the 2,474 with a positive amount the median is 0.21% [C; V wave 30]."
2. **§2.3, quantiles.**
   - **Find:** "- **Quantiles** among those 2,474: p10 0.006%, p25 0.036%, **median 0.20%**, p75 0.76%, p90 2.1%, p99 7.0%."
   - **Replace with:** "- **Quantiles** among the 2,531 lobbying recipients with a computable ratio (the 2,474 above plus 57 Part II-B filers reporting $0): p10 0.006%, p25 0.036%, **median 0.20%**, p75 0.76%, p90 2.1%, p99 7.0%. Over the 2,474 with a positive ratio: p25 0.041%, median 0.21%, p75 0.79% [C; V wave 30]."
