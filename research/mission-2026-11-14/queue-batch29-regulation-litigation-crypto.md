# State intermediary registration, DAF litigation 2021+, Candid retention and the crypto stress test (P-FAIL-08, P-CMP-07, P-TRM-04, P-FAIL-07)

**Queue items:** P-FAIL-08, P-CMP-07, P-TRM-04, P-FAIL-07 (batch29 B). The full text is in [`research-priority-queue.csv`](../../data/mission-2026-11-14/research-priority-queue.csv).

**Date:** 2026-11-15. **Method:**
- Public sources only: court PDFs in CourtListener RECAP storage, state and IRS primary texts, SEC filings, sponsor reports, and press and law-firm commentary.
- No logins, outreach or form submissions.
- The CourtListener search UI and API returned 403 or required authentication. The docket was reconstructed by probing the public RECAP storage paths for document numbers 1–90.

**Recency rule:** evidence dated 2021 or later. Older items appear only as labelled context.

**This is research, not legal advice.** The statute summaries come partly from a 2023 law-firm survey and should be checked against current law before anyone acts on them.

**Labels:**
- **[F]:** fact stated in a primary document.
- **[S]:** secondary source (law-firm survey, press).
- **[I]:** inference by this agent.
- **[U]:** unknown or not found.

**Builds on:** [failed-daf-startups-deep-research.md](failed-daf-startups-deep-research.md) (FD01, FD13–FD16, with its wave-4 corrections W4-10 and W4-11), [daf-user-complaints-deep-research.md](daf-user-complaints-deep-research.md) (§5.5, with correction W4-16), [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md) (§5 Candid), [regulation-market-structure-portability.md](regulation-market-structure-portability.md) (AB 488 note) and [ai-native-entrant-simulation.md](ai-native-entrant-simulation.md) (R11).

**Files written:**
- [`data/mission-2026-11-14/state-intermediary-registration-2026.csv`](../../data/mission-2026-11-14/state-intermediary-registration-2026.csv): 18 states.
- [`data/mission-2026-11-14/daf-litigation-2021plus.csv`](../../data/mission-2026-11-14/daf-litigation-2021plus.csv): 8 rows, 7 of them 2021+ and 1 pre-2021 context row.
- [`data/mission-2026-11-14/queue-proposals-batch29b.csv`](../../data/mission-2026-11-14/queue-proposals-batch29b.csv): P-B29B-01 to P-B29B-03.

---

## 1. Answers

| Item | Answer | Label |
|---|---|---|
| **P-CMP-07** Peterson v. WaterStone | **Pending. It has not been dismissed.**<br>- **Where it stands:** in D. Colo. No. 1:26-cv-00179-GPG-MDB, WaterStone's motion to dismiss the First Amended Complaint (Doc 34, 2026-04-21) has been fully briefed since 2026-05-26. No ruling appears among the RECAP documents reachable through Doc 58 (2026-10-15).<br>- **Discovery is running.** The court denied WaterStone's motion to stay discovery on 2026-06-11. The parties set **2027-02-14** as the deadline for final productions.<br>- **The queue's source conflict is resolved.** The "dismissed for standing" language in the Greenleaf note refers to *Pinkert*, not *Peterson*.<br>- **Other cases:** no other 2021+ successor-advisor suit against a DAF sponsor was found. The other 2021+ cases are Pinkert (dismissed for standing, affirmed in 2022), Fairbairn (judgment for Fidelity in 2021), the Georgia AG v. SDG Impact Fund (2026, receiver sought), Alaska v. GoFundMe/PayPal et al. (2026, consent) and the California AG order against Flipcause (2025). | F (docket); U (sealed or unbought orders) |
| **P-FAIL-08** State registration for vendors | **Custody is not the general trigger.**<br>- **Most of the 18 states sampled** require a paid solicitor or professional fundraiser to register, and to bond for $10k–$50k, whether or not it holds funds.<br>- **Fundraising counsel or consultants register** in NY, MA, FL, PA, NC, MD, VA, IL, CO and HI.<br>- **Bonds tied to custody:** only CT, NJ, OH, GA and IL tie the bond (and CT and OH tie registration) to custody of contributions.<br>- **Platform-specific laws:** California (AB 488, in force since 2024–25) and Hawaii (in force from 2026-07-01). California's DAF exclusion protects the *sponsor*, and only conditionally. A vendor is excluded only if it "solely" provides technical services.<br>- **Enforcement 2021+:** the CA AG against Flipcause (2025); Alaska's six suits including GoFundMe and PayPal (2026); the 21-AG GoFundMe letter (2026); the Georgia AG against SDG (2026). **No regulator action against Benevity was found.** Benevity and PayPal registered as California platforms on time (press). | F (CA statute and regs, NY definitions, AK release); S (survey bond and fee detail); I (application to vendors) |
| **P-TRM-04** Candid retention | **No contractual right to retain is visible, but the IRS reliance rule requires retention.**<br>- **The licence (2026-09-14)** requires the licensee to "cease … all use of the Candid Data" on termination. It has no record-retention carve-out, and it says the Agreement controls over Exhibits.<br>- **Rev. Proc. 2011-33 §4(2)** makes reliance on third-party BMF data conditional on the grantor retaining "a copy of the report". Treas. Reg. §1.6001-1(e) requires records to be kept while "material".<br>- **Is archiving "use"?** Whether keeping an archived copy counts as "use" is not defined in the licence (**[I]**: contested).<br>- **Escape routes:**<br>  - the sponsor owns any Derivative Work "sufficiently distinct and different from Candid Data";<br>  - grantors may rely on the IRS's own TEOS or BMF data directly, as Candid's FAQ concedes;<br>  - a negotiated Order Form clause. | F (texts); I (conflict and escape routes) |
| **P-FAIL-07** Crypto stress test | **Crypto inflows behave like a high-beta, pro-cyclical channel.**<br>- **Fidelity Charitable** crypto contributions: more than $330M (2021) → $38M (2022, −88%) → $49M (2023) → $786M (2024) → $362M (2025, −54%).<br>- **Shift4's Giving Block earnout** (maximum $246M; $57.8M fair value at acquisition) settled at **$10.4M**: $2.8M cash and $7.6M equity.<br>- **Endaoment:**<br>  - its FY6/2024 Form 990 shows $29.8M of $29.9M in contributions as "CRYPTO ASSET" (99.7%);<br>  - its FY6/2023 return reports only $1.6M and leaves Schedule D Part I blank, which is a data-quality anomaly.<br>- **Large sponsors liquidate on receipt** (Fidelity, NPT). Ren and Daffy let donors hold crypto. | F (reports, filings); I (stress model) |

