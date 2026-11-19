# Validation wave 36A: CF local share (top 100) and the corporate-DAF segment

**Date:** 2026-11-19 · **Validator:** independent-validation-agent-wave36a · **Register:** [`data/mission-2026-11-14/validation-register-wave36a.csv`](../../data/mission-2026-11-14/validation-register-wave36a.csv) (V36A-01 to V36A-36)

**Studies checked**
- **Study 1:** [b42n21-02-cf-local-share-top100.md](b42n21-02-cf-local-share-top100.md), with its CSV `cf-local-share-top100-2026-11-19.csv` and script `scripts/mission_cf_local_share_top100.py`.
- **Study 2:** [b41n18-01-corporate-daf-segment.md](b41n18-01-corporate-daf-segment.md), with its CSV `corporate-daf-segment-2026-11-19.csv` and script `scripts/mission_b41n18_01_corporate_segment.py`.

**Method.**
- Both scripts were re-run into scratch roots (`$SCRATCH/v36a/root1`, `root2`). The repo CSVs were not touched.
- Statistics were recomputed independently with numpy, scipy and statsmodels from the committed CSV.
- 22 Form 990 XMLs were re-fetched from the GivingTuesday mirror of IRS TEOS. That host has no robots.txt (404), and every request used User-Agent `research-script/1.0`.
- 7 first-party documents were re-fetched after robots.txt checks (log in `$SCRATCH/v36a/robots/log.tsv`):
  - svcf.org: 200, allows /assets;
  - fidelitycharitable.org: 200, allows /content/dam/fc-public/docs/insights;
  - cafamerica.org: 200, crawl-delay 10, honoured;
  - growyourgiving.org: 200, allows all.
- No outreach, logins or forms. crt.sh, certspotter and sec.gov were not used.

## Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| CF local share, top 100 (V36A-01 to -18) | 18 | 13 | 3 | 2 | 0 |
| Corporate DAF segment (V36A-19 to -36) | 18 | 13 | 5 | 0 | 0 |
| **Total** | **36** | **26** | **8** | **2** | **0** |

## Findings

### Study 1: CF local share, top 100

**What holds**
- **Reproduction.** The script reproduces the CSV byte for byte (md5 `65a2a303…`) and the summary JSON exactly, in 12.5 s from the cached lines.
- **Medians and correlations.** Independent recomputation matches every headline figure:
  - medians 83.07% / 69.35% / 54.51%, pooled 65.3%;
  - Pearson −0.447 (Fisher CI −0.595 to −0.269);
  - controlled OLS slope −0.248 (HC1 CI −0.394 to −0.103), R² 0.35;
  - all four sub-samples and the metro and county models agree to ±0.001.
- **Robustness.** The negative slope survives every extra check:
  - a multi-state-metro dummy as a control: −0.229;
  - CFs with Schedule I coverage of at least 50% only: −0.238;
  - without the two capped CFs: −0.250;
  - without SVCF and Chicago: −0.241;
  - without the 4 CFs under 50% in-state: −0.191 (−0.325 to −0.057);
  - leave-one-out: −0.278 to −0.224;
  - SE Michigan included at |Schedule D| ÷ Part IX = 0.96: −0.232.
- **Covariate.** The DAF-share covariate is built as described.
  - SE Michigan's filed DAF grants are negative in both XMLs (−$64,258,868 and −$129,289,062).
  - CF of New Jersey's Schedule D DAF grants ($193.6m) exceed its Part IX grants ($165.3m), so its share is capped.
  - The code flags a CF as negative if any of its fiscal years is negative, and caps the share at 1.
- **Spot-check.** Six CFs re-parsed from fresh XMLs with an independent parser and whitelist exclusion match exactly: Lancaster 97.34%, Idaho 98.01%, Delaware 53.20%, Greater Cincinnati 42.49%, Toledo 83.04% and CF of New Jersey 38.59%.

**What fails or needs qualifying**
1. **Omaha CF's Schedule I is truncated (V36A-07, contradicted).**
   - Each XML year has 8 RecipientTable rows, all alphabetically first, against 824 and 863 counted 501(c)(3) recipients.
   - The 16 lines total $0.83m, against $216.6m of Part IX line 1 grants (0.4%).
   - The study's "highest own-state share, 98.8%" is therefore not a measurement. The highest measured share is Idaho CF at 98.0%.
   - The acceptance check could not catch this: it compares the XML with a cache built from the same XML.
   - Without Omaha the result gets slightly stronger (r −0.472; slope −0.255). Omaha was a leverage point on the log Schedule I size control.
