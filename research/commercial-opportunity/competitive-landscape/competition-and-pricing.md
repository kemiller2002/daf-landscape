# Competitive landscape and pricing benchmarks for an independent DAF expert firm

**Date:** 2026-11-20. **Method:** desk research from public sources only. No logins, forms, outreach or paywall bypass. Robots-allowed endpoints only: the ProPublica Nonprofit Explorer API, the GSA CALC public API, IRS e-file XML on the public S3 data lake, and public PDFs.
**Companion file:** [`competition.csv`](../../../data/commercial-opportunity/competitors.csv), with 40 competitor rows.
**Reused repo work (cited, not redone):**
- `research/mission-2026-11-14/failed-daf-startups-deep-research.md`
- `gap19-startup-cohort.md`
- `queue-pe-lenders-labour-rates.md`
- `queue-bdc-fix-labour-benevity.md`
- `analyst-and-education-landscape.md`
- `data/mission-2026-11-14/form990-contractors-harvest-full.csv` (Form 990 Part VII-B, the five highest-paid contractors over $100k)

**Tags:**
- **[F]**: read from a filing, a price list or a primary page.
- **[R]**: a reported figure (trade press, an aggregator, a vendor blog, or a search-engine snippet of a page we could not fetch).
- **[I]**: inference by this analyst.

**Price discipline:** each figure is labelled as one of:
- **list**: a published list price;
- **award**: a public contract or award amount;
- **filed**: a 990 payment;
- **reported**: a third-party estimate;
- **inference**.

"Not public" means we searched for a price and found none.

---

## 1. Bottom line

1. **No independent firm sells DAF-specific technology assessment, sponsor operating-model review or DAF market intelligence as a named service.** [F/I]
   - Analyst coverage of DAF platforms is absent: no Gartner, Forrester, Celent or Datos category, and the last philanthropy-specific titles date from 2003 (Celent) and 2021 (Datos) (CP47, CP59).
   - Philanthropy consultancies sell strategy, fundraising or CRM implementation.
   - Wealthtech consultancies sell RIA and broker-dealer stack work.
   - DAF vendors (Ren, Foundation Source, Foundant, Blackbaud) sell their own launch and implementation services.
   - The "independent DAF tech assessor" slot is empty. §4 explains why that is not automatically an opportunity.
2. **Large sponsors do buy outside consulting, at scale, but from generalists.** [F] Form 990 Part VII-B shows:

   | Sponsor | Firm | Fiscal year | Payment | 990 description |
   |---|---|---|---|---|
   | Fidelity Charitable | McKinsey | ended 2025-06 | **$11.8M** | "PHIL. CONSULTING" |
   | Fidelity Charitable | McKinsey | ended 2024-06 | $2.88M | "phil. consulting" |
   | Vanguard Charitable | Slalom | 2021–23 | $2.1–3.4M a year | "TECH SERVICES" |
   | National Christian Foundation | Accenture | 2022 | $0.8M | consulting |
   | Silicon Valley Community Foundation | Slalom | 2023 | $1.5M | consulting |
   | Communities Foundation of Texas | EPAM | 2022 | $1.6M | technology consulting |
   | Chicago Community Trust | BCG | 2024 | $1.0M | consulting |

   Sources: CP37–CP40.
   - [I] The budget exists at the top 20 sponsors. It goes to brand-name firms and systems integrators who also implement. An independent specialist would sell *alongside* them (as buyer-side advisor, QA or second opinion) rather than replace them.
3. **Hourly-rate anchors cluster at $175–$350/h.** [F] The public anchors are:
   - **Vendor and partner list or contract rates:**
     - Foundant scoped consulting, $250/h (CP26);
     - Omatic on a public university contract (Blackbaud CRM work), $175/$195/h, rising to $250/$350/h in 2022–23 (CP27).
   - **GSA ceiling rates:**
     - "senior consultant" median $187/h (IQR $152–233);
     - "principal consultant" median $227/h (CP31).
   - **Kitces list prices** (CP09):
     - $400/h-equivalent virtual consults;
     - $1,000/h strategy calls;
     - $19.5–39.5k market scans;
     - $49.5k+ platform design.
4. **Engagement anchors for selection work are about $20k–$175k.** [F]
   - ScholarMatch's CRM-selection RFP capped the budget at $20k (CP53, snippet only).
   - A BerryDunn ERP selection for a village was a $117.7k award including a 10% contingency (CP29).
   - A BerryDunn EHR needs assessment had a not-to-exceed of $175k (CP30).
   - No public community-foundation or DAF-sponsor award amount for a technology consultant was found.
5. **Research and intelligence price points span two orders of magnitude.** [F]

   | Product | Published price |
   |---|---|
   | Chronicle of Philanthropy | $144–384 a year |
   | Giving USA | $159 a year |
   | Kitces Premier | $199 a year |
   | Inside Philanthropy | $397 a year single user; $3,797 a year unlimited |
   | Candid | $1,199–1,699 a year |
   | Cerulli single reports | **$21,500–22,000** each |
   | PitchBook | about $12–13.5k per seat (reported only) |

   Sources: CP13–CP19.
6. **Training anchors.** [F]

   | Program | Published price |
   |---|---|
   | DAFCP | $1,495 for about 30 hours, about $50 per learning hour; $1,195 for nonprofit staff |
   | CAP | $4,495 package |
   | Penn Advising for Impact | $4,750 |
   | Foundant onsite training | $2,500 per trainer-day |
   | Crescendo seminar | $495 for 12 CE hours |

   Sources: CP20–CP26.
7. **Exits in the adjacent consulting space were absorption into larger platforms or wind-downs, not independent scale-ups.** [F]
   - Heller Consulting was acquired by RKD Group (2024).
   - Arabella Advisors dissolved, and its back office moved to Sunflower Services (2025).
   - Aite and Novarica merged with RBR, and the combined firm rebranded as Datos Insights (2023).
   - CF Insights moved from FSG to Foundation Center to the Council on Foundations.
   - Carey & Co. rolled up fundraising agencies.
   - Crosslake is held by private equity and makes add-on acquisitions.

   This matches the repo's DAF-tech finding: of the documented DAF-tech exits, six of six went to consolidators (CP49).

---

## 2. Part 1: Consulting and advisory competitors

Full rows are in `competition.csv`. In the condensed view below, "DAF evidence" means public proof of DAF-specific work.

### 2.1 Philanthropy and nonprofit technology consultants

