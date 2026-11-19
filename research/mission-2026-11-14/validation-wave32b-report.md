# Validation wave 32B: complaints with denominators (P-GAP19-13) and the 50-state DAF-law check (P-GAP19-14)

**Validator:** independent-validation-agent-wave32b | **Date:** 2026-11-19 | **Register:** [`validation-register-wave32b.csv`](../../data/mission-2026-11-14/validation-register-wave32b.csv) (45 claims, V32B-01 to V32B-45)

**Method.** I read the data before the conclusions, and re-ran both scripts with all output sent to scratch (`scratchpad/v32b/`). The complaint script was loaded as a module with `OUT` pointed at scratch; its output file path is hard-coded, so `--force` was not needed and nothing in the repo was overwritten. The state script's `build` stage was run from a scratch working directory against the original raw JSON in `scratchpad/ge14/`.

- I recomputed the Poisson intervals with my own inversion of the regularized incomplete gamma function, and I re-derived every denominator from the DAFRC FY2024 file and the applied R1 rows.
- I re-read every Trustpilot record (33) from the pages' embedded JSON, all 6 Google Play records, 6 BBB records and 2 give.org reports. That is 47 of 47 additions.
- I re-read 15 official texts (NJ P.L.2018 c.29, NJ P.L.2014 c.82, NJ S2247 I1, NC SB 684, MO HB 1181 and HB 2216, MS SB 2210, OH SB 12, HI Acts 205 and 108, HI HB 992 HD1, Iowa 15E.305, N.D.C.C. 57-38, KS K.A.R. 92-12-152, CA FPPC Reg. 18424.3) and re-ran one Florida official search.
- robots.txt was read before the first request to each host. No sec.gov, crt.sh or certspotter requests were made, there was no outreach, and all evidence is from 2021 or later except the enacted texts under test.

---

## 1. Summary of results

| Result | Count | P-GAP19-13 (complaints) | P-GAP19-14 (state law) |
|---|---|---|---|
| confirmed | 31 | 15 | 16 |
| partially_confirmed | 10 | 5 | 5 |
| contradicted | 3 | 2 | 1 |
| unverifiable | 1 | 0 | 1 |
| **Total** | **45** | **22** | **23** |

**Bottom line.** Both studies reproduce exactly from their scripts, and their sources check out. The complaint study's denominators, frame, intervals and record-level coding are sound. It has two real defects: duplicate incidents are counted twice in the `all_venues` and `review_venues` scopes, and the window is mis-stated as 5.883 years. Its AOGF headline is also soft, because it includes non-US Benevity reviewers. The state study's "no mandate" negative holds, within the limits it states itself. Its New Jersey correction is right, but it dates the DAF clause to the wrong act: the clause was added by P.L.2014 c.82, not by P.L.2018 c.29. All 47 of its Open States bill-page URLs now return 404.

---

## 2. Findings: P-GAP19-13 (complaints with denominators)

1. **Reproduction and denominators are exact (V32B-01 to -04).**
   - The re-run output is byte-identical to the repo CSV (67 rows).
   - All 20 FY2024 account and grant denominators equal the DAFRC values with the applied R1 corrections. Examples: GS DAPF 3,613 → 4,134 accounts; PPGF 694,979 → 380,644 accounts; NFG grants $427.9m → $199.8m.
   - The top-15 frame matches league-table ranks 1–15, and the processor top five matches the corrected grants (Mightycause sixth).
   - The Garwood intervals match my independent computation to 3 dp for every n checked (0, 1, 3, 9, 27, 50, 56).
2. **Duplicates are double-counted outside `strict` (V32B-08, -09).**
   - The script removes `dup_of` records only in `strict`.
   - **PPGF all_venues (n=5)** counts the same Alaska suit twice (CMP-232 and CMP-G1913-046). The 4 distinct records give 0.105 per 10k [0.029–0.269] and 5.03 per $1bn [1.37–12.87], against the 0.131 and 6.28 reported.
   - **NFG** counts the Trustpilot/BBB pair -037/-040 twice: review_venues 8 → 7 distinct (35.0 per $1bn [14.1–72.2], against the 40.0 headline) and all_venues 9 → 8.
   - The pooled processor rows inherit both pairs: review 67 → 66, at 24.42 per $1bn [18.89–31.07].
