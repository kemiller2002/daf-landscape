# 01. Method and scope

## Question
What does it cost Echelon Foundry to operate Unbound for paying institutional customers, if we start from zero operating expense and add only what an obligation, a workload or a capacity limit requires?

## Ground rules
1. **Unbound is assumed functionally complete and production-qualified.** The cost of reaching that state is modelled separately in `data/inputs/qualification.csv` and [09](09-cost-to-production-qualification.md). It is never mixed into operating cost, except as an explicitly amortised line in the fully loaded view.
2. **Nothing is inherited.** Staffing ratios, organisation charts, development budgets and operating expenses from the Phase II models are not inputs. They appear only in [08](08-prior-estimate-challenges.md), as claims to reconstruct and test.
3. **Every expense row has the ten required attributes, and the validator enforces them (gate V2):**
   - identifier and purpose;
   - evidence source and accountable economic entity;
   - triggering condition;
   - minimum cost and likely cost range;
   - capacity limit;
   - alternative approach;
   - consequence of not incurring it.
4. **Every human activity answers the ten challenge questions** (gate V4):
   - why it exists;
   - whether law or contract requires it;
   - whether it can be prevented, done by deterministic software or assisted by AI;
   - who must decide;
   - how often it occurs and how long it takes;
   - when it forces staffing.
5. **No role exists without a reason.** A role needs a workload or a mandatory-coverage rule behind it (gate V6). "Conventional administrators employ someone in that role" is not a reason.
6. **Controls are not modelled away.** A legally or contractually required human decision keeps a positive human share at every level (gate V5). Decisions reserved to the sponsor are never borne by Echelon Foundry (gate V4), following CNV-GOV-004 and UNB-CDD-CMF-002.
7. **Evidence decides the direction.** Where the zero-based figure is higher than the prior estimate, it is reported as higher.

## Economic entities and cost views
| Code | Entity | Used for |
|---|---|---|
| E1 | Echelon Foundry (including the Unbound product line; a separate Unbound entity is deferred until there is a demonstrated need, per owner direction of 2026-11-27) | Operating cost of every commercial model |
| E3 | Sponsor (customer programme) | Sponsor-borne cost: reserved decisions, payment rails, own audit |
| E5 | Shared Echelon Foundry overhead | Workspace, entity, bookkeeping; allocated, mostly not incremental |

Each scenario reports five cost views:
- **Incremental cash:** new cash the DAF business causes. Shared costs count only for their incremental share.
- **Noncash founder labour:** founder hours × market rate (BLS software-developer median × ECEC loading ÷ 1,600 h = $123/h).
- **Shared allocation:** the DAF business's allocated share of shared Echelon Foundry costs.
- **Fully loaded economic cost:** incremental cash + shared allocation + founder labour + amortised cost of reaching production qualification.
- **Sponsor-borne cost:** reported separately and never added to Echelon Foundry cost.

## Expense classes (mission taxonomy)
`unavoidable-cash`, `conditional-cash`, `volume-triggered`, `shared-infrastructure`, `noncash-founder-labor`, `fully-loaded-economic`, `discretionary`. Labour is classified by the engine:
- founder hours become `noncash-founder-labor`;
- contracted and employed hours are cash, either conditional (coverage) or volume-triggered (workload).

## Obligation tiers (mandatory versus contractual)
| Tier | Obligation | Included when |
|---|---|---|
| 0 | `legal`, `operational-mandatory` (Unbound requirements that define "production-qualified") | Always |
| 1 | `contract-typical` (what most institutional contracts ask: SOC 2 Type II, $2M E&O/cyber, two-deep on-call) | Base case |
| 2 | `contract-demanding` (bank-grade: SOC 1 under licensing, $5M limits, 24x7 rotation, vCISO, warm standby region) | Sensitivity |
| 3 | `discretionary` | Never in the minimum configuration |

## Engine (F#, `model/`)
1. **Volume.** Each scenario has a customer count, a mix and four independent factor levels: accounts, assets per account, transactions per account and exception intensity.
   - The mix fixes which institutional profiles the first *n* customers have. Customers are deliberately not all the same size: profiles run from XS (60 accounts) to XL (30,000 accounts).
   - Each factor takes its low, base or high value independently, giving 81 combinations per count and mix.
2. **Expenses.** An expense is active when the model bears it, its tier is within the scenario's tier, and its trigger metric reaches its threshold. Drivers are `fixed`, `per <metric>` or `step <metric> <capacity>`.
3. **Workload.** Each activity's hours = driver units × rate × human share × minutes ÷ 60.
   - Exception-driven activities scale with exception intensity independently of volume.
   - Activities gated by `min_customers` do not exist with no customers.
4. **Staffing.** The founder absorbs eligible work first, in register order, up to the hours available to the DAF business.
   - Residual hours below a role's hire threshold are contracted.
   - Whole FTEs of residual work are employed, and a remainder above the threshold adds one employee.
5. **Coverage.** Rules requiring distinct qualified people are met as follows:
   - **The rules:** two non-author approvers for control-module changes, two-person break-glass, two-deep on-call, and business-day operations continuity.
   - **How each shortfall is met:** for every role, every combination of *k* extra hires plus per-rule retainers for the remaining shortfall is costed. The cheapest feasible combination wins.
   - **What counts towards each rule:** a hire counts towards every rule on its role. A retainer counts only towards its own rule; a contracted code reviewer is not on-call cover.
6. **Revenue.** Each model's reference prices (`parameters.csv`) give contribution margins. Break-even prices and fees are computed independently of those references.
7. **Analysis.** The engine then computes:
   - the 0/1/2/5/10/25/50/100-customer table for every model and tier;
   - the full factor grid and staffing thresholds by mix;
   - break-even customers and assets, single-customer break-even assets at 5–30 bps, and break-even prices;
   - capital before first revenue;
   - self-financing at 1–10 customers;
   - prior-estimate comparables;
   - a tornado and a 2,000-draw Monte Carlo (independent, and ρ = 0.5 adverse-correlated).

`run` writes `data/outputs/`. `check` proves byte-identical reproduction. `validate` enforces gates V1–V9. Unit tests cover triggers, drivers, sharing, tiers, staffing, coverage optimisation, sponsor attribution, revenue, orientation, sampling and every validation gate, and confirm that the published outputs reproduce.

## Levels
The cost-side ranges are ordered low ≤ base ≤ high. Scenario views use **oriented** levels:
- **Low:** every input at its favourable end: more founder hours, higher prices, lower costs.
- **High:** every input at its adverse end.

The Monte Carlo samples each range triangularly. Volume uncertainty is not sampled there; it is covered separately by the factor grid.

## What is not in scope
- Production implementation, paid research, outreach or any expenditure. None is authorised, and nothing here authorises any.
- Legal conclusions. Open legal questions stay open:
  - TPSP role under Nacha;
  - source rights;
  - IP assignment mechanics;
  - whether extra screening lists are legally required.
  
  They are costed as counsel time, not resolved.
