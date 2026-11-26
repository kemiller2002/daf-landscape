# Validation wave 38A: Canadian netting and disbursement quota; DAF money abroad outside NTEE Q

**Validator:** independent-validation-agent-wave38a · **Date:** 2026-11-19 · **Register:** [`data/mission-2026-11-14/validation-register-wave38a.csv`](../../data/mission-2026-11-14/validation-register-wave38a.csv) (35 claims)

**Studies checked**
- Study 1 (V38A-01 to -17): [`b39n3-0406-canada-netting-dq.md`](b39n3-0406-canada-netting-dq.md), `canada-daf-netting-dq-2026-11-19.csv`, `scripts/mission_canada_netting_dq.py`.
- Study 2 (V38A-18 to -35): [`b4531-01-03-non-q-foreign-spending.md`](b4531-01-03-non-q-foreign-spending.md), `non-q-foreign-spending-2026-11-19.csv`, `scripts/mission_non_q_foreign.py`.

**Rules followed.** No outreach, no logins. Not used: crt.sh, certspotter, sec.gov. User agent `research-script/1.0` throughout, never changed. robots.txt checked before fetching: laws-lois.justice.gc.ca returned 404 (no rules), so two pages were fetched (ITA s.149.1; Regulations s.3701). gt990datalake-rawdata.s3.amazonaws.com also returned 404, so nine Form 990 XMLs were fetched, 2 s apart. Scratch: `scratchpad/v38a/`. Nothing was committed.

## Counts

| Result | Study 1 | Study 2 | Total |
|---|---|---|---|
| confirmed | 14 | 12 | 26 |
| partially_confirmed | 3 | 4 | 7 |
| contradicted | 0 | 2 | 2 |
| unverifiable | 0 | 0 | 0 |
| **Total** | 17 | 18 | 35 |

## Findings

### Study 1: Canadian netting and the disbursement quota

1. **Reproducible.** Rerunning with the q0903 and q0346 inputs gives a byte-identical CSV (md5 `e103aaad…`, 1,710 rows).
2. **Netted payouts match.** I recomputed them from the CSV columns:
   - 2025 release: 13.30% gross, 12.76% (tier A), 12.05% (B), 8.82% (C), on C$15.39bn;
   - 2024 release: 16.41%, 15.71%, 14.28%, 10.74%.
   - Tier B equals 9.4% of 2025 line-5864 dollars and tier A 4.1%. Both shares are capped at line 5864; uncapped, tier B is 10.0%.
   - The matched n of 586 includes one sponsor with negative prior-year DAF assets (−C$487). This changes nothing to 4 dp.
3. **The quota rules match the primary law** (Act and Regulations current to 2026-10-29):
   - **Rates:** 3.5% up to C$1m, and C$35,000 plus 5% of the excess above C$1m.
   - **De minimis:** C$100k for charitable organizations, C$25k for other charities.
   - **Pro-rating:** A ÷ 365.
   - **Prescribed amount (Reg. 3701):** the average over 2 to 8 equal, consecutive periods totalling 24 months.
   - **Carry-over (s.149.1(20)):** an excess counts for the immediately preceding year and up to five later years.
   - **Gap:** the study cites only s.149.1(1.1)(d). Paragraphs (a), designated gifts, and (c), Part V transfers, are also excluded (partial).
4. **Top-20 routes are confirmed against raw Schedule 8 rows.**
   - Victoria's recomputed DQ (C$21,042,468) equals its own 2024 line-890 estimate.
   - **Hamilton:** line 865 is −C$279,041 (FPE 2025-03-31). The prior year (FPE 2024-03-31) shows an excess of C$973,348. The carry-forward is valid.
5. **Brookfield's “gross-only” label is not about DAF-to-DAF money (partial).** Its tier-B gifts total C$3.33m:
   - UHN Foundation, C$2.315m;
   - United Way of Greater Toronto, C$0.469m;
   - SickKids Foundation, C$0.30m;
   - C.D. Howe Institute, C$0.25m.
   - True DAF-sponsor gifts (tier A) are only C$0.172m. Net of tier A, Brookfield covers the quota (C$23.40m against C$21.37m).
   - It also carries a 2024 excess of C$54.26m.