| Firm | Offering / model | DAF evidence | Main limitation vs an independent DAF specialist | Conf. |
|---|---|---|---|---|
| **Heller Consulting** (an RKD Group company since May 2024) | Nonprofit tech strategy, selection and implementation across Salesforce, Microsoft and Blackbaud; billable services | None found | Now owned by a fundraising-agency group; implementation revenue biases selection advice | High (ownership) |
| **Build Consulting** | Technology assessments, roadmaps and software selection for nonprofits, foundations and associations; pricing not public | None found | Generalist; no DAF ledger or recordkeeping depth | Medium |
| **KELL Partners** | Salesforce implementation for nonprofits and higher education; since about 2009 | None found | Single-platform integrator | Low-Medium |
| **Salesforce and IT SIs at sponsors** (Slalom, EPAM, Plative, Redpath, Xantrion, RSM) | Implementation and managed services; T&M or fixed-bid | **Yes, as 990 payees** (Vanguard Charitable, SVCF, CFT, CF Southeast Michigan, OCCF, SFF) | Build-side incentive; not independent | High (payments) |
| **Bridgespan** | Strategy consulting to nonprofits and philanthropists; a nonprofit funded by fees plus grants. FY2023: $84.8M revenue, $71.0M program-service revenue | No DAF-sponsor tech work found | Strategy only; no technology evaluation | High (financials) |
| **FSG** | Strategy and evaluation; co-founded CF Insights in 2006 and handed it off in 2015 | Historical CF benchmarking | Exited CF benchmarking; no tech work | Medium |
| **Arabella Advisors** | Philanthropy consulting plus back-office services for fiscal-sponsor funds. **Dissolved November 2025**; about 243 staff moved to Sunflower Services | Was paid by Telescope Fund (an NVF-network DAF-type sponsor) and by California and Marin CFs | Gone; politically exposed | High |
| **CCS Fundraising** | Campaign counsel and research (*Philanthropic Landscape*) | 990 payee at CFT ($762k, 2023) and SFF ($522k, 2024) | Fundraising, not operations or tech; its report repeats unscoped DAF counts (CP57) | High (payments) |
| **Marts & Lundy; Grenzebach Glier (GG+A); Campbell & Company** | Fundraising, campaign and advancement-services consulting; Campbell is a Blackbaud Connect partner | None found | Advancement-side buyers (gift offices), not sponsor operations | Low (not researched in depth) |
| **Daylight (Daylight Advisors)** | Advisor education: IPA certification, 20 weeks, price not public; Dafopedia knowledge hub; PhilanthPro partnership | DAF content (Dafopedia) | Education, not assessment; founded 2023 | Medium |

### 2.2 Community-foundation infrastructure and associations

| Entity | Offering | Notes |
|---|---|---|
| **CF Insights (Council on Foundations)** | Financial and operational benchmarking survey for CFs. Run by FSG from 2006, Foundation Center/Candid from 2015, the Council from 2023-09-01 | A benchmarking competitor for "operating-model review" at CFs, but it is survey-based and member-oriented. Price not found. |
| **Exponent Philanthropy** | Association for lean funders. 2026 dues: $870 Signature, $2,020 Signature PLUS for existing members. Tiered by assets from 2027 | A price anchor for the willingness to pay of small private foundations, not a DAF-tech competitor |
| **Tech Impact** | Free and low-cost technology assessments; publishes *Landscape of Integrated Software for Community Foundations* | The closest thing to free CF vendor-landscape content. Undercuts low-end paid assessments [I] |

### 2.3 Wealth, RIA and fintech research and consulting

| Firm | Offering and prices | DAF evidence | Limitation |
|---|---|---|---|
| **Kitces (Kitces.com)** | Membership: Premier $199 a year, groups $142–170 per member. **Kitces Consulting list prices:** $800 for 2 hours virtual, $3,000 plus travel on-site, $1,000 for a 1-hour strategy call, $19.5–39.5k market scan or sizing, $49.5k+ RIA tech-platform design, 0.25–2% advisory or board. Also lists "Managing RFP & vendor selection" and "Fractional Chief Technology Officer" (prices not shown) | The AdvisorTech map lists Foundation Source; no DAF category confirmed | The strongest brand-plus-price-list competitor for wealth-manager DAF strategy and vendor-facing research. Not DAF-deep |
| **T3 / Inside Information** (Bruckenstein, Veres) | Annual software survey; AICPA PFP members get it free; retail price not public | No charitable category in public summaries | Survey breadth, not DAF depth |
| **Ezra Group** (Iskowitz) | Wealthtech strategy, RFP and vendor selection, integration scoring; clients include LPL, Pershing, Envestnet, Orion; prices not public | None found | Would be a natural entrant if DAF demand appears [I] |
| **Cerulli** | Report series at $21,500 (*U.S. Advisor Metrics 2025*) and $22,000 (*State of U.S. Wealth Management Technology 2026*); custom research | Wealth-transfer projections only; no DAF study found | Price ceiling anchor; no DAF tech |
| **Datos Insights** (formerly Aite-Novarica plus RBR) | Subscription research and advisory; one 2021 philanthropic-advisory report; price not public | Abstract only | No ongoing DAF coverage |
| **Celent** (Oliver Wyman) | FS technology research; last philanthropy title 2003 | None current | No DAF coverage |
| **Broadridge, Fiserv** | Vendors with consulting arms | None found | Vendor-conflicted. Not researched in depth |

### 2.4 Large consultancies and technical or commercial due diligence

| Firm | DAF / philanthropy evidence | Notes |
|---|---|---|
| **McKinsey** | **Fidelity Charitable paid McKinsey $11,805,000 ("PHIL. CONSULTING") in FY ended 2025-06 and $2,880,000 the year before.** Also paid by Central Valley CF ($1.45M, 2024) and Saint Paul & Minnesota Foundation ($0.47M, 2022). [F] | [I] The scope is not disclosed. "Phil. consulting" could be strategy or operating-model work, or a donor-facing service. The figure proves budget, not scope. |
| **BCG** | Chicago Community Trust $1.0M (2024) [F] | Strategy |
| **Accenture** | National Christian Foundation $798k (2022) [F] | |
| **Deloitte / PwC / KPMG / EY / RSM** | Mostly audit and tax. Deloitte Financial Advisory $457k at SVCF (2023); RSM "technology consultant" at CF Tampa Bay ($105–159k) [F] | The audit relationship limits their independence on vendor work at audit clients [I] |
| **Crosslake** | Technical DD for PE. Falfurrias-backed since 2020; acquired Intechnica (2023) and reportedly Lucen Partners (2025) [R] | Prices not public. Tech DD for DAF-software deals would be generic code, security and architecture work without DAF domain checks [I] |
| **West Monroe; Bain / L.E.K. / Stax** | Not researched in this session beyond general knowledge | Commercial DD fees are not public (§5.2) |

