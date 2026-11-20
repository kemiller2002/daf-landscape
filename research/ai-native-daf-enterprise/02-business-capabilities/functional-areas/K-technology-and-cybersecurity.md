# K. Technology and cybersecurity

**Capabilities:** C5.6 Security and privacy (primary), C5.5, C6.2, plus the platform underlying every capability · **Outcomes:** O-17, O-11, O-03, O-05 · **Accountable:** CTO (CISO delegate for security) · **Detailed architecture:** [`../../07-technology-architecture/`](../../07-technology-architecture/) · **Component constraints:** DD-009, DD-014, DD-015

## 1. Existing industry operating model

Most sponsors license a recordkeeping and portal platform, or run the parent firm's systems.

**Who supplies the technology**
- **Ren family.** Any confirmed Ren/Stellar link covers a floor of 32.2% of FY2024 DAF assets ($105.6bn, 54 sponsors).
- **Foundant** serves 361 of 803 community foundations (45%, 32.7% of mapped CF DAF assets) and 282 of 351 tail community foundations with an identified vendor.
- **Give Interactive's** first-party-evidenced book is $23.90bn.
- **Affiliated nationals** run on the parent's systems (for example Fidelity on FMR).

Sources: [industry report §1, §3](../../../DAF-INDUSTRY-REPORT-2026-11.md); strategic synthesis §0 G7–G8.

**Assurance is opaque**
- None of 13 vendors publishes a SOC report with period and system scope [V wave 5].
- Ren's own boilerplate states SOC 2 "Type 2" in July 2025 and "Type 1" in April 2026 ([industry report §5](../../../DAF-INDUSTRY-REPORT-2026-11.md); [`soc2-assessment-2026-11-11.md`](../../../soc2-assessment-2026-11-11.md)).
- Audited sponsor statements read (Fidelity, Vanguard FY2026, RCF, NCF, Charityvest) reference no SOC report (report §11.6).

**Security practice**
- Login MFA or a one-time code is published at only 3 sponsors (52.0% of assets) ([`b49-04-fraud-diversion-controls.md`](../../../mission-2026-11-14/b49-04-fraud-diversion-controls.md)).
- State breach registers found no entry naming a charitable or DAF entity. Every notice is filed by a parent or a vendor ([`b39n1-03-b39n2-02-lobbying-and-breaches.md`](../../../mission-2026-11-14/b39n1-03-b39n2-02-lobbying-and-breaches.md)).

**Integration practice**
- Integration is by batch files and portals.
- Public vendor templates allow batch export but not live integration.
- Platform migrations lose history (AEF kept two years) (industry report §4, §8).

**Shared single points of failure:** the RCF–Ren contract, Ren's DFX portal family, Chariot on Column N.A., and the IRS master file (§2.7).

## 2. Actual required business outcomes

- Correct, available, recoverable processing of every outcome's events (O-05, O-06).
- Structural enforcement of exclusive legal control and segregation of duties (O-03, O-08).
- Confidentiality and integrity of donor, recipient and financial data (O-17).
- Exit-ready, portable data with no lock-in to any vendor, including our own (O-11, O-16).
- Observable operations: every outcome's time, cost, error and intervention measured (O-18).

## 3. Legal and risk constraints

- State breach notification and the state comprehensive privacy laws that reach nonprofits (see the [regulatory applicability map](../../08-governance-and-compliance/)).
- PCI DSS if cards are accepted. The design avoids it via a tokenized processor, or by not accepting cards.
- E-SIGN and UETA for electronic records and agreements.
- IRS record retention.
- Contractual SOC expectations of institutional partners.
- §4966 control evidence must be reproducible for examination.
- **Licensing:** 10 of 14 Echelon repositories carry PolyForm Noncommercial 1.0.0. That may cover a charitable sponsor but not a commercial infrastructure provider (Model C), so legal review is required before any use ([component assessment](../../07-technology-architecture/echelon-component-assessment.md)).

## 4. Proposed AI-native operating model

**Application architecture (summary):**
- a **modular monolith** in F# (DD-009, DD-015);
- one transactional PostgreSQL-class managed database per tenant cell, with a transactional outbox, append-only event ledger tables and projections;
- durable workflow state machines persisted in the same database;
- one deployable per cell, with cells replicated for isolation in the multi-sponsor model (DD-016);
- agents run in a separate **agent runtime** process that holds *no* database write credentials. It calls the monolith's APIs through a **tool broker** that enforces per-agent scopes, rate limits and value caps.