6. **Tier C is an upper bound only for itemised sponsors (partial).**
   - 109 matched sponsors report C$113.5m of 5864 with no T1236 rows. Counting all of it as transfers gives 8.08%, not 8.82%.
   - Some tier-C edges look like DAF moves: JCF Montreal → Dean & Bédard family foundation, C$27.9m; CGF Canada → Badge of Hope, C$20.0m.
7. **Donee BN matching is sound.**
   - The unresolved 4.4% is mostly foreign universities, municipalities and First Nations.
   - Unresolved names that resemble a sponsor (C$10.8m) include no actual sponsor. Missed transfers are immaterial.
8. **Wording issues.**
   - Headline 7 places the 22 no-DQ and 6 incomplete rows after the 489 sponsors with no Schedule 8. They are among the 375 sponsors that have one.
   - Headline 8's “18 of 20” means 18 top-20 sponsors meet the proxy floor, not that 18 fall below it.
9. **US comparison holds.** 22.8% is the FY2024 market payout net of DAF-to-DAF (R5 central). Against the US FY2024 itemised tier B (20.8%, excluding processors), Canada's tier B (12.0%) is still 8.8 points lower.

### Study 2: DAF money abroad outside NTEE Q

1. **Reproducible offline.** The CSV is byte-identical (md5 `f185452f…`, 1,028 rows).
   - I summed the 458 non-Q rows independently: $1,346.8m (FY2023 $478.7m, FY2024 $868.1m).
   - Re-deriving them from the cached extracts gives the same total.
   - Combined share: (1,890.8 + 1,867.7 + 1,346.8) ÷ 98,265.4 = **5.195%**. On the itemising base it is 6.44%.
2. **XML re-reads** of Part IX line 3, line 25 and Schedule F Part I confirm the study's inputs for six recipients:
   - **The Clear Fund:** TY2024 line 3 $113,705,380 of $183,707,000; TY2023 $23,677,371 of $115,576,357.
   - **ClimateWorks:** TY2024 Part I $152,001,011 against line 3 $133,475,087 and line 25 $317,281,654.
   - **GiveDirectly:** Part I $95.55m, of which $2.89m is FUNDRAISING rows.
   - **Samaritan's Purse:** line 3 $383.6m; Part I $584.0m of $1,093.2m.
   - **Kyiv School of Economics:** Part I $26.93m of $33.81m.
   - **Wesleyan:** TY2023 Central America “Program services” $444,004,429 against total expenses of $352,224,000. Its Europe and Sub-Saharan Africa rows in the same block look like investments too.
3. **Two large recipients are contradicted on activity type.**
   - **US Olympic and Paralympic Foundation (TY2024).** Every Part I row is labelled “FUNDRAISING” (Europe $50.05m), and line 3 is blank. Its $24.1m is therefore fundraising spending abroad, not money reaching foreign programmes.
   - **Grantham Environmental Trust (TY2024).** Line 3 is blank. Its counted Part I rows are program-related investments of $32.98m, set against $42.1m of expenses. The whole $57.5m rests on investments.
   - **Effect:** excluding fundraising and PRI rows across all non-Q recipients gives **$1,253.4m and 5.10%**, not 5.20%.
4. **The frame exclusion is exact.** None of the 150 base EINs appears among the 500 new recipients.
5. **DAF-sponsor tests are partial.** The 42 + 11 counts are confirmed. Federation-type recipients answering No to the DAF question remain in non-Q (JFNA, Jewish Federation Council of Greater LA, JUF Chicago), as do the Chicago Community Foundation (no 990) and Tides Center. The money abroad involved is small.
6. **Extrapolation arithmetic is exact, but the tail share is driven by outliers.**
   - The 4.30% comes from non-Q ranks 387–500, where the median recipient share is 0%.
   - Five recipients supply $44.3m of the $77.6m. The largest is Friends of the World Food Program, which the friends-of pattern does not catch.
   - The doc's 0–4.3% range is right; 8.41% should not be quoted alone.
