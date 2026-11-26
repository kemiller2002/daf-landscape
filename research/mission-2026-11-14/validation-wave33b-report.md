# Validation wave 33B: DAF tax guidance (P-B41N16-01, P-B42N20-03) and the gap19-11 consistency pass

**Validator:** independent-validation-agent-wave33b. **Date:** 2026-11-19. **Register:** [`validation-register-wave33b.csv`](../../data/mission-2026-11-14/validation-register-wave33b.csv) (46 claims, V33B-01 to V33B-46).

**Scope.**
1. [`b41n16-b42n20-daf-tax-guidance.md`](b41n16-b42n20-daf-tax-guidance.md), with its two CSVs and `scripts/mission_b41n16_b42n20_checks.py`.
2. [`gap19-11-consistency-pass.md`](gap19-11-consistency-pass.md): 66 Find/Replace items and the proposed synthesis §0.

**Rules kept.**
- No edits to the report or the synthesis. No commit or push.
- No crt.sh, certspotter or sec.gov, and no outreach.
- No fetch of NPT, Renaissance or Foundation For The Carolinas sites.
- robots.txt was read before every host. A page was fetched only when `*`, `research-script/1.0`, ClaudeBot, Claude-User and anthropic-ai were all allowed. A non-200, non-404 robots.txt meant no fetch.
- The user agent was never changed.
- congress.gov was not used.

**Fetched (all HTTP 200, robots allowed).**
- **Law and guidance:**
  - Notice 2017-73;
  - the NPRM (govinfo FR-2023-11-14, doc 2023-24982);
  - all five Priority Guidance Plan PDFs;
  - P.L. 119-21 on govinfo;
  - LII 26 USC 170 and 63;
  - two Federal Register API searches;
  - the eCFR Part 53 structure;
  - IR-2026-135;
  - Schedule D (Form 990), Rev. 12-2024;
  - the DAFRC 2024 executive summary.
- **Sponsor pages (11):**
  - Fidelity OBBB article and pledge FAQ;
  - the Vanguard bunching blog, tax center (with its calculator JS) and January 2026 policies PDF;
  - SVCF 2026 tax blog;
  - the Morgan Stanley DAF article and MS GIFT grantmaking PDF;
  - the AEF bunching article and granting guidelines PDF;
  - the NCF OBBBA PDF and guide;
  - the DAFgiving360 2024 Program Policies (Squarespace copy).
- **University pages (5):** Caltech gift policies PDF, USC policy, the Northwestern NBI transmittal, Chicago Booth and WashU.

**Not fetched.** `www.dafgiving360.org/robots.txt` and `advisorservices.schwab.com/robots.txt` returned **403** on 2026-11-19, so the DAFgiving360 tax page and calculator were not re-read. The source pass recorded those hosts as allowed.

## Summary counts

| Result | Count |
|---|---|
| Confirmed | 28 |
| Partially confirmed | 13 |
| Contradicted | 4 |
| Unverifiable | 1 |
| **Total** | **46** |

**Consistency-pass items (66):** 57 accept, 9 modify, 0 reject.
- C-S09 carries the 11 corrections to the §0 text (§3 below).
- All 66 Find strings occur exactly once in the current files. That still holds after §11.32 (wave 33A) was added to the report.
- Sequential application, with C-S09 last, gives 0 problems.

## Findings

### 1. Tax guidance (P-B41N16-01, P-B42N20-03)

**Confirmed from primary text.**
- **Notice 2017-73.** The three §4 conditions are on pp. 9–10, and §7 reliance ("Taxpayers may rely on the rules described in section 4 until additional guidance is issued") is on p. 14. §4 itself is framed as an approach Treasury "anticipated" for proposed regulations, so reliance rests on §7 alone.
- **NPRM.** Its background recites the notice's pledge approach. Footnote 4 defers other comments to "future guidance under other Code sections". The NPRM starts at 88 FR 77922.
- **Priority Guidance Plans.**
  - The §4967 item is item 7 in the 2023–24 Q4 update (2024-09-06) and in the 2024–25 initial plan (2024-10-03).
  - "4967" occurs 0 times in the 2025–26 initial plan, the 2025–26 year-end update and the 2026–27 plan.
  - Item 35 in both 2025–26 PDFs has no PUBLISHED line.
  - 2026–27 Tax Exempt Organizations item 4 is verbatim. The 40 OBBBA items include no §170 item.
