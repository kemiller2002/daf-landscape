# Validation wave 10: independent check of V10-01 to V10-10

**Validator:** independent-validation-agent-wave10 · **Validated on:** 2026-11-15 (brief dated 2026-11-14) · **Register:** [`data/mission-2026-11-14/validation-register-wave10.csv`](../../data/mission-2026-11-14/validation-register-wave10.csv) (24 rows)

**Method.** For each claim I went to primary sources first: vendor and foundation pages, the GKCCF audit, SEC EDGAR filings and full-text search, IRS e-file XML, and fee pages and PDFs. I only read the three queue documents after reaching a verdict, to compare. I re-ran `scripts/mission_all_in_cost.py`. I re-ran `scripts/mission_bdc_loans.py` from a scratch copy, offline, using the session's cached EDGAR hits and documents, with outputs sent to scratch so no repo data file was overwritten. There was no outreach, no login and no form submission. Evidence is 2021 or later. Two pre-2021 items appear only to date something: the NRS acquisition (2016–17) and an MS GIFT clause effective 2021-07-21.

## Verdicts

| ID | Verdict | Key point |
|---|---|---|
| V10-01 | **Confirmed** (all three CFs) | **CFNEF:** the Redpath story page is dated 2024-03-25 in its JSON-LD. **Maine CF:** the Fund 360 case study names it. **Arizona CF:** a copy of the Sage/Clark Nuber case study is dated 2024-03-06 and names "Blackbaud FIMS". The repo's "Accounting Seed" for Maine is not supported. |
| V10-02 | **Confirmed, with nuance** | The "Manufacturer is Fusion Laboratories LLC / dba NPact" sentence is in NPact's SaaS Standard Terms (2025-08-26), not its Terms of Use. The Terms of Use say "Fusion Laboratories dba NPact, a Delaware corporation", so NPact's own documents disagree on LLC vs corporation. |
| V10-03 | **Confirmed** | 2023 audit: income from services **$1,915,649** (2022: $3,035,924). This covers back-office accounting for other nonprofits **and** pool administration fees. The privacy policy (September 2024) lists donor-portal.org. The apex page uses the GKCCF favicon and a gkccf Wufoo form. Indian River CF still links an `ircf.donor-portal.org` tenant. |
| V10-04 | **Confirmed** | nrstpa.com: "wholly owned subsidiary of Community Financial System, Inc. (NYSE: CBU)". CBU's 2025 annual report shows the chain BPAS → NRS → Global Trust Company. |
| V10-05 | **Confirmed for 5 of 6 rows, label error on the sixth; inputs check out, with two caveats** | Re-run output is byte-identical. Typical-pool bps at $250k: Daffy 25.6, Vanguard 62, Fidelity 115, DAFgiving360 125, NCF 145, **San Francisco Foundation** 213. The claim as relayed says "SVCF", but the repo correctly says SFF. Fidelity 60% pool is 0.55% net (0.58% gross) against 0.015% for the index pool. The NPT PDF was created 2026-10-15. MS GIFT's 1.00% cap excludes legacy pools (up to 1.24%) and Select UMA manager fees. TIFIN's 1% cap is confirmed. Edward Jones' 0.70% rests only on a search-index capture of now-404 Ren pages. That same capture gives admin tiers of 0.60/0.35/0.25, which contradicts the script's assumed 0.60/0.30/0.20. |
| V10-06 | **Confirmed** | Help centre: "A donor's login credentials are passed through to each DAF provider". The token method is "in use by DAFgiving360 and community foundations using the Foundant platform". Notes dated 2026-05-31 and 2026-09-18. Chariot's developer docs offer the OAuth route to any provider, so "only" describes what the help centre names, not a technical limit. |
| V10-07 | **Confirmed** | Timeline: "April 6, 2026 – The new AEF platform officially launches". The Export step on the platform-resources page sits inside DonorCentral how-tos that link to `aef.donorcentral.com`. That host is still live (HTTP 200, Blackbaud SKY UX) and is still linked from AEF's Donors menu. |
| V10-08 | **Golub part confirmed. New Mountain part confirmed but incomplete; repo range wrong. Absence claim confirmed. Script reproducible.** | **GBDC 10-Q at 2024-12-31:** par 92,893+7,599+3,957+256 = $104,705k, with fair value equal to par. The 2025-03-31 10-Q shows only the 2024-09-30 comparative. **NMFC at 2026-09-30:** 16,719/17,017 = 98.25%. **Other holders of the same 2032 facility:** FS KKR (~99.5%) and others. **KKR Enhanced US Direct Lending Fund-L at 2026-06-30:** columns are "Par/Shares, Fair Value". TL 30,474 / 29,776 and DDTL 3,319 / 3,243 give **97.71%**, below New Mountain. This breaks the repo's "98.25–99.5%" range and its "New Mountain marks lowest". **Re-run:** 1,252 deduplicated rows and 304 latest-mark rows, both CSVs byte-identical. |
| V10-09 | **Confirmed (Indian River, Winston-Salem, Acadiana-as-inference). Arkansas confirmed with nuance. Flint plausible but weakly dated.** | **Winston-Salem:** the /portal page itself says "As of July 15, 2024", so the year is stated on the page and need not be inferred from the 990. **Arkansas:** 2026-06-01 is the date the instruction email went out, not a stated go-live. **Flint:** the only date is the CMS publication date of the login page (2026-01-20). |
| V10-10 | **Confirmed** | **FY2025 XML:** total revenue 16,344,032; contributions 16,343,906; grants 6,942,359; 3 DAFs holding 10,772,483 at year-end. "Goodstack-affiliated" in the claim conflicts with the repo's governing wording ("not subsidiaries or affiliates"). |

