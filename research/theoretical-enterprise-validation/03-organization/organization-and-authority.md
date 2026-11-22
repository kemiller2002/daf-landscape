# Domain inventory, organization and authority model

**Status:** theoretical [T]. Baseline:
- [capability map](../ai-native-daf-enterprise/02-business-capabilities/capability-map.md): 30 capabilities, C1.1–C6.4;
- [organization model](../ai-native-daf-enterprise/02-business-capabilities/organization-model.md);
- [accountability matrix](../ai-native-daf-enterprise/02-business-capabilities/accountability-matrix.csv);
- ADM-01..30;
- AUTH-01..10.

## 1. Domain inventory: two partitions reconciled

The repository partitions the enterprise twice. ADM has 30 domains; the capability map has 30 capabilities in 6 groups. The table maps each directive capability to both, and states where they diverge.

| Directive capability | ADM domain(s) | Capability(ies) | Divergence |
|---|---|---|---|
| Fund establishment and administration | ADM-02, 03, 04, 05, 21 | C1.1 | ADM separates establishment from activation (EST-11, EST-14). WF set has no fund-opening workflow (only WF-12 advisor onboarding). **Missing workflow** (W-NEW-01). |
| Contributions and asset acceptance | ADM-09 | C2.1, C2.2 | Aligned. ACH finality missing in both (TVC-023). |
| Investment management and custody | ADM-11 | C2.3, C2.4, C2.5 | Aligned. |
| Grant recommendations and approvals | ADM-12, 15 | C3.2, C3.3 | ADM-15 "spending and distribution" has no capability counterpart; recommendable capacity lives nowhere in C. Assign to C2.5 + C3.3. |
| Charity information management | ADM-13 | C3.1 | Aligned. |
| Compliance and legal | ADM-20, 07, 08 | C5.1, C5.2 | Aligned. |
| Accounting and reporting | ADM-10, 19 | C4.1, C4.2, C4.4 | Aligned. |
| Treasury and payments | (ADM-12 tail, ADM-30) | C3.4, C2.5 | ADM has no treasury domain. Payments sit under grant administration. |
| Donor and advisor services | ADM-16, 17 | C1.4 | Aligned. |
| Succession and authority | ADM-06 | C1.2 | Aligned. |
| Enterprise risk | ADM-20 | C5.x | No ERM risk register owner in either. Gap. |
| Security and privacy | ADM-28 | C5.6 | CISO under CTO (TVF-042). |
| Vendor and partner management | ADM-23, 30 | C5.5 | Partner (distribution) and vendor (supplier) are merged in C5.5. They need different controls. |
| Internal administration | — | — | Neither covers HR, payroll, procurement or the sponsor's own corporate books. Out of scope, but they are SOC 2 / ICFR dependencies. Recorded as a known exclusion. |
| Embedded distribution | (ADM-23) | C1.3? | Widget platform has no owning capability. **Assign one** (TVR-ORG-005). |
| Business intelligence | ADM-29 | C6.2 | Aligned. |
| AI governance | ADM-27 | C6.3, C6.4 | Aligned. |
| Audit and regulatory response | ADM-20, 22 | C4.4, C4.5 | Aligned. |

## 2. Challenging the proposed organization

| Proposed function | Necessary in this form? | Finding |
|---|---|---|
| One exception queue with skill routing (DD-013) | Yes. It removes departmental handoffs. | Keep, but the queue owner (COO) must not also own the metrics that judge the queue (TVF-043). |
| Controller accountable for C2.1, C3.4, C4.1, C4.2, C4.3 | **No.** Concentrates paying and checking. | Move reconciliation (C4.2) accountability outside the payment chain (TVC-028). |
| CRCO owns screening (C5.2) and the evidence ledger (C4.5) | **No.** The assurer owns the assurance record of its own controls. | Evidence ledger becomes a platform function with read-only CRCO access; independence via internal audit (TVF-041). |
| CISO reporting to CTO | Questionable at small scale; common in practice [I] | Allow, with a direct line to the Audit & Risk Committee (TVF-042). |
| COO owns exception queue, telemetry, digital twin, and chairs the change board | **No.** Self-assessment. | Split: telemetry and twin to an analytics function reporting to the CFO or CRCO (TVF-043). |
| Separate Grants Compliance and Complex-Asset specialist pools | Partly. E6 shows pooling saves 1 FTE (35→34); deferral saves more (25). | The deferral result depends on untested donor acceptance of execution windows (GAP-027/INN-37). Keep separate pools until measured. |
| Agent owners (4 FTE flat) | Plausibly understated; agent incidents scale with run volume, not linearly [I] | Recorded as assumption TVA-021 |
| "No departments" (INN-31) | **No** as stated: removes the structure that SoD relies on | Adversarial review already moved it to Test |

## 3. Responsibility allocation rule

Every activity is assigned to one of five executors. The rule decides which, in order:

1. **Human (H) – mandatory** if any of these is true:
   - the law places the judgment or liability on a person (§4966/4967 manager taxes, ER pre-grant inquiry, ED, sanctions true-match);
   - the action is irreversible and the evidence is ambiguous;
   - the decision is an exception to policy;
   - the decision changes authority, policy or agent permissions.
