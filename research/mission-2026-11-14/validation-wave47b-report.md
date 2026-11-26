# Validation wave 47B: Charity Navigator rating eligibility at grant time

**Date:** 2026-11-20 · **Validator:** validator wave 47B · **Study validated:** [b40n1202-b43n26-04-cn-eligibility-by-year.md](b40n1202-b43n26-04-cn-eligibility-by-year.md), with [`cn-eligibility-by-year-2026-11-20.csv`](../../data/mission-2026-11-14/cn-eligibility-by-year-2026-11-20.csv) and [`scripts/mission_cn_eligibility_by_year.py`](../../scripts/mission_cn_eligibility_by_year.py)
**Register:** [`validation-register-wave47b.csv`](../../data/mission-2026-11-14/validation-register-wave47b.csv) (20 rows)

Wave 47A's three studies (b40n1202-04, b45n33-02-01, g050303-01) were not touched. No repo file other than this report and the register was written. Nothing was committed.

## Counts

| Result | Rows |
|---|---|
| confirmed | 15 |
| partially confirmed | 5 |
| contradicted | 0 |
| unverifiable | 0 |
| **Total** | **20** |

All ten headline claims are confirmed (V47B-01 to -10), and so is the 20-recipient spot-check (V47B-11). The five partial confirmations concern how the results are read, plus two citation and list slips. No number is wrong.

## Method

1. **Re-run.** The repo script was re-run from the same caches with `python3 -B`, writing to scratch. The CSV (391 rows) and the JSON summary are byte-identical to the committed CSV and to the study's `q0426/final.json`.
2. **Independent checks** (own stdlib code; no repo imports):
   - the OBJECT_ID/DLN Julian-day check over all ten index files (2017–2026);
   - processing-year coverage counts;
   - a re-implementation of CN's filing tests, run on 20 recipients at each of their sponsor cut-offs and on November 2026 filings, with BMF status;
   - the lost dollars broken down by BMF ruling year and first e-filed tax period, from a per-unit dump of the study's own units.
3. **Primary-source fetches** (user agent `research-script/1.0`; robots checked first and logged):
   - six return XMLs from the GivingTuesday mirror of IRS TEOS: The 85 Fund TY2021 and TY2022, Biohub Inc TY2022, Compassion TY2019 (990) and TY2021 (990-T), Just Trust TY2022;
   - 34 HEAD requests for the Last-Modified dates of TEOS batch and index files (32 returned 200; 2026_11A and 2026_12A are not posted yet);
   - CN's release-notes page;
   - Pub. L. 116-25 on govinfo.gov.
4. **Sensitivities.** A wrapper imports the repo script without modifying it, swaps the processing-date function or the index set, and writes to scratch. Variants:
   - each return dated from its TEOS posting (third Wednesday of the month after processing, the 2025–26 pattern);
   - TEOS posting plus 63 days, the longest 2025–26 gap between CN data refreshes;
   - index files from 2021 on only.

**Robots and fetch log** (scratchpad `v47b/robots/`, `v47b/fetchlog.tsv`):
- apps.irs.gov/robots.txt returns 302 to www.irs.gov/404, so the host has no robots file.
- www.irs.gov, www.charitynavigator.org and www.govinfo.gov have only `User-agent: *` groups, with no ClaudeBot, anthropic-ai or Claude-* group, and the paths used are not disallowed. CN disallows `/profile`, `/search` and `/basket`, and none of them was fetched.
- gt990datalake-rawdata.s3.amazonaws.com/robots.txt returns 404.
- No blocked host was used. sec.gov, crt.sh and certspotter were not used. There was no login or outreach.

## Findings

### F1. The numbers reproduce exactly (V47B-01 to -05, -18, -19)
- **Grant-time share.** 72.6557% ($53,818,778,086 of $74,073,755,051).
- **Current status.** 76.8507%; the self-check gives 0.7685074.
- **By grant year.** FY2023 68.11% vs 73.73%; FY2024 76.68% vs 79.62%.
- **FY start.** 68.83%.
- **Variants.** 72.36–72.66%; the gap bound gives 74.67%.
- **CZ look-through.** 74.81% at grant time, 79.00% now.
- **Lost dollars.** $3,496.6m (30,541 units, 15,294 recipients), of which $2,914.2m fails the three-return rule.
- **Gained dollars.** $389.1m.
- **Coverage counts.** 88,373, 146,340 and 150,057 all match.