7. **Labelling is consistent in the tables** (F / I-alloc / I-extrap). However, “measured” in the prose means filed foreign shares × proportional allocation, so it should always carry [I-alloc].
8. **Repo propagation.**
   - Report §11.42 (3.82%; 4.74% itemising) is correct for its scope and is not changed.
   - The new figure goes into §11.45 below, strategic-synthesis §0 and the comparison table, and FINAL-STATUS.

## Exact corrections

### `research/mission-2026-11-14/b39n3-0406-canada-netting-dq.md`

- **Find:** "One (Brookfield Partners Foundation) meets it from DAF disbursements only gross of transfers (C$23.6m gross, C$20.1m net, DQ C$21.4m)."
- **Replace with:** "One (Brookfield Partners Foundation) meets it from DAF disbursements only gross of transfers (C$23.6m gross, C$20.1m net, DQ C$21.4m). Its tier-B transfers are gifts to UHN Foundation (C$2.3m), United Way of Greater Toronto, SickKids Foundation and the C.D. Howe Institute; its gifts to DAF-primary sponsors are only C$0.17m, so net of tier A it covers the DQ, and its 2024-release excess of C$54.3m is also available under s.149.1(20) [V wave 38A]"

- **Find:** "Tier C is therefore an upper bound, like US tier C [C/I]."
- **Replace with:** "Tier C is therefore an upper bound on netting for itemised sponsors, like US tier C [C/I]. It is not a strict bound overall: 109 matched 2025 sponsors (C$113.5m of line 5864, including Canada Gives) have no T1236 rows, and counting all of that as transfers would give 8.1% instead of 8.8%. A few tier-C edges are DAF-like (JCF Montreal → a private family foundation, C$27.9m) [V wave 38A]"

- **Find:** "The other 489 sponsors (C$2.79bn) have no Schedule 8 row; 22 have no DQ and 6 have blank spending lines."
- **Replace with:** "The other 489 sponsors (C$2.79bn) have no Schedule 8 row. Of the 375 with a row, 22 have no DQ and 6 have blank spending lines [V wave 38A]"

- **Find:** "Among the top-20 the count is 18 of 20 (net) [C]."
- **Replace with:** "Among the top-20, 18 of 20 meet such a floor net of tier-B transfers and 19 gross [C] [V wave 38A]"

- **Find:** "**s.149.1(1.1)(d)** excludes administration and management from qualifying spending [F]."
- **Replace with:** "**s.149.1(1.1)** deems designated gifts (a), transfers that reduced a Part V liability (c) and administration and management expenditures (d) not to be qualifying spending [F] [V wave 38A]"

### `research/mission-2026-11-14/b39n3-canada-australia.md`

- **Find:** "The Canadian figure is gross of them, so the gap is if anything understated [I]."
- **Replace with:** "The Canadian figure is gross of them. Netted against the CRA qualified-donee lists, 2025 payout is 12.8% (tier A, DAF-primary sponsors), 12.0% (tier B, any line-5860 = Y sponsor) or 8.8% (tier C, plus all foundations; an upper bound for itemised sponsors), so the gap widens only modestly under a DAF-to-DAF definition ([b39n3-0406-canada-netting-dq.md](b39n3-0406-canada-netting-dq.md)) [C/I] [V wave 38A]"

- **Find:** "Canada's ~13% against the US 22.8% is a conservative comparison: Canadian DAF payout is lower."
- **Replace with:** "Canada's ~13% against the US 22.8% is a conservative comparison: Canadian DAF payout is lower. Netted of gifts to other line-5860 = Y sponsors, it is 12.0% in 2025, against the US FY2024 itemised tier B of 20.8% excluding processors [C] [V wave 38A]"

- **Find:** "and a sponsor can meet it while individual accounts pay nothing [I; P-B39N3-06]."
- **Replace with:** "and a sponsor can meet it while individual accounts pay nothing [I; P-B39N3-06]. Tested in b39n3-0406: in the 2025 release 13 of the top-20 sponsors meet the DQ from DAF disbursements net of sponsor transfers, four community foundations need non-DAF spending, and Hamilton Community Foundation's C$279k shortfall is covered by its C$973k prior-year excess (ITA s.149.1(20): one year back, up to five forward) [V wave 38A]"

