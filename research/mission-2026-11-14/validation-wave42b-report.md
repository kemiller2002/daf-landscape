# Validation wave 42B: faith sponsors outside the top 50; corporate 1% floor pull-forward

**Date:** 2026-11-20 · **Validator:** independent-validation-agent-wave42b · **Register:** [`data/mission-2026-11-14/validation-register-wave42b.csv`](../../data/mission-2026-11-14/validation-register-wave42b.csv) (34 claims, V42B-01 to V42B-34)

**Studies validated**
- Study 1: [b4026-06-01-faith-sponsors-outside-top50.md](b4026-06-01-faith-sponsors-outside-top50.md), its CSV and `scripts/mission_faith_sponsors_outside.py` (V42B-01 to -16).
- Study 2: [b41n18-02-corporate-floor-pull-forward.md](b41n18-02-corporate-floor-pull-forward.md), its CSV and `scripts/mission_b41n18_02_floor_pullforward.py` (V42B-17 to -34).

## Counts

| Result | Study 1 | Study 2 | Total |
|---|---|---|---|
| confirmed | 11 | 11 | 22 |
| partially_confirmed | 4 | 5 | 9 |
| contradicted | 1 | 1 | 2 |
| unverifiable | 0 | 1 | 1 |
| **Total** | **16** | **18** | **34** |

## Method and fetch log

- **Study 1 re-run.** The script was re-run cache-only, with `--out` and `--work` pointed at the validator scratch directory and the q2661 caches copied there. The CSV is byte-identical (md5 e497f4aca747d2b5958be7386845b25e). Headline figures were then recomputed from the CSV rows and the JSON diagnostic, not taken from the text.
- **Study 1 XML.** gt990datalake-rawdata.s3.amazonaws.com robots.txt returned 404 (no restriction). The validator fetched 4 raw returns: OJC Fund FY2023 and FY2024 (202411369349313111, 202521359349314057) and CCF-LA Supporting Organization FY2023 and FY2024 (202423189349312252, 202543179349308674). It re-read the study's saved XMLs for NCF Wisconsin, NCF Real Property and UJA-Federation. It parsed Schedule I with its own parser, independent of the repo extractor, and joined it to the cached IRS BMF.
- **Study 2 re-run.** The script was run with a scratch root. The CSV is byte-identical (md5 0d247c2eeb9efa5245ce6a544ac7e334). Every percentage was recomputed by hand.
- **Study 2 sources.** robots.txt returned 200 and allowed the paths on govinfo.gov, law.cornell.edu, ir.apollo.com, circle.com, ir.blackrock.com and investors.unum.com. The validator fetched the P.L. 119-21 HTML, LII 26 U.S.C. §170, the Apollo 10-K 2025 and 10-Q Q3 2026, and the Circle Q4 2025 release and Foundation blog post.
  - The BlackRock and Unum annual-report PDF URLs now return a 302 redirect to s24.q4cdn.com and s201.q4cdn.com. robots.txt on both hosts returns 403, so the validator did not follow the redirects and did not change its user agent. Those two reports were re-read from the study's cached PDFs (q1802/dl).
  - No request went to sec.gov, crt.sh, certspotter or any transcript site.

## Findings: Study 1 (faith sponsors outside the top 50)

1. **The core numbers hold** (V42B-02 to -06).
   - **S0.** S0 reproduces the base to the dollar: 29,469 recipients, $6,177,546,936, faith share 22.10%, nationals 74.22%.
   - **The addition.** It is $1,080,256,486 (+17.49%): $1,079.6m from 149 panel sponsors and $0.7m from 3 non-panel sponsors.
   - **Faith share.** It is 33.70% in S2 and 30.18% in S3. Without the OJC Fund it is 28.31% and 25.14%.
   - **Nationals.** Their share is 63.17% in S2 and 58.83% in S3, and 68.30% and 63.07% without the OJC Fund. National dollars rise only $182.7m.
