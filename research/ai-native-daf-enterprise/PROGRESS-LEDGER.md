# Progress ledger: AI-native DAF enterprise architecture

**Branch:** `claude/ai-native-daf-architecture-lsfr4y`. **Started:** 2026-11-20.
**Purpose:** a durable record so the work can resume after a context limit or an interrupted session. Update this file in the same commit as the work it describes.

## How to resume
1. Read this ledger, then [README.md](README.md) (reading order) and [DECISION-LOG.md](DECISION-LOG.md).
2. Check the "Open items" table below; each has an owner directory and acceptance test.
3. Executable models live in [`models/`](models/) (F#, .NET 8). Run `dotnet test models/Daf.Enterprise.Tests` before committing changes to them.
4. Never edit files outside `research/ai-native-daf-enterprise/` without recording why here. Existing research is read-only for this workstream; conflicts are recorded, not overwritten.

## Status by deliverable (2026-11-20)

| # | Directory | Status | Contents (counts verified by script or tests) |
|---|---|---|---|
| 00 | `00-research-inventory/` | done | Inventory (12 sections); 156 evidence rows (EV-001–156); 40 gaps (GAP-001–040; 9 P0) |
| 01 | `01-enterprise-outcomes/` | done | 18 outcomes; 81 decision types (37 D / 11 P / 33 H); 80 legacy activities classified (tested census) |
| 02 | `02-business-capabilities/` | done | 29 capabilities; org model; accountability matrix (one A per row, tested); functional areas A–N × 18 headings |
| 03 | `03-workflow-redesign/` | done | 24 workflows (22 span ≥2 legacy departments; WF-11 and WF-23 are new capabilities, exempted); integration journey; 16 diagrams |
| 04 | `04-enterprise-apis/` | done | 23 API domains; 5 OpenAPI 3.1 contracts (load-checked) |
| 05 | `05-agent-architecture/` | done | 19 agents; category model; authority boundaries INV-A1–A8 (tested in models/) |
| 06 | `06-data-and-knowledge/` | done | 35 entities; 58 events (8 added after cross-deliverable review) |
| 07 | `07-technology-architecture/` | done | Technology architecture; Echelon component assessment (DD-014) |
| 08 | `08-governance-and-compliance/` | done | 65 regulatory requirements; 50 controls (CTL-046–050 added from the Clarity review); governance; security; continuous compliance; continuous improvement |
| 09 | `09-financial-models/` | done ([S]) | F# model outputs at 1k/10k/100k/1m; AUM variants; sensitivity; break-even; models A–D grid; 5-year ramps |
| 10 | `10-market-and-business-model/` | done | Options; A/B/C/D/Dc matrix (reproducible scoring.py); §8 reconciliation with 09; capability commercialization; competition; validation plan |
| 11 | `11-scenarios-and-validation/` | done | 22 scenarios; SPOF register; digital twin and outputs |
| 12 | `12-implementation-roadmap/` | done | Six phases; Gates 1–5; budget $5.5m–$9.5m [A] |
| 13 | `13-clarity-edf-analysis/` | done | 19 assumption challenges; 5 EDF analyses; 25 failure modes; 9 major conclusions |
| 14 | `14-executive-conclusions/` | done | Executive report (softened per 13-); traceability matrix (18 rows) |
| — | `models/` | done | F# .NET 8 solution: domain, policy, ledger, journey, economics, twin, report, CLI; **59 passing tests** |

## Open items (next session)

| Item | Why | Acceptance |
|---|---|---|
| CTL→REG mapping table | `controls.csv` refers to obligations generically; the coverage test needs REG ids | Every REG row with obligation_type=legal maps to ≥1 CTL |
| Agent-name reconciliation | Functional areas and workflows introduced agent names not in the 19-agent catalog (e.g. QA sampler, fairness monitor, foreign-diligence) | Each name maps to a catalog agent or is added |
| API sub-resources raised by forks | `/v1/recommendations:batch`, `/v1/grants/{id}/verification`, `/v1/parties/{id}/preferences`, `/v1/policies/{id}/evaluate`, shared-determination entity | Added to the API catalog or explicitly rejected |
| Determination-reuse parameter in 09 model | The largest unmodeled lever | Parameterised; sensitivity rerun |
| Workflow-local IDs | Functional areas use WF-A1…WF-N5 locally | Mapped to WF-01…WF-24 or listed as sub-workflows |
| Phase 1 evidence | GAP-001/002/004/005/006/012/014/027 need design partners and counsel | Roadmap Gate 1 |

## Conflicts recorded (not overwritten)
- **Exception share:** the governing figure is ~4.2% like-for-like; the earlier 2.5–3% is superseded. The 7.76%/11.61% core proxy is used as the per-recipient basis and ~7–8.5% per grant (EV-079–081).
- **Fidelity grant volume:** 3.0m (CY2025) in the entrant model against 2,664,446 (CY2024) in the efficiency study. This workstream uses CY2024 with FY2024 990s for period alignment.
- **"B is dominated"** (10- §5) vs B's best steady-state margins (09): reconciled in 10- §8. B is dominated on risk-adjusted time-to-evidence, not on terminal economics.
- **Echelon F#-first:** the brief assumed a Foundry mandate; the component assessment found none. DD-015 records F# on its own merits.

## Session log

| Date | Work | Commit |
|---|---|---|
| 2026-11-20 | Audited the repository (410 docs, 764 CSVs, 2,557 validation rows; governing texts: industry report §1–§11.79 and strategic synthesis §0). Installed .NET 8 SDK for F# models. Created the workstream structure, ledger, decision log. | (this commit) |
| 2026-11-20 | Research inventory, regulatory map, Echelon assessment (background agents); outcome model, capability map, org model, data model, events, decision log; functional areas A–N, workflows, APIs, agents, governance, scenarios, market models (parallel forks); F# reference models with 59 tests; economics outputs and ramps; digital twin; technology architecture; roadmap; Clarity/EDF; executive report; traceability | see git log |
