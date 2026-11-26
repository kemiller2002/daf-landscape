# Validation wave 29: new directions N27–N30 (sponsor financial resilience, nonprofit-side experience, public opinion, league table and concentration)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave29.
**Register:** [`validation-register-wave29.csv`](../../data/mission-2026-11-14/validation-register-wave29.csv), rows V29-01 to V29-36.
**Documents validated:**
- N27: [direction-sponsor-financial-resilience.md](direction-sponsor-financial-resilience.md), `sponsor-financial-resilience-2021-2024.csv` (430 rows) and `scripts/mission_sponsor_resilience.py`
- N28: [direction-nonprofit-side-experience.md](direction-nonprofit-side-experience.md) and `nonprofit-side-daf-issues-2021-2026.csv` (60 rows)
- N29: [direction-public-opinion-dafs.md](direction-public-opinion-dafs.md) and `daf-opinion-polls-positions-2021-2026.csv` (59 rows)
- N30: [direction-league-table-concentration.md](direction-league-table-concentration.md), `daf-sponsor-league-table-fy2021-2025.csv` (267 rows), `daf-concentration-fy2021-2025.csv` (44 rows) and `scripts/mission_league_table.py`

**Method:** public sources only. I did not log in, submit forms, solve or bypass CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching any page on it, checking the ClaudeBot, anthropic-ai and `*` groups. **I did not use crt.sh** and fetched nothing from www.irs.gov. For each claim I formed a verdict from the primary source first and compared it with the documents afterwards. The sources were:
- **N27:**
  - a **re-run of the script** on a copy of the repo in scratch, with a **fresh, empty cache** and `--fetch`. All 415 returns were re-read: 408 from the GivingTuesday mirror (robots.txt 404, no rules) and 7 from TEOS members cached by earlier batches. apps.irs.gov robots.txt redirects to a 404 page, and no request was made to it;
  - an **independent regex parse** of the full XML of 11 returns: Fidelity, NPT ×4, MS GIFT, Renaissance, Johnson, CAF America, NYCT and AOGF.
- **N28:** the DAFRC manager and donor survey PDFs (via static1.squarespace.com, robots 404); the Chariot "All Checks, No Balance" page; Fidelity's nonprofit FAQ; the Blackbaud NPOconnect check-reissue help page (robots 404); the AFP RFP PDF; the NonProfit Times article; and two AASP FundSvcs threads.
- **N29:** the IPS/Inequality.org 2024 deck and 2022 article; Philanthropy Daily; the Lilly School release; the Independent Sector 2025 trust PDF and 2025 TargetPoint release; the IS/TargetPoint 2023 deck; Associations Now (2026); Ripon Advance; IPS Donor Revolt; and the CFAI blog (2022).
  - The BofA Private Bank article returned 403 and was not retried. cof.org returned 403.
- **N30:**
  - a **re-run of the script** with the session's `netpayout990/` cache;
  - an **independent rebuild** of corrected sponsor values from the DAFRC panel plus every `applied = 1` correction row, with CR and HHI recomputed.

## Headline

The four documents hold up on their numbers. Of 36 claims, 28 are confirmed, 6 partially confirmed, 1 contradicted and 1 unverifiable. **Both scripts reproduce byte-for-byte**: N27 from a fresh download of every return, and N30 from repo data.

**What holds independently:**
- **N27 sponsor resilience:**
  - The re-run CSV is identical to the repo file: 415 returns, all parsed; 400 rows; 381 analysable.
  - At nationals, median DAF share of net assets is 99.6% (affiliated) and 99.7% (independent).
  - Median R1 cover is 29.4 months (affiliated) against 2.2 months (independent). Community foundations: 417 months, but 1.6 months under R5.
  - MS GIFT's TY2024 DAF value exceeds its net assets by $133,374,179, exactly its Part X liabilities.
  - Fidelity's non-DAF net assets equal its Schedule D column (b) value to the dollar in all four years ($381,019,657 in TY2024).
  - Program-service revenue is $0 in all 60 affiliated sponsor-years. Eleven returns match the XML field by field.