2. **The OJC Fund is a real DAF sponsor, weighted correctly, and its lines check out** (V42B-07 to -09).
   - **DAF status.** Both FY2023 and FY2024 returns answer Yes to Part IV line 6. They report 4,731 and 5,976 DAFs and DAF grants of $338.3m and $385.7m, against total grants of $338.9m and $390.7m. The weights are 0.998 and 0.987.
   - **Line counts.** Raw Schedule I line counts (3,009 and 3,410) equal the cache.
   - **Recipient spot-checks.** Keren Mugein Imoisheya and Congregation Chonen Vnosen reconcile to the dollar. Keren Mugein's extra $7.1k is a third line from Associated Jewish Charities of Baltimore.
   - **Independent block recompute.** A BMF-only recompute gives $548.1m (76.7%) against the CSV's $545.3m (76.4%).
   - **New point: why it sits outside the top 50.** The OJC Fund is a pass-through sponsor: year-end DAF assets are only $42.5m and $34.5m. It ranks **22nd by FY2023 DAF grants but 284th by DAF assets**. Its absence from the top 50 is an artefact of ranking by assets.
3. **The CCF-LA attribution is wrong** (V42B-10, contradicted).
   - CCF-LA's Schedule I gives the Archdiocese of Los Angeles $24.0m in FY2023 and $51.9m in FY2024, **$75.9m** in all.
   - The $103.7m figure is the Archbishop's total from all faith sponsors outside the top 50. About $27.8m of it comes mostly from Catholic Community Foundation of Los Angeles (EIN 383941057).
4. **CCF-LA is Catholic by filing, not by inference** (V42B-11).
   - It is a Type II supporting organisation of Catholic Community Foundation of Los Angeles. Its mission is "donor advised fund granting to charities with Catholic values".
   - It holds one DAF account, received no contributions in FY2023–24 and is drawing down a single fund.
   - The Catholic total becomes $230.6m and the Christian $235.7m. The faith total does not change.
5. **NCF Wisconsin and NCF Real Property are confirmed** (V42B-12, -13).
   - Both have `DonorAdvisedFundInd` 0.
   - NCF Wisconsin made no grants in FY2024.
   - NCF Real Property's only FY2024 grant is $38.6m to NCF itself (DAF-to-DAF).
6. **The UJA reading needs a wording fix** (V42B-14).
   - UJA answers **Yes** to Part IV line 6, but Schedule D column (a), donor advised funds, is empty.
   - Its 18 accounts ($0.9m of grants) are in column (b), "funds and other accounts". Column (b) holds non-DAF accounts, so the study should not call them DAFs. Excluding UJA is correct.
7. **Classification audit: 14 of 15 correct** (V42B-15).
   - **One mislabel.** CCF-LA is labelled Christian but is Catholic.
   - **The DAFRC subtype admits religious operating charities.** World Vision, American Bible Society, Jewish National Fund and Hebrew Academy of Cleveland are included, despite §1.3's statement that single-issue sponsors are left out. Their block dollars are under $1m, so this is immaterial.
   - **The name-rule admissions are sound:** the Signatry Charitable Trust and the Catholic Foundation of North Georgia.
8. **"Nationals' three-quarters holds only within the top 50"** (V42B-16, partially confirmed).
   - **What holds.** The arithmetic is correct, and "74.2%" must be labelled top-50 wherever it is reused.
   - **Denominator effect.** The fall is a denominator effect. The OJC Fund alone is 28.3% of the S3 non-top-50 addition.
   - **Missing nationals.** BofA Charitable Gift Fund and Renaissance, both DAFRC National, do not itemise and are absent from every scenario. All national shares are therefore understated by an unknown amount.
   - **Inconsistent wording.** §0 says the share "stays about two-thirds" without the OJC Fund (63.1%) while recommending "about three-fifths".
   - **Defensible statement:** "about three-fifths (58.8%; 63.1% without the OJC Fund) of itemised church-block dollars across all itemising panel sponsors; 74% within the top 50".

## Findings: Study 2 (corporate 1% floor pull-forward)

