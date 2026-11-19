# Validation wave 38C: new-sponsor and community-foundation exit frames (gap1915-b4011)

**Validator:** independent-validation-agent-wave38c. **Date:** 2026-11-19.
**Study validated:** [gap1915-b4011-filing-frames.md](gap1915-b4011-filing-frames.md), with `scripts/mission_filing_frames.py` and its three CSVs.
**Register:** [`data/mission-2026-11-14/validation-register-wave38c.csv`](../../data/mission-2026-11-14/validation-register-wave38c.csv) (25 claims, V38C-01 to V38C-25).

**Method.**
- The script was re-run from the existing cache (`q1511/cache`) without `--fetch`. Its root was a scratch copy holding only the three input CSVs, so nothing was written into the repo. The committed CSVs have the same md5 before and after the run.
- Frame A and frame B counts were recomputed from the run's JSON and, separately, from the CSVs.
- Twelve e-filed returns were re-read from the GivingTuesday mirror of IRS TEOS XML: Groundswell (amended and original TY2024), Givmo, Bridges, Spiral, One Big Gift, Neta, DAFshare, Monument, Overflow, Three Rivers, Coastal and Greater White Bear Lake. The default curl user agent was used.
- The cohort rules were compared with gap19-startup-cohort.md §2.1 as amended in wave 32A. Wilson intervals were recomputed. Frame B was set against `sponsor-mortality-summary.csv` and `sponsor-exit-verification.csv`.
- Not used: crt.sh, certspotter and sec.gov. There was no outreach.

## Counts

| Result | n |
|---|---|
| confirmed | 17 |
| partially_confirmed | 6 |
| contradicted | 2 |
| unverifiable | 0 |
| **Total** | **25** |

## Findings

### Replication (V38C-01 to -04, -06, -16): confirmed
- **The three CSVs reproduce byte for byte** (`cmp`): additions 16 rows, CF exits 195 rows, holders 179 rows.
- **Every funnel figure matches the run output.**
  - Frame A: 513,145 new-c3 EINs; 86,637 returns from 36,115 EINs; 7,682 dropped; 83,020 read; 3,617 not mirrored, all in `index_2026`; 990 EINs with no readable return.
  - Holders: 179 holders on 329 returns; 43 in DAFRC and 136 not.
  - Line 6: 265 EINs answer "Yes"; 198 returns answer "Yes" with 0 accounts; 17 positive returns answer "No"; **14 holders (7.8%) never answer "Yes"**.
  - Window: 122 holders are in window, 24 in DAFRC and 98 not. Of the 98, 64 report a value above 0 and 28 report 50 or more accounts, 18 of them with $0.
  - Frame B: all screen counts, the 195 rows and the 85 and 71 exit filers match.

### Groundswell (V38C-05): confirmed
- **The amended TY2024 return confirms the study.** It is OBJECT_ID 202640289349301029, e-filed 2026-01-28, with `AmendedReturnInd` X. It reports `DonorAdvisedFundInd` 0 and Part I with 12,808 accounts, $9,691,912 of contributions and $10,084,314 at year end.
- **The original TY2024 return has no Part I.** It is 202513219349318726, e-filed 2025-11-17, with line 6 = 0 and no Part I tags. All four of Groundswell's returns answer "No" on line 6.

### Screen accounting and the "not sponsors" sample (V38C-07, -08)
- **The 98 decompose cleanly.** They are 2 existing members (Groundswell and Percent Impact/Goodstack), 7 additions, 7 named exclusions (SAX01, SAX02, SAX04, both SAX05 entities, SAX06 and SAX07), 3 community foundations and 79 residual filers.
- **SAX08 is mislabelled.** 7 of its "ten in-window community foundations" are DAFRC panel members, so only 3 of them are among the 98.
- **A sample confirms the residual filers are not sponsors.** The sample was 15 of the 89 screened-out non-DAFRC holders, drawn with `Random(20261119)`.
  - All 15 are not public DAF sponsors: clubs, ministries, school foundations, a radio club, a surf club and one CF.
  - Three put dollar amounts or implausible counts in the account field: 81,042, 10,000, and 19,853 accounts equal to $19,853 of value.
  - No residual holder has a DAF mission, and the largest residual value is $0.90m (Virtual Christianity, 1 DAF).

