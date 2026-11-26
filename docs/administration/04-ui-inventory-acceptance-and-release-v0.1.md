# DAF Administration: UI Inventory, Acceptance and Release v0.1

Status: proposed UI requirements, no implemented screens. Builds on 54-capability enterprise UI inventory; these are additional administration capabilities and may be consolidated into shared workspaces.

## Administration UI capability inventory
| ID | Capability | Primary actor | Primary decision/action |
|---|---|---|---|
| A01 | Sponsor setup | Platform admin | activate legal entity and jurisdiction |
| A02 | Fund product catalog | Product/policy owner | approve product and defaults |
| A03 | Prospect intake | Service/onboarding | qualify and open application |
| A04 | Fund application wizard | Donor/advisor | complete application |
| A05 | Onboarding review queue | Fund admin | accept/hold/reject |
| A06 | Agreement template library | Legal/policy | approve template |
| A07 | Agreement execution tracking | Onboarding | verify executed terms |
| A08 | Fund activation checklist | Fund admin | activate only after gates |
| A09 | Fund administration home | Fund admin | understand status and tasks |
| A10 | Party/relationship graph | Service/compliance | resolve relationships |
| A11 | Advisor rights matrix | Authorized admin | grant/revoke rights |
| A12 | Successor plan editor | Authorized advisor | nominate successors |
| A13 | Successor verification case | Sponsor/legal | activate on verified trigger |
| A14 | Restrictions editor | Sponsor/legal | approve constraints |
| A15 | Policy Studio | Sponsor policy | version and simulate |
| A16 | Policy exception review | Sponsor officer | approve/decline exception |
| A17 | Contribution acceptance | Gift officer | accept gift |
| A18 | Complex asset diligence | Gift/legal | evaluate liabilities |
| A19 | Fee schedule editor | Finance | configure pricing |
| A20 | Fee preview and simulation | Finance/service | explain impact |
| A21 | Fee assessment workbench | Finance | approve and post |
| A22 | Relationship service workspace | Service | resolve inquiry |
| A23 | Donor communication center | Service | send authorized notice |
| A24 | Document vault | Authorized users | view/version/retain |
| A25 | Statement/acknowledgment studio | Finance/service | produce Folio output |
| A26 | Sponsor governance queue | Board/committee | review decision |
| A27 | Conflict and recusal register | Compliance | record and enforce |
| A28 | Periodic fund review | Sponsor compliance | attest/resolve |
| A29 | Fund amendment workspace | Sponsor/legal | execute change |
| A30 | Fund merge/split planner | Sponsor/finance | model conservation |
| A31 | Sponsor transfer workspace | Sponsor/legal | authorize migration |
| A32 | Fund closure workbench | Sponsor/finance | close with no open obligations |
| A33 | Migration import review | Migration team | reconcile legacy records |
| A34 | Integration capability center | Integration admin | verify provider scope |
| A35 | Sponsor economics dashboard | Executive/finance | analyze cost to serve |
| A36 | Administration control evidence | Auditor/compliance | verify executed controls |

## Critical screen contracts
A04 Application: adaptive intake, document uploads, fund type and sponsor, advisors/successors, agreement preview, privacy, save/resume. Never imply fund active upon submission.
A08 Activation: signed agreement, sponsor acceptance, verified party rights, policy restrictions, ledger book, initial gift status, custody readiness; show each blocker with owner and evidence.
A11 Rights matrix: person, capacity, legal scope, effective window, delegator, evidence, dual control, revocation preview, pending work impact.
A13 Succession: verified trigger, evidence, legal review, conflicting nominations, interim holds, effective activation, notices.
A15 Policy Studio: typed rule, effective dates, simulation, impacted funds, exceptions, approvals and rollback.
A19 Fee editor: tier and marginal math, fee basis, proration, waivers, min/max, examples, versioning, approval.
A21 Fee assessment: source NAV, cutoff, calculation trace, amount, account, ledger posting, correction, explanation.
A30 Merge/split: donor intent, agreement/restrictions, open grants, assets, unitization, cash and liabilities, fees, approvals, conservation proof.
A32 Closure: grant obligations, unsettled payments, holdings, fees, liabilities, retention, notices, final accounting, authorized closure.
A33 Migration: imported source vs canonical value, identity conflicts, unreconciled balance, signed agreements, manual correction with provenance.

