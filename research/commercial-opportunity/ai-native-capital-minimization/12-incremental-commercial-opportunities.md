# 12: Incremental commercial opportunities

**Pass:** COM (parts 2-3), integrated in sequences D and G (model section 9). **Data:** [`opportunities.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/opportunities.csv) (11 capabilities).

**Integrator conclusions**
- **Most standalone opportunities have potential, not demonstrated, demand.**
- Where demand is demonstrated, the products are commoditised, contested or risky as disconnected products:
  - charity verification data;
  - disbursement, which raises a money-transmission question;
  - donor portals, which would sit on incumbents' ledgers;
  - migration.
- **Two have paid precedents and are also platform components:** migration/import tooling and the eligibility (charity verification) service. Build these first.
- **Narrow entry does not reduce capital in the model.**
  - Sequence D needs a $7.0M equity need; sequence G needs $6.9M.
  - A non-custodial service still carries SOC 2, insurance, compliance consulting and support from its own launch.
  - At an assumed $40k per sponsor, six sponsors earn $240k a year against about $0.6M of fixed non-personnel cost.
  - Its value is **evidence**: price, recall of charity matching, buyer behaviour. Its value is not funding.
- **Customer-funded development is limited.**
  - Implementation fees exist (TIFIN's SEC filing, Ren's product descriptions) but amounts are not public.
  - A realistic $100-500k prepaid implementation covers onboarding, not the platform build.
  - A charitable sponsor that pays above fair value for vendor-owned IP raises a private-benefit risk.
  - No public DAF design-partner prepayment or equity deal was found.

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Part 2: incremental commercial opportunities

Full table: `opportunities.csv` (11 rows). Demand label: **demonstrated** = someone is observed paying for this capability (repo or public source); **potential** = only a hypothesis or adjacent product.

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

**Architectural risk.** Each standalone product sold onto another vendor's ledger forces integrations with iPhi/DFX, Foundant, Blackbaud and in-house systems - each a separate data model - and creates evidence about records the company does not control. Selling disconnected products risks building five integration businesses instead of one platform. The two products whose external version **is** the platform component (eligibility service, migration/import) are the only ones that validate economics (onboarding cost, exception rates) while building shared assets. Operational intelligence is the cheapest way to test buyer demand but validates nothing about productivity.

## Part 3: customer-funded development

**Evidence (public/repo only).**
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

**Risks overall:** concentration (one partner = most revenue; prior study: margin 48% -> 3% if anchor lost); customisation debt; partner procurement/board timelines (6-12 months); charitable-purpose constraints on how a sponsor may spend; IP and data-rights disputes (iPhi MSA reserves vendor rights to anonymised data); partner churn before payback. Customer-funded development can reduce, not remove, the $2.7-11M capital range: a realistic prepaid implementation ($100-500k) covers onboarding, not the platform build.
