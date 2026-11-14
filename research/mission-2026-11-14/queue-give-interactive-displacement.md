# Give Interactive: Ren displacement, Vanguard scope, tenants, ownership (P-VEN-01, P-QA1-01, P-VEN-07)

**Date:** 2026-11-14. **Status:** public-source evidence only. No authenticated page was accessed, no credentials were used and no contract was seen.

**Evidence labels** (same as [queue-vendor-scope-ren-denominator.md](queue-vendor-scope-ren-denominator.md)):
- **confirmed:** a first-party page, live HTTP response or IRS filing states the fact.
- **inferred:** convergent indirect evidence (CT logs, DNS, slug naming, search snippets).
- **unknown:** no evidence either way.

A Give Interactive tenant hostname is a configured environment. **It is not a contract and not a go-live.**

**Data written:**
- [`data/mission-2026-11-14/give-interactive-client-timeline.csv`](../../data/mission-2026-11-14/give-interactive-client-timeline.csv): 160 dated events for 10 sponsors. The rows cover Form 990 Part VII-B payments and absence bounds, first certificate per Give host, live portal observations, announcements and Schedule R entries.
- [`data/mission-2026-11-14/relationship-graph-edges-additions-2.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-2.csv): edges EB001–EB009.
- [`data/mission-2026-11-14/queue-proposals-give-interactive.csv`](../../data/mission-2026-11-14/queue-proposals-give-interactive.csv): proposals P-GIV-01 to P-GIV-07.

---

## 0. Headline findings

1. **The pattern is "pipeline overlap", not yet "systematic displacement".** Give is in some stage of implementation at five sponsors that pay Ren/Stellar today: ImpactAssets, Minneapolis, Thrivent, Stifel and WaterStone. Together they hold $5.86bn, or 1.8% of DAFRC FY2024 DAF assets. Of those five:
   - **One has cut over:** WaterStone, on 1 Nov 2026 ([waterstone.org/login](https://waterstone.org/login/)).
   - **One is in late-stage dual tenancy:** ImpactAssets has a Give production host and a first-party page announcing a 2026-09-08 launch, but its login is still on iPhi.
   - **Three are at the staging/SFTP stage:** Minneapolis, Thrivent and Stifel. All three live logins are still iPhi.
2. **Two more of the named clients are ex-Ren, but Give is replacing someone else there.**
   - **Chicago Community Trust** paid RenPSG for "record keeping services" until FY9/2020: $1.31m, $1.38m and $1.60m in FY2018–FY2020 ([990 FY2020](https://projects.propublica.org/nonprofits/organizations/362167000/202112239349302351/full)). Its live donor portal is "Powered by GiftingNetwork" ([donorportal.cct.org](https://donorportal.cct.org/)).
   - **Jewish Communal Fund** paid Renaissance Acquisition Co. $417,742 for "PREVIOUS DONOR PORTAL SUPPORT" in FY6/2023 ([990](https://projects.propublica.org/nonprofits/organizations/237174183/202410969349301036/full)).
3. **The Signatry itself is the first documented Ren→Give migration.** Servant Foundation (dba The Signatry) paid Renaissance Philanthropic Solutions Group for "managed services": $668,826 in FYE 3/2021 and $828,787 in FYE 3/2022 ([990 FYE 3/2022](https://projects.propublica.org/nonprofits/organizations/431890105/202320469349302877/full)). Over the same period it was building on Give, which it controls: the `thesignatry` production host dates from 2021-06-15.
4. **Give's ownership is a five-year fact, not a one-off.** The Signatry Charitable Trust's Schedule R lists **Give Interactive LLC (EIN 84-4835291) at OwnershipPct 0.99 in every return from CY2020 to CY2024**. The Trust is general/managing partner from CY2023. Give is loss-making: the Trust's 990-T books Give partnership losses of -$494,509 in CY2023 and -$2,718,246 in CY2024 ([990 CY2024](https://projects.propublica.org/nonprofits/organizations/825070897/202543189349315279/full)). Give's own site does not disclose the owner.
5. **Vanguard Charitable: Give is the ledger, not (yet) the donor UX.** The live donor log-in `client.vanguardcharitable.org` is **Salesforce Experience Cloud**: it sends Salesforce `x-sfdc-trace-flags` headers and uses a SAML `authn-request.jsp` flow. Search snippets of Vanguard Charitable job posts list "Salesforce Experience Cloud, **Give Interactive accounting system**, AWS integrations" as new platforms. Go-live is not observed. A `vanguard-sftp` data channel was first certified 2026-11-03.
6. **Give churn is real.** Foundation for the Carolinas paid Give $654,500 for "software" in CY2023 ([990](https://projects.propublica.org/nonprofits/organizations/566047886/202433209349318318/full)), which is the only sponsor 990 found naming Give. Its tenants lapsed in Feb 2024. Tenants for OCF, Omaha, EBCF, KZCF and the San Diego Foundation also expired. Kalamazoo's site now links a Spectrum portal ([kzcf.org](https://kzcf.org/)).

---

## 1. Method and limits

- **Certificate transparency.**
  - [crt.sh `%.giveinteractive.com`](https://crt.sh/?q=%25.giveinteractive.com) returned 1,979 certificates and 138 names.
  - [certspotter](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names) was paged to 300 currently valid issuances. It adds the `*-sftp.int` hosts, `tc-innov`, `vc-innov` and `ia-innov`, which crt.sh had not yet indexed.
  - The timeline uses the earliest date from either source.
  - For **iPhi/Stellar, per-client CT history does not exist.** [crt.sh `%.iphiview.com`](https://crt.sh/?q=%25.iphiview.com) and [`%.stellartechsol.com`](https://crt.sh/?q=%25.stellartechsol.com) show wildcard certificates (`*.iphiview.com` from 2011, `*.stellartechsol.com` from 2010). The only exceptions are a 2025-04-20 batch (cafa, ccfnj, eqt, ocf, rj) and the `auth-npt-*` hosts. Ren-side status therefore rests on live portals and 990s.
- **Form 990.** IRS e-file XML was read by object_id from the GivingTuesday mirror (`gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/<id>_public.xml`), with object_ids listed from ProPublica organisation pages. Every return on ProPublica for the 13 EINs was parsed: Part VII-B, Schedule R, Schedule L and 990-T.
  - Part VII-B lists only the **five** highest contractors paid more than $100k. Where no vendor line appears, the timeline records the fifth-highest amount as an upper bound. An absence means "below that floor or zero", not "no relationship".
- **Live HTTP** on 2026-11-14 covered sponsor home and login pages, iPhi login pages, Give tenant landing pages and DNS via [dns.google](https://dns.google/).
- **Not reached:**
  - web.archive.org is blocked by egress policy, so there is no Wayback history of login links.
  - jcfny.org, cct.org (home), unitedcharitable.org and thesignatry.com return Cloudflare 403 to curl. WebFetch reached thesignatry.com and cct.org.
  - jcfny.donorfirst.org returned 503 or a reset.
  - Job-post pages (Teal) returned 403, so only search-engine snippets were seen.
  - Probing Give tenant `config.js` files was declined by the session's permission policy. SSO labels cited in earlier repo work ("cct-prod", "vanguard-prod-okta") were therefore **not re-checked**.

---

## 2. Per-client timelines and classification (Q1)

Classification as of 2026-11-14. The categories are migrated / migrating (dual tenancy) / Give-only / Ren-only / unclear. Assets are DAFRC FY2024 ([dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)).

| Sponsor (DAF $bn) | Ren/Stellar in 990 Part VII-B | Give hosts (first cert) | Live log-in, 2026-11-14 | Class |
|---|---|---|---|---|
| **WaterStone** / Christian Community Foundation Inc, EIN 75-1750059 (0.54) | Stellar in **every year FYE 3/2014–3/2025**, rising from $119,943 to $366,469 | staging 2025-10-28; split-interest 2026-04-13; production 2026-05-14; SFTP 2026-10-05 | [waterstone.org/login](https://waterstone.org/login/): "We've moved to a new, upgraded online portal. If you haven't logged in since **November 1, 2026** …", which leads to `waterstone.giveinteractive.com`. "Open A Fund" still goes to an iPhi page ([iphi …/ws/OpenaGivingFund](https://iphi.stellartechsol.com/ws/OpenaGivingFund/tabid/123/Default.aspx)) | **migrated** (confirmed). Residual iPhi page |
| **ImpactAssets**, EIN 26-2048480 (3.63) | Stellar: CY2019 $188,794; CY2020 $249,320; CY2021 $331,193; CY2024 $232,315. CY2022–23 not in top-5 | staging 2025-04-29; production 2026-01-28; ~15 `ia-*` feature hosts in 2026 (private equity, Addepar, restricted investments, investment fee, reverse rebook); `ia-innov` 2026-10-27; SFTP 2026-11-03 | [impactassets.org](https://impactassets.org/) client login goes to `iphi.stellartechsol.com/calvert` (Stellar footer). The [DAF platform transition page](https://impactassets.org/daf-platform-transition/) announces a "new DAF hub on September 8, 2026". It does not name the vendor and still carries placeholder text | **migrating (dual tenancy)**. The announced launch had not happened by 2026-11-14. Give as the hub vendor is inferred |
| **Minneapolis Foundation**, EIN 41-6029402 (0.60) | Stellar $125,126 in FYE 3/2014 only. No Ren/Stellar line FYE 3/2019–3/2025 | staging 2026-02-12; SFTP 2026-10-05; **no production host** | [tmf.iphiview.com](https://tmf.iphiview.com/tmf/LogIn/tabid/54/Default.aspx) (Stellar) | **migrating (dual tenancy), early** (inferred) |
| **Thrivent Charitable**, EIN 41-1802412 (0.59) | Stellar CY2020–CY2024 ($194,080 → $270,307). **Renaissance Acquisition Co. $479,172 in CY2025** ([990](https://projects.propublica.org/nonprofits/organizations/411802412/202612669349300236/full)) | staging 2026-08-14; sandbox 2026-09-23; SFTP 2026-10-05; possibly `tc-innov` 2026-11-09 | [infaith.iphiview.com](https://infaith.iphiview.com/infaith/LogIn/tabid/444/Default.aspx) (Stellar) | **migrating (dual tenancy), early** (inferred) |
| **Stifel Charitable**, EIN 84-2049692 (0.49) | Stellar CY2022 $179,110. "Renaissance": $233,979 (CY2023), $498,305 (CY2024), **$801,302 (CY2025)** | staging 2026-06-25; SFTP internal and **external** 2026-09-04; no production host | [stifel.com DAF page](https://www.stifel.com/individual/donor-advised-funds) links to [sci.iphiview.com](https://sci.iphiview.com/sci/LogIn/tabid/444/Default.aspx) (Stellar, meta "Copyright 2026 by Stifel Charitable") | **migrating (dual tenancy), early** (inferred). Rising Ren spend is counter-evidence |
| **Chicago Community Trust**, EIN 36-2167000 (4.65) | RenPSG "record keeping services": $1,310,996 / $1,379,179 / $1,597,942 (FY9/2018–2020). Absent FY2021–FY2025 (5th-highest payee $276k+) | sandbox **2024-08-12**; staging 2025-02-28; production **2025-06-11**; k8s 2026; SFTP 2026-11-03 | [donorportal.cct.org](https://donorportal.cct.org/): "Powered by GiftingNetwork" | **unclear** for the Ren question. Give is implementing over a GiftingNetwork incumbent. CCT is ex-Ren (left around FY2021) |
| **Jewish Communal Fund**, EIN 23-7174183 (2.87) | Renaissance Acquisition Co. "PREVIOUS DONOR PORTAL SUPPORT" $417,742 (FY6/2023). No line in other years; the floor is ~$400k+ because investment managers dominate the top five | staging 2026-01-21; sandbox 2026-08-21; grant-cart 2026-08-31; innov 2026-09-09; SFTP 2026-10-05; no production host | Not observed: jcfny.org returned 403. `jcfny.donorfirst.org` (a Ren DonorFirst domain) has its own DNS record (Azure 52.240.154.157; random `*.donorfirst.org` names do not resolve) but returned 503 | **unclear** |
| **Vanguard Charitable**, EIN 23-2888152 (21.95) | No Ren line in any year (5th-highest $453k–$792k) | sandbox 2025-08-06; staging 2025-10-02; production 2026-01-28; `vc-innov` 2026-10-09; SFTP 2026-11-03 | Salesforce Experience Cloud (see §3) | **Give-only** (implementation). Not a Ren client |
| **The Signatry** (Servant Foundation EIN 43-1890105; Trust EIN 82-5070897) (1.01 + 0.40) | Renaissance Philanthropic Solutions Group, managed services: $668,826 (FYE 3/2021) and $828,787 (FYE 3/2022). Not in top-5 afterwards, but the floor was $930,697 or more | production **2021-06-15**; signatry-* 2022; `ts-fund-statements` 2024-02-28 (slug read as The Signatry, inferred) | [thesignatry.giveinteractive.com/log-in](https://thesignatry.giveinteractive.com/log-in) | **migrated** (confirmed). Ren and Give overlapped in 2021–22 |
| **Foundation for the Carolinas**, EIN 56-6047886 (2.95) | No Ren line in CY2019–2024. **Give Interactive LLC, software, $654,500 (CY2023)** | sandbox 2022-01-10 … last cert 2024-02-12 | No Give link on [fftc.org](https://www.fftc.org/) | **lapsed Give client** |

**Notes on dating.**
- **SFTP certificates were batch-issued.** The `*-sftp.int` certificates for jcf, nhf, jttw, jmt, thrivent, tmf and ws were all first issued on **2026-10-05**, and WaterStone was already live then. Read this as a platform-wide SFTP rollout, not a per-client milestone. The `cct`, `impactassets`, `vanguard` and `signatry` SFTP certificates followed on 3–4 November.
- **The earlier repo dates were too late**, as V3-08 found for CCT and Vanguard. The edges file's "certs 2026-08 to 2026-11" reflects certspotter's view of currently valid certificates only.

**Verdict on P-VEN-01** (inference, medium confidence):
- **What Give has shown.** Give has proven it can take Ren/iPhi software clients: The Signatry in 2021–22 and WaterStone in Nov 2026. Its active pipeline is concentrated in Ren's inherited iPhi community and faith book.
- **Why "systematic" goes too far.** Calling it systematic overstates the completed record: one late-stage and three early implementations have no production host yet. Stifel's Ren spend rose 61% in CY2025. Give has also lost five or more tenants.
- **Size of the exposure.** The Ren evidenced numerator at risk is about $5.9bn, or 1.8 points of the 27.9% "Ren technology in some form" share. Only WaterStone's $0.54bn (0.16 points) has moved.
- **Effect on V3-06.** The Signatry ($1.4bn) was never in the Ren numerator, so V3-06 needs no change on its account.

---

## 3. Vanguard Charitable: live? scope? (Q2)

| Item | Finding | Label |
|---|---|---|
| Contract | Vendor-issued release dated 2025-11-04: "modernize and scale its donor-advised fund recordkeeping function" ([PR Newswire](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html); [giveinteractive.com/post/vanguard](https://www.giveinteractive.com/post/vanguard)) | confirmed |
| Implementation timeline | sandbox 2025-08-06; staging 2025-10-02; production-named 2026-01-28; `vc-innov` 2026-10-09; `vanguard-sftp.int` 2026-11-03 ([crt.sh](https://crt.sh/?q=%25.giveinteractive.com); [certspotter](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names)) | inferred (environments) |
| Donor UX today | The homepage log-in is an on-page `#login` control using Auth0 SPA JS ([vanguardcharitable.org](https://www.vanguardcharitable.org/)). [client.vanguardcharitable.org](https://client.vanguardcharitable.org/) is CNAMEd to Akamai and returns `x-sfdc-trace-flags` and a Salesforce `saml/authn-request.jsp` redirect with Issuer `mygiving.vanguardcharitable.org`. **The donor portal is Salesforce Experience Cloud.** No giveinteractive.com link appears | confirmed |
| Salesforce history | A Slalom case study says Vanguard Charitable migrated donor and DAF data into Salesforce Financial Services Cloud and added Experience Cloud in 2023 ([Slalom](https://www.slalom.com/us/en/customer-stories/vanguard-charitable)). The 990s show Salesforce at $453,123 (FY2023) and $791,734 (CY2024 comp), plus Slalom and UST Global ([990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/full)) | confirmed |
| Scope from job posts | Search-engine snippets of Vanguard Charitable CX roles ("CX Research & Insights Specialist"; "CX Program & Service Design Lead (Apollo)") mention research into "new platforms (Salesforce Experience Cloud, Give Interactive accounting system, AWS integrations)". The pages returned 403 ([Teal listing](https://www.tealhq.com/job/cx-research-insights-specialist_7ea1a024fd13551579e8674f6092c69a458fc)) | inferred (snippet only) |
| Help/FAQ/donor notices | No donor notice of a platform change was found ([search, 2026-11-14](https://www.vanguardcharitable.org/portal/my-account)). The January 2026 Policies & Guidelines say nothing about a vendor ([PDF](https://www.vanguardcharitable.org/sites/default/files/2026-01/policies_and_guidelines_january_2026_011326_final_0.pdf)) | confirmed absence |
| Financial statements | FY2025 audited statements: software capitalised $0; Give Interactive not mentioned ([PDF](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)) | confirmed absence |
| 990 | Give Interactive is not in the top-5 for any year through FY2025 (CY2024 comp). The FY2026 return, due around May 2027 with extensions, is the first that could show it | confirmed absence |

**Answer.**
- **Live status:** not observed live for donors as of 2026-11-14.
- **Scope:** the scope is a **ledger, accounting and recordkeeping replacement**, inferred from the vendor's wording, the job-post phrase "accounting system" and the new SFTP data channel. It sits behind a **Salesforce Experience Cloud donor front end that Vanguard keeps**.
- **Two readings remain open:**
  - The ledger may already be live in parallel. Nothing public shows this.
  - The donor UX may later move to Give screens embedded in Salesforce. Nothing public shows this either.

---

## 4. Unresolved tenants; cct/jcf mappings (Q3)

| Slug (first cert) | Best candidate | Evidence | Label |
|---|---|---|---|
| `cct` (sandbox 2024-08-12; production 2025-06-11) | Chicago Community Trust | Slug, plus CCT's own Ren history and its current GiftingNetwork portal (§2). The "cct-prod" SSO label from earlier repo work was not re-checked | inferred (strong) |
| `jcf` (staging 2026-01-21; `jcf-grant-cart`, `jcf-innov`) | Jewish Communal Fund (NY) | Slug only. JCF is a $2.9bn sponsor with a documented portal change by FY2023. Other "JCF" organisations exist (Milwaukee, Montreal); the Montreal JCF launched a different portal in 2023 ([jcfmontreal.org](https://jcfmontreal.org/fund-advisor-portal-getting-started/)) | inferred (medium) |
| `jmacarthurtrust` (production 2025-05-01), `jmctdaf-staging` (2025-06-03), `jmt-sftp` | John MacArthur Charitable Trust, EIN 83-0981937, Newhall CA, NTEE X20 ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/830981937.json)) | Name match ("jmct" read as J. MacArthur Charitable Trust). No e-filed 990s. A Grace Community Church URL for the trust now returns 404 | inferred (medium) |
| `nhf` (staging 2025-10-23; production 2026-04-08; SFTP) | unresolved | National Heritage Foundation Inc (EIN 58-2085326, Ashburn VA) "supports United Charitable" and reported **$0 total assets at end-2022** ([990 TY2022](https://projects.propublica.org/nonprofits/organizations/582085326/202343179349306884/full)), so it is unlikely as a 2026 tenant in its own name. United Charitable (EIN 20-4286082, Ashburn; $0.18bn DAFs) is a related-org candidate. Its site returns 403. New Hampshire Charitable Foundation uses Foundant (`nhcf.fcsuite.com`), so it is excluded | unknown |
| `jttw` (staging 2025-10-15; production 2026-01-29; SFTP) | unresolved | No public match found | unknown |
| `tc-innov` (2026-11-09) | possibly Thrivent Charitable | Pattern only: `vc-innov` = Vanguard Charitable, `jcf-innov`, `ia-innov`. CCT uses `cct`, The Signatry uses `ts-`/`signatry` | unknown (weak inference) |
| `giveinteractive-clients.com` (wildcard since 2024-10-15) | marketing/client microsites | A search result showed `giftfundscanada.giveinteractive-clients.com/company`, but the host does not resolve from this session. Not verified | unknown |

---

## 5. Ownership: The Signatry and Give Interactive (Q4)

### 5.1 Filings across years (confirmed)

**Signatry Charitable Trust** (EIN 82-5070897; Sioux Falls SD; 170(b)(1)(A)(vi) public charity). Schedule R entry for GIVE INTERACTIVE LLC, EIN 84-4835291, 7171 W 95th St Ste 501, Overland Park KS:

| Return | Activity | Domicile | Share of income | Share of EOY assets | GP/managing | OwnershipPct |
|---|---|---|---|---|---|---|
| [CY2020](https://projects.propublica.org/nonprofits/organizations/825070897/202133199349322153/full) (also an amended copy) | Software development | KS | — | $6,101,573 | No | 0.99000 |
| [CY2021](https://projects.propublica.org/nonprofits/organizations/825070897/202203199349325815/full) | Investing | KS | — | — | No | 0.99000 |
| [CY2022](https://projects.propublica.org/nonprofits/organizations/825070897/202333199349322863/full) | Investing | KS | — | — | No | 0.99000 |
| [CY2023](https://projects.propublica.org/nonprofits/organizations/825070897/202443209349305764/full) | Investing | KS | $0 (UBI -$494,509) | $0 | **Yes** | 0.99 |
| [CY2024](https://projects.propublica.org/nonprofits/organizations/825070897/202543189349315279/full) | Software | **DE** | **-$2,791,186** | **$6,692,181** | **Yes** | 0.99 |

- **990-T.** "GIVE INTERACTIVE LLC" appears as a separate unrelated trade or business, with a partnership loss of -$494,509 (CY2023) and -$2,718,246 (CY2024). There is a $494,509 NOL carryover under activity code 510000 ([990-T CY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189339304508_public.xml)).
- **Schedule R Part V.** In CY2023–CY2024 the Trust answers **Yes** to "loans or loan guarantees to related organizations" and "receipt of interest … from a controlled entity", but **no line-2 itemisation appears in the XML**. The counterparty is not identified. Give is the obvious candidate, as the only operating controlled entity with losses, but that is inference.
- **Schedule L.**
  - The Trust reports loans to a "substantial contributor" and persons "related to substantial contributor". Original principals are $7,002,670, $1,670,000 and $328,904. The stated purposes are "purchasing of equity shares" (CY2020) and later "to sell shares and gain liquidity" (CY2023). All have board approval and written agreements.
  - **None names Give Interactive or its management.**
  - Whether these loans came from donor-advised funds matters under IRC §4958(c)(2), which makes loans from a DAF to its donor or advisor automatic excess-benefit transactions. The filings do not say where the loans came from: **unknown**.
- **Conflict-of-interest policy.** The Trust's CY2020 Schedule O says it is covered by Servant Foundation's conflict-of-interest policy and calls Servant "its supported organization".

**Servant Foundation (dba The Signatry)**, EIN 43-1890105, Overland Park KS:
- **Schedule R (FYE 3/2025):** lists Give Interactive LLC (Software, DE; controlling entity "NA") and Signatry Charitable Trust ("facilitates charitable giving in support of Servant Foundation", controlled = Yes) ([990](https://projects.propublica.org/nonprofits/organizations/431890105/202600439349302250/full)).
- **Transfers to the Trust (Part V type b):** $344.1m (FYE 3/2024) and $222.9m (FYE 3/2025). Over the same period Servant's DAF count fell from 2,870 to 463, while the Trust's rose from 86 (CY2023) to 2,564 (CY2024). **Inference:** The Signatry has consolidated its DAF book into the Trust, the entity that owns Give.
- **Ren payments:** paid Ren "managed services" in FYE 3/2021–3/2022 (§2).
- **Schedule L:** no Give-related entries.

**Context (confirmed).**
- Give's founder and CEO Lucas Cherry was EVP at The Signatry ([company page](https://www.giveinteractive.com/company)). A 2023 article describes him as Executive VP for Operations & Technology until 2019 ([The Racket News, 2023-01-23](https://www.theracketnews.com/p/who-is-he-gets-us-and-why-you-cant)).
- In FYE 3/2017 Servant paid KEM LLC, owned by board member Emmitt Mitchell, from the same street address Give now uses (7171 W 95th St Ste 501) ([990](https://projects.propublica.org/nonprofits/organizations/431890105/201820469349302202/full)). This shows the shared address only, nothing more.
- No public statement by The Signatry or Give about ownership was found.

### 5.2 Implications for Vanguard Charitable (inference unless cited)

1. **Structure.** Vanguard Charitable ($21.9bn) has chosen as recordkeeper a for-profit LLC that is about 99% owned and managed by the Signatry Charitable Trust. That Trust is itself a DAF sponsor ($0.80bn of DAFs, CY2024) and is controlled by or supports Servant Foundation (The Signatry). The client is roughly 14 times The Signatry's combined DAF assets ($0.80bn in the Trust plus $0.78bn at Servant).
2. **Tax law does not prohibit this.**
   - IRC §4958 reaches transactions with *disqualified persons* of the paying organisation, and for DAF sponsors also with donors, advisors and their related parties (§4958(c)(2), (f)(7)). Nothing in the public record makes The Signatry or Give a disqualified person of Vanguard Charitable, so paying Give at arm's length is an ordinary vendor relationship.
   - On The Signatry's side, Give's profits or losses flow through to the Trust as unrelated business income (§§511–512; partnership flow-through under §512(c)), which matches the 990-T.
   - If the Trust's 99% interest sat inside donor-advised funds, the excess-business-holdings rules applied to DAFs by §4943(e) would be engaged. Where the interest sits is **unknown** (P-GIV-03).
3. **The real issues are commercial and governance issues, not statutory ones:**
   - **Competitive data access.** A competing sponsor's affiliate processes Vanguard's donor identities, balances, grant recommendations and investment data. Protection depends entirely on contract terms (data segregation, non-use, audit, change of control), which are not public (P-GIV-04).
   - **Vendor continuity.** Give reports losses that its charitable owner funds: CY2024 share of income -$2.79m. Vanguard's recordkeeping continuity depends partly on another charity's willingness to keep capitalising a for-profit subsidiary.
   - **Director oversight.** Vanguard Charitable's directors owe the usual state-law duties of care in selecting and monitoring a critical vendor. The public record does not show whether the ownership was disclosed or weighed in Vanguard's "comprehensive review" ([release](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html)). This report cites no specific state statute because Vanguard Charitable's domicile statute was not checked.
   - **Market structure.** A sponsor-owned platform now serves Vanguard, CCT, ImpactAssets, JCF, WaterStone and others. The Signatry gains an industry-wide view and recurring software revenue, which echoes the RCF/Ren pattern but inverted: there the vendor sponsors a DAF, here a sponsor owns the vendor.

---

## 6. Corrections to repo files

| File / edge | Correction |
|---|---|
| EA002 notes | "Ownership unknown" is superseded by EB001: Signatry Charitable Trust holds 99% in CY2020–CY2024. |
| EA003 / EA004 | WaterStone cut over to Give on 2026-11-01 (first-party notice). Stellar payments ran FYE 3/2014–3/2025, not just FY2025. |
| EA005 | CCT is not a current Ren client. RenPSG recordkeeping ended after FY2020 (EB004) and the incumbent portal is GiftingNetwork (EB005). CCT Give hosts date from 2024-08, not "2026-09". |
| EA006 | JCF paid Ren for "previous donor portal support" in FY2023 (EB006). JCF is ex-Ren, current vendor unknown. |
| EA007 | ImpactAssets has announced a 2026-09-08 "DAF Hub" launch on a first-party page. The login is still iPhi as of 2026-11-14. |
| EA001 | Vanguard's donor portal is Salesforce Experience Cloud (EB008), not just "Auth0/Akamai". |
| queue-vendor-scope §1.3 "No banks or wirehouses … apart from Stifel" | Unchanged. Add FFTC as a lapsed paying client (EB007). |
| Ren share at risk "about $6.5bn" | $5.86bn: IA 3.63 + TMF 0.60 + Thrivent 0.59 + WaterStone 0.54 + Stifel 0.49. The earlier figure does not reproduce from the DAFRC FY2024 rows for these five sponsors. |

---

## 7. Source register

| ID | Source | Used for |
|---|---|---|
| S1 | [crt.sh %.giveinteractive.com](https://crt.sh/?q=%25.giveinteractive.com) | Give host first and last certificate dates |
| S2 | [certspotter giveinteractive.com](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names) | Recent hosts (SFTP, `*-innov`) |
| S3 | [crt.sh %.iphiview.com](https://crt.sh/?q=%25.iphiview.com); [crt.sh %.stellartechsol.com](https://crt.sh/?q=%25.stellartechsol.com); [crt.sh %.donorfirst.org](https://crt.sh/?q=%25.donorfirst.org) | Ren-side CT (wildcard only) |
| S4 | [waterstone.org/login](https://waterstone.org/login/) | WaterStone cut-over 2026-11-01 |
| S5 | [impactassets.org](https://impactassets.org/); [DAF platform transition](https://impactassets.org/daf-platform-transition/) | ImpactAssets login and announced launch |
| S6 | [tmf.iphiview.com](https://tmf.iphiview.com/tmf/LogIn/tabid/54/Default.aspx); [infaith.iphiview.com](https://infaith.iphiview.com/infaith/LogIn/tabid/444/Default.aspx); [sci.iphiview.com](https://sci.iphiview.com/sci/LogIn/tabid/444/Default.aspx); [stifel.com DAF page](https://www.stifel.com/individual/donor-advised-funds) | Live iPhi portals |
| S7 | [donorportal.cct.org](https://donorportal.cct.org/) | CCT GiftingNetwork portal |
| S8 | [dns.google jcfny.donorfirst.org](https://dns.google/resolve?name=jcfny.donorfirst.org&type=A) | JCF DonorFirst host |
| S9 | [client.vanguardcharitable.org](https://client.vanguardcharitable.org/); [vanguardcharitable.org](https://www.vanguardcharitable.org/); [Slalom case study](https://www.slalom.com/us/en/customer-stories/vanguard-charitable) | Vanguard donor UX = Salesforce |
| S10 | [PR Newswire 2025-11-04](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html) | Vanguard scope wording |
| S11 | [Teal job listing (snippet)](https://www.tealhq.com/job/cx-research-insights-specialist_7ea1a024fd13551579e8674f6092c69a458fc) | "Give Interactive accounting system" |
| S12 | [Vanguard FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf); [Policies & Guidelines Jan 2026](https://www.vanguardcharitable.org/sites/default/files/2026-01/policies_and_guidelines_january_2026_011326_final_0.pdf) | Absence of Give disclosure |
| S13 | Signatry Charitable Trust 990s: [CY2020](https://projects.propublica.org/nonprofits/organizations/825070897/202133199349322153/full), [CY2021](https://projects.propublica.org/nonprofits/organizations/825070897/202203199349325815/full), [CY2022](https://projects.propublica.org/nonprofits/organizations/825070897/202333199349322863/full), [CY2023](https://projects.propublica.org/nonprofits/organizations/825070897/202443209349305764/full), [CY2024](https://projects.propublica.org/nonprofits/organizations/825070897/202543189349315279/full); [990-T CY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189339304508_public.xml) | Ownership, Sched L/R, 990-T |
| S14 | Servant Foundation 990s: [FYE 3/2021](https://projects.propublica.org/nonprofits/organizations/431890105/202210469349301641/full), [FYE 3/2022](https://projects.propublica.org/nonprofits/organizations/431890105/202320469349302877/full), [FYE 3/2025](https://projects.propublica.org/nonprofits/organizations/431890105/202600439349302250/full) | Ren payments; Sched R |
| S15 | 990 series per client (object ids in the timeline CSV): [WaterStone FYE 3/2025](https://projects.propublica.org/nonprofits/organizations/751750059/202610409349301411/full), [ImpactAssets CY2024](https://projects.propublica.org/nonprofits/organizations/262048480/202543169349307999/full), [Thrivent CY2025](https://projects.propublica.org/nonprofits/organizations/411802412/202612669349300236/full), [Stifel CY2025](https://projects.propublica.org/nonprofits/organizations/842049692/202642609349301859/full), [Minneapolis FYE 3/2014](https://projects.propublica.org/nonprofits/organizations/416029402/201520279349300012/full), [CCT FY2020](https://projects.propublica.org/nonprofits/organizations/362167000/202112239349302351/full), [JCF FY2023](https://projects.propublica.org/nonprofits/organizations/237174183/202410969349301036/full), [FFTC CY2023](https://projects.propublica.org/nonprofits/organizations/566047886/202433209349318318/full) | Vendor payments by year |
| S16 | [National Heritage Foundation TY2022](https://projects.propublica.org/nonprofits/organizations/582085326/202343179349306884/full); [United Charitable 990s](https://projects.propublica.org/nonprofits/organizations/204286082); [nhcf.org/mynhcf](https://www.nhcf.org/mynhcf/) | `nhf` candidates |
| S17 | [Give company page](https://www.giveinteractive.com/company); [The Racket News 2023-01-23](https://www.theracketnews.com/p/who-is-he-gets-us-and-why-you-cant) | Founder history; no ownership disclosure |
| S18 | [thesignatry.giveinteractive.com/log-in](https://thesignatry.giveinteractive.com/log-in); [fftc.org](https://www.fftc.org/); [kzcf.org](https://kzcf.org/) | Live / lapsed tenants |