### 2.5 Planned-giving firms, DAF vendors' own services, and other benchmarks

| Firm | Offering and prices | Notes |
|---|---|---|
| **PG Calc** | Software plus consulting, including a "planned giving program launch" service that selects software. Gift Annuity Manager $300 license plus $285 a year. Planned Giving Manager price not public | Adjacent to "DAF launch" advisory for charities |
| **Crescendo Interactive** | Software from $215 to $645 a year; Comprehensive seminar $495 for 12 CE hours; GiftCollege $49 a session | Low-price training anchor |
| **Sharpe Group** | Planned-giving consulting; discloses fees before engagement; amounts not public | |
| **Foundation Source** | Private-foundation and DAF administration with an in-house Philanthropic Advisory team. Supports more than 5,600 PFs and 20,000 DAF accounts (2025-12-31). DAF admin fees from 45 bp | A vendor whose advice is bundled into administration |
| **Ren** | Consulting for financial institutions on DAF, CGA and trust programs (consulting@reninc.com); serves 140+ institutions. Was paid $19.2M as administrator by Renaissance Charitable Foundation (2024) | Vendor-conflicted on build-vs-buy |
| **Blackbaud professional services** | Billed per SOW or "then current Blackbaud standard rates"; rate card not public | |
| **Foundant professional services** | **List prices:** scoped consulting $250/h; onsite training $2,500 per trainer per day; new-admin training $500–2,500; optimization $1,000–1,750. A partner program covers vendor selection and implementation; the roster is not public | The clearest DAF/CF-vendor rate card |
| **Omatic** (Blackbaud-ecosystem integrator) | VCU contract: $175/h basic, $195/h complex; renewed for 2022–23 at **$250/$350/h** | A public-sector-procured nonprofit-tech rate |
| **BerryDunn** (public-sector selection) | Awards of $117.7k (ERP selection) and $175k NTE (needs assessment) | The comparator for structured selection work |

**What an independent DAF specialist could do differently** [I]. These are the gaps the evidence shows; each is a hypothesis to test, not a demonstrated market.
- **Conflict-free buyer-side selection.** Every DAF-capable adviser found sells implementation (SIs, Foundant partners), the platform itself (Ren, Foundation Source, Blackbaud) or fundraising (CCS, RKD/Heller).
- **DAF-domain test scripts.** None of the generalists publishes them. Examples: grant-recommendation workflow, Notice 2017-73 checks, succession, DAF-to-DAF transfers, 990 Schedule D reconciliation and recipient vetting.
- **Evidence-grade market data.** The repo's 990-derived panel is independent of vendor share claims, which no analyst challenges (CP47).
- **DAF-specific technical DD modules** for PE buyers of DAF software. These would sit alongside a Crosslake-type code review, not replace it.
- **Neutral training.** DAFCP's teaching repeats aggregate payout without its denominator (repo analyst file T1).

---

## 3. Where sponsor consulting dollars go (Form 990 Part VII-B, FY2021–2025) [F]

Source: the repo harvest `form990-contractors-harvest-full.csv` (5,074 contractor rows; 494 national-sponsor and 1,778 community-foundation rows). Part VII-B lists only the five highest-paid contractors over $100k, so smaller consulting engagements are invisible.

| Sponsor (type) | Contractor | Services as filed | FY | Paid |
|---|---|---|---|---|
| Fidelity Investments Charitable Gift Fund (National) | McKinsey & Company | PHIL. CONSULTING | 2024 (ended 2025-06) | $11,805,000 |
| Fidelity Investments Charitable Gift Fund | McKinsey & Company | phil. consulting | 2023 | $2,880,000 |
| Vanguard Charitable (National) | Slalom | TECH SERVICES | 2021 / 2022 / 2023 | $2.06M / $2.41M / $3.37M |
| Vanguard Charitable | UST Global | TECH ADMIN. SERVICES | 2021–23 | $2.1–5.7M per line |
| National Christian Charitable Fdn | Accenture | CONSULTING | 2022 | $798,451 |
| GS Donor Advised Philanthropy Fund | Publicis Sapient | TECHNOLOGY SERVICES | 2023 / 2024 | $449k / $824k |
| American Endowment Foundation | PRCGEN | SOFTWARE DEVELOPMENT | 2022 | $532,562 |
| American Endowment Foundation | Tiger Hill Partners | CONSULTING | 2024 | $126,452 |
| Silicon Valley CF | Slalom | CONSULTING SERVICES | 2022 / 2023 / 2024 | $804k / $1.53M / $633k |
| Communities Foundation of Texas | EPAM Systems | TECHNOLOGY CONSULTING | 2022 / 2023 / 2024 | $1.61M / $1.26M / $388k |
| CF for Southeast Michigan | Plative | CONSULTANT | 2023 / 2024 | $1.68M / $559k |
| Chicago Community Trust | BCG / Clarity Partners | Consulting Services | 2024 | $1.00M / $1.04M |
| Orange County CF | Redpath Consulting | TECHNOLOGY CONSULTANT | 2022 | $481,100 |
| CF of Tampa Bay | RSM US | TECHNOLOGY CONSULANT [sic] | 2022 / 2023 | $106k / $159k |
| Marin CF | Arabella Advisors | CONSULTING SERVICE | 2024 | $495,000 |
| Telescope Fund | Arabella Advisors | ADMIN. OPERATIONS AND SUPPORT | 2022–24 | $268k–694k |

[I] Reading:
- A handful of sponsors account for multi-million technology and strategy budgets, roughly the top 10 nationals and the top 20 CFs by assets.
- The long tail of about 1,000+ smaller sponsors shows no consulting line above $100k.
- The repo's labour-rate work shows these sponsors' own loaded staff cost a median **$38.87/h** across all sponsors (`/home/user/daf-landscape/research/mission-2026-11-14/queue-pe-lenders-labour-rates.md` §P-COST-02), against **$57–86/h** at large nationals (DAFgiving360 $84.60–86.35/h).
- An outside specialist at $200–250/h therefore costs 3–6× the buyer's internal loaded rate. That is a normal consulting multiple, but it is a hard sell to a small CF that has no line item for it.
- The companion file `/home/user/daf-landscape/research/mission-2026-11-14/queue-bdc-fix-labour-benevity.md` §3 shows the archetype rates: CF_SMALL $41.21/h, CF_250M $53.07/h, CF_1BN $61.35/h, NAT_LARGE draw p50 $84.60/h.

---

## 4. Part 2: Failed, acquired, pivoted and exited firms, and lessons

### 4.1 Consulting and research firms (new in this file)

