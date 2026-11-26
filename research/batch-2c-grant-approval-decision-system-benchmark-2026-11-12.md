# Batch 2C: Grant approval decision-system benchmark and falsifiable experiment
**Date:** 2026-11-12
**Research register:** V12–V18, C01–C04
**Status:** BENCHMARK SPECIFICATION COMPLETE; NO EXPERIMENTAL RESULTS CLAIMED.

## Research question
Which intervention improves sponsor-controlled DAF grant processing without increasing impermissible approvals, wrongful denials, or lost auditability?
A. **Structured intake**: clear donor-facing fields, dynamic guidance, immediate validation, targeted missing-data prompts.
B. **Deterministic rules**: same intake plus versioned eligibility/purpose rules, explainable triage, human exception queue.
C. **AI-assisted reviewer**: same intake and deterministic controls plus LLM evidence summarization, ambiguity identification, suggested disposition and cited rationale. **AI cannot execute final grant authorization**.

**Critical design control:** Compare A/B/C on identical synthetic cases, common policy versions, same reviewer training, same source snapshots and common payment assumptions. Use counterbalanced assignment across reviewers to reduce learning effects. Also include baseline D: existing generic form/manual review where obtainable. Distinguish simulations from live production.

## Decision state machine
DRAFT → SUBMITTED → IDENTITY_VERIFIED → ELIGIBILITY_CHECKED → PURPOSE_REVIEWED → (NEEDS_INFORMATION | EXCEPTION_REVIEW | READY_FOR_AUTHORIZATION) → (APPROVED | DENIED) → LIQUIDATION_PENDING → FUNDS_AVAILABLE → PAYMENT_QUEUED → SENT → (SETTLED | RETURNED | REISSUE_PENDING) → CLOSED.
Separate: **recommendation**, **risk screening**, **sponsor approval**, **liquidation**, **payment**, **recipient reconciliation**. 'Approved' must never be inferred from 'eligible' or 'funded'. Each transition needs actor/authority, policy version, source provenance, timestamp, reason and override trace.

## 20 synthetic grant cases and adjudication expectations
**These are review triggers, not universal legal conclusions.** Expected outcome means route and required evidence; final sponsor decision must follow its own current policy and legal review.
| ID | Case | Initial expected route / evidence |
|---|---|---|
| G01 | Established US 501(c)(3) public charity, general support, verified account | Low-risk eligibility/purpose checks; candidate for straight-through review subject to sponsor authority |
| G02 | Church absent from IRS public lookup | Exception: alternative church verification; do not auto-deny |
| G03 | Government school district | Exception: government-unit eligibility and public-purpose review |
| G04 | Private operating foundation | Verify precise classification and sponsor policy; no blanket eligibility assumption |
| G05 | Type III supporting organization | Escalate to legal/policy review; distinguish disqualified forms |
| G06 | IRS auto-revoked organization | Check effective date, reinstatement and legal eligibility; hold pending resolution |
| G07 | Newly established unlisted nonprofit | Request determination/other permissible evidence; manual review |
| G08 | EIN and legal-name mismatch | Identity resolution, parent/subordinate and alias verification |
| G09 | Local chapter with parent EIN | Verify grantee legal entity and correct disbursement payee |
| G10 | Foreign NGO direct grant | International grant policy, equivalency/expenditure responsibility or intermediary; enhanced review |
| G11 | US public-charity intermediary with overseas program | Verify US intermediary and purpose; distinguish from direct foreign grant |
| G12 | Ordinary unrestricted program grant | Confirm permissible charitable purpose and restrictions |
| G13 | Gala tickets / admission or membership benefit | Donor benefit check; typically reject impermissible benefit, evaluate facts |
| G14 | Binding personal pledge fulfillment | Sponsor policy/legal escalation; do not assume donor may satisfy personal obligation |
| G15 | Nonbinding pledge indication | Distinguish from enforceable obligation; verify sponsor policy |
| G16 | Scholarship where donor selects individual | Escalate prohibited earmarking/private benefit risk |
| G17 | Political campaign purpose | Escalate/reject impermissible political activity |
| G18 | Weakly sourced public allegation about charity | Human corroboration, evidence grading, no automatic reputational denial |
| G19 | Verified repeat charity, changed bank account | Payment-identity and change-control review despite past eligibility |
| G20 | Recurring grant, charity status changed since last payment | Re-screen and hold if unresolved; recurring authorization does not override new facts |

## Data dictionary and traceability
Required inputs: case_id, sponsor_policy_id/version, donor_fund_id (synthetic), requestor_authority, requested_amount, recommendation_date, grantee_legal_name, EIN/jurisdiction_id, DBA/parent linkage, purpose_text, purpose_category, donor_benefit_flag, pledge_flag, recipient_type, cross_border_flag, payment_destination_id, bank_change_flag, anonymity_choice, available_balance, liquidity_route.
Evidence records: evidence_id, source_name, source_url_or_snapshot, as_of_date, retrieved_at, status, confidence, reviewer_notes, contradiction_ids.
Decisions: rule_id, trigger, result (pass/fail/unknown), reason, exception_owner, human_approver, approval_scope, appeal_path.
Events: event_id, actor, role, timestamp, previous_state, new_state, policy_version, evidence_hash, reason_code, correlation_id.

