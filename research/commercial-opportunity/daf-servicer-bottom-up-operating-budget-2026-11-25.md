# Bottom-up DAF servicer operating budget
2026-11-25 | Scenario research, not validated staffing or price.
Companion: [20 bps market entry](daf-servicing-20bps-market-entry-2026-11-25.md).
Scope: contracted servicer, sponsor retains legal ownership and reserved decisions; no custody or investment management. 20 bps on average billable assets. No paid consultations.

## Fixed budget
| Role | Salary | Loaded at 1.25 |
|---|---:|---:|
| Managing director / sales | 130000 | 162500 |
| Technical lead | 150000 | 187500 |
| Engineer | 120000 | 150000 |
| Controller / financial operations | 115000 | 143750 |
| Grant/client operations | 80000 | 100000 |
| Total | 595000 | 743750 |

| Expense | Annual USD |
|---|---:|
| Loaded personnel | 743750 |
| Legal/compliance | 60000 |
| Independent accounting/controls | 45000 |
| Seasonal/backup coverage | 60000 |
| Cloud/monitoring | 36000 |
| Security/assurance | 65000 |
| Insurance | 30000 |
| Business software | 18000 |
| Sales/travel | 40000 |
| General administration | 20000 |
| Contingency | 60000 |
| Total | 1177750 |

All amounts are analyst-selected planning assumptions, not quotes or labor-market measurements. Five FTE is a hypothesis; sponsor retains decision authority; independent controls, dual authorization, backup coverage and incident response must be demonstrated. No assumption that one controller can independently approve own work. Fixed staff capacity is finite.

## Incremental cost and capacity
Use $75/fund-year as sensitivity placeholder, incremental to fixed budget, not a measured cost. Illustrative decomposition: external payments $10, data/identity $10, incremental cloud $5, incremental operations labor $40, other exception/vendor cost $10. Avoid counting fixed staff or contracted coverage again; payment and vendor rates unverified. Replace with activity drivers: grants, contributions, contacts, reconciliations, sponsor integrations, exceptions and complexity. At $50/hour incremental labor, $40 funds 48 minutes per account annually; test against observed activity. At 5000 funds this implies 4000 incremental hours if fully used, approximately 2.5 FTE at 1600 productive hours, beyond five fixed staff. Do not represent the organization as only five people at all scales. Step-fixed hiring, sponsor-specific costs and capacity must be modeled separately.

## Economics
F=1177750, v=75, r=.002, B=200000. Revenue=r*AUA; cost=F+v*AUA/B. Break-even=F/(r-v/B); target margin m=F/((1-m)*r-v/B).
| AUA billions | Revenue | Cost | Surplus | Margin |
|---:|---:|---:|---:|---:|
| 0.5 | 1000000 | 1365250 | -365250 | -36.52% |
| 0.75 | 1500000 | 1459000 | 41000 | 2.73% |
| 1 | 2000000 | 1552750 | 447250 | 22.36% |
| 1.5 | 3000000 | 1740250 | 1259750 | 41.99% |
| 2 | 4000000 | 1927750 | 2072250 | 51.81% |
At B=50k/100k/200k/500k break-even AUA $2.356B/$942M/$725M/$637M; 25% margin impossible/$1.570B/$1.047B/$872M. At $1B and 30% full-year asset shock, unchanged accounts/costs, loss $152750. To survive 30% shock at B=200k initial AUA must be at least $1.149B. For 25% margin after shock, $1.745B initial AUA. Sponsor concentration and minimum contract fee matter.

## Startup runway
Illustrative 12 months pre-revenue fixed burn $1.178M plus $250k one-time launch/migration reserve = $1.428M; 18 months $2.017M; 24 months $2.606M. Add working capital, actual development scope, implementation and financing costs not covered; not a capital commitment. No live charitable assets handled before controls and contracts. Revenue ramp must use actual billable average assets, not signed headline assets.

## Reconcile prior Unbound model
[05a economic tables](https://github.com/kemiller2002/unbound/blob/main/requirements/convergence/2026-11-24-master/05a-ECONOMIC-TABLES.md) reports $192/$299 per fund at 10k funds under base/adverse platform scale, excluding sponsor-retained decision costs ~$43 and certain vendor P&L items. This scenario yields $192.775 at 10k funds, numerical proximity is not validation: cost boundaries and platform scale differ. At 5k funds cost $310.55. Do not add prior all-in per-fund model to this fixed budget; reconcile component by component. No validators or independent evidence checks executed.

## Next evidence
Benchmark salaries using public BLS/OEWS, benefits using BLS ECEC; obtain public cloud/payment price schedules, insurance and assurance ranges, estimate actual grant/contact workloads, staff coverage, sponsor integration effort, and sales cycle. Test 3/5/8 core FTE, outsourcing and founder-led alternatives; compare 10–30 bps and adverse mix. Record primary evidence and uncertainty. Apply formal Clarity/EDF when available; no formal execution claimed. No Unbound requirements modified.
