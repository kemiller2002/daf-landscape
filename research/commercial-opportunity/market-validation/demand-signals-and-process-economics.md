# DAF market: demand signals and operating economics

**Prepared:** 2026-11-20. **Question:** would organisations pay for independent DAF expertise, technology assessment, operating-model redesign or software?

**Method.** Public sources only. robots.txt was checked where pages were fetched (idealist.org was checked; it allows job pages). There were no logins, forms, outreach or paywall bypass. Repo files were read before any search, and repo findings are summarised, not redone.

**Tags**

| Tag | Meaning |
|---|---|
| **[F]** | Fact from a fetched primary page, a filed 990, or a repo-verified dataset |
| **[R]** | Forum or Reddit material. A hypothesis only; no new [R] material was collected in this pass. |
| **[X]** | Search-engine extract or vendor or aggregator claim that could not be confirmed by fetching (page 403/404, or third-party listing) |
| **[I]** | Inference |

Scenario outputs taken from repo models are marked **[S]**.

Spend computations: script [`scripts/commercial_sponsor_spend_distribution.py`](../../../scripts/commercial_sponsor_spend_distribution.py) (stdlib; reads the repo CSVs, writes nothing).

---

## 0. Bottom line

1. **Direct demand is thin. Paid demand appears inside budgets.**
   - **No public RFP or RFI for DAF administration software, DAF fund-accounting software or DAF operating-model consulting from a community foundation, university or state agency in 2024–2026 was found.** That is after about 20 targeted searches (§5).
   - **Purchasing does happen, but not through public tenders:**
     - Community foundation platform migrations: at least 6 new ones in 2024–2026 beyond the repo's 8.
     - Named outside tech and consulting payees on 990s, e.g. Vanguard Charitable paid UST Global and Slalom about $8–10m a year.
     - Grant-funded capability work: AFP's Fidelity-funded DAF-expert RFP, and St. David's Foundation's AI-adoption RFP. [F/I]
2. **The buyers who visibly pay are a small set.**
   - The big nationals, mostly through affiliates or line 11a fees.
   - Roughly 40–60 community foundations of $250m or more, which have six- and seven-figure IT lines and pay named consultancies.
   - About 760 community foundations under $250m have a median IT line of $0–$166k (p75). That is below the $150–750k fixed cost of a single AI project. [F/C]
3. **Operating pain is real, but it is mostly cheap to solve, structural, or borne by recipients.**
   - Migration freezes of 3–5 weeks on grant processing are the most consistent cost evidence. [F]
   - Complaints cluster on grant delay, paper checks and processor rules. [F, repo]
   - Exceptions are about 7–8% of recipient lines and 11–12% of dollars on the core definition. [F/C, repo]
   - Per-process AI value is small except at large-national scale. [S, repo]
4. **What is commercially testable.**
   - **Strongest:** advisory and assessment sold to $250m+ community foundations and mid nationals around vendor selection and migration. This replaces work they now buy from generalist IT consultancies. The evidence is the 990 payees, the migration cadence and the Ren→Foundant/Give churn.
   - **Second:** redesign-first operating-model work. In the repo's latest calibrated runs, redesign (D) leads in 6 of 15 processes and has the highest mean rank-first probability in every cell.
   - **Weakest:** standalone AI grant-review software for sponsors.

---

## 1. Demand-signal table

The "Strength" column rates the signal as evidence that someone pays for DAF expertise, technology assessment, redesign or software. **S** = strong, **M** = medium, **W** = weak.

### 1a. RFPs and procurement (2024–2026)

| # | Signal | Organisation | Date | URL | Type | Strength | Tag |
|---|---|---|---|---|---|---|---|
| 1 | RFP for a "Donor Advised Fund Content Expert" for a curriculum, funded by the Fidelity Charitable Catalyst Fund | Association of Fundraising Professionals (AFP) Foundation | Released 2024-11-07; due 2025-01-06 | https://afpglobal.org/sites/default/files/attachments/resource/DAF_content_expert_RFP_11_7_24.pdf | RFP: DAF expertise | M (paid DAF expertise, but on the education/nonprofit side, not sponsor operations) | F |
| 2 | RFP for outsourced year-end tax compliance for 56 charitable remainder trusts (CRTs), 3-year term TY2026–28 | The Foundation for Enhancing Communities (TFEC, PA community foundation) | Issued 2026-08-17; due 2026-09-04 | https://www.tfec.org/request-for-proposal | RFP: outsourced planned-giving admin | M (a CF outsourcing back-office compliance; adjacent to DAF) | F |
| 3 | RFP for an AI adoption and integration consultant: readiness assessment, use cases, roadmap, governance, training | St. David's Foundation (TX) | Proposals due 2026-03-27; kickoff week of 2026-04-27 | https://stdavidsfoundation.org/?p=7632 | RFP: AI consulting at a grantmaker | M (a grantmaker paying for AI assessment; not a DAF sponsor) | F |
| 4 | Fidelity Charitable Catalyst Fund RFP for community foundations: 8–12 project grants up to $630k each | Fidelity Charitable Catalyst Fund | Due 2024-10-18 | https://fidelitycharitable.org/content/dam/fc-public/vessel/fidelity-charitable-catalyst-fund-RFP.pdf (fetch 404; search extract) | Funder subsidy to CFs (donor engagement, not tech) | W | X |
| 5 | Grant management system RFP | Texas A&M University (Aggie Green Fund) | Aggregator gives two date sets: posted 2025-10-03 / closed 2026-01-21, and posted 2026-01-06 / closed 2026-02-10 | https://starbridge.ai/rfp/aggie-green-fund-grant-management-system | Public procurement: grants software (not DAF) | W | X |
| 6 | Grant-management RFP for the Maine Recovery Council (opioid settlement grantmaking support) | Maine Attorney General | 2025-06-13 (from file name) | https://www1.maine.gov/ag/docs/2025.06.13%20Grant%20Management%20RFP%20Final%20Version.pdf (fetch 404) | Public outsourced grantmaking admin | W | X |
| 7 | Request for Qualifications for an organisation to hold and manage DAFs for board and staff | Bush Foundation | Undated (PDF returned 403) | https://www.bushfoundation.org/sites/default/files/Donor_Advised_Funds_RFQ_final.pdf | RFQ: DAF sponsor selection | W (date unknown) | X |
| 8 | RFP for investment consulting on a $165m endowment plus a $50m portfolio. Outside the 2024–26 window and not DAF; kept as a false positive | Cal Poly Pomona Philanthropic Foundation | Released 2023-09-15 | https://www.cpp.edu/philanthropy/about/request-for-proposal-cal-poly-pomona-philanthropic-foundation.pdf | RFP: investment consultant | n/a (out of scope) | F |

