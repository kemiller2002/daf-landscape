# Automated Charity Assurance: 180-Day Vetting and Low-Friction Grants
Date: 2026-11-22
Status: PROPOSED, sponsor counsel/compliance validation required
Principle: eliminate routine human touches, not accountability. 180 days is a sponsor-proposed maximum comprehensive review interval, not a universal legal safe harbor.

## Decision and challenge log
1. **180-day comprehensive revalidation.** Schedule each charity for a full evidence and policy review no later than 180 days after last successful full validation, with proactive refresh before expiry and jitter/load control. **Why:** reusable assurance across grants; removes repeat casework. **Challenge:** passage of 180 days says nothing about interim loss of status. **Mitigation:** event-driven continuous monitoring plus transaction-time critical checks; immediately invalidate impacted claims on material adverse signals. **Reconsider:** if sponsor policy, jurisdiction, grant class or evidence source requires shorter periods.
2. **Reusable verified charity registry.** Store canonical entity identity, aliases/EIN, source-specific claims, effective/observed times, provenance, review policy version, evidence freshness, and scoped eligibility decisions. **Why:** amortize vetting costs. **Challenge:** same charity may be eligible for one sponsor/grant purpose but not another. **Mitigation:** global factual evidence shared; sponsor/purpose-specific policy decisions never shared as universal eligibility.
3. **Automatic straight-through clearance.** When current high-confidence evidence satisfies deterministic approved rules, automatically renew assurance and permit grant workflow progression with no manual approval of the vetting result. **Challenge:** incorrect source or false entity match. **Mitigation:** corroboration, identity thresholds, source hierarchy, uncertainty states, independent policy engine, sampling and control monitoring. Grant approval authority remains sponsor-governed.
4. **Continuous monitoring.** Monitor authoritative tax-status/filing sources where available, sanctions, legal-entity changes, payment destination risk and other material adverse events at source-appropriate cadence. **Challenge:** 'continuous' does not mean real-time or comprehensive; feeds can be delayed. **Mitigation:** publish last-checked and coverage metadata, fail safely for critical unavailable checks, and do not claim certainty.
5. **Exceptions only.** Route missing, contradictory, stale, suspicious, foreign/nonstandard or policy-ambiguous cases to bounded automated evidence-gathering first, then human specialist if still unresolved. **Challenge:** queue may become overloaded. **Mitigation:** reason-coded triage, priority by grant impact, source repair, bulk remediation, exception analytics and measured false positives.
6. **Recurring and future grants.** Reuse charity assurance at each occurrence but perform lightweight transaction-time critical revalidation, funding, authority, purpose, and destination checks. **Challenge:** automatic blocking for transient data outages frustrates donors. **Mitigation:** distinguish authoritative adverse signal from unavailable data; configurable bounded retry and documented sponsor risk policy; never silently assume eligible.
7. **Identity and disbursement separation.** Charity identity/eligibility approval does not prove bank details or mailing instructions. Independently verify destination changes and prevent forged payment redirection. **Challenge:** repeated verification adds friction. **Mitigation:** reuse previously verified destinations and trigger enhanced controls only on changes or risk.
8. **Automation and AI boundary.** AI can extract, compare, investigate and summarize evidence with citations; deterministic sponsor policy decides routine cases; no autonomous override of contradictory authoritative evidence. **Challenge:** deterministic rules may be inflexible. **Mitigation:** versioned rules and measured exceptions, with human-reviewed policy updates rather than ad hoc approvals.
9. **Expiry and failure semantics.** States: NotAssessed, Pending, Verified, VerifiedWithConditions, NeedsEvidence, Suspended, Ineligible, Expired. Separate factual verification, sponsor eligibility, grant authorization, and payment settlement. **Challenge:** too many visible states. **Mitigation:** simple donor labels and specific next-best action.
10. **Efficiency metrics.** Measure straight-through processing rate, median grant latency, manual touches per 1,000 grants, evidence reuse, renewal success, false-clearance/false-hold rates, cost per grant, time-to-detect adverse changes, and source outage impact. **Challenge:** optimizing only manual touches can degrade safety. **Mitigation:** guardrail metrics and independent sampling.

## Proposed requirements
CA-180-01 configurable maximum 180-day full validation interval per sponsor and charity class.
CA-180-02 refresh proactively before expiration; deterministic scheduling, retries, alerting.
CA-180-03 canonical charity identity and deduplication with provenance.
CA-180-04 typed source claims, timestamps, authority, uncertainty and retention.
CA-180-05 continuous material-change monitoring with source-coverage disclosure.
CA-180-06 automatic renewal with sponsor-versioned deterministic policy.
CA-180-07 transaction-time lightweight checks and risk-triggered deeper checks.
CA-180-08 no mandatory human signoff for fully passing automated vetting where sponsor authority permits.
CA-180-09 automated evidence gathering before human escalation.
CA-180-10 sponsor/purpose-specific eligibility distinct from shared factual verification.
CA-180-11 payment destination independently verified and changes risk-gated.
CA-180-12 adverse events invalidate affected assurance and pause impacted unfulfilled grants.
CA-180-13 source outage handling: distinguish unknown from ineligible, bounded retry, approved fail-safe policy.
CA-180-14 audit of sources, decisions, policy versions, overrides and effective time.
CA-180-15 dashboard and API/widget presentation of last validated, next due, conditions and blocker.
CA-180-16 metrics, independent sampling, exception review, false-negative investigation.
CA-180-17 sponsor-configurable shorter cadence and additional diligence for nonstandard/international grants.
CA-180-18 idempotent renewal and concurrency-safe grant execution.

## Test scenarios
- At day 179 verified charity renews automatically with current clean evidence; no operator touch.
- On day 30 material adverse authoritative status update invalidates affected decision immediately despite 150 days remaining.
- On day 180 source unavailable: distinguish Unknown/Stale from Ineligible; retry and apply sponsor fail-safe rules.
- Identical EIN/alias collision: no false entity merge.
- Charity verified for sponsor A but prohibited grant purpose for sponsor B: sponsor B blocked.
- Recurring grant due after eligibility loss: occurrence held, donor notified, no payment.
- Verified charity changes banking details: separate payment destination verification.
- Duplicate webhook or concurrent renewal: one effective assurance decision, complete audit trail.
- False positive event cleared: restore only after recorded evidence and policy re-evaluation.
- No human action in fully passing routine renewal; sample for independent assurance without blocking.

## Dependencies and unresolved validation
Sponsor counsel and compliance must approve source hierarchy, domestic/international policy, 180-day interval, monitoring thresholds, decision delegation, evidence retention, and grant-purpose rules. Treasury must approve payment destination controls. Operational pilots must measure error rates and throughput before broad straight-through deployment. Do not treat the 180-day interval as a statutory rule or guaranteed safety period.

## Architectural crosslinks
Existing DAF UI O04/O05/O06/O07, D03/D06/D07/D14, grant scheduling decision record, policy engine, typed requirements registry, finance controls and audit events. This file is a proposed decision record and must be transcribed to authoritative registry after validation.
