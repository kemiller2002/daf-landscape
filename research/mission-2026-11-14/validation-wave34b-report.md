# Validation wave 34B: recipient basis and rating eligibility; long-tail fee census

**Date:** 2026-11-19 · **Validator:** independent-validation-agent-wave34b · **Register:** [`data/mission-2026-11-14/validation-register-wave34b.csv`](../../data/mission-2026-11-14/validation-register-wave34b.csv) (38 claims, V34B-01 to V34B-38)

**Studies checked**
- Study 1 (V34B-01 to 19): [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md), its two CSVs and `scripts/mission_recipient_basis_eligibility.py`.
- Study 2 (V34B-20 to 38): [b45n33-01-long-tail-fee-census.md](b45n33-01-long-tail-fee-census.md), `long-tail-fee-census-2026-11-19.csv` and `scripts/mission_long_tail_fee_census.py`.

**Method.** Both scripts were re-run. Primary pages were re-fetched after reading each host's robots.txt, with one generic user agent (`validation-script/1.0`) used throughout and never changed. Fee engines, Wilson intervals, sampling and allocation were reimplemented independently. A sensitivity script imports the study module unchanged. No outreach and no login. crt.sh, certspotter and sec.gov were not used. Scratch: `/tmp/claude-0/-home-user/ed3d1503-0f0d-5a0d-a5e2-85e6e3196309/scratchpad/v34b/`.

## Counts

| | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| Study 1: recipient basis and CN eligibility | 19 | 13 | 4 | 2 | 0 |
| Study 2: long-tail fee census | 19 | 14 | 5 | 0 | 0 |
| **Total** | **38** | **27** | **9** | **2** | **0** |

## Findings

### Study 1: recipient basis and rating eligibility

**What holds**
- **Reproduction (V34B-01).** The script re-run to scratch (`--out-a`, `--out-b`) gives CSVs byte-identical to the repo copies, and every total in §1.1 reproduces.
- **IRS text (V34B-02, 03).** The line 1f text on DAF grants is verbatim in the 2025 Instructions for Form 990 (page updated 30-Apr-2026; robots.txt allows `/instructions/`).
  - **1b and 1c belong in the private basis.** Line 1b is dues "that represent contributions from the public rather than payments for benefits". Line 1c is only the contribution part of event payments (above retail value), and gaming goes to 1f. Both are contributions by definition and mostly individual.
  - **"1h − 1d − 1e" is a sound, if loose, proxy for private giving.** The identity holds in every in-scope 990.
- **Headline shares (V34B-04, 05, 07).** The line mix, the headline medians and pooled shares with their intervals, and the size-band shares all match the CSV.
- **XML spot-check (V34B-06).** Eight recipients (16 returns, including IRC and one EZ year) match the XML exactly on every Part VIII line.
- **CN rules (V34B-09, 10).** The CN rule quotes are verbatim (dated April 9, 2026).
  - **No revenue threshold.** None appears in six CN pages: the rating-system article, two nonprofit-FAQ articles, the methodology page, the release notes and the Spring 2026 update. Revenue is used only for size classes and metric counts.
  - The Guide PDF still returns 404.
- **Eligibility results (V34B-13, 18, 19).** The headline 76.9% ($56.93bn of $74.07bn; 89,124 of 174,220 units), the variants, the expense diagnostic and the sector and band tables all reproduce.

**What needs correcting**
1. **Not-in-BMF recipients are not mainly "revoked or inactive" (V34B-14, contradicted).** By Schedule I name, the largest are four CZ LLCs on Silicon Valley Community Foundation lines:
   - CZ Institute for Advanced Biological Imaging, $563.9m;
   - CZ Biohub SF LLC, $554.3m;
   - CZ Biohub New York LLC, $238.6m;
   - CZ Biohub Chicago LLC, $237.2m.

   Together they hold $1.59bn, 38% of not-in-BMF dollars. Next come governmental units (UT Austin, Penn State, Washoe County School District) and religious bodies. Only 3 of the 22,269 EINs are in Pub 78. CN "automatically lists all 501(c)(3) nonprofits included in the IRS Business Master File", so the ineligible verdict stands. The label, and the "likely new or recently re-listed" reading, do not.
