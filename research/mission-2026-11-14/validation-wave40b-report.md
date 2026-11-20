# Validation wave 40B: non-top-50 numerator and Canada follow-ups

**Validator:** independent-validation-agent-wave40b · **Date:** 2026-11-19 (fetches completed 2026-11-20 UTC) · **Register:** [`validation-register-wave40b.csv`](../../data/mission-2026-11-14/validation-register-wave40b.csv)

**Studies checked**
- Study 1: [`b40n1202-01-non-top50-numerator.md`](b40n1202-01-non-top50-numerator.md), [`non-top50-numerator-2026-11-19.csv`](../../data/mission-2026-11-14/non-top50-numerator-2026-11-19.csv), [`mission_non_top50_numerator.py`](../../scripts/mission_non_top50_numerator.py)
- Study 2: [`b3946-canada-followups.md`](b3946-canada-followups.md), [`canada-followups-2026-11-19.csv`](../../data/mission-2026-11-14/canada-followups-2026-11-19.csv), [`mission_canada_followups.py`](../../scripts/mission_canada_followups.py)

No commits or pushes. No outreach. crt.sh, certspotter and sec.gov were not used. User agent `research-script/1.0`, the same as the studies. Scratch outputs are in the session scratchpad `v40b/`.

## Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| 1. Non-top-50 numerator | 16 | 8 | 8 | 0 | 0 |
| 2. Canada follow-ups | 16 | 10 | 6 | 0 | 0 |
| **Total** | **32** | **18** | **14** | **0** | **0** |

All 26 Find strings below were checked by script: each occurs exactly once in its target file as of this validation.

## Study 1: non-top-50 numerator (V40B-01 to V40B-16)

### Reproduction
- **Byte-identical rerun.** The cache-only rerun to scratch reproduces the CSV byte for byte (md5 `435ac483db15a4a45bd47b2d8e812ddf`). It took about 2.2 minutes. All diagnostics reproduce:
  - 3,097 sponsor-years; 2,611 other sponsor-years with status ok;
  - 604,913 and 487,896 lines;
  - frames of 138,832 and 70,008 EINs;
  - 6,512 of 6,518 returns ok;
  - the q1202 check: 4,124 returns, 0 mismatches.
- **Coverage.** 67.3%, 17.6% and 84.9% recompute from the coverage rows: $39.29bn, $10.31bn and $49.60bn of $58.41bn.
- **Uplift.** 0.2144 against an implied 0.4865.
- **Headline shares.** All recompute: expanded frame 7.3% (6.5–8.2) and 12.1% (10.9–13.4); committed frame 8.4% (7.6–9.2) and 12.6% (11.3–14.0).

### XML spot-checks
- **Sponsors.** Four randomly drawn non-top-50 sponsor returns were re-fetched from the GivingTuesday mirror (robots.txt 404 again on 2026-11-20). Their cached line counts and cash totals match the XML exactly:
  - Chaffee County CF: 17 lines;
  - Uncommon Charitable Impact: 66;
  - Knights of Columbus Charitable Fund: 254;
  - CF for Southeast Michigan: 964.
- **Recipients.** For six recipients (12 returns), the two-year sums of Part VIII 1h and of 1h − 1d − 1e match the CSV denominators to the dollar.

### Supplementary sample
- **Seeding.** The sample is seeded (`random.Random(20261120)`) and drawn with the committed `draw_sample`.
- **Weighting.** Its 52 `new|` strata sum to N = 70,008, and weights are N_h / (n_h − xml_not_read).
- **Adding it to the frame.** This is statistically valid, because the frames and strata are disjoint. But it changes the target population, so the 8.4% → 7.3% step is not a correction of the old inference.

### Main finding: “the scaling overstated” needs qualifying
The study reports a fall of −2.9 points (10.3% → 7.3%, 1h) and labels it [F]. That fall has three parts:

| Step | 1h | 1h − 1d − 1e | What it is |
|---|---|---|---|
| Committed scaled inference (top 50 ÷ 0.673) | 10.3% | 15.4% | Starting point |
| All sponsors, committed frame, ÷ 0.849 | 9.9% (−0.4) | 14.8% (−0.6) | **Like-for-like measured overstatement** |
| All sponsors, committed frame, unscaled | 8.4% (−1.5) | 12.6% (−2.2) | Leaves the 15.1% unitemised gap unassigned: an assumption, so the figure is a floor |
| All sponsors, expanded frame | 7.3% (−1.0) | 12.1% (−0.5) | Adds 70,008 recipients with no top-50 grant: a population change |

