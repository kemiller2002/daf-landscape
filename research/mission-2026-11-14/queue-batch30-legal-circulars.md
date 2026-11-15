# California platform law for DAF vendors, Candid reliance elements, wealth-captive circulars and Fidelity export (P-B29B-01, P-B29B-03, P-STF-04, P-TRM-03)

**Queue items:** P-B29B-01, P-B29B-03, P-STF-04, P-TRM-03 (batch30 A). The full text is in [`research-priority-queue.csv`](../../data/mission-2026-11-14/research-priority-queue.csv).

**Date:** 2026-11-15.

**Method:**
- Public sources only: statute and regulation texts, AG forms and pages, IRS bulletin, Candid developer docs and sample report, sponsor PDFs, and one third-party-hosted circular.
- No logins, outreach or form submissions. The California AG Registry search is a web form, so it was not queried.
- The MS GIFT circular uses an image-encoded font, so it was read by OCR (`tesseract`) of rendered pages. Quotes from it are transcriptions.

**Recency rule:** current-state claims use evidence dated 2021 or later. Older items appear only as labelled context.

**This is research, not legal advice.** The California analysis applies statutory text to hypothetical vendor designs. The AG has published no guidance on DAF vendors that this agent could find.

**Labels:**
- **[F]:** fact stated in a primary document.
- **[S]:** secondary source.
- **[R]:** search-index snippet only; page not read.
- **[I]:** inference by this agent.
- **[U]:** unknown or not found.

