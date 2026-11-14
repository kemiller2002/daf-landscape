# Breadth pass: community foundations, faith sponsors, shared infrastructure, emerging entrants, and the non-standard grant share (Q-B15)

**Date:** 2026-11-14. **Evidence cut-off:** sources retrieved 2026-11-14.
**Companion data:** `data/mission-2026-11-14/breadth-entity-profiles.csv` (41 entity rows; the data dictionary is in section 8).
**Scope note:** This is a breadth pass. It covers segments the repo had covered only thinly. Every factual claim cites a source ID (section 9). Statements marked **[Inference]** are analyst judgment, not source facts. Repo files already cover Ren/RCF, TIFIN, Chariot, Foundation Source/Charityvest, Daffy and the national sponsors in depth, and this file does not repeat that work.
**Method limits (please read):**
- The session's web-search budget ran out partway through. After that, evidence came only from three kinds of source: direct fetches of first-party pages, ProPublica Nonprofit Explorer renders of IRS e-file XML, and public DNS lookups.
- A few targets could not be retrieved: Every.org returned HTTP 429, JCF's report returned 403, the Chicago Community Trust and GKCCF sites served bot challenges, and the DonorsTrust "about" page returned 404. Their rows say so.
- I did no further search to fill those gaps.

---

## 1. Executive findings

1. **Two nationals and a community foundation both run on the Give Interactive / Stellar iPhi layer. The CF market is therefore not sealed off from the national market.**
   - **Give Interactive** (Overland Park, KS) has a press release dated Nov 4, 2025. It says **Vanguard Charitable** "partnered with Give Interactive to modernize and scale its donor-advised fund recordkeeping function" after "a comprehensive review ... of platforms across the industry" [S01].
   - The **Signatry's** donor log-in is served from `thesignatry.giveinteractive.com` [S02, S03].
   - Give Interactive markets white-label DAF software to three groups: financial institutions, community foundations and "special purpose" (faith/mission) DAFs. It claims to power "$40+ billion in charitable assets" [S04]. Its founder is a former EVP of The Signatry [S05].
   - The repo had no record of this vendor before this pass.
2. **Ren-owned Stellar iPhi still serves the Cleveland Foundation and ImpactAssets in production, checked on 2026-11-14.**
   - The Cleveland Foundation's donor portal (`iphiview.com/tcf/...`) states "Powered by Stellar Technology Solutions, LLC" [S06].
   - ImpactAssets' client log-in is `iphi.stellartechsol.com/calvert/...` [S07]. The path keeps the name of ImpactAssets' Calvert Foundation origin.
   - Both hostnames resolve to the same AWS Global Accelerator IPs (13.248.164.2 and 35.71.183.32) [S08].
   - Ren acquired Stellar in January 2023 (repo: `research/npt-givingpoint-iphi-architecture-and-stellar-customer-cohorts-2026-11-11.md`).
   - So a top-10 community foundation and a large impact-investing DAF sponsor depend on the same vendor as Ren's national/white-label book. This is a **confirmed shared-infrastructure link**: a first-party "powered by" statement plus DNS.
3. **NCF and SVCF donor portals run on Salesforce Experience Cloud.**
   - `secure.ncfgiving.com` and `donor.siliconvalleycf.org` both CNAME to `*.live.siteforce.com` [S08], which is Salesforce's Experience Cloud hosting.
   - The NCF page is titled "MyGiving with NCF" [S09].
   - Who built it (in-house or a Salesforce partner) and what fund-accounting ledger sits behind it are **unknown**.
4. **The long-tail community-foundation software market is concentrated, and Foundant is its anchor.**
   - Foundant's CommunitySuite page says it is "trusted by 700+ community foundations" with "$62B" in assets under management and a "99% renewal rate" [S10].
   - The Fia launch release says Foundant has "more than 4,000 clients" across products [S11].
   - Foundant merged with SmartSimple in August 2024 [S12]. GivingData is now part of the "Foundant family" [S13].
   - The "CSuite" in the task brief is CommunitySuite. The Columbus Foundation's fund portal is `columbusfdn.fcsuite.com`, titled "Community Suite", and its markup references Foundant [S14]. I found no evidence of a separate company called CSuite being merged.
   - Blackbaud sold FIMS and DonorCentral NXT to **NPact** in September 2022. NPact said it serves "hundreds of community, faith-based, education and independent foundations" [S15].
   - Blackbaud still sells Financial Edge NXT for foundations [S16].
5. **Q-B15 (the non-standard grant share), bounded from IRS e-file data.**
   - Foreign grants (Form 990 Part IX line 3) are **1.46% of grant dollars** across Fidelity Charitable, DAFgiving360, Vanguard Charitable and NPT combined (FY ended 6/30/2025). The range is 0.12% (Vanguard) to 4.84% (NPT).
   - They are 3.4% across three large community foundations (SVCF, Chicago Community Trust, GKCCF), and 9.4% at Jewish Communal Fund.
   - Grants to a named list of large fiscal sponsors add about **0.5–2.4%** of dollars at the nationals and community foundations, and 5.6% at JCF.
   - Domestic grantees that sponsors coded as non-501(c)(3) (governments, (c)(4)/(c)(6), etc.) are generally **<1%**. The exception is **NCF**: about 20% of its Schedule I dollars go to grantees coded "religious organization" (mostly churches) or 509(a)(3) supporting organizations.
   - **Dollar-weighted, the observable non-standard share is about 2.5–3% at the large national sponsors. Count-weighted it is far smaller.** At NPT, 560 listed foreign recipients against 159,543 grants processed is a floor of about 0.35% by count.
   - Details and caveats are in section 6.
