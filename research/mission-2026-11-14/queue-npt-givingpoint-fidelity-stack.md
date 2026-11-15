# NPT GivingPoint program book, NPT–Ren payment trail and the Fidelity Charitable stack

Queue items: **P-REN-03** (GivingPoint white-label book), **P-VEN-03** (what NPT pays Ren, and why no Ren payee appears in Part VII-B), **P-QA1-02** (platform vendors inside Fidelity Charitable and NPT GivingPoint). Prepared 2026-11-15 by the GivingPoint agent.

**Method.** All reads were public and unauthenticated:
- unauthenticated `GET`s of site roots and their public JavaScript bundles;
- DNS through dns.google;
- certificate-transparency (CT) logs through crt.sh, with certspotter where crt.sh failed;
- IRS e-file XML from the GivingTuesday 990 data lake, cross-referenced to ProPublica;
- UK charity accounts, read through the opencharities.uk mirror of Charity Commission filings, because the Commission's own site returned 403;
- web search.

There were no log-ins, form submissions, API calls beyond public version endpoints, or outreach. Requests were kept to about 1 per second per host.

**Evidence tags** follow the repo convention: [F] first-party or filing, [I] inference, [S] secondary or search summary.

**Recency.** Only 2021-or-later evidence supports current-state findings. One 2018 J.P. Morgan PDF is used only to interpret a code label, and is flagged where it appears.