### 1b. Hiring

| # | Signal | Organisation | Date | URL | Type | Strength | Tag |
|---|---|---|---|---|---|---|---|
| 9 | Repo hiring snapshot: 168 roles at 12 employers. 27.7% mention AI; 29.1% at vendors vs 13.3% at sponsors. 0 of 11 Fidelity Charitable roles mention AI. | Sponsors and vendors | Fetched 2026-11-15 | repo: data/mission-2026-11-14/daf-hiring-signals-2026.csv | Hiring | M (AI demand is vendor-side) | F |
| 10 | Vanguard Charitable "Platform Reliability & Automation Analyst" (use-AI-tools role) | Vanguard Charitable | Snapshot 2026-11-15 | repo CSV (ADP source) | Hiring: ops automation at a sponsor | M | F |
| 11 | Greater Kansas City CF "Software Applications Administrator" | GKCCF | Snapshot 2026-11-15 | repo CSV (Paylocity) | Hiring: CF systems | W–M | F |
| 12 | Chariot "Compliance Operations" (use AI to speed compliance support); "Applied AI Engineer"; "Software Engineer, Agentic Infrastructure" | Chariot (DAF rail) | Snapshot 2026-11-15 | repo CSV (Ashby) | Hiring: vendor AI build | M | F |
| 13 | Blackbaud "AI Governance Principal" and "Agents for Good" roles | Blackbaud | Snapshot 2026-11-15 | repo CSV | Hiring: vendor AI governance | M | F |
| 14 | "Grants Processor": reviews DAF grant requests, manages the grants inbox, follows up grant checks, handles ACH enrolment; $60–65k | The Boston Foundation | Live 2026-11-20 (req. 20260902) | https://www.tbf.org/who-we-are/careers/job-listings/grants-processor-20260902 | Hiring: manual DAF grant ops | M (manual inbox/check work is a redesign target) | F |
| 15 | "Officer, Grant Operations": DAF grant processing incl. international, weekly reconciliation reports, manages grants associates; $125–138k | ImpactAssets | Removed 2026-07-23 | https://www.builtinaustin.com/job/officer-grant-operations/9929301 | Hiring: DAF ops | M | F |
| 16 | Director, IT Product Delivery (Web Portal); Senior Director, Investment Systems & Strategy; Supervisor, Grants; seasonal grants and donor-admin associates | National Philanthropic Trust | Jan 2026 (aggregators) | https://devroot.diversityjobs.com/career/1003680/Director-It-Product-Delivery-Web-Portal-Pennsylvania-Jenkintown ; https://www.snagajob.com/jobs/1261399468 | Hiring: sponsor systems + seasonal manual ops | M | X |
| 17 | Director/Sr Director of Fund Administration: about 1,100 funds and 10,000+ grants a year; snippet says the role "evaluat[es] AI solutions" to modernise grants and gifts operations | Jewish Federation Bay Area | 2026 (posting inactive) | https://recruiting.paylocity.com/Recruiting/Jobs/Details/3803096 (inactive); https://www.idealist.org/en/nonprofit-job/90c5fe48a0bc4ffba48562626af46f62-directorsr-director-of-fund-administration-jewish-federation-bay-area-san-francisco (404) | Hiring: sponsor ops modernisation with AI | M if verified | X |
| 18 | "Donor Operations Data Analyst": snippet says the role designs automation (RPA, CRM integrations) for gift and grant workflows | Foundation for the Carolinas (per search) | 2026 (posting inactive) | https://recruiting.paylocity.com/Recruiting/Jobs/Details/4079946 (inactive) | Hiring: CF ops automation | M if verified | X |
| 19 | CF database/systems admin roles: Catholic CF of Mid-Michigan (CommunitySuite admin + DAF admin); Arlington CF Gift & Grant Administrator (Foundant, deadline 2026-01-28); Triangle CF (CSuite, 2026-02-26); Jewish Communal Fund Senior Data & Reporting Analyst (deadline 2026-01-09) | Various CFs and sponsors | Dec 2025–Apr 2026 | idealist.org listings (all returned 404 on fetch) | Hiring: CF systems/data | W–M | X |

### 1c. Technology modernisation and migrations (new beyond repo CSV)

| # | Signal | Organisation | Date | URL | Type | Strength | Tag |
|---|---|---|---|---|---|---|---|
| 20 | Repo: 8 CF migration events 2023–2026, 6 of them to Foundant: Arkansas CF, Acadiana, Flint (iPhi→Foundant), Tampa Bay (RE→Foundant), Winston-Salem (Blackbaud→Foundant), Indian River, Yakima (iPhi→akoyaGO); NM is a non-event | 8 CFs | 2023-07 to 2026-07 | repo: data/mission-2026-11-14/cf-vendor-migrations-2022-2026.csv | Vendor migration | S (paid replatforming) | F |
| 21 | Donor Central → Foundation Cloud Community Portal plus Financial Edge NXT. Grant requests after Aug 14 held until the Sept 21 go-live. Not in repo CSV. | Greater Washington Community Foundation | Notice dated Jul 28; go-live 2026-09-21 (year inferred from search) | https://www.thecommunityfoundation.org/news/an-update-on-our-technology-transformation-what-fundholders-need-to-know | Migration within the Blackbaud/NPact stack | S | F |
| 22 | "Core software systems" upgrade. DAF grant recommendations cut off May 9; outage grants processed week of June 9. Not in repo CSV. | New Hampshire Charitable Foundation | Announced 2025-04-15; live 2025-05-27/28 | https://www.nhcf.org/?p=27131 | Migration | S | F |
| 23 | "New integrated software"; distributions suspended Aug 30–Sept 20; new MyGiving portal Oct 9. Not in repo CSV. | Central New York Community Foundation | 2024-08-30 to 2024-10-09 | https://cnycf.org/upcoming-software-conversion-will-lead-to-service-delays | Migration | S | F |
| 24 | FIMS (NPact, used since 1998) → Raiser's Edge NXT/Financial Edge NXT plus NPact tools. Pre-2024; context only. | CF of the Eastern Shore (MD) | 2022-08 to 2023-04 | https://www.cfes.org/transition | Migration | context | F |
| 25 | Portal transitions seen in search only: CF of New Jersey (2025 redesign), Coastal CF ("Portal Guide 2026"), Alaska CF Giving Hub, East Bay CF "Update About Your Donor Portal" (fetch 404) | Various | 2025–2026 | https://cfnj.org/helpful-guide-to-the-new-donor-portal ; https://coastalcommunityfoundation.org/app/uploads/2026/02/Portal-Guide-2026.pdf | Migration (unverified) | M | X |
| 26 | Vanguard Charitable selected Give Interactive for DAF recordkeeping (vendor release); go-live unobserved | Vanguard Charitable | 2025-11 | repo: research/mission-2026-11-14/queue-give-interactive-displacement.md; https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html | Legacy replacement at a top-3 national | S | F (repo) / X (vendor claim) |
| 27 | Give Interactive pipeline at 5 Ren/Stellar-paying sponsors ($5.86bn): WaterStone cut over 2026-11-01; ImpactAssets in dual tenancy | Multiple | 2025–2026 | repo: research/mission-2026-11-14/queue-give-interactive-displacement.md | Vendor displacement | S | F |