3. **AOGF headline mixes in non-US programmes (V32B-07).**
   - The 56 review-venue records include 9 added Trustpilot reviews from CA, AU, GB, FR, CH and ID reviewers, and 27 corpus records with no country token.
   - On the strict scope (47 records), the rate is 24.1 per $1bn and the ratio to Fidelity is 11.3×, not about 13×.
4. **Window length mis-stated (V32B-05).** The text says 5.883 years in four places. The script and CSV use 5.881 (2,148 days ÷ 365.25).
5. **Record-level checks pass (V32B-12, -14, -16, -17, -18).**
   - All 33 Trustpilot review ids, publish dates, countries, star ratings and quotes match the live pages.
   - The Google Play listing figures match (3.8 stars, 29 reviews, 5K+ downloads, updated 2026-11-09; 3.2 stars, 94 reviews, 50K+), as do the BBB profile counts (24/5 and 17/10) and the give.org text (Alaska, March 2026, Case No. 3AN-26-CI, 2 complaints in 36 months).
   - No reviewer display name appears anywhere, and the longest quote is 14 words.
6. **Coding challenges, not errors (V32B-13, -15).**
   - CMP-G1913-002 (a lost check, voided at 180 days) fits `payment_rail_fees` better than `nonprofit_receipt_attribution`.
   - The Fidelity Android crash records are coded high, but the corpus's two most recent iOS crash-on-launch records (Oct 2026) are coded medium.
   - CMP-G1913-041 and -044 are mainly CRM-contract and data-export disputes.
7. **Minor: the NFG account count is not just "imputed" (V32B-02).** The filed 990 value is also 1 (R1 row applied=0, delta 0). It is unusable either way.

## 3. Findings: P-GAP19-14 (50-state check)

1. **Reproduction and aggregator figures are exact (V32B-23 to -26).**
   - The `build` stage regenerates the CSV byte-for-byte: 38 / 12 / 1, with 59 instrument rows.
   - A live re-query matches the stored figures: totals 70 and 27; state counts HI 4, NY 8, NJ 2, CT 0; control counts CT 16 and IL 3,851.
   - The raw JSON reconciles to 47 state bills plus 23 federal bills.
2. **The NJ correction is right in substance, but cites the wrong act for the DAF clause (V32B-27).**
   - P.L.2018 c.29 (approved 2018-05-30) contains the clause on assets "transferred by the nonprofit charitable entity to a donor-advised fund". The Superior Court may reallocate such assets to the entity acquiring, or operating, an equivalent nonprofit hospital.
   - The same clause is already in **P.L.2014 c.82** (approved 2014-12-26). The 2018 bill (S2247 I1) underlines only the new paragraph labels.
   - The headline, the per-state table and CSV row G095 cite only "P.L.2000 c.143 as amended by P.L.2018 c.29".
   - Finding 2 in the study says "(2014, amended 2018)", which is correct but does not name the act.
3. **The "no mandate" negative holds, with limits (V32B-28).**
   - I re-read 15 official texts and none is a sponsor mandate.
   - A web search for 2025–26 state DAF payout bills found only federal material and Colorado SB26-118. That bill concerns financial institutions paying charitable beneficiary designations, and no DAF wording is reported. Its text was not read, because the bill_files downloads are disallowed by robots.txt.
   - The study's own limits stand: Connecticut is unchecked, recall is 6 of 8, and 36 states rest on one aggregator screen.
   - The classification "N" for the CA and HI platform exclusions is right for the three mandate types tested. The exclusion is conditional, though: a sponsor that names charities to non-advisors falls under the platform law.
4. **Instrument rows are not distinct instruments (V32B-29).**
   - HI HB 992 and SB 1311 each have two rows (2025 and 2026 sessions), and IL HB 4462 is the enactment of 205 ILCS 305/39.
   - So the 37 rows are 34 distinct instruments, and the 11 regulatory exclusions are 8.
5. **Official texts confirm the classifications (V32B-30 to -37).**
   - NC SB 684 and MS SB 2210 include DAFs in "endowed fund" (MS credits stop after 2023).
   - MO HB 1181 and HB 2216 say "(e) Is not a donor advised fund".
   - OH SB 12 lists DAFs in the community-foundation definition.
   - HI Act 205's effective date moved to 2026-07-01 under Act 108 §10.
   - Iowa 15E.305 and N.D.C.C. 57-38 contain no "donor".
   - K.A.R. 92-12-152 denies the credit for DAF gifts, effective 2026-04-17.
   - FPPC Reg. 18424.3 binds officials, operative 2021-12-22.
