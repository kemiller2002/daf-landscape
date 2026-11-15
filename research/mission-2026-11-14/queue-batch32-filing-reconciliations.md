# Queue batch 32 B: Endaoment count and balance reconciliation (P-B31B-02), Every.org giving credit and QCDs (P-B31B-01), tier-B sponsor DAF exits (P-MOR-02), Givinga's 2024 bank-fraud loss (P-PRC-02)

**Date:** 2026-11-15.

**Method:**
- Public sources only, 2021 onward. No accounts were created, no logins were used, no forms were submitted and nobody was contacted.
- **IRS e-files.** 359 Form 990 XMLs for the 58 tier-B sponsors, plus four Endaoment and four Givinga returns, were listed from the IRS e-file indexes for 2019–2026.
  - Most came from the GivingTuesday mirror.
  - 13 that the mirror does not hold (404) were read from [`2026_TEOS_XML_05B.zip`](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip) with HTTP range requests. The index labels them batch "05A"; batch 31 found the same mislabelling.
- **Parsing.** Fields and text were extracted with stdlib Python (`xml.etree`), and keyword scans covered Schedule D, O and I, Part III and Part XI. The scripts are in the session scratchpad and are not part of the repo.
- **PDFs** were read with `pdftotext`. **Every.org help articles** were read from the public Zendesk JSON. `www.every.org/terms` returned 403 (curl) and 429 (WebFetch), so it was **not read**.
- **Tags:** **[F]** fact from a cited primary source; **[C]** calculation; **[I]** inference; **[U]** not found; **[S]** secondary.
- **This is research, not legal or tax advice.**

**Builds on, and applies the governing corrections of:**
- [queue-batch31-filings-feeds.md](queue-batch31-filings-feeds.md), with wave-16 corrections 1–5. In particular, **the bar on QCDs to DAFs is IRC 408(d)(8)(B)(i)**, not (ii).
- [queue-batch30-everyorg-givinga-goodstack.md](queue-batch30-everyorg-givinga-goodstack.md), with wave-15 corrections 1–5. In particular, Every.org's 990-PF deferred revenue is not like-for-like with its audited customer deposits, and the original CY2024 Givinga return carried no Part I values.
- [sponsor-mortality-analysis.md](sponsor-mortality-analysis.md), with its wave-4 corrections. This includes the exposure base of 5,746 sponsor-years.