Details and alternatives are in [`../../07-technology-architecture/`](../../07-technology-architecture/).

**Identity model**

| Principal | Authentication | Authorization |
|---|---|---|
| Donor / advisor / successor | Passkeys (WebAuthn) primary; step-up for payout-relevant actions | PrivilegeGrants (ReBAC: relationship to account) + ABAC (limits) |
| Institution (machine) | OAuth 2.0 client credentials + mTLS | Per-institution scopes + PrivilegeGrants of represented donors |
| Donor's AI agent (delegated principal) | OAuth with a token bound to an agent identity; donor consent | Scoped PrivilegeGrant with value caps; confirmation rules (DD-017) |
| Staff | SSO + phishing-resistant MFA; JIT privileged elevation | Delegation register (roles + limits) |
| Enterprise agents | Workload identity per agent version | Tool-broker scopes; no authoritative writes |
| Services | Workload identity | Least-privilege service roles |

**Security controls:**
- encryption in transit and at rest, with bank-account and identity data tokenized in a separate vault;
- KMS or HSM-backed keys;
- payment instructions signed by the payment gate's key, which only that module can use;
- dual control on key operations;
- an immutable audit and evidence store (WORM object storage) with hash chaining;
- dependency and supply-chain controls: pinned dependencies, SBOM, signed builds, reproducible builds where feasible;
- secrets in a managed vault, never in code;
- WAF and rate limits at the edge.

**Observability:** structured logs, traces with correlation ID equal to the business journey, metrics per outcome (latency, error, intervention, cost), an agent-run ledger, and SLO dashboards that feed C6.2.

**Incident response:**
- severity matrix with money-movement incidents always Sev-1;
- payments-pause switch; per-agent kill switch;
- runbooks per scenario (see [`../../11-scenarios-and-validation/`](../../11-scenarios-and-validation/));
- breach-notification decision tree with counsel;
- post-incident review feeding C6.4.

**Disaster recovery:** RPO ≤ 5 minutes (managed database point-in-time recovery plus event ledger replication), RTO ≤ 4 hours for core and ≤ 1 business day for non-core [A]. Quarterly restore tests produce evidence (ACT-080). An exit-readiness test periodically exports all data in open formats (including the open grant record) and restores it into a cold standby.

**Vendor integration:**
- one adapter module per counterparty (custodian, bank, rail, identity provider, data providers);
- file-to-event conversion for file-based counterparties;
- contract tests per adapter;
- circuit breakers;
- a second provider pre-integrated for critical rails where feasible (C5.5).

**Echelon components (DD-014):** none in the regulated runtime.
- **Forma:** evaluate-later for UI CSS and HTML.
- **Folio:** evaluate-later for HTML→PDF statement layout, but archival needs PDF/A, which was not found.
- **Limen:** browser state only; it is not a WASM runtime.
- **Aegis:** failure handling only; it is not security.
- **Dokimos, Praxis:** dev tooling.
- The security component Tutela was not inspected. Do not assume it exists or is mature.

## 5. Eliminated activities

- ACT-058: nightly batch exchanges, reduced to adapters only.
- ACT-059: multiple copies of donor data, eliminated.
- ACT-060: spreadsheet access reviews, now automated entitlement analytics.
- Manual DR checklists, replaced by automated restore evidence.
- Annual vendor questionnaires, replaced by telemetry (ACT-064).

## 6. New workflows

- **WF-K1 Payments pause.** A Sev-1 signal or human trigger sets the pause flag. The payment gate refuses releases, queued instructions stay queued, and notices go out. Resumption requires dual human approval.
- **WF-K2 Credential compromise.** Detection (anomaly or report) leads to token revocation (`PrivilegeRevoked` or client disable), a scoped forensic query over the event ledger by principal, a review of affected instructions, and recovery.
- **WF-K3 Agent kill switch.** Triggered by an evaluation regression, an incident or anomalous tool use. The tool broker denies the agent, its work falls back to human queues, and the incident is reviewed.
- **WF-K4 Restore test.** A scheduled restore to an isolated environment, then invariant checks (ledger balances, unit identity), then an evidence record.
- **WF-K5 Exit-readiness export.** A full export in open formats, a schema validation, and a cold-standby import test.
- **WF-K6 Vendor degradation.** `CustodianUnavailable` (or a rail outage) puts the system in degraded mode per runbook (see 11-).

