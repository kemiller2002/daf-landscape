# Batch 38A: FE NXT Payment Assistant grant payers (P-B29A-01), FFTC go-live and portal (P-B29A-03), NPact as a host (P-B31C-03), the last 8 Foundation Cloud GLs (P-B31C-02), the Give "$40B+" gap (P-B30C-03), PNC `/scbf` and `ocf` on iPhi (P-REN-04), GivingPoint donor export (P-B33B-01), and rails at four top-30 CFs (P-EXP-05)

**Date:** 2026-11-15. **Queue items:** P-B29A-01, P-B29A-03, P-B31C-03, P-B31C-02, P-B30C-03, P-REN-04, P-B33B-01, P-EXP-05 (`data/mission-2026-11-14/research-priority-queue.csv`).

**Status: public sources only.**
- I logged in nowhere, submitted no forms, contacted no one and called no tenant API.
- I read robots.txt on each host before fetching, using a generic User-Agent. I did not fetch `fcsuite.com`.
- Pages that refused scripted reads were not worked around: the npact.com WAF (403 to scripts), newhorizonsfoundation.net (a bot-check page), and tealhq.com (403).

**Robots disclosure.**
- `crt.sh/robots.txt` is `User-agent: * / Disallow: /`. My checker flagged this, but the same command still sent four crt.sh JSON queries (for `fftc.spectrumportal.net`, `daf.fftc.org`, `fcjc.fftc.org` and `myfcjc.org`) before I read the result.
- **I discarded that output and use none of it here.**
- Earlier batches (23, 30) cite crt.sh exports. The validator should note that the host disallows all crawling.

**Recency rule:** current-state claims rest on 2021+ evidence. One Wayback capture from 2018 is used only to date when a path existed (§6), not as a current-state claim.

**Read first and built on**, each with its governing corrections:
- `queue-batch31-ren-npact-gl.md` (wave 16)
- `queue-batch30-cf-coverage-give.md` (wave 15)
- `queue-batch29-fit-ledgers.md` (wave 14)
- `queue-batch33-voids-exports-rails.md` (wave 18)
- Also `queue-community-foundation-rails-portals.md` (wave 7: GWCF is "REPAY (payments partner, alongside Blackbaud Financial Edge NXT)") and existing edges EN003/EN004/EN009/EN010, EF003/EF004 and EB007.

**Evidence labels:**
- [F]: first-party (sponsor or vendor page, posting, government record, filing)
- [V]: vendor statement
- [S]: search-engine extract; the page itself was not opened or not readable
- [H]: HTTP or DNS observation
- [I]: my inference

**Outputs:**
- `data/mission-2026-11-14/relationship-graph-edges-additions-22.csv`: EV001–EV008
- `data/mission-2026-11-14/queue-proposals-batch38a.csv`: P-B38A-01 and P-B38A-02

---

## 0. Answers