### `research/mission-2026-11-14/direction-international-comparison.md`

- **Find:** "(11.2% in 2025; 13.3% on prior-year assets)"
- **Replace with:** "(11.2% in 2025; 13.3% on prior-year assets); 12.0% on prior-year assets net of gifts to other DAF sponsors [C: b39n3-0406] [V wave 38A]"

- **Find:** "Canadian figures also include DAF-to-DAF transfers, which the authors flag [F: S13]."
- **Replace with:** "Canadian figures also include DAF-to-DAF transfers, which the authors flag [F: S13]. Netting gifts to other line-5860 = Y sponsors lowers Canada's 2025 prior-year-asset payout from 13.3% to 12.0% [C: b39n3-0406] [V wave 38A]"

- **Find:** "with 6% and smoothing decided but not yet in any registered instrument at 2026-11-19 [V wave 37B]"
- **Replace with:** "with 6% and smoothing decided but not yet in any registered instrument at 2026-11-19 [V wave 37B]. Canada's quota (3.5% to C$1m, 5% above, on a 24-month average) is charity-level and rarely binds on DAF sponsors: in the 2025 release 13 of the top-20 meet it from DAF disbursements net of sponsor transfers [V wave 38A]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "or 5.93% extrapolated [I] ([b45n31-01-daf-money-abroad.md](b45n31-01-daf-money-abroad.md)) [V wave 37A]"
- **Replace with:** "or 5.93% extrapolated [I] ([b45n31-01-daf-money-abroad.md](b45n31-01-daf-money-abroad.md)) [V wave 37A]. Adding the 458 largest recipients outside NTEE Q and the DAF-sponsor panel ($1.347bn at their own filed foreign shares [I-alloc]) raises it to 6.44% on that base, or 5.20% of top-50 total grants (from 3.82%); 5.10% without program-related-investment and fundraising rows ([b4531-01-03-non-q-foreign-spending.md](b4531-01-03-non-q-foreign-spending.md)) [V wave 38A]"

- **Find:** "Measured money abroad on the same base: 4.74% (5.93% extrapolated [I]; 3.82% of total grants) [V wave 37A]"
- **Replace with:** "Measured money abroad on the same base: 4.74% (5.93% extrapolated [I]; 3.82% of total grants) [V wave 37A]; adding the non-Q top 500, 6.44% (5.20% of total grants; 5.10% without PRI and fundraising rows) [I-alloc] [V wave 38A]"

- **Find:** "set sponsor-level floors [V wave 37B]"
- **Replace with:** "set sponsor-level floors [V wave 37B]; Canada's is a charity-level 3.5%/5% quota that most large DAF sponsors meet from DAF disbursements alone (13 of the top 20 in the 2025 release, net of sponsor transfers) [V wave 38A]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "Including direct foreign grants, measured outflow is 3.82% of total grants. The earlier 7.8% is a share by recipient sector."
- **Replace with:** "Including direct foreign grants, measured outflow is 3.82% of total grants. The earlier 7.8% is a share by recipient sector. Adding the 458 largest recipients outside NTEE Q raises measured outflow to 5.20% of total grants (6.44% of net Schedule I plus line 3; 5.10% without program-related-investment and fundraising rows) [I-alloc] [V wave 38A]"

### `research/mission-2026-11-14/b4531-01-03-non-q-foreign-spending.md`

- **Find:** "+ non-Q 500: **5.20%** ($5.105bn) [I-alloc]. This is the measured headline."
- **Replace with:** "+ non-Q 500: **5.20%** ($5.105bn) [I-alloc]. This is the measured headline (filed foreign shares × proportional allocation; 5.10% without program-related-investment and fundraising rows) [V wave 38A]"

