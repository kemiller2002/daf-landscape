# L. Governance and executive management

**Capabilities:** C5.4 Governance and delegations (primary), C5.1, C4.5, C6.2, C6.3, C6.4 · **Outcomes:** O-10, O-07, O-12, O-18 · **Accountable:** Board (strategy, oversight), CEO (management) · **Companion:** [governance architecture](../../08-governance-and-compliance/governance-architecture.md), which is authoritative for board structure and the delegation design; this file covers the functional-area redesign.

## 1. Existing industry operating model

Sponsors are §501(c)(3) public charities with volunteer or compensated boards, typically with investment and audit committees. Management reports to the board in quarterly packs assembled by staff.

What the repository shows:
- **Governance quality is mostly boilerplate at the top.** The conflict-of-interest policy is affirmed by 50 of 50 top-50 sponsors, against 49 of 57 (86.0%) in the < $10m band. All 8 sponsors answering "No" are under $10m ([`b49-05-sponsor-governance-quality.md`](../../../mission-2026-11-14/b49-05-sponsor-governance-quality.md)). Two of 150 sponsors report excess-benefit transactions: NPT (TY2022–2024) and Servant Foundation (TY2022, with $6,494 of §4958(c)(2) tax).
- **Vendor-related directors exist.** Charityvest's president and director is paid by its technology vendor Foundation Source ($163,944 via Vennfi, 2024) ([industry report §2.3](../../../DAF-INDUSTRY-REPORT-2026-11.md); [`sponsor-governance-and-fee-transparency-2026-11-11.md`](../../../sponsor-governance-and-fee-transparency-2026-11-11.md)).
- **Related-party administration is normal and audited:**
  - RCF → Ren $19.23m in FY2024;
  - Vanguard Charitable's related-party service fee of $4.24m in FY2026;
  - Fidelity Charitable pays FMR affiliates amounts equal to donors' admin fees (§2.1–2.2; [`rcf-ren-governance-related-party-controls-institutional-comparison-2026-11-12.md`](../../../rcf-ren-governance-related-party-controls-institutional-comparison-2026-11-12.md)).
- **Discretionary board-level policy decisions are consequential.** The 2026 SPLC grant holds at three national sponsors drew a 16-attorney-general letter ([industry report §4](../../../DAF-INDUSTRY-REPORT-2026-11.md)).
- **Litigation reinforces board discretion over investments and fees within disclosed terms.** *Pinkert* and *Fairbairn* failed; *Peterson v. WaterStone* is pending ([`b50-01-daf-litigation.md`](../../../mission-2026-11-14/b50-01-daf-litigation.md)).
- **Audited statements read** (Fidelity, Vanguard, RCF, NCF, Charityvest) have unmodified opinions and none references a SOC report (report §11.6).

[I] Board information is periodic and management-curated. No sponsor publishes evidence of continuous control monitoring.

## 2. Actual required business outcomes

- The board makes and records the decisions only it can make: strategy, risk appetite, policy, delegations, auditor, CEO oversight and compensation, conflicted transactions (O-10).
- The board can verify, not merely be told, that delegated authority is used within limits and that controls operate (O-07, O-10).
- Executives manage by current evidence, not by assembled reports (O-12, O-18).
- Policy parameters that change behavior (thresholds, model cut-offs, caps) are governed objects with an approval trail (O-10).

## 3. Legal and risk constraints

- **Duties:** state nonprofit law duties of care, loyalty and obedience.
- **Form 990 disclosures:** Part VI governance (independence, COI policy, whistleblower and document-retention policies, 990 review), Schedule L transactions with interested persons, Schedule R related organizations.
- **§4958** excess benefit, with the rebuttable-presumption procedure for compensation.
- **State AG oversight.**
- **Independent audit thresholds** (state-specific; see the [regulatory map](../../08-governance-and-compliance/)).
- **§4966 and §4967:** fund managers with knowing participation face personal excise tax, so board and officer understanding of the policies is itself a control.
- **Risk:** directors overseeing AI-mediated operations they cannot inspect; concentration of authority in whoever controls policy parameters or agent permissions.

## 4. Proposed AI-native operating model

1. **The machine-enforced delegation register.** Every authority (approve a non-routine grant up to $X, release a payment hold, clear a sanctions true match, accept a complex asset up to $Y, publish a policy, change agent permissions) is a record. It says who holds the authority, its limits, its effective dates and the approving board resolution. The authorization service *enforces* it, so a person cannot exercise an authority the register does not grant. The board approves the register; it does not just describe it.
2. **Policy parameters are governed objects.** A threshold change is a `PolicyPublished` event with:
   - a back-test report;
   - an independent test (the evaluation lead or policy engineer who did not author it);
   - an approval recorded at the authority level the register requires.

   Material parameters (grant auto-approval ceilings, sanctions fuzzy-match thresholds, agent value caps) need committee approval. This closes the risk of AI "setting policy through thresholds no one approved" (O-10 failure mode).
3. **Continuous evidence for executives and the board.**
   - The evidence ledger (C4.5) and telemetry (C6.2) feed live dashboards: control health, exception aging, delegation usage, flags raised and cleared and by whom, agent scorecards, reconciliation status, concentration metrics and the regulatory calendar.
   - Board packs become **approved snapshots** of those dashboards, with drill-down to evidence, plus the **board evidence pack narrator's** draft commentary, which the CEO and CFO review and sign.
   - Internal audit tests the dashboards' lineage (ACT-061 transformed).
4. **Three lines adapted to AI:**
   - first line: capability owners plus agent owners;
   - second line: the CRCO, including model risk via the evaluation lead's dotted line;
   - third line: independent internal audit with read access to the evidence ledger and agent-run ledger, reporting to the Audit and Risk Committee (see [governance architecture §4](../../08-governance-and-compliance/governance-architecture.md)).