| Item | Answer | Confidence |
|---|---|---|
| **P-B29A-01** | **GWCF is still the only sponsor found that publicly pays grants through FE NXT Payment Assistant (REPAY). No sponsor names BILL yet.**<br>- GWCF's live [Nonprofit FAQ](https://www.thecommunityfoundation.org/nonprofit-faqs) still says REPAY, not BILL: "ACH is the default method"; "If REPAY doesn't receive it in that time, they will issue the grant or payment by check" [F, read 2026-11-15].<br>- Searches for grantee-facing REPAY, "Payment Assistant" and BILL text found no other CF or DAF sponsor.<br>- Six FE NXT/Foundation Cloud sponsors' sites show no REPAY text: San Diego, Tulsa, Santa Barbara, CFES, FFTC and CFGP [S].<br>- Among CFs in the repo's 990 VII-B harvest, only GWCF has a Blackbaud payee line of $100k or more.<br>- BILL's Payment Assistant is in an early-adopter programme for domestic vendor payments ([Blackbaud help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/fe/content/fe-payment-assistant-virtual-cards.html) [V]), so grantee-facing BILL notices are unlikely before 2027 [I] | Medium (a negative search; grantee FAQs are often unindexed) |
| **P-B29A-03** | **Fundholders use GiftingNetwork (`daf.fftc.org`). The FE NXT / Foundation Cloud go-live date is still not public, but it can be bounded to 2024-02 … 2025-03 [I].**<br>- fftc.org links only "MyFFTC Login" → `daf.fftc.org` and "MyFCJC login" → `myfcjc.org` (→ `fcjc.fftc.org`). Both sign-in pages read "Powered by GiftingNetwork" and "If this is your first time logging into the new portal, you'll need to re-register" [F/H].<br>- `fftc.spectrumportal.net` still resolves and serves a "Foundation Cloud Community Portal" shell, but no fftc.org page links it [H/I].<br>- FE NXT is the current GL: a 2026-03-26 FFTC posting lists "Blackbaud Financial Edge NXT", and other 2026 postings name FE NXT and RE NXT [F/S].<br>- FFTC's audited IT expense fell from $5.33m (2023) to $2.85m (2024) ([audit](https://www.fftc.org/sites/default/files/2025-09/Foundation_For_The_Carolinas_12-31-24_Audited_Financials.pdf)) [F]. This is consistent with a 2023 build year [I].<br>- The TY2024 990 shows no software payee above $100k (top five: art, legal, audit, advertising, consulting) [F] | High (portal); medium (GL); low (go-live window) |
| **P-B31C-03** | **No. NPact does not present itself as a host or managed-services provider for Blackbaud software.**<br>- NPact's [Standard Terms](https://npact.com/software-as-a-service-license-and-services-standard-terms/) (modified 2026-01-08) speak only of "Software hosted by NPact" (NPact's own SaaS). They say "NPact is not responsible for any third-party products, including Blackbaud products" and that the customer "must contract directly with Blackbaud" [F].<br>- "Hosting" is not a defined service type. The defined types are Subscription, Professional and Support Services. Professional Services include "monitoring … backup and recovery" under a SOW [F].<br>- Of NPact's 36 sitemap pages ([page-sitemap](https://npact.com/page-sitemap.xml)), none is a hosting page. Blackbaud Consulting, Outsourced Accounting and Foundation Cloud pages do not mention hosting [F].<br>- Santa Barbara's $130k "HOSTED INFRASTRUCTURE" payee is therefore best read as the Foundation Cloud SaaS (FC is SBF's third database beside FE and RE), not hosting of FE/RE [I] | Medium-high |
| **P-B31C-02** | **No change: all 8 stay "GL not evidenced".**<br>- Montana's FY2024 audit and Ventura's FY2025 audit contain no system-conversion, software-capitalisation or cloud-computing note.<br>- Searches for Door County, Frederick, Amarillo, Greenville, NW Minnesota and Initiative postings that name a GL found none [S]. | High that public sources are exhausted; no ledger evidence |
| **P-B30C-03** | **The gap closes on a time basis. No unknown client is needed.**<br>- Swap Vanguard Charitable's FY2024 DAFRC value ($21.95bn) for its own FYE 2025-06 DAF value ($27.01bn; repo `breadth-entity-profiles.csv` from the TY2024 990, object 202621329349306657, listed in the [IRS 2026 index](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) [F]). Known clients then sum to **$41.80bn**, or **$40.11bn** without the three staging-only clients.<br>- Give's own timeline reads "2024 — $8B live or in implementation" → "2025 — $40B+" ([company page](https://www.giveinteractive.com/company) [V]). That step is the size of the Vanguard Charitable contract (released 2025-11-04).<br>- `nhf` and `jttw` stay unidentified. New Horizons' TY2024 990 lists no VII-B contractor, and its site blocks scripted reads | Medium (the reconciliation uses a repo figure I could not re-read; the mirror lacks the XML) |
| **P-REN-04** | **Neither tenant is identified. Two new dated facts:**<br>- **`pnc.iphiview.com/scbf/`** was captured by the Wayback Machine with HTTP 200 on **2018-08-31** ([availability API](https://archive.org/wayback/available?url=pnc.iphiview.com/scbf) [H]). The path predates the PNC Gifting Portal launch (2021-03-08), which weakens the "Gifting Portal client" candidate [I].<br>- **`ocf.iphiview.com/ocf/`** was captured with HTTP 200 on **2025-12-20** ([availability API](https://archive.org/wayback/available?url=ocf.iphiview.com/ocf) [H]). It was therefore live after the 2025-04-20 certificate and lapsed between 2025-12-20 and 2026-11-15.<br>- `web.archive.org` itself was unreachable from this session (connection reset), so the captured pages were not read → P-B38A-01.<br>- PNC's public DAF pages and its Fund for Charitable Giving guide (PDF modified 2023-10-24; "Grants are delivered by checks") contain no "SCBF" or iPhi reference [F] | Low (identity); high (capture dates) |
| **P-B33B-01** | **Yes for NPT. NPT documents the export to donors.** NPT's [How to Access Fund Activity](https://www.nptrust.org/wp-content/uploads/2022/09/How-to-Access-Fund-Activity-NPT.pdf) (PDF created 2026-03-23, code "NPT TUT HTAFA 0326"):<br>- "You can also export the data in any table to an Excel file by clicking the Export link beneath the table." Screenshots show "Export" under the Issued Grants, Contribution Activity and Grant Activity tables [F].<br>- The live GivingPoint main bundles (NPT, J.P. Morgan `jpmgiving.org`, J.P. Morgan `jpmgiftfund.org`) carry the same donor text: "The selected date range affects the data you export. Exporting table data can take five or more seconds." No per-program display flag gates export (the only `displaySettings` flag is `displayfundActivityStatements`) [F, code].<br>- J.P. Morgan's "Explore NPT GivingPoint" page is indexed as saying donors can "export data for your records" [S].<br>- **UBS and other NPT programs:** not separately documented [I: same build] | High (NPT); medium (J.P. Morgan); low (others) |
| **P-EXP-05** | **Still nothing public for CF Greater Memphis, East Bay CF, GiveWell CF or Marin.**<br>- Targeted searches found no grantee payment page or award letter for any of the four.<br>- EBCF's fund-advisor page (© 2026) gives only deadlines ("received after December 9 will be processed and disbursed in January 2027") [F].<br>- None of the four has a payment-vendor payee in TY2021–24 VII-B (repo harvest). Marin's IT payee is VRP Consulting (Salesforce consultancy) [F] | High that nothing is public; no rail evidence |

---

## 1. P-B29A-01: who pays grants through FE NXT Payment Assistant

| Check | Result |
|---|---|
| GWCF Nonprofit FAQ (live 2026-11-15) [F] | "As part of our systems transformation upgrades completed in September 2026, the Greater Washington Community Foundation has partnered with Blackbaud and REPAY"; "ACH is the default method, and REPAY can deposit only to standard checking accounts"; "Please return the form within one business day. If REPAY doesn't receive it in that time, they will issue the grant or payment by check"; "Once completed, future payments move to ACH automatically". **No BILL text** |
| Web search: "REPAY" plus grant, foundation, community foundation, enrollment or "on behalf of"; "Payment Assistant" plus grantees; "powered by BILL" plus grants (6 queries) [S] | Only GWCF. The other hits are Blackbaud FE help pages, REPAY's own vendor-enablement pages, and unrelated CF ACH programmes (Greater Cincinnati runs its own `gcfdn.org/ach` portal with micro-deposit verification, which is not REPAY) |
| Site-restricted search for "REPAY" on six FE NXT/FC sponsor domains (SDF, TCF, SBF, CFES, FFTC, CFGP) [S] | None |
| Repo 990 VII-B harvest (`form990-contractors-harvest-full.csv`): Blackbaud, REPAY and BILL payees | 24 Blackbaud lines, nearly all at university or hospital foundations. GWCF is the only community foundation ($177,444 TY2022; $151,433 TY2024). No REPAY or BILL payee anywhere |
| BILL status | The release is dated 2026-09-29 ([BILL](https://www.bill.com/press-release/bill-and-blackbaud-partner-to-simplify-vendor-payments)) and was republished 2026-10-12 ([CPA Practice Advisor](https://www.cpapracticeadvisor.com/2026/10/12/bill-and-blackbaud-partner-to-simplify-vendor-payments-for-nonprofits-and-education/191503/)). Blackbaud help: BILL with Payment Assistant is "currently in an Early Adopter Program (EAP)" [V] |

**Reading [I]:**
- Payment Assistant's vendor flow behaves the same for grantees: an email from REPAY, ACH by default, a check if the form is not returned, and no pre-notes. A CF using it would show these signs only in grantee emails or FAQs, and most CFs do not publish such FAQs.
- The absence of other names is therefore weak evidence of absence.
- GWCF remains the single public marker. When GWCF rewrites its FAQ for BILL, that will date its own migration.

## 2. P-B29A-03: FFTC ledger, go-live window and portal

| Evidence | What it shows |
|---|---|
| [fftc.org](https://www.fftc.org/) navigation, live 2026-11-15 [F] | "MyFFTC Login" → `https://daf.fftc.org`; "MyFCJC login" → `https://myfcjc.org`. No Foundation Cloud link |
| [daf.fftc.org/m/login](https://daf.fftc.org/m/login) and `myfcjc.org` → [fcjc.fftc.org/m/login](https://fcjc.fftc.org/m/login), fetched 2026-11-15 [H] | Titles "Foundation for the Carolinas" and "Foundation For The Charlotte Jewish Community"; both "Powered by GiftingNetwork". Banner: "If this is your first time logging into the new portal, you'll need to re-register, as your previous credentials are no longer valid." The FCJC affiliate is on the same GiftingNetwork tenant family (already EF004) |
| [fftc.spectrumportal.net](https://fftc.spectrumportal.net/) [H] | Resolves (52.154.137.83) and serves a "Foundation Cloud Community Portal" shell. Unlinked from fftc.org. It is probably retained for grants or applicants, or simply not yet decommissioned [I] |
| GiftingNetwork release, repo (batch 30) [V] | "running a new donor portal on the GiftingNetwork platform since July 1, 2026" |
| FFTC "Finance Data & Automation Analyst" ([Y-Axis copy](https://jobs.y-axis.com/jobs/finance-data-automation-analyst-foundation-for-the-carolinas); posted 2026-03-26, expiry 2026-06-23) [F via job board] | "Familiarity with financial and ERP systems such as: Sage Intacct Blackbaud Financial Edge NXT NetSuite QuickBooks". This is a list of examples, so it is a weak signal on its own |
| FFTC "Financial Analyst, Reporting & Analytics" and "Donor Operations Data Analyst" (2026; Teal/Y-Axis copies, 403/404 now) [S] | "Experience with nonprofit fund-accounting systems, including Financial Edge NXT"; "record maintenance in both Raiser's Edge NXT and Financial Edge NXT" |
| NPact story (repo [V] 2025-03-07; scripted read now blocked by WAF) and search extract [S] | "self-hosted software stack was sunsetting"; selected "Raiser's Edge NXT, Financial Edge NXT, and NPact's Foundation Cloud Grants and Foundation Cloud Community Portal". No date in any extract |
| FFTC 2024 audit, statement of functional expenses [F] | Information technology: **$5,325,416 (2023)** → **$2,853,618 (2024)**. There is no software-capitalisation or cloud-computing note |
| FFTC TY2024 990 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543219349306689_public.xml)) [F] | VII-B: James Cohan Gallery $265,000; McGuireWoods $217,997; Cherry Bekaert $157,650; Adams Outdoor $143,535; Loyd Visuals $101,200. No NPact, Blackbaud or GiftingNetwork payee. The TY2025 return is not yet in the IRS 2026 index (checked 2026-11-15) |

**Go-live window [I]:**
- **Lower bound:** Give Interactive hosts lapsed in 2024-02 (repo).
- **Upper bound:** the NPact story was published 2025-03-07 and describes the system as live.
- The audit's IT-expense peak in 2023 fits a 2023 build with go-live in 2024.
- Not dated first-party, so this stays an inference → P-B38A-02 (TY2025 990, then the 2025 audit).

**Ledger:** BLACKBAUD_FE (NXT). Confidence moves from medium to **medium-high**, on 2026 FFTC postings [F/S] plus the vendor story.

**Portal:** **GiftingNetwork** for fundholders (high). Foundation Cloud remains a live but unlinked host.

## 3. P-B31C-03: is NPact a hosting or managed-services provider for Blackbaud CFs?

| Source | Text |
|---|---|
| [Standard Terms](https://npact.com/software-as-a-service-license-and-services-standard-terms/) (modified 2026-01-08) [F] | §2.3 "remotely logging into the Software hosted by NPact for Customer"; §4.4(b) "If NPact hosts Software for Customer that requires access to Customer Data…"; §4.3 "NPact is not responsible for any third-party products, including Blackbaud products" and "must contract directly with Blackbaud or any other third-party for its products". Services = Subscription, Professional (incl. "monitoring, technical support, backup and recovery"), Support |
| [Assumptions and Responsibilities](https://npact.com/assumptions-and-responsibilities/) (2026-01-08) [F] | "The Software included under the ATP is understood to be Software-as-a-Service"; "All Services will be performed remotely" |
| [Blackbaud Consulting](https://npact.com/blackbaud-consulting/) (2026-10-12), [Outsourced Accounting](https://npact.com/outsourced-accounting/) (2025-11-25), [Foundation Cloud](https://npact.com/software/foundation-cloud/) (2026-11-12) [F] | Consulting, implementation, training, reports, audit preparation and statements. None mentions hosting or managed infrastructure. Foundation Cloud "integrates with industry-leading CRM and financial accounting tools" (no GL named) |
| [NPact page sitemap](https://npact.com/page-sitemap.xml) (36 URLs) [F] | No hosting or managed-services page |
| Repo 990 VII-B harvest, "HOST" / Fusion / NPact payees [F] | SBF: Centered Networks "HOSTED INFRASTRUCTURE" $110,138 (TY2022) and $159,839 (TY2023) → Fusion Labs $130,000 (TY2024). No other CF pays NPact for hosting. Other CFs pay hosting to Stellar (Cleveland $416,391 TY2024) or NaviSite (SVCF TY2022). NPact lines elsewhere: GKCCF "Advising", GNOF "Implementation", VCF "Consulting", AEF "Software development" |
| [PR Newswire 2022](https://prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html) [V] | NPact would move FIMS and DonorCentral "to NPact's own independent infrastructure". NPact hosts its *own* products, including the FIMS ledger, which it now owns |

**Reading [I]:**
- NPact's hosting is hosting of NPact-owned software: Foundation Cloud and, since 2022, FIMS/DonorCentral.
- Its terms push Blackbaud licensing and responsibility back to the customer. It is not an FE/RE host.
- SBF's switch from Centered Networks to Fusion Labs under the same 990 description most likely reflects the start of the Foundation Cloud subscription replacing a prior hosted environment (probably SBF's old on-premises/FIMS stack). The SBF posting lists FC as a separate database.
- **Effect on the NPact target profile:** CF revenue is SaaS (Foundation Cloud, FIMS, DonorCentral) plus services; it does not include Blackbaud hosting.

## 4. P-B31C-02: the last 8 Foundation Cloud tenants

| Tenant | New check | Result |
|---|---|---|
| Montana | [FY2024 audit](https://stdidmtcfprod.blob.core.windows.net/mtcf/documents/MCF-June-2024-Audited-Financials-Statements.pdf) (June 2024 and 2023) [F] | No software, system or cloud-computing note. IT expense $145,080 (FY2024) |
| Ventura | [FY2025 audit](https://vccf.org/wp-content/uploads/2026/02/Ventura-County-Community-Foundation-Sep25-AR-Final.pdf) (Sept 2025) [F] | No system note. IT $135,475 (FY2025) vs $131,612 (FY2024) |
| Greenville | Search for postings naming FE, Blackbaud, Intacct or QuickBooks [S] | Only Prisma Health (Greenville) postings, which belong to a different employer |
| Initiative Foundation | Search [S] | A Little Falls "Accounting Specialist" aggregator listing does not name the employer (jobg8 robots disallows, so it was not opened) |
| Door County, Frederick, Amarillo, NW Minnesota | Search [S] | Nothing |

The v3 split is unchanged: 8 rows, $256m, 10.4%.

## 5. P-B30C-03: the Give "$40B+" gap

| Basis | Known-client total |
|---|---|
| Batch 30 (all clients at DAFRC FY2024 DAF assets) | $36.74bn (gap $3.26bn) |
| Vanguard Charitable at FYE 2025-06 DAF value $27,012,089,382 (repo `breadth-entity-profiles.csv`, from TY2024 990 object 202621329349306657; the IRS 2026 index lists this return, tax period 202506) | **$41.80bn** |
| Same, excluding staging-only Minneapolis, Thrivent and Stifel | **$40.11bn** |

- **Give's own series** ([company page](https://www.giveinteractive.com/company), read 2026-11-15) [V]: "2023 — $2B processed"; "2024 — $8B live or in implementation"; "2025 — $40B+ live or in implementation". The page names no clients and gives no client count.
- **Reading [I]:** the claim is consistent with known clients measured at 2025 asset levels. The 2024 → 2025 jump (about $32bn) matches Vanguard Charitable plus 2025 additions (WaterStone, ImpactAssets hub).
- **`nhf` and `jttw` stay unidentified.**
  - New Horizons' TY2024 990 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349306440_public.xml)) has no VII-B contractor; IT expense is $474,548; 287 DAFs; website `newhorizonsfoundation.net`, which shows a bot check.
  - No public page links New Horizons to Give.
- **Caveat:** the GT mirror returned NoSuchKey for the Vanguard XML, and ProPublica's Schedule D page did not render. So the $27.01bn is the repo's earlier read, not re-verified here.

## 6. P-REN-04: PNC `/scbf` and `ocf.iphiview.com`

| Host | New evidence | Reading |
|---|---|---|
| `pnc.iphiview.com/scbf/` | Wayback availability API: closest capture `20180831230800`, status 200 [H]. No 2021+ capture is returned for the path. The bare host has no capture | The `/scbf` program existed on iPhi under the PNC host by 2018-08, 2.5 years before the PNC Gifting Portal launch (2021-03-08). If it is a Gifting Portal client, it was migrated in. More likely it was a pre-existing PNC-administered fund [I]. Its identity is unknown |
| `ocf.iphiview.com/ocf/` | Wayback capture `20251220065252`, status 200; the root has a 2018-03-30 capture [H] | The tenant was live on 2025-12-20 and NXDOMAIN by 2026-11-15, so it lapsed within the last 11 months. It has existed since at least 2018. This fits a long-standing iPhi CF that left in 2026 [I]. Omaha (Foundant since 2024-07) and Oregon CF (Salesforce) are unlikely matches, since both had moved before 2025-12 [I] |
| PNC public pages | [Gifting Portal launch](https://pnc.mediaroom.com/2021-03-08-PNC-Institutional-Asset-Management-Launches-PNC-Gifting-Portal); [Fund for Charitable Giving guide](https://www.pnc.com/content/dam/pnc-com/pdf/personal/wealth-investments/private-bank/Fund_for_Charitable_Giving_Program_Informational_Guide.pdf) (modified 2023-10-24) [F] | No "SCBF" and no iPhi URL. FCG: "Grants are delivered by checks from The Fund for Charitable Giving" |
| Search ("iphiview.com/scbf", "pnc.iphiview.com", "ocf.iphiview.com") [S] | No hits |

The snapshot contents were not read because `web.archive.org` resets connections from this session → P-B38A-01.

## 7. P-B33B-01: GivingPoint donor Excel export

| Evidence | Text |
|---|---|
| NPT [How to Access Fund Activity](https://www.nptrust.org/wp-content/uploads/2022/09/How-to-Access-Fund-Activity-NPT.pdf), 4 pp., PDF created 2026-03-23 [F] | "TO BEGIN: Log in to the donor portal at nptgivingpoint.org and click Activity…"; "You can also export the data in any table to an Excel file by clicking the Export link beneath the table." "Export" links appear under the Issued Grants, Contribution Activity, Grant Activity and Recurring Grant Schedules tables. Grant letters can be opened from the Grant Letter column |
| GivingPoint main bundles, live 2026-11-15: [NPT](https://www.nptgivingpoint.org/main-OYPICD2D.js), [jpmgiving.org](https://jpmgiving.org/main-JBUINBFD.js), [jpmgiftfund.org](https://jpmgiftfund.org/main-W7WT45DD.js) [F, code] | Same donor instruction in all three: "The selected date range affects the data you export. Exporting table data can take five or more seconds." `exportExcel` is bound on data tables, and `exportService.export("accounts.xlsx", …)` is called. No export toggle in `displaySettings` |
| J.P. Morgan [Explore NPT GivingPoint](https://jpmgiving.org/givingpoint) (SPA; text not rendered to WebFetch) [S] | "access gift receipts, grant letters, and other DAF history, and export data for your records" |
| NPT [A Guide to your Donor-Advised Fund](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) (PDF created 2026-10-15) [F] | No export text; documents "available for download" only |

**Effect:** NPT's Y1/Y5 export score should move from "no (2021+ sources)" to "**yes, Excel export of grant activity, issued grants and contributions (NPT tutorial 2026-03)**". J.P. Morgan programs: yes, at medium [code + S]. UBS, Wells Fargo and other NPT-sponsored GivingPoint sites: probable [I], not documented.

## 8. P-EXP-05: four top-30 CFs with no public rail

| CF | Portal (repo) | Checks this batch | Result |
|---|---|---|---|
| CF of Greater Memphis | Ren iPhi | Search for cfgm.org ACH, direct-deposit or electronic-payment text [S] | Nothing first-party. An aggregator mention of a "grant check" (2024 capacity grants) is unchanged [S] |
| East Bay CF | akoyaGO GOfund | [Fund-advisor resources](https://www.ebcf.org/donors/donor-resources/resources-for-fund-advisors/) (© 2026); Grants Management page ([`?p=46229`](https://www.ebcf.org/?p=46229) → 404) [F] | Deadlines only; no payment method |
| GiveWell CF | Foundant | Search [S]; harvest | Nothing. Results conflate it with GiveWell (the charity evaluator) |
| Marin CF | custom (`givingcenter.marincf.org`) | Search [S]; harvest | Nothing new. VII-B IT payee is VRP Consulting ($494,950 TY2024) |

The top-30 rail map is unchanged: 3 not found among the 15, plus Marin unverified.

---

## 9. Corrections and notes for existing repo text (proposed, not governing)

1. **`cf-ledger-families-2026-v2.csv`, FFTC.** Raise confidence to medium-high, citing the 2026 FFTC postings. Add to notes: "Fundholder portal GiftingNetwork (daf.fftc.org, 'new portal', re-register); fftc.spectrumportal.net live but unlinked (2026-11-15)."
2. **`donor-data-export-top10-2026.csv`, NPT row (and batch 33B note 6).** Replace "availability to donors unverified" with "documented to donors: NPT 'How to Access Fund Activity' (2026-03) — 'export the data in any table to an Excel file' (batch 38A §7)".
3. **`give-claim-reconciliation-batch30.csv`.** Add a note row: "At Vanguard Charitable FYE 2025-06 DAF value ($27.01bn) the known-client total is $41.80bn ($40.11bn excl. staging-only); gap closes on asset-date basis."
4. **`ren-iphi-tenant-census.csv`.**
   - `ocf` row: add "Wayback capture 2025-12-20 (HTTP 200); lapsed between 2025-12-20 and 2026-11-15".
   - `pnc` row: add "/scbf captured 2018-08-31, predates PNC Gifting Portal (2021-03-08)".
5. **`queue-batch31-ren-npact-gl.md` §4 note on NPact services lines.** Add: "NPact Standard Terms §4.3 exclude Blackbaud products; 'hosting' covers only NPact Software (batch 38A §3)."
6. **crt.sh.** Its robots.txt disallows all agents. Batch 23 and batch 30 certificate spans came from crt.sh; the validator may wish to flag those sources' crawl status.

## 10. Limitations

- npact.com customer-story and product pages refuse scripted reads (WAF 403) and render empty to WebFetch. FFTC story text is from repo reads and search extracts only.
- `web.archive.org` was unreachable, so only availability-API metadata (capture timestamp and status) is used.
- FFTC's TY2025 990 (CY2025) is not yet in the IRS index. That is the filing that would show 2025 NPact or GiftingNetwork payments.
- The Vanguard FYE 2025-06 DAF value is a repo figure I could not re-read.
- The REPAY/BILL scan is search-based. Grantee FAQs behind portals, and grantee emails, are invisible to it.

---

## 11. Source register

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| S1 | GWCF Nonprofit FAQ | sponsor [F] | Sept 2026; read 2026-11-15 | https://www.thecommunityfoundation.org/nonprofit-faqs |
| S2 | Blackbaud FE help: Payment Assistant virtual cards with BILL / onboarding | vendor [V] | live | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/fe/content/fe-payment-assistant-virtual-cards.html ; https://webfiles-sc1.blackbaud.com/files/support/helpfiles/fe/content/fe-payment-assistant-onboarding.html |
| S3 | BILL–Blackbaud release; CPA Practice Advisor copy | vendor [V] | 2026-09-29; 2026-10-12 | https://www.bill.com/press-release/bill-and-blackbaud-partner-to-simplify-vendor-payments ; https://www.cpapracticeadvisor.com/2026/10/12/bill-and-blackbaud-partner-to-simplify-vendor-payments-for-nonprofits-and-education/191503/ |
| S4 | Repo 990 VII-B harvest | filings [F] | TY2021–24 | data/mission-2026-11-14/form990-contractors-harvest-full.csv |
| S5 | fftc.org homepage navigation | sponsor [F] | 2026-11-15 | https://www.fftc.org/ |
| S6 | FFTC and FCJC GiftingNetwork sign-in pages | portal [H] | 2026-11-15 | https://daf.fftc.org/m/login ; https://fcjc.fftc.org/m/login |
| S7 | fftc.spectrumportal.net | portal [H] | 2026-11-15 | https://fftc.spectrumportal.net/ |
| S8 | FFTC Q3 2026 Quarterly Spotlight | sponsor [F] | 2026 Q3 | https://fftc.org/node/9634 |
| S9 | FFTC Finance Data & Automation Analyst (Y-Axis copy) | posting [F] | 2026-03-26 | https://jobs.y-axis.com/jobs/finance-data-automation-analyst-foundation-for-the-carolinas |
| S10 | FFTC Financial Analyst; Donor Operations Data Analyst (Teal) | posting [S] | 2026 | https://www.tealhq.com/job/financial-analyst-reporting-analytics_7ea1a3c2de062d79cb3c310df644cf2fe3760 ; https://www.tealhq.com/job/donor-operations-data-analyst_7ea1a9840a242c75aecd785bcac5a21296805 |
| S11 | FFTC 2024 audited financial statements | sponsor [F] | posted 2025-09 | https://www.fftc.org/sites/default/files/2025-09/Foundation_For_The_Carolinas_12-31-24_Audited_Financials.pdf |
| S12 | FFTC TY2024 990 XML | filing [F] | TY2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543219349306689_public.xml |
| S13 | IRS e-file indexes 2025, 2026 | government [F] | read 2026-11-15 | https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv ; https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv |
| S14 | NPact story FFTC (search extract) | vendor [V]/[S] | 2025-03-07 | https://npact.com/customer-stories/foundation-for-the-carolinas/ |
| S15 | NPact Standard Terms; Assumptions and Responsibilities | vendor [F] | 2026-01-08 | https://npact.com/software-as-a-service-license-and-services-standard-terms/ ; https://npact.com/assumptions-and-responsibilities/ |
| S16 | NPact Blackbaud Consulting; Outsourced Accounting; Foundation Cloud; page sitemap | vendor [F] | 2026-10-12; 2025-11-25; 2026-11-12; 2026-11-13 | https://npact.com/blackbaud-consulting/ ; https://npact.com/outsourced-accounting/ ; https://npact.com/software/foundation-cloud/ ; https://npact.com/page-sitemap.xml |
| S17 | NPact acquires FIMS and DonorCentral | press [V] | 2022-09 | https://prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html |
| S18 | Montana CF FY2024 audit | sponsor [F] | FY2024 | https://stdidmtcfprod.blob.core.windows.net/mtcf/documents/MCF-June-2024-Audited-Financials-Statements.pdf |
| S19 | Ventura County CF FY2025 audit | sponsor [F] | FY2025 (posted 2026-02) | https://vccf.org/wp-content/uploads/2026/02/Ventura-County-Community-Foundation-Sep25-AR-Final.pdf |
| S20 | Give Interactive company page | vendor [V] | read 2026-11-15 | https://www.giveinteractive.com/company |
| S21 | New Horizons Foundation TY2024 990 XML | filing [F] | TY2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349306440_public.xml |
| S22 | Repo Vanguard Charitable FYE 2025-06 profile row | repo [F] | FY2025 | data/mission-2026-11-14/breadth-entity-profiles.csv |
| S23 | Wayback availability API (pnc /scbf; ocf /ocf; ocf root) | archive [H] | captures 2018-08-31; 2025-12-20; 2018-03-30 | https://archive.org/wayback/available?url=pnc.iphiview.com/scbf ; https://archive.org/wayback/available?url=ocf.iphiview.com/ocf ; https://archive.org/wayback/available?url=ocf.iphiview.com |
| S24 | PNC Gifting Portal launch; PNC Fund for Charitable Giving guide | bank [F] | 2021-03-08; 2023-10-24 | https://pnc.mediaroom.com/2021-03-08-PNC-Institutional-Asset-Management-Launches-PNC-Gifting-Portal ; https://www.pnc.com/content/dam/pnc-com/pdf/personal/wealth-investments/private-bank/Fund_for_Charitable_Giving_Program_Informational_Guide.pdf |
| S25 | NPT How to Access Fund Activity; NPT DAF guide | sponsor [F] | 2026-03-23; 2026-10-15 | https://www.nptrust.org/wp-content/uploads/2022/09/How-to-Access-Fund-Activity-NPT.pdf ; https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf |
| S26 | GivingPoint main bundles (NPT, jpmgiving, jpmgiftfund) | code [F] | live 2026-11-15 | https://www.nptgivingpoint.org/main-OYPICD2D.js ; https://jpmgiving.org/main-JBUINBFD.js ; https://jpmgiftfund.org/main-W7WT45DD.js |
| S27 | J.P. Morgan Explore NPT GivingPoint | sponsor [S] | live | https://jpmgiving.org/givingpoint |
| S28 | EBCF fund-advisor resources | sponsor [F] | © 2026 | https://www.ebcf.org/donors/donor-resources/resources-for-fund-advisors/ |
| S29 | Repo CF rails file (Memphis, EBCF, GiveWell, Marin rows) | repo | 2026-11-14 | data/mission-2026-11-14/community-foundation-rails-portals-2026-v2.csv |

---

## 12. Data dictionary

### `relationship-graph-edges-additions-22.csv` (EV001–EV008)

- **Columns:** the same as `relationship-graph-edges.csv`: `edge_id, source_entity, source_type, target_entity, target_type, relationship_type, status, evidence_summary, source_url, source_date, accessed_date, notes`.
- **Status:**
  - `confirmed`: first-party text, code or a filing.
  - `inferred`: archive metadata, search extract or reasoning.
- **Relationship types used:**
  - `portal_provider`
  - `ledger_provider`
  - `contract_exclusion`: vendor terms that exclude a third party's products.
  - `donor_export_feature`: donor-facing export documented. EV004 is a self-loop on the sponsor; EV005 runs from the platform builder to the program.
  - `vendor_claim`: self-loop; a vendor's own metric series.
  - `technology_provider`
- Entity names follow existing edges, for example "NPact (Fusion Laboratories LLC)" and "FOUNDATION FOR THE CAROLINAS (EIN 56-6047886)".

### `queue-proposals-batch38a.csv`

- **Format:** per `queue-proposals-README.md`; `state` = `open`.
- **P-B38A-01:** read the two Wayback captures (`ocf.iphiview.com/ocf/` 2025-12-20; `pnc.iphiview.com/scbf/` 2018-08-31) from an environment that can reach web.archive.org, to name the tenants.
- **P-B38A-02:** FFTC's TY2025 990 VII-B and 2025 audit, once posted, to date the FE NXT / Foundation Cloud / GiftingNetwork spend.

## Compliance note (2026-11-15) — governing
crt.sh disallows all crawlers in its robots.txt. Any claim in this document that rests **only** on crt.sh certificate data is downgraded to an unverified lead until re-sourced. See [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md).
