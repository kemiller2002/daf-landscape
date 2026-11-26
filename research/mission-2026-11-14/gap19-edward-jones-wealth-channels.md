# Gap-19 pass: Edward Jones and thin wealth channels (P-GAP19-07, P-GAP19-08)

**Date:** 2026-11-19. **Scope:** public filings and public pages only, 2021 onward. No outreach, logins or forms.
**Read first and respected:** `thoroughness-gap-audit-2026-11-19.md` (§2, C09); `queue-batch33-market-structure.md` §4.1 and its wave-18/19 governing corrections (the Edward Jones "$535m" figure may be cumulative, not year-end assets; "$2.9bn" stays unattributed); `queue-bank-programs-and-eft-providers.md` and its wave-6/18 governing corrections.

**Outputs**
- `data/mission-2026-11-14/wealth-channel-daf-programs-2026-11-19.csv`: 11 program rows (data dictionary in §7).
- `data/mission-2026-11-14/relationship-graph-edges-additions-26.csv`: edges EZ001–EZ022, 7 of them explicit negatives or re-checks.
- `data/mission-2026-11-14/queue-proposals-g07.csv`: P-G07-01 to P-G07-03.

**Labels:** [F] = first-party text or filing read this pass. [I] = inference. [N] = explicit negative (searched, not found). [B] = route blocked (robots or transport).

---

## 0. Bottom line

1. **The Edward Jones private DAF still has no public sponsor, administrator, vendor, fee or asset figure.** This is now an explicit negative across every 2021+ public filing route the queue named, not a gap in searching. The sources read were:
   - five 10-Ks and three 2026 10-Qs;
   - four ADV Part 2A wrap brochures, the financial-planning brochure and the Form CRS;
   - the Generations agreement and site;
   - RCF's FY2021–FY2024 audits and its CY2024 990.

   E018/ER016 stand. Do not assume RCF or Ren (EZ001–EZ003) [N].
2. **The standard Edward Jones Charitable Gift Fund is unchanged.** Its terms:
   - RCF "manages and administers" the fund, and the donor portal is Ren DonorFirstX (program code `EJDAF`).
   - Minimum $10,000, and $500,000 for unique assets.
   - Up to two of seven portfolios; $250 minimum grant.
   - No fee schedule is published [F].
3. **SEI runs two DAFs on two different stacks.** The SEI Giving Fund is an RCF program (on Ren). The SEI Charitable Fund (launched 2026-10-28) is sponsored by GiveClear on TIFIN Give. Neither publishes program fees. SEI's FY2025 10-K and Q3 2026 10-Q do not mention TIFIN or DAFs [F/N].
4. **Charityvest does not publish fees for its custom programs** (TIAA, OneGive) ("reach out to your program contact"). OneAscent and TIAA hosts could not be read this pass [F/B].
5. **Pave Finance has no DAF product or partner on any of its 206 public pages** [N].
6. **Bank channel check:**
   - **BofA/Merrill:** first-party trustee and administrator text. BofA N.A. is sole trustee and BofA Private Bank is administrator; Merrill advisors are a distribution channel; minimum $25,000 [F].
   - **Wells Fargo:** live pages no longer name a sponsor, so E093 (NPT) remains search-excerpt only [N].
   - **U.S. Bank:** names no sponsor ($5,000 minimum) [N].
   - **PNC:** the guide was unreachable [B]; its 2021 Gifting Portal names no vendor.
7. **New 990 facts on the channels' roles** (they also act as investment managers or custodians to other sponsors):
   - Wells Fargo Advisors LLC was paid **$3.41m by Fidelity Charitable** (FYE 2025-06) for investment management.
   - PNC Bank was an "administrative services" payee of AOGF (FYE 2022–2023) and was replaced by Citibank.
   - U.S. Bank is custodian or manager to DAF-holding foundations.
   - Merrill manages money for the Arizona Community Foundation.

## 1. Method

### 1.1 Routes
- **SEC EDGAR**, with a generic User-Agent:
  - the submissions JSON (data.sec.gov);
  - filing documents under `/Archives/edgar/data/` (allowed by sec.gov robots.txt).
  - `cgi-bin` and EFTS full-text search were not used (cgi-bin is disallowed, and EFTS robots returned 403).