1. **The statute is confirmed verbatim** (V42B-18 to -22).
   - **Source.** govinfo P.L. 119-21 §70426 (139 Stat. 237–238, approved July 4, 2025).
   - **Floor and cap.** The 1% floor and 10% cap are on taxable income.
   - **Exclusions.** Contributions under (B) and (C) are outside the floor.
   - **Effective date.** "taxable years beginning after December 31, 2025".
   - **Carryforward.** The new §170(d)(2)(A)–(D) keeps the 5-year FIFO carryforward. It adds the rule that floor amounts carry forward only from years in which the 10% cap is exceeded, and an NOL reduction rule.
   - **Base.** LII confirms the §170(b)(2)(D) modifications to taxable income.
   - **Accrual timing.** §170(a)(2) is as described: board authorisation in the year, payment by the 15th day of the 4th month, and an election on the return. For a 31 January year-end, the FY2026 deadline is 2026-05-15.
2. **The company facts are confirmed** (V42B-23, -24, -27, -29).
   - **Apollo.** $200m and 1,213,003 shares in Feb 2025, "ongoing commitment to philanthropy". Pre-tax income $6,677m gives 3.00%. Q3 2026 shows "—" against $200m. That line is a supplemental non-cash financing disclosure, not a cash flow.
   - **BlackRock.** $109m expense and $29m benefit on 2025-12-10; "established in 2013"; nonrecurring. Pre-tax income $7,619m gives 1.43% and a 26.6% tax rate, 22 days before the floor.
   - **Unum.** $20.0m "accelerated", $15.8m after tax and a 21.0% tax rate. It states that OBBBA is not expected to be material, and pre-tax income is $933.5m (2.14%).
   - **Arithmetic.** Every percentage in the CSV recomputes.
3. **Circle** (V42B-25, -26).
   - Both quotes are verbatim.
   - The blog itself says "a donor-advised fund housed with Fidelity", so the Fidelity vehicle is first-party [F] and not only [R].
   - "Scheduled annual pledge" rests on the words "first annual". The first tranche fell after enactment in the last floor-free year, and no 2026 tranche was read. The case is partially confirmed.
4. **The BlackRock "ordinary explanation" is contradicted** (V42B-28).
   - The study calls it "disposing of a marked-down Circle stake".
   - The Annual Report records **about $100 million of noncash pre-tax gains** on its Circle investment in 2025. The gift was of an appreciated stake.
5. **CBU's OBBBA quote is unverifiable.** The source is robots-blocked and the text comes from a search index (V42B-31).
6. **Robots note** (V42B-32).
   - The BlackRock and Unum PDF URLs now redirect a standard client to q4cdn hosts whose robots.txt returns 403.
   - The study's log records a direct 200, so behaviour differs by client. Future re-reads should use the cached copies.
7. **The verdict is fairly stated overall** (V42B-33).
   - "Consistent with a modest pull-forward, not proof" matches the evidence.
   - Two phrases overreach:
     - Disclosed-motive evidence is "absent" only for the documents read, because the screen was search-based.
     - The 2026 test is useful but not decisive, because a 2026 gap fits both a prefund and a one-off gift.
8. **Propagation** (V42B-34).
   - direction-corporate-dafs.md §4 still says all four large contributions "fit a pre-floor pull-forward". It needs the correction below.
   - b41n18-01 has no floor-timing claim and needs no change.
   - The Apollo DAF row in the direction doc notes grants recommended "for the next four years". That makes Apollo a multi-year prefund in substance, but one made before the bill text.

## Notes on scope

- The industry report's earlier §11 paragraphs (including §11.38, which quotes 22.1% and 74.2%) are **not** edited. The new §11.58 carries the update.
- Wave 42A may insert §11.57 first. The §11.58 Find anchors on the source-register heading, so it applies whichever runs first.
- `research/mission-2026-11-14/b41n18-01-corporate-daf-segment.md` needs no correction. It makes no floor-timing or pull-forward claim (V42B-34).
- In the corrections below, curly quotes appear inside values. No value contains straight double quotes. A script checked that each Find occurs exactly once in its file as of 2026-11-20.

