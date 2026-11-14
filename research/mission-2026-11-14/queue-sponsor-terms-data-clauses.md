# Sponsor terms on credentials, automated access, aggregators and export; Candid API licence (P-EXP-03, P-PAY-08, P-EXP-01, P-QA2-07)

**Date:** 2026-11-14. **Status:** I read public pages and PDFs only. I logged in nowhere, submitted no forms, created no accounts and contacted no one.

**Recency rule:** current-state findings use only 2021+ documents, or live pages that carry no date (marked "undated, live 2026-11-14"). Anything older is named and marked "pre-2021, not counted".

**Evidence labels:**
- **[F]:** first-party document (sponsor, vendor or platform).
- **[V]:** a vendor's statement about its own product.
- **[R]:** a search-index summary I could not open first-hand.
- **[I]:** my inference.

Quotes are verbatim and 40 words or fewer. A script checked every quote in the CSV against the fetched source text.

**Governing corrections applied:** wave-8 corrections 17 and 18 ([validation-wave8-report.md](validation-wave8-report.md)). The SVCF clause is quoted with its purpose limit and with the third-party-access indemnity.

**Data written:**
- [`data/mission-2026-11-14/sponsor-terms-clauses-2026.csv`](../../data/mission-2026-11-14/sponsor-terms-clauses-2026.csv): 36 clause rows covering 10 sponsors and Schwab as DAFgiving360's platform.
- [`data/mission-2026-11-14/queue-proposals-terms.csv`](../../data/mission-2026-11-14/queue-proposals-terms.csv): P-TRM-01 to P-TRM-06.

---

## 0. Headline answers

| Item | Answer | Confidence |
|---|---|---|
| **P-EXP-03: SVCF-like clauses elsewhere in the top 20** | **Yes, and two are stronger than SVCF's.**<br>- **NCF's Program Agreement (effective 2025-09-17)** has a named "Credential sharing prohibition", a "Scraping prohibition" and a "Third-party services" section: "NCF does not authorize any third-party service to access the Secure Site or an NCF charitable fund on behalf of users" [F].<br>- **Vanguard Charitable's User Agreement (May 2025)** bars "any program, expert system, electronic agent, bot, or other automated means". It also expressly *permits* account holders to use read-only "aggregators" [F].<br>- **NPT's Terms of Use (2026-10-29)** ban robot or script harvesting "for any purpose" and use of site data to build AI tools [F].<br>- **Purpose-limited bans:** SVCF's ban is the narrowest; it applies only to purposes unrelated to grantmaking. The Charityvest and RCF website terms carry generic anti-bot clauses [F].<br>- **Fidelity Charitable** has no automated-access clause in its public terms. Its License Agreement instead *provides for* "export or download … within a third party software product or on-line service" [F].<br>- **Data ownership:** no sponsor gives donors ownership of account data. Fidelity is the only one with an export clause, and it makes transmitted data "the sole responsibility of the user". | High for documents read; 10 of 20 top sponsors not yet read (P-TRM-05) |
| **P-PAY-08: credential sharing and aggregators at national sponsors** | **Credential sharing is barred or discouraged at every national sponsor whose donor terms are public. Losses from shared credentials fall on the donor.**<br>- **Explicit third-party bans:** Vanguard ("including charities or grant recommendation processing services") and NCF ("any third-party service or application that requires you to provide your NCF credentials") [F]. Both read directly on credential pass-through tools such as DAFpay's [I].<br>- **Ban unless the sponsor authorises the person:** NPT [F].<br>- **No sharing with third parties:** Fidelity ("not to make it available to any third parties") and SVCF's website terms [F].<br>- **Keep the password confidential (no third-party ban):** Charityvest [F].<br>- **DAFgiving360:** its own terms page returned 403. Its Program Policies bind Client Center users to Schwab's Online Services Agreement, which is behind login. Schwab's public third-party terms (2021) say "DO NOT SHARE … THE SECURITY GUARANTEE WILL NOT APPLY" [F]. Whether that reaches DAFgiving360 accounts is [I].<br>- **Daffy and AEF:** no credential clause found. Daffy disclaims "losses resulting from account fraud, theft, or any other unauthorized activity" [F].<br>- **Liability:** Vanguard, NPT, NCF and Fidelity treat instructions entered with the credentials as the donor's own, or disclaim liability [F]. SVCF adds an indemnity from the advisor [F]. Chariot's donor terms cap Chariot's liability at US$1,000 (repo, [F]).<br>- **Mitigants:** Chariot moved DAFgiving360 to an email-code and phone-call verification flow (2026), and shipped DAF-side Donor Account and Authorization Token APIs in its 2026-05-08 changelog [V]. Sponsor approval of every grant is unchanged. | High (documents read in full); DAFgiving360/Schwab applicability [I] |
| **P-EXP-01: DAFgiving360 donor-side export** | **Still unverified; no change in score.**<br>- **No donor-side export documented.** The 2024 Program Policies (PDF modified 2024-12-12) give users "access to the account's grant history and grant award letters on the DAFgiving360 Client Center" and describe no export [F].<br>- **Advisor-side Export, search index only.** A search-index summary again places the "Export" function in Grant History under Schwab Advisor Center [R].<br>- **Pages unreadable from here.** dafgiving360.org returned 403 again. web.archive.org reset the connection through the proxy, and WebFetch cannot reach it. | Medium (absence in a first-party PDF; help pages unread) |
| **P-QA2-07: Candid API licence, SOC, Charity Check sources** | **The licence is restrictive on redistribution and has no carve-out for retention after termination.**<br>- **Public API License Agreement (last updated 2026-09-14):**<br>  - bars third-party access beyond named Authorized Users and Licensee Customers<br>  - bars republication<br>  - bars building a database "other than for Licensee's own internal business use"<br>  - expressly bars extraction for "artificial intelligence"<br>  - requires the licensee to "cease … all use of the Candid Data" on termination, with no record-retention exception<br>  - gives Candid annual audit rights, lasting two years after the term [F].<br>- **No caching clause and no retention period** are stated [F, absence].<br>- **Docs pull the other way:** they tell users to save Charity Check PDFs "to build an audit trail for grantmaking" [F]. The conflict is [I].<br>- **SOC:** Candid completed its first external SOC 2 audit in 2023 and audits annually (blog posts 2023 and 2025). The type and the report are not public, and the developer portal refers security questions to sales [F].<br>- **Charity Check sources:**<br>  - IRS Pub 78, BMF, IRB, Automatic Revocation and the OFAC SDN list.<br>  - Candid checks the IRS site "every 20 minutes" for new BMF, Pub78 and Revocations files.<br>  - OFAC refresh cadence: not stated [F]. | High (documents read) |