6. **Sponsor-to-sponsor transfers are the largest "non-retail" flow, bigger than foreign grants.**
   - On a name-matched basis, grants to other DAF sponsors and community foundations are **14.0% of Fidelity's**, **18.5% of DAFgiving360's**, **17.4% of NPT's** and **9.6% of Vanguard's** Schedule I dollars.
   - SVCF's 2024 Schedule I includes **$1,591,322,838 to National Philanthropic Trust**, about 50% of SVCF's listed domestic grants [S20].
   - [Inference] These transfers are mostly low-judgment, sponsor-to-sponsor flows. They still matter for portability analytics and for any "grants per sponsor" benchmark, because they double-count charitable dollars.

---

## 2. Community foundations as DAF sponsors

All figures come from the IRS e-file XML as rendered by ProPublica, unless noted. "DAF accounts" and "DAF value" are from Schedule D Part I, column (a). Column (b) ("other funds") is shown where it is material.

| Sponsor (EIN) | Tax period | Total assets EOY | DAF accounts (Sch D) | DAF value EOY | Grants from DAFs | Portal/tech evidence | Source |
|---|---|---|---|---|---|---|---|
| Silicon Valley Community Foundation (20-5205488) | CY2024 | $12,299,698,780 | 1,011 | $9,578,124,315 | $3,064,391,940 | `donor.siliconvalleycf.org` on Salesforce Experience Cloud (DNS) | S20, S08 |
| Chicago Community Trust (36-2167000) | FY 10/2024–9/2025 | $7,126,827,178 | 1,995 | $4,443,682,319 | $1,099,477,073 | Not determined (site blocked automated fetch) | S21, S27 |
| Greater Kansas City Community Foundation (43-1152398) | CY2024 | $3,386,068,279 | 3,052 (col b: 1,052 other funds) | $2,574,010,894 | $297,130,687 | Not determined. Historically built its own DonorEdge tool and licensed it to other CFs (2006) | S22, S28 |
| Columbus Foundation (31-6044264) | CY2024 | $2,783,783,271 | 1,533 (col b: 1,807) | $1,232,316,877 (col b: $1,557,280,757) | $171,929,535 | **Foundant CommunitySuite** fund portal `columbusfdn.fcsuite.com` (confirmed) | S23, S14 |
| Cleveland Foundation (34-0714588) | CY2024 | $3,285,560,340 | 690 | $493,328,839 | $56,011,580 | **Stellar iPhi (Ren-owned)** donor portal (confirmed) | S24, S06 |
| Greater Horizons (20-0849590) | CY2024 | $2,782,672,021 | 3,055 | $2,531,091,105 | $222,370,123 | Not determined | S25 |

Additional sponsor-reported context:
- CCT's FY2025 statements report consolidated assets of $7.2B and grants net of refunds of $1,225,087,518 [S27].
- CCT's financials page breaks out commitments. Advised funds were 78.2% of $1,479,071,181 in commitments, and that figure includes inter-fund grants [S27].
- Cleveland Foundation says it granted more than $195M in 2025 to 2,221 organizations [S29].

[Inference] Cleveland's DAF share of assets (about 15%) is very different from SVCF's (about 78%). "Community foundation" is not one homogeneous DAF segment: SVCF behaves like a national DAF sponsor, while Cleveland is endowment-led.

### 2.1 Community-foundation software vendors

| Vendor | Product(s) | Customer counts (vendor-stated) | Ownership/events | Evidence |
|---|---|---|---|---|
| Foundant Technologies | CommunitySuite (fund accounting + GL + CRM + donor/advisor portal); GLM/SLM; SmartSimple; GivingData; Fia (AI) | "700+ community foundations", "$62B AUM", "99% renewal" (CommunitySuite page); "more than 4,000 clients" overall (Sep 2026) | Merged with SmartSimple (Aug 13, 2024; L Squared-backed); GivingData now in the "Foundant family" | S10–S13 |
| NPact | FIMS, DonorCentral NXT (bought from Blackbaud 2022), Foundation Cloud (formerly GrantsEdge NXT / Spectrum NXT) | "hundreds of community, faith-based, education and independent foundations" (2022) | Acquisition announced Sep 12, 2022; terms undisclosed | S15, S17 |
| Blackbaud | Financial Edge NXT for foundations (fund accounting) | No count found | Sold FIMS/DonorCentral to NPact | S16 |
| Stellar Technology Solutions (iPhi), now Ren | iPhi CoreEnterprise / DonorView / GranteeView | Not public. The repo has historical named clients | Ren acquisition Jan 2023 (repo) | S06–S08; repo |
| Give Interactive | DAF fund management, grants, portals, investment accounting (fund-of-funds, legacy funds) | "$40+ billion in charitable assets" | Founder is ex-Signatry EVP; Vanguard Charitable partnership Nov 2025 | S01–S05 |

**Is the community-foundation DAF software market distinct from the national/white-label market (Ren, Foundation Source, TIFIN)?** Partly.

- **What makes it distinct (fact-based):**
  - CommunitySuite's requirements are endowment-centric: "endowed and non-endowed funds in one system", pooled-earnings allocation, spending policy, fund statements, and a general ledger that can replace QuickBooks [S10].
  - Community foundations also run competitive grant cycles and scholarships (GLM/SLM).
  - National/white-label platforms emphasize advisor-managed accounts, custody feeds and private-label distribution (repo: Foundation Source + BridgeFT, TIFIN/SEI).
  - The buyer is different too: a CF finance team versus a bank or wealth platform. Foundant's "700+ CF" count has no equivalent in Ren/Foundation Source/TIFIN materials.
