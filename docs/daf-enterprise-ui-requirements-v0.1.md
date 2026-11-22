# DAF Enterprise UI Requirements Catalog v0.1
Status: **PROPOSED / NOT IMPLEMENTED**. Canonical UI inventory for Limen (WASM), Forma (components), Folio (documents), mobile-first, API-first F# modular monolith. Charcoal/bronze is the preferred visual direction, subject to accessibility verification.

## Product rules
- Organize by human outcome, not database domain. No internal implementation terms on donor screens.
- Differentiate fund market value, available-to-recommend, projected liquidity, restricted resources, and settled cash. Every financial number shows basis, currency, as-of timestamp, and relevant limitations.
- Recommendations are not approvals; approvals are not settlements; AI suggestions are not verified facts.
- Mobile 320 CSS px target, 400% zoom/reflow, WCAG 2.2 AA, keyboard and screen-reader operation, reduced motion, accessible errors, contrast verified, no color-only status.
- Every Limen app has a meaningful nonblank startup state, branded landing page, offline/reconnect messaging, and safe recovery.
- All forms use server-authoritative validation, resumable encrypted drafts, optimistic concurrency, no duplicate submission, and precise confirmation IDs.
- Financial actions require server-side authorization and independently verified legal-entity context; hiding a button is not access control.
- Sensitive details never appear in analytics telemetry, general logs, AI prompts, or browser history.
- White-label branding cannot disable controls, weaken accessibility, or change financial semantics.

## Screen inventory
Fields: ID | Screen/capability | Roles | Primary information | Primary action | API contract (proposed).

### Donor & Advisor (16)

| ID | Capability | Roles | Information hierarchy | Primary action | API |
|---|---|---|---|---|---|
| D01 | Fund home | Donor,advisor | Value, available-to-recommend, pending actions | Recommend grant | FundSummary |
| D02 | Fund switcher | Multi-fund user | Authorized funds and current context | Switch fund | FundAccess |
| D03 | Grant recipient search | Donor,advisor | Identity, eligibility, history | Select charity | CharitySearch |
| D04 | Grant amount | Donor,advisor | Fixed/percent basis, valuation timestamp | Set amount | GrantDraft |
| D05 | Grant funding allocation | Donor,advisor | Cash, portfolio, position, restrictions | Allocate dollars/percent | FundingPreview |
| D06 | Grant review & submit | Donor,advisor | Recipients, totals, limits, consequences | Submit recommendation | GrantCommand |
| D07 | Grant tracking | Donor,advisor | Approval, funding, payment as separate states | View details | GrantStatus |
| D08 | Contribution initiation | Donor,advisor | Cash/securities/complex gift intake | Save proposed gift | ContributionDraft |
| D09 | Contribution tracking | Donor,advisor | Accepted, received, valued, acknowledged | View next steps | ContributionStatus |
| D10 | Investment overview | Donor,advisor | Holdings, performance, mandates, as-of dates | Explore portfolio | PortfolioRead |
| D11 | Giving history | Donor,advisor | Grants, reversals, annual totals | Filter/export | GivingHistory |
| D12 | Statements & documents | Donor,advisor | Statements, acknowledgment, report periods | Preview/download | FolioReport |
| D13 | Family advisory access | Authorized fund owner | Rights, successors, effective dates | Invite/revoke | AuthorityCommand |
| D14 | Recurring giving | Donor,advisor | Schedules, recalculation basis, approval status | Create/pause | RecurringGrant |
| D15 | Notifications & messages | All external users | Requests, delivery, communication history | Respond | Notifications |
| D16 | Profile & preferences | All external users | Accessibility, alerts, contact settings | Update preferences | UserProfile |

### Operations (18)