- **NPT FY2023 $22.84bn (V29-09).** **It is a real filed value, not a parse error.** `DonorAdvisedFundsVlEOYAmt` is 22843599245 in return 202431429349301368, the only Form 990 indexed for the period ending 2023-06, with no amended return.
  - The same return's Part X total net assets are $27.92bn.
  - The roll-forward from FY2022 gives $26.29bn before market gains. Reaching FY2024's $42.12bn from $22.84bn would need a 32% return, against 14% from about $27.9bn.
  - In every other year NPT's DAF value is at or above its net assets.
  - It is most likely a filer reporting error [I]. DAFRC carries the same figure, so it also enters N30's FY2023.
- **N28 nonprofit side:**
  - Counts reproduce: 60 rows; 48 coded complaint, mixed and finding rows; identity 16/48 (7/5/4); 15/34 excluding the 14 Benevity rows.
  - DAFRC manager survey: 128 sponsors, 86% community foundations, defaults 36/24/35/5/1%. Donor survey: 49% always or almost always thanked.
  - The Fidelity reissue sentence, the YourCause conditions and the AFP–Fidelity Catalyst Fund funding (January 2024, three years) are all verbatim.
  - AASP's `/discussion/` pages are robots-allowed and readable without login. The CSV forum rows contain no poster names, institutions or emails.
- **N29 public opinion:**
  - Ipsos/IPS June 2022: n=1,005, 69% payout, 72% within 5 years. Ipsos February 2024: n=1,005, 71%, and "79% … increased from 72%".
  - Lilly: 11.4% familiar (n=1,334). IS/TargetPoint: 88/85/87/88%.
  - Philanthropy trust 33% → 29% in 2026 (Associations Now). HNW trust 29% in 2025, down 2.
  - Buchanan and 32 Ways and Means colleagues, April 19 2024. Donor Revolt, April 4 2024.
- **N30 league table:**
  - The re-run is identical and corrected totals rebuild to the dollar ($323,269,551,062 FY2024).
  - My own rebuild gives the same CR and HHI for every FY × metric: assets CR5 51.0 → 56.9 and HHI 734 → 853; grants CR5 53.6 → 46.6 and HHI 803 → 653.
  - Top-50 shares: assets 83.1–85.5% and grants 77.9–81.3%. Netted FY2024 grant HHI 669 (673.7–683.5).
  - GS DAPF FY2021 6.6% → 3.0%; SVCF FY2024 4.6% → 2.5%. FY2025: 899 sponsors, 67.6% of assets, 24 of the top 50.

**What needs correcting or qualifying:**
1. **N27 §0 ranges (V29-05), contradicted.**
   - MS GIFT is not "−$133m in every year". R1 is −$107.0m, −$97.7m, −$86.2m and −$133.4m; the doc's own §4 has these right.
   - Renaissance runs from −$11.9m to −$80.7m, not −$17m to −$81m. Johnson is −$1, not exactly $0.
   - The "Schedule D before liabilities" pattern is not unique to MS GIFT. American Gift Fund's R1 equals its liabilities in all four years, and Renaissance's in TY2021 and TY2024.
2. **NPT FY2023 in N30 (V29-34).** The FY2023 league table and concentration use the $22.84bn that N27 excludes as a break.
   - With NPT at Part X net assets, FY2023 assets CR3 rises from 42.9 to 44.0, CR5 from 52.9 to 53.8, HHI from 801 to 808, and NPT's share from 8.9% to about 10.7%.
   - The endpoints and the trend are unchanged.
3. **Chariot 1–2 days (V29-15).** The figure belongs to the fastest three providers (Pledger, The Donors Fund and Fidelity, all ACH), not to all ACH providers.
4. **YourCause (V29-18).** The 120-day limit rests on "clients' guidelines" that return funds "to the company" or redirect them. This is a workplace-giving intermediary rule, not a DAF sponsor rule.
5. **CMP-241 redate (V29-16): accepted.** The post reads "Jan 20". It analyses six months of 2025 data, says checks are "not where we want to be in 2026", and its image is versioned 2026-01-26. So the date is 2026-01-20, with the year inferred.
6. **"79% partially anonymous" (V29-14): the doc's ruling is upheld.** NPT's sentence is not supported by either DAFRC survey. In the donor survey, 39% recommend partially anonymous grants at least occasionally, and 79% *of those* feel identifiable. Keep it out of headlines.
7. **N29 wording:**
   - **Awareness (V29-23).** The 17–19% is "aware of DAFs and how they work"; the no-payout item is 17–18%.
   - **HNW trust (V29-25).** The 2022–2023 HNW values (34%, 33%) are inferred from chart layout, not printed.
   - **TargetPoint (V29-27).** The 2022 wave's fieldwork is August 2022.
   - **2022 letter (V29-29).** The 6 D / 5 R split comes only from Chronicle summaries. CFAI calls it a "Dear Colleague" letter.
