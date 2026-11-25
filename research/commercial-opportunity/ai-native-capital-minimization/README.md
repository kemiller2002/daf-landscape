# Capital minimization and AI-native DAF enterprise design

**Date:** 2026-11-25.

**Mission:** [2026-11-25-capital-minimization-agent-mission.md](../2026-11-25-capital-minimization-agent-mission.md) (verbatim).

**Previous study:** [servicing-economics/](../servicing-economics/README.md), preserved unchanged and reused as the model baseline.

**Status:** theoretical research.
- No outreach, paid data, consultations or confidential information.
- Unbound and the Echelon component repositories were read-only.
- Proposed requirement changes are in report 17.
- **Not a launch authorization, and not independently validated** (same-model passes and review).

**Start here:** [18-executive-findings.md](18-executive-findings.md).

**Short answer:**
- No fundamentally different company emerges on present evidence. Designing from outcomes gives a somewhat cheaper, better-instrumented version of the same business: about 8% cheaper like for like at $1.5B.
- Break-even at 20 bps is **$1.44-1.85B** with a minimum-scope platform, and **$2.46-2.65B** with Unbound's full scope.
- Minimum equity is **$4.5M** founder-led, **$6.4-7.2M** on other AI-native paths, and **$10.1M** conventional.
- A servicing company on an existing Unbound needs **$1.35-2.8M**.
- Gates costing $0.15M and then $0.75M test the conditions that could change this before any build spend.

## Reports

| # | Report | Content |
|---|---|---|
| 00 | [Source baseline](00-source-baseline.md) | Revisions, passes, evidence rules; previous conclusions and their status |
| 01 | [Conventional assumption register](01-conventional-assumption-register.md) | 52 assumptions: origin, replacement, better, worse or unproven |
| 02 | [Outcome-driven enterprise design](02-outcome-driven-enterprise-design.md) | 27 outcomes; responsibility matrix; work elimination (50.7 → 30.1 minutes; transfers separated) |
| 03 | [Three-layer economic model](03-three-layer-economic-model.md) | Echelon, Unbound and servicing: standalone, incremental, allocated and consolidated views; entity options |
| 04 | [Development cost reconstruction](04-development-cost-reconstruction.md) | The $5M and $60k origins; minimum servicing product $1.1-2.4M; $100k-$5M scenarios; deferrable scope |
| 05 | [Echelon productivity evaluation](05-echelon-productivity-evaluation.md) | 26 repos built and tested; throughput; productivity sensitivity; measurement protocol |
| 06 | [Workload-driven staffing](06-workload-driven-staffing.md) | Handling targets of 10-100 minutes; floor about 12; December sizing; real drivers replace ratios |
| 07 | [Minimum viable organization](07-minimum-viable-organization.md) | 1, 2, 3, 5, 6 and 9-core designs; CNV-GOV-003 admissibility; three core + hires |
| 08 | [AI-native operating architecture](08-ai-native-operating-architecture.md) | Cases, events, controls and evidence; 16 bounded AI capabilities (proposal) |
| 09 | [Administrative overhead elimination](09-administrative-overhead-elimination.md) | Coordination 12 → 4.75 hours a week; real gain about 3% of capacity |
| 10 | [Pricing strategy reassessment](10-pricing-strategy-reassessment.md) | Sponsor value and retained margin; $737 is not a ceiling; per-account tariff |
| 11 | [Capital minimization strategies](11-capital-minimization-strategies.md) | Sequences A-G; growth and existing-Unbound variants; staged gates |
| 12 | [Incremental commercial opportunities](12-incremental-commercial-opportunities.md) | 11 standalone capabilities; customer-funded development |
| 13 | [Incumbent replication analysis](13-incumbent-replication-analysis.md) | 7 advantages + combination; incumbent responses |
| 14 | [Revised economic model](14-revised-economic-model.md) | Cost bridge; scenario matrix; findings; what is assumed |
| 15 | [Failure and resilience analysis](15-failure-and-resilience-analysis.md) | 23 failures; 11 modifiers including correlated failures; detection and gates |
| 16 | [Adversarial review](16-adversarial-review.md) | 27 model findings and dispositions; hidden-cost ledger; Clarity, EDF, nine perspectives, falsification |
| 17 | [Requirements transfer candidates](17-requirements-transfer-candidates.md) | RC-AN-001..020, traced to Unbound IDs |
| 18 | [Executive findings](18-executive-findings.md) | Mission answer; the 20 questions; corrections |
| — | [Research ledger](research-ledger.md) | Checkpoints and test runs |

## Data (`data/commercial-opportunity/ai-native-capital-minimization/`)

| Dataset (mission section 22) | Files |
|---|---|
| Assumptions | `assumptions-register.csv` (76), `assumption-register.csv` (52 conventional assumptions) |
| Activities | `work-elimination.csv` (33), `outcomes.csv` (27), `responsibility-matrix.csv` (83), `handling-targets.csv` (32), `workload-tails.csv` (17), `overhead.csv` (14), `ai-capabilities.csv` (16) |
| Costs | `layer-costs.csv` (43), `layer-summary.json`, `entity-options.csv` (7), `hidden-costs.csv` (23) |
| Staffing capacity | `staffing-capacity.csv` (11 roles), `ops-metrics.json` |
| Development estimates | `dev-scenarios.csv` (36), `deferrable-capabilities.csv` (24), `component-verification.csv` (26), `throughput.csv` (31), `loc.json`, `build-logs/` |
| Commercial | `sponsor-value.csv` (35), `pricing-structures.csv` (210), `opportunities.csv` (11), `replication.csv` (12) |
| Commercial milestones | `commercial-milestones.csv` (12 gated milestones) |
| Evidence | `evidence-register.csv` (160) |
| Decisions | `decision-register.csv` (D-CM-001..011) |
| Requirements | `requirements-candidates.csv` (20) |
| Review | `adversarial-findings.csv` (27), `framework-procedure.jsonl` (26), `nine-perspectives.csv` (9), `falsification.csv` (6), `failure-catalogue.csv` (23), `adv-experiments.out` |
| Pass records | `pass-reports/*.jsonl` (DEV, OPS, COM, LYR, ADV), `pass-evidence/*.jsonl` |

## Reproduce

```bash
cd research/commercial-opportunity/ai-native-capital-minimization/model
dotnet test tests/CapitalMinimization.Tests                 # 23 tests
dotnet run --project src/CapitalMinimization -c Release -- out
cd ../../../..
python3 -I -B research/commercial-opportunity/ai-native-capital-minimization/scripts/build_registers.py .
python3 -I -B research/commercial-opportunity/ai-native-capital-minimization/scripts/assemble_reports.py .
```

Pass scripts are kept verbatim in [`scripts/`](scripts/) (`dev/`, `ops/`, `com/`, `lyr/`, `adv/`). They ran in a scratch workspace, and some reference its absolute paths and the local clones of the read-only repositories.
