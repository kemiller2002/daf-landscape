# Validation wave 44A: charity-data terms for AI uses; Chariot size match

**Validator:** validator wave 44A · **Date:** 2026-11-20
**Register:** [`data/mission-2026-11-14/validation-register-wave44a.csv`](../../data/mission-2026-11-14/validation-register-wave44a.csv) (26 rows, V44A-01 to V44A-26)

**Studies validated**
1. Charity-data terms for AI uses: [b43n26-03-charity-data-terms-ai.md](b43n26-03-charity-data-terms-ai.md), `data/mission-2026-11-14/charity-data-terms-ai-matrix-2026-11-20.csv`, `scripts/mission_b43n26_03_terms_matrix.py`.
2. Chariot size match: [b40n1202-b43n26-02-chariot-size-match.md](b40n1202-b43n26-02-chariot-size-match.md), `data/mission-2026-11-14/chariot-size-match-2026-11-20.csv`, `scripts/mission_chariot_size_match.py`.

## Method

- **Terms study.**
  - Re-ran the matrix script with `.` as root.
  - Re-fetched 21 URLs with a stdlib fetcher (user agent `research-script/1.0`), checking robots.txt with `urllib.robotparser` before each fetch. A 401, 403 or 429 robots response counted as disallowed.
  - Checked every CSV `clause_quote`, and every quoted fragment in `notes`, against the fetched text after whitespace and quote-mark normalisation.
  - Read the clauses around each quote to test the coding.
  - Robots results, 2026-11-20:
    - candid.org: robots 403, not fetched.
    - www.every.org: robots 429, not fetched.
    - irs.gov TEOS search path: disallowed, not fetched.
    - Allowed and fetched: www.charitynavigator.org, developer.charitynavigator.org, developer.candid.org, go.benevity.com, goodstack.io, www.pledge.to, docs.every.org, www.irs.gov (BMF page), www.govinfo.gov.
    - No robots file (404): developer.pledge.to.
    - www.givechariot.com: robots 200, allowed.
  - No user-agent changes, logins or forms.
- **Chariot study.**
  - Re-ran the script from the existing scratchpad caches with `--out` pointed at a scratch file, so nothing in the repo was written.
  - Compared the output md5 and recomputed every quoted figure from the CSV.
  - Re-implemented the bootstrap in a scratch script that imports the module. With the same seed it reproduces the study's interval; holding the certainty stratum fixed tests the design.
  - Re-fetched the Chariot webinar page once.

## Counts by study and result

| Study | Claims | confirmed | partially confirmed | contradicted | unverifiable |
|---|---|---|---|---|---|
| Charity-data terms for AI (V44A-01 to 15) | 15 | 10 | 5 | 0 | 0 |
| Chariot size match (V44A-16 to 26) | 11 | 6 | 4 | 1 | 0 |
| **Total** | **26** | **16** | **9** | **1** | **0** |

Two sub-points sit inside partially confirmed rows and could not be settled:
- the Every.org Authentication-page quote (“inappropriate usage”), because that page returned 404;
- the 2026 Candid licence wording, because candid.org returned 403.

## Findings

### 1. Charity-data terms for AI uses

1. **The script reproduces.** It returns 28 rows and 0 validation errors. The 24 commercial cells split permitted 1, prohibited 5, requires-licence 6 and silent 12. Eleven cells have an express clause, and one (Candid (b)) has AI-specific wording.
2. **Charity Navigator: all four cells confirmed** against the API Terms page ("Last updated October 2026").
   - (a) Display is licensed only "on the Licensee Site", free, for personal non-commercial use. The licence is non-sublicensable. s.2(b) bars any use "not expressly permitted", and s.2(b)(v) bars service-bureau use.
   - (c) s.1(d) permits caching of "ratings data" for site speed, with no time limit.
   - (d) s.6(c)(ii) requires deletion, "except as otherwise required by applicable law".
   - (b) The ratings ban binds through s.4(a), which incorporates the "Attribution Requirements".
