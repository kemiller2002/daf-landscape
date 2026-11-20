# Commercial offerings: design, pricing hypotheses and pilots

**Date:** 2026-11-20. **Status:** hypotheses. **Nothing here is validated demand.**
- Prices are **testing hypotheses** taken from the benchmarks in [competition-and-pricing.md](../competitive-landscape/competition-and-pricing.md) §5. They are not observed DAF prices.
- Scores and their basis are in [`opportunity-scores.csv`](../../../data/commercial-opportunity/opportunity-scores.csv). The sensitivity analysis is in [`opportunity-sensitivity.csv`](../../../data/commercial-opportunity/opportunity-sensitivity.csv), produced by [`scripts/commercial_opportunity_scoring.py`](../../../scripts/commercial_opportunity_scoring.py).

**Evidence references:**
- INV### refers to [the Phase 0 inventory](../evidence/phase0-repository-inventory.md).
- DS## refers to [demand signals and process economics](../market-validation/demand-signals-and-process-economics.md).
- CP## refers to [competition and pricing](../competitive-landscape/competition-and-pricing.md).
- PS/PW/PV refer to prospect rows in [`data/commercial-opportunity/`](../../../data/commercial-opportunity/).

## Shared assets Echelon already has (capability fit)

Everything below comes from the repository:
- A 1.6m-word public-evidence base with validation registers.
- 990 contractor and vendor-footprint datasets.
- Evidence Quadrants for 43 providers.
- A buyer-neutral platform evaluation protocol ([platform-evaluation-protocol.md](../../platform-evaluation-protocol.md)).
- A migration runbook ([migration-runbook-2026.md](../../migration-runbook-2026.md)).
- An AI governance failure-mode register.
- A draft open DAF grant record schema.
- The process-economics model.

What Echelon lacks:
- references;
- delivery track record;
- buyer relationships;
- tested pricing.

## OF1 Independent DAF technology assessment and vendor selection (rank 1 in every scenario but recurring-focus)

| Field | Design |
|---|---|
| Target buyer | Community foundations and faith or single-issue sponsors with $250m–$5bn of DAF assets. Roles: COO, CFO, VP operations or technology, often with a board technology committee [I] |
| Problem | Vendor choice and renewal are made without comparative evidence. No analyst covers DAF platforms (INV094). Migrations freeze grantmaking for 3–5 weeks and can lose donor history (DS migrations; INV026). Ren's iPhi lost 6 of 57 sponsors in 2023–26 (INV035) |
| Deliverable | Requirements baseline. Market scan of 4–6 platforms with documented-evidence scoring (no invented scores). Total-cost model from comparable 990 vendor payments. Contract-term checklist (export, transition, SOC scope). Reference-check script. Recommendation memo. Optional renewal-negotiation benchmark |
| Expertise | DAF operations; platform evidence; procurement; contract terms |
| Effort | 4–8 weeks, about 120–250 hours [I] |
| Price hypothesis | $35k–90k fixed. Anchors: BerryDunn $107–118k selection and $175k needs assessment (public-sector work: a 2019 village ERP and a 2023 health-records assessment, not DAF); Kitces scan $19.5–39.5k; GSA principal median about $227/h (CP) |
| ROI hypothesis | Ren/Stellar fees at community foundations run $118k–416k a year (INV032–INV033), and reach $801k at Stifel Charitable. A 10% better contract saves only $12k–42k a year, so it covers a $35k–90k fee only over a multi-year term or with an avoided failed migration [I, unquantified] |
| Differentiation | Vendor-neutral (no vendor revenue). Evidence base across 43 providers. Contract and migration test library |
| Risks | Lumpy, trigger-driven demand. The recent migration wave is largely finished (PS notes). Incumbent IT consultancies (EPAM, Slalom, Clarity Partners) are already paid (DS spend). Vendors may refuse cooperation |
| Recurring potential | Low. Annual renewal benchmarks and monitoring add some |
| Pilot | One mid-size sponsor facing renewal or migration. Discounted fixed fee in exchange for a reference and permission to publish anonymised findings |
| Evidence needed before launch | At least 3 of 6 sponsor interviews report outside spending on selection or migration in the last 3 years (Q3/Q4), and one names a decision within 12 months (Q1/Q13) |

