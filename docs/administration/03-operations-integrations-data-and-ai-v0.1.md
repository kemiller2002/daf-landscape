# DAF Administration: Operations, Integrations, Data and AI v0.1

Status: proposed contracts. Financial core controls and release gates remain independent.

## Cross-domain administration workflows
OPS-01 Establish fund -> activate book and allowed accounts only after authorized acceptance.
OPS-02 Accept gift -> custody receipt -> asset valuation -> fund allocation -> acknowledgment under approved policy.
OPS-03 Recommend grant -> verify charity -> sponsor approval -> reserve funds -> payment instruction -> provider observation -> settlement -> reconciliation -> reporting.
OPS-04 Investment mandate -> permitted account/custodian -> order authorization -> execution -> position/cash observation -> ledger reconciliation.
OPS-05 Fee assessment -> policy-calculated charge -> review -> ledger journal -> statement.
OPS-06 Successor activation -> verified trigger -> authority revision -> pending-work reassessment -> notices.
OPS-07 Fund merge/split/transfer -> conservation/restriction check -> custody and ledger actions -> closure of old records -> lineage preserved.
OPS-08 Policy change -> impact simulation -> approval -> effective activation -> notifications -> audit.
OPS-09 Charity data update -> provenance ingestion -> identity match -> eligibility recheck -> impact on pending grants.
OPS-10 Payment provider outage -> durable unknown-state handling -> reconciliation -> controlled recovery.

## Integration architecture
INT-01 Provider capability registry: read balances, positions, transactions, trades, cash transfer, statement, corporate action, grant payment, identity, signature, messaging.
INT-02 Capability is independently verified per provider, account, contract, legal entity and environment; never infer Schwab integration access from general market availability.
INT-03 Stable external identity mapping with effective dates, source, confidence and reconciliation.
INT-04 Durable inbox/outbox, request hash/idempotency, retry classification, rate limits, backoff, provider receipt and correlation.
INT-05 Poll/webhook event reconciliation with duplicate, missing, late, out-of-order and contradictory observations.
INT-06 Data freshness policy per source and decision: stale data cannot silently authorize financial action.
INT-07 Credential rotation, secrets management, least privilege, consent, tenant segregation and integration health evidence.
INT-08 Manual fallback must preserve authorization, audit and financial conservation.
INT-09 Contract tests and sandbox fixtures for each adapter; no fake success for unsupported operations.
INT-10 Provider failure cannot erase command status or release reserved resources without confirmed evidence.

## Data model / provenance
DATA-01 Canonical identifiers for Sponsor, LegalEntity, Fund, Party, Relationship, Agreement, Policy, Restriction, Contribution, Asset, Grant, Charity, CustodyAccount, FeeSchedule, Case, Document, AuditEvent.
DATA-02 Separate operational record from financial book; link by immutable identifiers and source events.
DATA-03 Effective time and recorded time for changes in authority, agreement, eligibility, valuation and policy.
DATA-04 Immutable snapshots of evidence and decisions, content hashes and source citations.
DATA-05 Data classification: public charity data, internal operational, confidential donor, sensitive identity, financial account, legal privileged.
DATA-06 Retention, deletion, legal hold, consent and subject rights reviewed per applicable law and entity.
DATA-07 Source-of-truth registry per field; no silent last-write-wins across custody, ledger and operational systems.
DATA-08 Explicit correction events with old/new value, rationale, approval, impact and downstream replay.
DATA-09 Schema/version migrations, historical imports, reconciliation and dual-run comparisons.
DATA-10 Analytics derived from governed events and definitions, not ad hoc cross-tenant joins.

## Migration from incumbent administrator
MIG-01 Source inventory and contract rights to export; legacy fund IDs, balances, grant history, donors, advisors, agreements, restrictions, successors, fees, statements, custody.
MIG-02 Data mapping with canonical ID, provenance, confidence and unresolved conflicts.
MIG-03 Reconcile opening fund balances, liabilities, cash, positions, pooled interests and pending obligations to external statements.
MIG-04 Validate signed agreements and effective authority, not just imported contact roles.
MIG-05 Preserve historical grant and tax acknowledgment records and original document evidence.
MIG-06 Shadow operations and dual-run before cutover; explicit variance tolerance and owner signoff.
MIG-07 Cutover freeze, command sequencing, provider coordination, rollback/forward recovery, donor notices.
MIG-08 Post-cutover sampling, exception queue, audit evidence and historical query continuity.
MIG-09 Do not activate live money movement until external provider contracts and safety gates are verified.

## AI-native administration
AI-01 Identify task, source evidence, policy rule and authority before proposing automation.
AI-02 Replace repetitive intake with extraction + validation + confidence + human exception review.
AI-03 Prepare fund establishment packet from verified documents and structured terms; never declare legally executed agreement from OCR.
AI-04 Compare governing agreements and policy revisions, flag contradictions and required legal review.
AI-05 Detect duplicate charities, mismatched identifiers, changed payment destination, stale evidence and unusual grant patterns.
AI-06 Assemble decision package with evidence links, missing information, deterministic rule results and AI suggestions separated.
AI-07 Draft communications with approved templates and audience permissions; human approval for sensitive/legal content.
AI-08 Recommend next best action based on permitted workflow, dependency, urgency and measurable outcome.
AI-09 Learn from reviewed corrections with privacy and governance controls; do not silently change sponsor policy.
AI-10 Measure automation value by eliminated user steps, time, error, rework, service quality and control failures.
AI-11 Explicit prompt-injection defenses for external charity descriptions, documents, emails and imported data.
AI-12 AI unavailability has a functional non-AI fallback; model hallucination cannot bypass authorization.
AI-13 Record model/version, retrieval snapshot, prompt template version, decision provenance, reviewer and action outcome as appropriate to privacy rules.
AI-14 No automatic grant approval, investment execution, cash movement, fee waiver or authority escalation without independently approved policy and authorization.

## Reliability and operational SLO candidates
SLO-01 Time to first meaningful UI paint measured on representative mobile devices and networks; set target after baseline.
SLO-02 Draft durability and recoverability tested with device restart and network interruption.
SLO-03 Command receipt survives timeout, retries and process crash.
SLO-04 Provider data freshness observable and displayed, with policy-defined safe fallback.
SLO-05 Reconciliation lag, unowned exceptions, failed controls and unresolved unknown payment states monitored.
SLO-06 Accessible incident messaging, customer support escalation and rollback/forward recovery runbooks.
SLO-07 Tenant isolation tested under load, concurrency and compromised user scenarios.

## Risks and challenges
- DAFs are not merely brokerage subaccounts; sponsor control, gift acceptance and advisory privilege are first-class.
- One fund can have many contributors, advisors, agreements and custodial exposures; simple CRUD screens lose legal nuance.
- Sponsor policies are not all identical and may vary by fund product and historical agreement.
- 'Automated' does not mean 'unreviewed'; distinguish deterministic controls, AI preparation and delegated human decisions.
- Historical migration can be more dangerous than greenfield onboarding if authority, restrictions or unsettled obligations are imported incorrectly.
- SOC 2 readiness requires operating controls and evidence, not logging everything indiscriminately.