3. **Where the ratings ban sits.** The study's precision note on strategic-synthesis l.543 is overstated.
   - The API Terms page itself prints an "Attribution Requirements" section after s.12(g). It contains the exact CSV sentence: "Please remember, our ratings may not be used in any other calculation or manipulated."
   - The developer attribution page that the CSV cites words it differently ("Our ratings may not be used …"). That page is dated "Last modified on November 17, 2026", not undated.
   - So l.543 ("API licence … bars using ratings 'in any other calculation'") is accurate in substance and needs no correction. Nor do l.556, l.612, report l.869 or direction-charity-ratings-integrations l.78–79, l.221 and l.271. Only the study's own §5.3 and §2.1 wording changes.
4. **Candid.**
   - The AI/ML sentence is verbatim in the developer-portal copy of the License Agreement (APIs) ("Last updated December 2023"; portal updatedAt 2026-09-07). It is absent from the portal TOS.
   - It qualifies a mining ban for three purposes: a non-internal database, resale, and a competing service. §2.2 says so. The §0 headline drops the qualifier, which this wave corrects.
   - The (a), (c) and (d) clauses and "Powered by Candid" are confirmed in the portal copies.
   - The 2026 candid.org licence stays blocked (robots 403). Its rows are treated as blocked, and the repo's 2026 wording "for use in or through the use of artificial intelligence" cannot be checked.
   - Evidence status is inconsistent: Candid (b)–(d) are marked `read` although the governing 2026 text was not read.
5. **Benevity and Goodstack quotes are all verbatim.** Neither has AI or caching wording.
   - Goodstack (d) is an inference from an IP clause and a return-of-property clause, yet it is coded `express_clause=yes`. On the study's own definition the express count is 10, not 11.
6. **Pledge.**
   - The API terms are non-public. The table-of-contents link is inside an HTML comment, and `/terms-services` and `/terms-services-non-public` both return 404.
   - The MCP reference lists `lookup_organization`, `create_nonprofit_fundraiser` and `create_donation`, plus account, crowdfund, webhook and utility tools.
   - The guide pitches the server at "AI coding assistants" working on a partner account. That is integration tooling, which qualifies the comparison with donor-facing agent tools.
7. **"Silent" is used for two different things.** In 8 of the 12 silent cells (all of Every.org and Pledge) the governing terms were blocked or are not public, so those cells are not determinable. Only 4 cells (Goodstack and Benevity, uses (b) and (c)) are silent in terms that were read. The §6 limits say this, but the §0 table and the tally do not. No cell is over-read toward permission.
   - The headline "no public term permits any of the four uses without conditions", outside CN caching, stands.
   - The headline phrase "Every commercial licence that speaks to display ties it to the licensee's own site or app" stands too.
8. **Robots disclosure.**
   - **Honest and harmless.** No content came from the 403 or 429 hosts.
   - **Count error.** The note says "three requests" but lists two plus two, which is four.
   - **Not reproducible.** The fetcher lives in a session scratchpad, so the log cannot be re-run.
   - **Rule context.** RFC 9309 treats a 4xx robots response other than 429 as "unavailable", which permits crawling. A 429 should be treated as unreachable. The corrected rule is stricter than the RFC and matches repo practice.
9. **IRS baseline confirmed.** 17 U.S.C. 105 is quoted verbatim, and the BMF page shows "11/10/2026" and "1,984,891". The TEOS search path is robots-disallowed.

### 2. Chariot size match

1. **Reproduction.**
   - The cache-only re-run took 4 min 11 s. Its md5 is `fc2ad5b7ca54b8f47b561251a006f08d`, byte-identical to the repo CSV, with 407 rows.
   - The all-recipient central figures reproduce: 9.16% on 1h and 13.71% on 1h − 1d − 1e.
2. **Band.**
   - $26.1bn ÷ 54 ÷ 5 = $96.7m. $3.3bn ÷ $26.1bn = 12.64%. Chariot's page prints "nearly 13%", so 12.6% is derived.
   - The page says neither that the $26.1bn spans five years nor that the panel is balanced. Read as one year, the total is $483m per participant.
3. **Headline confirmed.**
   - Pooled 10.04% (8.23–12.06%); median 5.85% (3.42–6.76%); 1h 8.11%.
   - 220 respondents, 115 of them certainty units; 358.35 weighted.
   - BMF $25–100m: 13.75% (531 respondents). BMF $50–200m: 11.42% (458).
   - Excluding intermediaries: 7.96% (159).
   - Dropping The 85 Fund: 9.58%.
   - Expanded frame: 9.85%.
