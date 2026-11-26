# Workflow innovation methodology

**Status:** governing method for `workflow-innovation/`. **Started:** 2026-11-20.
**Builds on:** the enterprise architecture in the parent workstream ([`../../README.md`](../../README.md)):
- 18 outcomes;
- 24 workflows (WF-01…WF-24);
- the [F# reference models](../../models/);
- evidence register EV-001…EV-156;
- gap register GAP-001…GAP-040.

This research area does **not** re-derive those. It asks the next question: *for each outcome, what entirely different mechanisms could produce it, and which survive testing?*

## 1. The question asked of every activity

> Why does the organization perform this activity at all, what outcome does it actually produce, and what entirely different mechanism could produce a better result?

"Better" is never "fewer manual steps". A design is better only if it beats a stated comparator on stated criteria (§6), under stated assumptions, with its evidence class shown.

## 2. Two modes, kept separate

| Mode | Rules |
|---|---|
| **Ideation** (02, 03) | Unconstrained. No idea is rejected for being unconventional. Legal, fiduciary, accounting, privacy and financial-safeguard constraints are *suspended only to generate ideas* and are reintroduced one at a time in the constraint pass (§3C) |
| **Execution** (07–12) | Evidence-based, authorized, controlled. An idea advances only by evidence. Legal requirements, fiduciary duty, accounting integrity, donor privacy and financial safeguards are never optional |

## 3. Creative reasoning methods, applied to every major process

| Method | Procedure | Output field |
|---|---|---|
| **A. First-principles decomposition** | State the outcome. Strip every step. List only the *information*, *authority*, *resources* and *actions* strictly necessary. Rebuild from those | `necessary_elements` in each design catalog entry |
| **B. Inversion** | Ask the ten inversion prompts in the brief (eliminate it? make it unnecessary? no employee touch? no form? no departments? continuous compliance? continuous reconciliation? no approval queue? begin before the request? an external partner does it?) | `inversion_findings` |
| **C. Constraint removal and reintroduction** | Remove the technology and organization constraints, then generate. Reintroduce **legal → fiduciary → accounting → privacy/security → economic → operational → human-acceptance** one at a time. Record which ideas die at which constraint, and what modification revives them | Constraint ledger table per workflow |
| **D. Cross-industry transfer** | Payment networks, insurance, airlines, manufacturing, logistics, healthcare, autonomous systems, exchanges, compilers, distributed transactions, scientific experimentation, marketplaces. For each transfer state *why it might work* and *where the analogy breaks* | [cross-industry transfer catalog](../02-creative-hypotheses/cross-industry-transfers.md) |
| **E. Zero-based organizational design** | Design around capabilities, decision rights, accountability and outcomes; preserve nothing by default | [`../11-reference-architectures/`](../11-reference-architectures/) |
| **F. Contrarian hypotheses** | State plausible contradictions of industry convention as falsifiable hypotheses | Hypothesis register (`hypothesis_type = contrarian`) |

## 4. Mandatory alternative set per major outcome

Each design catalog entry ([`../03-alternative-designs/`](../03-alternative-designs/)) contains at least:

1. **Conventional baseline:** how it is typically done today, with evidence class.
2. **Automation-first:** the same process with substantial automation.
3. **AI-native redesign:** a different process using AI, structured data and APIs. Usually this is the parent workstream's design.
4. **Radical alternative:** removes major steps, boundaries or assumptions. *It must differ in mechanism from the AI-native design*, not just in degree. Where a workflow is eliminated, the entry states what replaces its underlying function.
5. **Externalized or ecosystem model:** partners, shared infrastructure, distributed capabilities.
6. (Optional) further alternatives where genuinely distinct.

An adversarial check (§7) rejects superficial variants. Two designs are "meaningfully different" if they differ in at least one of: *who holds the decision right*, *when the work happens relative to the request*, *what data source is authoritative*, or *which organization performs it*.

## 5. Maturity ladder (never skipped, never overstated)

| Level | Name | Meaning | Required evidence |
|---|---|---|---|
| L0 | **Invented hypothesis** | An idea with a stated mechanism | Mechanism statement |
| L1 | **Plausible design** | Mechanism is coherent with law and architecture; no contradicting evidence known | Constraint pass survived; regulatory map rows checked |
| L2 | **Evidence-supported design** | Public or repository evidence supports the *mechanism's premise* (for example data showing recipients recur across sponsors) | Cited EV rows or new data with method |
| L3 | **Tested prototype** | Executable model or experiment on synthetic or public data shows the effect under defined metrics, including adversarial cases | Experiment spec plus reproducible results plus passing tests |
| L4 | **Operationally validated capability** | Measured in operation with a real organization under authorization | **None in this research.** No design here can be L4 without a design partner |

The highest level any item reaches in this research is **L3**. L3 means "works in a model", not "works in a DAF".

## 6. Evaluation criteria (defined before scoring)

| Criterion | Definition | Measured how |
|---|---|---|
| Human workload | Human minutes per outcome unit | Model or experiment |
| Latency | Time from trigger to outcome (p50/p95) | Simulation |
| Control effectiveness | Share of seeded defects caught before money moves; escaped-defect rate | Adversarial test sets |
| Accuracy | Correct decisions ÷ decisions, against ground truth in synthetic data | Experiment |
| Resilience | Correctness after injected failures (crash, duplicate, outage) | Fault-injection tests |
| Cost per outcome | Fixed + variable + AI + human + vendor + risk cost | F# economics |
| Exception rate | Share routed to humans | Experiment |
| Reuse | Share of work avoided because an earlier verified result applies | Data (Schedule I overlap) plus model |
| Experience | Donor, advisor and nonprofit steps, waits and information quality | Structured comparison (no user research available, labeled) |
| Risk transfer | Whether work is eliminated or merely moved (to donor, nonprofit, partner, reviewer) | Adversarial review |

## 7. Adversarial validation

Adversarial reviews ([`../07-adversarial-reviews/`](../07-adversarial-reviews/)) were produced by a **separate agent that did not author the designs**. It was given the documents, not the authors' conclusions, mirroring the repository's validation-wave practice. Each promising innovation faces the brief's 13 questions: work moved rather than eliminated, hidden review cost, segregation of duties, concentration, unreliable AI, fraud, lock-in, compliance cost, unusual transactions, scale cost, acceptance, replicability, and missing authority.

## 8. Creative competition (seven perspectives)

For each top-10 workflow, the design catalog records a pass from each perspective: **Inventor**, **Enterprise architect**, **Economist**, **Regulatory specialist**, **Adversarial reviewer**, **Customer advocate** and **Commercial strategist**. Disagreements and unresolved questions are kept. Scoring happens only after evidence exists (§6) and is never collapsed into one opaque number ([`../10-prioritization/`](../10-prioritization/)).

## 9. Frameworks

- **Clarity** and **EDF** are used as pinned in [`../../../mission-2026-11-14/clarity-edf-application-guide.md`](../../../mission-2026-11-14/clarity-edf-application-guide.md): EDF only on observed outcomes; Clarity governs reasoning depth, posture and reconsideration.
- **Echelon AI-Native Enterprise Design Framework:** inspected 2026-11-20 at `github.com/kemiller2002/Echelon-AI-Native-Enterprise-Design-Framework`, commit `57c53f7` ("Initial commit"). It contains one empty `README.md`. **There are no verified schemas or methods to use yet.** This research therefore uses its own method (this file) and records generalizable patterns as *proposals* in [`../12-implementation-proposals/framework-feedback-proposals.md`](../12-implementation-proposals/framework-feedback-proposals.md). The framework repository is not modified (brief §16).

## 10. Standards

- **F#** for executable models and experiments (`models/Daf.Experiments*`). **Python** is used only for public-data harvesting, following the repository's existing `scripts/` convention.
- No live transactions. Synthetic data only, plus public filings.
- Every number carries a basis: sourced (EV, data file), assumed [A], scenario [S] or experiment result [X]. Experiment results are reproducible by command.
- Progress is checkpointed in [`../PROGRESS.md`](../PROGRESS.md).
