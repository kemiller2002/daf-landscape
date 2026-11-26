# Validation wave 32A: gap-audit batch part A (exception-load proxy, startup cohort)

**Date:** 2026-11-19. **Validator:** independent-validation-agent-wave32a.
**Register:** [`validation-register-wave32a.csv`](../../data/mission-2026-11-14/validation-register-wave32a.csv), rows V32A-01 to V32A-47. V32A-01–22 cover the exception-load proxy and V32A-23–47 cover the startup cohort.

**Documents validated:**
- [gap19-exception-load-proxy.md](gap19-exception-load-proxy.md) (P-GAP19-05), with `exception-load-proxy-2026-11-19.csv` and `scripts/mission_exception_load.py`.
- [gap19-startup-cohort.md](gap19-startup-cohort.md) (P-GAP19-15), with `daf-startup-cohort-2021-2026.csv` and `scripts/mission_gap19_startup_cohort.py`.

**Method:**
- **Own view first.** I re-ran both scripts and recomputed the headline figures from the outputs and the Schedule I line cache before reading either note's conclusions. All outputs went to scratch (`scratchpad/v32a/`).
- **Primary sources.** I checked the statute text on LII (26 U.S.C. §4966 and §170). I checked the BMF field guide (`eo-info.pdf`). I read the ProPublica Nonprofit Explorer API for 14 EINs, one e-file XML on the GivingTuesday mirror, and 17 company, app-store and press pages. Fidelity Charitable's 2025 Giving Report was also read.
- **robots.txt.** I read robots.txt on every host before fetching from it, and LII's 10-second crawl delay was kept.
  - **Skipped:** `www.clickondetroit.com` disallows ClaudeBot, so the AP/Causeway page was not fetched.
  - **Blocked:** `www.morningstar.com` and `www.grapevine.org` returned 403. For those two I used web-search extracts and labelled them as such.
- **Not used:** crt.sh, certspotter and sec.gov. There was no outreach. All evidence is from 2021 or later. The one exception is Uncommon Giving's 2020 release, which the cohort note itself relies on and which is used here only to test the window rule.

## Headline

**Of 47 claims, 29 are confirmed, 12 partially confirmed and 6 contradicted. None is unverifiable.**

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| P-GAP19-05 exception-load proxy | 22 | 13 | 5 | 4 | 0 |
| P-GAP19-15 startup cohort | 25 | 16 | 7 | 2 | 0 |
| **Total** | **47** | **29** | **12** | **6** | **0** |

**Both scripts reproduce exactly:**
- `mission_exception_load.py` ran in 33 s, and its CSV is identical to the repository file after sorting.
- `mission_gap19_startup_cohort.py` prints the §4 tables exactly and reports `Frame A consistency: OK`.

## Findings: exception-load proxy (P-GAP19-05)

### What holds
- **Denominators and category arithmetic.** Recomputing from the 94 itemised `sponsor_year` rows reproduces every pooled share to six decimals, as computed (V32A-05 to V32A-07).
- **Count-versus-dollar story.** Fiscal-sponsor lines are 10.7× more dollar-heavy than average, PF/ER lines 3.5× and foreign lines 3.3×. The not-in-Pub-78 pool is count-heavy (0.48×) because of church and group-subordinate lines.
- **Big-4 nationals.** The like-for-like 3.6% stands (1.96% + 1.50% + 0.15%). So do core 7.3%/10.0% and broad 28.3%/17.8%, and operating-foundation dollars of $948.6m (V32A-12 to V32A-14). Greater Horizons is not among the four, so none of these changes.
- **Community foundations.** The pooled gap is +11.4 pp against a median of −1.2 pp (V32A-10).
- **Legal reasoning on private foundations (V32A-15 to V32A-17).** The statute supports the split:
  - §4966(c)(2)(A) exempts distributions to §170(b)(1)(A) organisations other than disqualified supporting organisations.
  - §170(b)(1)(A)(vii) covers "a private foundation described in subparagraph (F)", and (F)(i) is the private operating foundation. Operating foundations therefore need no expenditure responsibility (ER).
  - Non-operating PFs, and Type III supporting organisations that are not functionally integrated (§4966(d)(4)(A)(i)), do need ER under §4945(h).
  - The BMF codes are mapped correctly: 02/03 are operating foundations, 04 is a non-operating PF and 24 is Type III not functionally integrated.