- **Federal Register.** Both searches returned 5 results. The only Treasury rule documents are the NPRM and its procedural notices. The eCFR jumps from §53.4965 to §53.4968.
- **Statute.**
  - §§70424, 70425 and 70111 read verbatim at 139 Stat. 235–236 and 164–165.
  - LII §170(p) shows the DAF and 509(a)(3) exclusions and the "(b)(1)(I)" carve-out, with no indexing.
  - LII §63(b)(4) confirms that §170(p) is a deduction for non-itemizers taken from AGI. It is not an above-the-line deduction.
- **Pledge tallies.**
  - Recipients recompute exactly from the CSV: 2 / 8 / 13 / 7, with $841.5m / $852.9m / $2,158.0m / $3,260.7m, totalling $7,113.1m.
  - The shares also recompute: 11.8% and 45.8%.
- **Sponsor and university quotes.** All quotes re-read verbatim: AEF (all three notice conditions), Fidelity, DAFgiving360 2024, Vanguard, MS GIFT, NCF, Caltech, USC (last reviewed 2021-03-01), Northwestern, Booth and WashU.
- **Vanguard bunching example.** "$9,490 ... $28,470 ... $29,125 ... a $655 increase" is verbatim. The implied rates are 26% and 25%, and at 35% the gain is $2,450. The page also writes the floor as "700,000 x 0.5".
- **Vanguard calculator.** `calculateTaxSavings()` was re-fetched and matches the port: floor 0.005, cash cap 0.6, MFJ $32,200, and 0.37 → 0.35. The H3 excess is 3 × (40,000 − 32,200) × 0.35 = $8,190.
- **Calculator outputs.** The script reproduces every H1–H3 figure. Its inputs match the tax-scenario note's §2.1.
- **AEF worked example.** $52,500 / $96,600 / $116,900 / "roughly $4,900" (= $4,872) all hold. The page does not mention the 35% cap.
- **Other sponsor pages.** These match as stated: Fidelity (not indexed; $350 against $370), SVCF, Vanguard's tax center exclusion, MS GIFT footnotes 2 and 4, and IR-2026-135.

**Corrections needed.**
1. **The deemed-distribution risk is overstated** (V33B-03).
   - The NPRM preamble says a deemed distribution "generally would be a taxable distribution".
   - §4966(c)(2)(A), restated in the NPRM, excludes distributions to §170(b)(1)(A) organizations, and a pledge payment goes to such an organization.
   - "Would face §4966 tax" should therefore be "could face", with the exception flagged as unresolved.
2. **The NPRM applicability wording is imprecise** (V33B-04). Proposed §53.4966-6 says "ending on or after".
3. **The "$161.8bn" is misattributed** (V33B-14). It is the 7 sponsors read in full, including MS GIFT. The 6 that state the DAF exclusion hold $152.73bn.
4. **The AEF framing is partly unfair** (V33B-20). The article says DAF gifts do not qualify under §70424 and that "small cash gifts made directly to charities in off years can still capture it". Only the worked table's baseline omits §170(p). The $3,432 recomputation stands.
5. **NCF is not error-free** (V33B-22). It calls §170(p) "an above-the-line deduction", which is wrong in terminology but not in eligibility.
6. **NPT [S] is presented as a pledge-feature anchor.** The product-implication sentence should rest on AEF [F] and treat NPT as unverified.
7. **Two pledge CSV labels are wrong** (V33B-11).
   - PL-GO-32 (Rockefeller, "not researched (time)") and PL-GO-33 (Boston College, "not fetched") are labelled R with no robots block, so both should be U.
   - The §3.1 not-read row should state the reasons.
   - "Mostly because of robots.txt" still holds: 5 of 7, and $3,132.6m of $3,260.7m.
8. **The DAFgiving360 rows could not be re-checked** (V33B-17, V33B-18). The robots.txt now returns 403.
   - The port arithmetic is confirmed: $2,016, $5,472, $55,500, $3,456 and +17.46%.
   - The absence of indexing in §170(p) is confirmed from the statute.
   - The page text itself is unverifiable this wave, and a limits note is added.

