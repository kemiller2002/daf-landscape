# Sponsor prospect hypotheses: notes (2026-11-20)

Companion to `prospects-sponsors.csv` (23 rows, PS01-PS23). Each row is a **hypothesis** to test, not a qualified lead.

## Method
- **Repo first** (`/home/user/daf-landscape`, read only). Sources used:
  - Scale: `daf-sponsor-league-table-fy2025-refresh.csv`, plus `sponsor-cost-structure.csv` for FY2024 sponsors without a parsed FY2025 return.
  - Vendor payments: `form990-contractors-harvest-full.csv` and `form990-contractors-fy2025-refresh.csv` (Part VII-B: top-5 contractors over $100k only, so these are floors).
  - Portals: `cf-vendor-map-by-ein-v2.csv`.
  - Migrations: `cf-vendor-migrations-2022-2026.csv`.
  - Hiring: `daf-hiring-signals-2026.csv`.
  - Notes: queue-ren-iphi-attrition, queue-give-interactive-displacement, queue-cf-vendor-map, b4014-b4427, the Dechomai note and the breadth note.
- **Governing validation sections were applied.** Ren/Stellar to Foundant moves are dated 2025-2026. crt.sh-only evidence counts as a lead only, so Give Interactive staging dates for Minneapolis, Thrivent and JCF are labelled CT-only leads; only the DNS existence of those hosts is used.
- **Web work.** About 25 searches and about 10 page fetches, after checking robots.txt on each fetched host (none disallowed the pages used). Sources were careers pages, transition pages and press releases. No logins, forms or outreach.
- **Tags.** [F] first-party, [R] secondary or snippet, [X] repo, [I] inference, [C] computed from [X], [V] vendor statement.
- **Named people.** Only 4 rows name someone, each verified on an official page:
  - NPT CTO Eric Ziegler.
  - AEF CEO Ron Ransom.
  - GWCF COO Marcus Braxton.
  - Arkansas CF CEO Jessica Hughes Ford.
  - Other rows give roles only. Names that appeared only in snippets or third-party profiles (JCF, Des Moines, RCF) were withheld.

## Segment patterns
- **What mid-sized CFs pay DAF platform vendors.** CFs with $200m-$5bn DAF assets, TY2023-24 990 lines:
  - Ren/Stellar: about $197k-$416k a year (median about $204k; Cleveland is highest at $416k for "hosting & customizations").
  - Foundant: about $159k-$345k (Columbus is highest at $345k).
  - Blackbaud at GWCF: about $151k-$177k.
  - Give Interactive: one line, $654.5k (FFTC, TY2023).
  - Because these are top-5 floors, many CF vendor fees sit below the $100k reporting line or outside the top 5.
- **Separate outside tech consulting is common.** Typical amounts are $120k-$410k a year:
  - Root Integrated Systems (Cleveland);
  - Ideal Integrations (Columbus);
  - Atomic Data (Saint Paul);
  - Capacity Partners (GWCF);
  - Wipfli (Minneapolis, Thrivent);
  - Gant (Memphis).
  - Communities Foundation of Texas (CFT) is the outlier: EPAM $1.6m and Pegasus $0.4m. A firm offering technology assessment would compete with these firms.
- **Cost base.** For mid-sized CFs ($200m-$1bn DAF assets, n=51, FY2024):
  - median 990 IT line is about $406k;
  - median operating cost (excluding investment fees) is about $10.0m;
  - IT is about 4% of operating cost.
  - At $1-5bn (n=9), the medians are about $1.17m IT on about $27m operating cost.
- **What triggers a migration.** These patterns are inferred from the evidence:
  - **Ren/iPhi attrition among CFs.** 5 of 28 left in 2023-26, and 4 of the 5 went to Foundant.
  - **Blackbaud ledger and portal replacement.** Tampa Bay and Winston-Salem moved to Foundant. GWCF stayed in the Blackbaud/NPact family but launched a new portal and Financial Edge NXT.
  - **Donor-survey pressure for faster grant turnaround** (GWCF).
  - **Leadership change** (Arkansas has a new CEO; Saint Paul's CEO is retiring; NPT has a new CTO).
  - **Give Interactive pipeline among Ren clients** (Minneapolis, Thrivent; possibly JCF).
- **Buying window.** Most visible migrations are already complete (Columbus, Arkansas, Tampa Bay, GWCF, AEF). The open opportunities are therefore:
  - post-implementation review and optimisation;
  - independent assurance for sponsors that look mid-migration (Minneapolis, Thrivent, JCF);
  - renewal benchmarks for sponsors that pay Ren heavily (Cleveland, Memphis, Des Moines).
- **Poor fits.**
  - Vendor-captive sponsors: RCF (Ren) and Charityvest (Foundation Source).
  - App-native entrants: Daffy and Endaoment.
  - Non-cash processors: Dechomai.
  - Very large nationals with incumbent systems integrators: Vanguard, NPT and NCF. These need niche entry points.
- **Strongest mid-sized hypotheses.** These are the Medium-High and Medium rows with active signals:
  - CFT: large tech spend and CIO/data hiring.
  - Greater Horizons/GKCCF: in-house build and a hiring cluster.
  - Cleveland: high Ren spend amid peer exits.
  - Arkansas: new CEO and new platform.
  - Minneapolis and Thrivent: Ren to Give pipeline.
  - GWCF: COO-led transformation that has just gone live.

## Unsuccessful or partial searches
- **Public RFPs for DAF or grants-management software from US sponsors (2025-26).** None found; only vendor listicles and selection guides.
- **NCF.** No 2025-26 public announcement of a platform modernisation, and no specific technology job posting verified. Its careers page points to an ATS that was not crawled.
- **JCF.** No first-party portal announcement. jcfny.org is not readable by automated fetch (403 in repo work).
- **Cleveland, Des Moines, Memphis, Saint Paul, Thrivent.** No 2026 portal-transition announcements found.
- **GKCCF.** The "Software Applications Administrator" posting (repo) could not be re-read. The Director of Business Applications Paylocity link was inactive on 2026-11-20. Other GKCCF roles are snippet-only [R].
- **CFT.** The CIO posting is undated and unverified on cftexas.org.
- **Renaissance Charitable Foundation.** No 2026 leadership or program announcements; results were swamped by the unrelated "Renaissance Philanthropy".
- **Dechomai.** No technology or vendor evidence.
- **Conference talks by sponsor staff.** None searched successfully within budget.
- **Gaps in scale data.** FY2025 990s are not yet parsed for AEF, RCF, NCF, Greater Horizons, Dechomai and Daffy, so FY2024 figures are used. Endaoment's account counts are inconsistent between filings.