## Exact corrections

### `research/mission-2026-11-14/b4026-06-church-daf-recipients.md`

- **Find:** "Nationals send 74.2% and community foundations 3.1% [F]"
- **Replace with:** "Nationals send 74.2% and community foundations 3.1% [F]. These shares are within the top-50 frame. Across all itemising DAFRC panel sponsors plus four non-panel faith sponsors the block is $8,104.5m: faith sponsors send 30.2% (25.1% without the OJC Fund) and nationals 58.8% (b4026-06-01-faith-sponsors-outside-top50.md) [V wave 42B]"

- **Find:** "nationals about three-quarters and community foundations 3%"
- **Replace with:** "nationals about three-quarters and community foundations 3%, within the top-50 frame; across all itemising panel sponsors nationals send about three-fifths (58.8%; 63.1% without the OJC Fund) [V wave 42B]"

- **Find:** "Proposal P-B4026-06-01 would test this"
- **Replace with:** "P-B4026-06-01 tested this: 30.2% across all itemising panel sponsors (33.7% adding only faith sponsors outside the top 50). About half of the added $1,080.3m is one Brooklyn pass-through sponsor, the OJC Fund ($545.3m), which ranks 22nd by FY2023 DAF grants but 284th by DAF assets; without it the all-panel share is 25.1% [V wave 42B]"

- **Find:** "Faith sponsors send 21–26% of church dollars, against 10% of all top-50 dollars"
- **Replace with:** "Faith sponsors send 21–26% of church dollars within the top 50, against 10% of all top-50 dollars; across all itemising panel sponsors they send 30.2% of block dollars and 31.8% of church-coded dollars (25.1% of the block without the OJC Fund) [V wave 42B]"

- **Find:** "  - But **about three-quarters of church DAF dollars come from national sponsors**, led by Fidelity and DAFgiving360"
- **Replace with:** "  - But **about three-quarters of top-50 church DAF dollars come from national sponsors**, led by Fidelity and DAFgiving360; across all itemising panel sponsors the national share is about three-fifths (58.8%) [V wave 42B]"

- **Find:** "explains about a fifth to a quarter of the dollars (22.1% of the block, 25.7% of all church-coded dollars) [I] [V wave 35C]"
- **Replace with:** "explains about a fifth to a quarter of the dollars within the top 50 (22.1% of the block, 25.7% of all church-coded dollars) [I] [V wave 35C], and about three-tenths across all itemising panel sponsors (30.2% and 31.8%; b4026-06-01) [V wave 42B]"

- **Find:** "including WaterStone, NCF affiliates and most Jewish and Catholic foundations"
- **Replace with:** "including WaterStone, NCF affiliates and most Jewish and Catholic foundations (b4026-06-01 adds them: block $8,104.5m, faith share 30.2%; ranking by assets also omits high-throughput sponsors such as the OJC Fund, 22nd by FY2023 DAF grants and 284th by DAF assets) [V wave 42B]"


### `research/mission-2026-11-14/b4026-06-01-faith-sponsors-outside-top50.md`

- **Find:** "CCF-LA Supporting Organization, $139.6m (of which $103.7m goes to the Roman Catholic Archbishop of Los Angeles)"
- **Replace with:** "CCF-LA Supporting Organization, $139.6m (of which $75.9m goes to the Roman Catholic Archbishop of Los Angeles; the Archbishop's $103.7m total from faith sponsors outside the top 50 also includes about $27.8m, mostly from Catholic Community Foundation of Los Angeles) [V wave 42B]"

- **Find:** "Catholic Community Foundation (EIN 383941057), $33.5m"
- **Replace with:** "Catholic Community Foundation of Los Angeles (EIN 383941057, the one supported organisation of CCF-LA Supporting Organization), $33.5m [V wave 42B]"