### 2. Consistency pass (gap19-11)

**Confirmed.**
- **Finds.** All 66 occur exactly once, and sequential application gives 0 problems.
- **Markers.** There are 17 in the report and 6 in the synthesis.
- **Citation audit.** It flags 225 lines, 201 of them in the report.
- **C-R20 status counts.** They recompute exactly from the consolidated CSV with `self_loop=False`: 958 / 23 / 47 / 11 / 5 / 3 / 2 / 1 / 1, summing to 1,051.
  - The red-team members total 41 / 16 / 52 over 109 edges, one of which is a self-loop.
  - Red-team outcomes are not written back to `status`. For example, 7 unknown edges that the red team confirmed are still "unknown". C-R20 reports both, so it is consistent.
- **Validation registers.** The totals recompute exactly: 37 files, 1,036 rows and 1,012 IDs, with results 784 / 195 / 32 / 15 / 10. The 80-row waves 1–2B subset (22 + 31 + 27) gives 45 / 25 / 7 / 3.
- **Exception figures.** 3.6% (1.96 + 1.50 + 0.15), 10.0% (core, four nationals) and 11.0% / 7.4% (top 50, corrected 10.96% / 7.41%) all match the source.
- **Wayback softening (C-R13).** It is supported by `competitive-history-timelines.md` l.65 and l.390, FINAL-STATUS l.211, and wave 31B ("fetched no captured page"). The report cites 4 captures (3 distinct).
- **C-R01.** The Schedule D Part I lines 1–4 and the DAFRC figures were re-fetched and match.
- **Spot-checked text.** These items match their cited text: C-R05 (with one added limit), C-R07, C-R09, A01, A02, A05, A07, A08, A10–A16, A19–A21, A23–A30 and C-S01–C-S07.

**Problems.**
1. **§9 "Other" composition** (V33B-28). "Passed 22 of 24" is one of the seven wave-13 rows, and "weakly supported" (wave 12) is missing from the list. The total of 10 is right.
2. **Ren 19 sponsors / $31.56bn** (V33B-29). The figure is right, but the +1 is Ayco's final return, and Ayco "is not a live client" (it merged into GS DAPF on 2025-07-01). C-R25 should say this, and so should A22 and §0 A, which present 19 as current reach.
3. **A09** (V33B-35). It turns the report's correct plural "help pages" into "a Ren help page" and drops the basis. V10-05 says the fee "rests only on a search-index capture of now-404 Ren pages".
4. **§0 accounts** (V33B-37). The 2.59m figure restates the corrected 3.31m, and the wave-21 changelog says DAFRC's 3.59m is "on a different basis". So "the 3.59m reported accounts become 2.59m" (G2) is wrong as worded, and A1 needs the basis stated.
5. **§0 B AI coverage** (V33B-39). The source read 13 of the 20 entities (7 were blocked). "12 of 20" is the wave-31B validator's spot-check count.
6. **§0 citations.**
   - The adviser-fee caps come from `queue-all-in-cost-dafpay-access.md` and V10-05, not `queue-adviser-fees-pools-npact.md`. MS GIFT's cap also excludes Legacy Pools and Select UMA fees.
   - Fidelity's 20.5–21.7% is in `direction-league-table-concentration.md`, not the long-tail file.
   - NPT's 12.8% is not in `gap19-second-source-pass.md`.
7. **Small items.**
   - C-S08's "FY2025 990s" should be "FY6/2025".
   - C-R21's method pointer should be §1 (method) and §4 (caveat).
   - A06 should note that MS GIFT, RCF, US Charitable Gift Trust and NCF have not yet filed FY2025.
   - C-R05 should keep V wave 22's "top-five contractor lines" limit.
   - C-R06's proxy list should say "private foundations or other recipients needing expenditure responsibility".
   - C-S09's Replace is a placeholder. The checker's tag test passes only because the placeholder contains the tag, so C-S09 must be applied by hand from the corrected §6.