| Firm | Event | Date | Tag | What it signals |
|---|---|---|---|---|
| Heller Consulting | Acquired by RKD Group (fundraising agency); continues as a subsidiary | 2024-05 | [F] | Independent nonprofit-tech consultancies get absorbed into agency platforms that cross-sell |
| Arabella Advisors | Dissolved after years of political investigations. Back-office and admin services sold to Sunflower Services (a PBC funded by NVF, Windward and Hopewell); about 243 of 425 (2023) staff moved | 2025-11 | [F] | Philanthropy-services firms carry political and reputational concentration risk. Earlier (December 2024) it had acquired assets to expand "technology-driven fiscal sponsorship" |
| Aite Group, Novarica, RBR → Datos Insights | Roll-up (2021–22) and rebrand | 2023-06-21 | [F] | FS research consolidates. Philanthropy coverage (one 2021 report) did not become a practice |
| CF Insights | FSG (2006) → Foundation Center (2015) → Council on Foundations (2023-09-01) | 2015, 2023 | [F] | CF benchmarking could not sustain itself as a standalone or consulting-firm product; it migrated to member associations |
| Celent | Philanthropy title in 2003, none since | — | [F] | Analyst demand for philanthropy tech did not recur |
| Carey & Co. | Acquired Lautman Maska Neill and Schultz & Williams | 2025 | [R] | Agency roll-ups; consultancies are acquired for client books |
| Crosslake | PE-backed (Falfurrias, 2020); add-ons Intechnica (2023), Lucen Partners (2025, reported); continuation vehicle (2026, aggregator-reported) | 2020–26 | [R] | Tech DD scales through PE roll-up and generalist breadth, not vertical niches |

### 4.2 DAF-tech startups (from the repo, not redone)

- **Purposive-50** (`failed-daf-startups-deep-research.md`):
  - Six documented DAF-tech exits were all acquisitions by consolidators: Pinkaloo, Amicus.io, iPhi/Stellar, Vennfi, Giving Place and Crown/DonorFirst, bought by Ren, Foundation Source or TIFIN (P2).
  - Money was lost only where an operator held funds (P1).
  - The pattern is channel pivots from consumer to employer to bank or advisor (P3).
  - Low-take pricing could not cover CAC (P4, Low-Medium).
- **2021–26 cohort** (`gap19-startup-cohort.md`):
  - 18 entrants: 10 active, 1 acquired (Causeway → Charity Navigator), 1 pivoted (Uncommon Giving), 6 unknown, 0 shut.
  - The weak point is a **quiet fade**, not a visible failure.

### 4.3 Why apparent gaps were not opportunities [I, grounded in the cited facts]

1. **Insufficient independent demand.** Analysts have not covered DAF tech since 2003/2021 (CP12, CP59). CF benchmarking migrated to a member association (CP06). Both suggest buyers have not paid enough for neutral research to sustain it.
2. **Concentrated buyers.** The sponsors with seven-figure budgets are few and buy from McKinsey, Slalom, Accenture and EPAM (CP37–CP40). They value a firm that can implement, or a brand board members recognise, over niche independence.
3. **Vendor bundling.** Ren, Foundation Source and Foundant give away or cheaply price advice as part of administration or implementation: Foundant at $250/h, Foundation Source's in-house advisory team (CP26, CP43, CP44). This caps what small sponsors will pay a third party.
4. **Exit structure.** Consolidators buy plumbing and client books (CP49, CP03, CP46). An independent advisory firm's likely terminal value is acquisition by an agency, a vendor-neutral consultancy or a research group, which threatens its independence.
5. **Distribution and politics.** Arabella shows that philanthropy-services concentration in one political network can end a firm (CP01). A DAF firm should avoid client concentration in one ideological cluster.
6. **Regulatory timing.** No rule forces sponsors to buy assurance (Notice 2017-73 aside). Demand for operating-model and AI reviews depends on discretionary budgets, not compliance mandates. *Not directly evidenced. Inference.*

---

## 5. Part 3: Price benchmarks

### 5.1 (a) Nonprofit technology consulting and vendor selection

| Benchmark | Price | Type | Tag | Conf. | Source |
|---|---|---|---|---|---|
| Foundant scoped consulting | $250/h | list | [F] | High | CP26 |
| Foundant onsite training | $2,500 per trainer-day plus travel | list | [F] | High | CP26 |
| Foundant new-admin training | $500 (GLM/SLM) to $2,500 (CSuite full admin) | list | [F] | High | CP26 |
| Omatic at VCU (Blackbaud CRM work) | $175/h basic, $195/h complex (original); $250/h and $350/h (2022–23 renewal) | award (public contract) | [F] | High | CP27 |
| Blackbaud professional services | "then current Blackbaud standard rates", not published | not public | [F] | High | CP28 |
| BerryDunn, Downers Grove ERP selection | $117,700 including a 10% contingency (about $107k base); total project $1.3–2.4M | award | [F] | High | CP29 |
| BerryDunn, Pasadena EHR needs assessment | NTE $175,000, 1 year; 5 proposals | award | [F] | High | CP30 |
| ScholarMatch CRM evaluation and selection consultant | $20,000 ceiling (RFP, 2025) | RFP budget | [R] | Low-Medium (page 404; snippet) | CP53 |
| Small software-selection projects | "can begin at $2,000–$5,000" | reported (federal guidance page) | [R] | Low (page 403; snippet) | CP52 |
| Kitces Consulting market scan or sizing | $19,500–39,500 | list | [F] | High | CP09 |
| Kitces turnkey RIA tech-platform design | $49,500 and up | list | [F] | High | CP09 |
| Kitces virtual consult | $800 per 2 hours; $1,000 per hour for business strategy | list | [F] | High | CP09 |
| GSA CALC "senior consultant" (n=1,240) | median $187/h; IQR $152–233; p90 $306 | ceiling rates | [F] computed | Medium-High | CP31 |
| GSA CALC "management consultant" (n=1,588) | median $164/h; IQR $127–210 | ceiling rates | [F] computed | Medium-High | CP31 |
| GSA CALC "principal consultant" (n=500) | median $227/h; IQR $188–275; p90 $338 | ceiling rates | [F] computed | Medium-High | CP31 |
| GSA CALC "engagement manager" (n=105) | median $235/h | ceiling rates | [F] computed | Medium | CP31 |
| Community-foundation or DAF-sponsor award for tech consulting | **not found** | — | — | — | see §7 |

### 5.2 (b) Commercial and technical due diligence

No primary or published price was found for Crosslake, West Monroe, Bain, L.E.K. or Stax. All figures below are vendor-blog estimates.