**Outputs:**
- This file.
- [data/mission-2026-11-14/tier-b-daf-exit-reasons.csv](../../data/mission-2026-11-14/tier-b-daf-exit-reasons.csv): 58 rows.
- [data/mission-2026-11-14/queue-proposals-batch32b.csv](../../data/mission-2026-11-14/queue-proposals-batch32b.csv): P-B32B-01..03.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B31B-02** Endaoment | **The counts cannot be reconciled from public sources, and the dollar series has a larger problem than the counts.**<br>• The FY2023 Form 990 understated year-end net assets by **$12,215,133** against the audited statements ($4,203,797 against $16,418,930) [C].<br>• The FY2024 return then **silently opened at the audited figure**. It has no prior-period line, and "other changes" is 0 [F].<br>• FY2022 is also off by $3.92m (990 $16,331,056 against audit $20,249,033) [C].<br>• All four returns answer "financial statements audited" **No**, although audits for FY2021–23 exist (issued in 2024 and 2025) [F].<br>• The DAF counts (331; not reported; 6,000; 1,213) appear in no audit or Endaoment publication [U]. The FY2024 "6,000" remains a round, unsupported figure; FY2025's 1,213 is the best-evidenced count.<br>• The FY2025 prior-period adjustment of −$2,495,535 is unexplained [U]. It is close to, but not equal to, the FY2024 gap between net assets and Schedule D DAF value ($2,478,379) [C].<br>• The $1.39m self-grant is larger than the most Endaoment's published intra-organisational fees could produce (≤$0.31m) [C]. | High on the reconciliation arithmetic; low on the causes |
| **P-B31B-01** Every.org | **On the face of the statute and the 2023 proposed regulations, a giving-credit balance looks like a "fund or account described in section 4966(d)(2)"** [I]. If so, an IRA distribution used to fund it is outside 408(d)(8)(B)(i) and is not a QCD.<br>• Every.org's help text says an IRA gift "can be used to fund your account balance with giving credit" (article updated 2026-10-05) [F].<br>• Every.org itself calls the balance mechanism its "DAF structure" [F].<br>• A QCD sent through Every.org to a named nonprofit (an immediate unrestricted grant) is a weaker DAF case [I].<br>• There is no IRS ruling, notice or publication on platform giving-credit balances [U]. Pub. 590-B (2025) does not mention the DAF exclusion at all [F]. | Medium on the statute reading; this is an open classification question, not a finding of non-compliance |
| **P-MOR-02** Tier-B sponsors (58) | **Only 14 of the 58 are documented DAF exits:**<br>– 6 transferred out;<br>– 4 granted to zero;<br>– 1 zeroed with no disposition stated;<br>– 3 already at zero.<br>**18 are clear non-exits:**<br>– 13 still answer Part IV line 6 "Yes" with Part I values blank;<br>– 1 (Gorge) resumed reporting 36 DAFs and $5.1m in FY2025;<br>– 3 reclassified;<br>– 1 still labels grants "Donor Advised Fund".<br>**6 are ambiguous:** a blank-Part-I gap, then line 6 "No".<br>**20 are undetermined:** no text in the filings explains the change. | High on the classification inputs; [C] on the rate effect |
| | **Effect on the central exit bound [C]:** dropping the 18 non-exits lowers it from 1.20% to **0.89%/yr** ((11 + 40)/5,746). Counting only documented exits gives **0.44%/yr** ((11 + 14)/5,746). | |
| **P-PRC-02** Givinga | **The vector, payment rail and any recovery are not publicly disclosed** [U].<br>• The only public trace is a Part IX line, "EXTERNAL BANK FRAUD LOS[S]", $316,184, booked to management and general. It appears in both the original return (2025-08-25) and the amended CY2024 return (2025-11-13) [F].<br>• Part VI line 5 (diversion) is No. Financial statements are audited, separate basis. The preparer is Nisivoccia LLP [F].<br>• Unexplained "miscellaneous income" of $93,725 might be a recovery, but nothing says so [I].<br>• The CY2025 return is not yet in the IRS index (last modified 2026-10-21) [F].<br>• No press, court record or public audit was found [U]. | High that it is undisclosed |

---

## 1. P-B31B-02: Endaoment (EIN 84-4661797; fiscal year ends 30 June)

### 1.1 Sources read
- **IRS returns:**
  - FY2022: [202323209349303992](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202323209349303992_public.xml), ReturnTs 2023-11-16.
  - FY2023: [202411369349317486](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411369349317486_public.xml), ReturnTs 2024-05-15.
  - FY2024: [202542899349300104](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542899349300104_public.xml), ReturnTs 2025-10-15.
  - FY2025: 202631359349315978, from the [05B zip](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip); ReturnTs 2026-05-15.
