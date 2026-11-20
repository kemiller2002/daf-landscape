# Security architecture

**Outcome:** O-17, together with the security aspects of O-03, O-08 and O-11.

**Component note:** the Echelon component *Aegis* is failure handling, not security ([component assessment](../07-technology-architecture/echelon-component-assessment.md)). Security capabilities here come from mature commodity services: the cloud provider's IAM and KMS/HSM, a workforce identity provider, a customer identity platform, a SIEM, and a secrets manager. The design does not depend on any Echelon component for security (DD-014).

## 1. Identity model: every actor is a principal

| Principal type | Authentication | Authorization basis | Notes |
|---|---|---|---|
| Workforce (staff, contractors) | SSO with phishing-resistant MFA (FIDO2) (CTL-033) | Role plus attributes plus delegation register; just-in-time privileged access (CTL-031) | No standing production write access; no human holds payment-signing credentials |
| Donor | Customer identity platform; passkeys or MFA; risk-based step-up for payout-relevant changes | PrivilegeGrants on accounts | Recovery flows are a major attack surface; recovery triggers cooling-off |
| Advisor (individual) | Federated from the advisor's firm (SAML/OIDC) where possible, otherwise customer identity | Donor-consented PrivilegeGrant (view, recommend investment, recommend grant) | Firm-level offboarding revokes access |
| Institution or partner system | OAuth 2.0 client credentials with mTLS or private-key JWT; short-lived tokens (CTL-034) | Partner scope per program; per-endpoint scopes | Separate credentials per environment and per program |
| **Donor-side AI agent** (third-party or the enterprise's own donor assistant) | OAuth on behalf of the donor (delegated grant); agent identity asserted | PrivilegeGrant with `agent` flag: value caps, recipient allow-lists, confirmation rules, expiry (DD-017) | The agent can *request*. Requests above caps require out-of-band donor confirmation |
| **Enterprise AI agents** (internal) | Workload identity | Tool broker with an explicit tool allow-list per agent version; read scopes; *no* write to authoritative records (CTL-008) | Each run is an AgentRun record |
| Services (modules) | Workload identity | Least privilege per module; only the payment gate can call KMS sign (CTL-032) | Modular monolith: modules separate at the code and database-schema level |

## 2. Zero-trust posture

- Every request is authenticated and authorized at the point of use, whatever the network location.
- Data-layer authorization: a module can read only its own schema and published read models.
- No shared administrative accounts. Break-glass accounts are sealed, alarmed and reviewed.

## 3. Secrets and keys

| Asset | Protection |
|---|---|
| Payment-instruction signing / bank API credentials | HSM-backed KMS. Callable only by the payment-gate workload identity. Dual-person approval for key administration. Alarms on any other caller |
| Custodian API credentials | KMS; withdrawal whitelists set at the custodian. Changing a whitelist requires bank-side dual control |
| Data encryption keys | Envelope encryption per tenant (sponsor) and per data class (identity vault separate) |
| Partner OAuth secrets | Secrets manager, rotated; prefer asymmetric client auth |
| Agent / model API keys | Secrets manager; per-agent keys for attribution and blast-radius limits |

## 4. Data protection and minimization

- **Identity vault.** Government ID numbers, dates of birth and document images live in a separate encrypted store. Operational modules hold Party IDs only.
- **Bank account numbers** are stored as provider tokens, never raw in operational stores.
- **Analytics** use pseudonymous keys. Donor anonymity choices are enforced at the remittance projection (CTL-043).
- **Model inputs** carry the minimum necessary. No identity-vault data is sent to external model APIs. Vendor terms must prohibit training on enterprise data. Data-processing terms are part of vendor onboarding.
- **Retention** follows the schedule in [continuous compliance](continuous-compliance-and-evidence.md) §1.

## 5. Logging and observability

- Structured logs, metrics and traces with the correlation ID from the event envelope, so one business journey can be traced across modules and agents.
- Security events go to a SIEM, with detections for: anomalous partner traffic, step-up failures, payee changes, KMS access, privileged sessions, and agent tool-call anomalies.
- Logs are immutable. Privileged access to logs is itself logged.

## 6. Incident response

| Stage | Owner | Notes |
|---|---|---|
| Detect | SOC (managed at small scale) plus automated detections | Severity by impact on money, data or legal state |
| Declare | CISO (H) | Runbooks per incident class; kill switches available (CTL-028) |
| Contain | Incident commander | Revoke tokens, pause payments, disable an agent, isolate a module |
| Notify | GC (H) | State breach notification analysis; partners per contract; board for severity 1 |
| Recover and learn | CTO, COO | Post-incident review → controlled change |

## 7. Disaster recovery and continuity

These targets are assumptions **[A]**, to be validated in Phase 5 restore tests (CTL-036):

| Tier | Scope | RPO | RTO |
|---|---|---|---|
| T0 | Event ledger, payment gate, authorization | ≤5 min | ≤4 h |
| T1 | Grant decisioning, contributions intake, read models | ≤15 min | ≤8 h (read models can be rebuilt from the ledger) |
| T2 | Agents, discovery, analytics | ≤24 h | ≤72 h (operations degrade to D-path plus human queue) |

- **Degraded modes.** Without agents, the D path continues; P-dependent items queue for humans. Without the custodian, trading is suspended and grants are paid from the cash buffer within limits. Without a rail, the secondary rail is used or payments are queued with status shown to donors. Scenarios exercise each.
- **Exit readiness** (CTL-035): a quarterly full export and restore into a cold standby in open formats.

## 8. Threat model (STRIDE-style)

| Threat | STRIDE | Vector | Primary controls | Residual |
|---|---|---|---|---|
| Donor account takeover → grant to an attacker-controlled "charity" | S, E | Credential stuffing, SIM swap, recovery abuse | CTL-033 step-up; recipient must be an eligible registered org (CTL-011); payee verification (CTL-004); new-recipient velocity caps (CTL-029) | Attacker-controlled *real* charity; mitigated by anomaly scoring and caps |
| Payee bank-account hijack (BEC posing as a nonprofit) | S, T | Email to the sponsor or the nonprofit; forged bank letter | CTL-004 cooling-off plus out-of-band verification via previously verified contact; account-ownership verification service | Compromise of the nonprofit's own systems |
| API credential compromise (partner) | S, I, E | Leaked client secret | CTL-034 short-lived tokens, mTLS, anomaly detection; partner can only *request*; requests are still gated | Data exposure within the partner's scope until revocation |
| Insider: create payee and pay | E, T | Staff with broad rights | SoD-1 (CTL-006); dual control (CTL-005); no standing payment credentials (CTL-031/032) | Collusion of two; mitigated by sampling and internal audit |
| Insider: loosen a threshold quietly | T | Config edit | CTL-010 monotonic rule; CTL-009; SoD-5 | Collusion |
| **Prompt injection** via charity website text, documents or emails into an agent | T, E | Malicious text instructs the agent to clear a flag or recommend a payee | CTL-008: agent cannot clear flags or write state; tool allow-lists; untrusted content tagged and quoted; output schema validation; red-team evaluation sets (CTL-026) | Agent fails to raise a flag it should (false negative). Deterministic gates still apply |
| Data poisoning of the recipient registry | T | Fake records from a third-party data provider | IRS data is authoritative for eligibility; third-party data is advisory only; provenance and diffs | Misleading discovery content |
| Vendor compromise (data provider, rail, model provider) | multiple | Supply chain | Vendor risk program; least data shared; exit readiness; rail settlement reconciliation (CTL-015) | Rail-level fraud is borne by contract allocation |
| Denial of service at year-end peak | D | Volumetric or application-level | CDN/WAF; rate limits per partner; queue-based intake | Degraded latency |
| Repudiation of a recommendation by a donor | R | "I didn't ask for that" | Signed request events with auth context; confirmation receipts | Disputes go to service recovery |
| Information disclosure of anonymous donors | I | Remittance or report leakage | Anonymity enforced at projection; tests; access logging | Inference from timing and amount |

## 9. AI-specific security

1. Agents run with *read* tools and *propose / flag* outputs only (CTL-008). Any write is a separate deterministic command, authorized independently.
2. Untrusted content (web pages, PDFs, emails) is processed in isolated agent contexts with no tool access beyond extraction.
3. Model and provider changes are agent version changes and go through CTL-026.
4. Per-agent cost and rate ceilings prevent runaway spend.
5. Evaluation sets include adversarial cases: injection, social engineering and jailbreaks. Results are reported to the board (governance §6).