4. **Why The 85 Fund shows 106.6%.** Its two-year 1h − 1d − 1e is $311.58m.
   - Top-50 DAF-weighted Schedule I grants alone come to $311.83m (100.1%). The central allocation adds 6.5%, giving $332.13m.
   - The numerator comes from sponsors' returns for their own fiscal years and the denominator from the recipient's returns, so a per-recipient share is not bounded at 100%. A share near or above 100% marks a recipient funded almost wholly by DAFs; it is not an arithmetic error.
   - Capping every share at 100% moves the pooled figure from 10.04% to 10.01%.
   - The 10 recipients above 50% hold 17.2% of the weighted numerator and 2.3% of the weighted denominator.
5. **Contradicted.** The study says "Every contribution-based band containing the $96.7m mean gives 9.9–10.2%". In fact:
   - $25–100m contains the mean and gives 12.9% (11.3–14.8%);
   - the open-ended ≥$50m band gives 8.5%.

   The true statement is narrower: the bounded bands centred near the mean give 9.9–10.2%.
6. **Is "below Chariot" robust?** The direction is; the size of the gap is not.
   - **Direction holds.**
     - Every contribution band from $48m up gives 7.3–10.2%, and so does the expanded frame.
     - A shorter average panel only raises the per-participant mean: $120.8m at 4 years, $161.1m at 3 years and $483m as a one-year total. That moves the match toward bands with lower shares (≥$200m: 7.3%).
     - Only a participant mix concentrated in $25–100m would reach Chariot's level.
   - **Size of the gap is not settled.**
     - The 0.6–4.4 point interval covers recipient sampling only.
     - It excludes the numerator allocation, which the envelope covers only partly.
     - It excludes the CRM-versus-Schedule I definitions: sub-$5,000 gifts, gifts that DAFpay routes, and booking timing.
     - It excludes the period difference (2021–25 pooled against FY2023–24). Because DAF shares rose over the period, that difference probably widens the gap.
7. **Bootstrap design.**
   - Resampling each stratum and then applying the domain is correct for a domain estimate. The validator's re-implementation reproduces 8.23–12.06%.
   - However, it also resamples the 400-unit certainty stratum, which is a census. Holding those units fixed gives 8.85–11.49%, so the published interval is conservative.
   - The sponsor-side numerator and the allocation keys are not resampled, so the interval understates total uncertainty.
   - Weights are held fixed. The percentile indexing is fine.
8. **Named participants** match the CSV: ACLU Foundation 35.3% ($176.6m a year) and Share Our Strength 18.1% ($78.9m a year). The study's 35.2% and 18.0% are truncated rather than rounded. As the study says, two organisations are an illustration only.
9. **Repo text.**
   - b40n1202-b43n26 §0 l.31, the §3 table and Reading l.215 still carry the BMF-band bracketing.
   - b40n12 l.190 says 9.2% and 13.7% "bracket" 12.6%. These are figures on two bases, and only 1h − 1d − 1e matches Chariot's basis.
   - FINAL-STATUS l.102 and strategic-synthesis l.100 give 9.2% and 13.7% without the size-matched figure.
   - The industry report's l.1000 and l.1013 are wave 33A and 34B §11 paragraphs and are left alone; a new §11.63 records the result. The report body (§§1–10) does not set the filing shares beside Chariot.

## Accept / modify / reject

