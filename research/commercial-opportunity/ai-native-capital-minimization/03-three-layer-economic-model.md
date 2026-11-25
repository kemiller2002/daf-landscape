# 03: Three-layer economic model

**Pass:** LYR (part 1), integrated in model section 7. **Data:**
- [`layer-costs.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/layer-costs.csv) (43 lines);
- [`entity-options.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/entity-options.csv);
- [`layer-summary.json`](../../../data/commercial-opportunity/ai-native-capital-minimization/layer-summary.json).

**Integrator conclusions.** Model section 7, at $1B in 5 sponsors and 50 minutes, MSP platform base:

| Question | Answer |
|---|---|
| Incremental annual cost of servicing if Unbound exists | about **$2.0M** (F5, $1B; the pass gives $2.29M, $1.22-5.18M, at $1.5B / 10,000 accounts) |
| Incremental annual cost of Unbound if Echelon exists | about **$0.7M** with the minimum product at 1.5x; **$1.8M** on the LYR full-scope base (the pass gives $2.26M, $1.03-5.80M) |
| Servicing standalone vs incremental | standalone carries about $0.9-1.0M a year more (build amortisation, Echelon share and licence, maintenance gap) |
| Consolidated A+B+C at $1B | a loss of about $1.0M (MSP base) to $2.1M (full-scope base): the platform has one customer |

- **Shared Echelon resources are not free.** Production reliance creates about $0.27M a year of Echelon cost (second maintainer, component security review, licence programme, licensor insurance) against about $0.13M a year of verified reuse saving.
  - The integrated base charges 45% of a $300k Echelon capability plus a $60k licence.
  - The LYR base charges $0.27M plus 90%.
- **Entity structure** (research level, not legal or tax advice):
  - Run as one entity with priced internal charges now.
  - Move servicing to a subsidiary at the first live-money signing (liability ring-fence, SOC 1 boundary).
  - Separate Echelon only when it has a second commercial user.
  - Transfer prices move profit between layers and cancel on consolidation.
- **Two bases, not optimistic and conservative (ADV2-002).** "MSP base" covers the minimum servicing product with 1-2 maintaining engineers. "Full-scope base (LYR)" covers Unbound's full scope with a technical lead and three engineers. The truth for a first release lies between them and depends on scope discipline.

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## LYR summary: three-layer economics, assumptions, requirements and the cost of being wrong

**Group LYR, 2026-11-25. Status: theoretical research; same-model reasoning, not independent validation. No legal or tax advice.**

**Reference scenario R** (used throughout): 5 sponsors, 10,000 accounts, $1.5B average assets ($150k balance), AI-native steady state, 20 bps = **$3.00M revenue**. The previous study's F# model, re-run here, gives a servicing operating cost of **$2,916,936** at R (profit $83,064) [M].

| Question | Answer (base, low-high) |
|---|---|
| Incremental cost of a servicing operation if Unbound exists | **$2.29M ($1.22M-$5.18M)/yr** fully allocated (direct + causal share of corporate cost) |
| Incremental cost of Unbound if Echelon exists | **$2.26M ($1.03M-$5.80M)/yr** (servicer is the only customer) |
| Echelon cost caused by Unbound's commercial reliance | $0.27M ($0.11M-$0.41M)/yr (second maintainer, component security, licence programme, licensor insurance) |
| Echelon's verified saving to Unbound | $125k ($0k-$310k)/yr; **net of the cost-plus licence charge: -$225k base**, positive only in the low case ($181k) which needs measured >=2x agent throughput |
| Three-layer group cost at R | **$4.99M ($2.43M-$11.70M)** vs $3.00M revenue (base loss $1.99M) |
| Group break-even at 20 bps (5 sponsors, captive platform) | **$2.3-2.8B** base by balance ($500k-$150k); $1.5-1.9B low; $4.3-5.1B high [M]. Previous study: $1.1-1.5B operating, $1.8-2.3B fully loaded |
| Founder opportunity cost inside the base | $195k/yr (economic, not cash) |

