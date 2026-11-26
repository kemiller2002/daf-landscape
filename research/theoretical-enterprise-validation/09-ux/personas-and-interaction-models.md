# Personas and theoretical interaction models

**Status:** theoretical [T]. No user research was conducted. Personas are analytical constructs derived from the requirements, not observations of real users. The UX v0.2 rule applies: "Establish baselines before setting performance targets. Document user disagreement rather than flattening it."

## 1. Persona model

The baseline names roles but has no persona for users with disabilities, external auditors, charities as users, executors/trustees, or board members ([TVF-050](../16-registers/findings.csv)). Added rows are marked **+**.

| Persona | Authority | Information needs | Likely errors | Accessibility / access needs | Recovery needs |
|---|---|---|---|---|---|
| P1 Donor, experienced, desktop | Recommend (if advisor) | Available-to-recommend, grant status, tax documents | Treats "available" as cash; expects instant payment | — | Cancel a mistaken grant before payment |
| **+**P2 Donor, older, low technical familiarity, phone | Recommend | Plain status; who to call | Duplicate submission after slow response; misreads % grant | Large text, 400% zoom, no time limits without extension, accessible authentication without puzzles, phone fallback | Human contact path that sees the same status |
| **+**P3 Donor using a screen reader | Recommend | Same as P1 | Misses a live status change; allocation table hard to verify | Table alternatives; restrained live regions; no drag-only allocation; deterministic focus | Review screen that reads the full effect in sequence |
| **+**P4 Donor with cognitive disability or under stress (e.g. bereavement) | Recommend or successor | Short steps; confirmation of what happened | Abandons multi-step flows; confuses recommend vs pay | Plain language; saved progress; no irreversible step without a summary | Undo window where policy allows (withdraw before decision) |
| P5 Professional advisor, many clients | Recommend or view for many funds; investment proposal | Cross-client dashboard, rights per fund | Acts in the wrong client context | Keyboard-heavy power use | Clear context indicator; context switch invalidates drafts (TVC-011) |
| P6 Co-advisor (spouse) | Joint recommend | What the other advisor did | Conflicting recommendations | — | Visible pending claims (REC-1) |
| **+**P7 Successor (nominated, not active) | None until activation | What happens next; what evidence to send | Assumes access on nomination | Sensitive-document upload; accessible during bereavement | Status of verification |
| **+**P8 Executor / trustee / POA holder | Per instrument | Scope of their authority | Exceeds scope | Documented-instrument intake | Explanation of a denied action |
| **+**P9 Donor's AI agent (delegated principal) | Recommend within caps | Machine-readable status, policy errors | Prompt-injected recommendations | Machine API | Revocation by donor; confirmation requests |
| P10 Grant specialist | Decide referred cases within DoA | Evidence package, contradictions | Automation bias (FM-04) | — | Re-open with new evidence |
| P11 Sanctions officer | Clear true-match flags | Match details, list version | Clearing under time pressure | — | Escalation to GC |
| P12 Payment operations | Release payments; handle Unknown | Attempt history; provider status | Retrying an Unknown | — | Provider query tool; PA-2 decision path |
| P13 Controller / reconciler | Post adjustments; resolve breaks | Three-way view | Writes off its own breaks (TVC-005) | — | Reversal entries |
| P14 Compliance lead / CRCO | Publish policy (not author) | Back-test impact | Approves an untested parameter | — | Policy rollback |
| **+**P15 External auditor (CPA, SOC examiner) | Read-only, scoped, time-bound | Population, samples, control evidence, as-known-at views | Samples from a projection rather than the record | Exportable evidence | Evidence provenance trail |
| **+**P16 Regulator / state AG examiner (through counsel) | None directly | Produced records | — | — | Legal-hold-aware production |
| **+**P17 Charity finance staff | None over funds; manages own payment profile | Grant ID, remittance, who sent it | Updates bank details via email (fraud vector) | — | Verified re-enrolment; return explanation |
| **+**P18 Board / committee member | Approve DoA, policies, exceptions above threshold | Decision packages; conflicts | Approves without seeing conflicts | — | Recusal and re-vote |
| P19 Partner administrator | Partner configuration; no donor data | Integration health, origins | Registers wildcard origin | — | Sandbox and rollback |
| P20 Platform support staff | JIT, time-limited access | Case context | Over-broad access | — | Access logged and reviewed (AUTH-10) |
| **+**P21 Custodian / payment provider operations (external) | None in the platform | Instruction details, correction requests | Duplicate processing | — | Contracted query and correction channels |

## 2. Interaction models for critical workflows

### 2.1 Grant recommendation (P1–P6, P9)

| Element | Requirement |
|---|---|
| Objective | Recommend a grant that the sponsor can approve and pay |
| Entry points | Fund home; charity search; prior-grant "repeat"; partner widget; agent API |
| Required info | Recipient (resolved identity); amount or % with denominator; purpose; anonymity |
| Decision support | Recipient eligibility source and date; estimated available amount (labelled estimate, FI-06); policy limits; expected timing **only if measured** (vertical slice rule) |
| Validation | Field level and server preview; preview hash expires; amount ≤ estimated capacity is a warning, not a guarantee |
| Loading/pending | Submitting → receipt; on timeout → "Confirming whether we received it" (command Unknown), **no resubmit button** until resolved |
| Confirmation | Review screen in reading order: sponsor, fund, recipient legal name and EIN, amount (fixed or "about $X"), funding sources, purpose, "Sponsor approval required; this is not a payment" |
| Errors | UX-F07/F10/F11/F13 |
| Conflict | Co-advisor recommendation on the same capacity: shown as pending claim (REC-1) |
| Recovery | Withdraw before decision; cancellation request after |
| Notifications | Decision; payment sent; paid; returned; hold (non-sensitive class). No amounts or recipient names in push previews (content governance rule) |
| Audit visibility | Donor sees who submitted (self, co-advisor, agent) and when |
| Accessibility | P2–P4 needs above |
| Mobile | Four steps, one action per screen, bottom action bar clear of keyboard |
| Embedded | W02; host gets only opaque events |