| # | Proposed change (source) | Decision | Reason |
|---|---|---|---|
| 1 | Use the terms matrix as a separate rights lens, not an overlay flag (b43n26-03 §5.2) | Accept | Consistent with §7 overlay scope |
| 2 | Y1 sub-check for downstream AI reuse rights in A5 (P-B43N26-03-05) | Accept | Gap is real. Score changes stay with the two-scorer rule |
| 3 | Candid AI clause and store ban support Y1 3 → 2 (b43n26-03 §5.1) | Accept as evidence only | No score change in this wave |
| 4 | Precision note on strategic-synthesis l.543 (b43n26-03 §5.3) | Reject | The ban is printed on the API Terms page under the s.4(a) Attribution Requirements; l.543 is accurate. The study's note is corrected instead |
| 5 | Add Pledge MCP to the AI product census with a product-level reading (b43n26-03 §5.2, §5.3) | Modify | Add it, noting that it is partner-account tooling for AI coding assistants; controls not yet read |
| 6 | Matrix tally, "silent 12" (b43n26-03 §0) | Modify | Split into 4 silent and 8 not determinable; express clauses 10 if Goodstack (d) is excluded |
| 7 | Headline "Candid needs written consent before its data are mined for AI" (b43n26-03 §0) | Modify | Add the three-purpose qualifier next to the headline |
| 8 | Replace the BMF-band size match in b40n1202-b43n26 §0/§3 with contribution-matched 10.0% (b40n1202-b43n26-02 §5) | Modify | Adopt, adding that the direction is robust but the interval is sampling-only |
| 9 | New conclusion "Chariot's 12.6% is above the size-matched filing estimate by about 2.6 points (0.6–4.4)" (§5) | Modify | Call 0.6–4.4 a sampling interval and name the period and definition differences |
| 10 | Proposed wording "…not with denominator choice or size" (§0) | Modify | Add the period difference; say size matching does not close the gap rather than that size is ruled out |
| 11 | Keep 9.2% / 13.7% unchanged, but do not set them beside Chariot (§5) | Accept | Corrections to FINAL-STATUS, strategic-synthesis and b40n12 add the size-matched figure |
| 12 | NPB038 median reading confirmed by the 5.8% size-matched median (§5) | Accept | Recomputed 5.85% (3.42–6.76%) |
| 13 | "Every contribution band containing the mean gives 9.9–10.2%" (§3.2) | Reject as stated | $25–100m (12.9%) and ≥$50m (8.5%) contain the mean |

## Limits

- candid.org (403) and www.every.org (429) were not read, by rule. Their cells stay as the study coded them, with the caveats above.
- Legal readings (MCP output as distribution, ranking features as calculation) are interpretations, not legal advice.
- The Chariot comparison rests on the same unverified participant-size distribution as the study.

## Exact corrections

### `research/mission-2026-11-14/b40n1202-b43n26-recipient-basis-and-rating-eligibility.md`

**Find:** "Size matching is loose too: about $97m of giving per participant-year implies revenue at or above $97m, so the ≥$100m band (5.8% unscaled, 8.7% scaled), where Chariot's 12.6% is above the range, is the closer match."
**Replace with:** "Size matching on BMF revenue was loose. Matched instead on each recipient’s own 1h − 1d − 1e (average $50–200m a year, around Chariot’s $96.7m per participant-year if all 54 participants report five years), the central numerator gives a pooled 10.0% (sampling CI 8.2–12.1%) and a median 5.8%, so the filings sit about 2.6 points below Chariot’s 12.6%, not around it. The direction holds in every contribution band from $48m up (7.3–10.2%), so it survives a shorter average panel; only the $25–100m band (12.9%) reaches Chariot. The size of the gap is not settled: the interval covers recipient sampling only, not the numerator allocation, the CRM-versus-Schedule I definitions or the period difference ([b40n1202-b43n26-02-chariot-size-match.md](b40n1202-b43n26-02-chariot-size-match.md)). [V wave 44A]"

**Find:** "Size-matched (~$97m giving per participant-year [I]): $25–100m 11.0% / 16.4% [I]; ≥$100m 5.8% / 8.7% [I]"
**Replace with:** "Size-matched on BMF revenue (~$97m giving per participant-year [I]): $25–100m 11.0% / 16.4% [I]; ≥$100m 5.8% / 8.7% [I]. Size-matched on own 1h − 1d − 1e of $50–200m a year, central numerator: 10.0% (8.2–12.1%), median 5.8% [F] [V wave 44A]"

**Find:** "Chariot's 12.6% sits inside the unscaled-to-scaled range for the $25–100m band and for all recipients, and above the ≥$100m range."
**Replace with:** "On BMF-revenue bands, Chariot’s 12.6% sat inside the unscaled-to-scaled range for the $25–100m band and for all recipients, and above the ≥$100m range. Matched on recipients’ own contributions, the central filing share (10.0%) is about 2.6 points below Chariot; that interval (0.6–4.4) is sampling-only. The all-recipient 13.7% is not a like-for-like comparison (b40n1202-b43n26-02). [V wave 44A]"