- **Find:** "but its largest grant is $103.7m to the Roman Catholic Archbishop of Los Angeles. If it is Catholic, the Catholic figure would be about $230m [I]"
- **Replace with:** "but it is Catholic on its own Form 990: a Type II supporting organisation of Catholic Community Foundation of Los Angeles (EIN 383941057) whose mission is “donor advised fund granting to charities with Catholic values”. It holds one DAF account. Its largest recipient is the Archdiocese of Los Angeles ($24.0m in FY2023 and $51.9m in FY2024, $75.9m in all). Relabelled Catholic, the Catholic figure is $230.6m and the Christian $235.7m [V wave 42B]"

- **Find:** "It stays about two-thirds even without the OJC Fund (63.1% in S3) [F]"
- **Replace with:** "Without the OJC Fund it is 63.1% in S3, between three-fifths and two-thirds [F]. Two national sponsors that do not itemise Schedule I (BofA Charitable Gift Fund, Renaissance) are absent from every scenario, so all national shares are understated by an unknown amount [V wave 42B]"

- **Find:** "not in panel; Schedule D shows DAFs in column (b)"
- **Replace with:** "not in panel; Part IV line 6 is Yes, but Schedule D column (a), donor advised funds, is empty and all its accounts sit in column (b) [V wave 42B]"

- **Find:** "and its line amounts are taken as filed"
- **Replace with:** "and its line amounts are taken as filed. Re-read: its FY2023 and FY2024 Form 990s (years ending June) answer Yes to Part IV line 6 and report 4,731 and 5,976 DAFs, DAF grants of $338.3m and $385.7m against total grants of $338.9m and $390.7m (weights 0.998 and 0.987), and year-end DAF assets of only $42.5m and $34.5m. Its Schedule I line counts (3,009 and 3,410) match the cache. It is a pass-through sponsor, 22nd by FY2023 DAF grants in the DAFRC panel but 284th by DAF assets, which is why an assets-ranked top 50 omits it [V wave 42B]"


### `research/mission-2026-11-14/direction-faith-giving-platforms.md`

- **Find:** "against the faith sponsors' 10.0% of all top-50 dollars (b4026-06) [V wave 35C]"
- **Replace with:** "against the faith sponsors' 10.0% of all top-50 dollars (b4026-06) [V wave 35C]. Across all itemising DAFRC panel sponsors plus four non-panel faith sponsors, nationals send 58.8% and faith sponsors 30.2% (25.1% without the OJC Fund, a Brooklyn pass-through sponsor that sends $545.3m) (b4026-06-01) [V wave 42B]"


### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "about half of it congregations, three-quarters of it from national sponsors"
- **Replace with:** "about half of it congregations, three-quarters of it from national sponsors within the top-50 frame (about three-fifths, 58.8%, across all itemising DAFRC panel sponsors, where faith sponsors send about 30%; [b4026-06-01-faith-sponsors-outside-top50.md](b4026-06-01-faith-sponsors-outside-top50.md)) [V wave 42B]"


### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "Faith sponsors send about 22–26% of it, and none of the 14 congregation giving pages read offers a DAF option"
- **Replace with:** "Faith sponsors send about 22–26% of it within the top-50 frame and about 30% across all itemising DAFRC panel sponsors (25% without the OJC Fund), where nationals send about 59% rather than three-quarters; none of the 14 congregation giving pages read offers a DAF option [V wave 42B]"


### `research/mission-2026-11-14/direction-corporate-dafs.md`

- **Find:** "The large 2025/FY2026 contributions (Apollo $200m, Urban Outfitters $46.0m, Circle $23.1m, Zoom $20.9m) fit a pre-floor pull-forward, but **no filing gives the floor as the reason**. P-B41N18-02 tests this."
- **Replace with:** "Of the large 2025/FY2026 contributions, Apollo's $200m (Feb 2025) predates the floor's first bill text (2025-05-12), although its DAF is meant to fund about four years of grants, and Circle's $23.1m is its “first annual share contribution” under Pledge 1%, so neither is a floor pull-forward. Urban Outfitters' $46.0m fell in its last floor-free year (FY2026), and Zoom's $20.9m could not be re-read. No company read ties a DAF gift to the floor. Late-2025 gifts by BlackRock ($109m of appreciated Circle shares, 2025-12-10), Unum ($20.0m “accelerated”, recipient not named) and Live Oak fit the timing; only Community Financial System (about $0.6m, non-DAF, search-index text) names OBBBA as the reason ([b41n18-02](b41n18-02-corporate-floor-pull-forward.md)) [V wave 42B]"


