# Queue batch 31 B: Endaoment FY2025 Form 990 (P-B30B-02), Every.org's 990-PF years and reclassification (P-INF-07), aggregator sync of Fidelity Charitable (P-B30A-01), adviser data feeds at GS PF, MS GIFT, BofA CGF and NPT (P-QA3-03)

**Date:** 2026-11-15.

**Method:**
- Public sources only, 2021 onward. No accounts were created, no logins were used, no forms were submitted and nobody was contacted.
- IRS sources: e-file index, TEOS XML zips and the EO Business Master File (BMF).
- The Endaoment XML was pulled from the IRS zip with HTTP range requests, reading only the one zip member. The member is Deflate64-compressed, so it was inflated with `unzip`. The scripts are stdlib Python in the session scratchpad and are not part of the repo.
- First-party help centres were read through their public Zendesk JSON. First-party PDFs were read with `pdftotext`. The IRS letter is image-only and was read by OCR (`tesseract`), so quotes from it are transcriptions.
- Integration directories were read from their public pages: the Addepar Integration Center and Intuit's FI directory.

**Builds on, and applies the governing corrections of:**
- [queue-batch30-everyorg-givinga-goodstack.md](queue-batch30-everyorg-givinga-goodstack.md), including wave-15 corrections 1–5. For example, Every.org's 990-PF deferred revenue is not like-for-like with its audited customer deposits.
- [queue-batch30-legal-circulars.md](queue-batch30-legal-circulars.md) §4–5, including wave-15 corrections 1–5.
- [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md), including its wave-9 corrections.
- [queue-bank-programs-and-eft-providers.md](queue-bank-programs-and-eft-providers.md) §1 "Adviser data feeds", and its corrections.

**Evidence tags:**
- **[F]** fact from a cited primary source.
- **[C]** calculation from cited inputs.
- **[I]** inference by this agent.
- **[R]** search-index snippet only; the page was not read.
- **[S]** secondary source.
- **[U]** not found.

**This is research, not legal or tax advice.**

**Outputs:**
- This file.
- [data/mission-2026-11-14/sponsor-data-feeds-2026.csv](../../data/mission-2026-11-14/sponsor-data-feeds-2026.csv): 22 rows.
- [data/mission-2026-11-14/queue-proposals-batch31b.csv](../../data/mission-2026-11-14/queue-proposals-batch31b.csv): P-B31B-01..03.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B30B-02** Endaoment FY2025 | **Retrieved.** The FY2025 Form 990 (FYE 2025-06-30; ReturnTs 2026-05-15; prepared by Forvis Mazars) reports **1,213 DAFs**, $25,033,424 of contributions, $18,679,151 of grants and an EOY value of $18,900,000 [F].<br>• That count is about one-fifth of FY2024's **6,000** [F]. With FY2023 also unreported, this makes **the FY2024 count an outlier** [I]. **FY2025 is the best-evidenced Endaoment count.**<br>• DAFRC's imputed FY2024 row (425 DAFs, $23.8m) is wrong on every field against the FY2024 e-file [C].<br>• Crypto: 100% of Part VIII contributions ($24.33m) are noncash "CRYPTO ASSET", across 1,430 contributions (Schedule M) [F]. Year-end program-related investments are $18.31m of "Crypto Assets" plus $0.60m held at "Fidelity Investments" [F].<br>• Contractors: one over $100k, SingerLewak (accounting, $111,519). Part IX "Contractor expense" is $140,000 [F].<br>• Program-service revenue is $699,614, and it equals the difference between Schedule D contributions and Part VIII contributions [C].<br>• The return has an unexplained **prior-period adjustment of −$2,495,535** [F]. | High (primary XML) |
| **P-INF-07** Every.org | **Why 990-PF:** Every.org was a private foundation in a **60-month termination under IRC 507(b)(1)(B)**. IRS instructions require Form 990-PF "for each year in the 60-month termination period" [F].<br>• IRS Letter 4422 of 2025-10-23 says the IRS "determined you terminated your private foundation status under … 507(b)(1)(B)" and "reclassified you as of **January 1, 2020** as a public charity" under **170(b)(1)(A)(vi)** [F, OCR]. The BMF agrees: foundation code 15, ruling 202510, Form 990 filing requirement 01, 990-PF requirement 0 [F].<br>• **What changed:**<br>  1. The reclassification is retroactive to 2020, so gifts from 2020 to 2024 count as gifts to a public charity, with 60%/30% AGI limits and fair-market value for appreciated property, including crypto [I from statute].<br>  2. The 4940 excise tax paid ($891 for 2023, $9,853 for 2024) becomes refundable on a timely claim [F instructions; claim not seen].<br>  3. **Donor names stop being public.** Every 990-PF Schedule B named its ≥$5k contributors (530 in CY2024); Form 990 Schedule B names are not public [F].<br>  4. The first Form 990, for CY2025, will carry Schedule D [F].<br>• **New tension:** since 2026-09 Every.org accepts **IRA QCDs, including to fund a "giving credit" balance**. QCDs cannot go to a DAF (IRC 408(d)(8)(B)(ii)), so the DAF question for these balances is now live [I]. | High on why; medium on consequences (law applied, no IRS guidance on Every.org) |
| **P-B30A-01** Fidelity Charitable aggregation | **Yes, on the adviser side; partially on the consumer side.**<br>• **Addepar's live Integration Center** lists a portfolio data feed "Fidelity Investments: Charitable Gift Fund/Donor-Advised Fund" (last updated **2026-09-09**). It "Requires Fidelity advisory relationship with G-Number" [F]. Fidelity Charitable's adviser page confirms the G-Number link to Giving Accounts [F].<br>• **Empower Personal Dashboard** (article updated **2025-12-06**) tells users to re-link Giving Accounts "under the 'Fidelity Charitable' option" because they no longer sync under the Fidelity Investments OAuth option [F]. The method behind that option is not disclosed [U].<br>• **eMoney** (Fidelity-owned) lists "Fidelity Charitable sites" among institutions migrated to API connections. The post is undated, c.2023 [F; date I].<br>• **Morningstar ByAllAccounts** moved FI 44892 to Akoya in 2023 [F, 2023], and Morningstar sold ByAllAccounts in 2026 [S]. Current Fidelity Charitable status: [U].<br>• **Intuit's FI directory** (Quicken/QuickBooks, generated 2026-11-15) has **no Fidelity Charitable entry** [F, absence]. Its only DAF-programme entry is T. Rowe Price's charitable programme on a Ren `donorfirstx.com` host [F].<br>• Plaid, Yodlee, Monarch and Simplifi: no Fidelity Charitable status was found [U]. | High on Addepar, Empower and Intuit; low on the consumer apps |
| **P-QA3-03** GS PF, MS GIFT, BofA CGF, NPT | **None publishes an API, a file feed or an aggregator listing for DAF accounts.**<br>• **The integrations are portal embeds and single sign-on:**<br>  – BofA CGF: balances, top charities and grants appear in MyMerrill and Private Bank Account Access (repo, [F]).<br>  – MS GIFT: donors use Morgan Stanley Online and advisers use "3D", with no separate credentials [F, Ren FAQ].<br>  – GS PF: "Login with Goldman.com" (repo, [F]).<br>  – NPT: "online access, SSO" and private-label views for institutions, plus full or read-only financial-adviser access [F].<br>• **Addepar** lists custodial feeds for GS PWM, Morgan Stanley GWM (brokerage and investment accounts; branch approval), BofA Private Bank and Merrill PWM. **None names a DAF or charitable account type**, unlike the Fidelity Charitable feed [F].<br>• Where MS GIFT and BofA CGF assets sit in MSSB or Private Bank accounts, those custodial feeds *may* carry them [I, untested].<br>• **Contractual data rights:** none found. The terms read are view and statement rights only (repo). | Medium-high on absence in public docs; low on what custodial feeds actually include |