2. **"About half" of ineligible dollars going to churches is wrong (V34B-16, contradicted).** Church-status recipients take $6.18bn of the $17.15bn that fails, 36% (8.3 of 23.1 points): about a third.
3. **Three-return rule (V34B-11).** CN's methodology page says "three years of IRS Form 990 filings (990EZ, 990N, 990PF does not qualify)". That is stricter than the help article, which the study follows by counting EZ and PF returns. On the strict reading, the eligible share is **76.5%** ($56.70bn; 86,482 recipients), against 76.9%.
4. **Chariot size match (V34B-08).** About $97m of giving per participant-year implies revenue at or above $97m. So the ≥$100m BMF-revenue band (5.8–8.7%) is the closer size match than $25–100m, and against it Chariot's 12.6% is above the range. The pooled 12.6% is also dollar-weighted towards the largest participants, and the periods differ (2021–25 against FY2023–24).
5. **Minor points.**
   - Navigation is about half (49.5%) of the fewer-than-three-returns category, not "most" (V34B-17).
   - Two nonprofit-FAQ articles of the same date write "consolidated subsidiaries", which partly defines the term the study calls undefined (V34B-12).
   - 53 of 2,170 respondents (3.4% weighted) have b3 shares above 100%, among them APHL at 132%. The study does not report this (V34B-06).
- **Churches (V34B-15).** The treatment is right: FOUNDATION 10 with no e-filed return is ineligible, and 996 church-status organisations that do e-file are counted eligible. The category is church-status organisations, many of them ministries (Cru, Wycliffe, Salvation Army), not only congregations.

### Study 2: long-tail fee census

**What holds**
- **Reproduction (V34B-20).** `--out` is not supported, so the repo CSV was backed up, the census task re-run, and the repo copy restored (md5 unchanged). The output CSV and all Appendix tables are byte-identical.
- **Sampling (V34B-21 to 23).** The frame (1,240), strata, floor-1 largest-remainder allocation and seeded draw (20261119 + stratum index) all reproduce independently.
- **Schedules (V34B-25 to 31).** Re-fetched within robots rules and confirmed: Hutchinson, Pikes Peak, Homer, Athens, ATC, Cal Poly Pomona, and CF West Texas (pre-2021, "Revised 12/01/16"). Rates, minimum fees, opening minimums and dates match.
  - Homer's DAF is "permanently endowed" in Appendix 1, but the rate is the same for non-endowed DAFs.
  - Hutchinson's PDF has no date inside it; "2023" appears only in the file name.
- **Whatcom (V34B-24, partially confirmed).** The Terms & Conditions PDF ("Last Updated: 12/31/2025"; DAF $5,000) re-fetched. The fee page now returns a bot-verification page, so the 2.00/1.50/1.25/1.00 scale was confirmed from the study's cache only.
- **Arithmetic (V34B-32, 33, 38).** Effective fees at $25k, $100k and $500k, the medians and IQRs, every Wilson interval checked, the T7 coverage ratios and the $138m arithmetic all reproduce.

**What needs correcting**
1. **One "no published fee" call is wrong (V34B-36).** Eight randomly chosen `no_published_fee` sponsors were tested. Seven hold:
   - BSA Foundation;
   - UM Foundation of Louisiana;
   - UF Foundation;
   - Central Florida Foundation;
   - Mackinac Island CF;
   - Greenwood County CF;
   - Cape Coral CF, now a redirect to charitablecommunity.org, a site with no fund pages.

   **Columbus Medical Association Foundation does not hold.** Its page lists donor-advised funds and says funds open "with a minimum gift of $10,000" and "All named funds are assessed a quarterly administration fee, based on the size of the fund." That makes it `partial` under the study's own definition. The corrected counts are:
   - any fee term: **16/60 = 26.7% (17.1–39.0%)**;
   - "other" type: 2/8;
   - band t0_1: 4/18;
   - read with no fee: 33.