### 1d. Conferences and agendas

| # | Signal | Organisation | Date | URL | Type | Strength | Tag |
|---|---|---|---|---|---|---|---|
| 28 | "Plus Member Peer Connections": roundtable on CF technology systems and AI for internal processes and reporting | Council on Foundations (CF Insights) | 2026-03-03 | https://cof.org/node/19905 | Peer event: CF ops/AI | M (demand for peer learning, not paid services) | F |
| 29 | Responsible AI in Philanthropy Summit, co-hosted by TAG and Council of Michigan Foundations, hosted by Grand Rapids CF IT director; Copilot demos; akoyaGO AI use cases | TAG / CMF | 2025-05-20 | https://akoyago.com/event/responsible-ai-in-philanthropy-summit/ | Conference: AI ops | M | F |
| 30 | TAG 2024 State of Philanthropy Tech (350+ foundations): 81% some AI use, 4% organisation-wide | TAG (via CEP blog) | 2024-12-04 | https://cep.org/?p=10296 | Survey: adoption gap | M | F |
| 31 | TAG 2025 conference: recaps say AI dominated sessions | TAG | 2025 | https://blog.rockarch.org/putting-ai-in-its-place | Conference | W–M | X |
| 32 | DAF Giving Summit webinar: "2025 Research studies", moderated by DAFgiving360 | DAF Giving Summit | 2025 (undated page) | https://app.livestorm.co/dafsummit/2025-research-studies | Conference: research, not ops | W | F |
| 33 | Foundant Summit 2026 (Tampa, Apr 20–22, sold out). The client resource page shows 0 AI items; no session list found | Foundant | 2026-04 | https://www.foundant.com/resources/client-resources/col/upcoming-client-events/Summit2026 | User conference | W (demand for vendor training) | X |
| 34 | T3 2026 and Future Proof 2026: AI-led agendas (e.g., "Claude for Financial Advisors" launch); no DAF-ops session found | Advisor-tech conferences | 2026-03 | https://www.advisorpedia.com/fintech/key-insights-from-the-2026-t3-conference ; https://www.investmentnews.com/practice-management/at-future-proof-wealth-management-industry-weighs-realities-of-the-ai-revolution/268308 | Advisor channel | W (for DAF ops) | X |
| 35 | CASE Summer Institute in Advancement Services 2026 session "Donor Advised Fund Gifts" (recipient-side processing) | CASE | 2026 | https://www.case.org/conferences-training/summer-institute-advancement-services-2026/sessions/donor-advised-fund-gifts (403) | Recipient-side DAF gift processing training | W–M | X |

### 1e. Complaints and disclosed spending

| # | Signal | Organisation | Date | URL | Type | Strength | Tag |
|---|---|---|---|---|---|---|---|
| 36 | Coded complaint corpus: 244 records plus 47 added. Grant delay leads (33 of 169 complaint/mixed records since 2021). 117 records are fixable vs 47 structural; all 5 critical records are structural. | Donors, nonprofits | 2012–2026 | repo: research/mission-2026-11-14/daf-user-complaints-deep-research.md; gap19-complaints-with-denominators.md | Complaints | M | F (venues include [R]-type forums) |
| 37 | Disclosed outside tech/consulting payees at sponsors (§2.3): Vanguard Charitable (UST Global, Slalom), SVCF (Slalom), Chicago Community Trust (Clarity Partners), CF of Texas (EPAM), Marin CF (VRP), NCF (Salesforce), GS DAPF (Sapient) | Sponsors | FY2022–FY2025 | 990 XML (§2.3) | Paid tech services | S | F |

---

## 2. Spend distribution analysis

### 2.1 Method

| Item | Detail |
|---|---|
| **Part IX source** | `data/mission-2026-11-14/sponsor-cost-structure.csv`: 5,272 parsed 990s, FY2022–FY2025, full Part IX. FY2024 is used. |
| **Part IX exclusions** | Size band "z no DAF value"; subtype "Universities and Healthcare". Size band is by Schedule D DAF assets. |
| **IT** | Line 14, with zeros included in medians. This differs from `sponsor-cost-structure-and-sensitivities.md` §1.3, which uses medians among IT > 0 ($17k / $55k / $116k / $468k / $1.28m by band). |
| **Outside services** | Lines 11a, 11b, 11c, 11e and 11g (investment management, 11f, excluded). Line 11a can hold affiliated-administrator fees: Fidelity Charitable books $139.7m there and $0 IT. |
| **Contractor source** | `data/mission-2026-11-14/form990-contractors-harvest-full.csv`, Part VII-B. This lists only the **five highest-paid independent contractors above $100k**, so it is a floor on outside spend. |
| **Contractor scope** | Joined to size band by EIN and fiscal year (0 unmatched); restricted to Community Foundation and National sponsor types, FY2022–FY2024 summed. |
| **Contractor grouping** | Repo `vendor_category` regrouped: **tech** = technology_services, daf_tech_admin_vendor, daf_tech_vendor, enterprise_software, giving_platform_or_outsourced_admin, payment_processor, investment_accounting_software, grant_admin_due_diligence. **consult/admin** = consulting, philanthropic_advisory, investment_consultant, staffing, administration. |
| **Caveat** | The "consulting" category includes programme consulting (e.g., EE Ventures at Seattle Foundation); it is not all operations work. |

### 2.2 Community foundations, FY2024 Part IX (n = 796 with DAF value) [F/C]

