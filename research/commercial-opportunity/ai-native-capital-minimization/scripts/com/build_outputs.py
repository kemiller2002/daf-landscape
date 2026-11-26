"""COM: opportunities.csv, replication.csv, evidence.jsonl, assumptions.jsonl, report.jsonl.
Run after sponsor_value.py: python3 -I -B build_outputs.py <outdir>"""
import csv
import json
import sys

import pandas as pd

OUT = sys.argv[1]
ACC = "2026-11-25"
DL = "/home/user/daf-landscape"
SE = f"{DL}/data/commercial-opportunity/servicing-economics"
MS = f"{DL}/data/mission-2026-11-14"

# ------------------------------------------------------------------ evidence
EV = [
    ("MS GIFT paid RenPSG for admin & legal, CY2024", "14930249", "USD/yr", f"{SE}/price-observations.csv (PRC-O-001)", "IRS 990 Part VII-B", "CY2024", "A", "18.46 bps of avg DAF assets; $737/avg account; sponsor 0 employees"),
    ("MS GIFT donors pay MSSB a separate admin/platform fee", "7", "bps", f"{SE}/price-observations.csv (PRC-O-004/005)", "donor circular", "2024-08-22", "A", "plus up to 3 bps sponsor GOE; MSSB advisory up to 1.00% on same assets; Ren's 18.5 bps excludes channel relationship work"),
    ("Ren realised take at U.S. Charitable Gift Trust", "40.1", "bps avg assets", f"{SE}/price-observations.csv (PRC-O-008)", "IRS 990", "CY2024", "A", "$429/account at $107k avg balance: per-account price is not stable either"),
    ("Ren + Stifel Trust + Advent full admin stack at Stifel Charitable", "1142", "USD/account-yr", f"{SE}/price-observations.csv (PRC-O-014)", "IRS 990", "CY2025", "A", "29.5 bps; above MS GIFT per account"),
    ("CAF America grant administration only for GS Charitable Gift Fund", "1198", "USD/account-yr", f"{SE}/price-observations.csv (PRC-O-022)", "IRS 990", "FY2025", "B", "$875,665; grant due diligence only; 15.2 bps"),
    ("TIFIN Give ADV list service fee billed to sponsor", "30 (<=$1M accts); 10-20 (>$1M)", "bps", "https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=1057059", "SEC Form ADV 2A", "2026-09-04", "A", "also SaaS one-time implementation fee + subscription, amounts undisclosed (repo EV-PRC-015)"),
    ("Fidelity Charitable internal DAF admin fee (paid on to FMR)", "139686600", "USD/yr", f"{MS}/sponsor-fee-revenue-margin-2026-11-19.csv", "audited FS", "FY2024", "A", "22.9 bps of avg DAF value vs 60 bps headline at $337k mean balance: realisation ~0.38"),
    ("RCF internal DAF fee revenue", "19617095", "USD/yr", f"{MS}/sponsor-fee-revenue-margin-2026-11-19.csv", "audited FS", "FY2024", "A", "38.7 bps vs schedule ~61 bps at $196k: realisation ~0.63; 98% paid to Ren"),
    ("Jewish Communal Fund internal fee and opex", "11789740 fee / 7944558 opex", "USD/yr", f"{MS}/sponsor-fee-revenue-margin-2026-11-19.csv", "audited FS", "FY2024", "A", "42.2 bps fee; fee less opex $3.85M"),
    ("Combined Jewish Philanthropies internal DAF fee", "1642000", "USD/yr", f"{MS}/sponsor-fee-revenue-margin-2026-11-19.csv", "audited FS", "FY2024", "A", "8.7 bps: some sponsors subsidise DAFs; little fee revenue to share"),
    ("NCF internal fees (eliminated interfund)", "47411000", "USD/yr", f"{MS}/sponsor-fee-revenue-margin-2026-11-19.csv", "audited FS", "FY2024", "B", "88.8 bps incl. all fund types; opex $124.2M"),
    ("CF published DAF admin schedules (top CFs)", "50-150 at $100k; 40-85 at $10M", "bps", f"{MS}/cf-daf-fee-census-2026.csv", "sponsor fee pages", "2026-11-15", "A", "e.g. Chicago CT 60/60/40.5; FFTC 85/85/48; GKCCF 100/80; NYCT 50"),
    ("Conventional servicer cost per account by archetype (labour + external, incremental)", "217 typical; 262 market mix; 467 high value", "USD/account-yr", f"{SE}/capacity-model.csv", "model [D from A]", "2026-11-25", "D", "no time study exists; parameters are assumptions"),
    ("AI-native redesigned servicer cost per account, market mix", "88.78", "USD/account-yr", f"{SE}/capacity-model.csv", "model [D from A]", "2026-11-25", "D", "51 min/acct-yr vs 260 conventional"),
    ("Sponsor loaded labour rates by archetype", "CF_SMALL 41.21; CF_250M 53.07; CF_1BN 61.35; NAT_LARGE 84.60", "USD/h", f"{DL}/research/commercial-opportunity/competitive-landscape/competition-and-pricing.md:205", "repo derived", "2026-11", "C", ""),
    ("Ren/Stellar software-only lines at small clients", "118000-175000", "USD/yr", f"{DL}/research/commercial-opportunity/servicing-economics/01-pricing-and-scope.md (d)", "IRS 990", "2022-2025", "A", "apparent platform floor"),
    ("Sponsor consulting/tech spend lines (Part VII-B)", "McKinsey $11.8M (Fidelity FY2025); Slalom $2.1-3.7M/yr (Vanguard); EPAM $1.6M (CFT 2022); PRCGEN $532,562 software development (AEF 2022)", "USD/yr", f"{DL}/research/commercial-opportunity/competitive-landscape/competition-and-pricing.md:183-198", "IRS 990", "2021-2025", "A", "demonstrates sponsor-funded development/consulting budgets; scope undisclosed"),
    ("CF vendor migration events 2022-2026 in repo ledger", "8", "events", f"{MS}/cf-vendor-migrations-2022-2026.csv", "sponsor sites, 990", "2023-2026", "A", "6 of 8 to Foundant CommunitySuite; 4 left Ren iPhi"),
    ("iPhi lost sponsors 2023-26", "6 of 57", "sponsors", f"{DL}/research/commercial-opportunity/service-offerings/offerings.md (OF1, INV035)", "repo", "2023-2026", "B", ""),
    ("Ren technology lineage by acquisition", "Blackbaud DAF tech 2011; DonorFirst 2016; Pinkaloo 2021; Stellar/iPhi 2023", "events", f"{DL}/research/historical-daf-sponsor-technology-lifecycle-2011-2026.md", "press/vendor", "2011-2023", "A", "no observed merging of all acquired ledgers into one architecture"),
    ("iPhi MSA exit terms", "content available in industry-standard format for 15 days; annual auto-renewal; 12-month fee liability cap", "terms", "https://www.reninc.com/wp-content/uploads/2023/07/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20.pdf", "vendor template MSA", "2023-06-20", "B", "template, not executed contract (repo ren-iphi-platform-contract-architecture-integration-audit)"),
    ("Ren RAC MSA termination and renewal", "1-year auto-renewal, 60-day notice; fees through end of termination quarter", "terms", "https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf", "vendor template MSA", "2025-08", "B", ""),
    ("Ren paid add-ons", "SSO, data migration onto DFX, API integration, branding", "list", "https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf", "vendor product description", "2025-08", "B", "implementation and integration are separately priced (amounts undisclosed)"),
    ("AEF post-migration self-service history", "2", "years", "https://engage.aefonline.org/dc-sunset/", "sponsor notice", "2026-10", "A", "older history by staff request; portability is a real buyer issue"),
    ("RCF fee share paid to Ren", "95% (2020-22); 98% (2023-24)", "share", "https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf", "audited FS", "FY2024", "A", "revenue-share precedent (related party)"),
    ("Candid API pricing", "2750-9900", "USD (period unstated)", "https://candid.org/explore-apis/", "vendor page snippet", "2026-11-15", "C", "repo CDP-027; conflicting secondary $2,750-50,000/month"),
    ("Chariot DAFpay processing fee", "2.9", "% of DAF payment", "https://www.givelively.org/resources/daf-donations-on-giving-basket", "partner page", "2026", "A", "repo CDP-013"),
    ("Chariot Donor Accounts API in beta with unnamed design partners", "handful", "partners", "https://docs.givechariot.com/changelog/2026/5/8", "vendor changelog", "2026-05-08", "A", "no design-partner fees disclosed"),
    ("Processing vendors paid by flow-heavy sponsors", "Benevity $45.97-54.45M (AOGF); CyberGrants $5.41-8.29M (CAF America)", "USD/yr", f"{SE}/price-observations.csv / 01-pricing-and-scope.md (a)", "IRS 990", "FY2024-25", "A", "~2.4% / ~0.7% of grants"),
    ("Foundant professional services list prices", "$250/h consulting; $2,500/trainer-day", "USD", f"{DL}/research/commercial-opportunity/competitive-landscape/competition-and-pricing.md:164", "vendor list", "2026", "A", ""),
    ("Foundant offers no-cost proof-of-concept migration before contract", "0", "USD", "https://communityfoundations.foundant.com/?p=246", "vendor page (search snippet)", "accessed 2026-11-25", "C", "suggests vendors absorb pre-sale migration cost; not read in full"),
    ("Blackbaud FY2025: one-time services revenue immaterial; combined into revenue", "immaterial", "share of revenue", "https://www.sec.gov/Archives/edgar/data/1280058/000128005826000006/blkb-20251231.htm", "SEC 10-K (search snippet)", "FY2025", "C", "Q-level recurring revenue 98.1% of total per release snippet; implementation is not a large revenue pool for a scaled vendor"),
    ("USBFS fund administration contract minimum", "60000 + CPI", "USD/yr", "https://www.sec.gov/Archives/edgar/data/1719606/000121390019004827/f10k2018ex10-2_pharoscap.htm", "SEC exhibit", "2018-03-01", "A", "minimum-annual-fee precedent (repo PRC-O-057)"),
    ("NC ABLE term sheet state administration fee", "5", "USD/account", "https://www.nctreasurer.gov/documents/files/ncable/national-able-contract-term-sheet/download", "state term sheet (search snippet)", "2017", "C", "public-procurement per-account fee precedent; not read in full"),
    ("Unbound EV-02: advantage over AI-enhanced incumbents rests on unmeasured redesign levers; several are policies incumbents can adopt", "C0~B: E1 $301 vs $313", "USD/fund", "/home/user/unbound/requirements/convergence/2026-11-24-master/05-ECONOMIC-VALIDATION.md:54", "repo model", "2026-11-24", "D", ""),
    ("Unbound EV-04: CF entry hypothesis not supported; CF software already serves all fund types", "C $6,671 vs AL $6,361 at 128 funds", "USD", "/home/user/unbound/requirements/convergence/2026-11-24-master/05-ECONOMIC-VALIDATION.md:56", "repo model", "2026-11-24", "D", ""),
    ("Unbound public-data replay: safety 600/600; sanctions 88/100 caught", "88/100", "count", "/home/user/unbound/requirements/convergence/2026-11-24-master/14-PUBLIC-DATA-REPLAY.md", "repo measurement (not re-run)", "2026-11-24", "B", "verification is not a solved commodity at 100%"),
    ("Echelon AI coding agents capability", "described-not-verified", "status", f"{SE}/echelon-capabilities.csv (ECH-02)", "repo", "2026-11-25", "A", "no agent capability trial or independent replication"),
    ("Echelon components licence", "PolyForm Noncommercial 1.0.0", "licence", f"{SE}/echelon-capabilities.csv (ECH-20)", "repo", "2026-11-25", "A", "commercial licence absent: launch blocker"),
    ("DAF grants to church-coded recipients absent from Pub 78 (top-50 sponsors)", "2.17", "USD bn", f"{MS}/charity-data-provider-integrations-2026.csv (CDP-055)", "repo derived", "2026-11-15", "C", "eligibility data commodity has gaps"),
    ("Reconciliation standalone product caution", "base-case $667/yr labour saving at 1,000 grants (recipient side)", "USD/yr", f"{DL}/research/daf-reconciliation-economics-scenario-model-2026-11-11.md:33,56", "repo model", "2026-11-11", "D", ""),
    ("Sponsor-own DAF opex vs servicer cost gap", "median ~$3.8k/account CFs", "USD/account", f"{DL}/research/commercial-opportunity/servicing-economics/02-sponsor-market-analysis.md:94", "repo derived", "2026-11-25", "C", "sponsors carry much work a servicer would not replace"),
    ("Ren customer concentration", "85.8% of named 990 receipts from three customers", "share", f"{DL}/research/commercial-opportunity/service-offerings/offerings.md (OF4, INV056)", "repo derived", "2024", "B", "defending top accounts dominates incumbent response"),
    ("GivingTech DAFtech advertises technology licence or full-service revenue share", "advertised", "model", "https://givingtech.org/daf-institutions", "vendor page", "2026", "B", "deployments unverified"),
    ("Vanguard Charitable tech services spend (Slalom; UST Global)", "Slalom $2.06-3.74M/yr; UST $2.1-5.7M per line", "USD/yr", f"{DL}/research/commercial-opportunity/competitive-landscape/competition-and-pricing.md:185-186", "IRS 990", "2021-2024", "A", "large incumbents can and do fund transformation"),
]
evidence = [dict(evidence_id=f"EV-COM-{i+1:03d}", claim=c, value=v, unit=u, source_url_or_path=s, source_type=t, filing_period=fp,
                 accessed=ACC, quality=q, notes=n) for i, (c, v, u, s, t, fp, q, n) in enumerate(EV)]
