# Batch 31C: Ren for Charities coverage (P-CFR-04), a named RDE program (P-REN-05), NPact ownership after the move to Massachusetts (P-LSG-03), and the GL behind Foundation Cloud tenants (P-B30C-02)

**Date:** 2026-11-15. **Queue items:** P-CFR-04, P-REN-05, P-LSG-03, P-B30C-02 (`data/mission-2026-11-14/research-priority-queue.csv`).

**Status: public sources only.**
- I logged in nowhere, submitted no forms and contacted no one.
- I did not query tenant APIs. I read three kinds of thing:
  - public web pages and public static files: Ren's public front-end JavaScript bundle and NPact's WordPress media listing;
  - the Texas Comptroller open-data endpoint and the SEC EDGAR full-text search;
  - the IRS e-file index and the GivingTuesday 990 XML mirror.
- I did not fetch fcsuite.com.
- The Massachusetts, Delaware and OpenCorporates registries need forms or a CAPTCHA, so I did not query them.

**Excluded data:** NPact's public payments page shows bank-account and routing numbers, and its posted W-9s show the company's EIN. I read them but **do not reproduce them** here or in any data file.

**Recency rule:** every current-state claim rests on 2021+ evidence. Undated items are labelled as undated.

**Read first and built on:** the following files, each with its governing corrections:
- `queue-ren-iphi-attrition.md` (wave 11)
- `queue-ledger-segment-npact-owner.md` (wave 12; BroadWest "U" status, privacy-policy date)
- `queue-batch29-fit-ledgers.md` (wave 14)
- `queue-batch30-cf-coverage-give.md` (wave 15; CFES "NXT generation inferred")
- `spectrumportal-portal-vs-ledger-v2.csv`

**Evidence labels:**
- **[F]**: first-party (the sponsor's or vendor's own page, a posting it wrote, a government record or a filing).
- **[V]**: vendor statement.
- **[R]**: search-index capture of a page that is now gone or blocked.
- **[I]**: my inference.

