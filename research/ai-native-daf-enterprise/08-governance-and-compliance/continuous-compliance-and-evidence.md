# Continuous compliance and evidence

**Principle:** compliance evidence is a by-product of operating, not a project. The record that drives a workflow is the record an auditor or examiner reads.

## 1. Evidence ledger

| Property | Design |
|---|---|
| Content | `Evidence` records (see the [data model](../06-data-and-knowledge/canonical-data-model.md)), each with `control_id`, subject, producing component and version, timestamp, payload hash, and links to the Decision, Event and Document records |
| Immutability | Append-only, hash-chained per day. A daily root hash is anchored externally, for example in the board-approved daily operations report and an external timestamping service. Tampering is therefore detectable (CTL-019) |
| Retention | Per a retention schedule keyed to obligations. Records for tax and Form 990 support are kept at least as long as returns can be examined, and longer where state law or policy requires [A, confirm with counsel]. Litigation hold overrides deletion |
| Access | Role-based. Auditors and regulators get *read-only, scoped, logged* access through an evidence API ([`../04-enterprise-apis/`](../04-enterprise-apis/), Audit Evidence API) |
| Privacy | Evidence references Party IDs, not identity attributes. Examiner views can reveal identity only where legally required, and the reveal is logged |

## 2. A reviewable decision record: what an examiner sees for one grant

A single query by grant ID returns one bundle:

```
Grant G-2027-000123 · $5,000 · Recipient EIN 12-3456789 · Account A-…  (correlation C-…)
├─ RecommendationSubmitted  by Party P-… (donor) via channel=advisor-API (partner X), privilege grant PG-… v3
├─ RecipientResolved        method=exact-EIN · registry snapshot 2027-03-02
├─ EligibilityEvaluated     PASS · rule ELIG-PC-001@v7 · Pub78 2027-02-28 (sha…) · BMF 2027-02-10 (sha…)
│                           · revocation list 2027-02-15 (sha…) · freshness OK (CTL-011)
├─ ScreeningCompleted       PASS · OFAC list 2027-03-01T… (sha…) · fuzzy policy SCR-003@v2 (CTL-012)
├─ Flags                    none raised · agents run: BenefitRisk@v4 (AgentRun AR-…, cost $0.004) → no flag
├─ GrantApproved            actor=Rule GRANT-ROUTINE-001@v12 (approved by GC on 2027-01-05, back-test BT-…)
│                           · amount ≤ routine limit $250k (param DOA-ROUTINE@v3)
├─ PaymentInstructed        gate PASS (CTL-003) · payee profile PP-… verified 2026-11-20 (evidence …)
├─ PaymentSettled           ACH trace … · 2027-03-03
├─ Remittance               grant ID in addenda · donor info per choice=name_only (CTL-043)
└─ Journal entries          JE-…, JE-… (posting rule POST-GRANT@v5) · reconciled REC-… (CTL-015)
```

For a human-decided grant, the bundle adds:
- the ExceptionCase, with its flags and the dossier version the human saw;
- the Approval: approver, delegated-authority reference and reason;
- the SoD and related-party checks performed (CTL-006/007).

**Why this matters.** The question an IRS examiner or state AG asks ("what did you know, when, and who decided?") is answered from bitemporal facts with source versions. No reconstruction from email is needed.

## 3. Obligation → control coverage tests

- The obligation register (machine-readable REG rows; see [`regulatory-applicability-matrix.csv`](regulatory-applicability-matrix.csv)) is linked to controls (CTL rows) by a mapping table.
- **CTL-037:** a CI and runtime test fails if any obligation with status `current_law` and applicability `sponsor=yes` has no mapped control with evidence produced within its frequency window.
- `proposed` obligations (for example the 2023 proposed §4966 regulations, still neither final nor withdrawn per [industry report §6](../../DAF-INDUSTRY-REPORT-2026-11.md)) are tracked with impact analyses and pre-built policy variants. They are not enforced.
- When an obligation changes (`ComplianceObligationChanged`), the impact analysis runs the candidate policy against the historical grant corpus. This is the "policy-as-code back-test" (strategic synthesis §B, structural change 1).

## 4. Self-audit sampling

| Sample | Size [A] | Frequency | Checks |
|---|---|---|---|
| Routine auto-approved grants | 50 per month, stratified by amount and channel | Monthly | Recompute the decision from the pinned inputs (determinism check); verify data versions; verify no unexamined flag |
| Human-decided exception grants | 100% of ER and foreign; 20% of others | Monthly | Dossier completeness; authority; reasoning quality |
| Sanctions clearances | 100% | Monthly | Officer, evidence, timeliness |
| Contributions and acknowledgments | 30 per month plus all noncash > $5k | Monthly | Settlement, date, content (CTL-020) |
| Reconciliation write-offs | 100% above threshold | Monthly | Approval, root cause |
| Agent runs | Random 200 per agent per month | Monthly | Output quality versus a human re-rating; flags missed |

Sampled results feed the [continuous improvement system](continuous-improvement-system.md) and the internal audit plan.

## 5. External audit model

- The auditor receives scoped read access to the evidence API and ledger extracts. "Prepared by client" lists are replaced by queries the auditor runs (ACT-041).
- Auditor-recomputable artifacts: NAV calculations, fee calculations, the unit-ledger identity, and reconciliations.
- The auditor's control testing samples from the same decision bundles (§2). Any automated control the auditor relies on must have documented change management, which CTL-009, CTL-010 and CTL-026 supply.
- Year-end is a checkpoint, not a project: cut-off tests run on bitemporal records.

## 6. Regulatory inquiry response procedure

1. **Intake (H: GC).** Log the inquiry as a case. Apply a legal hold to the subject records (deletion suspended). Classify by scope and deadline.
2. **Scope query (DET).** Assemble decision bundles and evidence for the subjects and period. Generate an index with hashes.
3. **Review (H: GC, outside counsel as needed).** Privilege review. Agents may summarize and draft; counsel reviews every outbound statement.
4. **Respond (H: officer).** Produce the response with an evidence index. Record what was produced.
5. **Learn.** Findings become `ComplianceObligationChanged` or control changes through the controlled-change cycle.

Scenario coverage: see "Regulatory inquiry" and "SPLC-style hold controversy" in [`../11-scenarios-and-validation/scenarios.md`](../11-scenarios-and-validation/scenarios.md).