| DAF-asset band | n | Median operating cost ex-11f | Median IT (line 14, incl. zeros) | p75 IT | Median outside services ex-11f | p75 outside services | Sum IT | Sum outside services |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| < $10m | 428 | $404k | $81 | $20k | $37k | $102k | $6.7m | $49.0m |
| $10–50m | 207 | $1.55m | $42k | $76k | $88k | $377k | $11.0m | $67.3m |
| $50–250m | 108 | $4.05m | $102k | $166k | $294k | $688k | $14.4m | $74.9m |
| $250m–1bn | 43 | $10.5m | $455k | $799k | $1.29m | $2.82m | $23.2m | $117.1m |
| $1–10bn | 10 | $28.6m | $1.28m | $1.71m | $2.60m | $3.53m | $15.9m | $44.6m |
| **Total** | 796 | | | | | | **$71.2m** | **$352.9m** |

All sponsor types except university/health, FY2024, median shares of operating cost [C]:

| Band | IT share | Outside services ex-11f share | Share of returns with IT > 0 |
|---|---:|---:|---:|
| < $10m | 0.3% | 10.4% | 51% |
| $10–50m | 1.8% | 8.4% | 69% |
| $50–250m | 2.5% | 8.6% | 79% |
| $250m–1bn | 4.2% | 10.9% | 89% |
| $1–10bn | 3.8% | 17.4% | 76% |
| > $10bn (n = 5) | 21% | 6.8% | 80% |

### 2.3 Part VII-B named contractors, FY2022–24 summed [F/C]

| Sponsor type, band | All lines | Tech | Consult/admin | Investment | Sponsors with any line | with tech line | with consult line |
|---|---:|---:|---:|---:|---:|---:|---:|
| CF < $10m | $47.6m | $0.7m | $3.2m | $2.4m | 39 | 5 | 8 |
| CF $10–50m | $96.3m | $4.2m | $14.5m | $23.1m | 74 | 6 | 23 |
| CF $50–250m | $211.7m | $4.4m | $65.7m | $61.7m | 72 | 14 | 25 |
| CF $250m–1bn | $224.6m | $16.9m | $56.9m | $88.9m | 43 | 22 | 31 |
| CF $1–10bn | $95.1m | $6.4m | $14.0m | $57.5m | 10 | 6 | 8 |
| National < $10m | $41.4m | $13.8m | $2.0m | $0.0m | 11 | 5 | 5 |
| National $10–50m | $96.2m | $43.8m | $24.9m | $1.0m | 13 | 3 | 7 |
| National $50–250m | $161.4m | $100.7m | $32.9m | $8.4m | 18 | 8 | 6 |
| National $250m–1bn | $85.7m | $65.3m | $4.4m | $6.1m | 10 | 7 | 2 |
| National $1–10bn | $628.4m | $117.2m | $0.3m | $98.6m | 9 | 8 | 1 |
| National > $10bn | $547.4m | $30.7m | $5.2m | $506.9m | 5 | 2 | 2 |

**Largest tech payees across CF and National sponsors, FY2022–24** [F]:

| Payee | Amount | Sponsors |
|---|---:|---|
| Ren (incl. Stellar/iPhi) | $105.1m | 20 |
| Benevity (AOGF administration) | $108.7m | 1 |
| TASC (Give Back Foundation) | $43.3m | 1 |
| UST Global (Vanguard Charitable) | $21.6m | 1 |
| Gloo (Servant Foundation) | $18.5m | 1 |
| Bonterra/CyberGrants | $17.7m | 3 |
| Slalom (Vanguard Charitable and SVCF) | $10.8m | 2 |
| Foundant | $1.36m | 6 (top-5 threshold hides most Foundant fees) |
| Give Interactive | $0.65m | 1 |

**Named technology and consulting payees, FY2024 unless stated** [F; 990 XML via GivingTuesday mirror]:

| Sponsor | Payee and amount | 990 XML |
|---|---|---|
| Vanguard Charitable | UST Global "tech admin services" $4.37m + $2.14m; Slalom "tech services" $3.37m | [202511349349313096](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511349349313096_public.xml) |
| Silicon Valley CF | Slalom: $0.80m (FY2022), $1.53m (FY2023), $0.63m (FY2024) | [202543149349305759](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349305759_public.xml) |
| Chicago Community Trust | Clarity Partners: $1.41m (FY2024), $1.04m (FY2025) | [202512119349301861](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202512119349301861_public.xml) |
| Communities Foundation of Texas | EPAM "technology consulting": $1.61m (FY2022), $1.26m (FY2023), $0.39m (FY2024) | [202500849349300230](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202500849349300230_public.xml) |
| Marin CF | VRP Consulting "IT service": $0.35–0.49m a year | [202541349349313719](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541349349313719_public.xml) |
| National Christian Foundation | Salesforce consulting: $1.13m (FY2023), $1.36m (FY2024) | [202513109349303201](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513109349303201_public.xml) |
| GS DAPF | Sapient: $0.45m (FY2023), $0.82m (FY2024) | [202503109349303645](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml) |

### 2.4 Reading [I]

- **Under $50m of DAF assets, there is almost no visible discretionary tech spend.** The median IT line is under $50k. Only 11 of 113 CFs under $50m with any VII-B line show a named tech payee. A typical engagement there would be under $25–50k, or bundled into vendor fees.
- **$250m–1bn community foundations are the visible buyer segment for assessment and migration work.**
  - Median IT is $455k, median outside services $1.29m.
  - 22 of 43 band members with VII-B lines name a tech payee and 31 a consultant.
  - Payees include generalist consultancies (Slalom, Clarity Partners, EPAM, VRP), not DAF specialists. An independent DAF specialist would be competing for that budget.
- **At nationals, tech spend is large but captive or affiliate-routed.** Examples: Fidelity's $139.7m on line 11a; Benevity, TASC and Gloo at affiliated or programme-specific sponsors. Independent services would sell to the CIO of a Vanguard-like sponsor, or to vendors.
- **The $150k–$750k fixed cost of one AI project** (repo assumption, [S]) is above the p75 IT line for every CF band under $250m.

---

## 3. Process economics

**Sources and governing corrections.** Inputs are from:
- `ai-economics-replacement-analysis.md`: v1, with its wave-2A corrections and the "Update from observed cost data".
- `ai-economics-v2-observed-costs.md`.
- `gap19-ai-calibration.md`.
- `g0401-g0502…`, `g0403-04…`, `g0403-01…` and `g0403-0105-04…` (the latest).
- `gap19-exception-load-proxy.md` with the V-wave 32A/40A corrections.
- `sponsor-cost-structure-and-sensitivities.md`.
- The two 2026-11-11/12 scenario notes.
- `ai-governance-failure-modes.md` (correction 17: its counts are rubric ratings, not incidents).
- `ai-native-entrant-simulation.md` (corrections 10–16: Strategy 3 is a "research probe", not a recommendation; AI may add flags but not clear them).

