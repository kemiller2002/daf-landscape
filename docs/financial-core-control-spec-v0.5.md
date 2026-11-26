# DAF Financial Core: Consolidated Control Specification v0.5

Status: **DESIGN / NO-GO FOR PRODUCTION FINANCIAL EXECUTION**. Consolidates local v0.1–v0.4 design work. This repository is the DAF research and architecture repository, not a verified deployable financial application. No PostgreSQL, .NET, Strata, custodian, or payment-provider integration tests have passed.

## Architecture invariants

1. Legal ownership, advisory rights, custodial holdings, portfolio positions, and ledger balances are different records. They must reconcile, never overwrite one another.
2. A tenant is an isolation boundary, not necessarily a legal entity. Every financial command must resolve an authorized principal, tenant, legal entity, fund/mandate, and effective-dated scope.
3. Posting is balanced, immutable, idempotent, and restricted to approved accounting periods. Corrections are new reversals/adjustments.
4. Confirmed cash, unsettled proceeds, projected liquidity, active reservations, and external payment attempts are separate concepts.
5. No cash can become spendable merely because a reservation is consumed. Settlement must atomically apply the cash movement, accounting posting (when policy requires), and reservation transition, or remain unresolved.
6. Availability checks must cover all constrained ancestors of a resource, including fund, pool, legal owner, and custodial account. Locks are acquired in a deterministic order. Shared ancestor capacity is never double-allocated.
7. External provider timeout means **unknown**, not failed. Query and reconcile before any retry. Stable provider idempotency keys and attempt identities are required.
8. Domain events and transactional outbox entries commit with the authoritative mutation. Event replay never repeats an external side effect.
9. AI agents have no independent financial authority. Proposed actions pass the same deterministic policy and human authorization gates as all other commands.
10. Audit logs must record actual control execution and evidence, not merely statements that the organization follows SOC 2 policies.

## Critical corrections to earlier prototypes

- The v0.3 `treasury.transition_reservation` implementation decreases `resource.reserved_amount` on Consume without proving a corresponding cash debit. **Do not expose or use it for payments/trades.**
- v0.2/v0.3 privileged SQL functions accept caller-provided actor/authority IDs; non-null IDs are not proof of authority. **Revoke EXECUTE until replaced with independently verified authorization.**
- `treasury.resource_constraint` records parent relations but does not enforce parent capacity or prevent cyclic constraints. **No pooled reservation execution until fixed.**
- Tenant RLS using a custom session variable does not authenticate who set it. SECURITY DEFINER functions and connection-pool reuse need a trusted role/session strategy and adversarial tests.
- An external balance feed is an observation, not settled cash. Reconciliation discrepancies require explicit holds and reviewed resolution.
- A closed accounting period must block backdated postings through every write path, not only one posting function.

## Canonical financial command

Command envelope: command_id, idempotency_key, tenant_id, legal_entity_id, principal_id, capability, aggregate_id, expected_revision, request_hash, effective_at, correlation_id, causation_id, evidence_refs, policy_version. Trusted authentication and scope are resolved server-side. Same key + same hash returns original result; same key + different hash is rejected.

Command lifecycle: Received -> Authorized -> Reserved -> Submitted (if external) -> Observed -> Settled -> Reconciled. Alternative states: Denied, Held, Unknown, Failed, Returned, Compensating. A compensating action is a new transaction, not history deletion.

## Settlement conservation invariant

For each constrained cash resource, define available cash as confirmed eligible cash less active/held encumbrances. On confirmed settlement of amount X, in **one authorized database transaction**: record unique external evidence, reduce confirmed cash by X, reduce the matching outstanding reservation by X, record the required journal posting and outbox event, and commit. If any step fails, preserve the prior reservation and enter a recoverable exception state. Never release an Unknown external instruction.

## Gate sequence

G0: accounting/legal policies and role ownership approved.
G1: schema and migrations run against a real PostgreSQL instance.
G2: restricted roles and tenant isolation penetration tests pass.
G3: balanced journals, period close, reversal, idempotency tests pass.
G4: concurrent fund/pool/account capacity tests pass.
G5: settlement crash/retry/unknown-state tests pass.
G6: custody/provider capabilities and contractual authorization verified.
G7: reconciliation and incident recovery drills pass.
G8: SOC 2 control-to-evidence collection and independent review pass.
G9: controlled pilot approved; payment and trade execution remain separately gated.

## Next engineering work

1. Implement a **new** settlement-coordinated command boundary; do not patch unsafe procedures by adding comments.
2. Add hierarchical resource-capacity enforcement, acyclic constraints, obligation caps, and deterministic multi-resource locking.
3. Establish trusted authorization using non-bypassable service/database privileges and signed/verified authority context as appropriate; test pool/session reuse.
4. Add command inbox, provider attempt state machine, outbox dispatch, and reconciliation-driven retry rules.
5. Implement real PostgreSQL integration and F# property-based tests, including crash injection.
6. Complete contribution, charity, grant, custody, and payment migrations after the financial kernel passes its gates.

## Assumptions to challenge

- PostgreSQL is a proposed persistence baseline, not a confirmed Strata contract.
- Full event sourcing is not required; immutable journals, domain events, and authoritative relational state may be sufficient.
- Fund-level liquidity cannot guarantee account-level availability.
- AUM, AUA, and regulatory AUM require distinct definitions and consolidation rules.
- Sponsor, manager, and platform legal roles require counsel review before activating regulated capabilities.

## Provenance and status

This document merges the design conclusions from the local DAF Financial Core v0.1–v0.4 packages into the architecture repository. It **does not** claim that the source ZIP packages, executable SQL/F# implementation, tests, or deployment were committed to GitHub. Those remain local design artifacts pending code review and runtime verification.