## Measurable outcomes
Primary safety: **impermissible approval rate** and **wrongful denial rate** against an independently adjudicated case-level reference; stratify by risk type. Do not optimize speed by allowing unsafe autoapproval.
Operational: reviewer active minutes, donor follow-up count, first-pass complete rate, total elapsed time submission→approval, approval→funding, funding→settlement; median/P90/P99 separately.
Quality: agreement with reference, correct escalation, evidence coverage, unsupported factual assertions, source freshness, reversibility, override audit completeness.
Economics: loaded reviewer cost per grant, donor support effort, technology and data cost, exception handling, failed-payment cost; report payer vs beneficiary.
Fairness: disparate false-denial patterns for churches, small nonprofits, new organizations, foreign programs and groups with nonstandard records; avoid assuming all unusual cases are suspect.

## Experimental protocol
1. Independently prepare sponsor-specific expected disposition with counsel/compliance review; label disagreements rather than forcing a false gold standard.
2. Freeze policy version, evidence snapshot and synthetic case inputs; preregister measures and unacceptable error thresholds.
3. Give each approach the same information and donor context; log extra questions each asks.
4. Run at least 3 trained reviewers per condition where feasible, rotate case order, record active time and interruptions separately.
5. For AI: prohibit tool-based submission, grant approval and external payment; require source-grounded rationale and abstention when evidence insufficient.
6. Include adversarial variants: prompt injection in charity web text, stale IRS status, conflicting EIN, fabricated determination letter, spoofed bank-change notice, duplicate submission, and misleading charity names.
7. Report per-case results, confidence intervals where sample permits, and total cost; **20 cases are a pilot, not a population-level performance study**.
8. Test end-to-end payment and reconciliation in a safe mock environment separately from legal approval adjudication.
9. Require sponsor approval before any real-data access or production experiments.

## Hypotheses and disconfirming observations
- H1 **Intake-first dominates:** A cuts missing-data follow-ups more cheaply than C. Falsify if A leaves most labor in substantive policy review.
- H2 **Rules capture ordinary cases:** B reduces active reviewer time without increasing incorrect approvals. Falsify on frequent ambiguous policy exceptions.
- H3 **AI adds value in exceptions:** C improves evidence synthesis and reviewer accuracy for G05/G10/G18. Falsify if hallucinations, reviewer verification and governance cost outweigh gains.
- H4 **Payment controls are separate bottleneck:** G19 and funding states remain costly after better vetting. Falsify if most delay is prior to sponsor approval.
- H5 **New/small charities face avoidable friction:** G02/G07/G09 show higher false denials with naive IRS lookup. Falsify with verified alternate-eligibility pathways.
- H6 **Sponsor-specific policy is the binding constraint:** same case produces legitimate differences among sponsors. Falsify if verified policies and outcomes converge.

## Clarity assessment
**Observation:** Ren separates vetting, staff authorization and divestment; Chariot reserves grant decisions to sponsor; IRS data covers only part of eligibility.
**Inference:** Decision provenance and workflow coordination may be more differentiated than standalone lookup.
**Not yet established:** which approach saves the most money, which vendor has the best technology, automation rates, actual sponsor turnaround or ROI.
**Potential counterargument:** vendors may already implement sophisticated exception queues, making an independent orchestration layer redundant. Obtain demos, APIs and real case distributions.

## EDF failure chains
Ambiguous donor input→wrong recipient identity→incorrect tax classification→purpose overlooked→unjustified approval→payment misdirection→irreversible harm.
Alternative chain: overly rigid screening→false denial of church/new charity→rework and donor frustration→slow grant delivery.
Controls: evidence snapshots, explicit UNKNOWN, policy versioning, risk-tier routing, human authorization, bank-change verification, idempotency, settlement reconciliation and appeal.

## Provider verification questions
For Ren, TIFIN Give, Chariot, NPT, Fidelity, Vanguard, DAFgiving360, AEF, Foundation Source and community foundations ask:
1. Which stages are automated vs staff-reviewed? Give denominator and trailing 12-month share.
2. Who legally authorizes grants, with what delegated thresholds?
3. Which source datasets, refresh schedules and manual alternate-verification paths?
4. Which exceptions cause the most delay and what are median/P90/P99 per stage?
5. Can approval evidence and decisions be exported with policy versions and override history?
6. How do adviser-managed liquidity, payment verification and returns alter grant timelines?
7. What is cost per grant by stage and who bears it?
8. Which controls handle donor benefits, foreign recipients, sanctions, supporting orgs and changed bank details?

## Next work package
Create a provider-by-provider evidence matrix with source URLs and explicit unknowns; draft synthetic fixture JSON schema and deterministic baseline rules; collect current public forms and policy versions. Run actual experiment only with access to real systems or an explicitly labeled prototype. No numerical performance claims until then.