with open(f"{OUT}/evidence.jsonl", "w") as f:
    for e in evidence:
        f.write(json.dumps(e) + "\n")

# ------------------------------------------------------------------ assumptions
AS = [
    ("Replaceable (equivalent-scope) share of DAF-allocated opex excl. advertising/professional fundraising", "CF 0.30; faith 0.45; independent national 0.55; affiliate in-house 0.60; other 0.45", "share", "CF 0.15; nat 0.40", "CF 0.45; nat 0.70",
     "Retained by sponsor: board/legal control, reserved decisions, development, philanthropic advising, community grantmaking, investment oversight, non-DAF funds. MS GIFT vendor/opex = 0.81 bounds the outsourced case", "EV-COM-001;EV-COM-041", "High: drives value_high; base value is bounded by bottom-up instead"),
    ("Realisation factor: realised donor-fee bps / schedule bps at mean balance", "0.60", "ratio", "0.40", "0.75", "Calibrated on Fidelity 0.38, RCF 0.63, MS GIFT TPA 0.68", "EV-COM-007;EV-COM-008;EV-COM-001", "Medium: changes sponsor margin, not value or price"),
    ("Headline donor-fee bps where no schedule is in repo", "CF 90; national/faith 60; other 75", "bps", "50", "100", "Census medians and national schedules", "EV-COM-012", "Low-medium"),
    ("Management/overhead multiplier on conventional incremental cost", "1.35", "x", "1.2", "1.6", "Supervision, QA, occupancy, IT support not in activity model", "EV-COM-013", "Medium on bottom-up value"),
    ("Sponsor-level conventional cost (close, audit support, governance reporting)", "100000", "USD/yr", "50000", "200000", "ACT-S01/S04/S05 scale", "EV-COM-013", "Low"),
    ("Software cost avoided when sponsor outsources", "max(current DAF vendor payment, $150k, 3 bps x assets)", "USD/yr", "0.5 bps", "9 bps", "Software-only band 0.5-9 bps; $118-175k floor", "EV-COM-016", "Medium for large sponsors"),
    ("Sponsor oversight cost after outsourcing", "60000 + 7.5/account", "USD/yr", "40000 + 5", "120000 + 15", "7.0 sponsor-retained min/acct-yr x $61.35/h + vendor management", "EV-COM-013;EV-COM-015", "Low"),
    ("Sponsor-side migration cost, amortised over 5 years", "(150000 + 20/account)/5", "USD/yr", "(75000+10)/5", "(400000+50)/5", "Parallel run, data cleanup, donor communication; AEF lost self-service history", "EV-COM-024", "Low-medium"),
    ("Value delivered on equivalent scope = min(top-down replaceable opex, bottom-up conventional equivalent cost)", "rule", "", "", "value_high = top-down base", "Do not count work the servicer would not do; do not exceed what sponsor spends", "EV-COM-041", "High: base vs high changes 20 bps verdict for faith/CF"),
    ("For 0-employee pass-through sponsors, donor-fee revenue ~ DAF opex", "1.00", "ratio", "0.95", "1.05", "MS GIFT TPA funds Ren; opex = vendor + GOE", "EV-COM-001;EV-COM-002", "Low"),
    ("Tiered structure S4 parameters", "20 bps to $500M; 12 bps $0.5-2B; 6 bps >$2B; $250/account floor", "bps", "", "", "MSSB and USBFS program-size tier precedents", "EV-COM-033;EV-COM-002", "Illustrative"),
    ("Per-account + low bps S3 parameters", "$150/account + 7.5 bps", "", "$100+5", "$200+10", "Report 05 cost-reflective tariff centre", "", "Illustrative"),
    ("Value-share S5 parameter", "50% of equivalent-scope value; floor = servicer AI-native high-case cost", "share", "30%", "70%", "Common gain-share practice [A]; no DAF precedent found", "", "Illustrative"),
    ("Servicer marginal cost per sponsor", "sponsor-model-economics.csv annual_cost_ai_native_base/high", "USD/yr", "", "", "Previous study model (fixed costs excluded)", "EV-COM-014", "Excludes fixed company cost"),
    ("Replication difficulty scores (1 easy-5 hard)", "see replication.csv", "score", "", "", "Analyst judgement from repo evidence; same-model reasoning, not validation", "EV-COM-020;EV-COM-021;EV-COM-035", "High: qualitative"),
    ("Opportunity build sizes", "S <=6 eng-months; M 6-18; L >18", "engineer-months", "", "", "Analogy to Unbound domain clause counts and prior build estimate ($1-5M)", "EV-COM-035", "Medium"),
]
assumptions = [dict(assumption_id=f"A-COM-{i+1:03d}", statement=s, value=v, unit=u, low=lo, high=hi, basis=b, evidence_ids=e, sensitivity=se)
               for i, (s, v, u, lo, hi, b, e, se) in enumerate(AS)]