### F2. The named cases hold against the index and the return headers (V47B-06 to -08, -10, -11)
- **The 85 Fund.**
  - Its TY2022 return is OBJECT_ID 202313199349307191. Julian day 319 is 2023-11-15, and the XML `ReturnTs` is 2023-11-08.
  - At its sponsor's 2023-06-30 year end it had two e-filed returns (TY2020 and TY2021).
- **Compassion International.**
  - It filed full 990s for tax periods ending June 2016–2019, then only 990-T from June 2021. Both XMLs confirm the return types.
  - Its 2023 pass depends on the TY2017–2018 returns, which are only in the 2017/2018 index files.
- **Biohub Inc.**
  - Its TY2022 return was processed on 2023-11-14 (`ReturnTs` 2023-11-14).
  - At 2023-12-31 it has five periods in the 2017–2022 window. It would still pass without that return.
- **Ruling dates.** KIPP NY (ruling 202512) and Christian Union (202505) have full 990s back to TY2016. This confirms that RULING cannot date first recognition.
- **Spot-check.** 20 of 20 recipients match:
  - 12 top-lost and 7 top-gained recipients, plus Biohub Inc;
  - re-tested with independent code at every listed cut-off.

### F3. The Julian-day identity holds on all 5,542,528 rows (V47B-09), but it is a consistency check, not a timing check
- On 990, 990-EZ and 990-PF rows in the 2017–2026 index files, OBJECT_ID[5:8] equals DLN[5:8], and the year digits agree, with no exceptions.
- The TEOS object id is derived from the DLN, so this shows the processing date is read correctly. It says nothing about when a return became public.
- The script docstring says the check covered 2019–2026; the note says 2017–2026. Both hold.

### F4. "Processed by FY end" is optimistic but close (V47B-13)
- **Posting lag.**
  - Last-Modified dates for the 2025–26 monthly batches (not re-uploaded) show batch M posted in mid-to-late month M+1. Examples: 2025_11A on 17 Dec 2025, 2026_06A on 15 Jul 2026, 2026_10A on 18 Nov 2026. 2026_11A is not posted yet.
  - The 2023–24 files were all re-uploaded on 6 March 2025, so their first posting cannot be seen.
- **CN's refresh cycle.** CN's release notes show data refreshes every one to two months in 2025–26. The 2024 entries are incomplete: versions 19–20 date from Nov–Dec 2024, and earlier versions are not listed.
- **Effect** (validator runs):

