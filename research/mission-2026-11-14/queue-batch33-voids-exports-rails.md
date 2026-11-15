# Batch 33B: uncashed-check rules (P-NPP-02), community-foundation donor export (P-EXP-02), Ren DFX export (P-BNK-03), and the rail behind NPT's GivingPoint programs (P-B31C-01)

**Date:** 2026-11-15. **Queue items:** P-NPP-02, P-EXP-02, P-BNK-03, P-B31C-01 (`data/mission-2026-11-14/research-priority-queue.csv`).

**Status: public sources only.**
- I logged in nowhere, submitted no forms and contacted no one.
- I read public web pages, public PDFs, and the public JavaScript bundles that load on GivingPoint site roots. I called no APIs.
- I checked robots.txt for each host before scripted reads. I did not fetch fcsuite.com.
- I respected AEF's crawl-delay by reading only three AEF pages.
- AEF's ACH-setup page shows bank details. I read it but **do not reproduce** them.

**Recency rule:** every current-state claim rests on 2021+ evidence. Undated live pages are marked "undated, live 2026-11-15". One 2018 J.P. Morgan PDF that I found is excluded.

**Read first and built on:** the following files, with their governing corrections:
- `queue-batch31-ren-npact-gl.md`, including the wave-16 corrections. The RDE/Legacy enum is used as stated there.
- `queue-npt-givingpoint-fidelity-stack.md`, including the wave-12 corrections. The Global Accelerator attribution stays [I].
- `queue-sponsor-terms-data-clauses.md`, including the wave-9 corrections.
- Also: `queue-batch28-ledgers-voids-cf-apps.md`, `queue-batch29-complaints-voids.md`, `queue-donor-export-cf-payments-donorsphere.md`, `nonprofit-side-panel-2026-evidence.csv` and `community-foundation-rails-portals-2026-v2.csv`.

**Evidence labels:**
- **[F]:** first-party. This covers the sponsor's or vendor's own page or PDF, and code served from its own site.
- **[V]:** a vendor's statement about its own product.
- **[R]:** a search-index summary of a page I could not read first-hand.
- **[I]:** my inference.

**Quote check:** quotes are verbatim and 40 words or fewer. A script checked every quote in both CSVs against the fetched source text. The bundle quotes in §4 were checked by grep.

**Outputs:**
- [`data/mission-2026-11-14/uncashed-grant-rules-2026.csv`](../../data/mission-2026-11-14/uncashed-grant-rules-2026.csv): 19 rows covering 11 sponsors and rails.
- [`data/mission-2026-11-14/donor-export-evidence-cf-2026.csv`](../../data/mission-2026-11-14/donor-export-evidence-cf-2026.csv): 40 rows, one for each top-40 community foundation.
- [`data/mission-2026-11-14/queue-proposals-batch33b.csv`](../../data/mission-2026-11-14/queue-proposals-batch33b.csv): P-B33B-01 to P-B33B-03.

---

## 0. Answers

