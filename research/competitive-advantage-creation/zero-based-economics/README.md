# Zero-based operating economics (Phase III, first deliverable)

This is the first independently deliverable Phase III research package, as directed by the owner on 2026-11-27. Starting from zero operating expense, it builds up the cost of operating a functionally complete, production-qualified Unbound for paying institutional customers. Every expense must be justified by an obligation, a workload or a capacity trigger. The cost of reaching production qualification is kept separate.

**Start here: [00 — direct answers to the ten questions](00-answers.md).**

| # | Report |
|---|---|
| 00 | [Direct answers](00-answers.md) |
| 01 | [Method and scope](01-method-and-scope.md) |
| 02 | [Minimum operating configuration](02-minimum-operating-configuration.md) |
| 03 | [Expense register](03-expense-register.md) → generated [register](data/outputs/expense-register.md) |
| 04 | [Challenging human intervention](04-human-intervention-challenge.md) → generated [register](data/outputs/activity-register.md) |
| 05 | [Staffing derivation](05-staffing-derivation.md) |
| 06 | [Institutional growth, 0–100 customers](06-institutional-growth-scenarios.md) |
| 07 | [Commercial models](07-commercial-models.md) |
| 08 | [Prior estimates challenged](08-prior-estimate-challenges.md) |
| 09 | [Cost of reaching production qualification](09-cost-to-production-qualification.md) |
| 10 | [Sensitivity, capital and stress](10-sensitivity.md) |
| 11 | [Adversarial review and reconciliation](11-adversarial-review.md) |
| 12 | [Evidence gaps, legal uncertainties and gates](12-evidence-gaps.md) |

## Layout
```
data/inputs/      expenses, activities, roles, coverage, profiles, mixes, parameters, qualification, prior-estimates (CSV)
data/registers/   sources.csv, adversarial-findings.csv
data/evidence/    architecture-obligations.md, prices-infra.csv, prices-ops.csv, adversarial/ (raw reviews)
data/outputs/     generated: results.md, registers, headline/grid/thresholds/break-even/price-floors/capital/... CSVs
model/            F# model (pure core; I/O only in Program.fs) and xUnit tests
```

## Reproduce
```bash
export PATH=$HOME/.dotnet:$PATH DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1
cd model
dotnet test tests/ZeroBasedEconomics.Tests                                               # 26 tests
dotnet run --project src/ZeroBasedEconomics -c Release -- run ../data/inputs ../data/outputs
dotnet run --project src/ZeroBasedEconomics -c Release -- check ../data/inputs ../data/outputs   # byte-identical
dotnet run --project src/ZeroBasedEconomics -c Release -- validate ..                           # gates V1-V9
```
CI: `.github/workflows/zero-based-economics.yml` runs all three on every pull request touching this package.

## Boundaries
- Research only. No production implementation, paid research, external outreach or expenditure is authorised.
- Prices are public list prices read on 2026-11-27; nothing was purchased or requested from vendors.
- Legal questions stay open and are costed as counsel time ([12](12-evidence-gaps.md)).
- Founder-specific facts (availability, personal capital) are ranged parameters, not recorded facts. Sensitive internal detail belongs in the private organisation repository.
- The package sits beside the Phase III package in PR #94 and depends on nothing in it. It reuses only the entity codes E1/E3/E5.
