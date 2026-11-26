# Vendor scope and the Ren denominator (Q-N02, Q-B04, Q-N01)

**Date:** 2026-11-14. **Status:** public-source evidence only. This pass used IRS Form 990 Part VII-B, as rendered by ProPublica from IRS e-file XML. It also used live sponsor and vendor web pages, public DNS (dns.google), and certificate-transparency (CT) logs (certspotter). No authenticated portal was accessed, no credentials were used, and no contract was seen.

**Data written:**
- [`data/mission-2026-11-14/form990-top-contractors.csv`](../../data/mission-2026-11-14/form990-top-contractors.csv): 121 rows across 19 sponsors and 31 filings.
- [`data/mission-2026-11-14/relationship-graph-edges-additions.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions.csv): edges EA001–EA032.
- [`data/mission-2026-11-14/queue-proposals-vendor-scope.csv`](../../data/mission-2026-11-14/queue-proposals-vendor-scope.csv): proposals P-VEN-01 to P-VEN-10.

**Governing conventions:** this file applies the red-team corrections in [vendor-dependency-concentration.md](vendor-dependency-concentration.md#red-team-corrections-wave-2b-2026-11-14--governing) and [red-team-wave2b-graph-data-incentives.md](red-team-wave2b-graph-data-incentives.md):
- Shares use DAFRC FY2024 values, where a June fiscal year is labelled by the year in which it ends. The denominator is $327.87bn across 1,512 sponsors.
- "$200bn" is not a DAF-only figure.

**Evidence labels:**
- **confirmed:** a first-party page or filing states the fact.
- **inferred:** convergent indirect evidence such as DNS, CT logs or tenant naming.
- **unknown:** no evidence either way.

---

## 0. Headline findings

1. **NPT and the GS PWM DAF run on Ren infrastructure today.** Earlier repo work held that NPT–Ren was "unknown" and that Goldman's vendor was "unknown". Both are now superseded.
   - **GS PWM DAF.** The log-in page at `gspf.goldman.com` carries the meta author "GS Donor Advised Philanthropy Fund for Wealth Management". Its footer reads "iPhi ::: Copyright © 2001 - 2026 Stellar Technology Solutions, LLC." ([gspf.goldman.com](https://gspf.goldman.com/gspf/)) The host is a CNAME to an AWS load balancer named `ren-workload-02-public-…elb.amazonaws.com` ([dns.google](https://dns.google/resolve?name=gspf.goldman.com&type=CNAME)). **Status: confirmed (software).**
   - **NPT.** NPT's homepage labels a link "NPT GivingPoint Login" / "Donor GivingPoint Login". That link points to `npt.iphiview.com` ([nptrust.org](https://www.nptrust.org/)), which is Stellar/Ren's iPhi domain. That host returns a 301 redirect to `nptgivingpoint.org` ([npt.iphiview.com](https://npt.iphiview.com/npt/LogIn/tabid/444/Default.aspx?returnurl=%2fnpt%2f)). Four further pieces of evidence point to Ren:
     - `www.nptgivingpoint.org` is a CNAME to the same `ren-workload-02` load balancer ([dns.google](https://dns.google/resolve?name=www.nptgivingpoint.org&type=CNAME)).
     - The GivingPoint web bundle links its build and version tickets to `renpsg.atlassian.net`, which is Ren's Jira ([nptgivingpoint.org main bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js)).
     - Ren hosts a status page titled "NPT iPhi Statuspage" at `iphistatus.reninc.com` ([iphistatus.reninc.com](https://iphistatus.reninc.com/)).
     - CT logs show `auth-npt-int.stellartechsol.com` and `auth-npt-stg.stellartechsol.com`, issued in 2026 ([certspotter: stellartechsol.com](https://api.certspotter.com/v1/issuances?domain=stellartechsol.com&include_subdomains=true&expand=dns_names)).

     **Status: confirmed that Ren hosts the technology and builds the front end.** Neither NPT nor Ren has made a first-party statement, and neither the contract nor the ledger scope is public.
2. **MS GIFT pays RenPSG $14.93m.** Form 990 Part VII-B shows RenPSG paid **$14,930,249** in CY2024 and $11,949,715 in CY2023 for "admin & legal" ([MS GIFT 990 CY2024](https://projects.propublica.org/nonprofits/organizations/527082731/202503239349300435/full); [CY2023](https://projects.propublica.org/nonprofits/organizations/527082731/202403209349313980/full)). This is the first payee-specific Ren amount outside RCF.
3. **Part VII-B names Ren entities as paid vendors at several more sponsors:**

   | Sponsor | Ren entity named | Service | Amount | Source |
   |---|---|---|---|---|
   | Stifel Charitable | "Renaissance" | ops system & service | $801k (CY2025); $498k (CY2024) | [990 CY2025](https://projects.propublica.org/nonprofits/organizations/842049692/202642609349301859/full) |
   | Thrivent Charitable | Renaissance Acquisition Company LLC | technology services | $479k (CY2025) | [990 CY2025](https://projects.propublica.org/nonprofits/organizations/411802412/202612669349300236/full) |
   | Cleveland Foundation | Stellar | hosting & software licence | $416k (CY2024) | [990](https://projects.propublica.org/nonprofits/organizations/340714588/202543189349305969/full) |
   | WaterStone (Christian Community Foundation Inc) | Stellar | computer & software | $366k (FY3/2025) | [990](https://projects.propublica.org/nonprofits/organizations/751750059/202610409349301411/full) |
   | ImpactAssets | Stellar | technology services | $232k (CY2024) | [990](https://projects.propublica.org/nonprofits/organizations/262048480/202543169349307999/full) |
   | Goldman Sachs Charitable Gift Fund (the second GS program) | Stellar | information technology | $173k (FY6/2025) | [990](https://projects.propublica.org/nonprofits/organizations/113813663/202611249349302616/full) |

4. **Give Interactive is migrating Ren/iPhi clients.** Give Interactive is the vendor behind Vanguard Charitable's recordkeeping. CT logs for `giveinteractive.com` show tenants for 15 or more organisations ([certspotter: giveinteractive.com](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names)). At least five of those organisations either pay Ren/Stellar today or did until recently:
   - **WaterStone:** its live portal link is already `waterstone.giveinteractive.com` ([waterstone.org](https://waterstone.org/)).
   - **ImpactAssets, Minneapolis Foundation, Thrivent Charitable and Stifel Charitable:** each has Give staging, sandbox and SFTP tenants, while its live log-in is still on iPhi or Ren.

   **Status: inferred** (the evidence is implementation-stage).
5. **Ren's ">60%" claim cannot be reached on public evidence.** Every sponsor with public Ren evidence, including NPT and GS, adds up to **$91.0bn, or 27.8% of DAFRC FY2024 assets** (section 3). Reaching 60% ($196.7bn) would need roughly another $106bn. Only Fidelity Charitable, DAFgiving360 or Vanguard Charitable are big enough to supply it. Vanguard has chosen Give Interactive, and nothing ties Ren to Fidelity or DAFgiving360.

---

## 1. Q-N02: Give Interactive's scope at Vanguard Charitable and its client list

### 1.1 Company facts

| Item | Finding | Status | Source |
|---|---|---|---|
| Legal name / HQ | Give Interactive, LLC; Overland Park, Kansas | confirmed | [Give Legacy Fund release, 2026-08-24](https://www.giveinteractive.com/post/give-interactive-launches-give-legacy-fund-bringing-a-perpetual-giving-platform-to-daf-sponsors) |
| Founding | Market discovery 2018; build started 2019; first enterprise client committed 2020; MVP live 2021 | confirmed (self-reported) | [giveinteractive.com/company](https://www.giveinteractive.com/company) |
| Founder | Lucas Cherry, Founder & CEO (CPA). Previously EVP at The Signatry, overseeing financial and operational strategy | confirmed | [company page](https://www.giveinteractive.com/company) |
| Other executives | Sam Hoefer (CPO, ex-CEO Brushfire Interactive); Neil McQueen (CTO, ex-CTO AirStrip); Jen McMaster (VP Technology); Hannah Erickson (VP Client Delivery) | confirmed | [company page](https://www.giveinteractive.com/company) |
| Advisor | Dan Greenspon, Market Strategy Advisor (Aug 27, 2024) | confirmed | [Newswire, 2024-08-27](https://www.newswire.com/news/dan-greenspon-joins-give-interactive-as-market-advisor-22408596) |
| Ownership / funding | No disclosed outside investors or rounds. Directories list it as privately held, 11–50 staff | unknown | [search, 2026-11-14](https://www.startuphub.ai/startups/give-interactive) |
| Products | DAF and charitable-asset administration, fund accounting, grants, branded donor portals, investment accounting (SMAs, unitized pools). Give Legacy Fund (perpetual family funds, launched Aug 24 2026). Fund of Funds / Advanced Investment Management Platform (multi-layer NAV, Aug 2026). AI grantmaking modules described as "stay tuned" | confirmed | [home](https://www.giveinteractive.com/); [Fund of Funds release](https://www.giveinteractive.com/post/fund-of-funds-platform); [Legacy Fund release](https://www.giveinteractive.com/post/give-interactive-launches-give-legacy-fund-bringing-a-perpetual-giving-platform-to-daf-sponsors); [platform](https://www.giveinteractive.com/platform) |
| Integrations (named) | Sage Intacct, Salesforce, PowerBI, Stripe, Morningstar, GuideStar, Segment, Intercom, Plaid | confirmed | [home](https://www.giveinteractive.com/); [financial institutions](https://www.giveinteractive.com/solutions/financial-institutions) |
| Security | SOC 2 Type II and SOC 3 issued Sept 2025 (BD Emerson readiness) | confirmed (vendor and advisor) | [BD Emerson case study](https://www.bdemerson.com/case-studies/give-interactive) |
| Hosting (observed) | Per-tenant Google Cloud load-balancer IPs; AWS Cognito (us-west-2) authentication with per-client enterprise SSO (Okta / Entra) | confirmed (DNS and public page config) | [dns.google](https://dns.google/resolve?name=vanguardcharitable.giveinteractive.com&type=A) |

**The "$40B+" claim.** Give Interactive's own timeline reads:
- "2023 $2B processed"
- "2024 $8B live or in implementation"
- "2025 $40B+ live or in implementation" ([company page](https://www.giveinteractive.com/company))

BD Emerson repeats "more than $40 billion in live or implementation-stage activity" as of Sept 2025 ([BD Emerson](https://www.bdemerson.com/case-studies/give-interactive)). The August 2024 figure was "over $7 billion in charitable funds" ([Newswire](https://www.newswire.com/news/dan-greenspon-joins-give-interactive-as-market-advisor-22408596)).

**[Inference]** The jump from $8bn to $40bn between 2024 and 2025 matches Vanguard Charitable's selection. Vanguard's net assets were $27.21bn at 6/30/2025 ([Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)). So the claim is mostly Vanguard and counts **implementation-stage assets, not live assets**.

### 1.2 What Give Interactive does for Vanguard Charitable

| Question | Finding | Status | Source |
|---|---|---|---|
| Scope | Vanguard Charitable "partnered with Give Interactive to modernize and scale its donor-advised fund recordkeeping function", following "a comprehensive review … of platforms across the industry". CIO Chris Bennett is quoted | confirmed (vendor release, PR Newswire, 2025-11-04) | [giveinteractive.com/post/vanguard](https://www.giveinteractive.com/post/vanguard); [PR Newswire](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html) |
| Vanguard Charitable's own disclosure | None found in the newsroom. The FY2025 audit has no mention: its subsequent-events note runs only to Oct 16, 2025, before the announcement | confirmed absence | [newsroom](https://www.vanguardcharitable.org/newsroom); [FY2025 statements, Note 9](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf) |
| FY2026 audited statements / 990 | Not located on 2026-11-14. FY2026 ended 6/30/2026, so the 990 is due by May 2027 | unknown | — |
| Go-live date | Not disclosed. CT logs show certificates for the production tenant `vanguardcharitable.giveinteractive.com` from 2026-08-28. Staging, sandbox and SFTP tenants were issued Aug–Nov 2026. The public config on the production tenant names an enterprise identity provider labelled "vanguard-prod-okta" | inferred: production environment built by Aug–Sep 2026; go-live unknown | [certspotter](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names) |
| Portal vs ledger | The donor log-in on vanguardcharitable.org still uses Vanguard Charitable's own Auth0 tenant (`account.vanguardcharitable.org`) and `client.vanguardcharitable.org`. Both are fronted by Akamai, not Give Interactive ([vanguardcharitable.org](https://www.vanguardcharitable.org/); [dns.google](https://dns.google/resolve?name=client.vanguardcharitable.org&type=CNAME)). **[Inference]** The vendor's word is "recordkeeping", the production tenant has a staff SSO, and the donor portal remains on Vanguard's domain. Together these point to Give Interactive becoming the **back-office ledger/recordkeeping system**, with the donor experience either kept under Vanguard Charitable's brand or not yet cut over | inferred | as cited |
| What stays with Vanguard Group | Vanguard Group receives a fee for "certain support services including investment recordkeeping and administrative services": $4,014,052 in FY2025 and $3,916,396 in FY2024. Vanguard Group also provided $1.0m of in-kind services and manages 35 of the 37 pools ([FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)). Part VII-B lists Vanguard Group Inc for "occup. & admin. svs." at $3,620,366 (CY2024) ([990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/full)). Investment management stays with Vanguard. Whether Vanguard Group's *investment* recordkeeping (pool unit accounting) moves to Give Interactive is **unknown** | confirmed (current); unknown (after go-live) | as cited |
| What stays in-house or with other vendors | Before Give, Vanguard Charitable's top technology contractors in CY2024 were:<br>- **UST Global** "tech admin. services": $4,074,805 (Singapore entity) plus $2,117,669 (California entity)<br>- **Slalom** tech services: $3,741,729<br>- **Salesforce** tech services: $791,734<br>Twenty-eight contractors were paid more than $100k ([990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/full)). Vanguard Charitable capitalised $0 of software in FY2025 ([statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)). **[Inference]** Its existing stack is an outsourced custom/Salesforce build run by UST and Slalom. Give Interactive replaces or overlays part of it. Grant payments run on PayPal Grant Payments (E107) | confirmed (spend); inferred (architecture) | as cited |
| Give Interactive payments so far | Give Interactive does not appear in Vanguard Charitable's CY2024 top five, where the fifth is $791,734. This fits a 2025 contract start | confirmed absence (CY2024) | [990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/full) |

### 1.3 Give Interactive client list

Sources:
- **Tenant list:** CT logs for `*.giveinteractive.com`. These cover only currently valid certificates, issued Aug–Nov 2026 ([certspotter](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names)).
- **Assets:** DAFRC FY2024 rows from [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv).

A tenant name is not a signed contract.

| Client (tenant slug) | Segment | Evidence | Status | DAFRC FY2024 DAF assets |
|---|---|---|---|---|
| Vanguard Charitable (`vanguardcharitable`, `vanguard-*`, `vc-innov`) | National | Vendor release plus production tenant | **confirmed** | $21.95bn |
| The Signatry (`thesignatry`, `signatry-*`) | Faith | Live log-in linked from thesignatry.com ([S03](https://thesignatry.giveinteractive.com/log-in)) | **confirmed** | $0.40bn (imputed) |
| WaterStone (`waterstone`, `ws-sftp`) | Faith | waterstone.org links to `waterstone.giveinteractive.com` ([waterstone.org](https://waterstone.org/)) | **confirmed** | $0.54bn (Christian Community Foundation Inc, EIN 75-1750059; name link inferred) |
| Chicago Community Trust (`cct`, `cct-*`) | Community foundation | Production tenant with "cct-prod" SSO label | inferred | $4.65bn |
| ImpactAssets (`impactassets`, `ia-*`, incl. `ia-addepar`) | National / impact | Production plus staging tenants; live log-in still iPhi | inferred (migrating) | $3.63bn |
| Jewish Communal Fund (`jcf-*`, incl. `jcf-grant-cart`) | Faith / single-issue | Staging, sandbox and SFTP only | inferred (implementation) | $2.87bn |
| The Minneapolis Foundation (`minneapolisfoundation-staging`, `tmf-sftp`) | Community foundation | Staging; live log-in still `tmf.iphiview.com` ([minneapolisfoundation.org](https://www.minneapolisfoundation.org/)) | inferred (implementation) | $0.60bn |
| Thrivent Charitable (`thriventcharitable-*`, `thrivent-sftp`) | Faith / affinity | Staging; live log-in `infaith.iphiview.com` ([thriventcharitable.com](https://www.thriventcharitable.com/)) | inferred (implementation) | $0.59bn |
| Stifel Charitable (`stifelcharitable-staging`, `stifel-sftp`) | Financial institution | Staging plus external SFTP | inferred (implementation) | $0.49bn |
| `nhf` (possibly National Heritage Foundation) | Faith? | Production plus staging | unknown identity | — |
| `jttw`; `jmacarthurtrust` / `jmctdaf` | Unknown | Production plus staging | unknown identity | — |

- **Sum of identified tenants:** about $35.7bn (DAFRC FY2024). That is roughly consistent with "$40B+ live or in implementation".
- **Confirmed-live subset:** about $22.9bn. The confirmed-live label is a first-party statement and does not prove go-live. Vanguard dominates this subset.
- **No banks or wirehouses were found** among Give Interactive's tenants, apart from Stifel's charity, although the vendor markets to "financial institutions".

**[Inference] Strategic reading.** Give Interactive's pipeline overlaps heavily with Ren's inherited iPhi book:
- WaterStone, ImpactAssets, Minneapolis and Thrivent are current or recent Stellar/Ren clients.
- Stifel pays "Renaissance".

This is the first public evidence of **Ren attrition to a challenger**.

---

## 2. Q-B04: who provides technology and administration for the Goldman Sachs programs and MS GIFT

| Program | Portal / software | Administration | Other named contractors | Status | Sources |
|---|---|---|---|---|---|
| **GS Donor Advised Philanthropy Fund for Wealth Management** (EIN 31-1774905; $12.64bn TY2024) | **Ren's iPhi.** The log-in footer reads "iPhi ::: Copyright 2001-2026 Stellar Technology Solutions, LLC". The host is a CNAME to the `ren-workload-02` AWS load balancer. The public docs URLs use the same DotNetNuke pattern (`LinkClick.aspx`) as other iPhi sites | **The Ayco Company LP**, "admin. services": $1,026,306 (CY2024), $3,234,367 (CY2023). **Goldman Sachs & Co LLC**, "tech & inv adv fees": $8,078,863 (CY2024) | The Goldman Sachs Trust Company, investment/advisory: $14.60m. Oak Hill Advisors: $2.31m. **Sapient Corporation**, technology services: $824,200 (CY2024), $449,360 (CY2023). Thirteen contractors were paid more than $100k | Software **confirmed**; administration **confirmed** as Goldman-affiliated (Ayco/GS & Co). Ren's fee is **unknown**: Ren is not in the top five, so it was paid less than $824,200 or through GS & Co | [gspf.goldman.com](https://gspf.goldman.com/gspf/); [dns.google](https://dns.google/resolve?name=gspf.goldman.com&type=CNAME); [990 CY2024](https://projects.propublica.org/nonprofits/organizations/311774905/202503109349303645/full); [990 CY2023](https://projects.propublica.org/nonprofits/organizations/311774905/202413109349303336/full) |
| **The Goldman Sachs Charitable Gift Fund / GS Gives** (EIN 11-3813663; $0.52bn FY6/2024) | **Stellar (Ren)**, "information technology": $172,604 (FY6/2025) and $139,000 (FY6/2024). The payee address is 8910 Purdue Rd, Indianapolis, which is Ren's | **Charities Aid Foundation America**, "grant administration": $875,665 (FY2025), $310,950 (FY2024) | PwC audit services | **confirmed** | [990 FY2025](https://projects.propublica.org/nonprofits/organizations/113813663/202611249349302616/full); [990 FY2024](https://projects.propublica.org/nonprofits/organizations/113813663/202511119349301416/full) |
| **Morgan Stanley GIFT** (EIN 52-7082731; $9.43bn DAFRC FY2024) | Ren DFX portal (`msgift.donorfirstx.com`, E078) | **RenPSG**, "admin & legal": **$14,930,249** (CY2024), $11,949,715 (CY2023). The 25% rise outpaces the program's growth | Morgan Stanley, investment advisor: $4.24m. EY, tax & audit: $185k. Malka Media IT: $139k (CY2023). Only 3–5 contractors were paid more than $100k, so Ren is the dominant vendor | **confirmed** (payee-specific) | [990 CY2024](https://projects.propublica.org/nonprofits/organizations/527082731/202503239349300435/full); [990 CY2023](https://projects.propublica.org/nonprofits/organizations/527082731/202403209349313980/full) |

**Implication.** Goldman is a hybrid. A Goldman affiliate administers its PWM DAF (Ayco plus GS & Co), but the software is Ren's iPhi. The GS employee fund uses Stellar IT plus CAF America for grant administration. **Both GS programs belong in Ren's software footprint and not in its administration footprint.** MS GIFT is the cleanest outsourced-administration case outside RCF: RenPSG is paid about 1.6 bp of DAF assets ($14.93m against about $9.4bn) ([990](https://projects.propublica.org/nonprofits/organizations/527082731/202503239349300435/full)). This is an analyst ratio from mixed-period values.

---

## 3. Q-N01: reconstructing Ren's numerator

Ren's claims are:
- "60%+ U.S. DAF assets using Ren technology" ([reninc.com](https://www.reninc.com/))
- "$175 billion in charitable funding … approximately half of all donor-advised fund assets" ([Great Hill release, 2025-10-28](https://www.businesswire.com/news/home/20251028702541/en/Great-Hill-Partners-Announces-Strategic-Growth-Investment-in-Philanthropy-Tech-Platform-Ren))
- "approximately $200 billion of donor-advised funds and other charitable assets" ([AEF/Ren, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))

All values below are DAFRC FY2024 DAF assets from the [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx), via the repo panel. The denominator is $327.87bn.

| Tier | Sponsor | Ren evidence | Status | $bn |
|---|---|---|---|---|
| A: previously evidenced | RCF | Audited admin fee; 990 VII-B shows Renaissance Administration LLC paid $19,225,546 (CY2024) ([990](https://projects.propublica.org/nonprofits/organizations/352129262/202543189349301959/full)) | confirmed | 5.634 |
| | AEF | Ren "fully power" (Apr 2026) | confirmed | 9.480 |
| | MS GIFT | DFX portal; RenPSG $14.93m | confirmed | 9.430 |
| | BofA CGF | DFX portal; dedicated `boa-api.reninc.com` and `api-boa-prod.donorfirstx.com` hosts ([certspotter](https://api.certspotter.com/v1/issuances?domain=reninc.com&include_subdomains=true&expand=dns_names)). Part VII-B is blank ([990](https://projects.propublica.org/nonprofits/organizations/46010342/202503219349318170/full)) | confirmed (technology) | 5.109 |
| | **Tier A subtotal** | | | **29.653 (9.0%)** |
| B: new this pass | **NPT** | GivingPoint on Ren infrastructure (section 0) | confirmed (technology/hosting) | 42.119 |
| | GS PWM DAF | iPhi footer plus Ren load balancer | confirmed (software) | 11.843 |
| | GS Gives | Stellar IT payee | confirmed | 0.517 |
| | **A+B subtotal** | | | **84.132 (25.7%)** |
| C: iPhi / Ren long tail | ImpactAssets | Stellar $232k; iPhi log-in (Give tenant exists) | confirmed (at risk) | 3.628 |
| | Minneapolis Foundation | `tmf.iphiview.com` (Give staging exists) | confirmed (at risk) | 0.602 |
| | Thrivent Charitable | Ren $479k; `infaith.iphiview.com` (Give staging exists) | confirmed (at risk) | 0.594 |
| | WaterStone (CCF Inc) | Stellar $366k FY3/2025; now on Give | historical / moved | 0.537 |
| | Stifel Charitable | "Renaissance" $801k (Give staging exists) | confirmed (at risk) | 0.494 |
| | Cleveland Foundation | Stellar $416k; iPhi log-in | confirmed | 0.489 |
| | Arkansas CF | `arcf.iphiview.com` (meta author) ([arcf.iphiview.com](https://arcf.iphiview.com/arcf/)) | confirmed | 0.350 |
| | Gulf Coast CF (EIN 59-1052433; which "Gulf Coast" is unverified) | `gccf.iphiview.com` ([gccf.iphiview.com](https://gccf.iphiview.com/gccf/)) | confirmed portal / inferred EIN | 0.148 |
| | Stanislaus CF; Marion CF | `scf` / `mcf.iphiview.com` ([scf](https://scf.iphiview.com/scf/); [mcf](https://mcf.iphiview.com/mcf/)) | confirmed | 0.049 |
| | **All tiers** | | | **91.02 (27.8%)** |

Smaller iPhi tenants with no DAFRC match or no confirmed sponsor:
- Community Foundation of Greater Memphis ([cfgm.iphiview.com](https://cfgm.iphiview.com/cfgm/))
- Catholic Foundation of Central Florida ([cfcf.iphiview.com](https://cfcf.iphiview.com/cfcf/))
- Azzad (an RCF program, [rcf.iphiview.com](https://rcf.iphiview.com/azzad/))
- Truist Financial Corporation ([truist.iphiview.com](https://truist.iphiview.com/truist/)); the product is unknown
- PNC (`pnc.iphiview.com` → `/scbf`, on the `ren-workload-02` load balancer)
- UBS (`ubs.iphiview.com` returns a 301 to `donoradvisedfund.ubs.com`; possibly the NPT-sponsored UBS DAF, which would already be inside NPT)

These hosts were found by DNS probes of `*.iphiview.com` on 2026-11-14 ([dns.google](https://dns.google/resolve?name=pnc.iphiview.com&type=CNAME)). The Gulf Coast CF and Southeast Missouri State DFX programs from repo edges E088/E089 add little.

**Is Ren's claim reachable?**
- **"Approximately half / $175bn" (Oct 2025):** not reachable on DAF assets. The evidenced total is $91bn. Even using later values (NPT $55.9bn at 6/2025, GS $12.64bn TY2024), the total is about $105bn, leaving a gap of at least $70bn.
- **"60%+":** that would need about $197bn. The gap of about $106bn could only come from Fidelity Charitable ($66.2bn), DAFgiving360 ($40.9bn) or Vanguard Charitable ($21.9bn, which is now going to Give Interactive). Their 990s name FMR, Schwab, Vanguard Group, UST, Slalom and Salesforce as top contractors. **No Ren entity appears** ([Fidelity 990](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/full); [DAFgiving360 990](https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/full); [Vanguard 990](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/full)). Absence from the top five only caps payments below $1.0–3.4m. It does not exclude a small Ren component.
- **"$200bn charitable assets supported":** this is plausibly reachable only by adding non-DAF assets. Examples are community-foundation endowments on iPhi (for instance Cleveland Foundation total assets far exceed its DAF value), trusts and other charitable assets. That figure is not a DAF share.
- **Verdict: the claim is still disputed, but the evidenced floor has roughly tripled**, from 9.0% to about 26–28%. The red team's arithmetic fit (residual + NPT ≈ 60.6%) is wrong as a mechanism. NPT *is* Ren-hosted, but the non-big-four residual is not mostly Ren: Foundant, NPact, Blackbaud, Salesforce and Give Interactive all hold documented sponsors.
- **Direction of travel:** about $6bn of Tier C (ImpactAssets, Minneapolis, Thrivent, Stifel, WaterStone) shows Give Interactive implementation activity. That puts **about 6.5% of Ren's evidenced numerator at risk.**

### NPT on Ren/iPhi (GivingPoint lineage): primary evidence

| Test | Result | Source |
|---|---|---|
| NPT homepage log-in target | "NPT GivingPoint Login" points to `npt.iphiview.com/npt/LogIn/...` | [nptrust.org](https://www.nptrust.org/) |
| iPhi host behaviour | 301 to `nptgivingpoint.org` (Microsoft IIS/ASP.NET, the same stack as iPhi DNN) | [npt.iphiview.com](https://npt.iphiview.com/npt/LogIn/tabid/444/Default.aspx?returnurl=%2fnpt%2f) |
| GivingPoint hosting | `www.nptgivingpoint.org` CNAMEs to `ren-workload-02-public…elb.amazonaws.com`. `nptgivingpoint.org` and `npt.stellartechsol.com` resolve to the same IPs | [dns.google](https://dns.google/resolve?name=www.nptgivingpoint.org&type=CNAME); [dns.google](https://dns.google/resolve?name=npt.stellartechsol.com&type=A) |
| Build provenance | The GivingPoint bundle renders version links to `renpsg.atlassian.net/browse/<ticket>` for both the SPA and the API | [main bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js) |
| Ren operational artefacts | "NPT iPhi Statuspage" at `iphistatus.reninc.com`; `auth-npt-int` / `auth-npt-stg.stellartechsol.com` certificates (2026) | [iphistatus.reninc.com](https://iphistatus.reninc.com/); [certspotter](https://api.certspotter.com/v1/issuances?domain=stellartechsol.com&include_subdomains=true&expand=dns_names) |
| Payment trail | **None in Part VII-B.** NPT's top five in CY2024 run from $2.86m (ICONIQ) down to $220,927 (Patterson Belknap). Nine contractors were paid more than $100k. Part IX information technology was $5,871,282 ([990 FY2025](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/full)). Either Ren is paid under $221k, or (more likely) software and hosting fees are not reported as "independent contractor" compensation | confirmed absence; explanation unknown |

**Conclusion:**
- **Supported:** the repo's hypothesis H1 from `npt-givingpoint-iphi-architecture…md`, that GivingPoint is a front end over Ren-hosted iPhi.
- **Contradicted:** H4, that NPT runs an independent system. Ren also builds or maintains the GivingPoint front end, as the Jira links show.

E092 is upgraded from `unknown` to `confirmed (technology/hosting)` in EA015. The publication rule still applies in one respect: do not claim that Ren *administers* NPT DAFs or that NPT pays a specific amount.

---

## 4. Form 990 Part VII-B: five highest-paid independent contractors

The full table is [`form990-top-contractors.csv`](../../data/mission-2026-11-14/form990-top-contractors.csv). Compensation is for the calendar year ending with or within the tax year.

| Sponsor (latest filing) | Technology / admin vendor named | Amount | Count >$100k |
|---|---|---|---|
| Fidelity Charitable (FY6/2025) | FMR LLC, admin & investment management | $159.9m | 73 |
| DAFgiving360 (FY6/2025) | Charles Schwab & Co, brokerage & admin | $9.83m | 101 |
| Vanguard Charitable (FY6/2025) | UST Global $6.19m (two entities); Slalom $3.74m; Vanguard Group $3.62m; Salesforce $0.79m | as stated | 28 |
| NPT (FY6/2025) | No technology vendor (ICONIQ, RSM, consultants, law firm) | — | 9 |
| GS PWM DAF (CY2024) | GS & Co "tech & inv adv" $8.08m; Ayco admin $1.03m; Sapient technology $0.82m | as stated | 13 |
| GS Gives (FY6/2025) | Stellar Technology Solutions $0.17m; CAF America grant administration $0.88m | as stated | 3 |
| MS GIFT (CY2024) | RenPSG $14.93m | as stated | 3 |
| RCF (CY2024) | Renaissance Administration LLC $19.23m (its only contractor) | as stated | 1 |
| AEF (CY2024) | Clearwater Analytics $0.83m; NPact software development $0.25m (pre-Ren stack) | as stated | 6 |
| BofA CGF (CY2024, CY2023) | Section B blank | — | — |

Sources: links per row in the CSV. Fidelity: [990](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/full). AEF: [990](https://projects.propublica.org/nonprofits/organizations/341747398/202513219349310376/full).

**Method caveats:**
1. Section B covers *independent contractors*. Software licences, cloud hosting and affiliate cost-sharing are often reported elsewhere, or not at all. Absence is therefore weak evidence, as the NPT and BofA cases show.
2. The rows are ProPublica renderings of IRS e-file XML. ProPublica's direct XML download was blocked by a bot check, but the rendered `full_text` pages were used.
3. The amounts are calendar-year figures and are not period-aligned to Schedule D.

---

## 5. Implications for the strategic synthesis

- **A4 ("Ren powers over half"):** keep the verdict "unsupported (disputed, not disproven)". Replace the about-9.0% floor with: "Publicly evidenced Ren technology covers about 26% (Tiers A+B: RCF, AEF, MS GIFT, BofA, NPT, GS) to about 28% (with iPhi community foundations) of DAFRC FY2024 assets. NPT is now evidenced as Ren-hosted. 60% still requires Fidelity, DAFgiving360 or Vanguard, none of which shows a Ren vendor." Also note that "$200bn" can be reached only with non-DAF assets.
- **G3 (shared spine):** extend it to **Goldman (both programs) and NPT**.
  - Ren now underpins the #2 (NPT), #5 (GS PWM) and #7–#8 (AEF, MS GIFT) sponsors by FY2024 DAF assets.
  - The systemic-SPOF point therefore gets much stronger. An outage of Ren's `ren-workload-02` load balancer or iPhi would hit NPT and GS together.
  - Administration differs by row. Ren administers RCF and MS GIFT. Ayco/GS administers GS PWM. NPT administers itself.
- **G4 (claim unsupported):** soften to "materially overstated but larger than previously evidenced". Add the "next" action: P-VEN-04 (ask Ren for its denominator).
- **G10 (Give Interactive):** reframe from "Vanguard plus Signatry" to the following:
  - "A third white-label stack with about $36bn of identified tenants (Vanguard, CCT, ImpactAssets, JCF, Minneapolis, Thrivent, Stifel, WaterStone, Signatry), several migrating off Ren iPhi."
  - Vanguard's scope is "recordkeeping". The donor portal is still on Vanguard's own domain, and go-live is undisclosed; the production tenant has existed since about Aug 2026.
  - Add to F (monitors): Vanguard Charitable's FY2026 990 Part VII-B (expected 2027) should show Give Interactive as a payee.
- **G2 (two markets plus captive):** Goldman moves from "unknown" to "affiliate-administered with Ren software". Large sponsors buy *software* separately from *administration*, so vendor share must be measured on both axes.

---

## 6. Open questions

These questions are in the queue file: P-VEN-01 to P-VEN-10.
1. When do the Vanguard Charitable go-live and cutover happen, which functions move, and what happens to UST, Slalom and Salesforce?
2. What contract covers Ren–NPT, and why is it absent from Part VII-B?
3. Who are the unidentified Give Interactive tenants (nhf, jttw, jmacarthurtrust), and are cct and jcf what they appear to be?
4. What are the PNC, Truist and UBS iPhi programs?
5. What split of the AssetMark program moved to TIFIN Give?
6. How does Ren define its denominator?

---

## Source register

| ID | Source | Used for |
|---|---|---|
| S1 | [Give Interactive: Vanguard release](https://www.giveinteractive.com/post/vanguard); [PR Newswire](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html) | Vanguard scope |
| S2 | [Give Interactive company page](https://www.giveinteractive.com/company) | Founding, team, $40B timeline |
| S3 | [Give Interactive home](https://www.giveinteractive.com/); [platform](https://www.giveinteractive.com/platform); [financial institutions](https://www.giveinteractive.com/solutions/financial-institutions) | Products, integrations |
| S4 | [Fund of Funds release](https://www.giveinteractive.com/post/fund-of-funds-platform); [Give Legacy Fund release](https://www.giveinteractive.com/post/give-interactive-launches-give-legacy-fund-bringing-a-perpetual-giving-platform-to-daf-sponsors) | 2026 products |
| S5 | [BD Emerson case study](https://www.bdemerson.com/case-studies/give-interactive) | SOC 2, $40B basis |
| S6 | [Newswire, Aug 2024](https://www.newswire.com/news/dan-greenspon-joins-give-interactive-as-market-advisor-22408596) | $7B (2024) |
| S7 | [certspotter: giveinteractive.com](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names) | Tenant list |
| S8 | [certspotter: stellartechsol.com](https://api.certspotter.com/v1/issuances?domain=stellartechsol.com&include_subdomains=true&expand=dns_names); [reninc.com](https://api.certspotter.com/v1/issuances?domain=reninc.com&include_subdomains=true&expand=dns_names) | NPT/BofA Ren hosts |
| S9 | [dns.google](https://dns.google/) resolutions for gspf.goldman.com, www.nptgivingpoint.org, *.iphiview.com, *.vanguardcharitable.org | Hosting attribution |
| S10 | [gspf.goldman.com](https://gspf.goldman.com/gspf/) | GS iPhi footer |
| S11 | [nptrust.org](https://www.nptrust.org/); [npt.iphiview.com](https://npt.iphiview.com/npt/LogIn/tabid/444/Default.aspx?returnurl=%2fnpt%2f); [nptgivingpoint.org bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js); [iphistatus.reninc.com](https://iphistatus.reninc.com/) | NPT on Ren |
| S12 | [vanguardcharitable.org](https://www.vanguardcharitable.org/); [newsroom](https://www.vanguardcharitable.org/newsroom); [FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf) | Vanguard portal and related party |
| S13 | Form 990 Part VII-B filings (ProPublica `/full`), listed in the CSV | Contractors |
| S14 | Sponsor sites: [waterstone.org](https://waterstone.org/); [impactassets.org](https://impactassets.org/); [minneapolisfoundation.org](https://www.minneapolisfoundation.org/); [thriventcharitable.com](https://www.thriventcharitable.com/) | Live log-in targets |
| S15 | iPhi tenant pages: [tmf](https://tmf.iphiview.com/tmf/), [infaith](https://infaith.iphiview.com/infaith/), [arcf](https://arcf.iphiview.com/arcf/), [cfgm](https://cfgm.iphiview.com/cfgm/), [cfcf](https://cfcf.iphiview.com/cfcf/), [gccf](https://gccf.iphiview.com/gccf/), [scf](https://scf.iphiview.com/scf/), [mcf](https://mcf.iphiview.com/mcf/), [truist](https://truist.iphiview.com/truist/), [rcf/azzad](https://rcf.iphiview.com/azzad/) | iPhi client list |
| S16 | [DAFRC FY2024 dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) (repo panel) | Asset sums |
| S17 | [Ren homepage](https://www.reninc.com/); [Great Hill release](https://www.businesswire.com/news/home/20251028702541/en/Great-Hill-Partners-Announces-Strategic-Growth-Investment-in-Philanthropy-Tech-Platform-Ren); [AEF/Ren release](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/) | Ren claims |