with open(f"{OUT}/assumptions.jsonl", "w") as f:
    for a in assumptions:
        f.write(json.dumps(a) + "\n")

# ------------------------------------------------------------------ opportunities
OPP_COLS = ["opp_id", "capability", "buyer", "problem", "demand_evidence", "demand_label", "evidence_ids", "price_benchmarks",
            "build_size", "build_basis", "shared_components_with_unbound", "contribution_to_full_platform", "disconnected_product_risk",
            "validates", "verdict"]
OPP = [
    ("OPP-01", "Charity verification and continuous eligibility monitoring (API + evidence record)",
     "Sponsors without in-house DD; grant processors; wealth platforms; donor apps",
     "Eligibility at approval and release; continuous monitoring vs 180-day manual re-verification (~$69 vs ~$1/acct-yr in prior model); church/Pub 78 gaps",
     "Paid market exists: CAF America $875,665 for GS CGF grant admin; Candid APIs $2,750-9,900; Charity Navigator paid API plans; iPhi resells GuideStar search API; Pledge free API with 5% donate fee",
     "demonstrated (adjacent market, commoditised core)", "EV-COM-005;EV-COM-026;EV-COM-040;EV-COM-037",
     "Data APIs $2.75k-$50k/month (conflicting); DD outsourcing ~$1,200/account at GS CGF; per-check pricing not public",
     "M", "Unbound UNB-CHAR (42 clauses) + replay screening code exists (not production); sanctions recall 88/100 must be fixed",
     "UNB-CHAR, UNB-GRANT eligibility, sanctions screening, evidence store", "High: same engine is the core of the servicer",
     "Low if built as the platform's own eligibility service; medium if a separate data product with its own data licences (Candid licence terms limit redistribution)",
     "Service quality (false-clear rate, latency); productivity (exceptions per 1,000 grants)",
     "Build first as internal component; sell externally only after recall >=99% on sanctions replay and a licence-clean data stack"),
    ("OPP-02", "Grant processing and disbursement (EFT-first, positive pay, returns handling)",
     "Small/mid sponsors and CFs; foundations; processors",
     "Check-heavy payment, voids/reissues, remittance to charities",
     "Paid: Benevity $46-54M (AOGF), CyberGrants $5.4-8.3M (CAF America); Chariot Disbursements charges grantmakers per transaction; DAFpay 2.9%",
     "demonstrated", "EV-COM-029;EV-COM-027",
     "~0.7%-2.9% of grant dollars for processors; $25/wire at NCF",
     "L", "Payments + bank integration + money-transmission analysis; counsel question unresolved in prior study",
     "CNV-PAY, TVR-PAY, UNB-PAY, reconciliation", "High (payments are ~$26/acct-yr in prior model)",
     "High: standalone disbursement makes the company a payments firm (licensing, bonding, fraud liability) before it is a servicer",
     "Economics of pass-through rails; service quality (time to charity)",
     "Do not sell standalone; keep as pass-through via licensed processor inside the servicer"),
    ("OPP-03", "Reconciliation (bank/custodian/ledger, break resolution)",
     "Sponsors with in-house ledgers; CFs on Blackbaud/Foundant",
     "Manual breaks, month-end close effort",
     "No paid DAF-specific standalone product found; repo model warns base-case savings small and not to build standalone before observed baseline",
     "potential", "EV-COM-041",
     "None DAF-specific found; generic fintech recon SaaS prices not in repo",
     "M", "Unbound UNB-RCN 97 clauses: large spec surface",
     "UNB-RCN, ledger, custodian feeds", "High: the accounting core is the hardest shared component",
     "High: reconciliation without owning the ledger means many source formats and no control over breaks",
     "Productivity (break rate, close days) - the most important unmeasured economic driver",
     "Build only as part of the ledger; offer 'close-as-a-service' to servicer clients"),
    ("OPP-04", "Sponsor/board reporting (delegated-approval reports, Schedule D support, KPIs)",
     "Sponsor CFOs, boards, auditors",
     "Board oversight of delegated approvals; 990 Schedule D preparation",
     "No observed paid product; CF Insights survey benchmarking exists (price not found)",
     "potential", "EV-COM-019",
     "None observed", "S", "Report templates over platform data; Folio has no renderer yet",
     "UNB-KNOW, Folio, metrics", "Medium", "Medium: reports from other vendors' data need integration per vendor",
     "Service quality / transparency", "Bundle; do not sell separately"),
    ("OPP-05", "Operational intelligence / benchmarking (cost per grant, exception rates, vendor footprint)",
     "Sponsors' COO/CFO; vendors; investors",
     "No analyst coverage; vendor claims hard to check",
     "Hypothesis OF3/OF7: institutional tier $5-25k; Cerulli reports $21.5-22k; McKinsey $11.8M at Fidelity proves budget not scope",
     "potential", "EV-COM-017",
     "$5-25k/yr institutional; $35-90k assessments (OF1)", "S", "Repo datasets exist; refresh labour",
     "None of the ledger; 990 harvest tooling", "Low (separate data business)",
     "Medium: independence conflict if the same firm sells servicing",
     "Market evidence; buyer conversations (cheap demand test)",
     "Useful as a cheap demand-discovery channel; low revenue; conflict with servicing must be disclosed"),
    ("OPP-06", "Customer-service automation (donor/adviser contact deflection, status, statements)",
     "Sponsors and vendors with service desks",
     "Contact volume, December peaks",
     "TIFIN 'Louise' agentic AI live; Daffy MCP; generic CX AI vendors crowded",
     "potential", "EV-COM-006",
     "No DAF-specific price; generic CX tooling", "M", "Needs account data access, identity, audit trail",
     "UNB-NAV, identity, workflow", "Medium",
     "High: an AI agent on someone else's ledger without authoritative state gives wrong answers and creates liability",
     "Productivity (contacts per 1,000 accounts)", "Internal only"),
    ("OPP-07", "Configurable donor/adviser portals (white label)",
     "CFs, faith sponsors, wealth programmes",
     "Dated portals; migrations; history loss",
     "Paid: Ren/Stellar software lines $118-416k/yr at CFs, $801k at Stifel; 8 recorded CF migrations 2022-26 (6 to Foundant)",
     "demonstrated (contested)", "EV-COM-016;EV-COM-018;EV-COM-019",
     "0.5-9 bps; $34-611/account; ~$120-175k floor", "L", "Forma 174 components, 28 unimplemented; 140 Unbound screens specified",
     "Forma, Limen, UNB-NAV, UNB-EXT", "High",
     "Very high: a portal without the ledger is a front-end over incumbent ledgers - integration to iPhi/Foundant/Blackbaud each",
     "Service quality (donor experience); weak on economics", "Only as part of full platform"),
    ("OPP-08", "Advisor widgets and data feeds (balances, grant activity in adviser tools)",
     "RIAs, broker-dealers, wealth platforms",
     "Advisers lack DAF data in their stack",
     "Addepar lists only Fidelity DAF feed (needs Fidelity advisory relationship); TIFIN/Foundation Source market adviser white label and BridgeFT multi-custodian",
     "potential (adjacent demonstrated)", "EV-COM-006",
     "Not public", "S-M", "API + entitlements",
     "UNB-API, UNB-EXT, identity", "Medium (distribution channel)",
     "Medium: feeds from other sponsors require their consent and APIs",
     "Distribution/demand; adviser engagement", "Build as part of platform; partner with aggregators"),
    ("OPP-09", "Compliance evidence (control evidence by default, SOC 1/2 support, audit packs)",
     "Sponsor CFOs, auditors; vendors needing SOC",
     "Audit support labour; scoped assurance gaps (Ren SOC report conflict noted in repo)",
     "No paid DAF-specific product observed; audit fees paid to firms (Deloitte, RSM lines)",
     "potential", "EV-COM-017",
     "Not observed", "M", "Evidence store + control register; Unbound control baseline exists (82 clauses approved)",
     "Control register, evidence store, ledger events", "High: the differentiator of the full platform",
     "High standalone: evidence about another vendor's ledger is not evidence",
     "Service quality / assurance; auditor acceptance", "Core of platform; not a separate product"),
    ("OPP-10", "Data migration and continuity (full-fidelity export/import, acceptance tests)",
     "Sponsors changing platforms; vendors onboarding",
     "Grant freezes 3-5 weeks; lost history (AEF 2 years self-service)",
     "Demonstrated: Ren sells data migration add-on; 8 CF migrations recorded; OF6 hypothesis $25-75k; Foundant absorbs POC migration pre-sale",
     "demonstrated (event-driven)", "EV-COM-023;EV-COM-024;EV-COM-018;EV-COM-031",
     "$25-75k project hypothesis; Foundant $250/h", "M", "Mapping per source system (iPhi, Blackbaud, Foundant, DonorCentral)",
     "Import pipelines, canonical grant record, reconciliation", "High: every servicer onboarding needs it",
     "Low: the importer is the onboarding tool",
     "Productivity (onboarding cost $105k assumed); service quality", "Build early; sell as onboarding + independent assurance"),
    ("OPP-11", "Workflow automation (delegated approval, exceptions, complex-gift intake)",
     "Sponsors with manual approval queues",
     "Approval latency; exception handling",
     "Fluxx 'Grantelligence' paid add-on (grantmaking, not DAF); OF9 complex-asset decision support rejected for lack of repeat buyers",
     "potential", "EV-COM-019",
     "Add-on subscription (amount unpublished)", "M", "Policy engine; Praxis/Ordo not production",
     "UNB-WF, UNB-RULE, UNB-GRANT", "High",
     "High: rules over another vendor's data needs deep integration; liability for approvals",
     "Productivity (minutes per grant); the 50-min claim", "Internal; external only via shadow-mode replay with design partner"),
]
with open(f"{OUT}/opportunities.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(OPP_COLS)
    w.writerows(OPP)

# ------------------------------------------------------------------ replication
REP_COLS = ["row_type", "advantage", "conceptual", "technical", "organisational", "capital", "time", "migration", "revenue_disruption",
            "operational_disruption", "mean_difficulty", "time_to_match_months_favourable_incumbent", "time_to_match_months_unfavourable_incumbent",
            "who_can_copy_fastest", "who_struggles", "incumbent_incentive", "combination_effect", "previous_verdict", "revised_verdict", "evidence_ids"]
REP = [
    ("advantage", "Shared verification network (cross-sponsor reuse of eligibility evidence)", 1, 2, 2, 2, 2, 1, 1, 1,
     "6-12", "18-24", "Ren (GuideStar API, Ren for Charities network), Fidelity (largest recipient overlap)", "Single-CF vendors without network",
     "Positive: cuts their cost; no revenue loss", "Feeds evidence-by-default and minimum-touch", "Temporary to weak", "Weak: understood and implementable; network effect favours largest incumbents", "EV-COM-037;EV-COM-040"),
    ("advantage", "Integrated accounting controls with evidence-by-default (single ledger, control evidence emitted by transactions)", 2, 4, 3, 4, 4, 4, 2, 4,
     "18-30 (single-codebase vendor: Foundant, TIFIN)", "36-60 (multi-lineage: Ren iPhi + DFX + Pinkaloo heritage)", "Single-codebase vendors; captive nationals with capital (Vanguard tech spend $2-6M/yr)", "Multi-lineage vendors with many customised ledgers and clients on old versions",
     "Mixed: improves audit cost but forces re-platforming of paying clients", "Precondition for portability and minimum-touch at scale", "Moderately durable if delivered; incumbent-favoured on SOC history",
     "Most durable technical advantage against multi-lineage incumbents; NOT durable against a funded greenfield sub-brand; entrant starts with zero assurance history", "EV-COM-020;EV-COM-021;EV-COM-045"),
    ("advantage", "Reusable configuration (policy packs instead of custom code/change orders)", 1, 3, 3, 2, 3, 3, 2, 2,
     "12-18", "24-36", "Foundant (CF templates), TIFIN", "Vendors whose installed base runs per-client customisations",
     "Mildly negative (change-order and add-on revenue) but scaled vendors' one-time services are small (Blackbaud: immaterial)", "Lowers onboarding cost, enables value-share pricing", "Temporary",
     "Temporary for new clients; slow for incumbents' installed base (customisation debt)", "EV-COM-023;EV-COM-032"),
    ("advantage", "Minimum-touch operations (delegation, EFT default, continuous monitoring, exception-only review)", 1, 2, 4, 2, 3, 2, 1, 3,
     "6-18", "24-36", "Any bps-priced incumbent: cost cuts raise their margin", "Staffed BPO teams; sponsors whose boards will not delegate",
     "Positive for bps-priced incumbents (keep revenue, cut cost) - strongest reason they WILL copy", "Without a single ledger, exception routing is partial", "Temporary",
     "Temporary; the binding constraint is sponsor board delegation, which is equally available to incumbents", "EV-COM-035"),
    ("advantage", "Per-account / payout-neutral pricing with activity fees", 1, 1, 2, 1, 1, 1, 4, 1,
     "0-6 (for at-risk accounts)", "12-36 (book-wide repricing)", "Channel owners (MSSB/TIFIN) who earn on advisory assets", "Ren at small-balance books (USCGT 40 bps would halve)",
     "Negative where bps exceed cost-to-serve; neutral at MS GIFT (already ~$737)", "Counter-positioning only while incumbent revenue depends on bps", "More durable (positioning)",
     "Moderately durable: incumbents re-tier selectively at renewal (cheap); book-wide repricing is costly", "EV-COM-001;EV-COM-003;EV-COM-043"),
    ("advantage", "Portability (no termination fee, full-fidelity export incl. approval provenance)", 1, 3, 2, 2, 2, 1, 3, 1,
     "3-6 (contract terms)", "18-30 (full-fidelity export technically)", "Single-codebase vendors", "Vendors with 15-day export windows and fragmented records",
     "Negative: lock-in protects renewal", "Requires the single ledger to be true", "Durable as positioning",
     "Contract promise copyable quickly; full-fidelity export is a data-model property and is slower", "EV-COM-021;EV-COM-022;EV-COM-024"),
    ("advantage", "AI-native development (agents write/test code under provenance)", 2, 3, 4, 2, 3, 2, 1, 2,
     "6-12 (tools are generic)", "24-48 (legacy codebases, regulated change control)", "Well-funded vendors with modern stacks", "Vendors with old code and change-advisory processes",
     "Positive", "Lowers cost of the other six only if the code base is clean", "Not assessed",
     "Weak and unverified for Echelon (ECH-02 described-not-verified; PolyForm NC licence); tools are available to everyone", "EV-COM-038;EV-COM-039"),
    ("combination", "All seven together, delivered as one service with published control metrics", 2, 4, 5, 4, 4, 4, 4, 4,
     "18-30 (greenfield sub-brand or acquisition of the entrant)", "48-72 (transform installed base)", "Captive nationals for themselves; acquirers (6 of 6 DAF-tech exits went to consolidators per repo H-07)", "Multi-lineage vendors protecting 3-customer revenue concentration",
     "Conjunction forces re-platforming + repricing + org change at once; incentives conflict", "The difficulty is in the conjunction, not any one item", "Few advantages durable",
     "Moderately durable against installed-base transformation; NOT durable against greenfield replication or acquisition. Incumbents can transform: they can build a new sub-brand and migrate selectively", "EV-COM-020;EV-COM-043;EV-COM-045"),
]
REP2 = []
for r in REP:
    scores = r[2:10]
    REP2.append(list(r[:10]) + [round(sum(scores) / 8, 2)] + list(r[10:]))
RESP = [
    ("incumbent_response", "Ren (multi-lineage vendor + BPO; MS GIFT, USCGT, RCF)", "", "", "", "", "", "", "", "", "",
     "Favourable to entrant: Ren busy integrating iPhi/DFX, losing CF iPhi clients to Foundant, protects RCF/MS GIFT; reacts only at renewals", "Unfavourable: re-tier small-balance books at renewal, waive change orders, bundle 'managed services' on Stellar at marginal cost, offer multi-year discounts; build a greenfield DFX ledger in 24-36 months",
     "", "", "Cheapest response first: do nothing at MS GIFT (already ~18.5 bps)", "", "", "", "EV-COM-001;EV-COM-020;EV-COM-043"),
    ("incumbent_response", "Foundant (CF all-fund-type platform, winning migrations)", "", "", "", "", "", "", "", "", "",
     "Favourable: CF DAF-only servicing is not its business; DAF-only servicer must integrate with Foundant for non-DAF funds", "Unfavourable: adds BPO/managed services and continuous monitoring to CommunitySuite; CFs prefer one system for all fund types (Unbound EV-04)",
     "", "", "", "", "", "", "EV-COM-018;EV-COM-036"),
    ("incumbent_response", "TIFIN Give / Foundation Source (channel-funded, acquisitive)", "", "", "", "", "", "", "", "", "",
     "Favourable: focused on adviser distribution and investment economics", "Unfavourable: cross-subsidise admin from management/sponsorship fees; acquire an AI-native entrant",
     "", "", "", "", "", "", "EV-COM-006"),
    ("incumbent_response", "Captive nationals (Fidelity, Schwab, Vanguard) and NPT", "", "", "", "", "", "", "", "", "",
     "Favourable: not buyers; their transformation does not take the entrant's customers", "Unfavourable: NPT private-label or a captive offering administration to third parties at marginal cost; demonstrated capacity to spend $3-12M/yr on consulting/tech",
     "", "", "", "", "", "", "EV-COM-017;EV-COM-045"),
]
with open(f"{OUT}/replication.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(REP_COLS)
    w.writerows(REP2)
    w.writerows([list(x) for x in RESP])

# ------------------------------------------------------------------ report
sv = pd.read_csv(f"{OUT}/sponsor-value.csv")
arch = sv[sv.row_type == "archetype"]


def fm(x):
    return f"${x/1e6:.2f}M"


arch_tbl = "| Archetype (median inputs) | Assets | Accts | Avg bal | Donor-fee rev (bps) | DAF opex (bps) | Value: base / high (bps) | Value $/acct base | Max value price base / high (bps) | 20 bps = $/acct | Sponsor net @20bps base / high | Net @$737 base | Net @$150+7.5bps base | Net @value-share | Servicer contribution @20bps |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
for _, r in arch.iterrows():
    arch_tbl += (f"| {r['name']} | {fm(r.avg_assets_usd)} | {r.accounts} | ${r.avg_balance_usd:,.0f} | {r.donor_fee_revenue_bps_base} | {r.daf_opex_bps} | "
                 f"{r.value_delivered_bps} / {round(r.value_delivered_high_usd / r.avg_assets_usd * 1e4, 1)} | ${r.value_delivered_per_account_usd:,.0f} | "
                 f"{r.max_value_price_base_bps} / {r.max_value_price_high_bps} | ${r.S1_flat_20bps_price_per_account:,.0f} | "
                 f"{fm(r.S1_flat_20bps_sponsor_net_value_usd)} / {fm(r.S1_flat_20bps_sponsor_net_value_high_usd)} | {fm(r.S2_per_account_737_sponsor_net_value_usd)} | "
                 f"{fm(r['S3_per_account_150_plus_7.5bps_sponsor_net_value_usd'])} | {fm(r.S5_value_share_50pct_sponsor_net_value_usd)} | {fm(r.S1_flat_20bps_servicer_contribution_usd)} |\n")

named = sv[sv.row_type == "named_sponsor"]
pick = ["MORGAN STANLEY GLOBAL IMPACT FUNDING TRUST INC", "THE US CHARITABLE GIFT TRUST", "RAYMOND JAMES CHARITABLE ENDOWMENT FUND", "AMERICAN ENDOWMENT FOUNDATION",
        "JEWISH COMMUNAL FUND", "IMPACTASSETSINC", "Greater Horizons", "Greater Kansas City Community Foundation", "The Chicago Community Trust", "FOUNDATION FOR THE CAROLINAS",
        "Combined Jewish Philanthropies of Greater Boston Inc", "NATL CHRISTIAN CHARITABLE FDN INC", "THE NEW YORK COMMUNITY TRUST", "COLUMBUS FOUNDATION"]
ntbl = "| Sponsor | Group | Avg bal | Fee rev bps (kind) | Current DAF vendor | Value base / high bps | Value $/acct | Max price base bps / $acct | Max price high bps | Net @20bps base / high | Net @$737 | Net @$150+7.5 | Net @tiered |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
for nm in pick:
    r = named[named.name == nm].iloc[0]
    ntbl += (f"| {nm.title()[:40]} | {r.service_group} | ${r.avg_balance_usd:,.0f} | {r.donor_fee_revenue_bps_base} ({r.donor_fee_revenue_kind}) | {fm(r.current_daf_vendor_payment_usd)} | "
             f"{r.value_delivered_bps} / {round(r.value_delivered_high_usd / r.avg_assets_usd * 1e4, 1)} | ${r.value_delivered_per_account_usd:,.0f} | {r.max_value_price_base_bps} / ${r.max_value_price_base_per_account:,.0f} | {r.max_value_price_high_bps} | "
             f"{fm(r.S1_flat_20bps_sponsor_net_value_usd)} / {fm(r.S1_flat_20bps_sponsor_net_value_high_usd)} | {fm(r.S2_per_account_737_sponsor_net_value_usd)} | {fm(r['S3_per_account_150_plus_7.5bps_sponsor_net_value_usd'])} | {fm(r.S4_tiered_bps_floor_sponsor_net_value_usd)} |\n")

buy = named[~named.captive_status.isin(["captive_inhouse_affiliate", "vendor_captive", "inhouse_platform_custom"]) & (named.recent_migration != 1)]
S = ["S1_flat_20bps", "S2_per_account_737", "S3_per_account_150_plus_7.5bps", "S4_tiered_bps_floor", "S5_value_share_50pct", "S6_per_account_350_plus_3bps_cap20"]
agg = {k: buy[k + "_price_usd"].sum() / buy.avg_assets_usd.sum() * 1e4 for k in S}
stbl = "| Structure | Median price bps | Book-weighted bps | Median $/acct | Sponsors better off, base value (of %d) | ...if top-down value | Servicer covers marginal cost |\n|---|---|---|---|---|---|---|\n" % len(buy)
for s in S:
    stbl += (f"| {s} | {buy[s + '_price_bps'].median():.1f} | {agg[s]:.1f} | ${buy[s + '_price_per_account'].median():,.0f} | {(buy[s + '_sponsor_net_value_usd'] > 0).sum()} | "
             f"{(buy[s + '_sponsor_net_value_high_usd'] > 0).sum()} | {(buy[s + '_servicer_contribution_usd'] > 0).sum()} |\n")
mv_b = buy.max_value_price_base_bps.median()
mv_h = buy.max_value_price_high_bps.median()

SECTIONS = []


def sec(t, m):
    SECTIONS.append({"section": t, "markdown": m})


sec("COM summary", f"""**Group COM, 2026-11-25. Commercial: pricing, sponsor value, incremental offers, customer-funded development, incumbent replication.** Labels [S]/[A]/[D]/[E]; evidence EV-COM-001..{len(evidence):03d}, assumptions A-COM-001..{len(assumptions):03d}. Same-model reasoning; not validated with any buyer.

**Five most consequential findings**
1. **$737/account (MS GIFT) is not a market-wide ceiling, but the previous verdict on high-balance books largely survives for a different reason.** MS GIFT's 18.5 bps buys a narrower scope (0-employee bank channel; MSSB separately earns 7 bps admin plus up to 1% advisory and owns the donor relationship), and observed per-account prices run $413-$1,198 (USCGT $429, Stifel stack $1,142, CAF America grant-admin-only $1,198) [S, EV-COM-001..005]. However, on **equivalent scope** the value a servicer delivers to a high-balance sponsor is about **$560-1,830 per account but only 5-10 bps**; median value-based maximum price across {len(buy)} buyable top sponsors is **{mv_b:.1f} bps (base)** and **{mv_h:.1f} bps** only if sponsors actually shed the assumed share of their own DAF opex [D].
2. **20 bps is defensible as value-based pricing in three places only:** (a) sponsors that already outsource at >=20 bps (USCGT 40, RCF-like 38; RJ ~18-20 borderline); (b) sponsors that will actually retire DAF staff/systems (faith federations and CFs whose DAF opex is 100-200 bps; value_high 40-68 bps) - i.e. a headcount decision, not a price decision; (c) small/mid-balance books ($100-400k) where per-account value is close to 20 bps x balance. For $1M+ balance books 20 bps flat ($1,500-5,000/acct) exceeds equivalent-scope value in every base case.
3. **Per-account-led and value-share structures dominate flat 20 bps, but they reveal that 20 bps is not the book-weighted value of the top market.** Value-share leaves {(buy['S5_value_share_50pct_sponsor_net_value_usd'] > 0).sum()}/{len(buy)} buyable top sponsors better off and covers servicer marginal cost in all; $350/account + 3 bps (capped at 20 bps) leaves {(buy['S6_per_account_350_plus_3bps_cap20_sponsor_net_value_usd'] > 0).sum()}/{len(buy)} better off; flat 20 bps {(buy['S1_flat_20bps_sponsor_net_value_usd'] > 0).sum()}/{len(buy)}; the earlier $150 + 7.5 bps tariff only {(buy['S3_per_account_150_plus_7.5bps_sponsor_net_value_usd'] > 0).sum()}/{len(buy)} (its bps component is too high at $1M+ balances). Book-weighted, the acceptable tariffs earn **{agg['S6_per_account_350_plus_3bps_cap20']:.1f}-{agg['S2_per_account_737']:.1f} bps** on top-30 assets, not 20. Keep 20 bps as the objective for small/mid-balance and already-outsourced books; it is not reachable across high-balance books without the sponsor retiring its own DAF staff.
4. **Incremental products mostly have potential, not demonstrated, demand; the demonstrated ones (verification data, disbursement, portals, migration) are contested or carry the highest disconnected-architecture risk.** Migration/onboarding tooling and eligibility services are the two that both have paid precedents and are components of the full platform.
5. **Incumbent replication: understanding is easy, enterprise implementation is not - but it is not impossible.** Individually, five of seven advantages are copyable within 6-24 months under conditions favourable to the incumbent. The conjunction (single ledger + evidence-by-default + portability + per-account pricing) is moderately durable against multi-lineage incumbents (48-72 months to transform an installed base) and **not durable** against a funded greenfield sub-brand or acquisition (18-30 months).

**Largest gaps:** no executed servicer contract or price sheet; no sponsor cost-by-activity data (value relies on [A] replaceable shares and an un-time-studied activity model); no observed design-partner fee in DAF; no buyer willingness-to-pay evidence.""")

sec("Part 1a: pricing logics distinguished", """| Logic | What sets the price | DAF evidence | Fits a servicer at 20 bps? |
|---|---|---|---|
| **Cost-based** | Servicer cost + margin | Prior model: AI-native ~$89/acct market mix [D from A], conventional ~$262 | Gives ~3-8 bps at $400k balances: leaves value on the table and invites 'pass the savings' demands |
| **Competitive** | Incumbent price for same scope | Ren 18.5 bps/$737 (MS GIFT), 40 bps/$429 (USCGT), TIFIN 30 / 10-20 bps list | 20 bps = parity at ~$400k, discount below $250k, premium above $1M |
| **Value-based** | Buyer's avoided cost (equivalent scope only) + quality value | This study: 5-10 bps base at high balances; 18-40 bps where sponsor already outsources at that level | Defensible only where avoided cost is real (see 1c) |
| **Asset-based (bps)** | AUA | All donor schedules; MSSB 7 bps; USBFS tiers | Aligns with donor fee; mismatches account/transaction-driven cost; market risk |
| **Per-account** | Accounts | $100-360 donor minima; Ren $413-814/acct realised; NC ABLE $5/acct state fee [C] | Matches cost shape; can deter small accounts unless capped |
| **Activity-based** | Events (grants, complex gifts, wires, foreign DD) | MS GIFT 2019 $2,000-3,500 per 'other grantee'; NCF $25/wire; RCF extraordinary-service fees | Right for genuinely exceptional work; must not deter grants (charitable-purpose safeguard) |
| **Hybrid** | Per-account + low bps + activity fees, with floors/caps | Report 05 tariff $100-200 + 5-10 bps; USBFS bps + $60k minimum + CPI | Preferred form, but per-account-led (~$350 + 3 bps, cap 20 bps); report 05's bps share is too high for $1M+ books |
| **Value-share** | Share of measured avoided cost | No DAF precedent found; RCF->Ren 95-98% fee share is a related-party revenue share | Best alignment, but needs a measured baseline (time study) and audit rights |

**Safeguards preserved in every structure modelled:** payout-neutral base (approved-unpaid grants excluded from billable assets; RC-SE-002); complex gifts, foreign/ER grants and wires as cost-based activity fees, never inside the asset fee (RC-SE-007) and never applied in a way that deters an acceptable grant; per-account floors waived for accounts in wind-down after a final grant and capped so they never exceed the account's balance-based fee by more than the floor (RC-SE-001); payment rails passed through at cost (RC-SE-003); no fee on grant dollars.""")

sec("Part 1b: is $737/account a market-wide ceiling? (challenge)", """**No.** The previous study used Ren at MS GIFT ($737, 18.5 bps) as the per-account anchor and concluded 20 bps is 2-7x too expensive at high-balance programs. Five corrections:
1. **Scope is narrower than a self-operated sponsor's.** MS GIFT has 0 employees; MSSB is paid a separate 7 bps admin/platform fee by donors and earns advisory fees up to 1.00% on the same assets; financial advisers own onboarding, donor relationship and much service [S, EV-COM-002]. Ren's $737 buys back-office administration for a channel that has already absorbed front-office cost.
2. **Concentration and scale.** $8.1B across 21,800 accounts from one contract; realised take below the donor TPA first tier (27 bps) implies custom deals on very large accounts [S/D]. A single-contract price for the largest outsourced book is a volume price, not a ceiling.
3. **Other observed per-account prices are higher:** Stifel full stack $1,142; Bradley $1,140; CAF America grant administration alone $1,198; GiveClear/TIFIN $815; RCF $814 [S]. And lower: USCGT $429. Per-account price is not stable either; it rises with balance and grant intensity.
4. **Sponsor revenue context.** Sponsors keep 30-54 bps of realised donor fees in most groups (Fidelity 22.9, JCF 42.2, RCF 38.7 realised; CFs ~30-60 estimated) [S/E]; a 20 bps servicer price is 40-65% of that revenue, which matters for affordability but is not itself evidence of value.
5. **Alternatives differ by buyer:** in-house (nationals spend 14-27 bps all-in), software-only (0.5-9 bps) plus own staff, BPO (Ren), or a channel owner absorbing cost. A buyer's reservation price is its best alternative, not MS GIFT's contract.

**But the conclusion largely survives on value grounds** (1c): the equivalent-scope work a servicer replaces at a $1M+ balance sponsor is worth roughly $600-1,800 per account, i.e. 5-10 bps. The defensible per-account price for high-balance books is therefore **above $737 (often $1,000-1,700)** but **well below 20 bps** ($1,500-5,000).""")

sec("Part 1c: sponsor value model and archetypes", f"""**Method** (`scripts/sponsor_value.py`, reproducible). For each sponsor: donor-fee revenue (realised where audited; else schedule at mean balance x realisation 0.6, calibrated 0.38-0.68) [S/E]; DAF opex = 990 opex ex investment mgmt x DAF asset share, less advertising/professional fundraising [S/D]; **value delivered** = min(top-down: DAF opex x replaceable share [A-COM-001], bottom-up: accounts x conventional equivalent-scope cost by balance archetype x 1.35 overhead + $100k sponsor-level + avoided software [D from A]); `value_high` = top-down unbounded (only if the sponsor actually sheds that share). For 0-employee outsourced sponsors value = current vendor payment. Sponsor net value = value - oversight ($60k + $7.5/acct) - migration ((150k + $20/acct)/5) - price. Servicer contribution = price - AI-native marginal cost from the previous model (fixed company cost excluded).

{arch_tbl}
Reading: the **base** case (bottom-up bound) says a CF or faith federation would be worse off at 20 bps; the **high** case says it would be better off **only if** it cut DAF operating staff and systems by the assumed share (30-45%) - an organisational choice the servicer cannot make for it. Advisor programmes (0-employee, median $1.1B, vendor median $1.05M, 9.5 bps) already buy cheaper than 20 bps; note many of them buy software-only and staff ops at an affiliate, whose cost is not visible on the 990 (gap). CF 'margin now' is negative under asset allocation because CF opex funds community work: fee revenue is not DAF-only profit.""")

sec("Part 1d: named top sponsors (from sponsor-model-economics.csv / sponsor-economics.csv)", f"""{ntbl}
**Pricing-structure scoreboard across {len(buy)} buyable top-30 sponsors** (captives and the recently migrated excluded):

{stbl}
Observations [D]: MS GIFT is better off switching only below ~18 bps ($669/acct after oversight/migration) - confirms parity, nothing more. USCGT (Ren at 40 bps) is the clearest 20-bps-value case (+$2.0M/yr net). AEF, JCF, Greater Horizons, GKCCF: base value 8-10 bps ($500-610/acct); 20 bps leaves each $2.6-7.7M/yr worse off; per-account $737 is near break-even; value-share leaves them +$0.8-3.2M. High-balance CFs (Chicago CT, FFTC, CJP): value $1,300-1,830/acct; $737/acct is affordable (+$0.5-1.1M), 20 bps ($4,500-5,200/acct) is not. NCF (custom in-house, 31,943 accounts, $167k balance) shows the opposite: 20 bps ($334/acct) is below base value ($417/acct) - small-balance high-volume books are where 20 bps is cheap.""")

sec("Part 1e: conclusions on 20 bps, passing efficiency, and competing on service", f"""**Is 20 bps defensible as value-based pricing?** Yes, where avoided equivalent-scope cost >= 20 bps + oversight + migration: (1) currently outsourced books at 25-40 bps (USCGT-, RCF-, RJ-like; small/mid balances $100-250k); (2) high-volume, small-to-mid-balance in-house books (NCF-like, $150-400k balances) where per-account work is dense; (3) any sponsor that commits to retire DAF staff/systems (value_high median {mv_h:.1f} bps). **No** for high-balance ($1M+) independent nationals, faith federations and CFs on equivalent scope (base 5-10 bps) - there 20 bps only works as a **book-level revenue objective delivered through a per-account tariff** ($1,000-1,700/acct) or a value share.

**Must we pass efficiency to customers?** Not by doctrine - value pricing captures the gap between our cost (~$89/acct AI-native, ~$170-220 high-value) and the buyer's avoided cost ($400-1,800). But three forces will push part of it through: (a) incumbent re-tiering at renewals (cheapest response, report 01 g); (b) charitable sponsors' boards owe donors reasonable fees and publish schedules - a sponsor that saves cost but keeps donor fees faces scrutiny; (c) the value-share floor/ceiling must be auditable. Plan for 30-50% of measured savings to reach sponsors (value-share 50% modelled) and protect margin through cost, not price.

**Competing on service, reliability, transparency, flexibility.** Where price parity holds (MS GIFT-like), switching gains are ~0 or negative after migration cost, so only non-price value moves buyers: measured grant turnaround, exception error rates, published control metrics, full-fidelity export, no termination fee, configurable policy without change orders. These are real but **unquantified** in public data; they cannot carry a price premium until measured at a design partner. The weakest claim is 'reliability': the entrant has no SOC history (incumbent-favoured).

**Recommended tariff (testable):** a **per-account-led hybrid** - about $350/account + ~3 bps, capped at 20 bps (S6; ~20 bps at $100-200k balances, ~10 bps at $500k, ~6 bps at $1-2M) - or a value share of measured savings for sponsors willing to baseline; this corrects report 05's $150 + 7.5 bps, whose bps component exceeds equivalent-scope value at $1M+ balances; activity fees at cost for complex gifts, foreign/ER grants and wires; optional value-share above a measured baseline with a cap at 20 bps; payout-neutral base; floors waived in wind-down. This keeps 20 bps as the working objective on the books where it is value-defensible and stops it from being the reason high-balance buyers say no.""")

sec("Part 2: incremental commercial opportunities", """Full table: `opportunities.csv` (11 rows). Demand label: **demonstrated** = someone is observed paying for this capability (repo or public source); **potential** = only a hypothesis or adjacent product.

| Capability | Demand | Price anchors | Build | Platform contribution | Disconnected-product risk | Verdict |
|---|---|---|---|---|---|---|
| Charity verification / monitoring | Demonstrated, commoditised (CAF America $0.88M at GS CGF; Candid APIs) | $2.75k+/mo data; ~$1,200/acct outsourced DD | M | High (core engine) | Low as internal service; licence risk externally | Build first internally; sell only after sanctions recall fixed (88/100 in replay) |
| Grant processing / disbursement | Demonstrated (Benevity, CyberGrants, Chariot) | 0.7-2.9% of grants | L | High | **High** (money transmission) | Pass-through via licensed processor |
| Reconciliation | Potential (repo model warns against standalone) | none found | M | High | High without ledger | Inside ledger only |
| Sponsor reporting | Potential | none | S | Medium | Medium | Bundle |
| Operational intelligence | Potential (OF3/OF7) | $5-25k/yr | S | Low | Medium (independence conflict) | Demand-discovery channel only |
| Customer-service automation | Potential (TIFIN Louise, Daffy MCP exist) | none DAF-specific | M | Medium | High (agent on foreign ledger) | Internal |
| Configurable donor portals | Demonstrated, contested (Ren/Stellar $118-416k/yr CF lines; 8 migrations, 6 to Foundant) | 0.5-9 bps | L | High | **Very high** (front-end over incumbent ledgers) | Only as full platform |
| Advisor widgets/feeds | Potential (adjacent: Addepar-Fidelity, TIFIN, BridgeFT) | not public | S-M | Medium | Medium | With platform; partner with aggregators |
| Compliance evidence | Potential | not observed | M | High (differentiator) | High standalone | Core, not a product |
| Data migration / continuity | Demonstrated, event-driven (Ren add-on; AEF 2-year history) | $25-75k projects; $250/h | M | High (onboarding) | Low | **Build early; sell as onboarding + independent assurance** |
| Workflow automation | Potential (Fluxx add-on; OF9 rejected) | add-on subscription | M | High | High | Internal; shadow replay with partner |

**Architectural risk.** Each standalone product sold onto another vendor's ledger forces integrations with iPhi/DFX, Foundant, Blackbaud and in-house systems - each a separate data model - and creates evidence about records the company does not control. Selling disconnected products risks building five integration businesses instead of one platform. The two products whose external version **is** the platform component (eligibility service, migration/import) are the only ones that validate economics (onboarding cost, exception rates) while building shared assets. Operational intelligence is the cheapest way to test buyer demand but validates nothing about productivity.""")

sec("Part 3: customer-funded development", """**Evidence (public/repo only).**
| Evidence | What it shows | Quality |
|---|---|---|
| TIFIN Give ADV: 'one-time implementation fee and ongoing subscription fee' for third-party platform users, amounts undisclosed | Implementation fees exist in DAF tech | A (EV-COM-006) |
| Ren product descriptions: SSO, data migration onto DFX, API integration, branding as add-ons; MSA order forms/SOWs set fees; termination fees through quarter-end; 1-year auto-renewal | Implementation and change work are billed; contracts protect vendor revenue | B (EV-COM-021..023) |
| Foundant $250/h consulting, $2,500/trainer-day; no-cost proof-of-concept migration before contract | CF vendors bill services but absorb pre-sale migration to win | A / C (EV-COM-030/031) |
| Blackbaud FY2025: one-time services revenue immaterial, combined into revenue | At scale, implementation is a small revenue pool | C (EV-COM-032) |
| USBFS fund admin: bps tiers + $60k minimum + CPI escalator | Minimum-annual-fee precedent | A (EV-COM-033) |
| NC ABLE term sheet: $5/account state administration fee; state ABLE RFPs (IL, CA, MD) award program managers with no implementation fee visible | Public procurement prices recurring per-account/asset fees; implementation absorbed | C (EV-COM-034) |
| Sponsors' own Part VII-B lines: AEF PRCGEN 'software development' $532,562 (2022); Vanguard Slalom $2-3.7M/yr; Fidelity McKinsey $11.8M; CFT EPAM $1.6M | **Large sponsors already fund development directly** - the budget exists, scope undisclosed | A (EV-COM-017/045) |
| Chariot Donor Accounts beta with 'a handful of design partners', unnamed, no fees | Design partnerships occur; terms not public | A (EV-COM-028) |
| RCF -> Ren 95-98% fee share; GivingTech advertises 'full-service revenue share' | Revenue-share structures exist (related-party / advertised) | A / B |

**No public evidence found** of a DAF design partner prepaying development, taking equity, or of an amount for any DAF implementation fee. The prior model's $100k implementation fee remains [A].

**Structures and fit.**
| Structure | Mechanism | Fit | Risk |
|---|---|---|---|
| Prepaid implementation (credited against first-year fees) | $100-500k at signing/go-live | Best fit; mirrors TIFIN/Ren | Sponsor paying for vendor-owned IP with charitable assets must be at fair market value for services received (private-benefit/excess-benefit exposure; counsel) |
| Minimum annual fee | Floor regardless of AUA (USBFS precedent) | Good; protects capital plan | Sponsor bears market risk asymmetry |
| Development partnership | Partner funds named features; vendor keeps IP; partner gets licence, MFN pricing, roadmap seat | Plausible for nationals with consulting budgets | Bespoke drift destroys reusable configuration; exclusivity demands |
| Revenue share / fee share | Vendor takes share of donor fees (RCF model) | Aligns with value-share pricing | Ties servicer to donor fee levels; related-party optics if governance overlaps |
| Equity/warrants to partner | Partner invests | Rare for 501(c)(3) sponsors; possible for for-profit channels (banks, RIAs, TIFIN-like) | Charity holding vendor equity creates conflict in vendor oversight; investment policy limits |

**Risks overall:** concentration (one partner = most revenue; prior study: margin 48% -> 3% if anchor lost); customisation debt; partner procurement/board timelines (6-12 months); charitable-purpose constraints on how a sponsor may spend; IP and data-rights disputes (iPhi MSA reserves vendor rights to anonymised data); partner churn before payback. Customer-funded development can reduce, not remove, the $2.7-11M capital range: a realistic prepaid implementation ($100-500k) covers onboarding, not the platform build.""")

sec("Part 4: incumbent replication", """Full scores: `replication.csv` (1 = easy for incumbent, 5 = hard; [E] judgement on repo evidence).

| Advantage | Concept | Tech | Org | Capital | Time | Migration | Revenue disruption | Ops disruption | Mean | Months to match (favourable to incumbent / unfavourable) | Revised verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Shared verification network | 1 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1.5 | 6-12 / 18-24 | Weak; network effects favour largest incumbents |
| Integrated accounting + evidence-by-default | 2 | 4 | 3 | 4 | 4 | 4 | 2 | 4 | 3.4 | 18-30 single-codebase / 36-60 multi-lineage | Most durable technical edge vs multi-lineage vendors; entrant has no SOC history |
| Reusable configuration | 1 | 3 | 3 | 2 | 3 | 3 | 2 | 2 | 2.4 | 12-18 / 24-36 | Temporary for new clients; slow for installed base |
| Minimum-touch operations | 1 | 2 | 4 | 2 | 3 | 2 | 1 | 3 | 2.3 | 6-18 / 24-36 | Temporary - bps-priced incumbents gain margin by copying |
| Per-account / payout-neutral pricing | 1 | 1 | 2 | 1 | 1 | 1 | 4 | 1 | 1.5 | 0-6 selective / 12-36 book-wide | Positioning; selective re-tiering is cheap |
| Portability | 1 | 3 | 2 | 2 | 2 | 1 | 3 | 1 | 1.9 | 3-6 contract / 18-30 full-fidelity | Promise copyable; full-fidelity export slower |
| AI-native development | 2 | 3 | 4 | 2 | 3 | 2 | 1 | 2 | 2.4 | 6-12 / 24-48 | Weak and unverified for Echelon (ECH-02; PolyForm NC) |
| **All seven combined** | 2 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 3.9 | 18-30 greenfield or acquisition / 48-72 installed-base transformation | Moderately durable vs transformation; not vs greenfield/acquisition |

**Understanding vs implementing.** Every advantage is conceptually easy (scores 1-2). Implementation difficulty lives in: (1) **legacy architecture** - Ren's platform is an acquisition stack (Blackbaud DAF tech 2011, DonorFirst 2016, Pinkaloo 2021, iPhi/Stellar 2023) with separate MSAs and no observed ledger unification; (2) **customisations and contracts** - per-client order forms/SOWs, 15-day export windows, annual auto-renewal; (3) **cannibalisation** - per-account pricing halves Ren's USCGT revenue (40 -> 20 bps) while leaving MS GIFT unchanged, so incumbents re-tier selectively; (4) **migration risk** - re-platforming their own clients risks the 3-customer concentration (85.8% of named receipts); (5) **assurance dependencies** - SOC reports scoped to existing systems; (6) **customer resistance** - sponsors just migrated (AEF 2026) will not move again soon; (7) **incentives** - minimum-touch ops *raise* a bps incumbent's margin, so they will copy those levers quietly without lowering price.

**Do not assume incumbents cannot transform.** Evidence of capacity: Vanguard Charitable spends $2-6M/yr on tech services; Fidelity $11.8M on consulting; Foundant has won 6 of 8 recorded CF migrations; Schwab rebranded to DAFgiving360; Ren has executed four acquisitions; TIFIN ships agentic AI. The incumbent's best move is not transforming the installed base but **launching a greenfield sub-brand** on modern infrastructure, migrating selectively, or **acquiring** the entrant (repo: six of six DAF-tech exits went to consolidators).

**Responses modelled.** Favourable to the entrant: Ren preoccupied with iPhi/DFX integration and CF attrition to Foundant; Foundant not in BPO; TIFIN focused on adviser distribution; captives are not buyers. Unfavourable: selective re-tiering and waived change orders at renewals (0-6 months); 'managed services' bundled on Stellar at marginal cost; Foundant adds BPO + continuous monitoring for all fund types (CFs prefer one system: Unbound EV-04); channel owners cross-subsidise admin from advisory fees; greenfield competitor or acquisition within 18-30 months. **Net:** the previous 'easily copied' verdict is too strong for the combination against multi-lineage incumbents and about right for each lever alone and for well-funded greenfield responses. The window is roughly 2-4 years, which must be enough to earn SOC history and measured unit cost.""")

sec("Limitations and evidence gaps", """1. **Value delivered is modelled, not observed.** Bottom-up cost uses the previous activity model (no time study; [A] parameters); top-down uses [A] replaceable shares. No sponsor cost-by-activity data is public.
2. **Donor-fee revenue** is realised only for Fidelity, RCF, JCF, CJP, NCF; others are schedule x realisation [E] (calibration n=3, range 0.38-0.68).
3. **DAF opex allocation by asset share** overstates DAF cost at CFs with large non-DAF endowments and understates it where DAFs are labour-intensive; BofA CGF 990 opex ($70,800) excludes trustee compensation netted elsewhere - its row is unreliable.
4. **Advisor-programme value** sees only the 990 vendor line; affiliate staff (e.g. Ayco, Stifel Trust) is invisible, so value is understated for software-only buyers.
5. **Service-quality value** (turnaround, errors, transparency) is not quantified; it can only be argued, not priced, until measured.
6. **No executed contract, design-partner term, implementation amount or equity arrangement** in DAF is public; search-snippet sources (Foundant POC migration, Blackbaud 10-K, NC ABLE) are quality C and were not read in full.
7. **Replication scores and time-to-match are analyst judgement** from public evidence; incumbents' internal architecture, budgets and plans are unknown.
8. **Same-model reasoning** throughout; prices and structures must be tested in owner-led buyer conversations quoting bps and $/account side by side.
9. Servicer contribution excludes company fixed cost; see previous study's fixed budget ($1.1-1.7M).""")

with open(f"{OUT}/report.jsonl", "w") as f:
    for s in SECTIONS:
        f.write(json.dumps(s) + "\n")
print("ok", len(evidence), len(assumptions), len(OPP), len(REP2) + len(RESP), len(SECTIONS))
