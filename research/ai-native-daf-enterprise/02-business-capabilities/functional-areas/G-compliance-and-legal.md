# G. Compliance and legal

**Capabilities:**
- C5.1 Policy-as-code
- C5.2 Screening and fraud
- C4.5 Evidence and audit
- C5.4 Governance and delegations (with area L)

**Outcomes:** O-07, O-08, O-10, O-17.

**Accountable:**
- General Counsel: law into policy, and inquiries.
- Chief Risk and Compliance Officer: controls and evidence.

**Companion:** [`../../08-governance-and-compliance/regulatory-applicability-map.md`](../../08-governance-and-compliance/regulatory-applicability-map.md) and its matrix CSV. They establish *which* requirements apply. This file designs *how* the enterprise satisfies them.

## 1 Existing industry operating model

**Federal status** ([industry report §6](../../../DAF-INDUSTRY-REPORT-2026-11.md)):
- The 2023 proposed §4966 regulations (REG-142338-07) are neither final nor withdrawn.
- The 2026–27 Priority Guidance Plan reframes the project as "guidance under sections 4966 and 6033 regarding certain DAF arrangements".
- OBBBA (2025) adds a 0.5%-AGI floor and a 35% cap, and excludes DAF gifts from the nonitemizer deduction.
- The ACE Act and the IRA-to-DAF QCD bills are not enacted.
- No DAF-specific SEC or FINRA rule was found.

**States:**
- A 51-jurisdiction search found no 2021–2026 state payout, reporting or donor-intent mandate; Connecticut was not checked ([`gap19-state-law-50-state-check.md`](../../../mission-2026-11-14/gap19-state-law-50-state-check.md); strategic synthesis §0 A).
- State charity registration: Colorado and Connecticut have open data; other states require manual lookups ([`b50-02-state-registration.md`](../../../mission-2026-11-14/b50-02-state-registration.md)).

**Litigation.** No private donor suit has succeeded (*Pinkert*, *Fairbairn*). *Keefer* applies a strict acknowledgment rule. Peterson v. WaterStone is pending. AG actions are pending ([`b50-01-daf-litigation.md`](../../../mission-2026-11-14/b50-01-daf-litigation.md); industry report §11.9).

**Fraud.** No public DAF diversion case since 2021 was found. MFA is published at 3 sponsors ([`b49-04-fraud-diversion-controls.md`](../../../mission-2026-11-14/b49-04-fraud-diversion-controls.md)).

**Discretionary action.** Sponsors used discretion beyond tax exposure in 2026 (SPLC holds). Sixteen AGs wrote to the three largest sponsors (industry report §4).

**Assurance.** None of 13 vendors publishes a scoped SOC report (strategic synthesis §0 C).

**AI.** First-party reading of 13 of 20 entities found none documenting AI in approval, eligibility or money movement (strategic synthesis §0 B).

**Conventional practice** [I]:
- Policy manuals in prose.
- Periodic attestation surveys.
- Per-grant manual lookups.
- Bank-style AML procedures adopted by convention.
- Evidence assembled for each audit.

## 2 Actual required business outcomes

1. Every applicable obligation is known, owned and mapped to at least one operating control (O-07).
2. Every control produces evidence continuously, and that evidence can be produced on request (O-07, O-12).
3. Policies stay consistent with law. A change in law reaches the affected policies, workflows and content in days, not quarters (O-07, O-18).
4. Sanctions, fraud and prohibited-benefit risk stay within the board's appetite (O-08).
5. Regulator, AG and auditor inquiries are answered accurately and quickly (O-07).
6. The sponsor can defend each decision with what it knew at the time (bitemporal records) (O-06, O-07).

## 3 Legal and risk constraints

**The design principle is applicability, not assumption.** A requirement enters the obligation register only with a citation and an applicability determination from the regulatory map. The map distinguishes three kinds:

| Kind | What it means | Examples |
|---|---|---|
| **Legal obligations** | Required by law | Ch. 42 excise taxes; acknowledgment content; 990 and Schedule D; OFAC; state registration; record retention |
| **Internal risk controls** | Chosen by the sponsor | Identity assurance levels; discretionary holds; review thresholds; MFA |
| **Conventions** | Habit, often mistaken for law | Bank-style BSA programs, if counsel confirms a charity is not a BSA financial institution (ACT-048); blanket manual grant review (ACT-017); paper attestations (ACT-046) |

