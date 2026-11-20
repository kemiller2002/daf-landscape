# Did the 2026 corporate 1% floor pull corporate DAF gifts into 2025? (P-B41N18-02)

**Date:** 2026-11-20 · **Task:** P-B41N18-02 (proposed in [direction-corporate-dafs.md](direction-corporate-dafs.md) §4 "Timing") · **Builds on:** [direction-corporate-dafs.md](direction-corporate-dafs.md), including its wave-26 governing corrections, and [b41n18-01-corporate-daf-segment.md](b41n18-01-corporate-daf-segment.md), including its wave-36A corrections. None of those corrections changes a figure used here.

**Outputs**
- [`data/mission-2026-11-14/corporate-floor-pull-forward-2026-11-20.csv`](../../data/mission-2026-11-14/corporate-floor-pull-forward-2026-11-20.csv): 9 rows. PF01–PF08 are company events and SA01 is the Fidelity Charitable aggregate.
- [`scripts/mission_b41n18_02_floor_pullforward.py`](../../scripts/mission_b41n18_02_floor_pullforward.py): builds the CSV and computes every [C] figure. Run it as `python3 -I scripts/mission_b41n18_02_floor_pullforward.py . --print`.
- [`data/mission-2026-11-14/queue-proposals-b41n18-02.csv`](../../data/mission-2026-11-14/queue-proposals-b41n18-02.csv): P-B41N1802-01 to -05.

**Labels:** **[F]** first-party text read this pass (statute, company IR site, company press page or sponsor report). **[R]** repo value carried over, or a search-index capture of a page that was not fetched. **[S]** secondary source. **[C]** computed by the script. **[I]** inference.

**Rules followed.**
- No sec.gov or congress.gov. Every company document came from the company's own investor-relations or press site.
- robots.txt was read on every host before fetching, and logged (§7). Hosts whose robots.txt did not return 200 or 404 were not fetched.
- A crawl-delay of 10 seconds was honoured on the Q4-platform IR hosts.
- The user agent was `research-script/1.0`.
- Third-party transcript sites were not fetched. Call quotes are search-index captures, labelled [R].
- This is research, not tax advice.

---

## 0. Verdict in brief

