# Batch 35 B: delegated-access routes (P-B34C-03), For Good / DCSO (P-B34B-03), TIFIN Give separation signals (P-BUY-04), unassigned faith sponsors (P-B33C-03), pool weights (P-B32A-02)

Prepared 2026-11-15 by the batch 35 B agent. These are files only: no commit, no outreach, no logins, no form submissions.

**Evidence labels:**
- **[F]** filed or first-party document read this batch.
- **[C]** computed here.
- **[R]** search-index snippet or third-party report; the page itself was not read.
- **[I]** inference.
- **[X]** carried from the repo.

**Recency:** everything is 2021+. The one exception is a 2009 Schwab proxy, cited only to show the method in §5.3.

**Outputs:**
- [`delegated-access-routes-2026.csv`](../../data/mission-2026-11-14/delegated-access-routes-2026.csv): 21 routes, top-20 sponsors.
- [`relationship-graph-edges-additions-20.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-20.csv): ET001–ET011.
- [`queue-proposals-batch35b.csv`](../../data/mission-2026-11-14/queue-proposals-batch35b.csv): P-B35B-01 to P-B35B-03.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B34C-03 delegated access** | **No top-20 document names a software service as an appointable party.** Every documented route appoints a person, or at most an advisory firm, and most issue that person their own credentials. Three texts leave room for a sanctioned non-human path: <br>- **Vanguard Charitable** lets an Authorized Person, who holds their own Vanguard-issued credentials, use "aggregators", while still barring bots. <br>- **GS DAF** lets the donor appoint "another third party" as agent. <br>- **SVCF** bars third-party portal access only "without SVCF's prior approval". <br>Fidelity has narrowed its wording: an Authorized Person "is an individual", though associates at that person's firm can get firm-wide access. | High (texts); [I] for agent feasibility |
| **P-B34B-03 DCSO / For Good** | DCSO (EIN 99-0468956, Delaware, formed 2024) files as **"The Resiliency Company"**, a climate-resilience "parent organization" with 10 employees. Its first 990 is for CY2024. <br>- **Money:** it received about **$27.0–27.5m** from Network for Good and gave back **$200,000 "for the giving collaborative"**. <br>- **Management:** shared. Abby Ross is CEO of both; Stephanie Goldfine is GC of both. <br>- **Name:** Network for Good now trades as **For Good**; its IRS name is "Forgood Inc". <br>- **Volume:** For Good's 2024 report shows **$193.1m** of DAF grants and **$219.7m** processed. <br>- **Bonterra:** it describes a "continued technology and fundraising relationship" with Bonterra Tech. <br>- **Not yet available:** the CY2025 990 is not indexed. | High (filings, first-party report) |
| **P-BUY-04 TIFIN Give** | **No public evidence of a strategic review, banker mandate or carve-out hire for TIFIN Give.** <br>Separation signals [I]: <br>- TIFIN folded its AI businesses into TIFIN.AI (Apr 2026), and TIFIN Give is not among them. <br>- TIFIN has spun units out before: AMP (June 2023, independent board and Series A), AG (2024), and 55ip, sold to J.P. Morgan. <br>- It divested Giving Place (Apr 2025). <br>- An executive-in-residence joined TIFIN Give's board (Mar 2025). <br>Commercial momentum continues: SEI white-label (Jan 2026), Confluence (Feb), Canterbury (Apr), and the SEI Charitable Fund (Oct 2026). | Medium (absence of evidence; [R]-heavy) |
| **P-B33C-03 faith platforms** | **7 of the 8 named sponsors are resolved from their own websites:** <br>- **Ren iPhi:** Atlanta (EIN 58-1021791), Greater Washington (53-0212445), JUF Chicago and Knights of Columbus (already EK004). <br>- **Foundant CommunitySuite:** Dallas JCF and Christian Community Foundation of Memphis (62-1752885). <br>- **NPact DonorCentral:** Houston JCF. <br>That is $1.35bn of FY2024 DAF assets. **JCF NY ($2.87bn) is still unresolved.** Its portal is login.jcfny.org behind Cloudflare, and 990s for FY2024 and FY2025 name no platform vendor. | High (7); low (JCF) |
| **P-B32A-02 pool weights** | **Vanguard Charitable: resolved.** Its audited statements (Note 3) list every pool balance. Weighted by the published pool expense ratios, in-fund cost is **≈3.6 bps** (FY2026 balances) and 3.8 bps (FY2025). With unpriced holdings included, the bounds are 3.5–4.8 bps. This replaces the 1–59 bps range. <br>**DAFgiving360 and NPT: not resolved.** NPT publishes only summary statements. The SEC and Schwab fund-document hosts returned 403 on robots.txt, so they were not read. | High (Vanguard [F]+[C]); open (others) |

---

## 1. P-B34C-03: sanctioned delegated-access routes in top-20 sponsor documents

Detail: [`delegated-access-routes-2026.csv`](../../data/mission-2026-11-14/delegated-access-routes-2026.csv). Documents read this batch:
- [Fidelity Program Guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf) (PDF 2026-09-11)
- [Fidelity CIAP guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-investment-policies-and-guidelines.pdf) (June 2026)
- [NPT donor guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) (PDF 2026-10-15)
- [Vanguard User Agreement](https://www.vanguardcharitable.org/company-policies/user-agreement) (May 2025)
- [SVCF agreement](https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf)
- [BofA Program Guidelines 2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf)
- [JCF Policy Guide](https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf) (Aug 2024)
- [GKCCF Terms](https://www.growyourgiving.org/terms-of-use/)
- [CJP DAF Policies](https://www.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf?hsLang=en)

The other rows are carried from the census [X].

### 1.1 What each route admits

| Sponsor | Route | Who may be appointed | Entity? | Software? | Credentials |
|---|---|---|---|---|---|
| Fidelity | Authorized Person | "an individual designated by an Account Holder"; with permission, "associates at the firm of the Authorized Person" | P (firm associates) | N | not in Guidelines |
| Fidelity | CIAP Advisor | qualified adviser firm, unrelated to the donor | Y | N | — (no grant rights: "not authorized … to submit grant recommendations") |
| NPT | secondary / financial advisor | full or read-only; financial advisors "do not have independent advisory privileges" | P | N (bot ban [X]) | NPT-authorized persons only [X] |
| DAFgiving360 | Schwab Advisor Center | "view-only access" [X] | P | N | Schwab terms [X] |
| **Vanguard** | Interested Party → Authorized Person | person who files the access form and gets a VC-issued login | P | **P: "An Authorized Person may use "aggregators" or similar web crawler devices for the purpose of aggregating information"** | **issued separately**; sharing barred "including charities or grant recommendation processing services" |
| **GS DAF** | agent | PWM team "(or another third party)" [X] | P | unclear | not stated |
| **SVCF** | Fund / Secondary Advisor / Fund Representative; third-party access | individuals; a third party with prior approval | P | unclear | — |
| BofA CGF | Advisor | "one or more individuals"; US taxpayers; same powers as donor | N | N | MyMerrill / BofA terms not read |
| JCF | Authorized Party; POA | "relatives, employees, or professional advisors"; POA "third party" | P | N | portal login.jcfny.org |
| GKCCF / Greater Horizons | Authorized Use | "Financial advisors managing Community Foundation funds may access and use their Account" | P | N (aggregator only for an Authorized Use) | own Account |
| NCF | none; strict ban [X] | — | — | N | each person approved; no sharing with advisors [X] |
| CJP, CCT, RCF, AEF, MS GIFT, ImpactAssets, FFTC | none documented, or staff-managed | — | — | — | — |
| Dechomai, Raymond James | not read | — | — | — | — |

**SVCF data and approval clauses [F]:**
- **Data:** SVCF bars Authorized Advisors from collecting information "(through automated means or otherwise) … for any purposes unrelated to the Authorized Advisor's grantmaking advisory privileges". The ban is tied to purpose, so automated collection for the advisor's own grantmaking is not barred.
- **Third parties:** "Any access granted to a third party by an Authorized Advisor without SVCF's prior approval will be solely at the Authorized Advisor's risk."

**JCF [F]:**
- Authorized Parties "may obtain confidential information about the fund, including fund balance, investment allocation, and grant history via online access or over the phone".
- They may also sign grant and investment recommendations.
- A POA "may authorize a third party to submit grants, investment recommendations, and other privileges".

### 1.2 Reading for an AI agent [I]

1. **Credential sharing is not a sanctioned route anywhere it is addressed.** NCF, Vanguard, NPT and GKCCF bar it, as do SVCF's and Fidelity's online terms [X]. The sanctioned pattern is the opposite: **the sponsor issues the appointee their own credentials** (Vanguard Authorized Person, GKCCF advisor Account, JCF Authorized Party online access, Fidelity firm-wide associates).
2. **The only automated path a top-20 text expressly permits is read-only.** Vanguard lets an Authorized Person run aggregators. A tool operated by a properly appointed Interested Party, using that party's own login, appears to fit. Grant submission by a bot does not, because "electronic agent, bot" access is barred.
3. **An entity agent is possible in principle at GS DAF and SVCF, and through a POA at JCF.** None of the three publishes how to appoint one. P-B35B-03 asks for the forms.
4. **The agent-access matrix should change from batch 34C as follows** (proposed, not applied):
   - Vanguard: "automated read permitted for appointed persons".
   - Fidelity: "human delegation only (individual)".
   - SVCF: "third-party access by prior approval".
   - JCF: "human or POA delegation".
   - BofA: "human delegation only".
   - CJP: "none documented".

---

## 2. P-B34B-03: Durable Capital for Sustainable Outcomes and For Good

**DCSO CY2024 Form 990** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503189349302575_public.xml)) [F]:

| Field | Value |
|---|---|
| Identity | EIN 99-0468956, Washington DC; formed 2024, Delaware; dba **The Resiliency Company**; website resiliency.com |
| Mission | "mobilizes the funding, policies, and innovation required to decrease the financial impact of climate disasters and hazards" |
| Size | Revenue $27,461,203, almost all contributions ($27,334,203); expenses $2,420,846; total assets $25,357,393; 10 employees |
| Program service fees | $127,000 |
| Grants out | $200,000, all to "NETWORK FOR GOOD (DBA FOR GOOD)", purpose "FOR THE GIVING COLLABORATIVE" (Sch I). Sch O: grants went "SOLELY" to its subsidiary, monitored "THROUGH OVERLAPPING MANAGEMENT" |
| Schedule R | NFG listed as a related tax-exempt org it controls ("GRANTMAKING THROUGH DONOR ADVISED FUNDS"). Transactions with NFG: <br>- code B $200,000 <br>- **code C $26,957,291** <br>- L $110,000 <br>- O $82,500 <br>- P $58,407 <br>(Standard Sch R Part V codes: C = grant from related org; L = services for; O = shared employees; P = reimbursement paid to) |
| Board | Timothy Scott Case (chair), Danica Remy (treasurer), Maureen Sullivan; 3 voting members |
| Officers | Abigail Ross, President & CEO ($225,000 from DCSO plus $125,000 from related orgs); Stephanie Goldfine, Secretary & GC ($184,026 plus $104,308) |
| Contractors | Frontline Solutions International (strategic learning) $182,011; Future Forest Studio (strategic advisory) $100,500 |

**For Good 2024 Annual Report** ([PDF](https://cdn.prod.website-files.com/6462856520f6ad95c7d6e2da/6a8386bfae9f58936876e2b4_For%20Good%202024%20Annual%20Report.pdf), linked from [forgood.org](https://www.forgood.org/who-we-are)) [F]:
- **Volume:** "$219.7 million in total donations processed in 2024"; **$193.1m** of DAF grants; net DAF donations $193.5m.
- **Revenue and costs:** earned revenue $9.76m. Operating expenses were $38.5m, including a "$24.6 million one-time, Board-approved grant", or about $13.9m without it.
- **Balance sheet:** net assets $19.0m on $96.2m of assets.
- **Change of control:** in June 2024 the board made For Good "a subsidiary of The Resiliency Company (formerly Durable Capital for Sustainable Outcomes)". It "committed $27.47 million in grants to The Resiliency Company during 2024", of which "$2.9 million was disbursed by year-end".
- **Partners:** Google, Walmart, Patagonia, Deed, Every.org, GlobalGiving and Tremendous, "alongside our continued technology and fundraising relationship with Bonterra Tech, LLC (formerly NFG.com)".
- **People:** NFG board in the report: Scott Case (chair), Tim Willey, Brian Sasscer. Remy and Sullivan left in June 2024 to join the Resiliency Company board. The executive team is shared with DCSO (Ross, Goldfine).
- **Name:** forgood.org: "Network for Good Donor Advised Fund is now ForGood, Inc." The IRS/ProPublica name is "Forgood Inc" ([ProPublica](https://projects.propublica.org/nonprofits/organizations/680480736)). A May 2025 release announced the new name [R: [Business Wire 2025-05-29](https://www.businesswire.com/news/home/20250529977479/en/Donor-Advised-Fund-Network-for-Good-Unveils-New-Name-For-Good)]. The annual report dates the rebrand to 2023, so the sources conflict on the date.

**Answers:**
1. **What is DCSO?** A climate-resilience nonprofit parent, staffed by For Good's own CEO and GC, capitalised almost entirely by a ~$27m transfer from the DAF sponsor's operating reserves. The grant purpose, a "change-of-control" grant, and the weight of the transfer against NFG's ~$13.9m operating budget are filed facts. Whether this is an appropriate use of a DAF sponsor's unrestricted assets is a governance question for the governance file, not settled here [I].
2. **What is the giving collaborative?** Its only public trace is the $200,000 grant purpose. No program description was found.
3. **Is volume falling?** For Good reports $193.1m of grants for CY2024, against the 990's $199.8m (batch 34B). The bases differ (grants paid vs. DAF-column grants). The CY2025 return is not indexed, so the trend after 2024 is unknown.
4. **Does Bonterra depend on NFG?** The relationship is described as "continued". The Bonterra Tech fee fell $4.77m → $2.49m (CY2023→CY2024 [X]).
5. **Discrepancy to note:** $26.96m (DCSO Sch R), $27.33m (DCSO contributions), $27.47m (committed) and $27.5m (batch 34B, NFG side) all describe the same transfer. Only $2.9m was paid by 2024-12-31 per For Good, yet DCSO records the contribution as revenue. That fits a pledge receivable [I].

---

## 3. P-BUY-04: is TIFIN Give being prepared for separation or sale?

**Search result:** no report of a strategic review, banker mandate, sale process or carve-out hire for TIFIN Give in 2025–26 (searches 2026-11-15). tifin.com news pages returned 404 this batch, so items below rest on search snippets and syndicated copies [R].

| Date | Event | Source |
|---|---|---|
| 2023-06 | TIFIN AMP spun off with a $10m Series A (Motive) and a board independent of TIFIN | [PR Newswire](https://prnewswire.com/news-releases/tifin-amp-announces-spinoff-with-independent-series-a-funding-backed-by-motive-partners-and-tifin-301845592.html) [R] |
| 2024 | TIFIN AG spin-off announced | [PR Newswire](https://www.prnewswire.com/news-releases/tifin-announces-the-spin-off-of-tifin-ag-an-ai-platform-to-help-wealth-enterprises-drive-net-new-assets-302041452.html) [R] |
| 2025-03-11 | Brian McDonald joins TIFIN as executive in residence and "will join the boards of TIFIN @Work and TIFIN Give" | [syndicated copy](https://redmondspokesman.com/2025/03/11/brian-mcdonald-joins-tifin-as-executive-in-residence) [R] |
| 2025-04-21 | Giving Place sold to Foundation Source so Give can focus on DAF solutions | [X] (repo) |
| 2025 (late) | Andrew Dahlinghaus named TIFIN COO | [StreetInsider](https://www.streetinsider.com/PRNewswire/TIFIN+Appoints+Andrew+Dahlinghaus+as+Chief+Operating+Officer/25710740.html) [R] |
| 2026-01-29 | TIFIN Give partners with SEI for white-label DAFs for bank and trust clients | [PR Newswire](https://www.prnewswire.com/news-releases/tifin-give-partners-with-sei-to-deliver-white-labeled-donor-advised-fund-solutions-to-bank-and-trust-clients-302674049.html) [R] |
| 2026-02-26 | Confluence Financial Partners | [GlobeNewswire](https://www.globenewswire.com/news-release/2026/02/26/3245703/0/en/tifin-give-to-power-donor-advised-fund-experience-for-confluence-financial-partners.html) [R] |
| 2026-04-01 | Canterbury Consulting | [GlobeNewswire](https://www.globenewswire.com/news-release/2026/04/01/3266455/0/en/TIFIN-Give-Works-With-Canterbury-Consulting-to-Expand-Strategic-Philanthropic-Planning-Capabilities.html) [R] |
| 2026-04-14/20 | TIFIN consolidates "its AI businesses" into TIFIN.AI (Nair executive chair; Bindal CEO). TIFIN Give is not mentioned | [Pulse 2.0, 2026-04-20](https://pulse2.com/tifin-group-launches-tifin-ai-to-unify-enterprise-ai-workflows-in-wealth-management/) [F, trade report] |
| 2026-10-28 | SEI Charitable Fund launched, powered by TIFIN Give and sponsored by GiveClear | repo E048/E049 [X] |

**Reading [I]:**
- **TIFIN's pattern is to give each unit its own board and outside capital, then spin it out or sell it** (AMP, AG, 55ip).
- **TIFIN Give already has a separate board seat** (McDonald) and sits outside TIFIN.AI. Structurally it is separable.
- **Nothing public shows a process underway.** The 2026 cadence (four channel wins) reads as scaling, not preparing for sale. Treat "being prepared for sale" as **unsupported**, and "separable" as **supported**.
- **Natural buyers:**
  - SEI: investor (E051), with two live channels (SEI white-label and the SEI Charitable Fund).
  - J.P. Morgan: investor; bought 55ip from TIFIN.
  - Franklin Templeton and Morningstar: investors.
  - SS&C: an ALPS DAF program partner, not a recorded investor (queue text).
  - Foundation Source: bought Giving Place.
- This list is ranked by observed ties, not by stated interest.

---

## 4. P-B33C-03: platforms of the unassigned faith sponsors with more than $100m

Method: each sponsor's own homepage or DAF page (robots.txt allows `*`), reading the login link target. Vendor hosts (iphiview.com, fcsuite.com) were not used as evidence, because their robots.txt disallows this agent (§7).

| Sponsor (EIN) | FY2024 DAF assets | Login link found | Platform | Edge |
|---|---|---|---|---|
| Jewish Federation of Greater Atlanta (58-1021791) | $283.5m | atlantajewishfoundation.org → `jfga.iphiview.com/jfga/` | **Ren iPhi** | ET004 |
| Jewish Federation of Greater Washington (53-0212445) | $125.5m (DAFRC imputed) | shalomdc.org "Donor Dashboard" → `www.iphiview.com/ujef/` | **Ren iPhi** | ET005 |
| JUF / Jewish Federation of Metropolitan Chicago (36-2167761) | $312.0m | juf.org Donor Resources: "log in to your Donor View account" → `jfmc.iphiview.com/jfmc/` | **Ren iPhi (current)** | ET006 |
| Knights of Columbus Charitable Fund (81-5466677) | $130.8m | knightscharitable.org → `ccfnj.iphiview.com/kofc/` | **Ren iPhi** (already EK004; administration by KofC Asset Advisors, ES021) | — |
| Christian Community Foundation of Memphis (62-1752885) | $212.7m | ccfmemphis.com → `ccfmemphis.fcsuite.com/erp/portal` | **Foundant CommunitySuite** | ET008 |
| Dallas Jewish Community Foundation (75-2836123) | $162.5m | djcf.org "My DJCF Login" / "Access Your Fund" → `djcf.fcsuite.com` | **Foundant CommunitySuite** | ET007 |
| Houston Jewish Community Foundation (76-0187329) | $125.7m | hjcf.org → `hjcf.donorcentral.com` | **NPact DonorCentral** (FIMS ledger likely [I]) | ET009 |
| Jewish Communal Fund NY (23-7174183) | $2,870.6m | Policy Guide: "Visit the JCF donor portal at https://login.jcfny.org" (Cloudflare-proxied, challenge page) | **unresolved** | — |

Asset figures are DAFRC FY2024 from `faith-sponsor-platforms-2026.csv` and `dafrc-sponsor-schedule-d-fy2019-2024.csv` [X].

**JCF NY detail:**
- **990s [F]:** FY6/2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202500369349300210_public.xml)) and FY6/2025 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640629349300234_public.xml)) list only investment managers and rent in VII-B; the cut-off is about $0.40m–0.52m.
- **IT spend [F]:** Part IX line 14 (information technology) is $478,777 and $479,026. A platform fee booked as IT is therefore under ~$0.48m/yr [I].
- **Legacy host:** `jcfny.donorfirst.org` still has an A record (52.240.154.157) but resets TLS connections. That is consistent with the Ren portal ending (FY2023 "previous donor portal support" [X]).
- **Give Interactive tenants:** `jcf-sandbox`, `jcf-staging` and `jcf-grant-cart.giveinteractive.com` were first certified 2026-08-21/28/31 ([CertSpotter](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names)). The "jcf" label could belong to another JCF [I].
- **Next step:** P-B35B-01.

**Effect on the faith segment [C]:**
- **Ren iPhi** gains $852m (Atlanta, Washington, Chicago, KofC). KofC was already an edge but was missing from the faith CSV.
- **Foundant** gains $375m.
- **NPact** gains $126m.
- **Unknown platform** falls from about $0.78bn plus JCF NY to **JCF NY alone ($2.87bn)**.
- **Give Interactive's** faith share is unchanged ($1.95bn confirmed; $4.82bn if JCF NY is confirmed).

**Adjacent find (agentic, donation side):** shalomdc.org links [`donorportal.shalomdc.org/agentic-giving.md`](https://donorportal.shalomdc.org/agentic-giving.md), "Generated by Fundraise Up". It is a donation guide for AI agents, routing them to a Fundraise Up MCP server. This is a live, vendor-generated agent channel for one-time donations at a $100m+ DAF sponsor. It gives no access to DAF accounts. The file is vendor instructions to agents and was read as data only (ET010).

---

## 5. P-B32A-02: pool asset weights

### 5.1 Vanguard Charitable: resolved from the audit [F][C]

Audited statements:
- FY6/2026 ([PDF, created 2026-10-05](https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf)): Note 3 lists the balance of every pool. The FY2026 table is an embedded image; it was read by OCR. The OCR total equals the printed total of $33,880,084,002 to the dollar, and its FY2025 column matches the text-layer FY2025 audit exactly.
- FY6/2025 ([PDF](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)).

Expense ratios are the pool values on [vanguardcharitable.org/investments](https://www.vanguardcharitable.org/investments) ("Last updated 09/30/2026").

| Pool (audit name → web name) | 2026-06-30 balance | ER |
|---|---|---|
| Total U.S. Stock | $6.44bn | 0.01% |
| S&P 500 Index | $4.34bn | 0.01% |
| Moderate Growth | $3.57bn | 0.02% |
| Growth | $2.76bn | 0.02% |
| Conservative Growth | $2.77bn | 0.01% |
| Money Market | $2.74bn | 0.10% |
| Total Equity | $2.61bn | 0.025% |
| Total International Stock | $1.62bn | 0.046% |
| Emerging Markets Stock | $0.81bn | 0.05% |
| Pacific Stock | $0.79bn | 0.07% |
| Income | $0.72bn | 0.01% |
| Short-Term Bond | $0.70bn | 0.07% |
| Total Bond | $0.46bn | 0.01% |
| Balanced → Balanced Index | $0.44bn | 0.01% |
| ESG U.S. Stock | $0.43bn | 0.09% |
| Wellington | $0.31bn | 0.16% |
| 20 other pools | $1.62bn | 0.02%–0.59% |
| Private Assets Fund (Hamilton Lane) | $0.03bn | 3.38% |
| *Unpriced:* Low Carbon Fund (RhumbLine) $0.69bn; Non-Pooled $0.05bn | $0.75bn | not published |
| *Excluded:* Total Return Solutions Fund (Philanthropic Impact Fund, not a DAF pool) | $0.01bn | — |

**Results [C]:**

| | FY2026 balances | FY2025 balances |
|---|---|---|
| Coverage (pools with a published ER) | 97.7% | 96.6% |
| Asset-weighted ER, covered pools | **3.58 bps** | 3.83 bps |
| Same, excluding the Private Assets Fund | 3.26 bps | 3.53 bps |
| All investments, unpriced at 0 / at 59 bps | 3.50 / 4.81 bps | 3.70 / 5.72 bps |

**Caveats:**
- Expense ratios are as of 2026-09-30 and are applied to both year-ends. The FY2025 figure therefore assumes unchanged ERs.
- Some pool balances moved sharply in FY2026: Pacific $51m → $789m, Emerging Markets $171m → $805m, Commodity $308m → $45m. These are as printed and tie to the total. No reason is given.

**Consequence:**
- Row N061 (1–59 bps) can be replaced by **≈3.6 bps (3.5–4.8)**.
- N070's all-in bound (19–77 bps) becomes **≈22 bps** (18.4 bps Part IX FY2024 [X] + 3.6). The years are mismatched: FY2024 operating cost against FY2026 in-fund cost.
- Vanguard is then the cheapest national per dollar on the repo's figures, below Fidelity's ≈50–52 bps floor (wave 17 correction).
- **Batch 32's "no audit found online" is superseded for Vanguard.** The repo already cites both PDFs elsewhere.

### 5.2 NPT: summary statements only [F]

[FY25 consolidated financials](https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf) (PDF dated 2026-09-01) contains two pages: position and activities, with no notes and no portfolio balances.
- **Composition:** cash and equivalents $9.24bn and investments at fair value $47.84bn at 2025-06-30.
- **Fee line:** the expense section carries a line labelled "Asset management fees payable" of **$116,260k**. The label repeats a liability caption and is a layout error: the FY2024 PDF prints the same FY2024 figure ($94,289k) as “Program services”, so $116,260k is program services expense excluding grants, not an asset-management fee, and the ≈27 bps reading is withdrawn. The nearest public fee measure is FY2025 990 line 11f (program column $93.5m, 22.4 bps of mean Part X investments) [V wave 36C] It is not in-fund cost and should not replace N063 without the notes.

### 5.3 DAFgiving360: not resolved

- The sponsor's own pages return 403 [X].
- Schwab fund documents (schwabassetmanagement.com) and SEC EDGAR (www.sec.gov) returned HTTP 403 on robots.txt this batch, so they were not fetched (§7).
- The method is viable: a [2009 Schwab proxy](https://www.sec.gov/Archives/edgar/data/0000857156/000095012309055432/f53694adef14a.htm) lists "Schwab Charitable Fund … Growth Pool" as a ~98% record holder of a Schwab MarketTrack portfolio [R; pre-2021, method only].
- Proposal P-B35B-02 asks for a permitted route.

---

## 6. Proposed repo changes (not applied; for the validator)

1. **`faith-sponsor-platforms-2026.csv`:**
   - Fill the rows for 58-1021791, 62-1752885, 75-2836123, 76-0187329 and 815466677, and add 530212445, per §4.
   - Change JUF Chicago `platform_family` from REN_IPHI_HISTORIC to REN_IPHI (live link).
   - Keep JCF NY as GIVE_INTERACTIVE_INFERRED / low.
2. **`infund-expense-nationals-2026.csv` N061/N070:** replace the bounds with the weighted values in §5.1, citing the FY2026 audit Note 3. Add a note that the FY2026 table was read by OCR and ties to the total.
3. **`queue-batch32-infund-costs.md` §1.2:**
   - Find: "Not published, and no audit found online" (Vanguard row).
   - Replace with: "Published: audit Note 3 lists pool balances (FY2025 and FY2026 statements); asset-weighted ≈3.6 bps (batch 35 B)".
4. **Agent-access gap matrix:** apply the §1.2 item 4 flags.
5. **Repo text naming the NFG entity:** add "(dba For Good; IRS name Forgood Inc)". Add that DCSO files as "The Resiliency Company" and that For Good calls it "formerly Durable Capital for Sustainable Outcomes", although the IRS name is unchanged.
6. **`sponsor-terms-census-top20-2026.csv` row 1:** set `sanctioned_delegation_path` to "Authorized Person (an individual; firm-wide access for that person's firm associates; Program Guidelines Sept 2026)". "Authorized Interested Parties" survives only in the CIAP guidelines.

---

## 7. Robots and compliance log

| Host | robots.txt | Action |
|---|---|---|
| jcfny.org, growyourgiving.org, fidelitycharitable.org, vanguardcharitable.org, svcf.org, nptrust.org, juf.org, jewishatlanta.org, atlantajewishfoundation.org, shalomdc.org, djcf.org, ccfmemphis.com, hjcf.org, knightscharitable.org, forgood.org, cjp.org, bankofamerica.com (path allowed), donorportal.shalomdc.org | allow | fetched |
| login.jcfny.org | allow | Cloudflare challenge (403); not bypassed |
| medium.com, resiliency.com / Squarespace site, fcsuite.com | disallow ClaudeBot | not used as evidence |
| iphiview.com | `User-agent: * Disallow: /` (named search engines allowed) | not used as evidence |
| secure.ncfgiving.com | `Disallow: /` for `*` | not used; NCF rows carried from repo |
| www.sec.gov, efts.sec.gov, schwabassetmanagement.com, globenewswire.com | robots.txt returned 403 | not fetched; cited via search index only |
| tifin.com | no robots file | news URLs returned 404 |

**Disclosure.** Before the full robots.txt was read, single requests were made to five places:
- the login pages `djcf.fcsuite.com/erp/portal/list`, `jfmc.iphiview.com/jfmc/` and `www.iphiview.com/ujef/`;
- `secure.ncfgiving.com/agreement`;
- one SEC full-text search query.

Their content was discarded and none of it is used as evidence above. Each row rests on the sponsor's own allowed page or on carried repo text.

No logins, form submissions or contact with any organisation took place.

---

## 8. Limitations

- **TIFIN:** the findings rest on an absence of evidence, and most of it is [R]. A private process would not be public.
- **Vanguard ERs:** the website figure is taken as the pool's in-fund cost. If a pool holds several funds, the site's figure is assumed to be the blended ratio.
- **DCSO:** only one 990 exists. The NFG CY2025 990 and For Good's audited Note 8 (available "upon request") were not available.
- **JCF NY:** the faith-platform status still rests on inference.

---

## Source register

| # | Source | Date | Used for |
|---|---|---|---|
| S1 | [Fidelity Program Guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf) | PDF 2026-09-11 | DA01 |
| S2 | [Fidelity CIAP guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-investment-policies-and-guidelines.pdf) | June 2026 | DA02 |
| S3 | [NPT donor guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) | PDF 2026-10-15 | DA03 |
| S4 | [Vanguard Charitable User Agreement](https://www.vanguardcharitable.org/company-policies/user-agreement) | May 2025 | DA05 |
| S5 | [SVCF Donor Advised Fund Agreement](https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf) | 2025-08-22 [X] | DA07 |
| S6 | [BofA CGF Program Guidelines 2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf) | 2024-09-18 | DA12 |
| S7 | [JCF Policy Guide](https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf) | Aug 2024 | DA16; §4 |
| S8 | [GKCCF Terms of Use](https://www.growyourgiving.org/terms-of-use/) | eff. May 2024 | DA17 |
| S9 | [CJP DAF Policies](https://www.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf?hsLang=en) | PDF 2026-04-29 | DA20 |
| S10 | [FireAid report, App. B (GS DAF circular)](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf) | 2025-09 [X] | DA06 |
| S11 | [DCSO CY2024 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503189349302575_public.xml) | CY2024 | §2; ET001–ET003 |
| S12 | [For Good 2024 Annual Report](https://cdn.prod.website-files.com/6462856520f6ad95c7d6e2da/6a8386bfae9f58936876e2b4_For%20Good%202024%20Annual%20Report.pdf) | 2024 | §2 |
| S13 | [forgood.org](https://www.forgood.org/) / [who-we-are](https://www.forgood.org/who-we-are) | live 2026-11-15 | §2 |
| S14 | [ProPublica API: Forgood Inc / DCSO](https://projects.propublica.org/nonprofits/organizations/680480736) | 2026-11-15 | names; filing index |
| S15 | [Business Wire rebrand release](https://www.businesswire.com/news/home/20250529977479/en/Donor-Advised-Fund-Network-for-Good-Unveils-New-Name-For-Good) | 2025-05-29 [R] | §2 |
| S16 | [Pulse 2.0 on TIFIN.AI](https://pulse2.com/tifin-group-launches-tifin-ai-to-unify-enterprise-ai-workflows-in-wealth-management/) | 2026-04-20 | §3; ET011 |
| S17 | TIFIN Give / SEI / Confluence / Canterbury / AMP / AG / McDonald / Dahlinghaus releases (URLs in §3) | 2023–2026 [R] | §3 |
| S18 | [atlantajewishfoundation.org](https://atlantajewishfoundation.org/), [shalomdc.org](https://www.shalomdc.org/), [juf.org donor resources](https://www.juf.org/donor-resources/), [knightscharitable.org](https://www.knightscharitable.org/), [ccfmemphis.com](https://ccfmemphis.com/), [djcf.org](https://djcf.org/), [hjcf.org](https://hjcf.org/) | live 2026-11-15 | §4; ET004–ET009 |
| S19 | [donorportal.shalomdc.org/agentic-giving.md](https://donorportal.shalomdc.org/agentic-giving.md) | 2026-11-15 | ET010 |
| S20 | JCF 990 XML [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202500369349300210_public.xml), [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640629349300234_public.xml) | FY6/2024–25 | §4 |
| S21 | [CertSpotter giveinteractive.com](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names); dns.google lookups | 2026-11-15 | §4 |
| S22 | [Vanguard Charitable FY2026 audit](https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf); [FY2025 audit](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf) | 2026-10 / 2025-10 | §5.1 |
| S23 | [Vanguard Charitable investments page](https://www.vanguardcharitable.org/investments) | ERs as of 2026-09-30 | §5.1 |
| S24 | [NPT FY25 consolidated financials](https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf) | PDF 2026-09-01 | §5.2 |
| S25 | Foundant support snippet (portal invitations from noreply@fcsuite.com) via search; repo cf-vendor map | [R]/[X] | fcsuite.com = Foundant |

---

## Data dictionary

### `delegated-access-routes-2026.csv`

| Column | Meaning |
|---|---|
| route_id | DA01…DA21 |
| rank_fy2024, sponsor, ein | as in `sponsor-terms-census-top20-2026.csv` |
| route_name | the sponsor's own name for the role or route |
| document, document_date, source_url | the public document read (or carried) |
| who_can_be_appointed | who may be appointed, in the document's own words where possible |
| entity_appointable | Y = a firm or entity is expressly allowed; P = wording permits or does not exclude it; N = individuals only; — = no route |
| software_service_appointable | Y / P / N / unclear: whether a software service can itself be the appointee, or run under one |
| data_access, actions_permitted | what the appointee can see and do |
| credential_model | separately issued / sharing barred / not stated |
| automation_terms | bot, aggregator and scraping clauses relevant to the route |
| sponsor_approval | whether the sponsor approves the appointment |
| key_quote | ≤40 words, verbatim |
| evidence_label | F / R / X / — |
| read_status | read this batch / carried / not read, with the reason |
| retrieved | access date |
| agent_reading | [I] for AI-agent feasibility |
| notes | free text |

### `relationship-graph-edges-additions-20.csv`

Same columns as `relationship-graph-edges.csv`; IDs ET001–ET011. `status` follows repo usage (confirmed / inferred).

### `queue-proposals-batch35b.csv`

Columns per `queue-proposals-README.md`; IDs P-B35B-01 to P-B35B-03; state `open`.

## Proposals

- **P-B35B-01:** JCF NY platform. Check the FY2026 990 and watch the CT logs.
- **P-B35B-02:** DAFgiving360 and NPT pool weights through a permitted SEC/SAI route.
- **P-B35B-03:** read the public delegation forms behind Vanguard Interested Party, GS DAF agent authorization and SVCF prior approval.

## Validation corrections (wave 20, 2026-11-15) — governing
Source: [validation-wave20-report.md](validation-wave20-report.md); register `data/mission-2026-11-14/validation-register-wave20.csv`.

1. **§0, P-B34B-03 row (DCSO name).**
   - **Find:** "DCSO (EIN 99-0468956, Delaware, formed 2024) files as **\"The Resiliency Company\"**, a climate-resilience \"parent organization\" with 10 employees."
   - **Replace with:** "DCSO (EIN 99-0468956, Delaware, formed 2024) files under its legal name, Durable Capital for Sustainable Outcomes Inc, **doing business as \"The Resiliency Company\"**. It is a climate-resilience \"parent organization\" with 10 employees [V wave 20]."
2. **§2 table, Identity row.**
   - **Find:** "| Identity | EIN 99-0468956, Washington DC; formed 2024, Delaware; dba **The Resiliency Company**; website resiliency.com |"
   - **Replace with:** "| Identity | Legal name Durable Capital for Sustainable Outcomes Inc; EIN 99-0468956, Washington DC; formed 2024, Delaware; dba **The Resiliency Company** (DoingBusinessAsName on the return); website resiliency.com [V wave 20] |"