**How to read the scenario figures.**
- Pools are v1 base pools at 1M grants. They are **scenario** values, not observed costs.
- Winners are the latest modal winners at a large national (NAT_LARGE, CAL_CENTRAL, A_FIELD × BD_FIELD), shown for two variants:
  - "Assist": ADABDDAADDDBAAB;
  - "Route A01, m = 1.77, C_UPPER_FIELD": ADCBDDCADDDBAAB.
- **A** = improve the manual workflow; **B** = conventional automation; **C** = AI on the workflow; **D** = eliminate or redesign.
- At community foundations under $250m, "none" (no intervention clears its fixed cost) wins net in 87–100% of draws for every process [S].

**Cross-cutting observed anchors [F/C]:**

| Anchor | Value |
|---|---|
| Operating cost per grant | Fidelity Charitable $67.70; DAFgiving360 $54.59; Vanguard Charitable $134; NPT $419; GS $574 |
| v2 scenario pool per grant [S] | Large national $7.9; community foundation with $250m–1bn $180–186; CF $10–100m $323 |
| Loaded labour rate | 990 median $38.87/h (IQR $26.84–52.91); $57–73/h at $250m+ sponsors. BLS-loaded model rates: $55.45 (compliance), $34.80 (ops), $30.76 (service) |
| Posted salaries | Boston Foundation Grants Processor $60–65k; ImpactAssets Officer, Grant Operations $125–138k |
| Inference cost | $0.01–$0.60 per case. Heavy document review about $0.45, against about $83 of reviewer time |
| Calibrated AI time saving | Central 7.9% (field evidence 3–13%) |
| Sponsor AI value pool (calibrated) | Large national $445k as an assistant; $1.31m with confidence-gated routing at m = 1.77 [S]. $1bn CF $69k; $250m CF $18k |
| Exception load (top-50, FY2023–24) | Core 7.41–7.76% of lines and 10.96–11.61% of dollars; broad 24.8–25.1% / 19.7–19.9%. Four nationals: core 7.3% of lines / 10.0% of dollars. Like-for-like "existing measure": about 3.6% of dollars |

### Process table

