# Community-foundation grant rails and donor portals: top-40 census, CCT layers, Ren ACH network (P-BNK-04, P-VCM-02, P-VCM-01, P-BNK-02)

**Date:** 2026-11-14. **Status:** public pages only. I logged in nowhere, submitted no forms and contacted no one. Login pages were fetched without credentials, only to read their host, title and footer.
**Recency rule:** current-state findings use 2021+ evidence only. Every rail and portal claim below rests on a page that was live on 2026-11-14 or a 2022–2026 filing.

**Evidence labels:**
- **[F]:** first-party (the foundation's or vendor's own live page or document, or an IRS e-file return).
- **[V]:** vendor statement about its own clients.
- **[R]:** third-party or search-index summary that I could not open first-hand.
- **[I]:** my inference.
- **[U]:** unknown.

**Data written:**
- [`data/mission-2026-11-14/community-foundation-rails-portals-2026.csv`](../../data/mission-2026-11-14/community-foundation-rails-portals-2026.csv): 40 rows, the top 40 community foundations by FY2024 DAF assets.
- [`data/mission-2026-11-14/relationship-graph-edges-additions-7.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-7.csv): edges EG001–EG028. 26 are confirmed and 2 inferred.
- [`data/mission-2026-11-14/queue-proposals-cf-rails.csv`](../../data/mission-2026-11-14/queue-proposals-cf-rails.csv): proposals P-CFR-01 to P-CFR-05.

**Universe.** I took DAFRC rows with `type = Community Foundation` and `fiscal_year_end = 2024`, ranked by `eoy_daf_assets` ([dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo copy `dafrc-sponsor-schedule-d-fy2019-2024.csv`).
- This list differs from the one used in the P-VCM-02 queue text. That text named Dallas, CICF, Kalamazoo and Greater Memphis.
- On this ranking, Greater Memphis is #16, CICF is #81, The Dallas Foundation is #102 and Kalamazoo is #209. Dallas Jewish CF is classed "Single Issue Charity".
- The census therefore covers the 40 listed in the CSV.

---

## 0. Headline answers

| Item | Answer | Confidence |
|---|---|---|
| **P-BNK-04: rails at the 30 largest community foundations** | **The community-foundation segment runs mostly on its own ACH, and much of it is still undocumented.** Of the top 30 (details in §2):<br>- **10 document their own ACH or electronic payment**, with no provider named: Oregon, California CF, Greater Houston, Denver, Seattle, SFF, Minneapolis, CFT, Pittsburgh and NE Florida.<br>- **2 use a named third-party rail:** Chariot at Saint Paul & Minnesota (moving "this fall"), and Bill.com at CF Greater Atlanta.<br>- **2 are check-only:** Chicago Community Trust (DAF grants are mailed checks), and New Hampshire, whose checks are printed by Citizens Bank's Checkmint.<br>- **1 is unverified:** Greater Cincinnati, whose ACH form URL now redirects.<br>- **15 publish nothing.**<br>- **PayPal Grant Payments and Ren ACH: zero.**<br>- **Seattle is the only one that makes ACH mandatory.** It has done so from 2026-06-30.<br>- **Only Denver, Minneapolis, CCT and Louisville (#34) say explicitly that the rail applies to DAF grants.** The others describe "grant payments" generally. | Each rail [F]; DAF coverage mostly [U] |
| **P-VCM-02: GiftingNetwork census, top 40** | **GiftingNetwork runs only at CCT and FFTC** (plus FFTC's affiliate FCJC). All 40 sites were attempted, and the portal layer was identified for 34 of them (§3):<br>- **Foundant CommunitySuite: 13**<br>- **Salesforce Experience Cloud: 6**<br>- **Ren/Stellar iPhi: 5**<br>- **NPact Foundation Cloud (spectrumportal.net): 3**<br>- **GiftingNetwork: 2**<br>- **One each:** DonorSphere, Blackbaud NetCommunity, SmartSimple, Akoya GOfund and Microsoft Power Pages.<br>- **3 unidentified custom portals:** GKCCF, NYCT and Marin.<br>- **3 not resolvable:** OC-CF, Arizona and North Texas. | [F] per row; GiftingNetwork absence [F within coverage] |
| **P-VCM-01: CCT layers** | **Unresolved, but narrowed.**<br>- **GiftingNetwork is the documented donor front end** (2024-02 and 2025-12 documents), and DAF grants are paid by **mailed check** [F].<br>- **Give Interactive's `cct` tenant is configured for production** with CCT's own Okta SSO (`cct-prod-okta`, Cognito pool `give-cct-prod`). Its sandbox and staging certificates were renewed 2026-09-01 [F].<br>- **No CCT page links to Give.** CCT's FYE 9/2026 990 is not filed yet.<br>- **Ledger vendor:** [U]. | Layers [F]; Give role [U] |
| **P-BNK-02: Ren's "ACH once" network** | **Ren now claims "25+ donor-advised fund programs at once" but names none** ([Ren help, July 2026](https://intercom.help/rengiving/en/articles/6229556-ren-for-charities-overview)) [V].<br>- **Sponsor confirmations:** AEF only [F]. RCF says grants are "delivered electronically or by check" without naming the rail [F].<br>- **BofA CGF:** still check-only in its Feb 2026 guide [F].<br>- **Ren's own iPhi community-foundation clients do not visibly use it.** SPMF, on iPhi, chose Chariot [F]. Minneapolis pays electronically through an unnamed provider [F]. | [V]/[F] |

---

## 1. Method

1. **Home-page crawl.** I fetched each foundation's home page with a browser-like User-Agent, followed links whose anchor or URL matched login, portal, fundholder, nonprofit, ACH or payment, and fingerprinted the portal hosts.
   - With proper headers, **36 of 40** home pages returned 200. Only CCT and Pittsburgh (Cloudflare challenge) and Arizona (empty reply) refused.
   - Two foundations' domains had changed: SPMF is now `spmcf.org` and GiveWell is `givecf.org`.
2. **Sitemap scan.** For each site I read the sitemap and searched URLs for `ach`, `payment`, `eft`, `chariot`, `faq` and similar.
3. **WebFetch and web search** for the blocked sites (CCT, Pittsburgh, Arizona) and for domain-restricted searches on ACH or electronic grant payments.
4. **990 contractor lines**, FY2021+, from the repo harvest ([form990-contractors-harvest-full.csv](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv)).
5. **Certificate-transparency logs** ([crt.sh](https://crt.sh/); [certspotter](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names)). Public `config.js` files on vendor hosts were read only for product and tenant names; no credentials were used.

---

## 2. P-BNK-04: grant-payment rails, top 30

| # | Foundation | FY2024 DAF assets | Rail | Provider | DAF grants covered? | Source |
|---|---|---|---|---|---|---|
| 1 | Silicon Valley CF | $9.58bn | not found | — | — | [grant FAQ](https://www.svcf.org/nonprofits/grant-faq) has no payment rail |
| 2 | Chicago Community Trust | $4.65bn | **check** | none | **Yes**: "Checks are then mailed to the charitable grant recipient within five and seven business days" | [CCT Donor Portal FAQ](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf) (PDF created 2025-12-02) [F] |
| 3 | Foundation For The Carolinas | $2.95bn | not found | — | — | [FAQ](https://www.fftc.org/faqs) |
| 4 | Greater Kansas City CF | $2.57bn | not found | — | — | ACH appears only for contributions ([agency funds](https://growyourgiving.org/agency-fund-holders)) |
| 5 | Columbus Foundation | $1.33bn | not found for DAF grants | — | — | Giving Store "Credit card gifts are distributed electronically, via direct deposit" ([portal FAQ](https://columbusfoundation.org/nonprofit-center/nonprofit-portal-resource-center)) [F] |
| 6 | New York Community Trust | $1.25bn | not found | — | — | [nonprofit FAQ](https://thenytrust.org/nonprofits/nonprofit-faqs/) |
| 7 | Oregon CF | $1.19bn | own ACH, "on some grants" | own | not stated | [OCF](https://oregoncf.org/ach-grant-payments) [F] |
| 8 | Boston Foundation | $1.10bn | not found | — | — | — |
| 9 | California CF | $1.09bn | own ACH: "we are happy to offer future payments via ACH electronic fund transfer" (form at calfund.org/ach, which returned 502) | own | not stated | [grant report page](https://connect.calfund.org/GrantDisbursementReport) [F] |
| 10 | CF Greater Atlanta | $1.06bn | **Bill.com**: "any partner or grantee accepting a grant from us in the future will receive electronic payment processing through Bill.com" | Bill.com | not stated | [grant opportunities](https://cfgreateratlanta.org/grant-opportunities/) [F] |
| 11 | Greater Houston CF | $0.92bn | own ACH | own | not stated | [GHCF](https://ghcf.org/articles/why-ach-grant-payments-benefit-nonprofits/) [F] (carried from the bank-programs pass) |
| 12 | Marin CF | $0.87bn | not found | — | — | — |
| 13 | CF New Jersey | $0.82bn | not found | — | — | [grants FAQ](https://cfnj.org/cfnj-grants-faqs/) |
| 14 | Denver Foundation | $0.73bn | **check or ACH** | own | **Yes**: TDF Fund Manager status "Paid/Complete – The Denver Foundation has paid the grant and sent the payment to the grantee via USPS mail, or ACH electronic payment" | [Fund Manager guide](https://denverfoundation.org/fundmanager/) [F] |
| 15 | San Diego Foundation | $0.71bn | not found | — | — | [nonprofit FAQ](https://www.sdfoundation.org/nonprofits/nonprofit-faqs/) |
| 16 | CF Greater Memphis | $0.69bn | not found | — | — | — |
| 17 | Tulsa CF | $0.69bn | not found | — | — | [FAQ](https://tulsacf.org/faqs/) |
| 18 | Seattle Foundation | $0.69bn | **own ACH, mandatory**: "Effective June 30, 2026, organizations must be enrolled in ACH Transfer to receive future grant payments" | own | implied (all grant payments). Its [donor FAQ](https://www.seattlefoundation.org/philanthropists/faqs/) still says "checks are cut within a week" | [EFT enrolment](https://www.seattlefoundation.org/seafdn-eft-enrollment/) [F] |
| 19 | Minneapolis Foundation | $0.60bn | **check and electronic** | not named | **Yes**: DonorView FAQ, "For electronic payments, this also means that the funding has been distributed to the grant recipient's bank account" | [DonorView FAQ](https://www.minneapolisfoundation.org/donorview-faq/) [F] |
| 20 | San Francisco Foundation | $0.59bn | own ACH preferred: "prefers to make grant payments as direct deposits (ACH)"; one-time DocuSign set-up | own | not stated | [SFF](https://sff.org/what-we-do/funding/enroll-in-direct-deposit-ach-grant-payments/) [F] |
| 21 | CF Tampa Bay | $0.59bn | not found | — | — | — |
| 22 | Saint Paul & Minnesota Foundation | $0.58bn | **Chariot**: "We are adopting Chariot …"; enrolment optional, otherwise "you can still receive grant payments by check"; transition "this fall" | Chariot Disbursements | probable: Chariot is described as letting "foundations and donor-advised fundholders … send grants electronically" | [SPMF Chariot FAQ](https://spmcf.org/nonprofits/grant-resources/chariot-electronic-grant-payments-faqs) [F] |
| 23 | Communities Foundation of Texas | $0.53bn | own ACH ("Payment ACH enrollment form") | own | not stated | [financials page](https://www.cftexas.org/about-cft/financials-investments/) [F] |
| 24 | East Bay CF | $0.53bn | not found | — | — | — |
| 25 | Pittsburgh Foundation | $0.53bn | own ACH opt-in: "The grants team has shifted from issuing paper checks and letters to electronic payment"; banking details at pittsburghfoundation.org/ach | own | not stated (Wish Book program page) | [Wish Book FAQ](https://pittsburghfoundation.org/wish-book-faqs) [F, via WebFetch] |
| 26 | Omaha CF | $0.52bn | not found | — | — | — |
| 27 | Greater Cincinnati Foundation | $0.50bn | **unverified**: the search index shows an "ACH Authorization and Enrollment" form at gcfdn.org/ach | own [R] | — | [gcfdn.org/ach](https://www.gcfdn.org/ach/) redirects to the home page on 2026-11-14 |
| 28 | GiveWell CF | $0.50bn | not found | — | — | — |
| 29 | CF Northeast Florida | $0.50bn | own ACH: "converting most nonprofit grantees to ACH payment"; ACH authorisation form (Operations 2025-09, uploaded 2026/07) | own | not stated | [portal post](https://www.jaxcf.org/introducing-the-grantee-portal-a-one-stop-shop-for-nonprofits-seeking-support/); [form](https://www.jaxcf.org/wp-content/uploads/2026/07/TCF-ACH-Authorization-Form_Operations-2025-09.pdf) [F] |
| 30 | New Hampshire Charitable Foundation | $0.49bn | **check only**, outsourced: "moving to an automated check payment service: Checkmint by Citizens Bank" | Citizens Bank (check printing) | not stated | [NHCF FAQ](https://www.nhcf.org/how-can-we-help-you/apply-for-a-grant/frequently-asked-questions/) [F] |

**Beyond the top 30, found during the census:**
- **Greater Washington CF (#38): Blackbaud REPAY**, live since September 2026. "ACH is the default method". If REPAY does not receive the set-up form within one business day, "they will issue the grant or payment by check" ([nonprofit FAQ](https://www.thecommunityfoundation.org/nonprofit-faqs); [portal launch](https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived)) [F].
- **Louisville (#34): check.** "The Foundation sends checks directly to nonprofits" ([FAQ](https://www.cflouisville.org/faqs/)) [F].
- **Rhode Island (#35): own ACH**, through an access-code "ACH Submission" page ([RIF](https://rifoundation.org/about/your-community-foundation/connect/grantee-authorize)) [F].

**Reading [I]:**
- **Rails at community foundations are mostly built in house.** They use the foundation's own bank ACH, with banking details collected by form, DocuSign, Formstack or portal. They do not use the DAF-specific EFT networks: none of the top 30 uses PayPal Grant Payments or Ren ACH.
- **Third-party rails are general accounts-payable tools** (Bill.com, Blackbaud REPAY, Citizens Checkmint), with Chariot as the one DAF-native exception.
- **The trend is toward ACH by default:**
  - Seattle made it mandatory.
  - CF Northeast Florida is "converting most" grantees.
  - Pittsburgh has "shifted" to electronic payment.
  - GWCF made ACH the default.
- **One counter-move:** NHCF outsourced check printing.
- **What this means for Chariot:** each community foundation that moves needs its own grantee enrolment. Chariot's pitch to grantees ("a single Chariot account", quoted in the [SPMF FAQ](https://spmcf.org/nonprofits/grant-resources/chariot-electronic-grant-payments-faqs)) answers this fragmentation directly.

---

## 3. P-VCM-02: donor-portal census, top 40

The portal signature checked is the GiftingNetwork pattern: `/m/login`, `/ma/images/logo_xs.png` and the footer "Powered by GiftingNetwork".

| Portal layer | Count | Foundations (rank) and evidence |
|---|---|---|
| **GiftingNetwork** | 2 | **CCT (#2):** [donorportal.cct.org/m/login](https://donorportal.cct.org/m/login), footer "Powered by GiftingNetwork", `/ma/images/logo_xs.png`.<br>**FFTC (#3):** [daf.fftc.org/m/login](https://daf.fftc.org/m/login), plus fcjc.fftc.org. |
| **Foundant CommunitySuite** (`*.fcsuite.com/erp/…`) | 13 | Columbus (#5, [columbusfdn.fcsuite.com](https://columbusfdn.fcsuite.com/erp/portal)); CF Greater Atlanta (#10, [cfga.fcsuite.com](https://cfga.fcsuite.com/erp/fundmanager/list)); CFNJ (#13, [cfnj.fcsuite.com](https://cfnj.fcsuite.com/erp/fundmanager)); Denver (#14, [denver.fcsuite.com](https://denver.fcsuite.com/erp/fundmanager)); Tampa Bay (#21, [cftampabay.fcsuite.com](https://cftampabay.fcsuite.com/erp/portal)); Omaha (#26, [login page](https://omahafoundation.org/login/)); Greater Cincinnati (#27, [gcfdn.fcsuite.com](https://gcfdn.fcsuite.com/erp/portal)); GiveWell (#28, [login page](https://www.givecf.org/login/)); NHCF (#30, [nhcf.fcsuite.com](https://nhcf.fcsuite.com/erp/portal)); CF Middle Tennessee (#32, [cfmt.fcsuite.com](https://cfmt.fcsuite.com/erp/portal)); Rhode Island (#35, [donor portal page](https://rifoundation.org/giving/give-well/donorportal)); St. Louis (#39, [donor services](https://stlgives.org/donors/donor-services/)); Richmond (#40, [tcfrichmond.fcsuite.com](https://tcfrichmond.fcsuite.com/erp/portal/list)) [F] |
| **Salesforce Experience Cloud** | 6 | SVCF (#1, [donor.siliconvalleycf.org/s/](https://donor.siliconvalleycf.org/s/), which returns an `x-sfdc-trace-flags` header); Oregon (#7, [oregoncf.my.site.com](https://oregoncf.my.site.com/MyOCF_login)); California CF (#9, [my.site.com](https://californiacommunityfoundation.my.site.com/s/login/)); SFF (#20, [tsff.my.site.com/donorcenter](https://tsff.my.site.com/donorcenter/s/)); CFT (#23, links to communitiesfoundationoftexas.my.site.com on its [portal page](https://www.cftexas.org/portal-login/)); NE Florida (#29, [myfund.jaxcf.org/s/](https://myfund.jaxcf.org/s/), with Sfdc markup) [F] |
| **Ren (Stellar) iPhi** | 5 | Greater Memphis (#16, [cfgm.iphiview.com](https://cfgm.iphiview.com/cfgm/LogIn/tabid/444/Default.aspx)); Minneapolis (#19, [tmf.iphiview.com](https://tmf.iphiview.com/tmf/)); SPMF (#22, [spmf.iphiview.com](https://spmf.iphiview.com/spmf/), "DonorView Portal"); Cleveland (#31, [iphiview.com/tcf](https://www.iphiview.com/tcf/)); Louisville (#34, [cfl.iphiview.com](https://cfl.iphiview.com/cfl/)) [F] |
| **NPact Foundation Cloud** (`*.spectrumportal.net`) | 3 | San Diego (#15, [sdfoundation.spectrumportal.net](https://sdfoundation.spectrumportal.net/)); Tulsa (#17, [tcf.spectrumportal.net](https://tcf.spectrumportal.net/accounts/signin)); GWCF (#38, [thecommunityfoundation.spectrumportal.net](https://thecommunityfoundation.spectrumportal.net/accounts/signin)).<br>GWCF itself names the product "Foundation Cloud Community Portal" ([GWCF](https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived)) [F]. That NPact makes it rests on third-party sources ([TrustRadius](https://www.trustradius.com/products/npact-foundation-cloud/details); NPact bought FIMS and DonorCentral NXT from Blackbaud, [PR Newswire](https://prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html)) [R] |
| **DonorSphere** | 1 | Greater Houston (#11, [ghcf.donorsphere.org](https://ghcf.donorsphere.org/login), bundle string "Powered by DonorSphere®") [F] |
| **Blackbaud NetCommunity** | 1 | Pittsburgh (#25). [community.pittsburghfoundation.org](https://community.pittsburghfoundation.org/pages/frequently-asked-questions) carries `BLACKBAUD.netcommunity` markers [F]. DonorSphere's shared config also lists a `pgh` tenant ([config](https://ghcf.donorsphere.org/config/googleAnalyticsIDs.js)), which suggests a possible migration [I] |
| **SmartSimple** | 1 | Boston (#8, "Donor Portal" links to [bostonfoundation.smartsimple.com](https://bostonfoundation.smartsimple.com/)) [F] |
| **Akoya GOfund** | 1 | East Bay (#24, [gofund.akoyago.com/eastbay](https://gofund.akoyago.com/eastbay)) [F] |
| **Microsoft Power Pages** | 1 | Seattle (#18, [seattlefoundation.powerappsportals.com](https://seattlefoundation.powerappsportals.com/donors/)) [F] |
| **Unidentified custom portal** | 3 | GKCCF (#4): [gkccf.donor-portal.org](https://gkccf.donor-portal.org/login), a React app called "giving_portal_client" that loads Stripe JS. Its brand fallback is `donor-portal.org`, whose wildcard certificate dates from 2026-08-22 ([crt.sh](https://crt.sh/?q=%25.donor-portal.org)).<br>NYCT (#6): MyGrants on ASP.NET ([mygrants.thenytrust.org](https://mygrants.thenytrust.org/Account/Login)).<br>Marin (#12): Angular app "mcf-client" ([givingcenter.marincf.org](https://givingcenter.marincf.org/login)). |
| **Not resolvable** | 3 | OC-CF (#33): [donor.oc-cf.org](https://donor.oc-cf.org/) returned 503.<br>Arizona (#36): [site](https://www.azfoundation.org/access-your-fund/) returned an empty reply.<br>CF North Texas (#37): "DonorCentral Login" points to [edonorcentral.com/login_0487.asp](https://www.edonorcentral.com/login_0487.asp), which returns 404. The same cfntx.org page also carries a spam "LOGIN" link to an unrelated gambling domain, which suggests the site is compromised. |

**Bottom line [F within coverage]:**
- **GiftingNetwork holds 2 of 40** top community-foundation donor portals, worth $7.6bn of FY2024 DAF assets between them.
- **Foundant CommunitySuite is the modal platform at 13 of 40**, but it sits mainly at ranks 5–40. The top two are elsewhere.
- **No reachable top-40 site links to a Give Interactive host.**
- **Ren/Stellar iPhi is the donor web at 5 of 40.**
- **990 corroboration:** Foundant appears as a 990 payee at Columbus ($344,614), CF Greater Atlanta ($270,407) and Denver ($158,850). Stellar appears at Greater Memphis ($203,119) and Cleveland ($416,391) ([harvest](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv); e.g. [Cleveland XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349305969_public.xml)) [F].

**Ledger layer where known:**
- **Explicit:** GWCF uses Blackbaud Financial Edge NXT ([GWCF update](https://www.thecommunityfoundation.org/news/an-update-on-our-technology-transformation-what-fundholders-need-to-know)) [F].
- **Likely [I]:** CommunitySuite sites run Foundant as their ERP, since the portal path is `/erp/`.
- **Mixed stack at Minneapolis:** Give Interactive staging and SFTP tenants sit beside an iPhi front end (repo edge EA009).
- **Elsewhere:** unknown.

---

## 4. P-VCM-01: which layer each vendor runs at Chicago Community Trust

| Layer | Evidence (2026-11-14) | Reading |
|---|---|---|
| Donor front end | [donorportal.cct.org/m/login](https://donorportal.cct.org/m/login): "Powered by GiftingNetwork" [F].<br>The [user guide](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-User-Guide.pdf) (created 2025-12-02) says "Powered by The GiftingNetwork, Donor Portal is a full-service platform" [F].<br>An older guide, `DonorPortalUserGuide.pdf`, was created 2024-02-06 (validation wave 6, V6-08).<br>The live donor-portal certificate was reissued 2026-09-27 ([crt.sh](https://crt.sh/?q=donorportal.cct.org)). | GiftingNetwork is the incumbent donor layer [F] |
| DAF grant payment | FAQ: "reviews and approves grant recommendations twice per week. Checks are then mailed … within five and seven business days" ([FAQ](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf)) [F].<br>The CCT DAF brochure (May 2026) says "The Trust will issue payment to the nonprofit organizations you recommend … and maintain all financial recordkeeping" ([brochure](https://www.cct.org/wp-content/uploads/2026/05/IntrotoDAFs_5.20.26.pdf)) [F]. | Paid by mailed check. Recordkeeping is in house; the software is not named |
| Give Interactive tenant | `cct.giveinteractive.com` serves the Give app (an unknown subdomain gives no answer).<br>Its public [config.js](https://cct.giveinteractive.com/config.js) decodes to `VITE_ALTERNATE_IDP_APP_CLIENT_NAME = cct-prod-okta` and Cognito domain `give-cct-prod.auth.us-west-2.amazoncognito.com` [F].<br>`cct-sandbox` and `cct-staging` certificates were issued 2026-09-01 ([certspotter](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names)) [F].<br>For comparison, WaterStone (`ws-prod-entra`) and The Signatry (`signatry-prod-okta`) have the same pattern; ImpactAssets still points to `give-dev-okta`. | A production tenant, wired to CCT's corporate identity provider and still under active development. **An enterprise IdP is standard for Give tenants, so it does not show whether staff or donors use it** [I] |
| 990 | FYE 9/2025: 40 contractors above $100k, listed floor $735,318. Neither vendor appears ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202632239349302058_public.xml)) [F]. FYE 9/2026 is not filed yet. | No new evidence |
| Search for any naming | A web search for CCT with "Give Interactive", "GiftingNetwork" or "FIMS" found nothing that names a vendor. | — |

**Reading [I]:**
- **Ruled out:** an *imminent* donor-facing cut-over to Give. The GiftingNetwork documents were refreshed in December 2025 and the GiftingNetwork certificate in September 2026.
- **Two readings remain:**
  - Give runs back-office or ledger functions (GiftingNetwork advertises compatibility with "FIMS, FoundationPower, and any third-party XML client", [GiftingNetwork](https://www.giftingnetwork.com/portals.html)).
  - Or Give is a long-running replacement project.
- **I cannot choose between them.** Proposal P-CFR-05 sets a watch.

---

## 5. P-BNK-02: Ren's "sign up for ACH once" network

| Program | Evidence | Shares Ren ACH? |
|---|---|---|
| Ren (vendor) | "Charities sign up for ACH once and are digitally enabled for every DAF program we support" ([Ren payments](https://www.reninc.com/payments/)) [V].<br>Help centre: "enroll in ACH grants from 25+ donor-advised fund programs at once" ([overview, July 2026](https://intercom.help/rengiving/en/articles/6229556-ren-for-charities-overview)) [V].<br>Grants made outside Ren's own engine show as "Legacy" payments ([charity grants](https://intercom.help/rengiving/en/articles/6232128-charity-grants)).<br>"ACH reissuance is only possible if the donor allows payment flexibility" ([reissue](https://intercom.help/rengiving/en/articles/13123383-what-should-i-do-if-i-have-issues-with-receiving-a-grant-check-or-need-to-request-a-reissue)) [V].<br>The Nov 2026 release adds donor-initiated "ACH request" emails to charities ([Nov 2026](https://intercom.help/rengiving/en/articles/17828016-2026-november-release)) [V]. | Program list not published |
| American Endowment Foundation | "Our Charity Portal is now live. Powered by Ren, charities can claim their organization, provide ACH information" ([AEF](https://www.aefonline.org/charities/)) [F] | **Yes** [F] |
| Renaissance Charitable Foundation | Grant timing depends on "whether funds are delivered electronically or by check" ([RCF FAQ](https://renaissancecharitable.org/faqs/)) [F] | Electronic payment exists; Ren ACH not named. Likely [I] |
| BofA Charitable Gift Fund | The 2024 guidelines are check-only (repo, V6-02). The [Navigating guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf) (modified 2026-02-23) describes only check fields ("This name will appear on the check") [F]. 2025 and 2026 guideline PDFs return 404. | **No evidence of participation**; check-only on current documents |
| Morgan Stanley GIFT | ACH is claimed and disbursement is assigned to Ren (repo, V6-01). | Likely [I]; not confirmed |
| Ren iPhi community foundations | SPMF (iPhi) uses **Chariot** ([FAQ](https://spmcf.org/nonprofits/grant-resources/chariot-electronic-grant-payments-faqs)).<br>Minneapolis (iPhi) pays electronically with no provider named ([DonorView FAQ](https://www.minneapolisfoundation.org/donorview-faq/)).<br>Louisville (iPhi) pays by check ([FAQ](https://www.cflouisville.org/faqs/)). | **No** at SPMF and Louisville; [U] at Minneapolis, Cleveland and Memphis |

**Reading [I]:** Ren's ACH network is a feature of Ren's **disbursement engine** (RDE), not of its iPhi donor web. Community foundations that license iPhi pay grants from their own systems, and SPMF picked Chariot. The "25+ programs" are most likely RCF's white-label programs plus AEF, which have moved onto Ren's full stack. That has not been verified (P-CFR-04).

---

## 6. Source register (accessed 2026-11-14)

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| S1 | DAFRC FY2024 dataset (repo copy) | dataset | Spring 2026 | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx |
| S2 | CCT Donor Portal FAQ | CF doc | 2025-12-02 | https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf |
| S3 | CCT Donor Portal User Guide | CF doc | 2025-12-02 | https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-User-Guide.pdf |
| S4 | CCT DAF brochure | CF doc | 2026-05-20 | https://www.cct.org/wp-content/uploads/2026/05/IntrotoDAFs_5.20.26.pdf |
| S5 | Give `cct` tenant config | vendor host | live | https://cct.giveinteractive.com/config.js |
| S6 | certspotter giveinteractive.com | CT log | 2026-09-01 issuances | https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names |
| S7 | SPMF Chariot FAQ | CF web | fall 2026 | https://spmcf.org/nonprofits/grant-resources/chariot-electronic-grant-payments-faqs |
| S8 | CFGA grant opportunities (Bill.com) | CF web | live | https://cfgreateratlanta.org/grant-opportunities/ |
| S9 | GWCF nonprofit FAQ (REPAY) | CF web | Sept 2026 | https://www.thecommunityfoundation.org/nonprofit-faqs |
| S10 | GWCF portal launch | CF web | 2026-09-21 | https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived |
| S11 | GWCF technology update | CF web | 2026-07-28 | https://www.thecommunityfoundation.org/news/an-update-on-our-technology-transformation-what-fundholders-need-to-know |
| S12 | Seattle EFT enrolment | CF web | 2026 | https://www.seattlefoundation.org/seafdn-eft-enrollment/ |
| S13 | SFF ACH enrolment | CF web | live | https://sff.org/what-we-do/funding/enroll-in-direct-deposit-ach-grant-payments/ |
| S14 | Denver Fund Manager guide | CF web | live | https://denverfoundation.org/fundmanager/ |
| S15 | Minneapolis DonorView FAQ | CF web | live | https://www.minneapolisfoundation.org/donorview-faq/ |
| S16 | CFT financials page (ACH form) | CF web | FY2026 | https://www.cftexas.org/about-cft/financials-investments/ |
| S17 | Pittsburgh Wish Book FAQ | CF web | live | https://pittsburghfoundation.org/wish-book-faqs |
| S18 | Pittsburgh donor portal FAQ (NetCommunity) | CF web | live | https://community.pittsburghfoundation.org/pages/frequently-asked-questions |
| S19 | CF NE Florida portal post and ACH form | CF web/doc | 2025-09 form | https://www.jaxcf.org/introducing-the-grantee-portal-a-one-stop-shop-for-nonprofits-seeking-support/ ; https://www.jaxcf.org/wp-content/uploads/2026/07/TCF-ACH-Authorization-Form_Operations-2025-09.pdf |
| S20 | NHCF FAQ (Checkmint) | CF web | live | https://www.nhcf.org/how-can-we-help-you/apply-for-a-grant/frequently-asked-questions/ |
| S21 | California CF grant report page (ACH) | CF web | live | https://connect.calfund.org/GrantDisbursementReport |
| S22 | Louisville FAQ | CF web | ©2026 | https://www.cflouisville.org/faqs/ |
| S23 | RIF ACH submission | CF web | live | https://rifoundation.org/about/your-community-foundation/connect/grantee-authorize |
| S24 | DonorSphere login and config (GHCF) | vendor host | live | https://ghcf.donorsphere.org/login ; https://ghcf.donorsphere.org/config/googleAnalyticsIDs.js |
| S25 | GKCCF portal env | CF host | live | https://gkccf.donor-portal.org/env.js |
| S26 | Ren payments page | vendor web | 2026 | https://www.reninc.com/payments/ |
| S27 | Ren for Charities help articles | vendor help | Jul–Nov 2026 | https://intercom.help/rengiving/en/articles/6229556-ren-for-charities-overview |
| S28 | AEF charities page | sponsor web | Q2 2026 | https://www.aefonline.org/charities/ |
| S29 | RCF FAQ | sponsor web | live | https://renaissancecharitable.org/faqs/ |
| S30 | BofA CGF Navigating guide | sponsor doc | 2026-02-23 | https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf |
| S31 | NPact Foundation Cloud listing | third party [R] | — | https://www.trustradius.com/products/npact-foundation-cloud/details |
| S32 | 990 contractor harvest (FY2021+) | filings | FY2022–FY2025 | data/mission-2026-11-14/form990-contractors-harvest-full.csv |
| S33 | Portal hosts per foundation | CF web | live | see `source_urls` in the CSV |

---

## 7. Data dictionary: `community-foundation-rails-portals-2026.csv`

| Column | Meaning |
|---|---|
| `foundation` | Common name of the community foundation. |
| `ein` | IRS EIN, 9 digits with no dash; leading zeros are dropped where DAFRC drops them. |
| `fy2024_daf_assets_usd` | DAFRC `eoy_daf_assets` for `fiscal_year_end = 2024`. DAFRC's FY label can map to a tax period ending in 2023 or 2024; see the DAFRC `end_of_tax_period` column. |
| `payment_rails` | How grants reach grantees, as documented on 2026-11-14: check, own ACH, a named third-party rail, or "not found". Quotes are verbatim. DAF coverage is noted where the source states it. |
| `eft_provider` | A named third party (Chariot Disbursements, Bill.com, REPAY, Citizens Bank Checkmint), "own ACH (no provider named)", "none documented", or "not found". |
| `portal_vendor` | Vendor or platform behind the donor/fundholder login, identified from host, footer or markup. |
| `portal_evidence` | The link path from the foundation site to the login host, and the fingerprint used. |
| `ledger_vendor_if_known` | Fund-accounting or back-office vendor where a 990 payee line or first-party page names one, with the amount. [I] marks an inference from the portal path. |
| `source_urls` | Primary sources, separated by " ; ". |
| `retrieved` | Access date (2026-11-14). |
| `dafrc_rank_fy2024` | Rank among DAFRC "Community Foundation" filers by FY2024 DAF assets. |

**Edges (EG001–EG028):**
- **Rails:** Chariot→SPMF (first-party; upgrades E149), REPAY→GWCF, Bill.com→CFGA and Citizens Checkmint→NHCF.
- **GWCF stack:** Blackbaud Financial Edge NXT→GWCF, and NPact Foundation Cloud→GWCF (inferred).
- **DonorSphere:** GHCF (confirmed) and Pittsburgh (inferred).
- **iPhi:** SPMF and Louisville.
- **Single portals:** Akoya→EBCF, SmartSimple→Boston and Power Pages→Seattle.
- **Foundant:** 10 new CommunitySuite portal edges (Columbus, Atlanta and Denver already exist as EC008–EC010).
- **Salesforce:** 5 portal edges.

## Validation corrections (wave 7, 2026-11-14) — governing
Source: [validation-wave7-report.md](validation-wave7-report.md). Where these conflict with the text above, these govern.

1. **Line 84**
   - Current: "**Greater Washington CF (#38): Blackbaud REPAY**, live since September 2026."
   - Replace with: "**Greater Washington CF (#38): REPAY (payments partner, alongside Blackbaud Financial Edge NXT)**. GWCF says it 'partnered with Blackbaud and REPAY' in 'systems transformation upgrades completed in September 2026'."
2. **Line 90**
   - Current: "(Bill.com, Blackbaud REPAY, Citizens Checkmint)"
   - Replace with: "(Bill.com, REPAY, Citizens Checkmint)"
3. **Line 30**
   - Current: "**NPact Foundation Cloud (spectrumportal.net): 3**"
   - Replace with: "**Foundation Cloud on spectrumportal.net (NPact per third-party sources [R]): 3**"
   - Optionally add to line 111: "The GWCF sign-in page loads `payments.blackbaud.com/Checkout/bbCheckout.2.0.js` [F]."
4. **Line 29**
   - Current: "**2 are check-only:** Chicago Community Trust (DAF grants are mailed checks)"
   - Replace with: "**2 document checks only:** Chicago Community Trust (for DAF grants; discretionary-grant rail not documented)"
5. **Line 73 (SPMF row).** Append: "Chariot's own post (dated 'Sep 15', © 2026) says the move is expected 'with a few exceptions' ([Chariot](https://givechariot.com/resources/insights/enrolling-with-chariot-for-electronic-grant-payments-from-the-saint-paul--minnesota-foundation)) [V]. The year of 'this fall' is inferred from the footers."

## Compliance note (2026-11-15) — governing
crt.sh disallows all crawlers in its robots.txt. Any claim in this document that rests **only** on crt.sh certificate data is downgraded to an unverified lead until re-sourced. See [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md).