Outputs:
- [`npt-givingpoint-programs-2026.csv`](../../data/mission-2026-11-14/npt-givingpoint-programs-2026.csv): 15 rows, of which 13 are live programs and 2 are client codes with no live site.
- [`relationship-graph-edges-additions-12.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-12.csv): EL001–EL028.
- [`queue-proposals-givingpoint.csv`](../../data/mission-2026-11-14/queue-proposals-givingpoint.csv): P-GPT-01 to P-GPT-03.

---

## 1. Findings

| Item | Finding | Confidence |
|---|---|---|
| **P-REN-03: program census** | **One Ren-built GivingPoint codebase serves 13 live NPT-family program sites, and names 16 client codes.** The production bundle at `nptgivingpoint.org` and its lazy chunks branch on these client codes: `npt`, `jpmc`, `jpms`, `icgf`, `ubs`, `wells`, `bmo`, `glenmede`, `tolleson`, `pitcairn`, `nptplus`, `npttransatlantic`, `nptuk`, `nptukusd`, `rathbones`, `cazenove` ([main bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js)) [F].<br>Thirteen of the codes have a live site. Every live site is either on the `ren-workload-02` ELB or on the iPhi Global Accelerator pair. Every one shares one AWS WAF id (`55fe72368c58/bd2698c5ab04`), links `renpsg.atlassian.net`, and states "GivingPoint is a registered trademark of National Philanthropic Trust" [F].<br>**New this pass (10 sites):**<br>- J.P. Morgan Charitable *Gift* Fund (`jpmgiftfund.org`)<br>- UBS (`donoradvisedfundgiving.org`)<br>- BMO (`bmodaf.org`)<br>- Glenmede (`glenmededaf.com`)<br>- Tolleson (`tollesondaf.org`)<br>- Pitcairn (`pitcairndaf.org`)<br>- NPT UK (`nptukgiving.org`)<br>- NPT Transatlantic (`npttransatlanticdaf.org`)<br>- Rathbones (`rathbonesdaf.org`)<br>- Cazenove Capital (`cazenovecapitaldaf.org`)<br>The `wells` and `nptplus` codes have no live site. | high (sites, hosting, sponsor text); unresolved for wells and nptplus |
| **P-REN-03: sponsors** | 10 of the programs are sponsored by NPT US (EIN 23-7825575): NPT direct, JPM ×2, ICGF, UBS, BMO, Glenmede, Tolleson, Pitcairn and Transatlantic. NPT Transatlantic Ltd (charity 1153376) is a **disregarded entity of NPT** on Schedule R. Three programs are UK-sponsored by **NPT UK** (charity 1181128): NPT UK direct, Rathbones and Cazenove [F]. | high |
| **P-REN-03: book size** | **No program-level asset figure is public for any of the programs.** Only entity totals are public:<br>- NPT Schedule D DAF value is **$55,895,378,438 at FY6/2025** (20,691 DAFs; FY6/2024 $42,119,335,128). This total includes the direct NPT book and all US private-label programs, plus Transatlantic ([990](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/full)).<br>- NPT UK net assets were **£367.1m** (30 Jun 2025).<br>- NPT Transatlantic's register assets were **£202.9m** (30 Jun 2025); Schedule R gives $279.7m.<br>NPT's own log-in also goes to GivingPoint, so **the whole NPT book is on GivingPoint**. The white-label share of $55.9bn is unknown. | confirmed (totals); unknown (split) |
| **P-REN-03: UBS / BNY** | **UBS resolved:** the live UBS program is `donoradvisedfundgiving.org`, which is Ren GivingPoint, "UBS clients … NPT Donor-Advised Fund accounts". The legacy iPhi UBS hosts point to `donoradvisedfund.ubs.com` (67.216.67.101), which still does not answer, so that target is a dead legacy redirect, not a separate platform. **BNY Mellon CGF:** `bnymelloncharitablegiftfund.org` still returns HTTP 502. Nothing in the GivingPoint build references BNY, so it is not an NPT program on this evidence. | high (UBS); unchanged (BNY) |
| **P-VEN-03: amount** | **Unknown.** No NPT-family filing names Ren, Stellar or iPhi:<br>- NPT US 990s for FY2024 and FY2025;<br>- NPT UK and NPT Transatlantic 2025 accounts.<br>The plausible ceiling is NPT's Part IX information-technology line: **$5,871,282** (FY2025), up from $3,649,680 (+$2.22m) [F]. | confirmed absence |
| **P-VEN-03: why absent** | Ranked explanations:<br>(1) **Classification** [I]: a SaaS, hosting or licence fee is booked in Part IX line 14 and treated as a purchase rather than "independent contractor" compensation. This is a filer's choice: Cleveland Foundation, for example, does list Stellar "hosting & software licence" in VII-B.<br>(2) **Below threshold:** if Ren were reported in VII-B, it would have been paid ≤$220,927. That is implausible for 13 sites and 20,691 DAFs when NCF pays Stellar $2.50m [I].<br>(3) **Another payer:** this is now partly tested. The UK affiliates *receive* technology from NPT US under service agreements, paying NPT US £72,000 (NPT UK) and £77,554 (Transatlantic). They are not alternative payers to Ren. Direct payment by partner banks is not excluded. NPT itself books **"MAINTENANCE & HOSTING" revenue** of $480,556 (FY2025) and $784,533 (FY2024), which suggests NPT recharges hosting to an undisclosed counterparty [F/I]. | medium (ranking is inference) |
| **P-QA1-02: Fidelity Charitable** | **No third-party DAF platform vendor is visible.** Schedule O says FMR provides "RECORD-KEEPING, SYSTEMS, ADMINISTRATION…" under a services agreement. FMR LLC was paid $159.9m; Part IX IT is $0; the charity has 0 employees.<br>The donor log-in is on `charitablegift.fidelity.com` behind Akamai, and the CDN origin is `fmrcloud.com`.<br>The visible vendors are marketing and edge vendors only: Akamai, Salesforce Marketing Cloud and Pardot, Adobe (Analytics, AEM), Segment, Nuance, Mailgun, Microsoft 365, DocuSign and Stripe.<br>**No Ren, iPhi or Give marker** was found. Any recordkeeping vendor would sit inside FMR, where it cannot be seen. | high (visible stack); unknown (inside FMR) |
| **P-QA1-02: NPT GivingPoint** | **The vendor is Ren**, for the portal, the API and, probably, the iPhi sub-ledger (see `queue-npt-dafgiving360-misc.md` §1). Ren operates the AWS layer (WAF, ELB, Global Accelerator). NPT runs **Salesforce** (Service Cloud and Pardot by SPF and job ads [S/F]), Microsoft 365, Proofpoint and Atlassian. The front end loads Hotjar, Google Analytics and reCAPTCHA (CSP). NPT's SPF still authorises **67.216.67.30**, in the legacy Stellar/iPhi 67.216.67.0/24 range [F]. That is consistent with iPhi-generated mail [I]. | high |

**Implications for repo conclusions.**
- **The Ren numerator is unchanged.** NPT was already counted at its full Schedule D value. The UK entities are outside DAFRC's US denominator.
- **The concentration and SPOF reading is stronger.** Eight US institution-branded programs (J.P. Morgan ×2, UBS, BMO, Glenmede, Tolleson, Pitcairn and ICGF) depend, together with NPT direct, NPT UK and NPT Transatlantic, on one Ren build and two Ren network front doors. For the bank and wealth channel, a Ren outage would hit NPT's private-label partners and GS PWM together.
- **Census status changes.** The census row for UBS (`unknown`) can be set to active, as a within-Ren move to GivingPoint. The pitcairn and glenmede iPhi tenant paths now redirect to GivingPoint sites, which is the same pattern as NPT, JPM and ICGF.

---

## 2. P-REN-03: GivingPoint program census

### 2.1 How the programs were found
1. **Client codes from the shared build.** The `nptgivingpoint.org` main bundle and 55 lazy chunks contain conditionals such as `h.name!=="ubs"&&h.name!=="jpms"&&h.name!=="bmo"&&h.name!=="glenmede"&&h.name!=="rathbones"&&h.name!=="tolleson"&&h.name!=="nptplus"&&h.name!=="cazenove"&&h.name!=="npttransatlantic"&&h.name!=="pitcairn"&&h.name!=="icgf"`. Others include `$.name==="jpmc"`, `this.client==="wells"` and `toUpperCase()==="NPTUKUSD"` ([main bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js)) [F].
2. **Domain discovery.** For each code, candidate names were checked on dns.google. The pattern `<brand>daf.org` hit for Tolleson, Pitcairn, BMO and Rathbones, and `.com` hit for Glenmede. The iPhi tenant paths gave further hits:
   - `jpms.iphiview.com/jpms` → `jpmgiftfund.org`;
   - `pitcairn.iphiview.com/pitcairn` → `pitcairndaf.org`;
   - `npt.iphiview.com/glenmede` → `glenmededaf.com/glen`;
   - `npt.iphiview.com/nptukusd` → `npttransatlanticdaf.org`.

   NPT's own home pages supplied `nptukgiving.org` ([nptuk.org](https://www.nptuk.org/)). A search summary of a UBS tutorial supplied `donoradvisedfundgiving.org` [S]. That site was then verified first-hand.
3. **Verification per site.** Each site was checked for:
   - HTTP 200;
   - an Angular GivingPoint shell with the shared AWS WAF challenge (`55fe72368c58/bd2698c5ab04`);
   - a site-specific `main-*.js` bundle containing a program sentence ("… is a donor-advised fund offered in conjunction with (the) National Philanthropic Trust (NPT)") or an NPT UK / Transatlantic copyright;
   - a `renpsg.atlassian.net` link;
   - DNS pointing to the `ren-workload-02` ELB (54.88.200.68 / 44.223.132.165; `www` CNAME `ren-workload-02-public-1461601509.us-east-1.elb.amazonaws.com`) or to the iPhi Global Accelerator pair (35.71.183.32 / 13.248.164.2).

   NPT-owned defensive `.com` domains (`bmodaf.com`, `jpmgiving.com`, `nptgivingpoint.com`, `icgfdaf.com`, `tollesondaf.com`, `pitcairndaf.com`, `jpmorgandaf.com`, `mynptuk.org`) sit on 209.17.116.163 and 301 to the `.org` sites.

### 2.2 Program table (summary; full fields in the CSV)

| ID | Program (site) | Institution | Sponsor | Hosting | First CT cert | Bundle evidence |
|---|---|---|---|---|---|---|
| GP01 | NPT GivingPoint ([nptgivingpoint.org](https://nptgivingpoint.org/)) | NPT direct | NPT | ELB | 2020-10-29 | [bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js) |
| GP02 | J.P. Morgan Charitable Giving Fund ([jpmgiving.org](https://jpmgiving.org/)) | J.P. Morgan Private Bank | NPT | ELB | 2021-06-04 | [bundle](https://jpmgiving.org/main-JBUINBFD.js) |
| GP03 | J.P. Morgan Charitable Gift Fund ([jpmgiftfund.org](https://jpmgiftfund.org/)) | J.P. Morgan; code `jpms` (Securities channel [I]) | NPT | ELB | 2022-03-16 | [bundle](https://jpmgiftfund.org/main-W7WT45DD.js) |
| GP04 | ICGF Donor-Advised Fund ([icgfdaf.org](https://icgfdaf.org/)) | NPT program for independent advisers | NPT | GA pair | 2025-06-02 | [bundle](https://icgfdaf.org/main-2IGH5MJZ.js) |
| GP05 | UBS ([donoradvisedfundgiving.org](https://donoradvisedfundgiving.org/)) | UBS (US) | NPT | ELB | 2021-09-23 | [bundle](https://donoradvisedfundgiving.org/main-5PZW2EPZ.js) |
| GP06 | BMO Donor-Advised Fund Program ([bmodaf.org](https://bmodaf.org/)) | BMO | NPT | ELB | 2026-02-15 (certspotter; current certs only) | [bundle](https://bmodaf.org/main-CME7MTNM.js) |
| GP07 | Glenmede Donor-Advised Fund ([glenmededaf.com](https://glenmededaf.com/)) | Glenmede | NPT | ELB | 2017-02-10 (domain predates GivingPoint) | [bundle](https://glenmededaf.com/main-2GMDDIKR.js) |
| GP08 | Tolleson Wealth Management DAF Program ([tollesondaf.org](https://tollesondaf.org/)) | Tolleson Wealth Management | NPT | GA pair | 2025-02-10 | [bundle](https://tollesondaf.org/main-N3M4QVUS.js) |
| GP09 | Pitcairn Donor-Advised Fund ([pitcairndaf.org](https://pitcairndaf.org/)) | Pitcairn | NPT | GA pair | 2025-04-28 | [bundle](https://pitcairndaf.org/main-TXNWGRMW.js) |
| GP10 | NPT UK GivingPoint ([nptukgiving.org](https://nptukgiving.org/)) | NPT UK direct | NPT UK | ELB | 2021-12-16 | [bundle](https://nptukgiving.org/main-4ALO56BR.js) |
| GP11 | NPT Transatlantic GivingPoint ([npttransatlanticdaf.org](https://npttransatlanticdaf.org/)) | NPT Transatlantic direct | NPT Transatlantic (disregarded entity of NPT) | GA pair | 2025-06-03 | [bundle](https://npttransatlanticdaf.org/main-L5UEGKW2.js) |
| GP12 | Rathbones Donor-Advised Fund ([rathbonesdaf.org](https://rathbonesdaf.org/)) | Rathbones | NPT UK | GA pair | 2024-11-20 | [bundle](https://rathbonesdaf.org/main-GUDOXMXE.js) |
| GP13 | Cazenove Capital DAF Programme ([cazenovecapitaldaf.org](https://cazenovecapitaldaf.org/)) | Cazenove Capital (Schroders) | NPT UK | ELB | 2021-09-28 | [bundle](https://cazenovecapitaldaf.org/main-LSW43PUG.js) |
| GP14 | `wells` (code only) | Wells Fargo [S] | NPT [S] | — | — | code branch only |
| GP15 | `nptplus` (code only) | unknown | unknown | — | — | code branch only |

CT dates come from crt.sh unless marked; crt.sh covers full history. DNS evidence uses `https://dns.google/resolve?name=<host>&type=A` for each host in the CSV.

**Supporting third-party confirmation (2021+):**
- **Rathbones**, 2025-08-26: "Rathbones offers donor advised funds in partnership with National Philanthropic Trust UK (NPT UK), a registered charity" ([rathbones.com](https://www.rathbones.com/en-gb/wealth-management/media-centre/news-and-comment/legal-complexity-deterring-wealthy-leaving-money-charity)) [F].
- **NPT UK's 2025 accounts** list Cazenove Capital and UBS among its principal investment managers ([accounts](https://opencharities.uk/ew/1181128/files/2025-06-30-accounts.md)) [F].
- **J.P. Morgan.** A J.P. Morgan PDF calls the "J.P. Morgan Donor Advised Fund … offered in conjunction with National Philanthropic Trust", with transactions "through J.P. Morgan Securities LLC" ([jpmorgan.com PDF](https://www.jpmorgan.com/content/dam/jpm/securities/documents/DAFExecutiveSummary.pdf)). The PDF was created in 2018, so it is **pre-2021** and is used only to interpret the `jpms` label [I].
- **ICGF.** NPT owns the ICGF trademark ([Justia trademarks](https://trademarks.justia.com/owners/national-philanthropic-trust-4033609)) [S].

### 2.3 Book sizing

| Entity | Measure | Value | Source |
|---|---|---|---|
| NPT (US), all programs incl. Transatlantic | Schedule D DAF value, end of year FY6/2025 | $55,895,378,438 (20,691 DAFs) | [990 FY2025](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/full) |
| NPT (US) | Schedule D DAF value, end of year FY6/2024 (= DAFRC FY2024) | $42,119,335,128 (17,940 DAFs) | [990 FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml) |
| NPT annual report FY25 | AUM; accounts | $56.4bn; 20,561 DAF accounts. UK affiliate figures "are not included" | [annual report](https://www.nptrust.org/annual-reports/npt-annual-report/) |
| NPT Transatlantic Ltd (1153376) | Schedule R end-of-year assets; register assets | $279,696,494; £202,919,462 (30 Jun 2025) | [990 Sched R](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/full); [opencharities](https://opencharities.uk/ew/1153376) |
| NPT UK Ltd (1181128), incl. Rathbones and Cazenove | Total net assets | £367,144,508 (30 Jun 2025; £180.1m in 2024) | [2025 accounts](https://opencharities.uk/ew/1181128/files/2025-06-30-accounts.md) |
| Any single private-label program | Assets | **not public** | none of the 13 sites, partner pages or filings checked |

**Reading** [I]:
- The "GivingPoint book" is all of NPT US's $55.9bn plus about £0.37bn at NPT UK.
- The **white-label sub-book** (JPM ×2, UBS, BMO, Glenmede, Tolleson, Pitcairn, plus ICGF as an adviser-channel brand) cannot be separated from the direct NPT book on public evidence (P-GPT-03).
- For Ren-share arithmetic this split does not matter, because NPT is already counted in full.

---

## 3. P-QA1-02: platform vendors inside Fidelity Charitable and NPT GivingPoint

### 3.1 Fidelity Charitable (FMR stack)

| Layer | Evidence | Vendor | Tag |
|---|---|---|---|
| Recordkeeping, systems and administration | Schedule O: "FIDELITY CHARITABLE ENGAGES FMR LLC … SERVICES PROVIDED BY FMR: RECORD-KEEPING, SYSTEMS, ADMINISTRATION, FUNDRAISING, INVESTMENT ADVISORY SERVICES…". Costs borne by FMR "are not separately stated" ([990 FY6/2025](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/full)) | FMR LLC ($159,901,679 in VII-B). Sub-vendors not disclosed | [F] |
| Return shape | Part IX IT $0; management fees $179.9m; 0 employees; 73 contractors paid more than $100k. The rest of the VII-B top five are McKinsey ($11.8m), UBS Financial Services ($11.8m), ICONIQ ($10.6m) and Wells Fargo Advisors ($3.4m), all investment or consulting | none is a platform vendor | [F] |
| Donor log-in and web | `charitablegift.fidelity.com` and `www.fidelitycharitable.org` CNAME `*.edgekey.net` ([dns.google](https://dns.google/resolve?name=charitablegift.fidelity.com&type=CNAME)). CT includes `fidelitycharitable-cloudfront.fc-prod.aws.fmrcloud.com` ([certspotter](https://api.certspotter.com/v1/issuances?domain=fidelitycharitable.org&include_subdomains=true&expand=dns_names)) | Akamai; AWS under FMR's own cloud account | [F] |
| Marketing | `cloud.content.fidelitycharitable.org` CNAME `*.cp-sap.sfmc-content.com` ([dns.google](https://dns.google/resolve?name=cloud.content.fidelitycharitable.org&type=CNAME)). SPF: `_fidelitynets.fmr.com`, `aspmx.pardot.com`, `mailgun.org`. A Fidelity Charitable job ad (removed 2026-03-30) names "Salesforce Marketing Cloud, Segment CDP, and Adobe Experience Manager" ([Built In](https://builtin.com/job/director-marketing-technology-engineering/8794296)) | Salesforce (SFMC, Pardot), Segment, Adobe, Mailgun | [F] |
| Other | `nuance.fidelitycharitable.org`; `sitecatalyst.*` (Adobe Analytics); `fctms.fidelitycharitable.org` CNAME `fidelitycgf.edge.nc0.co` (provider unidentified); MX Microsoft 365; DocuSign TXT; Stripe for nonprofit EFT (repo E102) | Nuance [I], Adobe, Microsoft, DocuSign, Stripe | [F]/[I] |
| Ren / iPhi / Give | No host on Ren IPs, no Stellar or iPhi strings, no Give tenant in the Fidelity CT set | — | absence |

A search summary also mentions Fidelity "Charitable Technology" engineering postings (Angular/Spring Boot, Salesforce, AWS) [S]. The postings themselves returned 404, so they are not relied on.

**Answer** [I]: Fidelity Charitable's platform is FMR-built or FMR-procured, and any vendor sits behind the FMR services agreement. Public evidence cannot attribute a DAF-platform vendor. The Ren ">60%" arithmetic still cannot use Fidelity.

### 3.2 NPT GivingPoint

| Layer | Evidence | Vendor | Tag |
|---|---|---|---|
| Portal, API and probable ledger | 13 GivingPoint sites, all on Ren infrastructure; Ren Jira links; "NPT iPhi Statuspage"; DonorView naming (prior work) | **Ren** (Stellar/iPhi lineage) | [F]/[I] |
| Edge | AWS WAF (one shared id), ELB `ren-workload-02`, Global Accelerator; IIS/ASP.NET origin | AWS, operated by Ren | [F] |
| Product ownership | NPT staff page: Rachel Mele Kramarski "leads development of the GivingPoint portal" ([nptrust.org](https://www.nptrust.org/?p=9259)) | NPT owns the product; Ren builds and hosts it [I] | [F] |
| CRM and marketing | SPF includes `_spf.salesforce.com` and `aspmx.pardot.com`, plus a `pardot929923` verification ([dns.google](https://dns.google/resolve?name=nptrust.org&type=TXT)). Job ads for an NPT Salesforce Service Cloud specialist and a Salesforce DevOps engineer appear in search summaries [S] | Salesforce | [F]/[S] |
| Mail and collaboration | MX Proofpoint (`pphosted.com`); SPF Microsoft 365, Atlassian; DocuSign TXT | Proofpoint, Microsoft, Atlassian, DocuSign | [F] |
| Legacy iPhi mail | SPF `ip4:67.216.67.30`, in the 67.216.67.0/24 range that holds legacy iPhi and UBS hosts (repo census) | Stellar legacy range | [F]; purpose [I] |
| Front-end trackers | CSP allows Hotjar, Google Analytics/Tag Manager, reCAPTCHA, Vimeo, Typekit ([response headers](https://www.nptgivingpoint.org/)) | — | [F] |

---

## 4. P-VEN-03: what NPT pays Ren, and why Part VII-B shows no Ren payee

### 4.1 Facts

| Item | FY6/2024 | FY6/2025 | Source |
|---|---|---|---|
| Part VII-B top five | 5th-highest $345,954 | ICONIQ $2,860,300; RSM $942,249; Riess $260,130; Disciplina $253,426; Patterson Belknap $220,927. 9 contractors paid more than $100k | [990 FY2025](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/full) |
| Part IX line 14, information technology | $3,649,680 | $5,871,282 (program $1,996,236; management $2,348,513; fundraising $1,526,533) | same; [FY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml) |
| Part IX line 11g, other fees for services | $2,500,886 | $1,461,666 | same |
| Part IX line 24, "PROGRAM FEES" | $4,077,996 | $4,295,780 | same |
| Part VIII, "MAINTENANCE & HOSTING" revenue (code 561000, exempt function) | $784,533 | $480,556 | same |
| Part VIII, "ADMINISTRATIVE FEES" revenue | $710,557 | $632,700 | same |
| Schedule R, related organisations | — | Disregarded: NPT Transatlantic, CC Private Equity LLC, MME Mission Hope LLC, NPT Fiscal Sponsorship LLC, Donari LLC and others. Related exempt: 6 supporting organisations plus NPT UK. Part V transactions are only gifts, services (L) and reimbursements (Q) with supporting organisations, all of which NPT performs or receives. **No technology entity** appears | same |
| NPT UK 2025 accounts | — | "administration, management information systems and technology functions of the charity are provided to NPT UK by … NPT Transatlantic Limited … and National Philanthropic Trust of the U.S." Purchases from NPT US: £72,000 | [accounts](https://opencharities.uk/ew/1181128/files/2025-06-30-accounts.md) |
| NPT Transatlantic 2025 accounts | — | Functions "provided … by … Buzzacott LLP of the UK and National Philanthropic Trust of the US". Purchases: £77,554 | [accounts](https://opencharities.uk/ew/1153376/files/2025-06-30-accounts.md) |
| Ren, Stellar or iPhi strings | none | none | NPT XML; UK accounts |

### 4.2 Assessment
1. **The amount is unknown.** No filing or statement gives it. The only defensible bound is NPT's Part IX IT line of $5.87m (FY2025), assuming Ren is paid by NPT US and booked there [I].
   - The rise of $2.22m (+61%) from FY2024 coincides with new GivingPoint sites. CT first dates: Rathbones 2024-11, Tolleson 2025-02, Pitcairn 2025-04, ICGF and Transatlantic 2025-06.
   - That timing is consistent with expanded Ren work, but it does not prove it [I].
2. **Why there is no VII-B line.** Ranked [I]:
   - **(a) Treated as a purchase or licence, not contractor compensation.** Practice varies: Cleveland Foundation reports Stellar "hosting & software licence" in VII-B (repo §3), and NPT evidently does not.
   - **(b) Paid by another entity.** NPT UK and Transatlantic are ruled out as substitute payers, because both buy technology *from* NPT US. Partner institutions paying Ren directly for their branded sites is not ruled out. NPT books "MAINTENANCE & HOSTING" revenue, which shows NPT *charges* someone for hosting; the counterparty is undisclosed (P-GPT-01).
   - **(c) Paid ≤$220,927 and so below the top five.** This is least plausible. NCF pays Stellar $2.50m for one sponsor's iPhi (repo [`form990-contractors-harvest-full.csv`](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv)), and NPT runs 13 sites over about 20,700 DAFs.
3. **Licence or full outsourcing?** NPT employs 310 people, pays no administrator, and its UK accounts say technology is provided *by NPT US*. Together these support **"Ren = licensed technology and hosting vendor to NPT US, which re-provides it across the NPT family"**. They do not support "Ren administers NPT". This agrees with the A1 recommendation in `queue-npt-dafgiving360-misc.md`.

---

## 5. Corrections and updates to repo files (proposed; not applied)
- **[`ren-iphi-tenant-census.csv`](../../data/mission-2026-11-14/ren-iphi-tenant-census.csv)**:
  - The UBS rows (`ubs.iphiview.com/ubs`, `iphi.stellartechsol.com/ubs`) can move from `unknown` to `active (within-Ren move to GivingPoint, donoradvisedfundgiving.org)`. The legacy redirect target is dead.
  - Add `pitcairn.iphiview.com/pitcairn`, `jpms.iphiview.com/jpms`, `npt.iphiview.com/glenmede` and `npt.iphiview.com/nptukusd` as GivingPoint redirects. All are NPT-sponsored, so they add no new sponsor EIN.
- **[`queue-ren-iphi-attrition.md`](queue-ren-iphi-attrition.md) §1 item 3** lists only J.P. Morgan and ICGF as NPT white-label programs. Extend the list: JPM Gift Fund, UBS, BMO, Glenmede, Tolleson and Pitcairn (US), plus Rathbones and Cazenove (UK, NPT UK).
- **[`queue-npt-dafgiving360-misc.md`](queue-npt-dafgiving360-misc.md) §1 open item** "whether private-label programs (UBS, Wells Fargo) use the same stack": answered for UBS (yes). Wells Fargo is unresolved, with a code branch only.
- **Fidelity VII-B, for the record.** Fidelity's own FY2025 VII-B top five are FMR, McKinsey, UBS Financial Services, ICONIQ and Wells Fargo Advisors. None of them is UST, Slalom or Salesforce. The sentence in [`queue-vendor-scope-ren-denominator.md`](queue-vendor-scope-ren-denominator.md) §3 that names those three covers the Fidelity, DAFgiving360 and Vanguard returns together. That sentence was not re-checked here, so attribute each name to its filer before reuse.

## 6. Limits
- **Client codes can be stale.** `wells` and `nptplus` may be dead branches. All 13 live sites are confirmed independently.
- **Sites were found by guessing domains and following redirects**, not from a vendor list. Other GivingPoint sites using other naming patterns may exist (P-GPT-02).
- **crt.sh was intermittent.** It failed for `bmodaf.org`, so that date comes from certspotter, which shows current certificates only.
- **UK accounts were read through the opencharities.uk mirror**, because the Charity Commission site returned 403. Figures match the register's financial-history values reported in search.
- **No exposed secrets were encountered.** The front-end bundles contained no credentials of note.

## 7. Source register

| ID | Source | Used for |
|---|---|---|
| S1 | [nptgivingpoint.org main bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js) and lazy chunks; [response headers](https://www.nptgivingpoint.org/) | Client-code list; CSP vendors |
| S2 | Site bundles: [jpmgiving](https://jpmgiving.org/main-JBUINBFD.js), [jpmgiftfund](https://jpmgiftfund.org/main-W7WT45DD.js), [icgfdaf](https://icgfdaf.org/main-2IGH5MJZ.js), [donoradvisedfundgiving](https://donoradvisedfundgiving.org/main-5PZW2EPZ.js), [bmodaf](https://bmodaf.org/main-CME7MTNM.js), [glenmededaf](https://glenmededaf.com/main-2GMDDIKR.js), [tollesondaf](https://tollesondaf.org/main-N3M4QVUS.js), [pitcairndaf](https://pitcairndaf.org/main-TXNWGRMW.js), [nptukgiving](https://nptukgiving.org/main-4ALO56BR.js), [npttransatlanticdaf](https://npttransatlanticdaf.org/main-L5UEGKW2.js), [rathbonesdaf](https://rathbonesdaf.org/main-GUDOXMXE.js), [cazenovecapitaldaf](https://cazenovecapitaldaf.org/main-LSW43PUG.js) | Program name, sponsor text, Ren Jira link |
| S3 | [dns.google](https://dns.google/) A/CNAME/TXT/MX for every host in the CSV, e.g. [www.jpmgiftfund.org](https://dns.google/resolve?name=www.jpmgiftfund.org&type=A), [nptrust.org TXT](https://dns.google/resolve?name=nptrust.org&type=TXT), [fidelitycharitable.org TXT](https://dns.google/resolve?name=fidelitycharitable.org&type=TXT) | Hosting, email and marketing vendors |
| S4 | [crt.sh](https://crt.sh/) (`?q=<domain>&output=json`); [certspotter](https://api.certspotter.com/v1/issuances?domain=fidelitycharitable.org&include_subdomains=true&expand=dns_names) | First-cert dates; Fidelity host set |
| S5 | iPhi tenant redirects: `jpms.iphiview.com/jpms`, `pitcairn.iphiview.com/pitcairn`, `npt.iphiview.com/glenmede`, `npt.iphiview.com/nptukusd` | Program lineage |
| S6 | [nptrust.org](https://www.nptrust.org/); [nptuk.org](https://www.nptuk.org/); [NPT annual report FY25](https://www.nptrust.org/annual-reports/npt-annual-report/); [For Financial Institutions](https://www.nptrust.org/advisors-and-institutions/for-financial-institutions/); [staff page](https://www.nptrust.org/?p=9259) | Log-in links, totals, private-label statement, product ownership |
| S7 | NPT 990 FY6/2025 ([ProPublica](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/full); [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml)); FY6/2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml)) | VII-B, Part IX, Part VIII, Schedules D/O/R |
| S8 | NPT UK 2025 accounts ([opencharities](https://opencharities.uk/ew/1181128/files/2025-06-30-accounts.md)); NPT Transatlantic 2025 accounts ([opencharities](https://opencharities.uk/ew/1153376/files/2025-06-30-accounts.md)); [register summary](https://opencharities.uk/ew/1153376) | UK assets; technology-provision clauses |
| S9 | Fidelity Charitable 990 FY6/2025 ([ProPublica](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/full); [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml)) | FMR services agreement, VII-B, IT $0 |
| S10 | [Built In: Fidelity Charitable Director of Marketing Technology Engineering](https://builtin.com/job/director-marketing-technology-engineering/8794296) | SFMC, Segment, AEM |
| S11 | [Rathbones 2025-08-26](https://www.rathbones.com/en-gb/wealth-management/media-centre/news-and-comment/legal-complexity-deterring-wealthy-leaving-money-charity); [J.P. Morgan DAF PDF (2018; label interpretation only)](https://www.jpmorgan.com/content/dam/jpm/securities/documents/DAFExecutiveSummary.pdf); [Justia NPT trademarks](https://trademarks.justia.com/owners/national-philanthropic-trust-4033609) | Partner confirmation |
| S12 | Repo baseline: [queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md), [queue-vendor-scope-ren-denominator.md](queue-vendor-scope-ren-denominator.md), [queue-npt-dafgiving360-misc.md](queue-npt-dafgiving360-misc.md), [validation-wave3-report.md](validation-wave3-report.md), [validation-wave11-report.md](validation-wave11-report.md) | Prior findings |

## 8. Data dictionary: `npt-givingpoint-programs-2026.csv`

| Column | Meaning |
|---|---|
| `program_id` | GP01–GP15 |
| `program_name` | Program name as stated in the site bundle (or `[code only]`) |
| `client_code_in_build` | Client identifier(s) used in the shared GivingPoint JavaScript |
| `givingpoint_url` | Live GivingPoint site root |
| `redirecting_hosts` | iPhi paths and defensive domains that redirect to the site |
| `institution`, `institution_type` | Distributing institution and its category (bank, wealth, RIA, family office, adviser channel, sponsor direct) |
| `legal_sponsor`, `sponsor_id`, `jurisdiction` | Sponsoring charity, its EIN or UK charity number, and country |
| `hosting_observed`, `dns_evidence_url` | `ren-workload-02` ELB or iPhi Global Accelerator pair; dns.google link |
| `bundle_text_evidence`, `bundle_evidence_url` | Verbatim sponsor or program text and the bundle it came from |
| `renpsg_jira_link`, `shared_waf_id` | Whether the bundle links `renpsg.atlassian.net`; AWS WAF challenge id |
| `ct_first_cert`, `ct_source` | Earliest certificate seen and which log was used |
| `live_status_2026_11_15` | HTTP result on 2026-11-15 |
| `program_assets_public`, `assets_value`, `assets_basis`, `assets_source_url` | Whether assets are public at program level (`no`), at entity level (`entity_total`) or only as the sponsor total (`sponsor_total_only`); value (USD unless GBP stated); basis; source |
| `attribution_status` | confirmed / inferred / unresolved |
| `notes`, `retrieved` | Free text; retrieval date |

The edges file uses the standard `relationship-graph-edges.csv` columns. EL001–EL016 are Ren→program (technology_provider) and sponsor→program (sponsor_of) pairs for the 8 newly evidenced sites. EL017–EL018 are Ren→NPT UK and Ren→NPT Transatlantic technology edges. NPT-family control and technology-provision edges follow (EL019–EL023). EL024–EL028 cover the Fidelity Charitable stack, including an `unknown` Ren→Fidelity edge that records absence of evidence.