| Benchmark | Range | Type | Tag | Conf. |
|---|---|---|---|---|
| Technical DD by a specialised tech firm | $35k–95k; $300–600/h | reported (Papermark, 2025-10, updated 2026-08; no cited basis) | [R] | Low |
| Technical DD by Big Four tech advisory | $50k–150k; $400–700/h | reported (same) | [R] | Low |
| Fixed-fee technical DD for small deals | $5k–30k over 2–4 weeks (MEV) | vendor list | [R] | Low-Medium |
| UK technical review / full TDD | from £15k / £35k plus VAT (Rocking Tech) | vendor list | [R] | Low-Medium |
| Commercial DD, desk-heavy / with an interview program | $20k–50k / $50k–150k+ | reported (vendor guide) | [R] | Low |
| Total mid-market PE diligence across workstreams | $100k–400k over 6–12 weeks; $200k–2M | reported | [R] | Low |

### 5.3 (c) Research and intelligence subscriptions

| Product | Price | Type | Tag | Conf. |
|---|---|---|---|---|
| Chronicle of Philanthropy | $144 (digital), $288 (digital plus print), $384 (premium) a year | list | [F] | High |
| Giving USA annual subscription | $159 a year | list | [F] | High |
| Kitces Premier membership | $199 a year (1 person); $170 / $160 / $142 per member for groups of 2–4 / 5–10 / 11–50 | list | [F] | High |
| Inside Philanthropy | $397 a year or $47 a month single user; team plans $1,097 (5 users) to $3,797 (unlimited) a year | list | [F] | High |
| Candid (Search / FDO tools) | Premium $1,199 a year or $219 a month; Ultimate $1,699 a year; Enterprise custom | list | [F] | High |
| Exponent Philanthropy (association) | $870 / $2,020 a year (2026, existing members) | list | [R] | Medium |
| Cerulli *U.S. Advisor Metrics 2025* | $21,500 per report | list | [F] | High |
| Cerulli *State of U.S. Wealth Management Technology 2026* | $22,000 per report | list | [F] | High |
| T3 / Inside Information Software Survey | free to AICPA PFP members; retail not public | — | [R] | Medium |
| Datos Insights, Celent | not public | — | — | — |
| PitchBook | about $12,000–13,500 a year for 1 seat; $18,000 for 2; negotiated about $7k per seat with a 5-seat minimum | reported (aggregators, Vendr-type data) | [R] | Low-Medium |

### 5.4 (d) Training and CE

| Program | Price | Hours / format | Tag |
|---|---|---|---|
| DAFCP (The American College) | $1,495; $1,195 for nonprofit staff | 30 hours, 6 modules, online and self-paced | [F] |
| CAP (The American College) | $4,495 package or $2,050 per course; nonprofit $3,695 / $1,650 | 3 courses | [F] |
| Penn Center for Social Impact, *Advising for Impact* | $4,750 (early bird $3,750 / $4,250) | 2 in-person days plus Zoom | [F] |
| Daylight IPA certification | not public; discounts via PhilanthPro and AiP | 20 weeks, online | [R] |
| Crescendo Comprehensive seminar | $495 for 12 CE hours; GiftCollege $49 a session | | [F] |
| Foundant onsite training | $2,500 per trainer-day | max 12 clients per trainer | [F] |
| Kitces courses | $297 per course; $223–267 for groups | | [F] |
| Community-foundation CAP study groups | free to participants (CF-subsidised) | | [R] |

### 5.5 (e) Fractional CTO and advisory day rates

| Benchmark | Rate | Tag | Conf. |
|---|---|---|---|
| GoFractional, fractional CTO average | about $203/h; middle half $150–250/h (fintech and nonprofit cuts have "limited data") | [R] (page 403; snippet) | Low-Medium |
| Practitioner guide (Prommer, 2026), fractional CTO day rate | $2,500–5,000/day for bounded advisory | [R] | Low |
| Kitces Consulting, ongoing advisory or board | 0.25–2% (equity or fee; basis not specified); fractional CTO offered, unpriced | [F] | High (list exists) |
| Implied day rates from §5.1 (8h × $187–250/h) | about $1,500–2,000/day | [I] | — |

### 5.6 Pricing implications for the independent DAF firm [I]

| Service | Indicative fee band | Anchors |
|---|---|---|
| DAF tech assessment and vendor selection: small CF or sponsor | $15k–40k fixed | ScholarMatch $20k cap; Kitces scan $19.5–39.5k; Foundant $250/h × 60–150h |
| DAF tech assessment and vendor selection: mid or large sponsor | $50k–150k | BerryDunn $107k selection, $175k needs assessment; GSA principal ~$227/h |
| Operating-model and AI-readiness review | $35k–120k | Same anchors. Sponsor internal loaded labour is $39–86/h, so ROI cases must show 3–6× labour leverage |
| Market-intelligence subscription | Tiered: about $400–1,500 for individuals and advisers (IP / Candid band); $5k–25k for institutions or vendors (below the Cerulli $21.5–22k single-report anchor; PitchBook-seat band) | — |
| Investor CDD/TDD DAF module | $25k–75k as a DAF-domain add-on to a generalist TDD | Reported $35–150k full TDD; Low confidence |
| Wealth-manager DAF strategy | $10k–50k projects; $800–1,000/h ad hoc | Kitces list |
| Training | $500–1,500 per seat for online certificates (DAFCP $50 per hour); $2,500–5,000/day onsite | — |

These bands are hypotheses for willingness-to-pay testing, not observed DAF prices.

---

## 6. Evidence table

Quotes are 25 words or fewer. "Snippet" means the text came from a search-engine summary of a page we could not fetch.