2. **Deterministic software (D)** if the rule can be written so that two independent implementations agree, and its inputs are authoritative and fresh.
3. **AI-assisted (P → H)** if the work is retrieval, summarization, extraction, translation or anomaly detection feeding a human or a D gate. The output can only add flags or drafts.
4. **Supervised agent (Cat 3)** for multi-step drafting or tracking where every external effect passes a D gate or a human.
5. **Autonomous agent**: **none** in any money-moving, legal-state or authority path. This matches DD-002, AI-14 and INV-A1..A5.

The baseline mostly follows this. The exceptions found are where *D decides with no human at any point in the chain*:
- below-cap donor-agent grants (TVC-026);
- TOTP-initiated routine grants (TVC-025);
- the benefit-risk timeout (TVC-007).

In each case a D gate is used where the rule-writing precondition (authoritative, fresh inputs) is not met for the *requester's identity*.

## 4. Separation of duties: minimum independent roles

The theoretical minimum number of distinct people needed to satisfy SoD-1..9 plus TVR-ORG-003, ignoring workload, is derived from which pairs of duties must be held by different people:

| Must be different people | Basis |
|---|---|
| Payee profile approver ≠ payment releaser | SoD-1, CTL-004/006 |
| Policy author ≠ policy publisher | SoD-2, DD-011 |
| Exception case raiser ≠ decider | SoD-4 |
| Privileged-access granter ≠ user | SoD-6 |
| Write-off approver ≠ break owner | SoD-7 |
| Agent owner ≠ model-risk sign-off | SoD-8 |
| Payment releaser ≠ reconciler (new) | TVR-ORG-003 |
| Sanctions officer clears true matches; must not be the grant approver on the same case | CTL-013 + inference |
| Board/committee approves DoA and policy delegations | REG-058 [K] |

**Corrected in review (architecture A1):** an earlier draft claimed a graph-colouring floor of four people. The pairwise constraints above form a **bipartite** conflict graph, so in principle **two** people satisfy them. The real floor comes from:
- absence coverage;
- reviewer independence (a reviewer must not report to the reviewed);
- workload.

**Unresolved disagreement (preserved):** the operations review (B-2) estimates that daily two-deep coverage of the payment chain needs **~10 or more people**. That chain is profile approver, releaser, independent reconciler, two PA-2 deciders excluding the releaser, and the sanctions decider. The org model says 8–10. This program has no derivation that settles it (TVA-022). A rota and on-call model is required (TVR-OPS-004).

## 5. Authority model

### 5.1 Sources of authority

| Source | Grants authority over | Can be delegated? | Example |
|---|---|---|---|
| Law | Sponsor exclusive legal control; manager liability | No | §4966(d)(2) |
| Sponsor governing instrument and board | Delegation of authority (DoA) to officers, committees, policies | Yes, by resolution | Grant approval delegated to policy version P-12 for class X (TVC-003) |
| Fund agreement | Advisory privileges, successor plan, restrictions | Only as the agreement permits | Primary advisor may appoint co-advisor if allowed |
| Sponsor policy | Thresholds, routing, eligibility | Through the policy gate | Routine threshold |
| Advisory privilege | Recommend grants or investments | Subset delegation (AUTH-03) | Advisor → agent principal (DD-017) |
| Partner contract | Distribution, identity federation, display | No financial authority | Wealth-firm portal |
| Workforce role | Operational actions within DoA | JIT, time-bounded (CTL-031) | Payment release |

### 5.2 Authority evaluation (every command)

`allowed(command) = tenant_ok ∧ legal_entity_ok ∧ scope_ok ∧ relationship_effective(t_exec) ∧ capability_granted ∧ delegation_chain_valid ∧ assurance(session) ≥ required(command, amount, recipient_novelty) ∧ no_hold(subject) ∧ SoD_ok(actor, subject_history) ∧ policy_version_effective(t_exec)`

Additions to the baseline. The tenant and legal-entity terms were added after round 2 S-3: one tenant's verification or change never becomes another tenant's decision input without that tenant's own control.
- the assurance term depends on **recipient novelty** as well as amount (TVC-025);
- `delegation_chain_valid` re-walks the chain at execution time (AUTH-I2);
- `SoD_ok` uses the subject's history (who created the payee, who raised the case).

### 5.3 Authority transitions that need explicit requirements

| Event | Requirement |
|---|---|
| Authorized user becomes unauthorized mid-session | AUTH-I1: maximum staleness window stated per channel (portal, widget, partner API, agent token). Commands are rechecked (AUTH-06). Displayed data is cleared on next poll or push (WS-1). |
| Death reported with past effective date | AUTH-I3; GR-8; TVC-033 |
| Advisor dispute | Fund `AuthorityState = Disputed`. Recommendations from the disputing parties held; sponsor-initiated actions (fees, investments) continue (AUTH-09). |
| Partner offboarded | All partner-derived sessions and launch grants revoked. Donors keep direct access. Partner-specific fee sharing stops at the effective date. |
| Staff terminated | IAM deprovision. Approvals they completed stay valid (made under authority at the time). SM-6 re-checks the **releaser's** authority and the grant state at payment, not that of past approvers (TVC-042). Their **queued** approvals not yet executed are re-routed. |
| Board delegation resolution amended | Policies relying on the old delegation are suspended at the effective time until re-linked (TVR-GOV-002). |