**Builds on, and applies the governing corrections of:**
- [queue-batch29-regulation-litigation-crypto.md](queue-batch29-regulation-litigation-crypto.md), including wave-14 correction 1–4. **Rev. Proc. 2018-32 §8.01 is the governing rule.** It superseded Rev. Proc. 2011-33.
- [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md) §2 (Fidelity) and §5 (Candid).
- [queue-bank-programs-and-eft-providers.md](queue-bank-programs-and-eft-providers.md) §2, §4 and §5, including its wave-6 corrections.
- [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §8 (recency).

**Files written:**
- [`data/mission-2026-11-14/wealth-captive-terms-2026.csv`](../../data/mission-2026-11-14/wealth-captive-terms-2026.csv): 53 rows covering MS GIFT, GS DAF and BofA CGF.
- [`data/mission-2026-11-14/queue-proposals-batch30a.csv`](../../data/mission-2026-11-14/queue-proposals-batch30a.csv): P-B30A-01 to P-B30A-03.

---

## 1. Answers

| Item | Answer | Label |
|---|---|---|
| **P-B29B-01:** is a non-custodial DAF tech vendor a California "charitable fundraising platform" (CFP)? | **On the text, often yes. Custody is not the test, and the sponsor's DAF exclusion does not pass to its vendor.**<br>- **Own-brand grant-recommendation or charity-search app:** this matches §12599.9(a)(1)(A). The app "lists or references by name" charities to receive "grants of recommended donations made by donors who use the platform". Regulation 314(m) calls this Type A.<br>- **White-label DAF portal licensed to a sponsor:** this matches (a)(1)(E). It is SaaS "that allows charitable organizations to solicit or receive donations". Regulation 314(q) names "private-labeled" platforms under a "software as a service license agreement". A DAF sponsor is a charitable organization.<br>- **The DAF exclusion (a)(2)(C) names only "A sponsoring organization of donor-advised funds".**<br>- **The vendor exclusion (a)(2)(B) is narrow.** It covers vendors that "solely" serve *a charitable fundraising platform*. An excluded sponsor is not a CFP, so a vendor to it does not fit the carve-out's wording.<br>- **Narrowest escape:** a pure back-end with no donor-facing listing and no contribution intake.<br>- **Not found:** AG guidance or FAQ on DAF vendors, and registry entries for DAF-adjacent vendors (registry not queried). | F (statute, regs, AG page, PL-1); I (application); U (registry) |
| **P-B29B-03:** does a Candid Charity Check report meet Rev. Proc. 2018-32 §8.01? | **Mostly, but not fully on the face of the public sample PDF.**<br>- **§8.01(1)(a), name, EIN, foundation status and deductibility:** yes.<br>- **§8.01(1)(b), BMF revision date:** a "Most recent IRS BMF" date is printed. There is no express statement that the data come from "the most current update of the EO BMF Extract".<br>- **§8.01(1)(c), date and time:** the PDF shows "Generated April 16, 2025", a date with no time. The JSON API's `report_date` gives date and time in GMT.<br>- **Superseded citation:** both the PDF and the FAQ still cite Rev. Proc. 2011-33.<br>- **§8.01(2), retention:** this depends on the grantor. Candid's 2026-09-14 **Subscriber** License Agreement lets copies made before termination "be retained". The 2026-09-14 **API** licence has no such carve-out (repo). The subscriber agreement lists Charity Check as "(discontinued)".<br>- **No public Order Form** was found. | F (IRB, sample PDF, schema, licence); I (gap reading) |
| **P-STF-04:** current circulars for MS GIFT, GS PF and BofA CGF | **All three now have 2021+ evidence. GS PF moves off U.**<br>- **GS DAF:** a current Program Circular (ETF ratios "as of September 30, 2024") is reproduced as Appendix B of FireAid's Sept 2025 investigative report. Terms: $20,000 minimum; $100 minimum grant; check **or wire**; marginal admin fee from 0.60% down to 0.03%; options from 0.10% plus index ERs to IMAP; no DAF-to-DAF clause; no export.<br>- **MS GIFT (Aug 2024):** $25,000 minimum; $250 minimum grant; administrator fee 0.27% (min $100) + MSSB 0.07% + up to 0.03%; advisory fee up to 1.00%; no outbound or export clause.<br>- **BofA CGF:** guidelines v3.2024 are still current, since the 2025 and 2026 filenames return 404. Flat first-dollar fee from 0.90% down to 0.10%, plus 0.12% for management and fund fees. Transfer to "another donor-advised fund" is named only on termination. The 2025 guide offers an Excel export of contributions.<br>- **Detail:** see the CSV. | F |
| **P-TRM-03:** does Fidelity Charitable offer an export? | **Only PDF documents are documented for donors. A third-party aggregation channel existed in 2023, and its current status is unverified.**<br>- **Current how-to (file metadata 2026-05):** "Click the document name to view and download the PDF".<br>- **FAQs:** describe on-screen history only.<br>- **Program Guidelines (2026-09-11):** give a "view, but not necessarily modify" right.<br>- **License Agreement s.8 ("Last Reviewed January 2021"):** says Fidelity "may provide" export to third-party software.<br>- **2023 evidence:** Morningstar ByAllAccounts notices (July 2023) list "Fidelity Charitable Gift Fund (Investment)" among accounts moving to Fidelity's Akoya open-banking API, primary holder only.<br>- **Possible break:** an Empower help article says these accounts are "no longer able to sync" under the Fidelity option [R]. | F (Fidelity, Morningstar); R (Empower) |

---

## 2. P-B29B-01: California charitable fundraising platform law and DAF vendors

### 2.1 Texts read

| Text | Source | Date |
|---|---|---|
| Gov. Code §12599.9 (full) | [california.public.law](https://california.public.law/codes/government_code_section_12599.9). This mirrors leginfo, which returned 403 to automated fetch | "updated Jan. 1, 2025"; accessed 2026-11-11 |
| 11 CCR §§314–323 | [AG PDF](https://oag.ca.gov/system/files/media/Cal-Code-Regs-titl-11-secs-314-323.pdf) (19 pp) | in force from 2024-06-12 (AG page) |
| AG "Charitable Fundraising Platforms" page | [oag.ca.gov/charities/pl](https://oag.ca.gov/charities/pl) | live 2026-11-15 |
| Form PL-1 and instructions | [PL-1](https://oag.ca.gov/system/files/media/PL-1-Form-and-Instructions.pdf) | "Orig. 01/2024" |
| Initial Statement of Reasons | [ISOR](https://www.oag.ca.gov/system/files/media/pf-initial-statement-of-reasons.pdf) | rulemaking record |

### 2.2 The operative words

**Definition, (a)(1).** A CFP is an entity that "uses the internet to provide an internet website, service, or other platform to persons in this state, and performs, permits, or otherwise enables acts of solicitation to occur" [F]. Two of the listed acts matter here:
- **(A):** "Lists or references by name one or more recipient charitable organizations to receive donations or grants of recommended donations made by donors who use the platform" [F].
- **(E):** "Provides to charitable organizations a customizable internet-based website, software as a service, or other platform that allows charitable organizations to solicit or receive donations on or through the platform" [F]. The customizable platform "does not include the charitable organization's own platform, but may integrate with" it [F].

**Regulations.**
- **Type A (314(m))** covers soliciting "donations or recommended donations ... from donors who are platform users by listing or referencing by name one or more recipient charitable organizations" [F].
- **Type E (314(q))** covers a platform that "can be private-labeled or otherwise customized, that is subject to a software as a service license agreement" [F].
- **"Platform" (314(j))** includes a "mobile device application, computer software application" [F].
- **"Fee" (314(d))** expressly reaches amounts charged by "a vendor that provides services to a charitable fundraising platform" [F].

**Exclusions, (a)(2).**
- **(B), vendors:** a vendor "that solely provides technical or supportive services to a charitable fundraising platform", such as hosting, "internet application development, or digital payment processing". However, if that vendor enables solicitation "on its own platform to persons in this state, it is a charitable fundraising platform for its own platform" [F].
- **(C), DAF sponsors:** the exclusion covers "A sponsoring organization of donor-advised funds, as defined in subdivision (d) of Section 4966". It applies only where the sponsor "does not list or reference by name one or more recipient charitable organizations for solicitation purposes on its platform for persons who do not have advisory privileges" [F].
- **(a)(6)** gives the same carve-out from "platform charity" [F].

**Registration.**
- **The AG page** says a CFP must register "before performing, permitting, or enabling any solicitations". Renewal is on PL-2 by January 15, and the annual report on PL-4 by July 15 [F].
- **The PL-1 fee is $625** [F].
- **The PL-1 uses its own type labels:** soliciting, peer-to-peer, coventuring, "consulting", or "other" [F]. **[I]** "Consulting" appears to correspond to Type E.
- **Filing system:** the platforms filing service was replaced by a new Online Filing Service from late August 2026 [F].

### 2.3 Application to vendor designs [I]

| Vendor design | Fits (a)(1)? | Exclusion available? | Reading |
|---|---|---|---|
| **V1. Own-brand donor app.** Donors link DAFs at any sponsor, search charities and send grant recommendations. Funds go from the sponsor to the charity, and the vendor never holds them | (A): the app lists charities by name to receive "grants of recommended donations made by donors who use the platform" | (C) no: the vendor is not a §4966(d) sponsor. (B) no: it enables solicitation "on its own platform" | **Likely a CFP (Type A).** The DAF-specific wording "grants of recommended donations" points directly at this flow. Custody is irrelevant to the definition |
| **V2. White-label DAF portal licensed to a sponsor** (contributions, grant recommendations, charity search; sponsor-branded) | (E): SaaS "that allows charitable organizations to solicit or receive donations". A DAF sponsor is a charitable organization, and 314(q) names private-label SaaS | (C) covers the sponsor only. (B) covers vendors "to a charitable fundraising platform", and the excluded sponsor is not one. "Own platform" in (E) refers to the charity's own platform, not a licensed one | **Textual Type E exposure.** No guidance found. The obligations are light for a non-custodial vendor (§2.4) |
| **V3. Charity-side DAF button on nonprofit sites** (DAFpay pattern) | (E): a platform provided to charities "to solicit or receive donations on or through the platform" | (B) is arguable only if the button is a pure payment-processing service to a CFP. A nonprofit's own site is excluded under (a)(2)(A), but that does not cover the button vendor | **Likely Type E**, or a vendor to a CFP where the button is embedded in a registered fundraising platform |
| **V4. Pure back-end API to a sponsor** (no donor UI, no listing; sponsor-hosted) | Weak. The vendor does not itself "provide ... to persons in this state" a platform that enables solicitation | (B) by analogy (technical services) | **Lowest exposure.** Wording risk remains, because (B) is framed around service to a CFP |

**Why the sponsor exclusion matters less than the queue assumed.** The (C) condition (no listing of charities for solicitation purposes to non-advisors) fits a donor-only charity search. It is still written for the sponsor. A vendor's app showing the same list to the same advisors is not covered by (C), because the vendor is not "a sponsoring organization" [I].

### 2.4 What registration would cost a non-custodial vendor [F, applied I]

- **Type E disclosure (316(d)(3)).** Disclose to the charitable organization that it "may be deemed ineligible to be sent donated funds". The vendor must also ask the charity to pass this disclosure on to users.
- **Type E remittance (318(c)(1)).** Donations go out "no later than five business days" with at least monthly eligibility checks. A vendor that never receives funds meets this structurally.
- **Contracts.** Vendor contracts to "solicit, receive, control, process, distribute" donations must be "available for inspection by the Attorney General" (§12599.9).
- **Ongoing filings.** The PL-2 renewal and the PL-4 annual report.

### 2.5 Hawaii (HRS 467B)

- **Not re-read at the primary level.** capitol.hawaii.gov returned 403.
- **The batch29 secondary reading stands** [S]: a platform "may be a CFP even if it does not itself ask for the donation" ([FKKS, 2026-07-29](https://advertisinglaw.fkks.com/post/102nf2j/hawaiis-charitable-platform-law-now-in-effect)).

### 2.6 Registry evidence

- **Not obtained.** The registry search ([ca-rcf.evokeplatform.com](https://ca-rcf.evokeplatform.com/app/registrationPortal)) is a form-based app, which this mission's rules exclude.
- **Vendor terms are silent.** None of the public terms read from Chariot ([nonprofit terms](https://givechariot.com/legal-nonprofit)), Endaoment ([terms](https://endaoment.org/terms)) or Chariot donor terms mention California registration [F, absence].
- **Proposed follow-up:** P-B30A-02.

---

## 3. P-B29B-03: Candid Charity Check against Rev. Proc. 2018-32 §8.01

### 3.1 The governing rule

[Rev. Proc. 2018-32 §8.01, IRB 2018-23](https://www.irs.gov/irb/2018-23_IRB) [F]. A grantor may rely on EO BMF data from a third party if:
- **(1)(a)** the report includes "The organization's name, EIN, foundation status under § 509(a)(1), (2), or (3) (including supporting organization type, if applicable), and whether contributions to the organization are deductible";
- **(1)(b)** the report includes "A statement that the information is from the most current update of the EO BMF Extract and the revision date of the EO BMF Extract containing the information";
- **(1)(c)** the report includes "The date and time the information was provided to the grantor or contributor"; and
- **(2)** "The grantor or contributor retains a paper or electronic copy of the report."

### 3.2 Element check

The sample report is Candid's public [Charity Check PDF example](https://docs.candid.org/files/guidestar-charity-check-pdf-api-example-response-13-1837418.pdf): EIN 13-1837418, IronPdf, created 2025-04-16, one page.

| Element | PDF report (public sample) | JSON API ([schema](https://developer.candid.org/reference/charitycheck_v1.md); [examples](https://developer.candid.org/reference/charity-check-example-responses.md), updated 2026-09-07) | Reading |
|---|---|---|---|
| (1)(a) Name and EIN | "Candid", "EIN: 13-1837418" | `bmf_organization_name`, `bmf_ein` | Met [F] |
| (1)(a) Foundation status, including SO type | "Foundation status code: PC" and "Public charity described in section 509(a)(1) or (2)"; "Reason for Non-Private Foundation status" | `foundation_code` (21–24 = SO Types I–III), `foundation_509a_status` | Met [F] |
| (1)(a) Deductibility | "Deductibility status description: A public charity (50% deductibility limitation)" | `organization_types[].deductibility_status_description` | Met [F] |
| (1)(b) Revision date of the BMF extract | "Most recent IRS BMF: March 10, 2025" | `most_recent_bmf`: "Date of the most recent IRS Business Master File" | Date present [F] |
| (1)(b) Statement that the data are from the most current update | Not stated in those words. The PDF says only that Candid "acquires all IRS data directly from the Internal Revenue Service" | Not stated | **Gap on the face of the document** [I]. The label "Most recent" arguably implies it. Candid's FAQ says it checks the IRS "every 20 minutes" (repo) |
| (1)(c) Date and time provided | "Generated April 16, 2025". **No time is printed** | `report_date`: "Date and time the Charity Check API returned the result. Reported in Greenwich Mean Time (GMT)" | **PDF gap on time** [F]. The JSON meets it. **[I]** A sponsor archiving the PDF alone may lack the time element |
| (2) Retention | Candid tells users to "download and save a PDF copy ... which includes a timestamp, to build an audit trail" ([get started](https://developer.candid.org/reference/get-started-with-charity-check.md), 2026-09-07) | — | Grantor-side duty. The licence position is in §3.3 |
| Authority cited | "IRS Revenue Procedure 2011-33 allows grantors to rely on third-party resources" | FAQ cites Rev. Proc. 2011-33 ([FAQ](https://developer.candid.org/reference/faqs-charity-check.md), 2026-09-07) | **Superseded citation** [F]. 2018-32 changed the wording of (1)(b) and (2), adding "paper or electronic" |

**Caveat.** The public sample was generated in April 2025. The 2026 PDF v2 output was not observed (P-B30A-03).

### 3.3 Retention after termination: two Candid licences differ

- **API License Agreement** (last updated 2026-09-14). The licensee must "cease ... all use of the Candid Data" on termination, with no retention carve-out (repo: [queue-sponsor-terms-data-clauses.md §5](queue-sponsor-terms-data-clauses.md)) [F].
- **Subscriber License Agreement** ([page](https://candid.org/terms-of-service/candid-subscriber-license-agreement/), dated 2026-09-14; read through a fetch tool because curl returned 403):
  - **§11.1:** on termination, copies made in accordance with the Agreement "may be retained by Licensee or Authorized Users and may be used only as permitted by the terms of this Agreement" [F].
  - **§2.5:** "Any stored hard copy or digital copy remains the property of Candid" [F].
  - **Coverage:** its service list includes "Charity Check (discontinued)" [F].
- **Reading [I].** Candid's web-subscriber contract has a pre-termination-copy retention right, and its API contract does not. Sponsors that get Charity Check PDFs by API (the current product) fall under the stricter text unless their Order Form adds a carve-out.
- **No public Order Form, Exhibit or procurement copy was found** [U]. Candid's [explore-APIs page](https://candid.org/explore-apis/) lists Charity Check API pricing "starting at" $2,750 [R].

---

## 4. P-STF-04: wealth-captive program circulars (2021+)

Full terms with quotes are in [`wealth-captive-terms-2026.csv`](../../data/mission-2026-11-14/wealth-captive-terms-2026.csv). Summary:

| Term | MS GIFT (circular Aug 2024) | GS DAF (circular, ratios as of 2024-09-30) | BofA CGF (guidelines v3.2024; fee schedule 2024) |
|---|---|---|---|
| Minimum to open | $25,000 (Select UMA / PM); NextGen $5,000 | **$20,000**; additional gifts $5,000 | $25,000; additional gifts $250 |
| Minimum grant | $250 | **$100** | $250 or the balance |
| Admin fee | Administrator 0.27% (min $100) tiering down to 0.11%, flat 0.09% at $50m+; plus MSSB 0.07% (lower above $25m); plus charitable fee of up to 0.03% | Marginal: 0.60% / 0.30% / 0.20% / 0.10% / 0.05% / 0.03% at breaks of $0.5m, $1m, $2.5m, $10m and $25m | **Flat from the first dollar:** 0.90% (to $100k) down to 0.10% ($20–50m); custom above |
| Investment layer | MSSB advisory fee of up to 1.00% (from 2021-07-21), shared with the FA, plus fund and SMA fees. Legacy Pools 0.60–1.24% (closed) | GSAM funds 0.18–0.67% ER; third-party allocation 0.55% + 0.30–0.33%; index 0.10% + 0.02–0.04%; Passive up to 0.50% + 0.05–0.16%; IMAP up to 0.50% + 0.57–1.03% (est.) | 0.12% Private Bank fee + fund fees; estimated totals 0.17–0.29% |
| Investment options | Select UMA (MSSB discretionary), Portfolio Management (FA-run), "Other" with approval. Default after 30 days uninvested: an MSSB ETF model | Four objectives across GSAM funds, third-party index or allocation funds, Passive ETF (ESG available, $50k), and IMAP ($5m, some private investments). Default: FGTXX | Eight objectives: money market, or seven objectives in active (SMA) or passive versions |
| Grant rail | "validated mailing address or banking details" | **"check or wire transfer"**; the 2008–2017 circulars said check | Check only (USPS) |
| Transfer-out | No clause names DAF sponsors. Grantees are public charities, domestic organizations, POFs and foreign organizations | No clause names DAF sponsors. Grantees are 509(a)(1)–(3) except NFI Type III, POFs and governments. A full-balance grant carries a prorated admin fee | "another donor-advised fund" only after CGF ends advisory rights. Otherwise closing grants follow the residual rules |
| Inactivity | 5 years with no activity: may be distributed or moved to the undesignated fund | Under 5% over 5 years: up to 5% swept after 60 days. No grants in 5 years: whole account to the Directors' fund and closed after 90 days | 5 years: General Fund |
| Donor data | Portal view and quarterly statements; no export clause | Donor web view of histories and quarterly statements; no export clause | Documents tab; **"export to Excel"** on the contribution listing (2025 guide) |

**Notes.**
- **GS DAF provenance.**
  - The circular is reproduced in [FireAid's investigative report by Latham & Watkins](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf), Appendix B, pp. 15ff (PDF created 2025-09-26). FireAid used GS DAF for grant administration.
  - The copy is undated. The ETF ratios "in effect as of September 30, 2024" put it at late 2024 or 2025 [I].
  - It is a third-party-hosted copy of a sponsor document. It is admissible as 2021+ evidence, labelled **F (third-party-hosted copy)**.
  - It **supersedes** the repo's 2008, 2012 and 2017 terms ($25,000 minimum, $250 grants in $50 steps, check only) and the 2019 secondary source.
  - The service provider is now "Goldman Sachs Wealth Services, L.P.", not Ayco.
- **MS GIFT.** The file is unchanged at its URL (Last-Modified 2024-08-23). The circular itself tells donors to check the portal for "the most up to date terms".
- **BofA.** No 2025 or 2026 guidelines exist at the expected paths (404). The 9/2025 portal guide is the newest document.
- **Quadrant consequence [I].** GS PF's A3/A4 portability and payment criteria can now be scored from 2021+ evidence instead of U. Under §8 of the methodology, they no longer default to "insufficient evidence". The score itself is for the quadrant agent.

---

## 5. P-TRM-03: Fidelity Charitable export or download

| Source | What it says | Label |
|---|---|---|
| [How-to: view and download statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/how-to-view-and-download-statement-confirmation-and-tax-forms.pdf) (curl 403; read through a fetch tool. XMP metadata 2026-05-15/26; job code 1082789.3.0) | Statements, contribution receipts, grant confirmations and Form 8283: "Click the document name to view and download the PDF". No CSV or transaction export | F |
| [FAQ: find Giving Account history](https://www.fidelitycharitable.org/faqs/all/find-giving-account-history.html) and [Using my Giving Account](https://www.fidelitycharitable.org/faqs/donor/using-my-giving-account.html) (live) | "hover over 'History' in the top navigation menu and select the Giving Account history content you are looking for". No download mentioned | F |
| [Advisor grant support](https://www.fidelitycharitable.org/advisors/support/grants.html) (live) | "Click the 'Print' button to keep a hard copy for your records" | F |
| [Program Guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf) (PDF 2026-09-11) | Right "to view, but not necessarily modify, all Giving Account information, including contribution and grant history" | F |
| [License Agreement](https://www.fidelitycharitable.org/legal/license-agreement-and-copyright.html) s.8 ("Last Reviewed January 2021") | Fidelity "may provide users the opportunity to export or download Giving Account information ... within a third party software product or on-line service" | F. **The review date predates the 2021-11-14 recency cut-off.** It is the live text, but weak evidence of a live channel |
| Morningstar ByAllAccounts client notices ([8/23 migration](https://advisor.morningstar.com/Enterprise/VTC/ClientCommunication-Q3%20Fidelity%20Update-8.23Migration.pdf); [9/6 migration](https://advisor.morningstar.com/Enterprise/VTC/OB_FidelityUpdate_9.6Migration.pdf); PDFs July 2023) | The in-scope list includes "Fidelity Charitable Gift Fund (Investment)" (FI ID 44892), mapped to the new "Fidelity (Investment)" Akoya feed. "Fidelity only allows the primary account owner to directly engage and consent for aggregation services" | F (2023) |
| [Empower help: "Fidelity Charitable Gift Fund Accounts"](https://support-personalwealth.empower.com/hc/en-us/articles/22540027869591-Fidelity-Charitable-Gift-Fund-Accounts) (403; snippet only, undated) | After Fidelity moved to Open Authentication, Fidelity Charitable accounts are "no longer able to sync under the Fidelity Investments option" | R |

**Reading [I].**
- **The s.8 channel did exist in practice** as screen-scrape or OFX-style aggregation, and in 2023 was routed into Fidelity's Akoya API. It covers primary holders only; advisers with delegate access are excluded.
- **Current status is unclear.** Whether Giving Accounts still flow through Akoya to any aggregator in 2026 is not confirmed, and one aggregator reports a break.
- **No sponsor-documented CSV or transaction-level export exists.** The repo's `donor-data-export-top10-2026.csv` row 1 ("PDF per document ... no transaction-level file") stands.
- **Suggested addition to that row:** "consumer-aggregator feed via Fidelity/Akoya existed in 2023 (primary holder only); status 2026 unverified".
- **Proposed follow-up:** P-B30A-01.

---

## 6. Source register

| # | Source | Type | Date | Used in |
|---|---|---|---|---|
| S1 | [Cal. Gov. Code §12599.9 (public.law mirror)](https://california.public.law/codes/government_code_section_12599.9) | statute | updated 2025-01-01 | §2 |
| S2 | [11 CCR §§314–323](https://oag.ca.gov/system/files/media/Cal-Code-Regs-titl-11-secs-314-323.pdf) | regulation | in force 2024-06-12 | §2 |
| S3 | [CA AG Charitable Fundraising Platforms page](https://oag.ca.gov/charities/pl) | regulator page | live 2026-11-15 | §2 |
| S4 | [Form PL-1 and instructions](https://oag.ca.gov/system/files/media/PL-1-Form-and-Instructions.pdf) | form | Orig. 01/2024 | §2 |
| S5 | [ISOR, platforms rulemaking](https://www.oag.ca.gov/system/files/media/pf-initial-statement-of-reasons.pdf) | rulemaking record | 2023–24 | §2 (types A–E rationale) |
| S6 | [Rev. Proc. 2018-32, IRB 2018-23](https://www.irs.gov/irb/2018-23_IRB) | IRS guidance | 2018-05-16 (current) | §3 |
| S7 | [Candid Charity Check sample PDF](https://docs.candid.org/files/guidestar-charity-check-pdf-api-example-response-13-1837418.pdf) | vendor document | generated 2025-04-16 | §3 |
| S8 | [Charity Check API schema](https://developer.candid.org/reference/charitycheck_v1.md); [example responses](https://developer.candid.org/reference/charity-check-example-responses.md); [FAQ](https://developer.candid.org/reference/faqs-charity-check.md); [get started](https://developer.candid.org/reference/get-started-with-charity-check.md); [PDF API](https://developer.candid.org/reference/charity-check-pdf-api.md) | vendor docs | 2026-09-07 | §3 |
| S9 | [Candid Subscriber License Agreement](https://candid.org/terms-of-service/candid-subscriber-license-agreement/) | contract | 2026-09-14 | §3.3 |
| S10 | [MS GIFT Donor Circular and Disclosure Statement](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf) | sponsor terms | 2024-08 | §4 |
| S11 | [FireAid investigative report (Latham), App. B GS DAF Program Circular](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf) | sponsor terms (third-party-hosted) | report 2025-09; circular ≥ 2024-09-30 | §4 |
| S12 | [BofA CGF Program Guidelines v3.2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf) | sponsor terms | 2024-09 | §4 |
| S13 | [BofA CGF fee schedule](https://www.bankofamerica.com/content/documents/philanthropic/cgf_fee_schedule.pdf) | sponsor fees | 2024-02/04 | §4 |
| S14 | [BofA Guide to Navigating Your DAF](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf) | sponsor guide | 9/2025 (modified 2026-02-23) | §4 |
| S15 | [Fidelity Charitable how-to (statements)](https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/how-to-view-and-download-statement-confirmation-and-tax-forms.pdf) | sponsor help | 2026-05 (metadata) | §5 |
| S16 | [Fidelity Charitable FAQs](https://www.fidelitycharitable.org/faqs/donor/using-my-giving-account.html) and [history FAQ](https://www.fidelitycharitable.org/faqs/all/find-giving-account-history.html) | sponsor help | live | §5 |
| S17 | [Fidelity Charitable Program Guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf) | sponsor terms | 2026-09-11 | §5 |
| S18 | [Fidelity Charitable License Agreement](https://www.fidelitycharitable.org/legal/license-agreement-and-copyright.html) | sponsor terms | reviewed 2021-01 | §5 |
| S19 | [Morningstar Fidelity open-banking notice (9/6)](https://advisor.morningstar.com/Enterprise/VTC/OB_FidelityUpdate_9.6Migration.pdf) and [(8/23)](https://advisor.morningstar.com/Enterprise/VTC/ClientCommunication-Q3%20Fidelity%20Update-8.23Migration.pdf) | aggregator notice | 2023-07 | §5 |
| S20 | [Empower help article](https://support-personalwealth.empower.com/hc/en-us/articles/22540027869591-Fidelity-Charitable-Gift-Fund-Accounts) | aggregator help (snippet) | undated | §5 |
| S21 | [Chariot nonprofit terms](https://givechariot.com/legal-nonprofit); [Endaoment terms](https://endaoment.org/terms) | vendor terms | live | §2.6 |

---

## 7. Data dictionary

### `wealth-captive-terms-2026.csv` (long format; one term per row)

| Column | Meaning |
|---|---|
| sponsor | Program name (MS GIFT; GS DAF / Goldman Sachs Philanthropy Fund; BofA CGF) |
| document | Document read, with date or dating basis |
| term_category | minimum / fee / investment / grant_ops / transfer_out / dormancy / succession / data / admin / document_status |
| term | Specific term key (e.g. `min_grant_usd`, `administration_fee`) |
| value | Value as stated; tiers are written out; "none found" for absences |
| quote_or_basis | Verbatim quote (≤40 words) or the section or table relied on |
| source_url | Primary URL |
| retrieved | Fetch date (2026-11-15) |
| evidence_label | F, F (OCR), F (third-party-hosted copy), F (absence), F (repo) |
| recency_admissible | Whether the evidence meets the 2021+ rule (all rows: yes) |
| notes | Supersession, caveats and [I] readings |

### `queue-proposals-batch30a.csv`

Columns follow [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md). The prefix is `P-B30A-`.

---

## 8. Limits

- **California.**
  - The analysis is textual. No AG guidance, FAQ on DAF vendors, enforcement action or registry entry addressing a DAF technology vendor was found or queried.
  - Statute text comes from a mirror (public.law), because leginfo and FindLaw returned 403.
  - Hawaii was not re-read at the primary level.
- **Candid.**
  - The PDF assessment rests on one public sample from April 2025. Current output may differ.
  - Subscriber Licence clauses were read through a fetch tool that summarises. The quoted phrases are short extracts.
- **GS DAF.** The circular is undated and comes from a third party's appendix. The live login page binds users to "GS DAF's Program Circular" without a version.
- **MS GIFT.** Values are OCR transcriptions. The extra fees for Other Grantee Organizations and recoverable grants are not published.
- **BofA.** The fund-fee chart's first column header reads "Sustainable" in the text layer, while the guidelines describe active (SMA) and passive versions. This was not reconciled.
- **Fidelity.** No logged-in check was made, so a CSV export behind login cannot be excluded. The aggregator evidence dates from 2023, and the 2026 status rests on a snippet.