- **IRS e-file XML** via the GivingTuesday S3 mirror (`gt990datalake-rawdata`, robots 404 = no rules). Part VII-B and Schedule D were parsed with a local script.
- **First-party websites**, after reading robots.txt on each host.

### 1.2 Robots log (read before any fetch)

| Host | robots.txt result | Action |
|---|---|---|
| www.sec.gov | 200; `/Archives/edgar/data` allowed | Fetched 10-K/10-Q documents |
| data.sec.gov | 404 (no rules) | Submissions JSON only |
| efts.sec.gov | 403 | Not fetched |
| adviserinfo.sec.gov | 200; disallows `/IAPD/Content/Common/crd_iapd_Brochure.aspx` and `/firm/brochure/` | Not fetched |
| api.adviserinfo.sec.gov, reports.adviserinfo.sec.gov | 403 | Not fetched (so IAPD brochure discovery and Form CRS PDFs were not available) |
| files.adviserinfo.sec.gov | 404 (no rules) | One known OneAscent brochure ID was tried; it returned 404 (the version has been retired) |
| www.edwardjones.com, generations.edwardjones.com | 200; content and `/sites/default/files/dam/` allowed | Fetched |
| edwardjones.donorfirstx.com, sei.donorfirstx.com | 404 (no rules) | Login page only (no login) |
| renaissancecharitable.org | 200; allow all | Fetched |
| www.seic.com | 200 | Fetched |
| guide.charityvest.org | 200; allow all | Fetched |
| www.pavefinance.com | 200 (sitemap only) | Fetched all 206 sitemap pages |
| www.usbank.com | 200 | Fetched wealth-management pages |
| www.wellsfargo.com | 200 | Sitemap only |
| conversations.wf.com | 200 | Fetched; it redirects to wellsfargoadvisors.com |
| www.wellsfargoadvisors.com | 404 (no rules) | Fetched philanthropy pages from its sitemap |
| www.bankofamerica.com | 200; `/philanthropic/` allowed | Fetched guidelines |
| www.ml.com | 200; **disallows `/mlwm/pages/daf.aspx`** | Not fetched |
| www.pnc.com | 200; `/content/dam/` allowed | Content fetches failed (HTTP/2 reset, empty reply) [B] |
| pnc.mediaroom.com | 404 (no rules) | Fetched the 2021 release |
| oneascent.com | 403, then empty reply | Not fetched [B] |
| www.tiaa.org | timed out | Not fetched [B] |
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | Fetched XML |

## 2. Edward Jones (P-GAP19-07)

### 2.1 The Jones Financial Companies, L.L.L.P. (CIK 815917): 10-K and 10-Q
Filings read, with counts of the terms "charit" and "donor":