| Question | Answer | Confidence |
|---|---|---|
| **What does §70426 do?** | **The statute (P.L. 119-21 §70426), verbatim:**<br>- **Floor and cap:** corporate charitable contributions are deductible "only to the extent that the aggregate of such contributions (i) exceeds 1 percent of the taxpayer's taxable income … and (ii) does not exceed 10 percent".<br>- **Exemptions:** two categories of qualified conservation contributions (§170(b)(2)(B) and (C)).<br>- **Effective date:** "taxable years beginning after December 31, 2025".<br>- **Carryforward:** the 5-year carryforward stays (first in, first out). Amounts disallowed by the 1% floor carry forward **only from years in which the 10% cap is exceeded**. A new NOL-interaction rule reduces carryforwards.<br>- **Enacted** July 4, 2025 [F]. | High |
| **Which corporate tax year was the last one without the floor?** | **It depends on the fiscal year.**<br>- **Calendar-year companies:** the floor bites from 2026-01-01.<br>- **Companies with a January 31 year-end (Urban Outfitters, Zoom):** the floor bites from the year starting 2026-02-01, so **FY2026 (Feb 2025–Jan 2026) was their last floor-free year** [C from statute].<br>- **Accrual-basis corporations:** §170(a)(2) lets them treat a payment made by the 15th day of the 4th month after year-end as paid in the prior year, if the board authorised it in that year [F]. | High |
| **Did any company say the floor caused a 2025 DAF gift?** | **None found.** No company read this pass ties a **DAF** contribution to the floor or to OBBBA.<br>- **The only disclosed floor motive found is not a DAF case:** Community Financial System said it would "accelerate the payment of approximately $0.6 million of charitable contribution commitments in the fourth quarter of 2025" because of OBBBA limits [R: search-index capture; the company PDF was robots-blocked]. | High (for the documents read); the screen is not exhaustive (§6) |
| **Is there timing evidence?** | **Yes, it is circumstantial.** Four late-2025 corporate gifts fall in the last floor-free tax year, after enactment, and none states a tax reason:<br>- **Urban Outfitters:** $46.0m to a DAF in Q4 FY2026 [F/R].<br>- **BlackRock:** $109m of Circle shares to the BlackRock Charitable Fund on 2025-12-10, **22 days before the floor** [F, C]. The fund is called its "existing donor-advised funds" on the call [R].<br>- **Unum:** a $20.0m "**accelerated** charitable contribution" in Q4 2025, recipient not named [F].<br>- **Live Oak:** an undisclosed "allocation of funding to our donor advised fund" in Q4 2025 [R]. | Medium on timing; low on motive |
| **Do the four starting cases fit a pull-forward?** | **Only one of the four starting cases fits.**<br>- **Apollo ($200m, Feb 2025): no.** It predates the first bill text (Ways and Means, 2025-05-12) by about three months [F, S].<br>- **Circle ($23.1m): no.** It is the "first annual share contribution" of a Pledge 1% schedule, i.e. scheduled and recurring [F].<br>- **Zoom ($20.9m, FY2026): unverified.** It draws on a share reserve set in FY2020 [R], and Zoom's IR site is robots-blocked.<br>- **Urban Outfitters: timing-consistent.** It fell in its last floor-free year, and management said it will fund "charitable initiatives in the coming years" [R]. That describes a multi-year prefund, but it gives no tax reason. | Medium |
| **Sponsor-side signal (Fidelity Charitable 2026 report, covering 2025)?** | **Weak.**<br>- Corporate DAFs rose **7.3%** (518 to 556) and corporate grants **2.8%** ($525M to $539.8M) [C]. Fidelity's DAFs overall rose **13.4%** [F].<br>- **No corporate contribution figure is published**, so a 2025 corporate inflow spike cannot be seen [F].<br>- The report credits *overall* account growth to "bunching donations in the face of tax law changes that took effect in 2026"; it says nothing comparable for corporate accounts [F]. | High (published); uninformative on contributions |
| **Overall verdict** | **The evidence is consistent with a modest corporate pull-forward into late 2025, but it is not proof of one.**<br>- There is no disclosed floor motive for any corporate DAF gift.<br>- There is one disclosed OBBBA motive for a small non-DAF prepayment.<br>- Several large late-2025 gifts fit the timing; one calls itself "accelerated" and one is described as a multi-year prefund.<br>- Two of the four starting cases are not pull-forwards (Apollo, Circle).<br>[I] A 2026 test (§5) can separate prefunds from recurring gifts. | [I] |

---

## 1. The statute (P.L. 119-21 §70426), verified

