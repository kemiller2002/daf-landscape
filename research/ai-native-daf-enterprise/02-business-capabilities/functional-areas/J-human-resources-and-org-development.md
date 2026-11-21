# J. Human resources and organizational development

**Capabilities:** cross-cutting; enables every capability's accountable and responsible roles · **Outcomes:** O-10, O-14, O-18, O-17 · **Accountable:** CEO, with board Governance Committee oversight · **Companion:** [organization model](../organization-model.md)

## 1. Existing industry operating model

The repository holds no published DAF sponsor organization charts or functional headcounts (stated in the [organization model §6](../organization-model.md)). The evidence that does exist is cost-based.

**Staff cost as a share of DAF assets**
- Pooled staff cost (Part IX lines 5–10, whole organization) is 78.7 bps of DAF assets at community foundations, against 5.6–15.0 bps at the four self-staffed nationals and 2.9 bps at affiliated-commercial sponsors.
- At affiliated-commercial sponsors the staff sit at the parent firm: Schedule O cites an FMR services agreement, MS/Eaton Vance employees and Schwab employees; at BofA a bank trustee is paid ([strategic synthesis §0 G6](../../../mission-2026-11-14/strategic-synthesis.md); [`direction-sponsor-executive-compensation.md`](../../../mission-2026-11-14/direction-sponsor-executive-compensation.md); industry report §11.25).
- 10 of 12 affiliated-commercial sponsors carry no paid executive on their own 990.

**Executive pay**
- Top-officer pay per $bn of DAF assets is NPT $14k, DAFgiving360 $20k and Vanguard $23k, against a community-foundation median of $734k.
- Median community-foundation top pay is $725k and barely scales with size (elasticity 0.23).

**AI capability and hiring**
- AI work sits at vendors. AI appears in 29.1% of vendor job postings (44 of 151) and 13.3% of sponsor postings (2 of 15, a small sample) (strategic synthesis §0 B; [`direction-news-hiring-signals.md`](../../../mission-2026-11-14/direction-news-hiring-signals.md)).

**Inferred conventional structure [I]**
- Large tier-1 operations and service teams performing D decisions by hand, with a thin specialist layer.

## 2. Actual required business outcomes

- Every capability has a competent accountable person and adequate responsible staff (O-10).
- Segregation of duties is staffed: at least two independent people for every SoD pair (O-05, O-08).
- People are trained for judgment domains and for supervising automated systems, not for manual procedures (O-18).
- The organization can absorb surges (year-end contributions, market events) without lowering control quality.
- Key-person risk is managed: there is no single human holder of a critical authority without a deputy.

## 3. Legal and risk constraints

| Constraint | Implication |
|---|---|
| Fiduciary duties of directors and officers; "knowing" manager liability under §4966(a)(2) and §4967(a)(2) | The people who approve non-routine grants and policies must be trained on the law. Training records are evidence |
| Segregation of duties (control objective, not statute) | Minimum headcount floor (around 8–10 people, see the [organization model §4](../organization-model.md)) |
| Employment law, background checks for staff with access to funds and PII | Pre-hire screening (FCRA-compliant) for privileged roles |
| Compensation reasonableness for disqualified persons (officers, directors) | §4958 rebuttable-presumption process: comparability data and independent approval |
| Automated decisions about employees (hiring tools) | State and local AI-in-employment rules (for example NYC LL144 for hiring tools if used in NYC). Avoid automated hiring decisions; human decisions only |

## 4. Proposed AI-native operating model

1. **Roles are defined by authority and judgment domain, not by task queue.** Each role description lists the delegated authorities it holds (from the delegation register), the decision types (DEC-ids) it decides, the agents it supervises, and the evidence it is accountable for.
2. **New roles.**
   - **Agent owner.** One per agent family. Accountable for the agent's evaluation results, permissions, incidents and cost. Not an engineer necessarily: the owner of the service answer agent is the Head of Client and Partner Operations.
   - **Evaluation lead** (CTO org, dotted line to CRCO). Owns evaluation datasets, regression gates and model-risk sign-off for every agent change.
   - **Policy engineer** (GC-adjacent). Translates counsel's policy into decision tables, maintains back-tests, and cannot deploy their own changes.
   - **Telemetry and twin analyst** (COO). Operates C6.2 and C6.3.
3. **Generalist specialists.** Exception queues route by skill tags (grants-ER, foreign, sanctions, complex-asset, service-recovery, payments). Staff hold several tags, so small teams cover the queue without departmental silos.
4. **Supervision is measured.** Each human reviewer's decisions are themselves sampled (four-eyes QA on a percentage of H decisions), and agent-versus-human disagreement analysis feeds both training and policy.
5. **Fractional and outsourced roles at small scale:** outsourced CIO, fractional CISO, outside counsel, outsourced internal audit, complex-asset processing vendor. In-house accountability for selection and oversight remains.
6. **Surge model.** Year-end complex-asset surges are absorbed by pre-contracted specialist vendors. D-path volume needs no surge staffing (ACT-015).

