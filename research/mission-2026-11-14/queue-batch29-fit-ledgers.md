# Batch 29A: NPact FIT ledgers (P-B28-01), GKCCF back-office clients (P-LDG-02), NYCT ERP (P-LSG-02), Foundation Cloud + FE NXT + REPAY stacks (P-CFR-03)

**Date:** 2026-11-15. **Author:** batch-29A queue agent.
**Queue items:** P-B28-01, P-LDG-02, P-LSG-02 and P-CFR-03 (`data/mission-2026-11-14/research-priority-queue.csv`).

**Status:** public sources only. I did not log in, submit forms or contact anyone. Reads were limited to:
- public web pages and PDFs;
- public DNS (dns.google);
- IRS e-file XML from the public `gt990datalake-rawdata` bucket, paced at about one request per second.

One action was refused by the session's permission layer and was not worked around: querying the donor-portal.org per-tenant `brand` API to discover tenants (§2.4). Where a page returned 403 or 404, the claim is marked [S] (search-engine extract) or [R] (repo capture), as in earlier batches.

**Recency rule:** every current-state claim rests on 2021+ evidence. No pre-2021 source is used.

**Built on (with their governing corrections):**
- `queue-batch28-ledgers-voids-cf-apps.md`, including the wave-13 corrections. NPact is "the trade name of Fusion Laboratories LLC". Pittsburgh's core ERP is "NetSuite, Salesforce and a cloud-based data warehouse".
- `queue-ledger-segment-npact-owner.md`, including the wave-12 corrections:
  - NYCT is **low-medium**, and its "migration in progress" rests on [R].
  - CCF's posting is dated 2026-06-08, and it lists Financial Edge as "preferred" only.
- `queue-ledgers-behind-portals.md`, including the wave-10 corrections. GKCCF's audit books "income from services, which covers back-office accounting services for other nonprofits and administrative fees on pool investments by other entities".
- `data/mission-2026-11-14/cf-ledger-families-2026.csv` and `cf-vendor-map-by-ein.csv`.

**Labels:**
- [F] first-party text or a filed government record
- [V] vendor statement or case study
- [H] HTTP or DNS observation
- [S] search-engine extract (page not opened)
- [R] repo capture of a page that now refuses reads
- [I] inference

**Outputs:**
- `data/mission-2026-11-14/cf-ledger-families-2026-v2.csv`: 7 rows. 6 are updated v1 rows and 1 is new. The v1 columns are kept and a `change_note` column is added.
- `data/mission-2026-11-14/relationship-graph-edges-additions-14.csv`: EN001–EN014.
- `data/mission-2026-11-14/queue-proposals-batch29a.csv`: P-B29A-01 to P-B29A-03.

---

## 0. Headline answers