8. **§0 figures otherwise confirmed** (V33B-42 to V33B-44): CR3/CR5/HHI, 32.2% (54 sponsors), payout 25.9 / 22.8 / 12.7, netting, 0.082%, 249 submissions, all-in cost, donate pages, geography, lobbying, foreign 7.8%, long tail, Foundant, Give Interactive, AI calibration, $0.45 against $83, 5 of 28, 36%, six of the top 20, complaints, startups, $58.41bn, 46.4% → 3.49%, 78.7 against 2.9 bps, $0 program-service revenue, and the CF fees (37 schedules covering 46.1%; the 46% at l.210 of the fee doc is a different quantity).
9. **§0 may govern after correction.** Once these corrections are applied, the §0 section can govern, as the pass's own §7 limits anticipate.

## Table of the 66 consistency-pass items

| Item | Target | Verdict | Note |
|---|---|---|---|
| C-R01 | report | accept | Schedule D and DAFRC re-fetched |
| C-R02 | report | accept | |
| C-R03 | report | accept | |
| C-R04 | report | accept | |
| C-R05 | report | modify | add the top-five-contractor-lines limit (V wave 22) |
| C-R06 | report | modify | the core proxy includes recipients needing expenditure responsibility; 10.96% |
| C-R07 | report | accept | |
| C-R08 | report | accept | |
| C-R09 | report | accept | |
| C-R10 | report | accept | |
| C-R11 | report | accept | |
| C-R12 | report | accept | |
| C-R13 | report | accept | softening supported |
| C-R14 | report | accept | |
| C-R15 | report | accept | |
| C-R20 | report | accept | counts recomputed |
| C-R21 | report | modify | method §1, caveat §4 |
| C-R22 | report | accept | totals recomputed |
| C-R23 | report | accept | |
| C-R24 | report | accept | |
| C-R25 | report | modify | Ayco is not a live client; 9.6% |
| C-R26 | report | accept | depends on C-S09 |
| A01 | report | accept | |
| A02 | report | accept | |
| A03 | report | accept | |
| A04 | report | accept | |
| A05 | report | accept | |
| A06 | report | modify | the largest Ren clients have not filed FY2025 |
| A07 | report | accept | |
| A08 | report | accept | |
| A09 | report | modify | keep "pages"; search-index capture |
| A10 | report | accept | |
| A11 | report | accept | |
| A12 | report | accept | |
| A13 | report | accept | |
| A14 | report | accept | |
| A15 | report | accept | |
| A16 | report | accept | |
| C-S01 | synthesis | accept | |
| C-S02 | synthesis | accept | |
| C-S03 | synthesis | accept | |
| C-S04 | synthesis | accept | |
| C-S05 | synthesis | accept | |
| C-S06 | synthesis | accept | |
| C-S07 | synthesis | accept | |
| C-S08 | synthesis | modify | FY6/2025 |
| C-S09 | synthesis | modify | placeholder; insert §6 as corrected below (11 corrections) |
| C-S10 | synthesis | accept | |
| C-S11 | synthesis | accept | |
| C-S12 | synthesis | accept | |
| C-S13 | synthesis | accept | |
| C-S14 | synthesis | accept | |
| A17 | synthesis | accept | |
| A18 | synthesis | accept | "so far" carries the limit |
| A19 | synthesis | accept | |
| A20 | synthesis | accept | |
| A21 | synthesis | accept | |
| A22 | synthesis | modify | Ayco caveat |
| A23 | synthesis | accept | |
| A24 | synthesis | accept | |
| A25 | synthesis | accept | |
| A26 | synthesis | accept | PGP item 4 re-fetched |
| A27 | synthesis | accept | |
| A28 | synthesis | accept | |
| A29 | synthesis | accept | |
| A30 | synthesis | accept | |

**Tally:** 57 accept, 9 modify (C-R05, C-R06, C-R21, C-R25, A06, A09, C-S08, C-S09, A22), 0 reject.

## Exact corrections

**Conventions.**
- Each Find is the verbatim text between the outer quotes. Inner double quotes are literal.
- Inner quotes are plain double quotes, exactly as in the target files.
- `\n` (backslash-n) in the report item stands for a newline.
- Each Find was checked to occur exactly once in its target as it stands on 2026-11-19.

