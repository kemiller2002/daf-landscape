# State DAF law tracker, 2021–2026 (queue item P-NEW-STL-01)

**Prepared 2026-11-15. Desk research only. No regulator, legislator, sponsor or vendor was contacted. No logins or form submissions. This is research, not legal advice.**

Labels: **[F]** the source states it directly. **[S]** secondary source. **[I]** our inference. Source IDs (SL01…) point to the [source register](#source-register). The row-level data, with one primary-source URL per row, is in [`state-daf-law-tracker-2021-2026.csv`](../../data/mission-2026-11-14/state-daf-law-tracker-2021-2026.csv) (records T01–T24).

**Repo context read first, with governing corrections applied.**
- [`regulation-market-structure-portability.md`](regulation-market-structure-portability.md) §Q-B09: CA AB 1712 failed in 2020; "no DAF reporting law effective in 2025"; AB 488 conditionally excludes DAF sponsors; the 2022 CA AG audit. All three are confirmed and extended here.
- [`queue-batch29-regulation-litigation-crypto.md`](queue-batch29-regulation-litigation-crypto.md) §2–3: state solicitation and registration table, Gov. Code §12599.9 wording, NY Exec. Law §171-a, and the Alaska, Flipcause and GoFundMe actions. Reused, not re-derived.
- [`queue-batch34-escheat-terms.md`](queue-batch34-escheat-terms.md): unclaimed-property law reaches nonprofit holders. Nothing in this file conflicts with it, so it is not repeated.
- [`direction-policy-lobbying-obbba.md`](direction-policy-lobbying-obbba.md) and **governing correction W4-13** ([validation-wave4-report.md](validation-wave4-report.md) #13): the attorneys-general letter is dated **May 21, 2026, led by Minnesota**, with a California release on May 22. This file uses that date.

**Access and robots.txt.** We read robots.txt on every host before fetching from it.
- **Fetched (robots allow):** oag.ca.gov (with its 10-second crawl delay), fppc.ca.gov, nysenate.gov `/legislation/` pages (its `/search` path is disallowed and was not used), malegislature.gov, ag.ny.gov, ag.state.mn.us, sos.ks.gov, apps.legislature.ky.gov (robots.txt returns 404, so nothing is disallowed), data.capitol.hawaii.gov (PDFs allowed; `*.htm` disallowed), lawfilesext.leg.wa.gov, mass.gov `/doc/`, law.cornell.edu, fastdemocracy.com.
- **Not fetched:**
  - leginfo.legislature.ca.gov, legiscan.com and california.public.law serve robots.txt behind a Cloudflare challenge (403), so it could not be read.
  - www.capitol.hawaii.gov and charity.ehawaii.gov return 403 on robots.txt.
  - ilga.gov and cga.ct.gov fail TLS through the proxy.
  - open.pluralpolicy.com disallows `/api/v1/`. Its bill pages returned 404.
  - billtrack50 and philanthropyroundtable.org returned 403 to the fetch tool.
  - Facts from these hosts come only from search-engine snippets and are labelled as such.
- crt.sh was not used.

---

## 1. Headline answers

| Question | Answer |
|---|---|
| **Is there a California DAF annual reporting law (the brief asked about "AB 2936" and a "CT-DAF" form)?** | **No.** Three Wicks bills failed: **AB 1712** (failed 2020-02-03), **AB 2936** (passed the Assembly in June 2020, then died in Senate Judiciary) and **AB 1353** (2021–22). AB 1353 was an intent-only bill that "Died at Desk" on 2022-02-01 [T06–T08; SL06, SL07]. **No "CT-DAF" form exists.** The AG's charities rulemaking page lists Forms PL-1 to PL-4, the CT-series and RRF-1, and none of them is DAF-specific [SL02]. The 2022 AG report is a one-off audit, not a filing duty [SL05]. |
| **Has any state enacted a DAF payout, account-level reporting or donor-intent mandate, 2021–2026?** | **None found.** No such bill was found as introduced either, apart from CA AB 1353, which had no operative text. Massachusetts' bill search finds no "donor advised" bill in the 194th General Court [SL21]. New York has none outside wealth-tax bills (§2.5). Searches for New Jersey, Connecticut and Illinois found no DAF bill, but CT and IL could not be checked at source (§5). |
| **What state rules do name DAFs?** | Four kinds, all 2021 or later. **(1) Platform laws** that exclude a DAF sponsor only if it does not publicly list charities: CA AB 488 / Gov. Code §12599.9 (effective 2023-01-01; regulations 2024–25), and Hawaii Act 205 (2024) as amended by Act 108 (2025), effective 2026-07-01. **(2) Political disclosure:** CA FPPC Reg. 18424.3 (effective 2021-12-22) requires officials to name the sponsor, fund and donor behind DAF-sourced behested payments. **(3) Tax-credit exclusions:** Illinois Gives (2024 Act; 2025 rule) and Kansas K.A.R. 92-12-152 (effective 2026-04-17). **(4) Wealth-tax drafts** that would count DAF gifts: NY A3632 (pending), and CA Proposition 40 by its transfer rule, rejected on 2026-11-03. |
| **AG guidance or enforcement involving DAFs?** | **Letters and reports, no enforcement action against a DAF sponsor.** Sixteen AGs (Minnesota lead) wrote to Fidelity Charitable, Vanguard Charitable and Donor Advised Charitable Giving on 2026-05-21 about SPLC payment holds [T17]. The CA-led multistate letter of 2026-03-03 demands that GoFundMe disclose "the role and nature of any DAF sponsor" [T18]. Alaska sued six platforms in March 2026, with PayPal Giving Fund as a DAF-sponsor conduit [T19]. The NY AG's 2022 *Pennies for Charity* report shows DAF campaigns reported under NY's professional-fundraiser regime [T15]. |
| **UPMIFA and DAFs** | **No state UPMIFA amendment or AG UPMIFA guidance naming DAFs was found.** Massachusetts' revised 2025 endowment guidance does not mention DAFs [T24]. The 2024 Kentucky donor-intent act gives donors standing only for endowment agreements with donor-imposed restrictions, and does not mention DAFs [T23]. |

---

## 2. Findings by theme

### 2.1 California: reporting bills (all failed) and the AG audit

- **AB 1712 (2019–20)** would have required AG rules for DAF sponsor reporting, including fund-level data. It failed on 2020-02-03 (Joint Rule 56) [repo S16]. Pre-2021, so context only.
- **AB 2936 (2019–20), "Supervision of Trustees and Fundraisers for Charitable Purposes Act: donor-advised funds".**
  - The title comes from the official leginfo URL in the search index ([leginfo](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201920200AB2936)); the page was not fetched.
  - It would have created a separate AG classification for DAF sponsors.
  - It passed the Assembly in June 2020 and was then held in Senate Judiciary [S] ([Adler & Colvin, 2020-08-27](https://www.adlercolvin.com/blog/2020/08/27/california-legislation-on-charitable-fundraising-platforms-tabled-until-next-year/)). Pre-2021, so context only.
  - **This is the bill the brief half-remembered. It is not a reporting law.**
- **AB 1353 (2021–22), "Donor-advised funds"** ([leginfo](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202120220AB1353), title from the search index).
  - Introduced 2021-02-19 by Wicks. Last action: "Feb 01, 2022 | Assembly Died at Desk" ([FastDemocracy](https://fastdemocracy.com/bill-search/ca/20212022/bills/CAB00023191/)) [S].
  - Secondary summaries describe it as intent language only, with no operative provisions [S].
  - **New to the repo.** It confirms that no CA DAF reporting bill advanced after 2020.
- **CA AG, "Donor Advised Funds: An Overview"** ([PDF](https://oag.ca.gov/system/files/media/donor-advised-funds-overview.pdf)), created 2022-05-18 [F].
  - **Scope:** 57 sponsors (35 California, 22 national). Selection was California sponsors with over $10m and national sponsors registered in California with over $200m.
  - **Data:** reporting periods from 2016-07-01 to 2020-12-31. Two donation processors were excluded from the results.
  - **Findings:** combined DAF assets of $105.3bn at the end of Year 3. 95% of sponsors had a disbursement policy, 97% a self-dealing policy and 98% an advisory-privileges policy.
  - It is evidence of oversight interest. It creates no filing duty.

### 2.2 Charitable-solicitation law: the platform-law DAF exclusion (CA, HI)

- **California AB 488 / Gov. Code §12599.9.**
  - The AG release of 2024-04-16 announces "the final regulations implementing Assembly Bill 488 (Government Code section 12599.9)" ([CA AG](https://oag.ca.gov/node/584000)) [F].
  - The rulemaking page says that "effective January 1, 2023, charitable fundraising platforms and platform charities are subject to the Attorney General's supervision" [F].
  - **Regulation dates:** OAL approved the regulations on 2024-03-26. They took effect in stages: most on 2024-03-26, §§315 and 328 on 2024-06-12, and §§318–322 on 2025-01-01 ([rulemaking page](https://oag.ca.gov/charities/regs/platforms)) [F].
  - **DAF exclusion:** a sponsor is outside the law only if it "does not list or reference by name one or more recipient charitable organizations for solicitation purposes on its platform for persons who do not have advisory privileges" ([FindLaw §12599.9](https://codes.findlaw.com/ca/government-code/gov-sect-12599-9/), via queue-batch29) [F].
- **Hawaii Act 205 (SLH 2024; S.B. 2983)**, approved 2024-07-05 ([Act 205 PDF](https://data.capitol.hawaii.gov/sessions/sessionlaws/Years/SLH2024/SLH2024_Act205.pdf)) [F].
  - It adds platform rules to HRS ch. 467B.
  - **Same exclusion as California:** a "sponsoring organization of donor advised funds" is not a platform or platform charity if it "does not list or reference by name one or more recipient charitable organizations for solicitation purposes on its platform for persons who do not have advisory privileges". "Donor advised fund" has the §4966(d)(2) meaning.
  - Its original effective date was 2026-01-01.
- **Hawaii Act 108 (SLH 2025; S.B. 1048)**, approved 2025-05-29 ([Act 108 PDF](https://data.capitol.hawaii.gov/sessions/sessionlaws/Years/SLH2025/SLH2025_Act108.pdf)) [F].
  - The legislature found that Act 205 "creates undue burdens", and Act 108 narrows it.
  - It keeps the DAF-sponsor exclusion and adds that a person meeting both definitions "shall be deemed a charitable fundraising platform".
  - It moves the effective date to **2026-07-01**; section 10 took effect on 2025-07-01.
- **New York** has no platform law, as the AG itself noted in 2022 [SL15]. But its *Pennies for Charity* report (Nov 2022) shows DAF fundraising reported as professional-fundraiser campaigns [F]:
  - "Nearly 60% of funds raised was reported by two donor-advised funds (DAFs), Network for Good, which partners with Facebook … and Eaton Vance Distributors". Eaton Vance's campaigns were to "increase contributions to its donor-advised fund, U.S. Charitable Gift Trust".
  - The report warns that platforms that partner with a DAF "may not always disclose that the donation is going to the fund".
  - ([2022 report](https://ag.ny.gov/sites/default/files/reports/2022_pennies_for_charity_report.pdf))
- **[I] What this means.** In CA, HI and NY, a DAF sponsor is regulated as a charitable organization for solicitation, and its paid solicitors register (queue-batch29 §3). Two states now use the same test for when a DAF product becomes a regulated "platform": whether it names charities to people who are not account holders. A public charity directory with "give" buttons is the risk feature. This is the subject of P-B40N9-02.

### 2.3 Political disclosure: California FPPC Reg. 18424.3

- **What it requires** ([text](https://www.fppc.ca.gov/siteassets/documents/legal_div/regulations/01_index/chapter_04/18424.3._Behested_Payment_Reporting_Payments_from_Donor_Advised_Funds.pdf)) [F]:
  - For a behested payment "from a sponsoring organization utilizing a donor advised fund", the reporting official must give the sponsor's name, the fund's name (or "anonymous donor advised fund") and the donor's name (or "anonymous donor"), plus any donor's advisor who exercised discretion.
  - The official must inquire of the sponsor and must amend the report within 10 days of learning more.
  - Single-source rules set how the $5,000 threshold applies. Anonymous-fund payments from one sponsor are aggregated.
  - Definitions follow §4966(d).
- **History:** filed 2021-11-22; operative **2021-12-22**.
- **Observed use** (FPPC staff memo, 2024-11-08; [memo](https://www.fppc.ca.gov/siteassets/documents/agendadocuments/general-items/2024/november/21-bp-staff-memo.pdf)) [F]:
  - "33 of the 2,029 state submissions, or about 1.63%" used the DAF fields. "Only eight of the 33" completed all three.
  - DAF-sourced behested payments by state officials totalled **$1,242,728**.
  - None of the 148 local reports named a DAF.
- **[I] Effect on sponsors:** the rule binds officials, not sponsors. Sponsors may still withhold names, and the anonymous labels cover that case.

### 2.4 State tax rules that treat DAF gifts differently

- **Illinois Gives Tax Credit Act (35 ILCS 60).**
  - The rule defines "Donor advised fund" by §4966(d). A credit-eligible "permanent endowment fund" must be one that "(v) is not a donor advised fund" ([86 Ill. Adm. Code 1050.100 via LII](https://www.law.cornell.edu/regulations/illinois/Ill-Admin-Code-tit-86-SS-1050.100)) [F].
  - The rule took effect 2025-05-23, after an emergency rule of 2024-12-12 [F].
  - The source Act is **P.A. 103-592**, per the ilga.gov ILCS page as shown in the search index (not fetched) [S].
  - Credits apply to tax years ending on or after 2025-12-31 ([IL DOR FAQ](https://tax.illinois.gov/programs/illinoisgives/il-gives-faqs.html), search snippet) [S].
- **Kansas K.A.R. 92-12-152 (Pregnancy Resource Act credit)**, effective **2026-04-17** ([Kansas Register](https://www.sos.ks.gov/publications/Register/Volume-45/Issues/Issue-14/04-02-26-54020.html)) [F]. It provides: "Any taxpayer who contributes to a donor advised fund … shall not be allowed credit for that contribution even if the taxpayer recommends that the donor advised fund contribute the funds to an eligible charitable organization."
- **Washington RCW 82.87.080 (capital gains tax charitable deduction)** ([RCW](https://lawfilesext.leg.wa.gov/Law/RCW/RCW%20%2082%20%20TITLE/RCW%20%2082%20.%2087%20%20CHAPTER/RCW%20%2082%20.%2087%20.080.htm)) [F].
  - The deduction covers gifts above $250,000, capped at $100,000. It is limited to a "qualified organization" that is "principally directed and managed within the state of Washington" (2021 c 196; 2025 c 409).
  - The statute does not mention DAFs. Commentators read it to deny the deduction for gifts to out-of-state DAF sponsors ([Fox Rothschild](https://www.foxrothschild.com/publications/washingtons-capital-gains-tax-why-your-daf-sponsors-location-matters-more-than-you-think)) [S].

### 2.5 Wealth-tax measures that would count DAF gifts

- **New York billionaire mark-to-market tax bills** [F].
  - **Bills:** A5092 (2021–22), S1570 and A3252 (2023–24), and A3632 (2025–26, "In Assembly Committee" as of 2026-11-15).
  - **DAF provision:** each would count property "contributed by the taxpayer … to any private foundation, donor advised fund, and any other entity described in section 501(c) or section 527" of which the taxpayer is a substantial contributor ([A3632](https://www.nysenate.gov/legislation/bills/2025/A3632)).
  - **Status:** the earlier bills died in committee.
- **California Initiative 25-0024A1, "The 2026 Billionaire Tax Act" (Proposition 40)** ([text](https://oag.ca.gov/system/files/initiatives/pdfs/25-0024A1%20%28Billionaire%20Tax%20%29.pdf)) [F].
  - **Transfer rule:** net worth "shall include the value of any property the individual transferred … for less than fair market value after October 15, 2025" above $1m.
  - **Pledges:** pledges made after 2025-10-15 cannot reduce net worth.
  - **[I] DAF effect:** the text does not name DAFs, but by its terms a post-2025-10-15 DAF gift would stay in the donor's base.
  - **Result:** voters rejected it about 52.8% to 47.2% per AP-based reports of 2026-11-09 ([KTVU](https://www.ktvu.com/news/prop-40-californias-billionaire-tax-fails-ballot-box)) [S]. The certified result has not been checked.

### 2.6 AG letters and enforcement touching DAFs (2021–2026)

- **2026-05-21: 16-AG letter (Minnesota lead)** to Fidelity Investments Charitable Gift Fund, Donor Advised Charitable Giving, Inc. and Vanguard Charitable Endowment Program ([MN AG PDF](https://www.ag.state.mn.us/Office/Communications/2026/docs/SPLC_Donor-Advised-Fund_Ltr.pdf); [CA release, 2026-05-22](https://oag.ca.gov/node/623769)) [F].
  - **Signatories:** MN, CA, CO, CT, DE, HI, IL, ME, MD, MA, NV, NY, OR, VT, VA, WA.
  - **Stated basis:** the AGs write as "chief regulators of nonprofits, charities, and charitable trusts" and "representatives of the public and donor intent", citing Restatement (Third) of Trusts §94 and Restatement of Charitable Nonprofit Orgs. §5.01.
  - **Ask:** "We urge you to reconsider your actions and policies". There is no legal demand, deadline or cited state statute.
  - **[I]** It is the first multistate AG communication addressed to DAF sponsors as a class that we found in the window.
- **2026-03-03: CA-led multistate letter to GoFundMe** ([PDF](https://ag.ny.gov/sites/default/files/letters/multistate-letter-on-gofundme-letters-2026.pdf)) [F].
  - **Cited failures:** pages "did not clearly disclose that contributions were made to a DAF sponsor rather than the featured charity", including "the use of a DAF intermediary, that donors can no longer direct the donation".
  - **Demand:** prominent disclosure of "the legal recipient of the donation" and "the role and nature of any DAF sponsor". It adds that "Investigative requests from interested States are also forthcoming".
  - **Signatories:** reported as 21 AGs [S].
- **2026-03-10: Alaska suits against six platforms**, including PayPal and Network for Good ([Alaska Dept. of Law](https://law.alaska.gov/press/releases/2026/031026-FinTech.html), via queue-batch29) [F]. PayPal Giving Fund, a DAF sponsor, is the conduit [S].
- **No enforcement action against a DAF sponsor** for grant discretion, payout or reporting was found in 2021–2026. This agrees with queue-batch29 §2.2.

### 2.7 UPMIFA and donor intent

- **No 2021–2026 state UPMIFA amendment naming DAFs was found, and no AG UPMIFA guidance addressing DAF sponsors.**
  - Massachusetts' "Guidance on Endowments for Charities Facing Financial Challenges" (2025-08-20) has no DAF reference on a text search ([mass.gov](https://www.mass.gov/doc/endowment-guidance-revised-2025/download)) [F].
  - **[I] Why DAFs mostly sit outside these rules:** DAF assets are institutional funds of the sponsor. They are usually wholly expendable and carry advisory privileges, not donor-imposed restrictions, so the UPMIFA endowment-spending and release rules rarely bite.
- **Kentucky SB 70 (2024 RS; Acts ch. 121), signed 2024-04-09** ([Act PDF](https://apps.legislature.ky.gov/law/acts/24RS/documents/0121.pdf)) [F].
  - Lets a "donor" sue for declaratory or injunctive relief over a "donor-imposed restriction" in an "endowment agreement". An "endowment fund" is an institutional fund "not wholly expendable … on a current basis".
  - It does not mention DAFs.
  - **[I]** A standard DAF gift would rarely qualify.
- **Similar acts reported elsewhere:** Kansas (2023), Georgia (2024) and Montana (2025) ([Philanthropy Roundtable](https://www.philanthropyroundtable.org/resource/donor-intent-legislation-over-the-last-10-years/); [Faegre Drinker, 2025-04](https://www.faegredrinker.com/en/insights/publications/2025/4/montana-allows-donor-standing-for-endowment-violations-while-similar-efforts-are-pending-in-oklahoma)) [S]. **Their bill numbers were not verified at source, so they are not in the CSV.**

---

## 3. Tracker summary (full rows in the CSV)

| ID | State | Instrument | Year | Status | DAF relevance | Effective |
|---|---|---|---|---|---|---|
| T01 | CA | AB 488 / Gov. Code §12599.9 | 2021 | enacted | conditional exclusion | 2023-01-01 |
| T02 | CA | 11 CCR §§300–346 (platform regulations) | 2024 | in force | implements exclusion | 2024-03-26 / 06-12 / 2025-01-01 |
| T03 | CA | FPPC Reg. 18424.3 | 2021 | in force | DAF payment disclosure by officials | 2021-12-22 |
| T04 | CA | FPPC staff memo | 2024 | issued | use data | — |
| T05 | CA | AG DAF audit report | 2022 | issued | oversight | — |
| T06 | CA | AB 1353 | 2021 | failed | intent bill | — |
| T07–T08 | CA | AB 2936, AB 1712 | 2020 | failed | context (pre-2021) | — |
| T09 | CA | Init. 25-0024A1 / Prop 40 | 2026 | failed (unofficial count) | transfer rule [I] | — |
| T10–T11 | HI | Act 205 (SB 2983); Act 108 (SB 1048) | 2024; 2025 | enacted | conditional exclusion | 2026-07-01 |
| T12–T14 | NY | A3632; S1570/A3252; A5092 | 2021–25 | pending; failed | counts DAF gifts | — |
| T15–T16 | NY | AG *Pennies* report; Exec. Law §171-a | 2022; in force | issued; in force | solicitation treatment | — |
| T17–T19 | Multistate, AK | SPLC letter; GoFundMe letter; AK suits | 2026 | issued; pending | direct / adjacent | — |
| T20 | IL | Illinois Gives Act and rule | 2024–25 | enacted | DAF excluded from credit | TY ending ≥ 2025-12-31 |
| T21 | KS | K.A.R. 92-12-152 | 2026 | in force | DAF excluded from credit | 2026-04-17 |
| T22 | WA | RCW 82.87.080 | 2021 | in force | sponsor-location test [S] | — |
| T23 | KY | SB 70, Acts ch. 121 | 2024 | enacted | adjacent; no DAF mention | not stated |
| T24 | MA | AG endowment guidance | 2025 | issued | none (negative check) | — |

---

## 4. Relationship to existing repo statements

- **Confirmed:** regulation-market-structure-portability.md says "We found no DAF reporting law effective in 2025". This pass extends that to **2021–2026 and to all states checked**.
- **Added:** AB 2936 (2020) and AB 1353 (2021–22) are missing from the repo. FPPC Reg. 18424.3, the Hawaii Acts 205 and 108, the Illinois and Kansas credit exclusions and the NY wealth-tax DAF clause are also new.
- **Refined (not a correction):** queue-batch29 lists Hawaii's platform law as effective 2026-07-01 from a secondary source. That date is now **confirmed at source** (Act 108 §13), and Hawaii's DAF exclusion copies California's.
- **Governing correction respected:** the SPLC letter is dated 2026-05-21 and led by Minnesota (W4-13).

## 5. Gaps and limits

1. **The negative findings for California (2023–24 and 2025–26), Illinois and Connecticut rest on search-engine results**, because leginfo, LegiScan, ilga.gov and cga.ct.gov could not be fetched (robots.txt unreadable or TLS failure). Massachusetts (site search: no hit in the 194th Court), New York (site search via the search index) and New Jersey (search index only) were checked more directly. Proposal **P-B40N9-01**.
2. **AB 1353 status** rests on a tracker, and its bill title on the leginfo URL in the search index.
3. **Illinois P.A. 103-592** comes from the ilga.gov ILCS page as shown in a search snippet. The credit's start date comes from the IL DOR FAQ snippet.
4. **The Proposition 40 result is the unofficial count.**
5. **No search was made of all 50 states' charitable-solicitation statutes** for DAF-specific wording beyond CA, HI and NY. Proposal **P-B40N9-02** covers the platform-law angle, and **P-B40N9-03** covers tax credits.

---

## 6. Data dictionary (`state-daf-law-tracker-2021-2026.csv`)

| Column | Meaning |
|---|---|
| record_id | T01…T24 |
| state | Two-letter state; "Multistate (…)" for joint AG actions |
| instrument_type | bill, statute, regulation, AG report, regulator report, AG guidance, AG action (letter), AG enforcement (lawsuits), ballot initiative |
| instrument_id | Bill, act, rule or document identifier, exactly as shown in the source |
| session_or_year | Legislative session or year of issue |
| short_title | Official or descriptive title |
| year | Year introduced, enacted or issued |
| status | enacted / in force / failed / pending / issued (with qualifiers) as of 2026-11-15 |
| daf_relevance | direct (names DAFs); indirect (reaches DAF gifts without naming them, or by our reading); adjacent (DAF-related setting but not about DAFs); none found |
| what_it_requires | Operative effect, quoting the source where it is load-bearing |
| effective_date | Effective or operative date per the source; "n/a" for reports, letters and failed bills |
| primary_source_url | Official source (legislature, agency or AG) or an official-text mirror where noted |
| secondary_source_url | Corroborating secondary source, if any |
| verification | fetched_official / official_url_in_search_index / repo-cited / LII mirror, plus notes |
| evidence_label | F, S, I or combinations |
| in_recency_window | Y if 2021–2026; "N (context)" for pre-2021 background |
| notes | Dates, caveats, related items |

---

## Source register

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| SL01 | CA AG release, final AB 488 regulations | official [F] | 2024-04-16 | https://oag.ca.gov/node/584000 |
| SL02 | CA AG rulemaking page, platforms (effective dates; forms list) | official [F] | read 2026-11-15 | https://oag.ca.gov/charities/regs/platforms |
| SL03 | 11 CCR §§314–323 text | official [F] | 2024 | https://oag.ca.gov/system/files/media/Cal-Code-Regs-titl-11-secs-314-323.pdf |
| SL04 | Gov. Code §12599.9 (FindLaw mirror; repo R17) | statute mirror [F] | current | https://codes.findlaw.com/ca/government-code/gov-sect-12599-9/ |
| SL05 | CA AG, "Donor Advised Funds: An Overview" | official [F] | PDF 2022-05-18 | https://oag.ca.gov/system/files/media/donor-advised-funds-overview.pdf |
| SL06 | CA AB 1353 (2021–22), leginfo (title via search index) and FastDemocracy status | official URL [S] / tracker [S] | 2021-02-19 to 2022-02-01 | https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202120220AB1353 ; https://fastdemocracy.com/bill-search/ca/20212022/bills/CAB00023191/ |
| SL07 | CA AB 2936 (2019–20) leginfo (search index); Adler & Colvin | official URL / secondary [S] | 2020-08-27 | https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201920200AB2936 ; https://www.adlercolvin.com/blog/2020/08/27/california-legislation-on-charitable-fundraising-platforms-tabled-until-next-year/ |
| SL08 | CA AB 1712 (repo S16) | tracker [S] | 2020-02-03 | https://legiscan.com/CA/bill/AB1712/2019 |
| SL09 | FPPC Reg. 18424.3 text | official [F] | operative 2021-12-22 | https://www.fppc.ca.gov/siteassets/documents/legal_div/regulations/01_index/chapter_04/18424.3._Behested_Payment_Reporting_Payments_from_Donor_Advised_Funds.pdf |
| SL10 | FPPC staff memo, DAF/proceeding/relationship disclosure data | official [F] | 2024-11-08 | https://www.fppc.ca.gov/siteassets/documents/agendadocuments/general-items/2024/november/21-bp-staff-memo.pdf |
| SL11 | CA Initiative 25-0024A1 text | official [F] | amended Nov 2025 | https://oag.ca.gov/system/files/initiatives/pdfs/25-0024A1%20%28Billionaire%20Tax%20%29.pdf |
| SL12 | KTVU, Prop 40 fails | press [S] | 2026-11-09 | https://www.ktvu.com/news/prop-40-californias-billionaire-tax-fails-ballot-box |
| SL13 | Hawaii Act 205 (SLH 2024), S.B. 2983 | official [F] | approved 2024-07-05 | https://data.capitol.hawaii.gov/sessions/sessionlaws/Years/SLH2024/SLH2024_Act205.pdf |
| SL14 | Hawaii Act 108 (SLH 2025), S.B. 1048 | official [F] | approved 2025-05-29 | https://data.capitol.hawaii.gov/sessions/sessionlaws/Years/SLH2025/SLH2025_Act108.pdf |
| SL15 | NY AG, *Pennies for Charity* (Nov 2022) | official [F] | 2022-11 | https://ag.ny.gov/sites/default/files/reports/2022_pennies_for_charity_report.pdf |
| SL16 | NY A3632 (2025–26) bill page and text | official [F] | read 2026-11-15 | https://www.nysenate.gov/legislation/bills/2025/A3632 |
| SL17 | NY S1570, A3252 (2023–24); A5092 (2021–22) | official [F] | read 2026-11-15 | https://www.nysenate.gov/legislation/bills/2023/S1570 ; https://www.nysenate.gov/legislation/bills/2023/A3252 ; https://www.nysenate.gov/legislation/bills/2021/A5092 |
| SL18 | 16-AG letter to DAF sponsors (MN AG copy); CA release | official [F] | 2026-05-21 / 05-22 | https://www.ag.state.mn.us/Office/Communications/2026/docs/SPLC_Donor-Advised-Fund_Ltr.pdf ; https://oag.ca.gov/node/623769 |
| SL19 | Multistate letter to GoFundMe | official [F] | 2026-03-03 | https://ag.ny.gov/sites/default/files/letters/multistate-letter-on-gofundme-letters-2026.pdf |
| SL20 | Alaska Dept. of Law release (repo-cited) | official [F] | 2026-03-10 | https://law.alaska.gov/press/releases/2026/031026-FinTech.html |
| SL21 | Massachusetts Legislature bill search, "donor advised" | official [F] | run 2026-11-15 | https://malegislature.gov/Bills/Search?SearchTerms=donor+advised |
| SL22 | 86 Ill. Adm. Code 1050.100 (LII mirror) | rule mirror [F] | effective 2025-05-23 | https://www.law.cornell.edu/regulations/illinois/Ill-Admin-Code-tit-86-SS-1050.100 |
| SL23 | IL DOR Illinois Gives FAQ (search snippet only) | official [S] | 2025 | https://tax.illinois.gov/programs/illinoisgives/il-gives-faqs.html |
| SL24 | Kansas Register, K.A.R. 92-12-152 | official [F] | 2026-04-02 (effective 04-17) | https://www.sos.ks.gov/publications/Register/Volume-45/Issues/Issue-14/04-02-26-54020.html |
| SL25 | RCW 82.87.080 | official [F] | current | https://lawfilesext.leg.wa.gov/Law/RCW/RCW%20%2082%20%20TITLE/RCW%20%2082%20.%2087%20%20CHAPTER/RCW%20%2082%20.%2087%20.080.htm |
| SL26 | Fox Rothschild on WA deduction and DAF sponsor location | secondary [S] | 2025–26 | https://www.foxrothschild.com/publications/washingtons-capital-gains-tax-why-your-daf-sponsors-location-matters-more-than-you-think |
| SL27 | Kentucky SB 70 record and Acts ch. 121 | official [F] | signed 2024-04-09 | https://apps.legislature.ky.gov/record/24rs/sb70.html ; https://apps.legislature.ky.gov/law/acts/24RS/documents/0121.pdf |
| SL28 | MA AG endowment guidance (revised) | official [F] | 2025-08-20 | https://www.mass.gov/doc/endowment-guidance-revised-2025/download |
| SL29 | Philanthropy Roundtable; Faegre Drinker on donor-intent acts | secondary [S] | 2025 | https://www.philanthropyroundtable.org/resource/donor-intent-legislation-over-the-last-10-years/ ; https://www.faegredrinker.com/en/insights/publications/2025/4/montana-allows-donor-standing-for-endowment-violations-while-similar-efforts-are-pending-in-oklahoma |
| SL30 | NY Exec. Law §171-a (repo-cited) | official [F] | current | https://www.nysenate.gov/legislation/laws/EXC/171-A |

## 7. Queue proposals

See [`queue-proposals-batch40-n9.csv`](../../data/mission-2026-11-14/queue-proposals-batch40-n9.csv):
- **P-B40N9-01:** verify the negative bill searches in CA, IL and CT by a permitted route.
- **P-B40N9-02:** apply the CA/HI DAF-sponsor platform exclusion test to entrants and sponsors that list charities publicly, and check the CA and HI registries.
- **P-B40N9-03:** inventory state tax credits and deductions that exclude or condition DAF gifts.

## Validation corrections (wave 25A, 2026-11-15) — governing
Source: [validation-wave25a-report.md](validation-wave25a-report.md); register `data/mission-2026-11-14/validation-register-wave25a.csv`.

1. **§2.6, GoFundMe letter (governing replacement).**
   - **Find:** "  - **Signatories:** reported as 21 AGs [S]."
   - **Replace with:** "  - **Signatories:** 23 officials from 21 states: 19 attorneys general (CA, DE, IL, KY, MD, MA, MI, MN, NH, NJ, NM, NY, NC, OK, OR, PA, VT, WA, WI) and 4 secretaries of state (MD, PA, SC, TN), per the letter's signature pages. Responses were requested within 14 days [F; V wave 25A]."