- **Spot figures.** These all check against the line cache and summary JSON (V32A-18 to V32A-22):
  - the SVCF Further Future line ($1,309.0m, ruling 2023-03);
  - the BM-A Institute line ($83.1m, ruling 2024-09, after NPT's June 2024 year-end);
  - the fiscal-sponsor totals ($1,211,634,404; generic markers add $55,100);
  - the Schedule F count-basis mix;
  - Fidelity's 2,664,446 grants in 2024.

### What fails

1. **A totals row is counted as a $212.2m grant (V32A-03, -04).**
   - Greater Horizons' FY2024 Schedule I (object 202513189349309621) has two blank lines:
     - one of $212,187,406, which is **exactly** the sum of its 3,282 named lines;
     - one of $3,282, which is the line count.
   - This is a totals row, not a recipient. The note instead calls it "a line with no name and no EIN" and builds three claims on it:
     - Greater Horizons' 59.8% sponsor share;
     - the maximum of the sponsor distribution;
     - part of the "unexplained" pool.
   - A scan of all 94 returns finds no other instance.
   - **Corrected, pooled:**
     - denominator 608,610 lines and $92.72bn;
     - broad 25.08% / **19.72%**;
     - core 7.41% / **10.96%** (gap +3.55 pp, 1.48×);
     - unexplained non-list recipients $0.89bn (0.96%), not $1.10bn (1.19%);
     - ex SVCF and university/hospital, core 7.2% / 9.6%;
     - FY2024 core 7.36% / 9.73%.
   - **Corrected, Greater Horizons:** 25.1% / 19.8% broad and 7.2% / 9.5% core.
   - The headline reading "about 7% of lines and 10–11% of dollars" survives.
   - The same line cache feeds P-NEW-REC-01, so its $91.02bn base carries the same artefact. P-NEW-REC-01 is outside this wave and was not corrected here.
2. **Servant Foundation is counted twice in the sponsor-type table (V32A-08).**
   - The §3.2 "National 16 (31)" row and the National rows of both category tables use `dafrc_segment` values, which include Servant Foundation. The Faith row also includes Servant, so the table covers 49 sponsors against 48.
   - The correct `sponsor_type` national row is 15 sponsors (29 sponsor-years), 466,753 lines and $62.50bn. Its shares are broad 26.47% / 17.83% and core 7.02% / 10.18%.
3. **The lowest sponsor outside university/hospital is Dechomai, not Ayco (V32A-09).**
   - Dechomai is 5.6%, and the CSV's own `all_ex_university_hospital` minimum (0.055982) shows it. Ayco (7.9%) comes next.
4. **The CSV has 167 rows, not 166 (V32A-02).** The note's own list of row types sums to 167.

### Interpretation challenges (not errors)
- **The ER-required set is both too wide and too narrow.**
  - *Too wide:* §170(b)(1)(F)(ii) conduit and (F)(iii) common-fund foundations are also (A)(vii) organisations, so not every PF-coded recipient needs ER.
  - *Too wide:* Founders Pledge ($53.9m) is code 04 on the BMF but PC on Pub 78, and Rev. Proc. 2018-32 lets a sponsor rely on Pub 78. Without it the ER-required total is about $86.7m.
  - *Too narrow:* donor-controlled Type I, Type II and functionally integrated Type III supporting organisations are also disqualified (§4966(d)(4)(A)(ii)), but the screen does not catch them.
  - *Too narrow:* Pub 78 `SOUNK` recipients are not flagged.
  - *Too narrow:* the 286 foreign individual grants at Stanford are grants to natural persons. Made from a DAF, they would be taxable distributions under §4966(c)(1)(A).
- **"Covers about a third" mixes bases.** It sets a sum of shares on different denominators (3.6%) against a union (10.0%). The three omitted categories listed (2.05%, 4.25% and 0.98%) overlap, so they do not add up to the 6.4 pp difference.
- **The CF count-share claim needs a scope.** "Community foundations have the highest foreign count share" holds among the national, CF and faith types only. The university/hospital pair is at 56.2% (V32A-11).

## Findings: startup cohort (P-GAP19-15)

### What holds
- **Counts and intervals.** All counts, Wilson intervals, exposure (80.9 company-years) and the rule-of-three bounds (3.7% full cohort, 8.7% strict subset) recompute exactly (V32A-24 to V32A-27).
- **Frame A.** The 11 Frame A hits re-derive mechanically from the panel (V32A-28). The DAFRC base-rate comparison also holds: 23 sponsor-years, 0.28 expected exits, P(0) = 0.76 (V32A-30).
- **Spot-checks.** 12 of 18 members were checked against live primary pages or filings (V32A-35 to V32A-44). All statuses, dates and figures hold:
  - Daffy: listing dated to 2026-11-18;
  - Groundswell: seller Groundswell Giving Inc., listing dated to 2026-09-28;
  - Chariot: YC shows "Active", team 24, S2022; DAFpay listing to 2026-09-11; gift-processing post dated Jan 28, 2026;
  - Causeway: PR Newswire, Sep 12, 2024, "acquired by Charity Navigator in 2023";
  - Infinite Giving: $2M seed on 2024-10-01; blog posts to 2026-11-18;
  - GivingIQ: EasyDAF launched April 30, 2026;
  - Abundance, Matbia and Daffodil: copyright 2026;
  - Givepact: live but undated;
  - iMaaser: last dated 2025-08-27; assets $319;
  - Goodstack: TY2025 XML shows 3 DAFs and $10,772,483;
  - AnonDo $17,982 and GivingTrax $78,774.
- **Cross-tabs.** The survivor and funding cross-tabs are consistent with the CSV (V32A-47).

### What fails or needs qualification
1. **Uncommon Giving fails the pre-registered window rule (V32A-31).**
   - The rule's test is the unit's *first observable entry event*. The sponsor itself (EIN 84-3815117) has a FY2020 DAFRC row with 266 DAF accounts ($890,600, filed). Its 2020-07-28 release offers "an Uncommon Giving Wallet, a DAF, with as little as $10".
   - It is in only because the sponsor's IRS ruling month reads 2021-01. Endaoment (ruled 2020-05) is out.
   - Without it, the cohort is 17: active 10, acquired 1, unknown 6 and **pivoted 0**. The lower bound becomes 11/17 = 64.7% (41.3–82.7%).
   - The cohort's only pivot, cited as "the most visible non-death outcome", is therefore a pre-window entrant.
2. **The "incumbent" exclusion is not defined (V32A-32).**
   - Telescope Fund is excluded. It is a dedicated sponsor ruled in the window, but its parent is an older network.
   - GivingTrax (2010) and GoodCoin (in/PACT 2015) are included on the same footing: dedicated in-window sponsors of older companies.
   - Eight of 18 members have a parent founded before 2021. The strict subset (n=8) is the only reading free of this choice. The note's "its rates are similar" is fair (active 62.5% against 55.6%).
3. **Grapevine's evidence strength (V32A-34).**
   - The CSV marks it `moderate`, but its status rests only on search extracts, which the data dictionary defines as `weak`. §7.5 of the note already counts it as weak.
   - Grapevine's pages returned 403 to this validator too. The search extract dates the Catalyst Fund grant post 2026-06-25.
4. **FY2024 filing survival rests partly on imputed rows (V32A-29).**
   - For 6 of the 10 Frame A sponsors, the FY2024 DAFRC row is `Imputed`: Daffy, AnonDo, Grapevine, GoodCoin, Matbia and Manifold.
   - The ProPublica 202412 listing and the null `revocation_date` (both confirmed for all 10) are the real FY2024 evidence.
5. **Minor figures:**
   - The median age is 4.375 years, not 4.35 (V32A-26).
   - The purposive-50 has 13 unknown founding years, not 12, and 15 pre-2021 (V32A-45).
   - Uncommon Giving's 2026 price floor is $2,400/yr for grants management; $5,000/yr is the employee-giving tier (V32A-39).
   - Every.org's ProPublica record now shows a 2025-10 ruling with public-charity code 15, alongside 990-PF returns for 2018–2024 (V32A-46).
6. **Interpretation.**
   - The 3.7%/yr hazard bound treats the 6 unknowns as still operating (V32A-27). The note gives the 7.4% alternative but calls 3.7% "the honest summary" without saying it is conditional.
   - Infinite Giving is a borderline fit for product rule (ii) next to the excluded Givefront (V32A-33). Infinite Giving accepts DAF grants for nonprofits but is not built for DAFs.

## Exact corrections

### `research/mission-2026-11-14/gap19-exception-load-proxy.md`
1. **Outputs, row count.**
   - **Find:** "- [`data/mission-2026-11-14/exception-load-proxy-2026-11-19.csv`](../../data/mission-2026-11-14/exception-load-proxy-2026-11-19.csv): 166 rows."
   - **Replace with:** "- [`data/mission-2026-11-14/exception-load-proxy-2026-11-19.csv`](../../data/mission-2026-11-14/exception-load-proxy-2026-11-19.csv): 167 rows [V wave 32A]"
2. **§0, core proxy.**
   - **Find:** "Excluding SVCF and the university/hospital sponsors: **7.2% / 9.8%**."
   - **Replace with:** "Excluding SVCF and the university/hospital sponsors: **7.2% / 9.8%**. Without the Greater Horizons FY2024 totals row (§2), core is 7.41% / **10.96%** (gap +3.55 pp, 1.48×) and 7.2% / 9.6% excluding SVCF and university/hospital sponsors [V wave 32A]"
3. **§0, sponsor distribution.**
   - **Find:** "Outside the university/hospital sponsors the lowest is 7.9% (Ayco)."
   - **Replace with:** "Outside the university/hospital sponsors the lowest is 5.6% (Dechomai, 9 lines), then 7.9% (Ayco). The 59.8% at Greater Horizons is an e-file totals row (§2). Without it Greater Horizons is 19.8%, the maximum is SVCF at 45.8% and the p75 is 20.7% [V wave 32A]"
4. **§0, national sponsor count.**
   - **Find:** "- National (16 sponsors): 7.0% / 10.2%."
   - **Replace with:** "- National (15 sponsors; Servant Foundation is counted under faith): 7.0% / 10.2%, or 7.0% / 9.9% without the Greater Horizons totals row [V wave 32A]"
5. **§2, Greater Horizons line.**
   - **Find:** "  - Greater Horizons FY2024: a line with **no name and no EIN**, $212.2m (blank EIN, so `not_c3_or_not_pub78_unexplained`);"
   - **Replace with:** "  - Greater Horizons FY2024: a line with **no name and no EIN**, $212.2m (blank EIN, so `not_c3_or_not_pub78_unexplained`). It is not a grant. $212,187,406 is exactly the sum of the return's 3,282 named lines, and a second blank line carries $3,282, the line count. Together they are an e-filed totals row, so Greater Horizons' Schedule I dollars are double-counted. No other return among the 94 has this pattern [V wave 32A]"
6. **§3.1, pooled denominator.**
   - **Find:** "Denominator: 608,612 lines; $92.94bn."
   - **Replace with:** "Denominator: 608,612 lines; $92.94bn. **Validation note:** this includes Greater Horizons' FY2024 totals row (two blank lines: $212,187,406 and 3,282). Without it the denominator is 608,610 lines and $92.72bn; raw not-c3/not-Pub-78 is 9.11% of dollars (0.47×); unexplained is 13,568 lines and $0.89bn (0.96%); blank EIN with no label is $0.06bn on 1,095 lines; broad is 25.08% / 19.72%; core is 7.41% / 10.96% (gap +3.55 pp); and FY2024 core is 7.36% / 9.73% [V wave 32A]"
7. **§3.1, sensitivity.**
   - **Find:** "- Excluding university/hospital sponsors and SVCF (88 sponsor-years): broad 25.1% / 17.5%; core **7.2% / 9.8%**."
   - **Replace with:** "- Excluding university/hospital sponsors and SVCF (88 sponsor-years): broad 25.1% / 17.5%; core **7.2% / 9.8%**. Without the Greater Horizons totals row: broad 25.1% / 17.3%, core 7.2% / 9.6% [V wave 32A]"
8. **§3.2, National row (use `sponsor_type`, not `dafrc_segment`).**
   - **Find:** "| National | 16 (31) | 471,541 | $63.97bn | 26.48% | 17.85% | −8.6 | 7.03% | 10.21% | +3.2 | 16.87% (15.20–19.68%) | 24.58% (17.05–28.02%)"
   - **Replace with:** "| National (excl. Servant) | 15 (29) | 466,753 | $62.50bn | 26.47% | 17.83% | −8.6 | 7.02% | 10.18% | +3.2 | 16.78% (15.08–20.02%) | 24.54% (16.91–27.35%) [V wave 32A]"
9. **§3.2, National dollar shares by category.**
   - **Find:** "| National | 1.91% | 8.32% | 1.34% | 4.58% | 1.45% | 1.72%"
   - **Replace with:** "| National (excl. Servant) | 1.96% | 8.42% | 1.36% | 4.36% | 1.49% | 1.75% [V wave 32A]"
10. **§3.2, National count shares by category.**
    - **Find:** "| National | 0.35% | 21.12% | 2.28% | 4.66% | 0.08% | 0.39%"
    - **Replace with:** "| National (excl. Servant) | 0.36% | 21.13% | 2.28% | 4.64% | 0.08% | 0.39% [V wave 32A]"
11. **§3.2 reading, CF count shares.**
    - **Find:** "- Community foundations also have the highest foreign and fiscal-sponsor **count** shares (1.34% and 0.34%), about four times the nationals'."
    - **Replace with:** "- Among the national, community-foundation and faith types, community foundations have the highest foreign and fiscal-sponsor **count** shares (1.34% and 0.34%), about four times the nationals'. The two university/hospital sponsors are higher on foreign counts (56.2%) [V wave 32A]"
12. **§3.3 notes, Greater Horizons.**
    - **Find:** "- **Greater Horizons (59.8% of dollars)** is driven by one FY2024 line with no name and no EIN ($212.2m)."
    - **Replace with:** "- **Greater Horizons (59.8% of dollars)** is driven by one FY2024 line with no name and no EIN ($212.2m). That line is an e-filed total: it equals the sum of the 3,282 named lines, and a second blank line holds the count. Without them Greater Horizons is 25.1% / 19.8% broad and 7.2% / 9.5% core (core gap +2.3 pp) [V wave 32A]"
13. **§1.4, legal basis for the PF/ER split.**
    - **Find:** "   - Non-operating PFs and Type III non-functionally-integrated SOs need ER under [§4945(h)](https://www.law.cornell.edu/uscode/text/26/4945) standards."
    - **Replace with:** "   - Non-operating PFs and Type III non-functionally-integrated SOs need ER under [§4945(h)](https://www.law.cornell.edu/uscode/text/26/4945) standards. The `er_required` flag is approximate in both directions. It overstates, because conduit and common-fund PFs (§170(b)(1)(F)(ii)–(iii)) are also (A)(vii) organisations. It understates, because donor-controlled Type I, Type II and functionally integrated Type III SOs are disqualified supporting organisations under §4966(d)(4)(A)(ii) but are not screened, and Pub 78 `SOUNK` recipients are not flagged [V wave 32A]"
14. **§3.1, Founders Pledge.**
    - **Find:** "($53.9m: BMF code 04 but Pub 78 PC, so the IRS lists disagree"
    - **Replace with:** "($53.9m: BMF code 04 but Pub 78 PC, so the IRS lists disagree. A sponsor relying on Pub 78 under Rev. Proc. 2018-32 would treat it as a public charity. Without it the ER-required total is about $86.7m [V wave 32A]"

### `research/mission-2026-11-14/gap19-startup-cohort.md`
1. **§1.1, hazard bound.**
   - **Find:** "(rule-of-three 95% bound)"
   - **Replace with:** "(rule-of-three 95% bound, which assumes the 6 unknowns are still operating) [V wave 32A]"
2. **§1.2, filing frame.**
   - **Find:** "carry no DAFRC exit flag through FY2024"
   - **Replace with:** "carry no DAFRC exit flag through FY2024. For 6 of the 10 (Daffy, AnonDo, Grapevine, GoodCoin, Matbia, Manifold) the FY2024 DAFRC row is imputed, not filed, so the ProPublica 2024-12 listing is the FY2024 evidence [V wave 32A]"
3. **§1.3, purposive-50 founding years.**
   - **Find:** "Twelve have an unknown founding year, and the rest predate 2021"
   - **Replace with:** "Thirteen have an unknown founding year, and the other 15 predate 2021 [V wave 32A]"
4. **§2.1, unit of analysis (Uncommon Giving).**
   - **Find:** "One consequence: companies older than 2021 that created a dedicated sponsor in the window are included, for example GivingTrax (2010) and in/PACT (2015)."
   - **Replace with:** "One consequence: companies older than 2021 that created a dedicated sponsor in the window are included, for example GivingTrax (2010) and in/PACT (2015). Uncommon Giving does not pass the window test. Its sponsor (84-3815117) has a FY2020 DAFRC row with 266 DAF accounts, and the product launched publicly on 2020-07-28. Its first observable entry event therefore predates the window, as Endaoment's does. It is in only because its ruling month reads 2021-01. Without it the cohort is 17 (active 10, acquired 1, pivoted 0, unknown 6), and the lower bound is 11/17 = 64.7% (41.3–82.7%) [V wave 32A]"
5. **§2.1, incumbent exclusion.**
   - **Find:** "  - Subsidiaries or products of incumbents founded before 2021 (bank DAF programs, GoFundMe Giving Funds, Altruist DAFs, Telescope Fund)"
   - **Replace with:** "  - Subsidiaries or products of incumbents founded before 2021 (bank DAF programs, GoFundMe Giving Funds, Altruist DAFs, Telescope Fund). The rules do not define \"incumbent\". Telescope Fund (a dedicated sponsor ruled in 2023 inside an older network) is excluded, while dedicated in-window sponsors of older companies (GivingTrax, GoodCoin, Goodstack) are included. The strict subset is the only reading free of this choice [V wave 32A]"
6. **§4.1, median age.**
   - **Find:** "80.9 (median age 4.35 years; range 2.3–5.8)"
   - **Replace with:** "80.9 (median age 4.4 years, exactly 4.375; range 2.3–5.8) [V wave 32A]"
7. **§7.3, median age.**
   - **Find:** "The median age is 4.35 years and the maximum 5.8"
   - **Replace with:** "The median age is 4.4 years (4.375) and the maximum 5.8 [V wave 32A]"
8. **§5, Uncommon Giving price.**
   - **Find:** "In 2026 the product is an employer CSR suite priced from $5,000/yr"
   - **Replace with:** "In 2026 the product is an employer CSR suite (grants management from $2,400/yr; employee giving and volunteering from $5,000/yr) [V wave 32A]"

### `data/mission-2026-11-14/daf-startup-cohort-2021-2026.csv`
1. **SC12 Grapevine, evidence strength.**
   - **Find:** "/20230808466348/en/,2,moderate,202412,yes,none,,,Grapevine pages returned 403 to curl and WebFetch; dates taken from search-result extracts"
   - **Replace with:** "/20230808466348/en/,2,weak,202412,yes,none,,,Grapevine pages returned 403 to curl and WebFetch; dates taken from search-result extracts; strength set to weak per the data dictionary [V wave 32A]"
2. **SX07 Every.org, exclusion reason.**
   - **Find:** "990-PF filer, no DAF sponsor entity"
   - **Replace with:** "990-PF filer, no DAF sponsor entity; ProPublica API 2026-11-19 lists 990-PF returns 2018-12 to 2024-12 and an org record with ruling 2025-10 and foundation code 15 [V wave 32A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.29.** Add "### 11.30 Gap-audit batch part A (validated, wave 32A)", containing the paragraph below. If §11.30 is already taken, use the next free number.
   - **Find:** "   >   - Every changed cell has a resolving pointer. Source: [validation-wave31a-report.md](mission-2026-11-14/validation-wave31a-report.md)."
   - **Replace with:** "   >   - Every changed cell has a resolving pointer. Source: [validation-wave31a-report.md](mission-2026-11-14/validation-wave31a-report.md).

### 11.30 Gap-audit batch part A (validated, wave 32A)

> **Gap-audit batch part A** (validated, wave 32A). Top-50 sponsors' FY2023–24 Schedule I and F filings were screened for grants that leave the routine "listed, long-recognised US public charity" path. The routes screened were foreign recipients, recipients outside Pub 78 without an explaining label, rulings within 24 months, named fiscal sponsors and private foundations. On that core definition the share is 7.4% of recipient lines and 11.0% of dollars, once one $212.2m totals row is removed. The broad definition gives 25% and 20%; it is count-heavy because of churches and group subordinates. At the four largest nationals the existing "2.5–3%" measure reproduces at 3.6%, about a third of their core 10.0%. Operating foundations ($949m) need no expenditure responsibility under §4966(c)(2)(A). The screen measures recipients, not observed review. A census of 18 DAF entrants from 2021–2026 finds no documented shutdown: 10 active, 1 acquired, 1 pivoted, 6 unknown. Survival is 66.7–100%, with a 3.7%/yr hazard bound if the unknowns survive. Uncommon Giving operated in 2020, so the strict subset (n=8) is the cleaner read (repo [`validation-wave32a-report.md`](mission-2026-11-14/validation-wave32a-report.md)) [V wave 32A]"

New subsection text:

> **Gap-audit batch part A** (validated, wave 32A). Top-50 sponsors' FY2023–24 Schedule I and F filings were screened for grants that leave the routine "listed, long-recognised US public charity" path. The routes screened were foreign recipients, recipients outside Pub 78 without an explaining label, rulings within 24 months, named fiscal sponsors and private foundations. On that core definition the share is 7.4% of recipient lines and 11.0% of dollars, once one $212.2m totals row is removed. The broad definition gives 25% and 20%; it is count-heavy because of churches and group subordinates. At the four largest nationals the existing "2.5–3%" measure reproduces at 3.6%, about a third of their core 10.0%. Operating foundations ($949m) need no expenditure responsibility under §4966(c)(2)(A). The screen measures recipients, not observed review. A census of 18 DAF entrants from 2021–2026 finds no documented shutdown: 10 active, 1 acquired, 1 pivoted, 6 unknown. Survival is 66.7–100%, with a 3.7%/yr hazard bound if the unknowns survive. Uncommon Giving operated in 2020, so the strict subset (n=8) is the cleaner read (repo [`validation-wave32a-report.md`](mission-2026-11-14/validation-wave32a-report.md)) [V wave 32A]