- **Audits linked from Endaoment's [legal documentation page](https://docs.endaoment.org/governance/resources/legal-documentation)** (page "Last updated March 10, 2025"):
  - [FY2021 audit](https://storage.googleapis.com/endaoment-static/docs-assets/audit-fy21.pdf) (PDF created 2024-03-12);
  - [FY2022–FY2023 audit](https://storage.googleapis.com/endaoment-static/docs-assets/audit-fy22-23.pdf) (report dated **2025-03-07**; SingerLewak per [Endaoment's blog](https://blog.endaoment.org/blog/2022-2023-fiscal-audits-complete)).
  - No FY2024 or FY2025 audit is posted. Guessed object names (`audit-fy24.pdf`, `audit-fy24-25.pdf`, `audit-fy25.pdf` and others) return 404 [U].
- **Endaoment docs:**
  - [Onchain recordkeeping](https://docs.endaoment.org/advisors/about/platform-recordkeeping): "Independent third parties can audit transaction integrity". The page publishes no fund count or contract registry [F].
  - [Fee schedule](https://docs.endaoment.org/donors/resources/fee-schedule): one-time inbound fee tiered from 0.50%; 1.0% outbound fee [F].
  - [DAF Agreement §10](https://docs.endaoment.org/governance/documentation/fund-agreement) (updated 2026-08-14): "Intraorganizational fees will be transferred from the Fund to Endaoment's general funds" [F].

### 1.2 Net assets and contributions: audit against Form 990 [F]/[C]

| FY (30 June) | Audit: net assets EOY | 990: net assets BOY → EOY | Gap, 990 − audit (EOY) | Audit contributions | 990 Part VIII contributions | 990 Sch D DAF EOY | Audit "Donor-advised funds" asset |
|---|---|---|---|---|---|---|---|
| 2021 | $1,039,186 | — | — | — | — | — | $784,265 |
| 2022 | $20,249,033 | $1,147,782 → $16,331,056 | **−$3,917,977** | $45,072,798 | $41,338,191 | $15,309,881 (331 DAFs) | $19,482,202 |
| 2023 | $16,418,930 | $16,331,056 → **$4,203,797** | **−$12,215,133** | $10,144,181 | **$1,623,475** | not reported | $15,568,573 |
| 2024 | not public | **$16,418,930** → $19,590,753 | — | — | $29,879,802 | $17,112,374 (6,000 DAFs) | — |
| 2025 | not public | $19,590,753 → $22,213,794 (after **PPA −$2,495,535**) | — | — | $24,333,810 | $18,900,000 (1,213 DAFs) | — |

**Reading:**
- **The FY2024 opening balance is the audited FY2023 close, not the FY2023 990 close.** BOY net assets ($16,418,930) and total assets ($16,420,149) equal the audit exactly [F]. BOY program-related investments of $16,263,586 equal the audit's DAF asset ($15,568,573) plus digital assets ($695,013) [C].
  - The +$12.2m step from the FY2023 990 is not shown as a prior-period adjustment ("other changes" = 0) [F].
- **[I]** The FY2023 990 appears to have left most fund-held crypto/USDC out of both the balance sheet and contributions: 990 contributions are $1.62m against $10.14m audited, while grants roughly agree ($12.27m against $12.82m). Its year-end total assets of $4.2m are mostly "savings and temporary cash" of $3.74m. The FY2022 990 understates in the same direction, but less.
- **"Audited" boxes:** `FSAuditedInd` is 0/false on all four returns [F].
  - The FY2022 and FY2023 returns were filed before the March 2025 audit report, so "No" was true at filing [C].
  - The FY2024 return (filed 2025-10-15) and the FY2025 return also say No. That implies FY2024 and FY2025 were not audited, or the box is wrong [I].
- **FY2025 prior-period adjustment (−$2,495,535):**
  - No Schedule O or Part XI text explains it [F].
  - The FY2024 gap between net assets and Schedule D DAF value is $19,590,753 − $17,112,374 = $2,478,379, which is within $17,156 of the PPA [C]. One possibility is a write-down of non-fund (operating or digital) assets carried in FY2024 [I]. This is unproven.

### 1.3 DAF counts [F]/[C]/[U]
- The audits give **no fund counts** [F]. Endaoment publishes none: no count was found in the docs index ([llms.txt](https://docs.endaoment.org/llms.txt)), blog or search results [U].
- The public API documents an unauthenticated ["total platform impact"](https://docs.endaoment.org/developers/api/donations/get-total-platform-impact) value (dollars, not counts) and public community-fund listings. It has no count endpoint [F].
  - Counting fund-creation events on-chain was not attempted. This is proposal P-B32B-02.
- **Plausibility checks [C]:**
  - FY2024: 6,000 DAFs at $17.11m is $2,852 each. Its Schedule M crypto-contribution count field is 0, so it gives no cross-check.
  - FY2025: 1,213 DAFs at $18.9m is $15,581 each, against 1,430 Schedule M crypto contributions.
  - FY2022: 331 DAFs at $15.31m is $46,253 each.
  - The 6,000 is out of line with both neighbours. No amended FY2024 return is indexed in 2025 or 2026 [F].
- **Recommendation [I]:**
  - Use **1,213 (FY2025)**.
  - Keep FY2024's 6,000 flagged "round; contradicted by FY2025; no published or audited support".
  - Treat FY2023 as missing.
  - For dollar series, **prefer the audit for FY2022–23** ($19.48m and $15.57m of DAF assets) over the 990 Schedule D or Part X figures.

### 1.4 The $1.39m self-grant [F]/[C]
- FY2025 Schedule I lists "Endaoment … 844661797 … $1,391,928 … General Purpose". FY2024 lists $1,163,874, also "GENERAL PURPOSE" [F].
- **Ceiling on published fees [C]:**
  - Inbound fee at most 0.50% × $25,033,424 = $125,167. The tiers make it lower for large gifts.
  - Outbound fee 1.0% × $18,679,151 = $186,792.
  - Total at most **$311,959**.
- So the published App fees cannot account for the self-grant. They also cannot account for the $699,614 of program-service revenue (batch 31 showed it equals Schedule D minus Part VIII contributions) [C].
- **[I] Possible components:**
  1. Fees from the separate "AUM partner" lane (for example Altruist), which the fee page says use "a different Endaoment product lane".
  2. Donor-recommended grants to Endaoment's own operations.
  3. Treatment of fees as grants.
- None is stated in the filings [U].

---

## 2. P-B31B-01: are Every.org giving-credit balances DAFs, given IRA QCDs since 2026-09?

### 2.1 Statute [F]
- **IRC 408(d)(8)(B)** ([LII](https://www.law.cornell.edu/uscode/text/26/408)): a QCD is a distribution "(i) which is made directly by the trustee to an organization described in section 170(b)(1)(A) (other than any organization described in section 509(a)(3) or **any fund or account described in section 4966(d)(2)**), and (ii) which is made on or after the date that the individual … has attained age 70½".
- **IRC 408(d)(8)(C):** the exclusion applies only if the entire distribution would otherwise be deductible under section 170.
- **IRC 4966(d)(2)(A)** ([LII](https://www.law.cornell.edu/uscode/text/26/4966)): a DAF is a fund or account that is:
  - "(i) … separately identified by reference to contributions of a donor or donors,
  - (ii) … owned and controlled by a sponsoring organization, and
  - (iii) with respect to which a donor (or any person appointed or designated by such donor) has, or reasonably expects to have, advisory privileges with respect to the distribution or investment of amounts held in such fund or account by reason of the donor's status as a donor".
- **Exceptions (4966(d)(2)(B)):** a fund that makes distributions only to a single identified organisation or governmental entity, and certain individual-grant (travel or study) funds.

### 2.2 Proposed regulations (REG-142338-07, [88 FR 77922, 2023-11-14](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm); not final) [F]
- **Separate identification.** A fund is separately identified "if the sponsoring organization maintains a formal record of contributions to the fund or account relating to a donor or donors". This holds "regardless of whether the sponsoring organization commingles the assets".
- **Fallback factors** where there is no formal record include:
  - a balance reflecting contributions and distributions;
  - "the sponsoring organization refers to the fund or account as a DAF";
  - donors "regularly receive a fund or account statement";
  - the sponsor "generally solicits advice from the donor(s) … before making distributions".
- **Donor-advisor** is defined as "a person appointed or designated by a donor to have advisory privileges".
- **Advisory privileges** depend on the facts and circumstances, and "may [exist] even in the absence of the actual provision of advice".
- **No platform, gift-card or giving-credit carve-out** appears in the preamble or the proposed text (keyword scan for "gift card", "intermediar", "online", "platform" found none relevant) [F].

### 2.3 Every.org facts (help centre, Zendesk JSON, 2026-11-15) [F]
- **[IRA article](https://support.every.org/hc/en-us/articles/55340641316115-How-can-I-donate-from-my-IRA-to-a-charity-using-Every-org)** (created 2026-09-11; updated 2026-10-05):
  - "Can I use an IRA gift to fund my Every.org account balance? Yes, an IRA gift can be used to fund your account balance with giving credit … fund your account with one large donation from your IRA, and then complete your gifts from your account balance".
  - Also: "Every.org does not determine whether your retirement account or individual circumstances qualify for a QCD".
  - Also: "Every.org is the legal charitable recipient of your gift … we issue an unrestricted grant to the nonprofit".
- **[Asset article](https://support.every.org/hc/en-us/articles/360058166014-How-can-I-donate-stocks-cryptocurrency-or-other-assets)** (updated 2026-10-30): fund the balance and "then you can make multiple smaller donations from your account balance thanks to our DAF structure".
- **[DAF article](https://support.every.org/hc/en-us/articles/360059998953-How-can-I-donate-using-a-Donor-Advised-Fund-DAF)** (updated 2026-11-03): "Funding your account grants you a giving credit balance … think of it like a gift card!"
- **[Gift card article](https://support.every.org/hc/en-us/articles/360057502334-How-do-I-use-a-gift-card-or-giving-credit)** (updated 2026-11-03):
  - The balance is visible in "Payments Overview".
  - Credit unused for 2 years is recognised as "breakage" but "can be redeemed at any time".
  - Gift-card recipients are not entitled to a deduction.
- **Accounting (batch 30):** audited FY2021–23 statements book unredeemed credit as **customer deposits** (a liability).

### 2.4 Application to the three prongs [I]

| Prong | Evidence | Reading |
|---|---|---|
| (i) Separately identified by a donor's contributions | Per-user balance shown in Payments Overview; credit arises from the user's own funding | Met. Every.org keeps a formal per-donor record, which the proposed regulation treats as sufficient even with commingling. It also calls the mechanism a "DAF structure" (a listed factor) |
| (ii) Owned and controlled by the sponsor | Every.org is "the legal charitable recipient", issues an immediate receipt, and holds variance power (state disclosures, batch 30) | Met on Every.org's own legal framing. The **customer-deposit (liability) accounting points the other way**. If Every.org does not own the balance, the gift may be incomplete, which would put the donor's §170 deduction, and therefore QCD prong 408(d)(8)(C), in doubt |
| (iii) Advisory privileges by reason of donor status | The donor chooses recipients from the balance. For gift cards, the donor designates a recipient who then advises | Met. A gift-card recipient fits "person appointed or designated by such donor" (donor-advisor) |
| Exceptions | Recipients are any nonprofit on the platform | Neither exception applies |

**Bottom line [I]:**
- **Funding a giving-credit balance with an IRA distribution looks like a distribution to a "fund or account described in section 4966(d)(2)".** It would fall outside 408(d)(8)(B)(i) and be taxable to the IRA owner. The alternative reading, that the balance is not owned by Every.org, has its own problem: the 408(d)(8)(C) full-deductibility condition.
- **A QCD earmarked to a single named nonprofit** and passed through as an immediate grant is closer to a conduit gift than a donor-advised account. Even so, Every.org's variance power and its practice of crediting undeliverable gifts back as "gift card credit" leave some residual DAF character.
- **Every.org's own classification** will show in its first Form 990 Schedule D (CY2025). It is not yet in the IRS index (last modified 2026-10-21) [F].
- **IRS guidance:** none specific [U]. Notice 2017-73 concerns DAF pledges and benefits, not this question. [Pub. 590-B (2025)](https://www.irs.gov/publications/p590b) describes QCDs as distributions "to an organization eligible to receive tax-deductible contributions" and does not restate the DAF exclusion [F]. So donors relying on IRS publications alone would not see the bar.

---

## 3. P-MOR-02: what happened to the 58 tier-B sponsors' DAFs

### 3.1 Approach
- For each sponsor, every e-filed return from TY2019 to TY2025 was read (359 returns; on average 6.2 per sponsor). For each, the following were recorded:
  - Part IV line 6;
  - Schedule D Part I (DAF column, "funds and other accounts" column, and lines 5–6 legal control);
  - Schedule I recipients and purposes;
  - Schedule N;
  - Schedule D Part XIII and Schedule O text;
  - Part III and Part XI text.
- Each sponsor's exit was then classified (codes in §6).
- Sponsor-level evidence, with the object ID and quote, is in [`tier-b-daf-exit-reasons.csv`](../../data/mission-2026-11-14/tier-b-daf-exit-reasons.csv).

### 3.2 Results

| exit_reason | n | DAFRC exit-reference DAF assets | True exit? |
|---|---|---|---|
| transferred_out_documented | 6 | $23.6m | yes |
| granted_out_to_zero | 4 | $2.6m | yes |
| balance_zeroed_disposition_unstated | 1 | $0.07m | yes (disposition unknown) |
| zero_balance_before_exit | 3 | ~$0 | yes (trivial) |
| reporting_gap_still_reports_dafs | 13 | $54.8m | **no**: line 6 still Yes |
| reporting_gap_resumed | 1 | $3.8m | **no** |
| reclassified_not_daf | 3 | $81.2m (Goldstein $72.4m) | no as a DAF exit (relabelling) |
| daf_labelled_grants_continue_line6_no | 1 | $0.4m | probably not |
| reporting_gap_then_line6_no | 6 | $21.5m | ambiguous |
| undetermined_no_disclosure | 20 | $23.3m | unknown |

**Documented transfers [F]:**
- **Oracle Health Foundation** (formerly First Hand Foundation; 137 DAFs, $15.86m).
  - Schedule O: "THE DONOR-ADVISED FUNDS WERE DISCONTINUED AS OF DECEMBER 31, 2023".
  - Schedule I and Schedule N list "DONOR ADVISED FUND ACCOUNT TRANSFER" grants to 12 sponsors. The largest are NPT $12,311,449, Servant Foundation $964,924, Catholic Community Foundation $775,888, Greater Kansas City CF $547,307, Schwab Charitable $300,476, BofA CGF $205,239, Charityvest $193,569 and Fidelity Charitable $85,199 ([202413179349304206](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413179349304206_public.xml)).
  - This is the clearest tier-B example of donor-directed dispersal to many successor sponsors, with NPT taking 76% of FY2023 Schedule D DAF grants ($12.31m of $16.17m) [C].
- **Columbus Community Foundation (KS).** "A MAJOR PORTION OF THE FUNDS HAVE BEEN MOVED TO THE COMMUNITY FOUNDATION OF SOUTHEAST KANSAS"; total assets fell from $2.01m to $14k ([202421319349301902](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202421319349301902_public.xml)).
- **Women's Foundation of California.** "FBO" DAF grants of $4.07m to Philanthropic Ventures Foundation and $1.92m to American Endowment Foundation ([202111099349301821](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202111099349301821_public.xml)).
- **Cardinal Funds (Ball State).** "IN HOUSE DONOR ADVISED FUNDS PROGRAM WAS OUTSOURCED TO A THIRD PARTY ADMINISTRATOR DURING FY20". The administrator is unnamed ([202111269349300041](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202111269349300041_public.xml)).
- **Levy Family Campus** (formerly Jewish Federation of Silicon Valley). It assigned its "designated giving fund manager" role to the Jewish Federation of Silicon Valley, LLC, and recorded a net-asset transfer of −$11,757,693 ([202221749349301352](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202221749349301352_public.xml)).
- **The Schenectady Foundation, Inc.** "TRANSFER OUT TO THE SCHENECTADY FOUNDATION −108,332", which equals its single DAF ([202102859349301765](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202102859349301765_public.xml)). That the transfer was the DAF is [I].

**Reclassifications [F]:**
- **Goldstein Foundation.** An amended TY2022 return changed "PART IV, LINES 6 AND 11F FROM YES TO NO … SCHEDULE D, PART I - UPDATED TO BLANK" ([202510929349300421](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202510929349300421_public.xml)). It is a pooled fund for the Greater Manhattan Community Foundation.
- **Marietta CF** and **CF of Dickinson County** still answer line 6 Yes. Each now reports only the "funds and other accounts" column.

**Reporting gaps [F]:**
- 13 sponsors answer line 6 Yes in every later return and answer Part I lines 5–6, but leave the count and dollar lines blank. Examples: Tompkins, Kern, Orange & Sullivan, West TN Healthcare, Savannah Jewish Council, Calaveras, Nevada Women's Fund.
- **Gorge CF** returned in FY2025 with 36 DAFs and $5,102,097 ([05B zip member 202631339349305278](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip)).
- **Arctic Slope CF** answers line 6 No but still lists Schedule I grants for "ASRC Donor Advised Fund" ([202302489349302110](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202302489349302110_public.xml)).

**Effect on the exit-rate bounds [C]:**
- The exposure base is 5,746 sponsor-years, and tier A has 11 sponsors.

| Treatment | Exits | Rate |
|---|---|---|
| Original central bound (A + all of tier B) | 69 | 1.20%/yr |
| Remove the 18 clear non-exits | 51 | **0.89%/yr** |
| Also remove the 6 ambiguous cases | 45 | 0.78%/yr |
| Documented exits only (A + 14) | 25 | **0.44%/yr** |

- These are arithmetic alternatives. Re-weighting is for the mortality owner (see P-B32B-01).
- **Donor-asset outcome [I]:** in every tier-B case where the disposition is stated, balances went to other sponsors or were granted out. None was found absorbed into the sponsor's unrestricted funds. This mirrors tier A's finding that all ceased sponsors used Schedule N.

### 3.3 Limits
- **The 20 undetermined sponsors** give no disposition text. Their audited statements (state registries) were not read.
- **Keyword scans can miss** dispositions written without the words "donor", "advised", "transfer" or "fund".
- **The undetermined group includes:**
  - large university foundations whose Part I counts were 1 (Ohio University Foundation, St Lawrence);
  - Washington Women's Foundation and Beaver Creek Wetlands, which have no DAF-reporting e-file in the window read.

---

## 4. P-PRC-02: Givinga Foundation's CY2024 "external bank fraud loss"

| Check | Result | Label |
|---|---|---|
| CY2024 original return ([202522379349301497](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202522379349301497_public.xml), 2025-08-25) and amended return ([202503179349301975](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml), 2025-11-13) | Part IX other expenses: "EXTERNAL BANK FRAUD LOS" $316,184 (management and general); "COST OF SERVICE" $1,123,082; "BANK AND CREDIT CARD FE" $84,552. Part VIII "MISCELLANEOUS INCOME" $93,725 (code 900099). `MaterialDiversionOrMisuseInd` 0; `FSAuditedInd` 1 (separate basis); audit committee yes; preparer Nisivoccia LLP (Mt Arlington, NJ) | F |
| Schedule O | Generic text only: tax status, 990 review, conflict-of-interest and compensation policies, and documents available "upon written request" at 396 Washington Street, Wellesley. **No fraud narrative** | F |
| CY2023 ([202403139349303260](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403139349303260_public.xml)) and amended CY2022 ([202420369349301017](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202420369349301017_public.xml)) | No fraud line in either year. Bank/card fees were $384,069 (CY2023) and $934,941 (CY2022) | F |
| CY2025 return | Not in the IRS 2026 index (last modified 2026-10-21) | F (absence) |
| Audited statements | Not found publicly. The 990 offers them "upon written request". The Massachusetts AG charities database was not queried because it requires a search-form submission | U |
| Press, court records | Web searches for Givinga with fraud, lawsuit, wire, check and ACH terms returned nothing relevant | U |

- **[I]** "External bank fraud" most naturally reads as fraud carried out through Givinga's bank accounts by an outside party, rather than by an insider. The modifier "external" and the No on Part VI line 5 both point that way. The rail (ACH, check or wire) is not stated.
- The $93,725 of miscellaneous income could be a partial recovery, but nothing ties it to the loss.
- This leaves the batch-28 fraud register row unchanged: "bank (unspecified)".

---

## 5. Source register

| ID | Source | Date | Used for |
|---|---|---|---|
| S1 | IRS e-file indexes [2019–2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) | 2026 index last modified 2026-10-21 | Object IDs; CY2025 absences |
| S2 | [GivingTuesday 990 mirror](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413179349304206_public.xml) (347 tier-B objects; 7 Endaoment and Givinga objects) | Read 2026-11-15 | Tier-B, Endaoment and Givinga returns |
| S3 | [IRS 2026_TEOS_XML_05B.zip](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip) (13 members by range request: 12 tier-B plus Endaoment FY2025) | Zip 2026-06 | Returns missing from the mirror, including Endaoment FY2025 and Gorge FY2025 |
| S4 | [Endaoment FY2021 audit](https://storage.googleapis.com/endaoment-static/docs-assets/audit-fy21.pdf); [FY2022–23 audit](https://storage.googleapis.com/endaoment-static/docs-assets/audit-fy22-23.pdf); [legal documentation page](https://docs.endaoment.org/governance/resources/legal-documentation); [audits blog](https://blog.endaoment.org/blog/2022-2023-fiscal-audits-complete) | 2024-03; 2025-03-07; 2025-03-10 | Reconciliation |
| S5 | Endaoment docs: [fee schedule](https://docs.endaoment.org/donors/resources/fee-schedule); [DAF Agreement](https://docs.endaoment.org/governance/documentation/fund-agreement); [onchain recordkeeping](https://docs.endaoment.org/advisors/about/platform-recordkeeping); [llms.txt index](https://docs.endaoment.org/llms.txt); [platform impact API](https://docs.endaoment.org/developers/api/donations/get-total-platform-impact) | Agreement updated 2026-08-14 | Fees; absence of counts |
| S6 | [26 USC 408](https://www.law.cornell.edu/uscode/text/26/408) and [26 USC 4966](https://www.law.cornell.edu/uscode/text/26/4966) (LII) | Read 2026-11-15 | QCD bar; DAF definition |
| S7 | [REG-142338-07, 88 FR 77922](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm) | 2023-11-14 (proposed) | Separate identification, donor-advisor, advisory privileges |
| S8 | [IRS Pub. 590-B (2025)](https://www.irs.gov/publications/p590b) | 2025 edition | IRS QCD description |
| S9 | Every.org help centre: [IRA](https://support.every.org/hc/en-us/articles/55340641316115-How-can-I-donate-from-my-IRA-to-a-charity-using-Every-org); [assets](https://support.every.org/hc/en-us/articles/360058166014-How-can-I-donate-stocks-cryptocurrency-or-other-assets); [DAF](https://support.every.org/hc/en-us/articles/360059998953-How-can-I-donate-using-a-Donor-Advised-Fund-DAF); [gift card](https://support.every.org/hc/en-us/articles/360057502334-How-do-I-use-a-gift-card-or-giving-credit) | Updated 2026-10-05 to 2026-11-03 | Giving-credit facts |
| S10 | `www.every.org/terms` | 403/429 on 2026-11-15 | Not read |
| S11 | Repo: [sponsor-exit-verification.csv](../../data/mission-2026-11-14/sponsor-exit-verification.csv); [sponsor-mortality-analysis.md](sponsor-mortality-analysis.md); [sponsor-fraud-loss-disclosures.csv](../../data/mission-2026-11-14/sponsor-fraud-loss-disclosures.csv) | 2026-11-14/15 | Tier-B list; exposure base; Givinga row |
| S12 | Web searches (Givinga fraud, Givinga audit, Endaoment counts, Growfund) | 2026-11-15 | No relevant hits [U] |

---

## 6. Data dictionary

### `tier-b-daf-exit-reasons.csv` (one row per tier-B sponsor; 58 rows)

| Column | Meaning |
|---|---|
| ein, name, sponsor_type | From `sponsor-exit-verification.csv` |
| dafrc_exit_fy, dafrc_exit_ref_daf_assets, dafrc_exit_ref_daf_accounts | DAFRC exit year and the reference-year DAF values used by the mortality analysis |
| last_period_with_daf_values | Last tax period (YYYYMM) whose Schedule D Part I DAF column has a count or EOY value. This includes zero-value closing returns, and Gorge's resumed FY2025 values |
| last_daf_count, last_daf_eoy_value | Values on that return |
| later_returns_read | Number of e-filed returns read after that period |
| latest_period_read | Latest tax period read |
| line6_yes_years_after_last_values | Later periods in which Part IV line 6 ("maintain DAFs") is Yes |
| latest_line6 | Line 6 on the latest return (raw XML value: 1/true or 0/false) |
| exit_reason | One of the following:<br>- `transferred_out_documented`: text, Schedule I or Schedule N shows the balances moved to named or unnamed successor(s)<br>- `granted_out_to_zero`: final Part I shows grants approximately equal to the prior balance and EOY 0<br>- `balance_zeroed_disposition_unstated`: EOY 0 without matching grants or text<br>- `zero_balance_before_exit`: DAF balance was already 0 in the reference year<br>- `reclassified_not_daf`: amended to line 6 No, or values moved to the "funds and other accounts" column<br>- `reporting_gap_still_reports_dafs`: line 6 Yes on every later return, Part I values blank<br>- `reporting_gap_resumed`: Part I values reappear later<br>- `reporting_gap_then_line6_no`: blank-Part-I years, then line 6 No<br>- `daf_labelled_grants_continue_line6_no`: line 6 No, but grants are still labelled DAF<br>- `undetermined_no_disclosure`: line 6 No with no disposition text |
| evidence_label | F, C, I or U (see header) |
| counterparty, counterparty_ein | Successor or recipient, where named |
| evidence_object_id, source_url | IRS object holding the key evidence. The URL is the GivingTuesday mirror, or the IRS 05B zip member for objects the mirror lacks |
| quote_or_basis | Short quote or calculation basis |
| last_values_object_id | Object of the last return with DAF values |
| recency_admissible | `yes` if the last DAF values are 2020 or later. Otherwise `context`; the later returns are still 2020+ |
| accessed | Access date |

### `queue-proposals-batch32b.csv`
- Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- IDs are P-B32B-01..03.