8. **BofA 98% / 80% (V29-28): unverifiable.** The page returned 403. Secondary coverage confirms 1,431 respondents, about 1 in 10 using a DAF, and 75% planning to increase, but none of the reason percentages.

## Limits

- **Not fetched:** bofa.com article (403), cof.org (403), the Chronicle and Wealthmanagement (robots), the Philanthropy Roundtable, the IS 2026 PDF, and NPT's audited statements, which would settle the FY2023 Schedule D value.
- **Not re-checked:**
  - N28: the donor-side corpus counts (85 and 53); FreeWill figures; the 7 AASP threads not re-read.
  - N29: Harris, YouGov, GSG, Give.org, DS01–DS06, and most EL rows.
  - N30: entrant and exit reasons; the FY2025 provisional entrants.
- **Pages change.** All quotes are as of 2026-11-15.

## Exact corrections

### `research/mission-2026-11-14/direction-sponsor-financial-resilience.md`
1. **§0 item 1, affiliated R1 ≤ 0.**
   - **Find:** "Morgan Stanley GIFT (−$133m in every year, TY2021–2024), Renaissance (−$17m to −$81m) and Johnson Charitable Gift Fund (exactly $0)."
   - **Replace with:** "Morgan Stanley GIFT (−$86m to −$133m every year, TY2021–2024, each equal to its total liabilities), Renaissance (−$12m to −$81m) and Johnson Charitable Gift Fund (−$1, i.e. $0) [C; V wave 29]."
2. **§1.6, NPT break.**
   - **Find:** "  - **NPT TY2022 (FY Jun-2023):** Schedule D $22.84bn against Part X $27.92bn. A roll-forward from FY2022 gives about $26.3bn before market gains; see P-B44N27-01."
   - **Replace with:** "  - **NPT TY2022 (FY Jun-2023):** Schedule D $22.84bn against Part X $27.92bn. A roll-forward from FY2022 gives about $26.3bn before market gains; see P-B44N27-01.\n    - Wave 29 checked the XML: `DonorAdvisedFundsVlEOYAmt` is 22843599245 in return 202431429349301368, the only Form 990 for that period (no amendment). It is a real filed value, not a parse error. It is most likely a filer error [I]: reaching FY2024's $42.12bn from it would need a 32% return. DAFRC carries the same value, so N30's FY2023 uses it [V wave 29]."
3. **§4 Readings, MS GIFT.**
   - **Find:** "Schedule D appears to report DAF value before liabilities (grants payable), so its true own equity is about $0."
   - **Replace with:** "Schedule D appears to report DAF value before liabilities (grants payable), so its true own equity is about $0. The same identity holds for American Gift Fund in all four years and for Renaissance in TY2021 and TY2024 [C; V wave 29]."

### `research/mission-2026-11-14/direction-nonprofit-side-experience.md`
1. **§0, Checks row, Chariot.**
   - **Find:** "Check-paying providers averaged **7–162 days**; ACH providers paid in 1–2 days"
   - **Replace with:** "The 18 check-paying providers averaged **7–162 days**; the fastest three (Pledger, The Donors Fund, Fidelity, all ACH) averaged 1–2 days [V wave 29]"
2. **§0, Checks row, YourCause.**
   - **Find:** "YourCause/Blackbaud may forfeit voided funds [F]."
   - **Replace with:** "YourCause/Blackbaud may forfeit voided funds, under corporate giving-programme client rules rather than a DAF sponsor's [F; V wave 29]."