---

## 1. P-EXP-03: clause census across the top 20 (FY2024 DAF assets)

Ranks are from [dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv).

**Column key:**
- **Y:** the document has an explicit clause of this type.
- **G:** a generic website clause covers it, not the donor account.
- **P:** the clause permits the activity.
- **N:** the document was read and has no clause of this type.

| # | Sponsor | Document read (date) | Automated collection | Credential sharing | Third-party / aggregator access | Export or data clause |
|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable | [Electronic Customer Services Agreement](https://www.fidelitycharitable.org/legal/electronic-customer-svcs-agreement.html) and [License Agreement](https://www.fidelitycharitable.org/legal/license-agreement-and-copyright.html) (undated, live); [Program Guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf) (2026-09-11) | N | Y ("not to make it available to any third parties") | N (no aggregator clause) | **P**: s.8 "export or download Giving Account information … within a third party software product or on-line service". The guidelines give a "view, but not necessarily modify" right |
| 2 | NPT | [Terms of Use/Privacy](https://www.nptrust.org/privacy-policy/) (2026-10-29) | Y ("robots, spiders, scripts … for any purpose"; plus an AI-development ban) | Y (only persons "authorized in accordance with NPT's policies") | via credential clause | N |
| 3 | DAFgiving360 | [2024 Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) (2024-12-12); [terms page](https://www.dafgiving360.org/terms-and-conditions) returned 403 | not read (Schwab OSA) | by reference to the Schwab OSA; Schwab's [third-party terms](https://www.schwab.com/legal/third-party-terms) (2021-07-30) say do not share | Schwab offers sanctioned aggregator API access for brokerage clients; for DAF accounts this is [I] | Grant history viewable; no export |
| 4 | Vanguard Charitable | [User Agreement](https://www.vanguardcharitable.org/company-policies/user-agreement) (May 2025) | Y ("electronic agent, bot") | Y (names "charities or grant recommendation processing services") | **P** for the account holder's own aggregator; barred for "Unauthorized Third Parties" | Y: may "print, download and distribute" account content to advisers and agents |
| 5 | GS DAF | none public 2021+ (2008 circular only, pre-2021) | — | — | — | — |
| 6 | SVCF | [Advised Fund Agreement](https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf) (2025-08-22); [website terms](https://www.svcf.org/terms-of-use) (2024-04-22) | Y (purpose-limited) | Y (website terms: "may not share your Account credentials with third parties") | Third-party portal access is at the advisor's risk, with an indemnity | N |
| 7 | AEF | no terms of use found; [platform FAQ](https://engage.aefonline.org/platform-resources/) (undated, live) | — | — | — | **Export button** for a grants-paid list in DonorCentral (see §4) |
| 8 | MS GIFT | [grantmaking PDF](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf) (2024-10-01) | N | N | N | N. Ren's FAQ says MS GIFT donors "will not receive separate login credentials" ([Ren, 2025](https://www.reninc.com/giving-season-2025-commonly-asked-questions/)) [V] |
| 9 | RCF | [Terms & Conditions](https://renaissancecharitable.org/terms) (undated, live; copyright line 2014) | G ("scrape … without the advance written authorization") | N | N | N |
| 10 | NCF | [Program Agreement](https://secure.ncfgiving.com/agreement) (effective 2025-09-17); [public-site terms](https://www.ncfgiving.com/terms-and-disclosures) (undated) | Y (scraping and bulk download) | Y (named section; includes advisors and MFA codes) | Y ("does not authorize any third-party service") | NCF owns the public website's "data"; republishing Secure Site data is barred |
| 11–20 | BofA CGF, CCT, ImpactAssets, FFTC, JCF, GKCCF, Greater Horizons, Dechomai, CJP, Raymond James | CCT [portal user guide](https://donorportal.cct.org/ma/docs/cct/DonorPortalUserGuide.pdf) (2024-02) has no such clauses. CCT's policy page returned 403. The rest were not read | — | — | — | — (P-TRM-05) |
| comparator | Daffy | [Member Agreement](https://www.daffy.org/legal/agreement) (2025-11-11) | N | N | N (Daffy itself publishes an API and MCP) | Fraud-loss disclaimer |
| comparator | Charityvest | [Terms of Use](https://www.charityvest.org/terms-of-use) (CMS update 2025-06-28) | G ("automated or non-human means, whether through a bot, script, or otherwise") | Y (confidentiality; user responsible) | N | N |

**Reading [I]:**
1. **SVCF is no longer the only top-10 contractual limit, and it is now the mildest.**
   - NCF's September 2025 agreement is the most complete anti-agent text found at any sponsor. It covers credential sharing, scraping, bulk download and third-party services, and it says NCF may deploy "CAPTCHA challenges, IP blocking, rate limiting, behavioral analysis".
   - Wave-8 correction 18 called SVCF's clause "the only top-10 contractual limit". That statement should now read: "one of four top-10 sponsors with contractual limits (NCF, Vanguard, NPT, SVCF)".
2. **Vanguard draws the line where a product designer would want it.**
   - **Allowed:** read-only aggregation by the account holder.
   - **Not allowed:** a third party, or an "electronic agent", acting with the holder's credentials.
   - **Open tension:** the agreement permits "web crawler devices" for aggregation but bars "automated means" of access. A read-only agent run by the donor may sit on either side.
3. **Fidelity is the outlier the other way.** Its License Agreement provides for third-party export, but its public how-to material documents only PDF download (P-TRM-03).
4. **No sponsor states that the donor owns the account data or may port it.** The nearest is Vanguard's right to "print, download and distribute" content to agents.

---

## 2. P-PAY-08: credentials, aggregators and liability at the national sponsors

**Who bears the loss when shared credentials lead to an unauthorized grant:**

| Sponsor | Credential rule | Who bears a loss from shared credentials | Source |
|---|---|---|---|
| Fidelity Charitable | "not to make it available to any third parties". The user is responsible for "the confidentiality and use of my (our) password(s)" | Donor. Fidelity has no "responsibility or liability" if the donor fails to notify | [ECSA](https://www.fidelitycharitable.org/legal/electronic-customer-svcs-agreement.html) [F] |
| DAFgiving360 | Bound by Schwab's Online Services Agreement (not public). Schwab's public terms: "DO NOT SHARE … THE SECURITY GUARANTEE WILL NOT APPLY" | Donor, by inference. Schwab's site terms: "if you do share this information with anyone we'll consider their activities to have been authorized by you" | [Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf); [Schwab third-party terms](https://www.schwab.com/legal/third-party-terms); [Schwab terms](https://www.schwab.com/legal/terms) [F]/[I] |
| Vanguard Charitable | Explicit ban, naming "grant recommendation processing services". No "electronic agent, bot" access | Donor. Instructions are deemed authorized, Vanguard has no liability for "mishandling" of credentials, and the donor indemnifies | [User Agreement](https://www.vanguardcharitable.org/company-policies/user-agreement) [F] |
| NPT | Access only for persons authorized under NPT policy | Donor. Instructions are "authorized by you", with "no responsibility or liability" | [Terms of Use](https://www.nptrust.org/privacy-policy/) [F] |
| NCF (top 10, not national) | Explicit ban on third-party services and on sharing with advisors | Donor. Responsible "whether or not authorized by you"; privileges may be terminated | [Program Agreement](https://secure.ncfgiving.com/agreement) [F] |
| Daffy | No sharing clause. Each member has their own login. API and MCP access are sanctioned | Donor. Daffy is "not responsible for any losses resulting from account fraud" | [Member Agreement](https://www.daffy.org/legal/agreement) [F] |
| Charityvest | Keep the password confidential. No bots | Donor. "responsible for all use of your account and password" | [Terms of Use](https://www.charityvest.org/terms-of-use) [F] |
| AEF | No public terms of use found. Its privacy policy refers to "Terms of Service" | unknown | [privacy policy](https://www.aefonline.org/data-protection-privacy-policy/) [F, absence] |
| RCF | Website terms only. No portal credential clause found | unknown | [Terms](https://renaissancecharitable.org/terms) [F, absence] |

**How this fits with DAFpay:**
- **Chariot's own terms:** the DAFpay Donor Terms (effective 2025-09-24) have the donor warrant "requisite authority to give to Chariot permission to use the DAF Provider credentials", and cap Chariot's liability at US$1,000 ([repo: queue-fidelity-chariot-goodstack-vanguard.md §3](queue-fidelity-chariot-goodstack-vanguard.md); [dafpay.com](https://www.dafpay.com/donor-terms-of-use)) [F].
- **The conflict:** at Vanguard and NCF that warranty cannot be true, because both sponsors' own agreements deny the donor that authority [I].
- **DAFgiving360 is now handled differently.** Donors verify by "emailed code", can enable a passkey, and get "a call from DAFgiving360" on first use ([Chariot, 2026-05-31](https://givechariot.com/resources/insights/new-access-method-for-dafgiving360-in-dafpay.md)) [V].
- **Chariot's DAF-side APIs (2026-05-08 changelog).** These offer "Donor-Initiated Verification" and "DAF-Initiated Setup" via Authorization Tokens, which give a path with no credentials ([changelog](https://docs.givechariot.com/changelog/2026/5/8)) [V].
- **Implication for AI agents [I]:** an agent driving a donor's sponsor login breaches the written terms at Vanguard, NCF and NPT. The donor would bear any loss everywhere checked. Sanctioned agent paths exist only where the sponsor publishes them (Daffy's API and MCP, Endaoment) or brokers them (Chariot's DAF-side tokens).

**Pre-2021 context, not counted:** Schwab's data-aggregation FAQ (form code 0620) says Schwab requires "Data Access terms" before aggregators get API access ([Schwab](https://www.schwab.com/legal/public-security-tips-popup)).

---

## 3. P-EXP-01: DAFgiving360 donor-side export

| Check | Result |
|---|---|
| Live help pages ([donor](https://www.dafgiving360.org/content/how-recordkeeping-works), [advisor](https://www.dafgiving360.org/content/how-recordkeeping-works-advisor)) | HTTP 403 again on 2026-11-14 |
| Wayback (snapshots 2025-02-17 donor, 2025-06-19 advisor, from the availability API) | Exist, but web.archive.org reset the connection through the proxy, and WebFetch cannot reach it |
| Search index | **Advisor side:** in Schwab Advisor Center, "In Grant History, use the Export function" [R].<br>**Donor side:** paraphrased as Account, then Statements, then Account History, with receipts and an annual summary letter. No export mentioned [R]. |
| 2024 Program Policies (PDF modified 2024-12-12) [F] | **Client Center:** "access to the account's grant history and grant award letters on the DAFgiving360 Client Center". No export described.<br>**Advisors:** "view-only access … via the secure Schwab Advisor Center" for advisors who hold only Schwab brokerage accounts |

**Conclusion:** no change to the A1/A3 export score. The `donor-data-export-top10-2026.csv` row 3 stays "advisor-side only, unverified". Verifying it needs a network that dafgiving360.org does not block, or a logged-in check, which is outside this mission's rules.

---

## 4. AEF: a donor export instruction (new; conflicts with the existing row)

- **What AEF's live page says:** the [platform-resources FAQ](https://engage.aefonline.org/platform-resources/) gives donors this path in DonorCentral: Funds tab → Grants Paid → choose the columns → "Click on the Export button, and the file will automatically be exported to the device's Download location" [F]. The format is not stated.
- **What the repo says:** the AEF row in `donor-data-export-top10-2026.csv` reads "no export; history truncated", based on AEF's Ren-migration FAQ.
- **Two readings:**
  - The page describes the legacy DonorCentral (NPact) platform during migration.
  - DonorCentral is still live for some donors.
- **Status:** unresolved (P-TRM-02). If the export is still live, AEF becomes the only top-10 sponsor with a documented donor-side export.

---

## 5. P-QA2-07: Candid API licence and Charity Check

**Licence terms.** Source: [API License Agreement](https://candid.org/terms-of-service/api-license-agreement/), last updated 2026-09-14. The [developer-portal copy](https://developer.candid.org/page/candid-api-terms-of-service.md) is an older form; the [Candid License Agreement](https://developer.candid.org/page/candid-license-agreement.md) is dated December 2023.

| Topic | Clause (verbatim) | Reading |
|---|---|---|
| Permitted use | Provide data to Licensee Customers "in order to allow Licensee Customers to learn about nonprofit organizations for the purpose of evaluating them as recipients of charitable donations" | Any further use must be listed in an Exhibit |
| Third-party access | "Licensee shall not permit access by any third party (other than Authorized Users, Licensee Customers or any other persons or entities to the extent specifically identified in the Order Form) to any portion of the Candid API." | A sponsor's vendor or agent must be named in the Order Form |
| Redistribution | Licensee may not "republish or distribute information from the Candid API (including, without limitation, by posting same on any third party Web site) except as expressly permitted herein" | Passing results between sponsors and vendors is restricted |
| Database building and AI | No database "other than for Licensee's own internal business use". "This prohibition expressly applies to data mining or extraction for use in or through the use of artificial intelligence" | Survives termination. An AI-native platform caching Candid data needs explicit terms |
| Caching and retention | **No clause found** | Silent |
| On termination | "Licensee shall cease, and shall cause its Authorized Users to cease, all use of the Candid Data" | No exception for keeping due-diligence records |
| Audit | Candid may audit "not more than one (1) time during each year of the Term and for a period of two (2) years thereafter" | — |
| Attribution | "Powered by Candid" must appear on pages that show Candid Data | — |
| Website ToS | [Terms of service](https://candid.org/terms-of-service/), last updated 2025-08-01: generic; links to the separate licence agreements | — |

**Docs vs licence [I].** The [Charity Check getting-started page](https://developer.candid.org/reference/get-started-with-charity-check.md) (updated 2026-09-07) says to "download and save a PDF copy of the charity check report, which includes a timestamp, to build an audit trail for grantmaking". The public licence has no retention carve-out. A sponsor that switches vendors may lack an express right to keep relying on stored reports. This may be resolved in Order Forms (P-TRM-04).

**Security and SOC [F]:**
- "In 2023, Candid completed our first external SOC 2 audit" ([blog, 2023-11-29](https://candid.org/blogs/building-a-culture-of-nonprofit-compliance-at-candid/)).
- "Candid performs an annual audit that requires a third-party auditor to review our controls and policies" ([blog, 2025-04-24](https://candid.org/blogs/how-candid-ensures-data-security-safeguards/)).
- Not stated publicly: whether the report is Type 1 or Type 2, its scope, and any public trust centre.
- The developer portal says only TLS 1.2, and: "For more information on our security policies, please reach out to your business development representative" ([uptime and security](https://developer.candid.org/reference/status-and-uptime.md)).

**Charity Check data sources [F]:**
- **Databases checked:** "IRS Publication 78, IRS Business Master File, Internal Revenue Bulletin, Automatic Revocation of Exemption, and OFAC Specially Designated Nationals List" ([getting started](https://developer.candid.org/reference/get-started-with-charity-check.md)).
- **State data:** California only (AG Registry and FTB) ([FAQ](https://developer.candid.org/reference/faqs-charity-check.md)).
- **Refresh:**
  - "We ping the IRS website every 20 minutes and download the big three files (BMF, Pub78, Revocations) when we detect changes."
  - The IRS updates TEOS and the EO BMF monthly.
  - "Candid processes paper and electronic annual filings daily."
  - There is "not an explicit field for the last date a revocations file was processed" ([FAQ](https://developer.candid.org/reference/faqs-charity-check.md), updated 2026-09-07).
- **OFAC:** the `ofac_status` field "Indicates whether this organization has been listed by OFAC on the Specially Designated National (SDN) List" ([fields](https://developer.candid.org/reference/interpret-charity-check-data-fields.md), updated 2026-11-10). **No OFAC refresh cadence is stated.**
- **Correction to the queue text:** the queue described the cadence as "weekly IRB vs monthly BMF". Candid's own FAQ instead describes change-triggered pulls of BMF, Pub78 and Revocations. The IRB is the IRS's weekly bulletin, and each Charity Check record carries a `most_recent_irb` date.

**Implication for the A5 Candid scores [I]:**
- **Y1 (portability) = 3 holds.** The API is documented, but redistribution and post-termination use are restricted. Moving it down to 2 is defensible if P-TRM-04 finds no retention carve-out.
- **X3 (assurance):** move from U to "SOC 2 audited annually (self-reported); report not public".

---

## 6. Changes this implies for other repo files (proposed; not applied)

1. **`queue-donor-export-cf-payments-donorsphere.md`, §0 and §2, reading item 4** (already amended by wave-8 correction 18): change "the only top-10 contractual limit" to "one of four top-10 sponsors with written limits on automated or third-party access: NCF (2025-09), Vanguard (2025-05), NPT (2026-10) and SVCF (2025-08)".
2. **`donor-data-export-top10-2026.csv`:**
   - **Row 7 (AEF):** add a note on the DonorCentral "Export" instruction; the status stays pending P-TRM-02.
   - **Row 1 (Fidelity):** add License Agreement s.8 (a provision for third-party export).
   - **Row 4 (Vanguard):** add the User Agreement's right to "print, download and distribute".
3. **Agentic-control gap matrix:** add a "sponsor terms prohibit agent or third-party credential use" flag. Set it to yes for Vanguard, NCF and NPT; yes (website terms) for SVCF; and unknown for DAFgiving360, AEF, GS DAF and MS GIFT.

---

## 7. Source register

| ID | Source | Type | Date | Retrieved | URL |
|---|---|---|---|---|---|
| T01 | SVCF Advised Fund Agreement | sponsor contract | PDF mod. 2025-08-22 | 2026-11-14 | https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf |
| T02 | SVCF Website Terms of Use | site terms | 2024-04-22 | 2026-11-14 | https://www.svcf.org/terms-of-use |
| T03 | NCF Program Agreement | sponsor contract | eff. 2025-09-17 | 2026-11-14 | https://secure.ncfgiving.com/agreement |
| T04 | NCF Terms and Disclosures | site terms | undated | 2026-11-14 | https://www.ncfgiving.com/terms-and-disclosures |
| T05 | Vanguard Charitable User Agreement | portal terms | May 2025 | 2026-11-14 | https://www.vanguardcharitable.org/company-policies/user-agreement |
| T06 | Vanguard Charitable Terms & Conditions | site terms | eff. 2016-08-01 (pre-2021; points to T05) | 2026-11-14 | https://www.vanguardcharitable.org/company-policies/terms-and-conditions |
| T07 | Vanguard Charitable Policies & Guidelines | program policy | 2026-01-09 | 2026-11-14 | https://www.vanguardcharitable.org/company-policies/policies-and-guidelines |
| T08 | NPT Terms of Use / Privacy Policy | site and portal terms | 2026-10-29 | 2026-11-14 | https://www.nptrust.org/privacy-policy/ |
| T09 | Fidelity Charitable Electronic Customer Services Agreement | portal terms | undated | 2026-11-14 | https://www.fidelitycharitable.org/legal/electronic-customer-svcs-agreement.html |
| T10 | Fidelity Charitable License Agreement and Copyright Policy | portal terms | undated | 2026-11-14 | https://www.fidelitycharitable.org/legal/license-agreement-and-copyright.html |
| T11 | Fidelity Charitable Program Guidelines | program policy | 2026-09-11 | 2026-11-14 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf |
| T12 | DAFgiving360 2024 Program Policies | program policy | PDF mod. 2024-12-12 | 2026-11-14 | https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf |
| T13 | DAFgiving360 terms and help pages | site | — (HTTP 403) | 2026-11-14 | https://www.dafgiving360.org/terms-and-conditions ; https://www.dafgiving360.org/content/how-recordkeeping-works ; https://www.dafgiving360.org/content/how-recordkeeping-works-advisor |
| T14 | Schwab Third Party Provider instruction and consent | platform terms | 2021-07-30 | 2026-11-14 | https://www.schwab.com/legal/third-party-terms |
| T15 | Schwab Terms of Use | site terms | form 0225 | 2026-11-14 | https://www.schwab.com/legal/terms |
| T16 | Schwab data-aggregation FAQ | platform FAQ | form 0620 (pre-2021, context only) | 2026-11-14 | https://www.schwab.com/legal/public-security-tips-popup |
| T17 | Daffy Member Agreement | sponsor contract | 2025-11-11 | 2026-11-14 | https://www.daffy.org/legal/agreement |
| T18 | Charityvest Terms of Use | site terms | CMS 2025-06-28 | 2026-11-14 | https://www.charityvest.org/terms-of-use |
| T19 | Charityvest Policies & Guidelines | program policy | eff. 2025-04-04 | 2026-11-14 | https://www.charityvest.org/documents/Charityvest,%20Inc.%20-%20Personal%20Charitable%20Giving%20Fund%20-%20Policies%20&%20Guidelines.pdf |
| T20 | RCF Terms & Conditions | site terms | undated (©2014 line) | 2026-11-14 | https://renaissancecharitable.org/terms |
| T21 | AEF platform-resources FAQ | help page | undated | 2026-11-14 | https://engage.aefonline.org/platform-resources/ |
| T22 | AEF privacy policy | privacy | undated | 2026-11-14 | https://www.aefonline.org/data-protection-privacy-policy/ |
| T23 | MS GIFT grantmaking PDF | program doc | 2024-10-01 | 2026-11-14 | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf |
| T24 | Ren giving-season 2025 FAQ | vendor FAQ | 2025 | 2026-11-14 | https://www.reninc.com/giving-season-2025-commonly-asked-questions/ |
| T25 | CCT Donor Portal User Guide | portal guide | PDF mod. 2024-02-06 | 2026-11-14 | https://donorportal.cct.org/ma/docs/cct/DonorPortalUserGuide.pdf |
| T26 | NYCT DAF Policies 2025 (outside top 20; checked) | program policy | 2025 edition | 2026-11-14 | https://thenytrust.org/wp-content/uploads/2026/03/DAF-Policies-and-Guidelines-2025-edited.pdf |
| T27 | Chariot: new access method for DAFgiving360 | vendor note | 2026-05-31 | 2026-11-14 | https://givechariot.com/resources/insights/new-access-method-for-dafgiving360-in-dafpay.md |
| T28 | Chariot API changelog 2026-05-08 | vendor docs | 2026-05-08 | 2026-11-14 | https://docs.givechariot.com/changelog/2026/5/8 |
| T29 | DAFpay Donor Terms of Use (repo, not re-read) | vendor contract | 2025-09-24 | repo | https://www.dafpay.com/donor-terms-of-use |
| T30 | Candid API License Agreement | vendor licence | 2026-09-14 | 2026-11-14 | https://candid.org/terms-of-service/api-license-agreement/ |
| T31 | Candid Terms of Service | site terms | 2025-08-01 | 2026-11-14 | https://candid.org/terms-of-service/ |
| T32 | Candid developer-portal API ToS and License Agreement | vendor licence | Dec 2023 / page 2026-09-07 | 2026-11-14 | https://developer.candid.org/page/candid-api-terms-of-service.md ; https://developer.candid.org/page/candid-license-agreement.md |
| T33 | Candid Charity Check docs (getting started, FAQ, fields, uptime) | vendor docs | 2026-09-07 to 2026-11-10 | 2026-11-14 | https://developer.candid.org/reference/get-started-with-charity-check.md ; https://developer.candid.org/reference/faqs-charity-check.md ; https://developer.candid.org/reference/interpret-charity-check-data-fields.md ; https://developer.candid.org/reference/status-and-uptime.md |
| T34 | Candid SOC 2 blog posts | vendor blog | 2023-11-29 ; 2025-04-24 | 2026-11-14 | https://candid.org/blogs/building-a-culture-of-nonprofit-compliance-at-candid/ ; https://candid.org/blogs/how-candid-ensures-data-security-safeguards/ |

---

## 8. Data dictionary

### `sponsor-terms-clauses-2026.csv`

| Column | Meaning |
|---|---|
| sponsor | DAF sponsor, or the platform whose terms a sponsor incorporates (Schwab for DAFgiving360) |
| document | Name of the agreement, terms or help page |
| date | The document's own date (effective, updated or PDF modification date). "undated (live 2026-11-14)" if it shows none |
| clause_type | One of the following:<br>- `automated_collection`: bots, scraping, automated access, AI use of data<br>- `credential_sharing`: sharing or transferring login credentials<br>- `aggregator`: third-party services, aggregators or agents accessing the account<br>- `data_ownership`: who owns or is responsible for data<br>- `export`: rights or functions to download or export account data<br>- `liability`: who bears loss from credential misuse. This value is an addition to the brief's five types, made to answer P-PAY-08 |
| quote | Verbatim text, ≤40 words; "…" marks omissions. Checked by script against the fetched text |
| source_url | Primary-source URL |
| retrieved | Date fetched (2026-11-14) |
| evidence_label | F = first-party |
| notes | Scope caveats, conflicts and inferences |

### `queue-proposals-terms.csv`

The columns and scales follow [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md). The prefix is P-TRM-.

## Validation corrections (wave 9, 2026-11-14) — governing
Source: [validation-wave9-report.md](validation-wave9-report.md). Where these conflict with the text above, these govern.

1. **§1 table, P-EXP-03 row.**
   - Replace "It also expressly *permits* account holders to use read-only \"aggregators\" [F]." with: "It also expressly permits an Authorized Person to use \"aggregators or similar web crawler devices for the purpose of aggregating information\" [F]; a third party using the holder's credentials is an \"Unauthorized Third Party\" and may not [F]. That this is in effect read-only, self-run aggregation is [I]."
   - Replace "and use of site data to build AI tools [F]" with "and use of site data or user data for the development or operation of any software, model or AI system [F]".
2. **§1 table, P-QA2-07 row.**
   - Replace "bars republication" with "bars republication except as expressly permitted (Licensee Customers via the Licensee Site; Order Form)".
   - Replace "expressly bars extraction for \"artificial intelligence\"" with "applies its database-building/resale/competition ban expressly to extraction \"for use in or through the use of artificial intelligence\" (internal business use is outside the ban)".
3. **§3 "Reading", item 2.** Mark "**Allowed:** read-only aggregation by the account holder." as [I]. Add: "Vanguard may block 'systematic, commercial or otherwise inappropriate' automated access in its discretion."
4. **§3 "Reading", item 3.** After "Its License Agreement provides for third-party export", insert "(s.8, permissive 'may provide', undated; no live feature found)".
5. **§4 (AEF).** Add: "The instruction sits on AEF's 'Technology Upgrade' (Ren) support site and covers only a grants-paid list in legacy DonorCentral."