### Givmo and Bridges XML (V38C-09, -10): confirmed
- **Givmo.** The TY2025 return was e-filed 2026-07-27 and reports 31 accounts and $865. Schedule O defines the 31 as DAFs that made a donation in the year, including 2 employer-match accounts. The app is run by Givfi Inc, and three directors are SCS Financial executives.
- **Bridges.** The TY2025 return was e-filed 2026-09-11 from Omaha, NE, with formation year 2024 and BMF ruling 2025-01. It reports 42 accounts, $114.7m of contributions, $7.76m of grants and $106,978,471 at year end. Operations are delegated to Bridges Investment Management and Bridges Trust Company.

### Bridges and the cohort rules (V38C-11, -12): partially confirmed
- **The rules treat Bridges and its comparators differently.**
  - Telescope Fund was excluded because its parent is a pre-2021 **DAF sponsor network**.
  - GivingTrax (2010) and GoodCoin/in/PACT (2015) were included as dedicated in-window sponsors of older companies.
  - Bridges' parent is a wealth manager and trust company, not a DAF sponsor. That is the GivingTrax pattern, so the exclusion rests only on the "bank DAF programs" example.
  - Givmo, Spiral and Overflow are admitted although their parents' founding dates were not checked.
- **Bridges would change the bound.** Bridges is active (TY2025 return e-filed 2026-09-11). Including it gives 16/26 = 61.5% (42.5–77.6%).
- **Bridges could not be in DAFRC.** Its only return is for TY2025, after the panel's FY2024 end.
- **The status calls are correct.** ReturnTs values read from the XML: Spiral 2026-08-12, One Big Gift 2026-08-18, Neta 2025-10-12, Monument 2025-11-14, Overflow 2025-11-15 and DAFshare 2025-11-17. `index_2026` lists no 2026 filing for the four unknowns.
- **The account threshold is applied asymmetrically.** Non-DAFRC "dedicated sponsors" get no threshold, which admits Spiral and DAFshare with 1 DAF each. In the original cohort, Possibility Labs and Our Change were cut by the ≥50 rule.

### Survival arithmetic (V38C-13, -14)
- **The arithmetic is correct.** The cohort is 13/1/1/10 (active, acquired, pivoted, unknown). Survival is 15/25 = 60.0% (40.7–76.6%) to 25/25 (86.7–100%), and 15/15 = 79.6–100% among resolved cases.
- **The headline bound keeps a member that fails the window test.** Uncommon Giving fails the study's own window test (and wave 32A's). Without it the cohort is 24 and the lower bound is 14/24 = 58.3% (38.8–75.5%).
- **The strict subset grows from 8 to 12.** The four additions with 2023–2024 formation years join it: active 6, acquired 1, unknown 5. Its bounds are 7/12 = 58.3% (32.0–80.7%) to 12/12 (75.8–100%).

### Size of the DAFRC miss (V38C-15): confirmed, with a timing caveat
- **The figures check.** The seven additions report $12,394,899 in all, of which Neta and Monument hold $11,356,390.
- **Part of the miss is timing.**
  - Neta, Monument, Overflow and DAFshare e-filed their only positive return between 2025-10-12 and 2025-11-17.
  - Givmo's TY2024 return was filed in 2026.
  - DAFRC's FY2024 is 30% imputed.

### Frame B exits (V38C-17 to -21)
- **Exits by year are confirmed.** The geographic-CF counts are 6, 2, 4, 6 and 6 for 2021–2025, and 0 for 2026.
  - 23 of the 24 are small. The median largest observed total assets is $248,412, and 16 are under $1m.
  - 12 filed 990-EZ.
  - The states are OH 4, MI 4, WI 3 and 10 others.
  - Schedule N fair market value totals $26,901,149.
  - 9 transferred to a CF, and 7 filed a final return with no Schedule N Part I.