---

## 2. P-CMP-07: Peterson v. WaterStone and other DAF litigation since 2021

### 2.1 Docket reconstruction (D. Colo. 1:26-cv-00179)

The documents below were retrieved from `storage.courtlistener.com/recap/gov.uscourts.cod.250708/` on 2026-11-15. The documents present are 1, 9, 13, 20, 24, 30, 32, 34, 38, 39, 41–46, 55 and 58.

| Date | Doc | Event | Source |
|---|---|---|---|
| 2026-01-15 | 1 | Complaint and jury demand by Philip G. Peterson "in his capacity as Successor Advisor to the Peterson Family Stewardship Fund". Fund balance "$21,071,102" as of 2023-12-31 | [Doc 1](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.1.0_1.pdf) |
| 2026-03-13 | 20 | WaterStone's first counsel (Taft) moves to withdraw | [Doc 20](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.20.0.pdf) |
| 2026-03-17 | 24 | Motion to dismiss the original complaint | [Doc 24](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.24.0.pdf) |
| 2026-04-07 | 32 | First Amended Complaint | [Doc 32](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.32.0.pdf) |
| 2026-04-21 | 34 | Motion to dismiss the FAC. It attacks breach of contract, implied covenant, negligent misrepresentation (economic-loss rule, no false statement, no reliance), the CCPA claim and declaratory relief | [Doc 34](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.34.0.pdf) |
| 2026-05-12 | 38 | Plaintiff's opposition ("oral argument requested") | [Doc 38](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.38.0.pdf) |
| 2026-05-26 | 42 | WaterStone's reply in support of the MTD | [Doc 42](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.42.0.pdf) |
| 2026-06-11 | 45 | Motion hearing on the partial stay of discovery: "The Motion is DENIED. The parties shall engage in meaningful conferral on staging discovery" | [Doc 45](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.45.0.pdf) |
| 2026-06-29 | 46 | Stage 1 stipulated ESI protocol | [Doc 46](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.46.0.pdf) |
| 2026-08-24 | 55 | Joint status report. Final productions deadline "February 14, 2027". The plaintiff says a document identified people "involved in transferring assets from the Peterson Fund either in February, 2026—after this litigation had already commenced—or in 2025 and earlier" | [Doc 55](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.55.0.pdf) |
| 2026-10-15 | 58 | Video-conference access notice for a further proceeding before Magistrate Judge Dominguez Braswell | [Doc 58](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.58.0.pdf) |

