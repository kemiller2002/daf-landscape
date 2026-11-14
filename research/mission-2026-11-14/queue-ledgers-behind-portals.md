# Ledgers behind portal-layer community foundations (P-CFV-01, P-QA1-07, P-CFV-04, P-EXP-04, P-99F-05)

**Date:** 2026-11-14. **Status:** public sources only. I logged in nowhere, submitted no forms and contacted no one. Portal pages and one JavaScript bundle were fetched without credentials, only to read hosts and strings.
**Recency rule:** current-state claims rest on 2021+ evidence: pages live on 2026-11-14, 990 lines for TY2021–2025, or documents dated 2021 or later. One 2017 SEC filing is cited only to explain NRS's current owner.

**Evidence labels** (same as [queue-cf-vendor-map.md](queue-cf-vendor-map.md)):
- **[F]:** first-party. The sponsor's own page, audit, DNS record, shipped code or IRS e-file return.
- **[V]:** a vendor statement or vendor case study.
- **[R]:** a third-party source, such as a company database or a search-index snippet of a page that refused scripted reads.
- **[I]:** my inference.

## Key findings

1. **The ledger is now named for 3 of the 29 portal-layer CFs at high or medium confidence. They hold $3.4bn (11%) of the segment's $30.4bn of FY2024 DAF assets.**
   - **CF for Northeast Florida ($496m):** Sage Intacct behind a Salesforce portal, built by Redpath [V].
   - **Maine CF ($309m):** Foundation Partners' Fund 360, a fund-accounting layer on Salesforce and Accounting Seed [V + F 990].
   - **GKCCF ($2.57bn):** a self-operated platform. GKCCF runs donor-portal.org itself; the GL product behind it is not public [F].
   - **Low-confidence candidates** cover 8 more rows ($8.9bn). These are CCT and FFTC (Give Interactive or GiftingNetwork back office), Seattle (Microsoft), GNOF (NPact or Sage Intacct), Vermont, Dayton ×2 (Fund 360) and West Central.
   - **No evidence** was found for 18 rows ($18.1bn). These include SVCF, NYCT, Oregon CF, California CF, Boston, SFF and CF Texas.