2. **The top-100 "any fee term" comparison is not like-for-like (V34B-34).** The top-100 count (52) leaves out 7 `no_rates_published` rows, for example Boston's fee schedule "available upon request" and Greater Salina's reference to a separate schedule. The tail rules would count these (GlobalTrust is `partial`; Eastern Shore and Muscatine are `published_unread`). Matched, the top-100 figure is **59/100 (49.2–68.1%)**. The 2021+ schedule comparison (34/100) and the fee medians (118/100/100 bps) are unaffected.
3. **The opening-minimum comparison mixes populations (V34B-35).** The top-100 $15,000 covers the 34 schedule publishers only. On the same basis as the tail (every row stating a minimum), the top-100 median is **$10,000 (n=26)**. The direction holds; the gap is about half as large.
4. **"Robots-blocked" is a user-agent refusal, not a robots disallow (V34B-37).** For the five CF hosts, robots.txt read with the validator's agent returns 200, either "User-agent: * Disallow:" or only /wp-admin/ disallowed. It returns 403 to `research-script/1.0`. Williams and Wheaton return 403 to both agents. Keeping all seven as unknown is right, and the validator did not crawl them. The label and §1.4 definition need fixing.

**Not applied as exact corrections (follow-up)**
- **CMAF in the script.** `FEES["200385860"]` in `scripts/mission_long_tail_fee_census.py` should become `partial` (opening minimum 10000, quotes as above), with the page added to the cache. Until then the CSV and Appendix tables T2, T3 and T6 show the pre-correction count. A note is added to the Appendix below.
- **Strict three-return variant.** `scripts/mission_recipient_basis_eligibility.py` could add the strict reading as a fourth `rule_variant`. The figure (76.5%) is supplied here from the validator's sensitivity run.

## Exact corrections

Apply in order. Each Find occurs exactly once in its file as it stands on 2026-11-19 (checked by script; see the end). In a Find or Replace, `\n` stands for a newline.

### `research/mission-2026-11-14/b40n1202-b43n26-recipient-basis-and-rating-eligibility.md`

1. **§0 Chariot: size match** (V34B-08).
   - **Find:** "So unscaled, the filings sit just below Chariot. Scaled, they sit above it. The two numerators differ (top-50 Schedule I against CRM-coded gifts from all sponsors), so neither reading is like-for-like."
   - **Replace with:** "So unscaled, the filings sit just below Chariot. Scaled, they sit above it. The two numerators differ (top-50 Schedule I against CRM-coded gifts from all sponsors), so neither reading is like-for-like. Size matching is loose too: about $97m of giving per participant-year implies revenue at or above $97m, so the ≥$100m band (5.8% unscaled, 8.7% scaled), where Chariot's 12.6% is above the range, is the closer match. The periods also differ (2021–25 against FY2023–24) [V wave 34B]"
2. **§0 (B): not-in-BMF line** (V34B-14).
   - **Find:** "  - EINs not in the IRS BMF: 5.6%;"
   - **Replace with:** "  - EINs not in the IRS BMF: 5.6%, mostly CZ Biohub LLCs and governmental units rather than revoked charities [V wave 34B];"
3. **§0 (B): Navigation share** (V34B-17).
   - **Find:** "of which Navigation Charitable Fund's $1.26bn is most;"
   - **Replace with:** "of which Navigation Charitable Fund's $1.26bn is about half (49.5%) [V wave 34B];"
4. **§1.3: other CN pages and the stricter methodology wording** (V34B-10, V34B-11).
   - **Find:** "No revenue floor appears in any of the three CN pages read."
   - **Replace with:** "No revenue floor appears in any of the three CN pages read. None appears either in CN's methodology page (charitynavigator.org/about-us/our-methodology/ratings/) or in its nonprofit-FAQ articles "Getting My Nonprofit Listed and Rated" and "Understanding the Encompass Rating" (both dated 2026-04-09). The methodology page is stricter on filings than the help article: "a charity must have three years of IRS Form 990 filings (990EZ, 990N, 990PF does not qualify)". The nonprofit FAQs say "consolidated subsidiaries" where the donor FAQ says "nonprofit subsidiaries", and add that CN "automatically lists all 501(c)(3) nonprofits included in the IRS Business Master File (BMF)" [V wave 34B]"