| ID | Claim | URL | Publisher | Date | Quote (≤25 words) | Tag | Confidence |
|---|---|---|---|---|---|---|---|
| CP01 | Arabella Advisors dissolved; about 243 staff to Sunflower; 425 employees and $60M in 2023 | https://www.philanthropy.com/news/arabella-advisors-dissolves-after-years-of-gop-led-investigations/ | Chronicle of Philanthropy | 2025-11-18 | "New Venture Fund will absorb roughly 243 Arabella staffers into Sunflower Services" | F | High |
| CP02 | Sunflower Services bought Arabella's fiscal-sponsorship servicing business; Arabella to cease operations | https://markets.financialcontent.com/theeveningleader/article/gnwcq-2025-11-17-new-entity-sunflower-services-purchasing-fiscal-sponsorship-services-business-from-arabella-advisors | GlobeNewswire (via FinancialContent) | 2025-11-17 | "Arabella Advisors will cease operations" (snippet) | R | Medium-High |
| CP03 | RKD Group acquired Heller Consulting; terms undisclosed | https://thenonprofittimes.com/npt_articles/heller-consulting-acquired-by-rkd-group/ ; https://prnewswire.com/news-releases/rkd-group-acquires-heller-consulting-to-provide-end-to-end-technology-and-strategic-solutions-302132896.html | NonProfit Times; PR Newswire | 2024-05 | "RKD Group announced the acquisition of Heller Consulting" (snippet) | F | High |
| CP04 | KELL Partners: Salesforce consultancy for nonprofits and higher education since about 2009 | https://www.crunchbase.com/organization/kell-partners | Crunchbase | n.d. | "helped over 1,300 clients implement and train" (snippet) | R | Low-Medium |
| CP05 | Build Consulting offers technology assessments and roadmaps for nonprofits and foundations | https://www.idealist.org/en/consultant/98870e56abbc44fb9313190c7580c40b-build-consulting-washington | Idealist | n.d. | "providing comprehensive technology assessments and roadmaps" (snippet) | R | Medium |
| CP06 | CF Insights: FSG and CoF 2006 → Foundation Center 2015 → CoF 2023-09-01 | https://cof.org/cf-insights/faqs ; https://cof.org/news/cf-insights-moves-candid-council-foundations | Council on Foundations | 2023 | "As of September 1, 2023, CF Insights is a service of the Council on Foundations" (snippet) | F | High |
| CP07 | Exponent dues 2026 $870 / $2,020; tiered from 2027 | https://exponentphilanthropy.org/wp-content/uploads/FAQs-2027-Dues-Restructure.pdf | Exponent Philanthropy | 2025–26 | "your 2026 dues remain unchanged: $870 for Signature members and $2,020 for Signature PLUS" (snippet) | R | Medium |
| CP08 | Ezra Group: wealthtech strategy, RFP and vendor selection, integration score; named clients | https://ezragroup.com/ | Ezra Group | n.d. | "supported banks, RIAs, broker-dealers, and WealthTech vendors through platform decisions" (snippet) | R | Medium |
| CP09 | Kitces Consulting list prices, including RFP and vendor selection and fractional CTO | https://www.kitces.com/consulting/ | Kitces.com | read 2026-11-20 | "Competitive Market Scan / Market Sizing: $19,500 - $39,500"; "Managing RFP & vendor selection" | F | High |
| CP10 | Kitces Premier membership $199 for 1 person; group rates | https://www.kitces.com/courses-groups/ | Kitces.com | read 2026-11-20 | "1 person … $199" Premier Membership; course $297 | F | High |
| CP11 | Aite-Novarica and RBR became Datos Insights | https://insurance-canada.ca/2023/06/22/aite-novarica-group-rbr-rebrand-datos-insights/ | Insurance-Canada.ca | 2023-06-22 | "Aite-Novarica Group and RBR are now Datos Insights" | F | High |
| CP12 | Celent's last philanthropy title is 2003 (repo) | https://www.celent.com/en/insights/312707366 | Celent (via repo analyst file) | 2003-03-07 | *World of Philanthropy: Entering the Mainstream?* | F | Medium-High |
| CP13 | Cerulli *U.S. Advisor Metrics 2025* list price | https://www.cerulli.com/reports/us-advisor-metrics-2025 | Cerulli Associates | read 2026-11-20 | "$21,500 … Discounts available for bulk purchase." | F | High |
| CP14 | Cerulli WM-technology report $22,000; description has no philanthropy | https://www.cerulli.com/reports/state-of-us-wealth-management-technology-2026 | Cerulli Associates | read 2026-11-20 | "$22,000" | F | High |
| CP15 | Inside Philanthropy prices | https://www.insidephilanthropy.com/membership | Inside Philanthropy | read 2026-11-20 | "Annual (Save 30%): $397 … Unlimited: $3,797" | F | High |
| CP16 | Chronicle of Philanthropy membership prices | https://www.philanthropy.com/store/memberships/individual-memberships/ | Chronicle of Philanthropy | read 2026-11-20 | "Digital: $12/month, billed annually at $144" | F | High |
| CP17 | Candid Premium and Ultimate prices | https://candid.org/pricing | Candid | read 2026-11-20 | "Starting price $1,199 billed annually … Starting price $1,699 billed annually" | F | High |
| CP18 | Giving USA subscription | https://givingusa.org/product/giving-usa-annual-subscription/ | Giving USA Foundation | read 2026-11-20 | "$159.00 / year" | F | High |
| CP19 | PitchBook seat prices (reported) | https://www.failory.com/blog/pitchbook-pricing ; https://privateequitylist.com/intelligence/pitchbook-pricing | Failory; PrivateEquityList | 2026 | "one seat at $12,000–$13,500 and two seats at $18,000" (snippet) | R | Low-Medium |
| CP20 | CAP tuition | https://www.theamericancollege.edu/designations-degrees/cap | The American College | read 2026-11-20 | "$2,050 per individual course and $4,495 for the three-course package" (snippet) | F | High |
| CP21 | DAFCP price and hours | https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp | The American College | read 2026-11-20 | "$1,495" … "$1,195 for nonprofit professionals!" … "30 Hours" | F | High |
| CP22 | Penn *Advising for Impact* tuition | https://www.impact.upenn.edu/advising-for-impact/ | Penn Center for Social Impact | read 2026-11-20 | "Tuition: $4,750 (includes breakfast and lunch during on-campus sessions)" | F | High |
| CP23 | Daylight founded 2023; aims to train 10,000 advisers; IPA price not public | https://www.wealthmanagement.com/ria-news/daylight-ceo-underscores-need-philanthropic-planning-know-how | WealthManagement.com | 2024–25 | "about 800 philanthropy advisors in the U.S." (snippet) | R | Medium |
| CP24 | Crescendo software and seminar prices | https://giftlegacy.com/store/products.html ; https://giftlegacy.com/training/comprehensive.html | Crescendo Interactive | read 2026-11-20 | CresPro $635 … Comprehensive seminar $495, 12 CE hours (snippet) | R | Medium |
| CP25 | PG Calc: GAM $300 plus $285; PGM price not public; program-launch consulting selects software | https://pgcalc.com/gift-annuity-manager ; https://pgcalc.com/consulting/planned-giving-program-launch | PG Calc | read 2026-11-20 | "select the appropriate software to support the program" (snippet) | R | Medium |
| CP26 | Foundant professional-services list prices | https://www.foundant.com/professional-services/ | Foundant Technologies | read 2026-11-20 | "Scoped Consulting Services – $250/hour"; "Onsite Training – $2,500 per Foundant team member per 8-hour day" | F | High |
| CP27 | Omatic rates under a VCU contract for Blackbaud CRM customisation | https://procurement.vcu.edu/media/procurement/contracts/8067797BA-03_CDOC.pdf | Virginia Commonwealth University | 2021–22 renewals | "Basic Rate = $250/hr … Rate for Complex engagements = $350/hr" | F | High |
| CP28 | Blackbaud PSA bills at SOW or "then current" standard rates | https://contracts.justia.com/companies/blackbaud-188/contract/981485 | Justia (Blackbaud filing) | n.d. | "pay Blackbaud in accordance with each SOW or at the then current Blackbaud standard rates" | F | High |
| CP29 | Downers Grove: BerryDunn ERP-selection award | https://agendadocs.downers.us/public/docs/agendas/2019/08-06-19/MOT_2019-8264.pdf | Village of Downers Grove | 2019-08-06 | "BerryDunn McNeil & Parker, LLC … in the amount of $117,700, which includes a 10% contingency" | F | High |
| CP30 | Pasadena: BerryDunn needs-assessment NTE | https://ww2.cityofpasadena.net/2023%20Agendas/Jun_05_23/AR%2010.pdf | City of Pasadena | 2023-06-05 | "needs assessment in an amount not to exceed $175,000 for a one-year term" | F | High |
| CP31 | GSA CALC ceiling-rate distributions (computed 2026-11-20) | https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=senior%20consultant | GSA CALC | index 2026-11-20 | Computed: senior consultant median $187/h (n=1,240) | F | Medium-High |
| CP32 | Fractional CTO average about $203/h | https://gofractional.com/insights/rates/cto | GoFractional | live page | "average at about $203/hr … middle half … between $150 and $250" (snippet) | R | Low-Medium |
| CP33 | Fractional CTO day rate $2,500–5,000 | https://prommer.net/en/tech/fractional/rates/ | Prommer (practitioner) | 2026 | "$2,500 to $5,000 for bounded advisory work and board sessions" (snippet) | R | Low |
| CP34 | Technical-DD fee table (vendor blog, no cited basis) | https://www.papermark.com/blog/due-diligence-cost | Papermark | 2025-10-27, updated 2026-08-19 | "Technical Due Diligence \| Specialized Tech Firms \| $300-$600/hour \| $35K-$95K" | R | Low |
| CP35 | Commercial-DD fee bands (vendor guide) | https://www.userintuition.ai/posts/commercial-due-diligence-cost/ | User Intuition | 2026 | "$20k–$50k … $50k–$150k+" for desk vs interview-led CDD (snippet) | R | Low |
| CP36 | Crosslake is PE-backed (Falfurrias 2020) and acquired Intechnica | https://www.newswire.com/news/crosslake-acquires-intechnica-accelerates-european-presence-21932379 ; https://www.privateequitywire.co.uk/falfurrias-capital-partners-adds-crosslake-corsis-acquisition/ | Newswire; Private Equity Wire | 2020–23 | "Crosslake Acquires Intechnica; Accelerates European Presence" | R | Medium |
| CP37 | Fidelity Charitable paid McKinsey $11.805M "PHIL. CONSULTING" (FY ended 2025-06) and $2.88M (prior FY) | https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/full ; XML https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml | IRS Form 990 via ProPublica | filed 2026 | "<PersonNm>MCKINSEY COMPANY INC</PersonNm> … <ServicesDesc>PHIL. CONSULTING</ServicesDesc> <CompensationAmt>11805000" | F | High (payment); Low (scope) |
| CP38 | Vanguard Charitable paid Slalom $3.37M (2023) and UST Global multi-million for tech services | https://projects.propublica.org/nonprofits/organizations/232888152/202511349349313096/full | Form 990 via ProPublica | FY2023 | "SLALOM LLC DBA SLALOM CONSULT … TECH SERVICES … 3374395" | F | High |
| CP39 | National Christian Foundation paid Accenture $798,451 for consulting (2022) | https://projects.propublica.org/nonprofits/organizations/581493949/202333179349303063/full | Form 990 via ProPublica | FY2022 | "ACCENTURE LLP … CONSULTING … 798451" | F | High |
| CP40 | SVCF–Slalom; CFT–EPAM; CCT–BCG and Clarity; CFSEM–Plative; OCCF–Redpath payments | e.g. https://projects.propublica.org/nonprofits/organizations/362167000/202632239349302058/full ; https://projects.propublica.org/nonprofits/organizations/750964565/202410609349301461/full | Form 990 via ProPublica | FY2022–24 | "Boston Consulting Group … Consulting Services … 1000000" | F | High |
| CP41 | Arabella paid as administrator by Telescope Fund and as consultant by Marin CF | https://projects.propublica.org/nonprofits/organizations/ (via repo harvest CSV, `filing_page_url`) | Form 990 via repo harvest | FY2022–24 | "ADMIN. OPERATIONS AND SUPPORT SERVI … 693750" | F | High |
| CP42 | Bridgespan FY2023: total revenue $84.76M, program-service revenue $70.98M, contributions $8.15M | https://projects.propublica.org/nonprofits/api/v2/organizations/311625487.json | ProPublica API (Form 990) | FY2023 | totrevenue 84763020; totprgmrevnue 70984075 | F | High |
| CP43 | Foundation Source scale and in-house advisory; DAF admin fees from 45 bp | https://foundationsource.com/wealth-advisors/ ; https://pcadafguide.foundationsource.com/how-client-fees-work | Foundation Source | 2025–26 | "admin fees … starting at 45bps and blending down based on fund balance" (snippet) | R | Medium |
| CP44 | Ren provides consulting to institutions; 140+ institutions | https://www.reninc.com/charitable-donation-services-for-financial-institutions | Ren | n.d. | "supports charitable gift portfolios for over 140 institutions" (snippet) | R | Medium |
| CP45 | Campbell & Company: Blackbaud Connect partner; employee-owned; no acquisition found | https://nonprofitpro.com/article/campbell-company-partners-with-blackbaud-404910/2 | NonProfit PRO | n.d. | "formed a strategic partnership with Blackbaud" (snippet) | R | Low-Medium |
| CP46 | Carey & Co. acquired Lautman Maska Neill (and Schultz & Williams) | https://thenonprofittimes.com/?p=216976 | NonProfit Times | 2025 | "Lautman Maska Neill Join With Carey Platform" | R | Medium |
| CP47 | No Gartner, Forrester, IDC, Celent or Datos category for DAF platforms | repo `analyst-and-education-landscape.md` §1, §3 | this repo | 2026-11-14 | "Mainstream technology analysts do not cover DAF technology." | F (repo) | Medium-High |
| CP48 | Sponsor loaded labour: median $38.87/h; large sponsors $57–86/h | repo `queue-pe-lenders-labour-rates.md` findings 9–10; `queue-bdc-fix-labour-benevity.md` §3 | this repo (Form 990 Part IX) | 2026-11-14 | "Median loaded labour cost per employee … is $38.87/h" | F/S (repo) | High |
| CP49 | Six of six documented DAF-tech exits went to Ren, Foundation Source or TIFIN | repo `failed-daf-startups-deep-research.md` §1.2, P2 | this repo | 2026-11-14 | "Six DAF-tech companies were bought by Ren, Foundation Source or TIFIN" | F (repo) | Medium-High |
| CP50 | 2021–26 cohort: 18 entrants, 0 shut, 1 acquired, 6 unknown | repo `gap19-startup-cohort.md` §1 | this repo | 2026-11-19 | "none has a documented shutdown" | F (repo) | Medium |
| CP51 | Daylight and PhilanthPro partnership; IPA discounts | https://www.newswire.ca/news-releases/daylight-and-philanthpro-launch-a-new-partnership-849723476.html | Newswire.ca | 2024-12 | "Daylight and PhilanthPro Launch a new Partnership" | R | Medium |
| CP52 | Small software-selection projects from $2k–5k | https://headstart.gov/organizational-leadership/article/working-technology-consultants | HHS / ACF Head Start | n.d. | "smaller software selection projects can begin at $2,000–$5,000" (snippet; page 403) | R | Low |
| CP53 | ScholarMatch CRM selection consultant ceiling $20,000 | https://www.scholarmatch.org/rfps/crm-evaluation-and-selection-consultant | ScholarMatch | 2025-09-18 | "ceiling of $20,000 for the project" (snippet; page 404 on fetch) | R | Low-Medium |
| CP54 | Arabella acquired assets to expand "technology-driven fiscal sponsorship" (December 2024) | https://manilatimes.net/2024/12/05/tmt-newswire/globenewswire/arabella-advisors-acquires-new-assets-to-expand-technology-driven-fiscal-sponsorship-solutions/2016318 | GlobeNewswire (via Manila Times) | 2024-12-05 | "Arabella Advisors Acquires New Assets to Expand Technology-Driven Fiscal Sponsorship Solutions" | R | Medium |
| CP55 | Tech Impact publishes a CF software landscape and offers low-cost assessments | https://techimpact.org/news/how-select-right-software-your-community-foundation | Tech Impact | n.d. | "Landscape of Integrated Software for Community Foundations" | F | Medium-High |
| CP56 | CCS (Community Counselling Service) paid by Communities Foundation of Texas ($762k, 2023) and SFF ($522k, 2024) | repo harvest CSV (`form990-contractors-harvest-full.csv`, `filing_page_url`) | Form 990 | FY2023–24 | "COMMUNITY COUNSELLING SERVICES … CONSULTING … 762208" | F | Medium-High (name match) |
| CP57 | CCS landscape report repeats "2 million DAFs" (wrong denominator) | repo `analyst-and-education-landscape.md` §1.3 | this repo | 2026-11-14 | "CCS's 2024 landscape report says '2 million DAFs'" | F (repo) | Medium |
| CP58 | McKinsey paid by Central Valley CF ($1.45M, 2024) and SPMF ($467k, 2022) | https://projects.propublica.org/nonprofits/organizations/770478025/202533219349323253/full | Form 990 via ProPublica | FY2022–24 | "McKinsey & Company Inc … Project Management … 1450000" | F | High |
| CP59 | Datos (Aite-Novarica) 2021 philanthropic-advisory report: "sector lags in fintech investment" | https://datos-insights.com/?p=13920 | Datos Insights (repo) | 2021-09 | philanthropy "really can't be left out of wealth plans anymore" | F (abstract) | Medium |
| CP60 | Ren paid $19.2M administration fee by Renaissance Charitable Foundation (2024) | repo harvest CSV, Renaissance Charitable Foundation 990 | Form 990 | FY2024 | "Renaissance Administration LLC … Administration … 19225546" | F | High |

