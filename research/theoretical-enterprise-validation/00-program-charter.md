# Program charter: DAF theoretical enterprise validation

**Started:** 2026-11-22. **Branch:** `claude/daf-theoretical-validation-4zbxfh`.
**Status:** theoretical analysis only. Nothing here is implemented, tested against a real system, legally reviewed, or independently validated.

## 1. Purpose

Find where the existing DAF enterprise requirements are wrong, incomplete, contradictory, needlessly complicated, economically fragile or unable to handle real operations. Then produce a requirements foundation that is as coherent as the available evidence allows.

The goal is **not** to show that the existing requirements are good. A domain with no findings is labelled "not yet evaluated" or "coherent with unresolved assumptions". It is never labelled correct.

## 2. Scope

**Under test** (the "baseline"):

| Baseline body | Location | Version |
|---|---|---|
| Financial core control spec | [`docs/financial-core-control-spec-v0.5.md`](../../docs/financial-core-control-spec-v0.5.md) | v0.5 |
| Administration core (ADM-01..30, EST, AG, PARTY, AUTH, SUCC, POL, SPEND, FEE, SVC, GOV, ECON, OPS, INT, DATA, MIG, AI, SLO) | [`docs/administration/`](../../docs/administration/) | v0.1 |
| Enterprise UI, vertical slices, UX v0.2, widget contracts W01–W05 | [`docs/`](../../docs/), [`docs/ui/`](../../docs/ui/) | v0.1–v0.2 |
| AI-native enterprise workstream (outcomes, 24 workflows, 35 entities, 58 events, 54 controls, 65 REG rows, 19 agents, DD-001..021) | [`research/ai-native-daf-enterprise/`](../ai-native-daf-enterprise/) | 2026-11-21 |
| Workflow-innovation designs, experiments E1–E10, adversarial verdicts | [`research/ai-native-daf-enterprise/workflow-innovation/`](../ai-native-daf-enterprise/workflow-innovation/) | 2026-11-21 |

**Out of scope (directive restrictions):** application code, prototypes, executable simulations, schemas, APIs, UI, infrastructure, technology selection, changes to existing F# models, claims of production readiness or SOC 2 compliance.

Conceptual state diagrams, invariant statements, decision tables, event catalogs and interface-contract *requirements* are in scope as specification artifacts.

## 3. Governance discovered and how it is applied

| Standard named in the directive | What was found | How this program applies it |
|---|---|---|
| Praxis (repository OS), Ordo/SDE, Dokimos | Not installed in this repository. The [component assessment](../ai-native-daf-enterprise/07-technology-architecture/echelon-component-assessment.md) classes them as SDLC tooling, PolyForm Noncommercial, single maintainer (DD-014). | Not invoked. Their intent (durable checkpoints, provenance, verification evidence) is met by this repository's own conventions: [ledger](LEDGER.md), ID registers, evidence labels. |
| Echelon Knowledge Store | Research-phase; "do-not-depend" (DD-014). | Pattern only: governed Markdown and CSV registers are the source; no compiled artifacts. |
| Clarity | `clarity-framework` is private and was **not inspected**. The pinned summary [`clarity-edf-application-guide.md`](../mission-2026-11-14/clarity-edf-application-guide.md) is used. | Claim states (supported / contested / unverified), falsification criteria and reconsideration triggers in the [assumption register](16-registers/assumption-register.csv). Marked as an application of the pinned summary, not of verified Clarity. |
| EDF | Self-declared unvalidated diagnostic grammar (v0.3). | Used as optional vocabulary for causal chains in [failure analysis](12-failure-analysis/failure-analysis.md). Never cited as validation. |
| Echelon AI-Native Enterprise Design Framework (`kemiller2002/Echelon-AI-Native-Enterprise-Design-Framework`) | Rules: evidence or nothing; preserve contradictions; never weaken governance invariants; read-only dependencies. | Followed. That repository is **not modified** by this program (its AGENTS.md rule 6). |
| This repository | Labels [V]/[I]/[S]/[A]; EV/GAP/DD/REG ids; conflicts recorded, not overwritten; existing research read-only. | Followed. Existing files are not edited. New IDs use the `TV` prefix to avoid collisions. |

## 4. Evidence labels and ID scheme

Labels are inherited from the [AI-native workstream](../ai-native-daf-enterprise/README.md#evidence-conventions): **[V]** validated against a cited primary source; **[I]** inference; **[S]** scenario; **[A]** assumption with no source. This program adds:

| Label | Meaning |
|---|---|
| **[T]** | Theoretical derivation: follows logically from stated requirements. Not observed. |
| **[C]** | Requires professional (legal, tax, accounting) review before it may be relied on. |
| **[P]** | Sponsor policy choice; no legal mandate is claimed. |

| Prefix | Object | Register |
|---|---|---|
| TVF-nnn | Finding | [findings](16-registers/findings.csv) |
| TVR-<domain>-nnn | Requirement (new or restated) | [requirements graph](16-registers/requirements.csv) |
| TVC-nnn | Contradiction | [contradiction register](16-registers/contradiction-register.md) |
| TVA-nnn | Assumption | [assumption register](16-registers/assumption-register.csv) |
| TVS-nnn | Scenario | [scenario library](11-scenarios/scenarios.csv) |
| FI-nn | Financial invariant | [financial invariants](07-financial-invariants/financial-invariants.md) |
| TVCTL-nn | Proposed control | [compliance and controls](08-compliance/compliance-and-controls.md) |
| OD-nn | Owner decision required | [owner decisions](16-registers/owner-decisions.md) |

## 5. Independence statement

All analytical passes in this program were produced by one AI model family. Some passes ran in **separate model contexts** that received only the artifacts, not the author's reasoning. That separation reduces anchoring. It is still **role-separated self-critique, not independent validation**. No human reviewer, auditor, counsel or sponsor has reviewed any conclusion. See [adversarial reviews](13-adversarial-reviews/role-reviews.md).

## 6. Stopping rules

Analysis of a workflow stops expanding when:
- new scenarios are mostly semantic duplicates;
- additional findings are immaterial (severity ≤ 2 of 5);
- progress needs unavailable external evidence; or
- the remaining question is an owner policy decision.

Scenario counts and document counts are not completion criteria. Saturation is measured as new material findings per round ([scenario library §4](11-scenarios/scenario-library.md#4-saturation-tracking)).