2. **Armstrong County CF is not a top-100 CF (V36A-08, contradicted).**
   - Its rank 73 rests on a DAFRC FY2024 paper-submission row: $148.2m and 479 accounts, with grants imputed.
   - Its own Schedule D shows $8.9m (FY2023, 31 accounts) and $9.5m (FY2024, 28 accounts).
3. **The multi-state-metro story explains Kansas City, not Cincinnati, Delaware or New Jersey (V36A-13).**
   - Cincinnati's out-of-state dollars go mainly to The Nature Conservancy (Arlington, VA; $58.2m) and Conservation International (DC; $25.9m).
   - Delaware's largest out-of-state recipient is The Conservation Fund (VA; $10.75m), and CF of New Jersey's is GBSC Foundation (SC; $14.25m).
   - So the big-city confound is mainly the address of national headquarters, which is the place-of-benefit problem, rather than commuter metros.
4. **The causal wording is acceptable but incomplete (V36A-11).**
   - The bivariate fit (intercept 1.008, slope −0.344) is what a pure composition model gives if non-DAF grants are about 100% in-state and DAF grants about 66% in-state. This is mechanical and says nothing about donor intent.
   - A reverse direction is also possible: a CF with a national brand or grantees may draw more DAF donors.
   - The study's "association only" framing is right, but it should name both readings.
5. **Smaller CFs are more local only unconditionally (V36A-04, V36A-17).**
   - Once DAF share is controlled, neither size term is significant for own-state share.
   - For the own-metro and own-county models, log Schedule I dollars is significant. The study's "size controls not significant" applies to own-state share only.

### Study 2: corporate DAF segment

**What holds**
- **Reproduction.** The script reproduces the 76-row CSV byte for byte, with all [C] and [I] figures: 3.930%, 3.379%, 9.123%, a base of $9,947.9m and $278.2m–$690.6m.
  - Its SV and FC inputs are hard-coded, so they were re-read from the PDFs.
- **SVCF audited statements (all four re-fetched).** Every corporate-advised figure matches the text "These funds made grants of approximately …":
  - 2021 $100m and 2022 $175m (FY2022 statement);
  - 2023 $134m (FY2023 and FY2024 statements);
  - 2024 $189m and 2025 $153m (FY2024 and FY2025 statements).
  - Donor-advised grants are $2,155m, $2,553m, $4,657m, $3,077m and $2,051m.
  - "Corporate Advised" is a sibling programme heading of "Advised Funds", so corporate ÷ (corporate + donor-advised) is the right share.
  - The study cites the wrong location: the text is in Note 1 (Programs), not in net-asset notes.
- **Fidelity Giving Reports.**
  - 2025 report: 518 corporate DAFs; $237M (2023) and $525M (2024) of corporate grants; 24,975 grants averaging $21,024; $14.9bn of total grants.
  - 2026 report: 556 corporate DAFs; $539.8M of corporate grants; 26,036 grants averaging $20,732; $18.3bn of total grants.
  - Shares: 3.52% (2024) and 2.95% (2025). Corporate DAFs are 0.247% of accounts.
- **No 990 splits corporate and individual DAFs (10-return sample, fresh XMLs).**
  - The sample covers CAF, CCF, Columbus, Atlanta, FFTC, GKCCF, NPT, RPA, SVCF and TBF.
  - Schedule D has only the four DonorAdvisedFunds fields.
  - "Corporation" text appears only in donor-type lists or in unrelated contexts.
  - All 10 Schedule D totals match the CSV.
- **Other sources confirmed.**
  - The CAF America consolidating schedules split by entity only: CAF America, CADF and CAF Canada.
  - The Tides CY2024 Schedule I line to AOGF (EMPLOYEE GIVING) is $1,696,333.
  - The GKCCF sentence is on the live page word for word.
  - The NYCT CY2023 Schedule D grants are $13,369,298.
  - The AOGF columns ($1,390,021,897 and $935,709,539) and the 0.15× and 5.6× ratios are correct.

