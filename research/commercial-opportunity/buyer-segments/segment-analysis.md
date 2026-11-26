# Buyer segments: who might pay, for what, and why they might not

**Date:** 2026-11-20. **Status:** segment hypotheses built from 78 prospect profiles. These come from public sources and the repository. **No buyer has been interviewed.**

**Profiles:**
- [`prospects-sponsors.csv`](../../../data/commercial-opportunity/prospects-sponsors.csv): PS01–PS23. Notes in [sponsors-notes.md](../prospect-profiles/sponsors-notes.md).
- [`prospects-wealth.csv`](../../../data/commercial-opportunity/prospects-wealth.csv): PW01–PW24. Notes in [wealth-and-entrants-notes.md](../prospect-profiles/wealth-and-entrants-notes.md).
- [`prospects-other.csv`](../../../data/commercial-opportunity/prospects-other.csv): PV01–PV31. Notes in [vendors-investors-other-notes.md](../prospect-profiles/vendors-investors-other-notes.md).

**Evidence references:**
- INV### refers to [the Phase 0 inventory](../evidence/phase0-repository-inventory.md).
- DS## refers to [demand signals and process economics](../market-validation/demand-signals-and-process-economics.md).
- CP## refers to [competition and pricing](../competitive-landscape/competition-and-pricing.md).

## Segment table

| Segment | Pain (evidence) | Who holds budget [I] | Ability to pay (evidence) | Triggers | Current alternatives | Fit | Main disconfirming evidence |
|---|---|---|---|---|---|---|---|
| **A1 National sponsors (affiliated: Fidelity, DAFgiving360, Vanguard Charitable)** | Parent-run technology. Vanguard Charitable/Give Interactive go-live not observed (INV015) | Parent firm (FMR, Schwab, Vanguard) | Very high: McKinsey $11.8m paid by Fidelity Charitable (FY2025); Slalom $2.06–3.74m a year at Vanguard Charitable (TY2021–24) (CP) | Platform changes, regulation | Large consultancies, parent IT | Low | Purchasing decisions are out of reach |
| **A2 National sponsors (independent: NPT, AEF, RCF, NCF)** | NPT costs $419 per grant (INV006); thin margins (RCF +0.8%); 2.2 months of reserves (INV012) | CEO, COO, CTO. A CTO appointed in March 2026 at NPT is verified on an official page (PS01) | Moderate. NCF paid Ren $2.50m (INV047) and Accenture $0.8m (CP) | §4966 final rule; vendor renewal | Vendors' own services; Accenture-type firms | Medium (niche work) | RCF is run by Ren and does not choose its own vendor (PS03) |
| **A3 Mid-size community foundations ($250m–$5bn)** | Admin fees 1.7–4.7× the nationals' (INV037); cost per DAF dollar up 21% (INV044); migrations freeze grants for 3–5 weeks (DS) | CEO, COO, CFO; board technology or finance committee | **Best visible:** median IT $455k and outside services $1.29m for the $250m–1bn band (DS spend, reproducible); vendor fees $118k–416k (INV032–INV033) | iPhi attrition, renewals, leadership change (Arkansas), donor surveys | EPAM, Slalom, Clarity Partners; vendor implementation; peer referral | **High** | No public RFPs; the migration wave is largely complete (PS notes) |
| **A4 Small and tail sponsors (under $250m)** | Cost pressure | Executive director | Very low: median IT $81 (under $10m) and $42k ($10–50m) (DS spend) | — | Foundant module; peers | Low | "No intervention" wins in 87–100% of model runs (DS) |
| **A5 Faith and single-issue sponsors** | Platform choices (Thrivent's Ren spend up to $479k, PS19); JCF portal changes (PS17) | CEO, COO | Moderate. Already pays outside advisers: PhilanthroCorp $623k, Excellence in Giving $568k (INV048, unvalidated) | Platform migration; growth | Faith-sector advisers | Medium | Some (Dechomai, Daffy, Endaoment) are unlikely buyers (PS20–PS23) |
| **B1 Wirehouses and private banks** | Run adviser-retaining programmes already (MS GIFT, BofA, Goldman, J.P. Morgan) | Philanthropic-services heads; product | High but self-sufficient | Rarely | In-house; Ren | Low | No evidence of outside DAF advisory purchases |
| **B2 Independent broker-dealers, regional banks, trust companies** | Dated decisions: LPL–Commonwealth conversion in Q4 2026 (PW06); Stifel Ren spend up to $801k (PW08); Raymond James on iPhi (PW07) | Head of wealth products or philanthropy; platform committee | Moderate–high | Mergers, platform renewals, launches (Regions guide May 2026, PW24) | Sponsor and vendor sales teams (free) | **Medium-High** | Access; free advice from vendors |
| **B3 Large RIAs and aggregators** | Mercer in-house Philanthropic Services launch on 2026-11-10 (PW11); no DAF programme found at Creative Planning, Mariner, Focus or CAPTRUST | Philanthropic-services head | Moderate | New practice launches | Kitces/XY, sponsor advisor teams | Medium | Most use national sponsors' free advisor programmes |
| **B4 Wealthtech and new entrants** | SEI two stacks (PW20); Vanguard–Altruist (INV066); TIAA–Charityvest (INV065) | Product and partnerships | Moderate | Launch decisions | In-house product teams | Medium | They partner with vendors directly |
| **C Technology vendors** | Need evidence for fundraising or positioning (Chariot, no raise since its 2024 Series A, PV03) | CEO, CPO, strategy | Moderate | Fundraising, launches | In-house; PR firms | Medium (research/intel) | **Conflict with independent assessment** (PV notes) |
| **D Investors and lenders** | Exit windows 2026–29 for Foundation Source, Benevity, Bonterra, Ren [I] (INV100) | Deal teams; operating partners | High per deal | Deals | Generalist due-diligence firms; expert networks | Medium | Deal releases name only banks and law firms (PV) |
| **E Nonprofits and universities** | DAF gift identification and reconciliation; 41.2% of top recipients show a DAF option (INV106) | Advancement services | Low–moderate | — | Chariot, CRM vendors | Low | Not the payer for sponsor-side work; budgets unknown |
| **F Education providers** | Curricula omit operations, fees and technology (DE046, DE057); AFP RFP in Nov 2024 (INV108) | Programme directors | Low | Curriculum refresh | Sponsor-funded content | Low (credibility) | Sponsor-funded education ecosystem |
| **G Adjacent** (CPAs, estate lawyers, planned-giving software, noncash administrators) | Complex gifts; planned-giving integration | Practice leads | Low–moderate | — | Crescendo, PG Calc, FreeWill | Low | No DAF-specific purchasing evidence |

## Reading [I]

- **The most promising buyers combine three things:** a discretionary budget, a dated platform or programme decision, and decision-making held in-house rather than at a parent firm. That means:
  - **A3** mid-size community foundations (53 community foundations at $250m–10bn plus 10 religiously affiliated sponsors in FY2024 [C]; the 43 CFs in the $250m–1bn band from the DS spend table plus larger independents);
  - **A5** faith and single-issue sponsors;
  - **B2** independent broker-dealers and regional banks.
- **Investors (D) and vendors (C)** are better served by OF3 research and the OF4 diligence module, with explicit conflict rules.
- **The largest asset pools (A1, B1)** are poor initial targets because their purchasing sits elsewhere. This contradicts assumption A8 in [assumption-tests.md](../clarity-edf-analysis/assumption-tests.md).