5. **Strategic planning with the digital twin.** Strategic options (enter Model C, double complex-asset intake, add an institution) are simulated before decision. Every twin output labels simulated versus measured inputs (addendum §23).
6. **Conflict management by graph.** The related-party detector continuously compares the relationship graph (directors, officers, staff, vendors, recipients) with transactions. Hits are flags for the governance committee chair. Conflicted directors are recused automatically from approval flows on matching subjects.

## 5. Eliminated activities

- ACT-061: quarterly board packs assembled by hand, transformed.
- ACT-046: periodic compliance attestations by staff survey, eliminated.
- ACT-073: annual-only risk workshop, transformed to continuous telemetry plus an annual review.
- Manual minute-to-policy reconciliation: policy versions link to resolutions automatically.

## 6. New workflows

- **WF-L1 Delegation change.** A proposal (CEO) goes to the Governance Committee review, then a board resolution, then a delegation register update (`PolicyPublished`, delegation type), then authorization enforcement, then an evidence record.
- **WF-L2 Material policy parameter change.** A hypothesis from C6.4 is simulated in the twin, back-tested, independently tested, approved by the committee, published (`PolicyPublished`), and then its effect is verified with post-change telemetry, which is reported to the committee.
- **WF-L3 Board evidence pack.** Dashboards are snapshotted, the narrator agent drafts commentary with citations to evidence IDs, the CEO and CFO review and sign, the board receives the pack, and questions are logged with responses linked to evidence.
- **WF-L4 Discretionary policy hold.** For example a recipient under indictment: CEO and GC propose, the board or delegated committee decides (DEC-044), the policy is published, affected grants are held with donor notices, and a review date is set. These are reputational decisions, made by people and recorded, never left to an implicit agent behavior.
- **WF-L5 Conflict recusal.** A related-party flag on a subject leads to automatic recusal of the conflicted approver from that approval flow, an alternate approver, and a log entry for Schedule L analysis.

## 7. Required data

Delegation register; policy registry with approvals; board and committee resolutions (documents with hashes); relationship graph including directors and vendors; control evidence; telemetry; twin scenarios; Schedule L and R relevant transactions.

## 8. Required APIs

`/v1/policies` (delegation and parameter objects), `/v1/decisions`, `/v1/evidence`, `/v1/reports` (board packs, dashboards), `/v1/cases` (governance flags), `/v1/documents` (resolutions, minutes), `/v1/parties` (directors, officers), `/v1/events`.

## 9. Event triggers

`PolicyPublished`, `ComplianceObligationChanged`, `AgentPermissionChanged`, `ExceptionCaseOpened` (governance types), `RegulatoryDeadlineApproaching` (990 review by the board before filing), `CustodianUnavailable` and Sev-1 incidents (board notice per policy), `RelationshipDeclared` / `RelationshipInferred` involving insiders.

## 10. AI agent responsibilities

- **Board evidence pack narrator** (Category 2): drafts commentary strictly from evidence IDs and states what is *not* known. Signed by executives. It cannot alter dashboard data.
- **Related-party detector** (Category 2): flag-only.
- **Regulatory change monitor** (Category 2): drafts impact notes for GC on monitored sources (Federal Register, IRS guidance plan, state AG releases).
- **Improvement agent** (Category 2): proposes changes; cannot approve them.

## 11. Deterministic automation responsibilities

Delegation enforcement; recusal routing; the governance calendar (meetings, 990 board review, COI annual disclosure, auditor rotation reminders); dashboard computation with lineage; snapshot hashing; vote and approval recording.

## 12. Human oversight requirements

All board and committee decisions (DEC-057, DEC-058, DEC-044, DEC-066, DEC-021); CEO evaluation and compensation under the §4958 process; auditor appointment; approval of the risk appetite statement; annual review of agent categories and prohibited actions (Category 5 list).

## 13. Exception management

Governance case types: `governance.conflict`, `governance.delegation_breach_attempt` (blocked attempts are informational, repeated ones escalate), `governance.policy_parameter_drift` (a deployed parameter differs from its approved value, which is critical), `governance.whistleblower` (routed to the Audit Committee chair outside management).

## 14. Security and compliance controls

- Board portal with phishing-resistant MFA.
- Resolutions hashed and stored WORM.
- Separation: no single person can both propose and approve a delegation or a material policy.
- Whistleblower channel independent of management.
- Annual board self-assessment.
- External review of the governance model every three years [A].

## 15. Estimated staffing implications

**Drivers:** fixed (board, CEO, corporate secretary function) plus the cost of governance cadence.

**Direction:** effort shifts from assembling reports to interpreting evidence. The corporate secretary function can be fractional at small scale. FTE in [`../../09-financial-models/`](../../09-financial-models/).

## 16. Cost and performance model

| Metric | Target [A] |
|---|---|
| Board pack preparation effort | ≤ 1 staff-day per meeting (vs multi-week assembly [I]) |
| Material parameters live in production without approval record | 0 |
| Board questions answered with evidence links | 100% |
| Delegation register review | Annual, plus on every role change |

## 17. Implementation dependencies

Evidence ledger (C4.5); telemetry (C6.2); policy registry (C5.1); authorization enforcement of the register; the relationship graph (C1.1); the twin (C6.3); counsel-approved governance documents.

## 18. Measurable success criteria

- Internal audit confirms lineage from dashboard to evidence for 100% of sampled board metrics.
- Zero authority exercises outside the register (enforced and audited).
- Zero parameter-drift findings.
- Conflict recusal applied in 100% of flagged approvals.
- 990 Part VI answers are generated from register and evidence data rather than asserted.