| Process (repo ID) | Documented cost and volume evidence | What AI could do | Accuracy requirement | Error consequence | Human-review cost | Elimination vs automation |
|---|---|---|---|---|---|---|
| **Onboarding / KYC (P01)** | No public volume. Scenario: 20k accounts, 25% touched, 12 min, $55k pool [S] | Document extraction, identity and sanctions pre-screen | High for sanctions | OFAC exposure; m for P01/P14 "not pinned down" (OFAC per-alert pricing gives central about 128) [C/I] | Compliance rate $55.45/h | Modal winner A (manual fix). D = reuse custodian/adviser KYC. AI routing only if sanctions misses cannot escape |
| **Contributions: cash and securities (P02)** | No exception data. 170(f)(8)/(18) acknowledgments required. $44k pool [S] | Match transfers to funds | Medium | Misposted gift, receipt error | Ops $34.80/h | **D wins**: pre-announced transfers with structured fund reference |
| **Complex / noncash assets (P03)** | Fidelity: about 500 complex contributions a year, avg 65 days to liquidity, $2.6bn noncash in 2025 (8% of contributions) [F, repo]. Dechomai $0.5–1.0bn a year intake. Pool $532k [S] | Read appraisals, Form 8283, LP docs, title; draft due-diligence memo | High (valuation, §4943 holdings) | Mis-substantiation; donor relationship at largest gifts | 4 h per case base, compliance or counsel | One of only 2–3 processes where C (routing) is modal [S]. Judgment is the product, so keep human sign-off. **Automation (AI assist) beats elimination here** |
| **Grant recommendation intake (P05)** | Fidelity about 3.0M grants (CY2025); DAFgiving360 1.5M; NPT 159,543. DAFgiving360: 71–72% of grants "did not specify a purpose" [F]. Pool $174k [S] | Classify purpose, flag benefit language | Medium | Missed pledge or benefit leads to §4967 exposure | Ops $34.80/h; 5% touched, 6 min [S] | **D wins**: structured purpose and attestation at entry |
| **Grant approval / prohibited-benefit review (P08)** | §4966: 20% on sponsor, 5% on manager (cap $10k); §4967: 125% on donor, 10% on manager. Pool $462k [S] | Screen 100% for benefit and self-dealing signals; add flags only | Very high on clearing; moderate on flagging | Escaped error 1–10.6 handling units if detection is ≤1 in 10; 2.2–174 if always detected [C+I] | 25 min, compliance | Modal A (route) or D (assist). Governance rule: **AI may add a flag, never clear one** |
| **Charity verification, routine (P06)** | Data from IRS BMF/Pub 78/ARL monthly plus OFAC. RCF ">98%" is coverage, not an exception rate. Pool $139k [S] | Not needed: deterministic | Exact match | Taxable distribution | Minimal if continuous | **Elimination wins (P = 0.94)**: a continuous status subscription replaces per-grant lookup |
| **Charity verification, non-standard (P07)** | Exception proxy: foreign 0.63% of lines / 2.07% of dollars; PF/expenditure responsibility 0.39% / 1.39%; fiscal sponsors 0.12–0.44% / 1.30–1.94% [F/C]. RCF: about $4k typical international cost, $50k minimum. Pool $1.25M, the largest sponsor pool [S] | Equivalency-determination document reading, evidence packets | High | Taxable distribution; expenditure-responsibility failure | 90 min per case, compliance | C modal under routing (P(C clears fixed cost) 0.31–0.73 at a large national, depending on variant) [S]. **D (shared determinations across sponsors) has larger gross value but needs coordination** |
| **Compliance / AML / sanctions (P14)** | BSA applicability to standalone sponsors not established. Bank SAR penalties are $36k–$471k per missed SAR [C]. Pool $139k [S] | Alert triage | Very high | Bank-style enforcement only by analogy | 15 min | Modal A or C (m-dependent). Auto-closing alerts is ruled out where AML enforcement applies |
| **Donor / advisor communications (P11)** | No volume anchor. Fidelity site assistant is navigation-only. Complaints led by grant delay (33) and app/login (25+18) [F]. Pool $656k [S] | Agent-assist; proactive status | Medium–high (Air Canada chatbot liability; legal AI hallucinates 17–33% on benchmarks) [F] | Misstatement liability; relationship damage | 8 min, service rate $30.76/h | **D wins**: proactive grant-status visibility removes "where is my grant" contacts |
| **Tax receipts and statements (P12)** | 170(f)(8) content rules. Pool $26k [S] | Little | Exact | Donor deduction failure | Low | B (deterministic automation) |
| **Investment admin (P04)** | No public data. Pool $9k [S]. NPT hiring Senior Director, Investment Systems [X] | Rebalancing exceptions | High | Mispricing | Low | B. Keep it automated; little to sell |
| **Disbursement and reconciliation (P09/P10/P16)** | Paper checks are a cross-cutting complaint root cause; Fidelity moving to EFT-only from 2026-07-01, with conflicting status [F, repo]. Reconciliation scenario at 3M grants: $0.375m / $2.0m / $10m (low/base/high) [S]. Recipient-side scenario: 1,000 grants a year saves $667 [S]. Pools P09 $174k, P10 $348k, P16 $1.04M (sector) [S]. ImpactAssets and Boston Foundation posts show manual reconciliation and check follow-up [F] | Payment matching, remittance coding (Chariot AI agent) | Medium | Misattribution, delayed cash | Ops $34.80/h | **Elimination wins (D 0.8–0.85)**: EFT to verified payees plus structured remittance. Incidence mismatch: recipients bear the cost, sponsors control the fix |
| **Advisor integration** | No cost data. Ren DFX hosts 7+ wealth-firm programs on one sponsor/vendor pair; TIFIN Give and Chariot Disbursements serve SEI [F, repo]. T3/Future Proof 2026 agendas AI-heavy, no DAF-ops content found [X] | Advisor copilots (TIFIN Louise executes donor requests, no guardrails stated) | High (agent-originated recommendations) | Unauthorised money movement upstream of the sponsor | Unknown | Not modelled. Governance (limits on agent-originated requests) before automation [I] |
| **Data migration** | CNYCF: 3-week distribution suspension, about 6-week portal freeze (2024). NHCF: about 4-week grant hold (2025). GWCF: Aug 14–Sep 21 hold (about 5 weeks, 2026). Tampa Bay: funds page "temporarily unavailable" (2026) [F]. Repo runbook: synthetic acceptance tests only | Mapping and validation of legacy records | Exact (ledger) | Lost history; grant backlog; donor complaints | Unmeasured | Not in model. **The visible paid demand point (§2.4)**: assessment and migration planning are bought now |
| **Legacy replacement** | Ren paid $117.1m across 25 sponsors (FY2022–25). CCT paid RenPSG $1.3–1.6m a year until FY2020. FCF paid Give Interactive $654.5k for one year, then churned. Vanguard paid UST/Slalom about $8–10m a year [F] | Code/data conversion assistance | Exact | Platform failure | n/a | Repo entrant simulation: building a full platform needs about 3–4× the capital of an operating layer; S3 operating layer needs about 369k grants a year from grant review alone (about 76k with all redesign and AI value) to reach $120k a year [S] |
| **Exceptions (aggregate)** | See exception-load row in the anchors table. No sponsor publishes routing, minutes or exception rates [F] | Triage and evidence packets | Asymmetric: high on clearing | §4966/4967 | Sensitivity at 1M grants, 40% saving, $65/h: $22k (0.5%, 10 min) to $2.6M (10%, 60 min) [S] | Prevention first, then triage, then packets; AI extraction only after a blinded test |
| **Third-party dependencies** | Ren hub (34 edges); CR5 about 70% of sponsor assets; IRS BMF/Pub 78 upstream of every disclosed check [F, repo] | Vendor and data monitoring | n/a | Concentration / outage risk | n/a | Assessment service, not software [I] |
| **Auditability / Schedule D (P15)** | 573 of 574 Schedule D values match DAFRC; DAFRC imputes $3.64bn where 990s show none [F, repo]. Pool $92k [S] | Event-sourced audit trail; policy-as-code | Exact | Misreporting | Low | B/D: fix data upstream. Event-sourced decisions are an enabler, not a revenue line [I] |

**Improvement vs elimination [S/I].**
- **D (redesign) has the highest mean rank-first probability in every calibrated cell** (0.369–0.434). It is the modal winner in P02, P05, P06, P09, P10 and P11.
- **C (AI) is modal only in P03 and P07** (plus P14 at m = 1.56) under confidence-gated routing. Its value beyond the best of A, B and D is a median $84k a year at a large national (hybrid routing $249k).
- **A (manual improvement) keeps P01, P08, P13 and P14.**
- **Implication:** the economics favour selling operating-model redesign and data/payment-rail changes over AI software. The exception is document-heavy, low-volume work at the largest sponsors.

---

## 4. Evidence table

Repo items are cited by path. Quotes are 25 words or fewer.