| ID | Answer | Confidence |
|---|---|---|
| **P-B28-01** | **SVCF is the only NetSuite + FIT sponsor in public view. Every other named FIT user runs on Blackbaud Financial Edge NXT.** NPact names 6 FIT customer stories: SVCF on NetSuite; Broward College Foundation, Valdosta State University Foundation and the Catholic Foundation of Greater Philadelphia (CFGP) on FE NXT; Winthrop University Foundation with its GL unnamed; and FFTC, where FIT is a page tag only, on an FE NXT GL. Among DAF sponsors in DAFRC, FIT users with stated evidence are **SVCF ($9.58bn)** and **CFGP ($0.02bn)**; **FFTC ($2.95bn)** is a tag-only candidate. **Recommendation: do not add a "NetSuite + NPact FIT" family (n = 1).** Keep SVCF in SF_NETSUITE, record FIT in `product`, and treat FIT as a fund-accounting overlay on the GL, not a ledger family. NPact's DAF-asset footprint is understated either way: FIT at SVCF, Foundation Cloud at FFTC, and the AEF NPact "SOFTWARE DEVELOPMENT" lines ($207k / $217k / $250k, TY2022–24) are all outside the repo's NPact/FIMS total of $2.7bn | High on what the stories say; medium on completeness, since NPact lists only the customers that agree to a story |
| **P-LDG-02** | **No back-office client is named in any public filing. One former or current client is confirmed by its tenant (Indian River CF), and IRCF now appears to have moved to Foundant.** The 2024 consolidated audit (dated 2025-11-12) confirms the business: revenue "from contracts with customers (e.g., other non-profit organizations) ... for providing back-office accounting services", billed as a flat monthly fee. Income from services was **$1,806,759 (2024)** and **$1,915,649 (2023)**, a line that also includes pool administrative fees [F]. The GKCCF-only 990 shows a larger "SERVICE INCOME" line: **$5,562,451 (TY2023)** and **$6,127,929 (TY2024)** [F]. Schedule R lists 21 related supporting organisations, none of them back-office clients. Known donor-portal.org tenants: `gkccf`, `gh` (Greater Horizons, new in this batch) and `ircf`. IRCF's "My Fund has been Upgraded!" page now sends fundholders to `indianriver.fcsuite.com` (Foundant) [F] | Medium (business model); low (client list) |
| **P-LSG-02** | **No public source names NYCT's legacy ERP, implementer or go-live dates.** The only primary text that could be read is still the JobTarget posting of 2026-08-01, which lists Sage Intacct and Salesforce as "preferred" skills. The "3–5-year transition from a legacy ERP to Salesforce + Sage Intacct" (start "Fall 2025") is [S]/[R] only: every copy now returns 403 or 404. The TY2025 990 is not yet in the IRS index (index files of 2026-11-14). TY2022–24 Part VII-B lists only investment managers and trustees. NYCT stays **low** in v2, following the wave-12 correction. **CCF:** no new source. Financial Edge remains a "preferred" skill in the 2026-06-08 posting; no replacement project was found | Low |
| **P-CFR-03** | **3 sponsors, holding $3.37bn of DAF assets, run NPact Foundation Cloud with Blackbaud FE NXT as the GL: FFTC ($2.95bn, medium), GWCF ($0.40bn, medium, FE NXT inferred) and CFGP ($0.02bn, high). Only GWCF names REPAY.** "Blackbaud REPAY" is FE NXT's embedded payments product: REPAY was "the exclusive embedded vendor payment solution for Blackbaud Financial Edge NXT" from 2023-11-15 [V]. So GWCF's REPAY grant payments are themselves an FE NXT signal [I]. Blackbaud announced BILL as the new Payment Assistant partner on **2026-09-29**, and its help pages tell REPAY users to "switch from REPAY to BILL" [V]. GWCF went live on REPAY in the same month. **San Diego and Tulsa:** no REPAY, Payment Assistant or BILL text on their homepages, and no Blackbaud or NPact line of $100k or more in TY2021–24 Part VII-B. Not established | Medium |

---

## 1. P-B28-01: who else runs NPact FIT

### 1.1 NPact's own FIT customer list [V]

