# 03. Expense register

The full register is generated from [`data/inputs/expenses.csv`](data/inputs/expenses.csv) into [`data/outputs/expense-register.md`](data/outputs/expense-register.md). It has 51 expenses, and each carries the ten required attributes:
- identifier, purpose and evidence;
- accountable entity, trigger and minimum;
- likely range and capacity limit;
- alternative and consequence.

Gate V2 fails the build if any attribute is missing. The first customer count at which each expense becomes Echelon Foundry cost, by model, is in [`expense-activation.csv`](data/outputs/expense-activation.csv).

## By class (counts of expense rows)
| Class | Rows | Examples |
|---|---|---|
| Unavoidable cash | 8 | Database cluster, application hosting, write-once storage, edge, logs, keys, staging, free IRS/OFAC sources ($0, recorded so the decision is visible) |
| Conditional cash | 23 | SOC 2/SOC 1 audits, pen test, compliance platform, insurance by limit, counsel, status/paging, help desk, vCISO (tier 2), escrow (tier 2) |
| Volume-triggered | 11 | Database and hosting scale-out, storage and log growth, email, AI inference, migration compute, contract counsel per new customer, acquisition travel, payment rails (sponsor) |
| Shared infrastructure | 5 | Workspace and identity, code hosting, AI development tooling, legal entity, bookkeeping. Only the incremental share is DAF cash; the allocated share appears in the fully loaded view |
| Discretionary | 4 | D&O insurance, fractional CFO, licensed charity data (platform models), commercial sanctions screening |

Two classes are produced by the engine rather than the register:
- **Noncash founder labour:** founder hours × $123/h.
- **Fully loaded economic cost:** cash + shared allocation + founder labour + amortised qualification.

## By accountable entity
| Entity | Role |
|---|---|
| E1 Echelon Foundry | Every operating cost of every commercial model |
| E3 Sponsor | Payment-rail fees, positive pay; sponsor-reserved activities (via [`activities.csv`](data/inputs/activities.csv)) |
| E5 Shared Echelon Foundry overhead | Workspace, entity, bookkeeping, D&O |

## Triggers used
- `always`;
- `customers ≥ 1` (most assurance and insurance);
- `customers ≥ 2` (SOC 1 under limited operations);
- `customers ≥ 3` (SOC 1 under licensing);
- `accounts ≥ 5,000` (scale-out);
- `accounts ≥ 20,000` (read replica);
- `new_customers` (counsel, acquisition, migration compute);
- contract tier, which separates mandatory, typical and demanding obligations ([01](01-method-and-scope.md)).

## Capacity limits that matter
- **Database:** the benchmarked slice handled 2,100–3,900 tx/s against about 200 needed, so the base cluster carries about 5,000 accounts before scale-up.
- **Insurance:** every limit is an aggregate. Contracts with universities and bank partners commonly require $5M (tier 2).
- **SOC reports:** one per scope per year. Bridge letters only cover gaps after an existing report.