- **What is measured.** Only the first step is a measured overstatement. The rest depends on where the $8.8bn gap goes: foreign grants, sub-$5,000 grants, non-itemising sponsors, and the corrected-versus-raw difference. Sub-$5,000 grants largely reach domestic recipients.
- **The 48.6% comparator is not like for like.** 22.4 points of it is the unitemised gap. The right comparator for the measured 21.4% is 26.2% (0.176 ÷ 0.673).
- **The 32.7 points.** They are not what the scaling attributed to the non-top-50 sponsors. They are everything outside top-50 itemised lines.
- **The interval comparison.** The inference interval does overlap the direct committed-frame interval on both bases. All estimates come from the same sample, so non-overlap is not a test.
- **What to report.** The scaled “≈10%” on 1h was close to the like-for-like 9.9%. The defensible replacement is a range: 8.4% (floor, same recipients) to 9.9% (gap assigned pro rata) on 1h, and 12.6–14.8% on 1h − 1d − 1e. The 7.3% / 12.1% figures belong to a wider population.

### Other findings
- **The gap wording.** “The rest of the 15.1-point gap ($8.8bn)” is wrong: $8.8bn is the whole gap, and the $2.07bn of non-itemising sponsors is part of it.
- **Hexagon Foundation.** Its “1h of $600m” is a two-year sum. The $50.7m it received as filed from Christian Community Foundation equals its line 1d (related organisation) to the dollar over the two years. On 1h − 1d − 1e, DAF grants from related sponsors stay in the numerator but leave the denominator: a small upward bias the study does not mention.
- **Minor.** NTEE group respondents run 207–413 on 1h − 1d − 1e, not 209–413. At ≥$100m, the expanded all-sponsor share (3.7%) equals the top-50-only committed share.
- **Repo passages with scaled figures:**
  - b40n12 §0 (≈10.2%);
  - b40n1202-b43n26 §0 (15.4% scaled);
  - report §11.32 (“about 10% of 1h, or 15% of private contributions”);
  - FINAL-STATUS (10.3%, top-50 only, unlabelled);
  - strategic-synthesis §0 carries only the unscaled 6.9% and needs an addition, not a correction.
  - The report group may hold only the §11.52 item, so §11.52 states that it replaces §11.32's scaled figure.

## Study 2: Canada follow-ups (V40B-17 to V40B-32)

### Reproduction
- **Byte-identical rerun.** The rerun reproduces the CSV byte for byte (md5 `b5389aa4fd24e84729d09967b5bdb2d3`, 18 s).
- **`--check-parent`.** It reports 1,710 = 1,710 rows, identical.
- **Recomputed figures.** All of these reproduce from the summary JSON:
  - C$445.5m by type, and the rule split;
  - the 0210 share (74.4%);
  - middle-tier payouts (B 12.05%, BP 12.04%, BP+CF+F 11.54%, C 8.82%; medians 4.89 / 4.84 / 4.18);
  - the 0.48 / 2.10 / 0.62-point decomposition;
  - Schedule 8 gap counts by line 5850 (2025 N 196/197, blank 14/14, Y 16/6,382; 2024 N 235/236, blank 17/17, Y 2/6,017);
  - the quarter table;
  - the CanadaHelps scenarios.

### Donee audit (20 donees: the 8 largest plus 12 random, seed 40)
- **Plausible: 16.**
- **Clear mistypes: 2.**
  - Senators Community Foundation, an NHL club's charity typed as a community foundation. At C$0.5m it is the largest donee of that type.
  - Glaucoma Research Society of Canada, typed other although it is a health-research charity.
- **Debatable residuals: 2.** Israel Magen Fund of Canada and a Knights of Columbus charitable trust.
- **Platform rule.** It misses CharityEx Foundation (C$2.1m; own line 5050 102% of revenue), a pass-through intermediary. The effect on tier BP is at most about 0.01 point.
- **Effect on results.** None of these changes the payout conclusions.

