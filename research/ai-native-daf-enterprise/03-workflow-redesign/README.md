# 03 Workflow redesign

This directory specifies 24 end-to-end workflows that cross traditional department lines, and one reference journey that runs through the whole enterprise (addendum §24). Each workflow sets the legacy approach beside the redesigned one.

## The rule: change the mechanism, not the names

A redesigned step only counts if it changes the mechanism. Replacing "reviewer checks the IRS list" with "agent checks the IRS list" is a rename. It is not a redesign.

Each workflow below must remove at least one of the following *causes* of legacy work:

| Legacy cause | Redesigned mechanism | Where it appears |
|---|---|---|
| Information arrives without identifiers, so people match it by hand | Intents and idempotency keys issued *before* the money moves | WF-01, WF-02, WF-04, WF-19 |
| Point-in-time lookups repeated on every transaction | **Continuous eligibility**: facts are pre-computed on every IRS or OFAC publication and pushed into in-flight work | WF-01, WF-05, WF-09 |
| Review queues that ignore risk | **Exception-only routing** under **policy-as-code**; people see only refer or flag cases, with a prepared dossier | WF-01, WF-05–WF-08 |
| Status unknown across departments | One durable **shared state machine** per grant, case and change, readable by donor, advisor, recipient and staff | all |
| Batch runs (weekly payments, nightly NAV, month-end close) | **Event-driven** processing with fan-out caps and a continuous close | WF-05, WF-17–WF-20 |
| Prose policy interpreted by each person | Versioned rules, back-tested against history, approved by someone other than the author | WF-22, WF-23 |
| Determinations redone for every grant | Reusable enterprise assets: shared equivalency determinations, verified payment profiles, structured successor plans | WF-06, WF-10, WF-13 |
| Manually curated board reporting | Generated evidence snapshots, kept separate from management commentary | WF-24 |

## Method

Every workflow specification contains the same sections:

1. Outcomes and legacy departments.
2. Legacy approach, labeled [I] where inferred. No sponsor publishes its procedures or effort (Q-N03). Repository evidence is cited where it exists.
3. Redesigned approach:
   - trigger events (from [`../06-data-and-knowledge/events.csv`](../06-data-and-knowledge/events.csv));
   - the state machine;
   - capabilities;
   - agents and their category;
   - deterministic gates;
   - human decisions, with the reason each one is human;
   - exception paths;
   - controls;
   - evidence.
4. Activities eliminated or changed, as ACT-ids from [`../01-enterprise-outcomes/legacy-activity-classification.csv`](../01-enterprise-outcomes/legacy-activity-classification.csv).
5. Metrics. Targets marked **[T]** are design targets, not measurements, and not industry benchmarks.

## Index

"Activities changed / eliminated or reduced" counts the ACT-ids cited for each workflow (from [`workflows.csv`](workflows.csv)). The first number counts every cited ACT-id, including activities that remain human-accountable but now have a different mechanism. The second number counts only those whose disposition is *eliminate* or *reduce*.