Internal controls are not optional once adopted. The board's risk appetite makes them binding. They are labeled so that they can be **changed through governance** rather than treated as fixed.

Personal liability for managers (§4966(a)(2), §4967(a)(2)) means approval authority in legally sensitive classes must stay with a named human or a deterministic rule that a human approved (DD-002).

## 4 Proposed AI-native operating model

**Compliance becomes a compiled, continuously evidenced control system:**

1. **Obligation register.** Machine-readable `Obligation` records:
   - citation;
   - status (current law, proposed, guidance);
   - scope (sponsor or provider);
   - owner;
   - mapped controls.

   It is seeded from the regulatory matrix (REG- IDs). A **coverage test** fails the build if any current-law obligation lacks a control, or a control lacks an evidence specification.
2. **Policy-as-code (DD-011).**
   - Grant routing, eligibility, acceptance, fees, onboarding facts, agent permissions and retention are versioned decision tables.
   - A prose rendering is generated *from* the rules for staff, donors and regulators, so the text and the behavior cannot diverge.
   - Changes are drafted by the policy drafting and impact agent, back-tested against the historical decision corpus, reviewed by GC, approved by the owner and CRCO, and published by someone other than the author.
3. **Continuous compliance evidence.** Every control emits `Evidence` records to the evidence ledger (C4.5):
   - screening list version and result;
   - eligibility snapshot versions;
   - acknowledgment content-test pass;
   - approval with authority reference;
   - reconciliation status;
   - access reviews.

   An evidence query answers "show every grant approved in Q2 to an organization later revoked, with what we knew at the time" in minutes.
4. **Regulatory change monitoring.**
   - The regulatory change monitor agent watches Federal Register queries, IRS guidance pages, state AG releases and court dockets already tracked in the repository's regulatory tracker.
   - It drafts an impact analysis: which obligations, policies, content clauses and workflows are affected.
   - GC decides (H), and the change follows the controlled change process (O-18).
   - **Proposed rules are modeled but not enforced.** The digital twin runs the proposed §4966 adviser-as-donor-advisor rule against current advisor programs so the sponsor is ready either way.
5. **Screening.**
   - Sanctions screening is deterministic and pinned to the list version, with re-screening on list updates. Near-matches go to triage (P). Only the sanctions officer clears a true potential match (H).
   - Fraud models score; rules hold; humans release.
6. **Inquiries and audits.** Counsel and CRCO answer from evidence queries. Responses are themselves recorded as evidence.
7. **AI governance as compliance.** Every agent has:
   - a permission policy;
   - an evaluation dataset;
   - an owner;
   - a model-risk sign-off by the CRCO;
   - a record of every run (`AgentRun`).

   See [`../../05-agent-architecture/`](../../05-agent-architecture/).

## 5 Eliminated activities

| Activity | Disposition | Replaced by |
|---|---|---|
| ACT-045 prose-only policy manuals | Transformed | Policy-as-code |
| ACT-046 attestation surveys | Eliminated | Continuous evidence |
| ACT-048 bank-style BSA program by convention | Transformed | A risk-based program sized to actual obligations, pending counsel confirmation |
| ACT-050 newsletter-based change monitoring | Transformed | Monitored sources and an impact agent |
| ACT-049 conflict disclosures | Automated | Continuous relationship graph plus annual attestation |
| ACT-047 state registrations | Automated | Deadline tracking; officer signs |

## 6 New workflows

- **WF-G1 Law change → policy change.**
  1. `ComplianceObligationChanged`.
  2. Impact analysis.
  3. Policy draft.
  4. Back-test.
  5. GC review.
  6. Approval.
  7. `PolicyPublished`.
  8. Content re-validation.
  9. Evidence.
- **WF-G2 Sanctions list update.** `SanctionsListUpdated` → re-screen parties, recipients and payment profiles → new hits become cases → holds applied automatically.
- **WF-G3 Regulatory inquiry.**
  1. Intake.
  2. Legal hold.
  3. Evidence query.
  4. Counsel review.
  5. Response.
  6. Evidence recorded.
- **WF-G4 Coverage audit (continuous).** The obligation → control → evidence coverage test runs on every policy publication and nightly. Failures open CRCO cases.
- **WF-G5 State registration cycle.** `RegulatoryDeadlineApproaching` → filing pack assembled from the ledger and governance data → officer signs → receipt recorded.

## 7 Required data