- **Three Rivers.** Cash of $128,105, investments of $5,265,136 and a remainder-trust interest of $50,045, totalling $5,443,286, all dated 2024-12-31, went to Sturgis Area CF.
- **Coastal.** $10,072,419 of "CASH" went to the San Diego Foundation on 2024-07-15.
  - Its final-return Schedule D reports **39 DAFs worth $5,658,142** against $0 total assets at year end. About 56% of the transfer was therefore DAF money, unnamed on Schedule N.
  - DAFRC carries Coastal's FY2024 row as filed and "Assume Operating Sponsor".
- **Greater White Bear Lake.** Seven Part II lines totalling $4,965,262 went to CommunityGiving. That is 96% of its $5,150,898 of beginning-of-year assets, leaving $26,355. It is an exit in substance, though not under the frame's rule, so 24 is a floor.

### Comparison with the mortality study (V38C-22 to -25)
- **The tier-A CFs reappear.** All 5 tier-A CFs reappear in frame B, and Sunbury's exit is dated 2020-07-27.
- **"About five times what DAFRC shows" is contradicted.**
  - Over the years both sources cover (2021–2023), frame B finds 12 geographic-CF exits. The DAFRC panel has 4 CFs with filed exits in those years, so the ratio is **3.0×**.
  - The 24/5 = 4.8 figure sets five years of filings against panel members only. Its 2024–2025 exits fall after the panel ends, and it counts Coastal, which DAFRC shows as operating.
  - DAFRC's own panel shows **more** CF exits than frame B: 35 in FY2021–FY2023.
- **"1.1%/yr is a rate for DAFRC-sized CFs" is contradicted.**
  - The 1.1% is the naive panel-exit rate: 36 exits in 3,175 CF sponsor-years at risk, FY2020–FY2023.
  - Of the 46 CF exit candidates, 28 survive without reported DAFs (tier B). Only 5 are organisational deaths (tier A), about 0.16%/yr.
- **The cf-consolidation rows reproduce** (C002, C010–C014, C017–C019).
- **Not checked:** three "geographic" calls are marginal: Ingleside Community Fund, Kingman CF (its assets went to Abbid Grotto) and Mobridge Community Fund.

## Exact corrections

### `research/mission-2026-11-14/gap1915-b4011-filing-frames.md`

- **Find:** "but the handful is about five times larger than DAFRC shows."
- **Replace with:** "but over the years both sources cover the handful is about three times what DAFRC’s filed exits show: 12 geographic-CF exits dated 2021–2023 against the 4 panel CFs (Shelby, Fairfield, Milbank, Rusk County) with filed exits in those years. A 24/5 ratio would set five years of filings against panel members only; 2024–2025 exits fall after the panel’s FY2024 end, and DAFRC still shows Coastal as operating. DAFRC’s own panel shows more CF exits (35 in FY2021–FY2023), but most are CFs that survive and stop reporting DAFs [V wave 38C]"

- **Find:** "The panel's CF exit rate (1.1%/yr) is therefore a rate for DAFRC-sized CFs. The very small CFs that DAFRC never tracked exit at a steady 2–6 per year in filed returns."
- **Replace with:** "The panel’s CF exit rate (1.1%/yr) counts DAFRC panel exits (36 in 3,175 CF sponsor-years at risk, FY2020–FY2023), most of them CFs that survive but stop reporting DAFs (tier B, 28 of 46 CF exit candidates). Only 5 CF candidates are organisational deaths (tier A), about 0.16%/yr, and that is the rate to compare with these filings. The very small CFs that DAFRC never tracked exit at a steady 2–6 per year in filed returns [V wave 38C]"

- **Find:** "- Operating in any form ranges from 15/25 = 60.0% (Wilson 95% 40.7–76.6%), counting unknowns as failures, to 25/25 (86.7–100%)."
- **Replace with:** "- Operating in any form ranges from 15/25 = 60.0% (Wilson 95% 40.7–76.6%), counting unknowns as failures, to 25/25 (86.7–100%).\n- Uncommon Giving fails the window test (§3.2; wave 32A). Without it the cohort is 24 (active 13, acquired 1, pivoted 0, unknown 10) and the lower bound is 14/24 = 58.3% (38.8–75.5%). Adding Bridges (active: TY2025 990 e-filed 2026-09-11) would give 16/26 = 61.5% (42.5–77.6%). The strict subset grows from 8 to 12 (active 6, acquired 1, unknown 5): 7/12 = 58.3% (32.0–80.7%) to 12/12 (75.8–100%) [V wave 38C]"