## 5. Eliminated activities

- ACT-071: large tier-1 service and operations teams, reduced.
- ACT-072: training on many manual procedures, reduced.
- Staffing rosters for batch processing windows, eliminated with batching itself (ACT-028).
- Manual competency attestations, replaced by evidence from QA sampling.

## 6. New workflows

- **WF-J1 Authority provisioning.** A role assignment (H, CEO or delegate) records the authorities in the delegation register (`PolicyPublished`, type delegation). The authorization model enforces them, and they become effective only after required training evidence exists.
- **WF-J2 Reviewer calibration.** A weekly sample of H decisions per reviewer is blind-re-reviewed. Disagreements are adjudicated, and the results feed the training plan and policy clarifications.
- **WF-J3 Agent owner review.** A monthly agent scorecard (accuracy, escalation rate, cost, incidents). The owner attests; a regression creates a C6.4 change case.
- **WF-J4 Key-person coverage.** Each critical authority (sanctions true-match clearance, payment release above limit, filing signature) must have at least two active holders. The coverage check is a deterministic daily test, and a breach is a case to the CEO.
- **WF-J5 Surge activation.** The twin forecasts complex-asset intake above capacity, which triggers the vendor surge contract (H approval).

## 7. Required data

Delegation register (authority × person × limits × effective dates); training records with evidence; reviewer QA results; agent scorecards; skill tags; capacity models from the twin; compensation comparability data for §4958.

## 8. Required APIs

`/v1/parties` (staff as parties), `/v1/policies` (delegation register as a policy type), `/v1/cases` (routing by skill), `/v1/decisions` (sampling for QA), `/v1/reports` (scorecards), `/v1/evidence` (training evidence).

## 9. Event triggers

`ExceptionCaseOpened` (capacity telemetry), `ExceptionCaseResolved` (QA sampling), `AgentRunCompleted` (scorecards), `PolicyPublished` (delegation changes), `AgentPermissionChanged` (agent owner sign-off), `RegulatoryDeadlineApproaching` (training renewals).

## 10. AI agent responsibilities

- Training content drafting from policy changes (Category 2): GC and policy owner approve.
- Capacity forecasting narrative from twin output (Category 2).
- QA sampler for reviewer decisions (Category 2, flag-only).
- **No AI in hiring, promotion, compensation or performance decisions** (Category 5, prohibited).

## 11. Deterministic automation responsibilities

Delegation enforcement in the authorization model; key-person coverage checks; training-prerequisite gates on authority activation; case routing by skill; access deprovisioning on role change or termination (same day).

## 12. Human oversight requirements

All people decisions are H. The board Governance Committee approves executive compensation (§4958 process) and reviews the delegation register annually. CEO approves role and authority design.

## 13. Exception management

Coverage breach; an authority used without valid training evidence (blocked at the gate, so the case is informational); reviewer calibration failure; agent owner vacancy (agent auto-restricted to Category 2 until an owner is assigned).

## 14. Security and compliance controls

- Background checks for privileged roles.
- Joiner, mover and leaver automation with same-day deprovisioning.
- Privileged access is just-in-time.
- Annual SoD conflict scan of the delegation register.
- Conflict-of-interest disclosures integrated with the relationship graph (ACT-049).

## 15. Estimated staffing implications

**Drivers:** the structural floor (SoD pairs, board committees); exception volume × handle time / productive hours; agent families (owners); institutions (relationship managers).

**Direction:**
- Headcount scales with *exception volume and institutions*, not with accounts.
- The ratio of specialists to total staff rises sharply compared with the conventional structure.
- Numeric FTE by function and scale come from the F# staffing model in [`../../09-financial-models/`](../../09-financial-models/).

## 16. Cost and performance model

| Metric | Target [A] |
|---|---|
| Share of staff in judgment, specialist or supervision roles | ≥ 70% |
| Key-person coverage for critical authorities | 100% with ≥ 2 holders |
| Reviewer inter-rater agreement on sampled H decisions | ≥ 90% (below → calibration) |
| Time from role change to authority deprovisioning | Same business day |

## 17. Implementation dependencies

Delegation register as a policy object (C5.1, C5.4); case routing (C5.3); QA sampling (C6.2); agent scorecards (05-); compensation comparability source; vendor surge contracts.

## 18. Measurable success criteria

- Zero authorities exercised without training evidence.
- Zero SoD conflicts in the register.
- Exception SLA attainment ≥ 95% at forecast volume.
- Twin-forecast capacity within ±15% of measured [A].
- Every agent family has an owner 100% of the time.