| Item | Answer | Confidence |
|---|---|---|
| **P-NPP-02** | **Fidelity still publishes the only national-sponsor void window: 90 days, with funds returned to the Giving Account.** A new published rule is **GiveClear (TIFIN Give): 90 days, "cancelled and redeposited into your account"**, worded the same as BlueGive's [F].<br>**PayPal Giving Fund (policy updated 2025-01-01):** a check to an unenrolled charity that "is not cashed within the time period specified on the check" may lead PPGF to remove the charity and reassign the funds. The period itself is not published. The 2025 policy also cut PPGF's check delivery to unenrolled charities from 90 days to 45 days after month-end [F].<br>**No void window found** at Vanguard (return of funds "at the discretion of Vanguard Charitable"; issued grants cannot be cancelled), NPT (only the 14-day PayPal expiry), DAFgiving360 (2024 policies; the 2026 page is unreadable here), AEF, MS GIFT or BofA CGF.<br>**Reissue rules:** Fidelity reissues only at the donor's request. Ren reissues after confirming the check has not cleared, and ACH reissue needs the donor to allow "payment flexibility".<br>**Escheat:** **none of the 11 sponsors and rails states an escheat treatment**, and NPT's FY2025 statements are a 2-page summary with no notes. | High on the stated rules; high on absence for the documents read; escheat unknown everywhere |
| **P-EXP-02** | **8 of the top 40 CFs document a donor download in public guides. 6 of them name a grant-history export:** CCT (CSV), Columbus (spreadsheet), Saint Paul & Minnesota (Excel), Omaha (Excel), Orange County CF (Excel) and GWCF (CSV, repo). Minneapolis exports fund activity to Excel or PDF, and GKCCF says "download your granting history" without naming a format.<br>The 6 hold **18.2%** of top-40 CF DAF assets; all 8 hold **25.4%**. Tampa documents a CSV of contributions only.<br>5 guides read do not mention export (Atlanta, Denver, Houston, Seattle, NE Florida). 24 have no public guide I could find.<br>**By vendor:** export shows up on **Foundant CommunitySuite** (Foundant says grant-history export was added 2024-08-27 [V]), **iPhi DonorView** (2 tenants [F]), **GiftingNetwork** (CCT) and **Foundation Cloud** (GWCF). No **Salesforce Experience Cloud** tenant documents one. | Medium: tenant guides lag vendor releases, so absences are weak |
| **P-BNK-03** | **BofA CGF: yes, the Grant Listing also has "Export to Excel".** The 2025/26 guide (PDF modified 2026-02-23) shows an "Export to Excel" button in its Grant Listing screenshot (p.28), next to the date range and above Pending and Paid Grants. The guide's *text* mentions export only on the Contribution Listing (p.14) [F, screenshot]. Whether the button covers Paid as well as Pending grants is not stated.<br>**MS GIFT: nothing public.** The 2025 brochure promises portal access to "track activity", with no export.<br>**Other Ren DFX programs:** the only other public guide found is RCF's DFX guide (2021-10), which shows no export. Ren's UBS and Northwestern Mutual guides now 404.<br>**New:** the Ren-built **GivingPoint** code ships 17 Excel-export handlers, including grant payments (§4.3). | High (BofA screenshot); medium (MS GIFT absence) |
| **P-B31C-01** | **NPT pays, not Ren: the GivingPoint programs show no sign of Ren's RDE rail.**<br>- **J.P. Morgan site:** the jpmgiving.org bundle tells donors: "NPT will verify that the organization has an active EFT status … If the EFT status is inactive, NPT will issue a check" [F].<br>- **GivingPoint payment enum:** `PhysicalCheck:1, CreditCard:2, Wire:5, Check:6, Cash:11, Eft:16`. It has no `RDE_*` or "Ren for Charities" value. Ren's own charity app uses those labels.<br>- **NPT's charity-facing pages** (modified 2026-11-10) name only PayPal Grant Payments and checks. NPT's own engineering team "built NPT's PayPal integrations".<br>**Reading [I]:** if NPT grants appear in Ren for Charities at all, they would appear as "Legacy". Ren's hosting of 13 NPT-family sites does not add to the RDE network. | Medium-high: no grant letter or charity-side remittance was seen |

---

## 1. P-NPP-02: uncashed-check void window, reissue and escheat

### 1.1 Sponsor table (detail and quotes in `uncashed-grant-rules-2026.csv`)

