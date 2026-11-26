# Widget W01: Fund Summary Detailed Contract v0.2

Status: proposed, not implemented. P0 read-only proof of architecture.

## User jobs
Donor: understand the fund's current position and what can be recommended.
Advisor: see permitted client fund information and next action without switching portals.
Sponsor: provide consistent financial terminology and access controls across distribution channels.
Partner: embed the experience without holding a duplicate financial truth.

## Widget variants
Compact (320px+): fund identity, value, available-to-recommend, freshness, one status link.
Standard (375px+): compact plus pending grants, recent activity, accessible action links.
Expanded (768px+): standard plus allocation/investment summary and period comparison when supported.
Advisor aggregate: multiple fund cards only if every fund is individually authorized; aggregate totals require validated consolidation and no pooled double count.
Variants must not silently change financial semantics. Small view may omit detail but must preserve warnings and basis.

## Information hierarchy
1. Trusted sponsor identity and fund name, role and scope.
2. Fund value with currency, methodology, valuation timestamp, source and caveat.
3. Available-to-recommend with sponsor policy version, denominator, restrictions, holds and as-of; show 'not available' rather than zero if calculation missing.
4. Pending recommendations, grants on hold and next action. Submitted vs approved vs paid states remain distinct.
5. Optional year-to-date giving, investment summary, contributions and Folio statement entry points, each independently authorized.
6. Staleness banner, source outage or incomplete data prominent before actions.

## Proposed read model
FundSummaryQuery { FundId; RequestedSections; Locale; Timezone; WidgetVariant }
FundSummaryView { FundId; SponsorDisplayName; FundDisplayName; UserCapacity; AsOf; SourceFreshness; PolicyVersion; FundValue: MoneyWithBasis option; Recommendable: MoneyWithBasis option; Restrictions: RestrictionSummary list; PendingGrantCounts: StatusCount list; YtdGiving: MoneyWithBasis option; AvailableActions: Capability list; WarningCodes: Warning list; ContextRevision; ETag }
MoneyWithBasis includes Currency, Value decimal, BasisKind, ValuationAsOf, ObservedAt, Source, Precision, Restrictions, IsEstimate. Do not use floating point for money.
Server filters fields and actions based on current effective rights. Null and unavailable are not zero.

## Interactions
- Refresh: explicit request, preserve last safe observation with stale badge until authoritative update.
- View detail: opens scoped widget route or trusted top-level handoff depending on manifest.
- Recommend grant: only if W02 permitted; host cannot force-enable.
- Select fund: require explicit user action and fresh authorization, no silent host-supplied switch.
- Open statement: separate authorized document workflow, no raw URL containing secrets.
- Copy financial values: include currency, as-of and basis in accessible text.
- If source data is incomplete, offer explanation and support reference, not unsupported 'recalculate'.

## Screen states
Loading, Ready, Empty (new/unfunded fund), Stale, Partial (custody feed missing), Restricted (view permitted but details masked), Unauthorized, ReauthRequired, Offline, ErrorRecoverable, FatalError, ContextChanged. In each state define heading, explanatory text, action and accessible announcement. Do not display cached prior-tenant data even briefly.

## Privacy and audit
No fund balances in parent messages, page title, URL, query string, untrusted analytics or support logs. Widget view telemetry may include anonymous latency, widget/version and safe status category; identifiable financial reads logged under sponsor-approved access policy. No screenshot/export unless explicitly authorized. Public host page analytics must not receive donor identifiers through bridge.

## Acceptance criteria
FS-01 shows fund value with currency and valuation basis.
FS-02 shows recommendable amount separately, with policy version and as-of.
FS-03 missing source does not render $0 or green status.
FS-04 pending recommendation not labeled approved/paid.
FS-05 advisor can see only independently authorized funds.
FS-06 fund switch clears old sensitive state before new fetch.
FS-07 multiple instances isolate sessions, events and focus.
FS-08 320px, 400% zoom, keyboard and screen reader tests.
FS-09 no sensitive values in host bridge or URL.
FS-10 Safari/Firefox/Chromium embed works or uses documented safe fallback.
FS-11 stale source warning persists across compact variant.
FS-12 server denies revoked permission despite cached widget state.
FS-13 sponsor theme cannot hide disclosures or fail contrast.
FS-14 no duplicate aggregate when pooled assets appear across accounts.
FS-15 clear response when fund is approved but not yet funded.
FS-16 no client-only calculation of recommendable amount.

## Performance and observability
Measure initial meaningful render, authentication handoff, source read, re-render, layout shift, and error rate by device/network. Set budgets after realistic baseline; do not assert arbitrary SLO. Track support cases caused by misinterpreted value vs available-to-recommend.

## P0 deliverable
A fully functional read-only hosted iframe with synthetic sandbox data, secure launch, independent authorization, stale/offline/error fixtures, and documented partner integration. No real donor data before threat review and tenant isolation verification.
