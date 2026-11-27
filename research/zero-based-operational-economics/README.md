# Zero-based operational economics: Unbound, Beneficium and shared Echelon capabilities

Date: 2026-11-27. Status: research. **Not legal, tax, accounting or investment advice; not a launch, hiring or expenditure authorisation.** Every economic figure is conditional on labelled inputs. Nothing is measured operational performance. Agents, reviewers and integrator are the same model family; nothing here is independent professional assurance.

**Start with [00-executive-findings.md](00-executive-findings.md); recommendations in [27-final-recommendations.md](27-final-recommendations.md).**

## Reports

| # | Report |
|---|---|
| 00 | [Executive findings](00-executive-findings.md) (answers the 25 required questions) |
| 01 | [Methodology](01-methodology.md) |
| 02 | [Existing model reconstruction](02-existing-model-reconstruction.md) |
| 03 | [Cost assumption audit](03-cost-assumption-audit.md) |
| 04 | [Operational activity inventory](04-operational-activity-inventory.md) |
| 05 | [Activity elimination and automation](05-activity-elimination-and-automation.md) |
| 06 | [Human control obligations](06-human-control-obligations.md) |
| 07 | [Minimum viable organisation](07-minimum-viable-organization.md) |
| 08 | [Shared Echelon resource economics](08-shared-echelon-resource-economics.md) |
| 09 | [Operational simulation design](09-operational-simulation-design.md) |
| 10 | [Workload and capacity model](10-workload-and-capacity-model.md) |
| 11 | [Staffing thresholds](11-staffing-thresholds.md) |
| 12 | [Infrastructure economics](12-infrastructure-economics.md) |
| 13 | [Beneficium public-data economics](13-beneficium-public-data-economics.md) |
| 14 | [Beneficium verification economics](14-beneficium-verification-economics.md) |
| 15 | [Charity vetting alternatives](15-charity-vetting-alternatives.md) |
| 16 | [Software development economics](16-software-development-economics.md) |
| 17 | [Revenue models](17-revenue-models.md) |
| 18 | [Break-even analysis](18-break-even-analysis.md) |
| 19 | [Sensitivity and stress testing](19-sensitivity-and-stress-testing.md) |
| 20 | [Competitive comparison](20-competitive-comparison.md) |
| 21 | [Requirement economic impact](21-requirement-economic-impact.md) |
| 22 | [Continuous economic validation](22-continuous-economic-validation.md) |
| 23 | [Adversarial review](23-adversarial-review.md) |
| 24 | [Cross-repository implications](24-cross-repository-implications.md) |
| 25 | [Evidence gaps and validation plan](25-evidence-gaps-and-validation-plan.md) |
| 26 | [Decisions and open questions](26-decisions-and-open-questions.md) |
| 27 | [Final recommendations](27-final-recommendations.md) |

Ledger: [research-ledger.md](research-ledger.md). Data conventions: [data/CONVENTIONS.md](data/CONVENTIONS.md).

## Machine-readable data

| Path | Content |
|---|---|
| `data/registers/operational-activities.csv` | 183 operational activities linked to Unbound requirements |
| `data/registers/control-obligations.csv` | 63 control obligations with mandate class and primary citations |
| `data/registers/requirement-economic-impact.csv` | 51 requirement economic impact records |
| `data/registers/original-cost-trace.csv` | 132-row trace of the original model's costs |
| `data/registers/shared-capabilities.csv` | 32 Echelon capabilities with verified responsibilities |
| `data/registers/infrastructure-prices.csv`, `infrastructure-consumption-assumptions.csv` | 88 published prices; 44 consumption assumptions |
| `data/registers/beneficium-data-sources.csv`, `beneficium-dataset-sizing.csv` | 29 public data sources; 38 sizing measurements and assumptions |
| `data/registers/adversarial-findings.csv` | 118 findings with dispositions |
| `data/registers/decisions.csv`, `open-questions.csv`, `cross-repository-implications.csv`, `scenario-definitions.csv`, `evidence-sources.csv` | decisions, questions, proposals, scenarios, source index |
| `data/model-inputs/*.csv` | parameters (assumption schema), roles, configurations, fixed costs, programmes, infrastructure and Beneficium parameters |
| `data/model-outputs/*` | 31 generated outputs (byte-reproducible), summary in `results.md` |
| `data/evidence/*` | agent evidence notes, adversarial reviews, infrastructure cross-check script |

## Reproduce and validate

Requires .NET 10 SDK. The model references `research/competitive-displacement/model` (reused, not duplicated) and reproduces the original model in the same run.

```bash
cd model
dotnet test tests/ZeroBased.Tests                                                                                  # 20 tests
dotnet run --project src/ZeroBased -c Release -- run   ../data ../../competitive-displacement/data/model-inputs ../data/model-outputs
dotnet run --project src/ZeroBased -c Release -- check ../data ../../competitive-displacement/data/model-inputs ../data/model-outputs   # byte-identical
dotnet run --project src/ZeroBased -c Release -- validate ..                                                         # deliverables, CSVs, schema, links, dispositions
```

## Rules followed

Public sources and owner repositories only; bounded public-data sampling (≈185 MB, deleted); no logins, purchases, paid consultations, outreach or production deployment; no changes to Unbound, Transitus, Praxis, Echelon or the preserved competitive-displacement baseline (proposals only); unfavourable findings preserved, including the reversal of this research's own first draft.