## 7. Required data

Identity and entitlement data; the delegation register; key inventory; asset and software inventory with SBOM; logs, traces and metrics; the agent-run ledger; vendor register with SLAs and SOC report metadata; incident records; restore-test evidence.

## 8. Required APIs

Platform-internal: the tool broker API (agent → capability calls); the admin API for the payments pause and kill switches (dual control); `/v1/evidence`; `/v1/events` (security event export to SIEM); `/v1/privileges` (revocation). External: the identity provider, KMS and vault, SIEM.

## 9. Event triggers

`PrivilegeRevoked`, `AgentPermissionChanged`, `AgentRunCompleted` (anomaly detection), `CustodianUnavailable`, `PaymentProfileChanged` (fraud signal), `SanctionsListUpdated`, `PolicyPublished` (security policy), security telemetry events (failed logins, token misuse), `ExceptionCaseOpened` (Sev classification).

## 10. AI agent responsibilities

- **SOC report analyzer** (Category 2): extracts scope, period, exceptions and complementary user-entity controls from vendor SOC reports, and maps them to our controls. Flag-only; CISO accepts (DEC-061).
- **Security triage assistant** (Category 2): summarizes alerts and correlates by principal. It cannot execute containment except via pre-approved deterministic playbooks triggered by humans.
- **Code review assistant** in the SDLC (Category 2): suggestions only, human review required, and it never deploys.

## 11. Deterministic automation responsibilities

Authorization decisions; token issuance and revocation; payment-gate signing; invariant tests in CI and production (no donor-facing credential can reach payment APIs); backup and restore jobs; dependency scanning; WORM evidence writes; SLO alerting; circuit breakers; rate limits.

## 12. Human oversight requirements

Privileged access approvals (DEC-076); incident declaration (DEC-077); payments-pause release (dual control); acceptance of SOC exceptions (DEC-061); production deployment approvals for changes touching controls (Change Board); annual penetration test scoping and remediation acceptance.

## 13. Exception management

Security cases (`security.incident`, `security.access_anomaly`, `vendor.soc_exception`, `dr.test_failure`) sit in the single queue with Sev-based SLAs. Sev-1 incidents also page on-call and notify the CEO, and the Audit and Risk Committee is notified per policy.

## 14. Security and compliance controls

- **Mapped frameworks:** SOC 2 Trust Services Criteria (target: publish a scoped Type II report, unlike the 13 vendors studied); NIST CSF 2.0 as the organizing taxonomy.
- **Controls catalog:** [`../../08-governance-and-compliance/controls.csv`](../../08-governance-and-compliance/controls.csv).
- **Testing:** an annual external penetration test plus continuous automated testing, and red-team exercises against agents (prompt injection, tool misuse).

## 15. Estimated staffing implications

**Drivers:** platform complexity (fixed), number of counterparty adapters, number of agent families (evaluation load), and tenants (cells).

**Direction:**
- At 1k–10k accounts, *buying* platform capability from an infrastructure provider (Model C) dominates building it.
- A self-built platform needs a fixed core engineering team regardless of account count.

FTE by scale is in [`../../09-financial-models/`](../../09-financial-models/).

## 16. Cost and performance model

| Metric | Target [A] |
|---|---|
| Core availability (grant intake, decisioning, payment gate) | ≥ 99.9% monthly |
| RPO / RTO | ≤ 5 min / ≤ 4 h |
| Restore tests passed | 4 of 4 per year |
| Critical vulnerabilities open > 15 days | 0 |
| Infrastructure cost per account-year | Modeled in 09-; small relative to labor at every scale [A] |

## 17. Implementation dependencies

Managed database and cloud provider selection; identity provider; KMS and vault; custodian, bank and rail adapters; SOC 2 auditor engagement; the evaluation harness for agents (05-); legal review of any Echelon component license before use.

## 18. Measurable success criteria

- Invariant tests prove that no donor- or agent-facing credential can reach the payment instruction capability (continuous).
- A published, scoped SOC 2 Type II report within 18 months of operation.
- Zero Sev-1 incidents without a postmortem.
- An exit-readiness export completes and validates quarterly.
- 100% of production changes traceable to an approved change record.
