# Validation wave 34S: synthesis §0 (governing A–G and top ten, 2026-11-19)

**Task:** P-G1911-01. **Validator:** independent-validation-agent-wave34s. **Date:** 2026-11-19.
**Register:** [`validation-register-wave34s.csv`](../../data/mission-2026-11-14/validation-register-wave34s.csv), 45 claims (V34S-01 to V34S-45).
**Scope:** [`strategic-synthesis.md`](strategic-synthesis.md) from "## 0. Current A–G and top ten (governing, 2026-11-19)" to the "---" before "## A.". That is 89 lines covering A (12 beliefs), B–F and the G top ten plus four notable items.

**Method.**
- I opened every repo file that §0 cites. All 51 relative links resolve. For each figure I took the governing value. That means applied `[V wave N]` replacements, governing appendices and validation-correction sections, the validation reports for waves 32A, 32B, 33A and 33B, and industry report §11.28–§11.33.
- **Recomputed from CSVs** (scratch only):
  - `dafrc-sponsor-schedule-d-fy2019-2024.csv`: 3,590,067 accounts and $327.87bn; CR3 45.52%, CR5 55.83%, HHI 830.3; NPT $42.12bn (12.85%); under-$50m on the raw basis 1,235 sponsors and 2.80%. The 1,240 / 2.84% figure is on corrected assets.
  - `dafrc-market-accounts-restated.csv`: 3,309,483, 2,589,633 and 787,978.
  - `daf-startup-cohort-2021-2026.csv`: 18 in the cohort (10 / 1 / 1 / 6); strict subset 8.
  - `state-daf-law-50-state-check-2026-11-19.csv`: 51 state rows, Connecticut "not checkable", and no in-window row coded as a mandate.
  - `complaint-rates-2026-11-19.csv`: only Fidelity (27) and RCF (1) among the top 15; Fidelity 1.320 per 10k; AOGF 0.777 per 10k and 28.7 per $1bn.
  - `philanthropy-ai-products-2026.csv`: 30 rows and 0 RED.
  - `sponsor-transfer-portability-terms.csv`: 12 sponsors plus 1 ecosystem row.
  - `nonprofit-donate-page-daf-scan-2026.csv`: 75 and 25 pages.
  - `data/rcf-ren-audited-admin-payments-2020-2024.csv`: $19,225,546 at 98%.
- No web fetch was needed, and no crt.sh, certspotter or sec.gov request was made. Nothing in the repo was edited except the two output files. No commit or push.

## Counts

| Result | Count |
|---|---|
| confirmed | 33 |
| partially_confirmed | 11 |
| contradicted | 1 |
| unverifiable | 0 |
| **Total** | **45** |

**Exact corrections:** 14 against `strategic-synthesis.md`. A script checks that every Find occurs exactly once and that sequential application succeeds (0 problems).

## Findings

### 1. The figures hold
Every figure in §0 traces to its cited governing source, and all nine wave-33B §0 corrections (b10–b18) are applied correctly. The A1/G2 account basis, the Ayco caveat, the NPT $42.12bn / $327.87bn basis, the adviser-cap citations, 44/151 and 2/15, 13 of 20, the Fidelity share citation and the PGP item are all in place. No number in §0 is wrong.

### 2. Waves 32A–33B: what §0 misses or understates
- **The source line is stale (V34S-01).** §0 cites report §11.28–§11.31 (waves 31A–32B), but it already carries wave-33B text, and §11.32 (33A) and §11.33 (33B) exist. No wave-33A finding appears in §0.
- **Startup cohort (V34S-20, wave 32A).** The cohort's only pivot, Uncommon Giving, fails the pre-registered window rule: it has a FY2020 DAFRC row and launched on 2020-07-28. Without it the cohort is 17 with 0 pivots. Report §11.30 calls the strict subset (n=8) "the cleaner read". §0 gives the 18-member split without either caveat.
- **Exception-load (V34S-09, V34S-44, wave 32A).**
  - The 11.0% stands as rounded (10.96% after the totals-row fix). But §0's "broader" proxy is the source's *core* definition; the source's *broad* definition is 25% / 20%.
  - **G10 is contradicted as worded.** It says the proxy "bounds what could need review". Wave 32A finds the ER set both too wide (conduit and common-fund PFs; Founders Pledge on Pub 78) and too narrow (donor-controlled Type I, II and FI Type III SOs; Pub 78 SOUNK; grants to foreign individuals). The source itself calls the proxy an "upper-leaning screen". So it is an indicator, not a bound.