## Proposed API command boundaries
POST /commands/fund-applications
POST /commands/fund-approvals
POST /commands/fund-activations
POST /commands/agreement-amendments
POST /commands/authority-grants
POST /commands/authority-revocations
POST /commands/successor-activations
POST /commands/policy-revisions
POST /commands/policy-exceptions
POST /commands/fee-assessments
POST /commands/fund-mergers
POST /commands/fund-splits
POST /commands/fund-transfers
POST /commands/fund-closures

Every command must include stable idempotency key, expected revision and canonical request hash; server derives principal/tenant/legal authority. Return receipt with accepted/rejected/unknown state, correlation ID and evidence references. No direct UI-to-database privileged access.

## 40 proposed acceptance tests
AD-T01 application resume; AD-T02 duplicate prospect detection; AD-T03 wrong fund type classification; AD-T04 expired agreement template; AD-T05 unsigned agreement blocks activation; AD-T06 sponsor rejection blocks activation; AD-T07 initial contribution pending; AD-T08 duplicate activation; AD-T09 advisor cross-fund access denied; AD-T10 authority revoked mid-action; AD-T11 successor nomination does not activate; AD-T12 competing successors; AD-T13 incapacity evidence restricted; AD-T14 backdated amendment; AD-T15 conflicting restrictions; AD-T16 policy simulation; AD-T17 policy exception unauthorized; AD-T18 historical policy reproducibility; AD-T19 fee tier breakpoint; AD-T20 marginal fee vs flat fee; AD-T21 fee proration; AD-T22 waiver expiry; AD-T23 stale NAV fee hold; AD-T24 duplicate fee posting; AD-T25 fee reversal; AD-T26 fund merge conservation; AD-T27 split allocation conservation; AD-T28 closure with open grant blocked; AD-T29 closure with unknown payment blocked; AD-T30 sponsor transfer authority; AD-T31 legal hold retention; AD-T32 imported fund balance reconciliation; AD-T33 imported advisor rights proof; AD-T34 cross-tenant donor search; AD-T35 service case privacy; AD-T36 AI fabricated agreement clause; AD-T37 AI prompt injection; AD-T38 320px onboarding; AD-T39 400% zoom rights matrix; AD-T40 accessible Folio acknowledgment.

Tests are specifications only; none reported executed.

## Readiness and dependencies
ADMIN-G0 Legal sponsor model, fund classification and authority taxonomy approved.
ADMIN-G1 Domain contracts and migrations reviewed with realistic legacy cases.
ADMIN-G2 Form components, accessible screens, mocked API and all error states tested.
ADMIN-G3 Policy engine deterministic and versioned; fee math and agreement constraints validated.
ADMIN-G4 Trusted command boundary, tenant isolation, SoD and bitemporal authority verified.
ADMIN-G5 Financial ledger, liquidity, settlement, provider recovery and reconciliation gates passed.
ADMIN-G6 End-to-end fund lifecycle and migration rehearsals pass with independent evidence.
ADMIN-G7 Privacy, retention, SOC 2 operating evidence and incident exercises verified.
ADMIN-G8 Sponsor/legal/compliance approval for production activation.

## Remaining unknowns that block detailed implementation
Exact sponsor legal structure and jurisdictions; fund types offered; sponsor discretion/authority policy; eligibility rule set; gift acceptance thresholds; advisory/succession rules; fee formulas; accounting policy; custody contract capabilities; payment provider arrangements; records retention; approved tax acknowledgments; regulatory filing obligations; permitted white-label partner authority. Do not invent answers to these questions.