### Schedule 8 and JCF Montreal
- **Line 5850 and line 5900.** The dictionary text confirms both measure the same 24-month average. Large returns answering N are therefore internally inconsistent.
- **“Almost all answered N” overstates.** In 2025, 196 of 226 large returns without Schedule 8 (86.7%) answered N, 14 left it blank and 16 answered Y. The converse holds: almost every large N return lacks Schedule 8.
- **Lag and paper.** The tests are suggestive, not decisive. Release and quarter comparisons are confounded by designation and FPE mix. The rise in 5850 = Y returns without Schedule 8 (72 → 435) in the newer release is what a lag would predict.
- **JCF Montreal.** Raw Section C confirms 5850 = N in both releases and the 5862, 5864 and 5900 values. The DQ formula gives C$92,511,845 and C$107,136,990, both covered by DAF disbursements. That makes 14 of the 2025 top-20 DAF_NET_COVERS, against 13 in the parent.
- **“Small DAF holders (C$0.2m or less)” is wrong for 2024.**
  - Parish of St David holds C$0.23m.
  - Two others answered 5860 = Y with line 5862 blank: Children's Family House Society of B.C. (line 5900 C$24.0m) and Ottawa Mission Foundation (C$15.9m).

### CanadaHelps (re-fetched 2026-11-20; robots.txt allows; about 6 s between requests)
- **Pages re-read.** Six pages and both audited statements were fetched again. The PDFs are byte-identical to the study's copies.
- **Quotations.** The product quotations match, including the refund policy's date (Last updated August 26, 2026). The Terms of Use are dated September 2, 2025.
- **Audited figures.** The C$11,019,785 of designated cash and the C$467,074,451 of donations to charities match the statements.
- **Gift cards.** The statements place only cards unredeemed after 18 months (as undisbursable funds) explicitly in contributions due to designated charities. The claim that all gift-card balances sit inside designated cash is therefore an inference, not [F].
- **Note citation.** The designated-cash note is note 7 of the FY2025 statements and note 6 of the FY2024 ones.
- **Is “CanadaHelps is not a DAF” fairly stated?** Yes, as an inference about products, with the stated limits: C18 is quoted second-hand and the help articles were not read. Two more points support it:
  - designated cash is 2.4% of the year's payments;
  - St Mary's General Hospital Foundation, the source of C$10.16m of sponsor gifts to CanadaHelps, reports one DAF account worth C$0.84m, so that gift cannot be DAF money.
- **The earlier docs.** The parent doc still cites CanadaHelps as a DAF-like product (§2.3 reading, §4 limits). It should be corrected.

## Exact corrections