| ID | Capability | Roles | Information hierarchy | Primary action | API |
|---|---|---|---|---|---|
| O01 | Work inbox | Grant/operations staff | Prioritized work, owner, deadlines, evidence | Open case | CaseQueue |
| O02 | Case detail | Operations | Facts, blockers, timeline, actions | Resolve/escalate | CaseRead |
| O03 | Grant approval review | Grant officer | Recipient, purpose, restrictions, authority | Approve/hold/decline | GrantDecision |
| O04 | Charity identity resolution | Analyst | Aliases, EINs, duplicates, legal relationships | Confirm identity | CharityRegistry |
| O05 | Charity eligibility | Compliance analyst | Rules, source freshness, uncertainty | Decide/escalate | EligibilityDecision |
| O06 | Charity evidence viewer | Analyst | Sources, provenance, version, contradiction | Accept/reject evidence | EvidenceRead |
| O07 | Charity payment verification | Payment operations | Destination changes, independent checks | Verify destination | PaymentDestination |
| O08 | Contribution acceptance | Gift officer | Asset, restrictions, liabilities, approvals | Accept/decline | ContributionDecision |
| O09 | Complex asset diligence | Gift/compliance | Valuation, legal, UBTI, disposition | Assign reviews | AssetDiligence |
| O10 | Grant funding planner | Operations/treasury | Cash, reserves, liquidation, settlement | Prepare plan | FundingPlan |
| O11 | Payment preparation | Payment operations | Authorized amount, verified recipient, hold status | Prepare instruction | PaymentCommand |
| O12 | Payment tracking | Payment operations | Attempts, unknown states, returns | Investigate | PaymentStatus |
| O13 | Reconciliation exceptions | Finance operations | Custody vs investment vs ledger | Assign exception | Reconciliation |
| O14 | Exception resolution | Finance operations | Difference, evidence, allowed corrections | Propose adjustment | ExceptionCommand |
| O15 | Operational timeline | Operations/audit | Actor, action, effective/recorded time | Inspect evidence | AuditEvents |
| O16 | Bulk work review | Operations lead | Selected items, mixed permissions, individual outcomes | Batch eligible actions | BulkCommand |
| O17 | Service requests | Service team | Donor inquiries, SLA, linked cases | Respond/route | ServiceCase |
| O18 | Communication templates | Operations lead | Approved templates, audience, version | Publish template | TemplateAdmin |

### Enterprise & Investment (20)

| ID | Capability | Roles | Information hierarchy | Primary action | API |
|---|---|---|---|---|---|
| E01 | Executive overview | Sponsor executive | Service, assets, grants, exceptions, controls | Drill into risk | ExecutiveMetrics |
| E02 | Sponsor/legal entity switch | Authorized staff | Entity, legal role, tenant context | Change context | EntityAccess |
| E03 | Accounting workbench | Finance | Journals, balances, periods, source evidence | Review posting | LedgerRead |
| E04 | Period close | Controller | Reconciliations, blockers, approval chain | Close period | PeriodCommand |
| E05 | Liquidity dashboard | Treasury | Confirmed vs unsettled vs reserved cash | Inspect resource | TreasuryRead |
| E06 | Reservation explorer | Treasury | Ancestors, commitments, holds, revisions | Investigate hold | ReservationRead |
| E07 | Custodian accounts | Custody team | Ownership, capability, balances, feed freshness | Inspect account | CustodyRead |
| E08 | Custodian integration health | Integration team | Read/trade capability, sync, incidents | Reconcile connection | ProviderHealth |
| E09 | Portfolio overview | Investment manager | Mandates, performance, holdings, restrictions | Review portfolio | PortfolioRead |
| E10 | Mandate management | Investment governance | Permissions, effective dates, approvals | Propose change | MandateCommand |
| E11 | Trade proposal review | Investment manager | Authority, liquidity, risk, settlement | Authorize/hold | TradeCommand |
| E12 | Investment pool administration | Pool admin | NAV, unit ledger, subscriptions, redemptions | Review valuation | PoolRead |
| E13 | AUM/AUA methodology | Finance executive | Scope, exclusions, double-count rules | Approve methodology | AssetMeasure |
| E14 | Fee management | Finance | Sponsor, manager, custody, platform fee bases | Review calculation | FeeEngine |
| E15 | Compliance policy studio | Compliance lead | Rule versions, scope, effective dates | Propose policy | PolicyAdmin |
| E16 | Audit & SOC 2 evidence | Security/audit | Control execution, evidence, owner, gaps | Inspect/export | ControlEvidence |
| E17 | Tenant & partner administration | Platform admin | Brand, partner contracts, isolation | Configure partner | TenantAdmin |
| E18 | Access & delegation | Security admin | Roles, legal scopes, delegation history | Grant/revoke | AuthorityAdmin |
| E19 | Reporting studio | Authorized report user | Scope, filters, as-of, accessibility | Generate Folio report | ReportEngine |
| E20 | System operations | Platform ops | WASM health, API, queue, recovery, incidents | Investigate | OpsHealth |