### 2.2 Successor activation (P7, P8, P10)

| Element | Requirement |
|---|---|
| Entry | Notice-of-death form, phone, or letter. The form requires no login (the notifier may not be a user). |
| Required info | Decedent identity, relationship, evidence upload, notifier contact |
| Pending | "We received your notice on D. Grant activity on this fund is paused while we verify." Successor sees nothing of the fund until `Active`. |
| Errors | Evidence unreadable → accessible alternative request (UX-F17) |
| Recovery | Dispute path; contact named case owner |
| Accessibility | P4 bereavement: plain language, no time pressure, phone alternative |

### 2.3 Payment Unknown resolution (P12)

| Element | Requirement |
|---|---|
| Entry | Exception queue item `PaymentStatusUnknown` |
| Info | Attempt ID, provider key, submitted time, all provider responses, query results, bank statement match status |
| Actions | Query provider (D); mark observed (evidence required); request provider proof of non-receipt; **escalate for duplicate-risk decision** (PA-2). "Retry" does not exist as a button. |
| Audit | Every action logged with evidence |

### 2.4 Referred grant decision (P10, P11)

| Element | Requirement |
|---|---|
| Info | Evidence package: deterministic rule results, AI flags (visually and semantically distinct), contradictions first, sources with snapshot links |
| Actions | Approve within DoA; decline with reason class; request information; escalate; recuse |
| Automation-bias control | Seeded known-answer cases (CTL-046) indistinguishable from real ones; AI summary hidden until the reviewer has opened the evidence (proposal, TVR-UX-006) [T] |

## 3. Alternative interaction models

Scoring per directive criteria: clarity (Cl), accessibility (Ac), error prevention (EP), auditability (Au), operating cost (OC). Scale: + better, 0 neutral, − worse, relative to the form-driven baseline. These are judgments [I], not measurements.

### 3.1 Grant recommendation

| Model | Cl | Ac | EP | Au | OC | Notes |
|---|---|---|---|---|---|---|
| A. Form-driven (single page) | 0 | 0 | 0 | 0 | 0 | Baseline; long form on mobile |
| B. Guided task (W02 four steps) | + | + | + | 0 | 0 | Current proposal; best for P2–P4 |
| C. Conversational AI ("give $500 to the food bank I gave to last year") | − to + | − (voice) / + (some cognitive) | − | − | − | Resolution ambiguity is the dominant error; conversation must end in the B review screen as a deterministic confirmation. AI never "submits" from free text. |
| D. Proactive / no screen: "repeat last year's grants" one-tap batch | + | + | + (known recipients) | 0 | + | Strong for the majority repeat case [I: repeat-recipient share is not measured in the repository]. Needs per-item review list. |
| E. Delegated (advisor or agent prepares, donor confirms) | + | + | + | + | + | Confirmation step is the control (TVC-026) |

**Conclusion [I]:** B is the base. D and E remove most screens for repeat behaviour. C is an *entry point* into B, not a replacement. Whether a screen is needed at all: for repeat grants to known recipients under the routine path, a confirmation list (D) is sufficient.

### 3.2 Fund opening

| Model | Notes |
|---|---|
| A. 20-field form | Baseline experiment A comparator |
| B. Evidence-led prefill (from partner, KYC, prior relationship) and progressive questions | Fewer fields; risk of wrong prefill accepted without reading (automation bias at the donor) |
| C. Advisor-initiated, donor-confirmed | Fits channel-led distribution (DD-010); donor confirmation must be the donor's own session (no advisor-asserted consent) |

### 3.3 Exception handling (staff)

| Model | Notes |
|---|---|
| A. Departmental queues | Rejected (DD-013) |
| B. Single queue with evidence package | Baseline |
| C. Exception-driven with no queue for routine; staff see only aged or high-severity items; everything else is auto-routed to the requester for missing information | Lowest staff load; risk that requester-facing "missing info" loops become the hidden queue. Measure requester abandonment. |

## 4. Accessibility findings

| ID | Finding |
|---|---|
| UXA-1 | No accessibility persona and no assistive-technology/browser test matrix (traceability only says "tested assistive technologies"). |
| UXA-2 | WCAG 2.2 criteria with direct financial-flow impact are not named: 3.3.7 Redundant Entry (multi-step grant), 3.3.8 Accessible Authentication (step-up for sensitive actions), 2.4.11 Focus Not Obscured (sticky bottom action bar on mobile). |
| UXA-3 | Step-up authentication (TVC-025 resolution) must offer an accessible phishing-resistant method. Passkeys generally satisfy 3.3.8 [I]. Hardware keys may not suit P2/P4. |
| UXA-4 | Session expiry during the review step loses the preview hash. The resumed flow must restore the draft and regenerate the preview without re-entry (3.3.7). |
| UXA-5 | Generated documents need a tagged-PDF conformance target (PDF/UA is named nowhere). |
| UXA-6 | Charities (P17) are users of remittance and re-enrolment flows; those flows are not in the UI inventory at all. |