6. **Dead citations (V32B-41).**
   - All 47 `open.pluralpolicy.com/<st>/bills/...` URLs in the CSV return HTTP 404 today, including the hrefs on Open States' own search page.
   - Statuses can still be re-checked through the search-result rows, and they match (V32B-38).
7. **Unverifiable or snippet-only items (V32B-39, -40).** AK AS 43.23.130(k) is consistent with a search snippet; akleg.gov bars Anthropic agents. The Illinois items cannot be read, because ilga.gov fails TLS verification.
8. **Process note (V32B-44).** The state script sends `User-Agent: daf-landscape-research/1.0`, which discloses the project name to an outside service. Future runs should use a generic client string.

## 4. Queue proposals

- **P-V32B-01:** apply `dup_of` removal in every scope of `mission_complaint_rates_gap19.py`, or add a `distinct_incidents` column, then regenerate the rates CSV with `--force`.
- **P-V32B-02:** add the `country=` tokens to the 27 corpus Benevity Trustpilot records (the review JSON carries `countryCode`), so that the AOGF strict scope screens them too.
- **P-V32B-03:** replace the 47 dead Open States bill URLs in the state CSV with official URLs where the text was read, or with the search URL.
- **P-V32B-04:** make the state script's User-Agent a generic string.

---

## Exact corrections

### `research/mission-2026-11-14/gap19-complaints-with-denominators.md`
1. **Window length (V32B-05).**
   - **Find:** "**Window:** 2021-01-01 to 2026-11-19, which is 5.883 years."
   - **Replace with:** "**Window:** 2021-01-01 to 2026-11-19, which is 5.881 years (2,148 days ÷ 365.25) [V wave 32B]"
2. **Window length, rates list.**
   - **Find:** "- the same divided by 5.883 for a per-year rate;"
   - **Replace with:** "- the same divided by 5.881 for a per-year rate [V wave 32B]"
3. **Window length, denominator notes.**
   - **Find:** "The per-year column divides by 5.883 and assumes a stable account base, which is optimistic for growing sponsors."
   - **Replace with:** "The per-year column divides by 5.881 and assumes a stable account base, which is optimistic for growing sponsors [V wave 32B]"
4. **Window length, data dictionary.**
   - **Find:** "| window_years | number | 5.883, or the aggregate's own window |"
   - **Replace with:** "| window_years | number | 5.881, or the aggregate's own window [V wave 32B]"
5. **AOGF headline: add the strict figure (V32B-07).**
   - **Find:** "   - **AOGF/Benevity:** 56 records. That is **0.78 per 10,000 accounts [0.59–1.01]**, but **28.7 per $1bn of grants [21.7–37.3]**."
   - **Replace with:** "   - **AOGF/Benevity:** 56 records. That is **0.78 per 10,000 accounts [0.59–1.01]**, but **28.7 per $1bn of grants [21.7–37.3]**. The 56 include 9 added reviews from non-US reviewers (Benevity's other programmes). On the strict scope (47 records), the figures are 0.65 per 10,000 [0.48–0.87] and 24.1 per $1bn [17.7–32.0] [V wave 32B]"
6. **Ratio (V32B-07).**
   - **Find:** "   - So per account, Fidelity ranks worse than AOGF; per grant dollar, AOGF is about 13 times worse. Neither ranking is a prevalence estimate (§6)."
   - **Replace with:** "   - So per account, Fidelity ranks worse than AOGF; per grant dollar, AOGF is about 13 times worse on review venues and 11 times worse on the strict scope. Neither ranking is a prevalence estimate (§6) [V wave 32B]"
7. **NFG headline dedup (V32B-08).**
   - **Find:** "   - It shows 40.0 complaints per $1bn [17.3–78.9] on review venues, from 8 records."
   - **Replace with:** "   - It shows 40.0 complaints per $1bn [17.3–78.9] on review venues, from 8 records. One Trustpilot/BBB pair (-037/-040) is a single incident, so the distinct-incident rate is 35.0 per $1bn [14.1–72.2] from 7 [V wave 32B]"
8. **NFG account-count source (V32B-02).**
   - **Find:** "   - DAFRC's FY2024 account count for it is "1" (imputed), so we did not compute a per-account rate."
   - **Replace with:** "   - DAFRC's FY2024 account count for it is "1". DAFRC marks it imputed, and the filed 990 also shows 1, so we did not compute a per-account rate [V wave 32B]"