5. **§1.3 rule table: what "not in the BMF" holds** (V34B-14).
   - **Find:** "| Revoked or inactive | Not in the BMF"
   - **Replace with:** "| Revoked or inactive | Not in the BMF; in practice mostly subsidiary LLCs and governmental units, not revoked charities (§4.1) [V wave 34B]"
6. **§4.1 variants: strict three-return reading** (V34B-11).
   - **Find:** "- six-year window by IRS processing year: 76.9% (89,160 recipients)."
   - **Replace with:** "- six-year window by IRS processing year: 76.9% (89,160 recipients).\n- only full Form 990s counted towards the three-return rule, as CN's methodology page reads ("990EZ, 990N, 990PF does not qualify"): 76.5% ($56.70bn; 86,482 recipients). 2,642 central-eligible recipients ($0.23bn) have fewer than three full 990s in the window [V wave 34B]"
7. **§4.1 diagnostics: who is not in the BMF** (V34B-14).
   - **Find:** "These are likely new or recently re-listed organisations [I], so the upper bound on eligibility is about 77.3% [I]."
   - **Replace with:** "These may be new or recently re-listed organisations [I], so the upper bound on eligibility is about 77.3% [I]. Most not-in-BMF dollars are not of this kind. They are subsidiary LLCs and governmental units: CZ Biohub SF, New York and Chicago LLCs and the CZ Institute for Advanced Biological Imaging ($1.59bn together, 38% of not-in-BMF dollars), the University of Texas at Austin, Penn State and the Washoe County School District. Only 3 of the 22,269 EINs are in Pub 78 [V wave 34B]"
8. **§4.1 largest ineligible: name the two EINs** (V34B-14).
   - **Find:** "  - Two EINs not in the BMF, $0.56bn each"
   - **Replace with:** "  - Two EINs not in the BMF, $0.56bn each: CZ Institute for Advanced Biological Imaging and CZ Biohub SF LLC, both named on Silicon Valley Community Foundation lines [V wave 34B]"
9. **§4.2 reading: what eligibility turns on** (V34B-14).
   - **Find:** "- **Eligibility is mostly a church and new-organisation question, not a size question.**"
   - **Replace with:** "- **Eligibility is mostly a question of church status, subsidiary or government-unit status and organisation age, not of size [V wave 34B]**"
10. **§4.2 reading: churches' share of ineligible dollars** (V34B-16).
    - **Find:** "and about half of those dollars go to churches."
    - **Replace with:** "and about a third of those dollars (8.3 of 23.1 points) go to church-status organisations with no e-filed 990 [V wave 34B]."
11. **§5 limit 2: shares above 100%** (V34B-06).
    - **Find:** "2. **(A) 990-EZ filers.** Their line 1 includes government grants and is used unchanged on every basis."
    - **Replace with:** "2. **(A) 990-EZ filers.** Their line 1 includes government grants and is used unchanged on every basis. Separately, 53 of 2,170 respondents (3.4% weighted) have a b3 share above 100%. One is the Association of Public Health Laboratories at 132%, with $334,788 on line 1f against $238m on 1e. This points to timing or DAF-weighting mismatches at heavily government-funded recipients [V wave 34B]"
12. **§5 limit 8: BMF stand-in** (V34B-14).
    - **Find:** "8. **(B) The BMF stands in for \"revoked or inactive\".** EINs not in the BMF are treated as ineligible. 1,213 of them, holding $0.29bn, pass the filing rules."
    - **Replace with:** "8. **(B) The BMF stands in for \"revoked or inactive\".** EINs not in the BMF are treated as ineligible, which matches CN listing only BMF organisations. Most of their dollars go to subsidiary LLCs and governmental units, not to revoked charities. 1,213 of them, holding $0.29bn, pass the filing rules [V wave 34B]"

In item 12, `\"` stands for a literal straight double quote.

### `research/mission-2026-11-14/b45n33-01-long-tail-fee-census.md`