**Outputs:**
- [`data/mission-2026-11-14/spectrumportal-portal-vs-ledger-v3.csv`](../../data/mission-2026-11-14/spectrumportal-portal-vs-ledger-v3.csv): 16 rows. These are the 14 v2 rows plus Greenville and Ventura, with a `change_note` on each row.
- [`data/mission-2026-11-14/relationship-graph-edges-additions-16.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-16.csv): EP001–EP011.
- [`data/mission-2026-11-14/queue-proposals-batch31c.csv`](../../data/mission-2026-11-14/queue-proposals-batch31c.csv): P-B31C-01 to P-B31C-03.

---

## 0. Answers

| Item | Answer | Confidence |
|---|---|---|
| **P-CFR-04** | **One enrolment covers the programs that pay through Ren's own rail, not every program Ren hosts.** Ren's public front-end code maps the payment codes `RDE_ACH` to "Ren for Charities ACH", `RDE_CHECK` to "Ren for Charities Check" and `RDE_MANUAL` to "Ren for Charities Manual". It keeps `LEGACY_ACH`, `LEGACY_CHECK` and `LEGACY_WIRE` separate, for grants paid by third-party systems and only displayed in the portal. Ren still names none of its "25+" programs. Programs tied to the rail: **AEF** [F]; **MS GIFT** [V, Ren FAQ plus MS brochure]; **RCF and its private-label programs** [I]. **Ren-owned iPhi CFs:** no public page shows Minneapolis, Cleveland, Greater Memphis or Louisville paying through Ren ACH. Louisville's latest public statement (2022) describes mailed checks | Medium on the mechanism; low on the program list |
| **P-REN-05** | **No new program is confirmed first-party.** The best new candidate is **MS GIFT**. Ren's Giving Season FAQ ("Current version updated 12/29", 2025 tax year) gives MS GIFT-specific steps and tells donors and advisors to have charities "Register for Ren for Charities" and "Enroll to receive grants via ACH". This is vendor-side evidence only. **New finding:** "Ren for Charities ACH" *is* the RDE rail (code `RDE_ACH`), so any charity-side remittance labelled that way is RDE. Ren's metric conflict ($48K per second against 1.7M grants a year) is unchanged; the wave-11 per-minute reading stands | Low (MS GIFT); high (RDE = Ren for Charities ACH) |
| **P-LSG-03** | **Still no evidence of a sale or recapitalization.** The move to Massachusetts is now dated: NPact's own posted W-9s show "Fusion Laboratories LLC" (dba NPact) with a **Dallas, TX** PO address on a form last modified 2024-02-29, and **701 Edgewater Drive, Wakefield, MA 01880** on a form uploaded 2025-07-23. Both W-9s classify the LLC as **"P" (partnership)**, so it still has two or more members and has not become a single-member subsidiary of one corporate buyer. Since 2025–26 the terms are governed by Massachusetts law with Boston venue. The owner is unchanged from wave 12: "BroadWest Partners vehicle with search-fund investors (probably including Cambria); unconfirmed" | Medium (address timing, tax form); low (owner identity) |
| **P-B30C-02** | **Santa Barbara is closed as Blackbaud FE NXT (high), and San Diego rises to medium.** This removes the last row that left room for an NPact-hosted ledger. SBF's own Accounting Specialist posting says "Enter A/P invoices in FE NXT" and "Reconcile Gifts/Grants between FE, RE and FC databases monthly", where FC is NPact Foundation Cloud. Nevada moves from none to low (Blackbaud). Amarillo, Montana, Frederick, Door County, NW Minnesota, Initiative, Greenville and Ventura stay unknown | See §4 |

---

## 1. P-CFR-04: what one Ren for Charities ACH enrolment covers

### 1.1 Mechanism (new)

| Evidence | What it shows |
|---|---|
| Ren for Charities public front-end bundle [`app.js`](https://static.rengiving.com/static/frontend/js/app.js), loaded by [charities.rengiving.com](https://charities.rengiving.com/), read 2026-11-15 [F] | It contains a frozen enum: `LEGACY_ACH:"Legacy ACH", LEGACY_CHECK:"Legacy Check", LEGACY_WIRE:"Legacy Wire", RDE_ACH:"Ren for Charities ACH", RDE_CHECK:"Ren for Charities Check", RDE_MANUAL:"Ren for Charities Manual"`. Bank verification options are `PLAID` and `EARLY_WARNING`, with micro-deposit "amounts" or a "descriptor_code" |
| [Charity Grants](https://intercom.help/rengiving/en/articles/6232128-charity-grants) (2026-05-04) [V] | "Filterable Columns: Distribution, Foundation, Customer." "Ren for Charities now supports additional payment types from third parties, allowing your organization to view all grants from a Donor Advised program in one place. These payment types, called 'Legacy' … tracking information is not available for Legacy payments." |
| [Grant letters](https://intercom.help/rengiving/en/articles/9791242-how-to-view-and-download-charity-grant-letters) (2026-05-05) [V] | "Grants are processed through two different systems … For grants processed through an external system, letters cannot be downloaded from the portal." |
| [ACH setup](https://intercom.help/rengiving/en/articles/6232119-charity-ach-setup-step-by-step) (2026-10-30) [V] | "Once approved, all ACH grant payments from our DAF programs will be sent directly to your organization." |
| [Overview](https://intercom.help/rengiving/en/articles/6229556-ren-for-charities-overview) (2026-07-08) [V] | "enroll in ACH grants from 25+ donor-advised fund programs at once". No programs are named |
| [Reissue FAQ](https://intercom.help/rengiving/en/articles/13123383-what-should-i-do-if-i-have-issues-with-receiving-a-grant-check-or-need-to-request-a-reissue) (2025-12-10) [V] | "ACH reissuance is only possible if the donor allows payment flexibility." Donor preferences can therefore keep an enrolled charity on checks |

**Reading [I]:**
- The "Distribution" column is what separates the two kinds of grant. A grant labelled "Ren for Charities ACH/Check/Manual" was paid on Ren's RDE. A grant labelled "Legacy" was paid by the sponsor's or another system and is only *displayed* in the portal.
- One enrolment therefore reaches the RDE-paying programs. It does not reach every program whose grants appear in the report.
- The "Foundation" filter lists sponsors. Its values are visible only after login, so I did not read them.

### 1.2 Which programs

Ren-fronted programs are already in the repo: edges E011–E047 and EA023, plus `queue-vendor-scope-ren-denominator.md`. That gives 13+ DonorFirstX subdomains: `msgift`, `rcf`, `edwardjones`, `cfndaf`, `sei`, `rbcrcf`, `ampf`, `mdrt`, `ft`, `tda`, `firstcitizensdaf`, `semo`, `gccf`, `rcfgivingfund`, plus BofA, AEF and the NPT GivingPoint sites. Ren's help centre once had program-specific articles for Edward Jones CGF, Northwestern Mutual and the SEI Giving Fund. The SEI caption read "Sponsoring Charity: Renaissance Charitable Foundation". All three articles return 404 now [R].

| Program | Tie to Ren for Charities ACH | Status |
|---|---|---|
| American Endowment Foundation | "Powered by Ren, charities can claim their organization, provide ACH information" ([AEF charities](https://www.aefonline.org/charities/)) [F] | **Confirmed** (unchanged) |
| MS GIFT | Ren FAQ ([Giving Season FAQ](https://www.reninc.com/giving-season-2025-commonly-asked-questions/), "Current version updated 12/29") covers MS GIFT logins in FAQ 2–3. In FAQ 7, a general question, it tells donors to have charities "Register for Ren for Charities" and "Enroll to receive grants via ACH, which is the fastest delivery method". The MS brochure says "Rapid disbursement technology with ACH granting capabilities" ([PDF](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf)) [V] | **Probable** [V+I] (EP007) |
| RCF and its private-label programs (Edward Jones, SEI, Ameriprise, RBC, LPL/Commonwealth, MDRT, Fisher, NWM) | RCF: "delivered electronically or by check"; "Ren-powered technology" ([RCF FAQ](https://renaissancecharitable.org/faqs/)) [F]. Ren: "all ACH grant payments from our DAF programs" [V] | **Probable** [I] (EP008). No charity page names the rail |
| BofA Charitable Gift Fund | Ren hosts are present (EA023), but the charity guides describe checks (repo) | Not established |
| NPT GivingPoint programs (NPT, J.P. Morgan, ICGF) | Hosted by Ren. NPT's own charity rail is PayPal Grant Payments, with checks otherwise ([NPT](https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/), 2023) [F] | Not established; probably "Legacy" [I] → P-B31C-01 |
| Ren-owned iPhi CFs: Minneapolis, Cleveland, Greater Memphis, Louisville | No grantee-payment page mentioning ACH, Ren or Chariot was found for any of them. Louisville: "our goal is to have the check in the mail within 2-5 business days" ([CFL, 2022-06-12](https://www.cflouisville.org/improvement-to-grant-distributions-checks-now-mailed-twice-a-week/)) [F]. Its 2025 year-end guide ([PDF](https://www.cflouisville.org/wp-content/uploads/2025/10/2025-Year-End-Contributions-and-Grant-Distributions_Community-Foundation-of-Louisville-2.pdf)) does not say how grants are paid | **No public evidence**. iPhi is a separate stack from the RDE. SPMF (also on iPhi) uses Chariot |

**Count check [I]:** the RCF private-label programs (about 11), plus MS GIFT, AEF, RCF direct, BofA, the NPT/JPM/ICGF GivingPoint sites and the remaining DFX subdomains, can reach "25+". That holds only if the count includes programs Ren merely *displays* as Legacy. The claim is consistent with Ren's footprint, but it does not show that 25 programs pay over the RDE.

---

## 2. P-REN-05: a named RDE program beyond AEF

- **Search coverage.**
  - Ren's 90+ help-centre articles were read in full (2024–2026 release notes and charity FAQs). None names a sponsor other than RCF, and none names MS GIFT on the charity side.
  - Charity-side web search ("Ren for Charities", `rengiving.com`, grant letters with a QR code) found only Ren and AEF pages.
- **RDE = Ren for Charities.** The front-end enum (§1.1) settles naming. "Ren for Charities ACH" is `RDE_ACH`. The October 2024 release note's "ACH ID for RDE ACH" refers to the same rail. A program whose charity-facing materials say "Ren for Charities ACH" is therefore an RDE program.
- **MS GIFT is the strongest unconfirmed candidate (EP007).**
  - It is the only program named in Ren's year-end FAQ that also carries the ACH instruction.
  - Its brochure claims "rapid disbursement technology with ACH".
  - Upgrading it would take an MS GIFT charity-facing page or grant letter naming Ren for Charities.
- **Metrics.** No new Ren figure. The wave-11 correction stands: "$48K per second" against "$35B granted annually" (about $1.1K per second) is probably a per-minute figure mislabelled [I]. "1.7M grants a year" fits all Ren-administered programs, not RDE-ACH alone.

---

## 3. P-LSG-03: NPact ownership after the address change

| Signal | Evidence | Reading |
|---|---|---|
| **W-9, earlier** | NPact-hosted [NPact-W9.pdf](https://npact.com/wp-content/uploads/2025/01/NPact-W9.pdf). The media listing gives an upload date of 2025-01-09; the PDF was created 2023-06-07 and modified 2024-02-29; the form is rev. Oct 2018. Line 1 "Fusion Laboratories LLC"; line 2 "NPact"; LLC tax classification **P**; address: a Dallas, TX 75313 PO-box-style address on N Ervay St [F] | Texas address in force until at least 2024-02 |
| **W-9, later** | [NPact-2025-W9.pdf](https://npact.com/wp-content/uploads/2025/07/NPact-2025-W9.pdf), uploaded 2025-07-23 (scanned; read by OCR); form rev. Mar 2024. "Fusion Laboratories LLC" / "NPact"; LLC classification **P**; "701 Edgewater Drive, Wakefield, MA 01880" [F] | The move happened between 2024-02 and 2025-07, before the January 2026 privacy policy |
| Payments page | [npact.com/payments](https://npact.com/payments/) (modified 2025-08-04): payee "Fusion Laboratories LLC dba NPact" at a Rhode Island bank, and a Boston, MA lockbox for checks [F]. Account details are not reproduced | Banking and receivables are in New England by 2025-08 |
| Governing law | [Standard Terms](https://npact.com/software-as-a-service-license-and-services-standard-terms/) (modified 2026-01-08): "governed in all respects by the laws of the Commonwealth of Massachusetts"; venue in Boston; "Manufacturer is Fusion Laboratories LLC / dba NPact". [Terms of Use](https://npact.com/terms-of-use/) (modified 2025-08-05): Massachusetts law, but still "a Delaware corporation" [F] | Massachusetts is now the operating base. The "corporation" wording conflicts with the W-9s' LLC/partnership classification, so it is probably a drafting error [I] |
| Privacy Policy | [npact.com/privacy-policy](https://npact.com/privacy-policy/): "Fusion Laboratories, LLC dba NPact, 701 Edgewater Drive, Suite 130, Wakefield, MA 01880". The body says "Last updated: Updated August 19, 2026"; the header and footer say January 28/27, 2026. It names no parent; affiliates are defined generically [F] | Unchanged from wave 12 |
| Leadership | [npact.com/about](https://npact.com/about/) (modified 2026-11-13): Burt Hurlock, CEO. Conn and Greeley are not listed. New products: "NPact Core Connect" and "NPact Payments" [F]. CB Insights still shows Jeff Conn as CEO [R, stale] | The CEO change stands. Hurlock's earlier roles (Azima DLI; Humanyze) are Massachusetts-area companies per unverified profiles, which fits a move to the CEO's base [I] |
| Texas | data.texas.gov (dataset 9cir-efmm), queried 2026-11-15: BROADWEST PARTNERS LLC, taxpayer 32086573816, 5580 Peterson Ln Ste 200, Dallas, now **record_type_code `X`** with right_to_transact `U` (wave 12 recorded `U`). No "Fusion Lab(oratorie)s" or "NPact" taxpayer appears in the file [F] | The record looks dormant. Fusion Laboratories LLC has no Texas franchise-tax record in this file |
| SEC / press | EDGAR full text 2021–2026: "Fusion Laboratories" appears only in Blackbaud's 10-Q and 10-Ks about the 2022 FIMS/DonorCentral sale ($6.4m). There is no Form D. No sale, financing or recap press was found [F] | No change of control is visible |
| Not reached | Massachusetts Corporations Division, Delaware ICIS and OpenCorporates (form, CAPTCHA or bot wall); LinkedIn (login wall) | These remain for a human read |

**Conclusion [I]:**
- The legal entity is unchanged: the same Fusion Laboratories LLC, taxed as a partnership both before and after the move.
- The company relocated its legal, billing and governing-law base from Dallas to the Boston area between 2024-02 and 2025-07, around the CEO transition.
- A 100% sale to a corporate buyer would normally make the LLC disregarded, so its W-9 would show the owner's classification. That did not happen.
- A sale to a multi-member group, or a partial recap, cannot be excluded.
- **Owner as recorded:** "BroadWest Partners vehicle with search-fund investors (probably including The Cambria Group); entity relocated to Wakefield, MA by 2025-07; no change of control evidenced; unconfirmed."

---

## 4. P-B30C-02: the GL behind Foundation Cloud tenants

Method:
- Job-board searches for each tenant against Financial Edge, Raiser's Edge, Blackbaud, FIMS, NPact, Intacct, NetSuite and QuickBooks.
- The newest e-filed 990 for each tenant, from the [IRS e-file index](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) (2025 and 2026 files) and the GivingTuesday XML mirror. Part VII-B and the free-text fields were parsed for software terms. Six tenants have a newly indexed FYE 2025-06 return: Nevada, Montana, NW Minnesota, San Diego, Frederick and Door County.
- Sponsor careers pages.

| Tenant (FY2024 DAF $m) | Batch-31 evidence | v2 → v3 |
|---|---|---|
| **Santa Barbara (152)** | SBF Accounting Specialist, posted 2025-11-06 ([nprnsb.org](https://nprnsb.org/jobs/accounting-specialist-3/)) and listed 2026-01-09 to 2026-07-08 ([career.com](https://www.career.com/job/santa-barbara-foundation/accounting-specialist/j202511071718559649946)): "Enter A/P invoices in FE NXT." "Update fee schedules and allocation pools related to Capital Preservation funds in FE." "Reconcile Gifts/Grants between FE, RE and FC databases monthly." "Blackbaud Raiser's Edge (RE), Financial Edge (FE) and NPact Foundation Cloud (FC) experience is a plus." [F via job boards; sbfoundation.org copy 404/403]. The TY2024 990 FUSION LABS INC "HOSTED INFRASTRUCTURE" $130,000 therefore pays for the FC layer. The TY2022–23 hosting payee was Centered Networks ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533149349305653_public.xml)) | NPACT (low) → **BLACKBAUD_FE, high** |
| **San Diego (708)** | "Seasonal Accounting Operations Assistant (Policy & Innovation Center)", employment 2026-06-15 to 2026-08-10: helps "test systems, including data transfer to Financial Edge" ([Workable, now 404](https://apply.workable.com/san-diego-foundation/jobs/view/127644E322.md)) [R]. This corroborates the undated Blackbaud case study [V]. The FYE 2025-06 990 VII-B shows no software payee (UNAMESA "INFORMATION TECHNOLOGY" $275k) | BLACKBAUD_FE low → **medium** |
| **Nevada (140)** | Accountant posting: "Proficiency in Blackbaud software: Beneficial." ([WayUp](https://www.wayup.com/i-j-Accountant-Full-Time-On-Nevada-Community-Foundation-184255630034082), undated, closed) [F]. FYE 2025-06 990: NOW CFO LAS VEGAS LLC "PROF SERVICES" $151,561 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610229349300311_public.xml)) [F] | unknown → **Blackbaud (product unstated), low** |
| Tulsa (694) | Re-read the [ffwd copy](https://jobs.ffwd.org/companies/idealist/jobs/66859314-accounting-clerk): "Experience with QuickBooks, Raiser's Edge, Financial Edge (preferred), Bill.com/DIVVY"; "Posted 6+ months ago". TCF Senior Accountant postings name no system. TY2024 990 shows no software payee | unchanged (low) |
| Kalamazoo (78) | No accounting posting names a GL. A database-manager posting asking for Raiser's Edge appears only in an [R] aggregator copy that I could not attribute | unchanged (low) |
| Amarillo (48) | A search-index capture of [AAF jobs](https://amarilloareafoundation.org/jobs/) listed a role responsible for data in "Raiser's Edge NXT" [R]. The live page now says "There are no open positions currently". RE NXT is a CRM, not a GL | unchanged (none); CRM noted |
| NW Minnesota (9) | The [Staff Accountant description (Jan 2025)](https://nwmf.org/wp-content/uploads/2025/01/Staff-Accountant-FKA-Accountant-Associate-1.2025.pdf) says the role will collaborate in "Software system selection, training, data corrections, NMF software implementation and web portal systems". The [Accounting Associate (June 2026)](https://nwmf.org/wp-content/uploads/2026/06/Accounting-Associate-FINAL-6.2026-2.pdf) names no product [F] | unchanged (none); system selection was under way in 2025 |
| Montana (47), Frederick (21), Door County (17), Initiative (6) | No posting naming a GL. FYE 2025-06 990s (Montana, Frederick, Door County) and the TY2024 990 (Initiative) show no software payee | unchanged (none) |
| **Greenville (67)**, **Ventura (40)** (new rows) | Greenville's TY2024 990 has no VII-B contractor over $100k. Ventura's TY2023–25 VII-B lists investment, Armanino audit/tax, legal, research and staffing payees. Ventura's Director of Accounting posting names no system in the captured text | added; unknown |

**v3 split (15 fund-portal rows, $2.46bn; New Mexico excluded as not a fund portal):**

| Class | Rows | $m | Share |
|---|---|---|---|
| Portal over Blackbaud FE (SBF high, CFES high, GWCF medium, SD medium) | 4 | 1,292 | 52.5% |
| Portal over Blackbaud, product inferred (Tulsa, Kalamazoo, Nevada; all low) | 3 | 911 | 37.0% |
| Portal, GL not evidenced | 8 | 256 | 10.4% |
| NPact-hosted ledger | **0** | 0 | 0% |

**Reading [I]:**
- Every Foundation Cloud tenant with any GL evidence (7 in this set, plus FFTC and CFGP from batch 29) points to Blackbaud.
- Santa Barbara was the only case behind the "NPact-hosted ledger" hypothesis. Its posting now lists FC as a *third* database beside FE and RE.
- Foundation Cloud should be treated as a grants/portal layer over Blackbaud FE in this segment. The remaining eight tenants are 10.4% of the group's assets.
- Separately, the harvest's Fusion/NPact payees are all services lines:
  - SBF hosting, $130k;
  - GKCCF "Advising", about $152k;
  - GNOF "Implementation", $118k;
  - VCF "Consulting", $148k;
  - AEF "Software development", $207k–$250k (TY2022–24).
- None is a ledger licence (P-B31C-03).

---

## 5. Corrections and notes for existing repo text (proposed, not governing)

1. **`spectrumportal-portal-vs-ledger-v2.csv` and `queue-batch30-cf-coverage-give.md` §2.**
   - Santa Barbara's "NPact-hosted (ledger possible)" is superseded by v3: Blackbaud FE NXT, high.
   - The §2 table row "NPact-hosted, ledger possible | 1 | 152 | 6.5%" becomes 0 rows.
2. **EJ005** (NPact → Santa Barbara, technology_provider). Keep the edge, but read it as Foundation Cloud hosting (EP002), not ledger hosting.
3. **`queue-ledger-segment-npact-owner.md` line 162 / wave-12 note.**
   - Add: "The Wakefield address already appears on a W-9 uploaded 2025-07-23. A W-9 uploaded 2025-01-09 (PDF modified 2024-02-29) shows Dallas. Both classify the LLC as a partnership (EP009)."
   - Also: the Texas BroadWest record's dataset code is now `X` (was `U`).
4. **`queue-ren-iphi-attrition.md` §6.**
   - Add: "'Ren for Charities ACH' is the RDE rail (front-end code `RDE_ACH`). 'Legacy' ACH, check and wire are third-party payments displayed in the portal (EP006)."
   - Also: the MS GIFT verdict "Probable" now also rests on Ren's Giving Season FAQ (EP007).

---

## 6. Limitations

- **Registries.** The Massachusetts, Delaware and OpenCorporates registries and LinkedIn were not read. The owner question still needs a human read (P-LSG-03 remains open).
- **San Diego.** The posting is read only through search-index captures (Workable 404; aggregators 410/503).
- **Santa Barbara.** The posting was read on two job boards, not on sbfoundation.org (404/403).
- **Undated items.** Nevada's and Tulsa's postings are undated, so both stay at low.
- **Ren "Foundation" filter.** Its values are behind login and were not read.
- **Ren help-centre program guides.** The Edward Jones, Northwestern Mutual and SEI guides are known only from search captions; all three return 404.
- **W-9 OCR.** The OCR of the July 2025 W-9 is clear for name, classification and address. The signature date is illegible; I rely on the upload date from the media listing.

---

## 7. Source register

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| S1 | Ren for Charities front-end bundle | vendor code [F] | live 2026-11-15 | https://static.rengiving.com/static/frontend/js/app.js |
| S2 | Ren help: Charity Grants; Grant letters; ACH setup; Overview; Reissue; Where is our grant | vendor [V] | 2026-05-04; 2026-05-05; 2026-10-30; 2026-07-08; 2025-12-10; 2024-10-08 | https://intercom.help/rengiving/en/articles/6232128-charity-grants ; https://intercom.help/rengiving/en/articles/9791242-how-to-view-and-download-charity-grant-letters ; https://intercom.help/rengiving/en/articles/6232119-charity-ach-setup-step-by-step ; https://intercom.help/rengiving/en/articles/6229556-ren-for-charities-overview ; https://intercom.help/rengiving/en/articles/13123383-what-should-i-do-if-i-have-issues-with-receiving-a-grant-check-or-need-to-request-a-reissue ; https://intercom.help/rengiving/en/articles/9970231-where-is-our-grant |
| S3 | Ren Giving Season FAQ | vendor [V] | "updated 12/29" (2025 tax year) | https://www.reninc.com/giving-season-2025-commonly-asked-questions/ |
| S4 | Ren help: Edward Jones, Northwestern Mutual and SEI program articles (now 404) | vendor [R] | captions only | https://intercom.help/rengiving/en/articles/10810347-edward-jones-charitable-gift-fund ; https://intercom.help/rengiving/en/articles/10810926-northwestern-mutual ; https://intercom.help/rengiving/en/articles/10811146-sei-giving-fund |
| S5 | AEF charities; RCF FAQ; MS GIFT brochure | sponsor [F]/[V] | 2026-04-20; 2026-01-21; undated | https://www.aefonline.org/charities/ ; https://renaissancecharitable.org/faqs/ ; https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf |
| S6 | Community Foundation of Louisville: check timing post; 2025 year-end guide | sponsor [F] | 2022-06-12; 2025-10 | https://www.cflouisville.org/improvement-to-grant-distributions-checks-now-mailed-twice-a-week/ ; https://www.cflouisville.org/wp-content/uploads/2025/10/2025-Year-End-Contributions-and-Grant-Distributions_Community-Foundation-of-Louisville-2.pdf |
| S7 | NPT PayPal Grant Payments | sponsor [F] | 2023 | https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/ |
| S8 | NPact W-9s (Jan 2025, Jul 2025) and WordPress media listing | vendor [F] | 2025-01-09; 2025-07-23 | https://npact.com/wp-content/uploads/2025/01/NPact-W9.pdf ; https://npact.com/wp-content/uploads/2025/07/NPact-2025-W9.pdf ; https://npact.com/wp-json/wp/v2/media?search=w9 |
| S9 | NPact Privacy Policy, Standard Terms, Terms of Use, About, Payments, NPact Payments | vendor [F] | 2026 (Jan/Aug); 2026-01-08; 2025-08-05; 2026-11-13; 2025-08-04; 2026-08-13 | https://npact.com/privacy-policy/ ; https://npact.com/software-as-a-service-license-and-services-standard-terms/ ; https://npact.com/terms-of-use/ ; https://npact.com/about/ ; https://npact.com/payments/ ; https://npact.com/software/npact-payments/ |
| S10 | Texas Comptroller Active Franchise Taxpayers | government open data [F] | queried 2026-11-15 | https://data.texas.gov/resource/9cir-efmm.json?taxpayer_number=32086573816 |
| S11 | SEC EDGAR full text ("Fusion Laboratories", "NPact"); Blackbaud 10-K FY2024 | SEC [F] | 2021–2026; 2025-02-21 | https://efts.sec.gov/LATEST/search-index?q=%22Fusion%20Laboratories%22 ; https://www.sec.gov/Archives/edgar/data/1280058/000128005825000010/blkb-20241231.htm |
| S12 | CB Insights; theorg (Hurlock) | aggregators [R] | live | https://www.cbinsights.com/company/npact/people ; https://theorg.com/org/npact/org-chart/burt-hurlock |
| S13 | SBF Accounting Specialist (two boards) | sponsor posting [F] | 2025-11-06; 2026-01-09 | https://nprnsb.org/jobs/accounting-specialist-3/ ; https://www.career.com/job/santa-barbara-foundation/accounting-specialist/j202511071718559649946 |
| S14 | SDF Seasonal Accounting Operations Assistant | sponsor posting [R] | 2026 summer | https://apply.workable.com/san-diego-foundation/jobs/view/127644E322.md |
| S15 | Nevada CF Accountant (WayUp); NCF careers | sponsor posting [F] | undated; live | https://www.wayup.com/i-j-Accountant-Full-Time-On-Nevada-Community-Foundation-184255630034082 ; https://www.nevadafund.org/careers |
| S16 | TCF Accounting Clerk (ffwd copy) | sponsor posting [F] | undated ("6+ months ago") | https://jobs.ffwd.org/companies/idealist/jobs/66859314-accounting-clerk |
| S17 | NWMF job descriptions | sponsor [F] | 2025-01; 2026-06 | https://nwmf.org/wp-content/uploads/2025/01/Staff-Accountant-FKA-Accountant-Associate-1.2025.pdf ; https://nwmf.org/wp-content/uploads/2026/06/Accounting-Associate-FINAL-6.2026-2.pdf |
| S18 | AAF jobs page | sponsor [F]/[R] | live / capture | https://amarilloareafoundation.org/jobs/ |
| S19 | IRS e-file index 2025–2026; GivingTuesday 990 XML (SBF TY2024, NCF FYE 2025-06, others) | filings [F] | 2025–2026 | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533149349305653_public.xml ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610229349300311_public.xml |
| S20 | Repo 990 VII-B harvest (Fusion/NPact payees) | repo [F] | TY2022–24 | data/mission-2026-11-14/form990-contractors-harvest-full.csv |

---

## 8. Data dictionary

### `spectrumportal-portal-vs-ledger-v3.csv` (16 rows)

The columns are the same as v2, plus `change_note`.

| Column | Meaning |
|---|---|
| `ein` | Sponsor EIN, 9 digits without a hyphen |
| `name` | Sponsor name as filed. The two new rows use names from the CF map |
| `fy2024_daf_assets_usd` | FY2024 DAF assets from the DAFRC-derived map |
| `portal_url` | The Foundation Cloud (spectrumportal.net) URL that the sponsor links |
| `split_class` | One of: `portal over Blackbaud FE` (FE named, NXT stated or inferred); `portal over Blackbaud (product inferred)`; `portal; GL not evidenced`; `not a fund portal (partner/grantee portal)` |
| `ledger_reading` | `BLACKBAUD_FE`; `BLACKBAUD (…)` with a qualifier; or `unknown` / `not evidenced` |
| `confidence` | `high` (sponsor's own dated text names the GL); `medium` (dated [R] text or a strong inference); `low` (undated or indirect); `none` |
| `basis` | Quoted evidence with its source and date |
| `ledger_families_v1` | The original v1 family label, kept for traceability |
| `retrieved` | Date the row was last checked (2026-11-15) |
| `change_note` | What changed in v3 and why. "unchanged" when nothing changed |

### `relationship-graph-edges-additions-16.csv` (EP001–EP011)

- **Columns:** the same as `relationship-graph-edges.csv`.
- **Status values:**
  - `confirmed`: first-party text or a filing.
  - `inferred`: [R], vendor-only, or undated evidence.
- **Relationship types introduced:**
  - `general_ledger`
  - `portal_provider`
  - `outsourced_accounting`
  - `operates`
  - `payment_channel`
  - `legal_form`: a self-loop recording entity facts.
  - `governing_law`

### `queue-proposals-batch31c.csv`

- **Format:** per `queue-proposals-README.md`. `state` = `open`.
- **P-B31C-01:** which rail the NPT GivingPoint programs pay on.
- **P-B31C-02:** the remaining 8 Foundation Cloud GLs, from audits.
- **P-B31C-03:** NPact as a hosting and services provider.