- **What makes it overlap (fact-based):**
  - Stellar iPhi serves both a top-10 CF (Cleveland) and a national impact DAF (ImpactAssets), and Ren now owns it [S06–S08].
  - Give Interactive serves both a national (Vanguard Charitable) and a faith sponsor (Signatry), and explicitly sells to CFs [S01–S04].
  - NPact's Grant Edge NXT listings name "Community Foundations & Federations, Single-Issue Charities, Commercial Donor Advised Funds, Private Foundations" as targets [S17].
  - Large sponsors in both segments (NCF, SVCF) build on Salesforce [S08].
- **[Inference] Segmentation:** The CF market splits into two tiers:
  - a **long tail of ~800 sponsors** (the repo's 803 FY2024 CF sponsor count from DAF Research Collaborative) that buy integrated fund accounting + GL from Foundant, NPact or Blackbaud;
  - a **top tier** (SVCF, CCT, Cleveland, ...) whose needs and vendors overlap with the nationals.
- **Count check [Inference]:** If all 700+ Foundant CF clients were U.S. DAF-sponsoring community foundations, Foundant would hold about 87% of the 803 CF sponsors. That is implausible, given that iPhi, NPact and Blackbaud have documented CF customers. The 700+ figure probably also counts Canadian CFs, grants-only (GLM) clients, or non-DAF-sponsoring CFs. **Open question.**

---

## 3. Faith and affinity sponsors

| Sponsor (EIN) | Period | DAF accounts | DAF value EOY | Grants from DAFs | Foreign grants (Part IX L3) | Platform evidence | Source |
|---|---|---|---|---|---|---|---|
| National Christian Charitable Foundation (58-1493949) | CY2024 | 31,943 (col b: 3,545) | $5,683,681,676 | $2,433,041,612 | Blank/none reported | "MyGiving with NCF" on Salesforce Experience Cloud (confirmed hosting; builder unknown) | S30, S09, S08 |
| Jewish Communal Fund (23-7174183) | FY 7/2024–6/2025 | 5,061 | $3,405,167,082 | $1,022,215,101 | $96,647,950 (9.44%) | Not determined (403 on site fetch) | S31 |
| The Signatry (Signatry Charitable Corporation; EIN not confirmed in ProPublica, see open questions) | 2024 report | n/a | n/a | "over $746 Million in Grants" (2024) | n/a | **Give Interactive** log-in (confirmed) | S02, S03 |
| DonorsTrust (52-2166327) | CY2024 | 579 | $1,211,799,615 | $283,497,636 | $326,806 | Custom client dashboard on Netlify (`client.mydonorstrust.org` → `dt-client-dashboard.netlify.app`); builder unknown | S32, S08 |

Other first-party NCF facts:
- NCF reports more than $25B in grants since 1982, more than 425 employees, and 30+ local offices supporting 180 communities.
- Its 2025 grants by category include churches ($468M), evangelism and missions ($268M), and humanitarian aid ($160M) [S33].

Other faith-sector observations:
- **NCF Schedule I coding (fact):**
  - 4,001 grantee rows ($401,577,222, or 15.6% of parsed Schedule I dollars) carry the IRC code "RELIGIOUS ORGANIZATION".
  - 123 rows ($118.3M, or 4.6%) are coded 509(a)(3) supporting organizations: Type I $101.3M, Type II $0.7M, Type III-FI $6.6M, unspecified $9.7M.
  - Schedule I line 3 reports 17,879 "other organizations" [S30].
  - [Inference] Churches are 501(c)(3) by statute and need no determination letter, so this is an *eligibility-verification* path, not a legal exception. It is, though, exactly the kind of grantee that IRS Pub 78/BMF lookups miss, which pushes work toward human review. Faith sponsors therefore have a structurally higher "non-standard verification" share than retail nationals.
- **JCF foreign-grant process (fact):** JCF "utilizes various agencies who perform equivalency determination for foreign charities" and "does not monitor the usage of grants made to qualified charities" [S31]. Its largest named fiscal-sponsor recipient was New Venture Fund, at $41,635,200 [S31].
- **Jewish Federations:** JCF's Schedule I shows grants to JFNA ($1,872,360) and several local federations [S31]. No platform evidence was gathered for federation DAF programs in this pass. **Open.**
- **Catholic and other faith foundations, WaterStone, AMCF:** The repo already covers these in `research/affinity-dafs-megachurches-and-special-interest-organizations-2026-11-11.md`. No new platform evidence was found here.
- **"Fidelity of Christian"?** I found no such entity. The faith-aligned investment link in the repo is OneAscent/OneGive (P25). Unverified; dropped.

[Inference] Give Interactive is a faith-sector-origin vendor: founded by an ex-Signatry executive, its first visible client is the Signatry, and it markets "special purpose DAFs ... faith-based". It has now landed a top-5 national sponsor (Vanguard Charitable). That is a vendor-diffusion path from the faith segment into the national segment. No other DAF technology vendor in the repo follows it.

---

## 4. Infrastructure layer

### 4.1 Giving-platform sponsors (pass-through / workplace)

These sponsors are DAF sponsors for Form 990 purposes, but their accounts are mostly transactional pass-through. Schedule D account counts are not comparable to classic DAFs.

| Entity (EIN) | Period | Sch D accounts | Contributions | Grants | Value EOY | Notes | Source |
|---|---|---|---|---|---|---|---|
| PayPal Charitable Giving Fund (45-0931286) | CY2024 | 380,644 | $808,158,994 | $795,681,014 | $97,016,071 | PayPal, Inc. is sole member; no fees to donors/charities | S34, S35 |
| American Online Giving Foundation (Benevity) (81-0739440) | FY 4/2025–3/2026 | 695 (col b: 751,746) | $1,557,848,744 | $1,390,021,897 | $205,671,333 | Foreign grants $85,293,297 (3.67%); 8 ED-recognized foreign recipients listed | S36 |
| Blackbaud Giving Fund (46-0942102) | CY2025 | not reported | $543,799,159 | $536,379,224 | $65,535,719 | | S37 |
| Network for Good (68-0480736) | CY2024 | 1 | $200,183,595 | $199,763,919 | $50,424,312 | Bonterra site could not be fetched (header overflow) | S38 |
| Givinga Foundation (47-4172718) | CY2024 | 1,421,011 | $12,300,836 | $12,417,069 | $1,949,239 | Givinga, Inc. builds "Philantech"; the Foundation operates accounts/sponsorship; ProjectFS fiscal sponsorship | S39, S40, S41 |
| CAF America (43-1634280) | FY 5/2024–4/2025 | 740 (col b: 235) | $989,778,001 | $947,432,791 | $498,249,958 | Specialist cross-border; foreign grants 26.0% of grant dollars; 4,152 ED/recognized foreign recipients | S42 |
| ImpactAssets (26-2048480) | CY2024 | 2,197 | $611,920,426 | $432,478,470 | $2,896,880,396 | Stellar iPhi portal (confirmed); "proprietary Impact Investment Platform" | S43, S07 |

Vendor-stated figures:
- **Benevity:** $16.6B donated, nearly 1,000 companies, "2.5 million nonprofits continuously validated", and "evolving into an AI-native platform" [S44].
- **Givinga Inc.:** its homepage lists payment processing, grantmaking, employee giving and "automated charity vetting", with no platform-wide volume figures [S40].

### 4.2 Nonprofit-side DAF grant capture

- **DAF Direct:**
  - The widget's sponsoring organizations are listed as **Fidelity Charitable, DAFgiving360 and BNY Mellon Charitable**. There are no download or transaction fees, and the contact address is `DAFDirect@fmr.com` [S45].
  - [Inference] `fmr.com` is Fidelity's (FMR LLC) corporate domain, so DAF Direct is very likely Fidelity-operated. The page does not state ownership. Provider status: *inferred*.
- **The Giving Block:**
  - Calls itself "a Shift4 company" and offers an "Accept DAF Grants" product. It lists "1,500+ nonprofits" in its finder and makes no AI claims [S46].
  - The acquisition date was not verified in this pass.
- **GivingIQ (formerly DonateStock):**
  - On April 30, 2026 it added EasyDAF (DAF grant initiation on nonprofit websites), EasyCrypto and EasyQCD. No AI claims [S47].
- **Chariot:** covered in the repo.

### 4.3 Charity verification data providers

| Provider | Offer | Notes | Source |
|---|---|---|---|
| IRS TEOS bulk data | Pub 78, auto-revocation list, 990-N, 990-series XML; "updated monthly" (Pub 78 last updated Sept 10, 2026) | Free; the authoritative base layer every vendor re-packages | S48 |
| Candid APIs | Charity Check (+ bulk 25/request, PDF, CA state check), Essentials, Premier, Grants, RFP, Demographics, News, Nonprofit Eligibility | The portal does not state data lineage (Pub 78/BMF/OFAC) | S49 |
| Charity Navigator API | EIN, name, address, active advisories, Encompass score/star rating; paid monthly tiers; 1,000 searches/day cap | Ratings-oriented, not an eligibility source of record | S50 |
| ProPublica Nonprofit Explorer | 990 summary API + rendered e-file schedules | Used for this report; good for sponsor benchmarking | S19 |

[Inference] Shared infrastructure here means **every sponsor and vendor relies on the same IRS files** (Pub 78/BMF/revocation), often via Candid. So common-mode failures (IRS update lags, church/no-letter organizations, fiscally sponsored projects) recur across sponsors. "CharityCheck101" was not verified and is excluded.

---

## 5. Emerging, AI-oriented and fintech entrants (2024–2026)

Classification key: **Direct** = sponsors DAFs or sells DAF administration. **Adjacent** = serves nonprofits, grantmakers or payments.

AI evidence classes:
- **A** = announced only.
- **D** = demonstrated (a public demo or beta).
- **E** = deployed with evidence (labelled live, with some third-party or customer evidence).
- **U** = unverified marketing.
- **—** = no AI claim found.

| Entity | Class | What | Funding (verified?) | AI claim & class | Source |
|---|---|---|---|---|---|
| Give Interactive | Direct (vendor) | White-label DAF admin; Vanguard Charitable recordkeeping partner; Fund of Funds (Aug 2026) and Give Legacy Fund (Aug 24, 2026) launches with §4943 monitoring automation | Not found | Integrations list includes "AI tools"; Vanguard release calls the software "intelligent". **U** | S01, S04, S18 |
| Endaoment (84-4661797) | Direct (sponsor; crypto/complex assets; partner API) | FY6/2025: 1,213 DAF accounts, $18.9M value, $18.68M grants; public API `/v1/funds/{dafId}` | Not verified here | None. **—** | S51, S52 |
| Daffy Charitable Fund (86-3177440) | Direct | CY2024 Sch D: 8,905 accounts, $334,483,489 value, $39,841,265 grants. The repo has the company-reported $2B (Sep 2026) | See repo | Not assessed here | S53 |
| Givinga | Direct (white-label + own sponsor) | See §4.1 | Not verified | None on homepage. **—** | S40 |
| Groundswell | Direct-ish (corporate/employee DAF) | DAF product; Candid GuideStar integration; claims SOC 2 Type II, "distributed within 24 hours", "1.8M+ vetted nonprofits". Sponsor entity **not named** | Not stated | None. **—** | S54 |
| GivingIQ | Adjacent (nonprofit intake) | EasyDAF/EasyCrypto/EasyQCD | Not stated | None. **—** | S47 |
| The Giving Block (Shift4) | Adjacent (crypto + DAF grant acceptance) | See §4.2 | Owned by Shift4 | None. **—** | S46 |
| Givefront | Adjacent (nonprofit cards/spend) | Nonprofit card, bill pay; card issued by First Internet Bank of Indiana via Clav/CapitalOS; **no DAF** | $2M (TechCrunch, Dec 18, 2025; repo source) | "AI ... categorize and match expenses", "AI-powered fraud detection". **U** | S55, S56 |
| Foundant Fia | Adjacent (funder AI; CF-installed base) | Knowledge base over grants/CRM/finance; reports; agents; policy engine; bias screening | Part of L Squared-backed Foundant | **D**: beta with early adopters, demoed Aug 2026 | S11 |
| Benevity | Adjacent (workplace; sponsor via AOGF) | Match Assurance, AI Grant Summaries labelled "Live" | Not assessed | **E-** (labelled live by vendor; no third-party evidence). Treat as **U/E-boundary** | S44 |
| Instrumentl | Adjacent (grant seekers) | 5,500+ nonprofits; AI matching/drafting | Not stated | **U** (vendor claims) | S57 |
| Grantable | Adjacent (grant writing) | "30,000+" organizations; "AI drafts, humans decide"; $0–$150/mo + $300 agency add-on | Not stated | **U** | S58 |
| Candid (AI) | Adjacent (data) | The API portal shows no AI products | n/a | **—** on the fetched page | S49 |

**Not covered (search budget exhausted):**
- "Agentic philanthropy" startups.
- Charitable "Philanthropy OS" startups.
- Funding rounds for Endaoment, Instrumentl and Grantable.
- Daffy feature changes after the repo's Sep 2026 note.

These are **open**. I did not invent any funding figures.

[Inference] Across this set, AI claims cluster in **grant-seeker and grantmaker workflow** (Instrumentl, Grantable, Fia, Benevity grant summaries). They are absent from DAF-sponsor core operations: none of Endaoment, Givinga, Groundswell, GivingIQ or The Giving Block makes an AI claim on its fetched pages. The one DAF-core vendor with momentum (Give Interactive) emphasizes investment and compliance automation (§4943, spending policy) rather than AI. That fits the repo's thesis that AI's DAF value sits in exception handling, not the standard path.

---

## 6. Q-B15: what fraction of DAF grants are non-standard and need human judgment?

### 6.1 Definitions and data

- **Foreign** = Form 990 Part IX line 3 ("grants and other assistance to foreign organizations, foreign governments, and foreign individuals"). Share = L3 / (L1 + L2 + L3).
- **Named fiscal sponsor** = Schedule I domestic grants to recipients whose names match a fixed list of large fiscal sponsors or sponsored-project hosts:
  - New Venture Fund, Tides Foundation/Center, Hopewell Fund, Windward Fund, Rockefeller Philanthropy Advisors, Fractured Atlas, Community Partners, Social Good Fund, Players Philanthropy Fund, Trust for Conservation Innovation, Earth Island Institute, Third Sector New England, SEE, North Star Fund, Public Health Institute, Multiplying Good, FJC, Open Collective, Propel Nonprofits.
  - This is a **lower bound**: it misses smaller fiscal sponsors and project-level designations.
- **Non-501(c)(3) code** = Schedule I rows whose IRC-section column is not 501(c)(3). This includes governments, (c)(4), (c)(6), (c)(13), "religious organization" and 509(a)(3) labels.
- **DAF/CF-named** = recipient names containing DAF-sponsor or "community foundation/trust" strings. These are not non-standard for judgment purposes, but they are reported because they distort grant totals.
- **Parser:** I wrote a custom regex parser over ProPublica's rendered Schedule I. Shares are shown only where parsed dollars are within ±10% of Part IX line 1, which covered 89–100% of line 1 for those rows.
- **Excluded for low parse coverage:** Cleveland, Columbus, PayPal Giving Fund, AOGF, CAF America, Blackbaud Giving Fund, Daffy, Givinga.
- **Schedule I limits:** it lists only recipients receiving more than $5,000, aggregated per recipient. Small grants are therefore invisible in the composition columns, but they are included in Part IX totals.

### 6.2 Results (FY ending 2024–2025; source per row = S19/S20–S25, S30–S32, S34–S43)

| Sponsor | Tax period | Part IX L1 (domestic orgs) | L3 foreign | Foreign % of grants | Named fiscal sponsor % (Sch I $) | Non-501(c)(3) code % (Sch I $) | DAF/CF-named % (Sch I $) | Sch F Part II foreign recipients (ED/recognized; "other") |
|---|---|---|---|---|---|---|---|---|
| Fidelity Charitable | 7/24–6/25 | $15,234,325,366 | $73,166,269 | 0.48% | 1.27% | 0.00% | 13.97% | 121; 0 |
| DAFgiving360 | 7/24–6/25 | $8,764,086,228 | $108,766,735 | 1.23% | 1.05% | 0.00% | 18.47% | count line blank in render |
| Vanguard Charitable | 7/24–6/25 | $3,499,146,686 | $4,179,293 | 0.12% | 0.45% | 0.00% | 9.56% | 21; 0 |
| National Philanthropic Trust | 7/24–6/25 | $6,104,565,909 | $310,506,570 | 4.84% | 1.70% | 0.13% (170(c)(1) govt) | 17.41% | 560; blank |
| Silicon Valley CF | CY2024 | $3,162,318,046 | $160,055,648 | 4.81% | 0.74% | 0.81% | 55.22% (incl. $1.59B to NPT) | 6; **308** |
| Chicago Community Trust | 10/24–9/25 | $1,217,385,518 | $7,952,000 | 0.65% | 2.35% | 0.90% | 8.63% | 20; 0 |
| Greater Kansas City CF | CY2024 | $353,684,313 | $643,000 | 0.18% | 0.12% | 0.15% | 3.21% | n/a |
| National Christian Fdn | CY2024 | $2,604,923,993 | none reported | 0% | 0.03% | **20.34%** (religious org 15.6%; 509(a)(3) 4.6%) | 5.71% | n/a |
| Jewish Communal Fund | 7/24–6/25 | $926,758,246 | $96,647,950 | 9.44% | 5.55% | 0.00% | 2.54% | 31; blank |
| ImpactAssets | CY2024 | $587,411,247 | $4,585,784 | 0.77% | 3.95% | 0.00% | 31.01% | 40; 0 |
| DonorsTrust | CY2024 | $283,796,842 | $326,806 | 0.12% | 0.01% | 0.00% | 1.61% | n/a |
| Network for Good | CY2024 | $219,943,565 | $190,644 | 0.09% | 1.07% | 0.00% | 1.03% | n/a |
| Greater Horizons | CY2024 | $224,183,118 | $1,579,291 | 0.70% | 0.09% | 0.15% | 7.64% | n/a |
| AOGF (Benevity) | 4/25–3/26 | $2,238,970,784 | $85,293,297 | 3.67% | parse n/a | parse n/a | parse n/a | 8; 0 |
| CAF America | 5/24–4/25 | $734,410,687 | $258,230,706 | 26.00% | parse n/a | parse n/a | parse n/a | 4,152; blank |
| PayPal Giving Fund | CY2024 | $794,381,014 | $3,509,075 | 0.44% | parse n/a | parse n/a | parse n/a | n/a |

### 6.3 Arithmetic

- **Big-4 nationals combined (Fidelity, DAFgiving360, Vanguard, NPT), FY ended 6/30/2025:**
  - Foreign: $73,166,269 + $108,766,735 + $4,179,293 + $310,506,570 = **$496,618,867**.
  - Total grants (L1 + L2 + L3) = **$34,098,743,056**.
  - Foreign share = **1.46%**.
- **Big-4 named fiscal sponsors (Schedule I, parsed):**
  - $188,690,046 (Fidelity) + $90,764,533 (DAFgiving360) + ~$15.4M (Vanguard, 0.45% × $3,432,214,916) + $101,865,828 (NPT) ≈ **$396.7M**.
  - Parsed Schedule I total is ≈ $32,945,851,172, so the share is ≈ **1.20%**.
- **Three community foundations (SVCF + CCT + GKCCF):** foreign $168,650,648 / $4,909,587,381 = **3.44%**.
- **All eight above plus JCF:** foreign $761,917,465 / $40,031,736,633 = **1.90%**.
- **Count-based floor, NPT:** 560 foreign recipient organizations (each >$5k) against the 159,543 grants processed in FY2025 (repo: `research/daf-reconciliation-economics-scenario-model-2026-11-11.md`, citing NPT's annual report) = **≥0.35%** of grants by count. It is a floor because a recipient can receive several grants and grants ≤$5k are not listed.
- **Recipient-based, Fidelity:** 121 listed foreign recipients against 89,889 listed domestic 501(c)(3)/government recipients = **0.13%** of listed recipients.

### 6.4 Bounded estimate (labelled)

- **Fact-based floor:** Legally non-standard grants are about **1.5% of dollars** at the big-4 nationals. These are foreign grants needing equivalency determination (ED) or expenditure responsibility (ER) under §4966/§4945(h); the sponsors' Schedule F narratives describe ED and/or ER procedures [S20, S31, S59, S60].
- **[Inference] Central estimate of grants that plausibly route to human review, by dollars:**
  - Foreign (1.46%) + named fiscal sponsors (≈1.2%) + non-(c)(3) codes (≈0.03%) ≈ **2.5–3%** at the big-4 nationals.
  - **About 4–6%** at large community foundations, driven by SVCF.
  - **About 15%** at JCF (foreign 9.4% + fiscal sponsors 5.6%).
  - **About 20%** at NCF if church and supporting-organization verification counts as "non-standard".
- **[Inference] By count it is much smaller, roughly 0.3–1% at nationals.** Foreign and fiscal-sponsor grants are larger on average than retail domestic grants (Fidelity's foreign recipients averaged ~$605k per listed recipient: $73.2M / 121).
- **Section 4966 ER cases specifically:**
  - Only SVCF reports a material count of foreign "other organizations" (308, i.e. not ED-recognized). That is consistent with ER grants.
  - Fidelity, Vanguard, CCT, ImpactAssets and AOGF report 0.
  - DAFgiving360 says it uses ER only "in a limited number of cases" [S59].
  - [Inference] ER is rare at nationals and concentrated at community foundations and specialists (CAF America).
- **What 990s cannot see:**
  - New-charity first-grant reviews, purpose restrictions, impermissible-benefit or pledge flags, private-foundation/Type III grantees caught pre-grant, donor-controlled supporting organizations, and grants declined (declined grants never appear).
  - The true human-review share is therefore **higher than the 990-observable share**.
  - The repo's batch-2A file records Vanguard's 2-business-day standard versus 2–10 days for new charities. That is the best public signal of an additional "new grantee" review cohort.

---

## 7. Open questions

1. **Give Interactive:** full client list (beyond Vanguard Charitable and The Signatry), Vanguard go-live status, contract scope (recordkeeping only, or also donor UX), and funding/ownership.
2. **Is Cleveland Foundation's iPhi still on Ren's current roadmap?** What is Ren's iPhi CF retention since 2023? (Repo: iPhi 175-client lead.)
3. **NCF and SVCF on Salesforce:** in-house or partner build? Which fund-accounting ledger sits underneath?
4. What does Foundant's "700+ community foundations" count cover (U.S./Canada; CommunitySuite vs GLM-only)?
5. Customer counts for NPact and Blackbaud FE NXT among U.S. CF DAF sponsors.
6. Chicago Community Trust and GKCCF portal vendors (sites blocked automated fetch).
7. Who owns or legally operates DAF Direct (the `fmr.com` contact suggests Fidelity)? Is BNY Mellon Charitable still active?
8. The Signatry's legal entity and EIN: ProPublica returned "Signatry Charitable Corporation Inc" (82-5047698) with no e-file data. Its 990 is needed to compare with NCF.
9. **Q-B15 extensions:**
   - Run the parser across 3+ years for trend.
   - Add a full fiscal-sponsor list (for example from the National Network of Fiscal Sponsors directory) to tighten the lower bound.
   - Reconcile NPT's "560 recipients" with the count of its foreign grants.
   - Obtain DAFgiving360's Schedule F count (blank in render).
10. Funding and AI deployment evidence for Endaoment, Groundswell, Instrumentl, Grantable, Every.org, and any "agentic philanthropy" entrants. Not searched because the budget was exhausted.

---

## 8. Data dictionary: `data/mission-2026-11-14/breadth-entity-profiles.csv`

| Column | Type | Definition |
|---|---|---|
| entity | text | Common name of the organization or product. Legal names are in `legal_role` where they differ. |
| segment | enum-ish text | community_foundation_sponsor; cf_software_vendor; daf_software_vendor; faith_affinity_sponsor; ideological_affinity_sponsor; impact_sponsor; giving_platform_sponsor; workplace_giving; nonprofit_daf_capture; charity_data_provider; fiscal_sponsor_grantee_class; emerging_direct; emerging_adjacent |
| legal_role | text | Role in DAF flows: sponsor (501(c)(3) holding DAF assets), technology vendor, payment/intake, data provider, or a combination. |
| EIN_if_charity | text | IRS EIN in NN-NNNNNNN format. Blank if not a charity or not verified. |
| latest_assets_or_scale_with_period | text | Latest dated scale metric with its period and basis (Form 990 total assets, Schedule D DAF value, or vendor-stated count). Vendor-stated figures are marked "(vendor-stated)". |
| technology_or_admin_provider | text | Named platform/vendor powering the sponsor's DAF portal or admin, or "self/in-house" or "unknown". |
| provider_evidence_status | enum | **confirmed** = first-party statement, or first-party page plus DNS showing vendor branding/hosting. **inferred** = indirect signals only (domain, hosting, staff history). **unknown** = no evidence gathered. n/a for vendors/data providers themselves. |
| distribution_channel | text | How the entity reaches donors or clients (direct, advisors, employers, nonprofits, faith networks, API partners). |
| notable_capabilities | text | Capabilities evidenced in sources (e.g., ED/ER procedures, fund accounting, API). |
| ai_claims | text | AI claim and evidence class: A=announced; D=demonstrated/beta; E=deployed with evidence; U=unverified marketing; none=no claim found on fetched pages; not_assessed. |
| source_urls | text | Semicolon-separated URLs supporting the row. |
| retrieved_date | date | Date the sources were retrieved (2026-11-14). |
| open_questions | text | Unresolved items for follow-up. |

---

## 9. Source register (all retrieved 2026-11-14)

- S01 Give Interactive, "Vanguard Charitable Partners with Give Interactive..." (PRNewswire Nov 4, 2025, reposted): https://www.giveinteractive.com/post/vanguard
- S02 The Signatry homepage (log-in link to giveinteractive): https://thesignatry.com/
- S03 Signatry log-in: https://thesignatry.giveinteractive.com/log-in
- S04 Give Interactive homepage: https://www.giveinteractive.com/
- S05 Give Interactive company/team: https://www.giveinteractive.com/company
- S06 Cleveland Foundation portal ("Powered by Stellar Technology Solutions, LLC"): https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx ; homepage https://www.clevelandfoundation.org/
- S07 ImpactAssets homepage (client log-in at iphi.stellartechsol.com/calvert): https://impactassets.org/
- S08 Google Public DNS (dns.google/resolve) lookups for secure.ncfgiving.com, donor.siliconvalleycf.org, www.iphiview.com, iphi.stellartechsol.com, client.mydonorstrust.org, npo.givingafoundation.app: https://dns.google/resolve?name=secure.ncfgiving.com&type=CNAME (and equivalents)
- S09 NCF log-in "MyGiving with NCF": https://secure.ncfgiving.com
- S10 Foundant CommunitySuite: https://www.foundant.com/products/communitysuite/
- S11 Foundant Fia release (GlobeNewswire, Sep 2, 2026): https://www.financialcontent.com/article/gnwcq-2026-9-2-foundant-introduces-fia-a-new-ai-platform-built-for-social-good-organizations
- S12 Foundant–SmartSimple merger (Business Wire, Aug 13, 2024): https://businesswire.com/news/home/20240813514222/en/Foundant-Technologies-and-SmartSimple-Software-Announce-Strategic-Merger-to-Revolutionize-Philanthropic-and-Grant-Management-Solutions
- S13 Foundant family page: https://www.foundant.com/about/foundant-smartsimple-givingdata
- S14 Columbus Foundation homepage and fund portal: https://columbusfoundation.org/ ; https://columbusfdn.fcsuite.com
- S15 NPact acquires FIMS and DonorCentral NXT (PR Newswire, Sep 12, 2022): https://prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html
- S16 Blackbaud Financial Edge NXT for grantmaking organizations: https://www.blackbaud.com/industry-insights/resources/foundations/blackbaud-financial-edge-nxt-for-grantmaking-organizations
- S17 Grant Edge NXT listing / Tech Impact guide: https://www.g2.com/products/grant-edge-nxt/reviews ; https://guides.techimpact.org/grants-management-systems/?p=639
- S18 Give Interactive Fund of Funds (Aug 17, 2026) and Give Legacy Fund (Aug 24, 2026): https://www.giveinteractive.com/post/fund-of-funds-platform ; https://www.giveinteractive.com/post/give-interactive-launches-give-legacy-fund-bringing-a-perpetual-giving-platform-to-daf-sponsors
- S19 ProPublica Nonprofit Explorer API and e-file renders: https://projects.propublica.org/nonprofits/api ; https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990ScheduleF
- S20 SVCF 990 CY2024 (object 202543149349305759): https://projects.propublica.org/nonprofits/organizations/205205488/202543149349305759/IRS990ScheduleI
- S21 CCT 990 FY9/2025 (202632239349302058): https://projects.propublica.org/nonprofits/organizations/362167000/202632239349302058/IRS990
- S22 GKCCF 990 CY2024 (202533189349314033): https://projects.propublica.org/nonprofits/organizations/431152398/202533189349314033/IRS990
- S23 Columbus Foundation 990 CY2024 (202513189349305651): https://projects.propublica.org/nonprofits/organizations/316044264/202513189349305651/IRS990
- S24 Cleveland Foundation 990 CY2024 (202543189349305969): https://projects.propublica.org/nonprofits/organizations/340714588/202543189349305969/IRS990
- S25 Greater Horizons 990 CY2024 (202513189349309621): https://projects.propublica.org/nonprofits/organizations/200849590/202513189349309621/IRS990
- S26 (reserved)
- S27 CCT financials FY2025: https://www.cct.org/about/financials/ ; https://www.cct.org/wp-content/uploads/2026/05/CCT-6051-Financials_2025_L3.pdf
- S28 Chronicle of Philanthropy on GKCCF DonorEdge (2006): https://www.philanthropy.com/news/web-site-gives-donors-data-on-charities/
- S29 Cleveland Foundation 2025 year-in-review (Feb 19, 2026): https://www.clevelandfoundation.org/stories-events/stories-news/2026/02/19/looking-back-on-a-year-of-partnership-and-impact
- S30 NCF 990 CY2024 (202513109349303201): https://projects.propublica.org/nonprofits/organizations/581493949/202513109349303201/IRS990ScheduleI
- S31 JCF 990 FY6/2025 (202640629349300234): https://projects.propublica.org/nonprofits/organizations/237174183/202640629349300234/IRS990ScheduleF
- S32 DonorsTrust 990 CY2024 (202513179349312256) and homepage: https://projects.propublica.org/nonprofits/organizations/522166327/202513179349312256/IRS990 ; https://www.donorstrust.org/
- S33 NCF About: https://www.ncfgiving.com/about/
- S34 PayPal Giving Fund 990 CY2024 (202533079349301308): https://projects.propublica.org/nonprofits/organizations/450931286/202533079349301308/IRS990ScheduleD
- S35 PayPal Giving Fund About: https://www.paypal.com/us/webapps/mpp/givingfund/about
- S36 AOGF 990 FY3/2026 (202642259349301349): https://projects.propublica.org/nonprofits/organizations/810739440/202642259349301349/IRS990ScheduleF
- S37 Blackbaud Giving Fund 990 CY2025 (202622529349301602): https://projects.propublica.org/nonprofits/organizations/460942102/202622529349301602/IRS990
- S38 Network for Good 990 CY2024 (202513039349301631): https://projects.propublica.org/nonprofits/organizations/680480736/202513039349301631/IRS990
- S39 Givinga Foundation 990 CY2024 (202503179349301975): https://projects.propublica.org/nonprofits/organizations/474172718/202503179349301975/IRS990ScheduleD
- S40 Givinga homepage: https://www.givinga.com/
- S41 Givinga Foundation homepage: https://www.givingafoundation.org/
- S42 CAF America 990 FY4/2025 (202610489349300906): https://projects.propublica.org/nonprofits/organizations/431634280/202610489349300906/IRS990ScheduleF
- S43 ImpactAssets 990 CY2024 (202543169349307999): https://projects.propublica.org/nonprofits/organizations/262048480/202543169349307999/IRS990ScheduleI
- S44 Benevity homepage: https://benevity.com/
- S45 DAF Direct: https://www.dafdirect.org/
- S46 The Giving Block About: https://thegivingblock.com/about/
- S47 GivingIQ announcement (Apr 30, 2026): https://givingiq.com/press/announce
- S48 IRS TEOS bulk data downloads: https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads
- S49 Candid developer portal: https://developer.candid.org/
- S50 Charity Navigator API terms/products: https://www.charitynavigator.org/products-and-services/api/
- S51 Endaoment homepage: https://endaoment.org/
- S52 Endaoment 990 FY6/2025 (202631359349315978): https://projects.propublica.org/nonprofits/organizations/844661797/202631359349315978/IRS990ScheduleD
- S53 Daffy Charitable Fund 990 CY2024 (202513209349301201): https://projects.propublica.org/nonprofits/organizations/863177440/202513209349301201/IRS990ScheduleD
- S54 Groundswell DAF: https://www.groundswell.io/products/donor-advised-fund
- S55 Givefront homepage: https://www.givefront.com/
- S56 TechCrunch on Givefront (Dec 18, 2025; repo source): https://techcrunch.com/2025/12/18/these-21-year-old-dropouts-raised-2m-to-build-givefront-a-fintech-for-nonprofits/
- S57 Instrumentl homepage: https://www.instrumentl.com/
- S58 Grantable homepage: https://www.grantable.co/
- S59 DAFgiving360 990 FY6/2025 (202611199349300601): https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF
- S60 Fidelity Charitable 990 FY6/2025 (202601389349301700), NPT 990 FY6/2025 (202601289349302480), Vanguard Charitable 990 FY6/2025 (202621329349306657): https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990 ; https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF ; https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990
