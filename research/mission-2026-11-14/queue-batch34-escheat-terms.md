# Batch 34C: escheat of voided DAF grant checks (P-PAY-04), DAFgiving360 2026 Program Policies (P-B33B-02), top-20 terms census (P-TRM-05), Fidelity's RIA custody minimum and the adviser channel (P-VCM-04), and the primary adviser-survey figures (P-ANL-02)

**Date:** 2026-11-15. **Queue items:** P-PAY-04, P-B33B-02, P-TRM-05, P-VCM-04, P-ANL-02 (`data/mission-2026-11-14/research-priority-queue.csv`).

**This is research, not legal advice.** The statute readings in §1 are an analyst's reading of public text. They are not an opinion on any sponsor's obligations.

**Status: public sources only.**
- I logged in nowhere, submitted no forms and contacted no one. TPI's full report sits behind a download form, so I did not obtain it (§5).
- Before every scripted read I checked robots.txt, as user agents `ClaudeBot`, `anthropic-ai` and `*`. Where robots.txt disallowed a path, or could not be read (HTTP 403), I did not fetch it. The hosts I skipped were:
  - gspf.goldman.com, sco.ca.gov, bogleheads.org, riabiz.com, financial-planning.com, fa-mag.com, thewealthadvisor.com and wealthmanagement.com articles, and app.termageddon.com (all disallowed);
  - cct.org, raymondjamescharitable.org, leginfo.legislature.ca.gov, nysenate.gov and mass.gov (robots.txt unreadable).
- dafgiving360.org, schwabcharitable.org and charitable.schwab.acsitefactory.com return 403 to every request, including robots.txt. web.archive.org resets the connection through the proxy.
- Two statute texts come from public.law mirrors because the official sites' robots.txt could not be read. Each mirror page names its official source and update date. These rows are labelled "mirror" in the CSV.

**Recency rule:** current-state claims rest on 2021+ evidence or on statutes in force today, which are current law whatever their enactment date. One figure the repo treats as 2026 data turns out to be 2018 data (§5). It is flagged, not counted as current.

**Read first and built on:** the following files, with their governing corrections:
- `queue-batch33-voids-exports-rails.md`, including the wave-18 corrections. The PPGF rule is treated as standing since 2022.
- `queue-sponsor-terms-data-clauses.md`, including the wave-9 corrections. The Vanguard aggregator reading stays [I].
- `analyst-and-education-landscape.md`, including the wave-4 correction W4-12. The TPI 51% figure is "philanthropically active HNW individuals, not screened for having an adviser".
- `data/mission-2026-11-14/uncashed-grant-rules-2026.csv`.

**Evidence labels:**
- **[F]:** first-party text. This covers statutes, a sponsor's or vendor's own document, and a study's own report.
- **[V]:** a vendor's statement about its own product.
- **[M]:** trade press.
- **[R]:** a search-index summary of a page I could not read.
- **[I]:** my inference.

**Quote check:** quotes are verbatim and 40 words or fewer. A script compared every CSV quote, and the quotes in this file, against the fetched text after normalising whitespace and curly quotes. Two-column PDFs (the DAFRC methods section and the NY OSC sheet) were checked against a column-wise reconstruction.

**Outputs:**
- [`data/mission-2026-11-14/state-escheat-daf-grants-2026.csv`](../../data/mission-2026-11-14/state-escheat-daf-grants-2026.csv): 10 rows. These cover 2 model acts, the UCC, 5 states (1 of them [R] only) and 1 enforcement-history search row.
- [`data/mission-2026-11-14/sponsor-terms-census-top20-2026.csv`](../../data/mission-2026-11-14/sponsor-terms-census-top20-2026.csv): 20 rows, one per top-20 sponsor by FY2024 DAF assets. Ten rows are new reads and ten are carried from the 2026-11-14 pass.
- [`data/mission-2026-11-14/queue-proposals-batch34c.csv`](../../data/mission-2026-11-14/queue-proposals-batch34c.csv): P-B34C-01 to P-B34C-03.

---

## 0. Answers