### `research/mission-2026-11-14/b41n16-b42n20-daf-tax-guidance.md`

- **Find:** "treats any DAF use that gives a more-than-incidental benefit as a distribution, and so as a taxable distribution. If a pledge payment were ever held to be such a benefit, the sponsor would face §4966 tax as well as §4967 tax."
- **Replace with:** "treats any DAF use that gives a more-than-incidental benefit as a deemed distribution, which the preamble says 'generally would be a taxable distribution'. If a pledge payment were ever held to be such a benefit, the sponsor could face §4966 tax as well as §4967 tax. Whether the §4966(c)(2)(A) exception for distributions to §170(b)(1)(A) organizations would still apply is not addressed [V wave 33B]."

- **Find:** "The deemed-distribution rule, if finalised, would make any benefit that is more than incidental under §4967 a taxable distribution as well [I]."
- **Replace with:** "The deemed-distribution rule, if finalised, would generally make any benefit that is more than incidental under §4967 a taxable distribution as well. Its interaction with the §4966(c)(2)(A) exception for distributions to public charities is unresolved [I; V wave 33B]."

- **Find:** "**Applicability:** proposed to apply to tax years ending after final regulations are published."
- **Replace with:** "**Applicability:** proposed §53.4966-6 applies to tax years ending on or after the date final regulations are published (the preamble says 'ending after') [V wave 33B]."

- **Find:** "That is $161.8bn of $222.5bn top-10 DAF assets read [F]."
- **Replace with:** "These six hold $152.7bn. The seven sponsors read in full [F], adding MS GIFT, hold $161.8bn of the top 10's $222.5bn [V wave 33B]."

- **Find:** "**AEF:** the arithmetic is right, but the annual baseline omits §170(p) for direct gifts."
- **Replace with:** "**AEF:** the arithmetic is right, but the worked table's annual baseline omits §170(p) for direct gifts. The article's text does say that small direct cash gifts in off years can still capture it [V wave 33B]."

- **Find:** "AEF's example leaves out §170(p) for direct gifts, which inflates the case for DAF bunching against giving cash directly."
- **Replace with:** "AEF's worked table leaves out §170(p) for direct annual gifts, which inflates the case for DAF bunching against giving cash directly. Its text mentions §170(p) only for small off-year direct gifts [V wave 33B]."

- **Find:** "| 10 | NCF (5.68) | yes ("not to Giving Funds") | yes | yes | none found | none | F |"
- **Replace with:** "| 10 | NCF (5.68) | yes ("not to Giving Funds") | yes | yes | none found | minor: calls §170(p) "an above-the-line deduction"; under §63(b)(4) it is taken from AGI by non-itemizers, not above the line [V wave 33B] | F |"

- **Find:** "The two largest sponsors by assets that follow the notice, NPT and AEF, are the ones on which a pledge-matching feature could rest."
- **Replace with:** "The two top-15 sponsors that follow the notice are AEF [F] and NPT [S, not page-verified]. A pledge-matching feature could rest on AEF now, and on NPT only after a direct page read [V wave 33B]."

- **Find:** "| Not read | 7 | 3,260.7 | Johns Hopkins (robots 403), UCSF (robots unreachable), NYU (robots 403), Oregon, Lucile Packard, Rockefeller, Boston College |"
- **Replace with:** "| Not read | 7 | 3,260.7 | Johns Hopkins (robots 403), UCSF (robots unreachable), NYU (robots 403), Oregon and Lucile Packard (robots-disallowed donate paths, per the repo), Rockefeller and Boston College (not researched; no robots block) [V wave 33B] |"

- **Find:** "A user who enters different inputs, such as the actual bracket for the Vanguard calculator, would get different outputs."
- **Replace with:** "A user who enters different inputs, such as the actual bracket for the Vanguard calculator, would get different outputs. On 2026-11-19 the robots.txt of www.dafgiving360.org and advisorservices.schwab.com returned 403 to the wave-33B validator. The DAFgiving360 tax page and calculator source were therefore not re-read; only the port was re-run [V wave 33B]."

### `data/mission-2026-11-14/daf-pledge-policy-2026-11-19.csv`