1. **§0 publication row: any fee term** (V34B-36).
   - **Find:** "**Counting any published fee term** (a rate, an opening minimum, a linked schedule, or an unquantified fee): **15/60 (25.0%; 15.8–37.2%)**"
   - **Replace with:** "**Counting any published fee term** (a rate, an opening minimum, a linked schedule, or an unquantified fee): **16/60 (26.7%; 17.1–39.0%)**, with Columbus Medical Association Foundation reclassified from `no_published_fee` to `partial`: a $10,000 minimum and a quarterly administration fee \"based on the size of the fund\" [V wave 34B]"
2. **§0 size row** (V34B-36).
   - **Find:** "Any fee term: 7/14, 5/24, 3/18, 0/4 [C]"
   - **Replace with:** "Any fee term: 7/14, 5/24, 4/18, 0/4 [C; V wave 34B]"
3. **§0 top-100 row: opening minimums** (V34B-35).
   - **Find:** "Tail opening minimums are lower (median $5,000 vs $15,000) [C]"
   - **Replace with:** "Tail opening minimums are lower: median $5,000 against $10,000 for top-100 CFs on the same basis (every CF stating a minimum, n=26). The $15,000 figure is the top-100 schedule publishers only (n=19) [C; V wave 34B]"
4. **§1.4 status table: robots_blocked definition** (V34B-37).
   - **Find:** "| `robots_blocked` | robots.txt 403: nothing could be read"
   - **Replace with:** "| `robots_blocked` | robots.txt request refused with HTTP 403 to `research-script/1.0`, so nothing could be read. For 5 of the 7 hosts, robots.txt itself allows all agents [V wave 34B]"
5. **§2.1 table: all sampled** (V34B-36).
   - **Find:** "| All sampled | 60 | **7 (11.7%; 5.8–22.2%)** | **15 (25.0%; 15.8–37.2%)**"
   - **Replace with:** "| All sampled | 60 | **7 (11.7%; 5.8–22.2%)** | **16 (26.7%; 17.1–39.0%)** [V wave 34B]"
6. **§2.1 table: other** (V34B-36).
   - **Find:** "| Other (university/hospital, nationals, processors) | 8 | 1 (12.5%) | 1 (12.5%)"
   - **Replace with:** "| Other (university/hospital, nationals, processors) | 8 | 1 (12.5%) | 2 (25.0%) [V wave 34B]"
7. **§2.1: no-fee count** (V34B-36).
   - **Find:** "- **[C] 34 of 60 sites were read and contain no DAF fee at all.**"
   - **Replace with:** "- **[C] 33 of 60 sites were read and contain no DAF fee at all [V wave 34B]**"
8. **§2.1: robots-blocked hosts** (V34B-37).
   - **Find:** "A further 7 hosts block robots (Wichita Falls, Clinton County OH, West Kentucky, Greene County PA, Clarinda, Williams College, Wheaton College), and 4 sponsors have no website."
   - **Replace with:** "A further 7 hosts refused the study's user agent with HTTP 403 (Wichita Falls, Clinton County OH, West Kentucky, Greene County PA, Clarinda, Williams College, Wheaton College), and 4 sponsors have no website. Read with another generic agent, robots.txt on the five CF hosts allows all agents (\"User-agent: * Disallow:\" or only /wp-admin/). The 403 is a server response to `research-script/1.0`, not a robots disallow. Williams and Wheaton return 403 to both agents. All seven stay unknown [V wave 34B]"
9. **§2.1: non-CF sponsors and DAF terms** (V34B-36).
   - **Find:** "- **[I] Outside CFs, a DAF is an accommodation, not a product.** Single-issue, faith and university sponsors in the sample do not market DAFs with terms."
   - **Replace with:** "- **[I] Outside CFs, a DAF is mostly an accommodation, not a product.** Single-issue, faith and university sponsors in the sample rarely market DAFs with terms. The exceptions are Cal Poly Pomona and Columbus Medical Association Foundation, whose fund page lists donor-advised funds with a $10,000 minimum and a quarterly fee \"based on the size of the fund\" (cmafohio.org/create-a-personalized-charitable-fund) [V wave 34B]"