### `research/mission-2026-11-14/b40n1202-01-non-top50-numerator.md`
- **Find:** "**The scaled estimate was too high [F].** On the line 1h basis, the committed 1/0.673 inference gives a pooled share of **10.3%** (implied interval 9.0–11.6%). The directly measured all-sponsor share is lower on either frame:"
- **Replace with:** "**The scaled estimate leaned high, but most of the fall below is not a measured overstatement [F/I].** On the line 1h basis, the committed 1/0.673 inference gives a pooled share of **10.3%** (implied interval 9.0–11.6%). Like for like (committed frame, both sides divided by their coverage) the measured figure is 9.9%, a fall of 0.4 point (14.8% against 15.4% on 1h − 1d − 1e, 0.6 point). Leaving the 15.1% unitemised gap unassigned takes 1h to 8.4% (−1.5 points), so the direct figures are floors. Adding the new-only recipients changes the population and takes it to 7.3% (−1.0 point). The direct shares on each frame: [V wave 40B]"
- **Find:** "The non-top-50 sponsors add 17.6 points, not the 32.7 points the scaling assumed."
- **Replace with:** "The non-top-50 sponsors add 17.6 points. The 32.7 points the scaling filled cover everything outside top-50 itemised lines, including the 15.1-point gap that no itemised line reaches, so they are not a like-for-like target for these sponsors [V wave 40B]"
- **Find:** "The 1/0.673 scaling assumed **48.6%**."
- **Replace with:** "The 1/0.673 scaling assumed **48.6%**. Of that, 26.2 points (0.176 ÷ 0.673) is the non-top-50 sponsors’ own measured coverage and 22.4 points is the unitemised gap. Like for like, the measured 21.4% is 0.82 of the 26.2% that proportional allocation would give [V wave 40B]"
- **Find:** "The rest of the 15.1-point gap ($8.8bn) is foreign grants, sub-$5,000 grants not itemised, timing, and the difference between DAF weighting and netting."
- **Replace with:** "The whole 15.1-point gap is $8.8bn ($58.41bn × 0.151, netted and DAF-weighted); the non-itemising sponsors’ $2.07bn (raw) is part of it, not additional. The remainder is foreign grants, sub-$5,000 grants not itemised, timing, the $1.84bn by which corrected DAFRC grants ($66.44bn) exceed the raw total ($64.60bn) used for that split, and the difference between DAF weighting and netting. [V wave 40B]"
- **Find:** "Hexagon Foundation has a 1h of $600m and received $29.0m."
- **Replace with:** "Hexagon Foundation has a 1h of $600m over its two matched years ($95.9m and $503.8m) and received $29.0m DAF-weighted ($50.7m as filed) from Christian Community Foundation. Hexagon reports that money on line 1d as related-organisation support (1d: $7.50m and $43.23m, the same $50.73m in total), so on 1h − 1d − 1e its numerator keeps a gift its denominator removes [V wave 40B]"
- **Find:** "- The larger effect is size. Measured, the others are 17.6% of netted grants, not the 32.7% the scaling attributes to them."
- **Replace with:** "- The larger effects are the unassigned gap and the frame, not where non-top-50 dollars land. On the committed frame with both sides divided by coverage, the move is 10.3% → 9.9% (1h) and 15.4% → 14.8% (1h − 1d − 1e). The rest of the move to the direct expanded figures comes from leaving the 15.1% gap unassigned (−1.5 and −2.2 points) and from adding new-only recipients (−1.0 and −0.5 point) [V wave 40B]"
- **Find:** "For both main bases it does not overlap the direct expanded-frame interval."
- **Replace with:** "For both main bases it does not overlap the direct expanded-frame interval. It does overlap the direct committed-frame interval (1h: 7.6–9.2% against 9.0–11.6%; 1h − 1d − 1e: 11.3–14.0% against 13.6–17.6%), and all figures rest on the same sample, so non-overlap is not a significance test [V wave 40B]"

### `research/mission-2026-11-14/b40n12-daf-share-of-recipient-revenue.md`
- **Find:** "Dividing by that coverage gives a pooled share of **≈10.2%**."
- **Replace with:** "Dividing by that coverage gives a pooled share of **≈10.2%**. Measured directly with every itemising panel sponsor instead, the pooled share is 8.4% (7.6–9.2%) on the same recipients and 7.3% (6.5–8.2%) with recipients that get only non-top-50 grants; both leave the 15.1% of netted grants that no itemised line reaches unassigned, so they are floors, and dividing the first by all-sponsor coverage (0.849) gives 9.9% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B]"

### `research/mission-2026-11-14/b40n1202-b43n26-recipient-basis-and-rating-eligibility.md`
- **Find:** "  - All recipients: 10.3% unscaled [F], 15.4% scaled [I]."
- **Replace with:** "  - All recipients: 10.3% unscaled [F], 15.4% scaled [I]. Measured with every itemising panel sponsor instead of scaled: 12.6% (11.3–14.0%) on the same recipients and 12.1% (10.9–13.4%) with recipients that get only non-top-50 grants; ≥$100m 7.0% and 6.8%; $25–100m 12.7% and 12.3%. These are floors (15.1% of netted grants reach no itemised line); scaled by all-sponsor coverage the same-recipient figure is 14.8% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B]"

### `research/mission-2026-11-14/strategic-synthesis.md`
- **Find:** "falling from 17.8% pooled under $1m of revenue to 3.7% at $100m and over ([b40n12-daf-share-of-recipient-revenue.md](b40n12-daf-share-of-recipient-revenue.md); wave 33A) [V wave 34S]."
- **Replace with:** "falling from 17.8% pooled under $1m of revenue to 3.7% at $100m and over ([b40n12-daf-share-of-recipient-revenue.md](b40n12-daf-share-of-recipient-revenue.md); wave 33A) [V wave 34S]. With every itemising panel sponsor measured, the pooled share is 8.4% on the same recipients (7.3% adding recipients with no top-50 grant), a floor that replaces the scaled ≈10% ([b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md)) [V wave 40B]"