## Reusable Forma patterns
F01 AppShell: authenticated legal-entity/fund context, responsive nav, role-switch, focus restoration.
F02 MoneyWithBasis: amount, currency, valuation/settlement basis, as-of, restrictions, drilldown.
F03 StateExplanation: human-language state, reason, owner, next action, expected update, provenance.
F04 DecisionPackage: evidence, contradictions, policy, confidence, authorizations, decision history.
F05 WorkflowStepper: resumable drafts, conditional steps, back navigation, validation summary.
F06 AllocationEditor: amount/percentage, rounding, valuation basis, sum constraints, locked resources.
F07 CaseQueue: accessible sortable/filterable list with mobile card projection, bulk safeguards.
F08 EvidenceViewer: source metadata, immutable snapshots, citation and discrepancy display.
F09 ActivityTimeline: recorded/effective time, actor, event type, privacy-safe audit trail.
F10 TransactionReview: irreversible consequence summary, explicit confirmation, idempotency key.
F11 ReconciliationDiff: custodian/investment/ledger comparison and exception explanation.
F12 FolioPreview: accessible report preview, print, export, redaction and permission checks.
F13 NotificationCenter: actionable, deduplicated, user-controlled channels and delivery.
F14 StatusShell: loading, empty, partial, stale, error, offline, unauthorized, maintenance.
F15 SecureContextSwitcher: no cross-tenant stale cache, legal scope and role visible.
F16 AdaptiveDataView: dense desktop table and equivalent mobile summary/drilldown.

## Mandatory per-screen state contract
Each screen must specify: Loading, Ready, Empty, Stale, Partial, ValidationError, Conflict, Unauthorized, Offline, RecoverableError, FatalError, and Success (where action exists). Do not show stale data as live; no blank WASM loading page. Preserve unsent user work; warn before destructive navigation. Show support correlation reference for recoverable failures, without exposing secrets.

## Cross-cutting acceptance requirements
UI-001 Responsive at 320/375/768/1024/1440 CSS px; no loss of critical actions.
UI-002 WCAG 2.2 AA target with keyboard, screen-reader, touch target, zoom/reflow, reduced-motion tests.
UI-003 All consequential commands require explicit preview of actor, fund, amount, recipients, and effects.
UI-004 Duplicate taps and network retries return same command outcome; never duplicate financial instructions.
UI-005 Drafts survive navigation, reload, and interrupted connection without silently submitting.
UI-006 Errors distinguish unsaved, saved, accepted, pending, and settled outcomes.
UI-007 Currency, percentage, date, time zone, and as-of basis explicit; never ambiguous AUM vs AUA.
UI-008 Search returns verified identities with aliases and confidence; ambiguous charities require selection/verification.
UI-009 AI outputs labeled as suggested, with citations and uncertainty; user can inspect source evidence.
UI-010 Tenant/legal context changes clear or partition cache, notifications, query state, and search.
UI-011 Mobile workflows have equivalent capability, not merely horizontally scrolling desktop tables.
UI-012 Folio print/export accessible and authorized; exports watermark as-of and scope.
UI-013 Component-level unit, interaction, accessibility, and Playwright E2E tests mandatory.
UI-014 Every SOC 2 claim linked to executed control evidence, not static policy prose.
UI-015 UI performance budgets set after device/network baselines; measure WASM startup and interaction latency.
UI-016 No loading spinner without explanatory text and recoverable timeout path.
UI-017 Financial operations use dual confirmation where policy requires, never AI self-approval.
UI-018 Privacy-by-default telemetry and data minimization; sensitive destination data masked.
UI-019 Consistent design tokens and branded app identity across donor, operations, and enterprise.
UI-020 Internationalization and readable content including legal plain-language explanations.

## Priority and consolidation
P0 vertical workflows: D01-D07, O01-O07, O10-O12, E02-E06, E16, E18; foundation F01-F06, F08-F10, F14-F16.
P1: contributions D08-D09 and O08-O09; reconciliation O13-O15; custody E07-E08; portfolio E09; reporting D11-D12/E19.
P2: complex investment and administration E10-E15/E17/E20; service and recurring D13-D16/O16-O18.

Screen rationalization: D03-D06 form one grant wizard with reusable steps, not four required routes; O04-O06 form one verification case workspace; O11-O12 one payment case view; E03-E04 one accounting workspace with close workflow. This reduces the number of top-level navigation destinations while retaining 54 separately testable capabilities.

## Critical journeys and failure tests
J01 Donor recommends grant by fixed amount; J02 percent-of-fund with valuation basis; J03 multi-portfolio allocation totals 100%; J04 resume offline draft; J05 donor loses authority mid-draft; J06 duplicate submission after timeout; J07 charity identity ambiguity; J08 eligibility revoked after approval; J09 bank destination changed; J10 payment unknown state; J11 partially settled grant; J12 two grants compete for pooled liquidity; J13 custodian stale holdings; J14 accounting close concurrent posting; J15 role/tenant switch with stale client cache; J16 AI-suggested unsupported evidence; J17 accessible screen-reader grant flow; J18 400% zoom operational case; J19 Folio accessible report; J20 security audit of role escalation.

