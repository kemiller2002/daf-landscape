# Zero-based economics model (F#)

Research tool, not product code. It follows the draft Echelon Foundry standards ENG-6BEA (reproducible F# research models) and MTH-48F0 (event-level costing).

**Structure.** The core is pure; I/O happens only in `Program.fs`.

| Module | Contents |
|---|---|
| `Domain` | Types: models, classes, obligations and tiers, metrics, drivers, expenses, activities, roles, coverage, profiles, mixes, factors |
| `Csv` | RFC 4180 reader and writer (copied from the Phase II model) |
| `Inputs` | Parsing with every error collected |
| `Sampling` | LCG, triangular, common-shock correlation, percentiles |
| `Engine` | Realisation (level, oriented, draw), volumes, expense activation, workload, staffing, coverage optimisation, revenue, `evaluate` |
| `Analysis` | Growth tables, factor grid, staffing thresholds, persistent break-even by mix, single-customer break-even assets, price floors, growth-path capital, self-financing, deep-review allocation, prior comparables, tornado, Monte Carlo |
| `Render` | CSV and Markdown outputs |
| `Validate` | Gates V1–V9 |

**Commands**
- `run <inputs> <outputs>` writes every output.
- `check` verifies byte-identical reproduction.
- `validate <package-root>` enforces:
  - V1 unique identifiers;
  - V2 the ten expense attributes;
  - V3 evidence identifiers that resolve;
  - V4 the ten activity answers, with sponsor-reserved decisions never borne by Echelon Foundry;
  - V5 no required control modelled to zero;
  - V6 no role without workload or coverage;
  - V7 coherent shares and bearers;
  - V8 parameters and mixes;
  - V9 Markdown links that resolve.

Requires the .NET 10 SDK (`global.json`).