**Find:** "At the median and for ≥$100m recipients the filings still give materially lower shares."
**Replace with:** "At the median, for ≥$100m recipients and for recipients size-matched on their own contributions (10.0% pooled, 5.8% median, central numerator), the filings still give lower shares than Chariot. [V wave 44A]"

### `research/mission-2026-11-14/b40n1202-b43n26-02-chariot-size-match.md`

**Find:** "Every contribution-based band containing the $96.7m mean gives a pooled share of 9.9–10.2%, below 12.6%. Only a band reaching down to $25m reaches Chariot's level."
**Replace with:** "Every bounded contribution band centred near the $96.7m mean ($50–200m, $75–125m, $48.3–193.3m) gives a pooled share of 9.9–10.2%, below 12.6%. Open-ended bands from $48m up give 7.3–8.5%. The $25–100m band, which also contains the mean, gives 12.9% (11.3–14.8%) and is the only one to reach Chariot’s level. [V wave 44A]"

**Find:** "so the interval for the share (8.2–12.1%) **excludes** 12.6%, though only just."
**Replace with:** "so the interval for the share (8.2–12.1%) **excludes** 12.6%, though only just. The interval reflects recipient sampling only. It resamples the 400-unit certainty stratum as if it were a sample, which widens it (holding certainty units fixed gives 8.9–11.5%), and it carries no numerator-allocation, definition or period uncertainty. [V wave 44A]"

**Find:** "plausibly because of timing or booking differences [I]."
**Replace with:** "plausibly because of timing or booking differences [I]. Top-50 Schedule I grants alone, DAF-weighted, equal 100.1% of its two-year 1h − 1d − 1e ($311.8m against $311.6m), and the central allocation adds 6.5% on top. The numerator comes from sponsors’ returns for their own fiscal years and the denominator from the recipient’s, so a per-recipient share is not bounded at 100%. Capping every share at 100% moves the pooled figure from 10.04% to 10.01%. [V wave 44A]"

**Find:** "is consistent with selection of DAFpay-using participants or with numerator definition, not with denominator choice or size."
**Replace with:** "is consistent with selection of DAFpay-using participants, with numerator definition or with the period difference; denominator choice does not explain it, and size matching on contributions does not close it. The 0.6–4.4 range is a sampling interval only. [V wave 44A]"

**Find:** "  - The participant panel is balanced; the page does not say so."
**Replace with:** "  - The $26.1bn spans all five years and the participant panel is balanced; the page says neither. Read as one year, it is $483m per participant, where the ≥$200m band gives 7.3%, further below Chariot. [V wave 44A]"

### `research/mission-2026-11-14/b43n26-03-charity-data-terms-ai.md`

**Find:** "(two to candid.org, two of the three to www.every.org) all returned 403 or 429, so no content was obtained from those hosts."
**Replace with:** "(two to candid.org and two of the three to www.every.org, so four requests, not three) all returned 403 or 429, so no content was obtained from those hosts. The fetcher is not in the repo, so the log cannot be re-run; a 2026-11-20 re-check found the same robots statuses (candid.org 403, www.every.org 429). [V wave 44A]"

**Find:** "**Confirmed, with a precision note.** The sentence is in the *Attribution Guidelines*, which Terms s.4(a) makes binding. It is not in the licence body."
**Replace with:** "**Confirmed.** The sentence is in the Attribution Requirements, which Terms s.4(a) makes binding. The API Terms page itself prints those requirements after s.12, with the sentence in the same words, so l.543 needs no correction. [V wave 44A]"

**Find:** "- [Attribution Guidelines](https://developer.charitynavigator.org/attribution) (undated)."
**Replace with:** "- [Attribution Guidelines](https://developer.charitynavigator.org/attribution) (“Last modified on November 17, 2026”). This page reads “Our ratings may not be used in any other calculation or manipulated.” The “Please remember, …” wording quoted below is the copy printed in the Attribution Requirements section of the API Terms page. [V wave 44A]"