3. **§2.2, YourCause.**
   - **Find:** "checks cannot be reissued.\" ([Blackbaud]"
   - **Replace with:** "checks cannot be reissued.\" The 120-day limit exists because \"clients have guidelines in place that state funds are returned to the company\" or redirected to another charity. It is a workplace-giving rule (YourCause CSRconnect and similar), not a DAF sponsor's [V wave 29] ([Blackbaud]"
4. **§3 reading 4, Benevity and Chariot.**
   - **Find:** "Removing Benevity halves the delay count."
   - **Replace with:** "Removing Benevity cuts the delay count from 16 to 7. Three of the 16 delay rows come from one Chariot page (NPS-023, NPS-024 and the carried NPS-059/CMP-241) [C; V wave 29]."

### `research/mission-2026-11-14/direction-public-opinion-dafs.md`
1. **§0, awareness.**
   - **Find:** "– Ipsos/IPS: only **17–19% aware** that DAFs have no payout rule."
   - **Replace with:** "– Ipsos/IPS: only **17–19%** say they know what DAFs are and how they work, and 17–18% knew that DAFs have no payout rule (2024 / 2022) [V wave 29]."
2. **§0, HNW trust.**
   - **Find:** "went **34% (2022) → 33% → 31% → 29% (2025)** [F/C;"
   - **Replace with:** "went **34% (2022) → 33% → 31% → 29% (2025)** [29% and the −2 change F; the 2022–23 values C, inferred from chart layout (§6); V wave 29;"
3. **§0, BofA donor reasons.**
   - **Find:** "DAF users cite tax-free growth (98%), maximising tax benefits (96%) and simplicity (94%) [F]."
   - **Replace with:** "DAF users cite tax-free growth (98%), maximising tax benefits (96%) and simplicity (94%) [F; the page returned 403 on the wave-29 re-fetch, so the reason percentages are not re-verified]."
4. **§2, TargetPoint dates.**
   - **Find:** "| PO16–19 | Dec 2021; Sep 2022; Aug 2023; Feb 2025 |"
   - **Replace with:** "| PO16–19 | Dec 2021; Aug 2022 (released Sep 2022); Aug 2023; Jan–Feb 2025 |"
5. **§4, 2022 letter.**
   - **Find:** "| 2022-03-07 | 11 Ways and Means members (6 D, 5 R) | letter |"
   - **Replace with:** "| 2022-03-07 | 11 Ways and Means members (6 D, 5 R per Chronicle coverage; a bipartisan \"Dear Colleague\" letter per CFAI [V wave 29]) | letter |"

### `research/mission-2026-11-14/direction-league-table-concentration.md`
1. **§2, top-10 table, FY2023 NPT.**
   - **Find:** "| 3 | Vanguard 16.00 (6.8%) | **NPT 21.52 (9.4%)** | NPT 22.84 (8.9%) |"
   - **Replace with:** "| 3 | Vanguard 16.00 (6.8%) | **NPT 21.52 (9.4%)** | NPT 22.84 (8.9%; anomalous filed value, see §5) |"