---

## 7. Unsuccessful or partial searches

| Search | Result |
|---|---|
| Public RFP **award amounts** from community foundations or DAF sponsors for technology consultants or vendor selection | None found. The Bush Foundation, Golden LEAF, Kauffman, CDC Foundation, Calgary Homeless Foundation, CF Southern Arizona and TFEC RFPs list scope but no award (TFEC's was for CRT tax services, not tech). |
| Higher-ed advancement CRM-selection consultant awards (UT Dallas / Kennedy & Co., USM, SMU) | Engagements confirmed; no amounts found. |
| Build Consulting, Heller, KELL, Bridgespan, FSG, CCS, Marts & Lundy, GG+A, Campbell rate cards | Not public. |
| Grenzebach Glier / Marts & Lundy ownership changes | The search returned the unrelated German Grenzebach Group. Not resolved. |
| FSG restructuring 2024–25 | No results. |
| Crosslake, West Monroe, Bain, L.E.K., Stax DD fees | Not public. Only vendor-blog ranges. |
| Cerulli subscription or annual-access pricing | Not public. Only per-report list prices. |
| Datos Insights, Celent, T3 survey retail price | Not public. |
| Inside Philanthropy institutional "starting at" price | Found via the membership page (team tiers). |
| Daylight IPA tuition | Not public in fetched or indexed pages. |
| Blackbaud professional-services rate card | Not public ("then current" standard rates). |
| Ren, Foundation Source advisory fees | Not public (bundled). |
| GoFractional CTO page; Head Start consultant page; ScholarMatch RFP page | HTTP 403 / 403 / 404. Figures used only as snippets, at Low or Low-Medium confidence. |
| Guidehouse, IBM and FCI GSA price lists | Blocked or 404. Replaced by computed GSA CALC API distributions. |
| Foundant implementation-partner roster | Not public (a partner registry exists, per a job posting). |

## 8. Caveats

- **Form 990 Part VII-B.**
  - It shows only the top five contractors over $100k, so the absence of consulting at small sponsors means "not in the top five", not "zero".
  - Service descriptions are filer free text. "PHIL. CONSULTING" at Fidelity Charitable could describe donor-facing philanthropic advisory rather than sponsor operations.
- **GSA CALC.**
  - The API keyword search is fuzzy. For example, "management consultant" includes "Senior Management Consultant".
  - Rates are ceiling rates including the 0.75% IFF, and are federal-market, not nonprofit, prices.
  - The computation script is at [`scripts/commercial_gsa_rate_benchmarks.py`](../../../scripts/commercial_gsa_rate_benchmarks.py).
- **Reported prices.** All DD fee ranges and PitchBook prices come from vendor or aggregator content with no stated sample. Use them only as order-of-magnitude anchors.
