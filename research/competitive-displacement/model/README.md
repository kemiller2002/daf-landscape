# Competitive displacement model (F#)

Research tool, not product code. Pure core (`Csv`, `Inputs`, `Sampling`, `Events`, `Enterprise`, `Registry`, `Routes`, `Analysis`, `Render`, `Validate`); I/O only in `Program.fs`.

**What it computes**
- Event-level cost of 25 operational events under 7 operating modes (conventional, AI-assisted, workflow, exception-driven, AI-native, licensing, hybrid): touch probability × minutes per touch × rate, AI cost, prevention, and expected failure lifecycle cost.
- Break-even assets at 5-30 bps by balance and sponsor count, with a 2,000-draw seeded Monte Carlo and a tornado.
- Saving decomposition (AI vs deterministic design vs prevention) and prevention-versus-speed per event.
- Charity registry: reconstruction of the $316k estimate and seven alternatives over 672 population/sponsor/change-rate/refresh scenarios.
- Entry-route capital (deepest cumulative deficit over 60 months) for seven routes.

**Requires** .NET 10 SDK (`global.json`).

```bash
dotnet test tests/CompetitiveDisplacement.Tests                                   # 13 tests
dotnet run --project src/CompetitiveDisplacement -c Release -- run ../data/model-inputs ../data/model-outputs
dotnet run --project src/CompetitiveDisplacement -c Release -- check ../data/model-inputs ../data/model-outputs   # byte-identical reproduction
dotnet run --project src/CompetitiveDisplacement -c Release -- validate ..                                       # registers, references, deliverables, links
```

`out/results.md` is a copy of `../data/model-outputs/results.md`.

**Inputs** (`../data/model-inputs/`): `events.csv` (anchored to `data/commercial-opportunity/servicing-economics/activities.csv` ACT-A01..S07), `parameters.csv`, `enterprise-modes.csv`, `registry-components.csv`, `registry-alternatives.csv`, `registry-parameters.csv`, `entry-routes.csv`. Every row carries an evidence class and basis.

**Limits.** Parameters are drawn independently (correlations would widen tails). Fixed costs and customer-acquisition rates are assumptions. Nothing is measured.