| ID | Claim | URL or repo path | Publisher | Date | Quote | Tag | Confidence |
|---|---|---|---|---|---|---|---|
| DS01 | AFP sought a paid DAF content expert, funded by the Fidelity Charitable Catalyst Fund | https://afpglobal.org/sites/default/files/attachments/resource/DAF_content_expert_RFP_11_7_24.pdf | AFP | 2024-11-07 | "AFP is seeking a content expert to support the development of a curriculum on Donor Advised Funds (DAFS)." | F | High |
| DS02 | A PA community foundation outsourced CRT tax compliance by RFP | https://www.tfec.org/request-for-proposal | TFEC | 2026-08-17 | "assume full responsibility for year-end tax reporting and compliance" | F | High |
| DS03 | A grantmaker issued an RFP for an AI readiness/roadmap/governance consultant | https://stdavidsfoundation.org/?p=7632 | St. David's Foundation | due 2026-03-27 | "This project is a priority, and the Foundation wants to begin the engagement no later than April 2026." | F | High |
| DS04 | Catalyst Fund RFP: 8–12 CF grants up to $630k | https://fidelitycharitable.org/content/dam/fc-public/vessel/fidelity-charitable-catalyst-fund-RFP.pdf | Fidelity Charitable | 2024 (due 10-18) | (search extract) "project grants up to $630,000 each" | X | Medium |
| DS05 | Texas A&M grant management system RFP | https://starbridge.ai/rfp/aggie-green-fund-grant-management-system | Starbridge (aggregator) | 2025-10 / 2026-01 (conflicting) | "Provide Aggie green fund grant management system." | X | Low–Medium |
| DS06 | Repo hiring: 27.7% of 166 roles mention AI; vendors 29.1%, sponsors 13.3%; Fidelity Charitable 0 of 11 | repo: research/mission-2026-11-14/direction-news-hiring-signals.md | repo | 2026-11-15 | "No sponsor posting names AI for grant review, eligibility or due diligence." | F | Medium (small sponsor n) |
| DS07 | Boston Foundation hires a manual DAF grants processor at $60–65k | https://www.tbf.org/who-we-are/careers/job-listings/grants-processor-20260902 | The Boston Foundation | live 2026-11-20 | "Manage the grants inbox daily to ensure all incoming emails are reviewed, responded to, and followed up on as needed;" | F | High |
| DS08 | ImpactAssets grant-ops officer at $125–138k with reconciliation duties | https://www.builtinaustin.com/job/officer-grant-operations/9929301 | Built In | removed 2026-07-23 | "Run all reports needed to support weekly grant posting and reconciliation" | F | High |
| DS09 | NPT hiring web-portal IT and investment-systems leaders | https://devroot.diversityjobs.com/career/1003680/Director-It-Product-Delivery-Web-Portal-Pennsylvania-Jenkintown | DiversityJobs (aggregator) | 2026-01 | n/a | X | Medium |
| DS10 | Jewish Federation Bay Area fund-admin director to evaluate AI for grants and gifts operations (about 10,000+ grants a year) | https://recruiting.paylocity.com/Recruiting/Jobs/Details/3803096 | Paylocity (inactive) | 2026 | n/a (search extract only) | X | Low |
| DS11 | FFTC analyst to design RPA/CRM automation for gift and grant workflows | https://recruiting.paylocity.com/Recruiting/Jobs/Details/4079946 | Paylocity (inactive) | 2026 | n/a (search extract only) | X | Low |
| DS12 | Repo: 8 CF migration events 2023–2026, mostly to Foundant | repo: data/mission-2026-11-14/cf-vendor-migrations-2022-2026.csv | repo | 2026-11-14 | n/a | F | High |
| DS13 | GWCF moved to Foundation Cloud plus Financial Edge NXT; grant processing paused | https://www.thecommunityfoundation.org/news/an-update-on-our-technology-transformation-what-fundholders-need-to-know | Greater Washington CF | Jul 28 (2026 inferred) | "We will resume processing any grants or payments submitted after August 14." | F | Medium (year inferred) |
| DS14 | NHCF core-software upgrade held DAF grant recommendations about 4 weeks | https://www.nhcf.org/?p=27131 | NH Charitable Foundation | 2025-04-15 | (dates only; grants submitted during outage processed week of June 9) | F | High |
| DS15 | CNYCF software conversion suspended distributions about 3 weeks | https://cnycf.org/upcoming-software-conversion-will-lead-to-service-delays | Central NY CF | 2024-10-08/09 | "Our software conversion is complete and the new MyGiving portal for fundholders is now active." | F | High |
| DS16 | CFES replaced FIMS (used since 1998) with Blackbaud NXT plus NPact | https://www.cfes.org/transition | CF of the Eastern Shore | 2023-04-24 | "there will be a period of transition." | F | High (pre-window) |
| DS17 | Vanguard Charitable selected Give Interactive for recordkeeping; go-live unobserved | repo: research/mission-2026-11-14/queue-give-interactive-displacement.md | repo / Give release | 2025-11 | n/a | F/X | Medium |
| DS18 | Give Interactive at 5 Ren-paying sponsors ($5.86bn); WaterStone cut over 2026-11-01 | repo: research/mission-2026-11-14/queue-give-interactive-displacement.md | repo | 2026-11-19 | "The pattern is 'pipeline overlap', not yet 'systematic displacement'." | F | High |
| DS19 | CoF peer roundtable on CF tech systems and AI | https://cof.org/node/19905 | Council on Foundations | 2026-03-03 | "Technology systems play a critical role in supporting community foundation operations." | F | High |
| DS20 | TAG/CMF Responsible AI in Philanthropy Summit, hosted by a CF IT director | https://akoyago.com/event/responsible-ai-in-philanthropy-summit/ | akoyaGO | 2025-05-20 | "how can we as a sector navigate AI ethically, with leading-edge security and technology practices" | F | High |
| DS21 | TAG survey: 81% of foundations use some AI; 4% organisation-wide | https://cep.org/?p=10296 | CEP (TAG CEO) | 2024-12-04 | "81 percent of foundations report some degree of AI usage" | F | High |
| DS22 | DAF Giving Summit research webinar moderated by DAFgiving360 | https://app.livestorm.co/dafsummit/2025-research-studies | DAF Giving Summit | 2025 | "provides a timely look at current research supporting the donor-advised fund (DAF) sector." | F | Medium |
| DS23 | Complaint corpus: grant delay leads; 117 fixable vs 47 structural | repo: research/mission-2026-11-14/gap19-complaints-with-denominators.md; daf-user-complaints-deep-research.md | repo | 2026-11-19 | n/a | F (venues partly forum-type, [R]) | Medium |
| DS24 | 13 of the top-15 sponsors have no public review-venue surface; processors draw most complaints | repo: research/mission-2026-11-14/gap19-complaints-with-denominators.md | repo | 2026-11-19 | n/a | F | High |
| DS25 | CF median IT (incl. zeros) $81 / $42k / $102k / $455k / $1.28m by band, FY2024 | repo: data/mission-2026-11-14/sponsor-cost-structure.csv (computed here) | IRS 990 via repo | FY2024 | n/a | F/C | High |
| DS26 | Vanguard Charitable paid UST Global and Slalom about $9.9m in FY2024 for tech services | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511349349313096_public.xml | IRS 990 | FY2024 | "TECH ADMIN. SERVICES" | F | High |
| DS27 | SVCF paid Slalom $0.6–1.5m a year, FY2022–24 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349305759_public.xml | IRS 990 | FY2024 | "CONSULTING SERVICES" | F | High |
| DS28 | Chicago Community Trust paid Clarity Partners $1.41m (FY2024) and $1.04m (FY2025) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202512119349301861_public.xml | IRS 990 | FY2024 | "Consulting Services" | F | High (service scope not stated) |
| DS29 | CF of Texas paid EPAM for technology consulting, $0.39–1.61m a year | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202500849349300230_public.xml | IRS 990 | FY2022–24 | "TECHNOLOGY CONSULTING" | F | High |
| DS30 | NCF paid Salesforce $1.13–1.36m for consulting | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513109349303201_public.xml | IRS 990 | FY2023–24 | "CONSULTING" | F | High |
| DS31 | Ren entities paid $117.1m across 25 sponsors (FY2022–25) | repo: research/mission-2026-11-14/vendor-footprint-990-harvest.md | repo | 2026-11-14 | n/a | F | High |
| DS32 | Operating cost per grant: Fidelity $68, DAFgiving360 $55, Vanguard $134, NPT $419 | repo: research/mission-2026-11-14/sponsor-cost-structure-and-sensitivities.md | repo | 2026-11-14 | n/a | F/C | Medium (period mismatch 0–18 months) |
| DS33 | The AI fixed-cost hurdle exceeds CF IT budgets below about $250m | repo: research/mission-2026-11-14/ai-economics-replacement-analysis.md (governing update) | repo | 2026-11-14 | "prohibitive below about $250m of DAF assets" | S/C | Medium |
| DS34 | Calibrated AI time saving 7.9% central; sponsor AI pool $445k at a large national | repo: research/mission-2026-11-14/gap19-ai-calibration.md | repo | 2026-11-19 | n/a | S | Medium |
| DS35 | Routing raises the pool to about $1.31m; after the realisation haircut C is modal in 2–3 processes; D highest in every cell | repo: research/mission-2026-11-14/g0403-0105-04-routing-realization-and-correlation.md | repo | 2026-11-20 | n/a | S | Medium |
| DS36 | At CFs under $250m, "none" wins net in 87–100% of draws | repo: research/mission-2026-11-14/ai-economics-v2-observed-costs.md | repo | 2026-11-14 | n/a | S | Medium |
| DS37 | Core exception proxy 7.76% of lines / 11.61% of dollars (refined) | repo: research/mission-2026-11-14/gap19-exception-load-proxy.md; g0503-0501-exception-proxy-refinements.md | repo | 2026-11-19/20 | n/a | F/C | Medium (upper-leaning screen) |
| DS38 | No published per-grant exception rates, minutes or costs; RCF 98% is not an exception rate | repo: research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md | repo | 2026-11-12 | "We do not have credible published per-grant exception frequencies, reviewer minutes, blended labor cost, appeal rates or error costs." | F | High |
| DS39 | Recipient-side reconciliation: $667 a year saving at 1,000 grants; incidence mismatch | repo: research/daf-reconciliation-economics-scenario-model-2026-11-11.md | repo | 2026-11-11 | "Recipient may bear cost while sponsor or processor controls data needed to solve it." | S/I | Medium |
| DS40 | Escaped-error cost under §4966/4967 is 1–10.6 handling units at low detection | repo: research/mission-2026-11-14/g0403-04-escaped-error-cost.md | repo | 2026-11-19 | n/a | C/I | Medium |
| DS41 | Governance: AI may add a flag, never clear one; counts are rubric ratings, not incidents | repo: research/mission-2026-11-14/ai-governance-failure-modes.md (correction 17) | repo | 2026-11-14 | "These counts are rubric ratings against unconstrained AI, with no observed DAF AI incidents" | I | High |
| DS42 | Entrant S3 is a research probe; needs about 369k grants a year from review alone for $120k a year | repo: research/mission-2026-11-14/ai-native-entrant-simulation.md (correction 10) | repo | 2026-11-14 | "Preferred research probe: Strategy 3, conditional on measuring operating cost pools." | S | Medium |
| DS43 | Fidelity: about 500 complex contributions a year, 65 days to liquidity, $2.6bn noncash in 2025 | repo: research/mission-2026-11-14/direction-noncash-gift-infrastructure.md | repo (Fidelity sources) | 2026-11-15 | n/a | F | High |
| DS44 | 990 loaded labour rate median $38.87/h; $57–73/h at $250m+ sponsors | repo: research/mission-2026-11-14/ai-economics-v2-observed-costs.md (labour-rate check) | repo | 2026-11-14 | n/a | C | Medium |
| DS45 | Foundation for the Carolinas paid Give Interactive $654.5k (CY2023), then churned | repo: research/mission-2026-11-14/queue-give-interactive-displacement.md | repo | 2026-11-19 | n/a | F | High |