| Availability rule | Both years | FY2023 | FY2024 |
|---|---|---|---|
| Processed by FY end (headline) | 72.66% | 68.11% | 76.68% |
| On TEOS by FY end (third Wednesday of the month after processing) | 72.58% | 67.99% | 76.65% |
| On TEOS plus 63 days (CN refresh) | 71.50% | 66.52% | 75.91% |
| Processed by FY start (study's lag bracket) | 68.83% | 64.75% | 72.44% |

- **Judgement.** The proxy is sound as a year-end, upper-leaning measure. Realistic lags cost 0.1–1.2 points and stay well inside the study's own 68.83% bracket.
- **Correction.** The note's statement that there is "no evidence of a publication lag" is true of the batch IDs but not of the batch files. A correction adds the posting-lag figures.
- **What remains unobserved.** "Must directly receive" (CN's receipt) cannot be observed.

### F5. Applying CN's 2026 rules to 2023–24 grants is acceptable as a counterfactual (V47B-14)
- **The question.** The repo uses the figure to ask whether DAF dollars went to organisations a rating could cover. The right test is today's rules on the filings that existed at grant time, and that is what the study measures.
- **Documented rule changes.** CN's release notes begin on 18 Sep 2023. The only eligibility change they list is the 8 Apr 2024 DAF exclusion, which is worth 0.47 points.
- **Before September 2023.** Rules in force for earlier grants are not documented on that page.
- **Labelling.** Call the figure "eligible under CN's current rules, at grant time". It is not CN's actual 2023 coverage.

### F6. The 2021+ rule does not argue for 72.36% (V47B-15)
- **Why the early files are needed.** The data describe eligibility in 2023–24. The six-year window is CN's own rule, and at a 2023 cut-off it needs tax years 2017–2022. The 2017/2018 index files are the record of those filings.
- **Effect of dropping them.** Dropping them is not a choice of evidence vintage. It treats organisations that filed as non-filers.
- **72.36% is not a 2021+ figure either.** It still reads the 2019–2020 files.
- **A literal 2021+ run.** Reading only the 2021–2026 files gives 61.60% (FY2023 45.31%; FY start 24.33%). That is plainly wrong, because the filings exist.
- **The parent is unaffected.** Its current-status figure barely depends on pre-2021 files (76.849% against 76.851%).
- **Recommendation.** **Headline 72.66%**, with 72.36% disclosed as a variant.

### F7. "The gap is organisational age" is two-thirds right (V47B-12)
- **Young organisations.** Of the $3.50bn lost, $2.35bn (67%) went to recipients with a BMF ruling in 2020 or later.
- **Older organisations.** $0.76bn (1.02 points; 5,510 recipients) went to recipients ruled by 2018 whose first e-filed return has a tax period ending July 2020 or later.
  - That fits paper filing until the Taxpayer First Act made 990 e-filing mandatory for tax years beginning after 1 July 2019 (Pub. L. 116-25 §3101) [I].
  - The 85 Fund, the study's lead example, is one (XML `FormationYr` 2004; BMF ruling 2011).
- **Reading.** CN counts only e-filed returns, so the test is right; only the reading needs changing. Corrections are below.

### F8. Minor slips (V47B-16, -17)
- **§2.3 list.** It omits Morgan Stanley GIFT FY2024, at 70.9% of $1.19bn. That is lower than DAFgiving360 FY2024 and both Fidelity years.
- **Source labels.** Two citations say S6, which is Pub 78 in the note's own register, where S8 (the CN help article) is meant.

### Repo text that should cite grant-time eligibility
- **FINAL-STATUS.md.** It cites 76.9% twice (the PR #68 bullet and the "76.5–76.9%" sentence, line 375) with no grant-time figure. Two corrections are proposed.
- **Parent note.** Its headline (§0) and limit 7 cite 76.9% and note the timing gap without the result. Two corrections are proposed.
- **strategic-synthesis.md.** It has no 76.85%/76.9% eligibility figure, so no change is needed.
- **Industry report.** 76.9% appears only in the §11 paragraphs of waves 34B and 46A, which are left unedited. The new §11.70 carries the grant-time figure.
- **FINAL-STATUS summary table.** It reads "§11.1–§11.68"; the consolidator should update it once §11.69–§11.70 land. No correction is proposed here, to avoid colliding with 47A.

## Accept / modify / reject

| Study claim | Decision | Note |
|---|---|---|
| 72.66% grant-time vs 76.85% current; 0.768507 reproduces | **Accept** | Byte-identical re-run |
| FY2023 68.11% vs 73.73%; FY2024 76.68% vs 79.62% | **Accept** | |
| FY-start 68.83% | **Accept** | Also the outer bound for lags |
| Variants 72.36–72.66%; loose bound 74.67% | **Accept** | 72.36% is not a 2021+ figure |
| $3.50bn lost, $2.91bn on the three-return rule; top names | **Accept** | |
| 85 Fund TY2022 processed 2023-11-15 | **Accept** | Index plus XML header |
| $0.39bn gained; Compassion to 990-T only | **Accept** | |
| CZ look-through 74.81% / 79.00%; Biohub Inc passes | **Accept** | Robust to lags |
| OBJECT_ID Julian day = DLN Julian day (5.5m rows) | **Accept** | 5,542,528 rows; consistency only |
| KIPP NY and Christian Union ruling anomalies | **Accept** | |
| "No evidence of a publication lag" | **Modify** | Posting lag exists; 72.58% / 71.50% |
| "Most of the drop is young organisations"; "gap is organisational age" | **Modify** | About a fifth of lost dollars are pre-2019 organisations new to e-filing |
| "Owner may prefer 72.36% under the 2021+ rule" | **Modify** | Keep 72.66% as the headline; a literal 2021+ run gives 61.60% |
| CN 2026 rules applied to 2023–24 | **Accept with label** | Counterfactual "current rules at grant time" |
| §2.3 lowest sponsor-years | **Modify** | Add MS GIFT FY2024 70.9% |
| Source labels S6 | **Modify** | S8 |
| None | **Reject** | No claim is rejected |

## Limits

- CN's actual receipt dates and 2023–24 refresh dates are not public. The 63-day lag is modelled on the 2025–26 cadence.
- The ruling-year split relies on the current BMF RULING field, which later determinations can reset (V47B-10).
- The paper-filing reading is an inference: pre-2020 paper returns are not in TEOS.
- The spot-check covers the largest movers, not a random sample.

## Source register

| Source | URL | Accessed | Use |
|---|---|---|---|
| IRS TEOS e-file index 2017–2026 | https://apps.irs.gov/pub/epostcard/990/xml/2017/index_2017.csv (and each year to 2026) | Cached 2026-11-14/15 and 2026-11-20 | Julian-day check, coverage, spot-check |
| IRS TEOS monthly XML batches (HEAD, Last-Modified) | https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_11A.zip (2023_11A–2026_12A as logged) | 2026-11-20 | Posting lag |
| Return XML, GivingTuesday mirror of IRS TEOS | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202313199349307191_public.xml (and 202223199349301462, 202303189349301730, 201922899349300442, 202142999339300504, 202343199349327379) | 2026-11-20 | Return headers |
| IRS EO BMF | https://www.irs.gov/pub/irs-soi/eo1.csv (eo1–eo4) | Cached 2026-11-14 | Subsection, foundation, ruling |
| Charity Navigator release notes | https://www.charitynavigator.org/about-us/our-methodology/ratings/release-notes/ | 2026-11-20 | Rule history, refresh cadence |
| Charity Navigator help article | https://intercom.help/charity-navigator/en/articles/8557824-charity-navigator-s-rating-system | As quoted by the parent (2026-11-19) | Rules |
| Taxpayer First Act, Pub. L. 116-25 §3101 | https://www.govinfo.gov/content/pkg/PLAW-116publ25/html/PLAW-116publ25.htm | 2026-11-20 | 990 e-file mandate (law in force; context for an inference) |

## Exact corrections

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.70 Charity Navigator eligibility at grant time (validated, wave 47B)\n\n**Charity Navigator eligibility at grant time** (validated, wave 47B). The grant-time study re-runs byte for byte and reproduces the parent’s 76.85% (0.768507). Tested against the filings the IRS had processed by each sponsor’s fiscal-year end, 72.66% of top-50 FY2023–24 DAF-weighted dollars ($53.82bn of $74.07bn) went to recipients that were rating-eligible when the grant was made: 68.11% in FY2023 and 76.68% in FY2024. An independent pass over the IRS e-file index confirms the processing-date rule (0 mismatches in 5,542,528 rows) and 20 sampled recipients’ transitions. Among them is The 85 Fund, whose third e-filed return was processed on 2023-11-15. Dating each return from its observed TEOS posting gives 72.58%. Adding two months for Charity Navigator’s refresh cycle gives 71.50%, and grants on day one give 68.83%. About $0.76bn of the $3.50bn lost went to older organisations whose e-filed history begins in 2020, after the e-file mandate, not to young ones [I]. Reading only IRS files from 2021 on would give 61.60%, because the six-year window would lose returns it needs, so 72.66% stays the headline. With the CZ LLCs looked through to Biohub Inc, it is 74.81% (repo [`validation-wave47b-report.md`](mission-2026-11-14/validation-wave47b-report.md)) [V wave 47B]\n\n---\n\n## Source register"

### `research/mission-2026-11-14/FINAL-STATUS.md`

**Find:** "so the eligible upper bound falls from 77.3% to 76.9%."
**Replace with:** "so the eligible upper bound falls from 77.3% to 76.9%.\n  - These shares use filings available in November 2026. Tested against the filings the IRS had processed by each sponsor’s fiscal-year end, the grant-time share is 72.7% (FY2023 68.1%, FY2024 76.7%; 68.8% if every grant fell on the first day of the year) (b40n1202-b43n26-04). [V wave 47B]"

**Find:** "76.5–76.9% of top-50 DAF dollars go to recipients eligible for a Charity Navigator rating."
**Replace with:** "76.5–76.9% of top-50 DAF dollars go to recipients eligible for a Charity Navigator rating on November 2026 filings. At grant time (filings processed by each sponsor’s fiscal-year end) the share is 72.7% (72.4–72.7% across variants; 71.5% allowing for IRS posting and Charity Navigator refresh lags) (b40n1202-b43n26-04). [V wave 47B]"

### `research/mission-2026-11-14/b40n1202-b43n26-recipient-basis-and-rating-eligibility.md`

**Find:** "On the as-filed Schedule I basis the dollar share is 76.3%."
**Replace with:** "On the as-filed Schedule I basis the dollar share is 76.3%. These shares use filings available in November 2026. Tested against the filings processed by each sponsor’s fiscal-year end, the grant-time share is 72.66% ($53.82bn; FY2023 68.11%, FY2024 76.68%) ([b40n1202-b43n26-04-cn-eligibility-by-year.md](b40n1202-b43n26-04-cn-eligibility-by-year.md)). [V wave 47B]"

**Find:** "The TEOS index for 2026 is partial: it was downloaded 2026-11-15."
**Replace with:** "The TEOS index for 2026 is partial: it was downloaded 2026-11-15. The follow-up b40n1202-b43n26-04 re-tests each grant against filings processed by its sponsor’s fiscal-year end: 72.66% against 76.85% (68.83% at the year start). [V wave 47B]"

### `research/mission-2026-11-14/b40n1202-b43n26-04-cn-eligibility-by-year.md`

**Find:** "  - Most of the drop is young organisations that had not yet filed three e-filed returns: $2.91bn fails the three-return rule at grant time."
**Replace with:** "  - Most of the drop is organisations that had not yet filed three e-filed returns: $2.91bn fails the three-return rule at grant time. About two-thirds of the $3.50bn ($2.35bn) went to recipients with a BMF ruling in 2020 or later. $0.76bn (1.02 points) went to recipients ruled by 2018 whose first e-filed return has a tax period ending July 2020 or later. That pattern fits paper filing until the e-file mandate (Pub. L. 116-25 §3101) [I]; The 85 Fund (formed 2004, ruling 2011) is one. [V wave 47B]"

**Find:** "The owner may prefer the 2019-on-only variant (72.36%) under the 2021+ evidence rule (§3.1)."
**Replace with:** "The 2019-on-only variant (72.36%) is not a 2021+-only figure, since it still reads the 2019–2020 files. Reading only the 2021–2026 files gives 61.60% (FY2023 45.31%), because CN’s window at a 2023 cut-off needs tax years 2017–2022. 72.66% stays the headline, and 72.36% is a disclosed variant. [V wave 47B]"

**Find:** "The batch IDs therefore give no evidence of a publication lag, and none is assumed beyond the FY-start variant."
**Replace with:** "The batch IDs therefore give no evidence of a publication lag, and none is assumed beyond the FY-start variant. The batch files do show one: their 2025–26 Last-Modified dates put each month’s batch on TEOS in mid-to-late month M+1. Dating each return from that posting gives 72.58% (FY2023 67.99%, FY2024 76.65%). Adding 63 days for CN’s data-refresh cycle gives 71.50%. [V wave 47B]"

**Find:** "The rules come from CN's help article (S6) [P]:"
**Replace with:** "The rules come from CN's help article (S8) [P]: [V wave 47B]"

**Find:** "- **The gap is organisational age.** Recipients that are rateable today but were one or two returns short at grant time account for 4.4 of the 4.7 points lost."
**Replace with:** "- **The gap is mostly organisational age, partly the e-file mandate.** Recipients that are rateable today but had fewer than three e-filed returns at grant time (including none) account for 4.4 of the 4.7 points lost. About 1.0 point of the 4.7 is older organisations whose e-filed history starts with tax periods ending in July 2020 or later [I]. [V wave 47B]"

**Find:** "- Fidelity Charitable: 73.3% (FY2023) and 75.7% (FY2024)."
**Replace with:** "- Fidelity Charitable: 73.3% (FY2023) and 75.7% (FY2024).\n- Morgan Stanley Global Impact Funding Trust: 70.9% of $1.19bn (FY2024). [V wave 47B]"

**Find:** "without defining them [P, S6]."
**Replace with:** "without defining them [P, S8]. [V wave 47B]"