- Obligation register.
- Controls and evidence specifications.
- Policies (versioned).
- The historical decision corpus for back-tests.
- Screening lists with versions.
- Relationship graph.
- Agent registry and evaluations.
- Filing calendar.
- Legal holds.
- Monitored regulatory sources.

## 8 Required APIs

`/v1/policies` (author, back-test, approve, publish, evaluate), `/v1/decisions`, `/v1/evidence`, `/v1/cases`, `/v1/events`, `/v1/reports`, and `/v1/documents` (legal hold).

The evaluate endpoint is commercializable as a compliance policy evaluation service (see [`../../10-market-and-business-model/`](../../10-market-and-business-model/)).

## 9 Event triggers

`ComplianceObligationChanged`, `PolicyPublished`, `SanctionsListUpdated`, `CharityEligibilityChanged`, `RegulatoryDeadlineApproaching`, `AgentPermissionChanged`, `ExceptionCaseResolved` (as evidence), and every decision event (evidence capture).

## 10 AI agent responsibilities

| Agent | Category | Responsibility | Prohibited |
|---|---|---|---|
| Regulatory change monitor | 2 | Watch sources; summarize changes with citations; mark current vs proposed | Changing obligations |
| Policy drafting and impact agent | 2 | Draft rule changes and rendered text; run back-tests; list affected artifacts | Approving or publishing |
| Sanctions near-match triage | 2 | Explain and rank near-matches | Clearing |
| SOC report analyzer | 2 | Map vendor SOC exceptions to enterprise controls | Accepting exceptions |
| Related-party detector | 2 | Detect conflicts and undeclared relationships | Writing relationships |

## 11 Deterministic automation responsibilities

- The coverage test.
- Policy evaluation.
- Back-testing.
- Screening.
- Hold and release gating (release only through H or a policy re-evaluation).
- Evidence capture.
- The deadline calendar.
- Legal-hold enforcement (retention suspension).

## 12 Human oversight requirements

- GC interprets law into policy.
- Approval of policy changes: owner plus CRCO; board for material policies.
- The sanctions officer clears matches.
- Responses to regulators and AGs.
- Approval of agent permissions (CRCO model-risk sign-off).
- Filing signatures.
- An internal audit opinion on control effectiveness.

## 13 Exception management

| Exception | Treatment |
|---|---|
| Coverage test failure | Treated like a failing build: no policy publication until it is resolved or a risk acceptance is recorded by the CRCO with a time limit |
| Sanctions cases | Same-day SLA |
| Regulatory inquiry | Board notice per the delegation register |

## 14 Security and compliance controls

- Author ≠ approver ≠ publisher for policy.
- Evidence ledger append-only, with hash chaining.
- Legal holds override retention deletion.
- Privileged communications segregated.
- The policy engine cannot run unapproved versions in production.
- Agent permission changes require independent evaluation results.

## 15 Estimated staffing implications

**Drivers:**
- number of jurisdictions with registrations;
- volume of sanctions near-matches above the triage threshold;
- regulatory change frequency;
- number of policies and agents requiring sign-off;
- inquiry volume.

**Direction:** compliance analysts who collected attestations and evidence shrink. GC, the CRCO with the sanctions-officer role, and a policy engineer remain. Fractional at small scale. Numeric FTE comes from [`../../09-financial-models/`](../../09-financial-models/).

## 16 Cost and performance model

**Cost drivers:**
- outside counsel hours;
- screening list licensing (OFAC is free; commercial enhanced lists are optional);
- state registration fees;
- the internal audit contract;
- policy engineer time.

**Design targets [A]:**

| Measure | Target |
|---|---|
| Current-law obligations with a mapped control and evidence | 100% |
| Time from regulatory change to approved policy update | Under 30 days for current-law changes |
| Evidence retrieval for any decision | Under 1 hour |
| Missed filings | Zero |

## 17 Implementation dependencies

- Regulatory applicability map (08-).
- Policy engine.
- Evidence ledger.
- Relationship graph.
- Agent registry.
- Counsel engagement.
- Board-approved risk appetite.

## 18 Measurable success criteria

1. Coverage ratio (obligations → controls → evidence).
2. Days from change detection to policy publication.
3. Audit and regulator findings.
4. Sanctions and prohibited-benefit misses found after the fact. Target: zero.
5. Back-test diffs reviewed before publication: 100%.
6. Time to answer an inquiry from evidence.
