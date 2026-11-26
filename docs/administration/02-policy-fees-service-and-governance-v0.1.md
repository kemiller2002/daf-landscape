# DAF Administration: Policies, Fees, Service and Governance v0.1

Status: proposed. Sponsor policies and regulatory interpretation require legal/compliance signoff.

## Policy engine
POL-01 Versioned sponsor policy bundles with inheritance from sponsor -> legal entity -> fund product -> fund-specific approved exception.
POL-02 Rules have legal/policy authority, owner, effective interval, approval, reason, scope, evidence and sunset/review date.
POL-03 Deterministic evaluations return decision, rationale, source rules, data freshness, required human review and exceptions.
POL-04 Evaluate at relevant event time and command time; do not apply current rules retroactively without approved transition.
POL-05 Fund agreement restrictions and legal requirements cannot be overridden by ordinary configuration.
POL-06 Exception requests use distinct initiator/approver rights and expiry; emergency exception policy must be explicit.
POL-07 Simulate proposed policy changes against historic and current funds to identify impacted workflows and financial exposure.
POL-08 Notify affected parties where required; preserve prior policy versions for audit and reproducibility.
POL-09 A policy may set grant minimums, frequency, eligible recipient categories, restricted purposes, international grants, spending, investments, fees, inactivity, succession and closure.
POL-10 No unbounded scripting in partner-configurable policies; typed rules and constrained expressions.

## Fund spending and recommendable capacity
SPEND-01 Separate fund NAV, cash, projected liquidity, encumbrances, available-to-recommend, payout policy and endowed spending amount.
SPEND-02 Recommendable amount derived from sponsor-approved policy with version, as-of time and restrictions.
SPEND-03 Multi-investment grant allocation by dollar or percent with denominator, rounding, liquidation lag and shared custody constraints.
SPEND-04 Funding plans must account for pending grants, fees, reserved liquidity, restricted assets and pooled investments.
SPEND-05 Insufficient liquidity produces actionable plan or hold, not fabricated availability.
SPEND-06 Recurring grant recommendations require explicit schedule, future basis and revalidation each cycle.

## Fee engine
FEE-01 Multiple fee classes: sponsor administration, investment management, custody, advisor, platform, transaction, special asset, extraordinary service and negotiated fee.
FEE-02 Fixed, tiered, marginal tiered, flat percentage, minimum/maximum, breakpoint, asset-class-specific and custom contractual fee formulas.
FEE-03 Fee bases include daily/period average NAV, beginning/ending balance, eligible assets, committed assets or specified account class; precise valuation cutoff.
FEE-04 Accrual vs assessment vs invoice vs collection vs journal posting vs refund are distinct.
FEE-05 Proration for openings/closings, fee schedule changes, partial periods, asset transfers, nonbusiness days and multi-currency.
FEE-06 Waivers, rebates, negotiated discounts, grandfathered pricing, caps, subsidies and fee sharing require approval and evidence.
FEE-07 Layered fee transparency: avoid double counting sponsor, custody and investment charges; disclose indirect expenses as appropriate.
FEE-08 Sponsor revenue recognition and receivable/payable accounting integrate with full double-entry ledger.
FEE-09 Fee preview and explanation for donor and advisor; staff can reproduce exact calculation using versioned inputs.
FEE-10 Negative NAV, stale valuations, illiquid assets and insufficient cash require explicit exception workflow.
FEE-11 Fee corrections use auditable adjustments, not silent overwrite.
FEE-12 Revenue-sharing and related-party arrangements require conflict disclosure and sponsor governance review.

## Donor and advisor service
SVC-01 Unified CRM-like relationship timeline scoped by sponsor, fund, party and role.
SVC-02 Contact preferences, communication consent, accessibility needs and privacy constraints.
SVC-03 Case intake from portal, staff, API, phone or email with consent, ownership and SLA.
SVC-04 Case types: account access, grant status, contribution, investment, statement, fund agreement, succession, complaint, privacy request, error correction.
SVC-05 AI may summarize case history and draft response, but cannot invent completion or send sensitive disclosures without authorization.
SVC-06 Shared household service does not imply shared access to private donor or fund information.
SVC-07 Track escalation, reopens, complaints, regulatory issues, service recovery and root causes.
SVC-08 Donor retention and satisfaction metrics require privacy-safe aggregation and defined cohorts.
SVC-09 Knowledge articles, contextual help, approved scripts, and accessible contact paths.
SVC-10 Advisor servicing supports multi-client context with explicit boundaries and appropriate delegated rights.

## Governance and controls
GOV-01 Board, committee and delegated officer authority, with effective terms, quorum and recusal where required.
GOV-02 Committee decision packages, agendas, minutes, resolutions and supporting evidence.
GOV-03 Related-party and conflict-of-interest declarations, recusals and review.
GOV-04 High-risk grant and gift acceptance escalation with policy-based decision chain.
GOV-05 Periodic fund reviews, inactivity review, restrictions review, successor validity review and sponsor policy attestation.
GOV-06 SOC 2 evidence: control definition, owner, frequency, execution event, evidence, exception, remediation and reviewer signoff.
GOV-07 Incident response, business continuity, disaster recovery and third-party risk reviews.
GOV-08 Retention schedule and legal holds by record type and jurisdiction.
GOV-09 Regulatory reporting calendar, responsibility and source traceability; verify specific filing obligations by entity and jurisdiction.
GOV-10 Board-level operational metrics distinguish donor service, financial risk, grants, charity compliance and sustainability.

## Administration operating economics
ECON-01 Sponsor cost-to-serve by fund, household, advisor channel, asset class and grant activity, subject to privacy.
ECON-02 Activity-based costing for charity checks, complex gifts, investment servicing, grants, statements and exceptions.
ECON-03 Pricing scenario model including fee tiers, waivers, investment costs and service levels.
ECON-04 Avoid optimizing staff throughput at expense of charitable impact or control quality.
ECON-05 Measure exception rate, time to resolution, first-contact resolution, grant cycle time, sponsor net revenue, and cost per controlled outcome.
ECON-06 Cross-sponsor benchmarks only with lawful permissions, anonymization and adequate aggregation.

## UI requirements
Policy Studio (version compare, impact simulation, approval); Fee Schedule Editor (tier visualization, test fixtures, disclosure); Fee Assessment Review (lineage, basis, journal); Relationship Workspace (timeline, permissions, service); Committee Decision Package (evidence, conflict, votes); Control Evidence Dashboard (actual execution vs policy assertion); Sponsor Economics (fund and channel analytics).

## Tests
Tier boundary, marginal vs flat fee, valuation cutoff, proration, waiver expiry, insufficient cash, duplicate fee posting, FX, fee reversal, policy retroactivity, exception escalation, recusal, missing control evidence, household privacy, role change during service case.