## Points that change confidence or wording

1. **BDC 2032 range (V10-08).** The repo says "13 BDCs hold the 2032 facility at 98.25–99.5% of par. New Mountain marks lowest". KKR Enhanced's latest schedule (2026-06-30) marks the term loan and delayed-draw tranches at 97.71%. The repo's own latest-marks CSV keeps these rows as `possible_unfunded_commitment` with "not computed". The filing's column header is "Par/Shares | Fair Value". The funded TL row (footnote (b) only) gives 29,776 / 30,474 = 97.71%. Read across periods, the range is **97.7–99.5%**. At 2026-09-30 alone, New Mountain is the lowest among the lenders parsed.
2. **Edward Jones admin tiers (V10-05).** The script assumes RCF breakpoints, 0.60/0.30/0.20/0.15. A search-index capture of Ren's EJ client resource guide shows 0.60% (first $500k), 0.35% (next $500k) and 0.25% (next $1m), with totals of 1.30% / 1.05% / 0.95% including the 0.70% program fee. The $25k and $250k results are unaffected. If the 0.25% tier extends to $2.5m, admin at $2.5m is about 34 bps against the modelled 30. Confidence stays low because the page is 404.
3. **MS GIFT cap (V10-05).** OCR of circular page 15 reads: "Effective on or about July 21, 2021 – The Maximum Morgan Stanley Advisory fee for Accounts is 1.00%, except for Accounts in MS GIFT Legacy Pools". Legacy pools run from 0.60% to 1.24%. In the Select UMA program, third-party SMA fees are added on top. So "1.37% with adviser" is a floor for Select UMA accounts, not a ceiling.
4. **Winston-Salem year (V10-09).** The year is stated on the source page itself ("As of July 15, 2024 …" on the same /portal page). Upgrade the date basis from [I] to [F].
5. **Arizona CF date (V10-01).** The case study is dated 2024-03-06 on the top10erp.org copy, so it is no longer "undated".
6. **Goodstack wording (V10-10).** Write "Goodstack-linked" or "Goodstack-serviced US foundation", not "Goodstack-affiliated". This keeps faith with the wave-7 wording.
7. **SVCF vs SFF (V10-05).** The 2.13% row is San Francisco Foundation. Anyone relaying this result must not call it Silicon Valley Community Foundation.

## Exact corrections

### `research/mission-2026-11-14/queue-bdc-coverage-migrations-goodstack.md`

- **§1 finding 2 (line 34).** Replace "**With these funds, 13 BDCs hold the 2032 facility at 98.25–99.5% of par.** New Mountain marks lowest, FS KKR highest (99.47%)." with: "**With these funds, 13 BDCs hold the 2032 facility at 97.7–99.5% of par.** At 2026-09-30, New Mountain marks lowest of the parsed lenders and FS KKR highest (99.47%). KKR Enhanced US Direct Lending Fund-L's latest schedule (2026-06-30, columns 'Par/Shares | Fair Value') marks the term loan at 29,776/30,474 = 97.71%."
- **Latest-marks table (line 122), KKR Enhanced row.** Replace "not computed (layout parsed as `possible_unfunded_commitment`; TL $30,474k par / $29,776k FV in `row_cells_raw`)" with "97.71 (TL 30,474 par / 29,776 FV; DDTL 03/25 3,319 / 3,243; revolver and DDTL 10/25 partly unfunded, footnote (c)); parser still types the rows `possible_unfunded_commitment`".
- **§3.1 inference list (line 153).** Replace "- **Winston-Salem:** the first Foundant 990 line." with "- **Winston-Salem:** none needed; the /portal page states 'As of July 15, 2024' (the 990 line corroborates)."
- **§3.2 Winston-Salem row (line 170).** Replace "**2024-09-30** [I]" with "**2024-09-30** [F]". Replace "No year is stated; it is set by the first Foundant 990 line" with "The same page states 'As of July 15, 2024, everyone will need to complete the registration process' for the Grants Portal, which fixes the year; corroborated by the first Foundant 990 line". Change the confidence from medium to high.
- **§3.2 Arkansas row.** After "were emailed on June 1", add: "(the instruction-email date, used as the event date; no go-live date is stated)".
- **§3.4 (line 191).** Replace "Three dates rest on stated inference rules: Acadiana (weekday), Winston-Salem (990 year) and Tampa Bay (pending-transition notice)." with "Two dates rest on stated inference rules: Acadiana (weekday) and Tampa Bay (pending-transition notice). Flint's date is a CMS page date only."
- **§4 heading and any summary that uses "affiliated".** Keep "Goodstack Impact Foundation US (Percent Impact Foundation, EIN 87-3165286)". Wherever a summary calls it "Goodstack-affiliated", replace that with "Goodstack-linked (service-provider relationship; not a subsidiary or affiliate)".