**Find:** "Script output for the 24 commercial cells: permitted 1, prohibited 5, requires-licence 6, silent 12. Express clauses back 11 of the 24."
**Replace with:** "Script output for the 24 commercial cells: permitted 1, prohibited 5, requires-licence 6, silent 12. Of the 12 silent cells, 8 (all of Every.org and Pledge) mean not determinable, because the governing terms were blocked or are not public; only 4 (Goodstack and Benevity (b) and (c)) are silent in terms that were read. Express clauses back 11 of the 24, or 10 if Goodstack (d), an inference, is not counted. [V wave 44A]"

**Find:** "- **Raw ratings.** An AI DAF product cannot treat third-party *ratings* as free model inputs."
**Replace with:** "- **Raw ratings.** An AI DAF product cannot treat third-party *ratings* as free model inputs. Candid’s AI wording, quoted below, qualifies a ban on mining to build a non-internal database, to resell or to compete; it is not a stand-alone AI ban (§2.2). [V wave 44A]"

### `research/mission-2026-11-14/b40n12-daf-share-of-recipient-revenue.md`

**Find:** "the figures are 9.2% (1h) and 13.7% (1h − 1d − 1e), which still bracket 12.6% (b40n120201-01) [V wave 41B]"
**Replace with:** "the figures are 9.2% (1h) and 13.7% (1h − 1d − 1e) (b40n120201-01) [V wave 41B]. They are on different bases and cover all recipients, so they do not bracket Chariot’s 12.6% like for like. On the matching basis (1h − 1d − 1e), size-matched on own contributions of $50–200m a year, the central share is 10.0% (8.2–12.1%), below Chariot (b40n1202-b43n26-02) [V wave 44A]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

**Find:** "Central estimate 9.2% of line 1h and 13.7% of 1h−1d−1e. The assumption range is 8.8–9.4% and 13.2–14.1%."
**Replace with:** "Central estimate 9.2% of line 1h and 13.7% of 1h−1d−1e. The assumption range is 8.8–9.4% and 13.2–14.1%. These are all-recipient figures, not a like-for-like match to Chariot’s 12.6%. Size-matched on recipients’ own 1h−1d−1e ($50–200m a year), the central share is 10.0% (sampling CI 8.2–12.1%), median 5.8%, about 2.6 points below Chariot; period and numerator differences are unquantified (b40n1202-b43n26-02). [V wave 44A]"

### `research/mission-2026-11-14/strategic-synthesis.md`

**Find:** "and the sampling CI 8.3–10.2% and 12.3–15.2% ([b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md)) [V wave 41B]"
**Replace with:** "and the sampling CI 8.3–10.2% and 12.3–15.2% ([b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md)) [V wave 41B]. Size-matched to Chariot’s participants on their own 1h − 1d − 1e ($50–200m a year), the central share is 10.0% (8.2–12.1%), about 2.6 points below Chariot’s 12.6%; the all-recipient 13.7% is not a like-for-like comparison ([b40n1202-b43n26-02-chariot-size-match.md](b40n1202-b43n26-02-chariot-size-match.md)). [V wave 44A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.63 Charity-data terms for AI use; Chariot size match (validated, wave 44A)\n\n**Charity-data terms for AI use; Chariot size match** (validated, wave 44A). Re-fetched public terms confirm the matrix’s cells for Charity Navigator, Candid’s portal copies, Benevity, Goodstack and Pledge. Charity Navigator lets licensees cache ratings for site speed with no time limit, ties display to the licensee’s own free site and requires deletion on termination. Through Attribution Requirements printed on its API Terms page and made binding by s.4(a), it bars using ratings “in any other calculation”. Candid’s December 2023 API licence requires written consent for data mining “for use in artificial intelligence”, as a qualifier on mining for a non-internal database, resale or a competing service. Eight of the twelve “silent” cells (Every.org, Pledge) mean not determinable, because the terms were blocked or are not public. A byte-identical cache-only re-run confirms that recipients matched on their own 1h − 1d − 1e of $50–200m a year give a central pooled DAF share of 10.0% (8.2–12.1%), median 5.8%, below Chariot’s derived 12.6%. The direction holds in every band from $48m up. The interval covers sampling only (repo [`validation-wave44a-report.md`](mission-2026-11-14/validation-wave44a-report.md)) [V wave 44A]\n\n---\n\n## Source register"
