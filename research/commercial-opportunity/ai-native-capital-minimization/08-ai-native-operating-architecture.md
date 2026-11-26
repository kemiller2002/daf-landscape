# 08: AI-native operating architecture

**Pass:** OPS (part 6). **Data:** [`ai-capabilities.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/ai-capabilities.csv) (16 capabilities).

**Integrator conclusions**
- The architecture is a **single operational model of cases, events, controls and evidence**, not departments re-implemented as agents.
- All 16 AI capabilities are capped at *recommend* and *prepare*. Every money movement, sponsor reserved decision and OFAC disposition stays with an authorised human or a deterministic rule the sponsor has adopted.
- **AI must not invent financial records, bypass sponsor authority or weaken controls.** Each capability has authority limits, evidence requirements, escalation criteria and a fail-closed behaviour.
- **This is a proposal. No runtime exists:**
  - Echelon is engineering tooling.
  - Unbound is requirements only.
  - Nothing in this report is demonstrated operation.
- Requirements candidates RC-AN-004 (case ownership), RC-AN-013 (bounded AI authority) and RC-AN-016 (transfer-not-saving reporting) carry the architecture into Unbound governance (report 17).

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Part 6: AI-native operating architecture and AI capabilities

**Architecture: one operational model, not departments as agents.**

| Primitive | What it holds |
|---|---|
| Event | Immutable fact from a feed, user or rule |
| Case | Typed profile (CNV-SVC-001) with clock, assignment and deadline |
| Control | Rule or required human step with justification, owner and expiry (CNV-GOV-006) |
| Evidence | IPE-supported, hashed, retained (CNV-GOV-001, CNV-PLT-009) |
| Authority | One matrix: command class x actor type x level (CNV-GOV-010), so every command declares its authority |
| Policy version | Sponsor-adopted, effective-dated (CNV-GOV-005) |

Humans and agents act on cases under the authority matrix. 'Departments' become role sets over one queue. That removes handoffs and status reporting, but not segregation of duties, which the engine enforces.

**16 AI capabilities** are specified (monitoring, exception detection, prioritisation, case assignment, customer service, control evidence, compliance monitoring, reporting, onboarding, policy configuration, learning, recurring-problem detection, dossiers, document extraction, fraud triage, reconciliation suggestions). **All are capped at recommend/prepare (A1)**, apart from reversible internal assignment (A2).

**Invariants:**
- AI never creates or alters financial figures;
- AI never clears flags or holds;
- AI never exercises or routes around reserved sponsor authority;
- AI cannot select samples to attest its own work;
- AI unavailability leaves deterministic paths running (CNV-AIO-001).

**Status: proposed.** No case, event, control or evidence runtime exists. The Echelon components are engineering tooling (repository OS, code quality, security discipline, UI, auth). The DAF application is 'planned' and monitoring is 'absent' (echelon-capabilities.csv). The architecture is a requirement set (Unbound), not a demonstrated system, and shared Echelon effort must be charged at loaded cost.