- **Processor rules (V34S-41, wave 33A).** G4 says processor complaints "describe payout rules". Wave 33A re-read 22 rule pages:
  - written rules fully explain only 2 of 7 named complaints (-001, -034);
  - -036 is now partial and -039 unverified;
  - 11 of 14 grant-delay records predate the rule versions they were coded against.

  The G4 sentence is true of what the complaints *say*, but read on its own it overstates how well the rules explain them.
- **Long-tail cost (V34S-35, wave 33A).** D's "standalone long-tail business" item rests only on the 2.84% asset share. Wave 33A adds the cost side: tail CFs' allocated operating cost is a median 205 bps of DAF assets, against 102 bps at top-50 CFs. That is 2.0× on rule A but 1.6× on the admin-only floor, and rule A compares whole organisations. This strengthens D.
- **Recipient DAF share (wave 33A).** Top-50 DAF grants are a median 5.9% (pooled 6.9%) of recipients' line 1h. The pooled share falls from 17.8% under $1m of revenue to 3.7% at $100m and over. It is a governing, validated figure that bears on G4 (nonprofit-side cost) and is absent from §0. It is proposed as a Notable line.
- **Complaints, state law and tax guidance (waves 32B, 33B).** A11, A7, A10 and F match the governing text.
  - The New Jersey hospital-conversion clause (P.L.2014 c.82) is a narrow court-reallocation rule, so "no mandate" stands.
  - Wave 33B's tax-guidance findings support A10: six of seven top-10 sponsor pages say DAF gifts fall outside §170(p).
  - In F, "which would have codified" is the source's own [F/I] conclusion, but §0 leaves it untagged (V34S-37).

### 3. Top-ten items that are overstated
- **G6, staff cost (V34S-43).** "78.7 bps against 2.9 bps" sets community foundations' pooled, whole-organisation Part IX lines 5–10 against *affiliated-commercial* sponsors, whose staff sit at parent firms. The self-staffed nationals run 5.6–8.6 bps (AEF 15.0), and the governing wave-28 text puts the gap at about 3.5–9×, not about 27×.
- **G10, review-need proxy (V34S-44).** See above.
- **G1, DAF Direct (V34S-33).** The "3 sponsors" are the home page's list. One of them, BNY Mellon Charitable Gift Fund, ended its DAF program in December 2024 (report §11.29; league table). The closure point stands, but the live count is two.
- **G7 and C, Ren receipts (V34S-26).** The $44.98m floor counts sponsors' top-five contractor lines only. Wave 33B asked for that limit to be kept (C-R05), and 85.8% is [S] in the source.
- **C, legacy attrition (V34S-28).** "No Ren attrition yet" rests on smaller payers. MS GIFT, RCF, US Charitable Gift Trust and NCF have not filed FY2025 (wave 33B, A06).
- **D, holding funds (V34S-34).** "Only where" generalises from three observed, unadjudicated cases.
- **Notable, international (V34S-45).** 7.8% is of top-50 sponsors' net Schedule I plus line 3 dollars, and the source calls it upper-leaning. It is not 7.8% of all DAF grants.

### 4. Basis notes (no correction needed)
- **Donate pages.** The 41.2% / 13.7% figures are on the wave-24B corrected base of 182 pages. The direction file's body still shows 40.3% / 13.4% on 186, but its governing correction supports 41.2%.
- **Long tail.** The 1,240 / 2.84% figures are on corrected assets. Raw DAFRC gives 1,235 / 2.80%.
- **AI census.** Daffy Quick Donate is also flagged money_moving "yes (recommendation)", but the census treats it as not moving money, so "only two" stands.
- **$0.45 per heavy review.** This figure is [S] in its source.