| ID | Workflow | Legacy departments spanned | Outcomes | Trigger events | Human decision points | Activities changed / eliminated or reduced | File |
|---|---|---|---|---|---|---|---|
| WF-01 | Routine cash contribution → routine domestic grant | 6 | O-01, O-02, O-05, O-06, O-09, O-15 | `ContributionSettled`, `RecommendationSubmitted` | None on the routine path | 12 / 7 | [wf-contributions](wf-contributions.md) |
| WF-02 | Appreciated securities contribution | 4 | O-01, O-03–O-05 | `ContributionIntentDeclared`, `ContributionReceived` | Unconfirmed orphan matches | 5 / 1 | [wf-contributions](wf-contributions.md) |
| WF-03 | Complex privately held asset | 5 | O-01, O-03, O-04, O-07, O-08 | `ContributionIntentDeclared` (complex) | Acceptance (specialist or committee); valuation; Form 8283 | 4 / 1 | [wf-contributions](wf-contributions.md) |
| WF-04 | Cryptocurrency contribution | 4 | O-01, O-04, O-07, O-08 | `ContributionIntentDeclared` | Source-of-funds holds; assets not on the accepted list | 2 / 0 | [wf-contributions](wf-contributions.md) |
| WF-05 | High-volume and recurring grants (year-end surge) | 5 | O-06, O-04, O-09, O-15 | `RecommendationSubmitted` | Exceptions only | 5 / 5 | [wf-grants](wf-grants.md) |
| WF-06 | Foreign grant (equivalency determination or expenditure responsibility) | 4 | O-06–O-08 | `EligibilityEvaluated` = refer: foreign | Specialist determination; sanctions officer | 2 / 0 | [wf-grants](wf-grants.md) |
| WF-07 | Grant to a domestic non-charity requiring expenditure responsibility | 4 | O-06, O-07 | `EligibilityEvaluated` = refer: ER | Pre-grant inquiry and approval | 1 / 0 | [wf-grants](wf-grants.md) |
| WF-08 | Fiscal-sponsor grant | 3 | O-06, O-15 | `RecipientResolved` | Flagged restrictions only | 3 / 1 | [wf-grants](wf-grants.md) |
| WF-09 | Recipient eligibility change mid-flight | 4 | O-06–O-09 | `CharityEligibilityChanged`, `SanctionsListUpdated` | Post-payment review; sanctions | 2 / 1 | [wf-grants](wf-grants.md) |
| WF-10 | Payment return and payee bank change | 5 | O-05, O-06, O-08, O-15 | `PaymentReturned`, `PaymentProfileChanged` | High-risk profile changes | 3 / 1 | [wf-grants](wf-grants.md) |
| WF-11 | Donor-side AI agent recommending grants | new capability | O-03, O-06, O-08, O-17 | `PrivilegeGranted`, `RecommendationSubmitted` | Donor confirmation; fraud holds | 0 / 0 | [wf-grants](wf-grants.md) |
| WF-12 | Advisor onboarding and delegated authority | 5 | O-02, O-04, O-09, O-17 | `PartyRegistered`, `PrivilegeGranted` | Firm admission | 4 / 2 | [wf-relationships-servicing](wf-relationships-servicing.md) |
| WF-13 | Donor death and successor activation | 4 | O-16, O-02, O-03, O-09 | `DonorDeceased` | Disputes; document mismatches | 1 / 0 | [wf-relationships-servicing](wf-relationships-servicing.md) |
| WF-14 | Outbound transfer with full history | 4 | O-16, O-06, O-05 | `TransferOutRequested` | Variance-power refusals only | 1 / 0 | [wf-relationships-servicing](wf-relationships-servicing.md) |
| WF-15 | Inactive or dormant account | 4 | O-16, O-13, O-04 | `AccountInactivityThresholdReached` | Charitable default distribution | 1 / 0 | [wf-relationships-servicing](wf-relationships-servicing.md) |
| WF-16 | Documentation request | 3 | O-09, O-12 | `DocumentationRequested` | Requests that fit no template | 2 / 1 | [wf-relationships-servicing](wf-relationships-servicing.md) |
| WF-17 | Liquidity for a grant wave or market disruption | 4 | O-04, O-06, O-10 | Recommendation stream, `PolicyBandBreached` | Actions beyond the pre-approved playbook | 4 / 0 | [wf-investments-treasury](wf-investments-treasury.md) |
| WF-18 | Daily NAV, unitization and fees | 4 | O-04, O-05, O-09, O-14 | `NavStruck`, `FeeAccrued` | Price exceptions; fee schedule | 3 / 0 | [wf-investments-treasury](wf-investments-treasury.md) |
| WF-19 | Continuous reconciliation and break resolution | 4 | O-05, O-08, O-11, O-15 | `PaymentSettled`, `ReconciliationBreakDetected` | Write-offs above threshold | 3 / 1 | [wf-accounting-reporting](wf-accounting-reporting.md) |
| WF-20 | Continuous close, Form 990 and Schedule D | 6 | O-05, O-07, O-10, O-12 | Period-end calendar event | CFO judgments; officer sign-off | 4 / 1 | [wf-accounting-reporting](wf-accounting-reporting.md) |
| WF-21 | State registration and deadlines | 4 | O-07, O-10, O-12 | `RegulatoryDeadlineApproaching` | Officer sign-off and submission | 2 / 0 | [wf-accounting-reporting](wf-accounting-reporting.md) |
| WF-22 | Regulatory or policy change → policy-as-code | 6 | O-07, O-10, O-18 | `ComplianceObligationChanged` | Counsel interpretation; approval | 3 / 1 | [wf-governance-change](wf-governance-change.md) |
| WF-23 | Agent permission change and improvement cycle | new capability | O-08, O-10, O-17, O-18 | `AgentRunCompleted` | Agent owner, evaluation lead and CRCO; Change Board | 0 / 0 | [wf-governance-change](wf-governance-change.md) |
| WF-24 | Board oversight evidence pack | 5 | O-04, O-07, O-10, O-14 | Calendar T-10; threshold events | Board decisions | 4 / 0 | [wf-governance-change](wf-governance-change.md) |

Twenty-two of the workflows span three or more legacy departments. WF-11 and WF-23 have no legacy equivalent: they are capabilities that a conventional sponsor does not have.

Mermaid diagrams (16 in total) appear in WF-01, 02, 03, 05, 06, 09, 10, 11, 12, 13, 17, 19, 20, 22 and 23, and in the [integration journey](enterprise-integration-journey.md).

## Reference journey

[`enterprise-integration-journey.md`](enterprise-integration-journey.md) covers the full path: acquisition → onboarding → contribution → custody → accounting → investment → recommendation → eligibility → authorization → disbursement → reconciliation → reporting. For each stage it gives the authoritative data, events, APIs, agents, exceptions, evidence and the reason any step needs a human. It ends with a full sequence diagram and five data-contract sketches. The executable counterpart is [`../models/Daf.Enterprise/Journey.fs`](../models/Daf.Enterprise/Journey.fs).

## Cross-cutting findings

1. **Human decision points cluster in a few types.** They are complex-asset acceptance, equivalency determinations and expenditure responsibility, benefit cases, sanctions true matches, write-offs, filings, policy and agent changes, and board decisions. None of the 24 workflows needs a human on its routine path for *processing*. Humans appear for *judgment*.
2. **Every workflow's latency target is a design target.** The industry publishes no measured baseline (industry report §4: 5 of 28 turnaround statements are measured). Phase 3 of the roadmap must measure both legacy and redesigned latency before anyone can claim the redesign is faster.
3. **"Routine" is an empirical share, not an assumption.** The repository's review-need proxy (about 7–8.5% of grants at three nationals) measures recipients that may need review, not observed review. The routine share must be measured in pilot operations (GAP: Q-N03).