- **Find:** "That exclusion is the ambiguous one that wave 32A flagged."
- **Replace with:** "That exclusion is the ambiguous one that wave 32A flagged. Bridges’ parent is a wealth manager and trust company, not a DAF sponsor network (Telescope’s case), so under the rule that admits GivingTrax and GoodCoin it could equally be included; Givmo, Spiral and Overflow are admitted although their parents’ founding dates were not checked. Bridges’ only return is for TY2025, after the DAFRC panel ends, so DAFRC could not have listed it [V wave 38C]"

- **Find:** "| SAX08 | Ten in-window community foundations | Community-foundation exclusion |"
- **Replace with:** "| SAX08 | Ten in-window community foundations (7 are DAFRC panel members; 3 are outside DAFRC) | Community-foundation exclusion. The 98 non-DAFRC holders are 2 existing members (Groundswell, Percent Impact), 7 additions, 7 named exclusions (SAX01, SAX02, SAX04–SAX07), 3 CFs and 79 residual filers [V wave 38C]"

- **Find:** "  - 4 reported DAF accounts on the exit-year Schedule D: Rusk County 6, Fairfield 12, Milbank 4, Coastal 39."
- **Replace with:** "  - 4 reported DAF accounts on the exit-year Schedule D: Rusk County 6, Fairfield 12, Milbank 4, Coastal 39. Coastal’s final return reports $5,658,142 of DAF value against $0 total assets at year end, so about 56% of its $10.07m transfer to the San Diego Foundation, which Schedule N calls “CASH”, was DAF money; DAFRC carries Coastal’s FY2024 row as an operating sponsor [V wave 38C]"

- **Find:** "($4.97m, 2025);"
- **Replace with:** "($4.97m, 2025; 96% of its $5.15m beginning-of-year assets, leaving $26,355 at year end, so an exit in substance though not under this frame’s rule, which makes 24 a floor) [V wave 38C]"

- **Find:** "**Exiting CFs do not name DAF balances on Schedule N.**"
- **Replace with:** "**Exiting CFs do not name DAF balances on Schedule N, but DAF money still moves.** Coastal’s final-return Schedule D shows $5.66m of DAF value inside a $10.07m “cash” transfer, and Greater White Bear Lake moved 96% of its assets, DAFs named, in a Part II disposition [V wave 38C]"

- **Find:** "of which Neta and Monument account for $11.36m."
- **Replace with:** "of which Neta and Monument account for $11.36m. Part of the miss is timing: Neta, Monument, Overflow and DAFshare e-filed their only positive returns (TY2024) between 2025-10-12 and 2025-11-17, Givmo’s TY2024 return was filed in 2026, and DAFRC’s FY2024 is 30% imputed [V wave 38C]"

### `research/mission-2026-11-14/gap19-startup-cohort.md`

- **Find:** "| Bounds over all 18, depending on how the unknowns resolve | **66.7% (43.7–83.7%) to 100% (82.4–100%)** |"
- **Replace with:** "| Bounds over all 18, depending on how the unknowns resolve | **66.7% (43.7–83.7%) to 100% (82.4–100%)** |\n| With the 7 IRS e-file additions (n=25; gap1915-b4011) | 60.0% (40.7–76.6%) to 100% (86.7–100%); 14/24 = 58.3% (38.8–75.5%) without Uncommon Giving [V wave 38C]"

- **Find:** "| Operating in any form, unknown counted as surviving (upper bound) | 18/18 = 100.0% (82.4%–100.0%) |"
- **Replace with:** "| Operating in any form, unknown counted as surviving (upper bound) | 18/18 = 100.0% (82.4%–100.0%) |\n| With the 7 frame-D additions (n=25: active 13, acquired 1, pivoted 1, unknown 10) | 15/25 = 60.0% (40.7%–76.6%) to 25/25 = 100.0% (86.7%–100.0%); strict subset 7/12 = 58.3% (32.0%–80.7%) to 12/12 [V wave 38C]"

