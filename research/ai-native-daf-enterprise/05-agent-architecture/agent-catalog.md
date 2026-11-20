# Agent catalog

**Source of record:** [`agent-catalog.csv`](agent-catalog.csv) lists 19 agents with all of the required attributes. This file explains the catalog's shape, the cost method and the acceptance policy. It does not repeat each row.

**No accuracy figure in this catalog is a measurement.** There are no public evaluation datasets for any DAF agent task. The repository's census found no sponsor documenting AI in approval or eligibility ([strategic synthesis §0 B](../../mission-2026-11-14/strategic-synthesis.md)). Every "acceptance target" is a *design gate to be set and measured* in Phases 3–5. The only exceptions are structural invariants, such as "zero postings without D confirmation", which are enforced by architecture and tested in the proof of concept.

## 1. Agents by category

| Category | Agents | Count |
|---|---|---|
| 2: AI-assisted analysis (propose, flag, dossier) | AG-01 Recipient resolution · AG-02 Benefit-risk flagger · AG-03 Sanctions near-match triage · AG-04 Exception grant dossier · AG-05 Orphan deposit matcher · AG-06 Reconciliation break triage · AG-07 Complex asset dossier · AG-08 Document extraction · AG-11 Donor discovery and education · AG-13 Policy drafting and impact · AG-14 Regulatory change monitor · AG-15 SOC report analyzer · AG-16 Improvement recommendation · AG-17 Undeclared related-party detector · AG-18 Fraud anomaly explainer | 15 |
| 3: Supervised execution (non-authoritative effects only) | AG-09 Service answer agent · AG-10 Advisor copilot · AG-12 Post-grant ER tracker · AG-19 Board evidence pack narrator | 4 |
| 4 and 5 | No agents. These categories are defined by their absence (see [agent-architecture.md §5](agent-architecture.md)) | 0 |

**Most enterprise volume involves no agent at all.** It runs through Category 1 deterministic services: routine eligibility, the payment gate, posting, fees, acknowledgments and rebalancing. Agents are concentrated where interpretation is unavoidable: free text, documents, near-matches and explanations.

### What the catalog deliberately does not contain

| Absent agent | Reason |
|---|---|
| Grant approver | DD-002 |
| Payment releaser | P1 |
| Investment manager | DD-007 |
| Flag clearer | DD-005 |
| Autonomous complaint resolver | P8 |

There is also no "general operations agent" with broad tools. Each agent has a narrow mission and a tool scope that fits it.

## 2. Mapping to the outcome decisions

| Outcome decision (from [`outcome-decisions.csv`](../01-enterprise-outcomes/outcome-decisions.csv)) | Agent | Resolves to |
|---|---|---|
| DEC-008 contribution sanctions near-match triage | AG-03 | DEC-009 (H, sanctions officer) |
| DEC-010 orphan deposit attribution | AG-05 | Donor confirmation (D) or controller (H) |
| DEC-012 forgery and synthetic-ID scoring | Identity-risk model (vendor, Cat. 2; not a catalog agent) | D threshold |
| DEC-017 undeclared relationship detection | AG-17 | DEC-018 (H) |
| DEC-033 reconciliation break triage | AG-06 | D rule or DEC-034 (H) |
| DEC-037 recipient resolution from free text | AG-01 | Donor confirms |
| DEC-040 benefit-risk flag | AG-02 | DEC-041 (H) |
| DEC-043 non-routine grant | AG-04 dossier | H |
| DEC-050 fraud scoring | Fraud model (Cat. 2) + AG-18 explanation | DEC-051 (D hold) / DEC-052 (H release) |
| DEC-055 policy question answers | AG-09 | Grounded reply (Cat. 3) |
| DEC-064 recipient information | AG-11 | Informational only |
| DEC-078 improvement opportunity | AG-16 | DEC-080 (H change board) |

## 3. Cost method

**Basis [V]:** the repository's AI economics analysis prices a *heavy* document review at about **$0.45 per case**. The workload assumed is 60k input and 3k output tokens, multiplied by 3 for retries and agent steps. The price is Claude Sonnet 5.5 list pricing ($2 / $10 per million input / output tokens), read 2026-11-14. Against this it sets about **$83** of reviewer time ([`ai-economics-replacement-analysis.md`](../../mission-2026-11-14/ai-economics-replacement-analysis.md) finding 1; [industry report §7](../../DAF-INDUSTRY-REPORT-2026-11.md)). Prices change, so the model takes the price as a parameter.

**Cost classes [A]:** these are token-volume assumptions for planning, not measurements.

| Class | Assumed tokens per run (in / out, before ×3 loop) | Cost per run at the 2026-11-14 Sonnet 5.5 list price, ×3 | Agents |
|---|---|---|---|
| light | 8k / 1k | ≈ $0.08 | AG-01, 02, 03, 05, 06, 09, 10, 11, 12, 17, 18 |
| medium | 25k / 2k | ≈ $0.21 | AG-08, 14, 16, 19 |
| heavy | 60k / 3k | ≈ $0.45 (the repository basis) | AG-04, 07, 13, 15 |

**Cost per completed outcome:**

`cost per completed outcome = Σ over agents (runs per outcome × cost per run) + validator and broker compute + human minutes × loaded rate`

The human-minutes term dominates. With 1 light run per recommendation, a routine grant carries about $0.08 of AG-01 cost (when the recipient is name-only) plus about $0.08 for AG-02, and zero human cost on the D path. An exception grant adds one heavy AG-04 run (about $0.45) plus specialist minutes, which are unknown: no sponsor publishes handling time (Q-N03; [strategic synthesis §0 F](../../mission-2026-11-14/strategic-synthesis.md)). These figures feed [`../09-financial-models/`](../09-financial-models/) as parameters with sensitivity ranges. They are not results.

Even at 10× these token assumptions, inference stays well below one human minute per case. The repository's conclusion that "inference cost is immaterial; oversight, integration and residual human workload are the constraint" therefore holds [I].

## 4. Acceptance policy (applies to every agent)

1. **Structural invariants: must be 100%, enforced by architecture.** No authoritative write, no flag clearance, no money movement, no out-of-privilege read. Tested in the proof of concept and in every release.
2. **Risk-flag agents (AG-02, 03, 17, plus the fraud model):** the activation gate is a *recall floor* on the golden and adversarial sets, set by the CRCO before activation. Precision is gated only so that the human queue stays within SLA.
3. **Proposal agents (AG-01, 05, 06, 08):** gate on the human acceptance-without-edit rate in shadow mode. Proposals never become authoritative without D confirmation or H.
4. **Effect agents (AG-09, 10, 12, 19):** gate on the grounding-check pass rate. 100% of *sent* outputs must pass, because the validator blocks the rest. A sampled QA pass rate is also required.
5. **Every agent has a baseline:** the conventional human process or the no-agent deterministic process. An agent is kept only if it beats that baseline on the outcome metric *after* QA cost. Eliminating the work is always considered first, following the repository's finding that redesign removes exception classes while AI only shortens handling ([industry report §7](../../DAF-INDUSTRY-REPORT-2026-11.md)).