### `research/mission-2026-11-14/FINAL-STATUS.md`
- **Find:** "On the private-giving proxy (1h − 1d − 1e), the median is 7.7% and the pooled share 10.3%."
- **Replace with:** "On the private-giving proxy (1h − 1d − 1e), top-50 DAF grants are a median 7.7% and a pooled 10.3%; with every itemising panel sponsor measured, the pooled share is 12.6% on the same recipients and 12.1% adding recipients with no top-50 grant (floors; the scaled 15.4% is superseded) [V wave 40B]"

### `research/mission-2026-11-14/b3946-canada-followups.md`
- **Find:** "**Large returns without Schedule 8 almost all answered line 5850 = N.**"
- **Replace with:** "**Large returns without Schedule 8 mostly answered line 5850 = N (196 of 226 in 2025, 235 of 254 in 2024; most others left it blank), and almost every large return answering N lacks Schedule 8.** [V wave 40B]"
- **Find:** "at 2025-06-30, against C$467.1m paid to charities in the year [F]."
- **Replace with:** "at 2025-06-30, against C$467.1m paid to charities in the year [F]. The statements place only cards unredeemed after 18 months (undisbursable funds) in that balance explicitly; that younger card balances sit there too is an inference [I] [V wave 40B]"
- **Find:** "Gift-card balances are not shown separately."
- **Replace with:** "Gift-card balances are not shown separately, and note 2 names only cards unredeemed after 18 months as included in contributions due to designated charities, so the inclusion stated next is partly inferred; the designated-cash note is note 7 of the FY2025 statements (note 6 of FY2024) [V wave 40B]"
- **Find:** "The others (four in 2025, four in 2024) are small DAF holders (C$0.2m of DAF assets or less): churches, a museum and small charities. All are NEEDS_NON_DAF [C]."
- **Replace with:** "The others (four in 2025, four in 2024) are all NEEDS_NON_DAF [C]. In 2025 they are small DAF holders (C$0.17m of DAF assets or less): a church, a diocese, a museum and a college alumni charity. In 2024 two are small (Parish of St David C$0.23m, the Anglican diocese of British Columbia C$0.02m) and two answered 5860 = Y with line 5862 blank: The Children’s Family House Society of B.C. (line 5900 C$24.0m) and The Ottawa Mission Foundation (C$15.9m) [V wave 40B]"
- **Find:** "came from a hospital foundation whose line 5864 is blank, so that money is not counted as DAF disbursement [C]."
- **Replace with:** "came from a hospital foundation whose line 5864 is blank, so that money is not counted as DAF disbursement [C]. That foundation reports one DAF account worth C$0.84m (line 5862), so the gift is about 12 times its DAF assets and cannot be DAF money; the T1236 row may also be misreported [I] [V wave 40B]"
- **Find:** "It found only CanadaHelps and PayPal Giving Fund Canada."
- **Replace with:** "It found only CanadaHelps and PayPal Giving Fund Canada. It misses CharityEx Foundation (C$2.1m in 2025, typed other; own line 5050 102% of revenue), which fails the 1,000-row test; adding it would move tier BP by about 0.01 point [V wave 40B]"
- **Find:** "  - Disease and research charities (e.g. cancer foundations) count as hospital/health."
- **Replace with:** "  - Disease and research charities (e.g. cancer foundations) count as hospital/health only when a name or code rule matches: the Glaucoma Research Society of Canada falls to other. The name rule also types the Senators Community Foundation (an NHL club’s charity; C$0.5m, the largest of the type) as a community foundation. A 20-donee audit found these two mistypes and two debatable residuals (Israel Magen Fund of Canada; a Knights of Columbus charitable trust) [V wave 40B]"