### 5. Do the A–G items still reflect the evidence?
Yes. No A–G verdict (contradicted, suggestive or unsupported) needs to change.
- The startup verdict "Suggestive; Low-Medium" already allows for the window issue.
- The complaint verdict "Contradicted as a quality measure" is reinforced by wave 32B's AOGF strict 24.1 per $1bn.
- The corrections below change wording and scope, not any verdict.

## Exact corrections

### `research/mission-2026-11-14/strategic-synthesis.md`

Apply in order. Each Find occurs exactly once in the file as it stands on 2026-11-19. In a Find or Replace, `\n` stands for a newline.

1. **§0 source line: add §11.32–§11.33** (V34S-01).
   - **Find:** "the industry report's [§11.28–§11.31](../DAF-INDUSTRY-REPORT-2026-11.md) (waves 31A–32B);"
   - **Replace with:** "the industry report's [§11.28–§11.33](../DAF-INDUSTRY-REPORT-2026-11.md) (waves 31A–33B) [V wave 34S];"
2. **A, exception-load: name the definition** (V34S-09).
   - **Find:** "A broader review-need proxy is 7.4% of top-50 recipient lines and 11.0% of dollars."
   - **Replace with:** "A broader review-need proxy (the source's "core" definition) is 7.4% of top-50 recipient lines and 11.0% of dollars (7.41% / 10.96% without a $212.2m Greater Horizons totals row); the source's "broad" definition gives 25% / 20% [V wave 34S]."
3. **A, startup cohort: Uncommon Giving window failure** (V34S-20).
   - **Find:** "18 entrants from 2021–2026 show no documented shutdown: 10 active, 1 acquired, 1 pivoted, 6 unknown"
   - **Replace with:** "18 entrants from 2021–2026 show no documented shutdown: 10 active, 1 acquired, 1 pivoted, 6 unknown. The one pivot, Uncommon Giving, fails the window rule (its DAF launched in 2020); without it the cohort is 17 with no pivot, and the strict subset (n=8) is the cleaner read [V wave 34S]"
4. **C, Ren receipts: top-five contractor-line limit** (V34S-26).
   - **Find:** "Named Ren receipts are a $44.98m floor, 85.8% from three customers"
   - **Replace with:** "Named Ren receipts are a $44.98m floor (sponsors' top-five contractor lines only), 85.8% from three customers [V wave 34S]"
5. **C, legacy attrition: largest Ren clients not yet filed** (V34S-28).
   - **Find:** "FY2025 filings show no Ren attrition yet ([gap19-fy2025-refresh.md](gap19-fy2025-refresh.md); wave 31A)."
   - **Replace with:** "FY2025 filings show no Ren attrition yet, but the largest Ren clients (MS GIFT, RCF, US Charitable Gift Trust, NCF) have not filed FY2025 ([gap19-fy2025-refresh.md](gap19-fy2025-refresh.md); wave 31A) [V wave 34S]."
6. **D, holding donor funds: three observed cases** (V34S-34).
   - **Find:** "Losses occurred only where one operator held unsegregated funds"
   - **Replace with:** "In the three documented loss cases (Ammado, Flipcause, SDG Impact Fund), one operator held donor money that was not segregated; the causes are not adjudicated [V wave 34S]"
7. **D, long tail: add wave-33A operating cost** (V34S-35; wave 33A).
   - **Find:** "The 1,240 sponsors under $50m hold 2.84% of assets ([direction-long-tail-sponsors.md](direction-long-tail-sponsors.md); wave 30)."
   - **Replace with:** "The 1,240 sponsors under $50m hold 2.84% of assets ([direction-long-tail-sponsors.md](direction-long-tail-sponsors.md); wave 30). Tail community foundations' allocated operating cost is a median 205 bps of DAF assets, twice top-50 CFs' 102 bps on rule A but 1.6× on an admin-only floor; rule A compares whole organisations ([b45n33-long-tail-operating-cost.md](b45n33-long-tail-operating-cost.md); wave 33A) [V wave 34S]."