**Five most consequential findings**
1. **The servicing layer alone works at R; the stack does not.** Servicing's incremental cost ($2.29M) leaves ~$0.71M toward a platform and foundry whose fully allocated cost is $2.70M. A captive platform needs ~28,724 funds at Unbound's $91/fund to cover its cost (~31,471 with licence sales cost), i.e. ~19-21k external funds beyond the servicer's 10k.
2. **Shared Echelon resources cost more than they save on current evidence.** Production reliance on single-maintainer, PolyForm-NC, largely agent-authored components creates ~$0.27M/yr of Echelon cost (base) against ~$0.13M/yr of verified reuse saving. The sign flips only if agent-assisted throughput is measured at >=2x on the DAF codebase.
3. **The value of Unbound to servicing is the redesign, not the software.** Without a platform that supports board-delegated straight-through handling, the same servicer costs +$0.94M/yr (AI-enhanced) to +$2.70M/yr (conventional) at R [M]. That value rests on unmeasured levers (Unbound EV-02) and on sponsor boards and auditors accepting deterministic release.
4. **Most conventional assumptions are not the binding constraint.** Of 52 assumptions registered, 17 have a replacement judged better (mostly small: December deferral, EFT default, lazy renewal, generated evidence), 32 are unproven and 2 are worse. Legal obligations, independent assurance and SoD remain; the large swings are platform build/engineering staffing, delegation and measured minutes.
5. **Stage the investment.** A gate sequence (buyer + licence + counsel + auditor approach; then design partner + instrumented shadow replay + engineering spike; then build) lets the owner stop at ~$0.15M or ~$0.75M instead of the $2-3M+ sunk at a failed go-live. Every failure in the catalogue except security incidents and market falls has a detection point before build spend.

**Does a fundamentally different company emerge?** Not at R on present evidence. The AI-native servicing layer is materially cheaper than a conventional one (if measured), but once the platform and Echelon are charged at cost the group needs more assets than the previous study's fully loaded case. A different company emerges only if (a) Unbound earns external licence revenue on ~20k+ funds, or (b) measured agent productivity brings the platform to the low case (~$1.0M/yr fully allocated). Both are testable early and cheaply.

## Method, definitions and double-counting rules

- **Layers.** A Echelon Foundry (shared engineering, reusable components, governance tooling, dev infrastructure, component security, monitoring, organisational administration). B Unbound (DAF-specific build, maintenance, integrations, platform operations, platform assurance, licensing in and out). C DAF servicing (acquisition, sponsor relationships, financial operations, grant administration, service, servicing assurance).
- **Standalone** = annual cost if the layer existed alone and had to buy or build what the other layers supply, including its own corporate floor. Standalone figures are **not additive**: the difference between the sum of standalone costs and the group cost is the duplication a split would create.
- **Incremental** = annual cost the group incurs by adding the layer when the other two exist (avoidable cost). For A, incremental includes the cost caused by B's production reliance; for B, it is net of verified Echelon reuse; for C, it excludes the platform (B supplies it).
- **Fully allocated** = incremental direct cost + causal share of shared corporate cost (keys in layer-costs.csv) + pro-rata contingency. Fully allocated costs sum exactly to the group total (checked: residual $0).
- **No double counting.** (1) The principal who maintains Echelon cannot also be Unbound's full-time accountable technical lead: the group carries 1.5 senior technical FTE (A01 0.5 + B02 1.0). (2) Transfer charges (T01-T03) are shown for entity P&Ls but eliminate on consolidation. (3) The integration engineer step cost moves from C to B (B04) and is removed from C06. (4) Payment rails are passed through (transfer, not saving). (5) Sponsor-retained work and sponsor entity costs are excluded and never counted as eliminated.
- **Sources.** Previous study cost register, staffing models and F# model (re-run at R with `dotnet fsi` against the published DLL: `work/fsx/ref.fsx`, `work/fsx/be.fsx`) [M]; Unbound parameters and convergence clauses [S]; Echelon component repos measured with `git log`/`git ls-files` [M]. Numbers marked [A] are analyst placeholders.
- **Scripts:** `work/build_layers.py` (layer-costs.csv, summary), `work/registers.py` (other CSVs), `work/report.py` (this file).

## Part 1: layer cost structures at R

| Layer | Standalone | Incremental direct | Fully allocated |
|---|---|---|---|
| A Echelon Foundry | $0.35M ($0.24M-$0.69M) | $0.40M ($0.17M-$0.66M) | $0.43M ($0.19M-$0.72M) |
| B Unbound | $2.87M ($1.56M-$6.57M) | $2.13M ($0.96M-$5.51M) | $2.26M ($1.03M-$5.80M) |
| C DAF servicing | $4.57M ($1.65M-$9.87M) | $2.07M ($1.11M-$4.73M) | $2.29M ($1.22M-$5.18M) |
| Shared corporate (audit/accounting, insurance, counsel, per-FTE, compliance tooling) | | $0.27M | allocated by key |
| Contingency 7.5% | | $0.12M | pro rata |
| **Group** | (not additive) | | **$4.99M** ($2.43M-$11.70M) |