## OF6 Platform migration assurance and data-continuity testing (rank 2; candidate to merge with OF1)

| Field | Design |
|---|---|
| Target buyer | Sponsors mid-migration or contracting: those leaving Ren iPhi, NPact DonorCentral sunset clients (INV086), Give Interactive go-lives (PS11, PS19); wealth programmes consolidating platforms (LPL–Commonwealth, PW06) |
| Problem | Grant freezes, lost history and broken donor exports. Vendors test their own migrations |
| Deliverable | Acceptance-test plan from the repository's migration runbook (20 synthetic cases). Data reconciliation (balances, grant history, successor designations). Cut-over readiness review. Post-go-live check at 30 and 90 days |
| Effort | 3–6 weeks [I] |
| Price hypothesis | $25k–75k |
| ROI hypothesis | Avoided freeze days and donor-service failures; board assurance [I]. Not quantified |
| Differentiation | Runbook already written; independence from the migrating vendor |
| Risks | Short engagement window; vendors may resist outside testing; demand tied to renewal cycles |
| Pilot | Offer it as an add-on to OF1, or to a sponsor identified with an upcoming go-live, after interviews |
| Evidence before launch | At least 2 sponsors confirm a migration problem cost them money or donors (Q7/Q10) |

## OF3 DAF market-intelligence subscription (rank 3; rank 1 under recurring-focus weights)