### `research/mission-2026-11-14/queue-ledgers-behind-portals.md`

- **Line 16.** Replace "Foundation Partners' Fund 360, a fund-accounting layer on Salesforce and Accounting Seed [V + F 990]" with "Foundation Partners' Fund 360, a fund-accounting package 'built entirely within Salesforce' [V + F 990]; Accounting Seed underneath is not stated for Maine [I]".
- **Line 85, ledger cell.** Replace "**Fund 360 (Foundation Partners) on Salesforce / Accounting Seed**" with "**Fund 360 (Foundation Partners) on Salesforce** (Accounting Seed not confirmed for Maine)". Replace the evidence link `fdnpartners.com/products` with, or add, [MaineCF success story](https://fdnpartners.com/maine-community-foundation-success-story).
- **Line 81, CFNEF citation.** Replace `https://redpathcg.com/about/case-studies` with `https://redpathcg.com/story/the-community-foundation-for-northeast-florida/`. Replace "(Mar 2024)" with "(datePublished 2024-03-25)".
- **Line 94, Arizona CF.** Replace "undated, live 2026" with "dated 2024-03-06 on the [top10erp.org copy](https://www.top10erp.org/case-study-library/sage-intactt-arizona-community-foundation)". In source row L8 (line 196), replace "undated, live" with "2024-03-06 (top10erp copy)".
- **Line 20, NPact.** After the Standard Terms quote, add: "The Terms of Use (modified 2025-08-05) instead call the company 'Fusion Laboratories dba NPact, a Delaware corporation', so NPact's documents disagree on entity form."
- **Line 30, GKCCF audit.** Replace "books 'back-office accounting services' revenue." with "books income from services, which covers back-office accounting services for other nonprofits and administrative fees on pool investments by other entities."
- **Line 180 limitations.** Replace "Arizona CF's go-live date is not stated." with "Arizona CF's go-live date is not stated (the case study itself is dated 2024-03-06)."

### `research/mission-2026-11-14/queue-all-in-cost-dafpay-access.md`

- **Line 24, adviser-layer bullet.** After "Published caps are 1.00% at MS GIFT, DAFgiving360 and TIFIN Give/GiveClear.", add: "MS GIFT's cap excludes Legacy Pools (0.60–1.24%) and, under Select UMA, third-party SMA manager fees, which are charged on top."
- **Line 65, MS GIFT row, adviser cell.** Replace "max 1.00% ([F](…))" with "max 1.00% from 2021-07-21, excl. Legacy Pools and SMA fees ([F](…))".
- **Line 133–135, Edward Jones.** Replace "Breakpoints are **assumed** equal to RCF donor-directed." with "Breakpoints are **assumed** equal to RCF donor-directed (0.60/0.30/0.20/0.15). A search-index capture of Ren's EJ client resource guide (article 10810347, now 404) shows administrator tiers of 0.60% / 0.35% / 0.25% (first $500k / next $500k / next $1m) and totals of 1.30% / 1.05% / 0.95%. If those apply, EJ admin at $2.5m is about 34 bps, not 30. Rows at $25k and $250k are unchanged."
- **Line 62, Edward Jones row.** Change the $2.5m admin cell from "0.30" to "0.30 (0.34 if captured tiers apply)".

### `scripts/mission_all_in_cost.py`

- **`edward_jones` sponsor (line 222).** Either keep the assumed tiers and add the captured alternative to `assumptions`, or change them to `((0, 500_000, 0.60), (500_000, 1_000_000, 0.35), (1_000_000, 2_500_000, 0.25), (2_500_000, INF, 0.15))`. If changed, add a second `Src` for `https://intercom.help/rengiving/en/articles/10810347-edward-jones-charitable-gift-fund` with status `search_index_capture`. Keep the confidence "low".

### `data/mission-2026-11-14/cf-vendor-migrations-2022-2026.csv`

- **Winston-Salem `event` row.** Change `date_basis` from its inferred value to a first-party basis, citing wsfoundation.org/portal ("As of July 15, 2024 …"). Set `date_confidence` to high.
- **Winston-Salem `evidence` rows.** Add a WS-PORTAL-YEAR row for https://www.wsfoundation.org/portal with the snippet "As of July 15, 2024, everyone will need to complete the registration process".

## Not re-verified

- **DAFgiving360's "not to exceed 1%" adviser cap.** dafgiving360.org returns 403 and I did not re-read the 2024 FPA deck. The repo cites a search-index capture plus the 2024 deck.
- **Flint's exact cut-over date.** The only date found is the CMS publication date of the login page.
- **Ren as a borrower name.** "Ren" is too generic for EDGAR full-text search. "Renaissance Philanthropy", "Fundraise Up" and "Foundant" return no BDC hits, and "Benevity" returns only non-BDC filers.