8. **F, tax guidance: tag the inference** (V34S-37).
   - **Find:** "The §4967 prohibited-benefits project, which would have codified the Notice 2017-73 pledge rule, has left the plan"
   - **Replace with:** "The §4967 prohibited-benefits project, the only formal project that would have codified the Notice 2017-73 pledge rule [I], has left the plan [V wave 34S]"
9. **G1, DAF Direct: one listed sponsor has ended** (V34S-33).
   - **Find:** "limit automated access ([queue-batch34-escheat-terms.md](queue-batch34-escheat-terms.md)). DAF Direct is closed, with 3 sponsors"
   - **Replace with:** "limit automated access ([queue-batch34-escheat-terms.md](queue-batch34-escheat-terms.md)). DAF Direct is closed, with 3 listed sponsors, one of which (BNY Mellon Charitable Gift Fund) ended its DAF program in December 2024 [V wave 34S]"
10. **G4, processor complaints: add wave-33A rule fit** (V34S-41).
   - **Find:** "Processor complaints describe payout rules: paper-check thresholds, lost checks and EFT vetting ([gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md); wave 32B)."
   - **Replace with:** "Processor complaints describe payout rules: paper-check thresholds, lost checks and EFT vetting ([gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md); wave 32B). Re-read rules show $100 check thresholds, monthly batches and redirection to employer- or processor-chosen charities, but written rules fully explain only two of seven named complaints, and 11 of 14 grant-delay records predate the rule versions read ([g1913-processor-disbursement-rules.md](g1913-processor-disbursement-rules.md); wave 33A) [V wave 34S]."
11. **G6, staff cost: name the comparator** (V34S-43).
   - **Find:** "Staff cost is 78.7 bps against 2.9 bps ([direction-sponsor-executive-compensation.md](direction-sponsor-executive-compensation.md))."
   - **Replace with:** "Staff cost (Part IX lines 5–10, whole organisation) is 78.7 bps of DAF assets at community foundations, against 5.6–15.0 bps at the four self-staffed nationals (CF cost about 3.5–9× theirs) and 2.9 bps at affiliated-commercial sponsors, whose staff sit at the parent firm ([direction-sponsor-executive-compensation.md](direction-sponsor-executive-compensation.md)) [V wave 34S]."
12. **G10, review-need proxy: not a bound** (V34S-44).
   - **Find:** "The review-need proxy (11.0% of top-50 dollars) bounds what could need review, but no observed review data exist"
   - **Replace with:** "The review-need proxy (11.0% of top-50 dollars; 10.96% corrected) indicates the scale of recipients that could need review. It is not a bound: it counts lines that sponsors clear by standing rule, and it misses donor-controlled supporting organisations and grants to individuals. No observed review data exist [V wave 34S]"
13. **Notable, international share: state the base** (V34S-45).
   - **Find:** "International grants are 7.8% of DAF grants with direct foreign grants included"
   - **Replace with:** "International grants (NTEE Q recipients plus direct foreign grants) are 7.8% of top-50 sponsors' net Schedule I plus line 3 dollars, an upper-leaning combination [V wave 34S]"
14. **Notable: add wave-33A recipient DAF share** (wave 33A; not in §0).
   - **Find:** "- The startup cohort shows no documented shutdown ([gap19-startup-cohort.md](gap19-startup-cohort.md)). [gap19-11]"
   - **Replace with:** "- The startup cohort shows no documented shutdown ([gap19-startup-cohort.md](gap19-startup-cohort.md)). [gap19-11]\n- Top-50 DAF grants are a median 5.9% (pooled 6.9%) of recipients' line 1h contributions, falling from 17.8% pooled under $1m of revenue to 3.7% at $100m and over ([b40n12-daf-share-of-recipient-revenue.md](b40n12-daf-share-of-recipient-revenue.md); wave 33A) [V wave 34S]."

## Check script
Run: `scratchpad/v34s/corr.py` and `scratchpad/v34s/check_report.py`, both in this session's scratchpad (not committed). The check parses this section and finds 14 Find strings, each occurring exactly once. Every Replace carries "[V wave 34S]". Sequential application gives 0 problems.