- **Find:** ",86,68.9,not_read,unknown,unknown,not_read,R,,,2026-11-15,not researched (time),"
- **Replace with:** ",86,68.9,not_read,unknown,unknown,not_read,U,,,2026-11-15,not researched (time) [V wave 33B: label R to U; no robots block],"

- **Find:** ",100,59.3,not_read,unknown,unknown,not_read,R,,,2026-11-15,gift policy (Feb 2020) has no DAF clause [S]; not fetched,"
- **Replace with:** ",100,59.3,not_read,unknown,unknown,not_read,U,,,2026-11-15,gift policy (Feb 2020) has no DAF clause [S]; not fetched [V wave 33B: label R to U; no robots block],"

### `data/mission-2026-11-14/sponsor-obbba-tax-page-audit-2026-11-19.csv`

- **Find:** "none found,no example to compare"
- **Replace with:** "minor: calls the 170(p) deduction above-the-line; under 63(b)(4) it is taken from AGI by non-itemizers [V wave 33B],no example to compare"

- **Find:** "Annual baseline gives the couple the bare $32,200 standard deduction;"
- **Replace with:** "Annual baseline in the worked table gives the couple the bare $32,200 standard deduction (the article text does say small direct cash gifts in off years can still capture 170(p)) [V wave 33B];"

### `research/mission-2026-11-14/gap19-11-consistency-pass.md`

**(b1) C-R05.**
- **Find:** "This is a floor on receipts, not Ren revenue."
- **Replace with:** "This is a floor on receipts, limited to sponsors' top-five contractor lines, not Ren revenue. [V wave 33B]"

**(b2) C-R06.**
- **Find:** "named fiscal sponsors and private foundations) is 10.0% of their dollars and 11.0% across the top 50."
- **Replace with:** "named fiscal sponsors, and private foundations or other recipients needing expenditure responsibility: the core proxy) is 10.0% of their dollars and 11.0% across the top 50 (10.96% after the Greater Horizons correction). [V wave 33B]"

**(b3) C-R21.**
- **Find:** "method in [gap19-11-consistency-pass.md](mission-2026-11-14/gap19-11-consistency-pass.md) §4)"
- **Replace with:** "method in [gap19-11-consistency-pass.md](mission-2026-11-14/gap19-11-consistency-pass.md) §1, caveat in §4; [V wave 33B])"

**(b4) C-R25.**
- **Find:** "the addition being Ayco's final return (repo [`validation-wave31a-report.md`](mission-2026-11-14/validation-wave31a-report.md); [`gap19-fy2025-refresh.md`](mission-2026-11-14/gap19-fy2025-refresh.md))."
- **Replace with:** "the addition being Ayco's final return. Ayco merged into GS DAPF on 2025-07-01, so it is not a live client. The share is 9.6% of DAFRC FY2024 assets (repo [`validation-wave31a-report.md`](mission-2026-11-14/validation-wave31a-report.md); [`gap19-fy2025-refresh.md`](mission-2026-11-14/gap19-fy2025-refresh.md)). [V wave 33B]"

**(b5) A06.**
- **Find:** "and all 8 comparable FY2024 payers name Ren again (repo [`gap19-fy2025-refresh.md`](mission-2026-11-14/gap19-fy2025-refresh.md); [V wave 31A])."
- **Replace with:** "and all 8 comparable FY2024 payers name Ren again. The largest Ren clients (MS GIFT, RCF, US Charitable Gift Trust, NCF) have not yet filed FY2025 (repo [`gap19-fy2025-refresh.md`](mission-2026-11-14/gap19-fy2025-refresh.md); [V wave 31A]). [V wave 33B]"

**(b6) A09.**
- **Find:** "rests on a Ren help page that now returns 404, so it is low confidence"
- **Replace with:** "rests on a search-index capture of Ren help pages that now return 404, so it is low confidence [V wave 33B]"

**(b7) C-S08.**
- **Find:** "(2.5–3% in FY2025 990s; 3.6% like-for-like in FY2023–24)"
- **Replace with:** "(2.5–3% for FY6/2025; 3.6% like-for-like in FY2023–24 [V wave 33B])"