**Layer A, Echelon Foundry.** Standalone ~$0.35M is mostly the principal's market cost ($222k, economic). Measured facts: 26 component repos, 9,045 commits since 2025-07-07, one human author plus AI agents (majority of commits carry Claude co-author trailers), ~833k lines in code-type files including tests and generated output; 22 repos PolyForm Noncommercial, 3 MIT, 2 without a licence file [M]. Nothing runs in production (ECH-21). Incremental cost rises to ~$0.40M because a regulated commercial dependant needs a second maintainer ($189k), component security review ($25k), a licence programme with escrow ($25k) and licensor insurance ($35k): **$0.27M/yr caused by B**.

**Layer B, Unbound.** Build amortisation dominates: $5M ($3-15M) over 5 years = $1.0M/yr standalone [S Unbound parameters]; base -8% with Echelon reuse ($0.92M), low $0.30M only if a 2x agent throughput gain is measured. Engineering run: technical lead + 3 engineers + 1 per-sponsor integration engineer (base). The previous study's Model B carried only a lead and one engineer, which report 03 already flagged as implying an existing platform. Hosting, assurance (SOC 2, pen test, vCISO, tech E&O) and data subscriptions are not reduced by any Echelon component.

**Layer C, servicing.** People are the cost: CEO/relationships, controller, core ops, 5 added ops FTE, ops manager, implementation analyst and fund accountant at R [M]. Plus SOC 1 Type 2, crime insurance, compliance consultant, sales ($250k), onboarding amortisation ($105k) and servicing-specific platform features ($60k/yr). Standalone (no Unbound) adds a platform ($0.32-1.29M: licensed incumbent software at $32-129 per DAF-year, or the previous study's in-house platform with a narrow $0.72M build) and, if that platform cannot support the redesign, a handling penalty of $0.94M (AI-enhanced) to $2.70M (conventional) [M].

**Cash vs economic.** Base group cash cost $4.79M vs economic $4.99M: the $195k gap is founder opportunity cost (Echelon principal assumed unpaid; CEO at Model A cash $116,255 vs $200,142 market). Cash plans may use the lower figure; break-even and pricing must use the economic one.

## Part 1: shared costs, allocation keys and why shared Echelon resources are not free

| Shared line | Base | Key | A / B / C share |
|---|---:|---|---|
| S01 audit, fractional CFO, bookkeeping, tax | $80,000 | transactions, entity complexity | 5% / 25% / 70% |
| S02 cyber $5M, D&O, EPLI, GL | $47,000 | records held, payments exposure, headcount | 5% / 35% / 60% |
| S03 outside counsel | $45,000 | matter coding | 15% / 25% / 60% |
| S04 per-FTE overhead | $64,067 | headcount A 1.5 / B 5 / C 11 FTE | 9% / 29% / 63% |
| S05 compliance automation, IR retainer, G&A | $37,700 | controls in scope | 10% / 45% / 45% |
| S06 contingency | $115,814 | direct cost | pro rata |

Keys are [A] causal drivers to be replaced by metered drivers (CNV-ECO-001: events, storage, compute, AI inference; work-item hours for people). **Echelon is charged by two keys:** dependency-caused cost goes 100% to B (A03, A05, A08, A09), and a usage share (base 40%, 20-80%) of Echelon running cost (principal time, agent compute, CI, entity admin) by work-item hours on components in B's SBOM. Leaving these out is the Clarity 'Burden Externalization' pattern the previous study warned about (ECH-01, ECH-19).

## Part 1: internal licence and service charges (transfer pricing, research level)

| Charge | Cost-plus | Market-based | Observation |
|---|---|---|---|
| T01 Echelon -> Unbound component licence | $0.35M ($0.13M-$0.67M)/yr (B-caused cost + 20/40/80% usage share, markup 5/8/10%) | none observable: commercial terms 'forthcoming' (forma README:162-164) | A licence of intangibles between commonly controlled parties should yield income 'commensurate with the income attributable to the intangible' (26 U.S.C. §482). |
| T02 Unbound -> servicing platform charge | $2.82M ($1.21M-$7.12M)/yr | T03: $0.49M / $0.91M / $2.29M (Unbound's own $49/$91/$229 per fund x 10,000) | Incumbent software band $32-129 per DAF-year (Unbound 05 §3a) is the external comparable; $0.32-1.29M at R. |

**Reading.** At R the servicer is the platform's only customer, so a cost-plus charge loads ~$2.8M onto a $3.0M revenue servicer; a market-based charge ($0.91M) leaves the loss in Unbound instead. **The transfer price moves the loss between entities; it does not change the group loss ($1.99M base).** The services cost method (no markup) applies only to services that do not 'contribute significantly to key competitive advantages, core capabilities, or fundamental risks of success or failure' (26 CFR 1.482-9(b)); platform engineering and core IP licensing look unlikely to qualify, so a markup or a profit-split style method would be expected. This is a research reading of public text, not tax advice; counsel and a tax adviser must decide.

**External revenue.** Servicing fees $3.0M at R. Unbound external licence revenue is $0 at R; 25,000 external funds at $91 would add $2.28M but needs sales ($250k) and SOC 2 for licensees. Echelon external licence revenue: no terms, price or licensee observed ($0). Note: PolyForm NC permits use 'by any charitable organization ... regardless of the source of funding' (forma/LICENSE:65-70), so a DAF sponsor that self-hosts may not need a commercial Echelon licence at all; a commercial servicer is not obviously covered. That limits Echelon's own licence market [research reading].

## Part 1: incremental answers

**Incremental cost of a servicing operation if Unbound exists: $2.29M ($1.22M-$5.18M)/yr at R.** Composition (base): servicing people $1.44M (CEO, controller, core and 5 added ops staff, step roles, December peak), servicing non-personnel $0.14M, sales $0.25M, onboarding amortisation $0.105M, servicing platform features $0.06M, external variable $0.07M, causal share of corporate and contingency ~$0.22M. Against $3.0M revenue, servicing contributes ~$0.71M/yr toward platform and foundry. A standalone servicer (no Unbound) costs $4.57M base because it must buy or build a platform and may lose the redesign.

**Incremental cost of Unbound if Echelon exists: $2.26M ($1.03M-$5.80M)/yr at R.** Of this, build amortisation is $0.92M and engineering $0.93M (lead, 3 engineers, integration engineer). Echelon reduces it by $125k base ($310k low, $0 high) and adds the T01 charge $351k base. **Net, Echelon makes Unbound $225k/yr more expensive at base** and $181k/yr cheaper in the low case.

**Break-even of the three-layer group at 20 bps** (previous model, Model B servicing, AI-native, 5 sponsors, plus the layer fixed extras over the model at R) [M]:

| Average balance | Operating (model only) | Previous fully loaded (+$1.25M) | Layers low (+$0.61M) | Layers base (+$2.07M) | Layers high (+$5.51M) |
|---|---|---|---|---|---|
| $150k | $1.46B | $2.29B | $1.90B | $2.82B | $5.08B |
| $300k | $1.20B | $2.08B | $1.62B | $2.50B | $4.54B |
| $500k | $1.14B | $1.83B | $1.50B | $2.29B | $4.29B |

Rule of thumb: each $100k/yr of fixed cost adds ~$65M of break-even assets at 20 bps (100,000 / (0.0020 x 76.7% contribution margin at R)) [D].

## Part 1: cost centre vs business unit vs separate legal entities

| Option | Structure | Added admin $/yr (base) | Assessment |
|---|---|---:|---|
| EO-LYR-01 | Cost centres in one legal entity | 0 | acceptable only as a pre-revenue phase |
| EO-LYR-02 | Business units in one legal entity | 20000 | recommended interim structure if a split is planned |
| EO-LYR-03 | Two entities: Echelon IP company + one operating company (Unbound + servicing) | 60000 | reasonable once Echelon has a second commercial user |
| EO-LYR-04 | Three entities: Echelon IP co, Unbound software co, servicing co | 130000 | premature at R; duplicated floors cost more than the ring-fence is worth before revenue |
| EO-LYR-05 | Echelon IP co + Unbound co with servicing as a wholly owned subsidiary of Unbound | 90000 | best fit for ring-fencing servicing without splitting the platform |
| EO-LYR-06 | No servicing entity: Unbound licenses to an existing administrator who services | 0 | economically weak: previous study partnership plan at 14 bps net never profitable within 60 months |
| EO-LYR-07 | Charitable or nonprofit vehicle for servicing (to rely on PolyForm NC charitable-organisation permission) | 80000 | not recommended without counsel; listed for completeness |

**Recommendation (research level, not legal advice).** Run Echelon, Unbound and servicing as **business units in one entity with priced internal charges now** (EO-LYR-02), so the economics are visible and a later split is cheap. **Ring-fence servicing in a subsidiary when the first staffed-administration sponsor signs** (EO-LYR-05): servicing is where instructions over charitable money, fraud exposure and the SOC 1 reliance sit, and Unbound's own perimeter (CNV-LEG-001: no custody, no payment execution) should be mirrored by the servicer. **Separate the Echelon IP company only when Echelon has a second commercial user** (EO-LYR-03). Three separate entities (EO-LYR-04) duplicate corporate floors (standalone sum $7.79M vs group $4.99M, including the platform a standalone servicer would need) before any revenue justifies them. Criteria covered per option in entity-options.csv: liability ring-fencing, SOC 1 boundary (inclusive vs carve-out of Unbound as subservice organisation), PolyForm NC licensing, fundraising and transfer pricing/tax.