**What needs qualifying**
1. **The 9.1% ceiling (V36A-25).** The arithmetic is right, but the figure is a ceiling for the Fidelity + SVCF + AOGF pool, not for the market.
   - It mixes periods (CY2025 with FYE 2026-03) and puts AOGF's non-DAF column in the denominator.
   - Its level is set mainly by AOGF's weight in the pool.
   - AOGF's own Schedule D Part XIII says its DAFs are where corporate donors give with ongoing advice. The column is therefore probably mostly corporate, so 9.1% is closer to the pool's value than to a loose bound [I].
2. **The [I] extrapolation (V36A-26).** The range is reproduced, but two caveats are missing.
   - Whether corporate funds sit inside Schedule D at all is unknown, even at SVCF.
   - CAF America's Schedule D does not match CAF America's own column in its consolidating schedule. Its end-of-year value ($441.3m) is near the consolidated figure ($430.8m), so the base may include the UK and Canadian affiliates.
   - Low confidence remains the right label.
3. **The Tides–AOGF inference (V36A-31).** One grant into an employee-giving program does not show that corporate money "leaves Tides through AOGF".
4. **Small count errors (V36A-28, V36A-34).**
   - 47 returns overlap with the harvest, not 46. One of them (Boston Foundation, 202641269349301584) has blank harvest values.
   - The headline says 4 community-foundation sites were unreadable, but §6 lists 5.
5. **The GKCCF "hundreds of companies" floor (V36A-32)** is undated marketing copy about companies, not funds. The ≥200-fund floor is an inference.

**Direction doc.** [direction-corporate-dafs.md](direction-corporate-dafs.md) stays consistent: Fidelity 2.9%, SVCF 6.9% and 5.8%, and AOGF 695 accounts with $1,390.0m of grants all match. The corrections below add the 2021–2025 SVCF series, the pooled 3.4%–3.9%, the 14-sponsor null result, the pool-only status of 9.1% and the four private-side programs (CN01–CN04).

## Exact corrections

Apply in order. Each Find is verbatim and occurs exactly once in its file as it stands on 2026-11-19. In both values, `\n` stands for a newline, and quotations inside a value use curly quotes. A script check confirmed each Find occurs exactly once (see the end of this section).

### `research/mission-2026-11-14/b42n21-02-cf-local-share-top100.md`

- **Find:** "- **Highest:** Omaha CF 98.8%, Idaho CF 98.0%, Lancaster County CF 97.3% (DAF share 19%), Greater Kanawha Valley 97.0%, Central New York CF 95.4%, Grand Rapids CF 94.6%."
- **Replace with:** "- **Highest:** Idaho CF 98.0%, Lancaster County CF 97.3% (DAF share 19%), Greater Kanawha Valley 97.0%, Central New York CF 95.4%, Grand Rapids CF 94.6%. Omaha CF shows 98.8%, but its XML Schedule I is truncated. Each year has 8 RecipientTable rows, against 824 (FY2023) and 863 (FY2024) 501(c)(3) recipients counted in the same schedule. Its 16 lines ($0.83m) cover 0.4% of its Part IX line 1 grants, so its shares are not measured. Without Omaha, the median own-state share is 83.0%, Pearson r is −0.47 and the controlled slope is −0.255 (HC1 CI −0.397 to −0.114) [V wave 36A]"

- **Find:** "range 20.0% Chicago Community Trust to 98.8% Omaha CF)"
- **Replace with:** "range 20.0% Chicago Community Trust to 98.8% Omaha CF; Omaha’s XML Schedule I is truncated to 8 of 800+ recipients a year, so the highest measured share is Idaho CF at 98.0%) [V wave 36A]"

- **Find:** "| 26 | Omaha Community Foundation"
- **Replace with:** "| 26 | Omaha Community Foundation (XML Schedule I truncated to 8 of 800+ recipients a year; shares not measured) [V wave 36A]"

- **Find:** "| 73 | Armstrong County Community"
- **Replace with:** "| 73 | Armstrong County Community (ranked on a DAFRC paper-submission value; own Schedule D DAF assets $9.5m) [V wave 36A]"

- **Find:** "- **Size ranking.** The universe is ranked by DAF assets, not total assets."
- **Replace with:** "- **Size ranking.** The universe is ranked by DAF assets, not total assets. It also inherits DAFRC errors. Armstrong County CF (rank 73) is ranked on a DAFRC FY2024 paper-submission value of $148.2m (479 accounts). Its own Schedule D shows $8.9m (FY2023, 31 accounts) and $9.5m (FY2024, 28 accounts), so it does not belong in the top 100 [V wave 36A]"

