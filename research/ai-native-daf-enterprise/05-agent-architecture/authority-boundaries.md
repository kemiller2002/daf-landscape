# Authority boundaries

This file sets out what each agent may do. Every forbidden cell is enforced by the **absence of a tool** in the tool broker, not by an instruction in a prompt.

## 1. Action matrix

**Legend:**
- **✓** allowed
- **—** forbidden (no tool exists)
- **(s)** scoped to the subjects the requester or delegation may access

| Agent | Read | Propose | Flag (raise) | Clear flag | Write authoritative record | Instruct money / trade | Approve own output | Non-authoritative effect |
|---|---|---|---|---|---|---|---|---|
| AG-01 Recipient resolution | ✓ | ✓ | ✓ | — | — | — | — | — |
| AG-02 Benefit-risk flagger | ✓ | — | ✓ | — | — | — | — | — |
| AG-03 Sanctions triage | ✓ | ✓ (dossier) | ✓ | — | — | — | — | — |
| AG-04 Exception dossier | ✓ | ✓ | ✓ | — | — | — | — | draft only |
| AG-05 Orphan matcher | ✓ (s) | ✓ | — | — | — | — | — | — |
| AG-06 Break triage | ✓ | ✓ | ✓ | — | — | — | — | — |
| AG-07 Complex asset dossier | ✓ | ✓ | ✓ | — | — | — | — | draft only |
| AG-08 Document extraction | ✓ | ✓ | ✓ | — | — | — | — | — |
| AG-09 Service answer | ✓ (s) | — | ✓ | — | — | — | — | grounded reply; open case |
| AG-10 Advisor copilot | ✓ (s) | ✓ (unsubmitted draft) | — | — | — | — | — | draft only |
| AG-11 Discovery | ✓ | ✓ | — | — | — | — | — | — |
| AG-12 ER tracker | ✓ | — | ✓ | — | — | — | — | templated reminder; open case |
| AG-13 Policy drafting | ✓ (pseudonymized) | ✓ (diff) | — | — | — | — | — | sandbox back-test |
| AG-14 Regulatory monitor | ✓ | ✓ | ✓ | — | — | — | — | open case |
| AG-15 SOC analyzer | ✓ | ✓ | ✓ | — | — | — | — | open case |
| AG-16 Improvement | ✓ (aggregated) | ✓ (hypothesis) | — | — | — | — | — | twin simulation (sandbox) |
| AG-17 Related-party detector | ✓ | ✓ | ✓ | — | — | — | — | — |
| AG-18 Fraud explainer | ✓ | ✓ (explanation) | — | — | — | — | — | — |
| AG-19 Board narrator | ✓ (approved snapshots) | — | — | — | — | — | — | draft only |
| *Donor-side agent principals (external, DD-017)* | ✓ (s) | ✓ (recommendations within caps) | — | — | — | — | — (above `confirm_above` needs donor confirmation) | — |

**Each column contains no "✓" for:**
- clear flag;
- write authoritative record;
- instruct money or trade;
- approve own output.

## 2. Who may perform the forbidden actions

| Action | Permitted actor kinds | Mechanism |
|---|---|---|
| Clear a flag | `Rule` (a deterministic rule that explicitly supersedes the flag condition, e.g. the recipient was re-verified) or `Person` within delegated authority | Decision record with `flags_cleared`; actor kind is checked |
| Create `GrantApproved` | `Rule` (policy engine, routine path) or `Person` (exception path) | Grant decisioning module only |
| Create `PaymentInstructed` | `Rule` (payment gate), plus `Person` dual-control approval above threshold | Payment module only; requires a `GrantApproved` |
| Create `TradeInstructed` | `Rule` (rebalancer or mandate checker) | Investment module only |
| Write a ledger entry | `Rule` (posting rules) | Ledger module only; corrections by reversal |
| Publish a policy or change an agent scope | `Person` (change board), author ≠ approver | Policy registry |

## 3. Invariants tested by the F# proof of concept

These invariants are implemented as property and example tests in `models/Daf.Enterprise.Tests` (`AuthorityInvariantTests`). The parent workstream owns `models/`; this list is the specification it must satisfy.

| ID | Invariant |
|---|---|
| INV-A1 | For every event of type `GrantApproved`, `PaymentInstructed`, `TradeInstructed`, `PolicyPublished`, `AgentPermissionChanged` or `JournalPosted`, `Actor.kind ∈ {Rule, Person}`. An `Agent` actor is rejected at construction, so the type makes the illegal state unrepresentable. |
| INV-A2 | For every `Decision` with a non-empty `flags_cleared`, `Actor.kind ∈ {Rule, Person}`. |
| INV-A3 | No `PaymentInstructed` exists without a prior `GrantApproved` for each grant ID, and the grant is not canceled. |
| INV-A4 | No `GrantApproved` exists while the grant has an open (uncleared) flag, unless the approving actor is a `Person` whose authority covers that flag type. |
| INV-A5 | An agent tool-scope set contains only `Read`, `Propose`, `RaiseFlag`, `OpenCase`, `Draft` and `SendTemplated`. Constructing any other capability for an agent fails. |
| INV-A6 | A recommendation from an agent principal whose amount exceeds `confirm_above` cannot leave `AwaitingDonorConfirmation` except through a confirmation by the delegating `Person`. |
| INV-A7 | A `Person` cannot approve a case whose subject involves a party related to them (relationship graph), or a payment to a payee they created. |
| INV-A8 | An event chain deeper than 8 without a `Rule` or `Person` checkpoint is quarantined. |
