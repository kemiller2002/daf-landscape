# Competitive advantage creation model (F#, Phase III)

Research tool, not product code. Pure core; I/O only in `Program.fs`. Methodology: [18](../18-economic-model-methodology.md).

Modules: `Csv` (copied from the Phase II model), `Domain` (ranges, cases, parameters, validation), `Sampling` (adapted from Phase II: LCG, triangular, grouped correlation), `Cashflow` (monthly cash and fully loaded engine), `Capital` (model 1), `Events` (model 2), `Registry` (model 3), `Channel` (model 4), `Licensing` (model 5), `SharedInfra` (model 6), `Response` (model 7), `Sequences` (model 8, kill rule, funding variants), `Phase2Check` (port of Phase II `Routes.flows` for the double-count checks), `Inputs`, `Analysis` (tornado, Monte Carlo, extremes), `Render`, `Registers` (merge), `Quote`, `Validate`.

The Phase II model in `../../competitive-displacement/model/` is not modified or referenced at build time. `Csv.fs` and `Sampling.fs` were copied and adapted; `Phase2Check.fs` ports `Routes.flows` and is tested to reproduce Phase II's ER-7 base capital exactly.

```bash
export PATH=$HOME/.dotnet:$PATH DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1
dotnet test tests/CompetitiveAdvantageCreation.Tests
R="dotnet run --project src/CompetitiveAdvantageCreation -c Release --"
$R run ../data/model-inputs ../data/model-outputs      # all models; tables under data/model-outputs/tables/
$R check ../data/model-inputs ../data/model-outputs    # byte-identical reproduction
$R fragments ..                                       # copy generated rows to data/fragments/MOD/
$R merge ..                                           # data/fragments/*/<register>.csv -> data/registers/
$R quote ..                                           # refresh <!-- model-output --> blocks in the reports
$R validate ..                                        # registers, references, deliverables, links, quoted tables
```

Inputs (`../data/model-inputs/`): `parameters.csv` and `settings.csv` (named ranges with an `adverse` end and assumption IDs), `capital-states.csv` (agent AB's `model-capital-states.csv` with categories renamed and AB's computed contingency and capital-charge rows dropped, since the model computes them), `event-work.csv` (agent HI's `event-work-decomposition.csv`), `registry-components.csv` (agent HI's components with explicit scaling and kind), `phase2-routes.csv` (Phase II ER-4 and ER-7 base values), `mvp-grid.csv` (agent CD), `shared-infra-pools.csv`, `shared-infra-products.csv`, `response-scenarios.csv` (agent EK), and `sequence-streams.csv`, `sequence-values.csv`, `sequence-meta.csv` (streams in long format; templates inherit values). Every row cites assumption, sequence or source IDs; `validate` checks that each cited ID exists in a register.

Monte Carlo: 2,000 draws per sequence, seed 20261126, triangular ranges; correlation by group (demand; cost) with rho 0 and 0.5.