Each journey requires a test fixture, screen-state assertions, API-contract assertions, audit evidence, and a documented result. Proposed statuses are **not tested**.

## Assumption challenges
A. 54 capabilities do not imply 54 independent pages: optimize navigation by intent.
B. A dashboard is not a substitute for a next-action queue; measure task completion.
C. AI summaries may obscure contradictions; evidence-first inspection is required for regulated decisions.
D. Mobile-first does not mean dense reconciliation is best on a phone; preserve function with adaptive progressive disclosure.
E. White-label flexibility cannot be allowed to fragment semantic behavior or accessibility.
F. "Available to recommend" is a sponsor policy calculation, not simply cash minus reservations.
G. "Instant" grant status is often impossible because external charity, custody, and payment systems are asynchronous.

## Design review / release gate
No screen is implementation-ready until: actor and purpose, data contract, states, permissions, error paths, mobile and desktop layout, accessibility, telemetry privacy, and executable tests are specified. No production gate passes on mockup appearance alone.

## Integrated Giving Plans extension (2026-11-22, proposed)

This extension links the canonical UI inventory to typed registry GP-01..GP-20, CA-180-01/05/08, CON-REC-05, GR-DEL-01 and GR-EXT-01 in `research/theoretical-enterprise-validation/16-registers/requirements.csv`. The full challenged reasoning is in `docs/integrated-giving-plans-decision-record-v0.1.md`. Existing screen IDs are retained.

| Existing screen | Added user capability | Required states and safeguards | Registry |
|---|---|---|---|
| D01 Fund home | Upcoming contribution and grant; forecast versus available | pending, held, blocked, stale, completed | GP-05;GP-11 |
| D02 Fund switcher | Authorized plan/fund allocation context | cross-fund authorization and isolation | GP-16;GP-19 |
| D03 Recipient search | Current assurance and purpose eligibility | last verified, adverse signal, unknown, ineligible | CA-180-01;CA-180-05;GP-06 |
| D06 Grant review | Recurring/future schedule, external reference, delivery and fees | separate grant and fee amounts, no implied approval | GP-03;GP-10;GR-EXT-01;GR-DEL-01 |
| D07 Grant tracking | Schedule occurrence, custody, payment and settlement | issued is not delivered; delivered is not cleared | GP-03;GR-DEL-01 |
| D08 Contribution initiation | $10/payday recurring funding and mandate consent | biweekly vs semimonthly; fees; revocation | GP-02;CON-REC-05 |
| D09 Contribution tracking | Each debit attempt, clearing, return, tax acknowledgment | pending not available, returned not accepted | GP-09;GP-20 |
| D14 Recurring giving | Unified giving plan wizard and calendar | create, edit, pause independently, preview shortfall, next action | GP-01..GP-08;GP-11;GP-12 |
| D15 Notifications | Shortfall, charity hold, mandate/fee change | mandatory notices and digests | GP-13 |
| O03/O05/O06 | Reusable charity assurance and exception-only vetting | zero-touch clean renewals, adverse signals, evidence lineage | CA-180-01;CA-180-05;CA-180-08;GP-14 |
| O10/O11/O12 | Scheduled funding, check custody, unknown payment | no blind retry, no projected cash spending | GP-07;GR-DEL-01 |
| O13/O14/O15 | Fee, debit, grant and correction evidence | immutable accounting corrections and audit | GP-17 |

### New composite journey J-GP-01
Select authorized fund -> choose automatic contributions (amount, true pay frequency, first date, mandate) -> optionally add grant schedule(s) (recipient, purpose, amount, frequency, delivery, external ID) -> display 12-month cash/fee/shortfall preview -> review sponsor rules and consent -> submit once with idempotency -> show plan calendar and independent contribution/grant statuses. An incoming contribution does not automatically create a grant payable. When a grant lacks eligible liquidity, default to hold and notify, not an unexpected debit.

### Build gates
- Verify every new registry ID has a UI/API mapping, authorization rule, normal/error/unknown state and acceptance test.
- Test small-screen and assistive-technology completion of a $10 biweekly mandate and a quarterly $100 grant with a projected shortfall.
- Test fee increase beyond consent ceiling, charity adverse event within the 180-day cycle, duplicate debit tick, ACH return, revoked authority, and cross-sponsor widget access.
- Sponsor legal, CFO/CPA, treasury, and compliance decisions remain gates; no design document constitutes production authorization.