| Filing | Filed | URL | "charit" / "donor" hits |
|---|---|---|---|
| 10-K FY2025 | 2026-03-13 | [link](https://www.sec.gov/Archives/edgar/data/815917/000119312526105798/ck0000815917-20251231.htm) | 0 / 0 |
| 10-K FY2024 | 2025-03-14 | [link](https://www.sec.gov/Archives/edgar/data/815917/000095017025039256/ck0000815917-20241231.htm) | 0 / 0 |
| 10-K FY2023 | 2024-03-12 | [link](https://www.sec.gov/Archives/edgar/data/815917/000095017024029758/ck0000815917-20231231.htm) | 0 / 0 |
| 10-K FY2022 | 2023-03-10 | [link](https://www.sec.gov/Archives/edgar/data/815917/000095017023007158/ck0000815917-20221231.htm) | 0 / 0 |
| 10-K FY2021 | 2022-03-11 | [link](https://www.sec.gov/Archives/edgar/data/815917/000095017022003436/ck0000815917-20211231.htm) | 0 / 0 |
| 10-Q Q1/Q2/Q3 2026 | 2026-05-07 / 08-07 / 11-05 | [Q1](https://www.sec.gov/Archives/edgar/data/815917/000119312526210969/ck0000815917-20260327.htm), [Q2](https://www.sec.gov/Archives/edgar/data/815917/000119312526339455/ck0000815917-20260626.htm), [Q3](https://www.sec.gov/Archives/edgar/data/815917/000119312526449407/ck0000815917-20260925.htm) | 0 / 0 |

What the filings do say [F]:
- **Revenue notes.** Asset-based fees consist of:
  - advisory programs fees;
  - service fees;
  - "other asset-based fees" (revenue sharing, fund adviser fees, cash solutions and Trust Co. fees).

  Total revenue was $17,897m in 2025.
- **Related parties.** Note 16 covers only branch leases from financial advisors (about 13% of branch space).
- **Strategy.** The FY2025 10-K lists a "High Net Worth" initiative. "Philanthropy" appears only in executive biographies (FY2021–FY2024).
- **Result.** There is no DAF revenue line, no related-party DAF arrangement, and no sponsor or administrator name [N] (EZ001).

### 2.2 ADV Part 2A brochures and Form CRS (from edwardjones.com, because IAPD was blocked)
- **Wrap brochures**, all "as of March 27, 2026":
  - [Investment Advisory Program](https://www.edwardjones.com/sites/default/files/dam/skca0yblka/ias-19127-a-e-pb.pdf) (the HNW-oriented program: $300,000 minimum eligible investments; alternatives for clients with $5m+);
  - [Advisory Solutions Fund Models](https://www.edwardjones.com/sites/default/files/dam/xarlxinb3w/ias-3936aa-a-pb.pdf);
  - [UMA Models](https://www.edwardjones.com/sites/default/files/dam/1inhmtcmnv/ias-6486aa-a-pb.pdf);
  - [Financial Advisor Managed Solutions](https://www.edwardjones.com/sites/default/files/dam/hmy2r9wfdd/ias-17188-a-e-pb.pdf).
- **[Branch Office Financial Planning Services brochure](https://www.edwardjones.com/sites/default/files/dam/du4jieozza/lgl-18036-a-pb-fnl.pdf)**, as of 2026-07-30.
- **[Form CRS / Client Relationship Summary](https://www.edwardjones.com/sites/default/files/dam/nehph0dcbf/lgl-12004-a-e-cc.pdf)**, as of 2026-08-15.
- **[Edward Jones Generations Financial Planning Agreement](https://www.edwardjones.com/sites/default/files/dam/jdywxf79iw/lgl-19371-a-sa-fnl.pdf).**
- **Result** [N] (EZ002):
  - No document names a DAF, a sponsor or an administrator.
  - The only charitable text: trade-error gains "we will donate the amount of such gain to charities chosen by Edward Jones", and "charitable organizations" listed as eligible account types.
  - The Form CRS and Generations agreement have no charitable content.

### 2.3 Edward Jones pages
- **[DAF product page](https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds)** (live 2026-11-19), repeated [F]:
  - "offered by Edward Jones in conjunction with Renaissance Charitable Foundation Inc., which manages and administers the Fund";
  - "One of seven professionally managed portfolios";
  - minimum grant $250;
  - "third-party administrators responsible for the day-to-day operations".
- **[Brochure ANG-13116H-A-E-SR](https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/ang-13116-a.pdf)** (© 2026, expires 2027-03-31) [F]:
  - $10,000 minimum for cash and marketable securities; $500,000 for unique assets;
  - "invest in up to two of these portfolios";
  - "it still has fees". No schedule is given.
- **Donor portal.** The [donor portal](https://edwardjones.donorfirstx.com/) login page carries the branding "Edward Jones Charitable Gift Fund", Intercom `program_code: "EJDAF"`, `program_id: "1630"` and a footer link to reninc.com [F] (EZ007). The portal reveals no other Edward Jones program; no enumeration was attempted.
- **Generations timeline** [F] (EZ004–EZ006):
  - [2025-03-12](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/enhancing-serve-high-net-worth-clients): Generations announced; $10m minimum investable assets; EY and Husch Blackwell for tax and estate work.
  - [2025-04-29](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/high-net-worth-offerings): CAIS alternatives platform; planning "may include ... philanthropic planning".
  - [2025-09-16](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management): "A private Donor Advised Fund (DAF) designed for significant philanthropic contributions, giving donors greater flexibility and customization in pricing and investment options". No sponsor is named.
  - [generations.edwardjones.com](https://generations.edwardjones.com/us-en/hnw/generations-v2) has no DAF content.

### 2.4 RCF filings
- **What is posted.** The [Legal, Compliance & Policies page](https://renaissancecharitable.org/legal-resources/) lists:
  - 990s for 2020–2024;
  - audits through "2023-2024".
  - FY2025 is not posted as of 2026-11-19.
- **[FY2024 audit](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)** [F]:
  - RCF "offers a private-labeled donor-advised fund program to financial services firms and nonprofits", with outsourced administration by Renaissance Acquisition Company LLC ("Ren").
  - Note 9: the fee paid to Ren is 98% of fundholder admin-fee revenue, $19,225,546 in 2024 and $15,543,682 in 2023.
  - No program is named.
- **Earlier audits.** The FY2021, FY2022 and FY2023 audits: 0 hits for "Edward" or "Jones" [N].
- **[CY2024 990](https://renaissancecharitable.org/wp-content/uploads/2026/01/Form-990-Public-Disclosure-Copy-2024-RCF.pdf)** and [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml):
  - Part VII-B: Renaissance Administration LLC, $19,225,546.
  - Schedule O: "outsources management and administrative services to Renaissance Administration LLC (Ren)".
  - "Edward Jones" appears only as a grantee ("Edward Jones Disaster Relief Fund").
  - Result: no program size, fee share or sponsor tie for either Edward Jones program [N] (EZ003).

### 2.5 Edward Jones checklist cells after this pass

| Cell | Status |
|---|---|
| financials | Charitable Gift Fund: "nearly $535m" (company-reported; may be cumulative, per wave 18). Private DAF: none disclosed [N] |
| custody/investments | Standard fund: seven portfolios, manager unnamed. Private DAF: "customization in pricing and investment options" only |
| grant workflow | $250 minimum; IRS-status check by the third-party administrator (EJ text); Ren portal |
| assurance | RCF audited (FY2024 posted); no program-level assurance |
| ownership/funding | Edward Jones is a partnership (JFC); no DAF-related party |
| timeline | Generations: 2025-03-12 announced → May 2025 launch → 2025-09-16 private DAF announced |
| ai | Nothing found |

## 3. Thin wealth-channel profiles (P-GAP19-08, part 1)

### 3.1 SEI
- **SEI Charitable Fund** ([release, 2026-10-28](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)) [F]:
  - "powered by TIFIN Give, a TIFIN company, and sponsored by GiveClear Foundation".
  - It follows an earlier-2026 partnership in which "TIFIN Give provides a white-labeled donor-advised fund solution to SEI's bank and affiliated wealth clients".
  - No fee, minimum or custody terms are given.
  - Sponsor-level size: [GiveClear CY2024 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533199349302978_public.xml) shows 228 DAFs, $215,283,755 at year end, $210.0m contributions, $31.8m DAF grants, and Tifin Give LLC paid $185,921. This is before the launch and covers all programs.
- **SEI Giving Fund** ([SEI adviser article, 2025-09-08](https://www.seic.com/financial-advisors/our-insights/tax-smart-planning-if-using-donor-advised-fund)) [F]:
  - "SEI offers a DAF called the SEI Giving Fund. The SEI Giving fund is administered by Renaissance Charitable Foundation".
  - $5,000 minimum; mutual fund strategies.
  - This upgrades E045 and E047 from a search excerpt to first-party text (EZ008).
- **SEI filings** [N]:
  - The [10-K FY2025](https://www.sec.gov/Archives/edgar/data/350894/000035089426000013/seic-20251231.htm) and [10-Q Q3 2026](https://www.sec.gov/Archives/edgar/data/350894/000035089426000058/seic-20260930.htm) do not mention TIFIN, charitable funds or DAFs, so the size of SEI's TIFIN stake is not disclosed.
- **Separately, SEI manages DAF-sponsor money** [F] (EZ009):
  - Delaware Community Foundation paid "SEI INVESTMENT" $939,051 (FYE 2025-06; 230 DAFs, $128.8m) ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601339349306915_public.xml)).
  - The repo harvest also shows SEI at First Community Foundation Partnership, the Miami Foundation, the Southwest Florida CF and the Dakota Medical Foundation.

### 3.2 OneAscent (OneGive) and TIAA (both Charityvest-sponsored, Foundation Source-powered)
- **Charityvest's [fees page](https://guide.charityvest.org/for-donors/fees-and-expenses)** [F]:
  - "If you are part of a custom DAF program, reach out to your program contact for fee details specific to your account".
  - The published retail schedule (invested accounts: 0.60% on the first $500k, then 0.30%, 0.20%, 0.15% and 0.10%; $100 minimum) **does not apply by default to OneGive or TIAA**. This is consistent with the repo's caution against adding 60 bps to OneGive's 55 bps.
- **Charityvest's [Foundation Source page](https://guide.charityvest.org/about-our-venture/charityvest-+-vennfi)** [F]:
  - Foundation Source provides "comprehensive software and administrative services to its DAF platform for a fee".
  - It has "no claim ... to Charityvest's DAF assets", and the board monitors whether fees "exceed fair market value".
- **Assurance.** The [financial reporting page](https://guide.charityvest.org/governance-and-legal/financial-reporting) lists Smith & Howard, P.C. audits for FY2019–FY2024 and 990s for 2019–2024 [F]. All of these predate the TIAA (2026-09) and OneGive (2026) programs, so they cannot show program-level figures.
- **Not refreshed** [B]. oneascent.com (robots 403, then empty reply) and tiaa.org (robots timed out) were not fetched. The repo facts stay as they were:
  - E128–E131 (TIAA: Charityvest sponsor, Foundation Source, TC Services adviser, seven model portfolios);
  - E134–E136 (OneGive: 55 bps adviser fee; OneAscent Impact Fund indirectly owns part of Foundation Source).

### 3.3 Pave Finance
- **No DAF product or partner** [N] (EZ010). All 206 sitemap URLs were fetched: home, capabilities, legal, the Series A post and newsletters. They contain 0 occurrences of charit, donor, DAF or philanthrop.
- **Entities** ([legal](https://www.pavefinance.com/legal); [Series A](https://www.pavefinance.com/newsletter/series-a)) [F]:
  - Pave Labs LLC (software);
  - Pave Securities LLC (introducing broker-dealer, FINRA/SIPC);
  - Pave Investment Advisors LLC (SEC RIA).
- **Revenue streams:** SaaS licences, broker-dealer revenue and advisory fees.
- **Form ADV:** not read (IAPD API blocked).

## 4. Bank and wirehouse channel check (P-GAP19-08, part 2)

### 4.1 Wells Fargo
- **No sponsor named on live pages** [N] (EZ012):
  - Live Wells Fargo Advisors pages ([DAF article](https://www.wellsfargoadvisors.com/private-wealth/conversations/philanthropy/donor-advised-funds.htm), [philanthropic services](https://www.wellsfargoadvisors.com/private-wealth/solutions/philanthropic-services.htm), [charitable giving](https://www.wellsfargoadvisors.com/planning/goals/charitable-giving.htm)) describe DAFs and say only "The sponsoring organizations maintaining the fund have ultimate control".
  - The repo source for E093/E094 (`conversations.wf.com/donor-advised-funds`) now redirects to the Private Wealth conversations hub.
  - E093 (NPT is the sponsor) and E094 (WF manages the investments) therefore remain search-excerpt evidence that was not re-confirmed this pass.
- **New fact** [F] (EZ011): the [Fidelity Charitable 990, FYE 2025-06-30](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml), Part VII-B, lists:
  - WELLS FARGO ADVISORS LLC, "INVEST. MANAGEMENT", $3,409,679;
  - UBS Financial Services, $11,756,056;
  - ICONIQ, $10,584,656.

  Wells Fargo Advisors is not among Fidelity's listed contractors for FYE 2022–2024 (repo harvest). [I] This is most likely Fidelity's adviser-managed account programme. The return does not say so. P-G07-02 (g0702-b4531) finds that Fidelity's audited investment management fees equal line 11f to the dollar in FY2022–25 and that CIAP held 46.9% of investments at June 2025. That is consistent with this reading but does not name the payee programme [V wave 35B].
- **Investment manager to a community foundation** [F] (EZ013): the Winston-Salem Foundation paid Wells Fargo Private Bank $400,765 in CY2024 (822 DAFs, $261.5m) ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349302739_public.xml)).

### 4.2 Merrill / Bank of America
- **[BofA CGF Program Guidelines, Version 3.2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf)** (PDF modified 2024-09-18) [F] (EZ014–EZ016):
  - "Bank of America, N.A. is the named, sole Trustee";
  - "currently administered by Bank of America Private Bank";
  - Merrill and Private Bank advisor clients submit signed original applications; other donors apply online;
  - minimum initial contribution $25,000; subsequent contributions $250; minimum grant $250;
  - fees: a general administrative fee, plus an investment management fee "based upon a fixed annual rate for all accounts", plus underlying fund expenses. The schedule is available only via the portal, an advisor or 888-703-3436.
- **Newer guidelines.** Versions for 2025 and 2026 return 404.
- **Merrill's DAF page.** ml.com `/mlwm/pages/daf.aspx` is disallowed by robots and was not fetched.
- **Ren portal.** Ren's portal role is repo evidence (E082, EA023).
- **Merrill as investment manager** [F] (EZ017): the Arizona Community Foundation paid "BANK OF AMERICA (MERRILL LYNCH)" $967,803 for investment management and broker fees (FYE 2025-03; 665 DAFs, $455.1m) ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610449349301691_public.xml)).

### 4.3 PNC
- **Guide unreachable** [B]. The Fund for Charitable Giving guide (pnc.com `/content/dam/...`, allowed by robots) could not be fetched (HTTP/2 stream reset, empty reply). This repeats P-B38A-01.
- **[PNC Gifting Portal release (2021-03-08)](https://pnc.mediaroom.com/2021-03-08-PNC-Institutional-Asset-Management-Launches-PNC-Gifting-Portal)** [F] (EZ019):
  - a white-label DAF portal for nonprofit sponsors;
  - bundled with investment management, custody, "subaccounting, recordkeeping and real-time transaction processing";
  - "best suited for charitable organizations with over $1 million in DAF assets".
  - No technology vendor is named. EV007's iPhi link (a 2018 capture) stays inferred.
- **New 990 fact** [F] (EZ018): American Online Giving Foundation paid PNC BANK (Kalamazoo) "ADMINISTRATIVE SVCS":
  - $196,447 in FYE 2022-03 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202340469349301209_public.xml));
  - $148,680 in FYE 2023-03 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202410469349300741_public.xml)).

  PNC is absent from FYE 2024-03 and 2025-03, where Citibank appears (repo harvest). The scope of the service is not stated. Benevity remains AOGF's main administrator.

### 4.4 U.S. Bank
- **No sponsor named** [N] (EZ022). The DAF is offered with "Initial deposit as little as $5,000" ([strategies page](https://www.usbank.com/wealth-management/charitable-giving-strategies.html)). The [DAF article](https://www.usbank.com/wealth-management/financial-perspectives/financial-planning/philanthropy-and-charitable-giving/donor-advised-funds.html) and the PWM and endowment pages name no sponsor, administrator or vendor.
- **Charitable Services Group.** It has served public charities and nonprofits "since 1991" ([endowments page](https://www.usbank.com/wealth-management/endowments-planned-giving.html)) [F].
- **990 roles** [F]:
  - custodian to the Catholic Community Foundation of Minnesota: $185,314, FYE 2025-06; 413 DAFs, $132.8m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503519349301415_public.xml)) (EZ020);
  - investment manager to the Troy Foundation: $295,329, CY2024; 139 DAFs, $30.1m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543219349302659_public.xml)) (EZ021).

## 5. Explicit negatives recorded

| # | Route | Result | Edge |
|---|---|---|---|
| N1 | JFC 10-K FY2021–FY2025; 10-Q Q1–Q3 2026 | No DAF, charitable or sponsor text | EZ001 |
| N2 | EJ ADV 2A (4 wrap brochures and the financial-planning brochure), Form CRS, Generations agreement and site | No DAF named | EZ002 |
| N3 | RCF audits FY2021–FY2024; CY2024 990 | No Edward Jones program line; FY2025 not posted | EZ003 |
| N4 | SEI 10-K FY2025; 10-Q Q3 2026 | No TIFIN or DAF disclosure | (text only) |
| N5 | pavefinance.com (206 pages) | No DAF content | EZ010 |
| N6 | Wells Fargo Advisors live DAF pages | No sponsor named; E093 not re-confirmed | EZ012 |
| N7 | U.S. Bank DAF pages | No sponsor named | EZ022 |
| N8 | Charityvest guide | Custom-program fees not published | (CSV WC05/WC06) |

## 6. Source register

| ID | Source | Date | Used in |
|---|---|---|---|
| G07-S01 | [JFC 10-K FY2025](https://www.sec.gov/Archives/edgar/data/815917/000119312526105798/ck0000815917-20251231.htm) | 2026-03-13 | §2.1, EZ001 |
| G07-S02 | JFC 10-Ks FY2021–FY2024 and 10-Qs 2026 (URLs in §2.1) | 2022–2026 | §2.1 |
| G07-S03 | [EJ Investment Advisory Program brochure](https://www.edwardjones.com/sites/default/files/dam/skca0yblka/ias-19127-a-e-pb.pdf) and the three other wrap brochures (§2.2) | 2026-03-27 | §2.2, EZ002 |
| G07-S04 | [EJ Form CRS](https://www.edwardjones.com/sites/default/files/dam/nehph0dcbf/lgl-12004-a-e-cc.pdf) | 2026-08-15 | §2.2 |
| G07-S05 | [EJ Branch Office Financial Planning brochure](https://www.edwardjones.com/sites/default/files/dam/du4jieozza/lgl-18036-a-pb-fnl.pdf) | 2026-07-30 | §2.2 |
| G07-S06 | [EJ Generations FP Agreement](https://www.edwardjones.com/sites/default/files/dam/jdywxf79iw/lgl-19371-a-sa-fnl.pdf) | 2025–2026 | §2.2 |
| G07-S07 | [EJ DAF product page](https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds) | live 2026-11-19 | §2.3 |
| G07-S08 | [EJ Charitable Gift Fund brochure](https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/ang-13116-a.pdf) | © 2026, exp 2027-03-31 | §2.3 |
| G07-S09 | [EJ DFX portal](https://edwardjones.donorfirstx.com/) | live 2026-11-19 | EZ007 |
| G07-S10 | EJ releases [2025-03-12](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/enhancing-serve-high-net-worth-clients), [2025-04-29](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/high-net-worth-offerings), [2025-09-16](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management) | 2025 | §2.3, EZ004–EZ006 |
| G07-S11 | [RCF legal resources](https://renaissancecharitable.org/legal-resources/); [FY2024 audit](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); FY2021–FY2023 audits (same folder) | FY2021–FY2024 | §2.4, EZ003 |
| G07-S12 | [RCF CY2024 990 PDF](https://renaissancecharitable.org/wp-content/uploads/2026/01/Form-990-Public-Disclosure-Copy-2024-RCF.pdf); [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml) | CY2024 | §2.4 |
| G07-S13 | [SEI Charitable Fund release](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience) | 2026-10-28 | §3.1 |
| G07-S14 | [SEI Giving Fund article](https://www.seic.com/financial-advisors/our-insights/tax-smart-planning-if-using-donor-advised-fund) | 2025-09-08 | §3.1, EZ008 |
| G07-S15 | [SEI 10-K FY2025](https://www.sec.gov/Archives/edgar/data/350894/000035089426000013/seic-20251231.htm); [10-Q Q3 2026](https://www.sec.gov/Archives/edgar/data/350894/000035089426000058/seic-20260930.htm) | 2026 | §3.1 |
| G07-S16 | [GiveClear CY2024 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533199349302978_public.xml) | CY2024 | §3.1 |
| G07-S17 | [Delaware CF 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601339349306915_public.xml) | FYE 2025-06 | EZ009 |
| G07-S18 | Charityvest guide: [fees](https://guide.charityvest.org/for-donors/fees-and-expenses), [Foundation Source](https://guide.charityvest.org/about-our-venture/charityvest-+-vennfi), [financial reporting](https://guide.charityvest.org/governance-and-legal/financial-reporting) | live 2026-11-19 | §3.2 |
| G07-S19 | Pave [legal](https://www.pavefinance.com/legal), [Series A](https://www.pavefinance.com/newsletter/series-a), full sitemap | live 2026-11-19 | §3.3, EZ010 |
| G07-S20 | Wells Fargo Advisors [DAF article](https://www.wellsfargoadvisors.com/private-wealth/conversations/philanthropy/donor-advised-funds.htm), [philanthropic services](https://www.wellsfargoadvisors.com/private-wealth/solutions/philanthropic-services.htm) | live 2026-11-19 | §4.1, EZ012 |
| G07-S21 | [Fidelity Charitable 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) | FYE 2025-06 | EZ011 |
| G07-S22 | [Winston-Salem Foundation 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349302739_public.xml) | CY2024 | EZ013 |
| G07-S23 | [BofA CGF Program Guidelines v3.2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf) | 2024-09 | §4.2, EZ014–EZ016 |
| G07-S24 | [Arizona CF 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610449349301691_public.xml) | FYE 2025-03 | EZ017 |
| G07-S25 | [PNC Gifting Portal release](https://pnc.mediaroom.com/2021-03-08-PNC-Institutional-Asset-Management-Launches-PNC-Gifting-Portal) | 2021-03-08 | EZ019 |
| G07-S26 | AOGF 990 XML [FYE 2022-03](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202340469349301209_public.xml), [FYE 2023-03](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202410469349300741_public.xml) | 2022–2023 | EZ018 |
| G07-S27 | U.S. Bank [strategies](https://www.usbank.com/wealth-management/charitable-giving-strategies.html), [DAF article](https://www.usbank.com/wealth-management/financial-perspectives/financial-planning/philanthropy-and-charitable-giving/donor-advised-funds.html), [endowments](https://www.usbank.com/wealth-management/endowments-planned-giving.html) | live 2026-11-19 | §4.4, EZ022 |
| G07-S28 | 990 XML: [Catholic CF of MN](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503519349301415_public.xml), [Troy Foundation](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543219349302659_public.xml) | 2024–2025 | EZ020, EZ021 |

Repo sources reused without re-fetching:
- `form990-contractors-harvest-full.csv`: prior-year payee rows;
- `sponsor-fee-schedules.csv`: the TIFIN Give Giving Fund schedule;
- edges E011–E018, E045–E050, E082–E084, E093–E094, E128–E137, EV007, ER014–ER016.

## 7. Data dictionary: `wealth-channel-daf-programs-2026-11-19.csv`

| Column | Meaning |
|---|---|
| program_id | WC01–WC11, local to this file |
| program_name | Program or offering as publicly named (or a description if unnamed) |
| distributor | Wealth firm or bank that offers the program to clients |
| legal_sponsor | 501(c)(3) sponsoring organization or trust, or `unknown` / `not named` |
| administrator | Entity stated to administer, quoted where possible |
| technology_vendor | Donor-platform vendor where evidenced |
| investment_custody | Investment manager, portfolio menu or custody text |
| trustee | Trustee where the program is a trust (BofA); otherwise n/a |
| program_status | live / announced / launch date / no program |
| fees_public | yes / no / partial: whether a program-specific fee schedule is publicly posted |
| fee_detail | Quoted or summarized fee text; repo comparators flagged as not program-specific |
| min_initial_contribution | Stated minimum opening contribution |
| min_grant | Stated minimum grant |
| assets_accounts | Program or sponsor-level size, with scope stated |
| assets_basis | Source type of the size figure (company-reported, IRS 990, n/a) |
| evidence_label | F, F (repo), negative, blocked, or combinations |
| primary_source_urls | Space-semicolon-separated URLs read this pass |
| source_dates | Document or filing dates |
| routes_tried_negative | Routes searched with no result, or blocked |
| notes | Cross-references to edges and caveats |

Edge file: same columns as `relationship-graph-edges.csv`. Status `unknown` is used for explicit negatives (the pattern of E018). Relationship types reuse the existing vocabulary. `controls` is used for the BofA trustee relationship (EZ014), and `historically_confirmed` for PNC→AOGF (EZ018).