### `research/mission-2026-11-14/b39n3-0406-canada-netting-dq.md`
- **Find:** "   - **2025:** 13 meet the DQ from DAF disbursements alone, even net of tier-B transfers."
- **Replace with:** "   - **2025:** 13 meet the DQ from DAF disbursements alone, even net of tier-B transfers. JCF Montreal (rank 2, no Schedule 8, line 5850 = N) would make 14: its line 5900 of C$2,143.0m implies a DQ of C$107.1m against C$236.9m of DAF disbursements ([b3946-canada-followups.md](b3946-canada-followups.md)) [V wave 40B]"
- **Find:** "- **NO_SCHEDULE8 (1):** JCF Montreal."
- **Replace with:** "- **NO_SCHEDULE8 (1):** JCF Montreal. It answered line 5850 = N; its line 5900 (C$1,850.5m) implies a DQ of C$92.5m against C$213.9m of DAF disbursements, so it would be DAF_NET_COVERS ([b3946-canada-followups.md](b3946-canada-followups.md)) [V wave 40B]"
- **Find:** "Examples are CanEd Foundation and CanadaHelps; CanadaHelps answered line 5860 = **N** in both releases [C]. See queue P-B3946-01 and -04."
- **Replace with:** "Examples are CanEd Foundation (whose nature is open) and CanadaHelps; CanadaHelps answered line 5860 = **N** in both releases [C]. The follow-up finds that CanadaHelps’ products do not fit the C18 DAF definition and that 97% of 2025 sponsor gifts to it came from one hospital foundation’s non-DAF money; netting public foundations by type moves tier B by 0.01 point (giving platforms) or 0.5 point (with federations), so tier C’s extra netting is mostly program grants ([b3946-canada-followups.md](b3946-canada-followups.md)) [V wave 40B]"
- **Find:** "Organisations that answer N but run DAF-like products (e.g. CanadaHelps) fall in tier C, or out of netting [C/I]."
- **Replace with:** "Organisations that answer N but run DAF-like products fall in tier C, or out of netting [C/I]. CanadaHelps, cited here earlier as an example, does not offer a DAF-like product on the follow-up’s reading: only charity gift cards hold balances for later direction ([b3946-canada-followups.md](b3946-canada-followups.md)) [V wave 40B]"

### `research/mission-2026-11-14/b39n3-canada-australia.md`
- **Find:** "or 8.8% (tier C, plus all foundations; an upper bound for itemised sponsors)"
- **Replace with:** "or 8.8% (tier C, plus all foundations; an upper bound for itemised sponsors; netting giving platforms, community foundations and federations beyond tier B gives 11.5%, per [b3946-canada-followups.md](b3946-canada-followups.md)) [V wave 40B]"

### `research/mission-2026-11-14/direction-international-comparison.md`
- **Find:** "13 of the top-20 meet it from DAF disbursements net of sponsor transfers [V wave 38A]"
- **Replace with:** "13 of the top-20 meet it from DAF disbursements net of sponsor transfers [V wave 38A], or 14 counting JCF Montreal, which files no Schedule 8 but whose line 5900 implies a DQ of C$107.1m against C$236.9m of DAF disbursements [V wave 40B]"
- **Find:** "lowers Canada's 2025 prior-year-asset payout from 13.3% to 12.0% [C: b39n3-0406] [V wave 38A]"
- **Replace with:** "lowers Canada's 2025 prior-year-asset payout from 13.3% to 12.0% [C: b39n3-0406] [V wave 38A]. CanadaHelps, a C$467m-a-year pass-through that answers 5860 = N, would raise it to 14.9% if counted as a sponsor, so platform-inclusive Canadian figures are not comparable [C: b3946] [V wave 40B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.52 Non-top-50 DAF share and Canadian follow-ups (validated, wave 40B)\n\n**Non-top-50 DAF share and Canadian follow-ups** (validated, wave 40B). An independent cache-only re-run reproduces both CSVs byte for byte, and 16 sampled returns (4 sponsor, 12 recipient) match their XML. Reading every itemising panel sponsor’s Schedule I covers 84.9% of netted FY2024 DAF grants, against 67.3% for the top 50. On the same recipients, all-sponsor DAF grants are a pooled 8.4% of line 1h and 12.6% of 1h − 1d − 1e. Adding 70,008 recipients with only non-top-50 grants gives 7.3% and 12.1%. These replace the scaled “about 10%” of §11.32 and the scaled 15.4%, but only about 0.4–0.6 point of the fall is a like-for-like overstatement. The rest comes from leaving the 15.1% of grants that no itemised line reaches unassigned, so the direct figures are floors, and from the larger recipient population. In Canada, tier-C public-foundation gifts (C$445.5m in 2025) are mostly hospital and federation grants. Netting giving platforms changes payout by 0.01 point; netting federations too gives 11.5%, against 12.0% for tier B. Large returns without Schedule 8 mostly answered line 5850 = N. JCF Montreal’s imputed quota (C$107.1m) is covered by its DAF disbursements (C$236.9m). CanadaHelps’ products do not fit the CRA DAF definition (repo [`validation-wave40b-report.md`](mission-2026-11-14/validation-wave40b-report.md)) [V wave 40B]\n\n---\n\n## Source register"