- **Find:** "  - Kansas City, New Jersey, Cincinnati and Delaware sit in metros that cross state lines."
- **Replace with:** "  - Kansas City, New Jersey, Cincinnati and Delaware sit in metros that cross state lines. Only at Kansas City is the gap mostly the neighbouring state (KS is about a quarter of dollars). Cincinnati’s largest out-of-state recipients are The Nature Conservancy in Arlington, VA ($58.2m) and Conservation International in DC ($25.9m). Delaware’s largest is The Conservation Fund in VA ($10.75m), and CF of New Jersey’s is GBSC Foundation in SC ($14.25m). These are national headquarters addresses, not neighbouring-state recipients [V wave 36A]"

- **Find:** "The relationship is an association across CFs, not a measured effect of DAF grants themselves."
- **Replace with:** "The relationship is an association across CFs, not a measured effect of DAF grants themselves. It is also close to what a pure composition effect would give. The bivariate fit is 100.8% in-state at a DAF share of 0 and 66.4% at a share of 1, as if non-DAF grants were all in-state and DAF grants two-thirds in-state. The data cannot separate this from donor-base confounding. The direction may also run the other way: a CF with a national brand or national grantees may draw more DAF donors [V wave 36A]"

- **Find:** "For own-county share it is −0.23, but the CI (−0.46 to +0.003) includes zero [C]."
- **Replace with:** "For own-county share it is −0.23, but the CI (−0.46 to +0.003) includes zero [C]. An independent re-estimation (statsmodels, HC1) reproduces every slope and CI to ±0.001. A multi-state-metro dummy used as a control, instead of dropping those CFs, gives −0.23 (−0.37 to −0.09). Dropping the 4 CFs under 50% in-state gives −0.19 (−0.33 to −0.06). Leave-one-out slopes range from −0.28 to −0.22 [V wave 36A]"

- **Find:** "**Smaller CFs are more local**"
- **Replace with:** "**Smaller CFs are more local** (unconditional medians; with DAF share held fixed, neither size term is significant for own-state share, §3.2) [V wave 36A]"

- **Find:** "**All 190 passed.**"
- **Replace with:** "**All 190 passed.** The check compares each XML with a cache parsed from the same XML, so it cannot catch a truncated schedule. Omaha CF’s schedule is truncated (§3.1) [V wave 36A]"

### `research/mission-2026-11-14/b41n18-01-corporate-daf-segment.md`

- **Find:** "net-asset notes"
- **Replace with:** "programme descriptions in Note 1 (Programs), not in a net-asset note [V wave 36A]"

- **Find:** "Corporate or employee-matching flows therefore leave Tides through Benevity's AOGF."
- **Replace with:** "This is one $1.7m Tides grant to AOGF’s employee-giving program (purpose “Equity, human rights, and economic empowerment”). It does not show which Tides fund made the grant, or that the money is corporate, so it is a signal only [V wave 36A]"

- **Find:** "That is an upper bound: wave 26 found the column is not wholly corporate."
- **Replace with:** "That is an upper bound only for this three-sponsor pool, not for the market. It mixes CY2025 with FYE 2026-03 and puts AOGF’s non-DAF other-funds column ($935.7m) in the denominator. Its level is set mainly by AOGF’s weight in the pool ($1.39bn of $22.8bn). AOGF’s Schedule D Part XIII says corporate donors give into its DAFs with ongoing advice, while individual micro-donations carry none. So the column is probably mostly corporate [I], and 9.1% is likely close to the pool’s true value rather than a loose bound [V wave 36A]"

- **Find:** "- Result: **$278m–$691m of corporate DAF grants [I]**."
- **Replace with:** "- Result: **$278m–$691m of corporate DAF grants [I]**. Two further caveats apply. If a sponsor reports corporate funds outside its Schedule D DAF column (unknown even at SVCF, §3.2), the corporate amount adds to the base rather than sitting inside it. CAF America’s FYE 2024-04 Schedule D ($821.2m grants; $441.3m end-of-year value) does not match CAF America’s own column in its consolidating schedule ($730.5m grants to third parties; $200.5m designated DAFs). The end-of-year value is near the consolidated $430.8m, so the base may include CADF and CAF Canada [V wave 36A]"