- **Find:** "The US Olympic and Paralympic Foundation went from $0.0m to $24.1m (Europe; FY2024 is the Paris 2024 year [I])."
- **Replace with:** "The US Olympic and Paralympic Foundation went from $0.0m to $24.1m (Europe; FY2024 is the Paris 2024 year [I]). Its TY2024 Schedule F Part I rows (Europe $50.05m) are all labelled “FUNDRAISING” and its line 3 is blank, so this is fundraising spending abroad, not money for foreign programmes [V wave 38A]"

- **Find:** "Non-Q recipients' Part I investment rows total $136.8bn pooled and are excluded; almost all of this is university endowments."
- **Replace with:** "Non-Q recipients' Part I investment rows total $136.8bn pooled and are excluded; almost all of this is university endowments. Program-related investments (counted as programme by the base rule) and fundraising rows stay in. Excluding both lowers non-Q from $1,346.8m to $1,253.4m (5.20% → 5.10%): Grantham Environmental Trust ($57.5m; line 3 blank, every counted Part I row a PRI) and the US Olympic and Paralympic Foundation ($24.1m; Europe row labelled fundraising) fall to zero [V wave 38A]"

- **Find:** "A zero-to-4.3% range on that step (5.20%/6.53% to 8.41%) is the honest statement."
- **Replace with:** "A zero-to-4.3% range on that step (5.20%/6.53% to 8.41%) is the honest statement. The 4.30% is outlier-driven: the median share among those 100 recipients is 0%, and five of them (led by Friends of the World Food Program, $13.2m) supply $44.3m of their $77.6m abroad [V wave 38A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.45 Canadian netting and quota; DAF money abroad outside NTEE Q (validated, wave 38A)\n\n**Canadian netting and quota; DAF money abroad outside NTEE Q** (validated, wave 38A). Both studies reproduce byte for byte. Netting Canadian DAF disbursements against the CRA qualified-donee lists lowers 2025 payout on prior-year DAF assets from 13.3% to 12.8% (gifts to DAF-primary sponsors), 12.0% (any DAF sponsor) and 8.8% (all foundations; an upper bound for itemised sponsors, 8.1% if every unitemised sponsor's disbursements were transfers). The quota rules match the Act and Regulations: 3.5% up to C$1m and 5% above, on a 24-month average, with one year back and five forward. In 2025, 13 of the top-20 sponsors meet the quota from net DAF disbursements, four community foundations need endowment spending, and Hamilton covers a C$279k shortfall with its C$973k prior excess. Brookfield's “gross-only” label rests on gifts to hospital, United Way and think-tank charities, not DAF moves. Abroad, the 458 largest recipients outside NTEE Q add $1.347bn [I-alloc], raising measured DAF money abroad from 3.82% to 5.20% of top-50 grants (6.44% of net Schedule I plus line 3). Excluding program-related-investment and fundraising rows, chiefly Grantham Environmental Trust and the US Olympic and Paralympic Foundation, gives 5.10%. [V wave 38A]\n\n---\n\n## Source register"

## Key sources

| Source | URL | Read |
|---|---|---|
| Income Tax Act s.149.1 (current to 2026-10-29) | https://laws-lois.justice.gc.ca/eng/acts/I-3.3/section-149.1.html | 2026-11-19 |
| Income Tax Regulations s.3701 (current to 2026-10-29) | https://laws-lois.justice.gc.ca/eng/regulations/C.R.C.,_c._945/section-3701.html | 2026-11-19 |
| CRA open data 2025 / 2024: qualified donees and Schedule 8 (cached q0346) | https://open.canada.ca/data/en/dataset/4b60228a-2b78-45d3-8e05-f7150b8fe8d8 ; https://open.canada.ca/data/en/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8 | 2026-11-19 (cache) |
| Form 990 XML: Clear Fund TY2024/TY2023, ClimateWorks, GiveDirectly, Samaritan's Purse, Wesleyan TY2023, Grantham, USOPF, Kyiv School of Economics | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{202523189349307757, 202413209349305336, 202512959349301466, 202523109349303682, 202522489349300607, 202411369349310371, 202543219349322204, 202541749349301309, 202533189349300118}_public.xml | 2026-11-19 |
