# Salesforce-centred ledger segment (P-LDG-04), GL at the largest Salesforce-portal CFs (P-LDG-03), NPact owner (P-ADV-04)

**Date:** 2026-11-15. **Queue items:** P-LDG-04, P-LDG-03, P-ADV-04 (`data/mission-2026-11-14/research-priority-queue.csv`).
**Status:** public sources only. I logged in nowhere, submitted no forms and contacted no one. The only structured queries were to public open-data or careers endpoints that a browser loads without credentials: data.texas.gov (Comptroller "Active Franchise Taxpayers"), the ProPublica Nonprofit API, and the public ADP Workforce Now requisition feed linked from oregoncf.org. Pages that refused scripted reads (Armanino, philanthropynewyork.org, pittsburghfoundation.org, aapip.org, several job boards) were not worked around. Where only search-index text was available, the claim is marked [R].
**Recency rule:** every current-state claim rests on 2021+ evidence. That means pages live on 2026-11-15, TY2021–2025 990 lines, or postings and case studies dated 2021 or later. One 2014 NCF/Skuid story turned up and is not used.

**Read first and built on:**
- `queue-ledgers-behind-portals.md`, including its wave-10 governing corrections. Those corrections fix Maine's Accounting Seed wording, the CFNEF citation and date, the Arizona case-study date of 2024-03-06, and NPact's entity-form conflict.
- `queue-cf-vendor-map.md` (wave-9 corrections).
- `queue-adviser-fees-pools-npact.md` (wave-11 corrections). That file established that BroadWest closed the purchase on 2020-12-30, that the 2022 FIMS buyer was Fusion Laboratories LLC, and the Cambria lead.
- `cf-ledger-vendors-2026.csv` and `cf-vendor-map-by-ein.csv`.

**Evidence labels:**
- **[F]** first-party: the sponsor's own page, posting or return, or a government record.
- **[V]** vendor statement or case study.
- **[R]** search-index capture of a page I could not open.
- **[I]** my inference.