- **Find:** "   - DAFRC misses some in-window DAF holders: Groundswell Charitable Foundation, Goodstack Impact Foundation US and I Maaser Inc all file returns but are absent from the panel."
- **Replace with:** "   - DAFRC misses some in-window DAF holders: Groundswell Charitable Foundation, Goodstack Impact Foundation US and I Maaser Inc all file returns but are absent from the panel. An IRS e-file frame of 501(c)(3)s ruled 2021 or later (gap1915-b4011) finds 98 in-window Schedule D Part I holders outside DAFRC; 7 meet this note’s rules (Givmo, Spiral Giving Network, Neta, One Big Gift, DAFshare, Monument, Overflow; $12.39m of DAF assets in all). Groundswell reports DAFs only on its amended TY2024 return (12,808 accounts, e-filed 2026-01-28, Part IV line 6 answered “No”), and that frame finds no Part I DAFs on I Maaser’s Form 990s [V wave 38C]"

### `research/mission-2026-11-14/sponsor-mortality-analysis.md`

- **Find:** "Single-issue charities exit at 1.9%/yr, national sponsors at 1.4% and community foundations at 1.1%."
- **Replace with:** "Single-issue charities exit at 1.9%/yr, national sponsors at 1.4% and community foundations at 1.1%. These are panel-exit rates: of the 46 community-foundation exit candidates dated FY2020–FY2023, 5 ceased (tier A, about 0.16%/yr) and 28 survive without reported DAFs (tier B). An IRS e-file screen of CF-named and NTEE T31 filers (gap1915-b4011) finds 24 geographic CFs that filed exit returns dated 2021–2025, 19 outside the panel and 23 with under $10m of assets; for 2021–2023 it finds 12, against 4 panel CFs with filed exits [V wave 38C]"

### `research/mission-2026-11-14/full-universe-990-harvest-and-corrected-totals.md`

- **Find:** "   - **For sponsor counts the miss is material:** about 27–37% more sponsors than DAFRC's roughly 1,450–1,510."
- **Replace with:** "   - **For sponsor counts the miss is material:** about 27–37% more sponsors than DAFRC's roughly 1,450–1,510.\n   - The same holds for entrants: 136 of the 179 Schedule D Part I holders among 501(c)(3)s ruled 2021 or later (2022–2026 e-file index) are outside DAFRC, but only 7 are DAF startups under the cohort rules ($12.39m in all), and the largest, Bridges Philanthropic Fund ($107.0m), first filed for TY2025, after the panel (gap1915-b4011) [V wave 38C]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.47 New-sponsor and community-foundation exit frames (validated, wave 38C)\n\n**New-sponsor and community-foundation exit frames** (validated, wave 38C). Both IRS e-file frames reproduce byte for byte. Of 36,115 new 501(c)(3) Form 990 filers ruled 2021 or later, 179 report DAF accounts on Schedule D Part I, and 43 of them are in the DAFRC panel. Part IV line 6 is not a safe filter: 14 holders never answer “Yes”, among them Groundswell, whose amended TY2024 return reports 12,808 accounts. Of 98 in-window holders outside DAFRC, most are not sponsors; 7 small ones ($12.39m in all) join the startup cohort, which becomes 25 with survival of 60.0–100% (58.3% at the low end without Uncommon Giving). Bridges Philanthropic Fund ($107.0m, ruled 2025) is excluded as a wealth manager’s product, a call the cohort rules leave open. Twenty-four small geographic community foundations filed exit returns in 2021–2025, 19 outside DAFRC. For 2021–2023 that is three times the panel’s filed CF exits, not five, and fewer than DAFRC’s 35 CF panel exits, which are mostly surviving CFs that stopped reporting DAFs (repo [`validation-wave38c-report.md`](mission-2026-11-14/validation-wave38c-report.md)) [V wave 38C]\n\n---\n\n## Source register"