| Field | Design |
|---|---|
| Target buyer | Vendors (product and strategy), investors and lenders (deal teams, portfolio operations), wealth-platform product heads, larger sponsors' strategy staff |
| Problem | No analyst covers DAF platforms (INV094). Market data is sponsor-funded and aggregate (DAFRC, NPT), and vendor claims are hard to check (for example Daffy's $2bn against $334m on its 990, INV083) |
| Deliverable | Quarterly briefing covering: 990 vendor-footprint refresh; migrations and attrition watchlist; deal and financing tracker; regulatory tracker; AI product census. Annual DAF infrastructure report. Institutional tier with analyst calls |
| Price hypothesis | Individual or adviser tier $400–1,500 a year (Inside Philanthropy and Candid band); institutional tier $5k–25k a year (below Cerulli's $21.5–22k single report; PitchBook seat band) (CP) |
| ROI hypothesis | Replaces ad-hoc research hours; feeds deal theses [I] |
| Differentiation | Validated 990-based datasets and change monitoring the repository already maintains (watchlist, 990 harvest) |
| Risks | **Independence conflict** if vendors are both subjects and subscribers. Mitigation: subscription access only, no paid placement or ratings, and disclosure of subscribers by category. Small buyer universe (fewer than 100 institutions) [I] |
| Recurring | High |
| Pilot | Publish one free quarterly briefing. Offer the institutional tier to 10 named organisations from the PV and PW rows **after authorisation**. Measure conversion |
| Evidence before launch | At least 5 institutions say they would pay at least $5k (Q19), or pre-orders |

## OF5 Wealth-manager DAF programme strategy and integration (rank 4–6)

| Field | Design |
|---|---|
| Target buyer | Broker-dealers, regional banks, trust companies and large RIAs deciding sponsor and vendor, or launching or consolidating programmes. Examples: PW06 LPL, PW08 Stifel, PW07 Raymond James, PW11 Mercer, PW20 SEI, PW24 Regions |
| Problem | Choosing among referring clients to a national, white-labelling on a sponsor of record (RCF/Ren, GiveClear/TIFIN, Charityvest/Foundation Source, Endaoment) or forming an affiliated charity. Designing fees (0–2% observed, INV060) and data flows that keep the adviser relationship |
| Deliverable | Options analysis; sponsor-of-record and vendor comparison; fee and conflict design (Reg BI and fiduciary disclosure, 2023 proposed-rule exposure); integration architecture; launch plan |
| Price hypothesis | $25k–100k project. Kitces lists $10–50k projects and $800–1,000/h (CP); larger firms higher [I] |
| Differentiation | Adviser-controlled design; cross-vendor evidence; regulatory currency |
| Risks | Hard access to large firms. Sponsors and vendors give this advice free during sales. Conflict optics around adviser fees on charitable assets |
| Pilot | One mid-size RIA or regional bank after interviews |
| Evidence before launch | At least 2 of 3 wealth interviews report a programme decision under way and outside-adviser use (Q15/Q16) |

## OF4 Investor DAF commercial and technical diligence module (rank 4–5)

| Field | Design |
|---|---|
| Target buyer | PE and growth investors, lenders, strategic acquirers. Their commercial and technical due-diligence providers act as the channel (PV15–PV21) |
| Problem | DAF-specific questions generalists cannot answer: sponsor-of-record dependence, customer concentration (Ren: 85.8% of named 990 receipts from three customers, INV056), attrition, contract terms, regulatory exposure |
| Deliverable | A DAF module inside a generalist due-diligence report: customer map from 990s, attrition, competitive position, regulatory scenarios, technology risk checklist |
| Price hypothesis | $25k–75k as a module (low confidence; CP) |
| Risks | **Conflict:** diligence on Ren for a buyer while also assessing Ren for sponsors. Mitigation: deal-level conflict checks and an information barrier. Deal timing unpredictable. Expert-network fees are lower |
| Pilot | Register with 1–2 expert networks; approach a generalist due-diligence firm as a subcontract bench (after authorisation) |
| Evidence before launch | At least 1 diligence practitioner confirms paying for sector specialists on comparable deals (Q17) |

## OF2 Operating-model and AI-readiness review (rank 6–7)

| Field | Design |
|---|---|
| Target buyer | Sponsors with $250m or more in DAF assets |
| Problem | Pressure to "do AI" against thin measured value. Redesign beats AI in most processes (DS process table). The rule that AI may add a flag but never clear one ([ai-governance-failure-modes.md](../../mission-2026-11-14/ai-governance-failure-modes.md)) |
| Deliverable | Process inventory with cost per grant and exception mapping; a "redesign, automate, AI or leave alone" decision per process; AI governance policy; one prioritised pilot (complex-asset intake or non-standard due diligence) |
| Price hypothesis | $35k–90k (CP) |
| Risks | Crowded with generic AI consultancies (St. David's AI-roadmap RFP, DS RFPs). The value pool is small at sub-national sponsors |
| Positioning | Sell as a module of OF1 ("assessment and redesign"), not standalone. The repository evidence argues against leading with AI |

## Discovered offerings (lower ranked)

| ID | Offering | Why ranked lower | Keep or reject |
|---|---|---|---|
| OF7 | Sponsor operating benchmark (data cooperative: turnaround, exceptions, cost per grant) | No current evidence sponsors will share data; slow to revenue; CF Insights is a peer | **Keep as a later recurring product.** Seed it from OF1 engagements with consent |
| OF8 | Buyer-side second opinion for nationals alongside large consultancies | Fidelity Charitable paid McKinsey $11.8m in FY2025 (verified in the 990 harvest), but decisions sit at parent firms and access is low | Opportunistic only |
| OF9 | Complex-asset intake decision-support software | Fails R8: no repeat-buyer evidence; incumbents (Dechomai/Charitable Solutions, NCF); valuation liability | **Reject now.** Revisit if OF1 or OF2 engagements show the same pain at 3 or more buyers |
| OF10 | Operations and technology education partnership | Low revenue; credibility value | Keep as marketing (one webinar or case study), not a revenue line |

## Deliberately rejected

| Opportunity | Reason |
|---|---|
| A competing DAF certification | No evidence of unmet demand (DE068, DE070); trademark-heavy incumbents |
| Standalone AI grant-review software | Routine vetting is deterministic; the AI value pool is thin; AI cannot clear liability (§2 of [assumption tests](../clarity-edf-analysis/assumption-tests.md)) |
| A long-tail sponsor SaaS or administration platform | Sub-$250m sponsors show "no intervention" wins in 87–100% of model runs; median IT spend $81–42k (DS); the repository advises against it (INV041) |
| Forming a DAF sponsor or holding donor funds | Capital, regulation, and conflict with independence (report §8; synthesis D) |
| Paid vendor ratings, sponsored placements or Forum Premier sponsorship | Destroys the independence that is the core asset |
| Vendor-paid "independent" assessments of the same vendor | Conflict; violates the R6 rejection criterion |
