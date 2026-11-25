# Research ledger: DAF servicing economics (2026-11-25)

Mission: [2026-11-25-servicing-economics-agent-mission.md](../2026-11-25-servicing-economics-agent-mission.md), plus the owner's expanded brief of 2026-11-25. Each entry is a durable checkpoint, with its commit recorded in git history.

| Date | Phase | Entry |
|---|---|---|
| 2026-11-25 | 0 | **Branch:** `claude/daf-economics-event-architecture-v1zdti` from `main` @ `e1a3633`. Unbound is read-only, at `main` @ `9b38de4`. **Tooling:** .NET 10 SDK installed for the F# research model; xUnit restores from NuGet. **Research passes:** five role-separated agent passes launched (pricing, sponsor dataset, cost register, activity costing, Echelon and Clarity/EDF). These are passes by the same model family, so they are not independent validation. |
| 2026-11-25 | 5 | **Model scaffold:** `model/` holds the pure F# core (annual economics, capacity with step hiring, December peak, minimum fees, stresses, break-even and minimum-price searches, monthly cash flow). **Regression:** 20 xUnit tests reproduce the prior memo's table, its 30%-shock loss and its closed-form break-even, and check units, invariants, capacity steps, peak premium and billing timing. Result: `dotnet test` 20/20 passed. |