- **Find:** "4 community-foundation sites could not be read (§6)"
- **Replace with:** "5 community foundations’ statements could not be read: Chicago and California CF (robots.txt 403), Oregon CF (/assets disallowed), Columbus (none located) and GKCCF (no statements link) (§6) [V wave 36A]"

- **Find:** "That is **≥6.6% of its 3,052 DAFs by count**, which is far above Fidelity's 0.25%."
- **Replace with:** "That is **≥6.6% of its 3,052 DAFs by count**, which is far above Fidelity's 0.25%. The page is undated marketing copy and counts companies, not funds, so the 200-fund floor is an inference, not a filed number [V wave 36A]"

- **Find:** "for all 46 overlapping returns (0 mismatches) [C]."
- **Replace with:** "for the 46 overlapping returns that have harvest values (0 mismatches). A 47th overlapping return, Boston Foundation 202641269349301584, has blank harvest values (http_404) [C] [V wave 36A]"

### `research/mission-2026-11-14/direction-corporate-dafs.md`

- **Find:** "That is 6.9% and 5.8% of SVCF's combined advised plus corporate-advised grants [C]."
- **Replace with:** "That is 6.9% and 5.8% of SVCF's combined advised plus corporate-advised grants [C]. SVCF’s audited series goes back to 2021: about $100m, $175m, $134m, $189m and $153m (2.8%–6.9% a year). Fidelity and SVCF together put corporate DAFs at 3.9% of grants in 2024 and 3.4% in 2025. Of 14 further sponsors checked (Tides, CAF America, RPA, NPT and the 10 largest community foundations), SVCF is the only one that publishes a split, and Form 990 has no corporate column ([b41n18-01](b41n18-01-corporate-daf-segment.md)) [V wave 36A]"

- **Find:** "   - Against the repo's corrected FY2024 market of $66.4bn of DAF grants (batch 35), corporate is a low single-digit share."
- **Replace with:** "   - Against the repo's corrected FY2024 market of $66.4bn of DAF grants (batch 35), corporate is a low single-digit share. Where it is published, it is 3.4%–3.9% of grants (Fidelity and SVCF). It reaches 9.1% if AOGF’s DAF column is counted as wholly corporate, but that is a ceiling for that pool only [V wave 36A]"

- **Find:** "- Only SEC filers are covered. Private companies, which are the main users of SVCF and Tides corporate funds, do not appear unless a sponsor names them."
- **Replace with:** "- Only SEC filers are covered. Private companies, which are the main users of SVCF and Tides corporate funds, do not appear unless a sponsor names them. Sponsor pages name four such programs that are not in CD01–CD49: DoorDash and the eBay Foundation (SVCF), and the Bain Capital Relief Fund and Income Research + Management (Boston Foundation) [V wave 36A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.39 Community-foundation locality and corporate DAFs (validated, wave 36A)\n\n**Community-foundation locality and corporate DAFs** (validated, wave 36A). Across 95 of the 100 largest community foundations with itemised FY2023–24 Schedule I XML, the median CF sends 83.0% of US grant dollars to its own state, 69.1% to its home metro and 54.4% to its home county. Omaha CF is left out: its XML Schedule I is truncated. CFs with a higher Schedule D DAF share of grants keep less in-state: Pearson r = −0.47, and −0.26 in-state share per unit of DAF share after size controls (HC1 95% CI −0.40 to −0.11). This is a cross-sectional association, consistent with composition (non-DAF grants almost all in-state, DAF grants about two-thirds) or with national donor bases. Low shares at Cincinnati, Delaware and New Jersey mostly reflect grants to national headquarters. No Form 990 splits corporate from individual DAFs. Of 14 large sponsors checked, only SVCF publishes corporate-advised grants ($100m–$189m a year, 2021–2025). Fidelity and SVCF together put corporate DAFs at 3.9% of grants in 2024 and 3.4% in 2025. The 9.1% figure that counts AOGF’s DAF column as wholly corporate is a ceiling for that pool only, not for the market (repo [`validation-wave36a-report.md`](mission-2026-11-14/validation-wave36a-report.md)) [V wave 36A]\n\n---\n\n## Source register"

**Check.** `$SCRATCH/v36a/scripts/check_finds.py` parses every Find in this section, decodes `\n` and counts occurrences in the target file. All 21 Finds occur exactly once, and no value contains a straight double quote.