**Reading.**
- **[F]** The case is in discovery while the MTD is pending.
- **[U]** RECAP holds only documents that someone has bought, so an order on the MTD issued after Doc 46 may exist and be missing from storage.
- **[I]** The denial of the discovery stay means the court did not treat the MTD as likely to dispose of the whole case. It is not a merits signal.
- **[I]** The "transfers from the fund" allegation (Doc 55, plaintiff's position) is new relative to the repo's complaint record. If it is substantiated, it moves the case from access and grant-refusal toward the sponsor moving assets during litigation.

**Correction to the repo:** [daf-user-complaints-deep-research.md](daf-user-complaints-deep-research.md) §5.5 says "sources conflict". The status should read: *pending; MTD fully briefed 2026-05-26; discovery stay denied 2026-06-11; production deadline 2027-02-14 (D. Colo. Docs 34, 42, 45, 55)*.

### 2.2 Other 2021+ cases

Detail is in [`daf-litigation-2021plus.csv`](../../data/mission-2026-11-14/daf-litigation-2021plus.csv).

- **Pinkert v. Schwab Charitable.** Dismissed for lack of Article III standing; affirmed at 48 F.4th 1051 (9th Cir. 2022) ([FindLaw](https://caselaw.findlaw.com/court/us-9th-circuit/1912100.html)). Commentary reads the court as leaving advisory privileges potentially enforceable ([Greenleaf Trust](https://greenleaftrust.com/missives/donor-advised-funds-back-in-court/)). [F/S]
- **Fairbairn v. Fidelity Charitable.** Judgment for Fidelity after a bench trial on 2021-02-26. According to the NY Community Trust the donors did not appeal ([NYCT, 2021-11-15](https://thenytrust.org/news/dafs-in-the-news-judges-push-back-on-donors-who-go-to-court/)). [S]
- **Georgia AG v. SDG Impact Fund and its CEO.** A receiver is sought. The suit alleges that SDG distributed 0.185% of up to $10B it claimed to control ([WSB-TV, 2026-09-25](https://www.wsbtv.com/news/local/atlanta/where-did-money-go-ag-sues-charity-spotlighted-by-channel-2/76726H6FXFCW5JQXC2N2VOTEQQ/)). [S]
- **Alaska v. GoFundMe, PayPal, Charity Navigator, JustGiving, Pledgeling and Network for Good** (2026-03-10) ([Alaska Dept. of Law](https://law.alaska.gov/press/releases/2026/031026-FinTech.html)). [F] PayPal Giving Fund, a DAF sponsor, is the conduit behind GoFundMe's nonprofit pages ([NonProfit PRO](https://www.nonprofitpro.com/article/alaska-sues-6-fundraising-platforms-over-unauthorized-nonprofit-donation-pages)). [S]
- **California AG order against Flipcause** (2025-11) ([CA AG](https://oag.ca.gov/news/press-releases/attorney-general-bonta-warns-fundraising-platform-flipcause-immediately-stop-its)). [F]
- **Reported GoFundMe nonprofit class action.** The court is not verified ([Oregon ArtsWatch](https://www.orartswatch.org/nonprofits-hurt-by-gofundme-scheme-can-join-class-action-lawsuit/)). [S/U]
- **Context only (pre-2021):** *Styles v. Friends of Fiji* (Nev. 2019) found a breach of the implied covenant for ignoring recommendations but awarded no damages ([NAEPC newsletter](https://www.naepc.org/events/newsletter/2/2026)). Peterson's FAC Count II uses this theory. [S]

**Pattern [I].**
- **Private plaintiffs against DAF sponsors** have lost on standing (Pinkert) or on proof (Fairbairn). Peterson is the first 2021+ case to reach discovery on successor-advisor rights.
- **Where action against DAF-adjacent entities succeeds,** it comes from regulators (GA, CA, AK). It targets custody failures (SDG, Flipcause) or consent and solicitation conduct (Alaska), not grant discretion.

---

## 3. P-FAIL-08: state registration of DAF vendors, fundraising counsel and coventurers

### 3.1 State table (summary)

The full table, with statutes and URLs, is [`state-intermediary-registration-2026.csv`](../../data/mission-2026-11-14/state-intermediary-registration-2026.csv). Bond and fee figures come from the [Lowenstein Sandler survey of May 2023](https://www.probonopartner.org/wp-content/uploads/2023/12/Summary-Survey-of-State-Charity-Registration-Requirements-May-2023.pdf) [S], except where marked otherwise.

| State | Solicitor / fundraiser bond | Counsel registers? | Counsel bond tied to custody? | Coventurer | Platform law |
|---|---|---|---|---|---|
| CA | $25,000 | Yes | — | Register unless 90-day remit, contract and accounting | **Yes (AB 488)** |
| HI | $25,000 | Yes | No | — | **Yes, from 2026-07-01** |
| NY | $10,000 | Yes | Definitional: no access to funds | Contract and accounting | No |
| MA | $25,000 | Yes ($400) | No | **Register, $25,000 bond** | No |
| FL | **$50,000** | Yes | No | No registration | No |
| PA | $25,000 | Yes | No | not extracted | No |
| NC | $20,000–$50,000 | Licence | No | Accounting only | No |
| MD | $25,000 | Yes ($250) | No | — | No |
| VA | $20,000 | Yes, with bond | No | Written agreement | No |
| OH | $25,000 | Only with custody | **Yes** | **Register, $25,000 bond** | No |
| NJ | $20,000 with custody | Yes | **Yes** | Charity files | No |
| IL | $10,000 with control | Yes | **Yes** | — | No |
| CT | $20,000 | Only with custody | **Yes** | No registration | No |
| GA | $10,000 with possession | Yes | **Yes** | No registration | No |
| WA | $25,000 | — | — | — | No |
| CO | none listed | Yes | No | No registration | No |
| AL | $10,000 | — | — | Register, $10,000 | No |
| AK | $10,000 | — | — | — | No; consent theory applied in 2026 suits |

### 3.2 Key primary texts

**California, Gov. Code §12599.9** ([FindLaw](https://codes.findlaw.com/ca/government-code/gov-sect-12599-9/); regulations [11 CCR 314–323](https://oag.ca.gov/system/files/media/Cal-Code-Regs-titl-11-secs-314-323.pdf)). [F]
- **Definition:** a platform is any entity that "uses the internet to provide an internet website, service, or other platform to persons in this state and performs, permits, or otherwise enables acts of solicitation to occur".
- **Type A** (11 CCR 314(m)) covers "soliciting donations or recommended donations … by listing or referencing by name one or more recipient charitable organizations".
- **Type E** (314(q)) covers a platform "private-labeled or otherwise customized, that is subject to a software as a service license agreement … and allows charitable organizations to solicit donations made to them".
- **Vendor exclusion:** "A vendor that solely provides technical or supportive services to a charitable fundraising platform", for example hosting or "digital payment processing". However, such a vendor that solicits "on its own platform … is a charitable fundraising platform for its own platform".
- **DAF exclusion:** a sponsor is excluded only if it "does not list or reference by name one or more recipient charitable organizations for solicitation purposes on its platform for persons who do not have advisory privileges".
- **Registration date:** registration has been required since 2024-06-12 ([DWT, 2024-06](https://www.dwt.com/insights/2024/06/california-ab-488-charitable-funds-rules-in-effect)). [S]

**Hawaii, HRS 467B** ([Frankfurt Kurnit, 2026-07-29](https://advertisinglaw.fkks.com/post/102nf2j/hawaiis-charitable-platform-law-now-in-effect)). [S]
- Registration is required from 2026-07-01.
- Per the article, the AG's FAQ says a platform "may be a CFP even if it does not itself ask for the donation".

**New York, Exec. Law §171-a** ([NY Senate](https://www.nysenate.gov/legislation/laws/EXC/171-A)). [F]
- **Fund raising counsel:** one who "plans, manages, advises, or assists … but who does not have access to contributions or other receipts from a solicitation or authority to pay expenses".
- **Professional fund raiser:** one who "plans, manages, conducts, carries on, or assists in connection with a charitable solicitation". The definition does not turn on custody.

**Alaska** ([Dept. of Law, 2026-03-10](https://law.alaska.gov/press/releases/2026/031026-FinTech.html)). [F]
- "The Charitable Solicitations Act requires solicitors to obtain consent before fundraising on behalf of a charity."

### 3.3 Enforcement against giving platforms since 2021

- **California v. Flipcause** (order 2025-11-12, release 2025-11-14). The AG said Flipcause was "not properly registered as a fundraising platform". It ordered Flipcause to stop operating, account for assets since 2015 and move cash to a blocked account, and it sought penalties up to $70,000 ([CA AG](https://oag.ca.gov/news/press-releases/attorney-general-bonta-warns-fundraising-platform-flipcause-immediately-stop-its)). [F] Press reports a 2019 notice telling Flipcause to register as a professional fundraiser, and an appeal filed on 2025-12-12 ([Oakland Voices, 2025-12-13](https://oaklandvoices.us/2025/12/13/california-donation-fundraising-platform-compliance-attorney-general/)). [S]
- **California registry compliance.** Of 205 vetted platforms, 37 (18%) were unregistered or expired. Benevity, Blackbaud, PayPal and Mastercard registered on time (same source). [S]
- **Alaska** suits against six platforms (2026-03), and a **21-AG letter** to GoFundMe led by California (2026-03) ([Chronicle, 2026-04-20](https://www.philanthropy.com/news/lawsuits-against-gofundme-paypal-fire-a-fundraising-warning-shot/)). [S]
- **PayPal Giving Fund:** the 2020 NY-led 23-state settlement is pre-2021 context ([NY AG](https://ag.ny.gov/press-release/2020/attorney-general-james-announces-settlement-paypal-charitable-giving-fund-inc)). The 2026 Alaska suit names PayPal. [F]
- **Benevity:** no regulator action was found. [U, absence]

### 3.4 Implications for an entrant that never holds funds [I]

1. **Not holding funds removes the bond in only about five of 18 states** (CT, NJ, OH, GA, IL). Elsewhere the role decides the outcome:
   - a vendor paid to *plan or run* a DAF sponsor's donor-acquisition campaigns is fund raising counsel at minimum;
   - a vendor that *conducts* solicitation (its own brand, its own copy, paid per contribution) risks professional fundraiser or solicitor status and bonding.
2. **The sponsor is the "charitable organization".** Inviting donors to open or fund DAF accounts is solicitation *for the sponsor*, so DAF sponsors are not outside these statutes.
3. **California and Hawaii pose the most specific risk.**
   - A donor-facing app that lists named charities for "recommended donations" matches Type A.
   - A white-label giving app licensed to a sponsor under SaaS terms matches Type E.
   - The DAF exclusion covers the sponsor, not its vendor.
   - Only a back-end vendor that "solely" provides technical services escapes, and even that vendor becomes a platform for any consumer-facing app of its own.
   - **Cost:** budget CA registration ($625 per year per secondary sources), annual PL-4 reports, the consent and disclosure rules, and the 2026 Hawaii regime.
4. **Charity directories carry consent risk.** A grant search built from IRS BMF data with "give" buttons resembles the pages Alaska sued over. California allows listing without consent only with disclosures and opt-out.
5. **Design choices that minimise exposure:**
   - contract as the sponsor's technology provider on flat SaaS fees, not a percentage of contributions;
   - the sponsor owns donor-facing solicitation copy;
   - no access to funds and no authority to pay expenses (this tracks the NY counsel definition);
   - no title claim to in-flight gifts (the Flipcause lesson, FD16);
   - register in CA and HI where the app is consumer-facing;
   - check coventurer rules (MA, OH and AL require a bond) before any "we give X% to your DAF" promotion.

---

## 4. P-TRM-04: can a sponsor keep Candid Charity Check results after its licence ends?

### 4.1 Texts

**Candid API License Agreement**, "Last updated September 14, 2026" ([Candid](https://candid.org/terms-of-service/api-license-agreement/)). [F]
- **Termination §4.c.v:** "Licensee shall cease, and shall cause its Authorized Users to cease, all use of the Candid Data".
- **Candid Data** means "the data and information regarding nonprofit entities that are made available to Licensee via the Candid API".
- **Derivative Works (§1.i / §2.b):** a Derivative Work is "any work based on or derived from the Candid Data that is sufficiently distinct and different from Candid Data". The licensee owns it: "Licensee shall be the sole owner of all Intellectual Property rights to any Derivative Works created by Licensee".
- **Precedence (§10.l):** "In the event of a conflict between the Agreement and an Exhibit, the terms of the Agreement shall control". The Order Form is not expressly given precedence.
- **Absent:** there is no retention, archival or backup clause. §9.b permits *disclosure* compelled by law; it does not permit retention.
- **Audit:** Candid may audit once a year during the term and for two years after (prior file).

**Candid developer docs** ([getting started](https://developer.candid.org/reference/get-started-with-charity-check.md), updated 2026-09-07; [FAQ](https://developer.candid.org/reference/faqs-charity-check.md), updated 2026-09-07). [F]
- "Download a timestamped Charity Check PDF document to archive for due diligence."
- "[Rev. Proc. 2011-33] allows grantors to rely on third-party resources, such as Charity Check, to obtain required Business Master File (BMF) data".
- The FAQ also says grantors "may rely on either the Tax Exempt Organization Search or the Exempt Organizations Business Master File Extract".

**IRS.** [F]
- **Rev. Proc. 2011-33 §4** ([IRB 2011-25](https://www.irs.gov/irb/2011-25_IRB)): reliance on third-party BMF data requires a report with name, EIN and foundation status, "a statement that the information is from the most current update of the BMF extract and the BMF extract revision date", and the date and time. It also requires that "(2) The grantor or contributor retains a copy of the report in hard copy or electronically."
- **Treas. Reg. §1.6001-1(e)** ([eCFR](https://www.ecfr.gov/current/title-26/section-1.6001-1)): records "shall be retained so long as the contents thereof may become material in the administration of any internal revenue law".
- **§4966 regulations** remain proposed ([Federal Register, 2023-11-14](https://www.federalregister.gov/documents/2023/11/14/2023-24982/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966)). The Council on Foundations reported on 2026-05-08 that they had not been finalized ([CoF](https://cof.org/node/20145)). [S]

### 4.2 Analysis [I]

1. **The two sets of rules conflict.** The IRS reliance safe harbour requires retention. The public licence requires the licensee to stop all use of Candid Data and has no retention carve-out. Candid's own docs encourage archiving.
2. **What "use" means decides the question.** Keeping a PDF in a closed grant file as audit evidence is arguably not "use" in the commercial sense. Producing it to the IRS on examination could fall under §9.b's compelled-disclosure language. Re-running eligibility logic on the stored payloads after termination would be use. None of this is settled by the text.
3. **Order Form.** Because the Agreement controls over Exhibits and the Order Form is not given precedence, a sponsor wanting certainty needs an express survival clause in the main terms or a signed amendment. A carve-out placed only in an Exhibit may not be enough.
4. **Practical mitigations:**
   - (a) Record the sponsor's own determination (status, date, BMF revision, OFAC result) in its grant file as a Derivative Work, or as the sponsor's own business record.
   - (b) Capture the IRS TEOS or BMF evidence directly alongside the Candid result. That reliance path needs no licence.
   - (c) Negotiate a "records retention for legal and tax compliance" survival clause.
5. **Unknowns:**
   - Whether a Charity Check PDF shows the BMF extract *revision date* that §4(1)(B) requires. Public field docs show a timestamp and IRB dates, but no BMF revision field was found.
   - The OFAC refresh cadence is still not stated. [U]

**A5 Candid Y1 (portability) [I].** The finding supports moving Y1 from 3 to 2, as the prior file suggested, unless P-B29B-03 finds a retention carve-out.

---

## 5. P-FAIL-07: crypto-exposure stress test, 2021–2025

### 5.1 Observed series

| Entity | 2021 | 2022 | 2023 | 2024 | 2025 | Source |
|---|---|---|---|---|---|---|
| **Fidelity Charitable crypto contributions** | >$330M | $38M | $49M | $786M (2026 table: $787M) | $362M | [2022](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2022-giving-report.pdf), [2023](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf), [2024](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf), [2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf), [2026](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) Giving Reports [F] |
| YoY change (computed) | — | **−88%** | +25% (FC) / +29% (computed) | ×16 (FC says "14 times") | **−54%** | [I] arithmetic |
| **The Giving Block, crypto processed** | $69.6M | Not reported. All-time ">$125M" by the 2023 report, so 2022 was roughly ≥$50M | n/r | Implied ≈$60M (2025 is ">$100M", "+66%") | >$100M; 22,343 donations; cumulative >$300M | [2022 BW release](https://www.businesswire.com/news/home/20220202005238/en); [2023 report PDF](https://go.thegivingblock.com/hubfs/Annual%20Report/2023%20Annual%20Report%20on%20Crypto%20Philanthropy.pdf); [2026 report page](https://thegivingblock.com/annual-report/); [StockTitan copy of the 2026 release](https://www.stocktitan.net/news/FOUR/the-giving-block-s-2026-annual-report-reveals-the-rise-of-the-du8tnwo3vg3d.html) [F; 2022 and 2024 = I] |
| **Shift4 / TGB earnout** | — | Acquisition-date fair value $57.8M (max $246M). FY2022 revaluation $(47.1)M; year-end liability $10.9M | Final earnout **$10.4M** ($2.8M cash, $7.6M equity) | — | — | Shift4 10-K [FY2022](https://www.sec.gov/Archives/edgar/data/1794669/000179466923000006/four-20221231.htm), [FY2023](https://www.sec.gov/Archives/edgar/data/1794669/000179466924000007/four-20231231.htm) [F] |
| **TGB crypto settlement assets held for users** (year-end) | — | $1.8M | $3.5M | $5.7M | n/f | Shift4 10-K [FY2022](https://www.sec.gov/Archives/edgar/data/1794669/000179466923000006/four-20221231.htm), [FY2023](https://www.sec.gov/Archives/edgar/data/1794669/000179466924000007/four-20231231.htm), [FY2024](https://www.sec.gov/Archives/edgar/data/1794669/000179466925000011/four-20241231.htm) [F] |
| **Endaoment Form 990** (fiscal years ending June) | FY6/21: no e-file found in index | FY6/22: contributions $41.34M (non-cash $22.60M); Sch. D DAF grants $24.98M; DAF year-end $15.31M | FY6/23: $1.62M contributions, Sch. D Part I blank (**anomaly**; DAFRC imputes $37.9M) | FY6/24: $29.88M, of which $29.79M Sch. M "CRYPTO ASSET" (99.7%); DAF grants $34.82M; DAF year-end $17.11M | FY6/25: contributions $25.03M; DAF value $18.9M; grants $18.68M (repo breadth profile) | IRS e-file XML [202323209349303992](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202323209349303992_public.xml), [202411369349317486](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411369349317486_public.xml), [202542899349300104](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542899349300104_public.xml); `breadth-entity-profiles.csv` [F] |

**Notes on the series:**
- **Endaoment's own impact page** reportedly shows calendar-2024 inbound donations of about $10.2M, down 58.7% from 2023 ([endaoment.org/impact](https://endaoment.org/impact), seen via search summary only; [S]). This does not reconcile with the 990 figures and needs checking.
- **Endaoment's FY6/24 990 is internally inconsistent:** Schedule D DAF contributions ($36.36M) exceed Part VIII total contributions ($29.88M). [F]
- **Market context:** Bitcoin lost "more than 75%" in fall 2022 ([Fidelity Charitable, 2024-05-31](https://www.fidelitycharitable.org/articles/can-cryptocurrency-still-do-good.html)). [F] Secondary sources put the 2025–26 decline at roughly 50% from the ~$126k October 2025 peak, and 32% below it a year later ([Crypto Briefing](https://cryptobriefing.com/bitcoin-down-32-percent-year-after-record/); [Galaxy](https://www.galaxy.com/insights/research/bitcoin-drawdown-nears-40-weakness-suggests-lower-prices-coming)). [S]

### 5.2 Sponsor crypto handling

| Sponsor | Policy | Label |
|---|---|---|
| Fidelity Charitable | Accepted crypto "liquidating the assets and unlocking these funds for philanthropy" ([2022 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2022-giving-report.pdf)). Accepts BTC, ETH and LTC (2024 article) | F |
| NPT | "Cryptocurrency cannot be held as an investment, according to NPT's investment policy"; "liquidation usually occurs shortly after receipt" ([NPT, 2025-05-20](https://www.nptrust.org/philanthropic-resources/philanthropist/make-a-charitable-impact-with-crypto-and-donor-advised-funds/)) | F |
| Ren (white-label administrator) | Lets donors keep BTC or ETH in a DAF. The account "must maintain a 15% value in traditional (liquid) assets". Wrap fee 1.5%–2.5% ([Ren, 2025-09-30](https://www.reninc.com/blog/invest-crypto-in-a-donor-advised-fund)) | F |
| Daffy | Offers Bitcoin, Ethereum and mixed portfolios through Coinbase, plus spot-Bitcoin ETF options ([Daffy](https://www.daffy.org/resources/crypto-bitwise-portfolios)) | F |
| Endaoment | Holding policy not verified | U |

### 5.3 Stress model for a crypto-heavy DAF entrant [I, illustrative]

**Shock sizes come from observed falls:**
- Fidelity's crypto inflow fell 88% in 2022 and 54% in 2025.
- The TGB revenue-multiple earnout came in at 4% of its maximum and 18% of its acquisition-date fair value.

**Model A: revenue = fee × contribution volume** (processor or intake-led entrant). If crypto is share *s* of inflow, a 2022-style shock cuts inflow by 0.88·*s*: −44% at *s*=50%, −70% at *s*=80% and −88% at *s*=100%. A 2025-style shock (−54%) gives −27%, −43% and −54%. Endaoment's FY6/24 mix (99.7% crypto) puts it at the *s*≈1 end.

**Model B: revenue = basis points × AUM.**
- Where the sponsor liquidates on receipt (Fidelity, NPT), AUM carries no price exposure after receipt. The hit is to *new* inflow only, and with a lag.
- Where donors may hold crypto (Ren, Daffy portfolios), AUM falls with price (2022: more than 75%), which compounds the inflow loss.

**Model C: acquirer valuation.** Revenue-multiple earnouts struck at a cycle peak are where the loss lands. TGB was bought in February 2022 and its earnout was measured from March 2022 to February 2023.

**Implications [I]:**
1. Treat crypto intake as optional and countercyclical-unsafe. Size fixed costs to the trough (2022 or 2023), not the peak (2021 or 2024).
2. Liquidate at receipt by default. If holding is offered, require a liquid floor, as Ren's 15% rule does.
3. The recovery is fast but unpredictable: Fidelity's crypto inflow multiplied 16-fold between 2023 and 2024. Optionality has value, but it cannot carry a business plan.
4. An entrant that depends on one crypto-native sponsor (e.g. Endaoment, almost all crypto) inherits that sponsor's beta.

---

## 6. Source register

| ID | Source | Date | Used for |
|---|---|---|---|
| R01 | [Peterson v. CCF, D. Colo. Doc 1](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.1.0_1.pdf) | 2026-01-15 | §2 |
| R02 | [Doc 34 MTD FAC](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.34.0.pdf) | 2026-04-21 | §2 |
| R03 | [Doc 38 opposition](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.38.0.pdf) ; [Doc 42 reply](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.42.0.pdf) | 2026-05 | §2 |
| R04 | [Doc 45 minutes](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.45.0.pdf) | 2026-06-11 | §2 |
| R05 | [Doc 55 joint status report](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.55.0.pdf) | 2026-08-24 | §2 |
| R06 | [Doc 58 VTC notice](https://storage.courtlistener.com/recap/gov.uscourts.cod.250708/gov.uscourts.cod.250708.58.0.pdf) | 2026-10-15 | §2 |
| R07 | [Foley on Peterson](https://www.foley.com/insights/publications/2026/05/new-lawsuit-tests-the-limits-of-donor-advised-fund-advisory-privileges/) | 2026-05 | §2 |
| R08 | [NAEPC newsletter (Fox)](https://www.naepc.org/events/newsletter/2/2026) | 2026 | §2 |
| R09 | [Pinkert, 9th Cir.](https://caselaw.findlaw.com/court/us-9th-circuit/1912100.html) | 2022 | §2 |
| R10 | [NYCT: judges push back](https://thenytrust.org/news/dafs-in-the-news-judges-push-back-on-donors-who-go-to-court/) | 2021-11-15 | §2 |
| R11 | [WSB-TV: GA AG sues SDG](https://www.wsbtv.com/news/local/atlanta/where-did-money-go-ag-sues-charity-spotlighted-by-channel-2/76726H6FXFCW5JQXC2N2VOTEQQ/) | 2026-09-25 | §2 |
| R12 | [Alaska Dept. of Law release](https://law.alaska.gov/press/releases/2026/031026-FinTech.html) | 2026-03-10 | §2, §3 |
| R13 | [Alaska's News Source](https://www.alaskasnewssource.com/2026/03/11/alaska-sues-gofundme-paypal-others-over-thousands-unauthorized-charity-pages/) | 2026-03-11 | §3 |
| R14 | [Chronicle: platform lawsuits](https://www.philanthropy.com/news/lawsuits-against-gofundme-paypal-fire-a-fundraising-warning-shot/) | 2026-04-20 | §2, §3 |
| R15 | [CA AG: Flipcause](https://oag.ca.gov/news/press-releases/attorney-general-bonta-warns-fundraising-platform-flipcause-immediately-stop-its) | 2025-11-14 | §3 |
| R16 | [Oakland Voices: CA platform compliance](https://oaklandvoices.us/2025/12/13/california-donation-fundraising-platform-compliance-attorney-general/) | 2025-12-13 | §3 |
| R17 | [Cal. Gov. Code §12599.9 (FindLaw)](https://codes.findlaw.com/ca/government-code/gov-sect-12599-9/) | current | §3 |
| R18 | [11 CCR 314–323 (OAG PDF)](https://oag.ca.gov/system/files/media/Cal-Code-Regs-titl-11-secs-314-323.pdf) | 2024 | §3 |
| R19 | [DWT: AB 488 in effect](https://www.dwt.com/insights/2024/06/california-ab-488-charitable-funds-rules-in-effect) | 2024-06 | §3 |
| R20 | [FKKS: Hawaii platform law](https://advertisinglaw.fkks.com/post/102nf2j/hawaiis-charitable-platform-law-now-in-effect) | 2026-07-29 | §3 |
| R21 | [NY Exec. Law §171-a](https://www.nysenate.gov/legislation/laws/EXC/171-A) | current | §3 |
| R22 | [Lowenstein Sandler 50-state survey](https://www.probonopartner.org/wp-content/uploads/2023/12/Summary-Survey-of-State-Charity-Registration-Requirements-May-2023.pdf) | 2023-05 | §3 |
| R23 | [NY AG 2020 PPGF settlement](https://ag.ny.gov/press-release/2020/attorney-general-james-announces-settlement-paypal-charitable-giving-fund-inc) | 2020 (context) | §3 |
| R24 | [Candid API License Agreement](https://candid.org/terms-of-service/api-license-agreement/) | 2026-09-14 | §4 |
| R25 | [Candid Charity Check getting started](https://developer.candid.org/reference/get-started-with-charity-check.md) ; [FAQ](https://developer.candid.org/reference/faqs-charity-check.md) ; [fields](https://developer.candid.org/reference/interpret-charity-check-data-fields.md) | 2026-09-07 / 2026-11-10 | §4 |
| R26 | [Rev. Proc. 2011-33, IRB 2011-25](https://www.irs.gov/irb/2011-25_IRB) | 2011 (current law) | §4 |
| R27 | [26 CFR 1.6001-1](https://www.ecfr.gov/current/title-26/section-1.6001-1) | current | §4 |
| R28 | [§4966 proposed regs](https://www.federalregister.gov/documents/2023/11/14/2023-24982/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966) ; [CoF status](https://cof.org/node/20145) | 2023-11-14 ; 2026-05-08 | §4 |
| R29 | Fidelity Charitable Giving Reports [2022](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2022-giving-report.pdf)–[2026](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) | 2022–2026 | §5 |
| R30 | [TGB 2023 annual report PDF](https://go.thegivingblock.com/hubfs/Annual%20Report/2023%20Annual%20Report%20on%20Crypto%20Philanthropy.pdf) ; [2026 report page](https://thegivingblock.com/annual-report/) | 2023 ; 2026-03 | §5 |
| R31 | Shift4 10-K [FY2022](https://www.sec.gov/Archives/edgar/data/1794669/000179466923000006/four-20221231.htm), [FY2023](https://www.sec.gov/Archives/edgar/data/1794669/000179466924000007/four-20231231.htm), [FY2024](https://www.sec.gov/Archives/edgar/data/1794669/000179466925000011/four-20241231.htm) | 2023–2025 | §5 |
| R32 | Endaoment 990 XML (three object IDs in §5.1) | 2023–2025 | §5 |
| R33 | [NPT crypto guide](https://www.nptrust.org/philanthropic-resources/philanthropist/make-a-charitable-impact-with-crypto-and-donor-advised-funds/) ; [Ren crypto DAF](https://www.reninc.com/blog/invest-crypto-in-a-donor-advised-fund) ; [Daffy crypto portfolios](https://www.daffy.org/resources/crypto-bitwise-portfolios) | 2025 | §5 |
| R34 | [Fidelity Charitable: Can crypto still do good](https://www.fidelitycharitable.org/articles/can-cryptocurrency-still-do-good.html) | 2024-05-31 | §5 |
| R35 | [Crypto Briefing](https://cryptobriefing.com/bitcoin-down-32-percent-year-after-record/) ; [Galaxy](https://www.galaxy.com/insights/research/bitcoin-drawdown-nears-40-weakness-suggests-lower-prices-coming) | 2026 | §5 (context) |

---

## 7. Data dictionary

### `state-intermediary-registration-2026.csv`

| Column | Meaning |
|---|---|
| state | USPS code |
| statute | Main charitable-solicitation statute and sections |
| professional_solicitor_or_fundraiser | Registration and filing duties for paid solicitors, professional or commercial fundraisers |
| solicitor_fundraiser_bond_usd | Surety bond amount; conditions noted |
| fundraising_counsel_consultant | Duties for counsel or consultants who do not solicit |
| counsel_custody_trigger | Whether counsel registration or bond depends on custody of or access to contributions |
| commercial_coventurer | Duties for commercial coventurers (charitable sales promotions) |
| coventurer_bond_usd | Coventurer bond, if any |
| online_platform_law | Whether a platform-specific regime exists |
| platform_law_status | Effective or in-force dates |
| daf_sponsor_exclusion_in_platform_law | DAF sponsor carve-out text or summary |
| tech_vendor_exclusion_in_platform_law | Technical-vendor carve-out |
| enforcement_2021plus_against_giving_platforms | Regulator actions since 2021 found |
| non_custodial_daf_vendor_exposure_inference | Agent's HIGH/MEDIUM/LOW reading for a vendor that never holds funds [I] |
| evidence_label | confirmed / secondary / unknown |
| source_urls, source_dates | Citations and dates |

### `daf-litigation-2021plus.csv`

| Column | Meaning |
|---|---|
| case_id | LIT-NN |
| caption, court, docket_or_citation | Case identifiers |
| filed_date | As known (year only where the day is unverified) |
| plaintiff_type, defendant, defendant_type | Parties |
| dispute_type, claims_or_theory | Subject and legal theories |
| amount_at_issue_usd | Fund balance or amount alleged (not damages awarded) |
| status_as_of_2026-11-15, last_public_event_date | Procedural status |
| outcome_or_holding | Result, or "None yet" |
| recency_flag | 2021+ or pre-2021 context |
| evidence_label, source_urls, notes | Provenance |

### `queue-proposals-batch29b.csv`

Columns follow [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md).

---

## 8. Limits

- **RECAP coverage is partial.** The docket page and API were blocked, so absence of an MTD order is absence in RECAP only.
- **The state table relies on a May 2023 survey** for bonds and fees. Only CA, NY and AK texts were read at the primary level. Amounts may have changed.
- **Not covered:** platform or vendor regimes for money transmission (custody-related), and state "commercial coventurer" definitions as they apply to round-ups.
- **Crypto shares of total inflow** for Fidelity could not be computed, because total contributions were not extracted. The Endaoment 990 series has a FY6/2023 filing anomaly.
- **Allegations in pending cases are not findings.**

## Validation corrections (wave 14, 2026-11-15) — governing
Source: [validation-wave14-report.md](validation-wave14-report.md); register `data/mission-2026-11-14/validation-register-wave14.csv`.

1. **Line 35 (§1, P-TRM-04).**
   - Replace: "**Rev. Proc. 2011-33 §4(2)** makes reliance on third-party BMF data conditional on the grantor retaining \"a copy of the report\"."
   - With: "**Rev. Proc. 2018-32 §8.01(2)** makes reliance on third-party BMF data conditional on the grantor retaining \"a paper or electronic copy of the report\". (Rev. Proc. 2018-32 superseded Rev. Proc. 2011-33, whose §4(2) is cited by Candid's FAQ, from 2018-05-16.)"
2. **Line 183 (§4.1 IRS).**
   - Replace the "Rev. Proc. 2011-33 §4" bullet with: "**Rev. Proc. 2018-32 §8.01** ([IRB 2018-23](https://www.irs.gov/irb/2018-23_IRB)), which \"modifies and supersedes … Rev. Proc. 2011–33\" (effective May 16, 2018). Reliance on third-party EO BMF data requires two things. (1) The report must include name, EIN and foundation status, deductibility, \"the revision date of the EO BMF Extract containing the information\", and the date and time provided. (2) \"The grantor or contributor retains a paper or electronic copy of the report.\" Candid's FAQ still cites the superseded Rev. Proc. 2011-33."
3. **Line 197 (§4.2, Unknowns).** Replace "that §4(1)(B) requires" with "that Rev. Proc. 2018-32 §8.01(1)(b) requires".
4. **Line 283 (R26).** Replace the row with: "| R26 | [Rev. Proc. 2018-32, IRB 2018-23](https://www.irs.gov/irb/2018-23_IRB) (supersedes [Rev. Proc. 2011-33, IRB 2011-25](https://www.irs.gov/irb/2011-25_IRB)) | 2018-05-16 (current) | §4 |".
5. **Line 34 (§1, P-FAIL-08) and line 144 (§3.4 item 1).**
   - Replace: "only CT, NJ, OH, GA and IL tie the bond" / "in only about five of 18 states (CT, NJ, OH, GA, IL)"
   - With: "of the 18 states sampled, only CT, NJ, OH, GA and IL tie the bond … (the same 2023 survey shows custody-triggered counsel bonds in MN, NH, RI and LA, which are outside the sample, so this is not a national ratio)".
6. **Line 75 (§2.2 Alaska).** Replace "JustGiving, Pledgeling and Network for Good" with "JustGiving, Pledge (\"Pledge to\" in the release) and Network for Good".
7. **Line 215 (§5.1, Endaoment row, FY6/25 cell).** Append: "The FY6/25 990 (202631359349315978) is in the 2026 IRS index but not yet on the mirror. FY6/22 also shows Sch. D DAF contributions ($43.24M) above Part VIII ($41.34M)."