**(b8) A22.**
- **Find:** "and 19 sponsors holding $31.56bn name Ren in their latest return ([validation-wave31a-report.md](validation-wave31a-report.md))."
- **Replace with:** "and 19 sponsors holding $31.56bn name Ren in their latest return. One of them is Ayco's final return, which is not a live client ([validation-wave31a-report.md](validation-wave31a-report.md); [gap19-fy2025-refresh.md](gap19-fy2025-refresh.md)). [V wave 33B]"

**(b9) C-S09 mechanics.**
- **Find:** "- **Note:** insert §6 without its leading "> " quote markers."
- **Replace with:** "- **Note:** insert §6 without its leading "> " quote markers, after applying the wave-33B corrections to §6. The Replace string below is a placeholder and must be substituted by hand, so the checker's tag test does not cover it [V wave 33B]."

**(b10) §0 A1, accounts basis.**
- **Find:** "On the ongoing-advisory basis there are 2.59m, or 0.79m without Givinga and PayPal Giving Fund"
- **Replace with:** "On corrected FY2024 totals (3.31m accounts, a different basis from DAFRC's 3.59m) the ongoing-advisory basis gives 2.59m, or 0.79m without Givinga and PayPal Giving Fund [V wave 33B]"

**(b11) §0 G2, accounts basis.**
- **Find:** "The 3.59m reported accounts become 2.59m on the ongoing-advisory basis"
- **Replace with:** "DAFRC reports 3.59m accounts. On corrected totals (3.31m, a different basis) the ongoing-advisory count is 2.59m [V wave 33B]"

**(b12) §0 A4, Ayco.**
- **Find:** "19 sponsors holding $31.56bn name Ren in their latest 990 ([validation-wave31a-report.md](validation-wave31a-report.md))."
- **Replace with:** "19 sponsors holding $31.56bn name Ren in their latest 990. One of them is Ayco's final return, which is not a live client ([validation-wave31a-report.md](validation-wave31a-report.md); [gap19-fy2025-refresh.md](gap19-fy2025-refresh.md)). [V wave 33B]"

**(b13) §0 A4, NPT share.**
- **Find:** "NPT, 12.8% of the market, still rests on hosting evidence alone;"
- **Replace with:** "NPT, 12.8% of FY2024 DAF assets ($42.12bn of $327.87bn, per the wave-31A text), still rests on hosting evidence alone [V wave 33B];"

**(b14) §0 A, adviser caps.**
- **Find:** "Only MS GIFT, DAFgiving360 and TIFIN Give cap adviser fees, at 1.00% ([queue-adviser-fees-pools-npact.md](queue-adviser-fees-pools-npact.md); wave 11)."
- **Replace with:** "Only MS GIFT, DAFgiving360 and TIFIN Give/GiveClear publish an adviser-fee cap, at 1.00%. MS GIFT's cap excludes Legacy Pools and Select UMA manager fees, and Fidelity CIAP, NPT, AEF and RCF publish none ([queue-all-in-cost-dafpay-access.md](queue-all-in-cost-dafpay-access.md); [validation-wave10-report.md](validation-wave10-report.md) V10-05; [queue-adviser-fees-pools-npact.md](queue-adviser-fees-pools-npact.md)). [V wave 33B]"

**(b15) §0 B, hiring.**
- **Find:** "AI appears in 29.1% of vendor job postings against 13.3% of sponsor postings"
- **Replace with:** "AI appears in 29.1% of vendor job postings (44 of 151) against 13.3% of sponsor postings (2 of 15, a small sample) [V wave 33B]"

**(b16) §0 B, AI coverage.**
- **Find:** "Re-reading 12 of 20 entities found none documenting AI in grant approval or money movement"
- **Replace with:** "First-party reading of 13 of 20 entities (7 were blocked) found none documenting AI in grant approval, eligibility or money movement. This is an absence finding; the wave-31B validator spot-checked 12 [V wave 33B]"