| Item | Answer | Confidence |
|---|---|---|
| **P-PAY-04** | **Unclaimed-property law can reach a DAF sponsor's checks, but a voided gift check has two strong defences, and no enforcement history was found.**<br>- **Scope:** every statute read covers nonprofit holders. RUUPA and California say "whether or not for profit"; Delaware says "for profit or nonprofit corporation"; NY's Comptroller covers "non-profit".<br>- **Two defences:**<br>  - **No consideration:** a grant check is "issued without consideration". RUUPA §1005(c)(6), Delaware §1175(b)(6) and Washington RCW 63.30.610(3)(f) list that as a rebuttal, and UCC §3-303(b) gives the drawer the same defence against the payee.<br>  - **Timely void:** RUUPA §1005(c)(8) and Washington (h) also accept a check "voided … for a valid business reason" in a contemporaneous record. RUUPA brackets the window as "not later than 90 days", the same period as Fidelity's, GiveClear's and BlueGive's published void rules [I on the match].<br>- **Gaps by state:** Delaware has the consideration defence but no void defence. California's §1520 catch-all (3 years) and Massachusetts c.200A §5 (3 years) reach any intangible "held or owing" in the course of business, and no such defence appears in the sections read. New York's §1315(1-a) covers only outstanding checks "in payment for goods or for services", so a grant check may fall outside it [I].<br>- **Enforcement:** no audit, case, settlement or regulator statement on DAF grant checks was found. | Statute text: high. Application to DAF voids: medium [I]. Enforcement absence: medium |
| **P-B33B-02** | **Still blocked; no 2026 text obtained.**<br>- dafgiving360.org and both mirror hosts (schwabcharitable.org, charitable.schwab.acsitefactory.com) return 403. Wayback is unreachable.<br>- No 2026 PDF is indexed on Squarespace's static host. Search indexes show the Program Policies resource page dated 2026-02-17 and 2026-08-07, and the queue cites 2026-10-22 [R].<br>- The only snippet surfaced is the irrevocable-gift clause, which is not new [R]. The `void_return_policy` cell for DAFgiving360 stays "not stated (2024 text)". | High (on the block) |
| **P-TRM-05** | **The census now covers 18 of the top 20; Dechomai and Raymond James are unreadable.** New findings:<br>- **GKCCF and Greater Horizons** (#16, #17; identical Terms of Use, effective May 2024) are the only top-20 texts that ban an **"aggregator"** by name. They also bar using an Account "for the purpose of providing services to any third party". Unlike most sponsors, they expressly let the user "download and retain information from your Account for your personal records" [F].<br>- **GS DAF** (#5): the Program Circular (third-party copy; cites 2024-09-30 data) lets donors appoint their PWM team "(or another third party)" as agent for advisory privileges and account information [F]. This is a sanctioned delegation route.<br>- **JCF** (#15, Policy Guide Aug 2024): Authorized Parties (relatives, employees, professional advisors) get online access to fund data [F].<br>- **Other new reads:** BofA (#11), CCT (#12) and CJP (#19) have no access clauses; CJP's terms page is a placeholder. ImpactAssets (#13) and FFTC (#14) have only generic website clauses.<br>- **Tally:** 6 of 20 now have explicit contractual limits on automated or third-party access: NCF, Vanguard, NPT, SVCF, GKCCF and Greater Horizons. | High for the texts read |
| **P-VCM-04** | **CIAP terms do not force a Giving Account out when an RIA leaves Fidelity custody; the cost of staying is small.**<br>- **Custody options:** Fidelity Charitable's CIAP Investment Policies and Guidelines (June 2026) allow CIAP assets at National Financial Services *or* an approved "Other Custodian".<br>- **Fee difference:** Other-Custodian assets pay 70 bps instead of 60 bps on the first $500,000, with the same rates above that tier. That is at most about $500 a year per account [F; arithmetic I].<br>- **The custody minimum:** Fidelity's $100m minimum (notices sent October 2026; comply or leave by 2027-06-30) is measured on assets at Fidelity, not total AUM [M].<br>- **Reading:** a custody-driven mirror image of the FY2025 DAFgiving360-to-Fidelity spike would therefore have to come from adviser preference for platform integration (DAFgiving360 on Schwab; Altruist's Endaoment-sponsored DAFs, with Altruist being acquired by Vanguard), not from CIAP eligibility [I].<br>- **Testability:** Fidelity Charitable's FYE 6/2026 Schedule I is not yet public, and FYE 6/2027 covers the wind-down [I]. | Terms: high. Channel effect: low (untested) |
| **P-ANL-02** | **DAFRC's primary report (PDF, created 2026-04-23) confirms 35% / 21% / 10% and 4%, and the reasons 83/69/69/63%.**<br>- **Correction:** the **"61% of clients initiate vs 6% adviser" figure is not a DAFRC 2026 survey result.** The report cites it, with footnotes 10–16, to the **2018 U.S. Trust/TPI study**. The repo's "DAFRC 2026" attribution (via InvestmentNews) is wrong, and the figure is 2018 data. DAFRC's own 2026 "61%" figures are different: frequent recommendation among $10m+ advisers, and among advisers who personally use a DAF.<br>- **Sample:** 669 advisers recruited by email and partner social-media promotion; results are "directly tabulated" with no weighting described. The research was funded by DAFgiving360.<br>- **TPI 2026:** the release confirms 90%, 96% (obligation), 78%, 51%, 73%, 85% and tax 21% vs 40%. The full report and its methodology are form-gated and were not obtained. | High (DAFRC). Medium (TPI, release only) |

---

## 1. P-PAY-04: do unclaimed-property laws reach voided or uncashed DAF grant checks?

### 1.1 What the statutes say (detail in `state-escheat-daf-grants-2026.csv`)

| Text | Covers nonprofit holders? | Covers checks? | Dormancy | "Without consideration" defence | Void defence | Source |
|---|---|---|---|---|---|---|
| **RUUPA (2016)** | Yes: "or other business entity, whether or not for profit" (§102(4)) | Yes (§102(24)(B)(i)) | 3 years for "a debt of a business association" (§201(4)) | §1005(c)(6) | §1005(c)(8): "voided [not later than 90 days] [within a reasonable time] after issuance for a valid business reason set forth in a contemporaneous record" | [ULC text, Maine legislature copy](https://legislature.maine.gov/doc/1519) [F] |
| **UUPA (1995)** | not read first-hand | — | RUUPA comment: 1995 bases "remain unchanged" | — | — | same [F/R] |
| **Delaware**, 12 Del. C. ch. 11 | Yes: "a for profit or nonprofit corporation" (§1130(3)) | Yes (§1130(21)b.1) | 5 years, catch-all (§1133(17)) | §1175(b)(6) | **Not listed** | [delcode](https://delcode.delaware.gov/title12/c011/sc02/index.html) [F] |
| **California**, CCP | Yes: "whether or not for profit" (§1501(c)) | Yes: anything "held or owing in the ordinary course of the holder's business" | 3 years (§1520(a)) | not found in §§1501, 1513, 1520 | not found | [§1520 via california.public.law](https://california.public.law/codes/code_of_civil_procedure_section_1520) (mirror of leginfo) [F] |
| **New York**, APL | Yes (OSC sheet covers "non-profit") | Only "outstanding checks … in payment for goods or for services" (§1315(1-a)) | 3 years | not stated | not stated | [§1315 via newyork.public.law](https://newyork.public.law/laws/n.y._abandoned_property_law_section_1315); [OSC reference sheet (2026-09-23)](https://www.osc.ny.gov/files/unclaimed-funds/reporters/pdf/general-corporations.pdf) [F] |
| **Massachusetts**, c.200A | Yes by text ("Person" includes any corporation, trust or association) | Yes ("checks, drafts", §1) | 3 years (§5) | not stated | not stated | [§5](https://malegislature.gov/Laws/GeneralLaws/PartII/TitleII/Chapter200A/Section5); [§1](https://malegislature.gov/Laws/GeneralLaws/PartII/TitleII/Chapter200A/Section1) [F] |
| **Washington**, RCW 63.30.610 (RUUPA, eff. 2023) | not read | — | — | (3)(f) | (3)(h) "within a reasonable time" | [RCW PDF](https://lawfilesext.leg.wa.gov/Law/RCWPDF/RCW%20%2063%20%20TITLE/RCW%20%2063%20.%2030%20%20CHAPTER/RCW%20%2063%20.%2030%20.610.pdf) [F] |
| **Illinois**, 765 ILCS 1026/15-1005 | — | — | — | reported | not confirmed | [R] only; ilga.gov failed TLS through the proxy |
| **UCC §3-303(b)** | n/a | n/a | n/a | "The drawer or maker of an instrument has a defense if the instrument is issued without consideration." | n/a | [LII](https://www.law.cornell.edu/ucc/3/3-303) [F] |

**Which state's law applies.**
- RUUPA §302 lets a state take custody when "the last-known address of the apparent owner in the records of the holder is in this state" [F].
- §304 lets the holder's domicile state take custody where the owner's state "does not provide for custodial taking of the property" [F].
- For a DAF grant, the owner is the payee charity. Its address is almost always known, so the charity's state governs first [I].

### 1.2 Reading [I]

1. **Nonprofit status is no shield.** Every text read either says "whether or not for profit" or lists nonprofit corporations. New York's Comptroller says its rules cover non-profits and that the APL "does not provide an exemption for business-to-business transactions".
2. **The decisive question is whether anything is still owed to the charity.**
   - RUUPA and Delaware reach only "a fixed and certain interest in intangible property held, issued, or owed in the course of a holder's business".
   - A DAF grant is a gift. The payee cannot enforce an uncashed gift check against the drawer (UCC §3-303(b)).
   - RUUPA, Delaware and Washington each list "issued without consideration" as a rebuttal of the presumption.
3. **Booked liabilities cut the other way.**
   - Under RUUPA §1005(a), "A record of a putative holder showing an unpaid debt or undischarged obligation is prima facie evidence of the debt or obligation".
   - Sponsors book approved grants as grants payable. NPT's FY25 statements show $300.6m (batch 33B §1.2).
   - So the burden sits with the sponsor, and the defence works only if the void is recorded and the money demonstrably went back to the fund.
4. **Reversion to the fund is the published practice, and it fits the void defence, not an exemption.**
   - Fidelity, GiveClear and BlueGive void at 90 days and return funds to the account (`uncashed-grant-rules-2026.csv`). That matches RUUPA's bracketed "not later than 90 days" void defence.
   - Chariot DPN regrants under "exclusive legal control" (batch 29). This is also a documented, recorded reason.
   - Vanguard (discretionary) and NPT, DAFgiving360 and the bank programs (silent) publish no void rule. In Delaware, where the void defence is absent, they would rely on the consideration defence alone.
5. **The exposed edges [I]:**
   - **California and Massachusetts:** broad catch-alls, and no defence list in the sections read.
   - **Long-outstanding checks never voided:** a check outstanding past three to five years with no void record keeps the prima facie presumption alive.
   - **Charity-requested reissues:** under RUUPA §1005(c)(2), a reissued check is a replacement, so the original drops out only if replaced.
6. **No enforcement history found** (CSV row E10).
   - Searches, the batch-28 scan of 990 Schedule O/D text, and sponsor documents show no audit, settlement or regulator statement about DAF grant checks.
   - Pennsylvania's Treasury tells nonprofits to search for property owed to them ([PA tips, 2024-01-10](https://www.patreasury.gov/pdf/unclaimed-property/BUP-Tips-For-Nonprofits.pdf)) [F]. That shows charities do appear as *owners* in state databases. Whether any came from DAF sponsors is untested (P-B34C-01).

**Change to `uncashed-grant-rules-2026.csv` / panel field `escheat_treatment` (proposed, not applied):** keep "not stated" for every sponsor. Add the note: "Statutes cover nonprofit holders; voids within 90 days with a contemporaneous record, and gift (no-consideration) checks, are statutory rebuttals in RUUPA states and (consideration only) Delaware; see state-escheat-daf-grants-2026.csv."

---

## 2. P-B33B-02: DAFgiving360 2026 Program Policies

| Route tried | Result |
|---|---|
| `www.dafgiving360.org/resource/dafgiving360-program-policies`, `/features/program-policies` (curl and WebFetch) | HTTP 403 (Akamai), including robots.txt |
| `schwabcharitable.org` and `charitable.schwab.acsitefactory.com` (legacy and platform hosts) | 403 |
| Squarespace static host (search) | Only the 2024 PDF (modified 2024-12-12) is indexed |
| Wayback (`archive.org/wayback/available` lists a 2026-08-25 capture) | web.archive.org resets the connection through the proxy |
| Bogleheads threads on DAFgiving360 reissues | robots.txt disallows ClaudeBot; not read |

**What the index says [R]:**
- The Program Policies page is dated 2026-02-17 in one result and 2026-08-07 in another.
- Snippets show only the irrevocable-gift and exclusive-legal-control language, which is already in the 2024 text.

**Effect:** none on repo scores. The uncashed-grant, void, transfer and data-term cells for DAFgiving360 remain those from the 2024 PDF: the 30-day decline before payment, grant history and award letters in the Client Center, and adviser view-only access.

---

## 3. P-TRM-05: top-20 terms census (detail in `sponsor-terms-census-top20-2026.csv`)

**Column key:**
- **Y:** explicit clause.
- **G:** generic website clause.
- **P:** the clause permits the activity.
- **N:** document read, no clause.
- **—:** not read.

| # | Sponsor | Document (date) | Automated | Credential sharing | Third-party / aggregator | Export / download | Sanctioned delegation |
|---|---|---|---|---|---|---|---|
| 1–4, 6–10 | Fidelity, NPT, DAFgiving360, Vanguard, SVCF, AEF, MS GIFT, RCF, NCF | carried from 2026-11-14 pass ([terms note §1](queue-sponsor-terms-data-clauses.md)) | — | — | — | — | Fidelity: Authorized Interested Parties ([CIAP guidelines, June 2026](https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf)) |
| 5 | GS DAF | Program Circular, reproduced in the [FireAid investigative report](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf), App. B (cites 2024-09-30 data) | N | N | **P**: agent may be the PWM team "(or another third party)" | N (donor web shows transaction histories) | Agent for advisory privileges and account information |
| 11 | BofA CGF | [Program Guidelines 2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf); [DFX guide (2026-02-23)](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf) | N | N | N | Y: "You can export to Excel to sort" | Authorized Advisor form; log-in via MyMerrill / BofA Online |
| 12 | CCT | [Portal FAQ (2025-12-02)](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf); [user guide (2024-02)](https://donorportal.cct.org/ma/docs/cct/DonorPortalUserGuide.pdf) | N | N | N | Y: CSV | Fund advisors via staff |
| 13 | ImpactAssets | [Privacy Policy and Terms of Use (mod. 2025-11-07)](https://impactassets.org/privacy-policy) | N | G: users responsible for "the confidentiality of their account credentials" | N | N | — |
| 14 | FFTC | [Website Terms of Use](https://fftc.org/website_terms_of_use) (undated) | G: "Use any robot, spider, or other automatic device…" barred | N | N | G | — |
| 15 | JCF | [Policy Guide (Aug 2024)](https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf) | N | N | P (human): Authorized Parties | grant history online; forms download | Appointment of Authorized Party |
| 16 | GKCCF | [Terms of Use (eff. May 2024)](https://www.growyourgiving.org/terms-of-use/) | **Y**, names "aggregator" | Y | **Y**: no use of an Account "for the purpose of providing services to any third party" | **P**: "download and retain information from your Account for your personal records" | "Authorized Use" covers financial advisors managing CF funds |
| 17 | Greater Horizons | [Terms of Use (eff. May 2024)](https://www.greaterhorizons.org/terms-of-use/) | Y (same text) | Y | Y | P | same |
| 18 | Dechomai | [Policies and Procedures](https://dechomai.org/policies-and-procedures/) | — (terms load from a robots-disallowed host) | — | — | — | — |
| 19 | CJP | [Terms page (2025-07-10)](https://www.cjp.org/terms-of-use); [DAF Policies (PDF 2026-04-29)](https://www.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf?hsLang=en) | N | N (issued credentials plus MFA) | N | N (transaction history viewable) | — |
| 20 | Raymond James Charitable | not read (robots.txt unreadable) | — | — | — | — | — |

**GKCCF clause (verbatim):** users may not "use any spider, scraper, robot, aggregator, site search/retrieval application or other automated similar means or device to use or access the Sites … unless it is for an Authorized Use" [F].

**CJP:** its public terms page says only that "CJP is developing comprehensive terms of use that will cover website usage guidelines, intellectual property rights, donation terms, user responsibilities, and other important policies" [F].

**Reading [I]:**
1. **Contractual limits on automated or third-party access now reach 6 of the top 20** (NCF, Vanguard, NPT, SVCF, GKCCF and Greater Horizons). Together they hold about $84bn of FY2024 DAF assets on the repo's figures (NCF 5.46, Vanguard 21.95, NPT 42.12, SVCF 9.58, GKCCF 2.57, Greater Horizons 2.53). Three more (RCF, FFTC, ImpactAssets) have only generic website clauses.
2. **Delegation routes exist where automation is barred.** GS DAF (agent "or another third party"), JCF (Authorized Parties), Vanguard (Authorized Person aggregators) and Fidelity (Authorized Interested Parties) all document a human or firm delegation path. Whether a software service can be appointed through these routes is the open question (P-B34C-03).
3. **GKCCF and Greater Horizons combine the strictest anti-aggregator wording with the most explicit personal-download right.** Under these terms, portability by manual export is allowed, but third-party pull is not.

**Change to the agentic-control gap matrix (proposed, not applied):** set the flag "sponsor terms prohibit agent or third-party credential use" as follows:
- yes: GKCCF and Greater Horizons;
- generic only: FFTC and ImpactAssets;
- no clause found: BofA, CCT, JCF and CJP;
- delegation permitted: GS DAF;
- unknown: Dechomai and Raymond James.

---

## 4. P-VCM-04: Fidelity's $100m RIA custody minimum and Fidelity Charitable's adviser channel

### 4.1 The custody minimum [M]
- **AdvisorHub (2026-10-01).** A Fidelity spokesperson confirmed that RIAs must hold $100m on its custody platform by 2027-06-30 or "discontinue their custodial relationship with Fidelity". Fidelity is "now extending that criteria to existing custody clients for consistency", and "The threshold is based on assets held at Fidelity and not a firm's total AUM." The same piece notes that "Vanguard agreed in August to acquire Altruist" ([AdvisorHub](https://www.advisorhub.com/fidelity-to-drop-rias-below-100m-custody-minimum/)).
- **InvestmentNews (2026-10-26).** Notices sent the prior week give firms "until June 30, 2027, to clear that threshold or start moving those assets to another custodian" ([InvestmentNews](https://www.investmentnews.com/practice-management/fidelity-minimum/268517); also [2026-10-05](https://www.investmentnews.com/goria/custodian/fidelitys-100m-ria-custody-minimum-lands-amid-long-short-sma-curbs/268473)).
- **Counts of affected firms.** The queue's figures (about 986 firms, $37.2bn) came from FINTRX. The FINTRX page fetched here rendered without that text, so these figures stay [R]. The queue's InvestmentNews 268505 URL now returns 404.
- **No mention of charitable accounts.** None of the reports read mentions Fidelity Charitable, DAFs or charitable accounts.

### 4.2 CIAP terms [F]
- **Custody.** The [CIAP Investment Policies and Guidelines](https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf) (last updated June 2026) say: "CIAP Assets can be maintained in brokerage accounts maintained by either National Financial Services LLC or custodians approved by Fidelity Charitable ("Other Custodian")".
- **Fees.** Other-Custodian assets "are subject to an administrative fee as set forth in the fee schedules below, effective July 1, 2020". The tiered rate is "First $500,000 70 bps", against 60 bps for NFS-custodied CIAP assets. All higher tiers and the flat schedule are identical.
- **Changing advisers.** An account holder or Fidelity Charitable may terminate a CIAP adviser at any time. Then "Generally, the CIAP Advisor will be required to liquidate the CIAP Assets so that they may be allocated to the Fidelity Charitable investment pools."
- **Overview flyer.** The [CIAP overview](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf) (PDF 2025-04-17) is headed "For firms that clear or custody with Fidelity Investments" and states a $100,000 program minimum. Its worked example says "$1M x 50 bps", while the guidelines say 45 bps; both give $1,125 a quarter, so the flyer's 50 bps is a typo [I].

### 4.3 Reading [I]
1. **The minimum does not end an RIA's CIAP role.** An RIA that moves custody from Fidelity to Schwab, Altruist or another custodian can keep managing a client's Giving Account in one of two ways:
   - at an approved Other Custodian, at an extra 10 bps on the first $500k (at most $500 a year per account);
   - or by leaving the assets in Fidelity Charitable pools.
2. **A mirror image of the FY2025 spike needs a different driver.** Flows from Fidelity Charitable to DAFgiving360, or to Altruist's Endaoment-sponsored DAF (repo: launched 41 days after the Vanguard–Altruist signing), would have to come from preference for integrated custody and DAF reporting, not from CIAP rules. Whether the Other-Custodian approval list includes the RIA's new custodian is not public.
3. **Test window.** The FYE 6/2026 Schedule I (filed by about May 2027 with extension) predates the deadline. FYE 6/2027 (filed about May 2028) covers the wind-down. Until then, P-VCM-04 stays a hypothesis.

---

## 5. P-ANL-02: primary DAFRC 2026 adviser report and TPI 2026

### 5.1 DAFRC, *Financial Planning in the Age of Donor Advised Funds* (2026)
**Sources:**
- [Full report](https://www.dafresearchcollaborative.org/s/DAF_FinancialAdvisorReport_Final_Web.pdf) (PDF created 2026-04-23, modified 2026-05-07; 45 pp.).
- [Executive summary](https://www.dafresearchcollaborative.org/s/260423_DAF_FinancialAdvisor-ExecSum_Print-1.pdf).
- [Press release (2026-05-11)](https://www.dafresearchcollaborative.org/s/Press-Release_Financial-Planning-in-the-Age-of-Donor-Advised-Funds.pdf).
- All three are linked from [dafresearchcollaborative.org/financial-advisors](https://www.dafresearchcollaborative.org/financial-advisors) [F].

| Repo figure | Primary report | Status |
|---|---|---|
| 35% recommend DAFs most of the time or always | Figure 3.4: 35% / 21% / 44% | **Confirmed** |
| 21% about half the time | Figure 3.4 | **Confirmed** (do not confuse with the separate "21%" of sub-$1m-client advisers recommending DAFs most of the time) |
| 10% never | "10% of financial advisors reporting that they "never" recommend a DAF" | **Confirmed** ("never" is a sub-category of "never or sometimes", 44%) |
| 4% private foundations most of the time or always | Figure 3.4 | **Confirmed** |
| Reasons: tax 83%, flexible timing 69%, convenience 69%, estate planning 63% | Figure on reasons (very or extremely important) | **Confirmed** |
| 669 advisers + 6 focus groups | Methods: 669 respondents. The project page and exec summary say six focus groups; one trade outlet said five | **Confirmed (six)** |
| **61% of clients initiate vs 6% adviser ("DAFRC 2026")** | The report says "when asked who initiates the philanthropic conversation, 61% of clients report that they initiate the conversation, compared to reporting that their advisor initiates the conversation only 6% of the time". Footnotes 10–16 cite the "2018 US Trust Study of the Philanthropic Conversation. Executive Summary." | **Misattributed: 2018 TPI/U.S. Trust data, not a 2026 DAFRC result.** Under the recency rule it is historical context, not current evidence |
| (new) | "Advisors who personally use a DAF are more than twice as likely to frequently recommend one (61%) than financial advisors who don't personally use a DAF (26%)." Advisers serving $10m+ clients: 61% | New 2026 figures. These are the "61%" that trade coverage blends together |

**Sample frame and weighting:**
- The report says: "The survey was sent to financial advisors via email and was promoted on social media by several institutional partners". It adds: "The results presented here are statistics directly tabulated from the survey data." Key findings were also checked by regression.
- No weighting or population frame is described. It is a convenience sample: 50% CFP, and 32% personally use DAFs [F].
- The release states: "The research for this report was completed with funding from DAFgiving360." Partners named are DAFgiving360, AEF, The American College, Fidelity Charitable and the Investments & Wealth Institute.

### 5.2 TPI, *2026 Study of the Philanthropic Conversation*
- **Release confirms these figures** ([release, 2026-04-16](https://tpi.org/?p=3256)) [F]:
  - 90% of advisers make it their practice to discuss philanthropy (80% in 2018);
  - discussing philanthropy "is also an obligation (96%, up from 62% in 2018)";
  - 78% of HNW clients use a structured vehicle (43% in 2018); DAF 51%;
  - 73% of advisers have taken philanthropy education; 85% plan to learn more;
  - "the desire to reduce taxes was also significantly less important to HNW clients (21%) than advisors believe (40%)";
  - advisers' "not enough money for self" 32%.
- **Not confirmed:** the client-side 9%, the sample sizes (300 / 103) and the fieldwork dates. The [report page](https://tpi.org/resource/2026advisorstudy/) says "Complete the form below to download the full report." Under mission rules I did not submit the form (P-B34C-02).

### 5.3 Corrections proposed for `analyst-and-education-landscape.md` (not applied; for the validator)
1. **§4.1, "Who starts the philanthropy conversation" row.** Replace the source cell "DAFRC 2026 via InvestmentNews" with "2018 U.S. Trust/TPI Study, as cited in DAFRC 2026 (footnotes 10–16)". Add the note: "pre-2021 data; not a 2026 survey result".
2. **§5.2 T8 and §6 item 1 ("client-initiated conversations: 61% versus 6%").** Re-label as 2018 data. Do not use it as 2026 evidence against the "advisers drive growth" framing.
3. **§4.1, DAFRC rows.** Change the access label from "secondary" to "primary (PDF read 2026-11-15)". Add "convenience sample; unweighted; funded by DAFgiving360".
4. **§4.1, TPI row.** Mark "300 advisers and 103 HNW clients, Dec 2025–Jan 2026" as [M]: it rests on InvestmentNews, and the release and form-gated report were not read.

---

## 6. Other repo changes implied (proposed, not applied)
1. **`research-priority-queue.csv`, P-VCM-04 evidence pointer.** The InvestmentNews 268505 URL returns 404. Replace it with AdvisorHub 2026-10-01 and InvestmentNews 268517.
2. **`queue-sponsor-terms-data-clauses.md` §1, rows 11–20.** Superseded by `sponsor-terms-census-top20-2026.csv`.
3. **`donor-data-export-top10-2026.csv` (CF rows, if extended to top 20).** GKCCF and Greater Horizons terms grant a personal download right (May 2024).

---

## 7. Source register

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| B01 | Revised Uniform Unclaimed Property Act (ULC), Maine legislature copy | model statute [F] | 2016 | https://legislature.maine.gov/doc/1519 |
| B02 | Delaware Code Title 12 ch. 11 subch. II | statute [F] | current | https://delcode.delaware.gov/title12/c011/sc02/index.html |
| B03 | Cal. CCP §1501 (mirror of leginfo) | statute [F] | updated 2026-01-01 | https://california.public.law/codes/code_of_civil_procedure_section_1501 |
| B04 | Cal. CCP §1520 (mirror) | statute [F] | updated 2026-01-01 | https://california.public.law/codes/code_of_civil_procedure_section_1520 |
| B05 | Cal. CCP §1513 (mirror) | statute [F] | updated 2017-01-01 | https://california.public.law/codes/code_of_civil_procedure_section_1513 |
| B06 | N.Y. APL §1315 (mirror of nysenate.gov) | statute [F] | amended 2014-09-22 | https://newyork.public.law/laws/n.y._abandoned_property_law_section_1315 |
| B07 | NY OSC reference sheet, all business entities incl. non-profit | regulator guidance [F] | PDF 2026-09-23 | https://www.osc.ny.gov/files/unclaimed-funds/reporters/pdf/general-corporations.pdf |
| B08 | NY OSC Handbook for Reporters | regulator guidance [F] | PDF 2026-09-23 | https://www.osc.ny.gov/files/unclaimed-funds/reporters/pdf/handbook.pdf |
| B09 | M.G.L. c.200A §1 | statute [F] | current | https://malegislature.gov/Laws/GeneralLaws/PartII/TitleII/Chapter200A/Section1 |
| B10 | M.G.L. c.200A §5 | statute [F] | current | https://malegislature.gov/Laws/GeneralLaws/PartII/TitleII/Chapter200A/Section5 |
| B11 | RCW 63.30.610 | statute [F] | 2022 c 225, eff. 2023-01-01 | https://lawfilesext.leg.wa.gov/Law/RCWPDF/RCW%20%2063%20%20TITLE/RCW%20%2063%20.%2030%20%20CHAPTER/RCW%20%2063%20.%2030%20.610.pdf |
| B12 | 765 ILCS 1026/15-1005 | statute [R] | — | https://ilga.gov/legislation/ilcs/documents/076510260K15-1005.htm |
| B13 | UCC §3-303 (LII) | model statute [F] | current | https://www.law.cornell.edu/ucc/3/3-303 |
| B14 | PA Treasury, Unclaimed Property for Nonprofits | regulator [F] | 2024-01-10 | https://www.patreasury.gov/pdf/unclaimed-property/BUP-Tips-For-Nonprofits.pdf |
| B15 | SC Treasurer reporting FAQ | regulator [F] | 2023-09-13 | https://treasurer.sc.gov/media/evvprcct/reporting-unclaimed-property-frequently-asked-questions.pdf |
| B16 | DAFgiving360 Program Policies page (403) | sponsor [R] | 2026-02-17 / 2026-08-07 per index | https://www.dafgiving360.org/resource/dafgiving360-program-policies |
| B17 | GS DAF Program Circular, App. B of FireAid investigative report | sponsor doc via third party [F] | report PDF 2025-09-26 | https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf |
| B18 | BofA CGF Program Guidelines 2024 | sponsor [F] | 2024-09-18 | https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf |
| B19 | BofA CGF DFX donor guide | sponsor [F] | 2026-02-23 | https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf |
| B20 | CCT Donor Portal FAQ | CF [F] | 2025-12-02 | https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf |
| B21 | CCT Donor Portal User Guide | CF [F] | 2024-02-06 | https://donorportal.cct.org/ma/docs/cct/DonorPortalUserGuide.pdf |
| B22 | ImpactAssets Privacy Policy and Terms of Use | sponsor [F] | mod. 2025-11-07 | https://impactassets.org/privacy-policy |
| B23 | FFTC Website Terms of Use | CF [F] | undated, live | https://fftc.org/website_terms_of_use |
| B24 | FFTC Privacy Policy | CF [F] | undated, live | https://fftc.org/node/913 |
| B25 | JCF Policy Guide | sponsor [F] | 2024-08-09 | https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf |
| B26 | GKCCF Terms of Use | CF [F] | eff. May 2024 | https://www.growyourgiving.org/terms-of-use/ |
| B27 | Greater Horizons Terms of Use | CF [F] | eff. May 2024 | https://www.greaterhorizons.org/terms-of-use/ |
| B28 | Dechomai Policies and Procedures | sponsor [F] | undated, live | https://dechomai.org/policies-and-procedures/ |
| B29 | CJP Terms of use | sponsor [F] | 2025-07-10 | https://www.cjp.org/terms-of-use |
| B30 | CJP DAF Policies and Procedures | sponsor [F] | PDF 2026-04-29 | https://www.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf?hsLang=en |
| B31 | Fidelity Charitable CIAP Investment Policies and Guidelines | sponsor [F] | June 2026 | https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf |
| B32 | Fidelity Charitable CIAP overview | sponsor [F] | PDF 2025-04-17 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf |
| B33 | Fidelity Charitable CIAP Investment Advisor Agreement | sponsor [F] | PDF 2025-01-28 | https://www.fidelitycharitable.org/docs/CIAP-Investment-Advisor-Agreement.pdf |
| B34 | AdvisorHub, Fidelity to drop RIAs below $100m | trade press [M] | 2026-10-01 | https://www.advisorhub.com/fidelity-to-drop-rias-below-100m-custody-minimum/ |
| B35 | InvestmentNews, custody minimum forces small RIAs to pick a path | trade press [M] | 2026-10-26 | https://www.investmentnews.com/practice-management/fidelity-minimum/268517 |
| B36 | InvestmentNews, custody minimum amid long-short SMA curbs | trade press [M] | 2026-10-05 | https://www.investmentnews.com/goria/custodian/fidelitys-100m-ria-custody-minimum-lands-amid-long-short-sma-curbs/268473 |
| B37 | DAFRC, Financial Planning in the Age of DAFs (full report) | study [F] | PDF 2026-04-23 / 2026-05-07 | https://www.dafresearchcollaborative.org/s/DAF_FinancialAdvisorReport_Final_Web.pdf |
| B38 | DAFRC executive summary | study [F] | PDF 2026-04-29 | https://www.dafresearchcollaborative.org/s/260423_DAF_FinancialAdvisor-ExecSum_Print-1.pdf |
| B39 | DAFRC press release | study [F] | 2026-05-11 | https://www.dafresearchcollaborative.org/s/Press-Release_Financial-Planning-in-the-Age-of-Donor-Advised-Funds.pdf |
| B40 | TPI 2026 study release | study [F] | 2026-04-16 | https://tpi.org/?p=3256 |
| B41 | TPI 2026 report page (form-gated) | study [F] | mod. 2026-10-28 | https://tpi.org/resource/2026advisorstudy/ |

---

## 8. Data dictionary

### `state-escheat-daf-grants-2026.csv`

| Column | Meaning |
|---|---|
| `row_id` | E01–E10 |
| `jurisdiction` | State, "Model act", or "All" (for the search row) |
| `instrument`, `citation` | Statute or model act and the sections relied on |
| `text_status` | enacted / model act / superseded model act / search result |
| `source_url`, `source_type` | Where the text was read. `source_type` says whether it is the official site, a mirror (and why), or the search index |
| `source_date` | Date of the text or its last amendment, as shown by the source |
| `nonprofit_holders_covered` | Whether the holder definition reaches nonprofit corporations or trusts, with the textual hook |
| `checks_are_property` | Whether an issuer's outstanding check is reportable property, and any limit (e.g. NY goods or services) |
| `dormancy_for_issuer_check` | Period after which the check is presumed abandoned |
| `without_consideration_defense` | Statutory rebuttal for checks issued without consideration (yes and section / not stated / not found / not read) |
| `void_defense` | Statutory rebuttal for checks voided for a valid business reason |
| `b2b_or_other_exemption` | Business-to-business or other exemptions relevant to grants |
| `reading_for_voided_daf_grant` | Analyst reading [I] for a DAF sponsor's voided or uncashed grant check; not legal advice |
| `key_quote` | Verbatim, ≤40 words, script-checked; "…" joins segments. Blank for [R] and search rows |
| `evidence_label`, `notes`, `retrieved` | As named |

### `sponsor-terms-census-top20-2026.csv`

| Column | Meaning |
|---|---|
| `rank_fy2024`, `sponsor`, `ein`, `fy2024_daf_assets_usd_bn` | Rank and year-end DAF assets from `dafrc-sponsor-schedule-d-fy2019-2024.csv` (FY2024) |
| `documents_read`, `document_date`, `source_url` | Documents relied on and their own dates |
| `read_status` | read / read (repo) / partial / not read, with the reason (robots, 403, form) |
| `automated_access`, `credential_sharing`, `third_party_or_aggregator`, `export_or_download` | Clause codes: Y explicit; G generic website clause; P permits; N read, no clause; "not read". Each code has a short gloss |
| `sanctioned_delegation_path` | Any documented route for a person or firm to act or see data for the donor |
| `key_quote` | Verbatim, ≤40 words, script-checked against the fetched text; blank for carried rows (quotes are in `sponsor-terms-clauses-2026.csv`) |
| `evidence_label`, `retrieved` | Label per header; retrieval date (2026-11-14 for carried rows) |
| `carried_from_repo` | Filled when the row restates the 2026-11-14 pass without a re-read |
| `notes` | Caveats and inferences |

### `queue-proposals-batch34c.csv`

Standard proposal columns per [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md); prefix P-B34C-.

---

## 9. Proposals
- **P-B34C-01:** count DAF sponsors appearing as holders in state unclaimed-property bulk files. Use only files that robots.txt allows; California's SCO file needs a human or another permitted route.
- **P-B34C-02:** obtain TPI 2026's full report and methodology without submitting TPI's form, for example from co-sponsor-hosted copies.
- **P-B34C-03:** map sanctioned delegation routes (GS DAF agent, JCF Authorized Party, Fidelity AIP, Vanguard Authorized Person, GKCCF "Authorized Use") and whether a software service can be appointed.

## Validation corrections (wave 19, 2026-11-15) — governing
Source: [validation-wave19-report.md](validation-wave19-report.md); register `data/mission-2026-11-14/validation-register-wave19.csv`.

1. **§0, P-TRM-05 lead.**
   - **Find:** "**The census now covers 18 of the top 20; Dechomai and Raymond James are unreadable.**"
   - **Replace with:** "**The census now has at least one document read for 18 of the top 20; Dechomai and Raymond James are unreadable.** DAFgiving360 rests on its 2024 text (the 2026 Program Policies are unreadable), and AEF has no terms of use found [V wave 19]."
2. **§5.1, sources (page count).**
   - **Find:** "(PDF created 2026-04-23, modified 2026-05-07; 45 pp.)"
   - **Replace with:** "(PDF created 2026-04-23, modified 2026-05-07; 46 pp.)"
