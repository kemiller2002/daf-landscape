# Queue items: donor data export at the top 10 sponsors, community-foundation grant rails, DonorSphere (P-FCG-05, P-CFR-01, P-CFR-02)

**Date:** 2026-11-14. **Status:** public pages only. I logged in nowhere, submitted no forms and contacted no one. Login pages and vendor front-end files were fetched without credentials, only to read host, title, footer and shipped code.
**Recency rule:** current-state findings use 2021+ evidence only. Older items are named and marked "pre-2021, not counted".

**Evidence labels:**
- **[F]:** first-party (the sponsor's, foundation's or vendor's own live page, document or shipped code, or an IRS e-file return).
- **[V]:** a vendor's statement about its own product or clients.
- **[R]:** third-party page or search-index summary that I could not open first-hand.
- **[I]:** my inference.

**Data written:**
- [`data/mission-2026-11-14/donor-data-export-top10-2026.csv`](../../data/mission-2026-11-14/donor-data-export-top10-2026.csv): 10 sponsor rows plus 2 comparator rows.
- [`data/mission-2026-11-14/community-foundation-rails-portals-2026-v2.csv`](../../data/mission-2026-11-14/community-foundation-rails-portals-2026-v2.csv): the 40-row v1 table with the 15 P-CFR-01 rows filled, and corrected Pittsburgh and Greater Houston portal fields.
- [`data/mission-2026-11-14/relationship-graph-edges-additions-8.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-8.csv): edges EH001–EH016. Of these, 11 are confirmed, 3 inferred and 2 unknown. EH005 corrects EG008.
- [`data/mission-2026-11-14/queue-proposals-export-cf.csv`](../../data/mission-2026-11-14/queue-proposals-export-cf.csv): proposals P-EXP-01 to P-EXP-05.

**Universe for P-FCG-05.** I took DAFRC FY2024 rows ranked by `eoy_daf_assets` ([repo copy](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)), whatever their DAFRC type:
1. Fidelity
2. NPT
3. DAFgiving360
4. Vanguard
5. GS DAF
6. SVCF
7. AEF
8. MS GIFT
9. RCF
10. NCF (DAFRC classes NCF as "Single Issue Charity")

BofA CGF is #11 and falls outside the ten.

---

## 0. Headline answers

| Item | Answer | Confidence |
|---|---|---|
| **P-FCG-05: donor-side machine-readable export, top 10** | **None of the ten documents a donor-side CSV, Excel or API export of contribution and grant history in 2021+ public material, and none has a portability statement.**<br>- **Closest:** DAFgiving360's advisor help names an "Export" function in Grant History for advisors in Schwab Advisor Center. This rests on a search-index summary only, because the live page returned 403 [R].<br>- **Statements or reports downloadable, format not stated:** NPT, SVCF and NCF [F].<br>- **PDF-only:** Fidelity [F].<br>- **View-only:** Vanguard [F].<br>- **Nothing public:** GS DAF, MS GIFT and RCF (donor side) [F, absence].<br>- **AEF is negative:** its Ren migration shows "only granting history from the past two (2) years" [F].<br>- **SVCF restricts the other way:** its DAF agreement bars advisors from collecting portal data "through automated means or otherwise" [F].<br>- **Benchmarks outside the ten:** Greater Washington CF (#38 CF) documents a donor CSV export of grant and gift history, with seven years of history ported [F]. DonorSphere's shipped front end includes Excel export of grant and contribution history [F code]. | High that nothing public exists for the ten. Logged-in views were not checked. |
| **P-CFR-01: rails at the 15 "nothing public" community foundations** | **10 of 15 now have a documented rail; 2 are unverified and 3 have nothing.**<br>- **Check for DAF grants (5):** GKCCF, San Diego, Omaha, SVCF (check by default; agreement allows wire and ACH) and Tulsa ("mailed").<br>- **Own ACH with limited or unstated scope (4):**<br>  - FFTC: an ACH grant-notification field on its nonprofit-fund form.<br>  - Columbus: an ACH authorisation form, dated Oct 2025.<br>  - NYCT: ACH via DocuSign for competitive grants; its DAF policy changed "grant checks" to "grant payments".<br>  - Boston: EFT eligibility named in 2022 and 2024 job postings.<br>- **Check for competitive grants only (1):** Tampa Bay.<br>- **Unverified (2):** Marin (a dead job-posting snippet [R]) and CFNJ (an April 2020 post, pre-2021).<br>- **Not found (3):** CF Greater Memphis, East Bay and GiveWell.<br>- **No named third-party rail:** none of the 15 shows Chariot, Bill.com, REPAY, PayPal or Ren ACH. | Each rail [F] unless marked; DAF coverage explicit only for GKCCF, San Diego, Omaha and SVCF |
| **P-CFR-02: DonorSphere** | **DonorSphere is made by FidTech Partners (Fiduciary Technology Partners LLC), founded 2005, with its Stamford CT address taken from 990 lines. Its companion back office is FoundationHub, formerly PGFundConnection.**<br>- **pgfundconnection.com** 301-redirects to foundationhub.com.<br>- **The `pgh` tenant is the Jewish Federation of Greater Pittsburgh, not The Pittsburgh Foundation.** This corrects EG008.<br>- **Confirmed users:** Greater Houston CF, Hawaii CF, JF Greater Pittsburgh and FJC (portal), plus Florida United Methodist Foundation (FoundationHub).<br>- **990 payees:** FidTech is paid by JF Greater Pittsburgh, Associated (Baltimore), FJC, United Jewish Foundation, JCF Greater MetroWest NJ and JEWISHColorado ($0.1m–$0.57m a year).<br>- **Inferred users:** Delaware CF, Greater Miami Jewish Federation and JF Northern NJ.<br>- **Ownership:** not found. | Vendor [F]; ownership [U] |

---

## 1. Method

1. **Sponsor documents (P-FCG-05).** For each sponsor I read its program guidelines, FAQs, help pages and donor guides, published 2021 or later. Each was fetched directly and searched for export, Excel, CSV, spreadsheet, download, history and portability. Where pages blocked scripted reads (DAFgiving360), I used search-index summaries, labelled [R].
2. **Portal fingerprints.** Where the repo had no platform for a sponsor, I read its unauthenticated login page: NCF (`secure.ncfgiving.com`) and GS DAF (`gspf.goldman.com`).
3. **Grant rails (P-CFR-01).** I searched each foundation for ACH, EFT, direct deposit, check and electronic payment. I also scanned sitemaps, and read DAF agreements and guides, RFPs, nonprofit FAQs and job postings. Chariot and Bill.com customer pages were searched for the 15 names.
4. **DonorSphere (P-CFR-02).**
   - **Shipped code:** the DonorSphere JavaScript bundle (`ghcf.donorsphere.org/main.*.js`) and its config file.
   - **Certificate logs:** CT logs ([crt.sh](https://crt.sh/?q=%25.donorsphere.org)).
   - **DNS:** records via dns.google.
   - **Vendor materials:** FidTech's website and product PDFs.
   - **Tenant pages:** each tenant's own page.
   - **990 lines:** the repo's 990 contractor harvest ([form990-contractors-harvest-full.csv](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv)).
   - **Caveat:** every `*.donorsphere.org` subdomain resolves (wildcard DNS to 52.138.119.67) and serves the same app shell, so a host answering is **not** evidence of a tenant.

---

## 2. P-FCG-05: donor-side data export across the ten largest sponsors

| # | Sponsor (FY2024 DAF assets) | Export documented? | What the public text says | Source |
|---|---|---|---|---|
| 1 | Fidelity Charitable ($66.2bn) | **No: PDF per document** | "Click the document name to view and download the PDF". The guidelines grant the privilege "to view, but not necessarily modify" contribution and grant history | [how-to PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/how-to-view-and-download-statement-confirmation-and-tax-forms.pdf) (2026-05-26); [Program Guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf) (2026-09-11) [F] |
| 2 | NPT ($42.1bn) | **No (2021+)** | "A quarterly statement … will be posted to GivingPoint, where it will be stored and will be available for download." The format is not stated. GivingPoint runs on Ren/Stellar iPhi (EA016). Ren's own iPhi DonorView description lists viewing "transaction statuses/histories" and statements, with no export | [NPT guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) (created 2026-10-15) [F]; [iPhi product descriptions](https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Product-Descriptions-v1.pdf) [V]. An NPT 2018 instruction sheet mentioned an Excel download (pre-2021, not counted) |
| 3 | DAFgiving360 ($40.9bn) | **Advisor-side only, unverified** | The advisor tutorial "How to access giving records" is summarised by the search index as naming an Export function in Grant History, in Schwab Advisor Center. The donor tutorial describes account history and letters, with no export | [advisor page](https://www.dafgiving360.org/content/how-recordkeeping-works-advisor), [donor page](https://www.dafgiving360.org/content/how-recordkeeping-works). Both returned 403; Wayback snapshots from 2025 exist but were unreadable here [R] |
| 4 | Vanguard Charitable ($21.9bn) | **No: view only** | "On the Documents & Statements page, select View Transaction Summary … filter by a specific transaction category". Online access lets you "View current and historical account activity" | [transaction FAQ](https://www.vanguardcharitable.org/faq/how-can-i-view-details-my-transaction); [registration FAQ](https://www.vanguardcharitable.org/faq/how-do-i-register-my-vanguard-charitable-account-online); [Policies](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) (updated 2026-01-09) [F] |
| 5 | GS DAF ($11.8bn) | **Nothing public** | The live "GS DAF Donor Web" runs on iPhi. Users "acknowledge that you have read GS DAF's Program Circular"; the only circular found is the 2008 one (repo) | [gspf.goldman.com](https://gspf.goldman.com/gspf/) [F] |
| 6 | SVCF ($9.6bn) | **No: statements downloadable** | The portal lets donors "review your giving history … download fund statements and investment performance reports". The agreement bars Authorized Advisors from collecting portal information "through automated means or otherwise" for non-grantmaking purposes | [DAF guide](https://www.svcf.org/assets/files/publications/svcf-daf_10_screen.pdf) (2025-05-08); [DAF agreement](https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf) (2025-08-22) [F] |
| 7 | AEF ($9.5bn) | **No; history truncated** | "Only granting history from the past two (2) years will be reviewable on this platform." The pilot pulled "the past 33 months" | [AEF platform FAQ](https://engage.aefonline.org/pilot-program-training-materials/) [F] |
| 8 | MS GIFT ($9.4bn) | **Nothing public** | The grantmaking PDF (modified 2024-10-01) contains no export or statement-format text | [MS GIFT grantmaking](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf) [F, absence] |
| 9 | RCF ($5.6bn) | **No (donor side)** | "You submit a grant recommendation through your donor portal". Ren's **charity** product does export: "You can also export grant details in a CSV" | [RCF FAQ](https://renaissancecharitable.org/faqs/) [F]; [Ren charity help](https://intercom.help/rengiving/en/articles/6232128-charity-grants) [V] |
| 10 | NCF ($5.5bn) | **No: report, format unknown** | "…or get a consolidated report of fund activity". Quarterly and annual statements. The login "MyGiving with NCF" shows Salesforce markers | [NCF guide](https://www.ncfgiving.com/guide-to-giving-at-NCF); [secure.ncfgiving.com](https://secure.ncfgiving.com/) [F] |

**Benchmarks found during the pass (not top 10):**
- **Greater Washington CF:** "You can also export your grant history, or your fund's gift history … as a CSV file for your records". It also "ported over seven years of fund history" ([GWCF, 2026-09-21](https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived)) [F].
- **DonorSphere's shipped bundle:** it defines `getDisbursementHistoryExcelAndPrint`, `getFundSummaryExcelAndPrint` and a `downloadFile(…,"allFunds.xlsx")` call ([bundle](https://ghcf.donorsphere.org/main.48440c3596588d4f9471570908a05a00.js)) [F code]. Whether each tenant enables these is [I].
- **Hawaii CF on DonorSphere:** it shows "information from January 1, 2020 to current"; older history must be requested ([HCF](https://www.hawaiicommunityfoundation.org/donorsphere)) [F].

**Reading [I]:**
1. **No large sponsor publishes the export.** Machine-readable donor export exists in the market, at a Foundation Cloud community foundation and in DonorSphere's code. None of the ten largest sponsors puts it in public material.
2. **Fidelity's "PDF-only, view right" is the norm, not an outlier.** Calibration should score Fidelity, Vanguard, NPT, SVCF, NCF, RCF, GS DAF and MS GIFT alike on Y1/Y2: no documented export.
   - **DAFgiving360** is a possible +1 once its advisor-side export is verified (P-EXP-01).
   - **AEF** is the one documented negative.
3. **Platform migrations are the main portability risk.** AEF (two years kept) and GWCF (seven years kept) show that migrations, more than policy, decide how much history a donor can see.
4. **SVCF's clause matters for agent access.** Its ban on automated collection is the only top-10 contractual limit found on donor-side aggregation. It bears on the agentic-control gap matrix (P-EXP-03).

---

## 3. P-CFR-01: grant-payment rails at the 15 foundations with nothing public

| # | Foundation | Rail found (2021+) | Covers DAF grants? | Source |
|---|---|---|---|---|
| 1 | SVCF | **Check by default.** Grants "are generally issued by checks bearing the name and logo of SVCF"; SVCF handles payment "(e.g., check, wire, ACH, etc.)". The guide says "a check or electronic transfer". Its corporate page says "We issue checks to your chosen charities" | **Yes** (DAF agreement) | [agreement](https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf) (2025-08); [guide](https://www.svcf.org/assets/files/publications/svcf-daf_10_screen.pdf) (2025-05); [corporate](https://www.svcf.org/corporations/corporate-responsibility) [F] |
| 3 | FFTC | **Own ACH** for nonprofit (agency) funds: the form asks for the "current ACH grant notification email recipient for your organization" | not stated | [NPO Representative form](https://www.fftc.org/sites/default/files/documents/FFTC_NPO_Representative_Information_Form_fillable.pdf) (modified 2025-07-10) [F] |
| 4 | GKCCF | **Check**: "In most cases, a grant check from a fund at the Community Foundation will arrive in the mail from USPS" | **Yes** (DAF grants) | [knowledge hub](https://www.growyourgiving.org/nonprofits/knowledge-hub/); [sample check](https://www.growyourgiving.org/wp-content/uploads/2024/11/Sample-Grant-Check-GKCCF.pdf) [F] |
| 5 | Columbus | **Own ACH**: "To receive ACH payments from The Columbus Foundation, your organization is required to submit" an automatic-deposit authorisation | not stated (form filed with Giving Store materials) | [ACH form](https://columbusfoundation.org/media/brvbfp22/tcf-giving-store-ach-forms-2025-2026_crgm-1.pdf) (2025-10-09) [F] |
| 6 | NYCT | **Own ACH via DocuSign** for competitive grants: "Grant recipients will be required to provide ACH (electronic banking) information via a secure DocuSign process". The DAF policy changed from "Grant checks are generally sent" (2024) to "Grant payments are generally sent" (2025 edition) | not stated (wording change only) | [RFP](https://grantseeker.thenytrust.org/Rfp/DownloadRfp/?id=106) (2025-04); [2025 DAF policy](https://thenytrust.org/wp-content/uploads/2026/03/DAF-Policies-and-Guidelines-2025-edited.pdf); [2024 DAF policy](https://thenytrust.org/wp-content/uploads/2024/06/2024-DAF-Policies-and-Guidelines.pdf) [F] |
| 8 | Boston | **Own EFT/ACH** for eligible grantees. One posting: "Identifies and corresponds with Electronic Funds Transfer (EFT) eligible grantee organizations to increase participation" (2022). Another: "Assists in the setup of electronic funds transfer via ACH" (2024) | not stated | [2022 posting](https://aapip.org/jobs/senior-finance-payables-coordinator-the-boston-foundation/); [2024 posting](https://aapip.org/jobs/fund-administration-payables-coordinator-the-boston-foundation/) [F, job board] |
| 12 | Marin | **Unverified**: a search snippet of the MCF Grants Manager posting mentions grantee "electronic payment information"; the page now returns 404 | — | [posting URL](https://www.marincf.org/inside-mcf/jobs-open-positions/grants-manager) [R] |
| 13 | CFNJ | **Not found (2021+).** An April 2020 post described a check "via USPS" or "an electronic bank transfer" showing as "Community Found" (pre-2021; now 404) | — | [2020 post](https://cfnj.org/were-very-much-open-for-business-a-refresh-on-our-grants-process) [R] |
| 15 | San Diego | **Check**: "Grant award checks are mailed directly to recipient nonprofit organizations. An award letter accompanies the check" | **Yes** (Recommend a Grant page) | [SDF](https://www.sdfoundation.org/ways-to-give/current-donor-resources/recommend-a-grant/) (modified 2026-01-13) [F] |
| 16 | CF Greater Memphis | not found (an aggregator mentions a "grant check" for 2024 capacity grants [R]) | — | — |
| 17 | Tulsa | **Mailed (check implied)**: "Please allow a window of 10 business days for grant requests to be processed and mailed to your agency" | likely (fund distribution requests) [I] | [Nonprofit FAQs](https://tulsacf.org/wp-content/uploads/2025/07/NonprofitFAQs.pdf) (2025-07-11) [F] |
| 21 | Tampa Bay | **Check** for competitive grants: "a grant check will be mailed" | no (competitive grants) | [competitive grants](https://www.cftampabay.org/annual-competitive-grants) [F] |
| 24 | East Bay | not found | — | [fund-advisor resources](https://www.ebcf.org/donors/donor-resources/resources-for-fund-advisors/) (no rail text) |
| 26 | Omaha | **Check**: "checks to nonprofits are issued by the Foundation twice a week". A 2019 Deluxe eCheck case study is pre-2021 and not counted | **Yes** (DAF how-it-works page) | [OCF](https://omahafoundation.org/donors/become-a-donor/how-a-fund-works/) (modified 2026-11-03) [F] |
| 28 | GiveWell CF | not found | — | — |

**Updated top-30 rail census (v1 plus this pass), counting each foundation once:**
- **Own ACH or electronic: 14.** These are the 10 from v1, plus FFTC, Columbus, NYCT and Boston, whose scope is unstated.
- **Third-party rail: 2.** Chariot at SPMF and Bill.com at CFGA.
- **Check only for DAF grants: 7.**
  - From v1: CCT and NHCF (Checkmint).
  - From this pass: GKCCF, San Diego, Omaha, Tulsa, and SVCF, whose check is the default.
- **Check documented only for competitive grants: 1** (Tampa Bay).
- **Unverified: 3.** Cincinnati, Marin and CFNJ.
- **Not found: 3.** Memphis, East Bay and GiveWell.

**Reading [I]:**
- **The "nothing public" group was mostly check-paying.** Where a rail could be found, five of the ten pay DAF grants by mailed check. The four with ACH describe it only for competitive or agency grants, or in staff postings.
- **The check-paid DAF pool is bigger than the v1 census implied.**
  - SVCF, GKCCF, San Diego, Omaha and Tulsa hold about **$14.1bn** of FY2024 DAF assets.
  - CCT and NHCF add **$5.1bn**.
- **For Chariot and AP-style rails**, the clearest top-30 targets are now SVCF (#1) and GKCCF (#4). Both describe checks for DAF grants in 2024–25 documents.

---

## 4. P-CFR-02: who builds DonorSphere and who runs it

**Vendor [F]:**
- **Products.** FidTech Partners' site lists **FoundationHub** ("Fund management & accounting") and **DonorSphere** ("A modern donor experience…"), plus GranteeSphere, Agency Pay and Giving Buttons ([home](https://www.fidtechpartners.com/); [solutions](https://www.fidtechpartners.com/solutions)).
- **Product PDF.** The DonorSphere Overview PDF (created 2026-09-19) ends "info@fidtechpartners.com". It lists online giving "through e-check, ACH, or credit card", processed through Authorize.net or Stripe ([PDF](https://www.fidtechpartners.com/_files/ugd/9bf60b_5371c949d2db40698b0024ef4548568b.pdf)).
- **Product lineage.** **pgfundconnection.com** 301-redirects to **foundationhub.com**. That site loads the same React shell as DonorSphere (same Google Maps key, Document360 help widget) and gives `support@foundationhub.com`.
  - DonorSphere marketing says statements are posted "when generated by PGFundconnection™" ([R], search snippet).
  - **So PGFundConnection is the older name for the FoundationHub back office [I].**
- **Company history.** "Over twenty years" serving faith-based organisations, financial institutions and public charities [V]. The founding year of 2005 comes from a FidTech news page [R].
- **Domain history.** The DonorSphere CT history begins in 2011 ([crt.sh](https://crt.sh/?q=%25.donorsphere.org)) [CT lead; not re-sourced, crt19].
- **Location and ownership.** Every 990 line gives the address as Stamford (or "Stanford"), CT. **I found no ownership, investor or parent.**

**Tenants:**

| Tenant (host label) | Organisation | Evidence | Status |
|---|---|---|---|
| `ghcf` | Greater Houston Community Foundation | [ghcf.org](https://ghcf.org/access-donorsphere/): "uses DonorSphere"; bundle "Powered by DonorSphere®" | confirmed [F] (EG007) |
| `hawaiicf` | Hawai'i Community Foundation ($270m DAF) | [HCF](https://www.hawaiicommunityfoundation.org/donorsphere): "We are excited to debut DonorSphere" | confirmed [F] |
| `pgh` | **Jewish Federation of Greater Pittsburgh** ($51m DAF) | [jewishpgh.org](https://jewishpgh.org/changes-to-donorsphere) (2022-02-14) links `pgh.donorsphere.org`. The 990 pays FidTech "FOUNDATION ADMINISTRATION" $525,587 (FYE 6/2025) | confirmed [F] |
| `delcf` | Delaware Community Foundation ($119m DAF) | GA id in the [config](https://ghcf.donorsphere.org/config/googleAnalyticsIDs.js); a DCF FAQ points to the DonorSphere login (delcf.org returned 403) | inferred [F config, R FAQ] |
| `fjc` | FJC, A Foundation of Philanthropic Funds ($336m DAF) | Guide served from the [fjc.donorsphere.org public API](https://fjc.donorsphere.org/API/DS/Public/Download/125?type=9). The 990 pays FidTech $109,565 (FYE 3/2025) | confirmed [F] |
| `fumf` | Florida United Methodist Foundation | [FUMF](https://fumf.org/news/foundation-launches-new-platform-to-enhance-partner-experience/) (2026-02-09): "FoundationHub™, a new platform powered by FidTech Partners" | confirmed [F] |
| `associated` | Associated Jewish Charities of Baltimore ($212m DAF) | CT name, plus 990 "ACCOUNTING SERVICES" $302,361 (FYE 6/2025) | vendor confirmed; portal [I] |
| `jcf` | JCF of Greater MetroWest NJ ($228m DAF) | CT name, plus 990 "Technology services" $290,188 (FYE 6/2024) | vendor confirmed; tenant label [I] |
| `jfmd` | United Jewish Foundation, Detroit area ($139m DAF) | CT name, plus 990 "ENDOWMENT SOFTWARE SERVICES" $205,940 (FYE 5/2025) | vendor confirmed; tenant label [I] |
| `jewishmiami`, `jfcin`, `jcfgm` | Greater Miami Jewish Federation; JF Cincinnati; JCF Greater Mercer | search-index listings only | inferred [R] |
| `jfnnj`, `gmw` | JF Northern NJ (by name); `gmw` unidentified | config / CT names only. `donorsphere.org` has a DNS wildcard, so DNS cannot confirm any label [crt19] | inferred / unknown (CT names: unverified lead) |
| Other CT names | `jpmc`, `mssb`, `tulane`, `umf`/`umfmichigan`, `drex`, `ignatius`, `nysarc`, `hoiuw`, `unitedwaypbc`, `UnitedWayOC`, `the-cei`, `ccs`, `a4g`, `aa`, `hf`, `ldc`, `mhbg`, `wpb`, `ftf` | names only. `jpmc` and `mssb` *may* denote bank tenants [I] | unknown |

**NCF trace [F code, I meaning]:**
- **What the bundle contains.** The DonorSphere bundle defines `APP_VERSIONS={v1:{name:"tp1",subdomainList:["ncf","ncfgiving2"]}}`. It also carries an NCF "Atlanta Office" address and links to `national.ncfgiving.com` forms.
- **What NCF runs today.** NCF's live login ("MyGiving with NCF", `secure.ncfgiving.com`) shows Salesforce markers.
- **Reading.** NCF was a client, pilot or design template at some point. **Its current use is not shown.**

**Pittsburgh Foundation question:**
- **Answer.** The queue asked whether The Pittsburgh Foundation is migrating to DonorSphere and who is behind `pgfundconnection.com`. **There is no sign of a Pittsburgh Foundation migration.**
- **Who `pgh` is.** The `pgh` tenant and the Pittsburgh-area client are the Jewish Federation of Greater Pittsburgh, a FidTech client for "more than two decades" according to a FidTech homepage testimonial [V].
- **Who runs the support domain.** `pgfundconnection.com` is FidTech's legacy back-office brand.
- **Repo effect.** EG008 should be read as superseded (EH005, status unknown).

**Reading [I]:**
- **FidTech's niche.** It is a small, long-lived vendor (portal plus sub-ledger plus outsourced back-office staff) whose core is Jewish federations and foundations. It also has a growing community-foundation foothold: Houston at $0.92bn DAF, Hawaii and Delaware.
- **Revenue floor from the harvest.** Its 990-visible fees from the five sponsors with amounts sum to about **$1.4m** in the latest years. That is a floor, because 990s list only payees above $100k.
- **Payments.** It sells ACH disbursement through GranteeSphere ("moving your foundation from checks to digital payments", [GranteeSphere](https://www.fidtechpartners.com/granteesphere)) [V]. No named bank or processor was found.

---

## 5. Corrections to existing repo text

1. **`community-foundation-rails-portals-2026.csv`, Pittsburgh row, and research §3:** "DonorSphere tenant 'pgh' configured" for The Pittsburgh Foundation is wrong. `pgh` is the Jewish Federation of Greater Pittsburgh (see v2 CSV, EH004/EH005).
2. **EG008** (DonorSphere → The Pittsburgh Foundation, inferred) is superseded by EH005 (status unknown).
3. **Rails census line "15 publish nothing"** becomes:
   - 10 documented, as in §3 above
   - 2 unverified (Marin, and CFNJ at pre-2021)
   - 3 not found (Memphis, East Bay, GiveWell)
4. **`sponsor-transfer-portability-terms-v2.csv`:** two cells should be read alongside `donor-data-export-top10-2026.csv`.
   - The NPT `history_export` cell ("format not stated") stands.
   - The SVCF row is not in v2. The new CSV adds its anti-automation clause.

---

## 6. Source register (accessed 2026-11-14)

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| S1 | DAFRC FY2024 dataset (repo copy) | dataset | 2026 | data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv |
| S2 | Fidelity how-to PDF | sponsor doc | 2026-05-26 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/how-to-view-and-download-statement-confirmation-and-tax-forms.pdf |
| S3 | Fidelity Program Guidelines | sponsor doc | 2026-09-11 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf |
| S4 | NPT DAF guide | sponsor doc | created 2026-10-15 | https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf |
| S5 | Ren iPhi product descriptions | vendor doc | 2023-09 (posted 2025-08) | https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Product-Descriptions-v1.pdf |
| S6 | DAFgiving360 recordkeeping pages | sponsor web [R] | 403 live | https://www.dafgiving360.org/content/how-recordkeeping-works-advisor |
| S7 | Vanguard Charitable FAQs and Policies | sponsor web | 2026-01-09 | https://www.vanguardcharitable.org/faq/how-can-i-view-details-my-transaction |
| S8 | GS DAF Donor Web login | sponsor host | live | https://gspf.goldman.com/gspf/ |
| S9 | SVCF DAF agreement | sponsor doc | 2025-08-22 | https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf |
| S10 | SVCF DAF guide | sponsor doc | 2025-05-08 | https://www.svcf.org/assets/files/publications/svcf-daf_10_screen.pdf |
| S11 | AEF platform FAQ | sponsor web | live | https://engage.aefonline.org/pilot-program-training-materials/ |
| S12 | MS GIFT grantmaking PDF | sponsor doc | 2024-10-01 | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf |
| S13 | RCF FAQ; Ren charity help | sponsor/vendor web | live | https://renaissancecharitable.org/faqs/ ; https://intercom.help/rengiving/en/articles/6232128-charity-grants |
| S14 | NCF guide; NCF login | sponsor web | live | https://www.ncfgiving.com/guide-to-giving-at-NCF ; https://secure.ncfgiving.com/ |
| S15 | GWCF portal launch (CSV export) | CF web | 2026-09-21 | https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived |
| S16 | DonorSphere bundle and config | vendor code | live | https://ghcf.donorsphere.org/main.48440c3596588d4f9471570908a05a00.js ; https://ghcf.donorsphere.org/config/googleAnalyticsIDs.js |
| S17 | FidTech Partners site and product PDFs | vendor web | 2026-09-19 PDFs | https://www.fidtechpartners.com/ ; https://www.fidtechpartners.com/solutions ; https://www.fidtechpartners.com/granteesphere |
| S18 | pgfundconnection.com → foundationhub.com | vendor host | live (301) | https://www.pgfundconnection.com/ |
| S19 | CT log donorsphere.org | CT | 2011– | https://crt.sh/?q=%25.donorsphere.org |
| S20 | HCF DonorSphere page | CF web | live | https://www.hawaiicommunityfoundation.org/donorsphere |
| S21 | JFGP "Changes to Donorsphere" | federation web | 2022-02-14 | https://jewishpgh.org/changes-to-donorsphere |
| S22 | FUMF FoundationHub launch | foundation web | 2026-02-09 | https://fumf.org/news/foundation-launches-new-platform-to-enhance-partner-experience/ |
| S23 | FJC DonorSphere public guide | tenant doc | 2022-11-08 | https://fjc.donorsphere.org/API/DS/Public/Download/125?type=9 |
| S24 | 990 contractor lines naming Fiduciary Technology Partners (FY2021+) | IRS XML | FYE 2022–2025 | data/mission-2026-11-14/form990-contractors-harvest-full.csv (e.g. https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601219349301200_public.xml) |
| S25 | GKCCF knowledge hub; sample check | CF web/doc | live; 2021 PDF | https://www.growyourgiving.org/nonprofits/knowledge-hub/ ; https://www.growyourgiving.org/wp-content/uploads/2024/11/Sample-Grant-Check-GKCCF.pdf |
| S26 | Columbus ACH authorisation form | CF doc | 2025-10-09 | https://columbusfoundation.org/media/brvbfp22/tcf-giving-store-ach-forms-2025-2026_crgm-1.pdf |
| S27 | NYCT RFP and DAF policies | CF docs | 2025-04; 2024; 2026-03 | https://grantseeker.thenytrust.org/Rfp/DownloadRfp/?id=106 ; https://thenytrust.org/wp-content/uploads/2026/03/DAF-Policies-and-Guidelines-2025-edited.pdf |
| S28 | Boston Foundation job postings | job board | 2022-08-11; 2024-08-06 | https://aapip.org/jobs/senior-finance-payables-coordinator-the-boston-foundation/ ; https://aapip.org/jobs/fund-administration-payables-coordinator-the-boston-foundation/ |
| S29 | FFTC NPO representative form | CF doc | 2025-07-10 | https://www.fftc.org/sites/default/files/documents/FFTC_NPO_Representative_Information_Form_fillable.pdf |
| S30 | San Diego Foundation Recommend a Grant | CF web | 2026-01-13 | https://www.sdfoundation.org/ways-to-give/current-donor-resources/recommend-a-grant/ |
| S31 | Tulsa CF Nonprofit FAQs | CF doc | 2025-07-11 | https://tulsacf.org/wp-content/uploads/2025/07/NonprofitFAQs.pdf |
| S32 | CF Tampa Bay competitive grants | CF web | live | https://www.cftampabay.org/annual-competitive-grants |
| S33 | Omaha CF "How a fund works" | CF web | 2026-11-03 | https://omahafoundation.org/donors/become-a-donor/how-a-fund-works/ |

---

## 7. Data dictionaries

**`donor-data-export-top10-2026.csv`**

| Column | Meaning |
|---|---|
| `dafrc_rank_fy2024` | Rank by DAFRC FY2024 `eoy_daf_assets` across all types; "comparator" rows are benchmarks outside the ten. |
| `sponsor`, `ein`, `fy2024_daf_assets_usd` | Sponsor name, EIN as in DAFRC (no dash), and DAFRC FY2024 DAF assets. |
| `donor_portal_platform` | Donor-portal software as fingerprinted here or in the repo (edge IDs cited). |
| `machine_readable_export_documented` | yes / no / advisor-side only / no public documentation, from 2021+ public text. |
| `export_format_documented` | Format named in the text (CSV, Excel, PDF), or "not stated". |
| `export_scope` | What the export or download covers. |
| `history_depth_note` | Any stated limit on how much history is online. |
| `portability_or_data_rights_statement` | Any clause granting, limiting or restricting donor data access or reuse. |
| `key_quote` | Verbatim quote (≤40 words) or a labelled summary. |
| `evidence_label` | F / V / R / I as defined above. |
| `source_urls`, `source_dates`, `retrieved` | Sources (" ; "-separated), their dates, and access date. |
| `y_score_implication` | Suggested reading for A1 and A3/A4 Y (data portability) scores. |
| `notes` | Caveats. |

**`community-foundation-rails-portals-2026-v2.csv`**
- **Columns:** identical to v1 (see [v1 dictionary](queue-community-foundation-rails-portals.md#7-data-dictionary-community-foundation-rails-portals-2026csv)).
- **Rows changed:** `payment_rails`, `eft_provider` and `source_urls` for the 15 P-CFR-01 rows; `portal_vendor`/`portal_evidence` for Pittsburgh (DonorSphere correction) and Greater Houston (vendor named).
- **Rows unchanged:** all others.

**`relationship-graph-edges-additions-8.csv`**
- **Columns:** same as `relationship-graph-edges.csv`.
- **IDs:** EH001–EH016.
- **Statuses used:**
  - `confirmed`: a first-party page or 990 line.
  - `inferred`: config, CT or search-index only.
  - `unknown`: a correction, or a code trace whose meaning is open.

**`queue-proposals-export-cf.csv`**
- **Format:** per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- **IDs:** P-EXP-01 to P-EXP-05.

## Validation corrections (wave 8, 2026-11-14) — governing
Source: [validation-wave8-report.md](validation-wave8-report.md). Where these conflict with the text above (including the earlier wave-7 Audax note), these govern.

17. **Line 38.** Replace "its DAF agreement bars advisors from collecting portal data 'through automated means or otherwise'" with: "its DAF agreement bars advisors from collecting website or portal information '(through automated means or otherwise) … for any purposes unrelated to' their grantmaking privileges, and puts third-party portal access without SVCF approval at the advisor's risk, with an indemnity".
18. **Line 86.** Replace "Its ban on automated collection is the only top-10 contractual limit" with: "Its purpose-limited bar on automated collection, together with the third-party-access indemnity, is the only top-10 contractual limit".
19. **Line 113 and the P-CFR-01 summary.** Replace "Check for DAF grants (5)" with "Check by default for DAF grants (5; SVCF 'generally', GKCCF 'in most cases', Tulsa 'mailed')".
20. **P-CFR-02, the "990 payees" bullet.** Add: "990 payee is not the same as a DonorSphere user. Baltimore books FidTech as 'accounting services' and JEWISHColorado as 'investment management', which points to back-office (FoundationHub) use."

## Compliance note (2026-11-15) — governing
crt.sh disallows all crawlers in its robots.txt. Any claim in this document that rests **only** on crt.sh certificate data is downgraded to an unverified lead until re-sourced. See [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md).