---

## 1. P-B30B-02: Endaoment FY2025 Form 990

### 1.1 Retrieval [F]

- IRS index row: `24678508,EFILE,844661797,202506,2026,Endaoment Inc,990,93493135159786,202631359349315978,2026_TEOS_XML_05A` ([index_2026.csv](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv)).
- **The member is not in `2026_TEOS_XML_05A.zip`.** That zip holds 84,172 members ending at 2026213…; the index assigns 168,344 rows to the "05A" batch.
- The member is in **[`2026_TEOS_XML_05B.zip`](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip)** (513,423,358 bytes), at local offset 298,203,445. It is Deflate64 (method 9), 14,650 bytes compressed and 105,932 uncompressed.
- **[I]** The index's "05A" batch label covers both the 05A and 05B zips. Future pulls of "05A" objects should try 05B as well.
- The GivingTuesday mirror still returns 404 for `202631359349315978_public.xml`.

### 1.2 Schedule D Part I and comparison [F]/[C]

| FY (June YE) | Object | DAFs | Contributions | Grants | EOY value | Avg value per DAF [C] |
|---|---|---|---|---|---|---|
| 2022 | 202323209349303992 | 331 | $43,237,525 | $24,976,644 | $15,309,881 | $46,253 |
| 2023 | 202411369349317486 | not reported | — | — | — | — |
| 2024 | [202542899349300104](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542899349300104_public.xml) | 6,000 | $36,361,819 | $34,818,019 | $17,112,374 | $2,852 |
| **2025** | **202631359349315978** (IRS zip 05B) | **1,213** | **$25,033,424** | **$18,679,151** | **$18,900,000** | **$15,581** |
| DAFRC FY2024 ("Imputed") | [dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | 425 | $52,812,015 | $30,840,700 | $23,816,741 | $56,039 |

- **Reading [I]:**
  - The count goes 331, then not reported, then 6,000, then 1,213. FY2025 has 1,430 crypto contributions (Schedule M), which fits about 1,200 funds. FY2024's Schedule M count field is 0, so it gives no check on the 6,000.
  - The round 6,000 is the outlier. The FY2025 count is the better-evidenced one. Use 1,213 for FY2025 and keep FY2024's 6,000 flagged "round; contradicted by FY2025".
  - **No amended FY2024 return** is in the 2025 or 2026 index [F].
- The FY2025 EOY value is rounded to $18,900,000. The balance sheet's program-related investments are $18,914,607 [F].
- Part I prior-year columns match the FY2024 return. For example, PY grants are $34,818,019 [F].
- Schedule D answers "yes" to both the legal-control and charitable-purpose disclosure questions [F].

### 1.3 Revenue, program revenue and partner lane

- **Part VIII [F]:**
  - Contributions: $24,333,810, all noncash.
  - Program-service revenue: $699,614 (code 900099/901101, "PROGRAM SERVICE REVENUE"), against FY2024's $438,540.
  - Investment income: $333,755. Net gain on sales: $84,522.
  - Total revenue: $25,451,721.
- **[C]** Schedule D contributions minus Part VIII contributions is $25,033,424 − $24,333,810 = **$699,614**, exactly the program-service revenue. So the inflows Endaoment books as program revenue are also counted as DAF contributions on Schedule D.
- **[I]** This is consistent with fee-like or partner-lane inflows that are credited to funds, but the return does not describe them. No separate partner, revenue-share or "AUM" revenue line exists.
- The partner economics found in batch 30 (Altruist's donor-facing "AUM in DAF account" fee) cannot be seen in Endaoment's return.
- **Schedule A [F]:** 170(b)(1)(A)(vi) support test, public support 83.86% (CY) and 89.54% (PY). Excess over the 2% limit (substantial contributors): $15,844,802.

### 1.4 Crypto, custody and grants [F]

- **Schedule M:** "CRYPTO ASSET", 1,430 contributions, $24,333,810, valued at "Market value". The review process for unusual noncash gifts is answered "yes".
- **Schedule D Part VIII (program-related investments):**
  - "Crypto Assets" $18,312,578, at cost or other basis (C).
  - "Fidelity Investments" $602,029 (C). This is the first appearance of a Fidelity-held position. FY2024 listed only "CRYPTO ASSETS" ($17,112,374).
- **Grants:**
  - Part IX grants to domestic organisations: $18,679,151, equal to Schedule D DAF grants.
  - Schedule I lists 100 501(c)(3) recipients over $5,000, totalling $18,627,655 [C].
  - Top recipients: Athanatos World $4.0m; DMT Quest $2.4m; World Research Foundation $2.32m.
  - **Endaoment itself (EIN 84-4661797) received $1,391,928** (FY2024: $1,163,874). **[I]** These are likely DAF grants to Endaoment's own operating or programme funds. The return gives no explanation.
- **Balance sheet [F]:**
  - Cash: $3.33m.
  - Total assets: $22,328,773.
  - Liabilities: $114,979.
  - Net assets (all without donor restriction): $22,213,794.
  - **The prior-period adjustment of −$2,495,535 has no Schedule O explanation.** **[C]** BOY $19,590,753 + $5,050,716 surplus + $67,860 unrealised gains − $2,495,535 = $22,213,794.

### 1.5 Contractors, staff, governance [F]

- **Contractors:** one over $100k: SingerLewak (Los Angeles), "ACCOUNTING SERVICES", $111,519. SingerLewak was the FY2024 return preparer; Forvis Mazars (Houston) prepared FY2025.
- **People:**
  - Employees: 7. Volunteers: 4. Five voting members, four of them independent.
  - Reportable compensation: COO $133,498; three staff at about $114k each; chairman $28,566.
  - Schedule J was required: the "Total compensation over $150k" indicator is set.
- **Schedule O:** describes generic 990 review, conflict-of-interest and compensation processes. Documents are available "UPON REQUEST".

---

## 2. P-INF-07: Every.org's 990-PF years and its reclassification

### 2.1 Why Every.org filed 990-PF

- **The IRS letter** ([Letter 4422, dated 2025-10-23](https://drive.google.com/file/d/1WLPWnCJ1--p6qQTu7gInxuj8rHUvD4CJ/view), linked from the [tax-status article](https://support.every.org/hc/en-us/articles/5715755336083-What-is-the-501-c-3-tax-exempt-status-of-Every-org); OCR transcription) [F]:
  - "You previously notified the IRS of your intent to terminate your foundation status as a private foundation under Internal Revenue Code (IRC) Section 507(b)(1)(B) and become a public charity."
  - "Based on the information you submitted at the end of your advance ruling period, we determined you terminated your private foundation status under the provisions of IRC Section 507(b)(1)(B). We reclassified you as of January 1, 2020 as a public charity described in the IRC Section listed at the top of this letter."
  - Header: "Public charity status: 170(b)(1)(A)(vi)"; "Form 990/990-EZ/990-N required: Yes".
- **The filing rule** ([Instructions for Form 990-PF (2025)](https://www.irs.gov/pub/irs-pdf/i990pf.pdf), §U) [F]:
  - An organisation terminating under 507(b)(1)(B) "is considered a private foundation for filing requirement purposes and must file an annual return on Form 990-PF. The return must be filed for each year in the 60-month termination period".
  - Notice is given on Form 8940. An advance ruling lets "grantors and contributors … generally rely on it during the 60-month period".
- **Reading [I]:**
  - The 60-month period ran **CY2020–CY2024**, which matches the five e-filed 990-PFs exactly (objects 202141729349100004, 202201479349100500, 202333179349100048, 202423199349106002, 202502749349100700).
  - The letter's phrase "end of your advance ruling period" indicates that Every.org obtained an advance ruling.
  - Why it started as a private foundation is not in any public document. A 2019 start-up funded by a few large grants would normally fail the public-support test at formation; Every.org names Camp.org, the Fidelity Charitable Catalyst Fund and the Gates Foundation as funders ([how Every.org is funded](https://support.every.org/hc/en-us/articles/360058165794-How-is-Every-org-funded)). This is consistent with that pattern but not shown.
- **Anomalies [F]:**
  - **None of the five 990-PF XMLs carries Item F** ("60-month termination under section 507(b)(1)(B)"). The only top-level indicators present are address change, accrual method and 501(c)(3) PF. The instructions say to check Item F during the period. **[I]** Likely a preparer omission; the IRS outcome was not affected.
  - The FY2023 audited statements (harriscpas, opinion 2024-07-10; [Drive](https://drive.google.com/file/d/1OJ7qglomTKL3QajTjgi05j6DGnvnI8cW/view)) say "The Organization files Form 990". They do not mention foundation status or the termination.
  - **The help centre overstates the status.** It says "509(a)(2) and 170(b)(1)(A)(vi)". The letter and the BMF say 170(b)(1)(A)(vi) only (foundation code 15; a 509(a)(2) organisation would carry code 16).

### 2.2 BMF record (IRS [eo_ca.csv](https://www.irs.gov/pub/irs-soi/eo_ca.csv), Last-Modified 2026-11-09) [F]

`611913297,EVERY ORG,…,SUBSECTION 03,…,RULING 202510,DEDUCTIBILITY 1,FOUNDATION 15,…,TAX_PERIOD 202412,…,FILING_REQ_CD 01,PF_FILING_REQ_CD 0,…,ASSET_AMT 9663375,INCOME_AMT 52438692,NTEE T30`

- **[I]** The ruling field (2025-10) records the reclassification letter, not the effective date. The effective date is 2020-01-01, per the letter.

### 2.3 What the reclassification changed

| Dimension | As a PF in termination (2020–2024 filings) | After Letter 4422 | Label |
|---|---|---|---|
| Donor AGI limits | Contributors could rely on the advance ruling during the period. Absent that, gifts to a non-operating PF: cash 30% of AGI; capital-gain property 20%; deduction for appreciated property limited to basis except qualified appreciated stock (IRC 170(b)(1)(B), (D); 170(e)(1)(B)(ii), (e)(5)) | Retroactive to 2020-01-01: public-charity limits (cash 60%, capital-gain property 30%, FMV deduction for long-term property) | Statute [F]; application [I] |
| Crypto donors | Crypto is not "qualified appreciated stock", so a gift to a non-operating PF would be deductible at basis only | FMV deduction (subject to appraisal rules) for long-held crypto | [I] |
| Excise tax | 4940 tax paid: $0 (2020–2022), **$891 (2023)**, **$9,853 (2024)** | The instructions allow a refund claim "after completing termination … establishing that it qualified as a public charity" | [F] amounts and instructions; claim not seen |
| Chapter 42 | Part VII-B completed. 2024: "Pay compensation to … a disqualified person" = yes; no taxable acts reported | Not applicable from 2020 on reclassification | [F]/[I] |
| Donor disclosure | **990-PF Schedule B is public.** Unredacted contributor rows: 27 (2020), 119 (2021), 112 (2022), 248 (2023), **530 (2024)** | Form 990 Schedule B names and addresses are not public | [F] counts; names not copied into this repo |
| Annual return | 990-PF; no Schedule D | Form 990 with Schedule A and Schedule D (Part I if balances are reported as DAFs) | [F] BMF codes |
| Payout | 4942 distributable amount $255,096 (2024) against $47.3m qualifying distributions; carryover $94.96m | No payout rule | [F] |
| QCD eligibility | QCDs cannot go to non-operating PFs (408(d)(8)(B)(ii)) | QCDs to a 170(b)(1)(A) charity qualify, but **not** to "any fund or account described in section 4966(d)(2)" | Statute [F]; see §2.4 |

### 2.4 DAF-like role: the QCD and giving-credit tension

- **[F]** Help-centre articles created **2026-09-11** say Every.org accepts IRA QCDs, by check to Every.org ([donor article](https://support.every.org/hc/en-us/articles/55340641316115-How-can-I-donate-from-my-IRA-to-a-charity-using-Every-org), updated 2026-10-05; [nonprofit article](https://support.every.org/hc/en-us/articles/55340873567251-How-can-my-nonprofit-accept-IRA-gifts-through-Every-org)).
- **[F]** On the account balance: "Can I use an IRA gift to fund my Every.org account balance? **Yes**, an IRA gift can be used to fund your account balance with giving credit … fund your account with one large donation from your IRA, and then complete your gifts from your account balance."
- **[F]** Every.org's own help text calls donor balances its "DAF structure" (repo, [asset article](https://support.every.org/hc/en-us/articles/360058166014-How-can-I-donate-stocks-cryptocurrency-or-other-assets)). Its audit books them as customer deposits (batch 30).
- **[I]** A giving-credit balance is separately identified by donor, owned by Every.org, and spent on the donor's recommendations. On its face it meets the three prongs of 4966(d)(2). If it is a DAF, a QCD used to fund it would fail the exclusion.
  - Every.org's "gift card" characterisation and its customer-deposit accounting point the other way. They imply no completed gift until redemption, which in turn sits awkwardly with an immediate tax receipt.
  - The CY2025 Form 990 Schedule D, expected in the 2026 or 2027 index (watchlist `irs-everyorg`), will show how Every.org itself classifies the balances.
  - **No IRS guidance specific to this structure was found.** This is a live classification question, not a finding of non-compliance. See proposal P-B31B-01.

---

## 3. P-B30A-01: does any aggregator sync Fidelity Charitable Giving Accounts?

| Channel | Evidence | Date | Status | Label |
|---|---|---|---|---|
| **Addepar** (adviser portfolio data feed) | [Integration Center: "Fidelity Investments: Charitable Gift Fund/Donor-Advised Fund"](https://integrations.addepar.com/product/fidelity-investments-charitable-gift-fund-donor-advised-fund): "Requires Fidelity advisory relationship with G-Number to be eligible"; "Charitable Gift Fund (CGF), Donor-Advised Fund (DAF)"; e-signature "No"; account formats of 3–7 digits | Last updated 2026-09-09 | **Listed live.** This is the only DAF-sponsor feed in Addepar's US portfolio-feed directory (page search for "charit") | F |
| Addepar (history) | [Addepar Data Network, Spring 2021 PDF](https://info.addepar.com/rs/232-KUI-215/images/addepar-data-providers.pdf) lists "Fidelity Investments: Charitable Gift Fund/Donor-Advised Fund" among domestic feeds | PDF modified 2021-03-30 | The feed existed in 2021 | F |
| Fidelity Charitable (sponsor side) | [Advisor account maintenance](https://fidelitycharitable.org/advisors/support/account-maintenance.html): "Firms that use Wealthscape and have their G Number added to a Giving Account can manage access"; brokerage clients "can use the link in their portfolio view for single sign on" | Live 2026-11 (WebFetch) | **Confirms the G-Number linkage** that Addepar's eligibility rule depends on | F |
| **Empower Personal Dashboard** (consumer) | [Help article 22540027869591](https://support-personalwealth.empower.com/hc/en-us/articles/22540027869591-Fidelity-Charitable-Gift-Fund-Accounts) (Zendesk JSON: created 2024-04-03, updated 2025-12-06): accounts "are no longer able to sync under the Fidelity Investments option … we recommend … syncing the account again under the 'Fidelity Charitable' option" | 2025-12-06 | **A separate "Fidelity Charitable" connection is offered.** Whether it uses OAuth, Akoya or credentials is not stated. Batch 30's [R] snippet is now upgraded to [F] (full text) | F |
| **eMoney** (Fidelity-owned, adviser) | [eMoney Connection Update](https://blog.emoneyadvisor.com/best-practices/the-industry-leader-in-account-aggregation-emoney-connection-update/): API migrations "since 2020, including … Fidelity – Including Fidelity Investments, Fidelity NetBenefits, and Fidelity Charitable sites"; "As of Q1 2023, 83% of eMoney connections are aggregated via API's" | Undated; c.2023 (cites Q1 2023 and a TD Ameritrade conversion "in September of 2023") [I] | API connection existed in 2023; 2026 status [U] | F (date I) |
| **Morningstar ByAllAccounts** | 2023 notices: FI 44892 "Fidelity Charitable Gift Fund (Investment)" moved to the Akoya "Fidelity (Investment)" feed, primary holder only (batch 30) | July 2023 | 2026 status [U]. Morningstar sold ByAllAccounts to Pello ([Kitces, May 2026](https://www.kitces.com/blog/the-latest-in-financial-advisortech-may-2026-morningstar-byallaccounts-data-aggregation-finny-advisor360-wealth/)) | F (2023); S |
| **Quicken / QuickBooks** (Intuit FI directory) | [fidir.txt](https://ofx-prod-filist.intuit.com/qm2400/data/fidir.txt) (Last-Modified 2026-11-15; 16,458 FIs): no "Fidelity Charitable" row. "Fidelity Investments" is listed (Express Web Connect). The only DAF-programme row is **"T. Rowe Price Program for Charitable"** (FI 66918) at `https://pcg.donorfirstx.com` (a Ren host), ACTIVE, Express Web Connect | 2026-11-15 | No dedicated Fidelity Charitable connection in Quicken's directory. Whether Giving Accounts come through the Fidelity Investments connection: [U] | F (absence) |
| Plaid / Yodlee / Monarch / Simplifi / Copilot | Searches found only Fidelity Investments brokerage connectivity threads, nothing for Fidelity Charitable | — | [U] | — |
| Fidelity Charitable security article | Snippet: "understand how your account information will be used before connecting to a third-party service" ([article](https://www.fidelitycharitable.org/articles/security-tips-common-scams.html); 403 to WebFetch) | — | Implies third-party connections are contemplated | R |
| Chariot "managed sources" (charity-side reconciliation) | Repo: Chariot's paid plan includes a "Fidelity Charitable" source ([sources](https://help.givechariot.com/getting-started/sources.md); [queue-bank-programs-and-eft-providers.md](queue-bank-programs-and-eft-providers.md) §6) | 2026 | A grant-receipt reconciliation feed for nonprofits, not donor aggregation | F (repo) |

**Reading [I]:**
- **The License Agreement s.8 "third party software product or on-line service" channel is live in 2025–2026**, by two routes:
  1. **Adviser portfolio feeds** gated on a Fidelity Institutional G-Number (Addepar; probably eMoney too).
  2. **At least one consumer aggregator** (Empower) that offers a dedicated Fidelity Charitable connection.
- The 2023 Akoya re-routing (primary holder only) and Empower's note show that Giving Accounts **do not ride Fidelity Investments' brokerage OAuth**. They need their own connection.
- **For Fidelity's A1/A3 Y data-portability score:** add "adviser feed (Addepar, G-Number) and a consumer aggregator option (Empower) exist". There is still no donor-side CSV or transaction export (batch 30 §5).
- Suggested amendment to `donor-data-export-top10-2026.csv` row 1: "consumer-aggregator feed via Fidelity/Akoya existed in 2023 (primary holder only); Empower offers a 'Fidelity Charitable' connection (2025-12); Addepar lists a CGF/DAF feed for G-Number advisers (2026-09)".

---

## 4. P-QA3-03: adviser and donor data feeds at GS PF, MS GIFT, BofA CGF and NPT

| Sponsor | Integration documented | API or file feed | Aggregator or portfolio-system listing | Contractual data right | Label |
|---|---|---|---|---|---|
| **GS PF** (EIN 31-1774905) | Donor web with "Login with Goldman.com" single sign-on (repo, [donor web](https://gspf.goldman.com/gspf/)) | None found | Addepar lists "Goldman Sachs Private Wealth Management" (global; e-signature yes; account types "Goldman Sachs Private Wealth Management, Goldman Sachs International") ([page](https://integrations.addepar.com/product/goldman-sachs-private-wealth-management), updated 2026-09-09). No DAF account type named. Intuit lists "Goldman Sachs Private Wealth" (Express Web Connect). Nothing for GS PF | View rights; quarterly statements govern (repo) | F; [I] on DAF coverage |
| **MS GIFT** (Ren DFX) | "Donors will not receive separate login credentials"; "Donors must access their DAF through Morgan Stanley Online (MSO)"; advisers "must login through 3D" ([Ren FAQ, "updated 12/29", giving season 2025](https://www.reninc.com/giving-season-2025-commonly-asked-questions/)) | None found | Addepar "Morgan Stanley Global Wealth Management": "Requires Morgan Stanley branch approval"; "Brokerage, Investment and E*trade Accounts" ([page](https://integrations.addepar.com/product/morgan-stanley-global-wealth-management), updated 2026-09-09). MS GIFT investments run through MSSB Select UMA or Portfolio Management accounts (circular, repo) | No export clause (circular, repo) | F; [I] that MSSB feeds may carry GIFT sub-accounts |
| **BofA CGF** (Ren DonorFirst) | "Balances for Charitable Gift Fund accounts are now available on MyMerrill and Private Bank Account Access"; BofA Online "Vendor Donor Portal" single sign-on (repo, [portal](https://bofa.donorfirst.org/); [2025 guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)) | Excel export of the contribution list only (repo) | Addepar "Bank of America Private Bank" and "Merrill Lynch Private Wealth Management" (brokerage; "Private wealth accounts, except NOT loans"), updated 2026-09-09. No DAF type named | No portability right (repo) | F; [I] |
| **NPT** | [For Financial Institutions](https://www.nptrust.org/advisors-and-institutions/for-financial-institutions/): "Digital workflow including online access, SSO, and advisor/client experience requirements"; "Private-label capabilities"; "Customized advisor and client dashboard views". [DAF Guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) (PDF dated 2026-10-15): financial advisor "full access or read-only access"; "online quarterly statement". Segregated accounts of $500k+ can be advised by the donor's adviser, and NPT staff liaise with "custodians" ([NPT job post, 2025-02-28](https://diversityjobs.com/career/11265966/Segregated-Accounts-Associate-Pennsylvania-Jenkintown)) | **No public API docs.** GivingPoint is "built using modern APIs" internally ([NPT 2021 blog PDF](https://www.nptrust.org/wp-content/uploads/2021/02/NPT-Blog-Five-things-to-Know-about-GivingPoint-NPT.pdf)) | No Addepar, Intuit or other listing found | Terms of Use (2026-10-29) ban robots and scripts and allow access only by authorised persons (repo) | F; [U] for feeds |
| Ren (vendor for MS GIFT and BofA CGF) | [DFX page](https://www.reninc.com/dfx): firms "can login and track key account activity"; advisers "View balances and investment activity" | No public API docs. Two Ren PDFs cited by search returned 404 | Intuit lists the T. Rowe Price programme on `pcg.donorfirstx.com` (Express Web Connect), so at least one Ren-hosted DAF portal is aggregated by Intuit | — | F |

**Reading [I]:**
- **The wealth-captive pattern is integration into the parent firm's own client and adviser surfaces:** MSO/3D, MyMerrill and Private Bank, Goldman.com, and NPT's partner SSO. It is not a feed to third-party systems.
- **Fidelity Charitable is the only DAF sponsor with a named feed in a major adviser portfolio system.** Addepar lists no Schwab, Vanguard, NPT, GS, MS or BofA DAF feed.
- **Whether parent-firm custodial feeds include DAF accounts is untested.** MS GIFT's assets are invested through MSSB advisory accounts, and BofA CGF's are invested through the Private Bank. Addepar's feed pages would carry them only if the sponsor-owned accounts are mapped to the client household, which they do not say.
- **For A3 Y1/Y2:** these sponsors move from "insufficient evidence" to "portal and SSO integration within the parent; no third-party feed or API documented" (Y1 at most 2) [I]. The score itself is for the quadrant agent.

---

## 5. Limits

- Endaoment: no audited statements were read. The prior-period adjustment and the 6,000 count cannot be explained from public filings.
- Every.org: Form 8940 and the advance-ruling letter are not public. Whether the 4940 refund was claimed is unknown. The DAF and QCD analysis applies statute only.
- Aggregators: consumer apps (Plaid, Yodlee, Monarch, Simplifi) publish no institution lists. Empower's "Fidelity Charitable" option was not tested (no login). Black Diamond, Orion and Tamarac custodian lists are not public; searches surfaced only generic feed counts.
- Wealth-captives: absence of public API or feed documentation is not proof that none exists. Adviser-only documents sit behind logins.

---

## 6. Source register

| ID | Source | Date | Used for |
|---|---|---|---|
| S1 | [IRS index 2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) | Last modified 2026-10-21 | Endaoment row; batch label |
| S2 | [IRS 2026_TEOS_XML_05B.zip](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip) (member 202631359349315978_public.xml); [05A zip](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05A.zip) (member absent) | Zip Last-Modified 2026-06-17; return 2026-05-15 | Endaoment FY2025 |
| S3 | [GivingTuesday mirror, FY2024 Endaoment](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542899349300104_public.xml) | 2025-10-15 | FY2024 comparison |
| S4 | [DAFRC dataset (repo copy)](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | Spring 2026 | Imputed rows |
| S5 | Every.org 990-PF XMLs: [2020](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202141729349100004_public.xml), [2021](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202201479349100500_public.xml), [2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333179349100048_public.xml), [2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423199349106002_public.xml), [2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502749349100700_public.xml) | 2021–2025 | Item F absence, 4940 tax, Schedule B counts, payout |
| S6 | [IRS Letter 4422, 2025-10-23 (Every.org Drive)](https://drive.google.com/file/d/1WLPWnCJ1--p6qQTu7gInxuj8rHUvD4CJ/view) | 2025-10-23 | 507(b)(1)(B) termination; effective date; 170(b)(1)(A)(vi) |
| S7 | [IRS EO BMF, California](https://www.irs.gov/pub/irs-soi/eo_ca.csv) | Last-Modified 2026-11-09 | Foundation code 15, ruling 202510, filing codes |
| S8 | [Instructions for Form 990-PF (2025)](https://www.irs.gov/pub/irs-pdf/i990pf.pdf) §U, §V, Item F | 2026-01-15 | Filing rule during termination; refund; advance-ruling reliance |
| S9 | Every.org help centre (Zendesk JSON, 2026-11-15): [tax status](https://support.every.org/hc/en-us/articles/5715755336083-What-is-the-501-c-3-tax-exempt-status-of-Every-org) (updated 2026-08-21); [IRA donor](https://support.every.org/hc/en-us/articles/55340641316115-How-can-I-donate-from-my-IRA-to-a-charity-using-Every-org); [IRA nonprofit](https://support.every.org/hc/en-us/articles/55340873567251-How-can-my-nonprofit-accept-IRA-gifts-through-Every-org); [funding](https://support.every.org/hc/en-us/articles/360058165794-How-is-Every-org-funded) | 2026 | Status claim, QCDs, funders |
| S10 | [Every.org FY2023 audited FS](https://drive.google.com/file/d/1OJ7qglomTKL3QajTjgi05j6DGnvnI8cW/view) | Opinion 2024-07-10 | "files Form 990" note |
| S11 | [Addepar Integration Center](https://integrations.addepar.com/type/portfolio-data-feeds): [Fidelity CGF/DAF](https://integrations.addepar.com/product/fidelity-investments-charitable-gift-fund-donor-advised-fund), [GS PWM](https://integrations.addepar.com/product/goldman-sachs-private-wealth-management), [MS GWM](https://integrations.addepar.com/product/morgan-stanley-global-wealth-management), [BofA Private Bank](https://integrations.addepar.com/product/bank-of-america-private-bank), [Merrill PWM](https://integrations.addepar.com/product/merrill-lynch-private-wealth-management) | Each updated 2026-09-09 | Feeds |
| S12 | [Addepar Data Network, Spring 2021](https://info.addepar.com/rs/232-KUI-215/images/addepar-data-providers.pdf) | 2021-03-30 | 2021 Fidelity Charitable feed |
| S13 | [Empower help 22540027869591](https://support-personalwealth.empower.com/hc/en-us/articles/22540027869591-Fidelity-Charitable-Gift-Fund-Accounts); [OAuth article 4414063333783](https://support-personalwealth.empower.com/hc/en-us/articles/4414063333783-New-Account-Linking-Process-with-Open-Authorization) | 2025-12-06; 2026-11-10 | Consumer aggregation |
| S14 | [eMoney Connection Update](https://blog.emoneyadvisor.com/best-practices/the-industry-leader-in-account-aggregation-emoney-connection-update/) | c.2023 | API migration incl. Fidelity Charitable |
| S15 | [Intuit FI directory fidir.txt](https://ofx-prod-filist.intuit.com/qm2400/data/fidir.txt) | 2026-11-15 | Quicken coverage |
| S16 | [Fidelity Charitable advisor account maintenance](https://fidelitycharitable.org/advisors/support/account-maintenance.html) | Live 2026-11 | G-Number, SSO |
| S17 | Morningstar ByAllAccounts notices (batch 30 §5); [Kitces May 2026](https://www.kitces.com/blog/the-latest-in-financial-advisortech-may-2026-morningstar-byallaccounts-data-aggregation-finny-advisor360-wealth/) | 2023; 2026-05 | Akoya route; ByAllAccounts sale |
| S18 | [Ren giving-season FAQ](https://www.reninc.com/giving-season-2025-commonly-asked-questions/); [Ren DFX](https://www.reninc.com/dfx) | "updated 12/29" (2025 season) | MS GIFT MSO/3D access |
| S19 | NPT: [For Financial Institutions](https://www.nptrust.org/advisors-and-institutions/for-financial-institutions/); [DAF Guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf); [GivingPoint blog PDF](https://www.nptrust.org/wp-content/uploads/2021/02/NPT-Blog-Five-things-to-Know-about-GivingPoint-NPT.pdf); [job post](https://diversityjobs.com/career/11265966/Segregated-Accounts-Associate-Pennsylvania-Jenkintown) | 2021–2026 | NPT access model |
| S20 | Repo: [queue-bank-programs-and-eft-providers.md](queue-bank-programs-and-eft-providers.md); [wealth-captive-terms-2026.csv](../../data/mission-2026-11-14/wealth-captive-terms-2026.csv); [bank-program-terms-2026.csv](../../data/mission-2026-11-14/bank-program-terms-2026.csv) | 2026-11-14/15 | BofA, GS PF and MS GIFT portal facts |

## 7. Data dictionary

### `sponsor-data-feeds-2026.csv` (one row per sponsor × channel × evidence item)

| Column | Meaning |
|---|---|
| feed_id | SDF-NN |
| sponsor | DAF sponsor (or vendor, for Ren) |
| channel_type | One of the following:<br>- `adviser_portfolio_feed`: custodial or sponsor feed into an adviser portfolio system<br>- `consumer_aggregator`: personal-finance aggregator<br>- `adviser_aggregator`: adviser planning aggregator<br>- `parent_portal_embed`: DAF data shown inside the parent firm's client or adviser portal<br>- `sso`: single sign-on hand-off<br>- `file_export`: in-portal download<br>- `api_public`: documented public API<br>- `charity_reconciliation`: feed for grant recipients<br>- `directory_absence`: checked directory with no entry |
| counterparty | System or firm on the other side |
| daf_specific | `yes` if the listing names a DAF or charitable account type; `no` if it is a parent-firm feed that may or may not carry DAF accounts; `n/a` |
| status | `listed_live`, `documented`, `historical`, `absent`, `unknown` |
| access_condition | Eligibility or authorisation stated |
| evidence_date | Date of the evidence (YYYY-MM-DD or YYYY-MM; `c.` when inferred) |
| evidence_label | F, R, S, I or U (see header) |
| recency_admissible | `yes` if the evidence is dated 2021 or later |
| quote_or_basis | Short quote or basis |
| source_url | Primary URL |
| accessed | Access date |
| notes | Caveats |

### `queue-proposals-batch31b.csv`

- Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- IDs are P-B31B-01..03.

## Validation corrections (wave 16, 2026-11-15) — governing
Source: [validation-wave16-report.md](validation-wave16-report.md); register `data/mission-2026-11-14/validation-register-wave16.csv`.

1. **Line 40 (§0, P-INF-07).** Replace "QCDs cannot go to a DAF (IRC 408(d)(8)(B)(ii))" with "QCDs cannot go to a DAF (IRC 408(d)(8)(B)(i), which excludes 'any fund or account described in section 4966(d)(2)')".
2. **Line 152 (§2.3 table, QCD row).** Replace "QCDs cannot go to non-operating PFs (408(d)(8)(B)(ii))" with "QCDs must go to a 170(b)(1)(A) organisation other than a 509(a)(3) supporting organisation or a DAF (408(d)(8)(B)(i)). Non-operating PFs not described in 170(b)(1)(F) do not qualify".
3. **Line 40 (§0, P-INF-07, item 3).**
   - Replace: "**Donor names stop being public.** Every 990-PF Schedule B named its ≥$5k contributors (530 in CY2024); Form 990 Schedule B names are not public [F]."
   - With: "**Donor names stop being public from CY2025 on.** Every 990-PF Schedule B named its ≥$5k contributors (530 in CY2024), and those five filed returns stay public. Form 990 Schedule B names are not public [F]."
4. **Line 41 (§0, P-B30A-01).** Replace "The post is undated, c.2023 [F; date I]." with "The post is dated 2023-04-17 (page metadata) [F]."
5. **Line 174 (§3 table, eMoney row).** Replace "| Undated; c.2023 (cites Q1 2023 and a TD Ameritrade conversion \"in September of 2023\") [I] |" with "| 2023-04-17 (page metadata `datePublished`) [F] |". In the S14 register row (line 235), replace "c.2023" with "2023-04-17". In `sponsor-data-feeds-2026.csv`, SDF-05 `evidence_date` should be "2023-04-17".