---

## 5. Unsuccessful searches and dead ends

- **DAF administration and software RFPs.**
  - "RFP donor advised fund administration 2025/2026", "community foundation request for proposals fund accounting software", "community foundation RFP grants management system / donor portal 2026", and "state request for proposals donor advised fund": **no qualifying 2024–26 notice.** Results were vendor marketing (Foundant, Fluxx, Tech Impact guides) or out-of-window or out-of-scope RFPs (TAF Canada 2020; Cal Poly Pomona 2023 investment consultant).
  - Jewish federation / foundation RFP for DAF software or an investment consultant: none; only programme-grant RFPs.
- **Public portals.**
  - BidNet: opioid-settlement grant-administration solicitation 443441238166 returned 403.
  - Delaware County PA opioid data-system RFP: 404.
  - Maine AG grant-management RFP PDF: 404 under both encodings.
  - Periscope/OpenGov were not queried directly (portal search requires interactive sessions); only search-engine extracts were used.
- **Unreadable or missing pages.**
  - Bush Foundation DAF RFQ PDF: 403.
  - Fidelity Catalyst Fund RFP PDF: 404.
  - CASE "Donor Advised Fund Gifts" session: 403.
  - Community Foundation for Southern Arizona IT RFP: 404.
  - East Bay CF portal notice: 404.
  - Idealist job pages (Arlington CF, Catholic CF Mid-Michigan, California CF, Jewish Federation Bay Area): 404, expired.
  - Paylocity postings 3803096 and 4079946: inactive.
- **Conference agendas.**
  - No session list found for the CoF Fall Conference for Community Foundations 2025/2026, the NAGP/CGP national conference 2025, Foundant Community Conference 2025/2026 (Summit 2026 sold out; no agenda), bbcon 2026 (catalog page returned only a title), TAG 2025 (recaps only), Ren events, or Fidelity/Schwab advisor conferences.
  - No DAF-operations session was found at T3 2026 or Future Proof 2026.
  - The Kitces-listed Donor-Advised Fund Forum (American College, Mar 9–10, Fort Worth) has no session list.
- **Hiring gaps not filled.** Schwab/DAFgiving360 (robots disallow, per repo), NPT official careers page (aggregators only), Endaoment, Every.org.
- **Paid-service price evidence.** No public price for DAF operating-model consulting, technology assessment or migration services was found. Only 990 aggregate payments to generalist consultancies (§2.3) and vendor fees were found.
