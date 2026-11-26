# Control framework

**Data:** [`controls.csv`](controls.csv) holds 45 controls (CTL-001 to CTL-045). Each maps an obligation or risk to a control, then gives:
- type (preventive or detective);
- automation level;
- the evidence produced;
- frequency, owner and test method.

Legal obligations come from [`regulatory-applicability-map.md`](regulatory-applicability-map.md) and [`regulatory-applicability-matrix.csv`](regulatory-applicability-matrix.csv) (REG-ids). Risks come from the [outcome model](../01-enterprise-outcomes/outcome-model.md) failure modes.

## 1. Design principles

1. **Prefer structural prevention to review.** The strongest controls make the bad state unrepresentable, not merely detectable. CTL-001 is the example: a donor-side principal has no command that creates an instruction.
2. **Every automated control produces evidence as a by-product of operating.** The same record that drives the workflow is the evidence. Nothing is assembled after the fact ([continuous compliance](continuous-compliance-and-evidence.md)).
3. **Humans sit where judgment or independence is required, not where data must be moved.** Manual controls: dual control above threshold, sanctions clearance, complex asset acceptance, write-offs, policy and parameter approval, related-party approval, and holds.
4. **Controls on the control system.** Policy publishing (CTL-009), the monotonic safety rule (CTL-010), agent evaluation gates (CTL-026) and coverage tests (CTL-037) prevent the improvement loop from eroding safeguards.
5. **Each control has a test method that can run in a non-production environment and the digital twin.** Controls without a test are not counted as operating.

## 2. Control families

| Family | Controls | Key invariant |
|---|---|---|
| Exclusive control and authority | CTL-001, 002, 006, 007 | No asset moves without a sponsor decision; nobody approves their own or a related party's item |
| Payments | CTL-003, 004, 005, 029, 032, 043, 044 | A payment requires an approved grant, a verified payee and an available limit, and is signed only by the payment-gate identity |
| Grant compliance | CTL-011, 012, 013, 014, 045 | Stale data refers rather than passes; only the sanctions officer clears a potential match |
| Accounting integrity | CTL-015 to 019 | Append-only ledger; daily three-way reconciliation; unit-ledger identity |
| Contributions | CTL-020, 021, 022 | Acknowledgment content is tested; complex assets need a human decision |
| Investments | CTL-023, 024, 025 | Pre-trade checks; parameters change only with committee approval |
| AI and automation | CTL-008, 010, 026, 027, 028, 030 | Flag-only AI; evaluation gates; kill switches; no loosening without approval |
| Security and resilience | CTL-031 to 036 | No standing human payment credentials; exit and restore are tested |
| Compliance operations | CTL-037, 038, 039, 040 | Obligation coverage is 100%; deadlines escalate |
| Governance | CTL-041, 042, 045 | Conflicts recused; related-party transactions approved by disinterested directors |

## 3. Segregation-of-duties invariants

These are enforced by the authorization model, checked continuously (CTL-006), and expected to return an empty conflict set.

| # | Invariant |
|---|---|
| SoD-1 | Create or modify a payee payment profile ⟂ approve a payment to that payee |
| SoD-2 | Author a policy version ⟂ approve or publish it |
| SoD-3 | Request (donor, advisor, agent principal) ⟂ instruct (sponsor) |
| SoD-4 | Raise an exception case ⟂ decide it |
| SoD-5 | Engineer with deploy rights ⟂ change rebalancer, fee or threshold parameters without the approval record |
| SoD-6 | Grant privileged access ⟂ use it (just-in-time approval by a second person) |
| SoD-7 | Perform reconciliation write-off above threshold ⟂ approve it |
| SoD-8 | Agent owner ⟂ sole model-risk sign-off for their own agent (CRCO signs) |
| SoD-9 | Related party of a donor or recipient ⟂ any decision on that grant |

**Small-scale limit:** at 1k accounts the minimum staff of about 8–10 can satisfy SoD-1 to SoD-9 only if the controller, CFO and CRCO roles are held by different people ([organization model §4](../02-business-capabilities/organization-model.md)). Below that, SoD fails and the enterprise should use Model C infrastructure under an established sponsor.

## 4. Dual control thresholds

Thresholds are *governed parameters*: versioned policy objects with approval records, never constants in code. Initial values are assumptions **[A]** for calibration in Phase 5:

| Item | Single control (deterministic gate only) | Second human approver |
|---|---|---|
| Routine grant to a listed public charity, no flags | up to $250k [A] | above $250k [A] |
| Exception-path grant (flagged, ER, foreign) | — | always: specialist plus a second approver above $50k [A] |
| Reconciliation write-off | up to $500 [A] (rule-classified rounding only) | above $500 [A] |
| Payee profile change | never (cooling-off and verification always) | release during cooling-off |
| Policy or threshold loosening | — | always (Change Board plus CRCO) |

## 5. What is deliberately *not* a control

- **Human re-review of every routine grant.** The statutory exposure for listed public charities is narrow (DD-004). The control effort goes to data freshness, sanctions and flags instead.
- **Bank-style BSA program elements.** These are not applicable to a charity that is not a BSA financial institution (see the REG map). The enterprise still runs a risk-based sanctions and fraud program (CTL-012/013/029).
- **Annual staff attestation surveys** (ACT-046). They are replaced by continuous evidence.