**Outputs:**
- [`data/mission-2026-11-14/cf-ledger-families-2026.csv`](../../data/mission-2026-11-14/cf-ledger-families-2026.csv): 491 rows.
- [`data/mission-2026-11-14/relationship-graph-edges-additions-13.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-13.csv): edges EM001–EM035.
- [`data/mission-2026-11-14/queue-proposals-ledger-segment.csv`](../../data/mission-2026-11-14/queue-proposals-ledger-segment.csv): P-LSG-01 to P-LSG-04.

---

## 0. Headline answers

| Item | Answer | Confidence |
|---|---|---|
| **P-LDG-04: size of the Salesforce-centred ledger segment** | **11 sponsors with a high- or medium-confidence named ledger, holding $3.53bn of FY2024 DAF assets.** Families: Fund 360 / Accounting Seed on Salesforce, 5 rows, $1.20bn; Sage Intacct + Salesforce, 4 rows, $2.32bn; Salesforce + another GL (QuickBooks, AccuFund), 2 rows, $0.01bn. By sponsor type: 7 CF rows ($2.78bn), 3 faith-based ($0.55bn; one, Catholic Foundation of Eastern Washington, has no DAFRC assets) and 1 national ($0.21bn). **A further $15.6bn sits in a low-confidence NetSuite + Salesforce bucket:** SVCF $9.58bn, NCF $5.46bn and Pittsburgh $0.53bn | High on the 11 named rows; low on NetSuite |
| P-LDG-04: exits to this route since 2021 | **5 dated or datable exits to a Salesforce-centred ledger.** FIMS: JCF San Diego, Arizona CF, Vermont CF. Blackbaud RE/FE/Grant Edge: Maine CF. Renaissance PSG: Bradley Impact Fund. **2 more under way in 2026:** Pittsburgh (Salesforce + NetSuite) and NYCT (legacy ERP to Salesforce + Sage Intacct). GNOF and Minneapolis are unresolved | Medium (most go-live dates are not stated) |
| P-LDG-03: GL at the five largest Salesforce-portal CFs | **NYCT:** Sage Intacct + Salesforce, the target of a migration in progress (medium). **California CF:** Blackbaud Financial Edge (medium). **SVCF:** NetSuite (low, [R] only). **Oregon CF:** none named. **Boston Foundation:** none named; Salesforce CRM and a SmartSimple portal | See §3 |
| **P-ADV-04: NPact owner** | **No public evidence of a sale or recapitalization after the 2022 FIMS purchase.** Signals: (1) BroadWest Partners LLC is still an active Texas franchise taxpayer at NPact's former Dallas suite; (2) Cambria lists NPact with no date or stake, which is consistent with Cambria being a search-fund co-investor in BroadWest's vehicle [I]; (3) Burt Hurlock is now CEO; (4) **new:** NPact's Privacy Policy (updated 2026-01-27) moves the legal address of "Fusion Laboratories, LLC dba NPact" to Wakefield, MA. The owner in 2026 is unconfirmed; my best reading is the BroadWest / search-fund investor group [I] | Low |

## 1. Method

| Step | Source | Notes |
|---|---|---|
| Vendor client lists | Foundation Partners sitemap: 20 pages, including every success story; the client-logo images were downloaded and viewed. Redpath case-study sitemap (28 stories). Sage Intacct (casestudies.com and top10erp). AccuFund. Armanino. Plative. akoyaGO | Clients counted only when the vendor names them, by text or by logo under a heading |
| 990 Part VII-B | [`form990-contractors-harvest-full.csv`](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv), TY2021+ | Every payee matching Foundation Partners, Redpath, Clark Nuber, Armanino, Wipfli, Plative, Fusion/NPact, Foundant, Salesforce, Blackbaud, Sage, AccuFund and others, plus any "software / implementation / technology" service line, for CFs, national sponsors and faith-based sponsors (484 lines reviewed) |
| Job postings | Search for SVCF, OCF, CCF, NYCT, Boston, Minneapolis, Pittsburgh and NCF finance and technology postings naming FE, Intacct, NetSuite, Workday, Dynamics, FIMS or Salesforce. Full-text reads where pages allowed: JobTarget (NYCT), career.com via WebFetch (CCF), the OCF ADP feed, and a TBF PDF | Most job boards returned 403 or 404; those claims are [R] |
| Family counts | Researched rows, plus the remaining portal-layer rows from `cf-ledger-vendors-2026.csv`, plus every `ledger_implied = yes` row in `cf-vendor-map-by-ein.csv` | Assets: DAFRC FY2024 `eoy_daf_assets`. Suite-implied rows carry `confidence = implied` |
| NPact | npact.com About, Terms, Standard Terms and Privacy Policy; Cambria portfolio; Texas Comptroller open data (data.texas.gov dataset 9cir-efmm); privateequityinfo; theorg; search | Massachusetts and Delaware registries not queried (forms and CAPTCHA); left for a human read (P-LSG-03) |

Requests were spaced at about one per second per host.

## 2. P-LDG-04: the Salesforce-centred ledger segment

### 2.1 Ledger families by DAF assets (FY2024)

From [`cf-ledger-families-2026.csv`](../../data/mission-2026-11-14/cf-ledger-families-2026.csv). "Implied" means a suite portal implies the ledger, as recorded in the vendor map [I]. These figures are not separately evidenced.

| Family | Rows | DAF $bn | Confidence mix | Note |
|---|---|---|---|---|
| Foundant CommunitySuite | 360 | 21.54 | implied | Vendor-map suite inference |
| **NetSuite + Salesforce (SF_NETSUITE)** | 3 | **15.56** | low | SVCF $9.58bn, NCF $5.46bn, Pittsburgh $0.53bn (implementing). All [R] postings |
| Unresolved (two candidates) | 6 | 8.95 | low | CCT, FFTC (GiftingNetwork / Give Interactive), GNOF, Minneapolis, CFSEM, Indian River |
| Unknown | 15 | 5.70 | none | Includes Oregon CF, Boston, SFF, CF Texas, OCCF, CICF, Philadelphia and Catholic CF of Minnesota |
| Ren / Stellar iPhi | 21 | 3.30 | implied | Minneapolis moved to unresolved |
| GKCCF self-operated | 1 | 2.57 | medium | — |
| NPact Foundation Cloud | 14 | 2.36 | 13 implied, 1 medium | — |
| **Sage Intacct + Salesforce (SF_INTACCT)** | 4 | **2.32** | 2 high, 2 medium | CFNEF, Arizona CF, Vermont CF, NYCT (migrating) |
| akoyaGO (Dynamics 365) | 48 | 2.13 | implied | akoyaGO reports 30% growth in foundation clients in 2024 ([year in review](https://akoyago.com/?p=32591)) [V] |
| FidTech DonorSphere | 3 | 1.31 | implied | — |
| **Fund 360 / Accounting Seed on Salesforce (SF_NATIVE)** | 5 | **1.20** | 4 high, 1 medium | Maine, JCF San Diego, Bradley Impact Fund, Dayton (+ Depository) |
| Blackbaud Financial Edge | 1 | 1.09 | medium | California CF |
| Microsoft platform | 1 | 0.69 | low | Seattle |
| FIMS / DonorCentral (NPact-owned since 2022) | 6 | 0.34 | implied | The vendor map labels these "Blackbaud". FIMS and DonorCentral were sold to Fusion Laboratories LLC in 2022 ([10-Q](https://www.sec.gov/Archives/edgar/data/1280058/000128005822000055/blkb-20220930.htm)), so these belong to the NPact family [I] |
| **Salesforce + other GL (SF_OTHER)** | 3 | **0.01** | 1 high, 1 medium, 1 low | CF Eastern Washington (QuickBooks), Richmond Jewish Foundation (AccuFund), West Central Initiative (unnamed) |

**Totals.** The file holds 491 rows and $69.1bn. Of that, $62.8bn is CF assets; the 803-row vendor map totals $66.1bn. 315 unmapped CFs and 5 GLM-only CFs are not in the file.

**Reading [I]:**
- **The named Salesforce-centred route is about $3.5bn.** That is the same order of size as Ren ($3.3bn) or NPact including FIMS/DonorCentral ($2.7bn), and about a sixth of Foundant's implied $21.5bn.
- **If the NetSuite evidence at SVCF and NCF were confirmed, Salesforce-plus-ERP ledgers would pass $19bn.** That would make them second only to Foundant by assets, concentrated in a handful of very large sponsors (P-LSG-01).

### 2.2 Sponsor-level evidence (high or medium)

| Sponsor | DAF $m | Family | Ledger statement | Source |
|---|---|---|---|---|
| CF for Northeast Florida | 496 | SF_INTACCT | "customized Salesforce org with donor, grant, and membership portals—creating a single source of truth integrated with Sage Intacct" [V] | [Redpath, datePublished 2024-03-25](https://redpathcg.com/about/case-studies/the-community-foundation-for-northeast-florida). The `/story/` path cited in the wave-10 correction redirects here |
| Arizona CF | 424 | SF_INTACCT | Sage Intacct + Salesforce replacing on-premises Blackbaud FIMS; Clark Nuber implementer [V] | [top10erp copy, 2024-03-06](https://www.top10erp.org/case-study-library/sage-intactt-arizona-community-foundation). **Raised to high:** the case study is dated and names client, ledger and implementer |
| Vermont CF | 146 | SF_INTACCT | "sunsetting Foundation Information Management System (FIMS)… integrated Sage Intacct and Salesforce Experience Cloud". Armanino became the sole partner in May 2024 [R] | [Armanino, 2025-10-20](https://www.armanino.com/case-studies/transforming-nonprofit-technology-for-greater-impact/) (403; search captures). Corroborated by [VCF portal page](https://vermontcf.org/donor-portal/) and 990 Armanino $227k/$243k. **Raised from low to medium** |
| New York Community Trust | 1,255 | SF_INTACCT (target) | "Experience with Sage Intacct, Salesforce, or similar investment/portfolio systems preferred" [F, posting 2026-08-01]. A Project Director posting says the Trust "is transitioning from a legacy Enterprise Resource Planning ("ERP") system to a modern, integrated platform built on Salesforce and Sage Intacct" [R] | [JobTarget](https://www.jobtarget.com/jobs/jt-ytfwftg0iq/director-investment-operations-and-treasury-new-york-city-new-york); [PNY listing](https://philanthropynewyork.org/node/42089) [R] |
| Maine CF | 309 | SF_NATIVE | "Fund 360 package, built entirely within Salesforce", replacing "Raiser's Edge, Financial Edge, and Grant Edge" [V] | [Foundation Partners](https://fdnpartners.com/maine-community-foundation-success-story); 990 TY2023–24 |
| JCF San Diego (Jewish) | 536 | SF_NATIVE | Salesforce + Fund 360 replacing FIMS used "over two decades" [V] | [Foundation Partners](https://fdnpartners.com/jewish-community-foundation-success-story); 990 $215,089 (TY2023) |
| Bradley Impact Fund (national) | 207 | SF_NATIVE | "Fund 360 and Donor 360 solutions, which integrate Accounting Seed with Salesforce"; data moved "from Renaissance PSG and QuickBooks" [V] | [Foundation Partners](https://fdnpartners.com/donor-success-story) |
| Dayton Foundation (+ Depository) | 110 + 42 | SF_NATIVE | Dayton's logo appears under the heading **"Foundations using Fund 360:"** [V] | [fdnpartners.com/products-1](https://fdnpartners.com/products-1) (image `fund360-clients.jpg`); 990 $164,771 (TY2023). **Raised from low [I] to high** |
| Catholic Foundation of Eastern Washington | n/a | SF_OTHER | "Gifts entered into Salesforce sync into QuickBooks automatically"; more than 260 funds; assets "over $53 million" [V] | [Foundation Partners](https://fdnpartners.com/catholic-foundation-of-eastern-washington). Not in DAFRC FY2024 |
| Richmond Jewish Foundation | 10 | SF_OTHER | "AccuFund implemented a customized Accounting Suite and integrated it with Salesforce" [V]; undated | [casestudies.com](https://www.casestudies.com/company/accufund/case-study/developing-personal-relationships-with-donors-required-a-dramatic-technology-upgrade) |

**Fund 360's installed base, as the vendor states it.** The "Foundations using Fund 360" image shows five organisations: Bradley, Dayton, Maine, JCF San Diego and Vancouver Foundation.
- [Vancouver](https://fdnpartners.com/vancouver-foundation) replaced "Foundation Power", used for 25 years.
- [Edmonton CF](https://fdnpartners.com/edmonton-community-foundation) runs Salesforce "integrated with Sage Intacct".
- Both are Canadian and are excluded from the asset counts.

**CRM is not the ledger.** Foundation Partners' separate "valued clients" image ([/foundations](https://fdnpartners.com/foundations)) shows NYCT, Boston, Philadelphia, Marin, CICF, Greater Cincinnati, Cleveland, Columbus, Catholic CF of Minnesota, Northwest Area Foundation and Lumina.
- Several of these have a different ledger on record: Cleveland on Stellar/Ren (990), and Columbus and Greater Cincinnati on Foundant (990 / vendor map).
- So a Salesforce services relationship says nothing about the GL. The edges EM004–EM012 are marked accordingly.

### 2.3 Integrator patterns and faith-based sponsors

**Integrators [V/F]:**
- **Redpath:** CFNEF (Sage Intacct). West Central Initiative ("integrating Salesforce with their accounting and business management application", [2024-05-21](https://redpathcg.com/about/case-studies/west-central-initiative)). SWIF. OCCF (990 $481,100, TY2022).
- **Clark Nuber:** Arizona CF; GNOF ("SOFTWARE IMPLEMENTATION" $115,385, TY2024).
- **Armanino:** Vermont CF. Armanino's [May 2023 CF webinar deck](https://www.armanino.com/-/media/pdf/webinars/2023/donor-portal-software-for-community-foundations.pdf) pitches a Salesforce donor portal and cites "FIMS sunsetting their donor portal". Jewish Federation of Greater Pittsburgh paid Armanino Solutions "DONOR MANAGEMENT SOFTWARE CONSULTANT" $536,465 (TY2024, [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601219349301200_public.xml)) while still paying FidTech $525,587.
- **Wipfli:** Minneapolis Foundation ("ACCOUNTING SERVICES" $328,525 TY2023; "IT SERVICES" $198,709 TY2024) and Thrivent Charitable ("TECHNOLOGY SERVICES" $136,051, TY2023). No Wipfli CF case study found.
- **Plative** (a Salesforce and NetSuite partner, [casestudies.com](https://www.casestudies.com/company/plative)): CF for Southeast Michigan, "CONSULTANT" $1,681,318 (TY2023) and $558,575 (TY2024). The system implemented is not stated.

**Faith-based sponsors:**
- **Named ledgers:** only three, JCF San Diego, Richmond Jewish Foundation and Catholic Foundation of Eastern Washington.
- **Salesforce activity with no GL named:**
  - NCF paid Salesforce Inc $1.17m, $1.13m and $1.36m (TY2022–24) ([TY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513109349303201_public.xml)). An NCF posting [R] lists "NetSuite ERP" as a plus.
  - The Jewish Community Federation of San Francisco ($995m) paid Swift River and Dancecard a combined $724k for "SALESFORCE IMPLEMENTATION CONSULTING" (TY2023).
  - Jewish National Fund pays Addapptation about $477k–487k a year for Salesforce consulting.
  - Catholic CF of Minnesota is a Foundation Partners Salesforce client.

**Salesforce Nonprofit Cloud Accounting Subledger.** I found no 2021+ source showing any CF or faith-based DAF sponsor using it. It prepares gift entries for an external GL ([Accounting Seed explainer](https://www.accountingseed.com/resource/blog/does-salesforce-have-a-nonprofit-accounting-subledger/)) and is not a GL itself.

### 2.4 Exits to the Salesforce-centred route since 2021

| Sponsor | From | To | When | Basis |
|---|---|---|---|---|
| JCF San Diego | FIMS | Fund 360 / Salesforce | c. 2023 [I] (990 FP line TY2023) | [V] |
| Arizona CF | FIMS | Sage Intacct + Salesforce | by 2024-03 (case-study date) | [V] |
| Vermont CF | FIMS / DonorCentral | Sage Intacct + Salesforce | Portal May 2025; Armanino from May 2024 | [F] + [R] |
| Maine CF | Blackbaud RE / FE / Grant Edge | Fund 360 / Salesforce | c. 2023–24 [I] (990 FP lines) | [V] + [F] |
| Bradley Impact Fund | Renaissance PSG + QuickBooks | Fund 360 + Accounting Seed | c. 2022 [I] (990 FP line TY2022) | [V] |
| Pittsburgh Foundation | Blackbaud (NetCommunity portal) [I] | NetSuite + Salesforce | Implementing in 2026 | [R] |
| NYCT | Legacy ERP (unnamed) | Sage Intacct + Salesforce | 3–5-year programme, 2026 | [F] + [R] |

**Not confirmed:**
- **GNOF** (NPact TY2023 versus Clark Nuber TY2024).
- **Minneapolis.** The portal is Ren iPhi, but a posting [R] names "Oracle NetSuite, Salesforce, and/or GiveInteractive".

## 3. P-LDG-03: GL at the five largest Salesforce-portal CFs

| CF | DAF $bn | GL finding | Confidence | Evidence |
|---|---|---|---|---|
| Silicon Valley CF | 9.58 | NetSuite (with Salesforce Experience Cloud portal) | low | Two SVCF postings, both closed and both [R]. Accounting Coordinator: "experience in a NetSuite and BOX environment preferred" ([capture](https://aijobs.app/accounting-coordinator-silicon-valley-community-found-4906816)). Director, Investment Operations: "enterprise business applications such as NetSuite, Salesforce, Asana". The SVCF [Trakstar board](https://siliconvalleycf.hire.trakstar.com/) showed "No jobs available" on 2026-11-15. 990 Slalom $0.63–1.53m a year |
| New York Community Trust | 1.25 | Sage Intacct + Salesforce (migration in progress; legacy ERP unnamed) | medium | §2.2. The domain is now thenytrust.org; the donor portal "MyGrants" vendor remains unidentified ([donor FAQs](https://thenytrust.org/current-donor/donor-faqs/)) |
| Oregon CF | 1.19 | Not named | none | The two current accounting requisitions in OCF's ADP feed (posted 2026-10-26 and 2026-08-07, linked from [oregoncf.org job openings](https://oregoncf.org/about/careers/job-openings)) say only "financial database" |
| Boston Foundation | 1.10 | Not named. Salesforce CRM and SmartSimple portal | none | [TBF payables posting, PDF 2025-06-17](https://www.macdc.org/sites/default/files/jobs/tbf_fund_administration_payables_coordinator.pdf): DAF grants "via Smart Simple portal"; "Experience with Salesforce preferred". The [FY25 audit](https://www.tbf.org/-/media/tbf/files/financial-information/financial-statements/tbf-fy25-audited-financials.pdf) names no system |
| California CF | 1.09 | Blackbaud Financial Edge (with Raiser's Edge), behind a Salesforce portal | medium | [Gift and Fund Financial Services Officer](https://www.career.com/job/california-community-foundation/gift-and-fund-financial-services-officer/j202606080846182943693) (posted 2026-06-25): "experience with Raiser's Edge, Financial Edge, and grantmaking software preferred". Controller posting [R]: "Blackbaud Financial Edge experience is highly desirable" |

**Note on the queue text.** It lists SFF and CF Texas in place of NYCT and Boston. I covered the five named in the task brief. SFF and CF Texas remain "none" in the families file, with no new evidence.

**Effect on portal-layer coverage.** Across the 32 portal-layer rows ($31.0bn: the original 29 plus Arizona, Indian River and Santa Barbara), the ledger is now named at high or medium confidence for **10 rows holding $6.60bn (21%)**.
- Before this pass, the 29-row set had 3 rows and $3.4bn.
- Low-confidence rows: 8, $18.8bn. No evidence: 14 rows, $5.6bn.

## 4. P-ADV-04: who owns NPact (Fusion Laboratories LLC) today?

| Signal | Finding | Source |
|---|---|---|
| 2020 buyout | BroadWest closed the Fusion Labs purchase on 2020-12-30. Jeff Conn and Brian Greeley are named "new NPact co-owners"; no co-investors are named | [Trident release, 2021-04-28](https://www.einpresswire.com/article/539680979/trident-world-ventures-provides-sell-side-advisory-to-fusion-labs) [F] |
| 2022 FIMS purchase | "Fusion Laboratories, LLC" paid about $6.4m in cash. The release quotes "NPact co-CEO Jeffrey Conn" | [Blackbaud 10-Q](https://www.sec.gov/Archives/edgar/data/1280058/000128005822000055/blkb-20220930.htm); [PR Newswire](https://www.prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html) [F] |
| BroadWest still on file | Texas Comptroller active franchise taxpayer: **BROADWEST PARTNERS LLC**, taxpayer 32086573816, 5580 Peterson Ln Ste 200, Dallas 75240. Organisation type "CI", responsibility from 2022-01-01. No Fusion Laboratories or NPact record appears in the same file | [data.texas.gov record](https://data.texas.gov/resource/9cir-efmm.json?taxpayer_number=32086573816) [F] |
| Search-fund model | Axial [R] describes BroadWest as two entrepreneurs seeking one company that will be "our sole investment". Cambria says its principals "invested in over 110 search fund acquired businesses" | [Axial](https://www.axial.net/company/broadwest-partners/) [R]; [Cambria search funds](https://cambriagroup.com/our-approach/search-funds) [F] |
| Cambria listing | NPact has its own portfolio page ("Developer of grant management and donor-advised fund management software… Dallas, TX"). No date, stake or exit shown | [cambriagroup.com/portfolio/npact](https://cambriagroup.com/portfolio/npact) [F] |
| CEO | "Burt Hurlock, Chief Executive Officer". Conn and Greeley are not on the leadership page. Start date not found. Hurlock's earlier roles (Humanyze 2022–23; Azima/Symphony Industrial AI 2008–19) come from an unverified profile | [npact.com/about](https://npact.com/about/) [F]; [theorg](https://theorg.com/org/npact/org-chart/burt-hurlock) [R] |
| **New: legal address** | Privacy Policy (updated 2026-01-27): "Fusion Laboratories, LLC dba NPact, 701 Edgewater Drive, Suite 130, Wakefield, MA 01880". The Terms of Use (2025-07-15) still say "a Delaware corporation"; the Standard Terms (2025-08-26) say "Fusion Laboratories LLC / dba NPact" | [Privacy Policy](https://npact.com/privacy-policy/); [Terms of Use](https://npact.com/terms-of-use/); [Standard Terms](https://npact.com/software-as-a-service-license-and-services-standard-terms/) [F] |
| Aggregators | privateequityinfo: owner "Cambria Group", dates blank. PitchBook (403 here; search capture): "Buyout/LBO" for the 2022 FIMS deal and debt as the latest deal type [R] | [privateequityinfo](https://privateequityinfo.com/directory/private-equity-portfolio-company/3/npact) [3P]; [PitchBook](https://pitchbook.com/profiles/company/64184-68) [R] |
| Sale or recap announcement after 2022 | **None found** in press, NPact news or SEC full text | Searches 2026-11-15 |

**Reading [I]:**
- The pattern fits a search-fund acquisition: two operator-owners, a search-fund investor (Cambria) listing the company, and a later hand-over to an outside CEO. Hand-overs like that are common when searcher-CEOs step back.
- The Massachusetts address may follow the new CEO, but that is not established.
- Nothing public shows a change of control. The 2026 owner should be recorded as **"BroadWest Partners vehicle with search-fund investors including (probably) The Cambria Group; unconfirmed"**.
- A human read of the Massachusetts and Delaware filings for Fusion Laboratories LLC, and of the Texas public information report for BroadWest Partners LLC, would settle it (P-LSG-03).

**Graph:**
- EM033 records BroadWest as acquirer (confirmed, 2020). It supersedes EJ032's `unknown` status, as the wave-11 recommendation asked.
- EM034 records Cambria as investor (inferred).
- EM035 records Hurlock as CEO.

## 5. Limitations

- **990 VII-B lists only the top five contractors above $100k.** Ledger licences often fall below that threshold.
- **Most NetSuite evidence is [R].** Job-board and first-party career pages largely refused scripted reads or had expired.
- **Vendor case studies are often undated.** Go-live dates marked c. are inferred from 990 payment years.
- **Suite-implied families are portal inferences, not ledger evidence.** This applies to Foundant, Ren, akoyaGO, NPact, FIMS/DonorCentral and FidTech.
- **akoyaGO.** Vendor materials mention clients going live "with accounting", but no named list ties individual CFs to akoyaGO's accounting module. All 48 rows therefore stay `implied`.
- **Faith-based coverage is thin.** The vendor map covers CFs only. Faith-based rows here come from vendor pages and the 990 harvest.
- **Massachusetts, Delaware and Texas SOS entity detail** (members, managers, filing history) was not read.

## 6. Source register (accessed 2026-11-15)

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| S1 | Foundation Partners products (Fund 360 logos), products-1, foundations (client logos), success stories, sitemap | vendor [V] | live; © 2025 | https://fdnpartners.com/products-1 ; https://fdnpartners.com/products ; https://fdnpartners.com/foundations ; https://fdnpartners.com/success-stories ; https://fdnpartners.com/sitemap.xml |
| S2 | Foundation Partners stories: Maine, JCF SD, Bradley, Catholic Fdn E. Washington, Vancouver, Edmonton, Augustine Institute | vendor [V] | live | https://fdnpartners.com/maine-community-foundation-success-story ; https://fdnpartners.com/jewish-community-foundation-success-story ; https://fdnpartners.com/donor-success-story ; https://fdnpartners.com/catholic-foundation-of-eastern-washington ; https://fdnpartners.com/vancouver-foundation ; https://fdnpartners.com/edmonton-community-foundation ; https://fdnpartners.com/augustine-institute |
| S3 | Foundation Partners news (Fund 360 "makes Accounting Seed follow fund accounting principles") | vendor [V] | 2024-01-01 | https://www.fdnpartners.com/news.html |
| S4 | Redpath case studies: CFNEF, WCI, SWIF, Catholic Charities | vendor [V] | 2024-03-25; 2024-05-21; 2024-06-14 | https://redpathcg.com/about/case-studies/the-community-foundation-for-northeast-florida ; https://redpathcg.com/about/case-studies/west-central-initiative ; https://redpathcg.com/about/case-studies/southwest-initiative-foundation |
| S5 | Sage Intacct: Arizona CF case study | vendor [V] | 2024-03-06 | https://www.top10erp.org/case-study-library/sage-intactt-arizona-community-foundation ; https://www.casestudies.com/company/sage-intacct/case-study/community-foundation-saves-over-24k-with-sage-intacct |
| S6 | Armanino: VCF case study | vendor [R] | 2025-10-20 | https://www.armanino.com/case-studies/transforming-nonprofit-technology-for-greater-impact/ |
| S7 | Armanino CF donor-portal webinar deck | vendor [V] | 2023-05-16 | https://www.armanino.com/-/media/pdf/webinars/2023/donor-portal-software-for-community-foundations.pdf |
| S8 | AccuFund: Richmond Jewish Foundation | vendor [V] | undated | https://www.casestudies.com/company/accufund/case-study/developing-personal-relationships-with-donors-required-a-dramatic-technology-upgrade |
| S9 | akoyaGO 2024 year in review | vendor [V] | 2024 | https://akoyago.com/?p=32591 |
| S10 | NYCT Director, Investment Operations & Treasury (JobTarget) | posting [F] | 2026-08-01 | https://www.jobtarget.com/jobs/jt-ytfwftg0iq/director-investment-operations-and-treasury-new-york-city-new-york |
| S11 | NYCT Project Director, Digital Innovation; Senior Manager, Finance | posting [R] | 2025–26 | https://philanthropynewyork.org/node/42089 ; https://philanthropynewyork.org/node/41807 |
| S12 | CCF Gift and Fund Financial Services Officer; CCF Controller | posting [F] / [R] | 2026-06-25; undated | https://www.career.com/job/california-community-foundation/gift-and-fund-financial-services-officer/j202606080846182943693 ; https://jobs.recruiter.com/jobs/11051954598-controller-ccf |
| S13 | SVCF Accounting Coordinator; SVCF Trakstar board | posting [R]; ATS [F] | closed; live | https://aijobs.app/accounting-coordinator-silicon-valley-community-found-4906816 ; https://siliconvalleycf.hire.trakstar.com/ |
| S14 | OCF job openings and ADP requisitions | ATS [F] | 2026-08-07; 2026-10-26 | https://oregoncf.org/about/careers/job-openings |
| S15 | Boston Foundation payables posting PDF; Donor Services Manager; FY25 audit | posting / audit [F] | 2025-06-17; 2021-08-24; FY2025 | https://www.macdc.org/sites/default/files/jobs/tbf_fund_administration_payables_coordinator.pdf ; https://app.massnonprofitnet.org/jobs/donor-services-manager ; https://www.tbf.org/-/media/tbf/files/financial-information/financial-statements/tbf-fy25-audited-financials.pdf |
| S16 | Pittsburgh Foundation Systems Solutions Architect | posting [R] | 2026-01-02 | https://pittsburghfoundation.org/systems-solutions-architect |
| S17 | Minneapolis Foundation finance posting | posting [R] | 2026 | https://careers.controllerscouncil.org/job/controller/83227831/ |
| S18 | NCF Local Market Business Analyst | posting [R] | undated | https://jobs.recruiter.com/jobs/11940900967-national-christian-foundation-is-hiring-local-market-business-analyst-in-alphar |
| S19 | 990 Part VII-B lines TY2021–24 | IRS XML [F] | various | per-row URLs in the CSVs; data/mission-2026-11-14/form990-contractors-harvest-full.csv |
| S20 | NPact About, Privacy Policy, Terms of Use, Standard Terms | vendor [F] | live; 2026-01-27; 2025-07-15; 2025-08-26 | https://npact.com/about/ ; https://npact.com/privacy-policy/ ; https://npact.com/terms-of-use/ ; https://npact.com/software-as-a-service-license-and-services-standard-terms/ |
| S21 | Cambria portfolio (NPact) and search-fund page | investor [F] | live | https://cambriagroup.com/portfolio/npact ; https://cambriagroup.com/portfolio?start=192 ; https://cambriagroup.com/our-approach/search-funds |
| S22 | Texas Comptroller Active Franchise Taxpayers (BroadWest Partners LLC) | government open data [F] | file live 2026-11-15 | https://data.texas.gov/resource/9cir-efmm.json?taxpayer_number=32086573816 |
| S23 | Trident World Ventures release; NPact FIMS release; Blackbaud 10-Q | press / SEC [F] | 2021-04-28; 2022-09-12; Q3 2022 | https://www.einpresswire.com/article/539680979/trident-world-ventures-provides-sell-side-advisory-to-fusion-labs ; https://www.prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html ; https://www.sec.gov/Archives/edgar/data/1280058/000128005822000055/blkb-20220930.htm |
| S24 | privateequityinfo; PitchBook; theorg; Axial | aggregators [3P/R] | live | https://privateequityinfo.com/directory/private-equity-portfolio-company/3/npact ; https://pitchbook.com/profiles/company/64184-68 ; https://theorg.com/org/npact/org-chart/burt-hurlock ; https://www.axial.net/company/broadwest-partners/ |
| S25 | Accounting Seed on Salesforce Accounting Subledger | vendor [V] | live | https://www.accountingseed.com/resource/blog/does-salesforce-have-a-nonprofit-accounting-subledger/ |
| S26 | Plative case-study index | vendor [V] | live | https://www.casestudies.com/company/plative |

## 7. Data dictionary

### `data/mission-2026-11-14/cf-ledger-families-2026.csv` (491 rows)

| Column | Meaning |
|---|---|
| `ein` | 9-digit EIN. Blank only for Catholic Foundation of Eastern Washington, which is not in DAFRC and whose EIN was not confirmed |
| `name` | DAFRC name, expanded where truncated |
| `ledger_family` | `SF_NATIVE` (Fund 360 / Accounting Seed inside Salesforce); `SF_INTACCT` (Sage Intacct + Salesforce); `SF_NETSUITE` (NetSuite + Salesforce); `SF_OTHER` (Salesforce + another or unnamed GL); `BLACKBAUD_FE`; `FOUNDANT`; `REN`; `AKOYA` (akoyaGO on Dynamics 365); `NPACT` (Foundation Cloud); `FIMS_DONORCENTRAL` (FIMS / DonorCentral, NPact-owned since 2022-09); `FIDTECH`; `MICROSOFT`; `SELF_OPERATED`; `UNRESOLVED` (two candidates); `UNKNOWN` |
| `product` | Product and integration as evidenced, including the system replaced where stated |
| `evidence_type` | `vendor_case_study`, `vendor_case_study_plus_990`, `vendor_client_logo(_plus_990)`, `job_posting(s)`, `job_posting_snippet(s)`, `990_part_vii_b_contractor`, `990_plus_job_posting_snippet`, `first_party_faq_plus_990`, `privacy_policy_and_audited_statements`, `shared_tenant`, `portal_suite_implied`, or a type carried from `cf-ledger-vendors-2026.csv` |
| `evidence_url` | Primary URL for the ledger call |
| `confidence` | **high:** the vendor or sponsor names the client and the ledger product. **medium:** a first-party posting naming the product, a dated vendor statement read only through captures but corroborated by a 990, an undated vendor case study, or an affiliate on the same tenant. **low:** [R]-only postings or a 990 payee inference. **none:** no ledger evidence. **implied:** ledger inferred from an integrated-suite portal in the vendor map [I] |
| `retrieved` | 2026-11-15 for rows researched or re-checked this pass; carried rows keep their original date |
| `fy2024_daf_assets_usd` | DAFRC FY2024 `eoy_daf_assets` (blank if not in DAFRC) |
| `sponsor_type` | DAFRC `type / subtype` |
| `evidence_detail` | Quotes, 990 amounts, dates and caveats |

### `data/mission-2026-11-14/relationship-graph-edges-additions-13.csv`

- **Edges:** EM001–EM035, with the same columns as `relationship-graph-edges.csv`.
- **New `relationship_type` values:** `ledger_provider` (the system of record for fund accounting) and `executive`.
- **Status:**
  - `confirmed`: a first-party document, a 990 line, or a vendor naming the client.
  - `inferred`: [R]-only text, a job-posting preference, or a search-fund reading.
- **Vendor-logo edges EM004–EM012** record Salesforce services relationships only.

### `data/mission-2026-11-14/queue-proposals-ledger-segment.csv`

- **Proposals:** P-LSG-01 to P-LSG-04, in the format of `queue-proposals-README.md`.

## 8. Corrections to existing repo text

1. **`cf-ledger-vendors-2026.csv`, Dayton rows.** The Dayton Foundation's `ledger_vendor` "Fund 360 … [I]" can drop the [I]: Foundation Partners shows Dayton under "Foundations using Fund 360". Raise confidence from low to high (Depository to medium).
2. **`cf-ledger-vendors-2026.csv`, Arizona CF.** Raise confidence from medium to high. The case study is dated 2024-03-06 and names client, ledger and implementer.
3. **`cf-ledger-vendors-2026.csv`, Vermont CF.**
   - Replace `unknown (pre-May 2025: DonorCentral/NPact stack [I])` with "Sage Intacct + Salesforce Experience Cloud (Armanino), replacing FIMS/DonorCentral [R + F]", confidence medium.
4. **`cf-ledger-vendors-2026.csv`, NYCT, CCF and SVCF.**
   - NYCT: `unknown` becomes "Sage Intacct + Salesforce (migration in progress)", medium.
   - CCF: becomes "Blackbaud Financial Edge", medium.
   - SVCF: becomes "NetSuite [R]", low.
5. **CFNEF citation.** Use `https://redpathcg.com/about/case-studies/the-community-foundation-for-northeast-florida`. The `/story/` URL given in the wave-10 correction now redirects to this path (checked 2026-11-15).
6. **`cf-vendor-map-by-ein.csv`, "Blackbaud (DonorCentral)" rows (6).**
   - The DonorCentral-implied ledger is FIMS, which NPact has owned since 2022-09.
   - Group these rows with NPact for ownership-concentration purposes [I].
7. **EJ032 (BroadWest → Fusion Laboratories).** Status `unknown` is superseded by EM033 (`confirmed`, 2020 close).