Source: govinfo, Public Law 119-21, HTML ([P01](https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm)), 139 Stat. 237–238, "Approved July 4, 2025". The current §170 text was checked on Cornell LII ([P02](https://www.law.cornell.edu/uscode/text/26/170)).

| Element | Text or effect | Label |
|---|---|---|
| **Floor rate** | **1 percent.** §170(b)(2)(A)(i): the aggregate of contributions must "exceed 1 percent of the taxpayer's taxable income for the taxable year". | F |
| **Base** | **The corporation's taxable income**, as defined for §170(b)(2), with its existing modifications. | F |
| **Cap** | **10 percent of taxable income**, unchanged (§170(b)(2)(A)(ii)). | F |
| **Excluded contributions** | Subparagraphs (B) and (C) are outside the floor: qualified conservation contributions by certain corporate farmers and ranchers, and by Alaska Native Corporations. | F |
| **Effective date** | §70426(d): "shall apply to taxable years beginning after December 31, 2025". | F |
| **Carryforward (general)** | Amounts over the 10% cap carry forward to later years, behind the current year's contributions. | F (§170(d)(2)(A)) |
| **Carryforward (5 years)** | No carryforward past the fifth year after the year of contribution, with contributions "treated as allowed on a first-in first-out basis". | F (§170(d)(2)(B)) |
| **Carryforward (floor amounts)** | "Contributions disallowed by 1-percent floor carried forward only from years in which 10 percent limitation is exceeded". In other years the floor amount is lost. | F (§170(d)(2)(C)) |
| **Carryforward (NOL interaction)** | A carryforward is reduced to the extent it would reduce taxable income and increase an NOL carryover. | F (§170(d)(2)(D)) |
| **Accrual-basis timing (existing law)** | The corporation may elect to treat a payment as paid in the prior year when two conditions hold. The board must authorise the contribution during that year. Payment must follow "on or before the 15th day of the fourth month following the close of such taxable year". | F (§170(a)(2)) |
| **Legislative timeline** | Ways and Means tax title released 2025-05-12 and reported 2025-05-14 (26-19) [S]; enacted 2025-07-04 [F]. | F / S |

**Why a DAF prefund helps under the floor [I]:**
- Under the floor, the first 1% of taxable income given each year is not deductible, unless the 10% cap is exceeded.
- A company that put several years of planned giving into a DAF in its last floor-free year deducts all of it without the floor. The later grants from the DAF are not new corporate contributions.
- Bunching gifts into a single later year also works, because the floor is then lost only once. So the floor rewards lumpiness in any year, not only 2025.
- Under the 10% cap, the largest prefund that is fully deductible in one year is 10% of taxable income. Above that, the excess carries forward into floor years.

---

## 2. Method

1. **Statute:** the §70426 text was taken from govinfo P.L. 119-21 HTML and cross-checked against Cornell LII 26 U.S.C. §170 (§1).
2. **Starting four companies (repo CD01, CD02, CD04, CD06):** each was looked up on the company's own IR or press site.
   - **Apollo:** ir.apollo.com hosts the company's 10-K, 10-Q and earnings-release HTML. Read: 10-K 2024 and 2025, the 1Q25 earnings release, and 10-Qs Q1–Q3 2026.
   - **Circle:** circle.com pressroom and blog. Read: Q4 2025, Q1–Q3 2026 releases and the 2025-12-02 Foundation announcement.
   - **Urban Outfitters:** the company blog copy of its FY26 Q4 release (urbn.com).
   - **Zoom:** blocked (§7).
3. **Other companies:** web searches for 2025 corporate DAF or charitable contributions that are paired with OBBBA, the 2026 floor, "accelerated" or "tax law changes". Each candidate was then read on its own IR site:
   - BlackRock: 2025 Annual Report on ir.blackrock.com.
   - Unum: 2025 Annual Report on investors.unum.com.
   - Live Oak: Q4 2025 release on investor.liveoak.bank.
   - Community Financial System: its PDF host was blocked, so it is labelled [R].
4. **Sponsor side:** Fidelity Charitable 2026 and 2025 Giving Reports (PDF, `pdftotext`) and its corporate-giving page.
5. **Coding:** each event was classed on two separate axes:
   - **disclosed motive:** whether the company names the floor, OBBBA or tax-law timing as the reason;
   - **timing:** last floor-free year, before or after the bill text and enactment, scheduled vs single.
6. **Derived figures [C]:** the script computes contribution as a share of GAAP pre-tax income, as a share of net income, days before the floor, tax-benefit rate and Fidelity growth rates.
   - GAAP pre-tax income is **not** taxable income (consolidation, foreign income, book-tax differences), so the shares are only an indication of scale [I].

---

## 3. Results: company events (CSV PF rows)

| ID | Company | When | Amount | Vehicle | Disclosed motive | Floor/OBBBA named? | Timing class |
|---|---|---|---|---|---|---|---|
| PF01 | **Urban Outfitters** | Q4 FY2026 (Nov 2025–Jan 2026); floor starts 2026-02-01 | **$46.0m** [R: repo 10-K row; release text read] | DAF, sponsor not named | Release: adjusted results exclude "a charitable contribution to a donor-advised fund" [F]. Call: "We intend to use this fund to support our charitable initiatives in the coming years" [R] | No | **Timing-consistent:** last floor-free year, and a multi-year prefund in substance |
| PF02 | **Apollo** | Feb 2025 | **$200m**, 1,213,003 new shares [F] | "Apollo DAF", sponsor not named | "as part of its ongoing commitment to philanthropy" [F] | No (OBBBA cited only for CFC rules) | **Not floor-driven [I]:** about 3 months before the bill text. No issuance in 9M 2026: the cash-flow line "Issuance of common stock to donor-advised fund" shows "—" for 9M 2026 against $200m for 9M 2025 [F] |
| PF03 | **Zoom** | FY2026 (Feb 2025–Jan 2026) | **$20.9m** in shares [R] | DAF at an "unaffiliated nonprofit organization" [R] | not read (IR robots.txt 403) | unknown | **Unverified:** draws on a reserve set in FY2020 [R] |
| PF04 | **Circle** | Nov 2025 [R] | **$23.1m** charge [R]; release text: "$23 million charge related to our first annual share contribution to the Circle Foundation" [F] | Circle Foundation, DAF at Fidelity Charitable [R, 2026 proxy] | "Seeded by Circle's Pledge 1% equity commitment" [F] | No | **Scheduled annual pledge, not a pull-forward [I].** Q1–Q3 2026 release narratives name no Foundation charge; the tables are images and were not read [F] |
| PF05 | **BlackRock** | **2025-12-10** (22 days before the floor) [F, C] | **$109m** expense, $29m tax benefit (26.6%) [F, C] | "BlackRock Charitable Fund, which BlackRock established in 2013"; called "existing donor-advised funds" on the call [R] | "will add to the long-term funding for BlackRock's philanthropic grants and programs"; "nonrecurring" [F] | No (OBBBA cited only for the TCJA extension and international rules) | **Timing-consistent:** in-kind Circle shares, in the last floor-free weeks |
| PF06 | **Unum** | Q4 2025 | **$20.0m** pre-tax, $15.8m after tax ($4.2m benefit, 21.0%) [F, C] | not named | "an expense related to an **accelerated** charitable contribution" [F]. Separately, 2025 giving to causes was "$14.8 million in charitable contributions" [F] | OBBBA: "We do not expect the OBBBA to have a material impact"; not linked to the gift [F] | **Self-described acceleration; motive unstated** |
| PF07 | **Community Financial System** | Q4 2025 (announced in Q3 release) | **≈$0.6m** [R] | direct prepayment of commitments, **not a DAF** | "As a result of tax law changes enacted under the One Big Beautiful Bill Act that limit the deductibility of charitable contributions beginning in 2026, the Company plans to accelerate…" [R] | **Yes** | **Disclosed floor motive (non-DAF)** |
| PF08 | **Live Oak Bancshares** | Q4 2025 | not disclosed | company DAF [R] | Call: "allocation of funding to our donor advised fund", one of about $11m of offsets [R]. The release has no DAF line [F] | No | **Timing-consistent, unverified** |

**Scale [C]:** contribution as a share of GAAP pre-tax income. Because the floor is 1% of taxable income, the same figure also reads as a multiple of the floor.
- Apollo: **3.00%** (3.0× a 1% floor proxy). Not relevant to the floor (it predates the bill).
- Unum: **2.14%** (2.1×).
- BlackRock: **1.43%** (1.4×).
- Urban Outfitters: **9.89% of net income** ($46.0m ÷ $464.9m). Pre-tax income was not read (the tables are not in the blog copy), and the share of pre-tax income is lower.
- **[I]** On that proxy, the late-2025 gifts equal roughly one to two years of the floor for BlackRock and Unum. If URBN's taxable income is near its pre-tax income, its gift is near the 10% cap. That is the largest gift that is fully deductible in one year.

**Disclosed motive versus timing, kept separate:**
- **Disclosed floor/OBBBA motive:** 1 event (PF07, a ≈$0.6m non-DAF prepayment) [R].
- **Disclosed non-tax motive, timing consistent:** PF01, PF05.
- **Self-described "accelerated" with no reason:** PF06.
- **Timing consistent, unverified:** PF08.
- **Not a pull-forward:** PF02 (before the bill text) and PF04 (a scheduled annual pledge).
- **Unverified:** PF03.

---

## 4. Results: sponsor side (CSV SA01)

**Fidelity Charitable, 2026 Giving Report (covering 2025) against the 2025 report (covering 2024) [F]:**

| Metric | 2024 | 2025 | Change [C] |
|---|---|---|---|
| Corporate DAFs | 518 | 556 | **+7.3%** |
| Corporate grant dollars | $525M | $539.8M | **+2.8%** |
| Corporate grant volume | 24,975 | 26,036 | +4.2% |
| All Fidelity DAFs | n/r | 246,006 | **+13.4%** ("as some donors took advantage of strategies like bunching donations in the face of tax law changes that took effect in 2026") |
| Corporate contributions | **not published** | **not published** | — |

- **Reading [I]:** grants and account counts lag contributions, so this table cannot show a 2025 corporate inflow.
- Corporate account growth (7.3%) trailing all-account growth (13.4%) is weak evidence *against* a large rush to open new corporate accounts at Fidelity. It says nothing about top-ups to existing accounts.
- The +4.2% grant-volume change is computed from the 2025 report's 24,975 and the 2026 report's 26,036.
- The corporate-giving page carried a generic banner, "Time is running out to make tax-deductible contributions in 2026", and no floor-specific text [F].
- **Fidelity's 2027 report, covering 2026, is not yet published.** No other sponsor publishes a corporate contribution split ([b41n18-01](b41n18-01-corporate-daf-segment.md)).

---

## 5. Verdict

1. **Disclosed motive.**
   - No public company read this pass says that the 2026 corporate floor or OBBBA caused a **DAF** contribution.
   - One bank (CBU) says OBBBA caused a small **direct** prepayment of commitments [R].
   - Disclosed-motive evidence for a corporate *DAF* pull-forward is therefore **absent**, not weak.
2. **Timing.**
   - Late 2025 shows several large, one-off corporate gifts in the last floor-free tax year, after enactment: BlackRock $109m (22 days before the floor), Urban Outfitters $46.0m, Unum $20.0m "accelerated", and Live Oak undisclosed.
   - Their timing is what a floor-driven prefund predicts. Each also has an ordinary explanation:
     - BlackRock: disposing of a marked-down Circle stake;
     - URBN: a record year;
     - Unum: an unexplained "acceleration".
   - [I] Timing alone cannot separate these explanations.
3. **The starting four.**
   - Apollo's $200m predates the floor's first public text, so it is a **coincidence** of timing.
   - Circle's is a **scheduled** Pledge 1% annual tranche.
   - Zoom's could not be read.
   - Only Urban Outfitters is a plausible pull-forward, and it gives no tax reason.
   - The repo's earlier framing, "The large 2025/FY2026 contributions (Apollo $200m, Urban Outfitters $46.0m, Circle $23.1m, Zoom $20.9m) fit a pre-floor pull-forward", should be narrowed: **two of the four do not fit** (§8).
4. **Sponsor side.** Fidelity publishes no corporate contribution series, and its corporate account growth trailed overall growth. **No sponsor-side evidence** of a corporate pull-forward exists yet [F].
5. **Overall [I].** It is plausible, but not demonstrated, that the floor pulled some corporate giving into late 2025. The amounts identified are small against corporate DAF flows (Fidelity corporate grants alone: $539.8M in 2025).
   - **The decisive test is 2026:** does each late-2025 giver report little or no new charitable expense in 2026? Apollo already shows none through September 2026, though its gift is not floor-linked.
   - **The other decisive data are sponsor corporate contributions for 2025 and 2026** (P-B41N1802-01, -03).

---

## 6. Limits

- **IR hosts blocked:** investor.urbn.com, urbanoutfittersinc.gcs-web.com, investors.zoom.us and every Q4 CDN host (s201, s204, s206, s24.q4cdn.com) returned 403 for robots.txt, so they were not fetched.
  - Zoom's row and the Urban Outfitters amount therefore rest on repo values from the earlier pass.
  - CBU's quote is a search-index capture.
  - ir.cbna.com gave a proxy 502 and businesswire.com timed out.
- **Not exhaustive:** the "other companies" screen used web search, not a systematic text screen of filings. EDGAR full-text search is off-limits (efts.sec.gov robots 403, wave 26; sec.gov excluded by rule). Companies that disclosed a floor-motivated DAF gift may exist and not have surfaced (P-B41N1802-04).
- **Not fetched:** call transcripts on third-party sites (one fetch attempt was refused by this session's permission policy and was not retried). Quotes from calls (URBN, BlackRock vehicle description, Live Oak, CBU) are [R].
- **Unconfirmed vehicles:** Unum's recipient and form are not stated. BlackRock's "Charitable Fund" is described as a DAF only on the call [R]. Circle's 2026 tables are images.
- **Taxable income is not public.** GAAP pre-tax income is a rough proxy, and the "multiple of the 1% floor" figures are indicative only.
- **Not observed:** §170(a)(2) accrual elections (early-2026 payments deducted in 2025) cannot be seen in public reports (P-B41N1802-05).
- **Not reached:** the URBN FY2027 and FY2026-Q3 releases. Guessed urbn.com slugs returned a generic page, and no sitemap was found (404).
- **Scope:** private companies, the main users of SVCF and Tides corporate funds, are not covered.

---

## 7. robots.txt and fetch log (2026-11-20)

| Host | robots.txt | Fetched |
|---|---|---|
| www.govinfo.gov | 200, allows path | P.L. 119-21 HTML |
| www.law.cornell.edu | 200, allows path | 26 U.S.C. §170 |
| ir.apollo.com | 200 (`Disallow: /form-submit` only) | sitemap; 5 press-release pages; 1Q25 earnings release; 10-K 2024, 10-K 2025; 10-Q Q1–Q3 2026; SEC-filings and financial-results index pages |
| www.circle.com | 200, allows | Q4 2025 and Q1–Q3 2026 releases; Foundation blog post |
| www.urbn.com | 404 (treated as allow) | FY26 Q4 release (blog); 3 guessed slugs returned a generic page; sitemap 404 |
| ir.blackrock.com | 200, `Allow: /`, crawl-delay 10 | annual-reports page, quarterly-results page, 2025 Annual Report PDF (`/files/` mirror) |
| investors.unum.com | 200, `Allow: /`, crawl-delay 10 | quarterly-results and SEC-filings pages; 2025 annual-report page and PDF; one guessed news URL returned 404 |
| investor.liveoak.bank | 200, `Allow: /`, crawl-delay 10 | Q4 2025 release |
| www.fidelitycharitable.org | 200, allows | 2026 and 2025 Giving Reports; corporate-giving page |
| investor.urbn.com; urbanoutfittersinc.gcs-web.com; investors.zoom.us; s201/s204/s206/s24.q4cdn.com | **403** | not fetched |
| ir.cbna.com | proxy 502 | not fetched |
| www.businesswire.com | timeout | not fetched |
| sec.gov, congress.gov | not used (rule) | — |

---

## 8. Proposed corrections to existing repo text (not governing until validated)

1. **[direction-corporate-dafs.md](direction-corporate-dafs.md) §4, "Timing [I]".**
   - **Find:** "The large 2025/FY2026 contributions (Apollo $200m, Urban Outfitters $46.0m, Circle $23.1m, Zoom $20.9m) fit a pre-floor pull-forward, but **no filing gives the floor as the reason**. P-B41N18-02 tests this."
   - **Replace with:** "Of the large 2025/FY2026 contributions, Apollo's $200m (Feb 2025) predates the floor's first bill text (2025-05-12), and Circle's $23.1m is the first tranche of an annual Pledge 1% schedule, so neither is a pull-forward. Urban Outfitters' $46.0m fell in its last floor-free year (FY2026), and Zoom's $20.9m could not be re-read. No company ties a DAF gift to the floor. Late-2025 gifts by BlackRock ($109m, 2025-12-10), Unum ($20.0m 'accelerated') and Live Oak fit the timing, and only Community Financial System (≈$0.6m, non-DAF) names OBBBA as the reason ([b41n18-02](b41n18-02-corporate-floor-pull-forward.md))."
2. **[direction-policy-lobbying-obbba.md](direction-policy-lobbying-obbba.md) §3 provisions table, "Corporate 1% floor" row.**
   - **Append:** "Effective for taxable years beginning after 2025, so corporations with a January year-end (e.g. URBN, Zoom) had a floor-free FY2026 running to 2026-01-31. §170(a)(2) lets accrual-basis corporations deduct in 2025 a contribution authorised in 2025 and paid by 2026-04-15 ([b41n18-02](b41n18-02-corporate-floor-pull-forward.md) §1)."

---

## Source register

| ID | Source | Date | Used for | Label |
|---|---|---|---|---|
| P01 | [P.L. 119-21, govinfo HTML](https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm), §70426 (139 Stat. 237–238) | 2025-07-04 | floor, base, effective date, carryforward | F |
| P02 | [26 U.S.C. §170, Cornell LII](https://www.law.cornell.edu/uscode/text/26/170) | live 2026-11-20 | current §170(b)(2), §170(a)(2), §170(d)(2) | F |
| S01 | [KPMG: Ways and Means approves tax title](https://kpmg.com/us/en/taxnewsflash/news/2025/05/ways-means-approves-tax-title-provisions-would-affect-tax-exempts.html); [Crowe: Ways and Means markup](https://www.crowe.com/insights/tax-news-highlights/house-ways-and-means-approves-markup) | 2025-05 | bill-text date (2025-05-12), committee vote | S (search-index) |
| C01 | [Apollo 10-K 2025 (IR copy)](https://ir.apollo.com/sec-filings/content/0001858681-26-000013/apo-20251231.htm) | 2026 | $200m, 1,213,003 shares, Feb 2025; OBBBA text | F |
| C02 | [Apollo 10-K 2024 (IR copy)](https://ir.apollo.com/sec-filings/content/0001858681-25-000034/apo-20241231.htm) | 2025 | "establishing a new donor-advised fund … ongoing commitment to philanthropy" | F |
| C03 | [Apollo 1Q25 earnings release (IR copy)](https://ir.apollo.com/sec-filings/content/0001858681-25-000045/agmearningsrelease1q2025.htm) | 2025-05-02 | "previously announced donor-advised fund", $200m | F |
| C04 | [Apollo 10-Q Q3 2026 (IR copy)](https://ir.apollo.com/sec-filings/content/0001858681-26-000067/apo-20260930.htm); Q1 ([link](https://ir.apollo.com/sec-filings/content/0001858681-26-000026/apo-20260331.htm)), Q2 ([link](https://ir.apollo.com/sec-filings/content/0001858681-26-000040/apo-20260630.htm)) | 2026 | no DAF issuance in 9M 2026 | F |
| C05 | [Circle Q4 / FY2025 results](https://www.circle.com/pressroom/circle-reports-fourth-quarter-and-full-fiscal-year-2025-financial-results); Q1–Q3 2026 releases ([Q1](https://www.circle.com/pressroom/circle-reports-first-quarter-2026-results), [Q2](https://www.circle.com/pressroom/circle-reports-second-quarter-2026-results), [Q3](https://www.circle.com/pressroom/circle-reports-third-quarter-2026-results)) | 2026 | "first annual share contribution"; 2026 narratives | F |
| C06 | [Circle Foundation announcement](https://www.circle.com/blog/announcing-the-circle-foundation-building-financial-resilience-for-all) | 2025-12-02 | Pledge 1% seeding | F |
| C07 | [URBN FY26 Q4 release (company blog)](https://www.urbn.com/blog/fy26-q4-results) | 2026-02-25 | DAF contribution excluded from adjusted results; FY net income $464.9m | F |
| C08 | URBN Q4 FY2026 call (quote via search index; transcript not fetched), e.g. [Insider Monkey listing](https://www.insidermonkey.com/blog/urban-outfitters-inc-nasdaqurbn-q4-2026-earnings-call-transcript-1708112/) | 2026-02 | "support our charitable initiatives in the coming years" | R |
| C09 | [BlackRock 2025 Annual Report (IR mirror)](https://ir.blackrock.com/files/doc_financials/2026/ar/BLK_AR25.pdf) | 2026 | 2025-12-10 Circle-stake contribution, $109m / $29m, pre-tax income $7,619m | F |
| C10 | BlackRock Q4 2025 call (quote via search index), e.g. [Yahoo summary](https://finance.yahoo.com/news/blackrock-q4-earnings-call-highlights-152737812.html) | 2026-01-15 | "existing donor-advised funds" | R |
| C11 | [Unum 2025 Annual Report (IR)](https://investors.unum.com/files/doc_financials/2025/Unum-Group-2025-Annual-Report.pdf) | 2026 | $20.0m accelerated contribution, $15.8m after tax, OBBBA statement, $14.8m giving, pre-tax income $933.5m | F |
| C12 | [Live Oak Q4 2025 release (IR)](https://investor.liveoak.bank/news/news-details/2026/Live-Oak-Bancshares-Inc--Reports-Fourth-Quarter-2025-Results/default.aspx) | 2026-01-21 | no DAF line; pre-tax income $142.8m | F |
| C13 | Live Oak Q4 2025 call (quote via search index), e.g. [Insider Monkey listing](https://www.insidermonkey.com/blog/live-oak-bancshares-inc-nyselob-q4-2025-earnings-call-transcript-1680143/) | 2026-01 | "allocation of funding to our donor advised fund" | R |
| C14 | [Community Financial System Q3 2025 release (company PDF, robots-blocked)](https://s204.q4cdn.com/276330220/files/doc_news/Community-Financial-System-Inc--Reports-Third-Quarter-2025-Results-2025.pdf) | 2025-10-21 | OBBBA-motivated ≈$0.6m prepayment | R (search-index text) |
| C15 | [Zoom FY2026 release (IR, robots-blocked)](https://investors.zoom.us/node/14156/html); repo row CD06 | 2026-02-25 | $20.9m (repo), non-GAAP exclusion (search-index) | R |
| D01 | [Fidelity Charitable 2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) | 2026 | 2025 corporate DAFs, grants; bunching statement | F |
| D02 | [Fidelity Charitable 2025 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) | 2025 | 2024 baseline (518 DAFs, $525M) | F |
| D03 | [Fidelity corporate-giving page](https://www.fidelitycharitable.org/corporate-giving.html) | live 2026-11-20 | no floor-specific text | F |
| R01 | [`corporate-daf-programs-2021-2026.csv`](../../data/mission-2026-11-14/corporate-daf-programs-2021-2026.csv) rows CD01, CD02, CD04, CD06 | 2026-11-15 | URBN, Zoom, Circle amounts | R |

---

## Data dictionary: `corporate-floor-pull-forward-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_id | PFnn = company event; SA01 = sponsor aggregate (Fidelity Charitable) |
| company, ticker | Issuer |
| fiscal_year | `calendar` or `fye_jan31` (fiscal year ends 31 January) |
| floor_first_applies | First day of the first tax year the 1% floor applies to [C from §70426(d)] |
| contribution_period | Fiscal quarter or year of the gift as reported |
| contribution_date | Exact date (YYYY-MM-DD) where stated; month or blank otherwise |
| days_before_floor | floor_first_applies minus contribution_date, in days, where the exact date is known [C] |
| timing_vs_bill | Before Ways and Means text (2025-05-12), or after enactment (2025-07-04) in the last floor-free year [C] |
| amount_usd | Contribution amount (expense or charge) in USD |
| amount_label | F = read this pass; R = repo value or search-index capture |
| vehicle | Recipient as described (DAF, named fund, not named) |
| form | Cash, shares or in-kind as stated |
| cadence | Single, scheduled or recurring, as stated |
| pretax_income_usd | GAAP income before income taxes for the same fiscal year, where read [F] |
| net_income_usd | GAAP net income, where read (Zoom's is a search-index value [R]) |
| contribution_pct_pretax | amount ÷ pre-tax income × 100 [C] (taxable-income proxy only) |
| contribution_pct_net_income | amount ÷ net income × 100 [C] |
| multiple_of_1pct_pretax | amount ÷ (1% of pre-tax income) [C]. Numerically equal to contribution_pct_pretax; read it as "years of floor covered" [I] |
| tax_benefit_usd, tax_benefit_rate_pct | Tax benefit stated by the company, and benefit ÷ amount × 100 [C] |
| disclosed_motive | The company's own stated reason, quoted |
| mentions_floor_or_obbba | Whether the disclosure ties the gift to the floor or OBBBA (Y/N, with context) |
| followup_2026 | What 2026 reports show about a repeat contribution |
| evidence_class | `disclosed_floor_motive_non_daf`, `self_described_acceleration_motive_unstated`, `timing_consistent_no_stated_tax_motive`, `timing_consistent_unverified`, `predates_proposal_not_floor_driven`, `scheduled_annual_pledge_not_pull_forward`, `unverified_legacy_program`, `sponsor_aggregate_no_contribution_split` |
| label | Evidence label(s) for the row |
| source_url | Primary company or sponsor URL |
| access_note | robots.txt and fetch notes |