**(b17) §0 C, Fidelity share.**
- **Find:** "Fidelity holds 20.5–21.7% of assets every year. Foundant serves 282 of 351 tail community foundations with an identified vendor ([direction-long-tail-sponsors.md](direction-long-tail-sponsors.md); wave 30)."
- **Replace with:** "Fidelity holds 20.5–21.7% of corrected assets every year in FY2021–24 ([direction-league-table-concentration.md](direction-league-table-concentration.md); wave 29). Foundant serves 282 of 351 tail community foundations with an identified vendor ([direction-long-tail-sponsors.md](direction-long-tail-sponsors.md); wave 30). [V wave 33B]"

**(b18) §0 F, tax guidance.**
- **Find:** "and any final §4966 rule ([IRS 2026-2027 Priority Guidance Plan](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf))."
- **Replace with:** "and any final §4966 rule, or guidance under the new 2026–27 item on §§4966 and 6033 DAF arrangements. The §4967 prohibited-benefits project, which would have codified the Notice 2017-73 pledge rule, has left the plan ([IRS 2026-2027 Priority Guidance Plan](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf); [b41n16-b42n20-daf-tax-guidance.md](b41n16-b42n20-daf-tax-guidance.md)). [V wave 33B]"

**(b19) §4, register "other" composition.**
- **Find:** "10 other (7 wave-13 audit-defect notes, plus "supported", "plausible" and "passed 22 of 24")"
- **Replace with:** "10 other (7 wave-13 audit notes: 5 defects, 1 cosmetic and 1 "passed 22 of 24"; 2 wave-12 "supported" and "weakly supported"; 1 wave-10 "plausible") [V wave 33B]"

**(b20) §7 limits, validation status.**
- **Find:** "It needs an independent validation pass before it governs."
- **Replace with:** "It needs an independent validation pass before it governs. Wave 33B validated it; with the corrections in [validation-wave33b-report.md](validation-wave33b-report.md) applied, it may govern [V wave 33B]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**New §11.33.** Insert after §11.32.
- **Find:** "Source: [validation-wave33a-report.md](mission-2026-11-14/validation-wave33a-report.md)."
- **Replace with:** "Source: [validation-wave33a-report.md](mission-2026-11-14/validation-wave33a-report.md).\n\n### 11.33 New-batch part B (validated, wave 33B)\n\n<the paragraph below> [V wave 33B]"
- *(The paragraph already ends with the tag. Do not add a second one.)*

New subsection text:

> **New-batch part B** (validated, wave 33B). Notice 2017-73 §4 still governs DAF pledge payments. Taxpayers "may rely" on it "until additional guidance is issued" (§7), and the Federal Register to 2026-11-19 holds only the 2023 §4966 proposal, which recites §4 as background. The §4967 prohibited-benefits project is in the 2023–24 and 2024–25 Priority Guidance Plans but not the 2025–26 or 2026–27 plans; the 2026–27 plan adds §§4966/6033 guidance on "certain donor advised fund arrangements". Of the top-30 university and medical gift offices, 2 ($841.5m of FY2023–24 DAF grants) publish the notice's rule, 8 ($852.9m) forbid DAF payment of personal or binding pledges or book DAF commitments as non-binding, and 20 ($5,418.7m) are silent or unread. Among the top-15 sponsors AEF [F] and NPT [S] follow the notice and five bar binding pledges. Under P.L. 119-21, six of the seven top-10 sponsor pages read in full say DAF gifts are outside the $1,000/$2,000 non-itemizer deduction. Vanguard's bunching example misstates the gain ($655; $2,450 at its own 35% rate), and MS GIFT states the floor carryover without its §170(d)(1)(C) condition (repo [`b41n16-b42n20-daf-tax-guidance.md`](mission-2026-11-14/b41n16-b42n20-daf-tax-guidance.md); [`validation-wave33b-report.md`](mission-2026-11-14/validation-wave33b-report.md)) [V wave 33B]

## Limits
- **DAFgiving360 sources were not re-read.** Their robots.txt returned 403. Two claims rest on the port and the statute only.
- **Search-text rows were not re-checked.** NPT and Renaissance rows stay [S], and nothing was fetched from those sites.
- **§0 figures were checked against their cited repo files, not raw data.** The exceptions are the graph status counts, the register totals and the pledge tallies, which were recomputed.
- **Recipient rows outside the ten fetched were not re-read.** The ten fetched were 5 university pages and 5 sponsor pledge documents.
- **This is not legal advice.**