The FIT product page ([npact.com/software/fund-investment-tool-fit/](https://npact.com/software/fund-investment-tool-fit/)) says:
- "Seamlessly connect FIT with Oracle NetSuite to automate journal entries".
- "FIT integrates directly with Blackbaud Financial Edge NXT ®".
- It lists four stories: SVCF, FFTC, Broward College Foundation and CFGP.

The NPact knowledge base adds Foundation Cloud to the integrations: "can be integrated with NPact's Foundation Cloud solution for Grant Management, with Blackbaud's FE NXT solution for Finance and with Oracle NetSuite for Finance" ([KB, updated 2025-11-24](https://npact.document360.io/docs/about-fund-investment-tool)) [V]. G2 lists the same product under an earlier name, "Endowment Manager", with "real-time, two-way integration with Blackbaud Financial Edge NXT" ([G2](https://www.g2.com/products/endowment-manager/discuss)) [S].

I read all 24 stories in the [customer-stories index](https://npact.com/customer-stories/) (pages 1–2). The FIT stories are:

| Organisation | Story date | GL named | FIT evidence | DAF sponsor in DAFRC? |
|---|---|---|---|---|
| Silicon Valley Community Foundation | 2025-04-29 (mod. 2026-10-20) | **NetSuite** | Co-developed FIT; FIT layered on NetSuite instead of a custom app ([story](https://npact.com/customer-stories/silicon-valley-community-foundation/)) | Yes, $9.58bn |
| Foundation For The Carolinas | 2025-03-07 (mod. 2026-01-28) | **FE NXT** (from FE 7) | Keyword tag "Fund Investment Tool (FIT)" only; the body describes Foundation Cloud Grants, FCCP, RE NXT and FE NXT ([story](https://npact.com/customer-stories/foundation-for-the-carolinas/)) | Yes, $2.95bn |
| Catholic Foundation of Greater Philadelphia | 2026-01-27 | **FE NXT** | FIT "creates journal entries that then go to FE NXT"; weekly rebalancing, gain/loss allocation, annual fund service fee ([story](https://npact.com/customer-stories/the-catholic-foundation-of-greater-philadelphia/)) | Yes, $22.4m (faith-based) |
| Broward College Foundation | 2025-12-12 | **FE NXT** | Replaced FE NXT's Allocation Management module for 700+ funds ([story](https://npact.com/customer-stories/broward-college-foundation/)) | Not found |
| Valdosta State University Foundation | 2026-08-21 | **FE NXT** | "FIT, which integrates with Financial Edge NXT"; implemented in under eight weeks ([story](https://npact.com/customer-stories/valdosta-state-university-foundation/)) | Not found |
| Winthrop University Foundation | 2026-09-15 | not named | FIT "creates detailed journal entries directly in the general ledger"; 1,000+ funds, team of four ([story](https://npact.com/customer-stories/winthrop-university-foundation/)) | Not found |

The other 18 stories are Blackbaud RE NXT and FE NXT consulting jobs (schools, a tribe, food banks, a diocese), plus Saint Mary's Hall, which moved to **Sage Intacct**. None of them uses FIT or NetSuite.

Other routes:
- **Blackbaud.** Blackbaud hosts an on-demand session, "Automate Advanced Investment Calculations with Blackbaud and NPact" (21 min, undated, no customers named) ([Blackbaud](https://www.blackbaud.com/events/all-events/automate-advanced-investment-calculations-with-blackbaud-and-npact)).
- **Oracle NetSuite.** No Oracle NetSuite or NetSuite.org page found pairs NetSuite with NPact.
- **Job postings.** Searches returned only NPact's own FE NXT consultant listings ([NPact ApplyToJob](https://npact.applytojob.com/apply/TAyc2aBYYM/Blackbaud-Financial-Edge-NXT-Consultant)). No sponsor posting names FIT.

### 1.2 990 Part VII-B payments to NPact (full harvest, 5,074 lines)

The only NPact or Fusion lines of $100k or more are:
- GKCCF "Advising": $151,954 and $152,246.
- Vermont CF "CONSULTING": $148,000.
- GNOF "IMPLEMENTATION SERVICES": $118,434.
- Santa Barbara "HOSTED INFRASTRUCTURE": $130,000.
- **AEF "NPACT ... SOFTWARE DEVELOPMENT": $206,682 (TY2022), $217,016 (TY2023) and $249,500 (TY2024)** ([TY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml)) [F].

AEF ($9.48bn) still runs DonorCentral (repo V9-05). Its NPact payments are consistent with FIMS/DonorCentral, and do not show FIT [I]. SVCF, FFTC and CFGP show no NPact line of $100k or more. FIT subscriptions are probably below the threshold, so 990s cannot size FIT [I].

### 1.3 Taxonomy recommendation

- **No new family.** Keep `SF_NETSUITE` for SVCF and set `product` = "NetSuite GL + NPact FIT ... + Salesforce portal".
- **Raise SVCF to medium.** The vendor story quotes the SVP Finance, which replaces the earlier [R]-only postings.
- **Treat FIT as an overlay.** FIT is a sub-ledger and calculation layer that posts journal entries to whichever GL sits beneath it. A future `fund_accounting_overlay` column (FIT / Fund 360 / none) would capture it without splitting families.
- **NPact's footprint by DAF assets.** It now spans:
  - FIMS/DonorCentral rows;
  - the Foundation Cloud portal rows;
  - FIT at SVCF ($9.58bn) and CFGP;
  - Foundation Cloud grants and portal at FFTC ($2.95bn).

  These layers sit on other vendors' GLs, so they should not be summed into "NPact ledger" assets.

---

## 2. P-LDG-02: GKCCF / Greater Horizons back-office clients

### 2.1 Audited statements [F]

The 2024 consolidated audit ([PDF](https://growyourgiving.org/wp-content/uploads/2025/11/Audit-Report-2024.pdf); the same file is on greaterhorizons.org; the auditor's report is dated 2025-11-12) says:
- "Revenue from contracts with customers (e.g., other non-profit organizations) is reported at the amount that reflects the consideration to which the Foundations expect to be entitled to in exchange for providing back-office accounting services."
- "Contracts for back-office accounting services are generally considered a single performance obligation and generally are a flat contract fee that is billed monthly."
- One of the factors it lists as affecting revenue is the "Organization size of back-office accounting customers".
- "The Foundations recognized revenue of $1,806,759 and $1,915,649" (2024, 2023). This line also includes pool administrative fees, and no customer is named.

The 2023 audit ([PDF](https://growyourgiving.org/wp-content/uploads/2024/12/Audit-Report-2023.pdf)) gives $1,915,649 (2023) and $3,035,924 (2022). The **2024 total, down from $3.04m (2022)**, is consistent with clients leaving [I].

### 2.2 990 filings [F]

- **GKCCF TY2024** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189349314033_public.xml)):
  - Part VIII "SERVICE INCOME" $6,127,929. TY2023 was $5,562,451 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433199349316533_public.xml)).
  - The gap to the consolidated $1.8m suggests fees charged to Greater Horizons and supporting organisations, which are eliminated on consolidation [I].
  - Schedule R lists 21 related exempt organisations at 1055 Broadway (Greater Horizons, Greater Horizons Foundation and Trust, family foundations, the KC Public Library Foundation and the KC Symphony Foundation). They are supporting organisations, not unrelated clients.
  - Schedule O has no client list.
- **Greater Horizons TY2024** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513189349309621_public.xml)) describes itself as "POWERED BY THE GREATER KANSAS CITY COMMUNITY FOUNDATION". It reports no program-service revenue line and names no clients.
- **Indian River CF FYE 2025-06** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610579349300416_public.xml)) and **FYE 2024-06** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202500629349301700_public.xml)):
  - No Part VII-B contractors.
  - Other expenses include "CONTRACT SERVICE FEE" $127,814 (FY2024), which becomes "ADVISORY EXPENSE" $127,489 (FY2025).
  - Information technology spend was $175 (FY2024).
  - The near-zero IT spend fits an outsourced platform [I]. No payee is named.

### 2.3 Tenants and sites

| Tenant | Owner | Evidence |
|---|---|---|
| `gkccf.donor-portal.org` | GKCCF | Repo (wave 10) |
| `gh.donor-portal.org` | Greater Horizons | [Access Your Fund Online](https://www.greaterhorizons.org/access-fund-online/): "https://gh.donor-portal.org/login", support@greaterhorizons.org [F] |
| `ircf.donor-portal.org` | Indian River CF | IRCF homepage menu "My Fund: Login" [F]. The [upgrade page](https://ircommunityfoundation.org/my-fund-has-been-upgraded/) says "With a new and improved My Fund, you can process grant recommendations online" and its "Go to My Fund" button goes to `https://indianriver.fcsuite.com/erp/portal` [F] |

**Reading [I].** IRCF has moved, or is moving, from the GKCCF back office to Foundant CommunitySuite. No date is given. In v2, IRCF moves from UNRESOLVED to FOUNDANT at low confidence.

I checked Topeka CF, CF of South Puget Sound and CF Monterey County, the only CF pages returned for a "donor-portal.org" search. All three link Foundant (`fcsuite.com`) or no portal, so none is a GKCCF tenant.

A search extract attributed to GKCCF's annual report mentions "assets returned to community foundations that previously utilized its accounting services" [S]. The live annual report (as of 2025-12-31) does not contain that text, so I do not use it.

### 2.4 Limits

- **Wildcard hosting.** donor-portal.org serves every subdomain with the same shell and `env.js`, so a host that answers does not prove a tenant.
- **Brand API not queried.** The bundle resolves tenants through `brand/{host}/` on the API and redirects unknown brands to donor-portal.org. Querying that endpoint for guessed names was refused by the session's permission layer, and I did not attempt it another way.
- **Remaining routes to the tenant list:**
  - sponsor websites that link `*.donor-portal.org`;
  - client CF audits naming GKCCF as service provider;
  - a GKCCF disclosure.

---

## 3. P-LSG-02: NYCT's ERP move, and CCF

| Item | Finding | Label |
|---|---|---|
| Legacy ERP name | Not found in any public source | n/a |
| Target platform | "transitioning from a legacy Enterprise Resource Planning ('ERP') system to a modern, integrated platform built on Salesforce and Sage Intacct"; "three- to five-year digital transformation initiative"; start "Fall 2025". Seen only in search extracts of the Project Director posting. [PNY](https://philanthropynewyork.org/node/42089) returns 403, and the idealist, findroles and gih copies return 404 or 403 (2026-11-15) | [S]/[R] |
| Primary text | [JobTarget, datePosted 2026-08-01](https://www.jobtarget.com/jobs/jt-ytfwftg0iq/director-investment-operations-and-treasury-new-york-city-new-york): "Experience with Sage Intacct, Salesforce, or similar investment/portfolio systems preferred". The [Paylocity copy](https://recruiting.paylocity.com/Recruiting/Jobs/Details/4366948) now reads "job does not exist or is not currently active" | [F] (repo) |
| Implementer | None named. General web searches, whose results included Armanino, Sage and top10erp case studies, turned up no NYCT story. Partner libraries were not browsed one by one | n/a |
| 990 | The TY2025 return is not in the IRS index (index files of 2026-11-14; the TY2024 return is 202523149349305672). TY2022–24 Part VII-B lists only investment managers and trustees | [F] |
| Go-live | Not stated | n/a |

**CCF ($1.09bn).** The 2026-06-08 Gift and Fund Financial Services Officer posting lists Financial Edge as preferred ([career.com](https://www.career.com/job/california-community-foundation/gift-and-fund-financial-services-officer/j202606080846182943693)). A DSG CFO search page appeared in results but now returns 404. No source names a replacement GL, so the v1 row (BLACKBAUD_FE, medium) is left unchanged and is not in v2.

---

## 4. P-CFR-03: NPact Foundation Cloud + Blackbaud FE NXT (+ REPAY)

### 4.1 Sponsors with the combination

| Sponsor | DAF assets (FY2024) | Foundation Cloud evidence | FE NXT evidence | REPAY | Confidence |
|---|---|---|---|---|---|
| FFTC | $2.95bn | NPact story: FCG and FCCP [V]; `fftc.spectrumportal.net` serves "Foundation Cloud Community Portal" with an explicit DNS record (52.154.137.83). `spectrumportal.net` has no wildcard: a random label returns NXDOMAIN, and the SOA is `fusdns03.fusionlabs.net` [H] | NPact story: moved from FE 7 to FE NXT [V] | Not found | Medium |
| GWCF | $0.40bn | [Portal news](https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived) (Sep 21): "Foundation Cloud Community Portal ... replaces Donor Central"; "ported over seven years of fund history" [F] | Inferred from Blackbaud REPAY, plus 990 BLACKBAUD "TECHNOLOGY" $177,444 (TY2022) and $151,433 (TY2024) [F]. 2025 postings named "FIMS/Raiser's Edge" [S] | [Nonprofit FAQ](https://www.thecommunityfoundation.org/nonprofit-faqs): "As part of our systems transformation upgrades completed in September 2026, the Greater Washington Community Foundation has partnered with Blackbaud and REPAY"; "ACH is the default method"; check if the form is not returned [F] | Medium |
| CFGP | $0.02bn | NPact story: FCG and FCCP [V] | Same story: "Blackbaud Financial Edge NXT and Raiser's Edge NXT" [V] | Not found | High |

**Total: $3.37bn.** The queue text said GWCF names FE NXT on its own pages. I did not find FE NXT on the GWCF pages I read, so that attribution is downgraded to [I].

### 4.2 What REPAY is here

- **REPAY's release, "REPAY Powers Digital Payment Assistant For Blackbaud Clients" (Nov. 15, 2023):** "REPAY is the exclusive embedded vendor payment solution for Blackbaud Financial Edge NXT®"; "Capabilities include virtual cards and ACH" ([REPAY](https://repay.com/repay-powers-digital-payment-assistant-for-blackbaud-clients/)) [V].
- **BILL's release (September 29, 2026):** "Payment Assistant™, powered by BILL, the new experience for Blackbaud Financial Edge NXT® customers"; "phased rollout, beginning with an early adopter program"; "Initial availability will support domestic vendor payments only" ([BILL](https://www.bill.com/press-release/bill-and-blackbaud-partner-to-simplify-vendor-payments)) [V].
- **Blackbaud FE help:** "If your organization currently processes Payment Assistant payments through REPAY, switch from REPAY to BILL". It also gives REPAY's ACH ID for bank allow-lists ([help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/fe/content/fe-payment-assistant-onboarding.html)) [V].

**Reading [I].** "Blackbaud REPAY" for grants is the FE NXT accounts-payable rail applied to grant disbursement. It belongs in the provider map as an **AP-embedded grant rail**, and its successor is BILL. GWCF launched on a rail that Blackbaud is already replacing.

### 4.3 San Diego and Tulsa

- **Pages.** Neither homepage contains "REPAY". Tulsa links `tcf.spectrumportal.net/accounts/signin`. The San Diego homepage returned a 4.5 KB shell. Grantee FAQ pages were not found.
- **990s.** Part VII-B for TY2021–24 has no Blackbaud, NPact or REPAY lines. San Diego shows UNAMESA (IT) and KPMG; Tulsa shows TriWest and BOK ([form990-contractors-harvest-full.csv](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv)). I also read San Diego's FYE 2025-06 return ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601339349305635_public.xml)), which adds nothing.
- **Status.** Both rows stay NPACT (implied) and are not in v2. P-B29A-02 asks for the portal-versus-ledger split.

---

## 5. Corrections to existing repo text (proposed)

1. **`cf-ledger-families-2026.csv`, FFTC.**
   - Before: UNRESOLVED (Give Interactive / Northeast Retirement Services).
   - After: **BLACKBAUD_FE + NPact Foundation Cloud, medium**.
   - Give Interactive is the portal (`daf.fftc.org`, "Powered by GiftingNetwork"), not the GL.
2. **`cf-ledger-families-2026.csv`, GWCF.** NPACT (implied) becomes **BLACKBAUD_FE (inferred via REPAY) with an NPact portal, medium**.
3. **`cf-ledger-families-2026.csv`, SVCF.** Confidence moves from low to medium, and the product adds FIT. The batch-28 headline already reflects this.
4. **`cf-ledger-families-2026.csv`, NYCT.** Confidence moves from medium to low, applying the wave-12 correction that had not reached v1.
5. **`spectrumportal.net` hosting.** It is not wildcard-hosted (NXDOMAIN for random labels). Unlike donorcentral.com and donor-portal.org, a resolving `<x>.spectrumportal.net` host is evidence of a tenant.
6. **The queue text for P-CFR-03.** It says GWCF names Financial Edge NXT on its own pages. Not confirmed in the pages read, so mark it [I].

---

## 6. Source register

| # | Source | Type | Date | URL |
|---|---|---|---|---|
| S1 | NPact FIT product page | vendor [V] | live 2026-11-15 | https://npact.com/software/fund-investment-tool-fit/ |
| S2 | NPact KB "about fund investment tool" | vendor [V] | 2025-11-24 | https://npact.document360.io/docs/about-fund-investment-tool |
| S3 | NPact story: SVCF | vendor [V] | 2025-04-29 | https://npact.com/customer-stories/silicon-valley-community-foundation/ |
| S4 | NPact story: FFTC | vendor [V] | 2025-03-07 | https://npact.com/customer-stories/foundation-for-the-carolinas/ |
| S5 | NPact story: CFGP | vendor [V] | 2026-01-27 | https://npact.com/customer-stories/the-catholic-foundation-of-greater-philadelphia/ |
| S6 | NPact story: Broward College Foundation | vendor [V] | 2025-12-12 | https://npact.com/customer-stories/broward-college-foundation/ |
| S7 | NPact story: Valdosta State Univ. Foundation | vendor [V] | 2026-08-21 | https://npact.com/customer-stories/valdosta-state-university-foundation/ |
| S8 | NPact story: Winthrop Univ. Foundation | vendor [V] | 2026-09-15 | https://npact.com/customer-stories/winthrop-university-foundation/ |
| S9 | NPact customer-stories index, pages 1–2 | vendor [V] | live | https://npact.com/customer-stories/ ; https://npact.com/customer-stories/page/2/ |
| S10 | Blackbaud on-demand session with NPact | vendor [V] | undated | https://www.blackbaud.com/events/all-events/automate-advanced-investment-calculations-with-blackbaud-and-npact |
| S11 | AEF TY2024 990 (NPact line) | 990 [F] | TY2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml |
| S12 | GKCCF 2024 consolidated audit | audit [F] | 2025-11-12 | https://growyourgiving.org/wp-content/uploads/2025/11/Audit-Report-2024.pdf |
| S13 | GKCCF 2023 consolidated audit | audit [F] | 2024-11-07 (signing date per search extract [S]) | https://growyourgiving.org/wp-content/uploads/2024/12/Audit-Report-2023.pdf |
| S14 | GKCCF TY2024 and TY2023 990 | 990 [F] | TY2023–24 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189349314033_public.xml ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433199349316533_public.xml |
| S15 | Greater Horizons TY2024 990 | 990 [F] | TY2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513189349309621_public.xml |
| S16 | Greater Horizons "Access Your Fund Online" | sponsor [F] | live 2026 | https://www.greaterhorizons.org/access-fund-online/ |
| S17 | IRCF "My Fund has been Upgraded!" and homepage | sponsor [F] | live 2026-11-15 | https://ircommunityfoundation.org/my-fund-has-been-upgraded/ ; https://www.ircommunityfoundation.org/ |
| S18 | IRCF FYE 2025-06 and 2024-06 990s | 990 [F] | FY2024–25 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610579349300416_public.xml ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202500629349301700_public.xml |
| S19 | NYCT Director, Investment Ops & Treasury | posting [F] | 2026-08-01 | https://www.jobtarget.com/jobs/jt-ytfwftg0iq/director-investment-operations-and-treasury-new-york-city-new-york |
| S20 | NYCT Project Director, Digital Innovation | posting [S]/[R] | 2025 | https://philanthropynewyork.org/node/42089 |
| S21 | CCF Gift and Fund Financial Services Officer | posting [F] (repo) | 2026-06-08 | https://www.career.com/job/california-community-foundation/gift-and-fund-financial-services-officer/j202606080846182943693 |
| S22 | GWCF nonprofit FAQ (REPAY) | sponsor [F] | Sept 2026 | https://www.thecommunityfoundation.org/nonprofit-faqs |
| S23 | GWCF "Our new donor portal has arrived" | sponsor [F] | Sep 21 (2026) | https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived |
| S24 | REPAY release on FE NXT Payment Assistant | vendor [V] | 2023-11-15 | https://repay.com/repay-powers-digital-payment-assistant-for-blackbaud-clients/ |
| S25 | BILL and Blackbaud partnership release | vendor [V] | 2026-09-29 | https://www.bill.com/press-release/bill-and-blackbaud-partner-to-simplify-vendor-payments |
| S26 | Blackbaud FE help: Payment Assistant onboarding | vendor [V] | live | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/fe/content/fe-payment-assistant-onboarding.html |
| S27 | FFTC portals (GiftingNetwork, Foundation Cloud) | portal [H] | 2026-11-15 | https://daf.fftc.org/m/login ; https://fftc.spectrumportal.net/ |
| S28 | dns.google: fftc.spectrumportal.net and a random-label NXDOMAIN check | DNS [H] | 2026-11-15 | https://dns.google/resolve?name=fftc.spectrumportal.net&type=A |
| S29 | San Diego Foundation FYE 2025-06 990 | 990 [F] | FY2025 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601339349305635_public.xml |
| S30 | G2 "Endowment Manager" (NPact) | aggregator [S] | undated | https://www.g2.com/products/endowment-manager/discuss |

---

## 7. Data dictionary

### `data/mission-2026-11-14/cf-ledger-families-2026-v2.csv`

The file holds 7 rows: SVCF, FFTC, GWCF, CFGP (new), IRCF, GKCCF and NYCT. Its columns are those of v1 plus `change_note`. Rows not listed keep their v1 values.

| Column | Meaning |
|---|---|
| `ein` | 9-digit EIN |
| `name` | Sponsor name as in v1 (CFGP: as on its 990) |
| `ledger_family` | Ledger family of the **general ledger** (v1 vocabulary: SF_NETSUITE, BLACKBAUD_FE, SF_INTACCT, FOUNDANT, SELF_OPERATED, etc.). Overlays such as FIT and portals go in `product` |
| `product` | GL plus overlays (FIT, Foundation Cloud, portal) as evidenced |
| `evidence_type` | Main evidence class for the row |
| `evidence_url` | Main source |
| `confidence` | high / medium / low / implied / none (v1 scale; NYCT "low" stands in for wave-12 "low-medium") |
| `retrieved` | 2026-11-15 for all v2 rows |
| `fy2024_daf_assets_usd` | DAFRC FY2024 DAF assets (CFGP from `form990-harvest-sponsor-universe-full.csv`) |
| `sponsor_type` | As in v1 |
| `evidence_detail` | Quotes and figures with their labels |
| `change_note` | What changed relative to v1 and why |

### `data/mission-2026-11-14/relationship-graph-edges-additions-14.csv`

Columns are the same as `relationship-graph-edges.csv`. There are 14 edges, EN001–EN014:
- `ledger_provider` for GL vendors and FIT;
- `technology_provider` for portal and grants layers;
- `payment_processor` for REPAY and BILL;
- `administers` for GKCCF back-office service, including one edge marked `historically_confirmed` (IRCF).

### `data/mission-2026-11-14/queue-proposals-batch29a.csv`

The file follows the format in `queue-proposals-README.md`. It holds 3 proposals:
- **P-B29A-01:** a REPAY/BILL grant-rail scan.
- **P-B29A-02:** a portal-versus-GL split for the spectrumportal.net rows.
- **P-B29A-03:** the date of FFTC's go-live and which portal its fundholders use.

## Validation corrections (wave 14, 2026-11-15) — governing
Source: [validation-wave14-report.md](validation-wave14-report.md); register `data/mission-2026-11-14/validation-register-wave14.csv`.

1. **Line 43 (§0, P-LDG-02).**
   - Replace: "One former or current client is confirmed by its tenant (Indian River CF), and IRCF now appears to have moved to Foundant."
   - With: "One sponsor outside the GKCCF family, Indian River CF, is confirmed as a donor-portal.org portal tenant by its own site. Back-office accounting for IRCF is not shown. IRCF now links both `ircf.donor-portal.org` and Foundant's `indianriver.fcsuite.com`, so it is moving or running both."
2. **Line 64 (§1.1 table, SVCF row).** Replace "FIT layered on NetSuite instead of a custom app" with "FIT used instead of a custom app that 'would layer on top of NetSuite' (a FIT–NetSuite integration at SVCF is implied, not stated)".
3. **Line 138 (§2.3 Reading).** Replace "IRCF has moved, or is moving, from the GKCCF back office to Foundant CommunitySuite." with "IRCF has moved, or is moving, from the GKCCF donor portal to Foundant CommunitySuite. Its homepage still links both logins."
