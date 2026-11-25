# Servicing economics research model (F#)

This is a research tool, not product code. It evaluates a DAF servicing business from labelled parameters:
- annual economics with stepped capacity, December peaks, pricing structures and stresses;
- break-even and target-margin searches;
- 60-month strategy cash plans.

**Layout:**
- Pure core: `Domain`, `Economics`, `Parameters`, `Analysis`, `CashFlow`, `Strategies`, `Render`.
- I/O: only `Program.fs`.

**Requires:** .NET 10 SDK (`global.json`).

```bash
dotnet test tests/ServicingEconomics.Tests                      # 28 tests, all passing on 2026-11-25
dotnet run --project src/ServicingEconomics -c Release -- out ../../../../data/commercial-opportunity/servicing-economics/sponsor-economics.csv
```

**Outputs:**
- `out/results.md`: all tables;
- `out/sponsor-model-economics.csv`: every sponsor re-costed; copied to `data/commercial-opportunity/servicing-economics/`.

Two consecutive runs are byte-identical.
