# DAF UX: Design System and Navigation v0.2

Status: proposed, not implemented. Companion to UI inventory and three vertical-slice contracts. Architecture: F# / Limen WASM / Forma / Folio, API-first, mobile-first, accessible, balanced charcoal and bronze.

## Product experience rules
1. Every role begins at a task-oriented landing page, not a module directory.
2. Distinguish user recommendation, sponsor approval, funding, instruction, external processing, settlement and reconciliation in labels and status.
3. Never present market value as immediately spendable; show policy-calculated recommendable value separately.
4. All relevant actions reveal actor, fund, legal entity, effect, evidence, and required authority.
5. Avoid unnecessary form fields: prefill only from trusted verified sources, identify provenance, and allow correction where authorized.
6. Preserve work, but never silently submit a financial action.
7. No blank WASM startup; every app has its own logo, branded landing state, and recovery.
8. Use a shared design system and role-specific navigation, not independently themed apps.

## Navigation architecture
- Donor bottom navigation: Home / Giving / Investments / Documents / More. The current fund is always visible; fund switching is explicit.
- Professional advisor: Clients / Work / Giving / Investments / Reports. Client and legal context are prominently displayed.
- Operations: My Work / Team Queue / Search / Reports / More. Queue is the primary landing page.
- Finance: Overview / Reconcile / Liquidity / Accounting / Controls. Dense data views use desktop rail and mobile drilldowns.
- Compliance: Cases / Policies / Evidence / Controls / Reports.
- Platform administration: Partners / Tenants / Integrations / Access / Operations.
- Users with multiple roles see an explicit role switcher. Switching contexts invalidates previous scoped caches and disables stale actions.
- A universal search is **permission-scoped**. It must not reveal existence of restricted funds, donors, charities under investigation, or financial records via suggestions/counts.
- Deep links carry stable opaque identifiers but no secrets; unauthorized links return a safe response with no data leak.
- Breadcrumbs and browser history preserve user intent, not sensitive financial payloads.
- Navigation destinations are configurable only within a verified role and capability contract; white labeling cannot remove required legal disclosures or security steps.

## Forma component contract registry
Each component must have an F# type contract, semantic HTML/ARIA specification, keyboard behavior, touch behavior, loading/empty/error/stale states, responsive layout, telemetry classification, story/demo, unit tests, accessibility tests, and Playwright selectors.

| ID | Component | Mandatory behavior |
|---|---|---|
| FC-01 | AppShell | responsive navigation, landmarks, focus restoration, authenticated context |
| FC-02 | ContextSwitcher | legal entity/fund/role scope, warning on unsaved changes, cache reset |
| FC-03 | MoneyWithBasis | amount, currency, basis, as-of, precision, source, restrictions |
| FC-04 | StatusExplanation | state, reason, owner, expected next event, evidence link |
| FC-05 | ActionBar | one primary action, allowed secondary actions, pending/unknown feedback |
| FC-06 | WorkflowStepper | conditional steps, draft revisions, resume, conflict resolution |
| FC-07 | RecipientPicker | canonical identity, aliases, ambiguity, eligibility and freshness |
| FC-08 | AllocationEditor | dollars/percent, caps, sum validation, rounding, valuation basis |
| FC-09 | DecisionPackage | policy, evidence, contradictions, AI suggestions separately labeled |
| FC-10 | EvidenceViewer | source provenance, version, timestamp, accessible alternatives |
| FC-11 | CaseQueue | priority, owner, deadline, filters, responsive list/card mode |
| FC-12 | ActivityTimeline | actor, effective and recorded time, immutable event refs |
| FC-13 | TransactionReview | preview, irreversible effect, explicit confirmation, command reference |
| FC-14 | ReconciliationDiff | custody vs positions vs GL, tolerances, timing and source |
| FC-15 | LiquidityConstraintView | shared ancestors, claims, capacities, data freshness, overlap |
| FC-16 | FolioPreview | authorized export, print, scope, watermark, accessible structure |
| FC-17 | ErrorBoundary | recovery, saved-work indication, correlation reference, no secrets |
| FC-18 | NotificationCenter | priority, dedupe, preference and privacy-safe preview |
| FC-19 | AdaptiveDataView | dense desktop table, mobile summary/drilldown, equivalent actions |
| FC-20 | AIProvenance | model/version, sources, uncertainty, deterministic checks separate |
| FC-21 | AccessibleDialog | focus trap, close semantics, escape, destructive-action safeguards |
| FC-22 | FileIntake | format/size validation, malware status, provenance, progress |
| FC-23 | TaskProgress | meaningful step status, pause/unknown/failed recovery |
| FC-24 | FormField | label, help, validation, error summary, accessible autocomplete |

## Design tokens
Semantic tokens only: surface/background/raised, text-primary/secondary/disabled, border, focus, action-primary/secondary/destructive, status-success/warning/error/unknown, data-series, chart-patterns. Support light/dark and high-contrast themes, reduced motion, large text, and browser zoom. Charcoal/bronze is brand styling, not a substitute for WCAG contrast measurement. Brand logos must have alt text and safe fallback. Never encode status in color alone.

## Responsive contract
- 320px: one-column, no page-level horizontal overflow, reachable primary action, keyboard does not obscure action.
- 375px: donor primary reference size.
- 768px: compact tablet, flexible side panels.
- 1024px: operations split view where space permits.
- 1440px: multi-pane finance/operations views.
- At 400% zoom, preserve content and essential functionality with reflow. Specialized data grids may scroll internally with labeled alternative detail views.
- Touch interactions have non-gesture alternatives; drag-to-allocate must have editable numeric fields.

## State language and microcopy
Never say 'Completed' for a submitted recommendation. Use: Draft / Submitted / Under review / Approved / Funding in progress / Payment processing / Paid / Returned / On hold / Status unknown, with precise domain semantics and human explanation. Do not promise dates when providers cannot support them. For an unknown external outcome: 'We are checking the provider's status. Do not submit this again.' Only use this when an actual status investigation is initiated and tracked.

## Security and privacy
Avoid storing sensitive information in local storage by default. Draft persistence requires threat-model approval, encryption, expiry, and data minimization. Mask account numbers and payment destinations. Treat all external charity content and AI output as untrusted display data; never render unsanitized HTML. No unsafe action may depend on disabled buttons alone. Route changes must clear sensitive content before new data loads.

## Component acceptance gates
A component is Ready only when semantics, keyboard, touch, screen reader, contrast, reduced motion, loading/empty/error/stale, localization, RTL-readiness, telemetry privacy, and Playwright tests pass. Record measured results; a screenshot is not evidence of usability.