2. **NPact's legal entity is Fusion Laboratories LLC** [F]. NPact's Standard Terms state "Manufacturer is Fusion Laboratories LLC / dba NPact" ([§18](https://npact.com/software-as-a-service-license-and-services-standard-terms/)).
   - **New NPact relationships at portal-layer CFs.** This unlocks four 990 lines:
     - Vermont CF: "consulting", $148,000 (TY2023).
     - GNOF: "implementation services", $118,434 (TY2023).
     - GKCCF: "advising", $151,954 and $152,246 (TY2023–24).
     - Santa Barbara Foundation: "hosted infrastructure", $130,000 (TY2024).
   - **Possible owner.** A [R] database says "Fusion Labs" at NPact's street address was bought by BroadWest Partners on 2021-04-28 ([CB Insights](https://www.cbinsights.com/company/fusion-labs)). This is unverified; see P-LDG-01.
3. **donor-portal.org is GKCCF's own platform, not a vendor (P-CFV-04)** [F].
   - **GKCCF's privacy policy** lists donor-portal.org as one of "the Community Foundation's" Sites. It also covers "back-office clients (Clients)" ([policy, last updated September 2024](https://www.growyourgiving.org/?p=3)).
   - **The portal code** gives support as `support@greaterhorizons.org` and branches on the brands `gkccf` and `gh` (Greater Horizons) ([bundle](https://gkccf.donor-portal.org/assets/index-BmzOrF4D.js)).
   - **GKCCF's 2023 audit** books "back-office accounting services" revenue. Income from services was $1,915,649 in 2023 and $3,035,924 in 2022 ([audit](https://www.greaterhorizons.org/wp-content/uploads/2024/11/Audit-Report-2023.pdf)).
   - **Reading.** Indian River CF's `ircf` tenant makes it a current or former GKCCF back-office client [I].
4. **FundMiner (Fund-Miner) is an overlay, not a ledger** [V].
   - **What it is.** A venture-backed El Paso startup, founded in 2022, that raised $1.725m in June 2023 in a round led by Sonoran Founders Fund, with Techstars and Cascade Seed Fund following ([release](https://www.prnewswire.com/news-releases/fundminer-raises-1-725-million-to-maximize-impact-for-fundraising-organizations-301857550.html)).
   - **Clients named by logo:** Nebraska CF, Paso del Norte, CF for Greater New Haven and Warren County Foundation ([fundminer.com/community](https://www.fundminer.com/community)).
5. **GiftingNetwork is both a portal and a back office** [V].
   - **Its own description:** "Fully outsourced DAF administration, fund accounting, gift acceptance, IRS compliance, and disbursement". It is founder-led, based in Morristown NJ, and says it is "not owned by commercial firms" ([giftingnetwork.com](https://www.giftingnetwork.com/)).
   - **It can sit on someone else's ledger.** At JCF San Diego, JCF's portal "powered by Gifting Network" sits on a Salesforce + Fund 360 ledger that replaced FIMS ([case study](https://fdnpartners.com/jewish-community-foundation-success-story)).
   - **So the CCT and FFTC ledgers cannot be inferred from the portal.**
6. **NRS (P-99F-05)** [F/V].
   - **Ownership and scale.** Northeast Retirement Services is "a wholly owned subsidiary of Community Financial System, Inc. (NYSE: CBU)". It "administers over $1.4 trillion … to over 500 clients" ([nrstpa.com](https://www.nrstpa.com/)).
   - **Relevant services:** "Unitized Accounting for Endowment Administration" and "UPMIFA Reporting", under "Endowment & Foundation" ([services](https://www.nrstpa.com/services)).
   - **No DAF product is described.** It is a unitization and fiduciary back office for asset owners, not a donor portal or CF suite. It is therefore **not a direct Ren or Foundant competitor** [I].
   - **990-visible DAF-sponsor fees:** $787,640 in TY2022 across three sponsors, then only Advisors Charitable Gift Fund (about $107k–$123k a year).
7. **FidTech (P-EXP-04).**
   - **No new tenants or owner found.** The 990-visible fee floor is $1.50m (TY2021, 6 payers), $1.60m (TY2022), $1.56m (TY2023) and $1.25m (TY2024, 5 payers; the MetroWest TY2024 return is not yet in the harvest).
   - **The FidTech homepage** names only the Jewish Federation of Greater Pittsburgh and gives no ownership ([fidtechpartners.com](https://www.fidtechpartners.com/)).

## 1. Method

| Step | Source | Notes |
|---|---|---|
| Universe | The 29 CFs in [`cf-vendor-map-by-ein.csv`](../../data/mission-2026-11-14/cf-vendor-map-by-ein.csv) with `ledger_implied = unknown` and a named portal | $30.36bn FY2024 DAF assets. Arizona CF, Indian River, Santa Barbara and two non-CF reference rows were added where ledger evidence turned up |
| 990 Part VII-B | [`form990-contractors-harvest-full.csv`](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv), TY2021+ | Every non-investment line for the 29 EINs was read. Payees were then traced across the whole harvest (Fusion Laboratories, Foundation Partners, Redpath, Clark Nuber, RSM, VRP, Armanino, GiftingNetwork, FidTech, NRS). Only the top five payees above $100k appear, so this is a floor |
| Vendor sites and case studies | Foundation Partners, Redpath, VRP, Sage Intacct (casestudies.com), FundMiner, GiftingNetwork, NPact terms, NRS, FidTech | Clients counted only when the vendor names them |
| First-party pages | GKCCF privacy policy and 2023 audit, Seattle Foundation FAQ, VCF portal page, donor-portal.org shell, env.js and bundle | No login |
| DNS and certificate transparency | dns.google, crt.sh for donor-portal.org and fund-miner.com | Wildcard certificates hide tenants |
| Job postings | Web search for OCF, SVCF, CCT, NCF finance postings naming Financial Edge, Intacct, FIMS, Workday or NetSuite | None named a GL in visible text (§5) |
| Context | Tech Impact, [*Landscape of Integrated Software for Community Foundations*, July 2022](https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf) | "Large foundations … tend to adopt such tools as NetSuite, Sage Intacct, Salesforce, and SmartSimple". Give Interactive "does not include a full general ledger … preferred partnership and integration with Sage Intacct" |

Requests were rate-limited to no more than one per second per host. Pages that refused scripted reads (Armanino, craft.co, G2, CPA job board, one Dayton news page) were not worked around. Where only search-index text was available, it is marked [R].

## 2. Ledger by portal-layer CF (P-CFV-01)

The full table is [`cf-ledger-vendors-2026.csv`](../../data/mission-2026-11-14/cf-ledger-vendors-2026.csv), with 34 rows. Assets are DAFRC FY2024.

| CF | DAF $bn | Portal | Ledger | Conf. | Key evidence |
|---|---|---|---|---|---|
| Silicon Valley CF | 9.58 | Salesforce | unknown | none | 990: Slalom "consulting" $0.80m / $1.53m / $0.63m (TY2022–24); NaviSite hosting; Deloitte ([TY2023 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413129349304911_public.xml)) |
| Chicago Community Trust | 4.65 | GiftingNetwork | unknown; candidate Give Interactive sub-ledger [I] | low | Give `cct` production certificate 2025-06 to 2026-08 ([crt.sh](https://crt.sh/?q=%25.giveinteractive.com)); Clarity Partners $1.41m / $1.04m (TY2023–24) |
| Foundation for the Carolinas | 2.95 | GiftingNetwork | unknown; candidates Give Interactive and NRS | low | Give Interactive "SOFTWARE" $654,500 (TY2023); NRS "FIDUCIARY SERVICES" $499,715 (TY2022) ([TY2023 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349318318_public.xml)) |
| Greater Kansas City CF | 2.57 | donor-portal.org (GKCCF-operated) | GKCCF self-operated (GL product not public) | medium | Privacy policy and audit (finding 3); RSM "TECHNOLOGY SERVICES" about $0.69–0.77m a year; NPact "advising" |
| New York Community Trust | 1.25 | unidentified | unknown | none | TY2021–24 lines are investment managers and trustees only |
| Oregon CF | 1.19 | Salesforce | unknown | none | 2025–26 accounting postings name no system |
| Boston Foundation | 1.10 | SmartSimple | unknown | none | Ricoh computer support $335,287 (TY2023) only |
| California CF | 1.09 | Salesforce | unknown | none | KPMG and consultants only |
| Marin CF | 0.87 | Salesforce giving site built by VRP (portal newly attributed) | unknown | none | [VRP case study](https://vrpconsulting.com/industries/nonprofit/) "MCF project … giving site … on the Salesforce Platform"; VRP $0.35–0.49m a year (TY2021–24) |
| Seattle Foundation | 0.69 | Power Pages | Microsoft platform (Dynamics not named) [I] | low | [FAQ](https://www.seattlefoundation.org/it-system-upgrade-faqs/): "updating our IT system to the Microsoft 365 platform … new online portal"; RSM "IT SYSTEMS DESIGN & BUILD" $1,625,493 (TY2024) |
| San Francisco Foundation | 0.59 | Salesforce | unknown | none | Xantrion managed IT $651,367 (TY2024) |
| CF Texas | 0.53 | Salesforce | unknown | none | CiviCore "technology provider" $1.03m (TY2021); EPAM; MightyCause |
| Pittsburgh Foundation | 0.53 | Blackbaud NetCommunity | unknown | none | NetCommunity suggests a Blackbaud stack [I], but no GL evidence |
| **CF for Northeast Florida** | 0.50 | Salesforce | **Sage Intacct** | **high** | [Redpath case study](https://redpathcg.com/about/case-studies) (Mar 2024): "customized Salesforce org with donor, grant, and membership portals", integrated with Sage Intacct |
| Orange County CF | 0.47 | Salesforce | unknown | none | Redpath "technology consultant" $481,100 (TY2022) |
| CICF and Indianapolis Foundation | 0.48 | Salesforce | unknown | none | Envista IT; Forvis accounting |
| Greater New Orleans Foundation | 0.34 | Salesforce | unresolved: NPact or Sage Intacct via Clark Nuber [I] | low | Fusion Labs "IMPLEMENTATION SERVICES" $118,434 (TY2023); Clark Nuber "SOFTWARE IMPLEMENTATION" $115,385 (TY2024) |
| **Maine CF** | 0.31 | Salesforce | **Fund 360 (Foundation Partners) on Salesforce / Accounting Seed** | **high** | [fdnpartners.com/products](https://fdnpartners.com/products) names Maine CF; 990 "System Implementation Consultant" $164,378 / $361,674 (TY2023–24) |
| Philadelphia Foundation | 0.15 | Salesforce | unknown | none | EY consulting $1.76m (TY2023) |
| Vermont CF | 0.15 | Salesforce | unknown (pre-May 2025 DonorCentral/NPact) | low | [VCF](https://vermontcf.org/donor-portal/): "In May 2025, we launched a new VCF portal, replacing DonorCentral"; NPact $148k (TY2023); Armanino $227k / $243k (TY2023–24); Armanino case study [R] |
| Dayton Foundation and Depository | 0.15 | Salesforce | Fund 360 [I] | low | Foundation Partners "INFORMATION/TECHNOLOGY SERVICES" $164,771 (TY2023); site notice of a "new accounting system" [R], year not shown |
| Monterey, Commonwealth Charitable Mgmt, SW Initiative | 0.12 | Salesforce | unknown | none | SWIF: Redpath "SALESFORCE SOFTWARE MANAGEMENT" $124,883 (TY2024) |
| West Central Initiative | 0.003 | Salesforce | unknown (Redpath "accounting integrations") | low | Redpath case study |
| Nebraska CF, Paso del Norte | 0.10 | FundMiner | unknown (FundMiner is an overlay) | none | FundMiner integrates "with your financial and CRM systems" [V] |

**Rows outside the 29:**
- **Arizona CF ($424m; portal unmapped by the crawler).** Sage Intacct + Salesforce, which replaced a "legacy, on-premises Blackbaud FIMS system". Implemented by Clark Nuber ([Sage case study](https://www.casestudies.com/company/sage-intacct/case-study/community-foundation-saves-over-24k-with-sage-intacct); undated, live 2026) [V]. Medium.
- **Santa Barbara Foundation.** NPact corroborated by "FUSION LABS INC … HOSTED INFRASTRUCTURE" $130,000 (TY2024). Medium.
- **Indian River CF.** Unresolved between Foundant and the GKCCF back office.

**Reading [I]:**
- **Below about $1bn, a Salesforce portal often means a Salesforce-centred ledger.** In this pass that was either Fund 360/Accounting Seed or Sage Intacct integrated by a regional Salesforce partner (Redpath, Clark Nuber, Armanino). It does not mean Foundant or NPact underneath. At least two FIMS sites (JCF San Diego, Arizona CF) left for this route.
- **The top Salesforce CFs (SVCF, OCF, CCF, SFF, CF Texas) disclose nothing about their GL in public 2021+ material.** Their 990s show only large generalist consultancies.

## 3. P-QA1-07: who built NCF's and SVCF's Salesforce portals

**SVCF.**
- **Builder not confirmed.** The only 2021+ technology payees are Slalom LLC ("CONSULTING SERVICES": $804,435 TY2022, $1,534,430 TY2023, $632,560 TY2024), NaviSite (data services and web hosting, $328,278, TY2022) and Deloitte Financial Advisory ($456,660, TY2023).
- **Why Slalom is plausible [I].** Slalom is a Salesforce partner and built Vanguard Charitable's Salesforce and Experience Cloud stack ([Slalom](https://www.slalom.com/au/en/customer-stories/vanguard-charitable)).
- **What is missing.** No Slalom or Salesforce case study names SVCF.
- **The ledger is unknown.**

**NCF (National Christian Foundation).**
- **Not in the 990 contractor harvest** under any technology payee.
- **The one public posting found** (Asset Management Coordinator) says only "Familiarity with Salesforce is a plus" ([listing](https://talents.vaia.com/companies/national-christian-foundation/alpharetta/asset-management-coordinator-100796777/)).
- **No partner case study** was found. The DonorSphere bundle's `ncf` / `ncfgiving2` app-version entry ([queue-donor-export-cf-payments-donorsphere.md §4](queue-donor-export-cf-payments-donorsphere.md)) is the only vendor trace, and its current meaning is unknown.
- **The builder and the ledger both stay open** (P-LDG-03 covers the method).

## 4. P-CFV-04: donor-portal.org and Fund-Miner

**donor-portal.org [F]:**
- **Hosting:** DigitalOcean nameservers; apex and tenants resolve to 165.245.151.118 (dns.google).
- **Certificates:** Let's Encrypt certificates from 2020-08-29, and wildcard `*.donor-portal.org` from 2021-10-14 ([crt.sh](https://crt.sh/?q=donor-portal.org)). No tenant names are exposed.
- **Apex page:** "To log in, you will need to visit your provider's custom login URL … https://provider.donor-portal.org". The favicon is served from growyourgiving.org (GKCCF's domain).
- **Tenant shell:** a Vite/React app. `env.js` sets the Datadog service `giving_portal_client`. The bundle hard-codes GKCCF and Greater Horizons links, and ACH micro-deposit text (statement descriptor "AMTS").
- **Owner:** GKCCF, together with its controlled affiliate Greater Horizons. The privacy policy and audit are cited in finding 3.
- **Other tenants:** only `gkccf` and `ircf` are known. GKCCF's audit does not name its back-office clients (P-LDG-02).
- **Does it supply the ledger?** For GKCCF itself, yes in the sense that it is GKCCF's own system. The GL product beneath it is not named. RSM's "technology services" ($0.69–0.77m a year) are the largest technology payee [F 990].

**FundMiner** [V]:
- **Company:** a SaaS fund-management and portal overlay. Founded in 2022 by Chelsea Lamego and Alejandro Stevenson-Duran, El Paso TX.
- **Funding:** $1.725m in June 2023, led by Sonoran Founders Fund.
- **Positioning:** "complementary to products that many users already have in place" (Raiser's Edge, PeopleSoft, Salesforce).
- **CF clients by logo:** Nebraska CF, Paso del Norte, CF for Greater New Haven and Warren County Foundation.
- **Paso del Norte launch:** PdNCF announced the portal on 2023-11-17 ([PdNCF](https://pdnfoundation.org/news/pdncf-announces-new-portal-for-funds)).
- **Does it supply the ledger?** **No.** It reads from the client's existing finance system.
- **Certificates:** one certificate name only, `fund-miner.com`, issued 2023-04-20 to 2026-06-07. Tenants sit on path prefixes (`/ncf/`).

## 5. P-EXP-04: FidTech Partners

| Payer (990 VII-B) | Service text | TY2021 | TY2022 | TY2023 | TY2024 |
|---|---|---|---|---|---|
| Jewish Federation of Greater Pittsburgh | Foundation administration | 574,057 | 551,337 | 540,123 | 525,587 |
| Associated Jewish Charities of Baltimore | Investment transaction / accounting services | 335,692 | 383,317 | 325,256 | 302,361 |
| JCF of Greater MetroWest NJ | Software sub-fund accounting / technology services | 265,119 | 264,830 | 290,188 | (not harvested) |
| United Jewish Foundation (Detroit) | Endowment (software) services | 218,424 | 191,949 | 197,516 | 205,940 |
| JEWISHColorado | Financial services / investment management | blank | 102,100 | 103,101 | 111,325 |
| FJC | Info tech support and services | 102,000 | 102,000 | 102,000 | 109,565 |
| **Total (floor)** | | **1,495,292** | **1,595,533** | **1,558,184** | **1,254,778** |

Source: [`form990-contractors-harvest-full.csv`](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv). An example return is the [JFGP TY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601219349301200_public.xml).

**Other clients:**
- **Named by FidTech or the client** [F/V]: Greater Houston CF, Hawai'i CF and Florida United Methodist Foundation. The FUMF move to FoundationHub was targeted for 2026-01-05 ([FUMF](https://fumf.org/news/foundation-launching-new-platform-to-enhance-partner-experience-in-january/)).
- **Delaware CF** is inferred (repo EH edges).

**What remains unknown:**
- **Ownership and revenue.** The homepage names no owner or leadership ([fidtechpartners.com](https://www.fidtechpartners.com/)). The founding year of 2005 is [R].
- **No 2021+ client announcement** was found for the CT-only labels `jpmc` and `mssb`.
- **The 990 floor understates revenue.** Payees under $100k, and sponsors whose top five contractors are larger, are invisible. Houston, Hawai'i and Delaware show no FidTech line.

## 6. P-99F-05: Northeast Retirement Services

- **Owner [F/V].** "A wholly owned subsidiary of Community Financial System, Inc. (NYSE: CBU)", founded 1999 ([nrstpa.com](https://www.nrstpa.com/)). The acquisition closed on 2017-02-03; this is cited only to date the current owner ([SEC 8-K](https://www.sec.gov/Archives/edgar/data/0000723188/000072318817000008/cbna20178kannouncingclosing.htm)).
- **Scope [V].**
  - Non-Profit Asset Services: "Endowment & Foundation", "Unitized Accounting for Endowment Administration" and "UPMIFA Reporting".
  - Global Trust Company (GTC) fiduciary services: collective investment trusts, group trusts and directed trustee services ([services](https://www.nrstpa.com/services)).
  - No donor-advised-fund product is described.
- **DAF-sponsor fees in the 990 harvest, TY2021+ [F]:**

  | Sponsor | Service text | Fees |
  |---|---|---|
  | Advisors Charitable Gift Fund | "Donor Accounting" | $153,859, $128,600, $107,178, $122,697 (TY2021–24) |
  | FFTC | "FIDUCIARY SERVICES" | $499,715 (TY2022) |
  | Winston-Salem Foundation | "ENDOWMENT UNITIZATION" | $159,325 (TY2022) |

  - FFTC and Winston-Salem show no NRS line after TY2022. That is either below the top five or the work ended; it is not established.
- **Reading [I].** NRS is a unitization and recordkeeping back office for pooled assets. It does not provide a donor portal or a grants workflow. It is therefore an input that a sponsor (or Ren or Foundant) could use, not a like-for-like competitor. Its only DAF-specific line is at a small national sponsor.

## 7. Limitations

- **990 Part VII-B shows only the top five contractors above $100k.** Licence fees for a ledger often fall below that, so "no line" is not "no vendor".
- **Vendor case studies [V] are often undated.** Arizona CF's go-live date is not stated.
- **Armanino and Dayton evidence is [R].** It rests on search-index text because the pages refused scripted reads.
- **Payee names are matched on name and city only.** "Fusion Labs Inc" (Santa Barbara) is treated as NPact on the shared Dallas location [I].
- **Job-posting coverage is thin.** Applicant-tracking full texts were mostly unreachable.

## 8. Source register (accessed 2026-11-14)

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| L1 | NPact SaaS Standard Terms §18 | vendor legal [F/V] | updated 2025-08-26 | https://npact.com/software-as-a-service-license-and-services-standard-terms/ |
| L2 | CB Insights, Fusion Labs | database [R] | 2021-04-28 event | https://www.cbinsights.com/company/fusion-labs |
| L3 | PitchBook, NPact (Dallas) | database [R] | live | https://pitchbook.com/profiles/company/64184-68 |
| L4 | Foundation Partners products page | vendor [V] | live | https://fdnpartners.com/products |
| L5 | Foundation Partners news (Fund 360 and Accounting Seed) | vendor [V] | 2024-01-01 | https://www.fdnpartners.com/news.html |
| L6 | Foundation Partners, JCF San Diego story | vendor [V] | (c) 2025 | https://fdnpartners.com/jewish-community-foundation-success-story |
| L7 | Redpath case studies (CF NE Florida, SWIF, WCI) | vendor [V] | 2024 | https://redpathcg.com/about/case-studies |
| L8 | Sage Intacct, Arizona CF case study | vendor [V] | undated, live | https://www.casestudies.com/company/sage-intacct/case-study/community-foundation-saves-over-24k-with-sage-intacct |
| L9 | VRP Consulting nonprofit page (MCF) | vendor [V] | live | https://vrpconsulting.com/industries/nonprofit/ |
| L10 | Armanino VCF case study | vendor [R] | 2025-10-20 | https://www.armanino.com/case-studies/transforming-nonprofit-technology-for-greater-impact/ |
| L11 | VCF donor portal page | CF [F] | live | https://vermontcf.org/donor-portal/ |
| L12 | Seattle Foundation IT upgrade FAQ | CF [F] | 2024 | https://www.seattlefoundation.org/it-system-upgrade-faqs/ |
| L13 | GKCCF privacy policy | CF [F] | 2024-09 | https://www.growyourgiving.org/?p=3 |
| L14 | GKCCF 2023 audited statements | CF [F] | FY2023 | https://www.greaterhorizons.org/wp-content/uploads/2024/11/Audit-Report-2023.pdf |
| L15 | donor-portal.org apex, gkccf env.js and bundle | portal code [F] | live | https://donor-portal.org/ ; https://gkccf.donor-portal.org/env.js ; https://gkccf.donor-portal.org/assets/index-BmzOrF4D.js |
| L16 | crt.sh donor-portal.org; fund-miner.com | CT [F] | 2020– | https://crt.sh/?q=donor-portal.org ; https://crt.sh/?q=fund-miner.com |
| L17 | dns.google donor-portal.org NS and A | DNS [F] | live | https://dns.google/resolve?name=gkccf.donor-portal.org&type=A |
| L18 | FundMiner community page | vendor [V] | live | https://www.fundminer.com/community |
| L19 | FundMiner funding release | vendor [V] | 2023-06-22 | https://www.prnewswire.com/news-releases/fundminer-raises-1-725-million-to-maximize-impact-for-fundraising-organizations-301857550.html |
| L20 | PdNCF FundMiner announcement | CF [F] | 2023-11-17 | https://pdnfoundation.org/news/pdncf-announces-new-portal-for-funds |
| L21 | GiftingNetwork homepage | vendor [V] | live | https://www.giftingnetwork.com/ |
| L22 | Give Interactive homepage | vendor [V] | live | https://www.giveinteractive.com/ |
| L23 | Tech Impact CF software landscape | third party [R] | 2022-07 | https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf |
| L24 | NRS homepage and services | vendor [V] | live | https://www.nrstpa.com/ ; https://www.nrstpa.com/services |
| L25 | Community Bank System 8-K (NRS closing) | SEC [F] | 2017-02-03 | https://www.sec.gov/Archives/edgar/data/0000723188/000072318817000008/cbna20178kannouncingclosing.htm |
| L26 | FidTech homepage | vendor [V] | live | https://www.fidtechpartners.com/ |
| L27 | FUMF FoundationHub announcement | client [F] | 2025 | https://fumf.org/news/foundation-launching-new-platform-to-enhance-partner-experience-in-january/ |
| L28 | Slalom, Vanguard Charitable story | vendor [V] | live | https://www.slalom.com/au/en/customer-stories/vanguard-charitable |
| L29 | 990 Part VII-B lines, TY2021–24 | IRS XML [F] | various | per-row `evidence_url` in the CSVs; harvest at data/mission-2026-11-14/form990-contractors-harvest-full.csv |

## 9. Data dictionary

**`data/mission-2026-11-14/cf-ledger-vendors-2026.csv`** (34 rows: the 29 portal-layer CFs, plus Arizona CF, Indian River, Santa Barbara, and two non-CF reference rows marked in `name`)

| Column | Meaning |
|---|---|
| `ein` | 9-digit EIN |
| `name` | DAFRC name, expanded where truncated |
| `portal_vendor` | Donor-portal product, from the vendor map or as corrected here (Marin, GKCCF) |
| `ledger_vendor` | Fund-accounting or GL system of record. Values are `unknown`, `unresolved: …` (two candidates), or a vendor name. `[I]` marks an inference |
| `evidence_type` | `vendor_case_study`, `vendor_case_study_plus_990`, `990_part_vii_b_contractor`, `first_party_faq_plus_990`, `privacy_policy_and_audited_statements`, `ct_tenant_label_plus_vendor_profile`, `shared_tenant`, `vendor_site`, `job_postings_checked`, `dual_portal_plus_gkccf_policy`, `none_found`, and similar |
| `evidence_url` | Primary URL for the ledger call |
| `confidence` | **High:** the vendor or sponsor names the client and the ledger. **Medium:** first-party evidence of the system without a product name, or an undated vendor case study. **Low:** inference from a 990 payee or a non-primary snippet. **None:** no ledger evidence |
| `retrieved` | 2026-11-14 |
| `fy2024_daf_assets_usd` | DAFRC FY2024 `eoy_daf_assets` |
| `evidence_detail` | Quotes, 990 amounts and caveats |
| `implementer_or_payee` | Integrator or technology payee named in the evidence |

**`data/mission-2026-11-14/relationship-graph-edges-additions-10.csv`:** edges EJ001–EJ032, using the same columns as `relationship-graph-edges.csv`.
- **Status:** `confirmed` means a first-party document or a vendor naming the client. `inferred` means a payee-name match or [R] text. `unknown` means a payee whose role is not stated (Slalom → SVCF) or an [R]-only ownership claim (BroadWest).

**`data/mission-2026-11-14/queue-proposals-ledgers.csv`:** P-LDG-01 to P-LDG-04, in the format of `queue-proposals-README.md`.

## 10. Corrections to existing repo text

1. **`cf-vendor-map-by-ein.csv` and queue-cf-vendor-map.md §3 and §5.**
   - "donor-portal.org (unidentified white-label)" should read **"donor-portal.org, GKCCF / Greater Horizons self-operated portal"**.
   - Its "vendor" share (3.9% of CF DAF assets) is a sponsor-built platform, not a third-party vendor.
2. **Marin CF** `portal_vendor` "unidentified" can be read as **Salesforce, built by VRP Consulting** [V + F 990].
3. **NPact ownership is no longer "[R] only" for every NPact edge.**
   - The NPact legal-entity link (EJ001) is first-party.
   - The Santa Barbara 990 line (EJ005) corroborates EI031.
   - The other `spectrumportal.net` = NPact attributions remain inferred.