2. **§5, limitation added.**
   - **Find:** "- **Fiscal years mix period ends.**"
   - **Replace with:** "- **NPT FY2023 (FYE 2023-06) is an anomalous filed value.** The $22.84bn is NPT's filed Schedule D line 4, and DAFRC carries it. The same return's Part X net assets are $27.92bn, and N27 excludes the value as a `daf_share_break`. Using $27.92bn would move FY2023 assets CR3 from 42.9% to 44.0%, CR5 from 52.9% to 53.8% and HHI from 801 to 808, and NPT's share from 8.9% to about 10.7%. FY2021, FY2024 and the trend direction are unaffected [C; V wave 29].\n- **Fiscal years mix period ends.**"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.25.** Add "### 11.26 New directions N27–N30 (validated, wave 29)", containing the paragraph below. If §11.26 is already taken, use the next free number.

   > **New directions N27–N30 (validated, wave 29).**
   > - **Sponsor financial resilience (Form 990, TY2021–24, top 100; the script reproduces exactly from a fresh download of all 415 returns).**
   >   - At national sponsors, DAFs are 99–100% of net assets, so the 990 can only bound a sponsor's own reserve. Median non-DAF net assets cover 29.4 months of operating cost at bank- and broker-affiliated nationals, against 2.2 months at independent nationals.
   >   - Several nationals show zero or negative non-DAF net assets. At MS GIFT the gap equals its liabilities exactly (−$133m in TY2024), so Schedule D reports DAF value before liabilities. NPT, Renaissance, CAF America and AOGF are also below zero.
   >   - Fidelity's non-DAF net assets are exactly its Schedule D "other funds" ($381m). Program-service revenue is $0 at all 15 affiliated sponsors: the DAF fee is an internal transfer.
   >   - Community foundations show 417 months of cover, but only 1.6 months once board-designated endowment is excluded.
   >   - NPT's FY2023 Schedule D value ($22.84bn against $27.92bn of net assets) is a real filed figure, most likely a filer error.
   > - **Nonprofit-side experience (60 coded rows, 2021–26).**
   >   - Identity and data issues lead the nonprofit complaints: 16 of 48, and 15 of 34 excluding Benevity.
   >   - Defaults, not chosen anonymity, drive the problem. Only 36% of sponsors default to full contact data, and 35% to fund name only (DAFRC, 128 sponsors, 86% community foundations). Only 49% of donors say they are always thanked.
   >   - In Chariot's one-nonprofit sample, check-paying providers took 7–162 days and the fastest ACH providers 1–2 days.
   >   - Only the donor can trigger a Fidelity reissue. YourCause's forfeiture rule is a workplace-giving rule.
   >   - AFP's DAF curriculum is funded by Fidelity Charitable. NPT's "79% partially anonymous" headline is not supported by DAFRC data.
   > - **Public opinion (2021–26).**
   >   - The only DAF policy polls are advocate-sponsored Ipsos opt-ins (n=1,005): 69% (2022) and 71% (2024) back a 10% payout, and support for granting within 5 years rose from 72% to 79%.
   >   - Only 17–19% know how DAFs work (Lilly: 11.4% familiar).
   >   - Trust in high-net-worth philanthropy is 29% (2025), and trust in philanthropy fell from 33% to 29% (2026). Universal-deduction support runs at 85–88%.
   >   - Elite opinion runs against reform, including a 33-member Ways and Means letter (2024).
   > - **League table and concentration (corrected DAFRC values; reproduced and independently rebuilt).**
   >   - Fidelity holds 20.5–21.7% of assets. NPT ($42.12bn) passed DAFgiving360 ($40.94bn) in FY2024. The top 50 hold 83–86% of assets and 78–81% of grants.
   >   - Asset concentration rose (CR5 51.0 → 56.9%, HHI 734 → 853) while grant concentration fell (CR5 53.6 → 46.6%, HHI 803 → 653). Both are "unconcentrated" by HHI, and R5 netting barely moves them (FY2024 grant HHI 669).
   >   - FY2023 uses NPT's anomalous filed value. Corrected, CR5 would be about 53.8% instead of 52.9%.
   >   - FY2025 is partial: 899 filers, 67.6% of assets.

## Data-file notes (not .md; for the owning agent)

- **`sponsor-financial-resilience-2021-2024.csv`:** no value changes. All 11 spot-checked returns match the XML.
- **`nonprofit-side-daf-issues-2021-2026.csv`:**
  - NPS-023: qualify the "ACH providers paid in 1-2 days" text as "fastest 3 providers (ACH)".
  - The YourCause row: add "corporate giving-programme client rule".
  - Accept the CMP-241 / NPS-059 redate to 2026-01-20, date_precision "day (year inferred)", in `daf-user-complaints-corpus.csv`.
- **`daf-opinion-polls-positions-2021-2026.csv`:**
  - DS07: note "page 403 on wave-29 re-fetch; reasons not re-verified".
  - PO17: fieldwork "Aug 2022".
  - EL07: add "CFAI: Dear Colleague letter".
- **`daf-sponsor-league-table-fy2021-2025.csv` / `daf-concentration-fy2021-2025.csv`:** add a flag on the NPT FY2023 row, `filed_sched_d_lt_part_x_net_assets (27.92bn)`. No value change is required while DAFRC values govern.
