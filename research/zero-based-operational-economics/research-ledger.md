# Research ledger: zero-based operational economics

Persistent initiative ledger (work, dependencies, gaps, decisions, blockers, repository changes, validation).

| # | Date | Step | Output | Verification |
|---|---|---|---|---|
| 1 | 2026-11-27 | Initialisation: daf-landscape `main` at `10b92f4`; branch `claude/zero-based-unbound-economics-kia9lj`; Praxis requirements read (daf-landscape has no Praxis installation; prior initiatives used a ledger and registers — followed) | — | git |
| 2 | 2026-11-27 | Repositories verified: unbound, transitus, praxis, echelon-foundry, echelon-registry, strata, forma, limen, folio, conditor, arca and others read; echelon-organization-administration attached (private); **beneficium not accessible — blocker, no replacement created** | [24](24-cross-repository-implications.md) | add_repo results |
| 3 | 2026-11-27 | .NET 10 SDK installed; original competitive-displacement model tests 16/16 pass; `check` byte-identical; $1.924B / $3.85M reconstructed by formula | [02](02-existing-model-reconstruction.md) | dotnet test; check |
| 4 | 2026-11-27 | Six independent research tracks launched in parallel: activity inventory; control obligations; Echelon shared capabilities and development records; infrastructure prices; Beneficium public data (bounded sampling); original cost trace | `data/registers/`, `data/evidence/` | each CSV validated by its agent with python csv |
| 5 | 2026-11-27 | F# model built (`ZeroBased`, referencing `CompetitiveDisplacement`): workload, queue simulation, staffing, infrastructure, costs (3 views), Beneficium, revenue, analyses | `model/` | builds with warnings as errors |
| 6 | 2026-11-27 | Defects found and fixed during build: weekend calendar ageing of SLAs (staffing ×400); FINANCE pool hired at 2 FTE for 28 h (hire decision moved to average load); slow linear staffing search (bisection) | Simulation.fs, Staffing.fs | re-run |
| 7 | 2026-11-27 | Cross-checks: model infrastructure at 1k accounts $12.56k vs independent arithmetic $12.49k; identity at 1M accounts $88.2k both; DB vCPU change point consistent (~730k accounts) | [12](12-infrastructure-economics.md) | test asserts within 5% |
| 8 | 2026-11-27 | Checkpoint commit `f0bfbc8`; 20/20 tests; `check` OK; pushed | — | dotnet test; check |
| 9 | 2026-11-27 | Five adversarial contexts × two perspectives launched (ten perspectives); 118 findings (43 high) | `data/evidence/adversarial/` | CSVs validated |
| 10 | 2026-11-27 | Correction round A: bucket order (sponsor-responsible work no longer bypasses configuration); review routing by work type; missing engineering (defects, shared integrations, second approver, change volume 600/yr); least-cost fractional vs dedicated; compliance backup; incident SLAs; duplicated incidents removed; management overhead; Beneficium upkeep into pools; vetting with grant-time check and Rev. Proc. 2018-32 reliance; insurance limits, MDR, on-call, breach cost, privileged-access review, immutable backups; SOC 1 in licensing; break-even by sponsor size, licensing per account, capital required, founder sensitivity, system cost | commit `8ff1b8d` | 20/20 tests; check OK |
| 11 | 2026-11-27 | Correction round B: controller separated from payment authorizer; turnover, escrow, key-person, entity bookkeeping, observability, standalone sales; counsel, contact rates, December concentration, regulatory change, patching, specialist engineering rate; economic build at $1.94M; fractional engagement floors; vendor coordinates provider exceptions; pool-specific analytic peak factors (analytic within ~6% of simulation); policy levers | commit `9b452f4` | 20/20 tests; check OK |
| 12 | 2026-11-27 | **Reversal preserved:** first draft showed full administration at $1.03M (break-even ≈ $0.5B); after review $2.20M (≈ $1.85B), within 1% of the original at its own operating point | [23](23-adversarial-review.md) | baseline-comparison.csv |
| 13 | 2026-11-27 | Probe runs (scratch scripts, not committed): per-sponsor marginal cost at fixed accounts (S = 1, 2, 4, 8 → $2.01M, $2.26M, $2.76M, $3.28M before round B); analytic vs simulated pool staffing; MS GIFT-sized book (21,800 accounts, 1 sponsor, $417k mean) → $5.1M analytic / $5.8M simulated (5.6-6.4 bps) | [10](10-workload-and-capacity-model.md), [20](20-competitive-comparison.md) | dotnet fsi |
| 14 | 2026-11-27 | Dispositions recorded for all 118 findings (84 accepted, 10 partly, 19 noted, 3 escalated, 1 superseded, 1 rejected as base) | `adversarial-findings.csv` | validate |
| 15 | 2026-11-27 | Reports 00-27, README, registers (decisions, open questions, cross-repository, scenarios, evidence index); `validate` command added | reports | validate |
| 16 | 2026-11-27 | Final synthesis review (independent context) of reports against regenerated outputs | see entry 17 | — |

## Blockers

- `kemiller2002/beneficium` not accessible: research held here (XRI-ZB-10).
- No measured operations, time study, design partner or effort telemetry: every operational number is modelled.
- DF-ASR-2026-0D0F prevents counsel, broker or auditor confirmation (OD-ZB-02).

## Repository changes

Only `research/zero-based-operational-economics/` in daf-landscape. No other repository was modified.