### `research/mission-2026-11-14/b41n18-02-corporate-floor-pull-forward.md`

- **Find:** "BlackRock: disposing of a marked-down Circle stake"
- **Replace with:** "BlackRock: giving part of an appreciated Circle stake (its 2025 Annual Report records about $100 million of noncash pre-tax gains on its Circle investment in 2025) [V wave 42B]"

- **Find:** "Disclosed-motive evidence for a corporate *DAF* pull-forward is therefore **absent**, not weak"
- **Replace with:** "Disclosed-motive evidence for a corporate *DAF* pull-forward is therefore **absent** in the documents read, not weak; the screen was search-based and not exhaustive (§6) [V wave 42B]"

- **Find:** "   - **The decisive test is 2026:** does each late-2025 giver report little or no new charitable expense in 2026?"
- **Replace with:** "   - **A useful test is 2026:** does each late-2025 giver report little or no new charitable expense in 2026? A gap fits a prefund and a one-off gift alike, so the test is not decisive [V wave 42B]"

- **Find:** "Circle Foundation, DAF at Fidelity Charitable [R, 2026 proxy]"
- **Replace with:** "Circle Foundation, DAF at Fidelity Charitable [F: Circle blog 2025-12-02, “a donor-advised fund housed with Fidelity”; R, 2026 proxy] [V wave 42B]"

- **Find:** "2025 Annual Report PDF (`/files/` mirror)"
- **Replace with:** "2025 Annual Report PDF (`/files/` mirror; on 2026-11-20 a standard client was redirected to s24.q4cdn.com, whose robots.txt returns 403, so re-reads should use the cached copy) [V wave 42B]"

- **Find:** "2025 annual-report page and PDF"
- **Replace with:** "2025 annual-report page and PDF (on 2026-11-20 the PDF URL redirected a standard client to s201.q4cdn.com, whose robots.txt returns 403) [V wave 42B]"


### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.58 Faith sponsors outside the top 50; corporate floor timing (validated, wave 42B)\n\n**Faith sponsors outside the top 50; corporate floor timing** (validated, wave 42B). Adding every itemising DAFRC panel sponsor and four non-panel faith sponsors to the church block (church-status recipients with no e-filed 990) raises it from $6,177.5m to $8,104.5m of FY2023–24 DAF-weighted dollars. Faith sponsors then send 30.2% of block dollars, against 22.1% in the top 50, and nationals 58.8% rather than 74.2%. Faith sponsors outside the top 50 add $1,080.3m. Half of that is the OJC Fund ($545.3m), a Brooklyn pass-through DAF sponsor that ranks 22nd by FY2023 DAF grants but 284th by DAF assets; without it the faith share is 25.1% and nationals 63.1%. BofA and Renaissance do not itemise, so national shares are understated. CCF-LA's $139.6m is Catholic, and $75.9m of it, not $103.7m, goes to the Archdiocese of Los Angeles. On the corporate 1% floor (P.L. 119-21 §70426, taxable years beginning after 2025), no company read ties a DAF gift to the floor. BlackRock ($109m of appreciated Circle shares, 2025-12-10), Urban Outfitters ($46.0m) and Unum ($20.0m “accelerated”) fit the timing. Apollo's $200m predates the bill text, and Circle's gift is an annual pledge tranche (repo [`validation-wave42b-report.md`](mission-2026-11-14/validation-wave42b-report.md)) [V wave 42B]\n\n---\n\n## Source register"