10. **§2.4 table: any fee term, matched definition** (V34B-34).
    - **Find:** "| Any fee term or schedule | 12/31 = 38.7% (23.7–56.2%) | 52/100 = 52.0% (42.3–61.5%)"
    - **Replace with:** "| Any fee term or schedule | 12/31 = 38.7% (23.7–56.2%) | 52/100 = 52.0% (42.3–61.5%); 59/100 = 59.0% (49.2–68.1%) counting the 7 `no_rates_published` rows (e.g. Boston \"available upon request\", Greater Salina's separate schedule), as the tail rules would [V wave 34B]"
11. **§2.4 table: opening minimum** (V34B-35).
    - **Find:** "| Opening minimum | $5,000 (n=11) | $15,000 (n=19)"
    - **Replace with:** "| Opening minimum | $5,000 (n=11) | $15,000 (n=19, schedule publishers only); $10,000 (n=26, every row stating one) [V wave 34B]"
12. **§5 source register: Whatcom re-fetch** (V34B-24).
    - **Find:** "https://whatcomcf.org/financial-oversight/investment-approach-fees/ | Schedule, gift fee, investment notes"
    - **Replace with:** "https://whatcomcf.org/financial-oversight/investment-approach-fees/ | Schedule, gift fee, investment notes. A wave 34B re-fetch on 2026-11-19 returned a bot-verification page, so the values are confirmed from the cached copy only [V wave 34B]"
13. **Appendix: pre-correction note** (V34B-36).
    - **Find:** "## Appendix: script output (`--task census`)"
    - **Replace with:** "## Appendix: script output (`--task census`)\n\n> These tables predate the wave 34B reclassification of Columbus Medical Association Foundation (EIN 200385860) to `partial`. T2, T3 and T6 still count it as `no_published_fee` until `FEES` in the script is updated [V wave 34B]"

In these items, `\"` stands for a literal straight double quote.

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

1. **New §11.35** (V34B-05, 08, 11, 13–16, 34, 36). Insert after §11.34, before the source register.
   - **Find:** "\n---\n\n## Source register"
   - **Replace with:** "\n\n### 11.35 Recipient basis, ratings and tail fees (validated, wave 34B)\n\n<the paragraph below, beginning `> **Recipient basis, ratings and tail fees**`> [V wave 34B]\n\n---\n\n## Source register"
   - *(The paragraph already ends with the tag. Do not add a second one.)*

New subsection text:

### 11.35 Recipient basis, ratings and tail fees (validated, wave 34B)

> **Recipient basis, ratings and tail fees** (validated, wave 34B). The IRS assigns DAF grants to Form 990 line 1f. On a denominator of lines 1a + 1b + 1c + 1f (contributions less government grants and related-organisation transfers), top-50 DAF grants are a median 7.7% and a pooled 10.3% of sampled recipients' contributions, against 5.9% and 6.9% on line 1h; eight recipients' lines match their XML exactly. Chariot's 12.6% lies above the ≥$100m band (5.8–8.7% unscaled to scaled), the closer size match. Of $74.07bn of top-50 FY2023–24 DAF-weighted grants, 76.9% reach recipients that pass every Charity Navigator rule filings can test, or 76.5% if only full 990s count towards the three-return rule. CN publishes no revenue threshold. Church-status organisations without e-filed returns take 8.3% of dollars. EINs absent from the BMF take 5.6%; they are mostly governmental units and CZ Biohub LLCs, not revoked charities. Among 60 sampled sponsors under $50m, 7 (11.7%; Wilson 5.8–22.2%) publish a 2021-or-later admin rate and 16 (26.7%) some fee term. On six schedules, tail CFs charge a median 150 bps at $100k, against 100 bps at top-100 CFs (repo [`validation-wave34b-report.md`](mission-2026-11-14/validation-wave34b-report.md)) [V wave 34B]

## Check script

`/tmp/claude-0/-home-user/ed3d1503-0f0d-5a0d-a5e2-85e6e3196309/scratchpad/v34b/gen/check_finds.py` parses this section and counts each Find (with `\n` and `\"` decoded) in its file. Every Find occurs exactly once, and every Replace ends with `[V wave 34B]` or `[C; V wave 34B]`, or holds the tag inside it. The §11.35 paragraph is 189 words.