9. **PPGF row dedup (V32B-09).**
   - **Find:** "| PayPal Charitable Giving Fund | all_venues | 380,644 (filed) | $0.80bn | 5 | 1 | 0.131 [0.043–0.307] | 0.022 | 6.284 [2.040–14.665] |"
   - **Replace with:** "| PayPal Charitable Giving Fund | all_venues | 380,644 (filed) | $0.80bn | 5 rows; 4 distinct (CMP-G1913-046 is dup_of CMP-232) | 1 | 0.131 [0.043–0.307]; distinct 0.105 [0.029–0.269] | 0.022; distinct 0.018 | 6.284 [2.040–14.665]; distinct 5.027 [1.370–12.871] [V wave 32B]"
10. **NFG all_venues row (V32B-08).**
    - **Find:** "| Network for Good (For Good) | all_venues | 1 (implausible) | $0.20bn | 9 | 9 | n/c | n/c | 45.053 [20.601–85.525] |"
    - **Replace with:** "| Network for Good (For Good) | all_venues | 1 (implausible) | $0.20bn | 9 rows; 8 distinct (-040 is dup_of -037) | 9 | n/c | n/c | 45.053 [20.601–85.525]; distinct 40.047 [17.290–78.909] [V wave 32B]"
11. **NFG review_venues row (V32B-08).**
    - **Find:** "| Network for Good (For Good) | review_venues | 1 (implausible) | $0.20bn | 8 | 8 | n/c | n/c | 40.047 [17.290–78.909] |"
    - **Replace with:** "| Network for Good (For Good) | review_venues | 1 (implausible) | $0.20bn | 8 rows; 7 distinct (-040 is dup_of -037) | 8 | n/c | n/c | 40.047 [17.290–78.909]; distinct 35.041 [14.088–72.199] [V wave 32B]"
12. **Pooled processors row (V32B-09).**
    - **Find:** "| Pooled processors | review_venues | n/c | $2.70bn | 67 | 40 | n/c | n/c | 24.791 [19.213–31.484] |"
    - **Replace with:** "| Pooled processors | review_venues | n/c | $2.70bn | 67 rows; 66 distinct | 40 | n/c | n/c | 24.791 [19.213–31.484]; distinct 24.421 [18.887–31.070] [V wave 32B]"
13. **Limits: duplicates.**
    - **Find:** "  - One BBB/Trustpilot pair is the same incident and is counted once in strict."
    - **Replace with:** "  - One BBB/Trustpilot pair is the same incident and is counted once in strict, but twice in review_venues and all_venues. CMP-G1913-046 and CMP-232 (the same Alaska suit) are likewise counted twice in PPGF all_venues [V wave 32B]"
14. **Venue wording (V32B-11).**
    - **Find:** "That came from the App Store, which now supplies 110 of 291 records (37.8%, down from 42.6%)."
    - **Replace with:** "That came from the App Store. App-store records (104 App Store plus 6 Google Play) now make up 110 of 291 records (37.8%, down from 42.6%) [V wave 32B]"

### `research/mission-2026-11-14/gap19-state-law-50-state-check.md`
1. **Headline NJ citation (V32B-27).**
   - **Find:** "Under P.L.2000 c.143 as amended by P.L.2018 c.29, hospital-conversion assets that a charity moved "to a donor-advised fund" and has not spent count as "remaining charitable assets"."
   - **Replace with:** "Under P.L.2000 c.143, hospital-conversion assets that a charity moved "to a donor-advised fund" and has not spent count as "remaining charitable assets". The donor-advised-fund clause was added by P.L.2014 c.82 (approved 2014-12-26) and kept by P.L.2018 c.29 [V wave 32B]"
2. **Per-state table, NJ row.**
   - **Find:** "| NJ | found | 2 / 2 | 1458 | P.L.2000 c.143 as amended by P.L.2018 c.29 (in force): court may reallocate undisbursed conversion assets held in a DAF [F] | pub.njleg.gov PDF |"
   - **Replace with:** "| NJ | found | 2 / 2 | 1458 | P.L.2000 c.143 as amended by P.L.2014 c.82 (which added the DAF clause) and P.L.2018 c.29 (in force): court may reallocate undisbursed conversion assets held in a DAF [F] | pub.njleg.gov PDFs (PL14/82, PL18/29) [V wave 32B]"