| Sponsor / rail | Void window | After void | Reissue | Escheat | Source |
|---|---|---|---|---|---|
| Fidelity Charitable | **90 days** | Giving Account | Only if the donor asks. A lost check is cancelled and a new grant made. The EFT exception is [R] only, because that page now 404s | not stated | [returned-grant FAQ](https://www.fidelitycharitable.org/faqs/all/returned-grant.html); [nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html); [lost check](https://www.fidelitycharitable.org/faqs/all/lost-grant-check.html) [F] |
| Vanguard Charitable | not stated | "at the discretion of Vanguard Charitable" | Not stated. "Advisors cannot cancel grants that have already been approved and issued" | not stated | [Policies (updated 2026-01-09)](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) [F] |
| NPT | none for checks. PayPal payments expire in 14 days and are then reissued as a check | not stated | not stated | not stated. FY25 statements have no notes | [Guide (2026-10-15)](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf); [For Nonprofits](https://www.nptrust.org/for-nonprofits/); [FY25 financials](https://www.nptrust.org/fy25-ar-consolidated-financials-npt/) [F] |
| DAFgiving360 | not stated | not stated | not stated (only a 30-day decline if the charity cannot be reached, before payment) | not stated | [2024 Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) [F]. The 2026 page returned 403 |
| AEF | not stated | not stated | Ren procedure (below) applies to Ren-paid grants [I] | not stated | [Charities page (2026-04-20)](https://www.aefonline.org/charities/) [F] |
| Ren for Charities (AEF, MS GIFT, RCF) | not stated | not stated | On request: "confirm that the original check has not cleared". ACH only if the donor allows "payment flexibility" | not stated | [Ren help (2025-12-10)](https://intercom.help/rengiving/en/articles/13123383-what-should-i-do-if-i-have-issues-with-receiving-a-grant-check-or-need-to-request-a-reissue) [V] |
| MS GIFT | not stated | not stated | not stated | not stated | [How It Works (2025-10-24)](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf) [F, absence] |
| BofA CGF | not stated (the portal shows a "date cleared") | not stated | not stated | not stated | [Program Guidelines 2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf); [DFX guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf) [F, absence] |
| PayPal Giving Fund | "time period specified on the check" (not published) | charity may be removed and funds reassigned | none; reassignment instead | not stated | [Delivery Policy 2025-01-01](https://www.paypalobjects.com/marketing/web25/us/paypal-giving-fund/policy-updates/ppgf-us-delivery-01012025.pdf) [F] |
| GiveClear (TIFIN Give) | **90 days** | "redeposited into your account" | Support voids and reissues for a wrong address | not stated | [Granting FAQs (2026-11-10)](https://intercom.help/give-ria/en/articles/10670838-granting-faqs) [F] |
| BlueGive | **90 days** | as GiveClear | as GiveClear | not stated | [Granting FAQs (2026-11-10)](https://intercom.help/bluegive-help-center/en/articles/10597826-granting-faqs) [F] |
| Chariot DPN | [R] 90 days | — | — | — | The [intercom article](https://intercom.help/givechariot/en/articles/8709675-dafpay-network-check-issuance) now 404s. The repo row rests on an earlier read |

### 1.2 Reading

1. **Where a rule is published, it is 90 days and the money goes back to the donor's account** (Fidelity, GiveClear, BlueGive). The word "escheat" appears nowhere. Returning funds to the DAF account at 90 days, well before any state dormancy period, is presumably what keeps escheat from arising [I].
2. **PPGF is the exception in design.** It sends no money back to a donor. It may drop the charity and reassign the funds. This matches its role as a platform that "retains exclusive legal control over all donations" [F].
3. **Vanguard and NPT keep discretion.** Vanguard's text makes any return of funds discretionary. NPT publishes an expiry only for its electronic rail.
4. **Check volume makes this matter.** Fidelity's prior-year voided-grant adjustment was $11.15m in FY2025 (repo, `daf-grant-voids-disclosures.csv`). The other nationals net voids inside grants paid (batch 29), so their volumes cannot be seen.
5. **Audited-note route:** NPT's FY25 annual-report financials ([PDF](https://www.nptrust.org/fy25-ar-consolidated-financials-npt/)) are a 2-page summary, with grants payable of $300.6m against $363.8m the year before (stated in thousands) and no notes. Batch 28 already found no void note in Fidelity's FY2025 audit. Vanguard's audit was not found online.

**Change to the panel field `void_return_policy`:** 12 of 20 sponsors and rails are now covered, up from 10, by adding GiveClear and PPGF. PPGF's cell changes from "PayPal expiry" to the reassignment rule above.

---

## 2. P-EXP-02: community-foundation donor export (top 40)

### 2.1 Positive evidence

| CF (rank) | Vendor (repo) | What the public guide says | Source |
|---|---|---|---|
| CCT (2) | GiftingNetwork | "You can however export CSV and chart-format gift history and grant history reports anytime." | [Donor Portal FAQ (2025-12-02)](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf) [F] |
| GKCCF (4) | white-label (donor-portal.org) | "You can also sort, filter, and download your granting history." No format named | [GKCCF tips (2022, mod. 2026)](https://growyourgiving.org/news/7-tips-for-maximizing-your-online-giving-experience) [F] |
| Columbus (5) | Foundant CSuite | "Gives you the option to export information on previous grants into a spreadsheet to save and/or print." | [Portal guide (2025-04)](https://columbusfoundation.org/media/p1za1dz4/csuite-fund-portal-donor-resources-2025.pdf) [F] |
| Minneapolis (19) | iPhi DonorView | "You can export the information into an Excel or PDF document." (Fund Activity Details) | [DonorView cheat sheet (2022)](https://www.minneapolisfoundation.org/wp-content/uploads/2023/11/DonorView-FAQs-Final.pdf) [F] |
| Tampa Bay (21) | Foundant CSuite | "Use the Export button to download a CSV file." This covers contribution history only | [Portal guide](https://www.cftampabay.org/portal-guide) (undated, live) [F] |
| Saint Paul & MN (22) | iPhi DonorView | "Based on the search criteria, the Grant History will generate. Results can be exported to Excel." | [DonorView grants guide (2022-09)](https://de4vzavwp1bb7.cloudfront.net/general/Donors/Files/DonorView-Instructions/Viewing-and-Managing-Your-Grants.pdf) [F] |
| Omaha (26) | Foundant CSuite | "To download a full list of grants from your fund, click on the Export" tab, and the system will create an Excel spreadsheet" | [MyAccount (2025-03-04)](https://omahafoundation.org/myaccount/) [F] |
| Orange County CF (33) | unknown | "Download History" option "to export grant information into a Microsoft Excel spreadsheet" | [Donor Portal FAQs (2025-09-30)](https://www.oc-cf.org/donors/donor-portal-faqs/) [F] |
| GWCF (38) | Foundation Cloud | CSV export of grant history (repo) | [GWCF (2026-09-21)](https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived) [F] |

### 2.2 Vendor matrix [I, built from 2.1 and repo vendor map]

| Portal vendor (top-40 tenants) | Evidence of a donor grant-history export | Tenants with a public positive |
|---|---|---|
| Foundant CommunitySuite (13) | **Vendor:** "Added donation and grant history export for fund managers" (2024-08-27) on the [Idea Lab](https://idealab.foundant.com/forums/597718-communitysuite-idea-lab/suggestions/48688049-export-grants-or-grant-history-new-portal) [V]. The idea was filed because the new portal's Grants tab lacked the button. A Foundant support article says "Click Export to export the grant history list" [R; 403 to fetch] | Columbus, Omaha. Tampa covers contributions only. Atlanta and Denver guides are silent |
| Ren/Stellar iPhi DonorView (5) | Excel export on tenant guides | Saint Paul & MN (grants), Minneapolis (fund activity) |
| GiftingNetwork (2) | CSV on tenant FAQ | CCT. No FFTC guide found |
| NPact Foundation Cloud (3) | CSV on tenant news | GWCF. San Diego and Tulsa: none found |
| DonorSphere (1) | Excel in shipped code (repo). Not in GHCF help | — |
| Salesforce Experience Cloud (6) | none found. Tenant-built | — |
| SmartSimple, Power Pages, NetCommunity, GOfund, custom (6) | none found for these tenants | — |

**Reading [I]:** portability follows the vendor. Every positive sits on a packaged CF portal: Foundant, iPhi, GiftingNetwork or Foundation Cloud. None sits on a CF that built its own Salesforce or Power Pages portal. The queue's hypothesis holds with medium confidence. The remaining uncertainty is tenant lag: Foundant shipped the export in August 2024, while Atlanta's 2025 guide still describes only viewing and sorting.

---

## 3. P-BNK-03: export on Ren DFX sponsor portals

- **BofA CGF.** The guide ([PDF](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf), created 2025-11-14, modified 2026-02-23, 38 pp.) gives these steps for the Contribution Listing (p.14): "You can export to Excel to sort and do analysis" [F].
  - **Grant Listing (p.28).** The screenshot shows an "Export to Excel" button on the date-range row, above the Pending Grants and Paid Grants tables. The callout text does not mention it. I read this from a 110-dpi render of the page [F, screenshot].
  - **Grant Details (p.29).** The page shows the check number and "date cleared".
  - **Effect.** The repo's "contributions only" reading should change to "contributions and grant listing; scope of the grant export (pending vs. paid) not stated".
- **MS GIFT.** The [How It Works brochure](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf) (modified 2025-10-24) offers "Donor portal access to recommend grants, track activity, and view balances in one secure place". It says nothing about export or file formats [F, absence]. Ren's FAQ (repo) says MS GIFT donors have no separate log-in, which suggests access through Morgan Stanley's own channels [I].
- **Other DFX.** Ren's [RCF DFX guide](https://www.reninc.com/wp-content/uploads/2022/02/Donor-User-Guide-RCF-Rebranded-10-21-Updated-2-3.pdf) (2021-10, 7 pp.) covers statements, grant recommendation, documents and preferences. It has no export [F, absence]. Ren's UBS (2024-07) and Northwestern Mutual (2024-06) guides are indexed but return 404.
- **Reading [I].** BofA's export comes from the DFX platform's grid control. The other DFX sponsors probably share it, but none documents it publicly.

---

## 4. P-B31C-01: which rail NPT's Ren-hosted programs use

### 4.1 Evidence

| Evidence | What it shows |
|---|---|
| jpmgiving.org [main bundle](https://jpmgiving.org/main-JBUINBFD.js), read 2026-11-15 [F] | Donor-facing charity popover: "NPT will verify that the organization has an active EFT status at the time of grant disbursement." and "If the EFT status is inactive, NPT will issue a check." |
| nptgivingpoint.org [main bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js) and icgfdaf.org [main bundle](https://icgfdaf.org/main-2IGH5MJZ.js) [F] | "Depending on the details of the grant recommendation and the charity's EFT status at the time of disbursement, the grant may be sent via EFT or check." The main bundles test `defaultPaymentTypeCode===16`, and the NPT lazy chunk `chunk-HARSYLHF.js` renders an "EFT Enrolled" badge |
| GivingPoint chunk [`chunk-GNPJY3AQ.js`](https://www.nptgivingpoint.org/chunk-GNPJY3AQ.js) (same enum in jpmgiving.org `chunk-QSILYNTZ.js`) [F] | Payment-type enum `PhysicalCheck:1,CreditCard:2,Wire:5,Check:6,Cash:11,Eft:16`. There is no RDE or "Ren for Charities" value, and no "PayPal" string in the 3 main bundles or in the 110 NPT and J.P. Morgan lazy chunks (ICGF chunks not fetched) |
| Ren for Charities [app.js](https://static.rengiving.com/static/frontend/js/app.js) (repo, batch 31) [F] | Ren's charity app labels its own rail `RDE_ACH: "Ren for Charities ACH"` and labels third-party payments "Legacy" |
| NPT [For Nonprofits](https://www.nptrust.org/for-nonprofits/) (modified 2026-11-10) [F] | Tells charities to "Sign up for Grant Payments" through PayPal. There is no Ren, ACH form or Ren for Charities link |
| NPT [PayPal post](https://www.nptrust.org/philanthropic-resources/philanthropist/nonprofits-receive-over-65-million-in-grants-from-npt-through-paypal-grant-payments/) (2023, modified 2026-10-05) [F] | Its author "leads the team of developers & engineers that built NPT's PayPal integrations". The payment integration is built in-house at NPT |

### 4.2 Reading [I]

- The donor text names **NPT** as the party that verifies EFT status and issues checks. The platform's payment codes are the older numeric iPhi-style codes, not Ren's RDE labels. NPT runs its own PayPal integration.
- Together these point to NPT paying grants on its own rails: PayPal Grant Payments as the "EFT", and NPT-issued checks or wires. Ren supplies the portal and the platform only.
- What remains open:
  - whether the "EFT" code also covers a non-PayPal ACH;
  - whether NPT grants are mirrored into Ren for Charities as "Legacy" items.

  A posted NPT grant letter or charity remittance would settle both. No such letter was found.
- **Effect on the "25+ programs" count (batch 31 §1):** the 13 NPT-family sites should be counted as Ren-*hosted*, not RDE-*paying*.

### 4.3 By-product: GivingPoint ships donor Excel export in code

- **Handlers.** The same GivingPoint build (NPT and J.P. Morgan chunks `chunk-GNPJY3AQ.js` / `chunk-QSILYNTZ.js`) contains 17 `…GetExcelExport` handlers, including:
  - `onApiDafAccountsGrantPaymentsGetExcelExport`
  - `onApiDafAccountsGrantActivityGetExcelExport`
  - `onApiDafAccountsContributionActivityGetExcelExport`
  - `onApiDafAccountsFundActivityDetailsGetExcelExport`
- **Front end.** Data tables expose an `exportExcel` output, and an export service writes `.xlsx` files [F, code].
- **What it does not show.** Code does not show that the feature is turned on for donors. NPT's public guide mentions only downloadable statements (repo).
- **Status.** This parallels DonorSphere (code only). It is put forward as P-B33B-01 and does not yet change NPT's score.

---

## 5. Corrections and notes for existing repo text (proposed, not governing)

1. **`nonprofit-side-panel-2026-evidence.csv`:**
   - Add a `void_return_policy` row for **GiveClear (TIFIN Give)**: 90 days, redeposited, using U17.
   - Replace the `paypal_grant_payments` / PPGF cell with the 2025 Delivery Policy rule (U15): checks not cashed within the period on the check lead to possible removal and reassignment; check delivery is within 45 days of month-end.
   - Keep the PayPal Grant Payments 14-day expiry for NPT.
2. **Fidelity rows:**
   - The `help/grant-delivery-faq.html` page cited in search results now returns 404. Any repo text that relies on its "EFT exception" should be marked [R].
   - The 90-day rule rests on the [returned-grant FAQ](https://www.fidelitycharitable.org/faqs/all/returned-grant.html). The 2026-09-11 Program Guidelines do not contain it.
3. **Chariot DPN check-issuance row:** the intercom URL now returns 404. Mark it "earlier read; not re-verified 2026-11-15".
4. **`bank-program-terms-2026.csv` / P-BNK-03 queue text:** change "BofA's 2025 DFX guide documents Excel export of contributions only" to "Contribution Listing (text, p.14) and Grant Listing (screenshot, p.28) both show Export to Excel; grant export scope not stated".
5. **`queue-batch31-ren-npact-gl.md` §1.2, NPT GivingPoint row:** change "Not established; probably 'Legacy' [I]" to "NPT-paid: donor text says NPT verifies EFT status and issues checks; GivingPoint payment enum has no RDE value (batch 33B §4) [F/I]".
6. **`donor-data-export-top10-2026.csv`, NPT row:** add to notes "GivingPoint front-end code contains Excel export handlers for grant payments and activity (batch 33B §4.3); availability to donors unverified".

---

## 6. Source register

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| S1 | Fidelity returned-grant FAQ | sponsor [F] | undated, live | https://www.fidelitycharitable.org/faqs/all/returned-grant.html |
| S2 | Fidelity nonprofit FAQ | sponsor [F] | undated, live | https://www.fidelitycharitable.org/nonprofits/faqs.html |
| S3 | Fidelity lost-check FAQ | sponsor [F] | undated, live | https://www.fidelitycharitable.org/faqs/all/lost-grant-check.html |
| S4 | Fidelity Program Guidelines | sponsor [F] | 2026-09-11 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf |
| S5 | Fidelity Grant Delivery FAQs (404) | [R] | — | https://www.fidelitycharitable.org/help/grant-delivery-faq.html |
| S6 | Vanguard Policies and Guidelines | sponsor [F] | 2026-01-09 | https://www.vanguardcharitable.org/company-policies/policies-and-guidelines |
| S7 | NPT DAF guide | sponsor [F] | 2026-10-15 | https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf |
| S8 | NPT For Nonprofits | sponsor [F] | 2026-11-10 | https://www.nptrust.org/for-nonprofits/ |
| S9 | NPT PayPal $65m post | sponsor [F] | 2023 (mod. 2026-10-05) | https://www.nptrust.org/philanthropic-resources/philanthropist/nonprofits-receive-over-65-million-in-grants-from-npt-through-paypal-grant-payments/ |
| S10 | NPT FY25 consolidated financials | sponsor [F] | 2026-09-01 | https://www.nptrust.org/fy25-ar-consolidated-financials-npt/ |
| S11 | DAFgiving360 2024 Program Policies | sponsor [F] | 2024-12-12 | https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf |
| S12 | AEF Charities page | sponsor [F] | 2026-04-20 | https://www.aefonline.org/charities/ |
| S13 | Ren reissue article | vendor [V] | 2025-12-10 | https://intercom.help/rengiving/en/articles/13123383-what-should-i-do-if-i-have-issues-with-receiving-a-grant-check-or-need-to-request-a-reissue |
| S14 | MS GIFT How It Works | sponsor [F] | 2025-10-24 | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf |
| S15 | MS GIFT Grantmaking | sponsor [F] | 2024-10-01 | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf |
| S16 | BofA CGF Program Guidelines 2024 | sponsor [F] | 2024-09-18 | https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf |
| S17 | BofA CGF DFX donor guide | sponsor [F] | 2026-02-23 | https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf |
| S18 | PPGF Delivery Policy 2025 | platform [F] | 2025-01-01 | https://www.paypalobjects.com/marketing/web25/us/paypal-giving-fund/policy-updates/ppgf-us-delivery-01012025.pdf |
| S19 | PPGF Delivery Policy 2022 (superseded) | platform [F] | 2022-03-15 | https://www.paypalobjects.com/marketing/web25/us/paypal-giving-fund/policy-updates/ppgf-us-delivery-03152022.pdf |
| S20 | GiveClear (TIFIN Give) Granting FAQs | sponsor [F] | 2026-11-10 | https://intercom.help/give-ria/en/articles/10670838-granting-faqs |
| S21 | BlueGive Granting FAQs | sponsor [F] | 2026-11-10 | https://intercom.help/bluegive-help-center/en/articles/10597826-granting-faqs |
| S22 | CCT Donor Portal FAQ | CF [F] | 2025-12-02 | https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf |
| S23 | GKCCF online-giving tips | CF [F] | 2022-03-28 | https://growyourgiving.org/news/7-tips-for-maximizing-your-online-giving-experience |
| S24 | Columbus CSuite portal guide | CF [F] | 2025-04-22 | https://columbusfoundation.org/media/p1za1dz4/csuite-fund-portal-donor-resources-2025.pdf |
| S25 | Columbus grant-request guide | CF [F] | 2024-04-16 | https://columbusfoundation.org/media/j13d4kgk/csuite-portal-donor-resources-2024_guide-to-submitting-a-grant-request.pdf |
| S26 | Minneapolis DonorView cheat sheet | CF [F] | 2022-07-07 | https://www.minneapolisfoundation.org/wp-content/uploads/2023/11/DonorView-FAQs-Final.pdf |
| S27 | Tampa Bay portal guide | CF [F] | undated, live | https://www.cftampabay.org/portal-guide |
| S28 | SPMF DonorView grants guide | CF [F] | 2022-09-13 | https://de4vzavwp1bb7.cloudfront.net/general/Donors/Files/DonorView-Instructions/Viewing-and-Managing-Your-Grants.pdf |
| S29 | Omaha MyAccount | CF [F] | 2025-03-04 | https://omahafoundation.org/myaccount/ |
| S30 | OCCF Donor Portal FAQs | CF [F] | 2025-09-30 | https://www.oc-cf.org/donors/donor-portal-faqs/ |
| S31 | CFGA Fund Advisor Portal guide | CF [F] | 2025-03-25 | https://cfgreateratlanta.org/wp-content/uploads/2025/03/Fund-Advisor-Portal-Guide.pdf |
| S32 | Denver TDF Fund Manager | CF [F] | 2026-06-24 | https://denverfoundation.org/fundmanager/ |
| S33 | GHCF Access DonorSphere | CF [F] | 2026-09-03 | https://ghcf.org/access-donorsphere/ |
| S34 | Seattle IT upgrade FAQs | CF [F] | 2024-10-16 | https://www.seattlefoundation.org/it-system-upgrade-faqs/ |
| S35 | JaxCF grant-request guide | CF [F] | 2023-06-29 | https://www.jaxcf.org/wp-content/uploads/2023/07/Making-a-Grant-Request_updatedJUNE2023.pdf |
| S36 | Foundant Idea Lab: grant history export | vendor [V] | 2024-07-29 / 2024-08-27 | https://idealab.foundant.com/forums/597718-communitysuite-idea-lab/suggestions/48688049-export-grants-or-grant-history-new-portal |
| S37 | Ren RCF DFX donor guide | vendor [F] | 2021-10-21 | https://www.reninc.com/wp-content/uploads/2022/02/Donor-User-Guide-RCF-Rebranded-10-21-Updated-2-3.pdf |
| S38 | GivingPoint bundles (NPT, JPM, ICGF) and chunks | NPT/Ren code [F] | read 2026-11-15 | https://www.nptgivingpoint.org/main-OYPICD2D.js ; https://jpmgiving.org/main-JBUINBFD.js ; https://icgfdaf.org/main-2IGH5MJZ.js ; https://www.nptgivingpoint.org/chunk-GNPJY3AQ.js |
| S39 | EBCF new-portal notice | CF [F] | 2025-07-09 | https://www.ebcf.org/our-new-donor-portal-is-almost-ready/ |

Pages that blocked or failed:
- dafgiving360.org: 403
- paypal.com policy HTML: 403
- support.foundant.com: 403
- Ren's UBS and NWM guides: 404
- Napa Valley GOfund guide: 404
- Chariot check-issuance article: 404

---

## 7. Data dictionary

### `uncashed-grant-rules-2026.csv`

| Column | Meaning |
|---|---|
| `row_id` | U01–U19 |
| `sponsor_or_rail` | Sponsor, platform or payment rail |
| `ein` | EIN where the repo records one; blank for rails and platforms not in the repo |
| `segment` | national / bank/broker / rail / national (adviser platform) / national (charitable platform) |
| `source_document`, `source_date` | Document read and its date: the stated date, else the PDF creation or modification date, else "undated, live" |
| `topic` | What the row evidences |
| `rule_status` | published_rule / discretion_only / not_found / not_determinable / superseded / search_index_only |
| `void_window` | Days after issue before an uncashed check is voided, as stated |
| `funds_after_void` | Where funds go after a void (donor account, reassignment, not stated) |
| `reissue_rule` | Who can trigger a reissue, and on what conditions |
| `escheat_treatment` | Any unclaimed-property treatment stated |
| `electronic_expiry_rule` | Expiry of electronic (e.g. PayPal) payments, or check-delivery timing for unenrolled charities |
| `key_quote` | Verbatim, ≤40 words; segments joined by "…". Blank where the row records an absence or rests on [R] |
| `source_url`, `evidence_label`, `retrieved`, `notes` | As named; labels per the header |

### `donor-export-evidence-cf-2026.csv`

| Column | Meaning |
|---|---|
| `cf_rank_fy2024`, `foundation`, `ein`, `fy2024_daf_assets_usd`, `portal_vendor_repo` | Carried from `community-foundation-rails-portals-2026-v2.csv` |
| `export_status` | yes_grant_history / yes_fund_activity / yes_contributions_only / download_format_not_stated / not_mentioned_in_guide / not_documented / no_public_guide_found / not_reached |
| `export_format` | Format named (CSV, Excel, PDF, spreadsheet), "not stated", or n/a |
| `export_scope` | What the export covers |
| `key_quote` | Verbatim, ≤40 words, from `source_url` (blank for GWCF, which is carried from the repo) |
| `source_url`, `source_date`, `evidence_label` | As named |
| `platform_signal` | Vendor-level evidence that bears on the tenant (vendor statement, other tenants, code) |
| `retrieved`, `notes` | As named |

### `queue-proposals-batch33b.csv`

Standard proposal columns per `queue-proposals-README.md`.

---

## 8. Proposals

- **P-B33B-01:** is GivingPoint's coded Excel export (grant payments and activity) available to NPT-family donors? Use public tutorials only.
- **P-B33B-02:** read the 2026 DAFgiving360 Program Policies PDF from its public static host, for void, escheat, export and third-party clauses.
- **P-B33B-03:** do the 13 Foundant top-40 tenants expose the 2024 grant-history export?