3. **Finding 2.**
   - **Find:** "New Jersey's hospital-conversion law (2014, amended 2018) treats undisbursed conversion assets "transferred … to a donor-advised fund" as "remaining charitable assets" that the Superior Court may reallocate to a successor hospital [F; G095]."
   - **Replace with:** "New Jersey's hospital-conversion law (P.L.2000 c.143; the DAF clause was added by P.L.2014 c.82 and kept by P.L.2018 c.29) treats undisbursed conversion assets "transferred … to a donor-advised fund" as "remaining charitable assets". The Superior Court may reallocate them to the entity acquiring or operating an equivalent nonprofit hospital [F; G095] [V wave 32B]"
4. **Instrument count (V32B-29).**
   - **Find:** "3 were not read, and 1 is the narrow NJ asset rule."
   - **Replace with:** "3 were not read, and 1 is the narrow NJ asset rule. The 37 rows are 34 distinct instruments: HI HB 992 and SB 1311 each have a 2025 and a 2026 row, and IL HB 4462 is the enactment of 205 ILCS 305/39. The regulatory exclusions are therefore 8 distinct instruments [V wave 32B]"
5. **Data dictionary, url (V32B-41).**
   - **Find:** "| url | Instrument URL (official where read), or the Open States search URL on state rows |"
   - **Replace with:** "| url | Instrument URL (official where read), or the Open States search URL on state rows. The 47 Open States bill-page URLs returned HTTP 404 on 2026-11-19; their status values come from the Open States search-result rows [V wave 32B]"

### `data/mission-2026-11-14/state-daf-law-50-state-check-2026-11-19.csv`
1. **G095 verification field (V32B-27).** The replacement contains no commas, so the CSV field stays unquoted.
   - **Find:** "official text fetched (pub.njleg.gov PL18/29_.PDF); same text as bill row S2247"
   - **Replace with:** "official text fetched (pub.njleg.gov PL18/29_.PDF); same text as bill row S2247; DAF clause first enacted by P.L.2014 c.82 approved 2014-12-26 (pub.njleg.gov PL14/82_.PDF) [V wave 32B]"

### `scripts/mission_gap19_state_daf_check.py`
1. **Keep the G095 fix on rebuild.**
   - **Find:** "official text fetched (pub.njleg.gov PL18/29_.PDF); same text as bill row S2247"
   - **Replace with:** "official text fetched (pub.njleg.gov PL18/29_.PDF); same text as bill row S2247; DAF clause first enacted by P.L.2014 c.82 approved 2014-12-26 (pub.njleg.gov PL14/82_.PDF) [V wave 32B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection §11.31.** Add "### 11.31 Gap-audit batch part B (validated, wave 32B)", containing the paragraph below, after §11.30 (wave 32A). If §11.31 is already taken, use the next free number.
   - **Find (wave 32A's §11.30 is already in the report as of 2026-11-19, so use this one):** "is the cleaner read (repo [`validation-wave32a-report.md`](mission-2026-11-14/validation-wave32a-report.md)) [V wave 32A]"
   - **Find (fallback, only if §11.30 is absent; inserts after §11.29):** "   >   - Every changed cell has a resolving pointer. Source: [validation-wave31a-report.md](mission-2026-11-14/validation-wave31a-report.md)."
   - **Replace with:** the found text, followed by a blank line, the heading "### 11.31 Gap-audit batch part B (validated, wave 32B)", a blank line and the paragraph below, ending "[V wave 32B]".

New subsection text:

> **Gap-audit batch part B** (validated, wave 32B). Complaint rates were put on FY2024 DAFRC denominators with R1 corrections, using Trustpilot, BBB and Google Play records from 2021 to 2026-11-19. Among the 15 largest sponsors only Fidelity Charitable and RCF (one low-attribution review of its administrator, Ren) have any such record, so zero counts mean "not observed". Fidelity shows 27 review-venue complaints: 1.32 per 10,000 accounts [95% CI 0.87–1.92], or 2.13 per $1bn of grants. AOGF (Benevity) shows 0.78 per 10,000 accounts but 28.7 per $1bn, or 24.1 on US-only reviewers, so the ranking turns on the denominator. Processor complaints describe payout rules: paper-check thresholds, lost checks and EFT vetting. A 51-jurisdiction bill search found no 2021–2026 state payout, account-reporting or donor-intent mandate on DAF sponsors; Connecticut could not be checked. Most state DAF wording is tax treatment. New Jersey's hospital-conversion law, whose DAF clause dates from P.L.2014 c.82, lets a court reallocate unspent conversion assets held in a DAF (repo [`validation-wave32b-report.md`](mission-2026-11-14/validation-wave32b-report.md)) [V wave 32B]
